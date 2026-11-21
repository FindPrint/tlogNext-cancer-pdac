### 8.75 Clôture du résidu M2 du §8.63 — la réplication tient, le taux est 80 %, pas 85 % (20–21 novembre 2026)

Go de Zackary « Les 3 allez s'y » (20 nov. 2026 18h04, 3e des 3
pistes du lot du 20 nov. — clôture du résidu M2 du §8.63,
protocole gelé avant tout nouveau script et tout nouveau run).

**Verdict d'abord, en trois phrases. (a) TRANCHÉ–CONFIRMÉ — la
réplication hors échantillon de M2 tient : le lot A (30 nuls ICGC
frais s61–s90) donne X = 24/30 (80,0 %) qui choisissent
(35, 16, 6), au-dessus du seuil gelé de 21, et le lot B (10 nuls
GSE62452 frais s31–s40) donne Y = 9/10 (90,0 %) qui choisissent
(34, 16, 6), au-dessus du seuil gelé de 7 — les deux critères
gelés sont appliqués tels quels, H_A est retenue et H_B est
rejetée. (b) Le taux stabilisé est 80 %, pas 85 % : sur 80 nuls
frais ICGC (s11–s90), 64/80 = 80,0 %, intervalle de Wilson 95 %
[0,700 ; 0,873], test binomial exact unilatéral vs p = 0,85 :
p = 0,138 ; le 85 % de §8.53 (17/20) était un tirage haut
ordinaire sur n = 20 (P(X ≥ 17 | p = 0,80) = 0,41) et le 6/10
de §8.63 un tirage bas ordinaire sur n = 10 (P(X ≤ 6 | p = 0,80)
= 0,12) — les deux sont compatibles avec un taux vrai de 80 %.
(c) L'attribution des écarts confirme le mécanisme : 5 des 7
écarts totaux sont des basculements de robustesse (sans le terme
de robustesse, la config réelle aurait gagné), les 2 autres sont
des quasi-ex-aequo purs (marges 0,0002 et 0,0009, rob = 0 des
deux côtés) — M2 global passe de PARTIELLEMENT EXPLIQUÉ à
EXPLIQUÉ (M2a et M2b expliqués, M2d confirme) ; le résidu
« pourquoi la robustesse bascule sur telle permutation » reste
renvoyé au §8.73 (NON ÉLUCIDÉ), non rouvert ici.**

## 8.75.1 Question, méthode, règles

**Question.** §8.63 a expliqué M2a (ensemble des 12 configs fixe
par n) et M2b (petit w + grille fine gagne) mais a laissé M2d
INDÉCIS : 6/10 nuls frais ICGC s31–s40 choisissent (35, 16, 6),
P(X ≤ 6 | p = 0,85) = 0,050, à la frontière. Le taux de §8.53
(17/20 = 85 %) ne se reproduisait pas à l'identique, il se
tassait (23/30 = 76,7 % sur s11–s40). La réplication
tient-elle avec un échantillon plus large ET un critère gelé
d'avance ?

**Méthode.** Protocole gelé `PROTOCOL_m2_cloture_875.md` (SHA
`f829fd77fa5c938891814cbd7c80ef229a2dc3cd14f51b30d8babdd1e771d89c`,
écrit avant tout nouveau script, toute nouvelle construction et
tout nouveau run). Trois volets, dans l'ordre : (A) construction
de 40 nuls frais, même méthode que §8.53/§8.63
(`default_rng(graine)`, `permutation(n)`, lignes entières,
colonne `step` inchangée) — ICGC graines 61–90, GSE62452
graines 31–40, jamais utilisées ; (B) deux lots v6.2 fast,
40 runs, via `systemd-run` + surveillance ; (C) extraction
des `all_results` (12 configs par run) avec recomposition du
MC vérifiée à 10⁻⁶, comptages gelés, attribution des écarts
par MC sans robustesse (définition gelée §2 E).

**Mécanique (lue dans le code v6.2, pas devinée — rappel §8.63).**
MC = 0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·acuité,
s_norm = tanh(maxsep/2), rob = exp(−((FWHM − 10)²)/(2·5²)).
L'optimiseur échantillonne 12 configs en mode fast avec
`rng = default_rng(42 + itération)` — l'ensemble des 12 configs
ne dépend que de n, pas des données. La « config réelle » est le
point de grille petit-w + fine-grille qui maximise le max :
ICGC (35, 16, 6), GSE62452 (34, 16, 6).

**Hypothèses nommées d'avance (protocole §2).** **H_A**
(réplication tient) : taux stable ~75–85 %, propriété de
grille ; le 85 % de §8.53 n'était pas un tirage haut, le 6/10
de §8.63 la fluctuation d'un petit échantillon. **H_B**
(réplication ne tient pas) : le 85 % était un tirage haut, le
taux réel est ≤ 60 %, dominé par les basculements de
robustesse. **H_0** (quasi-ex-aequo instable) : taux
intermédiaire ~65–75 %, marges ~0,003, étiquette instable.

**Règles de décision écrites avant (protocole §4).** Lot A
(n = 30) : CONFIRME si X ≥ 21, INFIRME si X ≤ 12, INDÉCIS si
13–20 (mêmes seuils proportionnels que M2d au §8.63 : ≥ 7/10
et ≤ 4/10 ; P(X ≤ 20 | p = 0,85) = 0,0097 ; P(X ≤ 12) <
0,0001). Lot B (n = 10) : CONFIRME si Y ≥ 7, INFIRME si
Y ≤ 4, INDÉCIS si 5–6 (reprise exacte de M2d au §8.63 ;
P(Y ≤ 6 | p = 0,85) = 0,0500 ; P(Y ≤ 4) = 0,0014). Verdict
global : TRANCHÉ–CONFIRMÉ si A CONFIRME et B n'INFIRME pas ;
TRANCHÉ–INFIRMÉ si A INFIRME ; TRANCHÉ–DIVERGENT si A
CONFIRME et B INFIRME ; FERMÉ COMME NON CONCLUANT si A
INDÉCIS. Le poolé (80 ICGC, 30 GSE) et l'attribution des
écarts sont des lectures secondaires, hors critère.

**Faits de départ (relus, jamais des verdicts réimportés).**
Baseline connue avant ce chantier : nuls frais ICGC s11–s60,
40/50 = 80,0 %, Wilson [0,670 ; 0,888], p vs 0,85 = 0,209 ;
nuls frais GSE62452 s11–s30, 17/20 = 85,0 %, Wilson
[0,640 ; 0,948], p vs 0,85 = 0,595. Ces nombres sont la
baseline DÉCLARÉE, pas le critère : le critère porte sur le
lot NEUF seul, dont le résultat était inconnu à l'écriture
du protocole.

## 8.75.2 Lot A — réplication ICGC : 24/30, CONFIRME

Lot v6.2 fast terminé le 21 nov. 2026 à 00:50:42Z (unité systemd
`v62-875-watch`, 30 runs ICGC s61–s90 ; **30/30 exit 0, 0
échec** — dont une reprise après redémarrage machine vers
23:21Z : les 5 runs s61–s65 déjà terminés ont été sautés,
le dossier partiel vide de s66 a été supprimé et le run
relancé tel quel, sans changer de graine, comme au §8.73 ;
SHA v6.2 vérifié avant le lot, avant la relance et après le
lot : `f07567c4…ec3abf`).

**X = 24/30 (80,0 %) choisissent (35, 16, 6) — CONFIRME**
(seuil gelé : ≥ 21). Intervalle de Wilson 95 % sur le lot
neuf seul : [0,627 ; 0,905] ; test binomial exact unilatéral
vs p = 0,85 : p = 0,289 (0,85 non rejeté). MC gagnant sur le
lot : min 0,3201, médiane 0,3403, max 0,4965. Marges
vainqueur–2e : médiane 0,0024, min 0,0002, max 0,0170 ;
23/30 < 0,005, 27/30 < 0,01 — le choix reste un
quasi-ex-aequo, au même niveau qu'au §8.63 (médiane 0,0029).

Les 6 écarts (gagnante ≠ (35, 16, 6)) :

| Run | Gagnante | MC / rob / maxsep | Marge | Config réelle (35, 16, 6) : MC / rob / maxsep | MC_sans_rob réelle vs gagnante | Classe gelée |
|---|---|---|---|---|---|---|
| s61 | (17, 34, 5) | 0,3598 / 0,2163 / 0,1553 | 0,0170 | 0,3429 / 0,0257 / 0,2751 | 0,4222 > 0,3957 | basculement de robustesse |
| s63 | (22, 16, 7) | 0,3298 / 0,0000 / 0,2058 | 0,0002 | 0,3297 / 0,0000 / 0,2075 | 0,4121 < 0,4123 | autre (quasi-ex-aequo) |
| s66 | (22, 16, 7) | 0,3767 / 0,1945 / 0,2903 | 0,0149 | 0,3619 / 0,1062 / 0,2942 | 0,4258 > 0,4223 | basculement de robustesse |
| s69 | (17, 34, 5) | 0,4965 / 0,8825 / 0,1886 | 0,0087 | 0,3710 / 0,1062 / 0,3554 | 0,4372 > 0,4000 | basculement de robustesse |
| s75 | (11, 15, 6) | 0,3606 / 0,1353 / 0,3299 | 0,0160 | 0,3447 / 0,0000 / 0,3236 | 0,4309 > 0,4170 | basculement de robustesse |
| s86 | (22, 16, 7) | 0,3326 / 0,0000 / 0,2291 | 0,0009 | 0,3317 / 0,0000 / 0,2293 | 0,4147 < 0,4158 | autre (quasi-ex-aequo) |

Lecture des écarts (descriptive, hors critère gelé). Dans les
4 basculements, la gagnante a une robustesse nettement
supérieure à celle de la config réelle (0,1353–0,8825 contre
0,0000–0,1062) et gagne grâce à elle : sans le terme de
robustesse, la config réelle l'emporterait dans les 4 cas.
Le cas s69 est le plus net : MC 0,4965, le plus haut du lot,
porté par rob 0,8825 alors que son maxsep (0,1886) est
presque deux fois plus bas que celui de la config réelle
(0,3554) — le même phénomène que M1a au §8.63 (un pic
étroit allume la robustesse), sur un nul frais, sans que la
cause du pic soit recherchée ici (§8.73, clos). Le cas s61
est du même type à plus petite échelle (maxsep 0,1553 contre
0,2751 pour la config réelle). Dans les 2 autres écarts
(s63, s86), la robustesse est nulle des deux côtés et la
marge est de 0,0002 et 0,0009 : un quasi-ex-aequo pur, sans
interrupteur — la config réelle y perd de 2 et 9
dix-millièmes. Dans les 6 cas, le MC de la config réelle
(0,3297–0,3710) est dans la plage normale des MC gagnants
du lot (min 0,3201) : la config réelle ne « rate » rien, la
gagnante la dépasse, par la robustesse ou par un cheveu.

Courbes rob-on sur le lot A : 10/360 courbes rob > 0,1,
2/360 rob > 0,5 ; 4 gagnantes rob-on sur 30 (s61, s66, s69,
s75 — exactement les 4 basculements). À comparer au lot
frais du §8.73 (3/240 rob > 0,1, 0/240 rob > 0,5,
0 gagnante rob-on sur 20) et au corpus §8.63 (25/996
courbes rob-on, 2,51 %, et 11/83 gagnantes rob-on, 13,25 %) :
le taux de ce lot (2,78 % des courbes, 13,3 % des gagnantes)
est dans la ligne du corpus, pas une anomalie.

## 8.75.3 Lot B — réplication GSE62452 : 9/10, CONFIRME

Lot v6.2 fast terminé le 21 nov. 2026 à 00:50:42Z (même unité
`v62-875-watch`, 10 runs GSE62452 s31–s40 ; **10/10 exit 0,
0 échec** ; SHA v6.2 vérifié avant et après : `f07567c4…ec3abf`).

**Y = 9/10 (90,0 %) choisissent (34, 16, 6) — CONFIRME**
(seuil gelé : ≥ 7). Intervalle de Wilson 95 % sur le lot
neuf seul : [0,596 ; 0,982] ; test binomial exact unilatéral
vs p = 0,85 : p = 0,803. MC gagnant sur le lot : min 0,3271,
médiane 0,3442, max 0,4875. Marges vainqueur–2e : médiane
0,0053, min 0,0012, max 0,0708 ; 4/10 < 0,005, 9/10 < 0,01.

Le seul écart, s32 : gagnante (22, 16, 7), MC 0,4875,
rob 0,6926, maxsep 0,4261, marge 0,0708 — la plus grosse
marge des deux lots neufs. Config réelle (34, 16, 6) :
MC 0,4167, rob 0,2621, maxsep 0,4638. MC_sans_rob :
réelle 0,4554 > gagnante 0,4362 — **basculement de
robustesse** (définition gelée §2 E). Ici la gagnante a
aussi un maxsep élevé (0,4261) : le basculement n'est pas
un pic sur une courbe faible, c'est un boost de robustesse
sur une courbe déjà forte. Courbes rob-on sur le lot B :
3/120 rob > 0,1, 1/120 rob > 0,5 ; 1 gagnante rob-on sur
10 (s32).

## 8.75.4 Taux poolés — 80 % stabilisé, pas 85 %

| Corpus | k / n | Taux | Wilson 95 % | p vs 0,85 (unilatéral) |
|---|---|---|---|---|
| ICGC frais, baseline s11–s60 (§8.53+§8.63+§8.73) | 40 / 50 | 80,0 % | [0,670 ; 0,888] | 0,209 |
| ICGC frais, lot neuf s61–s90 (§8.75) | 24 / 30 | 80,0 % | [0,627 ; 0,905] | 0,289 |
| **ICGC frais, poolé s11–s90** | **64 / 80** | **80,0 %** | **[0,700 ; 0,873]** | **0,138** |
| GSE frais, baseline s11–s30 (§8.53) | 17 / 20 | 85,0 % | [0,640 ; 0,948] | 0,595 |
| GSE frais, lot neuf s31–s40 (§8.75) | 9 / 10 | 90,0 % | [0,596 ; 0,982] | 0,803 |
| **GSE frais, poolé s11–s40** | **26 / 30** | **86,7 %** | **[0,703 ; 0,947]** | **0,678** |

Le lot neuf ICGC reproduit le taux de la baseline à
l'identique (24/30 = 80,0 % contre 40/50 = 80,0 %) : le
poolé reste à 80,0 % exactement, avec un intervalle qui se
resserre ([0,700 ; 0,873] contre [0,670 ; 0,888] à n = 50).
Les deux anciens tirages sont compatibles avec un taux vrai
de 80 % : P(X ≥ 17 | n = 20, p = 0,80) = 0,41 (§8.53) et
P(X ≤ 6 | n = 10, p = 0,80) = 0,12 (§8.63) — le 85 % était
un tirage haut ordinaire, le 6/10 un tirage bas ordinaire.
Le taux 85 % du §8.53 est donc révisé : l'estimation
stabilisée sur 80 tirages est **80 %**, et l'intervalle
[0,700 ; 0,873] inclut 0,85 sans le centrer. Côté GSE, le
poolé est à 86,7 % (26/30), Wilson [0,703 ; 0,947] — la
réplication y est, elle aussi, confirmée, avec un taux
légèrement supérieur à l'ICGC, sans que l'écart entre
cohortes (80,0 % contre 86,7 %) soit significatif sur ces
effectifs (écart 6,7 points, intervalles largement
chevauchants).

**H_A est retenue** (taux stable ~75–85 %, propriété de
grille) ; **H_B est rejetée** (taux ≤ 60 % : l'intervalle
poolé ICGC [0,700 ; 0,873] exclut 0,60) ; **H_0 est
partiellement retenue** : le taux n'est pas dans la zone
65–75 % qu'elle prévoyait, mais sa seconde moitié tient —
les marges médianes (~0,002–0,005) confirment le
quasi-ex-aequo, et 5 écarts sur 7 viennent d'un basculement
de robustesse.

## 8.75.5 Attribution des écarts — 5 basculements sur 7

Sur les 40 runs neufs, 7 écarts au total (6 ICGC + 1 GSE).
Par la définition gelée (§2 E, MC_sans_rob =
(MC − 0,2·rob)/0,8) :

- **5 basculements de robustesse** : ICGC s61, s66, s69,
  s75 ; GSE s32. Dans les 5 cas, MC_sans_rob(config réelle)
  > MC_sans_rob(gagnante) et rob(gagnante) > 0,1. Sans le
  terme de robustesse, la config réelle aurait gagné ces
  5 runs.
- **2 autres** : ICGC s63 et s86, marges 0,0002 et 0,0009,
  rob = 0 des deux côtés, MC_sans_rob(gagnante) >
  MC_sans_rob(réelle) de 0,0002 et 0,0011 — des
  quasi-ex-aequo sans interrupteur.

Lecture descriptive (hors critère gelé, même runs, même
définition) : sur le MC sans robustesse, la config réelle
gagnerait 28/30 en ICGC et 10/10 en GSE, soit **38/40
(95,0 %)**. Le biais de grille seul (M2b : petit w +
grille fine) porte donc le choix de la config réelle à
~95 % ; c'est le terme de robustesse — l'interrupteur de
forme de courbe du §8.63 — qui le ramène à ~80 % en
renversant 5 runs sur 40. Cette lecture ne change pas le
critère (le MC du pipeline inclut la robustesse, et c'est
lui qui est compté) : elle quantifie la part de chaque
terme dans le taux observé. Elle ne rouvre pas la question
du déclencheur du pic (§8.73, NON ÉLUCIDÉ) : elle dit
seulement que, quand le pic est là, il renverse le choix,
et que sans lui le choix serait presque unanime.

M2a est re-confirmé sur le corpus élargi : **1 seul
ensemble distinct de 12 configs** par cohorte, sur 80 runs
ICGC et 30 runs GSE62452 lus (dont les 40 neufs) — le code
le garantit (`rng = default_rng(42 + itération)`), la
lecture le confirme.

## 8.75.6 Ce que ça change, et ce que ça ne change pas

**Change.** (1) M2d n'est plus indécis : la réplication hors
échantillon tient sur 30 tirages frais ICGC et 10 tirages
frais GSE62452, avec des critères gelés appliqués tels quels.
**M2 global = EXPLIQUÉ** (M2a et M2b expliqués au §8.63, M2d
confirme ici) — le résidu ouvert du §8.63 est clos. (2) Le
taux de choix de la config réelle est révisé : **80 %** sur
80 tirages ICGC, pas 85 % — le 85 % de §8.53 était le taux
d'un échantillon de 20, pas la valeur du mécanisme. Toute
lecture ultérieure qui citerait « 85 % » comme taux de
réplication doit être corrigée en « 80 % (64/80, Wilson
[0,700 ; 0,873]) ». (3) La part des termes est quantifiée :
sans le terme de robustesse, la config réelle gagnerait
38/40 (95,0 %) ; avec lui, 33/40 (82,5 %) sur les lots
neufs — la robustesse est le seul terme qui fait dévier le
choix de façon systématique, les autres écarts étant des
quasi-ex-aequo de l'ordre du dix-millième. (4) Le cas s69
(MC 0,4965 porté par rob 0,8825 avec un maxsep deux fois
plus bas que la config réelle) est un nouvel exemple frais
du phénomène M1a : la robustesse peut faire gagner une
config au maxsep faible — un rappel que le MC n'est pas
une mesure de séparation, et que maxsep, score principal
adopté pleinement le 20 nov., doit rester la lecture
première.

**Ne change pas.** Aucun verdict de séparation n'est touché :
S_sep sépare toujours sur la série MTAP (§8.50), le réel
ICGC reste sous le plancher n≈70 (§8.53), le rationnel
vopimetostat + daraxonrasib n'est ni renforcé ni affaibli.
La marche de niveau multi-flux (§8.46) vit dans les CSV,
pas dans ces mécanismes. M1 reste expliqué tel qu'au §8.63.
Le mécanisme « pourquoi telle permutation a un pic étroit »
reste ouvert et renvoyé au §8.73 (NON ÉLUCIDÉ) : ce
chantier compte les basculements, il n'en cherche pas la
cause. La mise en garde du §8.63.8 (Delta comparé à w égal)
n'est pas modifiée.

## 8.75.7 Méthode

Protocole gelé avant tout nouveau script et tout nouveau run :
`PROTOCOL_m2_cloture_875.md`, SHA
`f829fd77fa5c938891814cbd7c80ef229a2dc3cd14f51b30d8babdd1e771d89c`.
**(A)** `build_nulls_icgc_gse_875.py` (SHA
`0de249cd872640ac7828b82b98973e6c18b83a95e929822c0174bbc734390575`) :
40 nuls frais, entrées vérifiées par SHA avant construction
(ICGC réel `10823879…388adc`, GSE62452 réel `97c4689a…ffd79a3`,
relus dans `nulls_n70_853_verify.json`, re-vérifiés ici) ;
sorties `nulls_icgc_gse_875_files.json` (40 SHA). **(B)** Lots
v6.2 : `run_v62_875.sh` (SHA
`212221560a451a949ba3c3bd5f6757ae807f8ed12fbca3ab5f3713897c7c7365`),
manifeste `manifest_v62_875.txt`, unité systemd
`v62-875-watch`, surveillance `watch_v62_875.sh` (SHA
`bbd7b4b76de87cdf23c1f026d0865fa3cb24e81265768879a1c8325a9f07f842`).
Journal `runs_v62_875.log` : lancement 20 nov. 2026
23:08:47Z (SHA v6.2 `f07567c4…ec3abf`) ; redémarrage machine
vers 23:21Z (uptime 0 min constaté à 23:24:44Z, unité
transiente perdue, 5 runs terminés intacts s61–s65) ;
reprise 23:24:55Z après vérification qu'aucun processus de
lot ne tournait, suppression du dossier partiel vide de
s66 (aucun `master_results.json`, comme au §8.73 pour s52)
et SHA v6.2 re-vérifié avant relance ; FIN 21 nov. 2026
00:50:42Z, deja_faits=5, termines=35, echecs=0 — **40/40
exit 0, 0 échec**, surveillance `WATCH 875 TERMINE 40/40`
à 00:51:02Z (tour 2). SHA v6.2 vérifié après le lot :
`f07567c4…ec3abf`, inchangé. **(C)** `m2_cloture_875.py`
(SHA `0deac752d372588384ebc23116f2bce88e0cb1faa9003e898a7eda70f6ddd90e`) :
lecture des `all_results` de 110 runs (80 ICGC + 30 GSE),
recomposition du MC et de rob vérifiées à **0,00e+00**
(1320 configs, 0 manquant) — voir §8.75.9 pour la
correction d'une erreur de transcription détectée par ce
contrôle. Sorties : `m2_cloture_875_extract.json` (SHA
`f94964cd75d4d8fb723e8751b0669984b780acf1b8cf2e900fe2c8a7296d9e48`),
`m2_cloture_875_results.csv` (SHA
`4cc0cdf5406654e1091fd58917fbb901a69fdd5b2d03faee8ce697334a811857`).

## 8.75.8 Limites

- Mode fast seulement : 12 configs par run. Les nombres
  (taux de choix, marges) sont propres au mode fast ; le
  mécanisme de grille fixe reste le même en nature dans les
  autres modes (graine fixe + itération), mais les taux
  pourraient différer.
- Le lot A (n = 30) tranche entre un taux ~0,85 et un taux
  ~0,60–0,70, pas entre 0,85 et 0,80 : avec un taux vrai de
  0,80, le lot A CONFIRME (X = 24 ≥ 21) tout en restant
  compatible avec un tassement — c'est pourquoi le taux
  poolé sur 80 nuls et son intervalle de Wilson sont
  rapportés, et pourquoi la révision 85 % → 80 % fait
  partie du verdict, pas d'une note.
- La baseline poolée 40/50 était connue avant le lot : le
  critère primaire porte sur le lot NEUF seul (X), jamais
  sur le poolé — le poolé est une lecture secondaire, et sa
  stabilité à 80,0 % exactement est une coïncidence
  arithmétique (40/50 puis 24/30), pas une propriété
  attendue.
- L'attribution des écarts (§8.75.5) mesure le rôle du
  terme de robustesse dans l'ordre des configs, pas la
  cause du pic : elle ne rouvre pas le §8.73. La lecture
  « 38/40 sans robustesse » est descriptive, sur les mêmes
  runs, pas un nouveau critère.
- n = 70 (ICGC) et 69 (GSE62452) ; un seul contrôle
  (`step`) ; aucune donnée nouvelle hors des CSV déjà sur
  disque et des 40 nuls frais ; aucun test direct ; aucun
  verdict biologique.

## 8.75.9 Provenance

- **Protocole gelé.** `PROTOCOL_m2_cloture_875.md` (SHA-256
  `f829fd77fa5c938891814cbd7c80ef229a2dc3cd14f51b30d8babdd1e771d89c`),
  écrit avant tout nouveau script, toute nouvelle construction
  et tout nouveau run de ce chantier.
- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant le lot, avant la relance après redémarrage
  machine et après le lot). Scripts neufs :
  `build_nulls_icgc_gse_875.py` (SHA-256
  `0de249cd872640ac7828b82b98973e6c18b83a95e929822c0174bbc734390575`),
  `run_v62_875.sh` (SHA-256
  `212221560a451a949ba3c3bd5f6757ae807f8ed12fbca3ab5f3713897c7c7365`),
  `watch_v62_875.sh` (SHA-256
  `bbd7b4b76de87cdf23c1f026d0865fa3cb24e81265768879a1c8325a9f07f842`),
  `m2_cloture_875.py` (SHA-256
  `0deac752d372588384ebc23116f2bce88e0cb1faa9003e898a7eda70f6ddd90e`).
- **Correction documentée (erreur de transcription, détectée
  par le contrôle croisé).** La première version de
  `m2_cloture_875.py` copiait `fwhm_rob_from_curve` de
  `mechanisms_863.py` avec une erreur d'un pas dans la boucle
  gauche (`scores[left - 1]` au lieu de `scores[left]`) :
  la recomposition de rob échouait alors sur 15/70 runs
  existants (écart max 0,87), alors que §8.63 trouvait
  0 run en écart. L'écart avec §8.63 a déclenché la
  comparaison caractère par caractère, la correction à la
  copie verbatim, et la re-vérification : rob reproduite à
  0,00e+00 sur les 1320 configs des 110 runs lus. La
  recomposition du MC, elle, était exacte à 0,00e+00 dès
  la première version (840 configs) : les comptages de
  base (40/50, 17/20) n'ont jamais dépendu de la fonction
  fautive. La version corrigée est celle dont le SHA est
  noté ci-dessus ; l'erreur et sa détection sont consignées
  ici, pas effacées.
- **Entrées (SHA-256 vérifiés).** ICGC réel
  `10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc`
  ; GSE62452 réel
  `97c4689a6ecacd0a73a77804200a72a90994d60bea7e6b2c079195acbffd79a3`
  (provenances complètes : `PROVENANCE_immune_v6.md`,
  `PROVENANCE_icgc.md`, `PROVENANCE_geo62452.md`). Nuls
  frais §8.75 : ICGC s61–s90, GSE62452 s31–s40, SHA dans
  `nulls_icgc_gse_875_files.json` (SHA-256
  `40ac6212e7f03871013fb61980ceada9a5b4baedc2201d4ca4b7f3840c57404b`)
  ; détail dans `PROVENANCE_875.md` (SHA-256
  `4070c421e3e568c92d80c7c43f5352d7d6d2e850bd2db9485ced583b8f629fd5`).
  Nuls existants relus : ICGC s11–s30 (§8.53), s31–s40
  (§8.63), s41–s60 (§8.73) ; GSE62452 s11–s30 (§8.53).
- **Sorties.** `manifest_v62_875.txt` (SHA-256
  `a8f815b6af93241ab9fcd7c196bca31df9343609c2b113da9f070a1ff2f8c413`),
  `runs_v62_875.log` (40/40, exit 0), `watch_v62_875.log`,
  dossiers `results_fast_v62_875_icgc_nul_s61/` … `s90/` et
  `results_fast_v62_875_geo62452_nul_s31/` … `s40/`,
  `m2_cloture_875_extract.json`,
  `m2_cloture_875_results.csv`.
- **Faits de départ.** `section_8.63_mechanisms.md`
  (protocole `PROTOCOL_mechanisms_863.md` SHA
  `4e05dfc2…f35e`) et `section_8.73_pic_etroit.md`
  (protocole `PROTOCOL_pic_etroit_873.md` SHA
  `28d2326c…51a4c`) — relus, jamais réimportés comme
  verdicts.
- **Nature des lignes.** Résidus d'expression ARN bulk
  ordonnés (mesures instrumentales transformées) ; flux
  immunitaires (ARN bulk) ; nuls = lignes permutées
  (échantillons hypothétiques, pas des mesures) ; aucune
  autre donnée nouvelle dans ce chantier.
- **Ce qui manque, ce qui reste ouvert.** Le déclencheur du
  pic étroit par permutation (§8.73, NON ÉLUCIDÉ) ; les
  modes autres que fast (12 configs) ; PDF non régénéré,
  rien poussé sur GitHub (hors de ce chantier).

— Fin de la §8.75. —
