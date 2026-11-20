#!/usr/bin/env python3
"""§8.62 — Loi d'échelle en n pour Delta. Protocole gelé :
PROTOCOL_delta_scaling_862.md (SHA 8e67f8c7…).
Lecture seule pour A ; construction déterministe des sous-échantillons B ;
analyse A puis B. numpy/scipy/pandas seulement. Aucun code pipeline modifié.
Usages :
  python3 v62_delta_scaling_862.py build     # construit les 31 CSV B (+ SHA)
  python3 v62_delta_scaling_862.py phase-a   # analyse des 222 runs détenus
  python3 v62_delta_scaling_862.py phase-b   # analyse des runs B (après le lot)
"""
import glob
import hashlib
import json
import math
import os
import sys

import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
V62 = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
V62_SHA = "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"
DIV = ["LevinaBickel", "PCAIntrinsic", "LocalPCA", "GraphDimension",
       "PersistentHomology", "MFA"]
SAT = ["Higuchi", "Katz", "Petrosian", "Sevcik", "BoxCounting", "Hurst2mH", "DFA"]
TARGETS = DIV + SAT + ["d_div", "d_sat", "Delta"]
SIZES = [45, 70, 100, 145, 178, 285, 515, 1000]
STRIDE_SIZES = [100, 285, 515]

SOURCES = [
    ("hp35", "/home/hatch/workspace/runs/biophysique-hp35/test_biophysique_input.csv"),
    ("hp35nul", "/home/hatch/workspace/runs/biophysique-hp35/test_biophysique_input_nul.csv"),
    ("luad", os.path.join(BASE, "pdac_luad_fluxes.csv")),
    ("tcga", os.path.join(BASE, "pdac_tcga_fluxes_v4.csv")),
]
LOG = os.path.join(BASE, "v62_delta_scaling_862.log")


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    with open(LOG, "a") as f:
        f.write(s + "\n")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def g(d, path, default=None):
    cur = d
    for k in path.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def fnum(x):
    try:
        x = float(x)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def parse_sorted(s):
    out = {}
    if not isinstance(s, str):
        return out
    for part in s.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k] = float(v)
    return out


# ------------------------------------------------------------------ build B
def build():
    assert sha(V62) == V62_SHA, "SHA v6.2 non conforme"
    manifest = []
    for name, src in SOURCES:
        s = sha(src)
        df = pd.read_csv(src)
        n = len(df)
        assert list(df.columns)[0] == "step", f"{src}: 1re colonne {df.columns[0]}"
        assert (df["step"].values == np.arange(n)).all(), f"{src}: step non 0..n-1"
        log(f"SOURCE {name}: {src} n={n} p={len(df.columns) - 1} sha={s[:12]}")
        for k in SIZES:
            if k > n or k < 45:
                continue
            sub = df.head(k).copy()
            sub["step"] = np.arange(k)
            out = os.path.join(BASE, f"pdac_862_{name}_n{k}.csv")
            sub.to_csv(out, index=False)
            manifest.append({"file": os.path.basename(out), "source": name,
                             "src_sha": s, "scheme": "prefix", "k": k,
                             "sha": sha(out)})
            log(f"  prefix k={k} -> {os.path.basename(out)} sha={sha(out)[:12]}")
        if name == "hp35":
            for k in STRIDE_SIZES:
                idx = np.unique(np.linspace(0, n - 1, k).round().astype(int))
                assert len(idx) == k, f"stride {k}: {len(idx)} lignes"
                m = round(float(np.median(np.diff(idx))))
                sub = df.iloc[idx].copy()
                sub["step"] = np.arange(k)
                out = os.path.join(BASE, f"pdac_862_hp35_stride_n{k}.csv")
                sub.to_csv(out, index=False)
                manifest.append({"file": os.path.basename(out), "source": name,
                                 "src_sha": s, "scheme": "stride", "k": k,
                                 "sha": sha(out)})
                log(f"  stride k={k} (m={m}) -> {os.path.basename(out)} sha={sha(out)[:12]}")
    with open(os.path.join(BASE, "v62_delta_scaling_862_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    log(f"BUILD OK: {len(manifest)} CSV (attendu 31)")
    assert len(manifest) == 31, f"manifest {len(manifest)} != 31"
    return manifest


# ------------------------------------------------------------------ OLS forms
def design(n, form):
    n = np.asarray(n, dtype=float)
    ln = np.log(n)
    if form == "F0":
        return np.ones((len(n), 1))
    if form == "F1":
        return np.column_stack([np.ones(len(n)), ln])
    if form == "F2":
        return np.column_stack([np.ones(len(n)), ln, ln ** 2])
    if form == "F3":
        return np.column_stack([np.ones(len(n)), n])
    if form == "F4":
        return np.column_stack([np.ones(len(n)), 1.0 / n])
    if form == "F5":
        return np.column_stack([np.ones(len(n)), 1.0 / np.sqrt(n)])
    if form == "F6":
        return np.column_stack([np.ones(len(n)), np.sqrt(n)])
    raise ValueError(form)


def ols_fit(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta


def ols_eval(X, y, beta):
    pred = X @ beta
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    mae = float(np.mean(np.abs(y - pred)))
    return pred, r2, mae


def fit_all(df, targets):
    """R²/MAE en échantillon pour F0..F6, par cible. df: colonnes n + cibles."""
    out = {}
    for t in targets:
        sub = df.dropna(subset=[t])
        y = sub[t].values.astype(float)
        nv = sub["n"].values.astype(float)
        row = {"n_obs": int(len(sub))}
        for form in ["F0", "F1", "F2", "F3", "F4", "F5", "F6"]:
            X = design(nv, form)
            beta = ols_fit(X, y)
            _, r2, mae = ols_eval(X, y, beta)
            row[f"{form}_R2"] = round(r2, 4)
            row[f"{form}_MAE"] = round(mae, 4)
            row[f"{form}_beta"] = [round(float(b), 6) for b in beta]
        row["r_logn"] = round(float(np.corrcoef(np.log(nv), y)[0, 1]), 4)
        out[t] = row
    return out


def cohort_of(csv_path):
    p = (csv_path or "")
    for pat, c in [("biophysique-hp35", "hp35"), ("geo62452", "geo62452"),
                   ("geo71729", "geo71729"), ("icgc", "icgc"),
                   ("cptac", "cptac"), ("depmap", "depmap"),
                   ("coad", "coad"), ("luad", "luad"), ("tcga", "tcga")]:
        if pat in p:
            return c
    return "?"


# ------------------------------------------------------------------ load A
def load_a():
    lv = pd.read_csv(os.path.join(BASE, "v62_delta_levels.csv"))
    rows = []
    for _, r in lv.iterrows():
        d = dict(r)
        dm = parse_sorted(r["div_sorted"])
        sm = parse_sorted(r["sat_sorted"])
        for k, v in dm.items():
            d[k] = v
        for k, v in sm.items():
            d[k] = v
        d["Delta"] = d["delta"]
        # métadonnées matrice (lecture JSON, 222 dossiers seulement)
        p = os.path.join(BASE, d["dir"], "master_results.json")
        j = json.load(open(p))
        d["csv_path"] = g(j, "metadata.csv_path")
        d["cohort"] = cohort_of(d["csv_path"])
        d["n_json"] = fnum(g(j, "reading_synthesis.n_samples"))
        rows.append(d)
    df = pd.DataFrame(rows)
    # vérifications d'identité
    mis_div = mis_sat = 0
    for _, r in df.iterrows():
        dm = sorted([(r[k], k) for k in DIV if pd.notna(r.get(k))])
        sm = sorted([(r[k], k) for k in SAT if pd.notna(r.get(k))])
        if len(dm) >= 2:
            k = len(dm)
            calc = (dm[k // 2 - 1][0] + dm[k // 2][0]) / 2 if k % 2 == 0 else dm[k // 2][0]
            if abs(calc - r["d_div"]) > 1e-3:
                mis_div += 1
        if len(sm) >= 4 and abs(sm[3][0] - r["d_sat"]) > 1e-3:
            mis_sat += 1
    assert mis_div == 0 and mis_sat == 0, f"identités: {mis_div}/{mis_sat}"
    assert (df["n"] == df["n_json"]).all(), "écart n CSV vs n JSON"
    log(f"A: {len(df)} runs, identités d_div/d_sat 0 écart >1e-3, 0 écart n")
    return df


def loco_f1(df, targets):
    """LOCO F1 (R² poolé, SStot vs moyenne globale du test)."""
    out = {}
    cohorts = sorted(df["cohort"].unique())
    for t in targets:
        res, tot, ymean = [], [], []
        per_fold = {}
        for c in cohorts:
            tr = df[(df["cohort"] != c)].dropna(subset=[t])
            te = df[(df["cohort"] == c)].dropna(subset=[t])
            if len(te) == 0 or len(tr) < 10:
                continue
            beta = ols_fit(design(tr["n"].values, "F1"), tr[t].values.astype(float))
            pred = design(te["n"].values, "F1") @ beta
            res.extend((te[t].values.astype(float) - pred).tolist())
            tot.extend(te[t].values.astype(float).tolist())
            per_fold[c] = {"n": int(len(te)),
                           "mae": round(float(np.mean(np.abs(te[t].values - pred))), 4)}
        res = np.array(res)
        tot = np.array(tot)
        r2 = 1.0 - float(np.sum(res ** 2)) / float(np.sum((tot - np.mean(tot)) ** 2))
        out[t] = {"R2_pooled": round(r2, 4),
                  "MAE_pooled": round(float(np.mean(np.abs(res))), 4),
                  "per_fold": per_fold}
    return out


def phase_a():
    assert sha(V62) == V62_SHA, "SHA v6.2 non conforme"
    df = load_a()
    res = {"ensemble": "A", "n_runs": int(len(df)),
           "n_distinct": sorted(df["n"].unique().astype(int).tolist()),
           "n_by_cohort": {c: sorted(g["n"].unique().astype(int).tolist())
                           for c, g in df.groupby("cohort")}}
    res["fit_all"] = fit_all(df, TARGETS)
    res["loco_F1"] = loco_f1(df, TARGETS)
    # moyennes par matrice (156 distinctes) : F1 Delta/d_div/d_sat
    mx = df.groupby("csv_path").agg(n=("n", "first"), cohort=("cohort", "first"),
                                    d_div=("d_div", "mean"), d_sat=("d_sat", "mean"),
                                    Delta=("Delta", "mean")).reset_index()
    res["n_matrices"] = int(len(mx))
    res["fit_matrix_mean"] = fit_all(mx, ["d_div", "d_sat", "Delta"])
    # à n fixé : étalement intra-cohorte
    fixed = {}
    for c, g in df.groupby("cohort"):
        if g["n"].nunique() == 1:
            fixed[c] = {"n": int(g["n"].iloc[0]), "n_runs": int(len(g)),
                        "Delta_std": round(float(g["Delta"].std(ddof=1)), 4),
                        "Delta_range": [round(float(g["Delta"].min()), 4),
                                        round(float(g["Delta"].max()), 4)],
                        "d_div_std": round(float(g["d_div"].std(ddof=1)), 4),
                        "d_sat_std": round(float(g["d_sat"].std(ddof=1)), 4)}
    res["fixed_n_spread"] = fixed
    # réel / nul
    beta_f1 = ols_fit(design(df["n"].values, "F1"), df["Delta"].values.astype(float))
    df["resid_Delta_F1"] = df["Delta"].values - design(df["n"].values, "F1") @ beta_f1
    lv = df.set_index("dir")
    pairs = []
    for d in df["dir"]:
        if d.endswith("_nul"):
            base = d[:-4]
            if base in lv.index:
                pairs.append((base, d))
    res["n_real_null_pairs"] = len(pairs)
    dd, rd = [], []
    for base, nul in pairs:
        dd.append(lv.loc[base, "Delta"] - lv.loc[nul, "Delta"])
        rd.append(lv.loc[base, "resid_Delta_F1"] - lv.loc[nul, "resid_Delta_F1"])
    dd, rd = np.array(dd), np.array(rd)
    res["real_null"] = {
        "Delta_diff_mean": round(float(np.mean(dd)), 4),
        "Delta_diff_std": round(float(np.std(dd, ddof=1)), 4),
        "Delta_diff_abs_le_010": f"{int(np.sum(np.abs(dd) <= 0.10))}/{len(dd)}",
        "resid_diff_mean": round(float(np.mean(rd)), 4),
        "resid_diff_std": round(float(np.std(rd, ddof=1)), 4),
        "resid_diff_abs_le_010": f"{int(np.sum(np.abs(rd) <= 0.10))}/{len(rd)}"}
    for lab, sub in [("real", df[~df["dir"].str.endswith("_nul")]),
                     ("null", df[df["dir"].str.endswith("_nul")])]:
        b = ols_fit(design(sub["n"].values, "F1"), sub["Delta"].values.astype(float))
        _, r2, mae = ols_eval(design(sub["n"].values, "F1"),
                              sub["Delta"].values.astype(float), b)
        res[f"F1_Delta_{lab}_only"] = {"n": int(len(sub)), "R2": round(r2, 4),
                                      "MAE": round(mae, 4),
                                      "beta": [round(float(x), 4) for x in b]}
    # sensibilités F1 Delta
    sens = {}
    sub = df[df["dfa"].abs() <= 10]
    b = ols_fit(design(sub["n"].values, "F1"), sub["Delta"].values.astype(float))
    _, r2, mae = ols_eval(design(sub["n"].values, "F1"), sub["Delta"].values.astype(float), b)
    sens["no_DFA_extreme"] = {"n": int(len(sub)), "R2": round(r2, 4), "MAE": round(mae, 4)}
    sub = df[df["cohort"] != "hp35"]
    b = ols_fit(design(sub["n"].values, "F1"), sub["Delta"].values.astype(float))
    _, r2, mae = ols_eval(design(sub["n"].values, "F1"), sub["Delta"].values.astype(float), b)
    sens["no_hp35"] = {"n": int(len(sub)), "R2": round(r2, 4), "MAE": round(mae, 4)}
    ded = df[~df["dir"].str.contains("rep2")].drop_duplicates(subset=["div_sorted"])
    b = ols_fit(design(ded["n"].values, "F1"), ded["Delta"].values.astype(float))
    _, r2, mae = ols_eval(design(ded["n"].values, "F1"), ded["Delta"].values.astype(float), b)
    sens["dedup_839"] = {"n": int(len(ded)), "R2": round(r2, 4), "MAE": round(mae, 4)}
    res["sens_F1_Delta"] = sens
    # sauvegarde
    feat = df[["dir", "version", "n", "cohort", "csv_path", "control", "d_div",
               "d_sat", "Delta", "resid_Delta_F1", "pair", "mask", "mfa",
               "dfa"] + DIV + SAT].copy()
    feat["ensemble"] = "A"
    feat.to_csv(os.path.join(BASE, "v62_delta_scaling_862_features.csv"), index=False)
    with open(os.path.join(BASE, "v62_delta_scaling_862_phaseA.json"), "w") as f:
        json.dump(res, f, indent=1)
    for t in ["Delta", "d_div", "d_sat"]:
        r = res["fit_all"][t]
        log(f"A {t}: F1 R2={r['F1_R2']} MAE={r['F1_MAE']} beta={r['F1_beta']} | "
            f"F2 R2={r['F2_R2']} | LOCO F1 R2={res['loco_F1'][t]['R2_pooled']}")
    log(f"A paires réel/nul: {res['n_real_null_pairs']}, "
        f"|ΔDelta|<=0.10: {res['real_null']['Delta_diff_abs_le_010']}, "
        f"|Δrésidu|<=0.10: {res['real_null']['resid_diff_abs_le_010']}")
    log("PHASE-A OK")
    return res


# ------------------------------------------------------------------ load B
def load_b():
    rows = []
    for p in sorted(glob.glob(os.path.join(BASE, "results_fast_v62_862_*",
                                           "master_results.json"))):
        d = os.path.basename(os.path.dirname(p))
        j = json.load(open(p))
        ht = g(j, "holographic_tension_state", {}) or {}
        per = g(ht, "per_estimator", {}) or {}
        dv = g(ht, "D_vector", {}) or {}

        def med(nm):
            return fnum((per.get(nm) or {}).get("raw_median"))
        row = {"dir": d, "n": fnum(g(j, "reading_synthesis.n_samples")),
               "d_div": fnum(dv.get("d_div")), "d_sat": fnum(dv.get("d_sat")),
               "Delta": fnum(g(j, "reading_synthesis.Delta_tension")),
               "csv_path": g(j, "metadata.csv_path"),
               "control": g(j, "metadata.control")}
        for nm in DIV + SAT:
            row[nm] = med(nm)
        # schéma / source / k depuis le nom du CSV
        base = os.path.basename(row["csv_path"] or "")
        row["src_csv"] = base
        rows.append(row)
    df = pd.DataFrame(rows)
    # identités
    mis = 0
    for _, r in df.iterrows():
        dm = sorted([(r[k], k) for k in DIV if pd.notna(r.get(k))])
        sm = sorted([(r[k], k) for k in SAT if pd.notna(r.get(k))])
        if len(dm) >= 2:
            k = len(dm)
            calc = (dm[k // 2 - 1][0] + dm[k // 2][0]) / 2 if k % 2 == 0 else dm[k // 2][0]
            if abs(calc - r["d_div"]) > 1e-3:
                mis += 1
        if len(sm) >= 4 and abs(sm[3][0] - r["d_sat"]) > 1e-3:
            mis += 1
    valid = df.dropna(subset=["d_div", "d_sat", "Delta"])
    log(f"B: {len(df)} dossiers lus, {len(valid)} valides (d_div/d_sat/Delta finis), "
        f"identités en écart: {mis}")
    return df


def phase_b():
    assert sha(V62) == V62_SHA, "SHA v6.2 non conforme"
    df = load_b()
    # rattacher schéma/source/k depuis le manifeste
    man = {m["file"]: m for m in
           json.load(open(os.path.join(BASE, "v62_delta_scaling_862_manifest.json")))}
    df["scheme"] = df["src_csv"].map(lambda s: man.get(s, {}).get("scheme"))
    df["source"] = df["src_csv"].map(lambda s: man.get(s, {}).get("source"))
    df["k"] = df["src_csv"].map(lambda s: man.get(s, {}).get("k"))
    df["curve"] = df["source"] + "_" + df["scheme"].fillna("prefix")
    valid = df.dropna(subset=["d_div", "d_sat", "Delta"]).copy()
    res = {"ensemble": "B", "n_dirs": int(len(df)), "n_valid": int(len(valid)),
           "n_expected": 31}
    res["fit_all_B"] = fit_all(valid, TARGETS)
    # F1 intra-courbe (préfixe seulement)
    intra = {}
    for curve, g in valid[valid["scheme"] == "prefix"].groupby("curve"):
        intra[curve] = {}
        for t in ["Delta", "d_div", "d_sat"]:
            sub = g.dropna(subset=[t])
            if len(sub) >= 3 and sub["n"].nunique() >= 3:
                b = ols_fit(design(sub["n"].values, "F1"), sub[t].values.astype(float))
                _, r2, mae = ols_eval(design(sub["n"].values, "F1"),
                                      sub[t].values.astype(float), b)
                intra[curve][t] = {"n": int(len(sub)), "R2": round(r2, 4),
                                   "MAE": round(mae, 4),
                                   "beta": [round(float(x), 4) for x in b]}
    res["F1_intra_curve"] = intra
    # transfert A -> B (F1, F2 ajustées sur A)
    A = pd.read_csv(os.path.join(BASE, "v62_delta_scaling_862_features.csv"))
    A = A[A["ensemble"] == "A"]
    trans = {}
    for form in ["F1", "F2"]:
        trans[form] = {}
        for t in TARGETS:
            sub = A.dropna(subset=[t])
            beta = ols_fit(design(sub["n"].values, form), sub[t].values.astype(float))
            vb = valid.dropna(subset=[t])
            pred = design(vb["n"].values, form) @ beta
            err = np.abs(vb[t].values.astype(float) - pred)
            trans[form][t] = {"n": int(len(vb)),
                              "frac_le_010": f"{int(np.sum(err <= 0.10))}/{len(vb)}",
                              "MAE": round(float(np.mean(err)), 4)}
    res["transfer_A_to_B"] = trans
    # réel vs nul HP35 préfixe
    hp = valid[(valid["source"] == "hp35") & (valid["scheme"] == "prefix")].set_index("k")
    hpn = valid[(valid["source"] == "hp35nul") & (valid["scheme"] == "prefix")].set_index("k")
    comp = {}
    for t in ["Delta", "d_div", "d_sat"]:
        diffs = []
        for k in sorted(set(hp.index) & set(hpn.index)):
            diffs.append((int(k), round(float(hp.loc[k, t] - hpn.loc[k, t]), 4)))
        comp[t] = {"diffs_by_k": diffs,
                   "frac_le_010": f"{sum(1 for _, d in diffs if abs(d) <= 0.10)}/{len(diffs)}"}
    res["hp35_real_vs_null"] = comp
    # stride vs préfixe HP35
    st = valid[(valid["source"] == "hp35") & (valid["scheme"] == "stride")].set_index("k")
    sc = {}
    for t in ["Delta", "d_div", "d_sat"]:
        diffs = []
        for k in sorted(set(st.index) & set(hp.index)):
            diffs.append((int(k), round(float(st.loc[k, t] - hp.loc[k, t]), 4)))
        sc[t] = {"diffs_by_k": diffs,
                 "frac_le_010": f"{sum(1 for _, d in diffs if abs(d) <= 0.10)}/{len(diffs)}"}
    res["hp35_stride_vs_prefix"] = sc
    # sauvegarde : ajouter B aux features
    bfeat = valid[["dir", "n", "control", "csv_path", "d_div", "d_sat", "Delta",
                   "source", "scheme", "k"] + DIV + SAT].copy()
    bfeat["ensemble"] = "B"
    feat = pd.read_csv(os.path.join(BASE, "v62_delta_scaling_862_features.csv"))
    feat = pd.concat([feat, bfeat], ignore_index=True, sort=False)
    feat.to_csv(os.path.join(BASE, "v62_delta_scaling_862_features.csv"), index=False)
    with open(os.path.join(BASE, "v62_delta_scaling_862_phaseB.json"), "w") as f:
        json.dump(res, f, indent=1)
    for t in ["Delta", "d_div", "d_sat"]:
        r = res["fit_all_B"][t]
        log(f"B {t}: F1 R2={r['F1_R2']} MAE={r['F1_MAE']} | F2 R2={r['F2_R2']} | "
            f"transfert F1 <=0.10: {trans['F1'][t]['frac_le_010']}")
    log(f"B hp35 réel/nul Delta <=0.10: {comp['Delta']['frac_le_010']}; "
        f"stride/prefixe Delta <=0.10: {sc['Delta']['frac_le_010']}")
    log("PHASE-B OK")
    return res


if __name__ == "__main__":
    open(LOG, "a").write(f"=== {sys.argv[1] if len(sys.argv) > 1 else '?'} ===\n")
    cmd = sys.argv[1]
    if cmd == "build":
        build()
    elif cmd == "phase-a":
        phase_a()
    elif cmd == "phase-b":
        phase_b()
    else:
        raise SystemExit(f"commande inconnue: {cmd}")
