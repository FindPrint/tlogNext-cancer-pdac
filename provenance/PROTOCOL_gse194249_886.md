# PROTOCOLE GELÉ — §8.86 : GSE194249, ré-audit pour une 14e paire principale indépendante pour `maxsep`

Date : 21 novembre 2026, ~14h00 EST. Chantier §8.86, piste B (suite du §8.79).
Protocole gelé AVANT tout téléchargement de données d'expression (aucun
fichier GEO de GSE194249 n'est détenu localement ; seules des vérifications
de métadonnées — livre blanc, E-utilities NCBI, page article — ont eu lieu
avant ce gel, documentées au §2). Aucun paramètre ne change après les
résultats. Le livre blanc N'EST PAS édité, le PDF N'EST PAS régénéré, rien
n'est poussé sur GitHub dans ce chantier (convention des chantiers ; fusion
par le coordinateur). La section §8.86 est écrite dans un FICHIER SÉPARÉ
(`section_8.86_gse194249.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié ; v6.1
`2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`).
Chemin : `/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`.

Note de cécité (état connu du fichier v6.2, inchangé depuis son
adoption) : un grep `temperature|Onsager|2.269` sur le fichier
retourne 8 occurrences, TOUTES confinées à l'annexe génératrice
d'exemple Ising (fonction `generate_example_ising_csv`, marquée
« EXEMPLE UNIQUEMENT, hors cœur du pipeline »). Le cœur d'analyse
ne voit ni T ni Tc ; le fichier est celui adopté, SHA vérifié
ci-dessus, jamais modifié.

## 0. Contexte décisionnel — à lire avant tout le reste

- §8.56 : `maxsep` seul SUFFIT aux barres gelées ; `sep` seul
  REJETÉ.
- §8.59 : ADOPTER SOUS CONDITION (D1, D2, D5 passent ; D3 et D4
  échouent). Condition C3 (§8.59.8) : 7 paires passantes au total,
  LOO pire cas à la barre A2 d'origine.
- §8.71 : onzième paire, GSE60979, **CONFIRME** (`d_maxsep =
  +0,2045`) ; A2 étendu **7/11, 9/11 positifs**, LOO 6/10 —
  **C3 LEVÉE**.
- 20 nov. 2026, 13h04 : Zackary a décidé d'**ADOPTER maxsep
  pleinement** (maxsep score principal, MC secondaire, aucun
  changement de code).
- §8.74 : douzième paire, GSE131050 lot Yeh_seq FF (n = 42),
  **CONFIRME** (`d_maxsep = +0,0739`) ; A2 étendu **8/12,
  10/12 positifs**, LOO 7/11. **C3 RESTE LEVÉE.**
- §8.76 : lot Yeh_seq FNA, mêmes tumeurs — test de robustesse
  APPARIÉ, pas une paire (41/42 codes communs) ; A2 INCHANGÉ.
- §8.77 : reproductibilité réparée (19/19 gaps fermés).
- §8.78 : inventaire des dépôts (piste A) — candidate C4,
  GSE194249 (84 PDPCOs), **À VÉRIFIER** : audit scripté,
  sortie d'audit absente du dépôt ; n réponse exact et
  couverture v4 NON vérifiés — audit à refaire depuis GEO.
- §8.79 : treizième paire, GSE57495, **CONFIRME**
  (`d_maxsep = +0,4494`, 11 flux, GSTM1 absent) ; A2 **9/13
  au-dessus du plancher, 11/13 positifs**, LOO 8/12. **C3
  RESTE LEVÉE.** La candidate C2 (GDC ORGANOID-PANCREATIC)
  y est arrêtée : DPCR1 absent de 55/55 fichiers (symbole
  retiré de GENCODE v36, devenu MUCL3) — aucun remappage.
- **Ce chantier ne rouvre pas C3, quelle que soit son issue.**
  Si la paire passe, elle consolide l'adoption par une
  quatorzième paire indépendante ; si elle échoue, l'adoption
  pleine reste la décision de Zackary du 20 nov. 13h04 — à dire
  plainement dans les deux cas, dans la section comme dans le
  rapport. Ce chantier ne rouvre pas les §8.56/§8.59/§8.64/
  §8.69/§8.70/§8.71/§8.74/§8.76/§8.79 et ne change aucune
  décision de Zackary.
- §8.70/§8.72 : correction de méthode notée au §8.70 (§8.70.5,
  §8.70.7) et APPLIQUÉE ici (§9) : le test de Cohen marginal
  est vacueux par construction quand le nul est une permutation
  de lignes (d = 0,0000 pour les 12 gènes) — le test informatif
  est le Spearman de chaque flux contre le pas (Δρ médian,
  nombre de positifs). Le Cohen marginal est quand même rapporté
  (il valide la construction du nul), mais il ne porte aucune
  information d'ordre et ne décide rien.

## 1. Les 13 paires principales indépendantes déjà comptées

Valeurs reprises des §8.56/§8.69/§8.70/§8.71/§8.74/§8.79, jamais
recalculées. Écart = maxsep réel − maxsep nul. Plancher 0,07.

| Paire | maxsep R / N | Écart | > 0,07 ? | Positif ? |
|---|---|---|---|---|
| HP35 | 1,7718 / 0,1206 | **+1,6512** | oui | oui |
| TCGA v4 | 0,4623 / 0,1696 | **+0,2928** | oui | oui |
| GSE71729 | 0,2593 / 0,2191 | +0,0402 | non | oui |
| GSE62452 | 0,3100 / 0,3136 | −0,0036 | non | NON |
| ICGC | 0,4080 / 0,3110 | **+0,0970** | oui | oui |
| Immunitaire TCGA | 0,5309 / 0,1634 | **+0,3675** | oui | oui |
| PARP TCGA | 0,3680 / 0,1992 | **+0,1688** | oui | oui |
| DepMap | 0,4436 / 0,2532 | **+0,1904** | oui | oui |
| GSE21501 (§8.69) | 0,2121 / 0,2221 | −0,0100 | non | NON |
| GSE79668 (§8.70) | 0,4104 / 0,3538 | +0,0567 | non | oui |
| GSE60979 (§8.71) | 0,4418 / 0,2373 | **+0,2045** | oui | oui |
| GSE131050 Yeh FF (§8.74) | 0,3220 / 0,2481 | **+0,0739** | oui | oui |
| GSE57495 (§8.79, 11 flux) | 0,6381 / 0,1887 | **+0,4494** | oui | oui |

Bilan : **9/13 au-dessus du plancher, 11/13 positifs.** LOO
8/12. Rotations V2 (48 paires, §8.44, sans doublon) : 37/48
pour `maxsep`. Elles ne sont PAS rejouées ici.

## 2. Ce qui est déjà connu sur GSE194249 avant le gel (vérifications de métadonnées seulement, aucune donnée d'expression lue)

### 2.1 Livre blanc (§8.78, C4) — repris tel quel

- Série GSE194249, 84 PDPCOs (organoïdes dérivés de patients
  pancréatiques), article DOI 10.1038/s41467-022-29857-6 (CC BY 4.0).
- Plateforme : FPKM (matrice `GSE194249_PDPCOs_FPKM.txt.gz`) +
  réponse aux médicaments (Suppl. Data 8, MOESM11) + suivi
  clinique (Suppl. Data 10, MOESM13) + cohorte 84 PDPCOs
  (Suppl. Data 1, MOESM4).
- n : expression 84 PDPCOs (colonnes exactes non versées) ;
  n réponse médicamenteuse < 50 sous le minimum v5.9.4 fast —
  le nombre exact n'est PAS vérifiable depuis le dépôt : le
  script d'audit (`audit_GSE194249_candidate.py`, SHA
  `ae3c85cd…`) existe, mais son dossier de sortie
  `candidate_GSE194249_sources/` (avec
  `CANDIDATE_DATA_AUDIT.json/.md`) est ABSENT du dépôt
  `universal-log-research`. Gènes v4 : NON VÉRIFIÉS.
- Statut au §8.78 : candidate conditionnelle à la vérification
  de n et de la couverture v4 — ne pas lancer sans l'audit
  refait et gelé. **Le présent protocole EST cet audit refait.**

### 2.2 NCBI E-utilities, esummary GDS (métadonnées, 21 nov. 2026)

Requête `esummary.fcgi?db=gds&id=200194249&retmode=json`,
réponse conservée `gse194249_esummary_886.json`, SHA-256
`73934e46a717a5db1ed8cd8e1c4349435683a0eed1dda85fe7b097ec448f460e`
(métadonnées, pas des données d'expression) :

- Titre : « Integrated profiling of human pancreatic cancer
  organoids reveals chromatin accessibility features associated
  with drug sensitivity ».
- Accession GSE194249, plateforme GPL31265, date de dépôt
  2022/02/23, `Homo sapiens`, « Expression profiling by high
  throughput sequencing », fichier supplémentaire de type TXT.
- **87 échantillons (GSM) listés**, titres :
  - 75 `CAS-DAC-*` (PDAC) ;
  - 4 `CAS-NEN-*` (néoplasmes neuroendocriniens) ;
  - 4 `CAS-IPMN-*` (tumeurs intracanalaires papillaires
    mucineuses) ;
  - 1 `CAS-ACC-1` (carcinome à cellules acinaires) ;
  - 3 `NPC-4`, `NPC-5`, `NPC-7` (normaux — « NPC »,
    normal pancreatic cells/organoids).
- Soit **84 PDPCOs** (75 + 4 + 4 + 1) + 3 normaux = 87 GSM.
  Ce décompte est cohérent avec l'article (voir §2.3) et
  avec le nom de la matrice (`…_PDPCOs_FPKM.txt.gz`).

### 2.3 Article (Shi et al., Nat. Commun. 2022, 13:2169)

DOI 10.1038/s41467-022-29857-6, consulté via la page
Nature Communications (résumé et résultats, 21 nov. 2026) :

- 84 lignées PDPCO établies à partir d'échantillons prélevés
  par chirurgie ou biopsie EUS-FNA : 80 lignes de 99 patients
  atteints de tumeurs exocrines (80,80 %) et 4 lignes de 39
  patients atteints de tumeurs neuroendocrines (10,26 %).
- Types pathologiques des tumeurs d'origine : **75 PDAC,
  4 IPMN, 1 ACC, 4 NEN**. 6 organoïdes ductaux pancréatiques
  normaux (NPO) établis en plus.
- Chaque PDPCO est caractérisée par WGS, RNA-seq, ATAC-seq et
  criblage de sensibilité aux médicaments (283 composés
  épigénétiques + 5 chimiothérapies).
- Auteurs (premiers, contribution égale) : Xiaohan Shi,
  Yunguang Li, Qiuyue Yuan, Shijie Tang, Shiwei Guo.

### 2.4 Indépendance — vérifiée par grep AVANT le gel

- Livre blanc (§8.1–§8.83) : « GSE194249 » apparaît
  uniquement au §8.78 (inventaire C4) et au §8.79.9
  (piste ouverte (d)) — jamais comme cohorte courue,
  jamais comme holdout, jamais comme valeur `maxsep`.
  « PDPCO » : 6 occurrences, toutes au §8.78. « CAS-DAC » :
  0 occurrence. « Shi et al » (Nat Commun 2022) : 0
  occurrence hors §8.78.
- Jamais courue : aucun CSV de flux, aucun run, aucun JSON,
  aucune valeur `maxsep` n'existe pour GSE194249 dans ce
  projet.
- Patients distincts par construction de programme : biobanque
  PDPCO de Shanghai (Second Military Medical University),
  échantillons prélevés par chirurgie ou EUS-FNA, identifiants
  `CAS-DAC-*` / `CAS-NEN-*` / `CAS-IPMN-*` / `CAS-ACC-1` /
  `NPC-*` — système d'identifiants sans aucun recouvrement
  possible par jointure avec les cohortes tenues (barres
  TCGA `TCGA-XX-XXXX`, GSM GEO des autres séries, ICGC).
  Aucun lien documenté avec TCGA PAAD, ICGC PACA-AU,
  GSE71729, GSE62452, GSE62165, GSE21501, GSE79668,
  GSE60979, GSE131050, GSE57495, ni avec les organoïdes
  GDC HCMI (programme américain distinct, §8.79), ni avec
  les PDO de Chen et al. 2025 (autre article, autre cohorte,
  46 PDO), ni avec Tiriac et al. 2018 (CSHL).
  **Limite déclarée :** aucun identifiant commun n'existe
  entre les deux systèmes, donc le non-recouvrement ne peut
  pas être prouvé par une jointure d'identifiants — il est
  établi par programme, par système d'identifiants et par
  absence de tout lien documenté ; c'est une limite, pas une
  preuve formelle. (Même caveat que §8.79 §2.2 point 2.)
- Pas un re-test déguisé : ni une relecture d'un JSON
  existant, ni une rotation déjà comptée, ni un sous-ensemble
  d'une paire V1, ni un nouvel ordre sur des CSV existants
  (nouveaux CSV, nouveaux runs, 2 runs v6.2 frais, données
  jamais courues).
- Statut de la cohorte : transversale, ordonnée par un flux
  (KRAS, comme TCGA/ICGC) — même statut que les paires
  TCGA/ICGC, pas de pseudo-temps. Les PDPCO sont des modèles
  organoïdes dérivés de patients, pas des tumeurs primaires
  directes : c'est dit plainement au §8.86, et le verdict
  porte sur l'instrument, pas sur une affirmation clinique.
- **Composition histologique gelée comme limite :** la série
  déposée compte 75 PDAC et 9 autres tumeurs (4 NEN, 4 IPMN,
  1 ACC). La cohorte primaire est la série déposée entière
  (§4.3) ; la mixité est déclarée, et une annexe descriptive
  PDAC-seul est pré-enregistrée (§9.3) — elle ne décide rien.

## 3. Arrêt borné — AUCUNE cohorte de repli courue dans ce chantier

**Une seule cohorte dans ce chantier : GSE194249, lignées
PDPCO de la matrice FPKM déposée, n attendu = 84.** Si elle
est INUTILISABLE selon les critères d'acceptation du §5
(fichier supplémentaire absent ou illisible, n PDPCO < 40,
KRAS absent, < 12 gènes v4 mappés, < 40 cas complets, mise
en page non couverte par le §4.2), le chantier s'arrête sur
un blocage documenté : section §8.86 écrite quand même, avec
les tentatives chiffrées, aucune valeur inventée, et la piste
fermée (les candidates restantes — C1 lot drogue Chen 2025,
C2 GDC sous protocole MUCL3 futur — sont nommées comme
pistes seulement, aucun run lancé pour elles dans ce
chantier). Il n'y a PAS de cohorte #2 courue dans ce chantier.

## 4. Construction des flux — variante (a), comme les paires GEO V1

Nouveau script `build_fluxes_886.py`. Préfixe `_886_` pour tous
les fichiers du chantier.

### 4.1 Source et téléchargement (APRÈS ce gel)

- Fichier : `GSE194249_PDPCOs_FPKM.txt.gz` (nom attendu, §8.78),
  URL GEO FTP :
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194249/suppl/GSE194249_PDPCOs_FPKM.txt.gz`
  (miroir HTTPS du FTP GEO ; si l'URL HTTPS échoue, même chemin
  en `ftp://`, consigné tel quel).
- Destination : `data/GSE194249_PDPCOs_FPKM.txt.gz`. Taille et
  SHA-256 consignés au téléchargement (aucun SHA attendu
  pré-connu : GEO ne publie pas de SHA pour ce fichier ; la
  vérification est l'intégrité gzip + les comptages du §5).
- Les suppléments de réponse aux médicaments (Suppl. Data 8,
  MOESM11) et de suivi clinique (Suppl. Data 10, MOESM13) ne
  sont PAS téléchargés : la paire utilise l'expression seule
  (le n de réponse < 50 du §8.78 est hors périmètre ici).
- La matrice série (`GSE194249_series_matrix.txt.gz`) n'est
  PAS téléchargée : les titres GSM viennent de l'esummary
  pré-gel (§2.2), suffisant pour la composition et l'exclusion
  des normaux.

### 4.2 Mise en page attendue et règles gelées

La mise en page exacte du fichier n'est pas connue avant
téléchargement (le §8.78 ne la décrit pas). Deux mises en
page sont autorisées, les seules standard pour une matrice
supplémentaire GEO :

- (A) première colonne = symbole de gène (exact, sensible à
  la casse), colonnes suivantes = échantillons GSM ;
- (B) première colonne = identifiant Ensembl, deuxième
  colonne = symbole de gène, colonnes suivantes = échantillons.

Si le fichier ne correspond ni à (A) ni à (B) (par exemple
première colonne = identifiant sans symbole nulle part),
la construction S'ARRÊTE (§3) et la mise en page est
consignée verbatim (première ligne d'en-tête, nombre de
colonnes) — aucune improvisation de mapping.

- Valeurs : **FPKM telles que déposées**, aucune
  renormalisation, aucune transformation log, aucune
  imputation ajoutée.
- Symboles dupliqués : agrégés par **médiane** (précédent
  §8.79, GSE57495) — règle gelée avant de voir les doublons.
- Colonnes : attendues = GSM des 87 échantillons (§2.2).
  Toute colonne dont le GSM correspond à un titre `NPC-*`
  (normal) est **EXCLUE** et comptée (attendu : 3 colonnes
  exclues si la matrice les contient ; 0 si la matrice ne
  contient que les 84 PDPCOs, comme son nom l'indique).
  Toute autre colonne non-PDPCO serait exclue de la même
  façon et nommée. Les colonnes retenues sont les PDPCOs.

### 4.3 Série réelle (variante (a))

- Gènes v4 (les 12 mêmes que TCGA v4, ordre de la liste) :
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1,
  CEACAM5, CLCA1, MUC16.
- Contrôle : KRAS (expression FPKM, croissant). Le contrôle
  n'est JAMAIS un flux : pas de doublon. Justification de
  l'ordre KRAS : identique aux paires principales V1 — KRAS
  est le contrôle monotone du projet, et l'ordre par son
  expression est celui de toutes les paires GEO à 12 gènes.
- Lignes retenues : les **PDPCOs de la matrice** (attendu
  84) ; les normaux `NPC-*` sont exclus et comptés (§4.2).
- **Unité = lignée organoïde.** Chaque GSM est une lignée
  distincte d'un patient distinct (article §2.3 : 84 lignes
  de 138 patients sources, une ligne par patient retenu —
  aucune lignée en double d'un même patient n'est documentée
  ; si la matrice révélait des doublons de patient, ils
  seraient nommés tels quels dans la section, sans
  ré-agrégation).
- Cas complets seulement (KRAS + 12 gènes présents), jamais
  d'imputation. Attendu : 84/84 cas complets (0 NaN attendu
  sur les 13 lignes × 84 colonnes — vérifié, sinon ARRÊT
  si < 40 complets).
- Tri : KRAS FPKM croissant ; `step` = rang 0..n−1.
- Sorties : `pdac_886_gse194249_fluxes.csv` (+ `_nul.csv`).
  Colonnes : `step` + 12 flux. SHA-256 consignés.

### 4.4 Le cas DPCR1 — règle gelée (leçon §8.79, C2)

- DPCR1 est exigé au **symbole exact**. Si DPCR1 est absent
  de la matrice, la présence de MUCL3 (symbole actuel,
  `prev_symbol` DPCR1, HGNC:21666) est vérifiée et rapportée
  **descriptivement seulement** (présent/absent, comptage) —
  **aucun remappage** : la porte « 12 gènes v4 présents »
  dit ARRÊT (§3), comme pour la candidate C2 au §8.79.
  Changer la porte après l'avoir vue échouer serait un
  changement de protocole sans go.

### 4.5 Nul

Bloc des flux permuté par lignes, graine 42, `rng(42)`,
contrôle (ordre KRAS, `step`) intact — même convention que
les paires V1 (§8.56.8, PROTOCOL_phase2 §2). Le nul est un
échantillon hypothétique, pas une mesure.

### 4.6 Nuls frais (conditionnels, §7)

Si et seulement si l'écart mesuré sur la paire graine 42 est
PROCHE du plancher (§7 : `d_maxsep` dans [−0,07 ; +0,14[),
2 nuls frais sont construits par la même méthode, graines
**8861** et **8862** (graines jamais utilisées dans ce projet,
gelées ici avant tout run), et courus en runs frais
(`pdac_886_gse194249_fluxes_nul_s8861.csv`,
`pdac_886_gse194249_fluxes_nul_s8862.csv`,
`results_fast_v62_886_gse194249_nul_s8861`,
`results_fast_v62_886_gse194249_nul_s8862`). Le verdict
reste celui de la paire graine 42 (§7) ; les nuls frais sont
un contrôle de robustesse descriptif (min / médiane / max des
écarts), jamais un moyen de choisir le nul qui arrange.

## 5. Critères d'acceptation de la cohorte (vérifiés sur le fichier téléchargé, avant construction)

- Fichier `GSE194249_PDPCOs_FPKM.txt.gz` téléchargé, gzip
  intègre, taille et SHA-256 consignés ; sinon ARRÊT (§3).
- Mise en page = (A) ou (B) du §4.2 ; sinon ARRÊT (§3).
- n ≥ 40 colonnes PDPCO retenues (après exclusion des
  normaux `NPC-*`) ; sinon ARRÊT (§3).
- Aucune colonne porteuse d'un code-barres TCGA ou déjà
  présente dans une cohorte du projet (vérifié par les titres
  GSM §2.2 : `CAS-*` / `NPC-*` uniquement) ; sinon ARRÊT (§3).
  (Caveat §2.4 : le non-recouvrement est établi par programme
  et système d'identifiants, pas par jointure.)
- KRAS présent comme ligne mappée (symbole exact) dans la
  matrice ; sinon ARRÊT (§3).
- Les 12 gènes v4 présents (une ligne chacun après agrégation
  des doublons par médiane, symbole exact) ; sinon ARRÊT (§3)
  (aucun gène remplacé, aucun absent toléré pour une paire
  comparable à 12 flux).
- Cas complets (KRAS + 12 gènes) ≥ 40 ; sinon ARRÊT (§3).

## 6. Runs v6.2 (mode fast)

- Lot : 2 runs — réel + nul — manifeste `manifest_v62_886.txt`,
  lanceur reprenable existant `run_v62_lot.sh` (saute les sorties
  déjà complètes), journal `runs_v62_886.log` (SHA du pipeline
  en tête, exits consignés).
- Dossiers : `results_fast_v62_886_gse194249` et
  `results_fast_v62_886_gse194249_nul` (nuls frais éventuels :
  `results_fast_v62_886_gse194249_nul_s8861` /
  `..._s8862`).
- Lancement en `systemd-run --unit=v62-886 --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance qui
  s'arrête d'elle-même à 2/2 (ou 4/4 si nuls frais). Ne JAMAIS
  supprimer le dossier d'un run en cours. Si la machine
  redémarre, reprise sans perte (SKIP des dossiers complets,
  jamais de relance à l'aveugle).
- SHA du pipeline revérifié avant ET après le lot.
- Durée attendue : ~2–3 min par run (référence §8.76 :
  n=42, 12 flux, ~2 min/run ; ici n=84, prévoir ~5 min/run) ;
  le lot complet tient en ~15 min hors téléchargement.

## 7. Critère de passage — GELÉ avant tout run

**La paire PASSE si et seulement si :**
`d_maxsep = maxsep_R − maxsep_N > 0,07` (plancher, en unités |d|,
gigue_eff = max(gigue mesurée, 0,07) — v6.2 déterministe, gigue
attendue 0, comme §8.56 §3) **ET** `d_maxsep > 0` (positif —
impliqué par > 0,07, mais consigné séparément comme au §8.56).

`maxsep` = `best_config.metrics.max_separation`, |d de Cohen|
maximal du scan, lu sur le best_config ANCIEN (sélection par
l'ancien composite) — mêmes définitions que §8.56.2. Le seuil MC,
la cascade, S_sep, Delta, L7a sont inchangés par construction.

**Catégories de verdict (gelées) :**
- **CONFIRME** : `d_maxsep > 0,07` — quatorzième paire
  indépendante passante.
- **PARTIEL** : `0 < d_maxsep ≤ 0,07` — positif mais sous le
  plancher (même catégorie que GSE71729, +0,0402, et GSE79668,
  +0,0567).
- **NON** : `d_maxsep ≤ 0` — négatif ou nul (même catégorie que
  GSE62452 et GSE21501).

**Ce que le verdict change (gelé) :**
- Si CONFIRME : A2 devient **10/14 au-dessus du plancher** (et
  12/14 positifs) ; LOO recalculé sur 14 paires (pire cas sur 13).
- Si PARTIEL : A2 devient **9/14 au-dessus du plancher,
  12/14 positifs** ; LOO recalculé sur 14 paires.
- Si NON : A2 devient **9/14 au-dessus du plancher,
  11/14 positifs** ; LOO recalculé sur 14 paires.
- Dans tous les cas, la paire entre dans le compte A2 : c'est
  une paire principale indépendante (contrairement au lot FNA
  §8.76, apparié). **C3 reste LEVÉE** dans tous les cas — elle
  l'était déjà depuis le §8.71 ; ce chantier est une
  consolidation supplémentaire, pas une condition.
- Le leave-one-out sur les paires indépendantes est recalculé
  ici (il change : la paire y entre).

**Nuls frais (§4.6, règle gelée).** La paire graine 42 fait le
verdict, dans tous les cas. Si `d_maxsep` est PROCHE du
plancher — défini ici comme `d_maxsep` dans [−0,07 ; +0,14[,
soit à moins d'une largeur de plancher du seuil, de part et
d'autre — les 2 nuls frais (graines 8861, 8862) sont courus et
les écarts `d` contre chaque nul frais sont rapportés
(min / médiane / max des 3 écarts). Lecture gelée : si les
3 écarts sont > 0,07, le passage est dit « consolidé » ; si
l'un des 3 est ≤ 0,07, le passage (ou l'échec) est dit
« fragile, non consolidé » — le verdict de la paire graine 42
n'est JAMAIS changé par les nuls frais. Si `d_maxsep` est
hors de [−0,07 ; +0,14[, aucun nul frais n'est couru.

**Contrôles descriptifs (à publier, ne décident pas) :**
- `sep` compagnon (= maxsep/(1+maxsep)), ancien MC (secondaire),
  S_sep, Delta, L7a, cascade, falsification — affichés selon
  la convention §8.64.6 (maxsep principal, ancien MC secondaire,
  sep compagnon, mention de fragilité en tête de table).
- Falsification : INDISPONIBLE sous n = 75 — GSE194249
  n attendu = 84 : **disponible en principe** (n ≥ 75) ;
  si n retenu < 75, noter « indisponible », ne pas imputer.
  (Si n = 84, la falsification est lue telle quelle, comme
  aux paires à n ≥ 75.)
- Plancher équivalent-sep (descriptif) : la paire passe-t-elle
  aussi `0,07·(1+m_R)(1+m_N)` ? Rapporté, non décisif (D4 n'est
  pas rejoué ici : il porte sur les paires V1, déjà tranché).
- Aucun autre critère, aucune repondération, aucune redéfinition
  du plancher après avoir vu les chiffres.

## 8. Extraction et vérification

1. Extracteur propre du chantier, `extract_886.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_866.py` / `extract_869.py` / `extract_871.py` /
   `extract_874.py` / `extract_876.py` / `extract_879_c3.py`) ;
   lit `maxsep`, `mc_score`, `stability`, `ssep`, `delta`, `l7a`,
   cascade, falsification dans les 2 (ou 4) `master_results.json` ;
   sorties `extract_886.json` / `extract_886.csv`.
2. Second calcul indépendant : relecture directe des
   `master_results.json` par un chemin distinct (script
   `verify_886.py`, SHA noté) — `maxsep` et ancien MC recoupés
   à 0,0 exact ; tout écart = résultat à diagnostiquer, pas un
   bruit.
3. Recoupements : les 13 valeurs déjà comptées reprises telles
   quelles du §8.56 (table `sep_maxsep_856_table.json`, SHA
   `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`),
   du §8.69 (`extract_869.json`, SHA
   `644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b`),
   du §8.70 (`extract_870.json`, SHA
   `4ffa851a83668b2369097703862e0413ff9af54af3a66ef70aea9333b40c444f`),
   du §8.71 (`extract_871.json`, SHA
   `85e9089a…55e3b`) et du §8.74 (`extract_874.json`, SHA
   `82ade74701245021dfdb965bdc689ac98262c70f12ecec7f39e1b5b742dfcb47`)
   et du §8.79 (`extract_879_c3.json`, valeurs §8.79.2),
   jamais recalculées ici — ce chantier ne re-vérifie pas les
   §8.56/§8.59/§8.64/§8.69/§8.70/§8.71/§8.74/§8.76/§8.79 (déjà clos).
4. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 9. Tests directs en appui (ne décident pas)

Script `direct_tests_886.py` (SHA noté), sur les CSV de flux
du chantier (réel + nul graine 42) :
1. **Test informatif (correction §8.70, appliquée ici) :**
   corrélation de Spearman de chaque flux avec le pas (ordre
   KRAS), réel vs nul : |ρ| moyen, Δρ médian, nombre de Δρ
   positifs (sur 12), table complète sans sélection. C'est le
   test qui porte l'information d'ordre.
2. d de Cohen marginal des 12 flux (réel vs nul) : pour chaque
   gène v4, moyenne et écart-type des valeurs ordonnées, d de
   Cohen réel−nul ; table complète, sans sélection. **Attendu
   vacueux par construction : d = 0,0000 pour les 12 gènes**
   (le nul est une permutation des lignes, chaque flux garde
   exactement ses n valeurs). Rapporté tel quel : il valide
   la construction du nul (marginales préservées exactement),
   il ne mesure pas la séparation.
3. Comparaison descriptive avec les paires précédentes
   (Δρ médian, 11/11 positifs au §8.79 ; valeurs reprises
   telles quelles, jamais recalculées). Si le signal d'ordre
   est plus faible, c'est consigné tel quel, sans être élucidé
   sans preuve ; si une divergence Delta/`maxsep` apparaît
   ici, elle est nommée telle quelle.
4. Aucun de ces tests ne change le verdict du §7.

### 9.3 Annexe descriptive pré-enregistrée — PDAC seul (ne décide rien, aucun run)

Parce que la série déposée compte 9 lignées non-PDAC sur 84
(4 NEN, 4 IPMN, 1 ACC — §2.4), une annexe descriptive est
pré-enregistrée : sur les valeurs FPKM de la matrice
téléchargée, Spearman de chaque flux contre le rang KRAS
**au sein des seules lignées `CAS-DAC-*`** (n attendu 75),
réel seulement (pas de nul, pas de run pipeline). Rapportée
comme table complète (12 Δρ non applicables — ρ PDAC-seul
par gène, médiane, nombre de positifs), elle répond à la
question « le signal d'ordre survit-il sans les 9 lignées
non-PDAC ? » sans toucher au verdict du §7, qui reste celui
de la paire sur les 84 PDPCOs. Aucune autre découpe
histologique n'est calculée.

## 10. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et le
  jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict : les résultats des autres dépôts (écran du 20 nov.,
  holdout GSE57495, pilote Chen, article Shi et al. lui-même —
  sous-types, pics ATAC, signature de sensibilité) ne prédisent
  rien ici — seul l'écart `maxsep` mesuré sur les runs du présent
  chantier fait le verdict.
- Un nul qui invalide une piste est un résultat ; un échec du lot
  est un verdict, pas un échec caché.
- Ne jamais présenter une lecture préliminaire comme un verdict.
- Aucun consensus exigé entre flux ou contrôles ; aucune
  affirmation clinique — l'étude porte sur l'instrument.
- **Compter cette paire comme quatorzième paire indépendante
  UNIQUEMENT si les portes du §5 sont passées** (n PDPCO ≥ 40,
  12/12 gènes, n ≥ 40 cas complets). Toute lecture future qui
  compterait aussi les 3 normaux `NPC-*` serait fausse.

## 11. Livrables

- Ce protocole (gelé avant téléchargement des données et runs).
- `PROVENANCE_886.md` (source, auteur, date, dépôt, URL, SHA-256
  du fichier téléchargé, plateforme, effectifs, exclus,
  identification des gènes, vérifications d'indépendance du §2).
- `download_gse194249_886.py` (téléchargement + vérification
  gzip) + reçu, `build_fluxes_886.py` + CSV de flux
  (`pdac_886_*`, SHA consignés).
- `manifest_v62_886.txt`, `runs_v62_886.log`, dossiers
  `results_fast_v62_886_*`, `extract_886.json` / `.csv`,
  `verify_886.py` + sortie de vérification,
  `direct_tests_886.py` + sortie.
- §8.86 dans le FICHIER SÉPARÉ
  `section_8.86_gse194249.md` (verdict d'abord, une phrase :
  CONFIRME / PARTIEL / NON ; chiffres ensuite ; détail complet
  après ; provenance nommée partout ; C3 reste levée dans tous
  les cas ; A2 recalculé sur 14 paires, dit explicitement).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin du protocole gelé §8.86. —
