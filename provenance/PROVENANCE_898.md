# PROVENANCE — §8.98 Suivi §8.93 : chaque paire jugée contre 200 nuls frais pipeline

Section : `section_8.98_suivi_nulls_200.md` (23 novembre 2026).
Lot : 190 nuls frais par paire, graines 9111–9300, pour atteindre
200 nuls frais par paire (avec les 10 du §8.93, graines 9101–9110).
Total 2850 runs. Go de Zackary : 22 novembre 2026, 11h32 EST
(« Allez s'y »), après la publication §8.93–§8.97.

Règle de provenance (AGENTS.md, 27 oct. 2026) : source complète,
nature des lignes, comment chaque valeur a été produite, hachages
des données, et ce qui manque. Rien n'est présenté sans sa
provenance.

## 1. Protocole et registre du lot

- **Protocole gelé §8.93** : `PROTOCOL_nulls_distribution_893.md`,
  SHA d'origine
  `d2cdbc3d589d3be61a506f7be2a250d3d4a1c9adc21d1327c8ffc7a61f6529a0`.
  Ce lot est une PROPOSITION, pas un fait du protocole : le
  protocole gelé valide par 10 nuls frais par paire et ne définit
  pas de « lot suivant ».
- **Registre du lot** : `nulls_lot_next/LEDGER.md`, SHA-256
  `2983cf0f545d7e637f9cee8cf9d8400f6b8fd25d70457798290470859e7a9eb1`,
  2989 lignes, 391 064 octets. Sections de suivi du 22–23 nov.
  2026 (runs GitHub #2/#3/E2, scission E2, lot local, trois
  téléchargements, agrégation).
- **Registre machine** : `nulls_lot_next/ledger.csv`, SHA-256
  `10669164ef4fb325939f0cd3701568f482df10c5bd7c7f77b850bbd0766bed69`,
  2851 lignes avec en-tête (2850 lignes de runs), 353 828 octets,
  statut « telecharge » sur les 2850 lignes. Sauvegarde avant
  mise à jour : `ledger_avant_telechargement.csv`. Avant la
  scission E2 : sauvegarde `ledger_avant_scission_e2.csv`
  (570 lignes piste Local → GitHub).

## 2. Pipeline et construction des nuls

- **Pipeline v6.2 (version de travail)** :
  `../biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
  624 157 octets. Vérifié inchangé en début et en fin de lot
  local. v6.1 (référence) SHA `2af5e5ce…`, v6 SHA `bb8bbdba…`.
  Le pipeline exclut la colonne de contrôle des flux analysés
  par construction (ligne 6787 : `c != control_col`).
- **Constructeur de nuls** :
  `nulls_lot_next/scripts/build_null_893.py`, SHA-256
  `572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467`.
  Règle gelée : `default_rng(graine)`, permutation des lignes
  entières, colonne de contrôle inchangée. Validé bit-à-bit le
  22 nov. 2026 : (TCGA v4, graine 9101) reproduit exactement le
  fichier du lot §8.93, SHA
  `22f39bf7b6ed0efc4c065347de94ef829e50f1e1df7afb9677686061c005e8fa`.
  Les 1330 CSV de nuls locaux ont été construits avant les runs
  (SHAs dans `nulls_893_next_files.json`) ; même script des deux
  côtés, donc même graine + même CSV réel = même nul, octet à
  octet.
- **Nature des lignes** : chaque nul est une permutation des
  lignes entières du CSV réel de sa paire (structure ordonnée
  brisée, marginales conservées). Ce n'est pas un nul biologique.
  Contrôle `step` pour les 15 paires ; KRAS absent des flux.

## 3. Exécution — piste GitHub

Dépôt : FindPrint/tlogNext-pipeline-actions
(https://github.com/FindPrint/tlogNext-pipeline-actions).

- **Run #2** : https://github.com/FindPrint/tlogNext-pipeline-actions/actions/runs/45056686992
  (workflow `pipeline-nulls-lot.yml`, commit `0511dae`,
  correctif matrice, 152 jobs, timeout 120 min). 146 succès, 6
  jobs HP35 annulés à la limite de 2 h (blocs 2, 5, 7, 8, 14, 17
  = 60 runs), 0 échec, 146 artefacts, conclusion « cancelled »,
  fin 22 nov. 19h13 EST. Données brutes des jobs et artefacts :
  `goals/pdac-pseudo-time-validation-tlog28-cancer-project/hidden_files/runs/pdac-v6/nulls_lot_next/gha2_jobs_p1.json`,
  `gha2_jobs_p2.json`, `gha2_artifacts.json`.
- **Relance #3** : https://github.com/FindPrint/tlogNext-pipeline-actions/actions/runs/45087899473
  (workflow `pipeline-nulls-lot-rerun.yml`, commit `05cf9b8`,
  timeout 360 min). 6/6 jobs, 60 runs HP35 récupérés à
  l'identique (mêmes graines, mêmes entrées), conclusion
  « success », fin 22 nov. 22h20 EST. 6 artefacts (~7,5 Mo
  chacun).
- **Run E2** : https://github.com/FindPrint/tlogNext-pipeline-actions/actions/runs/45170178139
  (workflow `pipeline-nulls-lot-e2.yml`, commit `0dba356`, 57
  jobs, timeout 360 min). 57/57 jobs réussis (geo57495,
  gdc_organoid, gse194249, blocs 0–18), 0 échec, 0 annulé,
  conclusion « success », fin 23 nov. ~08h35 EST.
- **Scission E2** : 23 nov. ~07h00, go de Zackary (06h55).
  geo57495, gdc_organoid, gse194249 (570 runs) basculés du local
  vers GitHub ; local garde yeh_ff. Totaux finaux : GitHub 2090
  runs, local 760 runs. CSV réels poussés dans `data/` du dépôt
  (commit `4990758`) ; workflow poussé (commit `0dba356`).

## 4. Exécution — piste locale

- Unité systemd `v62-nulls-next-local`, lanceur parallèle
  `run_nulls_parallel.sh` (`xargs -P 2`, 2 workers).
  760/760 runs, bilan ok=9, sautés=751, échecs=0, fin 23 nov.
  07h06 EST (12:06:55 UTC). Log :
  `runs_nulls_parallel_jobs-jobs_local_e2.log`. Gardien (hook de
  surveillance, 180 s) : 0 run perdu sur les redémarrages
  machine du lot. Fichier de jobs réduit à la scission :
  `nulls_lot_next/jobs_local_e2.txt` (760 jobs ; original
  `jobs_local_e2_full_1330.txt`).
- Dossiers de sortie : locaux
  `results_fast_v62_893_<paire>_nul_s<graine>`, GitHub
  `results_fast_gha_893_<paire>_nul_s<graine>`.

## 5. Téléchargement des artefacts

- **Quand et comment** : 23 novembre 2026, 08h37–09h20, via le
  navigateur, 209 artefacts (146 run #2 + 6 run #3 + 57 run E2),
  ~1,3 Go au total. Dossier de session :
  `~/workspace/browser_downloads/sess-1729575752/`.
- **Vérification run #3** : SHA-256 bit-à-bit contre les digests
  GitHub, 6/6 conformes (s9131-s9140, s9161-s9170, s9181-s9190,
  s9191-s9200, s9251-s9260, s9281-s9290 ; 1 doublon de
  s9131-s9140 ignoré).
- **Vérification run E2** : tailles exactes 57/57 (conformes
  aux reçus du navigateur) et intégrité zip 57/57.
- **Vérification run #2** : 209 artefacts distincts au total,
  210 fichiers testés, 0 corrompu.
- **Dette nommée** : la vérification SHA-256 des artefacts E2
  et run #2 contre les digests GitHub a été impossible — l'API
  GitHub a répondu 403 (limite de requêtes non authentifiées).
  À refaire à la prochaine occasion. Les artefacts restent sur
  GitHub jusqu'à ~29 nov. 2026 (rétention 7 jours).
- **Extraction** : 2090 `master_results.json` GitHub + 760
  locaux = 3000 nuls (200 par paire, graines 9101–9300),
  0 manquant, inventaire vérifié le 23 nov. 10h46.

## 6. Agrégation

- **Script** : `nulls_lot_next/analyse_lot_next.py`, SHA-256
  `c8d7d23fc57bc54411366cefe209f9d2dc8060377764ba7dbf0007eca3f3ca05`.
  Exécution : 23 nov. 10h52, exit 0, 3000/3000 nuls lus.
- **Comment chaque valeur est produite** : maxsep lu dans
  chaque `master_results.json` au chemin
  `run_pipeline.threshold_metadata.threshold_optimization.
  best_config.metrics.max_separation` (même chemin que
  `replica_nulls_893.read_best_config`) ; maxsep réel de chaque
  paire repris de `nulls_dist_893_table.json` (§8.93), aucune
  valeur re-saisie à la main ; dossiers des nuls 9111–9300 lus
  dans `ledger.csv`, dossiers 9101–9110 en
  `results_fast_v62_893_*` ; verdicts par `juger()` = règle
  gelée §8.93 §4 (plancher 0,07) ; médiane et p95 par
  interpolation linéaire (position p×(n−1), n = 200) ; valeurs
  arrondies à 4 décimales dans les sorties.
- **Sorties** :
  - `nulls_lot_next/nulls_lot_next_table.json`, SHA-256
    `351d929c8a923f678a9c6658dc359fd4b0c66d468386e8a80561ac87ce488565`,
    6179 octets.
  - `nulls_lot_next/nulls_lot_next_table.csv`, SHA-256
    `80b2cf14624f30b0332a176573ed5efbb55fd38909a06730bbb783428c75e0ac`,
    1450 octets.
- **Table des réels (§8.93)** : `nulls_dist_893_table.json`,
  SHA-256
  `3ce39accab00dae86e713794bc683e8d9f550e8b22a660576837b67f5dad27fd`.

## 7. Anciens verdicts comparés (§8.93)

Source : `section_8.93_nulls_distribution.md` (§8.93.2.2,
§8.93.2.5) et `nulls_dist_893_table.json` (SHA ci-dessus).
Verdicts §8.93 (réplique 1000 permutations + 10 nuls frais) :
HP35, TCGA v4, Immunitaire TCGA, PARP TCGA, GSE57495 SOLIDES ;
ICGC, DepMap, GSE79668, GSE60979, GSE131050 Yeh FF FRAGILES ;
GSE71729, GSE62452, GSE21501, GDC ORGANOID, GSE194249 NON.
A2-distrib 5/15, positifs 12/15 (d_maxsep contre le nul graine
42 > 0), LOO 4/14. La comparaison 14/15 inchangés / ICGC seul
changement a été vérifiée par relecture des deux tables
(voir §8.98.5).

## 8. Ce qui manque

- Vérification SHA-256 bit-à-bit de 203 des 209 artefacts
  contre les digests GitHub (dette §5) — à refaire tant que les
  artefacts sont sur GitHub (~29 nov. 2026).
- La réplique de 1000 permutations du §8.93 n'a pas été refaite
  pour ce lot : la distribution est faite de nuls pipeline
  seulement.
- Aucune recommandation clinique. Aucun run de pipeline lancé
  pour écrire cette section : lecture seule des fichiers cités.
