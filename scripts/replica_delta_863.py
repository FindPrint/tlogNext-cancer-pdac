#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.63 — Réplique Delta : séparer w de la permutation (M1b).
Miroir EXACT du bloc `run_pipeline` lignes 7075–7187 du pipeline v6.2
(scan_points, fenêtres triées par progression, séries concaténées par
flux, `apply_complexity` importée du pipeline) suivi de
`compute_holographic_tension_state` importée du pipeline. Seul paramètre
libre : w. Les fonctions du pipeline sont importées en lecture seule,
sans modification.
CALIBRATION D'ABORD : reproduire le D_vector stocké (d_sat, d_crit,
d_div, d_null) à |Δ| < 1e-6 pour 5 CSV à leur w propre. Si la calibration
échoue sur un CSV, le volet s'arrête pour ce CSV (protocole §2 C2).
PUIS croisement w ∈ {27, 30} × CSV ∈ {réel, s11111, s123} (+ w=42 sur
s11111 et s123 à titre de contrôle), avec médianes par estimateur.
Protocole gelé : PROTOCOL_mechanisms_863.md.
Sortie : replica_delta_863.json.
"""
import hashlib
import importlib.util
import json
import os

import numpy as np
import pandas as pd

PDAC = os.path.dirname(os.path.abspath(__file__))
V62_PATH = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
MTAP_FLUXES = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
               "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]
DIVERGENCE = ["LevinaBickel", "PCAIntrinsic", "LocalPCA", "GraphDimension",
              "PersistentHomology", "MFA"]
SATURATION = ["Higuchi", "Katz", "Petrosian", "Sevcik", "BoxCounting",
              "Hurst2mH", "DFA"]

_spec = importlib.util.spec_from_file_location("v62", V62_PATH)
V62 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V62)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mode_cfg_fast():
    """Reproduit la construction de mode_cfg de run_pipeline (lignes
    6664-6701) pour le mode fast, opt_cfg vide."""
    _param_modes = V62.PARAMETERS["modes"]
    modes = {}
    for _m, _p in _param_modes.items():
        modes[_m] = {
            "n_est": _p["n_bootstrap"],
            "n_bootstrap": _p["n_bootstrap"],
            "w_size": _p["w_size"],
            "test": _p["test"],
            "min_grp": _p["min_grp"],
            "min_len": _p["min_len"],
            "boot": _p["boot"],
            "window_scan": _p["window_scan"],
            "full_triangulation": V62.FULL_TRIANGULATION,
            "auto_optimize_threshold": bool(
                V62.PARAMETERS.get("mc_initial", {}).get(
                    "threshold_optimization_enabled",
                    _p["auto_optimize_threshold"])),
            "estimator_profile": _p.get("estimator_profile", "all"),
            "optimization_iterations": _p.get("optimization_iterations", 50),
            "max_workers": _p.get("max_workers", 1),
            "mc_complexity_enabled": bool(
                V62.PARAMETERS.get("mc_initial", {}).get(
                    "estimator_diagnostics_enabled",
                    V62.MC_COMPLEXITY_ENABLED)),
            "mc_complexity_max_scenarios": V62.PARAMETERS.get(
                "mc_initial", {}).get(
                "estimator_diagnostics_max_scenarios",
                _p.get("mc_complexity_max_scenarios",
                       V62.MC_COMPLEXITY_MAX_SCENARIOS)),
        }
    cfg = modes["fast"].copy()
    cfg.setdefault("random_seed", V62.RANDOM_SEED)
    return cfg


def build_df_feat(csv_path, w_size):
    """Miroir de run_pipeline lignes 7075-7187 (branche mono-colonne,
    FULL_TRIANGULATION=False, n_est=1, boot=False en mode fast)."""
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.replace('"', "").str.replace("'", "")
    control_col = "MTAPCN"
    control_series = df[control_col].values.astype(float)
    fluxes = {c: df[c].values.astype(float) for c in MTAP_FLUXES}
    fluxes_raw = {k: np.asarray(v, dtype=float).copy()
                  for k, v in fluxes.items()}
    mode_cfg = mode_cfg_fast()
    axis = V62._build_mc_progress_axis(control_series, fluxes_raw, mode_cfg)
    assert axis["status"] == "ok", axis["status"]
    progress = np.asarray(axis["progress_pct"], dtype=float)
    n_pts = len(progress)
    scan_points = np.linspace(progress.min(), progress.max(), 120)
    w_size = max(2, min(w_size, n_pts // 2))
    tol = max(3.0, (scan_points[1] - scan_points[0]) / 2.0)
    sort_idx = np.argsort(progress)
    prog_sorted = progress[sort_idx]
    flux_sorted = {k: v[sort_idx] for k, v in fluxes.items()}
    window_data = []
    for i in range(n_pts - w_size + 1):
        window_data.append({
            "progress": float(np.mean(prog_sorted[i:i + w_size])),
            "fluxes": {k: flux_sorted[k][i:i + w_size]
                       for k in fluxes.keys()},
        })
    rows = []
    for P in scan_points:
        matching = [wd for wd in window_data
                    if abs(wd["progress"] - P) <= tol]
        if not matching:
            matching = [min(window_data,
                            key=lambda wd: abs(wd["progress"] - P))]
        row = {"Progress": float(P), "N_cohorts": len(matching)}
        mode_cfg_dynamic = mode_cfg.copy()
        mode_cfg_dynamic["min_len"] = max(10, w_size // 2)
        for flux in fluxes.keys():
            combined = np.concatenate(
                [wd["fluxes"][flux] for wd in matching])
            ests = V62.apply_complexity(
                combined, flux_name=flux, mode_cfg=mode_cfg_dynamic)
            for k, v in ests.items():
                row[f"{flux}_{k}_mean"] = (float(v) if not np.isnan(v)
                                           else None)
                row[f"{flux}_{k}_std"] = 0.0
        rows.append(row)
    df_feat = pd.DataFrame(rows)
    state = V62.compute_holographic_tension_state(
        df_feat, None, n_samples=len(df), control_col=control_col,
        triangulation_estimators=None)
    dv = state["D_vector"]
    per = state.get("per_estimator", {}) or {}
    return {
        "d_sat": float(dv["d_sat"]) if dv.get("d_sat") is not None else None,
        "d_crit": float(dv["d_crit"]) if dv.get("d_crit") is not None else None,
        "d_div": float(dv["d_div"]) if dv.get("d_div") is not None else None,
        "d_null": float(dv["d_null"]) if dv.get("d_null") is not None else None,
        "delta": (float(state["Delta_tension"])
                  if state.get("Delta_tension") is not None else None),
        "per_estimator": {k: (None if v.get("raw_median") is None
                              else float(v["raw_median"]))
                          for k, v in per.items()},
        "n_rows_df_feat": int(len(df_feat)),
    }


def dvec_stocke(dossier):
    j = json.load(open(os.path.join(
        PDAC, dossier, "master_results.json")))
    dv = j["holographic_tension_state"]["D_vector"]
    return {k: (None if dv.get(k) is None else float(dv[k]))
            for k in ("d_sat", "d_crit", "d_div", "d_null")}


def main():
    out = {"calibration": {}, "croisement": {}, "ok_calibration": True}
    cal_cases = [
        ("reel", "pdac_tcga_fluxes_v4_mtap.csv",
         "results_fast_v62_mtap", 30),
        ("s11111", "pdac_tcga_fluxes_v4_mtap_nul_s11111.csv",
         "results_fast_v62_mtap_nul_s11111", 27),
        ("s123", "pdac_tcga_fluxes_v4_mtap_nul_s123.csv",
         "results_fast_v62_mtap_nul_s123", 27),
        ("nul42", "pdac_tcga_fluxes_v4_mtap_nul.csv",
         "results_fast_v62_mtap_nul", 42),
        ("s1011", "pdac_tcga_fluxes_v4_mtap_nul_s1011.csv",
         "results_fast_v62_mtap_nul_s1011", 30),
    ]
    for nom, csv, dossier, w in cal_cases:
        res = build_df_feat(os.path.join(PDAC, csv), w)
        stock = dvec_stocke(dossier)
        ecarts = {k: abs(res[k] - stock[k]) for k in stock
                  if res[k] is not None and stock[k] is not None}
        worst = max(ecarts.values())
        ok = worst < 1e-6
        out["calibration"][nom] = {
            "w_propre": w, "replique": {k: res[k] for k in
                                        ("d_sat", "d_crit", "d_div",
                                         "d_null", "delta")},
            "stocke": stock, "ecart_max": float(worst), "ok": bool(ok)}
        out["ok_calibration"] &= ok
        print(f"[Delta-cal {nom} w={w}] réplique d_div={res['d_div']:.6f} "
              f"stocké={stock['d_div']:.6f} ; Delta réplique={res['delta']:.6f} ; "
              f"écart max={worst:.2e} -> {'OK' if ok else 'ÉCHEC'}",
              flush=True)
    print(f"[Delta-cal] globale : "
          f"{'OK' if out['ok_calibration'] else 'ÉCHEC'}")
    if not out["ok_calibration"]:
        print("CALIBRATION ÉCHOUÉE — volet Delta arrêté (protocole §2 C2).")
        with open(os.path.join(PDAC, "replica_delta_863.json"), "w") as f:
            json.dump(out, f, indent=1, ensure_ascii=False, default=str)
        return out
    # ---- croisement w x CSV
    for nom, csv in (("reel", "pdac_tcga_fluxes_v4_mtap.csv"),
                     ("s11111", "pdac_tcga_fluxes_v4_mtap_nul_s11111.csv"),
                     ("s123", "pdac_tcga_fluxes_v4_mtap_nul_s123.csv")):
        for w in (27, 30):
            res = build_df_feat(os.path.join(PDAC, csv), w)
            out["croisement"][f"{nom}_w{w}"] = {
                "csv": csv, "w": w, "d_sat": res["d_sat"],
                "d_crit": res["d_crit"], "d_div": res["d_div"],
                "d_null": res["d_null"], "delta": res["delta"],
                "per_estimator": res["per_estimator"]}
            print(f"[Delta-x {nom} w={w}] d_sat={res['d_sat']:.4f} "
                  f"d_div={res['d_div']:.4f} Delta={res['delta']:.4f}",
                  flush=True)
    for nom, csv in (("s11111", "pdac_tcga_fluxes_v4_mtap_nul_s11111.csv"),
                     ("s123", "pdac_tcga_fluxes_v4_mtap_nul_s123.csv")):
        res = build_df_feat(os.path.join(PDAC, csv), 42)
        out["croisement"][f"{nom}_w42"] = {
            "csv": csv, "w": 42, "d_sat": res["d_sat"],
            "d_crit": res["d_crit"], "d_div": res["d_div"],
            "d_null": res["d_null"], "delta": res["delta"],
            "per_estimator": res["per_estimator"]}
        print(f"[Delta-x {nom} w=42] d_sat={res['d_sat']:.4f} "
              f"d_div={res['d_div']:.4f} Delta={res['delta']:.4f}",
              flush=True)
    # ---- partage w / permutation (Delta)
    cr = out["croisement"]
    ecart_csv_w30 = cr["s11111_w30"]["delta"] - cr["reel_w30"]["delta"]
    ecart_csv_w27 = cr["s11111_w27"]["delta"] - cr["reel_w27"]["delta"]
    ecart_w_reel = cr["reel_w27"]["delta"] - cr["reel_w30"]["delta"]
    ecart_w_s11111 = cr["s11111_w27"]["delta"] - cr["s11111_w30"]["delta"]
    ecart_w_s123 = cr["s123_w27"]["delta"] - cr["s123_w30"]["delta"]
    out["partage"] = {
        "ecart_delta_s11111_moins_reel_a_w30": round(ecart_csv_w30, 4),
        "ecart_delta_s11111_moins_reel_a_w27": round(ecart_csv_w27, 4),
        "ecart_delta_w27_moins_w30_reel": round(ecart_w_reel, 4),
        "ecart_delta_w27_moins_w30_s11111": round(ecart_w_s11111, 4),
        "ecart_delta_w27_moins_w30_s123": round(ecart_w_s123, 4),
        "ratio_w_sur_csv_s11111": (None if ecart_csv_w30 == 0 else
                                   round(abs(ecart_w_s11111
                                             / ecart_csv_w30), 4)),
    }
    print(f"[Delta-partage] écart CSV à w=30 : {ecart_csv_w30:.4f} ; "
          f"à w=27 : {ecart_csv_w27:.4f} ; effet w : réel {ecart_w_reel:.4f}, "
          f"s11111 {ecart_w_s11111:.4f}, s123 {ecart_w_s123:.4f}")
    # ---- porteurs de d_div : écarts par estimateur, à w fixé (30)
    reel_pe = cr["reel_w30"]["per_estimator"]
    for nom in ("s11111", "s123"):
        pe = cr[f"{nom}_w30"]["per_estimator"]
        ec = {e: round(pe[e] - reel_pe[e], 4) for e in DIVERGENCE
              if pe.get(e) is not None and reel_pe.get(e) is not None}
        print(f"[Delta-porteurs] écarts {nom} − réel à w=30 "
              f"(divergence) : {ec}")
        out["croisement"][f"{nom}_w30"]["ecarts_divergence_vs_reel_w30"] = ec
    with open(os.path.join(PDAC, "replica_delta_863.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=str)
    print("SHA script : " + sha(__file__))
    print("écrit: replica_delta_863.json")
    return out


if __name__ == "__main__":
    main()
