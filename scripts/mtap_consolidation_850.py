#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.50 — Consolidation de l'arbitrage MTAP : lecture des 14 runs v6.2
(réel original, réel de reproduction 850, 3 nuls anciens, 10 nuls frais)
et distribution des écarts S_sep réel − nul.
Protocole gelé : PROTOCOL_mtap_consolidation_850.md (écrit avant les runs).
Lecture seule : aucun seuil choisi après coup, aucune valeur inventée.
Reprend la logique de lecture de mtap_arbitration_846.py (read_run) :
S_sep = max_separation × stabilité ; MC recomposé
0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·acuité.
Sorties : mtap_consolidation_850_results.csv,
mtap_consolidation_850_extract.json.
"""
import ast
import hashlib
import json
import os

import numpy as np

PDAC = os.path.dirname(os.path.abspath(__file__))

RUNS = {
    "REEL": "results_fast_v62_mtap",
    "REEL_850": "results_fast_v62_mtap_850",
    "NUL42": "results_fast_v62_mtap_nul",
    "NUL_S7": "results_fast_v62_mtap_nul_s7",
    "NUL_S123": "results_fast_v62_mtap_nul_s123",
}
FRESH_SEEDS = (1011, 2022, 3033, 4044, 5055, 6066, 7077, 8088, 9099, 11111)
for s in FRESH_SEEDS:
    RUNS[f"NUL_S{s}"] = f"results_fast_v62_mtap_nul_s{s}"
FRESH = [f"NUL_S{s}" for s in FRESH_SEEDS]
OLD = ["NUL42", "NUL_S7", "NUL_S123"]
FLOOR = 0.07


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def g(d, path, default=None):
    cur = d
    for k in path.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def fnum(v):
    try:
        return None if v is None else float(v)
    except (TypeError, ValueError):
        return None


def read_run(d):
    r = json.load(open(os.path.join(PDAC, d, "master_results.json")))
    tm = g(r, "run_pipeline.threshold_metadata.threshold_optimization", {}) or {}
    bc = tm.get("best_config", {}) or {}
    m = bc.get("metrics", {}) or {}
    l7 = g(r, "prediction_levels.L7a_coherence", {}) or {}
    holo = g(r, "holographic_tension_state", {}) or {}
    casc = [fnum(g(r, "five_threshold_cascade." + k)) for k in
            ["T_-2_F2_pre_onset", "T_-1_F1_pre_inflection",
             "T_0_Monte_Carlo_Central", "T_+1_F1_post_deceleration",
             "T_+2_F2_post_attractor"]]
    mc_recomp = None
    if all(m.get(k) is not None for k in
           ("s_norm", "stability", "robustness", "sharpness")):
        mc_recomp = (0.3 * m["s_norm"] + 0.3 * m["stability"]
                     + 0.2 * m["robustness"] + 0.2 * m["sharpness"])
    try:
        arr = ast.literal_eval(tm["default_scan_curve"]) \
            if isinstance(tm.get("default_scan_curve"), str) else tm.get("default_scan_curve")
        sc = [(s["candidate"], s["score"]) for s in arr if s.get("score") is not None]
        dc, ds, dn = (max(sc, key=lambda t: t[1])[0], max(sc, key=lambda t: t[1])[1], len(sc)) if sc else (None, None, None)
    except Exception as e:  # noqa: BLE001 — consigné
        print(f"  !! default_scan_curve illisible pour {d} : {e}")
        dc, ds, dn = None, None, None
    return {
        "dir": d, "version": r.get("version"),
        "n": fnum(g(r, "reading_synthesis.n_samples")),
        "cascade_pct": casc,
        "mc_score": fnum(bc.get("score")), "mc_thr": fnum(bc.get("threshold")),
        "mc_recomp": mc_recomp,
        "mc_ecart_recomp": (None if mc_recomp is None or bc.get("score") is None
                            else abs(mc_recomp - float(bc["score"]))),
        "n_candidates": bc.get("n_candidates"), "w_size": bc.get("w_size"),
        "min_grp": bc.get("min_grp"), "rule": bc.get("rule"),
        "maxsep": fnum(m.get("max_separation")), "s_norm": fnum(m.get("s_norm")),
        "stability": fnum(m.get("stability")), "robustness": fnum(m.get("robustness")),
        "sharpness": fnum(m.get("sharpness")),
        "ssep": (None if m.get("max_separation") is None or m.get("stability") is None
                 else float(m["max_separation"]) * float(m["stability"])),
        "delta": fnum(g(r, "reading_synthesis.Delta_tension")),
        "d_vector": holo.get("D_vector"),
        "l7a_dir": l7.get("consensus_direction"),
        "l7a_conf": fnum(l7.get("global_confidence")),
        "fals": fnum(g(holo, "falsification_vs_null.delta_vs_null")),
        "default_thr": dc, "default_maxsep": ds, "default_n_scored": dn,
    }


def gap_stats(gaps):
    a = np.array(gaps, float)
    q = np.quantile(a, [0.0, 0.25, 0.5, 0.75, 1.0])
    return {
        "n": len(gaps), "min": float(q[0]), "q1": float(q[1]),
        "median": float(q[2]), "q3": float(q[3]), "max": float(q[4]),
        "mean": float(np.mean(a)),
        "n_above_floor": int(np.sum(a > FLOOR)),
        "n_at_or_below_floor": int(np.sum(a <= FLOOR)),
        "n_at_or_below_zero": int(np.sum(a <= 0.0)),
    }


def main():
    rows = {}
    for name, d in RUNS.items():
        rows[name] = read_run(d)
        e = rows[name]
        print(f"{name:12s} S_sep={e['ssep']:.4f} maxsep={e['maxsep']:.4f} "
              f"MC={e['mc_score']:.4f} Delta={e['delta']:.4f} "
              f"L7a={e['l7a_dir']} {e['l7a_conf']:.3f} "
              f"ecart_recomp={e['mc_ecart_recomp']:.2e}")
    reel = rows["REEL_850"]["ssep"]
    reel_orig = rows["REEL"]["ssep"]
    print(f"Réel 850 vs original : S_sep {reel:.6f} contre {reel_orig:.6f} "
          f"(écart {abs(reel - reel_orig):.2e})")
    gaps_fresh = [reel - rows[n]["ssep"] for n in FRESH]
    gaps_old = [reel - rows[n]["ssep"] for n in OLD]
    stats_fresh = gap_stats(gaps_fresh)
    stats_all = gap_stats(gaps_fresh + gaps_old)
    print("Écarts frais :", [f"{v:+.4f}" for v in gaps_fresh])
    print("Stats frais :", json.dumps(stats_fresh, indent=1))
    print("Stats 13 nuls :", json.dumps(stats_all, indent=1))
    mc_fresh = [rows[n]["mc_score"] for n in FRESH]
    dl_fresh = [rows[n]["delta"] for n in FRESH]
    print(f"MC réel {rows['REEL_850']['mc_score']:.4f} ; nuls frais "
          f"min {min(mc_fresh):.4f} max {max(mc_fresh):.4f} ; "
          f"nuls > réel : {sum(1 for v in mc_fresh if v > rows['REEL_850']['mc_score'])}")
    print(f"Delta réel {rows['REEL_850']['delta']:.4f} ; nuls frais "
          f"min {min(dl_fresh):.4f} max {max(dl_fresh):.4f} ; "
          f"nuls > réel : {sum(1 for v in dl_fresh if v > rows['REEL_850']['delta'])}")
    out = {"runs": rows, "reel_ssep_jour": reel,
           "gaps_frais": {n: reel - rows[n]["ssep"] for n in FRESH},
           "gaps_anciens": {n: reel - rows[n]["ssep"] for n in OLD},
           "stats_frais": stats_fresh, "stats_13_nuls": stats_all,
           "mc_frais": {n: rows[n]["mc_score"] for n in FRESH},
           "delta_frais": {n: rows[n]["delta"] for n in FRESH},
           "floor": FLOOR}
    with open(os.path.join(PDAC, "mtap_consolidation_850_extract.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=str)
    import csv
    with open(os.path.join(PDAC, "mtap_consolidation_850_results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["run", "dir", "ssep", "maxsep", "stabilite", "mc_score",
                    "mc_seuil", "mc_recomp", "ecart_recomp", "delta",
                    "l7a_dir", "l7a_conf", "falsification",
                    "cascade_T-2", "cascade_T-1", "cascade_T0",
                    "cascade_T+1", "cascade_T+2", "gap_ssep_vs_reel850",
                    "n_candidates", "w_size", "min_grp"])
        for name in RUNS:
            e = rows[name]
            w.writerow([name, e["dir"], e["ssep"], e["maxsep"], e["stability"],
                        e["mc_score"], e["mc_thr"], e["mc_recomp"],
                        e["mc_ecart_recomp"], e["delta"], e["l7a_dir"],
                        e["l7a_conf"], e["fals"]] + e["cascade_pct"] +
                       [None if name in ("REEL", "REEL_850") else reel - e["ssep"],
                        e["n_candidates"], e["w_size"], e["min_grp"]])
        w.writerow([])
        w.writerow(["stat", "valeur"])
        for k, v in stats_fresh.items():
            w.writerow([f"frais_{k}", v])
        for k, v in stats_all.items():
            w.writerow([f"13nuls_{k}", v])
        w.writerow(["reel_ssep_850", reel])
        w.writerow(["reel_ssep_original", reel_orig])
    print("SHA script : " + sha(__file__))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
