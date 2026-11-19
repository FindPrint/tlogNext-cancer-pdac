#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit les flux du jour depuis TCGA-PAAD (Firehose, RSEM normalisé).
Protocole gelé (15 nov. 2026) :
- Source : Broad GDAC Firehose stddata 2016-01-28, PAAD,
  rnaseqv2 RSEM genes normalized (tarball vérifié MD5 b09569ce...).
  Téléchargement frais aujourd'hui, pas de réutilisation du fichier local tlog28.
- Lignées : échantillons tumoraux primaires uniquement (code TCGA 01).
- Valeurs : log2(RSEM normalisé + 1).
- Sélection des flux PAR LES DONNÉES DU JOUR : les 12 gènes de plus forte
  variance entre les patients, hors KRAS. La variance ne dépend pas de
  l'ordre des lignes : la sélection n'est PAS circulaire avec l'axe.
- Ordre des lignes : expression KRAS croissante (la plus faible d'abord).
  KRAS est l'axe d'ordonnancement, JAMAIS un flux.
- Flux : log2(RSEM+1) des 12 gènes sélectionnés. step = 0..N-1.
- Nul : mêmes lignes permutées, graine 42.
Aucune donnée d'une autre expérience n'entre ici.
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
TARBALL = f"{DATA}/tcga_paad_rsem.tar.gz"
TARBALL_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
N_FLUX = 12
SEED = 42


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    assert md5(TARBALL) == TARBALL_MD5, "MD5 du tarball non conforme"
    with tarfile.open(TARBALL, "r:gz") as tf:
        member = [m for m in tf.getmembers() if m.name.endswith(".data.txt")][0]
        print("Fichier matrice :", member.name, f"({member.size} octets)")
        f = tf.extractfile(member)
        df = pd.read_csv(f, sep="\t", index_col=0)
    print(f"Matrice : {df.shape[0]} gènes x {df.shape[1]} échantillons")
    # Première colonne = symbole|entrez (format Firehose).
    symbols = df.index.to_series().str.split("|").str[0]
    df.index = symbols
    df = df[~df.index.duplicated(keep="first")]
    # Échantillons tumoraux primaires : code 01 (positions 14-15 du barcode).
    cols = df.columns.to_series()
    sample_type = cols.str[13:15]
    tumor_cols = cols[sample_type == "01"]
    other = cols[sample_type != "01"]
    print(f"Échantillons tumoraux primaires (01) : {len(tumor_cols)} ; "
          f"autres ({sorted(set(other.str[13:15]))}) : {len(other)}")
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    assert "KRAS" in mat.index, "KRAS absent de la matrice"
    # Règle : aucun NaN dans les flux (jamais de valeur inventée).
    nan_genes = mat.isna().any(axis=1)
    print(f"Gènes avec NaN sur les tumeurs : {int(nan_genes.sum())} (écartés)")
    mat = mat[~nan_genes]
    logmat = np.log2(mat + 1.0)
    var = logmat.var(axis=1).sort_values(ascending=False)
    var = var.drop(index=["KRAS"], errors="ignore")
    top = var.head(N_FLUX)
    print("Top 12 gènes par variance (hors KRAS) :")
    for gene, v in top.items():
        print(f"  {gene:12s} variance={v:.3f} "
              f"médiane_log2={float(logmat.loc[gene].median()):.3f}")

    kras = logmat.loc["KRAS"].sort_values(ascending=True)
    order = list(kras.index)
    print(f"KRAS log2(RSEM+1) sur tumeurs : min={kras.min():.3f} "
          f"médiane={kras.median():.3f} max={kras.max():.3f}")

    flux_cols = list(top.index)
    flux = logmat.loc[flux_cols, order].T
    assert flux.isna().sum().sum() == 0
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_tcga_fluxes.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes)")

    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_tcga_fluxes_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} (permutation graine {SEED})")

    provenance = {
        "date": "2026-11-15",
        "source": {
            "dépôt": "Broad GDAC Firehose stddata 2016-01-28, PAAD",
            "fichier": "gdac.broadinstitute.org_PAAD.Merge_rnaseqv2__illuminahiseq_"
                       "rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data."
                       "Level_3.2016012800.0.0.tar.gz",
            "url": "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/"
                   "data/PAAD/20160128/",
            "taille_octets": 15296232,
            "md5_vérifié": TARBALL_MD5,
            "matrice_interne": member.name,
            "matrice": f"{df.shape[0]} gènes x {df.shape[1]} échantillons",
            "données": "RNA-seq V2 RSEM normalisé (TCGA, UNC Illumina HiSeq)",
        },
        "patients": {
            "critère": "échantillons tumoraux primaires, code TCGA 01",
            "retenus": int(len(tumor_cols)),
            "écartés": int(len(other)),
            "transformation": "log2(RSEM normalisé + 1)",
        },
        "sélection_gènes": {
            "méthode": "variance entre les patients, par gène, sur log2(RSEM+1) ; "
                       "top 12 hors KRAS (la variance ne dépend pas de l'ordre "
                       "des lignes)",
            "gènes": [
                {"gène": g, "variance": round(float(v), 4),
                 "médiane_log2": round(float(logmat.loc[g].median()), 4)}
                for g, v in top.items()
            ],
            "gènes_écartés_NaN": int(nan_genes.sum()),
        },
        "ordre": "expression KRAS croissante (log2(RSEM+1), la plus faible "
                 "d'abord) ; KRAS = axe d'ordonnancement, jamais un flux",
        "KRAS_log2": {"min": round(float(kras.min()), 4),
                      "médiane": round(float(kras.median()), 4),
                      "max": round(float(kras.max()), 4)},
        "flux_csv": {"fichier": out_path, "sha256": sha(out_path),
                     "lignes": int(out.shape[0]), "colonnes": list(out.columns)},
        "nul_csv": {"fichier": nul_path, "sha256": sha(nul_path),
                    "méthode": "mêmes lignes permutées, graine 42"},
        "règle": "Données du jour uniquement (téléchargement frais depuis "
                 "Firehose). Aucune donnée ni conclusion d'une autre "
                 "expérience importée (règle 15 nov. 2026).",
    }
    with open(f"{OUT}/PROVENANCE_tcga.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — flux PDAC du jour (TCGA-PAAD, Firehose)\n\n")
        f.write("```json\n" + json.dumps(provenance, indent=2, ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_tcga.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
