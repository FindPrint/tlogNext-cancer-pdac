#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flux §8.70 — confirmation indépendante pour maxsep (C3) sur GSE79668.
Variante (a) [seule] : les 12 mêmes gènes que la v4 TCGA, ordre = KRAS
croissant, sans correction. Cas complets seulement. Nul = lignes
permutées, graine 42 (défaut). Copie adaptée de build_fluxes_869.py
(original intact) ; protocole PROTOCOL_maxsep_gse79668_870.md.

ADAPTATION DOCUMENTÉE (§4.1 du protocole) : la table de la matrice
GSE79668 est VIDE (0 ligne de données — en-tête ID_REF + 51 GSM
seulement). Les valeurs sont dans le fichier supplémentaire de la
SÉRIE ELLE-MÊME, nommé dans l'en-tête de la matrice
(!Series_supplementary_file) : GSE79668_51_tumors_sharedgenecounts.txt.gz
(comptages de transcrits, GENCODE v. 9, 48 956 gènes x 51 échantillons).
Les identifiants de lignes sont de la forme SYMBOLE_ENSG... : le
symbole est le préfixe avant « _ENSG » (extraction mécanique, aucun
mapping de plateforme nécessaire — GPL11154 n'est pas une table
sondes→symboles pour du RNA-seq). Symboles dupliqués : médiane
(règle du projet). Les 13 gènes utiles (12 v4 + KRAS) ont chacun
exactement 1 ligne : aucune agrégation ne les touche.
Jointure échantillons : positionnelle (même ordre dans la matrice et
dans le fichier de comptages), vérifiée : 49/51 radicaux de titres
identiques, les 2 autres ne diffèrent que par un « _T » final dans le
titre de la matrice (T_06_01_A033a_T, T_06_04_A296a_T).
Portes d'acceptation (protocole §5) : KRAS présent, les 12 gènes v4
présents, cas complets >= 40, n >= 40, aucun code-barres TCGA — sinon
sortie 1, message explicite, et AUCUN run n'est lancé.
Usage : python3 build_fluxes_870.py [--nul-seed 42]
"""
import argparse
import gzip
import hashlib
import sys

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"

V4_GENES = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
            "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]

MATRIX = "GSE79668_series_matrix.txt.gz"
COUNTS = "GSE79668_51_tumors_sharedgenecounts.txt.gz"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nul-seed", type=int, default=42)
    args = ap.parse_args()
    seed = args.nul_seed

    # ---- 1. Matrice : en-tête seulement (table vide, 0 ligne) ----
    gsm_order = []
    titles = []
    ch1 = []
    platform = None
    suppl = None
    with gzip.open(f"{DATA}/{MATRIX}", "rt", encoding="utf-8",
                   errors="replace") as f:
        for line in f:
            if line.startswith("!Series_platform_id"):
                platform = line.split("\t")[1].strip().strip('"')
            if line.startswith("!Series_supplementary_file"):
                suppl = line.split("\t")[1].strip().strip('"')
            if line.startswith("!Sample_characteristics_ch1"):
                ch1.append([v.strip('"') for v in
                            line.rstrip("\n").split("\t")[1:]])
            if line.startswith("!Sample_title"):
                titles = [t.strip('"') for t in
                          line.rstrip("\n").split("\t")[1:]]
            if line.startswith("!series_matrix_table_begin"):
                break
    with gzip.open(f"{DATA}/{MATRIX}", "rt", encoding="utf-8",
                   errors="replace") as f:
        hdr = [l for l in f if l.startswith("!series_matrix_table_begin")]
    print(f"Matrice : plateforme {platform} ; fichier supplémentaire "
          f"déclaré : {suppl}")
    # GSM : lus depuis la ligne d'en-tête de la table (ID_REF + GSM)
    with gzip.open(f"{DATA}/{MATRIX}", "rt", encoding="utf-8",
                   errors="replace") as f:
        in_table = False
        n_data_rows = 0
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                in_table = True
                continue
            if line.startswith("!series_matrix_table_end"):
                break
            if in_table:
                if line.startswith('"ID_REF"'):
                    gsm_order = [c.strip('"') for c in
                                 line.rstrip("\n").split("\t")[1:]]
                else:
                    n_data_rows += 1
    print(f"Matrice : {len(gsm_order)} GSM, {n_data_rows} ligne(s) de "
          f"données dans la table (attendue : 0, données dans le "
          f"fichier supplémentaire)")
    print(f"Titres : {len(titles)} ; tous préfixe T_ : "
          f"{all(t.startswith('T_') for t in titles)}")
    joined_ch1 = " | ".join(v for row in ch1 for v in row)
    print("Marqueur 'normal' / 'non-tumoral' dans characteristics_ch1 :",
          ("normal" in joined_ch1.lower()))
    print("Marqueur 'TCGA' dans titres/GSM :",
          ("TCGA" in " ".join(titles + gsm_order)))

    # ---- 2. Comptages : lignes = gènes, colonnes = échantillons ----
    counts = pd.read_csv(f"{DATA}/{COUNTS}", sep="\t", index_col=0)
    print(f"Comptages : {counts.shape[0]} gènes x {counts.shape[1]} "
          f"échantillons")
    print("Valeurs : min=%.1f médiane=%.1f max=%.1f ; NaN=%d" % (
        float(np.nanmin(counts.values)),
        float(np.nanmedian(counts.values)),
        float(np.nanmax(counts.values)),
        int(counts.isna().sum().sum())))
    # Jointure positionnelle, vérifiée mécaniquement
    stems = [t.rsplit("_SL", 1)[0] for t in titles]
    stems_norm = [s[:-2] if s.endswith("_T") else s for s in stems]
    print("Jointure positionnelle : 51/51 colonnes dans le même ordre ; "
          f"radicaux exacts {sum(a == b for a, b in zip(stems, counts.columns))}/51 ; "
          f"après retrait du '_T' final : "
          f"{sum(a == b for a, b in zip(stems_norm, counts.columns))}/51")
    assert len(counts.columns) == len(gsm_order) == len(titles) == 51
    assert stems_norm == list(counts.columns), \
        "jointure échantillons non vérifiée — arrêt"
    counts.columns = gsm_order  # colonnes désormais identifiées par GSM

    # ---- 3. Symboles (préfixe avant _ENSG) -> médiane ----
    syms = counts.index.to_series().str.split("_ENSG").str[0]
    print(f"Symboles extraits : {syms.notna().sum()} / {len(syms)} ; "
          f"symboles dupliqués : {int(syms.duplicated().sum())} "
          f"(agrégation par médiane, règle du projet)")
    genes = counts.copy()
    genes.index = syms
    genes = genes[genes.index.notna()]
    genes = genes.groupby(level=0).median()
    print(f"Après agrégation : {genes.shape[0]} gènes uniques")
    for g in V4_GENES + ["KRAS"]:
        n_rows = int((syms == g).sum())
        print(f"  {g} : {n_rows} ligne(s)")
    print("Gènes v4 présents :",
          [g for g in V4_GENES if g in genes.index])
    print("Gènes v4 absents :",
          [g for g in V4_GENES if g not in genes.index])
    print("KRAS présent :", "KRAS" in genes.index)

    # ---- 4. Portes d'acceptation (protocole §5) ----
    tum = gsm_order  # série de 51 tumeurs uniquement (titres T_*, aucune
    # caractéristique « normal », article Kirby et coll. 2016 : 51 tissus
    # tumoraux réséqués)
    present = [g for g in V4_GENES if g in genes.index]
    need = ["KRAS"] + present
    cc = genes.loc[need].dropna(axis=1) if "KRAS" in genes.index else None
    n_cc = int(cc.shape[1]) if cc is not None else 0
    gates = [
        ("table matrice vide, données dans le fichier supplémentaire "
         "de la série", n_data_rows == 0 and counts.shape[1] == 51),
        ("plateforme GPL11154", platform == "GPL11154"),
        ("n >= 40 tumeurs", len(tum) >= 40),
        ("aucun code-barres TCGA", "TCGA" not in " ".join(titles + gsm_order)),
        ("KRAS présent", "KRAS" in genes.index),
        ("12 gènes v4 présents",
         all(g in genes.index for g in V4_GENES)),
        ("cas complets >= 40", n_cc >= 40),
    ]
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
    out_path = f"{OUT}/pdac_870_geo79668_fluxes.csv"
    out.to_csv(out_path, index=False)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    suffix = "" if seed == 42 else f"_s{seed}"
    nul_path = f"{OUT}/pdac_870_geo79668_fluxes_nul{suffix}.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes) SHA {sha(out_path)}")
    print(f"Écrit : {nul_path} (graine {seed}) SHA {sha(nul_path)}")
    print("KRAS (comptages bruts) : min=%.0f médiane=%.0f max=%.0f" % (
        float(cc.loc["KRAS"].min()), float(cc.loc["KRAS"].median()),
        float(cc.loc["KRAS"].max())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
