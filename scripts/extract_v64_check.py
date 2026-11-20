#!/usr/bin/env python3
"""Chantier v6.4 MC — verification CODE v6.4 vs HORS-LIGNE v6.2 (PROTOCOL_v6.4_mc.md §7.2).
Compare les 10 master_results.json v6.4 (results_fast_v64_*) a leurs
homologues v6.2, et le MC2 calcule en code a celui de v64_mc_table.json.
Criteres (porte A4) : 10/10 exit 0 (lu dans runs_v64_mc.log, pas ici) ;
best_config (score ancien, threshold, metriques), cascade T_-2..T_+2 et
S_sep IDENTIQUES a v6.2 (tol. 0 apres parsing JSON) ; MC2 en code ==
MC2 hors-ligne (tol. 1e-9) ; version v6.4.0-L7aL7b-CohenD-short.
Sortie : v64_mc_check.json (+ resume stdout).
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
PAIRS = [
    ("HP35_REAL", "results_fast_v64_hp35", "results_fast_v62_hp35"),
    ("HP35_NUL", "results_fast_v64_hp35_nul", "results_fast_v62_hp35_nul"),
    ("TCGAV4_REAL", "results_fast_v64_tcga_v4", "results_fast_v62_tcga_v4"),
    ("TCGAV4_NUL", "results_fast_v64_tcga_v4_nul", "results_fast_v62_tcga_v4_nul"),
    ("CEACAM5_REAL", "results_fast_v64_v4rot_ceacam5_dedup",
     "results_fast_v62_v4rot_ceacam5_dedup"),
    ("CEACAM5_NUL", "results_fast_v64_v4rot_ceacam5_dedup_nul",
     "results_fast_v62_v4rot_ceacam5_dedup_nul"),
    ("GSTM1_REAL", "results_fast_v64_v4rot_gstm1_dedup",
     "results_fast_v62_v4rot_gstm1_dedup"),
    ("GSTM1_NUL", "results_fast_v64_v4rot_gstm1_dedup_nul",
     "results_fast_v62_v4rot_gstm1_dedup_nul"),
    ("TESTA_REAL", "results_fast_v64_prolif", "results_fast_v62_prolif"),
    ("TESTA_NUL", "results_fast_v64_prolif_nul", "results_fast_v62_prolif_nul"),
]
NAME2OFF = {"HP35_REAL": "HP35", "HP35_NUL": "HP35",
            "TCGAV4_REAL": "TCGA_v4", "TCGAV4_NUL": "TCGA_v4",
            "CEACAM5_REAL": "V4ROT_CEACAM5", "CEACAM5_NUL": "V4ROT_CEACAM5",
            "GSTM1_REAL": "V4ROT_GSTM1", "GSTM1_NUL": "V4ROT_GSTM1",
            "TESTA_REAL": "TESTA_PROLIF", "TESTA_NUL": "TESTA_PROLIF"}


def load(d):
    p = os.path.join(BASE, d, "master_results.json")
    if not os.path.exists(p):
        return None
    return json.load(open(p))


def main():
    off = json.load(open(os.path.join(BASE, "v64_mc_table.json")))
    off_by_name = {r["paire"]: r for r in off["paires"]}
    rows, problems = [], []
    for name, d64, d62 in PAIRS:
        j64, j62 = load(d64), load(d62)
        if j64 is None:
            problems.append(f"{name}: JSON v6.4 absent ({d64})")
            continue
        if j62 is None:
            problems.append(f"{name}: JSON v6.2 absent ({d62})")
            continue
        bc64 = j64["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
        bc62 = j62["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
        casc64 = j64.get("five_threshold_cascade") or {}
        casc62 = j62.get("five_threshold_cascade") or {}
        mc64 = j64["run_pipeline"]["threshold_metadata"]["threshold_optimization"].get("mc_v64")
        side = "R" if name.endswith("_REAL") else "N"
        orow = off_by_name[NAME2OFF[name]]
        mc_off = orow["mc2_R"] if side == "R" else orow["mc2_N"]
        diffs = []
        for k in ("score", "threshold", "n_candidates", "w_size", "min_grp"):
            if bc64.get(k) != bc62.get(k):
                diffs.append(f"best_config.{k}: v6.4={bc64.get(k)} v6.2={bc62.get(k)}")
        for k, v in bc62.get("metrics", {}).items():
            if bc64.get("metrics", {}).get(k) != v:
                diffs.append(f"metrics.{k}: v6.4={bc64.get('metrics', {}).get(k)} v6.2={v}")
        for k, v in casc62.items():
            if casc64.get(k) != v:
                diffs.append(f"cascade.{k}: v6.4={casc64.get(k)} v6.2={v}")
        ssep64 = bc64["metrics"]["max_separation"] * bc64["metrics"]["stability"]
        ssep62 = bc62["metrics"]["max_separation"] * bc62["metrics"]["stability"]
        if ssep64 != ssep62:
            diffs.append(f"S_sep: {ssep64} vs {ssep62}")
        mc_code = (mc64 or {}).get("mc2")
        d_mc = None if mc_code is None else abs(mc_code - mc_off)
        if mc_code is None:
            diffs.append("mc_v64 absent du JSON v6.4")
        elif d_mc > 1e-9:
            diffs.append(f"MC2 code {mc_code} vs hors-ligne {mc_off} (|d|={d_mc:.2e})")
        if j64.get("version") != "v6.4.0-L7aL7b-CohenD-short":
            diffs.append(f"version v6.4: {j64.get('version')}")
        if j62.get("version") != "v6.2.0-L7aL7b-CohenD-short":
            diffs.append(f"version v6.2 attendue: {j62.get('version')}")
        rows.append({"run": name, "version_v64": j64.get("version"),
                     "mc2_code": mc_code, "mc2_offline": mc_off,
                     "abs_diff_mc2": d_mc,
                     "best_config_identique": len([d for d in diffs
                                                   if d.startswith(("best_config", "metrics", "cascade", "S_sep"))]) == 0,
                     "diffs": diffs})
        problems.extend(f"{name}: {d}" for d in diffs)
    gigue = max([abs(r["mc2_code"] - r["mc2_offline"])
                 for r in rows if r["mc2_code"] is not None] or [0.0])
    out = {"runs": rows, "problemes": problems,
           "gigue_mc2_mesuree": gigue,
           "n_runs_verifies": len(rows),
           "n_identiques_best_config_cascade": sum(1 for r in rows if r["best_config_identique"])}
    json.dump(out, open(os.path.join(BASE, "v64_mc_check.json"), "w"),
              indent=1, ensure_ascii=False)
    print(f"runs verifies: {len(rows)}/10")
    print(f"best_config+cascade identiques: {out['n_identiques_best_config_cascade']}/10")
    print(f"gigue MC2 (code vs hors-ligne): {gigue:.2e}")
    for r in rows:
        print(f"  {r['run']:14s} mc2 code={r['mc2_code']} offline={r['mc2_offline']} "
              f"|d|={r['abs_diff_mc2']:.1e} identique={r['best_config_identique']}")
    print(f"problemes: {problems if problems else 'AUCUN'}")
    print("écrit: v64_mc_check.json")


if __name__ == "__main__":
    main()
