#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Étape 4 (c) — série TCGA v4 ordonnée par CN MTAP (18 nov. 2026).
Protocole gelé : PROTOCOL_enrichissements_833.md (écrit avant ce script).

- Recalcule les résidus v4 depuis la matrice Firehose (même méthode que
  build_fluxes_tcga_v4.py / build_fluxes_tcga_v4_prolif.py) et VÉRIFIE
  qu'ils reproduisent le CSV v4 (12 colonnes de flux, triées par résidu
  KRAS croissant, atol 1e-9). Arrêt si un écart dépasse le seuil.
- Contrôle = CN MTAP continue GISTIC (all_data_by_genes.txt, log2 ratio),
  tri croissant (perte profonde d'abord). Le seuillé (-2..+2) est rapporté
  comme contrôle de cohérence seulement (trop de ties).
- Jointure sur les 15 premiers caractères du code-barres TCGA (patient)
  entre GISTIC et les colonnes RSEM ; n apparié rapporté.
- Série réelle : MTAPCN en 1re colonne (contrôle), 12 flux v4 dans
  l'ordre v4, lignes triées par MTAPCN croissant. MTAPCN n'est pas un
  flux : pas de doublon contrôle/flux (défaut des rotations §8.32 évité).
- Nul : lignes permutées, graine 42, générateur frais rng(42),
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
GISTIC = f"{DATA}/tcga_paad_gistic.tar.gz"
GISTIC_MD5_PREFIX = "816034f7"
GISTIC_DIR = ("gdac.broadinstitute.org_PAAD-TP.CopyNumber_Gistic2."
              "Level_4.2016012800.0.0")
SEED = 42
ATOL = 1e-9

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
    assert md5(TARBALL) == TARBALL_MD5, "MD5 du tarball RSEM non conforme"
    assert sha(V4_CSV) == V4_SHA, "SHA du CSV v4 non conforme"
    gistic_md5 = md5(GISTIC)
    print(f"MD5 tarball GISTIC : {gistic_md5}")
    assert gistic_md5.startswith(GISTIC_MD5_PREFIX), \
        "MD5 du tarball GISTIC non conforme au §8.33"
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
    assert len(order_kras) == 178 == len(v4)

    # --- CN MTAP GISTIC : continue + seuillée ---
    with tarfile.open(GISTIC, "r:gz") as tf:
        cont = pd.read_csv(tf.extractfile(f"{GISTIC_DIR}/all_data_by_genes.txt"),
                           sep="\t", index_col=0, low_memory=False)
        thr = pd.read_csv(tf.extractfile(f"{GISTIC_DIR}/all_thresholded.by_genes.txt"),
                          sep="\t", index_col=0, low_memory=False)
    mtap_cont = cont.loc["MTAP"].drop(index=["Locus ID", "Cytoband"], errors="ignore")
    mtap_thr = thr.loc["MTAP"].drop(index=["Locus ID", "Cytoband"], errors="ignore")
    print(f"GISTIC : {len(mtap_cont)} échantillons ; MTAP continu "
          f"min={mtap_cont.min():+.3f} médiane={mtap_cont.median():+.3f} "
          f"max={mtap_cont.max():+.3f}")
    print(f"GISTIC : MTAP seuillé {mtap_thr.value_counts().sort_index().to_dict()}")

    # Jointure sur le patient (15 premiers caractères du code-barres)
    def patient(bc):
        return str(bc)[:15]

    rsem_patients = {patient(c): c for c in resid_df.columns}
    gistic_patients = {patient(c): c for c in mtap_cont.index}
    common = sorted(set(rsem_patients) & set(gistic_patients))
    print(f"Patients communs RSEM/GISTIC : {len(common)} / 178 tumeurs v4 ; "
          f"patients RSEM sans GISTIC : "
          f"{sorted(set(rsem_patients) - set(gistic_patients))}")
    print(f"Patients GISTIC sans RSEM : {len(set(gistic_patients) - set(rsem_patients))}")
    # Protocole : si < 178, la série utilise les tumeurs appariées
    # seulement (et le dit) — une tumeur sans GISTIC ne bloque pas la série.
    if len(common) < 178:
        print(f"ATTENTION : appariement {len(common)}/178 — la série "
              f"utilise les {len(common)} tumeurs appariées seulement "
              f"(protocole §0 (c)).")

    mtap_cn = pd.Series({rsem_patients[p]: float(mtap_cont[gistic_patients[p]])
                         for p in common})
    mtap_thr_s = pd.Series({rsem_patients[p]: int(mtap_thr[gistic_patients[p]])
                            for p in common})
    print(f"MTAP CN sur les 177 tumeurs appariées : min={mtap_cn.min():+.3f} "
          f"médiane={mtap_cn.median():+.3f} max={mtap_cn.max():+.3f}")
    print(f"MTAP seuillé sur les 177 appariées : {mtap_thr_s.value_counts().sort_index().to_dict()}")
    kras_rank = pd.Series({c: i for i, c in enumerate(order_kras)})
    matched_cols = [rsem_patients[p] for p in common]
    rho_kras, p_kras = spearmanr(mtap_cn.loc[matched_cols].to_numpy(),
                                 kras_rank.loc[matched_cols].to_numpy())
    print(f"Spearman CN MTAP vs rang KRAS (n={len(matched_cols)}) : "
          f"{rho_kras:+.3f} (p={p_kras:.2e})")

    order_mtap = list(mtap_cn.sort_values(ascending=True).index)
    top12_mtap = set(order_mtap[:12])
    top12_kras = set(order_kras[-12:])
    print(f"Recouvrement top-12 MTAP-délétées vs top-12 KRAS : "
          f"{len(top12_mtap & top12_kras)}/12")
    print(f"Top-12 MTAP : CN {sorted(mtap_cn.loc[order_mtap[:12]].values)} ; "
          f"seuillé {sorted(mtap_thr_s.loc[order_mtap[:12]].values)}")

    # --- Série réelle : MTAPCN contrôle, 12 flux v4, tri par MTAPCN ---
    flux = resid_df.loc[flux_cols, order_mtap].T
    assert flux.isna().sum().sum() == 0
    out = pd.DataFrame({"MTAPCN": mtap_cn.loc[order_mtap].values})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_tcga_fluxes_v4_mtap.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes)")

    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_tcga_fluxes_v4_mtap_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} (permutation graine {SEED}, contrôle intact)")

    provenance = {
        "date": "2026-11-18",
        "test": "Étape 4 (c) — série TCGA v4 ordonnée par CN MTAP",
        "protocole": "PROTOCOL_enrichissements_833.md (gelé avant les runs)",
        "go": "Zackary, 18 nov. 2026, 15h06",
        "source_rsem": "Broad GDAC Firehose stddata 2016-01-28, PAAD, RSEM genes "
                       "normalized, tarball déjà sur disque",
        "tarball_rsem": {"fichier": TARBALL, "md5": TARBALL_MD5},
        "base_v4": {"fichier": V4_CSV, "sha256": V4_SHA},
        "source_gistic": "Broad GDAC Firehose, PAAD-TP CopyNumber GISTIC2 "
                         "Level 4, 2016-01-28, tarball déjà sur disque",
        "tarball_gistic": {"fichier": GISTIC, "md5": gistic_md5},
        "verification_reproduction": {
            "méthode": "résidus v4 recalculés depuis le tarball, triés par "
                       "résidu KRAS croissant, comparés au CSV v4",
            "échantillon": 178,
            "écart_max_12_flux": max_diff,
            "atol": ATOL,
            "résultat": "reproduction exacte (écart <= atol)" if max_diff <= ATOL else "ÉCHEC",
        },
        "controle_mtap": {
            "définition": "CN MTAP continue GISTIC (all_data_by_genes.txt, "
                          "log2 ratio), tri croissant (perte profonde d'abord)",
            "fichier_seuille": "all_thresholded.by_genes.txt (cohérence seulement)",
            "appariement": f"{len(common)}/178 tumeurs (patient, 15 premiers caractères)",
            "min": round(float(mtap_cn.min()), 4),
            "médiane": round(float(mtap_cn.median()), 4),
            "max": round(float(mtap_cn.max()), 4),
            "seuille_178": {str(k): int(v) for k, v in
                            mtap_thr_s.value_counts().sort_index().items()},
            "spearman_vs_rang_KRAS": {"rho": round(float(rho_kras), 4),
                                      "p": float(p_kras)},
            "recouvrement_top12_mtap_vs_kras": len(top12_mtap & top12_kras),
        },
        "série": {"fichier": out_path, "sha256": sha(out_path),
                  "lignes": int(out.shape[0]), "colonnes": list(out.columns),
                  "ordre": "CN MTAP croissant",
                  "contrôle": "MTAPCN (1re colonne, pas un flux — pas de doublon)"},
        "nul": {"fichier": nul_path, "sha256": sha(nul_path),
                "méthode": "mêmes lignes permutées, graine 42, contrôle intact"},
        "script": "build_fluxes_tcga_v4_mtap.py",
    }
    with open(f"{OUT}/PROVENANCE_mtap_series.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — Étape 4 (c) : série TCGA v4 ordonnée par CN MTAP (18 nov. 2026)\n\n")
        f.write("```json\n" + json.dumps(provenance, indent=2, ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_mtap_series.md")
    print(f"SHA script : {sha(__file__)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
