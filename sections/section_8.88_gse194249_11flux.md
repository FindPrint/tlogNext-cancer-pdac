# §8.88 — GSE194249 à 11 flux : quinzième paire NON — `maxsep` ne sépare pas, le réel est dans la distribution des nuls (21 novembre 2026)

Piste 2 du lot du 21 nov. 2026 ; protocole gelé 21 nov. 2026
~10h10 EST avant toute construction et tout run
(`PROTOCOL_gse194249_11flux_888.md`, SHA
`f5eb1f952f562499e6ff31036b684cb75d094a2843a17a067acf27ca7c763e02`) ;
provenance `PROVENANCE_888.md`. Go de Zackary : 21 nov. 2026,
10h07. Cette section exécute la suite (d1) nommée au §8.86.4 :
la paire à **11 flux** (sans DPCR1), « comme la C3 du §8.79,
avec son caveat écrit ».

## Verdict d'abord

**NON — la quinzième paire principale indépendante, GSE194249
(84 PDPCOs, 11 flux, DPCR1 absent), donne
`d_maxsep = −0,0239` (réel 0,2306 contre nul 0,2545) : le nul
graine 42 sépare PLUS que le réel, et l'écart est négatif.
A2 devient 10/15 au-dessus du plancher, 12/15 positifs,
LOO 9/14. La condition C3 du §8.59.8, levée au §8.71,
RESTE LEVÉE (ce chantier est une consolidation
supplémentaire, pas une condition ; il ne rouvre rien).**

**Et, dans la même phrase, la lecture des nuls frais : les 2
nuls frais courus selon la règle gelée (`d` dans
[−0,07 ; +0,14[) donnent des écarts positifs mais sous le
plancher — +0,0517 (s8881) et +0,0354 (s8882). Les 3 écarts
sont −0,0239 / +0,0354 / +0,0517 (min / médiane / max) :
aucun des 3 n'est au-dessus du plancher 0,07. Le `maxsep`
réel (0,2306) est DANS la distribution des trois nuls
mesurés (0,1789 à 0,2545, étendue 0,0756) : il ne s'en
distingue pas. Le verdict de la paire graine 42 (NON) n'est
JAMAIS changé par les nuls frais (règle gelée) — et il ne
l'est pas ici : les nuls frais confirment l'échec, ils ne
l'atténuent pas.**

| Porte (protocole §5/§8, gelé) | Exigé | Mesuré 21 nov. 2026 | Sort |
|---|---|---|---|
| Matrice détenue, SHA identique au §8.86 | `479517fb…0f27` | **identique, 4 927 876 o** | **PASSE** |
| 11 gènes v4 retenus présents, un par un | 11/11 | **11/11, une ligne chacun** | **PASSE** |
| DPCR1 absent (paire pré-enregistrée à 11 flux) | absent | **0 occurrence, MUCL3 0 aussi** | **PASSE** |
| KRAS présent, cas complets ≥ 40 | ≥ 40 | **84/84 complets, 0 NaN** | **PASSE** |
| Quinzième paire : `d_maxsep > 0,07` et positif | > 0,07 | **−0,0239** (réel 0,2306, nul 0,2545) | **NON** |
| Nuls frais (§8, `d` dans [−0,07 ; +0,14[) | 2 nuls frais | **+0,0517 / +0,0354** (0/3 > 0,07) | **ÉCHEC CONFIRMÉ** |
| A2 des paires indépendantes | 10/14, 12/14 positifs | **10/15, 12/15 positifs** | **ÉTENDU** |
| LOO sur 15 paires (pire cas) | 9/13 | **9/14** | **ÉTENDU** |
| Exactitude de l'extraction | 4/4 à 0,0 exact | **4/4, écart max 0,0** | **PASSE** |
| 11 flux présents, DPCR1 absent | 11/11, 0 DPCR1 | **11/11, DPCR1 0/15 609, MUCL3 0** | **PASSE** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que
`maxsep` ne sépare pas le réel du nul sur une quinzième
cohorte indépendante — la deuxième cohorte d'organoïdes du
projet, et la première où le nul graine 42 dépasse le réel
en `maxsep` (0,2545 contre 0,2306) et en cascade (58–83 %
contre 26–46 %). Il dit aussi que le signal d'ordre direct
est pourtant présent (Δρ médian +0,191, 9/11 flux positifs —
voir §8.88.6) : `maxsep` échoue ici ALORS QUE les flux
individuels montrent une tendance monotone — la rupture
multi-flux n'est pas plus forte que ce qu'une permutation
produit par hasard sur cette cohorte. Il ne dit pas que
`maxsep` est invalidé en général : c'est une quinzième
paire, négative, pas une preuve. Il ne dit pas que
l'adoption pleine est remise en cause par ce chantier seul :
elle a été décidée par Zackary après lecture des
§8.56/§8.59/§8.64, et cette section est la vérification
a posteriori que le protocole prévoyait — elle ne consolide
pas la décision, elle la met en tension, et c'est dit tel
quel. Il ne dit rien de clinique : l'étude porte sur
l'instrument, pas sur un remède — aucune affirmation sur le
cancer du pancréas n'est tirée de ce lot.

**Fragilité, dite en tête.** Le verdict tient à une seule
paire mesurée aujourd'hui, mais il n'est pas fragile au sens
du §8.85 : les trois tirages de nul donnent des `maxsep`
de 0,1789 à 0,2545, et le réel (0,2306) est au milieu
d'eux — aucun des trois écarts ne passe le plancher, et
l'écart de la paire graine 42 est négatif. Ce n'est pas un
échec de justesse : c'est un échec sur trois tirages. La
paire compte 11 flux, pas 12 — toute comparaison aux paires
à 12 flux doit le rappeler, et toute lecture future qui
présenterait cette paire comme une paire à 12 flux serait
fausse. Enfin, le test direct d'ordre est positif alors que
`maxsep` échoue — cette divergence, miroir exact de celle
du §8.85 (`maxsep` passe / ordre faible), est consignée
telle quelle au §8.88.6, sans être élucidée sans preuve.

## 8.88.1 — La dérogation à 11 flux, et pourquoi la paire est indépendante

### La dérogation, gelée avant tout run

La porte « 12 gènes v4 présents » avait dit ARRÊT au §8.86
pour GSE194249 comme paire à 12 flux. La dérogation à 11 flux
est celle du §8.79 (addendum C3, GSE57495 à 11 flux, GSTM1
absent) : écrite AVANT toute construction et tout run, dans
le protocole gelé `PROTOCOL_gse194249_11flux_888.md`
(SHA `f5eb1f95…763e02`), avec le go de Zackary du 21 nov.
10h07 ; limitée à un seul gène nommé, DPCR1 ; l'absence est
un fait du fichier déposé, vérifié deux fois au §8.86 et
re-vérifié deux fois ici avant le gel (§8.88.1, tableau
ci-dessous) ; aucun remappage — le gène n'est mesuré sous
aucun nom dans la matrice déposée ; la comparabilité est
limitée et le caveat « 11 flux, DPCR1 absent » est écrit
dans le verdict, dans la table A2 et dans la provenance ;
la suite était pré-nommée au §8.86.4 (d1).

### Présence des gènes, vérifiée dans la matrice détenue

Matrice détenue : `data/GSE194249_PDPCOs_FPKM.txt.gz`,
4 927 876 o, SHA-256
`479517fbed1d8f5bb9d141b6b932b6ab56ba2ba72d4394d13aea2a3da0a50f27`
— identique au §8.86. Premier chemin (lecture pandas,
21 nov. 2026 ~10h05 EST) ; second chemin (zgrep sur le
fichier brut gzip, même jour) — mêmes comptages :

| Gène | Lignes exactes | Gène | Lignes exactes |
|---|---|---|---|
| PGC | 1 | CR2 | 1 |
| REG4 | 1 | KRT20 | 1 |
| CLDN18 | 1 | MUC2 | 1 |
| MUC17 | 1 | GSTM1 | 1 |
| **DPCR1** | **0** | CEACAM5 | 1 |
| CLCA1 | 1 | MUC16 | 1 |
| KRAS (contrôle) | 1 | MUCL3 (descriptif) | 0 |

**11/11 gènes v4 retenus présents, une ligne chacun,
0 doublon ; KRAS présent, une ligne. DPCR1 : 0 occurrence
dans tout le fichier (exact, insensible à la casse) ;
MUCL3 : 0 ; aucun symbole contenant `DPCR`.** Aucun autre
gène ne manque : la condition d'arrêt du protocole (§3 —
« si un autre gène manque aussi, fermer la piste ») ne
s'est pas déclenchée.

### La cohorte : GSE194249, 84 PDPCOs

Série GSE194249, Shi et al., Nat. Commun. 2022, 13:2169,
DOI 10.1038/s41467-022-29857-6. **Aucun nouveau
téléchargement dans ce chantier** : la matrice et les
métadonnées sont celles du §8.86, re-vérifiées par SHA
avant construction. 87 colonnes = 84 PDPCOs + 3 `NPC-*`
(normaux, exclus) ; composition des retenus : 75 PDAC,
4 IPMN, 4 NEN, 1 ACC.

**Construction (variante (a), 11 flux).** Valeurs FPKM
telles que déposées, sans renormalisation, sans
transformation log, sans imputation. Flux : PGC, REG4,
CLDN18, MUC17, CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1,
MUC16. Contrôle : KRAS (FPKM : min 3,1647 / médiane
13,2894 / max 24,9045) ; `step` = rang 0..83. Cas
complets : 84/84, 0 NaN. Portes §5 : 6/6 OK — dont DPCR1
absent (confirmé par le script de construction, qui
s'arrêterait si DPCR1 apparaissait) et MUCL3 absent.
CSV réel `pdac_888_gse194249_fluxes.csv` (SHA
`7799a62a…aeda`) ; nul graine 42 (SHA `2f633871…4569`).
La reconstruction du CSV réel lors de la construction des
nuls frais donne le même SHA exact — reproductibilité
vérifiée.

**Indépendance — le statut exact.** (1) Jamais courue comme
paire pipeline : aucun CSV, aucun run, aucun JSON, aucune
valeur `maxsep` n'existait pour GSE194249 avant ce
chantier (confirmé par l'absence des fichiers `886`).
(2) Patients distincts par construction de programme
(biobanque PDPCO de Shanghai, identifiants `CAS-*` /
`NPC-*` vs barres TCGA, GSM GEO des autres séries, ICGC)
— limite déclarée : aucun identifiant commun n'existe
entre les systèmes, donc pas de preuve par jointure.
(3) Grep du livre blanc : « GSE194249 » 34 occurrences,
toutes au §8.78 (inventaire C4), au §8.79.9 (piste ouverte
(d)) et au §8.86 — jamais comme cohorte courue, jamais
comme holdout, jamais comme valeur `maxsep` ; « Shi et
al » 4 occurrences, toutes dans le §8.86 ; « CAS-DAC »
2 occurrences, toutes dans le §8.86. (4) Statut :
transversale, ordonnée par KRAS — même statut que
TCGA/ICGC, pas de pseudo-temps ; des organoïdes dérivés
de patients, pas des tumeurs primaires directes — le
verdict porte sur l'instrument.

## 8.88.2 — Les runs et l'extraction

- Lot : 4 runs v6.2 mode fast — réel + nul graine 42, puis
  2 nuls frais (graines 8881, 8882) selon la règle gelée
  (`d_maxsep = −0,0239` dans [−0,07 ; +0,14[) —
  manifestes `manifest_v62_888.txt` +
  `manifest_v62_888_frais.txt`, lanceur reprenable
  `run_v62_lot.sh`, unités systemd `v62-888` et
  `v62-888frais` (leçon AGENTS.md 2026-11-17 : jamais
  nohup). **4/4 runs exit 0** (FIN 21 nov. 2026 15h23:29Z
  pour la paire, 15h36:25Z pour les nuls frais ; durées
  allongées par la contention CPU — d'autres lots v6.2
  tournaient en parallèle sur la VM partagée).
- SHA du pipeline revérifié avant ET après les lots, inchangé :
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
- Extraction `extract_888.py` (réutilise `extract()` de
  `extract_858.py`, original intact) : 4/4 runs, 0 manquant.
  Second calcul indépendant `verify_888.py` (chemin de code
  distinct, relecture directe par `json.load`) recoupe
  `maxsep`, ancien MC et stabilité à **0,0 exact sur les
  4 runs** (`maxsep_888_verify.json`, verdict OK). Version
  lue : `v6.2.0-L7aL7b-CohenD-short` sur les 4 runs. Second
  calcul indépendant des écarts `d_maxsep` depuis les
  `master_results.json` : −0,0239 / +0,0517 / +0,0354,
  identiques à l'extraction (écart 0,0 exact).

| Run | n | maxsep | ancien MC | S_sep | Delta | L7a | Cascade (Q1–Q5, %) |
|---|---|---|---|---|---|---|---|
| Réel GSE194249 | 84 | **0,2306** | 0,3350 | 0,2293 | 0,991 | up 0,352 | 26,0 / 34,1 / 39,5 / 43,1 / 45,5 |
| Nul graine 42 | 84 | 0,2545 | 0,3380 | 0,2533 | 0,935 | up 0,350 | 58,1 / 71,0 / 74,4 / 77,9 / 82,6 |
| Nul frais s8881 | 84 | 0,1789 | 0,3265 | 0,1778 | 0,947 | up 0,348 | 24,6 / 55,5 / 59,5 / 63,2 / 74,4 |
| Nul frais s8882 | 84 | 0,1952 | 0,3289 | 0,1945 | 0,998 | up 0,357 | 0,0 / 46,7 / 50,2 / 54,3 / 54,3 |

Valeurs complètes : `maxsep` réel 0,23059240234506262 ; nul
s42 0,2545160157551329 ; s8881 0,1788799298592756 ; s8882
0,19522875362904593. Stabilité : réel 0,9944 ; nul 0,9952 ;
s8881 0,9937 ; s8882 0,9964. Seuils MC : réel 70,73 ; nul
53,66 ; s8881 17,07 ; s8882 82,93. Pas de cascade : réel
[22, 28, 33, 36, 38] ; nul [48, 59, 62, 65, 69] ; s8881
[20, 46, 49, 52, 62] ; s8882 [0, 39, 42, 45, 45]. F1/F2 après
seuil : réel 3,7724 / 8,7736 ; nul 1,1943 / 0,8747 ; s8881
0,0527 / 0,0190 ; s8882 21,9736 / 43,6063 (descriptif, voir
§8.88.5). Falsification : disponible (n = 84 ≥ 75), statut
`ok` — réel 1,090427 contre nul 1,053223 (écart +0,0372,
descriptif) ; s8881 1,116066 ; s8882 0,98497. L7b :
FRAGILE sur les 4 runs — l'audit L7b est clos comme
non-informatif (il dit FRAGILE sur le réel comme sur les
nuls) ; il n'est pas rapporté comme une mesure de fragilité.
Régime : `saturation` pour les 4 runs. Estimateurs « tous ok » :
27 sur les 4 runs.

## 8.88.3 — Le verdict étendu : A2 à 10/15

Table des 15 paires principales indépendantes comptées
(valeurs des §8.56 / §8.69 / §8.70 / §8.71 / §8.74 / §8.79 /
§8.85 reprises telles quelles, jamais recalculées ; GSE194249
mesurée ici). Écart = maxsep réel − maxsep nul. Plancher 0,07.
Le lot FNA §8.76 n'y figure PAS — il est apparié au §8.74,
pas indépendant. Le lot drogue §8.84 n'y figure PAS — il est
hors compte (objet drogue, pas paire d'expression).

| Paire | maxsep R / N | Écart | > 0,07 ? | Positif ? |
|---|---|---|---|---|
| HP35 | 1,7718 / 0,1206 | **+1,6512** | oui | oui |
| TCGA v4 | 0,4623 / 0,1696 | **+0,2928** | oui | oui |
| GSE71729 | 0,2593 / 0,2191 | +0,0402 | non | oui |
| GSE62452 | 0,3100 / 0,3136 | −0,0036 | non | NON |
| ICGC | 0,4080 / 0,3110 | **+0,0970** | oui | oui |
| Immunitaire TCGA | 0,5309 / 0,1634 | **+0,3675** | oui | oui |
| PARP TCGA | 0,3680 / 0,1992 | **+0,1688** | oui | oui |
| DepMap | 0,4436 / 0,2532 | **+0,1904** | oui | oui |
| GSE21501 (§8.69) | 0,2121 / 0,2221 | −0,0100 | non | NON |
| GSE79668 (§8.70) | 0,4104 / 0,3538 | +0,0567 | non | oui |
| GSE60979 (§8.71) | 0,4418 / 0,2373 | **+0,2045** | oui | oui |
| GSE131050 Yeh FF (§8.74) | 0,3220 / 0,2481 | **+0,0739** | oui | oui |
| GSE57495 (§8.79, 11 flux) | 0,6381 / 0,1887 | **+0,4494** | oui | oui |
| GDC ORGANOID-PANCREATIC (§8.85, 12 flux, MUCL3 ex-DPCR1) | 0,2542 / 0,1658 | **+0,0884** | oui | oui |
| **GSE194249 (§8.88, 11 flux, DPCR1 absent)** | **0,2306 / 0,2545** | **−0,0239** | **non** | **NON** |

Bilan : **10/15 au-dessus du plancher, 12/15 positifs.**
LOO pire cas : retirer une paire passante donne 9/14 —
**LOO 9/14** (contre 9/13 avant cette paire). C3 du §8.59.8
RESTE LEVÉE — elle l'était depuis le §8.71 ; cette paire
est une consolidation supplémentaire manquée, pas une
condition.

**La décision de compter cette paire dans A2 avait été
prise AVANT les runs** (protocole §2.3, avec le précédent
§8.79 et la différence avec le §8.84 hors compte écrites
d'avance) : elle n'est pas révisée parce que la paire
échoue. Un compte qui n'inclurait que les paires passantes
serait un compte biaisé.

## 8.88.4 — Les nuls frais : échec confirmé sur trois tirages

`d_maxsep = −0,0239` est dans l'intervalle [−0,07 ; +0,14[
qui déclenche les nuls frais (graines 8881, 8882, gelées
dans le protocole, jamais utilisées dans ce projet). Les
2 nuls frais ont donc été construits par la même méthode et
courus en runs frais, comme la règle gelée l'exige :

| Écart contre | maxsep nul | `d_maxsep` | > 0,07 ? |
|---|---|---|---|
| Nul graine 42 (verdict) | 0,2545 | **−0,0239** | NON |
| Nul frais s8881 | 0,1789 | **+0,0517** | NON |
| Nul frais s8882 | 0,1952 | **+0,0354** | NON |

Écarts min / médiane / max : **−0,0239 / +0,0354 / +0,0517**.
0 sur 3 au-dessus du plancher. Lecture gelée : aucun des 3
écarts n'est > 0,07 — le passage n'a pas lieu, et l'échec
est dit **« confirmé, non fragile »** au sens où il ne tient
pas à un seul tirage de nul défavorable : le `maxsep` réel
(0,2306) est encadré par les nuls (0,1789 et 0,1952 en
dessous, 0,2545 au-dessus). Le verdict de la paire graine 42
(NON) n'est JAMAIS changé par les nuls frais, et il ne l'est
pas ici. C'est le miroir du §8.85, où un nul frais passait
sous le plancher alors que la paire passait : ici, c'est la
paire elle-même qui est négative, et les deux nuls frais
restent sous le plancher. La fragilité du nul à petit n
(§8.53, §8.70) ne joue pas ici en faveur du réel : à
n = 84, trois tirages de nul donnent des `maxsep` de 0,1789
à 0,2545 (étendue 0,0756), et le réel est dedans.

## 8.88.5 — Les scores compagnons : rien ne sépare, sauf Delta (faible)

- **`sep` compagnon ne passe PAS sa barre descriptive, et
  il est négatif comme `maxsep`.** `sep` réel 0,1874 contre
  nul 0,2029 : `d_sep = −0,0155`, sous le plancher
  équivalent-sep `0,07·(1+m_R)(1+m_N) = 0,1081`. (D4 n'est
  pas rejoué ici : il porte sur les paires V1, déjà tranché.)
  Au §8.85, `sep` ne passait pas non plus sa barre alors que
  `maxsep` passait ; ici les deux sont négatifs ensemble.
- **S_sep suit `maxsep` presque à l'identique, et partage
  son échec.** S_sep réel 0,2293 contre nul 0,2533 :
  `−0,0240` ; contre les nuls frais : +0,0516 (s8881) et
  +0,0348 (s8882) — même lecture que `maxsep` : 0/3
  au-dessus du plancher.
- **Ancien MC, négatif et minuscule.** MC réel 0,3350
  contre nul 0,3380 : `−0,0029` — comme aux §8.70/§8.74/
  §8.79/§8.85, MC ne sépare pas seul ; ici il ne sépare pas
  du tout. Les nuls frais sont à 0,3265 et 0,3289 : le réel
  ne les dépasse que de 0,0085 et 0,0061. `maxsep` reste le
  score principal par décision de Zackary (20 nov. 13h04) ;
  MC est secondaire.
- **Delta : écart réel–nul positif, mais dans l'étendue
  nulle.** Delta réel 0,991 contre nul 0,935 : `+0,0563` —
  mais les nuls frais sont à 0,947 et 0,998 : Delta varie de
  0,935 à 0,998 entre les trois nuls (étendue 0,063), soit
  plus que l'écart réel–nul. Aucune divergence
  Delta/`maxsep` à élucider ici : Delta ne distingue pas le
  réel du nul sur cette paire de façon stable, `maxsep` non
  plus — et cette instabilité de Delta entre nuls est
  consignée telle quelle.
- **L7a : up des quatre côtés, sans écart.** Réel up 0,3521,
  nul up 0,3503, s8881 up 0,3479, s8882 up 0,3567 — le nul
  frais s8882 est au-dessus du réel. Descriptif : L7a n'est
  pas le critère gelé.
- **Cascade : le nul monte plus tôt et plus haut que le
  réel.** Réel [26,0 / 34,1 / 39,5 / 43,1 / 45,5], pas
  [22, 28, 33, 36, 38] ; nul s42 [58,1 / 71,0 / 74,4 /
  77,9 / 82,6], pas [48, 59, 62, 65, 69]. Le nul graine 42
  atteint 58,1 % dès Q1, là où le réel n'atteint que 45,5 %
  en Q5. Les nuls frais montent aussi : s8881
  [24,6 / 55,5 / 59,5 / 63,2 / 74,4], s8882
  [0,0 / 46,7 / 50,2 / 54,3 / 54,3]. À n = 84, un nul peut
  monter plus haut que le réel — la cascade ne sépare pas
  seule ici, et elle sépare à l'envers.
- **F1/F2 après seuil (descriptif).** Réel : F1 3,7724,
  F2 8,7736 — les deux montent fortement après le seuil.
  Nul s42 : F1 1,1943, F2 0,8747. Nuls frais : s8881
  0,0527 / 0,0190 (chutent fortement), s8882
  21,9736 / 43,6063 (montent très fortement). Ces ratios
  sont descriptifs ; ils ne décident pas — et leur
  dispersion entre les trois nuls (0,05 à 21,97 pour F1)
  dit qu'ils ne portent pas d'information stable ici.
- **Falsification (disponible, n = 84 ≥ 75) :** réel
  1,090427 contre nul 1,053223 (écart +0,0372) ; s8881
  1,116066 ; s8882 0,98497. Le réel est dans l'étendue des
  nuls (0,9850 à 1,1161) — descriptif, ne décide pas.
- **Régime : `saturation` pour les 4 runs** — descriptif,
  pas un verdict.

## 8.88.6 — Tests directs en appui (ne décident pas)

Script `direct_tests_888.py`, sur les CSV de flux du
chantier (réel + nul graine 42), 11 flux.

1. **Test informatif (correction §8.70, appliquée ici) :**
   corrélation de Spearman de chaque flux avec le pas (ordre
   KRAS), réel vs nul : |ρ| moyen réel **0,179** contre nul
   **0,076** ; **Δρ médian +0,191 ; Δρ positifs 9/11** —
   entre le §8.85 (+0,088, 8/12) et le §8.79 (+0,337, 11/11).
   C'est le test qui porte l'information d'ordre — et ici il
   est positif.
2. d de Cohen marginal des 11 flux (réel vs nul) : **d =
   0,0000 pour les 11 gènes** (moyenne des |d| : 3,24×10⁻¹⁷,
   maximum 9,81×10⁻¹⁷) — attendu vacueux par construction :
   le nul est une permutation des lignes, chaque flux garde
   exactement ses 84 valeurs. Rapporté tel quel : il valide
   la construction du nul (marginales préservées exactement),
   il ne mesure pas la séparation.

| Gène | d de Cohen | ρ réel | ρ nul | Δρ |
|---|---|---|---|---|
| PGC | −0,0000 | +0,006 | +0,015 | −0,009 |
| REG4 | +0,0000 | +0,404 | +0,093 | **+0,311** |
| CLDN18 | +0,0000 | +0,158 | +0,093 | **+0,066** |
| MUC17 | +0,0000 | +0,291 | +0,006 | **+0,285** |
| CR2 | +0,0000 | +0,121 | −0,173 | **+0,293** |
| KRT20 | +0,0000 | +0,224 | −0,051 | **+0,275** |
| MUC2 | +0,0000 | +0,176 | +0,027 | **+0,149** |
| GSTM1 | −0,0000 | −0,113 | −0,071 | −0,042 |
| CEACAM5 | +0,0000 | +0,166 | −0,128 | **+0,295** |
| CLCA1 | +0,0000 | +0,306 | +0,115 | **+0,191** |
| MUC16 | +0,0000 | +0,003 | −0,068 | **+0,072** |

Lecture descriptive : le plus fort ρ réel est REG4
(+0,404), suivi de CLCA1 (+0,306) et MUC17 (+0,291) ;
les seuls flux descendants avec KRAS sont GSTM1 (−0,113)
et, marginalement, PGC et MUC16 plats (+0,006, +0,003).
**Divergence à consigner : `maxsep` échoue (−0,0239)
alors que le signal d'ordre direct est positif (Δρ médian
+0,191, |ρ| réel 0,179 contre |ρ| nul 0,076).** C'est le
miroir exact du §8.85, où `maxsep` passait (+0,0884)
alors que le signal d'ordre direct était faible (Δρ médian
+0,088, |ρ| réel 0,124 ≈ |ρ| nul 0,131). Sur ces deux
paires d'organoïdes, `maxsep` et l'ordre par flux se
découplent dans les deux sens — et c'est dit tel quel,
sans être élucidé sans preuve. Aucun de ces tests ne change
le verdict du §8.

### 8.88.6b — Annexe descriptive pré-enregistrée : PDAC seul (ne décide rien, aucun run)

Protocole §10.3 : Spearman de chaque flux contre le rang
KRAS au sein des seules lignées `CAS-DAC-*` (n = 75), réel
seulement, sur les FPKM de la matrice détenue
(`annexe_pdac_seul_888.json`).

| Gène | ρ PDAC-seul | Gène | ρ PDAC-seul |
|---|---|---|---|
| PGC | −0,130 | CR2 | +0,129 |
| REG4 | +0,397 | KRT20 | +0,238 |
| CLDN18 | +0,082 | MUC2 | +0,057 |
| MUC17 | +0,236 | GSTM1 | −0,111 |
| CEACAM5 | +0,071 | CLCA1 | +0,297 |
| MUC16 | −0,023 | | |

**Médiane +0,082 ; 8/11 positifs ; |ρ| moyen 0,161.**
Le signal d'ordre survit sans les 9 lignées non-PDAC
(médiane ρ réel sur les 84 : +0,166 ; 9/11 Δρ positifs),
mais affaibli : PGC passe de +0,006 à −0,130, MUC16 de
+0,003 à −0,023, et la médiane est divisée par deux. La
mixité histologique (9/84 non-PDAC) ne porte donc pas le
signal d'ordre — elle l'accompagne — et elle ne porte pas
non plus l'échec `maxsep` : l'échec est celui de la paire
sur les 84 PDPCOs, et l'annexe ne le change pas. Aucune
autre découpe histologique n'a été calculée.

## 8.88.7 — Comparaison descriptive avec le §8.86 : même matrice, un arrêt levé, un verdict nouveau

Le §8.86 et la présente section portent sur la **même
matrice** de GSE194249, mais ne mesurent pas la même chose
— et le §8.86 n'a rien mesuré du tout sur cette cohorte :

| | §8.86 | §8.88 (cette section) |
|---|---|---|
| Objet | Porte de construction « 12 gènes v4 présents » | Rupture multi-flux (11 flux, ordre KRAS) |
| Résultat | ARRÊT — DPCR1 absent, aucun CSV, aucun run | `d_maxsep = −0,0239` (réel 0,2306, nul 0,2545), NON |
| Flux | DPCR1 exigé au symbole exact | 11 flux, DPCR1 absent (dérogation gelée) |

Aucune des deux lectures ne valide l'autre : un arrêt de
construction ne prédit pas le verdict d'une paire, et un
verdict de paire ne rouvre pas l'arrêt — le §8.86 reste vrai
sous son protocole (symbole exact, aucun mappage), et le
§8.88 est vrai sous le sien (dérogation à 11 flux
pré-enregistrée, go du 21 nov. 10h07). Le fait que le signal
d'ordre direct soit positif (Δρ médian +0,191) ne diminue
ni n'augmente le verdict : le critère gelé est `d_maxsep`,
et il est négatif. Cette distinction est écrite ici pour
qu'aucune lecture future ne confonde l'arrêt §8.86 avec un
échec de la cohorte, ni le verdict §8.88 avec une révision
du §8.86.

## 8.88.8 — Ce que le verdict dit, et ce qu'il ne dit pas

Il dit que `maxsep` ne sépare pas le réel du nul sur une
quinzième cohorte indépendante — la deuxième cohorte
d'organoïdes, et la première où le nul graine 42 dépasse le
réel — avec un `maxsep` réel au milieu de trois tirages de
nul, donc un échec confirmé sur trois tirages, pas un échec
de justesse. Il dit aussi que le découplage entre `maxsep`
et l'ordre par flux, déjà vu au §8.85 dans un sens, se
produit ici dans l'autre sens : ordre positif, `maxsep`
négatif — une question ouverte nouvelle sur ce que `maxsep`
mesure au juste quand les deux divergent. Il dit enfin que
la dérogation à 11 flux fonctionne comme construction (les
11 gènes sont là, 84/84 cas complets, 4/4 runs exit 0) :
l'échec est un verdict de mesure, pas un arrêt de
construction. Il ne dit pas que `maxsep` est invalidé en
général, ni que l'adoption pleine est remise en cause par
ce chantier seul (elle a été décidée par Zackary, et cette
section est la vérification a posteriori qu'elle prévoyait
— elle la met en tension, elle ne la tranche pas), ni que
la rupture multi-flux n'existe pas dans les organoïdes
(GDC, §8.85, passe avec 12 flux). Il ne dit rien de
clinique.

## 8.88.9 — Pistes ouvertes

| Pistes ouvertes | Oui, une de plus | (a) La confirmation indépendante C3 est close depuis le §8.71 — cette quinzième paire est une consolidation supplémentaire manquée, pas une condition ; (b) la candidate C1 (Chen et al. 2025, 46 PDO × 63 AUC, supplément MOESM13 SHA vérifié `0e009cd5…`) reste la piste suivante pour un lot drogue v6.2 (cible Gemcitabine, 62 contrôles) — elle ne peut pas devenir une paire A2 ; (c) la suite (d2) du §8.86.4 — re-dérivation de l'expression de GSE194249 depuis les lectures brutes (SRA) avec une annotation actuelle — reste possible, sous son propre protocole : elle dirait si DPCR1/MUCL3 est mesurable dans les lectures brutes et si une paire à 12 flux y séparerait ; (d) la fragilité du nul à petit n est désormais mesurée sur 3 tirages ici aussi (0,1789 / 0,1952 / 0,2545, étendue 0,0756) — mais à n = 84, pas à petit n : la question ouverte devient celle de l'étendue nulle à n = 84, et du plancher 0,07 face à une étendue nulle de 0,0756 ; (e) la divergence `maxsep` échoue / ordre direct positif (Δρ médian +0,191, 9/11), miroir du §8.85, est une question ouverte nouvelle : sur quelles paires la rupture multi-flux existe-t-elle sans gradient monotone par flux, et sur quelles paires le gradient existe-t-il sans rupture — aucune décomposition ne tranche ici ; (f) la cascade du nul qui dépasse celle du réel (58–83 % contre 26–46 %) est un fait nouveau dans le compte A2 : à suivre sur les prochaines paires, si un nul peut monter plus haut que le réel, la cascade seule ne peut plus être lue comme un signal. |

## 8.88.10 — Annexe : provenance condensée et SHAs

- **Série :** GSE194249, Shi et al., Nat. Commun. 2022,
  13:2169, DOI 10.1038/s41467-022-29857-6. GEO
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE194249
  (page directe bloquée par reCAPTCHA le 21 nov. 2026 ;
  métadonnées via E-utilities, réponse conservée
  `gse194249_esummary_886.json`, SHA
  `73934e46a717a5db1ed8cd8e1c4349435683a0eed1dda85fe7b097ec448f460e`).
  Plateforme GPL31265, dépôt 2022/02/23, *Homo sapiens*.
- **Fichier :** `data/GSE194249_PDPCOs_FPKM.txt.gz`, 4 927 876 o,
  SHA `479517fbed1d8f5bb9d141b6b932b6ab56ba2ba72d4394d13aea2a3da0a50f27`,
  gzip intègre ; 15 610 lignes, 88 colonnes ; mise en page (A).
  URL : `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194249/suppl/GSE194249_PDPCOs_FPKM.txt.gz`.
  Reçu `download_gse194249_886_receipt.json`, SHA
  `fd9bd625a3869086d06b11bb4896b5e5de7f05da91bf5867bca8d1bf83a016ea`.
- **Comptages vérifiés deux fois, avant le gel :** 87 colonnes
  = 84 PDPCOs + 3 `NPC-*` ; 15 609 lignes de gènes ; 0 symbole
  dupliqué ; 11/11 gènes v4 retenus présents une fois chacun ;
  KRAS 1 ; **DPCR1 : 0 occurrence (exact, insensible à la
  casse, fichier entier) ; MUCL3 : 0.** KRAS FPKM min 3,1647 /
  médiane 13,2894 / max 24,9045.
- **Pipeline :** v6.2, SHA
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
  vérifié avant et après les lots.
- **Protocole gelé :** `PROTOCOL_gse194249_11flux_888.md`, SHA
  `f5eb1f952f562499e6ff31036b684cb75d094a2843a17a067acf27ca7c763e02`.
- **Provenance complète :** `PROVENANCE_888.md`.
- **CSV de flux :** réel SHA
  `7799a62a6c1145b728e60a2d1126a93b86c28123744c0dc904e454c35ae9aeda` ;
  nul (graine 42) SHA
  `2f633871d068ceaa7152f10d1190ecb7ca4a58eef0d3e4cfb3a9ad322db44569` ;
  nul frais s8881 SHA
  `f95b7cc4add9f23963d476a939ee9b66317f720eaa12f92e331c184a44388f49` ;
  nul frais s8882 SHA
  `78b1f280d8409b04fe92f7509c8291c718c3acb634c73a61f6b5da2fa4829950`.
- **Runs :** `results_fast_v62_888_gse194249`,
  `results_fast_v62_888_gse194249_nul`,
  `results_fast_v62_888_gse194249_nul_s8881`,
  `results_fast_v62_888_gse194249_nul_s8882`, 4/4 exit 0,
  FIN 21 nov. 2026 15h23:29Z (paire) et 15h36:25Z (frais).
  Extraction `extract_888.json` / `.csv` ; vérification
  `maxsep_888_verify.json` (4/4, écart max 0,0, verdict OK) ;
  tests directs `direct_tests_888.json` ; annexe PDAC-seul
  `annexe_pdac_seul_888.json`.
- **Scripts :** `build_fluxes_888.py` (SHA
  `f598c4b4…5e70`), `extract_888.py` (SHA `3dc9ff8b…6681d`),
  `verify_888.py` (SHA `689f0463…6f7`), `direct_tests_888.py`
  (SHA `ec93dcfd…6a39`) — originaux §8.86 intacts.
- **Verdict :** NON, `d_maxsep = −0,0239`
  (0,23059240234506262 − 0,2545160157551329) ; nuls frais
  +0,0517 / +0,0354 (min / max, médiane +0,0354). A2 :
  **10/15, 12/15 positifs, LOO 9/14.** C3 reste levée.

— Fin de la §8.88. —

---

## 8.88.11 — Note de fin de chantier (pour le coordinateur)

- Livre blanc NON édité, PDF NON régénéré, rien poussé sur
  GitHub (convention des chantiers ; fusion par le
  coordinateur).
- Titre à normaliser à la fusion : « ### 8.88 GSE194249 à 11
  flux : quinzième paire NON — `maxsep` ne sépare pas, le
  réel est dans la distribution des nuls (21 novembre 2026) ».
- Entrée de journal à ajouter : §8.88, protocole gelé
  ~10h10 EST (go 10h07), 4/4 runs exit 0, NON (−0,0239 ;
  nuls frais +0,0517 / +0,0354), A2 10/15.
