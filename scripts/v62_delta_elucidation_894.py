#!/usr/bin/env python3
"""§8.94 — Elucider Delta, nouvelle tentative (PROTOCOL_delta_elucidation_894.md).
Lecture seule des sorties detenues. AUCUN run pipeline, AUCUN recalcul
d'estimateur. Ensemble A : 222 runs (v62_delta_levels.csv) ; ensemble B :
31 runs v6.2 (§8.62, results_fast_v62_862_*).
Verification prealable (arret si echec) : identite d_div/d_sat a 1e-3
(222/222) + recomputation raw_median depuis df_feat.csv a 1e-6 (C0, §8.57).
A1 : Delta a w egal (w_size du best_config ; paires a w_R == w_N ; LOCO
d_div/Delta ~ [1, w, ln n] et [1, w, ln n, (ln n)^2] ; transfert A -> B).
A2 : residu R = Delta - F2(ln n), F2 gelee §8.62 (beta [-12.896435,
5.27966, -0.402319], R2 = 0,6725), sur les 106 paires reel/nul.
A3 : predicteurs depuis fluxes_raw.csv SEUL (pas de df_feat : paysage
d'estimateurs = circularite §8.57) — p, n, dispersion inter-flux,
correlation moyenne, part PC1, skew moyen ; cibles : identite de la
paire (kNN LOCO) et d_div +/-0,10 (ridge LOCO, §8.57).
A4 : declencheur du pic etroit, relecture de pic_etroit_873_extract.json
(position G(c), AUC G_max, P1/P2 frais, interventions).
Sorties : delta_894_results.json + delta_894_table.csv + log.
"""
import csv
import hashlib
import json
import math
import os
import sys
from collections import Counter

import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
DIV = ["LevinaBickel", "PCAIntrinsic", "LocalPCA", "GraphDimension",
       "PersistentHomology", "MFA"]
SAT = ["Higuchi", "Katz", "Petrosian", "Sevcik", "BoxCounting", "Hurst2mH", "DFA"]
TARGETS = DIV + SAT
F2_DELTA_BETA = [-12.896435, 5.27966, -0.402319]  # §8.62 phaseA, GELEE
LOG = open(os.path.join(BASE, "v62_delta_elucidation_894.log"), "w")


def log(s=""):
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_sorted(s):
    out = {}
    for part in str(s).split(";"):
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        try:
            out[k.strip()] = float(v)
        except ValueError:
            pass
    return out


def cohort_of(csv_path):
    p = str(csv_path)
    if "biophysique-hp35" in p:
        return "hp35"
    if "geo62452" in p:
        return "geo62452"
    if "geo71729" in p:
        return "geo71729"
    if "icgc" in p:
        return "icgc"
    if "cptac" in p:
        return "cptac"
    if "depmap" in p:
        return "depmap"
    if "coad" in p:
        return "coad"
    if "luad" in p:
        return "luad"
    if "tcga" in p:
        return "tcga"
    return "INCONNU"


def mom_of_columns(df, cols, row_mask=None):
    per = []
    sub = df.loc[row_mask, cols] if row_mask is not None else df[cols]
    for c in cols:
        v = sub[c].to_numpy(dtype=float)
        v = v[np.isfinite(v)]
        per.append(float(np.median(v)) if len(v) else np.nan)
    per = np.array(per, dtype=float)
    fin = per[np.isfinite(per)]
    if len(fin) == 0:
        return np.nan
    return float(np.median(fin))


def ridge_fit(Xtr, ytr, lam=10.0):
    mu = np.nanmean(Xtr, axis=0)
    sd = np.nanstd(Xtr, axis=0)
    sd = np.where(np.isfinite(sd) & (sd > 0), sd, 1.0)
    mu = np.where(np.isfinite(mu), mu, 0.0)
    Z = (Xtr - mu) / sd
    Z = np.where(np.isfinite(Z), Z, 0.0)
    Z1 = np.column_stack([np.ones(len(Z)), Z])
    p = Z1.shape[1]
    pen = np.eye(p) * lam
    pen[0, 0] = 0.0
    try:
        beta = np.linalg.solve(Z1.T @ Z1 + pen, Z1.T @ ytr)
    except np.linalg.LinAlgError:
        beta = np.linalg.lstsq(Z1.T @ Z1 + pen, Z1.T @ ytr, rcond=None)[0]
    return {"mu": mu, "sd": sd, "beta": beta}


def ridge_pred(model, Xte):
    Z = (Xte - model["mu"]) / model["sd"]
    Z = np.where(np.isfinite(Z), Z, 0.0)
    Z1 = np.column_stack([np.ones(len(Z)), Z])
    return Z1 @ model["beta"]


def ols_fit(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta


def knn_pred(Xtr, ytr, Xte, k=5):
    mu = np.nanmean(Xtr, axis=0)
    sd = np.nanstd(Xtr, axis=0)
    sd = np.where(np.isfinite(sd) & (sd > 0), sd, 1.0)
    mu = np.where(np.isfinite(mu), mu, 0.0)
    Ztr = np.where(np.isfinite((Xtr - mu) / sd), (Xtr - mu) / sd, 0.0)
    Zte = np.where(np.isfinite((Xte - mu) / sd), (Xte - mu) / sd, 0.0)
    out = []
    kk = min(k, len(Ztr))
    for z in Zte:
        d = np.sqrt(((Ztr - z) ** 2).sum(axis=1))
        idx = np.argsort(d, kind="mergesort")[:kk]
        vals, counts = np.unique(np.asarray(ytr)[idx], return_counts=True)
        out.append(vals[int(np.argmax(counts))])
    return np.array(out)


def auc_roc(scores, labels):
    """AUC Mann-Whitney (labels 0/1). None si une classe absente."""
    s = np.asarray(scores, dtype=float)
    y = np.asarray(labels, dtype=int)
    m = np.isfinite(s)
    s, y = s[m], y[m]
    n1, n0 = int((y == 1).sum()), int((y == 0).sum())
    if n1 == 0 or n0 == 0:
        return None, n1, n0
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s), dtype=float)
    ranks[order] = np.arange(1, len(s) + 1)
    # moyennes des rangs ex aequo
    i = 0
    ss = s[order]
    while i < len(ss):
        j = i
        while j + 1 < len(ss) and ss[j + 1] == ss[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = (i + 1 + j + 1) / 2.0
        i = j + 1
    auc = (float(ranks[y == 1].sum()) - n1 * (n1 + 1) / 2.0) / (n1 * n0)
    return float(auc), n1, n0


# ------------------------------------------------------------------ chargement A
def load_A():
    levels = list(csv.DictReader(open(os.path.join(BASE, "v62_delta_levels.csv"))))
    log(f"Runs lus (v62_delta_levels.csv) : {len(levels)}")
    rows, missing_json, missing_csv, missing_feat = [], [], [], []
    c0_ok, c0_bad, c0_tot = 0, [], 0
    for r in levels:
        d = r["dir"]
        p = os.path.join(BASE, d, "master_results.json")
        if not os.path.exists(p):
            missing_json.append(d)
            continue
        j = json.load(open(p))
        cp = (j.get("metadata") or {}).get("csv_path")
        if not cp:
            missing_csv.append(d)
            continue
        dfp = os.path.join(BASE, d, "df_feat.csv")
        if not os.path.exists(dfp):
            missing_feat.append(d)
            continue
        div = parse_sorted(r["div_sorted"])
        sat = parse_sorted(r["sat_sorted"])
        ds = sorted(div.values())
        k = len(ds)
        ddiv_calc = (ds[k // 2 - 1] + ds[k // 2]) / 2.0 if k % 2 == 0 else ds[k // 2]
        ss = sorted(sat.values())
        dsat_calc = ss[3] if len(ss) >= 4 else None
        df = pd.read_csv(dfp)
        per = (j.get("holographic_tension_state") or {}).get("per_estimator") or {}
        for t in TARGETS:
            cols = [c for c in df.columns if c.endswith("_" + t + "_mean")]
            f = mom_of_columns(df, cols) if cols else np.nan
            ref = per.get(t, {}).get("raw_median")
            c0_tot += 1
            if ref is None and not np.isfinite(f):
                c0_ok += 1
            elif ref is not None and np.isfinite(f) and abs(float(ref) - f) <= 1e-6:
                c0_ok += 1
            else:
                c0_bad.append((d, t, ref, f))
        try:
            bc = (j["run_pipeline"]["threshold_metadata"]
                  ["threshold_optimization"]["best_config"])
            w_size = bc.get("w_size")
            w_size = float(w_size) if w_size is not None else None
        except (KeyError, TypeError):
            w_size = None
        rows.append({"dir": d, "version": r["version"], "n": float(r["n"]),
                     "control": r["control"], "cohort": cohort_of(cp),
                     "csv_path": cp, "w": w_size,
                     "d_div": float(r["d_div"]), "d_sat": float(r["d_sat"]),
                     "delta": float(r["delta"]), "pair": r["pair"],
                     "ddiv_calc": ddiv_calc, "dsat_calc": dsat_calc,
                     "maxsep": float(r["max_sep"]) if r.get("max_sep") else None})
    log(f"JSON manquants : {missing_json} ; csv_path manquants : {missing_csv} ; "
        f"df_feat manquants : {missing_feat}")
    log(f"C0 recomputation serie complete : {c0_ok}/{c0_tot} a 1e-6 "
        f"(ecarts : {c0_bad[:5]})")
    bad_div = [x for x in rows if abs(x["d_div"] - x["ddiv_calc"]) > 1e-3]
    bad_sat = [x for x in rows if x["dsat_calc"] is None
               or abs(x["d_sat"] - x["dsat_calc"]) > 1e-3]
    log(f"Verification identite d_div/d_sat : ecart > 1e-3 sur {len(bad_div)}/{len(rows)} "
        f"(div) et {len(bad_sat)}/{len(rows)} (sat)")
    return rows, c0_ok, c0_tot, c0_bad, bad_div, bad_sat


def load_B():
    import glob
    dirs = sorted(glob.glob(os.path.join(BASE, "results_fast_v62_862_*")))
    rows = []
    for dp in dirs:
        d = os.path.basename(dp)
        p = os.path.join(dp, "master_results.json")
        if not os.path.exists(p):
            continue
        j = json.load(open(p))
        dv = (j.get("holographic_tension_state") or {}).get("D_vector") or {}
        try:
            bc = (j["run_pipeline"]["threshold_metadata"]
                  ["threshold_optimization"]["best_config"])
            w_size = bc.get("w_size")
            w_size = float(w_size) if w_size is not None else None
        except (KeyError, TypeError):
            w_size = None
        holo = j.get("holographic_tension_state") or {}
        dt = holo.get("Delta_tension")
        cp = (j.get("metadata") or {}).get("csv_path") or ""
        n = (j.get("reading_synthesis") or {}).get("n_samples")
        rows.append({"dir": d, "n": float(n) if n is not None else None,
                     "cohort": cohort_of(cp), "csv_path": cp, "w": w_size,
                     "d_div": (None if dv.get("d_div") is None else float(dv["d_div"])),
                     "d_sat": (None if dv.get("d_sat") is None else float(dv["d_sat"])),
                     "delta": (None if dt is None else float(dt))})
    return rows


# ------------------------------------------------------------------ A1 : Delta a w egal
def analyse_A1(rows, rows_B):
    log("\n=== A1. Delta a w egal ===")
    ws = [r["w"] for r in rows if r["w"] is not None]
    log(f"w_size recupere : {len(ws)}/222 runs ; manquants : {222 - len(ws)}")
    log(f"w : min={min(ws):.0f} med={float(np.median(ws)):.0f} max={max(ws):.0f} ; "
        f"valeurs distinctes : {len(set(ws))}")
    log(f"Distribution w (top 10) : {Counter(ws).most_common(10)}")
    # paires reel/nul (regle §8.62 : dir se terminant par _nul, base = dir[:-4])
    lv = {r["dir"]: r for r in rows}
    pairs = []
    for d in lv:
        if d.endswith("_nul"):
            base = d[:-4]
            if base in lv:
                pairs.append((base, d))
    log(f"Paires reel/nul : {len(pairs)}")
    same_w = [(b, n) for b, n in pairs if lv[b]["w"] is not None
              and lv[b]["w"] == lv[n]["w"]]
    log(f"Paires a w_R == w_N : {len(same_w)}/{len(pairs)}")
    res = {"n_paires": len(pairs), "n_same_w": len(same_w),
           "w_distincts": len(set(ws)), "w_manquants": 222 - len(ws),
           "w_min": min(ws), "w_mediane": float(np.median(ws)), "w_max": max(ws)}
    if same_w:
        dD = np.array([lv[b]["delta"] - lv[n]["delta"] for b, n in same_w])
        res["same_w"] = {
            "n": len(same_w),
            "delta_diff_abs_le_010": f"{int((np.abs(dD) <= 0.10).sum())}/{len(dD)}",
            "frac_le_010": float((np.abs(dD) <= 0.10).mean()),
            "delta_diff_mean": float(np.mean(dD)),
            "delta_diff_std": float(np.std(dD, ddof=1)) if len(dD) > 1 else None,
            "separent_gt_007": f"{int((dD > 0.07).sum())}/{len(dD)}",
            "separent_abs_gt_007": f"{int((np.abs(dD) > 0.07).sum())}/{len(dD)}",
            "w_valeurs": sorted(set(lv[b]["w"] for b, n in same_w)),
        }
        log(f"A w egal ({len(same_w)} paires) : |Delta_R-Delta_N| <= 0,10 sur "
            f"{res['same_w']['delta_diff_abs_le_010']} ; moyenne {np.mean(dD):+.4f} ; "
            f"ecart > 0,07 (reel > nul) : {res['same_w']['separent_gt_007']}")
    # Delta vs w (tous runs) : correlation
    w_arr = np.array([r["w"] for r in rows if r["w"] is not None], dtype=float)
    d_arr = np.array([r["delta"] for r in rows if r["w"] is not None], dtype=float)
    dd_arr = np.array([r["d_div"] for r in rows if r["w"] is not None], dtype=float)
    ln_n = np.log(np.array([r["n"] for r in rows if r["w"] is not None], dtype=float))
    res["corr_delta_w"] = float(np.corrcoef(w_arr, d_arr)[0, 1])
    res["corr_ddiv_w"] = float(np.corrcoef(w_arr, dd_arr)[0, 1])
    res["corr_delta_logn"] = float(np.corrcoef(ln_n, d_arr)[0, 1])
    log(f"Correlations (222 runs) : r(Delta, w) = {res['corr_delta_w']:+.3f} ; "
        f"r(d_div, w) = {res['corr_ddiv_w']:+.3f} ; r(Delta, ln n) = {res['corr_delta_logn']:+.3f}")
    # LOCO : predire d_div et Delta depuis [1, w, ln n] et [1, w, ln n, (ln n)^2]
    cohorts = sorted(set(r["cohort"] for r in rows))
    for target in ("d_div", "delta"):
        for design, label in ((lambda w_, l_: np.column_stack([np.ones(len(w_)), w_, l_]), "1+w+lnn"),
                              (lambda w_, l_: np.column_stack([np.ones(len(w_)), w_, l_, l_ ** 2]), "1+w+lnn+lnn2"),
                              (lambda w_, l_: np.column_stack([np.ones(len(w_)), l_]), "1+lnn (ref §8.62)"),
                              (lambda w_, l_: np.column_stack([np.ones(len(w_)), w_]), "1+w seul")):
            errs, ok = [], 0
            per_fold = {}
            for c in cohorts:
                tr = [r for r in rows if r["cohort"] != c and r["w"] is not None]
                te = [r for r in rows if r["cohort"] == c and r["w"] is not None]
                if not tr or not te:
                    continue
                Xtr = design(np.array([r["w"] for r in tr], dtype=float),
                             np.log(np.array([r["n"] for r in tr], dtype=float)))
                ytr = np.array([r[target] for r in tr], dtype=float)
                Xte = design(np.array([r["w"] for r in te], dtype=float),
                             np.log(np.array([r["n"] for r in te], dtype=float)))
                yte = np.array([r[target] for r in te], dtype=float)
                beta = ols_fit(Xtr, ytr)
                pred = Xte @ beta
                e = np.abs(yte - pred)
                errs.extend(e.tolist())
                per_fold[c] = {"n": len(te),
                               "frac_pm010": float((e <= 0.10).mean())}
            errs = np.array(errs)
            frac = float((errs <= 0.10).mean()) if len(errs) else None
            res[f"LOCO_{target}_{label}"] = {"frac_pm010": frac,
                                             "mae": float(np.mean(errs)) if len(errs) else None,
                                             "n": int(len(errs)), "per_fold": per_fold}
            log(f"LOCO {target} [{label}] : +/-0,10 sur {int((errs <= 0.10).sum())}/{len(errs)} "
                f"({frac * 100:.1f} %) ; MAE {np.mean(errs):.3f}")
    # Transfert A -> B (modeles ajustes sur A entier, testes sur B)
    Bv = [r for r in rows_B if r["d_div"] is not None and r["delta"] is not None
          and r["w"] is not None and r["n"] is not None]
    log(f"Ensemble B valide (d_div/Delta/w/n finis) : {len(Bv)}/31")
    res["B_n_valide"] = len(Bv)
    for target in ("d_div", "delta"):
        for design, label in ((lambda w_, l_: np.column_stack([np.ones(len(w_)), w_, l_]), "1+w+lnn"),
                              (lambda w_, l_: np.column_stack([np.ones(len(w_)), w_, l_, l_ ** 2]), "1+w+lnn+lnn2")):
            tr = [r for r in rows if r["w"] is not None]
            Xtr = design(np.array([r["w"] for r in tr], dtype=float),
                         np.log(np.array([r["n"] for r in tr], dtype=float)))
            ytr = np.array([r[target] for r in tr], dtype=float)
            beta = ols_fit(Xtr, ytr)
            Xte = design(np.array([r["w"] for r in Bv], dtype=float),
                         np.log(np.array([r["n"] for r in Bv], dtype=float)))
            yte = np.array([r[target] for r in Bv], dtype=float)
            e = np.abs(yte - (Xte @ beta))
            res[f"transfert_B_{target}_{label}"] = {
                "frac_pm010": float((e <= 0.10).mean()), "mae": float(np.mean(e)),
                "n": int(len(e))}
            log(f"Transfert A->B {target} [{label}] : +/-0,10 sur "
                f"{int((e <= 0.10).sum())}/{len(e)} ({float((e <= 0.10).mean()) * 100:.1f} %) ; "
                f"MAE {np.mean(e):.3f}")
    # Relecture §8.63 : ecart w27-w30 deja mesure (replica_delta_863.json)
    try:
        m63 = json.load(open(os.path.join(BASE, "replica_delta_863.json")))
        res["rappel_863_partage"] = m63.get("partage")
        log(f"Rappel §8.63 (replica, tenu) : {m63.get('partage')}")
    except Exception as exc:
        res["rappel_863_partage"] = f"illisible : {exc}"
    return res


# ------------------------------------------------------------------ A2 : residu F2
def analyse_A2(rows):
    log("\n=== A2. Residu Delta - F2(ln n) (coefficients §8.62 geles) ===")
    b0, b1, b2 = F2_DELTA_BETA
    lv = {r["dir"]: r for r in rows}
    pairs = []
    for d in lv:
        if d.endswith("_nul"):
            base = d[:-4]
            if base in lv:
                pairs.append((base, d))
    dd, rd, rd_check = [], [], []
    for base, nul in pairs:
        rb, rn = lv[base], lv[nul]
        assert rb["n"] == rn["n"], f"n differents dans la paire {base}"
        f2 = b0 + b1 * math.log(rb["n"]) + b2 * (math.log(rb["n"]) ** 2)
        dd.append(rb["delta"] - rn["delta"])
        rd.append((rb["delta"] - f2) - (rn["delta"] - f2))
        rd_check.append(abs((rb["delta"] - rn["delta"])
                            - ((rb["delta"] - f2) - (rn["delta"] - f2))))
    dd, rd = np.array(dd), np.array(rd)
    res = {"n_paires": len(pairs),
           "F2_beta": F2_DELTA_BETA,
           "Delta_diff_abs_le_010": f"{int((np.abs(dd) <= 0.10).sum())}/{len(dd)}",
           "Delta_diff_mean": float(np.mean(dd)),
           "Delta_diff_std": float(np.std(dd, ddof=1)),
           "resid_diff_abs_le_010": f"{int((np.abs(rd) <= 0.10).sum())}/{len(rd)}",
           "resid_diff_mean": float(np.mean(rd)),
           "resid_diff_std": float(np.std(rd, ddof=1)),
           "resid_frac_le_010": float((np.abs(rd) <= 0.10).mean()),
           "annulation_F2_max_ecart": float(max(rd_check)),
           "critere_90pc_atteint": bool((np.abs(rd) <= 0.10).mean() >= 0.90
                                        and abs(float(np.mean(rd))) <= 0.10)}
    log(f"F2(ln n) = {b0} + {b1}*ln n + {b2}*(ln n)^2 (R2 §8.62 = 0,6725)")
    log(f"|Delta_R - Delta_N| <= 0,10 : {res['Delta_diff_abs_le_010']} ; "
        f"moyenne {res['Delta_diff_mean']:+.4f}")
    log(f"|R_R - R_N| <= 0,10 : {res['resid_diff_abs_le_010']} ; "
        f"moyenne {res['resid_diff_mean']:+.4f} ; ecart-type {res['resid_diff_std']:.4f}")
    log(f"Annulation de F2 dans les paires a meme n (max |Delta_diff - resid_diff|) : "
        f"{res['annulation_F2_max_ecart']:.2e} — F2(ln n) s'annule exactement "
        f"dans chaque paire (meme n des deux cotes).")
    log(f"Critere A2 (>= 90 % a +/-0,10 ET |moyenne| <= 0,10) : "
        f"{'ATTEINT' if res['critere_90pc_atteint'] else 'NON ATTEINT'}")
    return res


# ------------------------------------------------------------------ A3 : structure des flux
def flux_features(csv_path):
    """Predicteurs depuis fluxes_raw.csv SEUL (matrice d'entree).
    p, n, dispersion inter-flux, correlation moyenne, part PC1, skew moyen."""
    df = pd.read_csv(csv_path)
    cols = [c for c in df.columns if c.lower() != "step"]
    X = df[cols].to_numpy(dtype=float)
    n, p = X.shape
    med = np.nanmedian(X, axis=0)
    disp = float(np.std(med, ddof=1)) if p > 1 else 0.0
    # correlation moyenne (paires, |r|)
    cors = []
    for i in range(p):
        for j in range(i + 1, p):
            a, b = X[:, i], X[:, j]
            m = np.isfinite(a) & np.isfinite(b)
            if m.sum() > 3 and np.std(a[m]) > 0 and np.std(b[m]) > 0:
                cors.append(abs(float(np.corrcoef(a[m], b[m])[0, 1])))
    corr_moy = float(np.mean(cors)) if cors else float("nan")
    # PC1 (SVD sur flux centres-reduits)
    mu = np.nanmean(X, axis=0)
    sd = np.nanstd(X, axis=0)
    sd = np.where(sd > 0, sd, 1.0)
    Z = (X - mu) / sd
    Z = np.where(np.isfinite(Z), Z, 0.0)
    try:
        s = np.linalg.svd(Z, compute_uv=False)
        var = s ** 2
        pc1 = float(var[0] / var.sum()) if var.sum() > 0 else float("nan")
    except np.linalg.LinAlgError:
        pc1 = float("nan")
    # skew moyen (moment standardise)
    skews = []
    for j in range(p):
        v = X[:, j]
        v = v[np.isfinite(v)]
        if len(v) > 3 and np.std(v) > 0:
            z = (v - np.mean(v)) / np.std(v)
            skews.append(float(np.mean(z ** 3)))
    return {"p": int(p), "n": int(n), "dispersion_inter_flux": disp,
            "correlation_moyenne": corr_moy, "part_PC1": pc1,
            "skew_moyen": float(np.mean(skews)) if skews else float("nan")}


def analyse_A3(rows):
    log("\n=== A3. Structure des flux (fluxes_raw.csv seul, sans estimateur) ===")
    feats, paires = [], []
    manquants = []
    for r in rows:
        fp = os.path.join(BASE, r["dir"], "fluxes_raw.csv")
        if not os.path.exists(fp):
            manquants.append(r["dir"])
            continue
        try:
            f = flux_features(fp)
        except Exception as exc:
            manquants.append(f"{r['dir']}: {exc}")
            continue
        f["dir"] = r["dir"]
        f["cohort"] = r["cohort"]
        f["d_div"] = r["d_div"]
        f["delta"] = r["delta"]
        f["pair"] = r["pair"]
        feats.append(f)
    log(f"Features calculees : {len(feats)}/222 ; manquants/erreurs : {len(manquants)}")
    keys = ["p", "n", "dispersion_inter_flux", "correlation_moyenne", "part_PC1", "skew_moyen"]
    X = np.array([[f[k] for k in keys] for f in feats], dtype=float)
    cohorts = np.array([f["cohort"] for f in feats])
    y_pair = np.array([f["pair"] for f in feats])
    y_div = np.array([f["d_div"] for f in feats], dtype=float)
    # (a) identite de la paire, kNN LOCO (k=5)
    accs, n_tot = [], 0
    per_fold = {}
    for c in sorted(set(cohorts)):
        tr, te = cohorts != c, cohorts == c
        if tr.sum() < 6 or te.sum() == 0:
            continue
        pred = knn_pred(X[tr], y_pair[tr], X[te], k=5)
        acc = float((pred == y_pair[te]).mean())
        per_fold[c] = {"n": int(te.sum()), "accuracy": acc}
        accs.extend((pred == y_pair[te]).tolist())
        n_tot += int(te.sum())
    acc_glob = float(np.mean(accs)) if accs else None
    log(f"(a) Identite de la paire (kNN k=5, LOCO) : {int(sum(accs))}/{n_tot} "
        f"({acc_glob * 100:.1f} %) — barre 90 %")
    for c, v in per_fold.items():
        log(f"    {c}: {v['accuracy'] * 100:.1f} % (n={v['n']})")
    # (b) d_div +/-0,10, ridge LOCO (lam=10, §8.57)
    errs = []
    per_fold_b = {}
    for c in sorted(set(cohorts)):
        tr, te = cohorts != c, cohorts == c
        if tr.sum() < 6 or te.sum() == 0:
            continue
        model = ridge_fit(X[tr], y_div[tr], lam=10.0)
        pred = ridge_pred(model, X[te])
        e = np.abs(y_div[te] - pred)
        errs.extend(e.tolist())
        per_fold_b[c] = {"n": int(te.sum()),
                         "frac_pm010": float((e <= 0.10).mean()),
                         "mae": float(np.mean(e))}
    errs = np.array(errs)
    frac = float((errs <= 0.10).mean()) if len(errs) else None
    log(f"(b) d_div +/-0,10 (ridge lam=10, LOCO) : {int((errs <= 0.10).sum())}/{len(errs)} "
        f"({frac * 100:.1f} %) ; MAE {np.mean(errs):.3f} — barre 90 %")
    for c, v in per_fold_b.items():
        log(f"    {c}: +/-0,10 {v['frac_pm010'] * 100:.1f} % (n={v['n']}, MAE {v['mae']:.3f})")
    # correlations simples predicteur -> d_div / Delta (descriptif)
    cors = {}
    for k in keys:
        v = np.array([f[k] for f in feats], dtype=float)
        m = np.isfinite(v)
        cors[k] = {"r_d_div": (None if m.sum() < 3 or np.std(v[m]) == 0 else
                               float(np.corrcoef(v[m], y_div[m])[0, 1])),
                   "r_delta": (None if m.sum() < 3 or np.std(v[m]) == 0 else
                               float(np.corrcoef(v[m], np.array([f['delta'] for f in feats])[m])[0, 1]))}
    log(f"Correlations predicteurs (descriptif) : {json.dumps(cors, ensure_ascii=False)}")
    return {"n_features": len(feats), "manquants": manquants,
            "pair_knn_loco_accuracy": acc_glob,
            "pair_knn_n": n_tot, "pair_knn_per_fold": per_fold,
            "ddiv_ridge_loco_frac_pm010": frac,
            "ddiv_ridge_loco_mae": float(np.mean(errs)) if len(errs) else None,
            "ddiv_ridge_loco_n": int(len(errs)), "ddiv_ridge_per_fold": per_fold_b,
            "correlations": cors}


# ------------------------------------------------------------------ A4 : pic etroit
def analyse_A4():
    log("\n=== A4. Pic etroit : declencheur (relecture §8.73) ===")
    ext = json.load(open(os.path.join(BASE, "pic_etroit_873_extract.json")))
    lignes = ext["corpus"]["lignes"]
    stats = ext["corpus"].get("stats", {})
    log(f"Corpus §8.73 relu : {len(lignes)} courbes gagnantes ; stats : "
        f"{json.dumps(stats, ensure_ascii=False)[:600]}")
    # Position G(c) : recompute depuis les lignes detenues
    ok_pos, n_robon = 0, 0
    for lig in lignes:
        if not lig.get("rob_on"):
            continue
        n_robon += 1
        ncand = lig["config_gagnante"][0]
        pas = 100.0 / (ncand - 1) if ncand > 1 else float("nan")
        if abs(lig["candidat_pred_G"] - lig["seuil_pic"]) <= 2 * pas + 1e-9:
            ok_pos += 1
    # AUC G_max (NOUVEAU : §8.73 a publie AUC pour E_max/H_max/max_e, pas G_max)
    g = [lig["G_max"] for lig in lignes]
    y = [1 if lig.get("rob_on") else 0 for lig in lignes]
    auc_g, n1, n0 = auc_roc(g, y)
    auc_h, _, _ = auc_roc([lig["H_max"] for lig in lignes], y)
    auc_e, _, _ = auc_roc([lig["E_max"] for lig in lignes], y)
    auc_m, _, _ = auc_roc([lig["max_e_ligne"] for lig in lignes], y)
    interv = ext.get("interventions", {})
    fresh = ext.get("fresh", {})
    res = {"n_courbes_corpus": len(lignes), "n_robon": n_robon,
           "position_G_pm2": f"{ok_pos}/{n_robon}",
           "position_G_frac": (ok_pos / n_robon if n_robon else None),
           "AUC_G_max": auc_g, "AUC_H_max": auc_h, "AUC_E_max": auc_e,
           "AUC_max_e_ligne": auc_m, "n_robon_auc": n1, "n_roboff_auc": n0,
           "interventions": interv, "fresh_P1": fresh.get("P1"),
           "fresh_P2": fresh.get("P2"),
           "fresh_n_gagnantes_robon": fresh.get("n_gagnantes_robon"),
           "fresh_verification_replique": fresh.get("verification_replique")}
    log(f"Position : argmax G(c) a +/-2 pas du vrai pic sur {ok_pos}/{n_robon} "
        f"courbes rob-on (recalcule depuis les lignes detenues).")
    log(f"AUC rob-on vs rob-off (corpus, {n1} vs {n0}) : G_max {auc_g:.3f} ; "
        f"H_max {auc_h:.3f} ; E_max {auc_e:.3f} ; max_e_ligne {auc_m:.3f}")
    log(f"Interventions §8.73 (relues) : {json.dumps(interv, ensure_ascii=False)[:900]}")
    log(f"Frais §8.73 (relus) : P1={fresh.get('P1')} ; P2={fresh.get('P2')} ; "
        f"n_gagnantes_robon={fresh.get('n_gagnantes_robon')}")
    return res


# ------------------------------------------------------------------ main
def main():
    log("=== §8.94 — Elucider Delta, nouvelle tentative ===")
    for name, path in (("v6.2", os.path.join(BASE, "..", "biophysique-hp35", "universal_v6.2.0_cohen.py")),
                       ("v6.1", os.path.join(BASE, "..", "biophysique-hp35", "universal_v6.1.0_cohen.py")),
                       ("v6", os.path.join(BASE, "..", "biophysique-hp35", "universal_v6.0.0_cohen.py"))):
        log(f"SHA pipeline {name} : {sha(path) if os.path.exists(path) else 'INTROUVABLE'}")
    log(f"SHA protocole : {sha(os.path.join(BASE, 'PROTOCOL_delta_elucidation_894.md'))}")
    rows, c0_ok, c0_tot, c0_bad, bad_div, bad_sat = load_A()
    if c0_bad or bad_div or bad_sat:
        log("ARRET : verification prealable echouee (protocole §2).")
        with open(os.path.join(BASE, "delta_894_results.json"), "w") as f:
            json.dump({"verification": {"c0_ok": c0_ok, "c0_tot": c0_tot,
                                        "c0_bad": c0_bad[:10],
                                        "bad_div": [r["dir"] for r in bad_div],
                                        "bad_sat": [r["dir"] for r in bad_sat],
                                        "ok": False}}, f, indent=1, ensure_ascii=False)
        return 1
    log("Verification prealable : OK (C0 + identites).")
    rows_B = load_B()
    log(f"Ensemble B lu : {len(rows_B)} dossiers.")
    a1 = analyse_A1(rows, rows_B)
    a2 = analyse_A2(rows)
    a3 = analyse_A3(rows)
    a4 = analyse_A4()
    out = {"verification": {"c0": f"{c0_ok}/{c0_tot}", "identite_div_sat": "222/222 a 1e-3",
                            "ok": True},
           "A1_w_egal": a1, "A2_residu_F2": a2, "A3_structure_flux": a3,
           "A4_pic_etroit": a4,
           "sha_protocole": sha(os.path.join(BASE, "PROTOCOL_delta_elucidation_894.md"))}
    with open(os.path.join(BASE, "delta_894_results.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=str)
    # CSV par run (w, d_div, d_sat, Delta, residu, paire)
    b0, b1, b2 = F2_DELTA_BETA
    with open(os.path.join(BASE, "delta_894_table.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["dir", "version", "n", "cohort", "w",
                                           "d_div", "d_sat", "delta", "residu_F2", "pair"])
        w.writeheader()
        for r in rows:
            lnn = math.log(r["n"])
            w.writerow({"dir": r["dir"], "version": r["version"], "n": r["n"],
                        "cohort": r["cohort"], "w": r["w"], "d_div": r["d_div"],
                        "d_sat": r["d_sat"], "delta": r["delta"],
                        "residu_F2": r["delta"] - (b0 + b1 * lnn + b2 * lnn ** 2),
                        "pair": r["pair"]})
    log("ecrit: delta_894_results.json, delta_894_table.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
