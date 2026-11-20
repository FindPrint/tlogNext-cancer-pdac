#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confirmation §8.58 — flux GSE71729 et GSE62452 pour les groupes
qualifiés par la règle gelée du protocole (PROTOCOL_stomach_mucus_flux_858.md
§6 : MC réel−nul > 0,05 OU S_sep réel−nul > 0,05 OU D1 |d| ≥ 0,50
au-delà du nul, sur au moins un ordre TCGA).
Groupes qualifiés à 24/24 TCGA : G1, G2, G3, G4, G5 (TEMOIN exclu :
c'est un témoin, pas un groupe candidat).
Méthode variante (a) des scripts du projet (build_fluxes_geo71729.py,
build_fluxes_geo62452.py, originaux intacts) : MÊMES gènes que les
listes retenues TCGA (ceux présents dans la cohorte), ordre = KRAS
(valeurs puce brutes, croissant), sans correction de pureté, cas
complets seulement (jamais d'imputation). GSE71729 : 145 tumeurs
primaires (« tissue type: Primary »). GSE62452 : 69 tumeurs
(« tissue: Pancreatic tumor ») ; ordre stade en plus, voir ci-dessous.
Règle de stade GSE62452, gelée AVANT la construction (le protocole
§6 ne la figeait pas ; elle est figée ici, avant tout calcul) :
« Stage: X » des characteristics_ch1 ; IA/IB → I, IIA/IIB → II,
III → III, IVA/IVB/IV → IV ; « >IIB » → EXCLU (ambigu : III ou
IV, impossible à assigner) ; stade manquant → exclu. Départage des
ex æquo dans un même stade : GSM, ordre lexicographique croissant
(neutre). Si la série stade tombe sous 40 lignes (minimum fast),
AUCUNE série stade n'est construite, aucun run stade lancé (règle
écrite d'avance, comme au §8.45). Groupe non construit dans une
cohorte si < 3 gènes retenus présents : noté, sans run.
Nuls : bloc des flux permuté par lignes, graine 42, rng(42),
contrôle intact. Sorties : pdac_858_<cohorte>_<groupe>_<ordre>.csv
(+ _nul.csv).
"""
import gzip
import hashlib
import re

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
SEED = 42

# Listes retenues TCGA (build_fluxes_858_tcga.py, vérifiées sur les CSV).
RETAINED = {
    "G1": ["TFF1", "TFF2", "MUC6", "MUC5B", "MUC4", "AQP5", "REG1A", "TFF3",
           "GKN1", "PGA3", "REG3A", "MUC21", "PGA4", "GKN2", "AGR2", "GAST",
           "SPDEF", "FCGBP", "MUC13", "REG1B"],
    "G2": ["PRSS1", "PRSS3", "AMY1A", "PNLIPRP2", "AMY2B", "AMY2A", "CPB2",
           "CELA2A", "CPA3", "CELA2B", "PNLIP", "PLA2G1B", "CEL", "CPB1",
           "PNLIPRP1", "CLPS", "CPA2", "CTRB2", "CTRB1", "CELA3B"],
    "G3": ["OR7D2", "OR13A1", "OR2A4", "OR52N4", "OR2B6", "OR51E2", "OR51E1",
           "OR2A7", "OR52N2", "OR2L13", "OR1J2", "OR2W3", "OR10H1", "OR2A1",
           "OR4C6", "OR7A5", "OR3A2", "OR5K2", "OR2T10", "OR2C1"],
    "G4": ["UGT1A1", "ALDH3A1", "CYP2C9", "CYP3A4", "ADH1B", "UGT2B7", "ADH4",
           "ADH1C", "ADH6", "ADH1A", "AOX1", "FMO1", "CYP2E1", "NOS1", "NOS2",
           "CYP2A6", "CBS", "TAS1R3", "ALDH3B1", "TAS2R38"],
    "G5": ["CDX1", "CDX2", "VIL1", "SI", "LCT", "FABP2", "APOA4", "APOB",
           "KRT7", "KRT19", "CHGA", "CHGB", "SYP", "INSM1", "NEUROD1"],
}
GROUPS = ["G1", "G2", "G3", "G4", "G5"]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_pair(df, path):
    df.to_csv(path, index=False)
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(df))
    nul = df.copy()
    nul.iloc[:, 1:] = df.iloc[:, 1:].to_numpy()[perm]
    pn = path.replace(".csv", "_nul.csv")
    nul.to_csv(pn, index=False)
    print(f"  Écrit : {path.split('/')[-1]} ({len(df)} lignes) "
          f"SHA {sha(path)[:12]}… ; nul SHA {sha(pn)[:12]}…")


def kras_file(genes_df, genes, cohort, gname):
    present = [g for g in genes if g in genes_df.index]
    missing = [g for g in genes if g not in genes_df.index]
    if len(present) < 3:
        print(f"{cohort} {gname}: {len(present)} gènes présents — NON CONSTRUIT.")
        return
    need = ["KRAS"] + present
    cc = genes_df.loc[need].dropna(axis=1)
    print(f"{cohort} {gname}: {len(present)}/{len(genes)} gènes présents ; "
          f"cas complets {cc.shape[1]} ; absents cohorte : "
          f"{missing if missing else '(aucun)'}")
    order = cc.loc["KRAS"].sort_values(ascending=True).index
    flux = cc.loc[present, order].T
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    write_pair(out, f"{OUT}/pdac_858_{cohort}_{gname}_kras.csv")
    return cc, present


def main():
    # ---- GSE71729 : symboles directs, 145 primaires ----
    mat = pd.read_csv(f"{DATA}/GSE71729_series_matrix.txt.gz", sep="\t",
                      comment="!", index_col=0, low_memory=False)
    mat.index = mat.index.str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    mat = mat.groupby(level=0).median()
    gsm_order = list(mat.columns)
    kinds = ["?"] * len(gsm_order)
    with gzip.open(f"{DATA}/GSE71729_series_matrix.txt.gz", "rt",
                   encoding="utf-8", errors="replace") as f:
        ch2 = []
        titles = []
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_characteristics_ch2"):
                ch2.append([v.strip('"') for v in
                            line.rstrip("\n").split("\t")[1:]])
            if line.startswith("!Sample_title"):
                titles = [t.strip('"') for t in
                          line.rstrip("\n").split("\t")[1:]]
    for i in range(len(gsm_order)):
        vals = [row[i] for row in ch2 if i < len(row)]
        joined = " | ".join(vals)
        if "tissue type: Primary" in joined:
            kinds[i] = "Primary"
        elif "tissue type: Metastasis" in joined:
            kinds[i] = "Metastasis"
        elif "tissue type: Normal" in joined:
            kinds[i] = "Normal"
        elif titles[i].endswith("-CellLine"):
            kinds[i] = "CellLine"
    prim = [g for g, k in zip(gsm_order, kinds) if k == "Primary"]
    print(f"GSE71729 : {len(prim)} tumeurs primaires "
          f"(sur {len(gsm_order)} échantillons)")
    sub71729 = mat[prim]
    print(f"GSE71729 KRAS présent : {'KRAS' in sub71729.index}")
    for gname in GROUPS:
        kras_file(sub71729, RETAINED[gname], "geo71729", gname)

    # ---- GSE62452 : sondes -> symboles, 69 tumeurs ----
    g = pd.read_csv(f"{DATA}/GSE62452_series_matrix.txt.gz", sep="\t",
                    comment="!", index_col=0, low_memory=False)
    g.index = g.index.astype(str).str.strip('"')
    g.columns = [c.strip('"') for c in g.columns]
    gsm62452 = list(g.columns)
    kinds = ["?"] * len(gsm62452)
    stages = [None] * len(gsm62452)
    with gzip.open(f"{DATA}/GSE62452_series_matrix.txt.gz", "rt",
                   encoding="utf-8", errors="replace") as f:
        ch1 = []
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_characteristics_ch1"):
                ch1.append([v.strip('"') for v in
                            line.rstrip("\n").split("\t")[1:]])
    for i in range(len(gsm62452)):
        vals = [row[i] for row in ch1 if i < len(row)]
        joined = " | ".join(vals)
        if "tissue: Pancreatic tumor" in joined:
            kinds[i] = "Tumor"
        elif "tissue: adjacent pancreatic non-tumor" in joined:
            kinds[i] = "Normal"
        m = re.search(r"Stage:\s*([^\s|]+)", joined)
        if m:
            stages[i] = m.group(1)
    tum = [gsm for gsm, k in zip(gsm62452, kinds) if k == "Tumor"]
    print(f"GSE62452 : {len(tum)} tumeurs (sur {len(gsm62452)} échantillons)")
    from collections import Counter
    print("  Stades bruts (tous échantillons) :",
          dict(Counter([s for s in stages if s])))
    pmap = {}
    with open(f"{DATA}/GPL6244_probe2symbol.tsv") as f:
        next(f)
        for line in f:
            p, s = line.rstrip("\n").split("\t")
            pmap[p] = s
    sub = g[tum].copy()
    syms = sub.index.astype(str).map(lambda x: pmap.get(x))
    sub.index = syms
    sub = sub[sub.index.notna()]
    genes62452 = sub.groupby(level=0).median()
    print(f"GSE62452 : {len(genes62452)} gènes uniques ; "
          f"KRAS présent : {'KRAS' in genes62452.index}")

    def stage_rank(s):
        if s is None:
            return None
        if s in ("IA", "IB"):
            return 1
        if s in ("IIA", "IIB"):
            return 2
        if s == "III":
            return 3
        if s in ("IV", "IVA", "IVB"):
            return 4
        return None  # ">IIB" et autres : exclus

    stage_map = {}
    for gsm, k, s in zip(gsm62452, kinds, stages):
        if k == "Tumor":
            stage_map[gsm] = stage_rank(s)
    print("  Stades tumoraux (rang principal) :",
          dict(Counter([v for v in stage_map.values() if v is not None])),
          "; sans rang :", sum(1 for v in stage_map.values() if v is None))
    for gname in GROUPS:
        res = kras_file(genes62452, RETAINED[gname], "geo62452", gname)
        if res is None:
            continue
        cc, present = res
        rows = []
        excluded = []
        for gsm in cc.columns:
            r = stage_map.get(gsm)
            if r is None:
                excluded.append(gsm)
            else:
                rows.append((r, gsm))
        rows.sort(key=lambda t: (t[0], t[1]))
        if len(rows) < 40:
            print(f"  geo62452 {gname} stade : {len(rows)} lignes < 40 — "
                  f"PAS DE SÉRIE STADE (règle gelée). Exclues : {excluded}")
            continue
        order_stage = [gsm for _, gsm in rows]
        flux = cc.loc[present, order_stage].T
        out = pd.DataFrame({"STAGE": [r for r, _ in rows]})
        out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
        print(f"  geo62452 {gname} stade : {len(rows)} lignes, "
              f"exclues : {len(excluded)}")
        write_pair(out, f"{OUT}/pdac_858_geo62452_{gname}_stage.csv")


if __name__ == "__main__":
    main()
