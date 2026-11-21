#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.75 — Construction de 40 nuls frais (aucun run).
Même méthode que build_nulls_icgc_863.py / build_nulls_n70_853.py :
rng = default_rng(graine), perm = rng.permutation(n), lignes entières
permutées (les 12 flux d'une tumeur voyagent ensemble), colonne step
inchangée. Graines NOUVELLES, jamais utilisées : ICGC 61-90,
GSE62452 31-40 (ICGC existants : 1-3, 11-60 ; GSE existants : 1-2,
11-30). Entrées vérifiées par SHA avant construction contre
nulls_n70_853_verify.json (ICGC réel 10823879…, GSE réel 97c4689a…).
Sortie : nulls_icgc_gse_875_files.json (SHA-256 de chaque fichier).
Protocole gelé : PROTOCOL_m2_cloture_875.md.
"""
import hashlib
import json

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
PLAN = [("icgc", range(61, 91),
         "10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc"),
        ("geo62452", range(31, 41),
         "97c4689a6ecacd0a73a77804200a72a90994d60bea7e6b2c079195acbffd79a3")]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    files = {}
    for cohorte, seeds, attendu in PLAN:
        src = f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv"
        sha_src = sha(src)
        assert sha_src == attendu, f"SHA entrée {cohorte} non conforme : {sha_src}"
        print(f"Entrée vérifiée : {src} SHA {sha_src[:12]}…")
        df = pd.read_csv(src)
        for seed in seeds:
            rng = np.random.default_rng(seed)
            perm = rng.permutation(len(df))
            nul = df.copy()
            nul.iloc[:, 1:] = df.iloc[:, 1:].to_numpy()[perm]
            assert (nul["step"].values == df["step"].values).all()
            cols = [c for c in df.columns if c != "step"]
            assert sorted(map(tuple, nul[cols].values.tolist())) == sorted(
                map(tuple, df[cols].values.tolist()))
            out = f"{PDAC}/pdac_immune_{cohorte}_fluxes_nul_s{seed}.csv"
            nul.to_csv(out, index=False)
            files[out.split("/")[-1]] = sha(out)
            print(f"[{cohorte} s{seed}] {out.split('/')[-1]} "
                  f"SHA {files[out.split('/')[-1]][:12]}…")
    with open(f"{PDAC}/nulls_icgc_gse_875_files.json", "w") as f:
        json.dump({"fichiers": files, "n_fichiers": len(files),
                   "sha_entrees": {c: a for c, _, a in PLAN}},
                  f, indent=2, ensure_ascii=False)
    print(f"écrit: nulls_icgc_gse_875_files.json ({len(files)} fichiers)")


if __name__ == "__main__":
    main()
