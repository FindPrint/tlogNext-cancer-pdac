#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flux §8.99 — GSE184585, 12 flux (DPCR1 remappé MUCL3, vérifié 5/5).

GSE184585 : 82 tumeurs PDAC primaires (MSKCC, réséquées), GPL17586
(Affymetrix Human Transcriptome Array 2.0, HTA 2.0), valeurs
déposées dans la matrice série (échelle log2 apparente, sans
correction). Protocole gelé PROTOCOL_899_gse184585.md (27 nov.
2026, avant toute construction et tout run).

Mapping sondes -> symboles : Bioconductor hta20transcriptcluster.db
8.8.0 (sonde -> Entrez) + org.Hs.eg.db 3.23.1 (Entrez -> symbole),
tous deux détenus localement et vérifiés par SHA. Aucune sonde
mappée à la main. Agrégation par médiane en cas de sondes
multiples pour un même gène (même méthode que §8.79).

Remappage DPCR1 -> MUCL3 (porte §2 du protocole, type §8.85) :
  R1 HGNC fetch symbol MUCL3 : MUCL3, HGNC:21666, « mucin like 3 »,
     Approved, prev_symbol ['DPCR1'], date_symbol_changed
     2018-03-19, ensembl ENSG00000168631, entrez 135656.
  R2 HGNC fetch prev_symbol DPCR1 : numFound = 1, même
     enregistrement (HGNC:21666, MUCL3).
  R3 org.Hs.eg.db : Entrez 135656 -> RefSeq NM_080870, Ensembl
     ENSG00000168631 (+ 4 autres, mêmes que §8.79) ; alias DPCR1
     et MUCL3 -> même _id 18000.
  R4 Ensembl REST : MUCL3 résout (ENSG00000168631, chr 6,
     30940973-30954221, GRCh38) ; DPCR1 ne résout pas
     (« No valid lookup found for symbol DPCR1 »).
  R5 Croisement avec les données détenues : MUCL3 = 5 sondes
     (Entrez 135656) ; DPCR1 = 0 sonde, aucune entrée Entrez
     (vérifié ici, avant construction, dans les deux SQLite).
Le flux est nommé MUCL3 (ex-DPCR1) partout — jamais « DPCR1 » seul.

Portes d'acceptation (protocole §1) : plateforme GPL17586, KRAS
présent, 11 gènes v4 exacts + MUCL3 présents ET DPCR1 absent, cas
complets >= 40 — sinon sortie 1, message explicite, et AUCUN run
n'est lancé.
Usage : python3 build_fluxes_899.py
"""
import gzip
import hashlib
import sys
from collections import Counter

import numpy as np
import pandas as pd
import sqlite3

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"

V4_GENES = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
            "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]
# DPCR1 est lu comme MUCL3 (remappage vérifié 5/5, voir docstring).
FLUX_GENES = ["PGC", "REG4", "CLDN18", "MUC17", "MUCL3", "CR2", "KRT20",
              "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]

MATRIX = "GSE184585_series_matrix.txt.gz"
HTA_SQLITE = "hta20transcriptcluster.sqlite"
EG_SQLITE = "org.Hs.eg.sqlite"
MAPPING = "GPL17586_probe2symbol.tsv"

EXPECTED_MATRIX_SHA256 = (
    "e2be8441979ee9210033fac588ed99e2605cdaa598e39e6d1e0d5304aad6de01")
EXPECTED_HTA_SHA256 = (
    "405837e13af445ccf8686c7f2985cbd5c685109d57b5c7e2ec946a2c562a4dac")
EXPECTED_EG_SHA256 = (
    "bbdf1a4d9181ac0873d8993b6c25742d6658eaa6c14a10b2df1a19dfba1f3dba")
EXPECTED_PLATFORM = "GPL17586"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    for name, expected in [
            (MATRIX, EXPECTED_MATRIX_SHA256),
            (HTA_SQLITE, EXPECTED_HTA_SHA256),
            (EG_SQLITE, EXPECTED_EG_SHA256)]:
        got = sha(f"{DATA}/{name}")
        if got != expected:
            print(f"ERREUR : SHA {name} différent de l'empreinte gelée "
                  f"(lu {got}).", file=sys.stderr)
            return 1
    print("Matrice et bases d'annotation SHA vérifiées (empreintes gelées).")

    # ---- 0. Plateforme lue dans l'en-tête ----
    mpath = f"{DATA}/{MATRIX}"
    platform = None
    with gzip.open(mpath, "rt", encoding="utf-8",
                   errors="replace") as f:
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Series_platform_id"):
                platform = line.split("\t")[1].strip().strip('"')
    print(f"Plateforme lue : {platform}")
    if platform != EXPECTED_PLATFORM:
        print("ERREUR : plateforme != GPL17586 — arrêt.", file=sys.stderr)
        return 1

    # ---- 1. Mapping sondes -> symboles (SQLite, aucune main) ----
    hta = sqlite3.connect(f"{DATA}/{HTA_SQLITE}")
    eg = sqlite3.connect(f"{DATA}/{EG_SQLITE}")
    eg_map = {}
    for sym, gid in eg.execute(
            "SELECT gi.symbol, g.gene_id FROM gene_info gi "
            "JOIN genes g ON g._id = gi._id"):
        eg_map.setdefault(gid, sym)
    pmap = {}
    n_probes = 0
    n_mapped = 0
    for probe_id, gene_id in hta.execute(
            "SELECT probe_id, gene_id FROM probes"):
        n_probes += 1
        if gene_id is None:
            continue
        sym = eg_map.get(str(gene_id))
        if sym is not None:
            pmap[probe_id] = sym
            n_mapped += 1
    print(f"Sondes HTA : {n_probes} ; mappées vers un symbole : {n_mapped}")
    with open(f"{DATA}/{MAPPING}", "w", encoding="utf-8") as f:
        f.write("probe_id\tsymbol\n")
        for p in sorted(pmap):
            f.write(f"{p}\t{pmap[p]}\n")
    print(f"Mapping écrit : {DATA}/{MAPPING} "
          f"({len(pmap)} sondes) SHA {sha(f'{DATA}/{MAPPING}')}")

    # ---- 2. Matrice : lignes = sondes, colonnes = GSM ----
    mat = pd.read_csv(mpath, sep="\t", comment="!", index_col=0,
                      low_memory=False)
    mat.index = mat.index.astype(str).str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    print(f"Matrice : {mat.shape[0]} sondes x {mat.shape[1]} échantillons")
    print("Valeurs : min=%.2f médiane=%.2f max=%.2f ; NaN=%d" % (
        float(np.nanmin(mat.values)), float(np.nanmedian(mat.values)),
        float(np.nanmax(mat.values)), int(mat.isna().sum().sum())))

    # ---- 3. Annotation des échantillons (characteristics_ch1) ----
    gsm_order = list(mat.columns)
    kinds = ["?"] * len(gsm_order)
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
            if line.startswith("!Sample_title"):
                titles = [t.strip('"') for t in
                          line.rstrip("\n").split("\t")[1:]]
    for i in range(len(gsm_order)):
        vals = [row[i] for row in ch1 if i < len(row)]
        joined = " | ".join(vals)
        if "Pancreatic ductal adecnocarcinoma" in joined:
            kinds[i] = "Tumor"
        elif titles and titles[i].startswith("PDAC"):
            kinds[i] = "Tumor"
    print("Types d'échantillons (characteristics_ch1 / titres) :",
          dict(Counter(kinds)))
    tum = [g for g, k in zip(gsm_order, kinds) if k == "Tumor"]
    print(f"Tumeurs retenues : {len(tum)}")
    sub = mat[tum]

    # ---- 4. Sondes -> symboles (médiane par gène) ----
    sub_idx = sub.index.astype(str)
    syms = sub_idx.map(lambda x: pmap.get(x))
    n_mapped_rows = int(syms.notna().sum())
    print(f"Sondes de la matrice mappées vers un symbole : "
          f"{n_mapped_rows} / {len(sub)}")
    sub2 = sub.copy()
    sub2.index = syms
    sub2 = sub2[sub2.index.notna()]
    dup = int(sub2.index.duplicated(keep=False).sum())
    print(f"Symboles dupliqués : {dup} lignes -> agrégation par médiane")
    genes = sub2.groupby(level=0).median()
    print(f"Après agrégation : {genes.shape[0]} gènes uniques")
    print("Gènes v4 exacts présents :",
          [g for g in V4_GENES if g in genes.index])
    print("Gènes v4 exacts absents :",
          [g for g in V4_GENES if g not in genes.index])
    print("MUCL3 (ex-DPCR1) présent :", "MUCL3" in genes.index,
          "| sondes MUCL3 :",
          int((sub2.index == "MUCL3").sum()))
    print("DPCR1 présent :", "DPCR1" in genes.index)
    print("KRAS présent :", "KRAS" in genes.index)

    # ---- 5. Portes d'acceptation (protocole §1–§2) ----
    gates = []
    gates.append(("KRAS présent", "KRAS" in genes.index))
    exact = [g for g in V4_GENES if g in genes.index]
    gates.append(("11 gènes v4 exacts présents (DPCR1 absent)",
                  len(exact) == 11 and "DPCR1" not in genes.index))
    gates.append(("MUCL3 (ex-DPCR1) présent", "MUCL3" in genes.index))
    gates.append(("DPCR1 absent (0 sonde)", "DPCR1" not in genes.index))
    need = ["KRAS"] + FLUX_GENES
    cc = genes.loc[need].dropna(axis=1) if "KRAS" in genes.index else None
    n_cc = int(cc.shape[1]) if cc is not None else 0
    gates.append(("cas complets >= 40", n_cc >= 40))
    print(f"Cas complets (KRAS + 12 flux) : {n_cc} / {len(tum)}")
    for name, ok in gates:
        print(f"PORTE {'OK ' if ok else 'ÉCHEC'} : {name}")
    if not all(ok for _, ok in gates):
        print("COHORTE INUTILISABLE selon le protocole §1–§2 — arrêt, "
              "aucun CSV écrit, aucun run lancé.", file=sys.stderr)
        return 1

    # ---- 6. Variante (a) : les 12 flux, ordre KRAS ----
    order = cc.loc["KRAS"].sort_values(ascending=True).index
    flux = cc.loc[FLUX_GENES, order].T
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_899_gse184585_fluxes.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes, "
          f"{out.shape[1]-1} flux) SHA {sha(out_path)}")
    print("KRAS (axe) : min=%.2f médiane=%.2f max=%.2f" % (
        float(cc.loc["KRAS"].min()), float(cc.loc["KRAS"].median()),
        float(cc.loc["KRAS"].max())))
    print("Sondes par flux :",
          {g: int((sub2.index == g).sum()) for g in FLUX_GENES})
    return 0


if __name__ == "__main__":
    sys.exit(main())
