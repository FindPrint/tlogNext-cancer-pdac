#!/usr/bin/env python3
"""Chantier §8.59 — trancher l'adoption de maxsep seul comme score MC
(PROTOCOL_maxsep_adoption_859.md). Lecture SEULE des master_results.json
v6.2/v6.1 deja sur disque. AUCUN run du pipeline, AUCUN code modifie.
Re-ecriture propre (ne reutilise PAS les fonctions de
extract_sep_maxsep_856.py) : autre parcours des JSON, autres noms,
autre structure de comptage.

Scores (relectures du best_config ANCIEN, selection inchangee) :
  maxsep = best_config.metrics.max_separation  (|d de Cohen|, [0, inf[)
  sep    = maxsep / (1 + maxsep)               ([0, 1[)
  mc_old = best_config.score (ancien composite, garde-fou)

Portes d'adoption (protocole §4) :
  D1 re-confirmation A1>=30/48, A2>=6/8 et >=7/8 positifs, A3 HP35>=0,30
  D2 exactitude (second calcul + recoupements 1e-9 + SHA) — D2a/b/c ici,
     D2d (SHA) verifie en shell et consigne au rapport
  D3 leave-one-out : V1 toute suppression d'1 paire -> >=6/7 restantes ;
     V2 toute suppression d'1 paire -> >=30/47 restantes
  D4 plancher equivalent-sep par paire : A2 tient-il a echelle egale ?
  D5a 0 changement de classe de separation maxsep vs §8.56 publie ;
  D5b 0 changement de classe de signe entre d_maxsep et d_sep
Sorties : maxsep_adoption_859_table.csv / maxsep_adoption_859_table.json
"""
import csv
import json
import math
import os

BASE = os.path.dirname(os.path.abspath(__file__))
FLOOR = 0.07
COHEN_SMALL = 0.20
VERSIONS_OK = {"v6.2.0-L7aL7b-CohenD-short", "v6.1.0-L7aL7b-CohenD-short"}

MAIN = [
    ("HP35", "results_fast_v62_hp35", "results_fast_v62_hp35_nul"),
    ("TCGA_v4", "results_fast_v62_tcga_v4", "results_fast_v62_tcga_v4_nul"),
    ("GSE71729", "results_fast_v62_geo71729", "results_fast_v62_geo71729_nul"),
    ("GSE62452", "results_fast_v62_geo62452", "results_fast_v62_geo62452_nul"),
    ("ICGC", "results_fast_v62_icgc", "results_fast_v62_icgc_nul"),
    ("IMMUNE_TCGA", "results_fast_v62_immune_tcga",
     "results_fast_v62_immune_tcga_nul"),
    ("PARP_TCGA", "results_fast_v62_parp_tcga",
     "results_fast_v62_parp_tcga_nul"),
    ("DEPMAP", "results_fast_v62_depmap", "results_fast_v62_depmap_nul"),
]
EXTRA = [
    ("TESTA_PROLIF", "results_fast_v62_prolif", "results_fast_v62_prolif_nul"),
    ("MTAP_PRMT5FLUX", "results_fast_v62_prmt5flux",
     "results_fast_v62_prmt5flux_nul"),
    ("MTAP_SERIES", "results_fast_v62_mtap", "results_fast_v62_mtap_nul"),
    ("V4R_PURITY", "results_fast_v62_v4r_purity",
     "results_fast_v62_v4r_purity_nul"),
]
# Paires rotations deja connues hors manifest (cf. §8.44 / §8.41).
EXTRA_ROT = {
    ("V4ROT", "CLDN18"): ("results_fast_v61_v4r_cldn18_dedup",
                          "results_fast_v61_v4r_cldn18_dedup_nul"),
    ("IMMROT", "CTLA4"): ("results_fast_v62_immrot_ctla4_dedup",
                          "results_fast_v62_immrot_ctla4_dedup_nul"),
    ("DEPMAPROT", "ACO2"): ("results_fast_v62_depmaprot_aco2_dedup",
                            "results_fast_v62_depmaprot_aco2_dedup_nul_sp"),
    ("PARPROT", "PARP1"): ("results_fast_v62_parprot_parp1_dedup",
                           "results_fast_v62_parprot_parp1_dedup_nul_sp"),
}


def read_run(folder):
    """Lit un dossier de run ; renvoie un dict ou leve ValueError."""
    path = os.path.join(BASE, folder, "master_results.json")
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    opt = raw["run_pipeline"]["threshold_metadata"]["threshold_optimization"]
    best = opt["best_config"]
    vals = best["metrics"]
    msep = vals["max_separation"]
    if not isinstance(msep, (int, float)) or not math.isfinite(msep) or msep < 0:
        raise ValueError(f"maxsep invalide {msep!r} dans {path}")
    msep = float(msep)
    return {
        "maxsep": msep,
        "sep": msep / (1.0 + msep) if msep else 0.0,
        "mc_old": float(best["score"]),
        "version": raw.get("version"),
        "n": raw["reading_synthesis"]["n_samples"],
    }


def rotation_folders():
    """Reconstruit les 48 paires rotations depuis le manifest §8.44."""
    found = {}
    man_path = os.path.join(BASE, "manifest_v62_dedup_844.txt")
    with open(man_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            run_id, _src, outdir = line.split("|")
            stem = run_id[len("DEDUP844_"):]
            is_nul = stem.endswith("_NUL")
            if is_nul:
                stem = stem[:-4]
            fam, ctrl = stem.rsplit("_", 1)
            slot = found.setdefault((fam, ctrl), {})
            slot["NUL" if is_nul else "REEL"] = outdir
    for key, (rdir, ndir) in EXTRA_ROT.items():
        found[key] = {"REEL": rdir, "NUL": ndir}
    return found


def separates(gaps, floor):
    """Comptage protocole §3 : direction = signe de la somme ; une paire
    separe si |ecart| > floor et signe = direction. Renvoie (n_ok, n,
    n_pos, total, ok_set)."""
    total = sum(gaps.values())
    direction = 0
    if total > 0:
        direction = 1
    elif total < 0:
        direction = -1
    ok = set()
    n_pos = 0
    for name, gap in gaps.items():
        if gap > 0:
            n_pos += 1
        if direction != 0 and abs(gap) > floor and (
                (gap > 0) == (direction > 0)):
            ok.add(name)
    return len(ok), len(gaps), n_pos, total, ok


def loo_worst(gaps, floor, bar):
    """Leave-one-out exhaustif : pour chaque paire retiree, compte les
    paires restantes qui separent (meme regle). Renvoie (passe, pire cas,
    liste des suppressions qui font echouer la barre)."""
    fails = []
    worst = None
    for dropped in sorted(gaps):
        rest = {k: v for k, v in gaps.items() if k != dropped}
        n_ok, _n, _p, _t, _o = separates(rest, floor)
        if worst is None or n_ok < worst[1]:
            worst = (dropped, n_ok)
        if n_ok < bar:
            fails.append({"retiree": dropped, "n_ok_restant": n_ok,
                          "n_restant": len(rest)})
    return (len(fails) == 0), worst, fails


def main():
    missing = []
    bad_versions = []
    rows = []

    def add_pair(scope, name, dir_r, dir_n):
        try:
            rrun = read_run(dir_r)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            missing.append(f"{name} REEL: {exc}")
            return
        try:
            nrun = read_run(dir_n)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            missing.append(f"{name} NUL: {exc}")
            return
        for side, run in (("REEL", rrun), ("NUL", nrun)):
            if run["version"] not in VERSIONS_OK:
                bad_versions.append(f"{name} {side}: {run['version']}")
        rows.append({
            "scope": scope, "paire": name, "n": rrun["n"],
            "maxsep_R": rrun["maxsep"], "maxsep_N": nrun["maxsep"],
            "d_maxsep": rrun["maxsep"] - nrun["maxsep"],
            "sep_R": rrun["sep"], "sep_N": nrun["sep"],
            "d_sep": rrun["sep"] - nrun["sep"],
            "mc_old_R": rrun["mc_old"], "mc_old_N": nrun["mc_old"],
            "d_mc_old": rrun["mc_old"] - nrun["mc_old"],
            "plancher_maxsep_equiv_sep":
                FLOOR * (1.0 + rrun["maxsep"]) * (1.0 + nrun["maxsep"]),
            "version_R": rrun["version"], "version_N": nrun["version"],
        })

    for name, dr, dn in MAIN:
        add_pair("V1_principales", name, dr, dn)
    for (fam, ctrl), sides in sorted(rotation_folders().items()):
        add_pair("V2_rotations", f"{fam}_{ctrl}", sides["REEL"], sides["NUL"])
    for name, dr, dn in EXTRA:
        add_pair("V3_V4_V5_descriptif", name, dr, dn)

    v1 = [r for r in rows if r["scope"] == "V1_principales"]
    v2 = [r for r in rows if r["scope"] == "V2_rotations"]
    gaps_m_v1 = {r["paire"]: r["d_maxsep"] for r in v1}
    gaps_s_v1 = {r["paire"]: r["d_sep"] for r in v1}
    gaps_m_v2 = {r["paire"]: r["d_maxsep"] for r in v2}
    gaps_s_v2 = {r["paire"]: r["d_sep"] for r in v2}
    gaps_o_v1 = {r["paire"]: r["d_mc_old"] for r in v1}
    gaps_o_v2 = {r["paire"]: r["d_mc_old"] for r in v2}

    # --- D1 : re-confirmation des barres §8.56 ---
    a1_m = separates(gaps_m_v2, FLOOR)
    a1_s = separates(gaps_s_v2, FLOOR)
    a2_m = separates(gaps_m_v1, FLOOR)
    a2_s = separates(gaps_s_v1, FLOOR)
    hp = next(r for r in v1 if r["paire"] == "HP35")
    d1 = {
        "A1_rotations_maxsep": {"n_ok": a1_m[0], "n": a1_m[1],
                                "barre": 30, "passe": a1_m[0] >= 30,
                                "n_positifs": a1_m[2], "somme": a1_m[3],
                                "moyenne": a1_m[3] / a1_m[1]},
        "A1_rotations_sep": {"n_ok": a1_s[0], "n": a1_s[1],
                             "n_positifs": a1_s[2], "somme": a1_s[3],
                             "moyenne": a1_s[3] / a1_s[1]},
        "A2_principales_maxsep": {"n_ok": a2_m[0], "n": a2_m[1],
                                  "barre": 6, "passe": a2_m[0] >= 6,
                                  "n_positifs": a2_m[2],
                                  "barre_positifs": 7,
                                  "passe_positifs": a2_m[2] >= 7,
                                  "somme": a2_m[3],
                                  "moyenne": a2_m[3] / a2_m[1]},
        "A2_principales_sep": {"n_ok": a2_s[0], "n": a2_s[1],
                               "n_positifs": a2_s[2], "somme": a2_s[3],
                               "moyenne": a2_s[3] / a2_s[1]},
        "A3_HP35_maxsep": {"d_maxsep": hp["d_maxsep"], "barre": 0.30,
                           "passe": hp["d_maxsep"] >= 0.30},
        "A3_HP35_sep": {"d_sep": hp["d_sep"]},
        "A3_HP35_mc_old": {"d_mc_old": hp["d_mc_old"]},
    }
    d1["passe"] = bool(d1["A1_rotations_maxsep"]["passe"]
                       and d1["A2_principales_maxsep"]["passe"]
                       and d1["A2_principales_maxsep"]["passe_positifs"]
                       and d1["A3_HP35_maxsep"]["passe"])

    # --- D3 : leave-one-out exhaustif ---
    loo_v1_ok, loo_v1_worst, loo_v1_fails = loo_worst(gaps_m_v1, FLOOR, 6)
    loo_v2_ok, loo_v2_worst, loo_v2_fails = loo_worst(gaps_m_v2, FLOOR, 30)
    d3 = {
        "V1_passe": loo_v1_ok, "V1_pire_cas": list(loo_v1_worst),
        "V1_suppressions_echouant": loo_v1_fails,
        "V2_passe": loo_v2_ok, "V2_pire_cas": list(loo_v2_worst),
        "V2_suppressions_echouant": loo_v2_fails,
    }
    d3["passe"] = bool(loo_v1_ok and loo_v2_ok)

    # --- D4 : plancher equivalent-sep, paire par paire (A2) ---
    d4_ok_v1 = []
    d4_ko_v1 = []
    for r in v1:
        if r["d_maxsep"] > r["plancher_maxsep_equiv_sep"]:
            d4_ok_v1.append(r["paire"])
        else:
            d4_ko_v1.append(r["paire"])
    n_pos_v1 = sum(1 for r in v1 if r["d_maxsep"] > 0)
    d4 = {
        "V1_n_ok_plancher_equiv": len(d4_ok_v1), "V1_n": len(v1),
        "V1_barre": 6, "V1_passe": len(d4_ok_v1) >= 6,
        "V1_n_positifs": n_pos_v1, "V1_passe_positifs": n_pos_v1 >= 7,
        "V1_ok": d4_ok_v1, "V1_ko": d4_ko_v1,
        "V1_passent_litteral_pas_equiv": [
            r["paire"] for r in v1
            if r["d_maxsep"] > FLOOR
            and r["d_maxsep"] <= r["plancher_maxsep_equiv_sep"]],
        "V2_passent_litteral_pas_equiv": [
            r["paire"] for r in v2
            if r["d_maxsep"] > FLOOR
            and r["d_maxsep"] <= r["plancher_maxsep_equiv_sep"]],
    }
    d4["passe"] = bool(d4["V1_passe"] and d4["V1_passe_positifs"])

    # --- D5a : classes maxsep re-verifiees vs §8.56 publie ---
    with open(os.path.join(BASE, "sep_maxsep_856_table.json"),
              encoding="utf-8") as fh:
        ref856 = json.load(fh)
    ref_rows = {r["paire"]: r for r in ref856["paires"]}
    ref_verdicts = ref856["verdicts"]
    classe = {}
    for scope_rows, key in ((v1, "V1_principales|maxsep_seul|0.07"),
                            (v2, "V2_rotations|maxsep_seul|0.07")):
        classe[key] = set(ref_verdicts[key]["ok"])
    d5a_changements = []
    recoupements = []
    for r in rows:
        ref = ref_rows.get(r["paire"])
        if ref is None:
            recoupements.append(f"{r['paire']}: absente de la table §8.56")
            continue
        for champ in ("maxsep_R", "maxsep_N", "d_maxsep", "sep_R", "sep_N",
                      "d_sep", "mc_old_R", "mc_old_N", "d_mc_old"):
            if abs(r[champ] - ref[champ]) > 1e-9:
                recoupements.append(
                    f"{r['paire']}: {champ} {r[champ]} vs §8.56 {ref[champ]}")
        scope_key = ("V1_principales|maxsep_seul|0.07"
                     if r["scope"] == "V1_principales"
                     else "V2_rotations|maxsep_seul|0.07"
                     if r["scope"] == "V2_rotations" else None)
        if scope_key:
            passe_avant = r["paire"] in classe[scope_key]
            passe_now = r["paire"] in (
                a2_m[4] if r["scope"] == "V1_principales" else a1_m[4])
            if passe_avant != passe_now:
                d5a_changements.append(
                    {"paire": r["paire"], "classe_856": passe_avant,
                     "classe_reverifiee": passe_now})
    # --- D5b : classes de signe d_maxsep vs d_sep ---
    d5b_changements = [
        {"paire": r["paire"], "d_maxsep": r["d_maxsep"],
         "d_sep": r["d_sep"]}
        for r in rows
        if (r["d_maxsep"] > 0) != (r["d_sep"] > 0)
        or (r["d_maxsep"] < 0) != (r["d_sep"] < 0)]
    d5 = {"D5a_changements_classe": d5a_changements,
          "D5a_passe": len(d5a_changements) == 0,
          "D5b_changements_signe": d5b_changements,
          "D5b_passe": len(d5b_changements) == 0}
    d5["passe"] = bool(d5["D5a_passe"] and d5["D5b_passe"])

    # --- Garde-fous : ancien MC relu vs publie (§8.44, phase 2) ---
    with open(os.path.join(BASE, "ssep_844_rotations.csv"),
              newline="", encoding="utf-8") as fh:
        s844 = {row["famille"] + "_" + row["controle"]: row
                for row in csv.DictReader(fh)}
    with open(os.path.join(BASE, "v62_phase2_table.csv"),
              newline="", encoding="utf-8") as fh:
        ph2 = {row["paire"]: row for row in csv.DictReader(fh)}
    for r in v2:
        ref = s844.get(r["paire"])
        if ref is not None:
            if abs(r["d_mc_old"] - float(ref["d_mc"])) > 1e-9:
                recoupements.append(f"{r['paire']}: d_mc_old vs §8.44")
            if abs(r["d_maxsep"] - float(ref["d_maxsep"])) > 1e-9:
                recoupements.append(f"{r['paire']}: d_maxsep vs §8.44")
    for r in v1:
        ref = ph2.get(r["paire"])
        if ref is not None:
            if abs(r["d_mc_old"] - float(ref["d_mc"])) > 1e-9:
                recoupements.append(f"{r['paire']}: d_mc_old vs phase2")

    # --- Sensibilites S1, S2, S4, S5, S6, S7 ---
    sens = {}
    for label, gaps in (("V1_maxsep", gaps_m_v1), ("V1_sep", gaps_s_v1),
                        ("V2_maxsep", gaps_m_v2), ("V2_sep", gaps_s_v2)):
        n_ok0, n0, n_pos0, tot0, _ = separates(gaps, 0.0)
        sens[f"S1_sans_plancher|{label}"] = {
            "n_ok_sans_plancher": n_ok0, "n": n0, "n_positifs": n_pos0}
    sens["S2_A1_a_24"] = {"maxsep_24_48": a1_m[0] >= 24,
                          "sep_24_48": a1_s[0] >= 24,
                          "maxsep_n_ok": a1_m[0], "sep_n_ok": a1_s[0]}
    sens["S4_familles"] = {}
    for fam in ("IMMROT", "V4ROT", "PARPROT", "DEPMAPROT"):
        sous_m = {r["paire"]: r["d_maxsep"] for r in v2
                  if r["paire"].startswith(fam + "_")}
        sous_s = {r["paire"]: r["d_sep"] for r in v2
                  if r["paire"].startswith(fam + "_")}
        cm = separates(sous_m, FLOOR)
        cs = separates(sous_s, FLOOR)
        sens["S4_familles"][fam] = {
            "maxsep_n_ok": cm[0], "maxsep_n": cm[1],
            "maxsep_n_positifs": cm[2], "maxsep_moyenne": cm[3] / cm[1],
            "sep_n_ok": cs[0], "sep_n": cs[1],
            "sep_n_positifs": cs[2], "sep_moyenne": cs[3] / cs[1]}
    for label, gaps in (("V1_maxsep", gaps_m_v1), ("V2_maxsep", gaps_m_v2)):
        n_ok20, n20, n_pos20, _t, _o = separates(gaps, COHEN_SMALL)
        sens[f"S5_plancher_Cohen_0.20|{label}"] = {
            "n_ok": n_ok20, "n": n20, "n_positifs": n_pos20}
    sens["S6_marges"] = [
        {"paire": r["paire"], "d_maxsep": r["d_maxsep"],
         "marge_maxsep_vs_0.07": r["d_maxsep"] - FLOOR,
         "d_sep": r["d_sep"], "marge_sep_vs_0.07": r["d_sep"] - FLOOR,
         "plancher_maxsep_equiv_sep": r["plancher_maxsep_equiv_sep"],
         "marge_maxsep_vs_equiv":
             r["d_maxsep"] - r["plancher_maxsep_equiv_sep"]}
        for r in rows
        if abs(r["d_maxsep"] - FLOOR) < 0.05 or r["paire"] in
        ("ICGC", "DEPMAPROT_MYH9", "V4ROT_MUC16")]
    # S7 : changements de classe ancien MC -> maxsep seul
    def classe_mc(gaps):
        _ok, _n, _p, _t, okset = separates(gaps, FLOOR)
        return okset
    s7 = {}
    for label, gm, go in (("V1", gaps_m_v1, gaps_o_v1),
                          ("V2", gaps_m_v2, gaps_o_v2)):
        set_m, set_o = classe_mc(gm), classe_mc(go)
        s7[label] = {
            "ancien_mc_n_ok": len(set_o), "maxsep_n_ok": len(set_m),
            "gagnent_classe": sorted(set_m - set_o),
            "perdent_classe": sorted(set_o - set_m),
            "n_changements": len(set_m ^ set_o)}
    sens["S7_ancien_mc_vers_maxsep"] = s7
    # Ancien MC : comptages de reference
    a1_o = separates(gaps_o_v2, FLOOR)
    a2_o = separates(gaps_o_v1, FLOOR)
    sens["ancien_MC_reference"] = {
        "V2_n_ok": a1_o[0], "V2_n": a1_o[1], "V2_n_positifs": a1_o[2],
        "V2_somme": a1_o[3], "V1_n_ok": a2_o[0], "V1_n": a2_o[1],
        "V1_n_positifs": a2_o[2], "V1_somme": a2_o[3]}

    portes = {"D1": d1, "D3": d3, "D4": d4, "D5": d5}
    if d1["passe"] and d3["passe"] and d4["passe"] and d5["passe"]:
        verdict = "ADOPTER"
    elif d1["passe"] and d5["passe"]:
        verdict = "ADOPTER_SOUS_CONDITION"
    else:
        verdict = "NE_PAS_ADOPTER"
    portes["verdict_propose"] = verdict
    portes["D2_recoupements"] = {
        "ecarts_vs_publie": recoupements,
        "passe_recoupements": len(recoupements) == 0,
        "note": "D2a (second calcul independant) dans "
                "maxsep_adoption_859_verify.json ; D2d (SHA) au rapport."}

    sortie = {"paires": rows, "portes": portes, "sensibilites": sens,
              "controles": {"manquants": missing,
                            "version_non_attendue": bad_versions,
                            "gigue_eff": FLOOR,
                            "formule_sep": "sep = maxsep/(1+maxsep)",
                            "formule_maxsep":
                                "maxsep = best_config.metrics.max_separation",
                            "n_paires": len(rows)}}
    with open(os.path.join(BASE, "maxsep_adoption_859_table.json"),
              "w", encoding="utf-8") as fh:
        json.dump(sortie, fh, indent=1, ensure_ascii=False)
    cols = ["scope", "paire", "n", "maxsep_R", "maxsep_N", "d_maxsep",
            "sep_R", "sep_N", "d_sep", "mc_old_R", "mc_old_N", "d_mc_old",
            "plancher_maxsep_equiv_sep", "version_R", "version_N"]
    with open(os.path.join(BASE, "maxsep_adoption_859_table.csv"),
              "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols)
        wr.writeheader()
        for r in rows:
            wr.writerow({k: r.get(k, "") for k in cols})

    print(f"paires lues: {len(rows)} (V1: {len(v1)}, V2: {len(v2)}, "
          f"descriptif: {len(rows) - len(v1) - len(v2)})")
    print(f"manquants: {missing if missing else 'AUCUN'}")
    print(f"version non attendue: {bad_versions if bad_versions else 'AUCUNE'}")
    print(f"recoupements vs publie: {recoupements if recoupements else 'AUCUN'}")
    print(f"D1 passe={d1['passe']} A1 maxsep {a1_m[0]}/48 (sep {a1_s[0]}), "
          f"A2 maxsep {a2_m[0]}/8 positifs {a2_m[2]}/8 (sep {a2_s[0]}), "
          f"HP35 maxsep {hp['d_maxsep']:+.4f}")
    print(f"D3 passe={d3['passe']} V1 pire={loo_v1_worst} "
          f"echecs={loo_v1_fails} V2 pire={loo_v2_worst} "
          f"echecs={loo_v2_fails}")
    print(f"D4 passe={d4['passe']} V1 plancher equiv: {len(d4_ok_v1)}/8 "
          f"ok={d4_ok_v1}")
    print(f"D5 passe={d5['passe']} D5a={d5a_changements} D5b={d5b_changements}")
    print(f"VERDICT PROPOSE (D2a/D2d hors script): {verdict}")
    print("ecrit: maxsep_adoption_859_table.json, maxsep_adoption_859_table.csv")


if __name__ == "__main__":
    main()
