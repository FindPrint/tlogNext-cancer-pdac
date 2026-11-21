# PROVENANCE_888 — GSE194249 à 11 flux (§8.88)

**Date :** 21 novembre 2026, ~10h05–15h40 EST.
**Agent :** TagPrint (subagent, piste 2 du lot du 21 nov. 2026, §8.88).
**Go :** Zackary, 21 nov. 2026, 10h07.
**Protocole gelé :** `PROTOCOL_gse194249_11flux_888.md`, SHA-256
`f5eb1f952f562499e6ff31036b684cb75d094a2843a17a067acf27ca7c763e02`
(gelé AVANT toute construction de CSV et tout run).
**Pipeline :** v6.2, SHA
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
vérifié avant et après les lots, inchangé — **4/4 runs exit 0**.
**Livre blanc :** non édité. PDF non régénéré. Rien poussé sur GitHub.

## 1. Source des données

- **Série :** GSE194249, NCBI GEO.
- **Article :** Shi X, Li Y, Yuan Q, Tang S, Guo S, et al.
  « Integrated profiling of human pancreatic cancer organoids
  reveals chromatin accessibility features associated with drug
  sensitivity », *Nature Communications* 2022, 13:2169.
  DOI 10.1038/s41467-022-29857-6 (CC BY 4.0).
  URL : https://www.nature.com/articles/s41467-022-29857-6
  (PDF : https://www.nature.com/articles/s41467-022-29857-6.pdf).
  Affiliations : Changhai Hospital, Second Military Medical
  University (Naval Medical University), Shanghai, Chine ;
  Shanghai Institute of Biochemistry and Cell Biology, Chinese
  Academy of Sciences, Shanghai, Chine ; et autres (voir
  l'article, p. 1).
- **Page GEO :** https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE194249
  (accès direct bloqué par reCAPTCHA le 21 nov. 2026 — les
  métadonnées viennent de l'API E-utilities, voir §2).
- **Fichier (unique source d'expression, aucun nouveau
  téléchargement dans ce chantier — matrice détenue depuis le
  §8.86, re-vérifiée par SHA avant construction) :**
  `GSE194249_PDPCOs_FPKM.txt.gz`, URL
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194249/suppl/GSE194249_PDPCOs_FPKM.txt.gz`
  (miroir HTTPS du FTP GEO, 1re tentative, 21 nov. 2026, §8.86).
- **Fichier local :** `data/GSE194249_PDPCOs_FPKM.txt.gz`,
  4 927 876 o, SHA-256
  `479517fbed1d8f5bb9d141b6b932b6ab56ba2ba72d4394d13aea2a3da0a50f27`,
  gzip intègre — identique au §8.86. Reçu :
  `download_gse194249_886_receipt.json`, SHA
  `fd9bd625a3869086d06b11bb4896b5e5de7f05da91bf5867bca8d1bf83a016ea`
  (reçu §8.86, réutilisé tel quel, aucun nouveau téléchargement).
- **Aucun SHA attendu pré-connu :** GEO ne publie pas de SHA
  pour ce fichier ; la vérification est l'intégrité gzip + les
  comptages (voir §4) + l'identité du SHA avec le §8.86.

## 2. Métadonnées pré-gel (aucune donnée d'expression lue avant le gel, sauf les comptages de présence du §4)

- **NCBI E-utilities, esummary GDS** (`db=gds&id=200194249`,
  21 nov. 2026, §8.86), réponse conservée
  `gse194249_esummary_886.json`, SHA-256
  `73934e46a717a5db1ed8cd8e1c4349435683a0eed1dda85fe7b097ec448f460e` :
  titre, accession GSE194249, plateforme GPL31265, dépôt
  2022/02/23, *Homo sapiens*, « Expression profiling by high
  throughput sequencing », fichier supplémentaire de type TXT,
  **87 échantillons** : 75 `CAS-DAC-*`, 4 `CAS-NEN-*`,
  4 `CAS-IPMN-*`, 1 `CAS-ACC-1`, 3 `NPC-*`.
- **Article (résumé et méthodes, lus le 21 nov. 2026, §8.86) :**
  84 lignées PDPCO (75 PDAC, 4 IPMN, 1 ACC, 4 NEN) + 6 NPO
  établis ; échantillons prélevés par chirurgie ou biopsie
  EUS-FNA. Méthodes RNA-seq : lectures mappées sur hg19 par
  TopHat ; FPKM par Cufflinks ; « Genes with FPKM values <1 in
  all 87 samples were filtered out. Finally, 15,819
  protein-coding genes remained for further analysis. »
  (p. 12 des méthodes). Les 87 échantillons du filtre sont
  les 84 PDPCOs + 3 NPOs — le même décompte que GEO.
- **Livre blanc (grep avant le gel, 21 nov. 2026 ~10h05 EST) :**
  « GSE194249 » : 34 occurrences, toutes au §8.78 (inventaire
  C4), au §8.79.9 (piste ouverte (d)) et au §8.86 — jamais
  comme cohorte courue, jamais comme holdout, jamais comme
  valeur `maxsep`. « Shi et al » : 4 occurrences, toutes dans
  le §8.86. « PDPCO » : 20 occurrences, toutes au §8.78/§8.86.
  « CAS-DAC » : 2 occurrences, toutes dans le §8.86.
- **Dossier de runs (avant le gel) :** aucun CSV `pdac_886_*`,
  aucun dossier `results_fast_v62_886_*`, aucun manifeste,
  journal ou extraction `886` — **0 run jamais lancé pour
  GSE194249** avant ce chantier. Les seuls fichiers contenant
  « 194249 » dans leur nom sont ceux du §8.86 (protocole,
  provenance, téléchargement, reçu, esummary, section).
- **Décision A2 gelée avant les runs (protocole §2.3) :** la
  paire à 11 flux ENTRE dans le compte A2 comme quinzième
  paire principale indépendante, avec le caveat « 11 flux,
  DPCR1 absent » — précédent §8.79 (GSE57495, 11 flux,
  compte comme treizième paire) ; différence avec le §8.84
  hors compte (lot drogue, objet différent, n = 46).
  Décision prise avant tout run, non révisée selon l'issue.

## 3. Nature des lignes

- La matrice détenue est un **fichier déposé par les auteurs**
  (FPKM Cufflinks, hg19, filtré FPKM < 1) : ce sont des valeurs
  mesurées, transformées par le pipeline des auteurs (mapping +
  quantification + filtre), pas des mesures brutes de ce chantier.
- Les CSV de flux de ce chantier (`pdac_888_*`) sont des
  **re-découpages** de cette matrice déposée : sélection des 11
  gènes + KRAS, exclusion des 3 normaux `NPC-*`, tri par KRAS
  FPKM croissant, `step` = rang. Aucune renormalisation, aucune
  transformation log, aucune imputation.
- Les CSV nuls (`_nul`, `_nul_s8881`, `_nul_s8882`) sont des
  **échantillons hypothétiques** : permutation des lignes du bloc
  des flux (graines 42, 8881, 8882), contrôle intact — pas des
  mesures.
- Les `maxsep`, MC, S_sep, Delta, L7a, cascades et falsifications
  sont des **sorties du pipeline v6.2** sur ces CSV, lues par
  `extract_888.py` et recoupées à 0,0 exact par `verify_888.py`.
- Les tests directs (Spearman contre le pas, d de Cohen marginal)
  et l'annexe PDAC-seul sont des **calculs de ce chantier** sur
  les CSV et la matrice détenue — ils ne décident pas.
- Les résultats de l'article (sous-types, pics ATAC, signature de
  sensibilité, mutations KRAS 96 %, etc.) sont des RÉSULTATS
  RAPPORTÉS par leurs auteurs, repris avec leur source — pas des
  mesures de ce chantier, pas des verdicts importés.

## 4. Vérifications effectuées (chiffres, deux chemins indépendants)

- Fichier : 15 610 lignes (en-tête + 15 609 lignes de gènes),
  88 colonnes (`GeneSymbol` + 87 échantillons) — mise en page
  (A) du protocole. En-tête : `GeneSymbol, CAS-DAC-1,
  CAS-IPMN-1, CAS-DAC-11, …`, dernière colonne `NPC-7`.
- Colonnes : les 87 titres correspondent EXACTEMENT aux
  87 échantillons de l'esummary (0 inattendu, 0 manquant —
  vérifié par le script de construction). Normaux `NPC-4`,
  `NPC-5`, `NPC-7` : 3 colonnes exclues ; PDPCOs : 84
  (75 PDAC, 4 IPMN, 4 NEN, 1 ACC).
- Symboles dupliqués : 0 ligne. Gènes uniques : 15 609.
- **Présence des 12 gènes utiles (symbole exact, une ligne
  chacun), vérifiée AVANT le gel par deux chemins (lecture
  pandas + zgrep brut, 21 nov. 2026 ~10h05 EST) et
  re-vérifiée par le script de construction :** PGC 1, REG4 1,
  CLDN18 1, MUC17 1, **DPCR1 0**, CR2 1, KRT20 1, MUC2 1,
  GSTM1 1, CEACAM5 1, CLCA1 1, MUC16 1, KRAS 1.
  **MUCL3 (descriptif) : 0.** DPCR1 : 0 occurrence dans tout
  le fichier (exact, insensible à la casse) ; aucun symbole
  contenant `DPCR`.
- **Construction :** 84/84 cas complets (KRAS + 11 gènes),
  0 NaN. KRAS FPKM : min 3,1647 / médiane 13,2894 / max
  24,9045 ; 0 valeur ≤ 0. Le script de construction s'arrête
  si DPCR1 apparaissait — il ne s'est pas arrêté.
- **Reproductibilité :** le CSV réel reconstruit lors de la
  construction des nuls frais porte le même SHA exact
  (`7799a62a…aeda`).
- **Runs :** 4/4 exit 0 (paire FIN 2026-11-21T15:23:29Z,
  nuls frais FIN 2026-11-21T15:36:25Z), unités systemd
  `v62-888` et `v62-888frais`, jamais nohup.
- **Extraction et vérification :** `extract_888.py` : 4/4 runs,
  0 manquant. `verify_888.py` : `maxsep`, ancien MC et
  stabilité recoupés à **0,0 exact sur les 4 runs**
  (`maxsep_888_verify.json`, verdict OK). Second calcul
  indépendant des écarts `d_maxsep` depuis les
  `master_results.json` : −0,0239 / +0,0517 / +0,0354,
  identiques à l'extraction (écart 0,0 exact).
- **Tests directs :** d de Cohen marginal = 0,0000 pour les
  11 gènes (moyenne des |d| 3,24×10⁻¹⁷, maximum 9,81×10⁻¹⁷)
  — attendu vacueux par construction (permutation des lignes).
  Spearman contre le pas : Δρ médian +0,1908, 9/11 positifs,
  |ρ| moyen réel 0,1790 contre nul 0,0764.
- **Annexe PDAC-seul (§10.3 du protocole) :** n = 75 lignées
  `CAS-DAC-*`, ρ médiane +0,0816, 8/11 positifs, |ρ| moyen
  0,1609 (`annexe_pdac_seul_888.json`).

## 5. Indépendance

- Jamais courue comme paire pipeline avant ce chantier (grep
  livre blanc §6 du protocole + absence des fichiers `886`).
- Patients distincts par construction de programme : biobanque
  PDPCO de Shanghai (Changhai Hospital, Second Military Medical
  University), chirurgie ou EUS-FNA, identifiants `CAS-*` /
  `NPC-*` — sans recouvrement possible par jointure avec les
  cohortes tenues (barres TCGA, GSM GEO des autres séries,
  ICGC). Aucun lien documenté avec TCGA PAAD, ICGC PACA-AU,
  GSE71729, GSE62452, GSE62165, GSE21501, GSE79668, GSE60979,
  GSE131050, GSE57495, ni avec les organoïdes GDC HCMI (§8.79),
  ni avec les PDO de Chen et al. 2025 (46 PDO, autre article),
  ni avec Tiriac et al. 2018 (CSHL).
- **Limite déclarée :** aucun identifiant commun n'existe entre
  les systèmes, donc le non-recouvrement est établi par
  programme, par système d'identifiants et par absence de tout
  lien documenté — c'est une limite, pas une preuve formelle
  (même caveat que §8.79 §2.2 point 2 et §8.86 §2.4).
- La dérogation à 11 flux ne crée pas une dépendance : DPCR1
  est absent du fichier déposé sous tout nom, aucun remappage
  n'est fait, et aucune autre cohorte du projet n'a utilisé
  GSE194249 comme paire.

## 6. Ce qui manque / limites

- **Cause exacte de l'absence de DPCR1 non établie :** le gène
  n'est dans le fichier déposé sous aucun des deux symboles
  (DPCR1 : 0 ; MUCL3 : 0). Compatible avec le filtre des
  auteurs (FPKM < 1 dans les 87 échantillons, Méthodes p. 12),
  mais les valeurs FPKM par gène de DPCR1/MUCL3 ne sont pas
  dans le fichier déposé — le filtre ne peut pas être vérifié
  gène par gène. L'absence est un fait du fichier déposé ; sa
  cause exacte reste une hypothèse (comme au §8.86).
- **Écart 15 609 / 15 819 :** les Méthodes annoncent 15 819
  gènes protéiques restants après filtre ; la matrice déposée
  en compte 15 609 — écart de 210 gènes, non élucidé (version
  du dépôt, annotation, ou autre — non tranché ici, comme au
  §8.86).
- **Comparabilité limitée aux paires à 12 flux :** la paire
  compte 11 flux, pas 12 — le caveat « 11 flux, DPCR1 absent »
  est écrit dans le verdict, la table A2 et cette provenance.
  Toute lecture future qui présenterait cette paire comme une
  paire à 12 flux serait fausse.
- Les suppléments de réponse aux médicaments (Suppl. Data 8,
  MOESM11) et de suivi clinique (Suppl. Data 10, MOESM13) n'ont
  PAS été téléchargés (hors périmètre de la paire, §4.1 du
  protocole) ; le n de réponse exact reste donc non vérifié,
  comme au §8.78 et au §8.86.
- Les 6 NPOs établis par l'article ne sont que 3 dans GEO
  (`NPC-4/5/7`) — les 3 autres ne sont pas dans la série
  déposée ; sans objet ici (normaux exclus de toute façon).
- La page GEO directe n'a pas pu être lue (reCAPTCHA) ;
  les métadonnées GEO viennent de l'API E-utilities, dont la
  réponse est conservée et hashée (§2).
- **Divergence non élucidée :** `maxsep` échoue (−0,0239)
  alors que le signal d'ordre direct est positif (Δρ médian
  +0,191, 9/11) — miroir du §8.85. Aucune décomposition ne
  tranche ici ; c'est consigné tel quel, pas expliqué.

## 7. Fichiers du chantier

- `PROTOCOL_gse194249_11flux_888.md` — SHA
  `f5eb1f952f562499e6ff31036b684cb75d094a2843a17a067acf27ca7c763e02`.
- `PROVENANCE_888.md` — ce fichier.
- `build_fluxes_888.py` — SHA
  `f598c4b464db90b0394a1e1511115161526b183b229f292854f3391edfbd5e70`.
- `build_fluxes_888_audit.json` — SHA
  `7e30cdb03a5f40f03a867bba9bbc9a24f9c28e219e5ae25d783a0471e281bc13`.
- `pdac_888_gse194249_fluxes.csv` — SHA
  `7799a62a6c1145b728e60a2d1126a93b86c28123744c0dc904e454c35ae9aeda`.
- `pdac_888_gse194249_fluxes_nul.csv` (graine 42) — SHA
  `2f633871d068ceaa7152f10d1190ecb7ca4a58eef0d3e4cfb3a9ad322db44569`.
- `pdac_888_gse194249_fluxes_nul_s8881.csv` — SHA
  `f95b7cc4add9f23963d476a939ee9b66317f720eaa12f92e331c184a44388f49`.
- `pdac_888_gse194249_fluxes_nul_s8882.csv` — SHA
  `78b1f280d8409b04fe92f7509c8291c718c3acb634c73a61f6b5da2fa4829950`.
- `manifest_v62_888.txt` — SHA
  `77538d050b80e9f63982bf33ac513f14d78a3e02b3779f6a151e2de6405aaa80`.
- `manifest_v62_888_frais.txt` — SHA
  `48f841c799706257a34318d05268b9c7f5e6010167a92f32d919c42d8306192d`.
- `runs_v62_888.log` — SHA
  `35aa2a01f6b6c820afde80df22eba5830c9b9148c62f5f7c7acac9ca01478fc7`.
- `runs_v62_888_frais.log` — SHA
  `513d439125f20e2abdafc6f08ae3d4d6bb867e10ba976352cb60cd374d25a1d5`.
- `results_fast_v62_888_gse194249`,
  `results_fast_v62_888_gse194249_nul`,
  `results_fast_v62_888_gse194249_nul_s8881`,
  `results_fast_v62_888_gse194249_nul_s8882` (4/4 exit 0).
- `extract_888.py` — SHA
  `3dc9ff8b40f9d0fb2afe9c1cfb8047ee05d69643338b704f593fd746f296681d`.
- `extract_888.json` — SHA
  `ad34293d02661f43070aac97921ba21aa4f9ab020f11691762763368a6ebe0dc`.
- `extract_888.csv` — SHA
  `52f2feb8f1c44b4825c77cd27987d23b5d57b72b089218f912ff0f0e87146f64`.
- `verify_888.py` — SHA
  `689f0463a2c2dbfd871f3c81adc62452f39e6358155af7c9120ebc268659c6f7`.
- `maxsep_888_verify.json` — SHA
  `53aeadc4675516676f822459d56b9929a1da310218e4b8926912b4783530db27`.
- `direct_tests_888.py` — SHA
  `ec93dcfdcb4c5f04dbc59ac17fe25b7e04aee9f216e441a2822f582cc2486a39`.
- `direct_tests_888.json` — SHA
  `92f43c24ee30c2cfeecce3f624d9e6deff293e974c2497d87b05be9c961671b1`.
- `annexe_pdac_seul_888.json` — SHA
  `c724fa849d757b65486f70bdc2e4815ea9460ccfe7e97a38d550b56248b94910`.
- `section_8.88_gse194249_11flux.md` — section (verdict : NON).
- **Fichiers §8.86 réutilisés (originaux intacts) :**
  `data/GSE194249_PDPCOs_FPKM.txt.gz` (SHA `479517fb…0f27`),
  `gse194249_esummary_886.json` (SHA `73934e46…0e`),
  `download_gse194249_886_receipt.json` (SHA `fd9bd625…ea`),
  `PROTOCOL_gse194249_886.md` (SHA `b620238b…1cf`),
  `PROVENANCE_886.md`, `section_8.86_gse194249.md`.

— Fin de la PROVENANCE_888. —
