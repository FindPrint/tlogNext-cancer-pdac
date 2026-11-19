### 8.46 Arbitrage de la contradiction MTAP — S_sep contre MC/Delta (19 novembre 2026)

**Verdict d'abord, en trois phrases. (a) ARBITRÉ : S_sep voit quelque chose
de réel — une marche de niveau multi-flux entre tumeurs MTAP-délétées et
intactes (CEACAM5, CLDN18, DPCR1, MUC17, MUC16 plus hauts côté délété,
d de Cohen jusqu'à +0,74, gradients de Spearman jusqu'à −0,39, nul plat),
et non une rupture localisée. (b) MC et Delta ne contredisent pas cette
marche : l'inversion MC est portée par le seul terme de robustesse
(FWHM 78,26 % réel contre 11,11 % nul graine 42 — le pic réel est haut
mais large, le MC récompense un pic étroit), et Delta est une largeur
spectrale globale sans rapport avec un seuil (réel 3,8051, à l'intérieur
de l'intervalle des trois nuls 3,14–4,35). (c) Le nul graine 42 était
extrême sur les trois indicateurs à la fois (S_sep le plus bas, MC et
Delta les plus hauts des trois nuls) : avec les nuls frais graines 7 et
123, les trois écarts s'effondrent ou changent de signe — S_sep
+0,072/+0,135, MC +0,009/−0,101, Delta −0,003/+0,664. Le verdict §8.36
est donc PRÉCISÉ, pas renversé : pas de rupture, pas de chaîne — mais
une différence de niveau réelle, que S_sep mesure et que MC/Delta ne
mesurent pas. Marge fragile, à lire avec le verdict : l'écart S_sep
contre le nul graine 7 (+0,0715) ne dépasse le plancher 0,07 que de
0,0015 — un quatrième nul pourrait le faire tomber sous le plancher.**

## 8.46.1 Question, méthode, règles

**Question.** Sur la série TCGA v4 ordonnée par CN MTAP (177 tumeurs,
contrôle MTAPCN, §8.36), S_sep = +0,1968 (réel > nul graine 42) alors
que MC = −0,1642 et Delta = −0,5416 sont inversés (§8.38). S_sep voit-il
quelque chose de réel que MC/Delta ratent, ou est-ce un artefact de
construction de S_sep ?

**Méthode.** Protocole gelé `PROTOCOL_mtap_arbitration_ssep.md`
(SHA `9cf3295a…`, écrit avant tout nouveau calcul et tout nouveau run).
Six volets, dans l'ordre : (A) relecture vérifiée des runs v6.2 et
recomposition du MC composite ; (B) forme du scan (FWHM recalculée) ;
(C) loupe par loupe depuis les CSV (harnais, hors pipeline) ; (D)
décomposition de Delta (D-vector, estimateur par estimateur) ;
(E) deux nuls frais (graines 7 et 123), seuls nouveaux runs ;
(F) tests directs PRMT5 contre MTAP avec et sans contrôle prolifération,
et relecture des 4 confirmations « PRMT5 suit MTAP, pas CDKN2A ».
Règles de décision écrites avant (protocole §4) : « S_sep VOIT DU RÉEL »
exige (1) les deux nuls frais sous le S_sep réel de plus de 0,07,
(2) ≥ 2 flux portant la séparation avec un support direct, (3) le
mécanisme nommé. Les trois conditions sont remplies (voir §8.46.6) —
avec la réserve de marge sur (1), consignée dans le verdict.

**Corrections trouvées en cours de route (traçabilité, pas silence).**
(1) Le protocole §1 disait que d_sat/d_div étaient des médianes T_log :
c'est FAUX — le code (`compute_holographic_tension_state`, lignes
~7990–8022) montre que ce sont des médianes BRUTES de dimensions
(médiane des médianes par estimateur) et que Delta = d_div − d_sat en
unités brutes ; T_log est une transformée séparée, rapportée ailleurs.
La correction est appliquée partout ci-dessous, et la conclusion (Delta
global, sans rapport avec un seuil) en sort renforcée, pas affaiblie.
(2) Piège pandas attrapé dans le volet F : `read_csv(usecols=[...])`
rend les colonnes dans l'ordre DU FICHIER, pas dans l'ordre demandé —
un premier renommage positionnel échangeait PRMT5 et ACTB et donnait
un F1 inversé (médianes −0,558/−0,610, p = 0,60). Corrigé par renommage
PAR LE NOM, avec vérification ligne à ligne contre la table §8.40
(écart max 5,67×10⁻⁸ sur CN, 1,12×10⁻⁷ sur PRMT5). Le premier calcul
faux n'est cité nulle part comme résultat.

## 8.46.2 (A) Relecture vérifiée — le MC composite se recompose à l'identique

| Indicateur | Réel | Nul graine 42 | Nul graine 7 | Nul graine 123 |
|---|---|---|---|---|
| S_sep = max_sep × stabilité | **0,3378** | 0,1409 | 0,2663 | 0,2031 |
| max_separation | 0,3392 | 0,1434 | 0,2685 | 0,2092 |
| stabilité | 0,9959 | 0,9825 | 0,9919 | 0,9705 |
| MC best_score (seuil) | 0,3511 (69,57 %) | 0,5153 (84,44 %) | 0,3422 (89,13 %) | 0,4518 (88,89 %) |
| s_norm / robustesse / acuité | 0,1680 / 3,37×10⁻⁴¹ / 0,0099 | 0,0716 / 0,9756 / 0,0198 | 0,1334 / 3,37×10⁻⁴¹ / 0,0231 | 0,1042 / 0,6290 / 0,0177 |
| Delta (d_div − d_sat) | 3,8051 | 4,3466 | 3,8085 | 3,1415 |
| D-vector (sat / crit / div / null) | 1,578 / 3,240 / 5,383 / 2,506 | 1,594 / 3,325 / 5,940 / 2,509 | 1,599 / 3,194 / 5,407 / 2,480 | 1,572 / 3,202 / 4,713 / 2,483 |
| Cascade T_-2 / T_-1 / T_0 / T_+1 / T_+2 (%) | 0,54 / 60,74 / 72,77 / 92,11 / 92,11 | 1,07 / 2,14 / 8,57 / 15,58 / 15,58 | 1,07 / 8,03 / 95,79 / 98,79 / 100,0 | 0,0 / 10,71 / 61,18 / 90,01 / 90,01 |
| L7a | DOWN 0,427 | UP 0,331 | DOWN 0,413 | UP 0,412 |
| Falsification delta_vs_null | 0,733 | 0,816 | 0,714 | 0,719 |

Écarts réel − nul : **S_sep +0,1968 / +0,0715 / +0,1347** ;
**MC −0,1642 / +0,0089 / −0,1006** ; **Delta −0,5416 / −0,0034 / +0,6636**.
Le réel est au-dessus des trois nuls en S_sep, mais DANS l'intervalle
des trois nuls en MC (0,342–0,515 ; réel 0,351) comme en Delta
(3,14–4,35 ; réel 3,81). La « contradiction » du §8.38 est spécifique
au nul graine 42 : c'est le seul des trois nuls qui soit à la fois le
plus bas en S_sep et le plus haut en MC et en Delta. Avec le nul graine
7, les trois écarts s'effondrent (+0,072 / +0,009 / −0,003) ; avec le
nul graine 123, Delta change de signe (+0,664).

**Le MC se recompose exactement** (écart 0,0 sur les 4 runs) depuis
0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·acuité (poids par
défaut, code lignes 3727–3730 et 3481–3484). Décomposition de
l'inversion MC contre le nul 42 : s_norm favorise le réel (+0,029),
stabilité est quasi égale (+0,004), acuité favorise le nul (+0,002),
**robustesse favorise le nul de +0,195 (0,2×0,9756 contre ~0)** — à
elle seule, elle porte l'inversion (−0,164). Contre le nul graine 7,
la robustesse est IDENTIQUE au réel (3,37×10⁻⁴¹ des deux côtés) et
l'écart MC tombe à +0,009.

**À paramètres de scan FIXES, le réel gagne partout.** La courbe par
défaut (mêmes paramètres des deux côtés) donne max_separation
0,2380 (réel) contre 0,0861 / 0,1548 / 0,1023 (nuls) — écarts
+0,152 / +0,083 / +0,136. Et sur les 12 itérations MC — dont les
configurations (n_candidats, w_size, min_grp) sont IDENTIQUES pour les
4 runs (échantillonneur seedé, graine globale 42) — le réel gagne en
max_separation 12/12 contre chaque nul, et en score MC 8/12 contre le
nul 42, 12/12 contre le nul 7, 10/12 contre le nul 123. Les seules
itérations perdues en MC sont celles où le nul produit un pic étroit
(robustesse ~0,6–0,98 : itérations 1, 4, 6, 10 pour le nul 42 ;
4 et 10 pour le nul 123 ; aucune pour le réel ni pour le nul 7).

## 8.46.3 (B) Forme du scan — le pic réel est haut et large, pas localisé

FWHM recalculée depuis chaque `scan_curve.json` en répliquant
`evaluate_scan_quality` (code lignes 3314–3390) ; les valeurs
recalculées reproduisent les métriques lues (robustesse, stabilité,
acuité) au chiffre près.

| Run | Candidats scorés | Max (seuil) | FWHM | Au-dessus de la moitié du max | Médiane des scores |
|---|---|---|---|---|---|
| Réel | 73/93 | 0,3392 (69,57 %) | **78,26 %** | **73/73** | 0,2899 |
| Nul 42 | 32/46 | 0,1434 (84,44 %) | 11,11 % | 30/32 | 0,0935 |
| Nul 7 | 73/93 | 0,2685 (89,13 %) | **78,26 %** | **73/73** | 0,2132 |
| Nul 123 | 22/28 | 0,2092 (88,89 %) | 14,81 % | 18/22 | 0,1331 |

Le scan réel ne descend JAMAIS sous la moitié de son max : de 10,87 %
à 89,13 %, le score reste entre 0,219 et 0,339. Ce n'est pas un pic,
c'est un plateau — la signature d'une différence de niveau stable sur
tout l'axe, pas d'une rupture localisée. Le nul graine 7 a EXACTEMENT
la même forme (FWHM 78,26 %, 73/73 au-dessus de la moitié, même
configuration best (93, 30, 6), même robustesse 3,37×10⁻⁴¹) : un nul
permuté produit le même plateau, à un niveau plus bas (max 0,269 contre
0,339, médiane 0,213 contre 0,290).

**La robustesse est, en régime plateau, déterminée par la configuration,
pas par les données.** Les 12 robustesses par itération sont IDENTIQUES
entre le réel et le nul graine 7 (les 12 valeurs, de 9,65×10⁻²³ à
3,37×10⁻⁴¹) : quand la courbe ne descend jamais sous la moitié du max,
la FWHM vaut la plage des candidats scorés, qui ne dépend que de
(n_candidats, w_size, min_grp). La robustesse ne devient informative
que quand la courbe descend sous la moitié du max — ce qui arrive pour
certaines paires (données, configuration) et pas d'autres. Conséquence :
le `best_config` compare des configurations DIFFÉRENTES d'un run à
l'autre — réel (93, 30, 6), nul 42 (46, 42, 7), nul 123 (28, 27, 6),
nul 7 (93, 30, 6) — choisies par un composite qui récompense un pic
étroit. L'inversion MC est un artefact de ce choix de « meilleur » :
à configuration fixée, le réel est devant partout (§8.46.2).

## 8.46.4 (C) Loupe par loupe — une marche de niveau multi-flux, pas 1–2 flux

**C1 — d de Cohen par flux au seuil MC (pas 122 réel / 149 nul 42).**
Lecture directe depuis les CSV ; le partage entier pré/post est une
APPROXIMATION du score fenêtré du pipeline (qui donne 0,339 contre
0,143), pas sa réplique exacte — les deux vont dans le même sens, et
l'approximation donne des valeurs plus grandes (0,392 contre 0,247).

| Flux | Réel (entier) | Nul 42 (entier) | Réel (±20) | Nul 42 (±20) |
|---|---|---|---|---|
| CEACAM5 | −0,772 | +0,536 | −0,270 | +0,624 |
| CLDN18 | −0,678 | +0,271 | −0,469 | +0,364 |
| MUC17 | −0,619 | +0,111 | −0,662 | −0,003 |
| DPCR1 | −0,518 | +0,157 | −0,117 | −0,100 |
| MUC16 | −0,428 | +0,261 | +0,018 | +0,393 |
| REG4 | −0,320 | +0,229 | −0,341 | +0,355 |
| GSTM1 | −0,320 | +0,263 | −0,356 | +0,794 |
| MUC2 | −0,297 | +0,318 | −0,538 | +0,677 |
| KRT20 | −0,230 | +0,231 | −0,386 | +0,169 |
| CR2 | +0,231 | −0,219 | −0,325 | −0,354 |
| PGC | −0,188 | −0,097 | −0,384 | −0,199 |
| CLCA1 | −0,103 | +0,265 | −0,500 | +0,249 |
| Moyenne \|d\| | **0,392** | 0,247 | 0,364 | 0,357 |

Signe : après − avant (négatif = plus haut côté délété, avant le seuil).
Le réel est porté par 8 flux pour 80 % de la séparation (part du top
16 %) — H3 (1–2 flux) est REJETÉE. Réserve honnête : en fenêtres ±20,
réel (0,364) et nul (0,357) sont quasi égaux — la lecture fenêtrée
locale ne sépare pas ; c'est le partage entier (niveau global) qui
sépare. C'est cohérent avec une marche, pas avec un pic.

**C2 — groupes GISTIC (jointure exacte par code-barres, reconstruite
depuis les tarballs ; colonne MTAPCN reproduite à 10⁻¹² près ;
GISTIC seuillé sur 177 : −2 : 43, −1 : 62, 0 : 69, +1 : 2, +2 : 1).**
d de Cohen (délétées − intactes ; positif = plus haut chez les délétées) :

| Flux | −2/−1 (n=105) vs 0/+ (n=72), réel | même, nul 42 | −2 (n=43) vs reste, réel | Top-12 vs reste, réel |
|---|---|---|---|---|
| CEACAM5 | **+0,740** | −0,115 | +0,546 | +0,585 |
| CLDN18 | **+0,634** | −0,045 | +0,178 | +0,012 |
| DPCR1 | **+0,476** | −0,045 | +0,215 | −0,078 |
| CR2 | −0,462 | +0,163 | −0,333 | −0,570 |
| MUC17 | **+0,442** | +0,095 | +0,248 | +0,185 |
| MUC16 | **+0,387** | +0,042 | +0,393 | −0,143 |
| REG4 | +0,278 | +0,008 | +0,301 | +0,238 |
| GSTM1 | +0,146 | +0,229 | +0,371 | +0,063 |
| KRT20 | +0,109 | −0,003 | +0,142 | −0,146 |
| MUC2 | +0,111 | +0,080 | +0,007 | −0,026 |
| PGC | +0,058 | +0,096 | −0,304 | −0,399 |
| CLCA1 | −0,046 | +0,016 | +0,010 | −0,010 |

Le nul 42 reste à |d| ≤ 0,23 sur les deux groupements GISTIC. Cinq flux
dépassent +0,38 en réel sur le groupement large (−2/−1 contre 0/+),
tous dans le même sens (plus hauts chez les délétées), et le top-12
reproduit le §8.36 au chiffre près (CEACAM5 +0,585, CR2 −0,570,
PGC −0,399). C'est une différence de NIVEAU entre deux groupes
biologiques (perte MTAP contre intact), pas un saut à un seuil : les
mêmes flux sont décalés sur tout l'axe.

**C3 — Spearman flux contre rang MTAP.** Réel : CEACAM5 −0,390
(p = 8,1×10⁻⁸), CLDN18 −0,270 (p = 2,8×10⁻⁴), MUC16 −0,270,
DPCR1 −0,262, MUC17 −0,219, REG4 −0,181 (p = 0,016), CR2 +0,184
(p = 0,014), MUC2 −0,118, GSTM1 −0,054, KRT20 −0,049, PGC −0,025,
CLCA1 −0,007. Nul 42 : tous |rho| ≤ 0,096, tous p ≥ 0,21. Les flux
montent en pente douce et monotone quand CN MTAP baisse — sans saut
chez les 12 plus délétées, comme déjà dit au §8.36.

## 8.46.5 (D) Décomposition de Delta — l'inversion vient de d_div seul

Delta = d_div − d_sat (médianes brutes de dimensions). Réel contre
nul 42 : d_sat 1,578 contre 1,594 (Δ −0,016), d_crit 3,240 contre 3,325
(Δ −0,086), **d_div 5,383 contre 5,940 (Δ −0,557)**, d_null 2,506 contre
2,509 (Δ −0,003). L'inversion Delta (−0,542) est portée à 103 % par
d_div. Le D-vector est reproduit exactement par la médiane des
médianes brutes par estimateur (saturation 1,5781 contre 1,578056 lu).
Par estimateur (écart réel − nul 42) : divergence — MFA −1,000
(niveau discret 3 contre 4), LocalPCA −0,494, PCAIntrinsic −0,328,
LevinaBickel +0,204, GraphDimension −0,069, PersistentHomology −0,078 ;
saturation — tous |Δ| ≤ 0,126 (BoxCounting −0,126) ; criticality —
Fisher −0,491, CorrelationD2 et GrassbergerProcaccia −0,193, TwoNN
+0,246, InformationD1 −0,093, DANCo −0,086, VisibilityGraph +0,025 ;
SpectralDimension −0,003. Delta ne dépend d'aucun seuil : c'est une
largeur spectrale globale de la matrice entière, et le nul permuté
l'élargit (surtout via MFA et LocalPCA, des estimateurs de dimension
qui lisent plus haut sur des lignes mélangées). Avec trois nuls, le
réel (3,805) est à l'intérieur de l'intervalle nul (3,14–4,35) :
Delta ne sépare rien sur cette série. Ceci est cohérent avec le §8.42
(Delta non élucidé, magnitudes portant l'échelle de n) — il n'explique
pas POURQUOI la permutation élargit d_div, il constate OÙ elle
l'élargit.

## 8.46.6 (E) Deux nuls frais — le nul graine 42 était extrême

Construction : même méthode que le nul graine 42 (lignes permutées
ensemble, `rng(seed)`, colonne MTAPCN intacte), graines 7 et 123,
script `build_mtap_nuls_846.py`. Runs v6.2 fast : lot lancé par
`systemd-run` (unité `mtap-nuls846`, jamais nohup), 19 nov. 2026
21:34:25Z ; s7 exit 0 ; 1re tentative s123 tuée par un redémarrage du
service (pas de `master_results.json`, pas de ligne EXIT) ; relance
par `systemd-run` (unité `mtap-nuls846b`, s7 ignoré car complet),
FIN 2026-11-19T21:53:04Z, terminés=1, échecs=0 — lot total 2/2, exit 0.
SHA v6.2 `f07567c4…ec3abf` vérifié avant et après (journal du lot).

| Écart réel − nul | Nul 42 | Nul 7 | Nul 123 | Moyenne des 3 nuls |
|---|---|---|---|---|
| S_sep | +0,1968 | +0,0715 | +0,1347 | réel 0,3378 contre moyenne 0,2034 |
| MC | −0,1642 | +0,0089 | −0,1006 | réel 0,3511 contre moyenne 0,4364 |
| Delta | −0,5416 | −0,0034 | +0,6636 | réel 3,8051 contre moyenne 3,7656 |

La condition (1) du protocole est remplie : les deux nuls frais
restent sous le S_sep réel de plus de 0,07 — mais de justesse pour le
nul 7 (+0,0715, soit 0,0015 au-dessus du plancher). La condition (2)
est remplie nettement : ≥ 5 flux avec support direct (C2/C3). La
condition (3) est remplie : MC = forme du pic (robustesse), Delta =
largeur spectrale globale — ni l'un ni l'autre ne nie la hauteur vue
par S_sep. **Verdict du protocole : ARBITRÉ — S_sep VOIT DU RÉEL**,
précisé ainsi : ce qu'il voit est une marche de niveau, pas une
rupture. Le L7a illustre la même variabilité du nul : DOWN réel
(0,427) et DOWN nul 7 (0,413) contre UP nul 42 (0,331) et UP nul 123
(0,412) — la direction L7a ne sépare pas non plus. La falsification
ne sépare pas davantage (réel 0,733 ; nuls 0,816 / 0,714 / 0,719).

## 8.46.7 (F) Tests directs — l'effet PRMT5 survit au contrôle prolifération

**F1 — reproduction §8.40.** 47 lignées pancréas DepMap 24Q4
(OncotreeLineage Pancreas, jointure GeneEffect/CN) : PRMT5 Chronos
délétées profondes (CN < 0,5, n = 20) médiane −1,385 contre intactes
(n = 27) −1,010, Mann-Whitney p = 0,003551 ; Spearman continu
rho = +0,497, p = 0,000376. Reproduit au chiffre près.

**F2 — contrôle prolifération, lignées.** Proxy gelé : médiane des
Chronos MKI67/TOP2A/PCNA/CCNB1 par lignée (mêmes 4 gènes que le score
TCGA §8.25c, mais en dépendance CRISPR, pas en expression — la
différence est nommée, le proxy est une hypothèse de travail, pas une
vitesse de division mesurée ; médiane du proxy −1,555, 0 NaN).
Spearman partiel PRMT5 ~ CN MTAP : brut rho = 0,497 (p = 0,00038) →
**partiel prolif rho = 0,445 (p = 0,0019, n = 47)** ; partiel KRAS
rho = 0,500 (p = 0,00041) ; partiel prolif + KRAS rho = 0,447
(p = 0,0021). L'effet perd ~10 % et reste significatif : il n'est
pas un confondant prolifération. CDKN2A fixé (MTAP-intacte, par CN) :
p = 0,464 (n = 7/20, méd −1,049/−0,984) — reproduit le §8.40 (0,46).

**F3 — contrôle prolifération, tumeurs TCGA.** Score §8.25c (médiane
des résidus MKI67/TOP2A/PCNA/CCNB1 ; jointure exacte par code-barres,
score reproduit à 10⁻⁹ près) : Spearman score ~ CN MTAP rho = −0,268
(p = 0,00031) — les tumeurs les plus délétées sont un peu plus
proliférantes ; d du score top-12 contre reste +0,218 (petit). Mais
les gradients flux ~ MTAP survivent au contrôle : CEACAM5 −0,390 →
−0,336 (p = 5,2×10⁻⁶), CLDN18 −0,270 → −0,237, MUC16 −0,271 → −0,212,
DPCR1 −0,263 → −0,254, MUC17 −0,220 → −0,175, REG4 −0,182 → −0,156,
CR2 +0,184 → +0,146. Atténuation de 10 à 20 %, pas d'élimination.
Partiels du nul 42 : tous |rho| ≤ 0,044.

**F4 — relecture des 4 confirmations « PRMT5 suit MTAP, pas CDKN2A ».**
Chaque valeur est RELUE dans son fichier source, pas recopiée :
§8.28 — `data/prmt5_mtap_results.csv`, pancréas profond : −1,385 /
−1,010, p = 0,003551. §8.29 — stratification CN pan-cancer, relue
dans `mtap_arbitration_840_results.csv`, ligne a3 (recomputation
§8.40 de cette stratification) : MTAP-intacte, n = 137/747,
−1,013 / −0,973, p = 0,257009. §8.36 — stratification mutation,
relue dans `mtap_arbitration_840_results.csv` ligne a4 et
`verify_alleles_mutations.txt` : MTAP-intacte, n = 10/15, −0,978 /
−1,010, p = 0,760301, d = +0,19. §8.40 — stratification CN pancréas,
même fichier, ligne a3 : n = 7/20, −1,049 / −0,984, p = 0,464000.
Quatre confirmations, quatre relectures exactes, deux angles (CN et
mutation) et deux échelles (pancréas et pan-cancer). La strate
MTAP-délétée ne peut pas être testée dans l'autre sens (20/0 en
pancréas, 293/1 au pan-cancer) — dit au §8.40, inchangé.

## 8.46.8 Ce que ça change, et ce que ça ne change pas

**Change — la contradiction est arbitrée, et le mécanisme est nommé.**
(1) S_sep mesure la HAUTEUR d'une marche de niveau réelle entre deux
groupes (perte MTAP contre intact) ; MC mesure la FORME d'un pic et
pénalise le plateau ; Delta mesure une LARGEUR spectrale globale. Les
trois sont exacts, ils ne se contredisent pas — ils ne mesurent pas la
même chose. (2) Le nul graine 42 ne doit plus être cité seul : sur
cette série, un nul = une permutation, et les trois nuls détenus
couvrent S_sep 0,141–0,266, MC 0,342–0,515, Delta 3,14–4,35. Toute
comparaison réel/nul sur un seul nul est fragile — ici, la conclusion
« MC et Delta inversés » tenait à UNE permutation. (3) La robustesse
du MC, en régime plateau, est déterminée par la configuration de scan,
pas par les données : le `best_config` ne doit pas être comparé entre
runs sans comparer aussi les configurations choisies.
**Ne change pas.** Le verdict §8.36 (la chaîne KRAS ne réapparaît pas
sous l'ordre MTAP ; pas de rupture localisée) est maintenu et précisé :
une marche de niveau n'est pas une rupture, et la chaîne reste propre
à l'axe KRAS. Le rationnel vopimetostat + daraxonrasib n'est ni renforcé
ni affaibli par ce chantier (il vit dans les lignées et la clinique,
pas dans cette série). S_sep ne devient pas un discriminateur général
recommandé : il sépare ici à configuration fixée (12/12 en maxsep
contre les trois nuls), mais sa marge contre le nul graine 7 est de
0,0015 au-dessus du plancher — un seul nul de plus pourrait renverser
la condition (1). **Reste ouvert :** pourquoi la permutation élargit
d_div (MFA discret 3 contre 4 en tête) — le §8.42 ne l'élucide pas
non plus ; et la distribution nulle complète (3 nuls seulement ici).

## 8.46.9 Provenance

- **Protocole gelé.** `PROTOCOL_mtap_arbitration_ssep.md` (SHA-256
  `9cf3295aea379d4df4c8acaa6afaf6b0410c6bb56b20a03c956cb9952693fed7`),
  écrit avant tout calcul et tout run de ce chantier.
- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant et après les runs, journal du lot) ; v6.1 de référence
  `2af5e5ce…c1c9`. Scripts neufs : `mtap_arbitration_846.py` (SHA-256
  `8e9c5382a768dd78c85a239d354e664a347e8be2ee772a164575599709164fc4`),
  `build_mtap_nuls_846.py` (SHA-256
  `6eeec29088bba5745b5603f16fbba0077b565d49f13462a50cfc4cd65eba3083`).
  Deux lancements antérieurs du script d'arbitrage documentés ici :
  un arrêt sur une erreur de lecture DepMap (colonnes, voir §8.46.1),
  puis un arrêt sur une assertion trop stricte (écart 10⁻⁷), puis un
  run tué par le redémarrage du service — le run final est complet,
  exit 0, 2 min 05 s.
- **Entrées (SHA-256 vérifiés avant les calculs).** Série MTAP :
  `pdac_tcga_fluxes_v4_mtap.csv`
  `578b8d3b9b26099d0784ed23754d1cc9717be7f9292eb47e201d186cdbc90df6`,
  nul graine 42
  `e6786a47ce107dbf9785d83981ab413f8afb4e75fbdbae4da56da8c1e46453b9`
  (PROVENANCE_mtap_series.md : Broad GDAC Firehose stddata 2016-01-28,
  PAAD, RSEM ; GISTIC2 Level 4 ; 177/178 appariées, TCGA-FB-A4P6-01
  sans GISTIC). Nuls frais : `pdac_tcga_fluxes_v4_mtap_nul_s7.csv`
  `cacce06f455a74450e74032f9103d9ebea9f730065fc9d4f1921a896957904d3`,
  `..._nul_s123.csv`
  `da2b1d3f6b4f6cb91c2888a0704a36b397ea1782ef8bc4c980a89d920c2626c1`.
  DepMap Public 24Q4 (figshare 27993248) : `CRISPRGeneEffect.csv`
  `3d8f3ec6…167e3b`, `OmicsCNGene.csv` `4851d3e9…134c`, `Model.csv`
  `b7a0c138…dcfa`. Tarballs TCGA revérifiés par MD5 dans la
  reconstruction (RSEM `b09569ce…`, GISTIC préfixe `816034f7…`).
- **Sorties.** Runs frais : `results_fast_v62_mtap_nul_s7/` et
  `results_fast_v62_mtap_nul_s123/` (`master_results.json` chacun) ;
  manifeste `manifest_v62_mtap_nuls846.txt` ; journal
  `runs_v62_mtap_nuls846.log` (2/2, exit 0) ; unités systemd
  `mtap-nuls846` (1re tentative s123 tuée par redémarrage) et
  `mtap-nuls846b` (reprise, FIN 2026-11-19T21:53:04Z). Lecture :
  `mtap_arbitration_846_extract.json` (SHA-256
  `db8b25acec563e39fa17b04385fe67c8bc9721a75c43528ab2ab20505d9076c6`),
  `mtap_arbitration_846_results.csv` (SHA-256
  `7b4e44d4851fade4408a917587ad176ce341bed6722779b98c56b4843a14e1ff`,
  252 lignes), `mtap_arbitration_846_prolif.csv` (SHA-256
  `6bb10b85b968c0344a882c9a8f53c61e455a3204842b4255e061bc2726126401`,
  26 lignes), `mtap_arbitration_846_patients.csv` (SHA-256
  `29ad89741f4416b6e752ecb2956ea6f5c1939e76d5c55cd0d5f0e964a74e2ae3`,
  177 lignes : barcode, MTAPCN, GISTIC seuillé, score prolifération).
- **Nature des lignes.** Résidus d'expression TCGA (mesures
  instrumentales — séquençage ARN — transformées) ordonnés par CN
  MTAP ; nuls = lignes permutées (échantillons hypothétiques, pas des
  mesures) ; Chronos, CN DepMap, viabilités = mesures instrumentales ;
  statuts GISTIC = appels mesurés ; score de prolifération TCGA =
  médiane de résidus (mesure transformée) ; proxy prolifération
  lignées = médiane de Chronos (hypothèse de travail, limite nommée
  au §8.46.7). Aucun mot humain, aucun échantillon hypothétique dans
  les séries réelles.
- **Ce qui manque, ce qui reste ouvert.** Trois nuls seulement (la
  condition (1) tient à 0,0015 près sur le nul 7) ; la C1 fenêtrée
  ±20 ne sépare pas (0,364 contre 0,357) alors que le partage entier
  sépare — la décomposition par flux est une approximation du score
  fenêtré du pipeline, pas sa réplique exacte ; le mécanisme
  « permutation élargit d_div » n'est pas élucidé (MFA discret en
  tête) ; le proxy prolifération lignées n'est pas une vitesse de
  division mesurée ; PDF non régénéré, rien poussé sur GitHub (hors
  de ce chantier).

— Fin de la §8.46. —
