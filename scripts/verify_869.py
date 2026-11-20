#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérification indépendante §8.69 — second calcul, chemin de code
distinct de extract_869.py (pas de réutilisation de extract_858.extract)
: relecture directe des 2 master_results.json par json.load + descente
manuelle, comparaison à extract_869.json à 0,0 exact sur maxsep et
ancien MC. Tout écart = résultat à diagnostiquer, pas un bruit.
Usage : python3 verify_869.py [--tag geo57495|geo62165]
Sortie : maxsep_869_verify.json (+ résumé stdout).
"""
import argparse
import json
import math
import os
import sys

PDAC = os.path.dirname(os.path.abspath(__file__))


def fnum(x):
    try:
        x = float(x)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def read_pair(d):
    with open(os.path.join(PDAC, d, "master_results.json")) as f:
        r = json.load(f)
    bc = (r["run_pipeline"]["threshold_metadata"]
          ["threshold_optimization"]["best_config"])
    return {
        "dir": d,
        "version": r.get("version"),
        "maxsep": fnum(bc["metrics"]["max_separation"]),
        "mc_score": fnum(bc["score"]),
        "stability": fnum(bc["metrics"]["stability"]),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", choices=["geo57495", "geo62165", "geo21501"],
                    default="geo57495")
    args = ap.parse_args()
    with open(os.path.join(PDAC, "extract_869.json")) as f:
        table = json.load(f)
    table = [r for r in table if r["paire"] == args.tag]
    out = {"tag": args.tag, "comparaisons": [], "ecart_max": 0.0,
           "verdict": None}
    for row in table:
        d = row["dir"]
        direct = read_pair(d)
        comp = {"dir": d}
        for k in ("maxsep", "mc_score", "stability"):
            a, b = row.get(k), direct[k]
            ecart = None if a is None or b is None else abs(a - b)
            comp[f"ecart_{k}"] = ecart
            if ecart is not None:
                out["ecart_max"] = max(out["ecart_max"], ecart)
        comp["version_extraction"] = row.get("version")
        comp["version_relecture"] = direct["version"]
        out["comparaisons"].append(comp)
    out["n_compares"] = len(out["comparaisons"])
    out["verdict"] = ("OK" if out["n_compares"] == 2
                      and out["ecart_max"] == 0.0 else "ÉCART")
    with open(os.path.join(PDAC, "maxsep_869_verify.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out["verdict"] == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
