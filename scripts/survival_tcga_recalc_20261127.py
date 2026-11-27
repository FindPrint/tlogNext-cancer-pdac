#!/usr/bin/env python3
"""Recalcul INDEPENDANT survie TCGA §8.12 (enquete 27 nov. 2026).
Lecture seule des donnees. Ecrit ses sorties sur stdout uniquement.
Outils : lifelines 0.30.3, statsmodels 0.15.0, scipy 1.18.1 + implementation
Cox Breslow maison (Newton-Raphson, ecrite de zero, validee sur donnees
simulees a beta connu avant usage sur les vraies donnees).
"""
import hashlib, tarfile, json
import numpy as np
import pandas as pd
from scipy.stats import norm, chi2 as chi2_dist

BASE = "/home/hatch/workspace/runs/pdac-v6"
TARBALL = f"{BASE}/data/tcga_paad_rsem.tar.gz"
CLIN = f"{BASE}/data_clinical_patient.txt"
GROUPS = f"{BASE}/tcga_groups_survival.json"

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

print("SHA256 tarball:", sha256(TARBALL))
print("MD5 tarball:", md5(TARBALL))
print("SHA256 clinique:", sha256(CLIN))
print("SHA256 groups:", sha256(GROUPS))
print("SHA256 fluxes_v4:", sha256(f"{BASE}/pdac_tcga_fluxes_v4.csv"))

# ---------- 1. Expression ----------
with tarfile.open(TARBALL, "r:gz") as tf:
    member = [m for m in tf.getmembers() if m.name.endswith(".data.txt")][0]
    print("membre tarball:", member.name)
    df = pd.read_csv(tf.extractfile(member), sep="\t", index_col=0, low_memory=False)
df.index = df.index.to_series().str.split("|").str[0]
df = df[~df.index.duplicated(keep="first")]
cols = df.columns.to_series()
tumor_cols = cols[cols.str[13:15] == "01"]
mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
mat = mat[~mat.isna().any(axis=1)]
logmat = np.log2(mat + 1.0)
print("tumeurs primaires:", logmat.shape[1], "| genes:", logmat.shape[0])

ACINAR = ["PNLIP","CTRB2","CELA3A","CTRB1","CPA1","CELA2A","CPB1","CELA3B","CLPS","CTRC","CPA2"]
ISLET = ["INS","GCG","PPY","SST"]
GENES = ["KRAS","MUC16","CEACAM5","PGC","DPCR1","CLDN18"]
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
groups = json.load(open(GROUPS))
assert set(order) == set(groups["all_tumors"])
top_res = set(kras_res.sort_values(ascending=False).head(12).index)
top_raw = set(logmat.loc["KRAS"].sort_values(ascending=False).head(12).index)
assert top_res == set(groups["top12_kras_resid"])
assert top_raw == set(groups["top12_kras_raw"])
print("top12 residu/brut conformes au JSON groupes: OK")

# ---------- 2. Clinique ----------
clin = pd.read_csv(CLIN, sep="\t", skiprows=[1, 2], dtype=str)
clin = clin.rename(columns={"#Patient Identifier": "patient",
    "Overall Survival Status": "os_status",
    "Overall Survival (Months)": "os_months",
    "Diagnosis Age": "age",
    "Sex": "sex",
    "Neoplasm Disease Stage American Joint Committee on Cancer Code": "stage",
    "American Joint Committee on Cancer Tumor Stage Code": "pt",
    "Neoplasm Disease Lymph Node Stage American Joint Committee on Cancer Code": "pn",
    "American Joint Committee on Cancer Metastasis Stage Code": "pm"})
print("lignes cliniques (hors 2 lignes descriptives):", len(clin))
print("OS_STATUS brut:", clin["os_status"].value_counts(dropna=False).to_dict())
clin["os_months"] = pd.to_numeric(clin["os_months"], errors="coerce")
clin["age"] = pd.to_numeric(clin["age"], errors="coerce")
clin = clin[clin["os_months"].notna()].set_index("patient")
event = clin["os_status"].astype(str).str.startswith("1")
patients = [c[:12] for c in order]
missing = [p for p in patients if p not in clin.index]
print("patients ARN sans survie:", missing)
patients = [p for p in patients if p in clin.index]
order = [c for c in order if c[:12] in clin.index]
time = clin.loc[patients, "os_months"].values.astype(float)
ev = event.loc[patients].values.astype(bool)
print(f"n={len(time)} deces={int(ev.sum())} OS mois: min={time.min():.2f} "
      f"max={time.max():.2f} mediane brute={np.median(time):.1f}")
print("sexe (n=177):", clin.loc[patients, "sex"].value_counts(dropna=False).to_dict())
print("age: n manquant =", int(clin.loc[patients, "age"].isna().sum()),
      "mediane =", float(np.nanmedian(clin.loc[patients, "age"].values)))
print("stade brut (n=177):", clin.loc[patients, "stage"].value_counts(dropna=False).to_dict())
print("pT:", clin.loc[patients, "pt"].value_counts(dropna=False).to_dict())
print("pN:", clin.loc[patients, "pn"].value_counts(dropna=False).to_dict())
print("pM:", clin.loc[patients, "pm"].value_counts(dropna=False).to_dict())

# ---------- 3. Cox maison (Breslow, Newton-Raphson) ----------
def cox_breslow_home(Z, t, e):
    """Z (n,p) deja standardise. Retourne beta, se, p, HR. Implementation
    ecrite de zero : vraisemblance partielle de Breslow, sommes sur les
    ensembles a risque a chaque temps d'evenement distinct."""
    Z = np.asarray(Z, dtype=float); t = np.asarray(t, dtype=float)
    e = np.asarray(e, dtype=bool)
    n, p = Z.shape
    ut = np.sort(np.unique(t[e]))
    beta = np.zeros(p)
    for _ in range(100):
        eta = Z @ beta
        w = np.exp(eta - eta.max())
        grad = np.zeros(p); hess = np.zeros((p, p))
        for tt in ut:
            risk = t >= tt
            d = int(np.sum((t == tt) & e))
            Zr = Z[risk]; wr = w[risk]
            S0 = wr.sum()
            S1 = (Zr * wr[:, None]).sum(axis=0)
            S2 = (Zr[:, :, None] * Zr[:, None, :] * wr[:, None, None]).sum(axis=0)
            mean = S1 / S0
            grad += Z[(t == tt) & e].sum(axis=0) - d * mean
            hess -= d * (S2 / S0 - np.outer(mean, mean))
        try:
            step = np.linalg.solve(hess, grad)
        except np.linalg.LinAlgError:
            break
        beta = beta - step
        if np.max(np.abs(step)) < 1e-10:
            break
    cov = np.linalg.inv(-hess)
    se = np.sqrt(np.diag(cov))
    z = beta / se
    pval = 2 * (1 - norm.cdf(np.abs(z)))
    return beta, se, pval

# Validation du fitter maison sur donnees simulees a beta connu
rng = np.random.default_rng(42)
n_sim = 4000
z_sim = rng.normal(size=n_sim)
beta_true = 0.7
haz = np.exp(beta_true * z_sim)
T_sim = rng.exponential(1.0 / haz)
C_sim = rng.exponential(0.5, size=n_sim)
t_sim = np.minimum(T_sim, C_sim)
e_sim = T_sim <= C_sim
b_sim, se_sim, p_sim = cox_breslow_home(z_sim.reshape(-1, 1), t_sim, e_sim)
print(f"[validation fitter maison] beta vrai={beta_true} estime={b_sim[0]:.3f} "
      f"se={se_sim[0]:.3f} p={p_sim[0]:.2e} (attendu ~0.70 +- 0.05)")

# ---------- 4. Kaplan-Meier maison + log-rank maison ----------
def km_median_home(t, e):
    surv = 1.0
    for tt in np.sort(np.unique(t[e])):
        at_risk = np.sum(t >= tt); d = np.sum((t == tt) & e)
        surv *= (1.0 - d / at_risk)
        if surv <= 0.5:
            return float(tt)
    return float("nan")

def km_curve_home(t, e):
    surv = 1.0; out = []
    for tt in np.sort(np.unique(t[e])):
        at_risk = np.sum(t >= tt); d = np.sum((t == tt) & e)
        surv *= (1.0 - d / at_risk)
        out.append((float(tt), float(surv)))
    return out

def logrank_home(t, e, grp):
    O = E = V = 0.0
    for tt in np.sort(np.unique(t[e])):
        r = t >= tt; r1 = int(np.sum(r & grp)); r0 = int(np.sum(r & ~grp))
        n_ = r1 + r0; d = int(np.sum((t == tt) & e))
        d1 = int(np.sum((t == tt) & e & grp))
        if n_ < 2 or d == 0:
            continue
        O += d1; E += d * r1 / n_
        V += (r1 * r0 * d * (n_ - d)) / (n_ * n_ * (n_ - 1))
    z2 = (O - E) ** 2 / V
    return float(1.0 - chi2_dist.cdf(z2, 1)), float(O), float(E), float(V)

print(f"[KM maison] mediane survie cohorte entiere = {km_median_home(time, ev):.1f} mois")
print(f"[KM maison] S(12)={dict(km_curve_home(time, ev)).get(12.0, float('nan'))}")

# ---------- 5. Covariables ----------
def zscore(v, ddof=0):
    v = np.asarray(v, dtype=float)
    return (v - v.mean()) / v.std(ddof=ddof)

kres = np.array([resid_df.loc["KRAS", c] for c in order])
kraw = np.array([logmat.loc["KRAS", c] for c in order])
resid_cov = {g: np.array([resid_df.loc[g, c] for c in order]) for g in GENES}
raw_cov = {g: np.array([logmat.loc[g, c] for c in order]) for g in GENES}
print("correlation residu vs brut par gene (Spearman approx Pearson sur rangs):")
for g in GENES:
    print(f"  {g}: pearson residu/brut = {np.corrcoef(resid_cov[g], raw_cov[g])[0,1]:.3f} "
          f"| sd residu={resid_cov[g].std(ddof=0):.3f} sd brut={raw_cov[g].std(ddof=0):.3f}")

# ---------- 6. Cox : 3 implementations x 2 versions de covariables ----------
from lifelines import CoxPHFitter
from lifelines.statistics import logrank_test
from statsmodels.duration.hazard_regression import PHReg

def run_cox(label, Zdict, t, e, keys):
    print(f"--- {label} ---")
    for k in keys:
        z = zscore(Zdict[k], ddof=0).reshape(-1, 1)
        b, se, p = cox_breslow_home(z, t, e)
        res_b = PHReg(t, z, status=e.astype(int), ties="breslow").fit(disp=0)
        res_e = PHReg(t, z, status=e.astype(int), ties="efron").fit(disp=0)
        dfl = pd.DataFrame({"z": z[:, 0], "T": t, "E": e.astype(int)})
        cph = CoxPHFitter().fit(dfl, duration_col="T", event_col="E")
        print(f"  {k:10s} MAISON Breslow HR={np.exp(b[0]):.4f} p={p[0]:.4g} | "
              f"statsmodels Breslow HR={np.exp(res_b.params[0]):.4f} p={res_b.pvalues[0]:.4g} | "
              f"statsmodels Efron HR={np.exp(res_e.params[0]):.4f} p={res_e.pvalues[0]:.4g} | "
              f"lifelines(Efron) HR={np.exp(cph.params_['z']):.4f} p={cph.summary['p']['z']:.4g}")

run_cox("Cox UNIVARIE, covariables = RESIDUS v4 (corriges purete), z ddof=0",
        resid_cov, time, ev, GENES)
run_cox("Cox UNIVARIE, covariables = BRUTES log2(RSEM+1), z ddof=0",
        raw_cov, time, ev, GENES)
# KRAS residu vs brut (meme chose que GENES KRAS residu ; brut deja dans raw)
# ddof=1 variante sur residus
print("--- variante ddof=1 (residus) ---")
for k in ["KRAS", "MUC16", "CEACAM5", "DPCR1"]:
    z = zscore(resid_cov[k], ddof=1).reshape(-1, 1)
    b, se, p = cox_breslow_home(z, time, ev)
    print(f"  {k:10s} MAISON Breslow HR={np.exp(b[0]):.4f} p={p[0]:.4g}")

def run_multi(label, Zmat, names, t, e):
    b, se, p = cox_breslow_home(Zmat, t, e)
    res_b = PHReg(t, Zmat, status=e.astype(int), ties="breslow").fit(disp=0)
    dfl = pd.DataFrame(Zmat, columns=names); dfl["T"] = t; dfl["E"] = e.astype(int)
    cph = CoxPHFitter().fit(dfl, duration_col="T", event_col="E")
    print(f"--- {label} ---")
    for i, nm in enumerate(names):
        print(f"  {nm:10s} MAISON HR={np.exp(b[i]):.4f} p={p[i]:.4g} | "
              f"statsmodels Breslow HR={np.exp(res_b.params[i]):.4f} p={res_b.pvalues[i]:.4g} | "
              f"lifelines HR={np.exp(cph.params_[nm]):.4f} p={cph.summary['p'][nm]:.4g}")

Zm_res = np.column_stack([zscore(resid_cov[g]) for g in ["KRAS", "MUC16", "CEACAM5"]])
run_multi("MULTIVARIE marqueurs seuls, RESIDUS", Zm_res, ["KRAS", "MUC16", "CEACAM5"], time, ev)
Zm_raw = np.column_stack([zscore(raw_cov[g]) for g in ["KRAS", "MUC16", "CEACAM5"]])
run_multi("MULTIVARIE marqueurs seuls, BRUTS", Zm_raw, ["KRAS", "MUC16", "CEACAM5"], time, ev)
Z6_res = np.column_stack([zscore(resid_cov[g]) for g in GENES])
run_multi("AJUSTE 6 genes, RESIDUS", Z6_res, GENES, time, ev)
Z6_raw = np.column_stack([zscore(raw_cov[g]) for g in GENES])
run_multi("AJUSTE 6 genes, BRUTS", Z6_raw, GENES, time, ev)

# ---------- 7. Multivarie + covariables cliniques ----------
age = clin.loc[patients, "age"].values.astype(float)
sex_m = (clin.loc[patients, "sex"] == "Male").astype(float).values
stage = clin.loc[patients, "stage"].values
def stage_group(s):
    if not isinstance(s, str):
        return -1  # manquant
    s = s.strip().upper()
    if s in ("STAGE I", "STAGE IA", "STAGE IB"):
        return 0
    if s in ("STAGE IIA", "STAGE IIB"):
        return 1
    if s in ("STAGE III", "STAGE IV"):
        return 2
    return -1
sg = np.array([stage_group(s) for s in stage])
print("stade regroupe I / II / III-IV / manquant:", [(k, int((sg == k).sum())) for k in (-1, 0, 1, 2)], "| manquants age:", int(np.isnan(age).sum()))
ok = (~np.isnan(age)) & (sg >= 0)
print(f"sous-echantillon avec age renseigne: n={int(ok.sum())} deces={int(ev[ok].sum())}")
age_z = zscore(age[ok])
Zm_clin = np.column_stack([zscore(resid_cov["KRAS"])[ok], zscore(resid_cov["MUC16"])[ok],
                           zscore(resid_cov["CEACAM5"])[ok], age_z,
                           sex_m[ok], (sg[ok] >= 2).astype(float)])
run_multi("MULTIVARIE marqueurs + age(z) + sexe(H=1) + stade III-IV (n=age connu)",
          Zm_clin, ["KRAS", "MUC16", "CEACAM5", "age_z", "sexe_M", "stade34"], time[ok], ev[ok])
# variante stade en 3 niveaux (II vs I, III-IV vs I)
d2 = (sg[ok] == 1).astype(float); d3 = (sg[ok] >= 2).astype(float)
Zm_clin2 = np.column_stack([zscore(resid_cov["KRAS"])[ok], zscore(resid_cov["MUC16"])[ok],
                            zscore(resid_cov["CEACAM5"])[ok], age_z, sex_m[ok], d2, d3])
run_multi("MULTIVARIE marqueurs + age(z) + sexe + stade II + stade III-IV (ref=I)",
          Zm_clin2, ["KRAS", "MUC16", "CEACAM5", "age_z", "sexe_M", "stadeII", "stade34"],
          time[ok], ev[ok])
# age brut (par an) seul + sexe seul + stade seul, descriptif
b, se, p = cox_breslow_home(age[ok].reshape(-1, 1), time[ok], ev[ok])
print(f"age seul (par an): HR={np.exp(b[0]):.4f} p={p[0]:.4g}")
b, se, p = cox_breslow_home(sex_m.reshape(-1, 1), time, ev)
print(f"sexe seul (H vs F): HR={np.exp(b[0]):.4f} p={p[0]:.4g}")
b, se, p = cox_breslow_home((sg >= 2).astype(float).reshape(-1, 1), time, ev)
print(f"stade III-IV seul vs I-II: HR={np.exp(b[0]):.4f} p={p[0]:.4g}")

# ---------- 8. Paysage log-rank + KM ----------
from lifelines import KaplanMeierFitter
kmf = KaplanMeierFitter().fit(time, ev)
print(f"[KM lifelines] mediane survie cohorte = {kmf.median_survival_time_:.1f} mois")
top12 = np.array([c in top_res for c in order])
p_home, O, E, V = logrank_home(time, ev, top12)
res_lr = logrank_test(time[top12], time[~top12], ev[top12], ev[~top12])
print(f"top12 KRAS residu: n={int(top12.sum())} deces={int(ev[top12].sum())} "
      f"mediane={km_median_home(time[top12], ev[top12]):.1f} (reste "
      f"{km_median_home(time[~top12], ev[~top12]):.1f}) | log-rank maison p={p_home:.4f} "
      f"| lifelines p={res_lr.p_value:.4f}")
top20 = np.zeros(len(time), dtype=bool)
top20[np.argsort(kres)[::-1][:20]] = True
p_home20, _, _, _ = logrank_home(time, ev, top20)
res_lr20 = logrank_test(time[top20], time[~top20], ev[top20], ev[~top20])
print(f"top20 KRAS residu: n={int(top20.sum())} deces={int(ev[top20].sum())} "
      f"mediane={km_median_home(time[top20], ev[top20]):.1f} (reste "
      f"{km_median_home(time[~top20], ev[~top20]):.1f}) | log-rank maison p={p_home20:.4f} "
      f"| lifelines p={res_lr20.p_value:.4f}")
# median-split dichotomise (hypothese d'ecart) : KRAS residu au-dessus de la mediane
med = np.zeros(len(time), dtype=bool); med[kres >= np.median(kres)] = True
b, se, p = cox_breslow_home(med.astype(float).reshape(-1, 1), time, ev)
print(f"[hypothese] Cox KRAS residu DICHOTOMISE (mediane): HR={np.exp(b[0]):.4f} p={p[0]:.4g}")
print("FIN RECALCUL")
