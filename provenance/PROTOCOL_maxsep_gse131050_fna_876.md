# PROTOCOLE GELÉ — §8.76 : Tester GSE131050 (PurIST), lot Yeh_seq FNA, comme test de robustesse APPARIÉ pour `maxsep`

Date : 20 novembre 2026, ~21h30 EST. Chantier §8.76, piste
nommée au §8.74.9 (lot Yeh_seq FNA, n = 42 codes) et au livre
blanc (journal, entrée §8.74). Ce protocole est gelé AVANT toute
construction et tout run. Le fichier source officiel
(`data/GSE131050_PurIST_Yeh_seq.tsv.gz`) est CELUI du §8.74,
téléchargé officiellement le 20 nov. 2026, SHA vérifié identique
avant ce gel — aucun nouveau téléchargement n'est requis ni
effectué ; le SHA est re-vérifié au §5. Aucun paramètre ne change
après les résultats. Le livre blanc N'EST PAS édité, le PDF
N'EST PAS régénéré, rien n'est poussé sur GitHub dans ce
chantier (convention des chantiers ; fusion par le coordinateur).
La section §8.76 est écrite dans un FICHIER SÉPARÉ
(`section_8.76_gse131050_fna.md`).
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
- §8.74 : douzième paire principale, GSE131050 lot Yeh_seq FF
  (n = 42), **CONFIRME** (`d_maxsep = +0,0739`, réel 0,3220
  contre nul 0,2481), A2 étendu **8/12, 10/12 positifs**, LOO
  7/11, passage consolidé par les nuls frais (graines 8741/8742).
  **C3 RESTE LEVÉE.**
- **Le présent chantier est donc une consolidation
  SUPPLÉMENTAIRE, pas une condition : il ne rouvre pas C3, quel
  que soit son verdict.** Si le lot FNA passe, il consolide
  l'adoption par une autre voie ; s'il échoue, l'adoption pleine
  reste la décision de Zackary du 20 nov. 13h04 — à dire
  plainement dans les deux cas, dans la section comme dans le
  rapport. Ce chantier ne rouvre pas les §8.56/§8.59/§8.64/
  §8.69/§8.70/§8.71/§8.74 et ne change aucune décision de
  Zackary.
- §8.70/§8.72 : correction de méthode notée au §8.70 (§8.70.5,
  §8.70.7) et APPLIQUÉE ici (§9) : le test de Cohen marginal
  est vacueux par construction quand le nul est une permutation
  de lignes (d = 0,0000 pour les 12 gènes) — le test informatif
  est le Spearman de chaque flux contre le pas (Δρ médian,
  nombre de positifs). Le Cohen marginal est quand même rapporté
  (il valide la construction du nul), mais il ne porte aucune
  information d'ordre et ne décide rien.

## 1. Les 12 paires principales indépendantes déjà comptées (V1 + §8.69 + §8.70 + §8.71 + §8.74)

Valeurs reprises des §8.56/§8.69/§8.70/§8.71/§8.74, jamais
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

Bilan : **8/12 au-dessus du plancher, 10/12 positifs.** LOO
7/11. Rotations V2 (48 paires, §8.44, sans doublon) : 37/48
pour `maxsep`. Elles ne sont PAS rejouées ici.

## 2. Paire choisie : GSE131050, lot Yeh_seq FNA — et pourquoi ce N'EST PAS une paire indépendante

### 2.1 Choix

**Cohorte : GSE131050, NCBI GEO** — Rashid et coll., *Clin
Cancer Res* 2020, 26(1):82–92 (PMID 31754050, doi
10.1158/1078-0432.CCR-19-1467), UNC Lineberger, Chapel Hill.
Série soumise le 10 mai 2019, publique le 10 déc. 2019, 191
échantillons, 2 plateformes : GPL16791 (Illumina HiSeq 2500) et
GPL18573 (Illumina NextSeq 500). BioProject PRJNA542388, SRA
SRP197641. Sous-série [RNA-Seq] de la SuperSeries GSE131049
(l'autre sous-série, GSE131051, est NanoString, non utilisée).
URL (convention FTP des autres provenances) :
`https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/suppl/GSE131050_PurIST_Yeh_seq.tsv.gz`
`https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/matrix/GSE131050-GPL18573_series_matrix.txt.gz`

**Lot : Yeh_seq, GPL18573 (Illumina NextSeq 500) : tumeurs
primaires PDAC, échantillons FNA ex-vivo, UN échantillon par
tumeur indépendante, n = 42 codes** (construction §4 : 45
colonnes FNA primaires → 42 codes-tumeurs distincts, les 2
codes à réplicats FNA agrégés par médiane).

### 2.2 Indépendance — le verdict est NON, et c'est écrit avant tout run

L'enquête pré-gel (`enquete_876/check_fna_876.py`, vérification
de portes uniquement, aucun maxsep, aucun run) établit, sur le
fichier officiel déjà téléchargé au §8.74 (SHA vérifié
identique, §5) :

1. **Le lot FNA n'a JAMAIS été utilisé dans ce projet.** Grep
   avant le gel (20 nov. 2026) : la chaîne « FNA » ne figure
   que comme « piste restante non vérifiée » dans les fichiers
   du §8.71 et du §8.74 et dans le livre blanc aux mêmes
   endroits — AUCUN CSV de flux, aucun run, aucun JSON, aucune
   valeur `maxsep` n'existe pour le lot FNA. Les graines
   8761/8762 et le préfixe `_876_` ne figurent dans aucun
   fichier du projet (hors contenu numérique d'un fichier de
   données tiers, sans rapport).
2. **MAIS ce ne sont pas de nouveaux patients.** Le lot Yeh_seq
   est APPARIÉ (§8.74.7) : les 97 échantillons primaires
   proviennent de 43 tumeurs indépendantes seulement (codes
   `MMDDT#`), chaque tumeur étant échantillonnée jusqu'à trois
   fois (FF, FNA, FFPE). Enquête §8.76 : **41 codes sur 42 sont
   communs aux lots FF et FNA** — recouvrement 41/42 (97,6 %).
   Code FNA seul (sans FF) : 0921T1. Code FF seul (sans FNA) :
   PancT6. Total : 43 tumeurs distinctes. **Le lot FNA est
   donc les MÊMES tumeurs que le lot FF du §8.74, vues par un
   autre type d'échantillon** (FNA ex-vivo au moment de la
   résection, 3 passages, aiguille 22G ; kit TruSeq RNA Exome
   contre TruSeq pour les FF ; échantillons faible volume).
3. **Conséquence gelée : le lot FNA N'EST PAS une treizième
   paire principale indépendante et N'ENTRE PAS dans le
   compte A2.** Le compte des paires indépendantes reste 12
   (8/12, 10/12 positifs, LOO 7/11), quel que soit le verdict
   ici. Le lot FNA est un **test de robustesse apparié** :
   le signal `maxsep` mesuré sur les mêmes tumeurs en FF
   survit-il au changement de type d'échantillon (FNA) ?
   C'est une question différente de la confirmation
   indépendante, et elle est nommée comme telle — ni
   minimisée, ni gonflée en « treizième paire ».
4. **Même construction que les autres paires principales GEO.**
   Variante (a) : les 12 mêmes gènes que la v4 TCGA (PGC, REG4,
   CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5,
   CLCA1, MUC16), ordre = KRAS croissant, sans correction, cas
   complets, nul = lignes permutées graine 42 (§4). La paire
   est donc comparable par construction — mais appariée au
   §8.74, pas indépendante. Une seule adaptation, gelée ici
   et justifiée au §4.4 : l'unité d'analyse est la TUMEUR
   INDÉPENDANTE, pas la colonne — les réplicats FNA d'une même
   tumeur sont agrégés par médiane (précédent du projet :
   agrégation par médiane des sondes multiples vers un même
   symbole, et des réplicats FF au §8.74).
5. **Pas un re-test déguisé du §8.74.** Ce ne sont ni une
   relecture d'un JSON existant, ni une rotation déjà comptée,
   ni un sous-ensemble d'une paire V1, ni un nouvel ordre sur
   des CSV existants (nouveaux CSV, nouveaux runs, 2 runs v6.2
   frais, données FNA jamais courues). La sous-série NanoString
   GSE131051 n'est pas utilisée ; le lot Linehan_seq reste
   écarté (§8.74, protocole §2.3 : 37 patients, pré/post
   mélangées).

**Différence d'échelle KRAS, consignée d'avance.** Enquête
§8.76 : KRAS FNA (médiane par code) min 0,0482, médiane 1,569,
max 5,803 — contre KRAS FF min 1,152, médiane 6,955, max 19,7
(§8.74). L'ordre reste KRAS croissant (même règle que toutes
les paires), mais l'échelle FNA est ~4 fois plus basse :
échantillons faible volume, kit TruSeq RNA Exome. C'est une
différence de mesure entre types d'échantillons, pas une
correction à appliquer — aucune renormalisation, aucune
transformation log ajoutée. Si le verdict diffère de celui du
§8.74, cette différence d'échelle est une piste d'explication
nommée, pas une excuse.

## 3. Arrêt borné — AUCUN repli technique

**Une seule cohorte dans ce chantier : le lot Yeh_seq FNA de
GSE131050 (n = 42 tumeurs indépendantes).** Si elle est
INUTILISABLE selon les critères d'acceptation du §5
(fichier source illisible ou SHA différent, plateforme sans
table exploitable, n < 40 tumeurs indépendantes, KRAS absent,
< 12 gènes v4 mappés, < 40 cas complets), le chantier s'arrête
sur un blocage documenté : section §8.76 écrite quand même,
avec les tentatives chiffrées, aucune valeur inventée, et la
piste suivante nommée comme piste seulement (aucune autre
cohorte forcée, aucun run lancé pour elle).
Il n'y a PAS de cohorte #2 dans ce chantier. Le lot Linehan_seq
n'est PAS un repli (§8.74, protocole §2.3 : écarté d'avance,
pour une raison structurelle). Le lot FFPE (5 échantillons,
5 codes) n'est PAS un repli non plus : n = 5 < 40.

## 4. Construction des flux — variante (a), comme les paires GEO V1

Nouveau script `build_fluxes_876.py` (copie adaptée de
`build_fluxes_874.py`, original intact). Préfixe `_876_` pour
tous les fichiers du chantier.

### 4.1 Identification gènes (GSE131050 Yeh_seq / GPL18573, Illumina NextSeq 500)

- Pas de mapping sonde→symbole : le fichier supplémentaire est
  déjà une table gène × échantillon, première colonne
  `geneID` de la forme `ENSG…;SYMBOLE` (ex.
  `ENSG00000133703;KRAS`). Le symbole est lu après le `;`.
- Couverture vérifiée dans l'enquête (à re-vérifier sur le
  fichier officiel, porte §5) : les 13 gènes utiles (12 v4 +
  KRAS) sont présents, UNE ligne chacun, sans doublon de
  symbole, dans le fichier Yeh (26 267 gènes). Aucun gène
  mappé à la main. 0 NaN sur les 13 lignes × 125 colonnes.
- La plateforme réelle est confirmée par l'en-tête de la
  matrice (`!Series_platform_id` : GPL18573 pour Yeh) et
  consignée dans `PROVENANCE_876.md` ; si l'en-tête dit autre
  chose que GPL18573 pour le lot Yeh, c'est consigné tel quel
  et la construction s'arrête (arrêt borné §3).
- Valeurs : telles que fournies par les déposants (nature
  exacte — allure TPM/FPKM non log-transformés ; l'article
  indique « FPKM ou TPM selon l'étude » sans préciser pour ce
  fichier : nature exacte consignée comme indéterminée entre
  FPKM et TPM dans `PROVENANCE_876.md` ; aucune
  renormalisation, aucune transformation log ajoutée).

### 4.2 Série réelle (variante (a))

- Gènes v4 (les 12 mêmes que TCGA v4, ordre de la liste) :
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1,
  CEACAM5, CLCA1, MUC16.
- Contrôle : KRAS (expression, croissant). Le contrôle n'est
  JAMAIS un flux : pas de doublon. Justification de l'ordre
  KRAS : identique aux paires principales V1 — KRAS est le
  contrôle monotone du projet, et l'ordre par son expression
  est celui de toutes les paires GEO à 12 gènes.
- Tumeurs seules : lot Yeh_seq, `sample type: FNA` ET kind `Pi`
  (primaire) dans les titres `S###.FNA.Pi.<code>` (45 colonnes
  attendues) ; les 28 PDX, les 47 FF primaires et les 5 FFPE
  primaires sont exclus et comptés (§2.2).
- **Unité = tumeur indépendante (§4.4).** Les 45 colonnes FNA
  primaires sont regroupées par code-tumeur (`MMDDT#`, 42
  codes) ; pour les 2 codes à réplicats FNA (0417T1 ×3,
  1119T1 ×2), la valeur retenue par gène est la MÉDIANE
  des réplicats FNA (précédent du projet). Le code 0921T1
  (FNA seul) ENTRE dans le lot FNA — c'est le seul code que le
  lot FF n'a pas.
- Cas complets seulement (KRAS + 12 gènes présents), jamais
  d'imputation. Enquête : 0 NaN — 42/42 cas complets attendus.
- Sorties : `pdac_876_yeh_fna_fluxes.csv` (+ `_nul.csv`).
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
**8761** et **8762** (graines jamais utilisées dans ce projet,
gelées ici avant tout run), et courus en runs frais
(`pdac_876_yeh_fna_fluxes_nul_s8761.csv`,
`pdac_876_yeh_fna_fluxes_nul_s8762.csv`,
`results_fast_v62_876_yeh_fna_nul_s8761`,
`results_fast_v62_876_yeh_fna_nul_s8762`). Le verdict reste
celui de la paire graine 42 (§7) ; les nuls frais sont un
contrôle de robustesse descriptif (min / médiane / max des
écarts), jamais un moyen de choisir le nul qui arrange.

## 5. Critères d'acceptation de la cohorte (vérifiés sur le fichier officiel, avant construction)

- Fichier source `data/GSE131050_PurIST_Yeh_seq.tsv.gz` : SHA-256
  `2fc0a66ef0ac62aab17e9bda1c78561786f887a9122591a9346a868f852be5b1`
  (téléchargement officiel §8.74, 9 468 179 o) — tout écart est
  consigné et les portes sont re-vérifiées. Matrice GPL18573 :
  SHA `9b333eb6b9181fedfc793b9a61f5970af459a5b37b8aa8f7808a3b6c34c7843e`
  (6 864 o). Aucun nouveau téléchargement : le fichier est
  celui du §8.74, déjà officiel et vérifié.
- Plateforme lue dans l'en-tête de la matrice du lot Yeh :
  GPL18573 ; sinon ARRÊT (§3).
- n ≥ 40 tumeurs PDAC indépendantes (codes-tumeurs distincts,
  lot Yeh FNA) ; sinon ARRÊT (§3).
- Aucun échantillon porteur d'un code-barres TCGA ou déjà
  présent dans une cohorte du projet (GSM/titres inspectés) ;
  sinon ARRÊT (§3). (Caveat §2.2 : titres anonymisés ; et le
  recouvrement avec le lot FF du §8.74 est CONNU et voulu —
  c'est le test apparié, pas un recouvrement caché.)
- KRAS présent comme ligne mappée ; sinon ARRÊT (§3).
- Les 12 gènes v4 présents (une ligne chacun, symbole exact
  après `;`) ; sinon ARRÊT (§3) (aucun gène remplacé, aucun
  absent toléré pour une paire comparable — la comparabilité
  au §8.74 l'exige).
- Cas complets (KRAS + 12 gènes) ≥ 40 ; sinon ARRÊT (§3).

## 6. Runs v6.2 (mode fast)

- Lot : 2 runs — réel + nul — manifeste `manifest_v62_876.txt`,
  lanceur reprenable existant `run_v62_lot.sh` (saute les sorties
  déjà complètes), journal `runs_v62_876.log` (SHA du pipeline
  en tête, exits consignés).
- Dossiers : `results_fast_v62_876_yeh_fna` et
  `results_fast_v62_876_yeh_fna_nul` (nuls frais éventuels :
  `results_fast_v62_876_yeh_fna_nul_s8761` /
  `..._s8762`).
- Lancement en `systemd-run --unit=v62-876 --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance qui
  s'arrête d'elle-même à 2/2 (ou 4/4 si nuls frais). Ne JAMAIS
  supprimer le dossier d'un run en cours. Si la machine
  redémarre, reprise sans perte (SKIP des dossiers complets,
  jamais de relance à l'aveugle).
- SHA du pipeline revérifié avant ET après le lot.

## 7. Critère de passage — GELÉ avant tout run

**Le lot FNA PASSE si et seulement si :**
`d_maxsep = maxsep_R − maxsep_N > 0,07` (plancher, en unités |d|,
gigue_eff = max(gigue mesurée, 0,07) — v6.2 déterministe, gigue
attendue 0, comme §8.56 §3) **ET** `d_maxsep > 0` (positif —
impliqué par > 0,07, mais consigné séparément comme au §8.56).

`maxsep` = `best_config.metrics.max_separation`, |d de Cohen|
maximal du scan, lu sur le best_config ANCIEN (sélection par
l'ancien composite) — mêmes définitions que §8.56.2. Le seuil MC,
la cascade, S_sep, Delta, L7a sont inchangés par construction.

**Catégories de verdict (gelées) :**
- **CONFIRME** : `d_maxsep > 0,07` — le signal survit au
  changement de type d'échantillon (FF → FNA) sur les mêmes
  tumeurs.
- **PARTIEL** : `0 < d_maxsep ≤ 0,07` — positif mais sous le
  plancher (même catégorie que GSE71729, +0,0402, et GSE79668,
  +0,0567).
- **NON** : `d_maxsep ≤ 0` — négatif ou nul (même catégorie que
  GSE62452 et GSE21501).

**Ce que le verdict change, et ce qu'il ne change pas (gelé) :**
- Le compte A2 des paires indépendantes NE CHANGE PAS : il reste
  **8/12 au-dessus du plancher, 10/12 positifs, LOO 7/11**,
  quel que soit le verdict. Le lot FNA n'y entre pas — il est
  apparié au §8.74, pas indépendant.
- **C3 reste LEVÉE** dans tous les cas — elle l'était déjà
  depuis le §8.71 ; ce chantier est une consolidation
  supplémentaire, pas une condition.
- Le verdict est rapporté comme **robustesse appariée**
  (mêmes tumeurs, autre échantillon), avec comparaison
  descriptive au §8.74 (mêmes 41 codes) : si le FNA passe, le
  signal `maxsep` n'est pas un artefact du type FF ; s'il
  échoue, le signal FF ne se transfère pas au FNA — les deux
  lectures sont écrites, aucune n'est un échec du §8.74.
- Le leave-one-out sur les 12 paires indépendantes n'est PAS
  recalculé ici (il ne change pas : le lot FNA n'y entre pas).

**Nuls frais (§4.4, règle gelée).** La paire graine 42 fait le
verdict, dans tous les cas. Si `d_maxsep` est PROCHE du
plancher — défini ici comme `d_maxsep` dans [−0,07 ; +0,14[,
soit à moins d'une largeur de plancher du seuil, de part et
d'autre — les 2 nuls frais (graines 8761, 8762) sont courus et
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
- Falsification : INDISPONIBLE sous n = 75 — GSE131050 Yeh FNA
  n = 42 : noter « indisponible », ne pas imputer.
- Plancher équivalent-sep (descriptif) : le lot passe-t-il aussi
  `0,07·(1+m_R)(1+m_N)` ? Rapporté, non décisif (D4 n'est pas
  rejoué ici : il porte sur les paires V1, déjà tranché).
- Comparaison descriptive au §8.74 (mêmes 41 codes) : `maxsep`
  réel/nul, MC, Delta, Δρ médian — reprise des valeurs du
  §8.74 telles quelles, jamais recalculées.
- Aucun autre critère, aucune repondération, aucune redéfinition
  du plancher après avoir vu les chiffres.

## 8. Extraction et vérification

1. Extracteur propre du chantier, `extract_876.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_866.py` / `extract_869.py` / `extract_871.py` /
   `extract_874.py`) ; lit `maxsep`, `mc_score`, `stability`,
   `ssep`, `delta`, `l7a`, cascade, falsification dans les 2
   (ou 4) `master_results.json` ; sorties `extract_876.json` /
   `extract_876.csv`.
2. Second calcul indépendant : relecture directe des
   `master_results.json` par un chemin distinct (script
   `verify_876.py`, SHA noté) — `maxsep` et ancien MC recoupés
   à 0,0 exact ; tout écart = résultat à diagnostiquer, pas un
   bruit.
3. Recoupements : les 12 valeurs déjà comptées reprises telles
   quelles du §8.56 (table `sep_maxsep_856_table.json`, SHA
   `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`),
   du §8.69 (`extract_869.json`, SHA
   `644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b`),
   du §8.70 (`extract_870.json`, SHA
   `4ffa851a83668b2369097703862e0413ff9af54af3a66ef70aea9333b40c444f`),
   du §8.71 (`extract_871.json`, SHA
   `85e9089a…55e3b`) et du §8.74 (`extract_874.json`, SHA
   `82ade74701245021dfdb965bdc689ac98262c70f12ecec7f39e1b5b742dfcb47`),
   jamais recalculées ici — ce chantier ne re-vérifie pas les
   §8.56/§8.59/§8.64/§8.69/§8.70/§8.71/§8.74 (déjà clos).
4. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 9. Tests directs en appui (ne décident pas)

Script `direct_tests_876.py` (SHA noté), sur les CSV de flux
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
3. Comparaison descriptive avec le §8.74 (mêmes 41 codes) :
   Δρ médian +0,386, 10/12 positifs, |ρ| moyen réel 0,336
   contre nul 0,146 au §8.74. Si le signal d'ordre FNA est
   plus faible, c'est consigné tel quel, sans être élucidé
   sans preuve ; si une divergence Delta/`maxsep` apparaît
   ici, elle est nommée telle quelle.
4. Aucun de ces tests ne change le verdict du §7.

## 10. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et le
  jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict : les tests directs des §8.66/§8.70/§8.71/§8.74, les
  sous-types PurIST publiés, les scores publiés ne prédisent
  rien ici — seul l'écart `maxsep` mesuré sur les runs du
  présent chantier fait le verdict.
- Un nul qui invalide une piste est un résultat ; un échec du lot
  est un verdict, pas un échec caché.
- Ne jamais présenter une lecture préliminaire comme un verdict.
- Aucun consensus exigé entre flux ou contrôles ; aucune
  affirmation clinique — l'étude porte sur l'instrument.
- **Ne jamais compter le lot FNA comme une paire indépendante
  : 41/42 codes sont les mêmes tumeurs que le §8.74.** Le
  compte A2 reste 12 paires. Toute lecture future qui
  compterait 13 paires avec le FNA serait un double comptage.

## 11. Livrables

- Ce protocole (gelé avant construction et runs).
- `PROVENANCE_876.md` (source, auteur, date, dépôt, URL, SHA-256
  du fichier source réutilisé du §8.74, plateforme réelle,
  effectifs, exclus, identification des gènes — avec la
  vérification d'appariement du §2.2, le compte rendu de
  l'enquête préalable et la structure appariée).
- `build_fluxes_876.py` + CSV de flux (`pdac_876_*`, SHA consignés).
- `manifest_v62_876.txt`, `runs_v62_876.log`, dossiers
  `results_fast_v62_876_*`, `extract_876.json` / `.csv`,
  `verify_876.py` + sortie de vérification,
  `direct_tests_876.py` + sortie.
- §8.76 dans le FICHIER SÉPARÉ
  `section_8.76_gse131050_fna.md` (verdict d'abord, une phrase :
  CONFIRME / PARTIEL / NON ; chiffres ensuite ; détail complet
  après ; provenance nommée partout ; C3 reste levée dans tous
  les cas ; A2 inchangé, dit explicitement).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin du protocole gelé §8.76. —
