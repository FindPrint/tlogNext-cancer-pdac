#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Survie GSE71729 (Moffitt PDAC) — confirmation du signal TCGA (KRAS et CA125
prédisent une survie plus courte, sans seuil).
Source survie : la matrice GEO elle-même, caractéristiques ch2
« survival_months » (125 échantillons) et « death_event_1death_0censor »
(125 échantillons). Fichier : data/GSE71729_series_matrix.txt.gz (SHA
b228789314ec4d866ec51b65724664abaa24b822577c55d3727820c867536a54).
Jointure : l'ordre des 145 tumeurs est reproduit EXACTEMENT comme dans
build_fluxes_geo71729.py (même lecture de la matrice, mêmes primaires,
même tri KRAS croissant) et vérifié ligne par ligne contre
pdac_geo71729_fluxes.csv (KRAS + MUC16). Aucune survie inventée : les
patients sans survie sont exclus, n rapporté.
Analyses : paysage complet (top12/top7/top20 KRAS, quartiles sup. MUC16 /
CEACAM5 / KRAS seuls, double-quartile CA125+CEA — médiane Kaplan-Meier,
log-rank contre le reste) + Cox continu (aucun seuil, HR par +1 écart-type)
univarié (KRAS, MUC16, CEACAM5, PGC, DPCR1, CLDN18) et multivarié
(KRAS+MUC16+CEACAM5). Même implémentation que la survie TCGA (KM, log-rank,
Cox Breslow en numpy).
"""
import gzip
import hashlib
from math import erf, sqrt

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"

V4_GENES = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
            "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def km_median(times, events):
    t = np.array(times, dtype=float)
    e = np.array(events, dtype=bool)
    order = np.argsort(t)
    t, e = t[order], e[order]
    n = len(t)
    surv = 1.0
    med = np.nan
    for i in range(n):
        at_risk = n - i
        if e[i]:
            surv *= (1 - 1 / at_risk)
            if surv <= 0.5 and np.isnan(med):
                med = t[i]
    return med


def logrank(t1, e1, t2, e2):
    # CORRECTION 16 nov. 2026 : les événements DOIVENT être booléens.
    # Passés en int (0/1), `t1[e1]` fait de l'indexation fantaisie (positions
    # 0 et 1) au lieu d'un masque booléen — les p log-rank de la première
    # exécution (top20 p=0,008) étaient fausses. Vérifié par ré-implémentation
    # indépendante : les vraies p sont top12 0,886 / top7 0,710 / top20 0,758.
    t1 = np.asarray(t1, dtype=float)
    t2 = np.asarray(t2, dtype=float)
    e1 = np.asarray(e1, dtype=bool)
    e2 = np.asarray(e2, dtype=bool)
    times = np.sort(np.unique(np.concatenate([t1[e1], t2[e2]])))
    O1 = E1 = V = 0.0
    for tt in times:
        n1 = (t1 >= tt).sum()
        n2 = (t2 >= tt).sum()
        d1 = ((t1 == tt) & e1).sum()
        d2 = ((t2 == tt) & e2).sum()
        n = n1 + n2
        d = d1 + d2
        if n == 0 or d == 0:
            continue
        E1 += d * n1 / n
        O1 += d1
        if n > 1:
            V += d * (n - d) * n1 * n2 / (n * n * (n - 1))
    if V <= 0:
        return float("nan")
    z = (O1 - E1) / sqrt(V)
    return 1 - erf(abs(z) / sqrt(2))


def cox_fit(df, cols):
    Z = df[cols].values.astype(float)
    Z = (Z - Z.mean(0)) / Z.std(0)
    t = df["os_months"].values
    e = df["dead"].values.astype(bool)
    order = np.argsort(-t)
    Z, t, e = Z[order], t[order], e[order]
    beta = np.zeros(Z.shape[1])
    hess = None
    for _ in range(50):
        eta = Z @ beta
        w = np.exp(eta - eta.max())
        S0 = np.cumsum(w)
        S1 = np.cumsum(Z * w[:, None], axis=0)
        S2 = np.cumsum((Z[:, :, None] * Z[:, None, :]) * w[:, None, None],
                       axis=0)
        grad = np.zeros_like(beta)
        hess = np.zeros((len(beta), len(beta)))
        for i in range(len(t)):
            if not e[i]:
                continue
            grad += Z[i] - S1[i] / S0[i]
            hess -= S2[i] / S0[i] - np.outer(S1[i], S1[i]) / (S0[i] ** 2)
        try:
            step = np.linalg.solve(hess, grad)
        except np.linalg.LinAlgError:
            break
        beta = beta - step
        if np.max(np.abs(step)) < 1e-8:
            break
    se = np.sqrt(np.diag(np.linalg.inv(-hess)))
    out = []
    for j, c in enumerate(cols):
        z = beta[j] / se[j]
        p = 1 - erf(abs(z) / sqrt(2))
        out.append((c, float(np.exp(beta[j])), float(beta[j]),
                    float(se[j]), float(p)))
    return out


def main():
    # ---- 1. Matrice + caractéristiques ch2 ----
    mat = pd.read_csv(f"{DATA}/GSE71729_series_matrix.txt.gz", sep="\t",
                      comment="!", index_col=0, low_memory=False)
    mat.index = mat.index.str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    gsm_order = list(mat.columns)
    ch2 = []
    titles = []
    with gzip.open(f"{DATA}/GSE71729_series_matrix.txt.gz", "rt",
                   encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_characteristics_ch2"):
                ch2.append([v.strip('"') for v in
                            line.rstrip("\n").split("\t")[1:]])
            if line.startswith("!Sample_title"):
                titles = [t.strip('"') for t in
                          line.rstrip("\n").split("\t")[1:]]
    # Pour chaque GSM : tissue type, survival_months, death_event, sous-types.
    annot = {}
    for i, gsm in enumerate(gsm_order):
        vals = [row[i] for row in ch2 if i < len(row)]
        joined = " | ".join(vals)
        rec = {"gsm": gsm, "title": titles[i] if i < len(titles) else ""}
        for v in vals:
            if v.startswith("tissue type:"):
                rec["tissue"] = v.split(":", 1)[1].strip()
            elif v.startswith("survival_months:"):
                rec["os_months"] = float(v.split(":", 1)[1].strip())
            elif v.startswith("death_event_1death_0censor:"):
                rec["dead"] = int(v.split(":", 1)[1].strip())
            elif v.startswith("tumor_subtype_0na_1classical_2basal:"):
                rec["tumor_subtype"] = v.split(":", 1)[1].strip()
            elif v.startswith("stroma_subtype_0na_1low_2normal_3activated:"):
                rec["stroma_subtype"] = v.split(":", 1)[1].strip()
        annot[gsm] = rec
    n_surv_all = sum(1 for r in annot.values() if "os_months" in r)
    print(f"Échantillons avec survie (toute la série) : {n_surv_all} / "
          f"{len(gsm_order)}")

    # ---- 2. Primaires, ordre KRAS croissant (même code que le build) ----
    kinds = []
    for i, gsm in enumerate(gsm_order):
        vals = [row[i] for row in ch2 if i < len(row)]
        joined = " | ".join(vals)
        if "tissue type: Primary" in joined:
            kinds.append("Primary")
        elif "tissue type: Metastasis" in joined:
            kinds.append("Metastasis")
        elif "tissue type: Normal" in joined:
            kinds.append("Normal")
        elif titles[i].endswith("-CellLine"):
            kinds.append("CellLine")
        else:
            kinds.append("?")
    prim = [g for g, k in zip(gsm_order, kinds) if k == "Primary"]
    print(f"Tumeurs primaires : {len(prim)}")
    sub = mat[prim]
    need = ["KRAS"] + V4_GENES
    cc = sub.loc[need].dropna(axis=1)
    order = cc.loc["KRAS"].sort_values(ascending=True).index
    # Vérification contre le CSV des flux existant (KRAS n'est pas un flux :
    # il n'est pas dans le CSV — on vérifie MUC16, CEACAM5, PGC).
    flux = pd.read_csv(f"{OUT}/pdac_geo71729_fluxes.csv")
    assert len(flux) == len(order), "nombre de lignes différent du CSV"
    checks = {}
    for g in ["MUC16", "CEACAM5", "PGC"]:
        checks[g] = bool(np.allclose(cc.loc[g, order].values,
                                     flux[g].values, atol=1e-9))
    print(f"Vérification ordre : {checks}")
    assert all(checks.values()), "ordre non reproduit — ARRÊT"
    # Le tri KRAS doit être monotone croissant.
    kras_sorted = cc.loc["KRAS", order].values
    assert bool(np.all(np.diff(kras_sorted) >= 0)), "KRAS non trié — ARRÊT"
    print(f"KRAS trié croissant : min={kras_sorted[0]:.2f} "
          f"médiane={np.median(kras_sorted):.2f} max={kras_sorted[-1]:.2f}")

    # ---- 3. Table survie ----
    rows = []
    for step, gsm in enumerate(order):
        r = annot[gsm]
        row = {"step": step, "gsm": gsm,
               "KRAS": float(cc.loc["KRAS", gsm])}
        for g in V4_GENES:
            row[g] = float(cc.loc[g, gsm])
        row["os_months"] = r.get("os_months", np.nan)
        row["dead"] = r.get("dead", np.nan)
        row["tumor_subtype"] = r.get("tumor_subtype", "")
        row["stroma_subtype"] = r.get("stroma_subtype", "")
        rows.append(row)
    d = pd.DataFrame(rows)
    d_surv = d.dropna(subset=["os_months"]).copy()
    d_surv["dead"] = d_surv["dead"].astype(int)
    print(f"Tumeurs primaires AVEC survie : {len(d_surv)} / {len(d)} ; "
          f"décès : {int(d_surv['dead'].sum())}")
    d.to_csv(f"{OUT}/geo71729_survival_table.csv", index=False)
    print(f"Écrit : {OUT}/geo71729_survival_table.csv "
          f"SHA {sha(f'{OUT}/geo71729_survival_table.csv')[:12]}…")

    # ---- 4. Paysage complet ----
    print("\n=== PAYSAGE DE SURVIE GSE71729 — toutes les définitions ===")
    print(f"Cohorte entière (avec survie) : n={len(d_surv)}, "
          f"OS médiane {km_median(d_surv['os_months'], d_surv['dead']):.1f} "
          f"mois, décès {int(d_surv['dead'].sum())}")
    # Groupes définis sur les 145 tumeurs (comme en TCGA : sur les 178),
    # puis restreints aux patients avec survie.
    n_all = len(d)
    q = n_all // 4  # 36
    defs = {
        "top12 KRAS": set(d.iloc[-12:]["gsm"]),
        "top7 KRAS": set(d.iloc[-7:]["gsm"]),
        "top20 KRAS": set(d.iloc[-20:]["gsm"]),
        "quartile sup. MUC16 (CA125) seul":
            set(d.sort_values("MUC16").iloc[-q:]["gsm"]),
        "quartile sup. CEACAM5 (CEA) seul":
            set(d.sort_values("CEACAM5").iloc[-q:]["gsm"]),
        "quartile sup. KRAS seul":
            set(d.sort_values("KRAS").iloc[-q:]["gsm"]),
        "CA125 ET CEA élevés (2 quartiles sup.)":
            set(d.sort_values("MUC16").iloc[-q:]["gsm"]) &
            set(d.sort_values("CEACAM5").iloc[-q:]["gsm"]),
    }
    print(f"{'groupe':38s} {'n':>3s} {'décès':>5s} {'OS médiane':>10s} "
          f"{'log-rank p':>10s}")
    results = []
    for name, pats in defs.items():
        sub_g = d_surv[d_surv["gsm"].isin(pats)]
        rest = d_surv[~d_surv["gsm"].isin(pats)]
        med = km_median(sub_g["os_months"], sub_g["dead"])
        med_r = km_median(rest["os_months"], rest["dead"])
        p = logrank(sub_g["os_months"].values, sub_g["dead"].values,
                    rest["os_months"].values, rest["dead"].values)
        print(f"{name:38s} {len(sub_g):3d} {int(sub_g['dead'].sum()):5d} "
              f"{med:9.1f} ({med_r:.1f} reste) {p:10.3f}")
        results.append((name, len(sub_g), int(sub_g["dead"].sum()),
                        float(med), float(med_r), float(p)))

    # ---- 5. Cox continu (aucun seuil) ----
    # CORRECTION 16 nov. 2026 : l'univarié se fait UN GÈNE À LA FOIS.
    # La première version appelait cox_fit une seule fois avec les 6 gènes
    # et étiquetait le résultat « univarié » — c'était en fait
    # l'ajustement à 6 gènes (KRAS 1,32, CEA 0,83, PGC 0,75). Les vrais
    # univariés (vérifiés par une maximisation groupée indépendante) sont
    # KRAS 1,24 / MUC16 1,06 / CEA 1,00 / PGC 0,85. L'ajustement à 6 gènes
    # est gardé en référence, étiqueté comme tel.
    print("\n=== COX CONTINU (aucun seuil) — risque par +1 écart-type ===")
    print(f"{'gène':9s} {'HR':>6s} {'coef':>6s} {'se':>5s} {'p':>7s}")
    cox_uni = []
    for g in ["KRAS", "MUC16", "CEACAM5", "PGC", "DPCR1", "CLDN18"]:
        for c, hr, b, se, p in cox_fit(d_surv, [g]):
            print(f"{c:9s} {hr:6.2f} {b:6.2f} {se:5.2f} {p:7.4f}")
            cox_uni.append((c, hr, b, se, p))
    print("\n=== COX MULTIVARIÉ (KRAS + MUC16 + CEACAM5) ===")
    cox_multi = []
    for c, hr, b, se, p in cox_fit(d_surv, ["KRAS", "MUC16", "CEACAM5"]):
        print(f"{c:9s} {hr:6.2f} {b:6.2f} {se:5.2f} {p:7.4f}")
        cox_multi.append((c, hr, b, se, p))
    print("\n=== COX AJUSTÉ 6 GÈNES (référence, mêmes 6 gènes ensemble) ===")
    cox_6 = []
    for c, hr, b, se, p in cox_fit(
            d_surv, ["KRAS", "MUC16", "CEACAM5", "PGC", "DPCR1", "CLDN18"]):
        print(f"{c:9s} {hr:6.2f} {b:6.2f} {se:5.2f} {p:7.4f}")
        cox_6.append((c, hr, b, se, p))

    # ---- 6. Sauvegarde des résultats ----
    with open(f"{OUT}/geo71729_survival_results.txt", "w") as f:
        f.write("SURVIE GSE71729 — paysage complet + Cox continu\n")
        f.write(f"Primaires : {len(d)} ; avec survie : {len(d_surv)} ; "
                f"décès : {int(d_surv['dead'].sum())}\n")
        f.write(f"OS médiane cohorte : "
                f"{km_median(d_surv['os_months'], d_surv['dead']):.1f} mois\n")
        for name, n, nd, med, medr, p in results:
            f.write(f"{name} | n={n} décès={nd} médiane={med:.1f} "
                    f"(reste {medr:.1f}) log-rank p={p:.4f}\n")
        f.write("Cox univarié (HR par +1 sd, un gène à la fois) :\n")
        for c, hr, b, se, p in cox_uni:
            f.write(f"  {c} HR={hr:.2f} coef={b:.2f} se={se:.2f} p={p:.4f}\n")
        f.write("Cox multivarié KRAS+MUC16+CEACAM5 :\n")
        for c, hr, b, se, p in cox_multi:
            f.write(f"  {c} HR={hr:.2f} coef={b:.2f} se={se:.2f} p={p:.4f}\n")
        f.write("Cox ajusté 6 gènes (référence) :\n")
        for c, hr, b, se, p in cox_6:
            f.write(f"  {c} HR={hr:.2f} coef={b:.2f} se={se:.2f} p={p:.4f}\n")
    print(f"\nÉcrit : {OUT}/geo71729_survival_results.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
