#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests directs §8.58 confirmations (harnais, hors pipeline) — même
méthode que reading_858.py : D1 top-12 contre reste (d de Cohen),
D3 Spearman rho de chaque flux contre le rang de contrôle (KRAS :
pas/step ; stade GSE62452 : rang 1-4), réel et nul aux mêmes indices.
Cohortes : GSE71729 (KRAS, 145 lignes), GSE62452 (KRAS 69 lignes,
stade 68 lignes). Sortie : direct_tests_858_geo.csv.
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

OUT = "/home/hatch/workspace/runs/pdac-v6"
GROUPS = ["G1", "G2", "G3", "G4", "G5"]


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
    for cohort, ordres in (("geo71729", ("kras",)), ("geo62452", ("kras", "stage"))):
        for g in GROUPS:
            for ordre in ordres:
                real = pd.read_csv(f"{OUT}/pdac_858_{cohort}_{g}_{ordre}.csv")
                nul = pd.read_csv(f"{OUT}/pdac_858_{cohort}_{g}_{ordre}_nul.csv")
                assert len(real) == len(nul)
                ctrl = real.columns[0]
                fluxes = list(real.columns[1:])
                n = len(real)
                top_idx = np.arange(n - 12, n)
                rest_idx = np.arange(0, n - 12)
                ctrl_rank = real[ctrl].values.astype(float)
                for f in fluxes:
                    r = {"cohorte": cohort, "groupe": g, "ordre": ordre,
                         "flux": f, "n": n}
                    for tag, df in (("reel", real), ("nul", nul)):
                        x = df[f].values.astype(float)
                        r[f"d1_top12_{tag}"] = cohen_d(x[top_idx], x[rest_idx])
                        rho, p = spearmanr(ctrl_rank, x)
                        r[f"rho_{tag}"] = float(rho)
                        r[f"rho_p_{tag}"] = float(p)
                    rows.append(r)
    out = pd.DataFrame(rows)
    out.to_csv(f"{OUT}/direct_tests_858_geo.csv", index=False)
    print(f"{len(out)} lignes")
    for cohort in ("geo71729", "geo62452"):
        for g in GROUPS:
            for ordre in ("kras", "stage"):
                sub = out[(out.cohorte == cohort) & (out.groupe == g)
                          & (out.ordre == ordre)]
                if len(sub) == 0:
                    continue
                s = sub.reindex(sub["rho_reel"].abs().sort_values(
                    ascending=False).index)
                print(f"\n== {cohort} {g}/{ordre} (n_flux={len(sub)}) ==")
                for _, r in s.head(5).iterrows():
                    print(f"  {r['flux']:10s} rho reel {r['rho_reel']:+.3f} "
                          f"(p {r['rho_p_reel']:.3g}) nul {r['rho_nul']:+.3f} "
                          f"| D1 reel {r['d1_top12_reel']:+.2f} "
                          f"nul {r['d1_top12_nul']:+.2f}")
                print(f"  rho reel max {sub['rho_reel'].abs().max():.3f} ; "
                      f"nul max {sub['rho_nul'].abs().max():.3f}")


if __name__ == "__main__":
    main()
