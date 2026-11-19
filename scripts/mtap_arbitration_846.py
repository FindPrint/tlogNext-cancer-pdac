#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.46 — Arbitrage de la contradiction MTAP (S_sep contre MC/Delta).
Protocole gelé : PROTOCOL_mtap_arbitration_ssep.md (écrit avant ce script).
Lecture seule des sorties existantes + 2 nuls frais (graines 7/123, runs
v6.2 lancés par systemd-run, unité mtap-nuls846) + tests directs depuis
les sources déjà détenues. Aucun code de pipeline modifié, aucun seuil
choisi après coup, aucune imputation, aucune valeur inventée.
Ce qui vient DU PIPELINE : cascade, best_config + métriques, Delta et
D-vector, L7a, falsification, scan_curve, 12 itérations MC, courbe par
défaut. Ce qui est APPORTÉ (harnais) : recomposition du MC composite,
FWHM recalculée, d de Cohen par flux aux seuils lus, groupes GISTIC,
Spearman, tests directs DepMap/TCGA avec contrôle prolifération.
Sorties : mtap_arbitration_846_results.csv,
mtap_arbitration_846_extract.json, mtap_arbitration_846_prolif.csv.
"""
import ast
import hashlib
import json
import math
import os
import tarfile

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr

PDAC = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(PDAC, "data")
FLUXES = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20", "MUC2",
          "GSTM1", "CEACAM5", "CLCA1", "MUC16"]
PROLIF_GENES = ["MKI67", "TOP2A", "PCNA", "CCNB1"]
ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]
ISLET = ["INS", "GCG", "PPY", "SST"]
V62 = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
V62_SHA = "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"
MTAP_CSV_SHA = "578b8d3b9b26099d0784ed23754d1cc9717be7f9292eb47e201d186cdbc90df6"
MTAP_NUL_SHA = "e6786a47ce107dbf9785d83981ab413f8afb4e75fbdbae4da56da8c1e46453b9"
W = 20  # demi-fenêtre autour d'un seuil (même convention que mtap_reading.py)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    sp = np.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1))
                 / (len(a) + len(b) - 2))
    return float((b.mean() - a.mean()) / sp) if sp > 0 else float("nan")


def partial_spearman(x, y, z):
    """Spearman partiel x~y en contrôlant z (rangs, résidus de régression OLS).
    z : un vecteur, ou une liste de vecteurs (contrôle multiple).
    Retourne (rho, p approx par test t sur les résidus, n)."""
    def ranks(v):
        return pd.Series(v).rank().to_numpy(float)
    rx, ry = ranks(x), ranks(y)
    zs = z if isinstance(z, (list, tuple)) else [z]
    rzs = [ranks(v) for v in zs]
    ok = np.isfinite(rx) & np.isfinite(ry)
    for rz in rzs:
        ok &= np.isfinite(rz)
    rx, ry = rx[ok], ry[ok]
    rzs = [rz[ok] for rz in rzs]
    n = len(rx)
    if n < 5:
        return float("nan"), float("nan"), n
    Z = np.column_stack([np.ones(n)] + rzs)
    k = Z.shape[1] - 1
    bx, *_ = np.linalg.lstsq(Z, rx, rcond=None)
    by, *_ = np.linalg.lstsq(Z, ry, rcond=None)
    ex, ey = rx - Z @ bx, ry - Z @ by
    if np.std(ex) == 0 or np.std(ey) == 0:
        return float("nan"), float("nan"), n
    r = float(np.corrcoef(ex, ey)[0, 1])
    if abs(r) >= 1.0:
        return r, 0.0, n
    from scipy.stats import t as tdist
    dof = n - 2 - k
    if dof < 1:
        return r, float("nan"), n
    t = r * np.sqrt(dof / (1 - r * r))
    p = float(2 * tdist.sf(abs(t), dof))
    return r, p, n


# ---------------------------------------------------------------- A. Relecture
RUNS = {
    "RÉEL": "results_fast_v62_mtap",
    "NUL42": "results_fast_v62_mtap_nul",
    "NUL_S7": "results_fast_v62_mtap_nul_s7",
    "NUL_S123": "results_fast_v62_mtap_nul_s123",
}


def read_run(d):
    r = json.load(open(os.path.join(PDAC, d, "master_results.json")))
    tm = g(r, "run_pipeline.threshold_metadata.threshold_optimization", {}) or {}
    bc = tm.get("best_config", {}) or {}
    m = bc.get("metrics", {}) or {}
    l7 = g(r, "prediction_levels.L7a_coherence", {}) or {}
    holo = g(r, "holographic_tension_state", {}) or {}
    casc = [fnum(g(r, "five_threshold_cascade." + k)) for k in
            ["T_-2_F2_pre_onset", "T_-1_F1_pre_inflection",
             "T_0_Monte_Carlo_Central", "T_+1_F1_post_deceleration",
             "T_+2_F2_post_attractor"]]
    # Recomposition du MC composite (poids par défaut, code lignes 3727-3730
    # et 3481-3484) : 0,3*s_norm + 0,3*stabilité + 0,2*robustesse + 0,2*acuité.
    mc_recomp = None
    if all(m.get(k) is not None for k in
           ("s_norm", "stability", "robustness", "sharpness")):
        mc_recomp = (0.3 * m["s_norm"] + 0.3 * m["stability"]
                     + 0.2 * m["robustness"] + 0.2 * m["sharpness"])
    # Les 12 itérations MC (relecture de all_results, chaîne repr).
    iters = []
    try:
        raw = tm.get("all_results")
        arr = ast.literal_eval(raw) if isinstance(raw, str) else raw
        for it in arr:
            iters.append({"iteration": it.get("iteration"),
                          "rule": it.get("rule"),
                          "n_candidates": it.get("n_candidates"),
                          "w_size": it.get("w_size"),
                          "min_grp": it.get("min_grp"),
                          "threshold": fnum(it.get("threshold")),
                          "score": fnum(it.get("score")),
                          "maxsep": fnum(g(it, "metrics.max_separation")),
                          "s_norm": fnum(g(it, "metrics.s_norm")),
                          "stability": fnum(g(it, "metrics.stability")),
                          "robustness": fnum(g(it, "metrics.robustness")),
                          "sharpness": fnum(g(it, "metrics.sharpness"))})
    except Exception as e:  # noqa: BLE001 — consigné, pas silencieux
        print(f"  !! all_results illisible pour {d} : {e}")
    # Courbe par défaut (paramètres fixes, mêmes des deux côtés) : max lu.
    def curve_max(key):
        try:
            arr = ast.literal_eval(tm[key]) if isinstance(tm.get(key), str) \
                else tm.get(key)
            sc = [(s["candidate"], s["score"]) for s in arr
                  if s.get("score") is not None]
            if not sc:
                return None, None, None
            c, s = max(sc, key=lambda t: t[1])
            return float(c), float(s), len(sc)
        except Exception:  # noqa: BLE001
            return None, None, None
    dc, ds, dn = curve_max("default_scan_curve")
    return {
        "dir": d, "version": r.get("version"), "n": fnum(g(r, "reading_synthesis.n_samples")),
        "cascade_pct": casc,
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
        "l7a_dir": l7.get("consensus_direction"),
        "l7a_conf": fnum(l7.get("global_confidence")),
        "fals": fnum(g(holo, "falsification_vs_null.delta_vs_null")),
        "regime": g(r, "reading_synthesis.dominant_regime"),
        "iterations": iters,
        "default_thr": dc, "default_maxsep": ds, "default_n_scored": dn,
        "per_estimator": holo.get("per_estimator") or {},
    }


# ---------------------------------------------------------------- B. Forme du scan
def scan_shape(d):
    """Réplique evaluate_scan_quality (code lignes 3314-3390) sur la
    scan_curve.json du run : max, FWHM, robustesse, stabilité, acuité."""
    sc = json.load(open(os.path.join(PDAC, d, "scan_curve.json")))
    scored = [(s["candidate"], s["score"]) for s in sc if s.get("score") is not None]
    cands = np.array([c for c, _ in scored], float)
    scores = np.array([s for _, s in scored], float)
    if len(scores) < 3:
        return {"n_scored": len(scores)}
    max_idx = int(np.argmax(scores))
    max_sep = float(scores[max_idx])
    win = max(3, len(scores) // 20)
    lo = max(0, max_idx - win)
    hi = min(len(scores), max_idx + win)
    local = scores[lo:hi]
    stability = float(1.0 / (1.0 + np.std(local))) if len(local) > 1 else 0.0
    half = max_sep / 2.0
    li = max_idx
    while li > 0 and scores[li] >= half:
        li -= 1
    ri = max_idx
    while ri < len(scores) - 1 and scores[ri] >= half:
        ri += 1
    fwhm = float(cands[ri] - cands[li])
    robustness = float(np.exp(-((fwhm - 10.0) ** 2) / (2 * 5.0 ** 2)))
    dx = np.diff(cands)
    ds = np.diff(scores)
    valid = dx > 1e-6
    sharp = 0.0
    if np.any(valid):
        derivs = np.abs(ds[valid] / dx[valid])
        loc = derivs[max(0, max_idx - win):min(len(derivs), max_idx + win)]
        sharp = float(np.tanh(float(np.max(loc)) / 0.5)) if len(loc) else 0.0
    above = int((scores >= half).sum())
    return {"n_scored": len(scores), "n_candidates": len(sc),
            "max_cand": float(cands[max_idx]), "max_score": max_sep,
            "stability_recalc": stability, "fwhm_pct": fwhm,
            "robustness_recalc": robustness, "sharpness_recalc": sharp,
            "n_above_half": above, "frac_above_half": above / len(scores),
            "score_first": float(scores[0]), "score_last": float(scores[-1]),
            "score_median": float(np.median(scores)),
            "cand_first": float(cands[0]), "cand_last": float(cands[-1])}


def main():
    print("=== §8.46 — vérifications d'entrée ===")
    assert sha(V62) == V62_SHA, "SHA v6.2 non conforme"
    assert sha(os.path.join(PDAC, "pdac_tcga_fluxes_v4_mtap.csv")) == MTAP_CSV_SHA
    assert sha(os.path.join(PDAC, "pdac_tcga_fluxes_v4_mtap_nul.csv")) == MTAP_NUL_SHA
    print("SHA v6.2, CSV réel, CSV nul graine 42 : conformes.")
    extr = {}
    for tag, d in RUNS.items():
        p = os.path.join(PDAC, d, "master_results.json")
        if not os.path.exists(p):
            print(f"--- {tag} ({d}) : ABSENT (run non terminé ?)")
            extr[tag] = None
            continue
        extr[tag] = read_run(d)
        e = extr[tag]
        print(f"--- {tag} ({d}) ---")
        print(f"  version={e['version']} n={e['n']} règle={e['rule']} "
              f"n_cand={e['n_candidates']} w={e['w_size']} min_grp={e['min_grp']}")
        print(f"  cascade % : {[None if c is None else round(c, 2) for c in e['cascade_pct']]}")
        print(f"  MC lu={e['mc_score']} recomposé={e['mc_recomp']} "
              f"écart={e['mc_ecart_recomp']} seuil={e['mc_thr']}")
        print(f"  maxsep={e['maxsep']} s_norm={e['s_norm']} stab={e['stability']} "
              f"rob={e['robustness']} acu={e['sharpness']} S_sep={e['ssep']}")
        print(f"  Delta={e['delta']} D={e['d_vector']} L7a={e['l7a_dir']} "
              f"{e['l7a_conf']} fals={e['fals']} régime={e['regime']}")
        print(f"  défaut : thr={e['default_thr']} maxsep={e['default_maxsep']} "
              f"n_scored={e['default_n_scored']}")
        sh = scan_shape(d)
        e["scan_shape"] = sh
        print(f"  scan : n_scored={sh['n_scored']} max@{sh['max_cand']:.2f}% "
              f"={sh['max_score']:.4f} FWHM={sh['fwhm_pct']:.2f}% "
              f"rob_recalc={sh['robustness_recalc']:.3e} "
              f"stab_recalc={sh['stability_recalc']:.4f} acu_recalc={sh['sharpness_recalc']:.4f} "
              f"au-dessus_moitié={sh['n_above_half']}/{sh['n_scored']} "
              f"médiane={sh['score_median']:.4f}")
        its = e["iterations"]
        if its:
            print(f"  12 itérations MC : scores "
                  f"{[round(i['score'], 4) if i['score'] is not None else None for i in its]}")
            print(f"    maxsep par itération : "
                  f"{[round(i['maxsep'], 4) if i['maxsep'] is not None else None for i in its]}")
            print(f"    robustesse par itération : "
                  f"{[('%.2e' % i['robustness']) if i['robustness'] is not None else None for i in its]}")
    with open(os.path.join(PDAC, "mtap_arbitration_846_extract.json"), "w",
              encoding="utf-8") as f:
        json.dump({"extraction": extr}, f, indent=2, ensure_ascii=False)
    print("Écrit (partiel) : mtap_arbitration_846_extract.json")

    # ---------------------------------------------------------------- C/D/F
    rows_out, prolif_rows = [], []
    patients = rebuild_patients()  # (T) jointure exacte par code-barres
    c_rows = per_flux_reading(extr, patients)
    rows_out.extend(c_rows)
    d_rows = delta_decomposition(extr)
    rows_out.extend(d_rows)
    f_rows, f_prolif = depmap_tests()
    rows_out.extend(f_rows)
    prolif_rows.extend(f_prolif)
    f3_rows = tcga_prolif_tests(patients)
    rows_out.extend(f3_rows)
    prolif_rows.extend([r for r in f3_rows if "prolif" in r.get("test", "")])
    f4_rows = reread_confirmations()
    rows_out.extend(f4_rows)
    with open(os.path.join(PDAC, "mtap_arbitration_846_extract.json"), "w",
              encoding="utf-8") as f:
        json.dump({"extraction": extr, "patients_sha":
                   sha(os.path.join(PDAC, "mtap_arbitration_846_patients.csv")),
                   "per_flux": c_rows, "delta": d_rows,
                   "depmap": f_rows, "tcga_prolif": f3_rows,
                   "confirmations_relues": f4_rows}, f, indent=2,
                  ensure_ascii=False)
    pd.DataFrame(rows_out).to_csv(
        os.path.join(PDAC, "mtap_arbitration_846_results.csv"), index=False)
    pd.DataFrame(prolif_rows).to_csv(
        os.path.join(PDAC, "mtap_arbitration_846_prolif.csv"), index=False)
    print("Écrit : mtap_arbitration_846_extract.json, "
          "mtap_arbitration_846_results.csv, mtap_arbitration_846_prolif.csv")
    print(f"SHA script : {sha(__file__)}")
    return extr


# ---------------------------------------------------------------- C. Loupe par loupe
def split_d(df, pas, window=None):
    """d de Cohen par flux, après - avant, à un pas donné.
    window=None : partage entier pré/post ; window=W : fenêtres ±W."""
    n = len(df)
    out = {}
    for flux in FLUXES:
        v = df[flux].to_numpy(float)
        if window is None:
            before, after = v[:pas], v[pas:]
        else:
            lo, hi = max(0, pas - window), min(n, pas + window)
            before, after = v[lo:pas], v[pas:hi]
        out[flux] = cohen_d(before, after) if len(before) >= 2 and len(after) >= 2 else float("nan")
    return out


def per_flux_reading(extr, patients):
    real = pd.read_csv(os.path.join(PDAC, "pdac_tcga_fluxes_v4_mtap.csv"))
    nul = pd.read_csv(os.path.join(PDAC, "pdac_tcga_fluxes_v4_mtap_nul.csv"))
    n = len(real)
    rows = []
    for tag, df in (("RÉEL", real), ("NUL42", nul)):
        e = extr[tag]
        pas_mc = int(round(e["mc_thr"] / 100 * (n - 1)))
        pas_max = int(round(e["scan_shape"]["max_cand"] / 100 * (n - 1)))
        for nom_pas, pas in (("MC", pas_mc), ("MAX", pas_max)):
            for nom_fen, win in (("entier", None), ("+-20", W)):
                d = split_d(df, pas, win)
                vals = np.array([abs(d[f]) for f in FLUXES if np.isfinite(d[f])])
                srt = np.sort(vals)[::-1]
                cum = np.cumsum(srt) / srt.sum() if srt.sum() > 0 else srt
                n80 = int((cum < 0.80).sum() + 1) if srt.sum() > 0 else None
                top = FLUXES[int(np.argmax([abs(d[f]) for f in FLUXES]))]
                print(f"--- C1 {tag} seuil {nom_pas} (pas {pas}) fenêtre {nom_fen} : "
                      f"moy|d|={vals.mean():.4f} top={top} "
                      f"|d|={max(vals):.3f} part_top={max(vals)/vals.sum():.2f} "
                      f"flux_pour_80%={n80}")
                print(f"    d par flux : "
                      + ", ".join(f"{f}:{d[f]:+.3f}" for f in FLUXES))
                for f in FLUXES:
                    rows.append({"test": f"C1_{nom_pas}_{nom_fen}", "série": tag,
                                 "flux": f, "pas": pas, "d": round(float(d[f]), 4),
                                 "abs_d": round(float(abs(d[f])), 4)})
                rows.append({"test": f"C1_{nom_pas}_{nom_fen}_SYNTH", "série": tag,
                             "flux": "MOYENNE_abs_d",
                             "pas": pas, "d": round(float(vals.mean()), 4),
                             "abs_d": round(float(vals.mean()), 4)})
    # C2 : groupes GISTIC (jointure exacte, patients) — d par flux.
    gistic = patients["mtap_gistic"].to_numpy()
    for nom_groupe, mask_del, mask_int in (
            ("GISTIC_-2_vs_reste", gistic == -2, gistic != -2),
            ("GISTIC_-2_-1_vs_0_+", np.isin(gistic, [-2, -1]), np.isin(gistic, [0, 1, 2])),
            ("TOP12_vs_reste", np.arange(n) < 12, np.arange(n) >= 12)):
        print(f"--- C2 {nom_groupe} : n_dél={int(mask_del.sum())} "
              f"n_int={int(mask_int.sum())}")
        for tag, df in (("RÉEL", real), ("NUL42", nul)):
            ds = {}
            for f in FLUXES:
                v = df[f].to_numpy(float)
                ds[f] = cohen_d(v[mask_int], v[mask_del])
            print(f"    {tag} : " + ", ".join(f"{f}:{ds[f]:+.3f}" for f in FLUXES))
            for f in FLUXES:
                rows.append({"test": f"C2_{nom_groupe}", "série": tag, "flux": f,
                             "pas": None, "d": round(float(ds[f]), 4),
                             "abs_d": round(float(abs(ds[f])), 4)})
    # C3 : Spearman flux contre rang MTAP.
    for tag, df in (("RÉEL", real), ("NUL42", nul)):
        rhos = {}
        for f in FLUXES:
            rho, p = spearmanr(np.arange(n), df[f].to_numpy(float))
            rhos[f] = (float(rho), float(p))
        print(f"--- C3 Spearman vs rang MTAP {tag} : "
              + ", ".join(f"{f}:{rhos[f][0]:+.3f}(p={rhos[f][1]:.2g})" for f in FLUXES))
        for f in FLUXES:
            rows.append({"test": "C3_spearman_rang", "série": tag, "flux": f,
                         "pas": None, "d": round(rhos[f][0], 4),
                         "abs_d": round(abs(rhos[f][0]), 4)})
    return rows


# ---------------------------------------------------------------- D. Delta
DIM_TLOG = {
    "saturation": ["Higuchi", "Katz", "Petrosian", "Sevcik", "BoxCounting",
                   "Hurst2mH", "DFA"],
    "criticality": ["CorrelationD2", "GrassbergerProcaccia", "InformationD1",
                    "VisibilityGraph", "TwoNN", "DANCo", "Fisher"],
    "divergence": ["LevinaBickel", "PCAIntrinsic", "LocalPCA", "GraphDimension",
                   "PersistentHomology", "MFA"],
    "null_reference": ["SpectralDimension"],
}


def delta_decomposition(extr):
    rows = []
    r, nn = extr["RÉEL"], extr["NUL42"]
    print(f"--- D D-vector RÉEL {r['d_vector']} NUL42 {nn['d_vector']}")
    print("    (Correction de lecture : d_sat/d_div sont des médianes BRUTES "
          "de dimensions — médiane des médianes par estimateur — et non "
          "des médianes T_log ; Delta = d_div - d_sat en unités de "
          "dimension brutes. Le protocole §1 disait T_log : c'est faux, "
          "corrigé ici d'après le code, lignes ~7990-8022.)")
    for cls, names in DIM_TLOG.items():
        diffs = []
        for name in names:
            mr = fnum(g(r["per_estimator"], f"{name}.raw_median"))
            mn = fnum(g(nn["per_estimator"], f"{name}.raw_median"))
            if mr is None or mn is None:
                print(f"    {cls}/{name} : médiane manquante")
                continue
            diffs.append((name, mr, mn, mr - mn))
            rows.append({"test": "D_per_estimateur", "série": f"{cls}/{name}",
                         "flux": name, "pas": None,
                         "d": round(mr - mn, 4), "abs_d": round(abs(mr - mn), 4)})
        dkey = {"saturation": "d_sat", "criticality": "d_crit",
                "divergence": "d_div", "null_reference": "d_null"}[cls]
        med_r = float(np.median([t[1] for t in diffs])) if diffs else None
        med_n = float(np.median([t[2] for t in diffs])) if diffs else None
        print(f"    {cls} : médiane brutes RÉEL={med_r:.4f} (D lu "
              f"{r['d_vector'].get(dkey)}) / NUL42={med_n:.4f} (D lu "
              f"{nn['d_vector'].get(dkey)}) ; écarts par estimateur : "
              + ", ".join(f"{t[0]}:{t[3]:+.3f}" for t in diffs))
    return rows


# ---------------------------------------------------------------- (T) Patients
def rebuild_patients():
    """Jointure exacte par code-barres : RSEM (résidus v4 + score prolif)
    et GISTIC (CN MTAP continu + seuillé). Vérifie la reproduction du CSV
    v4 (atol 1e-9), de la colonne MTAPCN du CSV MTAP, et du score prolif
    trié contre pdac_tcga_fluxes_v4_prolif.csv. Écrit la table patients."""
    out_path = os.path.join(PDAC, "mtap_arbitration_846_patients.csv")
    tarball = os.path.join(DATA, "tcga_paad_rsem.tar.gz")
    gistic_tb = os.path.join(DATA, "tcga_paad_gistic.tar.gz")
    gistic_dir = ("gdac.broadinstitute.org_PAAD-TP.CopyNumber_Gistic2."
                  "Level_4.2016012800.0.0")
    with tarfile.open(tarball, "r:gz") as tf:
        member = [m for m in tf.getmembers() if m.name.endswith(".data.txt")][0]
        df = pd.read_csv(tf.extractfile(member), sep="\t", index_col=0,
                         low_memory=False)
    df.index = df.index.to_series().str.split("|").str[0]
    df = df[~df.index.duplicated(keep="first")]
    cols = df.columns.to_series()
    tumor_cols = cols[cols.str[13:15] == "01"]
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    mat = mat[~mat.isna().any(axis=1)]
    logmat = np.log2(mat + 1.0)
    score_ac = logmat.loc[[g for g in ACINAR if g in logmat.index]].median(axis=0)
    score_is = logmat.loc[[g for g in ISLET if g in logmat.index]].median(axis=0)
    X = np.column_stack([np.ones(len(logmat.columns)), score_ac.values,
                         score_is.values])
    beta, *_ = np.linalg.lstsq(X, logmat.values.T, rcond=None)
    resid = logmat.values - (X @ beta).T
    resid_df = pd.DataFrame(resid, index=logmat.index, columns=logmat.columns)
    v4 = pd.read_csv(os.path.join(PDAC, "pdac_tcga_fluxes_v4.csv"))
    flux_cols = list(v4.columns[1:])
    kras_res = resid_df.loc["KRAS"].sort_values(ascending=True)
    order_kras = list(kras_res.index)
    recomputed = resid_df.loc[flux_cols, order_kras].T.reset_index(drop=True)
    max_diff = float(np.abs(recomputed.values - v4[flux_cols].values).max())
    print(f"--- (T) reproduction v4 : écart max = {max_diff:.3e} (atol 1e-9)")
    assert max_diff <= 1e-9, "reproduction v4 ÉCHOUÉE"
    prolif_res = resid_df.loc[PROLIF_GENES].median(axis=0)
    prolif_csv = pd.read_csv(os.path.join(PDAC, "pdac_tcga_fluxes_v4_prolif.csv"))
    assert np.allclose(np.sort(prolif_res.to_numpy()),
                       np.sort(prolif_csv["PROLIF"].to_numpy()), atol=1e-9), \
        "score prolif non reproduit"
    print("--- (T) score prolifération reproduit (tri, atol 1e-9).")
    with tarfile.open(gistic_tb, "r:gz") as tf:
        cont = pd.read_csv(tf.extractfile(f"{gistic_dir}/all_data_by_genes.txt"),
                           sep="\t", index_col=0, low_memory=False)
        thr = pd.read_csv(tf.extractfile(f"{gistic_dir}/all_thresholded.by_genes.txt"),
                          sep="\t", index_col=0, low_memory=False)
    mtap_cont = cont.loc["MTAP"].drop(index=["Locus ID", "Cytoband"], errors="ignore")
    mtap_thr = thr.loc["MTAP"].drop(index=["Locus ID", "Cytoband"], errors="ignore")
    patient = lambda bc: str(bc)[:15]  # noqa: E731
    rsem_patients = {patient(c): c for c in resid_df.columns}
    gistic_patients = {patient(c): c for c in mtap_cont.index}
    common = sorted(set(rsem_patients) & set(gistic_patients))
    print(f"--- (T) patients communs RSEM/GISTIC : {len(common)}/178 ; "
          f"sans GISTIC : {sorted(set(rsem_patients) - set(gistic_patients))}")
    mtap_cn = pd.Series({rsem_patients[p]: float(mtap_cont[gistic_patients[p]])
                         for p in common})
    mtap_thr_s = pd.Series({rsem_patients[p]: int(mtap_thr[gistic_patients[p]])
                            for p in common})
    order_mtap = list(mtap_cn.sort_values(ascending=True).index)
    mtap_csv = pd.read_csv(os.path.join(PDAC, "pdac_tcga_fluxes_v4_mtap.csv"))
    assert np.allclose(mtap_cn.loc[order_mtap].to_numpy(),
                       mtap_csv["MTAPCN"].to_numpy(), atol=1e-12), \
        "colonne MTAPCN non reproduite"
    print("--- (T) colonne MTAPCN reproduite exactement (atol 1e-12) ; "
          f"GISTIC seuillé sur 177 : {mtap_thr_s.value_counts().sort_index().to_dict()}")
    tab = pd.DataFrame({
        "barcode": order_mtap,
        "patient15": [patient(c) for c in order_mtap],
        "mtap_cn": mtap_cn.loc[order_mtap].to_numpy(),
        "mtap_gistic": mtap_thr_s.loc[order_mtap].to_numpy(),
        "prolif_score": prolif_res.loc[order_mtap].to_numpy(),
    })
    tab.to_csv(out_path, index=False)
    print(f"--- (T) écrit : {out_path} ({len(tab)} lignes)")
    return tab


# ---------------------------------------------------------------- F. DepMap
def depmap_tests():
    rows = []
    ge_path = os.path.join(DATA, "CRISPRGeneEffect.csv")
    cn_path = os.path.join(DATA, "OmicsCNGene.csv")
    model_path = os.path.join(DATA, "Model.csv")
    for p, exp in ((ge_path, "3d8f3ec6dbf2db7ff834b79b508622ec0b226f3518003fe96ecf5a4fcf167e3b"),
                   (cn_path, "4851d3e939d48837a39a0f01294deb90fa507a85703586a927b77474f999134c"),
                   (model_path, "b7a0c1385e6cef30132b56aff61f1261d11e3f490490b355c430d32ee0dbdcfa")):
        assert sha(p) == exp, f"SHA non conforme : {p}"
    print("--- F SHA DepMap 24Q4 (GeneEffect, CN, Model) : conformes.")
    cols_ge = ["PRMT5 (10419)", "KRAS (3845)", "MKI67 (4288)", "TOP2A (7153)",
               "PCNA (5111)", "CCNB1 (891)", "CDKN2A (1029)", "ACTB (60)"]
    def read_wide(path, wanted):
        """Lit un fichier DepMap large en ne gardant que les colonnes
        voulues (+ la 1re colonne = ModelID, en-tête vide). ATTENTION :
        pandas rend les colonnes dans l'ordre DU FICHIER, pas dans
        l'ordre de usecols — on renomme donc PAR LE NOM, jamais par
        position (piège attrapé le 19 nov. : un renommage positionnel
        échangeait PRMT5 et ACTB et inversait le test F1)."""
        header = pd.read_csv(path, nrows=0).columns.tolist()
        idx = [0] + [header.index(c) for c in wanted]
        d = pd.read_csv(path, usecols=idx, index_col=0)
        # d.columns est dans l'ordre du fichier : on vérifie chaque nom.
        assert sorted(d.columns.tolist()) == sorted(wanted), \
            f"colonnes lues {d.columns.tolist()} != voulues {wanted}"
        return d.reset_index().rename(columns={"index": "ModelID"})
    ge = read_wide(ge_path, cols_ge)
    ge = ge.rename(columns={"PRMT5 (10419)": "PRMT5", "KRAS (3845)": "KRAS",
                            "MKI67 (4288)": "MKI67", "TOP2A (7153)": "TOP2A",
                            "PCNA (5111)": "PCNA", "CCNB1 (891)": "CCNB1",
                            "CDKN2A (1029)": "CDKN2A", "ACTB (60)": "ACTB"})
    cn = read_wide(cn_path, ["MTAP (4507)", "CDKN2A (1029)"])
    cn = cn.rename(columns={"MTAP (4507)": "CN_MTAP",
                            "CDKN2A (1029)": "CN_CDKN2A"})
    model = pd.read_csv(model_path, usecols=["ModelID", "OncotreeLineage"])
    pan = model[model["OncotreeLineage"] == "Pancreas"]
    d = pan.merge(ge, on="ModelID", how="inner").merge(cn, on="ModelID", how="inner")
    d = d.dropna(subset=["PRMT5", "CN_MTAP"])
    print(f"--- F1 lignées pancréas jointes : n={len(d)} "
          f"(attendu 47 : 45 adénocarcinomes + 2 adénosquameux)")
    assert len(d) == 47, f"n pancréas = {len(d)}, attendu 47"
    # Vérification croisée ligne à ligne contre la table §8.40 (indépendante).
    ref = pd.read_csv(os.path.join(PDAC, "mtap_arbitration_840_pancreas_lines.csv"))
    chk = d.merge(ref[["ModelID", "MTAP_CN", "PRMT5"]], on="ModelID",
                  suffixes=("", "_ref"))
    assert len(chk) == 47, "jointure de vérification incomplète"
    e_cn = float(np.abs(chk["CN_MTAP"] - chk["MTAP_CN"]).max())
    e_pr = float(np.abs(chk["PRMT5"] - chk["PRMT5_ref"]).max())
    print(f"--- F1 vérification vs table §8.40 : écart max CN MTAP={e_cn:.2e}, "
          f"PRMT5={e_pr:.2e} (seuil 1e-6 : arrondi d'écriture de la table)")
    assert e_cn <= 1e-6 and e_pr <= 1e-6, "ÉCART vs table §8.40 — ARRÊT"
    dele = d["CN_MTAP"] < 0.5
    med_d = float(d.loc[dele, "PRMT5"].median())
    med_i = float(d.loc[~dele, "PRMT5"].median())
    u, p = mannwhitneyu(d.loc[dele, "PRMT5"], d.loc[~dele, "PRMT5"],
                        alternative="two-sided")
    rho, pr = spearmanr(d["CN_MTAP"], d["PRMT5"])
    print(f"--- F1 PRMT5 pancréas CN<0,5 : délétées n={int(dele.sum())} "
          f"méd={med_d:.3f} / intactes n={int((~dele).sum())} méd={med_i:.3f} "
          f"p={p:.4g} ; Spearman rho={rho:.3f} p={pr:.3g} "
          f"(attendus §8.40 : -1,385 / -1,010, p=0,0036, rho=+0,497)")
    rows.append({"test": "F1_PRMT5_pancreas_profond", "série": "DepMap24Q4",
                 "flux": "PRMT5", "pas": None, "d": round(med_d - med_i, 4),
                 "abs_d": round(abs(med_d - med_i), 4)})
    # F2 : contrôle prolifération (proxy Chronos) et contrôle KRAS.
    d["prolif_proxy"] = d[["MKI67", "TOP2A", "PCNA", "CCNB1"]].median(axis=1)
    n_nan = int(d["prolif_proxy"].isna().sum())
    print(f"--- F2 proxy prolif (médiane Chronos MKI67/TOP2A/PCNA/CCNB1) : "
          f"NaN={n_nan} sur {len(d)} ; médiane proxy={d['prolif_proxy'].median():.3f}")
    rho_raw, p_raw = spearmanr(d["CN_MTAP"], d["PRMT5"])
    rho_p, p_p, n_p = partial_spearman(d["CN_MTAP"], d["PRMT5"], d["prolif_proxy"])
    rho_k, p_k, n_k = partial_spearman(d["CN_MTAP"], d["PRMT5"], d["KRAS"])
    rho_pk, p_pk, n_pk = partial_spearman(d["CN_MTAP"], d["PRMT5"],
                                          [d["prolif_proxy"], d["KRAS"]])
    print(f"--- F2 Spearman PRMT5~CN MTAP brut rho={rho_raw:.3f} p={p_raw:.3g} ; "
          f"partiel prolif rho={rho_p:.3f} p={p_p:.3g} (n={n_p}) ; "
          f"partiel KRAS rho={rho_k:.3f} p={p_k:.3g} (n={n_k}) ; "
          f"partiel prolif+KRAS rho={rho_pk:.3f} p={p_pk:.3g} (n={n_pk})")
    rows.append({"test": "F2_partiel_prolif", "série": "DepMap24Q4",
                 "flux": "PRMT5", "pas": None, "d": round(rho_p, 4),
                 "abs_d": round(abs(rho_p), 4)})
    rows.append({"test": "F2_partiel_KRAS", "série": "DepMap24Q4",
                 "flux": "PRMT5", "pas": None, "d": round(rho_k, 4),
                 "abs_d": round(abs(rho_k), 4)})
    # CDKN2A fixé (reproduction §8.40, strate MTAP-intacte, par CN).
    sub = d[~dele]
    cd = sub["CN_CDKN2A"] < 0.5
    if cd.sum() >= 2 and (~cd).sum() >= 2:
        u2, p2 = mannwhitneyu(sub.loc[cd, "PRMT5"], sub.loc[~cd, "PRMT5"],
                              alternative="two-sided")
        print(f"--- F2 CDKN2A fixé (MTAP-intacte, par CN) : n={int(cd.sum())}/"
              f"{int((~cd).sum())} méd={sub.loc[cd, 'PRMT5'].median():.3f}/"
              f"{sub.loc[~cd, 'PRMT5'].median():.3f} p={p2:.3g} "
              f"(attendu §8.40 : p=0,46)")
        rows.append({"test": "F2_CDKN2A_fixe_CN_pancreas", "série": "DepMap24Q4",
                     "flux": "PRMT5", "pas": None, "d": round(p2, 4),
                     "abs_d": round(p2, 4)})
    return rows, []


def tcga_prolif_tests(patients):
    rows = []
    n = len(patients)
    rho, p = spearmanr(patients["mtap_cn"], patients["prolif_score"])
    top = patients["prolif_score"].to_numpy()[:12]
    rest = patients["prolif_score"].to_numpy()[12:]
    d_top = cohen_d(rest, top)
    print(f"--- F3 TCGA : Spearman score prolif ~ CN MTAP rho={rho:.3f} p={p:.3g} ; "
          f"d prolif top-12 MTAP vs reste = {d_top:.3f}")
    rows.append({"test": "F3_prolif_spearman_CN", "série": "TCGA",
                 "flux": "PROLIF", "pas": None, "d": round(float(rho), 4),
                 "abs_d": round(abs(float(rho)), 4)})
    rows.append({"test": "F3_prolif_top12_d", "série": "TCGA",
                 "flux": "PROLIF", "pas": None, "d": round(float(d_top), 4),
                 "abs_d": round(abs(float(d_top)), 4)})
    # Partiels flux ~ MTAP en contrôlant la prolif (rangs, données réelles).
    real = pd.read_csv(os.path.join(PDAC, "pdac_tcga_fluxes_v4_mtap.csv"))
    nul = pd.read_csv(os.path.join(PDAC, "pdac_tcga_fluxes_v4_mtap_nul.csv"))
    z = patients["prolif_score"].to_numpy(float)
    x = patients["mtap_cn"].to_numpy(float)
    for tag, df in (("RÉEL", real), ("NUL42", nul)):
        print(f"--- F3 partiels (contrôle prolif) {tag} :")
        for f in FLUXES:
            rho_b, _ = spearmanr(x, df[f].to_numpy(float))
            rho_p, p_p, _ = partial_spearman(x, df[f].to_numpy(float), z)
            print(f"    {f} : brut {rho_b:+.3f} -> partiel {rho_p:+.3f} (p={p_p:.2g})")
            rows.append({"test": "F3_partiel_prolif", "série": tag, "flux": f,
                         "pas": None, "d": round(float(rho_p), 4),
                         "abs_d": round(abs(float(rho_p)), 4)})
    return rows


def reread_confirmations():
    rows = []
    # §8.28 : prmt5_mtap_results.csv (ligne pancréas profond PRMT5).
    r28 = pd.read_csv(os.path.join(DATA, "prmt5_mtap_results.csv"))
    l = r28[(r28["label"] == "pancréas profond") & (r28["gene"] == "PRMT5")].iloc[0]
    print(f"--- F4 §8.28 relu : pancréas profond PRMT5 méd "
          f"{l['med_del']:.3f}/{l['med_int']:.3f} p={l['p']:.4g} "
          f"(attendu -1,385/-1,010 p=0,0036)")
    rows.append({"test": "F4_828_pancreas_profond", "série": "DepMap24Q4",
                 "flux": "PRMT5", "pas": None, "d": round(float(l["p"]), 6),
                 "abs_d": round(float(l["p"]), 6)})
    # §8.29 : stratification CN pan-cancer — relue dans
    # mtap_arbitration_840_results.csv (ligne a3, §8.40).
    r840 = pd.read_csv(os.path.join(PDAC, "mtap_arbitration_840_results.csv"))
    print(f"--- F4 §8.40 (fichier résultats, {len(r840)} lignes) : colonnes "
          f"{list(r840.columns)}")
    for _, row in r840.iterrows():
        lab = str(row.iloc[0])
        if "MTAP-intacte" in lab or "CDKN2A" in lab:
            print(f"    {lab} : {row.to_dict()}")
    # §8.36 : stratification mutation — verify_alleles_mutations.txt.
    txt = open(os.path.join(PDAC, "verify_alleles_mutations.txt"),
               encoding="utf-8", errors="replace").read()
    for line in txt.splitlines():
        if "0.76" in line or "0,76" in line or "stratifi" in line.lower():
            print(f"--- F4 §8.36 (verify_alleles_mutations.txt) : {line.strip()}")
    return rows


if __name__ == "__main__":
    main()
