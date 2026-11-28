#!/usr/bin/env python3
"""Construction d'UN nul frais — successeur de build_null_893.py.

Même méthode exacte que le builder gelé §8.93 (SHA-256
572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467) :
  rng = np.random.default_rng(graine)
  perm = rng.permutation(n)
  lignes entières permutées (les flux d'une tumeur voyagent ensemble),
  colonne de contrôle INCHANGÉE.
Mêmes assertions : contrôle inchangé, mêmes lignes (multiset),
0 valeur manquante. Même sortie : le CSV nul, et son SHA-256 sur
stdout ("SHA256 <sha> <fichier>").

SEUL CHANGEMENT (durcissement, audit externe du 27 nov. 2026, §8.1) :
le nom de la colonne de contrôle est EXPLICITE (--control, obligatoire).
build_null_893.py supposait que la première colonne était le contrôle
(`control = df.columns[0]`) ; un CSV réordonné aurait conservé la
mauvaise colonne. Ici le contrôle est nommé, vérifié présent une seule
fois, et la permutation s'applique à toutes les AUTRES colonnes, quelle
que soit sa position. Quand le contrôle est la première colonne, la
sortie est IDENTIQUE octet à octet à build_null_893.py (même graine,
même réel) — non-régression vérifiée sur les nuls s9311/s9312 du lot
§8.101 (SHA 476dbede… / d3c23537… reproduits).

Ce fichier NE REMPLACE PAS build_null_893.py pour les lots en cours :
le lot §8.101 (local + GitHub) utilise le builder gelé §8.93. Ce
builder est destiné aux LOTS FUTURS (protocole à geler avant usage).
Ne pas modifier : toute évolution passe par un nouveau fichier.

Usage :
  python3 build_null_894.py --real <csv reel> --seed <graine> --control <nom> --out <csv nul>
"""
import argparse
import hashlib
import sys

import numpy as np
import pandas as pd


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_nul(src_path, seed, control, out_path):
    df = pd.read_csv(src_path)
    cols = list(df.columns)
    if cols.count(control) != 1:
        raise ValueError(
            f"contrôle {control!r} absent ou non unique dans {src_path} "
            f"(colonnes : {cols})")
    idx = cols.index(control)
    others = [i for i in range(len(cols)) if i != idx]
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(df))
    nul = df.copy()
    nul.iloc[:, others] = df.iloc[:, others].to_numpy()[perm]
    assert (nul[control].values == df[control].values).all()
    other_cols = [c for c in cols if c != control]
    assert sorted(map(tuple, nul[other_cols].values.tolist())) == sorted(
        map(tuple, df[other_cols].values.tolist()))
    assert not nul.isna().any().any()
    nul.to_csv(out_path, index=False)
    return sha(out_path)


def main():
    ap = argparse.ArgumentParser(
        description="Construit un nul frais (successeur de build_null_893.py, contrôle explicite).")
    ap.add_argument("--real", required=True, help="CSV réel d'entrée")
    ap.add_argument("--seed", required=True, type=int, help="Graine (ex. 9111)")
    ap.add_argument("--control", required=True, help="Nom de la colonne de contrôle (ex. step)")
    ap.add_argument("--out", required=True, help="CSV nul de sortie")
    args = ap.parse_args()
    s = build_nul(args.real, args.seed, args.control, args.out)
    print(f"SHA256 {s} {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
