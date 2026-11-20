# §8.55 Pureté externe ABSOLUTE : la corrélation immunitaire est en partie un effet de pureté

Date : 20 novembre 2026 (03h16–05h02 UTC ; 22h16–00h02 heure de Montréal,
19–20 nov.). Go : coordinateur, 19 nov. 2026 ~22h15.
Protocole gelé avant tout téléchargement, avant tout calcul et avant tout run :
`PROTOCOL_purity_external_855.md` (SHA-256 `734a9b171cf0ce155d456288d8f617528aa237820269d1c3e429505bce134db7`).

## Verdict d'abord

**La pureté externe explique une partie substantielle de la corrélation
intra-famille immunitaire — mais pas toute. Verdict gelé : H1-ext PARTIELLE.**
La pureté ABSOLUTE (ADN, indépendante de l'ARN) corrèle fortement avec les
12 flux immunitaires — tous négativement, moyenne |r| = **0,4932**
(CD8A r = −0,676, R² = 45,7 %) — contre 0,146 / 0,198 pour les proxys
internes acineux / îlots du §8.51. Après régression sur ABSOLUTE, la
corrélation intra-famille chute d'un quart : **0,5040 → 0,3757 (−25,5 %)**,
fraction de paires fortes 37/66 → 18/66. Ordonner les flux par ABSOLUTE les
sépare fortement (**écart S_sep +0,6911**, prédit +0,6659, seuil trouvé tôt
à 25,77 %). Et le test décisif : ordonner les flux RÉSIDUALISÉS par CD8A
résidualisé sépare encore **+0,6499** — réduit à 66,1 % du brut (+0,9838),
mais loin sous le seuil H1 (< 0,30) et au-dessus du seuil H0 (≥ 0,45).
**La pureté porte environ un tiers de la corrélation et de la séparation ;
les deux tiers restants sont propres aux tumeurs.**

**Conséquence directe pour le §8.51 : son verdict « H0 soutenue » est
qualifié, pas renversé dans ses chiffres.** Les chiffres du §8.51 restent
vrais (0,5563 → 0,5480 après régression sur les proxys ; P-RES +0,9174).
Ce qui change, c'est l'interprétation : les proxys acineux/îlots étaient
de FAIBLES mesures de la pureté (moyenne |r| avec les flux 0,146/0,198,
contre 0,493 pour ABSOLUTE ; signes majoritairement positifs, contre
négatifs pour ABSOLUTE — le sens attendu d'une dilution). Le §8.51 a testé
les proxys, pas la pureté elle-même. Avec la vraie pureté, la réponse
n'est plus « pas un artefact » mais « en partie un effet de pureté, en
partie une propriété propre ». La domination IMMROT du §8.48 n'est pas
remise en cause : elle reste expliquée par le couplage ; ce chantier en
précise la cause amont — le couplage est porté pour environ un tiers par
la pureté tumorale.

## 8.55.1 Question, méthode, inventaire des sources (avant le gel)

**Question (§8.51.10).** Le §8.51 a innocenté la pureté avec des proxys
internes ARN. Une pureté EXTERNE, indépendante, donne-t-elle un autre
chiffre ? Deux mesures visées : ABSOLUTE (nombre de copies ADN — la plus
indépendante de l'ARN) et ESTIMATE-purity (ARN, signature indépendante).

**Sources candidates gelées :** (1) Aran et al., Nat Commun 2015, 6:8971,
tableau supplémentaire (ABSOLUTE, ESTIMATE, LUMP, IHC, CPE) via Nature /
UCSC Xena ; (2) ESTIMATE, Yoshihara et al., Nat Commun 2013 (site
MD Anderson, scores par maladie) ; (3) GDC / autres portails TCGA.

**Critères gelés.** T1' : lien substantiel si moyenne |r| ≥ 0,30 pour au
moins une pureté ; faible si < 0,15 pour les deux. T2' : EFFONDREMENT si
moyenne |r| résiduelle < 0,30 (chute ≥ 45 %) ET fraction |r| > 0,5 < 0,20 ;
PERSISTANCE si chute < 20 % (moyenne résiduelle > 0,80 × brute appariée) ;
entre les deux : partielle. T5' : E-ABS ou E-EST soutient H1-ext si écart
S_sep ≥ 0,45 ; E-RES soutient H1-ext si écart < 0,30, soutient H0-ext si
écart ≥ 0,45. Verdict : H1 totale si T2' = effondrement ET E-RES < 0,30
ET (E-ABS ≥ 0,45 OU E-EST ≥ 0,45) ; H1 PARTIELLE si T2' = partielle OU
(E-ABS/E-EST entre 0,30 et 0,45) avec E-RES < 0,70 ; H0 si T2' =
persistance ET E-ABS < 0,30 ET E-EST < 0,30 ET E-RES ≥ 0,45 ; toute autre
combinaison : zone grise. Références : IMMROT sans doublon, moyenne
+0,7521, minimum +0,4508 (CD68), CD8A écart +0,9838 (réel 1,2310, nul
0,2472) ; régression §8.48 d_ssep = −0,175 + 1,705·C. Le score immunitaire
ESTIMATE n'est PAS utilisé comme contrôle des flux immunitaires
(circulaire : il dérive d'une signature immunitaire ARN).

## 8.55.2 Porte S (source) : OUVERTE pour ABSOLUTE, fermée pour ESTIMATE publiée

### Aran et al. 2015 : obtenu, mais 0 PAAD
Supplementary Data 1 (« Tumor purity estimates for TCGA samples ») obtenu
via Europe PMC (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4671203/supplementaryFiles`,
zip SHA-256 `4685a8b2…541a5`, 8 048 764 octets ; xlsx extrait
`ncomms9971-s2.xlsx`, SHA-256 `fce1ba13…7529`, 553 082 octets, feuille
« Supp Data 1 », 9 364 lignes, colonnes Sample ID, Cancer type, ESTIMATE,
ABSOLUTE, LUMP, IHC, CPE). **Types couverts : 21, PAAD absent — 0 ligne
PAAD, 0 appariement sur 178.** Le téléchargement direct depuis PMC est
bloqué par un défi de preuve de travail (« Preparing to download… »,
page HTML au lieu du xlsx — tenté, documenté, non contourné). ABSOLUTE
n'existe dans ce tableau que pour 11 types (BLCA 101, BRCA 838, COAD 400,
GBM 548, HNSC 299, KIRC 416, LUAD 354, LUSC 332, OV 555, READ 159,
UCEC 396) — PAAD n'en fait pas partie, comme l'article l'annonçait
(« estimations available for only 11 cancer types »).

### UCSC Xena : même tableau, 0 PAAD (confirmation indépendante)
Le jeu `tcga_purity` du package UCSCXenaShiny 2.2.1 (tarball CRAN SHA
`377c0f3f…a597`, `data/tcga_purity.rda`) est exactement le tableau d'Aran :
9 364 lignes, mêmes colonnes, mêmes premières lignes (TCGA-OR-A5J1-01,
ACC, ESTIMATE 0,9368…) — 21 types, **PAAD absent**. La source Xena ne
donne rien de plus que la source 1a.

### ESTIMATE publiée pour PAAD : NON obtenue (tentative documentée)
Le site MD Anderson (`bioinformatics.mdanderson.org/estimate/`) liste
bien « Pancreatic ductal adenocarcinoma — RNA-seqV2 179 » avec un
téléchargement des scores par maladie (stromal, immunitaire, ESTIMATE).
Mais le téléchargement est piloté par JavaScript (`disease.html` +
`js/disease_histogram.js`, fonction `startDownload`) et le fichier JS
n'a pas pu être récupéré : curl en échec répété (000, 3 tentatives) puis
timeout du fetch de page sur ce même fichier — cette requête n'a pas été
répétée ensuite. **Aucun score ESTIMATE publié pour PAAD n'a donc été
obtenu.** Le repli par recalcul (package R `estimate` depuis notre
tarball) n'a PAS été fait : ce ne serait pas un score publié, et ABSOLUTE
(ADN, indépendant de l'ARN) est le contrôle externe le plus fort — il est
disponible. L'ESTIMATE-purity publiée reste un contrôle manquant, nommé
au §8.55.10.

### ABSOLUTE pour PAAD : obtenu via pdacR / Raphael et al. 2017
**Source primaire :** Raphael et al., « Integrated Genomic Characterization
of Pancreatic Ductal Adenocarcinoma », Cancer Cell 2017, 32(2):185–203.e13
(PMID 28810144, PMCID PMC5964983, DOI 10.1016/j.ccell.2017.07.007),
Table S1 — la table d'échantillons TCGA-PAAD avec la pureté ABSOLUTE.
Le téléchargement direct de la Table S1 depuis PMC
(NIHMS898701-supplement-10.xlsx, 40,2 Ko) est bloqué par le même défi de
preuve de travail que pour Aran (tenté, page HTML reçue, non contourné) ;
Europe PMC refuse le supplément (« Article with id PMC5964983 is not
open access one »).
**Copie curée utilisée :** pdacR (Torre-Healy et al., Commun Biol 2023,
6:163, doi 10.1038/s42003-023-04461-6), GitHub `rmoffitt/pdacR`,
fichier `data/TCGA_PAAD.rds`, URL
`https://raw.githubusercontent.com/rmoffitt/pdacR/master/data/TCGA_PAAD.rds`,
SHA-256 `52020679350d1539d7516f7d38f7bf09e510225eba2f228a4fe874f3c496ea76`
(12 311 529 octets, jamais modifié ; copie dans `data/pdacR_TCGA_PAAD.rds`).
Le script de construction du package (`R/parse_TCGA_PAAD.R`, copie dans
`pdacr_parse_TCGA_PAAD.R`, SHA `a65f716a…dd30`) lit explicitement la
Table S1 de Raphael (`Supplemental_Table_1_PAAD_sample_table_for_TCGA.xlsx`,
feuilles 1–4) pour construire le `sampInfo` — la colonne `ABSOLUTE.Purity`
vient de cette Table S1. Le `sampInfo` transcrit (181 lignes × 55 colonnes)
est `purity_855_sampinfo.csv` (SHA `7a09dde3…b014`) ; la transcription est
mécanique (lecture seule par le package `rdata`, aucune valeur calculée).

**Cohérence de la colonne ABSOLUTE — trois vérifications indépendantes :**
(a) ABSOLUTE corrèle à **r = +0,8556 (n = 149, p = 7,0×10⁻⁴⁴)** avec la
pureté par méthylation (`DNA.hypermethylation.mode.purity`, même table,
mesure ADN indépendante) — deux mesures ADN s'accordent ; (b) la
classification haut/bas publiée est EXACTEMENT le seuil ABSOLUTE 0,33 :
classe high n = 76, ABSOLUTE [0,33 ; 0,89], moyenne 0,503 ; classe low
n = 73, ABSOLUTE [0,09 ; 0,32], moyenne 0,194 — aucun chevauchement, la
colonne ABSOLUTE est bien celle qui a servi à la classification publiée ;
(c) la distribution reproduit le sous-ensemble indépendant ShrinkageTrees
`pdac` (CRAN 2.1.1, `data/pdac.rda`, n = 130, sans barcode — comparaison
de distribution seulement) : moyenne 0,3557 contre 0,3517, min 0,09,
max 0,89 identiques. Ces trois vérifications ne remplacent pas une
relecture directe de la Table S1 (restée inaccessible derrière le défi
PMC — à refaire par le coordinateur en navigateur si voulu) ; elles
rendent une erreur de transcription invraisemblable.

## 8.55.3 Porte S / jointure : OUVERTE

Jointure sur les **15 premiers caractères** du barcode (protocole §4) :
178/178 tumeurs du projet appariées (0 collision de clé des deux côtés) ;
**ABSOLUTE non nul pour 149/178 (83,7 %)** — au-dessus du seuil gelé
(≥ 100). Toutes les valeurs dans [0, 1]. Les 3 échantillons externes hors
projet sont TCGA-HZ-A9TJ-06A (06A, métastase), TCGA-H6-8124-11A et
TCGA-YB-A89D-11A (11A, tissu normal adjacent) — correctement exclus par
notre critère « tumeurs primaires code 01 ». Les 29 tumeurs sans ABSOLUTE
sont les non-whitelistées de Raphael (181 − 150 = 31 dans pdacR) : le
sous-ensemble apparié est le sous-ensemble whitelisting — effet de
sélection nommé au §8.55.8 (la cohésion brute passe de 0,5563 à n = 178
à 0,5040 à n = 149 par la seule exclusion de ces 29 tumeurs).

ABSOLUTE (n = 149) : min 0,09, médiane 0,33, moyenne 0,3517, écart-type
0,1845, max 0,89. Fichier apparié : `purity_855_external.csv`
(SHA `03f34fe0…bd6f`, 149 lignes : sample, purity_absolute, + colonnes de
provenance : pureté méthylation, leucocytes méthylation, classe, cellularité
pathologiste).

## 8.55.4 T1' — Chaque flux immunitaire suit ABSOLUTE : fortement, tous négativement

Pearson r (+ Spearman ρ) de chaque flux contre ABSOLUTE ; R² par flux
(OLS sur [1, ABSOLUTE]) ; p brutes bilatérales, sans correction pour tests
multiples (12 tests — le jugement porte sur la moyenne, pas sur une p
isolée).

| Gène | r ABSOLUTE (p) | ρ ABSOLUTE | R² ABSOLUTE |
|---|---|---|---|
| CD8A | **−0,676 (3,2×10⁻²¹)** | −0,689 | **0,457** |
| CD8B | −0,563 (7,6×10⁻¹⁴) | −0,583 | 0,317 |
| CD4 | −0,633 (4,6×10⁻¹⁸) | −0,624 | 0,401 |
| FOXP3 | −0,533 (2,7×10⁻¹²) | −0,555 | 0,284 |
| CD68 | −0,212 (9,6×10⁻³) | −0,156 | 0,045 |
| CD163 | −0,584 (5,3×10⁻¹⁵) | −0,544 | 0,341 |
| CD274 | −0,308 (1,3×10⁻⁴) | −0,349 | 0,095 |
| PDCD1 | −0,564 (6,7×10⁻¹⁴) | −0,576 | 0,318 |
| CTLA4 | −0,593 (1,6×10⁻¹⁵) | −0,587 | 0,352 |
| GZMB | −0,451 (7,9×10⁻⁹) | −0,475 | 0,203 |
| IFNG | −0,306 (1,5×10⁻⁴) | −0,320 | 0,094 |
| CD19 | −0,495 (1,4×10⁻¹⁰) | −0,525 | 0,245 |

Moyenne |r| : **0,4932** (Spearman 0,4985). **R² médian 0,3006 (30,1 %),
maximum 0,4569 (CD8A).** Significatifs à p < 0,05 : 12/12 ; à p < 0,001 :
11/12 (seul CD68 est à p = 9,6×10⁻³). Critère gelé : lien SUBSTANTIEL
(≥ 0,30 — dépassé de 64 %). Trois remarques : (a) les 12 corrélations
sont NÉGATIVES — le sens attendu d'une dilution : plus la tumeur est
pure, moins le signal immunitaire est fort ; c'est le sens inverse des
proxys internes du §8.51 (22/24 positives, petites), qui ne mesuraient
donc pas la pureté ; (b) ABSOLUTE explique 30 % de la variance du gène
immunitaire médian et 46 % de CD8A — contre 5,7 % et 13,2 % pour les
proxys internes (facteur ~5) ; (c) CD68 est l'exception (r = −0,212,
R² = 4,5 %) — les macrophages suivent moins la pureté que les lymphocytes.

## 8.55.5 T2' — La corrélation intra-famille chute d'un quart, ne s'effondre pas

Matrice 66 paires, sur les n = 149 appariées (la brute de référence est
recalculée sur ce sous-ensemble, jamais importée du §8.51).

| Matrice | Pearson moyenne \|r\| | médiane \|r\| | fraction \|r\| > 0,5 | Spearman moyenne \|r\| |
|---|---|---|---|---|
| Brute (n = 149) | **0,5040** | 0,5429 | 0,561 (37/66) | 0,4880 |
| Résidus [1, ABSOLUTE] | **0,3757** | 0,3746 | 0,273 (18/66) | 0,3617 |
| Brute (n = 178, réf.) | 0,5563 | — | — | 0,5403 |

**Chute : 25,5 %** (0,5040 → 0,3757) ; la fraction de paires fortes est
divisée par deux (37/66 → 18/66). Critère gelé : ni EFFONDREMENT
(résiduelle 0,3757 > 0,30 ; chute 25,5 % < 45 %) ni PERSISTANCE (chute
25,5 % > 20 % ; résiduelle 0,3757 < 0,80 × 0,5040 = 0,4032) : **T2' =
PARTIELLE**. Retirer linéairement toute la pureté ABSOLUTE retire un
quart de la corrélation — et en laisse trois quarts.

## 8.55.6 T3' — Couplage prédit : la régression §8.48 tient, avant comme après

Couplage C par contrôle immunitaire (moyenne des |r| avec les 11 autres
flux), brut contre résidualisé ; d_ssep prédit par d = −0,175 + 1,705·C.

| | C moyen | d_ssep prédit moyen |
|---|---|---|
| Brut (n = 149) | 0,5040 | **0,6844** |
| Résidualisé [ABSOLUTE] | 0,3757 | **0,4656** |

CD8A seul : C 0,6059 → 0,4522, d_pred 0,8581 → **0,5960**. Le T3' ne fait
que traduire T2' en S_sep prédit ; le verdict se joue au T5'.

## 8.55.7 T4' — Stratification : la cohésion persiste dans chaque moitié

Médiane d'ABSOLUTE = 0,33 (n = 76/73 — exactement les classes high/low
publiées, cf. §8.55.2) ; matrice intra-famille dans chaque moitié.

| Stratification | Moitié haute : moyenne \|r\| (frac. > 0,5) | Moitié basse : moyenne \|r\| (frac. > 0,5) |
|---|---|---|
| ABSOLUTE (méd. 0,33) | 0,3802 (0,273) | 0,4283 (0,394) |

Si la cohésion venait entièrement de la pureté, elle devrait s'effondrer
dans chaque moitié (bande de pureté étroite). Elle persiste dans les deux
moitiés (0,38 et 0,43, contre 0,5040 global) — réduite, pas effondrée.
Argument non paramétrique, indépendant de toute linéarité : il confirme
T2' par une autre voie — la pureté porte une partie, pas le tout.

## 8.55.8 T5' — Runs v6.2 : ABSOLUTE ordonne l'immunitaire, les résidus aussi

Prédictions calculées AVANT de lire les sorties (depuis T1'/T2' du jour) :
E-ABS d_pred +0,6659 (C = 0,4932) ; E-RES d_pred +0,5960 (C_résid CD8A =
0,4522). 4 runs v6.2, mode fast, graine 42, 4/4 exit 0 (lot 03h29:22 UTC –
05h02:00 UTC 20 nov. ; §8.55.10 pour l'incident de redémarrage machine).

| Run | Contrôle → analysés | S_sep réel | S_sep nul | Écart | Prédit | MC réel / nul | Delta réel / nul | w |
|---|---|---|---|---|---|---|---|---|
| E-ABS | ABSOLUTE → 12 imm. bruts | 0,9278 | 0,2367 | **+0,6911** | +0,6659 | 0,4316 / 0,3473 | 2,89 / 3,04 | 26 |
| E-RES | CD8A résid. → 11 imm. résid. | 0,7902 | 0,1403 | **+0,6499** | +0,5960 | 0,4162 / 0,3224 | 2,92 / 2,90 | 26 |

Lecture par critère gelé :
- **E-ABS : la pureté externe ordonne les flux immunitaires.** Écart
  +0,6911 — au-dessus du seuil H1 (0,45), à 92 % de la moyenne IMMROT
  (+0,7521), prédit +0,6659 à 0,025 près. MC sépare aussi (+0,0844 :
  0,4316 contre 0,3473) ; Delta non (2,89 contre 3,04, nul devant de
  0,14) — noté, non utilisé pour le verdict (le verdict porte sur S_sep,
  gelé). Le seuil est trouvé TÔT (T0 = 25,77 %, contre 84,78 % pour P-IS
  au §8.51) : une marche nette en début de course, pas une queue de
  distribution. L7a ne sépare pas dans le sens attendu (down 0,2019
  contre up 0,3785) : L7a n'est pas utilisé ici, comme au §8.48/§8.51.
- **E-RES : la séparation survit réduite.** Écart +0,6499 contre +0,9838
  pour CD8A brut (**66,1 % conservés, baisse de 33,9 %**) et contre
  +0,5960 prédit (écart à la prédiction +0,0539). MC +0,0939 (0,4162
  contre 0,3224) ; Delta quasi égal (2,92 contre 2,90). Critère gelé :
  E-RES < 0,70 → réduit (condition de H1 partielle remplie) ; E-RES
  ≥ 0,45 → encore séparant (la condition H0-ext sur E-RES seule serait
  aussi remplie — c'est pourquoi le verdict suit la règle de synthèse,
  pas un vote : T2' = partielle tranche).

## 8.55.9 Verdict de synthèse

Règle gelée, test par test : T1' = lien substantiel (moyenne |r| 0,4932) ;
T2' = PARTIELLE (chute 25,5 %) ; T4' = persistance réduite dans les deux
moitiés ; E-ABS = +0,6911 (≥ 0,45) ; E-RES = +0,6499 (< 0,70, ≥ 0,45).
**H1-ext totale est rejetée** (T2' n'est pas un effondrement, E-RES n'est
pas < 0,30). **H0-ext est rejetée** (T2' n'est pas une persistance,
E-ABS ≥ 0,45). **H1-ext PARTIELLE est SOUTENUE par la règle gelée**
(T2' = partielle). La corrélation intra-famille immunitaire est portée
pour environ un tiers par la pureté tumorale (ABSOLUTE) et pour environ
deux tiers par une co-expression propre aux tumeurs.

**Ce que cela dit, et ce que cela ne dit pas.** (a) Cela dit que la
pureté est un vrai contributeur, mesuré par une voie ADN indépendante de
l'ARN — pas un artefact des proxys du projet. (b) Cela ne dit pas que
l'infiltration est expliquée : aucune infiltration INDÉPENDANTE n'a été
testée ici (cf. §8.51.1) — ABSOLUTE mesure la fraction tumorale, pas la
composition de l'infiltrat. (c) Cela ne dit pas que les deux tiers
restants sont « biologiques » au sens d'une régulation : ils peuvent
venir d'une variable latente non testée (sous-type moléculaire, état
d'activation, stroma). (d) La mesure porte sur le sous-ensemble
whitelisting (n = 149) ; la brute y est déjà plus faible (0,5040 contre
0,5563 à n = 178) — la sélection elle-même retire 0,0523 de cohésion,
à ne pas confondre avec l'effet ABSOLUTE (0,1283 de chute par
régression, mesuré dans le même n = 149). (e) La domination IMMROT du
§8.48 n'est pas remise en cause : elle reste expliquée par le couplage,
dont un tiers environ vient de la pureté.

**Comparaison directe avec le §8.51 (scores internes) :**

| Test | §8.51 (proxys internes, n = 178) | §8.55 (ABSOLUTE externe, n = 149) |
|---|---|---|
| T1 moyenne \|r\| | acineux 0,146 / îlots 0,198 | ABSOLUTE **0,4932** |
| T1 R² médian | 0,057 | **0,3006** |
| T2 brute → résiduelle | 0,5563 → 0,5480 (−1,5 %) | 0,5040 → 0,3757 (−25,5 %) |
| T5 contrôle → flux | P-AC +0,0118 ; P-IS +0,2876 | E-ABS **+0,6911** |
| T5 résidualisé | P-RES +0,9174 (93,3 % du brut) | E-RES +0,6499 (66,1 % du brut) |
| Verdict | H0 soutenue | **H1 partielle** |

## 8.55.10 Provenance

- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant les calculs, dans les deux logs de lot, et après
  l'extraction). Mode `fast`, graine 42 (défaut), nul = lignes permutées,
  graine 42 (default_rng frais par fichier), contrôle intact.
- **Protocole.** `PROTOCOL_purity_external_855.md`, SHA-256
  `734a9b171cf0ce155d456288d8f617528aa237820269d1c3e429505bce134db7`,
  gelé le 19 nov. 2026 avant tout téléchargement, tout calcul et tout run
  de ce chantier.
- **Entrées externes.** (1) pdacR `data/TCGA_PAAD.rds`, SHA-256
  `52020679350d1539d7516f7d38f7bf09e510225eba2f228a4fe874f3c496ea76`
  (12 311 529 octets ; URL
  `https://raw.githubusercontent.com/rmoffitt/pdacR/master/data/TCGA_PAAD.rds`) ;
  publication source Raphael et al. 2017 (PMID 28810144, PMCID PMC5964983,
  DOI 10.1016/j.ccell.2017.07.007, Table S1) ; curation Torre-Healy et
  al. 2023 (doi 10.1038/s42003-023-04461-6). (2) Aran et al. 2015 Suppl.
  Data 1, `data/aran2015_supp_data1_ncomms9971-s2.xlsx`, SHA-256
  `fce1ba13ff3a6432b7e4f260eb516e407c967d615ca87bc8dffa7765baf97529`
  (via Europe PMC, zip SHA `4685a8b2…541a5`) — 0 PAAD, non utilisé pour
  les tests. (3) ShrinkageTrees 2.1.1 `data/pdac.rda` (tarball CRAN SHA
  `7c55b4d3…3c85c`, transcrit dans `data/shrinkagetrees_pdac.csv`, SHA
  `a582bc6f…5bab`) — vérification de distribution seulement. (4) Site
  ESTIMATE (MD Anderson) consulté, scores PAAD non récupérés (cf.
  §8.55.2).
- **Entrées du projet.** Base immunitaire `pdac_immune_tcga_fluxes.csv`,
  SHA-256 `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e` ;
  axe `immune_kras_order_tcga.csv`, SHA-256
  `31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d` ;
  écarts §8.48/§8.51 relus en machine dans `ssep_844_rotations.csv` et
  `purity_851_runs.csv` (CD8A : réel 1,2310, nul 0,2472, écart +0,9838).
- **Nature des lignes.** Les flux immunitaires sont des mesures
  instrumentales (séquençage ARN, log2(RSEM+1), brutes) ; ABSOLUTE est
  une estimation publiée depuis le nombre de copies ADN (indépendante de
  l'ARN) ; les résidus sont des valeurs calculées (OLS sur [1, ABSOLUTE]) ;
  les nuls sont des lignes permutées (graine 42) — des échantillons
  hypothétiques, pas des mesures. Aucun mot humain, aucun échantillon
  hypothétique dans les séries réelles.
- **Sorties et scripts de ce chantier.**
  `extract_pdacr_sampinfo_855.py` (SHA `70e72a53…5990`) : transcription
  du sampInfo (181 × 55). `analyze_purity_855.py` (SHA `6bc27fb9…5d75`) :
  porte S, jointure, T1'–T4'. `build_purity_855.py` (SHA `01ee8107…99b2`) :
  4 CSV T5' (résidus vérifiés : moyenne |r| = 0,3757, identique à T2').
  `extract_purity_855.py` (SHA `b6122f89…4dd1`) : lecture des 4 runs.
  `purity_855_sampinfo.csv` (SHA `7a09dde3…b014`, 181 lignes),
  `purity_855_external.csv` (SHA `03f34fe0…bd6f`, 149 tumeurs appariées),
  `purity_855_results.json` (SHA `4ab24df6…7213`, T1'–T4' + porte S),
  `purity_855_results.csv` (SHA `92736cb4…f71c`, T1' par flux),
  `purity_855_immune_resid.csv` (SHA `e7cad0d4…6b9f`, 12 flux résidualisés),
  `purity_855_csv_sha.json` (SHA `f1c5e18f…6183`, SHA des 4 CSV T5'),
  `purity_855_runs.json` (SHA `59a0fc16…a2ce`) / `.csv` (SHA `0c37af88…21a5`,
  4 runs). Manifeste `manifest_v62_purity_855.txt`
  (SHA `9d195acd…7772`) ; log `runs_v62_purity_855.log` ; surveillance
  `watch_v62_purity_855.sh` (SHA `bd643472…ca31`) ; unités systemd
  `v62-purity-855` puis `v62-purity-855b`.
- **Ce qui manque :** ESTIMATE-purity publiée pour PAAD (non récupérée,
  cf. §8.55.2) ; relecture directe de la Table S1 de Raphael (défi PMC
  non contourné — trois vérifications de cohérence à la place, §8.55.2) ;
  les moitiés T4' sont à n = 76/73 ; les p de T1' sont brutes, sans
  correction pour tests multiples.

## 8.55.11 Ce qui manque, ce qui reste ouvert

- **ESTIMATE-purity publiée pour PAAD.** Le site MD Anderson liste PAAD
  (n = 179, RNA-seqV2) : récupérer le fichier par maladie (navigateur ou
  autre voie) donnerait le second contrôle externe gelé — E-EST et E-RES
  sur [ABSOLUTE, ESTIMATE] — et testerait si l'ARN (ESTIMATE) et l'ADN
  (ABSOLUTE) s'accordent sur la part de pureté (~un tiers chacun, ou
  l'un plus que l'autre).
- **Pureté par méthylation.** La même Table S1 contient
  `DNA.hypermethylation.mode.purity` (150/178 appariées, r = 0,856 avec
  ABSOLUTE) : une troisième mesure externe, ADN elle aussi, non testée
  ici (hors protocole gelé) — candidate pour un chantier jumeau, avec la
  fraction leucocytaire par méthylation comme piste d'infiltration
  indépendante (non circulaire, contrairement aux gènes immunitaires).
- **Infiltration indépendante non testée.** Comme au §8.51 : aucun score
  de déconvolution (CIBERSORT/xCell) n'a été joint ; la part « deux
  tiers » restante pourrait encore contenir de l'infiltration (quantité
  de cellules immunitaires) en plus de la co-expression.
- **Le petit effet îlots du §8.51.** +0,2876 au T5, CD4 le plus lié
  (R² 13,2 %) : avec ABSOLUTE, CD4 est aussi très lié (r = −0,633,
  R² = 40,1 %) — l'effet îlots était probablement l'ombre de la vraie
  pureté, vue par un proxy faible. Non tranché formellement (pas de
  régression conjointe [îlots, ABSOLUTE] dans ce chantier).
- **Incident d'exécution.** La machine a redémarré pendant le lot
  (~03h44 UTC, `uptime` : 1 min à 03h45:37 UTC) ; la première unité
  `v62-purity-855` est morte avec elle (aucune entrée dans `journalctl`,
  cause non établie — comme aux §8.41/§8.44/§8.48/§8.51 ; unité
  `--collect`, donc introuvable après sa mort). Aucune sortie n'était
  perdue (1/4 terminé, EXIT 0) ; la relance reprenable `v62-purity-855b`
  a repris au 2e run à 03h45:40 UTC. Bilan final : **4/4 exit 0,
  0 échec**, lot 03h29:22 UTC – 05h02:00 UTC 20 nov.
  (`=== FIN 2026-11-20T05:02:00Z deja_faits=1 termines=3 echecs=0` ;
  surveillance arrêtée d'elle-même à 4/4, tour 1/12). Ralentissement
  noté : d'autres lots v6.2 tournaient en parallèle sur la même machine
  partagée (2 vCPU) — EABS_NUL ~30 min, ERES ~30 min, contre ~10 min
  pour EABS seul.
- **Périmètre.** 4 nouveaux runs v6.2 au maximum (protocole §7,
  substitution ESTIMATE indisponible), aucun autre. Aucun nouveau seuil
  proposé, aucun code modifié, aucun push GitHub dans ce chantier
  (publication sur go séparé ; règle permanente « Toujours github et
  pdf !!! » — par le coordinateur).

— Fin de la §8.55. —
