#!/usr/bin/env python3
"""Lecture flux par flux des 3 pistes réel/nul du lot étendu v6.1 (17 nov. 2026).

Lecture SEULE des sorties existantes du pipeline v6.1 (aucun run lancé, aucun CSV modifié).
Pour chaque paire (réel + nul) : V4R_PURITY, V4R_CLDN18, IMMUNE_TCGA.

Ce qui vient DU PIPELINE (master_results.json, transition_analysis.json, noise_diagnostic.json) :
  - cascade T_-2..T_+2 (%) et seuil MC (best_config) + composantes du score MC ;
  - F1/F2 avant/après seuil : transition_analysis.<estimateur>.Tous
    (first_derivative_pre / first_derivative, second_derivative_pre / second_derivative,
     order_pre -> order, sign_change) ;
  - test de bruit : noise_diagnostic.json (verdict, score moyen, top proxies / bruit blanc).
Ce qui est APPORTÉ par ce script (harnais, hors pipeline) :
  - lecture par flux autour de chaque seuil (z global, fenêtres ±W, d de Cohen) —
    même méthode que per_flux_reading.py, fonctions réimplémentées à l'identique ici ;
  - ordre de réaction des estimateurs : sur df_feat.csv (trajectoires d'estimateurs
    produites par le pipeline le long du scan), pour chaque estimateur, médiane entre
    flux des trajectoires z-scorées, puis position (Progress %) du max |F1| (gradient).
    C'est une lecture de harnais, pas une sortie native du pipeline.
  - pas de seuil = round(pct/100*(n-1)) (vérifié : 59,91 % -> 106 = control_value_raw).
Sortie : pistes_v61_flux_reading.md (+ impression).
"""
import json
import os

import numpy as np
import pandas as pd

PDAC = os.path.dirname(os.path.abspath(__file__))
PAIRS = {
    "V4R_PURITY": ("pdac_tcga_fluxes_v4r_purity.csv", "results_fast_v61_v4r_purity"),
    "V4R_PURITY_NUL": ("pdac_tcga_fluxes_v4r_purity_nul.csv", "results_fast_v61_v4r_purity_nul"),
    "V4R_CLDN18": ("pdac_tcga_fluxes_v4r_cldn18.csv", "results_fast_v61_v4r_cldn18"),
    "V4R_CLDN18_NUL": ("pdac_tcga_fluxes_v4r_cldn18_nul.csv", "results_fast_v61_v4r_cldn18_nul"),
    "IMMUNE_TCGA": ("pdac_immune_tcga_fluxes.csv", "results_fast_v61_immune_tcga"),
    "IMMUNE_TCGA_NUL": ("pdac_immune_tcga_fluxes_nul.csv", "results_fast_v61_immune_tcga_nul"),
}
CK = ["T_-2_F2_pre_onset", "T_-1_F1_pre_inflection", "T_0_Monte_Carlo_Central",
      "T_+1_F1_post_deceleration", "T_+2_F2_post_attractor"]
W = 20


def cohen_d(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    sp = np.sqrt(((len(a) - 1) * np.var(a, ddof=1) + (len(b) - 1) * np.var(b, ddof=1)) / (len(a) + len(b) - 2))
    return float((b.mean() - a.mean()) / sp) if sp > 0 else float("nan")


def reaction_order(df_feat, fluxes):
    prog = df_feat["Progress"].to_numpy(float)
    ests = sorted({c.split("_", 1)[1].rsplit("_", 1)[0] for c in df_feat.columns
                   if c.endswith("_mean") and c.split("_", 1)[0] in fluxes})
    out = []
    for e in ests:
        cols = [f"{f}_{e}_mean" for f in fluxes if f"{f}_{e}_mean" in df_feat.columns]
        zs = []
        for c in cols:
            v = df_feat[c].to_numpy(float)
            s = np.nanstd(v)
            if np.isfinite(s) and s > 0:
                zs.append((v - np.nanmean(v)) / s)
        if not zs:
            continue
        med = np.nanmedian(np.vstack(zs), axis=0)
        if not np.all(np.isfinite(med)):
            continue
        f1 = np.gradient(med, prog)
        inner = (prog >= 10) & (prog <= 90)  # bords du scan exclus (effets de bord, 1re lecture)
        if not inner.any() or not np.any(np.abs(f1[inner]) > 0):
            continue
        idx = np.where(inner)[0]
        i = int(idx[np.nanargmax(np.abs(f1[inner]))])
        out.append((e, float(prog[i]), float(f1[i])))
    return sorted(out, key=lambda t: t[1])


def main():
    lines = ["# Lecture flux par flux — 3 pistes du lot étendu v6.1 (17 nov. 2026)", "",
             "Lecture seule des sorties v6.1 ; méthode et partage pipeline/harnais : voir l'en-tête du script.", ""]
    for name, (csvf, out) in PAIRS.items():
        j = json.load(open(os.path.join(PDAC, out, "master_results.json")))
        df = pd.read_csv(os.path.join(PDAC, csvf))
        ctrl = df.columns[0]
        fl = list(df.columns[1:])
        n = len(df)
        casc = [j["five_threshold_cascade"][k] for k in CK]
        bc = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
        steps = {k.split("_")[0] + "_" + k.split("_")[1]: round(p / 100 * (n - 1)) for k, p in zip(CK, casc)}
        steps["MC"] = round(bc["threshold"] / 100 * (n - 1))
        lines.append(f"## {name} — contrôle `{ctrl}`, n={n}, fichier `{csvf}`")
        lines.append(f"- Cascade % : {' / '.join(f'{x:.2f}' for x in casc)} → pas {[steps[k] for k in list(steps)[:5]]} ; "
                     f"MC seuil {bc['threshold']:.2f} % (pas {steps['MC']}), score {bc['score']:.4f} = "
                     + ", ".join(f"{k} {v:.3f}" for k, v in bc["metrics"].items()))
        z = {c: (df[c].to_numpy(float) - df[c].mean()) / df[c].std(ddof=1) for c in fl}
        for lab, st in steps.items():
            if lab in ("T_+2",) and steps["T_+2"] == steps["T_+1"]:
                continue
            b = slice(max(0, st - W), st); a = slice(st, min(n, st + W))
            ds = sorted(((c, cohen_d(z[c][b], z[c][a])) for c in fl), key=lambda t: -abs(t[1]) if np.isfinite(t[1]) else 0)
            top = [f"{c} {d:+.2f}" for c, d in ds if np.isfinite(d) and abs(d) >= 0.5]
            lines.append(f"- Seuil {lab} (pas {st}, fenêtres {b.stop - b.start}/{a.stop - a.start} pts) — flux |d| ≥ 0,5 : "
                         + (", ".join(top) if top else "aucun") + f" | max |d| : {ds[0][0]} {ds[0][1]:+.2f}")
        # bruit
        nd = json.load(open(os.path.join(PDAC, out, "noise_diagnostic.json")))
        tp = [f"{d.get('flux_name')} {d.get('variance_proxy_score')}" for d in (nd.get("top_proxies") or [])][:3]
        bn = [f"{d.get('flux_name')} {d.get('variance_proxy_score')}" for d in (nd.get("bottom_noise") or [])][:3]
        lines.append(f"- Test de bruit (pipeline) : verdict {nd.get('verdict_level')} — « {nd.get('diagnostic_label')} » ; "
                     f"score moyen {nd.get('avg_variance_proxy_score'):.3f} (min {nd.get('min_variance_proxy_score')}, max {nd.get('max_variance_proxy_score')}) ; "
                     f"top proxies {tp} ; plus proches du bruit blanc {bn}")
        # F1/F2 du pipeline autour du seuil
        ta = json.load(open(os.path.join(PDAC, out, "transition_analysis.json")))
        sc = []; ordch = 0; tot = 0; wp = None
        for e, v in ta.items():
            t = (v or {}).get("Tous") or {}
            if t.get("status") != "success":
                continue
            tot += 1
            wp = t.get("window_pre")
            if t.get("sign_change"):
                sc.append(e)
            if t.get("order_pre") != t.get("order"):
                ordch += 1
        f1pre = np.nanmedian([abs(v["Tous"]["first_derivative_pre"]) for v in ta.values() if v and v.get("Tous", {}).get("status") == "success"])
        f1post = np.nanmedian([abs(v["Tous"]["first_derivative"]) for v in ta.values() if v and v.get("Tous", {}).get("status") == "success"])
        f2pre = np.nanmedian([abs(v["Tous"]["second_derivative_pre"]) for v in ta.values() if v and v.get("Tous", {}).get("status") == "success"])
        f2post = np.nanmedian([abs(v["Tous"]["second_derivative"]) for v in ta.values() if v and v.get("Tous", {}).get("status") == "success"])
        lines.append(f"- F1/F2 (pipeline, `transition_analysis` « Tous », fenêtre avant {wp}) : {tot} estimateurs ; "
                     f"médiane |F1| avant {f1pre:.2e} → après {f1post:.2e} (×{f1post / f1pre:.2f}) ; "
                     f"médiane |F2| avant {f2pre:.2e} → après {f2post:.2e} (×{f2post / f2pre:.2f}) ; "
                     f"changement de signe de F1 : {len(sc)}/{tot} ({', '.join(sc[:8])}{'…' if len(sc) > 8 else ''}) ; "
                     f"changement d'ordre 1er/2nd : {ordch}/{tot}")
        # ordre de réaction
        dfe = pd.read_csv(os.path.join(PDAC, out, "df_feat.csv"))
        ro = reaction_order(dfe, fl)
        first = ", ".join(f"{e} {p:.1f} %" for e, p, _ in ro[:6])
        pos = np.array([p for _, p, _ in ro])
        lines.append(f"- Ordre de réaction (harnais, df_feat, max |F1| par estimateur) : {len(ro)} estimateurs ; "
                     f"premiers : {first} ; médiane des positions {np.median(pos):.1f} % ; "
                     f"quartiles {np.percentile(pos, 25):.1f}–{np.percentile(pos, 75):.1f} %")
        lines.append("")
    txt = "\n".join(lines) + "\n"
    open(os.path.join(PDAC, "pistes_v61_flux_reading.md"), "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
