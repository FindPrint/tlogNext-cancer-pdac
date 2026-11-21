#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flux §8.74 — GSE131050, lot Yeh_seq FF (une tumeur indépendante =
une ligne). Variante (a) : les 12 mêmes gènes que la v4 TCGA, ordre =
KRAS croissant, sans correction. Cas complets seulement. Nul = lignes
permutées, graine 42. Copie adaptée de build_fluxes_871.py (original
intact) ; protocole PROTOCOL_maxsep_gse131050_874.md.
Usage : python3 build_fluxes_874.py
  Source : data/GSE131050_PurIST_Yeh_seq.tsv.gz (GPL18573, Illumina
  NextSeq 500) + matrice d'en-tête data/GSE131050-GPL18573_series_
  matrix.txt.gz (GSM, titres, caractéristiques).
  Sélection : titres S###.FF.Pi.<code> (tumeurs primaires flash-
  frozen, 47 colonnes attendues) ; les 28 PDX, 45 FNA et 5 FFPE
  primaires sont exclus et comptés. Les 47 colonnes FF sont
  regroupées par code-tumeur (42 codes) ; les 4 codes à réplicats
  FF (0417T1 x3, 0523T1 x2, 0806T1 x2, 1119T1 x2) sont agrégés par
  MÉDIANE par gène (précédent du projet). Le code 0921T1 (FNA
  seul) n'entre pas dans le lot FF.
Portes d'acceptation (protocole §5) : plateforme GPL18573, KRAS
présent, les 12 gènes v4 présents (une ligne chacun), cas complets
>= 40 tumeurs indépendantes — sinon sortie 1, message explicite,
et AUCUN run n'est lancé (aucun repli dans ce chantier).
"""
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

TSV = f"{DATA}/GSE131050_PurIST_Yeh_seq.tsv.gz"
MATRIX = f"{DATA}/GSE131050-GPL18573_series_matrix.txt.gz"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    # ---- 1. Matrice d'en-tête : GSM, titres, plateforme, types ----
    platform = None
    gsm = []
    titles = []
    char_lines = []
    with gzip.open(MATRIX, "rt", encoding="utf-8",
                   errors="replace") as f:
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Series_platform_id"):
                platform = line.split("\t")[1].strip().strip('"')
            if line.startswith("!Sample_geo_accession"):
                gsm = [v.strip('"') for v in
                       line.rstrip("\n").split("\t")[1:]]
            if line.startswith("!Sample_title"):
                titles = [t.strip('"') for t in
                          line.rstrip("\n").split("\t")[1:]]
            if line.startswith("!Sample_characteristics_ch1"):
                char_lines.append([v.strip('"') for v in
                                   line.rstrip("\n").split("\t")[1:]])
    print(f"Matrice : plateforme lue = {platform} ; "
          f"{len(gsm)} GSM ; {len(titles)} titres ; "
          f"{len(char_lines)} lignes de caractéristiques")
    # Les 3 lignes de caractéristiques sont, dans l'ordre du fichier :
    # sample type, lib prep kit, extraction protocol (125 valeurs ch.).
    sample_type = char_lines[0] if char_lines else []
    print("Types d'échantillons (matrice) :",
          dict(Counter(sample_type)))

    # ---- 2. Table Yeh_seq : geneID = ENSG...;SYMBOLE ----
    with gzip.open(TSV, "rt", encoding="utf-8", errors="replace") as f:
        hdr = f.readline().rstrip("\n").split("\t")
        cols = hdr[1:]
        rows = {}
        for line in f:
            gid, rest = line.rstrip("\n").split("\t", 1)
            sym = gid.split(";", 1)[1] if ";" in gid else gid
            rows[sym] = [float(v) for v in rest.split("\t")]
    print(f"TSV Yeh_seq : {len(rows)} gènes x {len(cols)} échantillons")
    print("Ordre des colonnes TSV == titres matrice :",
          cols == titles)
    print("Valeurs 13 gènes : NaN=%d" % sum(
        int(np.isnan(v).sum()) for g in V4_GENES + ["KRAS"]
        for v in [np.array(rows[g])] if g in rows))

    # ---- 3. Sélection FF primaires + regroupement par tumeur ----
    ff_pi = []   # (titre, code, index_colonne)
    for i, t in enumerate(cols):
        m = re.match(r"S\d+\.FF\.Pi\.(.+)$", t)
        if m:
            ff_pi.append((t, m.group(1), i))
    kinds = Counter()
    for t in cols:
        m = re.match(r"S\d+\.(FF|FNA|FFPE)\.(Pi|PDX)\.", t)
        kinds[(m.group(2), m.group(1))] += 1
    print("Colonnes par (kind, type) :", dict(kinds))
    print(f"Colonnes FF primaires : {len(ff_pi)}")
    codes = Counter(c for _, c, _ in ff_pi)
    print(f"Codes-tumeurs distincts (FF primaires) : {len(codes)}")
    print("Codes à réplicats FF :",
          {c: n for c, n in codes.items() if n > 1})

    # ---- 4. Portes d'acceptation (protocole §5) ----
    gates = []
    gates.append(("plateforme GPL18573", platform == "GPL18573"))
    gates.append(("KRAS présent", "KRAS" in rows))
    gates.append(("12 gènes v4 présents (1 ligne chacun)",
                  all(g in rows for g in V4_GENES)))
    gates.append(("aucun code-barres TCGA dans les titres",
                  all(re.match(r"^S\d+\.", t) for t in cols)))
    need = ["KRAS"] + V4_GENES
    # Matrice gène x code-tumeur (médiane des réplicats FF).
    code_list = sorted(codes)
    mat = {}
    for g in need:
        vals = rows[g]
        mat[g] = [float(np.median([vals[i] for _, cc, i in ff_pi
                                   if cc == code]))
                  for code in code_list]
    df = pd.DataFrame(mat, index=code_list)
    n_cc = int(df.dropna().shape[0])
    gates.append(("tumeurs indépendantes >= 40", len(code_list) >= 40))
    gates.append(("cas complets >= 40", n_cc >= 40))
    print(f"Cas complets (KRAS + 12 gènes) : {n_cc} / {len(code_list)}")
    for name, ok in gates:
        print(f"PORTE {'OK ' if ok else 'ÉCHEC'} : {name}")
    if not all(ok for _, ok in gates):
        print("COHORTE INUTILISABLE selon le protocole §5 — arrêt, "
              "aucun CSV écrit, aucun run lancé.", file=sys.stderr)
        return 1

    # ---- 5. Variante (a) : les 12 gènes v4, ordre KRAS ----
    df = df.dropna()
    order = df["KRAS"].sort_values(ascending=True).index
    flux = df.loc[order, V4_GENES]
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_874_yeh_ff_fluxes.csv"
    out.to_csv(out_path, index=False)
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_874_yeh_ff_fluxes_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes) SHA {sha(out_path)}")
    print(f"Écrit : {nul_path} SHA {sha(nul_path)}")
    print("KRAS (valeurs fournies, allure TPM/FPKM) : min=%.4g "
          "médiane=%.4g max=%.4g" % (
              float(df["KRAS"].min()), float(df["KRAS"].median()),
              float(df["KRAS"].max())))
    print("Codes-tumeurs retenus :", ", ".join(order.tolist()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
