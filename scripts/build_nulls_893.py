#!/usr/bin/env python3
"""§8.93 (§3b/§3c) — Construction des 150 nuls frais pipeline (10 par paire).
Methode du projet (build_nulls_n70_853.py) : rng = default_rng(graine),
perm = rng.permutation(n), lignes entieres permutees (les flux d'une
tumeur voyagent ensemble), colonne de controle inchangee. Graines gelees
(PROTOCOL_nulls_distribution_893.md §3b) : 9101-9110, jamais utilisees.
15 paires : 8 principales (etape 1) + 7 A2 restantes (etape 2).
Sortie : nulls_893_files.json (SHA-256 de chaque fichier).
"""
import hashlib
import json

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
GRAINES = list(range(9101, 9111))

PAIRS = [
    ("HP35", "results_fast_v62_hp35", "results_fast_v62_hp35_nul", 1),
    ("TCGA_v4", "results_fast_v62_tcga_v4", "results_fast_v62_tcga_v4_nul", 1),
    ("GSE71729", "results_fast_v62_geo71729", "results_fast_v62_geo71729_nul", 1),
    ("GSE62452", "results_fast_v62_geo62452", "results_fast_v62_geo62452_nul", 1),
    ("ICGC", "results_fast_v62_icgc", "results_fast_v62_icgc_nul", 1),
    ("IMMUNE_TCGA", "results_fast_v62_immune_tcga", "results_fast_v62_immune_tcga_nul", 1),
    ("PARP_TCGA", "results_fast_v62_parp_tcga", "results_fast_v62_parp_tcga_nul", 1),
    ("DEPMAP", "results_fast_v62_depmap", "results_fast_v62_depmap_nul", 1),
    ("GSE21501", "results_fast_v62_869_geo21501", "results_fast_v62_869_geo21501_nul", 2),
    ("GSE79668", "results_fast_v62_870_geo79668", "results_fast_v62_870_geo79668_nul", 2),
    ("GSE60979", "results_fast_v62_871_geo60979", "results_fast_v62_871_geo60979_nul", 2),
    ("GSE131050_YehFF", "results_fast_v62_874_yeh_ff", "results_fast_v62_874_yeh_ff_nul", 2),
    ("GSE57495", "results_fast_v62_879_geo57495", "results_fast_v62_879_geo57495_nul", 2),
    ("GDC_ORGANOID", "results_fast_v62_885_gdc_organoid", "results_fast_v62_885_gdc_organoid_nul", 2),
    ("GSE194249", "results_fast_v62_888_gse194249", "results_fast_v62_888_gse194249_nul", 2),
]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def csv_reel(nom_dir):
    j = json.load(open(f"{PDAC}/{nom_dir}/master_results.json"))
    return (j.get("metadata") or {}).get("csv_path")


def build_nul(src_path, seed, out_name):
    df = pd.read_csv(src_path)
    control = df.columns[0]
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(df))
    nul = df.copy()
    nul.iloc[:, 1:] = df.iloc[:, 1:].to_numpy()[perm]
    assert (nul[control].values == df[control].values).all()
    cols = [c for c in df.columns if c != control]
    assert sorted(map(tuple, nul[cols].values.tolist())) == sorted(
        map(tuple, df[cols].values.tolist()))
    assert not nul.isna().any().any()
    out = f"{PDAC}/{out_name}"
    nul.to_csv(out, index=False)
    return out


def main():
    files = {}
    for nom, dr, dn, etape in PAIRS:
        src = csv_reel(dr)
        base = src.split("/")[-1][:-4]  # sans .csv
        for seed in GRAINES:
            out_name = f"{base}_nul_s{seed}.csv"
            out = build_nul(src, seed, out_name)
            files[out_name] = sha(out)
        print(f"[{nom} etape {etape}] 10 nuls construits depuis {base}.csv")
    with open(f"{PDAC}/nulls_893_files.json", "w") as f:
        json.dump({"fichiers": files, "n_fichiers": len(files),
                   "graines": GRAINES}, f, indent=2, ensure_ascii=False)
    print(f"ecrit: nulls_893_files.json ({len(files)} fichiers)")


if __name__ == "__main__":
    main()
