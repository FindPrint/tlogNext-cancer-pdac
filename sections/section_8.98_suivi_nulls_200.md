### 8.98 Suivi §8.93 : chaque paire jugée contre 200 nuls frais pipeline — RÉSULTATS COMPLETS (23 novembre 2026)

**Verdict global.** Sur les 15 paires jugées contre 200 nuls frais
pipeline chacune (10 du §8.93 + 190 nouveaux, graines 9101–9300),
les données montrent : **6 paires SOLIDES, 4 FRAGILES, 5 NON** —
A2-distrib **6/15** (12/15 positifs, LOO pire cas 5/14), contre
A2-distrib 5/15 au §8.93 (12/15 positifs, LOO 4/14). **14/15
verdicts inchangés ; seul changement : ICGC passe de FRAGILE à
SOLIDE** (réel 0,4080, p95 0,3365, 95,5 % des nuls sous le plancher).
Les 15 réels sont au-dessus de la médiane de leurs 200 nuls. Le lot
est complet : 3000/3000 nuls lus, 0 manquant. Les verdicts décrivent
la position du réel dans la distribution des nuls observée ; ils ne
prédisent rien.

## 8.98.1 Question, méthode, règle gelée

**Question.** Au §8.93, chaque paire a été jugée contre une
réplique de 1000 permutations par ligne (config fixe) et validée
par 10 nuls frais pipeline. La question posée ici est la suite
directe : chaque paire survit-elle à une distribution de **200
nuls frais pipeline** — la cible que le §8.53 nomme pour un p95
stable (~200 nuls par paire) ? La réplique de 1000 permutations
n'est PAS refaite ici : la distribution est faite de nuls pipeline
uniquement.

**Statut du lot.** Ce lot est une PROPOSITION, pas un fait du
protocole gelé §8.93 : le protocole ne définit pas de « lot
suivant » et valide par 10 nuls frais par paire. La proposition
(190 nuls frais supplémentaires par paire, graines 9111–9300, pour
passer de 10 à 200 nuls frais par paire, total 2850 runs) a reçu le
go de Zackary le 22 novembre 2026 à 11h32 (« Allez s'y »), après la
publication §8.93–§8.97. Les graines 9111–9300 sont disjointes de
9101–9110 (lot §8.93), de 3000–3999 (réplique §8.93) et de 42 (nul
unique historique).

**Méthode.** Mêmes paires, mêmes réels, même règle, plus de nuls.
Les 190 nuls nouveaux sont construits par le même script que les
10 du §8.93 (`scripts/build_null_893.py` : `default_rng(graine)`,
permutation des lignes entières, colonne de contrôle inchangée).
Le maxsep réel de chaque paire est repris de
`nulls_dist_893_table.json` (§8.93) — aucune valeur re-saisie à la
main. Le maxsep de chaque nul est lu dans son
`master_results.json` (`run_pipeline.threshold_metadata.
threshold_optimization.best_config.metrics.max_separation`, même
chemin que `replica_nulls_893.read_best_config`). Les dossiers des
nuls 9111–9300 sont lus dans `ledger.csv` (seule source de vérité) ;
ceux des nuls 9101–9110 sont `results_fast_v62_893_*`. L'agrégation
est faite par `analyse_lot_next.py` (voir §8.98.8), qui juge chaque
paire selon la règle gelée §8.93 §4.

**Règle gelée (§8.93 §4), appliquée telle quelle.** SOLIDE si réel
> p95 des nuls ET ≥ 95 % des nuls sous le plancher (écart réel −
nul > 0,07 contre ≥ 95 % des nuls) ; FRAGILE si réel > médiane
mais ≤ p95, ou 50–95 % sous le plancher ; NON si réel ≤ médiane ou
< 50 % sous le plancher. Plancher 0,07. Note de lecture : le §8.93
écrivait « ≥ 950/1000 » parce que la réplique avait 1000 tirages ;
ici le dénominateur est 200 (≥ 190/200) — même seuil, même règle.
Les quantiles sont calculés par interpolation linéaire (position
p×(n−1), n = 200) ; toutes les valeurs de la table sont arrondies
à 4 décimales.

**Application de la correction de Zackary du 21 novembre 2026
(12h03, portée étendue à tout le projet à 12h04).** (1) Contrôle
jamais analysé : les 200 nuls sont des permutations des mêmes CSV
(contrôle `step`, KRAS absent des flux) et le pipeline exclut la
colonne de contrôle des flux analysés par construction (ligne 6787
de `universal_v6.2.0_cohen.py`). Règle respectée. (2) Aucun seuil
écarté pour non-monotonie. (3) Tous les verdicts de cette section
sont formulés comme de l'analyse (ce que les données montrent) et
non comme des prédictions.

## 8.98.2 Le lot : exécution

**Lancement.** 22 novembre 2026, 11h32 EST, après la publication
§8.93–§8.97. Répartition initiale par paires entières, aucune
graine recouvrante : GitHub E1 = 8 paires principales (HP35, TCGA
v4, GSE71729, GSE62452, ICGC, Immunitaire TCGA, PARP TCGA, DepMap)
= 1520 runs ; local E2 = 7 paires A2 restantes (GSE21501,
GSE79668, GSE60979, Yeh FF, GSE57495, GDC ORGANOID, GSE194249) =
1330 runs.

**Piste GitHub** (dépôt FindPrint/tlogNext-pipeline-actions).
Run #2 (45056686992, workflow `pipeline-nulls-lot.yml`, commit
0511dae, correctif matrice, 152 jobs, timeout 120 min) : 146
succès, 6 jobs HP35 annulés à la limite de 2 h (blocs 2, 5, 7, 8,
14, 17 = 60 runs, aucun résultat récupérable), 0 échec, 146
artefacts, conclusion « cancelled », fin 22 nov. 19h13 EST.
Relance #3 (45087899473, workflow `pipeline-nulls-lot-rerun.yml`,
commit 05cf9b8, timeout 360 min) : 6/6 jobs, les 60 runs HP35
récupérés à l'identique (mêmes graines, mêmes entrées), fin 22
nov. 22h20 EST. Piste GitHub E1 complète : 1520/1520 runs.

**Scission E2.** 23 novembre 2026, ~07h00, go de Zackary (06h55) :
une partie de ce qui reste est envoyée sur GitHub Actions, qui ne
fait rien depuis la fin du run #3. Découpage par paires entières,
sans recouvrement : GitHub prend geo57495, gdc_organoid,
gse194249 = 570 runs ; le local garde yeh_ff (11 runs restants).
Totaux finaux : GitHub 2090 runs, local 760 runs, total du lot
inchangé 2850. Workflow dédié `pipeline-nulls-lot-e2.yml` (commit
0dba356), run E2 45170178139 : 57/57 jobs réussis, 0 échec, 0
annulé, fin 23 nov. ~08h35 EST.

**Piste locale.** Unité systemd `v62-nulls-next-local`, lanceur
parallèle `run_nulls_parallel.sh` (`xargs -P 2`), 760/760, bilan
ok=9, sautés=751, échecs=0, fin 23 nov. 07h06 EST (12:06:55 UTC).
Gardien (hook de surveillance, 180 s) : 0 run perdu sur les
redémarrages machine du lot.

**Nuls et pipeline.** Nuls construits par
`scripts/build_null_893.py` (SHA `572b55bc…`), validé bit-à-bit
le 22 nov. 2026 : (TCGA v4, graine 9101) reproduit exactement le
fichier du lot §8.93 (SHA `22f39bf7…e8fa`). Pipeline v6.2, SHA
`f07567c4…`, vérifié inchangé en début et en fin de lot local.

**Téléchargement.** 23 novembre 2026, 08h37–09h20, via le
navigateur : 209 artefacts (146 run #2 + 6 run #3 + 57 run E2).
Vérification : run #3, SHA-256 bit-à-bit contre les digests
GitHub, 6/6 ; run E2, tailles exactes 57/57 et intégrité zip
57/57 ; run #2, 209 artefacts distincts au total, 210 fichiers
testés, 0 corrompu. Dette nommée : la vérification SHA-256 des
artefacts E2 et run #2 contre les digests GitHub a été impossible
(API GitHub en limite de requêtes non authentifiées, 403) — à
refaire à la prochaine occasion ; les artefacts restent sur GitHub
jusqu'à ~29 nov. (rétention 7 jours).

**Extraction et agrégation.** Extraction : 2090
`master_results.json` GitHub + 760 locaux = 3000 nuls (200 par
paire), 0 manquant, inventaire vérifié le 23 nov. 10h46 ;
`ledger.csv`, 2850 lignes, statut passé à « telecharge ».
Agrégation par `analyse_lot_next.py` (SHA `c8d7d23f…`), 23 nov.
10h52, exit 0, 3000/3000 nuls lus. Sorties :
`nulls_lot_next_table.json` (SHA `351d929c…`) et
`nulls_lot_next_table.csv` (SHA `80b2cf14…`).

## 8.98.3 Table complète — 200 nuls frais pipeline par paire

Rang ascendant /201, réel inclus : rang 201 = réel au-dessus des
200 nuls ; rang 111 = 90 nuls au-dessus du réel. Plancher gelé
0,07 : % des nuls dont l'écart réel−nul dépasse 0,07. d vs
médiane = maxsep réel − médiane des nuls. n = taille de la paire ;
flux = nombre de flux analysés.

| Paire | n | flux | maxsep réel | rang /201 | médiane nuls | p95 nuls | min–max nuls | nuls sous réel /200 | % sous plancher | d vs médiane | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HP35 | 1000 | 7 | 1,7718 | 201 | 0,1056 | 0,1787 | 0,0187–0,2263 | 200 | 100,0 % | 1,6662 | SOLIDE |
| TCGA v4 | 178 | 12 | 0,4623 | 201 | 0,1852 | 0,2716 | 0,0709–0,3529 | 200 | 100,0 % | 0,2771 | SOLIDE |
| GSE71729 | 145 | 12 | 0,2593 | 183 | 0,1916 | 0,2722 | 0,1230–0,3582 | 182 | 45,5 % | 0,0677 | NON |
| GSE62452 | 69 | 12 | 0,3100 | 176 | 0,2415 | 0,3539 | 0,1339–0,4354 | 175 | 48,5 % | 0,0685 | NON |
| ICGC | 70 | 12 | 0,4080 | 201 | 0,2372 | 0,3365 | 0,1259–0,4049 | 200 | 95,5 % | 0,1708 | SOLIDE |
| Immunitaire TCGA | 178 | 12 | 0,5309 | 201 | 0,1802 | 0,3047 | 0,0572–0,3860 | 200 | 100,0 % | 0,3507 | SOLIDE |
| PARP TCGA | 178 | 12 | 0,3680 | 201 | 0,1763 | 0,2804 | 0,0755–0,3279 | 200 | 97,0 % | 0,1917 | SOLIDE |
| DepMap | 45 | 12 | 0,4436 | 200 | 0,2777 | 0,4087 | 0,1108–0,4740 | 199 | 87,0 % | 0,1659 | FRAGILE |
| GSE21501 | 132 | 12 | 0,2121 | 124 | 0,2016 | 0,2820 | 0,0854–0,3349 | 123 | 3,0 % | 0,0105 | NON |
| GSE79668 | 51 | 12 | 0,4104 | 200 | 0,2811 | 0,3666 | 0,1281–0,4212 | 199 | 90,0 % | 0,1293 | FRAGILE |
| GSE60979 | 49 | 12 | 0,4418 | 199 | 0,2842 | 0,3879 | 0,1282–0,5238 | 198 | 92,0 % | 0,1576 | FRAGILE |
| GSE131050 Yeh FF | 42 | 12 | 0,3220 | 198 | 0,2110 | 0,2900 | 0,1239–0,3486 | 197 | 78,0 % | 0,1110 | FRAGILE |
| GSE57495 | 63 | 11 | 0,6381 | 201 | 0,2712 | 0,4177 | 0,1335–0,5275 | 200 | 100,0 % | 0,3669 | SOLIDE |
| GDC ORGANOID | 44 | 12 | 0,2542 | 171 | 0,2079 | 0,2778 | 0,1270–0,3255 | 170 | 24,0 % | 0,0463 | NON |
| GSE194249 | 84 | 11 | 0,2306 | 111 | 0,2244 | 0,2825 | 0,1424–0,3074 | 110 | 0,5 % | 0,0062 | NON |

## 8.98.4 Lecture par paire

**SOLIDES (6/15).** HP35 (réel 1,7718, p95 0,1787, 100,0 % sous
le plancher, d vs médiane 1,6662, rang 201/201 — le nul le plus
haut, 0,2263, reste 7,8 fois sous le réel) ; TCGA v4 (0,4623, p95
0,2716, 100,0 %, d 0,2771, rang 201) ; Immunitaire TCGA (0,5309,
p95 0,3047, 100,0 %, d 0,3507, rang 201) ; PARP TCGA (0,3680, p95
0,2804, 97,0 %, d 0,1917, rang 201) ; GSE57495 (0,6381, p95
0,4177, 100,0 %, d 0,3669, rang 201) ; ICGC (0,4080, p95 0,3365,
95,5 %, d 0,1708, rang 201 — passe la barre des 95 % d'un seul
nul : 191/200 nuls sous le plancher, seuil 190/200 ; 9 nuls sont
à moins de 0,07 du réel). Dans les six cas le réel est au-dessus
des 200 nuls (rang 201/201) et au-dessus du p95, avec au moins
95 % des nuls sous le plancher.

**FRAGILES (4/15).** DepMap (réel 0,4436 > p95 0,4087, rang
200/201 — un seul nul au-dessus du réel — mais 87,0 % sous le
plancher) ; GSE79668 (0,4104 > p95 0,3666, rang 200, 90,0 %) ;
GSE60979 (0,4418 > p95 0,3879, rang 199, 92,0 %) ; GSE131050 Yeh
FF (0,3220 > p95 0,2900, rang 198, 78,0 % — le fragile le plus
faible en part sous le plancher). Dans les quatre cas le réel est
au-dessus du p95 des nuls, mais la queue des nuls mord le
plancher : moins de 95 % des nuls sont sous l'écart 0,07.

**NON (5/15).** GSE71729 (réel 0,2593 < p95 0,2722, 45,5 % sous
le plancher, 182/200 nuls sous le réel, d vs médiane 0,0677 —
sous le plancher de justesse) ; GSE62452 (0,3100 < p95 0,3539,
48,5 %, 175/200, d 0,0685 — sous le plancher de justesse) ;
GSE21501 (0,2121, rang 124, 3,0 %, 123/200, d 0,0105) ; GDC
ORGANOID (0,2542 < p95 0,2778, 24,0 %, 170/200 nuls sous le réel
— le réel est au-dessus de 85 % des nuls mais sous le p95) ;
GSE194249 (0,2306, rang 111, 0,5 %, 110/200 — le réel est à peine
au-dessus de la médiane, d 0,0062).

**Note de lecture.** Les 15 réels sont au-dessus de la médiane
de leurs 200 nuls (d vs médiane > 0 partout, de 0,0062 à 1,6662).
C'est une mesure distincte du verdict, et distincte des
« positifs » (12/15 contre le nul graine 42, §8.98.5) : être
au-dessus de la médiane de 200 nuls ne fait pas un SOLIDE, et
GSE194249 montre que la médiane seule ne sépare rien (110/200).

## 8.98.5 Comparaison avec §8.93

Table : verdict §8.93 (réplique 1000 permutations + 10 nuls
frais) contre verdict à 200 nuls frais pipeline. % sous plancher
et p95 : ancien = réplique, config réelle (§8.93.2.2) ; nouveau =
200 nuls frais pipeline (§8.98.3).

| Paire | verdict §8.93 | verdict 200 nuls | % sous plancher §8.93 → 200 nuls | p95 §8.93 → 200 nuls |
|---|---|---|---|---|
| HP35 | SOLIDE | SOLIDE | 100,0 % → 100,0 % | 0,2097 → 0,1787 |
| TCGA v4 | SOLIDE | SOLIDE | 100,0 % → 100,0 % | 0,2644 → 0,2716 |
| GSE71729 | NON | NON | 46,1 % → 45,5 % | 0,2747 → 0,2722 |
| GSE62452 | NON | NON | 45,4 % → 48,5 % | 0,3378 → 0,3539 |
| ICGC | FRAGILE | **SOLIDE** | 93,3 % → **95,5 %** | 0,3489 → 0,3365 |
| Immunitaire TCGA | SOLIDE | SOLIDE | 99,6 % → 100,0 % | 0,3444 → 0,3047 |
| PARP TCGA | SOLIDE | SOLIDE | 97,5 % → 97,0 % | 0,2773 → 0,2804 |
| DepMap | FRAGILE | FRAGILE | 90,5 % → 87,0 % | 0,3977 → 0,4087 |
| GSE21501 | NON | NON | 2,7 % → 3,0 % | 0,2789 → 0,2820 |
| GSE79668 | FRAGILE | FRAGILE | 90,8 % → 90,0 % | 0,3535 → 0,3666 |
| GSE60979 | FRAGILE | FRAGILE | 88,3 % → 92,0 % | 0,4143 → 0,3879 |
| GSE131050 Yeh FF | FRAGILE | FRAGILE | 84,0 % → 78,0 % | 0,2891 → 0,2900 |
| GSE57495 | SOLIDE | SOLIDE | 99,5 % → 100,0 % | 0,4292 → 0,4177 |
| GDC ORGANOID | NON | NON | 32,4 % → 24,0 % | 0,2767 → 0,2778 |
| GSE194249 | NON | NON | 0,8 % → 0,5 % | 0,2793 → 0,2825 |

**14/15 verdicts inchangés ; seul changement : ICGC.** ICGC
passe de FRAGILE à SOLIDE : son % sous le plancher passe de
93,3 % (réplique) à 95,5 % (200 nuls pipeline), au-dessus de la
barre des 95 %, et son réel 0,4080 reste au-dessus du p95
(0,3365 à 200 nuls, contre 0,3489 en réplique). Le réel n'a pas
bougé ; c'est la distribution mesurée qui a bougé — de 2,2
points, d'un seul nul au-dessus du seuil (191/200 contre 190/200
exigés). La lecture ICGC reste la plus fragile des six SOLIDES
(voir §8.98.7).

**A2-distrib : 5/15 → 6/15.** Les six SOLIDES sont HP35, TCGA
v4, Immunitaire TCGA, PARP TCGA, GSE57495 et ICGC. **Positifs :
12/15, inchangés** — d_maxsep contre le nul graine 42 > 0 pour
les mêmes 12 paires qu'au §8.93 (les réels et le nul graine 42
n'ont pas bougé : HP35 +1,6512, TCGA v4 +0,2928, GSE71729
+0,0402, ICGC +0,0970, Immunitaire TCGA +0,3675, PARP TCGA
+0,1688, DepMap +0,1904, GSE79668 +0,0567, GSE60979 +0,2045,
Yeh FF +0,0739, GSE57495 +0,4494, GDC ORGANOID +0,0884 ;
négatifs : GSE62452 −0,0036, GSE21501 −0,0100, GSE194249
−0,0239). **LOO pire cas : 4/14 → 5/14** (convention du script :
solides − 1 sur 14 — retirer un SOLIDE laisse 5/14 ; retirer un
NON ou un FRAGILE laisse 6/14).

**Les p95 bougent dans les deux sens.** Le p95 à 200 nuls
pipeline n'est pas le p95 de la réplique : Immunitaire TCGA
0,3444 → 0,3047, GSE60979 0,4143 → 0,3879, HP35 0,2097 →
0,1787 d'un côté ; DepMap 0,3977 → 0,4087, GSE62452 0,3378 →
0,3539, GSE79668 0,3535 → 0,3666 de l'autre. Les deux
distributions ne sont pas le même objet (réplique = config fixe,
1000 tirages ; pipeline = optimiseur libre, 200 tirages) et le
p95 à 200 tirages porte une incertitude d'échantillonnage.
Aucun des deux p95 n'est « le » p95 ; le verdict de cette
section utilise celui des 200 nuls pipeline, comme gelé ici.
Aucun verdict ne change de côté à cause d'un p95 seul : le seul
changement (ICGC) vient du % sous le plancher, pas du p95.

## 8.98.6 Ce que cela change et ne change pas

**Ce que cela change.** A2-distrib passe de 5/15 à 6/15 ; ICGC
devient SOLIDE contre 200 nuls pipeline. La cible du §8.53
(~200 nuls par paire pour un p95 stable) est atteinte en nuls
pipeline : la proposition initiale du §8.93, déclarée
INFAISABLE en lot unique (3 000 runs ≈ 250 h), a été exécutée en
~21 heures d'horloge (22 nov. 11h32 → 23 nov. 08h35), sur deux
pistes (GitHub Actions + machine locale). La lecture contre une
distribution reste deux fois plus sévère que le compte classique
(6/15 contre 10/15), mais l'écart se resserre d'une paire.

**Ce qui ne change pas.** A2 classique 10/15 (les réels et le
nul graine 42 n'ont pas bougé) ; positifs 12/15 ; LOO classique
9/14. C3 reste levée (§8.71, GSE60979) — ce lot ne la re-teste
pas, il ne la touche pas. Les trois blocs de co-expression
(estomac/mucus, immunitaire, réparation ADN), l'effet PRMT5 qui
suit MTAP et non CDKN2A, et les résultats cliniques
(daraxonrasib, vopimetostat + daraxonrasib, IBI343) ne sont pas
touchés par ce lot. **Aucun remède** : ce lot juge la position
des réels dans leurs distributions de nuls, il ne teste aucun
traitement et ne change rien à ce qui est un remède candidat.

**Formulation.** Tous les verdicts de cette section sont des
verdicts d'analyse (ce que les données montrent), jamais des
prédictions — correction de Zackary du 21 novembre 2026, 12h03
(§8.98.1).

## 8.98.7 Limites et dettes

- **Dette SHA-256 (nommée).** La vérification des artefacts E2
  et run #2 contre les digests GitHub a été impossible : l'API
  GitHub a répondu 403 (limite de requêtes non authentifiées).
  Vérifié à la place : run #3 bit-à-bit 6/6 ; E2 tailles exactes
  57/57 et intégrité zip 57/57 ; run #2 : 209 artefacts distincts
  au total, 210 fichiers testés, 0 corrompu. La vérification SHA
  contre les digests est à refaire à la prochaine occasion, tant
  que les artefacts sont sur GitHub (~29 nov., rétention 7 jours).
  Les 3000 `master_results.json` lus sont complets et lisibles ;
  un artefact corrompu aurait été détecté à l'extraction ou à la
  lecture, mais la preuve bit-à-bit manque pour 203 des 209
  artefacts.
- **Distribution = nuls pipeline seulement.** La réplique de
  1000 permutations du §8.93 n'a pas été refaite ici. Les deux
  lectures coexistent (réplique : 5/15 SOLIDES ; 200 nuls
  pipeline : 6/15) ; elles ne se remplacent pas. Le p95 à 200
  tirages porte une incertitude d'échantillonnage (voir §8.98.5).
- **ICGC passe la barre de justesse.** 95,5 % sous le plancher,
  soit 191/200 nuls, seuil 190/200 : un seul nul de marge. Son
  réel est au-dessus des 200 nuls (rang 201/201) mais 9 nuls sont
  à moins de 0,07 du réel. ICGC est le plus fragile des six
  SOLIDES ; le classer SOLIDE dit où il tombe contre 200 nuls,
  pas qu'il est hors d'atteinte d'un nul supplémentaire.
- **GSE62452 et GSE71729 sous le plancher de justesse en d vs
  médiane** (0,0685 et 0,0677 contre 0,07) : leur réel est
  au-dessus de la médiane, mais l'écart n'atteint pas le plancher
  gelé. Ils restent NON, et de peu en d, de loin en % sous
  plancher (48,5 % et 45,5 %).
- **GSE194249, réel à peine au-dessus de la médiane** (110/200
  nuls sous le réel, d 0,0062) : le réel est au milieu de sa
  distribution de nuls, comme en réplique (rang 573/1001 au
  §8.93). Rien ne le distingue d'un tirage de nul.
- **GDC ORGANOID, réel sous le p95 malgré 170/200 nuls sous le
  réel** : être au-dessus de 85 % des nuls ne suffit pas quand le
  p95 est au-dessus du réel (0,2778 contre 0,2542) et que seuls
  24,0 % des nuls sont sous le plancher.
- **Les nuls sont des permutations par ligne** : ils brisent la
  structure ordonnée, pas les marginales — c'est le nul du projet
  depuis §8.31, pas un nul biologique.
- **Les verdicts SOLIDE / FRAGILE / NON décrivent la position
  du réel dans la distribution des nuls observée** ; ils ne
  prédisent rien sur un futur échantillon (correction du 21 nov.
  2026, §8.98.1).

## 8.98.8 Provenance

Protocole : le lot est une PROPOSITION, pas un fait du protocole
gelé §8.93 (`PROTOCOL_nulls_distribution_893.md`, SHA d'origine
`d2cdbc3d589d3be61a506f7be2a250d3d4a1c9adc21d1327c8ffc7a61f6529a0`) —
le protocole gelé valide par 10 nuls frais par paire et ne
définit pas de lot suivant. Registre du lot :
`nulls_lot_next/LEDGER.md` (SHA
`2983cf0f545d7e637f9cee8cf9d8400f6b8fd25d70457798290470859e7a9eb1`,
2989 lignes, sections de suivi du 22–23 nov. 2026) et
`nulls_lot_next/ledger.csv` (SHA
`10669164ef4fb325939f0cd3701568f482df10c5bd7c7f77b850bbd0766bed69`,
2851 lignes avec en-tête, 2850 lignes de runs, statut
« telecharge » ; sauvegarde
`ledger_avant_telechargement.csv`).

Pipeline : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(624 157 octets), vérifié inchangé en début et en fin de lot
local. v6.1 (référence) SHA `2af5e5ce…`, v6 SHA `bb8bbdba…`.

Scripts : `nulls_lot_next/scripts/build_null_893.py` (SHA-256
`572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467` ;
`default_rng(graine)`, permutation des lignes entières, colonne
de contrôle inchangée ; validé bit-à-bit le 22 nov. 2026 : TCGA
v4 graine 9101 reproduit le nul du lot §8.93, SHA
`22f39bf7b6ed0efc4c065347de94ef829e50f1e1df7afb9677686061c005e8fa`) ;
`nulls_lot_next/analyse_lot_next.py` (SHA-256
`c8d7d23fc57bc54411366cefe209f9d2dc8060377764ba7dbf0007eca3f3ca05` ;
lit maxsep dans `master_results.json` au chemin
`run_pipeline.threshold_metadata.threshold_optimization.
best_config.metrics.max_separation`, réels repris de
`nulls_dist_893_table.json` sans re-saisie, dossiers lus dans
`ledger.csv`, verdicts par `juger()` = règle gelée §8.93 §4,
quantiles par interpolation linéaire, valeurs arrondies à 4
décimales) ; lanceur local `run_nulls_parallel.sh` (`xargs -P
2`) ; lanceur GitHub : workflows
`pipeline-nulls-lot.yml` (commit `0511dae`),
`pipeline-nulls-lot-rerun.yml` (commit `05cf9b8`),
`pipeline-nulls-lot-e2.yml` (commit `0dba356`), dépôt
FindPrint/tlogNext-pipeline-actions.

Runs GitHub : run #2 45056686992 (152 jobs, 146 succès, 6 hp35
annulés à la limite 2 h — blocs 2, 5, 7, 8, 14, 17 — 0 échec,
146 artefacts, conclusion « cancelled », fin 22 nov. 19h13
EST) ; relance #3 45087899473 (6/6, 60 runs HP35, conclusion
« success », fin 22 nov. 22h20 EST) ; run E2 45170178139 (57/57,
conclusion « success », fin 23 nov. ~08h35 EST). Données brutes
des jobs et artefacts du run #2 :
`goals/pdac-pseudo-time-validation-tlog28-cancer-project/
hidden_files/runs/pdac-v6/nulls_lot_next/gha2_jobs_p1.json`,
`gha2_jobs_p2.json`, `gha2_artifacts.json`.

Runs locaux : unité systemd `v62-nulls-next-local`, 760/760,
bilan ok=9, sautés=751, échecs=0, fin 23 nov. 07h06 EST
(12:06:55 UTC) ; log `runs_nulls_parallel_jobs-jobs_local_e2.log`.

Sorties (SHA-256) : `nulls_lot_next/nulls_lot_next_table.json`
`351d929c8a923f678a9c6658dc359fd4b0c66d468386e8a80561ac87ce488565`
(6179 octets) ; `nulls_lot_next/nulls_lot_next_table.csv`
`80b2cf14624f30b0332a176573ed5efbb55fd38909a06730bbb783428c75e0ac`
(1450 octets). Réels repris de `nulls_dist_893_table.json` (SHA
`3ce39accab00dae86e713794bc683e8d9f550e8b22a660576837b67f5dad27fd`).

Téléchargement : 23 nov. 2026, 08h37–09h20, via le navigateur,
209 artefacts (146 run #2 + 6 run #3 + 57 run E2) ; vérification
run #3 SHA-256 bit-à-bit 6/6 contre les digests GitHub ; E2
tailles exactes 57/57 et intégrité zip 57/57 ; run #2 : 209
artefacts distincts, 210 fichiers testés, 0 corrompu. Dette :
vérification SHA-256 E2/run #2 contre les digests GitHub
impossible (API GitHub 403, limite de requêtes non
authentifiées) — à refaire ; artefacts sur GitHub jusqu'à ~29
nov. (rétention 7 jours).

Ce qui manque : la vérification SHA-256 bit-à-bit de 203 des 209
artefacts contre les digests GitHub (dette ci-dessus) ; la
réplique de 1000 permutations n'a pas été refaite pour ce lot
(§8.98.7). Aucune recommandation clinique.
