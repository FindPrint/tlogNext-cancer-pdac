# PROVENANCE — §8.70 : Confirmation indépendante pour `maxsep` (C3) sur GSE79668

Date : 20 novembre 2026. Chantier §8.70, go de Zackary « Allez s'y »
(20 nov. 2026, 14h29). Protocole gelé :
`PROTOCOL_maxsep_gse79668_870.md`, SHA-256
`fd479d50414a18c2daa2b7cb9aeab55dcc24a49ae30ed6ceee363b4d47c96980`
(gelé AVANT tout téléchargement, toute construction et tout run).

## 1. Cohorte

- Série : **GSE79668**, NCBI GEO — « RNA-sequencing of human
  pancreatic adenocarcinoma cancer tissues ».
- Étude d'origine : Kirby et coll., *Molecular Oncology* 2016,
  10(8):1169–1182 — « RNA sequencing of pancreatic adenocarcinoma
  tumors yields novel expression patterns associated with long-term
  survival and reveals a role for ANGPTL4 ». PMID **27282075**,
  PMCID PMC5423196, doi 10.1016/j.molonc.2016.05.004.
- Centre : University of Alabama at Birmingham + HudsonAlpha
  Institute for Biotechnology (Huntsville, AL, USA). Contact
  déposant : Marie K. Kirby (HudsonAlpha).
- Dépôt : série soumise le 29 mars 2016, publique le 11 juin 2016,
  dernière mise à jour 15 mai 2019. BioProject PRJNA316673, SRA
  SRP072492. Sous-série de GSE79670 (relation déclarée dans
  l'en-tête de la matrice).
- Effectif : **51 échantillons**, tous des tissus tumoraux de
  patients opérés par résection chirurgicale (titres `T_*`, GSM
  GSM2100851–GSM2100901, caractéristiques : statut de survie,
  survie en jours, âge, race, sexe — aucune caractéristique
  « normal » / « non-tumoral »). Aucun code-barres TCGA dans les
  titres ni les GSM (vérifié).
- Plateforme : **GPL11154** (Illumina HiSeq 2000, Homo sapiens),
  confirmée par `!Series_platform_id` dans l'en-tête de la matrice.
- Type : expression profiling by high throughput sequencing (RNA-seq).
- Usages publiés : jeu de validation indépendant face à TCGA dans
  Liu et coll., *Oncol Rep* 2019, 41:1521–1530
  (doi 10.3892/or.2019.6979, tableau I : TCGA n = 178, GSE79668
  n = 51, GSE62452 n = 69) ; jeu de validation dans l'étude TLS
  2025 (*IET Syst Biol* 19:e70038).
- Nombre de gènes attendu : 19 175 (Posta et coll., *Clin Transl
  Sci* 2023, tableau des cohortes) — à comparer aux 48 956 lignes
  du fichier de comptages (transcrits GENCODE v. 9, voir §2).

## 2. Fichiers téléchargés (20 nov. 2026, ~14h36 EST / 19h36 UTC)

- Matrice :
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE79nnn/GSE79668/matrix/GSE79668_series_matrix.txt.gz`
  — HTTP 200, 3 724 o, SHA-256
  `b2226fd096f27a9e5caf32cca3491d1f1e52082ce6e9876b2b1c1f67d88e4754`.
  Contenu : 80 lignes décompressées (63 699 o) ; en-tête complet
  (titre, accession, statut, contributeurs, 51 GSM, 51 titres,
  caractéristiques) ; **table de données VIDE : 0 ligne** (seule
  la ligne d'en-tête `ID_REF` + 51 GSM). Les valeurs ne sont PAS
  dans la matrice.
- Fichier supplémentaire de la série (nommé dans l'en-tête de la
  matrice, `!Series_supplementary_file`) :
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE79nnn/GSE79668/suppl/GSE79668_51_tumors_sharedgenecounts.txt.gz`
  — HTTP 200, 3 588 753 o, SHA-256
  `721cd3a0d1155375ea054f410f65497568284135f32ad59157d62a564cba54f8`.
  Contenu : 48 957 lignes décompressées (9 051 001 o) —
  48 956 gènes x 51 échantillons, 0 NaN.
- Nature des valeurs : **comptages bruts de transcrits** (entiers,
  min 0 / médiane 17 / max 17 823 551), GENCODE v. 9, d'après
  `!Sample_data_processing` : « Gene transcript sequence counts
  for all genes across all tissues using GENCODE v. 9 ». Ce ne
  sont NI des log2, NI des valeurs normalisées (FPKM/RPKM/TPM).
  Aucune renormalisation, aucune transformation log ajoutée
  (protocole §4.2) — les flux sont les comptages bruts tels que
  fournis, ordonnés par KRAS croissant (l'ordre est invariant
  par transformation log monotone : l'ordre KRAS serait le
  même en log). La nature « comptages bruts » est nommée comme
  limite au §8.70 (comme les log-ratios l'étaient au §8.69.5).
- Identifiants de lignes : forme `SYMBOLE_ENSG...` (ex.
  `KRAS_ENSG00000133703.7`) ; le symbole est le préfixe avant
  `_ENSG` (extraction mécanique, 48 956/48 956). Symboles
  dupliqués : 4 434 (plusieurs Ensembl vers un même symbole) —
  agrégation par médiane (règle du projet). Les 13 gènes utiles
  (12 v4 + KRAS) ont chacun exactement 1 ligne : aucune
  agrégation ne les touche. KRASP1 (pseudogène,
  `KRASP1_ENSG00000220635.2`) est une ligne distincte, non
  confondue avec KRAS.
- Jointure échantillons : positionnelle (même ordre dans la
  matrice et dans le fichier de comptages), vérifiée : 49/51
  radicaux de titres identiques, les 2 autres ne diffèrent que
  par un « _T » final dans le titre de la matrice
  (`T_06_01_A033a_T`, `T_06_04_A296a_T` → `T_06_01_A033a`,
  `T_06_04_A296a` dans les comptages) ; après retrait de ce
  suffixe, 51/51.
- KRAS (comptages bruts) : min 265 / médiane 1 919 / max 3 707.

## 3. Vérification d'indépendance (protocole §2.2, avant le gel)

- Chaîne exacte « GSE79668 » : seules mentions dans
  `~/workspace/runs/pdac-v6/` = protocole §8.69, provenance
  §8.69, section §8.69 (toutes au sens « piste restante non
  vérifiée »), plus le livre blanc au même sens. Aucun CSV de
  flux, aucun run, aucun JSON, aucune valeur `maxsep`, aucun
  fichier de données avant ce chantier. Les 2 257 fichiers JSON
  contenant la sous-chaîne nue « 79668 » sont des coïncidences
  numériques (ex. 65,79668663986135 dans
  `results_fast_tcga_v1/master_results.json`) — vérifié par
  lecture du contexte.
- Nouveaux patients (UAB, 51 tumeurs réséquées 2016), nouveau
  centre, nouvelle plateforme (GPL11154, RNA-seq Illumina) —
  distincts de TCGA, ICGC PACA-AU, GSE62452 (NCI, Affymetrix),
  GSE71729, GSE21501 (Stratford, Agilent), GSE57495 (Moffitt),
  GSE62165.
- L'article Kirby et coll. a lui-même utilisé TCGA comme cohorte
  de validation de sa signature : les 51 échantillons restent
  des patients UAB, pas des échantillons TCGA — aucun
  recouvrement d'échantillons (vérifié : aucun code-barres TCGA
  dans les titres/GSM).
- Exclusions reprises : GSE78229, GSE28735 (re-tests de
  GSE62452), COAD/LUAD, CPTAC, GSE15471/GSE16515/GSE32676/
  GSE91035/GSE84219/GSE179351 (n < 40), ICGC PACA-CA /
  E-MTAB-6134 (hors périmètre), GSE57495/GSE62165 (portes §5
  échouées au §8.69), GSE21501 (paire §8.69).

## 4. Construction (variante (a))

- Script : `build_fluxes_870.py` (SHA noté au §8.70.8 ;
  copie adaptée de `build_fluxes_869.py`, original intact).
- Gènes v4 (12, ordre de la liste) : PGC, REG4, CLDN18, MUC17,
  DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16 —
  **12/12 présents, 1 ligne chacun**.
- Contrôle : KRAS (comptages bruts, croissant), jamais un flux.
- Tumeurs seules : 51/51 (série tumorale uniquement).
- Cas complets (KRAS + 12 gènes) : **51/51** (0 NaN).
- Portes §5 : TOUTES OK (voir sortie du builder).
- Sorties : `pdac_870_geo79668_fluxes.csv` (51 lignes) et
  `pdac_870_geo79668_fluxes_nul.csv` (graine 42) — SHA notés
  au §8.70.8. Nuls frais éventuels (§4.4/§7) : graines 8701,
  8702 — courus seulement si `d_maxsep` dans [−0,07 ; +0,14[.

## 5. Ce qui manque

- Aucune donnée clinique individuelle utilisée (survie, âge,
  sexe sont dans les caractéristiques mais ne servent pas à
  la paire — ordre KRAS uniquement).
- La matrice ne contient pas les valeurs (table vide) : les
  valeurs viennent du fichier supplémentaire de la série
  (même dépôt, même série, nommé dans l'en-tête de la matrice).
  Aucun mapping GPL11154 construit : non nécessaire (symboles
  dans les identifiants de lignes) — le script
  `download_gpl11154_mapping_870.py` n'existe donc pas.
- Aucune renormalisation des comptages bruts : la distribution
  des flux est celle des comptages (forte asymétrie, médiane
  17, max 17,8 M) — nommée comme limite, pas corrigée après coup.
