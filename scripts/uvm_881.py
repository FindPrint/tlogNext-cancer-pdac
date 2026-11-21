#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Piste Œil §8.81 — TCGA-UVM (mélanome uvéal) : tests directs + série ordonnée par PRIV.
Protocole gelé : PROTOCOL_oeil_privilege_881.md (§5).
Source : Broad GDAC Firehose stddata 2016-01-28, UVM, RSEM genes normalized,
téléchargée le 21 nov. 2026 (voir PROVENANCE_881.md). Même échelle que TCGA-PAAD brut : log2(RSEM+1).
- (U1) Niveaux médians par gène, UVM vs TCGA-PAAD brut : d de Cohen entre cohortes.
- (U2) Série UVM ordonnée par score PRIV (z intra-UVM, gènes présents), 12 flux v4, réel + nul graine 42,
  SI n >= 40.
- (U3) d top-12 PRIV vs reste pour les 12 gènes v4 dans UVM (chaîne du §8.11 sous l'ordre PRIV).
Sorties : uvm_direct_tests_881.csv, pdac_uvm_fluxes_priv.csv (+ nul), uvm_881.json.
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
UVM_TARBALL = f"{DATA}/tcga_uvm_rsem.tar.gz"
PAAD_TARBALL = f"{DATA}/tcga_paad_rsem.tar.gz"
PAAD_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
SEED = 42

PRIV_GENES = ["FASLG", "TGFB1", "TGFB2", "IDO1", "HLA-G", "CD47", "CD274"]
TEMOINS = ["PDCD1", "CD8A", "GZMB", "IFNG"]
V4 = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20", "MUC2",
      "GSTM1", "CEACAM5", "CLCA1", "MUC16"]


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
    a = np.asarray(a, float); b = np.asarray(b, float)
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    sp = np.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))
    return float((b.mean() - a.mean()) / sp) if sp > 0 else float("nan")


def load_rsem_log2(tarball, label):
    with tarfile.open(tarball, "r:gz") as tf:
        member = [m for m in tf.getmembers() if m.name.endswith(".data.txt")][0]
        print(f"{label} : membre {member.name} ({member.size} o)")
        f = tf.extractfile(member)
        df = pd.read_csv(f, sep="\t", index_col=0, low_memory=False)
    df.index = df.index.to_series().str.split("|").str[0]
    df = df[~df.index.duplicated(keep="first")]
    cols = df.columns.to_series()
    tumor_cols = cols[cols.str[13:15] == "01"]
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    mat = mat[~mat.isna().any(axis=1)]
    logmat = np.log2(mat + 1.0)
    print(f"{label} : {logmat.shape[0]} gènes x {logmat.shape[1]} tumeurs primaires (code 01)")
    return logmat


def main():
    assert md5(PAAD_TARBALL) == PAAD_MD5, "MD5 tarball PAAD non conforme"
    uvm_sha = sha(UVM_TARBALL)
    print(f"SHA-256 tarball UVM : {uvm_sha}")
    log_uvm = load_rsem_log2(UVM_TARBALL, "UVM")
    log_paad = load_rsem_log2(PAAD_TARBALL, "PAAD brut")
    n_uvm = log_uvm.shape[1]
    assert n_uvm >= 40, f"UVM n={n_uvm} < 40 — ARRÊT (protocole §5)"

    present_priv = [g for g in PRIV_GENES if g in log_uvm.index]
    absent_priv = [g for g in PRIV_GENES if g not in log_uvm.index]
    present_v4 = [g for g in V4 if g in log_uvm.index]
    absent_v4 = [g for g in V4 if g not in log_uvm.index]
    absent_tem = [g for g in TEMOINS if g not in log_uvm.index]
    print(f"UVM privilège présents : {present_priv} ; absents : {absent_priv}")
    print(f"UVM v4 présents : {present_v4} ; absents : {absent_v4}")
    print(f"UVM témoins absents : {absent_tem}")

    # (U1) Niveaux médians UVM vs PAAD brut, par gène.
    rows = []
    for g in PRIV_GENES + TEMOINS + V4:
        if g not in log_uvm.index or g not in log_paad.index:
            rows.append({"gene": g, "present_uvm": g in log_uvm.index, "present_paad": g in log_paad.index,
                         "mediane_uvm": None, "mediane_paad": None, "d_uvm_vs_paad": None})
            continue
        vu = log_uvm.loc[g].to_numpy(float)
        vp = log_paad.loc[g].to_numpy(float)
        rows.append({"gene": g, "present_uvm": True, "present_paad": True,
                     "mediane_uvm": round(float(np.median(vu)), 3),
                     "mediane_paad": round(float(np.median(vp)), 3),
                     "d_uvm_vs_paad": round(float(cohen_d(vp, vu)), 3)})
    dt = pd.DataFrame(rows)
    dt.to_csv(f"{OUT}/uvm_direct_tests_881.csv", index=False)
    print(dt.to_string())

    # Score PRIV UVM (z intra-UVM, gènes présents).
    zmat = np.vstack([(log_uvm.loc[g].to_numpy(float) - log_uvm.loc[g].mean()) / log_uvm.loc[g].std(ddof=0)
                      for g in present_priv])
    priv = pd.Series(zmat.mean(axis=0), index=log_uvm.columns)
    order_priv = priv.sort_values(ascending=True).index.tolist()
    print(f"PRIV UVM : min={priv.min():+.3f} médiane={priv.median():+.3f} max={priv.max():+.3f} ({len(present_priv)} gènes)")

    # (U2) Série UVM ordonnée par PRIV, 12 flux v4 présents.
    flux = log_uvm.loc[present_v4, order_priv].T
    out = pd.DataFrame({"PRIV": priv.loc[order_priv].to_numpy(float)})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_uvm_fluxes_priv.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes)")
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_uvm_fluxes_priv_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} (permutation graine {SEED}, contrôle intact)")

    # (U3) d top-12 PRIV vs reste pour les 12 gènes v4 (réel + nul), et rho vs rang PRIV.
    u3 = []
    ranks = np.arange(len(out), dtype=float)
    for g in present_v4:
        v = out[g].to_numpy(float)
        rho, p = spearmanr(ranks, v)
        vn = nul[g].to_numpy(float)
        rho_n, p_n = spearmanr(ranks, vn)
        u3.append({"gene": g, "rho_priv_reel": round(float(rho), 3), "p_priv_reel": float(p),
                   "d_top12_reel": round(float(cohen_d(v[:-12], v[-12:])), 3),
                   "rho_priv_nul": round(float(rho_n), 3),
                   "d_top12_nul": round(float(cohen_d(vn[:-12], vn[-12:])), 3)})
    print(pd.DataFrame(u3).to_string())

    with open(f"{OUT}/uvm_881.json", "w", encoding="utf-8") as f:
        json.dump({"n_uvm": int(n_uvm), "tarball_uvm_sha256": uvm_sha,
                   "genes_privilege_presents": present_priv, "genes_privilege_absents": absent_priv,
                   "genes_v4_presents": present_v4, "genes_v4_absents": absent_v4,
                   "temoins_absents": absent_tem,
                   "priv_min": round(float(priv.min()), 4), "priv_mediane": round(float(priv.median()), 4),
                   "priv_max": round(float(priv.max()), 4),
                   "u1_niveaux": rows, "u3_chaine": u3,
                   "serie": {"fichier": out_path, "sha256": sha(out_path), "lignes": int(out.shape[0]),
                             "colonnes": list(out.columns)},
                   "nul": {"fichier": nul_path, "sha256": sha(nul_path)}}, f, indent=2, ensure_ascii=False)
    print("Écrit : uvm_881.json")
    print(f"SHA script : {sha(__file__)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
