#!/usr/bin/env python3
"""§8.47 (b) — Tests directs par cohorte, réel vs nul graine 42.
Mêmes définitions que direct_tests_immune.py : Spearman contre KRAS brut,
top-12 KRAS-fort contre reste (d de Cohen, Welch). Gènes focaux : GZMB,
CD8A, IFNG (PRF1 en ICGC), PDCD1 + tableau complet des 12.
Ajout : distribution de permutation (200 tirages, graines 1000-1199) du
rho et du d top-12 pour les 4 gènes focaux, par cohorte (nul direct).
Sorties : icgc_immune_inversion_direct.csv / .json.
Protocole gelé : PROTOCOL_icgc_immune_inversion.md
  SHA b55283eeb7a24e30b52ee6a8f24de8a77b3c7b53072d8b837fab9eb08a61eb34
"""
import json

import numpy as np
import pandas as pd
from scipy import stats

PDAC = "/home/hatch/workspace/runs/pdac-v6"
COHORTES = ["tcga", "geo71729", "geo62452", "icgc"]
GENES12 = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163",
           "CD274", "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
SUBST = {"icgc": {"IFNG": "PRF1", "CD19": "MS4A1"}}
FOCAUX = ["GZMB", "CD8A", "IFNG", "PDCD1"]


def genes(cohorte):
    return [SUBST.get(cohorte, {}).get(g, g) for g in GENES12]


def cohen_d(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    n1, n2 = len(a), len(b)
    s = np.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1)) / (n1 + n2 - 2))
    return float((a.mean() - b.mean()) / s) if s > 0 else 0.0


def stats_gene(values, kras):
    """Spearman vs KRAS + top-12 vs reste (d de Cohen, Welch)."""
    rho, p_rho = stats.spearmanr(values, kras)
    top, reste = values[-12:], values[:-12]
    d = cohen_d(top, reste)
    _, p_w = stats.ttest_ind(top, reste, equal_var=False)
    return {"rho": round(float(rho), 4), "p_rho": float(p_rho),
            "d_top12": round(float(d), 4), "p_welch": float(p_w),
            "moy_top12": round(float(np.mean(top)), 4),
            "moy_reste": round(float(np.mean(reste)), 4)}


def main():
    rows = []
    perm_out = {}
    for cohorte in COHORTES:
        cols = genes(cohorte)
        real = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv")
        nul = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes_nul.csv")
        axis = pd.read_csv(f"{PDAC}/immune_kras_order_{cohorte}.csv")
        kras = axis["kras_raw"].values.astype(float)
        assert (axis["step"].values == np.arange(len(axis))).all()
        for g_nom, g_col in zip(GENES12, cols):
            s_r = stats_gene(real[g_col].values.astype(float), kras)
            s_n = stats_gene(nul[g_col].values.astype(float), kras)
            rows.append({"cohorte": cohorte, "gene_demande": g_nom,
                         "gene_colonne": g_col, "n": int(len(real)),
                         "rho_reel": s_r["rho"], "p_rho_reel": s_r["p_rho"],
                         "d_top12_reel": s_r["d_top12"],
                         "p_welch_reel": s_r["p_welch"],
                         "rho_nul42": s_n["rho"], "p_rho_nul42": s_n["p_rho"],
                         "d_top12_nul42": s_n["d_top12"],
                         "p_welch_nul42": s_n["p_welch"]})
        # distributions de permutation pour les gènes focaux (nul direct)
        perm_out[cohorte] = {}
        rng_master = np.random.default_rng(7)
        for g_nom in FOCAUX:
            g_col = SUBST.get(cohorte, {}).get(g_nom, g_nom)
            v = real[g_col].values.astype(float)
            rhos, ds = [], []
            for _ in range(200):
                seed = int(rng_master.integers(1000, 10_000_000))
                rng = np.random.default_rng(seed)
                vp = rng.permutation(v)
                rho, _ = stats.spearmanr(vp, kras)
                rhos.append(rho)
                ds.append(cohen_d(vp[-12:], vp[:-12]))
            rhos, ds = np.array(rhos), np.array(ds)
            obs = stats_gene(v, kras)
            perm_out[cohorte][g_nom] = {
                "gene_colonne": g_col,
                "rho_obs": obs["rho"], "p_rho_obs": obs["p_rho"],
                "rho_perm_mediane": round(float(np.median(rhos)), 4),
                "rho_perm_p2.5": round(float(np.quantile(rhos, 0.025)), 4),
                "rho_perm_p97.5": round(float(np.quantile(rhos, 0.975)), 4),
                "p_perm_rho_abs_sup_obs": round(float(np.mean(np.abs(rhos) >= abs(obs["rho"]))), 4),
                "d_obs": obs["d_top12"],
                "d_perm_mediane": round(float(np.median(ds)), 4),
                "d_perm_p2.5": round(float(np.quantile(ds, 0.025)), 4),
                "d_perm_p97.5": round(float(np.quantile(ds, 0.975)), 4),
                "p_perm_d_abs_sup_obs": round(float(np.mean(np.abs(ds) >= abs(obs["d_top12"]))), 4)}
        print(f"[{cohorte}] direct OK ; "
              f"PDCD1 rho={perm_out[cohorte]['PDCD1']['rho_obs']} "
              f"p_perm={perm_out[cohorte]['PDCD1']['p_perm_rho_abs_sup_obs']} ; "
              f"CD8A rho={perm_out[cohorte]['CD8A']['rho_obs']} "
              f"p_perm={perm_out[cohorte]['CD8A']['p_perm_rho_abs_sup_obs']}")

    df = pd.DataFrame(rows)
    df.to_csv(f"{PDAC}/icgc_immune_inversion_direct.csv", index=False)
    with open(f"{PDAC}/icgc_immune_inversion_direct.json", "w") as f:
        json.dump({"tests_directs": rows, "permutations_200": perm_out},
                  f, indent=2, ensure_ascii=False)
    # résumé : moyenne des |d| top-12 et des |rho| par cohorte (réel vs nul42)
    for cohorte in COHORTES:
        sub = df[df["cohorte"] == cohorte]
        print(f"[{cohorte}] moy|d_top12| réel={np.mean(np.abs(sub['d_top12_reel'])):.3f} "
              f"nul42={np.mean(np.abs(sub['d_top12_nul42'])):.3f} | "
              f"moy|rho| réel={np.mean(np.abs(sub['rho_reel'])):.3f} "
              f"nul42={np.mean(np.abs(sub['rho_nul42'])):.3f} | "
              f"signes rho négatifs réel={(sub['rho_reel'] < 0).sum()}/12")
    print("écrit: icgc_immune_inversion_direct.csv / .json")


if __name__ == "__main__":
    main()
