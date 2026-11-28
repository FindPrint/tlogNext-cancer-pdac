# PROVENANCE §8.102 — Chasse à la 17e paire (27 novembre 2026)

Provenance nommée partout, comme exigé par la règle permanente
du 27 octobre 2026 : source complète, nature des lignes, comment
chaque valeur a été produite, hachages, ce qui manque.

## 1. Chantier et décision

- **Chantier :** C « §8.102 — chasse à la 17e paire », projet PDAC,
  27 novembre 2026. Agent du chantier : sous-agent (profondeur 2).
- **Décision :** deux candidates gelées successivement.
  (1) GSE55643, protocole gelé 27 nov. 2026 14h41 UTC, ÉCARTÉE
  (cas complets 24/45 < 40, porte 4 — valeurs manquantes,
  aucune imputation) : aucun CSV, aucun run.
  (2) GSE313117 bras whole-transcriptome, protocole opératif gelé
  27 nov. 2026 14h47 UTC, RETENUE : 11 runs v6.2, verdict
  FRAGILE à 10 nuls.
- **Aucune association** (corrélation KRAS–flux, `maxsep`) n'a été
  lue pour aucune candidate avant le gel de son protocole.

## 2. Sources des données

### 2.1 GSE313117 (paire retenue, 17e paire principale)

- **Source :** NCBI GEO, série GSE313117, « Cross-platform
  comparison of gene expression-based cancer molecular subtyping
  reveals discrepancies with exome capture methods ».
- **Auteur / dépôt :** essai PANCREAS (NCT04683315, Medical
  College of Wisconsin, phase 2, à partir de 2021) ; série
  soumise à GEO (GSM9361352… ; 158 échantillons).
- **Date :** série consultée et téléchargée le 27 nov. 2026.
- **URL série :**
  `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE313117`
- **Fichier utilisé :** supplément officiel whole-transcriptome
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE313nnn/GSE313117/suppl/GSE313117_tpm_whole_transcriptome.csv.gz`
  — 6 480 071 octets, SHA-256
  `28c946c4bfdf3fc23cd2fc787d3eb15d45e5bf093078e49cfd0171351d1a15b6`
  (copie d'enquête `/tmp` et téléchargement officiel dans
  `data/` : SHA identiques, vérifiés).
- **Contenu :** 24 416 gènes × 79 échantillons, TPM, symboles de
  gènes en lignes, valeurs min 0,000 / médiane 2,384 / max
  327 434,895, 0 NaN. 79 patients PDAC, 1 mesure
  whole-transcriptome par patient ; le bras exome-capture
  (mêmes tumeurs) est exclu. Plateformes GPL24676 / GPL18573
  (Illumina NextSeq 500).
- **Fichier clinique déposé** consulté pour sa structure
  uniquement (aucune valeur clinique utilisée) :
  `GSE313117_deidentified_clinical_data_final.csv.gz` (1 801 o).
- **Fichier exome-capture** (non utilisé, mêmes patients) :
  `GSE313117_tpm_exome_capture.csv.gz` (non téléchargé ; seule
  l'existence est consignée).
- **Nature des lignes :** chaque ligne du CSV réel est un patient
  PDAC de l'essai PANCREAS (1 mesure whole-transcriptome) ;
  chaque colonne de flux est une mesure instrumentale
  d'expression (RNA-seq, TPM déposées) ; `step` est un rang
  humain (0..78, ordre KRAS ascendant), pas une mesure ;
  MUCL3 est la mesure du gène historiquement nommé DPCR1
  (remappage vérifié, §4). Aucune valeur inventée, imputée
  ou mise à l'échelle.

### 2.2 GSE55643 (première candidate, écartée)

- **Source :** NCBI GEO, série GSE55643, « Gene expression in
  pancreatic ductal adenocarcinoma », Jamieson et coll.,
  Université de Glasgow (Royaume-Uni), PMID 25415223,
  BioProject PRJNA240283, soumise 2014-03-06, publique
  2014-03-14.
- **URL série :**
  `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE55643`
- **Fichier :** matrice série
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE55nnn/GSE55643/matrix/GSE55643_series_matrix.txt.gz`
  — 10 731 208 octets, SHA-256
  `96409670e6fbd0fe8bde0683eda4197c54f6bd402827f1c2b295d254c39e08ec`
  (copie d'enquête et téléchargement officiel : SHA identiques).
  41 093 sondes × 53 échantillons, valeurs min 0,81 /
  médiane 8,16 / max 20,64, 290 614 NaN.
- **Annotation :** `GPL6480.annot.gz` (annotation officielle GEO)
  — 7 380 104 octets, SHA-256
  `aacec81b2d95f183f0827b43e769388a92917811b81920c13ecc8fe148c5a3ab`
  ; mapping écrit `GPL6480_probe2symbol.tsv`, SHA-256
  `b44374e8a41c7c6e0e969a12aa8fa791c00b4c5958454141b5b9b75280a4bce4`
  (30 679 sondes, symbole unique ; 44 symboles multi-gènes exclus).
- **Échec vérifié :** 45 tumeurs retenues, 12/12 gènes v4 exacts
  présents (DPCR1 exact, 2 sondes), KRAS présent — mais cas
  complets **24/45** (NaN : KRT20 13/45, CLCA1 11/45, CEACAM5 3,
  MUC16 3, REG4 1, CLDN18 1 ; 21 tumeurs avec ≥ 1 NaN). Porte 4
  ÉCHEC → arrêt, aucun CSV, aucun run. Constructeur
  `build_fluxes_8102.py`, SHA-256
  `ce6b6d6e08f7e813c4b5ee14658e77b7d409e4dd737635ac1b117f0d8b2590ea`.

### 2.3 Autres candidates examinées (portes seulement, §8.102.1)

- **E-utilities, 27 nov. 2026 :** (a) « pancreatic ductal
  adenocarcinoma, expression profiling by array, Homo sapiens »
  (49 séries) ; (b) « … expression profiling by high throughput
  sequencing, Homo sapiens » (181 séries, 100 retournées).
- **GSE50827** (ICGC PACA-AU, recouvrement — titre « ICGC
  Pancreas », échantillons GEO-PC) ; **GSE98399, GSE89792,
  GSE157494** (PDX/xénogreffes) ; **GSE130563** (muscle
  squelettique) ; **GSE26089** (xénogreffes/lignées) ;
  **GSE212575** (matrice 55 977 o = en-tête seule) ;
  **GSE313657** (spatial GeoMx, feuille « HeatMap », ROI) ;
  **GSE278670** (spatial IPMN) ; **GSE296831 / GSE285406 /
  GSE303964 / GSE276223 / GSE248585 / GSE347008** (lignées
  in vitro) ; **GSE314073 / GSE239309** (lignées isogéniques
  KRAS). Fichiers d'enquête en `/tmp` (matrices, résumés,
  suppléments) : copies de vérification de portes, supprimables,
  jamais utilisées pour construire un flux ni lancer un run.
- **Recherche web :** essai PANCREAS NCT04683315
  (ClinicalTrials.gov, sponsor Medical College of Wisconsin)
  pour l'indépendance de GSE313117 ; article PMC11665842
  (table des cohortes PDAC) pour le dépistage initial.

## 3. Remappage DPCR1 → MUCL3 (re-vérifié en direct)

- **HGNC REST, 27 nov. 2026 14h45 UTC :**
  `https://rest.genenames.org/fetch/symbol/MUCL3` → MUCL3,
  HGNC:21666, « mucin like 3 », Approved, prev_symbol
  ['DPCR1'], date_symbol_changed 2018-03-19, ensembl
  ENSG00000168631, entrez 135656.
  `https://rest.genenames.org/fetch/prev_symbol/DPCR1` →
  numFound = 1, même enregistrement (HGNC:21666, MUCL3).
- **Données :** MUCL3 = 1 ligne TPM dans GSE313117 ; DPCR1 =
  0 ligne. (Dans GSE55643 : DPCR1 exact, 2 sondes, aucun
  remappage nécessaire — sans objet pour la paire retenue.)
- Référence antérieure : §8.85 (première vérification 5/5),
  §8.99 (R1–R5). Le présent remappage est une re-vérification
  en direct, pas une reprise aveugle.

## 4. Code et exécution (hachages)

- **Pipeline :** `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant le lot 14:47:10 UTC, après le lot 15:46:18 UTC,
  avant l'extraction ; inchangé 3/3 ; jamais modifié).
- **Constructeur de nuls :**
  `~/workspace/runs/pdac-v6/nulls_lot_next/scripts/build_null_893.py`,
  SHA-256
  `572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467`.
- **Constructeur de flux GSE313117 :**
  `build_fluxes_8102_gse313117.py`, SHA-256
  `1d94cf39215375760ee9e2cc6e7401bc08fb9ca9372445110c9d1924ea6e5e62`.
- **Constructeur de flux GSE55643 (échec) :**
  `build_fluxes_8102.py`, SHA-256
  `ce6b6d6e08f7e813c4b5ee14658e77b7d409e4dd737635ac1b117f0d8b2590ea`.
- **Lanceur :** `run_8102.sh`, SHA-256
  `a75bbe5bdc4df55e36f5ed813479d007517421b425a134e20be06a87c00951a9` ;
  journal `runs_8102.log`, SHA-256
  `54eb9dde7e2ca394016e29471139a2ecedadd166d838cae606076e869dc6537f` ;
  unité systemd `v62-8102-gse313117`, 27 nov. 2026 14:47:10 →
  15:46:18 UTC ; **redémarrage machine 15:04:38 UTC** (unité
  transiente tuée en cours du nul s9512, relance 15:05:30,
  reprise au nul s9512, réel et s9511 sautés comme déjà
  complets) ; **11/11 exit 0**.
- **Extraction :** `extract_8102.py`, SHA-256
  `bbba0e4451d2d5ede3ac41d000bb78becf8ff99f688ebdd903f5b68dc643bf05` ;
  `extraction_8102.json`, SHA-256
  `79c6c3063584d529bf40903c12ddbf7253331300afb8b20f11e8f84da3a9b0a0`
  (vérification croisée `best_config` vs `raw_best_config` :
  11/11 à 0,0 exact).
- **Protocoles :** `PROTOCOL_8102_gse55643.md`, SHA-256
  `87a5d030e9670751499e75609deefb7c4e3b02d6922b3a65be7986e1da08d20b`
  (gelé 14h41 UTC, inchangé) ; `PROTOCOL_8102_gse313117.md`,
  SHA-256
  `1babc13bb46f1469852629e52b8c7f6dcc9cd9880b1890dfdc13587075d89285`
  (gelé 14h47 UTC).
- **Section :** `section_8.102_gse313117.md`, SHA-256
  `dec756cccfa0913db22b8fa4f631706c2a4366f16ee9c39c07a927b964b1be52`.

## 5. Données produites (hachages)

- **CSV réel :** `pdac_8102_gse313117_fluxes.csv`, SHA-256
  `6b83243f7ddf26ec2b206373b4f0afaa3808572e336079b4f0ceb0ea999224b7`
  (79 lignes × 13 colonnes : `step` + 12 flux ; ordre KRAS
  ascendant ; KRAS TPM min 1,331 / médiane 13,365 / max 23,211).
- **CSV nuls (graines 9511–9520) :**
  - s9511 `d254d0c906f3a37adaa15cfae3e29069c12727c61651b64b7d8bfab96652be3d`
  - s9512 `3270cf1311a9cb54de136653ea5733553738ac17e02b4d43c5cc3d03e7e228ef`
  - s9513 `9858f25cd334d69b7147af6429f76fb809c78de54f5e9499c2438d6752867aea`
  - s9514 `c710e36510cd792254ad4a960c7739fb7a73d3f69ecf1fb2dc12acf7192a02c9`
  - s9515 `1bc4d512f04a4c17963aba1b73597c11c50c36d9f65aeed739d01a374d0e8aae`
  - s9516 `23a36bf150a8dccdd5a499d04f2da5eef4e412e8826d9889d0e947a1d3e0e2d7`
  - s9517 `e5cb83b2884b471e20493dd1e74aafa606ed0780acfe651be2cb545dc6917491`
  - s9518 `cad044706672cc67abc6db0b9f585a9adaa2e3f675e741f98209163e3d10a262`
  - s9519 `a26458250f69fd10dc970d438fcbe682ad467a9630b932f973f54397080a5a04`
  - s9520 `7ab1bc2db50737ddf3f5961d8e3006ebb9c8aa29968dd57e356d380e6da86be0`
- **Runs :** `results_fast_v62_8102_gse313117` et
  `results_fast_v62_8102_gse313117_nul_s9511` … `s9520`
  (11 `master_results.json` présents).

## 6. Résultat (analyse uniquement, jamais de prédiction)

- **Verdict §8.102 : FRAGILE** (règle gelée §8.93 §4, plancher
  0,07). `maxsep` réel 0,4261 ; nuls : médiane 0,2536, p95
  0,3614, min 0,1749, max 0,4056 ; écarts réel−nul : 9/10 >
  0,07 (90,0 %), min +0,0205 (nul s9518) ; d contre médiane
  +0,1725 ; d contre p95 +0,0647 ; rang 11/11. MC réel 0,3637
  (médiane des nuls 0,3398, p95 0,3856 — secondaire, ne décide
  pas). Spearman vs KRAS : Δρ médian +0,3070, 11/12 flux
  positifs (détail en §8.102.5). Aucune affirmation clinique.
- **A2 / LOO :** non mis à jour dans ce chantier (registre du
  coordinateur ; A2 défini contre le nul graine 42, non couru
  ici). Pour le coordinateur : 17e paire, FRAGILE à 10 nuls ;
  A2 classique 11/16 avant ce lot.

## 7. Ce qui manque

- Consolidation à 200 nuls (suite à faire, décisive ici : un
  seul nul haut, s9518, sépare FRAGILE de SOLIDE).
- Scores compagnons : Delta, L7a, falsification, F1/F2 après
  seuil (non extraits, hors règle gelée §8.93 §4).
- Mise à jour du registre A2/LOO (coordinateur).
- Fichiers bruts RNA-seq GSE313117 (non déposés par les auteurs :
  données personnelles identifiables).
- Une candidate supplémentaire au-delà de GSE313117 n'a pas été
  cherchée après la retenue (arrêt borné : une seule paire par
  chantier, comme au §8.99).

## 8. Ce qui n'a pas été fait

- Aucune modification du livre blanc, aucun PDF, aucune Release,
  aucun push GitHub ; `tlogNext-pdac-phase2` et
  `universal-log-research` non touchés ; Kaggle non touché ;
  pipeline jamais modifié ; aucune fusion.
- Aucun verdict importé d'un autre dépôt ou d'un autre article :
  le verdict FRAGILE vient des 11 runs propres de ce chantier.
- Aucune lecture d'association avant les gels de protocoles ;
  les appels PurIST, sous-types et survie de GSE313117 n'ont
  jamais été lus ni utilisés.
