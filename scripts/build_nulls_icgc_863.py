#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.63 (D) — Construction de 10 nuls ICGC frais (aucun run).
Même méthode que build_nulls_n70_853.py : rng = default_rng(graine),
perm = rng.permutation(n), lignes entières permutées (les 12 flux d'une
tumeur voyagent ensemble), colonne step inchangée. Graines NOUVELLES
(§8.47 : 1–3, 42 ; §8.53 : 11–30) : ICGC 31–40.
Entrée vérifiée par SHA avant construction contre
nulls_n70_853_verify.json (ICGC réel
10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc).
Sortie : nulls_icgc_863_files.json (SHA-256 de chaque fichier).
Protocole gelé : PROTOCOL_mechanisms_863.md.
"""
import hashlib
import json

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
SEEDS = range(31, 41)
ATTENDU = ("10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    src = f"{PDAC}/pdac_immune_icgc_fluxes.csv"
    sha_src = sha(src)
    assert sha_src == ATTENDU, f"SHA entrée non conforme : {sha_src}"
    print(f"Entrée vérifiée : {src} SHA {sha_src[:12]}…")
    df = pd.read_csv(src)
    files = {}
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        perm = rng.permutation(len(df))
        nul = df.copy()
        nul.iloc[:, 1:] = df.iloc[:, 1:].to_numpy()[perm]
        assert (nul["step"].values == df["step"].values).all()
        cols = [c for c in df.columns if c != "step"]
        assert sorted(map(tuple, nul[cols].values.tolist())) == sorted(
            map(tuple, df[cols].values.tolist()))
        out = f"{PDAC}/pdac_immune_icgc_fluxes_nul_s{seed}.csv"
        nul.to_csv(out, index=False)
        files[out.split("/")[-1]] = sha(out)
        print(f"[icgc s{seed}] {out.split('/')[-1]} "
              f"SHA {files[out.split('/')[-1]][:12]}…")
    with open(f"{PDAC}/nulls_icgc_863_files.json", "w") as f:
        json.dump({"fichiers": files, "n_fichiers": len(files),
                   "sha_entree": sha_src}, f, indent=2, ensure_ascii=False)
    print(f"écrit: nulls_icgc_863_files.json ({len(files)} fichiers)")


if __name__ == "__main__":
    main()
