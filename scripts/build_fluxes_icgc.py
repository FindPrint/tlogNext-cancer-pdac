#!/usr/bin/env python3
"""Construit les flux ICGC PACA-AU (variante a) pour le pipeline v6.
Protocole gelé (mission 16 nov. 2026) :
- Source expression : UCSC Xena, cohorte PACA-AU (Bailey et al. 2016, Nature),
  fichier nature16965-s2_normalised_exp.txt, log2(cpm), 96 échantillons.
  Miroir de l'ICGC DCC (portail dcc.icgc.org hors service : l'API renvoie
  index.html ; données retrouvées via la table XenaData d'UCSCXenaTools).
- Mapping gènes : probe map Xena PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp
  (Ensembl -> symbole) ; médiane par symbole en cas de duplicata.
- Clinique : Bailey et al. 2016, Supplementary Table 1 (MOESM270), jointe sur icgc_id.
- Retenus : tumeurs primaires PDAC uniquement (Sample type == 'Primary tumour'
  ET HistoSubtype == 'Pancreatic Ductal Adenocarcinoma').
- Flux : les 12 MÊMES gènes que la v4 TCGA, ordre KRAS croissant, sans imputation.
- Nul : lignes permutées, graine 42.
- Sorties : pdac_icgc_fluxes.csv, pdac_icgc_fluxes_nul.csv,
  icgc_clinical_70.csv (jointure clinique pour la survie).
"""
import hashlib
import numpy as np
import pandas as pd

GENES12 = ['PGC', 'REG4', 'CLDN18', 'MUC17', 'DPCR1', 'CR2',
           'KRT20', 'MUC2', 'GSTM1', 'CEACAM5', 'CLCA1', 'MUC16']
KRAS = 'KRAS'

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

# --- expression (log2 CPM) ---
exp = pd.read_csv('data/icgc_pacaau_exp.txt.gz', sep='\t', index_col=0, compression='gzip')
print(f"expression brute : {exp.shape[0]} gènes x {exp.shape[1]} échantillons")

# --- mapping Ensembl -> symbole ---
pm = pd.read_csv('data/icgc_pacaau_probemap.gz', sep='\t', compression='gzip')
mapping = dict(zip(pm['#id'], pm['gene']))
exp.index = exp.index.map(lambda g: mapping.get(g, g))
# médiane par symbole en cas de duplicata
exp = exp.groupby(level=0).median()
print(f"après mapping : {exp.shape[0]} symboles uniques x {exp.shape[1]} échantillons")

missing = [g for g in GENES12 + [KRAS] if g not in exp.index]
assert not missing, f"gènes absents : {missing}"
print("les 13 gènes (12 flux + KRAS) présents, mappage unique")

# --- clinique (Bailey Suppl. Table 1) ---
clin = pd.read_excel('data/bailey2016_suppl_tables1-13.xlsx',
                     sheet_name='Supp Table 1 Clinical', header=1)
clin = clin[['icgc_id', 'Sample type', 'HistoSubtype', 'Status',
             'Length of Follow Up (months)', 'Gender', 'Age at Diagnosis in Years']]
clin = clin.rename(columns={'Length of Follow Up (months)': 'followup_months'})
print(f"clinique : {len(clin)} patients")

# --- jointure + filtre tumeurs primaires PDAC ---
ids = [c for c in exp.columns if c in set(clin['icgc_id'])]
print(f"échantillons expression présents dans la clinique : {len(ids)}")
keep = clin[(clin['icgc_id'].isin(ids))
            & (clin['Sample type'] == 'Primary tumour')
            & (clin['HistoSubtype'] == 'Pancreatic Ductal Adenocarcinoma')]
print(f"tumeurs primaires PDAC retenues : {len(keep)}")
assert len(keep) >= 50, "moins de 50 patients complets"
assert keep['followup_months'].notna().all(), "suivi manquant"

# --- ordre KRAS croissant ---
kras = exp.loc[KRAS, keep['icgc_id']]
order = kras.sort_values(ascending=True).index.tolist()
mat = exp.loc[GENES12, order].T
mat.insert(0, 'step', range(len(mat)))
mat.to_csv('pdac_icgc_fluxes.csv', index=False)
print("pdac_icgc_fluxes.csv :", mat.shape, "SHA", sha('pdac_icgc_fluxes.csv')[:16], "...")

# --- nul : lignes permutées, graine 42 ---
rng = np.random.default_rng(42)
nul = mat.copy()
cols = list(mat.columns[1:])
nul[cols] = mat[cols].values[rng.permutation(len(mat))]
nul.to_csv('pdac_icgc_fluxes_nul.csv', index=False)
print("pdac_icgc_fluxes_nul.csv : SHA", sha('pdac_icgc_fluxes_nul.csv')[:16], "...")

# --- clinique des retenus, dans l'ordre KRAS (pour la survie) ---
clin70 = keep.set_index('icgc_id').loc[order].reset_index()
clin70['kras_rank'] = range(len(clin70))
clin70.to_csv('icgc_clinical_70.csv', index=False)
print("icgc_clinical_70.csv :", clin70.shape)
print("Status :", clin70['Status'].value_counts().to_dict())
print("KRAS log2cpm : min %.2f médiane %.2f max %.2f" % (kras.min(), kras.median(), kras.max()))
