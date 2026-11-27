### 8.99 Nouvelle paire : GSE184585 CONFIRME — SOLIDE à 10 nuls, avec remappage DPCR1 → MUCL3 vérifié 5/5 (27 novembre 2026)

Seizième paire principale ; protocole gelé 27 nov. 2026 12h30 UTC
avant toute construction et tout run (`PROTOCOL_899_gse184585.md`,
SHA `00f04748…3057c`) ; provenance `PROVENANCE_899.md`.
Pipeline v6.2, SHA `f07567c4…` vérifié avant et après chaque run.
Aucune association n'a été lue avant le choix de la cohorte (§8.99.1).

## Verdict d'abord

**SOLIDE — la seizième paire principale, GSE184585 (n = 82 tumeurs
PDAC primaires, 12 flux dont MUCL3 ex-DPCR1), donne
`maxsep` réel 0,3712 contre une médiane des nuls de 0,2231 et un
p95 des nuls de 0,2884 : écart contre la médiane +0,1480, écart
contre le p95 +0,0828, rang 11/11, et 10/10 écarts réel−nul
au-dessus du plancher 0,07 (le plus petit écart, +0,0777, reste
au-dessus du plancher).** La règle gelée §8.93 §4 est satisfaite
sur ses deux branches : réel > p95 des nuls ET 100 % des nuls
sous le plancher (≥ 95 % exigés).

**Et, dans la même phrase, la limite : le verdict est un verdict
à 10 nuls.** La distribution des nuls est courte (10 tirages) :
le p95 est interpolé entre les deux plus hauts nuls (0,2822 et
0,2935), et la consolidation à 200 nuls n'a pas été faite dans
ce chantier (temps : 200 runs ≈ 12 h) — elle est nommée comme
suite à faire au §8.99.7, pas supposée acquise. Le test direct
d'ordre est partagé (Δρ médian −0,0098, 6/12 flux positifs —
voir §8.99.5) : `maxsep` sépare ici sans gradient médian par
flux — la séparation vient d'une rupture multi-flux, pas d'un
gradient monotone médian. Le MC réel (0,3552) est SOUS le p95
MC des nuls (0,3722) : le MC est rapporté, il ne décide pas
(§8.93 : TCGA v4, Immunitaire TCGA et PARP TCGA sont SOLIDES
en `maxsep` avec un MC réel sous le p95 MC de leur réplique).

| Porte (protocole §8.99, gelé) | Exigé | Mesuré 27 nov. 2026 | Sort |
|---|---|---|---|
| `maxsep` réel > p95 des 10 nuls | > 0,2884 | **0,3712** | **PASSE** |
| % des nuls sous le plancher 0,07 | ≥ 95 % | **100,0 % (10/10)** | **PASSE** |
| Écart réel − médiane des nuls | — | **+0,1480** | — |
| Écart réel − p95 des nuls | — | **+0,0828** | — |
| Plus petit écart réel − nul | > 0,07 | **+0,0777** (nul s9308) | **PASSE** |
| Rang du réel / 11 | — | **11/11** | — |
| Remappage DPCR1 → MUCL3 vérifié (R1–R5) | 5/5 portes | **5/5 — HGNC, Ensembl, NCBI, données** | **TIENT** |
| 12 flux présents dont MUCL3, DPCR1 absent | 12/12, 0 DPCR1 | **12/12, DPCR1 0 sonde, MUCL3 5 sondes** | **PASSE** |
| Cas complets ≥ 40 | ≥ 40 | **82/82, 0 NaN** | **PASSE** |
| Runs v6.2 fast, exit 0 | 11/11 | **11/11** | **PASSE** |
| Exactitude de l'extraction | 11/11 à 0,0 exact | **11/11, écart max 0,0** | **PASSE** |
| Intégrité des nuls | 10/10 | **10/10 (contrôle, multiset, 0 NaN)** | **PASSE** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que le
signal `maxsep` se sépare du nul sur une seizième cohorte
indépendante — la première paire sur GSE184585, cohorte de
tumeurs primaires MSKCC jamais utilisée dans ce projet — avec
une marge de 0,0828 au-dessus du p95 des nuls, soit 1,2 fois
le plancher au-dessus du p95. Il dit aussi que la séparation
ne passe pas par un gradient médian par flux (Δρ médian
−0,0098) : `maxsep` et l'ordre direct divergent ici, comme
au §8.85 (Δρ médian +0,088) — cette divergence est consignée
telle quelle au §8.99.5, sans être élucidée sans preuve. Il ne
dit pas que `maxsep` est validé en général : c'est une
seizième paire, solide à 10 nuls, pas une preuve. Il ne dit
rien de clinique : l'étude porte sur l'instrument, pas sur
un remède — aucune affirmation sur le cancer du pancréas
n'est tirée de ce lot. Il ne met pas à jour le compte A2
(défini contre le nul graine 42, non couru ici) ni le LOO :
les 10 écarts réel−nul sont tous au-dessus du plancher, mais
le registre A2/LOO appartient au coordinateur (§8.99.4).

## 8.99.1 — Question, méthode, règle gelée

### La question

La série §8.93–§8.98 a figé la règle de verdict à 10 nuls frais
(§8.93 §4) et consolidé 200 nuls pour les 15 paires (§8.98).
La question ici est celle d'une nouvelle paire, la seizième :
le signal `maxsep` se sépare-t-il du nul sur une cohorte
PDAC primaire indépendante, jamais utilisée ni pour la
sélection ni comme paire, avec 10 nuls frais ?

### Le choix de la cohorte — sans lire les associations d'abord

Les 6 candidates de §8.78 ne passent aucune porte du protocole
gelé (§0.1 du protocole) : C1 Chen est exclue par la tâche et
n'est pas une cohorte d'expression v4 (matrice AUC, gènes N/A) ;
C2 GDC et C3 GSE57495 et C4 GSE194249 sont déjà courues comme
paires ; C5 GSE262627 a n = 7 < 40 ; C6 OrganoIDNetData est de
l'imagerie (gènes N/A) et exige un inventaire metadata-only
autorisé, non demandé. **Aucune candidate de §8.78 ne passe les
portes** — le cas prévu par la tâche.

Dépistage GEO (eutils, 27 nov. 2026) des séries « pancreatic
ductal adenocarcinoma, expression profiling by array, Homo
sapiens » : GSE183795 (139 tumeurs) a été écartée — son propre
résumé GEO déclare les données « partially earlier submitted
as GSE28735 and GSE62452 », et GSE62452 est une paire déjà
courue (GSE28735 y est incluse) : re-test déguisé. Écartée
pour recouvrement, pas pour son signal (aucune association lue).

**Cohorte choisie : GSE184585**, « Gene expression data from
patients with pancreatic ductal adenocarcinoma », NCBI GEO,
soumise le 2021-09-23, plateforme GPL17586 (Affymetrix Human
Transcriptome Array 2.0). 82 échantillons, tous intitulés
PDAC-1 à PDAC-82 — tissus PDAC primaires de patients réséqués
chirurgicalement au Memorial-Sloan Kettering Cancer Center
(NY, USA), d'après le résumé GEO ; `disease state: Pancreatic
ductal adecnocarcinoma` (sic) pour 82/82 échantillons dans
les caractéristiques de la matrice. n = 82 ≥ 40.
Indépendance, vérifiée avant le gel : jamais mentionnée dans
le livre blanc ni dans aucun protocole du dossier (grep exact
« GSE184585 » vide, 27 nov. 2026) ; aucune déclaration de
recouvrement avec les cohortes utilisées dans son résumé GEO ;
ne figure dans aucune liste d'exclusion du projet (§8.66 §1.3,
§8.78.8, tâche §8.99). Le choix repose sur n, la plateforme,
le tissu et l'indépendance — jamais sur un signal : aucune
corrélation, aucun ρ, aucune valeur `maxsep` n'a été lue pour
GSE184585 avant le gel du protocole.

### Le remappage DPCR1 → MUCL3 : cinq portes, cinq passages

DPCR1 n'existe plus comme symbole : aucune entrée Entrez dans
org.Hs.eg.db 3.23.1, 0 sonde dans hta20transcriptcluster.db
8.8.0. Le protocole gelé (§2) autorise le remappage vérifié
de type §8.85. Les cinq portes, vérifiées le 27 nov. 2026,
réponses brutes conservées dans le chantier :

- **R1 — HGNC, symbole actuel :**
  `https://rest.genenames.org/fetch/symbol/MUCL3` : **symbol
  MUCL3, HGNC:21666, name « mucin like 3 », status Approved,
  prev_symbol ['DPCR1']**, prev_name ['diffuse panbronchiolitis
  critical region 1'], alias_symbol ['PBLT', 'bCX105N19.6',
  'C6orf37'], ensembl_gene_id ENSG00000168631, entrez_id 135656,
  location 6p21.33, **date_symbol_changed 2018-03-19**. Le nom
  a changé en 2018 — DPCR1 est l'ancien symbole, pas un
  synonyme courant.
- **R2 — HGNC, recherche par ancien symbole :**
  `https://rest.genenames.org/fetch/prev_symbol/DPCR1` :
  **numFound = 1, un seul résultat — le même enregistrement
  (HGNC:21666, MUCL3)**. DPCR1 n'est le symbole approuvé
  actuel d'aucun autre gène.
- **R3 — NCBI RefSeq, corroboration :** org.Hs.eg.db 3.23.1 :
  Entrez 135656 → RefSeq **NM_080870**, Ensembl
  ENSG00000168631 (+ 4 autres, les mêmes que §8.79) ; alias
  DPCR1 et MUCL3 → même _id 18000. (RefSeq Gene MUCL3
  NM_080870.4, Synonyms C6orf37, DPCR1, PBLT, au §8.85.)
- **R4 — Ensembl :** MUCL3 résout (`id ENSG00000168631`,
  description « mucin like 3 [Source:HGNC Symbol;Acc:HGNC:21666] »,
  GRCh38, chr 6, 30940973–30954221) ; DPCR1 ne résout pas
  (« No valid lookup found for symbol DPCR1 », comme au §8.79).
- **R5 — Croisement avec les données détenues :** MUCL3 = **5
  sondes** (Entrez 135656) dans la base HTA 2.0, présentes dans
  la matrice ; DPCR1 = **0 sonde**, aucune entrée Entrez.

**Le remappage tient.** Une seule chose est autorisée : lire
la ligne MUCL3 comme la mesure du flux v4 historiquement
nommé DPCR1. Le flux est nommé **MUCL3 (ex-DPCR1)** partout —
jamais « DPCR1 » seul. Aucun autre gène n'est mappé à la main.

### Construction (variante (a), 12 flux)

Matrice série `GSE184585_series_matrix.txt.gz` (SHA
`e2be8441…6de01`, 22 632 266 o), 70 523 sondes × 82
échantillons, valeurs min 2,40 / médiane 5,19 / max 19,93,
0 NaN — valeurs telles que déposées, sans imputation, sans
mise à l'échelle, sans correction. Mapping sondes → symboles
construit à neuf depuis Bioconductor `hta20transcriptcluster.db`
8.8.0 (SHA `70680ab9…92f`, tarball ; SQLite extrait SHA
`405837e1…a4dac`) + `org.Hs.eg.db` 3.23.1 (SQLite extrait SHA
`bbdf1a4d…f3dba`) : 72 618 sondes HTA, 32 120 mappées vers un
symbole, 30 262 présentes dans la matrice → 23 864 gènes
uniques après agrégation par médiane ; mapping écrit
`GPL17586_probe2symbol.tsv` (SHA `2592d258…9e`). (La voie
`GPL17586.annot.gz` du FTP GEO répond 404 « Object not
found! » ; le SOFT `GPL17586_family.soft.gz`, > 1,2 Go en
cours de téléchargement, a été abandonné au profit des bases
Bioconductor, précédent déjà utilisé dans le dossier —
`hgu219.db`, `org.Hs.eg.db` détenus.)

Flux : PGC, REG4, CLDN18, MUC17, **MUCL3 (ex-DPCR1)**, CR2,
KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16. Sondes par flux :
PGC 1, REG4 1, CLDN18 1, MUC17 3, MUCL3 5, CR2 2, KRT20 1,
MUC2 3, GSTM1 1, CEACAM5 1, CLCA1 1, MUC16 1. Axe : KRAS
(1 sonde ; min 7,50 / médiane 8,00 / max 9,17) ; `step` =
rang 0..81, ordre KRAS ascendant. Cas complets : 82/82,
0 NaN. Portes §1–§2 : 5/5 OK. CSV réel
`pdac_899_gse184585_fluxes.csv` (SHA `07540af5…99d13`).

### Règle de verdict gelée (§8.93 §4)

Plancher 0,07. `maxsep` = score principal, lu dans
`master_results.json` →
`run_pipeline/threshold_metadata/threshold_optimization/best_config/metrics/max_separation`.
**SOLIDE** si réel > p95 des 10 nuls ET ≥ 95 % des nuls sous le
plancher ; **FRAGILE** si réel > médiane mais ≤ p95, ou 50–95 %
des nuls sous le plancher ; **NON** si réel ≤ médiane ou < 50 %
des nuls sous le plancher. d_maxsep rapporté contre la
distribution des 10 nuls (graines 9301–9310) et contre sa
médiane ; la graine 42 n'est PAS le nul de référence ici.
Formulations d'analyse uniquement (« les données montrent »),
jamais de prédiction ; aucune affirmation clinique.

## 8.99.2 — Le lot : exécution

- 11 runs v6.2, mode fast, commande identique aux lots
  précédents : `python3 universal_v6.2.0_cohen.py --input <csv>
  --mode fast --output <dossier>`, lanceur séquentiel
  reprenable `run_899.sh` via `systemd-run`
  (unité `v62-899-gse184585`), jamais `nohup`, aucun dossier
  de run écrasé.
- Lot 27 nov. 2026 12:37:38 → 13:06:35 UTC (~29 min) :
  réel puis nuls s9301 à s9310, **11/11 exit 0**
  (`runs_899.log`), 11 `master_results.json` présents.
- v6.2 SHA-256 vérifié avant le lot, après le lot et avant
  l'extraction : `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  inchangé (3/3).
- Nuls frais graines 9301–9310, script gelé
  `build_null_893.py` (SHA `572b55bc…f467`) : permutation de
  lignes entières, colonne de contrôle (`step`) inchangée.
  Absence de collision vérifiée avant le gel : 9301–9310 ∩
  {9101–9110, 9111–9300, 3000–3999, 42} = vide (calcul exact
  sur les ensembles). Intégrité vérifiée après construction :
  10/10 (contrôle inchangé, mêmes lignes en multiset, 0 NaN,
  même forme 82 × 13).
- Extraction `extract_899.py` (SHA `939b90f6…9d0fe`) :
  `extraction_899.json` (SHA `ee175155…7`). Exactitude de
  l'extraction vérifiée par une seconde voie
  (`best_config` vs `raw_best_config`) : **11/11 à 0,0 exact**.

## 8.99.3 — Table complète — réel vs 10 nuls frais

| Run | maxsep | MC | écart réel−nul |
|---|---|---|---|
| **Réel GSE184585** | **0,3712** | **0,3552** | — |
| Nul s9301 | 0,2180 | 0,3325 | +0,1532 |
| Nul s9302 | 0,2251 | 0,3335 | +0,1461 |
| Nul s9303 | 0,2180 | 0,3324 | +0,1532 |
| Nul s9304 | 0,2737 | 0,3401 | +0,0975 |
| Nul s9305 | 0,2234 | 0,3345 | +0,1478 |
| Nul s9306 | 0,2032 | 0,3301 | +0,1680 |
| Nul s9307 | 0,1777 | 0,3611 | +0,1935 |
| Nul s9308 | 0,2935 | 0,3492 | +0,0777 |
| Nul s9309 | 0,2229 | 0,3337 | +0,1483 |
| Nul s9310 | 0,2822 | 0,3813 | +0,0890 |
| **Médiane des nuls** | **0,2231** | **0,3341** | **+0,1480** |
| **p95 des nuls** | **0,2884** | **0,3722** | **+0,0828** |

Réel : `maxsep` 0,3712, seuil 72,50, s_norm 0,1835, stabilité
0,9905, robustesse 5,3×10⁻²⁷, sharpness 0,0152. Nuls :
min 0,1777, max 0,2935, étendue 0,1158. **10/10 écarts
au-dessus du plancher 0,07 (100,0 %)** ; le plus petit écart
(+0,0777, nul s9308) dépasse le plancher de 0,0077 seulement
— la marge la plus étroite du lot est mince, et c'est dit.
Rang du réel : 11/11.

## 8.99.4 — Lecture — verdict SOLIDE

La règle gelée §8.93 §4 est satisfaite sur ses deux branches :
réel 0,3712 > p95 des nuls 0,2884 (écart +0,0828), et 100,0 %
des nuls sous le plancher (≥ 95 % exigés). **Verdict :
SOLIDE.** Le réel bat les 10 nuls, et il les bat tous de plus
de 0,07 — y compris le plus haut nul (s9308, 0,2935).

Deux lectures de prudence, dans le verdict lui-même :
(1) le verdict est un verdict à 10 nuls — le p95 est interpolé
entre les deux plus hauts nuls, et un 11e tirage au-dessus de
0,3012 ferait passer l'écart contre le p95 sous le plancher
sans changer le verdict SOLIDE (la branche « % sous plancher »
resterait à 100 % tant que chaque écart dépasse 0,07) ;
(2) le plus petit écart (+0,0777) ne dépasse le plancher que
de 0,0077 : la queue des nuls mord presque le plancher, comme
dans les cas FRAGILES du §8.93 — ici elle ne le mord pas.

Le compte A2 et le LOO ne sont pas mis à jour dans ce
chantier : A2 est défini contre le nul graine 42, non couru
ici (les nuls sont 9301–9310), et le LOO exige le registre
complet des paires. Ce qui est mesuré ici : 10/10 écarts
réel−nul au-dessus du plancher, min +0,0777, médiane des
écarts +0,1480. La mise à jour du registre A2/LOO appartient
au coordinateur, avec la fusion du §8.99.

## 8.99.5 — Tests directs en appui (ne décident pas)

Spearman de chaque flux vs KRAS (valeurs KRAS relues depuis la
matrice série via le mapping gelé, dans l'ordre des lignes du
CSV réel ; méthode `pandas` Spearman) :

| Flux | ρ vs KRAS |
|---|---|
| PGC | +0,029 |
| REG4 | −0,048 |
| CLDN18 | +0,224 |
| MUC17 | +0,117 |
| MUCL3 (ex-DPCR1) | +0,176 |
| CR2 | −0,237 |
| KRT20 | −0,393 |
| MUC2 | −0,072 |
| GSTM1 | −0,304 |
| CEACAM5 | **+0,550** |
| CLCA1 | **−0,531** |
| MUC16 | +0,057 |

**Δρ médian −0,0098 ; flux positifs 6/12.** Les données
montrent une dispersion des ordres directs : CEACAM5 est le
flux le plus positivement ordonné avec KRAS (+0,550), CLCA1
le plus négativement (−0,531), devant KRT20 (−0,393) et
GSTM1 (−0,304) ; les 8 autres flux sont entre −0,237 et
+0,224. La médiane est proche de zéro : `maxsep` sépare le
réel du nul sans gradient médian par flux. Cette divergence
entre le score multi-flux et l'ordre direct est consignée
telle quelle, sans être élucidée sans preuve — comme au
§8.85, où `maxsep` passait avec un Δρ médian de +0,088
seulement. Les tests directs ne décident pas du verdict :
ils décrivent l'ordre par flux, rien de plus.

## 8.99.6 — Scores compagnons : `maxsep` passe, les autres suivent en partie

- **MC (secondaire, ne décide pas).** MC réel 0,3552
  (0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·sharpness,
  formule réplique §8.93 ; facteur 0,8 non appliqué :
  w_size fast 80 ≥ n//10 = 8). MC des nuls : médiane 0,3341,
  p95 0,3722. Le MC réel est SOUS le p95 MC des nuls
  (−0,0170) : le MC ne confirme pas le passage, et ce n'est
  pas une contradiction — au §8.93, TCGA v4, Immunitaire TCGA
  et PARP TCGA sont SOLIDES en `maxsep` avec un MC réel sous
  le p95 MC de leur réplique. Le MC est rapporté, il ne décide pas.
- **Stabilité.** Réel 0,9905 — haute, comme les autres paires
  SOLIDES ; les nuls ne sont pas rapportés ici (non extraits).
- **Delta, L7a, falsification, F1/F2 après seuil.** Non
  extraits dans ce chantier (hors règle gelée §8.93 §4, qui
  ne les exige pas pour le verdict à 10 nuls). Dette nommée
  au §8.99.7 : ils appartiennent à la consolidation, pas au
  verdict.
- **Seuil.** 72,50 sur l'axe `step` (0..81) — le seuil
  optimisé du réel se situe aux 88 % de l'axe ordonné KRAS.
  Aucune interprétation temporelle : l'ordre KRAS est un axe
  d'analyse, pas un temps.

## 8.99.7 — Ce que le verdict dit, et ce qu'il ne dit pas ; limites et dettes

**Ce que le verdict dit.** Les données montrent que le signal
`maxsep` se sépare du nul sur GSE184585, une seizième cohorte
PDAC primaire indépendante, avec 10/10 écarts au-dessus du
plancher et un réel au-dessus du p95 des nuls. C'est la
première paire courue sur cette cohorte, et la deuxième paire
rendue possible par le remappage DPCR1 → MUCL3 vérifié (§8.85
était la première).

**Ce que le verdict ne dit pas.** Il ne dit pas que `maxsep`
est validé en général. Il ne dit rien de clinique. Il ne dit
pas que la séparation passe par un gradient par flux — les
données montrent le contraire au niveau médian (Δρ −0,0098).
Il ne dit pas que CEACAM5 « explique » la séparation : CEACAM5
est le flux le plus positivement ordonné avec KRAS (+0,550),
mais un seul flux ne fait pas le score multi-flux, et aucune
analyse par flux retiré n'a été faite ici.

**Limites.**

1. **Verdict à 10 nuls.** La consolidation à 200 nuls n'a pas
   été faite (200 runs ≈ 12 h, hors du temps de ce chantier).
   Suite à faire : lot de 200 nuls frais (graines à geler par
   le coordinateur, sans collision avec 9301–9310), puis
   re-jugement selon la même règle §8.93 §4. Le verdict SOLIDE
   à 10 nuls n'est pas présenté comme consolidé.
2. **Marge étroite sur le plus petit écart.** +0,0777 contre
   le nul s9308 : 0,0077 au-dessus du plancher. Un nul plus
   haut ferait passer cet écart sous le plancher sans changer
   le verdict (la branche p95 resterait, tant que le réel
   dépasse le p95), mais la fragilité de la queue des nuls est
   réelle et mesurée.
3. **MC sous le p95.** Le MC réel ne dépasse pas le p95 MC
   des nuls : le score secondaire ne confirme pas le passage.
   C'est consigné, pas escamoté.
4. **Scores compagnons non extraits.** Delta, L7a,
   falsification, F1/F2 après seuil : non extraits ici, à
   extraire à la consolidation.
5. **Remappage.** Un flux sur douze porte un nom changé en
   2018 (MUCL3 ex-DPCR1) : toute comparaison aux paires à 12
   flux doit le rappeler. Le remappage est vérifié 5/5, mais
   il reste un remappage — il est nommé partout, jamais caché.
6. **Annotation HTA 2.0.** Le mapping vient de Bioconductor
   (hta20transcriptcluster.db 8.8.0, source Entrez 2021-04-14)
   + org.Hs.eg.db 3.23.1, pas du SOFT GEO (inaccessible en
   pratique : > 1,2 Go, abandonné). 40 453 des 72 618 sondes
   HTA n'ont pas de gene_id (non codant / non annoté) : elles
   ne portent aucun flux ici, et c'est sans effet sur les 13
   gènes lus, tous mappés.
7. **A2 / LOO non mis à jour** (voir §8.99.4) : registre du
   coordinateur.

## 8.99.8 — Provenance

- **Protocole gelé :** `PROTOCOL_899_gse184585.md`
  (SHA-256 `00f04748fe1d5416ffa47df467b878ab0c630afc6c7ba5a41090c4cea943057c`,
  gelé 27 nov. 2026 12h30 UTC, avant toute construction et tout run).
- **Pipeline :** `universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant le lot 12:37:38 UTC, après le lot 13:06:35 UTC,
  avant l'extraction ; inchangé 3/3 ; fichier jamais modifié).
- **Source des données :** NCBI GEO, série GSE184585,
  « Gene expression data from patients with pancreatic ductal
  adenocarcinoma », soumise 2021-09-23, plateforme GPL17586,
  BioProject PRJNA765314.
  URL : `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE184585`.
  Matrice série téléchargée du FTP GEO le 27 nov. 2026 :
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE184nnn/GSE184585/matrix/GSE184585_series_matrix.txt.gz`
  (SHA-256 `e2be8441979ee9210033fac588ed99e2605cdaa598e39e6d1e0d5304aad6de01`,
  22 632 266 o, 70 523 sondes × 82 échantillons, 0 NaN).
- **Annotation :** Bioconductor `hta20transcriptcluster.db`
  8.8.0 (tarball SHA `70680ab930d4290431c312449e0ab6b46f933d55c61012e903baefbaae07a92f` ;
  SQLite extrait SHA `405837e13af445ccf8686c7f2985cbd5c685109d57b5c7e2ec946a2c562a4dac` ;
  source Entrez Gene 2021-04-14) + `org.Hs.eg.db` 3.23.1
  (SQLite extrait SHA `bbdf1a4d9181ac0873d8993b6c25742d6658eaa6c14a10b2df1a19dfba1f3dba`).
  Mapping écrit `GPL17586_probe2symbol.tsv` (SHA
  `2592d2586af7f166121849c67b35e504e43e37e4176c022768abf0fc49ce929e`,
  30 262 sondes). HGNC REST
  (`https://rest.genenames.org/fetch/symbol/MUCL3`,
  `.../fetch/prev_symbol/DPCR1`, 27 nov. 2026) et Ensembl REST
  (`https://rest.ensembl.org/lookup/symbol/homo_sapiens/MUCL3`
  et `.../DPCR1`, 27 nov. 2026) pour le remappage R1–R4.
- **Construction :** `build_fluxes_899.py` (SHA
  `a9ede3eefae47a7d12fa6accd9400e7da4ed1afef3d0ce30b848e2c326956388`),
  valeurs telles que déposées, agrégation par médiane des
  sondes multiples, ordre KRAS ascendant, KRAS = axe, jamais
  un flux. CSV réel `pdac_899_gse184585_fluxes.csv` (SHA
  `07540af57ef27974178036ea333f4ad51d9a19e49d7993f1d997b80fe6b99d13`,
  82 lignes × 13 colonnes).
- **Nuls :** `build_null_893.py` (SHA
  `572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467`),
  graines 9301–9310, permutation de lignes entières, contrôle
  inchangé. SHA des 10 CSV nuls : s9301 `e67eb8bf…6397`,
  s9302 `d153a6db…abf4`, s9303 `35d94cfc…cb4`,
  s9304 `bcf812b4…ba30`, s9305 `0edc936a…2b7`,
  s9306 `2edea177…50fe`, s9307 `9b3e5791…424`,
  s9308 `5978da32…d904`, s9309 `58e90221…77d8`,
  s9310 `3f8dd192…1bba` (empreintes complètes dans
  `PROVENANCE_899.md`).
- **Runs :** `run_899.sh`, journal `runs_899.log`, unité
  systemd `v62-899-gse184585`, 27 nov. 2026 12:37:38 →
  13:06:35 UTC, 11/11 exit 0. Dossiers
  `results_fast_v62_899_gse184585` et
  `results_fast_v62_899_gse184585_nul_s9301` … `s9310`.
- **Extraction :** `extract_899.py` (SHA
  `939b90f6545672c6609980b82e8b0beac36efdf7c8f312481558e7c949c9d0fe`),
  `extraction_899.json` (SHA `ee175155…7`), vérification
  croisée 11/11 à 0,0 exact.
- **Nature des lignes :** chaque ligne du CSV réel est une
  tumeur PDAC primaire (MSKCC, réséquée) ; chaque colonne de
  flux est une mesure instrumentale d'expression (microarray
  HTA 2.0, valeurs déposées) ; `step` est un rang humain
  (0..81, ordre KRAS ascendant), pas une mesure ; MUCL3 est
  la mesure du gène historiquement nommé DPCR1 (remappage
  vérifié 5/5, §8.99.1). Aucune valeur n'est inventée, imputée
  ou mise à l'échelle.
- **Ce qui manque :** la consolidation à 200 nuls ; les scores
  compagnons (Delta, L7a, falsification, F1/F2 après seuil) ;
  la mise à jour du registre A2/LOO (coordinateur) ; le SOFT
  GEO GPL17586 complet (abandonné, > 1,2 Go — remplacé par
  les bases Bioconductor, §8.99.1).
- **Ce qui n'a pas été fait :** aucune modification du livre
  blanc, aucun PDF, aucune Release, aucun push GitHub ;
  `tlogNext-pdac-phase2` et `universal-log-research` non
  touchés ; pipeline jamais modifié.
