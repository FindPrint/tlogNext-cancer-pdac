#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.51 — Construction des 6 CSV T5 (runs v6.2).
Protocole gelé : PROTOCOL_purity_infiltration_851.md
(SHA 568d93d2459db1b78219a91fb1620486ecb4a2f5f61ac478629f7508f0867ab5).
Prédictions T5 (calculées AVANT tout run, depuis T1/T2 du jour) :
  P-AC : C = 0,1463 -> d_pred = -0,175 + 1,705 x 0,1463 = +0,0745
  P-IS : C = 0,1980 -> d_pred = -0,175 + 1,705 x 0,1980 = +0,1625
  P-RES (CD8A résid.) : C_résid = 0,6414 -> d_pred = +0,9185
  Référence CD8A brut IMMROT (§8.48) : écart +0,9838 (réel 1,2310, nul 0,2472).
CSV :
  P-AC : contrôle score_acineux, 12 flux immunitaires bruts, triés par ac.
  P-IS : contrôle score_îlots, 12 flux immunitaires bruts, triés par is.
  P-RES : contrôle CD8A résidualisé, 11 autres flux résidualisés (sans doublon).
Nuls : bloc analysé permuté conjointement, default_rng(42) FRAIS par fichier
(construction du projet), colonne de contrôle intacte.
Vérifications : résidus reproduisent la matrice T2 (moyenne |r| = 0,5480) ;
contrôles triés croissants ; SHA des 6 CSV dans purity_851_csv_sha.json.
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
    scores = pd.read_csv(f"{BASE}/purity_851_scores.csv")
    imm = pd.read_csv(f"{BASE}/pdac_immune_tcga_fluxes.csv")
    assert len(scores) == 178 and len(imm) == 178
    assert (scores["sample"].values == pd.read_csv(
        f"{BASE}/immune_kras_order_tcga.csv")["sample"].values).all()
    ac = scores["score_acineux"].values
    islet = scores["score_ilots"].values
    Y = imm[IMM_GENES].values.astype(float)
    n = len(Y)

    # Résidus OLS sur [1, ac, is] — même définition que analyze_purity_851.py.
    X = np.column_stack([np.ones(n), ac, islet])
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    resid = Y - X @ beta
    resid_df = pd.DataFrame(resid, columns=IMM_GENES)
    # Sanité : la matrice des résidus reproduit T2 (moyenne |r| = 0,5480).
    c = resid_df.corr(method="pearson").values
    iu = np.triu_indices_from(c, k=1)
    mean_abs_r = float(np.abs(c[iu]).mean())
    assert abs(mean_abs_r - 0.5480) < 0.001, f"résidus incohérents avec T2 : {mean_abs_r}"
    print(f"Résidus OK : moyenne |r| = {mean_abs_r:.4f} (T2 = 0,5480)")
    resid_df.to_csv(f"{BASE}/purity_851_immune_resid.csv", index=False)

    shas = {}

    def reg(tag, df):
        p, pn = write_csv(df, f"{BASE}/{tag}.csv")
        shas[f"{tag}.csv"] = sha(p)
        shas[f"{tag}_nul.csv"] = sha(pn)
        print(f"Écrit : {tag}.csv ({df.shape[0]} lignes) + nul")

    # P-AC : tri par score acineux croissant.
    o = np.argsort(ac)
    df_ac = pd.DataFrame({"score_acineux": ac[o]})
    df_ac = pd.concat([df_ac, pd.DataFrame(Y[o], columns=IMM_GENES)], axis=1)
    assert df_ac["score_acineux"].is_monotonic_increasing
    reg("purity851_pac", df_ac)

    # P-IS : tri par score îlots croissant.
    o = np.argsort(islet)
    df_is = pd.DataFrame({"score_ilots": islet[o]})
    df_is = pd.concat([df_is, pd.DataFrame(Y[o], columns=IMM_GENES)], axis=1)
    assert df_is["score_ilots"].is_monotonic_increasing
    reg("purity851_pis", df_is)

    # P-RES : contrôle CD8A résidualisé, 11 autres flux résidualisés.
    others = [g for g in IMM_GENES if g != "CD8A"]
    o = np.argsort(resid[:, 0])
    df_res = pd.DataFrame({"CD8A_resid": resid[o, 0]})
    df_res = pd.concat([df_res, pd.DataFrame(resid[o][:, 1:], columns=others)], axis=1)
    assert df_res["CD8A_resid"].is_monotonic_increasing
    reg("purity851_pres", df_res)

    with open(f"{BASE}/purity_851_csv_sha.json", "w", encoding="utf-8") as f:
        json.dump(shas, f, indent=2, ensure_ascii=False)
    print("SHA des 6 CSV écrits dans purity_851_csv_sha.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
