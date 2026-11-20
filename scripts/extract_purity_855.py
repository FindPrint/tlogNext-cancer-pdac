#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extraction §8.55 — 6 runs v6.2 (pureté -> immunitaire, CD8A résidualisé).
Miroir de extract_immrot_848.py : mêmes champs lus dans master_results.json
(best_config.metrics : max_separation, stability ; S_sep = produit).
Prédictions (gelées AVANT les runs, depuis T1'/T2' du jour) :
  E-ABS : d_pred +0,6659 | E-RES : d_pred +0,5960.
  Substitution gelée (protocole §7) : ESTIMATE publiée non obtenue -> 4 runs.
Référence CD8A brut IMMROT (§8.44, relue en machine) : écart +0,9838.
"""
import hashlib
import json
import os

import pandas as pd

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
    for line in open(os.path.join(BASE, "manifest_v62_purity_855.txt")):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, inp, out = line.split("|")
        manifest.append((name, inp, out))
    assert len(manifest) == 4, f"manifeste: {len(manifest)} lignes, attendu 4"
    shas = json.load(open(os.path.join(BASE, "purity_855_csv_sha.json")))
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
    by = {r["nom"]: r for r in rows}
    paires = [
        ("PURITY855_EABS", "PURITY855_EABS_NUL", "E-ABS ABSOLUTE->immunitaire", 0.6659),
        ("PURITY855_ERES", "PURITY855_ERES_NUL", "E-RES CD8A resid(ABSOLUTE)->immunitaire resid", 0.5960),
    ]
    out_pairs = []
    for a, b, label, pred in paires:
        ra, rb = by[a], by[b]
        ecart = ra["ssep"] - rb["ssep"]
        out_pairs.append({"label": label, "ssep_reel": ra["ssep"],
                          "ssep_nul": rb["ssep"], "ecart": ecart,
                          "maxsep_reel": ra["maxsep"], "maxsep_nul": rb["maxsep"],
                          "d_pred": pred, "mc_reel": ra["mc"], "mc_nul": rb["mc"],
                          "delta_reel": ra["delta"], "delta_nul": rb["delta"]})
        print(f"{label}: S_sep réel {ra['ssep']:.4f} / nul {rb['ssep']:.4f} "
              f"écart {ecart:+.4f} (prédit {pred:+.4f}) "
              f"(maxsep {ra['maxsep']:.4f}/{rb['maxsep']:.4f})")
    s844 = pd.read_csv(os.path.join(BASE, "ssep_844_rotations.csv"))
    ref = {(r.famille, r.controle): r for r in s844.itertuples()}
    cd8a = ref[("IMMROT", "CD8A")]
    print(f"Référence CD8A brut IMMROT (§8.44) : S_sep réel {cd8a.ssep_R:.4f} / "
          f"nul {cd8a.ssep_N:.4f} écart {cd8a.ssep_R - cd8a.ssep_N:+.4f}")
    out = {"runs": rows, "paires": out_pairs,
           "reference_CD8A_brut": {"ssep_R": float(cd8a.ssep_R),
                                   "ssep_N": float(cd8a.ssep_N),
                                   "ecart": float(cd8a.ssep_R - cd8a.ssep_N)}}
    with open(os.path.join(BASE, "purity_855_runs.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    pd.DataFrame(rows).to_csv(os.path.join(BASE, "purity_855_runs.csv"), index=False)
    print("Écrit : purity_855_runs.json/.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
