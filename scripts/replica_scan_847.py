#!/usr/bin/env python3
"""§8.47 (c) — Réplique du scan de seuil v6.2 (diagnostic externe).
CORRECTION DE MÉTHODE (19 nov., avant tout résultat de permutation) :
la première version de ce script ré-implémentait le scan avec le step brut
comme contrôle et ÉCHOUAIT la calibration (TCGA réel : réplique 0,3229
contre pipeline 0,5309 ; 4/8 exacts, 3/8 à ~0,002-0,008 près). Lecture du
code v6.2 : le scan n'utilise PAS le step brut — il utilise l'axe MC
`progress_pct` construit par `_build_mc_progress_axis` (médiane de 200
trajectoires harmoniques, graine 42, à partir du rang du contrôle ;
`run_pipeline`, l. 6817-6818). Cette version utilise donc les fonctions
DU PIPELINE ELLES-MÊMES (import en lecture seule, aucune modification) :
`_build_mc_progress_axis` pour l'axe + `scan_critical_threshold` pour le
scan (appel identique à celui du worker Monte-Carlo : n_candidates,
resolution=None, w_size, min_grp) + `evaluate_scan_quality` pour
max_separation/stabilité. Ce qui est répliqué, c'est le PLAN D'EXPÉRIENCE
(permutations), pas le calcul du scan.
CALIBRATION D'ABORD : la réplique doit reproduire max_separation des
8 runs v6.2 existants à ±0,001, courbe comprise — sinon rejet.
PUIS : 500 permutations par ligne par cohorte (graines 2000-2499),
500 permutations indépendantes par flux (graines 3000-3499, test H5),
décomposition par flux au meilleur candidat (ICGC réel / nul 42),
variante 10 gènes (sans IFNG/CD19) réel + nul 42, 4 cohortes (test H2),
bande nulle de la courbe de scan (ICGC).
L'axe progress_pct ne dépend que du contrôle (step) et de la graine :
il est IDENTIQUE pour le réel et tous les nuls d'une même cohorte
(le nul garde le step, il permute les flux).
Sorties : icgc_immune_inversion_replica.json / .csv.
Protocole gelé : PROTOCOL_icgc_immune_inversion.md
  SHA b55283eeb7a24e30b52ee6a8f24de8a77b3c7b53072d8b837fab9eb08a61eb34
  (+ addendum §9, correction de méthode, SHA à noter dans la section).
"""
import importlib.util
import json

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
COHORTES = ["tcga", "geo71729", "geo62452", "icgc"]
GENES12 = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163",
           "CD274", "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
SUBST = {"icgc": {"IFNG": "PRF1", "CD19": "MS4A1"}}

_spec = importlib.util.spec_from_file_location(
    "v62", "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py")
V62 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V62)
MODE_CFG = V62.PARAMETERS["modes"]["fast"].copy()
MODE_CFG.setdefault("random_seed", V62.RANDOM_SEED)


def genes(cohorte):
    return [SUBST.get(cohorte, {}).get(g, g) for g in GENES12]


def progress_axis(n):
    """Axe MC progress_pct du pipeline pour un contrôle step 0..n-1."""
    control = np.arange(n, dtype=float)
    axis = V62._build_mc_progress_axis(control, {}, MODE_CFG)
    assert axis["status"] == "ok", axis["status"]
    return np.asarray(axis["progress_pct"], dtype=float)


def scan_replica(flux_matrix, cols, progress, w_size, min_grp, n_candidates,
                 return_per_flux=False):
    """Scan via les fonctions du pipeline. Retourne
    (seuil, courbe, maxsep, stabilité, d_par_flux_au_max|None)."""
    fluxes = {k: flux_matrix[:, j].astype(float)
              for j, k in enumerate(cols)}
    thr, curve = V62.scan_critical_threshold(
        fluxes, progress, MODE_CFG, n_candidates, None, w_size, min_grp)
    metrics = V62.evaluate_scan_quality(curve, thr, w_size, len(progress))
    per_flux = None
    if return_per_flux:
        # d de Cohen par flux au seuil optimal, avec la formule exacte du
        # scan rapide : moments par fenêtres (écart-type poolé NON pondéré
        # sqrt((v1+v2)/2)), groupes = concaténation des fenêtres avec
        # leur multiplicité. (separation_score utiliserait le poolé
        # pondéré classique — autre formule, écart quand n1 != n2.)
        order = np.argsort(progress, kind="stable")
        prog_s = progress[order]
        n_pts = len(progress)
        w = max(2, min(w_size, n_pts // 2))
        n_windows = n_pts - w + 1
        cs = np.cumsum(np.concatenate(([0.0], prog_s)))
        win_progress = (cs[w:] - cs[:n_windows]) / w
        win_order = np.argsort(win_progress, kind="stable")
        win_sorted = win_progress[win_order]
        split = int(np.searchsorted(win_sorted, thr, side="left"))
        per_flux = {}
        for j, k in enumerate(cols):
            arr = flux_matrix[order, j].astype(float)
            anchor = float(np.median(arr))
            centered = arr - anchor
            sc = np.cumsum(np.concatenate(([0.0], centered)))
            qc = np.cumsum(np.concatenate(([0.0], centered * centered)))
            win_sum = sc[w:] - sc[:n_windows]
            win_sq = qc[w:] - qc[:n_windows]
            ps = np.concatenate(([0.0], np.cumsum(win_sum[win_order])))
            pq = np.concatenate(([0.0], np.cumsum(win_sq[win_order])))
            n1 = split * w
            n2 = (n_windows - split) * w
            s1, s2 = float(ps[split]), float(ps[-1] - ps[split])
            q1, q2 = float(pq[split]), float(pq[-1] - pq[split])
            m1 = anchor + s1 / n1
            m2 = anchor + s2 / n2
            v1 = max(0.0, q1 - s1 * s1 / n1) / (n1 - 1)
            v2 = max(0.0, q2 - s2 * s2 / n2) / (n2 - 1)
            pooled = np.sqrt((v1 + v2) / 2.0)
            d = abs((m1 - m2) / pooled) if pooled > 0 else 0.0
            per_flux[k] = round(float(d), 4)
    return (float(thr) if thr is not None and np.isfinite(thr) else np.nan,
            curve, float(metrics["max_separation"]),
            float(metrics["stability"]), per_flux)


def read_best_config(suffix):
    j = json.load(open(f"{PDAC}/results_fast_v62_{suffix}/master_results.json"))
    bc = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
    return {"w_size": int(bc["w_size"]), "min_grp": int(bc["min_grp"]),
            "n_candidates": int(bc["n_candidates"]),
            "resolution": (None if bc["resolution"] is None else float(bc["resolution"])),
            "maxsep_pipeline": float(bc["metrics"]["max_separation"]),
            "stab_pipeline": float(bc["metrics"]["stability"]),
            "mc_pipeline": float(bc["score"]),
            "thr_pipeline": float(bc["threshold"]),
            "scan_curve_pipeline": j["run_pipeline"]["scan_curve"]}


def main():
    out = {"calibration": {}, "distributions_nulles": {}, "h2_10_genes": {},
           "h5_flux_independants": {}, "decomposition_icgc": {},
           "bande_nulle_icgc": {}, "axe_progress": {}}

    # ---------- CALIBRATION sur les 8 runs v6.2 existants ----------
    print("=== CALIBRATION ===")
    cal_ok = True
    cfgs = {}
    for cohorte in COHORTES:
        prog = progress_axis(len(pd.read_csv(
            f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv")))
        out["axe_progress"][cohorte] = {
            "n": int(len(prog)),
            "min": round(float(prog.min()), 4), "max": round(float(prog.max()), 4),
            "ecart_max_vs_lineaire": round(
                float(np.max(np.abs(prog - np.linspace(0, 100, len(prog))))), 4),
            "monotone": bool(np.all(np.diff(prog) > 0))}
        print(f"[{cohorte}] axe progress_pct : min={prog.min():.2f} "
              f"max={prog.max():.2f} écart max vs linéaire="
              f"{np.max(np.abs(prog - np.linspace(0, 100, len(prog)))):.2f} "
              f"monotone={np.all(np.diff(prog) > 0)}")
        for side, suffix in (("reel", f"immune_{cohorte}"),
                             ("nul42", f"immune_{cohorte}_nul")):
            cfg = read_best_config(suffix)
            cfgs[(cohorte, side)] = cfg
            df = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes"
                             f"{'' if side == 'reel' else '_nul'}.csv")
            mat = df[genes(cohorte)].values.astype(float)
            thr, curve, maxsep, stab, _ = scan_replica(
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
                "config": {k: cfg[k] for k in ("w_size", "min_grp", "n_candidates", "resolution")},
                "maxsep_replique": round(maxsep, 6),
                "maxsep_pipeline": round(cfg["maxsep_pipeline"], 6),
                "ecart_maxsep": round(float(d_max), 8),
                "stab_replique": round(stab, 6),
                "stab_pipeline": round(cfg["stab_pipeline"], 6),
                "seuil_replique": round(thr, 4),
                "seuil_pipeline": round(cfg["thr_pipeline"], 4),
                "courbe_identique": bool(curve_ok),
                "ecart_max_courbe": round(float(max_curve_diff), 8),
                "ok": bool(ok)}
            print(f"[{cohorte} {side}] maxsep réplique={maxsep:.4f} "
                  f"pipeline={cfg['maxsep_pipeline']:.4f} écart={d_max:.2e} "
                  f"courbe_ok={curve_ok} (écart max {max_curve_diff:.2e}) -> {'OK' if ok else 'ÉCHEC'}")
    out["calibration_ok"] = bool(cal_ok)
    if not cal_ok:
        print("CALIBRATION ÉCHOUÉE — arrêt, la réplique est rejetée.")
        with open(f"{PDAC}/icgc_immune_inversion_replica.json", "w") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        return

    # ---------- Distributions nulles : 500 permutations par ligne ----------
    print("=== DISTRIBUTIONS NULLES (500 permutations par ligne) ===")
    rng_master = np.random.default_rng(20261119)
    for cohorte in COHORTES:
        df = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv")
        mat = df[genes(cohorte)].values.astype(float)
        prog = progress_axis(len(mat))
        cfg_r = cfgs[(cohorte, "reel")]
        cfg_n = cfgs[(cohorte, "nul42")]
        _, _, ms_r_cfgR, _, _ = scan_replica(
            mat, genes(cohorte), prog, cfg_r["w_size"], cfg_r["min_grp"],
            cfg_r["n_candidates"])
        _, _, ms_r_cfgN, _, _ = scan_replica(
            mat, genes(cohorte), prog, cfg_n["w_size"], cfg_n["min_grp"],
            cfg_n["n_candidates"])
        res = {"maxsep_reel_config_reelle": round(ms_r_cfgR, 4),
               "maxsep_reel_config_nulle": round(ms_r_cfgN, 4),
               "maxsep_nul42_config_nulle": round(cfg_n["maxsep_pipeline"], 4)}
        nul42 = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes_nul.csv")[genes(cohorte)].values.astype(float)
        _, _, ms_n42_cfgR, _, _ = scan_replica(
            nul42, genes(cohorte), prog, cfg_r["w_size"], cfg_r["min_grp"],
            cfg_r["n_candidates"])
        res["maxsep_nul42_config_reelle"] = round(ms_n42_cfgR, 4)
        for cfg_nom, cfg in (("config_reelle", cfg_r), ("config_nulle", cfg_n)):
            maxs = []
            curves = [] if cohorte == "icgc" else None
            for _ in range(500):
                seed = int(rng_master.integers(2000, 10_000_000))
                rng = np.random.default_rng(seed)
                perm = rng.permutation(len(mat))
                _, curve, ms, _, _ = scan_replica(
                    mat[perm], genes(cohorte), prog, cfg["w_size"],
                    cfg["min_grp"], cfg["n_candidates"])
                maxs.append(ms)
                if curves is not None:
                    curves.append([np.nan if c["score"] is None else c["score"]
                                   for c in curve])
            maxs = np.array(maxs)
            d = {"mediane": round(float(np.median(maxs)), 4),
                 "moyenne": round(float(np.mean(maxs)), 4),
                 "p2.5": round(float(np.quantile(maxs, 0.025)), 4),
                 "p97.5": round(float(np.quantile(maxs, 0.975)), 4),
                 "min": round(float(maxs.min()), 4),
                 "max": round(float(maxs.max()), 4),
                 "P_sup_nul42": round(float(np.mean(maxs >= cfg_n["maxsep_pipeline"])), 4),
                 "P_sup_reel": round(float(np.mean(maxs >= ms_r_cfgR)), 4),
                 "n_sup_nul42": int((maxs >= cfg_n["maxsep_pipeline"]).sum())}
            res[cfg_nom] = d
            print(f"[{cohorte} {cfg_nom}] médiane={d['mediane']} "
                  f"[p2.5={d['p2.5']}, p97.5={d['p97.5']}] "
                  f"P(≥nul42={cfg_n['maxsep_pipeline']:.3f})={d['P_sup_nul42']} "
                  f"P(≥réel={ms_r_cfgR:.3f})={d['P_sup_reel']}")
            if curves is not None:
                _, curve_ref, _, _, _ = scan_replica(
                    mat, genes(cohorte), prog, cfg["w_size"], cfg["min_grp"],
                    cfg["n_candidates"])
                arr = np.array(curves, dtype=float)
                band = {"candidats": [round(c["candidate"], 2) for c in curve_ref],
                        "mediane": [None if np.isnan(x) else round(float(x), 4)
                                    for x in np.nanmedian(arr, axis=0)],
                        "p25": [None if np.isnan(x) else round(float(x), 4)
                                for x in np.nanquantile(arr, 0.25, axis=0)],
                        "p75": [None if np.isnan(x) else round(float(x), 4)
                                for x in np.nanquantile(arr, 0.75, axis=0)]}
                out["bande_nulle_icgc"][cfg_nom] = band
        out["distributions_nulles"][cohorte] = res

    # ---------- H5 : permutations indépendantes par flux ----------
    print("=== H5 : PERMUTATIONS INDÉPENDANTES PAR FLUX (500 tirages) ===")
    for cohorte in COHORTES:
        df = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv")
        mat = df[genes(cohorte)].values.astype(float)
        prog = progress_axis(len(mat))
        cfg_n = cfgs[(cohorte, "nul42")]
        maxs = []
        for _ in range(500):
            seed = int(rng_master.integers(3000, 10_000_000))
            rng = np.random.default_rng(seed)
            perm_mat = np.column_stack(
                [rng.permutation(mat[:, j]) for j in range(mat.shape[1])])
            _, _, ms, _, _ = scan_replica(
                perm_mat, genes(cohorte), prog, cfg_n["w_size"],
                cfg_n["min_grp"], cfg_n["n_candidates"])
            maxs.append(ms)
        maxs = np.array(maxs)
        med_ligne = out["distributions_nulles"][cohorte]["config_nulle"]["mediane"]
        out["h5_flux_independants"][cohorte] = {
            "mediane_maxsep_indep": round(float(np.median(maxs)), 4),
            "p97.5_indep": round(float(np.quantile(maxs, 0.975)), 4),
            "mediane_maxsep_ligne": med_ligne,
            "ecart_medianes_ligne_moins_indep": round(float(med_ligne - np.median(maxs)), 4)}
        print(f"[{cohorte}] médiane indép={np.median(maxs):.4f} vs "
              f"ligne={med_ligne:.4f} écart={med_ligne - np.median(maxs):.4f}")

    # ---------- Décomposition par flux au meilleur candidat (ICGC) ----------
    print("=== DÉCOMPOSITION PAR FLUX (ICGC, meilleur candidat) ===")
    prog_icgc = progress_axis(70)
    for side, fname in (("reel", "pdac_immune_icgc_fluxes.csv"),
                        ("nul42", "pdac_immune_icgc_fluxes_nul.csv")):
        cfg = cfgs[("icgc", side)]
        mat = pd.read_csv(f"{PDAC}/{fname}")[genes("icgc")].values.astype(float)
        thr, _, maxsep, _, per_flux = scan_replica(
            mat, genes("icgc"), prog_icgc, cfg["w_size"], cfg["min_grp"],
            cfg["n_candidates"], return_per_flux=True)
        dec = {g: per_flux[g] for g in genes("icgc")}
        out["decomposition_icgc"][side] = {
            "seuil": round(thr, 2), "maxsep": round(maxsep, 4),
            "d_par_flux": dec,
            "flux_max": max(dec.items(), key=lambda kv: kv[1] if kv[1] is not None else -1)}
        print(f"[ICGC {side}] seuil={thr:.1f}% maxsep={maxsep:.4f} d par flux={dec}")

    # ---------- H2 : variante 10 gènes ----------
    print("=== H2 : VARIANTE 10 GÈNES (sans IFNG/CD19) ===")
    keep10 = [g for g in GENES12 if g not in ("IFNG", "CD19")]
    for cohorte in COHORTES:
        cols10 = [SUBST.get(cohorte, {}).get(g, g) for g in keep10]
        cfg_r = cfgs[(cohorte, "reel")]
        cfg_n = cfgs[(cohorte, "nul42")]
        df_r = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv")
        df_n = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes_nul.csv")
        prog = progress_axis(len(df_r))
        res10 = {}
        for side, df in (("reel", df_r), ("nul42", df_n)):
            mat10 = df[cols10].values.astype(float)
            for cfg_nom, cfg in (("config_reelle", cfg_r), ("config_nulle", cfg_n)):
                _, _, ms, stab, _ = scan_replica(
                    mat10, cols10, prog, cfg["w_size"], cfg["min_grp"],
                    cfg["n_candidates"])
                res10[f"maxsep_{side}_{cfg_nom}"] = round(ms, 4)
                res10[f"ssep_{side}_{cfg_nom}"] = round(ms * stab, 4)
        res10["d_ssep_config_reelle"] = round(
            res10["ssep_reel_config_reelle"] - res10["ssep_nul42_config_reelle"], 4)
        res10["d_ssep_config_nulle"] = round(
            res10["ssep_reel_config_nulle"] - res10["ssep_nul42_config_nulle"], 4)
        res10["d_ssep_12_genes_pipeline"] = {
            "tcga": 0.3659, "geo71729": 0.1343, "geo62452": 0.1534, "icgc": -0.2200}[cohorte]
        out["h2_10_genes"][cohorte] = res10
        print(f"[{cohorte}] 10g d_ssep config_réelle={res10['d_ssep_config_reelle']} "
              f"config_nulle={res10['d_ssep_config_nulle']} "
              f"(12g pipeline: {res10['d_ssep_12_genes_pipeline']})")

    with open(f"{PDAC}/icgc_immune_inversion_replica.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    rows = []
    for cohorte, r in out["distributions_nulles"].items():
        for cfg_nom in ("config_reelle", "config_nulle"):
            d = r[cfg_nom]
            rows.append({"cohorte": cohorte, "config": cfg_nom,
                         "maxsep_reel": r["maxsep_reel_config_reelle"],
                         "maxsep_nul42": r["maxsep_nul42_config_nulle"],
                         **{k: d[k] for k in
                            ("mediane", "moyenne", "p2.5", "p97.5", "min", "max",
                             "P_sup_nul42", "P_sup_reel", "n_sup_nul42")}})
    pd.DataFrame(rows).to_csv(f"{PDAC}/icgc_immune_inversion_replica.csv", index=False)
    print("écrit: icgc_immune_inversion_replica.json / .csv")


if __name__ == "__main__":
    main()
