#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit les flux du jour depuis DepMap 24Q4 (données du 15 nov. 2026).
Protocole gelé (go de Zackary, 15 nov. 2026) :
- Lignées : adénocarcinomes pancréatiques (OncotreePrimaryDisease ==
  'Pancreatic Adenocarcinoma') présents dans Model.csv ET CRISPRGeneEffect.csv.
- Sélection des gènes PAR LES DONNÉES DU JOUR : pour chaque gène, médiane
  Chronos dans les lignées pancréas vs médiane dans toutes les autres lignées ;
  sélectivité = médiane_pancréas - médiane_autres (plus négatif = plus
  essentiel en pancréas). Top 12 hors KRAS.
- Ordre des lignes : effet Chronos KRAS croissant (plus dépendant d'abord).
  KRAS est l'axe d'ordonnancement, JAMAIS un flux.
- Flux : effets Chronos des 12 gènes sélectionnés. step = 0..N-1.
- Nul : mêmes lignes permutées, graine 42 (marginales préservées, ordre détruit).
Aucune donnée d'une autre expérience n'entre ici.
"""
import hashlib
import json

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
GENE_EFFECT = f"{DATA}/CRISPRGeneEffect.csv"
MODEL = f"{DATA}/Model.csv"
N_FLUX = 12
KRAS_COL = "KRAS (3845)"
SEED = 42


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    model = pd.read_csv(MODEL, low_memory=False)
    panc_ids = model.loc[
        model["OncotreePrimaryDisease"] == "Pancreatic Adenocarcinoma",
        "ModelID",
    ].tolist()
    print(f"Model.csv : {len(model)} modèles, {len(panc_ids)} adénocarcinomes pancréatiques")

    ge = pd.read_csv(GENE_EFFECT, index_col=0)
    print(f"CRISPRGeneEffect.csv : {ge.shape[0]} modèles x {ge.shape[1]} gènes")
    assert KRAS_COL in ge.columns, "colonne KRAS absente"

    panc_in_ge = [m for m in panc_ids if m in ge.index]
    other_ids = [m for m in ge.index if m not in set(panc_ids)]
    print(f"Intersection : {len(panc_in_ge)} lignées pancréas dans GeneEffect, "
          f"{len(other_ids)} autres lignées")
    assert len(panc_in_ge) >= 10, "trop peu de lignées pancréas"

    panc = ge.loc[panc_in_ge]
    others = ge.loc[other_ids]
    med_panc = panc.median(axis=0)
    med_other = others.median(axis=0)
    selectivity = med_panc - med_other
    ranking = selectivity.sort_values(ascending=True)
    ranking = ranking.drop(index=[KRAS_COL], errors="ignore")
    # Règle : aucun NaN dans les flux (jamais de valeur inventée). On descend
    # le classement jusqu'à 12 gènes sans aucun NaN sur les lignées pancréas.
    nan_counts = panc.isna().sum(axis=0)
    eligible = [g for g in ranking.index if nan_counts.get(g, 0) == 0]
    skipped = [g for g in ranking.index[:30] if g not in eligible[:N_FLUX]]
    top = ranking.loc[eligible[:N_FLUX]]
    print(f"Gènes écartés pour NaN (top 30) : {skipped}")
    assert len(top) == N_FLUX
    kras_nan = int(panc[KRAS_COL].isna().sum())
    assert kras_nan == 0, f"KRAS a {kras_nan} NaN sur les lignées pancréas"
    print("Top 12 gènes sélectifs (hors KRAS) :")
    for gene, sel in top.items():
        print(f"  {gene:20s} sélectivité={sel:+.3f} "
              f"médiane_panc={med_panc[gene]:+.3f} médiane_autres={med_other[gene]:+.3f}")

    # Ordre des lignes : effet KRAS croissant (plus dépendant d'abord).
    kras = panc[KRAS_COL].sort_values(ascending=True)
    order = list(kras.index)
    print(f"KRAS Chronos sur lignées pancréas : min={kras.min():+.3f} "
          f"médiane={kras.median():+.3f} max={kras.max():+.3f}")

    def symbol(col):
        return col.split(" (")[0]

    flux_cols = list(top.index)
    flux = panc.loc[order, flux_cols].copy()
    flux.columns = [symbol(c) for c in flux_cols]
    assert flux.isna().sum().sum() == 0, "NaN dans les flux"
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_depmap_fluxes.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes)")

    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_depmap_fluxes_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} (permutation graine {SEED})")

    provenance = {
        "date": "2026-11-15",
        "sources": {
            "CRISPRGeneEffect.csv": {
                "depot": "DepMap Public 24Q4, figshare article 27993248, "
                         "DOI 10.25452/figshare.plus.27993248.v1",
                "fichier": "https://ndownloader.figshare.com/files/51064667",
                "taille_octets": 428678699,
                "sha256": sha(GENE_EFFECT),
            },
            "Model.csv": {
                "depot": "DepMap Public 24Q4, figshare article 27993248",
                "fichier": "https://ndownloader.figshare.com/files/51065297",
                "taille_octets": 645696,
                "sha256": sha(MODEL),
            },
        },
        "lignées": {
            "critère": "OncotreePrimaryDisease == 'Pancreatic Adenocarcinoma'",
            "dans Model.csv": len(panc_ids),
            "dans GeneEffect.csv": len(panc_in_ge),
            "exclues": "adénosquameux (2), neuroendocrine (1), non cancéreuse (1)",
            "ordre": "effet Chronos KRAS croissant (plus dépendant d'abord)",
        },
        "sélection_gènes": {
            "méthode": "médiane Chronos pancréas moins médiane Chronos autres "
                       "lignées, par gène ; top 12 hors KRAS",
            "gènes": [
                {"gène": symbol(c), "colonne": c,
                 "sélectivité": round(float(top[c]), 4),
                 "médiane_pancréas": round(float(med_panc[c]), 4),
                 "médiane_autres": round(float(med_other[c]), 4)}
                for c in flux_cols
            ],
            "KRAS_Chronos_pancréas": {
                "min": round(float(kras.min()), 4),
                "médiane": round(float(kras.median()), 4),
                "max": round(float(kras.max()), 4),
            },
        },
        "flux_csv": {"fichier": out_path, "sha256": sha(out_path),
                     "lignes": int(out.shape[0]), "colonnes": list(out.columns)},
        "nul_csv": {"fichier": nul_path, "sha256": sha(nul_path),
                    "méthode": "mêmes lignes permutées, graine 42"},
        "règle": "Données du jour uniquement (DepMap 24Q4). Aucune donnée ni "
                 "conclusion d'une autre expérience importée (règle 15 nov. 2026).",
    }
    with open(f"{OUT}/PROVENANCE_depmap.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — flux PDAC du jour (DepMap 24Q4)\n\n")
        f.write("```json\n" + json.dumps(provenance, indent=2, ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_depmap.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
