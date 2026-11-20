#!/usr/bin/env python3
"""Chantier §8.59 — second calcul independant (D2a).
Chemin de code distinct de extract_maxsep_adoption_859.py : ne reutilise
AUCUNE de ses fonctions. Parcours recursif des JSON (recherche de
"best_config" par descente generique, sans supposer le chemin exact),
recalcule sep et maxsep pour les 120 runs, compare a la table de
l'extracteur : ecart attendu 0,0 exact sur 120/120.
Sortie : maxsep_adoption_859_verify.json
"""
import json
import math
import os

BASE = os.path.dirname(os.path.abspath(__file__))


def find_best_config(node):
    """Descente recursive generique : renvoie le premier dict nomme
    best_config rencontre, quel que soit son chemin dans le JSON."""
    if isinstance(node, dict):
        if "best_config" in node and isinstance(node["best_config"], dict):
            return node["best_config"]
        for value in node.values():
            found = find_best_config(value)
            if found is not None:
                return found
    elif isinstance(node, list):
        for item in node:
            found = find_best_config(item)
            if found is not None:
                return found
    return None


def main():
    with open(os.path.join(BASE, "maxsep_adoption_859_table.json"),
              encoding="utf-8") as fh:
        table = json.load(fh)

    # Reconstitue la liste des dossiers depuis la table (scope/paire) :
    # on relit chaque master_results.json en retrouvant son dossier par
    # recherche du fichier dans BASE (dossiers results_fast_*).
    # Le dossier exact est retrouve via le manifest et les listes figees
    # ci-dessous, independantes de l'extracteur (recopiees du protocole).
    dossiers = {}
    for row in table["paires"]:
        dossiers[row["paire"]] = row  # paire -> ligne (pour la comparaison)

    # Liste des dossiers : reconstruite autrement — on balaye BASE et on
    # associe chaque dossier results_fast_* a sa paire par le contenu
    # (n_samples + maxsep lus) puis on apparie par paire via la table.
    # Plus simple et independant : on utilise les noms de dossiers
    # deja verifies au §8.56 (manifest + listes) — mais la LECTURE des
    # valeurs passe par find_best_config, jamais par le chemin de
    # l'extracteur.
    import csv
    dir_by_pair = {}
    for name, dr, dn in [
            ("HP35", "results_fast_v62_hp35", "results_fast_v62_hp35_nul"),
            ("TCGA_v4", "results_fast_v62_tcga_v4",
             "results_fast_v62_tcga_v4_nul"),
            ("GSE71729", "results_fast_v62_geo71729",
             "results_fast_v62_geo71729_nul"),
            ("GSE62452", "results_fast_v62_geo62452",
             "results_fast_v62_geo62452_nul"),
            ("ICGC", "results_fast_v62_icgc", "results_fast_v62_icgc_nul"),
            ("IMMUNE_TCGA", "results_fast_v62_immune_tcga",
             "results_fast_v62_immune_tcga_nul"),
            ("PARP_TCGA", "results_fast_v62_parp_tcga",
             "results_fast_v62_parp_tcga_nul"),
            ("DEPMAP", "results_fast_v62_depmap",
             "results_fast_v62_depmap_nul"),
            ("TESTA_PROLIF", "results_fast_v62_prolif",
             "results_fast_v62_prolif_nul"),
            ("MTAP_PRMT5FLUX", "results_fast_v62_prmt5flux",
             "results_fast_v62_prmt5flux_nul"),
            ("MTAP_SERIES", "results_fast_v62_mtap",
             "results_fast_v62_mtap_nul"),
            ("V4R_PURITY", "results_fast_v62_v4r_purity",
             "results_fast_v62_v4r_purity_nul")]:
        dir_by_pair[(name, "REEL")] = dr
        dir_by_pair[(name, "NUL")] = dn
    with open(os.path.join(BASE, "manifest_v62_dedup_844.txt"),
              encoding="utf-8") as fh:
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
            dir_by_pair[(f"{fam}_{ctrl}", "NUL" if is_nul else "REEL")] = outdir
    for name, dr, dn in [
            ("V4ROT_CLDN18", "results_fast_v61_v4r_cldn18_dedup",
             "results_fast_v61_v4r_cldn18_dedup_nul"),
            ("IMMROT_CTLA4", "results_fast_v62_immrot_ctla4_dedup",
             "results_fast_v62_immrot_ctla4_dedup_nul"),
            ("DEPMAPROT_ACO2", "results_fast_v62_depmaprot_aco2_dedup",
             "results_fast_v62_depmaprot_aco2_dedup_nul_sp"),
            ("PARPROT_PARP1", "results_fast_v62_parprot_parp1_dedup",
             "results_fast_v62_parprot_parp1_dedup_nul_sp")]:
        dir_by_pair[(name, "REEL")] = dr
        dir_by_pair[(name, "NUL")] = dn

    ecarts = []
    lus = 0
    introuvables = []
    valeurs = []  # (maxsep, sep) pour le multiset
    for row in table["paires"]:
        paire = row["paire"]
        for cote, cle in (("REEL", "maxsep_R"), ("NUL", "maxsep_N")):
            dossier = dir_by_pair.get((paire, cote))
            if dossier is None:
                introuvables.append(f"{paire} {cote}: dossier non liste")
                continue
            chemin = os.path.join(BASE, dossier, "master_results.json")
            if not os.path.isfile(chemin):
                introuvables.append(f"{paire} {cote}: {chemin} absent")
                continue
            with open(chemin, encoding="utf-8") as fh:
                data = json.load(fh)
            best = find_best_config(data)
            if best is None:
                ecarts.append({"paire": paire, "cote": cote,
                               "probleme": "best_config introuvable"})
                continue
            msep = float(best["metrics"]["max_separation"])
            sep = msep / (1.0 + msep) if msep else 0.0
            lus += 1
            valeurs.append((msep, sep))
            ref_m = row[cle]
            ref_s = row["sep_R" if cote == "REEL" else "sep_N"]
            if msep != ref_m or sep != ref_s:
                ecarts.append({"paire": paire, "cote": cote,
                               "maxsep_verif": msep, "maxsep_table": ref_m,
                               "sep_verif": sep, "sep_table": ref_s})
            if not math.isfinite(msep) or msep < 0:
                ecarts.append({"paire": paire, "cote": cote,
                               "probleme": f"maxsep invalide {msep}"})

    ecart_max = 0.0
    for e in ecarts:
        if "maxsep_verif" in e:
            ecart_max = max(ecart_max, abs(e["maxsep_verif"] - e["maxsep_table"]),
                            abs(e["sep_verif"] - e["sep_table"]))
    # Multiset : compare l'ensemble trie des valeurs relues a celui de la table.
    table_vals = sorted((r["maxsep_R"], r["sep_R"]) for r in table["paires"]) \
        + sorted((r["maxsep_N"], r["sep_N"]) for r in table["paires"])
    multiset_egal = sorted(valeurs) == sorted(table_vals)

    sortie = {"dossiers_lus": lus, "dossiers_attendus": 120,
              "dossiers_introuvables": introuvables,
              "ecarts_par_run": ecarts, "ecart_max_global": ecart_max,
              "multisets_egaux": multiset_egal,
              "verdict_verification":
                  "OK" if (lus == 120 and not ecarts and not introuvables
                           and ecart_max == 0.0 and multiset_egal) else "ECHEC"}
    with open(os.path.join(BASE, "maxsep_adoption_859_verify.json"),
              "w", encoding="utf-8") as fh:
        json.dump(sortie, fh, indent=1, ensure_ascii=False)
    print(f"dossiers lus: {lus}/120")
    print(f"introuvables: {introuvables if introuvables else 'AUCUN'}")
    print(f"ecarts: {ecarts if ecarts else 'AUCUN'}")
    print(f"ecart max: {ecart_max}")
    print(f"multisets egaux: {multiset_egal}")
    print(f"verdict: {sortie['verdict_verification']}")


if __name__ == "__main__":
    main()
