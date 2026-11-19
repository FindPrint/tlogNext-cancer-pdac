#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lecture du Étape 4 (c) — série TCGA v4 ordonnée par CN MTAP (18 nov. 2026).
Lecture SEULE des sorties existantes du pipeline v6.1 (aucun run lancé,
aucun CSV modifié). Protocole : PROTOCOL_enrichissements_833.md.

Ce qui vient DU PIPELINE (master_results.json, transition_analysis.json,
noise_diagnostic.json) : cascade, MC best_config + composantes, Delta,
L7a, falsification, L7b, bruit, F1/F2 « Tous ».
Ce qui est APPORTÉ par ce script (harnais, hors pipeline) : tests directs
top-12 contre reste, flux par flux (d de Cohen, z global), Spearman flux
vs rang, et lecture autour de T_0 (fenêtres ±20) — même méthode que
pistes_v61_flux_reading.py / per_flux_reading.py.
Sorties : mtap_reading.md, mtap_extract.json, mtap_direct_tests.csv.
"""
import json
import math
import os

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

PDAC = os.path.dirname(os.path.abspath(__file__))
PAIRS = {
    "MTAP_RÉEL": ("pdac_tcga_fluxes_v4_mtap.csv", "results_fast_v61_mtap"),
    "MTAP_NUL": ("pdac_tcga_fluxes_v4_mtap_nul.csv", "results_fast_v61_mtap_nul"),
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
    """d = (moyenne(b) - moyenne(a)) / écart-type poolé. Positif = b plus haut."""
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
    out = {
        "dir": d,
        "version": r.get("version") if isinstance(r.get("version"), str) else g(r, "version.master"),
        "n": fnum(g(r, "reading_synthesis.n_samples")),
        "control_col": g(r, "reading_synthesis.control_col"),
        "cascade_pct": casc,
        "cascade_pas": [None if c is None else round(c / 100 * (int(fnum(g(r, "reading_synthesis.n_samples")) or 177) - 1)) for c in casc],
        "l7a_dir": l7.get("consensus_direction"),
        "l7a_conf": fnum(l7.get("global_confidence")),
        "l7a_status": l7.get("status"),
        "l7b": l7b.get("verdict") or l7b.get("status"),
        "delta": fnum(g(r, "reading_synthesis.Delta_tension")),
        "mc_thr": fnum(bc.get("threshold")),
        "mc_score": fnum(bc.get("score")),
        "mc_metrics": bc.get("metrics") or {},
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
        # Médiane |F1| / |F2| avant/après sur les estimateurs en succès,
        # même méthode que pistes_v61_flux_reading.py.
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


def direct_tests(csv_name):
    df = pd.read_csv(os.path.join(PDAC, csv_name))
    n = len(df)
    rows = []
    for flux in FLUXES:
        v = df[flux].to_numpy(float)
        z = (v - v.mean()) / (v.std(ddof=0) if v.std(ddof=0) > 0 else 1.0)
        # Top-12 = les 12 tumeurs les PLUS DÉLÉTÉES en MTAP = les 12
        # PREMIÈRES lignes (tri par CN MTAP croissant). + = plus haut
        # chez les 12 plus délétées. Spearman vs rang : le rang monte
        # avec CN MTAP (rang 0 = perte la plus profonde).
        top12 = v[:12]
        rest = v[12:]
        d = cohen_d(rest, top12)
        rho, p = spearmanr(np.arange(n), v)
        rows.append({"flux": flux, "top12_moy_z": round(float(z[:12].mean()), 3),
                     "top12_d": round(float(d), 3),
                     "spearman_rho": round(float(rho), 3),
                     "spearman_p": float(p)})
    return df, rows


def around_threshold(df, pas):
    """Lecture autour d'un pas de seuil : fenêtres ±W, d de Cohen (après - avant)."""
    n = len(df)
    out = {}
    for flux in FLUXES:
        v = df[flux].to_numpy(float)
        lo = max(0, pas - W); hi = min(n, pas + W)
        before = v[lo:pas]; after = v[pas:hi]
        out[flux] = round(float(cohen_d(before, after)), 3) if len(before) >= 2 and len(after) >= 2 else None
    return out


def main():
    extr = {}
    for tag, (csv_name, d) in PAIRS.items():
        extr[tag] = extract(d)
        print(f"--- {tag} ({d}) ---")
        print(f"  version={extr[tag]['version']} n={extr[tag]['n']}")
        print(f"  cascade % : {extr[tag]['cascade_pct']}")
        print(f"  cascade pas : {extr[tag]['cascade_pas']}")
        print(f"  MC : score={extr[tag]['mc_score']} seuil={extr[tag]['mc_thr']} "
              f"métriques={extr[tag]['mc_metrics']}")
        print(f"  Delta={extr[tag]['delta']} L7a={extr[tag]['l7a_dir']} "
              f"conf={extr[tag]['l7a_conf']} status={extr[tag]['l7a_status']} L7b={extr[tag]['l7b']}")
        print(f"  falsification delta_vs_null={extr[tag]['fals']} status={extr[tag]['fals_status']} "
              f"régime={extr[tag]['regime']}")
        print(f"  bruit={extr[tag].get('bruit_verdict')} score_moyen={extr[tag].get('bruit_score_moyen')}")
        print(f"  F1 avant/après={extr[tag].get('f1_avant')}/{extr[tag].get('f1_apres')} "
              f"(ratio {extr[tag].get('f1_ratio')}) ; "
              f"F2 avant/après={extr[tag].get('f2_avant')}/{extr[tag].get('f2_apres')} "
              f"(ratio {extr[tag].get('f2_ratio')})")

    all_rows = []
    around = {}
    for tag, (csv_name, d) in PAIRS.items():
        df, rows = direct_tests(csv_name)
        for r in rows:
            r["série"] = tag
            all_rows.append(r)
        t0 = extr[tag]["cascade_pas"][2]
        if t0 is not None:
            around[tag] = around_threshold(df, t0)
            print(f"--- {tag} autour de T_0 (pas {t0}, ±{W}) : {around[tag]}")
    dt = pd.DataFrame(all_rows)
    dt.to_csv(os.path.join(PDAC, "mtap_direct_tests.csv"), index=False)
    print("\n--- Tests directs top-12 contre reste (d de Cohen ; + = plus haut chez les 12 plus délétées en MTAP) ---")
    print(dt.pivot(index="flux", columns="série", values="top12_d").to_string())
    print("\n--- Spearman flux vs rang ---")
    print(dt.pivot(index="flux", columns="série", values="spearman_rho").to_string())

    with open(os.path.join(PDAC, "mtap_extract.json"), "w", encoding="utf-8") as f:
        json.dump({"extraction": extr, "autour_T0": around,
                   "directs": all_rows}, f, indent=2, ensure_ascii=False)
    print("\nÉcrit : mtap_direct_tests.csv, mtap_extract.json")
    print(f"SHA script : {__import__('hashlib').sha256(open(__file__, 'rb').read()).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
