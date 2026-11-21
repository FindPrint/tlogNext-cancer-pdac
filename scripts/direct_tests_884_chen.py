#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests directs §8.84 — lot drogue Chen 2025.
Protocole gele : PROTOCOL_chen2025_drogue_884.md (§6).
Source : MOESM13 (Supplementary Data 10), SHA 0e009cd5...5340.
Sens des AUC : AUC basse = sensible.
D1 : Spearman AUC vs Gemcitabine, 62 drogues, FDR BH sur 62.
D2a : Olaparib, BRCA2-mutants n=6 (nommes article) vs n=40,
  Mann-Whitney bilateral, un seul test pre-enregistre.
D2b : CFTR VUS_D n=5 (nommes article) vs n=41, 63 drogues,
  Mann-Whitney, FDR BH sur 63.
D2c : volet CFTR, MT n=4 (DAC13, DAC24, DAC72, DAC84 — Fig. 6e
  Source Data, MOESM17) vs WT n=11, Wilcoxon bilateral sur les
  5 correcteurs, valeurs MOESM13 feuille CFTR (recoupement
  Fig. 6e vs MOESM13 : 75/75 paires, ecart max 4,96e-08).
D3 (KRAS) et D4 (MTAP) : IMPOSSIBLES — aucune table par-PDO
  recevable dans les supplements (voir §4 du protocole et
  PROVENANCE_884) ; consignes ici, non courus.
D5 : Spearman flux vs pas (reel vs nul graine 42) + d de Cohen
  marginal (attendu 0,0000).
Sortie : direct_tests_884_chen.json (+ .csv des tables D1/D2b).
Usage : python3 direct_tests_884_chen.py
"""
import json

import numpy as np
import openpyxl
import pandas as pd
from scipy import stats

PDAC = "/home/hatch/workspace/runs/pdac-v6"
SRC = f"{PDAC}/data/Chen2025_MOESM13_SupplData10.xlsx"
ANCHOR = "Gemcitabine"
BRCA2 = ["DAC_102", "DAC_58", "DAC_81", "DAC_85", "DAC_53", "DAC_4"]
CFTR5 = ["DAC_13", "DAC_73", "DAC_110", "DAC_32", "DAC_30"]
CFTR_MT = ["DAC13", "DAC24", "DAC72", "DAC84"]
CORRECTORS = ["Tezacaftor", "Lumacaftor", "FDL169", "Galicaftor",
              "Elexacaftor"]
ARTICLE_P = {"Tezacaftor": 0.006, "Lumacaftor": 0.005, "FDL169": 0.006,
             "Galicaftor": 0.016, "Elexacaftor": 0.002}


def bh(pvals):
    """Benjamini-Hochberg, retourne les q-values."""
    p = np.asarray(pvals, dtype=float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * n / np.arange(1, n + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.minimum(q, 1.0)
    return out


def main():
    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
    ws = wb["All Drugs AUC"]
    rows = list(ws.iter_rows(values_only=True))
    pdos = [c for c in rows[0][2:]]
    drugs = [r[0] for r in rows[1:]]
    arr = np.array([[r[2 + i] for i in range(46)] for r in rows[1:]],
                   dtype=float)
    df = pd.DataFrame(arr.T, index=pdos, columns=drugs)
    assert df.isna().sum().sum() == 0
    gem = df[ANCHOR].values
    out = {"n_pdo": 46, "n_drugs": 63}

    # ---- D1 ----
    d1 = []
    for d in drugs:
        if d == ANCHOR:
            continue
        rho, p = stats.spearmanr(df[d].values, gem)
        d1.append({"drug": d, "rho": float(rho), "p": float(p),
                   "n": 46})
    q = bh([r["p"] for r in d1])
    for r, qq in zip(d1, q):
        r["fdr"] = float(qq)
    d1s = sorted(d1, key=lambda r: -abs(r["rho"]))
    out["D1"] = {"method": "Spearman AUC vs AUC Gemcitabine, FDR BH sur 62",
                 "n_hits_fdr_lt_0.05": int(sum(r["fdr"] < 0.05 for r in d1)),
                 "min_fdr": float(min(r["fdr"] for r in d1)),
                 "top10_abs_rho": d1s[:10],
                 "table": d1}
    print(f"D1 : {out['D1']['n_hits_fdr_lt_0.05']} hit(s) FDR<0,05 sur 62 ; "
          f"FDR min = {out['D1']['min_fdr']:.4f} ; "
          f"top |rho| = {d1s[0]['drug']} {d1s[0]['rho']:+.4f} "
          f"(p={d1s[0]['p']:.4g}, FDR={d1s[0]['fdr']:.4f}).")

    # ---- D2a ----
    brca = df.loc[BRCA2, "Olaparib"].values
    rest = df.drop(index=BRCA2)["Olaparib"].values
    u, p = stats.mannwhitneyu(brca, rest, alternative="two-sided")
    out["D2a"] = {"method": "Mann-Whitney bilateral, Olaparib AUC",
                  "group_mut": BRCA2, "n_mut": 6,
                  "median_mut": float(np.median(brca)),
                  "median_rest": float(np.median(rest)),
                  "mean_mut": float(np.mean(brca)),
                  "mean_rest": float(np.mean(rest)),
                  "U": float(u), "p": float(p), "hit_p_lt_0.05": bool(p < 0.05),
                  "ranks_mut": sorted(
                      (float(df.loc[d, 'Olaparib'])
                       for d in BRCA2)),
                  "auc_olaparib_DAC76": float(df.loc["DAC_76", "Olaparib"]),
                  "auc_olaparib_DAC99": float(df.loc["DAC_99", "Olaparib"]),
                  "rank_olaparib_DAC76_asc": int(
                      (df["Olaparib"].values < df.loc["DAC_76", "Olaparib"]).sum() + 1),
                  "rank_olaparib_DAC99_asc": int(
                      (df["Olaparib"].values < df.loc["DAC_99", "Olaparib"]).sum() + 1)}
    print(f"D2a Olaparib BRCA2 (n=6) vs reste (n=40) : mediane "
          f"{np.median(brca):.4f} vs {np.median(rest):.4f}, "
          f"U={u:.1f}, p={p:.4g} -> "
          f"{'HIT' if p < 0.05 else 'NS'}.")

    # ---- D2b ----
    cf = df.loc[CFTR5]
    rest5 = df.drop(index=CFTR5)
    d2b = []
    for d in drugs:
        u, p = stats.mannwhitneyu(cf[d].values, rest5[d].values,
                                  alternative="two-sided")
        d2b.append({"drug": d, "median_cftr5": float(np.median(cf[d].values)),
                    "median_rest": float(np.median(rest5[d].values)),
                    "diff_median": float(np.median(cf[d].values)
                                         - np.median(rest5[d].values)),
                    "U": float(u), "p": float(p), "n": (5, 41)})
    q2 = bh([r["p"] for r in d2b])
    for r, qq in zip(d2b, q2):
        r["fdr"] = float(qq)
    d2bs = sorted(d2b, key=lambda r: r["p"])
    out["D2b"] = {"method": "Mann-Whitney bilateral, CFTR VUS_D n=5 vs n=41, FDR BH sur 63",
                  "n_hits_fdr_lt_0.05": int(sum(r["fdr"] < 0.05 for r in d2b)),
                  "min_fdr": float(min(r["fdr"] for r in d2b)),
                  "min_p": float(min(r["p"] for r in d2b)),
                  "top5_p": d2bs[:5],
                  "table": d2b}
    print(f"D2b : {out['D2b']['n_hits_fdr_lt_0.05']} hit(s) FDR<0,05 sur 63 ; "
          f"p min = {out['D2b']['min_p']:.4g} ({d2bs[0]['drug']}, "
          f"FDR={d2bs[0]['fdr']:.4f}).")

    # ---- D2c ----
    ws2 = wb["CFTR Drugs AUC"]
    r2 = list(ws2.iter_rows(values_only=True))
    hdr2 = r2[0]
    cf15 = [c for c in hdr2[2:]]
    m13 = {r[0]: {hdr2[2 + i]: r[2 + i] for i in range(15)}
           for r in r2[1:]}
    mt = [c for c in cf15 if c.replace("_", "") in CFTR_MT]
    wt = [c for c in cf15 if c.replace("_", "") not in CFTR_MT]
    assert len(mt) == 4 and len(wt) == 11, (mt, wt)
    d2c = []
    for d in CORRECTORS:
        a = np.array([m13[d][c] for c in mt])
        b = np.array([m13[d][c] for c in wt])
        u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
        d2c.append({"drug": d, "n_mt": 4, "n_wt": 11,
                    "median_mt": float(np.median(a)),
                    "median_wt": float(np.median(b)),
                    "U": float(u), "p": float(p),
                    "p_article": ARTICLE_P[d]})
    out["D2c"] = {"method": "Mann-Whitney bilateral (Wilcoxon dans l'article), correcteurs CFTR, MT n=4 vs WT n=11, valeurs MOESM13 feuille CFTR",
                  "mt": mt, "wt": wt, "table": d2c}
    for r in d2c:
        print(f"D2c {r['drug']:12s} MT med {r['median_mt']:.4f} vs WT med "
              f"{r['median_wt']:.4f}, p={r['p']:.4g} (article {r['p_article']:.3f}).")

    # ---- D3 / D4 : impossibles ----
    out["D3_KRAS"] = {"status": "IMPOSSIBLE",
                      "reason": "Aucune table par-PDO du statut KRAS somatique "
                                "dans les supplements (MOESM4-MOESM15) ni dans la "
                                "Source Data (MOESM17) : 0 identifiant DAC dans "
                                "les Data 1-12 ; l'article nomme un seul organoide "
                                "KRAS p.G12C sans identifiant DAC."}
    out["D4_MTAP"] = {"status": "IMPOSSIBLE",
                      "reason": "Aucune table par-PDO du statut MTAP (deletion / "
                                "nombre de copies 9p21) dans les supplements ni "
                                "dans la Source Data ; MTAP n'apparait que comme "
                                "entree de liste de genes (Data 4) et une variante "
                                "germinale VUS_D p.P41L chez un patient de la "
                                "cohorte decouverte (Data 3, EN233) — pas un "
                                "statut de deletion par PDO. De plus, aucun "
                                "inhibiteur PRMT5 / MAT2A / vopimetostat dans "
                                "les 63 drogues."}

    # ---- D5 : appui pipeline ----
    real = pd.read_csv(f"{PDAC}/pdac_884_chen_fluxes.csv")
    nul = pd.read_csv(f"{PDAC}/pdac_884_chen_fluxes_nul.csv")
    step = real["step"].values.astype(float)
    fluxes = [c for c in real.columns if c != "step"]
    d5 = []
    for f in fluxes:
        rho_r, _ = stats.spearmanr(real[f].values, step)
        rho_n, _ = stats.spearmanr(nul[f].values, step)
        mr, sr = float(np.mean(real[f].values)), float(np.std(real[f].values, ddof=1))
        mn, sn = float(np.mean(nul[f].values)), float(np.std(nul[f].values, ddof=1))
        sp = np.sqrt(((45 * sr ** 2) + (45 * sn ** 2)) / 90)
        d = (mr - mn) / sp if sp > 0 else 0.0
        d5.append({"flux": f, "rho_reel": float(rho_r),
                   "rho_nul": float(rho_n), "delta_rho": float(rho_r - rho_n),
                   "d_cohen_marginal": float(d)})
    drho = np.array([r["delta_rho"] for r in d5])
    dco = np.array([r["d_cohen_marginal"] for r in d5])
    out["D5"] = {"method": "Spearman flux vs pas, reel vs nul graine 42",
                 "n_flux": 62,
                 "delta_rho_median": float(np.median(drho)),
                 "delta_rho_mean_abs": float(np.mean(np.abs(drho))),
                 "n_delta_rho_positifs": int((drho > 0).sum()),
                 "d_cohen_marginal_max_abs": float(np.max(np.abs(dco))),
                 "table": d5}
    print(f"D5 : Delta-rho median {np.median(drho):+.4f}, "
          f"{int((drho > 0).sum())}/62 positifs ; "
          f"|d| marginal max = {np.max(np.abs(dco)):.4f} (attendu 0,0000).")

    with open(f"{PDAC}/direct_tests_884_chen.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    pd.DataFrame(d1).to_csv(f"{PDAC}/direct_tests_884_chen_D1.csv",
                            index=False)
    pd.DataFrame(d2b).to_csv(f"{PDAC}/direct_tests_884_chen_D2b.csv",
                             index=False)
    print("Ecrit : direct_tests_884_chen.json (+ D1/D2b .csv).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
