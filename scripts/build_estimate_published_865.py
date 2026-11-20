#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.65 — Construction des 6 CSV T5'' (runs v6.2).
Protocole gelé : PROTOCOL_estimate_published_865.md
(SHA b105e87b26c7f11b1bd29ec5eccfc05b8cb16cd5dbb5ff35db3f2df0dfd2961d).
Prédictions T5'' (calculées AVANT tout run, depuis T1''/T2'' du jour) :
  E-PIMM : C = 0,7164 -> d_pred = -0,175 + 1,705 x 0,7164 = +1,0466
  E-PSTR : C = 0,6002 -> d_pred = +0,8483
  E-PRES (CD8A résid.) : C_résid = 0,2765 -> d_pred = +0,2965
  Référence CD8A brut IMMROT (§8.48) : écart +0,9838 (réel 1,2310, nul 0,2472) ;
  références §8.54 (recalculé) : I-IMM +1,1942 ; I-STR +0,9407 ; I-RES +0,1982.
CSV (n = 178 tumeurs appariées avec les scores publiés, ordre KRAS brut
conservé pour la jointure, puis triés par le contrôle) :
  E-PIMM : contrôle ImmuneScore publié, 12 flux immunitaires bruts.
  E-PSTR : contrôle StromalScore publié, idem.
  E-PRES : contrôle CD8A résidualisé ([1, ImmuneScore_pub]), 11 autres flux
  résidualisés (sans doublon).
Nuls : bloc analysé permuté conjointement, default_rng(42) FRAIS par fichier
(construction du projet), colonne de contrôle intacte.
Vérifications : résidus reproduisent la matrice T2'' (moyenne |r| = 0,2001) ;
contrôles triés croissants ; SHA des 6 CSV dans estimate_published_865_csv_sha.json.
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
    ext = pd.read_csv(f"{BASE}/estimate_published_865_external.csv")
    assert len(ext) == 178, f"n apparié attendu 178, obtenu {len(ext)}"
    axis = pd.read_csv(f"{BASE}/immune_kras_order_tcga.csv")
    imm = pd.read_csv(f"{BASE}/pdac_immune_tcga_fluxes.csv")
    assert (imm["step"].values == axis["step"].values).all()
    assert (ext["sample"].values == axis["sample"].values).all(), \
        "ordre des échantillons appariés != ordre KRAS de l'axe"
    Y = imm[IMM_GENES].values.astype(float)
    imm_pub = ext["immune_pub"].values.astype(float)
    str_pub = ext["stromal_pub"].values.astype(float)
    n = len(Y)

    # Résidus OLS sur [1, ImmuneScore_pub] — même définition que analyze_..._865.py.
    X = np.column_stack([np.ones(n), imm_pub])
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    resid = Y - X @ beta
    resid_df = pd.DataFrame(resid, columns=IMM_GENES)
    c = resid_df.corr(method="pearson").values
    iu = np.triu_indices_from(c, k=1)
    mean_abs_r = float(np.abs(c[iu]).mean())
    assert abs(mean_abs_r - 0.2001) < 0.001, f"résidus incohérents avec T2'': {mean_abs_r}"
    print(f"Résidus OK : moyenne |r| = {mean_abs_r:.4f} (T2'' = 0,2001)")
    prev = pd.read_csv(f"{BASE}/estimate_published_865_immune_resid.csv")
    assert np.allclose(prev[IMM_GENES].values, resid, atol=1e-9), \
        "résidus incohérents avec estimate_published_865_immune_resid.csv"

    shas = {}

    def reg(tag, df):
        p, pn = write_csv(df, f"{BASE}/{tag}.csv")
        shas[f"{tag}.csv"] = sha(p)
        shas[f"{tag}_nul.csv"] = sha(pn)
        print(f"Écrit : {tag}.csv ({df.shape[0]} lignes) + nul")

    # E-PIMM : tri par ImmuneScore publié croissant.
    o = np.argsort(imm_pub)
    df_imm = pd.DataFrame({"ImmuneScore_pub": imm_pub[o]})
    df_imm = pd.concat([df_imm, pd.DataFrame(Y[o], columns=IMM_GENES)], axis=1)
    assert df_imm["ImmuneScore_pub"].is_monotonic_increasing
    reg("estpub865_epimm", df_imm)

    # E-PSTR : tri par StromalScore publié croissant.
    o = np.argsort(str_pub)
    df_str = pd.DataFrame({"StromalScore_pub": str_pub[o]})
    df_str = pd.concat([df_str, pd.DataFrame(Y[o], columns=IMM_GENES)], axis=1)
    assert df_str["StromalScore_pub"].is_monotonic_increasing
    reg("estpub865_epstr", df_str)

    # E-PRES : contrôle CD8A résidualisé, 11 autres flux résidualisés.
    others = [g for g in IMM_GENES if g != "CD8A"]
    o = np.argsort(resid[:, 0])
    df_res = pd.DataFrame({"CD8A_resid": resid[o, 0]})
    df_res = pd.concat([df_res, pd.DataFrame(resid[o][:, 1:], columns=others)], axis=1)
    assert df_res["CD8A_resid"].is_monotonic_increasing
    reg("estpub865_epres", df_res)

    with open(f"{BASE}/estimate_published_865_csv_sha.json", "w", encoding="utf-8") as f:
        json.dump(shas, f, indent=2, ensure_ascii=False)
    print("SHA des 6 CSV écrits dans estimate_published_865_csv_sha.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
