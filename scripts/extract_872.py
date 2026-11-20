#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extraction §8.72 — consolidation GSE79668 par 10 nuls frais.
Réutilise extract() de extract_858.py (original intact), comme
extract_870.py. Lecture SEULE des master_results.json (10 neufs +
4 anciens relus : réel + nuls graines 42, 8701, 8702), aucun run
lancé, aucun CSV modifié. Calcule la distribution des 13 nuls
(médiane, p95 numpy.percentile interpolation linéaire, min, max,
étendue, IQR, écart-type), d_médian = réel − médiane(13 nuls),
le rang du réel, la fraction des écarts > 0,07 — depuis les valeurs
extraites, jamais recopiées à la main. Vérifie que le maxsep réel
relu et les 3 nuls anciens relus égalent leurs valeurs §8.70 à
0,0 exact.
Usage : python3 extract_872.py
Sorties : extract_872.json, extract_872.csv.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_858 import extract  # noqa: E402

PDAC = os.path.dirname(os.path.abspath(__file__))
TAG = "geo79668"
REAL_MAXSEP = 0.41044843843771645
OLD_NULLS = {"nul": 0.3537953187066359,
             "nul_s8701": 0.3214731637696184,
             "nul_s8702": 0.2566001863019332}
FLOOR = 0.07
SEEDS = [8721, 8722, 8723, 8724, 8725, 8726, 8727, 8728, 8729, 8730]


def main():
    rows = []
    missing = []
    pairs = [("reel", "results_fast_v62_870_geo79668"),
             ("nul", "results_fast_v62_870_geo79668_nul"),
             ("nul_s8701", "results_fast_v62_870_geo79668_nul_s8701"),
             ("nul_s8702", "results_fast_v62_870_geo79668_nul_s8702")]
    for seed in SEEDS:
        pairs.append((f"nul_s{seed}",
                      f"results_fast_v62_872_geo79668_nul_s{seed}"))
    for tag, d in pairs:
        if not os.path.exists(os.path.join(PDAC, d, "master_results.json")):
            missing.append(d)
            continue
        e = extract(d)
        e["paire"] = TAG
        e["tag"] = tag
        rows.append(e)
    with open(os.path.join(PDAC, "extract_872.json"), "w") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    keys = ["paire", "tag", "n", "control", "target", "cascade_pct",
            "cascade_pas", "mc_score", "mc_thr", "maxsep", "stability",
            "ssep", "delta", "l7a_dir", "l7a_conf", "l7b", "fals",
            "fals_status", "regime", "bruit_verdict", "bruit_score_moyen",
            "f1_ratio", "f2_ratio"]
    tab = pd.DataFrame([{k: r.get(k) for k in keys} for r in rows])
    tab.to_csv(os.path.join(PDAC, "extract_872.csv"), index=False)
    print(f"Extraits : {len(rows)} runs ; manquants : {len(missing)} {missing}")
    for r in rows:
        mc = r["mc_score"]
        print(f"{r['paire']} {r['tag']:9s} n={r['n']} "
              f"MC={mc if mc is None else round(mc, 4)} "
              f"maxsep={r['maxsep'] if r['maxsep'] is None else round(r['maxsep'], 4)} "
              f"S_sep={r['ssep'] if r['ssep'] is None else round(r['ssep'], 4)} "
              f"Delta={r['delta'] if r['delta'] is None else round(r['delta'], 3)} "
              f"L7a={r['l7a_dir']} {r['l7a_conf']}")
    # ---- Relecture des valeurs §8.70 : 0,0 exact exigé ----
    reel = next((r for r in rows if r["tag"] == "reel"), None)
    checks = []
    if reel is not None:
        checks.append(("reel_maxsep", reel["maxsep"], REAL_MAXSEP))
    for tag, val in OLD_NULLS.items():
        row = next((r for r in rows if r["tag"] == tag), None)
        if row is not None:
            checks.append((f"{tag}_maxsep", row["maxsep"], val))
    for name, got, want in checks:
        ecart = None if got is None else abs(got - want)
        print(f"RELECTURE {name} : {got} vs §8.70 {want} — écart {ecart}")
        if ecart != 0.0:
            print("ÉCART DE RELECTURE — diagnostic, pas un bruit.",
                  file=sys.stderr)
            return 1
    if reel is None or reel["maxsep"] is None:
        print("Réel absent — arrêt.", file=sys.stderr)
        return 1
    m_r = reel["maxsep"]
    # ---- Distribution des nuls ----
    fresh = [r["maxsep"] for r in rows
             if r["tag"] in {f"nul_s{s}" for s in SEEDS}
             and r["maxsep"] is not None]
    old = [r["maxsep"] for r in rows
           if r["tag"] in OLD_NULLS and r["maxsep"] is not None]
    if len(fresh) != 10 or len(old) != 3:
        print(f"Nuls incomplets : frais {len(fresh)}/10, anciens "
              f"{len(old)}/3 — arrêt.", file=sys.stderr)
        return 1
    all_nulls = sorted(old + fresh)
    fresh_sorted = sorted(fresh)

    def stats(vals):
        a = np.array(vals, dtype=float)
        return {"n": int(len(a)),
                "median": float(np.median(a)),
                "p95": float(np.percentile(a, 95)),
                "min": float(np.min(a)),
                "max": float(np.max(a)),
                "etendue": float(np.max(a) - np.min(a)),
                "q1": float(np.percentile(a, 25)),
                "q3": float(np.percentile(a, 75)),
                "iqr": float(np.percentile(a, 75) - np.percentile(a, 25)),
                "sd": float(np.std(a, ddof=1)),
                "valeurs_triees": [float(v) for v in sorted(a)]}

    s_tot = stats(all_nulls)
    s_fresh = stats(fresh_sorted)
    d_median = m_r - s_tot["median"]
    d_fresh_median = m_r - s_fresh["median"]
    d_p95 = m_r - s_tot["p95"]
    gaps = [m_r - v for v in all_nulls]
    n_beaten = sum(1 for v in all_nulls if m_r > v)
    rank = n_beaten + 1  # rang du réel parmi les 14 valeurs (1 = plus bas)
    frac_pass = sum(1 for g in gaps if g > FLOOR) / len(gaps)
    if d_median < 0.05:
        verdict = "CONSOLIDÉ"
    elif d_median > 0.09:
        verdict = "RENVERSE"
    else:
        verdict = "INCONCLUSIF"
    dist = {"m_reel": m_r, "floor": FLOOR,
            "distribution_primaire_13_nuls": s_tot,
            "distribution_secondaire_10_frais": s_fresh,
            "ecart_medianes_frais_moins_totale":
                float(s_fresh["median"] - s_tot["median"]),
            "d_median": float(d_median),
            "d_median_frais_seuls": float(d_fresh_median),
            "d_contre_p95": float(d_p95),
            "gaps_tries": sorted(gaps),
            "rang_reel_sur_14": int(rank),
            "nuls_battus_par_reel": int(n_beaten),
            "fraction_ecarts_sup_plancher": float(frac_pass),
            "verdict": verdict}
    with open(os.path.join(PDAC, "dist_872.json"), "w") as f:
        json.dump(dist, f, indent=2, ensure_ascii=False)
    print(f"m_R = {m_r:.4f} ; médiane 13 nuls = {s_tot['median']:.4f} ; "
          f"p95 = {s_tot['p95']:.4f} ; étendue = {s_tot['etendue']:.4f} ; "
          f"IQR = {s_tot['iqr']:.4f}")
    print(f"médiane 10 frais = {s_fresh['median']:.4f} "
          f"(écart vs totale : {s_fresh['median'] - s_tot['median']:+.4f})")
    print(f"d_médian = {d_median:+.4f} (plancher 0,07) ; "
          f"d contre p95 = {d_p95:+.4f} ; rang réel {rank}/14 ; "
          f"nuls battus {n_beaten}/13 ; écarts > 0,07 : "
          f"{sum(1 for g in gaps if g > FLOOR)}/13")
    print(f"VERDICT §8.72 (règle gelée §4.3) : {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
