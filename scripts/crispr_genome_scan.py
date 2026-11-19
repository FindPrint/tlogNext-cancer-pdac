#!/usr/bin/env python3
"""
Balayage CRISPR génome entier — vulnérabilités des lignées pancréas KRAS-dépendantes.
Protocole gelé (16 nov. 2026) :
  - Données : DepMap Public 24Q4, CRISPRGeneEffect.csv + Model.csv (déjà sur disque).
  - Lignées : pancréas présentes dans GeneEffect (47 attendues).
  - Axe : Chronos KRAS (négatif = essentiel ; bas = lignée dépendante de KRAS).
  - Pour chaque gène : Spearman(Chronos gène, Chronos KRAS) sur les lignées pancréas.
    rho POSITIF = gène plus essentiel quand la lignée dépend de KRAS (létal synthétique).
  - BH-FDR sur les gènes testés. Significatif = FDR < 0,05.
  - Nul : Chronos KRAS permuté (graine 42), même balayage.
  - Jamais d'imputation : corrélations sur paires complètes ; gènes avec n < 30 exclus du FDR.
"""
import hashlib, time
import numpy as np
import pandas as pd
from scipy.stats import t as tdist, spearmanr

T0 = time.time()
LOG = open('crispr_genome_scan.log', 'w')
def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True); LOG.write(s + '\n'); LOG.flush()

GE = 'data/CRISPRGeneEffect.csv'
MO = 'data/Model.csv'
SEED = 42
MIN_N = 30

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

log('=== Balayage CRISPR génome entier — DepMap 24Q4, lignées pancréas ===')
log('SHA CRISPRGeneEffect.csv :', sha(GE))
log('SHA Model.csv :', sha(MO))

# --- lignées pancréas (Model.csv) ---
model = pd.read_csv(MO)
panc_ids = model.loc[model['OncotreeLineage'] == 'Pancreas', 'ModelID'].tolist()
log('lignées pancréas dans Model.csv :', len(panc_ids))

# --- lecture par blocs (fichier 428 Mo, RAM limitée) : seules les lignes pancréas ---
header = pd.read_csv(GE, nrows=0)
gene_cols = list(header.columns[1:])
log('colonnes gènes dans GeneEffect :', len(gene_cols))
chunks = []
dtypes = {c: 'float32' for c in gene_cols}
for ch in pd.read_csv(GE, index_col=0, chunksize=200, dtype=dtypes):
    keep = ch.index.intersection(panc_ids)
    if len(keep):
        chunks.append(ch.loc[keep])
X = pd.concat(chunks).astype('float64')
log('lignées pancréas dans GeneEffect :', X.shape[0], '| gènes :', X.shape[1])
log('lignées manquantes (Model.csv mais pas GeneEffect) :',
    len(set(panc_ids) - set(X.index)))
# symboles et Entrez
symbols = [c.split(' (')[0] for c in X.columns]
entrez = [c.split('(')[-1].rstrip(')') for c in X.columns]

kras_col = [c for c in X.columns if c.startswith('KRAS (')][0]
kras = X[kras_col]
log('colonne KRAS :', kras_col, '| NaN :', int(kras.isna().sum()),
    '| min %.3f médiane %.3f max %.3f' % (kras.min(), kras.median(), kras.max()))

def scan(kras_vec, label):
    """Spearman par gène contre kras_vec + p + BH-FDR. Retourne DataFrame."""
    rho = X.corrwith(kras_vec, method='spearman')
    n = (X.notna().values & kras_vec.notna().values[:, None]).sum(axis=0)
    r = rho.values.astype(float)
    nn = n.astype(float)
    with np.errstate(divide='ignore', invalid='ignore'):
        tstat = r * np.sqrt((nn - 2) / (1 - r ** 2))
    p = 2 * tdist.sf(np.abs(tstat), nn - 2)
    p = np.where(np.abs(r) >= 1.0, 0.0, p)
    p = np.where(nn < MIN_N, np.nan, p)
    m = int((~np.isnan(p)).sum())
    fdr = np.full(len(p), np.nan)
    idx = np.where(~np.isnan(p))[0]
    order = idx[np.argsort(p[idx])]
    ps = p[order]
    fs = ps * m / (np.arange(m) + 1)
    fs = np.minimum.accumulate(fs[::-1])[::-1]
    fdr[order] = np.clip(fs, 0, 1)
    out = pd.DataFrame({'gene': symbols, 'entrez': entrez, 'n': n,
                        'rho': r, 'p': p, 'fdr': fdr})
    log(f'[{label}] gènes testés (n>={MIN_N}) : {m} | exclus (n<{MIN_N}) : {len(p) - m}'
        f' | FDR<0,05 : {int((fdr < 0.05).sum())}'
        f' | FDR<0,01 : {int((fdr < 0.01).sum())}')
    return out

# --- balayage réel ---
res = scan(kras, 'réel')
# --- contrôle de cohérence : scipy direct sur les 10 gènes v4 ---
v4_expected = {'CLDN18': 0.045, 'MUC16': -0.117, 'CEACAM5': -0.131, 'PGC': -0.122,
               'KRT20': 0.061, 'CLCA1': 0.232, 'CR2': 0.217, 'REG4': -0.036,
               'MUC17': 0.005, 'GSTM1': 0.129}
log('--- contrôle de cohérence (gènes v4, 15 nov.) ---')
for g, exp in v4_expected.items():
    if g in symbols:
        j = symbols.index(g)
        ok = (X.iloc[:, j].notna() & kras.notna()).values
        r_scipy, _ = spearmanr(X.iloc[ok, j], kras.values[ok])
        r_mine = float(res.loc[j, 'rho'])
        log(f'  {g:8s} attendu {exp:+.3f} | corrwith {r_mine:+.3f} | scipy {r_scipy:+.3f}'
            f' | écart {abs(r_mine - r_scipy):.2e}')
    else:
        log(f'  {g:8s} ABSENT de la bibliothèque')
# contrôle positif KRAS lui-même
j_kras = symbols.index('KRAS')
log('contrôle positif KRAS (lui-même) : rho =', round(float(res.loc[j_kras, 'rho']), 4))

# --- nul : KRAS permuté (graine 42) ---
rng = np.random.default_rng(SEED)
kras_null = pd.Series(rng.permutation(kras.values), index=kras.index)
res_null = scan(kras_null, 'nul (KRAS permuté, graine 42)')

# --- tertiles de dépendance KRAS (fort = Chronos le plus bas = le plus dépendant) ---
tert = pd.qcut(kras, 3, labels=['fort', 'moyen', 'faible'])
log('tertiels KRAS : fort (Chronos min) n =', int((tert == 'fort').sum()),
    '| moyen n =', int((tert == 'moyen').sum()),
    '| faible n =', int((tert == 'faible').sum()))
hits = res[res['fdr'] < 0.05].copy()
for col_name, lab in [('fort', 'fort'), ('moyen', 'moyen'), ('faible', 'faible')]:
    res['mean_' + col_name] = np.nan
    if len(hits):
        for j in hits.index:
            ok = X.iloc[:, j].notna().values
            res.loc[j, 'mean_' + col_name] = X.iloc[ok, j][tert.values[ok] == lab].mean()

res = res.sort_values('fdr').reset_index(drop=True)
res.to_csv('data/crispr_genome_scan.csv', index=False)
log('CSV écrit : data/crispr_genome_scan.csv | lignes :', len(res))
log('durée : %.1f s' % (time.time() - T0))

# --- candidats connus de la littérature ---
known = ['TBK1', 'PLK1', 'BCL2L1', 'MAPK1', 'MAPK3', 'RAF1', 'MTOR', 'PIK3CA',
         'CDK4', 'CDK6', 'AURKA', 'STK33', 'MYC', 'KRAS']
log('--- candidats connus ---')
for g in known:
    if g in symbols:
        row = res[res['gene'] == g].iloc[0]
        log(f'  {g:8s} rho {row["rho"]:+.3f} p {row["p"]:.4g} FDR {row["fdr"]:.4g} n {int(row["n"])}')
    else:
        log(f'  {g:8s} ABSENT de la bibliothèque')
# --- top 30 chaque direction ---
log('--- TOP 30 rho positifs (létal synthétique potentiel) ---')
for _, row in res.sort_values('rho', ascending=False).head(30).iterrows():
    log(f'  {row["gene"]:10s} rho {row["rho"]:+.3f} p {row["p"]:.3g} FDR {row["fdr"]:.3g} n {int(row["n"])}')
log('--- TOP 30 rho négatifs ---')
for _, row in res.sort_values('rho').head(30).iterrows():
    log(f'  {row["gene"]:10s} rho {row["rho"]:+.3f} p {row["p"]:.3g} FDR {row["fdr"]:.3g} n {int(row["n"])}')
log('--- HITS FDR < 0,05 ---')
hits_final = res[res['fdr'] < 0.05]
if len(hits_final):
    for _, row in hits_final.iterrows():
        log(f'  {row["gene"]:10s} rho {row["rho"]:+.3f} p {row["p"]:.3g} FDR {row["fdr"]:.4g}'
            f' | Chronos moyen fort {row["mean_fort"]:+.2f} / moyen {row["mean_moyen"]:+.2f}'
            f' / faible {row["mean_faible"]:+.2f}')
else:
    log('  AUCUN hit FDR < 0,05')
log('=== FIN, exit 0 ===')
LOG.close()
