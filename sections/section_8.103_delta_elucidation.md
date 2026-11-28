### 8.103 Delta, nouvelle tentative d'élucidation — chantier D (27 novembre 2026)

Go de Zackary, 27 nov. 2026 09h52 : « il faudrait regarder le delta, il
ne faudrait pas l'oublier » (chantier D ajouté au lot en cours).
Protocole gelé `PROTOCOL_8103_delta_w.md` avant tout calcul neuf.

**Verdict d'abord, en quatre phrases. (a) NON ÉLUCIDÉ — cinquième
tentative, cinquième échec au critère gelé du §8.39 (≥ 90 % paires ET
≥ 90 % valeurs à ±0,10 en hold-out) : sur le corpus neuf de 3 015 runs
(200 nuls × 15 paires + 15 réels, §8.98), le meilleur modèle honnête
prédit d_div à ±0,10 sur 12,2 % des runs en leave-one-pair-out
(368/3 015, [1, w, ln n]) et l'identité de la paire sur 71,3 %
(2 150/3 015). (b) À w égal, l'écart Delta réel−nul reste dans ±0,10
sur 1 490/2 213 nuls seulement (67,3 %) — et il varie de 0,7 % (TCGA
v4) à 100 % (trois paires) selon la paire : w ne collapse pas l'écart.
(c) Le résidu de Delta après retrait de l'échelle en n et de l'effet w
ne suit pas les écarts des 4 estimateurs à loi d'échelle (meilleure
corrélation +0,355, GraphDimension ; ridge LOPO 41,9 % à ±0,10).
(d) La cartographie Delta(w) par réplique sur TCGA v4 (réel + 10 nuls,
121 builds) montre que Delta(w) n'est PAS une fonction en escalier :
sur le réel, 10 niveaux distincts à ±0,10 près sur 11 w, 9 pas
adjacents sur 10 au-dessus de 0,10 (max 2,51), étendue 3,75 — mais
cette courbe sauvage est presque la MÊME pour le réel et pour les
nuls (corrélation médiane 0,9967 ; la courbe médiane des autres
matrices prédit chaque build à ±0,10 sur 113/121, 93,4 %) : w
choisit le niveau, la permutation ne le déplace presque pas, sauf
à w = 30 — le w propre du réel — où le réel dépasse les 10 nuls de
+0,34 à +0,40. Delta reste une piste fragile et ne devient pas un
discriminateur recommandé.**

## 8.103.1 Ce qui était acquis avant ce chantier

Cinq tentatives closes NON ÉLUCIDÉES : §8.39 (variables structurelles,
meilleur hold-out honnête 87,9 % paires / 81,8 % valeurs), §8.42
(résumés de flux, 68,9 % paires / 6,3 % valeurs en LOCO), §8.57
(séries complètes, 89,2 % / 90,5 % en LOCO — manqué de 2 runs),
§8.62 (loi d'échelle en n, meilleur R² = 0,673 < 0,80 ; LOCO
R² = −0,005), §8.94 (quatre angles, meilleur hold-out 40,1 % paires
kNN / 13,5 % valeurs ; à w égal 71,2 % ; résidu après F2(ln n) non
bruit, 50,0 %). Acquis fermes : Delta = d_div − d_sat (vérifié exact
sur 96 runs, §8.32) ; la paire médiane se joue entre trois estimateurs
hauts {MFA, LevinaBickel, PCAIntrinsic} une fois LocalPCA fixée en 3e
position (§8.39) ; w déplace Delta fortement (r = +0,603 sur 222 runs,
+0,21 à +1,13 entre w = 27 et w = 30 sur les 8 paires principales,
§8.94) ; quatre estimateurs suivent une loi F2(ln n) qui passe les
trois volets (Katz, Petrosian, Sevcik, GraphDimension, §8.62) sans
porter Delta ; M2 clos EXPLIQUÉ à 80 % (§8.75). Barre gelée, inchangée
depuis §8.39 : 90 % en hold-out honnête, paires ET valeurs.

Ce chantier ajoute trois angles neufs, tous gelés avant tout calcul :
le corpus §8.98 (3 000 runs, B1), la paire GHA/local du smoke-test de
fusion (B2), le résidu de Delta contre les 4 estimateurs à loi
d'échelle (B3), et la cartographie directe Delta(w) par réplique sur
une paire fixe (B4). La correction de Zackary du 21 nov. 2026 12h03
s'applique : contrôle jamais analysé, contrôles non monotones lus comme
information (aucun seuil écarté pour non-monotonie), formulation en
analyse uniquement, jamais de prédiction.

## 8.103.2 Méthode du chantier

Protocole gelé `PROTOCOL_8103_delta_w.md`
(SHA `1c896cbb7fdd0ddfddf9b1a6b869eb4a4f07835ca5eb6b933635298a280b548a`),
écrit avant tout calcul neuf ; scripts `v62_delta_8103.py`
(extraction B1), `v62_delta_8103_analyse.py` (tests B1/B3),
`v62_delta_8103_b2.py` + `v62_delta_8103_b2_detail.py` (B2),
`v62_delta_8103_b4.py` + `v62_delta_8103_b4par.py` (B4).
Pipeline v6.2 `universal_v6.2.0_cohen.py`,
SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
vérifié avant travail et après chaque lot, jamais modifié.
**Aucun run du pipeline dans ce chantier** (B4 = réplique seule, avec
les fonctions du pipeline importées en lecture seule).

**Corpus B1 (extraction).** 3 015 dossiers candidats
(`results_fast_gha_893_*` 2 090 + `results_fast_v62_893_*` 910 + 15
réels) : **3 015/3 015 extraits, 0 erreur**. Vérifications
préalables : identités d_div/d_sat recalculées depuis les médianes
parsées — **3 015/3 015 à 10⁻³** (div et sat, 0 écart) ; Delta =
d_div − d_sat à 10⁻³ sur **3 015/3 015**. Chaque paire compte 200
nuls + 1 réel (vérifié par comptage). w récupéré sur 3 015/3 015
runs : 47 valeurs distinctes, de 10 à 500, médiane 19 ; 139 runs à
w > 100 (dont HP35, w jusqu'à 500). k_div : 6 membres sur 1 797 runs,
5 sur 425, 4 sur 793. Lot lancé en `systemd-run` (unité
`delta-8103-extract`, 346,6 s) avec gardien
(`delta-8103-extract-watch`) ; un redémarrage machine a tué la
première passe à 1 000/3 015 — reprise par le partiel incrémental,
sans rien écraser ni relire.

**B2.** 6 runs TCGA v4 (GHA réel/nul, local réel/nul, local rep2
réel/nul), comparaison feuille par feuille (égalité exacte).

**B3.** Coefficients F2(ln n) des 4 estimateurs repris de
`v62_delta_scaling_862_phaseA.json`, NON ré-estimés : Katz
[1,735112 ; −0,204006 ; 0,015424], Petrosian
[1,231508 ; −0,057639 ; 0,004119], Sevcik
[0,706901 ; 0,310716 ; −0,023533], GraphDimension
[−1,646663 ; 0,960839 ; −0,073355].

**B4.** Réplique `build_df_feat` de `replica_w_894.py` (importé, non
modifié) ; CSV nuls régénérés avec le builder gelé
`build_null_893.py` (SHA `572b55bc…f467`) ; calibration à |Δ| < 10⁻⁶
sur le D_vector stocké — **4/4 OK à 0,00e+00** (réel w = 30,
d_div 5,754216 ; nuls s9101 w = 30, s9102 w = 53, s9103 w = 30).
Grille w gelée : {10, 15, 20, 25, 27, 30, 35, 40, 50, 60, 80}.
Durées de build en calibration : 112,2 / 115,9 / 120,6 / 122,1 /
118,2 s (moyenne ≈ 117 s > 90 s) — **règle d'arrêt déclenchée :
B4a = réel + 10 nuls (graines 9101–9110) × 11 w = 121 builds**,
exécutés en 2 workers (7 499 s de mur, durées 69,8–236,6 s,
moyenne 123,7 s), lanceur `run_delta_8103_b4.sh` + gardien
`watch_8103_b4a.sh`, partiels atomiques, fusion 121/121
(`B4A_8103_DONE` 17:34:59 UTC). Phase B4b : déclencheur gelé atteint
(plus grand pas 2,51 > 0,10), mais **non lancée** — voir §8.103.6 :
le critère (i) tranche déjà le verdict et (ii)/(iii) passent déjà
sur B4a ; l'extension à 200 nuls (~19 h estimées, 800 builds) ne
peut pas changer le verdict.

## 8.103.3 B1 — Le corpus §8.98 : w n'explique ni le niveau, ni l'écart réel−nul

**B1a — Delta à w égal (version 3 000 runs du §8.94 A1).**
2 213/3 000 nuls (73,8 %) partagent le w de leur réel. Sur ces
2 213 nuls, |Delta_nul − Delta_réel| ≤ 0,10 sur **1 490 (67,3 %)**
— sous la barre de 90 %, et en baisse par rapport aux 71,2 % du
§8.94 (52/73 paires). Surtout, la fraction varie de **0,7 % à
100 %** selon la paire :

| Paire | w réel | nuls à w égal | ≤ 0,10 | Delta réel − médiane nuls |
|---|---|---|---|---|
| TCGA v4 | 30 | 151 | 0,7 % | +0,369 |
| GDC organoid | 19 | 198 | 10,1 % | +0,357 |
| Yeh FF | 18 | 197 | 29,9 % | +0,218 |
| Immune TCGA | 30 | 125 | 64,0 % | +0,076 |
| PARP TCGA | 30 | 155 | 63,9 % | +0,098 |
| GSE60979 | 11 | 148 | 68,2 % | +0,099 |
| GSE71729 | 23 | 13 | 69,2 % | −0,702 |
| GSE194249 | 18 | 192 | 77,1 % | +0,014 |
| DepMap | 10 | 114 | 86,0 % | +0,109 |
| GSE57495 | 15 | 177 | 88,1 % | +0,008 |
| ICGC | 16 | 191 | 91,1 % | +0,040 |
| GSE62452 | 16 | 188 | 96,3 % | +0,024 |
| GSE21501 | 24 | 178 | 100 % | +0,016 |
| GSE79668 | 12 | 159 | 100 % | +0,023 |
| HP35 | 59 | 27 | 100 % | −0,055 |

Lecture : à w égal, l'écart réel−nul s'effondre sur certaines paires
(100 % dans ±0,10 sur trois paires) et pas du tout sur d'autres
(0,7 % sur TCGA v4, où le réel dépasse la médiane des nuls de
+0,369 ; 10,1 % sur GDC). Le signe même de l'écart réel − médiane
nuls change : −0,702 sur GSE71729 (réel SOUS les nuls), +0,369 sur
TCGA v4. w ne choisit pas le niveau : il le déplace différemment
selon la paire. L'élucidation négative (« Delta = fonctionnelle de n
et de w, sans contenu de flux ») reste exclue, comme au §8.94 A2.

**B1c — Effet w à n fixé (dans chaque paire, 200 nuls).** La
corrélation r(Delta, w) intra-paire va de **−0,876 (DepMap,
R² = 0,768) à +0,759 (GSE79668, R² = 0,577)**, en passant par
+0,742 (ICGC), +0,673 (GSE71729), +0,601 (HP35) — et par **≈ 0**
sur TCGA v4 (+0,042, R² = 0,002), GDC organoid (−0,016), GSE21501
(+0,071), PARP TCGA (−0,044), Yeh FF (−0,022). Les pentes changent
de signe (DepMap −0,0226 par unité de w, GSE79668 +0,0690). Poolé
(recentré par paire), l'écart-type de Delta ne passe que de 0,363 à
0,332 après retrait de l'effet w linéaire : **w retire 8,6 % de la
dispersion intra-paire, pas le niveau.** w est un moteur local, pas
un mécanisme universel : il explique beaucoup sur certaines paires,
rien sur d'autres, et dans des sens opposés.

**B1b — LOPO (leave-one-pair-out).** Prédire les 6 médianes
divergence depuis [1, w, ln n] (OLS), paire et d_div dérivés par la
construction connue après application du masque vrai (§8.57) :

| Modèle (LOPO, 3 015 runs) | Paires | Valeurs ±0,10 | MAE d_div |
|---|---|---|---|
| 1 + w + ln n | 2 150 (71,3 %) | 368 (12,2 %) | 0,643 |
| 1 + w + ln n + (ln n)² | 1 762 (58,4 %) | 178 (5,9 %) | 0,917 |
| Majorité (paire, masque, MFA, n) | 2 068 (68,6 %) | 208 (6,9 %) | — |

Correction consignée : une première passe sans application du masque
vrai donnait 64,0 % / 10,4 % pour [1, w, ln n] ; la correction à la
construction du §8.57 (masque vrai appliqué) monte à 71,3 % / 12,2 %
— le verdict ne change pas : aucun modèle n'approche 90 % sur l'un
ou l'autre volet. Le terme quadratique dégrade les deux volets.
**B1 ne remplit pas le critère ÉLUCIDÉ.**

## 8.103.4 B2 — Décomposition de variance GHA / local / rep2 : le cœur est déterministe, la gigue est MC

**Local vs local rep2 : 10 feuilles différentes sur ~204 000–205 000
(6 dans `run_pipeline`, 4 dans `runtime`) — Delta identique au
dernier chiffre (réel 4,181387, nul 3,765664).** Le pipeline est
déterministe en local, comme le disait déjà le smoke-test.

**GHA vs local : 49 046 feuilles différentes (réel, sur 204 091) et
51 404 (nul, sur 205 485).** Ventilation (réel) : `threshold_metadata`
22 058 (dont `optimization_diagnostics` 4 742,
`raw_optimization_diagnostics` 4 742, `raw_mc_complexity` 4 740,
`mc_complexity` 4 740, `all_results` ~3 094), `noise_diagnostic`
21 314 (dont `estimator_four_tests/by_flux` 14 231 et
`estimator_drift` ~900), `scores` 2 111, `transition_analysis`
1 952, `prediction_levels` 1 413 (dont L1_L2_target 1 175,
L5_complexity 197), `reading_synthesis` 85,
`holographic_tension_state` 85, `top_signatures` 15, `csd_ranking` 4,
`runtime` 8, `metadata` 1. Définition étroite pré-enregistrée
(tout `threshold_metadata` + tout `noise_diagnostic` +
L5_complexity) : **43 569/49 046 = 88,8 % (réel), 45 755/51 404 =
89,0 % (nul)** — juste sous les 90 % en définition étroite ; le
reste est lui aussi en aval des mêmes traces MC (scores,
transition_analysis, L1/L3/L4) ou des z-scores croisés. Aucun score
de décision ne bouge : cascade, maxsep, MC calculé, `best_config`,
seuils — identiques ; w = 30 des deux côtés.

**Quelles feuilles portent la gigue de Delta ? Trois médianes sur 29
bougent, toutes côté saturation : DFA (réel 1,567181 GHA vs 1,573236
local, −0,006055 ; nul −0,006295), Hurst2mH (±0,001387 / ±0,000220),
Hurst (±0,001387 / ∓0,000220). d_div est IDENTIQUE (5,754216 réel,
5,368531 nul) ; les 26 autres médianes sont identiques.** La gigue
de Delta (+0,005648 réel, −0,000219 nul) est donc entièrement une
gigue de d_sat : sur le réel, la médiane DFA qui baisse de 0,006
fait basculer le 4e membre saturation (DFA ↔ Hurst2mH, d_sat 1,567181
vs 1,572829) ; sur le nul, le même mouvement ne fait pas basculer le
rang et d_sat ne bouge que de 0,00022. Les 29 `cross_z` bougent aussi,
de ~10⁻⁴ à 1,5×10⁻³ (z-scores MC). Lecture : la part tirages
MC/permutations de Delta vit dans DFA — l'estimateur déjà connu pour
ses extrêmes (−38,16, §8.39.8) — et elle ne pèse que ~0,006 sur
Delta, soit 1/17e de la tolérance ±0,10 ; elle n'explique ni le
niveau de Delta, ni son écart réel−nul (0,42 sur TCGA v4). B2 est
descriptif, comme gelé : il ne porte pas seul le verdict, il nomme
la part déterministe (d_div, 26/29 médianes, tous les scores de
décision) vs la part tirages (diagnostics MC/bruit + médiane DFA).

## 8.103.5 B3 — Le résidu de Delta ne suit pas les 4 estimateurs à loi d'échelle

Dans chaque paire, n est fixé : l'écart e_est = médiane − F2(ln n)
de chacun des 4 estimateurs est une déviation purement run-à-run.
Le résidu de Delta est recentré par paire et corrigé de l'effet w
linéaire intra-paire (B1c). Corrélations poolées (standardisées
intra-paire, n = 3 015) : **GraphDimension r = +0,355 ; Katz
r = −0,128 ; Sevcik r = −0,076 ; Petrosian r = −0,042.** Seul
GraphDimension — la plus basse des divergences, jamais dans la paire
— porte un signal faible (12,6 % de variance du résidu). Prédiction
en LOPO : **ridge (λ = 10) sur les 4 écarts + w recentré : 1 263/3 015
(41,9 %) des résidus à ±0,10, MAE 0,204** ; **kNN k = 5 sur les 4
écarts : 1 766/3 015 paires (58,6 %)**. Critère B3 (≥ 90 % aux deux
volets) : **NON ATTEINT, de loin.** Les déviations run-à-run des
estimateurs à loi d'échelle ne portent pas le résidu run-à-run de
Delta — pas plus que leur loi en n ne portait son niveau (§8.62).
La voie « loi d'échelle » reste close pour Delta, dans sa dernière
variante.

## 8.103.6 B4 — Cartographie Delta(w) : une courbe sauvage, la même pour le réel et les nuls

**La courbe du réel (11/11 w).** Delta(w) sur TCGA v4 réel :

| w | 10 | 15 | 20 | 25 | 27 | 30 | 35 | 40 | 50 | 60 | 80 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Delta | 1,43 | 1,52 | 2,83 | 1,58 | 3,16 | 4,18 | 3,01 | 3,72 | 2,36 | 4,88 | 5,18 |
| d_div | 3,00 | 3,11 | 4,42 | 3,16 | 4,73 | 5,75 | 4,57 | 5,27 | 3,89 | 6,40 | 6,66 |
| d_sat | 1,57 | 1,59 | 1,59 | 1,58 | 1,58 | 1,57 | 1,56 | 1,55 | 1,53 | 1,52 | 1,48 |
| Paire | L+MFA | L+MFA | L+MFA | L+MFA | L+PCI | L+LB | L+LB | L+PCI | L+MFA | L+MFA | L+MFA |

(L = LocalPCA, LB = LevinaBickel, PCI = PCAIntrinsic.) Pas adjacents :
+0,09 ; +1,31 ; −1,26 ; +1,58 ; +1,02 ; −1,17 ; +0,70 ; −1,35 ; +2,51 ;
+0,31 — **9/10 au-dessus de 0,10, max 2,51, étendue 1,43–5,18**.
d_sat dérive lentement (1,59 → 1,48) ; tout le mouvement est d_div.
MFA elle-même saute avec w (3,0 ; 4,0 ; 5,0 ; 4,0 ; 6,0 ; 7,0 ; 6,0 ;
7,0 ; 4,0 ; 7,0 ; 7,0) et la paire bascule (MFA → PCI → LB → PCI →
MFA) aux mêmes w que les sauts. **Critère (i) : 10 niveaux distincts
à ±0,10 près sur 11 w — ÉCHEC, de loin (il en fallait ≤ 3).**
Delta(w) n'est pas une fonction en escalier : c'est une fonction
irrégulière, non monotone, qui monte et descend de plus de 1,0 entre
deux w adjacents de la grille.

**Mais la même courbe pour les nuls.** Chacun des 10 nuls a 8 à 10
niveaux et 9 à 10 pas > 0,10 (max 2,48–2,56) — et **10/10 nuls
partagent la séquence de pas du réel** (mêmes positions à un pas de
grille près, mêmes signes) : **critère (ii) PASSÉ sur 10/10.**
Corrélation courbe réel vs nul : médiane **0,9967**. Écart réel−nul
à w fixé (médiane sur 10 nuls) : 0,025 (w = 10), 0,013 (15), 0,009
(20), 0,037 (25), 0,044 (27), **0,359 (30)**, 0,201 (35), 0,068 (40),
0,031 (50), 0,036 (60), 0,065 (80) — 10/10 nuls dans ±0,10 à w = 10,
15, 20, 25, 27, 50, 60 ; **0/10 à w = 30** (écarts +0,343 à +0,403) ;
2/10 à w = 35. La dispersion inter-matrices de Delta à w fixé est
minuscule (écart-type 0,011–0,042) sauf à w = 30 (0,107) et w = 35
(0,126), où c'est le réel qui sort du groupe. **Critère (iii) :
la courbe médiane des 10 autres matrices au même w (leave-one-
matrix-out) prédit chaque build à ±0,10 sur 113/121 (93,4 %),
MAE 0,039 — PASSÉ** ; la variante (w, paire) donne exactement les
mêmes 113/121 — l'identité de la paire n'ajoute rien, w seul porte
la courbe.

**Lecture.** (ii) et (iii) passent, (i) échoue : Delta(w) est
prévisible depuis w — à ±0,10 près sur 93,4 % des builds — mais ce
qui est prévisible n'est pas un escalier à 3 niveaux, c'est une
courbe irrégulière à ~10 niveaux, identique pour le réel et ses
nuls. Le mécanisme « le niveau est choisi par w » tient dans sa
forme faible (w détermine le niveau, à matrice fixée, à ±0,10 près
9 fois sur 10) et échoue dans sa forme gelée (≤ 3 niveaux) : le
choix du niveau n'est pas élucidé, parce que la fonction Delta(w)
elle-même n'est pas comprise — pourquoi MFA saute de 4,0 à 7,0 puis
retombe à 4,0 quand w passe de 25 à 50, pourquoi la paire bascule
à ces w-là, reste sans réponse. Fait neuf, consigné sans
interprétation : **le w propre du réel (30, choisi par l'optimiseur
de seuil) est exactement le w où l'écart réel−nul est maximal
(+0,36)**, alors qu'il est ≤ 0,07 partout ailleurs — c'est aussi
pourquoi B1a trouve 0,7 % sur TCGA v4 à w égal. Ce n'est pas une
preuve d'un mécanisme : c'est une coïncidence à tester sur d'autres
paires avant toute lecture.

**B4b — déclencheur atteint, extension non lancée (décision
consignée).** Le déclencheur gelé est atteint (plus grand pas réel
2,51 > 0,10, et 2,48 sur la médiane des nuls). L'extension
prévue — 200 nuls × 3 à 4 w (grille {40, 50, 60, 80} autour du
plus grand pas) ≈ 800 builds ≈ 19 h estimées — n'est PAS lancée,
pour une raison chiffrée et non pour gagner du temps : le verdict
B4 est déjà fixé par l'échec du critère (i) (conjonction (i) ET
(ii) ET (iii)), et les deux autres critères passent déjà sur B4a
((ii) 10/10, (iii) 113/121). B4b ne mesurerait que la précision de
(ii) sur 200 nuls au lieu de 10 — elle ne peut pas changer le
verdict. L'extension reste disponible en suivi (script
`v62_delta_8103_b4.py --b4b`, grille et graines gelées) ; son
absence est une limite nommée, pas un trou caché. **B4 : NON
ÉLUCIDÉ.**

## 8.103.7 Lecture croisée : ce qui est exclu, ce qui reste ouvert

**Exclu par ce chantier (chiffres, pas d'adjectifs).** (1) w seul
choisit le niveau au sens du critère ≥ 90 % : LOPO 71,3 % paires /
12,2 % valeurs ; à w égal 67,3 % ; effet w intra-paire de R² = 0,77
à 0,00 selon la paire, signes opposés. (2) ln n seul ou avec w :
LOPO 58,4 % / 5,9 % avec le terme quadratique. (3) Les écarts des
4 estimateurs à loi d'échelle portent le résidu de Delta : meilleure
corrélation +0,355, ridge LOPO 41,9 %. (4) Delta(w) est un escalier
à ≤ 3 niveaux : 10 niveaux sur le réel, 8 à 10 sur chaque nul.
(5) La gigue GHA/local porte le niveau de Delta : elle pèse ~0,006
sur Delta (médiane DFA), contre un écart réel−nul de 0,42 à w = 30
sur TCGA v4.

**Ce qui est établi, et qui ne change pas le verdict.** (a) w
détermine le niveau de Delta à matrice fixée : la courbe Delta(w)
est prévisible à ±0,10 sur 93,4 % des builds (B4 (iii)), et la
même pour le réel et ses nuls (corrélation 0,9967). (b) À w fixé,
le réel et ses nuls coïncident presque partout (écart médian
≤ 0,07 sur 9 w sur 11) — sauf à w = 30, le w propre du réel
(+0,36). (c) Le cœur du pipeline est déterministe (local vs rep2 :
10 feuilles sur ~204 000) ; la seule gigue qui touche Delta passe
par la médiane DFA (~0,006). (d) Sur le corpus de 3 015 runs,
Delta réel − médiane des nuls change de signe selon la paire
(−0,70 GSE71729, +0,37 TCGA v4, +0,36 GDC, ~0 sur 8 paires) :
Delta ne sépare pas le réel du nul de façon cohérente, même à
w égal.

**Ce qui reste ouvert, non testé ici.** (1) Pourquoi Delta(w) est
irrégulière : pourquoi MFA saute entre ses valeurs quasi discrètes
quand w varie, et pourquoi la paire bascule à ces w-là — la
question se déplace de « quel w choisit le niveau » vers « quelle
fonction de w est Delta, et d'où viennent ses sauts ». (2) Le fait
que le w propre du réel soit le w de séparation maximale : à
tester sur d'autres paires (le w propre de chaque réel est-il
toujours un w de grand écart réel−nul ?). (3) M1c (§8.63) — MC haut
et Delta bas ont-ils une cause commune ? Non tranché. (4) La
dispersion inter-flux de LevinaBickel (§8.57.9 point 2), inchangée.
(5) L'extension B4b à 200 nuls (mesure de précision de (ii)),
non lancée — voir §8.103.6.

**Pour le projet.** Delta reste une piste fragile, cinquième
confirmation. Aucun changement de protocole, aucun changement de
pipeline, aucune utilisation de Delta comme discriminateur. La
barre de 90 % ne bouge pas ; toute nouvelle tentative exigera un
protocole gelé neuf.

## 8.103.8 Limites

- B1 : le corpus §8.98 ne couvre que 15 paires (9 cohortes
  d'origine) ; les scores LOPO tiennent une paire entière à
  l'écart, pas une source inconnue. La majorité (paire, masque,
  MFA, n) retombe sur la majorité globale en LOPO (groupe
  inconnu au test) — c'est la règle gelée du §8.39, appliquée
  telle quelle, et elle vaut 68,6 % / 6,9 %.
- B1c : l'effet w intra-paire est linéaire par construction ; un
  effet non linéaire de w intra-paire n'est pas modélisé dans B1
  (il est mesuré directement en B4).
- B2 : 6 runs d'une seule paire (TCGA v4) ; la part MC (88,8 % /
  89,0 % en définition étroite) est une borne basse — le reste est
  en aval des mêmes traces MC, mais la classification large n'est
  pas recomptée formellement.
- B3 : les écarts e_est utilisent les F2 du §8.62, ajustées sur les
  222 runs d'origine — le corpus §8.98 est hors de leur train, ce
  qui est le sens voulu (pas de ré-estimation), mais les F2 ne sont
  pas ré-ajustées sur 3 015 runs.
- B4 : une seule paire (TCGA v4), 10 nuls (règle d'arrêt, 20 prévus
  initialement) ; grille de 11 w (pas de mesure entre les points
  de grille — les sauts pourraient être plus étroits que le pas) ;
  B4b non lancée (voir §8.103.6). Le critère (iii) est lu en
  leave-one-matrix-out sur les 11 matrices de B4a, pas sur une
  matrice nouvelle.
- Le verdict est lu sur la batterie gelée B1–B4, jamais sur un seul
  nombre (MC jamais seul) ; il décrit les données détenues, il ne
  prédit rien.

**Provenance (§8.103)**

- Protocole gelé `PROTOCOL_8103_delta_w.md`, SHA-256
  `1c896cbb7fdd0ddfddf9b1a6b869eb4a4f07835ca5eb6b933635298a280b548a`.
  Go : Zackary, 27 nov. 2026 09h52. Coordinateur : TagPrint
  (agent du chantier D).
- Code : pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant travail, avant chaque lot et après chaque lot ;
  inchangé) ; builder de nuls gelé `build_null_893.py`, SHA-256
  `572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467` ;
  réplique `replica_w_894.py` (§8.94, importée, non modifiée).
- Données : corpus B1 = 3 015 `master_results.json` (§8.98 :
  2 090 GHA + 910 locaux + 15 réels), 3 015/3 015 extraits,
  0 erreur, identités d_div/d_sat 3 015/3 015 à 10⁻³, Delta =
  d_div − d_sat 3 015/3 015 ; B2 = 6 runs TCGA v4 (GHA, local,
  rep2) ; B4 = TCGA v4 réel (CSV SHA `e7a2adab…3a0b0`) + 10 nuls
  régénérés (graines 9101–9110, SHA dans `delta_8103_b4.json`,
  calibration 4/4 à 0,00e+00 — dont s9101 SHA
  `22f39bf7b6ed0efc4c065347de94ef829e50f1e1df7afb9677686061c005e8fa`,
  identique à la validation §8.93).
- Scripts et sorties : voir `PROVENANCE_8103.md` (SHAs complets).
- Ce qui manque : B4b (200 nuls, non lancée — décision consignée
  §8.103.6) ; M1c et la fonction Delta(w) analytique (non testés) ;
  le livre blanc n'est pas modifié par ce fichier — section
  séparée, à fusionner par le coordinateur ; PDF non régénéré,
  rien poussé.

— Fin de la §8.103. —
