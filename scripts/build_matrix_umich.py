#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit la matrice protéique CPTAC PDAC (UMich, PDC000393) au niveau gène.
Protocole gelé (15 nov. 2026) — mission CPTAC :
- Source : Zenodo 8394329 (miroir des données du paquet cptac, lui-même issu
  du PDC PDC000393, Cao et al. 2021, Cell) :
  * umich-pdac-proteomics-Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz
    (20 504 572 o, MD5 vérifié contre Zenodo — voir PROVENANCE_cptac.md)
  * umich-pdac-mapping-aliquot_to_patient_ID.tsv.gz (22 881 o, MD5 vérifié)
- Traitement = logique du paquet cptac (UmichPdac.load_proteomics), reproduite
  ici pour traçabilité : Index -> Database_ID (ENSP, champ 0) et Name (symbole,
  champ 6) ; suppression des colonnes métadonnées ; transposition ; soustraction
  de la ligne ReferenceIntensity (ratios log vs référence) ; suppression des
  QC/références/pools ; correspondance aliquote -> patient (fichier de mapping
  + 8 correspondances manuelles du paquet, toutes normales .N).
- Tumeurs = patient_ID C3L-* SANS suffixe .N. Normales (.N ou C3N-*) exclues.
- Agrégation au niveau gène : médiane des isoformes protéiques d'un même
  symbole (documenté ; seule la médiane est utilisée, jamais une valeur
  inventée). Aucune imputation : une valeur manquante reste manquante.
- Sortie : matrice tumeurs x gènes (CSV) + rapport de couverture des 13 gènes
  cibles (KRAS + 12 flux v4 ARN).
Aucune donnée d'une autre expérience n'entre ici (téléchargement frais
depuis la source publique).
"""
import gzip
import hashlib
import json

import numpy as np
import pandas as pd

BASE = "/home/hatch/workspace/runs/pdac-v6"
UMICH = f"{BASE}/data/cptac/umich-pdac-proteomics-Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz"
MAPF = f"{BASE}/data/cptac/umich-pdac-mapping-aliquot_to_patient_ID.tsv.gz"
OUT = f"{BASE}/data/cptac/pdac_umich_protein_gene_matrix.csv"
REPORT = f"{BASE}/data/cptac/pdac_umich_coverage.json"

DROP_ROWS = ['ReferenceIntensity', 'QC1', 'QC2', 'QC3', 'QC4', 'QC5', 'QC6',
             'KoreanReference1', 'KoreanReference2', 'KoreanReference3',
             'Pool-24-2', 'WU-PDA1', 'WU-Pool-25']
MANUAL = {'CPT0347760002': 'C3L-07032.N', 'CPT0347790002': 'C3L-07033.N',
          'CPT0347820002': 'C3L-07034.N', 'CPT0347850002': 'C3L-07035.N',
          'CPT0347880002': 'C3L-07036.N', 'CPT0355180003': 'C3L-03513.N',
          'CPT0355190003': 'C3L-03515.N', 'CPT0355200003': 'C3L-03514.N'}
TARGETS = ['KRAS', 'CLDN18', 'MUC16', 'CEACAM5', 'PGC', 'DPCR1', 'KRT20',
           'CLCA1', 'CR2', 'REG4', 'MUC17', 'GSTM1', 'MUC2']


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    df = pd.read_csv(UMICH, sep="\t", compression="gzip")
    print("umich brut :", df.shape)
    df['Database_ID'] = df['Index'].apply(lambda x: x.split('|')[0])
    df['Name'] = df['Index'].apply(lambda x: x.split('|')[6])
    df = df.set_index(['Name', 'Database_ID'])
    df = df.drop(columns=['Index', 'MaxPepProb', 'NumberPSM', 'Gene'])
    df = df.T
    ref = df.loc["ReferenceIntensity"]
    df = df.subtract(ref, axis="columns")
    df.index.name = 'aliquot'
    df = df.drop(index=[r for r in DROP_ROWS if r in df.index], errors='ignore')
    print("après nettoyage QC/réf :", df.shape)

    mapping = pd.read_csv(MAPF, sep="\t", compression="gzip",
                          index_col='aliquot_ID', usecols=['aliquot_ID', 'patient_ID'])
    map_dict = mapping['patient_ID'].to_dict()
    map_dict.update(MANUAL)
    unmapped = [a for a in df.index if a not in map_dict]
    print("aliquotes sans correspondance :", len(unmapped), unmapped[:10])
    df = df.rename(index=map_dict)
    df = df.loc[[i for i in df.index if isinstance(i, str) and i.startswith('C3L') and not i.endswith('.N')]]
    print("tumeurs (C3L sans .N) :", df.shape[0], "| doublons patient :",
          int(df.index.duplicated().sum()))
    # Doublons (plusieurs aliquotes pour un même patient) : médiane, documenté.
    df = df.groupby(level=0).median()
    print("patients tumeurs uniques :", df.shape[0])

    # Agrégation au niveau gène : médiane des isoformes.
    gene = df.reset_index().set_index('aliquot') if False else df
    # df a un index multi (Name, Database_ID) en colonnes ; transposer pour agréger
    mat = df.T  # lignes = (Name, Database_ID), colonnes = patients
    mat.index = mat.index.get_level_values('Name')
    gene_mat = mat.groupby(level=0).median()  # médiane des isoformes par gène
    gene_mat = gene_mat.T  # lignes = patients, colonnes = gènes
    gene_mat.index.name = 'patient'
    gene_mat.to_csv(OUT)
    print("matrice gène écrite :", OUT, gene_mat.shape)

    cov = {}
    for g in TARGETS:
        if g in gene_mat.columns:
            v = gene_mat[g]
            cov[g] = {"present": True, "n_valid": int(v.notna().sum()),
                      "n_total": int(len(v)), "min": float(v.min()),
                      "max": float(v.max()), "median": float(v.median())}
        else:
            cov[g] = {"present": False}
    print(json.dumps(cov, indent=1, ensure_ascii=False))
    json.dump({"sha_umich": sha256(UMICH), "sha_map": sha256(MAPF),
               "n_tumors": int(gene_mat.shape[0]), "n_genes": int(gene_mat.shape[1]),
               "coverage": cov}, open(REPORT, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
