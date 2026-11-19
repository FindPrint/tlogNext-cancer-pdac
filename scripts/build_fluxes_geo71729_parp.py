#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bras 2 — contrôle GEO GSE71729 : mêmes 12 gènes de réparation, mêmes
tests directs que TCGA (pas de run v6 sur cette cohorte — contrôle
direct seulement, comme le permet le protocole gelé).
Source : GEO GSE71729, matrice déjà sur disque
(data/GSE71729_series_matrix.txt.gz), plateforme GPL20769 Agilent — les
ID_REF sont déjà des symboles de gènes (vérifié dans
build_fluxes_geo71729.py). Tumeurs primaires uniquement (145, voir
PROVENANCE_geo71729.md). Valeurs : log-expression puce, brutes.
Ordre : KRAS croissant. Nul : lignes permutées, graine 42.
Cas complets seulement, jamais d'imputation.
"""
import gzip
import hashlib
from collections import Counter

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
SEED = 42
GENES = ["PARP1", "PARP2", "BRCA1", "BRCA2", "ATM", "ATR", "CHEK1", "CHEK2",
         "RAD51", "XRCC1", "POLQ", "FANCD2"]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    mat = pd.read_csv(
        f"{DATA}/GSE71729_series_matrix.txt.gz", sep="\t",
        comment="!", index_col=0, low_memory=False)
    mat.index = mat.index.str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    print(f"Matrice : {mat.shape[0]} gènes x {mat.shape[1]} échantillons")
    dup = mat.index.duplicated(keep=False).sum()
    if dup:
        mat = mat.groupby(level=0).median()
        print(f"Symboles dupliqués agrégés par médiane : {mat.shape[0]} gènes uniques")
    gsm_order = list(mat.columns)
    kinds = ["?"] * len(gsm_order)
    with gzip.open(f"{DATA}/GSE71729_series_matrix.txt.gz", "rt",
                   encoding="utf-8", errors="replace") as f:
        ch2 = []
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_characteristics_ch2"):
                ch2.append([v.strip('"') for v in
                            line.rstrip("\n").split("\t")[1:]])
            if line.startswith("!Sample_title"):
                titles = [t.strip('"') for t in
                          line.rstrip("\n").split("\t")[1:]]
    for i in range(len(gsm_order)):
        vals = [row[i] for row in ch2 if i < len(row)]
        joined = " | ".join(vals)
        if "tissue type: Primary" in joined:
            kinds[i] = "Primary"
        elif "tissue type: Metastasis" in joined:
            kinds[i] = "Metastasis"
        elif "tissue type: Normal" in joined:
            kinds[i] = "Normal"
        elif titles[i].endswith("-CellLine"):
            kinds[i] = "CellLine"
    print("Types d'échantillons :", dict(Counter(kinds)))
    prim = [g for g, k in zip(gsm_order, kinds) if k == "Primary"]
    print(f"Tumeurs primaires retenues : {len(prim)}")
    sub = mat[prim]
    present = [g for g in GENES if g in sub.index]
    missing = [g for g in GENES if g not in sub.index]
    print("Gènes PARP présents :", present)
    print("Gènes PARP absents de la puce :", missing)
    assert not missing, f"Gènes absents : {missing}"
    assert "KRAS" in sub.index, "KRAS absent"
    need = ["KRAS"] + present
    cc = sub.loc[need].dropna(axis=1)
    print(f"Cas complets (KRAS + 12 gènes) : {cc.shape[1]} / {len(prim)}")
    assert cc.shape[1] >= 50, "moins de 50 cas complets — arrêt"
    order = cc.loc["KRAS"].sort_values(ascending=True).index
    flux = cc.loc[present, order].T
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_geo71729_fluxes_parp.csv"
    out.to_csv(out_path, index=False)
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_geo71729_fluxes_parp_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes) SHA {sha(out_path)}")
    print(f"Écrit : {nul_path} SHA {sha(nul_path)}")
    print("KRAS (valeurs puce) : min=%.2f médiane=%.2f max=%.2f" % (
        float(cc.loc["KRAS"].min()), float(cc.loc["KRAS"].median()),
        float(cc.loc["KRAS"].max())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
