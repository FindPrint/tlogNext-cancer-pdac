# PROTOCOL_inventaire_depots_878 — Inventaire en lecture seule des dépôts GitHub Ising / cancer (PISTE A, §8.78)

**Date :** 21 novembre 2026. **Auteur :** TagPrint (subagent, piste A).
**Statut :** protocole gelé avant lecture (inventaire en lecture seule — aucun run, aucun
téléchargement de données, aucune écriture sur GitHub, aucune modification de dépôt).
**Référence :** livre blanc §8.1–§8.77, SHA local `e4804934fa832131…` ; pipeline v6.2,
SHA `f07567c4…` (jamais modifié, jamais exécuté ici).

## 1. Question

Quels dépôts GitHub du compte FindPrint contiennent quelque chose d'UTILISABLE comme piste
pour le projet PDAC v6.2 (une cohorte PDAC non tenue, un flux, un protocole, un benchmark),
et lesquels sont vides, abandonnés ou sans rapport ?

## 2. Périmètre

- Compte : FindPrint, dénombré par recherche `user:FindPrint` via le connecteur GitHub
  (`/opt/hatch/bin/github`, `search_repositories`) — 17 dépôts au 21 nov. 2026.
- Inventaire en profondeur (README + arborescence + derniers commits + documents de
  synthèse lus) : `universal-log-research`, `pdac-systems-evidence-preclinical`,
  `apamea-artificial-spin-ice-multiflux`, `TLOG`, `T_log-`, `Simulation-tlog`.
- Nommés seulement (non relus en profondeur) : `tlogNext-cancer-pdac`,
  `tlogNext-cancer-pdac-suite`, `Code`, `pancreatic-cancer-open-data-reproducibility`.
- INTERDIT : `tlogNext-pdac-phase2` (dépôt d'une autre IA) — nommé seulement, contenu
  non lu, non ouvert au-delà de son nom dans la liste des 17.
- Nommés depuis la seule liste de recherche, sans lecture : `Canvas`, `Dissertation-`,
  `BTC_Tlog`, `seismologie-retrospective-cadrage`, `seismologie-retrospective-catalogue`,
  `UNIVERSAL_LOG_30_10_2026`.

## 3. Méthode de lecture (figée)

1. `github status` (connexion vérifiée) puis `search_repositories` (`user:FindPrint`).
2. Pour chaque dépôt cible : `list_commits` (2 derniers, date + SHA + message),
   `get_file_contents` sur la racine (arborescence) et sur `README.md` (SHA blob consigné).
3. Descente dans les sous-dossiers pertinents seulement : `pancréas/`,
   `ising_classique_test/`, `ising_quantique_test/`, `calibration_29*/`, `audit_release/`,
   `output/`, `data/`, `docs/`, `protocols/`, `registry/`, `results/`, `scripts/`,
   `pipelines/`, `Archive/`.
4. Lecture des documents de synthèse : README, `REPOSITORY_MAP_2026-11-20.md`,
   `INVENTAIRE_SOURCES_PDAC_ORDONNEES_20260827.md`,
   `SOURCES_PRECLINIQUES_PDAC_VERIFIEES.md`, `PROTOCOL_003_*`,
   `EXTERNAL_REPLICATION_SCREEN_REPORT_2026-11-20.md`,
   `SCREENING_SOURCE_MANIFEST_2026-11-20.json`,
   `TIRIAC2018_ALL_CONTROL_RUN_SUMMARY.md`, `PROTOCOLE_HOLDOUT_GSE57495.md`,
   `RESULTATS_HOLDOUT_GSE57495.md`, `PIPELINE_BENCHMARKS.md`,
   `RAPPORT_ISING_QUANTIQUE.md`, `STATUS.md` (×2), script
   `audit_GSE194249_candidate.py`.
5. Vérification du statut « tenue / non tenue » de chaque cohorte contre le livre blanc
   local par recherche textuelle (`grep` sur `livre-blanc-pdac-v6.md`, §8.1–§8.77).
6. Aucun téléchargement de matrice, aucun run de pipeline, aucune écriture GitHub.

## 4. Critères d'inclusion / exclusion (décidés avant lecture)

**Une cohorte est CANDIDATE pour la piste B si :** elle est PDAC (tumeur, organoïde,
lignée ou modèle préclinique documenté) ; ses données sont ouvertes et accessibles
(accession stable ou supplément public) ; son n est ≥ 40 (minimum v6.2 fast) ou son
déficit est explicitement documenté ; elle n'a jamais été courue dans le livre blanc
(§8.1–§8.77) ; sa couverture des 12 gènes v4 est vérifiée ou déclarée non vérifiée
(jamais supposée).

**Exclusions :** cohortes déjà courues ou déjà tenues (relecture interdite §8.64.7) ;
n < 40 ; accès contrôlé ou hors périmètre ; séries sans table d'échantillons ;
ordre dérivé de survie, de réponse clinique ou du transcriptome lui-même ;
re-tests déguisés (échantillons déjà inclus dans une cohorte tenue).

**Une ressource non-cohorte est UTILE si :** benchmark ou calibration reproductible
du pipeline (version nommée, jamais importée comme verdict v6.2) ; protocole ou
grille réutilisable ; script d'accès aux données avec provenance ; méthode de
rotation des contrôles documentée.

## 5. Règles de jugement

- Ce qui vient d'un autre dépôt est une PISTE, jamais un verdict importé (règle du
  15 nov. 2026) ; les résultats d'une autre expérience sont des hypothèses.
- « Non vérifié » est un statut à part entière : une couverture de gènes ou un n
  non lisible depuis le dépôt est écrit « non vérifié », jamais deviné.
- Les versions de pipeline trouvées (≤ v6.0) ne sont PAS v6.2 ; leurs résultats ne
  se transfèrent pas à v6.2.
- Toute date est la date du dernier commit GitHub (UTC) ; tout SHA est le SHA du
  commit ou du blob lu, consigné dans `PROVENANCE_878.md`.

## 6. Livrables

- `section_8.78_inventaire_depots.md` (cette section du livre blanc).
- `PROTOCOL_inventaire_depots_878.md` (ce fichier).
- `PROVENANCE_878.md` (sources lues, dates, SHA).

## 7. Écarts

Aucun. Le dépôt interdit n'a pas été lu. Aucun run, aucun téléchargement, aucune
écriture GitHub n'a eu lieu.
