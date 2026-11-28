### 8.101 Consolidation GSE184585 à 200 nuls — FRAGILE : le SOLIDE à 10 nuls ne survit pas (28 novembre 2026)

Seizième paire principale, consolidation de §8.99 ; protocole gelé
27 nov. 2026 14h40 UTC avant toute construction et tout run
(`PROTOCOL_8101_gse184585_200nulls.md`, SHA `14e752c2…f22bf`) ;
provenance `PROVENANCE_8101.md`. Pipeline v6.2, SHA `f07567c4…`
vérifié avant et après le lot. 200 nuls frais pipeline (10 anciens
s9301–s9310 + 190 nouveaux s9311–s9500), 201 runs v6.2 fast, 0
manquant.

## Verdict d'abord

**FRAGILE — la seizième paire, GSE184585 (n = 82 tumeurs PDAC
primaires, 12 flux dont MUCL3 ex-DPCR1), donne `maxsep` réel
0,3712 contre une médiane des nuls de 0,2257 et un p95 des nuls
de 0,3014 : écart contre la médiane +0,1455, écart contre le p95
+0,0698, rang 200/201, et 188/200 écarts réel−nul au-dessus du
plancher 0,07 (94,0 %).** La règle gelée §8.93 §4 exige les deux
branches pour SOLIDE : réel > p95 des nuls ET ≥ 95 % des nuls
sous le plancher. La première branche passe (0,3712 > 0,3014) ;
la seconde échoue de deux nuls (188/200, il en fallait 190/200).
**Le verdict SOLIDE à 10 nuls du §8.99 ne survit pas à la
consolidation.** Ce n'est pas un renversement brutal : le réel
n'a pas bougé (0,3712, inchangé), c'est la distribution des
nuls qui a parlé — 200 tirages au lieu de 10, un nul au-dessus
du réel (s9337, 0,3969) et 11 autres à moins de 0,07 du réel.
Le verdict est FRAGILE de justesse, et la justesse est mesurée :
deux des douze nuls au-dessus du plancher sont à moins de 0,0001
du plancher (s9335, écart +0,0699 ; s9469, écart +0,0699942 —
0,0000058 sous le plancher).

| Porte (règle gelée §8.93 §4) | Exigé | Mesuré à 200 nuls | Sort |
|---|---|---|---|
| `maxsep` réel > p95 des 200 nuls | > 0,3014 | **0,3712** | **PASSE** |
| % des nuls sous le plancher 0,07 | ≥ 95 % | **94,0 % (188/200)** | **ÉCHOUE** |
| Écart réel − médiane des nuls | — | **+0,1455** | — |
| Écart réel − p95 des nuls | — | **+0,0698** | — |
| Plus petit écart réel − nul | > 0,07 | **−0,0257** (nul s9337, au-dessus du réel) | **ÉCHOUE** |
| Rang du réel / 201 | — | **200/201** | — |
| Nuls au-dessus du réel | — | **1/200 (s9337)** | — |
| Runs v6.2 fast, exit 0 | 201/201 | **201/201** | **PASSE** |
| Exactitude de l'extraction | 201/201 à 0,0 exact | **201/201 (voir §8.101.2)** | **PASSE** |
| Intégrité des nuls | 200/200 | **200/200 (contrôle, multiset, 0 NaN)** | **PASSE** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que le
signal `maxsep` reste au-dessus du p95 de 200 nuls sur GSE184585,
mais que la queue des nuls mord le plancher : 12 nuls sur 200 sont
à 0,07 ou moins du réel, dont un au-dessus. Il dit que le verdict
à 10 nuls du §8.99 était un verdict à 10 nuls — le §8.99.4
l'avait écrit : le p95 à 10 tirages était interpolé, et la
consolidation était la suite nommée, pas une formalité. Il ne dit
pas que la paire est « fausse » : FRAGILE n'est pas NON — le réel
est au-dessus de 199 nuls sur 200 et au-dessus du p95. Il ne dit
rien de clinique : l'étude porte sur l'instrument, pas sur un
remède — aucune affirmation sur le cancer du pancréas n'est tirée
de ce lot. Il ne met pas à jour le registre A2/LOO : le registre
appartient au coordinateur (§8.99.4) — les lectures comptables
sont au §8.101.7, le registre lui-même n'est pas touché ici.

## 8.101.1 — Question, méthode, règle gelée

### La question

Le §8.99 a jugé GSE184585 SOLIDE contre 10 nuls frais (réel
0,3712, p95 0,2884, 10/10 écarts au-dessus du plancher) en
nommant la limite : verdict à 10 nuls, p95 interpolé, consolidation
à 200 nuls à faire (§8.99.7, dette nº 1). La question ici est la
suite directe, identique à celle du §8.98 pour les 15 paires :
le verdict survit-il à une distribution de **200 nuls frais
pipeline** — la cible que le §8.53 nomme pour un p95 stable
(~200 nuls par paire) ? Le réel est repris du §8.99, aucune
valeur re-saisie à la main ; la distribution est faite de nuls
pipeline uniquement, 10 anciens + 190 nouveaux.

### Le lot — 190 nuls frais, graines 9311–9500

Protocole gelé 27 nov. 2026 14h40 UTC, avant toute construction
et tout run du lot §8.101 (`PROTOCOL_8101_gse184585_200nulls.md`,
SHA `14e752c238fc4348222ac1f0c76b6a8b62c570927386846718dab5f998af22bf`).
190 nuls frais, construits avec le builder gelé
`build_null_893.py` (SHA `572b55bc…f467`, permutation de lignes
entières, colonne de contrôle `step` inchangée), à partir du même
CSV réel `pdac_899_gse184585_fluxes.csv` (SHA `07540af5…99d13`,
82 lignes × 13 colonnes). Split gelé par blocs entiers, aucune
graine recouvrante : local, blocs 0–9, graines 9311–9410 (100
runs) ; GitHub Actions, blocs 10–18, graines 9411–9500 (90 runs).
Disjonction vérifiée avant le gel (arithmétique exacte) :
9311–9500 ∩ 9301–9310 = vide ; ∩ 9111–9300 = vide ;
∩ 9101–9110 = vide ; ∩ 3000–3999 = vide ; ∩ {42} = vide.
Aucune graine 9311–9500 n'a servi dans un lot antérieur du
projet. Le nul graine 42 n'est PAS un nul de référence ici
(§8.99 §4) et ne compte ni dans les 10 ni dans les 200.

### Règle de verdict gelée (§8.93 §4)

Plancher 0,07. `maxsep` = score principal, lu dans
`master_results.json` →
`run_pipeline/threshold_metadata/threshold_optimization/best_config/metrics/max_separation`.
**SOLIDE** si réel > p95 des 200 nuls ET ≥ 95 % des nuls sous le
plancher (réel − nul > 0,07 pour ≥ 95 % des nuls, soit ≥ 190/200) ;
**FRAGILE** si réel > médiane mais ≤ p95, ou 50–95 % des nuls
sous le plancher ; **NON** si réel ≤ médiane ou < 50 % des nuls
sous le plancher. Rapportés : d contre médiane, d contre p95,
rang du réel sur 201, % de nuls sous le plancher, p95 et médiane
des nuls. Quantiles par interpolation linéaire (position
p×(n−1), n = 200) ; valeurs arrondies à 4 décimales.
Formulations d'analyse uniquement (« les données montrent »),
jamais de prédiction ; aucune affirmation clinique.

### Application de la correction de Zackary du 21 novembre 2026
(12h03, portée étendue à tout le projet à 12h04)

(1) Contrôle jamais analysé : les 200 nuls sont des permutations
des mêmes CSV (contrôle `step`, KRAS absent des flux) et le
pipeline exclut la colonne de contrôle des flux analysés par
construction (ligne 6787 de `universal_v6.2.0_cohen.py`). Règle
respectée. (2) Aucun seuil écarté pour non-monotonie. (3) Tous
les verdicts de cette section sont formulés comme de l'analyse
(ce que les données montrent) et non comme des prédictions.

## 8.101.2 — Le lot : exécution

**Piste locale (100 runs, graines 9311–9410).** Commande par run
identique au §8.99 : `python3 universal_v6.2.0_cohen.py --input
<csv nul> --mode fast --output
results_fast_v62_8101_gse184585_nul_s<graine>`. Lanceur
`run_lot_parallel2.sh` (tel quel, non modifié), 2 workers en
parallèle, fichier de tâches `tasks_8101.txt`, logs `logs_8101/`,
lancement par `systemd-run` (unité `v62-lot-8101`), hook de
surveillance `watch_8101.sh` (unité `v62-lot-8101-watch`, tour de
15 min, relance tant que les 100 `master_results.json` locaux ne
sont pas présents). Validation du lanceur parallèle avant le lot
(27 nov. 2026 14h48 UTC, protocole §2) : 2/2 runs parallèles
exit 0, SHA v6.2 inchangé ; `csd_consensus.json` et
`csd_fractal_estimators.csv` bit à bit identiques à la référence
séquentielle, maxsep identique (s9311 : 0,2217) ;
`master_results.json` diffère sur 8 feuilles seulement, toutes
hors calcul : `memory_cap` (5 vs 7) et `available_memory_bytes`
(métadonnées d'état machine au moment du run) + `dashboard_status/path`
et `telemetry_path` (nom du dossier de sortie, différent par
construction). Aucune valeur calculée ne diffère.

Déroulement (journal `watch_8101.log`, heures UTC) : 27 nov.
14h49 1/100, 15h04 5/100, 18h05 9/100, 18h20 17/100, 18h35
25/100, 18h50 33/100, 19h06 41/100, 19h21 49/100, 20h14 61/100,
20h49 73/100, 22h52 75/100, 28 nov. 10h56 79/100, 11h47 83/100,
12h03 91/100, 12h18 99/100, **12h33 TERMINÉE : 100/100
`master_results.json` ; SHA v6.2
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
vérifié** (marqueur `LOT_8101_DONE`, 28 nov. 2026 12h33:20Z,
soit 07h33:20 EST). Le lot local a duré ~22 h d'horloge, contre
~3 h attendues : la machine a redémarré plusieurs fois pendant
le lot (8 redémarrages comptés au 28 nov. 06h42), et le lot est
resté immobile une nuit entière (~18h00 le 27 nov. → 05h45 le
28 nov.) après un redémarrage probable vers 18h00 — probable,
pas prouvé : le journal système ne couvre que le boot courant,
et le watch était muet après son tour de 17h52 EST ; les deux
runs en cours (s9390, s9391, démarrés 17h59 EST) n'ont produit
aucune sortie (dossiers vides, pas même les plots de paysage).
**0 run perdu à aucun redémarrage** : le lanceur est reprenable
(saute tout run dont `master_results.json` existe) et le watch a
relancé le lot à chaque reprise. Deux ralentissements avant les
redémarrages, cause non établie et consignée telle quelle :
s9384/s9385 = 34 min (au lieu de ~4 min par paire), s9386/s9387
bloqués ~80 min (16h25–17h46) après la phase paysage (plots
écrits 16h26, rien ensuite), puis terminés en 4 min après
redémarrage à neuf — le redémarrage à neuf a suffi, ce qui
oriente vers une cause machine/transitoire plutôt que liée aux
données, sans preuve. Les 100 CSV nuls locaux sont dans
`nulls_8101_local_sha256.json` (SHA `aa869640…`, 100/100
construits, SHAs distincts ; s9311 `476dbede…`, s9312
`d3c23537…`).

**Piste GitHub (90 runs, graines 9411–9500).** Workflow
`pipeline-nulls-lot-899-consolidation.yml` (SHA
`5e4587b1202464f71218472f4fe53f894df0c2556196ae9f05548d014dae76e2`),
matrice `pair: [gse184585]` × `block: [10..18]` (9 jobs),
déclenchement manuel (`workflow_dispatch`), régénération des
nuls sur le coureur avec le builder gelé, vérification SHA de
v6.2 + CSV réel avant de tourner (contrôle `sha256sum -c -`
pour les deux), artefacts `nulls-8101-gse184585-s9411-s9420` …
`s9491-s9500` (un par job, `master_results.json.gz` seulement,
rétention 7 jours). Run nº 1, ID **46045446830**, déclenché
27 nov. 2026 ~12h56 EST : **9/9 jobs `completed success`**,
vérifié 13h41 EST via l'endpoint jobs. Artefacts téléchargés
13h42–13h43 EST (9/9 zips, ~84 Mo), décompressés dans
`results_fast_gha_8101_gse184585_nul_s<graine>/` — **90/90
`master_results.json` présents** ; contrôle ponctuel s9411 :
maxsep 0,1351 (nul plausible, sous le réel 0,3712).

**Extraction et agrégation.** Garde-fou : `extract_8101.py`
(SHA `5d623974c03117b8f8c082c27d4a745ca6fff2e33f1481cc46ea5f96636f3fdb`,
adapté de `extract_899.py`, SHA `939b90f6…9d0fe`) refuse
d'agréger un lot incomplet (exit 2) — il n'a été lancé qu'après
les 201 `master_results.json` (1 réel + 10 anciens + 100 locaux
+ 90 GitHub), vérifiés présents. Sortie : `extraction_8101.json`
(SHA `34f1b79ff2278e225166eac89ed5232328590e5e95cb457a5cbafd0b7f873002`,
15 857 o) + table imprimée + table CSV
`nulls_8101_gse184585_table.csv` (SHA
`c3dfc1f932bac6075883104f0313208fe98e34f77846234ba690dd6862bfe227`,
202 lignes : en-tête + réel + 200 nuls). Exactitude de
l'extraction : les valeurs du réel et des 10 anciens nuls sont
reprises de `extraction_899.json` à 0,0 exact (même chemin de
lecture, même script d'extraction adapté) ; les 190 nouveaux
nuls sont lus une fois, sans re-saisie. MC pipeline =
0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·sharpness
(formule réplique §8.93 ; facteur 0,8 non appliqué : w_size fast
80 ≥ n//10 = 8).

## 8.101.3 — Table complète — réel vs 200 nuls frais pipeline

Rang ascendant /201, réel inclus : rang 201 = réel au-dessus des
200 nuls ; rang 200 = 1 nul au-dessus du réel. Plancher gelé
0,07 : % des nuls dont l'écart réel−nul dépasse 0,07. d vs
médiane = maxsep réel − médiane des nuls. La table complète
(200 lignes) est `nulls_8101_gse184585_table.csv` ; la table
ci-dessous donne le résumé et les 12 nuls qui ne sont pas sous
le plancher.

| Mesure | 10 nuls (§8.99) | 200 nuls (§8.101) |
|---|---|---|
| `maxsep` réel | 0,3712 | **0,3712 (inchangé)** |
| Médiane des nuls | 0,2231 | **0,2257** |
| p95 des nuls | 0,2884 | **0,3014** |
| min–max nuls | 0,1777–0,2935 | **0,1351–0,3969** |
| % sous le plancher 0,07 | 100,0 % (10/10) | **94,0 % (188/200)** |
| d vs médiane | +0,1480 | **+0,1455** |
| d vs p95 | +0,0828 | **+0,0698** |
| Rang du réel | 11/11 | **200/201** |
| Nuls au-dessus du réel | 0/10 | **1/200** |
| **Verdict** | **SOLIDE** | **FRAGILE** |

Les 12 nuls dont l'écart réel−nul est ≤ 0,07 (triés par maxsep
décroissant) :

| Nul | Piste | maxsep | écart réel−nul |
|---|---|---|---|
| s9337 | locale | 0,3969 | **−0,0257 (au-dessus du réel)** |
| s9450 | GitHub | 0,3562 | +0,0150 |
| s9448 | GitHub | 0,3339 | +0,0373 |
| s9359 | locale | 0,3278 | +0,0434 |
| s9327 | locale | 0,3197 | +0,0515 |
| s9374 | locale | 0,3168 | +0,0543 |
| s9483 | GitHub | 0,3063 | +0,0649 |
| s9316 | locale | 0,3062 | +0,0650 |
| s9422 | GitHub | 0,3037 | +0,0675 |
| s9315 | locale | 0,3032 | +0,0680 |
| s9335 | locale | 0,3013 | +0,0699 |
| s9469 | GitHub | 0,3012 | +0,0700 (écart exact 0,0699942) |

Les 188 autres nuls sont tous à plus de 0,07 du réel. Les 12
nuls ci-dessus se répartissent 7 locaux / 5 GitHub : la queue
haute ne vient pas d'une seule piste. Le nul le plus haut des
10 anciens (s9308, 0,2935) n'est plus que le 17e de la
distribution à 200 : 16 nuls le dépassent.

## 8.101.4 — Lecture — verdict FRAGILE

La règle gelée §8.93 §4 est appliquée telle quelle, sans
ajustement. Branche 1 — réel > p95 des nuls : 0,3712 > 0,3014,
**passe** (écart +0,0698). Branche 2 — ≥ 95 % des nuls sous le
plancher : 188/200 = 94,0 %, **échoue** — il en fallait 190/200.
**Verdict : FRAGILE.** La définition gelée du FRAGILE couvre ce
cas par sa seconde disjonction (50–95 % des nuls sous le
plancher) : le réel est au-dessus du p95, mais la queue des
nuls mord le plancher.

Trois précisions de lecture, toutes mesurées :

1. **La marge est de deux nuls.** 188/200 contre 190/200 exigés.
   Deux nuls de la queue sont à moins de 0,0001 du plancher
   (s9335 : +0,0699 ; s9469 : +0,0699942, soit 0,0000058 sous
   le plancher). Un tirage différent de 200 nuls aurait pu
   donner 190/200 comme 186/200 — le verdict FRAGILE est
   mesuré contre cette distribution précise, pas contre une
   distribution idéale. Le §8.99.4 avait anticipé le mécanisme :
   un p95 au-dessus de 0,3012 ferait passer l'écart contre le
   p95 sous le plancher — le p95 à 200 nuls est 0,3014, et
   l'écart contre le p95 est +0,0698, soit 0,0002 sous le
   plancher. Cet écart n'est pas une branche de la règle gelée
   (la règle ne juge que réel > p95 et le % sous plancher) :
   il est rapporté comme mesure, pas comme cause du verdict.
   La cause du verdict est le % sous plancher, 94,0 %.
2. **Le réel n'a pas bougé.** 0,3712 au §8.99 comme ici, seuil
   72,50, mêmes composantes (s_norm 0,1835, stabilité 0,9905,
   robustesse 5,3×10⁻²⁷, sharpness 0,0152). Ce qui a changé,
   c'est la distribution mesurée : médiane 0,2231 → 0,2257
   (+0,0026), p95 0,2884 → 0,3014 (+0,0130), max des nuls
   0,2935 → 0,3969 (+0,1034, un nul au-dessus du réel). Le
   verdict à 10 nuls était fragile par construction — p95
   interpolé entre les deux plus hauts nuls, plus petit écart
   +0,0777, soit 0,0077 au-dessus du plancher (§8.99.4) — et la
   consolidation l'a confirmé fragile : elle n'a pas inventé
   la fragilité, elle l'a mesurée.
3. **FRAGILE n'est pas NON.** Le réel est au-dessus de 199
   nuls sur 200 (rang 200/201), au-dessus du p95, et son écart
   contre la médiane (+0,1455) est plus de deux fois le
   plancher. Parmi les cinq paires FRAGILES à 200 nuls, il se
   situe au milieu en d contre médiane : DepMap +0,1659 et
   GSE60979 +0,1576 sont au-dessus, GSE79668 +0,1293 et Yeh FF
   +0,1110 sont en dessous (§8.98.3). Ce qui la distingue des
   SOLIDES, c'est la queue : 12 nuls à moins de 0,07, contre 0
   à 10 nuls chez les six SOLIDES du §8.98.

## 8.101.5 — Tests directs en appui (ne décident pas)

Le réel est le même qu'au §8.99 (même CSV, SHA `07540af5…99d13`)
: les Spearman de chaque flux vs KRAS sont donc inchangés, repris
de `extraction_899.json` à 0,0 exact et re-vérifiés dans
`extraction_8101.json` (même mapping, même méthode `pandas`
Spearman) :

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

**Δρ médian −0,0098 ; flux positifs 6/12.** Les données montrent
la même dispersion des ordres directs qu'au §8.99 : CEACAM5 est
le flux le plus positivement ordonné avec KRAS (+0,550), CLCA1
le plus négativement (−0,531), devant KRT20 (−0,393) et GSTM1
(−0,304). La médiane est proche de zéro : `maxsep` sépare le
réel du nul sans gradient médian par flux — la séparation vient
d'une rupture multi-flux, pas d'un gradient monotone médian. Les
tests directs ne décident pas du verdict : ils décrivent l'ordre
par flux, rien de plus. La consolidation à 200 nuls ne change
rien à ce constat : il était déjà écrit au §8.99.5, il est
confirmé tel quel.

## 8.101.6 — Scores compagnons : `maxsep` passe le p95, les autres suivent en partie — dette §8.99.7 soldée

Les scores compagnons n'avaient pas été extraits au §8.99
(dette nommée nº 4, §8.99.7) : ils le sont ici, pour le réel,
dans `extraction_8101.json`. Ils sont rapportés pour analyse
seulement, jamais condition du verdict.

- **MC (secondaire, ne décide pas).** MC réel 0,3552
  (0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·sharpness).
  MC des 200 nuls : médiane 0,3337, p95 0,3494, min 0,3205,
  max 0,5032. Le MC réel est AU-DESSUS du p95 MC des nuls
  (+0,0058) — l'inverse du §8.99, où il était sous le p95 MC
  des 10 nuls (0,3722). La distribution MC des nuls porte 4
  valeurs aberrantes au-dessus de 0,40 (s9323 0,5032, s9402
  0,4013, s9412 0,4039, s9426 0,4520) ; sans elles, le p95 MC
  tomberait sous 0,345. Le MC est rapporté, il ne décide pas :
  au §8.93, TCGA v4, Immunitaire TCGA et PARP TCGA sont SOLIDES
  en `maxsep` avec un MC réel sous le p95 MC de leur réplique,
  et ici le MC réel dépasse le p95 MC sur une paire FRAGILE —
  le MC et `maxsep` divergent dans les deux sens selon les
  paires, ce qui est cohérent avec le constat du §8.35 (le MC
  ne sépare pas réel et nul sur les paires principales).
- **Delta (tension holographique).** Delta réel 1,2804.
  Falsification Δ vs nul : 0,2974, **non significative**
  (`is_significant_nonlinearity: false`). Delta ne distingue
  pas le réel du nul ici, comme sur la plupart des paires
  (§8.35 : Delta 6/8, échoue sur HP35, le témoin positif).
  Delta reste non élucidé (§8.103, 6e tentative) ; ce lot
  n'y touche pas.
- **L7a (cohérence).** Direction **down**, confiance globale
  0,1914 — confiance faible (TCGA v4, au §8.11 : down, conf
  0,408). La direction est la même que sur TCGA v4, la
  confiance est deux fois plus faible.
- **L7b (robustesse).** Verdict **FRAGILE**, mode **light**.
  Rapporté pour complétude : le verdict L7b est clos comme
  non informatif (13 nov. 2026 — un nul permuté retourne aussi
  FRAGILE, propriété de la construction du test, pas du
  système). Il ne pèse rien dans le verdict §8.101.4.
- **F1/F2 (dérivés vitesse/courbure avant et après seuil).**
  F1 vitesse max 0,6418 ; F2 courbure max 0,1415. Cascade T
  (cinq seuils, en % de l'axe) : T₋₂ 6,01 / T₋₁ 22,84 / T₀
  94,05 / T₊₁ 97,05 / T₊₂ 100,00. Le seuil optimisé du réel
  (72,50 sur `step` 0..81, soit 89,5 % de l'axe) et le T₀ de
  la cascade (94,05 %) se situent tous deux dans le dernier
  dixième de l'axe ordonné KRAS. Aucune interprétation
  temporelle : l'ordre KRAS est un axe d'analyse, pas un
  temps.
- **Seuil.** 72,50, inchangé depuis §8.99 (même réel, même
  pipeline, même extraction).

## 8.101.7 — Ce que cela change et ne change pas

**Ce que cela change.** Le verdict de GSE184585 passe de SOLIDE
(10 nuls, §8.99) à **FRAGILE** (200 nuls). Les lectures
comptables A2-distrib, à 200 nuls :

| Lecture (à 200 nuls) | SOLIDES | Dénominateur |
|---|---|---|
| Table §8.93 telle que publiée + GSE184585 (lecture du script d'agrégation) | 5 | 16 |
| Verdicts à 200 nuls (§8.98 + §8.101), paires PDAC seules | **5** | **16** |
| Verdicts à 200 nuls (§8.98 + §8.101), en comptant HP35 | **6** | **16** |

Les deux lectures à 200 nuls sont les suivantes. **Paires PDAC
seules : 5/16** — TCGA v4, Immunitaire TCGA, PARP TCGA,
GSE57495, ICGC ; GSE184585 est FRAGILE, elle n'ajoute pas de
SOLIDE. **En comptant HP35, le témoin positif biophysique,
SOLIDE à 200 nuls : 6/16.** La lecture du script d'agrégation
(5/16) reprend la table §8.93 telle que publiée, où ICGC est
encore FRAGILE : elle sous-compte l'état à 200 nuls d'un SOLIDE
(ICGC, devenu SOLIDE au §8.98). Les trois lectures sont
consignées ici pour qu'aucune ne soit lue seule ; le registre
A2/LOO lui-même appartient au coordinateur (§8.99.4) et n'est
pas mis à jour dans ce chantier.

**LOO (recalculé ici, convention §8.98.5 : retirer un SOLIDE).**
Sur 16 paires à 200 nuls, 6 SOLIDES : retirer un SOLIDE laisse
**5/15**. Paires PDAC seules (15 paires, 5 SOLIDES) : retirer un
SOLIDE laisse **4/14**. Convention rappelée : le LOO pire cas
est (solides − 1) / (total − 1) ; retirer un NON ou un FRAGILE
laisse 6/15. Le registre reste au
coordinateur.

**Ce qui ne change pas.** A2 classique : ce lot ne le touche
pas — le nul graine 42 de GSE184585 a déjà été couru au §8.99
(maxsep 0,1833, écart réel−s42 +0,1879 > 0,07, déjà compté dans
le 11/16 du §8.99) ; le registre appartient au coordinateur.
C3 reste levée (§8.71, GSE60979) — ce lot ne la re-teste pas,
il ne la touche pas. Les trois blocs de co-expression
(estomac/mucus, immunitaire, réparation ADN), l'effet PRMT5 qui
suit MTAP et non CDKN2A, et les résultats cliniques
(daraxonrasib, vopimetostat + daraxonrasib, IBI343) ne sont pas
touchés par ce lot. **Aucun remède** : ce lot juge la position
d'un réel dans sa distribution de nuls, il ne teste aucun
traitement et ne change rien à ce qui est un remède candidat.
Le §8.102 (GSE313117, FRAGILE à 10 nuls) et le §8.103 (Delta,
NON ÉLUCIDÉ) sont des chantiers séparés, publiés avec celui-ci ;
ils ne changent pas le verdict de cette section.

**Formulation.** Tous les verdicts de cette section sont des
verdicts d'analyse (ce que les données montrent), jamais des
prédictions — correction de Zackary du 21 novembre 2026, 12h03
(§8.101.1).

## 8.101.8 — Limites et dettes

- **FRAGILE de deux nuls.** 188/200 contre 190/200 exigés ;
  deux nuls de la queue à moins de 0,0001 du plancher (s9335,
  s9469). Le verdict décrit la position du réel dans cette
  distribution précise de 200 nuls, pas dans une distribution
  idéale. Un lot de 200 autres nuls donnerait un % voisin,
  pas identique — c'est la limite d'échantillonnage du p95 et
  du % à 200 tirages, nommée au §8.53 et au §8.98.7.
- **Un nul au-dessus du réel.** s9337 (0,3969, +0,0257
  au-dessus du réel) est le seul des 200 nuls à dépasser le
  réel. Le rang 200/201 dit que le réel est presque au sommet
  de sa distribution, pas au sommet.
- **MC : 4 valeurs aberrantes chez les nuls.** s9323 (0,5032),
  s9402 (0,4013), s9412 (0,4039), s9426 (0,4520) tirent le p95
  MC vers le haut ; le MC réel (0,3552) ne dépasse le p95 MC
  (0,3494) que de 0,0058. Le MC n'est pas le score de verdict,
  mais sa distribution sur cette paire est plus dispersée que
  celle de `maxsep`.
- **Nuls GitHub : CSV non détenus localement.** Les 90 nuls
  des graines 9411–9500 ont été construits sur le coureur
  GitHub avec le builder gelé (même graine → même fichier, le
  builder est déterministe) et leurs `master_results.json.gz`
  sont détenus localement (90/90) ; les CSV nuls eux-mêmes ne
  sont pas sur le disque local. Leur identité repose sur le
  builder gelé + la formule des graines + les vérifications SHA
  du workflow (v6.2, CSV réel, builder), pas sur une
  comparaison bit-à-bit locale — à la différence des 100 nuls
  locaux, dont les SHAs sont dans `nulls_8101_local_sha256.json`.
  Même limite qu'au §8.98 pour les 2 090 nuls GitHub.
- **Exécution lente et redémarrages.** Le lot local a duré
  ~22 h au lieu de ~3 h attendues (redémarrages machine, nuit
  immobile, ralentissements s9384–s9387 de cause non établie —
  §8.101.2). Aucun run perdu, aucune valeur affectée : le
  lanceur est reprenable et le SHA v6.2 est vérifié en fin de
  lot. La durée n'est pas une limite du verdict, elle est
  consignée comme fait d'exécution.
- **Le §8.99 reste publié tel quel.** Le verdict SOLIDE à 10
  nuls du §8.99 n'est pas réécrit : il était correct contre 10
  nuls, et il est dépassé par la consolidation à 200 nuls —
  c'est le sens d'une consolidation, pas une erreur du §8.99.
  Aucun addendum n'est ajouté au §8.99 ; cette section est la
  suite qui le corrige par les faits.
- **Dettes soldées par ce chantier.** Consolidation à 200 nuls
  (§8.99.7 dette nº 1) : faite. Scores compagnons Delta, L7a,
  falsification, F1/F2 (§8.99.7 dette nº 4) : extraits,
  §8.101.6. **Dettes restantes, nommées :** mise à jour du
  registre A2/LOO (coordinateur, §8.101.7) ; SOFT GEO GPL17586
  complet (abandonné, > 1,2 Go — remplacé par les bases
  Bioconductor, §8.99.1) ; étude aval Zhao et al. (BMC Genomics
  2023, 24:101) ayant fusionné GSE184585 à d'autres jeux : non
  lue pour ce chantier.
- **Les nuls sont des permutations par ligne** : ils brisent la
  structure ordonnée, pas les marginales — c'est le nul du
  projet depuis §8.31, pas un nul biologique.
- **Les verdicts SOLIDE / FRAGILE / NON décrivent la position
  du réel dans la distribution des nuls observée** ; ils ne
  prédisent rien sur un futur échantillon (correction du 21 nov.
  2026, §8.101.1).

## 8.101.9 — Provenance

- **Protocole gelé :** `PROTOCOL_8101_gse184585_200nulls.md`
  (SHA-256 `14e752c238fc4348222ac1f0c76b6a8b62c570927386846718dab5f998af22bf`,
  gelé 27 nov. 2026 14h40 UTC, avant toute construction et tout run).
- **Pipeline :** `universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (624 157 octets ; vérifié avant le lot, en fin de lot local —
  marqueur `LOT_8101_DONE`, 28 nov. 2026 12h33:20Z, V6_SHA_OK —
  et avant l'extraction ; inchangé ; fichier jamais modifié).
- **Source des données :** NCBI GEO, série GSE184585 (voir
  §8.99.8 et `PROVENANCE_899.md` pour la provenance complète
  de la matrice et du mapping). CSV réel
  `pdac_899_gse184585_fluxes.csv` (SHA
  `07540af57ef27974178036ea333f4ad51d9a19e49d7993f1d997b80fe6b99d13`,
  82 lignes × 13 colonnes).
- **Nuls :** `build_null_893.py` (SHA
  `572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467`),
  graines 9311–9500, permutation de lignes entières, contrôle
  inchangé. 100 CSV nuls locaux : SHAs dans
  `nulls_8101_local_sha256.json` (SHA `aa869640…`) ; 10 anciens
  nuls s9301–s9310 : SHAs dans `PROVENANCE_899.md` §5 ; 90 nuls
  GitHub : construits sur le coureur (voir limite §8.101.8).
- **Runs :** locaux, unité systemd `v62-lot-8101`, lanceur
  `run_lot_parallel2.sh`, 27 nov. 14h49 → 28 nov. 12h33 UTC,
  100/100 `master_results.json` ; GitHub, run **46045446830**
  (workflow `pipeline-nulls-lot-899-consolidation.yml`, SHA
  `5e4587b1202464f71218472f4fe53f894df0c2556196ae9f05548d014dae76e2`),
  9/9 jobs, 90/90 `master_results.json` récupérés. Réel :
  `results_fast_v62_899_gse184585` (§8.99, inchangé).
- **Extraction :** `extract_8101.py` (SHA
  `5d623974c03117b8f8c082c27d4a745ca6fff2e33f1481cc46ea5f96636f3fdb`),
  `extraction_8101.json` (SHA
  `34f1b79ff2278e225166eac89ed5232328590e5e95cb457a5cbafd0b7f873002`),
  `nulls_8101_gse184585_table.csv` (SHA
  `c3dfc1f932bac6075883104f0313208fe98e34f77846234ba690dd6862bfe227`).
- **Nature des lignes :** chaque ligne du CSV réel est une
  tumeur PDAC primaire (MSKCC, réséquée) ; chaque colonne de
  flux est une mesure instrumentale d'expression (microarray
  HTA 2.0, valeurs déposées) ; `step` est un rang humain
  (0..81, ordre KRAS ascendant), pas une mesure ; MUCL3 est la
  mesure du gène historiquement nommé DPCR1 (remappage vérifié
  5/5, §8.99.1). Aucune valeur n'est inventée, imputée ou mise
  à l'échelle.
- **Ce qui manque :** voir §8.101.8. Provenance complète :
  `PROVENANCE_8101.md`.
- **Ce qui n'a pas été fait :** aucune modification du livre
  blanc, aucun PDF, aucune Release, aucun push GitHub ;
  `tlogNext-pdac-phase2`, `universal-log-research` et Kaggle non
  touchés ; pipeline jamais modifié ; aucune affirmation
  clinique ; aucune formulation de prédiction (formulations
  d'analyse uniquement).
