#!/usr/bin/env python3
"""§8.53 (c) — Construction des nuls frais (aucun run).
Même méthode que build_icgc_immune_847.py : rng = default_rng(graine),
perm = rng.permutation(n), lignes entières permutées (les 12 flux d'une
tumeur voyagent ensemble), colonne step inchangée. Graines NOUVELLES
(§8.47 : 1–3 et 42) : ICGC 11–30, GSE62452 11–30, TCGA 11–15.
Sortie : nulls_n70_853_files.json (SHA-256 de chaque fichier).
Protocole gelé : PROTOCOL_nulls_n70_853.md
"""
import hashlib
import json

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
PLAN = [("icgc", range(11, 31)), ("geo62452", range(11, 31)),
        ("tcga", range(11, 16))]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build_nul(cohorte, seed):
    src = f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv"
    df = pd.read_csv(src)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(df))
    nul = df.copy()
    nul.iloc[:, 1:] = df.iloc[:, 1:].to_numpy()[perm]
    # vérification : même multi-ensemble de lignes, step inchangé
    assert (nul["step"].values == df["step"].values).all()
    cols = [c for c in df.columns if c != "step"]
    assert sorted(map(tuple, nul[cols].values.tolist())) == sorted(
        map(tuple, df[cols].values.tolist()))
    out = f"{PDAC}/pdac_immune_{cohorte}_fluxes_nul_s{seed}.csv"
    nul.to_csv(out, index=False)
    return out


def main():
    files = {}
    for cohorte, seeds in PLAN:
        for seed in seeds:
            out = build_nul(cohorte, seed)
            files[out.split("/")[-1]] = sha(out)
            print(f"[{cohorte} s{seed}] {out.split('/')[-1]} SHA {files[out.split('/')[-1]][:12]}…")
    with open(f"{PDAC}/nulls_n70_853_files.json", "w") as f:
        json.dump({"fichiers": files, "n_fichiers": len(files)}, f, indent=2, ensure_ascii=False)
    print(f"écrit: nulls_n70_853_files.json ({len(files)} fichiers)")


if __name__ == "__main__":
    main()
