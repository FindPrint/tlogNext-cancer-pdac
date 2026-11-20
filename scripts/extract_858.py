#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extraction §8.58 — lecture SEULE des sorties existantes du pipeline v6.2
(aucun run lancé, aucun CSV modifié). Copie adaptée de stage_reading.py
(original intact), clés §8.38 : cascade, MC best_config, max_separation,
stability, S_sep = max_separation × stability, Delta, L7a, falsification,
L7b, bruit, F1/F2 « Tous ».
Sorties : extract_858.json, extract_858.csv.
"""
import json
import math
import os

import numpy as np

PDAC = os.path.dirname(os.path.abspath(__file__))
GROUPS = ["G1", "G2", "G3", "G4", "G5", "TEMOIN"]
CASC_KEYS = ["T_-2_F2_pre_onset", "T_-1_F1_pre_inflection",
             "T_0_Monte_Carlo_Central", "T_+1_F1_post_deceleration",
             "T_+2_F2_post_attractor"]


def g(o, path, default=None):
    for k in path.split("."):
        if not isinstance(o, dict) or k not in o:
            return default
        o = o[k]
    return o


def fnum(x):
    try:
        x = float(x)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def extract(d):
    r = json.load(open(os.path.join(PDAC, d, "master_results.json")))
    casc = [fnum(g(r, "five_threshold_cascade." + k)) for k in CASC_KEYS]
    bc = g(r, "run_pipeline.threshold_metadata.threshold_optimization.best_config", {}) or {}
    l7 = g(r, "prediction_levels.L7a_coherence", {}) or {}
    l7b = g(r, "prediction_levels.L7b_robustesse", {}) or {}
    n = int(fnum(g(r, "reading_synthesis.n_samples")) or 0)
    m = bc.get("metrics") or {}
    out = {
        "dir": d,
        "version": r.get("version") if isinstance(r.get("version"), str) else g(r, "version.master"),
        "n": n,
        "control": g(r, "metadata.control"),
        "target": g(r, "metadata.target"),
        "cascade_pct": casc,
        "cascade_pas": [None if c is None else round(c / 100 * (n - 1)) for c in casc],
        "l7a_dir": l7.get("consensus_direction"),
        "l7a_conf": fnum(l7.get("global_confidence")),
        "l7b": l7b.get("verdict") or l7b.get("status"),
        "delta": fnum(g(r, "reading_synthesis.Delta_tension")),
        "mc_thr": fnum(bc.get("threshold")),
        "mc_score": fnum(bc.get("score")),
        "maxsep": fnum(m.get("max_separation")),
        "stability": fnum(m.get("stability")),
        "ssep": (fnum(m.get("max_separation")) * fnum(m.get("stability"))
                 if fnum(m.get("max_separation")) is not None
                 and fnum(m.get("stability")) is not None else None),
        "fals": fnum(g(r, "holographic_tension_state.falsification_vs_null.delta_vs_null")),
        "fals_status": g(r, "holographic_tension_state.falsification_vs_null.status"),
        "regime": g(r, "reading_synthesis.dominant_regime"),
    }
    p = os.path.join(PDAC, d, "noise_diagnostic.json")
    if os.path.exists(p):
        nd = json.load(open(p))
        out["bruit_verdict"] = nd.get("diagnostic_label")
        out["bruit_score_moyen"] = fnum(nd.get("avg_variance_proxy_score"))
    p = os.path.join(PDAC, d, "transition_analysis.json")
    if os.path.exists(p):
        ta = json.load(open(p))

        def med_abs(key):
            vals = [abs(v["Tous"][key]) for v in ta.values()
                    if v and isinstance(v, dict) and v.get("Tous", {}).get("status") == "success"
                    and v["Tous"].get(key) is not None]
            return float(np.nanmedian(vals)) if vals else None

        n_ok = sum(1 for v in ta.values()
                   if v and isinstance(v, dict) and v.get("Tous", {}).get("status") == "success")
        f1pre, f1post = med_abs("first_derivative_pre"), med_abs("first_derivative")
        f2pre, f2post = med_abs("second_derivative_pre"), med_abs("second_derivative")
        sc = [k for k, v in ta.items()
              if v and isinstance(v, dict) and v.get("Tous", {}).get("status") == "success"
              and v["Tous"].get("first_derivative_pre") is not None
              and v["Tous"].get("first_derivative") is not None
              and (v["Tous"]["first_derivative_pre"] > 0) != (v["Tous"]["first_derivative"] > 0)]
        out["f1_avant"] = f1pre
        out["f1_apres"] = f1post
        out["f2_avant"] = f2pre
        out["f2_apres"] = f2post
        out["f1_ratio"] = (f1post / f1pre) if f1pre not in (None, 0) else None
        out["f2_ratio"] = (f2post / f2pre) if f2pre not in (None, 0) else None
        out["n_estimateurs_tous_ok"] = n_ok
        out["f1_changement_signe"] = sc
    return out


def main():
    rows = []
    missing = []
    for grp in GROUPS:
        for ordre in ("kras", "stage"):
            for tag in ("reel", "nul"):
                d = f"results_fast_v62_858_{grp}_{ordre}" + ("" if tag == "reel" else "_nul")
                if not os.path.exists(os.path.join(PDAC, d, "master_results.json")):
                    missing.append(d)
                    continue
                e = extract(d)
                e["groupe"] = grp
                e["ordre"] = ordre
                e["tag"] = tag
                rows.append(e)
    with open(os.path.join(PDAC, "extract_858.json"), "w") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    keys = ["groupe", "ordre", "tag", "n", "control", "target", "cascade_pct",
            "cascade_pas", "mc_score", "mc_thr", "maxsep", "stability", "ssep",
            "delta", "l7a_dir", "l7a_conf", "l7b", "fals", "regime",
            "bruit_verdict", "bruit_score_moyen", "f1_ratio", "f2_ratio"]
    import pandas as pd
    tab = pd.DataFrame([{k: r.get(k) for k in keys} for r in rows])
    tab.to_csv(os.path.join(PDAC, "extract_858.csv"), index=False)
    print(f"Extraits : {len(rows)} runs ; manquants : {len(missing)} {missing}")
    for r in rows:
        mc = r["mc_score"]
        print(f"{r['groupe']:7s} {r['ordre']:5s} {r['tag']:4s} n={r['n']} "
              f"casc={['—' if c is None else round(c, 1) for c in r['cascade_pct']]} "
              f"MC={mc if mc is None else round(mc, 4)} "
              f"S_sep={r['ssep'] if r['ssep'] is None else round(r['ssep'], 4)} "
              f"Delta={r['delta'] if r['delta'] is None else round(r['delta'], 3)} "
              f"L7a={r['l7a_dir']} {r['l7a_conf']} fals={r['fals']}")


if __name__ == "__main__":
    main()
