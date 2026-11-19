#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rotations de contrôle systématiques avec v6.1 (16 nov. 2026).

Direction de Zackary : rotation de la colonne de contrôle — chaque flux
comme contrôle à tour de rôle. Règle permanente : un seul contrôle n'est
jamais un objectif ; ne jamais exiger de consensus entre flux/contrôles ;
plusieurs seuils critiques peuvent se succéder en chaîne causale.

Construction reprise EXACTEMENT de build_rotations.py (15 nov. 2026) :
- le contrôle est la 1re colonne du CSV ;
- lignes triées par le flux-contrôle croissant ;
- le flux-contrôle reste présent comme colonne de flux (le pipeline
  l'exclut par nom quand il est le contrôle) ;
- nul : mêmes lignes permutées (graine 42), colonne de contrôle intacte ;
- un générateur rng(42) par jeu de base, tirages séquentiels dans l'ordre
  des flux (même convention que le 15 nov.).

Jeux :
  TCGA v4    : pdac_tcga_fluxes_v4.csv      (178 patients, 12 flux)
  DepMap     : pdac_depmap_fluxes.csv       (45 lignées, 12 gènes)
  Immun TCGA : pdac_immune_tcga_fluxes.csv  (178 patients, 12 gènes)
  PARP TCGA  : pdac_tcga_fluxes_parp.csv    (178 patients, 12 gènes)
Sorties : pdac_<jeu>_rot_<FLUX>.csv et _nul.csv, avec PROVENANCE.
"""
import hashlib
import json

import numpy as np
import pandas as pd

OUT = "/home/hatch/workspace/runs/pdac-v6"
SEED = 42

SETS = [
    ("tcga_v4", "pdac_tcga_fluxes_v4.csv", "v4rot"),
    ("depmap", "pdac_depmap_fluxes.csv", "depmaprot"),
    ("immune_tcga", "pdac_immune_tcga_fluxes.csv", "immrot"),
    ("parp_tcga", "pdac_tcga_fluxes_parp.csv", "parprot"),
]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    prov = {}
    for set_name, fname, prefix in SETS:
        base = pd.read_csv(f"{OUT}/{fname}")
        flux_cols = list(base.columns[1:])
        rng = np.random.default_rng(SEED)
        prov[set_name] = {"base": fname, "sha256_base": sha(f"{OUT}/{fname}"),
                          "lignes": int(base.shape[0]), "flux": flux_cols,
                          "rotations": {}}
        for flux in flux_cols:
            order = base[flux].sort_values(ascending=True).index
            sorted_df = base.loc[order].reset_index(drop=True)
            out = pd.DataFrame({flux: sorted_df[flux].values})
            out = pd.concat([out, sorted_df[flux_cols].reset_index(drop=True)], axis=1)
            tag = f"{prefix}_{flux}"
            path = f"{OUT}/pdac_{set_name}_fluxes_{tag}.csv"
            out.to_csv(path, index=False)
            perm = rng.permutation(len(out))
            nul = out.copy()
            nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
            nul_path = f"{OUT}/pdac_{set_name}_fluxes_{tag}_nul.csv"
            nul.to_csv(nul_path, index=False)
            prov[set_name]["rotations"][flux] = {
                "fichier": path, "sha256": sha(path),
                "nul": nul_path, "sha256_nul": sha(nul_path)}
            print(f"Écrit : {tag} ({out.shape[0]} lignes, contrôle {flux})")
    with open(f"{OUT}/PROVENANCE_rotations_v61.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — rotations de contrôle systématiques v6.1 (16 nov. 2026)\n\n")
        f.write("Construction : `build_rotations_v61.py`, même méthode que "
                "`build_rotations.py` (15 nov. 2026). Contrôle = 1re colonne, "
                "lignes triées par le flux-contrôle croissant, nul = lignes "
                "permutées (graine 42, un générateur par jeu, tirages "
                "séquentiels dans l'ordre des flux), colonne de contrôle intacte.\n\n")
        f.write("```json\n" + json.dumps(
            {"date": "2026-11-16", "graine_nul": 42,
             "regle_lecture": "lire l'ordre de réaction des estimateurs, le "
             "test de bruit et les F1/F2 avant/après seuil ; jamais de consensus "
             "exigé ; plusieurs seuils critiques peuvent se succéder en chaîne "
             "causale ; un flux qui seuille avant un autre n'est pas faux.",
             "jeux": prov}, indent=2, ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_rotations_v61.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
