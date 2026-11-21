#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Piste Œil §8.81 — tests directs (harnais, hors pipeline).
Protocole gelé : PROTOCOL_oeil_privilege_881.md (§3, §5).
Aucun run pipeline ici. Aucun CSV de flux modifié.

Pour chaque cohorte PDAC (TCGA, GSE71729, GSE62452, ICGC) :
  (T1) Spearman rho de chaque gène de privilège / témoin contre le rang KRAS (test PRINCIPAL).
  (T2) d de Cohen top-12 KRAS-fort contre reste (réel ; nul = mêmes indices sur le nul graine 42,
       pour les 12 gènes v4 dont le nul existe — pour les gènes de privilège, le nul est la même
       permutation de lignes : marginales identiques par construction, d marginal = 0,0000 vérifié).
  (T3) Score PRIV = moyenne des z-scores des gènes de privilège présents ; rho vs rang KRAS.
UVM : présence des gènes, médianes log2(RSEM+1), d de Cohen UVM vs TCGA-PAAD brut, score PRIV UVM.
Sorties : priv_direct_tests_881.csv, priv_direct_tests_881.json, uvm_direct_tests_881.csv.
"""
import gzip
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
SEED = 42
ATOL = 1e-9

PRIV_GENES = ["FASLG", "TGFB1", "TGFB2", "IDO1", "HLA-G", "CD47", "CD274"]
TEMOINS = ["PDCD1", "CD8A", "GZMB", "IFNG"]
V4 = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20", "MUC2",
      "GSTM1", "CEACAM5", "CLCA1", "MUC16"]
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


def cohen_d(a, b):
    """d = (moyenne(b) - moyenne(a)) / ecart-type poole. Positif = b plus haut."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    sp = np.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))
    return float((b.mean() - a.mean()) / sp) if sp > 0 else float("nan")


def zscore(v):
    v = np.asarray(v, float)
    s = v.std(ddof=0)
    return (v - v.mean()) / s if s > 0 else np.zeros_like(v)


def analyse_cohorte(nom, gene_mat, kras_values, sample_ids):
    """gene_mat : DataFrame gènes x échantillons (valeurs du §3). kras_values : Series indexée par échantillon.
    Retourne (lignes de résultats, dict infos). L'ordre est KRAS croissant."""
    order = kras_values.sort_values(ascending=True).index.tolist()
    n = len(order)
    ranks = np.arange(n, dtype=float)
    rows = []
    present_priv = [g for g in PRIV_GENES if g in gene_mat.index]
    # Score PRIV : moyenne des z-scores des gènes présents, dans l'ordre KRAS.
    if present_priv:
        zmat = np.vstack([zscore(gene_mat.loc[g, order].to_numpy(float)) for g in present_priv])
        priv = zmat.mean(axis=0)
    else:
        priv = np.zeros(n)
    rho_priv, p_priv = spearmanr(ranks, priv)
    rows.append({"cohorte": nom, "gene": "SCORE_PRIV", "present": True,
                 "n": n, "n_genes_score": len(present_priv),
                 "rho_kras": round(float(rho_priv), 4), "p_kras": float(p_priv),
                 "d_top12": round(float(cohen_d(priv[:-12], priv[-12:])), 4),
                 "median": round(float(np.median(priv)), 4)})
    for g in PRIV_GENES + TEMOINS:
        if g not in gene_mat.index:
            rows.append({"cohorte": nom, "gene": g, "present": False, "n": n,
                         "n_genes_score": len(present_priv), "rho_kras": None, "p_kras": None,
                         "d_top12": None, "median": None})
            continue
        v = gene_mat.loc[g, order].to_numpy(float)
        cc = np.isfinite(v) & np.isfinite(kras_values.loc[order].to_numpy(float))
        rho, p = spearmanr(ranks[cc], v[cc])
        d = cohen_d(v[:-12], v[-12:])
        rows.append({"cohorte": nom, "gene": g, "present": True, "n": int(cc.sum()),
                     "n_genes_score": len(present_priv),
                     "rho_kras": round(float(rho), 4), "p_kras": float(p),
                     "d_top12": round(float(d), 4),
                     "median": round(float(np.median(v)), 4)})
    infos = {"cohorte": nom, "n": n, "genes_privilege_presents": present_priv,
             "genes_privilege_absents": [g for g in PRIV_GENES if g not in gene_mat.index],
             "temoins_absents": [g for g in TEMOINS if g not in gene_mat.index],
             "kras_min": float(kras_values.min()), "kras_mediane": float(kras_values.median()),
             "kras_max": float(kras_values.max())}
    return rows, infos, priv, order


def load_tcga():
    tarball = f"{DATA}/tcga_paad_rsem.tar.gz"
    assert md5(tarball) == "b09569ce3f4721f514bc137bd109ac0a", "MD5 tarball PAAD non conforme"
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
    score_ac = logmat.loc[[g for g in ACINAR if g in logmat.index]].median(axis=0)
    score_is = logmat.loc[[g for g in ISLET if g in logmat.index]].median(axis=0)
    X = np.column_stack([np.ones(len(logmat.columns)), score_ac.values, score_is.values])
    Y = logmat.values
    beta, *_ = np.linalg.lstsq(X, Y.T, rcond=None)
    resid = Y - (X @ beta).T
    resid_df = pd.DataFrame(resid, index=logmat.index, columns=logmat.columns)
    # Vérification de reproduction v4 (arrêt si écart > atol).
    v4 = pd.read_csv(f"{OUT}/pdac_tcga_fluxes_v4.csv")
    assert sha(f"{OUT}/pdac_tcga_fluxes_v4.csv") == "e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0"
    flux_cols = list(v4.columns[1:])
    kras_res = resid_df.loc["KRAS"].sort_values(ascending=True)
    order_kras = list(kras_res.index)
    recomputed = resid_df.loc[flux_cols, order_kras].T.reset_index(drop=True)
    max_diff = float(np.abs(recomputed.values - v4[flux_cols].values).max())
    print(f"TCGA : vérification v4, écart max = {max_diff:.3e} (atol {ATOL:g})")
    assert max_diff <= ATOL, "ÉCART v4 > atol — ARRÊT"
    return resid_df, resid_df.loc["KRAS"], logmat


def load_geo71729():
    mat = pd.read_csv(f"{DATA}/GSE71729_series_matrix.txt.gz", sep="\t",
                      comment="!", index_col=0, low_memory=False)
    mat.index = mat.index.str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    mat = mat.groupby(level=0).median()
    gsm_order = list(mat.columns)
    kinds = ["?"] * len(gsm_order)
    with gzip.open(f"{DATA}/GSE71729_series_matrix.txt.gz", "rt",
                   encoding="utf-8", errors="replace") as f:
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
    prim = [g for g, k in zip(gsm_order, kinds) if k == "Primary"]
    sub = mat[prim]
    need = ["KRAS"] + [g for g in PRIV_GENES + TEMOINS if g in sub.index]
    cc = sub.loc[need].dropna(axis=1)
    print(f"GSE71729 : {len(prim)} primaires, cas complets KRAS+privilège/témoins présents : {cc.shape[1]}")
    return cc, cc.loc["KRAS"]


def load_geo62452():
    mat = pd.read_csv(f"{DATA}/GSE62452_series_matrix.txt.gz", sep="\t",
                      comment="!", index_col=0, low_memory=False)
    mat.index = mat.index.astype(str).str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    gsm_order = list(mat.columns)
    kinds = ["?"] * len(gsm_order)
    with gzip.open(f"{DATA}/GSE62452_series_matrix.txt.gz", "rt",
                   encoding="utf-8", errors="replace") as f:
        ch1 = []
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_characteristics_ch1"):
                ch1.append([v.strip('"') for v in line.rstrip("\n").split("\t")[1:]])
    for i in range(len(gsm_order)):
        vals = [row[i] for row in ch1 if i < len(row)]
        joined = " | ".join(vals)
        if "tissue: Pancreatic tumor" in joined:
            kinds[i] = "Tumor"
    tum = [g for g, k in zip(gsm_order, kinds) if k == "Tumor"]
    sub = mat[tum]
    pmap = {}
    with open(f"{DATA}/GPL6244_probe2symbol.tsv") as f:
        next(f)
        for line in f:
            p, s = line.rstrip("\n").split("\t")
            pmap[p] = s
    syms = sub.index.astype(str).map(lambda x: pmap.get(x))
    sub2 = sub.copy()
    sub2.index = syms
    sub2 = sub2[sub2.index.notna()]
    genes = sub2.groupby(level=0).median()
    need = ["KRAS"] + [g for g in PRIV_GENES + TEMOINS if g in genes.index]
    cc = genes.loc[need].dropna(axis=1)
    print(f"GSE62452 : {len(tum)} tumeurs, cas complets : {cc.shape[1]}")
    return cc, cc.loc["KRAS"]


def load_icgc():
    exp = pd.read_csv(f"{DATA}/icgc_pacaau_exp.txt.gz", sep="\t", index_col=0, compression="gzip")
    pm = pd.read_csv(f"{DATA}/icgc_pacaau_probemap.gz", sep="\t", compression="gzip")
    mapping = dict(zip(pm["#id"], pm["gene"]))
    exp.index = exp.index.map(lambda g: mapping.get(g, g))
    exp = exp.groupby(level=0).median()
    clin = pd.read_excel(f"{DATA}/bailey2016_suppl_tables1-13.xlsx",
                         sheet_name="Supp Table 1 Clinical", header=1)
    keep = clin[(clin["Sample type"] == "Primary tumour")
                & (clin["HistoSubtype"] == "Pancreatic Ductal Adenocarcinoma")]
    ids = [c for c in exp.columns if c in set(keep["icgc_id"])]
    sub = exp[ids]
    need = ["KRAS"] + [g for g in PRIV_GENES + TEMOINS if g in sub.index]
    cc = sub.loc[need].dropna(axis=1)
    print(f"ICGC : {len(ids)} tumeurs primaires PDAC, cas complets : {cc.shape[1]}")
    return cc, cc.loc["KRAS"]


def main():
    all_rows, all_infos = [], {}
    # --- TCGA : résidus (même correction que v4) ---
    resid_df, kras_res, logmat_paad = load_tcga()
    rows, infos, priv_tcga, order_tcga = analyse_cohorte("TCGA", resid_df, kras_res, list(resid_df.columns))
    all_rows += rows; all_infos["TCGA"] = infos
    print(f"TCGA : n={infos['n']} ; privilège présents {infos['genes_privilege_presents']} ; absents {infos['genes_privilege_absents']}")
    # --- GEO ---
    for nom, loader in [("GSE71729", load_geo71729), ("GSE62452", load_geo62452), ("ICGC", load_icgc)]:
        cc, kras = loader()
        rows, infos, priv, order = analyse_cohorte(nom, cc, kras, list(cc.columns))
        all_rows += rows; all_infos[nom] = infos
        print(f"{nom} : n={infos['n']} ; privilège présents {infos['genes_privilege_presents']} ; absents {infos['genes_privilege_absents']}")

    # --- Contrôle de construction du nul (correction §8.70/§8.71) : d marginal réel-vs-nul ---
    # Le nul est une permutation des lignes : chaque flux garde exactement ses valeurs.
    # Vérifié numériquement sur un gène de privilège TCGA (FASLG, résidus, graine 42).
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(order_tcga))
    for g in ["FASLG", "TGFB1", "CD274"]:
        if g in resid_df.index:
            v = resid_df.loc[g, order_tcga].to_numpy(float)
            d_marg = cohen_d(v, v[perm])
            print(f"Contrôle nul TCGA {g} : d marginal réel-vs-nul (permutation s42) = {d_marg:+.4f} (attendu 0,0000)")
            all_infos.setdefault("controle_nul_marginal", {})[g] = round(float(d_marg), 4)

    dt = pd.DataFrame(all_rows)
    dt.to_csv(f"{OUT}/priv_direct_tests_881.csv", index=False)
    with open(f"{OUT}/priv_direct_tests_881.json", "w", encoding="utf-8") as f:
        json.dump({"infos": all_infos, "lignes": all_rows}, f, indent=2, ensure_ascii=False)
    print("Écrit : priv_direct_tests_881.csv, priv_direct_tests_881.json")
    print(dt.pivot(index="gene", columns="cohorte", values="rho_kras").to_string())
    print(f"SHA script : {sha(__file__)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
