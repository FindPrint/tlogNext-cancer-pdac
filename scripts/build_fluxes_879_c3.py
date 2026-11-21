#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flux §8.79 (cohorte #2) — GSE57495, 11 flux (GSTM1 absent).
Variante (a) a 11 flux : les 11 genes v4 presents, ordre = KRAS
croissant, sans correction. Cas complets seulement. Nul = lignes
permutees, graine 42. Copie adaptee de build_fluxes_869.py
(original intact) ; protocole-addendum
PROTOCOL_nouvelle_serie_879_C3.md (apres arret C2, DPCR1 absent
de GENCODE v36 — voir §0 de l'addendum).
Usage : python3 build_fluxes_879_c3.py [--fresh]
  --fresh : construit en plus les nuls frais graines 8791/8792
  (regle gelee §3.5/§6 — seulement si d_maxsep est proche du
  plancher ; ne jamais construire avant d'avoir lu l'extraction).
GSE57495 : 63 tumeurs PDAC, GPL15048, valeurs log2 deposees.
GSTM1 absent (sonde partagee merck-NM_000561_s_at exclue comme
ambigue, §8.69) ; la paire est a 11 flux, pre-enregistre.
Portes d'acceptation (addendum §4) : plateforme GPL15048, KRAS
present, 11 genes v4 presents ET GSTM1 absent, cas complets
>= 40 — sinon sortie 1, message explicite, et AUCUN run
n'est lance.
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
}
EXPECTED_MATRIX_SHA256 = (
    "995dbeff288a14c1cc1a52489e456b7677ede5da8e287069b8298d649b532efc")
EXPECTED_MAPPING_SHA256 = (
    "93e01ec387ab710dfbfe4b7ad960a90c494b131f62637df3a4476fa9f998f952")
EXPECTED_PLATFORM = "GPL15048"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cohort", choices=list(COHORTS), default="57495")
    ap.add_argument("--fresh", action="store_true")
    args = ap.parse_args()
    cfg = COHORTS[args.cohort]
    mpath = f"{DATA}/{cfg['matrix']}"
    if sha(mpath) != EXPECTED_MATRIX_SHA256:
        print("ERREUR : matrice SHA different de l'empreinte gelee.",
              file=sys.stderr)
        return 1
    if sha(f"{DATA}/{cfg['mapping']}") != EXPECTED_MAPPING_SHA256:
        print("ERREUR : mapping SHA different de l'empreinte gelee.",
              file=sys.stderr)
        return 1
    print("Matrice et mapping SHA verifies (empreintes gelees).")

    # ---- 0. Plateforme lue dans l'en-tete ----
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
        print("ERREUR : plateforme != GPL15048 — arret.",
              file=sys.stderr)
        return 1

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
        # 57495 : série de 63 tumeurs PDAC, titres PDAC1..63
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
    present = [g for g in V4_GENES if g in genes.index]
    gates.append(("11 gènes v4 présents (GSTM1 absent)",
                  len(present) == 11 and "GSTM1" not in genes.index))
    gates.append(("GSTM1 absent (porte pre-enregistree)",
                  "GSTM1" not in genes.index))
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

    # ---- 5. Variante (a) : les 11 gènes v4, ordre KRAS ----
    order = cc.loc["KRAS"].sort_values(ascending=True).index
    flux = cc.loc[present, order].T
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_879_{cfg['tag']}_fluxes.csv"
    out.to_csv(out_path, index=False)
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_879_{cfg['tag']}_fluxes_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes) SHA {sha(out_path)}")
    print(f"Écrit : {nul_path} SHA {sha(nul_path)}")
    print("KRAS (valeurs puce) : min=%.2f médiane=%.2f max=%.2f" % (
        float(cc.loc["KRAS"].min()), float(cc.loc["KRAS"].median()),
        float(cc.loc["KRAS"].max())))
    if args.fresh:
        for seed in (8791, 8792):
            r2 = np.random.default_rng(seed)
            perm2 = r2.permutation(len(out))
            nf = out.copy()
            nf.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm2]
            p = (f"{OUT}/pdac_879_{cfg['tag']}_fluxes_nul_s{seed}.csv")
            nf.to_csv(p, index=False)
            print(f"Écrit (nul frais s{seed}) : {p} SHA {sha(p)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
