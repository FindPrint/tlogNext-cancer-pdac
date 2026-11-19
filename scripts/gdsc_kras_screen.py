"""GDSC2 dose-réponse — test médicamenteux ciblé KRAS du sous-groupe v4.
Question : parmi les lignées pancréatiques, les lignées les plus dépendantes
de KRAS (axe du sous-groupe v4 TCGA) répondent-elles mieux aux inhibiteurs
de la voie KRAS en dose-réponse ?
Test par composé : corrélation de Spearman entre LN_IC50 (et AUC) GDSC2
et l'effet Chronos KRAS (DepMap 24Q4), + moyennes par tertile KRAS.
Sens attendu : rho > 0 = les lignées KRAS-dépendantes (Chronos négatif)
sont plus sensibles (IC50 / AUC plus bas).
Provenance : GDSC2 fitted dose-response 27Oct23 (Wellcome Sanger Institute),
via l'API Cell Model Passports ; DepMap Public 24Q4 (figshare 27993248).
Règles : jamais d'imputation ; FDR Benjamini-Hochberg sur l'ensemble testé ;
un hit isolé sans effet de classe = curiosité, pas un candidat.
"""
import csv, hashlib, os, sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
LOG = open(os.path.join(BASE, "gdsc_kras_screen.log"), "w")

def say(*a):
    print(*a, flush=True)
    print(*a, file=LOG, flush=True)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

GDSC = os.path.join(DATA, "GDSC2_fitted_dose_response_27Oct23.xlsx")
say("GDSC2 :", os.path.getsize(GDSC), "octets ; SHA-256", sha256(GDSC))

# 1. Lecture GDSC2
g = pd.read_excel(GDSC, engine="openpyxl")
say("GDSC2 lignes :", len(g), "| colonnes :", list(g.columns))
say("datasets :", g["DATASET"].unique() if "DATASET" in g.columns else "?")
say("composés uniques (DRUG_NAME) :", g["DRUG_NAME"].nunique(),
    "| DRUG_ID uniques :", g["DRUG_ID"].nunique())
say("lignées uniques :", g["CELL_LINE_NAME"].nunique(),
    "| SANGER_MODEL_ID uniques :", g["SANGER_MODEL_ID"].nunique())

# 2. Jointure lignées pancréas via Model.csv (SangerModelID -> ModelID)
mod = pd.read_csv(os.path.join(DATA, "Model.csv"))
say("Model.csv :", len(mod), "lignées ; SangerModelID non vides :",
    mod["SangerModelID"].notna().sum())
# Un seul SangerModelID dupliqué (SIDM00117 -> 2 lignées poumon, hors pancréas) :
# on garde la première occurrence pour rendre la jointure unique.
mod_u = mod.dropna(subset=["SangerModelID"]).drop_duplicates(
    subset=["SangerModelID"], keep="first")
say("SangerModelID dupliqués écartés :",
    int(mod["SangerModelID"].notna().sum() - len(mod_u)))
s2m = mod_u.set_index("SangerModelID")["ModelID"]
panc_mod = set(mod.loc[mod["OncotreeLineage"] == "Pancreas", "ModelID"])
say("lignées pancréas DepMap (OncotreeLineage == Pancreas) :", len(panc_mod))
g["ModelID"] = g["SANGER_MODEL_ID"].map(s2m)
say("lignées GDSC2 jointes à DepMap :", g["ModelID"].notna().sum(), "/", len(g))
gp = g[g["ModelID"].isin(panc_mod)].copy()
say("lignes GDSC2 pancréas :", len(gp), "| lignées pancréas distinctes :",
    gp["ModelID"].nunique())

# 3. Axe KRAS (Chronos DepMap 24Q4, convention prism_screen.py)
with open(os.path.join(DATA, "CRISPRGeneEffect.csv")) as f:
    header = next(csv.reader(f))
kpos = [i for i, c in enumerate(header) if c.startswith("KRAS (")][0]
ge = pd.read_csv(os.path.join(DATA, "CRISPRGeneEffect.csv"),
                 usecols=[0, kpos], index_col=0)
ge.columns = ["KRAS"]
kras = ge["KRAS"].dropna()
common = sorted(set(gp["ModelID"]) & set(kras.index))
say("lignées pancréas communes GDSC2 x DepMap KRAS :", len(common))
say("KRAS Chronos : min %.2f médiane %.2f max %.2f"
    % (kras.loc[common].min(), kras.loc[common].median(), kras.loc[common].max()))
gp = gp[gp["ModelID"].isin(common)]
k = kras.loc[common]

# 4. Agrégation par composé (DRUG_NAME ; moyenne sur DRUG_ID dupliqués)
#    une ligne par (lignée, composé) pour LN_IC50 et AUC.
agg = (gp.groupby(["ModelID", "DRUG_NAME"])
         .agg(ln_ic50=("LN_IC50", "mean"),
              auc=("AUC", "mean"),
              target=("PUTATIVE_TARGET", "first"),
              pathway=("PATHWAY_NAME", "first"),
              n_ids=("DRUG_ID", "nunique"))
         .reset_index())
dup = agg.groupby("DRUG_NAME")["n_ids"].max()
say("composés avec DRUG_ID dupliqués :", int((dup > 1).sum()),
    "sur", len(dup))
say("composés testables (au moins une lignée pancréas) :", agg["DRUG_NAME"].nunique())

# 5. Test par composé
def bh(pvals):
    p = np.asarray(pvals, dtype=float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * n / (np.arange(n) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.minimum(q, 1.0)
    return out

rows = []
for name, sub in agg.groupby("DRUG_NAME"):
    sub = sub.set_index("ModelID")
    for metric, col in (("ln_ic50", "ln_ic50"), ("auc", "auc")):
        pass
    v1 = sub["ln_ic50"].dropna()
    v2 = sub["auc"].dropna()
    if len(v1) < 15:
        continue
    kk1 = k.loc[v1.index]
    rho1, p1 = spearmanr(v1, kk1)
    rho2, p2 = spearmanr(v2.loc[v1.index], kk1) if len(v2) >= 15 else (np.nan, np.nan)
    # Tertiles de DÉPENDANCE KRAS : Chronos le plus négatif = le plus dépendant.
    # qcut étiquette par ordre croissant des valeurs : le 1er tiers (Chronos bas)
    # est donc le plus dépendant -> étiquette "fort". (Ne pas inverser : dans
    # prism_screen.py les étiquettes étaient dans l'autre sens, "fort" = Chronos
    # élevé = le MOINS dépendant. Ici "fort" = le plus dépendant, vérifié.)
    tert = pd.qcut(kk1, 3, labels=["fort", "moyen", "faible"])
    hi1 = v1[tert == "fort"].mean(); lo1 = v1[tert == "faible"].mean()
    hi2 = v2.loc[v1.index][tert == "fort"].mean(); lo2 = v2.loc[v1.index][tert == "faible"].mean()
    rows.append(dict(compound=name, n=len(v1),
                     target=sub["target"].iloc[0], pathway=sub["pathway"].iloc[0],
                     rho_ln_ic50=float(rho1), p_ln_ic50=float(p1),
                     rho_auc=float(rho2), p_auc=float(p2),
                     d_ic50_fort_moins_faible=float(hi1 - lo1),
                     ic50_kras_fort=float(hi1), ic50_kras_faible=float(lo1),
                     d_auc_fort_moins_faible=float(hi2 - lo2),
                     auc_kras_fort=float(hi2), auc_kras_faible=float(lo2)))
res = pd.DataFrame(rows)
res["fdr_ln_ic50"] = bh(res["p_ln_ic50"].values)
res["fdr_auc"] = bh(res["p_auc"].values)
res = res.sort_values("rho_ln_ic50", ascending=False)
res.to_csv(os.path.join(DATA, "gdsc_kras_screen.csv"), index=False)
say("\ncomposés testés (n>=15 lignées pancréas) :", len(res))
say("FDR LN_IC50 < 0,05 :", int((res["fdr_ln_ic50"] < 0.05).sum()),
    "| FDR AUC < 0,05 :", int((res["fdr_auc"] < 0.05).sum()))
say("p LN_IC50 < 0,001 :", int((res["p_ln_ic50"] < 0.001).sum()),
    "sur", len(res), "(attendu par hasard ~%.1f)" % (len(res) * 0.001))

say("\nTOP 10 — les plus sensibles chez KRAS-fort (rho LN_IC50 positif) :")
print(res.head(10)[["compound", "target", "pathway", "n", "rho_ln_ic50",
                    "p_ln_ic50", "fdr_ln_ic50", "rho_auc", "fdr_auc",
                    "d_ic50_fort_moins_faible"]].round(3).to_string(index=False))
say("\nTOP 10 — les moins sensibles chez KRAS-fort (rho négatif) :")
print(res.tail(10)[["compound", "target", "pathway", "n", "rho_ln_ic50",
                    "p_ln_ic50", "fdr_ln_ic50", "rho_auc", "fdr_auc",
                    "d_ic50_fort_moins_faible"]].round(3).to_string(index=False))

# 6. Composés prioritaires voie KRAS (présence + résultat)
prio = ["sotorasib", "amg-510", "amg 510", "adagrasib", "mrtx849", "mrtx-849",
        "mrtx1133", "mrtx-1133", "trametinib", "selumetinib", "cobimetinib",
        "binimetinib", "pd0325901", "pd-0325901", "ulixertinib", "sch772984",
        "shp099", "shp-099", "tno155", "bi-3406", "bi3406", "dabrafenib",
        "vemurafenib", "encorafenib", "sorafenib", "raf265", "azd6738"]
say("\n=== COMPOSÉS PRIORITAIRES VOIE KRAS ===")
found = res[res["compound"].str.lower().str.replace(" ", "").str.replace("-", "")
            .isin([p.replace(" ", "").replace("-", "") for p in prio])]
for _, r in found.iterrows():
    say("%-18s cible=%-28s voie=%-28s n=%d rho_IC50=%+.3f p=%.4g FDR=%.3f rho_AUC=%+.3f FDR_AUC=%.3f dIC50=%.2f"
        % (r["compound"], str(r["target"])[:28], str(r["pathway"])[:28],
           r["n"], r["rho_ln_ic50"], r["p_ln_ic50"], r["fdr_ln_ic50"],
           r["rho_auc"], r["fdr_auc"], r["d_ic50_fort_moins_faible"]))
missing = [p for p in prio
           if p.replace(" ", "").replace("-", "") not in
           set(res["compound"].str.lower().str.replace(" ", "").str.replace("-", ""))]
say("prioritaires ABSENTS de GDSC2 :", ", ".join(sorted(set(missing))) or "aucun")

# 7. Effets de classe : médiane des rho par voie (pathway) et par cible
say("\n=== EFFET DE CLASSE — médiane rho LN_IC50 par voie (n>=3 composés) ===")
cls = (res.groupby("pathway")["rho_ln_ic50"]
          .agg(["count", "median", "mean"])
          .query("count >= 3").sort_values("median", ascending=False))
print(cls.round(3).to_string())
say("\n=== EFFET DE CLASSE — médiane rho LN_IC50 par cible (n>=3 composés) ===")
clt = (res.groupby("target")["rho_ln_ic50"]
          .agg(["count", "median", "mean"])
          .query("count >= 3").sort_values("median", ascending=False))
print(clt.round(3).to_string())
cls.to_csv(os.path.join(DATA, "gdsc_kras_screen_pathways.csv"))
clt.to_csv(os.path.join(DATA, "gdsc_kras_screen_targets.csv"))

# 8. Cibles KRAS / MEK / ERK / SHP2 / SOS1 / RAF : tous les composés de ces cibles
say("\n=== TOUS LES COMPOSÉS DES CIBLES KRAS / MEK / ERK / RAF / SHP2 / SOS1 ===")
pat = res["target"].str.contains("KRAS|MEK|ERK|RAF|SHP2|PTPN11|SOS1|BRAF",
                                 case=False, na=False)
sub = res[pat].sort_values("rho_ln_ic50", ascending=False)
print(sub[["compound", "target", "pathway", "n", "rho_ln_ic50",
           "p_ln_ic50", "fdr_ln_ic50", "rho_auc", "fdr_auc"]].round(3)
      .to_string(index=False))
say("\nmédiane rho LN_IC50 de ce groupe :", round(float(sub["rho_ln_ic50"].median()), 3),
    "sur", len(sub), "composés")
say("\nFIN GDSC")
LOG.close()
