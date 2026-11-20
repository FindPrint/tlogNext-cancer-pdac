#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.63 — Mécanismes non élucidés §8.50 / §8.53.
Étape A : lecture des `all_results` existants (MTAP 14 runs, immunitaires
48 runs + 10 frais §8.63) — ensemble de configs fixe par n, recomposition
du MC, FWHM recalculée depuis les courbes stockées, D_vector et médianes
par estimateur.
Étape B : réplique du scan (fonctions DU PIPELINE, import en lecture
seule, sans modification) — calibration sur 5 entrées puis tableau
12 configs x 5 entrées MTAP et porteurs du pic par flux seul.
Protocole gelé : PROTOCOL_mechanisms_863.md
(SHA 4e05dfc208725d610c591c2e4845dca277ed0d7d0a64e8ac095491f03c21f35e).
Lecture seule : aucune valeur inventée, aucun seuil choisi après coup.
Sorties : mechanisms_863_extract.json, mechanisms_863_results.csv,
mechanisms_863_perflux.csv.
"""
import csv
import hashlib
import importlib.util
import json
import math
import os

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

PDAC = os.path.dirname(os.path.abspath(__file__))
V62_PATH = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"

MTAP_FLUXES = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
               "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]
GENES12 = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163",
           "CD274", "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
SUBST = {"icgc": {"IFNG": "PRF1", "CD19": "MS4A1"}}

MTAP_RUNS = {
    "REEL": "results_fast_v62_mtap",
    "REEL_850": "results_fast_v62_mtap_850",
    "NUL42": "results_fast_v62_mtap_nul",
    "NUL_S7": "results_fast_v62_mtap_nul_s7",
    "NUL_S123": "results_fast_v62_mtap_nul_s123",
}
for s in (1011, 2022, 3033, 4044, 5055, 6066, 7077, 8088, 9099, 11111):
    MTAP_RUNS[f"NUL_S{s}"] = f"results_fast_v62_mtap_nul_s{s}"

IMMUNE_RUNS = {}  # label -> (cohorte, dossier)
for cohorte, reel, anciens in (
        ("icgc", "results_fast_v62_immune_icgc",
         {"s1": "results_fast_v62_847_icgc_nul_s1",
          "s2": "results_fast_v62_847_icgc_nul_s2",
          "s3": "results_fast_v62_847_icgc_nul_s3",
          "nul42": "results_fast_v62_immune_icgc_nul"}),
        ("geo62452", "results_fast_v62_immune_geo62452",
         {"s1": "results_fast_v62_847_geo62452_nul_s1",
          "s2": "results_fast_v62_847_geo62452_nul_s2",
          "nul42": "results_fast_v62_immune_geo62452_nul"}),
        ("tcga", "results_fast_v62_immune_tcga",
         {"s1": "results_fast_v62_847_tcga_nul_s1",
          "s2": "results_fast_v62_847_tcga_nul_s2",
          "nul42": "results_fast_v62_immune_tcga_nul"})):
    IMMUNE_RUNS[f"{cohorte}_reel"] = (cohorte, reel)
    for etiquette, d in anciens.items():
        IMMUNE_RUNS[f"{cohorte}_{etiquette}"] = (cohorte, d)
    n853 = range(11, 31) if cohorte in ("icgc", "geo62452") else range(11, 16)
    for s in n853:
        IMMUNE_RUNS[f"{cohorte}_nul_s{s}"] = (
            cohorte, f"results_fast_v62_853_{cohorte}_nul_s{s}")
for s in range(31, 41):
    IMMUNE_RUNS[f"icgc_nul_s{s}"] = (
        "icgc", f"results_fast_v62_863_icgc_nul_s{s}")

DIVERGENCE = ["LevinaBickel", "PCAIntrinsic", "LocalPCA", "GraphDimension",
              "PersistentHomology", "MFA"]
SATURATION = ["Higuchi", "Katz", "Petrosian", "Sevcik", "BoxCounting",
              "Hurst2mH", "DFA"]


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


def load_master(dossier):
    with open(os.path.join(PDAC, dossier, "master_results.json")) as f:
        return json.load(f)


def fwhm_rob_from_curve(curve):
    """Reproduit evaluate_scan_quality (lignes 3321-3364) : FWHM contiguë
    autour du pic, puis rob = exp(-((FWHM-10)^2)/(2*5^2))."""
    scores = [s["score"] for s in curve if s.get("score") is not None]
    cand = [s["candidate"] for s in curve if s.get("score") is not None]
    if len(scores) < 3:
        return None, None, None
    max_idx = int(np.argmax(scores))
    maxsep = float(scores[max_idx])
    half = maxsep / 2.0
    left = max_idx
    while left > 0 and scores[left] >= half:
        left -= 1
    right = max_idx
    while right < len(scores) - 1 and scores[right] >= half:
        right += 1
    fwhm = float(cand[right] - cand[left])
    rob = float(np.exp(-((fwhm - 10.0) ** 2) / (2 * 5.0 ** 2)))
    return fwhm, rob, maxsep


def read_all_results(j):
    tm = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]
    out = []
    for r in tm["all_results"]:
        m = r["metrics"]
        mc_recomp = (0.3 * m["s_norm"] + 0.3 * m["stability"]
                     + 0.2 * m["robustness"] + 0.2 * m["sharpness"])
        fwhm, rob_recomp, _ = fwhm_rob_from_curve(r["scan_curve"])
        out.append({
            "iteration": r.get("iteration"),
            "rule": r.get("rule"),
            "n_candidates": int(r["n_candidates"]),
            "w_size": int(r["w_size"]),
            "min_grp": int(r["min_grp"]),
            "threshold": float(r["threshold"]),
            "score": float(r["score"]),
            "mc_recomp": mc_recomp,
            "ecart_recomp": abs(mc_recomp - float(r["score"])),
            "s_norm": float(m["s_norm"]),
            "stability": float(m["stability"]),
            "robustness": float(m["robustness"]),
            "sharpness": float(m["sharpness"]),
            "max_separation": float(m["max_separation"]),
            "fwhm_recalculee": fwhm,
            "rob_recalculee": rob_recomp,
            "ecart_rob": (None if rob_recomp is None else
                          abs(rob_recomp - float(m["robustness"]))),
        })
    return out, tm["best_config"]


def read_run_common(j, dossier):
    dv = g(j, "holographic_tension_state.D_vector", {}) or {}
    per = g(j, "reading_synthesis.per_estimator", {}) or {}
    return {
        "dir": dossier,
        "version": j.get("version"),
        "n": fnum(g(j, "reading_synthesis.n_samples")),
        "d_sat": fnum(dv.get("d_sat")),
        "d_crit": fnum(dv.get("d_crit")),
        "d_div": fnum(dv.get("d_div")),
        "d_null": fnum(dv.get("d_null")),
        "delta": fnum(g(j, "reading_synthesis.Delta_tension")),
        "per_estimator": {k: fnum(v.get("raw_median")) for k, v in per.items()},
    }


# ---------------------------------------------------------------- A
def main():
    out = {"runs_mtap": {}, "runs_immune": {}, "manquants": [],
           "config_sets": {}, "fwhm": {}, "m1a": {}, "m2": {},
           "calibration_scan": {}, "perflux": {}}
    # ---- MTAP
    for label, d in MTAP_RUNS.items():
        try:
            j = load_master(d)
        except FileNotFoundError:
            out["manquants"].append(label)
            print(f"[MTAP {label}] MANQUANT")
            continue
        rows, bc = read_all_results(j)
        rec = read_run_common(j, d)
        rec["best_config"] = (int(bc["n_candidates"]), int(bc["w_size"]),
                              int(bc["min_grp"]))
        rec["best_rule"] = bc.get("rule")
        rec["all_results"] = rows
        rec["n_configs"] = len(rows)
        out["runs_mtap"][label] = rec
        w = max(rows, key=lambda r: r["score"])
        print(f"[MTAP {label:10s}] win={w['n_candidates'], w['w_size'], w['min_grp']} "
              f"MC={w['score']:.4f} rob={w['robustness']:.4f} "
              f"maxsep={w['max_separation']:.4f} Delta={rec['delta']:.4f} "
              f"d_div={rec['d_div']:.4f} d_sat={rec['d_sat']:.4f} "
              f"max_ecart_recomp={max(r['ecart_recomp'] for r in rows):.2e} "
              f"max_ecart_rob={max(r['ecart_rob'] for r in rows if r['ecart_rob'] is not None):.2e}")
    # ---- Immunitaires
    for label, (cohorte, d) in IMMUNE_RUNS.items():
        try:
            j = load_master(d)
        except FileNotFoundError:
            out["manquants"].append(label)
            print(f"[IMM {label}] MANQUANT")
            continue
        rows, bc = read_all_results(j)
        rec = read_run_common(j, d)
        rec["cohorte"] = cohorte
        rec["best_config"] = (int(bc["n_candidates"]), int(bc["w_size"]),
                              int(bc["min_grp"]))
        rec["all_results"] = rows
        rec["n_configs"] = len(rows)
        out["runs_immune"][label] = rec
    print(f"Immunitaires lus : {len(out['runs_immune'])} / {len(IMMUNE_RUNS)} "
          f"(manquants : {out['manquants']})")

    # ---- A1 : ensembles de configs par n
    for groupe, runs in (("mtap_n177", out["runs_mtap"]),
                         ("immune", out["runs_immune"])):
        by_n = {}
        for label, rec in runs.items():
            key = tuple(sorted((r["n_candidates"], r["w_size"], r["min_grp"],
                                r["rule"]) for r in rec["all_results"]))
            by_n.setdefault((rec["n"], key), []).append(label)
        for (n, key), labels in by_n.items():
            print(f"[A1 {groupe} n={n}] {len(labels)} runs, "
                  f"configs={key}")
            out["config_sets"].setdefault(groupe, []).append(
                {"n": n, "n_runs": len(labels), "labels": labels,
                 "configs": [list(c) for c in key]})

    # ---- M1a : (93,30,6) sur s11111 / s123 + rob sur les 14 runs
    def cfg_row(rec, cfg):
        for r in rec["all_results"]:
            if (r["n_candidates"], r["w_size"], r["min_grp"]) == cfg:
                return r
        return None
    m1a = {}
    for label in ("NUL_S11111", "NUL_S123"):
        rec = out["runs_mtap"][label]
        c28 = cfg_row(rec, (28, 27, 6))
        c93 = cfg_row(rec, (93, 30, 6))
        m1a[label] = {
            "mc_28_27_6": c28["score"], "rob_28_27_6": c28["robustness"],
            "maxsep_28_27_6": c28["max_separation"],
            "thr_28_27_6": c28["threshold"],
            "fwhm_28_27_6": c28["fwhm_recalculee"],
            "mc_93_30_6": c93["score"], "rob_93_30_6": c93["robustness"],
            "maxsep_93_30_6": c93["max_separation"],
            "thr_93_30_6": c93["threshold"],
            "fwhm_93_30_6": c93["fwhm_recalculee"],
            "marge_28_sur_93": c28["score"] - c93["score"],
        }
        print(f"[M1a {label}] (28,27,6) MC={c28['score']:.4f} rob={c28['robustness']:.4f} "
              f"FWHM={c28['fwhm_recalculee']:.2f} thr={c28['threshold']:.2f} | "
              f"(93,30,6) MC={c93['score']:.4f} rob={c93['robustness']:.4f} "
              f"FWHM={c93['fwhm_recalculee']:.2f} thr={c93['threshold']:.2f} | "
              f"marge={c28['score'] - c93['score']:.4f}")
    max_rob_par_run = {}
    for label, rec in out["runs_mtap"].items():
        mx = max(r["robustness"] for r in rec["all_results"])
        n_gt01 = sum(1 for r in rec["all_results"] if r["robustness"] > 0.1)
        max_rob_par_run[label] = {"max_rob": round(mx, 4), "n_rob_gt01": n_gt01}
    m1a["max_rob_par_run"] = max_rob_par_run
    m1a["max_ecart_rob_tous"] = max(
        r["ecart_rob"] for rec in out["runs_mtap"].values()
        for r in rec["all_results"] if r["ecart_rob"] is not None)
    m1a["max_ecart_recomp_mc"] = max(
        r["ecart_recomp"] for rec in out["runs_mtap"].values()
        for r in rec["all_results"])
    out["m1a"] = m1a
    print(f"[M1a] max écart rob recalculée = {m1a['max_ecart_rob_tous']:.2e} ; "
          f"max écart recomposition MC = {m1a['max_ecart_recomp_mc']:.2e}")
    print(f"[M1a] max rob par run : {max_rob_par_run}")

    # ---- M1 : D_vector et porteurs de d_div (14 runs MTAP)
    print("[M1-Delta] run | d_sat | d_div | Delta | "
          + " | ".join(DIVERGENCE))
    for label, rec in out["runs_mtap"].items():
        pe = rec["per_estimator"]
        print(f"  {label:10s} | {rec['d_sat']:.4f} | {rec['d_div']:.4f} | "
              f"{rec['delta']:.4f} | "
              + " | ".join(f"{pe.get(e)}" if pe.get(e) is None
                           else f"{pe[e]:.3f}" for e in DIVERGENCE))
    # écarts s11111/s123 vs réel, par estimateur de divergence (médianes brutes)
    reel_pe = out["runs_mtap"]["REEL"]["per_estimator"]
    for label in ("NUL_S11111", "NUL_S123", "NUL42"):
        pe = out["runs_mtap"][label]["per_estimator"]
        ecarts = {e: round(pe[e] - reel_pe[e], 4) for e in DIVERGENCE
                  if pe.get(e) is not None and reel_pe.get(e) is not None}
        print(f"[M1-Delta] écarts {label} − réel (divergence) : {ecarts}")

    # ---- M2 : tableaux par config, par cohorte (nuls frais §8.53 + §8.63)
    m2 = {}
    reels = {"icgc": (35, 16, 6), "geo62452": (34, 16, 6), "tcga": (93, 30, 6)}
    for cohorte in ("icgc", "geo62452", "tcga"):
        # nuls frais = s11..s40 (853 + 863), anciens s1-s3/nul42 exclus ici
        frais = [rec for label, rec in out["runs_immune"].items()
                 if rec["cohorte"] == cohorte and "_nul_s" in label
                 and int(label.rsplit("_s", 1)[1]) >= 11]
        reel = out["runs_immune"][f"{cohorte}_reel"]
        cfgs = sorted({(r["n_candidates"], r["w_size"], r["min_grp"])
                       for rec in frais for r in rec["all_results"]})
        table = []
        for c in cfgs:
            rows_c = [next(r for r in rec["all_results"]
                           if (r["n_candidates"], r["w_size"], r["min_grp"]) == c)
                      for rec in frais]
            mx = [r["max_separation"] for r in rows_c]
            mc = [r["score"] for r in rows_c]
            wins = sum(1 for rec in frais
                       if rec["best_config"] == c)
            rr = next(r for r in reel["all_results"]
                      if (r["n_candidates"], r["w_size"], r["min_grp"]) == c)
            table.append({"config": list(c),
                          "mean_maxsep_nuls": round(float(np.mean(mx)), 4),
                          "mean_mc_nuls": round(float(np.mean(mc)), 4),
                          "mean_stab_nuls": round(float(np.mean(
                              [r["stability"] for r in rows_c])), 4),
                          "mean_sharp_nuls": round(float(np.mean(
                              [r["sharpness"] for r in rows_c])), 4),
                          "mean_rob_nuls": round(float(np.mean(
                              [r["robustness"] for r in rows_c])), 4),
                          "wins": wins,
                          "reel_maxsep": round(rr["max_separation"], 4),
                          "reel_mc": round(rr["score"], 4)})
        ncand = np.array([t["config"][0] for t in table], dtype=float)
        mmax = np.array([t["mean_maxsep_nuls"] for t in table])
        rho, p_rho = spearmanr(ncand, mmax)
        # marges vainqueur-2e sur les nuls frais + réel
        marges = []
        for rec in frais + [reel]:
            s = sorted((r["score"] for r in rec["all_results"]), reverse=True)
            marges.append(round(s[0] - s[1], 4))
        m2[cohorte] = {
            "n_nuls_frais": len(frais),
            "config_reelle": list(reels[cohorte]),
            "table_par_config": table,
            "spearman_maxsep_vs_ncand": {"rho": round(float(rho), 4),
                                         "p": float(p_rho)},
            "marges": {"median": round(float(np.median(marges)), 4),
                       "min": min(marges), "max": max(marges),
                       "n_lt_0.005": int(sum(1 for v in marges if v < 0.005)),
                       "n_lt_0.01": int(sum(1 for v in marges if v < 0.01)),
                       "n_total": len(marges),
                       "valeurs": marges},
        }
        print(f"[M2 {cohorte}] nuls frais={len(frais)} ; "
              f"Spearman(maxsep moyen, ncand) rho={rho:.3f} p={p_rho:.3g} ; "
              f"marge médiane={np.median(marges):.4f} "
              f"(<{0.005}: {sum(1 for v in marges if v < 0.005)}/{len(marges)})")
        for t in sorted(table, key=lambda t: -t["mean_maxsep_nuls"]):
            print(f"    {tuple(t['config'])} mean_maxsep={t['mean_maxsep_nuls']:.4f} "
                  f"mean_MC={t['mean_mc_nuls']:.4f} wins={t['wins']} "
                  f"réel_maxsep={t['reel_maxsep']:.4f}")
    # M2d : lot frais s31-s40
    frais31 = [rec for label, rec in out["runs_immune"].items()
               if rec["cohorte"] == "icgc" and "_nul_s" in label
               and int(label.rsplit("_s", 1)[1]) >= 31]
    n_win_reel = sum(1 for rec in frais31 if rec["best_config"] == (35, 16, 6))
    from math import comb
    p_exact = None
    if len(frais31) == 10:
        p_exact = sum(comb(10, k) * 0.85 ** k * 0.15 ** (10 - k)
                      for k in range(0, n_win_reel + 1))
    m2["replication_s31_s40"] = {
        "n": len(frais31),
        "n_choisissent_config_reelle": n_win_reel,
        "p_binomial_cumulee_H0_p0.85": p_exact,
    }
    print(f"[M2d] s31-s40 : {n_win_reel}/{len(frais31)} choisissent (35,16,6) ; "
          f"P(X<={n_win_reel} | p=0,85) = {p_exact}")
    out["m2"] = m2

    # Préserve les résultats de l'étape B (calibration scan + perflux) si
    # un passage précédent les a déjà écrits (le lot §8.63 arrive après).
    try:
        with open(os.path.join(PDAC, "mechanisms_863_extract.json")) as f:
            prev = json.load(f)
        for k in ("calibration_scan", "perflux"):
            if k in prev:
                out[k] = prev[k]
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    with open(os.path.join(PDAC, "mechanisms_863_extract.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=str)
    # CSV résultats
    with open(os.path.join(PDAC, "mechanisms_863_results.csv"), "w",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["serie", "run", "config_gagnante", "mc", "maxsep",
                    "robustesse", "stabilite", "s_norm", "acuite", "delta",
                    "d_sat", "d_div", "marge_vainqueur_2e"])
        for label, rec in out["runs_mtap"].items():
            win = max(rec["all_results"], key=lambda r: r["score"])
            s2 = sorted((r["score"] for r in rec["all_results"]),
                        reverse=True)[1]
            w.writerow(["mtap", label, rec["best_config"], win["score"],
                        win["max_separation"], win["robustness"],
                        win["stability"], win["s_norm"], win["sharpness"],
                        rec["delta"], rec["d_sat"], rec["d_div"],
                        round(win["score"] - s2, 4)])
        for label, rec in out["runs_immune"].items():
            win = max(rec["all_results"], key=lambda r: r["score"])
            s2 = sorted((r["score"] for r in rec["all_results"]),
                        reverse=True)[1]
            w.writerow(["immune_" + rec["cohorte"], label,
                        rec["best_config"], win["score"],
                        win["max_separation"], win["robustness"],
                        win["stability"], win["s_norm"], win["sharpness"],
                        rec["delta"], rec["d_sat"], rec["d_div"],
                        round(win["score"] - s2, 4)])
    print("SHA script : " + sha(__file__))
    print("écrit: mechanisms_863_extract.json, mechanisms_863_results.csv")
    return out


# ---------------------------------------------------------------- B
def load_v62():
    spec = importlib.util.spec_from_file_location("v62", V62_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def progress_axis(v62, n):
    cfg = v62.PARAMETERS["modes"]["fast"].copy()
    cfg.setdefault("random_seed", v62.RANDOM_SEED)
    axis = v62._build_mc_progress_axis(np.arange(n, dtype=float), {}, cfg)
    assert axis["status"] == "ok", axis["status"]
    return np.asarray(axis["progress_pct"], dtype=float), cfg


def scan_replica(v62, flux_matrix, cols, progress, cfg, w, mingrp, ncand):
    fluxes = {k: flux_matrix[:, j].astype(float)
              for j, k in enumerate(cols)}
    thr, curve = v62.scan_critical_threshold(
        fluxes, progress, cfg, ncand, None, w, mingrp)
    metrics = v62.evaluate_scan_quality(curve, thr, w, len(progress))
    return thr, curve, metrics


def step_b(out):
    v62 = load_v62()
    cal = {}
    # ---- calibration : 5 entrées x 12 configs stockées
    cal_inputs = [
        ("mtap_reel", "pdac_tcga_fluxes_v4_mtap.csv", "MTAPCN", MTAP_FLUXES,
         "REEL"),
        ("mtap_s11111", "pdac_tcga_fluxes_v4_mtap_nul_s11111.csv", "MTAPCN",
         MTAP_FLUXES, "NUL_S11111"),
        ("mtap_s123", "pdac_tcga_fluxes_v4_mtap_nul_s123.csv", "MTAPCN",
         MTAP_FLUXES, "NUL_S123"),
        ("icgc_reel", "pdac_immune_icgc_fluxes.csv", "step",
         [SUBST["icgc"].get(g, g) for g in GENES12], "icgc_reel"),
        ("icgc_nul_s29", "pdac_immune_icgc_fluxes_nul_s29.csv", "step",
         [SUBST["icgc"].get(g, g) for g in GENES12], "icgc_nul_s29"),
    ]
    cal_ok = True
    for nom, csv_file, ctrl, cols, label in cal_inputs:
        df = pd.read_csv(os.path.join(PDAC, csv_file))
        mat = df[cols].values.astype(float)
        prog, cfg = progress_axis(v62, len(mat))
        rec = (out["runs_mtap"].get(label) or out["runs_immune"].get(label))
        j_stock = load_master(rec["dir"])
        ar_stock = j_stock["run_pipeline"]["threshold_metadata"][
            "threshold_optimization"]["all_results"]
        worst = 0.0
        worst_curve = 0.0
        for r in rec["all_results"]:
            thr, curve, metrics = scan_replica(
                v62, mat, cols, prog, cfg, r["w_size"], r["min_grp"],
                r["n_candidates"])
            worst = max(worst,
                        abs(metrics["max_separation"] - r["max_separation"]),
                        abs(metrics["stability"] - r["stability"]),
                        abs(metrics["robustness"] - r["robustness"]),
                        abs(float(thr) - r["threshold"]))
            rr = next(x for x in ar_stock
                      if (x["n_candidates"], x["w_size"], x["min_grp"])
                      == (r["n_candidates"], r["w_size"], r["min_grp"]))
            for a, b in zip(curve, rr["scan_curve"]):
                if a["score"] is None and b["score"] is None:
                    continue
                if (a["score"] is None) != (b["score"] is None):
                    worst_curve = float("inf")
                    break
                worst_curve = max(worst_curve, abs(a["score"] - b["score"]))
        ok = worst <= 1e-6 and worst_curve <= 1e-6
        cal_ok &= ok
        cal[nom] = {"ecart_max_metriques": float(worst),
                    "ecart_max_courbe": float(worst_curve), "ok": bool(ok)}
        print(f"[B-cal {nom}] écart max métriques={worst:.2e} "
              f"courbe={worst_curve:.2e} -> {'OK' if ok else 'ÉCHEC'}",
              flush=True)
    out["calibration_scan"] = {"entrees": cal, "ok": bool(cal_ok)}
    print(f"[B-cal] globale : {'OK' if cal_ok else 'ÉCHEC'}")
    if not cal_ok:
        print("CALIBRATION ÉCHOUÉE — réplique rejetée (protocole §2 B).")
        return out
    # ---- M1c : porteurs du pic, par flux seul
    perflux = {}
    for label, csv_path in (("NUL_S11111",
                        "pdac_tcga_fluxes_v4_mtap_nul_s11111.csv"),
                       ("NUL_S123", "pdac_tcga_fluxes_v4_mtap_nul_s123.csv"),
                       ("NUL42", "pdac_tcga_fluxes_v4_mtap_nul.csv"),
                       ("NUL_S1011", "pdac_tcga_fluxes_v4_mtap_nul_s1011.csv"),
                       ("NUL_S2022", "pdac_tcga_fluxes_v4_mtap_nul_s2022.csv"),
                       ("NUL_S9099", "pdac_tcga_fluxes_v4_mtap_nul_s9099.csv")):
        rec = out["runs_mtap"][label]
        win = max(rec["all_results"], key=lambda r: r["score"])
        df = pd.read_csv(os.path.join(PDAC, csv_path))
        mat = df[MTAP_FLUXES].values.astype(float)
        prog, cfg = progress_axis(v62, len(mat))
        # courbe complète à la config gagnante (réplique)
        thr, curve, _ = scan_replica(v62, mat, MTAP_FLUXES, prog, cfg,
                                     win["w_size"], win["min_grp"],
                                     win["n_candidates"])
        peak_cand = float(thr)
        # courbes par flux seul
        per_flux_at_peak = {}
        curves_1f = {}
        for j, flux in enumerate(MTAP_FLUXES):
            _, c1, _ = scan_replica(v62, mat[:, [j]], [flux], prog, cfg,
                                    win["w_size"], win["min_grp"],
                                    win["n_candidates"])
            curves_1f[flux] = c1
            at = [p["score"] for p in c1
                  if abs(p["candidate"] - peak_cand) < 1e-9]
            per_flux_at_peak[flux] = (None if not at else float(at[0]))
        # calibration interne : moyenne des 12 courbes = courbe complète
        worst_mean = 0.0
        for i, p in enumerate(curve):
            vals = [curves_1f[f][i]["score"] for f in MTAP_FLUXES]
            if p["score"] is None:
                continue
            m = float(np.nanmean([v for v in vals if v is not None]))
            worst_mean = max(worst_mean, abs(m - p["score"]))
        tot = sum(v for v in per_flux_at_peak.values() if v is not None)
        parts = {f: (None if v is None else round(v / tot, 4))
                 for f, v in per_flux_at_peak.items()}
        dom = max(per_flux_at_peak.items(),
                  key=lambda kv: kv[1] if kv[1] is not None else -1)
        perflux[label] = {
            "config_gagnante": [win["n_candidates"], win["w_size"],
                                win["min_grp"]],
            "seuil_pic_pct": round(peak_cand, 4),
            "score_pic": round(win["max_separation"], 4),
            "fwhm": win["fwhm_recalculee"],
            "rob": win["robustness"],
            "d_par_flux_au_pic": {f: (None if v is None else round(v, 4))
                                  for f, v in per_flux_at_peak.items()},
            "part_du_flux_dominant": parts[dom[0]],
            "flux_dominant": dom[0],
            "ecart_calibration_moyenne_12_flux": float(worst_mean),
        }
        print(f"[M1c {label}] pic à {peak_cand:.2f}% score={win['max_separation']:.4f} "
              f"FWHM={win['fwhm_recalculee']:.2f} ; flux dominant {dom[0]} "
              f"part={parts[dom[0]]} ; écart calibration moyenne={worst_mean:.2e}",
              flush=True)
    out["perflux"] = perflux
    with open(os.path.join(PDAC, "mechanisms_863_perflux.csv"), "w",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["run", "config_gagnante", "seuil_pic_pct", "score_pic",
                    "fwhm", "rob", "flux_dominant", "part_dominant"]
                   + MTAP_FLUXES)
        for label, p in perflux.items():
            w.writerow([label, p["config_gagnante"], p["seuil_pic_pct"],
                        p["score_pic"], p["fwhm"], p["rob"],
                        p["flux_dominant"], p["part_du_flux_dominant"]]
                       + [p["d_par_flux_au_pic"][fl] for fl in MTAP_FLUXES])
    return out


if __name__ == "__main__":
    res = main()
    res = step_b(res)
    with open(os.path.join(PDAC, "mechanisms_863_extract.json"), "w") as f:
        json.dump(res, f, indent=1, ensure_ascii=False, default=str)
    print("SHA script : " + sha(__file__))
    print("écrit: mechanisms_863_extract.json (final)")
