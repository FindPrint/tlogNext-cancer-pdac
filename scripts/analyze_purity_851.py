#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.51 — Porte J, T1-T4 : pureté / infiltration vs corrélation immunitaire.
Protocole gelé : PROTOCOL_purity_infiltration_851.md
(SHA 568d93d2459db1b78219a91fb1620486ecb4a2f5f61ac478629f7508f0867ab5).
Ne modifie ni le pipeline v6.2 ni le livre blanc. Aucun run ici.
Entrées : tarball TCGA-PAAD (MD5 vérifié), base immunitaire TCGA
(pdac_immune_tcga_fluxes.csv), fichier d'axe immune_kras_order_tcga.csv.
Sorties : purity_851_scores.csv, purity_851_results.json/.csv (T1-T4).
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd
from scipy import stats

BASE = "/home/hatch/workspace/runs/pdac-v6"
DATA = f"{BASE}/data"
TARBALL = f"{DATA}/tcga_paad_rsem.tar.gz"
TARBALL_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
IMMUNE_SHA = "66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e"
AXIS_SHA = "31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d"
V62_SHA = "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"

ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]
ISLET = ["INS", "GCG", "PPY", "SST"]
IMM_GENES = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
             "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]


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


def pearson_p(r, n):
    if abs(r) >= 1.0:
        return 0.0
    t = r * np.sqrt((n - 2) / (1 - r * r))
    return float(2 * stats.t.sf(abs(t), n - 2))


def mat_stats(mat):
    """mat : DataFrame (lignes x gènes). Stats sur paires hors diagonale."""
    c = mat.corr(method="pearson").values
    iu = np.triu_indices_from(c, k=1)
    v = np.abs(c[iu])
    cs = mat.corr(method="spearman").values
    vs = np.abs(cs[iu])
    return {"n_pairs": int(len(v)),
            "pearson_mean_abs_r": float(v.mean()),
            "pearson_median_abs_r": float(np.median(v)),
            "pearson_frac_gt_0.5": float((v > 0.5).mean()),
            "pearson_max_abs_r": float(v.max()),
            "spearman_mean_abs_r": float(vs.mean()),
            "spearman_median_abs_r": float(np.median(vs))}


def ols_resid(Y, X):
    """Y : (n, p) ; X : (n, k) avec intercept. Retourne résidus + R² par colonne."""
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    fitted = X @ beta
    resid = Y - fitted
    ss_tot = ((Y - Y.mean(axis=0)) ** 2).sum(axis=0)
    ss_res = (resid ** 2).sum(axis=0)
    with np.errstate(invalid="ignore", divide="ignore"):
        r2 = 1.0 - ss_res / ss_tot
    return resid, r2


def main():
    out = {}
    # --- Vérifications SHA gelées ---
    assert sha(f"{BASE}/pdac_immune_tcga_fluxes.csv") == IMMUNE_SHA, "SHA immunitaire non conforme"
    assert sha(f"{BASE}/immune_kras_order_tcga.csv") == AXIS_SHA, "SHA axe non conforme"
    assert sha("/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py") == V62_SHA, "SHA v6.2 non conforme"
    assert md5(TARBALL) == TARBALL_MD5, "MD5 tarball non conforme"
    out["sha_checks"] = {"immune": True, "axis": True, "v62": True, "tarball_md5": True}
    print("SHA/MD5 : 4/4 conformes.")

    # --- Rechargement tarball ---
    with tarfile.open(TARBALL, "r:gz") as tf:
        member = [m for m in tf.getmembers() if m.name.endswith(".data.txt")][0]
        f = tf.extractfile(member)
        df = pd.read_csv(f, sep="\t", index_col=0, low_memory=False)
    df.index = df.index.to_series().str.split("|").str[0]
    df = df[~df.index.duplicated(keep="first")]
    cols = df.columns.to_series()
    tumor_cols = cols[cols.str[13:15] == "01"]
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    need = ["KRAS"] + IMM_GENES + ACINAR + ISLET
    missing = [g for g in need if g not in mat.index]
    assert not missing, f"gènes absents du tarball : {missing}"
    mat = mat[~mat.isna().any(axis=1)]
    logmat = np.log2(mat + 1.0)
    n_tum = int(logmat.shape[1])
    print(f"Tumeurs primaires : {n_tum}")

    score_ac = logmat.loc[ACINAR].median(axis=0)
    score_is = logmat.loc[ISLET].median(axis=0)
    kras_raw = logmat.loc["KRAS"]

    # --- Porte J ---
    axis = pd.read_csv(f"{BASE}/immune_kras_order_tcga.csv")
    imm = pd.read_csv(f"{BASE}/pdac_immune_tcga_fluxes.csv")
    assert list(imm.columns[1:]) == IMM_GENES, "colonnes immunitaires inattendues"
    assert len(axis) == 178 and len(imm) == 178, "n != 178"
    order_recalc = list(kras_raw.sort_values(ascending=True).index)
    order_file = list(axis["sample"])
    gate_order = (order_recalc == order_file)
    # KRAS brut recalculé vs fichier d'axe : valeurs aussi
    kras_file = axis["kras_raw"].values
    kras_rec = kras_raw.loc[order_file].values
    gate_kras_val = bool(np.allclose(kras_file, kras_rec, atol=1e-9))
    # Scores joints par barcode, dans l'ordre immunitaire
    samples = order_file
    assert set(samples) <= set(logmat.columns), "barcodes axe absents du tarball"
    ac = score_ac.loc[samples].values
    islet = score_is.loc[samples].values
    assert not np.isnan(ac).any() and not np.isnan(islet).any(), "NaN dans les scores"
    # Sanité : score acineux recalculé vs colonne v4r_purity triée
    v4p = pd.read_csv(f"{BASE}/pdac_tcga_fluxes_v4r_purity.csv")
    gate_purity_col = bool(np.allclose(np.sort(ac), v4p["score_acineux"].values, atol=1e-9))
    gate = {"n_tumors": n_tum, "order_178_178": bool(gate_order),
            "kras_values_match_1e-9": gate_kras_val,
            "purity_col_matches_v4r_purity_1e-9": gate_purity_col,
            "nan_in_scores": False}
    gate["open"] = bool(gate_order and gate_kras_val and gate_purity_col)
    out["gate_J"] = gate
    print("Porte J :", gate)
    assert gate["open"], "PORTE J FERMÉE — arrêt"

    # Scores alignés sur les lignes immunitaires (ordre KRAS brut croissant)
    imm_vals = imm[IMM_GENES].values.astype(float)
    assert np.allclose(imm_vals,
                       logmat.loc[IMM_GENES, samples].T.values, atol=1e-9), \
        "valeurs immunitaires non reproduites depuis le tarball — arrêt"
    out["gate_J"]["immune_values_match_tarball_1e-9"] = True
    print("Valeurs immunitaires reproduites depuis le tarball à 1e-9 près.")

    scores = pd.DataFrame({"sample": samples, "kras_raw": kras_rec,
                           "score_acineux": ac, "score_ilots": islet})
    scores.to_csv(f"{BASE}/purity_851_scores.csv", index=False)

    n = len(scores)
    r_ac_is = float(np.corrcoef(ac, islet)[0, 1])
    out["scores"] = {
        "score_acineux": {"min": float(ac.min()), "median": float(np.median(ac)),
                          "max": float(ac.max()), "mean": float(ac.mean()),
                          "sd": float(ac.std(ddof=1)),
                          "frac_zero": float((ac == 0).mean())},
        "score_ilots": {"min": float(islet.min()), "median": float(np.median(islet)),
                        "max": float(islet.max()), "mean": float(islet.mean()),
                        "sd": float(islet.std(ddof=1)),
                        "frac_zero": float((islet == 0).mean())},
        "r_acineux_ilots_pearson": r_ac_is,
        "p_acineux_ilots": pearson_p(r_ac_is, n)}
    print(f"Scores : acineux min={ac.min():.2f} méd={np.median(ac):.2f} "
          f"max={ac.max():.2f} frac0={(ac == 0).mean():.3f} ; îlots min={islet.min():.2f} "
          f"méd={np.median(islet):.2f} max={islet.max():.2f} frac0={(islet == 0).mean():.3f} ; "
          f"r(ac,is)={r_ac_is:+.4f}")

    # --- T1 : chaque flux vs pureté ---
    t1 = []
    for j, g in enumerate(IMM_GENES):
        y = imm_vals[:, j]
        r_ac = float(np.corrcoef(y, ac)[0, 1])
        r_is = float(np.corrcoef(y, islet)[0, 1])
        rho_ac = float(stats.spearmanr(y, ac).statistic)
        rho_is = float(stats.spearmanr(y, islet).statistic)
        X = np.column_stack([np.ones(n), ac, islet])
        _, r2 = ols_resid(y.reshape(-1, 1), X)
        t1.append({"gene": g, "r_acineux": r_ac, "p_acineux": pearson_p(r_ac, n),
                   "rho_acineux": rho_ac, "r_ilots": r_is,
                   "p_ilots": pearson_p(r_is, n), "rho_ilots": rho_is,
                   "R2_purity_both": float(r2[0])})
    out["T1_per_flux"] = t1
    out["T1_summary"] = {
        "mean_abs_r_acineux": float(np.mean([abs(d["r_acineux"]) for d in t1])),
        "mean_abs_r_ilots": float(np.mean([abs(d["r_ilots"]) for d in t1])),
        "mean_abs_rho_acineux": float(np.mean([abs(d["rho_acineux"]) for d in t1])),
        "mean_abs_rho_ilots": float(np.mean([abs(d["rho_ilots"]) for d in t1])),
        "median_R2_purity_both": float(np.median([d["R2_purity_both"] for d in t1])),
        "max_R2_purity_both": float(np.max([d["R2_purity_both"] for d in t1]))}
    print("T1 résumé :", out["T1_summary"])

    # --- T2 : matrice intra-famille brute vs résidus ---
    imm_df = pd.DataFrame(imm_vals, columns=IMM_GENES)
    Xboth = np.column_stack([np.ones(n), ac, islet])
    Xac = np.column_stack([np.ones(n), ac])
    Xis = np.column_stack([np.ones(n), islet])
    res_both, _ = ols_resid(imm_vals, Xboth)
    res_ac, _ = ols_resid(imm_vals, Xac)
    res_is, _ = ols_resid(imm_vals, Xis)
    t2 = {"brut": mat_stats(imm_df),
          "resid_both": mat_stats(pd.DataFrame(res_both, columns=IMM_GENES)),
          "resid_acineux_only": mat_stats(pd.DataFrame(res_ac, columns=IMM_GENES)),
          "resid_ilots_only": mat_stats(pd.DataFrame(res_is, columns=IMM_GENES))}
    out["T2_matrix"] = t2
    b = t2["brut"]["pearson_mean_abs_r"]
    rb = t2["resid_both"]["pearson_mean_abs_r"]
    out["T2_summary"] = {"drop_both_pct": float(100 * (b - rb) / b),
                         "drop_ac_only_pct": float(100 * (b - t2["resid_acineux_only"]["pearson_mean_abs_r"]) / b),
                         "drop_is_only_pct": float(100 * (b - t2["resid_ilots_only"]["pearson_mean_abs_r"]) / b)}
    print("T2 :", {k: round(v["pearson_mean_abs_r"], 4) for k, v in t2.items()},
          "chute both %:", round(out["T2_summary"]["drop_both_pct"], 1))

    # --- T3 : couplage par contrôle, brut vs résiduel + prédiction §8.48 ---
    def coupling(mat_df):
        c = mat_df.corr(method="pearson").values
        return {g: float(np.mean([abs(c[i, j]) for j in range(12) if j != i]))
                for i, g in enumerate(IMM_GENES)}
    c_brut = coupling(imm_df)
    c_res = coupling(pd.DataFrame(res_both, columns=IMM_GENES))
    t3 = []
    for g in IMM_GENES:
        t3.append({"control": g, "C_brut": c_brut[g], "C_resid": c_res[g],
                   "d_pred_brut": -0.175 + 1.705 * c_brut[g],
                   "d_pred_resid": -0.175 + 1.705 * c_res[g]})
    out["T3_coupling"] = t3
    out["T3_summary"] = {
        "mean_C_brut": float(np.mean(list(c_brut.values()))),
        "mean_C_resid": float(np.mean(list(c_res.values()))),
        "mean_d_pred_brut": float(np.mean([d["d_pred_brut"] for d in t3])),
        "mean_d_pred_resid": float(np.mean([d["d_pred_resid"] for d in t3]))}
    print("T3 résumé :", out["T3_summary"])

    # --- T4 : stratification médiane ---
    t4 = {}
    for name, s in [("acineux", ac), ("ilots", islet)]:
        med = float(np.median(s))
        hi = s >= med
        lo = ~hi
        t4[name] = {"median": med, "n_hi": int(hi.sum()), "n_lo": int(lo.sum()),
                    "hi": mat_stats(imm_df[hi]),
                    "lo": mat_stats(imm_df[lo])}
    out["T4_stratification"] = t4
    print("T4 :", {k: (round(v["hi"]["pearson_mean_abs_r"], 4),
                       round(v["lo"]["pearson_mean_abs_r"], 4)) for k, v in t4.items()})

    # --- Sauvegarde ---
    with open(f"{BASE}/purity_851_results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    rows = []
    for d in t1:
        rows.append({"test": "T1", "gene": d["gene"], "r_acineux": d["r_acineux"],
                     "p_acineux": d["p_acineux"], "r_ilots": d["r_ilots"],
                     "p_ilots": d["p_ilots"], "R2_purity_both": d["R2_purity_both"]})
    pd.DataFrame(rows).to_csv(f"{BASE}/purity_851_results.csv", index=False)
    print("Écrit : purity_851_scores.csv, purity_851_results.json/.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
