# PROTOCOLE GELÉ — §8.85 : GDC ORGANOID-PANCREATIC avec remappage DPCR1 → MUCL3, 14e paire principale indépendante pour `maxsep`

Date : 21 novembre 2026, ~08h55 EST. Chantier §8.85, piste 2 du lot
du 21 nov. 2026.
Protocole gelé AVANT toute vérification de remappage exécutée
dans ce chantier, avant toute construction de matrice et avant
tout run. Aucun paramètre ne change après les résultats.
Le livre blanc N'EST PAS édité, le PDF N'EST PAS régénéré, rien
n'est poussé sur GitHub dans ce chantier (convention des
chantiers ; fusion par le coordinateur). La section §8.85 est
écrite dans un FICHIER SÉPARÉ (`section_8.85_gdc_mucl3.md`).
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
- 20 nov. 2026, 13h04 : Zackary a décidé d'**ADOPTER maxsep
  pleinement** (maxsep score principal, MC secondaire, aucun
  changement de code).
- §8.79 : treizième paire, GSE57495, **CONFIRME**
  (`d_maxsep = +0,2045` au §8.71 ; `+0,4494` au §8.79) ; A2
  étendu **9/13, 11/13 positifs**, LOO 8/12. **C3 RESTE LEVÉE.**
- §8.79.9 (c) — la piste du présent chantier, écrite d'avance :
  « la candidate C2 (GDC ORGANOID-PANCREATIC) reste utilisable
  sous un protocole futur qui pré-enregistrerait MUCL3 à la
  place de DPCR1 — les 55 TSV vérifiés sont détenus ».
  Le présent protocole EST ce protocole futur. Il ne rouvre
  pas le §8.79 : la porte C2 y disait ARRÊT sous le protocole
  gelé d'alors (symbole exact DPCR1, aucun gène mappé à la
  main) ; le présent chantier pré-enregistre explicitement le
  remappage, ce qui est un autre protocole, pas un changement
  rétroactif du §8.79.
- §8.70/§8.72 : correction de méthode notée au §8.70 (§8.70.5,
  §8.70.7) et APPLIQUÉE ici (§9) : le test de Cohen marginal
  est vacueux par construction quand le nul est une permutation
  de lignes (d = 0,0000 pour les 12 gènes) — le test informatif
  est le Spearman de chaque flux contre le pas (Δρ médian,
  nombre de positifs). Le Cohen marginal est quand même rapporté
  (il valide la construction du nul), mais il ne porte aucune
  information d'ordre et ne décide rien.
- **Ce chantier ne rouvre pas C3, quelle que soit son issue.**
  Si la paire passe, elle consolide l'adoption par une
  quatorzième paire indépendante ; si elle échoue, l'adoption
  pleine reste la décision de Zackary du 20 nov. 13h04 — à dire
  plainement dans les deux cas, dans la section comme dans le
  rapport. Ce chantier ne rouvre pas les §8.56/§8.59/§8.64/
  §8.69/§8.70/§8.71/§8.74/§8.76/§8.79 et ne change aucune
  décision de Zackary.

## 1. Les 13 paires principales indépendantes déjà comptées

Valeurs reprises des §8.56/§8.69/§8.70/§8.71/§8.74/§8.79,
jamais recalculées. Écart = maxsep réel − maxsep nul.
Plancher 0,07.

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

## 2. La candidate : GDC ORGANOID-PANCREATIC, remappage DPCR1 → MUCL3 — et vérifications pré-gel

### 2.1 Ce qui est déjà établi avant ce gel (vérifications de métadonnées seulement, reprises du §8.79)

- Projet GDC `ORGANOID-PANCREATIC` (Human Cancer Models
  Initiative / Next Generation Cancer Models), RNA-seq, STAR
  Counts, accès ouvert, GENCODE v36.
- Manifeste détenu localement :
  `data/GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST_879.tsv`,
  SHA-256 `f713edebf0f8afb20305b1472d480564e45ac31ce79e28350d7dde6ae496220b`
  — re-vérifié avant ce gel, IDENTIQUE au §8.79.
- Les 55 TSV téléchargés au §8.79 sont détenus localement :
  `data/gdc_organoid_879/`, 55 fichiers, total 232 648 892 o
  exact (re-vérifié avant ce gel) ; MD5 conformes au manifeste
  selon `download_gdc_879_receipt.json` (§8.79) — à re-vérifier
  par programme avant construction (§5).
- Association fichier → échantillon (API GDC, §8.79) :
  `gdc_organoid_879_file_sample_map.tsv`, SHA-256
  `282d8b8319dbbc82279fa4bed08fcb7bc34a8fa9a6320ad3be46b443b109594a`
  — **44 fichiers Tumor** (cas « Adenocarcinoma, NOS »,
  38 cas, 3 cas multi-fichiers : 2, 3 et 4 fichiers),
  **11 fichiers Normal** (cas « Unknown », exclus).
- **Aucun CSV C2, aucun run C2** : `pdac_879_gdc_organoid*`
  inexistant sur cette VM (vérifié avant ce gel). La candidate
  n'a JAMAIS été courue comme paire pipeline.
- Comptages de symboles sur les 55 TSV détenus (grep, avant
  ce gel — vérification de métadonnées, pas une construction) :
  **MUCL3 présent dans 55/55 fichiers (1 occurrence chacun),
  DPCR1 absent de 55/55 (0 occurrence).** Ces comptages seront
  re-vérifiés par le script de construction, fichier par
  fichier, sur les 44 tumoraux (§5) — le grep pré-gel ne
  remplace pas les portes.
- Le remappage lui-même n'est PAS vérifié avant ce gel : il
  l'est à l'étape 1 ci-dessous, APRÈS le gel, par des sources
  nommées et lues. Le §8.79 rapporte que HGNC donne DPCR1 en
  `prev_symbol` de MUCL3 — c'est un RÉSULTAT RAPPORTÉ, pas une
  vérification de ce chantier ; il ne fait pas foi ici tant
  qu'il n'a pas été relu.

### 2.2 Indépendance — ce qui est établi avant tout run

1. **Jamais courue.** Aucun CSV de flux, aucun run, aucun JSON,
   aucune valeur `maxsep` n'existe pour GDC
   ORGANOID-PANCREATIC dans ce projet (§2.1).
2. **Patients distincts par construction de programme.** Les 49
   cas sont du projet GDC `ORGANOID-PANCREATIC` (HCMI / Next
   Generation Cancer Models), identifiants de cas UUID GDC et
   `submitter_id` entiers (1–71) — système d'identifiants sans
   aucun recouvrement possible par jointure avec les cohortes
   tenues (barres TCGA `TCGA-XX-XXXX`, GSM GEO, ICGC). Aucun
   `TCGA` dans le manifeste ni dans les cas interrogés. Les
   programmes sont distincts (modèles organoïdes dérivés de
   patients enrôlés pour HCMI, pas la cohorte chirurgicale
   TCGA PAAD).
   **Limite déclarée :** aucun identifiant commun n'existe
   entre les deux systèmes, donc le non-recouvrement ne peut
   pas être prouvé par une jointure d'identifiants — il est
   établi par programme, par système d'identifiants et par
   absence de tout lien documenté ; c'est une limite, pas une
   preuve formelle.
3. **Vérification grep du livre blanc (§8.1–§8.83), avant ce
   gel :** « ORGANOID-PANCREATIC » 14 mentions, toutes au
   §8.79 (arrêt C2 + piste ouverte (c)) ; « MUCL3 » 8 mentions,
   toutes au §8.79 (remappage noté + piste ouverte) ; aucune
   mention dans une autre section, aucun CSV, aucun run, aucune
   valeur `maxsep` pour cette cohorte ailleurs dans le livre
   blanc. La piste ouverte du §8.79.9 (c) est la seule
   antériorité — et c'est elle qui autorise ce chantier.
4. **Pas un re-test déguisé.** Ni une relecture d'un JSON
   existant, ni une rotation déjà comptée, ni un sous-ensemble
   d'une paire V1, ni un nouvel ordre sur des CSV existants
   (nouveaux CSV, nouveaux runs, 2 runs v6.2 frais, données
   jamais courues).
5. **Statut de la cohorte.** Transversale, ordonnée par un flux
   (KRAS, comme TCGA/ICGC) — même statut que les paires
   TCGA/ICGC, pas de pseudo-temps. Les organoïdes sont des
   modèles dérivés de patients, pas des tumeurs primaires
   directes : c'est dit plainement au §8.85, et le verdict
   porte sur l'instrument, pas sur une affirmation clinique.
6. **Le remappage ne crée pas une dépendance.** MUCL3 est le
   symbole actuel du même gène que DPCR1 (§3) : la mesure
   (la ligne du gène dans chaque TSV) est la même que celle
   que le §8.79 a vue sans pouvoir l'utiliser. Aucune autre
   cohorte du projet n'a utilisé MUCL3 comme flux (grep §2.2
   point 3) ; la paire ne réutilise donc aucune mesure déjà
   comptée comme flux.

## 3. ÉTAPE 1 — Vérification du remappage DPCR1 → MUCL3 (après ce gel, avant toute construction)

**But :** établir, par des sources nommées et lues, que DPCR1
est l'ancien symbole du même gène que MUCL3 — et rien d'autre.
Si cette étape échoue, la piste se ferme avec la raison
exacte, sans CSV et sans run (§3.5).

### 3.1 Sources à lire (dans cet ordre, réponses conservées)

1. **HGNC (source primaire de nomenclature), REST :**
   `https://rest.genenames.org/fetch/symbol/MUCL3`
   — lire le champ `prev_symbol` (DPCR1 attendu) et le champ
   `alias_symbol` ; noter `hgnc_id` (21666 attendu, à confirmer
   par la lecture, pas à pré-écrire comme fait), `name`
   (« mucin like 3 » attendu), `status` (Approved attendu),
   `location`, `ensembl_gene_id` le cas échéant.
2. **HGNC, recherche par ancien symbole :**
   `https://rest.genenames.org/fetch/prev_symbol/DPCR1`
   — doit renvoyer MUCL3 (et rien d'autre comme symbole
   approuvé actuel portant DPCR1).
3. **NCBI Gene :** recherche « DPCR1 » puis page du gène
   MUCL3 (URL relevée depuis la recherche, jamais devinée) —
   lire la mention d'alias / « also known as » DPCR1 et
   l'identifiant GeneID.
4. **Ensembl REST :**
   `https://rest.ensembl.org/lookup/symbol/homo_sapiens/MUCL3`
   et `https://rest.ensembl.org/lookup/symbol/homo_sapiens/DPCR1`
   — MUCL3 doit résoudre, DPCR1 ne doit pas résoudre (comme
   au §8.79) ; noter l'`id` Ensembl de MUCL3.
5. **Croisement avec les données détenues :** le `gene_id`
   (Ensembl) de la ligne MUCL3 dans les TSV GDC (GENCODE v36)
   doit être l'`id` Ensembl lu à l'étape 4 (ou l'un des
   identifiants Ensembl du gène selon HGNC/NCBI). Si le
   `gene_id` du TSV ne correspond à aucun identifiant du gène
   MUCL3, la piste se ferme (§3.5).

### 3.2 Critères d'acceptation du remappage (tous exigés)

- (R1) HGNC : DPCR1 figure en `prev_symbol` de MUCL3
  (symbole approuvé actuel, statut Approved).
- (R2) HGNC par ancien symbole : `prev_symbol/DPCR1` renvoie
  MUCL3 comme symbole approuvé — DPCR1 n'est pas le symbole
  approuvé actuel d'un autre gène.
- (R3) NCBI Gene confirme DPCR1 comme alias / ancien nom de
  MUCL3 (ou, à défaut de lecture NCBI, Ensembl confirme
  MUCL3 et l'absence de DPCR1 — le minimum est R1 + R2 + R4 ;
  NCBI est une corroboration, pas une porte bloquante si ses
  pages sont illisibles, et c'est consigné tel quel).
- (R4) Ensembl : MUCL3 résout, DPCR1 ne résout pas.
- (R5) Le `gene_id` de la ligne MUCL3 dans les TSV correspond
  à l'identifiant Ensembl du gène MUCL3 lu aux étapes 1/4.

### 3.3 Ce que le remappage autorise — et ce qu'il n'autorise pas

- Il autorise **une seule chose** : lire la ligne `gene_name =
  MUCL3` des TSV comme la mesure du flux v4 historiquement
  nommé DPCR1. Le flux est nommé **MUCL3 (ex-DPCR1)** dans
  les CSV, les tables et la section — jamais « DPCR1 » seul.
- Il n'autorise aucun autre mappage : les 11 autres gènes v4
  et KRAS sont lus au symbole exact, comme au §8.79 (§4.2).
  Tout autre gène absent = ARRÊT (§5).
- Il ne change pas la nature du flux : c'est le même gène,
  la même ligne de mesure ; la paire reste une paire à
  **12 flux** (11 symboles inchangés + MUCL3), comparable
  aux paires à 12 flux — avec la substitution nommée partout.
  L'appellation « 11 + MUCL3 » est équivalente et sera
  employée dans la section pour rappeler la substitution.

### 3.4 Ce qui est consigné de la vérification

- URL complète de chaque source lue, date et heure de lecture,
  contenu pertinent recopié (champs HGNC, GeneID NCBI,
  `id` Ensembl), et réponses brutes conservées dans le
  chantier (`hgnc_mucl3_885.json`, `hgnc_prev_dpcr1_885.json`,
  `ensembl_mucl3_885.json`, `ensembl_dpcr1_885.json` —
  métadonnées de nomenclature, pas des données d'expression).
- Si une source est illisible (erreur réseau, page bloquée),
  c'est consigné tel quel avec le code d'erreur, et la porte
  correspondante est jugée sur les sources lisibles selon
  §3.2 (R3 non bloquante ; R1, R2, R4, R5 bloquantes).

### 3.5 Si le remappage ne tient pas

Fermeture de la piste, sans CSV et sans run : section §8.85
écrite quand même, avec la raison exacte (quelle porte R1–R5
a échoué, ce que la source lue dit vraiment), les tentatives
chiffrées, aucune valeur inventée, et la piste suivante nommée
comme piste seulement (C1 lot drogue Chen 2025, ou C4
GSE194249 après re-audit — aucun run lancé pour elle dans ce
chantier). A2 INCHANGÉ (9/13).

## 4. Arrêt borné — AUCUN repli technique dans ce chantier

**Une seule cohorte dans ce chantier : GDC ORGANOID-PANCREATIC,
fichiers tumoraux, n = 44, avec MUCL3 à la place de DPCR1.**
Si elle est INUTILISABLE selon les critères d'acceptation du
§5 (remappage non vérifié, manifeste SHA différent, MD5 en
échec, n tumoraux < 40, KRAS absent, < 12 flux mappés dont
MUCL3, < 40 cas complets), le chantier s'arrête sur un blocage
documenté : section §8.85 écrite quand même, avec les
tentatives chiffrées, aucune valeur inventée, et la piste
suivante nommée comme piste seulement (§3.5).
Il n'y a PAS de cohorte #2 courue dans ce chantier.

## 5. Construction des flux — variante (a), comme les paires GEO V1, avec MUCL3

Nouveau script `build_fluxes_885.py` (copie adaptée de
`build_fluxes_879.py`, original intact — seule la liste des
gènes change : DPCR1 remplacé par MUCL3 ; tout le reste est
repris à l'identique). Préfixe `_885_` pour tous les fichiers
du chantier.

### 5.1 Source (aucun nouveau téléchargement)

- **Aucun téléchargement dans ce chantier.** Les 55 TSV sont
  détenus localement depuis le §8.79
  (`data/gdc_organoid_879/`, total 232 648 892 o).
- Avant construction, re-vérification par programme : MD5 de
  chaque fichier contre le manifeste (§2.1) et contre
  `download_gdc_879_receipt.json` ; manifeste SHA-256
  `f713edebf…6220b` re-vérifié. Tout écart = ARRÊT (§4).
- Format attendu (vérifié au §8.79, à re-vérifier ici) :
  colonnes `gene_id, gene_name, gene_type, unstranded,
  stranded_first, stranded_second, tpm_unstranded,
  fpkm_unstranded, fpkm_uq_unstranded` ; 60 660 lignes de
  gènes + 4 lignes techniques STAR (`N_unmapped`,
  `N_multimapping`, `N_noFeature`, `N_ambiguous`). Si
  l'en-tête diffère, c'est consigné tel quel et la
  construction s'arrête (arrêt borné §4).

### 5.2 Identification des gènes

- Symbole lu dans la colonne `gene_name` (symbole exact,
  sensible à la casse). **Un seul gène mappé, et
  pré-enregistré : MUCL3 pour le flux v4 historiquement
  nommé DPCR1** (§3). Aucun autre gène mappé à la main.
- Les 13 gènes utiles (12 flux + KRAS) doivent être présents,
  UNE ligne chacun, sans doublon de symbole, dans CHAQUE
  fichier retenu. Tout doublon ou absence = ARRÊT (§4).
- Le `gene_id` de la ligne MUCL3 est relevé et croisé avec
  §3.5 (porte R5).
- Valeurs : colonne **`tpm_unstranded`** telle que fournie
  par GDC (normalisation TPM du fournisseur, pas un calcul
  de ce chantier). Aucune renormalisation, aucune
  transformation log, aucune imputation ajoutée. Les 4
  lignes techniques STAR sont exclues.
- DPCR1 doit être ABSENT de chaque fichier retenu (porte §5) :
  si le symbole DPCR1 apparaissait dans un fichier (par
  exemple une annotation mixte), c'est consigné et la
  construction s'arrête — le remappage suppose un symbole
  unique par gène.

### 5.3 Série réelle (variante (a))

- Flux v4 (les 12, ordre de la liste, MUCL3 à la place de
  DPCR1) :
  PGC, REG4, CLDN18, MUC17, **MUCL3 (ex-DPCR1)**, CR2, KRT20,
  MUC2, GSTM1, CEACAM5, CLCA1, MUC16.
- Contrôle : KRAS (expression TPM, croissant). Le contrôle
  n'est JAMAIS un flux : pas de doublon. Justification de
  l'ordre KRAS : identique aux paires principales V1 — KRAS
  est le contrôle monotone du projet, et l'ordre par son
  expression est celui de toutes les paires GEO à 12 gènes.
- Fichiers retenus : les **44 fichiers tumoraux** (§2.1) ;
  les 11 fichiers Normal sont exclus et comptés. Le
  diagnostic « Adenocarcinoma, NOS » est celui des 38 cas
  sources ; les 44 fichiers sont tous des échantillons
  Tumor (`tissue_type = Tumor`).
- **Unité = fichier (§2.1).** Aucune agrégation entre
  fichiers d'un même cas. Les 3 cas multi-fichiers (2, 3 et
  4 fichiers) entrent tels quels, déclarés au §8.85.
- Cas complets seulement (KRAS + 12 flux présents), jamais
  d'imputation. Attendu : 44/44 cas complets (0 NaN attendu
  sur les 13 lignes × 44 fichiers — vérifié, sinon ARRÊT
  si < 40 complets).
- Tri : KRAS TPM croissant ; `step` = rang 0..43.
- Sorties : `pdac_885_gdc_organoid_fluxes.csv` (+ `_nul.csv`).
  Colonnes : `step` + 12 flux (en-tête `MUCL3`, jamais
  `DPCR1`). SHA-256 consignés.

### 5.4 Nul

Bloc des flux permuté par lignes, graine 42, `rng(42)`,
contrôle (ordre KRAS, `step`) intact — même convention que
les paires V1 (§8.56.8, PROTOCOL_phase2 §2). Le nul est un
échantillon hypothétique, pas une mesure.

### 5.5 Nuls frais (conditionnels, §7)

Si et seulement si l'écart mesuré sur la paire graine 42 est
PROCHE du plancher (§7 : `d_maxsep` dans [−0,07 ; +0,14[),
2 nuls frais sont construits par la même méthode, graines
**8851** et **8852** (graines jamais utilisées dans ce projet
— vérifié par grep avant ce gel : aucune occurrence comme
graine de nul ; seules 8791/8792 existent, au §8.79), et
courus en runs frais
(`pdac_885_gdc_organoid_fluxes_nul_s8851.csv`,
`pdac_885_gdc_organoid_fluxes_nul_s8852.csv`,
`results_fast_v62_885_gdc_organoid_nul_s8851`,
`results_fast_v62_885_gdc_organoid_nul_s8852`). Le verdict
reste celui de la paire graine 42 (§7) ; les nuls frais sont
un contrôle de robustesse descriptif (min / médiane / max des
écarts), jamais un moyen de choisir le nul qui arrange.

## 6. Critères d'acceptation de la cohorte (vérifiés avant construction, sauf les portes de présence vérifiées par le script)

- Remappage vérifié selon §3 (portes R1, R2, R4, R5
  passées ; R3 consignée) ; sinon ARRÊT (§3.5).
- Manifeste SHA-256 `f713edebf…6220b` (re-vérifié) ; 55 lignes.
- 55/55 fichiers détenus, MD5 conformes au manifeste et au
  reçu §8.79 ; taille totale 232 648 892 o ; sinon ARRÊT (§4).
- En-tête de chaque fichier = les 9 colonnes gelées (§5.1) ;
  60 660 lignes de gènes + 4 techniques ; sinon ARRÊT (§4).
- n ≥ 40 fichiers tumoraux (`tissue_type = Tumor` par
  l'association fichier → échantillon de l'API GDC, §8.79) ;
  sinon ARRÊT (§4).
- Aucun fichier porteur d'un code-barres TCGA ou déjà présent
  dans une cohorte du projet ; sinon ARRÊT (§4). (Caveat
  §2.2 point 2 : le non-recouvrement est établi par programme
  et système d'identifiants, pas par jointure.)
- KRAS présent comme ligne mappée (`gene_name` exact) dans
  chaque fichier retenu ; sinon ARRÊT (§4).
- Les 12 flux présents (une ligne chacun, symbole exact,
  MUCL3 à la place de DPCR1) dans chaque fichier retenu ;
  DPCR1 absent de chaque fichier retenu ; sinon ARRÊT (§4)
  (aucun autre gène remplacé, aucun absent toléré pour une
  paire comparable).
- Cas complets (KRAS + 12 flux) ≥ 40 ; sinon ARRÊT (§4).

## 7. Runs v6.2 (mode fast)

- Lot : 2 runs — réel + nul — manifeste `manifest_v62_885.txt`,
  lanceur reprenable existant `run_v62_lot.sh` (saute les sorties
  déjà complètes), journal `runs_v62_885.log` (SHA du pipeline
  en tête, exits consignés).
- Dossiers : `results_fast_v62_885_gdc_organoid` et
  `results_fast_v62_885_gdc_organoid_nul` (nuls frais éventuels :
  `results_fast_v62_885_gdc_organoid_nul_s8851` /
  `..._s8852`).
- Lancement en `systemd-run --unit=v62-885 --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance qui
  s'arrête d'elle-même à 2/2 (ou 4/4 si nuls frais). Ne JAMAIS
  supprimer le dossier d'un run en cours. Si la machine
  redémarre, reprise sans perte (SKIP des dossiers complets,
  jamais de relance à l'aveugle).
- Note réseau (leçon PROVENANCE_879) : les unités
  `systemd-run` n'héritent pas des variables proxy — sans
  conséquence ici : les runs v6.2 sont du calcul local, aucun
  téléchargement n'a lieu dans ce chantier.
- SHA du pipeline revérifié avant ET après le lot.
- Durée attendue : ~2–3 min par run (référence §8.76 :
  n=42, 12 flux, ~2 min/run) ; le lot complet tient en
  ~10 min hors vérification du remappage.

## 8. Critère de passage — GELÉ avant tout run

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
  12/14 positifs) ; LOO recalculé sur 14 paires (pire cas sur
  13) : retirer une paire passante donne 9/13 — **LOO 9/13**.
- Si PARTIEL : A2 devient **9/14 au-dessus du plancher,
  12/14 positifs** ; LOO recalculé sur 14 paires : retirer
  une paire passante donne 8/13 — **LOO 8/13**.
- Si NON : A2 devient **9/14 au-dessus du plancher,
  11/14 positifs** ; LOO recalculé sur 14 paires :
  **LOO 8/13**.
- Dans tous les cas, la paire entre dans le compte A2 : c'est
  une paire principale indépendante (contrairement au lot FNA
  §8.76, apparié). **C3 reste LEVÉE** dans tous les cas — elle
  l'était déjà depuis le §8.71 ; ce chantier est une
  consolidation supplémentaire, pas une condition.
- Le leave-one-out sur les paires indépendantes est recalculé
  ici (il change : la paire y entre).
- Si le remappage échoue (§3.5) ou si une porte du §6 échoue :
  A2 INCHANGÉ (9/13, 11/13 positifs, LOO 8/12) — aucune paire
  n'est comptée sans runs.

**Nuls frais (§5.5, règle gelée).** La paire graine 42 fait le
verdict, dans tous les cas. Si `d_maxsep` est PROCHE du
plancher — défini ici comme `d_maxsep` dans [−0,07 ; +0,14[,
soit à moins d'une largeur de plancher du seuil, de part et
d'autre — les 2 nuls frais (graines 8851, 8852) sont courus et
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
- Falsification : INDISPONIBLE sous n = 75 — GDC organoid
  n = 44 : noter « indisponible », ne pas imputer.
- Plancher équivalent-sep (descriptif) : la paire passe-t-elle
  aussi `0,07·(1+m_R)(1+m_N)` ? Rapporté, non décisif (D4 n'est
  pas rejoué ici : il porte sur les paires V1, déjà tranché).
- Aucun autre critère, aucune repondération, aucune redéfinition
  du plancher après avoir vu les chiffres.

## 9. Extraction et vérification

1. Extracteur propre du chantier, `extract_885.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_879_c3.py`) ; lit `maxsep`, `mc_score`,
   `stability`, `ssep`, `delta`, `l7a`, cascade,
   falsification dans les 2 (ou 4) `master_results.json` ;
   sorties `extract_885.json` / `extract_885.csv`.
2. Second calcul indépendant : relecture directe des
   `master_results.json` par un chemin distinct (script
   `verify_885.py`, SHA noté) — `maxsep` et ancien MC recoupés
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
   `85e9089a…55e3b`), du §8.74 (`extract_874.json`, SHA
   `82ade74701245021dfdb965bdc689ac98262c70f12ecec7f39e1b5b742dfcb47`)
   et du §8.79 (`extract_879_c3.json`, valeurs §8.79.2),
   jamais recalculées ici — ce chantier ne re-vérifie pas les
   §8.56/§8.59/§8.64/§8.69/§8.70/§8.71/§8.74/§8.76/§8.79
   (déjà clos).
4. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 10. Tests directs en appui (ne décident pas)

Script `direct_tests_885.py` (SHA noté), sur les CSV de flux
du chantier (réel + nul graine 42) :
1. **Test informatif (correction §8.70, appliquée ici) :**
   corrélation de Spearman de chaque flux avec le pas (ordre
   KRAS), réel vs nul : |ρ| moyen, Δρ médian, nombre de Δρ
   positifs (sur 12), table complète sans sélection. C'est le
   test qui porte l'information d'ordre.
2. d de Cohen marginal des 12 flux (réel vs nul) : pour chaque
   flux, moyenne et écart-type des valeurs ordonnées, d de
   Cohen réel−nul ; table complète, sans sélection. **Attendu
   vacueux par construction : d = 0,0000 pour les 12 flux**
   (le nul est une permutation des lignes, chaque flux garde
   exactement ses 44 valeurs). Rapporté tel quel : il valide
   la construction du nul (marginales préservées exactement),
   il ne mesure pas la séparation.
3. Comparaison descriptive avec les paires précédentes
   (Δρ médian, 11/11 positifs au §8.79 ; valeurs reprises
   telles quelles, jamais recalculées). Si le signal d'ordre
   est plus faible, c'est consigné tel quel, sans être élucidé
   sans preuve ; si une divergence Delta/`maxsep` apparaît
   ici, elle est nommée telle quelle.
4. Aucun de ces tests ne change le verdict du §8.

## 11. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et le
  jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict : les résultats des autres dépôts (écran du 20 nov.,
  holdout GSE57495, pilote Chen, et le §8.79 lui-même — y
  compris son `d_maxsep = +0,4494`) ne prédisent rien ici —
  seul l'écart `maxsep` mesuré sur les runs du présent
  chantier fait le verdict. **En particulier, le fait que
  MUCL3 soit présent dans 55/55 fichiers ne prédit pas le
  verdict de cette paire.**
- Un nul qui invalide une piste est un résultat ; un échec du lot
  est un verdict, pas un échec caché.
- Ne jamais présenter une lecture préliminaire comme un verdict.
- Aucun consensus exigé entre flux ou contrôles ; aucune
  affirmation clinique — l'étude porte sur l'instrument.
- **Compter cette paire comme quatorzième paire indépendante
  UNIQUEMENT si les portes du §6 sont passées** (remappage
  vérifié, 44 fichiers tumoraux, 12/12 flux dont MUCL3,
  n ≥ 40). Toute lecture future qui compterait aussi les 11
  fichiers Normal serait fausse. Toute lecture future qui
  écrirait « DPCR1 » pour ce flux sans « (ex-DPCR1) » / « MUCL3 »
  serait fausse.

## 12. Livrables

- Ce protocole (gelé avant vérification du remappage,
  construction et runs).
- `PROVENANCE_885.md` (remappage : source, auteur, date, URL,
  réponses lues ; données : source, dépôt, URL, SHA-256 du
  manifeste et de chaque fichier, plateforme, effectifs,
  exclus, identification des gènes, vérifications
  d'indépendance du §2).
- `hgnc_mucl3_885.json`, `hgnc_prev_dpcr1_885.json`,
  `ensembl_mucl3_885.json`, `ensembl_dpcr1_885.json`
  (réponses brutes de nomenclature).
- `build_fluxes_885.py` + CSV de flux (`pdac_885_*`,
  SHA consignés) — ou, si arrêt, le journal de l'arrêt.
- `manifest_v62_885.txt`, `runs_v62_885.log`, dossiers
  `results_fast_v62_885_*`, `extract_885.json` / `.csv`,
  `verify_885.py` + sortie de vérification,
  `direct_tests_885.py` + sortie.
- §8.85 dans le FICHIER SÉPARÉ
  `section_8.85_gdc_mucl3.md` (verdict d'abord, une phrase :
  CONFIRME / PARTIEL / NON — ou FERMÉE si le remappage ne
  tient pas, avec la raison exacte ; chiffres ensuite ; détail
  complet après ; provenance nommée partout ; C3 reste levée
  dans tous les cas ; A2 recalculé sur 14 paires, dit
  explicitement, avec la substitution MUCL3 nommée partout).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin du protocole gelé §8.85. —
