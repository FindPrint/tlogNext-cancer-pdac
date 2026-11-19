#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit les flux protéiques CPTAC PDAC (UMich, PDC000393) analogues à la
v4 ARN, pour le pipeline v6.
Protocole gelé (15 nov. 2026) — mission CPTAC :
- Entrée : data/cptac/pdac_umich_protein_gene_matrix.csv (68 tumeurs, matrice
  au niveau gène, médiane des isoformes, ratios log vs référence — voir
  build_matrix_umich.py et PROVENANCE_cptac.md).
- Flux retenus = les 12 gènes v4 ARN, restreints à ceux qui sont mesurés avec
  au moins 50 valeurs valides sur 68 tumeurs (même règle que DepMap : jamais
  d'imputation ; un gène trop incomplet est exclu et listé) :
  PGC, REG4, CLDN18, KRT20, CEACAM5, CLCA1, MUC16 (7 flux, ordre v4 conservé).
  Exclus : DPCR1 (symbole ambigu, 5 ID Ensembl candidats, aucune correspondance
  univoque vérifiée — Ensembl REST inaccessible au moment de la vérification),
  CR2 (44/68), MUC17 (11/68), GSTM1 (20/68), MUC2 (30/68).
- Cas complets : les 5 tumeurs sans MUC16 sont retirées (rangs KRAS 13, 20, 38,
  58, 61 sur 68 — réparties, pas concentrées en haut ; médiane KRAS 0,16 contre
  0,09 pour les autres — pas de biais d'ordonnancement). Reste 63 tumeurs,
  zéro valeur manquante. 63 >= 50 (minimum v6).
- Ordre des lignes = KRAS protéique croissant (KRAS = axe, jamais un flux).
- Nul = mêmes lignes permutées, graine 42.
- Sorties : pdac_cptac_fluxes.csv + pdac_cptac_fluxes_nul.csv, SHA-256 notés.
Aucune donnée d'une autre expérience n'entre ici.
"""
import hashlib

import numpy as np
import pandas as pd

BASE = "/home/hatch/workspace/runs/pdac-v6"
MAT = f"{BASE}/data/cptac/pdac_umich_protein_gene_matrix.csv"
OUT = f"{BASE}/pdac_cptac_fluxes.csv"
OUT_NUL = f"{BASE}/pdac_cptac_fluxes_nul.csv"
FLUXES = ["PGC", "REG4", "CLDN18", "KRT20", "CEACAM5", "CLCA1", "MUC16"]
SEED = 42


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    mat = pd.read_csv(MAT, index_col=0)
    print("matrice :", mat.shape, "| patients :", mat.shape[0])
    cols = ["KRAS"] + FLUXES
    sub = mat[cols].dropna()
    print("cas complets (KRAS + 7 flux) :", len(sub), "tumeurs")
    print("KRAS protéique : min %.2f médiane %.2f max %.2f" % (
        sub["KRAS"].min(), sub["KRAS"].median(), sub["KRAS"].max()))
    sub = sub.sort_values("KRAS").reset_index(drop=True)
    fluxes = sub[FLUXES].copy()
    fluxes.insert(0, "step", np.arange(len(fluxes)))
    fluxes.to_csv(OUT, index=False)
    rng = np.random.default_rng(SEED)
    nul = fluxes.copy()
    nul.iloc[:, 1:] = nul.iloc[:, 1:].values[rng.permutation(len(nul))]
    nul.to_csv(OUT_NUL, index=False)
    print("écrit :", OUT, "SHA", sha(OUT))
    print("écrit :", OUT_NUL, "SHA", sha(OUT_NUL))
    print("colonnes :", list(fluxes.columns))
    print("première ligne (KRAS le plus faible) :")
    print(fluxes.head(1).to_string(index=False))
    print("dernière ligne (KRAS le plus fort) :")
    print(fluxes.tail(1).to_string(index=False))


if __name__ == "__main__":
    main()
