#!/usr/bin/env python3
"""§8.96 bras A — Construction des 2 nuls frais LUAD (graines 9601, 9602).
Methode du projet (build_nulls_n70_853.py) : rng = default_rng(graine),
perm = rng.permutation(n), lignes entieres permutees (les 12 flux d'une
tumeur voyagent ensemble), colonne step inchangee. Source :
pdac_luad_fluxes.csv (SHA d407849b...), n=515.
Protocole gele : PROTOCOL_universalite_896.md
"""
import hashlib
import json

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build_nul(seed):
    src = f"{PDAC}/pdac_luad_fluxes.csv"
    df = pd.read_csv(src)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(df))
    nul = df.copy()
    nul.iloc[:, 1:] = df.iloc[:, 1:].to_numpy()[perm]
    assert (nul["step"].values == df["step"].values).all()
    cols = [c for c in df.columns if c != "step"]
    assert sorted(map(tuple, nul[cols].values.tolist())) == sorted(
        map(tuple, df[cols].values.tolist()))
    assert not nul.isna().any().any()
    out = f"{PDAC}/pdac_luad_fluxes_nul_s{seed}.csv"
    nul.to_csv(out, index=False)
    return out


def main():
    files = {}
    for seed in (9601, 9602):
        out = build_nul(seed)
        files[out.split("/")[-1]] = sha(out)
        print(f"[luad s{seed}] {out.split('/')[-1]} SHA {files[out.split('/')[-1]]}")
    with open(f"{PDAC}/luad_896_nulls_files.json", "w") as f:
        json.dump({"fichiers": files, "n_fichiers": len(files)}, f, indent=2, ensure_ascii=False)
    print("ecrit: luad_896_nulls_files.json")


if __name__ == "__main__":
    main()
