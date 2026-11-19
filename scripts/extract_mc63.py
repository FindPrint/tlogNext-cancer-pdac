#!/usr/bin/env python3
"""Chantier v6.3 MC — validation HORS-LIGNE du MC recompose (PROTOCOL_v6.3_mc.md).
Lecture SEULE des master_results.json v6.2 deja sur disque. AUCUN run du
pipeline, AUCUN code modifie.
Formules gelees (PROTOCOL_v6.3_mc.md §3-§4) :
  MC_new   = 0.60*sep + 0.25*stability + 0.15*recur
  sep      = maxsep/(1+maxsep)   (maxsep, stability du best_config ANCIEN)
  recur    = median_i(maxsep_i)/maxsep_best sur all_results (12 tirages fast)
  Variante S (exploratoire) : selection par 0.60*sep_i+0.25*stab_i, puis
  MC_new_S avec recur vs le tirage selectionne.
Sorties : v63_mc_table.csv / v63_mc_table.json / v63_mc_table.md
Verifications : ancien MC relu == valeurs publiees (ssep_844 / phase2 v6.2),
tol. 1e-9 ; versions JSON ; paires completes.
"""
import csv
import json
import math
import os
import statistics

BASE = os.path.dirname(os.path.abspath(__file__))
W_SEP, W_STAB, W_RECUR = 0.60, 0.25, 0.15


def g(o, path, default=None):
    for k in path.split("."):
        if not isinstance(o, dict) or k not in o:
            return default
        o = o[k]
    return o


def mc_new_from(best_maxsep, best_stab, all_maxseps):
    sep = best_maxsep / (1.0 + best_maxsep) if best_maxsep > 0 else 0.0
    if best_maxsep and all_maxseps:
        recur = statistics.median(all_maxseps) / best_maxsep
        recur = min(1.0, max(0.0, recur))
    else:
        recur = 0.0
    return W_SEP * sep + W_STAB * best_stab + W_RECUR * recur, sep, recur


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
        mc_new, sep, recur = mc_new_from(float(m["max_separation"]),
                                          float(m["stability"]), maxseps)
        # Variante S : selection par 0.60*sep_i + 0.25*stab_i
        best_s, sel = -1.0, None
        for ms, st in zip(maxseps, stabs):
            s = W_SEP * (ms / (1.0 + ms) if ms > 0 else 0.0) + W_STAB * st
            if s > best_s:
                best_s, sel = s, (ms, st)
        if sel is not None:
            mc_new_s, sep_s, recur_s = mc_new_from(sel[0], sel[1], maxseps)
            thr_s = None
            for r in allres:
                if (float(r["metrics"]["max_separation"]) == sel[0]
                        and float(r["metrics"]["stability"]) == sel[1]):
                    thr_s = float(r["threshold"])
                    break
        else:
            mc_new_s, sep_s, recur_s, thr_s = None, None, None, None
        casc = j.get("five_threshold_cascade") or {}
        return {
            "version": j.get("version"),
            "n": j["reading_synthesis"]["n_samples"],
            "mc_old": float(bc["score"]),
            "mc_thr": float(bc["threshold"]),
            "maxsep": float(m["max_separation"]),
            "stab": float(m["stability"]),
            "robustness": float(m["robustness"]),
            "sharpness": float(m["sharpness"]),
            "ssep": float(m["max_separation"]) * float(m["stability"]),
            "n_iter": len(allres),
            "n_maxsep": len(maxseps),
            "median_maxsep": statistics.median(maxseps) if maxseps else None,
            "sep": sep, "recur": recur, "mc_new": mc_new,
            "mc_new_s": mc_new_s, "sep_s": sep_s, "recur_s": recur_s,
            "thr_s": thr_s, "maxsep_s": sel[0] if sel else None,
            "t0": (float(casc["T_0_Monte_Carlo_Central"])
                   if casc.get("T_0_Monte_Carlo_Central") is not None else None),
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

    def add_pair(scope, name, rdir, ndir, n_expected=None):
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
            "recur_R": r["recur"], "recur_N": n["recur"],
            "median_maxsep_R": r["median_maxsep"],
            "median_maxsep_N": n["median_maxsep"],
            "n_iter_R": r["n_iter"], "n_iter_N": n["n_iter"],
            "mc_new_R": r["mc_new"], "mc_new_N": n["mc_new"],
            "d_mc_new": r["mc_new"] - n["mc_new"],
            "mc_new_S_R": r["mc_new_s"], "mc_new_S_N": n["mc_new_s"],
            "d_mc_new_S": (r["mc_new_s"] - n["mc_new_s"]
                           if r["mc_new_s"] is not None and n["mc_new_s"] is not None else None),
            "thr_S_R": r["thr_s"], "thr_S_N": n["thr_s"],
            "thr_old_R": r["mc_thr"], "thr_old_N": n["mc_thr"],
            "t0_R": r["t0"], "t0_N": n["t0"],
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

    # --- Verdicts geles §5 (gigue_eff = max(gigue mesuree 0 attendue, 0.07) = 0.07) ---
    verdicts = {}
    for scope in ("V1_principales", "V2_rotations"):
        sub = [r for r in rows if r["scope"] == scope]
        for key, label in (("d_mc_new", "MC_new"), ("d_mc_new_S", "MC_new_S"),
                           ("d_mc_old", "MC_old"), ("d_maxsep", "maxsep")):
            deltas = {r["paire"]: r[key] for r in sub if r[key] is not None}
            direction, ok, ko = classify(deltas, 0.07)
            verdicts[f"{scope}|{label}|0.07"] = {
                "direction": direction, "n_ok": len(ok), "n": len(deltas),
                "ok": ok, "ko": ko, "somme_ecarts": sum(deltas.values()),
                "moyenne_ecarts": sum(deltas.values()) / len(deltas)}
    # HP35
    hp = [r for r in rows if r["paire"] == "HP35"][0]
    verdicts["HP35"] = {"d_mc_new": hp["d_mc_new"], "d_mc_old": hp["d_mc_old"],
                        "d_maxsep": hp["d_maxsep"]}

    out = {"paires": rows, "verdicts": verdicts,
           "controles": {"manquants": missing, "version_non_attendue": version_bad,
                         "ecarts_vs_publie": checks,
                         "formule": "MC_new=0.60*maxsep/(1+maxsep)+0.25*stability+0.15*median_i(maxsep_i)/maxsep_best",
                         "gigue_eff": 0.07}}
    json.dump(out, open(os.path.join(BASE, "v63_mc_table.json"), "w"),
              indent=1, ensure_ascii=False)
    cols = ["scope", "paire", "n", "mc_old_R", "mc_old_N", "d_mc_old",
            "maxsep_R", "maxsep_N", "d_maxsep", "stab_R", "stab_N",
            "sep_R", "sep_N", "recur_R", "recur_N",
            "median_maxsep_R", "median_maxsep_N", "n_iter_R", "n_iter_N",
            "mc_new_R", "mc_new_N", "d_mc_new",
            "mc_new_S_R", "mc_new_S_N", "d_mc_new_S",
            "thr_S_R", "thr_S_N", "thr_old_R", "thr_old_N",
            "t0_R", "t0_N", "robust_R", "robust_N", "sharp_R", "sharp_N"]
    with open(os.path.join(BASE, "v63_mc_table.csv"), "w", newline="") as fh:
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
            print(f"HP35 d_mc_new={v['d_mc_new']:.4f} d_mc_old={v['d_mc_old']:.4f}")
        else:
            print(f"{k}: {v['n_ok']}/{v['n']} dir={v['direction']:+d} "
                  f"somme={v['somme_ecarts']:+.4f} moyenne={v['moyenne_ecarts']:+.4f}")
    print("écrit: v63_mc_table.json, v63_mc_table.csv")


if __name__ == "__main__":
    main()
