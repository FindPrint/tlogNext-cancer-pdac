#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.67 — Test décisif sur la fraction leucocytaire : Porte L, jointure,
T1-L2–T4-L, sensibilités T2-L-imog / T2-J1 / T2-J2, prédictions T3-L2.
Miroir de analyze_purity_861.py (mêmes définitions).
Protocole gelé : PROTOCOL_leukocyte_decisive_867.md
(SHA 571adf826f455b8dfd49c63f2c0e94fc73a7ae03a6e98b5bfda2bb0648ae59ad).
Sources (toutes déjà détenues, aucun nouveau téléchargement) :
fraction leucocytaire par méthylation = colonne
DNA.methylation.leukocyte.percent.estimate du sampInfo transcrit au
§8.55 (purity_855_sampinfo.csv, SHA 7a09dde3…b014), issu de la Table S1
de Raphael et al. 2017 via pdacR TCGA_PAAD.rds (SHA 52020679…ea76).
Égalité assertée avec les deux transcriptions détenues
(purity_861_external.csv, deconvolution_860_external.csv).
Re-vérifications gelées : T1-L et T2-L du §8.60 (bras L) doivent
reproduire à ± 0,005 près (moyenne |r| = 0,5456 ; 0,5035 -> 0,3372),
sinon arrêt. Aucun run ici.
Sorties : leukocyte_867_external.csv, leukocyte_867_results.json/.csv,
leukocyte_867_predictions.json (T3-L2, AVANT les runs).
"""
import hashlib
import json

import numpy as np
import pandas as pd
from scipy import stats

BASE = "/home/hatch/workspace/runs/pdac-v6"
IMMUNE_SHA = "66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e"
AXIS_SHA = "31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d"
V62_SHA = "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"
RDS_SHA = "52020679350d1539d7516f7d38f7bf09e510225eba2f228a4fe874f3c496ea76"
SAMPINFO_SHA = "7a09dde3d374d1afb64f1d1d053193fc884c04d62e63e519fcf4dbf17378b014"
P861_EXT_SHA = "cf127ef7310b35483c7fa7712fe69bf07a858726fb44f2d4e05613acc575d24b"
D860_EXT_SHA = "438d677aded8eaf74504f8bd89bfc2e578df32b4b31c64e94e64120b0f22d9cf"
S854_SHA = "628732ecbcc30a3281b0df7a5039ec2520a1c5f1a1ae9ce412c4d0d7caf78aa7"
P855_EXT_SHA = "03f34fe07a18ff106e21ce9028ef9ff60d3d95889c3064898442246e486fbd6f"

IMM_GENES = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
             "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
# Références §8.60 bras L (re-vérification, tolérance gelée ± 0,005).
REF_T1_MEAN_ABS_R = 0.5456
REF_T2_BRUT = 0.5035
REF_T2_RESID = 0.3372
TOL_REPRO = 0.005


def sha(path):
    h = hashlib.sha256()
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
    checks = {
        "immune": sha(f"{BASE}/pdac_immune_tcga_fluxes.csv") == IMMUNE_SHA,
        "axis": sha(f"{BASE}/immune_kras_order_tcga.csv") == AXIS_SHA,
        "v62": sha("/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py") == V62_SHA,
        "pdacr_rds": sha(f"{BASE}/data/pdacR_TCGA_PAAD.rds") == RDS_SHA,
        "sampinfo_csv": sha(f"{BASE}/purity_855_sampinfo.csv") == SAMPINFO_SHA,
        "purity861_external": sha(f"{BASE}/purity_861_external.csv") == P861_EXT_SHA,
        "deconvolution860_external": sha(f"{BASE}/deconvolution_860_external.csv") == D860_EXT_SHA,
        "infiltration854_scores": sha(f"{BASE}/infiltration_854_scores.csv") == S854_SHA,
        "purity855_external": sha(f"{BASE}/purity_855_external.csv") == P855_EXT_SHA,
    }
    print("SHA :", checks)
    assert all(checks.values()), f"SHA non conforme : {checks}"
    out["sha_checks"] = checks

    # --- Porte L / jointure (protocole §3-§4 : clé 15 premiers caractères) ---
    si = pd.read_csv(f"{BASE}/purity_855_sampinfo.csv")
    axis = pd.read_csv(f"{BASE}/immune_kras_order_tcga.csv")
    imm = pd.read_csv(f"{BASE}/pdac_immune_tcga_fluxes.csv")
    assert list(imm.columns[1:]) == IMM_GENES
    assert len(axis) == 178 and len(imm) == 178
    si["key15"] = si["Tumor.Sample.ID"].str[:15]
    axis["key15"] = axis["sample"].str[:15]
    assert si["key15"].nunique() == len(si) == 181, "collision de clé15 côté externe"
    assert axis["key15"].nunique() == 178, "collision de clé15 côté projet"
    m = axis.merge(si, on="key15", how="left", indicator=True)
    n_matched = int((m["_merge"] == "both").sum())
    leuko_col = m["DNA.methylation.leukocyte.percent.estimate"]
    n_leuko = int(leuko_col.notna().sum())
    in_range = bool(((leuko_col.dropna() >= 0) & (leuko_col.dropna() <= 1)).all())
    gate = {"n_ours": 178, "n_externes": 181, "matched_barcode": n_matched,
            "leukocyte_non_null": n_leuko,
            "leukocyte_dans_[0,1]": in_range,
            "unmatched_ours": m[m["_merge"] == "left_only"]["sample"].tolist(),
            "externes_hors_projet": si[~si["key15"].isin(axis["key15"])]["Tumor.Sample.ID"].tolist(),
            "sans_leukocyte": m[m["DNA.methylation.leukocyte.percent.estimate"].isna()]["sample"].tolist()}
    gate["open"] = bool(n_matched == 178 and n_leuko >= 100 and in_range)
    out["gate_L"] = gate
    print("Porte L / jointure :", {k: v for k, v in gate.items()
                                   if k not in ("unmatched_ours", "externes_hors_projet",
                                                "sans_leukocyte")})
    print("  externes hors projet :", gate["externes_hors_projet"])
    print("  sans leucocytes (n=%d) : %s" % (len(gate["sans_leukocyte"]),
                                             gate["sans_leukocyte"][:5]))
    assert gate["open"], "PORTE L FERMÉE — arrêt"

    # --- Sous-ensemble apparié avec fraction leucocytaire, ordre KRAS brut conservé ---
    sub = m.dropna(subset=["DNA.methylation.leukocyte.percent.estimate"]).reset_index(drop=True)
    n = len(sub)
    assert n == 150, f"n apparié attendu 150, obtenu {n}"
    samples = sub["sample"].tolist()
    leuko = sub["DNA.methylation.leukocyte.percent.estimate"].values.astype(float)
    meth = sub["DNA.hypermethylation.mode.purity"].values.astype(float)
    absol = sub["ABSOLUTE.Purity"].values.astype(float)
    n_abs = int(pd.Series(absol).notna().sum())
    imm_idx = imm.set_index(axis["sample"].values)
    Y = imm_idx.loc[samples, IMM_GENES].values.astype(float)
    assert not np.isnan(Y).any() and not np.isnan(leuko).any()

    # --- Égalité assertée avec les deux transcriptions détenues ---
    p861 = pd.read_csv(f"{BASE}/purity_861_external.csv").set_index("sample")
    d860 = pd.read_csv(f"{BASE}/deconvolution_860_external.csv").set_index("sample")
    s854 = pd.read_csv(f"{BASE}/infiltration_854_scores.csv").set_index("sample")
    p855 = pd.read_csv(f"{BASE}/purity_855_external.csv").set_index("sample")
    leuko_p861 = p861.loc[samples, "leukocyte_methyl_percent"].values.astype(float)
    leuko_d860 = d860.loc[samples, "Leukocyte_fraction_methylation_Raphael"].values.astype(float)
    eq_p861 = bool(np.allclose(leuko, leuko_p861, atol=1e-9, equal_nan=True))
    eq_d860 = bool(np.allclose(leuko, leuko_d860, atol=1e-9, equal_nan=True))
    out["transcription_checks"] = {"egal_purity_861_external": eq_p861,
                                   "egal_deconvolution_860_external": eq_d860}
    print("Transcriptions leucocytes : = purity_861_external :", eq_p861,
          "; = deconvolution_860_external :", eq_d860)
    assert eq_p861 and eq_d860, "DIVERGENCE DE TRANSCRIPTION — arrêt"

    lf_imog = d860.loc[samples, "Leukocyte_fraction_imogimap"].values.astype(float)
    imm_score = s854.loc[samples, "ImmuneScore"].values.astype(float)
    absol_p855 = p855["purity_absolute"].reindex(samples).values.astype(float)
    # Une tumeur (TCGA-2J-AAB9-01A-11R-A41B-07, §8.61.2) a METH/leuco mais
    # pas ABSOLUTE : purity_855_external.csv ne la contient pas (149 lignes).
    assert int(pd.Series(absol_p855).notna().sum()) == n_abs
    assert not np.isnan(lf_imog).any() and not np.isnan(imm_score).any()
    assert np.allclose(absol[~np.isnan(absol)], absol_p855[~np.isnan(absol_p855)], atol=1e-9), \
        "ABSOLUTE sampInfo vs purity_855_external diverge"
    ext = pd.DataFrame({"sample": samples, "key15": sub["key15"].values,
                        "leukocyte_methylation": leuko,
                        "leukocyte_imogimap": lf_imog,
                        "ImmuneScore_854": imm_score,
                        "purity_absolute": absol,
                        "purity_methylation": meth})
    ext.to_csv(f"{BASE}/leukocyte_867_external.csv", index=False)
    out["matched"] = {"n": n, "n_with_absolute": n_abs,
                      "leukocyte": {"min": float(leuko.min()), "median": float(np.median(leuko)),
                                    "mean": float(leuko.mean()), "sd": float(leuko.std(ddof=1)),
                                    "max": float(leuko.max())},
                      "leukocyte_imogimap": {"min": float(lf_imog.min()),
                                             "median": float(np.median(lf_imog)),
                                             "mean": float(lf_imog.mean()),
                                             "sd": float(lf_imog.std(ddof=1)),
                                             "max": float(lf_imog.max())}}
    print(f"Appariées leucocytes : n={n} (dont ABSOLUTE n={n_abs}) min={leuko.min():.4f} "
          f"méd={np.median(leuko):.4f} moy={leuko.mean():.4f} ET={leuko.std(ddof=1):.4f} "
          f"max={leuko.max():.4f}")
    r_leuko_imog = float(np.corrcoef(leuko, lf_imog)[0, 1])
    out["coherence"] = {"leukocyte_methylation_vs_imogimap":
                        {"n": n, "r_pearson": r_leuko_imog,
                         "p": pearson_p(r_leuko_imog, n), "reference_860": 0.9947},
                        "leukocyte_vs_ImmuneScore":
                        {"n": n, "r_pearson": float(np.corrcoef(leuko, imm_score)[0, 1])},
                        "leukocyte_vs_absolute":
                        {"n": n_abs, "r_pearson": float(np.corrcoef(
                            leuko[~np.isnan(absol)], absol[~np.isnan(absol)])[0, 1])}}
    print(f"Cohérence : leuco méthylation vs imogimap r={r_leuko_imog:.4f} "
          f"(réf. §8.60 0,9947) ; vs ImmuneScore "
          f"r={out['coherence']['leukocyte_vs_ImmuneScore']['r_pearson']:.4f} ; "
          f"vs ABSOLUTE r={out['coherence']['leukocyte_vs_absolute']['r_pearson']:.4f}")

    # --- T1-L2 : chaque flux vs fraction leucocytaire (re-vérification §8.60) ---
    imm_df = pd.DataFrame(Y, columns=IMM_GENES)
    t1 = []
    for j, g in enumerate(IMM_GENES):
        y = Y[:, j]
        r_l = float(np.corrcoef(y, leuko)[0, 1])
        rho_l = float(stats.spearmanr(y, leuko).statistic)
        _, r2 = ols_resid(y.reshape(-1, 1), np.column_stack([np.ones(n), leuko]))
        t1.append({"gene": g, "r_leukocyte": r_l, "p_leukocyte": pearson_p(r_l, n),
                   "rho_leukocyte": rho_l, "R2_leukocyte": float(r2[0])})
    out["T1_per_flux"] = t1
    mean_abs_r = float(np.mean([abs(d["r_leukocyte"]) for d in t1]))
    out["T1_summary"] = {
        "mean_abs_r_leukocyte": mean_abs_r,
        "mean_abs_rho_leukocyte": float(np.mean([abs(d["rho_leukocyte"]) for d in t1])),
        "median_R2_leukocyte": float(np.median([d["R2_leukocyte"] for d in t1])),
        "max_R2_leukocyte": float(np.max([d["R2_leukocyte"] for d in t1])),
        "reference_860_mean_abs_r": REF_T1_MEAN_ABS_R,
        "ecart_vs_860": float(mean_abs_r - REF_T1_MEAN_ABS_R)}
    print("T1-L2 résumé :", out["T1_summary"])
    assert abs(mean_abs_r - REF_T1_MEAN_ABS_R) <= TOL_REPRO, \
        f"T1-L2 ne reproduit pas le §8.60 : {mean_abs_r} vs {REF_T1_MEAN_ABS_R}"

    # --- T2-L2 : matrice brute vs résidus [1, leuco] (re-vérification §8.60) ---
    Xleu = np.column_stack([np.ones(n), leuko])
    res_leu, _ = ols_resid(Y, Xleu)
    res_leu_df = pd.DataFrame(res_leu, columns=IMM_GENES)
    t2 = {"brut_n150": mat_stats(imm_df),
          "resid_leukocyte": mat_stats(res_leu_df)}
    b = t2["brut_n150"]["pearson_mean_abs_r"]
    rb = t2["resid_leukocyte"]["pearson_mean_abs_r"]
    out["T2_matrix"] = t2
    out["T2_summary"] = {"drop_leukocyte_pct": float(100 * (b - rb) / b),
                         "reference_860_brut": REF_T2_BRUT,
                         "reference_860_resid": REF_T2_RESID,
                         "ecart_brut_vs_860": float(b - REF_T2_BRUT),
                         "ecart_resid_vs_860": float(rb - REF_T2_RESID)}
    print(f"T2-L2 : brut n=150 {b:.4f} -> résid leuco {rb:.4f} "
          f"(chute {out['T2_summary']['drop_leukocyte_pct']:.1f} %) ; "
          f"réf. §8.60 {REF_T2_BRUT:.4f} -> {REF_T2_RESID:.4f}")
    assert abs(b - REF_T2_BRUT) <= TOL_REPRO and abs(rb - REF_T2_RESID) <= TOL_REPRO, \
        "T2-L2 ne reproduit pas le §8.60 à ± 0,005 près — arrêt"
    imm178 = pd.DataFrame(imm[IMM_GENES].values.astype(float), columns=IMM_GENES)
    out["T2_reference_178"] = mat_stats(imm178)

    # --- T2-L-imog : sensibilité, résidus [1, LF imogimap], mêmes n ---
    Ximog = np.column_stack([np.ones(n), lf_imog])
    res_imog, _ = ols_resid(Y, Ximog)
    t2i = {"resid_leukocyte_imogimap": mat_stats(pd.DataFrame(res_imog, columns=IMM_GENES))}
    rb_imog = t2i["resid_leukocyte_imogimap"]["pearson_mean_abs_r"]
    out["T2_imog"] = t2i
    out["T2_imog_summary"] = {"drop_imogimap_pct": float(100 * (b - rb_imog) / b)}
    print(f"T2-L-imog : brut {b:.4f} -> résid LF imogimap {rb_imog:.4f} "
          f"(chute {out['T2_imog_summary']['drop_imogimap_pct']:.1f} %)")

    # --- T2-J1 : conjointe [leuco, ImmuneScore], mêmes n=150 ---
    Ximm = np.column_stack([np.ones(n), imm_score])
    res_imm, _ = ols_resid(Y, Ximm)
    Xjoint1 = np.column_stack([np.ones(n), leuko, imm_score])
    res_joint1, _ = ols_resid(Y, Xjoint1)
    r_imm = mat_stats(pd.DataFrame(res_imm, columns=IMM_GENES))["pearson_mean_abs_r"]
    r_joint1 = mat_stats(pd.DataFrame(res_joint1, columns=IMM_GENES))["pearson_mean_abs_r"]
    out["T2_J1"] = {"brut_n150": b, "resid_ImmuneScore_seul": r_imm,
                    "resid_leukocyte_seul": rb, "resid_conjoint": r_joint1,
                    "drop_ImmuneScore_seul_pct": float(100 * (b - r_imm) / b),
                    "drop_conjoint_pct": float(100 * (b - r_joint1) / b),
                    "gain_conjoint_vs_ImmuneScore_seul_points":
                        float(100 * (r_imm - r_joint1) / b)}
    print(f"T2-J1 : brut {b:.4f} ; ImmuneScore seul -> {r_imm:.4f} "
          f"(chute {out['T2_J1']['drop_ImmuneScore_seul_pct']:.1f} %) ; "
          f"conjoint [leuco, ImmuneScore] -> {r_joint1:.4f} "
          f"(chute {out['T2_J1']['drop_conjoint_pct']:.1f} %, gain "
          f"{out['T2_J1']['gain_conjoint_vs_ImmuneScore_seul_points']:.1f} points)")

    # --- T2-J2 : conjointe [leuco, ABSOLUTE], n communes (attendu 149) ---
    sub149 = ext.dropna(subset=["purity_absolute"]).reset_index(drop=True)
    Y149 = imm_idx.loc[sub149["sample"].tolist(), IMM_GENES].values.astype(float)
    leuko149 = sub149["leukocyte_methylation"].values.astype(float)
    absol149 = sub149["purity_absolute"].values.astype(float)
    b149 = mat_stats(pd.DataFrame(Y149, columns=IMM_GENES))["pearson_mean_abs_r"]
    r_abs149, _ = ols_resid(Y149, np.column_stack([np.ones(len(sub149)), absol149]))
    r_leu149, _ = ols_resid(Y149, np.column_stack([np.ones(len(sub149)), leuko149]))
    r_j149, _ = ols_resid(Y149, np.column_stack([np.ones(len(sub149)), leuko149, absol149]))
    m_abs149 = mat_stats(pd.DataFrame(r_abs149, columns=IMM_GENES))["pearson_mean_abs_r"]
    m_leu149 = mat_stats(pd.DataFrame(r_leu149, columns=IMM_GENES))["pearson_mean_abs_r"]
    m_j149 = mat_stats(pd.DataFrame(r_j149, columns=IMM_GENES))["pearson_mean_abs_r"]
    out["T2_J2"] = {"n": int(len(sub149)), "brut": b149,
                    "resid_absolute_seul": m_abs149, "resid_leukocyte_seul": m_leu149,
                    "resid_conjoint": m_j149,
                    "drop_absolute_seul_pct": float(100 * (b149 - m_abs149) / b149),
                    "drop_leukocyte_seul_pct": float(100 * (b149 - m_leu149) / b149),
                    "drop_conjoint_pct": float(100 * (b149 - m_j149) / b149),
                    "gain_conjoint_vs_absolute_seul_points":
                        float(100 * (m_abs149 - m_j149) / b149)}
    print(f"T2-J2 (n={len(sub149)}) : brut {b149:.4f} ; ABSOLUTE seul -> {m_abs149:.4f} "
          f"(chute {out['T2_J2']['drop_absolute_seul_pct']:.1f} %) ; "
          f"leuco seul -> {m_leu149:.4f} ; conjoint -> {m_j149:.4f} "
          f"(chute {out['T2_J2']['drop_conjoint_pct']:.1f} %, gain "
          f"{out['T2_J2']['gain_conjoint_vs_absolute_seul_points']:.1f} points)")

    # --- T3-L2 : couplage par contrôle, brut vs résiduel + prédictions §8.48 ---
    def coupling(mat_df):
        c = mat_df.corr(method="pearson").values
        return {g: float(np.mean([abs(c[i, j]) for j in range(12) if j != i]))
                for i, g in enumerate(IMM_GENES)}
    c_brut = coupling(imm_df)
    c_res = coupling(res_leu_df)
    t3 = []
    for g in IMM_GENES:
        t3.append({"control": g, "C_brut": c_brut[g], "C_resid": c_res[g],
                   "d_pred_brut": -0.175 + 1.705 * c_brut[g],
                   "d_pred_resid": -0.175 + 1.705 * c_res[g]})
    out["T3_coupling"] = t3
    # Prédictions des runs, AVANT lecture des sorties (protocole §7, T3-L2).
    c_resid_cd8a = c_res["CD8A"]
    d_pred_lres = -0.175 + 1.705 * c_resid_cd8a
    # C_ord : moyenne |r| entre leuco brute et les 12 flux résidualisés.
    c_ord_vals = [abs(float(np.corrcoef(leuko, res_leu[:, j])[0, 1])) for j in range(12)]
    c_ord = float(np.mean(c_ord_vals))
    d_pred_lord = -0.175 + 1.705 * c_ord
    pred = {"L_RES": {"C_resid_CD8A": c_resid_cd8a, "d_pred": d_pred_lres},
            "L_ORD": {"C_ord_leuco_vs_resid": c_ord,
                      "C_ord_par_flux": {g: c_ord_vals[j] for j, g in enumerate(IMM_GENES)},
                      "d_pred": d_pred_lord},
            "references": {"CD8A_brut_IMMROT_ecart": 0.9838, "I_RES": 0.1982,
                           "E_RES": 0.6499, "M_RES": 0.5427, "D_RES_TOP1": 0.7692,
                           "D_LEU": 0.7129}}
    out["T3_predictions"] = pred
    out["T3_summary"] = {
        "mean_C_brut": float(np.mean(list(c_brut.values()))),
        "mean_C_resid": float(np.mean(list(c_res.values()))),
        "mean_d_pred_brut": float(np.mean([d["d_pred_brut"] for d in t3])),
        "mean_d_pred_resid": float(np.mean([d["d_pred_resid"] for d in t3]))}
    print("T3-L2 résumé :", out["T3_summary"])
    print(f"Prédictions AVANT runs : L-RES d_pred={d_pred_lres:+.4f} "
          f"(C_résid CD8A={c_resid_cd8a:.4f}) ; L-ORD d_pred={d_pred_lord:+.4f} "
          f"(C_ord={c_ord:.4f})")
    with open(f"{BASE}/leukocyte_867_predictions.json", "w", encoding="utf-8") as f:
        json.dump(pred, f, indent=2, ensure_ascii=False)

    # --- T4-L : stratification médiane leucocytes ---
    med = float(np.median(leuko))
    sd_global = float(leuko.std(ddof=1))
    hi_m = leuko >= med
    lo_m = ~hi_m
    t4 = {"leukocyte": {"median": med, "sd_global": sd_global,
                        "n_hi": int(hi_m.sum()), "n_lo": int(lo_m.sum()),
                        "sd_hi": float(leuko[hi_m].std(ddof=1)),
                        "sd_lo": float(leuko[lo_m].std(ddof=1)),
                        "sd_hi_pct_global": float(100 * leuko[hi_m].std(ddof=1) / sd_global),
                        "sd_lo_pct_global": float(100 * leuko[lo_m].std(ddof=1) / sd_global),
                        "hi": mat_stats(imm_df[hi_m]),
                        "lo": mat_stats(imm_df[lo_m])}}
    out["T4_stratification"] = t4
    print(f"T4-L : médiane leuco={med:.4f} ; moitié haute n={int(hi_m.sum())} "
          f"cohésion={t4['leukocyte']['hi']['pearson_mean_abs_r']:.4f} "
          f"(ET {t4['leukocyte']['sd_hi_pct_global']:.1f} % du global) ; "
          f"moitié basse n={int(lo_m.sum())} "
          f"cohésion={t4['leukocyte']['lo']['pearson_mean_abs_r']:.4f} "
          f"(ET {t4['leukocyte']['sd_lo_pct_global']:.1f} % du global)")

    # --- Sauvegarde ---
    with open(f"{BASE}/leukocyte_867_results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    rows = []
    for d in t1:
        rows.append({"test": "T1-L2", "gene": d["gene"], "r_leukocyte": d["r_leukocyte"],
                     "p_leukocyte": d["p_leukocyte"], "rho_leukocyte": d["rho_leukocyte"],
                     "R2_leukocyte": d["R2_leukocyte"]})
    pd.DataFrame(rows).to_csv(f"{BASE}/leukocyte_867_results.csv", index=False)
    print("Écrit : leukocyte_867_external.csv, leukocyte_867_results.json/.csv, "
          "leukocyte_867_predictions.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
