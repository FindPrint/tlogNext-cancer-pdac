#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extraction §8.82 — lecture SEULE des sorties existantes du pipeline v6.2
(aucun run lancé, aucun CSV modifié). Réutilise extract() de extract_858.py
(original intact), comme extract_866.py / extract_869.py / extract_871.py /
extract_874.py / extract_876.py.
Usage : python3 extract_882.py
Sorties : extract_882.json, extract_882.csv.
"""
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_858 import extract  # noqa: E402

PDAC = os.path.dirname(os.path.abspath(__file__))

RUNS = [
    ("prolif", "reel", "results_fast_v62_882_gbm_prolif"),
    ("prolif", "nul", "results_fast_v62_882_gbm_prolif_nul"),
    ("prolif", "nul_s8821", "results_fast_v62_882_gbm_prolif_nul_s8821"),
    ("prolif", "nul_s8822", "results_fast_v62_882_gbm_prolif_nul_s8822"),
    ("privilege", "reel", "results_fast_v62_882_gbm_privilege"),
    ("privilege", "nul", "results_fast_v62_882_gbm_privilege_nul"),
]


def main():
    rows = []
    missing = []
    for paire, tag, d in RUNS:
        if not os.path.exists(os.path.join(PDAC, d, "master_results.json")):
            missing.append(d)
            continue
        e = extract(d)
        e["paire"] = paire
        e["tag"] = tag
        rows.append(e)
    with open(os.path.join(PDAC, "extract_882.json"), "w") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    keys = ["paire", "tag", "n", "control", "target", "cascade_pct",
            "cascade_pas", "mc_score", "mc_thr", "maxsep", "stability",
            "ssep", "delta", "l7a_dir", "l7a_conf", "l7b", "fals",
            "fals_status", "regime", "bruit_verdict", "bruit_score_moyen",
            "f1_ratio", "f2_ratio"]
    tab = pd.DataFrame([{k: r.get(k) for k in keys} for r in rows])
    tab.to_csv(os.path.join(PDAC, "extract_882.csv"), index=False)
    print(f"Extraits : {len(rows)} runs ; manquants : {len(missing)} {missing}")
    for r in rows:
        mc = r["mc_score"]
        print(f"{r['paire']:9s} {r['tag']:9s} n={r['n']} "
              f"casc={['—' if c is None else round(c, 1) for c in r['cascade_pct']]} "
              f"MC={mc if mc is None else round(mc, 4)} "
              f"maxsep={r['maxsep'] if r['maxsep'] is None else round(r['maxsep'], 4)} "
              f"sep={r['maxsep'] / (1 + r['maxsep']) if r['maxsep'] is not None else None} "
              f"S_sep={r['ssep'] if r['ssep'] is None else round(r['ssep'], 4)} "
              f"Delta={r['delta'] if r['delta'] is None else round(r['delta'], 3)} "
              f"L7a={r['l7a_dir']} {r['l7a_conf']} fals={r['fals']}")
    if rows:
        reel = {r["paire"]: r for r in rows if r["tag"] == "reel"}
        nul = {r["paire"]: r for r in rows if r["tag"] == "nul"}
        for paire in ("prolif", "privilege"):
            if paire in reel and paire in nul:
                mr, mn = reel[paire]["maxsep"], nul[paire]["maxsep"]
                if mr is None or mn is None:
                    print(f"d_maxsep {paire} = INDISPONIBLE "
                          f"(réel {mr} vs nul {mn})")
                else:
                    dmax = mr - mn
                    print(f"d_maxsep {paire} = {dmax:+.4f} "
                          f"(réel {mr:.4f} vs nul {mn:.4f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
