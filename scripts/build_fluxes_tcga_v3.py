#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Variante v3 des flux TCGA-PAAD du jour : correction de pureté.
Fait mesuré (v1/v2, 15 nov. 2026) : la variance dominante des données brutes
est la composition du tissu (pancréas normal acineux + îlots), pas la tumeur.
La v3 enlève cette composante de façon standard et documentée :
- Score acineux par patient = médiane log2(RSEM+1) des 11 gènes acineux de v1
  (PNLIP, CTRB2, CELA3A, CTRB1, CPA1, CELA2A, CPB1, CELA3B, CLPS, CTRC, CPA2).
- Score îlots par patient = médiane log2(RSEM+1) de INS, GCG, PPY, SST.
- Pour chaque gène : régression linéaire de son expression sur les 2 scores
  (moindres carrés, 178 patients) ; flux = résidu (observé - prédit).
- Ordre des lignes : résidu KRAS croissant (KRAS corrigé de la pureté).
  KRAS reste l'axe, jamais un flux.
- Sélection : les 12 gènes de plus forte variance des résidus, hors KRAS.
Hypothèse : les 2 scores capturent la composante tissu normal de façon
linéaire. Les v1/v2 restent les témoins sans correction. Tout est consigné.
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

ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]
ISLET = ["INS", "GCG", "PPY", "SST"]


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

    acinar_present = [g for g in ACINAR if g in logmat.index]
    islet_present = [g for g in ISLET if g in logmat.index]
    print(f"Score acineux : {len(acinar_present)} gènes ; "
          f"score îlots : {len(islet_present)} gènes")
    score_ac = logmat.loc[acinar_present].median(axis=0)
    score_is = logmat.loc[islet_present].median(axis=0)
    print(f"Score acineux : min={score_ac.min():.2f} médiane={score_ac.median():.2f} "
          f"max={score_ac.max():.2f}")
    print(f"Score îlots : min={score_is.min():.2f} médiane={score_is.median():.2f} "
          f"max={score_is.max():.2f}")
    print(f"Corrélation acineux-îlots : {np.corrcoef(score_ac, score_is)[0, 1]:+.3f}")

    # Régression de chaque gène sur [1, score_ac, score_is] ; résidus.
    X = np.column_stack([np.ones(len(logmat.columns)), score_ac.values,
                         score_is.values])
    Y = logmat.values  # gènes x patients
    beta, *_ = np.linalg.lstsq(X, Y.T, rcond=None)  # (3, n_gènes)
    fitted = (X @ beta).T
    resid = Y - fitted
    resid_df = pd.DataFrame(resid, index=logmat.index, columns=logmat.columns)
    # Part de variance expliquée par les 2 scores (médiane sur les gènes).
    var_tot = pd.Series(Y.var(axis=1), index=logmat.index)
    var_res = pd.Series(resid.var(axis=1), index=logmat.index)
    with np.errstate(invalid="ignore", divide="ignore"):
        r2 = 1.0 - var_res / var_tot
    r2 = r2.where(var_tot > 0)  # gènes constants -> R² indéfini (NaN)
    r2_med = float(np.nanmedian(r2.values))
    print(f"Variance expliquée par pureté (médiane des gènes) : {r2_med:.1%}")
    print(f"KRAS : R² pureté = {r2.loc['KRAS']:.1%}")

    var = resid_df.var(axis=1).sort_values(ascending=False)
    var = var.drop(index=["KRAS"], errors="ignore")
    top = var.head(N_FLUX)
    print("Top 12 gènes par variance des résidus (hors KRAS) :")
    for gene, v in top.items():
        r2g = r2.loc[gene]
        print(f"  {gene:12s} variance_résidu={v:.3f} "
              f"R²_pureté={r2g:.1%}" if pd.notna(r2g) else
              f"  {gene:12s} variance_résidu={v:.3f} R²_pureté=n/a")

    kras_res = resid_df.loc["KRAS"].sort_values(ascending=True)
    order = list(kras_res.index)
    print(f"Résidu KRAS : min={kras_res.min():+.3f} "
          f"médiane={kras_res.median():+.3f} max={kras_res.max():+.3f}")

    flux_cols = list(top.index)
    flux = resid_df.loc[flux_cols, order].T
    assert flux.isna().sum().sum() == 0
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_tcga_fluxes_v3.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes)")

    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_tcga_fluxes_v3_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} (permutation graine {SEED})")

    provenance = {
        "date": "2026-11-15",
        "variante": "v3 (correction de pureté par régression)",
        "base": "même source que v1/v2 (Firehose, voir PROVENANCE_tcga.md)",
        "correction": {
            "raison": "v1/v2 mesurent que la variance dominante est la "
                      "composition du tissu (acineux + îlots). La v3 enlève "
                      "cette composante par régression linéaire, méthode "
                      "standard (comme retirer un effet de lot).",
            "score_acineux": {"gènes": acinar_present,
                              "définition": "médiane log2(RSEM+1) par patient"},
            "score_îlots": {"gènes": islet_present,
                            "définition": "médiane log2(RSEM+1) par patient"},
            "corrélation_acineux_îlots": round(float(np.corrcoef(score_ac, score_is)[0, 1]), 4),
            "variance_expliquée_médiane": round(r2_med, 4),
            "R2_pureté_KRAS": round(float(r2.loc["KRAS"]), 4),
            "méthode": "moindres carrés par gène sur [1, score_acineux, "
                       "score_îlots] ; flux = résidus",
        },
        "sélection_gènes": {
            "méthode": "variance des résidus entre les patients, par gène ; "
                       "top 12 hors KRAS",
            "gènes": [
                {"gène": g, "variance_résidu": round(float(v), 4),
                 "R2_pureté": (round(float(r2.loc[g]), 4)
                               if pd.notna(r2.loc[g]) else None)}
                for g, v in top.items()
            ],
        },
        "ordre": "résidu KRAS croissant (KRAS corrigé de la pureté) ; KRAS = "
                 "axe d'ordonnancement, jamais un flux",
        "flux_csv": {"fichier": out_path, "sha256": sha(out_path),
                     "lignes": int(out.shape[0]), "colonnes": list(out.columns)},
        "nul_csv": {"fichier": nul_path, "sha256": sha(nul_path),
                    "méthode": "mêmes lignes permutées, graine 42"},
    }
    with open(f"{OUT}/PROVENANCE_tcga_v3.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — flux PDAC du jour (TCGA-PAAD, variante v3)\n\n")
        f.write("```json\n" + json.dumps(provenance, indent=2, ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_tcga_v3.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
