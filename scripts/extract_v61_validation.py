#!/usr/bin/env python3
"""Extrait cascade, L7a, L4, MC, Delta de chaque dossier de sortie v6.1.

Usage : python3 extract_v61_validation.py <dir1> [<dir2> ...]
Sortie : une ligne par run, chiffres vérifiables depuis master_results.json.
"""
import json
import pathlib
import sys


def fmt(x, nd=2):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "n/d"
    if v != v:  # NaN
        return "NaN"
    return f"{v:.{nd}f}"


def one(d):
    p = pathlib.Path(d) / "master_results.json"
    if not p.exists():
        return f"{d}: PAS DE master_results.json"
    r = json.loads(p.read_text())
    ver = r.get("version", "?")
    casc = r.get("five_threshold_cascade", {})
    zones = [
        casc.get("T_-2_F2_pre_onset"),
        casc.get("T_-1_F1_pre_inflection"),
        casc.get("T_0_Monte_Carlo_Central"),
        casc.get("T_+1_F1_post_deceleration"),
        casc.get("T_+2_F2_post_attractor"),
    ]
    pl = r.get("prediction_levels", {})
    l7 = pl.get("L7a_coherence", {}) or {}
    l4 = pl.get("L4_risk", {}) or {}
    rs = r.get("reading_synthesis", {}) or {}
    tm = r.get("run_pipeline", {}).get("threshold_metadata", {}) or {}
    bo = (tm.get("threshold_optimization") or {}).get("best_config", {}) or {}
    metrics = bo.get("metrics", {}) or {}
    nd = r.get("run_pipeline", {}).get("noise_diagnostic", {}) or {}
    fals = rs.get("falsification_vs_null", {}) or {}
    n = rs.get("n_samples")
    lines = [
        f"== {d} ==",
        f"  version={ver} n={n}",
        "  cascade T_-2/T_-1/T_0/T_+1/T_+2 (%): "
        + " / ".join(fmt(z) for z in zones),
        f"  L7a: status={l7.get('status')} dir={l7.get('consensus_direction')} "
        f"conf={fmt(l7.get('global_confidence'), 3)} "
        f"probs up={fmt((l7.get('probabilities') or {}).get('up'), 3)} "
        f"down={fmt((l7.get('probabilities') or {}).get('down'), 3)} "
        f"flat={fmt((l7.get('probabilities') or {}).get('flat'), 3)}",
        f"  L4: status={l4.get('status')} level={l4.get('level')} "
        f"risk={fmt(l4.get('risk_score'), 3)} conf={fmt(l4.get('confidence'), 3)} "
        f"top_csd={fmt(l4.get('top_csd'), 3)}",
        f"  Delta_tension={fmt(rs.get('Delta_tension'))} "
        f"MC opt_threshold={fmt(tm.get('opt_threshold'))} "
        f"MC best_score={fmt(bo.get('score'), 4)} "
        f"max_separation={fmt(metrics.get('max_separation'), 4)}",
        f"  falsification_vs_null={json.dumps(fals)[:200]}",
        f"  noise: avg_proxy={fmt(nd.get('avg_variance_proxy_score'), 3)} "
        f"n_complete={nd.get('n_complete_scores')}/{len(nd.get('all_flux_diagnostics', []) or [])}",
    ]
    return "\n".join(lines)


for arg in sys.argv[1:]:
    print(one(arg))
    print()
