#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test A — série TCGA v4 ordonnée par prolifération (18 nov. 2026).
Protocole gelé : PROTOCOL_testA_proliferation.md (écrit avant ce script).

- Recalcule les résidus v4 depuis la matrice Firehose (même méthode que
  build_fluxes_tcga_v4.py) et VÉRIFIE qu'ils reproduisent le CSV v4
  (12 colonnes de flux, triées par résidu KRAS croissant, atol 1e-9).
  Arrêt si un écart dépasse le seuil.
- Score de prolifération = médiane des RÉSIDUS de MKI67, TOP2A, PCNA,
  CCNB1 (définition (c) du §8.25, atr_chek1_retest.py).
  Sensibilité rapportée : même score sur valeurs brutes log2(RSEM+1).
- Série réelle : PROLIF en 1re colonne (contrôle), 12 flux v4 dans
  l'ordre v4, lignes triées par PROLIF croissant. PROLIF n'est pas un
  flux : pas de doublon contrôle/flux (défaut des rotations §8.32 évité).
- Nul : colonnes de flux permutées, graine 42, générateur frais rng(42),
  colonne de contrôle intacte (même convention que les autres nuls).
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
TARBALL = f"{DATA}/tcga_paad_rsem.tar.gz"
TARBALL_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
V4_CSV = f"{OUT}/pdac_tcga_fluxes_v4.csv"
V4_SHA = "e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0"
SEED = 42
ATOL = 1e-9

ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]
ISLET = ["INS", "GCG", "PPY", "SST"]
PROLIF = ["MKI67", "TOP2A", "PCNA", "CCNB1"]


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
    print(f"Tumeurs primaires (code 01) : {logmat.shape[1]} ; gènes : {logmat.shape[0]}")

    score_ac = logmat.loc[[g for g in ACINAR if g in logmat.index]].median(axis=0)
    score_is = logmat.loc[[g for g in ISLET if g in logmat.index]].median(axis=0)
    X = np.column_stack([np.ones(len(logmat.columns)), score_ac.values,
                         score_is.values])
    Y = logmat.values
    beta, *_ = np.linalg.lstsq(X, Y.T, rcond=None)
    resid = Y - (X @ beta).T
    resid_df = pd.DataFrame(resid, index=logmat.index, columns=logmat.columns)

    # --- Vérification de reproduction du CSV v4 (arrêt si écart > atol) ---
    v4 = pd.read_csv(V4_CSV)
    flux_cols = list(v4.columns[1:])
    kras_res = resid_df.loc["KRAS"].sort_values(ascending=True)
    order_kras = list(kras_res.index)
    recomputed = resid_df.loc[flux_cols, order_kras].T.reset_index(drop=True)
    assert recomputed.shape == v4[flux_cols].shape, "forme v4 différente"
    max_diff = float(np.abs(recomputed.values - v4[flux_cols].values).max())
    print(f"Vérification v4 : 12 flux recalculés, écart max vs CSV v4 = {max_diff:.3e} (atol {ATOL:g})")
    assert max_diff <= ATOL, f"ÉCART v4 {max_diff:.3e} > atol — ARRÊT"
    pgc_diff = float(np.abs(recomputed["PGC"].values - v4["PGC"].values).max())
    print(f"Colonne PGC seule : écart max = {pgc_diff:.3e} — reproduction exacte.")
    assert len(order_kras) == 178 == len(v4)

    # --- Score de prolifération (résidus, définition §8.25 (c)) ---
    missing = [g for g in PROLIF if g not in resid_df.index]
    assert not missing, f"gènes prolifération absents : {missing}"
    prolif_res = resid_df.loc[PROLIF].median(axis=0)
    prolif_raw = logmat.loc[PROLIF].median(axis=0)
    print(f"Score prolif (résidus) : min={prolif_res.min():+.3f} "
          f"médiane={prolif_res.median():+.3f} max={prolif_res.max():+.3f}")
    rho_res, p_res = spearmanr(prolif_res.loc[order_kras].to_numpy(), np.arange(178))
    rho_raw, p_raw = spearmanr(prolif_raw.loc[order_kras].to_numpy(), np.arange(178))
    print(f"Spearman prolif (résidus) vs rang KRAS : {rho_res:+.3f} (p={p_res:.2e})")
    print(f"Spearman prolif (brut) vs rang KRAS : {rho_raw:+.3f} (p={p_raw:.2e})")
    rho_scores, _ = spearmanr(prolif_res, prolif_raw)
    print(f"Spearman score résidus vs score brut : {rho_scores:+.4f}")
    order_prolif = list(prolif_res.sort_values(ascending=True).index)
    order_prolif_raw = list(prolif_raw.sort_values(ascending=True).index)
    top12_res = set(order_prolif[-12:])
    top12_raw = set(order_prolif_raw[-12:])
    print(f"Recouvrement top-12 proliférantes (résidus vs brut) : "
          f"{len(top12_res & top12_raw)}/12")
    print(f"Recouvrement top-12 prolif (résidus) vs top-12 KRAS : "
          f"{len(top12_res & set(order_kras[-12:]))}/12")

    # --- Série réelle : PROLIF contrôle, 12 flux v4, tri par PROLIF ---
    flux = resid_df.loc[flux_cols, order_prolif].T
    assert flux.isna().sum().sum() == 0
    out = pd.DataFrame({"PROLIF": prolif_res.loc[order_prolif].values})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_tcga_fluxes_v4_prolif.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes)")

    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_tcga_fluxes_v4_prolif_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} (permutation graine {SEED}, contrôle intact)")

    provenance = {
        "date": "2026-11-18",
        "test": "Test A — série TCGA v4 ordonnée par prolifération",
        "protocole": "PROTOCOL_testA_proliferation.md (gelé avant les runs)",
        "go": "Zackary, 18 nov. 2026, 15h06",
        "source": "Broad GDAC Firehose stddata 2016-01-28, PAAD, RSEM genes "
                  "normalized, tarball déjà sur disque",
        "tarball": {"fichier": TARBALL, "md5": TARBALL_MD5},
        "base_v4": {"fichier": V4_CSV, "sha256": V4_SHA},
        "verification_reproduction": {
            "méthode": "résidus v4 recalculés depuis le tarball, triés par "
                       "résidu KRAS croissant, comparés au CSV v4",
            "échantillon": 178,
            "écart_max_12_flux": max_diff,
            "écart_max_PGC": pgc_diff,
            "atol": ATOL,
            "résultat": "reproduction exacte (écart <= atol)" if max_diff <= ATOL else "ÉCHEC",
        },
        "score_prolifération": {
            "définition": "médiane des résidus (correction pureté v4) de "
                          "MKI67, TOP2A, PCNA, CCNB1 — §8.25 (c)",
            "spearman_vs_rang_KRAS_résidus": {"rho": round(float(rho_res), 4),
                                              "p": float(p_res)},
            "spearman_vs_rang_KRAS_brut": {"rho": round(float(rho_raw), 4),
                                           "p": float(p_raw)},
            "spearman_score_résidus_vs_brut": round(float(rho_scores), 4),
            "recouvrement_top12_résidus_vs_brut": len(top12_res & top12_raw),
            "recouvrement_top12_prolif_vs_KRAS": len(top12_res & set(order_kras[-12:])),
            "min": round(float(prolif_res.min()), 4),
            "médiane": round(float(prolif_res.median()), 4),
            "max": round(float(prolif_res.max()), 4),
        },
        "série": {"fichier": out_path, "sha256": sha(out_path),
                  "lignes": int(out.shape[0]), "colonnes": list(out.columns),
                  "ordre": "score de prolifération (résidus) croissant",
                  "contrôle": "PROLIF (1re colonne, pas un flux — pas de doublon)"},
        "nul": {"fichier": nul_path, "sha256": sha(nul_path),
                "méthode": "mêmes lignes permutées, graine 42, contrôle intact"},
        "script": "build_fluxes_tcga_v4_prolif.py",
    }
    with open(f"{OUT}/PROVENANCE_testA_proliferation.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — Test A : série TCGA v4 ordonnée par prolifération (18 nov. 2026)\n\n")
        f.write("```json\n" + json.dumps(provenance, indent=2, ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_testA_proliferation.md")
    print(f"SHA script : {sha(__file__)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
