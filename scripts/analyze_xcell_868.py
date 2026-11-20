#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.68 — Porte D, jointure, identification, circularite, T1-T4 (xCell, 64 types).
Protocole gele : PROTOCOL_xcell_868.md
(SHA 416de4bcb783e0fc8390539a8104e7cd99b1d75355c42d4bff3e79c204c66c33).
Regles : SHAs verifies avant tout calcul ; cohesion brute RECALCULÉE sur le
sous-ensemble apparie, jamais importee ; p brutes sans correction ;
scores xCell publies (Additional file 6, Aran et al. 2017), jamais recalcules ;
types stromaux = Group 'Non-Hematopoietic' de MOESM7 'Spill - Seq' (RNA-seq).
"""
import hashlib
import json
import re

import numpy as np
import pandas as pd
from scipy import stats

BASE = "/home/hatch/workspace/runs/pdac-v6"
D = BASE + "/data_xcell_868/"
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
    "ext860": ("deconvolution_860_external.csv",
               "438d677aded8eaf74504f8bd89bfc2e578df32b4b31c64e94e64120b0f22d9cf"),
    "zip_epmc": ("data_xcell_868/epmc_5688663_supp.zip",
                 "93c9a7b0cd93d7c35ea844e917a9144c00f3f69dbe1488a87097372d3581d20c"),
    "moesm6": ("data_xcell_868/13059_2017_1349_MOESM6_ESM.tsv",
               "c731427c4a69f82c82bc2f3592116cc6fdc32e8f52b515e1055a9bb9822c51ec"),
    "moesm3": ("data_xcell_868/13059_2017_1349_MOESM3_ESM.xlsx",
               "31a7d8c45414100b87bbb25139e106ed95ab3ff5f43e54865f97664a77ad32bc"),
    "moesm7": ("data_xcell_868/13059_2017_1349_MOESM7_ESM.xlsx",
               "5f559c5b46b46248228630d8e6cc8e8efc362d94adcb77e5c100ea085b2ac03c"),
}


def sha(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def check(name, rel, expect):
    p = "/home/hatch/workspace/runs/" + rel if rel.startswith("biophysique") \
        else BASE + "/" + rel
    got = sha(p)
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

    # --- Porte D : scores xCell publies (MOESM6), lignes = types, colonnes = echantillons ---
    xc = pd.read_csv(D + "13059_2017_1349_MOESM6_ESM.tsv", sep="\t", index_col=0)
    assert xc.shape == (64, 9947), xc.shape
    assert int(xc.isna().sum().sum()) == 0
    types = list(xc.index)
    print(f"MOESM6: {xc.shape[0]} types x {xc.shape[1]} echantillons ; "
          f"valeurs min {float(xc.values.min()):.4f} max {float(xc.values.max()):.4f} ; 0 NaN")
    n_tcga = sum(1 for c in xc.columns if str(c).startswith("TCGA"))
    n_target = sum(1 for c in xc.columns if str(c).startswith("TARGET"))
    print(f"Colonnes: TCGA {n_tcga} + TARGET {n_target} = {n_tcga + n_target}")
    assert n_tcga + n_target == 9947
    # Jointure par patient (12 car.) : IDs xCell avec points -> tirets.
    xc_pat12 = {str(c).replace(".", "-")[:12]: c for c in xc.columns
                if str(c).startswith("TCGA")}
    assert len(xc_pat12) == n_tcga  # 0 doublon de cle patient
    matched = np.array([p in xc_pat12 for p in pat12])
    missing = samples[~matched].tolist()
    print(f"Porte D: xCell appariees {int(matched.sum())}/178 (absentes: {missing})")
    assert int(matched.sum()) >= 100
    keep = matched
    n_eff = int(keep.sum())
    # Scores alignes sur nos 178 tumeurs (ordre KRAS brut conserve).
    cols = [xc_pat12[p] for p in pat12[keep]]
    X = xc[cols].T
    X.index = pd.Series(samples[keep]).values
    assert list(X.columns) == types
    Y = Y_all[keep]
    samp_k = samples[keep]
    print(f"n effectif: {n_eff} (aucune ligne tout-NaN : 0 NaN dans MOESM6)")

    # --- Groupes stromaux (MOESM7 'Spill - Seq', documente) ---
    spill = pd.read_excel(D + "13059_2017_1349_MOESM7_ESM.xlsx",
                          sheet_name="Spill - Seq", header=0, index_col=0)
    assert list(spill.index) == types
    groups = spill["Group"].to_dict()
    stromal = sorted([t for t, g in groups.items() if g == "Non-Hematopoietic"])
    print(f"Groupes MOESM7: {dict(pd.Series(groups).value_counts())} ; "
          f"stromaux (Non-Hematopoietic, n={len(stromal)}): {stromal}")

    # --- Verification d'identification (descriptif, §4c) ---
    sc854 = pd.read_csv(BASE + "/infiltration_854_scores.csv").set_index("sample")
    ext855 = pd.read_csv(BASE + "/purity_855_external.csv").set_index("sample")
    ext860 = pd.read_csv(BASE + "/deconvolution_860_external.csv").set_index("sample")
    imm_score = sc854.reindex(pd.Series(samples))["ImmuneScore"]
    absol = ext855.reindex(pd.Series(samples))["purity_absolute"]
    cib_cd8 = ext860.reindex(pd.Series(samples))["T.Cells.CD8"]
    verif = {}
    for a, b, lab in [
            (X["CD8+ T-cells"].values, cib_cd8.values[keep],
             "xCell CD8+ T-cells vs CIBERSORT T.Cells.CD8 (§8.60)"),
            (X["CD8+ T-cells"].values, Y[:, 0],
             "xCell CD8+ T-cells vs flux CD8A"),
            (X["CD8+ T-cells"].values, imm_score.values[keep],
             "xCell CD8+ T-cells vs ImmuneScore (§8.54)"),
            (X["B-cells"].values, Y[:, 11],
             "xCell B-cells vs flux CD19"),
            (X["Macrophages"].values, Y[:, 4],
             "xCell Macrophages vs flux CD68")]:
        m = ~np.isnan(a) & ~np.isnan(b)
        r, p = stats.pearsonr(a[m], b[m])
        verif[lab] = {"r": float(r), "p": float(p), "n": int(m.sum())}
        print(f"VERIF {lab}: r={r:+.4f} p={p:.2e} n={int(m.sum())}")
    print("NOTE: pas de ligne ImmuneScore/StromaScore agregee dans MOESM6 "
          "(64 types seuls) : le controle §4c par ImmuneScore xCell est "
          "impossible sur ce fichier — remplace par CD8/B/Macrophages ci-dessus.")

    # --- Circularite (comptee en machine, §2.4) : union des signatures par type ---
    sig = pd.read_excel(D + "13059_2017_1349_MOESM3_ESM.xlsx",
                        sheet_name="xCell_signatures.txt", header=0)
    assert len(sig) == 489, len(sig)
    sig_genes = {}
    for _, row in sig.iterrows():
        sid = str(row["Celltype_Source_ID"])
        m = re.match(r"(.+)_([A-Z0-9]+)_\d+$", sid)
        typ = m.group(1) if m else sid
        genes = {str(v) for v in row.values[2:] if isinstance(v, str)}
        sig_genes.setdefault(typ, set()).update(genes)
    assert set(sig_genes.keys()) == set(types), (
        set(sig_genes.keys()) ^ set(types))
    circ = {}
    for t in types:
        inter = sorted(set(IMM_GENES) & sig_genes[t])
        circ[t] = {"n_genes_signature": len(sig_genes[t]),
                   "flux_dans_signature": inter,
                   "n_flux": len(inter)}
    n_with = sum(1 for t in types if circ[t]["n_flux"] > 0)
    print(f"Circularite: {n_with}/64 types contiennent >=1 des 12 flux ; "
          f"total flux-genes en signatures: "
          f"{sum(circ[t]['n_flux'] for t in types)} occurrences")
    for t in types:
        if circ[t]["n_flux"] > 0:
            print(f"  CIRC {t}: {circ[t]['flux_dans_signature']} "
                  f"({circ[t]['n_flux']}/12, signature {circ[t]['n_genes_signature']} genes)")

    # --- T1 : chaque flux suit-il un type xCell ? ---
    t1 = []
    for t in types:
        x = X[t].values.astype(float)
        rs, rhos, ps, r2s = [], [], [], []
        for j, g in enumerate(IMM_GENES):
            r, p = stats.pearsonr(x, Y[:, j])
            rho, _ = stats.spearmanr(x, Y[:, j])
            rs.append(r); rhos.append(rho); ps.append(p); r2s.append(r ** 2)
        t1.append({"type": t, "n": n_eff, "group": groups[t],
                   "mean_abs_r": float(np.mean(np.abs(rs))),
                   "mean_abs_rho": float(np.mean(np.abs(rhos))),
                   "median_abs_r": float(np.median(np.abs(rs))),
                   "median_R2": float(np.median(r2s)), "max_R2": float(np.max(r2s)),
                   "r_par_flux": {g: float(v) for g, v in zip(IMM_GENES, rs)},
                   "p_par_flux": {g: float(v) for g, v in zip(IMM_GENES, ps)}})
    t1s = sorted(t1, key=lambda d: (-d["mean_abs_r"], -d["mean_abs_rho"]))
    for d in t1s:
        print(f"T1 {d['type']:28s} [{d['group']:18s}] mean|r|={d['mean_abs_r']:.4f} "
              f"mean|rho|={d['mean_abs_rho']:.4f} medR2={d['median_R2']:.3f}")
    top = [d["type"] for d in t1s[:3]]
    top1, top2, top3 = top
    print(f"TOP1={top1} TOP2={top2} TOP3={top3}")
    top_strom = next(d["type"] for d in t1s if d["group"] == "Non-Hematopoietic")
    d_strom = next(d for d in t1s if d["type"] == top_strom)
    print(f"TOP-STROM={top_strom} mean|r|={d_strom['mean_abs_r']:.4f} "
          f"(rang {t1s.index(d_strom) + 1}/64)")
    # Descriptif : chaque type vs ImmuneScore / ABSOLUTE.
    desc = {}
    for t in types:
        x = X[t].values.astype(float)
        row = {}
        for lab, arr_full in [("ImmuneScore", imm_score.values),
                              ("ABSOLUTE", absol.values)]:
            arr = arr_full[keep]
            m = ~np.isnan(arr)
            r, _ = stats.pearsonr(x[m], arr[m])
            row[lab] = float(r)
        desc[t] = row
    print("Descriptif r(type, ImmuneScore) TOP1/TOP2/TOP-STROM:",
          {t: round(desc[t]["ImmuneScore"], 4) for t in [top1, top2, top_strom]})
    print("Descriptif r(type, ABSOLUTE) TOP1/TOP2/TOP-STROM:",
          {t: round(desc[t]["ABSOLUTE"], 4) for t in [top1, top2, top_strom]})

    # --- T2 : cohesion brute vs residus ---
    flux_df = pd.DataFrame(Y, columns=IMM_GENES)
    brute = cohesion(flux_df)
    print(f"T2 brute (n={n_eff}): mean|r|={brute['mean_abs_r']:.4f} "
          f"med={brute['median_abs_r']:.4f} frac>0.5={brute['frac_gt_0.5']:.3f} "
          f"({brute['n_gt_0.5']}/66) max={brute['max_abs_r']:.4f}")
    X1 = X[[top1]].values.astype(float)
    R_a = resid_ols(Y, X1)
    coh_a = cohesion(pd.DataFrame(R_a, columns=IMM_GENES))
    R_b = resid_ols(Y, X[top[:3]].values.astype(float))
    coh_b = cohesion(pd.DataFrame(R_b, columns=IMM_GENES))
    qual = [d["type"] for d in t1s if d["mean_abs_r"] >= 0.30][:5]
    if qual:
        R_c = resid_ols(Y, X[qual].values.astype(float))
        coh_c = cohesion(pd.DataFrame(R_c, columns=IMM_GENES))
    else:
        coh_c = None
    print(f"T2 (a) residus [TOP1={top1}]: mean|r|={coh_a['mean_abs_r']:.4f} "
          f"frac>0.5={coh_a['frac_gt_0.5']:.3f} chute="
          f"{100 * (1 - coh_a['mean_abs_r'] / brute['mean_abs_r']):.1f}%")
    print(f"T2 (b) residus [TOP1-3]: mean|r|={coh_b['mean_abs_r']:.4f} "
          f"frac>0.5={coh_b['frac_gt_0.5']:.3f} chute="
          f"{100 * (1 - coh_b['mean_abs_r'] / brute['mean_abs_r']):.1f}%")
    if coh_c is not None:
        print(f"T2 (c) residus [types mean|r|>=0.30: {qual}]: "
              f"mean|r|={coh_c['mean_abs_r']:.4f} frac>0.5={coh_c['frac_gt_0.5']:.3f} "
              f"chute={100 * (1 - coh_c['mean_abs_r'] / brute['mean_abs_r']):.1f}%")
    else:
        print("T2 (c) : AUCUN type a mean|r|>=0.30 — sensibilite (c) vide, a dire.")
    # (d) paires sans marqueur : genes de flux presents dans la signature du TOP1.
    mk = set(circ[top1]["flux_dans_signature"])
    keep_genes = [g for g in IMM_GENES if g not in mk]
    sub_a = pd.DataFrame(R_a, columns=IMM_GENES)[keep_genes]
    sub_b = flux_df[keep_genes]
    coh_d = cohesion(sub_a)
    coh_d_brute = cohesion(sub_b)
    print(f"T2 (d) paires sans marqueur signature {top1} {sorted(mk)}: "
          f"{len(keep_genes)} genes, {coh_d['n_pairs']} paires, "
          f"brute={coh_d_brute['mean_abs_r']:.4f} -> residuelle={coh_d['mean_abs_r']:.4f} "
          f"chute={100 * (1 - coh_d['mean_abs_r'] / coh_d_brute['mean_abs_r']):.1f}%")

    # --- T3 : couplage predit ---
    def coupling(Ym):
        cs = []
        for j in range(12):
            others = [k for k in range(12) if k != j]
            cs.append(float(np.mean([abs(np.corrcoef(Ym[:, j], Ym[:, k])[0, 1])
                                     for k in others])))
        return cs
    cs_brut = coupling(Y)
    cs_res = coupling(R_a)
    d_pred_brut = -0.175 + 1.705 * float(np.mean(cs_brut))
    d_pred_res = -0.175 + 1.705 * float(np.mean(cs_res))
    print(f"T3 C brut moyen={float(np.mean(cs_brut)):.4f} d_pred={d_pred_brut:+.4f} ; "
          f"C residuel moyen={float(np.mean(cs_res)):.4f} d_pred={d_pred_res:+.4f}")
    c_cd8a_brut = cs_brut[0]
    c_cd8a_res = cs_res[0]
    print(f"T3 CD8A seul: C {c_cd8a_brut:.4f} -> {c_cd8a_res:.4f}, "
          f"d_pred {-0.175 + 1.705 * c_cd8a_brut:+.4f} -> "
          f"{-0.175 + 1.705 * c_cd8a_res:+.4f}")

    # --- T4 : stratification par TOP1 ---
    x1 = X[top1].values.astype(float)
    med = float(np.median(x1))
    hi = x1 >= med
    lo = ~hi
    coh_hi = cohesion(flux_df[hi])
    coh_lo = cohesion(flux_df[lo])
    print(f"T4 {top1} mediane={med:.4f} (n hi={int(hi.sum())} lo={int(lo.sum())}) : "
          f"haute mean|r|={coh_hi['mean_abs_r']:.4f} frac>0.5={coh_hi['frac_gt_0.5']:.3f} ; "
          f"basse mean|r|={coh_lo['mean_abs_r']:.4f} frac>0.5={coh_lo['frac_gt_0.5']:.3f}")
    print(f"T4 ecarts-types {top1}: global={float(np.std(x1)):.4f} "
          f"haute={float(np.std(x1[hi])):.4f} basse={float(np.std(x1[lo])):.4f} "
          f"(basse/global={float(np.std(x1[lo]) / np.std(x1)):.3f})")

    # --- Sorties ---
    ext = pd.DataFrame({"sample": samp_k})
    for t in types:
        ext[t] = X[t].values
    ext["ImmuneScore_854"] = imm_score.values[keep]
    ext["ABSOLUTE_855"] = absol.values[keep]
    ext.to_csv(BASE + "/xcell_868_external.csv", index=False)
    t1_out = [{k: d[k] for k in ("type", "n", "group", "mean_abs_r", "mean_abs_rho",
                                 "median_abs_r", "median_R2", "max_R2",
                                 "r_par_flux", "p_par_flux")} for d in t1s]
    results = {
        "n_eff": n_eff, "n_matched": int(matched.sum()), "n_missing": missing,
        "types": types, "groups": groups, "stromal_types": stromal,
        "top1": top1, "top2": top2, "top3": top3, "top_strom": top_strom,
        "top_strom_mean_abs_r": d_strom["mean_abs_r"],
        "top_strom_rank": t1s.index(d_strom) + 1,
        "verif": verif, "circularity": circ, "desc": desc,
        "t1": t1_out,
        "t2_brute": brute,
        "t2_a": coh_a, "t2_b": coh_b, "t2_c": coh_c,
        "t2_d": {"markers_top1": sorted(mk), "keep_genes": keep_genes,
                 "brute": coh_d_brute, "residuelle": coh_d},
        "t3": {"C_brut_moyen": float(np.mean(cs_brut)), "d_pred_brut": d_pred_brut,
               "C_res_moyen": float(np.mean(cs_res)), "d_pred_res": d_pred_res,
               "C_CD8A_brut": c_cd8a_brut, "C_CD8A_res": c_cd8a_res,
               "d_pred_CD8A_brut": -0.175 + 1.705 * c_cd8a_brut,
               "d_pred_CD8A_res": -0.175 + 1.705 * c_cd8a_res},
        "t4": {"top1": top1, "median": med, "n_hi": int(hi.sum()), "n_lo": int(lo.sum()),
               "coh_hi": coh_hi, "coh_lo": coh_lo,
               "sd_global": float(np.std(x1)), "sd_hi": float(np.std(x1[hi])),
               "sd_lo": float(np.std(x1[lo]))},
    }
    with open(BASE + "/xcell_868_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    t1_df = pd.DataFrame([{k: d[k] for k in ("type", "group", "mean_abs_r",
                                             "mean_abs_rho", "median_abs_r",
                                             "median_R2", "max_R2")}
                          for d in t1s])
    for g in IMM_GENES:
        t1_df[f"r_{g}"] = [d["r_par_flux"][g] for d in t1s]
    t1_df.to_csv(BASE + "/xcell_868_results.csv", index=False)
    print("Ecrit : xcell_868_external.csv, xcell_868_results.json, xcell_868_results.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
