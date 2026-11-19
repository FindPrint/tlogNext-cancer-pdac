#!/usr/bin/env python3
"""Lecture des 96 rotations v6.1 (17-18 nov. 2026) — COPIE adaptée de
extract_v61_lot_compare_v2.py. Ne lit que les master_results.json existants.
Sorties : v61_rotations_extract.csv + v61_rotations_verified.md (dans runs/pdac-v6).
Clés lues : prediction_levels.L7a_coherence, reading_synthesis.Delta_tension,
run_pipeline.threshold_metadata.threshold_optimization.best_config (score MC et
composantes), cascade T_-2..T_+2, falsification (delta_vs_null si présent).
Aucun run lancé, aucun fichier modifié."""
import csv, json, os, hashlib

BASE = os.path.dirname(os.path.abspath(__file__))

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]

def get(o, *keys):
    for k in keys:
        if isinstance(o, dict) and k in o:
            o = o[k]
        else:
            return None
    return o

def load(outdir):
    with open(os.path.join(outdir, "master_results.json")) as f:
        return json.load(f)

rows = []
for line in open(os.path.join(BASE, "manifest_v61_rotations.txt")):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    name, inp, out = line.split("|")
    j = load(os.path.join(BASE, out))
    casc = get(j, "cascade") or get(j, "thresholds") or {}
    # cascade may be dict of T_-2..T_+2 or list
    if isinstance(casc, dict):
        t = [casc.get(k) for k in ("T_-2", "T_-1", "T_0", "T_+1", "T_+2")]
    elif isinstance(casc, list):
        t = casc
    else:
        t = [None]*5
    bc = get(j, "run_pipeline", "threshold_metadata", "threshold_optimization", "best_config") or {}
    l7a = get(j, "prediction_levels", "L7a_coherence") or {}
    delta = get(j, "reading_synthesis", "Delta_tension")
    fals = get(j, "falsification") or get(j, "falsification_test") or {}
    if isinstance(fals, dict):
        fals_val = fals.get("delta_vs_null", fals.get("value", fals.get("falsification_delta")))
    else:
        fals_val = fals
    mc = bc.get("score") if isinstance(bc, dict) else None
    comp = bc.get("components") if isinstance(bc, dict) else None
    if not isinstance(comp, dict):
        comp = {}
    rows.append(dict(
        name=name, input=inp, out=out,
        T_m2=t[0], T_m1=t[1], T_0=t[2], T_p1=t[3], T_p2=t[4],
        MC=mc, MC_separation=comp.get("separation"), MC_persistence=comp.get("persistence"),
        MC_robustness=comp.get("robustness"), MC_shape=comp.get("shape"),
        Delta=delta if not isinstance(delta, dict) else delta.get("value"),
        L7a_dir=l7a.get("direction") if isinstance(l7a, dict) else None,
        L7a_conf=l7a.get("confidence") if isinstance(l7a, dict) else None,
        fals=fals_val,
    ))

with open(os.path.join(BASE, "v61_rotations_extract.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# Pair real vs nul
pairs = {}
for r in rows:
    base = r["name"].removesuffix("_NUL")
    pairs.setdefault(base, {})["nul" if r["name"].endswith("_NUL") else "real"] = r

def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

lines = ["# Rotations v6.1 — table vérifiée (96 runs, 48 paires réel/nul)",
         "",
         "Pipeline v6.1, mode fast. Clés : MC = best_config.score ; Delta = reading_synthesis.Delta_tension ;",
         "L7a = prediction_levels.L7a_coherence ; fals = falsification delta_vs_null (si présent).",
         "",
         "## V4ROT — TCGA v4, ARN tumeurs, n=178",
         "| contrôle | MC réel | MC nul | ΔMC | Delta réel | Delta nul | ΔDelta | T_0 réel | T_0 nul | L7a réel | L7a nul | fals réel | fals nul |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
         ]
for base in sorted(p for p in pairs if p.startswith("V4ROT_")):
    p = pairs[base]
    r, n = p.get("real", {}), p.get("nul", {})
    dm = (num(r.get("MC")) or 0) - (num(n.get("MC")) or 0)
    dd = (num(r.get("Delta")) or 0) - (num(n.get("Delta")) or 0)
    lines.append(f"| {base[6:]} | {r.get('MC')} | {n.get('MC')} | {dm:+.3f} | {r.get('Delta')} | {n.get('Delta')} | {dd:+.3f} | {r.get('T_0')} | {n.get('T_0')} | {r.get('L7a_dir')} {r.get('L7a_conf')} | {n.get('L7a_dir')} {n.get('L7a_conf')} | {r.get('fals')} | {n.get('fals')} |")

for fam, title in [("DEPMAPROT_", "DEPMAPROT — CRISPR DepMap, lignées, n=45"),
                   ("IMMROT_", "IMMROT — immunitaire TCGA, ARN tumeurs, n=178"),
                   ("PARPROT_", "PARPROT — réparation de l'ADN TCGA, ARN tumeurs, n=178")]:
    lines += ["", f"## {title}",
              "| contrôle | MC réel | MC nul | ΔMC | Delta réel | Delta nul | ΔDelta | T_0 réel | T_0 nul | L7a réel | L7a nul | fals réel | fals nul |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for base in sorted(p for p in pairs if p.startswith(fam)):
        p = pairs[base]
        r, n = p.get("real", {}), p.get("nul", {})
        dm = (num(r.get("MC")) or 0) - (num(n.get("MC")) or 0)
        dd = (num(r.get("Delta")) or 0) - (num(n.get("Delta")) or 0)
        lines.append(f"| {base[len(fam):]} | {r.get('MC')} | {n.get('MC')} | {dm:+.3f} | {r.get('Delta')} | {n.get('Delta')} | {dd:+.3f} | {r.get('T_0')} | {n.get('T_0')} | {r.get('L7a_dir')} {r.get('L7a_conf')} | {n.get('L7a_dir')} {n.get('L7a_conf')} | {r.get('fals')} | {n.get('fals')} |")

open(os.path.join(BASE, "v61_rotations_verified.md"), "w").write("\n".join(lines) + "\n")

# Summary stats
for fam in ["V4ROT_", "DEPMAPROT_", "IMMROT_", "PARPROT_"]:
    dmc, dd = [], []
    for base in sorted(p for p in pairs if p.startswith(fam)):
        p = pairs[base]
        r, n = p.get("real", {}), p.get("nul", {})
        if num(r.get("MC")) is not None and num(n.get("MC")) is not None:
            dmc.append(num(r["MC"]) - num(n["MC"]))
        if num(r.get("Delta")) is not None and num(n.get("Delta")) is not None:
            dd.append(num(r["Delta"]) - num(n["Delta"]))
    print(fam, "n_pairs=", len(dmc), "dMC mean=%.3f max=%.3f min=%.3f pos=%d" % (
        sum(dmc)/len(dmc), max(dmc), min(dmc), sum(1 for x in dmc if x > 0)) if dmc else "",
        "dDelta mean=%.3f max=%.3f min=%.3f pos=%d" % (
        sum(dd)/len(dd), max(dd), min(dd), sum(1 for x in dd if x > 0)) if dd else "")
print("total rows:", len(rows))
