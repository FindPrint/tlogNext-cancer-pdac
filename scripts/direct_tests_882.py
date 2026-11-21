#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests directs §8.82 (cerveau, TCGA-GBM).
Protocole gelé : PROTOCOL_cerveau_privilege_882.md (21 nov. 2026), §§4, 5, 9.
- (1) Spearman de chaque gène de privilège avec le pas de prolifération
  (test informatif, correction §8.70) ; médiane des 7 rho ; top-quartile
  de prolifération vs reste en sd (Welch p descriptive) ; Spearman du
  score de privilège lui-même.
- (2) Froid : Spearman de chacun des 12 gènes immunitaires (§8.23) avec
  le pas de prolifération ; Spearman du score froid ; CD274 seul ;
  top-quartile vs reste pour PDCD1 et CD8A.
- (9) En appui pipeline : Spearman de chaque flux v4 avec le pas (ordre
  prolifération, puis ordre privilège), réel vs nul ; d de Cohen marginal
  réel vs nul (attendu vacueux ≈ 0,0000 : il valide la construction du
  nul, il ne mesure pas l'ordre et ne décide rien).
Sortie : direct_tests_882.json + direct_tests_882.txt (toutes les tables,
sans sélection).
"""
import json
import math

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, ttest_ind

BASE = "/home/hatch/workspace/runs/pdac-v6"
PRIV = ["FASLG", "TGFB1", "TGFB2", "IDO1", "HLA-G", "CD47", "CD274"]
V4 = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
      "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]
IMM = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
       "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]


def spearman(x, y):
    r = spearmanr(np.asarray(x, dtype=float), np.asarray(y, dtype=float))
    return float(r.statistic), float(r.pvalue)


def topq_diff(values, order_values):
    """Différence (quartile supérieur de order_values moins le reste), en sd
    de values ; Welch p. Quartile = top 25 % (38/153)."""
    values = np.asarray(values, dtype=float)
    order_values = np.asarray(order_values, dtype=float)
    q = np.quantile(order_values, 0.75)
    hi = order_values >= q
    d = (values[hi].mean() - values[~hi].mean()) / values.std(ddof=0)
    p = float(ttest_ind(values[hi], values[~hi], equal_var=False).pvalue)
    return float(d), p, int(hi.sum())


def main():
    d = pd.read_csv(f"{BASE}/gbm_882_direct_table.csv")
    n = len(d)
    step = d["step"].values.astype(float)
    assert n == 153, n
    assert bool(np.all(np.diff(d["score_prolif"].values) >= -1e-12)), \
        "score de prolifération non trié"
    out = {"n": n}
    lines = []
    lines.append("TESTS DIRECTS §8.82 — TCGA-GBM, n=153 primaires")
    lines.append("Ordre primaire : score de prolifération croissant.")
    lines.append("")

    # --- (1) Privilège vs prolifération ---
    lines.append("=== (1) Gènes de privilège vs pas de prolifération ===")
    rows = []
    for g in PRIV:
        rho, p = spearman(d[g].values, step)
        dd, pw, nhi = topq_diff(d[g].values, d["score_prolif"].values)
        rows.append({"gène": g, "rho": round(rho, 4), "p": round(p, 4),
                     "d_topq_sd": round(dd, 4), "p_welch_topq": round(pw, 4),
                     "n_topq": nhi})
        lines.append(f"  {g:6s} rho={rho:+.3f} p={p:.4f} "
                     f"d_topq={dd:+.3f} sd (Welch p={pw:.4f}, n_topq={nhi})")
    rhos = np.array([r["rho"] for r in rows])
    out["privilege_vs_prolif"] = rows
    out["privilege_mediane_rho"] = round(float(np.median(rhos)), 4)
    out["privilege_n_rho_pos"] = int((rhos > 0).sum())
    out["privilege_n_p_lt_05"] = int(sum(1 for r in rows if r["p"] < 0.05))
    lines.append(f"  MÉDIANE rho = {np.median(rhos):+.3f} ; "
                 f"rho>0 : {int((rhos > 0).sum())}/7 ; "
                 f"p<0,05 : {sum(1 for r in rows if r['p'] < 0.05)}/7")
    rho_s, p_s = spearman(d["score_privilege"].values, step)
    out["score_privilege_vs_prolif"] = {"rho": round(rho_s, 4),
                                        "p": round(p_s, 4)}
    lines.append(f"  Score privilège vs pas : rho={rho_s:+.3f} p={p_s:.4f}")
    lines.append("")

    # --- (2) Froid ---
    lines.append("=== (2) Gènes immunitaires vs pas de prolifération "
                 "(référence §8.23, axe KRAS pancréas) ===")
    rows_i = []
    for g in IMM:
        rho, p = spearman(d[g].values, step)
        dd, pw, nhi = topq_diff(d[g].values, d["score_prolif"].values)
        rows_i.append({"gène": g, "rho": round(rho, 4), "p": round(p, 4),
                       "d_topq_sd": round(dd, 4),
                       "p_welch_topq": round(pw, 4)})
        lines.append(f"  {g:6s} rho={rho:+.3f} p={p:.4f} "
                     f"d_topq={dd:+.3f} sd (Welch p={pw:.4f})")
    out["imm_vs_prolif"] = rows_i
    cold4 = ["CD8A", "CD4", "FOXP3", "PDCD1"]
    cold_rhos = np.array([r["rho"] for r in rows_i
                          if r["gène"] in cold4])
    out["froid_mediane_rho"] = round(float(np.median(cold_rhos)), 4)
    out["froid_n_rho_neg"] = int((cold_rhos < 0).sum())
    rho_c, p_c = spearman(d["score_froid"].values, step)
    out["score_froid_vs_prolif"] = {"rho": round(rho_c, 4),
                                    "p": round(p_c, 4)}
    lines.append(f"  Score froid (CD8A/CD4/FOXP3/PDCD1) vs pas : "
                 f"rho={rho_c:+.3f} p={p_c:.4f}")
    lines.append(f"  MÉDIANE rho des 4 gènes du score froid = "
                 f"{np.median(cold_rhos):+.3f} ; rho<0 : "
                 f"{int((cold_rhos < 0).sum())}/4")
    lines.append("  Référence §8.23 (TCGA pancréas, axe KRAS) : CD8A −0,19 ; "
                 "CD4 −0,15 ; FOXP3 −0,10 ; PDCD1 −0,25 ; médiane ≈ −0,17 ; "
                 "CD274 +0,26 en TCGA seulement.")
    lines.append("")

    # --- (9) Appui pipeline : Spearman flux v4 vs pas, réel vs nul ---
    lines.append("=== (9) Appui pipeline : Spearman des 12 flux v4 vs pas, "
                 "réel vs nul ===")
    for tag, order_col in [("prolif", "step"), ("privilege", None)]:
        reel = pd.read_csv(f"{BASE}/pdac_882_gbm_{tag}_fluxes.csv")
        nul = pd.read_csv(f"{BASE}/pdac_882_gbm_{tag}_fluxes_nul.csv")
        assert list(reel.columns) == ["step"] + V4
        assert list(nul.columns) == ["step"] + V4
        st = reel["step"].values.astype(float)
        rhos_r, rhos_n, drhos, cohens = [], [], [], []
        lines.append(f"  -- ordre {tag} --")
        for g in V4:
            rr, _ = spearman(reel[g].values, st)
            rn, _ = spearman(nul[g].values, st)
            rhos_r.append(rr)
            rhos_n.append(rn)
            drhos.append(rr - rn)
            # d de Cohen marginal réel vs nul (mêmes valeurs permutées).
            a = reel[g].values.astype(float)
            b = nul[g].values.astype(float)
            pooled = math.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2.0)
            cohens.append((a.mean() - b.mean()) / pooled if pooled > 0
                          else 0.0)
            lines.append(f"    {g:8s} rho_réel={rr:+.3f} rho_nul={rn:+.3f} "
                         f"Δρ={rr - rn:+.3f} d_Cohen={cohens[-1]:+.4f}")
        out[f"pipeline_appui_{tag}"] = {
            "rho_reel_moyen_abs": round(float(np.mean(np.abs(rhos_r))), 4),
            "rho_nul_moyen_abs": round(float(np.mean(np.abs(rhos_n))), 4),
            "delta_rho_mediane": round(float(np.median(drhos)), 4),
            "delta_rho_positifs": int(sum(1 for x in drhos if x > 0)),
            "cohen_marginal_max_abs": round(float(np.max(np.abs(cohens))), 6),
            "cohen_marginal": {g: round(float(c), 6)
                               for g, c in zip(V4, cohens)},
        }
        lines.append(f"    |ρ| moyen réel={np.mean(np.abs(rhos_r)):.3f} "
                     f"nul={np.mean(np.abs(rhos_n)):.3f} ; "
                     f"Δρ médian={np.median(drhos):+.3f} ; "
                     f"Δρ positifs={sum(1 for x in drhos if x > 0)}/12 ; "
                     f"|d Cohen| max={np.max(np.abs(cohens)):.6f} "
                     f"(attendu ≈ 0,0000, nul = permutation)")
    lines.append("")

    with open(f"{BASE}/direct_tests_882.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    with open(f"{BASE}/direct_tests_882.txt", "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"Écrit : {BASE}/direct_tests_882.json, direct_tests_882.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
