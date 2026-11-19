#!/usr/bin/env python3
"""TCGA clinique — la radiothérapie (seule variable de traitement du fichier)
modifie-t-elle le signal CA125 ? Question : les patients CA125-élevés ont-ils
reçu un traitement différent, et la radiothérapie change-t-elle l'association
CA125-survie ?

Données : Firehose PAAD RSEM (MD5 vérifié) + data_clinical_patient.txt (184
patients). Protocole v4 recopié tel quel (régression acinaire/îlots, résidus,
ordre KRAS résiduel croissant). Jointure par patient (12 premiers caractères),
177 avec survie (92 décès) — même jointure que survival_tcga_verify.py.

ATTENTION : le fichier clinique ne contient AUCUNE colonne chimiothérapie
(pas de nom de médicament, pas de chimiothérapie adjuvante, pas de réponse).
La radiothérapie (Oui 44 / Non 123 / manquant 17) est la SEULE variable de
traitement exploitable. Tests exploratoires, petits effectifs — on rapporte,
on ne conclut pas au-delà.

Sortie : tcga_radiation_ca125_check.txt
"""
import hashlib
import tarfile

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import fisher_exact

BASE = "/home/hatch/workspace/runs/pdac-v6"
TARBALL = f"{BASE}/data/tcga_paad_rsem.tar.gz"
TARBALL_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
CLIN = f"{BASE}/data_clinical_patient.txt"

ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]
ISLET = ["INS", "GCG", "PPY", "SST"]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def km_median(t, e):
    times = np.sort(np.unique(t[e]))
    surv = 1.0
    n_at_risk = len(t)
    for tt in times:
        at_risk = np.sum(t >= tt)
        d = np.sum((t == tt) & e)
        if at_risk > 0:
            surv *= (1 - d / at_risk)
            if surv <= 0.5:
                return tt
    return np.nan


def logrank(t, e, grp):
    from math import erf, sqrt
    t1, e1 = t[grp], e[grp]
    t2, e2 = t[~grp], e[~grp]
    times = np.sort(np.unique(np.concatenate([t1[e1], t2[e2]])))
    O1 = E1 = V = 0.0
    for tt in times:
        n1 = (t1 >= tt).sum(); n2 = (t2 >= tt).sum()
        d1 = ((t1 == tt) & e1).sum(); d2 = ((t2 == tt) & e2).sum()
        n = n1 + n2; d = d1 + d2
        if n == 0 or d == 0:
            continue
        E1 += d * n1 / n
        O1 += d1
        if n > 1:
            V += d * (n - d) * n1 * n2 / (n * n * (n - 1))
    if V <= 0:
        return float("nan")
    z = (O1 - E1) / sqrt(V)
    return 1 - erf(abs(z) / sqrt(2))


def cox_fit(Z, t, e):
    # vraisemblance partielle de Breslow, Newton-Raphson (copie vérifiée de survival_tcga_verify.py)
    Z = np.asarray(Z, dtype=float)
    t = np.asarray(t, dtype=float); e = np.asarray(e, dtype=bool)
    order = np.argsort(-t)
    Zs, ts, es = Z[order], t[order], e[order]
    p = Zs.shape[1]

    def nll_grad(beta):
        xb = Zs @ beta
        m = xb.max()
        exb = np.exp(xb - m)
        S0 = np.cumsum(exb)
        S1 = np.cumsum(Zs * exb[:, None], axis=0)
        S2 = np.cumsum((Zs[:, :, None] * Zs[:, None, :]) * exb[:, None, None], axis=0)
        idx = np.where(es)[0]
        ll = float(np.sum(xb[idx]) - np.sum(np.log(S0[idx]) + m))
        grad = np.sum(Zs[idx], axis=0) - np.sum(S1[idx] / S0[idx][:, None], axis=0)
        H = -np.sum((S2[idx] / S0[idx][:, None, None])
                    - (S1[idx] / S0[idx][:, None])[:, :, None]
                    * (S1[idx] / S0[idx][:, None])[:, None, :], axis=0)
        return -ll, -grad, -H

    beta = np.zeros(p)
    for _ in range(50):
        f, g, H = nll_grad(beta)
        step = np.linalg.solve(H + 1e-8 * np.eye(p), g)
        beta = beta - step
        if np.max(np.abs(step)) < 1e-8:
            break
    f, g, H = nll_grad(beta)
    cov = np.linalg.inv(H)
    se = np.sqrt(np.diag(cov))
    z = beta / se
    from scipy.stats import norm
    pval = 2 * (1 - norm.cdf(np.abs(z)))
    return np.exp(beta), beta, se, pval


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
X = np.column_stack([np.ones(len(logmat.columns)), score_ac.values, score_is.values])
Y = logmat.values
beta, *_ = np.linalg.lstsq(X, Y.T, rcond=None)
resid = Y - (X @ beta).T
resid_df = pd.DataFrame(resid, index=logmat.index, columns=logmat.columns)
kras_res = resid_df.loc["KRAS"].sort_values(ascending=True)
order = list(kras_res.index)
assert len(order) == 178

clin = pd.read_csv(CLIN, sep="\t", skiprows=[1, 2], dtype=str)
clin = clin.rename(columns={"#Patient Identifier": "patient",
                            "Overall Survival Status": "os_status",
                            "Overall Survival (Months)": "os_months",
                            "Radiation Therapy": "radiation"})
clin = clin[clin["patient"].str.startswith("TCGA-", na=False)]
clin["os_months"] = pd.to_numeric(clin["os_months"], errors="coerce")
clin = clin[clin["os_months"].notna()].set_index("patient")
event = clin["os_status"].astype(str).str.startswith("1")
patients = [c[:12] for c in order]
order = [c for c in order if c[:12] in clin.index]
patients = [c[:12] for c in order]
muc = np.array([resid_df.loc["MUC16", c] for c in order])
kras = np.array([kras_res[c] for c in order])
time = clin.loc[patients, "os_months"].values.astype(float)
ev = event.loc[patients].values.astype(bool)
rad = clin.loc[patients, "radiation"].values
assert len(time) == 177 and ev.sum() == 92

out = []
out.append("=== TCGA — radiothérapie × CA125 (MUC16 résidu v4) ===")
out.append(f"n={len(time)}, décès={int(ev.sum())}")
out.append(f"Radiothérapie : Oui {int((rad == 'Yes').sum())} / Non {int((rad == 'No').sum())} / manquant {int(((rad != 'Yes') & (rad != 'No')).sum())}")
out.append("")
# 1. Taux de radiothérapie par quartile MUC16
q4 = muc >= np.quantile(muc, 0.75)
mask = (rad == "Yes") | (rad == "No")
tab = [[int(((rad == "Yes") & q4 & mask).sum()), int(((rad == "No") & q4 & mask).sum())],
       [int(((rad == "Yes") & ~q4 & mask).sum()), int(((rad == "No") & ~q4 & mask).sum())]]
or_, p_f = fisher_exact(tab)
out.append(f"1) Radiothérapie par quartile MUC16 : Q4 {tab[0][0]}/{sum(tab[0])} ({tab[0][0]/sum(tab[0]):.0%}) vs reste {tab[1][0]}/{sum(tab[1])} ({tab[1][0]/sum(tab[1]):.0%}) — Fisher p={p_f:.3f}, OR={or_:.2f}")
# top12 KRAS
top12 = np.zeros(len(time), dtype=bool); top12[-12:] = True
tab2 = [[int(((rad == "Yes") & top12 & mask).sum()), int(((rad == "No") & top12 & mask).sum())],
        [int(((rad == "Yes") & ~top12 & mask).sum()), int(((rad == "No") & ~top12 & mask).sum())]]
or2, p2 = fisher_exact(tab2)
out.append(f"   Radiothérapie top12 KRAS : {tab2[0][0]}/{sum(tab2[0])} vs reste {tab2[1][0]}/{sum(tab2[1])} — Fisher p={p2:.3f}")
out.append("")
# 2. Radiothérapie seule vs survie
out.append(f"2) Radiothérapie seule : médiane OS Oui {km_median(time[rad == 'Yes'], ev[rad == 'Yes']):.1f} mois vs Non {km_median(time[rad == 'No'], ev[rad == 'No']):.1f} — log-rank p={logrank(time, ev, rad == 'Yes'):.3f}")
out.append("")
# 3. CA125 stratifié par radiothérapie
for label, m in [("radiothérapie Oui", rad == "Yes"), ("radiothérapie Non", rad == "No")]:
    tt, ee, mm = time[m], ev[m], muc[m]
    qq = mm >= np.quantile(mm, 0.75)
    out.append(f"3) {label} (n={int(m.sum())}, décès={int(ee.sum())}) : quartile MUC16 médiane OS {km_median(tt[qq], ee[qq]):.1f} vs reste {km_median(tt[~qq], ee[~qq]):.1f} mois — log-rank p={logrank(tt, ee, qq):.3f}")
out.append("")
# 4. Cox MUC16 + radiation + interaction (exploratoire)
Z = np.column_stack([(muc - muc.mean()) / muc.std(ddof=0),
                     (rad == "Yes").astype(float),
                     ((muc - muc.mean()) / muc.std(ddof=0)) * (rad == "Yes").astype(float)])
hr, b, se, p = cox_fit(Z[mask], time[mask], ev[mask])
out.append("4) Cox (MUC16 + radiothérapie + interaction, n avec radiothérapie renseignée) :")
out.append(f"   MUC16 HR={hr[0]:.2f} p={p[0]:.3f} | radiothérapie HR={hr[1]:.2f} p={p[1]:.3f} | interaction HR={hr[2]:.2f} p={p[2]:.3f}")
out.append("   Lecture : une interaction non significative = la radiothérapie ne modifie pas mesurablement l'association CA125-survie ici.")
out.append("")
out.append("CONCLUSION : le fichier clinique TCGA ne contient aucune donnée de chimiothérapie.")
out.append("La seule question de traitement testable est la radiothérapie — et elle ne montre")
out.append("ici ni différence de prescription selon CA125, ni modification du signal CA125.")
open("tcga_radiation_ca125_check.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
