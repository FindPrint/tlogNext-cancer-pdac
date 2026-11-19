#!/usr/bin/env python3
"""Validation v6.2 — PROTOCOL_v6.2.md §5. Lecture SEULE des master_results.json.
Compare les 20 runs v6.2 (10 x 2 repetitions) aux references v6.1 :
cascades, L7a, L4, L5, MC best_score, max_separation, stability, S_sep, Delta.
Mesure la gigue par indicateur = max |rep1 - rep2| sur les 10 runs.
Verifie l'identite octet-pour-octet des JSON rep1/rep2 (sha256) et l'absence
d'horodatage dans master_results.json.
Sortie : v62_validation_table.md + v62_validation_table.json + resume stdout.
"""
import hashlib
import json
import math
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
HP35 = "/home/hatch/workspace/runs/biophysique-hp35"
CASC = ["T_-2_F2_pre_onset", "T_-1_F1_pre_inflection", "T_0_Monte_Carlo_Central",
        "T_+1_F1_post_deceleration", "T_+2_F2_post_attractor"]

# (nom, entree, dir_v61_ref, dir_v62_rep1, dir_v62_rep2)
RUNS = [
    ("HP35 reel", f"{HP35}/test_biophysique_input.csv",
     f"{HP35}/results_fast_hp35", "results_fast_v62_hp35", "results_fast_v62_hp35_rep2"),
    ("HP35 nul", f"{HP35}/test_biophysique_input_nul.csv",
     f"{HP35}/results_fast_hp35_nul", "results_fast_v62_hp35_nul", "results_fast_v62_hp35_nul_rep2"),
    ("TCGA v4 reel", "pdac_tcga_fluxes_v4.csv",
     "results_fast_v61_tcga_v4", "results_fast_v62_tcga_v4", "results_fast_v62_tcga_v4_rep2"),
    ("TCGA v4 nul", "pdac_tcga_fluxes_v4_nul.csv",
     "results_fast_v61_tcga_v4_nul", "results_fast_v62_tcga_v4_nul", "results_fast_v62_tcga_v4_nul_rep2"),
    ("GSE62452 reel", "pdac_geo62452_fluxes.csv",
     "results_fast_v61_geo62452", "results_fast_v62_geo62452", "results_fast_v62_geo62452_rep2"),
    ("GSE62452 nul", "pdac_geo62452_fluxes_nul.csv",
     "results_fast_v61_geo62452_nul", "results_fast_v62_geo62452_nul", "results_fast_v62_geo62452_nul_rep2"),
    ("ICGC reel", "pdac_icgc_fluxes.csv",
     "results_fast_v61_icgc", "results_fast_v62_icgc", "results_fast_v62_icgc_rep2"),
    ("ICGC nul", "pdac_icgc_fluxes_nul.csv",
     "results_fast_v61_icgc_nul", "results_fast_v62_icgc_nul", "results_fast_v62_icgc_nul_rep2"),
    ("DepMap reel", "pdac_depmap_fluxes.csv",
     "results_fast_v61_depmap", "results_fast_v62_depmap", "results_fast_v62_depmap_rep2"),
    ("DepMap nul", "pdac_depmap_fluxes_nul.csv",
     "results_fast_v61_depmap_nul", "results_fast_v62_depmap_nul", "results_fast_v62_depmap_nul_rep2"),
]


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


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def find_ts_keys(o, path=""):
    """Cherche les cles d'horodatage EXACTES dans l'arbre JSON (pas de
    sous-chaine : 'candidate' contient 'date' sans etre une date)."""
    hits = []
    TS = {"timestamp", "date", "generated_at", "run_date", "created_at",
          "datetime", "time", "ts"}
    if isinstance(o, dict):
        for k, v in o.items():
            if k.lower() in TS:
                hits.append(path + "/" + k)
            hits += find_ts_keys(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            hits += find_ts_keys(v, f"{path}[{i}]")
    return hits


def _eq(a, b):
    if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b):
        return True
    return a == b


def json_diff_paths(a, b, path=""):
    """Chemins divergents entre deux JSON (NaN == NaN)."""
    out = []
    if type(a) != type(b):
        out.append((path, "TYPE", repr(a)[:60], repr(b)[:60]))
        return out
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append((path + "/" + k, "ONLY_REP2", None, repr(b[k])[:60]))
            elif k not in b:
                out.append((path + "/" + k, "ONLY_REP1", repr(a[k])[:60], None))
            else:
                out += json_diff_paths(a[k], b[k], path + "/" + k)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((path, "LEN", len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            out += json_diff_paths(x, y, f"{path}[{i}]")
    elif not _eq(a, b):
        out.append((path, "VAL", repr(a)[:80], repr(b)[:80]))
    return out


def classify_diffs(diffs):
    """Classe les divergences : chemins runtime (nom du dossier de sortie),
    budget workers (RAM libre au lancement), autres (scientifiques)."""
    runtime = [d for d in diffs if d[0].startswith("/runtime/")
               and ("dashboard_status/path" in d[0] or "telemetry_path" in d[0])]
    worker = [d for d in diffs if "worker_budget" in d[0]
              or d[0].endswith("/n_workers") or d[0].endswith("/chunksize")
              or d[0].endswith("/safe_cap")]
    other = [d for d in diffs if d not in runtime and d not in worker]
    return {"n_total": len(diffs), "n_runtime_paths": len(runtime),
            "n_worker_budget": len(worker), "n_other": len(other),
            "other_paths": [d[0] for d in other]}


def extract(d):
    p = d if os.path.isabs(d) else os.path.join(BASE, d)
    j = json.load(open(os.path.join(p, "master_results.json")))
    casc = [fnum(g(j, "five_threshold_cascade." + k)) for k in CASC]
    bc = g(j, "run_pipeline.threshold_metadata.threshold_optimization.best_config", {}) or {}
    m = g(bc, "metrics", {}) or {}
    l7 = g(j, "prediction_levels.L7a_coherence", {}) or {}
    l4 = g(j, "prediction_levels.L4_risk", {}) or {}
    l5 = g(j, "prediction_levels.L5_complexity", {}) or {}
    maxsep = fnum(m.get("max_separation"))
    stab = fnum(m.get("stability"))
    return {
        "dir": d, "version": j.get("version"),
        "sha": sha(os.path.join(p, "master_results.json")),
        "ts_keys": find_ts_keys(j),
        "n": fnum(g(j, "reading_synthesis.n_samples")),
        "cascade": casc,
        "cascade_pas": [int(round(c / 100.0 * fnum(g(j, "reading_synthesis.n_samples")))) if c is not None else None for c in casc],
        "mc_thr": fnum(bc.get("threshold")), "mc_score": fnum(bc.get("score")),
        "max_sep": maxsep, "stability": stab,
        "s_sep": (maxsep * stab) if (maxsep is not None and stab is not None) else None,
        "robustness": fnum(m.get("robustness")), "sharpness": fnum(m.get("sharpness")),
        "delta": fnum(g(j, "reading_synthesis.Delta_tension")),
        "fals": fnum(g(j, "holographic_tension_state.falsification_vs_null.delta_vs_null")),
        "l7a_dir": l7.get("consensus_direction"), "l7a_conf": fnum(l7.get("global_confidence")),
        "l7a_status": l7.get("status"),
        "l4_level": l4.get("level"), "l4_risk": fnum(l4.get("risk_score")),
        "l5_top": l5.get("top_metric"), "l5_conf": fnum(l5.get("confidence")),
        "l5_n_alerts": l5.get("n_alerts"),
        "l5_stability": fnum(g(l5, "multi_horizon.stability")),
        "l5_ranking": [(r.get("metric"), fnum(r.get("score"))) for r in (l5.get("ranking") or [])],
        "l5_alerts": sorted((l5.get("alerts") or []), key=lambda a: json.dumps(a, sort_keys=True, default=str)),
    }


def signed(d, c):
    if c is None:
        return None
    return {"up": c, "down": -c, "flat": 0.0}.get(d, None)


def main():
    rows = []
    for name, inp, d61, d1, d2 in RUNS:
        r61 = extract(d61)
        r1 = extract(d1)
        r2 = extract(d2)
        j1 = json.load(open(os.path.join(BASE, d1, "master_results.json")))
        j2 = json.load(open(os.path.join(BASE, d2, "master_results.json")))
        diffs = classify_diffs(json_diff_paths(j1, j2))
        casc_id = r1["cascade"] == r61["cascade"]
        casc_id_rep = r1["cascade"] == r2["cascade"]
        jit = {}
        for k in ("mc_score", "max_sep", "stability", "s_sep", "delta", "fals",
                  "l4_risk", "l5_conf", "l5_stability"):
            a, b = r1.get(k), r2.get(k)
            jit[k] = abs(a - b) if (a is not None and b is not None) else None
        jit["l7a_signed"] = (abs(signed(r1["l7a_dir"], r1["l7a_conf"]) - signed(r2["l7a_dir"], r2["l7a_conf"]))
                             if signed(r1["l7a_dir"], r1["l7a_conf"]) is not None
                             and signed(r2["l7a_dir"], r2["l7a_conf"]) is not None else None)
        jit["cascade_max"] = max([abs(a - b) for a, b in zip(r1["cascade"], r2["cascade"])
                                  if a is not None and b is not None] or [0.0])
        rows.append({"run": name, "input": inp, "n": r1["n"],
                     "v61": r61, "rep1": r1, "rep2": r2,
                     "cascade_identique_v61": casc_id, "cascade_identique_rep": casc_id_rep,
                     "json_identique_rep": r1["sha"] == r2["sha"],
                     "json_diff": diffs,
                     "l5_identique_rep": (r1["l5_ranking"] == r2["l5_ranking"]
                                          and r1["l5_alerts"] == r2["l5_alerts"]
                                          and r1["l5_top"] == r2["l5_top"]
                                          and r1["l5_conf"] == r2["l5_conf"]
                                          and r1["l5_n_alerts"] == r2["l5_n_alerts"]),
                     "l4_identique_rep": (r1["l4_risk"] == r2["l4_risk"]
                                          and r1["l4_level"] == r2["l4_level"]),
                     "l7a_identique_rep": (r1["l7a_dir"] == r2["l7a_dir"]
                                           and r1["l7a_conf"] == r2["l7a_conf"]),
                     "jitter": jit})
    # Gigues max sur les 10 runs.
    jkeys = list(rows[0]["jitter"].keys())
    gmax = {}
    for k in jkeys:
        vals = [r["jitter"][k] for r in rows if r["jitter"][k] is not None]
        gmax[k] = max(vals) if vals else None
    out = {"runs": rows, "gigue_max": gmax,
           "sha_v62": sha(os.path.join(HP35, "universal_v6.2.0_cohen.py")),
           "sha_v61": sha(os.path.join(HP35, "universal_v6.1.0_cohen.py")),
           "sha_v6": sha(os.path.join(HP35, "universal_v6.0.0_cohen.py"))}
    json.dump(out, open(os.path.join(BASE, "v62_validation_table.json"), "w"),
              indent=1, default=str)
    print("=== VALIDATION v6.2 — 10 runs x 2 repetitions ===")
    for r in rows:
        r1, r61 = r["rep1"], r["v61"]
        print(f"{r['run']} n={r['n']:.0f} {r1['version']}")
        print(f"  cascade v62 rep1: {' / '.join(f'{c:.2f}' for c in r1['cascade'])} "
              f"(pas {r1['cascade_pas']}) | identique v6.1: {r['cascade_identique_v61']} | "
              f"identique rep2: {r['cascade_identique_rep']}")
        print(f"  L7a v62: {r1['l7a_dir']} {r1['l7a_conf']} (v6.1: {r61['l7a_dir']} {r61['l7a_conf']}) "
              f"| L4: {r1['l4_level']} {r1['l4_risk']} | L5 top: {r1['l5_top']} conf {r1['l5_conf']} "
              f"n_alerts {r1['l5_n_alerts']} stab {r1['l5_stability']}")
        print(f"  MC {r1['mc_score']:.4f} (v6.1 {r61['mc_score']:.4f}) | max_sep {r1['max_sep']:.4f} "
              f"| stab {r1['stability']:.4f} | S_sep {r1['s_sep']:.4f} | Delta {r1['delta']} "
              f"| fals {r1['fals']}")
        print(f"  JSON rep1==rep2 octet-pour-octet: {r['json_identique_rep']} | "
              f"divergences (NaN-aware) : total={r['json_diff']['n_total']} "
              f"chemins_runtime={r['json_diff']['n_runtime_paths']} "
              f"budget_workers={r['json_diff']['n_worker_budget']} "
              f"autres={r['json_diff']['n_other']} {r['json_diff']['other_paths'] or ''} | "
              f"L5 identique: {r['l5_identique_rep']} | L4 identique: {r['l4_identique_rep']} | "
              f"L7a identique: {r['l7a_identique_rep']} | cles horodatage exactes: {r1['ts_keys'] or 'aucune'}")
        print(f"  gigue rep1-rep2: " + ", ".join(
            f"{k}={r['jitter'][k]:.4f}" if r['jitter'][k] is not None else f"{k}=n/d" for k in jkeys))
    print()
    print("GIGUE MAX sur 10 runs (max |rep1-rep2|) :")
    for k, v in gmax.items():
        print(f"  {k}: {v}")
    n_casc_ok = sum(1 for r in rows if r["cascade_identique_v61"])
    n_json_ok = sum(1 for r in rows if r["json_identique_rep"])
    n_other0 = sum(1 for r in rows if r["json_diff"]["n_other"] == 0)
    n_ts0 = sum(1 for r in rows if not r["rep1"]["ts_keys"])
    print(f"\nCascades identiques v6.1 : {n_casc_ok}/10 | JSON rep1==rep2 octet-pour-octet : {n_json_ok}/10")
    print(f"Divergences non-runtime/non-worker : 0 sur {n_other0}/10 runs | "
          f"Sans cle d'horodatage exacte : {n_ts0}/10 runs")
    print("Ecrit : v62_validation_table.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
