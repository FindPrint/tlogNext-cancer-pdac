#!/usr/bin/env python3
"""Compare les sorties v6.1 (lot) avec les sorties v6, réel + nul — VERSION 2 (17 nov. 2026).

Copie corrigée de extract_v61_lot_compare.py (l'original n'est pas modifié).
Corrections :
  1. Clés réelles du master_results.json (l'original lisait level_7a / level_5 /
     tension_delta, absentes) :
       - L7a        : prediction_levels.L7a_coherence.{consensus_direction, global_confidence}
       - Delta      : reading_synthesis.Delta_tension
       - MC         : run_pipeline.threshold_metadata.threshold_optimization.best_config
                      .{threshold, score, metrics.max_separation}
       - Cascade    : five_threshold_cascade.T_-2 .. T_+2
       - Falsif.    : holographic_tension_state.falsification_vs_null.delta_vs_null
                      (compare d_crit géométrique au cadre SpectralDimension ; ce
                      n'est PAS une comparaison au nul permuté)
  2. Équivalent v6 trouvé par le CSV d'entrée (metadata.csv_path) parmi les dossiers
     results_fast_* non-v61 dont la version est v6.0.0, et non plus par le nom du
     dossier (l'original manquait PARP, ATR, LUAD, COAD, nommés autrement en v6).

Usage : python3 extract_v61_lot_compare_v2.py manifest_v61_extended.txt \
            --csv v61_extended_compare.csv --md v61_extended_compare.md
Lecture seule : n'écrit que les deux fichiers de sortie.
"""
import argparse
import csv
import glob
import json
import math
import os

PDAC = os.path.dirname(os.path.abspath(__file__))
CASC_KEYS = ["T_-2_F2_pre_onset", "T_-1_F1_pre_inflection", "T_0_Monte_Carlo_Central",
             "T_+1_F1_post_deceleration", "T_+2_F2_post_attractor"]


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
    p = os.path.join(PDAC, d, "master_results.json")
    if not os.path.exists(p):
        return None
    r = json.load(open(p))
    casc = [fnum(g(r, "five_threshold_cascade." + k)) for k in CASC_KEYS]
    bc = g(r, "run_pipeline.threshold_metadata.threshold_optimization.best_config", {}) or {}
    l7 = g(r, "prediction_levels.L7a_coherence", {}) or {}
    return {
        "dir": d,
        "version": r.get("version") if isinstance(r.get("version"), str) else g(r, "version.master"),
        "csv_path": g(r, "metadata.csv_path"),
        "n": fnum(g(r, "reading_synthesis.n_samples")),
        "cascade": casc,
        "l7a_dir": l7.get("consensus_direction"),
        "l7a_conf": fnum(l7.get("global_confidence")),
        "l7a_status": l7.get("status"),
        "delta": fnum(g(r, "reading_synthesis.Delta_tension")),
        "mc_thr": fnum(bc.get("threshold")),
        "mc_score": fnum(bc.get("score")),
        "max_sep": fnum(g(bc, "metrics.max_separation")),
        "fals": fnum(g(r, "holographic_tension_state.falsification_vs_null.delta_vs_null")),
    }


def v6_index():
    idx = {}
    for d in sorted(glob.glob(os.path.join(PDAC, "results_fast_*"))):
        b = os.path.basename(d)
        if b.startswith("results_fast_v61_"):
            continue
        e = extract(b)
        if e and e["csv_path"] and str(e["version"]).startswith("v6.0.0"):
            idx.setdefault(os.path.basename(e["csv_path"]), []).append(e)
    return idx


def f(x, nd=2):
    return "—" if x is None else f"{x:.{nd}f}"


def casc_s(c):
    return "/".join(f(x) for x in c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--csv", required=True)
    ap.add_argument("--md", required=True)
    a = ap.parse_args()
    idx = v6_index()
    rows, pairs = [], {}
    for line in open(os.path.join(PDAC, a.manifest)):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, inp, out = line.split("|")
        e = extract(out)
        v6l = idx.get(os.path.basename(inp), [])
        v6 = v6l[0] if v6l else None
        row = {"serie": name, "input": inp, "out_v61": out, "status": "ok" if e else "MANQUANT",
               "v6_dir": v6["dir"] if v6 else "", "v6_ambigu": len(v6l) > 1}
        if e:
            row.update({k: e[k] for k in ["n", "l7a_dir", "l7a_conf", "delta", "mc_thr", "mc_score", "max_sep", "fals"]})
            for k, x in zip(["T_-2", "T_-1", "T_0", "T_+1", "T_+2"], e["cascade"]):
                row[k] = x
            if v6:
                row["v6_cascade"] = casc_s(v6["cascade"])
                row["cascade_identique_v6"] = all(
                    (x is None and y is None) or (x is not None and y is not None and abs(x - y) < 1e-6)
                    for x, y in zip(e["cascade"], v6["cascade"]))
                row["v6_l7a_dir"], row["v6_l7a_conf"] = v6["l7a_dir"], v6["l7a_conf"]
                row["v6_delta"], row["v6_mc_score"] = v6["delta"], v6["mc_score"]
        rows.append(row)
        base = name[:-4] if name.endswith("_NUL") else name
        pairs.setdefault(base, {})["NUL" if name.endswith("_NUL") else "REEL"] = row

    cols = ["serie", "input", "out_v61", "status", "n", "T_-2", "T_-1", "T_0", "T_+1", "T_+2",
            "l7a_dir", "l7a_conf", "delta", "mc_thr", "mc_score", "max_sep", "fals",
            "v6_dir", "v6_ambigu", "v6_cascade", "cascade_identique_v6", "v6_l7a_dir", "v6_l7a_conf",
            "v6_delta", "v6_mc_score"]
    with open(os.path.join(PDAC, a.csv), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in cols})

    done = [r for r in rows if r["status"] == "ok"]
    with_v6 = [r for r in done if r.get("v6_dir")]
    diff = [r for r in with_v6 if not r.get("cascade_identique_v6")]
    out = ["# Comparaison v6.1 / v6 — lot étendu (extracteur v2, 17 nov. 2026)", "",
           f"Runs terminés : {len(done)}/{len(rows)} ; avec équivalent v6 (même CSV d'entrée) : {len(with_v6)} ; "
           f"cascades différentes de v6 : {len(diff)}.", "",
           "| Série | n | Cascade v6.1 T-2/T-1/T0/T+1/T+2 % | L7a v6.1 | L7a v6 | Delta | MC seuil/score | max_sep | falsif | vs v6 |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if r["status"] != "ok":
            out.append(f"| {r['serie']} | — | MANQUANT | — | — | — | — | — | — | — |")
            continue
        c = [r[k] for k in ["T_-2", "T_-1", "T_0", "T_+1", "T_+2"]]
        vs = ("pas de v6" if not r.get("v6_dir") else
              ("identique v6" if r["cascade_identique_v6"] else "DIFFÈRE : " + r["v6_cascade"]))
        l6 = (f"{r.get('v6_l7a_dir')} {f(r.get('v6_l7a_conf'), 3)}" if r.get("v6_dir") else "—")
        out.append(f"| {r['serie']} | {f(r['n'], 0)} | {casc_s(c)} | {r['l7a_dir']} {f(r['l7a_conf'], 3)} | {l6} | "
                   f"{f(r['delta'])} | {f(r['mc_thr'])}/{f(r['mc_score'], 4)} | {f(r['max_sep'], 4)} | {f(r['fals'], 3)} | {vs} |")
    out += ["", "## Réel contre nul (v6.1)", "",
            "| Paire | T0 réel/nul | MC score réel/nul (écart) | Delta réel/nul (écart) | L7a réel / nul | falsif réel/nul |",
            "|---|---|---|---|---|---|"]
    for b in sorted(pairs):
        p = pairs[b]
        R, N = p.get("REEL"), p.get("NUL")
        if not R or not N or R["status"] != "ok" or N["status"] != "ok":
            out.append(f"| {b} | PAIRE INCOMPLÈTE | | | | |")
            continue
        out.append(f"| {b} | {f(R['T_0'])} / {f(N['T_0'])} | {f(R['mc_score'], 4)} / {f(N['mc_score'], 4)} "
                   f"({R['mc_score'] - N['mc_score']:+.4f}) | {f(R['delta'])} / {f(N['delta'])} "
                   f"({R['delta'] - N['delta']:+.2f}) | {R['l7a_dir']} {f(R['l7a_conf'], 3)} / "
                   f"{N['l7a_dir']} {f(N['l7a_conf'], 3)} | {f(R['fals'], 3)} / {f(N['fals'], 3)} |")
    open(os.path.join(PDAC, a.md), "w").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
