### 8.43 Série MTAP avec la dépendance PRMT5 comme flux : NON, la chaîne ne réapparaît pas (19 novembre 2026)

**Verdict d'abord, en trois phrases. (a) Le pipeline ne sépare pas le réel
du nul sous l'ordre PRMT5 : MC quasi identiques (0,3390 contre 0,3386,
écart +0,0004), et S_sep, max_separation et Delta sont tous meilleurs au
nul — S_sep 0,1897 contre 0,2874 (écart −0,0977), max_separation 0,1919
contre 0,2955 (écart −0,1036), Delta 1,761 contre 1,912 (écart −0,151) —
au-delà de la gigue mesurée 0,00 en v6.2. (b) Les tests directs ne
retrouvent pas la chaîne KRAS : chez les 12 lignées les plus
PRMT5-dépendantes, PGC monte (+0,45, sens inverse de l'axe KRAS où il
s'effondre à −0,89), CLDN18 baisse à peine (−0,18, dans le bruit du nul)
et MUC16 ne bouge pas (−0,01, contre +0,64 sur l'axe KRAS) ; DPCR1,
quatrième gène de la chaîne, n'a pas de mesure Chronos dans DepMap 24Q4
et n'est pas testable. (c) Aucune autre chaîne n'apparaît : les seuls
mouvements au-dessus du nul sont des hausses (PGC +0,45, CEACAM5 +0,42),
pas un bloc qui chute, et aucun flux n'a de gradient le long de l'axe
(|rho de Spearman| ≤ 0,17, le nul fait mieux avec MUC17 +0,31).**

**Le lot.** Go du parent orchestrator, 19 nov. 2026 (chantier 1). Protocole
gelé `PROTOCOL_mtap_prmt5_flux.md` (écrit avant toute construction et
tout run ; SHA `1e56ed9a…66ae161d`). Pipeline
`universal_v6.2.0_cohen.py`, SHA `f07567c4…ec3abf`, revérifié inchangé
avant et après les runs ; v6.1 `2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`.
Mode fast, 2 runs, exit 0/0, 35 fichiers chacun, journal
`runs_v62_prmt5flux.log` (FIN 2026-11-19T13:39:42Z, terminés=2,
échecs=0), lanceur reprenable `run_v62_lot.sh` (manifeste
`manifest_v62_prmt5flux.txt`), lancé par `systemd-run`
(unité `prmt5flux-v62`, jamais nohup). Aucun incident : aucune
interruption, aucun dossier touché, aucun CSV modifié après construction.
Lecture : `prmt5_flux_reading.py` (SHA `3c05a04f…8b064cf48c`),
données `prmt5_flux_direct_tests.csv` (SHA `6e92c43d…64b671`) et
`prmt5_flux_extract.json` (SHA `b5826990…39121`). Livre blanc non édité
directement (cette section est un fichier séparé) ; PDF non régénéré ;
rien poussé sur GitHub.

**Construction.** Sources DepMap Public 24Q4, SHA revérifiés :
`CRISPRGeneEffect.csv` (428 678 699 octets,
`3d8f3ec6…167e3b`) et `Model.csv` (645 696 octets, `b7a0c138…dcfa`),
script `build_fluxes_depmap_prmt5.py` (SHA `7d68de19…488ff69e3`).
Lignées : 45 adénocarcinomes pancréatiques
(`OncotreePrimaryDisease == 'Pancreatic Adenocarcinoma'`, 64 dans
Model.csv, 45 dans GeneEffect ; les 19 absents sont listés dans la
provenance). Écart nommé : les tests directs §8.28/§8.29/§8.40
portaient sur 47 lignées (45 + 2 adénosquameux KP-3 ACH-000108 et L3.3
ACH-000685, présents dans GeneEffect) — la série de flux utilise les 45
adénocarcinomes seuls, comme toutes les séries DepMap du projet (§8.30).
Ordre : Chronos PRMT5 croissant (plus dépendante d'abord) ; PRMT5 sur
les 45 : min −2,937, médiane −1,089, max −0,647 (toutes les lignées sont
PRMT5-dépendantes à des degrés divers), sans ex æquo. PRMT5 est l'axe,
jamais un flux, absent du CSV. Contrôle = `step`, cible = PGC (repli du
pipeline, même convention que la série DepMap v6.2, contrôle `step`,
n=45).

**Flux : 9 sur 12 — trois exclus pour des raisons mesurées, pas choisies.**
Les 12 gènes v4 devaient être repris en valeurs Chronos ; vérification
des en-têtes (17 916 colonnes de gènes) : **DPCR1 et MUC2 sont absents
de la matrice Chronos 24Q4** (aucune colonne) ; **GSTM1 est présent
mais porte 8 NaN sur 45 lignées** — exclu sans imputation, règle du
projet (exclure les 8 lignées donnerait n=37 < 40, minimum fast : la
série deviendrait impossible). Flux retenus, 0 NaN vérifié :
PGC (5225), REG4 (83998), CLDN18 (51208), MUC17 (140453), CR2 (1380),
KRT20 (54474), CEACAM5 (1048), CLCA1 (1179), MUC16 (94025).
Séries `pdac_depmap_fluxes_prmt5.csv` (SHA `bb575a2c…f63050df`) et nul
`…_prmt5_nul.csv` (SHA `014a084f…52db9e20`, lignes permutées, graine 42,
`step` intact). **Longueur vérifiée : 45 lignes — le minimum fast
v6.2 est 40, ça passe de 5 points.**

**Lecture du pipeline (v6.2 fast, n=45, contrôle `step`).**

| Indicateur | Réel | Nul | Écart (réel − nul) |
|---|---|---|---|
| Cascade T_-2 / T_-1 / T_0 / T_+1 / T_+2 (%) | 0,60 / 3,60 / 6,60 / 35,30 / 35,30 (pas 0/2/3/16/16) | 2,20 / 66,38 / 73,11 / 82,07 / 84,31 (pas 1/29/32/36/37) | T_0 au pas 3 contre 32 |
| MC best_score (seuil) | 0,3390 (60,87 %) | 0,3386 (66,67 %) | **+0,0004** |
| max_separation | 0,1919 | 0,2955 | **−0,1036** |
| stability | 0,9883 | 0,9725 | +0,0158 |
| **S_sep = max_separation × stability** | **0,1897** | **0,2874** | **−0,0977** |
| Delta | 1,761 | 1,912 | **−0,151** |
| L7a | DOWN 0,340 | DOWN 0,179 | même sens, réel plus confiant (−0,161 signé) |
| Falsification delta_vs_null | 0,1536 (ok, seuil 0,5) | indisponible | pas de paire comparable |
| L7b | FRAGILE | FRAGILE | — |
| Régime | criticality | criticality | — |

Critère gelé : séparation réel > nul au-delà de la gigue mesurée 0,00.
**Aucun indicateur ne le passe dans le sens réel > nul.** MC est égal
à 0,0004 près — le seuil MC ne distingue rien ici. S_sep, max_separation
et Delta sont meilleurs au nul, au-delà de 0. L7a donne DOWN des deux
côtés (réel plus confiant, −0,161 signé), mais L7a est un vote interne,
pas une preuve, et il ne renverse pas trois indicateurs contraires.
La falsification du réel (0,1536) est sous son propre seuil 0,5, et
celle du nul est indisponible (« comparaison impossible sans les deux
dimensions ») : il n'y a pas de paire à comparer. Le bruit est
indisponible des deux côtés (« Scores proxy complets indisponibles »).
F1/F2 médians avant/après : réel 0,0022→0,0055 (ratio 2,51) et
0,00013→0,00036 (ratio 2,82) ; nul 0,00077→0,0053 (ratio 6,88) et
0,00013→0,00058 (ratio 4,53) — les ratios du nul sont plus grands ;
14 estimateurs changent de signe F1 dans le réel contre 8 dans le nul,
sans direction distinctive. La cascade réelle place son T_0 au pas 3
(6,6 %) — un seuil de bord, pas une rupture centrale.

**Tests directs top-12 contre reste (d de Cohen ; + = plus haut chez les
12 lignées les plus PRMT5-dépendantes ; mêmes unités que §8.4/§8.34/§8.36).**

| Flux | Réel top-12 d | Nul top-12 d | Réel Spearman vs rang | Nul Spearman vs rang |
|---|---|---|---|---|
| PGC | **+0,454** | +0,234 | +0,056 | +0,119 |
| CEACAM5 | **+0,417** | +0,128 | −0,013 | +0,053 |
| REG4 | +0,127 | −0,207 | +0,055 | −0,153 |
| MUC17 | +0,067 | −0,128 | −0,048 | +0,312 |
| MUC16 | −0,012 | −0,252 | −0,109 | +0,106 |
| CLCA1 | −0,058 | +0,032 | +0,025 | +0,063 |
| CR2 | −0,114 | −0,130 | −0,112 | −0,028 |
| CLDN18 | −0,176 | +0,094 | +0,149 | +0,021 |
| KRT20 | −0,286 | −0,016 | +0,172 | −0,046 |

Référence chaîne KRAS (§8.4) : PGC −0,89, DPCR1 −0,85, CLDN18 −0,46,
MUC16 +0,64. **Aucun des trois gènes testables ne se retrouve :**
PGC monte (+0,45) au lieu de s'effondrer — sens inverse ; CLDN18
baisse faiblement (−0,18, dans le bruit du nul, |d| ≤ 0,25) ; MUC16
ne bouge pas (−0,01). Les 12 plus PRMT5-dépendantes : ACH-000213
(−2,937), ACH-001107 (−2,056), ACH-000243, ACH-000535, ACH-002186,
ACH-000468, ACH-000265, ACH-000114, ACH-000354, ACH-000601,
ACH-001375, ACH-000320 (Chronos PRMT5 −2,937 à −1,370 ; ordre complet
dans `prmt5_flux_order.txt`, SHA `92e0b73c…cc8d30b`). Autour de T_0
(pas 3, ±20) : PGC −1,58 dans le réel contre +1,10 dans le nul — mais
la fenêtre « avant » du réel ne compte que 3 points (pas 0–2), donc
ce −1,58 n'est pas interprétable, et le nul montre un mouvement
opposé d'amplitude comparable à son propre T_0 : pas distinctif.

**Pas d'autre chaîne.** Les deux seuls mouvements réels au-dessus du
maximum du nul (|d| ≤ 0,25) sont des hausses — PGC +0,45 et CEACAM5
+0,42 — pas un bloc qui chute. Le long de l'axe, aucun gradient :
tous les Spearman réels ont |rho| ≤ 0,17 (KRT20 +0,17, CLDN18 +0,15),
et le nul fait mieux (MUC17 +0,31). La dépendance PRMT5 ordonne les
lignées sans ordonner les flux : les flux v4 en Chronos ne portent pas
de structure le long de cet axe.

**Ce que ça change.** La chaîne (bloc estomac/mucus qui chute + MUC16
qui monte) est confirmée comme propre à l'axe KRAS : elle ne réapparaît
ni sous les 48 contrôles du §8.32, ni sous l'ordre prolifération
(§8.34), ni sous l'ordre CN MTAP (§8.36), ni sous l'ordre dépendance
PRMT5 — quatrième axe testé qui ne la porte pas. C'est cohérent avec
l'arbitrage §8.40 : le groupe MTAP-délété existe comme groupe
biologique (dépendance PRMT5 plus forte) mais n'est pas le groupe
KRAS-fort — et ici l'axe qui définit ce groupe ne reconstruit pas la
signature KRAS. Le seul fait descriptif nouveau est le sens inverse
de PGC : il monte chez les plus PRMT5-dépendantes alors qu'il
s'effondre chez les KRAS-forts — une corrélation à noter, pas un
signal de rupture, et pas une piste thérapeutique.

**Ce qui manque, et ce qui reste ouvert.** DPCR1 n'est pas testable en
Chronos (absent de DepMap 24Q4) : la chaîne n'est testée que sur 3 de
ses 4 gènes ; GSTM1 est exclu (8 NaN) ; n=45, marge de 5 points
seulement au-dessus du minimum fast ; les 2 adénosquameux sont hors
série ; la falsification du nul est indisponible et le bruit
indisponible des deux côtés ; le T_0 réel est un seuil de bord (pas 3).
Reste ouvert : la série par stade TCGA (protocole C du brouillon
`PROTOCOL_enrichissements_833_DRAFT.md`, go à demander) ; la
publication finale (PDF + GitHub) après le go de Zackary. La
contradiction S_sep contre MC/Delta du §8.38 n'est pas arbitrée par ce
test — ici les trois indicateurs sont cohérents (MC égal, S_sep et
Delta au nul), ce qui ne renverse rien du §8.36.
