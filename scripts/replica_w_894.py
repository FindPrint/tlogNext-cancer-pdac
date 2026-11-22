#!/usr/bin/env python3
"""§8.94 A1 — Tier 2 (replique a w fixe), sonde de cadence + lot borne.
Generalisation de replica_delta_863.py (miroir EXACT du bloc run_pipeline
lignes 7075-7187 du pipeline v6.2, fonctions importees en lecture seule,
sans modification) : colonne de controle et liste de flux lues dans le
CSV et les metadonnees du run, pas codees en dur (MTAP).
CALIBRATION D'ABORD : reproduire le D_vector stocke (d_sat, d_crit,
d_div, d_null) a |Δ| < 1e-6 pour chaque CSV a son w propre. Si la
calibration echoue sur un CSV, le volet s'arrete pour ce CSV.
PUIS croisement w in {27, 30} sur les 8 paires principales V1 (§8.56) :
16 CSV x 2 w = 32 builds. Sortie : replica_w_894.json (+ log horodate).
Usage : python3 replica_w_894.py [--sonde] [--lot] [--cal-seule]
  --sonde : 1 seul build de calibration (MTAP s11111, w=27) + duree.
  --lot   : calibration 16 CSV + croisement 32 builds (systemd).
"""
import hashlib
import importlib.util
import json
import os
import sys
import time

import numpy as np
import pandas as pd

PDAC = os.path.dirname(os.path.abspath(__file__))
V62_PATH = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"

_spec = importlib.util.spec_from_file_location("v62", V62_PATH)
V62 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V62)

V1 = [
    ("HP35", "results_fast_v62_hp35", "results_fast_v62_hp35_nul"),
    ("TCGA_v4", "results_fast_v62_tcga_v4", "results_fast_v62_tcga_v4_nul"),
    ("GSE71729", "results_fast_v62_geo71729", "results_fast_v62_geo71729_nul"),
    ("GSE62452", "results_fast_v62_geo62452", "results_fast_v62_geo62452_nul"),
    ("ICGC", "results_fast_v62_icgc", "results_fast_v62_icgc_nul"),
    ("IMMUNE_TCGA", "results_fast_v62_immune_tcga", "results_fast_v62_immune_tcga_nul"),
    ("PARP_TCGA", "results_fast_v62_parp_tcga", "results_fast_v62_parp_tcga_nul"),
    ("DEPMAP", "results_fast_v62_depmap", "results_fast_v62_depmap_nul"),
]
# Dossiers v6.2 reels sous ~/workspace/runs/ (hors pdac-v6) : chemins absolus.
EXTRA_BASE = {
    "results_fast_v62_hp35": "/home/hatch/workspace/runs/biophysique-hp35/results_fast_v62_hp35",
}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mode_cfg_fast():
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


def run_dir(nom):
    p = os.path.join(PDAC, nom)
    if os.path.isdir(p):
        return p
    return os.path.join("/home/hatch/workspace/runs/biophysique-hp35", nom)


def meta_run(nom):
    j = json.load(open(os.path.join(run_dir(nom), "master_results.json")))
    cp = (j.get("metadata") or {}).get("csv_path")
    control = (j.get("metadata") or {}).get("control")
    bc = (j["run_pipeline"]["threshold_metadata"]
          ["threshold_optimization"]["best_config"])
    return cp, control, bc


def build_df_feat(csv_path, control_col, flux_cols, w_size):
    """Miroir de run_pipeline lignes 7075-7187 (branche mono-colonne,
    FULL_TRIANGULATION=False, n_est=1, boot=False en mode fast)."""
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.replace('"', "").str.replace("'", "")
    control_series = df[control_col].values.astype(float)
    fluxes = {c: df[c].values.astype(float) for c in flux_cols}
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


def dvec_stocke(nom):
    j = json.load(open(os.path.join(run_dir(nom), "master_results.json")))
    dv = j["holographic_tension_state"]["D_vector"]
    return {k: (None if dv.get(k) is None else float(dv[k]))
            for k in ("d_sat", "d_crit", "d_div", "d_null")}


def flux_cols_of(csv_path, control_col):
    df = pd.read_csv(csv_path, nrows=2)
    cols = [c.strip().strip('"').strip("'") for c in df.columns]
    return [c for c in cols if c != control_col]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--sonde"
    out_path = os.path.join(PDAC, "replica_w_894.json")
    out = {"mode": mode, "calibration": {}, "croisement": {},
           "ok_calibration": True, "durees_s": {}}
    if os.path.exists(out_path):
        out = json.load(open(out_path))
    if mode == "--sonde":
        # 1 build connu : MTAP s11111, w=27 (replique §8.63 : d_div 4,609748)
        csv = os.path.join(PDAC, "pdac_tcga_fluxes_v4_mtap_nul_s11111.csv")
        t0 = time.time()
        res = build_df_feat(csv, "MTAPCN",
                            ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2",
                             "KRT20", "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"], 27)
        dt = time.time() - t0
        stock = dvec_stocke("results_fast_v62_mtap_nul_s11111")
        ecarts = {k: abs(res[k] - stock[k]) for k in stock
                  if res[k] is not None and stock[k] is not None}
        print(f"[sonde] MTAP s11111 w=27 : d_div replique={res['d_div']:.6f} "
              f"stocke={stock['d_div']:.6f} ; Delta={res['delta']:.6f} ; "
              f"ecart max={max(ecarts.values()):.2e} ; duree={dt:.1f} s")
        out["sonde"] = {"duree_s": round(dt, 1), "ecart_max": float(max(ecarts.values())),
                        "d_div_replique": res["d_div"], "d_div_stocke": stock["d_div"],
                        "delta_replique": res["delta"]}
        with open(out_path, "w") as f:
            json.dump(out, f, indent=1, ensure_ascii=False, default=str)
        return 0
    # --lot : calibration 16 CSV a leur w propre, puis croisement w=27/30
    taches = []
    for nom_paire, dr, dn in V1:
        for cote, d in (("REEL", dr), ("NUL", dn)):
            taches.append((f"{nom_paire}_{cote}", d))
    for cle, d in taches:
        if out.get("calibration", {}).get(cle, {}).get("ok") is True:
            print(f"[cal {cle}] deja OK — saute", flush=True)
            continue
        cp, control, bc = meta_run(d)
        w_propre = int(bc["w_size"])
        flux_cols = flux_cols_of(cp, control)
        t0 = time.time()
        res = build_df_feat(cp, control, flux_cols, w_propre)
        dt = time.time() - t0
        stock = dvec_stocke(d)
        ecarts = {k: abs(res[k] - stock[k]) for k in stock
                  if res[k] is not None and stock[k] is not None}
        worst = max(ecarts.values()) if ecarts else float("nan")
        ok = worst < 1e-6
        out["calibration"][cle] = {"w_propre": w_propre, "duree_s": round(dt, 1),
                                   "ecart_max": float(worst), "ok": bool(ok),
                                   "d_div_replique": res["d_div"],
                                   "d_div_stocke": stock["d_div"],
                                   "delta_replique": res["delta"]}
        out["ok_calibration"] = bool(out["ok_calibration"] and ok)
        out["durees_s"][cle] = round(dt, 1)
        print(f"[cal {cle} w={w_propre}] ecart max={worst:.2e} "
              f"({'OK' if ok else 'ECHEC'}) duree={dt:.1f} s", flush=True)
        with open(out_path, "w") as f:
            json.dump(out, f, indent=1, ensure_ascii=False, default=str)
    if not out["ok_calibration"]:
        print("CALIBRATION ECHOUEE — croisement annule (protocole §8.94 A1).")
        return 1
    for nom_paire, dr, dn in V1:
        for cote, d in (("REEL", dr), ("NUL", dn)):
            cp, control, bc = meta_run(d)
            flux_cols = flux_cols_of(cp, control)
            for w in (27, 30):
                cle = f"{nom_paire}_{cote}_w{w}"
                if cle in out["croisement"]:
                    continue
                t0 = time.time()
                res = build_df_feat(cp, control, flux_cols, w)
                dt = time.time() - t0
                out["croisement"][cle] = {"w": w, "d_sat": res["d_sat"],
                                          "d_crit": res["d_crit"],
                                          "d_div": res["d_div"],
                                          "d_null": res["d_null"],
                                          "delta": res["delta"],
                                          "duree_s": round(dt, 1)}
                print(f"[x {cle}] d_sat={res['d_sat']:.4f} d_div={res['d_div']:.4f} "
                      f"Delta={res['delta']:.4f} ({dt:.1f} s)", flush=True)
                with open(out_path, "w") as f:
                    json.dump(out, f, indent=1, ensure_ascii=False, default=str)
    # Lecture : ecarts Delta reel-nul a w fixe, par paire
    lec = {}
    for nom_paire, dr, dn in V1:
        for w in (27, 30):
            r = out["croisement"][f"{nom_paire}_REEL_w{w}"]
            n = out["croisement"][f"{nom_paire}_NUL_w{w}"]
            lec[f"{nom_paire}_w{w}"] = {
                "delta_R": r["delta"], "delta_N": n["delta"],
                "ecart": r["delta"] - n["delta"],
                "abs_ecart_le_010": bool(abs(r["delta"] - n["delta"]) <= 0.10),
                "ecart_gt_007": bool((r["delta"] - n["delta"]) > 0.07)}
    for w in (27, 30):
        sous = [v for k, v in lec.items() if k.endswith(f"_w{w}")]
        lec[f"synthese_w{w}"] = {
            "n_paires": len(sous),
            "abs_ecart_le_010": f"{sum(1 for v in sous if v['abs_ecart_le_010'])}/{len(sous)}",
            "ecart_gt_007": f"{sum(1 for v in sous if v['ecart_gt_007'])}/{len(sous)}"}
    out["lecture"] = lec
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=str)
    print(f"synthese w27 : {lec['synthese_w27']} ; w30 : {lec['synthese_w30']}")
    print("ecrit: replica_w_894.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
