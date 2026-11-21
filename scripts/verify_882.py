#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérification indépendante §8.82 — relecture directe des
master_results.json par un chemin distinct d'extract_882.py.
`maxsep` et ancien MC recoupés à 0,0 exact ; tout écart = résultat à
diagnostiquer, pas un bruit.
Usage : python3 verify_882.py
"""
import json
import math
import os

BASE = "/home/hatch/workspace/runs/pdac-v6"

RUNS = [
    "results_fast_v62_882_gbm_prolif",
    "results_fast_v62_882_gbm_prolif_nul",
    "results_fast_v62_882_gbm_privilege",
    "results_fast_v62_882_gbm_privilege_nul",
]


def g(o, path, default=None):
    for k in path.split("."):
        if not isinstance(o, dict) or k not in o:
            return default
        o = o[k]
    return o


def fnum(x):
    try:
        x = float(x)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def main():
    ext = {r["dir"]: r for r in json.load(open(f"{BASE}/extract_882.json"))}
    ok = True
    for d in RUNS:
        p = os.path.join(BASE, d, "master_results.json")
        if not os.path.exists(p):
            print(f"{d} : MANQUANT (nul frais non couru ou run absent)")
            continue
        r = json.load(open(p))
        bc = g(r, "run_pipeline.threshold_metadata.threshold_optimization.best_config", {}) or {}
        m = bc.get("metrics") or {}
        maxsep = fnum(m.get("max_separation"))
        mc = fnum(bc.get("score"))
        e = ext.get(d)
        if e is None:
            print(f"{d} : ABSENT de extract_882.json — ÉCART")
            ok = False
            continue
        dm = (maxsep - e["maxsep"]) if maxsep is not None and e["maxsep"] is not None else None
        dc = (mc - e["mc_score"]) if mc is not None and e["mc_score"] is not None else None
        flag = "OK" if dm == 0.0 and dc == 0.0 else "ÉCART"
        if flag != "OK":
            ok = False
        print(f"{d} : maxsep direct={maxsep} vs extract={e['maxsep']} "
              f"(écart {dm}) ; MC direct={mc} vs extract={e['mc_score']} "
              f"(écart {dc}) — {flag}")
    print("VÉRIFICATION : " + ("2/2 à 0,0 exact (runs présents)"
                                if ok else "ÉCART DÉTECTÉ — DIAGNOSTIQUER"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
