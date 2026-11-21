#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Survie des gènes de privilège (§8.83) — TCGA, ICGC, GSE71729.
Protocole gelé : PROTOCOL_survie_privilege_883.md (21 nov. 2026), avant
toute analyse.
Méthode : EXACTEMENT celle des §8.12/§8.15/§8.16 — KM / log-rank
Mantel-Haenszel / Cox Breslow Newton-Raphson en numpy, événements
booléens. Fonctions KM/log-rank/Cox reprises littéralement de
survival_tcga_verify.py (correction du 16 nov. 2026 : univarié = UN gène
à la fois ; log-rank sur événements booléens). La première version du
Cox (BFGS + décalage non compensé) gonflait les coefficients — elle
n'est PAS utilisée ici.
Items testés (liste fermée, §0) : FASLG, TGFB1, TGFB2, IDO1, HLA-G,
CD47, CD274 + score combiné (moyenne des z-scores des 7, par cohorte).
Aucun gène ajouté ou retiré après les résultats.
CALIBRATION (§6, porte d'entrée) : le script reproduit D'ABORD les
chiffres publiés de MUC16 (Cox HR ±0,02 ; log-rank p ±0,01 ; effectifs
exacts ; OS médianes 20,0 / 16,6 / 17,0 mois). Si un seul contrôle
échoue, ARRÊT avant toute lecture des résultats privilège.
Échelles d'expression (§1) : TCGA = résidus corrigés de la pureté
(même construction que survival_tcga_verify.py) ; ICGC = log2(cpm)
brut Xena ; GSE71729 = valeurs brutes de la matrice (mêmes que
survival_geo71729.py). Jointures vérifiées contre les tables
sauvegardées (écart > 1e-9 = ARRÊT).
"""
import gzip
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd
from scipy.stats import chi2 as chi2_dist
from scipy.stats import norm, spearmanr

BASE = "/home/hatch/workspace/runs/pdac-v6"
PRIV = ["FASLG", "TGFB1", "TGFB2", "IDO1", "HLA-G", "CD47", "CD274"]
V4 = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
      "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]

ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]
ISLET = ["INS", "GCG", "PPY", "SST"]

TCGA_TARBALL = f"{BASE}/data/tcga_paad_rsem.tar.gz"
TCGA_TARBALL_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
TCGA_CLIN = f"{BASE}/data_clinical_patient.txt"
GSE71729_MAT = f"{BASE}/data/GSE71729_series_matrix.txt.gz"
GSE71729_SHA = "b228789314ec4d866ec51b65724664abaa24b822577c55d3727820c867536a54"
ICGC_EXP = f"{BASE}/data/icgc_pacaau_exp.txt.gz"
ICGC_EXP_SHA = "c2cb57af3ba4c3d7fdac292e66c81067d36e16aae9efdd8005147e20820f49fa"
ICGC_PROBE = f"{BASE}/data/icgc_pacaau_probemap.gz"
ICGC_PROBE_SHA = "b09a746f6084215beea3632b72e87834ea577d18fcb52add3641de5d0d975537"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --- KM / log-rank / Cox : reprise littérale de survival_tcga_verify.py ---
def km_median(t, e):
    times = np.sort(np.unique(t[e]))
    surv = 1.0
    for tt in times:
        at_risk = np.sum(t >= tt)
        d = np.sum((t == tt) & e)
        if at_risk > 0:
            surv *= (1.0 - d / at_risk)
            if surv <= 0.5:
                return float(tt)
    return float("nan")


def logrank(t, e, grp):
    """grp booléen : groupe testé vs reste. Retourne p (chi2, 1 ddl)."""
    times = np.sort(np.unique(t[e]))
    O = E = V = 0.0
    for tt in times:
        r = t >= tt
        r1 = np.sum(r & grp)
        r0 = np.sum(r & ~grp)
        n = r1 + r0
        d = np.sum((t == tt) & e)
        d1 = np.sum((t == tt) & e & grp)
        if n < 2 or d == 0:
            continue
        e1 = d * r1 / n
        O += d1
        E += e1
        V += (r1 * r0 * d * (n - d)) / (n * n * (n - 1))
    if V <= 0:
        return float("nan")
    z2 = (O - E) ** 2 / V
    return float(1.0 - chi2_dist.cdf(z2, 1))


def cox_fit(Z, t, e):
    """Z : (n, p) standardisé. Retourne HR, coef, se, p (Wald).
    Newton-Raphson sur la vraisemblance partielle de Breslow (version
    corrigée du 16 nov. 2026, vérifiée contre statsmodels PHReg)."""
    Z = np.asarray(Z, dtype=float)
    t = np.asarray(t, dtype=float)
    e = np.asarray(e, dtype=bool)
    order = np.argsort(-t)
    Z, t, e = Z[order], t[order], e[order]
    p = Z.shape[1]
    beta = np.zeros(p)
    hess = None
    for _ in range(50):
        eta = Z @ beta
        w = np.exp(eta - eta.max())
        S0 = np.cumsum(w)
        S1 = np.cumsum(Z * w[:, None], axis=0)
        S2 = np.cumsum((Z[:, :, None] * Z[:, None, :]) * w[:, None, None],
                       axis=0)
        grad = np.zeros(p)
        hess = np.zeros((p, p))
        for i in range(len(t)):
            if not e[i]:
                continue
            grad += Z[i] - S1[i] / S0[i]
            hess -= S2[i] / S0[i] - np.outer(S1[i], S1[i]) / (S0[i] ** 2)
        try:
            step = np.linalg.solve(hess, grad)
        except np.linalg.LinAlgError:
            break
        beta = beta - step
        if np.max(np.abs(step)) < 1e-8:
            break
    se = np.sqrt(np.diag(np.linalg.inv(-hess)))
    z = beta / se
    pval = 2 * (1 - norm.cdf(np.abs(z)))
    return np.exp(beta), beta, se, np.atleast_1d(pval)


def zscore(v):
    v = np.asarray(v, dtype=float)
    return (v - v.mean()) / v.std(ddof=0)


def quartile_mask(values):
    q = np.quantile(values, 0.75)
    return values >= q


def topn_mask(values, k):
    """Top k par rang (valeurs les plus hautes), comme aux §8.15/§8.16.
    En cas d'égalité à la coupure, l'ordre du tri départage (même
    comportement que sort_values().iloc[-k:] des scripts publiés)."""
    values = np.asarray(values, dtype=float)
    idx = np.argsort(values)[::-1][:k]
    m = np.zeros(len(values), dtype=bool)
    m[idx] = True
    return m


# --- Chargement des 3 cohortes (expression + survie) -----------------------
def load_tcga():
    assert md5(TCGA_TARBALL) == TCGA_TARBALL_MD5, "MD5 tarball TCGA"
    with tarfile.open(TCGA_TARBALL, "r:gz") as tf:
        member = [m for m in tf.getmembers()
                  if m.name.endswith(".data.txt")][0]
        f = tf.extractfile(member)
        df = pd.read_csv(f, sep="\t", index_col=0, low_memory=False)
    df.index = df.index.to_series().str.split("|").str[0]
    df = df[~df.index.duplicated(keep="first")]
    cols = df.columns.to_series()
    tumor_cols = cols[cols.str[13:15] == "01"]
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    mat = mat[~mat.isna().any(axis=1)]
    logmat = np.log2(mat + 1.0)
    score_ac = logmat.loc[ACINAR].median(axis=0)
    score_is = logmat.loc[ISLET].median(axis=0)
    X = np.column_stack([np.ones(len(logmat.columns)), score_ac.values,
                         score_is.values])
    Y = logmat.values
    beta, *_ = np.linalg.lstsq(X, Y.T, rcond=None)
    resid = Y - (X @ beta).T
    resid_df = pd.DataFrame(resid, index=logmat.index, columns=logmat.columns)
    kras_res = resid_df.loc["KRAS"].sort_values(ascending=True)
    order = list(kras_res.index)
    assert len(order) == 178, len(order)
    # Vérification contre le JSON des groupes du §8.12 (top12 résidu).
    groups = json.load(open(f"{BASE}/tcga_groups_survival.json"))
    assert set(order) == set(groups["all_tumors"])
    top_res = set(kras_res.sort_values(ascending=False).head(12).index)
    assert top_res == set(groups["top12_kras_resid"])
    clin = pd.read_csv(TCGA_CLIN, sep="\t", skiprows=[1, 2], dtype=str)
    clin = clin.rename(columns={"#Patient Identifier": "patient",
                                "Overall Survival Status": "os_status",
                                "Overall Survival (Months)": "os_months"})
    clin["os_months"] = pd.to_numeric(clin["os_months"], errors="coerce")
    clin = clin[clin["os_months"].notna()].set_index("patient")
    event = clin["os_status"].astype(str).str.startswith("1")
    patients = [c[:12] for c in order]
    present = [p for p in patients if p in clin.index]
    assert len(present) == 177, len(present)
    order = [c for c in order if c[:12] in clin.index]
    patients = present
    time = clin.loc[patients, "os_months"].values.astype(float)
    ev = event.loc[patients].values.astype(bool)
    assert len(time) == 177 and ev.sum() == 92
    # Vérification des résidus contre la table de vérification du §8.12 :
    # on recalcule MUC16/CEACAM5/KRAS ici même (calibration §6).
    data = {"patient": patients, "os_months": time, "dead": ev,
            "KRAS": resid_df.loc["KRAS", order].values,
            "MUC16": resid_df.loc["MUC16", order].values,
            "CEACAM5": resid_df.loc["CEACAM5", order].values}
    for g in PRIV:
        data[g] = resid_df.loc[g, order].values
    # Quartile MUC16 défini sur les 178 (méthode publiée §8.12) pour la
    # calibration ; les items privilège utilisent le quartile sur 177 (§3.2).
    q178 = np.quantile(resid_df.loc["MUC16", list(kras_res.index)].values,
                       0.75)
    data["_muc16_q178_mask"] = data["MUC16"] >= q178
    d = pd.DataFrame(data)
    return d, "TCGA"


def load_icgc():
    assert sha256(ICGC_EXP) == ICGC_EXP_SHA, "SHA exp ICGC"
    assert sha256(ICGC_PROBE) == ICGC_PROBE_SHA, "SHA probemap ICGC"
    clin = pd.read_csv(f"{BASE}/icgc_clinical_70.csv")
    clin["time"] = pd.to_numeric(clin["followup_months"], errors="coerce")
    clin["dead_os"] = clin["Status"].astype(str).str.startswith("Deceased")
    clin["dead_dss"] = clin["Status"] == "Deceased - Of Disease"
    assert clin["time"].notna().all() and len(clin) == 70
    assert int(clin["dead_os"].sum()) == 47
    exp = pd.read_csv(ICGC_EXP, sep="\t", index_col=0, compression="gzip")
    pm = pd.read_csv(ICGC_PROBE, sep="\t", compression="gzip")
    mapping = dict(zip(pm["#id"], pm["gene"]))
    exp.index = exp.index.map(lambda g: mapping.get(g, g))
    exp = exp.groupby(level=0).median()
    order = clin.sort_values("kras_rank")["icgc_id"].tolist()
    E = exp.loc[["KRAS", "MUC16", "CEACAM5"] + PRIV, order].T
    clin = clin.set_index("icgc_id").loc[order].reset_index()
    data = {"patient": clin["icgc_id"].values,
            "os_months": clin["time"].values.astype(float),
            "dead": clin["dead_os"].values.astype(bool),
            "dead_dss": clin["dead_dss"].values.astype(bool),
            "KRAS": E["KRAS"].values.astype(float),
            "MUC16": E["MUC16"].values.astype(float),
            "CEACAM5": E["CEACAM5"].values.astype(float)}
    for g in PRIV:
        data[g] = E[g].values.astype(float)
    return pd.DataFrame(data), "ICGC"


def load_gse71729():
    assert sha256(GSE71729_MAT) == GSE71729_SHA, "SHA matrice GSE71729"
    mat = pd.read_csv(GSE71729_MAT, sep="\t", comment="!",
                      index_col=0, low_memory=False)
    mat.index = mat.index.str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    gsm_order = list(mat.columns)
    ch2 = []
    titles = []
    with gzip.open(GSE71729_MAT, "rt", encoding="utf-8",
                   errors="replace") as f:
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_characteristics_ch2"):
                ch2.append([v.strip('"') for v in
                            line.rstrip("\n").split("\t")[1:]])
            if line.startswith("!Sample_title"):
                titles = [t.strip('"') for t in
                          line.rstrip("\n").split("\t")[1:]]
    annot = {}
    for i, gsm in enumerate(gsm_order):
        vals = [row[i] for row in ch2 if i < len(row)]
        rec = {"gsm": gsm, "title": titles[i] if i < len(titles) else ""}
        for v in vals:
            if v.startswith("tissue type:"):
                rec["tissue"] = v.split(":", 1)[1].strip()
            elif v.startswith("survival_months:"):
                rec["os_months"] = float(v.split(":", 1)[1].strip())
            elif v.startswith("death_event_1death_0censor:"):
                rec["dead"] = int(v.split(":", 1)[1].strip())
        annot[gsm] = rec
    kinds = []
    for i, gsm in enumerate(gsm_order):
        vals = [row[i] for row in ch2 if i < len(row)]
        joined = " | ".join(vals)
        if "tissue type: Primary" in joined:
            kinds.append("Primary")
        elif "tissue type: Metastasis" in joined:
            kinds.append("Metastasis")
        elif "tissue type: Normal" in joined:
            kinds.append("Normal")
        elif titles[i].endswith("-CellLine"):
            kinds.append("CellLine")
        else:
            kinds.append("?")
    prim = [g for g, k in zip(gsm_order, kinds) if k == "Primary"]
    assert len(prim) == 145, len(prim)
    sub = mat[prim]
    need = ["KRAS", "MUC16", "CEACAM5"] + PRIV
    cc = sub.loc[need].dropna(axis=1)
    order = cc.loc["KRAS"].sort_values(ascending=True).index
    # Vérification contre la table de survie du §8.15 (KRAS/MUC16/CEACAM5).
    prev = pd.read_csv(f"{BASE}/geo71729_survival_table.csv")
    assert len(prev) == 145
    prev = prev.set_index("gsm").loc[list(order)].reset_index()
    for g in ["KRAS", "MUC16", "CEACAM5"]:
        assert np.allclose(cc.loc[g, order].values, prev[g].values,
                           atol=1e-9), f"jointure GSE71729 {g}"
    rows = []
    for step, gsm in enumerate(order):
        r = annot[gsm]
        row = {"patient": gsm, "KRAS": float(cc.loc["KRAS", gsm]),
               "MUC16": float(cc.loc["MUC16", gsm]),
               "CEACAM5": float(cc.loc["CEACAM5", gsm]),
               "os_months": r.get("os_months", np.nan),
               "dead": r.get("dead", np.nan)}
        for g in PRIV:
            row[g] = float(cc.loc[g, gsm])
        rows.append(row)
    d = pd.DataFrame(rows)
    # Quartile MUC16 publié (§8.15) : top 36 PAR RANG sur les 145
    # primaires (survival_geo71729.py : sort_values().iloc[-36:]), restreint
    # aux patients avec survie. Un seuil au quantile 0,75 inclut un patient
    # lié de plus (n=34, p=0,86) — ce n'est PAS la définition publiée.
    top36_muc16 = set(d.sort_values("MUC16").iloc[-36:]["patient"])
    # Même définition pour chaque item privilège : top 36 par rang sur 145.
    top36 = {g: set(d.sort_values(g).iloc[-36:]["patient"])
             for g in PRIV}
    d_surv = d.dropna(subset=["os_months"]).copy()
    d_surv["dead"] = d_surv["dead"].astype(int).astype(bool)
    assert len(d_surv) == 125 and int(d_surv["dead"].sum()) == 84
    d_surv["_muc16_q145_mask"] = d_surv["patient"].isin(top36_muc16).values
    for g in PRIV:
        d_surv[f"_top36_{g}"] = d_surv["patient"].isin(top36[g]).values
    return d_surv.reset_index(drop=True), "GSE71729"


# --- Analyse d'une cohorte --------------------------------------------------
def analyze(d, cohort):
    time = d["os_months"].values.astype(float)
    ev = d["dead"].values.astype(bool)
    # Score combiné : moyenne des z-scores des 7, sur les patients avec survie.
    Z = np.column_stack([zscore(d[g].values) for g in PRIV])
    d = d.copy()
    d["SCORE_PRIV"] = Z.mean(axis=1)
    items = PRIV + ["SCORE_PRIV"]
    res = {}
    # --- Calibration MUC16 (porte d'entrée §6) ---
    hr, _, _, p = cox_fit(zscore(d["MUC16"].values).reshape(-1, 1), time, ev)
    if cohort == "TCGA":
        mask_cal = d["_muc16_q178_mask"].values.astype(bool)
    elif cohort == "GSE71729":
        mask_cal = d["_muc16_q145_mask"].values.astype(bool)
    else:  # ICGC : top 18 par rang, comme au §8.16.
        mask_cal = topn_mask(d["MUC16"].values, 18)
    p_lr = logrank(time, ev, mask_cal)
    med = km_median(time, ev)
    res["calibration"] = {"cox_MUC16_HR": round(float(hr[0]), 4),
                          "cox_MUC16_p": round(float(p[0]), 4),
                          "logrank_MUC16_p": round(float(p_lr), 4),
                          "n": int(len(time)), "deces": int(ev.sum()),
                          "os_mediane_cohorte": round(float(med), 1)}
    # --- Items privilège ---
    for item in items:
        vals = d[item].values.astype(float)
        hr, _, _, p = cox_fit(zscore(vals).reshape(-1, 1), time, ev)
        # Quartile supérieur : définition du bras publié de la cohorte
        # (protocole §3.2) : TCGA = seuil quantile 0,75 sur 177 ;
        # ICGC = top 18 par rang ; GSE71729 = top 36 par rang sur 145
        # (colonnes _top36_* pré-calculées) ; score combiné GSE71729 =
        # top 36 par rang sur les 125 avec survie (pas de population
        # de 145 pour le score, calculé sur les patients avec survie).
        if cohort == "TCGA":
            mask = quartile_mask(vals)
        elif cohort == "ICGC":
            mask = topn_mask(vals, 18)
        elif item in PRIV:
            mask = d[f"_top36_{item}"].values.astype(bool)
        else:
            mask = topn_mask(vals, 36)
        p_lr = logrank(time, ev, mask)
        med_hi = km_median(time[mask], ev[mask])
        med_lo = km_median(time[~mask], ev[~mask])
        rho, p_rho = spearmanr(vals, d["KRAS"].values.astype(float))
        res[item] = {
            "cox_HR": round(float(hr[0]), 4),
            "cox_p": round(float(p[0]), 4),
            "logrank_p": round(float(p_lr), 4),
            "n_q4": int(mask.sum()), "deces_q4": int(ev[mask].sum()),
            "os_mediane_q4": (None if not np.isfinite(med_hi)
                              else round(float(med_hi), 1)),
            "os_mediane_reste": (None if not np.isfinite(med_lo)
                                 else round(float(med_lo), 1)),
            "spearman_KRAS_rho": round(float(rho), 4),
            "spearman_KRAS_p": round(float(p_rho), 4),
        }
    # DSS (ICGC seulement, sensibilité §3.3 — calculée ici, rapportée si un
    # item passe l'OS ; sinon ignorée dans la section).
    if "dead_dss" in d.columns:
        ev_dss = d["dead_dss"].values.astype(bool)
        for item in items:
            vals = d[item].values.astype(float)
            hr, _, _, p = cox_fit(zscore(vals).reshape(-1, 1), time, ev_dss)
            res[item]["cox_DSS_HR"] = round(float(hr[0]), 4)
            res[item]["cox_DSS_p"] = round(float(p[0]), 4)
    res["_cohorte"] = cohort
    res["_n"] = int(len(time))
    res["_deces"] = int(ev.sum())
    res["_os_mediane"] = round(float(med), 1)
    return d, res


def verdict_cat(cox):
    """cox : liste de (HR, p) pour TCGA, ICGC, GSE71729 (dans cet ordre)."""
    sig_up = [i for i, (h, p) in enumerate(cox) if h > 1 and p < 0.05]
    sig_dn = [i for i, (h, p) in enumerate(cox) if h < 1 and p < 0.05]
    if len(sig_up) >= 2:
        return "PRÉDIT COMME CA125"
    if len(sig_dn) >= 2 and not sig_up:
        return "SENS INVERSE"
    if sig_up and sig_dn:
        return "MIXTE"
    if len(sig_up) == 1:
        return "UNE COHORTE"
    if len(sig_dn) == 1:
        return "UNE COHORTE (SENS INVERSE)"
    return "NE PRÉDIT RIEN"


def main():
    out_lines = []
    all_res = {}
    tables = []
    for loader in (load_tcga, load_icgc, load_gse71729):
        d, cohort = loader()
        d2, res = analyze(d, cohort)
        all_res[cohort] = res
        t = d2[["patient", "os_months", "dead", "KRAS", "MUC16",
                "CEACAM5"] + PRIV + ["SCORE_PRIV"]].copy()
        t.insert(0, "cohorte", cohort)
        tables.append(t)
        out_lines.append(f"=== {cohort} : n={res['_n']} décès={res['_deces']} "
                         f"OS médiane cohorte={res['_os_mediane']} mois ===")
        c = res["calibration"]
        out_lines.append(f"  CALIBRATION MUC16 : Cox HR={c['cox_MUC16_HR']} "
                         f"p={c['cox_MUC16_p']} ; log-rank p="
                         f"{c['logrank_MUC16_p']} ; n={c['n']} "
                         f"décès={c['deces']} ; OS médiane="
                         f"{c['os_mediane_cohorte']}")
    # --- Porte de calibration (§6) : AVANT toute lecture privilège ---
    expected = {"TCGA": {"hr": 1.44, "lr": 0.070, "n": 177, "d": 92,
                         "med": 20.0},
                "ICGC": {"hr": 1.57, "lr": 0.002, "n": 70, "d": 47,
                         "med": 16.6},
                "GSE71729": {"hr": 1.06, "lr": 0.73, "n": 125, "d": 84,
                             "med": 17.0}}
    ok = True
    for cohort, e in expected.items():
        c = all_res[cohort]["calibration"]
        checks = [
            abs(c["cox_MUC16_HR"] - e["hr"]) <= 0.02,
            abs(c["logrank_MUC16_p"] - e["lr"]) <= 0.01,
            c["n"] == e["n"], c["deces"] == e["d"],
            abs(c["os_mediane_cohorte"] - e["med"]) <= 0.5,
        ]
        out_lines.append(f"  Calibration {cohort} : "
                         + ("OK" if all(checks) else "ÉCHEC") +
                         f" (HR {c['cox_MUC16_HR']} vs {e['hr']} ; "
                         f"log-rank {c['logrank_MUC16_p']} vs {e['lr']} ; "
                         f"n {c['n']}/{e['n']} ; décès {c['deces']}/{e['d']} ; "
                         f"médiane {c['os_mediane_cohorte']}/{e['med']})")
        ok = ok and all(checks)
    if not ok:
        out_lines.append("CALIBRATION ÉCHOUÉE — ARRÊT, aucun résultat "
                         "privilège lu (§6 du protocole).")
        print("\n".join(out_lines))
        with open(f"{BASE}/survival_privilege_883_results.txt", "w") as f:
            f.write("\n".join(out_lines) + "\n")
        raise SystemExit(1)
    out_lines.append("CALIBRATION OK — les 3 cohortes reproduisent MUC16 ; "
                     "lecture des résultats privilège autorisée.")
    out_lines.append("")
    # --- Résultats privilège (lus seulement après calibration OK) ---
    items = PRIV + ["SCORE_PRIV"]
    for item in items:
        cox = [(all_res[c][item]["cox_HR"], all_res[c][item]["cox_p"])
               for c in ("TCGA", "ICGC", "GSE71729")]
        cat = verdict_cat(cox)
        out_lines.append(f"--- {item} : {cat} ---")
        for cohort in ("TCGA", "ICGC", "GSE71729"):
            r = all_res[cohort][item]
            line = (f"  {cohort:9s} Cox HR={r['cox_HR']:.2f} "
                    f"p={r['cox_p']:.4f} ; log-rank Q4 p={r['logrank_p']:.4f} "
                    f"(n={r['n_q4']}, décès={r['deces_q4']}, "
                    f"médiane {r['os_mediane_q4']} vs "
                    f"{r['os_mediane_reste']} mois) ; "
                    f"Spearman vs KRAS rho={r['spearman_KRAS_rho']:+.3f} "
                    f"p={r['spearman_KRAS_p']:.4f}")
            if "cox_DSS_HR" in r:
                line += (f" ; DSS HR={r['cox_DSS_HR']:.2f} "
                         f"p={r['cox_DSS_p']:.4f}")
            out_lines.append(line)
        # Monte avec KRAS ? (≥2/3 cohortes MONTE : rho ≥ +0,15 et p < 0,05)
        monte = sum(1 for c in ("TCGA", "ICGC", "GSE71729")
                    if all_res[c][item]["spearman_KRAS_rho"] >= 0.15
                    and all_res[c][item]["spearman_KRAS_p"] < 0.05)
        out_lines.append(f"  Monte avec KRAS : {monte}/3 cohortes "
                         f"(MONTE = rho ≥ +0,15 et p < 0,05)")
    n_pred = sum(1 for item in items
                 if verdict_cat([(all_res[c][item]["cox_HR"],
                                 all_res[c][item]["cox_p"])
                                for c in ("TCGA", "ICGC", "GSE71729")])
                 == "PRÉDIT COMME CA125")
    out_lines.append("")
    out_lines.append(f"VERDICT D'ENSEMBLE : {n_pred}/8 items "
                     f"« PRÉDIT COMME CA125 » — "
                     + ("AU MOINS UN gène de privilège prédit la survie "
                        "comme CA125." if n_pred >= 1 else
                        "AUCUN gène de privilège ne prédit la survie comme "
                        "CA125 dans nos 3 cohortes."))
    table = pd.concat(tables, ignore_index=True)
    table.to_csv(f"{BASE}/survival_privilege_883_table.csv", index=False)
    with open(f"{BASE}/survival_privilege_883_results.txt", "w") as f:
        f.write("\n".join(out_lines) + "\n")
    with open(f"{BASE}/survival_privilege_883_results.json", "w") as f:
        json.dump(all_res, f, indent=2, ensure_ascii=False)
    print("\n".join(out_lines))
    print(f"Écrit : {BASE}/survival_privilege_883_table.csv, "
          f"survival_privilege_883_results.txt/.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
