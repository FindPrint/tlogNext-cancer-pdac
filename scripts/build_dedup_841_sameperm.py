"""Nuls dédoublonnés à permutation identique, contrôle §8.41 (19 nov. 2026).
Complément de build_dedup_841.py : les nuls dédoublonnés de ce dernier
utilisaient un nouveau tirage (default_rng(42) par fichier), comme le
précédent CLDN18 — la comparaison dédoublonnée changeait donc DEUX choses
à la fois côté nul (retrait du doublon + nouvelle permutation). Sur n=45,
le nul varie d'une permutation à l'autre : l'inversion d'ACO2 (−0,1939)
mélange les deux effets.
Ici : on part du CSV _nul.csv ORIGINAL (même permutation que la rotation
avec doublon) et on retire seulement la colonne doublon — la permutation
est inchangée, seul le doublon disparaît. Appliqué aux deux paires où le
verdict est proche : ACO2 (inversée) et PARP1 (écart +0,0168, sous le
plancher 0,07). CTLA4 (+0,8986) et CLDN18 (+0,6761) sont robustes dans
les deux cas et n'ont pas besoin de ce contrôle.
Sorties : *_dedup_nul_sameperm.csv ; SHA-256 affichés.
"""
import hashlib
import numpy as np
import pandas as pd

PAIRS = [
    # (nul original, doublon_colonne, sortie)
    ("pdac_depmap_fluxes_depmaprot_ACO2_nul.csv", 12,
     "pdac_depmap_fluxes_depmaprot_ACO2_dedup_nul_sameperm.csv"),
    ("pdac_parp_tcga_fluxes_parprot_PARP1_nul.csv", 1,
     "pdac_parp_tcga_fluxes_parprot_PARP1_dedup_nul_sameperm.csv"),
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


for src, k, dst in PAIRS:
    raw = pd.read_csv(src, header=None, skiprows=1)
    hdr = open(src).readline().strip().split(",")
    ctrl = hdr[0]
    assert hdr[k] == ctrl, f"{src}: col {k} = {hdr[k]}, attendu {ctrl}"
    assert hdr.count(ctrl) == 2, f"{src}: {ctrl} x{hdr.count(ctrl)}"
    # Dans le nul, le contrôle est intact mais les flux sont permutés :
    # la colonne doublon n'est PAS égale ligne à ligne à la col. 0,
    # elle en est une permutation — on vérifie le multi-ensemble.
    assert np.allclose(np.sort(raw[0].values), np.sort(raw[k].values)), \
        f"{src}: col {k} n'est pas une permutation de col 0"
    keep = [i for i in range(len(hdr)) if i != k]
    out = raw[keep]
    out.columns = [hdr[i] for i in keep]
    assert list(out.columns).count(ctrl) == 1 and out.shape == (len(raw), len(hdr) - 1)
    # Vérification : les 11 colonnes restantes sont identiques au nul original, ligne par ligne.
    for j, i in enumerate(keep):
        assert np.allclose(out.iloc[:, j].values, raw[i].values), f"{src}: col {i} modifiée"
    out.to_csv(dst, index=False)
    print(f"{src} controle={ctrl} doublon_col={k} n={len(out)} colonnes {len(hdr)}->{len(keep)}")
    for p in (src, dst):
        print(f"  {p} {sha(p)}")
