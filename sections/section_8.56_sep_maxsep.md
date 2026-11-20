# §8.56 — « sep seul ou maxsep seul suffisent-ils » comme score MC ?

## Verdict d'abord

**`maxsep` seul SUFFIT aux quatre barres gelées — `sep` seul NE SUFFIT PAS.
La question ouverte du §8.52.6 est tranchée, et la marge est mince :
elle tient à trois paires et à l'échelle du plancher.**

| Candidat | A1 rotations (≥ 30/48) | A2 principales (≥ 6/8, ≥ 7/8 positifs) | A3 HP35 (≥ 0,30) | A4 relecture exacte | Sort |
|---|---|---|---|---|---|
| `sep` seul | **35/48** | **5/8**, 7/8 positifs | **+0,5316** | franchie | **REJETÉ** (A2) |
| `maxsep` seul | **37/48** | **6/8**, 7/8 positifs | **+1,6512** | franchie | **SUFFIT** — proposition d'adoption |

**Proposition (pas adoption) :** remplacer le score MC affiché — le
composite ancien `0.3·s_norm + 0.3·stability + 0.2·robustness +
0.2·sharpness` — par `max_separation` lui-même, le |d de Cohen| maximal
du scan de seuil, déjà émis par v6.2. La décision finale d'adoption
revient à Zackary ; ce chantier propose, il n'adopte pas. La v6.2 reste
la version de travail tant que la décision n'est pas prise.

**Fragilité, dite en tête et pas en note de bas de page.** Les deux
candidats ont le même ordre et les mêmes signes d'écart sur les 60
paires (`sep` est une transformée strictement croissante de `maxsep`) ;
sans plancher, ils sont identiques : 42/48 rotations et 7/8
principales, positifs, pour les deux. Toute la différence vient du
plancher 0,07 appliqué dans les unités propres de chaque candidat —
0,07 en |d| est plus facile à franchir que 0,07 en unités `sep`,
d'un facteur (1+m_R)(1+m_N) — médiane 1,80, étendue 1,30–3,11 sur les
60 paires (§8.56.4). Les trois
paires qui font basculer le verdict sont nommées : **ICGC** (A2 :
maxsep +0,0970 contre sep +0,0525), **DEPMAPROT_MYH9** et **V4ROT_MUC16**
(A1 : maxsep +0,0913 et +0,0703 — ce dernier passe le plancher de
0,0003). `maxsep` passe A2 exactement au minimum (6/8). Un verdict qui
tient à une paire et à l'échelle du plancher est un verdict à prendre
avec sa fragilité, pas un triomphe. Il dit tout de même quelque chose
de net : **aucun terme annexe n'est nécessaire** — la meilleure
composante du composite, seule, fait mieux que tous les composites
essayés (ancien 12/48, v6.3 31/48, v6.4 28/48, `sep` seul 35/48).

Protocole gelé : `PROTOCOL_sep_maxsep_856.md` (19 nov. 2026). Barres
écrites AVANT toute extraction du présent chantier (§4 du protocole) ;
aucune repondération, aucun nouveau terme, aucune redéfinition du
plancher après avoir vu les chiffres.

## 8.56.1 — Les quatre portes, et leur sort

| Porte (PROTOCOL_sep_maxsep_856.md §4) | Exigé | `sep` seul | `maxsep` seul |
|---|---|---|---|
| A1 — rotations sans doublon (48 paires), sépare au plancher 0,07 | ≥ 30/48 | **35/48** (direction réel > nul, somme +7,9306, moyenne +0,1652) | **37/48** (somme +17,3623, moyenne +0,3617) |
| A2 — paires principales, > 0,07 et positif | ≥ 6/8 > 0,07 et ≥ 7/8 positifs | **5/8** > 0,07 ; **7/8** positifs | **6/8** > 0,07 ; **7/8** positifs |
| A3 — HP35 (contrôle positif), écart | ≥ 0,30 | **+0,5316** (ancien +0,1950) | **+1,6512** (ancien +0,1950) |
| A4 — relecture exacte (pas de nouveau code pipeline) | 120/120 à 0,0 exact + recoupements à 1e-9 + SHA inchangés | **franchie** | **franchie** |

Références : ancien MC — rotations 12/48 (moyenne +0,0152),
principales 1/8 au plancher 0,07 (7/8 positifs), HP35 +0,1950 ;
v6.3 MC_new — 31/48, 4/8, +0,2271 ; v6.4 MC2 — 28/48, 4/8, +0,5529.
`sep` seul bat les deux recompositions sur les rotations (35/48 contre
31 et 28) et égale leur meilleur score aux principales (5/8 contre 4/8)
— et reste en retrait de `maxsep` sur les deux ensembles. La leçon des
§8.49.6 et §8.52.4 se confirme une troisième fois : chaque terme annexe
ajouté à la séparation coûte plus qu'il ne rapporte.

## 8.56.2 — Définitions exactes (lues dans le code v6.2)

Fichier `universal_v6.2.0_cohen.py`, fonction `evaluate_scan_quality`
(lignes 3314–3390). Par tirage, le scan de seuil donne une courbe de
scores = |d de Cohen| pré/post-seuil :

- **`maxsep`** = score maximal de la courbe (ligne 3333 :
  `max_separation = scores[max_idx]`). C'est un |d de Cohen|, sans
  dimension mais NON borné (plage [0, ∞[). Champ JSON lu :
  `run_pipeline.threshold_metadata.threshold_optimization.best_config.metrics.max_separation`.
- **`sep`** = `maxsep / (1 + maxsep)` (définition des protocoles v6.3 §4
  et v6.4 §3, reprise telle quelle ; absente du code v6.2, qui émet
  `s_norm = tanh(maxsep/2)` à la ligne 3336). Plage [0, 1[. Ancrage :
  sep = 0,5 quand |d| = 1.

Les deux scores sont lus sur le best_config ANCIEN (sélection par
l'ancien composite, lignes 3480–3484) : la question porte sur le SCORE
AFFICHÉ, pas sur la sélection du tirage. Seuil MC, cascade, S_sep,
Delta, L7a inchangés par construction pour les deux candidats.

**Identité d'échelle (consignée au protocole §1 avant le calcul) :**
pour une paire (R, N),
`d_sep = d_maxsep / ((1 + maxsep_R)·(1 + maxsep_N))`. Le plancher 0,07
en unités `sep` équivaut donc, en unités `maxsep`, à un plancher
`0,07·(1 + maxsep_R)·(1 + maxsep_N)` — toujours plus grand que 0,07.
C'est le mécanisme du §8.56.4.

## 8.56.3 — Validation hors-ligne (60 paires, JSON v6.2 existants, aucun run)

Extracteur `extract_sep_maxsep_856.py` : 60/60 paires lues, 0 manquante,
0 version non attendue (v6.2 partout sauf CLDN18 en v6.1, comme en
§8.49/§8.52) ; ancien MC relu sans écart vs §8.44 (rotations) et phase 2
v6.2 (principales), tol. 1e-9 ; `sep`/`maxsep` recoupés sans écart vs
`v64_mc_table.json`, tol. 1e-9. Second calcul indépendant
(`verify_sep_maxsep_856.py`, chemin de code distinct) : 120/120 dossiers
relus, écart max 0,0 exact, multisets égaux. Gigue_eff = max(gigue
mesurée 0, 0,07) = 0,07 (même plancher que S_sep et que v6.3/v6.4).
Les chiffres ci-dessous sont la RE-VÉRIFICATION du présent chantier ;
ils confirment exactement les diagnostics publiés au §8.52.3/§8.52.6
(`sep` 35/48 et 5/8, `maxsep` 37/48 et 6/8) — aucun écart constaté.

### Paires principales (V1) — `sep` 5/8, `maxsep` 6/8

| Paire | maxsep R / N (écart) | sep R / N (écart) | Ancien MC (écart) |
|---|---|---|---|
| HP35 | 1,7718 / 0,1206 (**+1,6512**) | 0,6392 / 0,1076 (**+0,5316**) | +0,1950 |
| TCGA v4 | 0,4623 / 0,1696 (**+0,2928**) | 0,3162 / 0,1450 (**+0,1712**) | +0,0453 |
| GSE71729 | 0,2593 / 0,2191 (+0,0402) | 0,2059 / 0,1797 (+0,0262) | +0,0059 |
| GSE62452 | 0,3100 / 0,3136 (−0,0036) | 0,2367 / 0,2387 (−0,0021) | −0,0031 |
| ICGC | 0,4080 / 0,3110 (**+0,0970**) | 0,2898 / 0,2372 (+0,0525) | +0,0150 |
| Immunitaire TCGA | 0,5309 / 0,1634 (**+0,3675**) | 0,3468 / 0,1405 (**+0,2063**) | +0,0545 |
| PARP TCGA | 0,3680 / 0,1992 (**+0,1688**) | 0,2690 / 0,1661 (**+0,1029**) | +0,0244 |
| DepMap | 0,4436 / 0,2532 (**+0,1904**) | 0,3073 / 0,2020 (**+0,1052**) | +0,0115 |

`sep` passe le plancher sur HP35, TCGA v4, immunitaire, PARP et DepMap ;
il échoue sur GSE71729 (+0,0262), **ICGC (+0,0525, à 0,0175 du plancher)**
et reste négatif sur GSE62452 (−0,0021, quasi nul, pas une inversion
forte). `maxsep` passe le plancher sur les mêmes cinq paires PLUS ICGC
(+0,0970) — c'est la seule différence aux principales, et c'est elle
qui fait basculer A2. Positifs : 7/8 pour les deux (seul GSE62452 est
négatif). Sommes des écarts V1 : `sep` +1,1939 (moyenne +0,1492),
`maxsep` +2,8043 (moyenne +0,3505).

### Rotations sans doublon (V2) — `sep` 35/48, `maxsep` 37/48

| Famille | `sep` > 0,07 | `maxsep` > 0,07 | Positifs (les deux) | Écart moyen `sep` | Écart moyen `maxsep` |
|---|---|---|---|---|---|
| IMMROT (n=178) | **12/12** | **12/12** | 12/12 | +0,301 | +0,760 |
| V4ROT (n=178) | **9/12** | **10/12** | 10/12 | +0,153 | +0,303 |
| PARPROT (n=178) | **9/12** | **9/12** | 12/12 | +0,162 | +0,306 |
| DEPMAPROT (n=45) | **5/12** | **6/12** | 8/12 | +0,045 | +0,078 |
| **Toutes** | **35/48** | **37/48** | **42/48** | **+0,165** | **+0,362** |

Échecs `sep` (13 paires, écart ≤ 0,07) : les 7 DEPMAPROT restantes
(ACO2, CCND1, CFLAR, MYC, MYH9, RAB10, UROD), PARPROT PARP1 (+0,0120),
PARP2 (+0,0127), XRCC1 (+0,0352), V4ROT CR2 (−0,0224), GSTM1 (−0,0949),
MUC16 (+0,0427). Échecs `maxsep` (11 paires) : les mêmes moins MYH9
(+0,0913) et MUC16 (+0,0703) — les deux seules paires qui séparent
`maxsep` de `sep` sur les rotations. Table complète par paire :

| Paire | maxsep (écart) | sep (écart) | Paire | maxsep (écart) | sep (écart) |
|---|---|---|---|---|---|
| DEPMAPROT_ACO2 | −0,0229 | −0,0146 | IMMROT_CD163 | +0,7945 | +0,2933 |
| DEPMAPROT_CCND1 | −0,1195 | −0,0808 | IMMROT_CD19 | +0,4464 | +0,1952 |
| DEPMAPROT_CFLAR | +0,0166 | +0,0099 | IMMROT_CD274 | +0,5022 | +0,2385 |
| DEPMAPROT_CRKL | +0,2049 | +0,1114 | IMMROT_CD4 | +0,7431 | +0,2404 |
| DEPMAPROT_DOCK5 | +0,2674 | +0,1681 | IMMROT_CD68 | +0,4610 | +0,2374 |
| DEPMAPROT_EFR3A | +0,2297 | +0,1256 | IMMROT_CD8A | +0,9955 | +0,3546 |
| DEPMAPROT_MYC | −0,1434 | −0,0890 | IMMROT_CD8B | +0,8450 | +0,3343 |
| DEPMAPROT_MYH9 | +0,0913 | +0,0603 | IMMROT_CTLA4 | +0,9089 | +0,3079 |
| DEPMAPROT_RAB10 | +0,0621 | +0,0319 | IMMROT_FOXP3 | +0,8480 | +0,2976 |
| DEPMAPROT_RAB6A | +0,2402 | +0,1460 | IMMROT_GZMB | +0,9215 | +0,3585 |
| DEPMAPROT_SCAP | +0,1431 | +0,0853 | IMMROT_IFNG | +0,7287 | +0,3707 |
| DEPMAPROT_UROD | −0,0289 | −0,0175 | IMMROT_PDCD1 | +0,9199 | +0,3830 |
| PARPROT_ATM | +0,1638 | +0,1077 | V4ROT_CEACAM5 | +0,5143 | +0,2615 |
| PARPROT_ATR | +0,2381 | +0,1469 | V4ROT_CLCA1 | +0,3053 | +0,1780 |
| PARPROT_BRCA1 | +0,5300 | +0,2738 | V4ROT_CLDN18 | +0,6831 | +0,3074 |
| PARPROT_BRCA2 | +0,4028 | +0,2154 | V4ROT_CR2 | −0,0292 | −0,0224 |
| PARPROT_CHEK1 | +0,3872 | +0,2135 | V4ROT_DPCR1 | +0,4186 | +0,2127 |
| PARPROT_CHEK2 | +0,2648 | +0,1574 | V4ROT_GSTM1 | −0,1354 | −0,0949 |
| PARPROT_FANCD2 | +0,4414 | +0,2166 | V4ROT_KRT20 | +0,2565 | +0,1516 |
| PARPROT_PARP1 | +0,0191 | +0,0120 | V4ROT_MUC16 | +0,0703 | +0,0427 |
| PARPROT_PARP2 | +0,0203 | +0,0127 | V4ROT_MUC17 | +0,5688 | +0,2736 |
| PARPROT_POLQ | +0,6151 | +0,2809 | V4ROT_MUC2 | +0,2002 | +0,1142 |
| PARPROT_RAD51 | +0,5359 | +0,2762 | V4ROT_PGC | +0,2378 | +0,1283 |
| PARPROT_XRCC1 | +0,0542 | +0,0352 | V4ROT_REG4 | +0,5439 | +0,2818 |

Table complète machine : `sep_maxsep_856_table.csv` / `.json`.

### Contrôles descriptifs (V3–V5, ne décident pas de l'adoption)

| Paire | Ancien MC (écart) | maxsep R / N (écart) | sep R / N (écart) | Lecture |
|---|---|---|---|---|
| Test A (prolifération) | −0,0948 | 0,3943 / 0,1442 (**+0,2501**) | 0,2828 / 0,1260 (**+0,1567**) | Suivent maxsep, comme prévu ; ne ressuscitent pas Test A (verdict NON du §8.34 portait sur la chaîne et MC/Delta) |
| MTAP série PRMT5-flux (§8.43) | +0,0004 | 0,1919 / 0,2955 (**−0,1036**) | 0,1610 / 0,2281 (**−0,0671**) | Restent négatifs, cohérent avec le verdict NON du §8.43 |
| MTAP série (§8.31) | −0,1642 | 0,3392 / 0,1434 (**+0,1957**) | 0,2533 / 0,1254 (**+0,1278**) | Suivent maxsep ; l'ancien MC était fortement inversé ici |
| V4R_PURITY (artefact §8.31) | +0,1520 | 0,1444 / 0,2114 (**−0,0670**) | 0,1262 / 0,1745 (**−0,0483**) | **Artefact CORRIGÉ** : les deux candidats reprennent le sens de maxsep, comme MC_new (−0,0353) et MC2 (−0,1197) avant eux |

Aucun écart de signe entre `sep` et `maxsep` sur les 60 paires : les
deux candidats disent la même chose partout, à l'échelle près — comme
l'exige leur relation monotone (§8.56.2).

## 8.56.4 — Pourquoi `maxsep` passe et `sep` échoue : l'échelle du plancher

C'est le cœur du verdict, et il est entièrement mécanique. Pour chaque
paire, le plancher `sep` de 0,07 équivaut en unités `maxsep` à
`0,07·(1 + maxsep_R)·(1 + maxsep_N)`. Les trois paires qui passent le
plancher littéral 0,07 en `maxsep` mais pas le plancher équivalent sont
exactement les trois paires qui séparent les deux candidats :

| Paire charnière | d_maxsep | Plancher équivalent-sep | d_sep | Effet sur le verdict |
|---|---|---|---|---|
| ICGC (V1) | +0,0970 | 0,1292 | +0,0525 | Fait passer A2 : 5/8 → 6/8 |
| DEPMAPROT_MYH9 (V2) | +0,0913 | 0,1061 | +0,0603 | Fait passer A1 : 35/48 → 36/48 |
| V4ROT_MUC16 (V2) | +0,0703 | 0,1152 | +0,0427 | Fait passer A1 : 36/48 → 37/48, par 0,0003 au-dessus du plancher |

Autrement dit : **si le plancher était appliqué à `maxsep` à son
équivalent d'échelle `sep`, les deux candidats auraient exactement les
mêmes comptages (35/48, 5/8) et le verdict serait « aucun des deux ne
suffit ».** Le verdict « `maxsep` suffit » tient donc à la convention
du projet — le plancher 0,07 appliqué littéralement, dans les unités
propres du score jugé (§3 du protocole) — et non à un signal que `sep`
manquerait. Cette convention est la même que pour S_sep, MC_new et MC2 ;
l'appliquer autrement ici aurait été une redéfinition après coup,
interdite par le protocole gelé. Mais elle doit être nommée : 0,07 en
|d| est une barre laxiste — en conventions de Cohen, 0,2 est déjà un
« petit » effet, et 0,07 en |d| est en dessous. Le même constat vaut
pour A3 : +1,6512 en |d| contre une barre de 0,30 calibrée pour des
scores en [0, 1] — `maxsep` franchit A3 trivialement, par l'échelle
autant que par le signal. Pour `sep`, en revanche, les barres sont
homogènes (même échelle [0, 1] que MC_new/MC2) : son échec à A2 est un
échec « propre », à 0,0175 du plancher sur ICGC.

Deux lectures honnêtes coexistent, et la section les donne toutes les
deux : (a) aux barres gelées, littéralement appliquées comme pour tous
les scores précédents, `maxsep` seul suffit et `sep` seul ne suffit
pas — c'est le verdict du chantier ; (b) à échelle de plancher égale,
les deux candidats sont le même score, et ni l'un ni l'autre ne franchit
A2. La proposition d'adoption porte sur (a) ; elle ne doit pas être
lue comme une preuve que `maxsep` détecte quelque chose que `sep`
ne détecte pas — il détecte exactement la même chose, moins comprimée.

## 8.56.5 — Sensibilités (descriptives, ne décident pas)

- **S1 — sans plancher** : V1 7/8 positifs pour les deux candidats
  (seul GSE62452 négatif, −0,0036 / −0,0021, quasi nul) ; V2 42/48
  positifs pour les deux (négatifs : DEPMAPROT_ACO2, CCND1, MYC,
  UROD, V4ROT_CR2, GSTM1). Sans plancher, S et M sont indiscernables.
- **S2 — barre A1 à 24/48** (protocoles v6.3/v6.4) : les deux candidats
  la franchissent (35/48 et 37/48) — le verdict ne change pas sous
  l'ancienne barre.
- **S3 — équivalence d'échelle** : voir le tableau du §8.56.4 — les
  trois paires charnières sont ICGC, MYH9, MUC16, et rien d'autre.
- **S4 — ventilation par famille** : IMMROT 12/12 pour les deux ;
  V4ROT 9/12 (`sep`) contre 10/12 (`maxsep`, +MUC16) ; PARPROT 9/12
  pour les deux (les trois échecs, PARP1/PARP2/XRCC1, sont positifs
  mais sous le plancher dans les deux échelles) ; DEPMAPROT 5/12
  contre 6/12 (+MYH9). DEPMAPROT (n=45) reste le point faible commun
  à l'ancien MC, MC_new, MC2, `sep` seul et `maxsep` : les petites
  cohortes séparent mal, quel que soit le score.

## 8.56.6 — Ce que « adopter `maxsep` » voudrait dire

Adopter `maxsep` seul comme score MC, ce serait **retirer le composite,
pas en composer un nouveau** : afficher `best_config.metrics.max_separation`
— le |d de Cohen| maximal du scan — comme le score, et abandonner
`s_norm`, `stability`, `robustness`, `sharpness` dans l'affichage (la
sélection du best_config, elle, continuerait d'utiliser l'ancien
composite, sauf décision contraire — ce chantier ne propose pas de
changer la sélection). Conséquences à peser avant toute adoption :

- **Ce qui est gagné :** plus de saturation artificielle (D4 tombe :
  `sep` et `s_norm` comprimaient les écarts PDAC), plus de terme mort
  (D1), plus de terme anti-discriminant (D2, D3), plus de malédiction
  du vainqueur déguisée en composite (D5) — le score est la séparation
  elle-même, lisible directement en |d de Cohen|.
- **Ce qui est perdu :** le plafond [0, 1] et la comparabilité immédiate
  avec les scores publiés (MC ancien, MC_new, MC2, S_sep) ; un |d| brut
  n'a pas d'échelle commune entre études sans son contexte (n, flux,
  contrôle). `maxsep` existe déjà comme indicateur (§8.37–§8.38, S_sep
  = maxsep × stability) : l'adopter comme « score MC » n'ajoute aucun
  nouvel indicateur, il en retire un.
- **Ce qui n'est pas prouvé :** que `maxsep` sépare « le réel du nul »
  en général — il sépare 37/48 rotations et 6/8 principales aux barres
  gelées, avec les fragilités du §8.56.4, et 5/12 seulement sur
  DEPMAPROT. Le verdict porte sur le score, pas sur l'instrument.

Si Zackary adopte, le chantier d'adoption devra : geler le changement
d'affichage (le champ `score` reste l'ancien composite pour la sélection
ou bascule aussi — à trancher explicitement), régénérer le PDF, pousser
sur GitHub (règle permanente), et mettre à jour les sections qui citent
le MC. Si Zackary n'adopte pas, le statu quo tient : v6.2 reste la
version de travail, l'ancien MC reste le score affiché avec ses défauts
connus (§8.49.3), et `maxsep` reste l'indicateur de référence qu'il est
déjà.

## 8.56.7 — Limites et ce qui reste

- La validation hors-ligne réutilise les JSON v6.2 : elle ne teste que
  la RELECTURE, pas une nouvelle mesure. La porte A4 (§8.56.3) est le
  seul contrôle d'exactitude, sur 120 runs relus deux fois.
- Le plancher 0,07 est une convention du projet, pas une propriété
  statistique de `sep` ou de `maxsep` ; le verdict « `maxsep` suffit »
  tient à son application littérale en unités |d| (§8.56.4). À échelle
  de plancher égale, le verdict serait « aucun des deux ».
- `maxsep` passe A2 exactement au minimum (6/8) et A1 avec deux paires
  dont une passe le plancher de 0,0003 (V4ROT_MUC16, +0,0703) : le
  verdict est fragile à une paire près sur les deux portes à la fois.
- DEPMAPROT (n=45) reste le point faible commun à tous les scores.
- `sep` seul est rejeté comme score MC unique — mais `sep` reste la
  transformée bornée de `maxsep` : là où un score en [0, 1] est voulu
  (comparaison inter-études, affichage), `sep` demeure l'option
  bornée, avec son échec à A2 consigné.
- La question du §8.52.6 est close telle que posée ici : « `sep` seul,
  ou `maxsep` lui-même, suffisent-ils » — réponse : `maxsep` seul, aux
  barres gelées, avec la fragilité dite ; `sep` seul, non. Aucune autre
  recomposition n'est proposée : trois chantiers (v6.3, v6.4, §8.56)
  ont maintenant montré que le problème n'était pas le terme annexe
  — c'était le composite lui-même.
- Rien de clinique : l'étude porte sur l'instrument.

## 8.56.8 — Provenance

- Protocole gelé : `PROTOCOL_sep_maxsep_856.md`, SHA
  `06e36725eedb3d52b1549290e1e8cccff381650928fbf4e6a28a090aec27fd4e`.
- Extracteur hors-ligne : `extract_sep_maxsep_856.py` (SHA noté au
  rapport) ; sorties `sep_maxsep_856_table.csv` /
  `sep_maxsep_856_table.json` (SHA notés au rapport).
- Vérification indépendante : `verify_sep_maxsep_856.py` (SHA noté au
  rapport) → `sep_maxsep_856_verify.json` (120/120 dossiers, écart
  max 0,0 exact).
- Section : `section_8.56_sep_maxsep.md` (ce fichier ; SHA noté au rapport).
- Données : JSON v6.2 existants (lots §8.44, phase 2, §8.43, Test A) ;
  CSV inchangés, SHA déjà publiés dans `PROVENANCE_rotations_dedup_844.md`,
  `PROVENANCE_tcga_v4.md`, `PROVENANCE_mtap_prmt5_flux.md`,
  `PROVENANCE_testA_proliferation.md`. Nuls = lignes permutées, graine
  42 — échantillons hypothétiques, pas des mesures. Séries réelles =
  résidus d'expression génique ou de dépendance CRISPR (mesures
  instrumentales transformées). Aucune valeur inventée ; aucune valeur
  recopiée à la main (tables générées depuis `sep_maxsep_856_table.json`,
  vérifiées paire par paire contre `v64_mc_table.json` à 1e-9).
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`), v6.1 (`2af5e5ce…c1c9`),
  v6 (`bb8bbdba…c0773`), v6.3 (`552e7359…44ffb`), v6.4 (`9ed728da…9ea3d`).
  Aucune nouvelle version construite dans ce chantier.
