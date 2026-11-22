#!/usr/bin/env python3
"""§8.93 — Chaque paire jugee contre une distribution de nuls.
(PROTOCOL_nulls_distribution_893.md). Reutilise la machinerie calibree
de replica_nulls_n70_853.py / replica_scan_847.py (fonctions DU PIPELINE,
import en lecture seule, aucune modification) : `_build_mc_progress_axis`
+ `scan_critical_threshold` + `evaluate_scan_quality`.
CALIBRATION D'ABORD : reproduire maxsep des 30 runs v6.2 existants
(15 paires x reel + nul graine 42) a ±0,001, courbe comprise — sinon
arret et diagnostic (protocole §3a, comme §8.47 §9).
PUIS, par paire, sous les DEUX configs fixes (config reelle et config
nulle du run v6.2 existant) : 1000 permutations par ligne, graine
maitresse default_rng(20261121) (NOUVELLE, distincte de §8.47 et §8.53).
Chaque tirage donne maxsep, stabilite, S_sep = maxsep x stab, et MC
(composite recalcule depuis les metriques du tirage, meme code que le
pipeline : 0,3*s_norm + 0,3*stab + 0,2*rob + 0,2*sharp, x0,8 si
w < n//10). Les 1000 valeurs brutes par (paire, config) sont conservees
integralement (JSON + CSV). Reprise possible : les (paire, config)
deja completes dans le CSV brut sont sautees.
Lecture gelee (§4) : rang du reel (/1001), p95 des nuls, mediane,
% de nuls sous le plancher (ecart > 0,07) ; SOLIDE / FRAGILE / NON ;
A2 recalcule (SOLIDE seulement). Config nulle en sensibilite.
Usage : python3 replica_nulls_893.py [--sonde] [--lot]
  --sonde : calibration sur 1 paire (TCGA v4) + 10 tirages chronometres.
  --lot   : calibration 30 runs + 30 000 tirages (systemd).
Sorties : nulls_dist_893_verify.json, nulls_dist_893_replica.json,
nulls_dist_893_replica_raw.csv, nulls_dist_893_table.json.
"""
import importlib.util
import json
import os
import sys
import time

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
N_TIRAGES = 1000
MASTER_SEED = 20261121
GRAINES_FRAICHES = list(range(9101, 9111))

PAIRS = [
    ("HP35", "results_fast_v62_hp35", "results_fast_v62_hp35_nul", 1),
    ("TCGA_v4", "results_fast_v62_tcga_v4", "results_fast_v62_tcga_v4_nul", 1),
    ("GSE71729", "results_fast_v62_geo71729", "results_fast_v62_geo71729_nul", 1),
    ("GSE62452", "results_fast_v62_geo62452", "results_fast_v62_geo62452_nul", 1),
    ("ICGC", "results_fast_v62_icgc", "results_fast_v62_icgc_nul", 1),
    ("IMMUNE_TCGA", "results_fast_v62_immune_tcga", "results_fast_v62_immune_tcga_nul", 1),
    ("PARP_TCGA", "results_fast_v62_parp_tcga", "results_fast_v62_parp_tcga_nul", 1),
    ("DEPMAP", "results_fast_v62_depmap", "results_fast_v62_depmap_nul", 1),
    ("GSE21501", "results_fast_v62_869_geo21501", "results_fast_v62_869_geo21501_nul", 2),
    ("GSE79668", "results_fast_v62_870_geo79668", "results_fast_v62_870_geo79668_nul", 2),
    ("GSE60979", "results_fast_v62_871_geo60979", "results_fast_v62_871_geo60979_nul", 2),
    ("GSE131050_YehFF", "results_fast_v62_874_yeh_ff", "results_fast_v62_874_yeh_ff_nul", 2),
    ("GSE57495", "results_fast_v62_879_geo57495", "results_fast_v62_879_geo57495_nul", 2),
    ("GDC_ORGANOID", "results_fast_v62_885_gdc_organoid", "results_fast_v62_885_gdc_organoid_nul", 2),
    ("GSE194249", "results_fast_v62_888_gse194249", "results_fast_v62_888_gse194249_nul", 2),
]

_spec = importlib.util.spec_from_file_location(
    "v62", "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py")
V62 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V62)
MODE_CFG = V62.PARAMETERS["modes"]["fast"].copy()
MODE_CFG.setdefault("random_seed", V62.RANDOM_SEED)


def sha(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def progress_axis(n):
    control = np.arange(n, dtype=float)
    axis = V62._build_mc_progress_axis(control, {}, MODE_CFG)
    assert axis["status"] == "ok", axis["status"]
    return np.asarray(axis["progress_pct"], dtype=float)


def scan_replica(flux_matrix, cols, progress, w_size, min_grp, n_candidates):
    fluxes = {k: flux_matrix[:, j].astype(float)
              for j, k in enumerate(cols)}
    thr, curve = V62.scan_critical_threshold(
        fluxes, progress, MODE_CFG, n_candidates, None, w_size, min_grp)
    m = V62.evaluate_scan_quality(curve, thr, w_size, len(progress))
    mc = (0.3 * float(m["s_norm"]) + 0.3 * float(m["stability"])
          + 0.2 * float(m["robustness"]) + 0.2 * float(m["sharpness"]))
    if w_size < len(progress) // 10:
        mc *= 0.8
    return (float(thr) if thr is not None and np.isfinite(thr) else np.nan,
            curve, float(m["max_separation"]), float(m["stability"]),
            float(mc), float(m["robustness"]))


def read_best_config(nom_dir):
    j = json.load(open(os.path.join(PDAC, nom_dir, "master_results.json")))
    bc = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
    l7a = j["prediction_levels"]["L7a_coherence"]
    conf = float(l7a["global_confidence"])
    direc = str(l7a["consensus_direction"]).lower()
    l7a_signed = conf if direc == "up" else (-conf if direc == "down" else 0.0)
    return {"w_size": int(bc["w_size"]), "min_grp": int(bc["min_grp"]),
            "n_candidates": int(bc["n_candidates"]),
            "maxsep_pipeline": float(bc["metrics"]["max_separation"]),
            "stab_pipeline": float(bc["metrics"]["stability"]),
            "mc_pipeline": float(bc["score"]),
            "rob_pipeline": float(bc["metrics"]["robustness"]),
            "l7a_pipeline": l7a_signed,
            "thr_pipeline": float(bc["threshold"]),
            "scan_curve_pipeline": j["run_pipeline"]["scan_curve"],
            "csv_path": (j.get("metadata") or {}).get("csv_path"),
            "control": (j.get("metadata") or {}).get("control"),
            "n": int(j["reading_synthesis"]["n_samples"]),
            "delta_pipeline": (None if (j.get("reading_synthesis") or {}).get("Delta_tension") is None
                               else float((j.get("reading_synthesis") or {}).get("Delta_tension")))}


def dist_stats(vals):
    v = np.asarray(vals, dtype=float)
    q = lambda p: float(np.quantile(v, p))
    return {"n": int(len(v)), "mediane": round(float(np.median(v)), 4),
            "moyenne": round(float(np.mean(v)), 4),
            "ecart_type": round(float(np.std(v, ddof=1)), 4),
            "p5": q(0.05), "p25": q(0.25), "p75": q(0.75),
            "p95": q(0.95), "p97.5": q(0.975), "p2.5": q(0.025),
            "iqr": round(q(0.75) - q(0.25), 4),
            "min": round(float(v.min()), 4), "max": round(float(v.max()), 4)}


def flux_cols(csv_path, control):
    df = pd.read_csv(csv_path, nrows=2)
    cols = [c.strip().strip('"').strip("'") for c in df.columns]
    return [c for c in cols if c != control]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--sonde"
    out = {"calibration": {}, "calibration_ok": None, "distributions": {},
           "reels": {}, "table": {}, "A2_distrib": {}}
    verify_path = os.path.join(PDAC, "nulls_dist_893_verify.json")
    if mode == "--sonde":
        # Calibration TCGA v4 (reel + nul) + 10 tirages chronometres, config reelle.
        nom, dr, dn, _ = PAIRS[1]
        for side, d in (("reel", dr), ("nul42", dn)):
            cfg = read_best_config(d)
            df = pd.read_csv(cfg["csv_path"])
            cols = flux_cols(cfg["csv_path"], cfg["control"])
            mat = df[cols].values.astype(float)
            prog = progress_axis(len(mat))
            t0 = time.time()
            thr, curve, maxsep, stab, mc, rob = scan_replica(
                mat, cols, prog, cfg["w_size"], cfg["min_grp"], cfg["n_candidates"])
            dt = time.time() - t0
            print(f"[sonde-cal {nom} {side}] maxsep replique={maxsep:.4f} "
                  f"pipeline={cfg['maxsep_pipeline']:.4f} "
                  f"ecart={abs(maxsep - cfg['maxsep_pipeline']):.2e} "
                  f"MC replique={mc:.4f} pipeline={cfg['mc_pipeline']:.4f} "
                  f"duree 1 scan={dt:.2f} s", flush=True)
            out["calibration"][f"{nom}_{side}"] = {
                "maxsep_replique": maxsep, "maxsep_pipeline": cfg["maxsep_pipeline"],
                "ecart_maxsep": abs(maxsep - cfg["maxsep_pipeline"]),
                "mc_replique": mc, "mc_pipeline": cfg["mc_pipeline"],
                "duree_1_scan_s": round(dt, 2)}
        # 10 tirages
        cfg = read_best_config(dr)
        df = pd.read_csv(cfg["csv_path"])
        cols = flux_cols(cfg["csv_path"], cfg["control"])
        mat = df[cols].values.astype(float)
        prog = progress_axis(len(mat))
        rng = np.random.default_rng(MASTER_SEED)
        t0 = time.time()
        for i in range(10):
            seed = int(rng.integers(2000, 10_000_000))
            r2 = np.random.default_rng(seed)
            perm = r2.permutation(len(mat))
            scan_replica(mat[perm], cols, prog, cfg["w_size"], cfg["min_grp"],
                         cfg["n_candidates"])
        dt = (time.time() - t0) / 10
        print(f"[sonde] 10 tirages TCGA v4 config reelle : {dt:.2f} s/tirage ; "
              f"estimation 30 000 tirages : {dt * 30000 / 3600:.2f} h", flush=True)
        out["sonde"] = {"s_par_tirage": round(dt, 3),
                        "estimation_30000_tirages_h": round(dt * 30000 / 3600, 2)}
        with open(verify_path, "w") as f:
            json.dump(out, f, indent=1, ensure_ascii=False)
        print("ecrit: nulls_dist_893_verify.json (sonde)")
        return 0

    # ---------------- LOT ----------------
    print("=== CALIBRATION (30 runs) ===", flush=True)
    cal_ok = True
    cfgs = {}
    for nom, dr, dn, _ in PAIRS:
        for side, d in (("reel", dr), ("nul42", dn)):
            cfg = read_best_config(d)
            cfgs[(nom, side)] = cfg
            df = pd.read_csv(cfg["csv_path"])
            cols = flux_cols(cfg["csv_path"], cfg["control"])
            mat = df[cols].values.astype(float)
            prog = progress_axis(len(mat))
            thr, curve, maxsep, stab, mc, rob = scan_replica(
                mat, cols, prog, cfg["w_size"], cfg["min_grp"], cfg["n_candidates"])
            d_max = abs(maxsep - cfg["maxsep_pipeline"])
            d_stab = abs(stab - cfg["stab_pipeline"])
            pc = cfg["scan_curve_pipeline"]
            curve_ok = len(curve) == len(pc)
            max_curve_diff = 0.0
            if curve_ok:
                for a, b in zip(curve, pc):
                    if abs(a["candidate"] - b["candidate"]) > 1e-6:
                        curve_ok = False
                        break
                    if (a["score"] is None) != (b["score"] is None):
                        curve_ok = False
                        break
                    if a["score"] is not None:
                        max_curve_diff = max(max_curve_diff, abs(a["score"] - b["score"]))
            ok = d_max <= 0.001 and d_stab <= 0.001 and curve_ok and max_curve_diff <= 0.001
            cal_ok &= ok
            out["calibration"][f"{nom}_{side}"] = {
                "maxsep_replique": round(maxsep, 6),
                "maxsep_pipeline": round(cfg["maxsep_pipeline"], 6),
                "ecart_maxsep": round(float(d_max), 8),
                "mc_replique": round(mc, 6), "mc_pipeline": round(cfg["mc_pipeline"], 6),
                "ecart_mc": round(abs(mc - cfg["mc_pipeline"]), 8),
                "courbe_identique": bool(curve_ok),
                "ecart_max_courbe": round(float(max_curve_diff), 8),
                "ok": bool(ok)}
            print(f"[{nom} {side}] maxsep ecart={d_max:.2e} MC ecart={abs(mc - cfg['mc_pipeline']):.2e} "
                  f"courbe_ok={curve_ok} -> {'OK' if ok else 'ÉCHEC'}", flush=True)
    out["calibration_ok"] = bool(cal_ok)
    with open(verify_path, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"Calibration globale : {'OK' if cal_ok else 'ÉCHEC'}", flush=True)
    if not cal_ok:
        print("CALIBRATION ÉCHOUÉE — arrêt, la réplique est rejetée (protocole §3a).", flush=True)
        return 1

    # Reprise : (paire, config) deja completes dans le CSV brut ?
    raw_path = os.path.join(PDAC, "nulls_dist_893_replica_raw.csv")
    faits = set()
    if os.path.exists(raw_path):
        raw_old = pd.read_csv(raw_path)
        for (pa, cf), g in raw_old.groupby(["paire", "config"]):
            if len(g) >= N_TIRAGES:
                faits.add((pa, cf))
        print(f"Reprise : {len(faits)} (paire, config) deja completes.", flush=True)
    else:
        raw_old = pd.DataFrame(columns=["paire", "config", "tirage", "maxsep",
                                        "stab", "ssep", "mc", "rob"])
    raw_rows = raw_old.to_dict("records") if len(raw_old) else []

    print(f"=== DISTRIBUTIONS NULLES ({N_TIRAGES} permutations par ligne x 15 paires x 2 configs) ===", flush=True)
    rng_master = np.random.default_rng(MASTER_SEED)
    for nom, dr, dn, _ in PAIRS:
        cfg_r = cfgs[(nom, "reel")]
        cfg_n = cfgs[(nom, "nul42")]
        df = pd.read_csv(cfg_r["csv_path"])
        cols = flux_cols(cfg_r["csv_path"], cfg_r["control"])
        mat = df[cols].values.astype(float)
        prog = progress_axis(len(mat))
        # Reels sous les deux configs + nul42 sous config nulle (references)
        reel = {}
        for cfg_nom, cfg in (("config_reelle", cfg_r), ("config_nulle", cfg_n)):
            _, _, ms, stab, mc, rob = scan_replica(
                mat, cols, prog, cfg["w_size"], cfg["min_grp"], cfg["n_candidates"])
            reel[cfg_nom] = {"maxsep": round(ms, 4), "stab": round(stab, 4),
                             "ssep": round(ms * stab, 4), "mc": round(mc, 4),
                             "rob": round(rob, 4)}
        df_n42 = pd.read_csv(cfg_n["csv_path"])
        mat_n42 = df_n42[cols].values.astype(float)
        _, _, ms_n42, stab_n42, mc_n42, rob_n42 = scan_replica(
            mat_n42, cols, prog, cfg_n["w_size"], cfg_n["min_grp"], cfg_n["n_candidates"])
        out["reels"][nom] = {**reel,
                             "nul42_config_nulle": {"maxsep": round(ms_n42, 4),
                                                    "stab": round(stab_n42, 4),
                                                    "ssep": round(ms_n42 * stab_n42, 4),
                                                    "mc": round(mc_n42, 4),
                                                    "rob": round(rob_n42, 4)},
                             "n": int(len(mat)), "n_flux": len(cols),
                             "maxsep_pipeline_R": cfg_r["maxsep_pipeline"],
                             "maxsep_pipeline_N": cfg_n["maxsep_pipeline"],
                             "d_maxsep_pipeline": round(cfg_r["maxsep_pipeline"] - cfg_n["maxsep_pipeline"], 4)}
        res = {}
        for cfg_nom, cfg in (("config_reelle", cfg_r), ("config_nulle", cfg_n)):
            if (nom, cfg_nom) in faits:
                print(f"[{nom} {cfg_nom}] deja complet — saute", flush=True)
                sub = raw_old[(raw_old["paire"] == nom) & (raw_old["config"] == cfg_nom)]
                maxs = sub["maxsep"].values.astype(float)
                stabs = sub["stab"].values.astype(float)
                mcs = sub["mc"].values.astype(float)
            else:
                maxs, stabs, mcs, robs = [], [], [], []
                t0 = time.time()
                for i in range(N_TIRAGES):
                    seed = int(rng_master.integers(2000, 10_000_000))
                    rng = np.random.default_rng(seed)
                    perm = rng.permutation(len(mat))
                    _, _, ms, stab, mc, rob = scan_replica(
                        mat[perm], cols, prog, cfg["w_size"], cfg["min_grp"],
                        cfg["n_candidates"])
                    maxs.append(ms)
                    stabs.append(stab)
                    mcs.append(mc)
                    robs.append(rob)
                    raw_rows.append({"paire": nom, "config": cfg_nom, "tirage": i,
                                     "maxsep": round(float(ms), 6),
                                     "stab": round(float(stab), 6),
                                     "ssep": round(float(ms * stab), 6),
                                     "mc": round(float(mc), 6),
                                     "rob": round(float(rob), 6)})
                    if (i + 1) % 250 == 0:
                        print(f"[{nom} {cfg_nom}] {i + 1}/{N_TIRAGES} "
                              f"({time.time() - t0:.0f} s)", flush=True)
                        pd.DataFrame(raw_rows).to_csv(raw_path, index=False)
                maxs = np.array(maxs)
                stabs = np.array(stabs)
                mcs = np.array(mcs)
                pd.DataFrame(raw_rows).to_csv(raw_path, index=False)
            sseps = np.array(maxs) * np.array(stabs)
            reel_ms = reel[cfg_nom]["maxsep"]
            d_max = dist_stats(maxs)
            d_ssep = dist_stats(sseps)
            d_mc = dist_stats(mcs)
            d_max["rang_reel_sur_1001"] = int((np.sum(maxs <= reel_ms) + 1))
            d_max["P_nul_sup_reel"] = round(float(np.mean(maxs >= reel_ms)), 4)
            d_max["pct_nuls_sous_plancher"] = round(
                float(np.mean((reel_ms - maxs) > 0.07)) * 100, 1)
            d_ssep["rang_reel_sur_1001"] = int((np.sum(sseps <= reel[cfg_nom]["ssep"]) + 1))
            res[cfg_nom] = {"maxsep": d_max, "ssep": d_ssep, "mc": d_mc}
            print(f"[{nom} {cfg_nom}] maxsep nul : mediane={d_max['mediane']} "
                  f"p95={d_max['p95']} ; reel {reel_ms} rang {d_max['rang_reel_sur_1001']}/1001 ; "
                  f"% nuls sous plancher {d_max['pct_nuls_sous_plancher']}", flush=True)
        out["distributions"][nom] = res
        with open(os.path.join(PDAC, "nulls_dist_893_replica.json"), "w") as f:
            json.dump(out, f, indent=1, ensure_ascii=False)

    # ---------------- Lecture gelee (§4) : config reelle primaire ----------------
    table = {}
    for nom, dr, dn, _ in PAIRS:
        cfg_r = cfgs[(nom, "reel")]
        d = out["distributions"][nom]["config_reelle"]["maxsep"]
        reel_ms = out["reels"][nom]["config_reelle"]["maxsep"]
        pct = d["pct_nuls_sous_plancher"]
        rang = d["rang_reel_sur_1001"]
        p95 = d["p95"]
        if reel_ms > p95 and pct >= 95.0:
            verdict = "SOLIDE"
        elif reel_ms > d["mediane"] or 50.0 <= pct < 95.0:
            verdict = "FRAGILE"
        else:
            verdict = "NON"
        # FRAGILE si reel > mediane mais <= p95, OU 50-95% sous plancher ;
        # NON si reel <= mediane OU < 50% sous plancher (prioritaire si conflit)
        if reel_ms <= d["mediane"] or pct < 50.0:
            verdict = "NON"
        table[nom] = {"n": out["reels"][nom]["n"], "n_flux": out["reels"][nom]["n_flux"],
                      "maxsep_reel": reel_ms, "p95_nuls": p95,
                      "mediane_nuls": d["mediane"],
                      "rang_reel_sur_1001": rang,
                      "pct_nuls_sous_plancher": pct,
                      "d_maxsep_pipeline": out["reels"][nom]["d_maxsep_pipeline"],
                      "verdict": verdict,
                      "config_nulle_p95": out["distributions"][nom]["config_nulle"]["maxsep"]["p95"],
                      "config_nulle_pct_sous_plancher": out["distributions"][nom]["config_nulle"]["maxsep"]["pct_nuls_sous_plancher"]}
    solides = [k for k, v in table.items() if v["verdict"] == "SOLIDE"]
    positifs = [k for k, v in table.items() if v["d_maxsep_pipeline"] > 0]
    out["table"] = table
    out["A2_distrib"] = {"solides": f"{len(solides)}/15",
                         "liste_solides": solides,
                         "positifs": f"{len(positifs)}/15",
                         "LOO": f"{len(solides) - 1 if solides else 0}/14",
                         "A2_classique_rappel": "10/15, 12/15 positifs, LOO 9/14 (§8.88.3)"}
    with open(os.path.join(PDAC, "nulls_dist_893_replica.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    with open(os.path.join(PDAC, "nulls_dist_893_table.json"), "w") as f:
        json.dump({"table": table, "A2_distrib": out["A2_distrib"]}, f, indent=1, ensure_ascii=False)
    print(f"A2-distrib : {out['A2_distrib']}")
    print("ecrit: nulls_dist_893_replica.json, nulls_dist_893_table.json, "
          "nulls_dist_893_replica_raw.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
