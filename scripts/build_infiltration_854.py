#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.54 — Construction des 6 CSV T5 (runs v6.2).
Protocole gelé : PROTOCOL_infiltration_854.md
(SHA 89be31eda298de193a31360ba4bb7bdd0a2f94ef7a88e8ac37307e846c467918,
amendement alias du 20 nov. 2026 — voir protocole §2.3).
Prédictions T5 (calculées AVANT tout run, depuis T1/T2 du jour) :
  I-IMM : C = 0,7164 -> d_pred = -0,175 + 1,705 x 0,7164 = +1,0466
  I-STR : C = 0,6002 -> d_pred = -0,175 + 1,705 x 0,6002 = +0,8483
  I-RES (CD8A résid.) : C_résid = 0,2766 -> d_pred = +0,2966
  Références : CD8A brut IMMROT (§8.48) : écart +0,9838 (réel 1,2310,
  nul 0,2472) ; P-RES §8.51 : +0,9174.
CSV :
  I-IMM : contrôle ImmuneScore, 12 flux immunitaires bruts, triés par ImmuneScore.
  I-STR : contrôle StromalScore, 12 flux immunitaires bruts, triés par StromalScore.
  I-RES : contrôle CD8A résidualisé ([1, ImmuneScore]), 11 autres flux
  résidualisés (sans doublon).
Nuls : bloc analysé permuté conjointement, default_rng(42) FRAIS par fichier
(construction du projet), colonne de contrôle intacte.
Vérifications : résidus reproduisent la matrice T2 (moyenne |r| = 0,2002)
et le fichier infiltration_854_immune_resid.csv ; contrôles triés croissants ;
SHA des 6 CSV dans infiltration_854_csv_sha.json.
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
    scores = pd.read_csv(f"{BASE}/infiltration_854_scores.csv")
    imm = pd.read_csv(f"{BASE}/pdac_immune_tcga_fluxes.csv")
    assert len(scores) == 178 and len(imm) == 178
    assert (scores["sample"].values == pd.read_csv(
        f"{BASE}/immune_kras_order_tcga.csv")["sample"].values).all()
    imm_score = scores["ImmuneScore"].values
    str_score = scores["StromalScore"].values
    Y = imm[IMM_GENES].values.astype(float)
    n = len(Y)

    # Résidus OLS sur [1, ImmuneScore] — même définition que analyze_infiltration_854.py.
    X = np.column_stack([np.ones(n), imm_score])
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    resid = Y - X @ beta
    resid_df = pd.DataFrame(resid, columns=IMM_GENES)
    # Sanité : la matrice des résidus reproduit T2 (moyenne |r| = 0,2002).
    c = resid_df.corr(method="pearson").values
    iu = np.triu_indices_from(c, k=1)
    mean_abs_r = float(np.abs(c[iu]).mean())
    assert abs(mean_abs_r - 0.2002) < 0.001, f"résidus incohérents avec T2 : {mean_abs_r}"
    print(f"Résidus OK : moyenne |r| = {mean_abs_r:.4f} (T2 = 0,2002)")
    prev = pd.read_csv(f"{BASE}/infiltration_854_immune_resid.csv")
    assert np.allclose(prev.values, resid, atol=1e-9), \
        "résidus incohérents avec infiltration_854_immune_resid.csv"

    shas = {}

    def reg(tag, df):
        p, pn = write_csv(df, f"{BASE}/{tag}.csv")
        shas[f"{tag}.csv"] = sha(p)
        shas[f"{tag}_nul.csv"] = sha(pn)
        print(f"Écrit : {tag}.csv ({df.shape[0]} lignes) + nul")

    # I-IMM : tri par ImmuneScore croissant.
    o = np.argsort(imm_score)
    df_imm = pd.DataFrame({"ImmuneScore": imm_score[o]})
    df_imm = pd.concat([df_imm, pd.DataFrame(Y[o], columns=IMM_GENES)], axis=1)
    assert df_imm["ImmuneScore"].is_monotonic_increasing
    reg("infil854_iimm", df_imm)

    # I-STR : tri par StromalScore croissant.
    o = np.argsort(str_score)
    df_str = pd.DataFrame({"StromalScore": str_score[o]})
    df_str = pd.concat([df_str, pd.DataFrame(Y[o], columns=IMM_GENES)], axis=1)
    assert df_str["StromalScore"].is_monotonic_increasing
    reg("infil854_istr", df_str)

    # I-RES : contrôle CD8A résidualisé, 11 autres flux résidualisés.
    others = [g for g in IMM_GENES if g != "CD8A"]
    o = np.argsort(resid[:, 0])
    df_res = pd.DataFrame({"CD8A_resid": resid[o, 0]})
    df_res = pd.concat([df_res, pd.DataFrame(resid[o][:, 1:], columns=others)], axis=1)
    assert df_res["CD8A_resid"].is_monotonic_increasing
    reg("infil854_ires", df_res)

    with open(f"{BASE}/infiltration_854_csv_sha.json", "w", encoding="utf-8") as f:
        json.dump(shas, f, indent=2, ensure_ascii=False)
    print("SHA des 6 CSV écrits dans infiltration_854_csv_sha.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
