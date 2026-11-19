#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bras 2 — flux réparation de l'ADN / PARP le long de l'axe KRAS (TCGA-PAAD).
Protocole gelé (16 nov. 2026, avant les runs) :
- Source : Broad GDAC Firehose stddata 2016-01-28, PAAD, rnaseqv2 RSEM genes
  normalized — tarball déjà sur disque, MD5 vérifié b09569ce3f4721f514bc137bd109ac0a.
  Rien re-téléchargé.
- Patients : échantillons tumoraux primaires uniquement (code TCGA 01) : 178.
- Valeurs : log2(RSEM normalisé + 1), BRUTES (sans correction de pureté).
  Différence explicite avec la v4 : la v4 utilisait des résidus après
  régression acineux/îlots et un ordre KRAS résiduel. Ici le protocole gelé
  de ce bras impose le brut : valeurs brutes, ordre KRAS BRUT croissant.
  Le choix est documenté, pas caché ; la v4 reste intacte comme témoin.
- Flux : 12 gènes de réparation FIXÉS par le protocole (pas sélectionnés
  par variance) : PARP1, PARP2, BRCA1, BRCA2, ATM, ATR, CHEK1, CHEK2,
  RAD51, XRCC1, POLQ, FANCD2. Tous présents, 178/178 valeurs valides
  chacun (vérifié avant construction) : aucun remplacement, aucune
  imputation. Règle >= 50 valeurs valides par gène : satisfaite partout.
- Ordre des lignes : expression KRAS BRUTE croissante (la plus faible
  d'abord). KRAS = axe d'ordonnancement, JAMAIS un flux.
- Format CSV : identique aux CSV existants (v1) : colonne `step` = 0..177,
  puis les 12 colonnes de flux, virgule, index=False.
- Nul : mêmes lignes permutées, graine 42, même construction que les
  nuls existants (permutation conjointe des lignes, corrélations
  intra-ligne conservées, ordre vs step brisé).
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
SEED = 42
GENES = ["PARP1", "PARP2", "BRCA1", "BRCA2", "ATM", "ATR", "CHEK1", "CHEK2",
         "RAD51", "XRCC1", "POLQ", "FANCD2"]


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
        df = pd.read_csv(f, sep="\t", index_col=0, low_memory=False)
    print(f"Matrice : {df.shape[0]} gènes x {df.shape[1]} échantillons")
    df.index = df.index.to_series().str.split("|").str[0]
    df = df[~df.index.duplicated(keep="first")]
    cols = df.columns.to_series()
    tumor_cols = cols[cols.str[13:15] == "01"]
    other = cols[cols.str[13:15] != "01"]
    print(f"Tumeurs primaires (01) : {len(tumor_cols)} ; autres : {len(other)}")
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    assert "KRAS" in mat.index, "KRAS absent de la matrice"
    missing = [g for g in GENES if g not in mat.index]
    assert not missing, f"Gènes absents : {missing} (remplacement requis)"
    logmat = np.log2(mat + 1.0)
    for g in GENES + ["KRAS"]:
        n_valid = int(logmat.loc[g].notna().sum())
        print(f"  {g:6s} n_valides={n_valid}/178 "
              f"médiane_log2={float(logmat.loc[g].median()):.3f} "
              f"variance={float(logmat.loc[g].var(ddof=1)):.3f}")
        assert n_valid >= 50, f"{g} : moins de 50 valeurs valides"
    assert logmat.loc[GENES].isna().sum().sum() == 0, "NaN dans les flux"

    kras = logmat.loc["KRAS"].sort_values(ascending=True)
    order = list(kras.index)
    print(f"KRAS brut log2(RSEM+1) : min={kras.min():.3f} "
          f"médiane={kras.median():.3f} max={kras.max():.3f}")

    flux = logmat.loc[GENES, order].T
    assert flux.isna().sum().sum() == 0
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_tcga_fluxes_parp.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes)")

    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_tcga_fluxes_parp_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} (permutation graine {SEED})")

    provenance = {
        "date": "2026-11-16",
        "bras": "Bras 2 — paysage réparation de l'ADN / PARP le long de l'axe KRAS",
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
            "téléchargement": "aucun — fichier déjà sur disque, MD5 vérifié",
        },
        "patients": {
            "critère": "échantillons tumoraux primaires, code TCGA 01",
            "retenus": int(len(tumor_cols)),
            "écartés": int(len(other)),
            "transformation": "log2(RSEM normalisé + 1), valeurs BRUTES",
        },
        "gènes_flux": {
            "méthode": "liste FIXÉE par le protocole gelé (pas de sélection "
                       "par variance)",
            "gènes": [
                {"gène": g, "n_valides": 178,
                 "médiane_log2": round(float(logmat.loc[g].median()), 4),
                 "variance": round(float(logmat.loc[g].var(ddof=1)), 4)}
                for g in GENES
            ],
            "absents": [],
            "remplacements": "aucun — les 12 gènes sont présents, 178/178 "
                             "valeurs valides chacun ; aucune imputation",
        },
        "ordre": "expression KRAS BRUTE croissante (log2(RSEM+1), la plus "
                 "faible d'abord) ; KRAS = axe d'ordonnancement, jamais un flux",
        "KRAS_log2_brut": {"min": round(float(kras.min()), 4),
                           "médiane": round(float(kras.median()), 4),
                           "max": round(float(kras.max()), 4)},
        "différence_v4": "v4 = résidus après régression pureté (acineux/îlots) "
                         "+ ordre KRAS résiduel. Ici = valeurs brutes + ordre "
                         "KRAS brut, selon le protocole gelé de ce bras. "
                         "La v4 reste intacte comme témoin.",
        "flux_csv": {"fichier": out_path, "sha256": sha(out_path),
                     "lignes": int(out.shape[0]), "colonnes": list(out.columns)},
        "nul_csv": {"fichier": nul_path, "sha256": sha(nul_path),
                    "méthode": "mêmes lignes permutées, graine 42"},
    }
    with open(f"{OUT}/PROVENANCE_parp_v6.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — Bras 2 : paysage réparation / PARP (TCGA-PAAD, v6)\n\n")
        f.write("```json\n" + json.dumps(provenance, indent=2, ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_parp_v6.md (complétée après les runs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
