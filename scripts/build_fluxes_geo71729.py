#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flux GEO GSE71729 (Moffitt PDAC) pour la confirmation du sous-groupe v4.
Source : GEO, série GSE71729, matrice téléchargée 2026-11-15 (voir
PROVENANCE_geo71729.md). Plateforme GPL20769 = Agilent-014850 Whole Human
Genome 4x44K G4112F, version « Gene Symbol » — les ID_REF de la matrice sont
DÉJÀ des symboles de gènes (19 749 lignes) : aucune conversion sonde→gène
n'est nécessaire (vérifié : même ensemble que la table de la plateforme).
Variante (a) [prioritaire] : les 12 mêmes gènes que la v4 TCGA, ordre = KRAS
croissant, sans correction. Variante (b) : re-sélection fraîche par le
protocole v4 (régression sur scores acineux/îlots, exclusion du sexe,
top 12 par variance des résidus). Jamais d'imputation : cas complets
seulement. Nuls = lignes permutées, graine 42.
"""
import gzip
import hashlib

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
SEED = 42

V4_GENES = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
            "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]
ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]
ISLET = ["INS", "GCG", "PPY", "SST"]
EXCLUDE_SEX = {"XIST", "TSIX", "RPS4Y1", "RPS4Y2", "DDX3Y", "EIF1AY",
               "KDM5D", "USP9Y", "UTY", "ZFY", "SRY", "TSPY1", "TSPY2",
               "NLGN4Y", "TTTY2", "TTTY15", "PRKY"}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    # ---- 1. Matrice : lignes = symboles, colonnes = GSM ----
    mat = pd.read_csv(
        f"{DATA}/GSE71729_series_matrix.txt.gz", sep="\t",
        comment="!", index_col=0, low_memory=False)
    mat.index = mat.index.str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    print(f"Matrice : {mat.shape[0]} gènes x {mat.shape[1]} échantillons")
    print("Valeurs : min=%.2f médiane=%.2f max=%.2f ; NaN=%d" % (
        float(np.nanmin(mat.values)), float(np.nanmedian(mat.values)),
        float(np.nanmax(mat.values)), int(mat.isna().sum().sum())))
    # Symboles dupliqués -> médiane (règle annoncée).
    dup = mat.index.duplicated(keep=False).sum()
    if dup:
        print(f"Symboles dupliqués : {dup} lignes -> agrégation par médiane")
        mat = mat.groupby(level=0).median()
        print(f"Après agrégation : {mat.shape[0]} gènes uniques")

    # ---- 2. Annotation des échantillons (ch2, 6 lignes) ----
    gsm_order = list(mat.columns)
    kinds = ["?"] * len(gsm_order)
    with gzip.open(f"{DATA}/GSE71729_series_matrix.txt.gz", "rt",
                   encoding="utf-8", errors="replace") as f:
        ch2 = []
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_characteristics_ch2"):
                ch2.append([v.strip('"') for v in
                            line.rstrip("\n").split("\t")[1:]])
            if line.startswith("!Sample_title"):
                titles = [t.strip('"') for t in
                          line.rstrip("\n").split("\t")[1:]]
    for i in range(len(gsm_order)):
        vals = [row[i] for row in ch2 if i < len(row)]
        joined = " | ".join(vals)
        if "tissue type: Primary" in joined:
            kinds[i] = "Primary"
        elif "tissue type: Metastasis" in joined:
            kinds[i] = "Metastasis"
        elif "tissue type: Normal" in joined:
            kinds[i] = "Normal"
        elif titles[i].endswith("-CellLine"):
            kinds[i] = "CellLine"
    from collections import Counter
    print("Types d'échantillons :", dict(Counter(kinds)))
    prim = [g for g, k in zip(gsm_order, kinds) if k == "Primary"]
    print(f"Tumeurs primaires retenues : {len(prim)}")
    sub = mat[prim]

    # ---- 3. Variante (a) : les 12 gènes v4 ----
    present = [g for g in V4_GENES if g in sub.index]
    missing = [g for g in V4_GENES if g not in sub.index]
    print("Gènes v4 présents :", present)
    print("Gènes v4 absents de la puce :", missing)
    print("KRAS présent :", "KRAS" in sub.index)
    need = ["KRAS"] + present
    cc = sub.loc[need].dropna(axis=1)
    print(f"Cas complets (KRAS + {len(present)} gènes) : {cc.shape[1]} / "
          f"{len(prim)}")
    assert cc.shape[1] >= 50, "moins de 50 cas complets — arrêt"
    order = cc.loc["KRAS"].sort_values(ascending=True).index
    flux = cc.loc[present, order].T
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_geo71729_fluxes.csv"
    out.to_csv(out_path, index=False)
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_geo71729_fluxes_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes) SHA {sha(out_path)[:12]}…")
    print(f"Écrit : {nul_path} SHA {sha(nul_path)[:12]}…")
    print("KRAS (valeurs puce) : min=%.2f médiane=%.2f max=%.2f" % (
        float(cc.loc["KRAS"].min()), float(cc.loc["KRAS"].median()),
        float(cc.loc["KRAS"].max())))

    # ---- 4. Variante (b) : re-sélection protocole v4 ----
    # Scores de pureté sur les 145 primaires (médianes, gènes présents).
    ac = [g for g in ACINAR if g in sub.index]
    isl = [g for g in ISLET if g in sub.index]
    print(f"Scores pureté : acineux {len(ac)} gènes, îlots {len(isl)} gènes")
    score_ac = sub.loc[ac].median(axis=0)
    score_is = sub.loc[isl].median(axis=0)
    print("Corrélation acineux-îlots : %+.3f" % float(
        np.corrcoef(score_ac, score_is)[0, 1]))
    # Régression par gène sur [1, score_ac, score_is], sur cas complets.
    sub_cc = sub.dropna(axis=1)
    print(f"Patients sans aucune valeur manquante : {sub_cc.shape[1]}")
    X = np.column_stack([np.ones(sub_cc.shape[1]),
                         score_ac.loc[sub_cc.columns].values,
                         score_is.loc[sub_cc.columns].values])
    Y = sub_cc.values
    beta, *_ = np.linalg.lstsq(X, Y.T, rcond=None)
    resid = Y - (X @ beta).T
    resid_df = pd.DataFrame(resid, index=sub_cc.index,
                            columns=sub_cc.columns)
    var_tot = pd.Series(Y.var(axis=1), index=sub_cc.index)
    var_res = pd.Series(resid.var(axis=1), index=sub_cc.index)
    with np.errstate(invalid="ignore", divide="ignore"):
        r2 = 1.0 - var_res / var_tot
    print("Variance expliquée par pureté (médiane des gènes) : %.1f%%" % (
        100 * float(np.nanmedian(r2.values))))
    print("KRAS : R² pureté = %.1f%%" % (
        100 * float(r2.loc["KRAS"]) if "KRAS" in r2.index else float("nan")))
    var = resid_df.var(axis=1).sort_values(ascending=False)
    var = var.drop(index=["KRAS"] + sorted(EXCLUDE_SEX & set(var.index)),
                   errors="ignore")
    top = var.head(12)
    print("Top 12 par variance des résidus (hors KRAS, hors sexe) :",
          list(top.index))
    kras_res = resid_df.loc["KRAS"].sort_values(ascending=True)
    order_b = list(kras_res.index)
    flux_b = resid_df.loc[list(top.index), order_b].T
    out_b = pd.DataFrame({"step": np.arange(len(flux_b))})
    out_b = pd.concat([out_b, flux_b.reset_index(drop=True)], axis=1)
    out_b_path = f"{OUT}/pdac_geo71729_fluxes_v4b.csv"
    out_b.to_csv(out_b_path, index=False)
    perm_b = rng.permutation(len(out_b))
    nul_b = out_b.copy()
    nul_b.iloc[:, 1:] = out_b.iloc[:, 1:].to_numpy()[perm_b]
    nul_b_path = f"{OUT}/pdac_geo71729_fluxes_v4b_nul.csv"
    nul_b.to_csv(nul_b_path, index=False)
    print(f"Écrit : {out_b_path} ({out_b.shape[0]} lignes) "
          f"SHA {sha(out_b_path)[:12]}…")
    print(f"Écrit : {nul_b_path} SHA {sha(nul_b_path)[:12]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
