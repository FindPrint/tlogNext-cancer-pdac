"""Rotations sans doublon, contrôle §8.41 (19 nov. 2026).
Miroir de build_v4r_cldn18_dedup.py (CLDN18, go de Zackary 17 nov. 17h17),
généralisé à 3 paires : IMMROT CTLA4 (plus grand écart S_sep, +1,1227),
DEPMAPROT ACO2 (plus petit écart, +0,0829, marginal sous la règle 0,07),
PARPROT PARP1 (plus petit écart PARPROT, +0,1968). CLDN18 est déjà couvert
par le run v6.1 existant results_fast_v61_v4r_cldn18_dedup (S_sep +0,6761
sans doublon contre +0,8783 avec).
Méthode identique au précédent : retirer la colonne flux en double du
contrôle (colonne k, valeurs identiques à la col. 0 vérifiées) ; contrôle,
ordre et autres flux inchangés. Nul : mêmes lignes permutées
(default_rng(42) par fichier), contrôle fixe — même méthode que
build_v4r_cldn18_dedup.py. Aucune valeur recalculée ni imputée.
Sorties : *_dedup.csv et *_dedup_nul.csv ; SHA-256 affichés.
"""
import hashlib
import numpy as np
import pandas as pd

PAIRS = [
    ("pdac_immune_tcga_fluxes_immrot_CTLA4.csv",
     "pdac_immune_tcga_fluxes_immrot_CTLA4_dedup.csv"),
    ("pdac_depmap_fluxes_depmaprot_ACO2.csv",
     "pdac_depmap_fluxes_depmaprot_ACO2_dedup.csv"),
    ("pdac_parp_tcga_fluxes_parprot_PARP1.csv",
     "pdac_parp_tcga_fluxes_parprot_PARP1_dedup.csv"),
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


for src, dst in PAIRS:
    raw = pd.read_csv(src, header=None, skiprows=1)
    hdr = open(src).readline().strip().split(",")
    ctrl = hdr[0]
    dup = [i for i in range(1, len(hdr)) if hdr[i] == ctrl]
    assert len(dup) == 1, f"{src}: doublons de {ctrl} en {dup}, attendu 1"
    k = dup[0]
    assert np.allclose(raw[0].values, raw[k].values), f"{src}: col {k} != col 0"
    keep = [i for i in range(len(hdr)) if i != k]
    out = raw[keep]
    out.columns = [hdr[i] for i in keep]
    assert list(out.columns).count(ctrl) == 1 and out.shape == (len(raw), len(hdr) - 1)
    out.to_csv(dst, index=False)
    nul_dst = dst.replace("_dedup.csv", "_dedup_nul.csv")
    rng = np.random.default_rng(42)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul.to_csv(nul_dst, index=False)
    print(f"{src} controle={ctrl} doublon_col={k} n={len(out)} "
          f"colonnes {len(hdr)}->{len(keep)}")
    for p in (src, dst, nul_dst):
        print(f"  {p} {sha(p)}")
