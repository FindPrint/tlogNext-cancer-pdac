# §8.59 — Trancher l'adoption de `maxsep` seul comme score MC

## Verdict d'abord

**ADOPTER SOUS CONDITION — adoption PROVISOIRE, pas pleine.**

| Porte (PROTOCOL_maxsep_adoption_859.md §4) | Exigé | Re-vérifié 20 nov. 2026 | Sort |
|---|---|---|---|
| D1 — re-confirmation de la suffisance (§8.56 A1–A3) | A1 ≥ 30/48, A2 ≥ 6/8 et ≥ 7/8 positifs, A3 HP35 ≥ 0,30 | **A1 37/48, A2 6/8 (7/8 positifs), A3 +1,6512** | **PASSE** |
| D2 — exactitude de la re-vérification | 120/120 à 0,0 exact + recoupements à 1e-9 + SHA inchangés | **120/120, écart max 0,0, multisets égaux, 0 recoupement en écart, 5 SHA inchangés** | **PASSE** |
| D3 — robustesse à une paire (leave-one-out) | Retirer n'importe quelle paire : V1 ≥ 6/7, V2 ≥ 30/47 | **V1 ÉCHOUE : retirer n'importe laquelle des 6 paires passantes donne 5/7 ; V2 passe (pire 36/47)** | **ÉCHOUE** |
| D4 — robustesse d'échelle (plancher équivalent-sep) | A2 tient au plancher `0,07·(1+m_R)(1+m_N)` | **5/8 — ICGC tombe (0,0970 < 0,1292)** | **ÉCHOUE** |
| D5 — stabilité des classes | 0 changement de classe vs §8.56 ; 0 changement de signe `maxsep` vs `sep` | **0 et 0, sur les 60 paires** | **PASSE** |

Règle de verdict gelée avant tout calcul : pleine adoption si et
seulement si D1 ∧ D2 ∧ D3 ∧ D4 ∧ D5 ; adoption sous condition si
D1 ∧ D2 ∧ D5 passent mais D3 ou D4 échoue ; non-adoption si D1, D2
ou D5 échoue. **D3 et D4 échouent, D1, D2 et D5 passent : la
recommandation est donc ADOPTER SOUS CONDITION**, dans les termes
précis du §8.59.8. La décision finale revient à Zackary ; ce
chantier recommande, il n'adopte pas. Aucune v6.5 n'est créée, aucun
code n'est modifié : l'adoption, si elle est décidée, est une
décision d'AFFICHAGE sur la v6.2 existante, et la v6.2 reste la
version de travail.

**Pourquoi pas « ne pas adopter ».** Les deux portes qui échouent
mesurent la fragilité du verdict de suffisance, pas la qualité du
score contre le statu quo. Le changement proposé est monotone dans
le bon sens : entre l'ancien composite et `maxsep` seul, **30 paires
changent de classe de séparation, toutes dans le sens du gain
(5/8 aux principales, 25/48 aux rotations), zéro dans le sens de la
perte** (§8.59.5, S7). L'ancien MC sépare 12/48 rotations et 1/8
principales ; `maxsep` 37/48 et 6/8. Garder l'ancien composite comme
score affiché, en sachant cela, serait garder un score dont on sait
qu'il sépare trois fois moins bien. La condition ne porte donc pas
sur « `maxsep` vaut-il mieux que l'ancien composite » — c'est
tranché, oui, et sans aucune perte — elle porte sur « le verdict
"il suffit" est-il assez solide pour une adoption pleine et
définitive » — et là, la réponse est non : il tient à une paire
(ICGC) et à l'échelle du plancher.

**Pourquoi pas « adopter » plainement.** Le verdict de suffisance
tient à une seule paire aux principales : retirer ICGC, ou HP35, ou
TCGA v4, ou IMMUNE_TCGA, ou PARP_TCGA, ou DEPMAP — n'importe
laquelle des six paires passantes — et A2 tombe à 5/7 (D3). Et à
échelle de plancher égale à celle de `sep`, A2 tombe à 5/8 (D4) :
`maxsep` ne passe A2 que parce que 0,07 en |d| est plus facile à
franchir que 0,07 en unités `sep`. Une adoption pleine et définitive
sur une marge d'une paire serait une décision dont le dossier ne
porte pas le poids. L'adoption provisoire dit exactement ce que les
chiffres permettent de dire : on affiche dès maintenant le meilleur
score connu, avec son compagnon borné et sa fragilité en tête de
chaque table, et on lève la condition par une confirmation
indépendante (§8.59.8, C3).

**Fragilité, dite en tête et pas en note de bas de page.** Le plancher
0,07 en |d| est en dessous du « petit » effet de Cohen (0,2) : au
plancher 0,20, `maxsep` ne sépare plus que 3/8 principales (S5).
`maxsep` passe A2 exactement au minimum (6/8), comme au §8.56, et
MUC16 passe A1 de 0,0003 (+0,0703). Rien de tout cela n'a bougé
entre le §8.56 et la re-vérification — c'est précisément pour cela
que les portes D3 et D4 ont été gelées : elles testent ce que le
§8.56 avait nommé sans trancher.

Protocole gelé : `PROTOCOL_maxsep_adoption_859.md` (20 nov. 2026,
SHA `efb5da79…675b`). Barres écrites AVANT toute extraction du
présent chantier (§4 du protocole) ; aucune repondération, aucun
nouveau terme, aucune redéfinition du plancher après avoir vu les
chiffres. Les nombres du §8.56 étaient la motivation, pas le
verdict : le verdict repose sur la re-vérification ci-dessous.

## 8.59.1 — Les cinq portes, et leur sort

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

## 8.59.2 — Méthode de re-vérification (60 paires, JSON v6.2 existants, aucun run)

Extracteur propre du chantier, `extract_maxsep_adoption_859.py` :
60/60 paires lues, 0 manquante, 0 version non attendue (v6.2
partout sauf CLDN18 en v6.1, comme en §8.49/§8.52/§8.56) ; ancien
MC relu sans écart vs §8.44 (rotations) et phase 2 v6.2
(principales), tol. 1e-9 ; `sep`/`maxsep`/ancien MC recoupés sans
écart vs `sep_maxsep_856_table.json`, tol. 1e-9 — **0 écart sur les
60 paires × 9 champs**. Second calcul indépendant
(`verify_maxsep_adoption_859.py`, parcours récursif générique des
JSON, sans réutiliser les fonctions de l'extracteur) : **120/120
dossiers relus, écart max 0,0 exact, multisets égaux, verdict OK**.
SHA revérifiés après travaux, inchangés : v6.2 `f07567c4…c3abf`,
v6.1 `2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`, v6.3 `552e7359…44ffb`,
v6.4 `9ed728da…9ea3d`.

**Aucun run du pipeline n'a été nécessaire** (protocole §5) : les 120
`master_results.json` étaient présents et valides. Aucun run lancé,
aucun exit code à noter — la règle de rattrapage (systemd-run,
jamais nohup) n'a pas eu à s'appliquer. La re-vérification est
hors-ligne, comme au §8.56.

Définitions (reprises du §8.56, inchangées) : `maxsep` =
`best_config.metrics.max_separation`, |d de Cohen| maximal du scan
de seuil, [0, ∞[ ; `sep` = `maxsep/(1+maxsep)`, [0, 1[ ; les deux
sont lus sur le best_config ANCIEN (sélection par l'ancien
composite) : la question porte sur le SCORE AFFICHÉ, pas sur la
sélection du tirage. Seuil MC, cascade, S_sep, Delta, L7a inchangés
par construction, quelle que soit la décision d'adoption.

Note sur la « classe » (§1.1 du protocole, gelé) : la mission
demandait de vérifier qu'aucune paire ne change de classe « entre le
score v6.2 et un score maxsep-seul ». Pris littéralement (ancien
composite contre `maxsep` seul), ce contrôle est impossible par
construction — 30 paires changent de classe, et c'est l'objet même
de l'adoption (§8.59.5, S7). Le contrôle gelé est donc sa forme
vérifiable : D5a (aucun changement de classe entre la
re-vérification et le §8.56 publié) et D5b (aucun changement de
signe entre `d_maxsep` et `d_sep`). Les 30 changements
ancien → `maxsep` sont comptés et publiés, pas cachés : ils sont la
mesure du changement proposé.

## 8.59.3 — D3 : le leave-one-out — l'adoption repose sur chaque paire passante

Leave-one-out exhaustif sur V1 (8 suppressions) et V2 (48
suppressions), même règle de comptage, même plancher 0,07 :

| Ensemble | Retrait testé | Résultat | Porte |
|---|---|---|---|
| V1 (8 paires) | Retirer GSE71729 (échec) ou GSE62452 (négative) | **6/7** — passe | — |
| V1 | Retirer HP35, TCGA v4, ICGC, IMMUNE_TCGA, PARP_TCGA ou DEPMAP (les 6 passantes) | **5/7** — échoue | **D3 ÉCHOUE** |
| V2 (48 paires) | Pire cas : retirer DEPMAPROT_CRKL | **36/47** — passe | D3 (V2) passe |
| V2 | Toutes les autres suppressions | 36 ou 37/47 — passe | D3 (V2) passe |

D3 exigeait ≥ 6/7 après tout retrait en V1, ce qui équivaut à
exiger 7/8 avant retrait : avec 6/8, CHAQUE paire passante est
charnière, pas seulement ICGC. La fragilité du §8.56 (« le verdict
tient à une paire ») est donc plus large qu'annoncée : elle tient à
six paires à la fois, c'est-à-dire à l'ensemble des paires qui
passent. En V2, en revanche, la marge est confortable (37/48, pire
cas 36/47) : la fragilité est concentrée aux principales, pas aux
rotations. C'est ce partage — rotations solides, principales
fragiles — qui justifie une adoption provisoire plutôt qu'un rejet :
le score sépare largement là où il y a 48 paires, et tout juste là
où il n'y en a que 8.

## 8.59.4 — D4 : le plancher à échelle égale — ICGC tombe, et c'est tout

Plancher équivalent-sep par paire : `0,07·(1 + maxsep_R)·(1 + maxsep_N)`.
Comptage A2 avec ce plancher :

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
§8.56.2, c'est exactement le comptage de `sep` (5/8) : D4 équivaut
à « `sep` franchit A2 », et `sep` ne le franchit pas. Aux rotations,
les deux paires qui passent le plancher littéral mais pas le
plancher équivalent sont les mêmes qu'au §8.56 : DEPMAPROT_MYH9
(+0,0913 contre 0,1061) et V4ROT_MUC16 (+0,0703 contre 0,1152).
Rien d'autre ne change entre les deux échelles : les trois paires
charnières du §8.56 sont exactement les trois paires qui séparent
les deux comptages, et la re-vérification le confirme à l'identique.

Marges (S6) : ICGC passe le plancher littéral de +0,0270 mais
échoue au plancher équivalent de −0,0322 ; MYH9 passe le plancher
littéral de +0,0213 ; MUC16 passe le plancher littéral de **+0,0003**
(+0,0703) — la plus petite marge du dossier, inchangée depuis le
§8.56. DEPMAPROT_RAB10 est la prochaine paire près du plancher
(+0,0621, à −0,0079) : elle ne passe ni l'un ni l'autre plancher,
dans aucune des deux échelles.

## 8.59.5 — D5 et S7 : les classes sont stables, et le changement est tout en gain

**D5a :** 0 changement de classe de séparation `maxsep` entre la
re-vérification et les classes publiées au §8.56, sur les 60 paires.
**D5b :** 0 changement de classe de signe entre `d_maxsep` et
`d_sep`, sur les 60 paires — comme l'exige la monotonie, vérifié et
non supposé. La re-vérification reproduit le §8.56 paire par paire ;
le dossier est stable, c'est le verdict d'adoption qui est fragile,
pas les chiffres.

**S7 — ancien composite → `maxsep` seul (descriptif, §1.1) :**

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
ce que l'ancien composite séparait déjà. C'est le fait le plus
fort en faveur de l'adoption, et il ne dépend d'aucun plancher
fragile : même au plancher équivalent-sep, `maxsep` (= `sep`)
sépare 35/48 rotations et 5/8 principales, contre 12/48 et 1/8
pour l'ancien composite.

## 8.59.6 — Sensibilités (descriptives, ne décident pas)

- **S1 — sans plancher** : V1 7/8 positifs pour les deux candidats
  (seul GSE62452 négatif, −0,0036 / −0,0021, quasi nul) ; V2 42/48
  positifs pour les deux (négatifs : DEPMAPROT_ACO2, CCND1, MYC,
  UROD, V4ROT_CR2, GSTM1). Identique au §8.56.
- **S2 — barre A1 à 24/48** (protocoles v6.3/v6.4) : les deux
  candidats la franchissent (35/48 et 37/48) — le verdict ne change
  pas sous l'ancienne barre.
- **S3 — équivalence d'échelle** : voir §8.59.4 — les trois paires
  charnières sont ICGC, MYH9, MUC16, et rien d'autre.
- **S4 — ventilation par famille** (V2) : IMMROT 12/12 pour les deux
  (moyenne `maxsep` +0,760, `sep` +0,301) ; V4ROT 10/12 (`maxsep`,
  +MUC16) contre 9/12 (`sep`) ; PARPROT 9/12 pour les deux (les
  trois échecs, PARP1/PARP2/XRCC1, sont positifs mais sous le
  plancher dans les deux échelles) ; DEPMAPROT 6/12 contre 5/12
  (+MYH9). DEPMAPROT (n=45) reste le point faible commun à tous les
  scores — ancien MC, MC_new, MC2, `sep` seul, `maxsep` seul.
- **S5 — plancher de Cohen 0,20 en |d|** : `maxsep` sépare 3/8
  principales (HP35, TCGA v4, IMMUNE_TCGA) et 33/48 rotations.
  Le plancher 0,07 est laxiste en unités |d| : 0,2 est déjà un
  « petit » effet chez Cohen, et 0,07 est en dessous. Le même
  constat vaut pour A3 : +1,6512 contre une barre de 0,30 calibrée
  pour des scores en [0, 1] — `maxsep` franchit A3 trivialement,
  par l'échelle autant que par le signal. S5 ne décide de rien ;
  elle situe la barre.

## 8.59.7 — Contrôles descriptifs (V3–V5, ne décident pas)

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

## 8.59.8 — Recommandation : adopter sous condition (provisoire)

**Recommandation à Zackary : ADOPTER `maxsep` seul comme score MC
affiché, À TITRE PROVISOIRE, aux conditions suivantes — toutes
vérifiables, aucune vague :**

- **C1 — Go explicite de Zackary** après lecture de la présente
  section. Sans ce go, rien ne change : v6.2 reste la version de
  travail, l'ancien MC reste le score affiché avec ses défauts
  connus (§8.49.3).
- **C2 — Affichage conjoint et fragilité en tête.** Partout où
  `maxsep` est affiché comme score MC : `sep` affiché en compagnon
  borné [0, 1] ; plancher 0,07 publié EN UNITÉS |d| ; mention
  « adoption provisoire (§8.59) — le verdict de suffisance tient à
  une paire aux principales (ICGC) et à l'échelle du plancher »
  en tête de chaque table qui cite le score. Pas de table qui
  affiche `maxsep` sans cette mention tant que C3 n'est pas levée.
- **C3 — Levée de la condition par confirmation indépendante.**
  La pleine adoption (sans étiquette « provisoire ») est différée
  jusqu'à ce qu'une confirmation indépendante porte A2 à 7/8 —
  soit une paire principale supplémentaire indépendante qui sépare
  au plancher 0,07 en `maxsep` (ce qui porterait aussi le
  leave-one-out V1 à 6/7 après retrait d'une paire passante),
  soit un lot de paires nouvelles confirmant A2 à ≥ 7/8 — à
  consigner dans une section ultérieure, avec son propre protocole
  gelé. Tant que C3 n'est pas levée, l'adoption reste provisoire.
- **Sélection inchangée.** La sélection du best_config continue
  d'utiliser l'ancien composite. Ce chantier ne propose pas de
  changer la sélection ; la changer demanderait son propre
  protocole et son propre go.
- **Aucune nouvelle version de code.** Pas de v6.5, pas de
  modification de v6.2. L'adoption est une décision d'affichage
  consignée sur la v6.2 existante. Si Zackary adopte, le
  coordinateur : gèle le changement d'affichage, régénère le PDF,
  pousse sur GitHub (règle permanente), et met à jour les sections
  qui citent le MC (dont les tableaux des §8.49, §8.52, §8.56, qui
  gardent leurs valeurs historiques avec la mention du changement
  d'affichage et sa date).

**Ce qui est gagné** (si Zackary adopte, même provisoirement) : plus
de saturation artificielle (D4 tombe), plus de terme mort (D1),
plus de terme anti-discriminant (D2, D3), plus de malédiction du
vainqueur déguisée en composite (D5) — le score est la séparation
elle-même, lisible directement en |d de Cohen| ; et 30 paires
gagnent la classe « sépare », zéro n'en perd.

**Ce qui est perdu / ce qui reste fragile** : le plafond [0, 1] et
la comparabilité immédiate avec les scores publiés (MC ancien,
MC_new, MC2, S_sep) — d'où le compagnon `sep` en C2 ; un |d| brut
n'a pas d'échelle commune entre études sans son contexte (n, flux,
contrôle) ; DEPMAPROT reste à 6/12 ; et le verdict de suffisance
reste à une paire près (D3) et à une convention d'échelle près (D4)
— d'où l'étiquette « provisoire » en C2 et la confirmation en C3.

**Ce qui n'est pas prouvé** par cette adoption : que `maxsep`
sépare « le réel du nul » en général — il sépare 37/48 rotations
et 6/8 principales aux barres gelées, avec les fragilités dites,
et 5/12 seulement sur DEPMAPROT. Le verdict porte sur le score,
pas sur l'instrument. Rien de clinique : l'étude porte sur
l'instrument.

## 8.59.9 — Limites et ce qui reste

- La validation hors-ligne réutilise les JSON v6.2 : elle ne teste
  que la RELECTURE, pas une nouvelle mesure. La porte D2 est le
  seul contrôle d'exactitude, sur 120 runs relus deux fois.
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
  demeure le compagnon borné de `maxsep` (C2), avec son échec à A2
  consigné.
- La question du §8.56.6 (« que voudrait dire adopter `maxsep` »)
  est close telle que posée ici : adopter, provisoirement, aux
  conditions C1–C3 ; la pleine adoption attend une confirmation
  indépendante. Aucune autre recomposition n'est proposée : quatre
  chantiers (v6.3, v6.4, §8.56, §8.59) ont maintenant montré que
  le problème n'était pas le terme annexe — c'était le composite
  lui-même, et que le remplacer se fait avec une marge d'une paire,
  pas avec un triomphe.

## 8.59.10 — Provenance

- Protocole gelé : `PROTOCOL_maxsep_adoption_859.md`, SHA-256
  `efb5da799d245d8e5db570945acc480f1c5bae42d63ed29b7cfeb780610e675b`.
- Extracteur hors-ligne : `extract_maxsep_adoption_859.py` (SHA-256
  `9521bd780bb7ede242c6c59002dfbef49f593728df5b13a687bbce199f169c26`) ;
  sorties `maxsep_adoption_859_table.csv` (SHA-256
  `c9ac12e4240b215ed54df43a97a55163a94635dae2baaee3919471d482b3bd9b`) /
  `maxsep_adoption_859_table.json` (SHA-256
  `702f166d76351ab62760655bbc35ed48a9cdcaf77002008d5f4ae172814c2c7f`).
- Vérification indépendante : `verify_maxsep_adoption_859.py`
  (SHA-256
  `9a2b9b1b6bd5773d03caadcc6014bcaf60ca75f804c05e25d40a3fa9ffcf3d36`)
  → `maxsep_adoption_859_verify.json` (SHA-256
  `046f739b03b3f9fa8f73fb6472769b2cf931e4b0ed392685acb78cdfb46c3976` ;
  120/120 dossiers, écart max 0,0 exact, multisets égaux).
- Section : `section_8.59_maxsep_adoption.md` (ce fichier ; SHA noté
  au rapport).
- Référence re-vérifiée : `sep_maxsep_856_table.json` (SHA-256
  `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`),
  `sep_maxsep_856_table.csv` (SHA-256
  `c9ac12e4240b215ed54df43a97a55163a94635dae2baaee3919471d482b3bd9b`) ;
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
  `maxsep_adoption_859_table.json`, vérifiées paire par paire contre
  `sep_maxsep_856_table.json` à 1e-9 ; les valeurs du §8.59.4 sont
  lues dans cette table, pas recopiées du §8.56).
- Livre blanc de référence : `livre-blanc-pdac-v6.md`, 8 315 lignes,
  SHA-256 `502d0b2f739f12e87fd1441fc7a63c9215d582701913fc6de7d5a90c06deb16b`
  (§8.1–§8.58, état au 20 nov. 2026 avant fusion de la présente section).
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`), v6.1 (`2af5e5ce…c1c9`),
  v6 (`bb8bbdba…c0773`), v6.3 (`552e7359…44ffb`), v6.4 (`9ed728da…9ea3d`).
  Aucune nouvelle version construite dans ce chantier — pas de v6.5.
  Aucun run du pipeline lancé dans ce chantier (re-vérification
  hors-ligne, 120 JSON existants).
