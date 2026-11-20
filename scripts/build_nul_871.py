#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nuls frais §8.71 (protocole §4.4, graines 8711/8712, gelées avant
tout run) — permutation des lignes du CSV de flux réel, même méthode
que le nul graine 42 de build_fluxes_871.py (rng(seed), contrôle
intact). Lecture seule du CSV réel, aucun run lancé ici.
Usage : python3 build_nul_871.py 8711 8712
Sorties : pdac_871_geo60979_fluxes_nul_s<seed>.csv (+ SHA stdout).
"""
import hashlib
import sys

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
REAL = f"{PDAC}/pdac_871_geo60979_fluxes.csv"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    seeds = [int(s) for s in sys.argv[1:]] or [8711, 8712]
    real = pd.read_csv(REAL)
    print(f"Réel : {REAL} ({real.shape[0]} lignes) SHA {sha(REAL)}")
    for seed in seeds:
        rng = np.random.default_rng(seed)
        perm = rng.permutation(len(real))
        nul = real.copy()
        nul.iloc[:, 1:] = real.iloc[:, 1:].to_numpy()[perm]
        out = f"{PDAC}/pdac_871_geo60979_fluxes_nul_s{seed}.csv"
        nul.to_csv(out, index=False)
        print(f"Écrit : {out} (graine {seed}) SHA {sha(out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
