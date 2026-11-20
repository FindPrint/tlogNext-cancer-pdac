#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.65 — Scores ESTIMATE publiés pour TCGA-PAAD (MD Anderson).
Protocole gelé : PROTOCOL_estimate_published_865.md
(SHA b105e87b26c7f11b1bd29ec5eccfc05b8cb16cd5dbb5ff35db3f2df0dfd2961d).
Porte S, jointure par barcode (15 premiers caractères), T0–T4''.
Comparateurs relus en machine : infiltration_854_scores.csv (§8.54),
purity_855_external.csv (§8.55, ABSOLUTE), pdac_immune_tcga_fluxes.csv.
Re-vérification Aran 2015 : 0 PAAD (cf. §8.55.2).
"""
import hashlib
import json

import numpy as np
import pandas as pd
from scipy import stats

BASE = "/home/hatch/workspace/runs/pdac-v6"
DATA = f"{BASE}/data_estimate_published_865"
IMM_GENES = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
             "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
PUB_FILE = f"{DATA}/pancreatic_ductal_adenocarcinoma_RNAseqV2.txt"
PUB_URL = ("https://bioinformatics.mdanderson.org/estimate/tables/"
           "pancreatic_ductal_adenocarcinoma_RNAseqV2.txt")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pearson(a, b):
    r, p = stats.pearsonr(a, b)
    return float(r), float(p)


def spearman(a, b):
    r, p = stats.spearmanr(a, b)
    return float(r), float(p)


def ols_resid(y, X):
    """Résidus OLS de y sur [1, X] (X : DataFrame de contrôles)."""
    M = np.column_stack([np.ones(len(y))] + [X[c].to_numpy() for c in X.columns])
    beta, *_ = np.linalg.lstsq(M, y.to_numpy(), rcond=None)
    return y.to_numpy() - M @ beta


def cohesion(df):
    """Moyenne |r| Pearson, médiane |r|, fraction |r|>0,5, max |r| sur 66 paires."""
    vals = []
    for i in range(len(IMM_GENES)):
        for j in range(i + 1, len(IMM_GENES)):
            r, _ = pearson(df[IMM_GENES[i]], df[IMM_GENES[j]])
            vals.append(abs(r))
    vals = np.array(vals)
    return {"mean_abs_r": float(vals.mean()), "median_abs_r": float(np.median(vals)),
            "frac_gt_05": float((vals > 0.5).mean()), "n_gt_05": int((vals > 0.5).sum()),
            "max_abs_r": float(vals.max()), "n_pairs": 66}


def main():
    out = {"protocol_sha": "b105e87b26c7f11b1bd29ec5eccfc05b8cb16cd5dbb5ff35db3f2df0dfd2961d"}
    # --- Vérifications gelées ---
    v62 = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
    out["v62_sha"] = sha(v62)
    assert out["v62_sha"] == "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"
    imm = pd.read_csv(f"{BASE}/pdac_immune_tcga_fluxes.csv")
    axis = pd.read_csv(f"{BASE}/immune_kras_order_tcga.csv")
    assert sha(f"{BASE}/pdac_immune_tcga_fluxes.csv") == \
        "66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e"
    assert sha(f"{BASE}/immune_kras_order_tcga.csv") == \
        "31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d"
    assert sha(f"{BASE}/infiltration_854_scores.csv") == \
        "628732ecbcc30a3281b0df7a5039ec2520a1c5f1a1ae9ce412c4d0d7caf78aa7"
    # Base immunitaire : lignes en ordre KRAS (step), barcode dans l'axe.
    assert (imm["step"].values == axis["step"].values).all()
    dat = pd.DataFrame({"sample": axis["sample"].values})
    for g in IMM_GENES:
        dat[g] = imm[g].values
    imm = dat

    # --- Porte S : fichier publié MD Anderson ---
    pub = pd.read_csv(PUB_FILE, sep="\t")
    out["porte_S"] = {
        "url": PUB_URL,
        "sha256": sha(PUB_FILE),
        "octets": len(open(PUB_FILE, "rb").read()),
        "colonnes": list(pub.columns),
        "n_lignes": int(len(pub)),
        "n_paad_lignes": int(pub["ID"].str.startswith("TCGA-").sum()),
    }
    assert list(pub.columns) == ["ID", "Stromal_score", "Immune_score", "ESTIMATE_score"]
    # ESTIMATEScore = somme des deux ? (vérification en machine)
    out["porte_S"]["estimate_eq_sum_max_abs_diff"] = float(
        np.abs(pub["ESTIMATE_score"] - (pub["Stromal_score"] + pub["Immune_score"])).max())
    # Re-vérification Aran 2015 (déjà détenu) : 0 PAAD
    aran = pd.read_excel(f"{BASE}/data/aran2015_supp_data1_ncomms9971-s2.xlsx",
                         sheet_name="Supp Data 1", header=3)
    out["aran_reverification"] = {
        "n_lignes": int(len(aran)),
        "types": sorted(aran["Cancer type"].dropna().unique().tolist()),
        "n_paad": int((aran["Cancer type"] == "PAAD").sum()),
        "sha256": sha(f"{BASE}/data/aran2015_supp_data1_ncomms9971-s2.xlsx"),
    }

    # --- Jointure §4 : 15 premiers caractères ---
    pub["key15"] = pub["ID"].str.slice(0, 15)
    assert pub["key15"].is_unique, "collision de clé côté publié"
    imm15 = imm.copy()
    imm15["key15"] = imm15["sample"].str.slice(0, 15)
    assert imm15["key15"].is_unique, "collision de clé côté projet"
    joined = imm15.merge(pub, on="key15", how="left")
    matched = joined[joined["Immune_score"].notna()].copy()
    unmatched = sorted(joined.loc[joined["Immune_score"].isna(), "sample"].tolist())
    out["jointure"] = {
        "n_projet": 178,
        "n_publie": int(len(pub)),
        "n_apparie": int(len(matched)),
        "n_non_apparie": int(len(unmatched)),
        "non_apparies": unmatched,
        "collisions": 0,
        "cles_pub_hors_projet": sorted(pub.loc[~pub["key15"].isin(imm15["key15"]), "ID"].tolist()),
    }
    # Descriptifs publiés (n apparié)
    for c in ["Stromal_score", "Immune_score", "ESTIMATE_score"]:
        s = matched[c]
        out[f"descriptif_publie_{c}"] = {"min": float(s.min()), "median": float(s.median()),
                                         "mean": float(s.mean()), "std": float(s.std()),
                                         "max": float(s.max())}

    # --- T0 : publié ↔ recalculé (§8.54) ---
    rec = pd.read_csv(f"{BASE}/infiltration_854_scores.csv")
    rec["key15"] = rec["sample"].str.slice(0, 15)
    m2 = matched.reset_index(drop=True).merge(
        rec[["key15", "ImmuneScore", "StromalScore", "ESTIMATEScore", "ImmuneScore_wo12"]],
        on="key15", how="left", suffixes=("_pub", "_recalc"))
    assert len(m2) == len(matched) and m2["ImmuneScore"].notna().all()
    t0 = {}
    for pub_c, rec_c in [("Immune_score", "ImmuneScore"), ("Stromal_score", "StromalScore"),
                         ("ESTIMATE_score", "ESTIMATEScore")]:
        r, p = pearson(m2[pub_c], m2[rec_c])
        rs, ps = spearman(m2[pub_c], m2[rec_c])
        t0[f"{pub_c}_vs_recalcule"] = {"pearson_r": r, "pearson_p": p,
                                       "spearman_rho": rs, "spearman_p": ps,
                                       "max_abs_diff": float(np.abs(m2[pub_c] - m2[rec_c]).max()),
                                       "mean_abs_diff": float(np.abs(m2[pub_c] - m2[rec_c]).mean())}
    r, p = pearson(m2["Immune_score"], m2["ImmuneScore_wo12"])
    t0["Immune_score_vs_recalcule_wo12"] = {"pearson_r": r, "pearson_p": p}
    r, p = pearson(m2["Immune_score"], m2["Stromal_score"])
    t0["r_immune_stromal_publies"] = {"pearson_r": r, "pearson_p": p}
    r, p = pearson(m2["Immune_score"], m2["StromalScore"])
    t0["r_immune_pub_vs_stromal_recalcule"] = {"pearson_r": r, "pearson_p": p}
    out["T0"] = t0
    # Pureté ESTIMATE publiée ? absente (pas de colonne pureté) — ABSOLUTE vs scores publiés
    absd = pd.read_csv(f"{BASE}/purity_855_external.csv")
    m3 = m2.merge(absd[["sample", "purity_absolute", "purity_methylation_mode"]],
                  left_on="sample", right_on="sample", how="left")
    sub = m3[m3["purity_absolute"].notna()]
    out["T0"]["n_avec_absolute"] = int(len(sub))
    for c in ["Immune_score", "Stromal_score", "ESTIMATE_score"]:
        r, p = pearson(sub[c], sub["purity_absolute"])
        out["T0"][f"{c}_vs_absolute"] = {"pearson_r": r, "pearson_p": p, "n": int(len(sub))}

    # --- T1'' : chaque flux vs scores publiés ---
    t1 = []
    for g in IMM_GENES:
        row = {"gene": g}
        for c in ["Immune_score", "Stromal_score", "ESTIMATE_score"]:
            r, p = pearson(matched[g], matched[c])
            rs, _ = spearman(matched[g], matched[c])
            row[f"r_{c}"] = r
            row[f"p_{c}"] = p
            row[f"rho_{c}"] = rs
        # R² OLS [Immune] et [Immune, Stromal]
        for cols, tag in [(["Immune_score"], "Immune"), (["Immune_score", "Stromal_score"], "ImmStrom")]:
            M = np.column_stack([np.ones(len(matched))] + [matched[c].to_numpy() for c in cols])
            beta, *_ = np.linalg.lstsq(M, matched[g].to_numpy(), rcond=None)
            pred = M @ beta
            ss_res = float(np.sum((matched[g].to_numpy() - pred) ** 2))
            ss_tot = float(np.sum((matched[g].to_numpy() - matched[g].mean()) ** 2))
            row[f"R2_{tag}"] = 1 - ss_res / ss_tot
        t1.append(row)
    out["T1"] = t1
    for c in ["Immune_score", "Stromal_score", "ESTIMATE_score"]:
        out[f"T1_moy_abs_r_{c}"] = float(np.mean([abs(r[f"r_{c}"]) for r in t1]))
    out["T1_R2_median_Immune"] = float(np.median([r["R2_Immune"] for r in t1]))
    out["T1_R2_max_Immune"] = float(np.max([r["R2_Immune"] for r in t1]))

    # --- T2'' : cohésion brute vs résidus ---
    brute = cohesion(matched)
    resid_imm = matched.copy()
    resid_both = matched.copy()
    for g in IMM_GENES:
        resid_imm[g] = ols_resid(matched[g], matched[["Immune_score"]])
        resid_both[g] = ols_resid(matched[g], matched[["Immune_score", "Stromal_score"]])
    out["T2"] = {"brute": brute,
                 "residus_ImmuneScore_pub": cohesion(resid_imm),
                 "residus_ImmStrom_pub": cohesion(resid_both)}
    out["T2"]["chute_Immune_pct"] = 100 * (brute["mean_abs_r"] - out["T2"]["residus_ImmuneScore_pub"]["mean_abs_r"]) / brute["mean_abs_r"]
    out["T2"]["chute_ImmStrom_pct"] = 100 * (brute["mean_abs_r"] - out["T2"]["residus_ImmStrom_pub"]["mean_abs_r"]) / brute["mean_abs_r"]

    # --- T3'' : couplage prédit ---
    def coupling(df):
        cs = {}
        for g in IMM_GENES:
            others = [h for h in IMM_GENES if h != g]
            cs[g] = float(np.mean([abs(pearson(df[g], df[h])[0]) for h in others]))
        return cs
    c_brut = coupling(matched)
    c_res = coupling(resid_imm)
    out["T3"] = {
        "C_moyen_brut": float(np.mean(list(c_brut.values()))),
        "C_moyen_resid_Immune": float(np.mean(list(c_res.values()))),
        "d_pred_moyen_brut": float(-0.175 + 1.705 * np.mean(list(c_brut.values()))),
        "d_pred_moyen_resid": float(-0.175 + 1.705 * np.mean(list(c_res.values()))),
        "CD8A_C_brut": c_brut["CD8A"],
        "CD8A_C_resid": c_res["CD8A"],
        "CD8A_d_pred_brut": float(-0.175 + 1.705 * c_brut["CD8A"]),
        "CD8A_d_pred_resid": float(-0.175 + 1.705 * c_res["CD8A"]),
        "C_par_controle_brut": c_brut,
        "C_par_controle_resid": c_res,
    }

    # --- T4'' : stratification médiane ImmuneScore publié ---
    med = float(matched["Immune_score"].median())
    hi = matched[matched["Immune_score"] >= med]
    lo = matched[matched["Immune_score"] < med]
    out["T4"] = {
        "mediane_ImmuneScore_pub": med,
        "n_haute": int(len(hi)), "n_basse": int(len(lo)),
        "sd_Immune_haute": float(hi["Immune_score"].std()),
        "sd_Immune_basse": float(lo["Immune_score"].std()),
        "sd_Immune_globale": float(matched["Immune_score"].std()),
        "plage_haute": [float(hi["Immune_score"].min()), float(hi["Immune_score"].max())],
        "plage_basse": [float(lo["Immune_score"].min()), float(lo["Immune_score"].max())],
        "cohesion_haute": cohesion(hi),
        "cohesion_basse": cohesion(lo),
    }

    # --- Fichiers de sortie ---
    ext = matched[["sample", "Immune_score", "Stromal_score", "ESTIMATE_score"]].copy()
    ext = ext.rename(columns={"Immune_score": "immune_pub", "Stromal_score": "stromal_pub",
                              "ESTIMATE_score": "estimate_pub"})
    ext["key15"] = ext["sample"].str.slice(0, 15)
    ext["source"] = "MD Anderson ESTIMATE disease table PAAD RNAseqV2"
    ext["source_url"] = PUB_URL
    ext["source_sha256"] = sha(PUB_FILE)
    ext.to_csv(f"{BASE}/estimate_published_865_external.csv", index=False)
    out["fichier_apparie"] = {"nom": "estimate_published_865_external.csv",
                              "sha256": sha(f"{BASE}/estimate_published_865_external.csv"),
                              "n_lignes": int(len(ext))}
    # Résidus publiés (pour le build T5'')
    resid_imm[["sample"] + IMM_GENES].to_csv(f"{BASE}/estimate_published_865_immune_resid.csv", index=False)
    out["fichier_residus"] = {"nom": "estimate_published_865_immune_resid.csv",
                              "sha256": sha(f"{BASE}/estimate_published_865_immune_resid.csv")}
    # T1 en CSV
    pd.DataFrame(t1).to_csv(f"{BASE}/estimate_published_865_results.csv", index=False)
    out["fichier_T1_csv"] = sha(f"{BASE}/estimate_published_865_results.csv")
    with open(f"{BASE}/estimate_published_865_results.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(json.dumps({k: out[k] for k in
                      ["porte_S", "jointure", "T0", "T1_moy_abs_r_Immune_score",
                       "T1_moy_abs_r_Stromal_score", "T1_R2_median_Immune", "T2",
                       "T3", "T4"]}, indent=2, ensure_ascii=False))
    print("ARAN:", out["aran_reverification"]["n_lignes"], "lignes, PAAD =",
          out["aran_reverification"]["n_paad"])


if __name__ == "__main__":
    main()
