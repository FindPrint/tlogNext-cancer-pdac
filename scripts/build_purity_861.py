#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.61 — Construction des 4 CSV T5'' (runs v6.2).
Protocole gelé : PROTOCOL_methylation_purity_861.md
(SHA 93f4f777f217d9a03c01b1b79397ed70e59567e53edaf4231864e9c6a50e0993).
Prédictions T5'' (calculées AVANT tout run, depuis T1''/T2'' du jour) :
  M-METH : C = 0,4228 -> d_pred = -0,175 + 1,705 x 0,4228 = +0,5459
  M-RES (CD8A résid.) : C_résid = 0,5092 -> d_pred = +0,6932
  Référence CD8A brut IMMROT (§8.48) : écart +0,9838 (réel 1,2310, nul 0,2472) ;
  CD8A brut sur n=150 : C = 0,6056 -> d_pred +0,8575.
  Référence E-RES (§8.55) : +0,6499.
CSV (n = 150 tumeurs appariées avec METH, ordre KRAS brut conservé
pour la jointure, puis triés par le contrôle) :
  M-METH : contrôle pureté METH, 12 flux immunitaires bruts, triés par
  METH croissant.
  M-RES : contrôle CD8A résidualisé ([1, METH]), 11 autres flux
  résidualisés (sans doublon).
Nuls : bloc analysé permuté conjointement, default_rng(42) FRAIS par fichier
(construction du projet), colonne de contrôle intacte.
Vérifications : résidus reproduisent la matrice T2'' (moyenne |r| = 0,4235) ;
contrôles triés croissants ; SHA des 4 CSV dans purity_861_csv_sha.json.
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
    ext = pd.read_csv(f"{BASE}/purity_861_external.csv")
    imm = pd.read_csv(f"{BASE}/pdac_immune_tcga_fluxes.csv")
    axis = pd.read_csv(f"{BASE}/immune_kras_order_tcga.csv")
    assert len(ext) == 150, f"n apparié attendu 150, obtenu {len(ext)}"
    assert (ext["sample"].values == axis.set_index("sample").loc[ext["sample"].values].index.values).all()
    meth = ext["purity_methylation"].values.astype(float)
    assert not np.isnan(meth).any()
    assert ((meth >= 0) & (meth <= 1)).all()
    Y = imm.set_index(axis["sample"].values).loc[ext["sample"].values, IMM_GENES].values.astype(float)
    n = len(Y)

    # Résidus OLS sur [1, METH] — même définition que analyze_purity_861.py.
    X = np.column_stack([np.ones(n), meth])
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    resid = Y - X @ beta
    resid_df = pd.DataFrame(resid, columns=IMM_GENES)
    # Sanité : la matrice des résidus reproduit T2'' (moyenne |r| = 0,4235).
    c = resid_df.corr(method="pearson").values
    iu = np.triu_indices_from(c, k=1)
    mean_abs_r = float(np.abs(c[iu]).mean())
    assert abs(mean_abs_r - 0.4235) < 0.001, f"résidus incohérents avec T2'' : {mean_abs_r}"
    print(f"Résidus OK : moyenne |r| = {mean_abs_r:.4f} (T2'' = 0,4235)")
    resid_df.to_csv(f"{BASE}/purity_861_immune_resid.csv", index=False)

    shas = {}

    def reg(tag, df):
        p, pn = write_csv(df, f"{BASE}/{tag}.csv")
        shas[f"{tag}.csv"] = sha(p)
        shas[f"{tag}_nul.csv"] = sha(pn)
        print(f"Écrit : {tag}.csv ({df.shape[0]} lignes) + nul")

    # M-METH : tri par pureté METH croissante.
    o = np.argsort(meth)
    df_meth = pd.DataFrame({"purity_methylation": meth[o]})
    df_meth = pd.concat([df_meth, pd.DataFrame(Y[o], columns=IMM_GENES)], axis=1)
    assert df_meth["purity_methylation"].is_monotonic_increasing
    reg("purity861_mmeth", df_meth)

    # M-RES : contrôle CD8A résidualisé, 11 autres flux résidualisés.
    others = [g for g in IMM_GENES if g != "CD8A"]
    o = np.argsort(resid[:, 0])
    df_res = pd.DataFrame({"CD8A_resid": resid[o, 0]})
    df_res = pd.concat([df_res, pd.DataFrame(resid[o][:, 1:], columns=others)], axis=1)
    assert df_res["CD8A_resid"].is_monotonic_increasing
    reg("purity861_mres", df_res)

    with open(f"{BASE}/purity_861_csv_sha.json", "w", encoding="utf-8") as f:
        json.dump(shas, f, indent=2, ensure_ascii=False)
    print("SHA des 4 CSV écrits dans purity_861_csv_sha.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
