#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests directs §8.58 (harnais, hors pipeline) — même méthode que
§8.34/§8.36/§8.45. Pour chaque groupe (G1, G2, G3, G4, G5, TEMOIN) et
chaque ordre (kras, stage), réel et nul aux mêmes indices :
- D1 : top-12 contre reste, d de Cohen par flux.
- D2 : contrastes par groupes (stade : IV vs I, III+IV vs I+II ;
  kras : tertile haut vs tertile bas), d + Mann-Whitney bilatéral.
- D3 : Spearman rho de chaque flux contre le rang de contrôle
  (stade 1-4 ; kras : pas/step 0..177).
Sortie : direct_tests_858.csv (+ résumé imprimé).
"""
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr

OUT = "/home/hatch/workspace/runs/pdac-v6"
GROUPS = ["G1", "G2", "G3", "G4", "G5", "TEMOIN"]


def cohen_d(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    sp = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    if sp == 0 or not np.isfinite(sp):
        return 0.0
    return float((a.mean() - b.mean()) / sp)


def main():
    rows = []
    for g in GROUPS:
        for ordre in ("kras", "stage"):
            real = pd.read_csv(f"{OUT}/pdac_tcga_858_{g}_{ordre}.csv")
            nul = pd.read_csv(f"{OUT}/pdac_tcga_858_{g}_{ordre}_nul.csv")
            assert len(real) == len(nul)
            ctrl = real.columns[0]
            fluxes = list(real.columns[1:])
            n = len(real)
            # D1 : top-12 vs reste
            top_idx = np.arange(n - 12, n)
            rest_idx = np.arange(0, n - 12)
            # D2
            if ordre == "stage":
                st = real[ctrl].values
                g_hi = np.where(st == 4)[0]
                g_lo = np.where(st == 1)[0]
                g_hi2 = np.where(st >= 3)[0]
                g_lo2 = np.where(st <= 2)[0]
                d2_label = ("IV_vs_I", "III+IV_vs_I+II")
            else:
                third = n // 3
                g_hi = np.arange(n - third, n)
                g_lo = np.arange(0, third)
                g_hi2, g_lo2 = g_hi, g_lo
                d2_label = ("tertH_vs_tertB", "tertH_vs_tertB")
            ctrl_rank = real[ctrl].values.astype(float)
            for f in fluxes:
                r = {"groupe": g, "ordre": ordre, "flux": f, "n": n}
                for tag, df in (("reel", real), ("nul", nul)):
                    x = df[f].values.astype(float)
                    r[f"d1_top12_{tag}"] = cohen_d(x[top_idx], x[rest_idx])
                    r[f"d2a_{tag}"] = cohen_d(x[g_hi], x[g_lo])
                    try:
                        r[f"d2a_p_{tag}"] = float(mannwhitneyu(
                            x[g_hi], x[g_lo], alternative="two-sided").pvalue)
                    except ValueError:
                        r[f"d2a_p_{tag}"] = float("nan")
                    r[f"d2b_{tag}"] = cohen_d(x[g_hi2], x[g_lo2])
                    try:
                        r[f"d2b_p_{tag}"] = float(mannwhitneyu(
                            x[g_hi2], x[g_lo2], alternative="two-sided").pvalue)
                    except ValueError:
                        r[f"d2b_p_{tag}"] = float("nan")
                    rho, p = spearmanr(ctrl_rank, x)
                    r[f"rho_{tag}"] = float(rho)
                    r[f"rho_p_{tag}"] = float(p)
                rows.append(r)
    out = pd.DataFrame(rows)
    out.to_csv(f"{OUT}/direct_tests_858.csv", index=False)
    print(f"{len(out)} lignes (groupes x ordres x flux)")
    for g in GROUPS:
        for ordre in ("kras", "stage"):
            sub = out[(out.groupe == g) & (out.ordre == ordre)]
            print(f"\n== {g} / {ordre} (n_flux={len(sub)}) ==")
            s = sub.reindex(sub["d1_top12_reel"].abs().sort_values(
                ascending=False).index)
            for _, r in s.head(6).iterrows():
                print(f"  D1 {r['flux']:10s} reel {r['d1_top12_reel']:+.2f} "
                      f"nul {r['d1_top12_nul']:+.2f} | rho reel "
                      f"{r['rho_reel']:+.3f} (p {r['rho_p_reel']:.3g}) "
                      f"nul {r['rho_nul']:+.3f}")
            print(f"  rho reel max |.| : "
                  f"{sub['rho_reel'].abs().max():.3f} ; nul max |.| : "
                  f"{sub['rho_nul'].abs().max():.3f}")
            print(f"  D1 reel max |d| : {sub['d1_top12_reel'].abs().max():.2f} "
                  f"; nul max |d| : {sub['d1_top12_nul'].abs().max():.2f}")


if __name__ == "__main__":
    main()
