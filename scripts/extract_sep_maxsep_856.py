#!/usr/bin/env python3
"""Chantier §8.56 — sep seul / maxsep seul comme score MC
(PROTOCOL_sep_maxsep_856.md). Lecture SEULE des master_results.json
v6.2/v6.1 deja sur disque. AUCUN run du pipeline, AUCUN code modifie.
Candidats (relectures du best_config ANCIEN, selection inchangee) :
  maxsep = best_config.metrics.max_separation  (|d de Cohen|, [0, inf[)
  sep    = maxsep / (1 + maxsep)               ([0, 1[)
Sorties : sep_maxsep_856_table.csv / sep_maxsep_856_table.json
Garde-fous : ancien MC relu vs ssep_844_rotations.csv (V2) et
v62_phase2_table.csv (V1), tol. 1e-9 ; sep/maxsep vs v64_mc_table.json,
tol. 1e-9 ; versions JSON consignees.
"""
import csv
import json
import math
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLANCHER = 0.07


def load_master(outdir):
    """Lit un master_results.json et renvoie (maxsep, sep, mc_old, version, n)."""
    p = HERE / outdir / "master_results.json"
    if not p.is_file():
        return None, f"absent: {p}"
    data = json.loads(p.read_text())
    try:
        bc = data["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]
        met = bc["metrics"]
        m = float(met["max_separation"])
        if not math.isfinite(m) or m < 0:
            return None, f"maxsep non valide ({m}) dans {p}"
        sep = 0.0 if m == 0 else m / (1.0 + m)
        return {
            "maxsep": m,
            "sep": sep,
            "mc_old": float(bc["score"]),
            "version": data.get("version"),
            "n": data["reading_synthesis"]["n_samples"],
        }, None
    except (KeyError, TypeError, ValueError) as exc:
        return None, f"champ manquant dans {p}: {exc}"


PRINCIPALES = [
    ("HP35", "results_fast_v62_hp35", "results_fast_v62_hp35_nul"),
    ("TCGA_v4", "results_fast_v62_tcga_v4", "results_fast_v62_tcga_v4_nul"),
    ("GSE71729", "results_fast_v62_geo71729", "results_fast_v62_geo71729_nul"),
    ("GSE62452", "results_fast_v62_geo62452", "results_fast_v62_geo62452_nul"),
    ("ICGC", "results_fast_v62_icgc", "results_fast_v62_icgc_nul"),
    ("IMMUNE_TCGA", "results_fast_v62_immune_tcga", "results_fast_v62_immune_tcga_nul"),
    ("PARP_TCGA", "results_fast_v62_parp_tcga", "results_fast_v62_parp_tcga_nul"),
    ("DEPMAP", "results_fast_v62_depmap", "results_fast_v62_depmap_nul"),
]
DESCRIPTIFS = [
    ("TESTA_PROLIF", "results_fast_v62_prolif", "results_fast_v62_prolif_nul"),
    ("MTAP_PRMT5FLUX", "results_fast_v62_prmt5flux", "results_fast_v62_prmt5flux_nul"),
    ("MTAP_SERIES", "results_fast_v62_mtap", "results_fast_v62_mtap_nul"),
    ("V4R_PURITY", "results_fast_v62_v4r_purity", "results_fast_v62_v4r_purity_nul"),
]
ROTATIONS_EXISTANTES = {
    ("V4ROT", "CLDN18"): ("results_fast_v61_v4r_cldn18_dedup",
                          "results_fast_v61_v4r_cldn18_dedup_nul"),
    ("IMMROT", "CTLA4"): ("results_fast_v62_immrot_ctla4_dedup",
                          "results_fast_v62_immrot_ctla4_dedup_nul"),
    ("DEPMAPROT", "ACO2"): ("results_fast_v62_depmaprot_aco2_dedup",
                            "results_fast_v62_depmaprot_aco2_dedup_nul_sp"),
    ("PARPROT", "PARP1"): ("results_fast_v62_parprot_parp1_dedup",
                           "results_fast_v62_parprot_parp1_dedup_nul_sp"),
}


def dossiers_rotations():
    """Reconstruit les 48 paires rotations depuis manifest_v62_dedup_844.txt."""
    table = {}
    for ligne in (HERE / "manifest_v62_dedup_844.txt").read_text().splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#"):
            continue
        nom, _entree, sortie = ligne.split("|")
        base = nom[len("DEDUP844_"):]
        est_nul = base.endswith("_NUL")
        base = base[:-4] if est_nul else base
        famille, controle = base.rsplit("_", 1)
        table.setdefault((famille, controle), {})["NUL" if est_nul else "REEL"] = sortie
    for cle, (r, n) in ROTATIONS_EXISTANTES.items():
        table[cle] = {"REEL": r, "NUL": n}
    return table


def compter(ecarts, plancher):
    """Regle de comptage du protocole §3 : direction = signe de la somme ;
    une paire separe si |ecart| > plancher et signe = direction."""
    total = sum(ecarts.values())
    direction = 1 if total > 0 else (-1 if total < 0 else 0)
    ok, ko = [], []
    for nom, val in ecarts.items():
        if direction != 0 and abs(val) > plancher and (1 if val > 0 else -1) == direction:
            ok.append(nom)
        else:
            ko.append(nom)
    positifs = [nom for nom, val in ecarts.items() if val > 0]
    return {"direction": direction, "n_ok": len(ok), "n": len(ecarts),
            "ok": ok, "ko": ko, "n_positifs": len(positifs),
            "positifs": positifs, "somme": total,
            "moyenne": total / len(ecarts) if ecarts else 0.0}


def main():
    manquants, versions_bad, ecarts_pub = [], [], []
    lignes = []

    def ajouter(portee, nom, rep_r, rep_n):
        r, e1 = load_master(rep_r)
        n, e2 = load_master(rep_n)
        if e1:
            manquants.append(f"{nom} REEL: {e1}")
            return
        if e2:
            manquants.append(f"{nom} NUL: {e2}")
            return
        for cote, v in (("REEL", r), ("NUL", n)):
            if v["version"] not in ("v6.2.0-L7aL7b-CohenD-short",
                                    "v6.1.0-L7aL7b-CohenD-short"):
                versions_bad.append(f"{nom} {cote}: {v['version']}")
        lignes.append({
            "scope": portee, "paire": nom, "n": r["n"],
            "maxsep_R": r["maxsep"], "maxsep_N": n["maxsep"],
            "d_maxsep": r["maxsep"] - n["maxsep"],
            "sep_R": r["sep"], "sep_N": n["sep"],
            "d_sep": r["sep"] - n["sep"],
            "mc_old_R": r["mc_old"], "mc_old_N": n["mc_old"],
            "d_mc_old": r["mc_old"] - n["mc_old"],
            # Plancher maxsep equivalent au plancher sep (§7 S3) :
            # d_sep > 0.07  <=>  d_maxsep > 0.07*(1+mR)*(1+mN)
            "plancher_maxsep_equiv_sep": PLANCHER * (1.0 + r["maxsep"]) * (1.0 + n["maxsep"]),
            "version_R": r["version"], "version_N": n["version"],
        })

    for nom, rr, nn in PRINCIPALES:
        ajouter("V1_principales", nom, rr, nn)
    for (fam, ctrl), cotes in sorted(dossiers_rotations().items()):
        ajouter("V2_rotations", f"{fam}_{ctrl}", cotes["REEL"], cotes["NUL"])
    for nom, rr, nn in DESCRIPTIFS:
        ajouter("V3_V4_V5_descriptif", nom, rr, nn)

    # --- Garde-fous : ancien MC relu vs publie ---
    s844 = {}
    with open(HERE / "ssep_844_rotations.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            s844[f"{row['famille']}_{row['controle']}"] = row
    for lig in lignes:
        if lig["scope"] == "V2_rotations" and lig["paire"] in s844:
            if abs(lig["d_mc_old"] - float(s844[lig["paire"]]["d_mc"])) > 1e-9:
                ecarts_pub.append(f"{lig['paire']}: d_mc_old relu vs §8.44")
            if abs(lig["d_maxsep"] - float(s844[lig["paire"]]["d_maxsep"])) > 1e-9:
                ecarts_pub.append(f"{lig['paire']}: d_maxsep relu vs §8.44")
    ph2 = {}
    with open(HERE / "v62_phase2_table.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            ph2[row["paire"]] = row
    for lig in lignes:
        if lig["scope"] == "V1_principales" and lig["paire"] in ph2:
            if abs(lig["d_mc_old"] - float(ph2[lig["paire"]]["d_mc"])) > 1e-9:
                ecarts_pub.append(f"{lig['paire']}: d_mc_old relu vs phase2")
    # --- Recoupement sep/maxsep vs table v6.4 (tol. 1e-9) ---
    v64 = {r["paire"]: r
           for r in json.loads((HERE / "v64_mc_table.json").read_text())["paires"]}
    for lig in lignes:
        if lig["paire"] in v64:
            ref = v64[lig["paire"]]
            for cle, cle_ref in (("maxsep_R", "maxsep_R"), ("maxsep_N", "maxsep_N"),
                                 ("sep_R", "sep_R"), ("sep_N", "sep_N"),
                                 ("d_maxsep", "d_maxsep"), ("d_sep", "d_sep")):
                if abs(lig[cle] - ref[cle_ref]) > 1e-9:
                    ecarts_pub.append(f"{lig['paire']}: {cle} relu vs v64")

    # --- Verdicts geles §4 (plancher 0.07) ---
    verdicts = {}
    for portee in ("V1_principales", "V2_rotations"):
        sous = [l for l in lignes if l["scope"] == portee]
        for cle, label in (("d_sep", "sep_seul"), ("d_maxsep", "maxsep_seul")):
            verdicts[f"{portee}|{label}|0.07"] = compter(
                {l["paire"]: l[cle] for l in sous}, PLANCHER)
    hp = [l for l in lignes if l["paire"] == "HP35"][0]
    verdicts["HP35"] = {"d_sep": hp["d_sep"], "d_maxsep": hp["d_maxsep"],
                        "d_mc_old": hp["d_mc_old"],
                        "sep_R": hp["sep_R"], "sep_N": hp["sep_N"],
                        "maxsep_R": hp["maxsep_R"], "maxsep_N": hp["maxsep_N"]}
    # --- Sensibilites S1-S4 (descriptives) ---
    sens = {}
    for portee in ("V1_principales", "V2_rotations"):
        sous = [l for l in lignes if l["scope"] == portee]
        for cle, label in (("d_sep", "sep_seul"), ("d_maxsep", "maxsep_seul")):
            sens[f"{portee}|{label}|sans_plancher"] = compter(
                {l["paire"]: l[cle] for l in sous}, 0.0)
    # S2 : A1 a 24/48 (ancienne barre) — rapporte, non decisif
    # S3 : paires M passant le plancher litteral mais pas le plancher equivalent-sep
    rot = [l for l in lignes if l["scope"] == "V2_rotations"]
    princ = [l for l in lignes if l["scope"] == "V1_principales"]
    sens["S3_echelle"] = {
        "V2_passent_litteral_pas_equiv": [
            l["paire"] for l in rot
            if l["d_maxsep"] > PLANCHER and l["d_maxsep"] <= l["plancher_maxsep_equiv_sep"]],
        "V1_passent_litteral_pas_equiv": [
            l["paire"] for l in princ
            if l["d_maxsep"] > PLANCHER and l["d_maxsep"] <= l["plancher_maxsep_equiv_sep"]],
    }
    # S4 : ventilation par famille (V2)
    sens["S4_familles"] = {}
    for fam in ("IMMROT", "V4ROT", "PARPROT", "DEPMAPROT"):
        sous = [l for l in rot if l["paire"].startswith(fam + "_")]
        sens["S4_familles"][fam] = {
            "sep": compter({l["paire"]: l["d_sep"] for l in sous}, PLANCHER),
            "maxsep": compter({l["paire"]: l["d_maxsep"] for l in sous}, PLANCHER),
        }

    sortie = {"paires": lignes, "verdicts": verdicts, "sensibilites": sens,
              "controles": {"manquants": manquants,
                            "version_non_attendue": versions_bad,
                            "ecarts_vs_publie": ecarts_pub,
                            "gigue_eff": PLANCHER,
                            "formule_sep": "sep = maxsep/(1+maxsep)",
                            "formule_maxsep": "maxsep = best_config.metrics.max_separation"}}
    (HERE / "sep_maxsep_856_table.json").write_text(
        json.dumps(sortie, indent=1, ensure_ascii=False))
    colonnes = ["scope", "paire", "n", "maxsep_R", "maxsep_N", "d_maxsep",
                "sep_R", "sep_N", "d_sep", "mc_old_R", "mc_old_N", "d_mc_old",
                "plancher_maxsep_equiv_sep", "version_R", "version_N"]
    with open(HERE / "sep_maxsep_856_table.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=colonnes)
        w.writeheader()
        for l in lignes:
            w.writerow({k: l.get(k, "") for k in colonnes})

    print(f"paires lues: {len(lignes)} (V1: 8, V2: 48, descriptif: 4 attendus)")
    print(f"manquants: {manquants if manquants else 'AUCUN'}")
    print(f"version non attendue: {versions_bad if versions_bad else 'AUCUNE'}")
    print(f"ecarts vs publie: {ecarts_pub if ecarts_pub else 'AUCUN'}")
    for k, v in verdicts.items():
        if k == "HP35":
            print(f"HP35 d_sep={v['d_sep']:.4f} d_maxsep={v['d_maxsep']:.4f} "
                  f"d_mc_old={v['d_mc_old']:.4f}")
        else:
            print(f"{k}: {v['n_ok']}/{v['n']} dir={v['direction']:+d} "
                  f"positifs={v['n_positifs']}/{v['n']} "
                  f"somme={v['somme']:+.4f} moyenne={v['moyenne']:+.4f}")
    print("ecrit: sep_maxsep_856_table.json, sep_maxsep_856_table.csv")


if __name__ == "__main__":
    main()
