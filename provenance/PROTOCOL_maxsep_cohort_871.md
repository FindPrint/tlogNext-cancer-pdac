# PROTOCOLE GELÉ — §8.71 : Confirmation indépendante pour `maxsep` (C3) sur GSE60979

Date : 20 novembre 2026, ~21h00 EST. Chantier §8.71, mission parent du
20 nov. 2026 (« PISTE 1 — §8.71 : chercher UNE AUTRE cohorte
indépendante pour la confirmation C3 de maxsep »).
Ce protocole est gelé AVANT tout téléchargement officiel, toute
construction et tout run. Le téléchargement officiel (dans `data/`,
SHA consigné) n'a lieu qu'après ce gel. Aucun paramètre ne change
après les résultats. Le livre blanc N'EST PAS édité, le PDF N'EST
PAS régénéré, rien n'est poussé sur GitHub dans ce chantier
(convention des chantiers ; fusion par le coordinateur). La section
§8.71 est écrite dans un FICHIER SÉPARÉ
(`section_8.71_gse60979.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié ; v6.1
`2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`).

## 0. Contexte décisionnel — à lire avant tout le reste

- §8.56 : `maxsep` seul SUFFIT aux barres gelées (A1 37/48, A2 6/8
  avec 7/8 positifs, A3 HP35 +1,6512) ; `sep` seul REJETÉ (A2 5/8).
- §8.59 : ADOPTER SOUS CONDITION (D1, D2, D5 passent ; D3 et D4
  échouent). Condition C3 (§8.59.8, lecture précise §8.69 §7 et
  §8.70 §8.70.8) : **7 paires passantes au total**, LOO pire cas
  (retrait d'une paire passante) à la barre A2 d'origine.
- §8.64 : adoption sous condition CONFIRMÉE par troisième lecture
  (0 écart), convention d'affichage figée (maxsep principal, ancien
  MC secondaire, sep compagnon borné, mention de fragilité en tête
  de chaque table).
- **Le 20 nov. 2026 à 13h04, Zackary a décidé d'ADOPTER maxsep
  pleinement dès maintenant** (convention d'affichage : maxsep score
  principal, MC secondaire, aucun changement de code). **La
  confirmation indépendante du présent chantier devient donc une
  vérification a posteriori, pas une condition.** Si elle passe,
  elle consolide l'adoption ; si elle échoue, l'adoption pleine
  reste sa décision et la confirmation reste ouverte — à dire
  plainement dans les deux cas, dans la section comme dans le
  rapport. Ce chantier ne rouvre pas les §8.56/§8.59/§8.64/§8.69/
  §8.70 et ne change aucune décision de Zackary.
- §8.69 : neuvième paire principale indépendante, GSE21501
  (n = 132), **NON** (`d_maxsep = −0,0100`) ; A2 étendu 6/9
  (7/9 positifs), LOO 5/8 — C3 NON levée.
- §8.70 : dixième paire principale indépendante, GSE79668
  (n = 51), **PARTIEL** (`d_maxsep = +0,0567`, sous le plancher
  0,07) ; A2 étendu 6/10 (8/10 positifs), LOO 5/9 — C3 NON
  levée. **Correction de méthode notée au §8.70 (§8.70.5,
  §8.70.7) et APPLIQUÉE ici (§9) : le test de Cohen marginal
  est vacueux par construction quand le nul est une permutation
  de lignes (d = 0,0000 pour les 12 gènes) — le test informatif
  est le Spearman de chaque flux contre le pas (Δρ médian,
  nombre de positifs).** Le Cohen marginal est quand même
  rapporté (il valide la construction du nul), mais il ne
  porte aucune information d'ordre et ne décide rien.

## 1. Les 10 paires principales déjà utilisées (V1 + §8.69 + §8.70)

Valeurs reprises du §8.56.3 (re-vérifiées à l'identique aux §8.59
et §8.64, 0 écart), du §8.69.2 (GSE21501) et du §8.70.2
(GSE79668). Écart = maxsep réel − maxsep nul (|d| de Cohen).
Plancher 0,07 en |d|.

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

Bilan : **6/10 au-dessus du plancher, 8/10 positifs.** Rotations
V2 (48 paires, §8.44, sans doublon) : 37/48 pour `maxsep`. Elles
ne sont PAS rejouées ici : le présent chantier ne porte que sur
UNE paire principale supplémentaire (C3), pas sur les rotations.

## 2. Paire choisie : GSE60979 — et pourquoi elle est vraiment indépendante

### 2.1 Choix

**Cohorte : GSE60979, NCBI GEO** — sous-série [mRNA] de la
SuperSeries GSE60980, « mRNA and miRNA expression profiles for
fresh frozen periampullary adenocarcinomas (pancreatobiliary and
intestinal type) and adjacent normal tissues », 93 échantillons,
plateforme GPL14550 (Agilent SurePrint G3 Human GE 8x60K),
soumise le 2 sept. 2014. Étude d'origine : Sandhu et coll.,
*Mol Oncol* 2015, 9:758–771 (PMID 25579086,
doi 10.1016/j.molonc.2014.12.002) — « Molecular signatures of
mRNAs and miRNAs as prognostic biomarkers in periampullary
adenocarcinomas ». Centre : Oslo University Hospital, Oslo,
Norvège (Department of Genetics, Institute for Cancer Research ;
Department of Hepato-Pancreato-Biliary Surgery). 49 tumeurs
PDAC (« tissue: pancreatic ductal adenocarcinoma »,
caractéristique ch1), 12 tissus normaux adjacents, 32 autres
adénocarcinomes périampullaires (duodénal 9, cholédoque 8,
ampoule type pancréatobiliaire 8, ampoule type intestinal 7).
URL (convention FTP des autres provenances) :
`https://ftp.ncbi.nlm.nih.gov/geo/series/GSE60nnn/GSE60979/matrix/GSE60979_series_matrix.txt.gz`

### 2.2 Justification d'indépendance (écrite avant tout téléchargement officiel)

1. **Jamais utilisée dans ce projet.** Vérifié par grep avant le
   gel (20 nov. 2026) : la chaîne exacte « GSE60979 » ne figure
   dans AUCUN fichier du projet (ni livre blanc, ni sections,
   ni protocoles, ni provenances, ni dossiers de runs). Aucun
   CSV de flux, aucun run, aucun JSON, aucune valeur `maxsep`
   n'existe pour GSE60979. La chaîne « GSE60980 » n'y figure
   pas davantage.
2. **Nouveaux patients, nouveau centre, nouvelle plateforme.**
   Cohorte monocentrique d'Oslo (Norvège) — aucun recoupement
   avec TCGA (multi-centres, 178 cas), ICGC PACA-AU, ni les
   cohortes GEO déjà utilisées (NCI pour GSE62452, autres
   centres pour GSE71729/GSE62165, Stratford Royaume-Uni pour
   GSE21501, UAB pour GSE79668, Moffitt pour GSE57495).
   Plateforme Agilent GPL14550, distincte de toutes les
   plateformes V1 et des confirmations (RNA-seq TCGA, Illumina
   ICGC, Affymetrix GPL20769/GPL6244/GPL13667/GPL15048/GPL570,
   Agilent GPL4133/GPL7264, Illumina HiSeq GPL11154).
   Patients distincts : 49 PDAC réséqués, cohorte d'Oslo 2014 ;
   titres `PDAC_1 [mRNA]` … `PDAC_49 [mRNA]`, aucun
   code-barres TCGA (vérifié sur la copie d'enquête ; à
   re-vérifier sur le téléchargement officiel, porte §5).
3. **Même construction que les autres paires principales GEO.**
   Variante (a) : les 12 mêmes gènes que la v4 TCGA (PGC, REG4,
   CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5,
   CLCA1, MUC16), ordre = KRAS croissant, sans correction, cas
   complets, nul = lignes permutées graine 42 (§4). La paire
   est donc comparable aux 10 paires comptées par construction.
4. **Pas un re-test déguisé.** Ce n'est ni une relecture d'un JSON
   existant (§8.64.7 : « pas une relecture »), ni une rotation
   déjà comptée, ni un sous-ensemble d'une paire V1, ni un
   nouvel ordre sur des CSV existants (nouveaux CSV, nouveaux
   runs, 2 runs v6.2 frais). La sous-série miRNA GSE60978
   (89 échantillons) n'est pas utilisée : ce n'est pas de
   l'expression génique codante.

**Note d'honnêteté sur l'enquête préalable.** Le choix de
GSE60979 repose sur une enquête GEO menée AVANT ce gel
(20 nov. 2026) : recherche E-utilities `pancreatic AND
Series[ET]` (789 séries), résumés récupérés, filtre n ≥ 40 et
humain, puis examen des sous-séries et des matrices des
candidats en copies temporaires `/tmp` (vérifications de
portes uniquement : effectifs, plateforme, couverture des
13 gènes — voir §2.3). Ces copies d'enquête sont des
vérifications de portes, pas des données de chantier : elles
sont supprimées, jamais utilisées pour construire un flux ni
lancer un run. Le téléchargement OFFICIEL (dans `data/`,
SHA consigné dans `PROVENANCE_871.md`) n'a lieu qu'après ce
gel ; si son SHA diffère de la copie d'enquête, c'est
consigné et les portes §5 sont re-vérifiées sur le fichier
officiel avant toute construction. Aucun `maxsep` GSE60979
n'existe à ce jour, et rien dans les résultats publiés
(signatures pronostiques périampullaires, Sandhu et coll.)
ne prédit l'écart réel−nul du pipeline.

### 2.3 Candidats écartés (enquête du 20 nov. 2026, raisons écrites d'avance)

Reprise des exclusions antérieures (§8.66 §1.3, §8.69.4,
§8.70 §2.3) : GSE78229, GSE28735 (re-découpages de GSE62452),
GSE15471 (39 < 40), GSE16515 (36 < 40), GSE32676 (25 < 40),
GSE32688 (sur-série de GSE32676), GSE91035 (25 < 40),
GSE57495 (11/12, GSTM1 absent), GSE62165 (10/12, DPCR1 et
GSTM1 absents), GSE21501 (§8.69, mesurée), GSE79668 (§8.70,
mesurée), GSE79670 (sur-série de GSE79668 + GSE79669 — mêmes
patients que §8.70), COAD / LUAD (autres cancers + lots déjà
courus), CPTAC (protéine, lots déjà courus), ICGC PACA-CA /
E-MTAB-6134 (accès hors périmètre), GSE84219, GSE179351
(n < 40).

Nouvelles exclusions, vérifiées dans l'enquête du 20 nov. 2026 :
- **GSE77858** (85 échantillons, UCLA, GPL7264, Agilent 4x44K,
  46 PDAC `pdac: Y`, valeurs = log2 ratios vs pool de 66
  tumeurs) : **12/13 — MUC17 ABSENT** de la plateforme GPL7264
  (mapping construit à neuf, 20 242 lignes, 18 703 sondes avec
  symbole, 16 746 symboles uniques, marqueur
  `!platform_table_end` vu ; aucune sonde à symbole exact
  MUC17 ; re-vérification par grep `MUC17` sur la table
  complète : aucune occurrence). Porte §5 échouée —
  INUTILISABLE comme paire principale à 12 gènes. Aucun CSV,
  aucun run. (Caveat consigné : GSE77858 est une étude UCLA,
  comme la cohorte inutilisée GSE32676 de Donahue et coll. —
  titres anonymes, recoupement de patients non vérifiable par
  identifiants ; ce caveat ne concerne pas GSE60979, centre
  d'Oslo.)
- **GSE43797** (62 échantillons, 3 types tumoraux) : 7 adéno-
  carcinomes canalaires seulement dans la sous-série mRNA
  (GPL10558, 31 échantillons : 13 SPN, 7 PCA, 6 NET, 5 non
  néoplasiques) — **7 < 40**. INUTILISABLE.
- **GSE161369** (« Pancreatic Cancer Datasets », sur-série,
  18 sous-séries vérifiées par titres) : lignées cellulaires,
  unicellulaire, CRISPR, xénogreffes — **aucune cohorte bulk
  de tumeurs primaires**. INUTILISABLE.
- **GSE63158** (sur-série de GSE56560 + GSE63111) : 35 + 35
  échantillons — **35 < 40** chaque sous-série. INUTILISABLE.
- **GSE131050** (PurIST, RNA-seq, 191 échantillons) : NON
  RETENUE comme primaire — deux plateformes (GPL16791,
  GPL18573), deux lots de séquençage en fichiers
  supplémentaires (`GSE131050_PurIST_Linehan_seq.tsv.gz`,
  `GSE131050_PurIST_Yeh_seq.tsv.gz`), matrices d'en-tête
  seules (4,7 Ko / 6,7 Ko) ; l'indépendance des deux lots
  (Linehan / Yeh) reste à vérifier cohorte par cohorte.
  **Piste restante nommée, non vérifiée**, pour un chantier
  futur — pas tentée ici (arrêt borné §3).
- Autres séries n ≥ 40 du filtre E-utilities : lignées
  cellulaires, xénogreffes, organoïdes, CTC, IPMN, îlots,
  tissus normaux, autres cancers, méthylation, ATAC, miRNA
  seul, unicellulaire/spatial — aucune autre cohorte bulk de
  tumeurs primaires PDAC avec expression codante identifiée.

## 3. Arrêt borné — AUCUN repli technique

**Une seule cohorte dans ce chantier : GSE60979.** Si elle est
INUTILISABLE selon les critères d'acceptation du §5
(téléchargement impossible, plateforme sans table exploitable,
n < 40, KRAS absent, < 12 gènes v4 mappés, < 40 cas complets,
ou recouvrement d'échantillons avec une cohorte déjà utilisée),
le chantier s'arrête sur un blocage documenté : section §8.71
écrite quand même, avec les tentatives chiffrées, aucune valeur
inventée, et la piste suivante nommée comme piste seulement
(GSE131050, §2.3 — aucune autre cohorte forcée, aucun run
lancé pour elle).
Il n'y a PAS de cohorte #2 dans ce chantier.

## 4. Construction des flux — variante (a), comme les paires GEO V1

Nouveau script `build_fluxes_871.py` (copie adaptée de
`build_fluxes_869.py`, original intact). Préfixe `_871_` pour
tous les fichiers du chantier.

### 4.1 Identification gènes (GSE60979 / GPL14550, Agilent)

- Le mapping GPL14550 a été construit à neuf AVANT le gel, dans
  l'enquête (§2.2) : `data/GPL14550_probe2symbol.tsv`
  (42 545 lignes de table, 30 436 sondes avec symbole,
  22 070 symboles uniques, colonne `GENE_SYMBOL`, marqueur
  `!platform_table_end` vu ; script
  `download_gpl14550_mapping_871.py`, adapté de
  `download_gpl4133_mapping_869.py`, original intact).
  Il est REPRIS tel quel — aucun mapping n'est reconstruit
  dans le chantier, et le script de construction le lit sans
  le modifier. SHA consigné dans `PROVENANCE_871.md`.
- Identifiants multiples vers un même symbole : agrégation par
  médiane (règle du projet). Identifiant sans symbole : non
  mappé. Identifiant vers plusieurs symboles : exclu si ambigu
  (aucun gène mappé à la main).
- La plateforme réelle est confirmée par l'en-tête de la
  matrice (`!Series_platform_id`) et consignée dans
  `PROVENANCE_871.md` ; si l'en-tête dit autre chose que
  GPL14550, c'est consigné tel quel et la construction
  s'arrête (arrêt borné §3 — aucun mapping d'une autre
  plateforme ne sera substitué sans nouveau protocole gelé).
- Couverture vérifiée dans l'enquête (à re-vérifier sur le
  fichier officiel, porte §5) : les 13 gènes utiles (12 v4 +
  KRAS) sont présents dans le mapping ET dans les lignes de
  la matrice (PGC 2 sondes, REG4 2, CLDN18 1, MUC17 2, DPCR1 1,
  CR2 2, KRT20 1, MUC2 4, GSTM1 1, CEACAM5 1, CLCA1 1, MUC16 2,
  KRAS 2).

### 4.2 Série réelle (variante (a))

- Gènes v4 (les 12 mêmes que TCGA v4, ordre de la liste) :
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1,
  CEACAM5, CLCA1, MUC16.
- Contrôle : KRAS (expression, croissant). Le contrôle n'est
  JAMAIS un flux : pas de doublon. Justification de l'ordre
  KRAS : identique aux paires principales V1 — KRAS est le
  contrôle monotone du projet, et l'ordre par son expression
  est celui de toutes les paires GEO à 12 gènes ; aucun ordre
  stade n'est construit (les paires principales V1 sont en
  ordre KRAS ; la survie publiée ne sert pas d'ordre ici —
  l'ordre KRAS est le seul ordre gelé).
- Tumeurs seules : caractéristique ch1
  `tissue: pancreatic ductal adenocarcinoma` (49 échantillons
  attendus) ; les 12 normaux adjacents et les 32 autres
  adénocarcinomes périampullaires sont exclus et comptés.
  Cas complets seulement (KRAS + 12 gènes présents), jamais
  d'imputation. Valeurs : telles que fournies par les
  déposants (nature exacte — d'après l'en-tête de la matrice
  et la plage des valeurs : min 4,02 / médiane 5,72 /
  max 18,56 sur les 2 000 premières lignes, 0 NaN — allure
  d'intensités log2 normalisées Agilent ; nature exacte
  consignée dans `PROVENANCE_871.md` d'après le fichier
  officiel ; aucune renormalisation, aucune transformation
  log ajoutée).
- Sorties : `pdac_871_geo60979_fluxes.csv` (+ `_nul.csv`).
  Colonnes : `step` + 12 flux. SHA-256 consignés.

### 4.3 Nul

Bloc des flux permuté par lignes, graine 42, `rng(42)`, contrôle
(KRAS, ordre) intact — même convention que les paires V1
(§8.56.8, PROTOCOL_phase2 §2). Le nul est un échantillon
hypothétique, pas une mesure.

### 4.4 Nuls frais (conditionnels, §7)

Si et seulement si l'écart mesuré sur la paire graine 42 est
PROCHE du plancher (§7 : `d_maxsep` dans [−0,07 ; +0,14[),
2 nuls frais sont construits par la même méthode, graines
**8711** et **8712** (graines jamais utilisées dans ce projet,
gelées ici avant tout run), et courus en runs frais
(`pdac_871_geo60979_fluxes_nul_s8711.csv`,
`pdac_871_geo60979_fluxes_nul_s8712.csv`,
`results_fast_v62_871_geo60979_nul_s8711`,
`results_fast_v62_871_geo60979_nul_s8712`). Le verdict reste
celui de la paire graine 42 (§7) ; les nuls frais sont un
contrôle de robustesse descriptif (min / médiane / max des
écarts), jamais un moyen de choisir le nul qui arrange.

## 5. Critères d'acceptation de la cohorte (vérifiés après téléchargement officiel, avant construction)

- Matrice téléchargée, HTTP 200, lecture complète vérifiée
  (nombre de lignes, NaN comptés) ; SHA-256 consigné dans
  `PROVENANCE_871.md` avant toute construction.
- Plateforme lue dans l'en-tête de la matrice : GPL14550 ;
  sinon ARRÊT (§3).
- n ≥ 40 tumeurs PDAC (caractéristique ch1) ; sinon ARRÊT (§3).
- Aucun échantillon porteur d'un code-barres TCGA ou déjà
  présent dans une cohorte du projet (GSM/titres inspectés) ;
  sinon ARRÊT (§3).
- KRAS présent comme ligne mappée ; sinon ARRÊT (§3).
- Les 12 gènes v4 présents (mappés ET dans les lignes de la
  matrice) ; sinon ARRÊT (§3) (aucun gène remplacé, aucun
  absent toléré pour une paire principale — la comparabilité
  aux 10 paires comptées l'exige).
- Cas complets (KRAS + 12 gènes) ≥ 40 ; sinon ARRÊT (§3).

## 6. Runs v6.2 (mode fast)

- Lot : 2 runs — réel + nul — manifeste `manifest_v62_871.txt`,
  lanceur reprenable existant `run_v62_lot.sh` (saute les sorties
  déjà complètes), journal `runs_v62_871.log` (SHA du pipeline
  en tête, exits consignés).
- Dossiers : `results_fast_v62_871_geo60979` et
  `results_fast_v62_871_geo60979_nul` (nuls frais éventuels :
  `results_fast_v62_871_geo60979_nul_s8711` /
  `..._s8712`).
- Lancement en `systemd-run --unit=v62-871 --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance qui
  s'arrête d'elle-même à 2/2 (ou 4/4 si nuls frais). Ne JAMAIS
  supprimer le dossier d'un run en cours. Si la machine
  redémarre, reprise sans perte (SKIP des dossiers complets,
  jamais de relance à l'aveugle).
- SHA du pipeline revérifié avant ET après le lot.

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
- **CONFIRME** : `d_maxsep > 0,07` — la paire passe.
- **PARTIEL** : `0 < d_maxsep ≤ 0,07` — positif mais sous le
  plancher (même catégorie que GSE71729, +0,0402, et GSE79668,
  +0,0567).
- **NON** : `d_maxsep ≤ 0` — négatif ou nul (même catégorie que
  GSE62452 et GSE21501).

**Verdict étendu (A2 à 11 paires) :**
- Si la paire passe : A2 étendu = **7/11 au-dessus du plancher,
  9/11 positifs** (les 10 paires gardent leurs valeurs : 6/10
  et 8/10 positifs). La condition C3 du §8.59.8 est levée —
  **7 paires passantes au total** — la confirmation
  indépendante consolide l'adoption pleine décidée par Zackary
  le 20 nov. 13h04. Le leave-one-out sur les 11 paires est
  calculé en descriptif : retirer n'importe quelle paire
  passante laisse 6/10, qui satisfait encore la barre A2
  d'origine (≥ 6/8) — l'adoption ne tient plus à une seule
  paire.
- Si la paire est PARTIELLE : A2 étendu = **6/11, 9/11
  positifs**. C3 reste OUVERTE.
- Si la paire échoue (NON) : A2 étendu = **6/11, 8/11 positifs**.
  C3 reste OUVERTE, la confirmation reste à trouver, et
  l'adoption pleine reste la décision de Zackary du 20 nov.
  13h04 — ce chantier ne la rouvre pas et ne la conditionne
  pas.

**Nuls frais (§4.4, règle gelée).** La paire graine 42 fait le
verdict, dans tous les cas. Si `d_maxsep` est PROCHE du
plancher — défini ici comme `d_maxsep` dans [−0,07 ; +0,14[,
soit à moins d'une largeur de plancher du seuil, de part et
d'autre — les 2 nuls frais (graines 8711, 8712) sont courus et
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
- Falsification : INDISPONIBLE sous n = 75 — GSE60979 n = 49 :
  noter « indisponible », ne pas imputer.
- Plancher équivalent-sep (descriptif) : la paire passe-t-elle
  aussi `0,07·(1+m_R)(1+m_N)` ? Rapporté, non décisif (D4 n'est
  pas rejoué ici : il porte sur les paires V1, déjà tranché).
- Aucun autre critère, aucune repondération, aucune redéfinition
  du plancher après avoir vu les chiffres.

## 8. Extraction et vérification

1. Extracteur propre du chantier, `extract_871.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_866.py` / `extract_869.py`) ; lit `maxsep`,
   `mc_score`, `stability`, `ssep`, `delta`, `l7a`, cascade,
   falsification dans les 2 (ou 4) `master_results.json` ;
   sorties `extract_871.json` / `extract_871.csv`.
2. Second calcul indépendant : relecture directe des
   `master_results.json` par un chemin distinct (script
   `verify_871.py`, SHA noté) — `maxsep` et ancien MC recoupés
   à 0,0 exact ; tout écart = résultat à diagnostiquer, pas un
   bruit.
3. Recoupements : les 10 valeurs déjà comptées reprises telles
   quelles du §8.56 (table `sep_maxsep_856_table.json`, SHA
   `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`),
   du §8.69 (`extract_869.json`, SHA
   `644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b`)
   et du §8.70 (`extract_870.json`, SHA
   `4ffa851a83668b2369097703862e0413ff9af54af3a66ef70aea9333b40c444f`),
   jamais recalculées ici — ce chantier ne re-vérifie pas les
   §8.56/§8.59/§8.64/§8.69/§8.70 (déjà clos).
4. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 9. Tests directs en appui (ne décident pas)

Script `direct_tests_871.py` (SHA noté), sur les CSV de flux
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
   exactement ses 49 valeurs). Rapporté tel quel : il valide
   la construction du nul (marginales préservées exactement),
   il ne mesure pas la séparation.
3. Si l'ordre est KRAS (cas attendu) : comparaison descriptive
   avec les §8.69/§8.70 — au §8.69, Delta +2,01 contre maxsep
   −0,01 ; au §8.70, Delta plat +0,05 contre maxsep +0,06.
   Si une divergence Delta/`maxsep` apparaît ici, elle est
   nommée telle quelle, sans être élucidée sans preuve ; si
   elle n'apparaît pas, c'est consigné aussi.
4. Aucun de ces tests ne change le verdict du §7.

## 10. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et le
  jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict : les tests directs des §8.66/§8.70, la signature
  pronostique Sandhu et coll., les scores publiés ne prédisent
  rien ici — seul l'écart `maxsep` mesuré sur les runs du
  présent chantier fait le verdict.
- Un nul qui invalide une piste est un résultat ; un échec de la
  paire est un verdict, pas un échec caché.
- Ne jamais présenter une lecture préliminaire comme un verdict.
- Aucun consensus exigé entre flux ou contrôles ; aucune
  affirmation clinique — l'étude porte sur l'instrument.

## 11. Livrables

- Ce protocole (gelé avant téléchargement officiel, construction
  et runs).
- `PROVENANCE_871.md` (source, auteur, date, dépôt, URL, SHA-256
  des fichiers téléchargés, plateforme réelle, effectifs, exclus,
  identification des gènes — avec la vérification d'indépendance
  du §2.2 et le compte rendu de l'enquête préalable §2.2/§2.3).
- `build_fluxes_871.py` + CSV de flux (`pdac_871_*`, SHA consignés).
- `manifest_v62_871.txt`, `runs_v62_871.log`, dossiers
  `results_fast_v62_871_*`, `extract_871.json` / `.csv`,
  `verify_871.py` + sortie de vérification,
  `direct_tests_871.py` + sortie.
- §8.71 dans le FICHIER SÉPARÉ
  `section_8.71_gse60979.md` (verdict d'abord, une phrase :
  C3 levée ou non ; chiffres ensuite ; détail complet après ;
  provenance nommée partout).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin du protocole gelé §8.71. —
