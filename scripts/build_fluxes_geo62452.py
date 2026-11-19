#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flux GEO GSE62452 (Hussain et al., PDAC, NCI) pour la confirmation du
résultat robuste : « le groupe KRAS-le-plus-fort a CA125 (MUC16) et CEA
(CEACAM5) élevés ».
Source : GEO, série GSE62452, matrice téléchargée 2026-11-15 (voir
PROVENANCE_geo62452.md). Plateforme GPL6244 = [HuGene-1_0-st] Affymetrix
Human Gene 1.0 ST Array (33 297 transcript clusters) — ATTENTION : la
tâche annonçait GPL570, la matrice dit GPL6244 ; les ID_REF sont
numériques (7892501…), mapping extrait de la table de la plateforme
GPL6244 (fichier family.soft.gz du FTP GEO, streaming arrêté après
!platform_table_end ; 33 297 lignes, 25 293 sondes avec symbole).
Variante (a) [prioritaire] : les 12 mêmes gènes que la v4 TCGA, ordre =
KRAS croissant, sans correction. Variante (b) : re-sélection fraîche par
le protocole v4 (régression sur scores acineux/îlots, exclusion du sexe,
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
    # ---- 1. Matrice : lignes = transcript clusters, colonnes = GSM ----
    mat = pd.read_csv(
        f"{DATA}/GSE62452_series_matrix.txt.gz", sep="\t",
        comment="!", index_col=0, low_memory=False)
    mat.index = mat.index.astype(str).str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    print(f"Matrice : {mat.shape[0]} sondes x {mat.shape[1]} échantillons")
    print("Valeurs : min=%.2f médiane=%.2f max=%.2f ; NaN=%d" % (
        float(np.nanmin(mat.values)), float(np.nanmedian(mat.values)),
        float(np.nanmax(mat.values)), int(mat.isna().sum().sum())))

    # ---- 2. Annotation des échantillons (characteristics_ch1) ----
    gsm_order = list(mat.columns)
    kinds = ["?"] * len(gsm_order)
    with gzip.open(f"{DATA}/GSE62452_series_matrix.txt.gz", "rt",
                   encoding="utf-8", errors="replace") as f:
        ch1 = []
        titles = []
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_characteristics_ch1"):
                ch1.append([v.strip('"') for v in
                            line.rstrip("\n").split("\t")[1:]])
            if line.startswith("!Sample_title"):
                titles = [t.strip('"') for t in
                          line.rstrip("\n").split("\t")[1:]]
    from collections import Counter
    for i in range(len(gsm_order)):
        vals = [row[i] for row in ch1 if i < len(row)]
        joined = " | ".join(vals)
        if "tissue: Pancreatic tumor" in joined:
            kinds[i] = "Tumor"
        elif "tissue: adjacent pancreatic non-tumor" in joined:
            kinds[i] = "Normal"
    print("Types d'échantillons (characteristics_ch1) :", dict(Counter(kinds)))
    # Contre-vérification par les titres : tumeur = suffixe -T* ou -Tp*/-Tc*,
    # ou titre se terminant par « T » dans le second lot ; normal = -Tn.
    title_kind = []
    for t in titles:
        if t.endswith("-Tn"):
            title_kind.append("Normal")
        elif "-Tp" in t or "-Tc" in t or t.endswith("T"):
            title_kind.append("Tumor")
        else:
            title_kind.append("?")
    agree = sum(1 for a, b in zip(kinds, title_kind) if a == b)
    print(f"Accord characteristics/titres : {agree}/{len(kinds)}")
    tum = [g for g, k in zip(gsm_order, kinds) if k == "Tumor"]
    print(f"Tumeurs primaires retenues : {len(tum)}")
    sub = mat[tum]

    # ---- 3. Sondes -> symboles (médiane par gène) ----
    pmap = {}
    with open(f"{DATA}/GPL6244_probe2symbol.tsv") as f:
        next(f)
        for line in f:
            p, s = line.rstrip("\n").split("\t")
            pmap[p] = s
    sub_idx = sub.index.astype(str)
    syms = sub_idx.map(lambda x: pmap.get(x))
    n_mapped = int(syms.notna().sum())
    print(f"Sondes mappées vers un symbole : {n_mapped} / {len(sub)}")
    sub2 = sub.copy()
    sub2.index = syms
    sub2 = sub2[sub2.index.notna()]
    dup = sub2.index.duplicated(keep=False).sum()
    print(f"Symboles dupliqués : {dup} lignes -> agrégation par médiane")
    genes = sub2.groupby(level=0).median()
    print(f"Après agrégation : {genes.shape[0]} gènes uniques")
    print("Gènes v4 présents :",
          [g for g in V4_GENES if g in genes.index])
    print("Gènes v4 absents :",
          [g for g in V4_GENES if g not in genes.index])
    print("KRAS présent :", "KRAS" in genes.index)

    # ---- 4. Variante (a) : les 12 gènes v4 ----
    present = [g for g in V4_GENES if g in genes.index]
    need = ["KRAS"] + present
    cc = genes.loc[need].dropna(axis=1)
    print(f"Cas complets (KRAS + {len(present)} gènes) : {cc.shape[1]} / "
          f"{len(tum)}")
    assert cc.shape[1] >= 50, "moins de 50 cas complets — arrêt"
    order = cc.loc["KRAS"].sort_values(ascending=True).index
    flux = cc.loc[present, order].T
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_geo62452_fluxes.csv"
    out.to_csv(out_path, index=False)
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_geo62452_fluxes_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes) SHA {sha(out_path)[:12]}…")
    print(f"Écrit : {nul_path} SHA {sha(nul_path)[:12]}…")
    print("KRAS (valeurs puce) : min=%.2f médiane=%.2f max=%.2f" % (
        float(cc.loc["KRAS"].min()), float(cc.loc["KRAS"].median()),
        float(cc.loc["KRAS"].max())))

    # ---- 5. Variante (b) : re-sélection protocole v4 ----
    ac = [g for g in ACINAR if g in genes.index]
    isl = [g for g in ISLET if g in genes.index]
    print(f"Scores pureté : acineux {len(ac)} gènes, îlots {len(isl)} gènes")
    score_ac = genes.loc[ac].median(axis=0)
    score_is = genes.loc[isl].median(axis=0)
    print("Corrélation acineux-îlots : %+.3f" % float(
        np.corrcoef(score_ac, score_is)[0, 1]))
    sub_cc = genes.dropna(axis=1)
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
    out_b_path = f"{OUT}/pdac_geo62452_fluxes_v4b.csv"
    out_b.to_csv(out_b_path, index=False)
    perm_b = rng.permutation(len(out_b))
    nul_b = out_b.copy()
    nul_b.iloc[:, 1:] = out_b.iloc[:, 1:].to_numpy()[perm_b]
    nul_b_path = f"{OUT}/pdac_geo62452_fluxes_v4b_nul.csv"
    nul_b.to_csv(nul_b_path, index=False)
    print(f"Écrit : {out_b_path} ({out_b.shape[0]} lignes) "
          f"SHA {sha(out_b_path)[:12]}…")
    print(f"Écrit : {nul_b_path} SHA {sha(nul_b_path)[:12]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
