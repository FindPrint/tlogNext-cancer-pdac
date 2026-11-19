#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérification indépendante de la survie TCGA (§8.12 du livre blanc).
Motif (16 nov. 2026) : le bras survie GSE71729 a trouvé deux erreurs dans
SON propre premier script (log-rank sur événements entiers au lieu de
booléens ; « univarié » qui était en fait un ajustement à 6 gènes). Le
script de survie TCGA du 15 nov. n'existe plus (exécuté en ligne, seul
tcga_groups_survival.json survit) : on le REFAIT ici, proprement, à partir
des données sauvegardées, et on compare aux chiffres du §8.12.

Données : Firehose PAAD RSEM (data/tcga_paad_rsem.tar.gz, MD5 vérifié
b09569ce3f4721f514bc137bd109ac0a) ; clinique datahub
(data_clinical_patient.txt, 184 patients). Protocole v4 recopié tel quel
(régression sur scores acineux/îlots, résidus, ordre KRAS résidu croissant).
Cox : vraisemblance partielle de Breslow, un gène à la fois pour
l'univarié ; HR par +1 écart-type. Log-rank : Mantel-Haenszel, événements
booléens. Aucune imputation.
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd
from scipy.optimize import minimize

BASE = "/home/hatch/workspace/runs/pdac-v6"
TARBALL = f"{BASE}/data/tcga_paad_rsem.tar.gz"
TARBALL_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
CLIN = f"{BASE}/data_clinical_patient.txt"
GROUPS = f"{BASE}/tcga_groups_survival.json"
OUT = f"{BASE}/tcga_survival_verify_results.txt"

ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]
ISLET = ["INS", "GCG", "PPY", "SST"]
GENES = ["KRAS", "MUC16", "CEACAM5", "PGC", "DPCR1", "CLDN18"]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --- 1. Expression : protocole v4 recopié ---------------------------------
assert md5(TARBALL) == TARBALL_MD5
with tarfile.open(TARBALL, "r:gz") as tf:
    member = [m for m in tf.getmembers() if m.name.endswith(".data.txt")][0]
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
# all_tumors du JSON est dans l'ordre des colonnes de la matrice, pas
# trié : on vérifie l'ensemble + les top12 recalculés, pas l'ordre.
groups = json.load(open(GROUPS))
assert set(order) == set(groups["all_tumors"]), "patients différents"
kras_raw = logmat.loc["KRAS"]  # brut log2(RSEM+1), par échantillon
top_res = set(kras_res.sort_values(ascending=False).head(12).index)
top_raw = set(kras_raw.sort_values(ascending=False).head(12).index)
assert top_res == set(groups["top12_kras_resid"]), "top12 résidu différent"
assert top_raw == set(groups["top12_kras_raw"]), "top12 brut différent"
flux_res = resid_df.loc[["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2",
                         "KRT20", "MUC2", "GSTM1", "CEACAM5", "CLCA1",
                         "MUC16"], order].T

# --- 2. Clinique : jointure par patient (12 premiers caractères) -----------
clin = pd.read_csv(CLIN, sep="\t", skiprows=[1, 2], dtype=str)
clin = clin.rename(columns={"#Patient Identifier": "patient",
                            "Overall Survival Status": "os_status",
                            "Overall Survival (Months)": "os_months"})
clin["os_months"] = pd.to_numeric(clin["os_months"], errors="coerce")
clin = clin[clin["os_months"].notna()].set_index("patient")
# os_status : "0:LIVING" / "1:DECEASED" -> booléen
event = clin["os_status"].astype(str).str.startswith("1")
patients = [c[:12] for c in order]
present = [p for p in patients if p in clin.index]
missing = [p for p in patients if p not in clin.index]
print(f"patients sans survie (exclus) : {missing}")
patients = present
order = [c for c in order if c[:12] in clin.index]
kres = np.array([kras_res[c] for c in order])
kraw = np.array([kras_raw[c] for c in order])
fx = {g: flux_res.loc[order, g].values.astype(float)
      for g in flux_res.columns}
time = clin.loc[patients, "os_months"].values.astype(float)
ev = event.loc[patients].values.astype(bool)
assert len(time) == 177 and ev.sum() == 92, (len(time), int(ev.sum()))
print(f"n={len(time)} décès={int(ev.sum())} OS médiane cohorte="
      f"{np.median(time):.1f}")


# --- 3. Kaplan-Meier + log-rank (Mantel-Haenszel, événements booléens) ----
def km_median(t, e):
    times = np.sort(np.unique(t[e]))
    surv = 1.0
    n_at_risk = len(t)
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
    from scipy.stats import chi2 as chi2_dist
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


def report_group(name, mask):
    m = np.asarray(mask, dtype=bool)
    med = km_median(time[m], ev[m])
    med_rest = km_median(time[~m], ev[~m])
    p = logrank(time, ev, m)
    print(f"{name} | n={int(m.sum())} décès={int(ev[m].sum())} "
          f"médiane={med:.1f} (reste {med_rest:.1f}) log-rank p={p:.4f}")
    return p


def top_mask(values, k):
    idx = np.argsort(values)[::-1][:k]
    m = np.zeros(len(values), dtype=bool)
    m[idx] = True
    return m


def quartile_mask(values):
    q = np.quantile(values, 0.75)
    return values >= q


print("--- Paysage (9 définitions) ---")
top12_r = np.array([c in set(groups["top12_kras_resid"]) for c in order])
top12_w = np.array([c in set(groups["top12_kras_raw"]) for c in order])
top12_s = np.array([c in set(groups["top12_score_kras_ca125_cea"])
                    for c in order])
report_group("top12 KRAS résidu (v4)", top12_r)
report_group("top12 KRAS brut", top12_w)
report_group("top12 score KRAS+CA125+CEA", top12_s)
report_group("top7 KRAS résidu", top_mask(kres, 7))
report_group("top20 KRAS résidu", top_mask(kres, 20))
report_group("quartile sup. MUC16 (CA125) seul", quartile_mask(fx["MUC16"]))
report_group("quartile sup. CEACAM5 (CEA) seul",
             quartile_mask(fx["CEACAM5"]))
report_group("quartile sup. KRAS brut seul", quartile_mask(kraw))
report_group("CA125 ET CEA élevés (2 quartiles sup.)",
             quartile_mask(fx["MUC16"]) & quartile_mask(fx["CEACAM5"]))

# --- 4. Cox continu (Breslow) ----------------------------------------------
def cox_fit(Z, t, e):
    """Z : (n, p) standardisé. Retourne HR, coef, se, p (Wald).
    Newton-Raphson sur la vraisemblance partielle de Breslow (sommes
    cumulées, tri décroissant). CORRECTION 16 nov. 2026 : la première
    version (BFGS + nll avec décalage xb.max() non compensé) gonflait les
    coefficients (MUC16 1,58 au lieu de 1,44 ; DPCR1 1,63 au lieu de 1,43).
    Cette version est vérifiée contre statsmodels PHReg (accord à 0,01 près)
    et contre l'implémentation indépendante de survival_geo71729.py.
    """
    from math import erf, sqrt

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
    from scipy.stats import norm
    pval = 2 * (1 - norm.cdf(np.abs(z)))
    return np.exp(beta), beta, se, np.atleast_1d(pval)


def zscore(v):
    v = np.asarray(v, dtype=float)
    return (v - v.mean()) / v.std(ddof=0)


print("--- Cox univarié (un gène à la fois, HR par +1 sd) ---")
covs = {"KRAS résidu": zscore(kres), "KRAS brut": zscore(kraw),
        "MUC16": zscore(fx["MUC16"]), "CEACAM5": zscore(fx["CEACAM5"]),
        "PGC": zscore(fx["PGC"]), "DPCR1": zscore(fx["DPCR1"]),
        "CLDN18": zscore(fx["CLDN18"])}
for name, z in covs.items():
    hr, b, se, p = cox_fit(z.reshape(-1, 1), time, ev)
    print(f"  {name:12s} HR={hr[0]:.2f} coef={b[0]:+.2f} se={se[0]:.2f} "
          f"p={p[0]:.4f}")

print("--- Cox multivarié KRAS résidu + MUC16 + CEACAM5 ---")
Zm = np.column_stack([covs["KRAS résidu"], covs["MUC16"], covs["CEACAM5"]])
hr, b, se, p = cox_fit(Zm, time, ev)
for name, h, bb, s, pp in zip(["KRAS résidu", "MUC16", "CEACAM5"],
                              hr, b, se, p):
    print(f"  {name:12s} HR={h:.2f} coef={bb:+.2f} se={s:.2f} p={pp:.4f}")

print("--- Cox ajusté 6 gènes (référence) ---")
Z6 = np.column_stack([covs["KRAS résidu"], covs["MUC16"], covs["CEACAM5"],
                      covs["PGC"], covs["DPCR1"], covs["CLDN18"]])
hr, b, se, p = cox_fit(Z6, time, ev)
for name, h, bb, s, pp in zip(["KRAS résidu", "MUC16", "CEACAM5", "PGC",
                               "DPCR1", "CLDN18"], hr, b, se, p):
    print(f"  {name:12s} HR={h:.2f} coef={bb:+.2f} se={s:.2f} p={pp:.4f}")
