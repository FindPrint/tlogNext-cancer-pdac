#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.54 — Extraction des données ESTIMATE en texte clair (étape ponctuelle).
À lancer avec le venv /tmp/venv854/bin/python (parseur `rdata`).
Lit les .rda du tarball CRAN tidyestimate 1.1.1 (SHA vérifié avant) et écrit :
  - infiltration_854_gene_sets.csv (141 stromal + 141 immune, en clair)
  - infiltration_854_common_genes.csv (symboles HGNC uniques, 10 391)
  - infiltration_854_ov_test.csv (matrice de test `ov`, 17 256 x 10, en clair)
Les scripts d'analyse ensuite n'utilisent que ces CSV (numpy/pandas/scipy).
"""
import hashlib
import sys

import pandas as pd
import rdata

BASE = "/home/hatch/workspace/runs/pdac-v6"
D = f"{BASE}/data_infiltration_854"
TARBALL_SHA = "cc747f787b6548a62219f3388ff6d93ad93cfcb60fe75f322fd712f41509514b"
GENESETS_SHA = "5d058439aed4f074b49d623c5bc4ebfbaceab79766249dd87f280c62d1c0469a"
COMMON_SHA = "f09453b2f12808b0dad73847390593cfee31142eb7490aa81e9d59aa0cba2ff3"
OV_SHA = "3fe246dbf5c9e1fd73c2a4d094e72d415d06b0018589be9dea341efa572b7478"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    assert sha(f"{D}/tidyestimate_1.1.1.tar.gz") == TARBALL_SHA, "SHA tarball non conforme"
    assert sha(f"{D}/tidyestimate/data/gene_sets.rda") == GENESETS_SHA, "SHA gene_sets non conforme"
    assert sha(f"{D}/tidyestimate/data/common_genes.rda") == COMMON_SHA, "SHA common_genes non conforme"
    assert sha(f"{D}/tidyestimate/data/ov.rda") == OV_SHA, "SHA ov non conforme"
    print("SHA : 4/4 conformes.")

    gs = rdata.read_rda(f"{D}/tidyestimate/data/gene_sets.rda")["gene_sets"]
    assert gs.shape == (141, 2), f"gene_sets inattendu : {gs.shape}"
    assert gs["stromal_signature"].nunique() == 141
    assert gs["immune_signature"].nunique() == 141
    assert len(set(gs["stromal_signature"]) & set(gs["immune_signature"])) == 0
    gs.to_csv(f"{BASE}/infiltration_854_gene_sets.csv", index=False)
    print("gene_sets : 141 stromal + 141 immune, disjoints, écrits.")

    cg = rdata.read_rda(f"{D}/tidyestimate/data/common_genes.rda")["common_genes"]
    symbols = sorted(set(cg["hgnc_symbol"].astype(str)))
    print(f"common_genes : {len(cg)} lignes, {len(symbols)} symboles uniques.")
    pd.DataFrame({"hgnc_symbol": symbols}).to_csv(
        f"{BASE}/infiltration_854_common_genes.csv", index=False)
    cg.to_csv(f"{BASE}/infiltration_854_common_genes_full.csv", index=False)
    print("common_genes_full : table complète 3 colonnes écrite.")

    ov = rdata.read_rda(f"{D}/tidyestimate/data/ov.rda")["ov"]
    dims = ov.dims
    coords = {d: list(ov.coords[d].values) for d in dims}
    print("ov dims :", dims, "shapes :", {d: len(v) for d, v in coords.items()})
    # dim_0 = gènes (symboles), dim_1 = échantillons (s516...)
    genes = [str(x) for x in coords[dims[0]]]
    samples = [str(x) for x in coords[dims[1]]]
    import numpy as np
    arr = np.asarray(ov.values, dtype=float)
    assert arr.shape == (len(genes), len(samples)), arr.shape
    df = pd.DataFrame(arr, index=genes, columns=samples)
    df.index.name = "gene"
    df.to_csv(f"{BASE}/infiltration_854_ov_test.csv")
    print(f"ov : {df.shape[0]} gènes x {df.shape[1]} échantillons, écrit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
