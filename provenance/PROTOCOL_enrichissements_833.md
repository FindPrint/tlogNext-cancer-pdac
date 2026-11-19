# PROTOCOLE GELÉ — Étape 4 : enrichissements du §8.33 (18 nov. 2026)

Go de Zackary : 18 nov. 2026, 15h06 — exécuter les 4 propositions dans
l'ordre ; l'étape 4 est la dernière (test A §8.34, Phase 2 §8.35 et PDF
457 pages terminés ; les poussées GitHub de l'étape 3 sont préparées mais
non poussées, approbation expirée — hors de cette étape, retentées à la
publication finale). Ce protocole est gelé AVANT tout run et tout test
direct de l'étape 4. Aucun paramètre ne change après les résultats.
Ne pas régénérer le PDF (publication finale).

Pipeline : `~/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py`,
SHA-256 attendu `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié).
Mode fast partout. Nul permuté graine 42, contrôle intact (même convention
que les 140 runs et le test A). Aucun seuil de séparation pré-enregistré :
les écarts réel/nul sont des pistes, jamais des preuves. Aucun consensus
exigé entre flux ou contrôles. Un négatif est un résultat.

## 0. Questions à trancher (une par sous-étape)

(a) Allèle KRAS : le §8.33 dit qu'il y a trop peu de lignées par allèle
pour une série v6.1 (G12D 23, G12V 20, G12R 5…). Vérifier sur les données
(`data/kras_alleles_pancreas.csv`, 54 lignées, et le MAF DepMap via la
table du 18 nov.). Règle écrite d'avance : si n < 40 pour chaque allèle,
la série v6.1 est IMPOSSIBLE (minimum fast 40) — tests directs seulement
(la dépendance KRAS/PRMT5 ou la viabilité MRTX1133 change-t-elle par
allèle ? en s'appuyant sur les données existantes §8.20, recalculées
aujourd'hui, jamais importées comme verdicts). Si un allèle atteint
n ≥ 40, construire la série et la lancer (réel + nul graine 42).

(b) Jointure MAF TP53/SMAD4/CDKN2A : le fichier MAF DepMap est sur le
disque (`data/OmicsSomaticMutationsMAFProfile.maf`) ; le §8.33 dit que
la jointure PR→ACH manque et que le « 0 mutation » brut est un artefact
de jointure absente. En fait la jointure a été construite le 18 nov.
(`build_mutation_table_pancreas.py`, table `data/mutation_table_pancreas.csv`,
45 lignées) : la revérifier en relançant le constructeur et en comparant
le SHA de sortie (`f3fa2bd2ddafdec83795211cd45de19ce88de674a2d660f47a5e72d813063f36`).
Tests directs ensuite : la dépendance Chronos à KRAS ou à PRMT5 (et ATR,
contrôle §8.25) change-t-elle selon la mutation TP53 (38/7), SMAD4 (11/34)
ou CDKN2A (12/33) ? Mann-Whitney bilatéral + d de Cohen + médianes, mêmes
conventions que §8.28/§8.29. Confondant MTAP vérifié pour PRMT5 (CN MTAP
par lignée, `data/OmicsCNGene.csv`) : si un groupe mutationnel diffère en
CN MTAP, le dire et tester si l'effet survit à la stratification MTAP.
Série v6.1 ? Règles écrites d'avance : deux séries muté/non-muté exigent
n ≥ 40 chacune — impossible ici (plus grand groupe 38). Ordonner les 45
lignées par statut binaire (0/1) : DÉGÉNÉRÉ — le seuil serait forcé à la
frontière des groupes par construction, pas découvert — donc NON lancé,
avec la preuve des effectifs. Si une autre stratification atteint
n ≥ 40 des deux côtés, elle serait lancée (réel + nul) ; sinon, dire
pourquoi avec la preuve.

(c) Série ordonnée par CN MTAP (TCGA v4, n=178) : mêmes 12 flux v4
(`pdac_tcga_fluxes_v4.csv`, SHA `e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0`),
ordre = CN MTAP croissant (perte profonde d'abord). Contrôle = valeur
continue GISTIC `all_data_by_genes.txt` (log2 ratio, `data/tcga_paad_gistic.tar.gz`,
MD5 `816034f7…` — revérifié avant usage), pas le seuillé (−2…+2, trop de
ties : 46/66/69/2/1 sur 184 échantillons). Le seuillé est rapporté comme
contrôle de cohérence seulement. Jointure sur les 15 premiers caractères
du code-barres TCGA (patient) entre GISTIC et les colonnes RSEM ; n
apparié rapporté — si < 178, la série utilise les tumeurs appariées
seulement et le dit. Vérification de reproduction AVANT construction
(même méthode que le test A) : les 12 flux v4 recalculés depuis
`data/tcga_paad_rsem.tar.gz` (MD5 `b09569ce…ac0a`) reproduisent le CSV v4
à atol 1e-9, sinon ARRÊT. 2 runs fast v6.1 (réel + nul graine 42).
Tests directs : top-12 (les 12 tumeurs les plus délétées en MTAP) contre
reste, flux par flux (d de Cohen, mêmes unités que §8.4/§8.34), plus
Spearman de chaque flux contre CN MTAP sur les 178. Question : la chaîne
(bloc qui chute + MUC16 qui monte) ou un autre signal apparaît-il quand
on ordonne par perte de MTAP ? Critère écrit avant : séparation réel/nul
sur position du seuil ET sens L7a, comme en v4 (§8.4) — sinon, négatif.

## 1. Lancement (machine qui redémarre souvent)

Lanceur reprenable existant `run_v61_lot.sh` (saute les sorties complètes :
`master_results.json` présent). Manifeste `manifest_v61_mtap.txt`.
Surveillance `watch_v61_mtap.sh` (boucle 15 min, max 48 tours, s'arrête
à 2/2), lancée par `systemd-run --unit=watch-v61-mtap --collect`
(jamais nohup), doublée d'un cron toutes les 15 min comme filet (même
montage que le test A : cron supprimé après 2/2). Ne jamais supprimer le
dossier d'un run en cours.

## 2. Sorties attendues

- `verify_alleles_mutations.py` + `verify_alleles_mutations.txt` :
  (a) comptages allèles sur les 2 sources, (b) revérification de la table
  de mutations, tests directs allèles et statuts mutationnels, MRTX1133
  par allèle recalculé.
- `build_fluxes_tcga_v4_mtap.py` + `pdac_tcga_fluxes_v4_mtap.csv` (réel)
  et `pdac_tcga_fluxes_v4_mtap_nul.csv` (nul graine 42).
- `results_fast_v61_mtap/` et `results_fast_v61_mtap_nul/`
  (master_results.json chacun), journal `runs_v61_mtap.log`.
- Lecture : `mtap_reading.py` + `mtap_direct_tests.csv` + `mtap_extract.json`.
- Livre blanc : §8.36 (avant le §8.5, physiquement à la fin du §8),
  lignes du §7, entrée de journal datée du 18 nov. — provenance et SHA
  de chaque script et fichier.
