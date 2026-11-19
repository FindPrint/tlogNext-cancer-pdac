#!/usr/bin/env python3
"""Compare les sorties v6.1 (lot) avec les sorties v6 existantes, réel + nul.

Usage : python3 extract_v61_lot_compare.py <manifeste> [--out rapport.md]
- Lit chaque ligne NOM|ENTREE|SORTIE_V61 du manifeste.
- Extrait cascade / L7a / Delta / MC / max_separation / falsification de la
  sortie v6.1 (si master_results.json présent, sinon « EN COURS »).
- Cherche l'équivalent v6 en remplaçant 'results_fast_v61_' par 'results_fast_'
  (rotations : même règle ; seul v4rot_CLDN18 a un équivalent v6, v4r_cldn18).
- Sort une table Markdown + un résumé réel-vs-nul par paire (base sans _NUL).
"""
import argparse
import json
import os
import sys

PDAC = os.path.dirname(os.path.abspath(__file__))


def load(path):
    with open(path) as f:
        return json.load(f)


def extract(d):
    p = os.path.join(PDAC, d, "master_results.json")
    if not os.path.exists(p):
        return None
    r = load(p)
    c = r["five_threshold_cascade"]
    casc = [c[k] for k in
            ["T_-2_F2_pre_onset", "T_-1_F1_pre_inflection",
             "T_0_Monte_Carlo_Central", "T_+1_F1_post_deceleration",
             "T_+2_F2_post_attractor"]]
    l7 = r.get("prediction_levels", {}).get("level_7a", {}) or {}
    hts = r.get("holographic_tension_state", {}) or {}
    fals = (hts.get("falsification_vs_null") or {})
    mc = r.get("prediction_levels", {}).get("level_5", {}) or {}
    return {
        "cascade": "/".join(f"{x:.2f}" for x in casc),
        "t0": casc[2],
        "l7a": f"{l7.get('direction', '?')} {l7.get('confidence', float('nan')):.3f}"
               if isinstance(l7.get("confidence"), (int, float)) else "?",
        "delta": hts.get("tension_delta", float("nan")),
        "mc_opt": mc.get("optimal_threshold", float("nan")),
        "mc_best": mc.get("best_score", float("nan")),
        "max_sep": mc.get("max_separation", float("nan")),
        "fals": fals.get("delta_vs_null"),
    }


def fmt(x, nd=2):
    try:
        return f"{float(x):.{nd}f}"
    except (TypeError, ValueError):
        return "—"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    rows = []
    done = changed = 0
    total = 0
    pairs = {}
    for line in open(os.path.join(PDAC, args.manifest)):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, _inp, out61 = line.split("|")
        total += 1
        v61 = extract(out61)
        v6dir = out61.replace("results_fast_v61_", "results_fast_", 1)
        v6 = extract(v6dir) if v6dir != out61 else None
        base = name[:-4] if name.endswith("_NUL") else name
        pairs.setdefault(base, {})["NUL" if name.endswith("_NUL") else "REEL"] = v61
        if v61 is None:
            rows.append(f"| {name} | EN COURS | — | — | — | — | — |")
            continue
        done += 1
        same = (v6 is not None and v6["cascade"] == v61["cascade"])
        if v6 is not None and not same:
            changed += 1
        rows.append(
            f"| {name} | {v61['cascade']} | {v61['l7a']} | {fmt(v61['delta'])} | "
            f"{fmt(v61['mc_opt'])}/{fmt(v61['mc_best'], 4)} | {fmt(v61['max_sep'], 4)} | "
            f"{fmt(v61['fals'], 3) if v61['fals'] is not None else 'indisp.'} | "
            f"{'identique v6' if same else ('DIFFÈRE de v6 : ' + (v6['cascade'] if v6 else 'pas de v6'))} |")
    out = []
    out.append(f"# Comparaison v6.1 / v6 — {args.manifest} (16 nov. 2026)")
    out.append(f"Terminés : {done}/{total} ; cascades différentes de v6 : {changed}.")
    out.append("")
    out.append("| Série | Cascade v6.1 (T_-2/T_-1/T_0/T_+1/T_+2 %) | L7a | Delta | MC opt/best | max_sep | falsif. | vs v6 |")
    out.append("|---|---|---|---|---|---|---|---|")
    out.extend(rows)
    out.append("")
    out.append("## Réel contre nul (v6.1, paires terminées)")
    for base in sorted(pairs):
        p = pairs[base]
        if "REEL" not in p or "NUL" not in p or p["REEL"] is None or p["NUL"] is None:
            continue
        r, n = p["REEL"], p["NUL"]
        out.append(f"- **{base}** : T_0 réel {r['t0']:.2f} % contre nul {n['t0']:.2f} % ; "
                   f"MC {fmt(r['mc_best'], 4)} contre {fmt(n['mc_best'], 4)} ; "
                   f"Delta {fmt(r['delta'])} contre {fmt(n['delta'])} ; "
                   f"L7a {r['l7a']} contre {n['l7a']}.")
    text = "\n".join(out) + "\n"
    if args.out:
        open(os.path.join(PDAC, args.out), "w").write(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
