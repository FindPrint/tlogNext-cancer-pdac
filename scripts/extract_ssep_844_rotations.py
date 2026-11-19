#!/usr/bin/env python3
"""§8.44 — S_sep sur les 48 rotations de contrôle SANS doublon (§8.32/§8.41).
Lecture SEULE des master_results.json :
- 88 runs v6.2 du lot dédoublonné §8.44 (manifest_v62_dedup_844.txt),
- 4 paires déjà refaites au §8.41 (CLDN18 v6.1, CTLA4 v6.2 nul nouvelle
  permutation, ACO2 et PARP1 v6.2 nuls à permutation identique — les
  valeurs canoniques du §8.41.3).
AUCUN nouveau run du pipeline, AUCUN code modifié.
Formule gelée (PROTOCOL_v6.2.md §3) : S_sep = max_separation × stability,
lus dans run_pipeline.threshold_metadata.threshold_optimization.best_config.
Règles de comptage : comme verdict() de extract_phase2.py et comme en
§8.38/§8.41 — direction = signe de la somme des écarts réel−nul (par
famille ET sur les 48 paires) ; une paire « sépare » si |écart| > gigue ET
signe = direction majoritaire. Deux gigues : (A) gelée §3.4, gigue_eff =
max(gigue mesurée 0,00 ; plancher 0,07) = 0,07 ; (B) gigue mesurée seule,
0,00, rapportée à part.
Vérifications : version v6.2.0-L7aL7b-CohenD-short sur les 88 runs (v6.1
attendue pour CLDN18 seul) ; SHA-256 des 88 CSV dédoublonnés comparés à
dedup_844_csv_sha.json ; S_sep des 4 paires §8.41 relus comparés aux
valeurs publiées au §8.41.3 (tolérance 1e-4, arrondi 4 décimales).
Sorties : ssep_844_rotations.json, ssep_844_rotations.csv,
ssep_844_rotations.md.
"""
import csv
import hashlib
import json
import math
import os

BASE = os.path.dirname(os.path.abspath(__file__))
FAMILIES = [("V4ROT", "TCGA v4, ARN tumeurs, n=178"),
            ("DEPMAPROT", "CRISPR DepMap, lignées, n=45"),
            ("IMMROT", "immunitaire TCGA, ARN tumeurs, n=178"),
            ("PARPROT", "réparation de l'ADN TCGA, ARN tumeurs, n=178")]

# Paires déjà refaites au §8.41 (dossiers de sortie, version attendue).
# ACO2 / PARP1 : nuls à permutation identique (canoniques §8.41.3).
# CTLA4 : nul à nouvelle permutation (seul disponible ; passe sous les
# deux règles avec +0,8986, la permutation ne change pas son verdict).
# CLDN18 : run v6.1 préexistant (§8.32).
EXISTING = {
    ("V4ROT", "CLDN18"): ("results_fast_v61_v4r_cldn18_dedup",
                          "results_fast_v61_v4r_cldn18_dedup_nul",
                          "v6.1.0-L7aL7b-CohenD-short", None, None),
    ("IMMROT", "CTLA4"): ("results_fast_v62_immrot_ctla4_dedup",
                          "results_fast_v62_immrot_ctla4_dedup_nul",
                          "v6.2.0-L7aL7b-CohenD-short", None, None),
    ("DEPMAPROT", "ACO2"): ("results_fast_v62_depmaprot_aco2_dedup",
                            "results_fast_v62_depmaprot_aco2_dedup_nul_sp",
                            "v6.2.0-L7aL7b-CohenD-short", None, None),
    ("PARPROT", "PARP1"): ("results_fast_v62_parprot_parp1_dedup",
                           "results_fast_v62_parprot_parp1_dedup_nul_sp",
                           "v6.2.0-L7aL7b-CohenD-short", None, None),
}
# Écarts S_sep publiés au §8.41.3 (4 décimales) — vérification de relecture.
EXPECTED_841 = {("V4ROT", "CLDN18"): 0.6761, ("IMMROT", "CTLA4"): 0.8986,
                ("DEPMAPROT", "ACO2"): -0.0208, ("PARPROT", "PARP1"): 0.0168}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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
        if t0 is None:
            t0 = fnum(g(j, "cascade.T_0")) or fnum(g(j, "thresholds.T_0"))
        return {
            "version": j.get("version"),
            "n": j["reading_synthesis"]["n_samples"],
            "control": j.get("metadata", {}).get("control"),
            "mc": float(bc["score"]),
            "mc_thr": float(bc["threshold"]),
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


def classify(deltas, gigue):
    s = sum(deltas.values())
    direction = 1 if s > 0 else (-1 if s < 0 else 0)
    ok = [k for k, v in deltas.items()
          if direction != 0 and abs(v) > gigue and (1 if v > 0 else -1) == direction]
    ko = [k for k in deltas if k not in ok]
    return direction, ok, ko


def main():
    # --- 1. Manifeste 88 runs ---
    manifest = []
    for line in open(os.path.join(BASE, "manifest_v62_dedup_844.txt")):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, inp, out = line.split("|")
        manifest.append((name, inp, out))
    assert len(manifest) == 88, f"manifeste: {len(manifest)} lignes, attendu 88"

    # --- 2. SHA des 88 CSV dédoublonnés vs dedup_844_csv_sha.json ---
    shas = json.load(open(os.path.join(BASE, "dedup_844_csv_sha.json")))
    sha_checked, sha_mismatch, sha_missing = 0, [], []
    for name, inp, out in manifest:
        key = name[len("DEDUP844_"):]
        fam, ctrl = key.rsplit("_", 1) if not key.endswith("_NUL") else \
            key[:-4].rsplit("_", 1)
        # clé = FAM_CTRL ; le nom contient _NUL pour les nuls
        fam_ctrl = key[:-4] if key.endswith("_NUL") else key
        fam, ctrl = fam_ctrl.rsplit("_", 1)
        want = shas[f"{fam}_{ctrl}"]["nul" if key.endswith("_NUL") else "reel"]
        p = os.path.join(BASE, inp)
        if not os.path.exists(p):
            sha_missing.append(p)
            continue
        sha_checked += 1
        if sha256_file(p) != want:
            sha_mismatch.append(f"{p}: lu {sha256_file(p)[:12]} vs {want[:12]}")

    # --- 3. Lecture des 88 + 8 runs ---
    runs, missing, version_bad = {}, [], []
    for name, inp, out in manifest:
        val, err = read_run(out)
        if err:
            missing.append(f"{name}: {err}")
            continue
        runs[name] = val
        if val["version"] != "v6.2.0-L7aL7b-CohenD-short":
            version_bad.append(f"{name}: version {val['version']}")
    existing_runs = {}
    for (fam, ctrl), (rdir, ndir, ver, _a, _b) in EXISTING.items():
        for side, d in (("REEL", rdir), ("NUL", ndir)):
            val, err = read_run(d)
            if err:
                missing.append(f"EXISTING {fam}_{ctrl} {side}: {err}")
                continue
            existing_runs[f"{fam}_{ctrl}_{side}"] = val
            if val["version"] != ver:
                version_bad.append(f"EXISTING {fam}_{ctrl} {side}: {val['version']}")

    # --- 4. Paires ---
    pairs = {}
    for name, val in runs.items():
        base = name[len("DEDUP844_"):]
        base = base[:-4] if base.endswith("_NUL") else base
        pairs.setdefault(base, {})["NUL" if name.endswith("_NUL") else "REEL"] = val
    for (fam, ctrl) in EXISTING:
        pairs[f"{fam}_{ctrl}"] = {
            "REEL": existing_runs[f"{fam}_{ctrl}_REEL"],
            "NUL": existing_runs[f"{fam}_{ctrl}_NUL"]}
    assert len(pairs) == 48, f"paires: {len(pairs)}, attendu 48"
    assert all("REEL" in p and "NUL" in p for p in pairs.values()), "paire incomplète"

    # --- 5. Vérification des 4 écarts §8.41 ---
    ecarts_841 = []
    for (fam, ctrl), want in EXPECTED_841.items():
        r, n = pairs[f"{fam}_{ctrl}"]["REEL"], pairs[f"{fam}_{ctrl}"]["NUL"]
        got = r["ssep"] - n["ssep"]
        if abs(got - want) > 1e-4:
            ecarts_841.append(f"{fam}_{ctrl}: relu {got:.4f} vs §8.41 {want:.4f}")

    rows = []
    for fam, _title in FAMILIES:
        for base in sorted(p for p in pairs if p.startswith(fam + "_")):
            r, n = pairs[base]["REEL"], pairs[base]["NUL"]
            ctrl = base[len(fam) + 1:]
            rows.append({
                "famille": fam, "controle": ctrl, "n": r["n"],
                "source": "844" if base not in
                          [f"{f}_{c}" for (f, c) in EXISTING] else "841",
                "control_json": r["control"],
                "maxsep_R": r["maxsep"], "maxsep_N": n["maxsep"],
                "d_maxsep": r["maxsep"] - n["maxsep"],
                "stab_R": r["stab"], "stab_N": n["stab"],
                "ssep_R": r["ssep"], "ssep_N": n["ssep"],
                "d_ssep": r["ssep"] - n["ssep"],
                "mc_R": r["mc"], "mc_N": n["mc"], "d_mc": r["mc"] - n["mc"],
                "delta_R": r["delta"], "delta_N": n["delta"],
                "d_delta": (r["delta"] - n["delta"]
                            if r["delta"] is not None and n["delta"] is not None else None),
                "l7a_R": f"{r['l7a_dir']} {r['l7a_conf']:.3f}",
                "l7a_N": f"{n['l7a_dir']} {n['l7a_conf']:.3f}",
                "d_l7a": r["l7a_signed"] - n["l7a_signed"],
                "t0_R": r["t0"], "t0_N": n["t0"],
                "robust_R": r["robustness"], "robust_N": n["robustness"],
                "sharp_R": r["sharpness"], "sharp_N": n["sharpness"],
            })

    # --- 6. Verdicts : 44 nouvelles, 48 combinées, par famille et global ---
    verdicts = {}
    for scope, subset in (("44", [r for r in rows if r["source"] == "844"]),
                          ("48", rows)):
        for fam, _ in FAMILIES + [("TOUTES", "")]:
            sub = subset if fam == "TOUTES" else [r for r in subset if r["famille"] == fam]
            for key, label in (("d_ssep", "S_sep"), ("d_maxsep", "max_sep"),
                               ("d_mc", "MC"), ("d_delta", "Delta")):
                for gigue, glabel in ((0.07, "A_0.07"), (0.0, "B_0")):
                    deltas = {r["controle"]: r[key] for r in sub if r[key] is not None}
                    direction, ok, ko = classify(deltas, gigue)
                    verdicts[f"{scope}|{fam}|{label}|{glabel}"] = {
                        "direction": direction, "ok": ok, "ko": ko,
                        "n_ok": len(ok), "n": len(deltas),
                        "somme_ecarts": sum(deltas.values())}

    stab_ranges = {}
    for fam, _ in FAMILIES:
        sub = [r for r in rows if r["famille"] == fam]
        vals = [r["stab_R"] for r in sub] + [r["stab_N"] for r in sub]
        stab_ranges[fam] = {"min": min(vals), "max": max(vals)}
    all_stab = [r["stab_R"] for r in rows] + [r["stab_N"] for r in rows]
    stab_ranges["TOUTES"] = {"min": min(all_stab), "max": max(all_stab)}

    out = {"paires": rows, "verdicts": verdicts, "stab_ranges": stab_ranges,
           "controles": {"runs_lus": len(runs), "runs_existants_lus": len(existing_runs),
                         "paires": len(pairs), "manquants": missing,
                         "version_non_attendue": version_bad,
                         "ecarts_vs_841": ecarts_841,
                         "sha_csv_dedup_verifies": sha_checked,
                         "sha_csv_mismatch": sha_mismatch,
                         "sha_csv_fichiers_absents": sha_missing}}
    json.dump(out, open(os.path.join(BASE, "ssep_844_rotations.json"), "w"),
              indent=1, ensure_ascii=False)
    cols = ["famille", "controle", "n", "source", "maxsep_R", "maxsep_N", "d_maxsep",
            "stab_R", "stab_N", "ssep_R", "ssep_N", "d_ssep", "mc_R", "mc_N",
            "d_mc", "delta_R", "delta_N", "d_delta", "l7a_R", "l7a_N", "d_l7a",
            "t0_R", "t0_N"]
    with open(os.path.join(BASE, "ssep_844_rotations.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in cols})

    print(f"runs lus: {len(runs)}/88 (+{len(existing_runs)}/8 existants), paires: {len(pairs)}/48")
    print(f"manquants: {missing if missing else 'AUCUN'}")
    print(f"version non attendue: {version_bad if version_bad else 'AUCUNE'}")
    print(f"écarts vs §8.41: {ecarts_841 if ecarts_841 else 'AUCUN'}")
    print(f"SHA CSV dédoublonnés vérifiés: {sha_checked}, mismatch: "
          f"{sha_mismatch if sha_mismatch else 'AUCUN'}, absents: {sha_missing}")
    print(f"stabilité toutes paires: {stab_ranges['TOUTES']['min']:.4f}–"
          f"{stab_ranges['TOUTES']['max']:.4f}")
    for scope in ("44", "48"):
        for fam, _ in FAMILIES + [("TOUTES", "")]:
            for key, label in (("d_ssep", "S_sep"), ("d_maxsep", "max_sep")):
                for glabel in ("A_0.07", "B_0"):
                    v = verdicts[f"{scope}|{fam}|{label}|{glabel}"]
                    print(f"{scope} {fam} {label} ({glabel}): {v['n_ok']}/{v['n']} "
                          f"dir={v['direction']:+d} somme={v['somme_ecarts']:+.4f} "
                          f"ko={v['ko']}")
    print("écrit: ssep_844_rotations.json, ssep_844_rotations.csv")


if __name__ == "__main__":
    main()
