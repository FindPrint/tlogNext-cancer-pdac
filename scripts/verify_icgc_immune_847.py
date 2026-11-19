#!/usr/bin/env python3
"""§8.47 (a) — Vérification des entrées immunitaires.
Aucun run pipeline. Lecture seule des CSV déjà sur le disque + NMF ICGC.
Sorties : icgc_immune_inversion_verify.json / .csv ; log stdout.
Protocole gelé : PROTOCOL_icgc_immune_inversion.md
  SHA b55283eeb7a24e30b52ee6a8f24de8a77b3c7b53072d8b837fab9eb08a61eb34
"""
import gzip  # noqa: F401  (gardé : lecture du .gz via pandas)
import hashlib

import json


import numpy as np
import pandas as pd
from scipy import stats

PDAC = "/home/hatch/workspace/runs/pdac-v6"
COHORTES = ["tcga", "geo71729", "geo62452", "icgc"]
GENES12 = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163",
           "CD274", "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
SUBST = {"icgc": {"IFNG": "PRF1", "CD19": "MS4A1"}}

EXP_SHA = {
    "pdac_immune_tcga_fluxes.csv": "66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e",
    "pdac_immune_tcga_fluxes_nul.csv": "9100d181e3391d558eec6bc97e82f93b16c118b807b4a5f0c0992f4bda51a405",
    "pdac_immune_geo71729_fluxes.csv": "8987ffcaeb9cac848bd220c2a1816f63ecbcd63e5cd68c4f698e7c3234952219",
    "pdac_immune_geo71729_fluxes_nul.csv": "b96b1f744db30193098e588326db33c3bca448bb87615fd011d9302e7c605fc7",
    "pdac_immune_geo62452_fluxes.csv": "97c4689a6ecacd0a73a77804200a72a90994d60bea7e6b2c079195acbffd79a3",
    "pdac_immune_geo62452_fluxes_nul.csv": "b0496cb923d49ef4913f90b895d856e3c02a1b1b4d78a2cc11a9f198c367d3a9",
    "pdac_immune_icgc_fluxes.csv": "10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc",
    "pdac_immune_icgc_fluxes_nul.csv": "3393ecd662e6decfa41416b535e509089cb43bd63345097fe3f25ad9b7860955",
    "immune_kras_order_tcga.csv": "31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d",
    "immune_kras_order_geo71729.csv": "2113e24c5b82303f4f808fc99a418ead53436ecbc530af0da02a623cffa76515",
    "immune_kras_order_geo62452.csv": "4a8549998b38021559724a08dcd5a882d170256f98d487cc45eeff3bd303c095",
    "immune_kras_order_icgc.csv": "67d41da9c93538e8670026bdfef0b3bddbc49df39bca3dc4d67af3101a720860",
}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def genes(cohorte):
    """Noms de colonnes réels du CSV (avec substitutions ICGC)."""
    return [SUBST.get(cohorte, {}).get(g, g) for g in GENES12]


def main():
    out = {"sha_verifies": {}, "cohortes": {}, "h4_sous_type": {}}

    # --- 1. SHA + nul = permutation par ligne ---
    for cohorte in COHORTES:
        for suffix in ("fluxes.csv", "fluxes_nul.csv"):
            f = f"pdac_immune_{cohorte}_{suffix}"
            out["sha_verifies"][f] = (sha(f"{PDAC}/{f}") == EXP_SHA[f])
        real = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv")
        nul = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes_nul.csv")
        cols = genes(cohorte)
        assert list(real.columns) == ["step"] + cols, (cohorte, list(real.columns))
        assert list(nul.columns) == ["step"] + cols
        assert (real["step"].values == np.arange(len(real))).all()
        assert (nul["step"].values == np.arange(len(nul))).all()
        # même multi-ensemble de lignes (tri lexicographique des lignes)
        r_sorted = real[cols].round(12).sort_values(cols).reset_index(drop=True)
        n_sorted = nul[cols].round(12).sort_values(cols).reset_index(drop=True)
        perm_ok = bool(np.allclose(r_sorted.values, n_sorted.values, rtol=0, atol=0))
        # le nul n'est pas identique au réel (ordre vraiment changé)
        order_changed = not bool(np.allclose(real[cols].values, nul[cols].values))
        # reconstruction graine 42 : même méthode que build_fluxes_immune.py
        rng = np.random.default_rng(42)
        perm = rng.permutation(len(real))
        seed42_ok = bool(np.allclose(
            nul[cols].values, real[cols].values[perm]))
        rec = {"n": int(len(real)), "nul_permutation_lignes": perm_ok,
               "ordre_change": order_changed, "nul_reconstruit_graine42": seed42_ok,
               "colonnes": cols}
        out["cohortes"][cohorte] = rec
        print(f"[{cohorte}] n={len(real)} perm_lignes={perm_ok} "
              f"ordre_change={order_changed} graine42={seed42_ok}")

        # --- 2. Statistiques par gène (réel) ---
        stats_genes = []
        for g in cols:
            v = real[g].values.astype(float)
            stats_genes.append({"gene": g, "moyenne": round(float(np.mean(v)), 4),
                                "ecart_type": round(float(np.std(v, ddof=1)), 4),
                                "min": round(float(np.min(v)), 4),
                                "max": round(float(np.max(v)), 4),
                                "nan": int(np.isnan(v).sum())})
        rec["genes_stats"] = stats_genes

        # --- 3. Axe KRAS ---
        axis = pd.read_csv(f"{PDAC}/immune_kras_order_{cohorte}.csv")
        k = axis["kras_raw"].values.astype(float)
        assert (axis["step"].values == np.arange(len(axis))).all()
        top12 = k[-12:]
        rec["kras"] = {"min": round(float(k.min()), 4),
                       "mediane": round(float(np.median(k)), 4),
                       "max": round(float(k.max()), 4),
                       "moy_top12": round(float(top12.mean()), 4),
                       "moy_reste": round(float(k[:-12].mean()), 4),
                       "ecart_top12_reste": round(float(top12.mean() - k[:-12].mean()), 4),
                       "sd": round(float(np.std(k, ddof=1)), 4),
                       "monotone_croissant": bool(np.all(np.diff(k) > 0))}
        print(f"[{cohorte}] KRAS min={k.min():.3f} med={np.median(k):.3f} "
              f"max={k.max():.3f} top12-reste={top12.mean()-k[:-12].mean():.3f}")

        # --- 4. Fardeau immunitaire par ligne + corrélation inter-flux ---
        z = (real[cols] - real[cols].mean()) / real[cols].std(ddof=1)
        burden = z.mean(axis=1).values
        rec["fardeau"] = {
            "moyenne_abs_z": round(float(np.mean(np.abs(burden))), 4),
            "max_abs_z": round(float(np.max(np.abs(burden))), 4),
            "lignes_abs_z_sup_2.5": int((np.abs(burden) > 2.5).sum()),
            "lignes_abs_z_sup_2.0": int((np.abs(burden) > 2.0).sum()),
            "rho_burden_vs_step": round(float(stats.spearmanr(burden, real["step"])[0]), 4),
            "p_burden_vs_step": float(stats.spearmanr(burden, real["step"])[1]),
            "lignes_extremes": [
                {"step": int(i), "fardeau_z": round(float(burden[i]), 3)}
                for i in np.where(np.abs(burden) > 2.0)[0]]}
        # corrélation de Spearman moyenne entre les 12 flux
        rho_mat = real[cols].corr(method="spearman").values
        iu = np.triu_indices(12, 1)
        rec["correlation_inter_flux"] = {
            "rho_spearman_moyen": round(float(rho_mat[iu].mean()), 4),
            "rho_spearman_mediane": round(float(np.median(rho_mat[iu])), 4),
            "rho_min": round(float(rho_mat[iu].min()), 4),
            "rho_max": round(float(rho_mat[iu].max()), 4)}
        print(f"[{cohorte}] rho_interflux_moyen={rho_mat[iu].mean():.3f} "
              f"fardeau_max|z|={np.max(np.abs(burden)):.2f} "
              f"lignes_|z|>2.5={(np.abs(burden) > 2.5).sum()} "
              f"rho_burden_step={stats.spearmanr(burden, real['step'])[0]:.3f}")

    # --- 5. H4 : sous-types Bailey le long de l'axe KRAS (ICGC) ---
    # Fichier NMF : TSV simple, en-tête « icgc_id \t expression subtype ».
    try:
        nmf = pd.read_csv(f"{PDAC}/data/icgc_pacaau_nmf.txt.gz", sep="\t")
        print("NMF colonnes:", list(nmf.columns), "lignes:", len(nmf))
        sample_col, class_col = nmf.columns[0], nmf.columns[1]
        axis = pd.read_csv(f"{PDAC}/immune_kras_order_icgc.csv")
        m = axis.merge(nmf, left_on="sample", right_on=sample_col, how="left")
        cls = class_col
        sub = m[cls].value_counts(dropna=False).to_dict()
        joint_ok = int(m[cls].notna().sum())
        out["h4_sous_type"] = {
            "fichier_nmf_lignes": int(len(nmf)),
            "jointure_70": joint_ok,
            "repartition_70": {str(k): int(v) for k, v in sub.items()},
            "classes": sorted(m[cls].dropna().unique().tolist())}
        # Mann-Whitney : rang KRAS (step) Immunogenic vs autres
        for target in ("Immunogenic",):
            a = m.loc[m[cls] == target, "step"].values
            b = m.loc[(m[cls] != target) & m[cls].notna(), "step"].values
            if len(a) >= 3 and len(b) >= 3:
                u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
                out["h4_sous_type"]["mannwhitney_immunogenic_vs_autres"] = {
                    "n_immunogenic": int(len(a)), "n_autres": int(len(b)),
                    "mediane_step_immunogenic": float(np.median(a)),
                    "mediane_step_autres": float(np.median(b)),
                    "U": float(u), "p": float(p)}
                print(f"[H4] Immunogenic n={len(a)} med_step={np.median(a):.0f} "
                      f"vs autres n={len(b)} med_step={np.median(b):.0f} p={p:.4f}")
        # tertiles de l'axe KRAS x sous-type
        m["tertile"] = pd.qcut(m["step"], 3, labels=["T1_bas", "T2", "T3_haut"])
        ct = pd.crosstab(m["tertile"], m[cls]).to_dict()
        out["h4_sous_type"]["tertiaire_x_sous_type"] = {
            str(k): {str(k2): int(v2) for k2, v2 in v.items()}
            for k, v in ct.items()}
        # médiane du step par sous-type (4 classes)
        med = m.groupby(cls)["step"].median().round(1).to_dict()
        out["h4_sous_type"]["mediane_step_par_sous_type"] = {
            str(k): float(v) for k, v in med.items()}
        print("[H4] répartition 70:", sub)
        print("[H4] médiane step par sous-type:", med)
        print("[H4] tertiles x sous-type:", out["h4_sous_type"]["tertiaire_x_sous_type"])
    except Exception as e:  # noqa: BLE001 — H4 non testable, pas un échec du chantier
        out["h4_sous_type"] = {"erreur": f"{type(e).__name__}: {e}",
                               "statut": "non testable"}
        print("[H4] NON TESTABLE:", e)

    with open(f"{PDAC}/icgc_immune_inversion_verify.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    # CSV plat : stats par gène et par cohorte
    rows = []
    for cohorte in COHORTES:
        for g in out["cohortes"][cohorte]["genes_stats"]:
            rows.append({"cohorte": cohorte, **g})
    pd.DataFrame(rows).to_csv(f"{PDAC}/icgc_immune_inversion_verify.csv", index=False)
    print("écrit: icgc_immune_inversion_verify.json / .csv")


if __name__ == "__main__":
    main()
