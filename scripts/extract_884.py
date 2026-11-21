#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extraction §8.84 — lot drogue Chen 2025, 46 PDO x 62 flux.
Réutilise extract() de extract_858.py (original intact), comme
extract_879_c3.py. Lecture SEULE des master_results.json du chantier
(réel + nul, + nuls frais éventuels), aucun run lancé, aucun CSV
modifié.
Usage : python3 extract_884.py
Sorties : extract_884.json, extract_884.csv.
"""
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_858 import extract  # noqa: E402

PDAC = os.path.dirname(os.path.abspath(__file__))
TAG = "chen"


def main():
    rows = []
    missing = []
    for tag in ("reel", "nul", "nul_s8841", "nul_s8842"):
        d = f"results_fast_v62_884_{TAG}" + ("" if tag == "reel"
                                             else "_" + tag)
        if not os.path.exists(os.path.join(PDAC, d,
                                           "master_results.json")):
            missing.append(d)
            continue
        e = extract(d)
        e["paire"] = TAG
        e["tag"] = tag
        rows.append(e)
    with open(os.path.join(PDAC, "extract_884.json"), "w") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    keys = ["paire", "tag", "n", "control", "target", "cascade_pct",
            "cascade_pas", "mc_score", "mc_thr", "maxsep", "stability",
            "ssep", "delta", "l7a_dir", "l7a_conf", "l7b", "fals",
            "fals_status", "regime", "bruit_verdict", "bruit_score_moyen",
            "f1_ratio", "f2_ratio"]
    tab = pd.DataFrame([{k: r.get(k) for k in keys} for r in rows])
    tab.to_csv(os.path.join(PDAC, "extract_884.csv"), index=False)
    print(f"Extraits : {len(rows)} runs ; manquants : {len(missing)} {missing}")
    for r in rows:
        mc = r["mc_score"]
        print(f"{r['paire']} {r['tag']:4s} n={r['n']} "
              f"casc={['—' if c is None else round(c, 1) for c in r['cascade_pct']]} "
              f"MC={mc if mc is None else round(mc, 4)} "
              f"maxsep={r['maxsep'] if r['maxsep'] is None else round(r['maxsep'], 4)} "
              f"sep={r['maxsep'] / (1 + r['maxsep']) if r['maxsep'] is not None else None} "
              f"S_sep={r['ssep'] if r['ssep'] is None else round(r['ssep'], 4)} "
              f"Delta={r['delta'] if r['delta'] is None else round(r['delta'], 3)} "
              f"L7a={r['l7a_dir']} {r['l7a_conf']} fals={r['fals']}")
    if rows:
        reel = next((r for r in rows if r["tag"] == "reel"), None)
        nul = next((r for r in rows if r["tag"] == "nul"), None)
        if reel and nul and reel["maxsep"] is not None \
                and nul["maxsep"] is not None:
            d = reel["maxsep"] - nul["maxsep"]
            print(f"d_maxsep = {reel['maxsep']:.4f} - {nul['maxsep']:.4f} "
                  f"= {d:+.4f}  (plancher 0,07 : "
                  f"{'PASSE' if d > 0.07 else 'ÉCHOUE'})")


if __name__ == "__main__":
    main()
