#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.68 — Construction des 8 CSV T5 (runs v6.2).
Protocole gelé : PROTOCOL_xcell_868.md
(SHA 416de4bcb783e0fc8390539a8104e7cd99b1d75355c42d4bff3e79c204c66c33).
TOP1/TOP2/TOP3/TOP-STROM définis par T1 AVANT les runs (analyze_xcell_868.py) :
  TOP1 = aDC (mean|r| 0,6102), TOP2 = DC (0,5796), TOP3 = Macrophages M1 (0,5090),
  TOP-STROM = Osteoblast (0,4823, rang 6/64, premier Non-Hematopoietic).
  n effectif xCell = 178 (jointure 178/178, 0 NaN).
  D-XSTROM lancé : condition gelée remplie (TOP-STROM ni TOP1 ni TOP2,
  mean|r| 0,4823 >= 0,30 — décision sur les seuls chiffres T1, avant tout run).
Prédictions T5 (calculées AVANT tout run, depuis T1/T2/T3 du jour) :
  D-XTOP1 : C = 0,6102 -> d_pred = -0,175 + 1,705 x 0,6102 = +0,8654
  D-XTOP2 : C = 0,5796 -> d_pred = +0,8132
  D-XRES (CD8A résid. sur [1, aDC]) : C_résid = 0,4218 -> d_pred = +0,5441
  D-XSTROM : C = 0,4823 -> d_pred = +0,6473
  Références : CD8A brut IMMROT (§8.48) : écart +0,9838 (réel 1,2310,
  nul 0,2472) ; I-RES §8.54 : +0,1982 ; E-RES §8.55 : +0,6499 ;
  D-RES §8.60 : +0,7692.
CSV :
  D-XTOP1 : contrôle aDC, 12 flux immunitaires bruts (n=178),
  triés par aDC.
  D-XTOP2 : contrôle DC, idem (n=178).
  D-XRES : contrôle CD8A résidualisé ([1, aDC]), 11 autres flux
  résidualisés (sans doublon).
  D-XSTROM : contrôle Osteoblast, 12 flux immunitaires bruts (n=178),
  triés par Osteoblast.
Nuls : bloc analysé permuté conjointement, default_rng(42) FRAIS par fichier
(construction du projet), colonne de contrôle intacte.
Vérifications : résidus reproduisent la matrice T2(a) (moyenne |r| = 0,3270)
; contrôles triés croissants ; SHA des 8 CSV dans
xcell_868_csv_sha.json.
"""
import hashlib
import json

import numpy as np
import pandas as pd

BASE = "/home/hatch/workspace/runs/pdac-v6"
IMM_GENES = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
             "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
TOP1 = "aDC"
TOP2 = "DC"
TOP_STROM = "Osteoblast"
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
    ext = pd.read_csv(f"{BASE}/xcell_868_external.csv")
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

    # --- Bras principal : n = 178 (scores xCell complets) ---
    x1 = ext[TOP1].values.astype(float)
    x2 = ext[TOP2].values.astype(float)
    xs = ext[TOP_STROM].values.astype(float)
    assert not np.isnan(x1).any() and not np.isnan(x2).any() and not np.isnan(xs).any()
    print(f"Bras principal n=178 (TOP1/TOP2/TOP-STROM non-NaN)")

    # Résidus OLS sur [1, TOP1] — même définition que analyze_xcell_868.py.
    X = np.column_stack([np.ones(len(Y)), x1])
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    resid = Y - X @ beta
    resid_df = pd.DataFrame(resid, columns=IMM_GENES)
    c = resid_df.corr(method="pearson").values
    iu = np.triu_indices_from(c, k=1)
    mean_abs_r = float(np.abs(c[iu]).mean())
    assert abs(mean_abs_r - 0.3270) < 0.001, f"résidus incohérents avec T2(a) : {mean_abs_r}"
    print(f"Résidus OK : moyenne |r| = {mean_abs_r:.4f} (T2(a) = 0,3270)")

    # D-XTOP1 : tri par aDC croissant.
    o = np.argsort(x1)
    df1 = pd.DataFrame({TOP1: x1[o]})
    df1 = pd.concat([df1, pd.DataFrame(Y[o], columns=IMM_GENES)], axis=1)
    assert df1[TOP1].is_monotonic_increasing
    reg("xcell868_dxtop1", df1)

    # D-XTOP2 : tri par DC croissant.
    o = np.argsort(x2)
    df2 = pd.DataFrame({TOP2: x2[o]})
    df2 = pd.concat([df2, pd.DataFrame(Y[o], columns=IMM_GENES)], axis=1)
    assert df2[TOP2].is_monotonic_increasing
    reg("xcell868_dxtop2", df2)

    # D-XRES : contrôle CD8A résidualisé, 11 autres flux résidualisés.
    others = [g for g in IMM_GENES if g != "CD8A"]
    o = np.argsort(resid[:, 0])
    df3 = pd.DataFrame({"CD8A_resid": resid[o, 0]})
    df3 = pd.concat([df3, pd.DataFrame(resid[o][:, 1:], columns=others)], axis=1)
    assert df3["CD8A_resid"].is_monotonic_increasing
    reg("xcell868_dxres", df3)

    # D-XSTROM : tri par Osteoblast croissant.
    o = np.argsort(xs)
    df4 = pd.DataFrame({TOP_STROM: xs[o]})
    df4 = pd.concat([df4, pd.DataFrame(Y[o], columns=IMM_GENES)], axis=1)
    assert df4[TOP_STROM].is_monotonic_increasing
    reg("xcell868_dxstrom", df4)

    with open(f"{BASE}/xcell_868_csv_sha.json", "w", encoding="utf-8") as f:
        json.dump(shas, f, indent=2, ensure_ascii=False)
    print("SHA des 8 CSV écrits dans xcell_868_csv_sha.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
