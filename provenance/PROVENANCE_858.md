# PROVENANCE §8.58 — Bloc estomac / mucus : nouveaux flux inattendus

Date : 19–20 nov. 2026. Protocole gelé :
`PROTOCOL_stomach_mucus_flux_858.md`,
SHA-256 `3a0762ef5e57b3d6c2b1f81c0672c8ceb5158aeafe526f8f3019f32bb4117935`.

## Pipeline (jamais modifié)

- Travail : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant le lot ; revérifié à la fin du chantier).
- Références : v6.1 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`,
  v6 `bb8bbdba4eb1f8c5…` (16 premiers caractères `bb8bbdba4eb1f8c5`).

## Données sources (rien de re-téléchargé)

- TCGA-PAAD : `data/tcga_paad_rsem.tar.gz`, MD5
  `b09569ce3f4721f514bc137bd109ac0a` (Firehose stddata 2016-01-28, RSEM
  genes normalized ; 178 tumeurs code 01 ; 20 502 gènes en cas complets).
- Clinique TCGA : `data_clinical_patient.txt`, SHA-256
  `0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5`
  (premier hachage consigné au §8.45 ; acquisition non documentée, voir
  protocole §9). Effectifs : 184 patients, STAGE IIB 121, IIA 30, IB 15,
  III 5, IV 5, IA 5, I 1, vide 2.
- GSE71729 : `data/GSE71729_series_matrix.txt.gz` (GPL20769, ID_REF déjà
  des symboles, 19 749 lignes ; matrice complète : 357 échantillons —
  les 145 tumeurs PDAC du projet sont un sous-ensemble ; l'inventaire
  porte sur l'univers des symboles, pas sur la sélection d'échantillons).
- GSE62452 : `data/GSE62452_series_matrix.txt.gz` (GPL6244, ID_REF
  numériques, mapping `data/GPL6244_probe2symbol.tsv`, 25 293 sondes
  avec symbole ; matrice complète : 130 échantillons — les 69 tumeurs
  du projet sont un sous-ensemble).
- ICGC PACA-AU : `data/icgc_pacaau_exp.txt.gz` + probemap
  `data/icgc_pacaau_probemap.gz` (Ensembl → symbole, médiane par
  symbole ; 18 247 symboles ; 96 échantillons → 70 tumeurs primaires
  PDAC dans le projet).
- CPTAC UMich : `data/cptac/pdac_umich_protein_gene_matrix.csv`
  (11 419 gènes-protéines x 68 tumeurs, abondance protéique log2).
- CPTAC BCM : `data/cptac/bcm-pdac-proteomics-…-Tumor.txt.gz`
  (11 403 gènes-protéines mappés ENSG → symbole via le rapport UMich,
  11 418 ENSG → symbole ; 1 ligne non mappée : ENSG00000143420.19,
  hors cibles — même méthode que `build_fluxes_cptac_bcm.py`).
- DepMap CRISPR : `data/CRISPRGeneEffect.csv` (17 916 gènes,
  dépendance CRISPR, PAS de l'expression ; 45 lignées pancréas
  dans le flux DepMap du projet).

## Scripts du chantier (SHA-256)

- `inventory_858.py` :
  `5105603f9c1a34178af665e8bb8221bbc2c0cde11d1a4970454f9b06806988cd`
- `build_fluxes_858_tcga.py` :
  `e861cbd392803f5f3c9ccb6a7b062daf39739d267fb8ed5b4a7f95f8ff222d25`
- `reading_858.py` :
  `949eb28d9a4a4054ec46f3088b65a76576b6a11e1a70dd293f90f02f15048ff7`
- `watch_v62_858.sh` :
  `fded58728c7f1a7e7f31b614ee7c4a4ab592a1bb92eb5db8174ed59a0245c0a8`
- `manifest_v62_858.txt` :
  `b49d4581d59950da5b4b69682ac429665146405bd04914753960b5f720f81340`

## Inventaire

- `inventory_858.csv`, SHA
  `808de0169ce0c826a7d5d429753963c01750e2f82e520172eb53ef8dd9fa3ae9`
  (présent/absent par gène candidat et par matrice).
- `or_scan_858.csv`, SHA
  `5e90a9e43cd134f953a457a5dada45e3f74b7b79ee2539a64ca40ee1d8d3db73`
  (tous les symboles `^OR[0-9]+[A-Z]?[0-9]*$` par matrice + médiane
  log2(RSEM+1) et fraction de tumeurs RSEM>0 dans TCGA).
- Résumé lisible : `inventory_858_summary.txt` (+ `inventory_858_run2.log`).
- Correction en cours de chantier : la première passe donnait
  CPTAC_BCM 0/36 partout — bug de mapping (mauvais champ du rapport
  UMich, `parts[-2]` des champs tabulés au lieu des champs `|` de
  l'Index). Corrigé en reprenant exactement la méthode de
  `build_fluxes_cptac_bcm.py` ; deuxième passe : BCM 11 403 symboles,
  cohérent avec UMich (11 419). Les chiffres du premier passage pour
  BCM sont jetés, pas rapportés.

## Construction des flux TCGA

- Méthode v4 exacte (log2(RSEM+1), scores acineux/îlots, régression
  par gène, flux = résidu). Vérification de reproduction du CSV v4
  (`pdac_tcga_fluxes_v4.csv`, SHA `e7a2adab…a0b0`) : écart max
  1,776e-15 (atol 1e-9) — PASSÉE avant toute construction.
- Stade : mêmes 3 tumeurs exclues qu'au §8.45
  (TCGA-3A-A9I5-01, TCGA-3A-A9IO-01, TCGA-IB-7654-01) ; série stade :
  175 lignes (I 21, II 146, III 4, IV 4) ; série KRAS : 178 lignes.
- Groupes construits (flux retenus = présents TCGA, plafond 20 par
  variance des résidus, règle gelée) :
  - G1 : 33 présents (absents : MUC3A, MUC5AC, MUC19), 20 retenus :
    TFF1, TFF2, MUC6, MUC5B, MUC4, AQP5, REG1A, TFF3, GKN1, PGA3,
    REG3A, MUC21, PGA4, GKN2, AGR2, GAST, SPDEF, FCGBP, MUC13, REG1B.
  - G2 : 24 présents (absents : AMY1B, AMY1C, PRSS2, ELA2A, ELA3A,
    ELA3B), 20 retenus : PRSS1, PRSS3, AMY1A, PNLIPRP2, AMY2B, AMY2A,
    CPB2, CELA2A, CPA3, CELA2B, PNLIP, PLA2G1B, CEL, CPB1, PNLIPRP1,
    CLPS, CPA2, CTRB2, CTRB1, CELA3B.
  - G3 : 356 OR présents dans TCGA (355 par regex + OR2AT4 par la
    liste fermée), 20 retenus : OR7D2, OR13A1, OR2A4, OR52N4, OR2B6,
    OR51E2, OR51E1, OR2A7, OR52N2, OR2L13, OR1J2, OR2W3, OR10H1,
    OR2A1, OR4C6, OR7A5, OR3A2, OR5K2, OR2T10, OR2C1.
  - G4 : 63 présents (absents : TAS2R44, TAS2R45), 20 retenus :
    UGT1A1, ALDH3A1, CYP2C9, CYP3A4, ADH1B, UGT2B7, ADH4, ADH1C,
    ADH6, ADH1A, AOX1, FMO1, CYP2E1, NOS1, NOS2, CYP2A6, CBS,
    TAS1R3, ALDH3B1, TAS2R38.
  - G5 : 15 présents (aucun absent), 15 retenus : CDX1, CDX2, VIL1,
    SI, LCT, FABP2, APOA4, APOB, KRT7, KRT19, CHGA, CHGB, SYP,
    INSM1, NEUROD1.
  - TEMOIN acineux : 11 présents, 11 retenus : PNLIP, CTRB2,
    CELA3A, CTRB1, CPA1, CELA2A, CPB1, CELA3B, CLPS, CTRC, CPA2.
- Fichiers (SHA complets dans `manifest_858_files.txt`) :
  G1 kras `782efc14…`, G1 stage `7fc24f40…`, G2 kras `5141764b…`,
  G2 stage `c3da75d0…`, G4 kras `f6bf4dfb…`, G4 stage `19c6001d…`,
  G5 kras `d1365fdc…`, G5 stage `659a7d92…`, TEMOIN kras `c913f7cc…`,
  TEMOIN stage `91fdd52c…`, G3 kras `acdc05aa…`, G3 stage `4af722ba…`
  (+ 12 nuls correspondants, graine 42).
- Nuls : bloc des flux permuté par lignes, graine 42, `rng(42)`,
  colonne de contrôle intacte.

## Runs v6.2 (mode fast) — lot TCGA terminé 24/24

- Manifeste `manifest_v62_858.txt` : 24 runs (6 groupes × 2 ordres ×
  réel/nul). Lanceur reprenable `run_v62_lot.sh`. Lancement en
  `systemd-run --unit=v62-858 --collect` (+ `--unit=v62-858b` pour
  G4+G5 en parallèle), surveillance `watch_v62_858.sh` (arrêtée
  d'elle-même à 24/24, tour 2, 2026-11-20T06:44:36Z).
  Journaux : `runs_v62_858.log` (FIN 2026-11-20T06:44:16Z,
  déjà faits 13, terminés 11, échecs 0) et `runs_v62_858b.log`
  (FIN 2026-11-20T06:16:50Z, déjà faits 3, terminés 5, échecs 0).
  Tous les exits : 0. Pipeline revérifié inchangé après le lot :
  SHA `f07567c4…c3abf`.
- Incidents : 2 redémarrages machine (20 nov. ~03h44 UTC et
  ~05h43 UTC), unités tuées, relancées à chaque fois, reprise
  sans perte (lanceur saute les sorties déjà complètes ; aucun
  dossier de run supprimé, aucun CSV modifié).
- Lecture : `extract_858.py` (SHA
  `a6765721332361343450456d629ace688baca17ebebe37aa319815238e8db6af`) ;
  `extract_858.json` + `extract_858.csv` (24 runs, 0 manquant).

## Confirmation — GSE71729 et GSE62452 (règle §6 statuée à 24/24)

- Groupes qualifiés : G1, G2, G3, G4, G5 (critère : MC diff > 0,05
  OU S_sep diff > 0,05 OU D1 |d| ≥ 0,50 au-delà du nul, sur au
  moins un ordre TCGA ; détail dans la section). TEMOIN exclu
  (témoin, pas candidat).
- Construction : `build_fluxes_858_geo.py`, SHA
  `3f7d4978588370a6a0ec093211e7e2eaeaee7e9eaf34c785903810552b869a4b`
  (variante (a) : mêmes gènes retenus TCGA présents dans la
  cohorte, ordre KRAS brut, sans correction de pureté, cas
  complets). GSE71729 : 145 tumeurs primaires
  (« tissue type: Primary », characteristics_ch2) ; GSE62452 :
  69 tumeurs (« tissue: Pancreatic tumor », characteristics_ch1),
  mapping GPL6244 (`data/GPL6244_probe2symbol.tsv`), médiane
  par symbole.
- Règle de stade GSE62452, gelée dans `build_fluxes_858_geo.py`
  avant la construction : IA/IB → I, IIA/IIB → II, III → III,
  IVA/IVB/IV → IV, « >IIB » exclu (ambigu), stade manquant exclu,
  départage GSM lexicographique ; série < 40 lignes → pas de
  série stade. Effectifs : I 4, II 45, III 13, IV 6, 1 exclue
  (« >IIB ») ; série stade 68 lignes. Stades bruts (tous
  échantillons) : IIA 18, III 26, IVA 4, IVB 2, IIB 64, IV 7,
  IB 7, « >IIB » 2.
- Fichiers : `pdac_858_geo71729_<groupe>_kras.csv` (+ _nul.csv),
  145 lignes ; `pdac_858_geo62452_<groupe>_<kras|stage>.csv`
  (+ _nul.csv), 69 / 68 lignes. SHA dans les sorties du script
  (G1 71729 `149acb88…`, G2 `b4f031e6…`, G3 `f92355a3…`, G4
  `60a55a63…`, G5 `b9f994a9…` ; G1 62452 kras `826e23e7…`,
  stage `7f445ac0…`, G2 kras `958c804d…`, stage `4b7045a6…`,
  G3 kras `91ecedde…`, stage `023263e1…`, G4 kras `74534dfd…`,
  stage `7138e988…`, G5 kras `b175e3ec…`, stage `eb55daab…`).
- Gènes retenus absents des cohortes (notés, jamais remplacés) :
  GSE71729 — G1 : MUC5B, MUC21, PGA4 ; G2 : AMY1A, AMY2A,
  CELA2A, CELA2B, CELA3B ; G3 : OR13A1, OR2A4, OR52N4, OR52N2,
  OR1J2, OR2A1, OR4C6, OR5K2, OR2T10 ; G4 : UGT1A1, ADH1B,
  TAS1R3 ; G5 : aucun. GSE62452 — G1 : PGA4 ; G2 : AMY1A,
  CTRB1 ; G3 : OR2A4, OR2A1, OR3A2 ; G4 : aucun ; G5 : aucun.
  Conséquence : OR2A4 (piste OR/KRAS de TCGA) absent des deux
  puces — non confirmable ; UGT1A1 (plus fort rho G4/KRAS)
  absent de GSE71729, présent dans GSE62452.
- Lots lancés le 20 nov. : unités `v62-858c` (GSE71729, 10 runs,
  manifeste `manifest_v62_858_71729.txt`) et `v62-858d`
  (GSE62452, 20 runs, manifeste `manifest_v62_858_62452.txt`),
  surveillance `watch_v62_858_geo.sh`, journaux
  `runs_v62_858_71729.log` / `runs_v62_858_62452.log`.
  **TERMINÉS 30/30, exits 0/0** : `WATCH 858-71729 TERMINE
  10/10`, `WATCH 858-62452 TERMINE 20/20` (20 nov. 08h37Z).
  Trois redémarrages de machine durant le lot, unités relancées
  à chaque fois, reprise sans perte (lanceur saute les sorties
  déjà complètes ; aucun dossier de run supprimé).
  Pipeline revérifié inchangé après le lot :
  SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
- Lecture des confirmations : `extract_858_geo.py` (SHA
  `27cc7985b9e5876a…`, réutilise `extract()` de `extract_858.py`,
  original intact) ; `extract_858_geo.json` /
  `extract_858_geo.csv` (30 runs, 0 manquant). Tests directs
  de confirmation : `reading_858_geo.py` (SHA
  `cf02bba1539db5c7…`, mêmes D1/D3 que `reading_858.py`) ;
  `direct_tests_858_geo.csv` (SHA `bc10e35d6c6c0db0…`, 253
  lignes ; seuil de Bonferroni 0,05/253 ≈ 0,0002). Résultats
  complets dans la section §8.58 (lignes 556–590 pour les
  confirmations ; verdict en tête ajusté).

## Tests directs

- `reading_858.py` (harnais, hors pipeline) ; table vérifiée
  `direct_tests_858.csv`, SHA
  `6ff4d9aa38b832f71bf39e342d4b5677c0dece4f0f80aa86ad39aab2ab49b8ba`
  (212 lignes : 6 groupes × 2 ordres × flux).
- Extracteur pipeline : (copie adaptée, clés §8.38 — à compléter
  après la fin du lot dans la section §8.58).

## Ce qui manque / limites

- Aucun composé volatil mesuré : pas de données de volatilome
  détenues ; la piste « odeurs » est testée au niveau des gènes
  (récepteurs OR/TAAR/TAS et enzymes), pas des molécules odorantes.
- G2 / pureté : 8 des 20 flux G2 retenus sont des gènes du score
  acineux (PNLIP, CELA2A, CPB1, CLPS, CPA2, CTRB2, CTRB1, CELA3B) —
  les résidus G2 sont calculés après régression sur un score
  construit à partir d'eux-mêmes (biais de construction nommé
  au protocole §3 ; témoin acineux fourni).
- OR : symboles des annotations détenues ; aucun réalignement.
  Une expression mesurée n'est pas une preuve de fonction
  olfactive ; une absence de la matrice n'est pas une preuve
  d'absence biologique (ex. ICGC ne retient que 3 OR : filtrage
  basse expression de la matrice, pas une mesure d'absence).
- Stade : 4 niveaux, ties massives, sommet mince (III + IV = 8),
  mêmes limites qu'au §8.45. Pas de single-cell, spatial,
  longitudinal, ni de volatilome.
