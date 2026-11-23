#!/usr/bin/env python3
"""Generateur du lot suivant §8.93 (double piste) — jobs local + registre.

Ecrit (dans ~/workspace/runs/pdac-v6/nulls_lot_next/) :
  jobs_local_e2.txt — 1330 lignes "label input out" pour
      run_nulls_parallel.sh jobs (moitie locale, E2).
  ledger.csv        — une ligne par (paire, graine) : 2850 lignes.
  LEDGER.md         — registre unique, seule source de verite du lot.

Decoupage gele ici (PROPOSITION, pas un fait du protocole — le protocole
§8.93 ne definit pas de lot suivant ; voir README.md) : 190 nuls frais
supplementaires par paire (graines 9111–9300), pour passer de 10 a 200
nuls frais par paire (cible §8.53 : ~200 nuls pour un plancher stable).
  GitHub (E1, 8 paires principales) : 1520 runs.
  Local  (E2, 7 paires A2 restantes) : 1330 runs.
Aucune graine recouvrante : la coupure est par paires ENTIERES.
"""
import csv
from pathlib import Path

NEXT = Path(__file__).resolve().parent
GRAINES = list(range(9111, 9301))

# (nom paire, base CSV reel, n lignes, SHA-256 complet du CSV reel)
PAIRES_E1 = [  # GitHub — 8 paires principales
    ("hp35", "test_biophysique_input", 1000,
     "6b656540598579a37cbc97c9dfbee26bf6186611f84f397cf9e7e6f1e88bb35e"),
    ("tcga_v4", "pdac_tcga_fluxes_v4", 178,
     "e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0"),
    ("geo71729", "pdac_geo71729_fluxes", 145,
     "7d69fa888f15e9a1a128e149e35f9eeacac106198c33929dfc51e113ee8c0cf1"),
    ("geo62452", "pdac_geo62452_fluxes", 69,
     "d7419c0ec3ed649d98ba920411ef5f41a056caa69b38c6b9a5e3ab702cc03abf"),
    ("icgc", "pdac_icgc_fluxes", 70,
     "710d41e55d32360b95f81113579eac4b6de023130b77410bd9ac3df906b61941"),
    ("immune_tcga", "pdac_immune_tcga_fluxes", 178,
     "66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e"),
    ("parp_tcga", "pdac_tcga_fluxes_parp", 178,
     "c9549b68280b2f4ca3d9b62020efa21ab97249b10e176de87ec528a0258c4309"),
    ("depmap", "pdac_depmap_fluxes", 45,
     "7d605fefb412fe16151a1b2508dffa6a1c2b8353600dccffd4af3333198e37f8"),
]
PAIRES_E2 = [  # Local — 7 paires A2 restantes
    ("geo21501", "pdac_869_geo21501_fluxes", 132,
     "3d7c1bfe1a4ce02cc7bc4087791e8175efc03338e0643c98463a836e9cd46ba9"),
    ("geo79668", "pdac_870_geo79668_fluxes", 51,
     "7744bc5a82fe80055b5ab9231fc7ae5395354f643b5b7cd1fdfce8aa6656107a"),
    ("geo60979", "pdac_871_geo60979_fluxes", 49,
     "51a7fa56869a2d8db788bc02f78f24d435a98cb3cefa50bbcb2b51bbb190554e"),
    ("yeh_ff", "pdac_874_yeh_ff_fluxes", 42,
     "db258c9900e0f6c603ff62f008e7cee6a4621ee1632a9d69d1544db86d58fe44"),
    ("geo57495", "pdac_879_geo57495_fluxes", 63,
     "224f98eb9cc7092e05b490b1e053edd14793e3def147890be0bab567630bb51c"),
    ("gdc_organoid", "pdac_885_gdc_organoid_fluxes", 44,
     "a83b98175bdbc33525ba8a175aa898504d2cc44125b891d0902c6c6c26345eaf"),
    ("gse194249", "pdac_888_gse194249_fluxes", 84,
     "7799a62a6c1145b728e60a2d1126a93b86c28123744c0dc904e454c35ae9aeda"),
]


def main():
    # --- jobs local (E2) ---
    jobs = []
    for nom, base, _n, _sha in PAIRES_E2:
        for s in GRAINES:
            jobs.append(f"{nom}_nul_s{s} {base}_nul_s{s}.csv "
                        f"results_fast_v62_893_{nom}_nul_s{s}")
    with open(NEXT / "jobs_local_e2.txt", "w") as f:
        f.write("# Lot suivant §8.93 — moitie LOCALE (E2, 7 paires x 190 graines 9111-9300)\n")
        f.write("# Lignes : label input out — pour run_nulls_parallel.sh jobs <fichier>\n")
        f.write("\n".join(jobs) + "\n")

    # --- registre (CSV + MD) ---
    rows = []
    for nom, base, _n, _sha in PAIRES_E1:
        for s in GRAINES:
            rows.append((nom, s, "GitHub",
                         f"data/{base}.csv (reel, regenere sur le runner)",
                         f"results_fast_gha_893_{nom}_nul_s{s}", "a faire"))
    for nom, base, _n, _sha in PAIRES_E2:
        for s in GRAINES:
            rows.append((nom, s, "Local",
                         f"{base}_nul_s{s}.csv",
                         f"results_fast_v62_893_{nom}_nul_s{s}", "a faire"))

    with open(NEXT / "ledger.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["paire", "graine", "piste", "input", "dossier_sortie", "statut"])
        w.writerows(rows)

    lignes = []
    lignes.append("# REGISTRE UNIQUE — Lot suivant §8.93, double piste (GitHub + local)")
    lignes.append("")
    lignes.append("**Seule source de vérité du lot.** Toute (paire, graine) apparaît ici")
    lignes.append("UNE fois, sur UNE seule piste. Si un run est relancé ailleurs, le")
    lignes.append("registre est corrigé avant, jamais après.")
    lignes.append("")
    lignes.append("## Définition du lot (PROPOSITION, pas un fait du protocole)")
    lignes.append("")
    lignes.append("Le protocole gelé §8.93 (PROTOCOL_nulls_distribution_893.md) ne définit")
    lignes.append("pas de « lot suivant » : il mesure la distribution par réplique (1000")
    lignes.append("permutations) et ne valide que par 10 nuls frais pipeline par paire")
    lignes.append("(graines 9101–9110, file en cours). La cible qu'il nomme (§8.53) est")
    lignes.append("~200 nuls par paire pour un plancher stable. Le complément logique")
    lignes.append("proposé ici : **190 nuls frais supplémentaires par paire, graines")
    lignes.append("9111–9300**, pour passer de 10 à 200 nuls frais par paire.")
    lignes.append("**Total : 2850 runs** (15 paires × 190).")
    lignes.append("")
    lignes.append("## Coupure GitHub / local (par paires ENTIÈRES, aucune graine recouvrante)")
    lignes.append("")
    lignes.append("| Piste | Paires | Runs | Justification |")
    lignes.append("|---|---|---|---|")
    lignes.append("| GitHub Actions | E1 — 8 paires principales (HP35, TCGA v4, GSE71729, GSE62452, ICGC, Immunitaire TCGA, PARP TCGA, DepMap) | 1520 | Suit la structure E1/E2 du protocole gelé ; chaque paire reste entière sur une piste ; la paire la plus lente (HP35, n=1000, ~7 min/run) va sur la piste parallèle |")
    lignes.append("| Local (machine ici) | E2 — 7 paires A2 restantes (GSE21501, GSE79668, GSE60979, Yeh FF, GSE57495, GDC ORGANOID, GSE194249) | 1330 | Petites paires (n=42 à 132, ~1 min/run), adaptées au lanceur parallèle local 2 workers |")
    lignes.append("")
    lignes.append("Graines 9111–9300 partout : disjointes de 9101–9110 (lot en cours), de")
    lignes.append("3000–3999 (réplique §8.93) et de 42 (nul unique historique).")
    lignes.append("")
    lignes.append("## Règles")
    lignes.append("")
    lignes.append("- Pipeline v6.2, SHA `f07567c4…`, jamais modifié ; vérifié avant chaque")
    lignes.append("  lot (local) et à chaque job (GitHub).")
    lignes.append("- Nuls construits par `scripts/build_null_893.py` (règle gelée :")
    lignes.append("  `default_rng(graine)`, permutation des lignes entières, colonne de")
    lignes.append("  contrôle inchangée) — même script des deux côtés, donc même graine +")
    lignes.append("  même CSV réel = même nul, octet à octet. Validé le 22 nov. 2026 :")
    lignes.append("  (TCGA v4, 9101) reproduit exactement le fichier du lot en cours")
    lignes.append("  (SHA `22f39bf7…e8fa`).")
    lignes.append("- Dossiers de sortie disjoints : local `results_fast_v62_893_<paire>_nul_s<graine>`")
    lignes.append("  (comme la file en cours), GitHub `results_fast_gha_893_<paire>_nul_s<graine>`.")
    lignes.append("- Reprise : un run dont `master_results.json` existe est sauté, jamais")
    lignes.append("  écrasé (règle des deux lanceurs).")
    lignes.append("- Artefacts GitHub : seuls les `master_results.json`, gzippés, rétention")
    lignes.append("  7 jours, un artefact par job (10 runs).")
    lignes.append("- Statuts : `a faire` → `en cours` → `fait` (master_results.json vérifié)")
    lignes.append("  ou `echec` (exit ≠ 0, à consigner). Le statut se met à jour dans ce")
    lignes.append("  fichier ET dans ledger.csv, ensemble.")
    lignes.append("")
    lignes.append("## Résumé par paire")
    lignes.append("")
    lignes.append("| Paire | n | Piste | Graines | Runs | Dossier de sortie (préfixe) |")
    lignes.append("|---|---|---|---|---|---|")
    for nom, base, n, _sha in PAIRES_E1:
        lignes.append(f"| {nom} | {n} | GitHub | 9111–9300 | 190 | results_fast_gha_893_{nom}_nul_s… |")
    for nom, base, n, _sha in PAIRES_E2:
        lignes.append(f"| {nom} | {n} | Local | 9111–9300 | 190 | results_fast_v62_893_{nom}_nul_s… |")
    lignes.append("")
    lignes.append("## Table complète (2850 lignes)")
    lignes.append("")
    lignes.append("| Paire | Graine | Piste | Entrée | Dossier de sortie | Statut |")
    lignes.append("|---|---|---|---|---|---|")
    for nom, s, piste, entree, sortie, statut in rows:
        lignes.append(f"| {nom} | {s} | {piste} | {entree} | {sortie} | {statut} |")
    with open(NEXT / "LEDGER.md", "w") as f:
        f.write("\n".join(lignes) + "\n")
    print(f"jobs_local_e2.txt : {len(jobs)} lignes")
    print(f"ledger.csv / LEDGER.md : {len(rows)} lignes")


if __name__ == "__main__":
    main()
