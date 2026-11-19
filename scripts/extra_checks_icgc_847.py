#!/usr/bin/env python3
"""§8.47 — Vérifications complémentaires (aucun run pipeline neuf).
(1) Courbe de scan réelle ICGC sur la grille config nulle (22 candidats)
    comparée à la bande nulle répliquée (médiane, p25, p75) : combien de
    candidats dans l'IQR nul.
(2) Dilution du signal tardif : moyenne des |d de Cohen| top-K vs reste
    pour K = 12 (test direct §8.23) et K élargi (≈ groupe « haut » du scan
    à un seuil tardif : 26 lignes à n=70, 60 à n=178, 40 à n=145).
    K élargi = 26/60/40 : taille du groupe haut à un seuil ~80 % avec les
    w_size des configs (fenêtres couvrant les dernières lignes).
(3) d_ssep avec un nul MÉDIAN (au lieu du nul graine 42) par cohorte :
    maxsep réel − médiane des maxsep nuls répliqués (config nulle).
Sortie : icgc_immune_inversion_extra.json.
Protocole gelé : PROTOCOL_icgc_immune_inversion.md
  SHA b55283eeb7a24e30b52ee6a8f24de8a77b3c7b53072d8b837fab9eb08a61eb34
  (+ addendum §9, SHA f1a5a37c0b8ce452b4d00a9d2a649ac41384e076dcb80839389eac728988379c)
"""
import importlib.util
import json

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
GENES12 = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163",
           "CD274", "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]
SUBST = {"icgc": {"IFNG": "PRF1", "CD19": "MS4A1"}}
COHORTES = ["tcga", "geo71729", "geo62452", "icgc"]
# groupe « haut » du scan à un seuil tardif (~80 %) : dernières lignes
# couvertes par les fenêtres hautes (w_size de la config nulle).
TOP_ELARGI = {"tcga": 60, "geo71729": 40, "geo62452": 26, "icgc": 26}

_spec = importlib.util.spec_from_file_location(
    "v62", "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py")
V62 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V62)
MODE_CFG = V62.PARAMETERS["modes"]["fast"].copy()
MODE_CFG.setdefault("random_seed", V62.RANDOM_SEED)


def cohen_d(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    n1, n2 = len(a), len(b)
    s = np.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1)) / (n1 + n2 - 2))
    return float((a.mean() - b.mean()) / s) if s > 0 else 0.0


def main():
    out = {"courbe_reelle_vs_bande_nulle_icgc": {}, "dilution_topk": {},
           "d_ssep_nul_median": {}}
    replica = json.load(open(f"{PDAC}/icgc_immune_inversion_replica.json"))

    # (1) courbe réelle ICGC, grille config nulle
    df = pd.read_csv(f"{PDAC}/pdac_immune_icgc_fluxes.csv")
    cols = [SUBST["icgc"].get(g, g) for g in GENES12]
    mat = df[cols].values.astype(float)
    prog = np.asarray(V62._build_mc_progress_axis(
        np.arange(70, dtype=float), {}, MODE_CFG)["progress_pct"], dtype=float)
    fluxes = {k: mat[:, j] for j, k in enumerate(cols)}
    _, curve = V62.scan_critical_threshold(fluxes, prog, MODE_CFG, 22, None, 16, 7)
    band = replica["bande_nulle_icgc"]["config_nulle"]
    lignes, inside, tot = [], 0, 0
    for c, med, p25, p75 in zip(curve, band["mediane"], band["p25"], band["p75"]):
        if c["score"] is None:
            continue
        tot += 1
        ok = bool(p25 <= c["score"] <= p75)
        inside += ok
        lignes.append({"candidat": round(c["candidate"], 2),
                       "score_reel": round(c["score"], 4),
                       "mediane_nulle": med, "p25_nulle": p25, "p75_nulle": p75,
                       "dans_iqr": ok})
    out["courbe_reelle_vs_bande_nulle_icgc"] = {
        "grille": "config nulle (w=16, min_grp=7, 22 candidats)",
        "dans_iqr": f"{inside}/{tot}", "lignes": lignes}
    print(f"(1) courbe réelle ICGC dans IQR nulle : {inside}/{tot} candidats")

    # (2) dilution top-K
    for cohorte in COHORTES:
        d = pd.read_csv(f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv")
        cc = [SUBST.get(cohorte, {}).get(g, g) for g in GENES12]
        m = d[cc].values.astype(float)
        rec = {}
        for label, k in (("top12", 12), ("top_elargi", TOP_ELARGI[cohorte])):
            ds = [abs(cohen_d(m[-k:, j], m[:-k, j])) for j in range(12)]
            rec[label] = {"k": k, "moy_abs_d": round(float(np.mean(ds)), 4),
                          "max_abs_d": round(float(np.max(ds)), 4),
                          "d_pdcd1": round(float(cohen_d(m[-k:, 7], m[:-k, 7])), 4),
                          "d_cd8a": round(float(cohen_d(m[-k:, 0], m[:-k, 0])), 4),
                          "d_gzmb": round(float(cohen_d(m[-k:, 9], m[:-k, 9])), 4)}
        rec["facteur_dilution_moy_abs_d"] = round(
            rec["top12"]["moy_abs_d"] / rec["top_elargi"]["moy_abs_d"], 3)
        out["dilution_topk"][cohorte] = rec
        print(f"(2) [{cohorte}] top12 moy|d|={rec['top12']['moy_abs_d']} -> "
              f"top{rec['top_elargi']['k']} moy|d|={rec['top_elargi']['moy_abs_d']} "
              f"(facteur {rec['facteur_dilution_moy_abs_d']})")

    # (3) d_ssep avec nul médian
    for cohorte in COHORTES:
        r = replica["distributions_nulles"][cohorte]
        med_nulle = r["config_nulle"]["mediane"]
        p975_nulle = r["config_nulle"]["p97.5"]
        reel = r["maxsep_reel_config_reelle"]
        out["d_ssep_nul_median"][cohorte] = {
            "maxsep_reel": reel, "mediane_nulle": med_nulle,
            "p97.5_nulle": p975_nulle,
            "d_ssep_nul_median": round(reel - med_nulle, 4),
            "d_ssep_nul_p97.5": round(reel - p975_nulle, 4),
            "P_nul_sup_reel": r["config_nulle"]["P_sup_reel"]}
        print(f"(3) [{cohorte}] d_ssep nul médian = {reel} - {med_nulle} = "
              f"{reel - med_nulle:.4f} ; nul p97.5 : {reel - p975_nulle:.4f} ; "
              f"P(nul>=réel)={r['config_nulle']['P_sup_reel']}")

    with open(f"{PDAC}/icgc_immune_inversion_extra.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("écrit: icgc_immune_inversion_extra.json")


if __name__ == "__main__":
    main()
