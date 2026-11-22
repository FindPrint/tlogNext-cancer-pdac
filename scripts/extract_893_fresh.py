#!/usr/bin/env python3
"""Extraction §8.93 — nuls frais pipeline (150 runs) + batterie reelle.

Lecture SEULE des dossiers results_fast_v62_893_*_nul_s9* et des 15
dossiers reels existants. Reutilise extract() de extract_858.py (methode
etablie des lots precedents). Aucun run lance, aucun fichier modifie.
Sorties : nulls_dist_893_fresh.json, nulls_dist_893_fresh.csv,
nulls_dist_893_fresh_summary.json (resume par paire, pour la section).
"""
import hashlib
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_858 import extract  # noqa: E402

PDAC = os.path.dirname(os.path.abspath(__file__))

PAIRS = [
    ("HP35", "results_fast_v62_hp35", "hp35"),
    ("TCGA_v4", "results_fast_v62_tcga_v4", "tcga_v4"),
    ("GSE71729", "results_fast_v62_geo71729", "geo71729"),
    ("GSE62452", "results_fast_v62_geo62452", "geo62452"),
    ("ICGC", "results_fast_v62_icgc", "icgc"),
    ("IMMUNE_TCGA", "results_fast_v62_immune_tcga", "immune_tcga"),
    ("PARP_TCGA", "results_fast_v62_parp_tcga", "parp_tcga"),
    ("DEPMAP", "results_fast_v62_depmap", "depmap"),
    ("GSE21501", "results_fast_v62_869_geo21501", "geo21501"),
    ("GSE79668", "results_fast_v62_870_geo79668", "geo79668"),
    ("GSE60979", "results_fast_v62_871_geo60979", "geo60979"),
    ("GSE131050_YehFF", "results_fast_v62_874_yeh_ff", "yeh_ff"),
    ("GSE57495", "results_fast_v62_879_geo57495", "geo57495"),
    ("GDC_ORGANOID", "results_fast_v62_885_gdc_organoid", "gdc_organoid"),
    ("GSE194249", "results_fast_v62_888_gse194249", "gse194249"),
]
GRAINES = list(range(9101, 9111))


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    # SHA v6.2 (lecture seule, verification)
    v6 = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
    print("v6.2 SHA:", sha(v6))
    rows, missing, summary = [], [], {}
    for nom, reel_dir, slug in PAIRS:
        reel = extract(reel_dir)
        reel["paire"] = nom
        reel["tag"] = "reel"
        reel["graine"] = None
        fresh = []
        for s in GRAINES:
            d = f"results_fast_v62_893_{slug}_nul_s{s}"
            p = os.path.join(PDAC, d, "master_results.json")
            if not os.path.exists(p):
                missing.append(d)
                continue
            e = extract(d)
            e["paire"] = nom
            e["tag"] = "nul_frais"
            e["graine"] = s
            e["sha_master"] = sha(p)
            fresh.append(e)
            rows.append(e)
        rows.append(reel)
        ms = np.array([f["maxsep"] for f in fresh if f["maxsep"] is not None], dtype=float)
        mc = np.array([f["mc_score"] for f in fresh if f["mc_score"] is not None], dtype=float)
        dl = np.array([f["delta"] for f in fresh if f["delta"] is not None], dtype=float)
        r_ms = reel["maxsep"]
        summary[nom] = {
            "n_frais": len(fresh),
            "reel": {"maxsep": reel["maxsep"], "mc": reel["mc_score"],
                     "delta": reel["delta"], "l7a_dir": reel["l7a_dir"],
                     "l7a_conf": reel["l7a_conf"], "l7b": reel["l7b"],
                     "fals": reel["fals"], "fals_status": reel["fals_status"],
                     "cascade_pct": reel["cascade_pct"],
                     "f1_ratio": reel.get("f1_ratio"), "f2_ratio": reel.get("f2_ratio"),
                     "n": reel["n"]},
            "frais_maxsep": {"mediane": float(np.median(ms)), "p95": float(np.percentile(ms, 95)),
                             "min": float(ms.min()), "max": float(ms.max()),
                             "moyenne": float(ms.mean())},
            "frais_mc_mediane": float(np.median(mc)),
            "frais_delta_mediane": float(np.median(dl)),
            "frais_l7a_dirs": {str(f["l7a_dir"]): sum(1 for g in fresh if str(g["l7a_dir"]) == str(f["l7a_dir"])) for f in fresh},
            "n_frais_sup_reel": int((ms > r_ms).sum()),
            "n_frais_sous_plancher_007": int(((r_ms - ms) > 0.07).sum()),
            "pct_frais_sous_plancher_007": float(100.0 * ((r_ms - ms) > 0.07).mean()),
            "frais_maxsep_liste": [round(float(x), 4) for x in ms],
        }
        print(f"{nom}: n_frais={len(fresh)} reel_maxsep={r_ms:.4f} "
              f"frais_med={np.median(ms):.4f} p95={np.percentile(ms, 95):.4f} "
              f"sup_reel={(ms > r_ms).sum()}/10 sous_plancher={((r_ms - ms) > 0.07).sum()}/10")
    with open(os.path.join(PDAC, "nulls_dist_893_fresh.json"), "w") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    keys = ["paire", "tag", "graine", "n", "control", "cascade_pct",
            "mc_score", "mc_thr", "maxsep", "stability", "ssep", "delta",
            "l7a_dir", "l7a_conf", "l7b", "fals", "fals_status", "regime",
            "f1_ratio", "f2_ratio"]
    pd.DataFrame([{k: r.get(k) for k in keys} for r in rows]).to_csv(
        os.path.join(PDAC, "nulls_dist_893_fresh.csv"), index=False)
    with open(os.path.join(PDAC, "nulls_dist_893_fresh_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Extraits : {len(rows)} runs (15 reels + {len(rows) - 15} nuls frais) ; manquants : {missing}")
    print("SHA nulls_dist_893_fresh.json:", sha(os.path.join(PDAC, "nulls_dist_893_fresh.json")))


if __name__ == "__main__":
    main()
