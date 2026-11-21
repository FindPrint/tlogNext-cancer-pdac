#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.75 — Extraction et comptages gelés de la clôture M2.
Lecture seule des master_results.json (aucun run). Reprend le lecteur
de mechanisms_863.py (read_all_results + fwhm_rob_from_curve) :
- vérification d'extraction : recomposition du MC
  (0,3·s_norm + 0,3·stab + 0,2·rob + 0,2·acuité) vs score stocké,
  écart toléré 10⁻⁶, sur TOUTES les configs de TOUS les runs lus ;
  la lecture n'est validée que si l'écart max est ≤ 10⁻⁶ ;
- comptages gelés : X (lot A, ICGC s61-s90, gagnante (35,16,6)),
  Y (lot B, GSE s31-s40, gagnante (34,16,6)) ;
- lectures secondaires : taux poolés + Wilson 95 % + binomial exact
  unilatéral vs p = 0,85 ; médiane des marges vainqueur-2e ;
  courbes rob-on (rob > 0,1 et > 0,5) ; attribution des écarts par
  MC_sans_rob = (MC - 0,2·rob)/0,8 (définition gelée §2 E du
  protocole) ; contrôle M2a (1 seul ensemble de 12 configs par n).
Sorties : m2_cloture_875_extract.json, m2_cloture_875_results.csv.
Protocole gelé : PROTOCOL_m2_cloture_875.md.
"""
import csv
import hashlib
import json
import math
import os
from math import comb

import numpy as np

PDAC = "/home/hatch/workspace/runs/pdac-v6"
CONFIG_REELLE = {"icgc": (35, 16, 6), "geo62452": (34, 16, 6)}
RUNS = {}
for s in range(11, 31):
    RUNS[f"icgc_nul_s{s}"] = ("icgc", f"results_fast_v62_853_icgc_nul_s{s}", "853")
for s in range(31, 41):
    RUNS[f"icgc_nul_s{s}"] = ("icgc", f"results_fast_v62_863_icgc_nul_s{s}", "863")
for s in range(41, 61):
    RUNS[f"icgc_nul_s{s}"] = ("icgc", f"results_fast_v62_873_icgc_nul_s{s}", "873")
for s in range(61, 91):
    RUNS[f"icgc_nul_s{s}"] = ("icgc", f"results_fast_v62_875_icgc_nul_s{s}", "875")
for s in range(11, 31):
    RUNS[f"geo62452_nul_s{s}"] = ("geo62452", f"results_fast_v62_853_geo62452_nul_s{s}", "853")
for s in range(31, 41):
    RUNS[f"geo62452_nul_s{s}"] = ("geo62452", f"results_fast_v62_875_geo62452_nul_s{s}", "875")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fwhm_rob_from_curve(curve):
    """Reproduit evaluate_scan_quality (lignes 3321-3364) : FWHM contiguë
    autour du pic, puis rob = exp(-((FWHM-10)^2)/(2*5^2)). Copie
    VERBATIM de mechanisms_863.py (lecture seule, aucune modification)."""
    scores = [s["score"] for s in curve if s.get("score") is not None]
    cand = [s["candidate"] for s in curve if s.get("score") is not None]
    if len(scores) < 3:
        return None, None, None
    max_idx = int(np.argmax(scores))
    maxsep = float(scores[max_idx])
    half = maxsep / 2.0
    left = max_idx
    while left > 0 and scores[left] >= half:
        left -= 1
    right = max_idx
    while right < len(scores) - 1 and scores[right] >= half:
        right += 1
    fwhm = float(cand[right] - cand[left])
    rob = float(np.exp(-((fwhm - 10.0) ** 2) / (2 * 5.0 ** 2)))
    return fwhm, rob, maxsep


def read_all_results(j):
    tm = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]
    out = []
    for r in tm["all_results"]:
        m = r["metrics"]
        mc_recomp = (0.3 * m["s_norm"] + 0.3 * m["stability"]
                     + 0.2 * m["robustness"] + 0.2 * m["sharpness"])
        fwhm, rob_recomp, _ = fwhm_rob_from_curve(r["scan_curve"])
        out.append({
            "iteration": r.get("iteration"),
            "rule": r.get("rule"),
            "n_candidates": int(r["n_candidates"]),
            "w_size": int(r["w_size"]),
            "min_grp": int(r["min_grp"]),
            "threshold": float(r["threshold"]),
            "score": float(r["score"]),
            "mc_recomp": mc_recomp,
            "ecart_recomp": abs(mc_recomp - float(r["score"])),
            "s_norm": float(m["s_norm"]),
            "stability": float(m["stability"]),
            "robustness": float(m["robustness"]),
            "sharpness": float(m["sharpness"]),
            "max_separation": float(m["max_separation"]),
            "fwhm_recalculee": fwhm,
            "rob_recalculee": rob_recomp,
            "ecart_rob": (None if rob_recomp is None else
                          abs(rob_recomp - float(m["robustness"]))),
        })
    return out, tm["best_config"]


def binom_cdf_le(k, n, p):
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i)
               for i in range(0, k + 1))


def wilson(k, n, z=1.96):
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def main():
    out = {"runs": {}, "manquants": [], "verdicts": {}}
    max_ecart_recomp = 0.0
    max_ecart_rob = 0.0
    n_configs_lues = 0
    for label, (cohorte, dossier, section) in sorted(RUNS.items()):
        path = os.path.join(PDAC, dossier, "master_results.json")
        if not os.path.exists(path):
            out["manquants"].append(label)
            print(f"[{label}] MANQUANT ({dossier})")
            continue
        with open(path) as f:
            j = json.load(f)
        rows, bc = read_all_results(j)
        best = (int(bc["n_candidates"]), int(bc["w_size"]), int(bc["min_grp"]))
        win = max(rows, key=lambda r: r["score"])
        win_cfg = (win["n_candidates"], win["w_size"], win["min_grp"])
        assert win_cfg == best, f"{label} : argmax != best_config"
        scores_tri = sorted((r["score"] for r in rows), reverse=True)
        marge = scores_tri[0] - scores_tri[1]
        rec_reelle = next((r for r in rows
                           if (r["n_candidates"], r["w_size"], r["min_grp"])
                           == CONFIG_REELLE[cohorte]), None)
        ecart = None
        if rec_reelle is not None and win_cfg != CONFIG_REELLE[cohorte]:
            mc_sr_reelle = (rec_reelle["score"] - 0.2 * rec_reelle["robustness"]) / 0.8
            mc_sr_win = (win["score"] - 0.2 * win["robustness"]) / 0.8
            bascule = bool(mc_sr_reelle > mc_sr_win and win["robustness"] > 0.1)
            ecart = {"mc_sans_rob_reelle": mc_sr_reelle,
                     "mc_sans_rob_gagnante": mc_sr_win,
                     "rob_gagnante": win["robustness"],
                     "basculement_robustesse": bascule}
        max_ecart_recomp = max(max_ecart_recomp,
                               max(r["ecart_recomp"] for r in rows))
        max_ecart_rob = max(max_ecart_rob,
                            max(r["ecart_rob"] for r in rows
                                if r["ecart_rob"] is not None))
        n_configs_lues += len(rows)
        out["runs"][label] = {
            "cohorte": cohorte, "section": section, "dir": dossier,
            "best_config": best, "best_rule": bc.get("rule"),
            "mc_gagnant": win["score"], "rob_gagnante": win["robustness"],
            "maxsep_gagnant": win["max_separation"],
            "marge_vainqueur_2e": marge, "n_configs": len(rows),
            "n_rob_gt01": sum(1 for r in rows if r["robustness"] > 0.1),
            "n_rob_gt05": sum(1 for r in rows if r["robustness"] > 0.5),
            "max_rob": max(r["robustness"] for r in rows),
            "config_reelle": CONFIG_REELLE[cohorte],
            "choisit_reelle": bool(win_cfg == CONFIG_REELLE[cohorte]),
            "ecart": ecart,
            "all_results": rows,
        }
        print(f"[{label:18s}] win={win_cfg} MC={win['score']:.4f} "
              f"rob={win['robustness']:.4f} maxsep={win['max_separation']:.4f} "
              f"marge={marge:.4f} rob>0.1:{out['runs'][label]['n_rob_gt01']}/12 "
              f"ecart_recomp_max={max(r['ecart_recomp'] for r in rows):.2e}")
    out["verification_extraction"] = {
        "n_runs_lus": len(out["runs"]),
        "n_configs_lues": n_configs_lues,
        "ecart_recomp_max": max_ecart_recomp,
        "ecart_rob_max": max_ecart_rob,
        # Porte gelée (§3C) : recomposition du MC seule.
        "validee": bool(max_ecart_recomp <= 1e-6),
        # Diagnostic seulement : recomposition de rob depuis les courbes.
        "ecart_rob_validee": bool(max_ecart_rob <= 1e-6),
    }
    print(f"Extraction : {len(out['runs'])} runs, {n_configs_lues} configs, "
          f"ecart_recomp_max={max_ecart_recomp:.2e}, "
          f"ecart_rob_max={max_ecart_rob:.2e}, "
          f"validee={out['verification_extraction']['validee']}")

    # ---- Contrôle M2a : 1 seul ensemble de 12 configs par cohorte
    for cohorte in ("icgc", "geo62452"):
        sets = {}
        for label, rec in out["runs"].items():
            if rec["cohorte"] != cohorte:
                continue
            key = tuple(sorted((r["n_candidates"], r["w_size"], r["min_grp"],
                                r["rule"]) for r in rec["all_results"]))
            sets.setdefault(key, []).append(label)
        out["verdicts"][f"m2a_{cohorte}"] = {
            "n_ensembles_distincts": len(sets),
            "n_runs": sum(len(v) for v in sets.values())}

    # ---- Comptages gelés et lectures secondaires
    def taux(labels):
        lus = [out["runs"][l] for l in labels if l in out["runs"]]
        k = sum(1 for r in lus if r["choisit_reelle"])
        return k, len(lus)

    icgc_875 = [f"icgc_nul_s{s}" for s in range(61, 91)]
    gse_875 = [f"geo62452_nul_s{s}" for s in range(31, 41)]
    icgc_tous = [f"icgc_nul_s{s}" for s in range(11, 91)]
    gse_tous = [f"geo62452_nul_s{s}" for s in range(11, 41)]
    icgc_base = [f"icgc_nul_s{s}" for s in range(11, 61)]
    gse_base = [f"geo62452_nul_s{s}" for s in range(11, 31)]

    res = {}
    for nom, labels in (("lotA_icgc_875", icgc_875),
                        ("lotB_gse_875", gse_875),
                        ("icgc_poole_80", icgc_tous),
                        ("gse_poole_30", gse_tous),
                        ("icgc_base_50", icgc_base),
                        ("gse_base_20", gse_base)):
        k, n = taux(labels)
        lo, hi = wilson(k, n) if n else (None, None)
        res[nom] = {"k": k, "n": n, "taux": (k / n if n else None),
                    "wilson95": [lo, hi],
                    "p_binom_vs_085": (binom_cdf_le(k, n, 0.85) if n else None),
                    "complet": n == len(labels)}
    out["comptages"] = res

    x = res["lotA_icgc_875"]["k"] if res["lotA_icgc_875"]["complet"] else None
    y = res["lotB_gse_875"]["k"] if res["lotB_gse_875"]["complet"] else None
    va = None
    if x is not None:
        va = "CONFIRME" if x >= 21 else ("INFIRME" if x <= 12 else "INDÉCIS")
    vb = None
    if y is not None:
        vb = "CONFIRME" if y >= 7 else ("INFIRME" if y <= 4 else "INDÉCIS")
    vg = None
    if va == "CONFIRME" and vb in ("CONFIRME", "INDÉCIS"):
        vg = "TRANCHÉ–CONFIRMÉ"
    elif va == "INFIRME":
        vg = "TRANCHÉ–INFIRMÉ"
    elif va == "CONFIRME" and vb == "INFIRME":
        vg = "TRANCHÉ–DIVERGENT"
    elif va == "INDÉCIS":
        vg = "FERMÉ COMME NON CONCLUANT"
    out["verdicts"].update({"lotA": va, "lotB": vb, "global_M2": vg,
                            "X": x, "Y": y})

    # ---- Marges et rob-on sur les lots neufs
    for nom, labels in (("lotA_icgc_875", icgc_875),
                        ("lotB_gse_875", gse_875)):
        lus = [out["runs"][l] for l in labels if l in out["runs"]]
        if lus:
            marges = sorted(r["marge_vainqueur_2e"] for r in lus)
            med = marges[len(marges) // 2] if len(marges) % 2 else (
                marges[len(marges) // 2 - 1] + marges[len(marges) // 2]) / 2
            out["verdicts"][f"marges_{nom}"] = {
                "mediane": med,
                "min": marges[0], "max": marges[-1],
                "n_inf_0005": sum(1 for m in marges if m < 0.005),
                "n_inf_001": sum(1 for m in marges if m < 0.01)}
            out["verdicts"][f"rob_on_{nom}"] = {
                "courbes_rob_gt01": sum(r["n_rob_gt01"] for r in lus),
                "courbes_rob_gt05": sum(r["n_rob_gt05"] for r in lus),
                "courbes_total": 12 * len(lus),
                "runs_gagnante_rob_gt01": sum(
                    1 for r in lus if r["rob_gagnante"] > 0.1)}
            basc = [l for l in labels
                    if l in out["runs"] and out["runs"][l]["ecart"]
                    and out["runs"][l]["ecart"]["basculement_robustesse"]]
            autres = [l for l in labels
                      if l in out["runs"] and out["runs"][l]["ecart"]
                      and not out["runs"][l]["ecart"]["basculement_robustesse"]]
            out["verdicts"][f"ecarts_{nom}"] = {
                "n_ecarts": len(basc) + len(autres),
                "basculements_robustesse": basc,
                "autres": autres}

    with open(f"{PDAC}/m2_cloture_875_extract.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    with open(f"{PDAC}/m2_cloture_875_results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["label", "cohorte", "section", "dir", "best_ncand",
                    "best_w", "best_min_grp", "mc_gagnant", "rob_gagnante",
                    "maxsep_gagnant", "marge", "choisit_reelle",
                    "n_rob_gt01", "n_rob_gt05", "max_rob",
                    "bascule_robustesse"])
        for label in sorted(out["runs"]):
            r = out["runs"][label]
            nc, ww, mg = r["best_config"]
            w.writerow([label, r["cohorte"], r["section"], r["dir"], nc, ww,
                        mg, f"{r['mc_gagnant']:.6f}",
                        f"{r['rob_gagnante']:.6f}",
                        f"{r['maxsep_gagnant']:.6f}",
                        f"{r['marge_vainqueur_2e']:.6f}",
                        int(r["choisit_reelle"]), r["n_rob_gt01"],
                        r["n_rob_gt05"], f"{r['max_rob']:.6f}",
                        ("" if r["ecart"] is None else
                         int(r["ecart"]["basculement_robustesse"]))])
    print(json.dumps({"comptages": res, "verdicts": out["verdicts"]},
                     indent=2, ensure_ascii=False))
    print("écrit: m2_cloture_875_extract.json, m2_cloture_875_results.csv")


if __name__ == "__main__":
    main()
