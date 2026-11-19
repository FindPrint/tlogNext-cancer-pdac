#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-test ATR/CHEK1 — contrôles ICGC (70) et GSE62452 (69).
Protocole gelé (16 nov. 2026, avant les runs) :
- Mêmes 12 gènes de réparation que le bras PARP, mêmes tests directs que
  GEO71729 (Spearman gène vs rang KRAS ; top12 = 12 KRAS-forts, en sd ;
  recouvrement Q3, attendu 3/12). Valeurs brutes (log-expression puce /
  log2 CPM), ordre KRAS croissant, cas complets seulement, jamais
  d'imputation. Nul : lignes permutées, graine 42.
- ICGC : matrice UCSC Xena PACA-AU (log2 CPM, déjà sur disque) + mapping
  Ensembl -> symbole (probemap Xena) + filtre tumeurs primaires PDAC
  (Bailey Suppl. Table 1) — code repris de build_fluxes_icgc.py.
- GSE62452 : série-matrix GEO déjà sur disque + mapping GPL6244
  probe -> symbole (médiane par gène) + filtre « tissue: Pancreatic
  tumor » — code repris de build_fluxes_geo62452.py.
- Analyse secondaire (même question centrale, ajoutée après le re-test
  TCGA qui a montré que la prolifération tue CHEK1/RAD51/POLQ) :
  score de prolifération (médiane MKI67, TOP2A, PCNA, CCNB1) par
  patient, rho gène-prolif et Spearman partiel gène vs rang KRAS |
  score prolifération. Étiquetée « secondaire » dans les sorties.
"""
import gzip
import hashlib
from collections import Counter

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from scipy.stats import t as tdist

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
SEED = 42
GENES12 = ["PARP1", "PARP2", "BRCA1", "BRCA2", "ATM", "ATR", "CHEK1",
           "CHEK2", "RAD51", "XRCC1", "POLQ", "FANCD2"]
GENES7 = ["BRCA2", "ATR", "CHEK1", "RAD51", "POLQ", "PARP1", "PARP2"]
PROLIF = ["MKI67", "TOP2A", "PCNA", "CCNB1"]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rankdata(a):
    return pd.Series(a).rank(method="average").to_numpy(dtype=float)


def partial_spearman(x, y, z):
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    X = np.column_stack([np.ones(len(z)), rz])
    bx, *_ = np.linalg.lstsq(X, rx, rcond=None)
    by, *_ = np.linalg.lstsq(X, ry, rcond=None)
    ex, ey = rx - X @ bx, ry - X @ by
    if ex.std() == 0 or ey.std() == 0:
        return np.nan, np.nan
    r = float(np.corrcoef(ex, ey)[0, 1])
    n = len(x)
    t = r * np.sqrt((n - 3) / max(1e-12, 1 - r * r))
    return r, float(2 * tdist.sf(abs(t), n - 3))


def direct_tests(mat, order, label, rows, txt, cohort):
    """mat : DataFrame gènes x patients ; order : patients triés par KRAS."""
    n = len(order)
    rank = np.arange(n)
    top12 = np.zeros(n, dtype=bool)
    top12[-12:] = True
    txt.append(f"--- {label} — {cohort} n={n} ---")
    for gene in GENES12:
        v = mat.loc[gene, order].to_numpy(dtype=float)
        q3 = float(np.quantile(v, 0.75))
        rho, p = spearmanr(rank, v)
        ov12 = int((top12 & (v > q3)).sum())
        top12_sd = float((v[top12].mean() - v[~top12].mean()) / v.std(ddof=0))
        txt.append(f"{gene:6s}: rho {rho:+.3f} p={p:.2e} | top12 {top12_sd:+.2f} sd | "
                   f"KRAS-forts >Q3 : {ov12}/12 (attendu 3)")
        rows.append(dict(cohorte=cohort, série=label, n=n, gene=gene,
                         rho_kras=float(rho), p_rho=float(p),
                         top12_sd=top12_sd, overlap_top12_q3=ov12))
    txt.append("")
    return rows


def prolif_diag(mat, order, cohort, txt, rows):
    """Secondaire : le signal survit-il au contrôle prolifération ?"""
    n = len(order)
    score = mat.loc[PROLIF, order].median(axis=0).to_numpy(dtype=float)
    rho_p, p_p = spearmanr(np.arange(n), score)
    txt.append(f"--- Secondaire prolifération — {cohort} n={n} ---")
    txt.append(f"Score prolifération vs rang KRAS : rho {rho_p:+.3f} p={p_p:.2e}")
    for gene in GENES12:
        v = mat.loc[gene, order].to_numpy(dtype=float)
        r, p = partial_spearman(v, np.arange(n), score)
        rp, pp = spearmanr(v, score)
        txt.append(f"{gene:6s}: partiel {r:+.3f} p={p:.2e} | rho gène-prolif {rp:+.3f} p={pp:.2e}")
        rows.append(dict(cohorte=cohort, série="PARTIEL prolif", n=n, gene=gene,
                         rho_kras=float(r), p_rho=float(p), top12_sd=np.nan,
                         overlap_top12_q3=-1))
    txt.append("")
    return rows


def load_icgc():
    exp = pd.read_csv(f"{DATA}/icgc_pacaau_exp.txt.gz", sep="\t",
                      index_col=0, compression="gzip")
    pm = pd.read_csv(f"{DATA}/icgc_pacaau_probemap.gz", sep="\t",
                     compression="gzip")
    mapping = dict(zip(pm["#id"], pm["gene"]))
    exp.index = exp.index.map(lambda g: mapping.get(g, g))
    exp = exp.groupby(level=0).median()
    clin = pd.read_excel(f"{DATA}/bailey2016_suppl_tables1-13.xlsx",
                         sheet_name="Supp Table 1 Clinical", header=1)
    clin = clin[["icgc_id", "Sample type", "HistoSubtype"]]
    ids = [c for c in exp.columns if c in set(clin["icgc_id"])]
    keep = clin[(clin["icgc_id"].isin(ids))
                & (clin["Sample type"] == "Primary tumour")
                & (clin["HistoSubtype"] == "Pancreatic Ductal Adenocarcinoma")]
    print(f"ICGC : {len(keep)} tumeurs primaires PDAC retenues")
    need = ["KRAS"] + GENES12 + PROLIF
    missing = [g for g in need if g not in exp.index]
    assert not missing, f"ICGC gènes absents : {missing}"
    sub = exp.loc[need, keep["icgc_id"]].dropna(axis=1)
    print(f"ICGC cas complets : {sub.shape[1]} / {len(keep)}")
    assert sub.shape[1] >= 50
    order = sub.loc["KRAS"].sort_values(ascending=True).index.tolist()
    return sub, order


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
                ch1.append([v.strip('"') for v in
                            line.rstrip("\n").split("\t")[1:]])
    for i in range(len(gsm_order)):
        vals = [row[i] for row in ch1 if i < len(row)]
        joined = " | ".join(vals)
        if "tissue: Pancreatic tumor" in joined:
            kinds[i] = "Tumor"
        elif "tissue: adjacent pancreatic non-tumor" in joined:
            kinds[i] = "Normal"
    print("GSE62452 types :", dict(Counter(kinds)))
    tum = [g for g, k in zip(gsm_order, kinds) if k == "Tumor"]
    sub = mat[tum]
    pmap = {}
    with open(f"{DATA}/GPL6244_probe2symbol.tsv") as f:
        next(f)
        for line in f:
            p, s = line.rstrip("\n").split("\t")
            pmap[p] = s
    sub2 = sub.copy()
    sub2.index = sub.index.astype(str).map(lambda x: pmap.get(x))
    sub2 = sub2[sub2.index.notna()]
    genes = sub2.groupby(level=0).median()
    need = ["KRAS"] + GENES12 + PROLIF
    missing = [g for g in need if g not in genes.index]
    assert not missing, f"GSE62452 gènes absents : {missing}"
    cc = genes.loc[need].dropna(axis=1)
    print(f"GSE62452 cas complets : {cc.shape[1]} / {len(tum)}")
    assert cc.shape[1] >= 50
    order = cc.loc["KRAS"].sort_values(ascending=True).index.tolist()
    return cc, order


def main():
    rows, txt = [], []
    txt.append("=== Re-test ATR/CHEK1 — contrôles ICGC (70) et GSE62452 (69) ===")
    txt.append("Mêmes 12 gènes et mêmes tests directs que GEO71729 (brut, ordre KRAS).")
    txt.append("Secondaire : contrôle prolifération (score MKI67/TOP2A/PCNA/CCNB1).")
    txt.append("")
    rng = np.random.default_rng(SEED)
    for cohort, loader in [("ICGC", load_icgc), ("GSE62452", load_geo62452)]:
        mat, order = loader()
        print(f"{cohort} KRAS : min={float(mat.loc['KRAS', order].min()):.2f} "
              f"médiane={float(mat.loc['KRAS', order].median()):.2f} "
              f"max={float(mat.loc['KRAS', order].max()):.2f}")
        direct_tests(mat, order, "RÉEL", rows, txt, cohort)
        prolif_diag(mat, order, cohort, txt, rows)
        # Nul : permuter les lignes des patients (colonnes) pour les 12 gènes
        mat_nul = mat.copy()
        perm = rng.permutation(len(order))
        mat_nul.loc[GENES12] = mat.loc[GENES12].to_numpy()[:, perm]
        direct_tests(mat_nul, order, "NUL graine 42", rows, txt, cohort)

    txt.append("--- Lecture (7 gènes du protocole) ---")
    for cohort in ["ICGC", "GSE62452"]:
        for g in GENES7:
            r = [x for x in rows if x["cohorte"] == cohort and x["gene"] == g
                 and x["série"] == "RÉEL"][0]
            rp = [x for x in rows if x["cohorte"] == cohort and x["gene"] == g
                  and x["série"] == "PARTIEL prolif"][0]
            txt.append(f"{cohort} {g}: rho {r['rho_kras']:+.3f} p={r['p_rho']:.2e} "
                       f"(top12 {r['top12_sd']:+.2f}) | partiel prolif "
                       f"{rp['rho_kras']:+.3f} p={rp['p_rho']:.2e}")
    for cohort in ["ICGC", "GSE62452"]:
        n_sig = sum(1 for x in rows if x["cohorte"] == cohort
                    and x["série"] == "RÉEL" and x["gene"] in GENES7
                    and x["p_rho"] < 0.05)
        n_sig_nul = sum(1 for x in rows if x["cohorte"] == cohort
                        and x["série"] == "NUL graine 42"
                        and x["gene"] in GENES7 and x["p_rho"] < 0.05)
        txt.append(f"{cohort} : gènes (sur 7) p < 0,05 — réel {n_sig}/7 ; nul {n_sig_nul}/7. "
                   f"Seuil Bonferroni 7 tests : p < 0,0071.")

    out_csv = f"{OUT}/atr_chek1_direct_tests_cohorts.csv"
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    out_txt = f"{OUT}/atr_chek1_direct_tests_cohorts.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(txt) + "\n")
    print("\n".join(txt))
    print(f"Écrit : {out_csv} (SHA {sha(out_csv)[:12]}…) et {out_txt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
