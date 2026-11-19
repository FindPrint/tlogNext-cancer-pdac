#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyse §8.48 — domination IMMROT : couplage controle-flux vs S_sep.
Protocole gele : PROTOCOL_immrot_domination.md (SHA 465b4f54...).
Ne modifie jamais le pipeline. Lit seulement les CSV existants + le tarball
TCGA (porte G). Sorties : immrot_848_correlations.csv/.json,
immrot_848_dfull.csv, immrot_848_gate.json.
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd
from scipy import stats

OUT = "/home/hatch/workspace/runs/pdac-v6"
DATA = f"{OUT}/data"
V62 = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"

EXPECTED = {
    "pdac_tcga_fluxes_v4.csv": "e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0",
    "pdac_depmap_fluxes.csv": "7d605fefb412fe16151a1b2508dffa6a1c2b8353600dccffd4af3333198e37f8",
    "pdac_immune_tcga_fluxes.csv": "66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e",
    "pdac_tcga_fluxes_parp.csv": "c9549b68280b2f4ca3d9b62020efa21ab97249b10e176de87ec528a0258c4309",
    "ssep_844_rotations.csv": "d1abc0aba2e480e611b87dea2861ef5bd96a83a196e1b8736b596506653fc999",
    "ssep_841_rotations.csv": "1d3b28a4ffa488ecb098d80692ba3fe077a1fc75ae6d220951b138147a3d58ab",
}
V62_SHA = "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"

FAMILIES = {
    "V4ROT": ("pdac_tcga_fluxes_v4.csv", "pdac_tcga_v4_fluxes_v4rot_{}.csv",
              "pdac_tcga_v4_fluxes_v4rot_{}_dedup.csv",
              "pdac_tcga_v4_fluxes_v4rot_{}_dedup_nul.csv"),
    "DEPMAPROT": ("pdac_depmap_fluxes.csv", "pdac_depmap_fluxes_depmaprot_{}.csv",
                  "pdac_depmap_fluxes_depmaprot_{}_dedup.csv",
                  "pdac_depmap_fluxes_depmaprot_{}_dedup_nul.csv"),
    "IMMROT": ("pdac_immune_tcga_fluxes.csv", "pdac_immune_tcga_fluxes_immrot_{}.csv",
               "pdac_immune_tcga_fluxes_immrot_{}_dedup.csv",
               "pdac_immune_tcga_fluxes_immrot_{}_dedup_nul.csv"),
    "PARPROT": ("pdac_tcga_fluxes_parp.csv", "pdac_parp_tcga_fluxes_parprot_{}.csv",
                "pdac_parp_tcga_fluxes_parprot_{}_dedup.csv",
                "pdac_parp_tcga_fluxes_parprot_{}_dedup_nul.csv"),
}
# Paires §8.41 non refaites en §8.44 (meme permutation) : fichiers dedup specifiques
DEDUP_841_SPECIAL = {
    ("V4ROT", "CLDN18"): ("pdac_tcga_fluxes_v4r_cldn18_dedup.csv",
                          "pdac_tcga_fluxes_v4r_cldn18_dedup_nul.csv"),
    ("IMMROT", "CTLA4"): ("pdac_immune_tcga_fluxes_immrot_CTLA4_dedup.csv",
                          "pdac_immune_tcga_fluxes_immrot_CTLA4_dedup_nul.csv"),
    ("DEPMAPROT", "ACO2"): ("pdac_depmap_fluxes_depmaprot_ACO2_dedup.csv",
                            "pdac_depmap_fluxes_depmaprot_ACO2_dedup_nul_sameperm.csv"),
    ("PARPROT", "PARP1"): ("pdac_parp_tcga_fluxes_parprot_PARP1_dedup.csv",
                           "pdac_parp_tcga_fluxes_parprot_PARP1_dedup_nul_sameperm.csv"),
}


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


def cohen_d(a, b):
    """d de Cohen, formule pipeline : ecart-type poolé = sqrt((v1+v2)/2), v ddof=1."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) < 2 or len(b) < 2:
        return np.nan
    m1, m2 = float(np.mean(a)), float(np.mean(b))
    v1 = float(np.var(a, ddof=1))
    v2 = float(np.var(b, ddof=1))
    pooled = np.sqrt((v1 + v2) / 2.0)
    if pooled == 0.0 or not np.isfinite(pooled):
        return 0.0 if m1 == m2 else np.nan
    return (m1 - m2) / pooled


def offdiag_mean_abs(corr):
    vals = corr.values[np.triu_indices_from(corr.values, k=1)]
    return float(np.mean(np.abs(vals))), float(np.median(np.abs(vals))), \
        float(np.mean(np.abs(vals) > 0.5)), int(np.sum(np.abs(vals) > 0.5))


def main():
    # --- 0. Vérifications SHA gelées (arrêt si mismatch) ---
    checks = {}
    for fname, exp in EXPECTED.items():
        got = sha(f"{OUT}/{fname}")
        checks[fname] = {"ok": got == exp, "sha": got}
        assert got == exp, f"SHA MISMATCH {fname}: {got} != {exp}"
    v62 = sha(V62)
    assert v62 == V62_SHA, f"SHA pipeline v6.2 mismatch: {v62}"
    checks["v6.2"] = {"ok": True, "sha": v62}
    print("SHA: 6 fichiers + pipeline v6.2 conformes.")

    s844 = pd.read_csv(f"{OUT}/ssep_844_rotations.csv")
    s841 = pd.read_csv(f"{OUT}/ssep_841_rotations.csv")
    assert len(s844) == 48 and len(s841) == 48
    d844 = {(r.famille, r.controle): r for r in s844.itertuples()}
    d841 = {(r.famille, r.controle): r for r in s841.itertuples()}
    assert set(d844) == set(d841), "paires 844/841 differentes"

    rows = []
    fam_summary = {}
    # --- (b) matrices de correlation par famille (base) ---
    for fam, (base_file, _, _, _) in FAMILIES.items():
        base = pd.read_csv(f"{OUT}/{base_file}")
        flux = [c for c in base.columns if c != "step"]
        assert len(flux) == 12
        cp = base[flux].corr(method="pearson")
        cs = base[flux].corr(method="spearman")
        mp, medp, fracp, cntp = offdiag_mean_abs(cp)
        ms, meds, fracs, cnts = offdiag_mean_abs(cs)
        # plus forte / plus faible paire (Pearson, hors diagonale)
        iu = np.triu_indices(12, k=1)
        avals = np.abs(cp.values[iu])
        order = np.argsort(avals)
        pairs = [(flux[iu[0][k]], flux[iu[1][k]], float(cp.values[iu[0][k], iu[1][k]]))
                 for k in range(len(avals))]
        fam_summary[fam] = {
            "n": int(base.shape[0]), "flux": flux,
            "pearson_mean_abs": mp, "pearson_median_abs": medp,
            "pearson_frac_gt_0.5": fracp, "pearson_count_gt_0.5": cntp,
            "spearman_mean_abs": ms, "spearman_median_abs": meds,
            "spearman_frac_gt_0.5": fracs, "spearman_count_gt_0.5": cnts,
            "strongest_pair": pairs[order[-1]], "weakest_pair": pairs[order[0]],
            "pearson_matrix": [[round(float(x), 4) for x in row] for row in cp.values],
            "spearman_matrix": [[round(float(x), 4) for x in row] for row in cs.values],
        }
        print(f"{fam}: Pearson mean|r|={mp:.4f} med={medp:.4f} frac>0.5={fracp:.3f} "
              f"| Spearman mean|r|={ms:.4f}")

    # --- (c) couplage / cohésion par rotation + D_full sur les 96 CSV dédoublonnés ---
    dfull_rows = []
    per_flux_rows = []
    for (fam, ctrl), r844 in sorted(d844.items()):
        base_file, _, dedup_pat, dedup_nul_pat = FAMILIES[fam]
        if (fam, ctrl) in DEDUP_841_SPECIAL:
            dedup_file, dedup_nul_file = DEDUP_841_SPECIAL[(fam, ctrl)]
        else:
            dedup_file = dedup_pat.format(ctrl)
            dedup_nul_file = dedup_nul_pat.format(ctrl)
        base = pd.read_csv(f"{OUT}/{base_file}")
        flux = [c for c in base.columns if c != "step"]
        others = [c for c in flux if c != ctrl]
        # couplage / cohésion sur la BASE
        cp = base[flux].corr(method="pearson")
        cs = base[flux].corr(method="spearman")
        c_c = float(np.mean([abs(cp.loc[ctrl, j]) for j in others]))
        c_c_s = float(np.mean([abs(cs.loc[ctrl, j]) for j in others]))
        sub_p = cp.loc[others, others].values[np.triu_indices(11, k=1)]
        sub_s = cs.loc[others, others].values[np.triu_indices(11, k=1)]
        h_c = float(np.mean(np.abs(sub_p)))
        h_c_s = float(np.mean(np.abs(sub_s)))
        # mêmes quantités sur CSV dédoublonnés réel et nul (vérification d'invariance)
        dre = pd.read_csv(f"{OUT}/{dedup_file}")
        dnu = pd.read_csv(f"{OUT}/{dedup_nul_file}")
        assert list(dre.columns[0:1]) == [ctrl] and len(dre.columns) == 12, \
            f"{dedup_file}: colonnes {list(dre.columns)}"
        assert list(dnu.columns[0:1]) == [ctrl] and len(dnu.columns) == 12
        assert dre.shape[0] == dnu.shape[0] == base.shape[0]
        ana_re = list(dre.columns[1:])
        assert ana_re == others or set(ana_re) == set(others), \
            f"{dedup_file}: flux analyses {ana_re} != {others}"
        cpr = dre.corr(method="pearson")
        c_c_re = float(np.mean([abs(cpr.loc[ctrl, j]) for j in ana_re]))
        cpn = dnu.corr(method="pearson")
        csn = dnu.corr(method="spearman")
        c_c_nul = float(np.mean([abs(cpn.loc[ctrl, j]) for j in ana_re]))
        c_c_nul_s = float(np.mean([abs(csn.loc[ctrl, j]) for j in ana_re]))
        sub_n = cpn.loc[ana_re, ana_re].values[np.triu_indices(11, k=1)]
        h_c_nul = float(np.mean(np.abs(sub_n)))
        # D_full : coupure pleine, lignes déjà triées par le contrôle
        for tag, dfr, maxsep_pipe in (("reel", dre, r844.maxsep_R),
                                      ("nul", dnu, r844.maxsep_N)):
            ctrl_vals = dfr[ctrl].values.astype(float)
            order_idx = np.argsort(ctrl_vals, kind="stable")
            dsorted = dfr.iloc[order_idx].reset_index(drop=True)
            n = len(dsorted)
            best, best_k, d_med = -1.0, -1, np.nan
            for k in range(20, n - 19):
                ds = [abs(cohen_d(dsorted[j].values[:k], dsorted[j].values[k:]))
                      for j in ana_re]
                m = float(np.nanmean(ds))
                if m > best:
                    best, best_k = m, k
                if k == n // 2:
                    d_med = m
            dfull_rows.append({
                "famille": fam, "controle": ctrl, "type": tag, "n": n,
                "D_full": best, "k_best": best_k,
                "D_med": d_med, "maxsep_pipeline": float(maxsep_pipe),
                "diff_Dfull_maxsep": best - float(maxsep_pipe),
            })
        # par flux à la médiane (réel) : d observé vs prédiction bivariée-normale
        n = len(dre)
        kmed = n // 2
        dsorted = dre.iloc[np.argsort(dre[ctrl].values, kind="stable")].reset_index(drop=True)
        for j in ana_re:
            r_j = float(cp.loc[ctrl, j])
            d_obs = cohen_d(dsorted[j].values[:kmed], dsorted[j].values[kmed:])
            d_pred = 1.5958 * r_j / np.sqrt(max(1e-12, 1 - 0.6366 * r_j * r_j))
            per_flux_rows.append({
                "famille": fam, "controle": ctrl, "flux": j, "n": n,
                "r_pearson_ctrl_flux": r_j, "d_obs_mediane": float(d_obs),
                "d_pred_bivarie": float(d_pred),
            })
        r841 = d841[(fam, ctrl)]
        rows.append({
            "famille": fam, "controle": ctrl, "n": int(base.shape[0]),
            "C_couplage_pearson": c_c, "C_couplage_spearman": c_c_s,
            "H_cohesion_pearson": h_c, "H_cohesion_spearman": h_c_s,
            "C_couplage_dedup_reel": c_c_re,
            "C_couplage_nul": c_c_nul, "C_couplage_nul_spearman": c_c_nul_s,
            "H_cohesion_nul": h_c_nul,
            "d_ssep_sans_doublon": float(r844.d_ssep),
            "d_ssep_avec_doublon": float(r841.d_ssep),
            "perte_doublon": float(r841.d_ssep - r844.d_ssep),
            "S_sep_reel_sans": float(r844.ssep_R), "S_sep_nul_sans": float(r844.ssep_N),
            "S_sep_reel_avec": float(r841.ssep_R), "S_sep_nul_avec": float(r841.ssep_N),
            "maxsep_reel_sans": float(r844.maxsep_R), "maxsep_nul_sans": float(r844.maxsep_N),
        })
    corr_df = pd.DataFrame(rows)
    corr_df.to_csv(f"{OUT}/immrot_848_correlations.csv", index=False)
    dfull_df = pd.DataFrame(dfull_rows)
    dfull_df.to_csv(f"{OUT}/immrot_848_dfull.csv", index=False)
    per_flux_df = pd.DataFrame(per_flux_rows)
    per_flux_df.to_csv(f"{OUT}/immrot_848_per_flux_mediane.csv", index=False)

    # --- vérification d'invariance : C_c base vs C_c CSV dédoublonné ---
    inv = np.abs(corr_df["C_couplage_pearson"] - corr_df["C_couplage_dedup_reel"])
    print(f"Invariance C_c base vs dedup: max|diff|={inv.max():.2e}")

    # --- (c) tests principaux ---
    def pearson_spearman(x, y):
        rp, pp = stats.pearsonr(x, y)
        rs, ps = stats.spearmanr(x, y)
        return {"pearson_r": float(rp), "pearson_p": float(pp),
                "spearman_rho": float(rs), "spearman_p": float(ps),
                "n": int(len(x))}

    tests = {}
    tests["C_vs_d_ssep_sans_doublon"] = pearson_spearman(
        corr_df["C_couplage_pearson"], corr_df["d_ssep_sans_doublon"])
    tests["C_spearman_vs_d_ssep_sans_doublon"] = pearson_spearman(
        corr_df["C_couplage_spearman"], corr_df["d_ssep_sans_doublon"])
    tests["C_vs_d_ssep_avec_doublon"] = pearson_spearman(
        corr_df["C_couplage_pearson"], corr_df["d_ssep_avec_doublon"])
    tests["H_vs_d_ssep_sans_doublon"] = pearson_spearman(
        corr_df["H_cohesion_pearson"], corr_df["d_ssep_sans_doublon"])
    tests["C_vs_Ssep_nul_sans"] = pearson_spearman(
        corr_df["C_couplage_pearson"], corr_df["S_sep_nul_sans"])
    tests["H_vs_Ssep_nul_sans"] = pearson_spearman(
        corr_df["H_cohesion_pearson"], corr_df["S_sep_nul_sans"])
    # régression d_ssep ~ a + b*C
    slope, intercept, rval, pval, stderr = stats.linregress(
        corr_df["C_couplage_pearson"], corr_df["d_ssep_sans_doublon"])
    tests["regression_d_ssep_sur_C"] = {
        "intercept": float(intercept), "slope": float(slope),
        "R2": float(rval ** 2), "p": float(pval), "stderr_slope": float(stderr)}
    # par famille (descriptif) : C et H séparément (mêmes paires disjointe)
    for fam in ["V4ROT", "DEPMAPROT", "IMMROT", "PARPROT"]:
        sub = corr_df[corr_df["famille"] == fam]
        tests[f"par_famille_{fam}"] = {
            "n": int(len(sub)),
            "C_moyen": float(sub["C_couplage_pearson"].mean()),
            "H_moyen": float(sub["H_cohesion_pearson"].mean()),
            "d_ssep_moyen_sans": float(sub["d_ssep_sans_doublon"].mean()),
            "d_ssep_moyen_avec": float(sub["d_ssep_avec_doublon"].mean()),
            "r_C_d_ssep": float(stats.pearsonr(sub["C_couplage_pearson"],
                                                sub["d_ssep_sans_doublon"])[0]),
            "r_H_d_ssep": float(stats.pearsonr(sub["H_cohesion_pearson"],
                                                sub["d_ssep_sans_doublon"])[0]),
            "r_C_H": float(stats.pearsonr(sub["C_couplage_pearson"],
                                           sub["H_cohesion_pearson"])[0]),
        }
    # corrélation globale C vs H (confusion possible au niveau famille)
    tests["C_vs_H_global"] = pearson_spearman(
        corr_df["C_couplage_pearson"], corr_df["H_cohesion_pearson"])
    # (d1) sanité du nul
    tests["sanite_nul"] = {
        "C_nul_moyen": float(corr_df["C_couplage_nul"].mean()),
        "C_nul_ecart_type": float(corr_df["C_couplage_nul"].std(ddof=1)),
        "C_nul_max": float(corr_df["C_couplage_nul"].max()),
        "H_nul_moins_H_reel_moyen": float((corr_df["H_cohesion_nul"]
                                           - corr_df["H_cohesion_pearson"]).mean()),
        "H_nul_moins_H_reel_ecart_type": float((corr_df["H_cohesion_nul"]
                                                - corr_df["H_cohesion_pearson"]).std(ddof=1)),
    }
    # (b3) D_full vs maxsep pipeline
    for tag in ["reel", "nul"]:
        sub = dfull_df[dfull_df["type"] == tag]
        rp, pp = stats.pearsonr(sub["D_full"], sub["maxsep_pipeline"])
        tests[f"D_full_vs_maxsep_{tag}"] = {
            "pearson_r": float(rp), "p": float(pp), "n": int(len(sub)),
            "ecart_moyen_abs": float(np.mean(np.abs(sub["diff_Dfull_maxsep"]))),
            "ecart_moyen_signe": float(np.mean(sub["diff_Dfull_maxsep"])),
        }
    rp, pp = stats.pearsonr(dfull_df["D_full"], dfull_df["maxsep_pipeline"])
    tests["D_full_vs_maxsep_tous"] = {
        "pearson_r": float(rp), "p": float(pp), "n": int(len(dfull_df)),
        "ecart_moyen_abs": float(np.mean(np.abs(dfull_df["diff_Dfull_maxsep"]))),
        "ecart_moyen_signe": float(np.mean(dfull_df["diff_Dfull_maxsep"])),
    }
    # per-flux médiane : |d| observé vs |d| prédit.
    # CORRECTION (19 nov., avant rédaction de la section) : la première version
    # comparait d_obs SIGNÉ (bas−haut : négatif quand r>0, car le groupe 1 est
    # le bas du contrôle) à d_pred SIGNÉ (haut−bas, positif quand r>0) — les
    # deux conventions de signe sont opposées, d'où r ≈ −0,95. Le pipeline ne
    # lit que |d| : la comparaison correcte est sur les valeurs absolues.
    # Les valeurs signées restent dans le CSV per-flux ; le test porte sur |d|.
    rp, pp = stats.pearsonr(per_flux_df["r_pearson_ctrl_flux"].abs(),
                            per_flux_df["d_obs_mediane"].abs())
    tests["per_flux_abs_r_vs_abs_d_obs_mediane"] = {
        "pearson_r": float(rp), "p": float(pp), "n": int(len(per_flux_df))}
    rp2, pp2 = stats.pearsonr(per_flux_df["d_pred_bivarie"].abs(),
                              per_flux_df["d_obs_mediane"].abs())
    tests["per_flux_abs_d_pred_vs_abs_d_obs_mediane"] = {
        "pearson_r": float(rp2), "p": float(pp2), "n": int(len(per_flux_df)),
        "ecart_moyen_abs": float(np.mean(np.abs(per_flux_df["d_pred_bivarie"].abs()
                                                - per_flux_df["d_obs_mediane"].abs()))),
        "ecart_moyen_signe_abs": float(np.mean(per_flux_df["d_pred_bivarie"].abs()
                                               - per_flux_df["d_obs_mediane"].abs())),
    }
    # vérification de la convention de signe : d_obs signé vs −d_pred signé
    rp3, _ = stats.pearsonr(per_flux_df["d_obs_mediane"],
                            -per_flux_df["d_pred_bivarie"])
    tests["per_flux_signe_controle_d_obs_vs_moins_d_pred"] = {
        "pearson_r": float(rp3), "n": int(len(per_flux_df))}
    # (d4) perte doublon vs couplage
    rp, pp = stats.pearsonr(corr_df["C_couplage_pearson"], corr_df["perte_doublon"])
    tests["perte_doublon_vs_C"] = {"pearson_r": float(rp), "p": float(pp),
                                   "n": int(len(corr_df)),
                                   "perte_moyenne": float(corr_df["perte_doublon"].mean())}

    # --- DIAGNOSTIC POST-HOC (hors protocole gelé, hors verdict) ---
    # D_full dépasse maxsep de ~0,19 sur les réels : l'écart vient-il du
    # fenêtrage (fenêtres de 80 points qui se recouvrent : les deux groupes
    # partagent ~80 lignes autour du seuil, ce qui atténue |d|) ? Réplication
    # fenêtrée D_win : même algorithme que _scan_critical_threshold_fast
    # (w_size=80, plafonné à n//2 ; min_grp=2 ; candidats linspace(0,100,n_use),
    # n_use = milieu des bornes de loupe), sauf l'axe de progression, remplacé
    # par le percentile de rang du contrôle (l'axe MC du pipeline est monotone
    # en le rang du contrôle). Ne sert qu'à expliquer l'écart D_full−maxsep ;
    # le verdict H1 repose sur le test (c), pas sur ce diagnostic.
    def loupe_n_use(n_windows):
        hi = int(max(12, min(int(max(n_windows, 1)), 801)))
        lo = int(min(21, max(8, hi // 8)))
        if lo >= hi:
            lo = max(5, hi - 1)
        return int(round((lo + hi) / 2.0))

    def d_win(dfr, ctrl, ana):
        n = len(dfr)
        w_size = max(2, min(80, n // 2))
        n_windows = n - w_size + 1
        order_idx = np.argsort(dfr[ctrl].values.astype(float), kind="stable")
        srt = dfr.iloc[order_idx].reset_index(drop=True)
        progress = 100.0 * (np.arange(n) + 0.5) / n
        prog_cs = np.concatenate(([0.0], np.cumsum(progress)))
        win_prog = (prog_cs[w_size:] - prog_cs[:n_windows]) / w_size
        win_order = np.argsort(win_prog, kind="stable")
        win_prog_sorted = win_prog[win_order]
        n_use = loupe_n_use(n_windows)
        candidats = np.linspace(0, 100, n_use)
        best = -1.0
        for s in candidats:
            split = int(np.searchsorted(win_prog_sorted, s, side="left"))
            n_low, n_high = split, n_windows - split
            if n_low < 2 or n_high < 2:
                continue
            low_ids, high_ids = win_order[:split], win_order[split:]
            sep = []
            for j in ana:
                arr = srt[j].values.astype(float)
                g1 = np.concatenate([arr[i:i + w_size] for i in low_ids])
                g2 = np.concatenate([arr[i:i + w_size] for i in high_ids])
                d = cohen_d(g1, g2)
                if np.isfinite(d):
                    sep.append(abs(d))
            if sep:
                best = max(best, float(np.mean(sep)))
        return best, n_use

    dwin_rows = []
    for (fam, ctrl), r844 in sorted(d844.items()):
        base_file, _, dedup_pat, dedup_nul_pat = FAMILIES[fam]
        if (fam, ctrl) in DEDUP_841_SPECIAL:
            dedup_file, dedup_nul_file = DEDUP_841_SPECIAL[(fam, ctrl)]
        else:
            dedup_file = dedup_pat.format(ctrl)
            dedup_nul_file = dedup_nul_pat.format(ctrl)
        for tag, fname, maxsep_pipe in (("reel", dedup_file, r844.maxsep_R),
                                        ("nul", dedup_nul_file, r844.maxsep_N)):
            dfr = pd.read_csv(f"{OUT}/{fname}")
            ana = list(dfr.columns[1:])
            dw, n_use = d_win(dfr, ctrl, ana)
            dwin_rows.append({"famille": fam, "controle": ctrl, "type": tag,
                              "n": len(dfr), "n_use": n_use, "D_win": dw,
                              "maxsep_pipeline": float(maxsep_pipe),
                              "diff_Dwin_maxsep": dw - float(maxsep_pipe)})
    dwin_df = pd.DataFrame(dwin_rows)
    dwin_df.to_csv(f"{OUT}/immrot_848_dwin_diagnostic.csv", index=False)
    for tag in ["reel", "nul", "tous"]:
        sub = dwin_df if tag == "tous" else dwin_df[dwin_df["type"] == tag]
        rp, pp = stats.pearsonr(sub["D_win"], sub["maxsep_pipeline"])
        tests[f"DIAGNOSTIC_D_win_vs_maxsep_{tag}"] = {
            "pearson_r": float(rp), "p": float(pp), "n": int(len(sub)),
            "ecart_moyen_abs": float(np.mean(np.abs(sub["diff_Dwin_maxsep"]))),
            "ecart_moyen_signe": float(np.mean(sub["diff_Dwin_maxsep"])),
        }

    out_json = {
        "protocole": "PROTOCOL_immrot_domination.md",
        "protocole_sha256": sha(f"{OUT}/PROTOCOL_immrot_domination.md"),
        "sha_checks": checks,
        "familles": fam_summary,
        "tests": tests,
        "invariance_C_max_abs_diff": float(inv.max()),
    }
    with open(f"{OUT}/immrot_848_correlations.json", "w", encoding="utf-8") as f:
        json.dump(out_json, f, indent=2, ensure_ascii=False)
    print(json.dumps(tests, indent=2, ensure_ascii=False))
    print("Écrit : immrot_848_correlations.csv/.json, immrot_848_dfull.csv, "
          "immrot_848_per_flux_mediane.csv")

    # --- Porte G : jointure IMMROT <-> PARPROT (même patient par ligne ?) ---
    gate = {}
    tarball = f"{DATA}/tcga_paad_rsem.tar.gz"
    gate["tarball_md5"] = md5(tarball)
    gate["tarball_md5_attendu"] = "b09569ce3f4721f514bc137bd109ac0a"
    gate["tarball_md5_ok"] = gate["tarball_md5"] == gate["tarball_md5_attendu"]
    with tarfile.open(tarball, "r:gz") as tf:
        member = [m for m in tf.getmembers() if m.name.endswith(".data.txt")][0]
        f = tf.extractfile(member)
        df = pd.read_csv(f, sep="\t", index_col=0, low_memory=False)
    df.index = df.index.to_series().str.split("|").str[0]
    df = df[~df.index.duplicated(keep_first := "first")]
    cols = df.columns.to_series()
    tumor_cols = cols[cols.str[13:15] == "01"]
    gate["tumeurs_primaires_01"] = int(len(tumor_cols))
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    logmat = np.log2(mat + 1.0)
    imm_genes = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
                 "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
    parp_genes = ["PARP1", "PARP2", "BRCA1", "BRCA2", "ATM", "ATR", "CHEK1",
                  "CHEK2", "RAD51", "XRCC1", "POLQ", "FANCD2"]
    gate["nan_kras_plus_imm"] = int(logmat.loc[["KRAS"] + imm_genes].isna().sum().sum())
    gate["nan_kras_plus_parp"] = int(logmat.loc[["KRAS"] + parp_genes].isna().sum().sum())
    kras = logmat.loc["KRAS"].sort_values(ascending=True)
    order = list(kras.index)
    axis = pd.read_csv(f"{OUT}/immune_kras_order_tcga.csv")
    gate["axis_lignes"] = int(len(axis))
    gate["ordre_kras_recalcule_egal_axis"] = (order == list(axis["sample"]))
    gate["n_concordants"] = int(sum(1 for a, b in zip(order, list(axis["sample"])) if a == b))
    gate["kras_min_med_max"] = [round(float(kras.min()), 4),
                                round(float(kras.median()), 4),
                                round(float(kras.max()), 4)]
    gate["ouverte"] = bool(gate["tarball_md5_ok"]
                           and gate["tumeurs_primaires_01"] == 178
                           and gate["nan_kras_plus_imm"] == 0
                           and gate["nan_kras_plus_parp"] == 0
                           and gate["ordre_kras_recalcule_egal_axis"])
    with open(f"{OUT}/immrot_848_gate.json", "w", encoding="utf-8") as f:
        json.dump(gate, f, indent=2, ensure_ascii=False)
    print("PORTE G :", json.dumps(gate, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
