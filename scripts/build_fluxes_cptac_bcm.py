#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contre-vérification secondaire : flux protéiques CPTAC PDAC (BCM, PDC000393),
52 tumeurs — autre centre que UMich, autre normalisation.
Protocole gelé (15 nov. 2026) — mission CPTAC :
- Entrée : data/cptac/bcm-pdac-proteomics-PDAC_proteomics_gene_abundance_log2_reference_intensity_normalized_Tumor.txt.gz
  (7 382 441 o, MD5 vérifié 988150c28a2c1db14a3c0e62d08c06d2). Lignes = ID gène
  Ensembl ; colonnes = 52 tumeurs C3L + 53 normales C3N (le fichier dit
  « Tumor » contient aussi des normales — seules les C3L sont gardées).
- Carte ENSG -> symbole reconstruite depuis le fichier UMich (champ symbole
  de l'Index, même méthode que build_matrix_umich.py). 11 403/11 404 lignes
  mappées (1 non mappée : ENSG00000143420.19, hors cibles).
- Flux retenus = gènes v4 ARN avec au moins 50 valeurs valides sur 52 tumeurs
  (même règle : jamais d'imputation) : PGC, REG4, CLDN18, KRT20, CEACAM5,
  CLCA1 (6 flux). MUC16 a 48/52 valides — exclue ici (cas complets tomberaient
  à 48 < 50, minimum v6) ; elle est testée dans la matrice UMich (63/68).
  DPCR1 : symbole ambigu, exclu (voir PROVENANCE_cptac.md). CR2 (35/52),
  MUC17 (10/52), GSTM1 (16/52), MUC2 (25/52) : exclus (< 50).
- Cas complets : 52 tumeurs, zéro valeur manquante. Ordre = KRAS protéique
  croissant (axe, jamais flux). Nul = mêmes lignes permutées, graine 42.
- Sorties : pdac_cptac_bcm_fluxes.csv + _nul.csv, SHA-256 notés.
But : tester la moitié « CLDN18 tombe » de la chaîne v4 sur une deuxième
matrice protéique indépendante (autre centre). Ne pas combiner BCM + UMich
(centres et normalisations différents).
"""
import hashlib
import re

import numpy as np
import pandas as pd

BASE = "/home/hatch/workspace/runs/pdac-v6"
BCM = f"{BASE}/data/cptac/bcm-pdac-proteomics-PDAC_proteomics_gene_abundance_log2_reference_intensity_normalized_Tumor.txt.gz"
UMICH = f"{BASE}/data/cptac/umich-pdac-proteomics-Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz"
OUT = f"{BASE}/pdac_cptac_bcm_fluxes.csv"
OUT_NUL = f"{BASE}/pdac_cptac_bcm_fluxes_nul.csv"
FLUXES = ["PGC", "REG4", "CLDN18", "KRT20", "CEACAM5", "CLCA1"]
SEED = 42


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    u = pd.read_csv(UMICH, sep="\t", compression="gzip", usecols=['Index'])
    mapping = {}
    for idx in u['Index']:
        parts = str(idx).split('|')
        ensg = next((p.split('.')[0] for p in parts if p.startswith('ENSG')), None)
        sym = parts[-2] if len(parts) >= 2 else None
        if ensg and sym and not sym.startswith('ENS'):
            mapping.setdefault(ensg, sym)
    b = pd.read_csv(BCM, sep="\t", compression="gzip")
    b['ensg'] = b['idx'].str.split('.').str[0]
    b['gene'] = b['ensg'].map(mapping)
    tumors = [c for c in b.columns if c.startswith('C3L')]
    print("tumeurs C3L :", len(tumors))
    mat = b.set_index('gene')[tumors].T
    mat.index.name = 'patient'
    for g in ["KRAS"] + FLUXES + ["MUC16", "CR2", "MUC17", "GSTM1", "MUC2", "DPCR1"]:
        if g in mat.columns:
            print(f"  {g}: {int(mat[g].notna().sum())}/{len(mat)} valides")
        else:
            print(f"  {g}: ABSENT")
    sub = mat[["KRAS"] + FLUXES].dropna()
    print("cas complets (KRAS + 6 flux) :", len(sub), "tumeurs")
    print("KRAS protéique : min %.2f médiane %.2f max %.2f" % (
        sub["KRAS"].min(), sub["KRAS"].median(), sub["KRAS"].max()))
    sub = sub.sort_values("KRAS").reset_index(drop=True)
    fluxes = sub[FLUXES].copy()
    fluxes.insert(0, "step", np.arange(len(fluxes)))
    fluxes.to_csv(OUT, index=False)
    rng = np.random.default_rng(SEED)
    nul = fluxes.copy()
    nul.iloc[:, 1:] = nul.iloc[:, 1:].values[rng.permutation(len(nul))]
    nul.to_csv(OUT_NUL, index=False)
    print("écrit :", OUT, "SHA", sha(OUT))
    print("écrit :", OUT_NUL, "SHA", sha(OUT_NUL))


if __name__ == "__main__":
    main()
