#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.73 — Déclencheur du pic étroit (§8.63, résidu ouvert).
Protocole gelé : PROTOCOL_pic_etroit_873.md
(SHA 28d2326c3ae83676d3e15f7283f0b37ae69a1791bcaa1f50c7b06ee368651a4c).
Lecture seule du pipeline v6.2 (jamais modifié) ; réplique du scan par
ses fonctions importées, calibration à 1e-6 avant toute lecture.
Étapes : cal (calibration), corpus (statistiques §4 B),
interv (interventions A/A1/A2/B1/B0/B2), fresh (lecture des 20 runs
frais et comparaison aux prédictions — exige que le fichier de
prédictions existe déjà).
Sorties : pic_etroit_873_extract.json, pic_etroit_873_results.csv,
pic_etroit_873_interv.csv, pic_etroit_873_interv_*.csv (CSV modifiés).
"""
import csv
import hashlib
import importlib.util
import json
import math
import os
import sys

import numpy as np
import pandas as pd

PDAC = os.path.dirname(os.path.abspath(__file__))
V62_PATH = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
EXTRACT863 = os.path.join(PDAC, "mechanisms_863_extract.json")

MTAP_FLUXES = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
               "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]

# --- courbes rob-on gagnantes (relues §8.63, protocole §0) : label -> (csv, dir) ---
ROBON = {
    "mtap_NUL42": ("pdac_tcga_fluxes_v4_mtap_nul.csv",
                   "results_fast_v62_mtap_nul"),
    "mtap_NUL_S123": ("pdac_tcga_fluxes_v4_mtap_nul_s123.csv",
                      "results_fast_v62_mtap_nul_s123"),
    "mtap_NUL_S11111": ("pdac_tcga_fluxes_v4_mtap_nul_s11111.csv",
                        "results_fast_v62_mtap_nul_s11111"),
    "icgc_s1": ("pdac_immune_icgc_fluxes_nul_s1.csv",
                "results_fast_v62_847_icgc_nul_s1"),
    "geo62452_nul_s12": ("pdac_immune_geo62452_fluxes_nul_s12.csv",
                         "results_fast_v62_853_geo62452_nul_s12"),
    "tcga_s2": ("pdac_immune_tcga_fluxes_nul_s2.csv",
                "results_fast_v62_847_tcga_nul_s2"),
    "tcga_nul_s11": ("pdac_immune_tcga_fluxes_nul_s11.csv",
                     "results_fast_v62_853_tcga_nul_s11"),
    "tcga_nul_s12": ("pdac_immune_tcga_fluxes_nul_s12.csv",
                     "results_fast_v62_853_tcga_nul_s12"),
    "icgc_nul_s32": ("pdac_immune_icgc_fluxes_nul_s32.csv",
                     "results_fast_v62_863_icgc_nul_s32"),
    "icgc_nul_s35": ("pdac_immune_icgc_fluxes_nul_s35.csv",
                     "results_fast_v62_863_icgc_nul_s35"),
    "icgc_nul_s37": ("pdac_immune_icgc_fluxes_nul_s37.csv",
                     "results_fast_v62_863_icgc_nul_s37"),
}
CONTROLES = {  # label -> (csv, dir) ; gagnante rob = 0,0000 (vérifié avant gel)
    "mtap_NUL_S7": ("pdac_tcga_fluxes_v4_mtap_nul_s7.csv",
                    "results_fast_v62_mtap_nul_s7"),
    "mtap_NUL_S1011": ("pdac_tcga_fluxes_v4_mtap_nul_s1011.csv",
                       "results_fast_v62_mtap_nul_s1011"),
    "icgc_nul_s31": ("pdac_immune_icgc_fluxes_nul_s31.csv",
                     "results_fast_v62_863_icgc_nul_s31"),
    "icgc_nul_s33": ("pdac_immune_icgc_fluxes_nul_s33.csv",
                     "results_fast_v62_863_icgc_nul_s33"),
    "geo62452_nul_s11": ("pdac_immune_geo62452_fluxes_nul_s11.csv",
                         "results_fast_v62_853_geo62452_nul_s11"),
    "tcga_nul_s13": ("pdac_immune_tcga_fluxes_nul_s13.csv",
                     "results_fast_v62_853_tcga_nul_s13"),
}
# Donneurs B2 : (contrôle -> donneur rob-on, même série)
DONNEUR_B2 = {"mtap_NUL_S1011": "mtap_NUL_S11111",
              "icgc_nul_s31": "icgc_nul_s37",
              "icgc_nul_s33": "icgc_nul_s37"}
# B0 (bloc médian au bord) sur ces 2 contrôles
B0_CONTROLES = ["geo62452_nul_s11", "tcga_nul_s13"]

ICGC_CONFIGS = [[9, 20, 7], [11, 15, 6], [14, 23, 2], [14, 35, 7],
                [17, 34, 5], [22, 16, 7], [24, 27, 5], [26, 29, 6],
                [35, 16, 6], [38, 24, 5], [38, 28, 9], [39, 24, 9]]
# (ncand, w, mingrp) ; règles lues dans l'extract §8.63 (config_sets immune n=70)
ICGC_RULES = {(9, 20, 7): "uniform", (11, 15, 6): "uniform",
              (14, 23, 2): "sqrt3", (14, 35, 7): "sqrt3",
              (17, 34, 5): "uniform", (22, 16, 7): "e",
              (24, 27, 5): "uniform", (26, 29, 6): "uniform",
              (35, 16, 6): "uniform", (38, 24, 5): "uniform",
              (38, 28, 9): "uniform", (39, 24, 9): "sqrt2"}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_v62():
    spec = importlib.util.spec_from_file_location("v62", V62_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def flux_cols(df):
    return [c for c in df.columns if c not in ("MTAPCN", "step")]


def load_mat(csv_name):
    df = pd.read_csv(os.path.join(PDAC, csv_name))
    cols = flux_cols(df)
    return df[cols].values.astype(float), cols, df


def progress_axis(v62, n):
    cfg = v62.PARAMETERS["modes"]["fast"].copy()
    cfg.setdefault("random_seed", v62.RANDOM_SEED)
    axis = v62._build_mc_progress_axis(np.arange(n, dtype=float), {}, cfg)
    assert axis["status"] == "ok", axis["status"]
    return np.asarray(axis["progress_pct"], dtype=float), cfg


def win_progress_of(prog, w):
    n = len(prog)
    nw = n - w + 1
    cs = np.cumsum(np.concatenate(([0.0], prog)))
    winp = (cs[w:] - cs[:nw]) / w
    wo = np.argsort(winp, kind="stable")
    assert np.array_equal(wo, np.arange(nw)), "win_order n'est pas l'identité"
    assert np.all(np.diff(winp) > 0), "win_progress non strictement croissante"
    return winp, nw


def z_scores(mat):
    med = np.median(mat, axis=0)
    mad = np.median(np.abs(mat - med), axis=0)
    scale = np.where(mad == 0, 1.0, 1.4826 * mad)
    z = np.where(mad == 0, 0.0, (mat - med) / scale)
    return z, med


def row_extremity(mat):
    z, med = z_scores(mat)
    return np.mean(np.abs(z), axis=1), z, med


def small_rows(split, nw, w, n):
    """Lignes distinctes du petit côté, à un split donné."""
    if split <= nw / 2:
        return slice(0, split + w - 1)  # côté bas : lignes 0..split+w-2
    return slice(split, n)              # côté haut : lignes split..n-1


def gh_at_candidates(mat, w, mingrp, ncand, prog):
    """G(c), H(c) sur les candidats de bord valides du scan.
    Retourne dict : candidats, splits, G, H, winp, nw."""
    n = len(mat)
    e, z, med = row_extremity(mat)
    winp, nw = win_progress_of(prog, w)
    cands = np.linspace(0, 100, int(ncand))
    out = {"candidats": [], "splits": [], "G": [], "H": [], "winp": winp,
           "nw": nw}
    for c in cands:
        split = int(np.searchsorted(winp, float(c), side="left"))
        if split < mingrp or split > nw - mingrp:
            continue
        if min(split, nw - split) > 0.20 * nw:
            continue
        rows = small_rows(split, nw, w, n)
        out["candidats"].append(float(c))
        out["splits"].append(split)
        out["G"].append(float(np.mean(e[rows])))
        out["H"].append(float(np.mean(np.abs(np.mean(z[rows], axis=0)))))
    return out


def scan_replica(v62, mat, cols, prog, cfg, w, mingrp, ncand):
    fluxes = {k: mat[:, j].astype(float) for j, k in enumerate(cols)}
    thr, curve = v62.scan_critical_threshold(
        fluxes, prog, cfg, ncand, None, w, mingrp)
    metrics = v62.evaluate_scan_quality(curve, thr, w, len(prog))
    return thr, curve, metrics


def curve_score_at(curve, thr):
    """Score de la courbe au candidat thr (tolérance 1e-9)."""
    for p in curve:
        if abs(p["candidate"] - thr) < 1e-9:
            return p["score"]
    return None


def load_master(dossier):
    with open(os.path.join(PDAC, dossier, "master_results.json")) as f:
        return json.load(f)


def stock_row(j, cfg):
    ar = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["all_results"]
    for r in ar:
        if (r["n_candidates"], r["w_size"], r["min_grp"]) == tuple(cfg):
            return r
    return None


def best_stock(j):
    tm = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]
    bc = tm["best_config"]
    return (int(bc["n_candidates"]), int(bc["w_size"]), int(bc["min_grp"])), tm


def load_extract863():
    with open(EXTRACT863) as f:
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


# ------------------------------------------------------------------ A
def stage_cal(v62, out):
    """Calibration réplique : 5 entrées §8.63 x 12 configs + 17 courbes
    (11 rob-on + 6 contrôles) à leur config gagnante. Seuil 1e-6."""
    ex863 = load_extract863()
    cal = {"entrees_863": {}, "courbes_873": {}, "ok": True}
    cal_inputs = [
        ("mtap_reel", "pdac_tcga_fluxes_v4_mtap.csv", "REEL"),
        ("mtap_s11111", "pdac_tcga_fluxes_v4_mtap_nul_s11111.csv", "NUL_S11111"),
        ("mtap_s123", "pdac_tcga_fluxes_v4_mtap_nul_s123.csv", "NUL_S123"),
        ("icgc_reel", "pdac_immune_icgc_fluxes.csv", "icgc_reel"),
        ("icgc_nul_s29", "pdac_immune_icgc_fluxes_nul_s29.csv", "icgc_nul_s29"),
    ]
    # map label extract -> (serie, run_dir)
    dir_of = {}
    for label, rec in ex863["runs_mtap"].items():
        dir_of[label] = rec["dir"]
    for label, rec in ex863["runs_immune"].items():
        dir_of[label] = rec["dir"]
    for nom, csv_file, label in cal_inputs:
        mat, cols, _ = load_mat(csv_file)
        prog, cfg = progress_axis(v62, len(mat))
        j = load_master(dir_of[label])
        rec = (ex863["runs_mtap"].get(label)
               or ex863["runs_immune"].get(label))
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
            rr = stock_row(j, (r["n_candidates"], r["w_size"], r["min_grp"]))
            for a, b in zip(curve, rr["scan_curve"]):
                if a["score"] is None and b["score"] is None:
                    continue
                if (a["score"] is None) != (b["score"] is None):
                    worst_curve = float("inf")
                    break
                worst_curve = max(worst_curve, abs(a["score"] - b["score"]))
        ok = worst <= 1e-6 and worst_curve <= 1e-6
        cal["entrees_863"][nom] = {"ecart_max_metriques": float(worst),
                                   "ecart_max_courbe": float(worst_curve),
                                   "ok": bool(ok)}
        cal["ok"] &= ok
        print(f"[CAL-863 {nom}] métriques={worst:.2e} courbe={worst_curve:.2e} "
              f"-> {'OK' if ok else 'ÉCHEC'}", flush=True)
    # 17 courbes à leur config gagnante
    for label, (csv_file, d) in {**ROBON, **CONTROLES}.items():
        mat, cols, _ = load_mat(csv_file)
        prog, cfg = progress_axis(v62, len(mat))
        j = load_master(d)
        bc, _ = best_stock(j)
        r = stock_row(j, bc)
        thr, curve, metrics = scan_replica(
            v62, mat, cols, prog, cfg, bc[1], bc[2], bc[0])
        worst = max(abs(metrics["max_separation"] - r["metrics"]["max_separation"]),
                    abs(metrics["stability"] - r["metrics"]["stability"]),
                    abs(metrics["robustness"] - r["metrics"]["robustness"]),
                    abs(float(thr) - r["threshold"]))
        worst_curve = 0.0
        for a, b in zip(curve, r["scan_curve"]):
            if a["score"] is None and b["score"] is None:
                continue
            if (a["score"] is None) != (b["score"] is None):
                worst_curve = float("inf")
                break
            worst_curve = max(worst_curve, abs(a["score"] - b["score"]))
        ok = worst <= 1e-6 and worst_curve <= 1e-6
        cal["courbes_873"][label] = {
            "config_gagnante": list(bc), "ecart_max_metriques": float(worst),
            "ecart_max_courbe": float(worst_curve), "ok": bool(ok),
            "rob_stockee": float(r["metrics"]["robustness"]),
            "seuil_stocke": float(r["threshold"]),
            "maxsep_stocke": float(r["metrics"]["max_separation"])}
        cal["ok"] &= ok
        print(f"[CAL-873 {label}] config={bc} métriques={worst:.2e} "
              f"courbe={worst_curve:.2e} -> {'OK' if ok else 'ÉCHEC'}",
              flush=True)
    out["calibration"] = cal
    print(f"[CAL] globale : {'OK' if cal['ok'] else 'ÉCHEC'}")
    return cal


# ------------------------------------------------------------------ B
def auc_mannwhitney(x_pos, x_neg):
    """AUC via U de Mann-Whitney (sans sklearn)."""
    x_pos = np.asarray(x_pos, dtype=float)
    x_neg = np.asarray(x_neg, dtype=float)
    n1, n2 = len(x_pos), len(x_neg)
    if n1 == 0 or n2 == 0:
        return None
    ranks = {}
    allv = np.concatenate([x_pos, x_neg])
    order = np.argsort(allv, kind="stable")
    r = np.empty(len(allv))
    i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[order[j + 1]] == allv[order[i]]:
            j += 1
        r[order[i:j + 1]] = (i + j) / 2.0 + 1
        i = j + 1
    u = float(np.sum(r[:n1]) - n1 * (n1 + 1) / 2.0)
    return u / (n1 * n2)


def mannwhitney_p(x_pos, x_neg):
    from scipy.stats import mannwhitneyu
    try:
        return float(mannwhitneyu(x_pos, x_neg, alternative="two-sided").pvalue)
    except Exception:
        return None


def stage_corpus(v62, out):
    """Statistiques §4 B : gagnantes des 82 runs + position G(c)."""
    ex863 = load_extract863()
    # map run -> csv
    def csv_for_immune(label, cohorte):
        if label == f"{cohorte}_reel":
            return f"pdac_immune_{cohorte}_fluxes.csv"
        if label.endswith("_nul42"):
            return f"pdac_immune_{cohorte}_fluxes_nul.csv"
        s = label.rsplit("_s", 1)[1]
        return f"pdac_immune_{cohorte}_fluxes_nul_s{s}.csv"

    def csv_for_mtap(label):
        if label == "REEL":
            return "pdac_tcga_fluxes_v4_mtap.csv"
        if label == "REEL_850":
            return None  # même CSV que REEL (doublon §8.50), exclu du corpus
        if label == "NUL42":
            return "pdac_tcga_fluxes_v4_mtap_nul.csv"
        s = label.rsplit("_S", 1)[1]
        return f"pdac_tcga_fluxes_v4_mtap_nul_s{s}.csv"

    from scipy.stats import kurtosis
    rows = []
    prog_cache = {}
    for serie, runs in (("mtap", ex863["runs_mtap"]),
                        ("immune", ex863["runs_immune"])):
        for label, rec in runs.items():
            if serie == "mtap":
                csv_file = csv_for_mtap(label)
                cohorte = "mtap"
            else:
                cohorte = rec["cohorte"]
                csv_file = csv_for_immune(label, cohorte)
            if csv_file is None:
                continue
            win = max(rec["all_results"], key=lambda r: r["score"])
            cfg = (win["n_candidates"], win["w_size"], win["min_grp"])
            mat, cols, _ = load_mat(csv_file)
            n = len(mat)
            if n not in prog_cache:
                prog_cache[n] = progress_axis(v62, n)
            prog, cfgm = prog_cache[n]
            gh = gh_at_candidates(mat, cfg[1], cfg[2], cfg[0], prog)
            e, z, med = row_extremity(mat)
            winp, nw = win_progress_of(prog, cfg[1])
            ek = np.array([e[k:k + cfg[1]].mean() for k in range(nw)])
            rows.append({
                "serie": serie, "run": label, "cohorte": cohorte,
                "config_gagnante": list(cfg),
                "mc": win["score"], "rob": win["robustness"],
                "maxsep": win["max_separation"],
                "seuil_pic": win["threshold"], "fwhm": win["fwhm_recalculee"],
                "rob_on": bool(win["robustness"] > 0.5),
                "rob_off": bool(win["robustness"] < 0.05),
                "H_max": max(gh["H"]) if gh["H"] else None,
                "G_max": max(gh["G"]) if gh["G"] else None,
                "E_max": float(np.max(ek)),
                "max_e_ligne": float(np.max(e)),
                "kurtosis_moy": float(np.mean(
                    [kurtosis(mat[:, j]) for j in range(mat.shape[1])])),
                "candidat_pred_G": (gh["candidats"][int(np.argmax(gh["G"]))]
                                   if gh["G"] else None),
                "n_candidats_bord": len(gh["G"]),
            })
    on = [r for r in rows if r["rob_on"]]
    off = [r for r in rows if r["rob_off"]]
    stats = {}
    for key in ("H_max", "E_max", "max_e_ligne", "kurtosis_moy"):
        xp = [r[key] for r in on]
        xn = [r[key] for r in off]
        stats[key] = {"n_on": len(xp), "n_off": len(xn),
                      "median_on": float(np.median(xp)),
                      "median_off": float(np.median(xn)),
                      "auc": auc_mannwhitney(xp, xn),
                      "p_mannwhitney": mannwhitney_p(xp, xn)}
    # position : pic réel vs argmax G(c) sur les 11 rob-on gagnantes
    step = {}
    pos_ok = 0
    pos_detail = []
    for r in on:
        ncand = r["config_gagnante"][0]
        pas = 100.0 / (ncand - 1)
        ok = (r["candidat_pred_G"] is not None
              and abs(r["seuil_pic"] - r["candidat_pred_G"]) <= 2 * pas + 1e-9)
        pos_ok += int(ok)
        pos_detail.append({"run": r["run"], "seuil_reel": r["seuil_pic"],
                           "candidat_pred_G": r["candidat_pred_G"],
                           "pas": round(pas, 4), "ok_2pas": bool(ok)})
    stats["position_G"] = {"n_rob_on": len(on), "ok_2pas": pos_ok,
                           "detail": pos_detail}
    out["corpus"] = {"lignes": rows, "stats": stats}
    print(f"[CORPUS] {len(rows)} gagnantes ; rob-on={len(on)} "
          f"rob-off={len(off)} ; position G ok={pos_ok}/{len(on)}")
    for k, s in stats.items():
        if k != "position_G":
            print(f"  {k}: médiane on={s['median_on']:.4f} "
                  f"off={s['median_off']:.4f} AUC={s['auc']} p={s['p_mannwhitney']}")
    return out["corpus"]


# ------------------------------------------------------------------ C/D
def block_of_curve(w, thr, prog):
    """Bloc B d'une courbe rob-on : (lignes [debut, fin], split, winp, nw)."""
    winp, nw = win_progress_of(prog, w)
    split = int(np.searchsorted(winp, float(thr), side="left"))
    assert 1 <= split <= nw - 1, f"split hors bornes : {split}/{nw}"
    debut, fin = split - 1, split + w - 1
    assert 0 <= debut and fin <= len(prog) - 1
    return (debut, fin), split, winp, nw


def write_modified(df_orig, mat_new, path):
    df = df_orig.copy()
    cols = flux_cols(df_orig)
    for j, c in enumerate(cols):
        df[c] = mat_new[:, j]
    df.to_csv(path, index=False)
    return sha(path)


def stage_interv(v62, out):
    """Interventions A/A1/A2 (11 rob-on) et B1/B0/B2 (6 contrôles)."""
    ex863 = load_extract863()
    interv = []
    prog_cache = {}

    def prog_of(n):
        if n not in prog_cache:
            prog_cache[n] = progress_axis(v62, n)
        return prog_cache[n]

    # ---- C : 11 courbes rob-on
    for label, (csv_file, d) in ROBON.items():
        j = load_master(d)
        bc, _ = best_stock(j)
        ncand, w, mingrp = bc
        r = stock_row(j, bc)
        thr = float(r["threshold"])
        maxsep = float(r["metrics"]["max_separation"])
        mat, cols, df = load_mat(csv_file)
        n = len(mat)
        prog, cfg = prog_of(n)
        (deb, fin), split, winp, nw = block_of_curve(w, thr, prog)
        e, z, med = row_extremity(mat)
        rec = {"run": label, "csv": csv_file, "config_gagnante": list(bc),
               "seuil_pic": thr, "maxsep": maxsep,
               "rob_stockee": float(r["metrics"]["robustness"]),
               "bloc_lignes": [deb, fin], "split": split,
               "E_bloc_moy": float(np.mean(e[deb:fin + 1])),
               "E_mediane_fenetres": None}
        ek = np.array([e[k:k + w].mean() for k in range(nw)])
        rec["E_mediane_fenetres"] = float(np.median(ek))
        rec["E_max_fenetres"] = float(np.max(ek))
        rec["E_fenetres_frontieres"] = [float(ek[split - 1]), float(ek[split])]
        rec["rang_E_fenetres_frontieres"] = [
            int((ek > ek[split - 1]).sum()), int((ek > ek[split]).sum())]
        # --- A : swap bloc B <-> bloc médian M
        m = None
        for m_cand in (n // 2 - w // 2, n - w - 1, 0,
                       n // 2 - w // 2 + (w + 1), n // 2 - w // 2 - (w + 1)):
            if 0 <= m_cand and m_cand + w < n and (m_cand + w < deb
                                                   or m_cand > fin):
                m = m_cand
                break
        assert m is not None, f"aucun bloc médian valide pour {label}"
        rec["bloc_median_lignes"] = [m, m + w]
        mat_swap = mat.copy()
        tmp = mat[deb:fin + 1].copy()
        mat_swap[deb:fin + 1] = mat[m:m + w + 1]
        mat_swap[m:m + w + 1] = tmp
        p_swap = os.path.join(PDAC, f"pic873_interv_{label}_Aswap.csv")
        rec["sha_Aswap"] = write_modified(df, mat_swap, p_swap)
        thr2, curve2, met2 = scan_replica(
            v62, mat_swap, cols, prog, cfg, w, mingrp, ncand)
        sc_old = curve_score_at(curve2, thr)
        idx = min(range(len(curve2)),
                  key=lambda i: abs(curve2[i]["candidate"] - thr))
        voisinage = [curve2[i]["score"] for i in range(
            max(0, idx - 2), min(len(curve2), idx + 3))
            if curve2[i]["score"] is not None]
        rec["A_swap_score_vieux_seuil"] = sc_old
        rec["A_swap_max_voisinage_2pas"] = max(voisinage) if voisinage else None
        rec["A_swap_rob_nouvelle"] = met2["robustness"]
        fwhm2, _, maxsep2 = fwhm_rob_from_curve(curve2)
        rec["A_swap_succes"] = bool(
            sc_old is not None and sc_old < 0.5 * maxsep
            and max(voisinage) < 0.5 * maxsep)
        rec["A_swap_nouveau_seuil"] = float(thr2)
        rec["A_swap_maxsep_nouvelle"] = met2["max_separation"]
        rec["A_swap_fwhm_nouvelle"] = fwhm2
        rec["A_swap_courbe"] = [p["score"] for p in curve2]
        rec["A_swap_candidats"] = [p["candidate"] for p in curve2]
        # --- A1 : winsorisation, échelons (a) 2, (b) 4, (c) 8 fenêtres
        rec["A1"] = {}
        for nom_ech, (f0, f1) in (("a_2fen", (split - 1, split)),
                                  ("b_4fen", (split - 2, split + 1)),
                                  ("c_8fen", (split - 4, split + 3))):
            d0, f0r = max(0, f0), min(n - 1, f1 + w - 1)
            mat_w = mat.copy()
            mat_w[d0:f0r + 1] = med
            p_w = os.path.join(
                PDAC, f"pic873_interv_{label}_A1{nom_ech[0]}.csv")
            sh = write_modified(df, mat_w, p_w)
            _, curvew, metw = scan_replica(
                v62, mat_w, cols, prog, cfg, w, mingrp, ncand)
            fwhmw, _, _ = fwhm_rob_from_curve(curvew)
            rec["A1"][nom_ech] = {
                "lignes": [d0, f0r], "rob_nouvelle": metw["robustness"],
                "maxsep_nouvelle": metw["max_separation"],
                "fwhm_nouvelle": fwhmw,
                "score_vieux_seuil": curve_score_at(curvew, thr),
                "succes": bool(metw["robustness"] < 0.1), "sha": sh}
        # --- A2 : winsorisation d'une seule ligne (argmax e_i dans B)
        r_star = deb + int(np.argmax(e[deb:fin + 1]))
        mat_1 = mat.copy()
        mat_1[r_star] = med
        p_1 = os.path.join(PDAC, f"pic873_interv_{label}_A2.csv")
        rec["A2_sha"] = write_modified(df, mat_1, p_1)
        rec["A2_ligne"] = int(r_star)
        rec["A2_e_ligne"] = float(e[r_star])
        _, curve1, met1 = scan_replica(
            v62, mat_1, cols, prog, cfg, w, mingrp, ncand)
        fwhm1, _, _ = fwhm_rob_from_curve(curve1)
        rec["A2_rob_nouvelle"] = met1["robustness"]
        rec["A2_maxsep_nouvelle"] = met1["max_separation"]
        rec["A2_fwhm_nouvelle"] = fwhm1
        rec["A2_score_vieux_seuil"] = curve_score_at(curve1, thr)
        rec["A2_succes"] = bool(met1["robustness"] < 0.1)
        interv.append(rec)
        print(f"[INTERV {label}] A-swap succès={rec['A_swap_succes']} "
              f"(score vieux seuil={sc_old} vs {0.5 * maxsep:.4f}) ; "
              f"A1 a/b/c rob={[rec['A1'][k]['rob_nouvelle'] for k in ('a_2fen', 'b_4fen', 'c_8fen')]} ; "
              f"A2 rob={met1['robustness']:.4f}", flush=True)

    # ---- D : contrôles B1 / B0 / B2
    controles = []
    for label, (csv_file, d) in CONTROLES.items():
        j = load_master(d)
        bc, _ = best_stock(j)
        ncand, w, mingrp = bc
        mat, cols, df = load_mat(csv_file)
        n = len(mat)
        prog, cfg = prog_of(n)
        winp, nw = win_progress_of(prog, w)
        e, z, med = row_extremity(mat)
        ek = np.array([e[k:k + w].mean() for k in range(nw)])
        cands = np.linspace(0, 100, int(ncand))
        pas = 100.0 / (ncand - 1)
        pred = float(cands[int(np.argmin(np.abs(cands - winp[1])))])
        rec = {"run": label, "csv": csv_file, "config_gagnante": list(bc),
               "rob_stockee": 0.0, "candidat_pred_B": pred, "pas": pas,
               "E_max_fenetres": float(np.max(ek)),
               "E_mediane_fenetres": float(np.median(ek))}
        # --- B1 : propre bloc extrême au bord
        k_star = int(np.argmax(ek))
        idx_new = list(range(k_star, k_star + w + 1)) + [
            i for i in range(n) if not (k_star <= i <= k_star + w)]
        mat_b1 = mat[idx_new]
        p_b1 = os.path.join(PDAC, f"pic873_interv_{label}_B1.csv")
        rec["B1_sha"] = write_modified(df, mat_b1, p_b1)
        rec["B1_bloc_lignes_origine"] = [k_star, k_star + w]
        thr_b1, curve_b1, met_b1 = scan_replica(
            v62, mat_b1, cols, prog, cfg, w, mingrp, ncand)
        fwhm_b1, _, _ = fwhm_rob_from_curve(curve_b1)
        rec["B1_fwhm_nouvelle"] = fwhm_b1
        rec["B1_rob_nouvelle"] = met_b1["robustness"]
        rec["B1_maxsep_nouvelle"] = met_b1["max_separation"]
        rec["B1_nouveau_seuil"] = float(thr_b1)
        rec["B1_succes"] = bool(met_b1["robustness"] > 0.5
                                and abs(float(thr_b1) - pred) <= 2 * pas + 1e-9)
        # --- B0 : bloc médian au bord (contrôle négatif)
        if label in B0_CONTROLES:
            k_med = int(np.argmin(np.abs(ek - np.median(ek))))
            idx0 = list(range(k_med, k_med + w + 1)) + [
                i for i in range(n) if not (k_med <= i <= k_med + w)]
            mat_b0 = mat[idx0]
            p_b0 = os.path.join(PDAC, f"pic873_interv_{label}_B0.csv")
            rec["B0_sha"] = write_modified(df, mat_b0, p_b0)
            rec["B0_bloc_lignes_origine"] = [k_med, k_med + w]
            thr_b0, _, met_b0 = scan_replica(
                v62, mat_b0, cols, prog, cfg, w, mingrp, ncand)
            rec["B0_rob_nouvelle"] = met_b0["robustness"]
            rec["B0_maxsep_nouvelle"] = met_b0["max_separation"]
            rec["B0_nouveau_seuil"] = float(thr_b0)
            rec["B0_pic_cree"] = bool(met_b0["robustness"] > 0.5)
        # --- B2 : valeurs donneuses au bord
        if label in DONNEUR_B2:
            don = DONNEUR_B2[label]
            dcsv, dd = ROBON[don]
            dj = load_master(dd)
            dbc, _ = best_stock(dj)
            dw = dbc[1]
            dmat, _, _ = load_mat(dcsv)
            dn = len(dmat)
            dprog, _ = prog_of(dn)
            dthr = float(stock_row(dj, dbc)["threshold"])
            (ddeb, dfin), _, _, _ = block_of_curve(dw, dthr, dprog)
            L = dfin - ddeb + 1
            mat_b2 = mat.copy()
            mat_b2[0:L] = dmat[ddeb:dfin + 1]
            p_b2 = os.path.join(PDAC, f"pic873_interv_{label}_B2.csv")
            rec["B2_sha"] = write_modified(df, mat_b2, p_b2)
            rec["B2_donneur"] = don
            rec["B2_L_lignes"] = int(L)
            thr_b2, _, met_b2 = scan_replica(
                v62, mat_b2, cols, prog, cfg, w, mingrp, ncand)
            rec["B2_rob_nouvelle"] = met_b2["robustness"]
            rec["B2_maxsep_nouvelle"] = met_b2["max_separation"]
            rec["B2_nouveau_seuil"] = float(thr_b2)
            rec["B2_succes"] = bool(
                met_b2["robustness"] > 0.5
                and abs(float(thr_b2) - pred) <= 2 * pas + 1e-9)
        controles.append(rec)
        print(f"[INTERV-CTRL {label}] B1 rob={rec['B1_rob_nouvelle']:.4f} "
              f"succès={rec['B1_succes']} ; "
              + (f"B0 rob={rec.get('B0_rob_nouvelle')} pic={rec.get('B0_pic_cree')} ; "
                 if label in B0_CONTROLES else "")
              + (f"B2 rob={rec.get('B2_rob_nouvelle')} succès={rec.get('B2_succes')}"
                 if label in DONNEUR_B2 else ""), flush=True)
    out["interventions"] = {"robon": interv, "controles": controles}
    # bilans
    n_swap = sum(1 for r in interv if r["A_swap_succes"])
    n_a1 = {}
    for ech in ("a_2fen", "b_4fen", "c_8fen"):
        n_a1[ech] = sum(1 for r in interv if r["A1"][ech]["succes"])
    n_a2 = sum(1 for r in interv if r["A2_succes"])
    n_b1 = sum(1 for r in controles if r["B1_succes"])
    n_b2 = sum(1 for r in controles
               if "B2_succes" in r and r["B2_succes"])
    n_b2_tot = sum(1 for r in controles if "B2_succes" in r)
    n_b0 = sum(1 for r in controles
               if "B0_pic_cree" in r and r["B0_pic_cree"])
    out["interventions"]["bilan"] = {
        "A_swap_succes": f"{n_swap}/11", "A1_succes": n_a1,
        "A2_succes": f"{n_a2}/11", "B1_succes": f"{n_b1}/{len(controles)}",
        "B2_succes": f"{n_b2}/{n_b2_tot}", "B0_pic_cree": f"{n_b0}/2"}
    print(f"[INTERV-BILAN] A-swap {n_swap}/11 ; A1 {n_a1} ; A2 {n_a2}/11 ; "
          f"B1 {n_b1}/{len(controles)} ; B2 {n_b2}/{n_b2_tot} ; B0 pic {n_b0}/2")
    return out["interventions"]


# ------------------------------------------------------------------ E
def stage_fresh(v62, out):
    """Lecture des 20 runs frais : vérification réplique 240 courbes,
    comparaison aux prédictions (P1/P2). Exige le fichier de prédictions."""
    pred_path = os.path.join(PDAC, "pic_etroit_873_predictions.json")
    assert os.path.exists(pred_path), "fichier de prédictions absent"
    with open(pred_path) as f:
        pred = json.load(f)
    print(f"[FRESH] prédictions SHA {sha(pred_path)[:12]}… "
          f"écrites {pred['horodatage_utc']}")
    pred_by = {(p["graine"], tuple(p["config"])): p
               for p in pred["predictions"]}
    ex863 = load_extract863()
    fresh = {"runs": {}, "verification_replique": {}, "P1": {}, "P2": {}}
    worst_met = 0.0
    worst_curve = 0.0
    n_curves = 0
    p1_ok = 0
    p1_tot = 0
    p1_detail = []
    y_true, y_score, y_pred = [], [], []
    n_pred_exclues = 0
    for seed in range(41, 61):
        d = f"results_fast_v62_873_icgc_nul_s{seed}"
        csv_file = f"pdac_immune_icgc_fluxes_nul_s{seed}.csv"
        j = load_master(d)
        bc, _ = best_stock(j)
        mat, cols, _ = load_mat(csv_file)
        prog, cfg = progress_axis(v62, len(mat))
        run_rec = {"config_gagnante": list(bc), "courbes": {}}
        ar = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["all_results"]
        for r in ar:
            cfg_t = (r["n_candidates"], r["w_size"], r["min_grp"])
            thr, curve, metrics = scan_replica(
                v62, mat, cols, prog, cfg, cfg_t[1], cfg_t[2], cfg_t[0])
            n_curves += 1
            worst_met = max(worst_met,
                            abs(metrics["max_separation"]
                                - r["metrics"]["max_separation"]),
                            abs(metrics["stability"]
                                - r["metrics"]["stability"]),
                            abs(metrics["robustness"]
                                - r["metrics"]["robustness"]),
                            abs(float(thr) - r["threshold"]))
            for a, b in zip(curve, r["scan_curve"]):
                if a["score"] is None and b["score"] is None:
                    continue
                if (a["score"] is None) != (b["score"] is None):
                    worst_curve = float("inf")
                    break
                worst_curve = max(worst_curve, abs(a["score"] - b["score"]))
            rob = float(r["metrics"]["robustness"])
            run_rec["courbes"][str(list(cfg_t))] = {
                "mc": float(r["score"]), "rob": rob,
                "maxsep": float(r["metrics"]["max_separation"]),
                "seuil": float(r["threshold"]),
                "fwhm": None}
            # P1 / P2
            p = pred_by.get((seed, cfg_t))
            assert p is not None, f"prédiction manquante s{seed} {cfg_t}"
            if rob > 0.5:
                p1_tot += 1
                pas = 100.0 / (cfg_t[0] - 1)
                ok = abs(float(r["threshold"]) - p["candidat_pred_G"]) <= 2 * pas + 1e-9
                p1_ok += int(ok)
                p1_detail.append({"graine": seed, "config": list(cfg_t),
                                  "seuil_reel": float(r["threshold"]),
                                  "candidat_pred_G": p["candidat_pred_G"],
                                  "ok_2pas": bool(ok)})
            th = pred["T_H"].get(str(list(cfg_t)))
            if th is None:
                n_pred_exclues += 1
            else:
                y_true.append(1 if rob > 0.5 else 0)
                y_score.append(p["H_max"])
                y_pred.append(1 if p["H_max"] >= th else 0)
        win = max(ar, key=lambda r: r["score"])
        run_rec["mc_gagnant"] = float(win["score"])
        run_rec["rob_gagnant"] = float(win["metrics"]["robustness"])
        run_rec["gagnante_robon"] = bool(win["metrics"]["robustness"] > 0.5)
        fresh["runs"][f"s{seed}"] = run_rec
        print(f"[FRESH s{seed}] gagnante={bc} MC={win['score']:.4f} "
              f"rob={win['metrics']['robustness']:.4f}", flush=True)
    fresh["verification_replique"] = {
        "n_courbes": n_curves, "ecart_max_metriques": float(worst_met),
        "ecart_max_courbe": float(worst_curve),
        "ok": bool(worst_met <= 1e-6 and worst_curve <= 1e-6)}
    fresh["P1"] = {"n_courbes_robon": p1_tot, "ok_2pas": p1_ok,
                   "detail": p1_detail,
                   "succes_70pc": bool(p1_tot >= 5 and p1_ok / p1_tot >= 0.70)
                   if p1_tot else None}
    auc = auc_mannwhitney([s for t, s in zip(y_true, y_score) if t == 1],
                          [s for t, s in zip(y_true, y_score) if t == 0]) \
        if sum(y_true) > 0 and sum(y_true) < len(y_true) else None
    tp = sum(1 for t, p_ in zip(y_true, y_pred) if t == 1 and p_ == 1)
    fp = sum(1 for t, p_ in zip(y_true, y_pred) if t == 0 and p_ == 1)
    fn = sum(1 for t, p_ in zip(y_true, y_pred) if t == 1 and p_ == 0)
    tn = sum(1 for t, p_ in zip(y_true, y_pred) if t == 0 and p_ == 0)
    fresh["P2"] = {"n_courbes_scorées": len(y_true),
                   "n_courbes_exclues_T_H_indefini": n_pred_exclues,
                   "n_robon": int(sum(y_true)), "auc_H_max": auc,
                   "confusion_T_H": {"TP": tp, "FP": fp, "FN": fn, "TN": tn},
                   "succes_auc_080": bool(auc is not None and auc >= 0.80)}
    fresh["n_gagnantes_robon"] = sum(
        1 for r in fresh["runs"].values() if r["gagnante_robon"])
    out["fresh"] = fresh
    print(f"[FRESH] vérification réplique {n_curves} courbes : "
          f"métriques={worst_met:.2e} courbe={worst_curve:.2e}")
    print(f"[FRESH] gagnantes rob-on : {fresh['n_gagnantes_robon']}/20 ; "
          f"P1 {p1_ok}/{p1_tot} ; P2 AUC={auc} (TP={tp} FP={fp} FN={fn} TN={tn})")
    return fresh


# ------------------------------------------------------------------ main
def load_prev():
    p = os.path.join(PDAC, "pic_etroit_873_extract.json")
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {}


def save(out):
    p = os.path.join(PDAC, "pic_etroit_873_extract.json")
    with open(p, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=str)
    print(f"écrit: pic_etroit_873_extract.json (SHA {sha(p)[:12]}…)")


def main():
    stages = sys.argv[1:] or ["cal", "corpus", "interv"]
    v62 = load_v62()
    out = load_prev()
    out["protocole_sha"] = ("28d2326c3ae83676d3e15f7283f0b37ae69a1791bcaa1f50c7b06ee368651a4c")
    out["v62_sha"] = sha(V62_PATH)
    if "cal" in stages:
        stage_cal(v62, out)
        save(out)
    if "corpus" in stages:
        stage_corpus(v62, out)
        save(out)
    if "interv" in stages:
        if not out.get("calibration", {}).get("ok"):
            print("CALIBRATION NON OK — interventions refusées (protocole §5).")
            return
        stage_interv(v62, out)
        save(out)
    if "fresh" in stages:
        stage_fresh(v62, out)
        save(out)
    if "diag" in stages:
        if "interventions" not in out:
            print("Interventions absentes — diag refusé.")
            return
        stage_diag(v62, out)
        save(out)
    if "diag2" in stages:
        if "interventions" not in out:
            print("Interventions absentes — diag2 refusé.")
            return
        stage_diag2(v62, out)
        save(out)
    print("SHA script : " + sha(__file__))




# ------------------------------------------------------------------ DIAG
# POST-HOC (hors protocole gelé — diagnostics d'interprétation seulement,
# jamais dans les règles de décision du §5). Ajouté après lecture des
# premiers résultats d'intervention (A-swap 0/3, A1 tuant le pic) pour
# départager « le bloc B est spécial » de « winsoriser n'importe quel
# bloc tue le pic ».
def stage_diag(v62, out):
    from scipy.stats import spearmanr
    diag = {"D1_winsorise_M": [], "D2_courbe_vs_moyenne_cumulee": [],
            "D3_pic_apres_swap": []}
    interv = out.get("interventions", {}).get("robon", [])
    prog_cache = {}

    def prog_of(n):
        if n not in prog_cache:
            prog_cache[n] = progress_axis(v62, n)
        return prog_cache[n]

    for rec in interv:
        label = rec["run"]
        csv_file = rec["csv"]
        ncand, w, mingrp = rec["config_gagnante"]
        thr = rec["seuil_pic"]
        mat, cols, df = load_mat(csv_file)
        n = len(mat)
        prog, cfg = prog_of(n)
        winp, nw = win_progress_of(prog, w)
        e, z, med = row_extremity(mat)
        # --- D1 : winsoriser le bloc médian M (même taille que B)
        m0, m1 = rec["bloc_median_lignes"]
        mat_m = mat.copy()
        mat_m[m0:m1 + 1] = med
        _, curve_m, met_m = scan_replica(
            v62, mat_m, cols, prog, cfg, w, mingrp, ncand)
        fwhm_m, _, _ = fwhm_rob_from_curve(curve_m)
        diag["D1_winsorise_M"].append({
            "run": label, "bloc_M_lignes": [m0, m1],
            "rob_nouvelle": met_m["robustness"],
            "maxsep_nouvelle": met_m["max_separation"],
            "fwhm_nouvelle": fwhm_m,
            "score_vieux_seuil": curve_score_at(curve_m, thr),
            "tue_le_pic": bool(met_m["robustness"] < 0.1)})
        # --- D2 : corrélation courbe de scan vs écart de la moyenne
        # cumulative du groupe bas (par candidat valide du scan)
        _, curve0, _ = scan_replica(
            v62, mat, cols, prog, cfg, w, mingrp, ncand)
        xs, ys = [], []
        for p in curve0:
            if p["score"] is None:
                continue
            split = int(np.searchsorted(winp, p["candidate"], side="left"))
            if split < mingrp or split > nw - mingrp:
                continue
            rows = slice(0, split + w - 1)
            dev = float(np.mean(np.abs(np.mean(z[rows], axis=0))))
            xs.append(dev)
            ys.append(p["score"])
        rho, pval = spearmanr(xs, ys)
        diag["D2_courbe_vs_moyenne_cumulee"].append({
            "run": label, "spearman_score_vs_ecart_moyenne_bas": float(rho),
            "p": float(pval), "n_candidats": len(xs)})
        # --- D3 : où est le pic après le swap ?
        courbe_swap = rec.get("A_swap_courbe", [])
        cands_swap = rec.get("A_swap_candidats", [])
        if courbe_swap:
            i_max = int(np.argmax([s if s is not None else -1
                                   for s in courbe_swap]))
            pic_swap = cands_swap[i_max]
            # candidat correspondant à la nouvelle position de B (lignes m0..m1)
            cand_B_new = float(cands_swap[int(np.argmin(
                np.abs(np.array(cands_swap) - winp[m0])))])
            diag["D3_pic_apres_swap"].append({
                "run": label, "vieux_seuil": thr,
                "nouveau_pic": pic_swap,
                "candidat_position_B_apres_swap": cand_B_new,
                "distance_nouveau_pic_vieux_seuil": abs(pic_swap - thr),
                "distance_nouveau_pic_position_B": abs(pic_swap - cand_B_new),
                "pic_suit_B": bool(abs(pic_swap - cand_B_new) <= 2 * 100.0 / (ncand - 1) + 1e-9),
                "pic_reste_position": bool(abs(pic_swap - thr) <= 2 * 100.0 / (ncand - 1) + 1e-9)})
    out["diagnostics_posthoc"] = diag
    n_d1 = sum(1 for d in diag["D1_winsorise_M"] if d["tue_le_pic"])
    print(f"[DIAG] D1 winsorise M tue le pic : {n_d1}/{len(diag['D1_winsorise_M'])}")
    for d in diag["D2_courbe_vs_moyenne_cumulee"]:
        print(f"[DIAG] D2 {d['run']}: Spearman={d['spearman_score_vs_ecart_moyenne_bas']:.3f}")
    for d in diag["D3_pic_apres_swap"]:
        print(f"[DIAG] D3 {d['run']}: vieux={d['vieux_seuil']:.2f} "
              f"nouveau={d['nouveau_pic']:.2f} posB={d['candidat_position_B_apres_swap']:.2f} "
              f"suit_B={d['pic_suit_B']} reste={d['pic_reste_position']}")
    return diag



# ------------------------------------------------------------------ DIAG2
# POST-HOC (hors protocole gelé — suite des diagnostics). Teste si la
# robustesse est un interrupteur à seuil (knife-edge) : (D5) winsoriser
# UNE ligne au hasard (3 graines fixes) tue-t-elle le pic aussi souvent
# que winsoriser la ligne la plus extrême (A2) ? (D6) un bruit
# numérique infime (arrondi 6 décimales ; bruit gaussien 1e-3 et 1e-2
# de l'écart-type du flux, graines fixes) fait-il basculer rob ?
def stage_diag2(v62, out):
    diag2 = {"D5_ligne_aleatoire": [], "D6_poussiere": []}
    interv = out.get("interventions", {}).get("robon", [])
    prog_cache = {}

    def prog_of(n):
        if n not in prog_cache:
            prog_cache[n] = progress_axis(v62, n)
        return prog_cache[n]

    for rec in interv:
        label = rec["run"]
        csv_file = rec["csv"]
        ncand, w, mingrp = rec["config_gagnante"]
        thr = rec["seuil_pic"]
        rob_old = rec["rob_stockee"]
        mat, cols, df = load_mat(csv_file)
        n = len(mat)
        prog, cfg = prog_of(n)
        _, z, med = row_extremity(mat)
        sd = np.std(mat, axis=0)
        # --- D5 : 3 lignes au hasard (graines fixes 1000-1002)
        d5 = {"run": label, "lignes": [], "n_tue": 0}
        rng = np.random.default_rng(1000)
        for _ in range(3):
            r_alea = int(rng.integers(0, n))
            mat_r = mat.copy()
            mat_r[r_alea] = med
            _, _, met_r = scan_replica(
                v62, mat_r, cols, prog, cfg, w, mingrp, ncand)
            tue = bool(met_r["robustness"] < 0.1)
            d5["lignes"].append({"ligne": r_alea,
                                 "rob_nouvelle": met_r["robustness"],
                                 "tue_le_pic": tue})
            d5["n_tue"] += int(tue)
        diag2["D5_ligne_aleatoire"].append(d5)
        # --- D6 : poussière numérique
        d6 = {"run": label, "variantes": []}
        # (a) arrondi à 6 décimales
        mat_a = np.round(mat, 6)
        _, _, met_a = scan_replica(
            v62, mat_a, cols, prog, cfg, w, mingrp, ncand)
        d6["variantes"].append({"nom": "arrondi_6dec",
                                "rob_nouvelle": met_a["robustness"],
                                "maxsep_nouvelle": met_a["max_separation"],
                                "bascule": bool(
                                    (rob_old > 0.5) != (met_a["robustness"] > 0.5))})
        # (b) bruit gaussien 1e-3 et 1e-2 sd, graines fixes
        for nom, amp, graine in (("bruit_1e-3", 1e-3, 7),
                                 ("bruit_1e-2", 1e-2, 8)):
            rng_b = np.random.default_rng(graine)
            mat_b = mat + rng_b.normal(0.0, 1.0, size=mat.shape) * (amp * sd)
            _, _, met_b = scan_replica(
                v62, mat_b, cols, prog, cfg, w, mingrp, ncand)
            d6["variantes"].append({"nom": nom,
                                    "rob_nouvelle": met_b["robustness"],
                                    "maxsep_nouvelle": met_b["max_separation"],
                                    "bascule": bool(
                                        (rob_old > 0.5) != (met_b["robustness"] > 0.5))})
        diag2["D6_poussiere"].append(d6)
        print(f"[DIAG2 {label}] D5 aléatoire tue {d5['n_tue']}/3 ; "
              f"D6 bascules: {[(v['nom'], v['bascule'], round(v['rob_nouvelle'], 4)) for v in d6['variantes']]}",
              flush=True)
    out["diagnostics_posthoc2"] = diag2
    tot_d5 = sum(d["n_tue"] for d in diag2["D5_ligne_aleatoire"])
    n_d5 = 3 * len(diag2["D5_ligne_aleatoire"])
    basc = {}
    for v_nom in ("arrondi_6dec", "bruit_1e-3", "bruit_1e-2"):
        basc[v_nom] = sum(1 for d in diag2["D6_poussiere"]
                          for v in d["variantes"]
                          if v["nom"] == v_nom and v["bascule"])
    print(f"[DIAG2-BILAN] D5 lignes aléatoires tuent {tot_d5}/{n_d5} ; "
          f"D6 bascules {basc} / {len(diag2['D6_poussiere'])} courbes")
    return diag2

if __name__ == "__main__":
    main()
