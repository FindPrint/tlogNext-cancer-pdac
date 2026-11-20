### 8.50 Consolidation de l'arbitrage MTAP — 10 nuls frais (19–20 novembre 2026)

**Verdict d'abord, en trois phrases. (a) TIENT — l'arbitrage du §8.46
est consolidé : sur 10 nuls FRAIS (graines 1011, 2022, 3033, 4044, 5055,
6066, 7077, 8088, 9099, 11111), l'écart S_sep réel − nul vaut au minimum
+0,1110, médiane +0,1595, maximum +0,1981 — 10/10 au-dessus du plancher
0,07, et 13/13 en regroupant les 3 nuls anciens. (b) La marge fragile du
§8.46 (+0,0715 contre le nul graine 7, soit 0,0015 au-dessus du plancher)
était la queue basse de la distribution nulle, pas la règle : le nul 7
reste le plus proche du réel sur 13 permutations, et le plus petit écart
frais (+0,1110) reste 0,0395 au-dessus du sien. (c) MC et Delta ne séparent
toujours pas, mais l'« inversion » du §8.46 ne se reproduit pas sur les
nuls frais : le MC réel (0,3511) dépasse 9 nuls frais sur 10 (médiane
nulle 0,3288), et le Delta réel (3,8051) est au bord inférieur d'un
amas nul très serré (9/10 entre 3,8010 et 3,8482). La marche de niveau
multi-flux reste ce que S_sep mesure ; S_sep la mesure désormais
contre une distribution nulle, pas contre trois tirages.**

## 8.50.1 Question, méthode, règles

**Question.** Le §8.46 a arbitré « S_sep VOIT DU RÉEL » (marche de niveau
multi-flux entre tumeurs MTAP-délétées et intactes, pas une rupture)
avec 3 nuls seulement et une marge fragile : l'écart S_sep contre le nul
graine 7 (+0,0715) ne dépassait le plancher 0,07 que de 0,0015. Avec
10 nuls frais, la distribution des écarts tient-elle au-dessus du
plancher, ou l'arbitrage s'effondre-t-il ?

**Méthode.** Protocole gelé `PROTOCOL_mtap_consolidation_850.md`
(SHA `13fec689…e2bb09`, écrit avant toute nouvelle construction et
tout nouveau run). Trois volets, dans l'ordre : (A) construction de
10 nuls frais par la même méthode que le nul graine 42 (lignes
permutées ensemble, `rng(seed)`, colonne MTAPCN intacte), graines
1011, 2022, 3033, 4044, 5055, 6066, 7077, 8088, 9099, 11111 — aucune
n'ayant servi pour un nul MTAP (les seules graines antérieures sont
42, 7 et 123) ; (B) 11 runs v6.2 fast — 1 réel de reproduction (sortie
distincte `results_fast_v62_mtap_850`, l'original n'est ni écrasé ni
effacé) + 10 nuls frais — lanceur reprenable `run_v62_lot.sh`,
manifeste `manifest_v62_mtap_nuls850.txt`, `systemd-run` (jamais
nohup) ; (C) lecture par un extracteur neuf
(`mtap_consolidation_850.py`) des 14 `master_results.json` (réel
original, réel 850, 3 nuls anciens, 10 nuls frais) et distribution
des écarts S_sep, avec re-vérification MC et Delta et recomposition
du MC composite.

**Règles de décision écrites avant (protocole §3, plancher 0,07 hérité
du §8.46, dépassement strict exigé).** Sur les 10 écarts FRAIS seuls :
**TIENT** si min > 0,07 ; **SE FRAGILISE** si médiane > 0,07 mais
min ≤ 0,07 ; **TOMBE** si médiane ≤ 0,07. La marche de niveau
multi-flux (d de groupe GISTIC, Spearman, §8.46 §8.46.4) n'est PAS
re-testée ici : elle vit dans les CSV, pas dans S_sep, et aucun
verdict de ce chantier ne la confirme ni ne l'infirme. Le verdict
§8.36 (pas de rupture, pas de chaîne KRAS sous l'ordre MTAP) n'est
pas touché.

**Incident de lot (traçabilité, pas silence).** Première unité
`mtap-nuls850` lancée le 19 nov. 2026 à 23:30:18Z : le réel 850 sort
en exit 0, puis la machine redémarre (~23:39–23:44Z, `uptime` 0 min
à 23:44:28Z) et tue l'unité en plein run s1011 (dossier de sortie
vide, pas de `master_results.json`, pas de ligne EXIT). Relance à
23:44:37Z sous l'unité `mtap-nuls850b` : le lanceur reprenable ignore
le réel 850 (déjà complet) et refait s1011, puis enchaîne les 9
autres. FIN 2026-11-20T01:18:26Z : déjà-faits 1, terminés 10,
échecs 0 — lot total 11/11, exit 0. Le surveillant
`watch_v62_mtap850.sh` (lancé 23:45Z, contrôle toutes les 60 s)
n'a eu aucune relance à faire après la reprise manuelle. SHA v6.2
`f07567c4…ec3abf` vérifié avant et après les runs (journal du lot).

## 8.50.2 (C) Distribution des écarts S_sep — TIENT, 10/10 au-dessus du plancher

Le réel de reproduction est **identique au chiffre près** à l'original
(S_sep 0,337775, MC 0,3511, Delta 3,8051, cascade 0,54 / 60,74 /
72,77 / 92,11 / 92,11 %, écart 0,00e+00) : v6.2 est déterministe sur
cette série, et la valeur du jour est 0,3378.

| Run | S_sep | max_separation | stabilité | Écart réel − nul |
|---|---|---|---|---|
| Réel (850) | **0,3378** | 0,3392 | 0,9959 | — |
| Nul s2022 | 0,2268 | 0,2272 | 0,9980 | **+0,1110** |
| Nul s1011 | 0,2254 | 0,2257 | 0,9986 | +0,1124 |
| Nul s3033 | 0,1901 | 0,1907 | 0,9970 | +0,1477 |
| Nul s11111 | 0,1832 | 0,1882 | 0,9734 | +0,1546 |
| Nul s8088 | 0,1788 | 0,1809 | 0,9882 | +0,1590 |
| Nul s5055 | 0,1778 | 0,1786 | 0,9958 | +0,1600 |
| Nul s7077 | 0,1724 | 0,1729 | 0,9976 | +0,1653 |
| Nul s6066 | 0,1638 | 0,1642 | 0,9978 | +0,1740 |
| Nul s4044 | 0,1555 | 0,1562 | 0,9959 | +0,1823 |
| Nul s9099 | 0,1397 | 0,1399 | 0,9989 | +0,1981 |
| Nul 42 (ancien) | 0,1409 | 0,1434 | 0,9825 | +0,1968 |
| Nul 7 (ancien) | 0,2663 | 0,2685 | 0,9919 | +0,0715 |
| Nul 123 (ancien) | 0,2031 | 0,2092 | 0,9705 | +0,1347 |

**Distribution des 10 écarts frais : min +0,1110, Q1 +0,1494,
médiane +0,1595, Q3 +0,1718, max +0,1981, moyenne +0,1564 ;
10/10 > 0,07, 0/10 ≤ 0,07, 0/10 ≤ 0.** Sur les 13 nuls regroupés :
min +0,0715 (le nul 7, toujours le plus proche), Q1 +0,1347,
médiane +0,1590, Q3 +0,1740, max +0,1981, moyenne +0,1513 ;
13/13 > 0,07. La condition TIENT du protocole (min frais > 0,07)
est remplie avec une marge de 0,0410 au-dessus du plancher sur le
plus petit écart frais — contre 0,0015 au §8.46. Les S_sep nuls
frais couvrent 0,1397–0,2268 (médiane 0,1783) : le réel (0,3378)
est à +0,1595 au-dessus de leur médiane, soit 89 % de plus.

**Corroboration à paramètres de scan FIXES.** La courbe par défaut
(mêmes paramètres des deux côtés) donne max_separation 0,2380
(réel) contre 0,0627–0,1255 (nuls frais) — écarts +0,1125 à
+0,1753, tous au-dessus du plancher aussi. Et 9 nuls frais sur 10
choisissent le MÊME `best_config` que le réel (93, 30, 6) : la
réserve du §8.46.3 (le `best_config` compare des configurations
différentes d'un run à l'autre) ne s'applique presque plus ici —
à configuration identique, le réel reste devant partout. Seul le
nul s11111 choisit (28, 27, 6), comme le nul 123 avant lui
(voir §8.50.3 : c'est aussi le nul atypique sur MC et Delta).

## 8.50.3 (C) Re-vérification MC et Delta — ni l'un ni l'autre ne sépare, mais l'inversion ne se reproduit pas

| Indicateur | Réel | Nuls frais (10) : min–max | Médiane nulle | Nuls frais > réel |
|---|---|---|---|---|
| MC best_score | 0,3511 | 0,3215–0,5192 | 0,3288 | 1/10 (s11111 : 0,5192) |
| Delta | 3,8051 | 3,0168–3,8482 | 3,8297 | 8/10 |
| L7a | DOWN 0,427 | 6 UP / 4 DOWN | — | ne sépare pas |
| Falsification | 0,733 | 0,542–0,772 | — | ne sépare pas |

**MC.** Le réel est DANS l'intervalle des nuls frais, mais au-dessus
de 9 d'entre eux : 9/10 se serrent entre 0,3215 et 0,3352 (médiane
0,3288, réel +0,0223 au-dessus). L'« inversion MC » du §8.46
(réel 0,3511 < nul 42 0,5153) ne se reproduit pas : sur les nuls
frais, le réel est le plus souvent DEVANT en MC, et un seul nul
(s11111, 0,5192) le dépasse — le même qui choisit la configuration
(28, 27, 6) et dont le Delta est l'outlier bas (voir ci-dessous).
Le MC composite se recompose exactement (écart 0,0) sur les 14 runs.
Conclusion honnête : MC ne sépare pas systématiquement (1 nul sur
10 devant, intervalle large), mais il ne contredit plus S_sep comme
au §8.46 — le désaccord tenait à deux permutations (42 et, dans une
moindre mesure, 123) qui produisent un pic étroit bien noté par le
composite.

**Delta.** Le réel (3,8051) est DANS l'intervalle des nuls frais et
sous leur médiane (−0,0246) : 8 nuls frais sur 10 sont au-dessus.
Mais 9 nuls frais sur 10 se serrent entre 3,8010 et 3,8482 — un
amas très étroit (largeur 0,047) dont le réel touche le bord
inférieur (3,8051, devant seulement s2022 à 3,8010). Le dixième,
s11111, est l'outlier bas à 3,0168 — le même run qui dépasse le
réel en MC. Delta ne sépare donc toujours rien sur cette série,
conformément au §8.42 (non élucidé) et au §8.46.5 : c'est une
largeur spectrale globale, pas une mesure de rupture. Le fait
nouveau est la concentration de l'amas nul (9/10 dans 0,047) :
la permutation ne déplace presque plus Delta quand la
configuration est (93, 30, 6) — les deux outliers historiques
(nul 42 : 4,3466 ; nul 123 : 3,1415) venaient de configurations
différentes, comme s11111 ici.

**L7a et falsification.** L7a frais : 6 UP, 4 DOWN — la direction
ne sépare pas (réel DOWN 0,427). Falsification frais : 0,542–0,772,
réel 0,733 dedans. Rien de nouveau de ces deux côtés.

## 8.50.4 Ce que ça change, et ce que ça ne change pas

**Change — l'arbitrage §8.46 passe de 3 tirages à une distribution.**
(1) La condition (1) du §8.46 (nuls frais sous le S_sep réel de plus
de 0,07) tient désormais sur 10 nuls frais avec une marge minimale
de 0,0410, et sur 13 nuls au total : la fragilité signalée au §8.46
était un tirage (le nul 7), pas la règle. S_sep peut désormais être
cité comme séparant le réel des nuls sur cette série, avec sa
distribution (médiane +0,1595, min +0,1110), pas avec un seul écart.
(2) Le statut de MC change de sens : au §8.46, MC « contredisait »
S_sep (inversion −0,1642 contre le nul 42) ; sur 10 nuls frais, le
réel est devant 9 fois sur 10. MC ne devient pas pour autant un
séparateur (un nul le dépasse largement), mais l'argument
« MC inversé » ne doit plus être cité sans la distribution
complète : il tenait à la configuration (28/46, 42/27) choisie par
deux permutations sur trois. (3) Delta reste non séparant, mais son
amas nul se révèle très serré (9/10 dans 0,047) dès que la
configuration est fixée — une régularité à noter pour une future
élucidation (§8.42), pas une séparation.
**Ne change pas.** Le verdict §8.36 est maintenu et précisé comme au
§8.46 : pas de rupture localisée, pas de chaîne KRAS sous l'ordre
MTAP — une marche de niveau multi-flux, que S_sep mesure et que
MC/Delta ne mesurent pas. Le rationnel vopimetostat + daraxonrasib
n'est ni renforcé ni affaibli par ce chantier (il vit dans les
lignées et la clinique, pas dans cette série). S_sep ne devient pas
un discriminateur général recommandé : il sépare ici, sur cette
série et ce contrôle, contre 13 permutations — rien de plus.
**Reste ouvert :** pourquoi la configuration (28, 27, 6) — choisie
par les nuls 123 et s11111 — produit à la fois un MC élevé et un
Delta bas (s11111) ou un S_sep intermédiaire (123) ; pourquoi la
permutation élargit d_div (§8.42, §8.46.5) ; et la distribution
nulle reste empirique (13 permutations, quantiles bruités).

## 8.50.5 Provenance

- **Protocole gelé.** `PROTOCOL_mtap_consolidation_850.md` (SHA-256
  `13fec689a69f9d7b1c7307e2968e2b25f323b070f2cff3a0c1323c385de2bb09`),
  écrit avant toute construction et tout run de ce chantier.
- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant et après les runs, journal du lot) ; v6.1 de référence
  `2af5e5ce…c1c9`. Scripts neufs : `build_mtap_nuls_850.py` (SHA-256
  `23d7af20537f568ac806eb925258d105ed8d3301d4a38a72c1a92024ea2dcf94`),
  `mtap_consolidation_850.py` (SHA-256
  `276f9ff31c8ec40cedca1a97d76437714a0423eb12307ebb758fd2a31729cf7d`).
- **Entrées (SHA-256 vérifiés avant les calculs).** Série MTAP :
  `pdac_tcga_fluxes_v4_mtap.csv`
  `578b8d3b9b26099d0784ed23754d1cc9717be7f9292eb47e201d186cdbc90df6`
  (177 tumeurs, Broad GDAC Firehose stddata 2016-01-28, PAAD, RSEM ;
  GISTIC2 Level 4 ; 177/178 appariées — voir PROVENANCE_mtap_series.md).
  Nuls frais (lignes permutées ensemble, MTAPCN intact) :
  s1011 `e074becc…975a4`, s2022 `81663ffd…ebb3`, s3033 `fb42718d…b131`,
  s4044 `58eee570…0ecd`, s5055 `e3de4a84…91d80`, s6066 `734b4845…064a`,
  s7077 `70f9a8e8…fddde3c`, s8088 `fea69d43…8959`, s9099 `727bd3f0…65a`,
  s11111 `c7c1739d…958c0` (SHA complets dans la sortie du script de
  construction). Nuls anciens relus tels quels : 42
  `e6786a47…453b9`, s7 `cacce06f…904d3`, s123 `da2b1d3f…626c1`.
- **Sorties.** Runs frais : `results_fast_v62_mtap_850/` (réel de
  reproduction, identique à l'original) et
  `results_fast_v62_mtap_nul_s<graine>/` pour les 10 graines
  (`master_results.json` chacun) ; manifeste
  `manifest_v62_mtap_nuls850.txt` ; journal
  `runs_v62_mtap_nuls850.log` (11/11, exit 0 ; unités systemd
  `mtap-nuls850` — tuée par le redémarrage machine en plein s1011 —
  puis `mtap-nuls850b`, FIN 2026-11-20T01:18:26Z) ; surveillant
  `watch_v62_mtap850.sh` (aucune relance nécessaire après la reprise).
  Lecture : `mtap_consolidation_850_extract.json` (SHA-256
  `89ad1000bf4bde40d530e74d6c709486147fd452d734627dda4347450ab046f9`),
  `mtap_consolidation_850_results.csv` (SHA-256
  `e8825cd87acccb2ba299ededd41aa16661e5c642980837e6050930a36871deb1`,
  14 runs + statistiques).
- **Nature des lignes.** Résidus d'expression TCGA (mesures
  instrumentales — séquençage ARN — transformées) ordonnés par CN
  MTAP ; nuls = lignes permutées (échantillons hypothétiques, pas des
  mesures) ; aucune autre donnée nouvelle dans ce chantier (aucun
  test direct PRMT5/prolifération refait — voir §8.46.7).
- **Ce qui manque, ce qui reste ouvert.** 13 permutations seulement
  (quantiles bruités ; le plancher 0,07 est un critère hérité du
  §8.46, pas une loi physique, sans normalisation par la dispersion
  nulle) ; S_sep ≈ max_separation (stabilité 0,97–1,00) reste un
  maximum sur les seuils, sensible au `best_config` — atténué ici
  par 9/10 nuls frais dans la même configuration que le réel ;
  le mécanisme « configuration (28, 27, 6) → MC haut, Delta bas »
  et « permutation élargit d_div » ne sont pas élucidés ; PDF non
  régénéré, rien poussé sur GitHub (hors de ce chantier).

— Fin de la §8.50. —
