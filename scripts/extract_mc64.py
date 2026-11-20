#!/usr/bin/env python3
"""Chantier v6.4 MC — validation HORS-LIGNE du MC recompose par concentration
(PROTOCOL_v6.4_mc.md). Lecture SEULE des master_results.json v6.2 deja sur
disque. AUCUN run du pipeline, AUCUN code modifie.
Formules gelees (PROTOCOL_v6.4_mc.md §3-§4) :
  MC2 (candidate C) = 0.70*sep + 0.30*conc
  sep  = maxsep/(1+maxsep)   (maxsep du best_config ANCIEN)
  conc = 1 - mediane_i(|theta_i - theta*|) / (theta_max - theta_min)
         (theta_i = seuils des tirages all_results ; theta* = seuil best ;
          conc=1 si etendue 0 ; conc=0 si <2 seuils lisibles)
  MC_E (exploratoire) = 0.80*sep + 0.20*recur
  recur = mediane_i(maxsep_i)/maxsep_best (definition v6.3)
  Diagnostics : sep seul ; MC_new v6.3 recalcule et verifie vs v63_mc_table.json.
Sorties : v64_mc_table.csv / v64_mc_table.json / v64_mc_table.md
Verifications : ancien MC relu == valeurs publiees (ssep_844 / phase2 v6.2),
tol. 1e-9 ; MC_new v6.3 recalcule == v63_mc_table.json, tol. 1e-9 ;
versions JSON ; paires completes (60 attendues).
"""
import csv
import json
import math
import os
import statistics

BASE = os.path.dirname(os.path.abspath(__file__))
W_SEP_C, W_CONC = 0.70, 0.30
W_SEP_E, W_RECUR_E = 0.80, 0.20
W_SEP63, W_STAB63, W_RECUR63 = 0.60, 0.25, 0.15


def g(o, path, default=None):
    for k in path.split("."):
        if not isinstance(o, dict) or k not in o:
            return default
        o = o[k]
    return o


def conc_from(thresholds, best_thr):
    """Concentration des seuils (PROTOCOL_v6.4_mc.md §3)."""
    vals = []
    for x in (thresholds or []):
        try:
            fx = float(x)
        except (TypeError, ValueError):
            continue
        if math.isfinite(fx):
            vals.append(fx)
    if len(vals) < 2:
        return 0.0, len(vals), None
    rng = max(vals) - min(vals)
    if rng == 0:
        return 1.0, len(vals), 0.0
    try:
        b = float(best_thr)
    except (TypeError, ValueError):
        return 0.0, len(vals), rng
    med_dev = float(statistics.median([abs(v - b) for v in vals]))
    conc = 1.0 - med_dev / rng
    return float(min(1.0, max(0.0, conc))), len(vals), rng


def recur_from(maxseps, best_maxsep):
    if best_maxsep and maxseps:
        r = statistics.median(maxseps) / best_maxsep
        return float(min(1.0, max(0.0, r)))
    return 0.0


def read_run(outdir):
    p = os.path.join(BASE, outdir, "master_results.json")
    if not os.path.exists(p):
        return None, f"absent: {p}"
    j = json.load(open(p))
    try:
        opt = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]
        bc = opt["best_config"]
        m = bc["metrics"]
        allres = opt.get("all_results") or []
        maxseps = [float(r["metrics"]["max_separation"]) for r in allres
                   if r.get("metrics") and r["metrics"].get("max_separation") is not None]
        stabs = [float(r["metrics"]["stability"]) for r in allres
                 if r.get("metrics") and r["metrics"].get("stability") is not None]
        thrs = [float(r["threshold"]) for r in allres
                if r.get("threshold") is not None]
        best_maxsep = float(m["max_separation"])
        best_stab = float(m["stability"])
        best_thr = float(bc["threshold"])
        sep = best_maxsep / (1.0 + best_maxsep) if best_maxsep > 0 else 0.0
        conc, n_thr, thr_range = conc_from(thrs, best_thr)
        recur = recur_from(maxseps, best_maxsep)
        mc2 = W_SEP_C * sep + W_CONC * conc
        mc_e = W_SEP_E * sep + W_RECUR_E * recur
        mc63 = W_SEP63 * sep + W_STAB63 * best_stab + W_RECUR63 * recur
        casc = j.get("five_threshold_cascade") or {}
        return {
            "version": j.get("version"),
            "n": j["reading_synthesis"]["n_samples"],
            "mc_old": float(bc["score"]),
            "mc_thr": best_thr,
            "maxsep": best_maxsep,
            "stab": best_stab,
            "robustness": float(m["robustness"]),
            "sharpness": float(m["sharpness"]),
            "ssep": best_maxsep * best_stab,
            "n_iter": len(allres),
            "n_thr": n_thr,
            "thr_range": thr_range,
            "median_maxsep": statistics.median(maxseps) if maxseps else None,
            "sep": sep, "conc": conc, "recur": recur,
            "mc2": mc2, "mc_e": mc_e, "mc63_recalc": mc63,
        }, None
    except (KeyError, TypeError) as e:
        return None, f"champ manquant dans {p}: {e}"


PRINCIPALS = [
    ("HP35", "results_fast_v62_hp35", "results_fast_v62_hp35_nul"),
    ("TCGA_v4", "results_fast_v62_tcga_v4", "results_fast_v62_tcga_v4_nul"),
    ("GSE71729", "results_fast_v62_geo71729", "results_fast_v62_geo71729_nul"),
    ("GSE62452", "results_fast_v62_geo62452", "results_fast_v62_geo62452_nul"),
    ("ICGC", "results_fast_v62_icgc", "results_fast_v62_icgc_nul"),
    ("IMMUNE_TCGA", "results_fast_v62_immune_tcga", "results_fast_v62_immune_tcga_nul"),
    ("PARP_TCGA", "results_fast_v62_parp_tcga", "results_fast_v62_parp_tcga_nul"),
    ("DEPMAP", "results_fast_v62_depmap", "results_fast_v62_depmap_nul"),
]
EXTRA = [
    ("TESTA_PROLIF", "results_fast_v62_prolif", "results_fast_v62_prolif_nul"),
    ("MTAP_PRMT5FLUX", "results_fast_v62_prmt5flux", "results_fast_v62_prmt5flux_nul"),
    ("MTAP_SERIES", "results_fast_v62_mtap", "results_fast_v62_mtap_nul"),
    ("V4R_PURITY", "results_fast_v62_v4r_purity", "results_fast_v62_v4r_purity_nul"),
]
EXISTING_ROT = {
    ("V4ROT", "CLDN18"): ("results_fast_v61_v4r_cldn18_dedup",
                          "results_fast_v61_v4r_cldn18_dedup_nul"),
    ("IMMROT", "CTLA4"): ("results_fast_v62_immrot_ctla4_dedup",
                          "results_fast_v62_immrot_ctla4_dedup_nul"),
    ("DEPMAPROT", "ACO2"): ("results_fast_v62_depmaprot_aco2_dedup",
                            "results_fast_v62_depmaprot_aco2_dedup_nul_sp"),
    ("PARPROT", "PARP1"): ("results_fast_v62_parprot_parp1_dedup",
                           "results_fast_v62_parprot_parp1_dedup_nul_sp"),
}


def rotation_dirs():
    pairs = []
    for line in open(os.path.join(BASE, "manifest_v62_dedup_844.txt")):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, _inp, out = line.split("|")
        base = name[len("DEDUP844_"):]
        is_nul = base.endswith("_NUL")
        base = base[:-4] if is_nul else base
        fam, ctrl = base.rsplit("_", 1)
        pairs.append((fam, ctrl, out, is_nul))
    d = {}
    for fam, ctrl, out, is_nul in pairs:
        d.setdefault((fam, ctrl), {})["NUL" if is_nul else "REEL"] = out
    for (fam, ctrl), (r, n) in EXISTING_ROT.items():
        d[(fam, ctrl)] = {"REEL": r, "NUL": n}
    return d


def classify(deltas, gigue):
    s = sum(deltas.values())
    direction = 1 if s > 0 else (-1 if s < 0 else 0)
    ok = [k for k, v in deltas.items()
          if direction != 0 and abs(v) > gigue and (1 if v > 0 else -1) == direction]
    return direction, ok, [k for k in deltas if k not in ok]


def main():
    missing, version_bad = [], []
    rows = []

    def add_pair(scope, name, rdir, ndir):
        r, e1 = read_run(rdir)
        n, e2 = read_run(ndir)
        if e1:
            missing.append(f"{name} REEL: {e1}")
            return
        if e2:
            missing.append(f"{name} NUL: {e2}")
            return
        for side, v in (("REEL", r), ("NUL", n)):
            if v["version"] not in ("v6.2.0-L7aL7b-CohenD-short",
                                    "v6.1.0-L7aL7b-CohenD-short"):
                version_bad.append(f"{name} {side}: {v['version']}")
        rows.append({
            "scope": scope, "paire": name, "n": r["n"],
            "mc_old_R": r["mc_old"], "mc_old_N": n["mc_old"],
            "d_mc_old": r["mc_old"] - n["mc_old"],
            "maxsep_R": r["maxsep"], "maxsep_N": n["maxsep"],
            "d_maxsep": r["maxsep"] - n["maxsep"],
            "stab_R": r["stab"], "stab_N": n["stab"],
            "sep_R": r["sep"], "sep_N": n["sep"],
            "d_sep": r["sep"] - n["sep"],
            "conc_R": r["conc"], "conc_N": n["conc"],
            "d_conc": r["conc"] - n["conc"],
            "recur_R": r["recur"], "recur_N": n["recur"],
            "d_recur": r["recur"] - n["recur"],
            "median_maxsep_R": r["median_maxsep"],
            "median_maxsep_N": n["median_maxsep"],
            "n_iter_R": r["n_iter"], "n_iter_N": n["n_iter"],
            "n_thr_R": r["n_thr"], "n_thr_N": n["n_thr"],
            "thr_range_R": r["thr_range"], "thr_range_N": n["thr_range"],
            "mc2_R": r["mc2"], "mc2_N": n["mc2"],
            "d_mc2": r["mc2"] - n["mc2"],
            "mc_e_R": r["mc_e"], "mc_e_N": n["mc_e"],
            "d_mc_e": r["mc_e"] - n["mc_e"],
            "mc63_R": r["mc63_recalc"], "mc63_N": n["mc63_recalc"],
            "d_mc63": r["mc63_recalc"] - n["mc63_recalc"],
            "thr_old_R": r["mc_thr"], "thr_old_N": n["mc_thr"],
            "robust_R": r["robustness"], "robust_N": n["robustness"],
            "sharp_R": r["sharpness"], "sharp_N": n["sharpness"],
            "version_R": r["version"], "version_N": n["version"],
        })

    for name, rdir, ndir in PRINCIPALS:
        add_pair("V1_principales", name, rdir, ndir)
    for (fam, ctrl), sides in sorted(rotation_dirs().items()):
        add_pair("V2_rotations", f"{fam}_{ctrl}", sides["REEL"], sides["NUL"])
    for name, rdir, ndir in EXTRA:
        add_pair("V3_V4_V5_descriptif", name, rdir, ndir)

    # --- Vérifications : ancien MC relu vs valeurs publiées ---
    checks = []
    s844 = {f"{r['famille']}_{r['controle']}": r for r in
            csv.DictReader(open(os.path.join(BASE, "ssep_844_rotations.csv")))}
    for row in rows:
        if row["scope"] == "V2_rotations" and row["paire"] in s844:
            want = float(s844[row["paire"]]["d_mc"])
            if abs(row["d_mc_old"] - want) > 1e-9:
                checks.append(f"{row['paire']}: d_mc_old relu {row['d_mc_old']:.6f} vs §8.44 {want:.6f}")
            want_ms = float(s844[row["paire"]]["d_maxsep"])
            if abs(row["d_maxsep"] - want_ms) > 1e-9:
                checks.append(f"{row['paire']}: d_maxsep relu {row['d_maxsep']:.6f} vs §8.44 {want_ms:.6f}")
    ph2 = {r["paire"]: r for r in csv.DictReader(open(os.path.join(BASE, "v62_phase2_table.csv")))}
    for row in rows:
        if row["scope"] == "V1_principales" and row["paire"] in ph2:
            want = float(ph2[row["paire"]]["d_mc"])
            if abs(row["d_mc_old"] - want) > 1e-9:
                checks.append(f"{row['paire']}: d_mc_old relu {row['d_mc_old']:.6f} vs phase2 {want:.6f}")
    # --- Régression : MC_new v6.3 recalculé vs v63_mc_table.json ---
    v63 = {r["paire"]: r for r in json.load(open(os.path.join(BASE, "v63_mc_table.json")))["paires"]}
    for row in rows:
        if row["paire"] in v63:
            want = v63[row["paire"]]["d_mc_new"]
            if abs(row["d_mc63"] - want) > 1e-9:
                checks.append(f"{row['paire']}: d_mc63 recalcule {row['d_mc63']:.6f} vs v63 {want:.6f}")
            if abs(row["mc63_R"] - v63[row["paire"]]["mc_new_R"]) > 1e-9:
                checks.append(f"{row['paire']}: mc63_R recalcule vs v63")

    # --- Verdicts gelés §5 (gigue_eff = max(gigue mesurée 0 attendue, 0.07) = 0.07) ---
    verdicts = {}
    for scope in ("V1_principales", "V2_rotations"):
        sub = [r for r in rows if r["scope"] == scope]
        for key, label in (("d_mc2", "MC2"), ("d_mc_e", "MC_E"),
                           ("d_sep", "sep_seul"),
                           ("d_mc63", "MC_new_v63"), ("d_mc_old", "MC_old"),
                           ("d_maxsep", "maxsep")):
            deltas = {r["paire"]: r[key] for r in sub if r[key] is not None}
            direction, ok, ko = classify(deltas, 0.07)
            verdicts[f"{scope}|{label}|0.07"] = {
                "direction": direction, "n_ok": len(ok), "n": len(deltas),
                "ok": ok, "ko": ko, "somme_ecarts": sum(deltas.values()),
                "moyenne_ecarts": sum(deltas.values()) / len(deltas)}
    hp = [r for r in rows if r["paire"] == "HP35"][0]
    verdicts["HP35"] = {"d_mc2": hp["d_mc2"], "d_mc_e": hp["d_mc_e"],
                        "d_sep": hp["d_sep"], "d_mc63": hp["d_mc63"],
                        "d_mc_old": hp["d_mc_old"], "d_maxsep": hp["d_maxsep"],
                        "conc_R": hp["conc_R"], "conc_N": hp["conc_N"],
                        "recur_R": hp["recur_R"], "recur_N": hp["recur_N"],
                        "sep_R": hp["sep_R"], "sep_N": hp["sep_N"]}

    out = {"paires": rows, "verdicts": verdicts,
           "controles": {"manquants": missing, "version_non_attendue": version_bad,
                         "ecarts_vs_publie": checks,
                         "formule_C": "MC2=0.70*maxsep/(1+maxsep)+0.30*(1-median_i(|theta_i-theta*|)/(theta_max-theta_min))",
                         "formule_E": "MC_E=0.80*maxsep/(1+maxsep)+0.20*median_i(maxsep_i)/maxsep_best",
                         "gigue_eff": 0.07}}
    json.dump(out, open(os.path.join(BASE, "v64_mc_table.json"), "w"),
              indent=1, ensure_ascii=False)
    cols = ["scope", "paire", "n", "mc_old_R", "mc_old_N", "d_mc_old",
            "maxsep_R", "maxsep_N", "d_maxsep", "stab_R", "stab_N",
            "sep_R", "sep_N", "d_sep",
            "conc_R", "conc_N", "d_conc",
            "recur_R", "recur_N", "d_recur",
            "median_maxsep_R", "median_maxsep_N", "n_iter_R", "n_iter_N",
            "n_thr_R", "n_thr_N", "thr_range_R", "thr_range_N",
            "mc2_R", "mc2_N", "d_mc2",
            "mc_e_R", "mc_e_N", "d_mc_e",
            "mc63_R", "mc63_N", "d_mc63",
            "thr_old_R", "thr_old_N",
            "robust_R", "robust_N", "sharp_R", "sharp_N"]
    with open(os.path.join(BASE, "v64_mc_table.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in cols})

    print(f"paires lues: {len(rows)} (V1: 8, V2: 48, descriptif: 4 attendus)")
    print(f"manquants: {missing if missing else 'AUCUN'}")
    print(f"version non attendue: {version_bad if version_bad else 'AUCUNE'}")
    print(f"ecarts vs publie: {checks if checks else 'AUCUN'}")
    for k, v in verdicts.items():
        if k == "HP35":
            print(f"HP35 d_mc2={v['d_mc2']:.4f} d_mc_e={v['d_mc_e']:.4f} "
                  f"d_sep={v['d_sep']:.4f} d_mc63={v['d_mc63']:.4f} d_mc_old={v['d_mc_old']:.4f}")
            print(f"HP35 conc R={v['conc_R']:.4f} N={v['conc_N']:.4f} "
                  f"recur R={v['recur_R']:.4f} N={v['recur_N']:.4f}")
        else:
            print(f"{k}: {v['n_ok']}/{v['n']} dir={v['direction']:+d} "
                  f"somme={v['somme_ecarts']:+.4f} moyenne={v['moyenne_ecarts']:+.4f}")
    print("écrit: v64_mc_table.json, v64_mc_table.csv")


if __name__ == "__main__":
    main()
