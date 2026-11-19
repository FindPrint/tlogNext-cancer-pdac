#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bras 2 pan-cancer — tests directs (verdict principal) : l'axe KRAS -> CA125/CEA
se réplique-t-il dans le poumon (LUAD) et le côlon (COAD) ?
Conventions reprises EXACTEMENT de parp_direct_tests.py :
- Groupe KRAS fort = 12 dernières lignes (ordre KRAS croissant).
- top12_sd = (moyenne top12 - moyenne reste) / écart-type du gène (ddof=0).
- rho = Spearman entre l'indice de ligne (rang KRAS) et le gène ; p associée.
- Recouvrement Q3 : KRAS-forts au-dessus du quartile supérieur (attendu 3/12).
- Mêmes tests sur le nul (graine 42) en témoin.
En plus (mission) : test de Welch top12 contre reste (t + p).
Référence pancréas (mission) : MUC16 top-12 +0,64 / +0,67 / +0,48 sd ;
CEACAM5 +0,43 / +0,38 / +0,63 sd (3/4 cohortes pancréas).
Sorties : pancancer_direct_tests.csv + pancancer_direct_tests.txt
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, ttest_ind

GENES = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
         "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]

COHORTS = [("LUAD", "pdac_luad_fluxes.csv", "pdac_luad_fluxes_nul.csv"),
           ("COAD", "pdac_coad_fluxes.csv", "pdac_coad_fluxes_nul.csv")]

rows = []
txt = []
txt.append("=== Bras 2 pan-cancer — tests directs : KRAS -> CA125/CEA hors pancréas ===")
txt.append("Cohortes : TCGA-LUAD (515 tumeurs primaires) et TCGA-COAD (285), ARN brut log2(RSEM+1).")
txt.append("Groupe KRAS fort = 12 dernières lignes (KRAS brut croissant).")
txt.append("top12_sd = (moyenne top12 - moyenne reste) / écart-type du gène (ddof=0).")
txt.append("rho = Spearman gène vs rang KRAS (= Spearman gène vs KRAS brut).")
txt.append("Welch : test t de Welch top12 contre reste.")
txt.append("Q3 : attendu 3/12 KRAS-forts au-dessus du quartile supérieur sous indépendance.")
txt.append("Référence pancréas (3/4 cohortes) : MUC16 +0,64 / +0,67 / +0,48 sd ; "
           "CEACAM5 +0,43 / +0,38 / +0,63 sd.")
txt.append("")

for cohort, real_path, nul_path in COHORTS:
    for label, path in [("RÉEL", real_path), ("NUL (graine 42)", nul_path)]:
        f = pd.read_csv(path)
        n = len(f)
        step = f["step"].values
        assert (np.diff(step) >= 0).all(), f"{cohort} {label} : step non croissant"
        assert list(f.columns[1:]) == GENES, f"{cohort} {label} : colonnes inattendues"
        top12 = np.zeros(n, dtype=bool)
        top12[-12:] = True
        txt.append(f"--- {cohort} {label} — n={n} ---")
        for gene in GENES:
            v = f[gene].values.astype(float)
            q3 = np.quantile(v, 0.75)
            med = np.median(v)
            rho, p = spearmanr(np.arange(n), v)
            ov12 = int((top12 & (v > q3)).sum())
            top12_sd = float((v[top12].mean() - v[~top12].mean()) / v.std(ddof=0))
            tw, pw = ttest_ind(v[top12], v[~top12], equal_var=False)
            txt.append(
                f"{gene:8s}: médiane {med:+.2f} | Q3 {q3:+.2f} | "
                f"rho KRAS {rho:+.3f} p={p:.4g} | top12 {top12_sd:+.2f} sd | "
                f"Welch t={tw:+.2f} p={pw:.4g} | KRAS-forts >Q3 : {ov12}/12 (attendu 3)")
            rows.append(dict(cohorte=cohort, série=label, n=n, gene=gene,
                             median=med, q3=q3, rho_kras=rho, p_rho=p,
                             top12_sd=top12_sd, welch_t=float(tw),
                             welch_p=float(pw), overlap_top12_q3=ov12))
        txt.append("")

txt.append("--- Lecture ---")
for cohort, _, _ in COHORTS:
    real = [r for r in rows if r["cohorte"] == cohort and r["série"] == "RÉEL"]
    nul = [r for r in rows if r["cohorte"] == cohort and r["série"] == "NUL (graine 42)"]
    for key, name in [("rho_kras", "|rho|"), ("top12_sd", "|top12_sd|")]:
        br = max(real, key=lambda r: abs(r[key]))
        bn = max(nul, key=lambda r: abs(r[key]))
        txt.append(f"{cohort} — plus fort {name} RÉEL : {br['gene']} {br[key]:+.3f} "
                   f"(p={br['p_rho']:.4g}) ; plus fort {name} NUL : "
                   f"{bn['gene']} {bn[key]:+.3f} (p={bn['p_rho']:.4g}).")
    n_sig = sum(1 for r in real if r["p_rho"] < 0.05)
    txt.append(f"{cohort} — gènes avec p < 0,05 (Spearman, non corrigé, 12 tests) : "
               f"{n_sig}/12 en réel ; {sum(1 for r in nul if r['p_rho'] < 0.05)}/12 en nul.")
    txt.append(f"{cohort} — seuil Bonferroni 12 tests : p < 0,0042.")
    for g in ("MUC16", "CEACAM5"):
        r = next(x for x in real if x["gene"] == g)
        txt.append(f"{cohort} — {g} : top12 {r['top12_sd']:+.2f} sd, "
                   f"rho {r['rho_kras']:+.3f} (p={r['p_rho']:.4g}), "
                   f"Welch p={r['welch_p']:.4g}, >Q3 {r['overlap_top12_q3']}/12 "
                   f"[pancréas : {'+0,64/+0,67/+0,48' if g == 'MUC16' else '+0,43/+0,38/+0,63'} sd].")
    txt.append("")

pd.DataFrame(rows).to_csv("pancancer_direct_tests.csv", index=False)
with open("pancancer_direct_tests.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(txt) + "\n")
print("\n".join(txt))
print("Écrit : pancancer_direct_tests.csv et pancancer_direct_tests.txt")
