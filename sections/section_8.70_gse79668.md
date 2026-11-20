# §8.70 — Confirmation indépendante pour `maxsep` (C3) : la paire GSE79668 est PARTIELLE

## Verdict d'abord

**PARTIEL — la dixième paire principale indépendante, GSE79668
(n = 51), donne `d_maxsep = +0,0567` (positif, sous le plancher
0,07) : elle ne passe pas, mais elle n'échoue pas comme GSE62452
(−0,0036) ou GSE21501 (−0,0100) — elle est positive et proche du
plancher, à 0,0133 de celui-ci. A2 étendu : 6/10 au-dessus du
plancher, 8/10 positifs — la condition C3 du §8.59.8 n'est PAS
levée. L'adoption pleine de `maxsep`, décidée par Zackary le
20 nov. 2026 à 13h04, reste sa décision : ce chantier ne la
rouvre pas et ne la conditionne pas. La confirmation
indépendante reste ouverte.**

| Porte (PROTOCOL_maxsep_gse79668_870.md §7, gelé) | Exigé | Mesuré 20 nov. 2026 | Sort |
|---|---|---|---|
| Paire indépendante : `d_maxsep > 0,07` et positif | > 0,07 | **+0,0567** (réel 0,4104, nul 0,3538) | **PARTIEL** |
| A2 étendu (10 paires) | 7/10 et 8/10 positifs | **6/10, 8/10 positifs** | **ÉCHOUE** |
| LOO sur 10 paires (descriptif) | Retrait d'une paire passante : 6/9 | **5/9** après retrait de chaque paire passante | **ÉCHOUE** |
| Exactitude de l'extraction | 4/4 à 0,0 exact | **4/4, écart max 0,0** | **PASSE** |
| Nuls frais (§7, `d` dans [−0,07 ; +0,14[) | 2 nuls frais si proche du plancher | **+0,0890 et +0,1538** (les deux passent) | **FRAGILE, NON CONSOLIDÉ** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que la
dixième paire principale, mesurée aujourd'hui sur une cohorte
jamais utilisée dans ce projet, sépare le réel du nul en
`maxsep` dans le bon sens, mais pas assez pour le plancher
gelé : +0,0567 contre 0,07 exigé. Il dit aussi — et c'est le
fait nouveau de ce chantier — que cet échec tient au tirage du
nul : les deux nuls frais (graines 8701, 8702) donnent des
écarts qui PASSENT le plancher (+0,0890 et +0,1538). Le nul
graine 42, celui qui fait le verdict par règle gelée, est le
plus haut des trois nuls mesurés (0,3538 contre 0,3215 et
0,2566). Le verdict reste donc PARTIEL sur la paire gelée, et
la robustesse est dite « fragile, non consolidée » par la règle
gelée elle-même (§7) : un autre tirage de nul aurait passé. Il
ne dit pas que `maxsep` est validé : la règle gelée interdit de
changer le verdict avec les nuls frais, et C3 exige 7 paires
passantes — il n'y en a que 6. Il ne dit pas non plus que
l'adoption pleine est annulée : elle a été décidée par Zackary
après lecture des §8.56/§8.59/§8.64, et cette section est une
vérification a posteriori, pas une condition — comme le
protocole le dit depuis son §0. Les deux faits coexistent :
adoption pleine décidée, confirmation ouverte, et désormais une
paire positive proche du plancher au lieu d'une paire négative.

**Fragilité, dite en tête.** Le verdict tient à une seule paire
mesurée aujourd'hui — comme tous les verdicts de ce dossier
tiennent à une paire près. Mais ici la fragilité est mesurée,
pas seulement affirmée : l'écart entre les trois nuls
(0,3538 / 0,3215 / 0,2566, étendue 0,0972) est plus grand que
l'écart réel−nul de la paire gelée (0,0567). Autrement dit, le
bruit d'échantillonnage du nul à n = 51 dépasse le signal
mesuré. À n = 51, un seul nul ne suffit pas à trancher — c'est
exactement ce que les nuls frais montrent, et c'est pourquoi le
protocole les avait gelés. La paire n'est pas « presque
passante » par hasard de formulation : +0,0567 est à 0,0133 du
plancher, dans le bon sens, et 2 nuls frais sur 2 passent.
En revanche, Delta ne diverge pas ici (+0,05, plat des deux
côtés) et MC est inversé (−0,0053) : les scores compagnons ne
sauvent rien et ne condamnent rien — le critère gelé est
`maxsep`, et lui seul.

Protocole gelé : `PROTOCOL_maxsep_gse79668_870.md` (20 nov.
2026, SHA `fd479d50…c96980` au gel, inchangé). Critère de
passage écrit AVANT tout run (§7 du protocole) ; aucune
repondération, aucun nouveau terme, aucune redéfinition du
plancher après avoir vu les chiffres. Les nombres des §8.56/
§8.59/§8.64/§8.69 étaient la motivation, pas le verdict : le
verdict repose sur les 4 runs mesurés ci-dessous (2 principaux
+ 2 nuls frais, règle §7).

## 8.70.1 — La paire mesurée : GSE79668, et pourquoi elle est indépendante

**Cohorte : GSE79668, NCBI GEO** — Kirby et coll., 51 tissus
tumoraux PDAC réséqués, plateforme Illumina HiSeq 2000
GPL11154, article Kirby et coll. 2016 (*Molecular Oncology*,
10(8):1169–1182, PMID 27282075). Provenance complète :
`PROVENANCE_870.md`.

**Indépendance, en cinq points (protocole §2).**
1. **Jamais utilisée dans ce projet.** Aucun CSV de flux, aucun
   run, aucun JSON, aucune valeur `maxsep` n'existait pour
   GSE79668 avant ce chantier. Vérifié par grep avant le gel :
   la chaîne exacte « GSE79668 » ne figurait que dans les trois
   fichiers du chantier §8.69 (protocole, provenance, section),
   au sens « piste restante non vérifiée », plus le livre blanc
   au même sens. Les 2 257 fichiers JSON contenant la
   sous-chaîne nue « 79668 » sont des coïncidences numériques
   (ex. 65,79668663986135 dans
   `results_fast_tcga_v1/master_results.json`) — vérifié par
   lecture du contexte, pas des occurrences de GSE79668.
2. **Nouveaux patients, nouveau centre, nouvelle plateforme.**
   Cohorte monocentrique UAB (Birmingham, AL, USA), patients
   distincts de TCGA, ICGC PACA-AU et des cohortes GEO déjà
   utilisées ; plateforme RNA-seq Illumina HiSeq 2000
   (GPL11154), distincte de toutes les plateformes V1 (RNA-seq
   TCGA, Illumina ICGC, Affymetrix GPL20769/GPL6244/GPL13667/
   GPL15048, Agilent GPL4133).
3. **Traitée comme indépendante par la littérature.** Liu et
   coll., *Oncol Rep* 2019, 41:1521–1530, utilisent GSE79668
   (n = 51) comme jeu de validation indépendant face à
   l'entraînement TCGA (n = 178), aux côtés de GSE62452
   (n = 69) — les trois jeux sont disjoints dans leur analyse.
4. **Même construction que les autres paires principales GEO.**
   Variante (a) : les 12 mêmes gènes que la v4 TCGA (PGC, REG4,
   CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5,
   CLCA1, MUC16), ordre = KRAS croissant, sans correction, cas
   complets, nul = lignes permutées graine 42. La paire est donc
   comparable aux 9 paires comptées par construction.
5. **Pas un re-test déguisé.** Ce n'est ni une relecture d'un JSON
   existant (§8.64.7 : « pas une relecture »), ni une rotation
   déjà comptée, ni un sous-ensemble d'une paire V1, ni un nouvel
   ordre sur des CSV existants (nouveaux CSV, nouveaux runs,
   4 runs v6.2 frais). L'article Kirby et coll. a lui-même
   utilisé TCGA comme cohorte de validation de sa signature —
   les 51 échantillons restent des patients UAB, pas des
   échantillons TCGA : aucun code-barres TCGA dans les titres
   ni les GSM (vérifié), aucun recouvrement d'échantillons.

**Ce que GSE79668 n'est pas.** Ce n'est pas une cohorte choisie
pour ses résultats : aucun `maxsep` GSE79668 n'existait quand
le protocole a été gelé. Ce n'est pas non plus une paire à
12 gènes sur puce : c'est la première paire principale GEO en
RNA-seq à comptages bruts (voir §8.70.4) — la nature des
valeurs diffère des autres paires V1, et c'est nommé comme
limite, pas corrigé après coup.

**Convention d'affichage (§8.64.6, adoption pleine — le verdict
de suffisance tient à une paire aux principales et à l'échelle
du plancher).** La table ci-dessous affiche `maxsep` comme
score principal, l'ancien MC en second, `sep` en compagnon
borné [0, 1], plancher 0,07 en unités |d|.

## 8.70.2 — Le résultat : GSE79668 réel contre nul (v6.2, mode fast, 4 runs, exits 0/0/0/0)

| Indicateur | Réel | Nul (graine 42) | Écart (réel − nul) | Lecture |
|---|---|---|---|---|
| **`maxsep` (principal, \|d\|, plancher 0,07)** | **0,4104** | **0,3538** | **+0,0567** | **PARTIEL — positif, sous le plancher** |
| `sep` (compagnon borné [0, 1]) | 0,2910 | 0,2613 | +0,0297 | Positif, comme `maxsep` (monotonie) |
| Ancien MC (secondaire) | 0,3566 (seuil 76,19 %) | 0,3619 (seuil 75,00 %) | −0,0053 | Inversé, quasi nul |
| S_sep (= maxsep × stability) | 0,4022 | 0,3347 | +0,0675 | Positif, juste sous le plancher |
| Delta | 0,6353 | 0,5886 | **+0,0467** | Plat des deux côtés — voir §8.70.5 |
| L7a | UP 0,3459 | UP 0,3553 | même sens | Descriptif — voir §8.70.5 |
| L7b | FRAGILE | FRAGILE | — | Non-informatif, comme partout |
| Falsification | indisponible (n = 51 < 75) | indisponible | — | Règle du projet — voir §8.70.5 |
| Cascade (%) | 3,9 / 72,4 / 76,3 / 82,2 / 100,0 (pas 2/36/38/41/50) | 0,0 / 23,3 / 27,1 / 33,1 / 52,1 (pas 0/12/14/17/26) | formes différentes | Descriptif — voir §8.70.5 |
| Régime | saturation | saturation | — | Descriptif |
| Bruit | Scores proxy complets indisponibles | Scores proxy complets indisponibles | — | Même verdict |
| F1 / F2 « Tous » (après/avant) | ×9,72 / ×22,58 | ×24,06 / ×15,01 | sans direction | Descriptif — voir §8.70.5 |

Valeurs exactes (extraction) : réel `maxsep` 0,41044843843771645,
`stability` 0,9799354113237144, MC 0,35660142554790764 ; nul
`maxsep` 0,3537953187066359, `stability` 0,9460389511592959, MC
0,36194077374803485. Écart exact `d_maxsep` =
+0,05665311973108055. `d_sep` = +0,029669730937762706 ;
`d_MC` = −0,005339348200127214 ; `d_Ssep` =
+0,06750880711334534 ; `d_Delta` = +0,046684. Plancher
équivalent-sep (descriptif, §8.70.3) :
0,07·(1+0,4104)·(1+0,3538) = 0,1337 — la paire échoue aussi à
cette barre (0,0297 < 0,1337), comme elle échoue au plancher
`maxsep`.

**Lecture.** Les deux scores `maxsep` sont positifs et élevés
des deux côtés (0,4104 contre 0,3538) : le pipeline voit une
séparation forte dans la série réelle ET dans son nul permuté.
L'écart est positif de 0,0567 — du même ordre que l'écart
GSE71729 (+0,0402), l'autre paire positive sous le plancher, et
sans commune mesure avec les écarts passants (HP35 +1,6512,
immunitaire +0,3675, TCGA v4 +0,2928) comme avec les écarts
négatifs (GSE62452 −0,0036, GSE21501 −0,0100). L'ancien MC est
inversé d'un cheveu (−0,0053) : rien, dans cette paire, ne
sépare le réel du nul sur le MC. S_sep est positif de 0,0675,
à 0,0025 du plancher — la même histoire que `maxsep`, à la
marge près. Les cascades diffèrent en forme (réel 100,0 % à
T_+2, pas 50 ; nul 52,1 %, pas 26) sans que l'écart de score
suive. La paire est un quasi-passage : c'est un résultat, pas
un bruit de mesure — la vérification indépendante le confirme
à 0,0 exact (§8.70.3), et les nuls frais montrent que le
verdict tient au tirage du nul (§8.70.3).

**Lot.** Pipeline `universal_v6.2.0_cohen.py`, SHA
`f07567c4…c3abf`, revérifié inchangé avant ET après chaque lot ;
mode fast ; 4 runs, exits 0/0/0/0, 35 fichiers chacun (sans
`csd_consensus.png`, présent dans les dossiers §8.69 —
différence constatée, non expliquée). Lancement en
`systemd-run` (unité `v62-870`, deux invocations), surveillance
`watch_v62_870.sh` (arrêtée d'elle-même à 2/2 puis à 4/4,
`WATCH 870 TERMINE 4/4`, tour 2, 19h48:06Z) ; journal
`runs_v62_870.log` (202 lignes ; lot principal FIN 19h42:42Z,
déjà faits 0, terminés 2, échecs 0 ; lot nuls frais FIN
19h47:46Z, déjà faits 2, terminés 2, échecs 0). Durée du lot
principal : 19h39:03Z → 19h42:42Z (~4 min) ; lot nuls frais :
19h44:14Z → 19h47:46Z (~4 min). Un incident de lancement, réparé
ouvertement : la première invocation `systemd-run` a échoué en
~5 s (`Permission denied`, exit 126) parce que
`watch_v62_870.sh` n'était pas exécutable — `chmod +x`,
relance, unité active, aucune donnée perdue (aucun run n'avait
démarré). Aucun redémarrage de machine pendant les lots. Le
livre blanc n'est PAS édité, le PDF N'EST PAS régénéré, rien
n'est poussé sur GitHub dans ce chantier.

## 8.70.3 — A2 étendu, leave-one-out, nuls frais, exactitude

**A2 étendu (10 paires).** Les 9 paires comptées gardent leurs
valeurs (§8.56.3, §8.69.2, re-vérifiées à l'identique, 0 écart) ;
la dixième, GSE79668, est positive sous le plancher :

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
| **GSE79668 (nouvelle)** | **+0,0567** | **non** | **oui** |
| **Total** | — | **6/10** | **8/10** |

**Leave-one-out sur les 10 paires (descriptif, même règle que
D3).** Retirer n'importe laquelle des 6 paires passantes donne
5/9 — sous la barre A2 d'origine en nombre de passantes (6).
Retirer GSE71729, GSE62452, GSE21501 ou GSE79668 (les quatre
non passantes) donne 6/9. Le verdict de suffisance tient donc
toujours à une paire — et désormais à six paires à la fois,
comme aux §8.59/§8.69 : chaque paire passante reste charnière.
L'ajout d'une paire positive sous le plancher ne consolide
rien en nombre de passantes (6/10 au lieu de 6/9) ; il dit
simplement que la dixième paire apporte un huitième positif,
pas la septième passante attendue par C3.

**Nuls frais (règle gelée §7 : `d_maxsep` dans [−0,07 ; +0,14[,
donc courus).** Graines 8701 et 8702, jamais utilisées dans ce
projet, gelées avant tout run :

| Nul | `maxsep` nul | `d_maxsep` (réel − nul) | > 0,07 ? |
|---|---|---|---|
| Graine 42 (paire gelée) | 0,3538 | **+0,0567** | non |
| Graine 8701 | 0,3215 | **+0,0890** | oui |
| Graine 8702 | 0,2566 | **+0,1538** | oui |

Valeurs exactes : nul s8701 `maxsep` 0,3214731637696184,
`d` = +0,08897527466809805 ; nul s8702 `maxsep`
0,2566001863019332, `d` = +0,15384825213178325. Distribution
des 3 écarts : min +0,0567, médiane +0,0890, max +0,1538.
Lecture gelée (§7) : un des 3 écarts est ≤ 0,07 — le passage
est donc dit **« fragile, non consolidé »**, et le verdict de
la paire graine 42 (PARTIEL) n'est JAMAIS changé par les nuls
frais. Les faits bruts, eux, sont dits plainement : le réel
(0,4104) bat 2 nuls frais sur 2 au-dessus du plancher, et le
nul graine 42 est le plus haut des trois nuls mesurés. À
n = 51, le tirage du nul pèse plus lourd (étendue 0,0972 entre
les trois nuls) que l'écart mesuré (0,0567) : un seul nul ne
suffit pas à trancher ici. C'est la même leçon que le §8.50
(10 nuls frais pour consolider un arbitrage) et le §8.46
(marge fragile) — appliquée ici à une paire principale, avec
2 nuls frais seulement, comme le protocole l'avait gelé.

**Exactitude.** Extracteur `extract_870.py` (4/4 runs, 0
manquant, versions `v6.2.0-L7aL7b-CohenD-short` partout) ;
second calcul indépendant `verify_870.py` (chemin de code
distinct, relecture directe des 4 JSON) : **4/4 comparaisons,
écart max 0,0 exact** sur `maxsep`, ancien MC et `stability`,
verdict OK. SHA du pipeline revérifié après travaux, inchangé.
Les 9 valeurs comptées sont reprises telles quelles de
`sep_maxsep_856_table.json` (SHA
`ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`)
et de `extract_869.json` (SHA
`644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b`),
jamais recalculées ici — les §8.56/§8.59/§8.64/§8.69 sont clos.

## 8.70.4 — La construction : table de matrice vide, fichier supplémentaire, comptages bruts

La paire GSE79668 est la première cohorte du chantier dont la
table de matrice est VIDE — et c'est un fait de construction,
pas un résultat. Les portes §5 passent toutes (7/7), sans
qu'aucun run ait été lancé avant leur vérification.

| Porte §5 | Exigé | Mesuré 20 nov. 2026 | Sort |
|---|---|---|---|
| Matrice HTTP 200, lecture complète | 200, SHA consigné | **200, 3 724 o, SHA `b2226fd0…88e4754`, 80 lignes, 0 ligne de données** | **OK** |
| Plateforme lue dans l'en-tête | GPL11154 | **GPL11154** (`!Series_platform_id`) | **OK** |
| n ≥ 40 tumeurs PDAC | ≥ 40 | **51/51 tumeurs** (titres `T_*`, aucune caractéristique « normal ») | **OK** |
| Aucun code-barres TCGA | 0 | **0** (titres et GSM inspectés) | **OK** |
| KRAS présent | oui | **oui, 1 ligne** (`KRAS_ENSG00000133703.7`) | **OK** |
| 12 gènes v4 présents | 12/12 | **12/12, 1 ligne chacun** | **OK** |
| Cas complets ≥ 40 | ≥ 40 | **51/51** (0 NaN) | **OK** |

**Adaptation documentée (protocole §4.1, cas prévu en règle
générale, appliqué tel quel).** La matrice
`GSE79668_series_matrix.txt.gz` (3 724 o, SHA
`b2226fd0…88e4754`) ne contient que l'en-tête : 80 lignes
décompressées, la ligne `ID_REF` + 51 GSM, **0 ligne de
données**. Les valeurs sont dans le fichier supplémentaire de
la SÉRIE ELLE-MÊME, nommé dans l'en-tête de la matrice
(`!Series_supplementary_file`) :
`GSE79668_51_tumors_sharedgenecounts.txt.gz` (HTTP 200,
3 588 753 o, SHA `721cd3a0…54f8`, 48 957 lignes décompressées,
48 956 gènes x 51 échantillons, 0 NaN). Ce n'est pas une autre
source : c'est le fichier de données de la même déposition,
soumise par les mêmes auteurs le même jour (29 mars 2016).
Aucun mapping GPL11154 n'a été construit : non nécessaire —
les identifiants de lignes sont de la forme
`SYMBOLE_ENSG...` (ex. `KRAS_ENSG00000133703.7`), le symbole
est le préfixe avant `_ENSG` (extraction mécanique,
48 956/48 956). Symboles dupliqués : 4 434 (plusieurs Ensembl
vers un même symbole) — agrégation par médiane (règle du
projet) ; les 13 gènes utiles (12 v4 + KRAS) ont chacun
exactement 1 ligne, aucune agrégation ne les touche. KRASP1
(pseudogène, `KRASP1_ENSG00000220635.2`) est une ligne
distincte, non confondue avec KRAS.
**Jointure échantillons : positionnelle** (même ordre dans la
matrice et dans le fichier de comptages), vérifiée : 49/51
radicaux de titres identiques, les 2 autres ne diffèrent que
par un « _T » final dans le titre de la matrice
(`T_06_01_A033a_T`, `T_06_04_A296a_T` → `T_06_01_A033a`,
`T_06_04_A296a` dans les comptages) ; après retrait de ce
suffixe, 51/51.
**Nature des valeurs : comptages bruts de transcrits**
(entiers, min 0 / médiane 17 / max 17 823 551), GENCODE v. 9,
d'après `!Sample_data_processing` : « Gene transcript sequence
counts for all genes across all tissues using GENCODE v. 9 ».
Ce ne sont ni des log2, ni des valeurs normalisées
(FPKM/RPKM/TPM). Aucune renormalisation, aucune transformation
log ajoutée (protocole §4.2) — les flux sont les comptages
bruts tels que fournis, ordonnés par KRAS croissant. L'ordre
est invariant par transformation log monotone : l'ordre KRAS
serait le même en log. KRAS (comptages bruts) : min 265 /
médiane 1 919 / max 3 707. CSV de flux :
`pdac_870_geo79668_fluxes.csv` (51 lignes, SHA
`7744bc5a…6107a`), nul SHA `50ae9a36…423e3` ; nuls frais SHA
`6fffd4fa…baee` (s8701) et `69c95e26…08b3` (s8702).

## 8.70.5 — Contrôles descriptifs (à publier, ne décident pas)

**Delta ne diverge PAS sur cette paire.** Delta réel 0,6353
contre nul 0,5886 (+0,0467 en faveur du réel) — un écart
minuscule, du même ordre que l'écart `maxsep` (+0,0567) et
dans le même sens. C'est l'inverse du §8.69, où Delta
favorisait fortement le réel (+2,01) pendant que `maxsep`
était négatif (−0,01). Ici, les deux scores disent la même
chose : une petite séparation positive, sous le plancher.
La divergence Delta/`maxsep` du §8.69 ne se reproduit pas —
c'est consigné tel quel, sans élucider sans preuve. Contre les
nuls frais, Delta reste plat aussi : +0,0514 (s8701) et
+0,0110 (s8702). Delta ne porte pas de signal caché ici.

**L7a ne change pas de sens.** Réel UP 0,3459, nul UP 0,3553 —
même direction, confiance quasi identique. Descriptif : L7a
n'est pas le critère gelé, et il ne distingue pas les deux
séries ici. Contre les nuls frais : UP 0,3534 (s8701) et UP
0,3154 (s8702) — UP partout, sur les 4 runs.

**Falsification : indisponible (n = 51 < 75, règle du projet).**
Notée « indisponible », non imputée (protocole §7). Les
valeurs brutes du JSON sont rapportées ici à titre descriptif
seulement, sans statut de test : réel 1,40578, nul 1,356433
(écart +0,0493, statut « ok » dans le JSON, seuil 0,5, les
deux au-dessus) ; nuls frais 1,235386 (s8701) et 1,17805
(s8702). Elles ne comptent pas comme un test de falsification.

**Cascades : formes différentes, scores proches.** Cascade
réelle [3,9 / 72,4 / 76,3 / 82,2 / 100,0] (pas 2/36/38/41/50)
contre nul graine 42 [0,0 / 23,3 / 27,1 / 33,1 / 52,1] (pas
0/12/14/17/26) : le réel atteint 100,0 % à T_+2, le nul
s'arrête à 52,1 %. Mais les cascades des nuls frais sont
elles-mêmes instables : s8701 [5,6 / 8,6 / 11,6 / 15,5 / 21,3]
(pas 3/4/6/8/11), s8702 [0,0 / 86,2 / 92,1 / 95,1 / 98,1]
(pas 0/43/46/48/49) — de 21,3 % à 98,1 % à T_+2 selon le
tirage du nul. La forme de la cascade nulle n'est pas une
caractéristique stable à n = 51 : elle ne distingue pas les
séries, elle mesure le tirage. Aucune rupture visible qui
distinguerait le réel des trois nuls à la fois.

**F1/F2 sans direction.** Réel ×9,72 / ×22,58, nul graine 42
×24,06 / ×15,01, s8701 ×8,99 / ×12,80, s8702 ×16,32 / ×15,10
— les rapports après/avant varient sans direction cohérente
(même figure qu'aux §8.58/§8.66/§8.69 : des rapports sans
direction ne font pas un signal). L7b est FRAGILE sur les
4 runs — même non-informativité que dans TCGA et les
confirmations GEO. Bruit : « Scores proxy complets
indisponibles » sur les 4 runs — aucun score de bruit
mesuré, consigné tel quel.

**Tests directs (§9) : l'ordre est là, `maxsep` ne le passe
pas au plancher.** (1) d de Cohen marginal des 12 flux,
réel vs nul graine 42 : **+0,0000 pour les 12 gènes** — par
construction, pas par hasard : le nul est une permutation
des lignes, donc chaque flux garde exactement ses 51 valeurs
(moyennes et écarts-types identiques). Le test ne mesure pas
la séparation : il valide la construction du nul
(marginales préservées exactement). C'est rapporté tel quel —
le protocole §9.1 gelait ce test sans voir qu'il était
vacueux par construction, et la section le dit au lieu de le
taire. (2) Test informatif ajouté (descriptif, §9.2) :
corrélation de Spearman de chaque flux avec le pas (ordre
KRAS). |ρ| moyen : réel 0,245 contre nul 0,075 ; Δρ médian
+0,186 ; Δρ positifs 9/12. Les plus forts : CEACAM5 Δρ
+0,513 (ρ réel +0,443), CLDN18 +0,414 (ρ +0,511), PGC +0,356,
KRT20 +0,346, REG4 +0,336 ; les négatifs : CR2 −0,256, MUC2
−0,136, CLCA1 −0,077. La série réelle porte donc bien des
tendances ordonnées par KRAS (9 flux sur 12 montent ou
descendent avec KRAS plus que leur nul) — mais le pipeline,
sur cette paire à n = 51, ne convertit ces tendances qu'en
+0,0567 de `maxsep`, sous le plancher. L'ordre est mesurable
directement ; il ne suffit pas au score gelé.

**Nature des valeurs.** Les flux sont des comptages bruts
RNA-seq, pas des log-intensités comme les autres paires V1
ni des log-ratios comme GSE21501 : chaque gène est un nombre
entier de lectures, fortement asymétrique (médiane 17 sur
l'ensemble des gènes, max 17,8 M). L'ordre par KRAS reste un
ordre par KRAS (invariant par log). Cette différence de
nature est nommée ; elle n'est pas une excuse au verdict —
les autres paires GEO (intensités, log-ratios) comptent des
échecs (GSE71729, GSE62452, GSE21501) comme des succès, et
rien ne permet de dire que le comptage brut, plutôt que la
cohorte ou le tirage du nul, explique le quasi-passage. Un
chantier futur qui voudrait tester l'hypothèse « nature des
valeurs » devrait comparer des cohortes, pas invoquer la
nature après coup.

## 8.70.6 — Ce que ça change, et ce que ça ne change pas

| Poste | Change ? | Détail |
|---|---|---|
| Condition C3 (§8.59.8) | **Non levée** | Une paire indépendante mesurée, elle est PARTIELLE : A2 étendu 6/10 (8/10 positifs). La confirmation indépendante reste ouverte. |
| Adoption pleine de `maxsep` | **Non — décidée par Zackary le 20 nov. 13h04** | Ce chantier est une vérification a posteriori, pas une condition. L'adoption pleine reste sa décision ; la présente section la consolide par son honnêteté, pas par son verdict. |
| Score MC affiché (convention §8.64.6) | Non | `maxsep` principal, ancien MC secondaire, `sep` compagnon, mention de fragilité — inchangée. |
| Sélection du best_config, seuil MC, cascade, S_sep, Delta, L7a | Non | Inchangés par construction. |
| Code v6.2 / v6.1 / v6 | Non | Aucune modification, aucune v6.5. |
| Verdicts des §8.56, §8.59, §8.64, §8.69 | Non | Confirmés, pas rouverts ; les 9 paires comptées gardent leurs valeurs. |
| Pistes ouvertes | Oui, une de plus | (a) Une autre paire indépendante pourrait encore lever C3 — avec son propre protocole gelé ; la piste GSE79668 est désormais fermée comme paire principale (mesurée, PARTIELLE) ; (b) la fragilité du nul à petit n (étendue 0,0972 entre 3 nuls à n = 51) mérite un chantier propre : combien de nuls faut-il pour un plancher stable à n ≈ 50 ? — à rapprocher du §8.53 (∼200 nuls pour un plancher stable à petit n) ; (c) la divergence Delta/`maxsep` du §8.69 ne se reproduit pas ici — elle reste une piste ouverte, pas une loi. |

**Suite du dossier.** Si Zackary veut une nouvelle tentative de
confirmation : un chantier ultérieur, avec son propre protocole
gelé, sur une autre cohorte vérifiée indépendante — pas une
relecture, pas un re-test déguisé, et pas GSE79668 (mesurée).
Si Zackary ne veut pas de nouvelle tentative : C3 reste
ouverte, l'adoption pleine tient par sa décision du 20 nov.
13h04, et la présente section consigne le quasi-passage mesuré
avec ses chiffres — elle n'est pas effacée. Dans les deux cas,
le PDF et GitHub sont régénérés et poussés par le coordinateur
(règle permanente « Toujours github et pdf !!! »), avec la
présente section fusionnée.

## 8.70.7 — Limites et ce qui reste

- Une seule paire nouvelle a été mesurée : le verdict porte sur
  elle, pas sur « `maxsep` en général ». 6/10 et 8/10 sont des
  comptages sur 10 paires, pas des estimations de population.
- La paire est construite sur des comptages bruts RNA-seq,
  nature différente des autres paires V1 (log-intensités,
  RNA-seq log, log-ratios) : la comparaison est faite à
  construction égale (variante (a), 12 gènes, ordre KRAS), pas
  à nature de mesure égale — c'est nommé au §8.70.5, pas
  corrigé après coup.
- À n = 51, le tirage du nul pèse plus lourd que l'écart mesuré
  (étendue 0,0972 entre 3 nuls, écart 0,0567) : 2 nuls frais
  seulement ont été courus (règle gelée §7) — une distribution
  complète (10 nuls, comme au §8.50) n'a pas été mesurée ici,
  et le verdict ne repose que sur la paire graine 42, par
  règle gelée. Un chantier futur qui voudrait consolider
  GSE79668 devrait courir 10 nuls frais — mais le verdict de
  la paire graine 42 resterait PARTIEL, par construction.
- Le d de Cohen marginal du §9.1 est vacueux par construction
  (0,0000 pour les 12 gènes) : le protocole gelait ce test sans
  voir que la permutation de lignes préserve les marginales.
  La section le dit et ajoute le test de Spearman contre le
  pas, qui porte l'information d'ordre — une correction de
  méthode à reporter dans les protocoles futurs, pas un
  résultat tu.
- La table de la matrice est vide : les valeurs viennent du
  fichier supplémentaire de la série (même dépôt, même série,
  nommé dans l'en-tête). Si ce fichier n'avait pas existé, la
  cohorte aurait été inutilisable — la porte §5 ne prévoyait
  pas ce cas explicitement, et l'adaptation est documentée
  ici (§8.70.4), pas dans le protocole gelé.
- Delta ne diverge pas ici (+0,05) : la divergence du §8.69
  (+2,01 contre −0,01) n'est ni confirmée ni infirmée comme
  phénomène — une seule paire de plus, dans l'autre sens.
  L7b est FRAGILE sur les 4 runs — non-informatif, comme
  partout.
- Rien de clinique : l'étude porte sur l'instrument.

## 8.70.8 — Provenance

- Protocole gelé : `PROTOCOL_maxsep_gse79668_870.md`, SHA-256
  `fd479d50414a18c2daa2b7cb9aeab55dcc24a49ae30ed6ceee363b4d47c96980`
  (au gel, avant téléchargement ; fichier inchangé depuis).
  Note sur le libellé « 7/8 » de la mission et du §8.59.8 :
  lecture précise retenue (§8.69 §7) — **7 paires passantes au
  total**, soit 7/10 avec la dixième paire, LOO pire cas 6/9.
- Provenance complète : `PROVENANCE_870.md`, SHA-256
  `5e5d26a71d9b1eef7cccfd822496c10ea623b361b517fb31cbaeb6e93b21aad0`.
- Construction : `build_fluxes_870.py`, SHA-256
  `4dfdd6d6f7c88e8ac6327d09e0b40cda4fd628a75e9d863511e1c0f72354b949`
  (variante (a) seulement ; adaptation §4.1 documentée : table
  de matrice vide, valeurs dans le fichier supplémentaire de la
  série, symboles = préfixes avant `_ENSG`).
- Données : `data/GSE79668_series_matrix.txt.gz`, 3 724 o,
  SHA-256
  `b2226fd096f27a9e5caf32cca3491d1f1e52082ce6e9876b2b1c1f67d88e4754`
  (HTTP 200, 20 nov. 2026) ; `data/GSE79668_51_tumors_sharedgenecounts.txt.gz`,
  3 588 753 o, SHA-256
  `721cd3a0d1155375ea054f410f65497568284135f32ad59157d62a564cba54f8`
  (HTTP 200, 20 nov. 2026). Aucun mapping GPL11154 construit
  (non nécessaire — symboles dans les identifiants de lignes).
- Flux : `pdac_870_geo79668_fluxes.csv` (51 lignes), SHA-256
  `7744bc5a82fe80055b5ab9231fc7ae5395354f643b5b7cd1fdfce8aa6656107a` ;
  `pdac_870_geo79668_fluxes_nul.csv`, SHA-256
  `50ae9a361fe961c55eca7587f0b21c2b0a1e403aee0973758dabf3960fc423e3` ;
  `pdac_870_geo79668_fluxes_nul_s8701.csv`, SHA-256
  `6fffd4fa497371c3f4d0f21e208270eec69185f3ea575022df1c677c09debaee` ;
  `pdac_870_geo79668_fluxes_nul_s8702.csv`, SHA-256
  `69c95e26b31a2cdfd2c9a4463fe080bc09648379c9d0856d46fd6db7532808b3`.
- Runs : manifeste `manifest_v62_870.txt`, SHA-256
  `9c107fa469d018399a7d443dd7117a3a7ee79c2eed294fede66c904666d3751f` ;
  journal `runs_v62_870.log` (202 lignes), SHA-256
  `33b8bcb52ed7f66b7216e10568da7c0b3497048578c113bed1c057b287cbe89b` ;
  surveillance `watch_v62_870.sh`, SHA-256
  `2b69240c5815b5efd54c37f26a736bf9770f17167d7e83327779eabe77fbd90c` ;
  dossiers `results_fast_v62_870_geo79668[_nul|_nul_s8701|_nul_s8702]`
  (4 runs, exits 0/0/0/0, 35 fichiers chacun).
- Extraction : `extract_870.py`, SHA-256
  `4cd363e62e7031b74ce22977106135503ebefdb2ace5967edaa59558dcde86a2`
  → `extract_870.json`, SHA-256
  `4ffa851a83668b2369097703862e0413ff9af54af3a66ef70aea9333b40c444f` /
  `extract_870.csv`, SHA-256
  `cfab3f9f150fc2ee645f3140d12731a5184b2d6c3c3fc674bc2416458c21fa89`.
- Vérification indépendante : `verify_870.py`, SHA-256
  `67fd2c3b12cb9570432342a19686e1a8f634b4443b3a388e9d6915ace5e83c9b`
  → `maxsep_870_verify.json`, SHA-256
  `f106577c517811b886783c839d76e432bbc5489f1ba4f8c55501b7db855457c5`
  (4/4 comparaisons, écart max 0,0 exact, verdict OK).
- Tests directs : `direct_tests_870.py`, SHA-256
  `a3d8499e0ed4439ef4a5cb2cbafce87cd096256c135b59152f89568671677662`
  → `direct_tests_870.json`, SHA-256
  `2843d5edd07a7ba371478c54cc90a5a227f4ce8dd793517e2c166f6219e97fb3`.
- Références re-vérifiées : `sep_maxsep_856_table.json`, SHA-256
  `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`
  (8 paires V1 reprises telles quelles, jamais recalculées ici) ;
  `extract_869.json`, SHA-256
  `644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b`
  (GSE21501 reprise telle quelle) ; protocole §8.69
  `PROTOCOL_maxsep_independent_869.md` (SHA-256
  `be0a02ca7ffdc75dbf8bd069b48890b227143d4888c16cd92b751599be2e8ab9`,
  corps gelé `86c239b4…e61a52` + addendum) ; section §8.69
  `section_8.69_maxsep_independent.md`.
- Livre blanc de référence consulté :
  `livre-blanc-pdac-v6.md`, 13 896 lignes, SHA-256
  `102038901e8421b36c65e561112f1537a0386ee81d5a2e2b86f57986e7385855`
  (§8.1–§8.69, état au 20 nov. 2026) — le livre blanc n'a PAS
  été modifié par ce chantier. Fusion de la présente section par
  le coordinateur.
- Données : séries réelles = comptages bruts RNA-seq (mesures
  instrumentales transformées : comptages par les déposants,
  symboles extraits mécaniquement, agrégation des doublons par
  médiane, ordre par KRAS). Nuls = lignes permutées, graines
  42 / 8701 / 8702 — échantillons hypothétiques, pas des
  mesures. Aucune valeur inventée ; aucune valeur recopiée
  à la main (tables générées depuis `extract_870.json`, vérifiées
  paire par paire à 0,0 exact par `verify_870.py` ; les valeurs
  des §8.70.2–§8.70.3 sont lues dans cette sortie, pas recopiées
  des §8.56/§8.59/§8.64/§8.69).
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`, revérifié avant
  ET après chaque lot), v6.1 (`2af5e5ce…c1c9`), v6
  (`bb8bbdba…c0773`). Aucune nouvelle version construite dans ce
  chantier — pas de v6.5. Quatre runs du pipeline lancés dans ce
  chantier (GSE79668 réel + 3 nuls, exits 0/0/0/0) ; aucun push
  GitHub, aucune Release dans ce chantier.
- Section : `section_8.70_gse79668.md` (ce fichier ;
  SHA noté au rapport).

---

## ADDENDUM — 20 novembre 2026 (§8.72) : NOTE DATÉE DE CORRECTION — LECTURE RENVERSE

*Cet addendum est ajouté le 20 nov. 2026 par le chantier §8.72. Le
texte original ci-dessus est intact : rien n'y est modifié, rien
n'y est effacé. Seule la LECTURE du verdict est corrigée, comme le
protocole §8.72 §4.3 l'avait gelé.*

**Correction.** La lecture « sous le plancher » du §8.70 est
RENVERSE par la distribution des nuls mesurée au §8.72
(`section_8.72_nulls_gse79668.md`, protocole
`PROTOCOL_nulls_gse79668_872.md`, SHA `95acdd45…cf41`) :
10 nuls frais (graines 8721–8730) courus en v6.2 fast, joints
aux 3 nuls anciens, donnent une médiane des 13 nuls de 0,2657
et un écart médian `d_médian = +0,1447` (réel 0,4104 contre nul
médian 0,2657) — plus de deux fois le plancher 0,07. Le réel
bat les 13 nuls sur 13 (rang 14/14) ; 12 écarts sur 13
dépassent le plancher. Le nul graine 42 (0,3538), celui qui
faisait le verdict §8.70, est le PLUS HAUT des 13 nuls
mesurés : le verdict PARTIEL tenait au tirage le plus
défavorable possible.

**Ce qui ne change pas.** Le verdict de la paire graine 42
reste PARTIEL (+0,0567, sous le plancher) — règle gelée §8.70
§7. L'A2 étendu gelé reste 6/10 (8/10 positifs) : aucun
recomptage. La condition C3, au sens gelé (7 paires passantes
en paires graine 42), n'est pas levée par le §8.72 : la
décision de la lever sur la base de la distribution appartient
à Zackary et au coordinateur (§8.72.2). L'adoption pleine de
`maxsep` (décision de Zackary, 20 nov. 13h04) n'est ni
rouverte ni conditionnée.

— Fin de l'addendum du 20 nov. 2026 (§8.72). —
