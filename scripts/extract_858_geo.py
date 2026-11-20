#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extraction §8.58 confirmations — réutilise extract() de extract_858.py
(original intact). Dossiers results_fast_v62_858_71729_* (KRAS, 10 runs)
et results_fast_v62_858_62452_* (KRAS + stade, 20 runs).
Sorties : extract_858_geo.json, extract_858_geo.csv.
"""
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_858 import extract  # noqa: E402

PDAC = os.path.dirname(os.path.abspath(__file__))
GROUPS = ["G1", "G2", "G3", "G4", "G5"]


def main():
    rows = []
    missing = []
    for cohort, ordres in (("71729", ("kras",)), ("62452", ("kras", "stage"))):
        for grp in GROUPS:
            for ordre in ordres:
                for tag in ("reel", "nul"):
                    d = (f"results_fast_v62_858_{cohort}_{grp}_{ordre}"
                         + ("" if tag == "reel" else "_nul"))
                    if not os.path.exists(os.path.join(PDAC, d, "master_results.json")):
                        missing.append(d)
                        continue
                    e = extract(d)
                    e["cohorte"] = cohort
                    e["groupe"] = grp
                    e["ordre"] = ordre
                    e["tag"] = tag
                    rows.append(e)
    with open(os.path.join(PDAC, "extract_858_geo.json"), "w") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    keys = ["cohorte", "groupe", "ordre", "tag", "n", "control", "target",
            "cascade_pct", "cascade_pas", "mc_score", "mc_thr", "maxsep",
            "stability", "ssep", "delta", "l7a_dir", "l7a_conf", "l7b",
            "fals", "regime", "bruit_verdict", "bruit_score_moyen",
            "f1_ratio", "f2_ratio"]
    tab = pd.DataFrame([{k: r.get(k) for k in keys} for r in rows])
    tab.to_csv(os.path.join(PDAC, "extract_858_geo.csv"), index=False)
    print(f"Extraits : {len(rows)} runs ; manquants : {len(missing)} {missing}")
    for r in rows:
        mc = r["mc_score"]
        print(f"{r['cohorte']} {r['groupe']:3s} {r['ordre']:5s} {r['tag']:4s} "
              f"n={r['n']} casc={['—' if c is None else round(c, 1) for c in r['cascade_pct']]} "
              f"MC={mc if mc is None else round(mc, 4)} "
              f"S_sep={r['ssep'] if r['ssep'] is None else round(r['ssep'], 4)} "
              f"Delta={r['delta'] if r['delta'] is None else round(r['delta'], 3)} "
              f"L7a={r['l7a_dir']} {r['l7a_conf']} fals={r['fals']}")


if __name__ == "__main__":
    main()
