"""PRISM Repurposing Secondary Screen 19Q4 — test médicamenteux dose-réponse.
Question : parmi les lignées pancréatiques, les lignées les plus dépendantes
de KRAS (axe du sous-groupe v4 TCGA) répondent-elles mieux à certains
médicaments en DOSE-RÉPONSE (AUC / IC50) ? Le primaire (une seule dose
2,5 µM) était négatif ; une seule dose peut rater un vrai effet.
Test par composé : corrélation de Spearman entre AUC (et log10 IC50) PRISM
secondaire et l'effet Chronos KRAS (DepMap 24Q4), + moyennes par tertile KRAS.
Sens : rho > 0 = les lignées KRAS-dépendantes (Chronos négatif) sont plus
sensibles (AUC / IC50 plus bas).
Provenance : PRISM Repurposing 19Q4, Corsello et al. Nat Cancer 2020,
figshare article 9393293 (DOI 10.6084/m9.figshare.9393293.v4), fichier
secondary-screen-dose-response-curve-parameters.csv (MD5 vérifié).
Règles : jamais d'imputation ; tertiles étiquetés « fort » = Chronos le plus
négatif = le plus dépendant (VÉRIFIÉ par assertion — dans prism_screen.py
les étiquettes étaient inversées) ; FDR Benjamini-Hochberg sur l'ensemble
testé ; un hit isolé sans effet de classe = curiosité, pas un candidat.
"""
import csv, hashlib, os
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
LOG = open(os.path.join(BASE, "prism_secondary_screen.log"), "w")

def say(*a):
    print(*a, flush=True)
    print(*a, file=LOG, flush=True)

def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

PARAMS = os.path.join(DATA, "secondary-screen-dose-response-curve-parameters.csv")
say("Fichier :", PARAMS)
say("Taille :", os.path.getsize(PARAMS), "octets ; MD5", md5(PARAMS),
    "(attendu e629b9d505ad3d6bf65fde96f1c54bee)")

# 1. Lecture (colonnes utiles seulement)
cols = ["broad_id", "depmap_id", "screen_id", "auc", "ic50", "name",
        "moa", "target", "passed_str_profiling"]
p = pd.read_csv(PARAMS, usecols=cols)
say("Lignes lues :", len(p), "| broad_id uniques :", p["broad_id"].nunique(),
    "| noms uniques :", p["name"].nunique(),
    "| depmap_id uniques :", p["depmap_id"].nunique())
say("Écrans :", p["screen_id"].value_counts().to_dict())
say("IC50 NA :", int(p["ic50"].isna().sum()), "/", len(p),
    "| AUC NA :", int(p["auc"].isna().sum()))

# 2. Nettoyage : pas de depmap_id = pas de jointure possible (barcodes contrôles).
#    Le flag STR=False ne concerne que ces lignes (vérifié) : rien d'autre à écarter.
say("Lignes sans depmap_id :", int(p["depmap_id"].isna().sum()),
    "| dont STR=False :", int((p["depmap_id"].isna() & ~p["passed_str_profiling"]).sum()))
p = p.dropna(subset=["depmap_id"])
say("Après retrait des lignes sans depmap_id :", len(p),
    "| STR=False restantes :", int((~p["passed_str_profiling"]).sum()))

# 3. Déduplication (broad_id, depmap_id) entre écrans.
#    Le readme recommande MTS010 quand disponible (redos techniques des 147
#    composés d'oncologie). Priorité : MTS010 > HTS002 > MTS006 > MTS005.
prio = {"MTS010": 0, "HTS002": 1, "MTS006": 2, "MTS005": 3}
p["prio"] = p["screen_id"].map(prio)
n_dup = int(p.duplicated(subset=["broad_id", "depmap_id"], keep=False).sum())
p = p.sort_values("prio").drop_duplicates(subset=["broad_id", "depmap_id"],
                                          keep="first")
say("Lignes en doublon (broad_id, depmap_id) avant dédup :", n_dup,
    "| lignes après dédup :", len(p))
say("Écrans après dédup :", p["screen_id"].value_counts().to_dict())

# 4. Agrégation par nom de composé (54 noms ont 2 broad_id : médiane).
p["log10_ic50"] = np.log10(p["ic50"])
agg = (p.groupby(["depmap_id", "name"])
         .agg(auc=("auc", "median"),
              log10_ic50=("log10_ic50", "median"),
              moa=("moa", "first"),
              target=("target", "first"),
              n_batches=("broad_id", "nunique"))
         .reset_index())
say("Composés (noms) après agrégation :", agg["name"].nunique(),
    "| (lignée, composé) :", len(agg))

# 5. Lignées pancréas via Model.csv + axe KRAS (Chronos DepMap 24Q4)
mod = pd.read_csv(os.path.join(DATA, "Model.csv"))
panc_mod = set(mod.loc[mod["OncotreeLineage"] == "Pancreas", "ModelID"])
say("Lignées pancréas DepMap (OncotreeLineage == Pancreas) :", len(panc_mod))
with open(os.path.join(DATA, "CRISPRGeneEffect.csv")) as f:
    header = next(csv.reader(f))
kpos = [i for i, c in enumerate(header) if c.startswith("KRAS (")][0]
ge = pd.read_csv(os.path.join(DATA, "CRISPRGeneEffect.csv"),
                 usecols=[0, kpos], index_col=0)
ge.columns = ["KRAS"]
kras = ge["KRAS"].dropna()
ap = agg[agg["depmap_id"].isin(panc_mod)]
common = sorted(set(ap["depmap_id"]) & set(kras.index))
say("Lignées pancréas dans PRISM secondaire :", ap["depmap_id"].nunique())
say("Lignées pancréas communes PRISM x DepMap KRAS :", len(common))
k = kras.loc[common]
say("KRAS Chronos : min %.2f médiane %.2f max %.2f"
    % (k.min(), k.median(), k.max()))
ap = ap[ap["depmap_id"].isin(common)].set_index("depmap_id")

# 6. Test par composé
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
for name, sub in ap.groupby("name"):
    v_auc = sub["auc"].dropna()
    if len(v_auc) < 15:
        continue
    kk = k.loc[v_auc.index]
    # Tertiles de DÉPENDANCE : Chronos le plus négatif = le plus dépendant.
    # qcut étiquette par ordre croissant : le 1er tiers (Chronos bas) est donc
    # le plus dépendant -> étiquette "fort". VÉRIFICATION explicite :
    tert = pd.qcut(kk, 3, labels=["fort", "moyen", "faible"])
    assert tert[kk == kk.min()].iloc[0] == "fort", "étiquette tertile inversée !"
    assert kk[tert == "fort"].mean() < kk[tert == "faible"].mean()
    rho_a, p_a = spearmanr(v_auc, kk)
    v_ic = sub["log10_ic50"].dropna()
    if len(v_ic) >= 15:
        kk2 = k.loc[v_ic.index]
        rho_i, p_i = spearmanr(v_ic, kk2)
        tert2 = pd.qcut(kk2, 3, labels=["fort", "moyen", "faible"])
        hi_i = v_ic[tert2 == "fort"].mean(); lo_i = v_ic[tert2 == "faible"].mean()
        n_ic = len(v_ic)
    else:
        rho_i, p_i, hi_i, lo_i, n_ic = np.nan, np.nan, np.nan, np.nan, len(v_ic)
    hi_a = v_auc[tert == "fort"].mean(); lo_a = v_auc[tert == "faible"].mean()
    rows.append(dict(compound=name, n_auc=len(v_auc), n_ic50=n_ic,
                     moa=sub["moa"].iloc[0], target=sub["target"].iloc[0],
                     rho_auc=float(rho_a), p_auc=float(p_a),
                     rho_ic50=float(rho_i), p_ic50=float(p_i),
                     d_auc_fort_moins_faible=float(hi_a - lo_a),
                     auc_kras_fort=float(hi_a), auc_kras_faible=float(lo_a),
                     d_log10ic50_fort_moins_faible=float(hi_i - lo_i),
                     log10ic50_kras_fort=float(hi_i),
                     log10ic50_kras_faible=float(lo_i)))
res = pd.DataFrame(rows)
res["fdr_auc"] = bh(res["p_auc"].values)
res["fdr_ic50"] = bh(res["p_ic50"].fillna(1.0).values)
res = res.sort_values("rho_auc", ascending=False)
res.to_csv(os.path.join(DATA, "prism_secondary_kras_screen.csv"), index=False)
say("\nComposés testés (n_auc >= 15 lignées pancréas) :", len(res))
say("Composés avec n_ic50 >= 15 :", int((res["n_ic50"] >= 15).sum()))
say("FDR AUC < 0,05 :", int((res["fdr_auc"] < 0.05).sum()),
    "| FDR IC50 < 0,05 :", int((res["fdr_ic50"] < 0.05).sum()))
say("p AUC < 0,001 :", int((res["p_auc"] < 0.001).sum()),
    "sur", len(res), "(attendu par hasard ~%.1f)" % (len(res) * 0.001))
say("Médiane rho AUC sur les %d composés : %+.3f" % (len(res), res["rho_auc"].median()))
say("Part des rho AUC > 0 : %.1f %%" % (100 * (res["rho_auc"] > 0).mean()))

say("\nTOP 10 — les plus sensibles chez KRAS-fort (rho AUC positif) :")
print(res.head(10)[["compound", "moa", "target", "n_auc", "n_ic50",
                    "rho_auc", "p_auc", "fdr_auc", "rho_ic50", "fdr_ic50",
                    "d_auc_fort_moins_faible"]].round(3).to_string(index=False))
say("\nTOP 10 — les moins sensibles chez KRAS-fort (rho AUC négatif) :")
print(res.tail(10)[["compound", "moa", "target", "n_auc", "n_ic50",
                    "rho_auc", "p_auc", "fdr_auc", "rho_ic50", "fdr_ic50",
                    "d_auc_fort_moins_faible"]].round(3).to_string(index=False))

# 7. Composés prioritaires voie KRAS (présence + résultat)
prio_names = ["mrtx1133", "rmc6236", "sotorasib", "amg510", "adagrasib",
              "mrtx849", "bi3406", "shp099", "tno155", "cobimetinib",
              "binimetinib", "trametinib", "selumetinib", "refametinib",
              "pd0325901", "ulixertinib", "sch772984", "erk2440", "erk6604",
              "dabrafenib", "vemurafenib", "encorafenib", "sorafenib"]
norm = res["compound"].str.lower().str.replace(" ", "").str.replace("-", "")
say("\n=== COMPOSÉS PRIORITAIRES VOIE KRAS ===")
for pn in prio_names:
    hit = res[norm == pn.replace("-", "")]
    if len(hit):
        r = hit.iloc[0]
        say("%-14s moa=%-42s n=%d rho_AUC=%+.3f p=%.4g FDR=%.3f rho_IC50=%+.3f FDR_IC50=%.3f dAUC=%.3f"
            % (r["compound"], str(r["moa"])[:42], r["n_auc"], r["rho_auc"],
               r["p_auc"], r["fdr_auc"], r["rho_ic50"], r["fdr_ic50"],
               r["d_auc_fort_moins_faible"]))
    else:
        say("%-14s ABSENT du secondaire PRISM 19Q4" % pn)
say("Prioritaires ABSENTS (vérifié sur les noms du fichier) :",
    ", ".join(p for p in prio_names
              if p.replace("-", "") not in set(norm)) or "aucun")

# 8. Tous les composés des cibles KRAS / MEK / ERK / RAF / SHP2 / SOS1
say("\n=== TOUS LES COMPOSÉS DES CIBLES KRAS / MEK / ERK / RAF / SHP2 / SOS1 ===")
pat = res["target"].str.contains("KRAS|MEK|ERK|RAF|SHP2|PTPN11|SOS1|BRAF",
                                 case=False, na=False)
sub = res[pat].sort_values("rho_auc", ascending=False)
print(sub[["compound", "moa", "target", "n_auc", "rho_auc",
           "p_auc", "fdr_auc", "rho_ic50", "fdr_ic50"]].round(3)
      .to_string(index=False))
say("Médiane rho AUC de ce groupe :", round(float(sub["rho_auc"].median()), 3),
    "sur", len(sub), "composés")

# 9. Effets de classe : médiane des rho AUC par MOA et par cible
say("\n=== EFFET DE CLASSE — médiane rho AUC par MOA (n>=3 composés) ===")
cls_m = (res.groupby("moa")["rho_auc"]
            .agg(["count", "median", "mean"])
            .query("count >= 3").sort_values("median", ascending=False))
print(cls_m.round(3).to_string())
say("\n=== EFFET DE CLASSE — médiane rho AUC par cible (n>=3 composés) ===")
cls_t = (res.groupby("target")["rho_auc"]
            .agg(["count", "median", "mean"])
            .query("count >= 3").sort_values("median", ascending=False))
print(cls_t.round(3).to_string())
cls_m.to_csv(os.path.join(DATA, "prism_secondary_kras_screen_moa.csv"))
cls_t.to_csv(os.path.join(DATA, "prism_secondary_kras_screen_targets.csv"))

say("\nFIN PRISM SECONDAIRE")
LOG.close()
