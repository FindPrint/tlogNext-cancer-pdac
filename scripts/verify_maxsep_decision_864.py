#!/usr/bin/env python3
"""Chantier §8.64 — dossier de décision d'adoption maxsep
(PROTOCOL_maxsep_decision_864.md). Second calcul indépendant : troisième
lecture des 120 master_results.json déjà sur disque (après l'extracteur
§8.59 et son vérifieur). AUCUN run du pipeline, AUCUN code modifié.

Chemin de code distinct des deux scripts §8.59 : ne réutilise AUCUNE de
leurs fonctions. Descente récursive générique à la recherche de
"best_config" (re-écrite), listes de dossiers reconstruites depuis le
manifest §8.44 et les listes figées du protocole §8.59, comptages
re-écrits. Recoupements à 1e-9 contre maxsep_adoption_859_table.json et
sep_maxsep_856_table.json, ancien MC vs §8.44 et phase 2 v6.2.
Portes D1-D5 recalculées de zéro. Sortie : maxsep_decision_864_verify.json
"""
import csv
import json
import math
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SEUIL = 0.07
PETIT_COHEN = 0.20
VERSIONS_ATTENDUES = {"v6.2.0-L7aL7b-CohenD-short",
                      "v6.1.0-L7aL7b-CohenD-short"}

PRINCIPALES = [
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
DESCRIPTIFS = [
    ("TESTA_PROLIF", "results_fast_v62_prolif", "results_fast_v62_prolif_nul"),
    ("MTAP_PRMT5FLUX", "results_fast_v62_prmt5flux",
     "results_fast_v62_prmt5flux_nul"),
    ("MTAP_SERIES", "results_fast_v62_mtap", "results_fast_v62_mtap_nul"),
    ("V4R_PURITY", "results_fast_v62_v4r_purity",
     "results_fast_v62_v4r_purity_nul"),
]
ROTATIONS_HORS_MANIFEST = {
    "V4ROT_CLDN18": ("results_fast_v61_v4r_cldn18_dedup",
                     "results_fast_v61_v4r_cldn18_dedup_nul"),
    "IMMROT_CTLA4": ("results_fast_v62_immrot_ctla4_dedup",
                     "results_fast_v62_immrot_ctla4_dedup_nul"),
    "DEPMAPROT_ACO2": ("results_fast_v62_depmaprot_aco2_dedup",
                       "results_fast_v62_depmaprot_aco2_dedup_nul_sp"),
    "PARPROT_PARP1": ("results_fast_v62_parprot_parp1_dedup",
                      "results_fast_v62_parprot_parp1_dedup_nul_sp"),
}


def chercher_best_config(noeud):
    """Descente récursive générique : premier dict 'best_config' rencontré."""
    if isinstance(noeud, dict):
        if "best_config" in noeud and isinstance(noeud["best_config"], dict):
            return noeud["best_config"]
        for val in noeud.values():
            trouve = chercher_best_config(val)
            if trouve is not None:
                return trouve
    elif isinstance(noeud, list):
        for element in noeud:
            trouve = chercher_best_config(element)
            if trouve is not None:
                return trouve
    return None


def lire_run(dossier):
    chemin = os.path.join(BASE, dossier, "master_results.json")
    with open(chemin, encoding="utf-8") as fh:
        brut = json.load(fh)
    meilleur = chercher_best_config(brut)
    if meilleur is None:
        raise ValueError("best_config introuvable")
    msep = float(meilleur["metrics"]["max_separation"])
    if not math.isfinite(msep) or msep < 0:
        raise ValueError(f"maxsep invalide {msep!r}")
    return {"maxsep": msep,
            "sep": msep / (1.0 + msep) if msep else 0.0,
            "mc_old": float(meilleur["score"]),
            "version": brut.get("version"),
            "n": brut["reading_synthesis"]["n_samples"]}


def dossiers_rotations():
    """Reconstruit les 48 paires rotations depuis le manifest §8.44."""
    trouves = {}
    with open(os.path.join(BASE, "manifest_v62_dedup_844.txt"),
              encoding="utf-8") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if not ligne or ligne.startswith("#"):
                continue
            identifiant, _source, sortie = ligne.split("|")
            tige = identifiant[len("DEDUP844_"):]
            est_nul = tige.endswith("_NUL")
            if est_nul:
                tige = tige[:-4]
            famille, controle = tige.rsplit("_", 1)
            case = trouves.setdefault(f"{famille}_{controle}", {})
            case["NUL" if est_nul else "REEL"] = sortie
    for nom, (d_reel, d_nul) in ROTATIONS_HORS_MANIFEST.items():
        trouves[nom] = {"REEL": d_reel, "NUL": d_nul}
    return trouves


def compter(ecarts, plancher):
    """Comptage protocole §3 : direction = signe de la somme ; une paire
    sépare si |écart| > plancher et signe = direction."""
    somme = sum(ecarts.values())
    direction = 1 if somme > 0 else (-1 if somme < 0 else 0)
    ok = set()
    n_pos = 0
    for nom, ecart in ecarts.items():
        if ecart > 0:
            n_pos += 1
        if direction != 0 and abs(ecart) > plancher and (
                (ecart > 0) == (direction > 0)):
            ok.add(nom)
    return {"n_ok": len(ok), "n": len(ecarts), "n_positifs": n_pos,
            "somme": somme, "moyenne": somme / len(ecarts) if ecarts else 0.0,
            "ok": sorted(ok)}


def loo(ecarts, plancher, barre):
    """Leave-one-out exhaustif : pire cas et suppressions échouant la barre."""
    echecs = []
    pire = None
    for retiree in sorted(ecarts):
        reste = {k: v for k, v in ecarts.items() if k != retiree}
        resultat = compter(reste, plancher)
        if pire is None or resultat["n_ok"] < pire[1]:
            pire = (retiree, resultat["n_ok"])
        if resultat["n_ok"] < barre:
            echecs.append({"retiree": retiree,
                           "n_ok_restant": resultat["n_ok"],
                           "n_restant": len(reste)})
    return {"passe": len(echecs) == 0, "pire_cas": list(pire),
            "suppressions_echouant": echecs}


def main():
    manquants = []
    versions_inattendues = []
    lignes = []

    def ajouter_paire(portee, nom, dir_reel, dir_nul):
        try:
            reel = lire_run(dir_reel)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            manquants.append(f"{nom} REEL: {exc}")
            return
        try:
            nul = lire_run(dir_nul)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            manquants.append(f"{nom} NUL: {exc}")
            return
        for cote, run in (("REEL", reel), ("NUL", nul)):
            if run["version"] not in VERSIONS_ATTENDUES:
                versions_inattendues.append(f"{nom} {cote}: {run['version']}")
        lignes.append({
            "scope": portee, "paire": nom, "n": reel["n"],
            "maxsep_R": reel["maxsep"], "maxsep_N": nul["maxsep"],
            "d_maxsep": reel["maxsep"] - nul["maxsep"],
            "sep_R": reel["sep"], "sep_N": nul["sep"],
            "d_sep": reel["sep"] - nul["sep"],
            "mc_old_R": reel["mc_old"], "mc_old_N": nul["mc_old"],
            "d_mc_old": reel["mc_old"] - nul["mc_old"],
            "plancher_maxsep_equiv_sep":
                SEUIL * (1.0 + reel["maxsep"]) * (1.0 + nul["maxsep"]),
            "version_R": reel["version"], "version_N": nul["version"],
        })

    for nom, dr, dn in PRINCIPALES:
        ajouter_paire("V1_principales", nom, dr, dn)
    for nom, cotes in sorted(dossiers_rotations().items()):
        ajouter_paire("V2_rotations", nom, cotes["REEL"], cotes["NUL"])
    for nom, dr, dn in DESCRIPTIFS:
        ajouter_paire("V3_V4_V5_descriptif", nom, dr, dn)

    v1 = [r for r in lignes if r["scope"] == "V1_principales"]
    v2 = [r for r in lignes if r["scope"] == "V2_rotations"]
    e_m_v1 = {r["paire"]: r["d_maxsep"] for r in v1}
    e_s_v1 = {r["paire"]: r["d_sep"] for r in v1}
    e_m_v2 = {r["paire"]: r["d_maxsep"] for r in v2}
    e_s_v2 = {r["paire"]: r["d_sep"] for r in v2}
    e_o_v1 = {r["paire"]: r["d_mc_old"] for r in v1}
    e_o_v2 = {r["paire"]: r["d_mc_old"] for r in v2}

    # --- Recoupements exacts contre les tables publiées ---
    ecarts_recoup = []
    with open(os.path.join(BASE, "maxsep_adoption_859_table.json"),
              encoding="utf-8") as fh:
        table859 = json.load(fh)
    ref859 = {r["paire"]: r for r in table859["paires"]}
    with open(os.path.join(BASE, "sep_maxsep_856_table.json"),
              encoding="utf-8") as fh:
        table856 = json.load(fh)
    ref856 = {r["paire"]: r for r in table856["paires"]}
    champs = ("maxsep_R", "maxsep_N", "d_maxsep", "sep_R", "sep_N",
              "d_sep", "mc_old_R", "mc_old_N", "d_mc_old")
    for r in lignes:
        for etiquette, ref in (("859", ref859), ("856", ref856)):
            reference = ref.get(r["paire"])
            if reference is None:
                ecarts_recoup.append(f"{r['paire']}: absente table §8.{etiquette}")
                continue
            for champ in champs:
                if abs(r[champ] - reference[champ]) > 1e-9:
                    ecarts_recoup.append(
                        f"{r['paire']}: {champ} {r[champ]} vs §8.{etiquette} "
                        f"{reference[champ]}")
    # Ancien MC relu vs §8.44 (rotations) et phase 2 v6.2 (principales)
    with open(os.path.join(BASE, "ssep_844_rotations.csv"),
              newline="", encoding="utf-8") as fh:
        s844 = {row["famille"] + "_" + row["controle"]: row
                for row in csv.DictReader(fh)}
    with open(os.path.join(BASE, "v62_phase2_table.csv"),
              newline="", encoding="utf-8") as fh:
        phase2 = {row["paire"]: row for row in csv.DictReader(fh)}
    for r in v2:
        ref = s844.get(r["paire"])
        if ref is not None:
            if abs(r["d_mc_old"] - float(ref["d_mc"])) > 1e-9:
                ecarts_recoup.append(f"{r['paire']}: d_mc_old vs §8.44")
            if abs(r["d_maxsep"] - float(ref["d_maxsep"])) > 1e-9:
                ecarts_recoup.append(f"{r['paire']}: d_maxsep vs §8.44")
    for r in v1:
        ref = phase2.get(r["paire"])
        if ref is not None and abs(r["d_mc_old"] - float(ref["d_mc"])) > 1e-9:
            ecarts_recoup.append(f"{r['paire']}: d_mc_old vs phase2")

    # --- D1 ---
    a1_m = compter(e_m_v2, SEUIL)
    a1_s = compter(e_s_v2, SEUIL)
    a2_m = compter(e_m_v1, SEUIL)
    a2_s = compter(e_s_v1, SEUIL)
    hp35 = next(r for r in v1 if r["paire"] == "HP35")
    d1 = {
        "A1_rotations_maxsep": {"n_ok": a1_m["n_ok"], "n": a1_m["n"],
                                "barre": 30, "passe": a1_m["n_ok"] >= 30,
                                "n_positifs": a1_m["n_positifs"],
                                "somme": a1_m["somme"],
                                "moyenne": a1_m["moyenne"],
                                "ok": a1_m["ok"]},
        "A1_rotations_sep": {"n_ok": a1_s["n_ok"], "n": a1_s["n"],
                             "n_positifs": a1_s["n_positifs"],
                             "somme": a1_s["somme"],
                             "moyenne": a1_s["moyenne"]},
        "A2_principales_maxsep": {"n_ok": a2_m["n_ok"], "n": a2_m["n"],
                                  "barre": 6, "passe": a2_m["n_ok"] >= 6,
                                  "n_positifs": a2_m["n_positifs"],
                                  "barre_positifs": 7,
                                  "passe_positifs": a2_m["n_positifs"] >= 7,
                                  "somme": a2_m["somme"],
                                  "moyenne": a2_m["moyenne"],
                                  "ok": a2_m["ok"]},
        "A2_principales_sep": {"n_ok": a2_s["n_ok"], "n": a2_s["n"],
                               "n_positifs": a2_s["n_positifs"],
                               "somme": a2_s["somme"],
                               "moyenne": a2_s["moyenne"]},
        "A3_HP35_maxsep": {"d_maxsep": hp35["d_maxsep"], "barre": 0.30,
                           "passe": hp35["d_maxsep"] >= 0.30},
        "A3_HP35_sep": {"d_sep": hp35["d_sep"]},
        "A3_HP35_mc_old": {"d_mc_old": hp35["d_mc_old"]},
    }
    d1["passe"] = bool(d1["A1_rotations_maxsep"]["passe"]
                       and d1["A2_principales_maxsep"]["passe"]
                       and d1["A2_principales_maxsep"]["passe_positifs"]
                       and d1["A3_HP35_maxsep"]["passe"])

    # --- D3 ---
    loo_v1 = loo(e_m_v1, SEUIL, 6)
    loo_v2 = loo(e_m_v2, SEUIL, 30)
    d3 = {"V1": loo_v1, "V2": loo_v2,
          "passe": bool(loo_v1["passe"] and loo_v2["passe"])}

    # --- D4 ---
    d4_ok = [r["paire"] for r in v1
             if r["d_maxsep"] > r["plancher_maxsep_equiv_sep"]]
    d4_ko = [r["paire"] for r in v1
             if r["d_maxsep"] <= r["plancher_maxsep_equiv_sep"]]
    n_pos_v1 = sum(1 for r in v1 if r["d_maxsep"] > 0)
    d4 = {
        "V1_n_ok_plancher_equiv": len(d4_ok), "V1_n": len(v1),
        "V1_barre": 6, "V1_passe": len(d4_ok) >= 6,
        "V1_n_positifs": n_pos_v1, "V1_passe_positifs": n_pos_v1 >= 7,
        "V1_ok": d4_ok, "V1_ko": d4_ko,
        "V1_passent_litteral_pas_equiv": [
            r["paire"] for r in v1
            if r["d_maxsep"] > SEUIL
            and r["d_maxsep"] <= r["plancher_maxsep_equiv_sep"]],
        "V2_passent_litteral_pas_equiv": [
            r["paire"] for r in v2
            if r["d_maxsep"] > SEUIL
            and r["d_maxsep"] <= r["plancher_maxsep_equiv_sep"]],
    }
    d4["passe"] = bool(d4["V1_passe"] and d4["V1_passe_positifs"])

    # --- D5 ---
    ref_verdicts = table856["verdicts"]
    classes856 = {}
    for cle in ("V1_principales|maxsep_seul|0.07",
                "V2_rotations|maxsep_seul|0.07"):
        classes856[cle] = set(ref_verdicts[cle]["ok"])
    changements_d5a = []
    for r in lignes:
        if r["scope"] == "V1_principales":
            cle = "V1_principales|maxsep_seul|0.07"
            passe_now = r["paire"] in a2_m["ok"]
        elif r["scope"] == "V2_rotations":
            cle = "V2_rotations|maxsep_seul|0.07"
            passe_now = r["paire"] in a1_m["ok"]
        else:
            continue
        passe_avant = r["paire"] in classes856[cle]
        if passe_avant != passe_now:
            changements_d5a.append({"paire": r["paire"],
                                    "classe_856": passe_avant,
                                    "classe_reverifiee": passe_now})
    changements_d5b = [
        {"paire": r["paire"], "d_maxsep": r["d_maxsep"],
         "d_sep": r["d_sep"]}
        for r in lignes
        if (r["d_maxsep"] > 0) != (r["d_sep"] > 0)
        or (r["d_maxsep"] < 0) != (r["d_sep"] < 0)]
    d5 = {"D5a_changements_classe": changements_d5a,
          "D5a_passe": len(changements_d5a) == 0,
          "D5b_changements_signe": changements_d5b,
          "D5b_passe": len(changements_d5b) == 0}
    d5["passe"] = bool(d5["D5a_passe"] and d5["D5b_passe"])

    # --- D2 : exactitude (second calcul vs tables §8.59/§8.56) ---
    # Le présent script EST le second calcul indépendant (D2a) : il relit
    # les 120 JSON par un chemin distinct et compare valeur par valeur
    # à la table §8.59 (9 champs x 60 paires) : écart exact attendu 0,0.
    ecarts_exact = []
    for r in lignes:
        ref = ref859[r["paire"]]
        for champ in champs:
            if r[champ] != ref[champ]:
                ecarts_exact.append({"paire": r["paire"], "champ": champ,
                                     "reverifie": r[champ],
                                     "table_859": ref[champ]})
    d2 = {"dossiers_lus": 2 * len(lignes), "dossiers_attendus": 120,
          "ecarts_exacts_vs_table_859": ecarts_exact,
          "ecart_max_exact": max(
              [abs(e["reverifie"] - e["table_859"]) for e in ecarts_exact]
              or [0.0]),
          "recoupements_1e9_vs_859_856": ecarts_recoup,
          "passe_recoupements": len(ecarts_recoup) == 0,
          "manquants": manquants,
          "version_non_attendue": versions_inattendues}
    d2["passe"] = bool(2 * len(lignes) == 120 and not ecarts_exact
                       and not ecarts_recoup and not manquants
                       and not versions_inattendues)

    # --- Sensibilités S1, S5, S7 + marges ---
    sens = {}
    for etiquette, ecarts in (("V1_maxsep", e_m_v1), ("V1_sep", e_s_v1),
                             ("V2_maxsep", e_m_v2), ("V2_sep", e_s_v2)):
        c0 = compter(ecarts, 0.0)
        sens[f"S1_sans_plancher|{etiquette}"] = {
            "n_ok_sans_plancher": c0["n_ok"], "n": c0["n"],
            "n_positifs": c0["n_positifs"]}
        c20 = compter(ecarts, PETIT_COHEN) if "maxsep" in etiquette else None
        if c20 is not None:
            sens[f"S5_plancher_Cohen_0.20|{etiquette}"] = {
                "n_ok": c20["n_ok"], "n": c20["n"],
                "n_positifs": c20["n_positifs"]}
    sens["S7_ancien_mc_vers_maxsep"] = {}
    for etiquette, em, eo in (("V1", e_m_v1, e_o_v1), ("V2", e_m_v2, e_o_v2)):
        set_m = set(compter(em, SEUIL)["ok"])
        set_o = set(compter(eo, SEUIL)["ok"])
        sens["S7_ancien_mc_vers_maxsep"][etiquette] = {
            "ancien_mc_n_ok": len(set_o), "maxsep_n_ok": len(set_m),
            "gagnent_classe": sorted(set_m - set_o),
            "perdent_classe": sorted(set_o - set_m),
            "n_changements": len(set_m ^ set_o)}
    a1_o = compter(e_o_v2, SEUIL)
    a2_o = compter(e_o_v1, SEUIL)
    sens["ancien_MC_reference"] = {
        "V2_n_ok": a1_o["n_ok"], "V2_n": a1_o["n"], "V2_n_positifs": a1_o["n_positifs"],
        "V2_somme": a1_o["somme"], "V1_n_ok": a2_o["n_ok"], "V1_n": a2_o["n"],
        "V1_n_positifs": a2_o["n_positifs"], "V1_somme": a2_o["somme"]}
    sens["marges"] = [
        {"paire": r["paire"], "d_maxsep": r["d_maxsep"],
         "marge_maxsep_vs_0.07": r["d_maxsep"] - SEUIL,
         "d_sep": r["d_sep"], "marge_sep_vs_0.07": r["d_sep"] - SEUIL,
         "plancher_maxsep_equiv_sep": r["plancher_maxsep_equiv_sep"],
         "marge_maxsep_vs_equiv":
             r["d_maxsep"] - r["plancher_maxsep_equiv_sep"]}
        for r in lignes
        if abs(r["d_maxsep"] - SEUIL) < 0.05 or r["paire"] in
        ("ICGC", "DEPMAPROT_MYH9", "V4ROT_MUC16")]
    sens["S2_A1_a_24"] = {"maxsep_n_ok": a1_m["n_ok"],
                          "sep_n_ok": a1_s["n_ok"],
                          "maxsep_24_48": a1_m["n_ok"] >= 24,
                          "sep_24_48": a1_s["n_ok"] >= 24}

    portes = {"D1": d1, "D2": d2, "D3": d3, "D4": d4, "D5": d5}
    if d1["passe"] and d2["passe"] and d3["passe"] and d4["passe"] and d5["passe"]:
        verdict = "ADOPTER"
    elif d1["passe"] and d2["passe"] and d5["passe"]:
        verdict = "ADOPTER_SOUS_CONDITION"
    else:
        verdict = "NE_PAS_ADOPTER"
    portes["verdict_propose"] = verdict

    sortie = {"paires": lignes, "portes": portes, "sensibilites": sens,
              "controles": {"manquants": manquants,
                            "version_non_attendue": versions_inattendues,
                            "plancher": SEUIL,
                            "formule_sep": "sep = maxsep/(1+maxsep)",
                            "n_paires": len(lignes)}}
    with open(os.path.join(BASE, "maxsep_decision_864_verify.json"),
              "w", encoding="utf-8") as fh:
        json.dump(sortie, fh, indent=1, ensure_ascii=False)

    print(f"paires lues: {len(lignes)} (V1: {len(v1)}, V2: {len(v2)}, "
          f"descriptif: {len(lignes) - len(v1) - len(v2)})")
    print(f"manquants: {manquants if manquants else 'AUCUN'}")
    print(f"version non attendue: "
          f"{versions_inattendues if versions_inattendues else 'AUCUNE'}")
    print(f"ecarts exacts vs table §8.59: "
          f"{ecarts_exact if ecarts_exact else 'AUCUN'}")
    print(f"recoupements 1e-9 vs §8.59/§8.56/§8.44/phase2: "
          f"{ecarts_recoup if ecarts_recoup else 'AUCUN'}")
    print(f"D1 passe={d1['passe']} A1 maxsep {a1_m['n_ok']}/48 (sep {a1_s['n_ok']}), "
          f"A2 maxsep {a2_m['n_ok']}/8 positifs {a2_m['n_positifs']}/8 (sep {a2_s['n_ok']}), "
          f"HP35 maxsep {hp35['d_maxsep']:+.4f}")
    print(f"D2 passe={d2['passe']} dossiers lus {d2['dossiers_lus']}/120 "
          f"ecart max exact {d2['ecart_max_exact']}")
    print(f"D3 passe={d3['passe']} V1 pire={loo_v1['pire_cas']} "
          f"echecs={loo_v1['suppressions_echouant']} "
          f"V2 pire={loo_v2['pire_cas']} echecs={loo_v2['suppressions_echouant']}")
    print(f"D4 passe={d4['passe']} V1 plancher equiv: {len(d4_ok)}/8 ok={d4_ok} ko={d4_ko}")
    print(f"D5 passe={d5['passe']} D5a={changements_d5a} D5b={changements_d5b}")
    print(f"VERDICT PROPOSE: {verdict}")
    print("ecrit: maxsep_decision_864_verify.json")


if __name__ == "__main__":
    main()
