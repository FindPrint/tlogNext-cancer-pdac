#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construction des 10 nuls frais §8.72 — GSE79668.
Invoque build_fluxes_870.py --nul-seed <graine> (original intact) pour
les graines gelées 8721-8730 (PROTOCOL_nulls_gse79668_872.md §2).
Après chaque invocation, vérifie que le CSV réel garde son SHA
7744bc5a82fe80055b5ab9231fc7ae5395354f643b5b7cd1fdfce8aa6656107a
(déterministe : le builder le réécrit à chaque fois) — tout changement
= arrêt, diagnostic, aucun run lancé.
Sortie : nulls_872_files.json (SHA des 10 CSV de nuls + SHA réel).
Usage : python3 build_nulls_872.py
"""
import hashlib
import json
import os
import subprocess
import sys

PDAC = os.path.dirname(os.path.abspath(__file__))
REAL = os.path.join(PDAC, "pdac_870_geo79668_fluxes.csv")
REAL_SHA = ("7744bc5a82fe80055b5ab9231fc7ae5395354f643b5b7cd1fdfce8aa66"
            "56107a")
SEEDS = [8721, 8722, 8723, 8724, 8725, 8726, 8727, 8728, 8729, 8730]
BUILDER = os.path.join(PDAC, "build_fluxes_870.py")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if sha(REAL) != REAL_SHA:
        print(f"CSV réel inattendu AVANT construction : {sha(REAL)} "
              f"!= {REAL_SHA} — arrêt.", file=sys.stderr)
        return 1
    out = {"real_csv": "pdac_870_geo79668_fluxes.csv",
           "real_sha": REAL_SHA, "seeds": SEEDS, "nulls": {}}
    for seed in SEEDS:
        nul_path = os.path.join(
            PDAC, f"pdac_870_geo79668_fluxes_nul_s{seed}.csv")
        r = subprocess.run([sys.executable, BUILDER, "--nul-seed",
                            str(seed)], cwd=PDAC, capture_output=True,
                           text=True)
        if r.returncode != 0:
            print(f"graine {seed} : builder exit {r.returncode}\n"
                  f"{r.stdout}\n{r.stderr}", file=sys.stderr)
            return 1
        if sha(REAL) != REAL_SHA:
            print(f"graine {seed} : CSV réel modifié ({sha(REAL)}) "
                  f"— arrêt, diagnostic.", file=sys.stderr)
            return 1
        if not os.path.exists(nul_path):
            print(f"graine {seed} : CSV nul absent — arrêt.",
                  file=sys.stderr)
            return 1
        out["nulls"][str(seed)] = {
            "file": os.path.basename(nul_path), "sha256": sha(nul_path)}
        print(f"graine {seed} : {os.path.basename(nul_path)} "
              f"SHA {out['nulls'][str(seed)]['sha256'][:8]}… "
              f"(réel inchangé {REAL_SHA[:8]}…)")
    with open(os.path.join(PDAC, "nulls_872_files.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("Écrit : nulls_872_files.json — 10 nuls, réel inchangé.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
