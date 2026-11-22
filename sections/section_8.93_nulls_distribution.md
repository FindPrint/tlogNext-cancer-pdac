### 8.93 Chaque paire jugée contre une distribution de nuls — RÉSULTATS COMPLETS (22 novembre 2026)

## 8.93.0 Correction de Zackary du 21 novembre 2026 — à lire avant la section

**Correction datée, nommée, de Zackary (21 novembre 2026, 12h03 ;
portée étendue à tout le projet le 12h04).** Elle s'applique aux quatre
pistes du lot (§8.93–§8.96) et, rétrospectivement, à tout le livre
blanc (§8.97). Trois points :

**(1) Un flux en axe de contrôle ne doit JAMAIS être un flux analysé.**
Le pipeline fait déjà cela — à vérifier et à écrire : c'est vrai pour
les rotations REFAITES sans doublon (§8.44), mais les 96 fichiers de
rotations d'origine (§8.32) avaient le défaut du doublon. Dans ce lot,
les deux sont dits plainement : où la règle est respectée, où elle ne
l'était pas. Pour chaque piste, l'exclusion du flux de contrôle est
vérifiée AVANT tout run (addenda datés aux quatre protocoles, 21
novembre 2026) ; pour les runs déjà lancés au moment de la correction
(LUAD, §8.96 bras A), la vérification a été faite immédiatement sur
les fichiers construits, sans relance à l'aveugle, et son résultat est
consigné. Mécanisme vérifié par lecture du code : le pipeline exclut
la colonne de contrôle des flux analysés quand aucun `flux_mapping`
n'est fourni (ligne 6787 de `universal_v6.2.0_cohen.py` :
`[c for c in ... if c != control_col]`).

**(2) Même un flux NON monotone en axe de contrôle peut donner un
seuil différent — et c'est de l'information, pas une erreur.** Ce flux
peut avoir des propriétés distinctes, il fait partie de l'information.
Ne pas écarter les contrôles non monotones, ne pas exiger la monotonie
comme condition, et lire leurs seuils comme des résultats d'analyse à
part entière. Cela nuance la règle ancienne « le contrôle doit être
monotone en T » : la monotonie aide à lire, elle n'est pas une
condition pour que le seuil compte. Dans ce lot : aucun seuil écarté
au motif de non-monotonie sans le dire et le justifier.

**(3) Le pipeline est AVANT TOUT un pipeline d'ANALYSE, pas forcément
de prédiction.** Tous les verdicts de ce lot sont formulés comme de
l'analyse (ce que les données montrent) et non comme des prédictions.
Si une formulation présente un résultat comme une prédiction, elle est
signalée et reformulée.

## 8.93.1 Question, méthode, règles

**Question.** Jusqu'ici chaque paire a été jugée contre UN seul nul
(graine 42) ou quelques nuls frais : un réel au-dessus du nul peut
être un tirage chanceux du nul, ou un nul malchanceux. Question posée :
chaque paire survit-elle à une DISTRIBUTION de nuls — 1000
permutations par ligne, plus 10 nuls frais pipeline par paire ?

**Méthode.** Protocole gelé `PROTOCOL_nulls_distribution_893.md` (SHA
d'origine `d2cdbc3d589d3be61a506f7be2a250d3d4a1c9adc21d1327c8ffc7a61f6529a0`,
écrit avant tout calcul ; addendum de la correction du 21 novembre
2026 ajouté ensuite, texte gelé intact). Deux voies, décision de
faisabilité gelée : 200 nuls pipeline × 15 paires = 3 000 runs ≈ 250 h
— INFAISABLE en lot unique. Voie gelée : (a) réplique 1000
permutations par ligne (précédent §8.47/§8.53, calibration à ±0,001
avant tout tirage, sinon arrêt) sous les DEUX configs fixes (config
réelle et config nulle du run v6.2 existant) — 30 000 tirages, graine
maîtresse `default_rng(20261121)`, nouvelle, distincte de §8.47 et
§8.53 ; (b) 10 nuls frais pipeline par paire, graines gelées 9101–
9110 (jamais utilisées) — étape 1 : 8 paires principales, 80 runs
≈ 7 h ; étape 2 : 7 paires A2 restantes, 70 runs ≈ 6 h. La réplique
reprend les fonctions DU PIPELINE en lecture seule
(`_build_mc_progress_axis`, `scan_critical_threshold`,
`evaluate_scan_quality`) ; MC par tirage = 0,3·s_norm + 0,3·stabilité
+ 0,2·robustesse + 0,2·sharpness, pénalité ×0,8 si w < n//10 (code
v6.2 lignes 3480–3484 et 3727–3731) ; S_sep = maxsep × stabilité.

**Les 15 paires (table §8.88.3 reprise telle quelle ; A2 actuel 10/15,
12/15 positifs, LOO 9/14).** HP35 (d_maxsep +1,6512), TCGA v4
(+0,2928), GSE71729 (+0,0402), GSE62452 (−0,0036), ICGC (+0,0970),
Immunitaire TCGA (+0,3675), PARP TCGA (+0,1688), DepMap (+0,1904),
GSE21501 (−0,0100), GSE79668 (+0,0567), GSE60979 (+0,2045), GSE131050
Yeh FF (+0,0739), GSE57495 (+0,4494, 11 flux), GDC ORGANOID (+0,0884,
12 flux, MUCL3 ex-DPCR1), GSE194249 (−0,0239, 11 flux, DPCR1 absent).
Toutes ont le contrôle `step` ; n de 42 à 1000.

**Verdicts par paire gelés.** SOLIDE si réel > p95 des nuls ET ≥ 950/
1000 nuls sous le plancher (écart > 0,07 contre ≥ 95 % des nuls) ;
FRAGILE si réel > médiane mais ≤ p95, ou 50–95 % sous le plancher ;
NON si réel ≤ médiane ou < 50 % sous le plancher. A2 recalculé contre
les distributions (A2-distrib) — il coexiste avec A2 classique, il ne
le réécrit pas.

**Application de la correction du 21 novembre 2026 à cette piste.**
(1) Contrôle jamais analysé : vérifié avant les runs — les 15 CSV ont
le contrôle `step`, KRAS absent des flux ; les 150 nuls frais sont des
permutations des mêmes CSV ; la réplique exclut la colonne de contrôle
par construction. Règle respectée. (2) Aucun seuil écarté pour
non-monotonie. (3) Verdicts formulés comme de l'analyse : la position
du réel dans la distribution des nuls décrit ce que les données
montrent, elle ne prédit rien.

## 8.93.2 Résultats — COMPLETS (22 novembre 2026)

**Verdict global.** Sur les 15 paires jugées contre une distribution de
nuls (1000 permutations par ligne sous config réelle, plus 10 nuls frais
pipeline par paire), les données montrent : **5 paires SOLIDES, 5
FRAGILES, 5 NON** — A2-distrib **5/15** (12/15 positifs, LOO 4/14),
contre A2 classique 10/15 (12/15 positifs, LOO 9/14). Le compte
classique ne change pas ; c'est la lecture contre une distribution qui
est deux fois plus sévère. Aucune paire n'est sans résultat exploitable :
les 15 paires ont une réplique complète (1000 tirages × 2 configs) et
10 nuls frais pipeline chacune.

## 8.93.2.1 Calibration et exécution

- **Calibration (§3a).** 30/30 runs existants reproduits par la réplique
  à **0,00e+00** sur maxsep et sur MC, courbes identiques (écart max
  courbe 0,0) — `nulls_dist_893_verify.json`. La machinerie de réplique
  est donc la même mesure que le pipeline, à l'identique, avant tout
  tirage.
- **Réplique.** **30 000 tirages** (15 paires × 2 configs × 1000
  permutations par ligne, graines 3000–3999, graine maîtresse
  `default_rng(20261121)`), valeurs brutes intégrales conservées
  (`nulls_dist_893_replica_raw.csv`, 30 001 lignes avec en-tête ; 1000
  tirages par (paire, config), vérifié). Étape 3 de la file, exit 0,
  22 nov. 2026 12h33 UTC (`queue_893_896.log`).
- **Nuls frais pipeline.** **150/150 runs, exit 0, 0 échec** — étape 1 :
  80 runs (8 paires principales), 80 libellés distincts EXIT:0, fin
  22 nov. 13h16 UTC ; étape 2 : 70 runs (7 paires A2 restantes),
  70 libellés distincts EXIT:0, fin 22 nov. 15h35 UTC
  (`runs_nulls_893_e1.log`, `runs_nulls_893_e2.log`). v6.2 SHA vérifié
  avant chaque lot et à la fin des deux lots : `f07567c4…` inchangé.
  Marqueur `QUEUE_893_896_DONE` présent.
- **Ce qui n'a PAS été atteint.** Les ~200 nuls pipeline par paire de
  la proposition initiale : le protocole gelé l'avait déclaré
  INFAISABLE en lot unique (3 000 runs ≈ 250 h) et avait gelé la voie
  réplique + 10 nuls frais en validation. Ce qui a été atteint
  réellement : 1000 nuls réplique par paire et par config (soit
  2000 tirages par paire) + 10 nuls frais pipeline par paire. Les
  10 nuls frais valident la réplique, ils ne la remplacent pas
  (protocole §7).

## 8.93.2.2 Table des 15 paires — réplique, config réelle

Rang ascendant /1001, réel inclus : rang 1001 = réel au-dessus des
1000 nuls ; rang 573 = 428 nuls au-dessus du réel. Plancher gelé 0,07 :
% des nuls dont l'écart réel−nul dépasse 0,07. d_maxsep = écart contre
UN seul nul (graine 42), table §8.88.3 reprise telle quelle.

| Paire | n | flux | maxsep réel | rang /1001 | p95 nuls | médiane nuls | % nuls sous plancher | nuls réplique au-dessus du réel | d_maxsep (1 nul) |
|---|---|---|---|---|---|---|---|---|---|
| HP35 | 1000 | 7 | 1,7718 | 1001 | 0,2097 | 0,1342 | 100,0 % | 0 | +1,6512 |
| TCGA v4 | 178 | 12 | 0,4623 | 1001 | 0,2644 | 0,1826 | 100,0 % | 0 | +0,2928 |
| GSE71729 | 145 | 12 | 0,2593 | 913 | 0,2747 | 0,1935 | 46,1 % | 88 | +0,0402 |
| GSE62452 | 69 | 12 | 0,3100 | 883 | 0,3378 | 0,2447 | 45,4 % | 118 | −0,0036 |
| ICGC | 70 | 12 | 0,4080 | 991 | 0,3489 | 0,2440 | 93,3 % | 10 | +0,0970 |
| Immunitaire TCGA | 178 | 12 | 0,5309 | 1001 | 0,3444 | 0,2068 | 99,6 % | 0 | +0,3675 |
| PARP TCGA | 178 | 12 | 0,3680 | 1001 | 0,2773 | 0,1866 | 97,5 % | 0 | +0,1688 |
| DepMap | 45 | 12 | 0,4436 | 983 | 0,3977 | 0,2950 | 90,5 % | 18 | +0,1904 |
| GSE21501 | 132 | 12 | 0,2121 | 620 | 0,2789 | 0,2000 | 2,7 % | 381 | −0,0100 |
| GSE79668 | 51 | 12 | 0,4104 | 999 | 0,3535 | 0,2801 | 90,8 % | 2 | +0,0567 |
| GSE60979 | 49 | 12 | 0,4418 | 977 | 0,4143 | 0,2869 | 88,3 % | 24 | +0,2045 |
| GSE131050 Yeh FF | 42 | 12 | 0,3220 | 991 | 0,2891 | 0,2047 | 84,0 % | 10 | +0,0739 |
| GSE57495 | 63 | 11 | 0,6381 | 1000 | 0,4292 | 0,2565 | 99,5 % | 1 | +0,4494 |
| GDC ORGANOID | 44 | 12 | 0,2542 | 884 | 0,2767 | 0,2022 | 32,4 % | 117 | +0,0884 |
| GSE194249 | 84 | 11 | 0,2306 | 573 | 0,2793 | 0,2248 | 0,8 % | 428 | −0,0239 |

## 8.93.2.3 Lecture par paire — batterie entière

Règle gelée (§4) : SOLIDE si réel > p95 des nuls ET ≥ 95 % des nuls
sous le plancher ; FRAGILE si réel > médiane mais ≤ p95, ou 50–95 %
sous le plancher ; NON si réel ≤ médiane ou < 50 % sous le plancher.
`maxsep` est le score principal AFFICHÉ ; le verdict utilise la
batterie entière (§8.90.1.2), rapportée ci-dessous par paire depuis
les runs existants (MC, Delta, L7a, falsification, F1/F2 après seuil).

**SOLIDES (5/15).** HP35 (réel 1,7718, rang 1001, 100,0 % sous le
plancher) ; TCGA v4 (0,4623, rang 1001, 100,0 %) ; Immunitaire TCGA
(0,5309, rang 1001, 99,6 %) ; PARP TCGA (0,3680, rang 1001, 97,5 %) ;
GSE57495 (0,6381, rang 1000 — 1 seul nul réplique au-dessus du réel —
99,5 %).

**FRAGILES (5/15).** ICGC (réel 0,4080 > p95 0,3489, mais 93,3 % sous
le plancher < 95 %) ; DepMap (0,4436 > p95 0,3977, 90,5 %) ; GSE79668
(0,4104 > p95 0,3535, 90,8 %) ; GSE60979 (0,4418 > p95 0,4143, 88,3 %) ;
GSE131050 Yeh FF (0,3220 > p95 0,2891, 84,0 %). Dans les cinq cas le
réel est au-dessus du p95 des nuls, mais la queue des nuls mord le
plancher : moins de 95 % des nuls sont sous l'écart 0,07.

**NON (5/15).** GSE71729 (réel 0,2593 < p95 0,2747, 46,1 % sous le
plancher, 88 nuls au-dessus du réel) ; GSE62452 (0,3100 < p95 0,3378,
45,4 %, 118 nuls au-dessus) ; GSE21501 (0,2121, rang 620, 2,7 %,
381 nuls au-dessus) ; GDC ORGANOID (0,2542 < p95 0,2767, 32,4 %,
117 nuls au-dessus) ; GSE194249 (0,2306, rang 573, 0,8 %, 428 nuls
au-dessus — le réel est au milieu de sa distribution de nuls).

Batterie des réels (runs existants, extraction `extract_858.extract`,
même méthode que les lots précédents) :

| Paire | MC réel | p95 MC réplique | MC réel > p95 MC ? | Delta | L7a (dir, conf) | falsification (statut) | F1 / F2 après seuil |
|---|---|---|---|---|---|---|---|
| HP35 | 0,6035 | 0,4248 | oui | 4,483 | up 0,3779 | 1,2656 (ok) | 0,013 / 0,001 |
| TCGA v4 | 0,3720 | 0,4273 | non | 4,181 | down 0,4052 | 0,8494 (ok) | 0,031 / 0,009 |
| GSE71729 | 0,3393 | 0,3521 | non | 2,159 | up 0,4154 | 0,6013 (ok) | 0,057 / 0,043 |
| GSE62452 | 0,3454 | 0,3536 | non | 1,412 | down 0,1974 | 0,1988 (ok) | 0,025 / 0,020 |
| ICGC | 0,3600 | 0,3582 | oui | 1,444 | up 0,1811 | 0,2379 (ok) | 9,481 / 10,630 |
| Immunitaire TCGA | 0,3785 | 0,5259 | non | 4,210 | down 0,1835 | 0,9851 (ok) | 11,469 / 18,706 |
| PARP TCGA | 0,3555 | 0,4517 | non | 4,299 | up 0,1726 | 0,8671 (ok) | 0,391 / 0,343 |
| DepMap | 0,3615 | 0,3574 | oui | 1,934 | down 0,1959 | indisponible (n=45 < 75) | 1,030 / 1,503 |
| GSE21501 | 0,3337 | 0,3896 | non | 2,813 | up 0,1622 | 0,2583 (ok) | 41,845 / 46,206 |
| GSE79668 | 0,3566 | 0,3511 | oui | 0,635 | up 0,3459 | 1,4058 (ok) | 9,717 / 22,575 |
| GSE60979 | 0,3606 | 0,3605 | oui (à 0,0001 près) | 1,871 | up 0,1388 | 0,1746 (ok) | 9,914 / 19,524 |
| GSE131050 Yeh FF | 0,3985 | 0,3939 | oui | 1,470 | up 0,3352 | 1,3021 (ok) | 0,477 / 0,525 |
| GSE57495 | 0,3920 | 0,3775 | oui | 1,403 | up 0,3386 | 0,4476 (ok) | 0,121 / 0,083 |
| GDC ORGANOID | 0,3880 | 0,3918 | non | 1,468 | up 0,3372 | 1,5177 (ok) | 0,322 / 0,585 |
| GSE194249 | 0,3350 | 0,3425 | non | 0,991 | up 0,3521 | 1,0904 (ok) | 3,772 / 8,774 |

Trois lectures de la batterie :

- **MC jamais seul (§8.90.1.2).** Sur les 15 paires, le MC réel ne
  dépasse le p95 MC de sa réplique que pour 7 paires (HP35, ICGC,
  DepMap, GSE79668, GSE60979, Yeh FF, GSE57495). TCGA v4, Immunitaire
  TCGA et PARP TCGA sont SOLIDES en maxsep avec un MC réel SOUS le
  p95 MC de leur réplique (0,3720 contre 0,4273 ; 0,3785 contre
  0,5259 ; 0,3555 contre 0,4517). À l'inverse, GSE60979 a un MC réel
  au-dessus du p95 MC (0,3606 contre 0,3605, à 0,0001 près) sans
  être SOLIDE. Le MC est rapporté, il ne décide pas.
- **L7b.** FRAGILE sur les 15 réels — audit clos : L7b dit FRAGILE
  sur le réel comme sur un nul permuté, propriété de la construction
  du contrôle, pas mesure de fragilité de l'instrument ; il n'entre
  dans aucun verdict ici.
- **Falsification et dérivés.** Statut « ok » pour les 14 paires où
  la falsification est disponible ; indisponible pour DepMap
  (n=45 < 75). Les dérivés F1/F2 après seuil sont forts (> 1) pour
  ICGC (9,481 / 10,630), Immunitaire TCGA (11,469 / 18,706),
  GSE21501 (41,845 / 46,206), GSE79668 (9,717 / 22,575), GSE60979
  (9,914 / 19,524) et GSE194249 (3,772 / 8,774), faibles (< 1) pour
  HP35, TCGA v4, GSE71729, GSE62452, PARP TCGA, Yeh FF, GSE57495 et
  GDC ORGANOID, voisins de 1 pour DepMap (1,030 / 1,503) : la
  dérivée après seuil ne sépare pas les SOLIDES des NON, elle est
  rapportée comme élément de la batterie, pas comme critère.

## 8.93.2.4 Nuls frais pipeline — validation de la réplique

10 nuls frais par paire, graines 9101–9110, runs v6.2 fast, exit 0.
Extraction par `extract_858.extract` (même méthode que les lots
précédents) — `nulls_dist_893_fresh.json`.

| Paire | frais médiane | frais p95 | frais min–max | frais au-dessus du réel (/10) | frais sous plancher (/10) | p95 frais dans [p2,5 ; p97,5] réplique ? |
|---|---|---|---|---|---|---|
| HP35 | 0,0924 | 0,1672 | 0,0747–0,1722 | 0 | 10 | oui [0,0848 ; 0,2311] |
| TCGA v4 | 0,1857 | 0,2278 | 0,1346–0,2466 | 0 | 10 | oui [0,1262 ; 0,2841] |
| GSE71729 | 0,1992 | 0,2211 | 0,1663–0,2249 | 0 | 4 | oui [0,1379 ; 0,2944] |
| GSE62452 | 0,2219 | 0,3203 | 0,1509–0,3259 | 2 | 6 | oui [0,1704 ; 0,3656] |
| ICGC | 0,2552 | 0,3270 | 0,1939–0,3370 | 0 | 10 | oui [0,1634 ; 0,3764] |
| Immunitaire TCGA | 0,1719 | 0,2301 | 0,0572–0,2594 | 0 | 10 | oui [0,1158 ; 0,3792] |
| PARP TCGA | 0,1858 | 0,2161 | 0,1036–0,2173 | 0 | 10 | oui [0,1247 ; 0,2960] |
| DepMap | 0,3108 | 0,4288 | 0,1327–0,4391 | 0 | 7 | **non** [0,2073 ; 0,4272] — hors de 0,0016 |
| GSE21501 | 0,2000 | 0,2787 | 0,1772–0,3137 | 3 | 0 | oui [0,1403 ; 0,2999] |
| GSE79668 | 0,2690 | 0,3138 | 0,2316–0,3185 | 0 | 10 | oui [0,2068 ; 0,3704] |
| GSE60979 | 0,2493 | 0,3622 | 0,1563–0,3760 | 0 | 9 | oui [0,1881 ; 0,4387] |
| GSE131050 Yeh FF | 0,2004 | 0,2537 | 0,1554–0,2899 | 0 | 9 | oui [0,1325 ; 0,3080] |
| GSE57495 | 0,2612 | 0,4115 | 0,2046–0,4864 | 0 | 10 | oui [0,1595 ; 0,4687] |
| GDC ORGANOID | 0,2031 | 0,2338 | 0,1524–0,2412 | 0 | 3 | oui [0,1259 ; 0,2916] |
| GSE194249 | 0,2063 | 0,2423 | 0,1767–0,2584 | 1 | 0 | oui [0,1717 ; 0,2908] |

- **Question subsidiaire (§3b).** Le p95 des 10 nuls frais tombe
  dans l'intervalle [p2,5 ; p97,5] de la réplique pour **14/15
  paires**. Seule exception : DepMap, p95 frais 0,4288 contre
  p97,5 réplique 0,4272 — hors intervalle de 0,0016, consigné, pas
  corrigé, sans effet sur le verdict (DepMap FRAGILE dans les deux
  lectures).
- **Aucun nul frais ne renverse la lecture de la réplique.** Les
  nombres de nuls frais au-dessus du réel (GSE62452 2/10, GSE21501
  3/10, GSE194249 1/10, 0/10 ailleurs) sont compatibles avec les
  proportions de la réplique (11,8 %, 38,1 %, 42,8 %) pour un
  échantillon de 10 ; GSE71729 0/10 frais au-dessus du réel contre
  8,8 % en réplique est compatible aussi (probabilité d'observer
  0/10 à 8,8 % : 0,40). Les % sous plancher des frais suivent ceux
  de la réplique (HP35 10/10 contre 100,0 % ; TCGA 10/10 contre
  100,0 % ; GSE71729 4/10 contre 46,1 % ; GSE62452 6/10 contre
  45,4 % ; ICGC 10/10 contre 93,3 % ; DepMap 7/10 contre 90,5 % ;
  GSE79668 10/10 contre 90,8 % ; GSE60979 9/10 contre 88,3 % ;
  Yeh FF 9/10 contre 84,0 % ; GSE57495 10/10 contre 99,5 % ; GDC
  3/10 contre 32,4 % ; GSE21501 0/10 contre 2,7 % ; GSE194249 0/10
  contre 0,8 %).
- **L7a des nuls frais** (rapportée, non décisive) : les 10 nuls
  frais sont tous « up » pour GSE79668, Yeh FF et GDC ORGANOID ;
  partagés ailleurs (p. ex. DepMap 5 up / 5 down, GSE60979 5 up /
  5 down, PARP TCGA 7 up / 2 down / 1 flat). Un nul frais peut donc
  voter « up » comme le réel : la direction L7a seule ne sépare
  pas le réel du nul.

## 8.93.2.5 A2 recalculé contre les distributions

- **A2-distrib : 5/15 SOLIDES** (HP35, TCGA v4, Immunitaire TCGA,
  PARP TCGA, GSE57495) ; **positifs 12/15** (inchangé : d_maxsep
  > 0 pour les mêmes 12 paires que le classique) ; **LOO 4/14**
  (convention du script : solides − 1 sur 14, même convention que
  le LOO classique 9/14).
- **Ce qui bouge par rapport à A2 classique (10/15).** Cinq paires
  passent de passantes à non-SOLIDES : ICGC, DepMap, GSE60979 et
  Yeh FF (passantes classiques, devenues FRAGILES : réel au-dessus
  du p95 des nuls mais moins de 95 % des nuls sous le plancher) et
  GDC ORGANOID (passante classique à +0,0884, devenue NON : réel
  sous le p95, 32,4 % sous le plancher). GSE79668, déjà non passante
  en classique (+0,0567 < 0,07), est lue FRAGILE ici (réel
  au-dessus du p95, 90,8 % sous le plancher) — la distribution
  affine la lecture sans la renverser.
- **Les deux comptes coexistent.** A2 classique 10/15 n'est pas
  réécrit ; A2-distrib 5/15 est la lecture contre une distribution
  de nuls. Le verdict par paire décrit la position du réel dans la
  distribution des nuls observée ; il ne prédit rien sur un futur
  échantillon (correction du 21 nov. 2026, §8.93.0).

## 8.93.2.6 Sensibilités (rapportées, non décisives)

- **(a) Config nulle au lieu de config réelle.** Verdicts
  inchangés : les mêmes 5 paires sont SOLIDES sous config nulle
  (p95 nulle / % sous le plancher : HP35 0,2192 / 100,0 % ;
  TCGA v4 0,2649 / 99,9 % ; Immunitaire TCGA 0,2936 / 99,3 % ;
  PARP TCGA 0,2666 / 97,8 % ; GSE57495 0,4230 / 99,7 %) ;
  DepMap reste FRAGILE (94,6 % sous config nulle) ; ICGC 91,4 %,
  GSE79668 85,6 %, GSE60979 89,1 %, Yeh FF 81,0 % sous config
  nulle ; GSE71729 42,6 %, GSE62452 23,7 %, GSE21501 0,0 %,
  GDC 32,8 %, GSE194249 0,6 %.
- **(b) Plancher 0,05 et 0,10 au lieu de 0,07 (config réelle).**
  À 0,05, 7 paires seraient SOLIDES (s'ajoutent ICGC 96,4 % et
  GSE79668 96,0 % sous le plancher) ; à 0,10, 4 paires (PARP tombe
  à 93,7 % < 95 %, ICGC à 85,7 %). Le compte SOLIDE bouge 7 → 5 →
  4 quand le plancher bouge 0,05 → 0,07 → 0,10 — le plancher 0,07
  reste le plancher gelé, les deux autres sont des sensibilités.
  (% sous plancher à 0,05 : HP35 100,0 ; TCGA 100,0 ; GSE71729
  65,2 ; GSE62452 61,8 ; ICGC 96,4 ; Immunitaire 99,7 ; PARP 98,9 ;
  DepMap 94,2 ; GSE21501 12,0 ; GSE79668 96,0 ; GSE60979 92,2 ;
  Yeh FF 91,2 ; GSE57495 99,7 ; GDC 52,2 ; GSE194249 7,0. À 0,10 :
  HP35 100,0 ; TCGA 99,8 ; GSE71729 13,5 ; GSE62452 21,8 ; ICGC
  85,7 ; Immunitaire 99,3 ; PARP 93,7 ; DepMap 79,7 ; GSE21501 0,1 ;
  GSE79668 76,1 ; GSE60979 78,9 ; Yeh FF 64,3 ; GSE57495 99,1 ;
  GDC 10,8 ; GSE194249 0,0.)
- **(c) S_sep au lieu de maxsep (même règle SOLIDE appliquée à
  S_sep).** Mêmes 5 SOLIDES (HP35, TCGA v4, Immunitaire TCGA,
  PARP TCGA, GSE57495 — S_sep réel au-dessus du p95 S_sep et
  ≥ 95 % des nuls sous le plancher pour ces 5 paires ; rangs
  S_sep 1001/1001 pour les cinq) ; les 10 autres restent FRAGILES
  ou NON (rangs S_sep : ICGC 991, DepMap 984, GSE79668 998,
  GSE60979 978, Yeh FF 991, GSE71729 935, GSE62452 873, GSE21501
  611, GDC 878, GSE194249 577). La lecture ne dépend pas du choix
  maxsep / S_sep pour le compte SOLIDE.

## 8.93.2.7 Limites

- La réplique est à config fixe ; l'optimiseur libre (qui choisit
  sa config par run) élargit légèrement la distribution des nuls
  (§8.53) — l'écart réplique vs nuls frais pipeline est mesuré ici
  (§8.93.2.4), pas supposé nul : p95 frais dans l'intervalle
  réplique pour 14/15 paires, DepMap hors de 0,0016.
- Les nuls sont des permutations par ligne : ils brisent la
  structure temporelle/ordonnée, pas les marginales — c'est le nul
  du projet depuis §8.31, pas un nul biologique.
- 10 nuls frais par paire ne font pas une distribution à 200 : ils
  valident la réplique, ils ne la remplacent pas. Les ~200 nuls
  pipeline par paire de la proposition initiale n'ont pas été
  atteints (INFAISABLE, 3 000 runs ≈ 250 h, tranché avant le gel) ;
  ce qui a été atteint : 1000 nuls réplique par paire et par config
  + 10 nuls frais pipeline par paire.
- Les verdicts SOLIDE / FRAGILE / NON décrivent la position du réel
  dans la distribution des nuls observée ; ils ne prédisent rien
  sur un futur échantillon (correction du 21 nov. 2026, §8.93.0).

## 8.93.3 Provenance — COMPLÉTÉE (22 novembre 2026)

Protocole gelé `PROTOCOL_nulls_distribution_893.md` (SHA d'origine
`d2cdbc3d589d3be61a506f7be2a250d3d4a1c9adc21d1327c8ffc7a61f6529a0` ;
addendum correction 21 novembre 2026, SHA après ajout
`785784446c18f9450fc0963f26c40796dce66e70a329650d2001c19316bd2599`) ;
addendum `ADDENDUM_correction_20261121_893.md` (SHA
`50ad59801aa618f1908908c396c536ab649e63dd5ead08f97d591f8dd0bc34ec`) ;
provenance `PROVENANCE_893.md` (squelette au 21 nov. 2026 — les
résultats sont consignés ici, dans cette section, et dans les JSON
ci-dessous, sans réécrire le squelette).

Scripts : `replica_nulls_893.py` (SHA
`a270da28b0b9d96cdabe18bf189525f42ff0cd9d4bbe9728aa31843b7b9963fe`),
`extract_893_fresh.py` (SHA
`405b2cf666efafedfac1693d8f54328040493ffd82ceb4a614c9f4664ca6ec1a`,
extraction des 150 nuls frais + 15 réels par `extract_858.extract`,
lecture seule), `build_nulls_893.py`, `run_nulls_893_e1.sh`,
`run_nulls_893_e2.sh`, `queue_893_896.sh`, `watch_queue_893_896.sh`.
Versions : v6.2 SHA `f07567c4…` (travail, vérifié avant chaque lot et
à la fin des deux lots, inchangé), v6.1 SHA `2af5e5ce…` (référence),
v6 SHA `bb8bbdba…`.

Sorties (SHA-256) : `nulls_dist_893_verify.json`
`7122d7d7e1fa771ddd243c01593ef3725314d09f1a97dcf5f0ef05a612dd32f8`
(calibration 30/30 à 0,00e+00) ; `nulls_dist_893_replica.json`
`50f1924c498ff07fdf36e7a4eeda0c31d98c0f01f474f028005087a9f454fd9b` ;
`nulls_dist_893_replica_raw.csv`
`4a4c8cf43de2f456571f0bc71e4b2e0778192e0cf490c563c3a1acfe80ae1fc4`
(30 000 tirages bruts) ; `nulls_dist_893_table.json`
`3ce39accab00dae86e713794bc683e8d9f550e8b22a660576837b67f5dad27fd`
(lecture gelée + A2-distrib) ; `nulls_dist_893_fresh.json`
`76a571ee6e0339be5442d19127d3da599aba6335860169d5e0ad0544021d8d82`
(165 runs extraits : 15 réels + 150 nuls frais) ;
`nulls_dist_893_fresh.csv`
`d7a06f9064fed03b879ab46f8c7fbdf91c504a642620765cd924e4f5fef2c005` ;
`nulls_dist_893_fresh_summary.json`
`dfe619ff9eec8079867aed4856f73e330282cabf27739109f0aef6dc7834535e`
(résumé par paire) ; `nulls_dist_893_sensibilites.json`
`7a2f3e5398e9edcfd8e79b8c54900cc1ff76b18558f26636c3e36e999fc5020c`
(planchers 0,05/0,10, S_sep, MC, question subsidiaire).

Lots : file systemd `queue_893_896` — réplique étape 3 exit 0,
22 nov. 2026 12h33 UTC ; étape 1 (80 runs) fin 22 nov. 13h16 UTC,
80 libellés distincts EXIT:0, 0 non nul ; étape 2 (70 runs) fin
22 nov. 15h35 UTC, 70 libellés distincts EXIT:0, 0 non nul ;
marqueur `QUEUE_893_896_DONE` (SHA
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`,
fichier vide). Graines : réplique 3000–3999, maître
`default_rng(20261121)` ; nuls frais 9101–9110 ; CSV des 150 nuls
frais construits avant les runs, SHA consignés dans
`nulls_893_files.json` (SHA
`5787aca22f6950f0af08c555d314e3535f18ea245a8511446d9c42cf4d677d69`).

Correction de nom : le script de re-téléchargement des données est
`download_data_877.sh` (SHA `55811136…`), pas `download_data.sh` —
l'ancien nom n'est utilisé dans aucun texte neuf de cette section.
Aucune recommandation clinique.
