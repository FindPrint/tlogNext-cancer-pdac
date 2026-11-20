#!/usr/bin/env python3
"""§8.53 (b) — Réplique du scan : distribution des S_sep nuls, 1000 tirages.
Réutilise la machinerie calibrée de replica_scan_847.py (fonctions DU
PIPELINE, import en lecture seule, aucune modification) :
`_build_mc_progress_axis` + `scan_critical_threshold` +
`evaluate_scan_quality`. Ce qui est répliqué, c'est le PLAN D'EXPÉRIENCE
(permutations), pas le calcul du scan.
CALIBRATION D'ABORD : reproduire max_separation des 8 runs v6.2
existants à ±0,001, courbe comprise — sinon rejet, arrêt.
PUIS, par cohorte (ICGC n=70, GSE62452 n=69, TCGA n=178), sous les DEUX
configs fixes (config réelle et config nulle du run v6.2 existant) :
1000 permutations par ligne, graine maîtresse default_rng(20261119)
(NOUVELLE, distincte de §8.47). Chaque tirage donne maxsep ET stabilité,
donc S_sep = maxsep × stab. Les 1000 valeurs brutes par
(cohorte, config) sont conservées intégralement (JSON + CSV).
ENFIN : courbes de convergence — pour k = 1, 2, 3, 5, 10, 20, 30, 50,
100, 200, 500, 1000, 200 sous-échantillons sans remise de taille k
(k=1000 : l'échantillon complet, SE = 0 par construction) → écart-type
empirique de la médiane, intervalle 95 % du p95 estimé, écart-type de
l'écart-type. (Config nulle seulement, la config de référence du nul.)
Sorties : nulls_n70_853_replica.json, nulls_n70_853_replica_raw.csv,
nulls_n70_853_convergence.json / .csv.
Protocole gelé : PROTOCOL_nulls_n70_853.md
"""
import importlib.util
import json

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
COHORTES = ["icgc", "geo62452", "tcga"]
GENES12 = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163",
           "CD274", "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
SUBST = {"icgc": {"IFNG": "PRF1", "CD19": "MS4A1"}}
N_TIRAGES = 1000
KS = [1, 2, 3, 5, 10, 20, 30, 50, 100, 200, 500, 1000]
N_BOOT = 200

_spec = importlib.util.spec_from_file_location(
    "v62", "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py")
V62 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V62)
MODE_CFG = V62.PARAMETERS["modes"]["fast"].copy()
MODE_CFG.setdefault("random_seed", V62.RANDOM_SEED)


def genes(cohorte):
    return [SUBST.get(cohorte, {}).get(g, g) for g in GENES12]


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
    metrics = V62.evaluate_scan_quality(curve, thr, w_size, len(progress))
    return (float(thr) if thr is not None and np.isfinite(thr) else np.nan,
            curve, float(metrics["max_separation"]),
            float(metrics["stability"]))


def read_best_config(suffix):
    j = json.load(open(f"{PDAC}/results_fast_v62_{suffix}/master_results.json"))
    bc = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
    return {"w_size": int(bc["w_size"]), "min_grp": int(bc["min_grp"]),
            "n_candidates": int(bc["n_candidates"]),
            "maxsep_pipeline": float(bc["metrics"]["max_separation"]),
            "stab_pipeline": float(bc["metrics"]["stability"]),
            "mc_pipeline": float(bc["score"]),
            "thr_pipeline": float(bc["threshold"]),
            "scan_curve_pipeline": j["run_pipeline"]["scan_curve"]}


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


def main():
    out = {"calibration": {}, "distributions": {}, "reels": {}}
    raw_rows = []

    # ---------- CALIBRATION sur les 8 runs v6.2 existants ----------
    print("=== CALIBRATION ===", flush=True)
    cal_ok = True
    cfgs = {}
    for cohorte in COHORTES + ["geo71729"]:
        prog = progress_axis(len(pd.read_csv(
            f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv")))
        for side, suffix in (("reel", f"immune_{cohorte}"),
                             ("nul42", f"immune_{cohorte}_nul")):
            cfg = read_best_config(suffix)
            if cohorte in COHORTES:
                cfgs[(cohorte, side)] = cfg
            df = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes"
                             f"{'' if side == 'reel' else '_nul'}.csv")
            mat = df[genes(cohorte)].values.astype(float)
            thr, curve, maxsep, stab = scan_replica(
                mat, genes(cohorte), prog, cfg["w_size"], cfg["min_grp"],
                cfg["n_candidates"])
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
            out["calibration"][f"{cohorte}_{side}"] = {
                "maxsep_replique": round(maxsep, 6),
                "maxsep_pipeline": round(cfg["maxsep_pipeline"], 6),
                "ecart_maxsep": round(float(d_max), 8),
                "courbe_identique": bool(curve_ok),
                "ecart_max_courbe": round(float(max_curve_diff), 8),
                "ok": bool(ok)}
            print(f"[{cohorte} {side}] maxsep réplique={maxsep:.4f} "
                  f"pipeline={cfg['maxsep_pipeline']:.4f} écart={d_max:.2e} "
                  f"courbe_ok={curve_ok} -> {'OK' if ok else 'ÉCHEC'}", flush=True)
    out["calibration_ok"] = bool(cal_ok)
    if not cal_ok:
        print("CALIBRATION ÉCHOUÉE — arrêt, la réplique est rejetée.", flush=True)
        with open(f"{PDAC}/nulls_n70_853_replica.json", "w") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        return

    # ---------- Distributions nulles : 1000 permutations par ligne ----------
    print(f"=== DISTRIBUTIONS NULLES ({N_TIRAGES} permutations par ligne) ===", flush=True)
    rng_master = np.random.default_rng(20261119)
    for cohorte in COHORTES:
        df = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv")
        mat = df[genes(cohorte)].values.astype(float)
        prog = progress_axis(len(mat))
        cfg_r = cfgs[(cohorte, "reel")]
        cfg_n = cfgs[(cohorte, "nul42")]
        # réel sous les deux configs (référence)
        reel = {}
        for cfg_nom, cfg in (("config_reelle", cfg_r), ("config_nulle", cfg_n)):
            _, _, ms, stab = scan_replica(
                mat, genes(cohorte), prog, cfg["w_size"], cfg["min_grp"],
                cfg["n_candidates"])
            reel[cfg_nom] = {"maxsep": round(ms, 4), "stab": round(stab, 4),
                             "ssep": round(ms * stab, 4)}
        nul42 = pd.read_csv(
            f"{PDAC}/pdac_immune_{cohorte}_fluxes_nul.csv")[genes(cohorte)].values.astype(float)
        _, _, ms_n42, stab_n42 = scan_replica(
            nul42, genes(cohorte), prog, cfg_n["w_size"], cfg_n["min_grp"],
            cfg_n["n_candidates"])
        out["reels"][cohorte] = {
            **reel, "nul42_config_nulle": {"maxsep": round(ms_n42, 4),
                                           "stab": round(stab_n42, 4),
                                           "ssep": round(ms_n42 * stab_n42, 4)},
            "n": int(len(mat))}
        res = {}
        for cfg_nom, cfg in (("config_reelle", cfg_r), ("config_nulle", cfg_n)):
            maxs, stabs = [], []
            for i in range(N_TIRAGES):
                seed = int(rng_master.integers(2000, 10_000_000))
                rng = np.random.default_rng(seed)
                perm = rng.permutation(len(mat))
                _, _, ms, stab = scan_replica(
                    mat[perm], genes(cohorte), prog, cfg["w_size"],
                    cfg["min_grp"], cfg["n_candidates"])
                maxs.append(ms)
                stabs.append(stab)
                if (i + 1) % 250 == 0:
                    print(f"[{cohorte} {cfg_nom}] {i + 1}/{N_TIRAGES}", flush=True)
            sseps = np.array(maxs) * np.array(stabs)
            for j, (ms, st) in enumerate(zip(maxs, stabs)):
                raw_rows.append({"cohorte": cohorte, "config": cfg_nom,
                                 "tirage": j, "maxsep": round(float(ms), 6),
                                 "stab": round(float(st), 6),
                                 "ssep": round(float(ms * st), 6)})
            d_max = dist_stats(maxs)
            d_ssep = dist_stats(sseps)
            ssep_reel = reel[cfg_nom]["ssep"]
            d_ssep["P_nul_sup_reel"] = round(float(np.mean(sseps >= ssep_reel)), 4)
            d_ssep["percentile_reel"] = round(float(np.mean(sseps <= ssep_reel)) * 100, 1)
            d_ssep["P_nul_sup_nul42"] = round(
                float(np.mean(sseps >= ms_n42 * stab_n42)), 4)
            res[cfg_nom] = {"maxsep": d_max, "ssep": d_ssep}
            print(f"[{cohorte} {cfg_nom}] S_sep nul : médiane={d_ssep['mediane']} "
                  f"p5={d_ssep['p5']} p95={d_ssep['p95']} p97.5={d_ssep['p97.5']} "
                  f"SD={d_ssep['ecart_type']} IQR={d_ssep['iqr']} "
                  f"P(≥réel {ssep_reel})={d_ssep['P_nul_sup_reel']}", flush=True)
        out["distributions"][cohorte] = res

    pd.DataFrame(raw_rows).to_csv(f"{PDAC}/nulls_n70_853_replica_raw.csv", index=False)
    print("écrit: nulls_n70_853_replica_raw.csv "
          f"({len(raw_rows)} lignes)", flush=True)

    # ---------- Convergence : combien de nuls faut-il ? (config nulle) ----------
    print("=== CONVERGENCE (config nulle, 200 sous-échantillons) ===", flush=True)
    conv = {}
    rng_conv = np.random.default_rng(777)
    raw = pd.read_csv(f"{PDAC}/nulls_n70_853_replica_raw.csv")
    for cohorte in COHORTES:
        vals = raw[(raw["cohorte"] == cohorte)
                   & (raw["config"] == "config_nulle")]["ssep"].values
        assert len(vals) == N_TIRAGES
        rows = []
        for k in KS:
            if k >= N_TIRAGES:
                meds = np.array([np.median(vals)])
                p95s = np.array([np.quantile(vals, 0.95)])
                sds = np.array([np.std(vals, ddof=1)])
            else:
                meds, p95s, sds = [], [], []
                for _ in range(N_BOOT):
                    sub = rng_conv.choice(vals, size=k, replace=False)
                    meds.append(np.median(sub))
                    p95s.append(np.quantile(sub, 0.95))
                    sds.append(np.std(sub, ddof=1) if k > 1 else 0.0)
                meds, p95s, sds = map(np.array, (meds, p95s, sds))
            rows.append({"k": k,
                         "mediane_des_medianes": round(float(np.median(meds)), 4),
                         "se_mediane": round(float(np.std(meds, ddof=1)) if len(meds) > 1 else 0.0, 4),
                         "p95_median": round(float(np.median(p95s)), 4),
                         "p95_p2.5": round(float(np.quantile(p95s, 0.025)), 4),
                         "p95_p97.5": round(float(np.quantile(p95s, 0.975)), 4),
                         "demi_largeur_ic95_p95": round(float((np.quantile(p95s, 0.975) - np.quantile(p95s, 0.025)) / 2), 4),
                         "sd_median": round(float(np.median(sds)), 4),
                         "se_sd": round(float(np.std(sds, ddof=1)) if len(sds) > 1 else 0.0, 4)})
            print(f"[{cohorte} k={k}] SE(médiane)={rows[-1]['se_mediane']} "
                  f"IC95 p95 demi-largeur={rows[-1]['demi_largeur_ic95_p95']} "
                  f"SE(SD)={rows[-1]['se_sd']}", flush=True)
        conv[cohorte] = rows
    out["convergence"] = conv
    with open(f"{PDAC}/nulls_n70_853_replica.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    pd.DataFrame([{**{"cohorte": c}, **r} for c, rows in conv.items() for r in rows]
                 ).to_csv(f"{PDAC}/nulls_n70_853_convergence.csv", index=False)
    print("écrit: nulls_n70_853_replica.json / nulls_n70_853_convergence.csv", flush=True)


if __name__ == "__main__":
    main()
