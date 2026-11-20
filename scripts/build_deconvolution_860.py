#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.60 — Construction des 8 CSV T5/T5-L (runs v6.2).
Protocole gelé : PROTOCOL_deconvolution_860.md
(SHA 471568b1eb83027d4341c7ec5632b5749cf60aa2d06e8a4ddbf2315ffed86d57).
TOP1/TOP2/TOP3 définis par T1 AVANT les runs (analyze_deconvolution_860.py) :
  TOP1 = B.Cells.Naive (mean|r| 0,3314), TOP2 = T.Cells.CD8 (0,3293),
  TOP3 = Macrophages.M0 (0,2878). n effectif CIBERSORT = 151 ; bras L n = 150.
Prédictions T5 (calculées AVANT tout run, depuis T1/T2/T3 du jour) :
  D-TOP1 : C = 0,3314 -> d_pred = -0,175 + 1,705 x 0,3314 = +0,3900
  D-TOP2 : C = 0,3293 -> d_pred = +0,3865
  D-RES (CD8A résid. sur [1, TOP1]) : C_résid = 0,5770 -> d_pred = +0,8089
  D-LEU : C = 0,5456 -> d_pred = +0,7552
  Références : CD8A brut IMMROT (§8.48) : écart +0,9838 (réel 1,2310,
  nul 0,2472) ; I-RES §8.54 : +0,1982 ; E-RES §8.55 : +0,6499.
CSV :
  D-TOP1 : contrôle B.Cells.Naive, 12 flux immunitaires bruts (n=151),
  triés par B.Cells.Naive.
  D-TOP2 : contrôle T.Cells.CD8, idem (n=151).
  D-RES : contrôle CD8A résidualisé ([1, TOP1]), 11 autres flux
  résidualisés (sans doublon).
  D-LEU : contrôle fraction leucocytaire par méthylation (Raphael Table S1
  via pdacR), 12 flux immunitaires bruts (n=150), triés par fraction.
Nuls : bloc analysé permuté conjointement, default_rng(42) FRAIS par fichier
(construction du projet), colonne de contrôle intacte.
Vérifications : résidus reproduisent la matrice T2(a) (moyenne |r| = 0,4805)
; contrôles triés croissants ; SHA des 8 CSV dans
deconvolution_860_csv_sha.json.
"""
import hashlib
import json

import numpy as np
import pandas as pd

BASE = "/home/hatch/workspace/runs/pdac-v6"
IMM_GENES = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
             "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
TOP1 = "B.Cells.Naive"
TOP2 = "T.Cells.CD8"
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
    ext = pd.read_csv(f"{BASE}/deconvolution_860_external.csv")
    imm = pd.read_csv(f"{BASE}/pdac_immune_tcga_fluxes.csv")
    order = pd.read_csv(f"{BASE}/immune_kras_order_tcga.csv")
    assert len(ext) == 178 and len(imm) == 178 and len(order) == 178
    assert (ext["sample"].values == order["sample"].values).all()
    assert (imm["step"].values == order["step"].values).all()
    Y = imm[IMM_GENES].values.astype(float)

    shas = {}

    def reg(tag, df):
        p, pn = write_csv(df, f"{BASE}/{tag}.csv")
        shas[f"{tag}.csv"] = sha(p)
        shas[f"{tag}_nul.csv"] = sha(pn)
        print(f"Écrit : {tag}.csv ({df.shape[0]} lignes) + nul")

    # --- Bras principal : n = 151 (fractions CIBERSORT complètes) ---
    keep = ext[TOP1].notna().values
    print(f"Bras principal n={int(keep.sum())} (TOP1 non-NaN)")
    assert int(keep.sum()) == 151
    Yk = Y[keep]
    x1 = ext.loc[keep, TOP1].values.astype(float)
    x2 = ext.loc[keep, TOP2].values.astype(float)
    assert not np.isnan(x1).any() and not np.isnan(x2).any()

    # Résidus OLS sur [1, TOP1] — même définition que analyze_deconvolution_860.py.
    X = np.column_stack([np.ones(int(keep.sum())), x1])
    beta, *_ = np.linalg.lstsq(X, Yk, rcond=None)
    resid = Yk - X @ beta
    resid_df = pd.DataFrame(resid, columns=IMM_GENES)
    c = resid_df.corr(method="pearson").values
    iu = np.triu_indices_from(c, k=1)
    mean_abs_r = float(np.abs(c[iu]).mean())
    assert abs(mean_abs_r - 0.4805) < 0.001, f"résidus incohérents avec T2(a) : {mean_abs_r}"
    print(f"Résidus OK : moyenne |r| = {mean_abs_r:.4f} (T2(a) = 0,4805)")

    # D-TOP1 : tri par B.Cells.Naive croissant.
    o = np.argsort(x1)
    df1 = pd.DataFrame({TOP1: x1[o]})
    df1 = pd.concat([df1, pd.DataFrame(Yk[o], columns=IMM_GENES)], axis=1)
    assert df1[TOP1].is_monotonic_increasing
    reg("deconv860_dtop1", df1)

    # D-TOP2 : tri par T.Cells.CD8 croissant.
    o = np.argsort(x2)
    df2 = pd.DataFrame({TOP2: x2[o]})
    df2 = pd.concat([df2, pd.DataFrame(Yk[o], columns=IMM_GENES)], axis=1)
    assert df2[TOP2].is_monotonic_increasing
    reg("deconv860_dtop2", df2)

    # D-RES : contrôle CD8A résidualisé, 11 autres flux résidualisés.
    others = [g for g in IMM_GENES if g != "CD8A"]
    o = np.argsort(resid[:, 0])
    df3 = pd.DataFrame({"CD8A_resid": resid[o, 0]})
    df3 = pd.concat([df3, pd.DataFrame(resid[o][:, 1:], columns=others)], axis=1)
    assert df3["CD8A_resid"].is_monotonic_increasing
    reg("deconv860_dres", df3)

    # --- Bras L : n = 150 (fraction leucocytaire par méthylation non nulle) ---
    keepL = ext["Leukocyte_fraction_methylation_Raphael"].notna().values
    print(f"Bras L n={int(keepL.sum())}")
    assert int(keepL.sum()) == 150
    xL = ext.loc[keepL, "Leukocyte_fraction_methylation_Raphael"].values.astype(float)
    YL = Y[keepL]
    o = np.argsort(xL)
    dfL = pd.DataFrame({"leuko_methyl": xL[o]})
    dfL = pd.concat([dfL, pd.DataFrame(YL[o], columns=IMM_GENES)], axis=1)
    assert dfL["leuko_methyl"].is_monotonic_increasing
    reg("deconv860_dleu", dfL)

    with open(f"{BASE}/deconvolution_860_csv_sha.json", "w", encoding="utf-8") as f:
        json.dump(shas, f, indent=2, ensure_ascii=False)
    print("SHA des 8 CSV écrits dans deconvolution_860_csv_sha.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
