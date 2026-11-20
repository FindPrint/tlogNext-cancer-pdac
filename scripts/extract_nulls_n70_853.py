#!/usr/bin/env python3
"""§8.53 (d) — Extraction des résultats du lot pipeline v6.2.
Lecture seule des master_results.json des 45 runs (results_fast_v62_853_*)
+ des runs §8.47 déjà existants (ICGC s1–s3 + nul42 ; GSE62452 s1–s2 +
nul42 ; TCGA s1–s2 + nul42) pour les distributions pipeline complètes :
ICGC 24 tirages, GSE62452 23, TCGA 8. Percentile de chaque S_sep nul
pipeline dans la distribution répliquée (config nulle, 1000 tirages).
Sortie : nulls_n70_853_confirm.json.
Protocole gelé : PROTOCOL_nulls_n70_853.md
"""
import json
import os

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
PLAN = ([("icgc", s) for s in range(11, 31)]
        + [("geo62452", s) for s in range(11, 31)]
        + [("tcga", s) for s in range(11, 16)])
ANCIENS = {  # runs §8.47 déjà existants (dossier, cohorte, étiquette)
    "results_fast_v62_847_icgc_nul_s1": ("icgc", "s1"),
    "results_fast_v62_847_icgc_nul_s2": ("icgc", "s2"),
    "results_fast_v62_847_icgc_nul_s3": ("icgc", "s3"),
    "results_fast_v62_immune_icgc_nul": ("icgc", "nul42"),
    "results_fast_v62_847_geo62452_nul_s1": ("geo62452", "s1"),
    "results_fast_v62_847_geo62452_nul_s2": ("geo62452", "s2"),
    "results_fast_v62_immune_geo62452_nul": ("geo62452", "nul42"),
    "results_fast_v62_847_tcga_nul_s1": ("tcga", "s1"),
    "results_fast_v62_847_tcga_nul_s2": ("tcga", "s2"),
    "results_fast_v62_immune_tcga_nul": ("tcga", "nul42"),
}
REELS = {  # réels pipeline v6.2 existants
    "results_fast_v62_immune_icgc": ("icgc", "reel"),
    "results_fast_v62_immune_geo62452": ("geo62452", "reel"),
    "results_fast_v62_immune_tcga": ("tcga", "reel"),
}


def read_run(dossier):
    p = os.path.join(PDAC, dossier, "master_results.json")
    if not os.path.exists(p):
        return None, f"absent: {p}"
    with open(p) as f:
        j = json.load(f)
    bc = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
    l7a = j["prediction_levels"]["L7a_coherence"]
    conf = float(l7a["global_confidence"])
    direction = str(l7a["consensus_direction"]).lower()
    signed = conf if direction == "up" else (-conf if direction == "down" else 0.0)
    return {
        "version": j.get("version"),
        "n": int(j["reading_synthesis"]["n_samples"]),
        "w_size": int(bc["w_size"]), "min_grp": int(bc["min_grp"]),
        "n_candidates": int(bc["n_candidates"]),
        "seuil": round(float(bc["threshold"]), 4),
        "mc": round(float(bc["score"]), 4),
        "maxsep": round(float(bc["metrics"]["max_separation"]), 4),
        "stab": round(float(bc["metrics"]["stability"]), 4),
        "ssep": round(float(bc["metrics"]["max_separation"]) * float(bc["metrics"]["stability"]), 4),
        "delta": (None if j["reading_synthesis"]["Delta_tension"] is None
                  else round(float(j["reading_synthesis"]["Delta_tension"]), 4)),
        "l7a_signe": round(signed, 4),
    }, None


def dist(vals):
    v = np.asarray(vals, dtype=float)
    q = lambda p: float(np.quantile(v, p))
    return {"n": int(len(v)), "mediane": round(float(np.median(v)), 4),
            "moyenne": round(float(np.mean(v)), 4),
            "ecart_type": round(float(np.std(v, ddof=1)), 4) if len(v) > 1 else 0.0,
            "p5": q(0.05), "p25": q(0.25), "p75": q(0.75),
            "p95": q(0.95), "p97.5": q(0.975), "p2.5": q(0.025),
            "iqr": round(q(0.75) - q(0.25), 4),
            "min": round(float(v.min()), 4), "max": round(float(v.max()), 4)}


def main():
    out = {"runs": {}, "manquants": [], "distributions_pipeline": {}, "reels": {}}
    replica = json.load(open(f"{PDAC}/nulls_n70_853_replica.json"))
    raw = pd.read_csv(f"{PDAC}/nulls_n70_853_replica_raw.csv")
    for cohorte, seed in PLAN:
        label = f"{cohorte}_nul_s{seed}"
        dossier = f"results_fast_v62_853_{label}"
        r, err = read_run(dossier)
        if r is None:
            out["manquants"].append(label)
            print(f"[{label}] MANQUANT : {err}")
            continue
        ref = raw[(raw["cohorte"] == cohorte)
                  & (raw["config"] == "config_nulle")]["ssep"].values
        r["percentile_replique_config_nulle"] = round(float(np.mean(ref <= r["ssep"])) * 100, 1)
        out["runs"][label] = {"cohorte": cohorte, "graine": seed,
                              "dossier": dossier, **r}
        print(f"[{label}] S_sep={r['ssep']} maxsep={r['maxsep']} stab={r['stab']} "
              f"MC={r['mc']} pct_réplique={r['percentile_replique_config_nulle']}")
    # anciens runs §8.47 + réels
    for dossier, (cohorte, etiquette) in list(ANCIENS.items()) + list(REELS.items()):
        r, err = read_run(dossier)
        if r is None:
            out["manquants"].append(f"{cohorte}_{etiquette} ({dossier})")
            print(f"[{cohorte} {etiquette}] MANQUANT : {err}")
            continue
        key = f"{cohorte}_{etiquette}"
        out["runs"][key] = {"cohorte": cohorte, "graine": etiquette,
                            "dossier": dossier, **r}
        print(f"[{key}] S_sep={r['ssep']} maxsep={r['maxsep']} (ancien/réel)")
    # distributions pipeline par cohorte (nuls seulement)
    for cohorte in ("icgc", "geo62452", "tcga"):
        sseps = []
        for key, r in out["runs"].items():
            if r["cohorte"] != cohorte:
                continue
            if key.endswith("_reel"):
                continue
            sseps.append(r["ssep"])
        d = dist(sseps)
        rep = replica["distributions"][cohorte]["config_nulle"]["ssep"]
        reel = out["runs"][f"{cohorte}_reel"]["ssep"]
        d["reel_ssep"] = reel
        d["reel_moins_mediane_pipeline"] = round(reel - d["mediane"], 4)
        d["reel_percentile_pipeline"] = round(float(np.mean(np.array(sseps) <= reel)) * 100, 1)
        d["replique_mediane"] = rep["mediane"]
        d["replique_p95"] = rep["p95"]
        d["ecart_mediane_pipeline_moins_replique"] = round(d["mediane"] - rep["mediane"], 4)
        d["ecart_p95_pipeline_moins_replique"] = round(d["p95"] - rep["p95"], 4)
        # bootstrap de la médiane pipeline (2000 tirages) : SE empirique à k = n
        rng = np.random.default_rng(4242)
        meds = [np.median(rng.choice(sseps, size=len(sseps), replace=True))
                for _ in range(2000)]
        d["se_mediane_bootstrap"] = round(float(np.std(meds, ddof=1)), 4)
        out["distributions_pipeline"][cohorte] = d
        print(f"[{cohorte}] pipeline nuls n={d['n']} médiane={d['mediane']} "
              f"p95={d['p95']} SD={d['ecart_type']} | réplique médiane={rep['mediane']} "
              f"p95={rep['p95']} | réel={reel} (pct pipeline {d['reel_percentile_pipeline']})")
    with open(f"{PDAC}/nulls_n70_853_confirm.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"écrit: nulls_n70_853_confirm.json ({len(out['runs'])} runs lus, "
          f"{len(out['manquants'])} manquants)")


if __name__ == "__main__":
    main()
