### 8.53 Distribution des nuls à n≈70 — plancher honnête et nombre de nuls requis (19–20 nov. 2026)

**Verdict d'abord. À n≈70, le plancher honnête des S_sep nuls est
0,38 en ICGC et 0,36 en GSE62452 (p95, réplique 1000 tirages, config
nulle) — le réel ICGC (0,2289) est sous ce plancher, au 43,5e
percentile des nuls, donc indistinguable d'un tirage nul ; le réel
GSE62452 (0,4656) est au 99,2e percentile, donc au-dessus. Le plancher
est un effet de n, pas de cohorte : les deux bras n≈70 s'accordent
(médianes 0,239 / 0,236, p95 0,383 / 0,363) et diffèrent tous deux de
TCGA n=178 (médiane 0,166, p95 0,292). Un écart réel−médiane nulle
inférieur à l'IQR nul (~0,08) est un bruit de tirage, pas une mesure.
Pour qu'un écart S_sep devienne une mesure, il faut en pratique
≈200 nuls (la médiane converge dès ~50–100, mais le p95 — le plancher
lui-même — n'est stable qu'à ~100–200) ; avec 20 nuls, l'écart-type
de la médiane est encore de ~0,015 et la demi-largeur de l'intervalle
95 % du p95 de ~0,06–0,08. Le lot pipeline (24 nuls ICGC, 23 GSE62452,
8 TCGA) confirme la réplique en médiane sur les deux bras n≈70
(écarts +0,026 et +0,004, dans la tolérance gelée de ±0,03) et
partiellement en queue (p95 ICGC +0,059, juste au-dessus de la
tolérance de ±0,05 ; GSE62452 −0,032, dedans) : le pipeline tel qu'il
tourne, optimiseur libre, produit une distribution des nuls un peu
plus large que la réplique à config fixe, surtout dans la queue —
le plancher pipeline à n≈70 vaut 0,44 en ICGC et 0,33 en GSE62452,
contre 0,38 et 0,36 en réplique. Le réel ICGC reste sous les deux
planchers (29,2e percentile des nuls pipeline).**

#### 8.53.1 Faits de départ (§8.47, relus)

À n≈70, S_sep lu sur un seul nul est un tirage, pas une mesure :
réel ICGC maxsep 0,2299 battu par un nul dans 61 % des cas (500
permutations) ; nul graine 42 haut (0,4500, ~98e percentile) mais
ordinaire (1 nul frais sur 3 atteint 0,4564) ; petit n relève le
plancher du nul (médiane 0,246 à n=70 contre 0,170 à n=178, réplique
500 tirages). S_sep = max_separation × stabilité, stabilité saturée
(0,97–1,00) : S_sep ≈ max_separation. Ce chantier mesure la
distribution COMPLÈTE des S_sep nuls à n≈70 (1000 tirages par bras
et par config, plus 45 runs pipeline v6.2 sur des nuls frais) et en
déduit le plancher honnête et le nombre de nuls requis — les deux
critères gelés avant toute analyse dans
`PROTOCOL_nulls_n70_853.md`.

#### 8.53.2 Distribution des S_sep nuls (réplique, 1000 tirages par ligne)

Réplique calibrée 8/8 EXACTS (écart 0,00e+00 sur maxsep, courbe
identique) avant tout tirage ; 1000 permutations par ligne, graine
maîtresse neuve `default_rng(20261119)`, sous les deux configs fixes
(config réelle et config nulle du run v6.2 existant). Valeurs brutes
conservées intégralement (`nulls_n70_853_replica_raw.csv`, 6000
lignes). S_sep par tirage = maxsep × stabilité du tirage.

| Bras | n | Config | Médiane | p5 | p25 | p75 | p95 | p97,5 | SD | IQR | min–max |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ICGC | 70 | nulle | 0,2387 | 0,1592 | 0,2015 | 0,2873 | **0,3825** | 0,4181 | 0,0705 | 0,0858 | 0,1117–0,6599 |
| ICGC | 70 | réelle | 0,2481 | 0,1677 | 0,2062 | 0,3010 | 0,4214 | 0,4680 | 0,0802 | 0,0949 | 0,1193–0,6020 |
| GSE62452 | 69 | nulle | 0,2364 | 0,1668 | 0,2052 | 0,2819 | **0,3628** | 0,3761 | 0,0590 | 0,0767 | 0,1127–0,5250 |
| GSE62452 | 69 | réelle | 0,2493 | 0,1764 | 0,2120 | 0,2865 | 0,3649 | 0,3935 | 0,0592 | 0,0745 | 0,1291–0,5036 |
| TCGA | 178 | nulle | 0,1662 | 0,1001 | 0,1346 | 0,2050 | **0,2919** | 0,3242 | 0,0592 | 0,0704 | 0,0744–0,4755 |
| TCGA | 178 | réelle | 0,1971 | 0,1267 | 0,1608 | 0,2503 | 0,3447 | 0,3742 | 0,0690 | 0,0895 | 0,0930–0,5459 |

Lecture : à n≈70, la moitié des nuls tombent entre ~0,20 et ~0,29,
mais 5 % dépassent 0,36–0,38 et le maximum atteint 0,66 (ICGC) —
la queue est longue vers le haut, c'est elle qui fait le plancher.
Le nul graine 42 (S_sep 0,4489) est au ~99e percentile de la
distribution config nulle (P(nul ≥ 0,4489) = 0,011) : haut, pas
aberrant (max 0,66 sur 1000 tirages). Les médianes §8.47 (500
tirages) sont reproduites à ±0,01 près (ICGC 0,2458 → 0,2387 ;
GSE62452 0,2426 → 0,2364 ; TCGA 0,1700 → 0,1662) : la réplique est
stable d'une graine maîtresse à l'autre.

Position des réels dans leur distribution nulle (config nulle) :

| Bras | S_sep réel (pipeline, sa config) | S_sep réel sous config nulle | Médiane nulle | Réel − médiane | En SD nulles | Percentile du réel | P(nul ≥ réel) |
|---|---|---|---|---|---|---|---|
| ICGC | 0,2289 | 0,2283 | 0,2387 | −0,0104 | −0,15 | 43,5 | 0,565 |
| GSE62452 | 0,4656 | 0,4201 | 0,2364 | +0,1837 | +3,11 | 99,2 | 0,008 |
| TCGA | 0,5263 | 0,4260 | 0,1662 | +0,2598 | +4,39 | 99,9 | 0,001 |

Le réel ICGC est au 43,5e percentile des nuls : un nul tiré au
hasard le bat dans 56,5 % des cas (61 % en §8.47 à 500 tirages —
même conclusion). Son écart à la médiane nulle (−0,01) est sept
fois plus petit que l'IQR nul (0,086) : bruit de tirage, pas une
mesure. GSE62452 et TCGA, eux, sont à +3,1 et +4,4 SD de leur
médiane nulle. Même avec un nul au p97,5, GSE62452 reste positif
(+0,044) et TCGA largement (+0,102), alors qu'ICGC tombe à −0,19.

#### 8.53.3 Le plancher honnête à n≈70 (et son effet de n)

Plancher honnête (critère gelé : p95 de la distribution des S_sep
nuls, config nulle) : **ICGC 0,3825 ; GSE62452 0,3628 ; TCGA 0,2919**.
Un réel sous son p95 est « indistinguable d'un tirage nul » ; au-dessus,
« au-dessus du plancher ». En écart à la médiane nulle, le plancher
vaut d_plancher = p95 − médiane : ICGC +0,1438 ; GSE62452 +0,1264 ;
TCGA +0,1257 — soit ~2,1 SD nulles partout. Autrement dit, à n≈70
comme à n=178, il faut dépasser la médiane nulle d'environ +0,13 à
+0,14 pour parler de mesure ; ce qui change avec n, c'est la
médiane elle-même (+0,07 à n≈70).

Effet de n (réplique, config nulle) : Δ médiane n≈70 − n=178 =
+0,0725 (ICGC) et +0,0702 (GSE62452) ; Δ p95 = +0,0906 et +0,0709.
Les deux bras n≈70 s'accordent entre eux (médianes à 0,002, p95 à
0,020) et diffèrent tous deux de TCGA dans le même sens : l'effet
est dit « de n » selon le critère gelé, pas de cohorte. La dispersion
aussi croît quand n baisse : SD 0,0705 (ICGC) contre 0,0592 (TCGA),
IQR 0,0858 contre 0,0704 — mais la médiane porte l'essentiel de
l'effet (+0,07 sur +0,09 de p95).

Réserve — la config compte aussi : sous config réelle, les
distributions nulles sont décalées vers le haut (médiane ICGC
0,2481 contre 0,2387 ; TCGA 0,1971 contre 0,1662, soit +0,031 ;
p95 TCGA 0,3447 contre 0,2919, soit +0,053). Le plancher cité est
celui de la config nulle, la config de référence du nul ; sous
config réelle il serait plus haut de ~0,01 à ~0,05. Le plancher
n'est donc pas un nombre universel : il dépend de n ET de la config
du scan. Le lot pipeline confirme l'ordre de grandeur et
relève le plancher ICGC : plancher pipeline 0,4418 (ICGC) contre
0,3825 en réplique, 0,3310 (GSE62452) contre 0,3628 — le plancher
honnête « pipeline tel qu'il tourne » à n≈70 est donc 0,33–0,44
selon le bras, pas un nombre unique. Le réel ICGC (0,2289) est sous
les deux planchers ; le réel GSE62452 (0,4656) est au-dessus des
deux.

#### 8.53.4 Lot pipeline v6.2 : 45 nuls frais (20 + 20 + 5)

45 runs v6.2 fast, 45/45 exit 0 (19 nov. 23h35 – 20 nov. 02h36 UTC,
unités `v62-853`, `v62-853b`, `v62-853c` — deux reprises après
redémarrage du runtime, §8.53.6d ; SHA v6.2 re-vérifié avant et après,
`f07567c4…`). Nuls frais graines 11–30 (ICGC, GSE62452) et 11–15
(TCGA), plus les nuls pipeline déjà existants (§8.47 : s1–s3 + nul42
ICGC ; s1–s2 + nul42 GSE62452 ; s1–s2 + nul42 TCGA). Distributions
pipeline complètes (S_sep) :

| Bras | n tirages | Médiane | p5 | p25 | p75 | p95 | p97,5 | SD | IQR | min–max | Réel | Réel − méd. | Percentile du réel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ICGC | 24 | 0,2642 | 0,1792 | 0,2155 | 0,3337 | **0,4418** | 0,4492 | 0,0834 | 0,1182 | 0,1517–0,4497 | 0,2289 | −0,0353 | 29,2 |
| GSE62452 | 23 | 0,2403 | 0,1827 | 0,2030 | 0,2824 | **0,3310** | 0,3501 | 0,0565 | 0,0794 | 0,1487–0,3727 | 0,4656 | +0,2253 | 100,0 |
| TCGA | 8 | 0,2110 | 0,1437 | 0,1584 | 0,2852 | 0,4532 | 0,4672 | 0,1252 | 0,1269 | 0,1390–0,4811 | 0,5263 | +0,3153 | 100,0 |

Écart pipeline − réplique (config nulle) et verdict de prédictivité
(critères gelés : |Δ médiane| ≤ 0,03 ET |Δ p95| ≤ 0,05) :

| Bras | Δ médiane | Δ p95 | Verdict |
|---|---|---|---|
| ICGC | +0,0255 | +0,0593 | **Partiel** : médiane dedans, p95 dépassé de 0,009 |
| GSE62452 | +0,0039 | −0,0317 | **Prédictive** : les deux dedans |
| TCGA (8 tirages) | +0,0448 | +0,1613 | **Non prédictive sur 8 tirages** (voir ci-dessous) |

La réplique est donc prédictive en médiane sur les deux bras n≈70,
partielle en queue. Le pipeline tel qu'il tourne produit une
distribution des nuls un peu plus large que la réplique à config
fixe : SD 0,0834 contre 0,0705 en ICGC (+18 %), IQR 0,1182 contre
0,0858 ; 3 nuls pipeline ICGC sur 24 dépassent le p95 réplique
(12,5 % contre 5 % attendus) et 2 sur 24 dépassent le p97,5 (8,3 %
contre 2,5 %). En GSE62452 l'élargissement est absent (SD 0,0565
contre 0,0590 ; 1/23 au-dessus du p95 réplique, 4,3 %). Le mécanisme
est nommé : l'optimiseur choisit sa config par run et choisit
souvent la config RÉELLE pour un nul — 17 des 20 nuls frais ICGC
tournent en w=16/ncand=35 (config réelle ICGC) contre w=16/ncand=22
pour la config nulle de la réplique ; en TCGA, les deux tirages
extrêmes (s13 0,4014, s14 0,4811, percentiles réplique 99,8 et
100,0) tournent en w=30/ncand=93, la config réelle TCGA, contre
w=43/ncand=46 pour la config nulle. La distribution pipeline est un
mélange sur les configs, pas une distribution à config fixe —
c'est elle qui porte le plancher « tel qu'il tourne ».

TCGA, réserve majeure : 8 tirages seulement, dont 2 extrêmes
(s13, s14) qui à eux seuls font la SD (0,1252 contre 0,0592 en
réplique) et le p95 (0,4532, qui est presque le maximum). Le p95
pipeline TCGA n'est pas interprétable sur 8 tirages et la médiane
(+0,045) non plus avec cette incertitude (SE bootstrap de la médiane
0,0540). La quantification de l'effet de n repose donc sur la
réplique (§8.53.3) ; le lot pipeline ne la confirme qu'à n≈70, où
il a 23–24 tirages. Le réel TCGA (0,5263) reste au-dessus de tous
les planchers mesurés, réplique comme pipeline.

Position des réels : le réel ICGC est au 29,2e percentile des nuls
pipeline (7 nuls sur 24 sous lui, 17 au-dessus) — sous le plancher
pipeline comme sous le plancher réplique. Le réel GSE62452 est
au-dessus des 23 nuls pipeline (100e percentile). Les 20 nuls frais
ICGC seuls vont de 0,1517 (s20) à 0,4016 (s29) ; GSE62452 de 0,1487
(s26) à 0,3727 (s13) ; TCGA de 0,1523 (s15) à 0,4811 (s14).

Observation annexe (pas un critère du protocole) : le MC ne sépare
pas non plus sur ces tirages frais — nuls ICGC MC 0,323–0,360 contre
réel 0,3342 ; nuls TCGA s11/s12 MC 0,5324/0,4715 contre réel 0,3785
— cohérent avec §8.32/§8.35 (MC 1/8).

#### 8.53.5 Combien de nuls faut-il en pratique ? (convergence)

Courbes de convergence sur les 1000 tirages (config nulle, 200
sous-échantillons sans remise par k) : écart-type empirique de la
médiane estimée, et demi-largeur de l'intervalle 95 % du p95 estimé.

| k (nuls) | ICGC : SE(médiane) | ICGC : demi-larg. IC95 p95 | GSE62452 : SE(méd.) | GSE62452 : demi-larg. p95 | TCGA : SE(méd.) | TCGA : demi-larg. p95 |
|---|---|---|---|---|---|---|
| 1 | 0,0731 | 0,1282 | 0,0604 | 0,1021 | 0,0593 | 0,1193 |
| 2 | 0,0435 | 0,1119 | 0,0468 | 0,1060 | 0,0434 | 0,1081 |
| 3 | 0,0444 | 0,1227 | 0,0426 | 0,0894 | 0,0354 | 0,0925 |
| 5 | 0,0358 | 0,1041 | 0,0296 | 0,0752 | 0,0309 | 0,0896 |
| 10 | 0,0245 | 0,1016 | 0,0222 | 0,0757 | 0,0200 | 0,0766 |
| 20 | 0,0172 | 0,0801 | 0,0134 | 0,0591 | 0,0133 | 0,0661 |
| 30 | 0,0146 | 0,0656 | 0,0099 | 0,0400 | 0,0122 | 0,0570 |
| 50 | 0,0104 | 0,0502 | 0,0084 | 0,0400 | 0,0097 | 0,0465 |
| 100 | 0,0079 | 0,0349 | 0,0054 | 0,0248 | 0,0063 | 0,0333 |
| 200 | 0,0048 | 0,0253 | 0,0035 | 0,0176 | 0,0040 | 0,0274 |
| 500 | 0,0023 | 0,0137 | 0,0018 | 0,0070 | 0,0018 | 0,0148 |

Critères gelés : plus petit k tel que SE(médiane) ≤ 0,01 ET
demi-largeur IC95(p95) ≤ 0,03.

| Bras | k pour la médiane seule | k pour le p95 seul | k requis (max des deux) |
|---|---|---|---|
| ICGC (n=70) | 100 (0,0079 ; 50 donne 0,0104, juste au-dessus) | 200 (0,0253 ; 100 donne 0,0349) | **200** |
| GSE62452 (n=69) | 30 (0,0099) | 100 (0,0248 ; 50 donne 0,0400) | **100** |
| TCGA (n=178) | 50 (0,0097) | 200 (0,0274 ; 100 donne 0,0333) | **200** |

**En pratique : ≈200 nuls.** La médiane converge vite (30–100
nuls suffisent pour la situer à ±0,01), mais le plancher lui-même —
le p95 — est une statistique de queue : il faut 100 à 200 tirages
pour le situer à ±0,03. Avec un seul nul, l'écart-type de la
« médiane » estimée est de 0,06–0,07 et l'incertitude sur le p95
de ±0,10–0,13 : c'est la mesure chiffrée de « un nul est un tirage,
pas une mesure ». Avec 20 nuls (le lot pipeline de ce chantier),
SE(médiane) ≈ 0,013–0,017 et demi-largeur IC95(p95) ≈ 0,06–0,08 :
le lot pipeline situe la médiane à ~±0,015 mais son p95 reste
incertain à ~±0,07 — d'où la primauté de la réplique 1000 tirages
pour le plancher, le lot pipeline servant de confirmation.
(Vérification croisée SE bootstrap : voir le paragraphe après
« Conséquence pour les lots passés », ci-dessous.)

Conséquence pour les lots passés : les d_ssep lus sur un seul nul
(§8.32, §8.38, §8.47) portent une incertitude de tirage de l'ordre
de ±0,06–0,07 (SD nulle) sur le terme nul seul ; un d_ssep de
+0,15 à n≈70 (GSE62452) reste au-dessus du plancher, un d_ssep de
−0,22 (ICGC) est dominé par le tirage du nul (le nul 42 est à
+0,21 au-dessus de la médiane nulle, le réel à −0,01). Les verdicts
« sépare / ne sépare pas » fondés sur un seul nul doivent être
relus contre le plancher 0,36–0,38 à n≈70, pas contre 0.

Vérification croisée (critère gelé) : l'écart-type bootstrap de la
médiane pipeline vaut 0,0275 (ICGC, n=24) et 0,0236 (GSE62452,
n=23), contre ~0,016 et ~0,012 prédits par la courbe réplique à
k≈24 (interpolation entre k=20 et k=30) — écarts 0,011 sur les deux
bras, juste au-dessus de la tolérance de ±0,01. La vérification est
donc manquée de justesse : la médiane pipeline est un peu moins
précise que la courbe réplique ne le prédit, parce que la
distribution pipeline est plus large (ICGC) et que le bootstrap sur
23–24 tirages est lui-même bruité. L'écart est petit (0,001
au-dessus de la tolérance) et de même signe sur les deux bras ; il
ne change pas le nombre requis (≈200), il dit seulement que le lot
pipeline, à 24 tirages, situe sa médiane à ±0,025 environ, pas à
±0,016.

#### 8.53.6 Méthode

Protocole gelé avant tout run et toute analyse neuve :
`PROTOCOL_nulls_n70_853.md`, SHA
`38689f8a411ac9b5…`. Critères écrits avant :
plancher = p95 nul (config nulle) ; nombre de nuls requis = plus
petit k avec SE(médiane) ≤ 0,01 ET demi-largeur IC95(p95) ≤ 0,03 ;
validation réplique ↔ pipeline : |Δ médiane| ≤ 0,03 ET |Δ p95| ≤
0,05 ; effet « de n » si les deux bras n≈70 s'accordent (±0,03) et
diffèrent tous deux de TCGA dans le même sens ; vérification croisée
SE bootstrap pipeline vs courbe réplique à k = n (tolérance ±0,01).
**(a) Vérification des entrées** (`verify_nulls_n70_853.py`, SHA
`99f7910a0b36…`) : SHA des 6 CSV réel + nul42 re-vérifiés contre
PROVENANCE_immune_v6.md (conformes) ; chaque nul42 est bien une
permutation par ligne du réel (step inchangé, même multi-ensemble) ;
0 valeur manquante ; n = 70 / 69 / 178.
**(b) Réplique** (`replica_nulls_n70_853.py`, SHA
`023c1fcb50b0…`) :
fonctions du pipeline elles-mêmes, import en lecture seule
(`_build_mc_progress_axis` + `scan_critical_threshold` +
`evaluate_scan_quality`), calibration 8/8 EXACTS avant tout tirage
(écart maxsep 0,00e+00, courbe identique) ; 1000 permutations par
ligne par (cohorte, config), graine maîtresse `default_rng(20261119)`
(neuve, distincte de §8.47) ; S_sep = maxsep × stab par tirage ;
valeurs brutes conservées (`nulls_n70_853_replica_raw.csv`, 6000
lignes) ; convergence par sous-échantillonnage sans remise (200
répétitions par k, k=1000 = échantillon complet).
**(c) Nuls frais** (`build_nulls_n70_853.py`, SHA
`1af4f5ec691b…`) :
même méthode que §8.47 (`default_rng(graine)`, `permutation(n)`,
lignes entières, step inchangé), graines nouvelles 11–30 (ICGC,
GSE62452) et 11–15 (TCGA) — jamais utilisées (§8.47 : 1–3, 42).
**(d) Lot pipeline** : v6.2 mode fast, 45 runs, 45/45 exit 0, lancés
via `systemd-run` (unités `v62-853`, `v62-853b`, `v62-853c`), SHA v6.2
re-vérifié avant et après le lot (`f07567c4…`). Le lot a été
interrompu deux fois par des redémarrages du runtime (19 nov.
~23h44 UTC après le run s11, et 20 nov. ~01h43 UTC après 25 runs)
qui ont tué les unités systemd — `systemd-run` survit à la mort
d'une session shell, pas à un redémarrage de la machine ; le lot a
été repris deux fois à partir du journal des exit codes
(`run_nulls_n70_853_resume.sh`, SHA `b311ee0b831a…`, puis
`run_nulls_n70_853_resume2.sh`, SHA `0762f10d16f5…`), chaque run
interrompu (s12, puis s16 GSE62452) ayant été relancé intégralement
après suppression de son dossier partiel (sans `master_results.json`),
donc aucun run n'est compté deux fois. Début 19 nov. 23h35 UTC, fin
20 nov. 02h36 UTC. Extraction
(`extract_nulls_n70_853.py`, SHA `576885c74344…`).

#### 8.53.7 Limites

- La réplique fixe les configs ; l'optimiseur en choisit une par run
  — la distribution des nuls du pipeline tel qu'il tourne est un peu
  plus large que celle de la réplique : SD +18 % en ICGC, 3/24 nuls
  au-dessus du p95 réplique (12,5 % contre 5 % attendus) ; le plancher
  pipeline ICGC (0,4418) dépasse le plancher réplique (0,3825) de
  0,059. En GSE62452 l'élargissement est absent.
- Le plancher p95 est celui de la config nulle ; sous config réelle
  il est plus haut de ~0,01 à ~0,05. Le plancher dépend de n ET de
  la config : il n'y a pas un nombre unique « à n≈70 ».
- 24 tirages pipeline par bras n≈70 : la queue (p95) y est estimée
  avec une large incertitude (±0,06–0,08) — la réplique 1000 tirages
  porte l'estimation du p95, le lot pipeline la confirme ou la
  conteste. À n=178, le lot pipeline n'a que 8 tirages : son p95
  (0,4532) n'est pas interprétable.
- Le nul du projet permute les lignes entières (corrélations
  inter-flux préservées) : la distribution mesurée est celle du nul
  du projet, pas d'un nul à corrélations brisées (§8.47 H5 : écart
  de médianes 0,0115 en ICGC — petit, mais nommé).
- n=70 : toute distribution estimée reste une distribution du scan,
  pas une preuve biologique. Ce chantier ne change rien au verdict
  biologique du §8.23 (froid tumoral, KRAS + anti-PD-(L)1 : NON) :
  il quantifie seulement ce qu'il faut pour lire S_sep à n≈70.
- Le nombre « ≈200 nuls » vaut pour les critères gelés
  (SE médiane ≤ 0,01, IC95 p95 ±0,03). Des critères plus lâches
  (par ex. médiane seule à ±0,02) demanderaient moins ; des critères
  plus stricts (p97,5 à ±0,02) demanderaient plus — les courbes du
  §8.53.5 permettent de relire le nombre sous d'autres critères.

#### 8.53.8 Provenance

- Protocole : `PROTOCOL_nulls_n70_853.md`, SHA
  `38689f8a411ac9b5…`.
- Pipeline v6.2 :
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
  re-vérifié avant et après le lot, jamais modifié. Mode fast.
- Entrées (déjà sur disque, rien re-téléchargé) : flux immunitaires
  `pdac_immune_{tcga,geo62452,icgc}_fluxes(_nul).csv` (SHA dans
  PROVENANCE_immune_v6.md, re-vérifiés §8.53.6a) ; matrices sources :
  TCGA Firehose PAAD MD5 `b09569ce…`, GSE62452 SHA `8f41d5b3…`,
  ICGC Xena SHA `c2cb57af…` (Bailey et al., Nature 2016,
  doi:10.1038/nature16965).
- Scripts (SHA-256) : `verify_nulls_n70_853.py` `99f7910a0b36…`,
  `replica_nulls_n70_853.py` `023c1fcb50b0…`,
  `build_nulls_n70_853.py` `1af4f5ec691b…`,
  `extract_nulls_n70_853.py` `576885c74344…`,
  `run_nulls_n70_853.sh` `d623a3d128aa…`,
  `run_nulls_n70_853_resume.sh` `b311ee0b831a…`,
  `run_nulls_n70_853_resume2.sh` `0762f10d16f5…`.
- Sorties : `nulls_n70_853_verify.json` (`1ae1faf91ac8…`),
  `nulls_n70_853_replica.json` (`223a5c096bcc…`, contient aussi les
  courbes de convergence — pas de fichier JSON de convergence
  séparé), `nulls_n70_853_replica_raw.csv` (`b586eed348f3…`),
  `nulls_n70_853_convergence.csv` (`90786f599119…`),
  `nulls_n70_853_files.json` (`eee29a6f3058…`, SHA des 45 fichiers
  de nuls, re-vérifiés : 0 différence),
  `nulls_n70_853_confirm.json` (`cadfbef3c0ae…`),
  `replica_853.log` (réplique, exit 0),
  `runs_nulls_n70_853.log` (lot v6.2, 45/45 exit 0, 19 nov. 23h35 –
  20 nov. 02h36 UTC, unités systemd `v62-853` / `v62-853b` /
  `v62-853c`), dossiers `results_fast_v62_853_*` (45 runs), fichiers
  de flux `pdac_immune_{icgc,geo62452}_fluxes_nul_s{11..30}.csv` et
  `pdac_immune_tcga_fluxes_nul_s{11..15}.csv` (SHA dans
  `nulls_n70_853_files.json`).
- Faits de départ §8.47 : `section_8.47_icgc_immune_inversion.md`,
  protocole `PROTOCOL_icgc_immune_inversion.md` SHA `b55283ee…`
  (amendé `f1a5a37c…`).
- Livre blanc : `livre-blanc-pdac-v6.md`, SHA `31bc39a1…`, §8.1–§8.49
  (cette section §8.53 est à fusionner par le coordinateur ; §8.50–
  §8.52 appartiennent à d'autres chantiers).
