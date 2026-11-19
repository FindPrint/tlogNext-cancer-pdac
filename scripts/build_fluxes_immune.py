#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flux immunitaires PDAC le long de l'axe KRAS — Bras 1, protocole gelé 16 nov. 2026.
But : le paysage immunitaire change-t-il le long de l'axe KRAS ?
- Cohortes : TCGA PAAD (178 tumeurs), GSE71729 (145 tumeurs primaires),
  GSE62452 (69 tumeurs), ICGC PACA-AU (70 tumeurs primaires PDAC).
- Ordre : expression KRAS BRUTE croissante, même axe partout. Différence
  documentée avec la v4 TCGA : la v4 ordonnait par le RESIDU KRAS corrigé
  de la pureté ; ici KRAS brut, pour être comparable aux cohortes GEO/ICGC
  (aucune correction de pureté nulle part dans ce bras).
- Flux : 12 gènes immunitaires — CD8A, CD8B, CD4, FOXP3, CD68, CD163,
  CD274 (PD-L1), PDCD1 (PD-1), CTLA4, GZMB, IFNG, CD19. Aucune imputation ;
  cas complets seulement ; règle >= 50 valeurs valides par gène.
- Remplacements documentés (ICGC seulement) : IFNG absent -> PRF1 (règle du
  protocole : remplaçant nommé, effecteur cytotoxique voisin de IFNG/GZMB).
  CD19 absent AUSSI -> MS4A1 (CD20), marqueur B comme CD19. Écart documenté :
  le protocole ne nommait qu'un seul remplaçant (PRF1) ; deux absences
  exigent un second remplaçant. Dupliquer PRF1 aurait créé deux colonnes
  identiques — méthodologiquement pire. MS4A1 = voisin fonctionnel direct
  de CD19 (lignée B), même logique de substitution.
- Format CSV : identique aux CSV existants (ex. pdac_tcga_fluxes_v4.csv) :
  colonne 'step' 0..n-1, puis les 12 flux, lignes ordonnées par KRAS
  croissant, index=False, virgule.
- Nul : mêmes lignes permutées, graine 42 (rng frais par fichier).
- Fichier d'axe joint : immune_kras_order_<cohorte>.csv (step, échantillon,
  valeur KRAS brute) — KRAS n'est pas un flux, il n'apparaît pas dans le CSV
  de flux ; ce fichier rend les tests directs reproductibles.
- Sources : mêmes fichiers matrice que les bras précédents, hachages
  vérifiés avant construction (asserts dans le code).
"""
import gzip
import hashlib
import tarfile
from collections import Counter

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
SEED = 42

IMMUNE = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
          "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
# Remplacements ICGC : gène absent -> remplaçant (voir docstring).
REPLACE_ICGC = {"IFNG": "PRF1", "CD19": "MS4A1"}


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


def write_pair(tag, flux_df, kras_series, sample_ids):
    """Écrit CSV de flux + nul + fichier d'axe ; retourne les SHA."""
    out = pd.DataFrame({"step": np.arange(len(flux_df))})
    out = pd.concat([out, flux_df.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_immune_{tag}_fluxes.csv"
    out.to_csv(out_path, index=False)
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_immune_{tag}_fluxes_nul.csv"
    nul.to_csv(nul_path, index=False)
    axis = pd.DataFrame({"step": np.arange(len(flux_df)),
                         "sample": list(sample_ids),
                         "kras_raw": np.asarray(kras_series, dtype=float)})
    axis_path = f"{OUT}/immune_kras_order_{tag}.csv"
    axis.to_csv(axis_path, index=False)
    print(f"[{tag}] {out_path} : {out.shape[0]} lignes x {out.shape[1]} col, "
          f"SHA {sha(out_path)}")
    print(f"[{tag}] {nul_path} : SHA {sha(nul_path)}")
    print(f"[{tag}] {axis_path} : SHA {sha(axis_path)}")
    print(f"[{tag}] KRAS brut : min={float(kras_series.min()):.3f} "
          f"médiane={float(kras_series.median()):.3f} "
          f"max={float(kras_series.max()):.3f}")
    return {"flux": sha(out_path), "nul": sha(nul_path),
            "axis": sha(axis_path), "n": int(out.shape[0])}


def build_from_genes(tag, genes, genes_label):
    """Construction générique à partir d'un DataFrame gènes x échantillons
    (déjà filtré aux tumeurs) et d'un mapping gène->remplaçant éventuel."""
    repl = {}
    flux_genes = []
    for g in IMMUNE:
        if g in genes.index:
            flux_genes.append(g)
        elif tag == "icgc" and g in REPLACE_ICGC:
            r = REPLACE_ICGC[g]
            assert r in genes.index, f"remplaçant {r} absent ({tag})"
            repl[g] = r
            flux_genes.append(r)
            print(f"[{tag}] {g} absent -> remplacé par {r}")
        else:
            raise SystemExit(f"[{tag}] gène {g} absent et aucun remplaçant")
    need = ["KRAS"] + flux_genes
    cc = genes.loc[need].dropna(axis=1)
    print(f"[{tag}] cas complets (KRAS + {len(flux_genes)} flux) : "
          f"{cc.shape[1]} / {genes.shape[1]} échantillons")
    assert cc.shape[1] >= 50, f"[{tag}] moins de 50 cas complets"
    for g in flux_genes:
        n_valid = int(cc.loc[g].notna().sum())
        assert n_valid >= 50, f"[{tag}] {g} : {n_valid} valeurs valides < 50"
    order = cc.loc["KRAS"].sort_values(ascending=True).index
    flux = cc.loc[flux_genes, order].T
    assert flux.isna().sum().sum() == 0
    info = write_pair(tag, flux, cc.loc["KRAS", order], order)
    info["flux_genes"] = flux_genes
    info["remplacements"] = repl
    info["source_label"] = genes_label
    return info


def build_tcga():
    tarball = f"{DATA}/tcga_paad_rsem.tar.gz"
    assert md5(tarball) == "b09569ce3f4721f514bc137bd109ac0a", "MD5 TCGA non conforme"
    with tarfile.open(tarball, "r:gz") as tf:
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
    print(f"[tcga] {logmat.shape[0]} gènes x {logmat.shape[1]} tumeurs, "
          "valeurs log2(RSEM+1), KRAS BRUT (pas de correction pureté)")
    return build_from_genes("tcga", logmat, "Firehose PAAD log2(RSEM+1)")


def build_geo71729():
    path = f"{DATA}/GSE71729_series_matrix.txt.gz"
    assert sha(path) == ("b228789314ec4d866ec51b65724664abaa24b822577c55d3727820c867536a54"), \
        "SHA GSE71729 non conforme"
    mat = pd.read_csv(path, sep="\t", comment="!", index_col=0, low_memory=False)
    mat.index = mat.index.str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    dup = mat.index.duplicated(keep=False).sum()
    if dup:
        print(f"[geo71729] symboles dupliqués : {dup} lignes -> médiane")
        mat = mat.groupby(level=0).median()
    gsm_order = list(mat.columns)
    kinds = ["?"] * len(gsm_order)
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
        ch2 = []
        titles = []
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_characteristics_ch2"):
                ch2.append([v.strip('"') for v in line.rstrip("\n").split("\t")[1:]])
            if line.startswith("!Sample_title"):
                titles = [t.strip('"') for t in line.rstrip("\n").split("\t")[1:]]
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
    print("[geo71729] types :", dict(Counter(kinds)))
    prim = [g for g, k in zip(gsm_order, kinds) if k == "Primary"]
    print(f"[geo71729] tumeurs primaires : {len(prim)}")
    return build_from_genes("geo71729", mat[prim], "GEO GSE71729 GPL20769")


def build_geo62452():
    path = f"{DATA}/GSE62452_series_matrix.txt.gz"
    assert sha(path) == ("8f41d5b3f11451e653fd6bfc0c6b216c219d46711a7676d1e453dee16a078cba"), \
        "SHA GSE62452 non conforme"
    mat = pd.read_csv(path, sep="\t", comment="!", index_col=0, low_memory=False)
    mat.index = mat.index.astype(str).str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    gsm_order = list(mat.columns)
    kinds = ["?"] * len(gsm_order)
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
        ch1 = []
        titles = []
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_characteristics_ch1"):
                ch1.append([v.strip('"') for v in line.rstrip("\n").split("\t")[1:]])
            if line.startswith("!Sample_title"):
                titles = [t.strip('"') for t in line.rstrip("\n").split("\t")[1:]]
    for i in range(len(gsm_order)):
        vals = [row[i] for row in ch1 if i < len(row)]
        joined = " | ".join(vals)
        if "tissue: Pancreatic tumor" in joined:
            kinds[i] = "Tumor"
        elif "tissue: adjacent pancreatic non-tumor" in joined:
            kinds[i] = "Normal"
    print("[geo62452] types :", dict(Counter(kinds)))
    tum = [g for g, k in zip(gsm_order, kinds) if k == "Tumor"]
    print(f"[geo62452] tumeurs : {len(tum)}")
    sub = mat[tum]
    pmap = {}
    with open(f"{DATA}/GPL6244_probe2symbol.tsv") as f:
        next(f)
        for line in f:
            p, s = line.rstrip("\n").split("\t")
            pmap[p] = s
    sub_idx = sub.index.astype(str)
    syms = sub_idx.map(lambda x: pmap.get(x))
    print(f"[geo62452] sondes mappées : {int(syms.notna().sum())} / {len(sub)}")
    sub2 = sub.copy()
    sub2.index = syms
    sub2 = sub2[sub2.index.notna()]
    genes = sub2.groupby(level=0).median()
    print(f"[geo62452] après agrégation : {genes.shape[0]} gènes uniques")
    return build_from_genes("geo62452", genes, "GEO GSE62452 GPL6244")


def build_icgc():
    exp_path = f"{DATA}/icgc_pacaau_exp.txt.gz"
    assert sha(exp_path) == ("c2cb57af3ba4c3d7fdac292e66c81067d36e16aae9efdd8005147e20820f49fa"), \
        "SHA ICGC Xena non conforme"
    exp = pd.read_csv(exp_path, sep="\t", index_col=0, compression="gzip")
    pm = pd.read_csv(f"{DATA}/icgc_pacaau_probemap.gz", sep="\t", compression="gzip")
    mapping = dict(zip(pm["#id"], pm["gene"]))
    exp.index = exp.index.map(lambda g: mapping.get(g, g))
    exp = exp.groupby(level=0).median()
    print(f"[icgc] après mapping : {exp.shape[0]} symboles x {exp.shape[1]} échantillons")
    clin = pd.read_excel(f"{DATA}/bailey2016_suppl_tables1-13.xlsx",
                         sheet_name="Supp Table 1 Clinical", header=1)
    clin = clin[["icgc_id", "Sample type", "HistoSubtype"]]
    ids = [c for c in exp.columns if c in set(clin["icgc_id"])]
    keep = clin[(clin["icgc_id"].isin(ids))
                & (clin["Sample type"] == "Primary tumour")
                & (clin["HistoSubtype"] == "Pancreatic Ductal Adenocarcinoma")]
    print(f"[icgc] tumeurs primaires PDAC retenues : {len(keep)}")
    assert len(keep) >= 50
    return build_from_genes("icgc", exp[keep["icgc_id"]],
                            "UCSC Xena PACA-AU log2(cpm), Bailey 2016")


def main():
    import json
    results = {}
    for fn in (build_tcga, build_geo71729, build_geo62452, build_icgc):
        tag = fn.__name__.replace("build_", "")
        results[tag] = fn()
    with open(f"{OUT}/immune_build_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Résumé écrit : immune_build_summary.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
