#!/usr/bin/env python3
"""Chantier 3 (suite) — Elucider Delta par modelisation des magnitudes.
PROTOCOLE GELÉ : PROTOCOL_delta_magnitudes.md (19 nov. 2026).
Lecture SEULE. Aucun run du pipeline, aucune modification d'un code.
Cibles : les 13 medianes par estimateur (v62_delta_levels.csv, parsees
depuis div_sorted/sat_sorted). Predicteurs : resumes numeriques calcules
UNIQUEMENT sur les matrices de flux d'entree (metadata.csv_path).
INTERDIT : df_feat.csv (circulaire), tout autre champ de master_results.json,
noms de flux, etiquette reel/nul, famille comme variable du modele.
Modeles geles : M1 ridge lam=10 traits REDUITS (primaire), M2 ridge lam=10
traits COMPLETS, M3 kNN k=5 reduits, M4 meilleur trait unique (OLS),
B0 constante = mediane du train.
Hold-outs geles : PRIMAIRE leave-one-cohort-out (LOCO, unite = matrice),
SECONDAIRE A split aleatoire par matrice (graine 42, 70/30),
SECONDAIRE B version v6.1 -> v6.2 (DIAGNOSTIC, FUITE NOMMEE : memes
matrices des deux cotes, ne compte pas pour le critere), en-echantillon
(reference seulement).
Critere : ELUCIDE ssi au moins un modele M1-M4 atteint paires >= 90 % ET
valeurs ±0,10 >= 90 % sur LOCO poole ET sur le split aleatoire par matrice.
Sorties : v62_delta_magnitudes.log, .json, .md,
v62_delta_magnitudes_flux_features.csv.
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
LOG = []


def log(msg):
    print(msg, flush=True)
    LOG.append(msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_sorted(s):
    """'Nom=val;Nom=val' -> dict nom -> float."""
    out = {}
    if not s:
        return out
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
    """Regles gelees, dans CET ordre (premier motif gagne)."""
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


def ranks_average(x):
    """Rangs moyens (ties moyennes), 1..n."""
    x = np.asarray(x, dtype=float)
    order = np.argsort(x, kind="mergesort")
    r = np.empty(len(x), dtype=float)
    sx = x[order]
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and sx[j + 1] == sx[i]:
            j += 1
        r[order[i:j + 1]] = 0.5 * (i + j) + 1.0
        i = j + 1
    return r


def pearson_r(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3 or a.std() == 0 or b.std() == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def flux_features(df):
    """Resumes geles (§3) sur une matrice de flux. 1re colonne = controle."""
    cols = list(df.columns)
    ctrl = pd.to_numeric(df[cols[0]], errors="coerce").to_numpy(dtype=float)
    flux_df = df[cols[1:]].apply(pd.to_numeric, errors="coerce")
    flux_df = flux_df.dropna(axis=1, how="all")
    X = flux_df.to_numpy(dtype=float)  # n x p, lignes = ordre du controle
    n, p = X.shape
    idx = np.arange(n, dtype=float)
    # --- traits du controle ---
    ctrl_fin = ctrl[np.isfinite(ctrl)]
    is_step = 0
    if len(ctrl_fin) == n and n > 1:
        if np.allclose(np.sort(ctrl_fin), np.arange(n)):
            is_step = 1
    ctrl_feats = [float(len(np.unique(ctrl_fin))), float(np.ptp(ctrl_fin)) if len(ctrl_fin) else 0.0,
                  float(np.std(ctrl_fin)) if len(ctrl_fin) > 1 else 0.0, float(is_step)]
    # --- 13 statistiques par flux ---
    per_flux = []
    for j in range(p):
        col = X[:, j]
        mask = np.isfinite(col)
        x = col[mask]
        pos = np.where(mask)[0].astype(float)
        if len(x) < 3:
            per_flux.append([0.0] * 13)
            continue
        mu, sd = float(np.mean(x)), float(np.std(x, ddof=1)) if len(x) > 1 else 0.0
        z = (x - mu) / sd if sd > 0 else np.zeros_like(x)
        skew = float(np.mean(z ** 3)) if sd > 0 else 0.0
        kurt = float(np.mean(z ** 4) - 3.0) if sd > 0 else 0.0
        ac1 = pearson_r(x[:-1], x[1:])
        d = np.diff(x)
        drift = float(abs(x[-1] - x[0]) / sd) if sd > 0 else 0.0
        rho = pearson_r(ranks_average(x), pos)
        ridx = pearson_r(x, pos)
        per_flux.append([mu, sd, float(np.min(x)), float(np.max(x)),
                         float(np.max(x) - np.min(x)), skew, kurt,
                         ac1 if ac1 is not None else 0.0,
                         float(np.mean(np.abs(d))) if len(d) else 0.0,
                         float(np.std(d)) if len(d) > 1 else 0.0,
                         drift, rho if rho is not None else 0.0,
                         ridx if ridx is not None else 0.0])
    per_flux = np.array(per_flux)  # p x 13
    agg_mean = np.mean(per_flux, axis=0)
    agg_sd = np.std(per_flux, axis=0, ddof=1) if p > 1 else np.zeros(13)
    agg_min = np.min(per_flux, axis=0)
    agg_max = np.max(per_flux, axis=0)
    agg_med = np.median(per_flux, axis=0)
    # --- traits inter-flux ---
    if p >= 2:
        with np.errstate(invalid="ignore"):
            C = np.corrcoef(X.T)
        C = np.nan_to_num(C, nan=0.0)
        iu = np.triu_indices(p, k=1)
        rvals = C[iu]
        eig = np.linalg.eigvalsh(C)
        eig = np.sort(eig)[::-1]
        tot = float(np.sum(eig)) if np.sum(eig) > 0 else 1.0
        pc1 = float(eig[0] / tot) if len(eig) else 0.0
        pc2 = float(eig[1] / tot) if len(eig) > 1 else 0.0
        evec = np.linalg.eigh(C)[1][:, -1]
        mean_abs_load = float(np.mean(np.abs(evec)))
        cross = [float(np.mean(np.abs(rvals))), float(np.std(rvals)),
                 float(np.mean(np.abs(rvals) > 0.8)), pc1, pc2, mean_abs_load]
        # 7e trait gele : part de variance PC1+PC2 (ajout fige : somme pc1+pc2)
        cross.append(float(pc1 + pc2))
    else:
        cross = [0.0] * 7
    glob_feats = [float(n), float(p), float(n * p), float(math.log(n)) if n > 0 else 0.0]
    reduced = list(agg_mean) + list(agg_sd) + cross + ctrl_feats + glob_feats
    full = list(agg_mean) + list(agg_sd) + list(agg_min) + list(agg_max) + list(agg_med) \
        + cross + ctrl_feats + glob_feats
    # indices des traits invariants par permutation des lignes (pour §6.5) :
    # dans REDUIT : agg_mean/agg_sd des stats 0..6 (mu,sd,min,max,etendue,skew,kurt)
    # + cross (6 premiers sont invariants ; le 7e = somme, invariant aussi)
    # + ctrl (invariant : controle intact) + globaux. Sensibles a l'ordre :
    # agg des stats 7..12 (ac1, |d|, sd d, derive, rho, ridx).
    return {"reduced": np.array(reduced, dtype=float),
            "full": np.array(full, dtype=float),
            "n": n, "p": p,
            "per_flux_order_sensitive": per_flux[:, 7:13],
            "per_flux_invariant": per_flux[:, 0:7]}


# ----------------------------------------------------------------- chargement
def main():
    log("=== Chantier 3 (suite) — modelisation des magnitudes (PROTOCOL_delta_magnitudes.md) ===")
    # SHA pipelines (lecture seule, verification).
    for name, path in [("v6.2", os.path.join(BASE, "..", "biophysique-hp35", "universal_v6.2.0_cohen.py")),
                       ("v6.1", os.path.join(BASE, "..", "biophysique-hp35", "universal_v6.1.0_cohen.py")),
                       ("v6", os.path.join(BASE, "..", "biophysique-hp35", "universal_v6.0.0_cohen.py"))]:
        if os.path.exists(path):
            log(f"SHA pipeline {name} : {sha256_file(path)}")
        else:
            log(f"Pipeline {name} introuvable : {path}")
    log(f"SHA protocole : {sha256_file(os.path.join(BASE, 'PROTOCOL_delta_magnitudes.md'))}")

    levels = list(csv.DictReader(open(os.path.join(BASE, "v62_delta_levels.csv"))))
    log(f"Runs lus (v62_delta_levels.csv) : {len(levels)}")
    rows = []
    missing_json, missing_csvpath = [], []
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
        div = parse_sorted(r["div_sorted"])
        sat = parse_sorted(r["sat_sorted"])
        if sorted(div.keys()) != sorted([k for k in DIV if k in div]) and len(div) < 4:
            log(f"ATTENTION {d} : div_sorted incomplet {sorted(div.keys())}")
        # verification identite d_div / d_sat depuis les medianes parsees
        ds = sorted(div.values())
        k = len(ds)
        if k % 2 == 0:
            ddiv_calc = (ds[k // 2 - 1] + ds[k // 2]) / 2.0
        else:
            ddiv_calc = ds[k // 2]
        ss = sorted(sat.values())
        dsat_calc = ss[3] if len(ss) >= 4 else None
        rows.append({"dir": d, "version": r["version"], "n": float(r["n"]),
                     "control": r["control"], "mask": r["mask"],
                     "mask_L": r["mask"][0] == "L", "mask_P": r["mask"][1] == "P",
                     "d_div": float(r["d_div"]), "d_sat": float(r["d_sat"]),
                     "delta": float(r["delta"]), "pair": r["pair"],
                     "pair_set": set(r["pair"].split("+")) if r["pair"] else set(),
                     "div": div, "sat": sat, "ddiv_calc": ddiv_calc,
                     "dsat_calc": dsat_calc, "csv_path": cp,
                     "cohort": cohort_of(cp),
                     "targets": {t: (div.get(t) if t in DIV else sat.get(t)) for t in TARGETS}})
    log(f"JSON manquants : {missing_json} ; csv_path manquants : {missing_csvpath}")
    bad_div = [r for r in rows if abs(r["d_div"] - r["ddiv_calc"]) > 1e-3]
    bad_sat = [r for r in rows if r["dsat_calc"] is None or abs(r["d_sat"] - r["dsat_calc"]) > 1e-3]
    log(f"Verification identite : d_div ecart > 1e-3 sur {len(bad_div)}/"
        f"{len(rows)} ; d_sat ecart > 1e-3 sur {len(bad_sat)}/{len(rows)}")
    if bad_div or bad_sat:
        log("ARRET : identite non verifiee (protocole §2.1).")
        return 1
    # cibles manquantes ?
    miss_t = [(r["dir"], t) for r in rows for t in TARGETS if r["targets"][t] is None]
    log(f"Cibles manquantes (membre absent = masque) : {len(miss_t)} "
        f"(attendu : Levina/PH absents uniquement) : {Counter(t for _, t in miss_t)}")
    unexpected = [m for m in miss_t if m[1] not in ("LevinaBickel", "PersistentHomology")]
    if unexpected:
        log(f"ARRET : cible manquante inattendue : {unexpected}")
        return 1

    # --- matrices distinctes : existence, SHA, n, traits ---
    distinct = {}
    for r in rows:
        distinct.setdefault(r["csv_path"], []).append(r["dir"])
    log(f"Matrices distinctes : {len(distinct)} (pour {len(rows)} runs)")
    log(f"Cohortes (runs) : {dict(Counter(r['cohort'] for r in rows))}")
    log(f"Cohortes (matrices distinctes) : {dict(Counter(cohort_of(c) for c in distinct))}")
    if "INCONNU" in [cohort_of(c) for c in distinct]:
        log("ARRET : cohorte INCONNU.")
        return 1
    feat_by_csv = {}
    sha_by_csv = {}
    n_mismatch = []
    for cp in sorted(distinct):
        path = cp if os.path.isabs(cp) else os.path.join(BASE, cp)
        if not os.path.exists(path):
            log(f"ARRET : matrice introuvable : {cp}")
            return 1
        sha_by_csv[cp] = sha256_file(path)
        df = pd.read_csv(path)
        feats = flux_features(df)
        feat_by_csv[cp] = feats
        for d in distinct[cp]:
            r = next(x for x in rows if x["dir"] == d)
            if feats["n"] != int(r["n"]):
                n_mismatch.append((d, cp, feats["n"], int(r["n"])))
    log(f"Matrices lues : {len(feat_by_csv)} ; ecarts n (matrice vs run) : {n_mismatch}")
    if n_mismatch:
        log("ARRET : n matrice != n run (protocole §2.2).")
        return 1
    for r in rows:
        f = feat_by_csv[r["csv_path"]]
        r["x_red"] = f["reduced"]
        r["x_full"] = f["full"]
        r["p_flux"] = f["p"]
    n_red = len(rows[0]["x_red"])
    n_full = len(rows[0]["x_full"])
    log(f"Traits : REDUIT={n_red} (attendu 41), COMPLET={n_full} (attendu 80)")
    assert n_red == 41 and n_full == 80, "taille des traits inattendue"
    # ecriture traits par matrice (provenance)
    with open(os.path.join(BASE, "v62_delta_magnitudes_flux_features.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["csv_path", "cohort", "sha256", "n", "p_flux", "n_runs"] +
                   [f"red_{i}" for i in range(n_red)])
        for cp in sorted(distinct):
            f = feat_by_csv[cp]
            w.writerow([cp, cohort_of(cp), sha_by_csv[cp], f["n"], f["p"], len(distinct[cp])] +
                       [f"{v:.10g}" for v in f["reduced"]])

    # --- controle d'invariance reel/nul (§3) ---
    pairs_rn = []
    for cp in sorted(distinct):
        if cp.endswith("_nul.csv"):
            real = cp[:-len("_nul.csv")] + ".csv"
            if real in distinct:
                pairs_rn.append((real, cp))
    log(f"Paires reel/nul (matrices) : {len(pairs_rn)}")
    inv_ok = 0
    for real, nul in pairs_rn:
        fr, fn = feat_by_csv[real], feat_by_csv[nul]
        # invariants : per_flux stats 0..6 (moy, sd, min, max, etendue, skew, kurt)
        # + cross + ctrl + globaux. Comparaison via traits REDUITS en excluant
        # les agregats des stats sensibles a l'ordre (indices 7..12 x mean/sd).
        # REDUIT = [agg_mean(13), agg_sd(13), cross(7), ctrl(4), glob(4)].
        def inv_vec(f):
            v = f["reduced"].copy()
            idx = list(range(7, 13)) + list(range(13 + 7, 13 + 13))
            return np.delete(v, idx)
        if np.allclose(inv_vec(fr), inv_vec(fn), atol=1e-9, rtol=0):
            inv_ok += 1
        else:
            log(f"  invariance NON verifiee : {real} vs {nul} "
                f"(max |diff| = {np.max(np.abs(inv_vec(fr) - inv_vec(fn))):.3g})")
    log(f"Traits invariants egaux reel/nul a 1e-9 pres : {inv_ok}/{len(pairs_rn)}")

    # ------------------------------------------------------------- modeles
    def standardize(Xtr, Xte):
        mu = np.mean(Xtr, axis=0)
        sd = np.std(Xtr, axis=0)
        sd = np.where(sd == 0, 1.0, sd)
        return (Xtr - mu) / sd, (Xte - mu) / sd, mu, sd

    def fit_ridge(Xtr, Ytr, lam):
        Xc = Xtr - np.mean(Xtr, axis=0)
        Yc = Ytr - np.mean(Ytr, axis=0)
        A = Xc.T @ Xc + lam * np.eye(Xtr.shape[1])
        W = np.linalg.solve(A, Xc.T @ Yc)
        return {"mu_x": np.mean(Xtr, axis=0), "mu_y": np.mean(Ytr, axis=0), "W": W}

    def pred_ridge(model, Xte):
        return (Xte - model["mu_x"]) @ model["W"] + model["mu_y"]

    def fit_knn(Xtr, Ytr, k=5):
        return {"Xtr": Xtr, "Ytr": Ytr, "k": k}

    def pred_knn(model, Xte):
        out = np.empty((len(Xte), model["Ytr"].shape[1]))
        for i, x in enumerate(Xte):
            d = np.sqrt(np.sum((model["Xtr"] - x) ** 2, axis=1))
            nn = np.argsort(d)[:model["k"]]
            out[i] = np.mean(model["Ytr"][nn], axis=0)
        return out

    def fit_m4(Xtr, Ytr):
        # meilleur trait unique par cible (|Pearson| sur le train)
        mods = []
        for j in range(Ytr.shape[1]):
            best, best_r = None, -1.0
            for f in range(Xtr.shape[1]):
                r = pearson_r(Xtr[:, f], Ytr[:, j])
                if r is not None and abs(r) > best_r:
                    best, best_r = f, abs(r)
            if best is None:
                mods.append(None)
                continue
            x, y = Xtr[:, best], Ytr[:, j]
            ok = np.isfinite(x) & np.isfinite(y)
            if ok.sum() < 3 or x[ok].std() == 0:
                mods.append(None)
                continue
            a = np.polyfit(x[ok], y[ok], 1)
            mods.append((best, a))
        return mods

    def pred_m4(mods, Xte, Ytr_med):
        out = np.empty((len(Xte), len(mods)))
        for j, m in enumerate(mods):
            if m is None:
                out[:, j] = Ytr_med[j]
            else:
                f, a = m
                out[:, j] = a[0] * Xte[:, f] + a[1]
        return out

    def derive_pair_ddiv(pred_div, mask_L, mask_P):
        """pred_div : dict nom -> valeur predite (6). Applique le masque vrai."""
        present = []
        for nm in DIV:
            if nm == "LevinaBickel" and not mask_L:
                continue
            if nm == "PersistentHomology" and not mask_P:
                continue
            present.append((pred_div[nm], nm))
        present.sort()
        k = len(present)
        if k >= 2 and k % 2 == 0:
            pair = (present[k // 2 - 1][1], present[k // 2][1])
            ddiv = (present[k // 2 - 1][0] + present[k // 2][0]) / 2.0
        elif k >= 1:
            pair = (present[k // 2][1],)
            ddiv = present[k // 2][0]
        else:
            pair, ddiv = (), float("nan")
        return pair, ddiv

    def derive_dsat(pred_sat):
        vals = sorted(pred_sat[nm] for nm in SAT)
        return vals[3]

    def evaluate(idxs, pred_medians):
        """pred_medians : array n_runs x 13 (ordre TARGETS). Retourne dict."""
        ok_pair = ok_pair_ord = ok_val = ok_dsat = 0
        n = 0
        errs_div, errs_dsat, errs_delta = [], [], []
        for i in idxs:
            r = rows[i]
            pd = {t: pred_medians[i, TARGETS.index(t)] for t in DIV}
            ps = {t: pred_medians[i, TARGETS.index(t)] for t in SAT}
            pair_pred, ddiv_pred = derive_pair_ddiv(pd, r["mask_L"], r["mask_P"])
            dsat_pred = derive_dsat(ps)
            n += 1
            if set(pair_pred) == r["pair_set"]:
                ok_pair += 1
            if tuple(pair_pred) == tuple(r["pair"].split("+")) if r["pair"] else False:
                ok_pair_ord += 1
            if abs(ddiv_pred - r["d_div"]) <= 0.10:
                ok_val += 1
            if abs(dsat_pred - r["d_sat"]) <= 0.10:
                ok_dsat += 1
            errs_div.append(abs(ddiv_pred - r["d_div"]))
            errs_dsat.append(abs(dsat_pred - r["d_sat"]))
            errs_delta.append(abs((ddiv_pred - dsat_pred) - r["delta"]))
        return {"n": n, "paire_non_ordonnee": ok_pair / n if n else None,
                "paire_ordonnee": ok_pair_ord / n if n else None,
                "valeur_pm010": ok_val / n if n else None,
                "dsat_pm010": ok_dsat / n if n else None,
                "mae_d_div": float(np.mean(errs_div)) if errs_div else None,
                "mae_d_sat": float(np.mean(errs_dsat)) if errs_dsat else None,
                "mae_delta": float(np.mean(errs_delta)) if errs_delta else None}

    def run_models(train_idx, test_idx):
        """Entraine M1, M2, M3, M4, B0 sur train_idx, predit test_idx.
        Les cibles manquantes (masque) sont exclues de l'entrainement
        cible par cible (les modeles sont par cible)."""
        Xtr_red = np.array([rows[i]["x_red"] for i in train_idx])
        Xte_red = np.array([rows[i]["x_red"] for i in test_idx])
        Xtr_full = np.array([rows[i]["x_full"] for i in train_idx])
        Xte_full = np.array([rows[i]["x_full"] for i in test_idx])
        Ytr = np.array([[rows[i]["targets"][t] if rows[i]["targets"][t] is not None else np.nan
                         for t in TARGETS] for i in train_idx])
        Yte_true = np.array([[rows[i]["targets"][t] if rows[i]["targets"][t] is not None else np.nan
                              for t in TARGETS] for i in test_idx])
        Xtr_red_s, Xte_red_s, _, _ = standardize(Xtr_red, Xte_red)
        Xtr_full_s, Xte_full_s, _, _ = standardize(Xtr_full, Xte_full)
        out = {}
        # M1 / M2 : ridge par cible (lignes avec cible presente seulement)
        for label, Xtr_s, Xte_s in [("M1", Xtr_red_s, Xte_red_s), ("M2", Xtr_full_s, Xte_full_s)]:
            pred = np.empty((len(test_idx), len(TARGETS)))
            for j in range(len(TARGETS)):
                ok = np.isfinite(Ytr[:, j])
                model = fit_ridge(Xtr_s[ok], Ytr[ok, j:j + 1], lam=10.0)
                pred[:, j] = pred_ridge(model, Xte_s)[:, 0]
            out[label] = pred
        # M3 : kNN (cibles manquantes : voisins sans la cible ignores)
        pred = np.empty((len(test_idx), len(TARGETS)))
        for j in range(len(TARGETS)):
            ok = np.isfinite(Ytr[:, j])
            model = fit_knn(Xtr_red_s[ok], Ytr[ok, j:j + 1], k=5)
            pred[:, j] = pred_knn(model, Xte_red_s)[:, 0]
        out["M3"] = pred
        # M4 : meilleur trait unique (sur traits REDUITS bruts, non standardises)
        mods = fit_m4(Xtr_red, Ytr)
        Ytr_med = np.nanmedian(Ytr, axis=0)
        out["M4"] = pred_m4(mods, Xte_red, Ytr_med)
        # B0 : mediane du train
        out["B0"] = np.tile(Ytr_med, (len(test_idx), 1))
        return out, Yte_true

    def per_target_r2_mae(test_idx, pred, Yte_true):
        res = {}
        for j, t in enumerate(TARGETS):
            ok = np.isfinite(Yte_true[:, j])
            y, p = Yte_true[ok, j], pred[ok, j]
            if len(y) < 3:
                res[t] = {"R2": None, "MAE": None, "n": int(ok.sum())}
                continue
            ss_res = float(np.sum((y - p) ** 2))
            ss_tot = float(np.sum((y - np.mean(y)) ** 2))
            res[t] = {"R2": (1.0 - ss_res / ss_tot) if ss_tot > 0 else None,
                      "MAE": float(np.mean(np.abs(y - p))), "n": int(ok.sum())}
        return res

    def three_way(idxs, pred_medians, majority_globale):
        """k=6, LocalPCA 3e vraie : lequel des 3 hauts est le plus petit.
        Reference : majorite GLOBALE (222 runs), pas ajustee sur le test."""
        ok = tot = 0
        labs = []
        for i in idxs:
            r = rows[i]
            if len(r["div"]) != 6:
                continue
            srt = sorted(r["div"].items(), key=lambda kv: kv[1])
            if srt[2][0] != "LocalPCA":
                continue
            true_min = min(("MFA", "LevinaBickel", "PCAIntrinsic"),
                           key=lambda nm: r["div"][nm])
            pred_min = min(("MFA", "LevinaBickel", "PCAIntrinsic"),
                           key=lambda nm: pred_medians[i, TARGETS.index(nm)])
            labs.append(true_min)
            tot += 1
            if pred_min == true_min:
                ok += 1
        maj_ok = sum(1 for x in labs if x == majority_globale) if labs else 0
        return {"n": tot, "acc": ok / tot if tot else None,
                "majorite_globale": majority_globale,
                "acc_majorite": maj_ok / tot if tot else None}

    def mfa_exact(idxs, pred_medians, train_mfa_values):
        ok = tot = 0
        snap_ok = 0
        for i in idxs:
            r = rows[i]
            true = r["targets"]["MFA"]
            if true is None:
                continue
            tot += 1
            p = pred_medians[i, TARGETS.index("MFA")]
            if abs(p - true) < 1e-9:
                ok += 1
            snapped = min(train_mfa_values, key=lambda v: abs(v - p))
            if abs(snapped - true) < 1e-9:
                snap_ok += 1
        return {"n": tot, "n_exact_brut": ok, "n_exact_snappe": snap_ok,
                "exact_brut": ok / tot if tot else None,
                "exact_snappe": snap_ok / tot if tot else None}

    def majorite_trois_voies_globale():
        labs = []
        for r in rows:
            if len(r["div"]) != 6:
                continue
            srt = sorted(r["div"].items(), key=lambda kv: kv[1])
            if srt[2][0] != "LocalPCA":
                continue
            labs.append(min(("MFA", "LevinaBickel", "PCAIntrinsic"),
                            key=lambda nm: r["div"][nm]))
        return Counter(labs).most_common(1)[0][0] if labs else None

    MAJ_3V = majorite_trois_voies_globale()
    log(f"Majorite globale 3-voies (lequel des 3 hauts est le plus petit) : {MAJ_3V}")

    # --- assemblage des predictions par hold-out ---
    all_idx = list(range(len(rows)))
    results = {"n_runs": len(rows),
               "n_matrices": len(distinct),
               "cohorts_runs": dict(Counter(r["cohort"] for r in rows)),
               "cohorts_matrices": dict(Counter(cohort_of(c) for c in distinct)),
               "paires_reel_nul": len(pairs_rn),
               "traits_invariants_egaux": [inv_ok, len(pairs_rn)]}

    def full_eval(name, train_idx, test_idx):
        preds, Yte_true = run_models(train_idx, test_idx)
        ev = {}
        for label, pred in preds.items():
            # pred est indexe sur test_idx ; evaluate attend des indices
            # globaux : on construit une matrice pleine n_runs x 13.
            full = np.full((len(rows), len(TARGETS)), np.nan)
            for k, i in enumerate(test_idx):
                full[i] = pred[k]
            ev[label] = evaluate(test_idx, full)
            ev[label]["per_target"] = per_target_r2_mae(test_idx, pred, Yte_true)
            ev[label]["three_way"] = three_way(test_idx, full, MAJ_3V)
            train_mfa = sorted(set(round(rows[i]["targets"]["MFA"], 3)
                                   for i in train_idx if rows[i]["targets"]["MFA"] is not None))
            ev[label]["mfa"] = mfa_exact(test_idx, full, train_mfa)
        results[name] = ev
        log(f"--- {name} (train={len(train_idx)}, test={len(test_idx)}) ---")
        for label in ["B0", "M1", "M2", "M3", "M4"]:
            e = ev[label]
            log(f"  {label} : paire {e['paire_non_ordonnee']:.3f} "
                f"(ordonnee {e['paire_ordonnee']:.3f}) | valeur ±0,10 {e['valeur_pm010']:.3f} "
                f"| d_sat ±0,10 {e['dsat_pm010']:.3f} | MAE d_div {e['mae_d_div']:.3f} "
                f"| MAE Delta {e['mae_delta']:.3f} | 3-voies {e['three_way']['acc']} "
                f"(n={e['three_way']['n']}, maj {e['three_way']['acc_majorite']:.3f}) "
                f"| MFA exact snappe {e['mfa']['exact_snappe']}")
        return preds, ev

    # LOCO (PRIMAIRE)
    cohorts = sorted(set(r["cohort"] for r in rows))
    loco_preds = {label: np.full((len(rows), len(TARGETS)), np.nan)
                  for label in ["B0", "M1", "M2", "M3", "M4"]}
    loco_per_fold = {}
    for coh in cohorts:
        te = [i for i in all_idx if rows[i]["cohort"] == coh]
        tr = [i for i in all_idx if rows[i]["cohort"] != coh]
        preds, _ = run_models(tr, te)
        for label in preds:
            for k, i in enumerate(te):
                loco_preds[label][i] = preds[label][k]
        loco_per_fold[coh] = {"n_test": len(te)}
        log(f"  LOCO pli {coh} : test={len(te)} runs, train={len(tr)}")
    ev_loco = {}
    for label in loco_preds:
        ev = evaluate(all_idx, loco_preds[label])
        ev["per_target"] = per_target_r2_mae(
            all_idx, loco_preds[label],
            np.array([[rows[i]["targets"][t] if rows[i]["targets"][t] is not None else np.nan
                       for t in TARGETS] for i in all_idx]))
        ev["three_way"] = three_way(all_idx, loco_preds[label], MAJ_3V)
        # MFA en LOCO : ensemble de snap = valeurs MFA du TRAIN de chaque
        # pli (pas l'ensemble global — sinon fuite dans le diagnostic).
        mfa_n = mfa_b = mfa_s = 0
        for coh in cohorts:
            te = [i for i in all_idx if rows[i]["cohort"] == coh]
            tr = [i for i in all_idx if rows[i]["cohort"] != coh]
            train_mfa = sorted(set(round(rows[i]["targets"]["MFA"], 3)
                                   for i in tr if rows[i]["targets"]["MFA"] is not None))
            m = mfa_exact(te, loco_preds[label], train_mfa)
            mfa_n += m["n"]
            mfa_b += m["n_exact_brut"]
            mfa_s += m["n_exact_snappe"]
        ev["mfa"] = {"n": mfa_n, "n_exact_brut": mfa_b, "n_exact_snappe": mfa_s,
                     "exact_brut": mfa_b / mfa_n if mfa_n else None,
                     "exact_snappe": mfa_s / mfa_n if mfa_n else None}
        ev_loco[label] = ev
        # par pli
        for coh in cohorts:
            te = [i for i in all_idx if rows[i]["cohort"] == coh]
            e = evaluate(te, loco_preds[label])
            loco_per_fold[coh][label] = {"paire": e["paire_non_ordonnee"],
                                         "valeur": e["valeur_pm010"]}
    results["LOCO"] = ev_loco
    results["LOCO_par_pli"] = loco_per_fold
    log("--- LOCO (PRIMAIRE, poole 222 runs) ---")
    for label in ["B0", "M1", "M2", "M3", "M4"]:
        e = ev_loco[label]
        log(f"  {label} : paire {e['paire_non_ordonnee']:.3f} "
            f"(ordonnee {e['paire_ordonnee']:.3f}) | valeur ±0,10 {e['valeur_pm010']:.3f} "
            f"| d_sat ±0,10 {e['dsat_pm010']:.3f} | MAE d_div {e['mae_d_div']:.3f} "
            f"| MAE Delta {e['mae_delta']:.3f} | 3-voies {e['three_way']['acc']} "
            f"(n={e['three_way']['n']}, maj {e['three_way']['acc_majorite']:.3f}) "
            f"| MFA exact snappe {e['mfa']['exact_snappe']}")
        for t in TARGETS:
            pt = e["per_target"][t]
            log(f"      {t} : R2={pt['R2'] if pt['R2'] is None else round(pt['R2'], 3)} "
                f"MAE={pt['MAE'] if pt['MAE'] is None else round(pt['MAE'], 3)} n={pt['n']}")
    for coh in cohorts:
        log(f"  LOCO pli {coh} : " +
            " | ".join(f"{lab} {loco_per_fold[coh][lab]['paire']:.2f}/"
                       f"{loco_per_fold[coh][lab]['valeur']:.2f}"
                       for lab in ["M1", "M2", "M3", "M4"]))

    # SECONDAIRE A : split aleatoire par matrice, graine 42
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
    log(f"Split aleatoire par matrice : train {len(train_mats)} matrices / "
        f"{len(tr)} runs ; test {len(test_mats)} matrices / {len(te)} runs")
    full_eval("SPLIT_MATRICES_70_30", tr, te)

    # SECONDAIRE B : version v6.1 -> v6.2 (FUITE NOMMEE)
    tr = [i for i in all_idx if rows[i]["version"].startswith("v6.1")]
    te = [i for i in all_idx if rows[i]["version"].startswith("v6.2")]
    log("Hold-out version v6.1 -> v6.2 : FUITE — memes matrices des deux cotes, "
        "diagnostic seulement, ne compte pas pour le critere.")
    full_eval("VERSION_v61_v62_FUITE", tr, te)

    # En-echantillon (reference seulement)
    full_eval("EN_ECHANTILLON", all_idx, all_idx)

    # --- residu intra-groupe (LOCO, M1 et meilleur modele) ---
    def intra_group(pred_medians):
        groups = defaultdict(list)
        for i in all_idx:
            r = rows[i]
            key = (r["mask"], round(r["targets"]["MFA"], 3) if r["targets"]["MFA"] is not None else None,
                   int(r["n"]))
            groups[key].append(i)
        out = {}
        # deux plus gros groupes
        for key, idxs in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:2]:
            if len(idxs) < 5:
                continue
            pd_ = []
            td_ = []
            for i in idxs:
                pdv = {t: pred_medians[i, TARGETS.index(t)] for t in DIV}
                pair_pred, ddiv_pred = derive_pair_ddiv(pdv, rows[i]["mask_L"], rows[i]["mask_P"])
                pd_.append(ddiv_pred)
                td_.append(rows[i]["d_div"])
            r_ = pearson_r(pd_, td_)
            out[str(key)] = {"n": len(idxs),
                             "r_pred_vrai": r_,
                             "resid_sd": float(np.std(np.array(td_) - np.array(pd_))) if len(td_) > 1 else None,
                             "d_div_etendue": [float(np.min(td_)), float(np.max(td_))]}
        # correlation intra-groupe poolee (variables centrees par groupe, taille >= 10)
        xs, ys = [], []
        for key, idxs in groups.items():
            if len(idxs) < 10:
                continue
            pd_, td_ = [], []
            for i in idxs:
                pdv = {t: pred_medians[i, TARGETS.index(t)] for t in DIV}
                pair_pred, ddiv_pred = derive_pair_ddiv(pdv, rows[i]["mask_L"], rows[i]["mask_P"])
                pd_.append(ddiv_pred)
                td_.append(rows[i]["d_div"])
            pd_, td_ = np.array(pd_), np.array(td_)
            xs.extend(list(pd_ - pd_.mean()))
            ys.extend(list(td_ - td_.mean()))
        out["poole_groupes_ge10"] = {"r_intra_groupe": pearson_r(xs, ys),
                                      "n": len(xs)}
        return out

    for label in ["M1", "M2", "M3", "M4"]:
        ig = intra_group(loco_preds[label])
        results.setdefault("INTRA_GROUPE_LOCO", {})[label] = ig
        log(f"--- Intra-groupe LOCO {label} ---")
        for k, v in ig.items():
            log(f"  {k} : {v}")

    # --- variante masque ignore (k=6 force), LOCO M1 ---
    def evaluate_no_mask(pred_medians):
        ok_pair = ok_val = 0
        n = 0
        for i in all_idx:
            r = rows[i]
            pdv = {t: pred_medians[i, TARGETS.index(t)] for t in DIV}
            pair_pred, ddiv_pred = derive_pair_ddiv(pdv, True, True)
            n += 1
            if set(pair_pred) == r["pair_set"]:
                ok_pair += 1
            if abs(ddiv_pred - r["d_div"]) <= 0.10:
                ok_val += 1
        return {"n": n, "paire": ok_pair / n, "valeur": ok_val / n}

    nm = evaluate_no_mask(loco_preds["M1"])
    results["VARIANTE_MASQUE_IGNORE_LOCO_M1"] = nm
    log(f"Variante masque ignore (k=6 force), LOCO M1 : paire {nm['paire']:.3f} | "
        f"valeur {nm['valeur']:.3f} (n={nm['n']})")

    # --- paires predites identiques reel vs nul (LOCO M1) ---
    same_pair = tot_rn = 0
    for real, nul in pairs_rn:
        runs_r = [i for i in all_idx if rows[i]["csv_path"] == real]
        runs_n = [i for i in all_idx if rows[i]["csv_path"] == nul]
        for i in runs_r:
            for j in runs_n:
                if rows[i]["version"] != rows[j]["version"]:
                    continue
                tot_rn += 1
                pd_i = {t: loco_preds["M1"][i, TARGETS.index(t)] for t in DIV}
                pd_j = {t: loco_preds["M1"][j, TARGETS.index(t)] for t in DIV}
                pi, _ = derive_pair_ddiv(pd_i, rows[i]["mask_L"], rows[i]["mask_P"])
                pj, _ = derive_pair_ddiv(pd_j, rows[j]["mask_L"], rows[j]["mask_P"])
                if set(pi) == set(pj):
                    same_pair += 1
    results["PAIRE_PREDITE_IDENTIQUE_REEL_NUL_LOCO_M1"] = [same_pair, tot_rn]
    log(f"Paire predite identique reel vs nul (LOCO M1, meme version) : "
        f"{same_pair}/{tot_rn}")

    # --- dedup 153 runs (§8.39.6), LOCO M1 ---
    seen = set()
    dedup_idx = []
    for i in all_idx:
        r = rows[i]
        if r["dir"].endswith("_rep2"):
            continue
        key = ";".join(f"{k}={v:.4f}" for k, v in sorted(r["div"].items()))
        if key in seen:
            continue
        seen.add(key)
        dedup_idx.append(i)
    ev_dedup = evaluate(dedup_idx, loco_preds["M1"])
    results["DEDUP_153_LOCO_M1"] = {"n": len(dedup_idx), **ev_dedup}
    log(f"Dedup 153 runs, LOCO M1 : n={len(dedup_idx)} paire {ev_dedup['paire_non_ordonnee']:.3f} "
        f"| valeur {ev_dedup['valeur_pm010']:.3f}")

    # --- sensibilite lambda M1 (LOCO) ---
    for lam in (1.0, 100.0):
        pred_lam = np.full((len(rows), len(TARGETS)), np.nan)
        for coh in cohorts:
            te = [i for i in all_idx if rows[i]["cohort"] == coh]
            tr = [i for i in all_idx if rows[i]["cohort"] != coh]
            Xtr = np.array([rows[i]["x_red"] for i in tr])
            Xte = np.array([rows[i]["x_red"] for i in te])
            Xtr_s, Xte_s, _, _ = standardize(Xtr, Xte)
            Ytr = np.array([[rows[i]["targets"][t] if rows[i]["targets"][t] is not None else np.nan
                             for t in TARGETS] for i in tr])
            for j in range(len(TARGETS)):
                ok = np.isfinite(Ytr[:, j])
                model = fit_ridge(Xtr_s[ok], Ytr[ok, j:j + 1], lam=lam)
                for k, i in enumerate(te):
                    pred_lam[i, j] = pred_ridge(model, Xte_s[k:k + 1])[0, 0]
        ev = evaluate(all_idx, pred_lam)
        results.setdefault("SENSIBILITE_LAMBDA_LOCO", {})[f"lam_{lam:g}"] = ev
        log(f"Sensibilite lambda={lam:g} LOCO M1 : paire {ev['paire_non_ordonnee']:.3f} | "
            f"valeur {ev['valeur_pm010']:.3f} | MAE d_div {ev['mae_d_div']:.3f}")

    # --- verdict (critere §5.4) ---
    def passe(ev):
        return (ev["paire_non_ordonnee"] is not None and ev["paire_non_ordonnee"] >= 0.90
                and ev["valeur_pm010"] is not None and ev["valeur_pm010"] >= 0.90)

    verdicts = {}
    for label in ["M1", "M2", "M3", "M4"]:
        ok_loco = passe(ev_loco[label])
        ok_split = passe(results["SPLIT_MATRICES_70_30"][label])
        verdicts[label] = {"LOCO": ok_loco, "SPLIT": ok_split, "les_deux": ok_loco and ok_split}
        log(f"Verdict {label} : LOCO {'OK' if ok_loco else 'NON'} "
            f"(paire {ev_loco[label]['paire_non_ordonnee']:.3f}, "
            f"valeur {ev_loco[label]['valeur_pm010']:.3f}) ; SPLIT "
            f"{'OK' if ok_split else 'NON'} "
            f"(paire {results['SPLIT_MATRICES_70_30'][label]['paire_non_ordonnee']:.3f}, "
            f"valeur {results['SPLIT_MATRICES_70_30'][label]['valeur_pm010']:.3f})")
    elucide = any(v["les_deux"] for v in verdicts.values())
    results["verdicts_modeles"] = verdicts
    results["ELUCIDE"] = elucide
    log(f"\nVERDICT §5.4 : {'ELUCIDE' if elucide else 'NON ELUCIDE'}")

    json.dump(results, open(os.path.join(BASE, "v62_delta_magnitudes.json"), "w"),
              indent=1, default=str)
    with open(os.path.join(BASE, "v62_delta_magnitudes.log"), "w") as fh:
        fh.write("\n".join(LOG) + "\n")
    log("Ecrit : v62_delta_magnitudes.json, v62_delta_magnitudes.log, "
        "v62_delta_magnitudes_flux_features.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
