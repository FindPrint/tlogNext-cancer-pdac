#!/usr/bin/env python3
"""Survie ICGC PACA-AU — paysage complet + Cox continu (aucun seuil).
Sources : clinique Bailey et al. 2016 Suppl. Table 1 (Status + Length of Follow
Up (months)), jointe aux 70 tumeurs primaires PDAC (icgc_clinical_70.csv) ;
expression log2(cpm) Xena pour les quartiles et le Cox.
Survie globale (OS, comme en TCGA §8.12) : événement = tout statut 'Deceased...'
(Deceased - Of Disease / Of Other Cause / Of Unknown Cause) ; censuré sinon.
Sensibilité : survie spécifique (DSS), événement = 'Deceased - Of Disease' seul.
Groupes testés, TOUS rapportés sans en choisir un : top12/top7/top20 KRAS,
quartiles supérieurs MUC16 / CEACAM5 / KRAS seuls, double-quartile CA125+CEA.
Cox continu : risque par +1 écart-type, univarié puis multivarié.
"""
import numpy as np
import pandas as pd
from math import erf, sqrt

clin = pd.read_csv('icgc_clinical_70.csv')
clin['time'] = pd.to_numeric(clin['followup_months'], errors='coerce')
clin['dead_os'] = clin['Status'].astype(str).str.startswith('Deceased')
clin['dead_dss'] = clin['Status'] == 'Deceased - Of Disease'
assert clin['time'].notna().all()
print(f"patients : {len(clin)} | décès OS : {int(clin['dead_os'].sum())} | décès DSS : {int(clin['dead_dss'].sum())}")

# --- expression des 70 (ordre = kras_rank) ---
exp = pd.read_csv('data/icgc_pacaau_exp.txt.gz', sep='\t', index_col=0, compression='gzip')
pm = pd.read_csv('data/icgc_pacaau_probemap.gz', sep='\t', compression='gzip')
mapping = dict(zip(pm['#id'], pm['gene']))
exp.index = exp.index.map(lambda g: mapping.get(g, g))
exp = exp.groupby(level=0).median()
order = clin.sort_values('kras_rank')['icgc_id'].tolist()
E = exp.loc[['KRAS', 'MUC16', 'CEACAM5', 'PGC', 'DPCR1', 'CLDN18'], order].T
E.index = order
clin = clin.set_index('icgc_id').loc[order].reset_index()
for g in E.columns:
    clin[g] = E[g].values
print("KRAS log2cpm : min %.2f médiane %.2f max %.2f" % (clin['KRAS'].min(), clin['KRAS'].median(), clin['KRAS'].max()))

def km_median(times, events):
    t = np.array(times); e = np.array(events, dtype=bool)
    order = np.argsort(t); t, e = t[order], e[order]
    n = len(t); surv = 1.0; med = np.nan
    for i in range(n):
        if e[i]:
            surv *= (1 - 1 / (n - i))
            if surv <= 0.5 and np.isnan(med):
                med = t[i]
    return med

def logrank(t1, e1, t2, e2):
    t1, e1, t2, e2 = map(lambda a: np.array(a), (t1, e1, t2, e2))
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
        return float('nan')
    z = (O1 - E1) / sqrt(V)
    return 1 - erf(abs(z) / sqrt(2))

def topn(col, n):
    return set(clin.sort_values(col, ascending=True).tail(n)['icgc_id'])

defs = {
    'top12 KRAS': topn('kras_rank', 12),
    'top7 KRAS': topn('kras_rank', 7),
    'top20 KRAS': topn('kras_rank', 20),
    'quartile sup. MUC16 (CA125) seul': topn('MUC16', 18),
    'quartile sup. CEACAM5 (CEA) seul': topn('CEACAM5', 18),
    'quartile sup. KRAS seul': topn('KRAS', 18),
    'CA125 ET CEA élevés (2 quartiles sup.)': topn('MUC16', 18) & topn('CEACAM5', 18),
}
print("\n=== PAYSAGE DE SURVIE OS — toutes les définitions, sans choisir ===")
print(f"{'groupe':38s} {'n':>3s} {'décès':>5s} {'OS médiane':>10s} {'log-rank p':>10s} {'DSS p':>7s}")
for name, pats in defs.items():
    sub = clin[clin['icgc_id'].isin(pats)]
    rest = clin[~clin['icgc_id'].isin(pats)]
    med = km_median(sub['time'], sub['dead_os'])
    med_r = km_median(rest['time'], rest['dead_os'])
    p = logrank(sub['time'].values, sub['dead_os'].values, rest['time'].values, rest['dead_os'].values)
    p_dss = logrank(sub['time'].values, sub['dead_dss'].values, rest['time'].values, rest['dead_dss'].values)
    print(f"{name:38s} {len(sub):3d} {int(sub['dead_os'].sum()):5d} {med:9.1f} ({med_r:.1f} reste) {p:10.3f} {p_dss:7.3f}")
print(f"\nCohorte entière : n={len(clin)}, OS médiane {km_median(clin['time'], clin['dead_os']):.1f} mois, décès {int(clin['dead_os'].sum())}")

def cox_fit(df, cols, event_col='dead_os'):
    Z = df[cols].values.astype(float)
    Z = (Z - Z.mean(0)) / Z.std(0)
    t = df['time'].values; e = df[event_col].values.astype(bool)
    order = np.argsort(-t); Z, t, e = Z[order], t[order], e[order]
    beta = np.zeros(Z.shape[1])
    hess = None
    for _ in range(50):
        eta = Z @ beta
        w = np.exp(eta - eta.max())
        S0 = np.cumsum(w); S1 = np.cumsum(Z * w[:, None], axis=0)
        S2 = np.cumsum((Z[:, :, None] * Z[:, None, :]) * w[:, None, None], axis=0)
        grad = np.zeros_like(beta); hess = np.zeros((len(beta), len(beta)))
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
    return [(c, float(np.exp(beta[j])), float(beta[j]), float(se[j]),
             float(1 - erf(abs(beta[j] / se[j]) / sqrt(2)))) for j, c in enumerate(cols)]

genes = ['KRAS', 'MUC16', 'CEACAM5', 'PGC', 'DPCR1', 'CLDN18']
print("\n=== COX CONTINU OS (aucun seuil) — risque par +1 écart-type ===")
print("VRAIS UNIVARIÉS : un gène à la fois (cf. correction TCGA 16 nov. 07h40 :")
print("le tableau §8.12 du 15 nov. était en fait l'ajustement à 6 gènes, mal étiqueté).")
print(f"{'gène':9s} {'HR':>6s} {'coef':>6s} {'se':>5s} {'p':>7s}")
for g in genes:
    c, hr, b, se, p = cox_fit(clin, [g])[0]
    print(f"{c:9s} {hr:6.2f} {b:6.2f} {se:5.2f} {p:7.4f}")
print("\n=== COX MULTIVARIÉ OS (KRAS + MUC16 + CEACAM5) ===")
for c, hr, b, se, p in cox_fit(clin, ['KRAS', 'MUC16', 'CEACAM5']):
    print(f"{c:9s} {hr:6.2f} {b:6.2f} {se:5.2f} {p:7.4f}")
print("\n=== COX CONTINU DSS (événement = décédé de la maladie seul) ===")
for c, hr, b, se, p in cox_fit(clin, ['KRAS', 'MUC16', 'CEACAM5'], event_col='dead_dss'):
    print(f"{c:9s} {hr:6.2f} {b:6.2f} {se:5.2f} {p:7.4f}")
