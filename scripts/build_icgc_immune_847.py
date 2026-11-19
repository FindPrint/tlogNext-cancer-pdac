#!/usr/bin/env python3
"""§8.47 (d) — Construction des fichiers du lot de confirmation pipeline.
Même méthode que build_fluxes_immune.py : rng = default_rng(graine),
perm = rng.permutation(n), lignes entières permutées (les 12 flux d'une
tumeur voyagent ensemble), colonne step inchangée. Aucun run ici.
Fichiers produits :
- pdac_immune_icgc_fluxes_nul_s1/s2/s3.csv (graines 1, 2, 3)
- pdac_immune_geo62452_fluxes_nul_s1/s2.csv (graines 1, 2)
- pdac_immune_tcga_fluxes_nul_s1/s2.csv (graines 1, 2)
- pdac_immune_icgc_fluxes_10g.csv / _10g_nul.csv (sans IFNG/CD19,
  donc sans PRF1/MS4A1 en ICGC)
- pdac_immune_tcga_fluxes_10g.csv / _10g_nul.csv (sans IFNG/CD19)
Sortie : icgc_immune_inversion_confirm_files.json (SHA-256 de chaque fichier).
Protocole gelé : PROTOCOL_icgc_immune_inversion.md
  SHA b55283eeb7a24e30b52ee6a8f24de8a77b3c7b53072d8b837fab9eb08a61eb34
  (+ addendum §9, SHA f1a5a37c0b8ce452b4d00a9d2a649ac41384e076dcb80839389eac728988379c)
"""
import hashlib
import json

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build_nul(cohorte, seed):
    src = f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv"
    df = pd.read_csv(src)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(df))
    nul = df.copy()
    nul.iloc[:, 1:] = df.iloc[:, 1:].to_numpy()[perm]
    out = f"{PDAC}/pdac_immune_{cohorte}_fluxes_nul_s{seed}.csv"
    nul.to_csv(out, index=False)
    return out


def build_10g(cohorte, side):
    src = (f"{PDAC}/pdac_immune_{cohorte}_fluxes.csv" if side == "reel"
           else f"{PDAC}/pdac_immune_{cohorte}_fluxes_nul.csv")
    df = pd.read_csv(src)
    drop = {"icgc": ["PRF1", "MS4A1"], "tcga": ["IFNG", "CD19"]}[cohorte]
    keep = [c for c in df.columns if c not in drop]
    assert len(keep) == 11, keep  # step + 10 flux
    out = (f"{PDAC}/pdac_immune_{cohorte}_fluxes_10g.csv" if side == "reel"
           else f"{PDAC}/pdac_immune_{cohorte}_fluxes_10g_nul.csv")
    df[keep].to_csv(out, index=False)
    return out


def main():
    rec = {"fichiers": {}}
    for cohorte, seeds in (("icgc", [1, 2, 3]), ("geo62452", [1, 2]),
                           ("tcga", [1, 2])):
        for seed in seeds:
            p = build_nul(cohorte, seed)
            rec["fichiers"][p.split("/")[-1]] = sha(p)
            print(f"nul {cohorte} graine {seed}: {p.split('/')[-1]} "
                  f"SHA {rec['fichiers'][p.split('/')[-1]][:12]}…")
    for cohorte in ("icgc", "tcga"):
        for side in ("reel", "nul42"):
            p = build_10g(cohorte, side)
            rec["fichiers"][p.split("/")[-1]] = sha(p)
            print(f"10g {cohorte} {side}: {p.split('/')[-1]} "
                  f"SHA {rec['fichiers'][p.split('/')[-1]][:12]}…")
    with open(f"{PDAC}/icgc_immune_inversion_confirm_files.json", "w") as f:
        json.dump(rec, f, indent=2, ensure_ascii=False)
    print("écrit: icgc_immune_inversion_confirm_files.json")


if __name__ == "__main__":
    main()
