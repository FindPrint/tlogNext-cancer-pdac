#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Piste Œil §8.81 — série TCGA v4 ordonnée par score de privilège PRIV (bras pipeline).
Protocole gelé : PROTOCOL_oeil_privilege_881.md (§4, §6).

- Recalcule les résidus v4 depuis le tarball PAAD et VÉRIFIE qu'ils reproduisent le CSV v4
  (12 colonnes de flux, triées par résidu KRAS croissant, atol 1e-9). Arrêt si écart > atol.
- PRIV(tumeur) = moyenne des z-scores (intra-cohorte) des gènes de privilège PRÉSENTS
  (FASLG, TGFB1, TGFB2, IDO1, HLA-G, CD47, CD274) sur leurs RÉSIDUS (même correction que v4).
  Aucun des 7 n'est parmi les 12 flux v4 : pas de doublon contrôle/flux.
- Série réelle : PRIV en 1re colonne (contrôle), 12 flux v4 dans l'ordre v4, lignes triées par PRIV croissant.
- Nul : bloc des 12 flux permuté par lignes, graine 42, générateur frais rng(42), colonne PRIV intacte.
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
V4_CSV = f"{OUT}/pdac_tcga_fluxes_v4.csv"
V4_SHA = "e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0"
SEED = 42
ATOL = 1e-9

PRIV_GENES = ["FASLG", "TGFB1", "TGFB2", "IDO1", "HLA-G", "CD47", "CD274"]
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
    assert sha(V4_CSV) == V4_SHA, "SHA du CSV v4 non conforme"
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
    score_ac = logmat.loc[[g for g in ACINAR if g in logmat.index]].median(axis=0)
    score_is = logmat.loc[[g for g in ISLET if g in logmat.index]].median(axis=0)
    X = np.column_stack([np.ones(len(logmat.columns)), score_ac.values, score_is.values])
    Y = logmat.values
    beta, *_ = np.linalg.lstsq(X, Y.T, rcond=None)
    resid = Y - (X @ beta).T
    resid_df = pd.DataFrame(resid, index=logmat.index, columns=logmat.columns)

    v4 = pd.read_csv(V4_CSV)
    flux_cols = list(v4.columns[1:])
    kras_res = resid_df.loc["KRAS"].sort_values(ascending=True)
    order_kras = list(kras_res.index)
    recomputed = resid_df.loc[flux_cols, order_kras].T.reset_index(drop=True)
    max_diff = float(np.abs(recomputed.values - v4[flux_cols].values).max())
    print(f"Vérification v4 : écart max = {max_diff:.3e} (atol {ATOL:g})")
    assert max_diff <= ATOL, f"ÉCART v4 {max_diff:.3e} > atol — ARRÊT"

    present = [g for g in PRIV_GENES if g in resid_df.index]
    absent = [g for g in PRIV_GENES if g not in resid_df.index]
    print(f"Gènes de privilège présents (résidus TCGA) : {present}")
    print(f"Gènes de privilège absents : {absent}")
    assert len(present) >= 4, "moins de 4 gènes de privilège présents — ARRÊT (protocole §4)"

    barcodes = list(resid_df.columns)
    zmat = np.vstack([(resid_df.loc[g].to_numpy(float) - resid_df.loc[g].mean()) / resid_df.loc[g].std(ddof=0)
                      for g in present])
    priv = pd.Series(zmat.mean(axis=0), index=barcodes)
    print(f"PRIV : min={priv.min():+.3f} médiane={priv.median():+.3f} max={priv.max():+.3f} (gènes du score : {len(present)})")
    order_priv = priv.sort_values(ascending=True).index.tolist()
    flux = resid_df.loc[flux_cols, order_priv].T
    assert flux.isna().sum().sum() == 0
    out = pd.DataFrame({"PRIV": priv.loc[order_priv].to_numpy(float)})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_tcga_fluxes_v4_priv.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes)")

    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_tcga_fluxes_v4_priv_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} (permutation graine {SEED}, contrôle intact)")

    # Corrélation PRIV vs rang KRAS (rapportée, ne change pas la série).
    from scipy.stats import spearmanr
    kras_rank = {bc: i for i, bc in enumerate(order_kras)}
    rho, p = spearmanr(priv.loc[order_priv].to_numpy(float),
                       np.array([kras_rank[bc] for bc in order_priv]))
    print(f"Spearman PRIV vs rang KRAS : rho={rho:+.4f} (p={p:.3g})")
    top12_priv = set(order_priv[-12:])
    top12_kras = set(order_kras[-12:])
    print(f"Recouvrement top-12 PRIV/KRAS : {len(top12_priv & top12_kras)}/12")

    provenance = {
        "date": "2026-11-21",
        "chantier": "Piste Œil §8.81 — série TCGA v4 ordonnée par score de privilège PRIV",
        "protocole": "PROTOCOL_oeil_privilege_881.md (gelé avant les runs)",
        "tarball": {"fichier": TARBALL, "md5": TARBALL_MD5},
        "base_v4": {"fichier": V4_CSV, "sha256": V4_SHA},
        "verification_reproduction": {"écart_max_12_flux": max_diff, "atol": ATOL,
                                      "résultat": "reproduction exacte" if max_diff <= ATOL else "ÉCHEC"},
        "score_priv": {"définition": "moyenne des z-scores intra-cohorte des gènes de privilège présents, sur résidus",
                       "gènes_présents": present, "gènes_absents": absent,
                       "min": round(float(priv.min()), 4), "médiane": round(float(priv.median()), 4),
                       "max": round(float(priv.max()), 4)},
        "cohérence": {"spearman_priv_vs_rang_KRAS": {"rho": round(float(rho), 4), "p": float(p)},
                      "recouvrement_top12_priv_vs_kras": len(top12_priv & top12_kras)},
        "série": {"fichier": out_path, "sha256": sha(out_path), "lignes": int(out.shape[0]),
                  "colonnes": list(out.columns), "ordre": "PRIV croissant",
                  "contrôle": "PRIV (1re colonne, pas un flux — pas de doublon)"},
        "nul": {"fichier": nul_path, "sha256": sha(nul_path),
                "méthode": "bloc des 12 flux permuté par lignes, graine 42, contrôle intact"},
        "script": "build_priv_881.py",
    }
    with open(f"{OUT}/PROVENANCE_priv_881.json", "w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2, ensure_ascii=False)
    print("Provenance écrite : PROVENANCE_priv_881.json")
    print(f"SHA script : {sha(__file__)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
