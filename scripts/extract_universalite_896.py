#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.96 — Universalité (LUAD + BRCA) : lecture seule des 8 runs v6.2.
Reprend la logique de lecture de mtap_consolidation_850.py (read_run) :
S_sep = max_separation x stabilite ; MC recompose
0,3*s_norm + 0,3*stabilite + 0,2*robustesse + 0,2*acuite.
Ajouts : medians Q1-Q6 (scores.json, sur toutes les entrees flux x
estimateur), resume des 4 tests de bruit (estimator_four_tests.csv),
diagnostic de bruit (noise_diagnostic.json), L7b (rapport texte).
LECTURE SEULE : aucun run, aucune donnee re-telechargee, aucun CSV
reconstruit. Sorties : universalite_896_table.json / .csv.
"""
import ast
import csv
import hashlib
import json
import os
import statistics

PDAC = os.path.dirname(os.path.abspath(__file__))

RUNS = {
    "LUAD_REEL": "results_fast_v62_896_luad",
    "LUAD_NUL42": "results_fast_v62_896_luad_nul",
    "LUAD_NUL_S9601": "results_fast_v62_896_luad_nul_s9601",
    "LUAD_NUL_S9602": "results_fast_v62_896_luad_nul_s9602",
    "BRCA_REEL": "results_fast_v62_896_brca",
    "BRCA_NUL42": "results_fast_v62_896_brca_nul",
    "BRCA_NUL_S9601": "results_fast_v62_896_brca_nul_s9601",
    "BRCA_NUL_S9602": "results_fast_v62_896_brca_nul_s9602",
}
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


def med(vals):
    import math
    v = [x for x in vals if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return statistics.median(v) if v else None


def read_run(d):
    r = json.load(open(os.path.join(PDAC, d, "master_results.json")))
    tm = g(r, "run_pipeline.threshold_metadata.threshold_optimization", {}) or {}
    bc = tm.get("best_config", {}) or {}
    m = bc.get("metrics", {}) or {}
    l7 = g(r, "prediction_levels.L7a_coherence", {}) or {}
    l7b = g(r, "prediction_levels.L7b_robustesse", {}) or {}
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
    except Exception as e:  # noqa: BLE001
        print(f"  !! default_scan_curve illisible pour {d} : {e}")
        dc, ds, dn = None, None, None
    # Q1-Q6 : mediane sur toutes les entrees flux x estimateur de scores.json
    sc_json = json.load(open(os.path.join(PDAC, d, "scores.json")))
    qmed = {}
    for q in ["Q1_Calme_vs_Chaos", "Q2_Tension_Seuil", "Q3_Agressivite",
              "Q4_Persistence", "Q5_Actif_Receptif", "Q6_Actif_Receptif_Echelle"]:
        vals = [fnum(v) for v in (sc_json.get(q) or {}).values()]
        qmed[q] = med(vals)
        qmed[q + "_n"] = len([x for x in vals if x is not None])
    # 4 tests de bruit : resumes sur estimator_four_tests.csv
    ft = {"n_rows": 0}
    with open(os.path.join(PDAC, d, "estimator_four_tests.csv"), newline="") as f:
        rows = list(csv.DictReader(f))
    ft["n_rows"] = len(rows)
    for step, col in [("step1", "step1_candidate_to_white_ratio"),
                      ("step2", "step2_delta_corr"),
                      ("step3", "step3_hurst_mean"),
                      ("step4", "step4_delta_slope")]:
        ft[step + "_computed"] = sum(1 for r_ in rows if r_.get(step + "_status") == "computed")
        ft[step + "_median"] = med([fnum(r_.get(col)) for r_ in rows])
    nd = json.load(open(os.path.join(PDAC, d, "noise_diagnostic.json")))
    txt = open(os.path.join(PDAC, d, "universal_master_report.txt"),
               encoding="utf-8", errors="replace").read()
    l7b_lines = [ln.strip() for ln in txt.splitlines()
                 if ln.strip().startswith(("L7b-ROBUSTESSE", "L7b check"))]
    return {
        "dir": d, "version": r.get("version"),
        "n": fnum(g(r, "reading_synthesis.n_samples")),
        "cascade_pct": casc,
        "max_F1_velocity": fnum(g(r, "five_threshold_cascade.max_F1_velocity")),
        "max_F2_curvature": fnum(g(r, "five_threshold_cascade.max_F2_curvature")),
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
        "dominant_regime": g(r, "reading_synthesis.dominant_regime"),
        "l7a_dir": l7.get("consensus_direction"),
        "l7a_conf": fnum(l7.get("global_confidence")),
        "l7b": l7b,
        "l7b_lines": l7b_lines,
        "fals": fnum(g(holo, "falsification_vs_null.delta_vs_null")),
        "fals_significant": g(holo, "falsification_vs_null.is_significant_nonlinearity"),
        "default_thr": dc, "default_maxsep": ds, "default_n_scored": dn,
        "q_median": qmed,
        "four_tests": ft,
        "noise_diag": {"avg": fnum(nd.get("avg_variance_proxy_score")),
                       "max": fnum(nd.get("max_variance_proxy_score")),
                       "min": fnum(nd.get("min_variance_proxy_score")),
                       "label": nd.get("diagnostic_label"),
                       "verdict": nd.get("verdict_level"),
                       "noise_col": nd.get("noise_col")},
        "master_sha": sha(os.path.join(PDAC, d, "master_results.json")),
    }


def main():
    rows = {}
    for name, d in RUNS.items():
        rows[name] = read_run(d)
        e = rows[name]
        print(f"{name:16s} maxsep={e['maxsep']:.4f} S_sep={e['ssep']:.4f} "
              f"MC={e['mc_score']:.4f} (recomp ecart {e['mc_ecart_recomp']:.2e}) "
              f"Delta={e['delta']:.4f} L7a={e['l7a_dir']} {e['l7a_conf']:.4f} "
              f"fals={e['fals']:.4f} F1={e['max_F1_velocity']:.4f} F2={e['max_F2_curvature']:.4f}")
    # Ecarts reel-nul par bras (barre gelee : maxsep > 0,07 + 1 autre indicateur)
    for reel, nul42, fresh in [("LUAD_REEL", "LUAD_NUL42", ["LUAD_NUL_S9601", "LUAD_NUL_S9602"]),
                               ("BRCA_REEL", "BRCA_NUL42", ["BRCA_NUL_S9601", "BRCA_NUL_S9602"])]:
        r_, n_ = rows[reel], rows[nul42]
        print(f"{reel} vs {nul42}: d_maxsep={r_['maxsep']-n_['maxsep']:+.4f} "
              f"d_S_sep={r_['ssep']-n_['ssep']:+.4f} d_MC={r_['mc_score']-n_['mc_score']:+.4f} "
              f"d_Delta={r_['delta']-n_['delta']:+.4f} d_fals={r_['fals']-n_['fals']:+.4f} "
              f"L7a {r_['l7a_dir']} {r_['l7a_conf']:.4f} vs {n_['l7a_dir']} {n_['l7a_conf']:.4f}")
        for f in fresh:
            print(f"  vs {f}: d_maxsep={r_['maxsep']-rows[f]['maxsep']:+.4f} "
                  f"d_MC={r_['mc_score']-rows[f]['mc_score']:+.4f} "
                  f"d_Delta={r_['delta']-rows[f]['delta']:+.4f}")
    files_sha = {}
    for p in ["PROTOCOL_universalite_896.md", "PROVENANCE_896.md",
              "ADDENDUM_correction_20261121_896.md", "ADDENDUM_axe_brca_896.md",
              "brca_896_download.json", "luad_896_nulls_files.json",
              "build_fluxes_brca_896.py", "build_luad_nulls_896.py",
              "pdac_luad_fluxes.csv", "pdac_luad_fluxes_nul.csv",
              "pdac_luad_fluxes_nul_s9601.csv", "pdac_luad_fluxes_nul_s9602.csv",
              "pdac_brca_fluxes.csv", "pdac_brca_fluxes_nul.csv",
              "pdac_brca_fluxes_nul_s9601.csv", "pdac_brca_fluxes_nul_s9602.csv",
              "../biophysique-hp35/universal_v6.2.0_cohen.py"]:
        pp = os.path.join(os.path.dirname(PDAC), p) if p.startswith("runs/") else os.path.join(PDAC, p)
        files_sha[p] = sha(pp) if os.path.exists(pp) else "ABSENT"
    out = {"runs": rows, "floor": FLOOR,
           "gaps": {}, "files_sha": files_sha,
           "script_sha": sha(__file__)}
    for reel, nul42, fresh in [("LUAD_REEL", "LUAD_NUL42", ["LUAD_NUL_S9601", "LUAD_NUL_S9602"]),
                               ("BRCA_REEL", "BRCA_NUL42", ["BRCA_NUL_S9601", "BRCA_NUL_S9602"])]:
        r_ = rows[reel]
        out["gaps"][reel] = {n: {"d_maxsep": r_["maxsep"] - rows[n]["maxsep"],
                                 "d_ssep": r_["ssep"] - rows[n]["ssep"],
                                 "d_mc": r_["mc_score"] - rows[n]["mc_score"],
                                 "d_delta": r_["delta"] - rows[n]["delta"],
                                 "d_fals": r_["fals"] - rows[n]["fals"]}
                            for n in [nul42] + fresh}
    with open(os.path.join(PDAC, "universalite_896_table.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=str)
    with open(os.path.join(PDAC, "universalite_896_table.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["run", "dir", "n", "maxsep", "stabilite", "ssep", "mc_score",
                    "mc_recomp", "ecart_recomp", "delta", "l7a_dir", "l7a_conf",
                    "falsification", "fals_significant", "cascade_T-2", "cascade_T-1",
                    "cascade_T0", "cascade_T+1", "cascade_T+2",
                    "max_F1_velocity", "max_F2_curvature",
                    "Q1_med", "Q2_med", "Q3_med", "Q4_med", "Q5_med", "Q6_med",
                    "ft_n_rows", "ft_s1_ratio_med", "ft_s2_dcorr_med",
                    "ft_s3_hurst_med", "ft_s4_dslope_med",
                    "noise_avg", "noise_max", "noise_min", "noise_label",
                    "master_sha"])
        for name in RUNS:
            e = rows[name]
            q = e["q_median"]; ft = e["four_tests"]; nd = e["noise_diag"]
            w.writerow([name, e["dir"], e["n"], e["maxsep"], e["stability"], e["ssep"],
                        e["mc_score"], e["mc_recomp"], e["mc_ecart_recomp"], e["delta"],
                        e["l7a_dir"], e["l7a_conf"], e["fals"], e["fals_significant"]]
                       + e["cascade_pct"] + [e["max_F1_velocity"], e["max_F2_curvature"],
                        q["Q1_Calme_vs_Chaos"], q["Q2_Tension_Seuil"], q["Q3_Agressivite"],
                        q["Q4_Persistence"], q["Q5_Actif_Receptif"], q["Q6_Actif_Receptif_Echelle"],
                        ft["n_rows"], ft["step1_median"], ft["step2_median"],
                        ft["step3_median"], ft["step4_median"],
                        nd["avg"], nd["max"], nd["min"], nd["label"], e["master_sha"]])
    print("SHA script : " + sha(__file__))
    print("SHA table json : " + sha(os.path.join(PDAC, "universalite_896_table.json")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
