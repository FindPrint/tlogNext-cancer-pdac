#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flux §8.79 — GDC ORGANOID-PANCREATIC, fichiers tumoraux (n = 44).
Variante (a) : les 12 memes genes que la v4 TCGA, ordre = KRAS
croissant (TPM unstranded GDC), sans correction. Cas complets
seulement. Nul = lignes permutees, graine 42. Protocole
PROTOCOL_nouvelle_serie_879.md.
Usage : python3 build_fluxes_879.py [--fresh]
  --fresh : construit en plus les nuls frais graines 8791/8792
  (regle gelee §4.5/§7 — seulement si d_maxsep est proche du
  plancher ; ne jamais construire avant d'avoir lu l'extraction).
Sources :
  data/gdc_organoid_879/<file_id>.tsv (55 fichiers, MD5 verifies
  par download_gdc_879.py, recu download_gdc_879_receipt.json)
  gdc_organoid_879_file_sample_map.tsv (association fichier ->
  echantillon GDC, API GDC 21 nov. 2026 : 44 Tumor / 11 Normal)
  data/GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST_879.tsv
  (SHA f713edebf...6220b)
Unite d'analyse gelee : le FICHIER (echantillon organoide).
Les 11 fichiers Normal sont exclus. Les 3 cas multi-fichiers
(2, 3 et 4 fichiers tumoraux) entrent tels quels, declares
dans la section §8.79 — aucune agregation.
Portes d'acceptation (protocole §5) : en-tete 9 colonnes,
60 660 lignes de genes + 4 techniques, KRAS present, les 12
genes v4 presents (une ligne chacun, symbole exact), 44
fichiers tumoraux, cas complets >= 40 — sinon sortie 1,
message explicite, et AUCUN run n'est lance.
"""
import csv
import hashlib
import os
import sys
from collections import Counter

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
GDC_DIR = f"{DATA}/gdc_organoid_879"
OUT = "/home/hatch/workspace/runs/pdac-v6"
MAP = f"{OUT}/gdc_organoid_879_file_sample_map.tsv"
MANIFEST = f"{DATA}/GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST_879.tsv"
SEED = 42
FRESH_SEEDS = (8791, 8792)

V4_GENES = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
            "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]

EXPECTED_HEADER = ["gene_id", "gene_name", "gene_type", "unstranded",
                   "stranded_first", "stranded_second", "tpm_unstranded",
                   "fpkm_unstranded", "fpkm_uq_unstranded"]
TECHNICAL_IDS = ("N_unmapped", "N_multimapping", "N_noFeature",
                 "N_ambiguous")
EXPECTED_GENE_ROWS = 60660


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    fresh = "--fresh" in sys.argv
    # ---- 1. Manifeste + table d'association ----
    with open(MANIFEST, newline="", encoding="utf-8") as f:
        mrows = list(csv.DictReader(f, delimiter="\t"))
    assert len(mrows) == 55, f"manifeste : {len(mrows)} lignes"
    with open(MAP, newline="", encoding="utf-8") as f:
        amap = {r["file_id"]: r for r in csv.DictReader(f, delimiter="\t")}
    assert len(amap) == 55, f"table association : {len(amap)} lignes"
    tumor_ids = sorted(fid for fid, r in amap.items()
                       if r["tissue_type"] == "Tumor")
    normal_ids = sorted(fid for fid, r in amap.items()
                        if r["tissue_type"] == "Normal")
    print(f"Manifeste : {len(mrows)} fichiers ; association : "
          f"{len(tumor_ids)} Tumor, {len(normal_ids)} Normal")
    print(f"Fichiers Normal exclus : {len(normal_ids)} "
          f"(cas {(sorted(set(amap[f]['case_submitter_id'] for f in normal_ids)) )})")
    tumor_cases = Counter(amap[f]["case_id"] for f in tumor_ids)
    print(f"Cas sources des fichiers tumoraux : {len(tumor_cases)} ; "
          f"cas multi-fichiers : "
          f"{ {c: n for c, n in tumor_cases.items() if n > 1} }")
    print("Diagnostics des cas tumoraux :",
          dict(Counter(amap[f]["primary_diagnosis"] for f in tumor_ids)))

    # ---- 2. Lecture des 44 TSV tumoraux (colonne tpm_unstranded) ----
    need = ["KRAS"] + V4_GENES
    values = {g: {} for g in need}  # g -> {file_id: tpm}
    n_gene_rows = {}
    dup_other = {}
    n_nan = 0
    for fid in tumor_ids:
        path = os.path.join(GDC_DIR, fid + ".tsv")
        if not os.path.exists(path):
            print(f"MANQUANT : {path}", file=sys.stderr)
            return 1
        with open(path, encoding="utf-8") as f:
            # Premiere ligne : commentaire '# gene-model: ...'
            first = f.readline()
            assert first.startswith("#"), f"{fid} : 1re ligne inattendue"
            header = f.readline().rstrip("\n").split("\t")
            if header != EXPECTED_HEADER:
                print(f"EN-TETE INATTENDU {fid} : {header}",
                      file=sys.stderr)
                return 1
            rows = {}
            n_dup_other = 0
            n_rows_total = 0
            n_tech = 0
            for line in f:
                parts = line.rstrip("\n").split("\t")
                gid, sym = parts[0], parts[1]
                if gid in TECHNICAL_IDS:
                    n_tech += 1
                    continue
                n_rows_total += 1
                if sym in rows:
                    # Doublon de symbole hors des 13 genes utiles :
                    # conserve la premiere ligne, compte seulement.
                    # Un doublon sur un gene utile (KRAS ou v4) = arret.
                    if sym in need:
                        print(f"DOUBLON de symbole utile {sym} dans "
                              f"{fid}", file=sys.stderr)
                        return 1
                    n_dup_other += 1
                    continue
                rows[sym] = parts
            n_gene_rows[fid] = n_rows_total
            dup_other[fid] = n_dup_other
            if n_rows_total != EXPECTED_GENE_ROWS or n_tech != 4:
                print(f"COMPTAGE INATTENDU {fid} : {n_rows_total} lignes "
                      f"de genes, {n_tech} techniques", file=sys.stderr)
                return 1
            for g in need:
                if g not in rows:
                    print(f"GENE ABSENT {g} dans {fid}", file=sys.stderr)
                    return 1
                v = float(rows[g][6])  # tpm_unstranded
                if np.isnan(v):
                    n_nan += 1
                values[g][fid] = v
    print(f"Fichiers lus : {len(tumor_ids)} ; lignes de genes par "
          f"fichier : {set(n_gene_rows.values())} ; symboles en double "
          f"(hors 13 utiles, 1re ligne conservee) : "
          f"{sorted(set(dup_other.values()))} ; NaN sur 13 genes : "
          f"{n_nan}")

    # ---- 3. Portes d'acceptation (protocole §5) ----
    df = pd.DataFrame({g: pd.Series(values[g]) for g in need})
    n_cc = int(df.dropna().shape[0])
    gates = []
    gates.append(("55 fichiers telecharges (MD5 verifies par le recu)",
                  len(mrows) == 55))
    gates.append(("44 fichiers tumoraux", len(tumor_ids) == 44))
    gates.append(("11 fichiers Normal exclus", len(normal_ids) == 11))
    gates.append(("aucun file_id TCGA dans le manifeste",
                  all("TCGA" not in r["file_id"] + r["file_name"]
                      for r in mrows)))
    gates.append(("KRAS present dans les 44 fichiers",
                  all(fid in values["KRAS"] for fid in tumor_ids)))
    gates.append(("12 genes v4 presents (1 ligne chacun)",
                  all(all(fid in values[g] for fid in tumor_ids)
                      for g in V4_GENES)))
    gates.append(("fichiers tumoraux >= 40", len(tumor_ids) >= 40))
    gates.append(("cas complets >= 40", n_cc >= 40))
    print(f"Cas complets (KRAS + 12 genes) : {n_cc} / {len(tumor_ids)}")
    for name, ok in gates:
        print(f"PORTE {'OK ' if ok else 'ÉCHEC'} : {name}")
    if not all(ok for _, ok in gates):
        print("COHORTE INUTILISABLE selon le protocole §5 — arrêt, "
              "aucun CSV écrit, aucun run lancé.", file=sys.stderr)
        return 1

    # ---- 4. Variante (a) : les 12 genes v4, ordre KRAS ----
    df = df.dropna()
    order = df["KRAS"].sort_values(ascending=True).index
    flux = df.loc[order, V4_GENES]
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_879_gdc_organoid_fluxes.csv"
    out.to_csv(out_path, index=False)
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_879_gdc_organoid_fluxes_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes) SHA {sha(out_path)}")
    print(f"Écrit : {nul_path} SHA {sha(nul_path)}")
    print("KRAS TPM (GDC, tpm_unstranded) : min=%.4g médiane=%.4g "
          "max=%.4g" % (float(df["KRAS"].min()),
                        float(df["KRAS"].median()),
                        float(df["KRAS"].max())))
    print("Fichiers retenus (ordre KRAS croissant) :")
    for fid in order:
        r = amap[fid]
        print(f"  {fid} cas={r['case_submitter_id']} "
              f"ech={r['sample_submitter_id']} "
              f"KRAS={df.loc[fid, 'KRAS']:.4g}")
    if fresh:
        for seed in FRESH_SEEDS:
            r2 = np.random.default_rng(seed)
            perm2 = r2.permutation(len(out))
            nf = out.copy()
            nf.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm2]
            p = (f"{OUT}/pdac_879_gdc_organoid_fluxes_nul_s{seed}.csv")
            nf.to_csv(p, index=False)
            print(f"Écrit (nul frais s{seed}) : {p} SHA {sha(p)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
