#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bras 1 — MTAP / PRMT5 et l'axe KRAS (test direct, PAS de run v6).
Protocole GELÉ avant les tests (16 nov. 2026, 14h40) :
- Cohorte : TCGA-PAAD, 178 tumeurs primaires (code TCGA 01), même matrice
  que v1 (Firehose stddata 2016-01-28, RSEM normalisé, log2(RSEM+1)).
- Axe KRAS : expression KRAS brute log2(RSEM+1), croissante. Groupe
  « KRAS-fort » = les 12 tumeurs à plus forte expression KRAS (même
  définition que les bras immunitaire / PARP / ATR-CHEK1).
- Test 1 (expression) : pour MTAP, PRMT5, CDKN2A — Spearman contre KRAS
  (rho + p) ; top-12 contre reste : différence en sd (convention du
  projet : (moyenne_top12 - moyenne_reste) / écart-type ddof=0), test
  de Welch (t + p), d de Cohen ; recouvrement Q3 (attendu 3/12 sous
  indépendance). Seuil Bonferroni 3 gènes : p < 0,0167.
  Sensibilité : mêmes tests sur les RÉSIDUS de pureté v3 (régression
  sur scores acineux + îlots) avec ordre KRAS résidu.
- Test 2 (délétion mesurée) : GISTIC2 Level 4 Firehose analyses
  2016-01-28, fichier all_thresholded.by_genes.txt (-2 = délétion
  profonde / homozygote, -1 = perte peu profonde / hétérozygote).
  Délétion MTAP = valeur -2. Prévalence sur les 178 tumeurs ;
  Fisher exact bilatéral : MTAP -2 parmi les 12 KRAS-forts contre
  le reste ; idem CDKN2A -2 ; idem perte quelconque (-2 ou -1).
  Robustesse : p de permutation (10 000 mélanges des 12 étiquettes
  KRAS-fort, graine 42) pour l'enrichissement MTAP -2.
  Contrôle de cohérence : expression MTAP médiane selon le statut
  GISTIC (-2 contre -1/0/1) — une délétion vraie doit abaisser
  l'expression ; ce n'est pas un verdict, c'est un contrôle qualité.
  Co-délétion MTAP/CDKN2A (locus 9p21) : tableau de contingence.
- Test 3 (contrôles) : Spearman MTAP contre PRMT5 (expression) ;
  Spearman MTAP contre score acineux et score îlots (pureté) ; R² de
  pureté (v3) pour MTAP, PRMT5, CDKN2A, KRAS.
- Faits déjà mesurés, CITÉS sans être réimportés comme verdicts :
  balayage CRISPR génome entier DepMap 24Q4, 47 lignées pancréas —
  dépendance Chronos contre KRAS : PRMT5 rho -0,189 (FDR 0,87),
  MTAP +0,071 (FDR 0,96), CDKN2A +0,161 (FDR 0,89) ; tous ns.
- Règles : aucune imputation (NaN = écarté et compté) ; un négatif
  est un résultat ; le proxy « MTAP bas » n'est utilisé QUE si le
  GISTIC est inaccessible — il ne l'est pas ici, donc aucun proxy.
Sorties : mtap_direct_tests.csv, mtap_direct_tests.txt,
  mtap_gistic_status.csv (statut par tumeur), PROVENANCE_mtap.md, mtap.md.
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, spearmanr, ttest_ind

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
EXPR_TARBALL = f"{DATA}/tcga_paad_rsem.tar.gz"
EXPR_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
GISTIC_TARBALL = f"{DATA}/tcga_paad_gistic.tar.gz"
GISTIC_MD5 = "816034f742e8f89ca8734ca2cf4404d5"
GISTIC_SHA256 = "6edc20f365d2f828bf5b4ef90a93f67344928d069cdd138eb946ed3275eed0ed"
GISTIC_MEMBER = ("gdac.broadinstitute.org_PAAD-TP.CopyNumber_Gistic2.Level_4."
                 "2016012800.0.0/all_thresholded.by_genes.txt")
GENES = ["MTAP", "PRMT5", "CDKN2A"]
ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]
ISLET = ["INS", "GCG", "PPY", "SST"]
N_TOP = 12
N_PERM = 10000
SEED = 42


def sha256(path):
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
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    sp = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    return float((a.mean() - b.mean()) / sp)


def main():
    assert md5(EXPR_TARBALL) == EXPR_MD5, "MD5 expression non conforme"
    assert md5(GISTIC_TARBALL) == GISTIC_MD5, "MD5 GISTIC non conforme"
    assert sha256(GISTIC_TARBALL) == GISTIC_SHA256, "SHA256 GISTIC non conforme"

    # ---------- Expression ----------
    with tarfile.open(EXPR_TARBALL, "r:gz") as tf:
        member = [m for m in tf.getmembers() if m.name.endswith(".data.txt")][0]
        df = pd.read_csv(tf.extractfile(member), sep="\t", index_col=0)
    df.index = df.index.to_series().str.split("|").str[0]
    df = df[~df.index.duplicated(keep="first")]
    cols = df.columns.to_series()
    tumor_cols = cols[cols.str[13:15] == "01"]
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    missing = [g for g in ["KRAS"] + GENES + ACINAR + ISLET if g not in mat.index]
    assert not missing, f"gènes absents de la matrice : {missing}"
    nan_genes = mat.isna().any(axis=1)
    mat = mat[~nan_genes]
    logmat = np.log2(mat + 1.0)
    n = logmat.shape[1]
    assert n == 178, f"n attendu 178, obtenu {n}"
    print(f"Expression : {logmat.shape[0]} gènes x {n} tumeurs primaires")

    # Scores de pureté v3 + résidus
    score_ac = logmat.loc[ACINAR].median(axis=0)
    score_is = logmat.loc[ISLET].median(axis=0)
    X = np.column_stack([np.ones(n), score_ac.values, score_is.values])
    Y = logmat.values
    beta, *_ = np.linalg.lstsq(X, Y.T, rcond=None)
    resid = pd.DataFrame(Y - (X @ beta).T, index=logmat.index,
                         columns=logmat.columns)
    var_tot = pd.Series(Y.var(axis=1), index=logmat.index)
    var_res = pd.Series(resid.values.var(axis=1), index=logmat.index)
    with np.errstate(invalid="ignore", divide="ignore"):
        r2 = 1.0 - var_res / var_tot
    r2 = r2.where(var_tot > 0)

    kras = logmat.loc["KRAS"]
    order_raw = kras.sort_values(ascending=True).index
    kras_res = resid.loc["KRAS"]
    order_res = kras_res.sort_values(ascending=True).index

    txt = []
    txt.append("=== Bras 1 — MTAP / PRMT5 et l'axe KRAS (tests directs, TCGA-PAAD) ===")
    txt.append("Cohorte : 178 tumeurs primaires, ARN brut log2(RSEM+1), Firehose 2016-01-28.")
    txt.append("Groupe KRAS-fort = 12 tumeurs à plus forte expression KRAS.")
    txt.append("top12_sd = (moyenne top12 - moyenne reste) / écart-type du gène (ddof=0).")
    txt.append("Seuil Bonferroni 3 gènes : p < 0,0167 (Spearman).")
    txt.append("")
    txt.append(f"KRAS log2(RSEM+1) : min={kras.min():.3f} médiane={kras.median():.3f} "
               f"max={kras.max():.3f}")
    txt.append(f"Score acineux : min={score_ac.min():.2f} médiane={score_ac.median():.2f} "
               f"max={score_ac.max():.2f} ; score îlots : min={score_is.min():.2f} "
               f"médiane={score_is.median():.2f} max={score_is.max():.2f}")
    txt.append("")

    rows = []
    for version, frame, order in [("brut", logmat, order_raw),
                                  ("résidus_pureté_v3", resid, order_res)]:
        top12 = np.zeros(n, dtype=bool)
        top12[-N_TOP:] = True  # order croissant : les 12 derniers = KRAS-forts
        txt.append(f"--- Test 1 — expression, version {version} (n={n}) ---")
        for gene in GENES:
            v = frame.loc[gene, order].values.astype(float)
            assert not np.isnan(v).any()
            rho, p = spearmanr(np.arange(n), v)
            q3 = np.quantile(v, 0.75)
            ov = int((top12 & (v > q3)).sum())
            sd = float((v[top12].mean() - v[~top12].mean()) / v.std(ddof=0))
            t, pw = ttest_ind(v[top12], v[~top12], equal_var=False)
            d = cohen_d(pd.Series(v[top12]), pd.Series(v[~top12]))
            txt.append(
                f"{gene:6s}: médiane {np.median(v):+.2f} | rho KRAS {rho:+.3f} "
                f"p={p:.4g} | top12 {sd:+.2f} sd | Welch t={t:+.2f} p={pw:.4g} | "
                f"d Cohen {d:+.2f} | KRAS-forts >Q3 : {ov}/12 (attendu 3)")
            rows.append(dict(version=version, test="expression_vs_KRAS",
                             gene=gene, n=n, median=float(np.median(v)),
                             rho_kras=float(rho), p_rho=float(p),
                             top12_sd=sd, welch_t=float(t), welch_p=float(pw),
                             cohen_d=d, overlap_top12_q3=ov))
        txt.append("")

    # ---------- Contrôles ----------
    txt.append("--- Test 3 — contrôles (expression brute, n=178) ---")
    ctrl = []
    for a, b, label in [
            ("MTAP", "PRMT5", "MTAP vs PRMT5"),
            ("MTAP", None, "MTAP vs score acineux"),
            ("MTAP", None, "MTAP vs score îlots"),
            ("PRMT5", None, "PRMT5 vs score acineux"),
            ("CDKN2A", None, "CDKN2A vs score acineux"),
            ("KRAS", None, "KRAS vs score acineux")]:
        if b is not None:
            rho, p = spearmanr(logmat.loc[a], logmat.loc[b])
            ctrl.append(dict(contrôle=label, rho=float(rho), p=float(p)))
        else:
            score = score_ac if "acineux" in label else score_is
            rho, p = spearmanr(logmat.loc[a], score)
            ctrl.append(dict(contrôle=label, rho=float(rho), p=float(p)))
        txt.append(f"{label:28s}: rho {rho:+.3f} p={p:.4g}")
    for g in ["MTAP", "PRMT5", "CDKN2A", "KRAS"]:
        txt.append(f"R² pureté (v3) {g:6s}: {r2.loc[g]:.1%}")
        ctrl.append(dict(contrôle=f"R2_pureté_{g}",
                         rho=float(r2.loc[g]), p=np.nan))
    txt.append("")

    # ---------- GISTIC ----------
    with tarfile.open(GISTIC_TARBALL, "r:gz") as tf:
        g = pd.read_csv(tf.extractfile(GISTIC_MEMBER), sep="\t")
    print(f"GISTIC all_thresholded.by_genes.txt : {g.shape[0]} gènes x "
          f"{g.shape[1] - 3} échantillons")
    g = g.set_index("Gene Symbol")
    for gene in ["MTAP", "CDKN2A"]:
        assert gene in g.index, f"{gene} absent du GISTIC"
    # Barcodes : échantillons tumoraux primaires (code 01) ; appariement
    # aux 178 tumeurs d'expression par le barcode échantillon (15 car.).
    gcols = pd.Series(g.columns)
    g_sample15 = gcols.str[:15]
    expr_sample15 = pd.Series(logmat.columns).str[:15]
    common = sorted(set(g_sample15) & set(expr_sample15))
    # Un échantillon GISTIC par tumeur d'expression ?
    g_map = {}
    for c in g.columns:
        s15 = c[:15]
        if s15 in set(expr_sample15):
            g_map.setdefault(s15, []).append(c)
    dup = {k: v for k, v in g_map.items() if len(v) > 1}
    print(f"Échantillons GISTIC appariés aux 178 tumeurs : {len(g_map)} "
          f"(doublons : {len(dup)})")
    # Ordre KRAS brut croissant ; top-12 = 12 derniers.
    order_list = list(order_raw)
    status = []
    for bc in order_list:
        s15 = bc[:15]
        gcol = g_map[s15][0] if s15 in g_map else None
        status.append(dict(barcode=bc, sample15=s15,
                           mtap_gistic=(int(g.loc["MTAP", gcol])
                                        if gcol else np.nan),
                           cdkn2a_gistic=(int(g.loc["CDKN2A", gcol])
                                          if gcol else np.nan)))
    st = pd.DataFrame(status)
    st["kras_fort"] = False
    st.loc[st.index[-N_TOP:], "kras_fort"] = True
    n_matched = int(st["mtap_gistic"].notna().sum())
    txt.append("--- Test 2 — délétion mesurée (GISTIC2, -2 = délétion profonde) ---")
    txt.append(f"Tumeurs appariées expression ↔ GISTIC : {n_matched}/178 "
               f"(échantillons GISTIC totaux : {g.shape[1] - 3}).")
    st.to_csv(f"{OUT}/mtap_gistic_status.csv", index=False)
    print(f"Écrit : mtap_gistic_status.csv ({len(st)} lignes)")

    def fisher_table(df, gene_col, deleted_value, label):
        d = df.dropna(subset=[gene_col])
        is_del = (d[gene_col] == deleted_value) if deleted_value != "any_loss" \
            else d[gene_col].isin([-2, -1])
        a = int((d["kras_fort"] & is_del).sum())
        b = int((d["kras_fort"] & ~is_del).sum())
        c = int((~d["kras_fort"] & is_del).sum())
        e = int((~d["kras_fort"] & ~is_del).sum())
        or_, p = fisher_exact([[a, b], [c, e]])
        txt.append(f"{label} : KRAS-forts {a}/{a + b} délétés ; reste {c}/{c + e} ; "
                   f"OR={or_:.2f} ; Fisher bilatéral p={p:.4g}")
        return dict(test=label, gene=gene_col, deleted_top12=a, n_top12=a + b,
                    deleted_rest=c, n_rest=c + e, odds_ratio=float(or_),
                    fisher_p=float(p), n_analysé=len(d))

    fish_rows = []
    for gene_col, gene in [("mtap_gistic", "MTAP"), ("cdkn2a_gistic", "CDKN2A")]:
        vc = st[gene_col].value_counts(dropna=False).sort_index()
        txt.append(f"{gene} GISTIC (n={n_matched}) : " +
                   ", ".join(f"{int(k)}:{int(v)}" for k, v in vc.items()
                             if pd.notna(k)) +
                   (f" ; NaN:{int(vc[vc.index.isna()].sum())}" if vc.index.isna().any() else ""))
        fish_rows.append(fisher_table(st, gene_col, -2,
                                      f"{gene} délétion profonde (-2)"))
        fish_rows.append(fisher_table(st, gene_col, "any_loss",
                                      f"{gene} perte quelconque (-2 ou -1)"))
    # Co-délétion MTAP / CDKN2A
    d = st.dropna(subset=["mtap_gistic", "cdkn2a_gistic"])
    both = int(((d["mtap_gistic"] == -2) & (d["cdkn2a_gistic"] == -2)).sum())
    mtap_only = int(((d["mtap_gistic"] == -2) & (d["cdkn2a_gistic"] != -2)).sum())
    cdk_only = int(((d["mtap_gistic"] != -2) & (d["cdkn2a_gistic"] == -2)).sum())
    neither = int(((d["mtap_gistic"] != -2) & (d["cdkn2a_gistic"] != -2)).sum())
    txt.append(f"Co-délétion 9p21 (n={len(d)}) : MTAP-2 & CDKN2A-2 : {both} ; "
               f"MTAP-2 seul : {mtap_only} ; CDKN2A-2 seul : {cdk_only} ; "
               f"aucun : {neither}")
    # Permutation : enrichissement MTAP -2 chez les KRAS-forts.
    # Urne = les 177 tumeurs appariées uniquement (la tumeur sans GISTIC
    # ne peut pas être tirée : elle n'a pas de statut de délétion).
    d_perm = st.dropna(subset=["mtap_gistic"])
    rng = np.random.default_rng(SEED)
    is_del = (d_perm["mtap_gistic"] == -2).values.astype(bool)
    obs = int(is_del[d_perm["kras_fort"].values].sum())
    n_del = int(is_del.sum())
    counts = np.zeros(N_PERM, dtype=int)
    idx = np.arange(len(d_perm))
    for i in range(N_PERM):
        counts[i] = is_del[rng.choice(idx, size=N_TOP, replace=False)].sum()
    p_perm = float((counts >= obs).mean())
    txt.append(f"Permutation MTAP -2 (10 000 mélanges, graine 42, urne n=177) : "
               f"observé {obs}/12 KRAS-forts délétés ; {n_del} délétés au total ; "
               f"p_perm = {p_perm:.4f} (P[≥{obs} | hasard])")
    fish_rows.append(dict(test="permutation_MTAP_-2", gene="MTAP",
                          deleted_top12=obs, n_top12=N_TOP,
                          deleted_rest=n_del - obs, n_rest=len(d_perm) - N_TOP,
                          odds_ratio=np.nan, fisher_p=p_perm,
                          n_analysé=len(d_perm)))
    # Contrôle qualité : expression MTAP selon statut GISTIC
    expr = logmat.loc["MTAP"]
    st["mtap_expr"] = [expr[bc] for bc in st["barcode"]]
    txt.append("--- Contrôle qualité : expression MTAP selon statut GISTIC ---")
    for val in sorted(st["mtap_gistic"].dropna().unique()):
        sub = st[st["mtap_gistic"] == val]["mtap_expr"]
        txt.append(f"MTAP GISTIC {int(val):+d} : n={len(sub)} ; "
                   f"expression médiane {sub.median():.2f} "
                   f"(min {sub.min():.2f}, max {sub.max():.2f})")
    txt.append("")

    # ---------- Écritures ----------
    rows_all = rows + [dict(version="GISTIC", test=r["test"], gene=r["gene"],
                            n=r["n_analysé"], median=np.nan,
                            rho_kras=np.nan, p_rho=np.nan, top12_sd=np.nan,
                            welch_t=np.nan, welch_p=np.nan, cohen_d=np.nan,
                            overlap_top12_q3=np.nan,
                            deleted_top12=r["deleted_top12"],
                            n_top12=r["n_top12"],
                            deleted_rest=r["deleted_rest"],
                            n_rest=r["n_rest"],
                            odds_ratio=r["odds_ratio"],
                            fisher_p=r["fisher_p"]) for r in fish_rows]
    pd.DataFrame(rows_all).to_csv(f"{OUT}/mtap_direct_tests.csv", index=False)
    pd.DataFrame(ctrl).to_csv(f"{OUT}/mtap_controls.csv", index=False)
    txt_out = "\n".join(txt) + "\n"
    with open(f"{OUT}/mtap_direct_tests.txt", "w", encoding="utf-8") as f:
        f.write(txt_out)
    print(txt_out)
    print(f"Écrit : mtap_direct_tests.csv, mtap_controls.csv, mtap_direct_tests.txt")

    provenance = {
        "date": "2026-11-16",
        "bras": "Bras 1 — MTAP / PRMT5 et l'axe KRAS (test direct, pas de run v6)",
        "script": "mtap_kras_tests.py",
        "expression": {
            "dépôt": "Broad GDAC Firehose stddata 2016-01-28, PAAD",
            "fichier": "gdac.broadinstitute.org_PAAD.Merge_rnaseqv2__illuminahiseq_"
                       "rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data."
                       "Level_3.2016012800.0.0.tar.gz",
            "md5_vérifié": EXPR_MD5,
            "patients": "178 tumeurs primaires (code TCGA 01)",
            "transformation": "log2(RSEM normalisé + 1)",
            "gènes_écartés_NaN": int(nan_genes.sum()),
        },
        "copy_number": {
            "dépôt": "Broad GDAC Firehose analyses 2016-01-28, PAAD",
            "fichier": "gdac.broadinstitute.org_PAAD-TP.CopyNumber_Gistic2.Level_4."
                       "2016012800.0.0.tar.gz",
            "url": "https://gdac.broadinstitute.org/runs/analyses__2016_01_28/"
                   "data/PAAD/20160128/",
            "taille_octets": 26189717,
            "md5_vérifié": GISTIC_MD5,
            "sha256_vérifié": GISTIC_SHA256,
            "fichier_interne": GISTIC_MEMBER,
            "matrice": f"{g.shape[0]} gènes x {g.shape[1] - 3} échantillons",
            "définition": "GISTIC2 all_thresholded.by_genes.txt : -2 = délétion "
                          "profonde (homozygote), -1 = perte peu profonde "
                          "(hétérozygote), 0 = diploïde, +1/+2 = gains",
            "tumeurs_appariées_expression": n_matched,
            "échantillons_gistic_totaux": int(g.shape[1] - 3),
        },
        "définitions": {
            "axe_KRAS": "expression KRAS brute log2(RSEM+1) croissante",
            "KRAS_fort": "12 tumeurs à plus forte expression KRAS",
            "top12_sd": "(moyenne top12 - moyenne reste) / écart-type (ddof=0)",
            "seuil_Bonferroni": "p < 0,0167 (3 gènes, Spearman)",
            "permutation": "10 000 mélanges des 12 étiquettes KRAS-fort, graine 42",
            "correction_pureté_v3": "régression par gène sur [1, score acineux, "
                                    "score îlots] ; résidus (même définition que "
                                    "build_fluxes_tcga_v3.py)",
        },
        "faits_cités_sans_réimport": {
            "source": "balayage CRISPR génome entier DepMap 24Q4, 47 lignées "
                      "pancréas (PROVENANCE_crispr_scan.md)",
            "dépendance_Chronos_contre_KRAS": {
                "PRMT5": "rho -0,189 (FDR 0,87)",
                "MTAP": "rho +0,071 (FDR 0,96)",
                "CDKN2A": "rho +0,161 (FDR 0,89)",
            },
            "note": "tous non significatifs ; cités comme contexte, pas comme "
                    "verdicts de ce bras",
        },
        "contexte_clinique_cité": {
            "combinaison": "vopimetostat (inhibiteur PRMT5) + daraxonrasib",
            "résultat": "82 % de réponses chez les patients MTAP-délétés, "
                        "phase 1/2 NCT06922591, ESMO 2026",
            "note": "résultat clinique externe, vérifié par le bras "
                    "combinaisons ; pas une prédiction du pipeline",
        },
        "sorties": {
            "mtap_direct_tests.csv": sha256(f"{OUT}/mtap_direct_tests.csv"),
            "mtap_controls.csv": sha256(f"{OUT}/mtap_controls.csv"),
            "mtap_gistic_status.csv": sha256(f"{OUT}/mtap_gistic_status.csv"),
            "mtap_direct_tests.txt": sha256(f"{OUT}/mtap_direct_tests.txt"),
        },
        "règle": "Aucune imputation ; aucun proxy « MTAP bas » utilisé "
                 "(le GISTIC mesuré était accessible) ; un négatif est un "
                 "résultat ; données du jour uniquement pour les verdicts.",
    }
    with open(f"{OUT}/PROVENANCE_mtap.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — Bras 1 : MTAP / PRMT5 et l'axe KRAS (TCGA-PAAD)\n\n")
        f.write("```json\n" + json.dumps(provenance, indent=2,
                                          ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_mtap.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
