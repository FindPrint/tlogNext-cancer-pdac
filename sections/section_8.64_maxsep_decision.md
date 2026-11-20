# §8.64 — Adoption de `maxsep` : dossier de décision — adoption provisoire confirmée, comme convention d'affichage

## Verdict d'abord

**ADOPTER SOUS CONDITION — recommandation du §8.59 CONFIRMÉE par une
troisième lecture indépendante, sans aucun écart.**

| Porte (PROTOCOL_maxsep_decision_864.md §4) | Exigé | Re-vérifié 20 nov. 2026 (§8.64) | §8.59 | Écart | Sort |
|---|---|---|---|---|---|
| D1 — re-confirmation de la suffisance (§8.56 A1–A3) | A1 ≥ 30/48, A2 ≥ 6/8 et ≥ 7/8 positifs, A3 HP35 ≥ 0,30 | **A1 37/48, A2 6/8 (7/8 positifs), A3 +1,6512** | identique | **0** | **PASSE** |
| D2 — exactitude de la re-vérification | 120/120 à 0,0 exact + recoupements à 1e-9 + SHA inchangés | **120/120, écart max 0,0, 0 recoupement en écart, 5 SHA inchangés** | identique | **0** | **PASSE** |
| D3 — robustesse à une paire (leave-one-out) | Retirer n'importe quelle paire : V1 ≥ 6/7, V2 ≥ 30/47 | **V1 ÉCHOUE : retirer n'importe laquelle des 6 paires passantes donne 5/7 ; V2 passe (pire 36/47)** | identique | **0** | **ÉCHOUE** |
| D4 — robustesse d'échelle (plancher équivalent-sep) | A2 tient au plancher `0,07·(1+m_R)(1+m_N)` | **5/8 — ICGC tombe (0,0970 < 0,1292)** | identique | **0** | **ÉCHOUE** |
| D5 — stabilité des classes | 0 changement de classe vs §8.56 ; 0 changement de signe `maxsep` vs `sep` | **0 et 0, sur les 60 paires** | identique | **0** | **PASSE** |

Règle de verdict gelée avant tout calcul (protocole §4) : pleine adoption
si et seulement si D1 ∧ D2 ∧ D3 ∧ D4 ∧ D5 ; adoption sous condition si
D1 ∧ D2 ∧ D5 passent mais D3 ou D4 échoue ; non-adoption si D1, D2 ou D5
échoue. **D3 et D4 échouent, D1, D2 et D5 passent — exactement comme au
§8.59, sans un seul chiffre qui bouge : la recommandation est donc
ADOPTER SOUS CONDITION, confirmée.** La décision finale revient à
Zackary ; ce chantier recommande, il n'adopte pas. Aucune v6.5 n'est
créée, aucun code n'est modifié : l'adoption, si elle est décidée, est
une décision d'AFFICHAGE sur la v6.2 existante, dont la forme exacte
est figée au §8.64.6 ci-dessous, et la v6.2 reste la version de travail.

**Ce que ce chantier ajoute au §8.59.** Le §8.59 a tranché l'adoption
comme question ; le §8.64 en fait le dossier de décision : (a) une
troisième lecture des sorties détenues, par un chemin de code distinct
des deux lectures du §8.59, qui reproduit chaque chiffre à l'identique
— 540 valeurs recoupées (60 paires × 9 champs) à 0,0 exact contre la
table §8.59, 0 écart ; (b) la convention d'affichage écrite en toutes
lettres — score principal, score secondaire, compagnon borné, mention
de fragilité, champ d'application aux sections futures — prête à
appliquer dès le go de Zackary, sans rien à re-trancher ; (c) la
confirmation que rien n'a bougé entre le §8.56, le §8.59 et la présente
re-vérification : le dossier est stable, c'est le verdict d'adoption
qui est fragile, pas les chiffres — et cette stabilité même est
désormais vérifiée trois fois.

Protocole gelé : `PROTOCOL_maxsep_decision_864.md` (20 nov. 2026,
SHA `69c40d73…4ae8`). Barres écrites AVANT toute extraction du
présent chantier (§4 du protocole) ; aucune repondération, aucun
nouveau terme, aucune redéfinition du plancher après avoir vu les
chiffres. Les nombres du §8.59 étaient la motivation, pas le verdict :
le verdict repose sur la re-vérification ci-dessous.

## 8.64.1 — Les cinq portes, et leur sort

| Porte | Exigé | `maxsep` seul (re-vérifié) | `sep` seul (rappel, re-vérifié) | Ancien MC (rappel) |
|---|---|---|---|---|
| D1 — A1 rotations | ≥ 30/48 | **37/48** (somme +17,3623, moyenne +0,3617) | 35/48 (somme +7,9306) | 12/48 (somme +0,7295) |
| D1 — A2 principales | ≥ 6/8 et ≥ 7/8 positifs | **6/8, 7/8 positifs** (somme +2,8043) | 5/8, 7/8 positifs (somme +1,1939) | 1/8, 7/8 positifs (somme +0,3485) |
| D1 — A3 HP35 | ≥ 0,30 | **+1,6512** | +0,5316 | +0,1950 |
| D2 — exactitude | 120/120 à 0,0 | **120/120, écart max 0,0** | idem (même relecture) | recoupements 0 écart |
| D3 — LOO V1 | ≥ 6/7 après tout retrait | **5/7 après retrait de chaque paire passante** | — (non testé, porte sur `maxsep`) | — |
| D3 — LOO V2 | ≥ 30/47 après tout retrait | **36/47 au pire** | — | — |
| D4 — A2 au plancher équivalent | ≥ 6/8 et ≥ 7/8 positifs | **5/8** | 5/8 (par identité) | — |
| D5a — classes vs §8.56 | 0 changement / 60 | **0** | — | — |
| D5b — signes `maxsep` vs `sep` | 0 changement / 60 | **0** | — | — |

## 8.64.2 — Méthode de re-vérification (60 paires, JSON v6.2 existants, aucun run)

Script propre du chantier, `verify_maxsep_decision_864.py` : 60/60
paires lues, 0 manquante, 0 version non attendue (v6.2 partout sauf
CLDN18 en v6.1, comme en §8.49/§8.52/§8.56/§8.59) ; chemin de code
distinct des deux scripts du §8.59 — descente récursive générique à la
recherche de `best_config`, re-écrite, listes de dossiers reconstruites
depuis le manifest §8.44 et les listes figées du protocole §8.59,
comptages re-écrits. **Troisième lecture des sorties détenues** :
extracteur §8.59, vérifieur §8.59, présent chantier — trois parcours
indépendants, un seul jeu de chiffres.

**D2a — exactitude :** le présent calcul reproduit `sep` et `maxsep`
à **0,0 exact** sur les **120/120** runs contre la table §8.59
(540 valeurs : 60 paires × 9 champs, égalité stricte, pas de tolérance).
**D2b — recoupements à 1e-9 :** 0 écart contre
`maxsep_adoption_859_table.json`, 0 écart contre
`sep_maxsep_856_table.json`, 0 écart de l'ancien MC contre §8.44
(rotations) et phase 2 v6.2 (principales), 0 écart de `d_maxsep`
contre §8.44. **D2d — SHA revérifiés après travaux, inchangés :**
v6.2 `f07567c4…c3abf`, v6.1 `2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`,
v6.3 `552e7359…44ffb`, v6.4 `9ed728da…9ea3d`.

**Aucun run du pipeline n'a été nécessaire** (protocole §5) : les 120
`master_results.json` étaient présents et valides. Aucun run lancé,
aucun exit code à noter — la règle de rattrapage (systemd-run,
jamais nohup) n'a pas eu à s'appliquer. La re-vérification est
hors-ligne, comme aux §8.56 et §8.59.

Définitions (reprises du §8.59, inchangées) : `maxsep` =
`best_config.metrics.max_separation`, |d de Cohen| maximal du scan
de seuil, [0, ∞[ ; `sep` = `maxsep/(1+maxsep)`, [0, 1[ ; les deux
sont lus sur le best_config ANCIEN (sélection par l'ancien
composite) : la question porte sur le SCORE AFFICHÉ, pas sur la
sélection du tirage. Seuil MC, cascade, S_sep, Delta, L7a inchangés
par construction, quelle que soit la décision d'adoption.

## 8.64.3 — Re-vérification chiffre par chiffre : 0 écart contre le §8.59

Chaque chiffre du §8.59 a été re-calculé de zéro et comparé. Le
tableau ci-dessous est le compte rendu exhaustif de cette comparaison ;
il n'y a aucun écart à cacher, donc aucun à consigner comme écart.

| Chiffre du §8.59 | Valeur §8.59 | Valeur re-vérifiée (§8.64) | Écart |
|---|---|---|---|
| A1 rotations `maxsep` | 37/48, somme +17,3623, moyenne +0,3617 | 37/48, somme +17,3623, moyenne +0,3617 | 0 |
| A1 rotations `sep` | 35/48, somme +7,9306 | 35/48, somme +7,9306 | 0 |
| A2 principales `maxsep` | 6/8, 7/8 positifs, somme +2,8043 | 6/8, 7/8 positifs, somme +2,8043 | 0 |
| A2 principales `sep` | 5/8, 7/8 positifs, somme +1,1939 | 5/8, 7/8 positifs, somme +1,1939 | 0 |
| A3 HP35 `maxsep` | +1,6512 | +1,6512 (+1,6511952353773127) | 0 |
| A3 HP35 `sep` / ancien MC | +0,5316 / +0,1950 | +0,5316 / +0,1950 (+0,1949845784557579) | 0 |
| Re-vérification 120/120 | 120/120, écart max 0,0 | 120/120, écart max 0,0 exact | 0 |
| Multisets | égaux | égaux | 0 |
| Recoupements 1e-9 | 0 écart (60 paires × 9 champs) | 0 écart (60 paires × 9 champs) | 0 |
| D3 LOO V1 | 5/7 après retrait de chaque paire passante | 5/7, les 6 suppressions passantes | 0 |
| D3 LOO V2 pire cas | 36/47 (retirer DEPMAPROT_CRKL) | 36/47 (retirer DEPMAPROT_CRKL) | 0 |
| D4 A2 plancher équivalent | 5/8, ICGC tombe | 5/8, ICGC tombe (0,0970 < 0,1292) | 0 |
| D5a classes vs §8.56 | 0 changement / 60 | 0 changement / 60 | 0 |
| D5b signes `maxsep` vs `sep` | 0 changement / 60 | 0 changement / 60 | 0 |
| S7 ancien → `maxsep` | 30 changements, 0 perte (5/8 + 25/48) | 30 changements, 0 perte (5 + 25) | 0 |
| Ancien MC | 12/48, 1/8, sommes +0,7295 / +0,3485 | 12/48, 1/8, sommes +0,7295 / +0,3485 | 0 |
| Marges charnières | ICGC +0,0270 / −0,0322 ; MYH9 +0,0213 ; MUC16 +0,0003 | ICGC +0,0270 / −0,0322 ; MYH9 +0,0213 ; MUC16 +0,0003 (+0,00031206232338357176) | 0 |
| SHA des codes | v6.2 `f07567c4…c3abf`, v6.1 `2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`, v6.3 `552e7359…44ffb`, v6.4 `9ed728da…9ea3d` | identiques, revérifiés après travaux | 0 |

**Lecture de ce tableau.** Zéro écart ne veut pas dire « preuve » :
trois lectures du même jeu de JSON ne peuvent que confirmer la
relecture, pas la mesure — la porte D2 reste le seul contrôle
d'exactitude, sur 120 runs relus trois fois. Mais zéro écart veut
dire ceci : la recommandation du §8.59 ne repose sur aucune erreur
de lecture, aucune valeur recopiée, aucun comptage fragile. Ce qui
échoue (D3, D4) échoue sur des chiffres exacts, et ce qui passe
(D1, D2, D5) passe sur des chiffres exacts. La fragilité est une
propriété du dossier, pas un artefact de calcul — c'est précisément
pour cela qu'elle est confirmée plutôt que dissoute par la
re-vérification.

## 8.64.4 — D3 et D4 confirmés : l'échec est exact, pas approximatif

**D3 — leave-one-out exhaustif (V1, 8 suppressions ; V2, 48
suppressions), même règle de comptage, même plancher 0,07 :**

| Ensemble | Retrait testé | Résultat | Porte |
|---|---|---|---|
| V1 (8 paires) | Retirer GSE71729 (échec) ou GSE62452 (négative) | **6/7** — passe | — |
| V1 | Retirer HP35, TCGA v4, ICGC, IMMUNE_TCGA, PARP_TCGA ou DEPMAP (les 6 passantes) | **5/7** — échoue | **D3 ÉCHOUE** |
| V2 (48 paires) | Pire cas : retirer DEPMAPROT_CRKL | **36/47** — passe | D3 (V2) passe |
| V2 | Toutes les autres suppressions | 36 ou 37/47 — passe | D3 (V2) passe |

D3 exigeait ≥ 6/7 après tout retrait en V1, ce qui équivaut à
exiger 7/8 avant retrait : avec 6/8, CHAQUE paire passante est
charnière. La fragilité est confirmée à l'identique : elle tient à
six paires à la fois, c'est-à-dire à l'ensemble des paires qui
passent. En V2, la marge est confortable (37/48, pire cas 36/47) :
la fragilité est concentrée aux principales, pas aux rotations.

**D4 — plancher à échelle égale (A2) :**

| Paire (V1) | d_maxsep | Plancher équivalent-sep | d_sep | Passe au plancher équivalent ? |
|---|---|---|---|---|
| HP35 | +1,6512 | 0,2174 | +0,5316 | oui |
| TCGA v4 | +0,2928 | 0,1197 | +0,1712 | oui |
| GSE71729 | +0,0402 | 0,1075 | +0,0262 | non |
| GSE62452 | −0,0036 | 0,1205 | −0,0021 | non |
| ICGC | +0,0970 | 0,1292 | +0,0525 | **non — c'est la paire qui fait échouer D4** |
| IMMUNE_TCGA | +0,3675 | 0,1247 | +0,2063 | oui |
| PARP_TCGA | +0,1688 | 0,1148 | +0,1029 | oui |
| DEPMAP | +0,1904 | 0,1266 | +0,1052 | oui |

**Total : 5/8** (7/8 positifs) — D4 échoue. Par l'identité du
§8.56.2, c'est exactement le comptage de `sep` (5/8). Aux rotations,
les deux paires qui passent le plancher littéral mais pas le
plancher équivalent sont les mêmes qu'aux §8.56 et §8.59 :
DEPMAPROT_MYH9 (+0,0913 contre 0,1061) et V4ROT_MUC16 (+0,0703
contre 0,1152). Rien d'autre ne change entre les deux échelles.

Marges confirmées : ICGC passe le plancher littéral de +0,0270 mais
échoue au plancher équivalent de −0,0322 ; MYH9 passe le plancher
littéral de +0,0213 ; MUC16 passe le plancher littéral de **+0,0003**
(+0,0703) — la plus petite marge du dossier, inchangée depuis le
§8.56, re-vérifiée deux fois depuis. DEPMAPROT_RAB10 est la prochaine
paire près du plancher (+0,0621, à −0,0079) : elle ne passe ni l'un
ni l'autre plancher, dans aucune des deux échelles.

## 8.64.5 — D5 et S7 : les classes sont stables, et le changement est tout en gain

**D5a :** 0 changement de classe de séparation `maxsep` entre la
re-vérification et les classes publiées au §8.56, sur les 60 paires.
**D5b :** 0 changement de classe de signe entre `d_maxsep` et
`d_sep`, sur les 60 paires — comme l'exige la monotonie, vérifié et
non supposé. Trois lectures, un seul jeu de classes.

**S7 — ancien composite → `maxsep` seul (descriptif) :**

| Ensemble | Ancien MC | `maxsep` seul | Gagnent la classe « sépare » | Perdent la classe | Changements |
|---|---|---|---|---|---|
| V1 (8) | 1/8 | 6/8 | DEPMAP, ICGC, IMMUNE_TCGA, PARP_TCGA, TCGA_v4 (5) | aucune | 5 |
| V2 (48) | 12/48 | 37/48 | 25 paires (liste en table) | aucune | 25 |
| **Total** | **13/56** | **43/56** | **30** | **0** | **30** |

Les 25 gains aux rotations : DEPMAPROT_CRKL, DOCK5, EFR3A, MYH9,
RAB6A, SCAP ; IMMROT_CD19, CD8A, FOXP3, GZMB, IFNG ; PARPROT_ATM,
ATR, BRCA2, CHEK1, CHEK2, FANCD2, POLQ ; V4ROT_CEACAM5, CLCA1,
DPCR1, KRT20, MUC16, MUC2, PGC. **Aucune paire ne perd sa classe
en passant à `maxsep`** : le changement proposé ne dégrade rien de
ce que l'ancien composite séparait déjà. Même au plancher
équivalent-sep, `maxsep` (= `sep`) sépare 35/48 rotations et 5/8
principales, contre 12/48 et 1/8 pour l'ancien composite.

## 8.64.6 — La convention d'affichage : adoption provisoire, en toutes lettres

**Recommandation à Zackary : ADOPTER `maxsep` seul comme score MC
affiché, À TITRE PROVISOIRE, selon la convention ci-dessous — qui est
la forme exacte, figée ici, de l'adoption provisoire du §8.59.8.**
Tant que Zackary n'a pas donné son go explicite après lecture de la
présente section (C1), rien ne change : v6.2 reste la version de
travail, l'ancien MC reste le score affiché avec ses défauts connus
(§8.49.3).

**Convention d'affichage (applicable aux sections FUTURES, à compter
du go ; les sections §8.1–§8.63 gardent leurs valeurs historiques,
avec mention du changement et sa date) :**

1. **Score principal — `maxsep`.** Le score MC AFFICHÉ devient
   `best_config.metrics.max_separation` (le |d de Cohen| maximal du
   scan), à la place de l'ancien composite.
2. **Score secondaire — ancien MC.** L'ancien composite
   (`0.3·s_norm + 0.3·stability + 0.2·robustness + 0.2·sharpness`)
   reste AFFICHÉ EN SECOND, comme score secondaire, partout où
   `maxsep` est affiché comme score principal. Aucune table future
   n'affiche `maxsep` sans son ancien MC en second — c'est la
   nouveauté du présent dossier par rapport au §8.59.8, qui ne
   nommait que le compagnon `sep` : le dossier de décision ajoute
   l'ancien MC comme second, pour que le lecteur voie à chaque table
   ce qui est gagné et ce qui est abandonné.
3. **Compagnon borné — `sep`.** `sep` (= maxsep/(1+maxsep)) est
   affiché EN COMPAGNON borné [0, 1] partout où `maxsep` est affiché,
   pour garder une échelle comparable aux scores publiés.
4. **Plancher publié en unités |d|.** Le plancher 0,07 est publié EN
   UNITÉS |d| à chaque table, avec le rappel que 0,07 en |d| est en
   dessous du « petit » effet de Cohen (0,2).
5. **Mention de fragilité en tête de chaque table.** Chaque table qui
   cite le score porte en tête la mention exacte : « adoption
   provisoire (§8.59, §8.64) — le verdict de suffisance tient à une
   paire aux principales (ICGC) et à l'échelle du plancher ». Pas de
   table qui affiche `maxsep` sans cette mention tant que C3 n'est
   pas levée.
6. **Sélection inchangée.** La sélection du best_config continue
   d'utiliser l'ancien composite. Ce chantier ne propose pas de
   changer la sélection ; la changer demanderait son propre
   protocole et son propre go.
7. **Aucune nouvelle version de code.** Pas de v6.5, pas de
   modification de v6.2. L'adoption est une décision d'affichage
   consignée sur la v6.2 existante.

**Conditions (reprises du §8.59.8, inchangées) :**

- **C1 — Go explicite de Zackary** après lecture de la présente
  section. Sans ce go, rien ne change.
- **C2 — Affichage conjoint et fragilité en tête.** Points 2–5
  ci-dessus, à chaque table.
- **C3 — Levée de la condition par confirmation indépendante.**
  La pleine adoption (sans étiquette « provisoire ») est différée
  jusqu'à ce qu'une confirmation indépendante porte A2 à 7/8 —
  soit une paire principale supplémentaire indépendante qui sépare
  au plancher 0,07 en `maxsep` (ce qui porterait aussi le
  leave-one-out V1 à 6/7 après retrait d'une paire passante),
  soit un lot de paires nouvelles confirmant A2 à ≥ 7/8 — à
  consigner dans une section ultérieure, avec son propre protocole
  gelé. Tant que C3 n'est pas levée, l'adoption reste provisoire.

**Modèle de table future (à titre d'exemple de forme, pas de chiffres
nouveaux) :** en-tête « adoption provisoire (§8.59, §8.64) — le
verdict de suffisance tient à une paire aux principales (ICGC) et à
l'échelle du plancher » ; colonnes : paire | `maxsep` (principal,
|d|, plancher 0,07) | ancien MC (secondaire) | `sep` (compagnon
borné [0, 1]) | sépare (oui/non, au plancher 0,07 en |d|).

**Ce qui est gagné** (si Zackary adopte, même provisoirement) : plus
de saturation artificielle, plus de terme mort, plus de terme
anti-discriminant, plus de malédiction du vainqueur déguisée en
composite — le score est la séparation elle-même, lisible
directement en |d de Cohen| ; et 30 paires gagnent la classe
« sépare », zéro n'en perd — avec, à chaque table, l'ancien MC en
second pour le montrer.

**Ce qui est perdu / ce qui reste fragile** : le plafond [0, 1] et
la comparabilité immédiate avec les scores publiés (MC ancien,
MC_new, MC2, S_sep) — d'où le compagnon `sep` et le second ancien MC
en C2 ; un |d| brut n'a pas d'échelle commune entre études sans son
contexte (n, flux, contrôle) ; DEPMAPROT reste à 6/12 ; et le verdict
de suffisance reste à une paire près (D3) et à une convention
d'échelle près (D4) — d'où l'étiquette « provisoire » en C2 et la
confirmation en C3.

**Ce qui n'est pas prouvé** par cette adoption : que `maxsep`
sépare « le réel du nul » en général — il sépare 37/48 rotations
et 6/8 principales aux barres gelées, avec les fragilités dites,
et 5/12 seulement sur DEPMAPROT. Le verdict porte sur le score,
pas sur l'instrument. Rien de clinique : l'étude porte sur
l'instrument.

## 8.64.7 — Ce que la décision change, et ce qu'elle ne change pas

| Poste | Change ? | Détail |
|---|---|---|
| Score MC affiché, sections futures | **Oui, si go (C1)** | `maxsep` principal, ancien MC secondaire, `sep` compagnon, mention §8.64.6 point 5 |
| Score MC affiché, sections §8.1–§8.63 | Non | Valeurs historiques gardées, avec mention du changement et sa date |
| Sélection du best_config | Non | Ancien composite, lignes 3480–3484 de v6.2 |
| Seuil MC, cascade, S_sep, Delta, L7a | Non | Inchangés par construction |
| Code v6.2 / v6.1 / v6 / v6.3 / v6.4 | Non | Aucune modification, aucune v6.5 |
| Verdicts des §8.34, §8.43, §8.56, §8.59 | Non | Confirmés, pas rouverts ; les §8.56/§8.59 restent les sections de référence pour la suffisance et le premier tranchement |
| Pleine adoption (sans « provisoire ») | Non, différée | Attend C3 : confirmation indépendante portant A2 à 7/8 |

**Suite du dossier, si Zackary donne son go :** le coordinateur gèle
le changement d'affichage, régénère le PDF, pousse sur GitHub (règle
permanente « Toujours github et pdf !!! »), et met à jour les sections
qui citent le MC. **Suite du dossier, si Zackary ne donne pas son go
ou refuse :** le statu quo tient, `maxsep` reste l'indicateur de
référence qu'il est déjà, et la présente section consigne la
recommandation non suivie avec ses chiffres — elle n'est pas effacée.
**Suite du dossier, pour lever C3 :** une section ultérieure, avec son
propre protocole gelé, mesurant une paire principale supplémentaire
indépendante ou un lot de paires nouvelles — pas une relecture : les
relectures sont épuisées comme preuve, trois lectures disent la même
chose, et une quatrième ne dirait rien de plus.

## 8.64.8 — Sensibilités (descriptives, ne décident pas)

- **S1 — sans plancher** : V1 7/8 positifs pour les deux candidats
  (seul GSE62452 négatif, −0,0036 / −0,0021, quasi nul) ; V2 42/48
  positifs pour les deux (négatifs : DEPMAPROT_ACO2, CCND1, MYC,
  UROD, V4ROT_CR2, GSTM1). Identique aux §8.56 et §8.59.
- **S2 — barre A1 à 24/48** (protocoles v6.3/v6.4) : les deux
  candidats la franchissent (35/48 et 37/48) — le verdict ne change
  pas sous l'ancienne barre.
- **S5 — plancher de Cohen 0,20 en |d|** : `maxsep` sépare 3/8
  principales (HP35, TCGA v4, IMMUNE_TCGA) et 33/48 rotations.
  Le plancher 0,07 est laxiste en unités |d| : 0,2 est déjà un
  « petit » effet chez Cohen, et 0,07 est en dessous. Le même
  constat vaut pour A3 : +1,6512 contre une barre de 0,30 calibrée
  pour des scores en [0, 1] — `maxsep` franchit A3 trivialement,
  par l'échelle autant que par le signal. S5 ne décide de rien ;
  elle situe la barre.

## 8.64.9 — Contrôles descriptifs (V3–V5, ne décident pas)

| Paire | Ancien MC (écart) | maxsep (écart) | sep (écart) | Lecture |
|---|---|---|---|---|
| Test A (prolifération) | −0,0948 | **+0,2501** | +0,1567 | Suivent maxsep ; ne ressuscitent pas Test A (verdict NON du §8.34 portait sur la chaîne et MC/Delta) |
| MTAP série PRMT5-flux (§8.43) | +0,0004 | **−0,1036** | −0,0671 | Restent négatifs, cohérent avec le verdict NON du §8.43 |
| MTAP série (§8.31) | −0,1642 | **+0,1957** | +0,1278 | Suivent maxsep ; l'ancien MC était fortement inversé ici |
| V4R_PURITY (artefact §8.31) | +0,1520 | **−0,0670** | −0,0483 | Artefact CORRIGÉ : les deux candidats reprennent le sens de maxsep |

Aucun écart de signe entre `sep` et `maxsep` sur les 60 paires
(D5b). L'adoption ne change aucun de ces verdicts : ils portaient
sur la chaîne, sur MC/Delta, ou sur des tests directs — pas sur le
score MC affiché.

## 8.64.10 — Limites et ce qui reste

- La validation hors-ligne réutilise les JSON v6.2 : elle ne teste
  que la RELECTURE, pas une nouvelle mesure. Trois lectures disent
  la même chose — c'est une garantie d'exactitude, pas une mesure
  nouvelle. La porte D2 est le seul contrôle d'exactitude, sur 120
  runs relus trois fois.
- D3 a été gelée comme exigeant 7/8 en V1 avant retrait : c'est une
  barre d'adoption volontairement plus dure que la barre de
  suffisance (6/8). Elle est justifiée parce qu'adopter change le
  dossier public — mais elle doit être lue comme telle : une barre
  de prudence, pas une propriété mesurée du score.
- D4 équivaut par construction à « `sep` franchit A2 » : son échec
  ne dit rien de nouveau sur `maxsep` que le §8.56 n'ait déjà dit
  sur `sep` — il dit que le verdict de suffisance ne survit pas à
  l'expression du plancher à échelle égale. C'est une limite de la
  CONVENTION (plancher 0,07 littéral), pas une découverte sur les
  données.
- Aucune paire principale supplémentaire n'a été mesurée dans ce
  chantier : C3 attend des données nouvelles, pas une relecture.
  Tant qu'elles n'existent pas, l'adoption reste provisoire — et
  c'est un état stable, pas un état transitoire honteux : le score
  affiché est le meilleur connu, avec sa fragilité dite.
- `sep` seul reste rejeté comme score MC unique (§8.56) — mais il
  demeure le compagnon borné de `maxsep` (convention §8.64.6 point 3),
  avec son échec à A2 consigné.
- La seule nouveauté de forme du présent dossier par rapport au
  §8.59.8 est le point 2 de la convention (ancien MC affiché en
  second) : c'est un ajout d'affichage, pas un nouveau verdict — il
  ne change aucun chiffre, aucune porte, aucune condition C1–C3.
- La question du §8.56.6 (« que voudrait dire adopter `maxsep` »)
  est close telle que posée ici : adopter, provisoirement, selon la
  convention §8.64.6 ; la pleine adoption attend une confirmation
  indépendante. Aucune autre recomposition n'est proposée : cinq
  chantiers (v6.3, v6.4, §8.56, §8.59, §8.64) ont maintenant montré
  que le problème n'était pas le terme annexe — c'était le composite
  lui-même, et que le remplacer se fait avec une marge d'une paire,
  pas avec un triomphe.

## 8.64.11 — Provenance

- Protocole gelé : `PROTOCOL_maxsep_decision_864.md`, SHA-256
  `69c40d73258bab6855fe65c65198fc8ec524f455ac1ff15ef7641d1f578b4ae8`.
- Re-vérification indépendante : `verify_maxsep_decision_864.py`
  (SHA-256
  `0f456b78b0479c5b969d90574cdf7c8756083f9f68c8fbb2ce8c0f0d2fcc24e1`)
  → `maxsep_decision_864_verify.json` (SHA-256
  `0f2e182eb8fed122a81c2eb8960ac977e84248d50803e9f3686893e35b98e799` ;
  120/120 dossiers, écart max 0,0 exact, multisets égaux,
  0 recoupement en écart).
- Section : `section_8.64_maxsep_decision.md` (ce fichier ; SHA noté
  au rapport).
- Références re-vérifiées : `maxsep_adoption_859_table.json` (SHA-256
  `702f166d76351ab62760655bbc35ed48a9cdcaf77002008d5f4ae172814c2c7f`),
  `maxsep_adoption_859_table.csv` (SHA-256
  `c9ac12e4240b215ed54df43a97a55163a94635dae2baaee3919471d482b3bd9b`),
  `sep_maxsep_856_table.json` (SHA-256
  `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`) ;
  protocole §8.59 `PROTOCOL_maxsep_adoption_859.md` (SHA-256
  `efb5da799d245d8e5db570945acc480f1c5bae42d63ed29b7cfeb780610e675b`) ;
  section §8.59 `section_8.59_maxsep_adoption.md` (SHA-256
  `9951d22c1e3de415914f5ed9cf1271972a7e6a17bb5c0489684240177dee36f4`) ;
  protocole §8.56 `PROTOCOL_sep_maxsep_856.md` (SHA-256
  `06e36725eedb3d52b1549290e1e8cccff381650928fbf4e6a28a090aec27fd4e`) ;
  section §8.56 `section_8.56_sep_maxsep.md` (SHA-256
  `9015ab0cf8d4b577a5ba3bd37512032461762f31f9daa177f63ba41120fe9012`).
- Données : JSON v6.2 existants (lots §8.44, phase 2, §8.43, Test A) ;
  CSV inchangés, SHA déjà publiés dans `PROVENANCE_rotations_dedup_844.md`,
  `PROVENANCE_tcga_v4.md`, `PROVENANCE_mtap_prmt5_flux.md`,
  `PROVENANCE_testA_proliferation.md`. Nuls = lignes permutées, graine
  42 — échantillons hypothétiques, pas des mesures. Séries réelles =
  résidus d'expression génique ou de dépendance CRISPR (mesures
  instrumentales transformées). Aucune valeur inventée ; aucune valeur
  recopiée à la main (tables générées depuis
  `maxsep_decision_864_verify.json`, vérifiées paire par paire contre
  `maxsep_adoption_859_table.json` à 0,0 exact et contre
  `sep_maxsep_856_table.json` à 1e-9 ; les valeurs des §8.64.4 et
  §8.64.9 sont lues dans cette sortie, pas recopiées des §8.56/§8.59).
- Livre blanc de référence consulté : `livre-blanc-pdac-v6.md`,
  10 665 lignes, SHA-256
  `ba88761dd160afd360dab3c1fc831c3d2a0db54a729bed0f5bf796dc6882eebf`
  (§8.1–§8.63, état au 20 nov. 2026) — à noter : il diffère de la
  référence donnée dans la mission du présent chantier (10 661 lignes,
  SHA `fe036c92…`, 4 lignes de moins) ; le livre blanc n'a PAS été
  modifié par ce chantier, et l'écart est consigné ici tel que
  constaté, sans explication inventée. Fusion de la présente section
  par le coordinateur.
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`), v6.1 (`2af5e5ce…c1c9`),
  v6 (`bb8bbdba…c0773`), v6.3 (`552e7359…44ffb`), v6.4 (`9ed728da…9ea3d`).
  Aucune nouvelle version construite dans ce chantier — pas de v6.5.
  Aucun run du pipeline lancé dans ce chantier (re-vérification
  hors-ligne, 120 JSON existants, troisième lecture).
  Aucun push GitHub, aucune Release dans ce chantier.
