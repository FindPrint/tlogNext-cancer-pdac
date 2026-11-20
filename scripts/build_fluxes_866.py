#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construction §8.66 — flux GSE62165 pour les groupes qualifiés du §8.58.
Protocole gelé : PROTOCOL_stomach_mucus_cohort4_866.md (§3, §4).
Méthode variante (a) du §8.58 (build_fluxes_858_geo.py, original intact) :
MÊMES gènes que les listes retenues TCGA (ceux présents dans la cohorte),
ordre = KRAS (valeurs puce brutes, croissant), sans correction de pureté,
cas complets seulement (jamais d'imputation).
Ordre stade en plus (règle gelée §4) : IA/IB -> I, IIA/IIB -> II,
III -> III, IVA/IVB/IV -> IV ; valeur ambiguë ou manquante -> EXCLUE ;
départage ex æquo : GSM lexicographique. Si la série stade < 40 lignes :
AUCUNE série stade construite.
Sondes -> symboles : data/GPL13667_probe2symbol.tsv (voir
build_probe2symbol_866.py) ; sondes multiples vers un même symbole :
médiane (règle du projet).
Nuls : bloc des flux permuté par lignes, graine 42, rng(42), contrôle
intact. Sorties : pdac_866_geo62165_<groupe>_<ordre>.csv (+ _nul.csv).
Inventaire : inventory_866.csv (présent/absent par gène retenu),
or_scan_866.csv (scan regex ^OR[0-9]+[A-Z]?[0-9]*$ sur l'univers mappé).
"""
import gzip
import hashlib
import re
from collections import Counter

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
SEED = 42

# Listes retenues TCGA (build_fluxes_858_geo.py, reprises sans changement).
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
TEMOIN = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A", "CPB1",
          "CELA3B", "CLPS", "CTRC", "CPA2"]
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
        return None
    need = ["KRAS"] + present
    cc = genes_df.loc[need].dropna(axis=1)
    print(f"{cohort} {gname}: {len(present)}/{len(genes)} gènes présents ; "
          f"cas complets {cc.shape[1]} ; absents cohorte : "
          f"{missing if missing else '(aucun)'}")
    order = cc.loc["KRAS"].sort_values(ascending=True).index
    flux = cc.loc[present, order].T
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    write_pair(out, f"{OUT}/pdac_866_{cohort}_{gname}_kras.csv")
    return cc, present


def main():
    mat = pd.read_csv(f"{DATA}/GSE62165_series_matrix.txt.gz", sep="\t",
                      comment="!", index_col=0, low_memory=False)
    mat.index = mat.index.astype(str).str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    gsm = list(mat.columns)
    kinds = ["?"] * len(gsm)
    stages = [None] * len(gsm)
    with gzip.open(f"{DATA}/GSE62165_series_matrix.txt.gz", "rt",
                   encoding="utf-8", errors="replace") as f:
        ch1 = []
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_characteristics_ch1"):
                ch1.append([v.strip('"') for v in
                            line.rstrip("\n").split("\t")[1:]])
    for i in range(len(gsm)):
        vals = [row[i] for row in ch1 if i < len(row)]
        joined = " | ".join(vals)
        if "tissue: pancreatic tumor" in joined:
            kinds[i] = "Tumor"
        elif "tissue: non-tumoral pancreatic tissue" in joined:
            kinds[i] = "Normal"
        m = re.search(r"Stage:\s*([^\s|]+)", joined)
        if m:
            stages[i] = m.group(1)
    tum = [g for g, k in zip(gsm, kinds) if k == "Tumor"]
    print(f"GSE62165 : {len(tum)} tumeurs (sur {len(gsm)} échantillons)")
    print("  Stades bruts (tous échantillons) :",
          dict(Counter([s for s in stages if s])))

    pmap = {}
    with open(f"{DATA}/GPL13667_probe2symbol.tsv") as f:
        next(f)
        for line in f:
            p, s = line.rstrip("\n").split("\t")
            pmap[p] = s
    sub = mat[tum].copy()
    syms = sub.index.astype(str).map(lambda x: pmap.get(x))
    sub.index = syms
    sub = sub[sub.index.notna()]
    genes = sub.groupby(level=0).median()
    print(f"GSE62165 : {len(genes)} gènes uniques ; "
          f"KRAS présent : {'KRAS' in genes.index}")
    print(f"  Sondes sans symbole exclues : "
          f"{len(mat) - sub.index.notna().sum() - 0} (lignes non mappées)")

    # ---- Inventaire : présence des gènes retenus + témoin ----
    inv_rows = []
    for gname, glist in list(RETAINED.items()) + [("TEMOIN", TEMOIN)]:
        for g in glist:
            inv_rows.append({"groupe": gname, "gene": g,
                             "present_geo62165": g in genes.index})
    inv = pd.DataFrame(inv_rows)
    inv.to_csv(f"{OUT}/inventory_866.csv", index=False)
    for gname, glist in list(RETAINED.items()) + [("TEMOIN", TEMOIN)]:
        n = sum(g in genes.index for g in glist)
        print(f"  Inventaire {gname}: {n}/{len(glist)} présents")

    # ---- Scan OR de l'univers mappé ----
    or_pat = re.compile(r"^OR[0-9]+[A-Z]?[0-9]*$")
    or_genes = sorted([g for g in genes.index if or_pat.match(g)])
    print(f"  Scan OR (regex) : {len(or_genes)} symboles OR dans l'univers mappé")
    or_df = pd.DataFrame({"gene": or_genes})
    or_df.to_csv(f"{OUT}/or_scan_866.csv", index=False)
    # OR de la liste fermée §8.58
    closed = ["OR51E2", "OR51E1", "OR2AT4", "OR1A1", "OR2J3", "OR10J5"]
    print("  Liste fermée OR §8.58 :", {g: (g in genes.index) for g in closed})

    # ---- Ordre stade (règle gelée) ----
    def stage_rank(s):
        if s is None:
            return None
        if s in ("1a", "1b"):
            return 1
        if s in ("2a", "2b"):
            return 2
        if s == "3":
            return 3
        if s == "4":
            return 4
        return None

    stage_map = {}
    for gsm_id, k, s in zip(gsm, kinds, stages):
        if k == "Tumor":
            stage_map[gsm_id] = stage_rank(s)
    print("  Stades tumoraux (rang principal) :",
          dict(Counter([v for v in stage_map.values() if v is not None])),
          "; sans rang :", sum(1 for v in stage_map.values() if v is None))

    for gname in GROUPS:
        res = kras_file(genes, RETAINED[gname], "geo62165", gname)
        if res is None:
            continue
        cc, present = res
        rows = []
        excluded = []
        for gsm_id in cc.columns:
            r = stage_map.get(gsm_id)
            if r is None:
                excluded.append(gsm_id)
            else:
                rows.append((r, gsm_id))
        rows.sort(key=lambda t: (t[0], t[1]))
        if len(rows) < 40:
            print(f"  geo62165 {gname} stade : {len(rows)} lignes < 40 — "
                  f"PAS DE SÉRIE STADE (règle gelée). Exclues : {excluded}")
            continue
        order_stage = [g for _, g in rows]
        flux = cc.loc[present, order_stage].T
        out = pd.DataFrame({"STAGE": [r for r, _ in rows]})
        out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
        print(f"  geo62165 {gname} stade : {len(rows)} lignes, "
              f"exclues : {len(excluded)}")
        write_pair(out, f"{OUT}/pdac_866_geo62165_{gname}_stage.csv")


if __name__ == "__main__":
    main()
