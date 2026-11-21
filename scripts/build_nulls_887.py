#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construction des 10 nuls frais §8.87 — GDC ORGANOID-PANCREATIC.
Permute le bloc des flux du CSV réel pdac_885_gdc_organoid_fluxes.csv
(même méthode que §8.85 §5.4 : rng(graine), permutation des lignes du
bloc des flux, colonne step intacte) pour les graines gelées 8871-8880
(PROTOCOL_consolidation_gdc_887.md §2). Le CSV réel est LU, jamais
réécrit : son SHA a83b9817…45eaf est vérifié avant et après chaque
graine — tout changement = arrêt, diagnostic, aucun run lancé.
Le constructeur build_fluxes_885.py (original intact) n'accepte pas de
graine arbitraire (il ne construit que 8851/8852 avec --fresh) : il
n'est PAS modifié et PAS invoqué ici.
Sortie : nulls_887_files.json (SHA des 10 CSV de nuls + SHA réel).
Usage : python3 build_nulls_887.py
"""
import hashlib
import json
import os
import sys

import numpy as np
import pandas as pd

PDAC = os.path.dirname(os.path.abspath(__file__))
REAL = os.path.join(PDAC, "pdac_885_gdc_organoid_fluxes.csv")
REAL_SHA = ("a83b98175bdbc33525ba8a175aa898504d2cc44125b891d0902c6c6c2634"
            "5eaf")
SEEDS = [8871, 8872, 8873, 8874, 8875, 8876, 8877, 8878, 8879, 8880]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if sha(REAL) != REAL_SHA:
        print(f"CSV réel inattendu AVANT construction : {sha(REAL)} "
              f"!= {REAL_SHA} — arrêt.", file=sys.stderr)
        return 1
    real = pd.read_csv(REAL)
    if list(real.columns)[:1] != ["step"] or len(real) != 44:
        print(f"CSV réel inattendu : colonnes {list(real.columns)}, "
              f"{len(real)} lignes — arrêt.", file=sys.stderr)
        return 1
    out = {"real_csv": "pdac_885_gdc_organoid_fluxes.csv",
           "real_sha": REAL_SHA, "seeds": SEEDS, "nulls": {}}
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        perm = rng.permutation(len(real))
        nul = real.copy()
        nul.iloc[:, 1:] = real.iloc[:, 1:].to_numpy()[perm]
        nul_path = os.path.join(
            PDAC, f"pdac_885_gdc_organoid_fluxes_nul_s{seed}.csv")
        nul.to_csv(nul_path, index=False)
        if sha(REAL) != REAL_SHA:
            print(f"graine {seed} : CSV réel modifié ({sha(REAL)}) "
                  f"— arrêt, diagnostic.", file=sys.stderr)
            return 1
        if not os.path.exists(nul_path):
            print(f"graine {seed} : CSV nul absent — arrêt.",
                  file=sys.stderr)
            return 1
        out["nulls"][str(seed)] = {
            "file": os.path.basename(nul_path), "sha256": sha(nul_path)}
        print(f"graine {seed} : {os.path.basename(nul_path)} "
              f"SHA {out['nulls'][str(seed)]['sha256'][:8]}… "
              f"(réel inchangé {REAL_SHA[:8]}…)")
    with open(os.path.join(PDAC, "nulls_887_files.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("Écrit : nulls_887_files.json — 10 nuls, réel inchangé.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
