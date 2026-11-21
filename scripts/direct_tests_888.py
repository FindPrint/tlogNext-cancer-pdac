#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests directs §8.88 (ne décident pas, protocole §10) — sur les CSV de
flux du chantier (pdac_888_gse194249_fluxes.csv / _nul.csv). Lecture
seule, aucun run.
1) d de Cohen des 11 flux, réel vs nul graine 42 (gelé §10.2) : le nul
   est une permutation des LIGNES, donc chaque flux garde exactement
   ses 84 valeurs — moyennes et écarts-types identiques, d = 0 par
   construction. Le test ne mesure pas la séparation : il VALIDE la
   construction du nul (marginales préservées exactement). Rapporté
   tel quel, sans en faire un verdict.
2) Test informatif (descriptif, §10.1) : corrélation de Spearman
   de chaque flux avec le pas (ordre KRAS) — réel vs nul. Le nul
   détruit l'ordre, donc rho_nul ≈ 0 (bruit de permutation) ; rho_réel
   mesure la tendance ordonnée par KRAS. C'est ce test qui porte
   l'information d'ordre, pas le d marginal.
Sortie : direct_tests_888.json (+ résumé stdout).
"""
import json
import os

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

PDAC = os.path.dirname(os.path.abspath(__file__))
V4 = ["PGC", "REG4", "CLDN18", "MUC17", "CR2", "KRT20",
      "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]  # 11 flux, DPCR1 absent


def cohen_d(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    n1, n2 = len(a), len(b)
    m1, m2 = float(a.mean()), float(b.mean())
    s1, s2 = float(a.std(ddof=1)), float(b.std(ddof=1))
    sp = np.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
    return (m1 - m2) / sp if sp > 0 else None, m1, m2, s1, s2


def main():
    reel = pd.read_csv(os.path.join(PDAC, "pdac_888_gse194249_fluxes.csv"))
    nul = pd.read_csv(os.path.join(PDAC,
                                   "pdac_888_gse194249_fluxes_nul.csv"))
    assert list(reel.columns) == ["step"] + V4
    assert reel.shape == nul.shape == (84, 12)
    step = reel["step"].to_numpy(dtype=float)
    rows = []
    print("--- (1) d de Cohen marginal, réel vs nul (vacuité par "
          "construction : permutation de lignes) ---")
    for g in V4:
        d, m1, m2, s1, s2 = cohen_d(reel[g], nul[g])
        rho_r = float(spearmanr(step, reel[g]).statistic)
        rho_n = float(spearmanr(step, nul[g]).statistic)
        rows.append({"gene": g, "d_cohen": d, "moy_reel": m1,
                     "moy_nul": m2, "sd_reel": s1, "sd_nul": s2,
                     "rho_step_reel": rho_r, "rho_step_nul": rho_n,
                     "delta_rho": rho_r - rho_n})
        print(f"{g:8s} d={d:+.4f}  rho_step réel {rho_r:+.3f}  "
              f"nul {rho_n:+.3f}  Δrho {rho_r - rho_n:+.3f}")
    ds = np.array([r["d_cohen"] for r in rows])
    dr = np.array([r["delta_rho"] for r in rows])
    out = {"cohorte": "GSE194249 (11 flux, DPCR1 absent)", "n": 84, "flux": rows,
           "d_moyen_abs": float(np.mean(np.abs(ds))),
           "d_max_abs": float(np.max(np.abs(ds))),
           "delta_rho_moyen_abs": float(np.mean(np.abs(dr))),
           "delta_rho_median": float(np.median(dr)),
           "n_delta_rho_positifs": int((dr > 0).sum()),
           "rho_step_reel_moyen_abs": float(np.mean(
               [abs(r["rho_step_reel"]) for r in rows])),
           "rho_step_nul_moyen_abs": float(np.mean(
               [abs(r["rho_step_nul"]) for r in rows]))}
    with open(os.path.join(PDAC, "direct_tests_888.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"--- (2) Spearman vs pas : |rho| moyen réel "
          f"{out['rho_step_reel_moyen_abs']:.3f} contre nul "
          f"{out['rho_step_nul_moyen_abs']:.3f} ; Δrho médian "
          f"{out['delta_rho_median']:+.3f} ; Δrho positifs "
          f"{out['n_delta_rho_positifs']}/11")


if __name__ == "__main__":
    main()
