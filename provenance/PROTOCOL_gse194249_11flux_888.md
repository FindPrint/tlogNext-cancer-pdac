# PROTOCOLE GELÉ — §8.88 : GSE194249 à 11 flux, paire principale indépendante (suite du §8.86)

Date : 21 novembre 2026, ~10h10 EST. Chantier §8.88, piste 2 du lot du
21 nov. 2026. Go de Zackary : 21 nov. 2026, 10h07.
Protocole gelé AVANT toute construction de CSV et tout run. Aucun
paramètre ne change après les résultats. Le livre blanc N'EST PAS
édité, le PDF N'EST PAS régénéré, rien n'est poussé sur GitHub dans
ce chantier (convention des chantiers ; fusion par le coordinateur).
La section §8.88 est écrite dans un FICHIER SÉPARÉ
(`section_8.88_gse194249_11flux.md`).
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
- §8.71 : C3 LEVÉE (GSE60979, onzième paire, CONFIRME).
- 20 nov. 2026, 13h04 : Zackary a décidé d'**ADOPTER maxsep
  pleinement** (maxsep score principal, MC secondaire, aucun
  changement de code).
- §8.79 : treizième paire, GSE57495, **CONFIRME**
  (`d_maxsep = +0,4494`, **11 flux, GSTM1 absent**) ; A2 **9/13
  au-dessus du plancher, 11/13 positifs**, LOO 8/12. **C3
  RESTE LEVÉE.** C'est le précédent direct du présent chantier :
  une paire à 11 flux compte dans A2, avec son caveat écrit.
- §8.85 : quatorzième paire, GDC ORGANOID-PANCREATIC,
  **CONFIRME, FRAGILE ET NON CONSOLIDÉ**
  (`d_maxsep = +0,0884`, 12 flux dont MUCL3 ex-DPCR1) ; A2
  **10/14 au-dessus du plancher, 12/14 positifs**, LOO 9/13.
  **C3 RESTE LEVÉE.**
- §8.86 : GSE194249 (84 PDPCOs, Shi et al., Nat. Commun. 2022)
  **INUTILISABLE comme paire à 12 flux** — DPCR1 absent de la
  matrice FPKM déposée (0/15 609 lignes, vérifié par deux
  chemins indépendants), MUCL3 également absent, **0 run,
  0 CSV**. A2 inchangé à ce moment (10/14 après §8.85 — voir
  la correction datée du §8.86). Piste fermée comme paire à
  12 flux, avec deux suites nommées au §8.86.4 (d) : (d1) une
  paire à **11 flux** (sans DPCR1), « comme la C3 du §8.79,
  avec son caveat écrit », sous son propre protocole gelé et
  avec un go ; (d2) une re-dérivation depuis les lectures
  brutes (SRA). **Le présent chantier EST la suite (d1).**
- **Ce chantier ne rouvre pas C3, quelle que soit son issue.**
  Si la paire passe, elle consolide l'adoption par une
  quinzième paire indépendante ; si elle échoue, l'adoption
  pleine reste la décision de Zackary du 20 nov. 13h04 — à dire
  plainement dans les deux cas, dans la section comme dans le
  rapport. Ce chantier ne rouvre pas les §8.56/§8.59/§8.64/
  §8.69/§8.70/§8.71/§8.74/§8.76/§8.79/§8.85/§8.86 et ne change
  aucune décision de Zackary.
- §8.70/§8.72 : correction de méthode notée au §8.70 (§8.70.5,
  §8.70.7) et APPLIQUÉE ici (§9) : le test de Cohen marginal
  est vacueux par construction quand le nul est une permutation
  de lignes (d = 0,0000 pour les 11 gènes) — le test informatif
  est le Spearman de chaque flux contre le pas (Δρ médian,
  nombre de positifs). Le Cohen marginal est quand même rapporté
  (il valide la construction du nul), mais il ne porte aucune
  information d'ordre et ne décide rien.

## 1. Les 14 paires principales indépendantes déjà comptées

Valeurs reprises des §8.56/§8.69/§8.70/§8.71/§8.74/§8.79/§8.85,
jamais recalculées. Écart = maxsep réel − maxsep nul. Plancher 0,07.

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
| GDC ORGANOID-PANCREATIC (§8.85, 12 flux, MUCL3 ex-DPCR1) | 0,2542 / 0,1658 | **+0,0884** | oui | oui |

Bilan : **10/14 au-dessus du plancher, 12/14 positifs.** LOO
9/13. Rotations V2 (48 paires, §8.44, sans doublon) : 37/48
pour `maxsep`. Elles ne sont PAS rejouées ici.

## 2. La dérogation à la porte « 12 gènes v4 » — justifiée ici, avant tout run

### 2.1 Ce que dit la porte, et pourquoi elle est levée pour ce chantier

La porte gelée « 12 gènes v4 présents » (§5 du protocole §8.86)
a dit ARRÊT pour GSE194249 comme paire à 12 flux. Cette porte
protège la comparabilité des paires à 12 flux. La lever sans
règle serait un changement de protocole après avoir vu
l'échec — ce qui est interdit. Ce qui est fait ici est
différent, et c'est le même geste que le §8.79 (addendum C3,
GSE57495 à 11 flux, GSTM1 absent) :

1. **La dérogation est écrite AVANT toute construction et
   tout run du présent chantier**, dans ce protocole gelé,
   avec un go explicite de Zackary (21 nov. 2026, 10h07).
2. **Elle est limitée à un seul gène, nommé : DPCR1.** Aucun
   autre gène n'est remplacé, mappé à la main, ou toléré
   absent (§5).
3. **L'absence est un fait du fichier déposé, vérifié deux
   fois au §8.86 et re-vérifié deux fois ici avant ce gel**
   (§2.2) : DPCR1 0 occurrence, MUCL3 0 occurrence. Aucun
   remappage n'est fait — le gène n'est mesuré sous aucun
   nom dans la matrice déposée, donc il n'y a rien à mapper.
4. **La comparabilité est limitée, et c'est dit plainement
   partout où la paire est comptée** : la paire est étiquetée
   « 11 flux, DPCR1 absent » dans chaque table, et la
   section §8.88 porte ce caveat dans son verdict même.
5. **Le précédent existe et a compté** : GSE57495 (§8.79,
   11 flux, GSTM1 absent) est la treizième paire du compte
   A2, avec exactement ce statut. Une paire à 11 flux n'est
   donc pas une invention de ce chantier : c'est une forme
   déjà comptée, avec sa règle déjà écrite.
6. **La suite était pré-nommée** : le §8.86.4 (d1) nomme
   explicitement « une paire à 11 flux (sans DPCR1), comme
   la C3 du §8.79, avec son caveat écrit » comme suite
   possible, « sous son propre protocole gelé et avec un
   go ». Ce protocole est ce protocole-là ; le go est celui
   du 21 nov. 10h07.

### 2.2 Présence des gènes, vérifiée dans la matrice détenue AVANT ce gel

Matrice détenue : `data/GSE194249_PDPCOs_FPKM.txt.gz`,
4 927 876 o, SHA-256
`479517fbed1d8f5bb9d141b6b932b6ab56ba2ba72d4394d13aea2a3da0a50f27`
— identique au §8.86 (re-vérifié le 21 nov. 2026, ~10h05 EST,
avant ce gel). 15 609 lignes de gènes, 88 colonnes
(`GeneSymbol` + 87 échantillons : 84 `CAS-*` + 3 `NPC-*`),
0 symbole dupliqué.

**Premier chemin (lecture pandas, script de vérification
adhoc, 21 nov. 2026 ~10h05 EST) ; second chemin (zgrep sur
le fichier brut gzip, même jour) — les deux donnent les
mêmes comptages :**

| Gène | Lignes exactes | Statut | Gène | Lignes exactes | Statut |
|---|---|---|---|---|---|
| PGC | 1 | PRÉSENT | CR2 | 1 | PRÉSENT |
| REG4 | 1 | PRÉSENT | KRT20 | 1 | PRÉSENT |
| CLDN18 | 1 | PRÉSENT | MUC2 | 1 | PRÉSENT |
| MUC17 | 1 | PRÉSENT | GSTM1 | 1 | PRÉSENT |
| **DPCR1** | **0** | **ABSENT** | CEACAM5 | 1 | PRÉSENT |
| CLCA1 | 1 | PRÉSENT | MUC16 | 1 | PRÉSENT |
| KRAS (contrôle) | 1 | PRÉSENT | MUCL3 (descriptif) | 0 | ABSENT |

**11/11 gènes v4 retenus présents, une ligne chacun, 0
doublon ; KRAS présent, une ligne. DPCR1 : 0 occurrence
dans tout le fichier (exact, insensible à la casse) ;
MUCL3 : 0 ; aucun symbole contenant `DPCR`.** Aucun autre
gène ne manque : si un douzième gène manquait aussi, le
chantier s'arrêterait sur un blocage documenté (§3) — ce
n'est pas le cas, les 11 sont vérifiés un par un ci-dessus.

### 2.3 Décision écrite AVANT les runs : cette paire compte dans A2

**DÉCISION GELÉE : la paire GSE194249 à 11 flux ENTRE dans
le compte A2 comme quinzième paire principale
indépendante, avec le caveat « 11 flux, DPCR1 absent »
écrit dans chaque table.** Cette décision est prise avant
tout run, pas après avoir vu les chiffres, et elle ne sera
pas révisée selon l'issue.

Justification, écrite avant les runs :

- **Précédent §8.79 :** GSE57495, paire d'expression à
  11 flux (GSTM1 absent), compte dans A2 comme treizième
  paire. Le présent chantier est le même objet : une paire
  d'expression ordonnée par KRAS, sur une cohorte
  indépendante jamais courue, avec un flux v4 absent du
  fichier déposé et un caveat écrit. Appliquer une règle
  différente ici, sans raison nouvelle, serait incohérent.
- **Différence avec le §8.84 (hors compte) :** le §8.84 est
  un lot drogue (46 PDO × réponses AUC, n = 46, objet
  différent : sensibilité aux médicaments, pas une paire
  d'expression ordonnée par KRAS) — c'est pour cela qu'il
  est hors compte. Ici l'objet est une paire d'expression,
  n = 84 PDPCOs, comme les 14 paires comptées.
- **n = 84, au-dessus de tous les minimums** (40 pour le
  mode fast v6.2 ; 75 pour la falsification) : la taille ne
  plaide pas pour une exclusion.
- **Le caveat est le prix de l'inclusion, pas une
  dispense :** « 11 flux » est écrit dans le verdict, dans
  la table A2, et dans la provenance ; toute lecture future
  qui présenterait cette paire comme une paire à 12 flux
  serait fausse.

**Ce que le verdict change (gelé, à compter sur les chiffres
mesurés, pas à pré-écrire) :**
- Si CONFIRME : A2 devient **11/15 au-dessus du plancher,
  13/15 positifs** ; LOO recalculé sur 15 paires (pire cas
  sur 14 : **10/14**).
- Si PARTIEL : A2 devient **10/15 au-dessus du plancher,
  13/15 positifs** ; LOO **9/14**.
- Si NON : A2 devient **10/15 au-dessus du plancher,
  12/15 positifs** ; LOO **9/14**.
- Dans tous les cas, la paire entre dans le compte A2 :
  c'est une paire principale indépendante (contrairement au
  lot FNA §8.76, apparié). **C3 reste LEVÉE** dans tous les
  cas — elle l'était déjà depuis le §8.71 ; ce chantier est
  une consolidation supplémentaire, pas une condition.
- Le leave-one-out sur les paires indépendantes est
  recalculé ici (il change : la paire y entre).

## 3. Arrêt borné — AUCUNE cohorte de repli courue dans ce chantier

**Une seule cohorte dans ce chantier : GSE194249, lignées
PDPCO de la matrice FPKM déposée, n attendu = 84.** Si elle
est INUTILISABLE selon les critères d'acceptation du §5
(matrice SHA différente de celle du §8.86, mise en page non
(A), n PDPCO < 40, KRAS absent, < 11 gènes v4 présents,
DPCR1 PRÉSENT — ce qui contredirait le fichier vérifié —,
< 40 cas complets), le chantier s'arrête sur un blocage
documenté : section §8.88 écrite quand même, avec les
tentatives chiffrées, aucune valeur inventée, et la piste
fermée (la suite (d2) — re-dérivation SRA — reste nommée
comme piste seulement, aucun run lancé pour elle dans ce
chantier). Il n'y a PAS de cohorte #2 courue dans ce
chantier.

## 4. Construction des flux — variante (a) à 11 flux, comme §8.79 C3

Nouveau script `build_fluxes_888.py` (copie adaptée de
`build_fluxes_886.py`, original intact — la porte « 12
gènes » de l'original ne s'applique pas ici ; tout le reste
est repris). Préfixe `_888_` pour tous les fichiers du
chantier.

### 4.1 Source (aucun nouveau téléchargement)

- Matrice détenue : `data/GSE194249_PDPCOs_FPKM.txt.gz`,
  4 927 876 o, SHA-256
  `479517fbed1d8f5bb9d141b6b932b6ab56ba2ba72d4394d13aea2a3da0a50f27`
  (vérifié avant ce gel, re-vérifié §5). 15 609 lignes de
  gènes, 88 colonnes, mise en page (A), 0 symbole dupliqué.
- Métadonnées : `gse194249_esummary_886.json`, SHA-256
  `73934e46a717a5db1ed8cd8e1c4349435683a0eed1dda85fe7b097ec448f460e`
  (87 échantillons : 75 `CAS-DAC-*`, 4 `CAS-NEN-*`,
  4 `CAS-IPMN-*`, 1 `CAS-ACC-1`, 3 `NPC-*`).
- **Aucun nouveau téléchargement** : la matrice et les
  métadonnées sont celles du §8.86, re-vérifiées par SHA.
  Les suppléments de réponse aux médicaments (Suppl. Data 8,
  MOESM11) et de suivi clinique (Suppl. Data 10, MOESM13)
  ne sont PAS téléchargés (hors périmètre de la paire).

### 4.2 Identification des gènes

- Symboles exacts, sensibles à la casse ; symboles dupliqués
  agrégés par **médiane** (précédent §8.79, §8.86) — règle
  gelée avant de voir les doublons (0 attendu, vérifié §2.2).
- Valeurs : **FPKM telles que déposées**, aucune
  renormalisation, aucune transformation log, aucune
  imputation ajoutée.
- Colonnes : les 87 titres correspondent aux 87 échantillons
  de l'esummary (§8.86). Toute colonne `NPC-*` (normal) est
  **EXCLUE** et comptée (attendu : 3 colonnes exclues).
  Toute autre colonne non-PDPCO serait exclue de la même
  façon et nommée. Les colonnes retenues sont les PDPCOs.

### 4.3 Série réelle (variante (a), 11 flux)

- Gènes v4 retenus (11, ordre de la liste, DPCR1 absent) :
  PGC, REG4, CLDN18, MUC17, CR2, KRT20, MUC2, GSTM1,
  CEACAM5, CLCA1, MUC16.
- Contrôle : KRAS (expression FPKM, croissant). Le contrôle
  n'est JAMAIS un flux : pas de doublon. Justification de
  l'ordre KRAS : identique aux paires principales V1 — KRAS
  est le contrôle monotone du projet, et l'ordre par son
  expression est celui de toutes les paires GEO.
- Lignes retenues : les **PDPCOs de la matrice** (attendu
  84) ; les normaux `NPC-*` sont exclus et comptés (§4.2).
- **Unité = lignée organoïde.** Chaque titre est une lignée
  distincte d'un patient distinct (article : 84 lignes de
  138 patients sources, une ligne par patient retenu —
  aucune lignée en double d'un même patient n'est
  documentée ; si la matrice révélait des doublons de
  patient, ils seraient nommés tels quels dans la section,
  sans ré-agrégation).
- Cas complets seulement (KRAS + 11 gènes présents), jamais
  d'imputation. Attendu : 84/84 cas complets (0 NaN attendu
  sur les 12 lignes × 84 colonnes — vérifié, sinon ARRÊT
  si < 40 complets).
- Tri : KRAS FPKM croissant ; `step` = rang 0..n−1.
- Sorties : `pdac_888_gse194249_fluxes.csv` (+ `_nul.csv`).
  Colonnes : `step` + 11 flux. SHA-256 consignés.

### 4.4 Nul

Bloc des flux permuté par lignes, graine 42, `rng(42)`,
contrôle (ordre KRAS, `step`) intact — même convention que
les paires V1 (§8.56.8, PROTOCOL_phase2 §2). Le nul est un
échantillon hypothétique, pas une mesure.

### 4.5 Nuls frais (conditionnels, §7)

Si et seulement si l'écart mesuré sur la paire graine 42 est
PROCHE du plancher (§7 : `d_maxsep` dans [−0,07 ; +0,14[),
2 nuls frais sont construits par la même méthode, graines
**8881** et **8882** (gelées ici avant tout run, vérifiées
libres le 21 nov. 2026 ~10h10 EST — aucun fichier
`s8881`/`s8882` dans le dossier de runs ; la série s8871–
s8880 appartient au chantier §8.85, autre objet), et courus
en runs frais (`pdac_888_gse194249_fluxes_nul_s8881.csv`,
`pdac_888_gse194249_fluxes_nul_s8882.csv`,
`results_fast_v62_888_gse194249_nul_s8881`,
`results_fast_v62_888_gse194249_nul_s8882`). Le verdict
reste celui de la paire graine 42 (§7) ; les nuls frais sont
un contrôle de robustesse descriptif (min / médiane / max des
écarts), jamais un moyen de choisir le nul qui arrange.

## 5. Critères d'acceptation de la cohorte (vérifiés sur le fichier détenu, avant construction)

- Matrice SHA-256 `479517fb…0f27` (re-vérifié, identique au
  §8.86) ; taille 4 927 876 o ; gzip intègre ; sinon ARRÊT (§3).
- Mise en page = (A) du §4.2 (col1 = `GeneSymbol`) ; sinon
  ARRÊT (§3).
- n ≥ 40 colonnes PDPCO retenues (après exclusion des
  normaux `NPC-*`) ; sinon ARRÊT (§3).
- Aucune colonne porteuse d'un code-barres TCGA ou déjà
  présente dans une cohorte du projet (vérifié par les titres
  §2.2/§8.86 : `CAS-*` / `NPC-*` uniquement) ; sinon ARRÊT (§3).
  (Caveat §2.4 du protocole §8.86, repris : le
  non-recouvrement est établi par programme et système
  d'identifiants, pas par jointure.)
- KRAS présent comme ligne mappée (symbole exact) dans la
  matrice ; sinon ARRÊT (§3).
- **Les 11 gènes v4 retenus présents** (une ligne chacun après
  agrégation des doublons par médiane, symbole exact) **ET
  DPCR1 absent** ; sinon ARRÊT (§3) (aucun gène remplacé,
  aucun autre absent toléré ; si DPCR1 apparaissait, c'est
  consigné et la construction s'arrête — la paire
  pré-enregistrée est à 11 flux, pas à 12).
- Cas complets (KRAS + 11 gènes) ≥ 40 ; sinon ARRÊT (§3).

## 6. Indépendance — vérifiée par grep AVANT le gel

- Livre blanc (`livre-blanc-pdac-v6.md`, copie de travail du
  projet, 21 nov. 2026 ~10h05 EST) : « GSE194249 » : 34
  occurrences, toutes au §8.78 (inventaire C4), au §8.79.9
  (piste ouverte (d)) et au §8.86 — jamais comme cohorte
  courue, jamais comme holdout, jamais comme valeur
  `maxsep`. « Shi et al » : 4 occurrences, toutes dans le
  §8.86. « PDPCO » : 20 occurrences, toutes au §8.78/§8.86.
  « CAS-DAC » : 2 occurrences, toutes dans le §8.86.
- Dossier de runs (`~/workspace/runs/pdac-v6/`) : aucun
  CSV `pdac_886_*`, aucun dossier `results_fast_v62_886_*`,
  aucun manifeste, journal ou extraction `886` — **0 run
  jamais lancé pour GSE194249** (confirmé par l'absence des
  fichiers, comme au §8.86). Les seuls fichiers contenant
  « 194249 » dans leur nom sont ceux du §8.86 (protocole,
  provenance, téléchargement, reçu, esummary, section).
- Patients distincts par construction de programme : biobanque
  PDPCO de Shanghai (Changhai Hospital, Second Military
  Medical University), échantillons prélevés par chirurgie
  ou EUS-FNA, identifiants `CAS-DAC-*` / `CAS-NEN-*` /
  `CAS-IPMN-*` / `CAS-ACC-1` / `NPC-*` — système
  d'identifiants sans aucun recouvrement possible par
  jointure avec les cohortes tenues (barres TCGA
  `TCGA-XX-XXXX`, GSM GEO des autres séries, ICGC). Aucun
  lien documenté avec TCGA PAAD, ICGC PACA-AU, GSE71729,
  GSE62452, GSE62165, GSE21501, GSE79668, GSE60979,
  GSE131050, GSE57495, ni avec les organoïdes GDC HCMI
  (programme américain distinct, §8.79), ni avec les PDO de
  Chen et al. 2025 (autre article, autre cohorte, 46 PDO),
  ni avec Tiriac et al. 2018 (CSHL).
  **Limite déclarée :** aucun identifiant commun n'existe
  entre les deux systèmes, donc le non-recouvrement ne peut
  pas être prouvé par une jointure d'identifiants — il est
  établi par programme, par système d'identifiants et par
  absence de tout lien documenté ; c'est une limite, pas une
  preuve formelle. (Même caveat que §8.79 §2.2 point 2 et
  §8.86 §2.4.)
- Pas un re-test déguisé : ni une relecture d'un JSON
  existant, ni une rotation déjà comptée, ni un sous-ensemble
  d'une paire V1, ni un nouvel ordre sur des CSV existants
  (nouveaux CSV, nouveaux runs, 2 runs v6.2 frais, données
  jamais courues).
- Statut de la cohorte : transversale, ordonnée par un flux
  (KRAS, comme TCGA/ICGC) — même statut que les paires
  TCGA/ICGC, pas de pseudo-temps. Les PDPCO sont des modèles
  organoïdes dérivés de patients, pas des tumeurs primaires
  directes : c'est dit plainement au §8.88, et le verdict
  porte sur l'instrument, pas sur une affirmation clinique.
- **Composition histologique gelée comme limite :** la série
  déposée compte 75 PDAC et 9 autres tumeurs (4 NEN, 4 IPMN,
  1 ACC). La cohorte primaire est la série déposée entière
  (§4.3) ; la mixité est déclarée, et une annexe descriptive
  PDAC-seul est pré-enregistrée (§9.3) — elle ne décide rien.

## 7. Runs v6.2 (mode fast)

- Lot : 2 runs — réel + nul — manifeste `manifest_v62_888.txt`,
  lanceur reprenable existant `run_v62_lot.sh` (saute les sorties
  déjà complètes), journal `runs_v62_888.log` (SHA du pipeline
  en tête, exits consignés).
- Dossiers : `results_fast_v62_888_gse194249` et
  `results_fast_v62_888_gse194249_nul` (nuls frais éventuels :
  `results_fast_v62_888_gse194249_nul_s8881` /
  `..._s8882`).
- Lancement en `systemd-run --unit=v62-888 --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance qui
  s'arrête d'elle-même à 2/2 (ou 4/4 si nuls frais). Ne JAMAIS
  supprimer le dossier d'un run en cours. Si la machine
  redémarre, reprise sans perte (SKIP des dossiers complets,
  jamais de relance à l'aveugle).
- SHA du pipeline revérifié avant ET après le lot.
- Durée attendue : ~5 min par run (référence §8.86 §6 :
  n=84, prévoir ~5 min/run) ; le lot complet tient en
  ~15 min hors construction.

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
- **CONFIRME** : `d_maxsep > 0,07` — quinzième paire
  indépendante passante (11 flux, caveat DPCR1 écrit).
- **PARTIEL** : `0 < d_maxsep ≤ 0,07` — positif mais sous le
  plancher (même catégorie que GSE71729, +0,0402, et GSE79668,
  +0,0567).
- **NON** : `d_maxsep ≤ 0` — négatif ou nul (même catégorie que
  GSE62452 et GSE21501).

**Nuls frais (§4.5, règle gelée).** La paire graine 42 fait le
verdict, dans tous les cas. Si `d_maxsep` est PROCHE du
plancher — défini ici comme `d_maxsep` dans [−0,07 ; +0,14[,
soit à moins d'une largeur de plancher du seuil, de part et
d'autre — les 2 nuls frais (graines 8881, 8882) sont courus et
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

## 9. Extraction et vérification

1. Extracteur propre du chantier, `extract_888.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_885.py`) ; lit `maxsep`, `mc_score`,
   `stability`, `ssep`, `delta`, `l7a`, cascade, falsification
   dans les 2 (ou 4) `master_results.json` ; sorties
   `extract_888.json` / `extract_888.csv`.
2. Second calcul indépendant : relecture directe des
   `master_results.json` par un chemin distinct (script
   `verify_888.py`, SHA noté) — `maxsep` et ancien MC recoupés
   à 0,0 exact ; tout écart = résultat à diagnostiquer, pas un
   bruit.
3. Recoupements : les 14 valeurs déjà comptées reprises telles
   quelles du §8.56 (table `sep_maxsep_856_table.json`, SHA
   `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`),
   du §8.69 (`extract_869.json`, SHA
   `644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b`),
   du §8.70 (`extract_870.json`, SHA
   `4ffa851a83668b2369097703862e0413ff9af54af3a66ef70aea9333b40c444f`),
   du §8.71 (`extract_871.json`, SHA
   `85e9089a…55e3b`), du §8.74 (`extract_874.json`, SHA
   `82ade74701245021dfdb965bdc689ac98262c70f12ecec7f39e1b5b742dfcb47`),
   du §8.79 (`extract_879_c3.json`, valeurs §8.79.2) et du
   §8.85 (`extract_885.json`, valeurs §8.85.2), jamais
   recalculées ici — ce chantier ne re-vérifie pas les
   §8.56/§8.59/§8.64/§8.69/§8.70/§8.71/§8.74/§8.76/§8.79/§8.85
   (déjà clos).
4. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 10. Tests directs en appui (ne décident pas)

Script `direct_tests_888.py` (SHA noté), sur les CSV de flux
du chantier (réel + nul graine 42) :
1. **Test informatif (correction §8.70, appliquée ici) :**
   corrélation de Spearman de chaque flux avec le pas (ordre
   KRAS), réel vs nul : |ρ| moyen, Δρ médian, nombre de Δρ
   positifs (sur 11), table complète sans sélection. C'est le
   test qui porte l'information d'ordre.
2. d de Cohen marginal des 11 flux (réel vs nul) : pour chaque
   gène v4 retenu, moyenne et écart-type des valeurs ordonnées,
   d de Cohen réel−nul ; table complète, sans sélection.
   **Attendu vacueux par construction : d = 0,0000 pour les
   11 gènes** (le nul est une permutation des lignes, chaque
   flux garde exactement ses 84 valeurs). Rapporté tel quel :
   il valide la construction du nul (marginales préservées
   exactement), il ne mesure pas la séparation.
3. Comparaison descriptive avec les paires précédentes
   (Δρ médian, 11/11 positifs au §8.79 ; 8/12 au §8.85 ;
   valeurs reprises telles quelles, jamais recalculées). Si le
   signal d'ordre est plus faible, c'est consigné tel quel,
   sans être élucidé sans preuve ; si une divergence
   Delta/`maxsep` apparaît ici, elle est nommée telle quelle.
4. Aucun de ces tests ne change le verdict du §8.

### 10.3 Annexe descriptive pré-enregistrée — PDAC seul (ne décide rien, aucun run)

Parce que la série déposée compte 9 lignées non-PDAC sur 84
(4 NEN, 4 IPMN, 1 ACC — §6), une annexe descriptive est
pré-enregistrée (reprise du §9.3 du protocole §8.86) : sur
les valeurs FPKM de la matrice détenue, Spearman de chaque
flux contre le rang KRAS **au sein des seules lignées
`CAS-DAC-*`** (n attendu 75), réel seulement (pas de nul,
pas de run pipeline). Rapportée comme table complète
(ρ PDAC-seul par gène, médiane, nombre de positifs), elle
répond à la question « le signal d'ordre survit-il sans les
9 lignées non-PDAC ? » sans toucher au verdict du §8, qui
reste celui de la paire sur les 84 PDPCOs. Aucune autre
découpe histologique n'est calculée.

## 11. Règles du projet rappelées

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
- **Compter cette paire comme quinzième paire indépendante
  UNIQUEMENT si les portes du §5 sont passées** (n PDPCO ≥ 40,
  11/11 gènes retenus, DPCR1 absent, n ≥ 40 cas complets).
  Toute lecture future qui compterait aussi les 3 normaux
  `NPC-*` serait fausse, et toute lecture qui présenterait
  cette paire comme une paire à 12 flux serait fausse.

## 12. Livrables

- Ce protocole (gelé avant construction et runs).
- `PROVENANCE_888.md` (source, auteur, date, dépôt, URL, SHA-256
  de la matrice, plateforme, effectifs, exclus, identification
  des gènes un par un, vérifications d'indépendance du §6,
  décision A2 du §2.3).
- `build_fluxes_888.py` + CSV de flux (`pdac_888_*`, SHA
  consignés) + audit `build_fluxes_888_audit.json`.
- `manifest_v62_888.txt`, `runs_v62_888.log`, dossiers
  `results_fast_v62_888_*`, `extract_888.json` / `.csv`,
  `verify_888.py` + sortie de vérification,
  `direct_tests_888.py` + sortie.
- §8.88 dans le FICHIER SÉPARÉ
  `section_8.88_gse194249_11flux.md` (verdict d'abord, une phrase :
  CONFIRME / PARTIEL / NON ; chiffres ensuite ; détail complet
  après ; provenance nommée partout ; C3 reste levée dans tous
  les cas ; A2 recalculé sur 15 paires, dit explicitement, avec
  le caveat 11 flux).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin du protocole gelé §8.88. —
