#!/usr/bin/env python3
"""§8.60 — Porte D, jointure, T1-T4, bras L (fraction leucocytaire par
methylation). Protocole gele : PROTOCOL_deconvolution_860.md.
Regles : SHAs verifies avant tout calcul ; cohésion brute RECALCULÉE sur le
sous-ensemble apparie, jamais importee ; p brutes sans correction ; NaN
CIBERSORT = lignes tout-NaN exclues (analyse en complete-case par type —
les NaN sont tout-ou-rien par ligne, verifie en machine).
"""
import hashlib
import json

import numpy as np
import pandas as pd
from scipy import stats

BASE = "/home/hatch/workspace/runs/pdac-v6"
D = BASE + "/data_deconvolution_860/"
IMM_GENES = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
             "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]

EXPECTED = {
    "pipeline_v62": ("biophysique-hp35/universal_v6.2.0_cohen.py",
                     "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"),
    "flux": ("pdac_immune_tcga_fluxes.csv",
             "66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e"),
    "ordre": ("immune_kras_order_tcga.csv",
              "31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d"),
    "scores854": ("infiltration_854_scores.csv",
                  "628732ecbcc30a3281b0df7a5039ec2520a1c5f1a1ae9ce412c4d0d7caf78aa7"),
    "ext855": ("purity_855_external.csv",
               "03f34fe07a18ff106e21ce9028ef9ff60d3d95889c3064898442246e486fbd6f"),
    "sampinfo855": ("purity_855_sampinfo.csv",
                    "7a09dde3"),  # prefixe seul : le §8.55 cite 7a09dde3…b014
    # (tronque) ; SHA complet mesure : 7a09dde3d374…78b014.
    "imcell_rda": ("data_deconvolution_860/TCGA_IMCell_fraction.rda",
                   "739bfa99495643a926e6f010589044f69969962e2197378bba67e097366370c0"),
    "leuko_rda": ("data_deconvolution_860/TCGA_Leukocyte_fraction.rda",
                  "f576f5f261bbfe4dcc2384c7d90c375e109986f31ad54b544136e5d9a4e68289"),
    "lm22": ("data_deconvolution_860/LM22.txt",
             "8b1b4bb21fffcb10d25ecb6df9aafa3a24b527c35130b9d65e9341a6287cd36c"),
}


def sha(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def check(name, rel, expect):
    got = sha("/home/hatch/workspace/runs/" + rel) if rel.startswith("biophysique") \
        else sha(BASE + "/" + rel)
    ok = got.startswith(expect)
    print(f"SHA {name}: {'OK' if ok else 'MISMATCH ' + got}")
    assert ok, f"{name} mismatch: {got}"
    return got


def cohesion(df):
    c = df.corr(method="pearson").values
    iu = np.triu_indices_from(c, k=1)
    v = np.abs(c[iu])
    return {"mean_abs_r": float(v.mean()), "median_abs_r": float(np.median(v)),
            "frac_gt_0.5": float((v > 0.5).mean()),
            "n_gt_0.5": int((v > 0.5).sum()), "n_pairs": int(len(v)),
            "max_abs_r": float(v.max())}


def resid_ols(Y, X):
    Xd = np.column_stack([np.ones(len(Y)), X])
    beta, *_ = np.linalg.lstsq(Xd, Y, rcond=None)
    return Y - Xd @ beta


def main():
    for k, (rel, exp) in EXPECTED.items():
        check(k, rel, exp)
    tar_md5 = sha(BASE + "/data/tcga_paad_rsem.tar.gz", "md5")
    assert tar_md5 == "b09569ce3f4721f514bc137bd109ac0a", tar_md5
    print("MD5 tarball TCGA-PAAD: OK")

    order = pd.read_csv(BASE + "/immune_kras_order_tcga.csv")
    flux = pd.read_csv(BASE + "/pdac_immune_tcga_fluxes.csv")
    assert len(order) == 178 and len(flux) == 178
    assert (order["step"].values == flux["step"].values).all()
    assert flux[IMM_GENES].isna().sum().sum() == 0
    Y_all = flux[IMM_GENES].values.astype(float)
    samples = order["sample"].values
    pat12 = pd.Series(samples).str[:12].values

    im = pd.read_csv(D + "TCGA_IMCell_fraction.csv")
    lk = pd.read_csv(D + "TCGA_Leukocyte_fraction.csv")
    types = [c for c in im.columns if c != "PATIENT_BARCODE"]
    assert len(types) == 22, types
    im_idx = im.set_index("PATIENT_BARCODE")
    lk_idx = lk.set_index("Tumor_Sample_ID")
    assert im_idx.index.is_unique and lk_idx.index.is_unique

    # --- Porte D / jointure ---
    matched_mask = np.array([p in im_idx.index for p in pat12])
    print(f"Porte D: IMCell appariees {int(matched_mask.sum())}/178 "
          f"(absente: {samples[~matched_mask].tolist()})")
    assert int(matched_mask.sum()) >= 100
    F = im_idx.reindex(pd.Series(pat12)).reset_index(drop=True)
    complete = ~F[types].isna().all(axis=1)
    print(f"lignes appariees tout-NaN (CIBERSORT indisponible): "
          f"{int((matched_mask & ~complete).sum())} ; "
          f"n effectif complet: {int((matched_mask & complete).sum())}")
    # Les NaN sont tout-ou-rien par ligne (verifie).
    assert (F[types].isna().sum(axis=1).isin([0, 22])).all()
    n_eff = int((matched_mask & complete).sum())
    keep = matched_mask & complete
    Y = Y_all[keep]
    Fk = F[keep].reset_index(drop=True)
    samp_k = samples[keep]

    # --- Verification d'identification (descriptif) ---
    sc854 = pd.read_csv(BASE + "/infiltration_854_scores.csv").set_index("sample")
    ext855 = pd.read_csv(BASE + "/purity_855_external.csv").set_index("sample")
    sampinfo = pd.read_csv(BASE + "/purity_855_sampinfo.csv")
    si = sampinfo.set_index("Tumor.Sample.ID")
    leuko_meth = si.reindex(pd.Series(samples).str[:16])[  # IDs sampInfo = 16 car.
        "DNA.methylation.leukocyte.percent.estimate"]
    leuko_im = lk_idx.reindex(pd.Series(samples).str[:15])["Leukocyte_fraction"]
    imm_score = sc854.reindex(pd.Series(samples))["ImmuneScore"]
    absol = ext855.reindex(pd.Series(samples))["purity_absolute"]
    verif = {}
    for a, b, lab in [
            (leuko_im.values, leuko_meth.values, "LF_imogimap vs leuco_methyl"),
            (leuko_im.values, imm_score.values, "LF_imogimap vs ImmuneScore"),
            (leuko_meth.values, imm_score.values, "leuco_methyl vs ImmuneScore"),
            (leuko_im.values, absol.values, "LF_imogimap vs ABSOLUTE"),
            (leuko_meth.values, absol.values, "leuco_methyl vs ABSOLUTE")]:
        m = ~np.isnan(a) & ~np.isnan(b)
        r, p = stats.pearsonr(a[m], b[m])
        verif[lab] = {"r": float(r), "p": float(p), "n": int(m.sum())}
        print(f"VERIF {lab}: r={r:+.4f} p={p:.2e} n={int(m.sum())}")
    # Biais de selection des 26 tout-NaN : comparer les distributions.
    nan_grp = matched_mask & ~complete
    for lab, arr in [("ImmuneScore", imm_score.values),
                     ("LF_imogimap", leuko_im.values),
                     ("leuco_methyl", leuko_meth.values)]:
        a, b = arr[keep], arr[nan_grp]
        m1, m2 = ~np.isnan(a), ~np.isnan(b)
        print(f"SELECTION {lab}: complets med={np.nanmedian(a):.4f} (n={int(m1.sum())}) "
              f"vs tout-NaN med={np.nanmedian(b):.4f} (n={int(m2.sum())})")

    # --- Circularite LM22 (comptee en machine) ---
    lm = pd.read_csv(D + "LM22.txt", sep="\t")
    assert lm.shape == (547, 23)
    lm_genes = set(lm["Gene symbol"].astype(str))
    lm_flux = sorted(set(IMM_GENES) & lm_genes)
    print(f"LM22: 547 genes ; flux presents comme lignes LM22: {lm_flux} "
          f"({len(lm_flux)}/12 ; absents: {sorted(set(IMM_GENES) - lm_genes)})")
    # Marqueurs row-max par type : gene dont la colonne du type est le max
    # de la ligne (egalites : tous les maxima comptes).
    lm_map = {"B cells naive": "B.Cells.Naive", "B cells memory": "B.Cells.Memory",
              "Plasma cells": "Plasma.Cells", "T cells CD8": "T.Cells.CD8",
              "T cells CD4 naive": "T.Cells.CD4.Naive",
              "T cells CD4 memory resting": "T.Cells.CD4.Memory.Resting",
              "T cells CD4 memory activated": "T.Cells.CD4.Memory.Activated",
              "T cells follicular helper": "T.Cells.Follicular.Helper",
              "T cells regulatory (Tregs)": "T.Cells.Regulatory.Tregs",
              "T cells gamma delta": "T.Cells.gamma.delta",
              "NK cells resting": "NK.Cells.Resting",
              "NK cells activated": "NK.Cells.Activated",
              "Monocytes": "Monocytes", "Macrophages M0": "Macrophages.M0",
              "Macrophages M1": "Macrophages.M1",
              "Macrophages M2": "Macrophages.M2",
              "Dendritic cells resting": "Dendritic.Cells.Resting",
              "Dendritic cells activated": "Dendritic.Cells.Activated",
              "Mast cells resting": "Mast.Cells.Resting",
              "Mast cells activated": "Mast.Cells.Activated",
              "Eosinophils": "Eosinophils", "Neutrophils": "Neutrophils"}
    assert set(lm_map.values()) == set(types) and len(lm_map) == 22
    vals = lm[list(lm_map.keys())].values.astype(float)
    rowmax = vals.max(axis=1, keepdims=True)
    markers = {}
    for j, lm_col in enumerate(lm_map.keys()):
        g = lm["Gene symbol"].values[(vals[:, j] == rowmax[:, 0])]
        markers[lm_map[lm_col]] = sorted(set(g.tolist()) & set(IMM_GENES))
    print("Marqueurs row-max LM22 parmi les 12 flux, par type : "
          + json.dumps({k: v for k, v in markers.items() if v}, ensure_ascii=False))

    # --- T1 : chaque flux suit-il un type ? ---
    t1 = []
    for t in types:
        x = Fk[t].values.astype(float)
        rs, rhos, ps, r2s = [], [], [], []
        for j, g in enumerate(IMM_GENES):
            r, p = stats.pearsonr(x, Y[:, j])
            rho, _ = stats.spearmanr(x, Y[:, j])
            rs.append(r); rhos.append(rho); ps.append(p); r2s.append(r ** 2)
        t1.append({"type": t, "n": n_eff, "mean_abs_r": float(np.mean(np.abs(rs))),
                   "mean_abs_rho": float(np.mean(np.abs(rhos))),
                   "median_abs_r": float(np.median(np.abs(rs))),
                   "median_R2": float(np.median(r2s)), "max_R2": float(np.max(r2s)),
                   "r_par_flux": {g: float(v) for g, v in zip(IMM_GENES, rs)},
                   "p_par_flux": {g: float(v) for g, v in zip(IMM_GENES, ps)}})
    t1s = sorted(t1, key=lambda d: (-d["mean_abs_r"], -d["mean_abs_rho"]))
    for d in t1s:
        print(f"T1 {d['type']:32s} mean|r|={d['mean_abs_r']:.4f} "
              f"mean|rho|={d['mean_abs_rho']:.4f} medR2={d['median_R2']:.3f}")
    top = [d["type"] for d in t1s[:3]]
    top1, top2, top3 = top
    print(f"TOP1={top1} TOP2={top2} TOP3={top3}")
    # Descriptif : chaque type vs ImmuneScore / ABSOLUTE.
    desc = {}
    for t in types:
        x = Fk[t].values.astype(float)
        row = {}
        for lab, arr_full in [("ImmuneScore", imm_score.values),
                              ("ABSOLUTE", absol.values),
                              ("LF_imogimap", leuko_im.values)]:
            arr = arr_full[keep]
            m = ~np.isnan(arr)
            r, _ = stats.pearsonr(x[m], arr[m])
            row[lab] = float(r)
        desc[t] = row
    print("Descriptif r(type, ImmuneScore) TOP1/TOP2:",
          {t: round(desc[t]["ImmuneScore"], 4) for t in top[:2]})

    # --- T2 : cohesion brute vs residus ---
    flux_df = pd.DataFrame(Y, columns=IMM_GENES)
    brute = cohesion(flux_df)
    print(f"T2 brute (n={n_eff}): mean|r|={brute['mean_abs_r']:.4f} "
          f"frac>0.5={brute['frac_gt_0.5']:.3f} ({brute['n_gt_0.5']}/66)")
    X1 = Fk[[top1]].values.astype(float)
    R_a = resid_ols(Y, X1)
    coh_a = cohesion(pd.DataFrame(R_a, columns=IMM_GENES))
    R_b = resid_ols(Y, Fk[top[:3]].values.astype(float))
    coh_b = cohesion(pd.DataFrame(R_b, columns=IMM_GENES))
    qual = [d["type"] for d in t1s if d["mean_abs_r"] >= 0.30][:5]
    R_c = resid_ols(Y, Fk[qual].values.astype(float))
    coh_c = cohesion(pd.DataFrame(R_c, columns=IMM_GENES))
    print(f"T2 (a) residus [TOP1={top1}]: mean|r|={coh_a['mean_abs_r']:.4f} "
          f"frac>0.5={coh_a['frac_gt_0.5']:.3f} chute="
          f"{100 * (1 - coh_a['mean_abs_r'] / brute['mean_abs_r']):.1f}%")
    print(f"T2 (b) residus [TOP1-3]: mean|r|={coh_b['mean_abs_r']:.4f} "
          f"frac>0.5={coh_b['frac_gt_0.5']:.3f}")
    print(f"T2 (c) residus [types mean|r|>=0.30: {qual}]: "
          f"mean|r|={coh_c['mean_abs_r']:.4f} frac>0.5={coh_c['frac_gt_0.5']:.3f}")
    # (d) paires sans marqueur row-max du TOP1.
    mk = set(markers.get(top1, []))
    keep_genes = [g for g in IMM_GENES if g not in mk]
    sub_a = pd.DataFrame(R_a, columns=IMM_GENES)[keep_genes]
    sub_b = flux_df[keep_genes]
    coh_d = cohesion(sub_a)
    coh_d_brute = cohesion(sub_b)
    print(f"T2 (d) paires sans marqueur row-max {top1} {sorted(mk)}: "
          f"{len(keep_genes)} genes, {coh_d['n_pairs']} paires, "
          f"brute={coh_d_brute['mean_abs_r']:.4f} -> residuelle={coh_d['mean_abs_r']:.4f}")

    # --- T3 : couplage predit ---
    def coupling(Ym):
        cs = []
        for j in range(12):
            others = [k for k in range(12) if k != j]
            cs.append(np.mean([abs(np.corrcoef(Ym[:, j], Ym[:, k])[0, 1])
                               for k in others]))
        return float(np.mean(cs)), cs
    C_brut, _ = coupling(Y)
    C_res, c_res_list = coupling(R_a)
    d_pred_brut = -0.175 + 1.705 * C_brut
    d_pred_res = -0.175 + 1.705 * C_res
    print(f"T3 C brut={C_brut:.4f} d_pred={d_pred_brut:.4f} ; "
          f"C residuel TOP1={C_res:.4f} d_pred={d_pred_res:.4f}")
    cd8a_idx = IMM_GENES.index("CD8A")
    print(f"T3 CD8A seul: C brut={coupling(Y)[1][cd8a_idx]:.4f} -> "
          f"C residuel={c_res_list[cd8a_idx]:.4f} "
          f"d_pred={-0.175 + 1.705 * c_res_list[cd8a_idx]:.4f}")

    # --- T4 : stratification mediane TOP1 ---
    med = float(np.median(Fk[top1].values))
    hi = Fk[top1].values >= med
    coh_hi = cohesion(flux_df[hi])
    coh_lo = cohesion(flux_df[~hi])
    sd_g = float(np.std(Fk[top1].values))
    print(f"T4 mediane {top1}={med:.4f} (n={int(hi.sum())}/{int((~hi).sum())}): "
          f"haute mean|r|={coh_hi['mean_abs_r']:.4f} (ET {top1} "
          f"{float(np.std(Fk[top1].values[hi])):.4f}), basse "
          f"mean|r|={coh_lo['mean_abs_r']:.4f} (ET "
          f"{float(np.std(Fk[top1].values[~hi])):.4f}) vs ET global {sd_g:.4f}")

    # --- Bras L : fraction leucocytaire par methylation (detenue) ---
    lm_arr = leuko_meth.values.astype(float)
    mL = ~np.isnan(lm_arr)
    nL = int(mL.sum())
    YL = Y_all[mL]
    rsL, rhosL, psL = [], [], []
    for j, g in enumerate(IMM_GENES):
        r, p = stats.pearsonr(lm_arr[mL], YL[:, j])
        rho, _ = stats.spearmanr(lm_arr[mL], YL[:, j])
        rsL.append(r); rhosL.append(rho); psL.append(p)
    meanL = float(np.mean(np.abs(rsL)))
    print(f"T1-L leuco_methyl (n={nL}): mean|r|={meanL:.4f} "
          f"mean|rho|={float(np.mean(np.abs(rhosL))):.4f}")
    bruteL = cohesion(pd.DataFrame(YL, columns=IMM_GENES))
    RL = resid_ols(YL, lm_arr[mL].reshape(-1, 1))
    cohL = cohesion(pd.DataFrame(RL, columns=IMM_GENES))
    print(f"T2-L brute (n={nL}): mean|r|={bruteL['mean_abs_r']:.4f} -> "
          f"residuelle={cohL['mean_abs_r']:.4f} "
          f"chute={100 * (1 - cohL['mean_abs_r'] / bruteL['mean_abs_r']):.1f}% "
          f"frac>0.5={cohL['frac_gt_0.5']:.3f}")
    # T3-L couplage.
    CL_brut, _ = coupling(YL)
    CL_res, _ = coupling(RL)
    print(f"T3-L C brut={CL_brut:.4f} d_pred={-0.175 + 1.705 * CL_brut:.4f} ; "
          f"C residuel={CL_res:.4f} d_pred={-0.175 + 1.705 * CL_res:.4f}")

    # --- Fichiers externes apparies ---
    ext = pd.DataFrame({"sample": samples})
    for t in types:
        ext[t] = F[t].values
    ext["Leukocyte_fraction_imogimap"] = leuko_im.values
    ext["Leukocyte_fraction_methylation_Raphael"] = lm_arr
    ext["ABSOLUTE"] = absol.values
    ext["ImmuneScore_854"] = imm_score.values
    ext.to_csv(BASE + "/deconvolution_860_external.csv", index=False)

    res = {
        "porte_D": {"imcell_n_rows": int(im.shape[0]), "imcell_n_types": 22,
                    "leuko_n_rows": int(lk.shape[0]),
                    "appariees_imcell": int(matched_mask.sum()),
                    "non_appariees_imcell": samples[~matched_mask].tolist(),
                    "tout_nan_parmi_appariees": int((matched_mask & ~complete).sum()),
                    "n_effectif": n_eff,
                    "appariees_leuko_imogimap": int((~np.isnan(leuko_im.values)).sum()),
                    "n_leuco_methyl": nL},
        "verification": verif,
        "lm22_flux_rows": lm_flux,
        "marqueurs_rowmax_par_type": {k: v for k, v in markers.items() if v},
        "T1_par_type": t1s,
        "TOP1": top1, "TOP2": top2, "TOP3": top3,
        "descriptif_type_vs_scores": desc,
        "T2_brute": brute,
        "T2_resid_TOP1": coh_a,
        "T2_resid_TOP123": coh_b,
        "T2_resid_qualifiants": {"types": qual, **coh_c},
        "T2d_paires_sans_marqueur_TOP1": {"marqueurs_TOP1": sorted(mk),
                                          "genes_retenus": keep_genes,
                                          "brute": coh_d_brute,
                                          "residuelle": coh_d},
        "T3": {"C_brut": C_brut, "d_pred_brut": float(d_pred_brut),
               "C_residuel_TOP1": C_res, "d_pred_residuel": float(d_pred_res),
               "C_residuel_CD8A": float(c_res_list[cd8a_idx]),
               "d_pred_residuel_CD8A": float(-0.175 + 1.705 * c_res_list[cd8a_idx])},
        "T4": {"mediane_TOP1": med, "n_haute": int(hi.sum()), "n_basse": int((~hi).sum()),
               "coh_haute": coh_hi, "coh_basse": coh_lo,
               "ET_global_TOP1": sd_g,
               "ET_haute": float(np.std(Fk[top1].values[hi])),
               "ET_basse": float(np.std(Fk[top1].values[~hi]))},
        "bras_L": {"n": nL, "mean_abs_r": meanL,
                   "r_par_flux": {g: float(v) for g, v in zip(IMM_GENES, rsL)},
                   "p_par_flux": {g: float(v) for g, v in zip(IMM_GENES, psL)},
                   "T2L_brute": bruteL, "T2L_residuelle": cohL,
                   "T3L_C_brut": float(CL_brut),
                   "T3L_d_pred_brut": float(-0.175 + 1.705 * CL_brut),
                   "T3L_C_residuel": float(CL_res),
                   "T3L_d_pred_residuel": float(-0.175 + 1.705 * CL_res)},
    }
    with open(BASE + "/deconvolution_860_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    t1df = pd.DataFrame([{k: d[k] for k in
                          ["type", "n", "mean_abs_r", "mean_abs_rho",
                           "median_abs_r", "median_R2", "max_R2"]}
                         for d in t1s])
    t1df.to_csv(BASE + "/deconvolution_860_results.csv", index=False)
    print("Ecrits: deconvolution_860_external.csv, "
          "deconvolution_860_results.json/.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
