#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.55 — Construction des 4 CSV T5' (runs v6.2).
Protocole gelé : PROTOCOL_purity_external_855.md
(SHA 734a9b171cf0ce155d456288d8f617528aa237820269d1c3e429505bce134db7).
Substitution gelée (§7) : ESTIMATE publiée non obtenue -> seuls les runs
ABSOLUTE sont construits (4 runs au lieu de 6).
Prédictions T5' (calculées AVANT tout run, depuis T1'/T2' du jour) :
  E-ABS : C = 0,4932 -> d_pred = -0,175 + 1,705 x 0,4932 = +0,6659
  E-RES (CD8A résid.) : C_résid = 0,4522 -> d_pred = +0,5960
  Référence CD8A brut IMMROT (§8.48) : écart +0,9838 (réel 1,2310, nul 0,2472) ;
  CD8A brut sur n=149 : C = 0,6059 -> d_pred +0,8581.
CSV (n = 149 tumeurs appariées avec ABSOLUTE, ordre KRAS brut conservé
pour la jointure, puis triés par le contrôle) :
  E-ABS : contrôle pureté ABSOLUTE, 12 flux immunitaires bruts, triés par
  ABSOLUTE croissant.
  E-RES : contrôle CD8A résidualisé ([1, ABSOLUTE]), 11 autres flux
  résidualisés (sans doublon).
Nuls : bloc analysé permuté conjointement, default_rng(42) FRAIS par fichier
(construction du projet), colonne de contrôle intacte.
Vérifications : résidus reproduisent la matrice T2' (moyenne |r| = 0,3757) ;
contrôles triés croissants ; SHA des 4 CSV dans purity_855_csv_sha.json.
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
    ext = pd.read_csv(f"{BASE}/purity_855_external.csv")
    imm = pd.read_csv(f"{BASE}/pdac_immune_tcga_fluxes.csv")
    axis = pd.read_csv(f"{BASE}/immune_kras_order_tcga.csv")
    assert len(ext) == 149, f"n apparié attendu 149, obtenu {len(ext)}"
    assert (ext["sample"].values == axis.set_index("sample").loc[ext["sample"].values].index.values).all()
    absol = ext["purity_absolute"].values.astype(float)
    assert not np.isnan(absol).any()
    assert ((absol >= 0) & (absol <= 1)).all()
    Y = imm.set_index(axis["sample"].values).loc[ext["sample"].values, IMM_GENES].values.astype(float)
    n = len(Y)

    # Résidus OLS sur [1, ABSOLUTE] — même définition que analyze_purity_855.py.
    X = np.column_stack([np.ones(n), absol])
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    resid = Y - X @ beta
    resid_df = pd.DataFrame(resid, columns=IMM_GENES)
    # Sanité : la matrice des résidus reproduit T2' (moyenne |r| = 0,3757).
    c = resid_df.corr(method="pearson").values
    iu = np.triu_indices_from(c, k=1)
    mean_abs_r = float(np.abs(c[iu]).mean())
    assert abs(mean_abs_r - 0.3757) < 0.001, f"résidus incohérents avec T2' : {mean_abs_r}"
    print(f"Résidus OK : moyenne |r| = {mean_abs_r:.4f} (T2' = 0,3757)")
    resid_df.to_csv(f"{BASE}/purity_855_immune_resid.csv", index=False)

    shas = {}

    def reg(tag, df):
        p, pn = write_csv(df, f"{BASE}/{tag}.csv")
        shas[f"{tag}.csv"] = sha(p)
        shas[f"{tag}_nul.csv"] = sha(pn)
        print(f"Écrit : {tag}.csv ({df.shape[0]} lignes) + nul")

    # E-ABS : tri par pureté ABSOLUTE croissante.
    o = np.argsort(absol)
    df_abs = pd.DataFrame({"purity_absolute": absol[o]})
    df_abs = pd.concat([df_abs, pd.DataFrame(Y[o], columns=IMM_GENES)], axis=1)
    assert df_abs["purity_absolute"].is_monotonic_increasing
    reg("purity855_eabs", df_abs)

    # E-RES : contrôle CD8A résidualisé, 11 autres flux résidualisés.
    others = [g for g in IMM_GENES if g != "CD8A"]
    o = np.argsort(resid[:, 0])
    df_res = pd.DataFrame({"CD8A_resid": resid[o, 0]})
    df_res = pd.concat([df_res, pd.DataFrame(resid[o][:, 1:], columns=others)], axis=1)
    assert df_res["CD8A_resid"].is_monotonic_increasing
    reg("purity855_eres", df_res)

    with open(f"{BASE}/purity_855_csv_sha.json", "w", encoding="utf-8") as f:
        json.dump(shas, f, indent=2, ensure_ascii=False)
    print("SHA des 4 CSV écrits dans purity_855_csv_sha.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
