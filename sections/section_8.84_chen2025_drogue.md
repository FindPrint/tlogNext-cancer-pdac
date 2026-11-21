### 8.84 Lot drogue Chen 2025 (46 PDO × 63 AUC) : la paire exploratoire CONFIRME (consolidée), deux co-sensibilités à la gemcitabine, et les deux contrôles positifs de l'article répliqués — mais drogue × KRAS et drogue × MTAP sont intestables dans les données publiées (21 novembre 2026)

Piste 1 du lot du 21 nov. 2026 (lot drogue Chen 2025) ; protocole gelé
21 nov. 2026 ~14h10 EST avant tout téléchargement nouveau, toute
copie et tout calcul (`PROTOCOL_chen2025_drogue_884.md`, SHA
`62ee265e…fd13c00`) ; provenance `PROVENANCE_884.md`.

## Verdict d'abord

**CONFIRME (exploratoire, consolidée) — la paire pipeline sur les
46 organoïdes de Chen et al. 2025, ordonnés par sensibilité à la
gemcitabine, donne `d_maxsep = +0,0982` (réel 0,3478 contre nul
0,2496), au-dessus du plancher 0,07 — et les deux nuls frais
imposés par la règle gelée donnent des écarts encore plus grands
(+0,1528 et +0,1607), donc 3/3 au-dessus du plancher : le passage
est dit « consolidé ». MAIS la paire est exploratoire (n = 46 < 50,
plancher du pilote) et reste hors compte A2 (9/13, 11/13 positifs,
inchangés) ; l'ancien MC ne sépare pas (+0,0015). Et, dans la même
section, l'autre moitié du verdict : les tests directs
drogue × KRAS (D3) et drogue × MTAP (D4) sont IMPOSSIBLES — aucune
table du statut KRAS somatique ni du statut MTAP par PDO n'existe
dans les 12 Supplementary Data ni dans la Source Data de l'article
(0 identifiant DAC dans les Data 1–12 ; un seul organoïde KRAS
p.G12C nommé dans le texte, sans identifiant). Ce qui est testable
sans génotype, en revanche, est positif : co-sensibilité à la
gemcitabine pour le paclitaxel (rho +0,5085, FDR 0,0191) et la
mitomycine C (+0,4759, FDR 0,0257) ; réplication du contrôle
positif Olaparib / BRCA2 (médianes 0,9561 contre 0,9984, U = 8,0,
p = 0,00015) ; réplication quasi exacte des 5 correcteurs CFTR
(p 0,0059 / 0,0050 / 0,0061 / 0,0156 / 0,0015 contre 0,006 / 0,005 /
0,006 / 0,016 / 0,002 dans l'article) ; et un hit FDR pour la
chimio-résistance des 5 CFTR VUS_D, l'irinotécan (FDR 0,0300).**

| Porte (protocole §3/§6/§8, gelé) | Exigé | Mesuré 21 nov. 2026 | Sort |
|---|---|---|---|
| MOESM13 SHA / taille (G1) | `0e009cd5…5340`, 35 732 o | **identiques** | **PASSE** |
| Forme 63 × 46, 0 NaN, Gemcitabine présente (G2) | 63 / 46 / 0 | **63 / 46 / 0** | **PASSE** |
| BRCA2 (6) et CFTR VUS_D (5) nommés présents (G3) | 11/11 | **11/11** | **PASSE** |
| Paire exploratoire : `d_maxsep > 0,07` et positif | > 0,07 | **+0,0982** (réel 0,3478, nul 0,2496) | **CONFIRME (exploratoire)** |
| Nuls frais (règle gelée, d dans [−0,07 ; +0,14[) | 2 nuls frais, 3/3 > 0,07 = consolidé | **+0,1528 et +0,1607 — 3/3 > 0,07** | **CONSOLIDÉ** |
| Exactitude de l'extraction | 4/4 à 0,0 exact | **4/4, écart max 0,0** | **PASSE** |
| Vérification indépendante des tests directs | 0 problème | **0 problème** (écart max \|rho\| 5,6e-17) | **PASSE** |
| D3 drogue × KRAS / D4 drogue × MTAP | table ≥ 40/46 PDO | **aucune table — 0 identifiant DAC** | **IMPOSSIBLES** |
| D1 co-sensibilité gemcitabine | FDR < 0,05 | **2 hits** (paclitaxel, mitomycine C) | **POSITIF** |
| D2a Olaparib / BRCA2 (1 test) | p < 0,05 | **p = 0,00015** | **RÉPLIQUÉ** |
| D2c correcteurs CFTR (5 tests) | p < 0,05 | **5/5** (p 0,0015–0,0156) | **RÉPLIQUÉS** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que le
signal `maxsep` se sépare du nul sur une matrice de drogues
ordonnée par la gemcitabine — avec une cascade réelle qui s'effondre
presque entièrement (89,04 % au deuxième pas contre 19,40 % pour le
nul graine 42) et un écart qui survit à deux nuls frais, dont les
maxsep (0,1950 et 0,1870) sont plus bas que le nul graine 42
(0,2496). Il dit aussi que les écrans PDO portent de l'information
directe reproductible : les deux contrôles positifs nommés par
l'article se re-mesurent ici à des p quasi identiques, et deux
cytotoxiques suivent la gemcitabine après correction FDR. Il ne dit
pas que `maxsep` est validé en général : c'est une paire
exploratoire à n = 46, hors A2, sur un axe (la sensibilité à la
gemcitabine) qui n'est pas l'axe KRAS — elle ne confirme rien sur
la chaîne v4 et ne compte jamais comme une paire principale. Il ne
dit rien de clinique : les AUC sont des viabilités ex vivo sur 5
jours, pas des réponses de patients — aucune affirmation sur un
traitement n'est tirée de ce lot. Il ne dit pas que KRAS ou MTAP
sont sans effet sur ces PDO : sans table par-PDO, la question est
intestable ici, pas tranchée.

**Fragilité, dite en tête.** Le verdict tient à une seule paire
exploratoire mesurée aujourd'hui, à n = 46, avec un écart
(+0,0982) à 0,0282 au-dessus du plancher sur la paire graine 42 —
les nuls frais le consolident (+0,1528 / +0,1607), mais le nul
graine 42 est le plus haut des trois nuls, et l'ancien MC ne sépare
pas du tout (+0,0015) : la séparation est portée par `maxsep` et
par la cascade, pas par le score historique. La matrice porte un
plafond répété (0,9985714… dans 12,5 % des cellules) et 8 drogues
dépassent 1 — les tests de rang y sont robustes, mais les médianes
proches du plafond sont des non-réponses plafonnées, pas des mesures
fines. Enfin, la paire ordonne par la gemcitabine, une drogue, et
non par un gène : c'est un test d'ordre entre drogues, pas un test
de la chaîne KRAS.

## 8.84.1 — La source : Chen et al. 2025, et ce que MOESM13 contient vraiment

Article : Yin, X., Shen, H., Wang, H. *et al.*, « Pathogenic germline
variants in Chinese pancreatic adenocarcinoma patients », *Nature
Communications* **16**, 2214 (2025), DOI
10.1038/s41467-025-57520-3 (reçu 21 janv. 2024, accepté 25 févr.
2025, publié 5 mars 2025 ; CC BY-NC-ND 4.0 ; Shanghai Changhai
Hospital). Fichier source : Supplementary Data 10 =
`41467_2025_57520_MOESM13_ESM.xlsx` (MOESM13), 35 732 o, SHA-256
`0e009cd56d2f6c25b0b355590becc4abfee3e1080633173bc33606d1bf325340`
— IDENTIQUE à l'empreinte du §8.79. Copie de travail :
`data/Chen2025_MOESM13_SupplData10.xlsx` (copie du fichier déjà
détenu et vérifié au §8.79, SHA re-vérifié après copie).

Nature des lignes (vérifiée avant le gel) : feuille « All Drugs AUC »,
63 drogues × 46 PDO (`DAC_61 … DAC_115`), AUC normalisée publiée
(viabilité CellTiter-Glo, 7 concentrations en duplicata, 5 jours ;
AUC GraphPad Prism 9, « normalized AUC was obtained by dividing
each AUC by the maximum AUC for that drug » ; viabilités plafonnées
à 100). **0 NaN** sur 2 898 cellules ; min 0,0000 (Valproic acid,
DAC_22) ; médiane 0,9107 ; max 1,1746 (CCT245737). Deux anomalies
consignées sans correction : **8 drogues avec max > 1** (Sorafenib
1,0564 ; Lenvatinib 1,0496 ; AZD6738 1,0986 ; AZD5363 1,1668 ;
CCT245737 1,1746 ; Palbociclib 1,0929 ; Everolimus 1,1018 ;
Rapamycin 1,1085) — la normalisation « par le maximum » ne plafonne
donc pas à 1 dans le fichier déposé ; et la valeur plafond
**0,9985714285714287 (= 699/700) dans 362/2 898 cellules (12,5 %)**
— Valproic acid 36/46, APR-246 32/46, Dacarbazine 29/46,
Hydroxychloroquine 27/46, Pemetrexed 25/46, Olaparib 20/46 — lue
comme un plafond de non-réponse, conservée telle quelle.
Gemcitabine (ancre) : min 0,1399 / médiane 0,4384 / max 0,8167 /
écart-type 0,1882 (ddof = 1) ; PDO le plus sensible DAC_1 (0,1399),
le plus résistant DAC_110 (0,8167). La feuille « CFTR Drugs AUC »
(15 drogues CFTR × 15 PDO, 0 NaN, min 0,6462 / max 1,0000) sert au
test D2c. Forme des identifiants : l'article écrit DAC102, MOESM13
écrit DAC_102 — mappage par suppression de '_' (bijectif sur les
46) ; les 6 BRCA2 et les 5 CFTR VUS_D nommés sont tous présents.

Antériorité : le pilote v5.9.4 (`pilot.md`, `run_chen.py`) n'a JAMAIS
couru — bloqué avant tout run, N = 46 < 50 (minimum v5.9.4), 0 run,
0 résultat. Le pilote ne prédit rien ici.

## 8.84.2 — Ce qui est nouveau ici par rapport aux écrans PRISM / GDSC2 déjà négatifs

Les écrans déjà négatifs sont PRISM primaire 24Q2 (6 790 composés,
0 FDR < 0,05, FDR min 0,959 — §8.7), PRISM secondaire 19Q4 (1 437,
0 FDR < 0,05, FDR min 0,625) et GDSC2 (269, 0 FDR < 0,05, FDR min
0,561 / 0,882 — §8.40.3), repris tels quels, jamais recalculés.
Ce lot est nouveau sur quatre points, et un re-test partiel sur un
cinquième :

1. **Autre système :** organoïdes 3D dérivés de patients, cohorte
   chinoise, contre lignées 2D DepMap.
2. **Autre mesure :** AUC de viabilité sur 7 concentrations en
   duplicata (CellTiter-Glo, 5 jours), contre viabilité à dose
   unique 2,5 µM (PRISM primaire) et LN_IC50 / AUC (GDSC2).
3. **Autre bibliothèque :** 63 composés bespoke (chimiothérapie
   n = 8, cycle cellulaire n = 4, dommages ADN n = 5, cascades
   classiques n = 34, autres n = 12), dont les inhibiteurs KRAS
   G12C AMG510 et MRTX849.
4. **Autre groupement :** PRISM/GDSC2 groupaient par dépendance
   Chronos KRAS (continue) ; ici le groupement direct KRAS/MTAP
   dépend d'une table par-PDO (conditionnel, §8.84.3) et l'axe
   pipeline est la sensibilité à la gemcitabine, pas KRAS.
5. **Re-test partiel déclaré :** Gemcitabine, Fluorouracil,
   Oxaliplatin, Irinotecan, Cisplatin, Paclitaxel, Docetaxel,
   Olaparib, Trametinib, Palbociclib sont présents dans les deux
   mondes — un négatif 2D ne prouve pas un négatif 3D PDO, et le
   re-test vaut la peine pour cette raison.
6. **Absences communes, à ne pas re-présenter comme découverte :**
   vopimetostat absent des 63 comme des trois écrans §8.40 ;
   aucun inhibiteur PRMT5 ni MAT2A dans les 63 comme dans les
   écrans §8.40 — la sensibilité différentielle au vopimetostat
   lui-même reste intestable partout.

## 8.84.3 — D3 et D4 IMPOSSIBLES : aucune table KRAS / MTAP par PDO dans les données publiées

Tentative gelée (§4 du protocole), effectuée après le gel, en
exécution directe, et mesurée fichier par fichier :

1. **Source Data, Fig. 6 (MOESM17)** — 5 454 570 o, SHA-256
   `917a1011426c5ee749343ccabf8126e35923a65c4719ec929f84aa29a511f7b1`
   (feuille « Figure 6 », 121 × 151). Fig. 6b : **Z-scores des AUC
   seulement** (63 × 46), aucune ligne d'annotation mutationnelle.
   Fig. 6e : **statut CFTR par PDO pour les 15 du volet CFTR** —
   MT : DAC13, DAC24, DAC72, DAC84 (4) ; WT : 11 autres — avec les
   AUC des 5 correcteurs (recoupement Fig. 6e vs MOESM13 feuille
   CFTR : 75/75 paires, écart max 4,96e-08). **Aucune ligne KRAS,
   aucune ligne MTAP dans toute la feuille.**
2. **Description des suppléments (MOESM3)** — 140 637 o, SHA
   `3a84243b…5313c569` : aucune des Data 1–12 n'est une table
   somatique par organoïde.
3. **Autres Supplementary Data (MOESM4–MOESM12, MOESM14, MOESM15)** —
   tous téléchargés et examinés cellule par cellule (recherche
   `DAC`, `KRAS`, `MTAP` exacts) : MOESM4 (Data 1, 1 124 × 18) —
   0 DAC, 0 KRAS, 0 MTAP, identifiants patients GN1, GN2, … sans
   mappage GN → DAC ; MOESM5 (Data 2) — 0 partout ; MOESM6
   (Data 3, 8 408 × 38) — 0 vrai DAC (4 « HDAC », faux positifs),
   0 KRAS, **1 MTAP** : une variante germinale VUS_D missense
   p.P41L (chr 9:21816715, C>T) chez un patient de la cohorte
   découverte (échantillon EN233) — une variante germinale, pas
   un statut de délétion MTAP, pas un PDO ; MOESM7 (Data 4) —
   liste des 150 CSG, KRAS et MTAP simples entrées de liste ;
   MOESM8 (Data 5) — 0 vrai DAC, MTAP en liste seulement ;
   MOESM9–MOESM12, MOESM14, MOESM15 — 0 partout. SHA dans
   PROVENANCE_884 §3. Figure 1 de la Source Data (oncoprint,
   208 × 124) : une ligne KRAS (somatique) existe, mais **aucun
   identifiant DAC dans toute la feuille** — les 122 colonnes sont
   des tumeurs de la cohorte découverte, sans mappage vers les
   organoïdes.

**Conclusion mesurée : D3 (drogue × KRAS) IMPOSSIBLE** — aucune
table du statut KRAS somatique par PDO ; l'article nomme un seul
organoïde KRAS p.G12C sans identifiant DAC. **D4 (drogue × MTAP)
IMPOSSIBLE** — aucune table du statut MTAP (délétion / nombre de
copies 9p21) par PDO ; MTAP n'est nommé dans l'article que comme
gène de susceptibilité, jamais comme statut par organoïde. Ce sont
des verdicts d'intestabilité, pas des échecs cachés : la question
« drogue × KRAS / MTAP » sur ces PDO n'est pas tranchée, elle est
intestable avec les données publiées. **D2c (volet CFTR) :
POSSIBLE** — statut CFTR MT/WT des 15 PDO obtenu de la Source
Data Fig. 6e.

## 8.84.4 — Construction des flux et runs v6.2

Script `build_fluxes_884_chen.py` (SHA `d37973c8…9cd`) : 46 PDO
ordonnés par AUC Gemcitabine croissante (`step` 0..45), 62 flux =
les autres drogues, AUC publiées, ordre MOESM13, aucune
transformation, aucune imputation (0 NaN). Contrôle : `step`
(rang Gemcitabine) — jamais un flux, pas de doublon. Cible :
défaut du pipeline (première colonne hors contrôle, comme au
§8.79) — APR-246. Nul : lignes permutées, graine 42, `step`
intact. CSV réel `pdac_884_chen_fluxes.csv` (SHA
`73fefc10…4554`), nul `pdac_884_chen_fluxes_nul.csv` (SHA
`43866a01…200a`) ; nuls frais graines 8841 (`09e8e31e…06da7`) et
8842 (`adc95aa8…64dd3a`).

Runs v6.2 fast (`universal_v6.2.0_cohen.py`, SHA `f07567c4…c3abf`,
vérifié avant et après, jamais modifié), lanceur reprenable
`run_v62_lot.sh`, unités systemd `v62-884chen` (lot principal,
14:01:58–14:18:42Z) et `v62-884fresh` (nuls frais,
14:19:12–14:31:36Z) — jamais nohup. **4/4 runs, exits 0/0/0/0,
0 échec.** Dossiers `results_fast_v62_884_chen`,
`..._chen_nul`, `..._chen_nul_s8841`, `..._chen_nul_s8842`
(`master_results.json` 27,8–28,2 Mo chacun). Avertissement
consigné (figures seulement, exits 0) : la clustermap échoue sur
les deux lots (« Image size of 1800x73080 pixels is too large »,
62 flux) — aucune figure de clustermap, les `master_results.json`
sont complets. Extraction `extract_884.py` (SHA
`1d5a25c9…151`) ; vérification indépendante `verify_884.py`
(SHA `19d778ed…5255`) : **4/4 à 0,0 exact** sur maxsep, ancien MC
et stabilité (`maxsep_884_verify.json`, verdict OK).

## 8.84.5 — La paire : `d_maxsep = +0,0982`, consolidée par les nuls frais

| | Réel | Nul (graine 42) | Nul frais s8841 | Nul frais s8842 |
|---|---|---|---|---|
| `maxsep` | **0,3478** | 0,2496 | 0,1950 | 0,1870 |
| `d_maxsep` (réel − nul) | — | **+0,0982** | **+0,1528** | **+0,1607** |
| ancien MC (secondaire) | 0,3511 | 0,3496 | 0,3400 | 0,3400 |
| `d_MC` | — | +0,0015 | +0,0111 | +0,0111 |
| `sep` (= maxsep/(1+maxsep)) | 0,2580 | 0,1997 | 0,1632 | 0,1576 |
| S_sep | 0,3464 | 0,2490 | 0,1930 | 0,1863 |
| Delta | 1,890 | 1,662 | 1,659 | 1,646 |
| Cascade (%) | 2,16 / 89,04 / 95,62 / 98,62 / 100,0 | 0,0 / 19,40 / 25,87 / 30,19 / 36,65 | 2,62 / 5,62 / 8,62 / 15,09 / 15,09 | 0,0 / 34,53 / 41,37 / 78,08 / 95,62 |
| Cascade (pas) | 1 / 40 / 43 / 44 / 45 | 0 / 9 / 12 / 14 / 16 | 1 / 3 / 4 / 7 / 7 | 0 / 16 / 19 / 35 / 43 |
| Stabilité | 0,9962 | 0,9977 | 0,9897 | 0,9958 |
| L7a | flat 0,298 | flat 0,317 | flat 0,318 | flat 0,291 |
| L7b (light) | ROBUSTE | ROBUSTE | ROBUSTE | ROBUSTE |
| Falsification (brute) | 0,311 | 0,300 | 0,308 | 0,394 |
| F1 / F2 après seuil (ratios) | 0,148 / 0,077 | 1,885 / 1,682 | 0,281 / 0,439 | 1,859 / 0,575 |
| Seuil MC (%) | 23,81 | 60,87 | 39,13 | 52,17 |
| Estimateurs tous OK | 21 | 22 | 22 | 23 |
| Cible / contrôle / n | APR-246 / step / 46 | idem | idem | idem |

Valeurs exactes : réel maxsep 0,3477606744, nul 0,2495638180,
s8841 0,1949927558, s8842 0,1870370511 ; écarts
+0,0981968565 / +0,1527679187 / +0,1607236233 (min +0,0982,
médiane +0,1528, max +0,1607). **3/3 au-dessus du plancher 0,07 :
le passage est « consolidé » selon la règle gelée** (le verdict
reste celui de la paire graine 42, qui passe déjà). S_sep suit
`maxsep` (+0,0974 / +0,1535 / +0,1602) ; Delta suit aussi
(+0,2283 / +0,2311 / +0,2443). **L'ancien MC ne sépare pas**
(+0,0015 contre le nul graine 42 ; +0,0111 contre les frais) :
la séparation est portée par `maxsep` et par la cascade, pas par
le score historique. La cascade réelle s'effondre presque
entièrement au deuxième pas (89,04 % au pas 40, puis 95,62 % au
pas 43) quand le nul graine 42 plafonne à 36,65 % — mais le nul
frais s8842 monte à 95,62 % au dernier pas : la cascade seule ne
suffit pas, c'est l'écart `maxsep` qui fait le verdict. L7a est
flat des deux côtés (0,298 contre 0,317 / 0,318 / 0,291) : aucun
vote directionnel, descriptif seulement. Falsification :
**indisponible sous n = 75** (valeurs brutes 0,311 / 0,300 /
0,308 / 0,394, non interprétées). Régime `criticality` des quatre
côtés. F1/F2 : le réel s'effondre après le seuil (ratios 0,148 /
0,077) quand le nul graine 42 augmente (1,885 / 1,682) — lecture
descriptive, les nuls frais sont partagés (s8841 : 0,281 / 0,439 ;
s8842 : 1,859 / 0,575).

**Lecture honnête.** L'écart graine 42 (+0,0982) n'est qu'à 0,0282
au-dessus du plancher, et le nul graine 42 est le plus haut des
trois nuls (0,2496 contre 0,1950 et 0,1870) : sans les nuls frais,
le passage serait dit fragile ; avec eux, il est consolidé — mais
la consolidation vient de nuls frais *plus bas*, pas d'un réel
plus haut. Le réel lui-même (0,3478) est modeste à côté des paires
GEO (GSE57495 : 0,6381). La paire reste exploratoire, hors A2, et
son axe (gemcitabine) n'est pas l'axe KRAS : elle montre que
l'ordre de sensibilité à une drogue structure les autres drogues
chez ces PDO, rien de plus.

## 8.84.6 — Tests directs : D1 positif (2 hits FDR), D2a et D2c répliqués, D2b un hit FDR

Script `direct_tests_884_chen.py` (SHA `68811366…dd3`), sorties
`direct_tests_884_chen.json` (SHA `53602a86…dba`) et tables
`direct_tests_884_chen_D1.csv` / `..._D2b.csv`. Sens des AUC :
**AUC basse = sensible**. Vérification indépendante
`verify_884_direct.py` (SHA `dae9478e…52fd`) : Spearman recalculé
par Pearson sur rangs à la main (écart max |rho| 5,6e-17),
Mann-Whitney recalculé par sommes de rangs à la main (U identiques
partout), FDR BH recalculée (2 hits D1 et 1 hit D2b retrouvés à
l'unité près) — **0 problème, statut OK**.

### D1 — Co-sensibilité à la gemcitabine : 2 hits FDR < 0,05 sur 62

Spearman (AUC drogue, AUC Gemcitabine), n = 46, FDR BH sur 62.
**Hits : paclitaxel rho +0,5085, p = 0,000308, FDR 0,0191 ;
mitomycine C rho +0,4759, p = 0,00083, FDR 0,0257.** 11/62 p < 0,05
brutes (contre ~3,1 attendues par hasard), 33/62 rho > 0. Juste
au-dessus du seuil : irinotécan +0,4278 (FDR 0,0625), masitinib
+0,4110 (FDR 0,0706), vinblastine +0,3944 (FDR 0,0791). Sens :
rho > 0 = les PDO sensibles à la gemcitabine le sont aussi à la
drogue — les deux hits sont des cytotoxiques, cohérents avec une
sensibilité cytotoxique partagée, pas avec une cible. Les rho
négatifs les plus forts (valproic acid −0,3883, FDR 0,0791 ;
motixafortide −0,3389, FDR 0,1462 ; AZD5363 −0,2924, FDR 0,2556)
ne passent pas la correction. Table complète sans sélection dans
`direct_tests_884_chen_D1.csv`.

### D2a — Olaparib / BRCA2 : RÉPLIQUÉ (un seul test pré-enregistré)

Olaparib AUC, BRCA2-mutants n = 6 (DAC102, DAC58, DAC81, DAC85,
DAC53 somatiques ; DAC4 germinal — nommés dans l'article) contre
n = 40 autres. Médianes **0,9561 contre 0,9984**, U = 8,0,
**p = 0,0001466** — HIT (p < 0,05, pas de FDR : un seul test).
Sens attendu confirmé : les mutants sont plus sensibles (AUC plus
basse). AUC des 6 mutants : 0,9304 / 0,9371 / 0,9443 / 0,9679 /
0,9786 / 0,9786 — tous sous la médiane du reste, qui est au
plafond (0,9984 ≈ 0,9985714…, non-réponse plafonnée). Descriptif :
DAC99 (mutation somatique ATM selon l'article) est le PDO le plus
sensible à l'olaparib de tous (AUC 0,9068, rang 1/46) ; DAC76
(rang 9/46, AUC 0,9818) l'est moins. C'est une réplication du
contrôle positif de l'article, pas une découverte : l'article
nommait déjà ces organoïdes.

### D2b — CFTR VUS_D chimio-résistants : 1 hit FDR, l'irinotécan

Les 5 nommés (DAC13, DAC73, DAC110, DAC32, DAC30) contre n = 41,
Mann-Whitney bilatéral sur les 63 drogues, FDR BH sur 63.
**Hit : irinotécan, médianes 0,9622 contre 0,8642, diff +0,0980,
p = 0,000476, FDR 0,0300.** 14/63 p < 0,05 brutes (contre ~3,2
attendues). Sens attendu (article) : résistants (AUC plus haute) —
le signe est le même sur les cytotoxiques listées : gemcitabine
diff +0,1893 (p = 0,0181, FDR 0,125), docétaxel +0,1537
(p = 0,0287, FDR 0,1389), mitomycine C +0,1435 (p = 0,0089,
FDR 0,125), paclitaxel +0,1115 (p = 0,0198, FDR 0,125), cisplatine
+0,0752 (p = 0,0339, FDR 0,1526) — toutes NS après correction
sauf l'irinotécan. Autres p brutes < 0,05 sans FDR : MRTX849
diff +0,0880 (p = 0,0040, FDR 0,125), masitinib +0,0404
(p = 0,0065, FDR 0,125), sulfatinib +0,0607 (p = 0,0135,
FDR 0,125), lénvatinib +0,0196 (p = 0,0132, FDR 0,125),
olaparib +0,0011 (p = 0,0175, FDR 0,125), pomalidomide +0,0614
(p = 0,0198, FDR 0,125), CCT245737 +0,0700 (p = 0,0250,
FDR 0,1389), valproic acid −0,0064 (p = 0,0278, FDR 0,1389).
AMG510 : médianes 1,0 contre 1,0 (p = 0,356, FDR 0,5757) — plafond
des deux côtés, intestable par ce test. Le sous-ensemble
« chimiothérapie n = 8 » n'est pas identifiable dans MOESM13
(aucun drapeau) : aucun sous-test chimiothérapie inventé.
Table complète dans `direct_tests_884_chen_D2b.csv`.

### D2c — Volet CFTR : 5/5 correcteurs répliqués quasi à l'identique

Statut CFTR MT n = 4 (DAC13, DAC24, DAC72, DAC84 — Source Data
Fig. 6e) contre WT n = 11, valeurs MOESM13 feuille CFTR,
Mann-Whitney bilatéral (Wilcoxon dans l'article) :

| Correcteur | Médiane MT | Médiane WT | U | p (ici) | p (article) |
|---|---|---|---|---|---|
| Tezacaftor | 0,8667 | 0,9374 | 2,0 | **0,005861** | 0,006 |
| Lumacaftor | 0,8198 | 0,9794 | 0,0 | **0,004962** | 0,005 |
| FDL169 | 0,7963 | 0,8837 | 0,5 | **0,006066** | 0,006 |
| Galicaftor | 0,8065 | 0,8422 | 3,0 | **0,01563** | 0,016 |
| Elexacaftor | 0,7379 | 0,8225 | 0,0 | **0,001465** | 0,002 |

Les 5 p sont < 0,05, dans le sens attendu (mutants plus sensibles,
AUC plus basses), et chacune est à ≤ 0,001 de la p publiée : la
réplication est quasi exacte, ce qui valide aussi la lecture des
fichiers (les AUC Fig. 6e et MOESM13 coïncident à 5e-08 près).
C'est une réplication, pas une découverte — l'article affirmait
déjà ces 5 différences.

### D5 — Appui pipeline (descriptif, ne décide pas)

Spearman de chaque flux avec le pas (ordre Gemcitabine), réel
contre nul graine 42 : Δrho médian **+0,0510**, |Δrho| moyen
0,2606, **36/62 Δrho positifs**. Les plus grands |Δrho| :
valproic acid −0,7271, paclitaxel +0,6100, CCT245737 +0,6056,
irinotécan +0,5553, dacarbazine −0,5542, hydroxychloroquine
−0,5405 (9 flux avec |Δrho| > 0,5) — un signal d'ordre faible en
médiane, porté par quelques drogues, dont les deux hits D1
(paclitaxel, irinotécan) et la valproic acid (plafond, à lire avec
prudence). d de Cohen marginal des 62 flux (réel contre nul) :
**max |d| = 5,65e-15**, soit 0,0000 à 4 décimales — l'écart au
zéro exact vient de l'aller-retour CSV (texte), il valide la
construction du nul (marginales préservées), il ne mesure pas la
séparation.

## 8.84.7 — Ce que ce lot change, et ce qu'il ne change pas

- **A2 inchangé : 9/13 au-dessus du plancher, 11/13 positifs.**
  La paire Chen est exploratoire (n = 46 < 50) et hors compte.
- **La piste drogue Chen est close comme lot v6.2 :** la paire
  passe (consolidée), deux co-sensibilités FDR tiennent, les
  contrôles positifs de l'article se répliquent — mais l'axe
  n'est pas KRAS et les tests KRAS/MTAP sont impossibles sans
  table par-PDO. Aucune piste médicamenteuse nouvelle pour le
  sous-groupe KRAS-fort ne sort de ce lot : les hits D1 sont des
  cytotoxiques partagées, pas des cibles ; le hit D2b
  (irinotécan, CFTR VUS_D) concerne 5 PDO définis par une
  germinale CFTR, pas par KRAS ; MRTX849/AMG510 ne sont testables
  contre KRAS sans le statut du seul organoïde G12C (non nommé).
- **Le négatif PRISM/GDSC2 (§8.7, §8.40) n'est pas renversé :**
  ce lot ne teste pas la même question (pas de groupement KRAS,
  pas de Chronos) et ne trouve pas de médicament différentiel
  pour un groupe KRAS ou MTAP — il ne pouvait pas, faute de
  table. Il montre seulement qu'un écran PDO 3D porte de
  l'information d'ordre et des réplications propres.
- **Pistes ouvertes (pas des verdicts) :** (a) la table par-PDO
  KRAS/MTAP n'existe pas dans les suppléments — une demande aux
  auteurs ou un dépôt WGS des 69 organoïdes la fournirait, et
  alors D3/D4 deviendraient courables sur la même matrice ;
  (b) l'organoïde KRAS G12C unique, sensible à AMG510/MRTX849
  selon l'article, n'est pas identifiable ici — son DAC seul
  permettrait un test ciblé ; (c) la co-sensibilité
  gemcitabine–paclitaxel–mitomycine C est un fait d'écran, pas
  une piste thérapeutique : elle dit que ces cytotoxiques
  varient ensemble chez ces PDO, pas qu'il faut les combiner.
- **C3 reste LEVÉE** (elle l'était depuis le §8.71) ; ce chantier
  ne rouvre rien.

## 8.84.8 — Provenance (complète, liens cliquables)

- Article : Yin, X. *et al.*, *Nat. Commun.* **16**, 2214 (2025),
  DOI 10.1038/s41467-025-57520-3,
  https://doi.org/10.1038/s41467-025-57520-3 (CC BY-NC-ND 4.0).
- MOESM13 (Supplementary Data 10) :
  https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM13_ESM.xlsx
  — 35 732 o, SHA-256
  `0e009cd56d2f6c25b0b355590becc4abfee3e1080633173bc33606d1bf325340`.
- Source Data (MOESM17) :
  https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM17_ESM.xlsx
  — 5 454 570 o, SHA-256
  `917a1011426c5ee749343ccabf8126e35923a65c4719ec929f84aa29a511f7b1`.
- Description des suppléments (MOESM3) :
  https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM3_ESM.pdf
  — 140 637 o, SHA-256
  `3a84243b7b4c3bbab172a4ead61725663fd076cd00664091ea0fad3c5313c569`.
- Autres Supplementary Data examinés (MOESM4–MOESM12, MOESM14,
  MOESM15) : SHA dans PROVENANCE_884 §3 ; fichiers conservés
  dans `chen884_scratch/`.
- Pipeline : `universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
- Protocole gelé : `PROTOCOL_chen2025_drogue_884.md`, SHA-256
  `62ee265e2e8b71d0970b3dc58e2d8cdfe8c8aad727b43c687a6b37230fd13c00`.
- Provenance : `PROVENANCE_884.md`, SHA-256
  `1eb03395d69f48bdd116693d9232f969fcc07802f38c8fef024855ab767bca43`.
- CSV de flux : réel SHA
  `73fefc1044d9a92865b5a3a26aa493d0c62d2c9188fcd88e656d62fce7624554`,
  nul graine 42 SHA
  `43866a016393c34681517d04752ec18597f14deab56bbc900a49b51231c6200a`,
  nuls frais s8841 SHA
  `09e8e31efdfcf5dc89d942a9c2f50a37a4e0e6b2f9a50a168114e78129206da7`,
  s8842 SHA
  `adc95aa8b411cc9598802ff0a81e76bbb12227bfdea11ecf85c7f54fd164dd3a`.
- Scripts : `build_fluxes_884_chen.py` SHA
  `d37973c841170cac7502772266720883128ce3af33e864faf292348e33c0e9cd`,
  `direct_tests_884_chen.py` SHA
  `68811366a2a005d86d3c61ba5018747977031badbb1a707651ebf8d0ab4ffdd3`,
  `verify_884_direct.py` SHA
  `dae9478e1c3be59f770352fdbb46793d7dec4f74c6bdcfb38c4836221fe05f3a` ;
  `extract_884.py` SHA
  `1d5a25c93c1d92b5dc8121517772d7447423096692d1b5f1cd382cdd5394d363`, `verify_884.py` SHA
  `19d778ed796cac911542525572692086628c9ec5b4568ef2b7fdfa60f3298c5a` ; sorties `extract_884.json` SHA
  `d5380813224462a372f5dfd7ecee630fafd0636a333c5819a6ab691474139b9e`, `direct_tests_884_chen.json` SHA
  `53602a8662618c08033eb76821619b214868da3ee5383e7027337b8497cc9dba`, `maxsep_884_verify.json` SHA
  `7a6bc2022ec06f801e48426cf693a061647b239213499b8db4457c2d129aaf96`, `verify_884_direct.json` SHA
  `f3786eccd78ad35fb5039bf406e5756dfc3a71a70e5ee31266db5b3cc77f4a22`.
- Écrans antérieurs repris tels quels : PRISM primaire 24Q2
  (§8.7), PRISM secondaire 19Q4 et GDSC2 (§8.40.3) ; pilote Chen
  v5.9.4 : 0 run (N = 46 < 50).

## 8.84.9 — Ce qui manque

- D3/D4 impossibles (voir §8.84.3) ; vopimetostat et inhibiteurs
  PRMT5/MAT2A absents des 63 drogues ; sous-ensemble
  « chimiothérapie n = 8 » non identifiable dans MOESM13 ;
  n = 46 < 50 : paire exploratoire, hors A2 ; plafond répété
  0,9985714… (12,5 % des cellules) et 8 drogues > 1 (valeurs
  conservées telles quelles) ; clustermap absente (figure trop
  grande, 62 flux) ; falsification indisponible sous n = 75.
  Tous les SHA de cette section sont relevés des fichiers et
  re-vérifiés ; aucun nombre n'est un placeholder.

— Fin de la §8.84. —
