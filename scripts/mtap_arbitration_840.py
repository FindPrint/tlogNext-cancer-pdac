#!/usr/bin/env python3
"""
Chantier 1 — ARBITRER LA CONTRADICTION MTAP (§8.40, 19 nov. 2026).
Question : le groupe MTAP-délété se distingue-t-il vraiment ?
Contexte : v6.2 donne S_sep MTAP +0,1968 (réel > nul) mais MC -0,1642 et
Delta -0,5416 inversés (2 runs v6.2, cascades = v6.1, §8.38).

Tests directs, données du jour uniquement, aucun run de pipeline :
(a) Dépendance PRMT5 (Chronos) par copie MTAP, lignée par lignée
    (groupes CN < 0,5 vs intact ; médianes ; Mann-Whitney ; Spearman
    continu) + effet CDKN2A quand MTAP est fixé (stratification CN et
    stratification mutation, reconfirmation du p=0,76 du §8.36).
(b) Écrans de médicaments déjà détenus (PRISM primaire 24Q2, PRISM
    secondaire 19Q4, GDSC2) : composés différentiels MTAP-délété vs
    intact (Mann-Whitney + FDR Benjamini-Hochberg), classes, recherche
    ciblée PRMT5 / MAT2A.
(c) Lien avec l'axe KRAS : Fisher TCGA reconfirmé depuis
    mtap_gistic_status.csv (délétion GISTIC -2, top-12 KRAS) + Fisher
    lignées (MTAP-délété vs 12 plus KRAS-dépendantes, Chronos KRAS)
    + chevauchements lignées/tumeurs.

Définitions gelées ici (avant tout calcul) :
- CN DepMap = relatif LINÉAIRE (1,0 = diploïde), OmicsCNGene 24Q4.
  Délétion profonde : CN < 0,5. Sensibilité : CN < 1.
- Chronos : plus négatif = plus dépendant.
- Médicaments : PRISM primaire = log-fold-change viabilité (plus bas =
  plus sensible) ; PRISM secondaire AUC (plus bas = plus sensible) ;
  GDSC2 LN_IC50 et AUC (plus bas = plus sensible).
- Seuil de test par composé : n_délétées >= 5 ET n_intactes >= 5
  (valeurs non manquantes) ; FDR BH sur l'ensemble testé, par écran
  et par mesure. Aucune imputation, paires complètes uniquement.
- Fisher bilatéral, critère pré-enregistré (§8.26).
Aucun code original modifié ; ce script est neuf.
"""
import hashlib, json, math, time
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr, fisher_exact

T0 = time.time()
DATA = "data"
LOG = open("mtap_arbitration_840.log", "w")
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

def bh(pvals):
    """Benjamini-Hochberg FDR, retourne array même ordre."""
    p = np.asarray(pvals, dtype=float)
    n = len(p); out = np.full(n, np.nan)
    ok = ~np.isnan(p)
    q = p[ok]; m = len(q)
    order = np.argsort(q); ranked = q[order]
    adj = ranked * m / (np.arange(m) + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    adj = np.clip(adj, 0, 1)
    tmp = np.empty(m); tmp[order] = adj
    out[ok] = tmp
    return out

def cohen_d(a, b):
    a = np.asarray(a, dtype=float); b = np.asarray(b, dtype=float)
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    sp = math.sqrt(((na - 1) * va + (nb - 1) * vb) / max(na + nb - 2, 1))
    return float((a.mean() - b.mean()) / sp) if sp > 0 else float("nan")

def mw(a, b):
    a = np.asarray(a, dtype=float); a = a[np.isfinite(a)]
    b = np.asarray(b, dtype=float); b = b[np.isfinite(b)]
    if len(a) < 3 or len(b) < 3:
        return len(a), len(b), float(np.median(a)) if len(a) else None, \
            float(np.median(b)) if len(b) else None, None, None, None
    u, p = mannwhitneyu(a, b, alternative="two-sided")
    return len(a), len(b), float(np.median(a)), float(np.median(b)), \
        float(np.median(a) - np.median(b)), float(u), float(p)

log("=== §8.40 Arbitrage MTAP — tests directs, 19 nov. 2026 ===")
for f in ["CRISPRGeneEffect.csv", "Model.csv", "OmicsCNGene.csv",
          "Repurposing_Public_24Q2_Extended_Primary_Data_Matrix.csv",
          "Repurposing_Public_24Q2_Extended_Primary_Compound_List.csv",
          "Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv",
          "secondary-screen-dose-response-curve-parameters.csv",
          "GDSC2_fitted_dose_response_27Oct23.xlsx",
          "mutation_table_pancreas.csv"]:
    p = f"{DATA}/{f}"
    log(f"SHA {f} : {sha(p)}")
log("MD5 OmicsCNGene.csv :", md5(f"{DATA}/OmicsCNGene.csv"),
    "(attendu figshare : 4696565fa74dc805983bc278b4a41802)")
log("SHA mtap_gistic_status.csv :", sha("mtap_gistic_status.csv"),
    "(attendu §8.26 : b54cb94ff6aaba67e71524476d4e47c567f20ca8d49c09c52a9118977a7c38cb)")

# ---------------------------------------------------------------- (a) DepMap
model = pd.read_csv(f"{DATA}/Model.csv", low_memory=False)
panc_ids = model.loc[model["OncotreeLineage"] == "Pancreas", "ModelID"].tolist()
lineage = model.set_index("ModelID")["OncotreeLineage"]
disease = model.set_index("ModelID")["OncotreePrimaryDisease"]
sanger2ach = model.dropna(subset=["SangerModelID"]).set_index("SangerModelID")["ModelID"].to_dict()

cn_head = pd.read_csv(f"{DATA}/OmicsCNGene.csv", nrows=0)
cn_cols = list(cn_head.columns[1:])
mtap_col = [c for c in cn_cols if c.startswith("MTAP (")][0]
cdkn2a_col = [c for c in cn_cols if c.startswith("CDKN2A (")][0]
cn_chunks = []
for ch in pd.read_csv(f"{DATA}/OmicsCNGene.csv", index_col=0, chunksize=200,
                      usecols=[cn_head.columns[0], mtap_col, cdkn2a_col],
                      dtype={mtap_col: "float32", cdkn2a_col: "float32"}):
    cn_chunks.append(ch)
cn = pd.concat(cn_chunks).astype("float64")
log("OmicsCNGene : modèles", cn.shape[0], "| médiane MTAP", round(float(cn[mtap_col].median()), 3),
    "| min", round(float(cn[mtap_col].min()), 3), "| négatifs", int((cn[mtap_col] < 0).sum()),
    "-> échelle LINÉAIRE confirmée (aucune valeur négative)")

ge_head = pd.read_csv(f"{DATA}/CRISPRGeneEffect.csv", nrows=0)
ge_cols = list(ge_head.columns[1:])
need = {}
for sym in ["PRMT5", "CDKN2A", "KRAS", "ACTB", "MAT2A"]:
    hits = [c for c in ge_cols if c.startswith(sym + " (")]
    assert len(hits) == 1, f"{sym} : {len(hits)} colonnes"
    need[sym] = hits[0]
log("colonnes Chronos :", need)
ge_chunks = []
dtypes = {c: "float32" for c in need.values()}
for ch in pd.read_csv(f"{DATA}/CRISPRGeneEffect.csv", index_col=0, chunksize=200,
                      usecols=[ge_head.columns[0]] + list(need.values()), dtype=dtypes):
    ge_chunks.append(ch)
ge = pd.concat(ge_chunks).astype("float64")
_name_to_sym = {v: k for k, v in need.items()}
ge.columns = [_name_to_sym[c] for c in ge.columns]

df = ge.join(cn.rename(columns={mtap_col: "MTAP_CN", cdkn2a_col: "CDKN2A_CN"}), how="inner")
df["lineage"] = lineage.reindex(df.index)
df["disease"] = disease.reindex(df.index)
df["is_panc"] = df.index.isin(panc_ids)
df["mtap_del"] = df["MTAP_CN"] < 0.5
df["mtap_del_sens"] = df["MTAP_CN"] < 1.0
df["cdkn2a_del"] = df["CDKN2A_CN"] < 0.5
log("jointure CN x Chronos :", len(df), "modèles | pancréas :", int(df["is_panc"].sum()))
panc = df[df["is_panc"]].copy()
log("pancréas MTAP-délétées (CN<0,5) :", int(panc["mtap_del"].sum()), "/", len(panc),
    "| CN<1 :", int(panc["mtap_del_sens"].sum()), "/", len(panc))
log("pan-cancer MTAP-délétées (CN<0,5) :", int(df["mtap_del"].sum()), "/", len(df))

rows = []
def record(test, gene, scope, n_del, n_int, med_del, med_int, diff, U, p, extra=""):
    rows.append({"test": test, "gene": gene, "scope": scope, "n_del": n_del,
                 "n_int": n_int, "med_del": med_del, "med_int": med_int,
                 "diff_med": diff, "U": U, "p": p, "extra": extra})

log("--- (a1) PRMT5 pancréas, délétion profonde CN<0,5 ---")
for gene in ["PRMT5", "MAT2A", "CDKN2A", "KRAS", "ACTB"]:
    n1, n2, m1, m2, d, u, p = mw(panc.loc[panc["mtap_del"], gene],
                                panc.loc[~panc["mtap_del"], gene])
    log(f"  pancréas {gene} : délétées n={n1} méd {m1:+.3f} | intactes n={n2} méd {m2:+.3f} "
        f"| diff {d:+.3f} | U={u} p={p:.4g}")
    record("a1_pancreas_CN<0.5", gene, "pancreas", n1, n2, m1, m2, d, u, p)
log("--- (a1 sensibilité) PRMT5 pancréas, CN<1 ---")
for gene in ["PRMT5", "MAT2A"]:
    n1, n2, m1, m2, d, u, p = mw(panc.loc[panc["mtap_del_sens"], gene],
                                panc.loc[~panc["mtap_del_sens"], gene])
    log(f"  pancréas CN<1 {gene} : n={n1}/{n2} méd {m1:+.3f}/{m2:+.3f} diff {d:+.3f} p={p:.4g}")
    record("a1_pancreas_CN<1", gene, "pancreas", n1, n2, m1, m2, d, u, p)
log("--- (a2) pan-cancer ---")
for gene in ["PRMT5", "MAT2A", "CDKN2A", "KRAS", "ACTB"]:
    n1, n2, m1, m2, d, u, p = mw(df.loc[df["mtap_del"], gene], df.loc[~df["mtap_del"], gene])
    log(f"  pan-cancer {gene} : n={n1}/{n2} méd {m1:+.3f}/{m2:+.3f} diff {d:+.3f} p={p:.4g}")
    record("a2_pancancer_CN<0.5", gene, "pancancer", n1, n2, m1, m2, d, u, p)
log("--- (a2) Spearman continu PRMT5/MAT2A vs CN MTAP ---")
for scope, sub in [("pancreas", panc), ("pancancer", df)]:
    for gene in ["PRMT5", "MAT2A"]:
        ok = sub[[gene, "MTAP_CN"]].dropna()
        r, pp = spearmanr(ok[gene], ok["MTAP_CN"])
        log(f"  Spearman {scope} {gene} vs CN MTAP : n={len(ok)} rho {r:+.3f} p={pp:.3g}")
        record(f"a2_spearman_{scope}", gene, scope, len(ok), None, None, None,
               float(r), None, float(pp))
# cohérence interne : rho PRMT5-KRAS pancréas (attendu -0,189)
r, pp = spearmanr(panc["PRMT5"], panc["KRAS"], nan_policy="omit")
log(f"  cohérence interne Spearman PRMT5-KRAS pancréas : rho {r:+.3f} p={pp:.3g} (attendu -0,189)")

log("--- (a3) CDKN2A fixé, stratification par CN (neuf, données du jour) ---")
for scope, sub in [("pancreas", panc), ("pancancer", df)]:
    for stratum, mask in [("MTAP-intacte", ~sub["mtap_del"]), ("MTAP-délétée", sub["mtap_del"])]:
        s = sub[mask]
        n1, n2, m1, m2, d, u, p = mw(s.loc[s["cdkn2a_del"], "PRMT5"],
                                    s.loc[~s["cdkn2a_del"], "PRMT5"])
        dd = cohen_d(s.loc[s["cdkn2a_del"], "PRMT5"].dropna(),
                     s.loc[~s["cdkn2a_del"], "PRMT5"].dropna()) if n1 >= 3 and n2 >= 3 else None
        log(f"  {scope} [{stratum}] CDKN2A-délétée vs intacte, PRMT5 : n={n1}/{n2} "
            f"méd {m1}/{m2} diff {d} p={p} d={dd}")
        record(f"a3_CDKN2A_CN_fixe_{stratum}", "PRMT5", scope, n1, n2, m1, m2, d, u, p,
               extra=f"d_cohen={dd}")

log("--- (a4) CDKN2A fixé, stratification par MUTATION (reconfirmation §8.36, p=0,76) ---")
mut = pd.read_csv(f"{DATA}/mutation_table_pancreas.csv", comment="#")
log("table mutations : lignes", len(mut), "| colonnes", list(mut.columns[:7]))
mut = mut.set_index("ModelID")
mj = panc.join(mut[["CDKN2A_mut", "TP53_mut", "SMAD4_mut", "KRAS_mut"]], how="inner")
log("jointure pancréas x mutations :", len(mj), "lignées (attendu 45)")
log("  CDKN2A mutées :", int(mj["CDKN2A_mut"].sum()), "| MTAP-délétées parmi mutées :",
    int(mj.loc[mj["CDKN2A_mut"] == 1, "mtap_del"].sum()), "/",
    int(mj.loc[mj["CDKN2A_mut"] == 1].shape[0]),
    "| parmi sauvages :", int(mj.loc[mj["CDKN2A_mut"] == 0, "mtap_del"].sum()), "/",
    int(mj.loc[mj["CDKN2A_mut"] == 0].shape[0]))
log("  CN MTAP médiane mutées :", round(float(mj.loc[mj["CDKN2A_mut"] == 1, "MTAP_CN"].median()), 3),
    "| sauvages :", round(float(mj.loc[mj["CDKN2A_mut"] == 0, "MTAP_CN"].median()), 3))
for stratum, mask in [("non stratifié", np.ones(len(mj), dtype=bool)),
                      ("MTAP-intacte", ~mj["mtap_del"].values),
                      ("MTAP-délétée", mj["mtap_del"].values)]:
    s = mj[mask]
    a = s.loc[s["CDKN2A_mut"] == 1, "PRMT5"].dropna()
    b = s.loc[s["CDKN2A_mut"] == 0, "PRMT5"].dropna()
    n1, n2, m1, m2, d, u, p = mw(a, b)
    dd = cohen_d(a, b) if len(a) >= 3 and len(b) >= 3 else None
    log(f"  [{stratum}] CDKN2A mut vs sauv, PRMT5 : n={n1}/{n2} méd {m1}/{m2} "
        f"diff {d} p={p} d={dd}")
    record(f"a4_CDKN2A_mut_fixe_{stratum}", "PRMT5", "pancreas", n1, n2, m1, m2, d, u, p,
           extra=f"d_cohen={dd}")

# ---------------------------------------------------------------- (c) Fisher
log("--- (c1) Fisher TCGA reconfirmé depuis mtap_gistic_status.csv ---")
gst = pd.read_csv("mtap_gistic_status.csv")
# EXCLURE la tumeur sans GISTIC (TCGA-FB-A4P6, NaN) : le Fisher §8.26 porte
# sur les 177 appariées, pas 178. Sans cette exclusion, la tumeur NaN tombe
# dans la case « reste, non délétée » (166 au lieu de 165) et p passe à 0,041.
gst = gst.dropna(subset=["mtap_gistic"])
log("mtap_gistic_status.csv : lignes appariées (GISTIC non manquant) :", len(gst),
    "(attendu 177)")
log("mtap_gistic_status.csv : lignes", len(gst), "| colonnes", list(gst.columns))
# identifier les colonnes : statut MTAP, rang KRAS / top12
print(gst.head(3).to_string(), file=LOG)
kras_top_col = None
for c in gst.columns:
    if "kras" in c.lower() and ("top" in c.lower() or "fort" in c.lower() or "rank" in c.lower()):
        kras_top_col = c
log("colonnes GISTIC :", [c for c in gst.columns])
mtap_col_g = [c for c in gst.columns if "MTAP" in c.upper()][0]
log("colonne MTAP utilisée :", mtap_col_g, "| colonne KRAS-fort :", kras_top_col)
# Déterminer top-12 : si pas de colonne, ordre KRAS = ordre du fichier (tri KRAS croissant)
# Le fichier est trié par expression KRAS croissante (voir mtap.md) : les 12 dernières = KRAS-forts.
if kras_top_col is not None:
    is_top = gst[kras_top_col].astype(bool) if gst[kras_top_col].dtype == bool else (gst[kras_top_col] == 1)
else:
    is_top = pd.Series([False] * (len(gst) - 12) + [True] * 12, index=gst.index)
    log("top-12 = 12 dernières lignes du fichier trié KRAS croissant (convention mtap.md)")
is_del = (gst[mtap_col_g] == -2)
a = int((is_top & is_del).sum()); b = int((is_top & ~is_del).sum())
c_ = int(((~is_top) & is_del).sum()); d_ = int(((~is_top) & ~is_del).sum())
or_, p_f = fisher_exact([[a, b], [c_, d_]], alternative="two-sided")
log(f"  TCGA Fisher MTAP -2 : KRAS-forts {a}/{a+b} ({100*a/(a+b):.0f}%) vs reste {c_}/{c_+d_} "
    f"({100*c_/(c_+d_):.0f}%) | OR={or_:.2f} p={p_f:.4g} (attendu §8.26 : 6/12 vs 37/165, OR 3,46, p=0,073)")
record("c1_fisher_TCGA", "MTAP_del", "TCGA", a, c_, None, None, float(or_), None, float(p_f),
       extra=f"table [[{a},{b}],[{c_},{d_}]]")
top12_ids = gst.loc[is_top].iloc[:, 0].tolist() if gst.shape[1] else []
log("  tumeurs KRAS-forts MTAP-délétées (chevauchement) :", a, "sur 12")

log("--- (c2) Fisher lignées pancréas : MTAP-délété vs KRAS-fort (Chronos) ---")
panc_sorted = panc.sort_values("KRAS")  # Chronos le plus négatif = le plus dépendant
kras_fort_ids = panc_sorted.index[:12].tolist()
panc["kras_fort12"] = panc.index.isin(kras_fort_ids)
a2 = int((panc["kras_fort12"] & panc["mtap_del"]).sum())
b2 = int((panc["kras_fort12"] & ~panc["mtap_del"]).sum())
c2 = int(((~panc["kras_fort12"]) & panc["mtap_del"]).sum())
d2 = int(((~panc["kras_fort12"]) & ~panc["mtap_del"]).sum())
or2, p2 = fisher_exact([[a2, b2], [c2, d2]], alternative="two-sided")
log(f"  lignées Fisher (top-12 KRAS-dépendantes) : MTAP-délétées {a2}/12 vs reste {c2}/{c2+d2} "
    f"| OR={or2:.2f} p={p2:.4g} | table [[{a2},{b2}],[{c2},{d2}]]")
record("c2_fisher_lignees_top12", "MTAP_del", "pancreas", a2, c2, None, None, float(or2), None, float(p2),
       extra=f"table [[{a2},{b2}],[{c2},{d2}]]")
# tertile
thr = panc["KRAS"].quantile(1/3)
panc["kras_fort_tert"] = panc["KRAS"] <= thr
a3 = int((panc["kras_fort_tert"] & panc["mtap_del"]).sum())
b3 = int((panc["kras_fort_tert"] & ~panc["mtap_del"]).sum())
c3 = int(((~panc["kras_fort_tert"]) & panc["mtap_del"]).sum())
d3 = int(((~panc["kras_fort_tert"]) & ~panc["mtap_del"]).sum())
or3, p3 = fisher_exact([[a3, b3], [c3, d3]], alternative="two-sided")
log(f"  lignées Fisher (tertile KRAS-dépendant, n={int(panc['kras_fort_tert'].sum())}) : "
    f"MTAP-délétées {a3} vs reste {c3} | OR={or3:.2f} p={p3:.4g} | table [[{a3},{b3}],[{c3},{d3}]]")
record("c2_fisher_lignees_tertile", "MTAP_del", "pancreas", a3, c3, None, None, float(or3), None, float(p3),
       extra=f"table [[{a3},{b3}],[{c3},{d3}]]")
overlap_ids = sorted(set(kras_fort_ids) & set(panc.loc[panc["mtap_del"]].index.tolist()))
log("  chevauchement lignées MTAP-délétées ∩ top-12 KRAS :", len(overlap_ids), overlap_ids)
log("  lignées MTAP-délétées :", sorted(panc.loc[panc["mtap_del"]].index.tolist()))
log("  lignées top-12 KRAS-dépendantes :", sorted(kras_fort_ids))
# corrélation continue MTAP CN vs KRAS Chronos (lignées)
ok = panc[["MTAP_CN", "KRAS"]].dropna()
r, pp = spearmanr(ok["MTAP_CN"], ok["KRAS"])
log(f"  Spearman lignées CN MTAP vs Chronos KRAS : n={len(ok)} rho {r:+.3f} p={pp:.3g}")
record("c2_spearman_CNMTAP_KRAS", "KRAS", "pancreas", len(ok), None, None, None, float(r), None, float(pp))
# table par lignée pour le CSV
panc_out = panc[["lineage", "disease", "MTAP_CN", "CDKN2A_CN", "mtap_del",
                 "PRMT5", "MAT2A", "CDKN2A", "KRAS", "ACTB", "kras_fort12"]].copy()
panc_out.index.name = "ModelID"
panc_out = panc_out.sort_values("MTAP_CN")
panc_out.to_csv("mtap_arbitration_840_pancreas_lines.csv")
log("CSV lignées écrit : mtap_arbitration_840_pancreas_lines.csv | lignes :", len(panc_out))

# ---------------------------------------------------------------- (b) écrans médicaments
LOOKUP = ["PRMT5", "MAT2A", "MTAP", "MTA", "GSK591", "EPZ015666", "GSK3326595",
          "PF-06939999", "AMG193", "AG-270", "VOPIMETOSTAT", "MRTX1719",
          "TNG908", "TNG462", "IDE397", "GSK3368715", "JNJ-64619178"]
def lookup_hits(name, target, moa):
    txt = " ".join(str(x) for x in [name, target, moa]).upper()
    return [k for k in LOOKUP if k in txt]

def screen_table(df_screen, value_col, id_col, label):
    """df_screen : colonnes [id, group_del(bool), value] ; retourne DataFrame par composé."""
    out = []
    for cid, g in df_screen.groupby(id_col):
        a = g.loc[g["mtap_del"] == True, value_col].dropna()
        b = g.loc[g["mtap_del"] == False, value_col].dropna()
        if len(a) >= 5 and len(b) >= 5:
            u, p = mannwhitneyu(a, b, alternative="two-sided")
            out.append({id_col: cid, "n_del": len(a), "n_int": len(b),
                        "med_del": float(a.median()), "med_int": float(b.median()),
                        "diff_med": float(a.median() - b.median()),
                        "U": float(u), "p": float(p)})
    res = pd.DataFrame(out)
    if len(res):
        res["fdr"] = bh(res["p"].values)
    return res

# --- B1 PRISM primaire 24Q2
log("--- (b1) PRISM primaire 24Q2, MTAP-délété vs intact (lignées pancréas) ---")
prim_meta = pd.read_csv(f"{DATA}/Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv")
prim_meta_panc = prim_meta[prim_meta["depmap_id"].isin(panc_ids)]
log("  lignées pancréas dans la méta PRISM primaire :", prim_meta_panc["depmap_id"].nunique(),
    "| lignes méta :", len(prim_meta_panc))
panc_ach = sorted(set(prim_meta_panc["depmap_id"].tolist()) & set(panc.index.tolist()))
log("  lignées pancréas communes avec DepMap CN/Chronos :", len(panc_ach),
    "| MTAP-délétées :", int(panc.loc[panc_ach, "mtap_del"].sum()),
    "| intactes :", int((~panc.loc[panc_ach, "mtap_del"]).sum()))
prim = pd.read_csv(f"{DATA}/Repurposing_Public_24Q2_Extended_Primary_Data_Matrix.csv",
                   index_col=0, usecols=["Unnamed: 0"] + panc_ach)
log("  matrice primaire lue :", prim.shape, "(composés x lignées pancréas)")
clist = pd.read_csv(f"{DATA}/Repurposing_Public_24Q2_Extended_Primary_Compound_List.csv")
log("  liste composés :", len(clist), "| IDs uniques :", clist["IDs"].nunique(),
    "| doublons d'IDs :", int(clist["IDs"].duplicated().sum()),
    "(1 : AZ-628 présent en REP.1M et REP.300 — dédupliqué, premier gardé, sinon le merge gonfle le comptage)")
clist = clist.drop_duplicates("IDs", keep="first")
log("  liste composés après dédup IDs :", len(clist))
clist = clist.set_index("IDs")
prim_long = prim.reset_index().rename(columns={"index": "BRD"}).melt(
    id_vars="BRD", var_name="ModelID", value_name="viab")
prim_long["mtap_del"] = prim_long["ModelID"].map(panc.set_index(panc.index)["mtap_del"].to_dict())
prim_long = prim_long.dropna(subset=["viab"])
res1 = screen_table(prim_long, "viab", "BRD", "prism_primary")
res1 = res1.merge(clist[["Drug.Name", "MOA", "repurposing_target"]], left_on="BRD",
                  right_index=True, how="left")
res1 = res1.rename(columns={"Drug.Name": "name", "repurposing_target": "target"})
res1["lookup"] = [lookup_hits(r["name"], r["target"], r["MOA"]) for _, r in res1.iterrows()]
res1 = res1.sort_values("p")
res1.to_csv("mtap_arbitration_840_prism_primary.csv", index=False)
log(f"  PRISM primaire : {len(res1)} composés testés (n>=5/5) ; FDR<0,05 : {int((res1['fdr'] < 0.05).sum())} ; "
    f"FDR min : {res1['fdr'].min():.3g}")
log("  top 10 par p :")
for _, r in res1.head(10).iterrows():
    log(f"    {r['name']} (BRD {str(r['BRD'])[:30]}…) MOA={r['MOA']} target={r['target']} "
        f"n={r['n_del']}/{r['n_int']} méd {r['med_del']:+.3f}/{r['med_int']:+.3f} "
        f"diff {r['diff_med']:+.3f} p={r['p']:.3g} FDR={r['fdr']:.3g}")
lh1 = res1[res1["lookup"].apply(len) > 0]
log(f"  composés ciblés PRMT5/MAT2A présents au primaire : {len(lh1)}")
for _, r in lh1.iterrows():
    log(f"    CIBLÉ {r['name']} target={r['target']} MOA={r['MOA']} hits={r['lookup']} "
        f"n={r['n_del']}/{r['n_int']} méd {r['med_del']:+.3f}/{r['med_int']:+.3f} "
        f"diff {r['diff_med']:+.3f} p={r['p']:.3g} FDR={r['fdr']:.3g}")
for key in ["PRMT5", "MAT2A"]:
    hit = clist[clist["repurposing_target"].astype(str).str.contains(key, na=False)
                 | clist["Drug.Name"].astype(str).str.contains(key, na=False)]
    log(f"  recherche '{key}' dans la liste complète des composés primaires : {len(hit)} ligne(s)")
    for _, r in hit.iterrows():
        log(f"    {r['Drug.Name']} | target={r['repurposing_target']} | MOA={r['MOA']}")

# --- B2 PRISM secondaire 19Q4
log("--- (b2) PRISM secondaire 19Q4, MTAP-délété vs intact (AUC) ---")
sec_chunks = []
for ch in pd.read_csv(f"{DATA}/secondary-screen-dose-response-curve-parameters.csv",
                      chunksize=100000,
                      usecols=["broad_id", "depmap_id", "screen_id", "auc", "name", "moa", "target"]):
    ch = ch[ch["depmap_id"].isin(panc_ach)]
    sec_chunks.append(ch)
sec = pd.concat(sec_chunks) if sec_chunks else pd.DataFrame()
log("  lignes secondaires, lignées pancréas communes :", len(sec),
    "| lignées :", sec["depmap_id"].nunique() if len(sec) else 0,
    "| MTAP-délétées :", int(panc.loc[[i for i in sec['depmap_id'].unique() if i in panc.index], "mtap_del"].sum()) if len(sec) else 0)
prio = {"MTS010": 0, "HTS002": 1, "MTS006": 2, "MTS005": 3}
sec["prio"] = sec["screen_id"].map(prio).fillna(9)
sec = sec.sort_values("prio").drop_duplicates(["broad_id", "depmap_id"], keep="first")
log("  après déduplication (broad_id, depmap_id), priorité MTS010>HTS002>MTS006>MTS005 :", len(sec), "lignes")
# Agrégation par NOM de composé et par lignée (médiane AUC) : 54 noms ont
# 2 broad_id (convention PROVENANCE_prism_secondary.md) — sans ça, un même
# nom compterait deux fois la même lignée dans le Mann-Whitney.
sec = sec.groupby(["name", "depmap_id"], as_index=False).agg(
    auc=("auc", "median"), moa=("moa", "first"), target=("target", "first"))
log("  après agrégation (nom, lignée), médiane AUC :", len(sec), "lignes")
sec["mtap_del"] = sec["depmap_id"].map(panc["mtap_del"].to_dict())
sec = sec.dropna(subset=["auc"])
res2 = screen_table(sec, "auc", "name", "prism_secondary")
# ré-attacher moa/target (premier non nul par nom)
mt = sec.groupby("name").agg(moa=("moa", "first"), target=("target", "first")).reset_index()
res2 = res2.merge(mt, on="name", how="left")
res2["lookup"] = [lookup_hits(r["name"], r["target"], r["moa"]) for _, r in res2.iterrows()]
res2 = res2.sort_values("p")
res2.to_csv("mtap_arbitration_840_prism_secondary.csv", index=False)
log(f"  PRISM secondaire : {len(res2)} composés testés (n>=5/5) ; FDR<0,05 : {int((res2['fdr'] < 0.05).sum())} ; "
    f"FDR min : {res2['fdr'].min():.3g}")
log("  top 10 par p (AUC, plus bas = plus sensible) :")
for _, r in res2.head(10).iterrows():
    log(f"    {r['name']} MOA={r['moa']} target={r['target']} n={r['n_del']}/{r['n_int']} "
        f"méd {r['med_del']:.3f}/{r['med_int']:.3f} diff {r['diff_med']:+.3f} p={r['p']:.3g} FDR={r['fdr']:.3g}")
lh2 = res2[res2["lookup"].apply(len) > 0]
log(f"  composés ciblés PRMT5/MAT2A présents au secondaire : {len(lh2)}")
for _, r in lh2.iterrows():
    log(f"    CIBLÉ {r['name']} target={r['target']} MOA={r['moa']} hits={r['lookup']} "
        f"n={r['n_del']}/{r['n_int']} méd {r['med_del']:.3f}/{r['med_int']:.3f} "
        f"diff {r['diff_med']:+.3f} p={r['p']:.3g} FDR={r['fdr']:.3g}")

# --- B3 GDSC2
log("--- (b3) GDSC2, MTAP-délété vs intact (LN_IC50 et AUC) ---")
gd = pd.read_excel(f"{DATA}/GDSC2_fitted_dose_response_27Oct23.xlsx", engine="openpyxl")
log("  GDSC2 lignes :", len(gd), "| colonnes", list(gd.columns))
gd["ModelID"] = gd["SANGER_MODEL_ID"].map(sanger2ach)
gd_panc = gd[gd["ModelID"].isin(panc_ach)].copy()
log("  lignes GDSC2, lignées pancréas communes :", len(gd_panc),
    "| lignées :", gd_panc["ModelID"].nunique(),
    "| médicaments :", gd_panc["DRUG_NAME"].nunique(),
    "| MTAP-délétées :", int(panc.loc[[i for i in gd_panc['ModelID'].unique()], "mtap_del"].sum()))
gd_panc["mtap_del"] = gd_panc["ModelID"].map(panc["mtap_del"].to_dict())
gd_panc = gd_panc.dropna(subset=["LN_IC50", "AUC"])
# Déduplication (médicament, lignée) par médiane : GDSC2 contient plusieurs
# courbes par paire (242 036 lignes pour 235 748 paires uniques) — sans ça,
# le Mann-Whitney compterait plusieurs fois la même lignée (n gonflé, ex.
# Acetalax n=16/22 pour 8 délétées seulement dans le run précédent).
n_avant = len(gd_panc)
gd_panc = gd_panc.groupby(["DRUG_NAME", "ModelID"], as_index=False).agg(
    LN_IC50=("LN_IC50", "median"), AUC=("AUC", "median"),
    PUTATIVE_TARGET=("PUTATIVE_TARGET", "first"), PATHWAY_NAME=("PATHWAY_NAME", "first"),
    mtap_del=("mtap_del", "first"))
log(f"  après agrégation (médicament, lignée), médianes : {len(gd_panc)} lignes (avant : {n_avant})")
res3a = screen_table(gd_panc, "LN_IC50", "DRUG_NAME", "gdsc_lnic50")
res3b = screen_table(gd_panc, "AUC", "DRUG_NAME", "gdsc_auc")
tgt = gd_panc.groupby("DRUG_NAME").agg(target=("PUTATIVE_TARGET", "first"),
                                       pathway=("PATHWAY_NAME", "first")).reset_index()
res3 = res3a.merge(res3b, on="DRUG_NAME", suffixes=("_lnic50", "_auc"), how="outer")
res3 = res3.merge(tgt, on="DRUG_NAME", how="left")
res3["lookup"] = [lookup_hits(r["DRUG_NAME"], r["target"], r["pathway"]) for _, r in res3.iterrows()]
res3 = res3.sort_values("p_lnic50")
res3.to_csv("mtap_arbitration_840_gdsc.csv", index=False)
log(f"  GDSC2 LN_IC50 : {len(res3a)} médicaments testés ; FDR<0,05 : {int((res3a['fdr'] < 0.05).sum())} ; "
    f"FDR min : {res3a['fdr'].min():.3g}")
log(f"  GDSC2 AUC : {len(res3b)} médicaments testés ; FDR<0,05 : {int((res3b['fdr'] < 0.05).sum())} ; "
    f"FDR min : {res3b['fdr'].min():.3g}")
log("  top 10 par p LN_IC50 :")
for _, r in res3.head(10).iterrows():
    log(f"    {r['DRUG_NAME']} target={r['target']} pathway={r['pathway']} "
        f"n={r['n_del_lnic50']}/{r['n_int_lnic50']} LN_IC50 méd {r['med_del_lnic50']:+.3f}/{r['med_int_lnic50']:+.3f} "
        f"diff {r['diff_med_lnic50']:+.3f} p={r['p_lnic50']:.3g} FDR={r['fdr_lnic50']:.3g} | "
        f"AUC diff {r['diff_med_auc']:+.3f} p={r['p_auc']:.3g} FDR={r['fdr_auc']:.3g}")
lh3 = res3[res3["lookup"].apply(len) > 0]
log(f"  médicaments ciblés PRMT5/MAT2A présents dans GDSC2 : {len(lh3)}")
for _, r in lh3.iterrows():
    log(f"    CIBLÉ {r['DRUG_NAME']} target={r['target']} pathway={r['pathway']} hits={r['lookup']} "
        f"LN_IC50 diff {r['diff_med_lnic50']:+.3f} p={r['p_lnic50']:.3g} FDR={r['fdr_lnic50']:.3g} | "
        f"AUC diff {r['diff_med_auc']:+.3f} p={r['p_auc']:.3g} FDR={r['fdr_auc']:.3g}")
for key in ["PRMT5", "MAT2A", "GSK591"]:
    hit = gd[gd["DRUG_NAME"].astype(str).str.contains(key, na=False)
             | gd["PUTATIVE_TARGET"].astype(str).str.contains(key, na=False)]
    log(f"  recherche '{key}' dans GDSC2 complet : {len(hit)} ligne(s)")
    for _, r in hit.drop_duplicates("DRUG_NAME").iterrows():
        log(f"    {r['DRUG_NAME']} | target={r['PUTATIVE_TARGET']} | pathway={r['PATHWAY_NAME']}")

# --- sorties récapitulatives
res = pd.DataFrame(rows)
res.to_csv("mtap_arbitration_840_results.csv", index=False)
log("CSV résultats écrit : mtap_arbitration_840_results.csv | lignes :", len(res))
for f in ["mtap_arbitration_840_results.csv", "mtap_arbitration_840_pancreas_lines.csv",
          "mtap_arbitration_840_prism_primary.csv", "mtap_arbitration_840_prism_secondary.csv",
          "mtap_arbitration_840_gdsc.csv", "mtap_arbitration_840.py"]:
    log("SHA", f, ":", sha(f))
log("durée : %.1f s" % (time.time() - T0))
log("=== FIN, exit 0 ===")
LOG.close()
