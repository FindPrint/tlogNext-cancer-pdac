# PROVENANCE — §8.71 : GSE60979 (confirmation indépendante maxsep, C3)

Date : 20 novembre 2026. Chantier §8.71. Protocole gelé :
`PROTOCOL_maxsep_cohort_871.md`, SHA-256
`82a2c93d2975274e9a900343ef626b8d37b5634bb008d107e8bff9b106496eef`
(gel avant téléchargement officiel, construction et runs).

## 1. Source — la cohorte

- **Série : GSE60979, NCBI GEO** — sous-série [mRNA] de la
  SuperSeries GSE60980, « mRNA and miRNA expression profiles for
  fresh frozen periampullary adenocarcinomas (pancreatobiliary and
  intestinal type) and adjacent normal tissues ».
- **Étude d'origine : Sandhu et coll., *Molecular Oncology* 2015,
  9:758–771, PMID 25579086, doi 10.1016/j.molonc.2014.12.002** —
  « Molecular signatures of mRNAs and miRNAs as prognostic
  biomarkers in periampullary adenocarcinomas ». Centre : Oslo
  University Hospital, Oslo, Norvège (Department of Genetics,
  Institute for Cancer Research ; Department of
  Hepato-Pancreato-Biliary Surgery, Oslo University Hospital).
- **Dépôt : NCBI GEO**, série soumise le 2 sept. 2014, publique.
  URL du fichier de données :
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE60nnn/GSE60979/matrix/GSE60979_series_matrix.txt.gz`
- **Plateforme : GPL14550** (Agilent SurePrint G3 Human GE 8x60K,
  Homo sapiens), lue dans l'en-tête de la matrice
  (`!Series_platform_id "GPL14550"`, à confirmer sur le fichier
  officiel au §3).
- **Effectifs (caractéristique ch1, à confirmer §3) : 93
  échantillons — 49 tumeurs PDAC** (`tissue: pancreatic ductal
  adenocarcinoma`), 12 tissus normaux adjacents, 9 adénocarcinomes
  duodénaux, 8 du cholédoque, 8 de l'ampoule type
  pancréatobiliaire, 7 de l'ampoule type intestinal. Titres des
  PDAC : `PDAC_1 [mRNA]` … `PDAC_49 [mRNA]` ; aucun code-barres
  TCGA (vérifié sur la copie d'enquête et sur le fichier
  officiel, §3).
- **Nature des valeurs (confirmée §3) :** intensités log2
  normalisées Agilent, d'après `!Sample_data_processing` :
  « The scanned images were analyzed using Feature Extraction
  Software 10.7.3.1 (Agilent Technologies) using default
  parameters. The expression profiles were backgroundcorrected
  and quantile normalized for mRNA. » Plage sur la matrice
  complète : min 4,02 / médiane 6,72 / max 18,81, 0 NaN.
  Aucune renormalisation, aucune transformation log ajoutée
  (protocole §4.2).

## 2. Indépendance — vérifiée avant le gel

1. Chaîne exacte « GSE60979 » absente de tout le projet avant ce
   chantier (grep sur le livre blanc, les sections, les
   protocoles, les provenances et les dossiers de runs, 20 nov.
   2026) ; « GSE60980 » absente également. Aucun CSV, aucun run,
   aucun JSON, aucune valeur `maxsep` pour GSE60979.
2. Nouveaux patients (Oslo, 2014), nouveau centre, nouvelle
   plateforme (GPL14550) — distincte de toutes les plateformes
   V1 et des confirmations (voir protocole §2.2).
3. Pas un re-test déguisé : nouveaux CSV, nouveaux runs v6.2
   frais ; la sous-série miRNA GSE60978 n'est pas utilisée.
4. Caveat consigné (ne concerne pas GSE60979) : la cohorte
   écartée GSE77858 est une étude UCLA, comme la cohorte
   inutilisée GSE32676 (Donahue et coll.) — titres anonymes,
   recoupement de patients non vérifiable par identifiants.
   GSE60979 est une cohorte d'Oslo : ce caveat ne s'y applique
   pas.

## 3. Fichiers téléchargés (après le gel) — vérifiés

- `data/GSE60979_series_matrix.txt.gz`, 20 547 348 o, SHA-256
  `819408bf8dacb01c38eede69287d255eea76f74e2b1b18ec8863933f4700c4eb`
  (HTTP 200, 20 nov. 2026, 20h45 EST). **Identique bit à bit à
  la copie d'enquête `/tmp` (même SHA)** — les portes §5 ont
  néanmoins été re-vérifiées sur ce fichier officiel avant toute
  construction (`build_fluxes_871.py`, sortie consignée §5).
- Plateforme lue dans l'en-tête : **GPL14550**
  (`!Series_platform_id "GPL14550"`). Titre, dates (soumission
  2 sept. 2014, dernière mise à jour 14 juil. 2023) et PMID
  (25579086, 26590090, 36923555) lus dans l'en-tête.
- Effectifs confirmés sur le fichier officiel : 93 échantillons,
  49 tumeurs PDAC, 44 exclus (12 normaux adjacents + 32 autres
  adénocarcinomes périampullaires) ; 0 NaN ; aucun code-barres
  TCGA dans les titres ni les GSM.
- `data/GPL14550_probe2symbol.tsv`, SHA-256
  `cc034a76285b0785bff4dd5249d68becb58acacedb157a8032d0c9309dac3909`
  (construit à neuf dans l'enquête, 42 545 lignes de table,
  30 436 sondes avec symbole, 22 070 symboles uniques, colonne
  `GENE_SYMBOL`, marqueur `!platform_table_end` vu ; script
  `download_gpl14550_mapping_871.py`). Repris tel quel, non
  reconstruit dans le chantier.
- `data/GPL7264_probe2symbol.tsv`, SHA-256
  `41a4716063d9cb37518670dd0ab54b26064e52e34f8cb156614dc73e3aa6c27e`
  (mapping de la cohorte écartée GSE77858 ; construit dans
  l'enquête, 20 242 lignes, 18 703 sondes avec symbole,
  16 746 symboles uniques ; MUC17 absent — raison de
  l'exclusion, protocole §2.3). Détenu pour traçabilité,
  aucune valeur n'en est tirée.

## 4. Enquête préalable (avant le gel) — ce qui a été vérifié

- Recherche E-utilities NCBI GEO, 20 nov. 2026 : `pancreatic AND
  Series[ET]`, 789 séries ; résumés récupérés (793 enregistrements
  esummary) ; filtre humain + n ≥ 40 → 191 séries ; examen des
  titres et des sous-séries. Fichiers de travail : `/tmp`
  (`gds_series_summary.json`, `gds_series_ids.txt`) — hors
  chantier, non livrés.
- Copies temporaires `/tmp` (vérifications de portes uniquement,
  supprimées, jamais utilisées pour construire un flux ni lancer
  un run) : `GSE77858_series_matrix.txt.gz` (4 972 800 o, SHA
  `d4afe2289de3ca16053ce8a93f008317eb5af260bfe6345bfbfa52f4f04a2c18`),
  `GSE60979_series_matrix.txt.gz` (20 547 348 o, SHA identique
  au fichier officiel, voir §3), `GSE32676_series_matrix.txt.gz`
  (6 462 990 o, titres anonymes « human PDAC 1..25 »),
  `GSE43797_series_matrix.txt.gz` (7 977 135 o, 7 PCA seulement).
- Candidats écartés : voir protocole §2.3 (raisons écrites
  d'avance). Piste restante nommée : GSE131050 (PurIST, 191
  échantillons, deux lots Linehan/Yeh, deux plateformes) —
  non vérifiée, pour un chantier futur.

## 5. Construction et runs — terminés 20 nov. 2026

- Construction : `build_fluxes_871.py`, SHA-256
  `1134c574d6727b6d4fa2e13cfe4a69efca01143602b9ca4e47791b57fa268ed9`,
  variante (a), 12 gènes v4, ordre KRAS croissant, cas complets
  49/49, nul graine 42. Portes §5 : 3/3 OK sur le fichier
  officiel. KRAS (valeurs puce) : min 7,90 / médiane 8,75 /
  max 10,03. Flux : `pdac_871_geo60979_fluxes.csv` (49 lignes),
  SHA `51a7fa56…0554e` ; nul SHA `d427359a…34740`.
  Aucun nul frais construit : `d_maxsep` +0,2045 est hors de
  l'intervalle gelé [−0,07 ; +0,14[ (§7) — le script
  `build_nul_871.py` (SHA
  `cd8b5a4f5ff3e5fc888c094007e3f71e39a45b9fc544adc39994e2f06e141cda`)
  n'a pas été exécuté.
- Pipeline v6.2, SHA
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
  revérifié avant ET après le lot, inchangé.
- Runs : 2/2 v6.2 mode fast, exits 0/0, 35 fichiers chacun,
  20h46:50Z → 20h55:27Z (~9 min), unité systemd `v62-871`,
  surveillance `watch_v62_871.sh` (arrêtée d'elle-même à 2/2,
  `WATCH 871 TERMINE 2/2`, tour 2, 20h55:47Z) ; journal
  `runs_v62_871.log` (100 lignes ; FIN 20h55:27Z, déjà faits 0,
  terminés 2, échecs 0). Aucun redémarrage de machine.
- Extraction : `extract_871.py` (SHA
  `687bf9fe383633aa2bc5faa579e0bfa99f8cd08bd619ef3275a4e737ad1359e8`)
  → `extract_871.json` (SHA
  `85e9089a9f4c5ee0d7984bfd44ed2646dc0842174401395642cb479cd1f55e3b`)
  / `extract_871.csv` (SHA
  `6e474668eb24bbccb2d889d4ac38a80c528f1276b21d094ca0ac88c362166e25`).
  Vérification indépendante : `verify_871.py` (SHA
  `5cc8cc1d180f5b8571e21563c1cd9237cbd2ebb29774029e2a0e6ae0d408638d`)
  → `maxsep_871_verify.json` (SHA
  `ca8795b39e39e34a0155a5725834e809ea3bfa21819a1d1a66b117696117b063`) :
  2/2 comparaisons, écart max 0,0 exact, verdict OK.
- Tests directs : `direct_tests_871.py` (SHA
  `c543044a82b74d9e4b79b978f5971889a82aa0b664de2c6a8700dc2525295cbc`)
  → `direct_tests_871.json` (SHA
  `2c94e28a8bfb3aaeca83a4f4076a27d9436c2f7225572531a2a47b35d5811f94`) :
  Cohen marginal 0,0000 pour les 12 gènes (vacuité par
  construction, comme prévu au §9) ; Spearman Δρ médian +0,180,
  8/12 positifs.
- Verdict : **CONFIRME — d_maxsep +0,2045, A2 7/11, LOO 6/10,
  C3 levée.** Détail dans `section_8.71_gse60979.md`.

## 6. Ce qui manque

- Publication de Sandhu et coll. : aucune valeur `maxsep` n'y
  figure (signature pronostique périampullaire, pas de test du
  pipeline) — elle ne prédit rien ici.
- Les données brutes individuelles (FASTQ) ne sont pas utilisées :
  seule la matrice de série normalisée par les déposants sert
  aux flux. Les 12 normaux adjacents et les 32 autres
  adénocarcinomes périampullaires sont exclus (comptés §3) :
  ils ne servent pas à la paire.
- Aucune donnée clinique (stade, survie) n'est utilisée : la
  paire n'a besoin que de l'ordre KRAS.

— Fin de la provenance §8.71 (sections 3 et 5 à compléter après
construction et runs). —
