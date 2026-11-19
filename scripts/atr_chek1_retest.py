#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-test ATR/CHEK1 — la seule piste ouverte des 10 runs v6 immunitaire/PARP.
Protocole gelé (16 nov. 2026, avant les runs) :
- Source : Broad GDAC Firehose stddata 2016-01-28, PAAD, RSEM genes
  normalized — tarball déjà sur disque, MD5 vérifié
  b09569ce3f4721f514bc137bd109ac0a. Rien re-téléchargé.
- Patients : tumeurs primaires (code TCGA 01) : 178. log2(RSEM+1).
- Correction pureté (v3, identique à build_fluxes_tcga_v4.py) :
  score acineux = médiane des 11 gènes acineux de v1 ; score îlots =
  médiane de INS, GCG, PPY, SST ; régression linéaire de chaque gène sur
  [1, acineux, îlots] ; flux = résidus. Ordre = résidu KRAS croissant.
- Gènes testés (7, protocole) : BRCA2, ATR, CHEK1, RAD51, POLQ, PARP1,
  PARP2. Les 5 autres gènes de réparation du bras PARP (BRCA1, ATM,
  CHEK2, XRCC1, FANCD2) sont aussi mesurés (même code, complétude).
- Tests directs (mêmes conventions que parp_direct_tests.py) :
  rho = Spearman gène vs rang KRAS ; top12_sd = (moyenne 12 KRAS-forts -
  moyenne reste) / écart-type (ddof=0) ; recouvrement Q3 (attendu 3/12).
- Trois versions par gène :
  (a) BRUT, ordre KRAS brut — reproduction de parp_direct_tests.csv
      (contrôle de cohérence : doit matcher à l'identique).
  (b) RÉSIDUS pureté, ordre KRAS résidu — la hausse survit-elle à la
      correction de pureté ?
  (c) PROLIFÉRATION : score = médiane des résidus de MKI67, TOP2A,
      PCNA, CCNB1 ; résidus doubly-corrigés (gène résidu régressé sur le
      score), ordre KRAS résidu ; + Spearman partiel gène vs rang KRAS
      contrôlé sur le score (rangs régressés). Sensibilité : même calcul
      avec le score calculé sur les valeurs brutes.
- Nul : lignes permutées, graine 42, mêmes tests sur la version (b).
- Flux v6 : les 12 gènes de réparation en RÉSIDUS, ordre KRAS résidu,
  même ordre de colonnes que le bras PARP (PARP1 en premier = cible v6,
  comparabilité directe avec results_fast_parp) ->
  pdac_tcga_fluxes_atr.csv + nul.
Aucune donnée d'une autre expérience n'entre ici. Un négatif est un résultat.
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
TARBALL = f"{DATA}/tcga_paad_rsem.tar.gz"
TARBALL_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
SEED = 42

ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]
ISLET = ["INS", "GCG", "PPY", "SST"]
GENES7 = ["BRCA2", "ATR", "CHEK1", "RAD51", "POLQ", "PARP1", "PARP2"]
GENES12 = ["PARP1", "PARP2", "BRCA1", "BRCA2", "ATM", "ATR", "CHEK1",
           "CHEK2", "RAD51", "XRCC1", "POLQ", "FANCD2"]
PROLIF = ["MKI67", "TOP2A", "PCNA", "CCNB1"]


def sha(path):
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


def rankdata(a):
    return pd.Series(a).rank(method="average").to_numpy(dtype=float)


def partial_spearman(x, y, z):
    """Spearman partiel de x vs y contrôlé sur z (rangs régressés, Pearson)."""
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    X = np.column_stack([np.ones(len(z)), rz])
    bx, *_ = np.linalg.lstsq(X, rx, rcond=None)
    by, *_ = np.linalg.lstsq(X, ry, rcond=None)
    ex, ey = rx - X @ bx, ry - X @ by
    if ex.std() == 0 or ey.std() == 0:
        return np.nan, np.nan
    r = float(np.corrcoef(ex, ey)[0, 1])
    n = len(x)
    t = r * np.sqrt((n - 3) / max(1e-12, 1 - r * r))
    from scipy.stats import t as tdist
    p = float(2 * tdist.sf(abs(t), n - 3))
    return r, p


def direct_tests(values, order_idx, label, rows, txt, genes):
    """values : DataFrame gènes x patients (colonnes = patients).
    order_idx : liste des patients dans l'ordre KRAS croissant.
    Retourne les stats par gène (rho vs rang, top12 sd, Q3)."""
    n = len(order_idx)
    rank = np.arange(n)
    top12 = np.zeros(n, dtype=bool)
    top12[-12:] = True
    txt.append(f"--- {label} — n={n} ---")
    for gene in genes:
        v = values.loc[gene, order_idx].to_numpy(dtype=float)
        q3 = float(np.quantile(v, 0.75))
        rho, p = spearmanr(rank, v)
        ov12 = int((top12 & (v > q3)).sum())
        top12_sd = float((v[top12].mean() - v[~top12].mean()) / v.std(ddof=0))
        txt.append(f"{gene:6s}: rho {rho:+.3f} p={p:.2e} | top12 {top12_sd:+.2f} sd | "
                   f"KRAS-forts >Q3 : {ov12}/12 (attendu 3)")
        rows.append(dict(version=label, n=n, gene=gene, rho_kras=float(rho),
                         p_rho=float(p), top12_sd=top12_sd,
                         overlap_top12_q3=ov12))
    txt.append("")
    return rows


def main():
    assert md5(TARBALL) == TARBALL_MD5, "MD5 du tarball non conforme"
    with tarfile.open(TARBALL, "r:gz") as tf:
        member = [m for m in tf.getmembers() if m.name.endswith(".data.txt")][0]
        f = tf.extractfile(member)
        df = pd.read_csv(f, sep="\t", index_col=0, low_memory=False)
    df.index = df.index.to_series().str.split("|").str[0]
    df = df[~df.index.duplicated(keep="first")]
    cols = df.columns.to_series()
    tumor_cols = cols[cols.str[13:15] == "01"]
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    mat = mat[~mat.isna().any(axis=1)]
    logmat = np.log2(mat + 1.0)
    need = GENES12 + PROLIF + ["KRAS"] + ACINAR + ISLET
    missing = [g for g in need if g not in logmat.index]
    assert not missing, f"gènes absents de la matrice : {missing}"
    print(f"Matrice : {logmat.shape[0]} gènes x {logmat.shape[1]} tumeurs ; "
          f"tous les gènes requis présents ({len(need)}).")

    # ---- Correction pureté v3 (identique à v4) ----
    score_ac = logmat.loc[ACINAR].median(axis=0)
    score_is = logmat.loc[ISLET].median(axis=0)
    X = np.column_stack([np.ones(logmat.shape[1]), score_ac.values,
                         score_is.values])
    Y = logmat.values
    beta, *_ = np.linalg.lstsq(X, Y.T, rcond=None)
    resid = pd.DataFrame(Y - (X @ beta).T, index=logmat.index,
                         columns=logmat.columns)
    var_tot = pd.Series(Y.var(axis=1), index=logmat.index)
    var_res = pd.Series(resid.values.var(axis=1), index=logmat.index)
    with np.errstate(invalid="ignore", divide="ignore"):
        r2 = 1.0 - var_res / var_tot
    r2 = r2.where(var_tot > 0)
    print(f"Variance expliquée par pureté (médiane) : {float(np.nanmedian(r2.values)):.1%} ; "
          f"KRAS R² pureté = {float(r2.loc['KRAS']):.1%}")
    for g in GENES7 + PROLIF:
        print(f"  {g:6s} R² pureté = {float(r2.loc[g]):.1%}")

    # ---- Ordres ----
    kras_raw = logmat.loc["KRAS"].sort_values(ascending=True)
    order_raw = list(kras_raw.index)
    kras_res = resid.loc["KRAS"].sort_values(ascending=True)
    order_res = list(kras_res.index)
    n_common_top12 = len(set(order_raw[-12:]) & set(order_res[-12:]))
    print(f"Top12 KRAS brut vs résidu : {n_common_top12}/12 patients communs.")
    print(f"KRAS résidu : min={kras_res.min():+.3f} médiane={kras_res.median():+.3f} "
          f"max={kras_res.max():+.3f}")

    # ---- Score de prolifération ----
    # Primaire : médiane des RÉSIDUS des 4 gènes (espace corrigé pureté).
    prolif_res = resid.loc[PROLIF].median(axis=0)
    # Sensibilité : médiane des valeurs BRUTES.
    prolif_raw = logmat.loc[PROLIF].median(axis=0)
    print(f"Score prolifération (résidus) : min={prolif_res.min():+.2f} "
          f"médiane={prolif_res.median():+.2f} max={prolif_res.max():+.2f}")
    # Le score de prolifération suit-il KRAS ?
    rho_p_raw, p_p_raw = spearmanr(np.arange(178), prolif_raw.loc[order_raw].to_numpy())
    rho_p_res, p_p_res = spearmanr(np.arange(178), prolif_res.loc[order_res].to_numpy())
    print(f"Spearman score prolifération vs rang KRAS : brut {rho_p_raw:+.3f} "
          f"(p={p_p_raw:.2e}) ; résidus {rho_p_res:+.3f} (p={p_p_res:.2e})")
    print(f"Corrélation acineux-îlots : {np.corrcoef(score_ac, score_is)[0, 1]:+.3f} ; "
          f"prolif vs acineux {np.corrcoef(prolif_res, score_ac)[0, 1]:+.3f} ; "
          f"prolif vs îlots {np.corrcoef(prolif_res, score_is)[0, 1]:+.3f}")

    # ---- Doubly-corrected : chaque gène résidu régressé sur le score prolif ----
    Xp = np.column_stack([np.ones(178), prolif_res.values])
    Yp = resid.loc[GENES12].values  # 12 x 178, colonnes = patients (ordre matrice)
    bp, *_ = np.linalg.lstsq(Xp, Yp.T, rcond=None)
    resid2 = pd.DataFrame(Yp - (Xp @ bp).T, index=GENES12, columns=logmat.columns)
    # Sensibilité : score brut comme contrôle.
    Xp2 = np.column_stack([np.ones(178), prolif_raw.values])
    bp2, *_ = np.linalg.lstsq(Xp2, Yp.T, rcond=None)
    resid2_raw = pd.DataFrame(Yp - (Xp2 @ bp2).T, index=GENES12,
                              columns=logmat.columns)

    rows, txt = [], []
    txt.append("=== Re-test ATR/CHEK1 — TCGA-PAAD, 178 tumeurs ===")
    txt.append("Versions : (a) BRUT ordre KRAS brut [reproduction parp_direct_tests.csv] ;")
    txt.append("(b) RÉSIDUS pureté (v3) ordre KRAS résidu ;")
    txt.append("(c) DOUBLY-CORRIGÉ (résidus pureté régressés sur score prolifération), ordre KRAS résidu.")
    txt.append("Score prolifération = médiane de MKI67, TOP2A, PCNA, CCNB1.")
    txt.append("")

    # (a) reproduction du brut
    direct_tests(logmat, order_raw, "(a) BRUT", rows, txt, GENES12)
    # (b) résidus pureté
    direct_tests(resid, order_res, "(b) RÉSIDUS pureté", rows, txt, GENES12)
    # (c) doubly-corrigé
    direct_tests(resid2, order_res, "(c) DOUBLY-CORRIGÉ prolif (résidus)", rows, txt, GENES12)
    # sensibilité (c')
    direct_tests(resid2_raw, order_res, "(c') DOUBLY-CORRIGÉ prolif (brut)", rows, txt, GENES12)

    # ---- Nul (graine 42) sur la version (b) ----
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(178)
    resid_nul = resid.copy()
    # permuter les lignes des patients (ordre des colonnes) pour les 12 gènes
    resid_nul.loc[GENES12] = resid.loc[GENES12].to_numpy()[:, perm]
    order_nul = list(resid_nul.columns)  # ordre inchangé (KRAS résidu) mais valeurs permutées
    direct_tests(resid_nul, order_nul, "(b) NUL graine 42", rows, txt, GENES12)

    # ---- Spearman partiel : gène vs rang KRAS contrôlé sur prolif ----
    txt.append("--- Spearman partiel (gène vs rang KRAS | score prolifération) ---")
    txt.append("Rang KRAS = rang du résidu KRAS (ordre résidu).")
    for gene in GENES12:
        v_res = resid.loc[gene, order_res].to_numpy(dtype=float)
        r1, p1 = partial_spearman(v_res, np.arange(178), prolif_res.loc[order_res].to_numpy())
        r2p, p2p = partial_spearman(v_res, np.arange(178), prolif_raw.loc[order_res].to_numpy())
        # Corrélation du gène avec le score de prolifération (brut, ordre résidu)
        rp, pp = spearmanr(v_res, prolif_res.loc[order_res].to_numpy())
        txt.append(f"{gene:6s}: partiel (score résidus) {r1:+.3f} p={p1:.2e} | "
                   f"partiel (score brut) {r2p:+.3f} p={p2p:.2e} | "
                   f"rho gène-prolif {rp:+.3f} p={pp:.2e}")
        rows.append(dict(version="(c) PARTIEL prolif (résidus)", n=178, gene=gene,
                         rho_kras=float(r1), p_rho=float(p1), top12_sd=np.nan,
                         overlap_top12_q3=-1))
        rows.append(dict(version="(c) PARTIEL prolif (brut)", n=178, gene=gene,
                         rho_kras=float(r2p), p_rho=float(p2p), top12_sd=np.nan,
                         overlap_top12_q3=-1))
    txt.append("")

    # ---- Lecture : les 7 gènes du protocole, version par version ----
    txt.append("--- Lecture (7 gènes du protocole) ---")
    import collections
    by = collections.defaultdict(dict)
    for r in rows:
        if r["gene"] in GENES7 and r["version"] in (
                "(a) BRUT", "(b) RÉSIDUS pureté",
                "(c) DOUBLY-CORRIGÉ prolif (résidus)",
                "(c) PARTIEL prolif (résidus)"):
            by[r["gene"]][r["version"]] = r
    for g in GENES7:
        d = by[g]
        txt.append(f"{g}: brut rho {d['(a) BRUT']['rho_kras']:+.3f} "
                   f"(top12 {d['(a) BRUT']['top12_sd']:+.2f}) | résidus rho "
                   f"{d['(b) RÉSIDUS pureté']['rho_kras']:+.3f} "
                   f"(top12 {d['(b) RÉSIDUS pureté']['top12_sd']:+.2f}) | "
                   f"doubly rho {d['(c) DOUBLY-CORRIGÉ prolif (résidus)']['rho_kras']:+.3f} "
                   f"(top12 {d['(c) DOUBLY-CORRIGÉ prolif (résidus)']['top12_sd']:+.2f}) | "
                   f"partiel {d['(c) PARTIEL prolif (résidus)']['rho_kras']:+.3f}")
    n_sig = {v: sum(1 for r in rows if r["version"] == v and r["gene"] in GENES7
                    and r["p_rho"] < 0.05) for v in
             ["(a) BRUT", "(b) RÉSIDUS pureté",
              "(c) DOUBLY-CORRIGÉ prolif (résidus)"]}
    txt.append(f"Gènes (sur 7) avec p < 0,05 : brut {n_sig['(a) BRUT']}/7 ; "
               f"résidus {n_sig['(b) RÉSIDUS pureté']}/7 ; "
               f"doubly {n_sig['(c) DOUBLY-CORRIGÉ prolif (résidus)']}/7. "
               f"Seuil Bonferroni 7 tests : p < 0,0071 ; 12 tests : p < 0,0042.")

    out_csv = f"{OUT}/atr_chek1_direct_tests_tcga.csv"
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    out_txt = f"{OUT}/atr_chek1_direct_tests_tcga.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(txt) + "\n")
    print("\n".join(txt))
    print(f"Écrit : {out_csv} (SHA {sha(out_csv)[:12]}…) et {out_txt}")

    # ---- Flux v6 : 12 gènes de réparation en RÉSIDUS, ordre KRAS résidu ----
    flux = resid.loc[GENES12, order_res].T
    assert flux.isna().sum().sum() == 0
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_tcga_fluxes_atr.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes) "
          f"SHA {sha(out_path)[:12]}…")
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_tcga_fluxes_atr_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} SHA {sha(nul_path)[:12]}…")

    provenance = {
        "date": "2026-11-16",
        "mission": "Re-test ATR/CHEK1 : la hausse BRCA2/ATR/CHEK1/RAD51 "
                   "survit-elle à la pureté et à la prolifération ?",
        "source": "Broad GDAC Firehose 2016-01-28 PAAD, tarball déjà sur "
                  "disque, MD5 vérifié " + TARBALL_MD5,
        "patients": 178,
        "correction_pureté": "v3 identique à build_fluxes_tcga_v4.py "
                             "(scores acineux + îlots, régression, résidus)",
        "score_prolifération": "médiane de MKI67, TOP2A, PCNA, CCNB1 "
                               "(primaire : résidus ; sensibilité : brut)",
        "gènes_testés": GENES7,
        "gènes_complétude": GENES12,
        "ordre": "résidu KRAS croissant (versions b/c) ; KRAS brut pour (a)",
        "top12_commun_brut_résidu": int(n_common_top12),
        "spearman_prolif_vs_rang_kras": {
            "brut": round(float(rho_p_raw), 4), "p_brut": float(p_p_raw),
            "résidus": round(float(rho_p_res), 4), "p_résidus": float(p_p_res)},
        "r2_pureté": {g: round(float(r2.loc[g]), 4) for g in GENES7 + PROLIF},
        "fichiers": {
            "tests_csv": {"fichier": out_csv, "sha256": sha(out_csv)},
            "tests_txt": {"fichier": out_txt, "sha256": sha(out_txt)},
            "flux_csv": {"fichier": out_path, "sha256": sha(out_path)},
            "flux_nul_csv": {"fichier": nul_path, "sha256": sha(nul_path)},
        },
    }
    with open(f"{OUT}/atr_chek1_retest_provenance_tcga.json", "w",
              encoding="utf-8") as f:
        json.dump(provenance, f, indent=2, ensure_ascii=False)
    print("Provenance JSON écrite : atr_chek1_retest_provenance_tcga.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
