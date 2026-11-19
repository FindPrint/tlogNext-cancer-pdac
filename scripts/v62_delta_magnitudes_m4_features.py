#!/usr/bin/env python3
"""Supplement DESCRIPTIF a v62_delta_magnitudes.py (chantier 3, suite).
Ne contient AUCUN nouveau modele : pour chaque cible, il nomme les 3 traits
(RESUMES REDUITS, 41) les plus correles (Pearson) sur les 222 runs, et le
meilleur trait unique par cible en LOCO-poole (recalcule a partir des
predictions deja produites ? non — simple correlation descriptive).
But : dire QUEL resume porte les rares R2 positifs de M4 (Petrosian, Katz,
BoxCounting, GraphDimension, LevinaBickel), et lequel ne porte rien
(LocalPCA, PCAIntrinsic, DFA, Hurst2mH).
Lecture seule des sorties deja produites : v62_delta_levels.csv et
v62_delta_magnitudes_flux_features.csv. Sortie :
v62_delta_magnitudes_m4_features.json / .log.
"""
import csv
import json
import os
import sys

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
DIV = ["LevinaBickel", "PCAIntrinsic", "LocalPCA", "GraphDimension",
       "PersistentHomology", "MFA"]
SAT = ["Higuchi", "Katz", "Petrosian", "Sevcik", "BoxCounting", "Hurst2mH", "DFA"]
TARGETS = DIV + SAT
STAT_NAMES = ["mean", "sd", "min", "max", "range", "skew", "kurt", "ac1",
              "mean_abs_diff", "sd_diff", "drift", "spearman_idx", "pearson_idx"]
FEAT_NAMES = ([f"agg_mean_{s}" for s in STAT_NAMES]
              + [f"agg_sd_{s}" for s in STAT_NAMES]
              + ["cross_mean_abs_r", "cross_sd_r", "cross_frac_r_gt_08",
                 "cross_pc1", "cross_pc2", "cross_mean_abs_load_pc1",
                 "cross_pc1_plus_pc2"]
              + ["ctrl_n_unique", "ctrl_range", "ctrl_sd", "ctrl_is_step"]
              + ["glob_n", "glob_p", "glob_n_x_p", "glob_log_n"])
assert len(FEAT_NAMES) == 41


def parse_sorted(s):
    out = {}
    for part in str(s).split(";"):
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        out[k.strip()] = float(v)
    return out


def pearson(a, b):
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3 or a.std() == 0 or b.std() == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def main():
    levels = list(csv.DictReader(open(os.path.join(BASE, "v62_delta_levels.csv"))))
    feats = {}
    with open(os.path.join(BASE, "v62_delta_magnitudes_flux_features.csv")) as fh:
        for r in csv.DictReader(fh):
            feats[r["csv_path"]] = np.array([float(r[f"red_{i}"]) for i in range(41)])
    # csv_path par run : relu depuis les JSON (comme le script principal).
    import json as _json
    rows = []
    for lv in levels:
        j = _json.load(open(os.path.join(BASE, lv["dir"], "master_results.json")))
        cp = (j.get("metadata") or {}).get("csv_path")
        div = parse_sorted(lv["div_sorted"])
        sat = parse_sorted(lv["sat_sorted"])
        rows.append({"dir": lv["dir"], "csv_path": cp,
                     "targets": {t: (div.get(t) if t in DIV else sat.get(t)) for t in TARGETS}})
    X = np.array([feats[r["csv_path"]] for r in rows])
    out = {}
    lines = ["=== Supplement descriptif M4 : meilleur trait unique par cible (222 runs) ==="]
    for j, t in enumerate(TARGETS):
        y = np.array([r["targets"][t] if r["targets"][t] is not None else np.nan
                      for r in rows])
        scored = []
        for f in range(41):
            r_ = pearson(X[:, f], y)
            if r_ is not None:
                scored.append((abs(r_), r_, FEAT_NAMES[f]))
        scored.sort(reverse=True)
        top3 = [{"trait": name, "r": round(r_, 3), "|r|": round(a, 3)}
                for a, r_, name in scored[:3]]
        out[t] = {"n": int(np.isfinite(y).sum()), "top3": top3}
        lines.append(f"  {t} (n={int(np.isfinite(y).sum())}) : " +
                     " ; ".join(f"{d['trait']} r={d['r']}" for d in top3))
    json.dump(out, open(os.path.join(BASE, "v62_delta_magnitudes_m4_features.json"), "w"),
              indent=1, default=str)
    open(os.path.join(BASE, "v62_delta_magnitudes_m4_features.log"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
