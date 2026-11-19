#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extraction §8.48 — 8 runs v6.2 (permutation partielle + croisés inter-familles).
Miroir de extract_ssep_844_rotations.py : mêmes champs lus dans
master_results.json (best_config.metrics : max_separation, stability ;
S_sep = max_separation × stability, PROTOCOL_v6.2.md §3).
Sortie : immrot_848_results.csv/.json. Vérifie les SHA des 8 CSV contre
immrot_848_csv_sha.json et la version v6.2.0 sur les 8 runs.
"""
import hashlib
import json
import os

BASE = "/home/hatch/workspace/runs/pdac-v6"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def g(d, path):
    for k in path.split("."):
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def read_run(outdir):
    d = os.path.join(BASE, outdir, "master_results.json")
    if not os.path.exists(d):
        return None, f"absent: {d}"
    j = json.load(open(d))
    try:
        bc = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
        m = bc["metrics"]
        l7a = j["prediction_levels"]["L7a_coherence"]
        conf = float(l7a["global_confidence"])
        direction = str(l7a["consensus_direction"]).lower()
        signed = conf if direction == "up" else (-conf if direction == "down" else 0.0)
        t0 = fnum(g(j, "five_threshold_cascade.T_0_Monte_Carlo_Central"))
        return {
            "version": j.get("version"),
            "n": j["reading_synthesis"]["n_samples"],
            "control": j.get("metadata", {}).get("control"),
            "mc": float(bc["score"]),
            "mc_thr": float(bc["threshold"]),
            "w_size": bc.get("w_size"),
            "n_candidates": bc.get("n_candidates"),
            "maxsep": float(m["max_separation"]),
            "stab": float(m["stability"]),
            "ssep": float(m["max_separation"]) * float(m["stability"]),
            "robustness": float(m["robustness"]),
            "sharpness": float(m["sharpness"]),
            "delta": (None if j["reading_synthesis"]["Delta_tension"] is None
                      else float(j["reading_synthesis"]["Delta_tension"])),
            "l7a_dir": direction, "l7a_conf": conf, "l7a_signed": signed,
            "t0": t0,
        }, None
    except (KeyError, TypeError) as e:
        return None, f"champ manquant dans {d}: {e}"


def main():
    manifest = []
    for line in open(os.path.join(BASE, "manifest_v62_immrot_848.txt")):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, inp, out = line.split("|")
        manifest.append((name, inp, out))
    assert len(manifest) == 8, f"manifeste: {len(manifest)} lignes, attendu 8"
    shas = json.load(open(os.path.join(BASE, "immrot_848_csv_sha.json")))
    rows = []
    for name, inp, out in manifest:
        got = sha(inp)
        exp = shas[os.path.basename(inp)]
        assert got == exp, f"SHA MISMATCH {inp}: {got} != {exp}"
        r, err = read_run(out)
        assert r is not None, err
        assert r["version"] == "v6.2.0-L7aL7b-CohenD-short", \
            f"{out}: version {r['version']}"
        r["nom"] = name
        r["entree"] = os.path.basename(inp)
        r["sortie"] = out
        rows.append(r)
        print(f"{name}: S_sep={r['ssep']:.4f} maxsep={r['maxsep']:.4f} "
              f"MC={r['mc']:.4f} Delta={r['delta']} w={r['w_size']} "
              f"version={r['version']}")
    # écarts par paire
    by = {r["nom"]: r for r in rows}
    paires = [
        ("IMMROT848_XFAM_CD8A_OVER_PARP", "IMMROT848_XFAM_CD8A_OVER_PARP_NUL", "X1 CD8A→PARP"),
        ("IMMROT848_XFAM_POLQ_OVER_IMMUNE", "IMMROT848_XFAM_POLQ_OVER_IMMUNE_NUL", "X2 POLQ→IMMUNE"),
    ]
    for a, b, label in paires:
        ra, rb = by[a], by[b]
        print(f"{label}: S_sep réel {ra['ssep']:.4f} / nul {rb['ssep']:.4f} "
              f"écart {ra['ssep'] - rb['ssep']:+.4f} "
              f"(maxsep {ra['maxsep']:.4f}/{rb['maxsep']:.4f})")
    # dose–réponse (références §8.44 relues dans ssep_844_rotations.csv)
    import pandas as pd
    s844 = pd.read_csv(os.path.join(BASE, "ssep_844_rotations.csv"))
    ref = {(r.famille, r.controle): r for r in s844.itertuples()}
    dose = [
        ("CD8A", "IMMROT848_IMMUNE_TCGA_FLUXES_IMMROT_CD8A_PP50",
         ref[("IMMROT", "CD8A")], 0.50),
        ("CD8A", "IMMROT848_IMMUNE_TCGA_FLUXES_IMMROT_CD8A_PP25",
         ref[("IMMROT", "CD8A")], 0.25),
        ("CD68", "IMMROT848_IMMUNE_TCGA_FLUXES_IMMROT_CD68_PP50",
         ref[("IMMROT", "CD68")], 0.50),
    ]
    for ctrl, nom, r844, q in dose:
        rp = by[nom]
        print(f"Dose {ctrl} q={q}: S_sep réel {r844.ssep_R:.4f} -> "
              f"partiel {rp['ssep']:.4f} -> nul {r844.ssep_N:.4f} "
              f"(écart partiel-nul {rp['ssep'] - r844.ssep_N:+.4f})")
    # CLDN18 : référence §8.41 (avec doublon) et §8.44 (sans doublon, v6.1)
    cldn = by["IMMROT848_TCGA_FLUXES_V4R_CLDN18_PP50"]
    r844_cldn = ref[("V4ROT", "CLDN18")]
    print(f"Dose CLDN18 q=0.5: S_sep réel sans doublon {r844_cldn.ssep_R:.4f} -> "
          f"partiel {cldn['ssep']:.4f} -> nul {r844_cldn.ssep_N:.4f} "
          f"(écart partiel-nul {cldn['ssep'] - r844_cldn.ssep_N:+.4f})")
    out = {"runs": rows,
           "paires_xfam": [
               {"label": label,
                "ssep_reel": by[a]["ssep"], "ssep_nul": by[b]["ssep"],
                "ecart": by[a]["ssep"] - by[b]["ssep"],
                "maxsep_reel": by[a]["maxsep"], "maxsep_nul": by[b]["maxsep"]}
               for a, b, label in paires]}
    with open(os.path.join(BASE, "immrot_848_results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    pd.DataFrame(rows).to_csv(os.path.join(BASE, "immrot_848_results.csv"),
                              index=False)
    print("Écrit : immrot_848_results.csv/.json (8/8 runs, version v6.2.0)")


if __name__ == "__main__":
    main()
