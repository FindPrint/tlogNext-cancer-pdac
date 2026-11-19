#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Variante v2 des flux TCGA-PAAD du jour : même protocole que
build_fluxes_tcga.py, PLUS une liste d'exclusion explicite.
Pourquoi : la sélection par variance (v1) a choisi presque uniquement des
enzymes digestives du pancréas normal (PNLIP, CTRB1/2, CELA, CPA, CPB, CLPS,
CTRC) et XIST (sexe). Dans une biopsie de tumeur, ces gènes mesurent
surtout la quantité de pancréas normal mélangée à la tumeur (pureté) et le
sexe du patient, pas le cancer lui-même. La v1 reste intacte comme témoin ;
la v2 les exclut et re-sélectionne les 12 gènes de plus forte variance
parmi les autres. La liste d'exclusion est de la biologie de manuel
(le pancréas fabrique des enzymes digestives ; XIST = chromosome X),
pas une donnée d'une autre expérience. Tout est consigné en provenance.
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

# Enzymes digestives des cellules acineuses du pancréas normal + gènes du sexe.
EXCLUDE = {
    # Acineuses / digestives
    "PNLIP", "CTRB1", "CTRB2", "CELA1", "CELA2A", "CELA3A", "CELA3B",
    "CPA1", "CPA2", "CPB1", "CPB2", "CLPS", "CTRC", "AMY2A", "AMY2B",
    "PRSS1", "PRSS2", "PRSS3", "SYCN", "CUZD1", "REG1A", "REG1B",
    "REG3A", "REG3G",
    # Sexe : XIST/TSIX (chromosome X inactif) + chromosome Y
    "XIST", "TSIX", "RPS4Y1", "RPS4Y2", "DDX3Y", "EIF1AY", "KDM5D",
    "USP9Y", "UTY", "ZFY", "SRY", "TSPY1", "TSPY2", "NLGN4Y", "TTTY2",
    "TTTY15", "PRKY",
}


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
        f = tf.extractfile(member)
        df = pd.read_csv(f, sep="\t", index_col=0, low_memory=False)
    df.index = df.index.to_series().str.split("|").str[0]
    df = df[~df.index.duplicated(keep="first")]
    cols = df.columns.to_series()
    tumor_cols = cols[cols.str[13:15] == "01"]
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    mat = mat[~mat.isna().any(axis=1)]
    logmat = np.log2(mat + 1.0)
    excluded_present = sorted(set(EXCLUDE) & set(logmat.index))
    print(f"Gènes exclus présents dans la matrice : {len(excluded_present)}")
    print(f"  {excluded_present}")
    var = logmat.var(axis=1).sort_values(ascending=False)
    var = var.drop(index=["KRAS"] + excluded_present, errors="ignore")
    top = var.head(N_FLUX)
    print("Top 12 gènes par variance (hors KRAS, hors exclus) :")
    for gene, v in top.items():
        print(f"  {gene:12s} variance={v:.3f} "
              f"médiane_log2={float(logmat.loc[gene].median()):.3f}")

    kras = logmat.loc["KRAS"].sort_values(ascending=True)
    order = list(kras.index)
    flux_cols = list(top.index)
    flux = logmat.loc[flux_cols, order].T
    assert flux.isna().sum().sum() == 0
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_tcga_fluxes_v2.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes)")

    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_tcga_fluxes_v2_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} (permutation graine {SEED})")

    provenance = {
        "date": "2026-11-15",
        "variante": "v2 (exclusions pureté/sexe)",
        "base": "même source et même protocole que pdac_tcga_fluxes.csv (v1) ; "
                "voir PROVENANCE_tcga.md",
        "exclusions": {
            "raison": "la sélection par variance (v1) a choisi presque "
                      "uniquement des enzymes digestives du pancréas normal "
                      "et XIST : ces gènes mesurent la quantité de pancréas "
                      "normal dans la biopsie (pureté) et le sexe, pas le "
                      "cancer. La v1 reste intacte comme témoin.",
            "liste": sorted(EXCLUDE),
            "présents_dans_la_matrice": excluded_present,
        },
        "sélection_gènes": {
            "méthode": "variance entre les patients, par gène, sur log2(RSEM+1) ; "
                       "top 12 hors KRAS et hors liste d'exclusion",
            "gènes": [
                {"gène": g, "variance": round(float(v), 4),
                 "médiane_log2": round(float(logmat.loc[g].median()), 4)}
                for g, v in top.items()
            ],
        },
        "ordre": "expression KRAS croissante (log2(RSEM+1)) ; KRAS = axe "
                 "d'ordonnancement, jamais un flux",
        "flux_csv": {"fichier": out_path, "sha256": sha(out_path),
                     "lignes": int(out.shape[0]), "colonnes": list(out.columns)},
        "nul_csv": {"fichier": nul_path, "sha256": sha(nul_path),
                    "méthode": "mêmes lignes permutées, graine 42"},
    }
    with open(f"{OUT}/PROVENANCE_tcga_v2.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — flux PDAC du jour (TCGA-PAAD, variante v2)\n\n")
        f.write("```json\n" + json.dumps(provenance, indent=2, ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_tcga_v2.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
