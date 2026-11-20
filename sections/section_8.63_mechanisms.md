### 8.63 Mécanismes non élucidés §8.50 / §8.53 — deux mécanismes sur trois expliqués, le troisième partiel (20 novembre 2026)

**Verdict d'abord, en trois phrases. (a) M1 EXPLIQUÉ — la configuration
(28, 27, 6) ne cause ni le MC haut ni le Delta bas : le MC haut est une
propriété de la permutation (un pic étroit de la courbe de scan, FWHM
≈ 11–15 %, qui allume la robustesse sous (28, 27, 6) comme sous
(93, 30, 6) — MC 0,5143 contre 0,5192 sur s11111), et le Delta bas est
une propriété de w = 27 (à w = 30, s11111 et s123 retrouvent Delta
3,83 et 3,85, soit le niveau du réel 3,81 ; à w = 27, le RÉEL lui-même
tombe à 3,09). (b) M2 PARTIELLEMENT EXPLIQUÉ — l'optimiseur ne
« reconnaît » rien du réel : il maximise le MC sur 12 configs FIXES
par n (graine 42 + itération, indépendantes des données), et la
« config réelle » n'est que le point de grille qui maximise le max —
petit w (maxsep moyen anti-corrélé à w, Spearman −0,99) et grille fine
(stabilité croissante avec n_candidates, Spearman +0,80) — avec des
marges vainqueur–2e médianes de 0,003, un quasi-ex-aequo ; mais la
réplication hors échantillon est INDÉCISE (6/10 nuls frais s31–s40
choisissent (35, 16, 6), P(X ≤ 6 | p = 0,85) = 0,050), les 4 écarts
venant tous d'un basculement de robustesse. (c) Les deux phénomènes
de M1 sont deux conséquences INDÉPENDANTES du même tirage d'ordre :
aucun flux ne porte le pic (part maximale 0,25), le nul 42 est rob-on
avec un Delta HAUT (4,35), et à w fixé il ne reste aucun écart de
d_div entre s11111/s123 et le réel (≤ 0,19).**

## 8.63.1 Question, méthode, règles

**Questions.** (M1, §8.50.4) Pourquoi la configuration (28, 27, 6) —
choisie par les nuls MTAP graine 123 et s11111 — produit-elle à la
fois un MC élevé et un Delta bas (s11111 : MC 0,5192, Delta 3,0168 ;
s123 : MC 0,4518, Delta 3,1415), alors que les 9 autres nuls frais
restent en MC ~0,32–0,34 et Delta ~3,80–3,85, et que le nul 42 donne
MC 0,5153 avec Delta HAUT (4,3466) ? (M2, §8.53.4) Par quel mécanisme
l'optimiseur choisit-il la configuration RÉELLE pour un nul — 17 des
20 nuls frais ICGC en w=16/ncand=35, 17/20 GSE62452 en w=16/ncand=34,
4/5 TCGA en w=30/ncand=93 ?

**Méthode.** Protocole gelé `PROTOCOL_mechanisms_863.md` (SHA
`4e05dfc208725d610c591c2e4845dca277ed0d7d0a64e8ac095491f03c21f35e`,
écrit avant tout nouveau script, toute nouvelle construction et tout
nouveau run). Quatre volets, dans l'ordre : (A) lecture des
`all_results` (les 12 configs évaluées par run, avec métriques
complètes) des 14 runs MTAP et des 58 runs immunitaires existants ;
(B) réplique du scan par les fonctions DU PIPELINE importées en
lecture seule (`_build_mc_progress_axis` +
`scan_critical_threshold` + `evaluate_scan_quality`, même pattern
que §8.53) — calibration 5/5 EXACTE (écart 0,00e+00) avant toute
lecture ; (C) réplique Delta par miroir exact du bloc `run_pipeline`
(lignes 7075–7187) + `compute_holographic_tension_state` importée —
calibration 5/5 EXACTE (écart 0,00e+00) avant tout croisement ;
(D) lot v6.2 fast de 10 nuls ICGC frais (graines 31–40, jamais
utilisées), via `systemd-run`, 10/10 exit 0.

**Mécanique lue dans le code v6.2 (pas devinée).** MC =
0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·acuité, avec
s_norm = tanh(maxsep/2) et robustesse =
exp(−((FWHM − 10)²)/(2·5²)), FWHM = largeur à mi-hauteur de la
courbe de scan en % des candidats (lignes 3314–3389, 3729–3731) :
rob ≈ 1 si FWHM ≈ 10 %, rob ≈ 0 si FWHM ≥ ~32 %. L'optimiseur
échantillonne 12 configs en mode fast avec
`rng = default_rng(42 + itération)` (lignes 243, 3461) — l'ensemble
des 12 configs ne dépend que de n, pas des données ; le gagnant est
l'argmax du MC sur ces 12. Le scan : w_size = longueur des fenêtres
glissantes, n_candidates = nombre de seuils sur 0–100 %,
min_grp = fenêtres minimales par côté (lignes 3125–3287). Delta =
d_div − d_sat, médianes des classes d'estimateurs de divergence et
de saturation (lignes 1927–1935, 8022), calculées sur `df_feat`,
construit avec le **w_size du best_config** (lignes 7079–7081) :
Delta dépend donc de l'ordre des lignes du CSV ET de w — les deux
causes sont séparées par le croisement §8.63.3.

**Règles de décision écrites avant (protocole §3).** M1a expliqué si
la FWHM recalculée reproduit rob à 10⁻⁶, si (93, 30, 6) donne aussi
MC > 0,44 avec rob > 0,5 sur s11111 ET s123, et si les 11 autres runs
ont max rob < 0,1. M1b expliqué si la calibration Delta tient à
10⁻⁶ et si l'un des deux effets (w ou CSV) porte ≥ 5/6 de l'écart.
M1c : cause commune seulement si un même flux porte ≥ 50 % du pic
dans les 3 runs rob-on ET le même estimateur de divergence porte la
chute de d_div dans s11111 et s123 ; sinon deux conséquences
indépendantes (le nul 42 rob-on à Delta haut suffisant à lui seul).
M2a expliqué si 1 seul ensemble de 12 configs par n. M2b expliqué
si la config réelle a le maxsep moyen le plus élevé dans les deux
cohortes n≈70 ET (Spearman(maxsep, ncand) > 0,5 OU la config
gagnante est la plus fine grille parmi les configs de petit w).
M2d : confirme si ≥ 7/10, infirme si ≤ 4/10, indécis entre 5 et 6.
M1 expliqué seulement si M1a ET M1b expliqués ; M2 expliqué
seulement si M2a ET M2b expliqués et M2d confirme.

## 8.63.2 M1a — le MC haut est une propriété de la permutation, pas de la config (28, 27, 6)

La FWHM recalculée depuis les courbes stockées reproduit la
robustesse à **0,00e+00** sur les 12 configs × 14 runs MTAP, et la
recomposition du MC (0,3·s_norm + 0,3·stab + 0,2·rob + 0,2·acuité)
aussi (écart max 0,00e+00) : la formule est vérifiée, pas supposée.
La réplique du scan (fonctions du pipeline) reproduit les 12
configs × 5 entrées à 0,00e+00, courbes comprises.

| Run | (28, 27, 6) : MC / rob / FWHM / seuil | (93, 30, 6) : MC / rob / FWHM / seuil | Marge |
|---|---|---|---|
| Nul s11111 | 0,5192 / 0,9756 / 11,11 % / 11,11 % | 0,5143 / 0,9263 / 11,96 % / 10,87 % | +0,0048 |
| Nul s123 | 0,4518 / 0,6290 / 14,81 % / 88,89 % | 0,4468 / 0,5802 / 15,22 % / 88,04 % | +0,0049 |

Sur s11111 ET s123, la config (93, 30, 6) donne aussi MC > 0,44
avec rob > 0,5 sur la MÊME entrée — le MC haut ne vient pas de
(28, 27, 6), qui ne fait que gagner de 0,005 sur (93, 30, 6). Les
11 autres runs MTAP ont max rob < 0,1 sur leurs 12 configs (max
0,0018 pour s2022, 0,0000 partout ailleurs) : leurs courbes sont
des plateaux larges (FWHM 42–78 % sur les témoins relus), tandis
que les 3 runs rob-on ont des pics étroits (FWHM 11,11 % pour
s11111 et le nul 42, 14,81 % pour s123). Le nul 42, quatrième cas
rob-on (4 configs > 0,1), gagne avec (46, 42, 7), MC 0,5153,
rob 0,9756 : le même interrupteur, une autre config. **M1a =
EXPLIQUÉ (permutation, pas config).** La cause du MC haut est la
forme de la courbe — un pic étroit que la gaussienne de robustesse
récompense de +0,13 à +0,20 de MC — et cette forme appartient à la
permutation, pas à la grille.

## 8.63.3 M1b — le Delta bas est une propriété de w = 27, pas de la permutation

La réplique Delta (miroir du bloc `run_pipeline` lignes 7075–7187)
reproduit le D_vector stocké à **0,00e+00** sur les 5 CSV à leur w
propre (réel w=30, s11111 w=27, s123 w=27, nul42 w=42, s1011 w=30).
Le croisement w × CSV tranche :

| CSV | Delta à w=27 | Delta à w=30 | Delta à w=42 |
|---|---|---|---|
| Réel | **3,0886** (d_div 4,6768) | 3,8051 (d_div 5,3831) | — |
| Nul s11111 | 3,0168 (d_div 4,6097) | **3,8289** (d_div 5,4107) | 4,4254 (d_div 5,9871) |
| Nul s123 | 3,1415 (d_div 4,7132) | **3,8514** (d_div 5,4401) | 4,3760 (d_div 5,9498) |

À w = 30, s11111 (3,8289) et s123 (3,8514) retrouvent le niveau du
réel (3,8051) : le « Delta bas » disparaît entièrement. À w = 27,
le RÉEL lui-même tombe à 3,0886 — le même niveau que les deux nuls.
À w = 42, les deux nuls montent à 4,38–4,43 (le nul 42 stocké, lui
aussi en w=42, est à 4,3466). Delta croît avec w sur les trois CSV,
de ~3,0–3,1 (w=27) à ~3,8–3,85 (w=30) puis ~4,4 (w=42).
Partage chiffré : écart entre CSV à w fixé = +0,0238 (à w=30) et
−0,0718 (à w=27) ; effet de w à CSV fixé = −0,7165 (réel),
−0,8120 (s11111), −0,7099 (s123) — ratio w/CSV = 34,16, soit
**96,8 % de l'écart porté par w**, au-dessus du seuil gelé de 5/6.
d_sat ne bouge jamais (1,56–1,60 sur les 8 cellules) : tout le
mouvement de Delta est d_div. Et à w = 30 fixé, les écarts de
médianes par estimateur de divergence entre s11111/s123 et le réel
sont tous ≤ 0,19 (contre −1,28 pour PCAIntrinsic à w = 27) : à w
fixé, il ne reste plus aucun signal de permutation dans d_div.
**M1b = EXPLIQUÉ (w, pas permutation).** La chaîne complète de M1
est donc : la permutation crée un pic étroit → la robustesse
allume le MC → l'optimiseur choisit (28, 27, 6) → w = 27 abaisse
d_div → Delta bas. La config n'est que le maillon qui transmet w.

## 8.63.4 M1c — MC haut et Delta bas : deux conséquences indépendantes

Les porteurs du pic (scan par flux seul, moyenne des 12 courbes
reproduisant la courbe complète à 0,00e+00) : aucun flux ne domine
— part maximale 0,181 (GSTM1, s11111), 0,190 (MUC16, s123), 0,254
(CEACAM5, nul 42), contre 0,13–0,18 chez les témoins rob-off
(FWHM 42–78 %). Le pic est diffus sur les 12 flux, pas porté par
un flux. Côté Delta, la chute de d_div à w = 27 est portée par
trois estimateurs ensemble (PCAIntrinsic −1,28 / −1,15, LocalPCA
−0,97 / −0,89, LevinaBickel −0,95 / −0,66 pour s11111/s123 contre
le réel) — mais cette chute disparaît à w fixé (§8.63.3), donc
elle ne partage pas de cause avec le pic. Et le nul 42 contredit
tout lien unifié : rob-on (0,9756) avec un Delta HAUT (4,3466,
d_div 5,9404). **M1c = DEUX CONSÉQUENCES INDÉPENDANTES** du même
tirage d'ordre, par deux voies distinctes (forme de la courbe de
scan d'un côté, longueur de fenêtre des estimateurs de dimension
de l'autre). **M1 global = EXPLIQUÉ** (M1a et M1b expliqués).

## 8.63.5 M2a — l'ensemble des 12 configs est fixe par n

Un seul ensemble distinct de 12 configs par n, sur tous les runs
relus et le lot frais : MTAP n=177, 15 runs (réel, réel 850, 13
nuls) ; ICGC n=70, **35 runs** (réel, 4 anciens §8.47, 20 frais
§8.53, 10 frais §8.63) ; GSE62452 n=69, 24 runs ; TCGA n=178,
9 runs. C'est le code qui le garantit : `rng =
default_rng(42 + itération)` (ligne 3461), 12 itérations en mode
fast (ligne 243) — l'échantillonnage ne voit pas les données.
(À noter : les ensembles diffèrent légèrement entre n=177 et
n=178 — (28, 27, 6) contre (29, 27, 6), (92, 62, 9) contre
(93, 62, 9) — parce que les bornes de la grille dépendent de n.)
**M2a = EXPLIQUÉ.** Il n'y a donc pas d'« optimiseur qui choisit
la config réelle pour un nul » au sens adaptatif : il y a un
argmax sur une grille fixe, et la question devient pourquoi ce
point de grille gagne si souvent (§8.63.6).

## 8.63.6 M2b — pourquoi la config réelle gagne : petit w, grille fine

Tableaux par config (moyenne sur les nuls frais ; 30 ICGC, 20
GSE62452, 5 TCGA) — extrait, trié par MC moyen :

| Cohorte | Config | maxsep moyen | MC moyen | stab. moy. | acuité moy. | rob. moy. | Victoires |
|---|---|---|---|---|---|---|---|
| ICGC | **(35, 16, 6)** | **0,2704** | 0,3466 | 0,9879 | 0,0145 | 0,0353 | **23/30** |
| ICGC | (22, 16, 7) | 0,2672 | 0,3474 | 0,9799 | 0,0147 | 0,0534 | 5/30 |
| ICGC | (11, 15, 6) | 0,2697 | 0,3342 | 0,9586 | 0,0142 | 0,0181 | 1/30 |
| GSE62452 | **(34, 16, 6)** | **0,2545** | 0,3437 | 0,9879 | 0,0132 | 0,0336 | **17/20** |
| GSE62452 | (22, 16, 7) | 0,2390 | 0,3398 | 0,9826 | 0,0124 | 0,0347 | 1/20 |
| GSE62452 | (11, 15, 6) | 0,2505 | 0,3314 | 0,9683 | 0,0110 | 0,0068 | 0/20 |
| TCGA | **(93, 30, 6)** | 0,3026 | 0,3920 | 0,9928 | 0,0236 | 0,2227 | **4/5** |
| TCGA | (29, 27, 6) | 0,3102 | 0,3855 | 0,9707 | 0,0285 | 0,2128 | 0/5 |

La config réelle a le maxsep moyen le plus élevé dans les deux
cohortes n≈70 (ICGC 0,2704 > 0,2697 > 0,2672 ; GSE62452 0,2545 >
0,2505 > 0,2390) — première partie du critère gelé, vérifiée sur
les tableaux finaux à 30 nuls ICGC. Le Spearman(maxsep moyen,
n_candidates) global est de −0,140 (ICGC) et −0,118 (GSE62452),
loin du seuil 0,5 — mais la clause alternative du protocole
s'applique : dans chaque cohorte, la config gagnante est la plus
fine grille parmi les configs de petit w (ICGC : ncand 35 contre
22 et 11 à w = 15–16 ; GSE62452 : ncand 34 contre 22 et 11).
**M2b = EXPLIQUÉ** (par la clause alternative du protocole, avec
les deux nombres qui l'accompagnent rapportés tels quels).

Lecture plus fine — descriptive, au-delà du critère gelé : le
maxsep moyen est presque parfaitement anti-corrélé à w
(Spearman −0,986 ICGC, −0,988 GSE62452, −0,991 TCGA, p ~ 10⁻⁹) :
les fenêtres courtes donnent plus de fenêtres, des moyennes de
fenêtres plus variables, et un max de |d| plus haut. w porte le
maxsep ; n_candidates porte la stabilité (Spearman(stab. moy.,
ncand) = +0,800 / +0,737 / +0,830) : à w égal, la grille la plus
fine a la fenêtre locale de stabilité la plus étroite en % et
donc la stabilité la plus haute — ICGC : 0,9879 pour (35, 16, 6)
contre 0,9799 et 0,9586 pour (22, 16, 7) et (11, 15, 6) ; TCGA :
0,9928 pour (93, 30, 6) contre 0,9707 pour (29, 27, 6), ce qui
compense son déficit de maxsep (0,3026 contre 0,3102) et lui
donne 4 victoires sur 5. La « config réelle » est donc le point
de grille petit-w + fine-grille qui maximise les deux termes à la
fois — une propriété de la grille, pas du réel. Le réel lui-même
y gagne pour la même raison (marge 0,0004 en ICGC) : il ne
« reconnaît » rien, il subit la même grille.

## 8.63.7 M2c + M2d — marges quasi nulles, réplication indécise

**Marges (M2c).** Médiane des marges vainqueur − 2e : 0,0029
(ICGC, 25/31 < 0,005, 27/31 < 0,01), 0,0028 (GSE62452, 15/21 <
0,005), 0,0037 (TCGA, 5/6 < 0,005). Le choix de la config est un
quasi-ex-aequo : l'étiquette « config réelle » est instable, et
un basculement de robustesse suffit à la renverser (voir M2d).

**Réplication hors échantillon (M2d).** Lot frais ICGC s31–s40 :
**6/10** choisissent (35, 16, 6) — P(X ≤ 6 | p = 0,85) = 0,050 —
soit **INDÉCIS** au critère gelé (confirme ≥ 7, infirme ≤ 4). Les
4 écarts viennent tous d'un basculement de robustesse : s32 gagne
avec (14, 23, 2), MC 0,4320, rob 0,5600 ; s35 et s37 avec
(22, 16, 7), MC 0,4682 et 0,4935, rob 0,6926 (s37 : maxsep 0,4154,
le plus haut des 10) ; s40 avec (22, 16, 7), MC 0,3667,
rob 0,1945. Au total, 23/30 nuls frais ICGC choisissent
(35, 16, 6) (76,7 %) — le taux de 17/20 (85 %) de §8.53 ne se
reproduit pas à l'identique, il se tasse. **M2 global =
PARTIELLEMENT EXPLIQUÉ** (M2a et M2b expliqués, M2d indécis).
Ce qui reste non élucidé : pourquoi la robustesse bascule sur
certaines permutations (4/10 ici, 3/24 en §8.53 sur ICGC+GSE) et
pas sur d'autres — le même « pic étroit » que M1a, dont le
déclencheur par permutation n'a pas de signature identifiée
(§8.63.4 : aucun flux porteur).

## 8.63.8 Ce que ça change, et ce que ça ne change pas

**Change.** (1) La lecture « (28, 27, 6) → MC haut, Delta bas »
du §8.50 est dissoute : c'est une coïncidence de deux effets de
grille — le pic étroit allume rob (MC haut), et w = 27 abaisse
d_div (Delta bas) — réunis par le seul fait que l'optimiseur a
choisi cette config. Ni le MC haut ni le Delta bas ne disent
quoi que ce soit de la permutation elle-même au-delà de la forme
de sa courbe. (2) Le « choix de la config réelle pour un nul »
du §8.53 est expliqué comme un artefact de grille fixe :
l'optimiseur ne compare que 12 points, et le point petit-w +
fine-grille gagne sur presque toute entrée, réelle ou nulle.
(3) Delta est désormais documenté comme dépendant de w de façon
monotone et forte (≈ +0,7 entre w=27 et w=30, ≈ +0,6 entre w=30
et w=42 sur cette série) : toute comparaison de Delta entre runs
doit se faire à w égal, sinon elle compare des fenêtres, pas des
données. C'est une mise en garde qui vaut au-delà de ce chantier
— y compris pour les lectures de Delta des sections antérieures
où w différait entre runs comparés. (4) La FWHM et la robustesse
sont vérifiées par reproduction exacte depuis les courbes
stockées : le terme de robustesse du MC est un interrupteur de
forme de courbe, pas une mesure de robustesse au sens usuel.
**Ne change pas.** Aucun verdict de séparation n'est touché :
S_sep sépare toujours sur la série MTAP (§8.50, distribution
10/10 au-dessus du plancher), le réel ICGC reste sous le plancher
n≈70 (§8.53), le rationnel vopimetostat + daraxonrasib n'est ni
renforcé ni affaibli. La marche de niveau multi-flux (§8.46) vit
dans les CSV, pas dans ces mécanismes. Le mécanisme « pourquoi
telle permutation a un pic étroit » reste ouvert — c'est la
même question que le basculement de robustesse en M2d.

## 8.63.9 Méthode

Protocole gelé avant tout nouveau script et tout nouveau run :
`PROTOCOL_mechanisms_863.md`, SHA
`4e05dfc208725d610c591c2e4845dca277ed0d7d0a64e8ac095491f03c21f35e`.
**(A)** `mechanisms_863.py` (SHA
`83a16fa85f71401fa69f7eeb898b52fb86c1a5b043e4ec44b1483adc386defe1`) :
lecture des `all_results` des 14 runs MTAP + 68 runs immunitaires
(58 existants + 10 frais), recomposition du MC, FWHM recalculée
depuis les courbes stockées, D_vector et médianes par estimateur.
**(B)** Réplique du scan (fonctions du pipeline importées en
lecture seule) : calibration 5/5 EXACTE (écart 0,00e+00 sur
métriques et courbes) sur MTAP réel, s11111, s123, ICGC réel et
ICGC nul s29, puis tableau 12 configs × 5 entrées MTAP et scan
par flux seul (moyenne des 12 courbes = courbe complète à
0,00e+00). **(C)** `replica_delta_863.py` (SHA
`242c8cf6483e8c141aed96852351ece8a0dbefb48b1b295a5cfbd080a88154d4`) :
miroir du bloc `run_pipeline` lignes 7075–7187 +
`compute_holographic_tension_state` importée ; calibration 5/5
EXACTE (écart 0,00e+00 sur d_sat, d_crit, d_div, d_null) puis
croisement w ∈ {27, 30} × CSV ∈ {réel, s11111, s123} + w=42 sur
s11111/s123. **(D)** Lot v6.2 : `build_nulls_icgc_863.py` (SHA
`7145e8a6ac4545f2c9a70019d61fca60ede9a8754b893f90aead003929a318e5`,
entrée ICGC vérifiée par SHA
`10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc`)
— 10 nuls frais graines 31–40 ; `run_v62_863.sh` (SHA
`05c2baea01d6457d890048285ca8652924eb5802a6ec245ca9a2e38a63a3ef4e`),
manifeste `manifest_v62_863.txt`, unité systemd `v62-863`,
11:51:36Z–13:15:32Z le 20 nov. 2026, **10/10 exit 0, 0 échec**,
SHA v6.2 vérifié avant le lot (`f07567c4…ec3abf`) et après
(`f07567c4…ec3abf`, vérifié à la relance de l'analyse).

## 8.63.10 Limites

- Mode fast seulement : 12 configs par run. L'« optimiseur »
  étudié est celui du mode fast ; les modes robust/stable/full
  échantillonnent davantage et pourraient choisir d'autres points
  — le mécanisme de grille fixe reste le même en nature (graine
  fixe + itération), mais les nombres (taux de choix, marges)
  sont propres au mode fast.
- La réplique Delta est un miroir de code inline : sa calibration
  à 0,00e+00 sur 5 CSV est la garantie, pas une formalité — mais
  elle ne couvre que w ∈ {27, 30, 42} et 3 CSV ; la monotonie de
  Delta en w n'est mesurée que sur ces trois points.
- Le déclencheur du pic étroit (pourquoi telle permutation et pas
  telle autre) n'est pas élucidé : le pic est diffus sur les 12
  flux, sans flux porteur, et sa fréquence varie (3/14 MTAP,
  4/10 ICGC frais ici contre 3/24 en §8.53) sans signature
  identifiée. C'est le résidu ouvert de ce chantier, commun à M1a
  et M2d.
- M2d est indécis sur 10 tirages (P = 0,050, à la frontière) :
  le taux de choix de la config réelle est estimé à 23/30
  (76,7 %) sur les nuls frais ICGC, pas à 85 % — l'intervalle
  reste large et le lot ne tranche pas entre 60 % et 85 %.
- Les lectures « w porte maxsep » et « ncand porte stabilité »
  (§8.63.6, second paragraphe) sont des lectures descriptives
  post-hoc sur les mêmes tableaux (Spearman −0,99 et +0,80),
  pas le critère gelé — le critère gelé, lui, est appliqué tel
  quel via sa clause alternative, avec les deux Spearman
  rapportés.
- Aucune donnée nouvelle hors des CSV déjà sur disque et des 10
  nuls frais ; aucun test direct ; aucun verdict biologique.

## 8.63.11 Provenance

- **Protocole gelé.** `PROTOCOL_mechanisms_863.md` (SHA-256
  `4e05dfc208725d610c591c2e4845dca277ed0d7d0a64e8ac095491f03c21f35e`),
  écrit avant tout nouveau script, toute nouvelle construction et
  tout nouveau run de ce chantier.
- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant le lot et après, journal du lot). Scripts neufs :
  `mechanisms_863.py` (SHA-256
  `83a16fa85f71401fa69f7eeb898b52fb86c1a5b043e4ec44b1483adc386defe1`),
  `replica_delta_863.py` (SHA-256
  `242c8cf6483e8c141aed96852351ece8a0dbefb48b1b295a5cfbd080a88154d4`),
  `build_nulls_icgc_863.py` (SHA-256
  `7145e8a6ac4545f2c9a70019d61fca60ede9a8754b893f90aead003929a318e5`),
  `run_v62_863.sh` (SHA-256
  `05c2baea01d6457d890048285ca8652924eb5802a6ec245ca9a2e38a63a3ef4e`).
- **Entrées (SHA-256 vérifiés).** Série MTAP :
  `pdac_tcga_fluxes_v4_mtap.csv`
  `578b8d3b9b26099d0784ed23754d1cc9717be7f9292eb47e201d186cdbc90df6`
  (177 tumeurs, Broad GDAC Firehose stddata 2016-01-28, PAAD, RSEM ;
  GISTIC2 Level 4) et ses 13 nuls (§8.50 : s1011 `e074becc…975a4`,
  s2022 `81663ffd…ebb3`, s3033 `fb42718d…b131`, s4044
  `58eee570…0ecd`, s5055 `e3de4a84…91d80`, s6066 `734b4845…064a`,
  s7077 `70f9a8e8…fddde3c`, s8088 `fea69d43…8959`, s9099
  `727bd3f0…65a`, s11111 `c7c1739d…958c0` ; anciens 42
  `e6786a47…453b9`, s7 `cacce06f…904d3`, s123 `da2b1d3f…626c1`).
  Flux immunitaires : `pdac_immune_{tcga,geo62452,icgc}_fluxes.csv`
  (SHA dans PROVENANCE_immune_v6.md, re-vérifiés §8.53.6a ; ICGC
  réel `10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc`,
  re-vérifié avant construction des nuls s31–s40). Nuls ICGC frais
  s31–s40 : SHA dans `nulls_icgc_863_files.json` (s31
  `a6a216bbad4d…`, s32 `8946229115c3…`, s33 `09d570ab021b…`, s34
  `ef7088e74507…`, s35 `06375eac49ec…`, s36 `65ccfa18f083…`, s37
  `b04f609fa728…`, s38 `aebf5483dde0…`, s39 `a6bdbc448ac1…`, s40
  `f790ad6b9be1…`).
- **Sorties.** `mechanisms_863_extract.json`,
  `mechanisms_863_results.csv` (82 runs : 14 MTAP + 68
  immunitaires), `mechanisms_863_perflux.csv`,
  `replica_delta_863.json` (calibration 5/5 + croisement 8
  cellules), `nulls_icgc_863_files.json`, `manifest_v62_863.txt`,
  `runs_v62_863.log` (10/10 exit 0, unité `v62-863`,
  20 nov. 2026 11:51:36Z–13:15:32Z), dossiers
  `results_fast_v62_863_icgc_nul_s31/` … `s40/`.
- **Faits de départ.** `section_8.50_mtap_consolidation.md`
  (protocole `PROTOCOL_mtap_consolidation_850.md` SHA
  `13fec689…e2bb09`) et `section_8.53_nulls_n70.md` (protocole
  `PROTOCOL_nulls_n70_853.md` SHA `38689f8a411ac9b5…`) — relus,
  jamais réimportés comme verdicts.
- **Nature des lignes.** Résidus d'expression TCGA (mesures
  instrumentales — séquençage ARN — transformées) ordonnés par CN
  MTAP ; flux immunitaires (ARN bulk) ; nuls = lignes permutées
  (échantillons hypothétiques, pas des mesures) ; aucune autre
  donnée nouvelle dans ce chantier.
- **Ce qui manque, ce qui reste ouvert.** Le déclencheur du pic
  étroit par permutation (M1a/M2d) ; la monotonie de Delta en w
  au-delà de w ∈ {27, 30, 42} ; le taux de choix de la config
  réelle sur plus de 10 nuls frais (M2d indécis) ; les modes
  autres que fast (12 configs) ; PDF non régénéré, rien poussé
  sur GitHub (hors de ce chantier).

— Fin de la §8.63. —
