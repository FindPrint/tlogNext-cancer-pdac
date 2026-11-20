#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.55 — Porte S, jointure, T1'-T4' : pureté externe ABSOLUTE vs corrélation
immunitaire. Miroir de analyze_purity_851.py (mêmes définitions).
Protocole gelé : PROTOCOL_purity_external_855.md
(SHA 734a9b171cf0ce155d456288d8f617528aa237820269d1c3e429505bce134db7).
Source externe : pdacR TCGA_PAAD.rds (Raphael et al. 2017, Table S1),
data/pdacR_TCGA_PAAD.rds, SHA 52020679…ea76 ; sampInfo transcrit dans
purity_855_sampinfo.csv, SHA 7a09dde3…b014.
ESTIMATE-purity publiée pour PAAD : NON obtenue (cf. porte S, §8.55.2) ;
les tests portent donc sur ABSOLUTE seul, comme le prévoit la clause de
substitution du protocole §7. Aucun run ici.
Sorties : purity_855_external.csv, purity_855_results.json/.csv (T1'-T4').
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
ARAN_SHA = "fce1ba13ff3a6432b7e4f260eb516e407c967d615ca87bc8dffa7765baf97529"
SHRINK_SHA = "a582bc6f62c68e9a419c39a665b9e45a52baea7f31f5afee944147be587a5bab"

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
        "aran_supp_data1": sha(f"{BASE}/data/aran2015_supp_data1_ncomms9971-s2.xlsx") == ARAN_SHA,
        "shrinkagetrees_pdac": sha(f"{BASE}/data/shrinkagetrees_pdac.csv") == SHRINK_SHA,
    }
    print("SHA :", checks)
    assert all(checks.values()), f"SHA non conforme : {checks}"
    out["sha_checks"] = checks

    # --- Porte S : sources tentées (faits vérifiés en machine) ---
    aran = pd.read_excel(f"{BASE}/data/aran2015_supp_data1_ncomms9971-s2.xlsx",
                          sheet_name="Supp Data 1", header=3)
    aran = aran.drop(columns=[c for c in aran.columns if str(c).startswith("Unnamed")])
    n_aran = len(aran)
    n_aran_paad = int((aran["Cancer type"] == "PAAD").sum())
    n_aran_absolute = int(aran["ABSOLUTE"].notna().sum())
    out["porte_S"] = {
        "aran2015_supp_data1": {"rows": n_aran, "cancer_types": int(aran["Cancer type"].nunique()),
                                "paad_rows": n_aran_paad,
                                "absolute_non_null_total": n_aran_absolute,
                                "url": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4671203/supplementaryFiles",
                                "zip_sha256": "4685a8b2e903e34f0da3f4da4139448cdb8c80e141d42329d1f78581ebb541a5",
                                "xlsx_sha256": ARAN_SHA},
        "ucscxena_tcga_purity": {"note": "même tableau qu'Aran 2015 (9 364 lignes, "
                                 "mêmes colonnes et premières lignes) : 0 PAAD — vérifié sur "
                                 "UCSCXenaShiny 2.2.1 data/tcga_purity.rda, "
                                 "tarball SHA 377c0f3ff0444b68ecb2db65f3d71f18516a53e586c2c2f16efbb2283abca597"},
        "estimate_publie_paad": {"obtenu": False,
                                 "note": "site MD Anderson (bioinformatics.mdanderson.org/estimate/) "
                                 "liste PAAD RNA-seqV2 n=179 avec téléchargement par maladie, "
                                 "mais le fichier de données n'a pas pu être récupéré : "
                                 "téléchargement piloté par JS (disease.html + js/disease_histogram.js), "
                                 "fetch du JS en échec répété (curl 000 x3, timeout du fetch de page) ; "
                                 "repli par recalcul (package R estimate) NON fait — ce ne serait "
                                 "pas un score publié, et ABSOLUTE (ADN, indépendant de l'ARN) "
                                 "est le contrôle externe le plus fort et il est disponible."},
        "pdacr_absolute": {"fichier": "data/pdacR_TCGA_PAAD.rds",
                           "url": "https://raw.githubusercontent.com/rmoffitt/pdacR/master/data/TCGA_PAAD.rds",
                           "sha256": RDS_SHA, "sampinfo_sha256": SAMPINFO_SHA,
                           "publication": "Raphael et al. 2017, Cancer Cell 32(2):185-203.e13, "
                           "PMID 28810144, PMCID PMC5964983, DOI 10.1016/j.ccell.2017.07.007, Table S1",
                           "curation": "Torre-Healy et al. 2023, Commun Biol 6:163, "
                           "doi 10.1038/s42003-023-04461-6 (pdacR, github.com/rmoffitt/pdacR)"},
    }
    print(f"Porte S : Aran {n_aran} lignes, PAAD {n_aran_paad} ; pdacR ABSOLUTE à joindre.")
    assert n_aran_paad == 0, "Aran contiendrait PAAD — contredit l'exploration"

    # --- Jointure (protocole §4 : clé 15 premiers caractères) ---
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
    abs_col = m["ABSOLUTE.Purity"]
    n_abs = int(abs_col.notna().sum())
    in_range = bool(((abs_col.dropna() >= 0) & (abs_col.dropna() <= 1)).all())
    gate = {"n_ours": 178, "n_externes": 181, "matched_barcode": n_matched,
            "absolute_non_null": n_abs,
            "absolute_dans_[0,1]": in_range,
            "unmatched_ours": m[m["_merge"] == "left_only"]["sample"].tolist(),
            "externes_hors_projet": si[~si["key15"].isin(axis["key15"])]["Tumor.Sample.ID"].tolist()}
    gate["open"] = bool(n_matched == 178 and n_abs >= 100 and in_range)
    out["gate_S"] = gate
    print("Porte S / jointure :", {k: v for k, v in gate.items()
                                   if k not in ("unmatched_ours", "externes_hors_projet")})
    print("  externes hors projet :", gate["externes_hors_projet"])
    assert gate["open"], "PORTE S FERMÉE — arrêt"

    # --- Sous-ensemble apparié avec ABSOLUTE (n=149), ordre KRAS brut conservé ---
    sub = m.dropna(subset=["ABSOLUTE.Purity"]).reset_index(drop=True)
    n = len(sub)
    assert n == 149, f"n apparié attendu 149, obtenu {n}"
    samples = sub["sample"].tolist()
    absol = sub["ABSOLUTE.Purity"].values.astype(float)
    imm_idx = imm.set_index(axis["sample"].values)
    Y = imm_idx.loc[samples, IMM_GENES].values.astype(float)
    assert not np.isnan(Y).any() and not np.isnan(absol).any()
    ext = pd.DataFrame({"sample": samples, "key15": sub["key15"].values,
                        "purity_absolute": absol,
                        "purity_methylation_mode": sub["DNA.hypermethylation.mode.purity"].values,
                        "leukocyte_methyl_percent": sub["DNA.methylation.leukocyte.percent.estimate"].values,
                        "purity_class": sub["Purity.Class.high.or.low"].values,
                        "pathologist_cellularity": sub["Pathologist.Reviewed.Tumor.Cellularity"].values})
    ext.to_csv(f"{BASE}/purity_855_external.csv", index=False)
    out["matched"] = {"n": n, "absolute": {"min": float(absol.min()), "median": float(np.median(absol)),
                                           "mean": float(absol.mean()), "sd": float(absol.std(ddof=1)),
                                           "max": float(absol.max())}}
    print(f"Appariées ABSOLUTE : n={n} min={absol.min():.2f} méd={np.median(absol):.2f} "
          f"moy={absol.mean():.4f} max={absol.max():.2f}")

    # --- Cohérence externe (vérifications, pas des tests du verdict) ---
    both = ext.dropna(subset=["purity_absolute", "purity_methylation_mode"])
    r_meth = float(np.corrcoef(both["purity_absolute"], both["purity_methylation_mode"])[0, 1])
    hi = ext[ext["purity_class"] == "high"]["purity_absolute"]
    lo = ext[ext["purity_class"] == "low"]["purity_absolute"]
    shrink = pd.read_csv(f"{BASE}/data/shrinkagetrees_pdac.csv")
    sh_abs = shrink["absolute.purity"].dropna()
    out["coherence"] = {
        "absolute_vs_methylation_purity": {"n": int(len(both)), "r_pearson": r_meth,
                                           "p": pearson_p(r_meth, len(both))},
        "purity_class_vs_absolute": {"n_high": int(len(hi)), "n_low": int(len(lo)),
                                     "high_min": float(hi.min()), "high_max": float(hi.max()),
                                     "low_min": float(lo.min()), "low_max": float(lo.max()),
                                     "high_mean": float(hi.mean()), "low_mean": float(lo.mean())},
        "shrinkagetrees_distribution": {"n": int(len(sh_abs)), "mean": float(sh_abs.mean()),
                                        "sd": float(sh_abs.std(ddof=1)), "min": float(sh_abs.min()),
                                        "max": float(sh_abs.max()),
                                        "source": "CRAN ShrinkageTrees 2.1.1, data/pdac.rda "
                                        "(sous-ensemble réduit de pdacR, sans barcode — "
                                        "comparaison de distribution seulement)"},
    }
    print(f"Cohérence : ABSOLUTE vs pureté méthylation r={r_meth:.4f} (n={len(both)}) ; "
          f"classe high ABSOLUTE [{hi.min():.2f},{hi.max():.2f}] (n={len(hi)}), "
          f"low [{lo.min():.2f},{lo.max():.2f}] (n={len(lo)}) ; "
          f"ShrinkageTrees n={len(sh_abs)} moy={sh_abs.mean():.4f} min={sh_abs.min():.2f} max={sh_abs.max():.2f}")

    # --- T1' : chaque flux vs ABSOLUTE ---
    t1 = []
    for j, g in enumerate(IMM_GENES):
        y = Y[:, j]
        r_ab = float(np.corrcoef(y, absol)[0, 1])
        rho_ab = float(stats.spearmanr(y, absol).statistic)
        X = np.column_stack([np.ones(n), absol])
        _, r2 = ols_resid(y.reshape(-1, 1), X)
        t1.append({"gene": g, "r_absolute": r_ab, "p_absolute": pearson_p(r_ab, n),
                   "rho_absolute": rho_ab, "R2_absolute": float(r2[0])})
    out["T1_per_flux"] = t1
    out["T1_summary"] = {
        "mean_abs_r_absolute": float(np.mean([abs(d["r_absolute"]) for d in t1])),
        "mean_abs_rho_absolute": float(np.mean([abs(d["rho_absolute"]) for d in t1])),
        "median_R2_absolute": float(np.median([d["R2_absolute"] for d in t1])),
        "max_R2_absolute": float(np.max([d["R2_absolute"] for d in t1]))}
    print("T1' résumé :", out["T1_summary"])

    # --- T2' : matrice intra-famille brute (n=149) vs résidus [1, ABSOLUTE] ---
    imm_df = pd.DataFrame(Y, columns=IMM_GENES)
    Xabs = np.column_stack([np.ones(n), absol])
    res_abs, _ = ols_resid(Y, Xabs)
    t2 = {"brut_n149": mat_stats(imm_df),
          "resid_absolute": mat_stats(pd.DataFrame(res_abs, columns=IMM_GENES))}
    out["T2_matrix"] = t2
    b = t2["brut_n149"]["pearson_mean_abs_r"]
    rb = t2["resid_absolute"]["pearson_mean_abs_r"]
    out["T2_summary"] = {"drop_absolute_pct": float(100 * (b - rb) / b)}
    # Référence brute sur les 178 (information, pas le verdict — le verdict
    # compare brut et résiduel sur le MÊME n=149).
    imm178 = pd.DataFrame(imm[IMM_GENES].values.astype(float), columns=IMM_GENES)
    out["T2_reference_178"] = mat_stats(imm178)
    print(f"T2' : brut n=149 {b:.4f} -> résid ABSOLUTE {rb:.4f} "
          f"(chute {out['T2_summary']['drop_absolute_pct']:.1f} %) ; "
          f"brut n=178 (réf.) {out['T2_reference_178']['pearson_mean_abs_r']:.4f}")

    # --- T3' : couplage par contrôle, brut vs résiduel + prédiction §8.48 ---
    def coupling(mat_df):
        c = mat_df.corr(method="pearson").values
        return {g: float(np.mean([abs(c[i, j]) for j in range(12) if j != i]))
                for i, g in enumerate(IMM_GENES)}
    c_brut = coupling(imm_df)
    c_res = coupling(pd.DataFrame(res_abs, columns=IMM_GENES))
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
    print("T3' résumé :", out["T3_summary"])

    # --- T4' : stratification médiane ABSOLUTE ---
    med = float(np.median(absol))
    hi_m = absol >= med
    lo_m = ~hi_m
    t4 = {"absolute": {"median": med, "n_hi": int(hi_m.sum()), "n_lo": int(lo_m.sum()),
                       "hi": mat_stats(imm_df[hi_m]),
                       "lo": mat_stats(imm_df[lo_m])}}
    out["T4_stratification"] = t4
    print("T4' :", {k: (round(v["hi"]["pearson_mean_abs_r"], 4),
                        round(v["lo"]["pearson_mean_abs_r"], 4)) for k, v in t4.items()})

    # --- Sauvegarde ---
    with open(f"{BASE}/purity_855_results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    rows = []
    for d in t1:
        rows.append({"test": "T1'", "gene": d["gene"], "r_absolute": d["r_absolute"],
                     "p_absolute": d["p_absolute"], "rho_absolute": d["rho_absolute"],
                     "R2_absolute": d["R2_absolute"]})
    pd.DataFrame(rows).to_csv(f"{BASE}/purity_855_results.csv", index=False)
    print("Écrit : purity_855_external.csv, purity_855_results.json/.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
