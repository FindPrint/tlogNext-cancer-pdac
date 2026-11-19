#!/usr/bin/env python3
"""§8.41 — S_sep sur les 48 rotations de contrôle (§8.32), sorties v6.1.
Lecture SEULE des 96 master_results.json v6.1 listés dans
manifest_v61_rotations.txt. AUCUN nouveau run du pipeline, AUCUN code modifié.
Formule gelée (PROTOCOL_v6.2.md §3) : S_sep = max_separation × stability,
lus dans run_pipeline.threshold_metadata.threshold_optimization.best_config.
Règles de comptage : comme verdict() de extract_phase2.py — direction =
signe de la somme des écarts réel−nul (par famille ET sur les 48 paires) ;
une paire « sépare » si |écart| > gigue ET signe = direction majoritaire.
Deux gigues, comme en §8.38 : (A) gelée §3.4, gigue_eff = max(gigue mesurée
0,00 ; plancher 0,07) = 0,07 ; (B) gigue mesurée seule, 0,00, rapportée à part.
Vérifications : version v6.1 dans les 96 JSON ; MC et Delta relus comparés à
v61_rotations_extract.csv (tolérance 1e-9) ; SHA-256 des 96 CSV d'entrée
comparés à PROVENANCE_rotations_v61.md (bloc JSON) ; doublon contrôle=flux
vérifié sur l'en-tête d'un CSV par famille (le flux contrôle apparaît deux
fois : 1re colonne = contrôle, et colonne analysée) — S_sep est lu dans
best_config (global), il n'est pas affecté par le doublon ; aucune lecture
par flux n'est faite ici.
Sorties : ssep_841_rotations.json, ssep_841_rotations.csv, ssep_841_rotations.md.
"""
import csv
import hashlib
import json
import math
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
FAMILIES = [("V4ROT", "TCGA v4, ARN tumeurs, n=178"),
            ("DEPMAPROT", "CRISPR DepMap, lignées, n=45"),
            ("IMMROT", "immunitaire TCGA, ARN tumeurs, n=178"),
            ("PARPROT", "réparation de l'ADN TCGA, ARN tumeurs, n=178")]


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
        if t0 is None:  # repli : anciennes clés possibles
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
    """deltas: dict nom -> écart. Retourne (direction, ok, ko)."""
    s = sum(deltas.values())
    direction = 1 if s > 0 else (-1 if s < 0 else 0)
    ok = [k for k, v in deltas.items()
          if direction != 0 and abs(v) > gigue and (1 if v > 0 else -1) == direction]
    ko = [k for k in deltas if k not in ok]
    return direction, ok, ko


def main():
    # --- 1. Manifeste : 96 runs ---
    manifest = []
    for line in open(os.path.join(BASE, "manifest_v61_rotations.txt")):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, inp, out = line.split("|")
        manifest.append((name, inp, out))
    assert len(manifest) == 96, f"manifeste: {len(manifest)} lignes, attendu 96"

    # --- 2. SHA des 96 CSV d'entrée vs PROVENANCE_rotations_v61.md ---
    prov_text = open(os.path.join(BASE, "PROVENANCE_rotations_v61.md")).read()
    m = re.search(r"```json\n(.*?)```", prov_text, re.S)
    prov = json.loads(m.group(1))
    sha_mismatch, sha_checked, sha_missing_file = [], 0, []
    for jeu in prov["jeux"].values():
        for rot, rec in jeu["rotations"].items():
            for key in ("fichier", "nul"):
                p = rec[key]
                if not os.path.exists(p):
                    sha_missing_file.append(p)
                    continue
                sha_checked += 1
                got = sha256_file(p)
                want = rec["sha256" if key == "fichier" else "sha256_nul"]
                if got != want:
                    sha_mismatch.append(f"{p}: lu {got} vs provenance {want}")
    # SHA des 4 bases
    base_sha = {}
    for jeu_nom, jeu in prov["jeux"].items():
        p = os.path.join(BASE, jeu["base"])
        base_sha[jeu_nom] = {"fichier": jeu["base"],
                             "sha256_lu": sha256_file(p) if os.path.exists(p) else None,
                             "sha256_provenance": jeu["sha256_base"],
                             "conforme": (os.path.exists(p) and
                                          sha256_file(p) == jeu["sha256_base"])}

    # --- 3. Lecture des 96 JSON ---
    runs = {}
    missing, version_bad = [], []
    for name, inp, out in manifest:
        val, err = read_run(out)
        if err:
            missing.append(f"{name}: {err}")
            continue
        runs[name] = val
        if val["version"] != "v6.1.0-L7aL7b-CohenD-short":
            version_bad.append(f"{name}: version {val['version']}")

    # --- 4. Comparaison MC / Delta vs v61_rotations_extract.csv ---
    csv_rows = {r["name"]: r for r in csv.DictReader(
        open(os.path.join(BASE, "v61_rotations_extract.csv")))}
    diffs_csv = []
    for name, val in runs.items():
        row = csv_rows.get(name)
        if row is None:
            diffs_csv.append(f"{name}: absent de v61_rotations_extract.csv")
            continue
        for key_json, key_csv in (("mc", "MC"), ("delta", "Delta")):
            try:
                ref = float(row[key_csv])
            except (TypeError, ValueError):
                continue
            got = val[key_json]
            if got is None or abs(got - ref) > 1e-9:
                diffs_csv.append(f"{name} {key_csv}: relu {got} vs csv {ref}")

    # --- 5. Paires réel/nul, par famille ---
    pairs = {}
    for name, val in runs.items():
        base = name[:-4] if name.endswith("_NUL") else name
        pairs.setdefault(base, {})["NUL" if name.endswith("_NUL") else "REEL"] = val
    assert len(pairs) == 48, f"paires: {len(pairs)}, attendu 48"
    assert all("REEL" in p and "NUL" in p for p in pairs.values()), "paire incomplète"

    rows = []
    for fam, _title in FAMILIES:
        for base in sorted(p for p in pairs if p.startswith(fam + "_")):
            r, n = pairs[base]["REEL"], pairs[base]["NUL"]
            ctrl = base[len(fam) + 1:]
            rows.append({
                "famille": fam, "controle": ctrl, "n": r["n"],
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

    # --- 6. Verdicts par famille et global, règles (A) et (B), S_sep et max_sep ---
    verdicts = {}
    for fam, _ in FAMILIES + [("TOUTES", "")]:
        subset = rows if fam == "TOUTES" else [r for r in rows if r["famille"] == fam]
        for key, label in (("d_ssep", "S_sep"), ("d_maxsep", "max_sep")):
            for gigue, glabel in ((0.07, "A_0.07"), (0.0, "B_0")):
                deltas = {r["controle"]: r[key] for r in subset}
                direction, ok, ko = classify(deltas, gigue)
                verdicts[f"{fam}|{label}|{glabel}"] = {
                    "direction": direction, "ok": ok, "ko": ko, "n_ok": len(ok),
                    "n": len(deltas), "somme_ecarts": sum(deltas.values())}

    # Stabilité : plages par famille
    stab_ranges = {}
    for fam, _ in FAMILIES:
        sub = [r for r in rows if r["famille"] == fam]
        vals = [r["stab_R"] for r in sub] + [r["stab_N"] for r in sub]
        stab_ranges[fam] = {"min": min(vals), "max": max(vals)}
    all_stab = [r["stab_R"] for r in rows] + [r["stab_N"] for r in rows]
    stab_ranges["TOUTES"] = {"min": min(all_stab), "max": max(all_stab)}

    # Doublon contrôle=flux : vérifié sur l'en-tête d'un CSV par famille
    doublon = {}
    for fam, _ in FAMILIES:
        sample = [r for r in rows if r["famille"] == fam][0]
        csv_path = os.path.join(BASE, [x[1] for x in manifest
                                       if x[0] == f"{fam}_{sample['controle']}"][0])
        header = open(csv_path).readline().strip().split(",")
        doublon[fam] = {"csv": os.path.basename(csv_path),
                        "controle": sample["controle"],
                        "occurrences_dans_en_tete": header.count(sample["controle"]),
                        "premiere_colonne": header[0]}

    out = {"paires": rows, "verdicts": verdicts, "stab_ranges": stab_ranges,
           "doublon_controle_flux": doublon,
           "controles": {"runs_lus": len(runs), "paires": len(pairs),
                         "manquants": missing, "version_non_v61": version_bad,
                         "ecarts_vs_csv_v61_rotations": diffs_csv,
                         "sha_csv_rotations_verifies": sha_checked,
                         "sha_csv_mismatch": sha_mismatch,
                         "sha_csv_fichiers_absents": sha_missing_file,
                         "sha_bases": base_sha}}
    json.dump(out, open(os.path.join(BASE, "ssep_841_rotations.json"), "w"),
              indent=1, ensure_ascii=False)
    cols = ["famille", "controle", "n", "maxsep_R", "maxsep_N", "d_maxsep",
            "stab_R", "stab_N", "ssep_R", "ssep_N", "d_ssep", "mc_R", "mc_N",
            "d_mc", "delta_R", "delta_N", "d_delta", "l7a_R", "l7a_N", "d_l7a",
            "t0_R", "t0_N"]
    with open(os.path.join(BASE, "ssep_841_rotations.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in cols})

    print(f"runs lus: {len(runs)}/96, paires: {len(pairs)}/48")
    print(f"manquants: {missing if missing else 'AUCUN'}")
    print(f"version non v6.1: {version_bad if version_bad else 'AUCUNE'}")
    print(f"écarts MC/Delta vs v61_rotations_extract.csv: "
          f"{diffs_csv if diffs_csv else 'AUCUN'}")
    print(f"SHA CSV rotations vérifiés: {sha_checked}, mismatch: "
          f"{sha_mismatch if sha_mismatch else 'AUCUN'}, absents: {sha_missing_file}")
    print(f"SHA bases conformes: {all(v['conforme'] for v in base_sha.values())}")
    print(f"doublon contrôle=flux (occurrences dans l'en-tête): "
          f"{ {k: v['occurrences_dans_en_tete'] for k, v in doublon.items()} }")
    print(f"stabilité toutes paires: {stab_ranges['TOUTES']['min']:.4f}–"
          f"{stab_ranges['TOUTES']['max']:.4f}")
    for fam, _ in FAMILIES + [("TOUTES", "")]:
        for key, label in (("d_ssep", "S_sep"), ("d_maxsep", "max_sep")):
            for glabel in ("A_0.07", "B_0"):
                v = verdicts[f"{fam}|{label}|{glabel}"]
                print(f"{fam} {label} ({glabel}): {v['n_ok']}/{v['n']} "
                      f"dir={v['direction']:+d} somme={v['somme_ecarts']:+.4f} "
                      f"ok={v['ok']} ko={v['ko']}")
    print("écrit: ssep_841_rotations.json, ssep_841_rotations.csv")


if __name__ == "__main__":
    main()
