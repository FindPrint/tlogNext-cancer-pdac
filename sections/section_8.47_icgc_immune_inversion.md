### 8.47 Inversion immunitaire ICGC — EXPLIQUÉE : le réel ne sépare pas, le nul est haut (19 nov. 2026)

**Verdict d'abord. L'inversion S_sep immunitaire ICGC (−0,2200) est
expliquée, et elle ne vient pas de la biologie.** Les tests directs
confirment le froid tumoral en ICGC comme dans les trois autres cohortes
(PDCD1 rho −0,22, top-12 d −0,85). L'inversion est une propriété de la
métrique max_separation, et elle tient en trois faits mesurés :
**(1) le réel ICGC ne sépare pas du tout** — maxsep 0,2299, et un nul
tiré au hasard le bat dans 61 % des cas (500 permutations) ; sa courbe
de scan reste dans l'intervalle interquartile nulle sur 13/13 candidats ;
avec un nul médian, d_ssep vaudrait −0,016, c'est-à-dire zéro.
**(2) Le nul graine 42 est haut** (0,4500, ~98e percentile à config
fixe), **mais pas exceptionnel pour le pipeline tel qu'il tourne** : un
nul frais sur trois atteint 0,4564 ; sur quatre tirages de nuls
pipeline, d_ssep ICGC vaut −0,220 / +0,052 / −0,011 / −0,221 — le signe
dépend du tirage du nul.
**(3) Le réel ICGC est bas parce que son signal est une falaise, pas un
gradient** : la chute immunitaire est concentrée dans les 12 tumeurs
KRAS-les-plus-fortes (moyenne des |d| top-12 = 0,408), et élargir le
groupe « haut » à 26 lignes — ce que font les fenêtres chevauchantes du
scan — divise ce signal par 1,9 (0,408 → 0,215 ; PDCD1 −0,85 → −0,26),
alors qu'en TCGA le gradient survit à l'élargissement (facteur 0,95).
Le petit n (70) relève en plus le plancher du nul (médiane 0,246 contre
0,170 à n=178). Les trois autres explications testées sont rejetées :
les flux substitués (H2), la composition en sous-types (H4) et la
corrélation inter-flux (H5). **Conséquence de méthode : à n≈70, S_sep
lu sur un seul nul est un tirage, pas une mesure — il faut la
distribution des nuls.**

#### 8.47.1 Faits de départ et décomposition

S_sep = max_separation × stabilité (PROTOCOL_v6.2.md §3), relu dans les
`master_results.json` v6.2 (§8.38, vérifié identique en v6.1 sur 29/29
paires). Décomposition (§8.38 relue le 19 nov.) :

| Paire | n | maxsep réel | maxsep nul | d_maxsep | stab R/N | S_sep R | S_sep N | d_S_sep |
|---|---|---|---|---|---|---|---|---|
| IMMUNE_TCGA | 178 | 0,5309 | 0,1634 | +0,3675 | 0,9914/0,9819 | 0,5263 | 0,1604 | +0,3659 |
| IMMUNE_GEO71729 | 145 | 0,2925 | 0,1563 | +0,1362 | 0,9916/0,9964 | 0,2900 | 0,1557 | +0,1343 |
| IMMUNE_GEO62452 | 69 | 0,4804 | 0,3154 | +0,1650 | 0,9692/0,9899 | 0,4656 | 0,3122 | +0,1534 |
| IMMUNE_ICGC | 70 | 0,2299 | 0,4500 | −0,2200 | 0,9955/0,9976 | 0,2289 | 0,4489 | −0,2200 |

La stabilité est saturée partout (0,97–1,00) : S_sep ≈ max_separation.
L'inversion vient entièrement de max_separation, et elle est à deux
côtés : le nul ICGC (0,4500) est le plus élevé des 8 maxsep
immunitaires, le réel ICGC (0,2299) le plus faible des 4 réels.
max_separation = maximum, sur les candidats, du score de scan =
moyenne sur les 12 flux de |d de Cohen| entre groupes pré/post-seuil
de fenêtres (code v6.2 lu : `_scan_critical_threshold_fast` +
`evaluate_scan_quality`). C'est une statistique de MAXIMUM : elle
favorise le nul qui « a de la chance » sur un candidat. Les courbes de
scan relues (`run_pipeline.scan_curve`) : réel ICGC plat (0,18–0,23 sur
toute la plage, max à 23,5 %) ; nul ICGC en plateau haut précoce (0,450
à 19,0 %, 0,445 à 23,8 % et 28,6 %, puis décroissance lisse) — pas un
pic isolé. Réel TCGA en rampe jusqu'à 0,53 à ~79 % ; réel GSE62452 en
rampe jusqu'à 0,48 à 81,8 % ; réel GSE71729 en U (max 0,29 à 12,2 %).

#### 8.47.2 La biologie n'est pas inversée (tests directs, §8.23 reproduits)

Mêmes définitions que `direct_tests_immune.py` (Spearman contre KRAS
brut ; top-12 KRAS-fort contre reste, d de Cohen + Welch), réel contre
nul graine 42, 4 cohortes, plus 200 permutations par gène focal
(`direct_tests_icgc_847.py`, SHA `db97d1da…`) :

| Gène (ICGC) | rho réel | p_perm (rho) | d top-12 réel | p_perm (d) |
|---|---|---|---|---|
| PDCD1 (PD-1) | −0,223 | 0,07 | −0,854 | 0,005 |
| CTLA4 | −0,243 | — | −0,740 | — |
| FOXP3 | −0,196 | — | −0,705 | — |
| CD8A | −0,146 | 0,21 | −0,452 | 0,12 |
| GZMB | −0,035 | 0,75 | −0,517 | 0,14 |
| PRF1 (remplace IFNG) | −0,039 | 0,74 | −0,470 | 0,19 |

Moyenne des |d| top-12, réel contre nul 42 : TCGA 0,376/0,117 ;
GSE71729 0,409/0,271 ; GSE62452 0,584/0,158 ; ICGC 0,408/0,222. Signes
rho négatifs (réel) : 10/12, 7/12, 9/12, 9/12. **Le réel ICGC est, en
test direct, aussi « froid » que GSE71729 (0,408 contre 0,409) et plus
froid que TCGA (0,376).** Les magnitudes de rho sont quasi identiques
entre cohortes (PDCD1 −0,22 à −0,25) ; seules les p-values diffèrent,
par la taille (n=70 contre 145/178) — une histoire de puissance, pas
de sens. L'inversion est donc une propriété de la métrique, pas du
signal biologique.

#### 8.47.3 Le réel ICGC ne sépare pas (réplique, 500 permutations)

Réplique exacte du scan (voir §8.47.8 pour la correction de méthode) :
500 permutations par ligne par cohorte, sous les deux configs fixes
(config réelle et config nulle de chaque run), plus la distribution de
référence. Résultats (`icgc_immune_inversion_replica.json`, SHA
`539f9527…`) :

| Cohorte | n | maxsep réel | médiane nulle | [p2,5 ; p97,5] | P(nul ≥ nul42) | P(nul ≥ réel) |
|---|---|---|---|---|---|---|
| TCGA | 178 | 0,5309 | 0,1700 | [0,089 ; 0,324] | 0,538 | **0,000** |
| GSE71729 | 145 | 0,2925 | 0,1757 | [0,111 ; 0,271] | 0,672 | **0,014** |
| GSE62452 | 69 | 0,4804 | 0,2426 | [0,159 ; 0,395] | 0,130 | **0,004** |
| ICGC | 70 | 0,2299 | 0,2458 | [0,157 ; 0,443] | 0,024 | **0,612** |

ICGC est la seule cohorte où le réel ne dépasse pas la distribution
nulle : un nul tiré au hasard bat le réel ICGC dans 61 % des cas,
contre 0 % (TCGA), 1,4 % (GSE71729) et 0,4 % (GSE62452). Avec un nul
médian, d_ssep vaudrait : TCGA +0,361 ; GSE71729 +0,117 ; GSE62452
+0,238 ; **ICGC −0,016** — c'est-à-dire zéro. Même avec un nul au
97,5e percentile, les trois autres cohortes restent positives
(+0,207 / +0,022 / +0,085) alors qu'ICGC tombe à −0,214. La courbe de
scan réelle ICGC reste dans l'intervalle interquartile nulle sur
**13/13 candidats** (grille config nulle) : à aucun seuil le réel ne
sort du bruit du nul. Le côté « réel bas » suffit à lui seul à
expliquer l'absence de séparation ; le nul haut ne fait
qu'approfondir l'écart de −0,02 à −0,22.

#### 8.47.4 Le nul graine 42 est haut, mais le pipeline en produit d'autres (lot v6.2, 11/11 exit 0)

Trois nuls ICGC frais (graines 1, 2, 3), deux GSE62452, deux TCGA,
runs v6.2 fast via systemd-run (unité `v62-847`, 21h49–22h58 UTC,
11/11 exit 0, SHA v6.2 re-vérifié `f07567c4…`) :

| Nul frais | maxsep | S_sep | MC | Dans [p2,5 ; p97,5] réplique ? |
|---|---|---|---|---|
| ICGC s1 | 0,1796 | 0,1769 | 0,5262 | oui |
| ICGC s2 | 0,2443 | 0,2396 | 0,3354 | oui |
| ICGC s3 | 0,4564 | 0,4497 | 0,3675 | non (+0,013 au-dessus de p97,5 = 0,4434) |
| GSE62452 s1 | 0,2826 | 0,2780 | 0,3405 | oui |
| GSE62452 s2 | 0,1869 | 0,1861 | 0,3280 | oui |
| TCGA s1 | 0,2479 | 0,2465 | 0,3377 | oui |
| TCGA s2 | 0,1414 | 0,1390 | 0,5144 | oui |

6/7 dans l'intervalle 95 % de la réplique ; le 7e (s3) ne le dépasse
que de 0,013 — l'optimiseur, libre de choisir sa config par run,
élargit légèrement la distribution des nuls au-delà de la réplique à
config fixe. Surtout : **un nul frais sur trois atteint 0,4564,
c'est-à-dire le niveau du nul graine 42 (0,4500)**. d_ssep ICGC sur
quatre tirages de nuls pipeline (réel S_sep 0,2289) : graine 42
−0,2200 ; s1 +0,0520 ; s2 −0,0107 ; s3 −0,2208. Le signe dépend du
tirage du nul ; l'inversion se reproduit avec une autre graine (s3).
Observation annexe (pas un critère du protocole) : le MC ne sépare
pas non plus sur ces tirages frais — nul s1 MC 0,5262 contre réel
0,3342 ; TCGA nul s2 MC 0,5144 contre réel 0,3785 — cohérent avec
§8.32/§8.35 (MC 1/8).

#### 8.47.5 Pourquoi le réel ICGC est bas : falaise contre gradient, dilution mesurée

Le signal immunitaire ICGC est une **falaise au sommet**, pas un
gradient. Moyenne des |d| de Cohen, top-K contre reste
(`extra_checks_icgc_847.py`, SHA `0767d8dd…`) :

| Cohorte | top-12 | top élargi | Facteur de dilution |
|---|---|---|---|
| TCGA (top-60) | 0,376 | 0,397 | 0,95 (aucune) |
| GSE71729 (top-40) | 0,409 | 0,262 | 1,56 |
| GSE62452 (top-26) | 0,584 | 0,375 | 1,56 |
| ICGC (top-26) | 0,408 | 0,215 | **1,90** |

En ICGC, PDCD1 passe de −0,85 (top-12) à −0,26 (top-26) et CD8A de
−0,45 à −0,17 ; en TCGA, PDCD1 passe de −0,61 à −0,69 — le signal y
est un gradient sur tout le tiers supérieur, qui survit à
l'élargissement. Or le scan construit ses groupes à partir de fenêtres
chevauchantes : à un seuil tardif (~80 %), le groupe « haut » contient
environ deux fois plus de lignes du milieu d'axe que de lignes du
sommet à n=70 (w_size=16). La falaise ICGC y est diluée par ~2 et le
score tardif tombe à ~0,20, alors que le gradient TCGA donne 0,53.
C'est visible dans les courbes : TCGA et GSE62452 montent en rampe
(0,10 → 0,53 ; 0,16 → 0,48), ICGC reste plate (0,18–0,23) sans rampe
tardive. Décomposition par flux au meilleur candidat du scan :
réel ICGC à 23,5 % — CD68 0,58 ; GZMB 0,43 ; PRF1 0,41 ; CD274 0,39 ;
CTLA4 0,25 ; CD163 0,21 ; CD8B 0,20 ; CD8A 0,10 ; CD4 0,06 ; FOXP3
0,05 ; PDCD1 0,05 ; MS4A1 0,05. Au seuil optimal du scan, les
marqueurs T (CD8A, CD4, FOXP3, PDCD1) ne contribuent presque rien ;
le score est porté par CD68/GZMB/PRF1/CD274. Le scan ne « voit » pas
la falaise T du sommet — le test direct, lui, la voit (top-12).

#### 8.47.6 Le petit n relève le plancher du nul (H3 retenue, avec réserve)

Médianes des maxsep nuls répliqués (500 tirages, config nulle) :
**ICGC 0,2458 (n=70) ≈ GSE62452 0,2426 (n=69) > GSE71729 0,1757
(n=145) > TCGA 0,1700 (n=178)** — gradient net avec la taille, et
courbe réelle ICGC dans la bande nulle (13/13, §8.47.3). H3 est
retenue. Réserve : le petit n seul ne suffit pas — GSE62452 (n=69)
sépare nettement (réel 0,4804, P(nul ≥ réel) = 0,004). Le petit n
relève le plancher du nul d'environ +0,07 ; il faut AUSSI un réel bas
(falaise diluée) pour inverser. À n≈70, un réel doit dépasser ~0,25
pour seulement égaler le nul médian.

#### 8.47.7 Hypothèses rejetées

- **H2 — Substitution de flux (IFNG→PRF1, CD19→MS4A1), REJETÉE.**
  Variante 10 gènes (sans IFNG/CD19, donc sans PRF1/MS4A1 en ICGC —
  mêmes 10 gènes partout), réplique ET pipeline : ICGC d_ssep 10g =
  −0,2085 (réplique, config réelle) et **−0,2085 (pipeline v6.2)**,
  contre −0,2200 à 12 gènes ; TCGA 10g = +0,3634 (réplique) et
  +0,3974 (pipeline), contre +0,3659. Retirer les deux colonnes
  substituées ne change presque rien (−0,22 → −0,21) et ne renverse
  pas le signe. Décomposition du score nul 42 à son meilleur candidat
  (19,0 %) : aucun flux substitué ne domine — PRF1 0,46, MS4A1 0,56,
  pour une moyenne de 0,45 ; max CTLA4 0,69, CD163 0,67. Les deux
  colonnes portent leur part ordinaire du score, pas l'inversion.
  (Runs 10g : ICGC réel maxsep 0,2337/S_sep 0,2324, MC 0,3355 ;
  ICGC nul42 0,4439/0,4409, MC 0,3657 ; TCGA réel 0,5091/0,5065,
  MC 0,3762 ; TCGA nul42 0,1107/0,1091, MC 0,5102.)
- **H4 — Composition / sous-type Bailey, REJETÉE.** Jointure NMF
  70/70 (`data/icgc_pacaau_nmf.txt.gz`) : Pancreatic Progenitor 19,
  Immunogenic 19, Squamous 18, ADEX 14. Les tumeurs Immunogenic ne se
  concentrent à aucune extrémité de l'axe KRAS (médiane step 34
  contre 36 pour les autres, Mann-Whitney p=0,79 ; tertiles
  équilibrés : 6/8/5). Aucune ligne à fardeau immunitaire extrême
  (moyenne des z-scores des 12 flux : max |z| = 1,62 ; 0 ligne
  au-dessus de 2,5, dans les 4 cohortes). Pas d'artefact de
  composition, pas de ligne dominante.
- **H5 — Corrélation inter-flux préservée par le nul, REJETÉE comme
  mécanisme principal.** Le nul du projet permute les lignes
  entières, donc la corrélation entre flux survit — mais briser ces
  corrélations (500 permutations indépendantes par flux) ne baisse la
  médiane nulle que de 0,0115 en ICGC (0,2458 → 0,2343), 0,0153 en
  GSE62452, 0,0169 en GSE71729, 0,0224 en TCGA — loin du critère
  (> 0,10). La corrélation inter-flux moyenne (Spearman) est
  pourtant la 2e plus haute en ICGC (0,378, contre 0,540 TCGA,
  0,252 GSE71729, 0,243 GSE62452) : elle existe, elle ne porte pas
  l'inversion.
- **H1 — Fluke du nul graine 42 : statut nuancé, pas « tirage
  ordinaire ».** À config fixe, P(maxsep nul ≥ 0,45) = 0,022–0,024
  (11–12/500) et médiane 0,246 < 0,30 : le critère de retenue
  (P ≥ 0,05 ET médiane ≥ 0,30) n'est pas tenu, et le critère de rejet
  (P < 0,01) non plus — le nul 42 est un tirage haut (top ~2 %),
  pas un tirage ordinaire ni un aberrant (max sur 500 tirages :
  0,59–0,62). Le lot pipeline tranche le sens : avec l'optimiseur
  libre de choisir sa config, un nul frais sur trois atteint 0,4564.
  Le nul 42 n'est donc pas un accident de graine : c'est un tirage
  haut ordinaire du pipeline tel qu'il tourne, et l'inversion ne
  dépend pas de lui seul (s3 donne −0,221 comme 42).

#### 8.47.8 Méthode

Protocole gelé avant tout run et toute analyse neuve :
`PROTOCOL_icgc_immune_inversion.md`, SHA
`b55283eeb7a24e30b52ee6a8f24de8a77b3c7b53072d8b837fab9eb08a61eb34`
(amendé §9, SHA
`f1a5a37c0b8ce452b4d00a9d2a649ac41384e076dcb80839389eac728988379c`).
Hypothèses H1–H5 et leurs critères écrits avant les analyses ; un nul
qui invalide une piste est un résultat ; aucune conclusion importée
d'autres expériences (MTAP, test C, rotations).
**(a) Vérification des entrées** (`verify_icgc_immune_847.py`, SHA
`a92b4906…`) : les 12 SHA des CSV de flux et d'axe re-vérifiés contre
PROVENANCE_immune_v6.md ; chaque nul est bien une permutation par
ligne du réel (même multi-ensemble de lignes, step inchangé) et le
nul graine 42 est reconstruit à l'identique
(`default_rng(42).permutation(n)`) ; 0 valeur manquante partout ;
KRAS brut ICGC min 5,162 / médiane 6,359 / max 7,352, écart
top-12–reste 0,680 (TCGA 1,032 ; GSE71729 0,677 ; GSE62452 0,842).
**(b) Tests directs** (§8.47.2). **(c) Réplique du scan** :
correction de méthode documentée — la première version ré-implémentait
le scan avec le step brut et échouait sa propre calibration (TCGA
réel 0,3229 contre 0,5309 pipeline). Lecture du code v6.2 : le scan
n'utilise pas le step brut mais l'axe MC `progress_pct`
(`_build_mc_progress_axis`, médiane de 200 trajectoires harmoniques,
graine 42, à partir du rang du contrôle ; `run_pipeline` l. 6817–6818).
La réplique corrigée utilise les fonctions du pipeline elles-mêmes
(import en lecture seule, aucune modification) :
`_build_mc_progress_axis` + `scan_critical_threshold` (appel identique
à celui du worker Monte-Carlo : n_candidates, resolution=None, w_size,
min_grp) + `evaluate_scan_quality`. **Calibration : 8/8 EXACTS**
(écart 0,00e+00 sur maxsep, stabilité, seuil et courbe complète).
L'axe progress_pct est presque linéaire (écart max 1,06–1,16 point)
et identique pour le réel et tous les nuls d'une même cohorte (il ne
dépend que du contrôle et de la graine). La réplique ne reproduit pas
l'optimiseur de configs (12 itérations, choix par score MC) : elle
fixe les configs — le lot (d) calibre cet écart. **(d) Lot de
confirmation** (§8.47.4) : 11 runs v6.2 fast, 11/11 exit 0.
Calibration réplique ↔ pipeline : 3/4 prédictions ponctuelles 10g
exactes (ICGC réel 0,2337, ICGC nul42 0,4439, TCGA réel 0,5091 —
l'optimiseur a choisi la config réelle dans ces trois cas) ; la 4e
(TCGA nul42) vaut 0,1107 contre 0,1434 prédit sous config réelle
(écart 0,033, dans la tolérance) et 0,1717 sous config nulle (écart
0,061) — l'optimiseur y a choisi une troisième config (w=84,
ncand=37) ; 6/7 nuls frais dans l'intervalle 95 % de la réplique. La
réplique est déclarée prédictive, avec cette réserve : l'optimiseur
élargit un peu la distribution des nuls au-delà de la réplique à
config fixe.

#### 8.47.9 Limites

- La réplique fixe les configs ; l'optimiseur en choisit une par run —
  la distribution des nuls du pipeline tel qu'il tourne est un peu
  plus large que celle de la réplique (1 nul frais sur 3 au-dessus de
  p97,5). Les probabilités citées (P = 0,022 ; 0,612) sont celles de la
  réplique à config fixe, pas du pipeline avec optimiseur.
- n=70 : 500 permutations décrivent la distribution du scan, pas une
  preuve biologique ; les p de permutation des tests directs reposent
  sur 200 tirages.
- ARN bulk sans correction de pureté (choix du bras §8.23) : la baisse
  des marqueurs T peut être un effet de composition ; ce chantier n'y
  touche pas.
- ICGC : IFNG et CD19 absents de la matrice — aucune donnée IFNG/CD19
  ICGC n'existe sur le disque pour un test direct de remplacement ;
  H2 est testée par retrait, pas par remplacement.
- Le mécanisme « falaise diluée » est mesuré sur les moyennes de |d|
  (top-12 contre top-26) ; il explique le score tardif bas, pas le
  choix du seuil optimal précoce (23,5 %) du réel ICGC.
- Ce chantier ne change rien au verdict biologique du §8.23 (froid
  tumoral, KRAS + anti-PD-(L)1 : NON) : il explique seulement pourquoi
  la métrique S_sep s'inverse en ICGC.

#### 8.47.10 Provenance

- Protocole : `PROTOCOL_icgc_immune_inversion.md`, SHA
  `b55283eeb7a24e30b52ee6a8f24de8a77b3c7b53072d8b837fab9eb08a61eb34`
  (amendé §9 : `f1a5a37c…79c`).
- Pipeline v6.2 :
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
  re-vérifié avant le lot (d), jamais modifié. Mode fast.
- Entrées (déjà sur disque, rien re-téléchargé) : flux immunitaires
  `pdac_immune_{tcga,geo71729,geo62452,icgc}_fluxes(_nul).csv` (SHA
  dans PROVENANCE_immune_v6.md, re-vérifiés) ; matrices sources :
  TCGA Firehose PAAD MD5 `b09569ce…`, GSE71729 SHA `b2287893…`,
  GSE62452 SHA `8f41d5b3…`, ICGC Xena SHA `c2cb57af…` (Bailey et al.,
  Nature 2016, doi:10.1038/nature16965) ; sous-types Bailey NMF
  `data/icgc_pacaau_nmf.txt.gz`, SHA `f1e84b99…` (PROVENANCE_icgc.md).
- Scripts (SHA-256) : `verify_icgc_immune_847.py` `a92b4906…`,
  `direct_tests_icgc_847.py` `db97d1da…`, `replica_scan_847.py`
  `84b030a3…`, `build_icgc_immune_847.py` `fd2ad098…`,
  `extract_icgc_immune_847.py` `c32a542d…`,
  `extra_checks_icgc_847.py` `0767d8dd…`,
  `run_icgc_immune_847.sh` `494bbada…`.
- Sorties : `icgc_immune_inversion_verify.json` (`5c552aec…`) /
  `.csv` (`2b2d0c4a…`), `icgc_immune_inversion_direct.csv`
  (`997598f2…`) / `.json` (`df4b0d27…`),
  `icgc_immune_inversion_replica.json` (`539f9527…`) / `.csv`
  (`de90b445…`), `icgc_immune_inversion_extra.json` (`a1fdea07…`),
  `icgc_immune_inversion_confirm_files.json` (`385ed81e…`),
  `icgc_immune_inversion_confirm.json` (`3139a817…`),
  `replica_847.log` (réplique, exit 0),
  `runs_icgc_immune_847.log` (lot v6.2, 11/11 exit 0, 21h49–22h58
  UTC, unité systemd `v62-847`), dossiers
  `results_fast_v62_847_*` (11 runs), fichiers de flux
  `pdac_immune_icgc_fluxes_nul_s{1,2,3}.csv`,
  `pdac_immune_{geo62452,tcga}_fluxes_nul_s{1,2}.csv` et
  `pdac_immune_{icgc,tcga}_fluxes_10g(_nul).csv` (SHA dans
  `icgc_immune_inversion_confirm_files.json`).
- Livre blanc : `livre-blanc-pdac-v6.md`, SHA `00f344b9…`, 3 104
  lignes, §8.1–§8.45 (cette section §8.47 est à fusionner par le
  coordinateur ; §8.46 appartient à un autre chantier).
