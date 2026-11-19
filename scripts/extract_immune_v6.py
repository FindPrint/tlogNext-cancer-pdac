#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrait la cascade, le MC optimum, L7a et Delta des 8 runs v6 immune.
Sources par run : results_fast_immune_<tag>(_nul)/master_results.json
(cascade five_threshold_cascade, Delta holographic_tension_state) et
runs_immune_v6.log (Meilleur score MC, lignes L7a-COHERENCE / L7b).
L7a : le diagnostic de bruit exige 5 bins x 15 points (>= 75) ; à n=69/70
le score est NaN — artefact connu, documenté, jamais lu comme un vote.
Sortie : immune_v6_runs_summary.json + tableau imprimé.
"""
import json
import re

OUT = "/home/hatch/workspace/runs/pdac-v6"
RUNS = [("tcga", False), ("tcga", True), ("geo71729", False), ("geo71729", True),
        ("geo62452", False), ("geo62452", True), ("icgc", False), ("icgc", True)]


def main():
    log = open(f"{OUT}/runs_immune_v6.log", encoding="utf-8").read()
    # Le log concatène les 8 runs dans l'ordre du script : on découpe par
    # "File: pdac_immune_...csv".
    parts = re.split(r"(?=UNIVERSAL_LOG v6\.0\.0-L7aL7b-CohenD — RUNNING MASTER PIPELINE\nFile: )", log)
    mc, l7a = {}, {}
    for p in parts:
        m = re.search(r"File: (pdac_immune_\S+\.csv)", p)
        if not m:
            continue
        fname = m.group(1)
        ms = re.search(r"Meilleur score: ([0-9.]+)", p)
        if ms:
            mc[fname] = float(ms.group(1))
        m7 = re.search(r"L7a-COHERENCE: ([^\n]+)", p)
        if m7:
            l7a[fname] = m7.group(1).strip()
        m7b = re.search(r"L7b-ROBUSTESSE: ([^\n]+)", p)
        if m7b:
            l7a[fname + "|L7b"] = m7b.group(1).strip()
    rows = []
    for tag, is_nul in RUNS:
        suffix = "_nul" if is_nul else ""
        d = f"{OUT}/results_fast_immune_{tag}{suffix}"
        m = json.load(open(f"{d}/master_results.json", encoding="utf-8"))
        casc = m["five_threshold_cascade"]
        delta = m["holographic_tension_state"]["Delta_tension"]
        nd = json.load(open(f"{d}/noise_diagnostic.json", encoding="utf-8"))
        fname = f"pdac_immune_{tag}_fluxes{suffix}.csv"
        rows.append({
            "cohorte": tag, "nul": is_nul, "n": m["metadata"]["control_monotonicity"]["n_valid"],
            "cible_v6": m["metadata"]["target"],
            "T_-2_%": round(casc["T_-2_F2_pre_onset"], 2),
            "T_-1_%": round(casc["T_-1_F1_pre_inflection"], 2),
            "T_0_%": round(casc["T_0_Monte_Carlo_Central"], 2),
            "T_+1_%": round(casc["T_+1_F1_post_deceleration"], 2),
            "T_+2_%": round(casc["T_+2_F2_post_attractor"], 2),
            "MC_optimum": mc.get(fname),
            "Delta": round(float(delta), 3),
            "L7a": l7a.get(fname),
            "L7b": l7a.get(fname + "|L7b"),
            "bruit_status": nd.get("status"),
        })
    with open(f"{OUT}/immune_v6_runs_summary.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"{'cohorte':<10s} {'nul':<5s} {'n':>3s} {'cible':<7s} {'T-2':>6s} {'T-1':>6s} {'T0':>6s} {'T+1':>6s} {'T+2':>6s} {'MC':>6s} {'Delta':>6s}  L7a")
    for r in rows:
        print(f"{r['cohorte']:<10s} {str(r['nul']):<5s} {r['n']:>3d} {r['cible_v6']:<7s} "
              f"{r['T_-2_%']:>6.2f} {r['T_-1_%']:>6.2f} {r['T_0_%']:>6.2f} {r['T_+1_%']:>6.2f} "
              f"{r['T_+2_%']:>6.2f} {r['MC_optimum']:>6.3f} {r['Delta']:>6.3f}  {r['L7a']}")
    print("Écrit : immune_v6_runs_summary.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
