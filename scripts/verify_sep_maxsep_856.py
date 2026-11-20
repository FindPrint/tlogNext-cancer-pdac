#!/usr/bin/env python3
"""Chantier §8.56 — SECOND calcul independant (PROTOCOL_sep_maxsep_856.md §5.2).
Chemin de code distinct de extract_sep_maxsep_856.py : re-lecture directe
des master_results.json par parcours JSON explicite (pas de fonction
partagee), recalcul de sep = maxsep/(1+maxsep), comparaison a
sep_maxsep_856_table.json. Ecart attendu : 0,0 exact sur 120/120 runs.
Sortie : sep_maxsep_856_verify.json
"""
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Liste des 120 dossiers : reconstruite independamment (meme source gelée,
# manifest_v62_dedup_844.txt + listes V1/V3-V5 du protocole §2).
DOSSIERS_V1 = [
    "results_fast_v62_hp35", "results_fast_v62_hp35_nul",
    "results_fast_v62_tcga_v4", "results_fast_v62_tcga_v4_nul",
    "results_fast_v62_geo71729", "results_fast_v62_geo71729_nul",
    "results_fast_v62_geo62452", "results_fast_v62_geo62452_nul",
    "results_fast_v62_icgc", "results_fast_v62_icgc_nul",
    "results_fast_v62_immune_tcga", "results_fast_v62_immune_tcga_nul",
    "results_fast_v62_parp_tcga", "results_fast_v62_parp_tcga_nul",
    "results_fast_v62_depmap", "results_fast_v62_depmap_nul",
]
DOSSIERS_DESCR = [
    "results_fast_v62_prolif", "results_fast_v62_prolif_nul",
    "results_fast_v62_prmt5flux", "results_fast_v62_prmt5flux_nul",
    "results_fast_v62_mtap", "results_fast_v62_mtap_nul",
    "results_fast_v62_v4r_purity", "results_fast_v62_v4r_purity_nul",
]
ROT_EXIST = {
    "results_fast_v61_v4r_cldn18_dedup", "results_fast_v61_v4r_cldn18_dedup_nul",
    "results_fast_v62_immrot_ctla4_dedup", "results_fast_v62_immrot_ctla4_dedup_nul",
    "results_fast_v62_depmaprot_aco2_dedup", "results_fast_v62_depmaprot_aco2_dedup_nul_sp",
    "results_fast_v62_parprot_parp1_dedup", "results_fast_v62_parprot_parp1_dedup_nul_sp",
}


def dossiers_rotations():
    # Le manifeste porte deja les 44 paires dedup (88 dossiers) : les 4
    # paires §8.41 (CLDN18, CTLA4, ACO2, PARP1) n'y figurent pas (verifie :
    # grep cldn18|ctla4|aco2|parp1 sur le manifeste = 0 ligne) ; on ajoute
    # simplement leurs 8 dossiers.
    vus = set()
    for ligne in open(HERE / "manifest_v62_dedup_844.txt"):
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#"):
            continue
        _nom, _entree, sortie = ligne.split("|")
        vus.add(sortie)
    vus |= ROT_EXIST
    return sorted(vus)


def main():
    dossiers = DOSSIERS_V1 + dossiers_rotations() + DOSSIERS_DESCR
    table = json.loads((HERE / "sep_maxsep_856_table.json").read_text())
    # Index (paire, cote) -> valeurs de la table de l'extracteur.
    ref = {}
    for lig in table["paires"]:
        ref[(lig["paire"], "R")] = (lig["maxsep_R"], lig["sep_R"])
        ref[(lig["paire"], "N")] = (lig["maxsep_N"], lig["sep_N"])
    # Retrouver le dossier de chaque (paire, cote) : l'extracteur a note les
    # dossiers dans les memes regles ; on les re-deduit ici par le nom de
    # dossier lui-meme (suffixe _nul / _nul_sp = NUL).
    # On verifie par le contenu : chaque dossier appartient a exactement une
    # paire via la table des dossiers de l'extracteur — reconstituee ici
    # depuis le manifeste et les listes, puis comparee par valeurs.
    # Methode retenue : pour chaque dossier, lire maxsep/sep, puis chercher
    # la (paire, cote) dont la table donne exactement ces valeurs.
    ecarts, lus, introuvables = [], 0, []
    for d in dossiers:
        p = HERE / d / "master_results.json"
        if not p.is_file():
            introuvables.append(str(p))
            continue
        j = json.loads(p.read_text())
        opt = j["run_pipeline"]["threshold_metadata"]["threshold_optimization"]
        bc = opt["best_config"]
        m = float(bc["metrics"]["max_separation"])
        s = 0.0 if m == 0 else m / (1.0 + m)
        lus += 1
        # Recherche de la paire correspondante par egalite exacte des valeurs.
        candidats = [(k, v) for k, v in ref.items()
                     if v[0] == m and v[1] == s]
        if len(candidats) != 1:
            ecarts.append(f"{d}: {len(candidats)} candidat(s) exact(s) "
                          f"pour maxsep={m!r} sep={s!r}")
        # (L'unicite des valeurs n'etant pas garantie en theorie, on verifie
        # aussi globalement : multiset des valeurs.)
    # Comparaison globale par multisets (robuste aux collisions de valeurs).
    vals_table = sorted([(v[0], v[1]) for v in ref.values()])
    vals_relus = []
    for d in dossiers:
        j = json.loads((HERE / d / "master_results.json").read_text())
        m = float(j["run_pipeline"]["threshold_metadata"]
                  ["threshold_optimization"]["best_config"]["metrics"]["max_separation"])
        vals_relus.append((m, 0.0 if m == 0 else m / (1.0 + m)))
    vals_relus.sort()
    ecart_max = 0.0
    for (m1, s1), (m2, s2) in zip(vals_table, vals_relus):
        ecart_max = max(ecart_max, abs(m1 - m2), abs(s1 - s2))
    ok = (lus == 120 and not introuvables and not ecarts
          and len(vals_table) == len(vals_relus) == 120 and ecart_max == 0.0)
    rapport = {"dossiers_lus": lus, "dossiers_attendus": 120,
               "dossiers_introuvables": introuvables,
               "ecarts_par_paire": ecarts,
               "ecart_max_global_multiset": ecart_max,
               "multisets_egaux": vals_table == vals_relus,
               "verdict_verification": "OK" if ok else "ECHEC"}
    (HERE / "sep_maxsep_856_verify.json").write_text(
        json.dumps(rapport, indent=1, ensure_ascii=False))
    print(json.dumps(rapport, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
