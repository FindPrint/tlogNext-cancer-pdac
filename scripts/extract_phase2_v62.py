#!/usr/bin/env python3
"""Phase 2 — discrimination reel/nul, sorties v6.2 (PROTOCOL_v6.2.md §6, gele 18 nov. 2026).
Copie de extract_phase2.py (SHA 5eb3ac24…75aa), etendue d'un 9e indicateur S_sep.
Lecture SEULE dans les master_results.json v6.2 deja sur disque + CSV d'entree
pour l'indicateur 6. AUCUN nouveau run du pipeline.
Gigues : Delta, cascade, falsification = 0 (déterministes) ; MC best_score,
max_separation, L7a = gigues MESUREES en validation v6.2 (§5, lues dans
v62_validation_table.json) ; S_sep : gigue_eff = max(gigue mesuree, 0,07) (§3.4).
Regles de comptage : fonction verdict() inchangee (direction = signe de la
somme des ecarts ; une paire separe si |ecart| > gigue ET signe = direction
majoritaire). S_sep = max_separation x stability (§3.1).
"""
import csv, json, math, os, sys
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
CASC = ["T_-2_F2_pre_onset", "T_-1_F1_pre_inflection", "T_0_Monte_Carlo_Central",
        "T_+1_F1_post_deceleration", "T_+2_F2_post_attractor"]

PAIRS = [  # (nom, dossier_reel, dossier_nul, csv_reel, csv_nul) — sorties v6.2 rep1
 ("HP35", "results_fast_v62_hp35", "results_fast_v62_hp35_nul",
  "/home/hatch/workspace/runs/biophysique-hp35/test_biophysique_input.csv", None),
 ("TCGA_v4", "results_fast_v62_tcga_v4", "results_fast_v62_tcga_v4_nul",
  "pdac_tcga_fluxes_v4.csv", "pdac_tcga_fluxes_v4_nul.csv"),
 ("GSE71729", "results_fast_v62_geo71729", "results_fast_v62_geo71729_nul",
  "pdac_geo71729_fluxes.csv", "pdac_geo71729_fluxes_nul.csv"),
 ("GSE62452", "results_fast_v62_geo62452", "results_fast_v62_geo62452_nul",
  "pdac_geo62452_fluxes.csv", "pdac_geo62452_fluxes_nul.csv"),
 ("ICGC", "results_fast_v62_icgc", "results_fast_v62_icgc_nul",
  "pdac_icgc_fluxes.csv", "pdac_icgc_fluxes_nul.csv"),
 ("IMMUNE_TCGA", "results_fast_v62_immune_tcga", "results_fast_v62_immune_tcga_nul",
  "pdac_immune_tcga_fluxes.csv", "pdac_immune_tcga_fluxes_nul.csv"),
 ("PARP_TCGA", "results_fast_v62_parp_tcga", "results_fast_v62_parp_tcga_nul",
  "pdac_tcga_fluxes_parp.csv", "pdac_tcga_fluxes_parp_nul.csv"),
 ("DEPMAP", "results_fast_v62_depmap", "results_fast_v62_depmap_nul",
  "pdac_depmap_fluxes.csv", "pdac_depmap_fluxes_nul.csv"),
]

# Gigues mesurees en validation v6.2 (v62_validation_table.json, §5) ; S_sep :
# gigue_eff = max(gigue mesuree, 0,07) (§3.4). Chargees ici, jamais supposees.
_JIT = json.load(open(os.path.join(BASE, "v62_validation_table.json")))["gigue_max"]
JIT_MC = _JIT["mc_score"]
JIT_MAXSEP = _JIT["max_sep"]
JIT_L7A = _JIT["l7a_signed"]
JIT_SSEP = max(_JIT["s_sep"], 0.07)

# Paires secondaires (annexe) : lot etendu v6.1 + Test A. Dirs lus depuis le CSV
# verifie v61_extended_compare.csv (lui-meme extrait des memes JSON).
SECONDARY = []
try:
    import csv as _csv
    _rows = list(_csv.DictReader(open(os.path.join(BASE, "v61_extended_compare.csv"))))
    _seen = {}
    for _r in _rows:
        if _r["status"] != "ok":
            continue
        _base = _r["serie"][:-4] if _r["serie"].endswith("_NUL") else _r["serie"]
        _seen.setdefault(_base, {})["NUL" if _r["serie"].endswith("_NUL") else "REEL"] = _r
    for _b, _p in sorted(_seen.items()):
        if "REEL" in _p and "NUL" in _p:
            # Dossiers v6.2 correspondants : meme suffixe, prefixe v62.
            _r62 = _p["REEL"]["out_v61"].replace("results_fast_v61_", "results_fast_v62_", 1)
            _n62 = _p["NUL"]["out_v61"].replace("results_fast_v61_", "results_fast_v62_", 1)
            SECONDARY.append((_b, _r62, _n62,
                              _p["REEL"]["input"], _p["NUL"]["input"]))
except FileNotFoundError:
    pass
SECONDARY.append(("TESTA_PROLIF", "results_fast_v62_prolif", "results_fast_v62_prolif_nul",
                  "pdac_tcga_fluxes_v4_prolif.csv", "pdac_tcga_fluxes_v4_prolif_nul.csv"))
# COAD reel refait apres v61_extended_compare.csv (dossier present sur disque,
# cf. §8.31/§8.32 : lot final 140/140) — ajoute a la main, memes regles.
SECONDARY.append(("COAD", "results_fast_v62_coad", "results_fast_v62_coad_nul",
                  "pdac_coad_fluxes.csv", "pdac_coad_fluxes_nul.csv"))


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


def extract(d):
    j = json.load(open(os.path.join(BASE, d, "master_results.json")))
    casc = [fnum(g(j, "five_threshold_cascade." + k)) for k in CASC]
    bc = g(j, "run_pipeline.threshold_metadata.threshold_optimization.best_config", {}) or {}
    l7 = g(j, "prediction_levels.L7a_coherence", {}) or {}
    return {
        "dir": d, "csv_path": g(j, "metadata.csv_path"),
        "n": fnum(g(j, "reading_synthesis.n_samples")),
        "cascade": casc,
        "l7a_dir": l7.get("consensus_direction"), "l7a_conf": fnum(l7.get("global_confidence")),
        "delta": fnum(g(j, "reading_synthesis.Delta_tension")),
        "mc_thr": fnum(bc.get("threshold")), "mc_score": fnum(bc.get("score")),
        "max_sep": fnum(g(bc, "metrics.max_separation")),
        "stability": fnum(g(bc, "metrics.stability")),
        "s_sep": ((fnum(g(bc, "metrics.max_separation")) * fnum(g(bc, "metrics.stability")))
                  if fnum(g(bc, "metrics.max_separation")) is not None
                  and fnum(g(bc, "metrics.stability")) is not None else None),
        "fals": fnum(g(j, "holographic_tension_state.falsification_vs_null.delta_vs_null")),
        "version": j.get("version") if isinstance(j.get("version"), str) else g(j, "version.master"),
    }


def cohen_d(a, b):
    a = np.asarray(a, dtype=float); b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    na, nb = len(a), len(b)
    va, vb = np.var(a, ddof=1), np.var(b, ddof=1)
    sp = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    return float("nan") if sp <= 0 else float((np.mean(b) - np.mean(a)) / sp)


def flux_coherence(csv_path, t0_pct, n, l7a_dir):
    """Retourne (fraction coherente, |d| median, nb flux lus, pas utilise, fenetre)."""
    if csv_path is None:
        return None, None, 0, None, None
    p = csv_path if os.path.isabs(csv_path) else os.path.join(BASE, csv_path)
    df = pd.read_csv(p)
    if len(df) != int(n):
        print(f"  ATTENTION {p}: lignes CSV {len(df)} != n JSON {n}", file=sys.stderr)
    flux_cols = list(df.columns[1:])
    # Exclure le doublon controle=flux si present (controle = 1re colonne).
    ctrl = df.columns[0]
    flux_cols = [c for c in flux_cols if c != ctrl]
    step = int(round(t0_pct / 100.0 * len(df)))
    w = 10 if len(df) < 100 else 20
    sgn = {"up": 1, "down": -1}.get(l7a_dir, 0)
    ds = []
    for c in flux_cols:
        v = df[c].to_numpy(dtype=float)
        z = (v - np.nanmean(v)) / np.nanstd(v, ddof=1)
        zb = z[max(0, step - w):step]
        za = z[step:min(len(df), step + w)]
        ds.append(cohen_d(zb, za))
    ds = [d for d in ds if math.isfinite(d)]
    if sgn == 0 or not ds:
        return None, (float(np.median([abs(d) for d in ds])) if ds else None), len(ds), step, w
    frac = sum(1 for d in ds if (d > 0) == (sgn > 0) and d != 0) / len(ds)
    return frac, float(np.median([abs(d) for d in ds])), len(ds), step, w


def signed_conf(d, c):
    if c is None:
        return None
    return {"up": c, "down": -c, "flat": 0.0}.get(d, None)


def analyse(pairs):
    out = []
    for name, dr, dn, cr, cn in pairs:
        R, N = extract(dr), extract(dn)
        # CSV du nul : si None (HP35), deduire du csv_path du JSON nul.
        if cn is None:
            cn = N["csv_path"]
        if cr is None:
            cr = R["csv_path"]
        fr, mr, nfr, step_r, w_r = flux_coherence(cr, R["cascade"][2], R["n"], R["l7a_dir"])
        fn, mn, nfn, step_n, w_n = flux_coherence(cn, N["cascade"][2], N["n"], N["l7a_dir"])
        casc_sum = sum(abs(a - b) for a, b in zip(R["cascade"], N["cascade"]))
        out.append({
            "paire": name, "n": R["n"], "version": R["version"],
            "delta_R": R["delta"], "delta_N": N["delta"], "d_delta": R["delta"] - N["delta"],
            "mc_thr_R": R["mc_thr"], "mc_thr_N": N["mc_thr"], "d_mc_thr": R["mc_thr"] - N["mc_thr"],
            "mc_R": R["mc_score"], "mc_N": N["mc_score"], "d_mc": R["mc_score"] - N["mc_score"],
            "maxsep_R": R["max_sep"], "maxsep_N": N["max_sep"], "d_maxsep": R["max_sep"] - N["max_sep"],
            "stab_R": R["stability"], "stab_N": N["stability"],
            "ssep_R": R["s_sep"], "ssep_N": N["s_sep"], "d_ssep": R["s_sep"] - N["s_sep"],
            "T0_R": R["cascade"][2], "T0_N": N["cascade"][2], "d_T0": abs(R["cascade"][2] - N["cascade"][2]),
            "fals_R": R["fals"], "fals_N": N["fals"],
            "d_fals": (R["fals"] - N["fals"]) if R["n"] >= 75 else None,
            "fals_dispo": R["n"] >= 75,
            "frac_R": fr, "frac_N": fn, "d_frac": (fr - fn) if fr is not None and fn is not None else None,
            "medd_R": mr, "medd_N": mn, "d_medd": (mr - mn) if mr is not None and mn is not None else None,
            "nflux": nfr, "step_R": step_r, "step_N": step_n, "window": w_r,
            "l7a_R": f"{R['l7a_dir']} {R['l7a_conf']:.3f}" if R["l7a_conf"] is not None else str(R["l7a_dir"]),
            "l7a_N": f"{N['l7a_dir']} {N['l7a_conf']:.3f}" if N["l7a_conf"] is not None else str(N["l7a_dir"]),
            "l7a_s_R": signed_conf(R["l7a_dir"], R["l7a_conf"]),
            "l7a_s_N": signed_conf(N["l7a_dir"], N["l7a_conf"]),
            "d_l7a": signed_conf(R["l7a_dir"], R["l7a_conf"]) - signed_conf(N["l7a_dir"], N["l7a_conf"]),
            "casc_R": R["cascade"], "casc_N": N["cascade"], "casc_sum": casc_sum,
        })
    return out


def verdict(gaps, jitter, denom=None):
    """gaps: liste d'ecarts (None = indisponible, exclu). Retourne (X, liste_ok, liste_ko, direction)."""
    vals = [(i, x) for i, x in enumerate(gaps) if x is not None]
    if not vals:
        return 0, [], [], 0
    s = sum(x for _, x in vals)
    direction = 1 if s > 0 else (-1 if s < 0 else 0)
    ok, ko = [], []
    for i, x in vals:
        if direction != 0 and abs(x) > jitter and (1 if x > 0 else -1) == direction:
            ok.append(i)
        else:
            ko.append(i)
    return len(ok), ok, ko, direction


def main():
    rows = analyse(PAIRS)
    names = [r["paire"] for r in rows]
    checks = [
        ("1 Delta", [r["d_delta"] for r in rows], 0.0),
        ("2 MC best_score", [r["d_mc"] for r in rows], JIT_MC),
        ("3 max_separation", [r["d_maxsep"] for r in rows], JIT_MAXSEP),
        ("4 |T0 reel - T0 nul|", [r["d_T0"] for r in rows], 0.0),
        ("5 falsification delta_vs_null", [r["d_fals"] for r in rows], 0.0),
        ("6 coherence par flux (fraction)", [r["d_frac"] for r in rows], 0.0),
        ("6b |d| median a T0", [r["d_medd"] for r in rows], 0.0),
        ("7 L7a confiance signee", [r["d_l7a"] for r in rows], JIT_L7A),
        ("8 ecart cascade complet", [r["casc_sum"] for r in rows], 0.0),
        ("9 S_sep = max_separation x stability", [r["d_ssep"] for r in rows], JIT_SSEP),
    ]
    print(f"=== PHASE 2 — 8 paires principales (v6.2, lecture seule) ===")
    print(f"Gigues mesurees validation v6.2 : MC={JIT_MC} max_sep={JIT_MAXSEP} L7a={JIT_L7A} "
          f"S_sep_eff=max(mesuree, 0,07)={JIT_SSEP} ; Delta/cascade/fals=0")
    for r in rows:
        print(f"{r['paire']} n={r['n']:.0f} {r['version']} | Delta {r['delta_R']:.2f}/{r['delta_N']:.2f} "
              f"| MC {r['mc_R']:.4f}/{r['mc_N']:.4f} thr {r['mc_thr_R']:.2f}/{r['mc_thr_N']:.2f} "
              f"| maxsep {r['maxsep_R']:.4f}/{r['maxsep_N']:.4f} stab {r['stab_R']:.4f}/{r['stab_N']:.4f} "
              f"S_sep {r['ssep_R']:.4f}/{r['ssep_N']:.4f} | T0 {r['T0_R']:.2f}/{r['T0_N']:.2f} "
              f"| fals {r['fals_R']}/{r['fals_N']} dispo={r['fals_dispo']} "
              f"| frac {r['frac_R']}/{r['frac_N']} medd {r['medd_R']}/{r['medd_N']} "
              f"(pas {r['step_R']}/{r['step_N']}, fenetre ±{r['window']}, flux {r['nflux']}) "
              f"| L7a {r['l7a_R']} / {r['l7a_N']} | casc_sum {r['casc_sum']:.2f}")
    print()
    summary = {}
    for label, gaps, jit in checks:
        x, ok, ko, direction = verdict(gaps, jit)
        denom = sum(1 for v in gaps if v is not None)
        summary[label] = (x, denom, [names[i] for i in ok], [names[i] for i in ko], direction)
        print(f"{label}: separe {x}/{denom} direction {'+' if direction>0 else '-'} "
              f"OK={summary[label][2]} KO={summary[label][3]}")
    # Indicateur 6 combine : fraction ET med|d| doivent pointer reel > nul.
    ok6 = [i for i in range(len(rows))
           if rows[i]["d_frac"] is not None and rows[i]["d_medd"] is not None
           and rows[i]["d_frac"] > 0 and rows[i]["d_medd"] > 0]
    print(f"6 COMBINE (frac>0 ET med|d|>0): separe {len(ok6)}/8 OK={[names[i] for i in ok6]} "
          f"KO={[names[i] for i in range(len(rows)) if i not in ok6]}")
    summary["6 COMBINE"] = (len(ok6), 8, [names[i] for i in ok6],
                            [names[i] for i in range(len(rows)) if i not in ok6], 1)

    # Annexe : paires secondaires, memes regles.
    sec = analyse(SECONDARY)
    print(f"\n=== ANNEXE — {len(sec)} paires secondaires ===")
    for r in sec:
        print(f"{r['paire']} n={r['n']:.0f} | dDelta {r['d_delta']:+.2f} | dMC {r['d_mc']:+.4f} "
              f"| dMaxSep {r['d_maxsep']:+.4f} | dSsep {r['d_ssep']:+.4f} | dT0 {r['d_T0']:.2f} | dFals {r['d_fals']} "
              f"| dFrac {r['d_frac']} dMedd {r['d_medd']} | dL7a {r['d_l7a']:+.3f} | casc_sum {r['casc_sum']:.2f}")
    for label, key, jit in [("1 Delta", "d_delta", 0.0), ("2 MC", "d_mc", JIT_MC),
                            ("3 maxsep", "d_maxsep", JIT_MAXSEP), ("4 dT0", "d_T0", 0.0),
                            ("5 fals", "d_fals", 0.0), ("6 frac", "d_frac", 0.0),
                            ("7 L7a", "d_l7a", JIT_L7A), ("8 casc", "casc_sum", 0.0),
                            ("9 S_sep", "d_ssep", JIT_SSEP)]:
        gaps = [r[key] for r in sec]
        x, ok, ko, direction = verdict(gaps, jit)
        denom = sum(1 for v in gaps if v is not None)
        print(f"annexe {label}: {x}/{denom} direction {'+' if direction>0 else '-'} "
              f"OK={[sec[i]['paire'] for i in ok]}")

    # Ecriture CSV + JSON brut.
    cols = ["paire", "n", "delta_R", "delta_N", "d_delta", "mc_thr_R", "mc_thr_N", "d_mc_thr",
            "mc_R", "mc_N", "d_mc", "maxsep_R", "maxsep_N", "d_maxsep", "stab_R", "stab_N",
            "ssep_R", "ssep_N", "d_ssep", "T0_R", "T0_N", "d_T0",
            "fals_R", "fals_N", "d_fals", "fals_dispo", "frac_R", "frac_N", "d_frac",
            "medd_R", "medd_N", "d_medd", "nflux", "step_R", "step_N", "window",
            "l7a_R", "l7a_N", "d_l7a", "casc_sum"]
    with open(os.path.join(BASE, "v62_phase2_table.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["groupe"] + cols)
        w.writeheader()
        for r in rows:
            w.writerow({"groupe": "principale", **{k: r.get(k, "") for k in cols}})
        for r in sec:
            w.writerow({"groupe": "secondaire", **{k: r.get(k, "") for k in cols}})
    json.dump({"principal": rows, "secondaire": sec,
               "gigues": {"mc": JIT_MC, "maxsep": JIT_MAXSEP, "l7a": JIT_L7A, "ssep_eff": JIT_SSEP},
               "verdicts": {k: {"x": v[0], "denom": v[1], "ok": v[2], "ko": v[3], "direction": v[4]}
                            for k, v in summary.items()}},
              open(os.path.join(BASE, "v62_phase2_table.json"), "w"), indent=1, default=str)
    print("\nEcrit : v62_phase2_table.csv, v62_phase2_table.json")


if __name__ == "__main__":
    main()
