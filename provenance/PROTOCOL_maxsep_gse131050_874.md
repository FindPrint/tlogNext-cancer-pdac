# PROTOCOLE GELÉ — §8.74 : Tester GSE131050 (PurIST) comme douzième paire principale pour `maxsep`

Date : 20 novembre 2026, ~23h20 EST. Chantier §8.74, piste 2/3 du
lot du 20 nov. 2026 (go de Zackary « Les 3 allez s'y », 18h04).
Ce protocole est gelé AVANT tout téléchargement officiel, toute
construction et tout run. Le téléchargement officiel (dans `data/`,
SHA consigné) n'a lieu qu'après ce gel. Aucun paramètre ne change
après les résultats. Le livre blanc N'EST PAS édité, le PDF N'EST
PAS régénéré, rien n'est poussé sur GitHub dans ce chantier
(convention des chantiers ; fusion par le coordinateur). La section
§8.74 est écrite dans un FICHIER SÉPARÉ
(`section_8.74_gse131050.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié ; v6.1
`2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`).
Chemin : `/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`.

Note de cécité (état connu du fichier v6.2, inchangé depuis son
adoption) : un grep `temperature|Onsager|2.269` sur le fichier
retourne 8 occurrences, TOUTES confinées à l'annexe génératrice
d'exemple Ising (lignes ~10211 et ~12571–12817, fonction
`generate_example_ising_csv`, marquée « EXEMPLE UNIQUEMENT, hors
cœur du pipeline »). Le cœur d'analyse ne voit ni T ni Tc ; le
fichier est celui adopté, SHA vérifié ci-dessus, jamais modifié.

## 0. Contexte décisionnel — à lire avant tout le reste

- §8.56 : `maxsep` seul SUFFIT aux barres gelées ; `sep` seul
  REJETÉ.
- §8.59 : ADOPTER SOUS CONDITION (D1, D2, D5 passent ; D3 et D4
  échouent). Condition C3 (§8.59.8) : 7 paires passantes au total,
  LOO pire cas à la barre A2 d'origine.
- §8.71 : onzième paire principale, GSE60979 (n = 49),
  **CONFIRME** (`d_maxsep = +0,2045`) ; A2 étendu **7/11
  au-dessus du plancher, 9/11 positifs** — **C3 du §8.59.8
  LEVÉE** (7 paires passantes au total, LOO pire cas 6/10).
- **Le 20 nov. 2026 à 13h04, Zackary a décidé d'ADOPTER maxsep
  pleinement dès maintenant** (convention d'affichage : maxsep
  score principal, MC secondaire, aucun changement de code).
  **Le présent chantier est donc une confirmation
  SUPPLÉMENTAIRE, pas une condition : il ne rouvre pas C3, quel
  que soit son verdict.** Si la paire passe, elle consolide
  l'adoption ; si elle échoue, l'adoption pleine reste sa
  décision — à dire plainement dans les deux cas, dans la
  section comme dans le rapport. Ce chantier ne rouvre pas les
  §8.56/§8.59/§8.64/§8.69/§8.70/§8.71 et ne change aucune
  décision de Zackary.
- §8.69 : GSE21501 (n = 132), **NON** (`d_maxsep = −0,0100`).
- §8.70/§8.72 : GSE79668 (n = 51), d'abord **PARTIEL**
  (`+0,0567` contre le nul graine 42), puis renversé contre
  13 nuls (écart médian `+0,1447`). **Correction de méthode
  notée au §8.70 (§8.70.5, §8.70.7) et APPLIQUÉE ici (§9) : le
  test de Cohen marginal est vacueux par construction quand le
  nul est une permutation de lignes (d = 0,0000 pour les 12
  gènes) — le test informatif est le Spearman de chaque flux
  contre le pas (Δρ médian, nombre de positifs).** Le Cohen
  marginal est quand même rapporté (il valide la construction
  du nul), mais il ne porte aucune information d'ordre et ne
  décide rien.

## 1. Les 11 paires principales déjà utilisées (V1 + §8.69 + §8.70 + §8.71)

Valeurs reprises du §8.56.3 (re-vérifiées à l'identique aux §8.59
et §8.64, 0 écart), du §8.69.2 (GSE21501), du §8.70.2 (GSE79668)
et du §8.71.2 (GSE60979). Écart = maxsep réel − maxsep nul (|d|
de Cohen). Plancher 0,07 en |d|.

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

Bilan : **7/11 au-dessus du plancher, 9/11 positifs.** Rotations
V2 (48 paires, §8.44, sans doublon) : 37/48 pour `maxsep`. Elles
ne sont PAS rejouées ici : le présent chantier ne porte que sur
UNE paire principale supplémentaire, pas sur les rotations.

## 2. Paire choisie : GSE131050, lot Yeh_seq FF — et pourquoi elle est vraiment indépendante

### 2.1 Choix

**Cohorte : GSE131050, NCBI GEO** — sous-série [RNA-Seq] de la
SuperSeries GSE131049 (l'autre sous-série, GSE131051, est
NanoString, non utilisée : ce n'est pas de l'expression RNA-seq
codante en comptages géniques). Étude d'origine : Rashid et
coll., *Clin Cancer Res* 2020, 26(1):82–92 (PMID 31754050,
doi 10.1158/1078-0432.CCR-19-1467) — « Purity Independent
Subtyping of Tumors (PurIST), a clinically robust single-sample
classifier for tumor subtyping in pancreatic cancer ». Centre :
Lineberger Comprehensive Cancer Center, University of North
Carolina at Chapel Hill (UNC). Série soumise le 10 mai 2019,
publique le 10 déc. 2019, 191 échantillons, 2 plateformes :
GPL16791 (Illumina HiSeq 2500) et GPL18573 (Illumina NextSeq
500). BioProject PRJNA542388, SRA SRP197641.
URL (convention FTP des autres provenances) :
`https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/suppl/GSE131050_PurIST_Yeh_seq.tsv.gz`
`https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/suppl/GSE131050_PurIST_Linehan_seq.tsv.gz`
`https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/matrix/GSE131050-GPL18573_series_matrix.txt.gz`
`https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/matrix/GSE131050-GPL16791_series_matrix.txt.gz`

**La série contient DEUX lots, un seul est la paire primaire
(voir §2.3 pour le lot écarté) :**
- **Lot primaire — Yeh_seq, GPL18573 (Illumina NextSeq 500) :
  tumeurs primaires PDAC, échantillons flash-frozen (FF), UN
  échantillon par tumeur indépendante, n = 42** (construction
  §4 : 47 colonnes FF primaires → 42 codes-tumeurs distincts,
  les 4 codes à réplicats FF agrégés par médiane).
- Lot écarté — Linehan_seq, GPL16791 (Illumina HiSeq 2500) :
  66 biopsies de 37 patients, pré- ET post-traitement mélangées
  (voir §2.3).

### 2.2 Justification d'indépendance (écrite avant tout téléchargement officiel)

1. **Jamais utilisée dans ce projet.** Vérifié par grep avant le
   gel (20 nov. 2026) : la chaîne exacte « GSE131050 » ne
   figure que comme « piste restante non vérifiée » dans trois
   fichiers du §8.71 (`PROTOCOL_maxsep_cohort_871.md`,
   `PROVENANCE_871.md`, `section_8.71_gse60979.md`) et dans le
   livre blanc aux mêmes endroits — AUCUN CSV de flux, aucun
   run, aucun JSON, aucune valeur `maxsep` n'existe pour
   GSE131050. La chaîne « GSE131049 » n'y figure pas
   davantage comme donnée utilisée.
2. **Nouveaux patients, nouveau centre, nouvelle plateforme.**
   Données NOUVELLES générées pour l'étude PurIST : lot Yeh
   collecté de novo à l'UNC (Tissue Procurement Core Facility,
   Lineberger) — tumeurs réséquées, congelées flash en azote
   liquide ; lot Linehan issu de l'essai de phase 1b Nywening
   et coll. (FOLFIRINOX ± inhibiteur CCR2, PDAC localement
   avancé, Washington University / Rochester). Aucun
   recoupement avec TCGA (multi-centres, 178 cas), ICGC
   PACA-AU, ni les cohortes GEO déjà utilisées (NCI pour
   GSE62452, autres centres pour GSE71729/GSE62165, Stratford
   Royaume-Uni pour GSE21501, UAB pour GSE79668, Moffitt pour
   GSE57495, Oslo pour GSE60979). Plateforme Illumina NextSeq
   500 (GPL18573), distincte de toutes les plateformes V1 et
   des confirmations (RNA-seq TCGA, Illumina ICGC, Affymetrix
   GPL20769/GPL6244/GPL13667/GPL15048/GPL570, Agilent
   GPL4133/GPL7264/GPL14550, Illumina HiSeq GPL11154/GPL16791).
   Patients distincts : titres anonymes `S001…S125` (codes
   `MMDDT#`), aucun code-barres TCGA (vérifié sur la copie
   d'enquête ; à re-vérifier sur le téléchargement officiel,
   porte §5).
3. **Les jeux publics de la méta-analyse PurIST ne sont PAS dans
   GSE131050.** L'article utilise, pour la méta-analyse et
   l'entraînement de PurIST, des jeux publics (TCGA_PAAD,
   PACA_AU_seq/array, Moffitt_GEO_array, Aguirre, COMPASS,
   Linehan) — ces jeux ne sont PAS redéposés dans GSE131050 :
   la série ne contient que les deux fichiers supplémentaires
   Yeh_seq et Linehan_seq, données nouvelles. GSE131050 n'est
   donc pas un re-découpage d'une cohorte déjà tenue.
   Caveat consigné : les titres étant anonymisés (codes
   `S###`), une exclusion formelle, identifiant par
   identifiant, d'un recouvrement avec TCGA_PAAD est
   impossible — aucun échantillon ne porte de code-barres
   TCGA et la collecte est décrite comme de novo dans
   l'article ; c'est le même standard que le §8.71 (titres /
   GSM inspectés, aucun code-barres TCGA).
4. **Même construction que les autres paires principales GEO.**
   Variante (a) : les 12 mêmes gènes que la v4 TCGA (PGC, REG4,
   CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5,
   CLCA1, MUC16), ordre = KRAS croissant, sans correction, cas
   complets, nul = lignes permutées graine 42 (§4). La paire
   est donc comparable aux 11 paires comptées par construction.
   Une seule adaptation, gelée ici et justifiée au §4.4 :
   l'unité d'analyse est la TUMEUR INDÉPENDANTE, pas la
   colonne — les réplicats FF d'une même tumeur sont agrégés
   par médiane (précédent du projet : agrégation par médiane
   des sondes multiples vers un même symbole).
5. **Pas un re-test déguisé.** Ce n'est ni une relecture d'un JSON
   existant (§8.64.7 : « pas une relecture »), ni une rotation
   déjà comptée, ni un sous-ensemble d'une paire V1, ni un
   nouvel ordre sur des CSV existants (nouveaux CSV, nouveaux
   runs, 2 runs v6.2 frais). La sous-série NanoString GSE131051
   n'est pas utilisée.

**Note d'honnêteté sur l'enquête préalable.** Le choix du lot
Yeh_seq FF repose sur une enquête menée AVANT ce gel
(20 nov. 2026) : matrices d'en-tête GEO (4,7 Ko / 6,7 Ko) et
fichiers supplémentaires téléchargés en copies temporaires
dans `enquete_874/` (vérifications de portes uniquement :
effectifs, plateforme, couverture des 13 gènes, structure
appariée des échantillons — voir §2.3 et §4). Ces copies
d'enquête sont des vérifications de portes, pas des données
de chantier : elles sont SUPPRIMÉES après le gel et le
téléchargement OFFICIEL (dans `data/`, SHA consigné dans
`PROVENANCE_874.md`) les remplace ; si le SHA officiel
diffère de la copie d'enquête, c'est consigné et les portes
§5 sont re-vérifiées sur le fichier officiel avant toute
construction. SHA des copies d'enquête (pour comparaison) :
Yeh_seq `2fc0a66e…be5b1` (9 468 179 o),
Linehan_seq `729bb794…efc16` (5 157 464 o),
matrice GPL18573 `9b333eb6…7843e` (6 864 o),
matrice GPL16791 `03aa8ca6…1df94` (4 859 o).
Aucun `maxsep` GSE131050 n'existe à ce jour, et rien dans les
résultats publiés (sous-types PurIST, associations pronostic /
réponse FOLFIRINOX, Rashid et coll.) ne prédit l'écart
réel−nul du pipeline.

### 2.3 Le lot Linehan_seq est ÉCARTÉ comme paire principale (raison écrite d'avance)

- **Linehan_seq (GPL16791, Illumina HiSeq 2500, 66 échantillons) :
  66 biopsies pour 37 patients seulement** (29 patients × 2
  échantillons, 8 patients × 1 ; suffixes `.01` × 37, `.02`
  × 29). L'article le dit explicitement : « The Linehan Phase
  1b trial captured both pre- and post-treatment biopsies »
  (Rashid et coll. 2020, Résultats, stabilité des sous-types ;
  fig. 2C : transitions pré/post-traitement, Kappa de Cohen
  1,0 pour le schéma Moffitt). Les métadonnées GEO ne
  labellisent PAS pré/post (caractéristiques ch1 : seulement
  `sample type: tumor biopsies`, `tissue: pancreatic ductal
  adenocarcinoma`) — le partage pré/post n'est donc pas
  extractible sans la table supplémentaire 2 de l'article.
- Conséquence : le lot mélange biopsies pré-traitement (28
  patients avec données RNAseq + traitement, d'après
  l'article) et post-traitement, avec 29 patients comptés deux
  fois. Le plus grand sous-ensemble homogène de tumeurs
  indépendantes pré-traitement est d'au plus 37 < 40 — la porte
  n ≥ 40 échoue. **Linehan_seq est INUTILISABLE comme paire
  principale.** Aucun CSV, aucun run pour ce lot.
  (Caveat consigné : les 66 biopsies sont toutes des tumeurs
  PDAC prélevées avant traitement pour 37 d'entre elles — le
  lot n'est pas « mauvais », il est structurellement
  incompatible avec la construction d'une paire principale à
  tumeurs indépendantes.)

### 2.4 Structure appariée du lot Yeh_seq (vérifiée dans l'enquête — elle motive la construction §4)

- Yeh_seq (GPL18573, 125 échantillons) : 97 tumeurs primaires
  (Pi) + 28 xénogreffes dérivées de patients (PDX, exclues :
  ce ne sont pas des tumeurs primaires). Primaires : 47 FF +
  5 FFPE + 45 FNA.
- Les 97 échantillons primaires proviennent de **43 tumeurs
  indépendantes seulement** (codes `MMDDT#` : 41 codes ont à
  la fois un FF et un FNA — échantillonnage apparié décrit
  dans l'article : FNA ex-vivo au moment de la résection, 3
  passages, aiguille 22G ; FFPE relus par un pathologiste).
  Prendre les 97 colonnes comme 97 tumeurs compterait 54 fois
  la même tumeur — interdit par la règle d'indépendance (§2.2).
- FF primaires : 47 colonnes → 42 codes distincts. Codes à
  réplicats FF : 0417T1 (×3 FF), 0523T1 (×2), 0806T1 (×2),
  1119T1 (×2). Code sans FF : 0921T1 (FNA seul) — exclu du
  lot FF.
- FNA primaires (45 colonnes, 42 codes) et FFPE primaires (5)
  ne sont PAS mélangés au lot FF : types d'échantillons
  différents, kits de préparation différents (TruSeq pour les
  70 FF ; TruSeq RNA Exome pour les 55 FNA+FFPE). Ils restent
  une piste suivante nommée (§8.74.9), non courue ici.

## 3. Arrêt borné — AUCUN repli technique

**Une seule cohorte dans ce chantier : le lot Yeh_seq FF de
GSE131050 (n = 42 tumeurs indépendantes).** Si elle est
INUTILISABLE selon les critères d'acceptation du §5
(téléchargement impossible, plateforme sans table exploitable,
n < 40 tumeurs indépendantes, KRAS absent, < 12 gènes v4
mappés, < 40 cas complets, ou recouvrement d'échantillons avec
une cohorte déjà utilisée), le chantier s'arrête sur un blocage
documenté : section §8.74 écrite quand même, avec les tentatives
chiffrées, aucune valeur inventée, et la piste suivante nommée
comme piste seulement (lot Yeh_seq FNA, un FNA par tumeur,
n = 42 — §8.74.9 ; aucune autre cohorte forcée, aucun run
lancé pour elle).
Il n'y a PAS de cohorte #2 dans ce chantier. Le lot Linehan_seq
n'est PAS un repli (§2.3 : écarté d'avance, pour une raison
structurelle).

## 4. Construction des flux — variante (a), comme les paires GEO V1

Nouveau script `build_fluxes_874.py` (copie adaptée de
`build_fluxes_871.py`, original intact). Préfixe `_874_` pour
tous les fichiers du chantier.

### 4.1 Identification gènes (GSE131050 Yeh_seq / GPL18573, Illumina NextSeq 500)

- Pas de mapping sonde→symbole : le fichier supplémentaire est
  déjà une table gène × échantillon, première colonne
  `geneID` de la forme `ENSG…;SYMBOLE` (ex.
  `ENSG00000133703;KRAS`). Le symbole est lu après le `;`.
- Couverture vérifiée dans l'enquête (à re-vérifier sur le
  fichier officiel, porte §5) : les 13 gènes utiles (12 v4 +
  KRAS) sont présents, UNE ligne chacun, sans doublon de
  symbole, dans les DEUX fichiers supplémentaires (Yeh 26 267
  gènes, Linehan 23 686 gènes). Aucun gène mappé à la main.
- La plateforme réelle est confirmée par l'en-tête de la
  matrice (`!Series_platform_id` : GPL18573 pour Yeh) et
  consignée dans `PROVENANCE_874.md` ; si l'en-tête dit autre
  chose que GPL18573 pour le lot Yeh, c'est consigné tel quel
  et la construction s'arrête (arrêt borné §3).
- Valeurs : telles que fournies par les déposants (nature
  exacte — d'après la plage des valeurs : min 0 / médiane
  ~0,02–147 / max jusqu'à 13 070 sur les 13 gènes, 0 NaN, 0
  cellule vide — allure de TPM/FPKM non log-transformés ;
  l'article indique « FPKM ou TPM selon l'étude » sans
  préciser pour ces deux fichiers : nature exacte consignée
  comme indéterminée entre FPKM et TPM dans
  `PROVENANCE_874.md` ; aucune renormalisation, aucune
  transformation log ajoutée).

### 4.2 Série réelle (variante (a))

- Gènes v4 (les 12 mêmes que TCGA v4, ordre de la liste) :
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1,
  CEACAM5, CLCA1, MUC16.
- Contrôle : KRAS (expression, croissant). Le contrôle n'est
  JAMAIS un flux : pas de doublon. Justification de l'ordre
  KRAS : identique aux paires principales V1 — KRAS est le
  contrôle monotone du projet, et l'ordre par son expression
  est celui de toutes les paires GEO à 12 gènes.
- Tumeurs seules : lot Yeh_seq, `sample type: FF` ET kind `Pi`
  (primaire) dans les titres `S###.FF.Pi.######` (47 colonnes
  attendues) ; les 28 PDX, les 45 FNA primaires et les 5 FFPE
  primaires sont exclus et comptés (§2.4).
- **Unité = tumeur indépendante (§4.4).** Les 47 colonnes FF
  primaires sont regroupées par code-tumeur (`MMDDT#`, 42
  codes) ; pour les 4 codes à réplicats FF (0417T1, 0523T1,
  0806T1, 1119T1), la valeur retenue par gène est la MÉDIANE
  des réplicats FF (précédent du projet : agrégation par
  médiane). Le code 0921T1 (FNA seul) n'entre pas dans le lot
  FF.
- Cas complets seulement (KRAS + 12 gènes présents), jamais
  d'imputation. Enquête : 0 NaN, 0 cellule vide sur les 13
  lignes × 125 colonnes du fichier Yeh — 42/42 cas complets
  attendus.
- Sorties : `pdac_874_yeh_ff_fluxes.csv` (+ `_nul.csv`).
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
**8741** et **8742** (graines jamais utilisées dans ce projet,
gelées ici avant tout run), et courus en runs frais
(`pdac_874_yeh_ff_fluxes_nul_s8741.csv`,
`pdac_874_yeh_ff_fluxes_nul_s8742.csv`,
`results_fast_v62_874_yeh_ff_nul_s8741`,
`results_fast_v62_874_yeh_ff_nul_s8742`). Le verdict reste
celui de la paire graine 42 (§7) ; les nuls frais sont un
contrôle de robustesse descriptif (min / médiane / max des
écarts), jamais un moyen de choisir le nul qui arrange.

## 5. Critères d'acceptation de la cohorte (vérifiés après téléchargement officiel, avant construction)

- Fichiers téléchargés, HTTP 200, lecture complète vérifiée
  (nombre de lignes, NaN comptés) ; SHA-256 consignés dans
  `PROVENANCE_874.md` avant toute construction. SHA attendus
  (copies d'enquête) : Yeh_seq `2fc0a66e…be5b1`,
  Linehan_seq `729bb794…efc16`, matrice GPL18573
  `9b333eb6…7843e`, matrice GPL16791 `03aa8ca6…1df94` — tout
  écart est consigné et les portes sont re-vérifiées.
- Plateforme lue dans l'en-tête de la matrice du lot Yeh :
  GPL18573 ; sinon ARRÊT (§3).
- n ≥ 40 tumeurs PDAC indépendantes (codes-tumeurs distincts,
  lot Yeh FF) ; sinon ARRÊT (§3).
- Aucun échantillon porteur d'un code-barres TCGA ou déjà
  présent dans une cohorte du projet (GSM/titres inspectés) ;
  sinon ARRÊT (§3). (Caveat §2.2.3 : titres anonymisés.)
- KRAS présent comme ligne mappée ; sinon ARRÊT (§3).
- Les 12 gènes v4 présents (une ligne chacun, symbole exact
  après `;`) ; sinon ARRÊT (§3) (aucun gène remplacé, aucun
  absent toléré pour une paire principale — la comparabilité
  aux 11 paires comptées l'exige).
- Cas complets (KRAS + 12 gènes) ≥ 40 ; sinon ARRÊT (§3).

## 6. Runs v6.2 (mode fast)

- Lot : 2 runs — réel + nul — manifeste `manifest_v62_874.txt`,
  lanceur reprenable existant `run_v62_lot.sh` (saute les sorties
  déjà complètes), journal `runs_v62_874.log` (SHA du pipeline
  en tête, exits consignés).
- Dossiers : `results_fast_v62_874_yeh_ff` et
  `results_fast_v62_874_yeh_ff_nul` (nuls frais éventuels :
  `results_fast_v62_874_yeh_ff_nul_s8741` /
  `..._s8742`).
- Lancement en `systemd-run --unit=v62-874 --collect`
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

**Verdict étendu (A2 à 12 paires) :**
- Si la paire passe : A2 étendu = **8/12 au-dessus du plancher,
  10/12 positifs** (les 11 paires gardent leurs valeurs : 7/11
  et 9/11 positifs). **C3 reste LEVÉE** — elle l'était déjà
  depuis le §8.71 ; ce chantier est une confirmation
  supplémentaire, pas une condition. Le leave-one-out sur les
  12 paires est calculé en descriptif : retirer n'importe
  quelle paire passante laisse 7/11, qui satisfait encore la
  barre A2 d'origine (≥ 6/8).
- Si la paire est PARTIELLE : A2 étendu = **7/12, 10/12
  positifs**. C3 reste LEVÉE.
- Si la paire échoue (NON) : A2 étendu = **7/12, 9/12 positifs**.
  C3 reste LEVÉE, et l'adoption pleine reste la décision de
  Zackary du 20 nov. 13h04 — ce chantier ne la rouvre pas et
  ne la conditionne pas.

**Nuls frais (§4.4, règle gelée).** La paire graine 42 fait le
verdict, dans tous les cas. Si `d_maxsep` est PROCHE du
plancher — défini ici comme `d_maxsep` dans [−0,07 ; +0,14[,
soit à moins d'une largeur de plancher du seuil, de part et
d'autre — les 2 nuls frais (graines 8741, 8742) sont courus et
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
- Falsification : INDISPONIBLE sous n = 75 — GSE131050 Yeh FF
  n = 42 : noter « indisponible », ne pas imputer.
- Plancher équivalent-sep (descriptif) : la paire passe-t-elle
  aussi `0,07·(1+m_R)(1+m_N)` ? Rapporté, non décisif (D4 n'est
  pas rejoué ici : il porte sur les paires V1, déjà tranché).
- Aucun autre critère, aucune repondération, aucune redéfinition
  du plancher après avoir vu les chiffres.

## 8. Extraction et vérification

1. Extracteur propre du chantier, `extract_874.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_866.py` / `extract_869.py` / `extract_871.py`) ;
   lit `maxsep`, `mc_score`, `stability`, `ssep`, `delta`, `l7a`,
   cascade, falsification dans les 2 (ou 4)
   `master_results.json` ; sorties `extract_874.json` /
   `extract_874.csv`.
2. Second calcul indépendant : relecture directe des
   `master_results.json` par un chemin distinct (script
   `verify_874.py`, SHA noté) — `maxsep` et ancien MC recoupés
   à 0,0 exact ; tout écart = résultat à diagnostiquer, pas un
   bruit.
3. Recoupements : les 11 valeurs déjà comptées reprises telles
   quelles du §8.56 (table `sep_maxsep_856_table.json`, SHA
   `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`),
   du §8.69 (`extract_869.json`, SHA
   `644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b`),
   du §8.70 (`extract_870.json`, SHA
   `4ffa851a83668b2369097703862e0413ff9af54af3a66ef70aea9333b40c444f`)
   et du §8.71 (`extract_871.json` — SHA à consigner dans la
   section), jamais recalculées ici — ce chantier ne re-vérifie
   pas les §8.56/§8.59/§8.64/§8.69/§8.70/§8.71 (déjà clos).
4. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 9. Tests directs en appui (ne décident pas)

Script `direct_tests_874.py` (SHA noté), sur les CSV de flux
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
   exactement ses 42 valeurs — la médiane des réplicats est
   prise AVANT la permutation, donc les marginales sont
   préservées exactement). Rapporté tel quel : il valide la
   construction du nul (marginales préservées exactement),
   il ne mesure pas la séparation.
3. Si l'ordre est KRAS (cas attendu) : comparaison descriptive
   avec les §8.69/§8.70/§8.71 — au §8.69, Delta +2,01 contre
   maxsep −0,01 ; au §8.70, Delta plat +0,05 contre maxsep
   +0,06 ; au §8.71, Delta plat −0,015 contre maxsep +0,2045.
   Si une divergence Delta/`maxsep` apparaît ici, elle est
   nommée telle quelle, sans être élucidée sans preuve ; si
   elle n'apparaît pas, c'est consigné aussi.
4. Aucun de ces tests ne change le verdict du §7.

## 10. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et le
  jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict : les tests directs des §8.66/§8.70/§8.71, les
  sous-types PurIST publiés, les scores publiés ne prédisent
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
- `PROVENANCE_874.md` (source, auteur, date, dépôt, URL, SHA-256
  des fichiers téléchargés, plateforme réelle, effectifs, exclus,
  identification des gènes — avec la vérification d'indépendance
  du §2.2, le compte rendu de l'enquête préalable §2.2/§2.3 et
  la structure appariée §2.4).
- `build_fluxes_874.py` + CSV de flux (`pdac_874_*`, SHA consignés).
- `manifest_v62_874.txt`, `runs_v62_874.log`, dossiers
  `results_fast_v62_874_*`, `extract_874.json` / `.csv`,
  `verify_874.py` + sortie de vérification,
  `direct_tests_874.py` + sortie.
- §8.74 dans le FICHIER SÉPARÉ
  `section_8.74_gse131050.md` (verdict d'abord, une phrase :
  CONFIRME / PARTIEL / NON ; chiffres ensuite ; détail complet
  après ; provenance nommée partout ; C3 reste levée dans tous
  les cas).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin du protocole gelé §8.74. —
