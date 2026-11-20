#!/usr/bin/env python3
"""§8.57 — Elucider Delta a partir des series completes.
Protocole gele : PROTOCOL_delta_series_857.md (SHA 965a88dc90c8af0ca701af2da1c31d124ceccef059d13a0972fae15ba6266bdc).
Lecture seule. Aucun run du pipeline, aucune modification du pipeline.
Ensemble : 222 runs (v62_delta_levels.csv), 156 matrices, 9 cohortes.
Series : df_feat.csv par run (120 lignes de scan, colonnes <flux>_<est>_mean).
CIRCULARITE : la cible raw_median(e) = mediane sur les flux de la mediane sur
les 120 lignes de scan. La serie COMPLETE de e ne sert qu'au diagnostic C0
(recomputation, hors critere). Les modeles honnetes n'utilisent qu'une PARTIE
STRICTE : prefixe (Progress<=50), demi-flux (indices pairs), trans-estimateur
prefixe (aucune info de e), ou la matrice de flux d'entree seule (S4).
Sorties : v62_delta_series_857.log/.json/.md, v62_delta_series_857_features.csv
"""
import csv
import hashlib
import json
import math
import os
import sys
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
DIV = ["LevinaBickel", "PCAIntrinsic", "LocalPCA", "GraphDimension",
       "PersistentHomology", "MFA"]
SAT = ["Higuchi", "Katz", "Petrosian", "Sevcik", "BoxCounting", "Hurst2mH", "DFA"]
TARGETS = DIV + SAT
LABELS = ["B0", "S1d", "S1r", "S2d", "S2r", "S3r", "S4r", "S4k"]
LOG = open(os.path.join(BASE, "v62_delta_series_857.log"), "w")


def log(s=""):
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
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
    """Regles gelees, dans CET ordre (premier motif gagne). Identique §8.42."""
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


def pearson_r(xs, ys):
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    m = np.isfinite(xs) & np.isfinite(ys)
    if m.sum() < 3:
        return None
    xs, ys = xs[m], ys[m]
    if xs.std() == 0 or ys.std() == 0:
        return None
    return float(np.corrcoef(xs, ys)[0, 1])


def mom_of_columns(df, cols, row_mask):
    """Mediane-de-medianes sur les lignes row_mask et les colonnes cols.
    Retourne (mom, iqr_inter_flux, n_flux_finis, per_flux_medians)."""
    per = []
    sub = df.loc[row_mask, cols] if row_mask is not None else df[cols]
    for c in cols:
        v = sub[c].to_numpy(dtype=float)
        v = v[np.isfinite(v)]
        per.append(float(np.median(v)) if len(v) else np.nan)
    per = np.array(per, dtype=float)
    fin = per[np.isfinite(per)]
    if len(fin) == 0:
        return np.nan, np.nan, 0, per
    iqr = float(np.percentile(fin, 75) - np.percentile(fin, 25)) if len(fin) >= 2 else np.nan
    return float(np.median(fin)), iqr, int(len(fin)), per


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


def knn_pred(Xtr, ytr, Xte, k=5):
    mu = np.nanmean(Xtr, axis=0)
    sd = np.nanstd(Xtr, axis=0)
    sd = np.where(np.isfinite(sd) & (sd > 0), sd, 1.0)
    mu = np.where(np.isfinite(mu), mu, 0.0)
    Ztr = np.where(np.isfinite((Xtr - mu) / sd), (Xtr - mu) / sd, 0.0)
    Zte = np.where(np.isfinite((Xte - mu) / sd), (Xte - mu) / sd, 0.0)
    out = np.empty(len(Zte))
    kk = min(k, len(Ztr))
    for i, z in enumerate(Zte):
        d = np.sqrt(((Ztr - z) ** 2).sum(axis=1))
        idx = np.argsort(d, kind="mergesort")[:kk]
        out[i] = float(np.mean(ytr[idx]))
    return out


def impute_train_median(Xtr, Xte):
    """Impute les NaN par la mediane du TRAIN par colonne (0.0 si tout NaN)."""
    Xtr = Xtr.astype(float).copy()
    Xte = Xte.astype(float).copy()
    for j in range(Xtr.shape[1]):
        col = Xtr[:, j]
        med = np.nanmedian(col) if np.isfinite(col).any() else 0.0
        if not np.isfinite(med):
            med = 0.0
        Xtr[np.isnan(Xtr[:, j]), j] = med
        Xte[np.isnan(Xte[:, j]), j] = med
    return Xtr, Xte


def derive_pair_ddiv(pred_div, mask_L, mask_P):
    members = []
    for t in DIV:
        if t == "LevinaBickel" and not mask_L:
            continue
        if t == "PersistentHomology" and not mask_P:
            continue
        v = pred_div.get(t)
        if v is not None and np.isfinite(v):
            members.append((float(v), t))
    if len(members) < 2:
        return None, None
    members.sort()
    k = len(members)
    if k % 2 == 0:
        a, b = members[k // 2 - 1], members[k // 2]
        return (a[1], b[1]), (a[0] + b[0]) / 2.0
    return (members[k // 2][1],), members[k // 2][0]


def derive_dsat(pred_sat):
    vals = sorted([float(v) for v in pred_sat.values()
                   if v is not None and np.isfinite(v)])
    if len(vals) < 4:
        return None
    return vals[3]


# ----------------------------------------------------------------- chargement
def main():
    log("=== §8.57 — Delta depuis les series completes (PROTOCOL_delta_series_857.md) ===")
    for name, path in [("v6.2", os.path.join(BASE, "..", "biophysique-hp35", "universal_v6.2.0_cohen.py")),
                       ("v6.1", os.path.join(BASE, "..", "biophysique-hp35", "universal_v6.1.0_cohen.py")),
                       ("v6", os.path.join(BASE, "..", "biophysique-hp35", "universal_v6.0.0_cohen.py"))]:
        log(f"SHA pipeline {name} : {sha256_file(path) if os.path.exists(path) else 'INTROUVABLE'}")
    log(f"SHA protocole : {sha256_file(os.path.join(BASE, 'PROTOCOL_delta_series_857.md'))}")
    log(f"SHA protocole §8.42 (reference) : {sha256_file(os.path.join(BASE, 'PROTOCOL_delta_magnitudes.md'))}")

    levels = list(csv.DictReader(open(os.path.join(BASE, "v62_delta_levels.csv"))))
    log(f"Runs lus (v62_delta_levels.csv) : {len(levels)}")
    rows = []
    missing_json, missing_csvpath, missing_dffeat = [], [], []
    c0_ok, c0_bad, c0_tot = 0, [], 0
    n_prefix_rows = Counter()
    n_feat_sha = {}
    feat_rows_csv = []
    for r in levels:
        d = r["dir"]
        p = os.path.join(BASE, d, "master_results.json")
        if not os.path.exists(p):
            missing_json.append(d)
            continue
        j = json.load(open(p))
        cp = (j.get("metadata") or {}).get("csv_path")
        if not cp:
            missing_csvpath.append(d)
            continue
        dfp = os.path.join(BASE, d, "df_feat.csv")
        if not os.path.exists(dfp):
            missing_dffeat.append(d)
            continue
        div = parse_sorted(r["div_sorted"])
        sat = parse_sorted(r["sat_sorted"])
        ds = sorted(div.values())
        k = len(ds)
        ddiv_calc = (ds[k // 2 - 1] + ds[k // 2]) / 2.0 if k % 2 == 0 else ds[k // 2]
        ss = sorted(sat.values())
        dsat_calc = ss[3] if len(ss) >= 4 else None
        # --- series df_feat ---
        df = pd.read_csv(dfp)
        n_prefix_rows[int((df["Progress"] <= 50.0).sum())] += 1
        if len(df) != 120:
            log(f"ATTENTION {d} : df_feat {len(df)} lignes (attendu 120)")
        per = (j.get("holographic_tension_state") or {}).get("per_estimator") or {}
        row_mask = df["Progress"] <= 50.0
        pref, half, full = {}, {}, {}
        pref_iqr, half_iqr = {}, {}
        for t in TARGETS:
            cols = [c for c in df.columns if c.endswith("_" + t + "_mean")]
            if not cols:
                pref[t] = half[t] = full[t] = np.nan
                pref_iqr[t] = half_iqr[t] = np.nan
                continue
            f, _, _, _ = mom_of_columns(df, cols, None)
            pr, pri, _, _ = mom_of_columns(df, cols, row_mask)
            hf, hfi, _, _ = mom_of_columns(df, cols[0::2], None)
            full[t], pref[t], half[t] = f, pr, hf
            pref_iqr[t], half_iqr[t] = pri, hfi
            # --- diagnostic C0 : recomputation serie complete vs raw_median ---
            ref = per.get(t, {}).get("raw_median")
            c0_tot += 1
            if ref is None and (f is None or (isinstance(f, float) and not np.isfinite(f))):
                c0_ok += 1
            elif ref is not None and np.isfinite(f) and abs(float(ref) - f) <= 1e-6:
                c0_ok += 1
            else:
                c0_bad.append((d, t, ref, f))
        rows.append({"dir": d, "version": r["version"], "n": float(r["n"]),
                     "control": r["control"], "mask": r["mask"],
                     "mask_L": r["mask"][0] == "L", "mask_P": r["mask"][1] == "P",
                     "d_div": float(r["d_div"]), "d_sat": float(r["d_sat"]),
                     "delta": float(r["delta"]), "pair": r["pair"],
                     "pair_set": set(r["pair"].split("+")) if r["pair"] else set(),
                     "div": div, "sat": sat, "ddiv_calc": ddiv_calc,
                     "dsat_calc": dsat_calc, "csv_path": cp,
                     "div_sorted": r["div_sorted"],
                     "cohort": cohort_of(cp),
                     "targets": {t: (div.get(t) if t in DIV else sat.get(t)) for t in TARGETS},
                     "pref": pref, "half": half, "full_recomp": full,
                     "pref_iqr": pref_iqr, "half_iqr": half_iqr,
                     "df_feat_sha": sha256_file(dfp)})
        feat_rows_csv.append({"dir": d, "csv_path": cp, "cohort": cohort_of(cp),
                              "df_feat_sha": rows[-1]["df_feat_sha"],
                              **{f"pref_{t}": pref[t] for t in TARGETS},
                              **{f"half_{t}": half[t] for t in TARGETS},
                              **{f"full_recomp_{t}": full[t] for t in TARGETS}})
    log(f"JSON manquants : {missing_json} ; csv_path manquants : {missing_csvpath} ; "
        f"df_feat manquants : {missing_dffeat}")
    log(f"Lignes Progress<=50 par df_feat : {dict(n_prefix_rows)} (attendu 60 partout)")
    log(f"C0 recomputation serie complete : {c0_ok}/{c0_tot} a 1e-6 "
        f"(ecarts : {c0_bad[:5]})")
    if c0_bad:
        log("ARRET : identite C0 non verifiee (protocole §2.2).")
        return 1
    bad_div = [r for r in rows if abs(r["d_div"] - r["ddiv_calc"]) > 1e-3]
    bad_sat = [r for r in rows if r["dsat_calc"] is None or abs(r["d_sat"] - r["dsat_calc"]) > 1e-3]
    log(f"Verification identite d_div/d_sat : ecart > 1e-3 sur {len(bad_div)}/{len(rows)} "
        f"(div) et {len(bad_sat)}/{len(rows)} (sat)")
    if bad_div or bad_sat:
        log("ARRET : identite non verifiee (protocole §2.1).")
        return 1
    miss_t = [(r["dir"], t) for r in rows for t in TARGETS if r["targets"][t] is None]
    log(f"Cibles manquantes : {len(miss_t)} : {Counter(t for _, t in miss_t)}")
    log(f"Cohortes (runs) : {dict(Counter(r['cohort'] for r in rows))}")
    distinct = {}
    for r in rows:
        distinct.setdefault(r["csv_path"], []).append(r["dir"])
    log(f"Matrices distinctes : {len(distinct)} ; par cohorte : "
        f"{dict(Counter(cohort_of(c) for c in distinct))}")

    # --- S4 : traits serie de flux entiere (matrice d'entree) ---
    K = 20
    s4_by_csv = {}
    s4_nan_cols = 0
    for cp in sorted(distinct):
        path = cp if os.path.isabs(cp) else os.path.join(BASE, cp)
        mdf = pd.read_csv(path)
        n_mat = len(mdf)
        # premiere colonne = controle ; autres = flux, dans l'ordre du fichier
        flux_cols = list(mdf.columns[1:])
        p_flux = len(flux_cols)
        feats = []
        for pos in np.linspace(0, n_mat - 1, K):
            vals = []
            for c in flux_cols:
                v = mdf[c].to_numpy(dtype=float)
                if not np.isfinite(v).all():
                    s4_nan_cols += 1
                    idx = np.arange(n_mat)
                    good = np.isfinite(v)
                    if good.sum() >= 2:
                        v = np.interp(idx, idx[good], v[good])
                    elif good.sum() == 1:
                        v = np.full(n_mat, float(v[good][0]))
                    else:
                        v = np.zeros(n_mat)
                vals.append(float(np.interp(pos, np.arange(n_mat), v)))
            vals = np.array(vals)
            feats += [float(np.mean(vals)), float(np.std(vals, ddof=1)) if p_flux > 1 else 0.0,
                      float(np.min(vals)), float(np.max(vals)), float(np.median(vals))]
        feats += [float(math.log(n_mat)) if n_mat > 0 else 0.0, float(p_flux)]
        s4_by_csv[cp] = {"feats": np.array(feats, dtype=float),
                         "sha": sha256_file(path), "n": n_mat, "p": p_flux}
    n_mismatch = [r["dir"] for r in rows
                  if s4_by_csv[r["csv_path"]]["n"] != int(r["n"])]
    log(f"S4 : matrices lues {len(s4_by_csv)} ; colonnes avec NaN traitees : {s4_nan_cols} ; "
        f"ecarts n matrice vs n run : {n_mismatch}")
    if n_mismatch:
        log("ARRET : n matrice != n run.")
        return 1
    for fr in feat_rows_csv:
        fr["matrix_sha"] = s4_by_csv[[r["csv_path"] for r in rows if r["dir"] == fr["dir"]][0]]["sha"]
    with open(os.path.join(BASE, "v62_delta_series_857_features.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(feat_rows_csv[0].keys()))
        w.writeheader()
        w.writerows(feat_rows_csv)
    log("Traits de serie ecrits : v62_delta_series_857_features.csv "
        f"({len(feat_rows_csv)} runs)")

    n_runs = len(rows)
    all_idx = list(range(n_runs))
    logn = np.array([math.log(r["n"]) if r["n"] > 0 else 0.0 for r in rows])
    Y = np.array([[rows[i]["targets"][t] if rows[i]["targets"][t] is not None else np.nan
                   for t in TARGETS] for i in all_idx], dtype=float)

    def feats_for(label, t):
        """Matrice de traits (n_runs x F) pour le modele label et la cible t."""
        ti = TARGETS.index(t)
        others = [u for u in TARGETS if u != t]
        if label == "S1r":
            X = np.column_stack(
                [np.array([rows[i]["pref"][t] for i in all_idx]),
                 np.array([rows[i]["pref_iqr"][t] for i in all_idx])] +
                [np.array([rows[i]["pref"][u] for i in all_idx]) for u in others] +
                [logn])
        elif label == "S2r":
            X = np.column_stack(
                [np.array([rows[i]["half"][t] for i in all_idx]),
                 np.array([rows[i]["half_iqr"][t] for i in all_idx])] +
                [np.array([rows[i]["half"][u] for i in all_idx]) for u in others] +
                [logn])
        elif label == "S3r":
            X = np.column_stack(
                [np.array([rows[i]["pref"][u] for i in all_idx]) for u in others] +
                [logn])
        elif label in ("S4r", "S4k"):
            X = np.array([s4_by_csv[rows[i]["csv_path"]]["feats"] for i in all_idx])
        else:
            raise ValueError(label)
        return X

    def fit_predict(label, tr, te, lam=10.0):
        """Retourne pred (n_runs x 13), NaN hors test ou cible absente du train."""
        pred = np.full((n_runs, len(TARGETS)), np.nan)
        fallback_count = 0
        for ti, t in enumerate(TARGETS):
            y = Y[:, ti]
            tr_fin = [i for i in tr if np.isfinite(y[i])]
            if not tr_fin:
                continue
            train_med = float(np.median(y[tr_fin]))
            te_fin = [i for i in te if np.isfinite(y[i])]
            if not te_fin:
                continue
            if label == "B0":
                for i in te_fin:
                    pred[i, ti] = train_med
            elif label in ("S1d", "S2d"):
                src = "pref" if label == "S1d" else "half"
                for i in te_fin:
                    v = rows[i][src][t]
                    if v is None or not np.isfinite(v):
                        pred[i, ti] = train_med
                        fallback_count += 1
                    else:
                        pred[i, ti] = float(v)
            else:
                X = feats_for(label, t)
                Xtr, Xte = impute_train_median(X[tr_fin], X[te_fin])
                ytr = y[tr_fin]
                if label in ("S1r", "S2r", "S3r", "S4r"):
                    model = ridge_fit(Xtr, ytr, lam=lam)
                    pv = ridge_pred(model, Xte)
                elif label == "S4k":
                    pv = knn_pred(Xtr, ytr, Xte, k=5)
                else:
                    raise ValueError(label)
                for j, i in enumerate(te_fin):
                    pred[i, ti] = float(pv[j])
        return pred, fallback_count

    def evaluate(idxs, pred, train_idx_for_mfa):
        """Metriques sur les runs idxs, depuis pred (n_runs x 13)."""
        ok_pair = ok_pair_ord = ok_val = ok_dsat = 0
        n = 0
        mae_div, mae_sat, mae_delta = [], [], []
        per_target = {t: {"pred": [], "true": []} for t in TARGETS}
        three_n = three_ok = 0
        maj_glob = Counter()
        mfa_n = mfa_b = mfa_s = 0
        train_mfa = sorted(set(float(Y[i, TARGETS.index("MFA")])
                               for i in train_idx_for_mfa
                               if np.isfinite(Y[i, TARGETS.index("MFA")])))
        for i in idxs:
            r = rows[i]
            pdv = {t: (pred[i, TARGETS.index(t)]
                       if np.isfinite(pred[i, TARGETS.index(t)]) else None) for t in DIV}
            psv = {t: (pred[i, TARGETS.index(t)]
                       if np.isfinite(pred[i, TARGETS.index(t)]) else None) for t in SAT}
            pair_pred, ddiv_pred = derive_pair_ddiv(pdv, r["mask_L"], r["mask_P"])
            dsat_pred = derive_dsat(psv)
            if pair_pred is None or ddiv_pred is None or dsat_pred is None:
                continue
            n += 1
            if set(pair_pred) == r["pair_set"]:
                ok_pair += 1
            if tuple(pair_pred) == tuple(r["pair"].split("+")):
                ok_pair_ord += 1
            if abs(ddiv_pred - r["d_div"]) <= 0.10:
                ok_val += 1
            if abs(dsat_pred - r["d_sat"]) <= 0.10:
                ok_dsat += 1
            mae_div.append(abs(ddiv_pred - r["d_div"]))
            mae_sat.append(abs(dsat_pred - r["d_sat"]))
            mae_delta.append(abs((ddiv_pred - dsat_pred) - r["delta"]))
            for t in TARGETS:
                v = pred[i, TARGETS.index(t)]
                if np.isfinite(v) and np.isfinite(Y[i, TARGETS.index(t)]):
                    per_target[t]["pred"].append(float(v))
                    per_target[t]["true"].append(float(Y[i, TARGETS.index(t)]))
            # concours des trois hauts : k=6, LocalPCA 3e
            div_sorted_true = sorted([(v, k_) for k_, v in r["div"].items()])
            if len(div_sorted_true) == 6 and div_sorted_true[2][1] == "LocalPCA":
                three_n += 1
                # vrai plus petit des trois hauts
                tv = {t: r["div"][t] for t in ("MFA", "LevinaBickel", "PCAIntrinsic")}
                true_arg = min(tv, key=tv.get)
                pred_arg = min(((pdv[t], t) for t in ("MFA", "LevinaBickel", "PCAIntrinsic")
                                if pdv.get(t) is not None), default=(None, None))[1]
                if pred_arg == true_arg:
                    three_ok += 1
                maj_glob[true_arg] += 1
            # MFA exact
            if np.isfinite(Y[i, TARGETS.index("MFA")]) and np.isfinite(pred[i, TARGETS.index("MFA")]):
                mfa_n += 1
                if abs(pred[i, TARGETS.index("MFA")] - Y[i, TARGETS.index("MFA")]) <= 1e-9:
                    mfa_b += 1
                if train_mfa:
                    snap = min(train_mfa, key=lambda v: abs(v - pred[i, TARGETS.index("MFA")]))
                    if abs(snap - Y[i, TARGETS.index("MFA")]) <= 1e-9:
                        mfa_s += 1
        pt = {}
        for t in TARGETS:
            pr, tr_ = per_target[t]["pred"], per_target[t]["true"]
            if len(tr_) >= 3:
                ss_res = float(np.sum((np.array(pr) - np.array(tr_)) ** 2))
                ss_tot = float(np.sum((np.array(tr_) - np.mean(tr_)) ** 2))
                r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else None
                pt[t] = {"R2": r2, "MAE": float(np.mean(np.abs(np.array(pr) - np.array(tr_)))),
                         "r": pearson_r(pr, tr_), "n": len(tr_)}
            else:
                pt[t] = {"R2": None, "MAE": None, "r": None, "n": len(tr_)}
        maj = maj_glob.most_common(1)[0][0] if maj_glob else None
        maj_acc = (maj_glob[maj] / three_n) if (maj and three_n) else None
        return {"n": n,
                "paire_non_ordonnee": ok_pair / n if n else None,
                "paire_ordonnee": ok_pair_ord / n if n else None,
                "valeur_pm010": ok_val / n if n else None,
                "dsat_pm010": ok_dsat / n if n else None,
                "mae_d_div": float(np.mean(mae_div)) if mae_div else None,
                "mae_d_sat": float(np.mean(mae_sat)) if mae_sat else None,
                "mae_delta": float(np.mean(mae_delta)) if mae_delta else None,
                "per_target": pt,
                "three_way": {"n": three_n, "acc": three_ok / three_n if three_n else None,
                              "majorite_globale": maj, "acc_majorite": maj_acc},
                "mfa": {"n": mfa_n, "n_exact_brut": mfa_b, "n_exact_snappe": mfa_s,
                        "exact_brut": mfa_b / mfa_n if mfa_n else None,
                        "exact_snappe": mfa_s / mfa_n if mfa_n else None}}

    results = {"n_runs": n_runs, "n_matrices": len(distinct),
               "C0_recomputation": {"ok": c0_ok, "total": c0_tot, "bad": c0_bad[:5]},
               "prefix_rows": dict(n_prefix_rows)}
    cohorts = sorted(set(r["cohort"] for r in rows))

    def full_eval(name, tr, te, lam=10.0, store_loco=False):
        ev = {}
        preds = {}
        for label in LABELS:
            pred, fb = fit_predict(label, tr, te, lam=lam)
            preds[label] = pred
            ev[label] = evaluate(te, pred, tr)
            ev[label]["fallback_direct_ou_impute"] = fb
            log(f"  {name} {label} : paire {ev[label]['paire_non_ordonnee']:.3f} "
                f"(ordonnee {ev[label]['paire_ordonnee']:.3f}) | valeur ±0,10 "
                f"{ev[label]['valeur_pm010']:.3f} | d_sat ±0,10 {ev[label]['dsat_pm010']:.3f} "
                f"| MAE d_div {ev[label]['mae_d_div']:.3f} | MAE Delta {ev[label]['mae_delta']:.3f} "
                f"| 3-voies {ev[label]['three_way']['acc']} "
                f"(n={ev[label]['three_way']['n']}, maj {ev[label]['three_way']['acc_majorite']:.3f}) "
                f"| MFA exact snappe {ev[label]['mfa']['exact_snappe']}")
        results[name] = ev
        if store_loco:
            return preds
        return None

    # --- PRIMAIRE : LOCO ---
    log("--- LOCO (PRIMAIRE, poole 222 runs) ---")
    loco_preds = {label: np.full((n_runs, len(TARGETS)), np.nan) for label in LABELS}
    loco_per_fold = {}
    for coh in cohorts:
        te = [i for i in all_idx if rows[i]["cohort"] == coh]
        tr = [i for i in all_idx if rows[i]["cohort"] != coh]
        for label in LABELS:
            pred, _ = fit_predict(label, tr, te)
            loco_preds[label][te] = pred[te]
        loco_per_fold[coh] = {label: {"paire": evaluate(te, loco_preds[label], tr)["paire_non_ordonnee"],
                                      "valeur": evaluate(te, loco_preds[label], tr)["valeur_pm010"]}
                              for label in LABELS}
    ev_loco = {}
    for label in LABELS:
        ev_loco[label] = evaluate(all_idx, loco_preds[label], all_idx)
        e = ev_loco[label]
        log(f"  LOCO {label} : paire {e['paire_non_ordonnee']:.3f} "
            f"(ordonnee {e['paire_ordonnee']:.3f}) | valeur ±0,10 {e['valeur_pm010']:.3f} "
            f"| d_sat ±0,10 {e['dsat_pm010']:.3f} | MAE d_div {e['mae_d_div']:.3f} "
            f"| MAE Delta {e['mae_delta']:.3f} | 3-voies {e['three_way']['acc']} "
            f"(n={e['three_way']['n']}, maj {e['three_way']['acc_majorite']:.3f}) "
            f"| MFA exact snappe {e['mfa']['exact_snappe']}")
        for t in TARGETS:
            pt = e["per_target"][t]
            log(f"      {t} : R2={pt['R2'] if pt['R2'] is None else round(pt['R2'], 3)} "
                f"MAE={pt['MAE'] if pt['MAE'] is None else round(pt['MAE'], 3)} "
                f"r={pt['r'] if pt['r'] is None else round(pt['r'], 3)} n={pt['n']}")
    for coh in cohorts:
        log(f"  LOCO pli {coh} : " + " | ".join(
            f"{lab} {loco_per_fold[coh][lab]['paire']:.2f}/{loco_per_fold[coh][lab]['valeur']:.2f}"
            for lab in LABELS if lab != "B0"))
    results["LOCO"] = ev_loco
    results["LOCO_par_pli"] = loco_per_fold

    # --- SECONDAIRE A : split aleatoire par matrice, graine 42 ---
    rng = np.random.default_rng(42)
    mats = sorted(distinct.keys())
    by_coh = defaultdict(list)
    for m in mats:
        by_coh[cohort_of(m)].append(m)
    train_mats, test_mats = set(), set()
    for coh, ms in by_coh.items():
        ms = list(ms)
        rng.shuffle(ms)
        k = int(round(0.70 * len(ms)))
        train_mats.update(ms[:k])
        test_mats.update(ms[k:])
    tr = [i for i in all_idx if rows[i]["csv_path"] in train_mats]
    te = [i for i in all_idx if rows[i]["csv_path"] in test_mats]
    log(f"Split aleatoire par matrice : train {len(train_mats)} matrices / {len(tr)} runs ; "
        f"test {len(test_mats)} matrices / {len(te)} runs")
    log("--- SPLIT_MATRICES_70_30 ---")
    full_eval("SPLIT_MATRICES_70_30", tr, te)

    # --- SECONDAIRE B : version v6.1 -> v6.2 (FUITE NOMMEE) ---
    tr = [i for i in all_idx if rows[i]["version"].startswith("v6.1")]
    te = [i for i in all_idx if rows[i]["version"].startswith("v6.2")]
    log("Hold-out version v6.1 -> v6.2 : FUITE — memes matrices des deux cotes, "
        "diagnostic seulement, ne compte pas pour le critere.")
    log("--- VERSION_v61_v62_FUITE ---")
    full_eval("VERSION_v61_v62_FUITE", tr, te)

    # --- En-echantillon (reference seulement) ---
    log("--- EN_ECHANTILLON (reference, surajustement possible) ---")
    full_eval("EN_ECHANTILLON", all_idx, all_idx)

    # --- meilleur modele honnete (regle deterministe : max valeur LOCO, puis paire) ---
    honest = [l for l in LABELS if l != "B0"]
    best = max(honest, key=lambda l: (ev_loco[l]["valeur_pm010"] or 0,
                                      ev_loco[l]["paire_non_ordonnee"] or 0))
    log(f"Meilleur modele honnete (LOCO, max valeur puis paire) : {best}")
    results["meilleur_modele_honnete"] = best

    # --- D4 : derive prefixe / demi-flux ---
    drift = {}
    for t in TARGETS:
        dp, dh = [], []
        for i in all_idx:
            y = Y[i, TARGETS.index(t)]
            if not np.isfinite(y):
                continue
            if np.isfinite(rows[i]["pref"][t]):
                dp.append(abs(rows[i]["pref"][t] - y))
            if np.isfinite(rows[i]["half"][t]):
                dh.append(abs(rows[i]["half"][t] - y))
        dp, dh = np.array(dp), np.array(dh)
        drift[t] = {"prefixe": {"n": int(len(dp)), "frac_pm010": float((dp <= 0.10).mean()) if len(dp) else None,
                                "moy_ecart": float(dp.mean()) if len(dp) else None,
                                "med_ecart": float(np.median(dp)) if len(dp) else None},
                    "demi_flux": {"n": int(len(dh)), "frac_pm010": float((dh <= 0.10).mean()) if len(dh) else None,
                                  "moy_ecart": float(dh.mean()) if len(dh) else None,
                                  "med_ecart": float(np.median(dh)) if len(dh) else None}}
        log(f"  Derive {t} : prefixe <=0,10 {drift[t]['prefixe']['frac_pm010']:.3f} "
            f"(moy {drift[t]['prefixe']['moy_ecart']:.3f}) | demi-flux <=0,10 "
            f"{drift[t]['demi_flux']['frac_pm010']:.3f} (moy {drift[t]['demi_flux']['moy_ecart']:.3f})")
    results["DERIVE_PREFIXE_DEMI_FLUX"] = drift

    # --- D5 : residu intra-groupe (LOCO, meilleur modele) ---
    def intra_group(pred_medians):
        groups = defaultdict(list)
        for i in all_idx:
            r = rows[i]
            key = (r["mask"], round(r["targets"]["MFA"], 3) if r["targets"]["MFA"] is not None else None,
                   int(r["n"]))
            groups[key].append(i)
        out = {}
        for key, idxs in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:2]:
            if len(idxs) < 5:
                continue
            pd_, td_ = [], []
            for i in idxs:
                pdv = {t: pred_medians[i, TARGETS.index(t)] for t in DIV}
                _, ddiv_pred = derive_pair_ddiv(pdv, rows[i]["mask_L"], rows[i]["mask_P"])
                if ddiv_pred is None:
                    continue
                pd_.append(ddiv_pred)
                td_.append(rows[i]["d_div"])
            out[str(key)] = {"n": len(idxs), "r_pred_vrai": pearson_r(pd_, td_),
                             "resid_sd": float(np.std(np.array(td_) - np.array(pd_))) if len(td_) > 1 else None,
                             "d_div_etendue": [float(np.min(td_)), float(np.max(td_))]}
        xs, ys = [], []
        for key, idxs in groups.items():
            if len(idxs) < 10:
                continue
            pd_, td_ = [], []
            for i in idxs:
                pdv = {t: pred_medians[i, TARGETS.index(t)] for t in DIV}
                _, ddiv_pred = derive_pair_ddiv(pdv, rows[i]["mask_L"], rows[i]["mask_P"])
                if ddiv_pred is None:
                    continue
                pd_.append(ddiv_pred)
                td_.append(rows[i]["d_div"])
            pd_, td_ = np.array(pd_), np.array(td_)
            xs.extend(list(pd_ - pd_.mean()))
            ys.extend(list(td_ - td_.mean()))
        out["poole_groupes_ge10"] = {"r_intra_groupe": pearson_r(xs, ys), "n": len(xs)}
        return out
    ig = intra_group(loco_preds[best])
    results["INTRA_GROUPE_LOCO"] = {best: ig}
    log(f"--- Intra-groupe LOCO {best} ---")
    for k, v in ig.items():
        log(f"  {k} : {v}")

    # --- D6 : paires predites identiques reel vs nul (LOCO, meilleur modele) ---
    dirset = {r["dir"]: i for i, r in enumerate(rows)}
    rn_pairs = []
    for i, r in enumerate(rows):
        if r["dir"].endswith("_nul"):
            continue
        j = dirset.get(r["dir"] + "_nul")
        if j is not None:
            rn_pairs.append((i, j))
    same = 0
    for i, j in rn_pairs:
        def ppred(idx):
            pdv = {t: loco_preds[best][idx, TARGETS.index(t)] for t in DIV}
            pair_pred, _ = derive_pair_ddiv(pdv, rows[idx]["mask_L"], rows[idx]["mask_P"])
            return None if pair_pred is None else set(pair_pred)
        if ppred(i) is not None and ppred(i) == ppred(j):
            same += 1
    results["PAIRE_PREDITE_IDENTIQUE_REEL_NUL_LOCO"] = {
        "modele": best, "n_paires": len(rn_pairs), "identiques": same,
        "fraction": same / len(rn_pairs) if rn_pairs else None}
    log(f"Paire predite identique reel/nul (LOCO {best}) : {same}/{len(rn_pairs)} "
        f"= {same / len(rn_pairs):.3f}" if rn_pairs else "aucune paire reel/nul")

    # --- D7 : deduplication 153 runs (sans rep2, sans doublons div_sorted) ---
    seen, dedup_idx = set(), []
    for i, r in enumerate(rows):
        if "rep2" in r["dir"]:
            continue
        key = r["div_sorted"]
        if key in seen:
            continue
        seen.add(key)
        dedup_idx.append(i)
    log(f"Dedup : {len(dedup_idx)} runs (attendu 153, sans rep2, sans doublons div_sorted)")
    results["DEDUP"] = {"n_runs": len(dedup_idx), "attendu": 153}
    # LOCO restreint aux runs dedup : on reutilise les predictions LOCO deja calculees
    ev_dedup = evaluate(dedup_idx, loco_preds[best], all_idx)
    results["DEDUP_LOCO"] = {best: ev_dedup}
    log(f"  DEDUP LOCO {best} : paire {ev_dedup['paire_non_ordonnee']:.3f} | "
        f"valeur {ev_dedup['valeur_pm010']:.3f} | MAE d_div {ev_dedup['mae_d_div']:.3f}")

    # --- D8 : variante masque ignore (k=6 force), LOCO meilleur modele ---
    def evaluate_no_mask(pred_medians):
        ok_pair = ok_val = 0
        n = 0
        for i in all_idx:
            r = rows[i]
            pdv = {t: (pred_medians[i, TARGETS.index(t)]
                       if np.isfinite(pred_medians[i, TARGETS.index(t)]) else None) for t in DIV}
            pair_pred, ddiv_pred = derive_pair_ddiv(pdv, True, True)
            if pair_pred is None or ddiv_pred is None:
                continue
            n += 1
            if set(pair_pred) == r["pair_set"]:
                ok_pair += 1
            if abs(ddiv_pred - r["d_div"]) <= 0.10:
                ok_val += 1
        return {"n": n, "paire": ok_pair / n if n else None, "valeur": ok_val / n if n else None}
    ev_nomask = evaluate_no_mask(loco_preds[best])
    results["VARIANTE_MASQUE_IGNORE_LOCO"] = {best: ev_nomask}
    log(f"  Masque ignore LOCO {best} : paire {ev_nomask['paire']:.3f} | "
        f"valeur {ev_nomask['valeur']:.3f}")

    # --- sensibilite lambda S1r (LOCO) ---
    for lam in (1.0, 100.0):
        lp = {label: np.full((n_runs, len(TARGETS)), np.nan) for label in ["S1r"]}
        for coh in cohorts:
            te = [i for i in all_idx if rows[i]["cohort"] == coh]
            tr = [i for i in all_idx if rows[i]["cohort"] != coh]
            pred, _ = fit_predict("S1r", tr, te, lam=lam)
            lp["S1r"][te] = pred[te]
        e = evaluate(all_idx, lp["S1r"], all_idx)
        results.setdefault("SENSIBILITE_LAMBDA_LOCO", {})[f"S1r_lam{lam:g}"] = {
            "paire": e["paire_non_ordonnee"], "valeur": e["valeur_pm010"],
            "mae_d_div": e["mae_d_div"]}
        log(f"  Sensibilite lambda S1r lam={lam:g} LOCO : paire {e['paire_non_ordonnee']:.3f} | "
            f"valeur {e['valeur_pm010']:.3f}")

    # --- verdict ---
    def passes(ev):
        return ((ev["paire_non_ordonnee"] or 0) >= 0.90 and (ev["valeur_pm010"] or 0) >= 0.90)
    verdicts = {}
    for label in honest:
        loco_ok = passes(results["LOCO"][label])
        split_ok = passes(results["SPLIT_MATRICES_70_30"][label])
        verdicts[label] = {"LOCO": loco_ok, "SPLIT": split_ok, "les_deux": bool(loco_ok and split_ok)}
    elucide = any(v["les_deux"] for v in verdicts.values())
    results["verdicts_modeles"] = verdicts
    results["ELUCIDE"] = bool(elucide)
    log(f"VERDICT : ELUCIDE = {elucide} (criteres : paires >= 90% ET valeurs >= 90%, "
        f"LOCO et split par matrice)")
    for label in honest:
        log(f"  {label} : LOCO {results['LOCO'][label]['paire_non_ordonnee']:.3f}/"
            f"{results['LOCO'][label]['valeur_pm010']:.3f} | SPLIT "
            f"{results['SPLIT_MATRICES_70_30'][label]['paire_non_ordonnee']:.3f}/"
            f"{results['SPLIT_MATRICES_70_30'][label]['valeur_pm010']:.3f} | "
            f"les_deux={verdicts[label]['les_deux']}")

    with open(os.path.join(BASE, "v62_delta_series_857.json"), "w") as fh:
        json.dump(results, fh, indent=1, default=str)
    log("JSON ecrit : v62_delta_series_857.json")
    log("=== FIN §8.57 ===")
    LOG.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
