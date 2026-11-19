#!/usr/bin/env python3
"""Lecture des 96 rotations v6.1 (17-18 nov. 2026) — v3, clés vérifiées sur un JSON.
Sorties : v61_rotations_extract.csv + v61_rotations_verified.md (dans runs/pdac-v6).
Clés réelles :
- cascade : five_threshold_cascade.T_-2_F2_pre_onset / T_-1_F1_pre_inflection /
  T_0_Monte_Carlo_Central / T_+1_F1_post_deceleration / T_+2_F2_post_attractor,
  + max_F1_velocity / max_F2_curvature
- MC : run_pipeline.threshold_metadata.threshold_optimization.best_config.score
  et metrics {max_separation, s_norm, stability, robustness, sharpness}
- Delta : reading_synthesis.Delta_tension
- L7a : prediction_levels.L7a_coherence.consensus_direction / global_confidence
- falsification : holographic_tension_state.falsification_vs_null.delta_vs_null
  (comparaison interne d_crit vs SpectralDimension — PAS une comparaison au nul
  permuté, malgré le nom de la clé ; cf. §8.31)
Aucun run lancé, aucun fichier modifié."""
import csv, json, os

BASE = os.path.dirname(os.path.abspath(__file__))

def load(outdir):
    with open(os.path.join(outdir, "master_results.json")) as f:
        return json.load(f)

def get(o, *keys):
    for k in keys:
        if isinstance(o, dict) and k in o:
            o = o[k]
        else:
            return None
    return o

CASC = ["T_-2_F2_pre_onset", "T_-1_F1_pre_inflection", "T_0_Monte_Carlo_Central",
        "T_+1_F1_post_deceleration", "T_+2_F2_post_attractor"]

rows = []
for line in open(os.path.join(BASE, "manifest_v61_rotations.txt")):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    name, inp, out = line.split("|")
    j = load(os.path.join(BASE, out))
    casc = j.get("five_threshold_cascade") or {}
    bc = get(j, "run_pipeline", "threshold_metadata", "threshold_optimization", "best_config") or {}
    met = bc.get("metrics") or {}
    l7a = get(j, "prediction_levels", "L7a_coherence") or {}
    fals = get(j, "holographic_tension_state", "falsification_vs_null") or {}
    rows.append(dict(
        name=name, input=inp, out=out,
        T_m2=casc.get(CASC[0]), T_m1=casc.get(CASC[1]), T_0=casc.get(CASC[2]),
        T_p1=casc.get(CASC[3]), T_p2=casc.get(CASC[4]),
        max_F1=casc.get("max_F1_velocity"), max_F2=casc.get("max_F2_curvature"),
        MC=bc.get("score"), MC_threshold=bc.get("threshold"),
        MC_separation=met.get("max_separation"), MC_s_norm=met.get("s_norm"),
        MC_stability=met.get("stability"), MC_robustness=met.get("robustness"),
        MC_sharpness=met.get("sharpness"),
        Delta=get(j, "reading_synthesis", "Delta_tension"),
        L7a_dir=l7a.get("consensus_direction"), L7a_conf=l7a.get("global_confidence"),
        fals=fals.get("delta_vs_null"),
    ))

with open(os.path.join(BASE, "v61_rotations_extract.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

pairs = {}
for r in rows:
    base = r["name"].removesuffix("_NUL")
    pairs.setdefault(base, {})["nul" if r["name"].endswith("_NUL") else "real"] = r

def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def f(x, nd=3):
    v = num(x)
    return f"{v:.{nd}f}" if v is not None else "—"

lines = ["# Rotations v6.1 — table vérifiée (96 runs, 48 paires réel/nul)",
         "",
         "Pipeline v6.1, mode fast, 17–18 nov. 2026. MC = best_config.score ;",
         "Delta = reading_synthesis.Delta_tension ; L7a = prediction_levels.L7a_coherence",
         "(direction / confiance) ; fals = delta_vs_null interne (d_crit vs SpectralDimension,",
         "PAS une comparaison au nul permuté). T_0 = T_0_Monte_Carlo_Central (%).",
         ""]
fams = [("V4ROT_", "V4ROT — TCGA v4, ARN tumeurs, n=178"),
        ("DEPMAPROT_", "DEPMAPROT — CRISPR DepMap, lignées, n=45"),
        ("IMMROT_", "IMMROT — immunitaire TCGA, ARN tumeurs, n=178"),
        ("PARPROT_", "PARPROT — réparation de l'ADN TCGA, ARN tumeurs, n=178")]
hdr = "| contrôle | MC réel | MC nul | ΔMC | Delta réel | Delta nul | ΔDelta | T_0 réel | T_0 nul | L7a réel | L7a nul | fals réel | fals nul |"
sep = "|---|---|---|---|---|---|---|---|---|---|---|---|---|"
for fam, title in fams:
    lines += ["", f"## {title}", hdr, sep]
    for base in sorted(p for p in pairs if p.startswith(fam)):
        p = pairs[base]
        r, n = p.get("real", {}), p.get("nul", {})
        dm = (num(r.get("MC")) or 0) - (num(n.get("MC")) or 0)
        dd = (num(r.get("Delta")) or 0) - (num(n.get("Delta")) or 0)
        lines.append(f"| {base[len(fam):]} | {f(r.get('MC'))} | {f(n.get('MC'))} | {dm:+.3f} | "
                     f"{f(r.get('Delta'))} | {f(n.get('Delta'))} | {dd:+.3f} | {f(r.get('T_0'),1)} | "
                     f"{f(n.get('T_0'),1)} | {r.get('L7a_dir')} {f(r.get('L7a_conf'))} | "
                     f"{n.get('L7a_dir')} {f(n.get('L7a_conf'))} | {f(r.get('fals'))} | {f(n.get('fals'))} |")
open(os.path.join(BASE, "v61_rotations_verified.md"), "w").write("\n".join(lines) + "\n")

for fam, _ in fams:
    dmc, dd, dmc_rob = [], [], []
    for base in sorted(p for p in pairs if p.startswith(fam)):
        p = pairs[base]
        r, n = p.get("real", {}), p.get("nul", {})
        if num(r.get("MC")) is not None and num(n.get("MC")) is not None:
            dmc.append(num(r["MC"]) - num(n["MC"]))
            dmc_rob.append((num(r.get("MC_robustness")) or 0) - (num(n.get("MC_robustness")) or 0))
        if num(r.get("Delta")) is not None and num(n.get("Delta")) is not None:
            dd.append(num(r["Delta"]) - num(n["Delta"]))
    print(fam, "dMC mean=%.3f max=%.3f min=%.3f pos=%d/%d" % (
        sum(dmc)/len(dmc), max(dmc), min(dmc), sum(1 for x in dmc if x > 0), len(dmc)),
        "dDelta mean=%.3f max=%.3f min=%.3f pos=%d/%d" % (
        sum(dd)/len(dd), max(dd), min(dd), sum(1 for x in dd if x > 0), len(dd)))
print("total rows:", len(rows))
# top gaps
allp = []
for base, p in pairs.items():
    r, n = p.get("real", {}), p.get("nul", {})
    if num(r.get("MC")) is not None and num(n.get("MC")) is not None:
        allp.append((num(r["MC"]) - num(n["MC"]), base, "MC"))
    if num(r.get("Delta")) is not None and num(n.get("Delta")) is not None:
        allp.append((num(r["Delta"]) - num(n["Delta"]), base, "Delta"))
allp.sort(reverse=True)
print("Top 10 écarts réel-nul :")
for v, b, k in allp[:10]:
    print(f"  {k} {b} {v:+.3f}")
print("Bottom 5 :")
for v, b, k in allp[-5:]:
    print(f"  {k} {b} {v:+.3f}")
