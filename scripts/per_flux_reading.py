#!/usr/bin/env python3
"""Lecture par flux autour d'un seuil (méthode documentée, 16 nov. 2026).

Pour chaque flux d'un CSV ordonné (1re colonne = contrôle, autres = flux) :
- z-score global de la colonne (moyenne / écart-type ddof=1 sur toute la série) ;
- fenêtres de W points avant et après le pas de seuil donné ;
- rapporte : moyenne z avant -> moyenne z après, et d de Cohen entre les
  deux fenêtres (écart-type poolé).
- et le test top-groupe vs reste : les K dernières lignes (groupe fort)
  contre le reste, en d de Cohen par flux.

Usage : python3 per_flux_reading.py <csv> --steps 16,90,376 --window 20 [--topk 12]
Les fenêtres sont coupées aux bords (pas d'imputation, pas d'extension).
Cette méthode est propre à ce script ; les lectures du 15 nov. utilisaient
une autre convention — ne pas comparer les valeurs chiffre à chiffre.
"""
import argparse
import sys

import numpy as np
import pandas as pd


def cohen_d(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    na, nb = len(a), len(b)
    va, vb = np.var(a, ddof=1), np.var(b, ddof=1)
    sp = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    if sp <= 0:
        return float("nan")
    return float((np.mean(b) - np.mean(a)) / sp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--steps", default="")
    ap.add_argument("--window", type=int, default=20)
    ap.add_argument("--topk", type=int, default=12)
    ap.add_argument("--from-start", action="store_true",
                    help="groupe fort = PREMIÈRES lignes (ex. DepMap : Chronos "
                    "croissant = plus dépendant d'abord)")
    args = ap.parse_args()

    df = pd.read_csv(args.csv)
    flux_cols = list(df.columns[1:])
    n = len(df)
    print(f"# {args.csv} : n={n} flux={len(flux_cols)} fenêtre={args.window}")
    z = {}
    for c in flux_cols:
        v = df[c].to_numpy(dtype=float)
        z[c] = (v - np.nanmean(v)) / np.nanstd(v, ddof=1)

    steps = [int(s) for s in args.steps.split(",") if s.strip()] if args.steps else []
    for step in steps:
        w = args.window
        before = slice(max(0, step - w), step)
        after = slice(step, min(n, step + w))
        print(f"## seuil pas {step} (fenêtres [{before.start}:{before.stop}] vs [{after.start}:{after.stop}])")
        for c in flux_cols:
            zb, za = z[c][before], z[c][after]
            d = cohen_d(zb, za)
            print(f"  {c:>10} : z avant {np.mean(zb):+6.2f} -> z après {np.mean(za):+6.2f} | d de Cohen {d:+.2f}")

    k = min(args.topk, n - 1)
    if k >= 3:
        where = "premières" if args.from_start else "dernières"
        print(f"## top-{k} ({where} lignes) contre reste (d de Cohen)")
        for c in flux_cols:
            grp = z[c][:k] if args.from_start else z[c][-k:]
            rest = z[c][k:] if args.from_start else z[c][:-k]
            d = cohen_d(rest, grp)
            print(f"  {c:>10} : d {d:+.2f} (moy z top-{k} {np.mean(grp):+.2f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
