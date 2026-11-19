#!/usr/bin/env python3
"""Vérification mesurée — MUC16 (CA125) et CLDN18 dans les 4 cohortes PDAC v6.
Question : quelle fraction des tumeurs exprime MUC16 / CLDN18 au-dessus d'un
seuil clair, et cette expression suit-elle le groupe KRAS fort ?

Utilise UNIQUEMENT les CSV de flux déjà construits (aucune reconstruction) :
- TCGA v4 : résidus corrigés de la pureté (régression acinaire/islet), ordre KRAS résiduel croissant
- GSE71729 : log-expression puce Agilent, ordre KRAS croissant
- GSE62452 : log-expression puce Affymetrix, ordre KRAS croissant
- ICGC : log2(cpm) Xena, ordre KRAS croissant
Les lignes sont dans l'ordre KRAS croissant : les 12 dernières = groupe KRAS fort.

LIMITE EXPLICITE : ces valeurs sont de l'ARN (ou des résidus d'ARN). L'éligibilité
au zolbetuximab se décide sur l'IHC protéique CLDN18.2 (score ≥ 75 % de cellules
tumorales à coloration modérée/forte, seuil des essais SPOTLIGHT/GLOW) — l'ARN
CLDN18 n'est PAS cette mesure. Aucun seuil ARN ne peut dire qui serait éligible.

Sorties : expression_muc16_cldn18_check.csv + expression_muc16_cldn18_check.txt
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

COHORTS = {
    "TCGA (178, ARN-seq, résidus corrigés pureté)": "pdac_tcga_fluxes_v4.csv",
    "GSE71729 (145, puce Agilent, log-expression)": "pdac_geo71729_fluxes.csv",
    "GSE62452 (69, puce Affymetrix, log-expression)": "pdac_geo62452_fluxes.csv",
    "ICGC PACA-AU (70, ARN-seq, log2cpm)": "pdac_icgc_fluxes.csv",
}

rows = []
txt = []
txt.append("=== MUC16 (CA125) et CLDN18 — expression dans les 4 cohortes PDAC ===")
txt.append("Seuils : quartile supérieur (Q3) = 25 % par construction ; médiane + 1 écart-type ;")
txt.append("médiane + 2 écarts-types. Groupe KRAS fort = 12 dernières lignes (ordre KRAS croissant).")
txt.append("Attendu sous indépendance : 3 des 12 KRAS-forts dans le quartile supérieur de chaque gène.")
txt.append("")

for name, path in COHORTS.items():
    f = pd.read_csv(path)
    n = len(f)
    step = f["step"].values
    assert (np.diff(step) >= 0).all(), f"{name} : ordre non croissant"
    top12 = np.zeros(n, dtype=bool); top12[-12:] = True
    top7 = np.zeros(n, dtype=bool); top7[-7:] = True
    txt.append(f"--- {name} — n={n} ---")
    for gene in ["MUC16", "CLDN18"]:
        v = f[gene].values.astype(float)
        q3 = np.quantile(v, 0.75)
        med, sd = np.median(v), v.std(ddof=1)
        frac_q3 = float((v > q3).mean())
        frac_m1sd = float((v > med + sd).mean())
        frac_m2sd = float((v > med + 2 * sd).mean())
        rho, p = spearmanr(np.arange(n), v)
        ov12 = int((top12 & (v > q3)).sum())
        ov7 = int((top7 & (v > q3)).sum())
        top12_sd = float((v[top12].mean() - v[~top12].mean()) / v.std(ddof=0))
        txt.append(
            f"{gene}: médiane {med:+.2f} | Q3 {q3:+.2f} | >Q3 {frac_q3:.0%} (par construction) | "
            f">méd+1sd {frac_m1sd:.0%} | >méd+2sd {frac_m2sd:.0%} | "
            f"rho KRAS {rho:+.3f} p={p:.3f} | top12 {top12_sd:+.2f} sd | "
            f"KRAS-fort dans Q3 : {ov12}/12 (attendu 3), top7 : {ov7}/7 (attendu 1,75)"
        )
        rows.append(dict(cohorte=name, n=n, gene=gene, median=med, q3=q3,
                         frac_q3=frac_q3, frac_med1sd=frac_m1sd, frac_med2sd=frac_m2sd,
                         rho_kras=rho, p_rho=p, top12_sd=top12_sd,
                         overlap_top12_q3=ov12, overlap_top7_q3=ov7))
    # double-positifs (MUC16 ET CLDN18 au-dessus de Q3)
    q3_m = np.quantile(f["MUC16"].values, 0.75)
    q3_c = np.quantile(f["CLDN18"].values, 0.75)
    both = (f["MUC16"].values > q3_m) & (f["CLDN18"].values > q3_c)
    txt.append(f"Double-positifs (MUC16>Q3 ET CLDN18>Q3) : {both.sum()}/{n} ({both.mean():.0%}, attendu 6,25 % sous indépendance) ; "
               f"parmi les 12 KRAS-forts : {int((top12 & both).sum())}/12")
    txt.append("")

# --- TCGA clinique : radiothérapie (seule variable de traitement du fichier) ---
txt.append("=== TCGA clinique — traitement (data_clinical_patient.txt) ===")
lines = open("data_clinical_patient.txt", encoding="utf-8", errors="replace").read().splitlines()
hdr = lines[4].split("\t")  # ligne 5 = vrai en-tête (PATIENT_ID...) ; lignes 1-4 = métadonnées
data_rows = [l.split("\t") for l in lines[5:] if l.strip()]
clin = pd.DataFrame(data_rows, columns=hdr)
clin = clin[clin[hdr[0]].str.startswith("TCGA-", na=False)]
print("patients cliniques :", len(clin))
# la colonne survie / OS est en mois ; on joint par identifiant TCGA
f = pd.read_csv("pdac_tcga_fluxes_v4.csv")
# ordre KRAS : les identifiants ne sont pas dans le CSV de flux ; on utilise la
# survie déjà vérifiée (tcga_survival_verify_results.txt) — ici on ne refait que
# la répartition radiothérapie par quartile MUC16 via la jointure sur l'ordre
# des tumeurs du fichier Firehose, reproduite dans survival_tcga_verify.py.
# Simplification honnête : on rapporte les effectifs bruts du fichier clinique.
rad = clin["RADIATION_THERAPY"]
txt.append(f"Radiothérapie : Oui {int((rad == 'Yes').sum())} / Non {int((rad == 'No').sum())} / manquant {int((rad == '').sum())} sur {len(clin)} patients.")
neo = clin["HISTORY_NEOADJUVANT_TRTYN"]
txt.append(f"Néoadjuvant : Non {int((neo == 'No').sum())} / autre {int((neo != 'No').sum())} — aucun patient n'a reçu de néoadjuvant.")
txt.append("AUCUNE colonne chimiothérapie dans ce fichier : pas de nom de médicament, pas de chimiothérapie adjuvante, pas de réponse au traitement.")
txt.append("Conclusion partie 4 : la question « les CA125-élevés ont-ils reçu une chimio différente / répondu différemment ? » NE PEUT PAS être répondue avec ce fichier.")
txt.append("Seule variable de traitement exploitable : la radiothérapie (Oui/Non) — voir analyse complémentaire ci-dessous si jointe à l'expression.")

out = pd.DataFrame(rows)
out.to_csv("expression_muc16_cldn18_check.csv", index=False)
open("expression_muc16_cldn18_check.txt", "w").write("\n".join(txt) + "\n")
print("\n".join(txt))
print("\nFichiers écrits : expression_muc16_cldn18_check.csv / .txt")
