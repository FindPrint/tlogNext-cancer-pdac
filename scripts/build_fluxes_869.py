#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flux §8.69 — confirmation indépendante pour maxsep (C3).
Variante (a) [seule] : les 12 mêmes gènes que la v4 TCGA, ordre = KRAS
croissant, sans correction. Cas complets seulement. Nul = lignes
permutées, graine 42. Copie adaptée de build_fluxes_geo62452.py
(original intact) ; protocole PROTOCOL_maxsep_independent_869.md.
Usage : python3 build_fluxes_869.py [--cohort 57495|62165|21501]
  57495 (défaut) : GSE57495 / GPL15048, mapping GPL15048_probe2symbol.tsv.
  62165 (repli, protocole §3) : GSE62165 / GPL13667, mapping
  GPL13667_probe2symbol.tsv, tumeurs seules (règle §8.66).
  21501 (cohorte #3, addendum) : GSE21501 / GPL4133, mapping
  GPL4133_probe2symbol.tsv, tumeurs = libellé « tissue: Patient
  Primary Pancreatic Tumor » en characteristics_ch2 (règle
  mécanique, vérifiée positionnellement ; 30 + 102 = 132).
Portes d'acceptation (protocole §5) : KRAS présent, les 12 gènes v4
présents, cas complets >= 40 — sinon sortie 1, message explicite, et
AUCUN run n'est lancé (le repli ne s'applique que sur ce signal).
"""
import argparse
import gzip
import hashlib
import re
import sys
from collections import Counter

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
SEED = 42

V4_GENES = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
            "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]

COHORTS = {
    "57495": {
        "matrix": "GSE57495_series_matrix.txt.gz",
        "mapping": "GPL15048_probe2symbol.tsv",
        "tag": "geo57495",
    },
    "62165": {
        "matrix": "GSE62165_series_matrix.txt.gz",
        "mapping": "GPL13667_probe2symbol.tsv",
        "tag": "geo62165",
    },
    "21501": {
        "matrix": "GSE21501_series_matrix.txt.gz",
        "mapping": "GPL4133_probe2symbol.tsv",
        "tag": "geo21501",
    },
}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cohort", choices=list(COHORTS), default="57495")
    args = ap.parse_args()
    cfg = COHORTS[args.cohort]
    mpath = f"{DATA}/{cfg['matrix']}"

    # ---- 1. Matrice : lignes = sondes, colonnes = GSM ----
    mat = pd.read_csv(mpath, sep="\t", comment="!", index_col=0,
                      low_memory=False)
    mat.index = mat.index.astype(str).str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    print(f"Matrice : {mat.shape[0]} sondes x {mat.shape[1]} échantillons")
    print("Valeurs : min=%.2f médiane=%.2f max=%.2f ; NaN=%d" % (
        float(np.nanmin(mat.values)), float(np.nanmedian(mat.values)),
        float(np.nanmax(mat.values)), int(mat.isna().sum().sum())))

    # ---- 2. Annotation des échantillons (characteristics_ch1) ----
    gsm_order = list(mat.columns)
    kinds = ["?"] * len(gsm_order)
    stages = [None] * len(gsm_order)
    ch2 = []
    with gzip.open(mpath, "rt", encoding="utf-8",
                   errors="replace") as f:
        ch1 = []
        titles = []
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_characteristics_ch1"):
                ch1.append([v.strip('"') for v in
                            line.rstrip("\n").split("\t")[1:]])
            if line.startswith("!Sample_characteristics_ch2"):
                ch2.append([v.strip('"') for v in
                            line.rstrip("\n").split("\t")[1:]])
            if line.startswith("!Sample_title"):
                titles = [t.strip('"') for t in
                          line.rstrip("\n").split("\t")[1:]]
    for i in range(len(gsm_order)):
        vals = [row[i] for row in ch1 if i < len(row)]
        joined = " | ".join(vals)
        if args.cohort == "62165":
            if "tissue: pancreatic tumor" in joined:
                kinds[i] = "Tumor"
            elif "tissue: non-tumoral pancreatic tissue" in joined:
                kinds[i] = "Normal"
        elif args.cohort == "21501":
            # GSE21501 (Agilent deux couleurs) : l'annotation est en
            # characteristics_ch2, RAGUÉE : le libellé
            # « tissue: Patient Primary Pancreatic Tumor » est en
            # ligne ch2 n°0 pour les 30 premiers échantillons
            # (Nebraska/UNC, sans données cliniques) et en ligne
            # ch2 n°4 pour les 102 suivants (cohorte Stratford
            # annotée cliniquement) — vérifié positionnellement
            # avant la construction (30 + 102 = 132, contigus).
            # Règle mécanique : tumeur si le libellé figure dans
            # UNE ligne ch2 de l'échantillon. Les 30 sans données
            # cliniques sont gardés : la paire n'a besoin d'aucune
            # donnée clinique (ordre KRAS uniquement).
            vals2 = [row[i] for row in ch2 if i < len(row)]
            if ("tissue: Patient Primary Pancreatic Tumor" in vals2):
                kinds[i] = "Tumor"
        else:  # 57495 : série de 63 tumeurs PDAC, titres PDAC1..63
            if titles and titles[i].startswith("PDAC"):
                kinds[i] = "Tumor"
        m = re.search(r"Stage:\s*([^\s|]+)", joined)
        if m:
            stages[i] = m.group(1)
    print("Types d'échantillons (characteristics_ch1 / titres) :",
          dict(Counter(kinds)))
    print("Stades (characteristics_ch1) :",
          dict(Counter(s for s in stages if s is not None)))
    tum = [g for g, k in zip(gsm_order, kinds) if k == "Tumor"]
    print(f"Tumeurs retenues : {len(tum)}")
    sub = mat[tum]

    # ---- 3. Sondes -> symboles (médiane par gène) ----
    pmap = {}
    with open(f"{DATA}/{cfg['mapping']}") as f:
        next(f)
        for line in f:
            p, s = line.rstrip("\n").split("\t")
            pmap[p] = s
    sub_idx = sub.index.astype(str)
    syms = sub_idx.map(lambda x: pmap.get(x))
    n_mapped = int(syms.notna().sum())
    print(f"Sondes mappées vers un symbole : {n_mapped} / {len(sub)}")
    sub2 = sub.copy()
    sub2.index = syms
    sub2 = sub2[sub2.index.notna()]
    dup = sub2.index.duplicated(keep=False).sum()
    print(f"Symboles dupliqués : {dup} lignes -> agrégation par médiane")
    genes = sub2.groupby(level=0).median()
    print(f"Après agrégation : {genes.shape[0]} gènes uniques")
    print("Gènes v4 présents :",
          [g for g in V4_GENES if g in genes.index])
    print("Gènes v4 absents :",
          [g for g in V4_GENES if g not in genes.index])
    print("KRAS présent :", "KRAS" in genes.index)

    # ---- 4. Portes d'acceptation (protocole §5) ----
    gates = []
    gates.append(("KRAS présent", "KRAS" in genes.index))
    gates.append(("12 gènes v4 présents",
                  all(g in genes.index for g in V4_GENES)))
    present = [g for g in V4_GENES if g in genes.index]
    need = ["KRAS"] + present
    cc = genes.loc[need].dropna(axis=1) if "KRAS" in genes.index else None
    n_cc = int(cc.shape[1]) if cc is not None else 0
    gates.append(("cas complets >= 40", n_cc >= 40))
    print(f"Cas complets (KRAS + {len(present)} gènes) : {n_cc} / "
          f"{len(tum)}")
    for name, ok in gates:
        print(f"PORTE {'OK ' if ok else 'ÉCHEC'} : {name}")
    if not all(ok for _, ok in gates):
        print("COHORTE INUTILISABLE selon le protocole §5 — arrêt, "
              "aucun CSV écrit, aucun run lancé.", file=sys.stderr)
        return 1

    # ---- 5. Variante (a) : les 12 gènes v4, ordre KRAS ----
    order = cc.loc["KRAS"].sort_values(ascending=True).index
    flux = cc.loc[present, order].T
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_869_{cfg['tag']}_fluxes.csv"
    out.to_csv(out_path, index=False)
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_869_{cfg['tag']}_fluxes_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes) SHA {sha(out_path)}")
    print(f"Écrit : {nul_path} SHA {sha(nul_path)}")
    print("KRAS (valeurs puce) : min=%.2f médiane=%.2f max=%.2f" % (
        float(cc.loc["KRAS"].min()), float(cc.loc["KRAS"].median()),
        float(cc.loc["KRAS"].max())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
