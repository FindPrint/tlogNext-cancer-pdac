#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extraction et jugement §8.99 — GSE184585 (11 runs v6.2 fast).

Lit, pour chaque run, master_results.json ->
run_pipeline/threshold_metadata/threshold_optimization/best_config
(metrics : max_separation, s_norm, stability, robustness,
sharpness ; threshold). MC pipeline = 0,3*s_norm + 0,3*stabilité
+ 0,2*robustesse + 0,2*sharpness (formule réplique §8.93,
replica_nulls_893.py ; facteur 0,8 non appliqué : w_size fast 80
>= n//10 = 8). Verdict selon la règle gelée §8.93 §4 (plancher
0,07 ; SOLIDE / FRAGILE / NON) contre la distribution des 10
nuls frais graines 9301-9310.

Tests directs : Spearman de chaque flux vs KRAS (valeurs KRAS
relues depuis la matrice série via le mapping gelé, dans l'ordre
des lignes du CSV réel) ; Δρ médian, nombre de flux positifs.
Usage : python3 extract_899.py
Sortie : extraction_899.json + table imprimée.
"""
import gzip
import hashlib
import json
import sqlite3
import sys

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
DATA = PDAC + "/data"
REAL_CSV = PDAC + "/pdac_899_gse184585_fluxes.csv"
RUNS = {"reel": "results_fast_v62_899_gse184585"}
for s in range(9301, 9311):
    RUNS[f"nul_s{s}"] = f"results_fast_v62_899_gse184585_nul_s{s}"
PLANCHER = 0.07


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_best(d):
    j = json.load(open(f"{PDAC}/{d}/master_results.json"))
    bc = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
    m = bc["metrics"]
    mc = (0.3 * float(m["s_norm"]) + 0.3 * float(m["stability"])
          + 0.2 * float(m["robustness"]) + 0.2 * float(m["sharpness"]))
    return {"maxsep": float(m["max_separation"]),
            "s_norm": float(m["s_norm"]),
            "stabilite": float(m["stability"]),
            "robustesse": float(m["robustness"]),
            "sharpness": float(m["sharpness"]),
            "mc": mc,
            "seuil": float(bc["threshold"]) if bc["threshold"] is not None else None}


def kras_values():
    """Valeurs KRAS des 82 tumeurs, ordre croissant (= ordre du CSV)."""
    hta = sqlite3.connect(f"{DATA}/hta20transcriptcluster.sqlite")
    eg = sqlite3.connect(f"{DATA}/org.Hs.eg.sqlite")
    eg_map = {}
    for sym, gid in eg.execute(
            "SELECT gi.symbol, g.gene_id FROM gene_info gi "
            "JOIN genes g ON g._id = gi._id"):
        eg_map.setdefault(str(gid), sym)
    probes_kras = [p for p, g in hta.execute(
        "SELECT probe_id, gene_id FROM probes") if eg_map.get(str(g)) == "KRAS"]
    assert len(probes_kras) == 1, probes_kras
    mat = pd.read_csv(f"{DATA}/GSE184585_series_matrix.txt.gz",
                      sep="\t", comment="!", index_col=0, low_memory=False)
    mat.index = mat.index.astype(str).str.strip('"')
    mat.columns = [c.strip('"') for c in mat.columns]
    vals = mat.loc[probes_kras[0]].astype(float)
    # Tumeurs = toutes les colonnes (82/82, vérifié à la construction).
    return np.sort(vals.values)


def main():
    rows = {}
    for label, d in RUNS.items():
        rows[label] = read_best(d)
    reel = rows["reel"]
    nuls = np.array([rows[f"nul_s{s}"]["maxsep"] for s in range(9301, 9311)])
    nuls_mc = np.array([rows[f"nul_s{s}"]["mc"] for s in range(9301, 9311)])
    p95 = float(np.percentile(nuls, 95))
    med = float(np.median(nuls))
    pct_plancher = float(100.0 * np.mean((reel["maxsep"] - nuls) > PLANCHER))
    d_med = reel["maxsep"] - med
    d_p95 = reel["maxsep"] - p95
    rang = int(1 + np.sum(nuls < reel["maxsep"]))
    if reel["maxsep"] > p95 and pct_plancher >= 95.0:
        verdict = "SOLIDE"
    elif reel["maxsep"] > med or pct_plancher >= 50.0:
        # FRAGILE si réel > médiane mais ≤ p95, ou 50–95 % sous plancher ;
        # NON si réel ≤ médiane ou < 50 % sous plancher (règle §8.93 §4).
        if reel["maxsep"] > med and pct_plancher >= 50.0:
            verdict = "FRAGILE"
        else:
            verdict = "NON"
    else:
        verdict = "NON"
    # Le cas « réel > p95 mais 50–95 % sous plancher » est FRAGILE
    # (règle §8.93 §4 : FRAGILE si ... ou 50–95 % sous le plancher).
    if reel["maxsep"] > p95 and 50.0 <= pct_plancher < 95.0:
        verdict = "FRAGILE"

    # ---- Tests directs : Spearman flux vs KRAS ----
    df = pd.read_csv(REAL_CSV)
    fluxes = [c for c in df.columns if c != "step"]
    kras = kras_values()
    assert len(kras) == len(df), (len(kras), len(df))
    rhos = {}
    for f in fluxes:
        rhos[f] = float(pd.Series(df[f].values).corr(
            pd.Series(kras), method="spearman"))
    rhov = np.array(list(rhos.values()))
    d_rho_med = float(np.median(rhov))
    n_pos = int(np.sum(rhov > 0))

    out = {"reel": reel, "nuls_maxsep": {f"s{s}": rows[f"nul_s{s}"]["maxsep"]
           for s in range(9301, 9311)},
           "nuls_mc": {f"s{s}": rows[f"nul_s{s}"]["mc"]
           for s in range(9301, 9311)},
           "p95_nuls": p95, "mediane_nuls": med,
           "pct_sous_plancher": pct_plancher,
           "d_contre_mediane": d_med, "d_contre_p95": d_p95,
           "rang_sur_11": rang, "verdict": verdict,
           "spearman_vs_kras": rhos, "delta_rho_median": d_rho_med,
           "n_flux_positifs": n_pos,
           "mc_reel": reel["mc"], "p95_mc_nuls": float(np.percentile(nuls_mc, 95)),
           "mediane_mc_nuls": float(np.median(nuls_mc))}
    with open(f"{PDAC}/extraction_899.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"maxsep réel : {reel['maxsep']:.4f} (seuil {reel['seuil']:.4f})")
    print(f"nuls maxsep : min {nuls.min():.4f} médiane {med:.4f} "
          f"p95 {p95:.4f} max {nuls.max():.4f}")
    print("nuls :", " ".join(f"{v:.4f}" for v in nuls))
    print(f"% nuls sous plancher 0,07 : {pct_plancher:.1f} %")
    print(f"d contre médiane : {d_med:+.4f} ; d contre p95 : {d_p95:+.4f}")
    print(f"rang réel : {rang}/11")
    print(f"MC réel : {reel['mc']:.4f} ; MC nuls médiane "
          f"{out['mediane_mc_nuls']:.4f} p95 {out['p95_mc_nuls']:.4f}")
    print("Spearman vs KRAS :",
          " ".join(f"{k}={v:+.3f}" for k, v in rhos.items()))
    print(f"Δρ médian : {d_rho_med:+.4f} ; flux positifs : {n_pos}/{len(fluxes)}")
    print(f"VERDICT : {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
