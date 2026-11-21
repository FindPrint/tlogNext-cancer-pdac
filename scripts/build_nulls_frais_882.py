#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nuls frais §8.82 — règle gelée du protocole (PROTOCOL_cerveau_privilege_882.md §7).
d_maxsep (paire primaire, prolifération) = +0,0283, dans [−0,07 ; +0,14[ :
les 2 nuls frais (graines 8821, 8822) sont courus sur la paire primaire
seulement. Même construction que tous les nuls du dossier (mêmes lignes
permutées, graine donnée). Le verdict de la paire graine 42 n'est JAMAIS
changé par les nuls frais.
"""
import hashlib

import numpy as np
import pandas as pd

BASE = "/home/hatch/workspace/runs/pdac-v6"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out = pd.read_csv(f"{BASE}/pdac_882_gbm_prolif_fluxes.csv")
    for seed in (8821, 8822):
        rng = np.random.default_rng(seed)
        perm = rng.permutation(len(out))
        nul = out.copy()
        nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
        path = (f"{BASE}/pdac_882_gbm_prolif_fluxes_nul_s{seed}.csv")
        nul.to_csv(path, index=False)
        print(f"Écrit : {path} (permutation graine {seed}) "
              f"SHA {sha(path)[:12]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
