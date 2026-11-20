# §8.71 — Confirmation indépendante pour `maxsep` (C3) : la paire GSE60979 CONFIRME

## Verdict d'abord

**CONFIRME — la onzième paire principale indépendante, GSE60979
(n = 49), donne `d_maxsep = +0,2045` (réel 0,4418 contre nul
0,2373), nettement au-dessus du plancher 0,07 : elle passe.
A2 étendu : 7/11 au-dessus du plancher, 9/11 positifs — la
condition C3 du §8.59.8 est LEVÉE (7 paires passantes au total,
LOO pire cas 6/10). L'adoption pleine de `maxsep`, décidée par
Zackary le 20 nov. 2026 à 13h04, reste sa décision : ce chantier
ne la rouvre pas — il la consolide par une confirmation
indépendante mesurée, comme le protocole le prévoyait. La
confirmation indépendante est désormais close sur ce critère.**

| Porte (PROTOCOL_maxsep_cohort_871.md §7, gelé) | Exigé | Mesuré 20 nov. 2026 | Sort |
|---|---|---|---|
| Paire indépendante : `d_maxsep > 0,07` et positif | > 0,07 | **+0,2045** (réel 0,4418, nul 0,2373) | **CONFIRME** |
| A2 étendu (11 paires) | 7/11 et 9/11 positifs | **7/11, 9/11 positifs** | **C3 LEVÉE** |
| LOO sur 11 paires (descriptif) | Retrait d'une paire passante : 6/10 | **6/10** après retrait de chaque paire passante | **PASSE** |
| Exactitude de l'extraction | 2/2 à 0,0 exact | **2/2, écart max 0,0** | **PASSE** |
| Nuls frais (§7, `d` dans [−0,07 ; +0,14[) | 2 nuls frais si proche du plancher | **Non courus : +0,2045 hors de l'intervalle** | **SANS OBJET** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que la
onzième paire principale, mesurée aujourd'hui sur une cohorte
jamais utilisée dans ce projet (Oslo, 49 PDAC, plateforme
Agilent GPL14550), sépare le réel du nul en `maxsep` dans le
bon sens et au-delà du plancher gelé : +0,2045 contre 0,07
exigé — près de trois fois le plancher, et le plus grand écart
positif des paires GEO du dossier (les deux écarts plus grands,
immunitaire +0,3675 et TCGA v4 +0,2928, sont des paires TCGA,
pas GEO). Il dit aussi que le verdict de suffisance
ne tient plus à une seule paire : retirer n'importe laquelle
des 7 paires passantes laisse 6/10, qui satisfait encore la
barre A2 d'origine (≥ 6/8). Il ne dit pas que `maxsep` est
validé en général : c'est une confirmation sur 11 paires
comptées, dont 4 restent non passantes (GSE71729, GSE62452,
GSE21501, GSE79668), et les scores compagnons ne suivent pas
tous (Delta plat −0,015, MC à peine positif +0,026 — voir
§8.71.5). Il ne dit pas non plus que l'adoption pleine est
« prouvée » par ce chantier seul : elle a été décidée par
Zackary après lecture des §8.56/§8.59/§8.64, et cette section
est la vérification a posteriori que le protocole prévoyait —
elle consolide la décision, elle ne la fonde pas rétroactivement.

**Fragilité, dite en tête.** Le verdict tient à une seule paire
mesurée aujourd'hui — comme tous les verdicts de ce dossier.
Mais ici la fragilité est bornée par le protocole lui-même :
+0,2045 est hors de l'intervalle des nuls frais ([−0,07 ;
+0,14[), donc aucun nul frais n'a été couru et aucun tirage
de nul ne peut renverser le passage par la règle gelée — à la
différence du §8.70, où le verdict tenait au tirage du nul
(étendue 0,0972 entre 3 nuls à n = 51, écart 0,0567). À n = 49,
l'écart mesuré (+0,2045) dépasse de loin l'étendue des nuls
mesurée au §8.70 à n comparable. En revanche, la paire échoue
à la barre descriptive du plancher équivalent-sep (0,1146
contre 0,1249 exigé — voir §8.71.3) : `sep` ne suit pas
`maxsep` jusqu'à sa propre barre, comme aux §8.59/§8.64 où
`sep` seul avait été rejeté. C'est consigné tel quel, sans
sauver ni condamner le verdict, dont le critère gelé est
`maxsep` et lui seul.

Protocole gelé : `PROTOCOL_maxsep_cohort_871.md` (20 nov.
2026, SHA `82a2c93d…96eef` au gel, inchangé). Critère de
passage écrit AVANT tout run (§7 du protocole) ; aucune
repondération, aucun nouveau terme, aucune redéfinition du
plancher après avoir vu les chiffres. Les nombres des §8.56/
§8.59/§8.64/§8.69/§8.70 étaient la motivation, pas le verdict :
le verdict repose sur les 2 runs mesurés ci-dessous.

## 8.71.1 — La paire mesurée : GSE60979, et pourquoi elle est indépendante

**Cohorte : GSE60979, NCBI GEO** — Sandhu et coll., 49 tumeurs
PDAC réséquées (tissus frais congelés), plateforme Agilent
SurePrint G3 Human GE 8x60K GPL14550, article Sandhu et coll.
2015 (*Molecular Oncology*, 9:758–771, PMID 25579086,
doi 10.1016/j.molonc.2014.12.002). Provenance complète :
`PROVENANCE_871.md`.

**Indépendance, en cinq points (protocole §2).**
1. **Jamais utilisée dans ce projet.** Aucun CSV de flux, aucun
   run, aucun JSON, aucune valeur `maxsep` n'existait pour
   GSE60979 avant ce chantier. Vérifié par grep avant le gel :
   la chaîne exacte « GSE60979 » (comme « GSE60980 ») ne
   figurait dans AUCUN fichier du projet.
2. **Nouveaux patients, nouveau centre, nouvelle plateforme.**
   Cohorte monocentrique d'Oslo (Oslo University Hospital,
   Norvège), patients distincts de TCGA, ICGC PACA-AU et des
   cohortes GEO déjà utilisées ; plateforme Agilent GPL14550,
   distincte de toutes les plateformes V1 et des confirmations
   (RNA-seq TCGA, Illumina ICGC, Affymetrix GPL20769/GPL6244/
   GPL13667/GPL15048/GPL570, Agilent GPL4133/GPL7264, Illumina
   HiSeq GPL11154).
3. **Traitée comme indépendante par la littérature.** Sandhu et
   coll. constituent leur propre cohorte périampullaire
   d'Oslo (2014) ; aucune des cohortes du projet n'y figure
   comme sous-ensemble, et la cohorte n'est un re-découpage
   d'aucune série déjà tenue (les 49 PDAC sont identifiés par
   caractéristique ch1, titres `PDAC_1 [mRNA]` …
   `PDAC_49 [mRNA]`, aucun code-barres TCGA).
4. **Même construction que les autres paires principales GEO.**
   Variante (a) : les 12 mêmes gènes que la v4 TCGA (PGC, REG4,
   CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5,
   CLCA1, MUC16), ordre = KRAS croissant, sans correction, cas
   complets, nul = lignes permutées graine 42. La paire est donc
   comparable aux 10 paires comptées par construction.
5. **Pas un re-test déguisé.** Ce n'est ni une relecture d'un JSON
   existant (§8.64.7 : « pas une relecture »), ni une rotation
   déjà comptée, ni un sous-ensemble d'une paire V1, ni un nouvel
   ordre sur des CSV existants (nouveaux CSV, nouveaux runs,
   2 runs v6.2 frais). La sous-série miRNA GSE60978 n'est pas
   utilisée : ce n'est pas de l'expression génique codante.

**Ce que GSE60979 n'est pas.** Ce n'est pas une cohorte choisie
pour ses résultats : aucun `maxsep` GSE60979 n'existait quand
le protocole a été gelé. Ce n'est pas non plus une cohorte
périampullaire prise en bloc : seuls les 49 PDAC servent à la
paire — les 12 normaux adjacents et les 32 autres
adénocarcinomes périampullaires (duodénal 9, cholédoque 8,
ampoule pancréatobiliaire 8, ampoule intestinal 7) sont exclus
et comptés, comme le protocole l'exigeait. C'est la première
paire principale GEO sur plateforme Agilent 8x60K à
intensités log2 normalisées par les déposants (voir §8.71.4).

**Convention d'affichage (§8.64.6, adoption pleine — le verdict
de suffisance ne tient plus à une paire).** La table ci-dessous
affiche `maxsep` comme score principal, l'ancien MC en second,
`sep` en compagnon borné [0, 1], plancher 0,07 en unités |d|.

## 8.71.2 — Le résultat : GSE60979 réel contre nul (v6.2, mode fast, 2 runs, exits 0/0)

| Indicateur | Réel | Nul (graine 42) | Écart (réel − nul) | Lecture |
|---|---|---|---|---|
| **`maxsep` (principal, \|d\|, plancher 0,07)** | **0,4418** | **0,2373** | **+0,2045** | **CONFIRME — passe, ~3× le plancher** |
| `sep` (compagnon borné [0, 1]) | 0,3064 | 0,1918 | +0,1146 | Positif, comme `maxsep` (monotonie) |
| Ancien MC (secondaire) | 0,3606 (seuil 76,19 %) | 0,3346 (seuil 23,81 %) | +0,0260 | Positif, petit |
| S_sep (= maxsep × stability) | 0,4316 | 0,2356 | +0,1959 | Positif, passe aussi le plancher |
| Delta | 1,8707 | 1,8860 | **−0,0153** | Plat des deux côtés — voir §8.71.5 |
| L7a | UP 0,1388 | UP 0,3442 | même sens | Descriptif — voir §8.71.5 |
| L7b | FRAGILE | FRAGILE | — | Non-informatif, comme partout |
| Falsification | indisponible (n = 49 < 75) | indisponible | — | Règle du projet — voir §8.71.5 |
| Cascade (%) | 0,0 / 83,6 / 91,8 / 94,8 / 97,8 (pas 0/40/44/45/47) | 2,0 / 8,1 / 14,1 / 26,3 / 26,3 (pas 1/4/7/13/13) | formes très différentes | Descriptif — voir §8.71.5 |
| Régime | criticality | criticality | — | Descriptif |
| Bruit | Scores proxy complets indisponibles | Scores proxy complets indisponibles | — | Même verdict |
| F1 / F2 « Tous » (après/avant) | ×9,91 / ×19,52 | ×0,041 / ×0,058 | sens opposé, sans direction | Descriptif — voir §8.71.5 |

Valeurs exactes (extraction) : réel `maxsep` 0,4417749548909115,
`stability` 0,9768744847619764, MC 0,36063527837854986 ; nul
`maxsep` 0,23726557228635847, `stability` 0,9930728408602641, MC
0,3345954612679557. Écart exact `d_maxsep` =
+0,20450938260455304. `d_sep` = +0,11464439635911555 ;
`d_MC` = +0,026039817110594166 ; `d_Ssep` =
+0,19593668553105414 ; `d_Delta` = −0,01528. Plancher
équivalent-sep (descriptif, §8.71.3) :
0,07·(1+0,4418)·(1+0,2373) = 0,1249 — la paire échoue à cette
barre descriptive (0,1146 < 0,1249), alors qu'elle passe au
plancher `maxsep`.

**Lecture.** Les deux scores `maxsep` sont positifs, mais
l'écart est net : le réel (0,4418) dépasse le nul (0,2373) de
0,2045 — le plus grand écart positif des paires GEO du dossier,
devant GSE79668 (+0,0567) et GSE71729 (+0,0402), et sans commune
mesure avec les échecs négatifs (GSE62452 −0,0036, GSE21501
−0,0100). Les deux écarts plus grands du dossier (immunitaire
+0,3675, TCGA v4 +0,2928) sont des paires TCGA, pas GEO. L'ancien MC est positif
d'un cheveu (+0,0260) : il ne porte rien ici, mais il ne
contredit pas — à la différence des §8.69/§8.70, où il était
inversé. S_sep est positif de 0,1959, au-dessus du plancher
lui aussi. Les cascades diffèrent fortement en forme (réel
97,8 % à T_+2, pas 47 ; nul 26,3 %, pas 13) — la plus grande
différence de forme de cascade entre réel et nul parmi les
paires GEO à petit n, et elle va dans le même sens que
l'écart de score. La paire passe : c'est un résultat, pas un
bruit de mesure — la vérification indépendante le confirme à
0,0 exact (§8.71.3), et l'écart est hors de portée d'un tirage
de nul (§7 : aucun nul frais couru, +0,2045 hors de
[−0,07 ; +0,14[).

**Lot.** Pipeline `universal_v6.2.0_cohen.py`, SHA
`f07567c4…c3abf`, revérifié inchangé avant ET après le lot ;
mode fast ; 2 runs, exits 0/0, 35 fichiers chacun. Lancement en
`systemd-run` (unité `v62-871`), surveillance `watch_v62_871.sh`
(arrêtée d'elle-même à 2/2, `WATCH 871 TERMINE 2/2`, tour 2,
20h55:47Z) ; journal `runs_v62_871.log` (100 lignes ; lot FIN
20h55:27Z, déjà faits 0, terminés 2, échecs 0). Durée du lot :
20h46:50Z → 20h55:27Z (~9 min). Aucun incident de lancement,
aucun redémarrage de machine pendant le lot. Le livre blanc
n'est PAS édité, le PDF N'EST PAS régénéré, rien n'est poussé
sur GitHub dans ce chantier.

## 8.71.3 — A2 étendu, leave-one-out, exactitude

**A2 étendu (11 paires).** Les 10 paires comptées gardent leurs
valeurs (§8.56.3, §8.69.2, §8.70.2, re-vérifiées à l'identique,
0 écart) ; la onzième, GSE60979, passe :

| Paire | Écart `maxsep` | > 0,07 ? | Positif ? |
|---|---|---|---|
| HP35 | +1,6512 | oui | oui |
| TCGA v4 | +0,2928 | oui | oui |
| GSE71729 | +0,0402 | non | oui |
| GSE62452 | −0,0036 | non | non |
| ICGC | +0,0970 | oui | oui |
| Immunitaire TCGA | +0,3675 | oui | oui |
| PARP TCGA | +0,1688 | oui | oui |
| DepMap | +0,1904 | oui | oui |
| GSE21501 (§8.69) | −0,0100 | non | non |
| GSE79668 (§8.70) | +0,0567 | non | oui |
| **GSE60979 (nouvelle)** | **+0,2045** | **oui** | **oui** |
| **Total** | — | **7/11** | **9/11** |

**Condition C3 du §8.59.8 : LEVÉE.** Sept paires passantes au
total — c'est le nombre exigé par la lecture précise (§8.69 §7,
§8.70 §8.70.8). La confirmation indépendante consolide
l'adoption pleine décidée par Zackary le 20 nov. 13h04.

**Leave-one-out sur les 11 paires (descriptif, même règle que
D3).** Retirer n'importe laquelle des 7 paires passantes donne
6/10 — au-dessus de la barre A2 d'origine en nombre de
passantes (6). Retirer GSE71729, GSE62452, GSE21501 ou GSE79668
(les quatre non passantes) donne 7/10. Le verdict de suffisance
ne tient donc plus à une seule paire — c'est la première fois
depuis le §8.59 que le LOO pire cas satisfait la barre A2
d'origine. L'ajout d'une paire passante consolide le comptage
en nombre (7/11 au lieu de 6/10) et en robustesse (LOO 6/10 au
lieu de 5/9).

**Nuls frais (règle gelée §7 : `d_maxsep` dans [−0,07 ; +0,14[,
donc NON courus).** `d_maxsep` = +0,2045 est hors de
l'intervalle : aucun nul frais n'a été construit ni couru, et
le script `build_nul_871.py` (graines 8711, 8712) n'a pas été
exécuté. Le verdict de la paire graine 42 est donc le verdict,
sans contrôle de robustesse par nuls frais — par règle gelée,
parce que l'écart dépasse le plancher de près de trois fois et
sort de la zone où le tirage du nul pouvait renverser le
passage (c'est exactement le cas que la règle prévoyait : un
écart loin du plancher n'a pas besoin de nuls frais).

**Plancher équivalent-sep (descriptif).** La paire échoue à la
barre `0,07·(1+m_R)(1+m_N)` = 0,1249 (d_sep 0,1146 < 0,1249),
de 0,0103 — comme elle passe au plancher `maxsep` de 0,1345
de marge. `sep` ne suit pas `maxsep` jusqu'à sa propre barre :
c'est le même fait structurel qu'aux §8.59/§8.64 (`sep` seul
rejeté, A2 5/8), consigné tel quel. Le critère gelé est
`maxsep`, et lui seul ; la barre équivalent-sep ne décide
rien ici (D4 n'est pas rejoué : il porte sur les paires V1,
déjà tranché).

**Exactitude.** Extracteur `extract_871.py` (2/2 runs, 0
manquant, versions `v6.2.0-L7aL7b-CohenD-short` partout) ;
second calcul indépendant `verify_871.py` (chemin de code
distinct, relecture directe des 2 JSON) : **2/2 comparaisons,
écart max 0,0 exact** sur `maxsep`, ancien MC et `stability`,
verdict OK. SHA du pipeline revérifié après travaux, inchangé.
Les 10 valeurs comptées sont reprises telles quelles de
`sep_maxsep_856_table.json` (SHA
`ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`),
de `extract_869.json` (SHA
`644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b`)
et de `extract_870.json` (SHA
`4ffa851a83668b2369097703862e0413ff9af54af3a66ef70aea9333b40c444f`),
jamais recalculées ici — les §8.56/§8.59/§8.64/§8.69/§8.70 sont
clos.

## 8.71.4 — La construction : portes §5, intensités log2 normalisées

La paire GSE60979 passe les 7 portes §5 sur le fichier officiel
(aucun run lancé avant leur vérification).

| Porte §5 | Exigé | Mesuré 20 nov. 2026 | Sort |
|---|---|---|---|
| Matrice HTTP 200, lecture complète | 200, SHA consigné | **200, 20 547 348 o, SHA `819408bf…c4eb`, 42 545 sondes x 93 échantillons, 0 NaN** | **OK** |
| Plateforme lue dans l'en-tête | GPL14550 | **GPL14550** (`!Series_platform_id`) | **OK** |
| n ≥ 40 tumeurs PDAC | ≥ 40 | **49/49 tumeurs** (caractéristique ch1) ; 44 exclus comptés (12 normaux + 32 autres périampullaires) | **OK** |
| Aucun code-barres TCGA | 0 | **0** (titres et GSM inspectés) | **OK** |
| KRAS présent | oui | **oui, 2 sondes** (médiane) | **OK** |
| 12 gènes v4 présents | 12/12 | **12/12** (sondes : PGC 2, REG4 2, CLDN18 1, MUC17 2, DPCR1 1, CR2 2, KRT20 1, MUC2 4, GSTM1 1, CEACAM5 1, CLCA1 1, MUC16 2) | **OK** |
| Cas complets ≥ 40 | ≥ 40 | **49/49** (0 NaN) | **OK** |

**Mapping.** `data/GPL14550_probe2symbol.tsv` (SHA
`cc034a76…c3909`), construit à neuf dans l'enquête et repris
tel quel : 42 545 lignes de table, 30 436 sondes avec symbole,
22 070 symboles uniques, colonne `GENE_SYMBOL`, marqueur
`!platform_table_end` vu. Symboles dupliqués : 14 723 lignes —
agrégation par médiane (règle du projet) ; les 13 gènes utiles
(12 v4 + KRAS) ont chacun 1 à 4 sondes, agrégées par médiane.
**Nature des valeurs : intensités log2 normalisées Agilent**,
d'après `!Sample_data_processing` : « The scanned images were
analyzed using Feature Extraction Software 10.7.3.1 (Agilent
Technologies) using default parameters. The expression profiles
were backgroundcorrected and quantile normalized for mRNA. »
Plage sur la matrice complète : min 4,02 / médiane 6,72 /
max 18,81, 0 NaN. Ce sont des log-intensités comme les autres
paires GEO V1 (GSE71729, GSE62452) — pas des log-ratios comme
GSE21501, pas des comptages bruts comme GSE79668. Aucune
renormalisation, aucune transformation log ajoutée (protocole
§4.2). KRAS (valeurs puce) : min 7,90 / médiane 8,75 /
max 10,03. CSV de flux : `pdac_871_geo60979_fluxes.csv`
(49 lignes, SHA `51a7fa56…0554e`), nul SHA `d427359a…34740`.

**Enquête préalable, dite plainement.** Le choix de GSE60979
repose sur une enquête GEO menée avant le gel du protocole
(20 nov. 2026) : recherche E-utilities `pancreatic AND
Series[ET]` (789 séries), résumés récupérés, filtre humain +
n ≥ 40, examen des sous-séries et des matrices des candidats
en copies temporaires `/tmp` (vérifications de portes
uniquement, supprimées, jamais utilisées pour construire un
flux ni lancer un run). Le téléchargement officiel (dans
`data/`, SHA consigné) n'a eu lieu qu'après le gel — et son
SHA est identique bit à bit à la copie d'enquête. Les
candidats écartés dans cette enquête sont documentés au
protocole §2.3, avec la raison pour chacun — dont GSE77858
(46 PDAC, UCLA, GPL7264 : **MUC17 absent, 12/13** — même
porte échouée que GSE57495 et GSE62165) et GSE43797 (7 PCA
seulement). Piste restante nommée, non vérifiée : GSE131050
(PurIST, 191 échantillons, deux lots Linehan/Yeh, deux
plateformes) — elle reste ouverte comme cohorte future, mais
la confirmation C3 n'en a plus besoin.

## 8.71.5 — Contrôles descriptifs (à publier, ne décident pas)

**Delta ne diverge PAS sur cette paire — il est plat des deux
côtés.** Delta réel 1,8707 contre nul 1,8860 (−0,0153 en
faveur du nul, d'un cheveu) — à la différence du §8.69, où
Delta favorisait fortement le réel (+2,01) pendant que
`maxsep` était négatif (−0,01). Ici, Delta ne dit rien pendant
que `maxsep` passe de 0,2045 : les deux scores ne divergent
pas, ils se taisent sur des registres différents. C'est
consigné tel quel, sans élucider sans preuve. La divergence
Delta/`maxsep` du §8.69 ne se reproduit pas — deuxième paire
de suite où elle ne se reproduit pas dans le même sens
(§8.70 : Delta plat +0,05 contre `maxsep` +0,06).

**L7a ne change pas de sens.** Réel UP 0,1388, nul UP 0,3442 —
même direction, confiance plus faible côté réel. Descriptif :
L7a n'est pas le critère gelé, et il ne distingue pas les deux
séries ici (le nul est même plus « confiant »). Comme au
§8.70, UP des deux côtés.

**Falsification : indisponible (n = 49 < 75, règle du projet).**
Notée « indisponible », non imputée (protocole §7). Les
valeurs brutes du JSON sont rapportées ici à titre descriptif
seulement, sans statut de test : réel 0,174647, nul 0,30342
(écart −0,1288, statut « ok » dans le JSON des deux côtés,
seuil 0,5, les deux en dessous). Elles ne comptent pas comme
un test de falsification.

**Cascades : formes très différentes, dans le sens de l'écart.**
Cascade réelle [0,0 / 83,6 / 91,8 / 94,8 / 97,8] (pas
0/40/44/45/47) contre nul [2,0 / 8,1 / 14,1 / 26,3 / 26,3]
(pas 1/4/7/13/13) : le réel atteint 97,8 % à T_+2, le nul
s'arrête à 26,3 %. C'est la plus grande différence de forme
de cascade réel−nul parmi les paires GEO à petit n du dossier
— et elle accompagne l'écart de score, au lieu de le
contredire comme au §8.70 (où les cascades des nuls frais
allaient de 21,3 % à 98,1 % à T_+2). Aucune rupture visible
qui distinguerait le réel du nul au-delà de ce que le score
dit déjà.

**F1/F2 sans direction.** Réel ×9,91 / ×19,52, nul ×0,041 /
×0,058 — les rapports après/avant varient sans direction
cohérente (même figure qu'aux §8.58/§8.66/§8.69/§8.70 : des
rapports sans direction ne font pas un signal). L7b est
FRAGILE sur les 2 runs — même non-informativité que partout.
Bruit : « Scores proxy complets indisponibles » sur les
2 runs — aucun score de bruit mesuré, consigné tel quel.

**Tests directs (§9) : l'ordre est là, et `maxsep` le passe
cette fois.** (1) d de Cohen marginal des 12 flux, réel vs
nul graine 42 : **+0,0000 pour les 12 gènes** (valeurs exactes :
|d| moyen 6,0×10⁻¹⁶, max 3,2×10⁻¹⁵ — zéro à la précision
machine) — par construction, pas par hasard : le nul est une
permutation des lignes, donc chaque flux garde exactement ses
49 valeurs (moyennes et écarts-types identiques). Le test ne
mesure pas la séparation : il valide la construction du nul
(marginales préservées exactement). C'est la correction de
méthode du §8.70, appliquée ici comme prévu au protocole §9 :
le Cohen marginal est rapporté, il ne décide rien, et le test
informatif est le suivant. (2) Test de Spearman contre le
pas (ordre KRAS) : |ρ| moyen réel 0,228 contre nul 0,097 ;
**Δρ médian +0,180 ; Δρ positifs 8/12**. Les plus forts :
CEACAM5 Δρ +0,713 (ρ réel +0,547), MUC17 +0,362 (ρ +0,293),
PGC +0,360 (ρ +0,143), KRT20 +0,320 (ρ +0,295), DPCR1 +0,310
(ρ +0,190) ; les négatifs : GSTM1 −0,388, CLCA1 −0,288,
MUC2 −0,188, CR2 −0,003. La série réelle porte donc des
tendances ordonnées par KRAS (8 flux sur 12 montent ou
descendent avec KRAS plus que leur nul) — et cette fois le
pipeline convertit ces tendances en +0,2045 de `maxsep`,
au-dessus du plancher. L'ordre est mesurable directement, et
le score gelé le passe : les deux lectures concordent, pour
la première fois sur une paire de confirmation indépendante.

**Nature des valeurs.** Les flux sont des intensités log2
normalisées Agilent, comme les paires V1 GSE71729 et GSE62452 :
la comparaison est faite à construction égale (variante (a),
12 gènes, ordre KRAS) et à nature de mesure égale aux paires
V1 — c'est nommé, pas corrigé après coup. Rien ne permet de
dire que la nature des valeurs, plutôt que la cohorte,
explique le passage : GSE71729 et GSE62452, de même nature,
ne passent pas.

## 8.71.6 — Ce que ça change, et ce que ça ne change pas

| Poste | Change ? | Détail |
|---|---|---|
| Condition C3 (§8.59.8) | **LEVÉE** | Une paire indépendante mesurée, elle CONFIRME : A2 étendu 7/11 (9/11 positifs), LOO pire cas 6/10. La confirmation indépendante est close sur ce critère. |
| Adoption pleine de `maxsep` | **Non — décidée par Zackary le 20 nov. 13h04** | Ce chantier est une vérification a posteriori, pas une condition. L'adoption pleine reste sa décision ; la présente section la consolide par une confirmation mesurée, elle ne la fonde pas rétroactivement. |
| Score MC affiché (convention §8.64.6) | Non | `maxsep` principal, ancien MC secondaire, `sep` compagnon, mention de fragilité — inchangée. |
| Sélection du best_config, seuil MC, cascade, S_sep, Delta, L7a | Non | Inchangés par construction. |
| Code v6.2 / v6.1 / v6 | Non | Aucune modification, aucune v6.5. |
| Verdicts des §8.56, §8.59, §8.64, §8.69, §8.70 | Non | Confirmés, pas rouverts ; les 10 paires comptées gardent leurs valeurs. |
| Pistes ouvertes | Oui, une de moins | (a) La confirmation indépendante C3 est close — aucune autre paire indépendante n'est requise par ce critère ; la piste GSE131050 reste nommée comme cohorte future possible, pas comme condition ; (b) la fragilité du nul à petit n (§8.70 : étendue 0,0972 entre 3 nuls à n = 51) reste un chantier propre ouvert — à rapprocher du §8.53 (∼200 nuls pour un plancher stable à petit n) ; (c) la divergence Delta/`maxsep` du §8.69 ne se reproduit pas
sur deux paires de suite — elle reste une piste ouverte, pas
une loi ; (d) la barre descriptive du plancher équivalent-sep (échouée ici de 0,0103, comme aux §8.59/§8.64 pour `sep` seul) reste une limite affichée de `sep`, pas du critère gelé. |

**Suite du dossier.** Si Zackary veut une nouvelle confirmation
sur une autre cohorte (GSE131050, piste nommée) : un chantier
ultérieur, avec son propre protocole gelé — pas une relecture,
pas un re-test déguisé, et pas GSE60979 (mesurée, CONFIRME).
Si Zackary ne veut pas de nouvelle tentative : C3 est levée,
l'adoption pleine tient par sa décision du 20 nov. 13h04
consolidée par la présente confirmation, et la présente
section consigne le passage mesuré avec ses chiffres. Dans
les deux cas, le PDF et GitHub sont régénérés et poussés par
le coordinateur (règle permanente « Toujours github et
pdf !!! »), avec la présente section fusionnée.

## 8.71.7 — Limites et ce qui reste

- Une seule paire nouvelle a été mesurée : le verdict porte sur
  elle, pas sur « `maxsep` en général ». 7/11 et 9/11 sont des
  comptages sur 11 paires, pas des estimations de population.
  Quatre paires restent non passantes (GSE71729, GSE62452,
  GSE21501, GSE79668) : la confirmation n'efface pas les
  échecs, elle les dépasse en nombre.
- À n = 49, aucun nul frais n'a été couru (règle gelée §7 :
  +0,2045 hors de [−0,07 ; +0,14[) — la distribution des nuls
  à n ≈ 50 n'a pas été mesurée ici, et le verdict repose sur
  la paire graine 42, par règle gelée. Un chantier futur qui
  voudrait mesurer cette distribution devrait courir 10 nuls
  frais — mais le verdict de la paire graine 42 resterait
  CONFIRME, par construction.
- Le d de Cohen marginal du §9 est vacueux par construction
  (0,0000 pour les 12 gènes, à la précision machine) : le
  protocole gelait ce test en sachant qu'il l'était, et la
  section applique la correction du §8.70 — le test de
  Spearman contre le pas porte l'information d'ordre.
- La paire échoue à la barre descriptive du plancher
  équivalent-sep (0,1146 contre 0,1249) : `sep` ne suit pas
  `maxsep` jusqu'à sa propre barre. Le critère gelé est
  `maxsep`, et lui seul — c'est nommé, pas corrigé après coup.
- Delta est plat (−0,0153) et MC à peine positif (+0,0260) :
  les scores compagnons ne portent pas le passage — seul
  `maxsep` (et S_sep, +0,1959) le portent. L7b est FRAGILE
  sur les 2 runs — non-informatif, comme partout.
- Rien de clinique : l'étude porte sur l'instrument.

## 8.71.8 — Provenance

- Protocole gelé : `PROTOCOL_maxsep_cohort_871.md`, SHA-256
  `82a2c93d2975274e9a900343ef626b8d37b5634bb008d107e8bff9b106496eef`
  (au gel, avant téléchargement officiel ; fichier inchangé
  depuis).
- Provenance complète : `PROVENANCE_871.md`, SHA-256
  `74e603ab392b890f4935022fb0491c4d9c1931449f10ead240ad683b334bf430`
  (sections 3 et 5 complétées après construction et runs ;
  fichier inchangé depuis).
- Construction : `build_fluxes_871.py`, SHA-256
  `1134c574d6727b6d4fa2e13cfe4a69efca01143602b9ca4e47791b57fa268ed9`
  (variante (a) seulement ; règle tumeur = caractéristique ch1
  « tissue: pancreatic ductal adenocarcinoma »).
- Données : `data/GSE60979_series_matrix.txt.gz`, 20 547 348 o,
  SHA-256
  `819408bf8dacb01c38eede69287d255eea76f74e2b1b18ec8863933f4700c4eb`
  (HTTP 200, 20 nov. 2026) ; `data/GPL14550_probe2symbol.tsv`,
  SHA-256
  `cc034a76285b0785bff4dd5249d68becb58acacedb157a8032d0c9309dac3909`
  (42 545 lignes, 30 436 sondes avec symbole, 22 070 symboles
  uniques, colonne `GENE_SYMBOL`) ; `data/GPL7264_probe2symbol.tsv`,
  SHA-256
  `41a4716063d9cb37518670dd0ab54b26064e52e34f8cb156614dc73e3aa6c27e`
  (mapping de la cohorte écartée GSE77858, MUC17 absent).
- Flux : `pdac_871_geo60979_fluxes.csv` (49 lignes), SHA-256
  `51a7fa56869a2d8db788bc02f78f24d435a98cb3cefa50bbcb2b51bbb190554e` ;
  `pdac_871_geo60979_fluxes_nul.csv`, SHA-256
  `d427359aa9e244608150a707f54caa831ffd45938cd78eeeaf0dced2bca34740`.
  Aucun nul frais (règle gelée §7).
- Runs : manifeste `manifest_v62_871.txt`, SHA-256
  `a1dbe6dd2dd105a233bf77d8548e6c5d916020bb304ee55ef7e301a2ec5afd2e` ;
  journal `runs_v62_871.log` (100 lignes), SHA-256
  `b0620b8b91bd130b8eba6a855c29fb91c7dd563d8dbec111be885cd5eb6aae55` ;
  surveillance `watch_v62_871.sh`, SHA-256
  `34ccad3fc8f004d89ca1c6acebf9bc586cf0891f3af472f530e848eec86b5717` ;
  dossiers `results_fast_v62_871_geo60979[_nul]`
  (2 runs, exits 0/0, 35 fichiers chacun).
- Extraction : `extract_871.py`, SHA-256
  `687bf9fe383633aa2bc5faa579e0bfa99f8cd08bd619ef3275a4e737ad1359e8`
  → `extract_871.json`, SHA-256
  `85e9089a9f4c5ee0d7984bfd44ed2646dc0842174401395642cb479cd1f55e3b` /
  `extract_871.csv`, SHA-256
  `6e474668eb24bbccb2d889d4ac38a80c528f1276b21d094ca0ac88c362166e25`.
- Vérification indépendante : `verify_871.py`, SHA-256
  `5cc8cc1d180f5b8571e21563c1cd9237cbd2ebb29774029e2a0e6ae0d408638d`
  → `maxsep_871_verify.json`, SHA-256
  `ca8795b39e39e34a0155a5725834e809ea3bfa21819a1d1a66b117696117b063`
  (2/2 comparaisons, écart max 0,0 exact, verdict OK).
- Tests directs : `direct_tests_871.py`, SHA-256
  `c543044a82b74d9e4b79b978f5971889a82aa0b664de2c6a8700dc2525295cbc`
  → `direct_tests_871.json`, SHA-256
  `2c94e28a8bfb3aaeca83a4f4076a27d9436c2f7225572531a2a47b35d5811f94`.
- Références re-vérifiées : `sep_maxsep_856_table.json`, SHA-256
  `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`
  (8 paires V1 reprises telles quelles, jamais recalculées ici) ;
  `extract_869.json`, SHA-256
  `644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b`
  (GSE21501 reprise telle quelle) ; `extract_870.json`, SHA-256
  `4ffa851a83668b2369097703862e0413ff9af54af3a66ef70aea9333b40c444f`
  (GSE79668 reprise telle quelle) ; protocole §8.70
  `PROTOCOL_maxsep_gse79668_870.md` (SHA-256
  `fd479d50414a18c2daa2b7cb9aeab55dcc24a49ae30ed6ceee363b4d47c96980`) ;
  section §8.70 `section_8.70_gse79668.md`.
- Livre blanc de référence consulté :
  `livre-blanc-pdac-v6.md`, 14 483 lignes, SHA-256
  `072c0f51…` (§8.1–§8.70, état au 20 nov. 2026) — le livre blanc
  n'a PAS été modifié par ce chantier. Fusion de la présente
  section par le coordinateur.
- Données : séries réelles = intensités log2 normalisées Agilent
  (mesures instrumentales transformées : correction de fond +
  normalisation quantile par les déposants, sondes agrégées par
  médiane, ordre par KRAS). Nul = lignes permutées, graine 42 —
  échantillon hypothétique, pas une mesure. Aucune valeur
  inventée ; aucune valeur recopiée à la main (tables générées
  depuis `extract_871.json`, vérifiées paire par paire à 0,0
  exact par `verify_871.py` ; les valeurs des §8.71.2–§8.71.3
  sont lues dans cette sortie, pas recopiées des
  §8.56/§8.59/§8.64/§8.69/§8.70).
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`, revérifié avant
  ET après le lot), v6.1 (`2af5e5ce…c1c9`), v6
  (`bb8bbdba…c0773`). Aucune nouvelle version construite dans ce
  chantier — pas de v6.5. Deux runs du pipeline lancés dans ce
  chantier (GSE60979 réel + nul, exits 0/0) ; aucun push GitHub,
  aucune Release dans ce chantier.
- Section : `section_8.71_gse60979.md` (ce fichier ;
  SHA noté au rapport).
