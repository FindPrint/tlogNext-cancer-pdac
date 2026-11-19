# PROTOCOLE GELÉ — Test C : série TCGA v4 ordonnée par stade clinique (§8.45)

Date : 19 nov. 2026. Chantier 3 (go parent 19 nov. 2026).
Ce protocole est gelé AVANT toute construction et tout run.
Aucun run sans ce fichier. Aucun paramètre ne change après les résultats.
Livre blanc NON édité, PDF NON régénéré, rien poussé sur GitHub (instruction
explicite). La section §8.45 est écrite dans un FICHIER SÉPARÉ
(`section_8.45_testC_stage.md`).

## 0. Question à trancher

La chaîne du 15 nov. (§8.11) — au bout de l'axe KRAS, PGC / DPCR1 /
CLDN18 chutent et MUC16 monte (top-12 KRAS : PGC −0,89 sd, DPCR1 −0,85 sd,
CLDN18 −0,46 sd, MUC16 +0,64 sd, §8.4) — apparaît-elle quand les mêmes
tumeurs TCGA-PAAD sont ordonnées par stade clinique au lieu de KRAS ?
Réponse attendue : OUI ou NON, avec les chiffres vérifiés dans les JSON.
Un négatif est un résultat. C'est le 4e axe testé après la prolifération
(§8.34 : NON) et la CN MTAP (§8.36 : NON), et après les 48 contrôles
(§8.32 : aucun ne porte la chaîne).

## 1. Données et versions gelées

- Pipeline : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256 attendu `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant tout run ; le fichier n'est JAMAIS modifié).
  Références : v6.1 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`,
  v6 `bb8bbdba…c0773` (revérifiées à la fin du chantier).
- Base : mêmes 12 flux v4 que `pdac_tcga_fluxes_v4.csv`
  (SHA-256 `e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0`),
  178 tumeurs TCGA-PAAD, résidus après correction de pureté (v4).
- Matrice source : `data/tcga_paad_rsem.tar.gz`, MD5
  `b09569ce3f4721f514bc137bd109ac0a` (Firehose stddata 2016-01-28, PAAD,
  RSEM genes normalized ; déjà sur le disque, rien de re-téléchargé).
- Stade clinique : `data_clinical_patient.txt`, colonne
  `AJCC_PATHOLOGIC_TUMOR_STAGE` (7e colonne), fichier clinique TCGA
  PanCanAtlas déjà sur le disque. SHA-256 calculé le 19 nov. 2026 :
  `0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5`
  (premier hachage consigné — voir §9, ce qui manque).
  Effectifs bruts du fichier (184 patients PAAD, 0 doublon d'identifiant) :
  STAGE IIB 121, IIA 30, IB 15, III 5, IV 5, IA 5, I 1, vide 2.
  Le fichier compte 4 lignes d'en-tête descriptives avant la ligne
  d'en-tête `PATIENT_ID…` puis 184 lignes de patients.
- Construction : `build_fluxes_tcga_v4_stage.py` (SHA noté en provenance).

## 2. Définition gelée de l'ordre par stade

- Rang du stade PRINCIPAL : I = 1, II = 2, III = 3, IV = 4.
  Les sous-stades sont repliés sur le stade principal (IA/IB → I,
  IIA/IIB → II). Justifications, fixées avant tout calcul :
  (a) la question posée est l'ordre I < II < III < IV ;
  (b) les sous-stades distinguent des nuances T/N, pas un axe monotone
  de progression au même sens que le stade principal ;
  (c) le patient unique « STAGE I » (sous-stade non précisé) entre
  naturellement dans le stade I sans inventer un sous-rang ;
  (d) le contrôle reste une variable ordinale à 4 niveaux, lisible
  par le pipeline comme un pas (voir §3).
  La distribution des sous-stades dans chaque stade principal est
  rapportée en provenance, à titre descriptif seulement — elle ne
  change pas la série.
- Règle de départage des ex æquo DANS un même stade (gelée avant tout
  calcul) : code-barres échantillon TCGA complet, ordre lexicographique
  croissant (p. ex. TCGA-2J-AAB1-01 < TCGA-2L-AAQA-01). Neutre par
  construction : un identifiant administratif, sans lien avec la biologie,
  fixé avant de voir aucune valeur de flux. NE PAS départager par KRAS
  (ce serait réintroduire l'axe KRAS), ni par aucun flux, ni par la
  survie, ni par l'âge, ni par le sexe.
- Tumeurs SANS stade connu : EXCLUES de la série, sans imputation.
  Le nombre d'exclues et leurs codes-barres sont rapportés en provenance.
  Si la série tombe sous 40 lignes (minimum fast), ARRÊT : aucune série
  n'est construite, aucun run n'est lancé (règle écrite d'avance, comme
  au §8.36 (a)/(b)).
- Jointure : code patient = 12 premiers caractères du code-barres
  échantillon RSEM (code 01, tumeur primaire) vers `PATIENT_ID` du
  fichier clinique. Vérification : le nombre de tumeurs appariées, le
  nombre de patients cliniques sans RSEM, et l'absence de doublon
  d'appariement sont rapportés. Un patient clinique ne peut apparaître
  qu'une fois (0 doublon vérifié dans le fichier clinique).

## 3. Construction de la série

- Fichier réel : `pdac_tcga_fluxes_v4_stage.csv`.
  Colonnes : `STAGE` (1re colonne = contrôle), puis les 12 flux v4 dans
  l'ordre v4 (PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1,
  CEACAM5, CLCA1, MUC16). Lignes triées par (rang de stade, code-barres)
  croissants. STAGE n'est PAS un flux : il n'y a pas de doublon
  contrôle/flux (contrairement aux 96 rotations du §8.32 — défaut
  explicitement évité). STAGE occupe la place du « step » de la v4 :
  1re colonne = contrôle, comme PROLIF au test A (§8.34) et MTAPCN au
  §8.36. La cible du pipeline est la 1re colonne après le contrôle (PGC),
  comme pour les séries v4, prolifération et MTAP (politique fixe).
- Fichier nul : `pdac_tcga_fluxes_v4_stage_nul.csv`.
  Mêmes lignes permutées, graine 42, générateur frais `rng(42)` —
  même convention que les autres nuls du projet (bloc des 12 flux
  permuté par lignes, colonne de contrôle intacte).
- Vérification de reproduction (avant de construire la série, comme aux
  §8.34/§8.36) : le script recalcule les résidus v4 depuis le tarball
  (même méthode que `build_fluxes_tcga_v4.py` : scores acineux / îlots,
  régression linéaire par gène sur [1, acineux, îlots], flux = résidus)
  et compare au CSV v4 : même échantillon (178 tumeurs, codes TCGA 01),
  les 12 colonnes de flux, triées par résidu KRAS croissant, égales à
  atol 1e-9. Si un écart dépasse 1e-9, ARRÊT : rien n'est construit,
  rien n'est lancé.
- Contrôle de cohérence (rapporté, ne change pas la série) : Spearman
  rang de stade contre rang KRAS (résidus) ; effectifs par stade dans
  la série ; composition exacte des 12 dernières lignes (les plus haut
  stade) ; recouvrement top-12 stade/KRAS.

## 4. Runs (2, mode fast, v6.2)

Manifeste `manifest_v62_stage.txt` (2 lignes : réel + nul), lanceur
reprenable existant `run_v62_lot.sh` (saute les sorties déjà complètes :
`master_results.json` présent). Commande par run, identique aux runs
précédents :
`python3 universal_v6.2.0_cohen.py --input <csv> --mode fast --output <dossier>`

Sorties : `results_fast_v62_stage/` et `results_fast_v62_stage_nul/`.
Journal : `runs_v62_stage.log` (SHA du pipeline consigné en tête par le
lanceur ; exits consignés).

Lancement résistant aux redémarrages : `systemd-run --unit=v62-stage
--collect --working-directory=<dossier> /bin/bash -c '...'` (jamais nohup
depuis le shell — un nohup meurt avec la session). Surveillance : boucle
de vérification qui relance le lanceur tant que les 2
`master_results.json` ne sont pas présents ; elle s'arrête d'elle-même
à 2/2. Ne JAMAIS supprimer le dossier d'un run en cours.

## 5. Lecture (après les 2 runs, rien avant)

Extracteur : copie adaptée de `extract_ssep_838.py` (original intact),
clés vérifiées au §8.38 :
- cascade : `five_threshold_cascade.T_-2 .. T_+2` ;
- MC : `run_pipeline.threshold_metadata.threshold_optimization.best_config`
  (`score` + `threshold` ; `metrics.max_separation`, `metrics.stability`,
  S_sep = max_separation × stability, formule gelée PROTOCOL_v6.2 §3) ;
- Delta : `reading_synthesis.Delta_tension` ;
- L7a : `prediction_levels.L7a_coherence.{consensus_direction, global_confidence}` ;
- falsification : `holographic_tension_state.falsification_vs_null.delta_vs_null` ;
- bruit et F1/F2 : `noise_diagnostic.json`, `transition_analysis.json`
  (« Tous »), comme au §8.31/§8.36.

Tests directs (harnais, hors pipeline — même méthode que §8.34/§8.36,
script neuf `stage_reading.py` sur copie, originaux intacts) :
- (D1) top-12 contre reste, flux par flux (d de Cohen, + = plus haut
  chez les 12 dernières lignes = les plus haut stade) ; mêmes tests
  sur le nul (mêmes indices de lignes). C'est le test de la chaîne,
  dans les mêmes unités que §8.4/§8.34/§8.36. Composition des 12
  dernières lignes rapportée exactement (mélange attendu : stade IV
  ~5 + stade III ~5 + 2 IIB au plus grand code-barres — à confirmer
  par le calcul, pas deviné).
- (D2) contrastes par groupes : stade IV contre stade I ; stades
  III+IV contre stades I+II (d de Cohen + Mann-Whitney bilatéral, p).
  Limite nommée d'avance : effectifs minuscules au sommet (III ~5,
  IV ~5) — les p sont indicatives, les d sont lus contre le nul.
- (D3) tendance ordinale : Spearman rho de chaque flux contre le rang
  de stade (1–4) sur la série réelle ; mêmes rho sur le nul (attendu
  |rho| ≤ ~0,10 comme au §8.36). Un rho sans saut aux extrêmes = pente
  graduelle, pas rupture (leçon §8.34/§8.36).
- (D4) autour de T_0 si un T_0 existe (fenêtres ±20 lignes) : d par
  flux, réel contre nul. Si la cascade est dégénérée ou sans T_0
  lisible, le dire au lieu de forcer la lecture.
- Signature cherchée (référence §8.4) : PGC −0,89, DPCR1 −0,85,
  CLDN18 −0,46, MUC16 +0,64. La chaîne « apparaît » si, dans les
  tests directs, PGC / DPCR1 / CLDN18 chutent ET MUC16 monte au bout
  de l'axe stade, au-delà du bruit du nul.

## 6. Critères — écrits avant les runs

- Aucun seuil de séparation réel/nul n'est pré-enregistré pour MC,
  Delta, L7a, falsification : les écarts sont présentés comme des
  pistes, jamais comme des preuves (convention §8.31/§8.32/§8.34/§8.36).
- Gigue mesurée v6.2 = 0,00 (§8.37 : hachage stable, gigue L5 = 0 sur
  20/20 runs) : tout écart réel − nul non nul est au-delà de la gigue
  instrumentale — ce qui ne suffit pas à en faire une séparation
  démontrée, seulement un écart mesuré au-delà du bruit de l'instrument.
- Le verdict OUI/NON sur la chaîne repose sur les tests directs
  (D1–D4, réel contre nul), pas sur un score du pipeline seul.
  Le pipeline ne sépare pas réel et nul sur les séries PDAC jusqu'ici
  (§8.31/§8.32/§8.34/§8.36) : si c'est encore le cas ici, c'est dit
  tel quel. N'exiger jamais de consensus entre flux ou contrôles :
  plusieurs seuils critiques peuvent se succéder en chaîne.

## 7. Livrables

- Ce protocole (gelé avant les runs).
- `build_fluxes_tcga_v4_stage.py` + `PROVENANCE_testC_stage.md`
  (SHA des CSV réel/nul, du script, du pipeline, du tarball, du
  fichier clinique ; effectifs par stade ; exclues ; jointure).
- `manifest_v62_stage.txt`, `runs_v62_stage.log`, 2 dossiers de résultats.
- Lecture flux par flux (`stage_reading.py` + table vérifiée
  `stage_direct_tests.csv` + `stage_extract.json`).
- §8.45 dans le FICHIER SÉPARÉ `section_8.45_testC_stage.md`
  (le livre blanc n'est PAS édité).
- PDF NON régénéré. Rien poussé sur GitHub.

## 8. Réserve de méthode — nommée d'avance, à reprendre dans §8.45

Le stade est une variable clinique, pas une mesure du système : c'est
un résumé, au moment du diagnostic, de l'extension anatomique de la
maladie (taille, ganglions, métastases, classification AJCC 7e édition
dans ce fichier), décidé par des humains à partir d'examens — pas une
grandeur physique du tissu tumoral, pas un temps, pas un dosage.
La question devient donc « le pipeline voit-il la progression
clinique ? », différente de l'axe KRAS (qui ordonne les tumeurs par
l'activité d'un gène mesurée dans le tissu). Un éventuel signal sous
l'ordre stade ne doit PAS être présenté comme une rupture du système
sans cette réserve ; un négatif ne dit pas que le stade est étranger
à la biologie, seulement que, rangées par stade, les tumeurs ne
montrent pas la même coupure qu'au bout de l'axe KRAS.
Limites supplémentaires nommées d'avance : 4 niveaux seulement, avec
des ties massives (IIB ~121/178) — l'ordre DANS un stade est arbitraire
(code-barres), donc tout « seuil » à l'intérieur du stade II est sans
sens ; le sommet de l'axe est mince (III + IV ~10 tumeurs) ; le stade
mélange extension locale, atteinte ganglionnaire et métastases en une
seule étiquette ordinale ; pas de vrai temps, pas de suivi longitudinal.

## 9. Ce qui manque / limites nommées d'avance

- Provenance d'acquisition du fichier clinique : le fichier
  `data_clinical_patient.txt` était déjà sur le disque au début du
  chantier (modifié le 15 nov. 2026, 15h13 UTC) ; AUCUNE entrée ne
  documente son téléchargement (ni `fetch_tcga.log`, ni
  `download_firehose.log`, ni `PROVENANCE_tcga*.md` ne le mentionnent)
  et AUCUN hachage n'était consigné avant ce chantier. Le SHA-256
  calculé ici est le premier. Le contenu est vérifiable en lui-même
  (en-tête TCGA PanCanAtlas, 184 patients PAAD, stades AJCC), mais
  l'URL et la date d'acquisition exactes ne sont PAS connues — c'est
  nommé, pas comblé. Rien n'a été re-téléchargé pour ce chantier.
- Édition AJCC : 7e édition dans ce fichier (colonne
  `AJCC_STAGING_EDITION`) — un re-stadage en 8e édition pourrait
  déplacer quelques tumeurs ; non fait ici (données non détenues).
- Pas de données single-cell, spatiales, ni longitudinales (déjà nommé
  au §8.33) ; pas de stade moléculaire ; le stade ne mesure pas la
  vitesse de division (§8.34) ni la perte de MTAP (§8.36).
