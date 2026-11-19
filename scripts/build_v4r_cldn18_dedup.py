"""Rotation CLDN18 sans doublon (17 nov. 2026, go de Zackary 17h17).
Source : pdac_tcga_fluxes_v4r_cldn18.csv (build_rotations.py). Défaut : CLDN18 y est
à la fois la colonne de contrôle (col. 0) et un des 12 flux (col. 3), corrélation 1,000.
Correction : retirer le flux CLDN18 en double (col. 3) ; contrôle, ordre et 11 autres
flux inchangés. Nul : mêmes lignes permutées (graine 42), contrôle fixe — même
méthode que build_rotations.py. Aucune valeur recalculée ni imputée."""
import hashlib, numpy as np, pandas as pd
SRC="pdac_tcga_fluxes_v4r_cldn18.csv"
raw=pd.read_csv(SRC, header=None, skiprows=1)
hdr=open(SRC).readline().strip().split(",")
assert hdr[0]=="CLDN18" and hdr[3]=="CLDN18" and hdr.count("CLDN18")==2
assert np.allclose(raw[0].values, raw[3].values)
keep=[i for i in range(len(hdr)) if i!=3]
out=raw[keep]; out.columns=[hdr[i] for i in keep]
assert list(out.columns).count("CLDN18")==1 and out.shape==(178,12)
out.to_csv("pdac_tcga_fluxes_v4r_cldn18_dedup.csv", index=False)
rng=np.random.default_rng(42); perm=rng.permutation(len(out))
nul=out.copy(); nul.iloc[:,1:]=out.iloc[:,1:].to_numpy()[perm]
nul.to_csv("pdac_tcga_fluxes_v4r_cldn18_dedup_nul.csv", index=False)
for p in [SRC,"pdac_tcga_fluxes_v4r_cldn18_dedup.csv","pdac_tcga_fluxes_v4r_cldn18_dedup_nul.csv"]:
    print(p, hashlib.sha256(open(p,"rb").read()).hexdigest())
