#!/usr/bin/env python3
"""Elucidation Delta — PROTOCOL_v6.2.md §4. Lecture SEULE des master_results.json.
Aucun run du pipeline, aucune modification du pipeline.
Ensemble : 156 runs v6.1 (results_fast_v61_*) + tous les runs v6.2 sur disque
(results_fast_v62_*, validation rep1/rep2 + phase 2 principales + secondaires).
Pour chaque run : d_sat, d_crit, d_div, Delta, les 6 medianes divergence triees
AVEC leur nom (paire mediane 3e/4e), les 7 medianes saturation triees, masque
fini/absent, n_fluxes_used, MFA brut, best_config (max_sep, stability,
robustness, sharpness), L7a, trio_gap_E.
Hypotheses H1-H7 (§4.3) : pour chaque variable candidate, taux de prediction
de l'identite de la paire mediane (majorite dans le groupe) ET de la valeur
de d_div a ±0,10 pres (moyenne du groupe comme prediction — lecture honnete ;
la reconstruction par les valeurs de la paire est une identite de
construction, rapportee a part comme controle).
Critere §4.4 : elucide si (a) >= 90 % paire ET (b) >= 90 % valeur.
Sorties : v62_delta_levels.csv, v62_delta_levels.json (resume + tables).
"""
import glob
import json
import math
import os
import sys
from collections import Counter, defaultdict

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
DIV = ["LevinaBickel", "PCAIntrinsic", "LocalPCA", "GraphDimension",
       "PersistentHomology", "MFA"]
SAT = ["Higuchi", "Katz", "Petrosian", "Sevcik", "BoxCounting", "Hurst2mH", "DFA"]
CRIT = ["CorrelationD2", "GrassbergerProcaccia", "InformationD1", "VisibilityGraph",
        "TwoNN", "DANCo", "Fisher"]


def g(o, path, default=None):
    for k in path.split("."):
        if not isinstance(o, dict) or k not in o:
            return default
        o = o[k]
    return o


def fnum(x):
    try:
        x = float(x)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def collect():
    rows = []
    pats = [os.path.join(BASE, "results_fast_v61_*", "master_results.json"),
            os.path.join(BASE, "results_fast_v62_*", "master_results.json")]
    for pat in pats:
        for p in sorted(glob.glob(pat)):
            d = os.path.basename(os.path.dirname(p))
            try:
                j = json.load(open(p))
            except Exception as e:
                print(f"LECTURE IMPOSSIBLE {d}: {e}", file=sys.stderr)
                continue
            ht = g(j, "holographic_tension_state", {}) or {}
            per = g(ht, "per_estimator", {}) or {}
            dv = g(ht, "D_vector", {}) or {}
            bc = g(j, "run_pipeline.threshold_metadata.threshold_optimization.best_config", {}) or {}
            m = g(bc, "metrics", {}) or {}
            l7 = g(j, "prediction_levels.L7a_coherence", {}) or {}
            tri = g(ht, "tension_gap_diagnostics.triangulation", {}) or {}

            def meds(names):
                out = {}
                for nm in names:
                    e = per.get(nm) or {}
                    out[nm] = (fnum(e.get("raw_median")),
                               fnum(e.get("n_fluxes_used")))
                return out

            dm = meds(DIV)
            sm = meds(SAT)
            div_sorted = sorted([(v, k) for k, (v, _) in dm.items() if v is not None])
            sat_sorted = sorted([(v, k) for k, (v, _) in sm.items() if v is not None])
            d_div_calc = None
            pair = None
            if len(div_sorted) >= 2:
                k = len(div_sorted)
                if k % 2 == 0:
                    a, b = div_sorted[k // 2 - 1], div_sorted[k // 2]
                    d_div_calc = (a[0] + b[0]) / 2.0
                    pair = (a[1], b[1])
                else:
                    d_div_calc = div_sorted[k // 2][0]
                    pair = (div_sorted[k // 2][1],)
            d_sat_calc = sat_sorted[3][0] if len(sat_sorted) >= 4 else None
            sat_med_member = sat_sorted[3][1] if len(sat_sorted) >= 4 else None
            nflux = Counter(v for _, v in dm.values() if v is not None)
            rows.append({
                "dir": d,
                "version": j.get("version"),
                "n": fnum(g(j, "reading_synthesis.n_samples")),
                "control": g(j, "metadata.control"),
                "d_sat": fnum(dv.get("d_sat")), "d_crit": fnum(dv.get("d_crit")),
                "d_div": fnum(dv.get("d_div")), "d_null": fnum(dv.get("d_null")),
                "delta": fnum(g(j, "reading_synthesis.Delta_tension")),
                "d_div_calc": d_div_calc, "d_sat_calc": d_sat_calc,
                "pair": "+".join(pair) if pair else None,
                "pair_3e": pair[0] if pair else None,
                "pair_4e": pair[1] if pair and len(pair) > 1 else None,
                "sat_med_member": sat_med_member,
                "div_sorted": ";".join(f"{k}={v:.4f}" for v, k in div_sorted),
                "sat_sorted": ";".join(f"{k}={v:.4f}" for v, k in sat_sorted),
                "mask_levina": dm["LevinaBickel"][0] is not None,
                "mask_ph": dm["PersistentHomology"][0] is not None,
                "mask": ("L" if dm["LevinaBickel"][0] is not None else "-")
                        + ("P" if dm["PersistentHomology"][0] is not None else "-"),
                "mfa": dm["MFA"][0],
                "n_fluxes_mode": nflux.most_common(1)[0][0] if nflux else None,
                "n_fluxes_div": ";".join(f"{k}:{int(v)}" for k, (_, v) in dm.items() if v is not None),
                "max_sep": fnum(m.get("max_separation")),
                "stability": fnum(m.get("stability")),
                "robustness": fnum(m.get("robustness")),
                "sharpness": fnum(m.get("sharpness")),
                "l7a_dir": l7.get("consensus_direction"),
                "l7a_conf": fnum(l7.get("global_confidence")),
                "trio_gap_E": fnum(tri.get("trio_gap_E")),
                "trio_values": tri.get("trio_values"),
                "dfa": sm["DFA"][0],
                "div_medians": {k: v for k, (v, _) in dm.items()},
                "sat_medians": {k: v for k, (v, _) in sm.items()},
            })
    return rows


def majority_accuracy(rows, keyfn):
    """Prediction de la paire par la majorite dans chaque groupe defini par keyfn.
    Retourne (exactitude paire, exactitude valeur ±0,10 par moyenne de groupe,
    nb groupes, taille du plus grand groupe)."""
    groups = defaultdict(list)
    for r in rows:
        if r["pair"] is None or r["d_div"] is None:
            continue
        groups[keyfn(r)].append(r)
    n_tot = sum(len(v) for v in groups.values())
    ok_pair = ok_val = 0
    for _, rs in groups.items():
        maj_pair = Counter(x["pair"] for x in rs).most_common(1)[0][0]
        mean_div = float(np.mean([x["d_div"] for x in rs]))
        for x in rs:
            if x["pair"] == maj_pair:
                ok_pair += 1
            if abs(x["d_div"] - mean_div) <= 0.10:
                ok_val += 1
    return (ok_pair / n_tot if n_tot else None,
            ok_val / n_tot if n_tot else None, len(groups), n_tot)


def pearson(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None, len(pairs)
    a = np.array([p[0] for p in pairs]); b = np.array([p[1] for p in pairs])
    if a.std() == 0 or b.std() == 0:
        return None, len(pairs)
    return float(np.corrcoef(a, b)[0, 1]), len(pairs)


def main():
    rows = collect()
    v61 = [r for r in rows if str(r["version"]).startswith("v6.1")]
    v62 = [r for r in rows if str(r["version"]).startswith("v6.2")]
    print(f"Runs lus : {len(rows)} (v6.1 : {len(v61)}, v6.2 : {len(v62)})")

    # Verifications d'identite (§4.2).
    mis_div = [r for r in rows if r["d_div"] is not None and r["d_div_calc"] is not None
               and abs(r["d_div"] - r["d_div_calc"]) > 1e-6]
    mis_sat = [r for r in rows if r["d_sat"] is not None and r["d_sat_calc"] is not None
               and abs(r["d_sat"] - r["d_sat_calc"]) > 1e-6]
    print(f"Identite d_div = moyenne 3e/4e : {len(rows) - len(mis_div)}/{len(rows)} "
          f"(mismatches : {[r['dir'] for r in mis_div]})")
    print(f"Identite d_sat = 4e saturation : {len(rows) - len(mis_sat)}/{len(rows)} "
          f"(mismatches : {[r['dir'] for r in mis_sat]})")

    # Faits de base.
    ddiv_vals = [r["d_div"] for r in rows if r["d_div"] is not None]
    print(f"d_div : {len(set(round(v, 3) for v in ddiv_vals))} valeurs distinctes "
          f"(a 1e-3) sur {len(ddiv_vals)} runs ; min {min(ddiv_vals):.2f} max {max(ddiv_vals):.2f}")
    mfa_vals = sorted(set(round(r["mfa"], 3) for r in rows if r["mfa"] is not None))
    print(f"MFA : {len(mfa_vals)} valeurs distinctes : {mfa_vals}")
    print(f"Masques fini/absent : {dict(Counter(r['mask'] for r in rows))}")
    print(f"Paires medianes : {dict(Counter(r['pair'] for r in rows if r['pair']))}")
    print(f"Membre median saturation (4e) : {dict(Counter(r['sat_med_member'] for r in rows))}")

    # Correlations avec d_div.
    for name in DIV + ["robustness", "sharpness", "max_sep", "stability"]:
        xs = [r["div_medians"].get(name) if name in DIV else r[name] for r in rows]
        c, n = pearson(xs, [r["d_div"] for r in rows])
        print(f"  corr(d_div, {name}) Pearson = {c} (n={n})" if c is not None
              else f"  corr(d_div, {name}) : non calculable (n={n})")
    # d_sat quasi constant ?
    dsat = [r["d_sat"] for r in rows if r["d_sat"] is not None]
    print(f"d_sat : moyenne {np.mean(dsat):.3f} ecart-type {np.std(dsat):.3f} "
          f"min {min(dsat):.3f} max {max(dsat):.3f} ; "
          f"valeurs arrondies 0,01 les plus frequentes : {Counter(round(v, 2) for v in dsat).most_common(5)}")
    # Anomalie DFA.
    dfa_rows = sorted(rows, key=lambda r: (r["dfa"] if r["dfa"] is not None else 0))
    print(f"DFA min : {dfa_rows[0]['dfa']} ({dfa_rows[0]['dir']}, paire sat 4e={dfa_rows[0]['sat_med_member']}, "
          f"d_sat={dfa_rows[0]['d_sat']}) ; DFA max : {dfa_rows[-1]['dfa']} ({dfa_rows[-1]['dir']})")
    dfa_extreme = [r for r in rows if r["dfa"] is not None and r["dfa"] < -10]
    for r in dfa_extreme:
        print(f"  DFA EXTREME {r['dfa']} sur {r['dir']} : sat triees [{r['sat_sorted']}] "
              f"d_sat={r['d_sat']} (4e={r['sat_med_member']}) Delta={r['delta']}")

    # H1-H7 : taux de prediction (paire + valeur).
    cands = {
        "H1 masque (L/P)": lambda r: r["mask"],
        "H1b masque Levina seule": lambda r: r["mask_levina"],
        "H1c masque PH seule": lambda r: r["mask_ph"],
        "H2 MFA": lambda r: round(r["mfa"], 3) if r["mfa"] is not None else None,
        "H3 n": lambda r: r["n"],
        "H3b n_fluxes_mode": lambda r: r["n_fluxes_mode"],
        "H3c (n, n_fluxes_mode)": lambda r: (r["n"], r["n_fluxes_mode"]),
        "H5 controle": lambda r: r["control"],
        "H5b (controle, masque)": lambda r: (r["control"], r["mask"]),
        "H1+H2 (masque, MFA)": lambda r: (r["mask"], round(r["mfa"], 3) if r["mfa"] is not None else None),
        "H2+H3 (MFA, n)": lambda r: (round(r["mfa"], 3) if r["mfa"] is not None else None, r["n"]),
        "H1+H3 (masque, n)": lambda r: (r["mask"], r["n"]),
        "H1+H2+H3 (masque, MFA, n)": lambda r: (r["mask"], round(r["mfa"], 3) if r["mfa"] is not None else None, r["n"]),
    }
    results = {}
    for label, fn in cands.items():
        a_pair, a_val, ng, n_tot = majority_accuracy(rows, fn)
        results[label] = {"acc_paire": a_pair, "acc_valeur_pm010": a_val,
                          "n_groupes": ng, "n_runs": n_tot}
        print(f"{label} : paire {a_pair:.3f} | valeur ±0,10 {a_val:.3f} "
              f"({ng} groupes, n={n_tot})" if a_pair is not None else f"{label} : n/d")
    # v6.1 seul vs v6.2 seul, meilleure candidate.
    for subset, name in ((v61, "v6.1 seul"), (v62, "v6.2 seul")):
        if len(subset) >= 5:
            a_pair, a_val, ng, n_tot = majority_accuracy(subset, cands["H1+H2+H3 (masque, MFA, n)"])
            print(f"  Meilleure (H1+H2+H3) {name} : paire {a_pair} | valeur {a_val} (n={n_tot})")

    # H4 : robustness en quartiles.
    rob = sorted([r["robustness"] for r in rows if r["robustness"] is not None])
    if rob:
        qs = np.quantile(rob, [0, 0.25, 0.5, 0.75, 1.0])
        print(f"  H4 robustness quartiles : {['%.2e' % q for q in qs]} ; "
              f"table quartile x paire :")
        for qi in range(4):
            lo, hi = qs[qi], qs[qi + 1]
            sub = [r for r in rows if r["robustness"] is not None
                   and lo <= r["robustness"] <= hi + (1e-30 if qi == 3 else 0)]
            print(f"    Q{qi+1} [{lo:.2e}, {hi:.2e}] n={len(sub)} paires={dict(Counter(r['pair'] for r in sub))}")

    # H6 : reconstruction par les valeurs de la paire (identite de construction).
    recon_ok = sum(1 for r in rows if r["d_div"] is not None and r["d_div_calc"] is not None
                   and abs(r["d_div"] - r["d_div_calc"]) <= 0.10)
    print(f"H6 reconstruction (valeurs de la paire) : d_div retrouve a ±0,10 sur "
          f"{recon_ok}/{len(rows)} — identite de construction, pas une prediction.")

    # H7 : d_sat par famille (n) + membre median.
    by_n = defaultdict(list)
    for r in rows:
        if r["n"] is not None:
            by_n[r["n"]].append(r)
    for n in sorted(by_n):
        rs = by_n[n]
        ds = [x["d_sat"] for x in rs if x["d_sat"] is not None]
        print(f"  n={n:.0f} : {len(rs)} runs, d_sat {np.mean(ds):.3f} ± {np.std(ds):.3f}, "
              f"4e membre dominant : {Counter(x['sat_med_member'] for x in rs).most_common(2)}")

    # Verdict §4.4 (sur l'ensemble).
    best = max(results.items(), key=lambda kv: (kv[1]["acc_paire"] or 0))
    elucide = (best[1]["acc_paire"] is not None and best[1]["acc_paire"] >= 0.90
               and best[1]["acc_valeur_pm010"] is not None and best[1]["acc_valeur_pm010"] >= 0.90)
    print(f"\nVERDICT §4.4 : meilleure variable = {best[0]} (paire {best[1]['acc_paire']:.3f}, "
          f"valeur {best[1]['acc_valeur_pm010']:.3f}) -> {'ELUCIDE' if elucide else 'NON ELUCIDE'}")

    # Ecriture CSV + JSON.
    import csv as _csv
    cols = ["dir", "version", "n", "control", "d_sat", "d_crit", "d_div", "d_null", "delta",
            "d_div_calc", "d_sat_calc", "pair", "pair_3e", "pair_4e", "sat_med_member",
            "div_sorted", "sat_sorted", "mask", "mfa", "n_fluxes_mode", "n_fluxes_div",
            "max_sep", "stability", "robustness", "sharpness", "l7a_dir", "l7a_conf",
            "trio_gap_E", "dfa"]
    with open(os.path.join(BASE, "v62_delta_levels.csv"), "w", newline="") as fh:
        w = _csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in cols})
    json.dump({"n_runs": len(rows), "n_v61": len(v61), "n_v62": len(v62),
               "mismatch_d_div": len(mis_div), "mismatch_d_sat": len(mis_sat),
               "predictions": results, "meilleure": best[0],
               "elucide": elucide,
               "mfa_valeurs_distinctes": mfa_vals,
               "masques": dict(Counter(r["mask"] for r in rows)),
               "paires": dict(Counter(r["pair"] for r in rows if r["pair"])),
               "dfa_extremes": [{"dir": r["dir"], "dfa": r["dfa"], "d_sat": r["d_sat"],
                                 "sat_med_member": r["sat_med_member"]} for r in dfa_extreme]},
              open(os.path.join(BASE, "v62_delta_levels.json"), "w"), indent=1, default=str)
    print("Ecrit : v62_delta_levels.csv, v62_delta_levels.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
