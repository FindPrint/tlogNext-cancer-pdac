#!/usr/bin/env python3
"""MRTX1133 (et contrôles) contre l'axe de dépendance KRAS — test par allèle.

But : les inhibiteurs directs de KRAS G12D (MRTX1133) et pan-RAS (RMC-6236)
sont absents de GDSC2 et, pour RMC-6236, absents de PRISM. MRTX1133 et SHP099
sont en revanche présents dans le criblage PRISM Repurposing Public 24Q2
(dose unique 2,5 µM, viabilité). Ce script teste si la sensibilité à MRTX1133
dépend de l'allèle KRAS (G12D vs autres) et si, chez les G12D, l'axe Chronos
KRAS du projet prédit la sensibilité.

Données (toutes déjà téléchargées et vérifiées, voir PROVENANCE_kras_g12d.md) :
- data/Repurposing_Public_24Q2_Extended_Primary_Data_Matrix.csv (PRISM, 72 456 953 o)
- data/Repurposing_Public_24Q2_Extended_Primary_Compound_List.csv
- data/CRISPRGeneEffect.csv (DepMap 24Q4, Chronos KRAS)
- data/Model.csv (DepMap 24Q4, lignées pancréas)
- data/OmicsSomaticMutationsMAFProfile.maf (DepMap 24Q4, 98 439 503 o, SHA 86b8530b...)
- data/OmicsProfiles.csv (mapping ProfileID PR-... -> ModelID ACH-...)
- data/OmicsSomaticMutationsMatrixHotspot.csv (4 210 723 o, SHA 6444ce81... ; codes 0/1/2 seulement, pas d'allèle)

Sorties :
- data/kras_alleles_pancreas.csv : allèle KRAS par lignée pancréas (54 lignées)
- data/mrtx1133_prism_kras_allele.csv : viabilité PRISM + Chronos + allèle (40 lignées)

Méthode :
- Allèle = Protein_Change du MAF, joint par ProfileID -> ModelID.
- Tertiles CORRECTS : "fort" = Chronos le plus négatif = le plus dépendant
  (le script PRISM du 15 nov. avait les étiquettes inversées ; ici c'est corrigé).
- Tests : Mann-Whitney G12D vs autres ; Spearman Chronos vs viabilité
  (toutes lignées, G12D seules, non-G12D) ; SHP099 en contrôle négatif.

Résultats attendus (vérifiés le 16 nov. 2026) :
- MRTX1133 : viabilité moyenne G12D -1,70 (n=17) vs autres -0,38 (n=23),
  Mann-Whitney p=0,0001. Par allèle : G12D -1,70 ; G12V -0,37 ; G12R -0,29.
- Spearman Chronos vs MRTX1133 : toutes rho +0,36 (p=0,031, n=36) ;
  G12D seules rho +0,47 (p=0,079, n=15) ; non-G12D rho +0,11 (p=0,65).
- SHP099 : G12D +0,36 vs autres +0,32 — rien (contrôle).
"""
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, mannwhitneyu

BASE = "/home/hatch/workspace/runs/pdac-v6"

# --- 1. Allèles KRAS par lignée (MAF -> ProfileID -> ModelID) ---
kras_rows = []
for chunk in pd.read_csv(
    f"{BASE}/data/OmicsSomaticMutationsMAFProfile.maf",
    sep="\t",
    chunksize=200000,
    usecols=["Hugo_Symbol", "Protein_Change", "Tumor_Sample_Barcode", "Variant_Classification"],
):
    k = chunk[chunk["Hugo_Symbol"] == "KRAS"]
    if len(k):
        kras_rows.append(k)
k = pd.concat(kras_rows)
prof = pd.read_csv(f"{BASE}/data/OmicsProfiles.csv")
m = k.merge(prof[["ProfileID", "ModelID"]], left_on="Tumor_Sample_Barcode",
            right_on="ProfileID", how="left")
m = m[m["Protein_Change"].notna()]
allele = (m.groupby("ModelID")["Protein_Change"]
           .apply(lambda s: ";".join(sorted(set(s)))).reset_index())

model = pd.read_csv(f"{BASE}/data/Model.csv", index_col=0)
panc = model[model["OncotreeLineage"] == "Pancreas"]
allele_p = allele.merge(panc[["CellLineName"]], left_on="ModelID",
                        right_index=True, how="inner")
allele_p.to_csv(f"{BASE}/data/kras_alleles_pancreas.csv", index=False)
print(f"lignées pancréas avec allèle KRAS : {len(allele_p)}")
print(allele_p["Protein_Change"].value_counts().to_string())

# --- 2. PRISM + Chronos + allèle ---
mat = pd.read_csv(f"{BASE}/data/Repurposing_Public_24Q2_Extended_Primary_Data_Matrix.csv",
                  index_col=0)
lst = pd.read_csv(f"{BASE}/data/Repurposing_Public_24Q2_Extended_Primary_Compound_List.csv")
ge = pd.read_csv(f"{BASE}/data/CRISPRGeneEffect.csv",
                 usecols=["Unnamed: 0", "KRAS (3845)"], index_col=0)
kras = ge["KRAS (3845)"].dropna()

d = pd.DataFrame({"allele": allele_p.set_index("ModelID")["Protein_Change"]})
d["kras_chronos"] = kras
for name in ["MRTX1133", "SHP099", "K-RAS(G12C)-INHIBITOR-6"]:
    brd = lst[lst["Drug.Name"] == name]["IDs"].iloc[0]
    d[name.lower().replace("-", "_").replace("(", "").replace(")", "") + "_viab"] = mat.loc[brd]
d = d.dropna(subset=["mrtx1133_viab"])
d["is_g12d"] = d["allele"].str.contains("G12D", na=False)
d.to_csv(f"{BASE}/data/mrtx1133_prism_kras_allele.csv")
print(f"\nlignées pancréas avec viabilité MRTX1133 : {len(d)}")

# --- 3. Tests ---
g12d = d[d["is_g12d"]]["mrtx1133_viab"]
other = d[~d["is_g12d"]]["mrtx1133_viab"]
u, p = mannwhitneyu(g12d, other, alternative="two-sided")
print(f"MRTX1133 viabilité moyenne G12D {g12d.mean():+.2f} (n={len(g12d)}) "
      f"vs autres {other.mean():+.2f} (n={len(other)}) ; Mann-Whitney p={p:.4f}")
print("par allèle :")
print(d.groupby("allele")["mrtx1133_viab"].agg(["count", "mean"]).round(2).to_string())

dd = d.dropna(subset=["kras_chronos"])
for label, sub in [("toutes", dd), ("G12D seules", dd[dd["is_g12d"]]),
                   ("non-G12D", dd[~dd["is_g12d"]])]:
    rho, p = spearmanr(sub["kras_chronos"], sub["mrtx1133_viab"])
    print(f"Spearman Chronos vs MRTX1133 ({label}, n={len(sub)}) : rho={rho:+.3f} p={p:.4f}")

print(f"SHP099 contrôle : G12D {d[d['is_g12d']]['shp099_viab'].mean():+.2f} "
      f"vs autres {d[~d['is_g12d']]['shp099_viab'].mean():+.2f}")
