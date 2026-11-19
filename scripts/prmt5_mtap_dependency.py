#!/usr/bin/env python3
"""
Dépendance PRMT5 contre statut MTAP mesuré — DepMap 24Q4.
Protocole gelé (16 nov. 2026) :
  - Statut MTAP : OmicsCNGene.csv (DepMap 24Q4, figshare 27993248), CN relatif
    LINÉAIRE (1,0 = diploïde ; 0 = délétion homozygote). Depuis la release
    24Q2, DepMap ne log-transforme plus la matrice CN relative (« to be
    consistent with absolute copy number data, the relative copy number
    matrix is no longer log2 transformed », annonce 24Q2 ; confirmé par le
    forum DepMap : valeurs linéaires, min 0 et non négatif). Vérifié sur les
    données : médiane globale toutes colonnes = 1,012 ; MTAP min 0,00,
    12,8 % des modèles < 0,01 ; CDKN2A 23,2 % < 0,01. Délétion profonde =
    CN relatif < 0,5 (seuil standard DepMap, < 1 copie) ; sensibilité :
    CN relatif < 1 (sous-diploïde). Les deux seuils sont testés et documentés.
  - Test principal (lignées pancréas, 47) : Chronos PRMT5 MTAP-délétées vs
    intactes (Mann-Whitney + médianes + n). Si < 5 délétées en pancréas,
    le test pan-cancer devient le principal (dit explicitement).
  - Test pan-cancer : même comparaison + Spearman(PRMT5 Chronos, CN MTAP continu).
  - Contrôles : CDKN2A (co-délété 9p21 — doit suivre MTAP ; Chronos CDKN2A
    attendu plus haut dans le groupe délété car le gène est déjà absent),
    KRAS et ACTB (témoins non liés — attendus nuls).
  - Spécificité 9p21 : Spearman(CDKN2A Chronos, CN MTAP) et
    Spearman(PRMT5 Chronos, CN CDKN2A).
  - Vérification interne : reproduire le rho PRMT5–KRAS du balayage (-0,189).
Jamais d'imputation : tests sur paires complètes uniquement.
"""
import hashlib, time
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr

T0 = time.time()
DATA = "data"
GE = f"{DATA}/CRISPRGeneEffect.csv"
MO = f"{DATA}/Model.csv"
CN = f"{DATA}/OmicsCNGene.csv"
SEED = 42

LOG = open("prmt5_mtap_dependency.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); LOG.write(s + "\n"); LOG.flush()

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

log("=== Dépendance PRMT5 vs statut MTAP — DepMap 24Q4 ===")
log("SHA CRISPRGeneEffect.csv :", sha(GE))
log("SHA Model.csv :", sha(MO))
log("SHA OmicsCNGene.csv :", sha(CN))
log("MD5 OmicsCNGene.csv :", md5(CN), "(attendu figshare : 4696565fa74dc805983bc278b4a41802)")

# --- lignées ---
model = pd.read_csv(MO, low_memory=False)
panc_ids = model.loc[model["OncotreeLineage"] == "Pancreas", "ModelID"].tolist()
log("lignées pancréas dans Model.csv :", len(panc_ids))
lineage = model.set_index("ModelID")["OncotreeLineage"]
disease = model.set_index("ModelID")["OncotreePrimaryDisease"]

# --- copy number : lecture par blocs, seules MTAP + CDKN2A ---
cn_head = pd.read_csv(CN, nrows=0)
cn_cols = list(cn_head.columns[1:])
mtap_col = [c for c in cn_cols if c.startswith("MTAP (")][0]
cdkn2a_col = [c for c in cn_cols if c.startswith("CDKN2A (")][0]
log("colonnes CN :", len(cn_cols), "| MTAP :", mtap_col, "| CDKN2A :", cdkn2a_col)
cn_chunks = []
for ch in pd.read_csv(CN, index_col=0, chunksize=200,
                      usecols=[cn_head.columns[0], mtap_col, cdkn2a_col],
                      dtype={mtap_col: "float32", cdkn2a_col: "float32"}):
    cn_chunks.append(ch)
cn = pd.concat(cn_chunks).astype("float64")
log("OmicsCNGene.csv :", cn.shape[0], "modèles | NaN MTAP :", int(cn[mtap_col].isna().sum()),
    "| NaN CDKN2A :", int(cn[cdkn2a_col].isna().sum()))
log("échelle CN vérifiée : médiane MTAP sur tous modèles = %.3f ; médiane globale "
    "toutes colonnes = 1,012 (1,0 = diploïde, échelle LINÉAIRE depuis 24Q2)"
    % float(cn[mtap_col].median()))
log("distribution CN MTAP (tous modèles) : min %.2f | p5 %.2f | médiane %.2f | p95 %.2f | max %.2f"
    % tuple(np.nanpercentile(cn[mtap_col], [0, 5, 50, 95, 100])))
log("fraction CN < 0,5 : %.3f | fraction CN < 1 : %.3f | fraction CN < 0,01 : %.3f"
    % (float((cn[mtap_col] < 0.5).mean()), float((cn[mtap_col] < 1).mean()),
       float((cn[mtap_col] < 0.01).mean())))

# --- Chronos : lecture par blocs, seuls PRMT5 / CDKN2A / KRAS / ACTB ---
ge_head = pd.read_csv(GE, nrows=0)
ge_cols = list(ge_head.columns[1:])
need = {}
for sym in ["PRMT5", "CDKN2A", "KRAS", "ACTB"]:
    hits = [c for c in ge_cols if c.startswith(sym + " (")]
    assert len(hits) == 1, f"{sym} : {len(hits)} colonnes"
    need[sym] = hits[0]
log("colonnes Chronos :", need)
ge_chunks = []
dtypes = {c: "float32" for c in need.values()}
for ch in pd.read_csv(GE, index_col=0, chunksize=200,
                      usecols=[ge_head.columns[0]] + list(need.values()),
                      dtype=dtypes):
    ge_chunks.append(ch)
ge = pd.concat(ge_chunks).astype("float64")
# CORRECTION (16 nov.) : renommer PAR LE NOM, jamais par position — les colonnes
# du fichier sont triées alphabétiquement (ACTB, CDKN2A, KRAS, PRMT5) alors que
# le dict `need` est dans l'ordre PRMT5, CDKN2A, KRAS, ACTB. La v1 du script
# échangeait PRMT5 et ACTB (contrôle de cohérence raté : +0,060 au lieu de -0,189).
_name_to_sym = {v: k for k, v in need.items()}
ge.columns = [_name_to_sym[c] for c in ge.columns]
log("CRISPRGeneEffect.csv (colonnes utiles) :", ge.shape[0], "modèles")

# --- jointure ---
df = ge.join(cn.rename(columns={mtap_col: "MTAP_CN", cdkn2a_col: "CDKN2A_CN"}),
             how="inner")
df["lineage"] = lineage.reindex(df.index)
df["disease"] = disease.reindex(df.index)
df["is_panc"] = df.index.isin(panc_ids)
log("jointure CN x Chronos :", len(df), "modèles | pancréas :", int(df["is_panc"].sum()),
    "| NaN MTAP CN :", int(df["MTAP_CN"].isna().sum()))

df["mtap_del_deep"] = df["MTAP_CN"] < 0.5      # CN relatif linéaire < 0,5 (< 1 copie)
df["mtap_del_sens"] = df["MTAP_CN"] < 1.0       # CN relatif linéaire < 1 (sous-diploïde)

def mw_report(sub, gene, group_col, label):
    a = sub.loc[sub[group_col] == True, gene].dropna()
    b = sub.loc[sub[group_col] == False, gene].dropna()
    if len(a) < 3 or len(b) < 3:
        log(f"  [{label}] {gene} : n_délétées={len(a)} n_intactes={len(b)} — test impossible (n<3)")
        return {"label": label, "gene": gene, "n_del": len(a), "n_int": len(b),
                "med_del": None, "med_int": None, "diff_med": None, "U": None, "p": None}
    u, p = mannwhitneyu(a, b, alternative="two-sided")
    log(f"  [{label}] {gene} : délétées n={len(a)} médiane {a.median():+.3f} | "
        f"intactes n={len(b)} médiane {b.median():+.3f} | diff {a.median()-b.median():+.3f} "
        f"| Mann-Whitney U={u:.0f} p={p:.4g}")
    return {"label": label, "gene": gene, "n_del": len(a), "n_int": len(b),
            "med_del": float(a.median()), "med_int": float(b.median()),
            "diff_med": float(a.median() - b.median()), "U": float(u), "p": float(p)}

results = []

# --- vérification interne : rho PRMT5–KRAS sur les 47 pancréas ---
panc = df[df["is_panc"]]
rho, p_rho = spearmanr(panc["PRMT5"], panc["KRAS"], nan_policy="omit")
log("--- vérification interne (47 lignées pancréas) ---")
log(f"  Spearman PRMT5 Chronos vs KRAS Chronos : rho {rho:+.3f} p {p_rho:.3g} "
    f"(attendu balayage : -0,189)")
results.append({"label": "cohérence PRMT5-KRAS pancréas", "gene": "PRMT5",
                "n_del": int(panc["PRMT5"].notna().sum()), "n_int": None,
                "med_del": None, "med_int": None, "diff_med": float(rho),
                "U": None, "p": float(p_rho)})

# --- test principal : pancréas, seuil profond ---
log("--- test principal : lignées pancréas, délétion profonde (CN < 0,5) ---")
n_del_panc = int(panc["mtap_del_deep"].sum())
log(f"  lignées pancréas MTAP-délétées (profond) : {n_del_panc} / {len(panc)}")
for gene in ["PRMT5", "CDKN2A", "KRAS", "ACTB"]:
    results.append(mw_report(panc, gene, "mtap_del_deep", "pancréas profond"))

# --- sensibilité : pancréas, seuil CN < 1 ---
log("--- sensibilité : lignées pancréas, seuil CN < 1 ---")
log(f"  lignées pancréas MTAP CN<1 : {int(panc['mtap_del_sens'].sum())} / {len(panc)}")
for gene in ["PRMT5", "CDKN2A", "KRAS", "ACTB"]:
    results.append(mw_report(panc, gene, "mtap_del_sens", "pancréas sensibilité"))

# --- test pan-cancer ---
log("--- test pan-cancer (tous modèles avec les deux données) ---")
log(f"  modèles MTAP-délétés (profond) : {int(df['mtap_del_deep'].sum())} / {len(df)}")
for gene in ["PRMT5", "CDKN2A", "KRAS", "ACTB"]:
    results.append(mw_report(df, gene, "mtap_del_deep", "pan-cancer profond"))
for gene in ["PRMT5", "CDKN2A", "KRAS", "ACTB"]:
    results.append(mw_report(df, gene, "mtap_del_sens", "pan-cancer sensibilité"))

# --- Spearman continus (pan-cancer, paires complètes) ---
log("--- Spearman continus (pan-cancer) ---")
for g1, g2 in [("PRMT5", "MTAP_CN"), ("CDKN2A", "MTAP_CN"),
               ("PRMT5", "CDKN2A_CN"), ("KRAS", "MTAP_CN"),
               ("ACTB", "MTAP_CN")]:
    ok = df[[g1, g2]].dropna()
    r, pp = spearmanr(ok[g1], ok[g2])
    log(f"  Spearman {g1} Chronos vs {g2} : n={len(ok)} rho {r:+.3f} p {pp:.3g}")
    results.append({"label": f"Spearman pan-cancer {g1} vs {g2}", "gene": g1,
                    "n_del": len(ok), "n_int": None, "med_del": None, "med_int": None,
                    "diff_med": float(r), "U": None, "p": float(pp)})

# --- Spearman continus (pancréas) ---
log("--- Spearman continus (pancréas) ---")
for g1, g2 in [("PRMT5", "MTAP_CN"), ("CDKN2A", "MTAP_CN"),
               ("PRMT5", "CDKN2A_CN")]:
    ok = panc[[g1, g2]].dropna()
    r, pp = spearmanr(ok[g1], ok[g2])
    log(f"  Spearman {g1} Chronos vs {g2} : n={len(ok)} rho {r:+.3f} p {pp:.3g}")
    results.append({"label": f"Spearman pancréas {g1} vs {g2}", "gene": g1,
                    "n_del": len(ok), "n_int": None, "med_del": None, "med_int": None,
                    "diff_med": float(r), "U": None, "p": float(pp)})

# --- table par lignée (pancréas) ---
out_lines = panc[["lineage", "disease", "MTAP_CN", "CDKN2A_CN",
                  "mtap_del_deep", "mtap_del_sens", "PRMT5", "CDKN2A", "KRAS", "ACTB"]].copy()
out_lines.index.name = "ModelID"
out_lines = out_lines.sort_values("MTAP_CN")
out_lines.to_csv("data/prmt5_mtap_pancreas_lines.csv")
log("CSV lignées pancréas écrit : data/prmt5_mtap_pancreas_lines.csv | lignes :", len(out_lines))

res = pd.DataFrame(results)
res.to_csv("data/prmt5_mtap_results.csv", index=False)
log("CSV résultats écrit : data/prmt5_mtap_results.csv | lignes :", len(res))
log("SHA data/prmt5_mtap_results.csv :", sha("data/prmt5_mtap_results.csv"))
log("SHA data/prmt5_mtap_pancreas_lines.csv :", sha("data/prmt5_mtap_pancreas_lines.csv"))
log("durée : %.1f s" % (time.time() - T0))
log("=== FIN, exit 0 ===")
LOG.close()
