#!/usr/bin/env python3
"""§8.38 — vérification indépendante de S_sep sur les bras existants.
Lecture seule des master_results.json v6.2 et v6.1. Ne recopie aucune table :
chaque valeur est relue dans les JSON et comparée aux tables
v62_phase2_table.json / v61_phase2_table.csv (tolérance 1e-6).
Formule gelée (PROTOCOL_v6.2.md §3) : S_sep = max_separation × stability,
lus dans run_pipeline.threshold_metadata.threshold_optimization.best_config.
Critères comparés :
  (A) gelé §3.4 : |écart| > max(gigue mesurée 0,00 ; plancher 0,07) = 0,07,
      signe = direction majoritaire (signe de la somme des écarts).
  (B) gigue 0 (commande §8.38) : |écart| > 0, signe = direction majoritaire.
  La règle (B) est rapportée à part : un changement de verdict qui viendrait
  seulement du passage 0,07 -> 0,00 n'est pas une amélioration de l'instrument.
Sorties : ssep_838_verify.json, ssep_838_verify.md.
"""
import csv
import json
import math
import os

PDAC = "/home/hatch/workspace/runs/pdac-v6"

# paire -> suffixe de dossier (results_fast_v6X_<suffixe> et _nul)
PRINCIPAL = ["hp35", "tcga_v4", "geo71729", "geo62452", "icgc",
             "immune_tcga", "parp_tcga", "depmap"]
ANNEXE = ["atr_tcga", "cptac_bcm", "cptac", "geo62452_v4b", "geo71729",
          "geo71729_parp", "geo71729_v4b", "geo71729_v4c", "immune_geo62452",
          "immune_geo71729", "immune_icgc", "immune_tcga", "luad",
          "parp_tcga", "tcga_v1", "tcga_v2", "tcga_v3", "v4r_cldn18",
          "v4r_krasdesc", "v4r_krasval", "v4r_purity", "prolif", "coad"]
# noms d'affichage de la table v62 (secondaire) pour chaque suffixe
ANNEXE_LABEL = {
    "atr_tcga": "ATR_TCGA", "cptac_bcm": "CPTAC_BCM", "cptac": "CPTAC_UMICH",
    "geo62452_v4b": "GEO62452_V4B", "geo71729": "GEO71729",
    "geo71729_parp": "GEO71729_PARP", "geo71729_v4b": "GEO71729_V4B",
    "geo71729_v4c": "GEO71729_V4C", "immune_geo62452": "IMMUNE_GEO62452",
    "immune_geo71729": "IMMUNE_GEO71729", "immune_icgc": "IMMUNE_ICGC",
    "immune_tcga": "IMMUNE_TCGA", "luad": "LUAD", "parp_tcga": "PARP_TCGA",
    "tcga_v1": "TCGA_V1", "tcga_v2": "TCGA_V2", "tcga_v3": "TCGA_V3",
    "v4r_cldn18": "V4R_CLDN18", "v4r_krasdesc": "V4R_KRASDESC",
    "v4r_krasval": "V4R_KRASVAL", "v4r_purity": "V4R_PURITY",
    "prolif": "TESTA_PROLIF", "coad": "COAD",
}
PRINCIPAL_LABEL = {
    "hp35": "HP35", "tcga_v4": "TCGA_v4", "geo71729": "GSE71729",
    "geo62452": "GSE62452", "icgc": "ICGC", "immune_tcga": "IMMUNE_TCGA",
    "parp_tcga": "PARP_TCGA", "depmap": "DEPMAP",
}
# Bras §8.38 : chaque bras = liste de paires (suffixes)
BRAS = {
    "ATR": ["atr_tcga"],
    "MTAP": ["mtap"],
    "immunitaire": ["immune_tcga", "immune_geo62452", "immune_geo71729",
                    "immune_icgc"],
    "PARP": ["parp_tcga", "geo71729_parp"],
    "principales (Phase 2)": PRINCIPAL,
}


def read_run(version, suffix):
    """Lit un master_results.json ; None si absent (avec raison)."""
    d = os.path.join(PDAC, f"results_fast_{version}_{suffix}",
                     "master_results.json")
    if not os.path.exists(d):
        return None, f"absent: {d}"
    with open(d) as f:
        j = json.load(f)
    try:
        bc = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
        m = bc["metrics"]
        l7a = j["prediction_levels"]["L7a_coherence"]
        conf = float(l7a["global_confidence"])
        direction = str(l7a["consensus_direction"]).lower()
        signed = conf if direction == "up" else (-conf if direction == "down" else 0.0)
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
            "l7a_dir": direction,
            "l7a_conf": conf,
            "l7a_signed": signed,
        }, None
    except (KeyError, TypeError) as e:
        return None, f"champ manquant dans {d}: {e}"


def classify(deltas, gigue):
    """Verdict style extract_phase2.verdict : direction = signe de la somme ;
    une paire sépare si |écart| > gigue et signe = direction."""
    s = sum(deltas.values())
    direction = 1 if s >= 0 else -1
    ok = [k for k, v in deltas.items()
          if abs(v) > gigue and (1 if v > 0 else -1) == direction]
    ko = [k for k in deltas if k not in ok]
    return direction, ok, ko


def main():
    out = {"paires": {}, "manquants": [], "comparaison_tables": {}}
    for suffix in sorted(set(PRINCIPAL + ANNEXE + ["mtap"])):
        rec = {"suffix": suffix}
        for version in ("v62", "v61"):
            for side in ("R", "N"):
                sfx = suffix if side == "R" else suffix + "_nul"
                val, err = read_run(version, sfx)
                rec[f"{version}_{side}"] = val
                if err:
                    out["manquants"].append(f"{version} {sfx}: {err}")
        for version in ("v62", "v61"):
            r, n = rec[f"{version}_R"], rec[f"{version}_N"]
            if r and n:
                rec[f"d_ssep_{version}"] = r["ssep"] - n["ssep"]
                rec[f"d_maxsep_{version}"] = r["maxsep"] - n["maxsep"]
                rec[f"d_mc_{version}"] = r["mc"] - n["mc"]
                rec[f"d_delta_{version}"] = (None if r["delta"] is None or n["delta"] is None
                                             else r["delta"] - n["delta"])
                rec[f"d_l7a_{version}"] = r["l7a_signed"] - n["l7a_signed"]
        out["paires"][suffix] = rec

    # --- Comparaison aux tables existantes (v62 json, précision 1e-6) ---
    tab62 = json.load(open(os.path.join(PDAC, "v62_phase2_table.json")))
    tab62_by_label = {}
    for row in tab62["principal"] + tab62["secondaire"]:
        tab62_by_label[row["paire"]] = row
    label_of = {}
    for s in PRINCIPAL:
        label_of[s] = PRINCIPAL_LABEL[s]
    for s in ANNEXE:
        label_of[s] = ANNEXE_LABEL[s]
    diffs = []
    for suffix, rec in out["paires"].items():
        lab = label_of.get(suffix)
        if lab is None or lab not in tab62_by_label:
            continue
        row = tab62_by_label[lab]
        r62, n62 = rec.get("v62_R"), rec.get("v62_N")
        if not (r62 and n62):
            diffs.append(f"{lab}: v62 manquant, table non vérifiable")
            continue
        for key_json, key_tab in [
                ("maxsep", "maxsep_R"), ("stab", "stab_R"),
                ("ssep", "ssep_R"), ("mc", "mc_R")]:
            if abs(r62[key_json] - row[key_tab]) > 1e-6:
                diffs.append(f"{lab} R {key_json}: relu {r62[key_json]} vs table {row[key_tab]}")
        for key_json, key_tab in [
                ("maxsep", "maxsep_N"), ("stab", "stab_N"),
                ("ssep", "ssep_N"), ("mc", "mc_N")]:
            if abs(n62[key_json] - row[key_tab]) > 1e-6:
                diffs.append(f"{lab} N {key_json}: relu {n62[key_json]} vs table {row[key_tab]}")
        if abs(rec["d_ssep_v62"] - row["d_ssep"]) > 1e-6:
            diffs.append(f"{lab} d_ssep: relu {rec['d_ssep_v62']} vs table {row['d_ssep']}")
        if abs(rec["d_maxsep_v62"] - row["d_maxsep"]) > 1e-6:
            diffs.append(f"{lab} d_maxsep: relu {rec['d_maxsep_v62']} vs table {row['d_maxsep']}")
    out["comparaison_tables"]["v62_json_ecarts"] = diffs

    # --- Comparaison v61 : table CSV (arrondie à 4 décimales, tolérance 5e-5) ---
    diffs61 = []
    with open(os.path.join(PDAC, "v61_phase2_table.csv")) as f:
        rows61 = {r["paire"]: r for r in csv.DictReader(f)}
    # noms CSV : vérifier les clés présentes
    out["comparaison_tables"]["v61_csv_colonnes"] = list(next(iter(rows61.values())).keys())
    for suffix in PRINCIPAL + ANNEXE:
        lab = label_of.get(suffix)
        rec = out["paires"][suffix]
        r61, n61 = rec.get("v61_R"), rec.get("v61_N")
        if not (r61 and n61):
            continue
        # retrouver la ligne CSV : le CSV utilise quels noms ? on essaie lab et variantes
        row = None
        for cand in (lab, lab.replace("GSE", "GEO") if lab else None,
                     lab.upper() if lab else None):
            if cand in rows61:
                row = rows61[cand]
                break
        if row is None:
            diffs61.append(f"{lab}: pas de ligne CSV v61 trouvée (clés: {sorted(rows61)[:8]}...)")
            continue
        # colonnes attendues : maxsep_R etc. — on teste celles qui existent
        for key_json, key_tab in [("maxsep", "maxsep_R"), ("ssep", "ssep_R"),
                                  ("mc", "mc_R")]:
            if key_tab in row and row[key_tab] not in ("", None):
                try:
                    if abs(r61[key_json] - float(row[key_tab])) > 5e-5:
                        diffs61.append(f"{lab} v61 R {key_json}: relu {r61[key_json]} vs csv {row[key_tab]}")
                except ValueError:
                    pass
    out["comparaison_tables"]["v61_csv_ecarts"] = diffs61

    # --- Verdicts S_sep / max_sep sur les 8 principales, règles (A) et (B) ---
    verdicts = {}
    for name, key, gigue in [
            ("S_sep v62, gigue gelee 0,07 (A)", "d_ssep_v62", 0.07),
            ("S_sep v62, gigue 0 (B)", "d_ssep_v62", 0.0),
            ("max_sep v62, gigue 0", "d_maxsep_v62", 0.0),
            ("max_sep v61, gigue 0,07", "d_maxsep_v61", 0.07),
            ("S_sep v61 (retrospectif), gigue 0,07", "d_ssep_v61", 0.07),
            ("MC v62, gigue 0", "d_mc_v62", 0.0),
            ("MC v61, gigue 0,07", "d_mc_v61", 0.07)]:
        deltas = {PRINCIPAL_LABEL[s]: out["paires"][s][key]
                  for s in PRINCIPAL if key in out["paires"][s]}
        direction, ok, ko = classify(deltas, gigue)
        verdicts[name] = {"direction": direction, "ok": ok, "ko": ko,
                          "n_ok": len(ok), "deltas": deltas}
    out["verdicts_principales"] = verdicts
    # --- Annexe 23 : mêmes règles (direction propre aux 23) ---
    verdicts_anx = {}
    for name, key, gigue in [
            ("S_sep v62, gigue gelee 0,07 (A)", "d_ssep_v62", 0.07),
            ("S_sep v62, gigue 0 (B)", "d_ssep_v62", 0.0),
            ("max_sep v62, gigue 0", "d_maxsep_v62", 0.0),
            ("max_sep v61, gigue 0,07", "d_maxsep_v61", 0.07),
            ("S_sep v61 (retrospectif), gigue 0,07", "d_ssep_v61", 0.07)]:
        deltas = {}
        for s in ANNEXE:
            lab = ANNEXE_LABEL[s]
            if key in out["paires"][s] and lab not in deltas:
                deltas[lab] = out["paires"][s][key]
        direction, ok, ko = classify(deltas, gigue)
        verdicts_anx[name] = {"direction": direction, "ok": ok, "ko": ko,
                              "n_ok": len(ok), "deltas": deltas}
    out["verdicts_annexe23"] = verdicts_anx

    # --- Par bras : écart S_sep v62 + v61, classification sous (A) et (B) ---
    bras = {}
    for bras_nom, suffixes in BRAS.items():
        lignes = []
        for s in suffixes:
            rec = out["paires"][s]
            lignes.append({
                "paire": label_of.get(s, s.upper()),
                "n_v62": rec["v62_R"]["n"] if rec.get("v62_R") else None,
                "controle_v62": rec["v62_R"]["control"] if rec.get("v62_R") else None,
                "ssep_R_v62": rec["v62_R"]["ssep"] if rec.get("v62_R") else None,
                "ssep_N_v62": rec["v62_N"]["ssep"] if rec.get("v62_N") else None,
                "d_ssep_v62": rec.get("d_ssep_v62"),
                "ssep_R_v61": rec["v61_R"]["ssep"] if rec.get("v61_R") else None,
                "ssep_N_v61": rec["v61_N"]["ssep"] if rec.get("v61_N") else None,
                "d_ssep_v61": rec.get("d_ssep_v61"),
                "d_maxsep_v61": rec.get("d_maxsep_v61"),
                "d_maxsep_v62": rec.get("d_maxsep_v62"),
                "d_mc_v62": rec.get("d_mc_v62"),
                "d_delta_v62": rec.get("d_delta_v62"),
                "d_l7a_v62": rec.get("d_l7a_v62"),
            })
        bras[bras_nom] = lignes
    out["bras"] = bras

    with open(os.path.join(PDAC, "ssep_838_verify.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("paires lues:", len(out["paires"]))
    print("manquants:", out["manquants"])
    print("écarts vs table v62:", diffs if diffs else "AUCUN")
    print("écarts vs csv v61:", diffs61 if diffs61 else "AUCUN (sur champs comparables)")
    for name, v in verdicts.items():
        print(f"{name}: {v['n_ok']}/8 ok={v['ok']} ko={v['ko']}")
    for name, v in verdicts_anx.items():
        print(f"ANNEXE {name}: {v['n_ok']}/23 ok={v['ok']}")
    print("écrit: ssep_838_verify.json")


if __name__ == "__main__":
    main()
