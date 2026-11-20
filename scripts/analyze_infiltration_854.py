#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.54 — Porte J, T1-T4 : infiltration ESTIMATE vs corrélation immunitaire.
Protocole gelé : PROTOCOL_infiltration_854.md
(SHA 89be31eda298de193a31360ba4bb7bdd0a2f94ef7a88e8ac37307e846c467918).
Ne modifie ni le pipeline v6.2 ni le livre blanc. Aucun run ici.
Entrées : tarball TCGA-PAAD (MD5 vérifié), base immunitaire TCGA
(pdac_immune_tcga_fluxes.csv), axe immune_kras_order_tcga.csv,
signatures ESTIMATE en clair (infiltration_854_gene_sets.csv),
gènes communs (infiltration_854_common_genes.csv),
matrice de test `ov` (infiltration_854_ov_test.csv).
Sorties : infiltration_854_scores.csv, infiltration_854_immune_resid.csv,
infiltration_854_results.json/.csv (T1-T4).
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd
from scipy import stats

from estimate_ssgsea import estimate_scores, filter_common_genes

BASE = "/home/hatch/workspace/runs/pdac-v6"
DATA = f"{BASE}/data"
D854 = f"{BASE}/data_infiltration_854"
TARBALL = f"{DATA}/tcga_paad_rsem.tar.gz"
TARBALL_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
IMMUNE_SHA = "66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e"
AXIS_SHA = "31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d"
V62_SHA = "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"
TIDYESTIMATE_SHA = "cc747f787b6548a62219f3388ff6d93ad93cfcb60fe75f322fd712f41509514b"
GENESETS_RDA_SHA = "5d058439aed4f074b49d623c5bc4ebfbaceab79766249dd87f280c62d1c0469a"
COMMON_RDA_SHA = "f09453b2f12808b0dad73847390593cfee31142eb7490aa81e9d59aa0cba2ff3"
OV_RDA_SHA = "3fe246dbf5c9e1fd73c2a4d094e72d415d06b0018589be9dea341efa572b7478"

IMM_GENES = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
             "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
# Valeurs publiées de la vignette tidyestimate (ov, après filtre gènes
# communs) : s516 et s520, stromal / immune. Critère Porte J : 1 % relatif.
OV_EXPECTED = {"s516": {"stromal": -285.49841, "immune": 165.75062},
               "s520": {"stromal": 1927.51431, "immune": 2326.15984}}
OV_COMMON_EXPECTED = 10364


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
    assert sha(f"{D854}/tidyestimate_1.1.1.tar.gz") == TIDYESTIMATE_SHA, "SHA tidyestimate non conforme"
    assert sha(f"{D854}/tidyestimate/data/gene_sets.rda") == GENESETS_RDA_SHA, "SHA gene_sets.rda non conforme"
    assert sha(f"{D854}/tidyestimate/data/common_genes.rda") == COMMON_RDA_SHA, "SHA common_genes.rda non conforme"
    assert sha(f"{D854}/tidyestimate/data/ov.rda") == OV_RDA_SHA, "SHA ov.rda non conforme"
    out["sha_checks"] = {"immune": True, "axis": True, "v62": True,
                         "tarball_md5": True, "tidyestimate": True,
                         "gene_sets_rda": True, "common_genes_rda": True,
                         "ov_rda": True}
    print("SHA/MD5 : 8/8 conformes.")

    # --- Signatures en clair ---
    gs = pd.read_csv(f"{BASE}/infiltration_854_gene_sets.csv")
    assert list(gs.columns) == ["stromal_signature", "immune_signature"]
    assert len(gs) == 141
    stromal_set = set(gs["stromal_signature"])
    immune_set = set(gs["immune_signature"])
    assert len(stromal_set) == 141 and len(immune_set) == 141
    assert len(stromal_set & immune_set) == 0, "signatures non disjointes"
    flux_in_immune = sorted(immune_set & set(IMM_GENES))
    flux_in_stromal = sorted(stromal_set & set(IMM_GENES))
    assert flux_in_immune == ["GZMB"], f"flux dans signature immune : {flux_in_immune}"
    assert flux_in_stromal == ["CD163"], f"flux dans signature stromale : {flux_in_stromal}"
    cg = pd.read_csv(f"{BASE}/infiltration_854_common_genes.csv")
    assert len(cg) == 10391 and cg["hgnc_symbol"].nunique() == 10391
    common_set = set(cg["hgnc_symbol"])
    cg_full = pd.read_csv(f"{BASE}/infiltration_854_common_genes_full.csv")
    assert list(cg_full.columns) == ["entrezgene_id", "hgnc_symbol", "external_synonym"]
    assert len(cg_full) == 26336
    print("Signatures : 141+141, disjointes ; GZMB seule dans immune, "
          "CD163 seul dans stromal ; 10 391 gènes communs.")

    # --- Validation du port ssGSEA sur les données `ov` (Porte Jc) ---
    ov = pd.read_csv(f"{BASE}/infiltration_854_ov_test.csv", index_col=0)
    assert ov.shape == (17256, 10), f"ov inattendu : {ov.shape}"
    assert ov.index.is_unique, "symboles dupliqués dans ov"
    ov_filt, ov_info = filter_common_genes(ov, cg_full)
    n_ov_common = int(ov_filt.shape[0])
    print(f"ov filtré aux gènes communs : {n_ov_common} gènes "
          f"(exacts {ov_info['n_exact']} + alias {ov_info['n_alias']}, "
          f"attendu vignette : {OV_COMMON_EXPECTED}).")
    assert n_ov_common == OV_COMMON_EXPECTED, "nombre de gènes communs ov non conforme"
    ov_scores = estimate_scores(ov_filt, stromal_set, immune_set)
    ov_val = {}
    for sample, exp in OV_EXPECTED.items():
        row = ov_scores[ov_scores["sample"] == sample].iloc[0]
        for key in ("stromal", "immune"):
            rel = abs(float(row[key]) - exp[key]) / abs(exp[key])
            ov_val[f"{sample}_{key}"] = {"computed": float(row[key]),
                                         "expected": exp[key],
                                         "rel_err": float(rel)}
            assert rel < 0.01, f"port ssGSEA non validé : {sample} {key} err {rel:.4f}"
    out["port_validation_ov"] = {"n_common_genes": n_ov_common,
                                 "n_exact": ov_info["n_exact"],
                                 "n_alias": ov_info["n_alias"],
                                 "renamed_alias": ov_info["renamed"],
                                 "scores": ov_val, "tolerance_rel": 0.01,
                                 "passed": True}
    print("Port ssGSEA validé sur ov :",
          {k: round(v["rel_err"], 5) for k, v in ov_val.items()})

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
    need = ["KRAS"] + IMM_GENES
    missing = [g for g in need if g not in mat.index]
    assert not missing, f"gènes absents du tarball : {missing}"
    mat = mat[~mat.isna().any(axis=1)]
    logmat = np.log2(mat + 1.0)
    n_tum = int(logmat.shape[1])
    print(f"Tumeurs primaires : {n_tum} ; gènes (lignes) dans la matrice : {logmat.shape[0]}")

    axis = pd.read_csv(f"{BASE}/immune_kras_order_tcga.csv")
    imm = pd.read_csv(f"{BASE}/pdac_immune_tcga_fluxes.csv")
    assert list(imm.columns[1:]) == IMM_GENES, "colonnes immunitaires inattendues"
    assert len(axis) == 178 and len(imm) == 178, "n != 178"
    order_recalc = list(logmat.loc["KRAS"].sort_values(ascending=True).index)
    order_file = list(axis["sample"])
    gate_order = (order_recalc == order_file)
    kras_rec = logmat.loc["KRAS", order_file].values
    gate_kras_val = bool(np.allclose(axis["kras_raw"].values, kras_rec, atol=1e-9))
    samples = order_file
    assert set(samples) <= set(logmat.columns), "barcodes axe absents du tarball"
    imm_vals = imm[IMM_GENES].values.astype(float)
    assert np.allclose(imm_vals,
                       logmat.loc[IMM_GENES, samples].T.values, atol=1e-9), \
        "valeurs immunitaires non reproduites depuis le tarball — arrêt"

    # --- Scores ESTIMATE sur les 178 tumeurs ---
    mat_filt, tcga_info = filter_common_genes(logmat, cg_full)
    n_common_tcga = int(mat_filt.shape[0])
    out["tcga_common_filter"] = {"n_exact": tcga_info["n_exact"],
                                 "n_missing_before_alias": tcga_info["n_missing_before_alias"],
                                 "n_alias": tcga_info["n_alias"],
                                 "n_total": tcga_info["n_total"],
                                 "renamed_alias": tcga_info["renamed"]}
    sig_imm_present = sorted(immune_set & set(mat_filt.index))
    sig_str_present = sorted(stromal_set & set(mat_filt.index))
    print(f"TCGA filtré aux gènes communs : {n_common_tcga} / 10 391 "
          f"(exacts {tcga_info['n_exact']} + alias {tcga_info['n_alias']}) ; "
          f"signature immune présente : {len(sig_imm_present)}/141 ; "
          f"signature stromale présente : {len(sig_str_present)}/141.")
    assert len(sig_imm_present) == 141 and len(sig_str_present) == 141, \
        "gènes de signature absents de la matrice TCGA"
    scores_all = estimate_scores(mat_filt, stromal_set, immune_set)
    immune_wo12_set = immune_set - set(IMM_GENES)
    assert len(immune_wo12_set) == 140, "wo12 doit retirer GZMB seulement"
    scores_wo12 = estimate_scores(mat_filt, stromal_set, immune_wo12_set)
    s_map = scores_all.set_index("sample")
    w_map = scores_wo12.set_index("sample")
    imm_score = np.array([s_map.loc[s, "immune"] for s in samples])
    imm_wo12 = np.array([w_map.loc[s, "immune"] for s in samples])
    str_score = np.array([s_map.loc[s, "stromal"] for s in samples])
    est_score = np.array([s_map.loc[s, "estimate"] for s in samples])
    assert not np.isnan(imm_score).any() and not np.isnan(str_score).any()

    gate = {"n_tumors": n_tum, "order_178_178": bool(gate_order),
            "kras_values_match_1e-9": gate_kras_val,
            "immune_values_match_tarball_1e-9": True,
            "n_common_genes_tcga": n_common_tcga,
            "n_common_genes_tcga_over_10391": n_common_tcga / 10391.0,
            "sig_immune_present_141": len(sig_imm_present),
            "sig_stromal_present_141": len(sig_str_present),
            "port_validation_passed": True,
            "nan_in_scores": False}
    gate["open"] = bool(gate_order and gate_kras_val)
    out["gate_J"] = gate
    print("Porte J :", gate)
    assert gate["open"], "PORTE J FERMÉE — arrêt"

    scores = pd.DataFrame({"sample": samples, "kras_raw": kras_rec,
                           "ImmuneScore": imm_score,
                           "ImmuneScore_wo12": imm_wo12,
                           "StromalScore": str_score,
                           "ESTIMATEScore": est_score})
    scores.to_csv(f"{BASE}/infiltration_854_scores.csv", index=False)

    n = len(scores)
    out["scores"] = {}
    for name, s in [("ImmuneScore", imm_score), ("ImmuneScore_wo12", imm_wo12),
                    ("StromalScore", str_score), ("ESTIMATEScore", est_score)]:
        out["scores"][name] = {"min": float(s.min()), "median": float(np.median(s)),
                               "max": float(s.max()), "mean": float(s.mean()),
                               "sd": float(s.std(ddof=1))}
    out["scores"]["r_immune_stromal"] = float(np.corrcoef(imm_score, str_score)[0, 1])
    out["scores"]["r_immune_wo12"] = float(np.corrcoef(imm_score, imm_wo12)[0, 1])
    print("Scores :", {k: round(v["median"], 1) if isinstance(v, dict) else round(v, 4)
                       for k, v in out["scores"].items()})

    # --- Descriptif : infiltration vs proxys de pureté §8.51 ---
    pur = pd.read_csv(f"{BASE}/purity_851_scores.csv")
    assert len(pur) == 178 and set(pur["sample"]) == set(samples)
    pur = pur.set_index("sample").loc[samples]
    ac = pur["score_acineux"].values
    islet = pur["score_ilots"].values
    out["vs_purity_proxies"] = {
        "r_ImmuneScore_acineux": float(np.corrcoef(imm_score, ac)[0, 1]),
        "r_ImmuneScore_ilots": float(np.corrcoef(imm_score, islet)[0, 1]),
        "r_StromalScore_acineux": float(np.corrcoef(str_score, ac)[0, 1]),
        "r_StromalScore_ilots": float(np.corrcoef(str_score, islet)[0, 1]),
        "r_ImmuneScore_wo12_acineux": float(np.corrcoef(imm_wo12, ac)[0, 1]),
        "r_ImmuneScore_wo12_ilots": float(np.corrcoef(imm_wo12, islet)[0, 1])}
    print("vs pureté :", {k: round(v, 4) for k, v in out["vs_purity_proxies"].items()})

    # --- T1 : chaque flux vs scores d'infiltration ---
    t1 = []
    for j, g in enumerate(IMM_GENES):
        y = imm_vals[:, j]
        d = {"gene": g}
        for sname, s in [("ImmuneScore", imm_score),
                         ("ImmuneScore_wo12", imm_wo12),
                         ("StromalScore", str_score)]:
            r = float(np.corrcoef(y, s)[0, 1])
            d[f"r_{sname}"] = r
            d[f"p_{sname}"] = pearson_p(r, n)
            d[f"rho_{sname}"] = float(stats.spearmanr(y, s).statistic)
        X1 = np.column_stack([np.ones(n), imm_score])
        X2 = np.column_stack([np.ones(n), imm_score, str_score])
        _, r2a = ols_resid(y.reshape(-1, 1), X1)
        _, r2b = ols_resid(y.reshape(-1, 1), X2)
        d["R2_ImmuneScore"] = float(r2a[0])
        d["R2_ImmuneScore_StromalScore"] = float(r2b[0])
        t1.append(d)
    out["T1_per_flux"] = t1
    out["T1_summary"] = {
        "mean_abs_r_ImmuneScore": float(np.mean([abs(d["r_ImmuneScore"]) for d in t1])),
        "mean_abs_r_ImmuneScore_wo12": float(np.mean([abs(d["r_ImmuneScore_wo12"]) for d in t1])),
        "mean_abs_r_StromalScore": float(np.mean([abs(d["r_StromalScore"]) for d in t1])),
        "mean_abs_rho_ImmuneScore": float(np.mean([abs(d["rho_ImmuneScore"]) for d in t1])),
        "mean_abs_rho_ImmuneScore_wo12": float(np.mean([abs(d["rho_ImmuneScore_wo12"]) for d in t1])),
        "mean_abs_rho_StromalScore": float(np.mean([abs(d["rho_StromalScore"]) for d in t1])),
        "median_R2_ImmuneScore": float(np.median([d["R2_ImmuneScore"] for d in t1])),
        "max_R2_ImmuneScore": float(np.max([d["R2_ImmuneScore"] for d in t1])),
        "median_R2_ImmuneScore_StromalScore": float(np.median([d["R2_ImmuneScore_StromalScore"] for d in t1])),
        "max_R2_ImmuneScore_StromalScore": float(np.max([d["R2_ImmuneScore_StromalScore"] for d in t1]))}
    print("T1 résumé :", out["T1_summary"])

    # --- T2 : matrice intra-famille brute vs résidus ---
    imm_df = pd.DataFrame(imm_vals, columns=IMM_GENES)
    X_imm = np.column_stack([np.ones(n), imm_score])
    X_wo12 = np.column_stack([np.ones(n), imm_wo12])
    X_both = np.column_stack([np.ones(n), imm_score, str_score])
    res_imm, _ = ols_resid(imm_vals, X_imm)
    res_wo12, _ = ols_resid(imm_vals, X_wo12)
    res_both, _ = ols_resid(imm_vals, X_both)
    t2 = {"brut": mat_stats(imm_df),
          "resid_ImmuneScore": mat_stats(pd.DataFrame(res_imm, columns=IMM_GENES)),
          "resid_ImmuneScore_wo12": mat_stats(pd.DataFrame(res_wo12, columns=IMM_GENES)),
          "resid_ImmuneScore_StromalScore": mat_stats(pd.DataFrame(res_both, columns=IMM_GENES))}
    out["T2_matrix"] = t2
    b = t2["brut"]["pearson_mean_abs_r"]
    out["T2_summary"] = {
        "drop_ImmuneScore_pct": float(100 * (b - t2["resid_ImmuneScore"]["pearson_mean_abs_r"]) / b),
        "drop_ImmuneScore_wo12_pct": float(100 * (b - t2["resid_ImmuneScore_wo12"]["pearson_mean_abs_r"]) / b),
        "drop_ImmuneScore_StromalScore_pct": float(100 * (b - t2["resid_ImmuneScore_StromalScore"]["pearson_mean_abs_r"]) / b)}
    print("T2 :", {k: round(v["pearson_mean_abs_r"], 4) for k, v in t2.items()},
          "chutes %:", {k: round(v, 1) for k, v in out["T2_summary"].items()})
    pd.DataFrame(res_imm, columns=IMM_GENES).to_csv(
        f"{BASE}/infiltration_854_immune_resid.csv", index=False)

    # --- T3 : couplage par contrôle, brut vs résiduel + prédiction §8.48 ---
    def coupling(mat_df):
        c = mat_df.corr(method="pearson").values
        return {g: float(np.mean([abs(c[i, j]) for j in range(12) if j != i]))
                for i, g in enumerate(IMM_GENES)}
    c_brut = coupling(imm_df)
    c_res = coupling(pd.DataFrame(res_imm, columns=IMM_GENES))
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
    for name, s in [("ImmuneScore", imm_score), ("ImmuneScore_wo12", imm_wo12)]:
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
    with open(f"{BASE}/infiltration_854_results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    rows = []
    for d in t1:
        rows.append({"test": "T1", "gene": d["gene"],
                     "r_ImmuneScore": d["r_ImmuneScore"],
                     "p_ImmuneScore": d["p_ImmuneScore"],
                     "r_ImmuneScore_wo12": d["r_ImmuneScore_wo12"],
                     "p_ImmuneScore_wo12": d["p_ImmuneScore_wo12"],
                     "r_StromalScore": d["r_StromalScore"],
                     "p_StromalScore": d["p_StromalScore"],
                     "R2_ImmuneScore": d["R2_ImmuneScore"],
                     "R2_ImmuneScore_StromalScore": d["R2_ImmuneScore_StromalScore"]})
    pd.DataFrame(rows).to_csv(f"{BASE}/infiltration_854_results.csv", index=False)
    print("Écrit : infiltration_854_scores.csv, infiltration_854_immune_resid.csv, "
          "infiltration_854_results.json/.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
