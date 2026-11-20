#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.50 — Dix nuls frais pour la série MTAP (graines 1011..11111).
Protocole gelé : PROTOCOL_mtap_consolidation_850.md (écrit avant ce script).
Même méthode que le nul graine 42 (build_fluxes_tcga_v4_mtap.py, lignes
167-169) et que build_mtap_nuls_846.py (graines 7 et 123) : générateur
frais rng(seed), lignes permutées ensemble, colonne de contrôle MTAPCN
intacte. Aucune autre modification. Entrée vérifiée par SHA avant
construction. Graines jamais utilisées pour des nuls MTAP (42, 7, 123
sont les seules antérieures).
Sorties : pdac_tcga_fluxes_v4_mtap_nul_s<graine>.csv (+ SHA).
"""
import hashlib
import os

import numpy as np
import pandas as pd

PDAC = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(PDAC, "pdac_tcga_fluxes_v4_mtap.csv")
SRC_SHA = "578b8d3b9b26099d0784ed23754d1cc9717be7f9292eb47e201d186cdbc90df6"
SEEDS = (1011, 2022, 3033, 4044, 5055, 6066, 7077, 8088, 9099, 11111)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    assert sha(SRC) == SRC_SHA, f"SHA entrée non conforme : {sha(SRC)}"
    out = pd.read_csv(SRC)
    assert len(out) == 177 and list(out.columns)[0] == "MTAPCN"
    assert bool(out["MTAPCN"].is_monotonic_increasing)
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        perm = rng.permutation(len(out))
        assert not np.array_equal(perm, np.arange(len(out))), "permutation identique"
        nul = out.copy()
        nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
        assert (nul["MTAPCN"].to_numpy() == out["MTAPCN"].to_numpy()).all()
        assert not nul.iloc[:, 1:].equals(out.iloc[:, 1:])
        path = os.path.join(PDAC, f"pdac_tcga_fluxes_v4_mtap_nul_s{seed}.csv")
        nul.to_csv(path, index=False)
        print(f"Écrit : {path} (permutation graine {seed}, contrôle intact) "
              f"SHA={sha(path)}")
    print(f"SHA script : {sha(__file__)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
