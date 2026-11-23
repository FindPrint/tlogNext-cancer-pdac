#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agregateur de fin de lot — lot suivant §8.93 (200 nuls frais par paire).
Lit les master_results.json des nuls frais (graines 9101-9110 du lot §8.93
+ graines 9111-9300 du lot suivant, pistes locale et GitHub), extrait le
maxsep de chaque nul, et juge chaque paire contre la distribution de ses
200 nuls selon la regle GELEE §8.93 §4 :
  SOLIDE si reel > p95 des nuls ET >= 95 % des nuls sous le plancher
    (ecart reel - nul > 0,07 contre >= 95 % des nuls) ;
  FRAGILE si reel > mediane mais <= p95, ou 50-95 % sous le plancher ;
  NON si reel <= mediane ou < 50 % sous le plancher.
Le maxsep reel de chaque paire est repris de nulls_dist_893_table.json
(§8.93) — aucune valeur re-saisie a la main.
Dossiers des nuls 9111-9300 : lus dans nulls_lot_next/ledger.csv (seule
source de verite ; piste GitHub = results_fast_gha_893_*, piste locale =
results_fast_v62_893_*). Dossiers des nuls 9101-9110 : results_fast_v62_893_*.
Sorties : nulls_lot_next/nulls_lot_next_table.json et .csv.
Usage : python3 analyse_lot_next.py [--check]  (--check = inventaire seul,
sans verdicts : compte les nuls trouves et liste les graines manquantes).
"""
import csv
import json
import os
import sys

PDAC = "/home/hatch/workspace/runs/pdac-v6"
LOT = os.path.join(PDAC, "nulls_lot_next")
TABLE_893 = os.path.join(PDAC, "nulls_dist_893_table.json")
PLANCHER = 0.07

# slug du registre -> cle de la table §8.93
ALIAS = {
    "depmap": "DEPMAP", "gdc_organoid": "GDC_ORGANOID",
    "geo21501": "GSE21501", "geo57495": "GSE57495",
    "geo60979": "GSE60979", "geo62452": "GSE62452",
    "geo71729": "GSE71729", "geo79668": "GSE79668",
    "gse194249": "GSE194249", "hp35": "HP35", "icgc": "ICGC",
    "immune_tcga": "IMMUNE_TCGA", "parp_tcga": "PARP_TCGA",
    "tcga_v4": "TCGA_v4", "yeh_ff": "GSE131050_YehFF",
}


def read_maxsep(master_path):
    """maxsep du best_config d'un master_results.json (meme chemin que
    replica_nulls_893.read_best_config)."""
    with open(master_path) as f:
        j = json.load(f)
    bc = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
    return float(bc["metrics"]["max_separation"])


def quantile(vals, p):
    v = sorted(vals)
    n = len(v)
    if n == 1:
        return v[0]
    pos = p * (n - 1)
    lo = int(pos)
    hi = min(lo + 1, n - 1)
    frac = pos - lo
    return v[lo] * (1 - frac) + v[hi] * frac


def juger(reel, p95, med, pct):
    """Verdict gelee §8.93 §4 (plancher 0,07)."""
    if reel > p95 and pct >= 95.0:
        return "SOLIDE"
    if reel <= med or pct < 50.0:
        return "NON"
    return "FRAGILE"


def main():
    check_only = "--check" in sys.argv
    table893 = json.load(open(TABLE_893))["table"]

    # Dossiers des nuls 9111-9300, depuis le registre (seule source de verite).
    dirs = {}  # (slug, graine) -> dossier relatif a PDAC
    with open(os.path.join(LOT, "ledger.csv")) as f:
        for r in csv.DictReader(f):
            dirs[(r["paire"], int(r["graine"]))] = r["dossier_sortie"]

    rows = []
    for slug in sorted(ALIAS):
        key = ALIAS[slug]
        reel = float(table893[key]["maxsep_reel"])
        vals = {}
        manquantes = []
        for graine in range(9101, 9301):
            if graine <= 9110:
                d = "results_fast_v62_893_%s_nul_s%d" % (slug, graine)
            else:
                d = dirs.get((slug, graine))
            p = os.path.join(PDAC, d, "master_results.json") if d else None
            if p and os.path.isfile(p):
                try:
                    vals[graine] = read_maxsep(p)
                except Exception as e:
                    manquantes.append((graine, "lecture: %s" % e))
            else:
                manquantes.append((graine, "dossier absent"))
        n = len(vals)
        v = sorted(vals.values())
        row = {"paire": key, "slug": slug, "maxsep_reel": reel,
               "n_nuls_trouves": n, "n_nuls_attendus": 200,
               "graines_manquantes": [g for g, _ in manquantes]}
        if n:
            row.update({
                "mediane_nuls": round(float(quantile(v, 0.5)), 4),
                "p95_nuls": round(float(quantile(v, 0.95)), 4),
                "min_nuls": round(min(v), 4), "max_nuls": round(max(v), 4),
                "n_nuls_sous_reel": sum(1 for x in v if x < reel),
                "rang_reel_sur_%d" % (n + 1): sum(1 for x in v if x < reel) + 1,
                "pct_nuls_sous_plancher": round(
                    100.0 * sum(1 for x in v if reel - x > PLANCHER) / n, 1),
                "d_maxsep_vs_mediane": round(reel - float(quantile(v, 0.5)), 4),
            })
        if not check_only and n == 200:
            row["verdict"] = juger(reel, row["p95_nuls"],
                                   row["mediane_nuls"],
                                   row["pct_nuls_sous_plancher"])
        rows.append(row)

    out_json = os.path.join(LOT, "nulls_lot_next_table.json")
    out_csv = os.path.join(LOT, "nulls_lot_next_table.csv")
    with open(out_json, "w") as f:
        json.dump({"plancher": PLANCHER, "regle": "gelee §8.93 §4",
                   "table": rows}, f, indent=1, ensure_ascii=False)
    champs = ["paire", "slug", "maxsep_reel", "n_nuls_trouves",
              "n_nuls_attendus", "mediane_nuls", "p95_nuls", "min_nuls",
              "max_nuls", "n_nuls_sous_reel", "pct_nuls_sous_plancher",
              "d_maxsep_vs_mediane", "verdict", "graines_manquantes"]
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            rr = dict(r)
            rr["graines_manquantes"] = ";".join(str(g) for g in r["graines_manquantes"])
            rr["n_nuls_sous_reel"] = r.get("n_nuls_sous_reel", "")
            w.writerow(rr)

    total = sum(r["n_nuls_trouves"] for r in rows)
    print("Nuls trouves : %d / 3000 (200 x 15 paires)" % total)
    for r in rows:
        extra = ""
        if r.get("verdict"):
            extra = " -> %s (reel %.4f, p95 %.4f, %s %% sous plancher)" % (
                r["verdict"], r["maxsep_reel"], r["p95_nuls"],
                r["pct_nuls_sous_plancher"])
        print("%-16s %3d/200%s" % (r["paire"], r["n_nuls_trouves"], extra))
        if r["graines_manquantes"] and not check_only:
            print("   manquantes : %s" % r["graines_manquantes"][:20])
    if not check_only:
        solides = [r["paire"] for r in rows if r.get("verdict") == "SOLIDE"]
        print("A2-distrib (200 nuls) : %d/15 SOLIDES : %s"
              % (len(solides), ", ".join(solides) if solides else "aucun"))
    print("Ecrit : %s et %s" % (out_json, out_csv))


if __name__ == "__main__":
    main()
