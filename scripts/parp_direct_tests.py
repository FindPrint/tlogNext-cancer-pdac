#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bras 2 — tests directs (verdict principal) : paysage réparation / PARP
le long de l'axe KRAS, TCGA-PAAD (178 tumeurs, ARN brut log2(RSEM+1)).
Conventions reprises EXACTEMENT de check_expression_muc16_cldn18.py :
- Groupe KRAS fort = 12 dernières lignes (ordre KRAS croissant).
- top12_sd = (moyenne_top12 - moyenne_reste) / écart-type (ddof=0) du gène.
- rho = Spearman entre l'indice de ligne (rang KRAS) et le gène ; p associée.
  (Le rang KRAS = le rang de l'expression KRAS brute, donc rho est aussi
  le Spearman gène vs KRAS brut.)
- Recouvrement Q3 : nombre des 12 KRAS-forts au-dessus du quartile
  supérieur du gène (attendu 3 sous indépendance).
- Comparaison de référence : mêmes tests sur le nul (graine 42) — un effet
  réel doit dépasser ce que le nul produit par construction.
Sorties : parp_direct_tests.csv + parp_direct_tests.txt
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

GENES = ["PARP1", "PARP2", "BRCA1", "BRCA2", "ATM", "ATR", "CHEK1", "CHEK2",
         "RAD51", "XRCC1", "POLQ", "FANCD2"]

rows = []
txt = []
txt.append("=== Bras 2 — tests directs : réparation / PARP le long de l'axe KRAS ===")
txt.append("Cohorte : TCGA-PAAD, 178 tumeurs primaires, ARN brut log2(RSEM+1).")
txt.append("Groupe KRAS fort = 12 dernières lignes (KRAS brut croissant).")
txt.append("top12_sd = (moyenne top12 - moyenne reste) / écart-type du gène (ddof=0).")
txt.append("rho = Spearman gène vs rang KRAS (= Spearman gène vs KRAS brut).")
txt.append("Q3 : attendu 3/12 KRAS-forts au-dessus du quartile supérieur sous indépendance.")
txt.append("")

for label, path in [("RÉEL", "pdac_tcga_fluxes_parp.csv"),
                    ("NUL (graine 42)", "pdac_tcga_fluxes_parp_nul.csv")]:
    f = pd.read_csv(path)
    n = len(f)
    step = f["step"].values
    assert (np.diff(step) >= 0).all(), f"{label} : step non croissant"
    assert list(f.columns[1:]) == GENES, f"{label} : colonnes inattendues"
    top12 = np.zeros(n, dtype=bool)
    top12[-12:] = True
    txt.append(f"--- {label} — n={n} ---")
    for gene in GENES:
        v = f[gene].values.astype(float)
        q3 = np.quantile(v, 0.75)
        med, sd = np.median(v), v.std(ddof=1)
        rho, p = spearmanr(np.arange(n), v)
        ov12 = int((top12 & (v > q3)).sum())
        top12_sd = float((v[top12].mean() - v[~top12].mean()) / v.std(ddof=0))
        txt.append(
            f"{gene:6s}: médiane {med:+.2f} | Q3 {q3:+.2f} | "
            f"rho KRAS {rho:+.3f} p={p:.4f} | top12 {top12_sd:+.2f} sd | "
            f"KRAS-forts >Q3 : {ov12}/12 (attendu 3)")
        rows.append(dict(série=label, n=n, gene=gene, median=med, q3=q3,
                         rho_kras=rho, p_rho=p, top12_sd=top12_sd,
                         overlap_top12_q3=ov12))
    txt.append("")

# Synthèse : plus forts effets réels, et ce que le nul donne au même rang
txt.append("--- Lecture ---")
real = [r for r in rows if r["série"] == "RÉEL"]
nul = [r for r in rows if r["série"] == "NUL (graine 42)"]
for key, name in [("rho_kras", "|rho|"), ("top12_sd", "|top12_sd|")]:
    best_real = max(real, key=lambda r: abs(r[key]))
    best_nul = max(nul, key=lambda r: abs(r[key]))
    txt.append(f"Plus fort {name} RÉEL : {best_real['gene']} {best_real[key]:+.3f} "
               f"(p={best_real['p_rho']:.4f}) ; plus fort {name} NUL : "
               f"{best_nul['gene']} {best_nul[key]:+.3f} (p={best_nul['p_rho']:.4f}).")
n_sig = sum(1 for r in real if r["p_rho"] < 0.05)
txt.append(f"Gènes avec p < 0,05 (Spearman, non corrigé, 12 tests) : {n_sig}/12 "
           f"en réel ; {sum(1 for r in nul if r['p_rho'] < 0.05)}/12 en nul.")
txt.append("Seuil Bonferroni 12 tests : p < 0,0042.")

out_csv = "parp_direct_tests.csv"
pd.DataFrame(rows).to_csv(out_csv, index=False)
out_txt = "parp_direct_tests.txt"
with open(out_txt, "w", encoding="utf-8") as f:
    f.write("\n".join(txt) + "\n")
print("\n".join(txt))
print(f"Écrit : {out_csv} et {out_txt}")
