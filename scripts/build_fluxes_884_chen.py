#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flux §8.84 — lot drogue Chen 2025, 46 PDO x 63 AUC.
Protocole gele : PROTOCOL_chen2025_drogue_884.md (SHA 62ee265e...).
Matrice : MOESM13 (Supplementary Data 10), SHA 0e009cd5...5340.
Lignes : 46 PDO ordonnes par AUC Gemcitabine croissante (step 0..45).
Flux : les 62 autres drogues, AUC publiees, ordre MOESM13, aucune
transformation, aucune imputation (0 NaN). Controle : step.
Nul : lignes permutees, graine 42, step intact.
Usage : python3 build_fluxes_884_chen.py [--fresh]
  --fresh : construit en plus les nuls frais graines 8841/8842
  (regle gelee §8 — seulement si d_maxsep est proche du plancher ;
  ne jamais construire avant d'avoir lu l'extraction).
"""
import argparse
import hashlib
import sys

import numpy as np
import openpyxl
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
SRC = f"{PDAC}/data/Chen2025_MOESM13_SupplData10.xlsx"
EXPECTED_SHA256 = ("0e009cd56d2f6c25b0b355590becc4abfee3e1080633173bc33606d1bf325340")
EXPECTED_SIZE = 35732
SEED = 42
FRESH_SEEDS = (8841, 8842)
ANCHOR = "Gemcitabine"
BRCA2_NAMED = ["DAC102", "DAC58", "DAC81", "DAC85", "DAC53", "DAC4"]
CFTR_NAMED = ["DAC13", "DAC73", "DAC110", "DAC32", "DAC30"]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fresh", action="store_true")
    args = ap.parse_args()

    # ---- G1 : source ----
    import os
    if os.path.getsize(SRC) != EXPECTED_SIZE or sha(SRC) != EXPECTED_SHA256:
        print("ERREUR : MOESM13 SHA/taille differents de l'empreinte gelee.",
              file=sys.stderr)
        return 1
    print("MOESM13 SHA et taille verifies (empreinte gelee).")

    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
    ws = wb["All Drugs AUC"]
    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    pdos = [c for c in header[2:]]
    drugs = [r[0] for r in rows[1:]]
    # ---- G2 : forme ----
    if len(drugs) != 63 or len(pdos) != 46 or len(set(pdos)) != 46:
        print("ERREUR : forme != 63 drogues x 46 PDO.", file=sys.stderr)
        return 1
    if ANCHOR not in drugs:
        print("ERREUR : Gemcitabine absente.", file=sys.stderr)
        return 1
    arr = np.array([[r[2 + i] for i in range(46)] for r in rows[1:]],
                   dtype=float)
    if int(np.isnan(arr).sum()) != 0:
        print("ERREUR : NaN presents (%d)." % int(np.isnan(arr).sum()),
              file=sys.stderr)
        return 1
    print(f"Matrice : 63 drogues x 46 PDO, 0 NaN ; "
          f"AUC min={np.min(arr):.4f} med={np.median(arr):.4f} "
          f"max={np.max(arr):.4f}.")
    # ---- G3 : organoides nommes presents ----
    # Forme des identifiants : l'article et la Source Data ecrivent
    # DAC102, MOESM13 ecrit DAC_102 — meme identifiant, underscore
    # en plus dans le fichier. Normalisation : suppression de '_'
    # (bijective sur les 46 : chaque DAC_nnn -> un seul DACnnn).
    pdo_norm = {p.replace("_", ""): p for p in pdos}
    assert len(pdo_norm) == 46
    for grp, name in ((BRCA2_NAMED, "BRCA2"), (CFTR_NAMED, "CFTR VUS_D")):
        missing = [d for d in grp if d not in pdo_norm]
        if missing:
            print(f"ERREUR : organoides {name} absents : {missing}",
                  file=sys.stderr)
            return 1
    print("Organoides nommes BRCA2 (6) et CFTR VUS_D (5) tous presents "
          "(DAC102 = DAC_102, etc.).")

    df = pd.DataFrame(arr.T, index=pdos, columns=drugs)
    gem = df[ANCHOR].copy()
    order = gem.sort_values(kind="mergesort").index.tolist()
    print(f"Gemcitabine AUC : min={gem.min():.4f} med={gem.median():.4f} "
          f"max={gem.max():.4f} std={gem.std(ddof=1):.4f} ; "
          f"PDO le plus sensible : {order[0]} ({gem[order[0]]:.4f}) ; "
          f"le plus resistant : {order[-1]} ({gem[order[-1]]:.4f}).")
    fluxes = [d for d in drugs if d != ANCHOR]
    real = df.loc[order, fluxes].reset_index(drop=True)
    real.insert(0, "step", range(len(order)))
    real_path = f"{PDAC}/pdac_884_chen_fluxes.csv"
    real.to_csv(real_path, index=False)
    print(f"Reel : {real.shape[0]} lignes x {real.shape[1] - 1} flux -> "
          f"{real_path} SHA {sha(real_path)[:16]}...")

    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(order))
    nul = real.copy()
    nul.iloc[:, 1:] = real.iloc[:, 1:].values[perm]
    nul_path = f"{PDAC}/pdac_884_chen_fluxes_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Nul graine 42 : permutation {perm[:8].tolist()}... -> "
          f"{nul_path} SHA {sha(nul_path)[:16]}...")
    # controle : marginales preservees exactement
    assert np.allclose(np.sort(real.iloc[:, 1:].values, axis=0),
                       np.sort(nul.iloc[:, 1:].values, axis=0))
    print("Controle nul : marginales preservees exactement "
          "(tri par colonne identique).")

    if args.fresh:
        for s in FRESH_SEEDS:
            r = np.random.default_rng(s)
            p = r.permutation(len(order))
            n = real.copy()
            n.iloc[:, 1:] = real.iloc[:, 1:].values[p]
            fp = f"{PDAC}/pdac_884_chen_fluxes_nul_s{s}.csv"
            n.to_csv(fp, index=False)
            print(f"Nul frais graine {s} -> {fp} SHA {sha(fp)[:16]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
