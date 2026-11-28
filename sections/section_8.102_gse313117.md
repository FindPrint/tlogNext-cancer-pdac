### 8.102 Nouvelle paire : GSE313117 (bras whole-transcriptome) FRAGILE à 10 nuls, avec remappage DPCR1 → MUCL3 re-vérifié ; première candidate GSE55643 écartée (cas complets 24/45) (27 novembre 2026)

Dix-septième paire principale ; protocole opératif gelé 27 nov.
2026 14h47 UTC avant toute construction et tout run
(`PROTOCOL_8102_gse313117.md`, SHA `1babc13b…9285`) ; provenance
`PROVENANCE_8102.md`. Pipeline v6.2, SHA `f07567c4…` vérifié avant
et après chaque run. Aucune association n'a été lue avant le choix
de la cohorte (§8.102.1). Une première candidate, GSE55643, a été
gelée puis écartée dans ce même chantier (protocole
`PROTOCOL_8102_gse55643.md`, SHA `87a5d030…d20b`, inchangé) :
12/12 gènes présents mais cas complets 24/45 < 40 — aucun CSV,
aucun run pour GSE55643 (§8.102.1).

## Verdict d'abord

**FRAGILE — la dix-septième paire principale, GSE313117 bras
whole-transcriptome (n = 79 patients PDAC, 12 flux dont MUCL3
ex-DPCR1), donne `maxsep` réel 0,4261 contre une médiane des nuls
de 0,2536 et un p95 des nuls de 0,3614 : écart contre la médiane
+0,1725, écart contre le p95 +0,0647, rang 11/11, mais 9/10 écarts
réel−nul au-dessus du plancher 0,07 (90,0 %) — le nul s9518
(0,4056) ne laisse qu'un écart de +0,0205, sous le plancher.**
La règle gelée §8.93 §4 n'est satisfaite que sur sa première
branche (réel > p95) : la seconde exige ≥ 95 % des nuls sous le
plancher, et le lot est à 90,0 % — un nul sur dix sous le plancher
suffit à faire passer le verdict de SOLIDE à FRAGILE.

**Et, dans la même phrase, ce qui est solide dans ce FRAGILE :**
le réel bat les 10 nuls (rang 11/11), il dépasse le p95 de
+0,0647, et l'ordre direct est convergent (Δρ médian +0,3070,
11/12 flux positifs — voir §8.102.5), à l'inverse du §8.99 où
`maxsep` séparait sans gradient médian (Δρ −0,0098). Le MC réel
(0,3637) est SOUS le p95 MC des nuls (0,3856) : le MC est
rapporté, il ne décide pas. **Le verdict est un verdict à
10 nuls** : la distribution des nuls est courte, le p95 est
interpolé entre les deux plus hauts nuls (0,3075 et 0,4056),
et la consolidation à 200 nuls n'a pas été faite dans ce
chantier — elle est nommée comme suite à faire au §8.102.7,
pas supposée acquise.

| Porte (protocole §8.102, gelé) | Exigé | Mesuré 27 nov. 2026 | Sort |
|---|---|---|---|
| `maxsep` réel > p95 des 10 nuls | > 0,3614 | **0,4261** | **PASSE** |
| % des nuls sous le plancher 0,07 | ≥ 95 % | **90,0 % (9/10)** | **ÉCHOUE** |
| Écart réel − médiane des nuls | — | **+0,1725** | — |
| Écart réel − p95 des nuls | — | **+0,0647** | — |
| Plus petit écart réel − nul | > 0,07 | **+0,0205** (nul s9518) | **ÉCHOUE** |
| Rang du réel / 11 | — | **11/11** | — |
| Remappage DPCR1 → MUCL3 vérifié (R1–R3) | 3/3 portes | **3/3 — HGNC re-vérifié en direct, données** | **TIENT** |
| 12 flux présents dont MUCL3, DPCR1 absent | 12/12, 0 DPCR1 | **12/12, DPCR1 0 ligne, MUCL3 1 ligne** | **PASSE** |
| Cas complets ≥ 40 | ≥ 40 | **79/79, 0 NaN** | **PASSE** |
| Runs v6.2 fast, exit 0 | 11/11 | **11/11** | **PASSE** |
| Exactitude de l'extraction | 11/11 à 0,0 exact | **11/11, écart max 0,0** | **PASSE** |
| Intégrité des nuls | 10/10 | **10/10 (contrôle, multiset, 0 NaN)** | **PASSE** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que le
signal `maxsep` se sépare du nul sur une dix-septième cohorte
indépendante — la première paire sur GSE313117, cohorte de
tumeurs PDAC de l'essai PANCREAS jamais utilisée dans ce projet
— avec une marge de +0,0647 au-dessus du p95 des nuls, et un
ordre direct convergent (11/12 flux positifs, Δρ médian
+0,3070). Il dit aussi que la queue des nuls mord le plancher :
un nul (s9518, 0,4056) est à 0,0205 du réel — la séparation
n'est pas acquise contre toute la distribution des nuls. Il ne
dit pas que `maxsep` est validé en général : c'est une
dix-septième paire, fragile à 10 nuls, pas une preuve. Il ne
dit rien de clinique : l'étude porte sur l'instrument, pas sur
un remède — aucune affirmation sur le cancer du pancréas
n'est tirée de ce lot. Il ne met pas à jour le compte A2
(défini contre le nul graine 42, non couru ici) ni le LOO :
le registre A2/LOO appartient au coordinateur (§8.102.4).

## 8.102.1 — Question, méthode, règle gelée

### La question

La série §8.93–§8.99 a figé la règle de verdict à 10 nuls frais
(§8.93 §4) et consolidé 200 nuls pour les 15 paires (§8.98),
puis ajouté une seizième paire SOLIDE à 10 nuls (§8.99). La
question ici est celle d'une nouvelle paire, la dix-septième :
le signal `maxsep` se sépare-t-il du nul sur une cohorte
PDAC primaire indépendante, jamais utilisée ni pour la
sélection ni comme paire, avec 10 nuls frais ?

### La chasse — tableau des candidates et des portes

Dépistage GEO par E-utilities (27 nov. 2026) : (a) « pancreatic
ductal adenocarcinoma, expression profiling by array, Homo
sapiens » (49 séries) ; (b) « … expression profiling by high
throughput sequencing, Homo sapiens » (181 séries, 100
retournées, 11 avec n ≥ 40). Reprise des exclusions
antérieures (§8.66 §1.3, §8.69.4, §8.70 §2.3, §8.71 §2.3,
§8.99 §0.1–§0.2) : GSE78229, GSE28735 (re-découpages de
GSE62452), GSE183795 (recouvrement déclaré avec GSE28735 /
GSE62452), GSE15471 (39 < 40), GSE16515 (36 < 40), GSE32676
(25 < 40), GSE32688 (sur-série de GSE32676), GSE91035
(25 < 40), GSE57495 (déjà paire, 13e), GSE62165 (10/12,
DPCR1 et GSTM1 absents), GSE21501, GSE79668, GSE79670
(sur-série), GSE77858 (12/13, MUC17 absent de GPL7264),
GSE43797 (7 < 40), GSE161369 (aucune cohorte bulk de tumeurs
primaires), GSE63158 (35 < 40 chaque sous-série), GSE84219,
GSE179351 (n < 40), GSE131050 (déjà paire FF/FNA), GSE194249
(déjà paire), GSE184585 (déjà paire, §8.99), Chen 2025
(matrice médicament × PDO, pas d'expression), GDC organoid
(déjà paire), OrganoIDNetData (imagerie), GSE262627 (n < 40).

| Candidate | n tumeurs | Plateforme | Gènes v4 | Recouvrement | Téléchargeable | Verdict de porte |
|---|---|---|---|---|---|---|
| GSE50827 | 103 | GPL10558 Illumina | non testé | **OUI — ICGC PACA-AU** (titre « ICGC Pancreas », échantillons GEO-PC) | matrice 16,4 Mo | **EXCLUE (d)** |
| GSE98399 | 0 (PDX) | GPL570 | non testé | non | oui | **EXCLUE (a) — PDX** |
| GSE89792 | 0 (PDX) | — | non testé | non | oui | **EXCLUE (a) — PDX** |
| GSE157494 | 0 (xéno/lignées) | — | non testé | non | oui | **EXCLUE (a) — xénogreffes** |
| GSE130563 | 0 (muscle) | — | non testé | non | oui | **EXCLUE (a) — muscle squelettique** |
| GSE26089 | 0 (xéno/lignées) | — | non testé | non | oui | **EXCLUE (a) — xénogreffes** |
| GSE212575 | ? (essai phase 3) | — | non testé | non établi | **non — matrice 56 Ko = en-tête seule** | **EXCLUE (e)** |
| GSE313657 | ? (spatial) | — | non testé | non | xlsx GeoMx (ROI) | **EXCLUE (a) — spatial, pas du bulk** |
| GSE278670 | 191 (spatial IPMN) | — | non testé | non | oui | **EXCLUE (a) — spatial IPMN** |
| GSE296831 / GSE285406 / GSE303964 / GSE276223 / GSE248585 / GSE347008 | 43–48 (lignées) | — | non testé | non | oui | **EXCLUES (a) — lignées in vitro** |
| GSE314073 / GSE239309 | 40 (lignées isogéniques) | — | non testé | non | oui | **EXCLUES (a) — lignées KRAS** |
| **GSE55643** | **45** | GPL6480 Agilent | **12/12 exacts, DPCR1 exact** | non (Glasgow, 0 GSM commun) | matrice 10,7 Mo | **ÉCARTÉE — cas complets 24/45 < 40 (porte 4)** |
| **GSE313117 (whole-transcriptome)** | **79 patients** | GPL24676/18573 | **11/12 exacts + MUCL3 (ex-DPCR1)** | non (0 GSM commun, autre essai) | TPM 6,5 Mo | **RETENUE — toutes portes OK** |

Portes : (a) n ≥ 40 tumeurs PDAC primaires ; (b) 12/12 gènes
(KRAS présent) ; (c) KRAS présent ; (d) pas de recouvrement ;
(e) données téléchargeables en libre accès. Aucune association
(corrélation KRAS–flux, `maxsep`) n'a été lue pour aucune
candidate avant le gel du protocole de la candidate retenue :
seuls ont été lus en-têtes, titres, caractéristiques,
effectifs, plateformes, identifiants GSM/patients et
comptages de gènes / NaN.

### Première candidate gelée puis écartée : GSE55643

Protocole `PROTOCOL_8102_gse55643.md` gelé 27 nov. 2026
14h41 UTC (SHA `87a5d030…d20b`, inchangé). GSE55643, « Gene
expression in pancreatic ductal adenocarcinoma », Glasgow
(Jamieson et coll., PMID 25415223), GPL6480, 45 tumeurs
(« tissue: Pancreas tumour », Whipple 1–45) + 8 normaux,
matrice SHA `96409670…e08ec` (10 731 208 o), annotation
GPL6480 SHA `aacec81b…5a3ab` (30 723 sondes annotées).
Couverture : PGC 2, REG4 2, CLDN18 1, MUC17 4, DPCR1 2
(symbole exact), CR2 2, KRT20 1, MUC2 3, GSTM1 1 (unique),
CEACAM5 1, CLCA1 1, MUC16 1 sondes ; KRAS 4 sondes ; 0 GSM
commun avec les matrices existantes. **Échec à la porte 4 :
cas complets 24/45** — valeurs manquantes concentrées sur
KRT20 (13/45) et CLCA1 (11/45), puis CEACAM5 3, MUC16 3,
REG4 1, CLDN18 1 ; 21 tumeurs avec ≥ 1 NaN parmi les 13
gènes ; matrice 290 614 NaN / 2 177 929 valeurs. Aucune
imputation autorisée (porte 5) → arrêt, aucun CSV écrit,
aucun run lancé pour GSE55643. Constructeur
`build_fluxes_8102.py` (SHA
`ce6b6d6e08f7e813c4b5ee14658e77b7d409e4dd737635ac1b117f0d8b2590ea`).

### Le choix de la cohorte — sans lire les associations d'abord

**Cohorte choisie : GSE313117, bras whole-transcriptome**,
« Cross-platform comparison of gene expression-based cancer
molecular subtyping reveals discrepancies with exome capture
methods », NCBI GEO. 158 échantillons = 79 patients PDAC
× 2 mesures appariées de la même tumeur (whole-transcriptome
RNA-seq et capture d'exome commerciale Tempus xT/xR).
Caractéristiques : « PDAC », « patient XXXX » (×2). Essai
PANCREAS (NCT04683315, Medical College of Wisconsin, phase 2,
à partir de 2021 ; échantillons tumoraux prétraitement EUS/FNA
et tumeurs du même essai). **Seul le bras whole-transcriptome
est utilisé (79 échantillons, 1 par patient)** ; le bras
exome-capture est EXCLU (seconde mesure des mêmes tumeurs,
pas des patients indépendants). Fichier : supplément officiel
`GSE313117_tpm_whole_transcriptome.csv.gz` (TPM, 24 416 gènes
× 79 échantillons, symboles en lignes, 0 valeur manquante).
Les fichiers bruts n'ont pas été déposés (données personnelles
identifiables, déclaration du résumé). Plateformes GPL24676 /
GPL18573 (Illumina NextSeq 500). n = 79 ≥ 40.
Indépendance, vérifiée avant le gel : jamais mentionnée dans
le livre blanc ni dans aucun protocole du dossier comme paire
courue ; aucune déclaration de recouvrement dans son résumé
GEO ; 0 GSM commun avec GSE131050 (191 GSM locaux vérifiés)
et 0 GSM « GSM9361… » dans aucune des 11 matrices série
locales ; cohorte distincte de GSE131050 (autre essai —
PANCREAS NCT04683315, Medical College of Wisconsin, 2021+ —
contre UNC Lineberger, Rashid et coll. 2020, série soumise
2019 ; autres identifiants patients : patient_2236…
contre S1124.xx / S00x.FNA.Pi) ; ne figure dans aucune liste
d'exclusion du projet. Les appels PurIST de la série, les
sous-types, la survie (OS/PFS) et toute donnée clinique du
fichier `GSE313117_deidentified_clinical_data_final.csv.gz`
(lu uniquement pour sa structure) N'ENTRENT NI dans le
pipeline NI dans le jugement. Le choix repose sur n, le tissu
(tumeurs PDAC primaires), l'indépendance et la couverture
des gènes — jamais sur un signal : aucune corrélation, aucun
ρ, aucune valeur `maxsep` n'a été lue pour GSE313117 avant
le gel du protocole.

### Le remappage DPCR1 → MUCL3 : re-vérifié en direct

DPCR1 n'existe plus comme symbole : 0 ligne dans la matrice
TPM. Le protocole gelé (§2) autorise le remappage vérifié
de type §8.85. Les trois portes, vérifiées le 27 nov. 2026
14h45 UTC, réponses brutes conservées dans le chantier :

- **R1 — HGNC, symbole actuel :**
  `https://rest.genenames.org/fetch/symbol/MUCL3` : **symbol
  MUCL3, HGNC:21666, name « mucin like 3 », status Approved,
  prev_symbol ['DPCR1']**, date_symbol_changed **2018-03-19**,
  ensembl_gene_id ENSG00000168631, entrez_id 135656.
- **R2 — HGNC, recherche par ancien symbole :**
  `https://rest.genenames.org/fetch/prev_symbol/DPCR1` :
  **numFound = 1, un seul résultat — le même enregistrement
  (HGNC:21666, MUCL3)**. DPCR1 n'est le symbole approuvé
  actuel d'aucun autre gène.
- **R3 — Croisement avec les données :** MUCL3 = **1 ligne
  TPM** ; DPCR1 = **0 ligne** (vérifié ici, avant
  construction).

**Le remappage tient.** Une seule chose est autorisée : lire
la ligne MUCL3 comme la mesure du flux v4 historiquement
nommé DPCR1. Le flux est nommé **MUCL3 (ex-DPCR1)** partout —
jamais « DPCR1 » seul. Aucun autre gène n'est mappé à la main
(matrice TPM à symboles directs, aucune ambiguïté
multi-gènes). C'est la troisième paire rendue possible par ce
remappage (§8.85 la première, §8.99 la deuxième).

### Construction (variante (a), 12 flux)

Supplément TPM `GSE313117_tpm_whole_transcriptome.csv.gz`
(SHA `28c946c4…1a15b6`, 6 480 071 o), 24 416 gènes × 79
échantillons, valeurs min 0,000 / médiane 2,384 / max
327 434,895, 0 NaN — valeurs TPM telles que déposées, sans
imputation, sans mise à l'échelle, sans correction, sans log.
Symboles directs en lignes : aucune annotation externe, aucun
mapping de sondes.

Flux : PGC, REG4, CLDN18, MUC17, **MUCL3 (ex-DPCR1)**, CR2,
KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16 — 1 ligne chacun,
0 NaN. Axe : KRAS (1 ligne ; TPM min 1,331 / médiane 13,365
/ max 23,211) ; `step` = rang 0..78, ordre KRAS ascendant.
Cas complets : 79/79, 0 NaN. Portes §1–§2 : 5/5 OK. CSV réel
`pdac_8102_gse313117_fluxes.csv` (SHA `6b83243f…224b7`).

### Règle de verdict gelée (§8.93 §4)

Plancher 0,07. `maxsep` = score principal, lu dans
`master_results.json` →
`run_pipeline/threshold_metadata/threshold_optimization/best_config/metrics/max_separation`.
**SOLIDE** si réel > p95 des 10 nuls ET ≥ 95 % des nuls sous le
plancher ; **FRAGILE** si réel > médiane mais ≤ p95, ou 50–95 %
des nuls sous le plancher ; **NON** si réel ≤ médiane ou < 50 %
des nuls sous le plancher. d_maxsep rapporté contre la
distribution des 10 nuls (graines 9511–9520) et contre sa
médiane ; la graine 42 n'est PAS le nul de référence ici.
Formulations d'analyse uniquement (« les données montrent »),
jamais de prédiction ; aucune affirmation clinique.

## 8.102.2 — Le lot : exécution

- 11 runs v6.2, mode fast, commande identique aux lots
  précédents : `python3 universal_v6.2.0_cohen.py --input <csv>
  --mode fast --output <dossier>`, lanceur séquentiel
  reprenable `run_8102.sh` via `systemd-run`
  (unité `v62-8102-gse313117`), jamais `nohup`, aucun dossier
  de run écrasé.
- Lot 27 nov. 2026 14:47:10 → 15:46:18 UTC (~59 min, dont une
  interruption par redémarrage machine à 15:04:38 UTC —
  unité transiente tuée en cours du nul s9512, relance du
  même lanceur à 15:05:30, reprise au nul s9512, réel et
  s9511 sautés comme déjà complets) : réel puis nuls s9511
  à s9520, **11/11 exit 0** (`runs_8102.log`), 11
  `master_results.json` présents.
- v6.2 SHA-256 vérifié avant le lot, après le lot et avant
  l'extraction : `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  inchangé (3/3).
- Nuls frais graines 9511–9520, script gelé
  `build_null_893.py` (SHA `572b55bc…f467`) : permutation de
  lignes entières, colonne de contrôle (`step`) inchangée.
  Absence de collision vérifiée avant le gel : 9511–9520 ∩
  {9101–9110, 9111–9300, 9301–9310, 9311–9500, 3000–3999, 42}
  = vide (calcul exact sur les ensembles). Intégrité vérifiée
  après construction : 10/10 (contrôle inchangé, mêmes lignes
  en multiset, 0 NaN, même forme 79 × 13).
- Extraction `extract_8102.py` (SHA `bbba0e44…f05`) :
  `extraction_8102.json` (SHA `79c6c306…9b0a0`). Exactitude de
  l'extraction vérifiée par une seconde voie
  (`best_config` vs `raw_best_config`) : **11/11 à 0,0 exact**.

## 8.102.3 — Table complète — réel vs 10 nuls frais

| Run | maxsep | MC | écart réel−nul |
|---|---|---|---|
| **Réel GSE313117** | **0,4261** | **0,3637** | — |
| Nul s9511 | 0,2595 | 0,3759 | +0,1666 |
| Nul s9512 | 0,2476 | 0,3372 | +0,1784 |
| Nul s9513 | 0,2624 | 0,3385 | +0,1637 |
| Nul s9514 | 0,2807 | 0,3411 | +0,1454 |
| Nul s9515 | 0,2176 | 0,3904 | +0,2085 |
| Nul s9516 | 0,1956 | 0,3304 | +0,2305 |
| Nul s9517 | 0,3075 | 0,3798 | +0,1186 |
| Nul s9518 | 0,4056 | 0,3594 | **+0,0205** |
| Nul s9519 | 0,1749 | 0,3265 | +0,2512 |
| Nul s9520 | 0,2181 | 0,3320 | +0,2080 |
| **Médiane des nuls** | **0,2536** | **0,3398** | **+0,1725** |
| **p95 des nuls** | **0,3614** | **0,3856** | **+0,0647** |

Réel : `maxsep` 0,4261, seuil 17,9487, s_norm 0,2099, stabilité
0,9893, robustesse 3,8×10⁻²⁶, sharpness 0,0197. Nuls :
min 0,1749, max 0,4056, étendue 0,2307. **9/10 écarts
au-dessus du plancher 0,07 (90,0 %)** ; le plus petit écart
(+0,0205, nul s9518) est SOUS le plancher de 0,0495 — la
marge qui manque au verdict SOLIDE est un seul nul trop haut.
Rang du réel : 11/11.

## 8.102.4 — Lecture — verdict FRAGILE

La règle gelée §8.93 §4 n'est satisfaite que sur sa première
branche : réel 0,4261 > p95 des nuls 0,3614 (écart +0,0647),
mais 90,0 % des nuls sous le plancher (≥ 95 % exigés).
**Verdict : FRAGILE.** Le réel bat les 10 nuls, et il les bat
de plus de 0,07 pour 9 d'entre eux — mais le plus haut nul
(s9518, 0,4056) n'est battu que de 0,0205.

Deux lectures de prudence, dans le verdict lui-même :
(1) le verdict est un verdict à 10 nuls — le p95 est interpolé
entre les deux plus hauts nuls (0,3075 et 0,4056), et un 11e
tirage au-dessus de 0,3561 ferait passer l'écart contre le
p95 sous le plancher sans changer le verdict FRAGILE ;
(2) la queue des nuls est large (étendue 0,2307, contre
0,1158 au §8.99) : le nul s9518 est un tirage haut isolé,
0,0981 au-dessus du deuxième nul (s9517, 0,3075) — sans lui,
le lot serait SOLIDE (10/10 écarts au-dessus du plancher,
p95 à 0,3075). Cette sensibilité à un seul tirage est
exactement ce que la consolidation à 200 nuls doit trancher
(§8.102.7) : elle n'est pas tranchée ici.

Le compte A2 et le LOO ne sont pas mis à jour dans ce
chantier : A2 est défini contre le nul graine 42, non couru
ici (les nuls sont 9511–9520), et le LOO exige le registre
complet des paires. Ce qui est mesuré ici : 9/10 écarts
réel−nul au-dessus du plancher, min +0,0205, médiane des
écarts +0,1725. La mise à jour du registre A2/LOO appartient
au coordinateur, avec la fusion du §8.102. Pour le
coordinateur : 17e paire, FRAGILE à 10 nuls (la 16e, §8.99,
était SOLIDE à 10 nuls ; A2 classique 11/16 avant ce lot).

## 8.102.5 — Tests directs en appui (ne décident pas)

Spearman de chaque flux vs KRAS (valeurs KRAS TPM relues
depuis le supplément, dans l'ordre des lignes du CSV réel ;
méthode `pandas` Spearman) :

| Flux | ρ vs KRAS |
|---|---|
| PGC | −0,010 |
| REG4 | +0,034 |
| CLDN18 | +0,070 |
| MUC17 | **+0,385** |
| MUCL3 (ex-DPCR1) | +0,070 |
| CR2 | +0,263 |
| KRT20 | **+0,427** |
| MUC2 | **+0,406** |
| GSTM1 | +0,105 |
| CEACAM5 | **+0,410** |
| CLCA1 | +0,351 |
| MUC16 | **+0,416** |

**Δρ médian +0,3070 ; flux positifs 11/12.** Les données
montrent un ordre direct convergent : 11 flux sur 12 sont
positivement ordonnés avec KRAS, et 5 dépassent +0,38
(KRT20 +0,427, MUC16 +0,416, CEACAM5 +0,410, MUC2 +0,406,
MUC17 +0,385) ; seul PGC est quasi nul (−0,010). À l'inverse
du §8.99 (Δρ médian −0,0098, 6/12 positifs), `maxsep` et
l'ordre direct convergent ici — la séparation passe aussi
par un gradient médian par flux. Cette convergence est
consignée telle quelle, sans être élucidée sans preuve. Les
tests directs ne décident pas du verdict : ils décrivent
l'ordre par flux, rien de plus.

## 8.102.6 — Scores compagnons : `maxsep` passe, les autres suivent en partie

- **MC (secondaire, ne décide pas).** MC réel 0,3637
  (0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·sharpness,
  formule réplique §8.93 ; facteur 0,8 non appliqué :
  w_size fast 80 ≥ n//10 = 7). MC des nuls : médiane 0,3398,
  p95 0,3856. Le MC réel est SOUS le p95 MC des nuls
  (−0,0219) : le MC ne confirme pas le passage, et ce n'est
  pas une contradiction — au §8.93, TCGA v4, Immunitaire TCGA
  et PARP TCGA sont SOLIDES en `maxsep` avec un MC réel sous
  le p95 MC de leur réplique. Le MC est rapporté, il ne décide pas.
- **Stabilité.** Réel 0,9893 — haute, comme les autres paires
  SOLIDES et FRAGILES ; les nuls ne sont pas rapportés ici
  (non extraits).
- **Delta, L7a, falsification, F1/F2 après seuil.** Non
  extraits dans ce chantier (hors règle gelée §8.93 §4, qui
  ne les exige pas pour le verdict à 10 nuls). Dette nommée
  au §8.102.7 : ils appartiennent à la consolidation, pas au
  verdict.
- **Seuil.** 17,9487 sur l'axe `step` (0..78) — le seuil
  optimisé du réel se situe aux 23 % de l'axe ordonné KRAS.
  Aucune interprétation temporelle : l'ordre KRAS est un axe
  d'analyse, pas un temps.

## 8.102.7 — Ce que le verdict dit, et ce qu'il ne dit pas ; limites et dettes

**Ce que le verdict dit.** Les données montrent que le signal
`maxsep` se sépare du nul sur GSE313117, une dix-septième
cohorte PDAC primaire indépendante, avec 9/10 écarts
au-dessus du plancher et un réel au-dessus du p95 des nuls,
et un ordre direct convergent (Δρ médian +0,3070, 11/12 flux
positifs). C'est la première paire courue sur cette cohorte,
et la troisième paire rendue possible par le remappage
DPCR1 → MUCL3 vérifié (§8.85, §8.99).

**Ce que le verdict ne dit pas.** Il ne dit pas que `maxsep`
est validé en général. Il ne dit rien de clinique. Il ne dit
pas que la séparation est acquise contre toute la distribution
des nuls — les données montrent le contraire pour un nul sur
dix (s9518, écart +0,0205). Il ne dit pas qu'un flux
« explique » la séparation : cinq flux dépassent +0,38 en
Spearman, mais aucun flux retiré n'a été testé ici.

**Limites.**

1. **Verdict à 10 nuls.** La consolidation à 200 nuls n'a pas
   été faite (200 runs ≈ 12 h, hors du temps de ce chantier).
   Suite à faire : lot de 200 nuls frais (graines à geler par
   le coordinateur, sans collision avec 9511–9520), puis
   re-jugement selon la même règle §8.93 §4. Le verdict
   FRAGILE à 10 nuls n'est pas présenté comme consolidé — et
   la consolidation est ici décisive : un seul nul haut
   (s9518) sépare FRAGILE de SOLIDE.
2. **Queue des nuls large.** Étendue 0,2307 (contre 0,1158 au
   §8.99) ; le nul s9518 (0,4056) est isolé, 0,0981 au-dessus
   du deuxième nul. La distribution des nuls à 10 tirages ne
   permet pas de dire si s9518 est une queue rare ou le début
   d'une queue épaisse.
3. **MC sous le p95.** Le MC réel ne dépasse pas le p95 MC
   des nuls : le score secondaire ne confirme pas le passage.
   C'est consigné, pas escamoté.
4. **Scores compagnons non extraits.** Delta, L7a,
   falsification, F1/F2 après seuil : non extraits ici, à
   extraire à la consolidation.
5. **Remappage.** Un flux sur douze porte un nom changé en
   2018 (MUCL3 ex-DPCR1) : toute comparaison aux paires à 12
   flux doit le rappeler. Le remappage est re-vérifié en
   direct ici (R1–R3), mais il reste un remappage — il est
   nommé partout, jamais caché.
6. **Bras unique, fichiers bruts absents.** Seul le bras
   whole-transcriptome est utilisé (le bras exome-capture,
   mêmes tumeurs, est exclu) ; les fichiers bruts n'ont pas
   été déposés (données personnelles identifiables) — la
   matrice TPM est la seule source, prise telle que déposée.
   Les échantillons sont des tumeurs de l'essai PANCREAS
   (prétraitement EUS/FNA et tumeurs du même essai) : ce ne
   sont pas des tumeurs réséquées chirurgicalement au sens
   strict des cohortes précédentes — c'est dit, pas caché.
7. **A2 / LOO non mis à jour** (voir §8.102.4) : registre du
   coordinateur.
8. **GSE55643 écartée** (voir §8.102.1) : 12/12 gènes présents
   mais cas complets 24/45 — la chasse §8.102 a produit une
   paire et une candidate écartée pour valeurs manquantes, pas
   pour son signal (aucune association lue pour GSE55643).

## 8.102.8 — Provenance

- **Protocole gelé (opératif) :** `PROTOCOL_8102_gse313117.md`
  (SHA-256 `1babc13bb46f1469852629e52b8c7f6dcc9cd9880b1890dfdc13587075d89285`,
  gelé 27 nov. 2026 14h47 UTC, avant toute construction et tout run).
- **Protocole gelé (première candidate, écartée) :**
  `PROTOCOL_8102_gse55643.md`
  (SHA-256 `87a5d030e9670751499e75609deefb7c4e3b02d6922b3a65be7986e1da08d20b`,
  gelé 27 nov. 2026 14h41 UTC, inchangé ; échec porte 4, aucun
  CSV, aucun run).
- **Pipeline :** `universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant le lot 14:47:10 UTC, après le lot 15:46:18 UTC,
  avant l'extraction ; inchangé 3/3 ; fichier jamais modifié).
- **Source des données :** NCBI GEO, série GSE313117,
  « Cross-platform comparison of gene expression-based cancer
  molecular subtyping reveals discrepancies with exome capture
  methods », essai PANCREAS (NCT04683315, Medical College of
  Wisconsin), plateformes GPL24676 / GPL18573.
  URL : `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE313117`.
  Supplément TPM téléchargé du FTP GEO le 27 nov. 2026 :
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE313nnn/GSE313117/suppl/GSE313117_tpm_whole_transcriptome.csv.gz`
  (SHA-256 `28c946c4bfdf3fc23cd2fc787d3eb15d45e5bf093078e49cfd0171351d1a15b6`,
  6 480 071 o, 24 416 gènes × 79 échantillons, 0 NaN).
  Fichier clinique déposé consulté pour sa structure
  uniquement : `GSE313117_deidentified_clinical_data_final.csv.gz`
  (1 801 o ; aucune valeur clinique utilisée).
- **Annotation :** symboles de gènes directs en lignes de la
  matrice TPM (aucune annotation externe, aucun mapping de
  sondes). HGNC REST
  (`https://rest.genenames.org/fetch/symbol/MUCL3`,
  `.../fetch/prev_symbol/DPCR1`, 27 nov. 2026 14h45 UTC) pour
  le remappage R1–R2.
- **Construction :** `build_fluxes_8102_gse313117.py` (SHA
  `1d94cf39215375760ee9e2cc6e7401bc08fb9ca9372445110c9d1924ea6e5e62`),
  valeurs TPM telles que déposées, ordre KRAS ascendant, KRAS =
  axe, jamais un flux. CSV réel
  `pdac_8102_gse313117_fluxes.csv` (SHA
  `6b83243f7ddf26ec2b206373b4f0afaa3808572e336079b4f0ceb0ea999224b7`,
  79 lignes × 13 colonnes).
- **Nuls :** `build_null_893.py` (SHA
  `572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467`),
  graines 9511–9520, permutation de lignes entières, contrôle
  inchangé. SHA des 10 CSV nuls : s9511 `d254d0c9…52be3d`,
  s9512 `3270cf13…228ef`, s9513 `9858f25c…aea`,
  s9514 `c710e365…a02c9`, s9515 `1bc4d512…e0e2d`,
  s9516 `23a36bf1…2d7`, s9517 `e5cb83b2…7491`,
  s9518 `cad04470…262`, s9519 `a2645825…a04`,
  s9520 `7ab1bc2d…e0` (empreintes complètes dans
  `PROVENANCE_8102.md`).
- **Runs :** `run_8102.sh` (SHA
  `a75bbe5bdc4df55e36f5ed813479d007517421b425a134e20be06a87c00951a9`),
  journal `runs_8102.log`, unité systemd
  `v62-8102-gse313117`, 27 nov. 2026 14:47:10 → 15:46:18 UTC
  (redémarrage machine 15:04:38 UTC, relance 15:05:30,
  reprise au nul s9512), 11/11 exit 0. Dossiers
  `results_fast_v62_8102_gse313117` et
  `results_fast_v62_8102_gse313117_nul_s9511` … `s9520`.
- **Extraction :** `extract_8102.py` (SHA
  `bbba0e4451d2d5ede3ac41d000bb78becf8ff99f688ebdd903f5b68dc643bf05`),
  `extraction_8102.json` (SHA `79c6c306…9b0a0`), vérification
  croisée 11/11 à 0,0 exact.
- **Nature des lignes :** chaque ligne du CSV réel est un
  patient PDAC de l'essai PANCREAS (1 mesure
  whole-transcriptome par patient) ; chaque colonne de flux
  est une mesure instrumentale d'expression (RNA-seq, TPM
  déposées) ; `step` est un rang humain (0..78, ordre KRAS
  ascendant), pas une mesure ; MUCL3 est la mesure du gène
  historiquement nommé DPCR1 (remappage re-vérifié, §8.102.1).
  Aucune valeur n'est inventée, imputée ou mise à l'échelle.
- **Ce qui manque :** la consolidation à 200 nuls ; les scores
  compagnons (Delta, L7a, falsification, F1/F2 après seuil) ;
  la mise à jour du registre A2/LOO (coordinateur) ; les
  fichiers bruts RNA-seq (non déposés par les auteurs).
- **Ce qui n'a pas été fait :** aucune modification du livre
  blanc, aucun PDF, aucune Release, aucun push GitHub ;
  `tlogNext-pdac-phase2` et `universal-log-research` non
  touchés ; Kaggle non touché ; pipeline jamais modifié.


## Addendum daté — 27 nov. 2026, 13h00 (heure de Montréal) : nul graine 42 couru

Après la rédaction de cette section, le nul graine 42 a été couru (run local,
builder gelé §8.93, v6.2 fast, sortie `results_fast_v62_8102_gse313117_nul_s42`,
fichier `s42_8102.json`) : maxsep s42 0,2983 (MC 0,3437, seuil 64,10), soit un
écart réel − s42 de +0,1278, au-dessus du plancher 0,07. La paire GSE313117
compte donc dans le registre A2 classique : **A2 11/16 → 12/17**, LOO pire cas
10/15 → 11/16. Le verdict de cette section (FRAGILE à 10 nuls) est inchangé :
l'A2 classique et le verdict à 10 nuls sont deux lectures différentes de la
même paire. Texte d'origine ci-dessus inchangé.

— Fin de la §8.102. —
