#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extraction §8.68 — 8 runs v6.2 (types xCell -> immunitaire, CD8A
résidualisé, type stromal Osteoblast).
Miroir de extract_deconvolution_860.py : mêmes champs lus dans
master_results.json (best_config.metrics : max_separation, stability ;
S_sep = produit).
Prédictions (gelées AVANT les runs, depuis T1/T2/T3 du jour) :
  D-XTOP1 (aDC) : d_pred +0,8654 | D-XTOP2 (DC) : +0,8132
  D-XRES (CD8A résid. sur [1, aDC]) : d_pred +0,5441
  D-XSTROM (Osteoblast) : d_pred +0,6473.
Références : CD8A brut IMMROT (§8.44, relu en machine) : écart +0,9838 ;
I-RES §8.54 (relu en machine) : écart +0,1982 ; E-RES §8.55 : +0,6499 ;
D-RES §8.60 (relu en machine) : écart +0,7692.
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
    for line in open(os.path.join(BASE, "manifest_v62_xcell_868.txt")):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, inp, out = line.split("|")
        manifest.append((name, inp, out))
    assert len(manifest) == 8, f"manifeste: {len(manifest)} lignes, attendu 8"
    shas = json.load(open(os.path.join(BASE, "xcell_868_csv_sha.json")))
    rows = []
    for name, inp, out in manifest:
        got = sha(os.path.join(BASE, inp))
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
        ("XCELL868_DXTOP1", "XCELL868_DXTOP1_NUL",
         "D-XTOP1 aDC->immunitaire", 0.8654),
        ("XCELL868_DXTOP2", "XCELL868_DXTOP2_NUL",
         "D-XTOP2 DC->immunitaire", 0.8132),
        ("XCELL868_DXRES", "XCELL868_DXRES_NUL",
         "D-XRES CD8A resid->immunitaire resid", 0.5441),
        ("XCELL868_DXSTROM", "XCELL868_DXSTROM_NUL",
         "D-XSTROM Osteoblast->immunitaire", 0.6473),
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
    i854 = json.load(open(os.path.join(BASE, "infiltration_854_runs.json")))
    ires = [p for p in i854["paires"] if p["label"].startswith("I-RES")][0]
    print(f"Référence I-RES §8.54 : S_sep réel {ires['ssep_reel']:.4f} / "
          f"nul {ires['ssep_nul']:.4f} écart {ires['ecart']:+.4f}")
    e855 = json.load(open(os.path.join(BASE, "purity_855_runs.json")))
    eres = [p for p in e855["paires"] if p["label"].startswith("E-RES")][0]
    print(f"Référence E-RES §8.55 : S_sep réel {eres['ssep_reel']:.4f} / "
          f"nul {eres['ssep_nul']:.4f} écart {eres['ecart']:+.4f}")
    d860 = json.load(open(os.path.join(BASE, "deconvolution_860_runs.json")))
    dres = [p for p in d860["paires"] if p["label"].startswith("D-RES")][0]
    print(f"Référence D-RES §8.60 : S_sep réel {dres['ssep_reel']:.4f} / "
          f"nul {dres['ssep_nul']:.4f} écart {dres['ecart']:+.4f}")
    out = {"runs": rows, "paires": out_pairs,
           "reference_CD8A_brut": {"ssep_R": float(cd8a.ssep_R),
                                   "ssep_N": float(cd8a.ssep_N),
                                   "ecart": float(cd8a.ssep_R - cd8a.ssep_N)},
           "reference_IRES_854": {"ssep_R": float(ires["ssep_reel"]),
                                  "ssep_N": float(ires["ssep_nul"]),
                                  "ecart": float(ires["ecart"])},
           "reference_ERES_855": {"ssep_R": float(eres["ssep_reel"]),
                                  "ssep_N": float(eres["ssep_nul"]),
                                  "ecart": float(eres["ecart"])},
           "reference_DRES_860": {"ssep_R": float(dres["ssep_reel"]),
                                  "ssep_N": float(dres["ssep_nul"]),
                                  "ecart": float(dres["ecart"])}}
    with open(os.path.join(BASE, "xcell_868_runs.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    pd.DataFrame(rows).to_csv(os.path.join(BASE, "xcell_868_runs.csv"), index=False)
    print("Écrit : xcell_868_runs.json/.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
