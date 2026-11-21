#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extraction + lecture §8.81 — lecture SEULE des sorties existantes du pipeline v6.2
(aucun run lancé, aucun CSV modifié). Copie adaptée de extract_858.py / stage_reading.py
(originaux intacts), clés §8.38 : cascade, MC best_config, max_separation, stability,
S_sep = max_separation × stability, Delta, L7a, falsification, L7b, bruit, F1/F2 « Tous ».
Tests directs sur la série PRIV (TCGA) : (D1) top-12 PRIV contre reste, (D2) Spearman flux vs
rang PRIV, (D3) autour de T_0 (±20). Pour UVM : (U3) déjà dans uvm_881.json, relu ici.
Sorties : priv_extract_881.json, priv_direct_tests_881_series.csv.
"""
import hashlib
import json
import math
import os

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

PDAC = os.path.dirname(os.path.abspath(__file__))
PAIRS = {
    "PRIV_TCGA_RÉEL": ("pdac_tcga_fluxes_v4_priv.csv", "results_fast_v62_881_priv"),
    "PRIV_TCGA_NUL": ("pdac_tcga_fluxes_v4_priv_nul.csv", "results_fast_v62_881_priv_nul"),
    "PRIV_UVM_RÉEL": ("pdac_uvm_fluxes_priv.csv", "results_fast_v62_881_priv_uvm"),
    "PRIV_UVM_NUL": ("pdac_uvm_fluxes_priv_nul.csv", "results_fast_v62_881_priv_uvm_nul"),
}
FLUXES = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20", "MUC2",
          "GSTM1", "CEACAM5", "CLCA1", "MUC16"]
CASC_KEYS = ["T_-2_F2_pre_onset", "T_-1_F1_pre_inflection", "T_0_Monte_Carlo_Central",
             "T_+1_F1_post_deceleration", "T_+2_F2_post_attractor"]
W = 20


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


def cohen_d(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    sp = np.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))
    return float((b.mean() - a.mean()) / sp) if sp > 0 else float("nan")


def extract(d):
    r = json.load(open(os.path.join(PDAC, d, "master_results.json")))
    casc = [fnum(g(r, "five_threshold_cascade." + k)) for k in CASC_KEYS]
    bc = g(r, "run_pipeline.threshold_metadata.threshold_optimization.best_config", {}) or {}
    l7 = g(r, "prediction_levels.L7a_coherence", {}) or {}
    l7b = g(r, "prediction_levels.L7b_robustesse", {}) or {}
    n = int(fnum(g(r, "reading_synthesis.n_samples")) or 0)
    m = bc.get("metrics") or {}
    maxsep = fnum(m.get("max_separation"))
    stab = fnum(m.get("stability"))
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
        "l7a_status": l7.get("status"),
        "l7b": l7b.get("verdict") or l7b.get("status"),
        "delta": fnum(g(r, "reading_synthesis.Delta_tension")),
        "mc_thr": fnum(bc.get("threshold")),
        "mc_score": fnum(bc.get("score")),
        "maxsep": maxsep,
        "stability": stab,
        "ssep": (maxsep * stab) if (maxsep is not None and stab is not None) else None,
        "sep": fnum(m.get("sep")),
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
        out["f1_avant"] = f1pre
        out["f1_apres"] = f1post
        out["f2_avant"] = f2pre
        out["f2_apres"] = f2post
        out["f1_ratio"] = (f1post / f1pre) if f1pre not in (None, 0) else None
        out["f2_ratio"] = (f2post / f2pre) if f2pre not in (None, 0) else None
        out["n_estimateurs_tous_ok"] = n_ok
    return out


def direct_series(csv_name):
    """D1 top-12 PRIV contre reste ; D2 Spearman flux vs rang PRIV."""
    df = pd.read_csv(os.path.join(PDAC, csv_name))
    n = len(df)
    rows = []
    for flux in FLUXES:
        if flux not in df.columns:
            continue
        v = df[flux].to_numpy(float)
        z = (v - v.mean()) / (v.std(ddof=0) if v.std(ddof=0) > 0 else 1.0)
        rho, p = spearmanr(np.arange(n), v)
        rows.append({"flux": flux,
                     "top12_moy_z": round(float(z[-12:].mean()), 3),
                     "top12_d": round(float(cohen_d(v[:-12], v[-12:])), 3),
                     "spearman_rho_priv": round(float(rho), 3),
                     "spearman_p_priv": float(p)})
    return df, rows


def around_threshold(df, pas):
    n = len(df)
    out = {}
    for flux in FLUXES:
        if flux not in df.columns:
            continue
        v = df[flux].to_numpy(float)
        lo = max(0, pas - W); hi = min(n, pas + W)
        before = v[lo:pas]; after = v[pas:hi]
        out[flux] = round(float(cohen_d(before, after)), 3) if len(before) >= 2 and len(after) >= 2 else None
    return out


def main():
    extr = {}
    for tag, (csv_name, d) in PAIRS.items():
        extr[tag] = extract(d)
        e = extr[tag]
        print(f"--- {tag} ({d}) ---")
        print(f"  version={e['version']} n={e['n']} control={e['control']} target={e['target']}")
        print(f"  cascade % : {e['cascade_pct']}")
        print(f"  cascade pas : {e['cascade_pas']}")
        print(f"  MC : score={e['mc_score']} seuil={e['mc_thr']} maxsep={e['maxsep']} "
              f"stabilité={e['stability']} S_sep={e['ssep']} sep={e['sep']}")
        print(f"  Delta={e['delta']} L7a={e['l7a_dir']} conf={e['l7a_conf']} "
              f"status={e['l7a_status']} L7b={e['l7b']}")
        print(f"  falsification delta_vs_null={e['fals']} status={e['fals_status']} régime={e['regime']}")
        print(f"  bruit={e.get('bruit_verdict')} score_moyen={e.get('bruit_score_moyen')}")
        print(f"  F1 avant/après={e.get('f1_avant')}/{e.get('f1_apres')} "
              f"(ratio {e.get('f1_ratio')}) ; "
              f"F2 avant/après={e.get('f2_avant')}/{e.get('f2_apres')} "
              f"(ratio {e.get('f2_ratio')}) ; estimateurs OK={e.get('n_estimateurs_tous_ok')}")

    all_rows = []
    around = {}
    for tag, (csv_name, d) in PAIRS.items():
        df, rows = direct_series(csv_name)
        for r in rows:
            r["série"] = tag
            all_rows.append(r)
        t0 = extr[tag]["cascade_pas"][2]
        if t0 is not None:
            around[tag] = around_threshold(df, t0)
            print(f"--- {tag} autour de T_0 (pas {t0}, ±{W}) : {around[tag]}")
        else:
            around[tag] = None
            print(f"--- {tag} : pas de T_0 lisible, pas de lecture autour du seuil.")
    dt = pd.DataFrame(all_rows)
    dt.to_csv(os.path.join(PDAC, "priv_direct_tests_881_series.csv"), index=False)
    print("\n--- D1 top-12 PRIV contre reste (d) ---")
    print(dt.pivot(index="flux", columns="série", values="top12_d").to_string())
    print("\n--- D2 Spearman flux vs rang PRIV ---")
    print(dt.pivot(index="flux", columns="série", values="spearman_rho_priv").to_string())

    # d_maxsep par paire (plancher gelé 0,07).
    for reel, nul, label in [("PRIV_TCGA_RÉEL", "PRIV_TCGA_NUL", "TCGA PRIV"),
                             ("PRIV_UVM_RÉEL", "PRIV_UVM_NUL", "UVM PRIV")]:
        d = extr[reel]["maxsep"] - extr[nul]["maxsep"]
        print(f"d_maxsep {label} : {extr[reel]['maxsep']:.4f} - {extr[nul]['maxsep']:.4f} = {d:+.4f} (plancher 0,07)")

    with open(os.path.join(PDAC, "priv_extract_881.json"), "w", encoding="utf-8") as f:
        json.dump({"extraction": extr, "autour_T0": around, "directs_serie": all_rows},
                  f, indent=2, ensure_ascii=False)
    print("\nÉcrit : priv_direct_tests_881_series.csv, priv_extract_881.json")
    print(f"SHA script : {hashlib.sha256(open(__file__, 'rb').read()).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
