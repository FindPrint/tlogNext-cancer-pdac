#!/usr/bin/env python3
"""Lecture flux par flux des 96 rotations v6.1 (18 nov. 2026).
Réutilise les fonctions de pistes_v61_flux_reading.py (cohen_d, reaction_order).
Pour chaque paire réel/nul : cascade, MC + composantes, lecture par flux aux seuils
T_0 et MC (fenêtres ±20, d de Cohen), valeur du flux en double (contrôle = flux),
test de bruit, F1/F2 avant/après, ordre de réaction (médiane).
Lecture seule des sorties existantes. Aucun run lancé, aucun CSV modifié."""
import json, os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pistes_v61_flux_reading import cohen_d, reaction_order, CK, W

PDAC = os.path.dirname(os.path.abspath(__file__))
FAMS = {
    "V4ROT": ("pdac_tcga_v4_fluxes_v4rot_{}.csv", "results_fast_v61_v4rot_{}"),
    "DEPMAPROT": ("pdac_depmap_fluxes_depmaprot_{}.csv", "results_fast_v61_depmaprot_{}"),
    "IMMROT": ("pdac_immune_tcga_fluxes_immrot_{}.csv", "results_fast_v61_immrot_{}"),
    "PARPROT": ("pdac_parp_tcga_fluxes_parprot_{}.csv", "results_fast_v61_parprot_{}"),
}
FLUXES = {
    "V4ROT": ["PGC","REG4","CLDN18","MUC17","DPCR1","CR2","KRT20","MUC2","GSTM1","CEACAM5","CLCA1","MUC16"],
    "DEPMAPROT": ["EFR3A","RAB10","CCND1","UROD","CFLAR","DOCK5","MYH9","SCAP","RAB6A","CRKL","MYC","ACO2"],
    "IMMROT": ["CD8A","CD8B","CD4","FOXP3","CD68","CD163","CD274","PDCD1","CTLA4","GZMB","IFNG","CD19"],
    "PARPROT": ["PARP1","PARP2","BRCA1","BRCA2","ATM","ATR","CHEK1","CHEK2","RAD51","XRCC1","POLQ","FANCD2"],
}

def read_pair(fam, ctrl):
    csvpat, outpat = FAMS[fam]
    out = {}
    for suffix in ("", "_nul"):
        tag = ctrl + suffix
        csvf = csvpat.format(tag)
        outd = outpat.format(tag.lower())
        j = json.load(open(os.path.join(PDAC, outd, "master_results.json")))
        df = pd.read_csv(os.path.join(PDAC, csvf))
        n = len(df)
        casc = [j["five_threshold_cascade"][k] for k in CK]
        bc = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
        # flux list: columns after control (col 0); duplicate is col with same base name
        cols = list(df.columns[1:])
        base = [c.split(".")[0] for c in cols]
        dupcol = cols[base.index(ctrl)] if ctrl in base else None
        z = {c: (df[c].to_numpy(float) - df[c].mean()) / df[c].std(ddof=1) for c in cols}
        def at(pct, label):
            st = round(pct / 100 * (n - 1))
            b = slice(max(0, st - W), st); a = slice(st, min(n, st + W))
            ds = sorted(((c, cohen_d(z[c][b], z[c][a])) for c in cols),
                        key=lambda t: -abs(t[1]) if np.isfinite(t[1]) else 0)
            top = [(c, round(d, 2)) for c, d in ds if np.isfinite(d) and abs(d) >= 0.5]
            ddup = None
            if dupcol is not None:
                ddup = round(float(cohen_d(z[dupcol][b], z[dupcol][a])), 2)
            return dict(step=st, top=top, dup_d=ddup, max_d=(ds[0][0], round(ds[0][1], 2)))
        nd = json.load(open(os.path.join(PDAC, outd, "noise_diagnostic.json")))
        ta = json.load(open(os.path.join(PDAC, outd, "transition_analysis.json")))
        ok = [v["Tous"] for v in ta.values() if v and v.get("Tous", {}).get("status") == "success"]
        f1pre = float(np.nanmedian([abs(t["first_derivative_pre"]) for t in ok])) if ok else float("nan")
        f1post = float(np.nanmedian([abs(t["first_derivative"]) for t in ok])) if ok else float("nan")
        f2pre = float(np.nanmedian([abs(t["second_derivative_pre"]) for t in ok])) if ok else float("nan")
        f2post = float(np.nanmedian([abs(t["second_derivative"]) for t in ok])) if ok else float("nan")
        dfe = pd.read_csv(os.path.join(PDAC, outd, "df_feat.csv"))
        ro = reaction_order(dfe, cols)
        pos = np.array([p for _, p, _ in ro]) if ro else np.array([np.nan])
        dvec = (j.get("reading_synthesis") or {}).get("D_vector") or {}
        out[suffix or "real"] = dict(
            casc=[round(x, 2) for x in casc],
            mc=float(bc["score"]), mc_thr=float(bc["threshold"]), mc_met=bc["metrics"],
            delta=float(j["reading_synthesis"]["Delta_tension"]),
            dvec={k: round(float(v), 3) for k, v in dvec.items() if isinstance(v, (int, float))},
            l7a=j["prediction_levels"]["L7a_coherence"]["consensus_direction"],
            l7a_conf=float(j["prediction_levels"]["L7a_coherence"]["global_confidence"]),
            fals=(j.get("holographic_tension_state") or {}).get("falsification_vs_null", {}).get("delta_vs_null"),
            t0=at(casc[2], "T0"), mc_at=at(bc["threshold"], "MC"),
            noise=(nd.get("verdict_level"), nd.get("diagnostic_label"),
                   round(float(nd.get("avg_variance_proxy_score")), 3) if nd.get("avg_variance_proxy_score") is not None else None),
            f1_ratio=round(f1post / f1pre, 2) if f1pre and np.isfinite(f1pre) and f1pre != 0 else None,
            f2_ratio=round(f2post / f2pre, 2) if f2pre and np.isfinite(f2pre) and f2pre != 0 else None,
            react_med=round(float(np.median(pos)), 1) if len(pos) else None,
            react_iqr=(round(float(np.percentile(pos, 25)), 1), round(float(np.percentile(pos, 75)), 1)) if len(pos) else None,
            n_estimators=len(ro),
        )
    return out

results = {}
for fam, fluxes in FLUXES.items():
    for ctrl in fluxes:
        results[f"{fam}_{ctrl}"] = read_pair(fam, ctrl)
        print("fait", fam, ctrl, flush=True)

json.dump(results, open(os.path.join(PDAC, "v61_rotations_flux_reading.json"), "w"), indent=1)

# Compact summary table
lines = ["# Rotations v6.1 — lecture flux par flux (18 nov. 2026)", "",
         "d = Cohen d fenêtres ±20 autour du seuil (z global). « doublon » = d du flux qui est aussi la colonne de contrôle.",
         "F1×/F2× = médiane |F1|/|F2| après ÷ avant (transition_analysis « Tous »). Réact. = médiane des positions de max |F1| des estimateurs (%).",
         ""]
for fam in FLUXES:
    lines += [f"## {fam}", "",
              "| contrôle | MC r/n | Delta r/n | T_0 r (pas) — top flux |d|≥0,5 (réel) | doublon d (réel) | T_0 nul — top | doublon d (nul) | bruit r/n | F1× r/n | F2× r/n | réact. méd. r/n |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for ctrl in FLUXES[fam]:
        r = results[f"{fam}_{ctrl}"]["real"]; n = results[f"{fam}_{ctrl}"]["_nul"]
        def tops(d):
            return ", ".join(f"{c} {v:+.2f}" for c, v in d["top"]) or "aucun"
        lines.append(f"| {ctrl} | {r['mc']:.3f}/{n['mc']:.3f} | {r['delta']:.2f}/{n['delta']:.2f} | "
                     f"{r['t0']['step']} — {tops(r['t0'])} | {r['t0']['dup_d']} | "
                     f"{n['t0']['step']} — {tops(n['t0'])} | {n['t0']['dup_d']} | "
                     f"{r['noise'][0]}/{n['noise'][0]} | {r['f1_ratio']}/{n['f1_ratio']} | "
                     f"{r['f2_ratio']}/{n['f2_ratio']} | {r['react_med']}/{n['react_med']} |")
    lines.append("")
open(os.path.join(PDAC, "v61_rotations_flux_reading.md"), "w").write("\n".join(lines) + "\n")
print("OK")
