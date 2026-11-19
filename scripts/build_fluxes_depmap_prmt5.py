#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit la série §8.43 : 12 gènes v4 en valeurs Chronos, ordonnés par
dépendance PRMT5 croissante (PRMT5 = axe, jamais un flux, absent du CSV).
Protocole gelé : PROTOCOL_mtap_prmt5_flux.md (19 nov. 2026).

Vérifications avant gel (lecture des en-têtes DepMap 24Q4) :
- DPCR1 et MUC2 ABSENTS de la matrice Chronos -> hors série.
- GSTM1 présent mais 8 NaN sur 45 -> exclu, sans imputation.
  (Exclure les lignées donnerait n=37 < 40, minimum fast.)
- Flux retenus (9) : PGC, REG4, CLDN18, MUC17, CR2, KRT20, CEACAM5,
  CLCA1, MUC16. Contrôle = step (1re colonne), cible = PGC (repli).
- Nul : mêmes lignes permutées, graine 42, step intact.
Aucune donnée d'une autre expérience n'entre ici.
"""
import hashlib

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
GENE_EFFECT = f"{DATA}/CRISPRGeneEffect.csv"
MODEL = f"{DATA}/Model.csv"
SEED = 42

# symbole -> colonne Chronos "SYMBOLE (Entrez)"
FLUX_COLS = {
    "PGC": "PGC (5225)",
    "REG4": "REG4 (83998)",
    "CLDN18": "CLDN18 (51208)",
    "MUC17": "MUC17 (140453)",
    "CR2": "CR2 (1380)",
    "KRT20": "KRT20 (54474)",
    "CEACAM5": "CEACAM5 (1048)",
    "CLCA1": "CLCA1 (1179)",
    "MUC16": "MUC16 (94025)",
}
PRMT5_COL = "PRMT5 (10419)"
# exclus, raisons consignees dans le protocole
ABSENTS = {"DPCR1": "aucune colonne Chronos dans DepMap 24Q4",
           "MUC2": "aucune colonne Chronos dans DepMap 24Q4"}
EXCLU_NAN = {"GSTM1": "GSTM1 (2944) : 8 NaN sur 45 lignées"}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    print(f"SHA CRISPRGeneEffect.csv : {sha(GENE_EFFECT)}")
    print(f"SHA Model.csv            : {sha(MODEL)}")
    model = pd.read_csv(MODEL, low_memory=False)
    adeno_ids = model.loc[
        model["OncotreePrimaryDisease"] == "Pancreatic Adenocarcinoma",
        "ModelID",
    ].tolist()
    print(f"Model.csv : {len(model)} modèles, {len(adeno_ids)} adénocarcinomes pancréatiques")

    ge = pd.read_csv(GENE_EFFECT, index_col=0)
    print(f"CRISPRGeneEffect.csv : {ge.shape[0]} modèles x {ge.shape[1]} gènes")
    for sym, col in FLUX_COLS.items():
        assert col in ge.columns, f"colonne flux absente : {col}"
    assert PRMT5_COL in ge.columns, "colonne PRMT5 absente"
    for sym in ABSENTS:
        assert not any(c.startswith(sym + " (") for c in ge.columns), \
            f"{sym} present contrairement a la verification pre-gel"
    assert "GSTM1 (2944)" in ge.columns

    inter = [m for m in adeno_ids if m in ge.index]
    absents_ge = sorted(set(adeno_ids) - set(ge.index))
    print(f"Intersection : {len(inter)} lignées adéno dans GeneEffect")
    print(f"Adéno absents de GeneEffect ({len(absents_ge)}) : {absents_ge}")
    assert len(inter) == 45, f"attendu 45, obtenu {len(inter)}"

    # adénosquameux (hors série, pour la note de provenance §2)
    adeno_sq = model.loc[
        model["OncotreePrimaryDisease"] == "Adenosquamous Carcinoma of the Pancreas",
        ["ModelID", "CellLineName"],
    ]
    adeno_sq_in_ge = [m for m in adeno_sq["ModelID"] if m in ge.index]
    print(f"Adénosquameux pancréas dans GeneEffect : {len(adeno_sq_in_ge)} "
          f"{adeno_sq_in_ge} (hors série, cf. §8.28/§8.29/§8.40 = 47)")

    sub = ge.loc[inter, list(FLUX_COLS.values()) + [PRMT5_COL]]
    nan_counts = sub.isna().sum()
    print("NaN par colonne retenue :")
    print(nan_counts.to_string())
    gstm1_nan = int(ge.loc[inter, "GSTM1 (2944)"].isna().sum())
    print(f"GSTM1 (2944) NaN sur les 45 : {gstm1_nan} -> exclu (voir protocole §3)")
    assert gstm1_nan == 8
    flux_nan = int(sub[list(FLUX_COLS.values())].isna().sum().sum())
    assert flux_nan == 0, f"NaN dans les flux retenus : {flux_nan}"
    assert int(sub[PRMT5_COL].isna().sum()) == 0, "NaN dans PRMT5"

    prmt5 = sub[PRMT5_COL].sort_values(ascending=True)
    assert prmt5.is_unique, "ex aequo dans PRMT5 : ordre non defini"
    order = list(prmt5.index)
    print(f"PRMT5 Chronos sur 45 lignées : min={prmt5.min():+.4f} "
          f"médiane={prmt5.median():+.4f} max={prmt5.max():+.4f}")

    flux = sub.loc[order, list(FLUX_COLS.values())].copy()
    flux.columns = list(FLUX_COLS.keys())
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    assert out.isna().sum().sum() == 0
    out_path = f"{OUT}/pdac_depmap_fluxes_prmt5.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes)")

    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_depmap_fluxes_prmt5_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} (permutation graine {SEED}, step intact)")

    # ordre des ModelID pour la provenance / les tests directs
    with open(f"{OUT}/prmt5_flux_order.txt", "w", encoding="utf-8") as f:
        for i, mid in enumerate(order):
            f.write(f"{i}\t{mid}\t{prmt5[mid]:+.6f}\n")
    print(f"SHA réel : {sha(out_path)}")
    print(f"SHA nul  : {sha(nul_path)}")
    print(f"SHA script : {sha(__file__)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
