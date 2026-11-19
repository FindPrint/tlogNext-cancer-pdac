#!/usr/bin/env python3
"""§8.47 (d) — Extraction des résultats du lot de confirmation pipeline v6.2.
Lecture seule des master_results.json des 11 runs
(results_fast_v62_847_*). Compare chaque maxsep pipeline à la prédiction
de la réplique (icgc_immune_inversion_replica.json) quand elle existe :
pour les nuls graines 1-3 / 1-2, la réplique ne donne pas une valeur
ponctuelle mais une distribution — on rapporte le percentile du maxsep
pipeline dans la distribution répliquée (config nulle).
Sortie : icgc_immune_inversion_confirm.json.
Protocole gelé : PROTOCOL_icgc_immune_inversion.md
  SHA b55283eeb7a24e30b52ee6a8f24de8a77b3c7b53072d8b837fab9eb08a61eb34
  (+ addendum §9, SHA f1a5a37c0b8ce452b4d00a9d2a649ac41384e076dcb80839389eac728988379c)
"""
import json
import os

import numpy as np

PDAC = "/home/hatch/workspace/runs/pdac-v6"

# (étiquette, suffixe de dossier, cohorte, côté, config réplique de référence)
RUNS = [
    ("icgc_nul_s1", "icgc_nul_s1", "icgc", "nul", "config_nulle"),
    ("icgc_nul_s2", "icgc_nul_s2", "icgc", "nul", "config_nulle"),
    ("icgc_nul_s3", "icgc_nul_s3", "icgc", "nul", "config_nulle"),
    ("geo62452_nul_s1", "geo62452_nul_s1", "geo62452", "nul", "config_nulle"),
    ("geo62452_nul_s2", "geo62452_nul_s2", "geo62452", "nul", "config_nulle"),
    ("tcga_nul_s1", "tcga_nul_s1", "tcga", "nul", "config_nulle"),
    ("tcga_nul_s2", "tcga_nul_s2", "tcga", "nul", "config_nulle"),
    ("icgc_10g_reel", "icgc_10g", "icgc", "reel10g", "config_reelle"),
    ("icgc_10g_nul42", "icgc_10g_nul", "icgc", "nul10g", "config_nulle"),
    ("tcga_10g_reel", "tcga_10g", "tcga", "reel10g", "config_reelle"),
    ("tcga_10g_nul42", "tcga_10g_nul", "tcga", "nul10g", "config_nulle"),
]


def read_run(suffix):
    d = os.path.join(PDAC, f"results_fast_v62_847_{suffix}", "master_results.json")
    if not os.path.exists(d):
        return None, f"absent: {d}"
    with open(d) as f:
        j = json.load(f)
    bc = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
    l7a = j["prediction_levels"]["L7a_coherence"]
    conf = float(l7a["global_confidence"])
    direction = str(l7a["consensus_direction"]).lower()
    signed = conf if direction == "up" else (-conf if direction == "down" else 0.0)
    return {
        "version": j.get("version"),
        "n": int(j["reading_synthesis"]["n_samples"]),
        "control": j.get("metadata", {}).get("control"),
        "w_size": int(bc["w_size"]), "min_grp": int(bc["min_grp"]),
        "n_candidates": int(bc["n_candidates"]),
        "seuil": round(float(bc["threshold"]), 4),
        "mc": round(float(bc["score"]), 4),
        "maxsep": round(float(bc["metrics"]["max_separation"]), 4),
        "stab": round(float(bc["metrics"]["stability"]), 4),
        "ssep": round(float(bc["metrics"]["max_separation"]) * float(bc["metrics"]["stability"]), 4),
        "delta": (None if j["reading_synthesis"]["Delta_tension"] is None
                  else round(float(j["reading_synthesis"]["Delta_tension"]), 4)),
        "l7a_dir": direction, "l7a_conf": round(conf, 4),
        "l7a_signe": round(signed, 4),
    }, None


def main():
    replica = json.load(open(f"{PDAC}/icgc_immune_inversion_replica.json"))
    out = {"runs": {}, "manquants": [], "d_ssep_10g_pipeline": {}}
    for label, suffix, cohorte, cote, cfg_ref in RUNS:
        val, err = read_run(suffix)
        if err:
            out["manquants"].append(f"{label}: {err}")
            print(f"[{label}] MANQUANT: {err}")
            continue
        val["cohorte"] = cohorte
        val["cote"] = cote
        # percentile du maxsep pipeline dans la distribution répliquée
        # (config nulle, permutations par ligne) — pour les nuls seulement
        if cote == "nul":
            dist = replica["distributions_nulles"][cohorte][cfg_ref]
            # on n'a stocké que les quantiles : encadrement grossier
            val["replique_mediane"] = dist["mediane"]
            val["replique_p2.5"] = dist["p2.5"]
            val["replique_p97.5"] = dist["p97.5"]
            val["dans_intervalle_p2.5_p97.5"] = bool(
                dist["p2.5"] <= val["maxsep"] <= dist["p97.5"])
        out["runs"][label] = val
        print(f"[{label}] n={val['n']} maxsep={val['maxsep']} ssep={val['ssep']} "
              f"mc={val['mc']} delta={val['delta']} l7a={val['l7a_dir']} {val['l7a_conf']} "
              f"seuil={val['seuil']}% w={val['w_size']} ncand={val['n_candidates']}")
    # d_ssep 10 gènes côté pipeline (ICGC + TCGA)
    for cohorte in ("icgc", "tcga"):
        r = out["runs"].get(f"{cohorte}_10g_reel")
        n = out["runs"].get(f"{cohorte}_10g_nul42")
        if r and n:
            out["d_ssep_10g_pipeline"][cohorte] = round(r["ssep"] - n["ssep"], 4)
            print(f"[10g {cohorte}] d_ssep pipeline = {r['ssep']} - {n['ssep']} "
                  f"= {out['d_ssep_10g_pipeline'][cohorte]} "
                  f"(12g pipeline : {'-0,2200' if cohorte == 'icgc' else '+0,3659'})")
    with open(f"{PDAC}/icgc_immune_inversion_confirm.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("écrit: icgc_immune_inversion_confirm.json")


if __name__ == "__main__":
    main()
