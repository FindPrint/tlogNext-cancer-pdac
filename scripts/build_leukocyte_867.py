#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.67 — Construction des 4 CSV T5-L2 (runs v6.2).
Protocole gelé : PROTOCOL_leukocyte_decisive_867.md
(SHA 571adf826f455b8dfd49c63f2c0e94fc73a7ae03a6e98b5bfda2bb0648ae59ad).
Prédictions T5-L2 (calculées AVANT tout run, depuis T1-L2/T2-L2 du jour,
consignées dans leukocyte_867_predictions.json) :
  L-RES : C_résid CD8A = 0,4199 -> d_pred = +0,5409
  L-ORD : C_ord = 0,0000 (résidus OLS orthogonaux à leuco par construction)
          -> d_pred = -0,1750 (plancher : aucun signal LINÉAIRE ne reste ;
          toute séparation en L-ORD serait purement non linéaire)
  Références : CD8A brut IMMROT +0,9838 ; I-RES +0,1982 ; E-RES +0,6499 ;
  M-RES +0,5427 ; D-RES (TOP1) +0,7692 ; D-LEU +0,7129.
CSV (n = 150 tumeurs appariées avec la fraction leucocytaire par
méthylation, ordre KRAS brut conservé pour la jointure, puis triés par
le contrôle) :
  L-RES : contrôle CD8A résidualisé ([1, leuco]), 11 autres flux
  résidualisés (sans doublon).
  L-ORD : contrôle fraction leucocytaire BRUTE, 12 flux résidualisés
  ([1, leuco]).
Nuls : bloc analysé permuté conjointement, default_rng(42) FRAIS par fichier
(construction du projet), colonne de contrôle intacte.
Vérifications : résidus reproduisent la matrice T2-L2 (moyenne |r| = 0,3372) ;
contrôles triés croissants ; SHA des 4 CSV dans leukocyte_867_csv_sha.json.
"""
import hashlib
import json

import numpy as np
import pandas as pd

BASE = "/home/hatch/workspace/runs/pdac-v6"
IMM_GENES = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
             "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
SEED = 42


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(df, path):
    df.to_csv(path, index=False)
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(df))
    nul = df.copy()
    nul.iloc[:, 1:] = df.iloc[:, 1:].to_numpy()[perm]
    nul_path = path.replace(".csv", "_nul.csv")
    nul.to_csv(nul_path, index=False)
    return path, nul_path


def main():
    pred = json.load(open(f"{BASE}/leukocyte_867_predictions.json"))
    print(f"Prédictions gelées AVANT runs : L-RES d_pred={pred['L_RES']['d_pred']:+.4f} ; "
          f"L-ORD d_pred={pred['L_ORD']['d_pred']:+.4f}")
    ext = pd.read_csv(f"{BASE}/leukocyte_867_external.csv")
    imm = pd.read_csv(f"{BASE}/pdac_immune_tcga_fluxes.csv")
    axis = pd.read_csv(f"{BASE}/immune_kras_order_tcga.csv")
    assert len(ext) == 150, f"n apparié attendu 150, obtenu {len(ext)}"
    assert (ext["sample"].values == axis.set_index("sample").loc[ext["sample"].values].index.values).all()
    leuko = ext["leukocyte_methylation"].values.astype(float)
    assert not np.isnan(leuko).any()
    assert ((leuko >= 0) & (leuko <= 1)).all()
    Y = imm.set_index(axis["sample"].values).loc[ext["sample"].values, IMM_GENES].values.astype(float)
    n = len(Y)

    # Résidus OLS sur [1, leuco] — même définition que analyze_leukocyte_867.py.
    X = np.column_stack([np.ones(n), leuko])
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    resid = Y - X @ beta
    resid_df = pd.DataFrame(resid, columns=IMM_GENES)
    # Sanité : la matrice des résidus reproduit T2-L2 (moyenne |r| = 0,3372).
    c = resid_df.corr(method="pearson").values
    iu = np.triu_indices_from(c, k=1)
    mean_abs_r = float(np.abs(c[iu]).mean())
    assert abs(mean_abs_r - 0.3372) < 0.001, f"résidus incohérents avec T2-L2 : {mean_abs_r}"
    print(f"Résidus OK : moyenne |r| = {mean_abs_r:.4f} (T2-L2 = 0,3372)")
    # Sanité : orthogonalité des résidus à leuco (C_ord ≈ 0 par construction).
    c_ord_vals = [abs(float(np.corrcoef(leuko, resid[:, j])[0, 1])) for j in range(12)]
    c_ord = float(np.mean(c_ord_vals))
    assert abs(c_ord - pred["L_ORD"]["C_ord_leuco_vs_resid"]) < 1e-9, \
        f"C_ord incohérent avec les prédictions : {c_ord}"
    print(f"Orthogonalité OK : C_ord = {c_ord:.2e} (prédiction L-ORD = "
          f"{pred['L_ORD']['d_pred']:+.4f})")
    resid_df.to_csv(f"{BASE}/leukocyte_867_immune_resid.csv", index=False)

    shas = {}

    def reg(tag, df):
        p, pn = write_csv(df, f"{BASE}/{tag}.csv")
        shas[f"{tag}.csv"] = sha(p)
        shas[f"{tag}_nul.csv"] = sha(pn)
        print(f"Écrit : {tag}.csv ({df.shape[0]} lignes) + nul")

    # L-RES : tri par CD8A résidualisé croissant.
    others = [g for g in IMM_GENES if g != "CD8A"]
    o = np.argsort(resid[:, 0])
    df_res = pd.DataFrame({"CD8A_resid": resid[o, 0]})
    df_res = pd.concat([df_res, pd.DataFrame(resid[o][:, 1:], columns=others)], axis=1)
    assert df_res["CD8A_resid"].is_monotonic_increasing
    reg("leukocyte867_lres", df_res)

    # L-ORD : tri par fraction leucocytaire brute croissante.
    o = np.argsort(leuko)
    df_ord = pd.DataFrame({"leukocyte_methylation": leuko[o]})
    df_ord = pd.concat([df_ord, pd.DataFrame(resid[o], columns=IMM_GENES)], axis=1)
    assert df_ord["leukocyte_methylation"].is_monotonic_increasing
    reg("leukocyte867_lord", df_ord)

    with open(f"{BASE}/leukocyte_867_csv_sha.json", "w", encoding="utf-8") as f:
        json.dump(shas, f, indent=2, ensure_ascii=False)
    print("SHA des 4 CSV écrits dans leukocyte_867_csv_sha.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
