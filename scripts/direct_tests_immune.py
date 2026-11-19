#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests directs — paysage immunitaire le long de l'axe KRAS (Bras 1).
Verdict principal du bras (avant la cascade v6, qui ne vaut pas seule) :
- Pour chaque cohorte et chaque gène immunitaire : Spearman rho contre
  l'expression KRAS brute (ordre croissant = axe), avec p bilatérale.
- Top-12 KRAS-fort contre reste : différence des moyennes en écarts-types
  (d de Cohen, SD poolée) + test t de Welch (p bilatérale).
- n_top = 12 partout (même définition que les bras précédents).
Aucune correction pour tests multiples dans le tableau brut ; le rapport
signale les p < 0,05 brutes et le nombre de tests (12 gènes x 4 cohortes
= 48) pour juger la multiplicité. Sorties : immune_direct_tests.csv,
immune_direct_tests.txt.
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, ttest_ind

OUT = "/home/hatch/workspace/runs/pdac-v6"
COHORTS = ["tcga", "geo71729", "geo62452", "icgc"]
TOP = 12


def cohen_d(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    n1, n2 = len(a), len(b)
    s = np.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1)) / (n1 + n2 - 2))
    return float((a.mean() - b.mean()) / s) if s > 0 else float("nan")


def main():
    rows = []
    for tag in COHORTS:
        flux = pd.read_csv(f"{OUT}/pdac_immune_{tag}_fluxes.csv")
        axis = pd.read_csv(f"{OUT}/immune_kras_order_{tag}.csv")
        assert (flux["step"].values == axis["step"].values).all(), f"pas aligné {tag}"
        kras = axis["kras_raw"].values
        assert np.all(np.diff(kras) >= 0), f"KRAS non croissant {tag}"
        genes = [c for c in flux.columns if c != "step"]
        top_idx = np.arange(len(flux) - TOP, len(flux))
        rest_idx = np.arange(0, len(flux) - TOP)
        for g in genes:
            v = flux[g].values.astype(float)
            rho, p_rho = spearmanr(kras, v)
            d = cohen_d(v[top_idx], v[rest_idx])
            _, p_t = ttest_ind(v[top_idx], v[rest_idx], equal_var=False)
            rows.append({
                "cohorte": tag, "n": len(flux), "gene": g,
                "spearman_rho": round(float(rho), 3),
                "spearman_p": float(p_rho),
                "top12_vs_reste_d_cohen": round(float(d), 3),
                "top12_vs_reste_p_welch": float(p_t),
                "moy_top12": round(float(v[top_idx].mean()), 3),
                "moy_reste": round(float(v[rest_idx].mean()), 3),
            })
        print(f"[{tag}] n={len(flux)} top12 vs reste ({len(rest_idx)}) : fait")
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}/immune_direct_tests.csv", index=False)
    with open(f"{OUT}/immune_direct_tests.txt", "w", encoding="utf-8") as f:
        f.write("TESTS DIRECTS — paysage immunitaire le long de l'axe KRAS\n")
        f.write("Top-12 KRAS-fort vs reste ; Spearman vs KRAS brut. "
                "p brutes (48 tests : 12 gènes x 4 cohortes).\n\n")
        for tag in COHORTS:
            sub = df[df["cohorte"] == tag]
            f.write(f"== {tag} (n={int(sub['n'].iloc[0])}) ==\n")
            f.write("gène         rho     p_rho    d_top12  p_welch\n")
            for _, r in sub.iterrows():
                f.write(f"{r['gene']:<12s} {r['spearman_rho']:+.3f}  "
                        f"{r['spearman_p']:.4g}  {r['top12_vs_reste_d_cohen']:+.3f}   "
                        f"{r['top12_vs_reste_p_welch']:.4g}\n")
            sig_rho = sub[sub["spearman_p"] < 0.05]
            sig_d = sub[sub["top12_vs_reste_p_welch"] < 0.05]
            f.write(f"p_rho<0,05 : {list(sig_rho['gene'])} "
                    f"({len(sig_rho)}/12) ; "
                    f"p_welch<0,05 : {list(sig_d['gene'])} ({len(sig_d)}/12)\n\n")
        # Cohérence inter-cohortes : signe du rho par gène.
        piv = df.pivot(index="gene", columns="cohorte", values="spearman_rho")
        f.write("== Signe du rho de Spearman par gène (cohérence inter-cohortes) ==\n")
        f.write(piv.to_string() + "\n")
        same = (np.sign(piv.values) == np.sign(piv.values[:, [0]])).all(axis=1)
        f.write("Gènes au signe constant sur les 4 cohortes : "
                f"{list(piv.index[same])}\n")
    print(df.to_string(index=False))
    print("Écrit : immune_direct_tests.csv / .txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
