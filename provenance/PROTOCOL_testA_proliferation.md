# PROTOCOLE GELÉ — Test A : série TCGA v4 ordonnée par prolifération (18 nov. 2026)

Go de Zackary : 18 nov. 2026, 15h06 — exécuter les 4 propositions dans l'ordre ;
le test A est le n° 1 (recommandé). Ce protocole est gelé AVANT tout run.
Aucun run sans ce fichier. Aucun paramètre ne change après les runs.

## 0. Question à trancher

La chaîne du 15 nov. (§8.4 / §8.5) — au bout de l'axe KRAS, PGC / DPCR1 /
CLDN18 chutent et MUC16 monte — réapparaît-elle quand les mêmes 178 tumeurs
sont ordonnées par vitesse de division (prolifération) au lieu de KRAS ?
Réponse attendue : OUI ou NON, avec les chiffres vérifiés dans les JSON.
Un négatif est un résultat.

## 1. Données et versions gelées

- Pipeline : `~/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py`,
  SHA-256 attendu `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`
  (vérifié avant tout run ; le fichier n'est JAMAIS modifié).
- Base : mêmes 12 flux v4 que `pdac_tcga_fluxes_v4.csv`
  (SHA-256 `e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0`),
  178 tumeurs TCGA-PAAD, résidus après correction de pureté (v4).
- Matrice source : `data/tcga_paad_rsem.tar.gz`, MD5
  `b09569ce3f4721f514bc137bd109ac0a` (Firehose stddata 2016-01-28, PAAD,
  RSEM genes normalized ; déjà sur le disque, rien de re-téléchargé).
- Construction : `build_fluxes_tcga_v4_prolif.py` (SHA noté en provenance).

## 2. Définition gelée du score de prolifération

Score = médiane des RÉSIDUS (correction pureté v4) de MKI67, TOP2A, PCNA,
CCNB1 — définition (c) du §8.25 (`atr_chek1_retest.py`). Les résidus sont
recalculés depuis la matrice Firehose par la même méthode que
`build_fluxes_tcga_v4.py` (scores acineux / îlots, régression linéaire par
gène sur [1, acineux, îlots], flux = résidus). Le score vit donc dans le
même espace corrigé que les 12 flux : l'ordre ne réintroduit pas la
composante tissu normal que la v4 a retirée.

Sensibilité (rapportée, ne change pas la série) : le même score calculé
sur les valeurs brutes log2(RSEM+1) ; Spearman entre les deux scores et
entre les deux ordres, et recouvrement des 12 premières tumeurs.

## 3. Vérification de reproduction (avant de construire la série)

Le script recalcule les résidus v4 depuis le tarball et compare au CSV v4 :
- même échantillon : 178 tumeurs (codes TCGA 01) ;
- colonne PGC recalculée, triée par résidu KRAS croissant, égale à la
  colonne PGC de `pdac_tcga_fluxes_v4.csv` à atol 1e-9 (même méthode que
  la vérification survie : recompute et compare) ;
- en fait, les 12 colonnes de flux sont comparées, pas seulement PGC.
Si un écart dépasse 1e-9, ARRÊT : rien n'est construit, rien n'est lancé.

Contrôle de cohérence supplémentaire : Spearman score prolifération
(résidus) contre rang KRAS (résidus) — le §8.25 rapporte +0,386 pour le
score (brut et résidu calculés là-bas) ; la valeur recalculée ici est
rapportée telle quelle, sans forcer l'égalité.

## 4. Construction de la série

- Fichier réel : `pdac_tcga_fluxes_v4_prolif.csv`.
  Colonnes : `PROLIF` (1re colonne = contrôle), puis les 12 flux v4 dans
  l'ordre v4 (PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1,
  CEACAM5, CLCA1, MUC16). Lignes triées par PROLIF croissant.
  PROLIF n'est PAS un flux : il n'y a pas de doublon contrôle/flux
  (contrairement aux 96 rotations du §8.32 — défaut explicitement évité).
- Fichier nul : `pdac_tcga_fluxes_v4_prolif_nul.csv`.
  Mêmes lignes permutées, graine 42, générateur frais `rng(42)` —
  même convention que les autres nuls du projet (colonnes de flux
  permutées, colonne de contrôle intacte).
- La cible du pipeline est la 1re colonne après le contrôle (PGC),
  comme pour la série v4 de base (politique fixe du pipeline).

## 5. Runs (2, mode fast, v6.1)

Manifeste `manifest_v61_testa.txt` (2 lignes : réel + nul), lanceur
reprenable existant `run_v61_lot.sh` (saute les sorties déjà complètes :
`master_results.json` présent). Commande par run, identique aux 140 runs
précédents :
`python3 universal_v6.1.0_cohen.py --input <csv> --mode fast --output <dossier>`

Sorties : `results_fast_v61_prolif/` et `results_fast_v61_prolif_nul/`.
Journal : `runs_v61_testa.log` (SHA du pipeline consigné en tête par le
lanceur ; exits consignés).

Lancement résistant aux redémarrages : `systemd-run --unit=v61-testa
--collect --working-directory=<dossier> /bin/bash -c '...'` (jamais nohup
depuis le shell — un nohup meurt avec la session). Surveillance : boucle
de vérification toutes les 15 min qui relance le lanceur tant que les 2
`master_results.json` ne sont pas présents ; elle s'arrête d'elle-même
à 2/2. Ne JAMAIS supprimer le dossier d'un run en cours.

## 6. Lecture (après les 2 runs, rien avant)

Extracteur : copie adaptée de `extract_v61_lot_compare_v2.py` (original
intact), clés vérifiées au §8.32 :
- cascade : `five_threshold_cascade.T_-2 .. T_+2` ;
- MC : `run_pipeline.threshold_metadata.threshold_optimization.best_config`
  (best_score + composantes) ;
- Delta : `reading_synthesis.Delta_tension` ;
- L7a : `prediction_levels.L7a_coherence.{consensus_direction, global_confidence}` ;
- falsification : `holographic_tension_state.falsification_vs_null.delta_vs_null` ;
- bruit et F1/F2 : `noise_diagnostic.json`, `transition_analysis.json`
  (« Tous »), comme au §8.31.

Tests directs (harnais, hors pipeline — même méthode que §8.31/§8.32,
`pistes_v61_flux_reading.py` ou équivalent sur copie) : top-12 (les 12
tumeurs les plus proliférantes) contre reste, flux par flux (d de Cohen,
z global) ; mêmes tests sur le nul ; lecture autour de T_0 (fenêtres ±20)
si un T_0 existe. La chaîne à chercher : PGC / DPCR1 / CLDN18 en chute
(d négatif net, au-dessus du bruit du nul) ET MUC16 en hausse (d positif
net) dans les 12 premières — comme au bout de l'axe KRAS (top-12 KRAS :
PGC −0,89 sd, DPCR1 −0,85 sd, CLDN18 −0,46 sd, MUC16 +0,64 sd, §8.4).

## 7. Critères — aucun seuil de séparation pré-enregistré

Comme pour les §8.31/§8.32 : AUCUN seuil de séparation réel/nul n'est
pré-enregistré. Les écarts MC, Delta, L7a, falsification sont présentés
comme des pistes, jamais comme des preuves. Le verdict OUI/NON sur la
chaîne repose sur les tests directs (top-12 contre reste, réel contre
nul), pas sur un score du pipeline seul. Le pipeline ne sépare pas
réel et nul sur les séries PDAC jusqu'ici (§8.31/§8.32) : si c'est encore
le cas ici, c'est dit tel quel. N'exiger jamais de consensus entre flux
ou contrôles : plusieurs seuils critiques peuvent se succéder en chaîne.

## 8. Livrables

- Ce protocole (gelé avant les runs).
- `build_fluxes_tcga_v4_prolif.py` + `PROVENANCE_testA_proliferation.md`
  (SHA des CSV réel/nul, du script, du pipeline, du tarball).
- `manifest_v61_testa.txt`, `runs_v61_testa.log`, 2 dossiers de résultats.
- Lecture flux par flux (script + table vérifiée).
- §8.34 au livre blanc (avant le §8.5, physiquement à la fin du §8),
  ligne 39 au §7, entrée de journal datée du 18 nov. 2026.
- PDF NON régénéré (instruction explicite).

## 9. Ce qui manque / limites nommées d'avance

- Pas de vrai temps : l'ordre prolifération est un classement, pas une
  horloge — comme l'ordre KRAS (§8.33).
- La prolifération est corrélée à KRAS (+0,386 au §8.25) : les deux axes
  se recouvrent en partie ; un résultat positif ne prouve pas un axe
  indépendant, un résultat négatif ne prouve pas que la prolifération
  est étrangère à la chaîne — il dit seulement que, rangées par
  prolifération, les tumeurs ne montrent pas la même coupure.
- Le score est une médiane de 4 gènes en ARN bulk : il mesure une
  vitesse de division moyenne du tissu, pas celle de chaque cellule.
