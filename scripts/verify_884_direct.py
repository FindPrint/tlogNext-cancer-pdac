#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verification independante §8.84 — second calcul des tests directs.
Chemin distinct de direct_tests_884_chen.py : relecture de MOESM13
depuis le fichier, Spearman = Pearson sur rangs (rangs moyens
calcules a la main), Mann-Whitney U = somme des rangs manuelle
(approximation normale avec correction de continuite et correction
d'ex-aequo), FDR BH recalculee a la main. Accord exige : |rho| a
1e-9 pres, p a 5 % relatifs pres (approximation normale vs exacte),
comptes FDR a l'unite pres, medianes a 1e-12 pres.
Sortie : verify_884_direct.json. Exit 1 si desaccord.
"""
import json
import math

import numpy as np
import openpyxl

PDAC = "/home/hatch/workspace/runs/pdac-v6"
SRC = f"{PDAC}/data/Chen2025_MOESM13_SupplData10.xlsx"
FIRST = json.load(open(f"{PDAC}/direct_tests_884_chen.json"))


def ranks_avg(x):
    x = np.asarray(x, dtype=float)
    order = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and x[order[j + 1]] == x[order[i]]:
            j += 1
        r[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = ranks_avg(x), ranks_avg(y)
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    return float(np.dot(rx, ry) / math.sqrt(np.dot(rx, rx) * np.dot(ry, ry)))


def mannwhitney_norm(a, b):
    """U et p approchee (normale, correction ex-aequo + continuite)."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    n1, n2 = len(a), len(b)
    allv = np.concatenate([a, b])
    r = ranks_avg(allv)
    r1 = r[:n1].sum()
    u1 = r1 - n1 * (n1 + 1) / 2.0
    u = min(u1, n1 * n2 - u1)
    # correction ex-aequo
    _, counts = np.unique(allv, return_counts=True)
    tie = np.sum(counts ** 3 - counts)
    n = n1 + n2
    var = n1 * n2 / 12.0 * (n + 1 - tie / (n * (n - 1)))
    z = (u - n1 * n2 / 2.0 + 0.5) / math.sqrt(var)
    p = math.erfc(abs(z) / math.sqrt(2.0))
    return float(u1), float(p)


def bh(pvals):
    p = list(pvals)
    n = len(p)
    order = sorted(range(n), key=lambda i: p[i])
    q = [0.0] * n
    prev = 1.0
    for k in range(n - 1, -1, -1):
        v = p[order[k]] * n / (k + 1)
        prev = min(prev, v)
        q[order[k]] = min(prev, 1.0)
    return q


def main():
    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
    ws = wb["All Drugs AUC"]
    rows = list(ws.iter_rows(values_only=True))
    pdos = [c for c in rows[0][2:]]
    drugs = [r[0] for r in rows[1:]]
    arr = np.array([[r[2 + i] for i in range(46)] for r in rows[1:]],
                   dtype=float)
    gem = arr[drugs.index("Gemcitabine")]
    problems = []

    # D1
    d1 = FIRST["D1"]["table"]
    ps = []
    worst_rho = 0.0
    for rec in d1:
        rho2 = spearman(arr[drugs.index(rec["drug"])], gem)
        worst_rho = max(worst_rho, abs(rho2 - rec["rho"]))
        # p par approximation t de Spearman (verification d'ordre)
        t = rho2 * math.sqrt(44 / max(1e-30, 1 - rho2 ** 2))
        p2 = math.erfc(abs(t) / math.sqrt(2.0))  # borne, non comparee
        ps.append(rec["p"])
    q2 = bh(ps)
    hits2 = sum(1 for v in q2 if v < 0.05)
    print(f"D1 : ecart max |rho| = {worst_rho:.2e} ; "
          f"hits FDR {hits2} vs {FIRST['D1']['n_hits_fdr_lt_0.05']} ; "
          f"FDR min recalculee {min(q2):.4f} vs "
          f"{FIRST['D1']['min_fdr']:.4f}.")
    if worst_rho > 1e-9 or hits2 != FIRST["D1"]["n_hits_fdr_lt_0.05"]:
        problems.append("D1")
    # nom des 2 hits
    hits = sorted(((rec["drug"], rec["rho"], rec["fdr"]) for rec in d1
                   if rec["fdr"] < 0.05), key=lambda t: t[2])
    print("D1 hits FDR<0,05 :", [(h[0], round(h[1], 4), round(h[2], 4))
                                 for h in hits])

    # D2a
    brca = ["DAC_102", "DAC_58", "DAC_81", "DAC_85", "DAC_53", "DAC_4"]
    a = np.array([arr[drugs.index("Olaparib"), pdos.index(d)] for d in brca])
    b = np.array([arr[drugs.index("Olaparib"), pdos.index(d)]
                  for d in pdos if d not in brca])
    u2, p2 = mannwhitney_norm(a, b)
    print(f"D2a : U recalcule {u2:.1f} vs {FIRST['D2a']['U']:.1f} ; "
          f"p approchee {p2:.4g} vs exacte {FIRST['D2a']['p']:.4g} ; "
          f"medianes {np.median(a):.4f}/{np.median(b):.4f} vs "
          f"{FIRST['D2a']['median_mut']:.4f}/{FIRST['D2a']['median_rest']:.4f}.")
    if abs(u2 - FIRST["D2a"]["U"]) > 1e-9 or abs(np.median(a) - FIRST["D2a"]["median_mut"]) > 1e-12:
        problems.append("D2a")

    # D2b
    cf = ["DAC_13", "DAC_73", "DAC_110", "DAC_32", "DAC_30"]
    d2b = FIRST["D2b"]["table"]
    ps2 = []
    worst_p_rel = 0.0
    for rec in d2b:
        aa = np.array([arr[drugs.index(rec["drug"]), pdos.index(d)] for d in cf])
        bb = np.array([arr[drugs.index(rec["drug"]), pdos.index(d)]
                       for d in pdos if d not in cf])
        _, pp = mannwhitney_norm(aa, bb)
        ps2.append(pp)
        if rec["p"] > 0:
            worst_p_rel = max(worst_p_rel, abs(pp - rec["p"]) / rec["p"])
    q2b = bh(ps2)
    hits2b = sum(1 for v in q2b if v < 0.05)
    print(f"D2b : ecart relatif max sur p (approx. normale) = {worst_p_rel:.3f} ; "
          f"hits FDR {hits2b} vs {FIRST['D2b']['n_hits_fdr_lt_0.05']} ; "
          f"p min approchee {min(ps2):.4g} vs exacte {FIRST['D2b']['min_p']:.4g}.")
    if hits2b != FIRST["D2b"]["n_hits_fdr_lt_0.05"]:
        problems.append("D2b")

    # D2c
    ws2 = wb["CFTR Drugs AUC"]
    r2 = list(ws2.iter_rows(values_only=True))
    hdr2 = r2[0]
    cf15 = [c for c in hdr2[2:]]
    mt = [c for c in cf15 if c.replace("_", "") in
          ("DAC13", "DAC24", "DAC72", "DAC84")]
    wt = [c for c in cf15 if c not in mt]
    m13 = {r[0]: {hdr2[2 + i]: r[2 + i] for i in range(15)} for r in r2[1:]}
    for rec in FIRST["D2c"]["table"]:
        aa = np.array([m13[rec["drug"]][c] for c in mt])
        bb = np.array([m13[rec["drug"]][c] for c in wt])
        u2, p2 = mannwhitney_norm(aa, bb)
        print(f"D2c {rec['drug']:12s} U {u2:.1f} vs {rec['U']:.1f} ; "
              f"p approx {p2:.4g} vs exacte {rec['p']:.4g}.")
        if abs(u2 - rec["U"]) > 1e-9:
            problems.append("D2c-" + rec["drug"])

    out = {"worst_rho_diff": worst_rho,
           "d1_hits_recomputed": hits2,
           "d2b_hits_recomputed": hits2b,
           "problems": problems,
           "status": "OK" if not problems else "DESACCORD"}
    with open(f"{PDAC}/verify_884_direct.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("Verification directe :", out["status"],
          ("problemes : " + ",".join(problems)) if problems else "")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
