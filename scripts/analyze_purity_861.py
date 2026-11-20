#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.61 — Porte S, jointure, T1''-T4'' : pureté par méthylation vs
corrélation immunitaire. Miroir de analyze_purity_855.py (mêmes définitions).
Protocole gelé : PROTOCOL_methylation_purity_861.md
(SHA 93f4f777f217d9a03c01b1b79397ed70e59567e53edaf4231864e9c6a50e0993).
Source : même Table S1 de Raphael et al. 2017 que le §8.55, via pdacR
TCGA_PAAD.rds (SHA 52020679…ea76) ; colonne DNA.hypermethylation.mode.purity
lue dans purity_855_sampinfo.csv (SHA 7a09dde3…b014), sans transformation.
Re-téléchargement de vérification du RDS le 20 nov. 2026 : SHA identique
(52020679…ea76), 12 311 529 octets — source toujours accessible.
Annexe leucocytes (DNA.methylation.leukocyte.percent.estimate) :
descriptive seulement, hors verdict, aucun run. Aucun run ici.
Sorties : purity_861_external.csv, purity_861_results.json/.csv (T1''-T4'').
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

IMM_GENES = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
             "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]


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
    }
    print("SHA :", checks)
    assert all(checks.values()), f"SHA non conforme : {checks}"
    out["sha_checks"] = checks

    # --- Porte S / jointure (protocole §3-§4 : clé 15 premiers caractères) ---
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
    meth_col = m["DNA.hypermethylation.mode.purity"]
    n_meth = int(meth_col.notna().sum())
    in_range = bool(((meth_col.dropna() >= 0) & (meth_col.dropna() <= 1)).all())
    gate = {"n_ours": 178, "n_externes": 181, "matched_barcode": n_matched,
            "methylation_non_null": n_meth,
            "methylation_dans_[0,1]": in_range,
            "unmatched_ours": m[m["_merge"] == "left_only"]["sample"].tolist(),
            "externes_hors_projet": si[~si["key15"].isin(axis["key15"])]["Tumor.Sample.ID"].tolist(),
            "sans_methylation": m[m["DNA.hypermethylation.mode.purity"].isna()]["sample"].tolist()}
    gate["open"] = bool(n_matched == 178 and n_meth >= 100 and in_range)
    out["gate_S"] = gate
    print("Porte S / jointure :", {k: v for k, v in gate.items()
                                   if k not in ("unmatched_ours", "externes_hors_projet",
                                                "sans_methylation")})
    print("  externes hors projet :", gate["externes_hors_projet"])
    print("  sans méthylation (n=%d) : %s" % (len(gate["sans_methylation"]),
                                              gate["sans_methylation"][:5]))
    assert gate["open"], "PORTE S FERMÉE — arrêt"

    # --- Sous-ensemble apparié avec METH (n=150), ordre KRAS brut conservé ---
    sub = m.dropna(subset=["DNA.hypermethylation.mode.purity"]).reset_index(drop=True)
    n = len(sub)
    assert n == 150, f"n apparié attendu 150, obtenu {n}"
    samples = sub["sample"].tolist()
    meth = sub["DNA.hypermethylation.mode.purity"].values.astype(float)
    absol = sub["ABSOLUTE.Purity"].values.astype(float)
    n_abs = int(pd.Series(absol).notna().sum())
    imm_idx = imm.set_index(axis["sample"].values)
    Y = imm_idx.loc[samples, IMM_GENES].values.astype(float)
    assert not np.isnan(Y).any() and not np.isnan(meth).any()
    ext = pd.DataFrame({"sample": samples, "key15": sub["key15"].values,
                        "purity_methylation": meth,
                        "purity_absolute": absol,
                        "leukocyte_methyl_percent": sub["DNA.methylation.leukocyte.percent.estimate"].values,
                        "purity_class": sub["Purity.Class.high.or.low"].values,
                        "pathologist_cellularity": sub["Pathologist.Reviewed.Tumor.Cellularity"].values})
    ext.to_csv(f"{BASE}/purity_861_external.csv", index=False)
    out["matched"] = {"n": n, "n_with_absolute": n_abs,
                      "methylation": {"min": float(meth.min()), "median": float(np.median(meth)),
                                      "mean": float(meth.mean()), "sd": float(meth.std(ddof=1)),
                                      "max": float(meth.max())}}
    print(f"Appariées METH : n={n} (dont ABSOLUTE n={n_abs}) min={meth.min():.4f} "
          f"méd={np.median(meth):.4f} moy={meth.mean():.4f} max={meth.max():.4f}")

    # --- Cohérence (vérifications, pas des tests du verdict) ---
    both = ext.dropna(subset=["purity_absolute", "purity_methylation"])
    r_meth_abs = float(np.corrcoef(both["purity_absolute"], both["purity_methylation"])[0, 1])
    hi = ext[ext["purity_class"] == "high"]["purity_methylation"]
    lo = ext[ext["purity_class"] == "low"]["purity_methylation"]
    leuko = ext["leukocyte_methyl_percent"].values.astype(float)
    r_meth_leuko = float(np.corrcoef(meth, leuko)[0, 1])
    r_abs_leuko = float(np.corrcoef(both["purity_absolute"],
                                    both["leukocyte_methyl_percent"])[0, 1])
    out["coherence"] = {
        "methylation_vs_absolute": {"n": int(len(both)), "r_pearson": r_meth_abs,
                                    "p": pearson_p(r_meth_abs, len(both)),
                                    "reference_855": 0.8556},
        "purity_class_vs_methylation": {"n_high": int(len(hi)), "n_low": int(len(lo)),
                                        "high_min": float(hi.min()), "high_max": float(hi.max()),
                                        "low_min": float(lo.min()), "low_max": float(lo.max()),
                                        "high_mean": float(hi.mean()), "low_mean": float(lo.mean())},
        "methylation_vs_leukocyte": {"n": int(len(ext)), "r_pearson": r_meth_leuko,
                                     "p": pearson_p(r_meth_leuko, len(ext))},
        "absolute_vs_leukocyte": {"n": int(len(both)), "r_pearson": r_abs_leuko,
                                  "p": pearson_p(r_abs_leuko, len(both))},
    }
    print(f"Cohérence : METH vs ABSOLUTE r={r_meth_abs:.4f} (n={len(both)}, réf. §8.55 0,8556) ; "
          f"classe high METH [{hi.min():.4f},{hi.max():.4f}] (n={len(hi)}), "
          f"low [{lo.min():.4f},{lo.max():.4f}] (n={len(lo)}) ; "
          f"METH vs leucocytes r={r_meth_leuko:.4f} ; ABSOLUTE vs leucocytes r={r_abs_leuko:.4f}")

    # --- T1'' : chaque flux vs METH ---
    t1 = []
    for j, g in enumerate(IMM_GENES):
        y = Y[:, j]
        r_m = float(np.corrcoef(y, meth)[0, 1])
        rho_m = float(stats.spearmanr(y, meth).statistic)
        X = np.column_stack([np.ones(n), meth])
        _, r2 = ols_resid(y.reshape(-1, 1), X)
        t1.append({"gene": g, "r_methylation": r_m, "p_methylation": pearson_p(r_m, n),
                   "rho_methylation": rho_m, "R2_methylation": float(r2[0])})
    out["T1_per_flux"] = t1
    out["T1_summary"] = {
        "mean_abs_r_methylation": float(np.mean([abs(d["r_methylation"]) for d in t1])),
        "mean_abs_rho_methylation": float(np.mean([abs(d["rho_methylation"]) for d in t1])),
        "median_R2_methylation": float(np.median([d["R2_methylation"] for d in t1])),
        "max_R2_methylation": float(np.max([d["R2_methylation"] for d in t1]))}
    print("T1'' résumé :", out["T1_summary"])

    # --- T2'' : matrice intra-famille brute (n=150) vs résidus [1, METH] ---
    imm_df = pd.DataFrame(Y, columns=IMM_GENES)
    Xmeth = np.column_stack([np.ones(n), meth])
    res_meth, _ = ols_resid(Y, Xmeth)
    t2 = {"brut_n150": mat_stats(imm_df),
          "resid_methylation": mat_stats(pd.DataFrame(res_meth, columns=IMM_GENES))}
    b = t2["brut_n150"]["pearson_mean_abs_r"]
    rb = t2["resid_methylation"]["pearson_mean_abs_r"]
    out["T2_matrix"] = t2
    out["T2_summary"] = {"drop_methylation_pct": float(100 * (b - rb) / b)}
    # Sensibilité conjointe [ABSOLUTE, METH] sur les n=149 communes.
    sub149 = ext.dropna(subset=["purity_absolute"]).reset_index(drop=True)
    Y149 = imm_idx.loc[sub149["sample"].tolist(), IMM_GENES].values.astype(float)
    Xboth = np.column_stack([np.ones(len(sub149)),
                             sub149["purity_absolute"].values.astype(float),
                             sub149["purity_methylation"].values.astype(float)])
    res_both, _ = ols_resid(Y149, Xboth)
    t2s = {"brut_n149": mat_stats(pd.DataFrame(Y149, columns=IMM_GENES)),
           "resid_absolute_methylation": mat_stats(pd.DataFrame(res_both, columns=IMM_GENES))}
    b149 = t2s["brut_n149"]["pearson_mean_abs_r"]
    rb149 = t2s["resid_absolute_methylation"]["pearson_mean_abs_r"]
    out["T2_sensitivity_both"] = t2s
    out["T2_sensitivity_summary"] = {"n": int(len(sub149)),
                                     "drop_both_pct": float(100 * (b149 - rb149) / b149)}
    imm178 = pd.DataFrame(imm[IMM_GENES].values.astype(float), columns=IMM_GENES)
    out["T2_reference_178"] = mat_stats(imm178)
    print(f"T2'' : brut n=150 {b:.4f} -> résid METH {rb:.4f} "
          f"(chute {out['T2_summary']['drop_methylation_pct']:.1f} %) ; "
          f"sensibilité conjointe n=149 : {b149:.4f} -> {rb149:.4f} "
          f"(chute {out['T2_sensitivity_summary']['drop_both_pct']:.1f} %) ; "
          f"brut n=178 (réf.) {out['T2_reference_178']['pearson_mean_abs_r']:.4f}")

    # --- T3'' : couplage par contrôle, brut vs résiduel + prédiction §8.48 ---
    def coupling(mat_df):
        c = mat_df.corr(method="pearson").values
        return {g: float(np.mean([abs(c[i, j]) for j in range(12) if j != i]))
                for i, g in enumerate(IMM_GENES)}
    c_brut = coupling(imm_df)
    c_res = coupling(pd.DataFrame(res_meth, columns=IMM_GENES))
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
    print("T3'' résumé :", out["T3_summary"])

    # --- T4'' : stratification médiane METH ---
    med = float(np.median(meth))
    hi_m = meth >= med
    lo_m = ~hi_m
    t4 = {"methylation": {"median": med, "n_hi": int(hi_m.sum()), "n_lo": int(lo_m.sum()),
                          "hi": mat_stats(imm_df[hi_m]),
                          "lo": mat_stats(imm_df[lo_m])}}
    out["T4_stratification"] = t4
    print("T4'' :", {k: (round(v["hi"]["pearson_mean_abs_r"], 4),
                         round(v["lo"]["pearson_mean_abs_r"], 4)) for k, v in t4.items()})

    # --- Annexe leucocytes (descriptive seulement, hors verdict) ---
    t_leuko = []
    for j, g in enumerate(IMM_GENES):
        y = Y[:, j]
        r_l = float(np.corrcoef(y, leuko)[0, 1])
        rho_l = float(stats.spearmanr(y, leuko).statistic)
        t_leuko.append({"gene": g, "r_leukocyte": r_l, "p_leukocyte": pearson_p(r_l, n),
                        "rho_leukocyte": rho_l})
    out["annex_leukocyte"] = {
        "per_flux": t_leuko,
        "mean_abs_r_leukocyte": float(np.mean([abs(d["r_leukocyte"]) for d in t_leuko])),
        "note": "Descriptif seulement : la fraction leucocytaire par méthylation "
                "est une piste d'infiltration indépendante (non circulaire), "
                "mais elle ne fait pas partie du verdict H1-meth/H0-meth "
                "(protocole §2, §7). Aucun run sur cette colonne."}
    print("Annexe leucocytes : moyenne |r| = %.4f" % out["annex_leukocyte"]["mean_abs_r_leukocyte"])

    # --- Sauvegarde ---
    with open(f"{BASE}/purity_861_results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    rows = []
    for d in t1:
        rows.append({"test": "T1''", "gene": d["gene"], "r_methylation": d["r_methylation"],
                     "p_methylation": d["p_methylation"], "rho_methylation": d["rho_methylation"],
                     "R2_methylation": d["R2_methylation"]})
    pd.DataFrame(rows).to_csv(f"{BASE}/purity_861_results.csv", index=False)
    print("Écrit : purity_861_external.csv, purity_861_results.json/.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
