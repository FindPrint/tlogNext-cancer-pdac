#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-test ATR/CHEK1 — point 5 : inhibiteurs ATR / CHEK1 dans les 3
criblages EXISTANTS (aucun nouveau téléchargement).
- PRISM primaire : data/prism_kras_screen_named.csv (6 790 composés)
- GDSC2 : data/gdsc_kras_screen.csv (269 composés)
- PRISM secondaire : data/prism_secondary_kras_screen.csv (1 427 composés)
Recherche par nom de composé, MOA et cible : ceralasertib/AZD6738,
berzosertib/VX-970, elimusertib/BAY1895344 (ATR) ; prexasertib/LY2606368,
rabusertib/LY2603618, SRA737 (CHEK1/CHK1).
"""
import re

import pandas as pd

OUT = "/home/hatch/workspace/runs/pdac-v6"
KEYS = {
    "ATR": ["ceralasertib", "azd6738", "berzosertib", "vx970",
            "elimusertib", "bay1895344"],
    "CHEK1": ["prexasertib", "ly2606368", "rabusertib", "ly2603618",
              "sra737"],
}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def name_hit(series, keys):
    return series.fillna("").str.lower().apply(
        lambda s: any(k in norm(s) for k in keys))


def moa_hit(series):
    """Mot entier ATR/CHK1/CHEK1 dans la MOA — 'MATRIX' ne doit PAS
    matcher ('ATR' est une sous-chaîne de MATRIX)."""
    return series.fillna("").str.contains(r"\bATR\b|\bCHK1\b|\bCHEK1\b",
                                          case=False, na=False, regex=True)


def target_hit(series):
    return series.fillna("").str.contains(r"\bATR\b|\bCHK1\b|\bCHEK1\b",
                                          case=False, na=False, regex=True)


def main():
    rows = []
    txt = ["=== Inhibiteurs ATR / CHEK1 dans les criblages existants ===",
           "Aucun nouveau téléchargement. rho = Spearman viabilité/IC50 "
           "vs Chronos KRAS (positif = plus sensible quand KRAS-dépendant).",
           ""]

    # --- PRISM primaire ---
    p = pd.read_csv(f"{OUT}/data/prism_kras_screen_named.csv")
    txt.append(f"--- PRISM primaire ({len(p)} composés) ---")
    for fam, keys in KEYS.items():
        hit = p[name_hit(p["Drug.Name"], keys) | moa_hit(p["MOA"])]
        txt.append(f"{fam} : {len(hit)} hit(s)")
        for _, r in hit.iterrows():
            txt.append(f"  {r['Drug.Name']} | MOA={r['MOA']} | n={r['n']} "
                       f"rho={r['spearman_kras']:+.3f} p={r['p']:.4g} "
                       f"FDR={r['fdr_bh']:.3f}")
            rows.append(dict(criblage="PRISM primaire", famille=fam,
                             composé=r["Drug.Name"], moa=r["MOA"], n=int(r["n"]),
                             rho=float(r["spearman_kras"]), p=float(r["p"]),
                             fdr=float(r["fdr_bh"])))
    txt.append("")

    # --- GDSC2 ---
    g = pd.read_csv(f"{OUT}/data/gdsc_kras_screen.csv")
    txt.append(f"--- GDSC2 ({len(g)} composés) ---")
    for fam, keys in KEYS.items():
        hit = g[name_hit(g["compound"], keys) | target_hit(g["target"])]
        txt.append(f"{fam} : {len(hit)} hit(s)")
        for _, r in hit.iterrows():
            txt.append(f"  {r['compound']} | target={r['target']} | "
                       f"pathway={r['pathway']} | n={r['n']} "
                       f"rho_LN_IC50={r['rho_ln_ic50']:+.3f} p={r['p_ln_ic50']:.4g} "
                       f"FDR={r['fdr_ln_ic50']:.3f} | rho_AUC={r['rho_auc']:+.3f} "
                       f"FDR={r['fdr_auc']:.3f}")
            rows.append(dict(criblage="GDSC2", famille=fam,
                             composé=r["compound"], moa=r["pathway"],
                             n=int(r["n"]), rho=float(r["rho_ln_ic50"]),
                             p=float(r["p_ln_ic50"]),
                             fdr=float(r["fdr_ln_ic50"])))
    txt.append("")

    # --- PRISM secondaire ---
    s = pd.read_csv(f"{OUT}/data/prism_secondary_kras_screen.csv")
    txt.append(f"--- PRISM secondaire ({len(s)} composés) ---")
    for fam, keys in KEYS.items():
        hit = s[name_hit(s["compound"], keys) | target_hit(s["target"])
                | moa_hit(s["moa"])]
        txt.append(f"{fam} : {len(hit)} hit(s)")
        for _, r in hit.iterrows():
            txt.append(f"  {r['compound']} | moa={r['moa']} | "
                       f"target={r['target']} | rho_AUC={r['rho_auc']:+.3f} "
                       f"p={r['p_auc']:.4g} FDR={r['fdr_auc']:.3f} | "
                       f"rho_IC50={r['rho_ic50'] if pd.notna(r['rho_ic50']) else 'n/a'} "
                       f"FDR_IC50={r['fdr_ic50'] if pd.notna(r['fdr_ic50']) else 'n/a'}")
            rows.append(dict(criblage="PRISM secondaire", famille=fam,
                             composé=r["compound"], moa=r["moa"], n=int(r["n_auc"]),
                             rho=float(r["rho_auc"]), p=float(r["p_auc"]),
                             fdr=float(r["fdr_auc"])))
    txt.append("")
    txt.append("--- Lecture ---")
    txt.append("Conventions de signe : PRISM rho > 0 = lignées KRAS-dépendantes "
               "PLUS sensibles (viabilité basse) ; GDSC rho_LN_IC50 < 0 = PLUS "
               "sensibles (IC50 basse).")
    if rows:
        # Plus fort signal dans le sens « sensible » par criblage
        prism = [r for r in rows if r["criblage"] != "GDSC2"]
        gdsc = [r for r in rows if r["criblage"] == "GDSC2"]
        if prism:
            best_p = max(prism, key=lambda r: r["rho"])
            txt.append(f"PRISM — plus fort rho (sens sensible) : "
                       f"{best_p['composé']} ({best_p['criblage']}, "
                       f"{best_p['famille']}) rho {best_p['rho']:+.3f} "
                       f"p={best_p['p']:.4g} FDR={best_p['fdr']:.3f}.")
        if gdsc:
            best_g = min(gdsc, key=lambda r: r["rho"])
            txt.append(f"GDSC2 — plus fort rho (sens sensible, négatif) : "
                       f"{best_g['composé']} rho {best_g['rho']:+.3f} "
                       f"p={best_g['p']:.4g} FDR={best_g['fdr']:.3f}.")
        n_sig = sum(1 for r in rows if r["fdr"] < 0.05)
        txt.append(f"Composés FDR < 0,05 : {n_sig}/{len(rows)}.")
        txt.append("Absents des 3 criblages : berzosertib (VX-970), SRA737.")
    else:
        txt.append("Aucun inhibiteur ATR/CHEK1 trouvé dans les 3 criblages : "
                   "la question médicament ne peut pas être tranchée sur ces "
                   "données (absence de données, pas une preuve d'absence d'effet).")

    out_csv = f"{OUT}/atr_chek1_drugs.csv"
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    out_txt = f"{OUT}/atr_chek1_drugs.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(txt) + "\n")
    print("\n".join(txt))
    print(f"Écrit : {out_csv} et {out_txt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
