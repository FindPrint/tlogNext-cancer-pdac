#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Étape 4 (a) + (b) — vérifications et tests directs (18 nov. 2026).
Protocole gelé : PROTOCOL_enrichissements_833.md (écrit avant ce script).

(a) Allèles KRAS : comptages sur data/kras_alleles_pancreas.csv (54 lignées)
    et sur la table de mutations (45 lignées DepMap). Règle gelée : n < 40
    pour chaque allèle => série v6.1 IMPOSSIBLE (minimum fast 40).
    Tests directs : Chronos KRAS / PRMT5 par allèle (G12D vs G12V),
    viabilité MRTX1133 par allèle (recalculée aujourd'hui depuis
    data/mrtx1133_prism_kras_allele.csv, §8.20 comme référence seulement).
(b) Jointure MAF : revérification en relançant build_mutation_table_pancreas.py
    et en comparant le SHA de sortie au SHA consigné le 18 nov.
    (f3fa2bd2...). Tests directs : Chronos KRAS / PRMT5 / ATR selon
    TP53 (38/7), SMAD4 (11/34), CDKN2A (12/33) — Mann-Whitney bilatéral
    + d de Cohen + médianes. Confondant MTAP pour PRMT5 : CN MTAP par
    lignée (OmicsCNGene.csv), distribution par groupe mutationnel et
    Spearman PRMT5 ~ CN MTAP dans chaque groupe.
AUCUN run pipeline dans ce script. AUCUN verdict importé d'autres jours :
tout est recalculé ici.
"""
import hashlib
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr

BASE = "/home/hatch/workspace/runs/pdac-v6"
DATA = f"{BASE}/data"
OUT = open(f"{BASE}/verify_alleles_mutations.txt", "w", encoding="utf-8")


def log(*a):
    print(*a)
    print(*a, file=OUT)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cohen_d(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    nx, ny = len(x), len(y)
    sp = np.sqrt(((nx - 1) * x.var(ddof=1) + (ny - 1) * y.var(ddof=1)) / (nx + ny - 2))
    return float((x.mean() - y.mean()) / sp) if sp > 0 else float("nan")


def mw(x, y, label):
    x, y = np.asarray(x, float), np.asarray(y, float)
    x, y = x[~np.isnan(x)], y[~np.isnan(y)]
    u, p = mannwhitneyu(x, y, alternative="two-sided")
    log(f"  {label} : n={len(x)} vs {len(y)} | médianes {np.median(x):+.3f} vs "
        f"{np.median(y):+.3f} | moyennes {x.mean():+.3f} vs {y.mean():+.3f} | "
        f"d de Cohen {cohen_d(x, y):+.2f} | Mann-Whitney p={p:.3g}")
    return p


def main():
    log("=== Étape 4 (a) + (b) — 18 nov. 2026 ===")
    log(f"SHA kras_alleles_pancreas.csv : {sha(f'{DATA}/kras_alleles_pancreas.csv')}")
    log(f"SHA mutation_table_pancreas.csv (avant revérification) : "
        f"{sha(f'{DATA}/mutation_table_pancreas.csv')}")

    # --- (a) comptages allèles, fichier 54 lignées ---
    k54 = pd.read_csv(f"{DATA}/kras_alleles_pancreas.csv")
    log(f"\n(a) kras_alleles_pancreas.csv : {len(k54)} lignées")
    for allele, n in k54["Protein_Change"].value_counts().items():
        log(f"  {allele} : {n}")
    log(f"  MAX par allèle : {k54['Protein_Change'].value_counts().max()} "
        f"(minimum fast v6.1 = 40) => série v6.1 par allèle IMPOSSIBLE")

    # --- (b) revérification de la jointure : relancer le constructeur ---
    log("\n(b) Revérification de la jointure PR->ACH : relance de "
        "build_mutation_table_pancreas.py")
    r = subprocess.run([sys.executable, f"{BASE}/build_mutation_table_pancreas.py"],
                       capture_output=True, text=True, cwd=BASE)
    log(f"  exit constructeur : {r.returncode}")
    log(f"  sortie constructeur (dernières lignes) :")
    for line in (r.stdout.strip().splitlines() or ["(vide)"])[-6:]:
        log(f"    {line}")
    sha_after = sha(f"{DATA}/mutation_table_pancreas.csv")
    sha_expected = "f3fa2bd2ddafdec83795211cd45de19ce88de674a2d660f47a5e72d813063f36"
    log(f"  SHA après relance : {sha_after}")
    log(f"  SHA attendu (18 nov.) : {sha_expected}")
    log(f"  JOINTURE REPRODUITE À L'IDENTIQUE : {sha_after == sha_expected}")

    mut = pd.read_csv(f"{DATA}/mutation_table_pancreas.csv", comment="#")
    log(f"\n  Table mutations : {len(mut)} lignées")
    for g in ["TP53_mut", "SMAD4_mut", "CDKN2A_mut", "KRAS_mut"]:
        log(f"  {g} : {int(mut[g].sum())}/{len(mut)}")
    log("  Allèles KRAS dans les 45 :")
    for allele, n in mut["KRAS_allele"].value_counts().items():
        log(f"    {allele} : {n}")
    log(f"  MAX par allèle dans les 45 : "
        f"{mut['KRAS_allele'].value_counts().max()} (< 40 aussi)")

    # --- Chronos par lignée (KRAS / PRMT5 / ATR) ---
    ge = pd.read_csv(f"{DATA}/CRISPRGeneEffect.csv", index_col=0,
                     usecols=["Unnamed: 0", "KRAS (3845)", "PRMT5 (10419)",
                              "ATR (545)"])
    ge = ge.rename(columns={"KRAS (3845)": "KRAS", "PRMT5 (10419)": "PRMT5",
                            "ATR (545)": "ATR"})
    df = mut.set_index("ModelID").join(ge, how="left")
    assert df["KRAS"].notna().all(), "KRAS Chronos manquant sur une lignée"
    log(f"\n  Chronos joint à la table : {len(df)} lignées, 0 NaN sur KRAS")

    # --- (a) tests directs par allèle ---
    log("\n(a) TESTS DIRECTS — dépendance Chronos par allèle KRAS (45 lignées)")
    g12d = df[df["KRAS_allele"] == "p.G12D"]
    g12v = df[df["KRAS_allele"] == "p.G12V"]
    other = df[~df["KRAS_allele"].isin(["p.G12D", "p.G12V"])]
    log(f"  groupes : G12D n={len(g12d)}, G12V n={len(g12v)}, "
        f"autres (G12R/Q61H/G12C/G12A/inconnu) n={len(other)}")
    for gene in ["KRAS", "PRMT5"]:
        log(f"  Chronos {gene} :")
        mw(g12d[gene], g12v[gene], f"G12D vs G12V")
        mw(g12d[gene], other[gene], f"G12D vs autres")
        mw(g12v[gene], other[gene], f"G12V vs autres")
    wt = df[df["KRAS_allele"] == "inconnu"]
    log(f"  KRAS sauvages / allèle inconnu : n={len(wt)} — "
        f"Chronos KRAS médiane {wt['KRAS'].median():+.3f} "
        f"(G12D {g12d['KRAS'].median():+.3f}, G12V {g12v['KRAS'].median():+.3f})")

    # --- MRTX1133 par allèle (recalculé aujourd'hui) ---
    log("\n(a) TESTS DIRECTS — viabilité MRTX1133 par allèle "
        "(mrtx1133_prism_kras_allele.csv, recalculé)")
    mr = pd.read_csv(f"{DATA}/mrtx1133_prism_kras_allele.csv")
    log(f"  SHA mrtx1133_prism_kras_allele.csv : "
        f"{sha(f'{DATA}/mrtx1133_prism_kras_allele.csv')}")
    log(f"  n={len(mr)} lignées ; allèles : "
        f"{mr['allele'].value_counts().to_dict()}")
    d = mr[mr["allele"] == "p.G12D"]
    v = mr[mr["allele"] == "p.G12V"]
    o = mr[~mr["allele"].isin(["p.G12D", "p.G12V"])]
    log(f"  groupes : G12D n={len(d)}, G12V n={len(v)}, autres n={len(o)}")
    mw(d["mrtx1133_viab"], v["mrtx1133_viab"], "MRTX1133 G12D vs G12V")
    mw(d["mrtx1133_viab"], o["mrtx1133_viab"], "MRTX1133 G12D vs autres")
    mw(v["mrtx1133_viab"], o["mrtx1133_viab"], "MRTX1133 G12V vs autres")
    log(f"  (référence §8.20 : MRTX1133 tue les G12D spécifiquement, "
        f"p=0,0001 — valeur recalculée ci-dessus, pas importée)")

    # --- (b) tests directs par statut mutationnel ---
    log("\n(b) TESTS DIRECTS — dépendance Chronos selon le statut mutationnel")
    for gene, col in [("TP53", "TP53_mut"), ("SMAD4", "SMAD4_mut"),
                      ("CDKN2A", "CDKN2A_mut")]:
        m = df[df[col] == 1]
        w = df[df[col] == 0]
        log(f"  {gene} muté n={len(m)} vs sauvage n={len(w)} :")
        for dep in ["KRAS", "PRMT5", "ATR"]:
            mw(m[dep], w[dep], f"{gene} mut vs sauv — Chronos {dep}")

    # --- Confondant MTAP pour PRMT5 ---
    log("\n(b) CONFONDANT MTAP — CN MTAP par groupe mutationnel "
        "(OmicsCNGene.csv, seuil délétion < 0,5 comme au §8.29)")
    cn = pd.read_csv(f"{DATA}/OmicsCNGene.csv", index_col=0,
                     usecols=["Unnamed: 0", "MTAP (4507)", "CDKN2A (1029)"])
    cn = cn.rename(columns={"MTAP (4507)": "MTAP_CN",
                            "CDKN2A (1029)": "CDKN2A_CN"})
    df2 = df.join(cn, how="left")
    log(f"  CN MTAP joint : {df2['MTAP_CN'].notna().sum()}/{len(df2)} lignées")
    for gene, col in [("TP53", "TP53_mut"), ("SMAD4", "SMAD4_mut"),
                      ("CDKN2A", "CDKN2A_mut")]:
        m = df2[df2[col] == 1]
        w = df2[df2[col] == 0]
        log(f"  {gene} : CN MTAP médiane mut {m['MTAP_CN'].median():+.3f} "
            f"vs sauv {w['MTAP_CN'].median():+.3f} ; délétées (<0,5) "
            f"{int((m['MTAP_CN'] < 0.5).sum())}/{len(m)} vs "
            f"{int((w['MTAP_CN'] < 0.5).sum())}/{len(w)}")
        rho, p = spearmanr(m["MTAP_CN"], m["PRMT5"], nan_policy="omit")
        rho2, p2 = spearmanr(w["MTAP_CN"], w["PRMT5"], nan_policy="omit")
        log(f"    Spearman PRMT5 ~ CN MTAP : mut rho {rho:+.3f} (p={p:.3g}, "
            f"n={len(m)}) ; sauv rho {rho2:+.3f} (p={p2:.3g}, n={len(w)})")
    # PRMT5 par statut mutationnel DANS les strates MTAP (si effectifs >= 5)
    log("  PRMT5 par statut, stratifié par délétion MTAP (< 0,5) :")
    for gene, col in [("TP53", "TP53_mut"), ("SMAD4", "SMAD4_mut"),
                      ("CDKN2A", "CDKN2A_mut")]:
        for strat, mask in [("MTAP-délétée", df2["MTAP_CN"] < 0.5),
                            ("MTAP-intacte", df2["MTAP_CN"] >= 0.5)]:
            sub = df2[mask]
            m = sub[sub[col] == 1]["PRMT5"]
            w = sub[sub[col] == 0]["PRMT5"]
            if len(m) >= 3 and len(w) >= 3:
                mw(m, w, f"{gene} mut vs sauv, {strat} — PRMT5")
            else:
                log(f"  {gene} mut vs sauv, {strat} — PRMT5 : "
                    f"effectifs trop petits (mut n={len(m)}, sauv n={len(w)})")

    # --- (b) faisabilité série v6.1 : preuve chiffrée ---
    log("\n(b) FAISABILITÉ SÉRIE v6.1 — preuve")
    for gene, col in [("TP53", "TP53_mut"), ("SMAD4", "SMAD4_mut"),
                      ("CDKN2A", "CDKN2A_mut")]:
        log(f"  {gene} : muté {int(df[col].sum())} / sauvage "
            f"{int((df[col] == 0).sum())} — deux séries muté/non-muté "
            f"exigeraient 40 + 40 : IMPOSSIBLE")
    log("  Ordre binaire 0/1 sur 45 lignées : DÉGÉNÉRÉ (seuil forcé à la "
        "frontière des groupes par construction) — NON lancé (protocole).")
    log("\n=== FIN ===")
    OUT.close()


if __name__ == "__main__":
    main()
