# §8.61 Pureté par méthylation : une seconde mesure ADN qui sépare comme ABSOLUTE, mais retire moins en linéaire — zone grise

Date : 20 novembre 2026 (06h43–07h30 heure de Montréal, 11h43–12h30 UTC).
Go : coordinateur, 20 nov. 2026 (chantier jumeau du §8.55, nommé au
§8.55.11).
Protocole gelé avant tout calcul de ce chantier, avant tout nouveau run :
`PROTOCOL_methylation_purity_861.md` (SHA-256
`93f4f777f217d9a03c01b1b79397ed70e59567e53edaf4231864e9c6a50e0993`).

## Verdict d'abord

**Les deux mesures ADN s'accordent sur la séparation, elles divergent
sur la part linéaire — et la règle gelée tranche : ZONE GRISE.**
La pureté par méthylation (`DNA.hypermethylation.mode.purity`,
Raphael et al. 2017, Table S1) corrèle fortement avec les 12 flux
immunitaires — tous négativement, moyenne |r| = **0,4228** (CD8A
r = −0,635, R² = 40,3 %) — et **ordonner les flux par METH les sépare
presque autant qu'ABSOLUTE : écart S_sep +0,6739**, soit 97,5 % du
+0,6911 d'E-ABS au §8.55, prédit +0,5459 à 0,128 près. Ordonner les flux
RÉSIDUALISÉS par CD8A résidualisé sépare encore **+0,5427** — 55,2 % du
brut (+0,9838), 83,5 % d'E-RES (+0,6499). Mais la régression linéaire
raconte une autre histoire : après régression sur METH, la corrélation
intra-famille ne chute que de **15,9 % (0,5035 → 0,4235)** — contre
25,5 % pour ABSOLUTE — et la sensibilité conjointe [ABSOLUTE, METH]
retombe à 24,6 %, c'est-à-dire qu'**ajouter METH à ABSOLUTE ne retire
presque rien de plus qu'ABSOLUTE seul**. Critère gelé : T2'' =
PERSISTANCE (chute < 20 %), M-METH = +0,6739 (≥ 0,45), M-RES = +0,5427
(≥ 0,45, < 0,70). Ni H1-meth totale (pas d'effondrement), ni H1-meth
partielle (T2'' n'est pas partielle et M-METH n'est pas entre 0,30 et
0,45), ni H0-meth (M-METH n'est pas < 0,30) ne sont soutenues par la
règle gelée. **Verdict gelé : ZONE GRISE.** Le « environ un tiers »
du §8.55 n'est pas contredit sur la séparation — il est qualifié sur
la part linéaire : par la voie méthylation seule, la part linéaire
retirée est d'environ un sixième, pas un tiers.

**Ce que cela dit, en une phrase.** Deux mesures ADN de la même table
donnent le même ordre (les tumeurs pures en bas, les infiltrées en
haut) mais pas la même part linéaire — la pureté porte la séparation,
la linéarité ne la capture qu'en partie, et la différence entre les
deux mesures est elle-même une information, pas une erreur à lisser.

## 8.61.1 Question, méthode, inventaire des sources (avant le gel)

**Question (§8.55.11).** Le §8.55 a établi, avec ABSOLUTE (nombre de
copies ADN), que la corrélation intra-famille immunitaire est portée
pour environ un tiers par la pureté : 0,5040 → 0,3757 après régression
(chute 25,5 %), E-ABS +0,6911, E-RES +0,6499 (66,1 % du brut) —
H1-ext PARTIELLE. La même Table S1 contient une troisième mesure de
pureté, par méthylation de l'ADN, indépendante de l'ARN elle aussi mais
par une voie différente (mode d'hyperméthylation, pas nombre de
copies). Donne-t-elle le même chiffre, ou un chiffre différent ?

**Source gelée : pas un nouveau téléchargement.** La colonne méthylation
vient de la MÊME table que l'ABSOLUTE du §8.55, déjà obtenue et
vérifiée : pdacR (Torre-Healy et al. 2023), `data/TCGA_PAAD.rds`,
SHA-256 `52020679350d1539d7516f7d38f7bf09e510225eba2f228a4fe874f3c496ea76`,
transcrite dans `purity_855_sampinfo.csv` (SHA `7a09dde3…b014`).
**Re-vérification faite avant les calculs :** re-téléchargement du RDS
depuis son URL le 20 nov. 2026 — SHA identique (`52020679…ea76`),
12 311 529 octets — la source est toujours accessible et inchangée.
Le téléchargement direct de la Table S1 de Raphael depuis PMC reste
bloqué par le défi de preuve de travail (constaté au §8.55, non
re-tenté ici).

**Note d'honnêteté sur l'ordre des opérations.** La présence de la
colonne méthylation n'est pas une découverte de ce chantier : elle
était nommée au §8.55.2/§8.55.11 (150/178 appariées, r = 0,856 avec
ABSOLUTE, calculé au §8.55 comme vérification de cohérence, n = 149).
Ce qui est gelé ici, ce sont la porte S, la jointure, les tests et les
critères — aucun chiffre T1''–T5'' n'a été calculé avant le gel.

**Critères gelés.** Ceux du §8.55, appliqués à METH (mêmes seuils) :
T1'' substantiel si moyenne |r| ≥ 0,30 ; T2'' EFFONDREMENT si moyenne
|r| résiduelle < 0,30 (chute ≥ 45 %) ET fraction |r| > 0,5 < 0,20 ;
PERSISTANCE si chute < 20 % ; entre les deux : partielle. T5'' :
M-METH soutient H1-meth si écart ≥ 0,45 ; M-RES soutient H1-meth si
écart < 0,30, soutient H0-meth si écart ≥ 0,45. Verdict : H1-meth
totale si T2'' = effondrement ET M-RES < 0,30 ET M-METH ≥ 0,45 ;
H1-meth PARTIELLE si T2'' = partielle OU (M-METH entre 0,30 et 0,45)
avec M-RES < 0,70 ; H0-meth si T2'' = persistance ET M-METH < 0,30 ET
M-RES ≥ 0,45 ; toute autre combinaison : zone grise. Références :
IMMROT sans doublon, moyenne +0,7521, minimum +0,4508 (CD68), CD8A
écart +0,9838 (réel 1,2310, nul 0,2472) ; régression §8.48
d_ssep = −0,175 + 1,705·C ; §8.55 : E-ABS +0,6911, E-RES +0,6499.

## 8.61.2 Porte S (source) : OUVERTE

Jointure sur les **15 premiers caractères** du barcode (protocole §4) :
178/178 tumeurs du projet appariées (0 collision de clé des deux
côtés) ; **METH non nulle pour 150/178 (84,3 %)** — au-dessus du seuil
gelé (≥ 100). Toutes les valeurs dans [0, 1] (min 0,1345, max 0,6814).
Les 3 échantillons externes hors projet sont les mêmes qu'au §8.55
(TCGA-HZ-A9TJ-06A, métastase ; TCGA-H6-8124-11A et TCGA-YB-A89D-11A,
tissu normal adjacent) — correctement exclus par le critère « tumeurs
primaires code 01 ». Les 28 tumeurs sans METH sont les non-whitelistées
de Raphael, comme les 29 sans ABSOLUTE (une seule tumeur,
TCGA-2J-AAB9-01A-11R-A41B-07, a METH mais pas ABSOLUTE : n METH = 150,
n ABSOLUTE = 149).

METH (n = 150) : min 0,1345, médiane 0,3996, moyenne 0,3958,
écart-type 0,1276, max 0,6814. Fichier apparié :
`purity_861_external.csv` (SHA `cf127ef7…d24b`, 150 lignes : sample,
purity_methylation, purity_absolute, fraction leucocytaire, classe,
cellularité pathologiste).

**Cohérence de la colonne METH — trois vérifications :**
(a) METH corrèle à **r = +0,8556 (n = 149, p = 7,0×10⁻⁴⁴)** avec
ABSOLUTE — reproduction EXACTE à 4 décimales de la valeur du §8.55
(0,8556), recalculée en machine ici ; deux mesures ADN s'accordent ;
(b) la classification haut/bas publiée est MOINS nette pour METH que
pour ABSOLUTE : classe high n = 76, METH [0,2661 ; 0,6814], moyenne
0,4915 ; classe low n = 74, METH [0,1345 ; 0,4739], moyenne 0,2976 —
les deux classes se CHEVAUCHENT sur [0,2661 ; 0,4739], contrairement à
ABSOLUTE qui les séparait exactement au seuil 0,33 sans chevauchement.
METH ne reproduit pas la classification publiée : elle est une mesure
de pureté plus bruitée, ou une mesure d'autre chose en partie ;
(c) METH corrèle à r = −0,6774 avec la fraction leucocytaire par
méthylation (n = 150, p = 1,8×10⁻²¹), ABSOLUTE à r = −0,6901
(n = 149) — les deux puretés s'accordent aussi contre les leucocytes.
Ces vérifications ne remplacent pas une relecture directe de la
Table S1 (restée inaccessible derrière le défi PMC) ; elles rendent
une erreur de transcription invraisemblable, et la (b) est une limite
réelle de METH, nommée ici.

## 8.61.3 T1'' — Chaque flux immunitaire suit METH : fortement, tous négativement

Pearson r (+ Spearman ρ) de chaque flux contre METH ; R² par flux
(OLS sur [1, METH]) ; p brutes bilatérales, sans correction pour tests
multiples (12 tests — le jugement porte sur la moyenne, pas sur une p
isolée).

| Gène | r METH (p) | ρ METH | R² METH | r ABSOLUTE (§8.55, n = 149) |
|---|---|---|---|---|
| CD8A | **−0,635 (2,7×10⁻¹⁸)** | −0,632 | **0,403** | −0,676 |
| CD8B | −0,538 (1,3×10⁻¹²) | −0,535 | 0,289 | −0,563 |
| CD4 | −0,556 (1,6×10⁻¹³) | −0,563 | 0,309 | −0,633 |
| FOXP3 | −0,457 (4,1×10⁻⁹) | −0,487 | 0,209 | −0,533 |
| CD68 | −0,121 (0,14) | −0,080 | 0,015 | −0,212 |
| CD163 | −0,486 (3,0×10⁻¹⁰) | −0,485 | 0,236 | −0,584 |
| CD274 | −0,209 (1,0×10⁻²) | −0,240 | 0,044 | −0,308 |
| PDCD1 | −0,540 (1,0×10⁻¹²) | −0,557 | 0,291 | −0,564 |
| CTLA4 | −0,515 (1,5×10⁻¹¹) | −0,512 | 0,266 | −0,593 |
| GZMB | −0,397 (4,9×10⁻⁷) | −0,436 | 0,158 | −0,451 |
| IFNG | −0,171 (3,7×10⁻²) | −0,218 | 0,029 | −0,306 |
| CD19 | −0,450 (7,7×10⁻⁹) | −0,455 | 0,202 | −0,495 |

Moyenne |r| : **0,4228** (Spearman 0,4334), contre 0,4932 pour
ABSOLUTE — 86 % de la force d'ABSOLUTE, flux par flux dans le même
ordre (CD8A en tête, CD68 dernier, IFNG et CD274 faibles). **R²
médian 0,2224 (22,2 %), maximum 0,4030 (CD8A).** Significatifs à
p < 0,05 : 11/12 (seul CD68 ne l'est pas, p = 0,14) ; à p < 0,001 :
9/12. Critère gelé : lien SUBSTANTIEL (≥ 0,30 — dépassé de 41 %).
Trois remarques : (a) les 12 corrélations sont NÉGATIVES — le sens
attendu d'une dilution, comme ABSOLUTE ; (b) METH explique 22 % de la
variance du gène immunitaire médian et 40 % de CD8A — contre 30 % et
46 % pour ABSOLUTE : METH est la mesure la plus faible des deux, sur
chaque flux sans exception (12/12 |r| plus petits) ; (c) CD68 est
l'exception comme au §8.55 (r = −0,121, R² = 1,5 %) — les macrophages
suivent moins la pureté que les lymphocytes, quelle que soit la mesure.

## 8.61.4 T2'' — La corrélation intra-famille chute peu, ne s'effondre pas — et c'est là que METH diverge d'ABSOLUTE

Matrice 66 paires, sur les n = 150 appariées (la brute de référence est
recalculée sur ce sous-ensemble, jamais importée du §8.51 ou du §8.55).

| Matrice | Pearson moyenne \|r\| | médiane \|r\| | fraction \|r\| > 0,5 | Spearman moyenne \|r\| |
|---|---|---|---|---|
| Brute (n = 150) | **0,5035** | 0,5422 | 0,561 (37/66) | 0,4871 |
| Résidus [1, METH] | **0,4235** | 0,4337 | 0,364 (24/66) | 0,4041 |
| Brute (n = 178, réf.) | 0,5563 | — | — | 0,5403 |
| Sensibilité [ABS, METH] (n = 149) : brute → résidus | 0,5040 → **0,3798** | — | — | — |

**Chute METH seul : 15,9 %** (0,5035 → 0,4235) ; la fraction de
paires fortes passe de 37/66 à 24/66. Critère gelé : ni EFFONDREMENT
(résiduelle 0,4235 > 0,30 ; chute 15,9 % < 45 %) ni PARTIELLE (chute
15,9 % < 20 % ; résiduelle 0,4235 > 0,80 × 0,5035 = 0,4028) :
**T2'' = PERSISTANCE**. Retirer linéairement toute la pureté METH ne
retire qu'un sixième de la corrélation.

**Sensibilité conjointe (n = 149, les deux mesures ADN ensemble) :**
0,5040 → 0,3798, chute **24,6 %** — pratiquement identique à ABSOLUTE
seul (25,5 %). **Ajouter METH à ABSOLUTE ne retire presque rien de
plus (0,9 point de chute) :** l'information linéaire de METH sur la
cohésion est presque entièrement contenue dans ABSOLUTE. Les deux
mesures ne sont pas additives en linéaire — elles se recouvrent.

**La divergence METH↔ABSOLUTE, chiffrée.** ABSOLUTE retire 25,5 %,
METH 15,9 % : 9,6 points d'écart sur la même cohorte, les mêmes flux,
le même n à une tumeur près. Ce n'est pas un effet de sélection
(la brute est 0,5035 à n = 150 contre 0,5040 à n = 149 — identique).
C'est une différence entre deux mesures ADN de la même table : ABSOLUTE
(nombre de copies) capte plus de la corrélation linéaire que METH
(mode d'hyperméthylation). Deux lectures possibles, non tranchées ici :
METH est plus bruitée (elle ne reproduit pas la classification
high/low, §8.61.2b), ou elle mesure une facette différente de la
pureté, moins alignée avec la dilution ARN. Dans les deux cas, la part
linéaire « pureté » dépend de la mesure choisie : ~un quart par
ABSOLUTE, ~un sixième par METH.

## 8.61.5 T3'' — Couplage prédit : la régression §8.48 tient, avant comme après

Couplage C par contrôle immunitaire (moyenne des |r| avec les 11 autres
flux), brut contre résidualisé ; d_ssep prédit par d = −0,175 + 1,705·C.

| | C moyen | d_ssep prédit moyen |
|---|---|---|
| Brut (n = 150) | 0,5035 | **0,6835** |
| Résidualisé [METH] | 0,4235 | **0,5470** |

CD8A seul : C 0,6056 → 0,5092, d_pred 0,8575 → **0,6932**. Le T3''
ne fait que traduire T2'' en S_sep prédit ; le verdict se joue au T5''.
À noter : la prédiction résiduelle (+0,6932) est PLUS haute que
l'observée E-RES au §8.55 (+0,6499) — la régression §8.48 surestime
ici le résiduel METH, de 0,1505 (cf. §8.61.7).

## 8.61.6 T4'' — Stratification : la cohésion persiste dans chaque moitié

Médiane de METH = 0,3996 (n = 75/75) ; matrice intra-famille dans
chaque moitié.

| Stratification | Moitié haute : moyenne \|r\| (frac. > 0,5) | Moitié basse : moyenne \|r\| (frac. > 0,5) |
|---|---|---|
| METH (méd. 0,3996) | 0,4213 (—) | 0,4350 (—) |

Si la cohésion venait entièrement de la pureté, elle devrait
s'effondrer dans chaque moitié (bande de pureté étroite). Elle persiste
dans les deux moitiés (0,42 et 0,44, contre 0,5035 global) — réduite,
pas effondrée. Argument non paramétrique, indépendant de toute
linéarité : il confirme T2'' par une autre voie — la pureté METH porte
une partie, pas le tout. (Les deux moitiés sont ici presque égales,
contrairement à ABSOLUTE au §8.55 où la moitié basse était plus
cohésive, 0,4283 contre 0,3802.)

## 8.61.7 T5'' — Runs v6.2 : METH ordonne l'immunitaire comme ABSOLUTE, les résidus aussi

Prédictions calculées AVANT de lire les sorties (depuis T1''/T2'' du
jour) : M-METH d_pred +0,5459 (C = 0,4228) ; M-RES d_pred +0,6932
(C_résid CD8A = 0,5092). 4 runs v6.2, mode fast, graine 42, 4/4 exit 0
(lot 11h44:59 UTC – 12h29:47 UTC 20 nov. ; §8.61.10 pour le
déroulement).

| Run | Contrôle → analysés | S_sep réel | S_sep nul | Écart | Prédit | MC réel / nul | Delta réel / nul | w |
|---|---|---|---|---|---|---|---|---|
| M-METH | METH → 12 imm. bruts | 0,8215 | 0,1476 | **+0,6739** | +0,5459 | 0,4204 / 0,3234 | 3,45 / 3,42 | 26 |
| M-RES | CD8A résid. → 11 imm. résid. | 0,8101 | 0,2674 | **+0,5427** | +0,6932 | 0,4190 / 0,3402 | 3,41 / 3,39 | 26 |

Lecture par critère gelé :
- **M-METH : la pureté par méthylation ordonne les flux immunitaires
  comme ABSOLUTE.** Écart +0,6739 — au-dessus du seuil H1 (0,45), à
  97,5 % d'E-ABS (+0,6911), à 90 % de la moyenne IMMROT (+0,7521).
  MC sépare aussi (+0,0970 : 0,4204 contre 0,3234) ; Delta non (3,45
  contre 3,42, écart 0,02) — noté, non utilisé pour le verdict (le
  verdict porte sur S_sep, gelé). Le seuil est trouvé à mi-course
  (T0 = 47,82 %, contre 25,77 % pour E-ABS) : une marche moins nette
  en début de course qu'ABSOLUTE. L7a ne sépare pas dans le sens
  attendu (down 0,2017 contre up 0,1639) : L7a n'est pas utilisé ici,
  comme au §8.48/§8.51/§8.55. **Point clé : M-METH dépasse sa
  prédiction de 0,1280 (+0,6739 contre +0,5459)** — la régression
  §8.48 SOUS-estime la séparation par METH, alors qu'elle la
  prédisait bien pour ABSOLUTE (+0,6911 contre +0,6659, écart 0,025).
  L'ordonnancement par METH est plus fort que son couplage linéaire
  ne le laisse attendre.
- **M-RES : la séparation survit réduite, plus réduite que pour
  ABSOLUTE.** Écart +0,5427 contre +0,9838 pour CD8A brut (**55,2 %
  conservés, baisse de 44,8 %**) et contre +0,6499 pour E-RES (83,5 %
  d'E-RES). MC +0,0788 (0,4190 contre 0,3402) ; Delta quasi égal
  (3,41 contre 3,39). Critère gelé : M-RES < 0,70 → réduit (condition
  de H1 partielle remplie) ; M-RES ≥ 0,45 → encore séparant. **M-RES
  est 0,1505 SOUS sa prédiction (+0,5427 contre +0,6932)** — la
  régression §8.48 SURESTIME ici le résiduel, à l'inverse exact de
  M-METH. Les deux écarts à la prédiction sont de sens opposés et de
  magnitude comparable (±0,13–0,15) : la régression §8.48, calibrée
  sur les rotations IMMROT, encadre mal la méthylation — elle
  sous-estime le brut et surestime le résiduel.

## 8.61.8 Verdict de synthèse — ZONE GRISE

Règle gelée, test par test : T1'' = lien substantiel (moyenne |r|
0,4228) ; T2'' = PERSISTANCE (chute 15,9 %) ; T4'' = persistance
réduite dans les deux moitiés ; M-METH = +0,6739 (≥ 0,45) ;
M-RES = +0,5427 (< 0,70, ≥ 0,45).
**H1-meth totale est rejetée** (T2'' n'est pas un effondrement, M-RES
n'est pas < 0,30). **H1-meth partielle est rejetée par la règle
gelée** (T2'' n'est pas partielle ; M-METH n'est pas entre 0,30 et
0,45 — il est au-dessus). **H0-meth est rejetée** (M-METH n'est pas
< 0,30 — il sépare fortement). **Aucune des trois hypothèses gelées
n'est soutenue : ZONE GRISE.** Ce n'est pas un échec de mesure, c'est
le résultat : la pureté par méthylation sépare les flux presque comme
ABSOLUTE (T5''), mais ne retire que 15,9 % de la corrélation en
linéaire (T2'') — les deux voies du même chantier ne convergent pas
vers la même part.

**Ce que cela dit, et ce que cela ne dit pas.** (a) Cela dit que la
part de pureté dépend de la mesure : ~un quart en linéaire par
ABSOLUTE, ~un sixième par METH, et que la séparation par ordonnancement
est, elle, robuste aux deux mesures (+0,67 et +0,69). (b) Cela ne dit
pas que le §8.55 est faux : ses chiffres restent vrais sur ABSOLUTE,
et METH les confirme sur T5'' — c'est sur T2'' seulement que les deux
mesures divergent. Le « environ un tiers » du §8.55 reste la lecture
ABSOLUTE ; la lecture METH dirait « environ un sixième en linéaire,
un tiers en séparation ». (c) Cela ne dit pas que l'infiltration est
expliquée : aucune infiltration INDÉPENDANTE n'a été testée ici en
run — voir l'annexe leucocytes (§8.61.9), descriptive seulement.
(d) La mesure porte sur le sous-ensemble whitelisting (n = 150) ; la
brute y est déjà plus faible (0,5035 contre 0,5563 à n = 178) — la
sélection elle-même retire 0,0528 de cohésion, à ne pas confondre avec
l'effet METH (0,0800 de chute par régression, mesuré dans le même
n = 150). (e) La domination IMMROT du §8.48 n'est pas remise en cause :
elle reste expliquée par le couplage ; ce chantier en précise la cause
amont — le couplage est porté par la pureté, et la part portée dépend
de la mesure de pureté choisie.

**Comparaison directe avec le §8.51 (scores internes) et le §8.55
(ABSOLUTE) :**

| Test | §8.51 (proxys internes, n = 178) | §8.55 (ABSOLUTE, n = 149) | §8.61 (METH, n = 150) |
|---|---|---|---|
| T1 moyenne \|r\| | acineux 0,146 / îlots 0,198 | ABSOLUTE **0,4932** | METH **0,4228** |
| T1 R² médian | 0,057 | **0,3006** | **0,2224** |
| T2 brute → résiduelle | 0,5563 → 0,5480 (−1,5 %) | 0,5040 → 0,3757 (−25,5 %) | 0,5035 → 0,4235 (−15,9 %) |
| T2 verdict | PERSISTANCE | PARTIELLE | **PERSISTANCE** |
| T5 contrôle → flux | P-AC +0,0118 ; P-IS +0,2876 | E-ABS **+0,6911** | M-METH **+0,6739** |
| T5 résidualisé | P-RES +0,9174 (93,3 % du brut) | E-RES +0,6499 (66,1 %) | M-RES +0,5427 (55,2 %) |
| Verdict | H0 soutenue | **H1 partielle** | **ZONE GRISE** |

## 8.61.9 Annexe — Fraction leucocytaire par méthylation : une piste d'infiltration, descriptive seulement

La même Table S1 contient `DNA.methylation.leukocyte.percent.estimate`
(fraction leucocytaire estimée par méthylation). Par le protocole (§2),
elle est rapportée en annexe descriptive — AUCUN run, AUCUN rôle dans
le verdict. Les chiffres valent pourtant d'être nommés, parce qu'ils
désignent le prochain chantier (§8.61.10).

Corrélation de chaque flux avec la fraction leucocytaire (n = 150,
Pearson r, p brutes) : CD8A +0,660 (4,3×10⁻²⁰), CD8B +0,582, CD4
+0,614, FOXP3 +0,687 (3,1×10⁻²²), CD68 +0,220 (6,9×10⁻³), CD163
+0,483, CD274 +0,276, PDCD1 +0,704 (9,3×10⁻²⁴), CTLA4 +0,713
(1,4×10⁻²⁴), GZMB +0,581, IFNG +0,325, CD19 +0,702 (1,3×10⁻²³).
**Moyenne |r| = 0,5456 — PLUS FORTE que celle de METH (0,4228) et
d'ABSOLUTE (0,4932) avec les mêmes flux.** Les 12 corrélations sont
POSITIVES — le sens attendu : plus de leucocytes estimés, plus de
signal immunitaire. La fraction leucocytaire corrèle à r = −0,6774
avec METH et r = −0,6901 avec ABSOLUTE : elle est l'image miroir de la
pureté (pureté basse = plus de leucocytes), comme attendu.

**Lecture honnête.** Cette corrélation plus forte ne prouve pas que
l'infiltration explique la corrélation intra-famille : la fraction
leucocytaire est elle-même une mesure de composition, presque
l'inverse de la pureté (r ≈ −0,68 avec les deux puretés), et elle n'a
pas été testée en régression ni en run. Ce qu'elle dit : la prochaine
mesure à tester n'est pas une troisième pureté, c'est un score
d'infiltration indépendant des 12 gènes — déconvolution
(CIBERSORT/xCell) ou cette fraction leucocytaire elle-même en
régression + runs — pour séparer ce qui, dans la co-expression,
vient de la QUANTITÉ de cellules immunitaires de ce qui vient de leur
état. C'est le chantier jumeau qui reste ouvert depuis le §8.51.10.

## 8.61.10 Provenance

- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant les calculs, dans le log du lot, et après
  l'extraction). Mode `fast`, graine 42 (défaut), nul = lignes permutées,
  graine 42 (default_rng frais par fichier), contrôle intact.
- **Protocole.** `PROTOCOL_methylation_purity_861.md`, SHA-256
  `93f4f777f217d9a03c01b1b79397ed70e59567e53edaf4231864e9c6a50e0993`,
  gelé le 20 nov. 2026 avant tout calcul et avant tout run de ce
  chantier.
- **Entrées externes.** (1) pdacR `data/TCGA_PAAD.rds`, SHA-256
  `52020679350d1539d7516f7d38f7bf09e510225eba2f228a4fe874f3c496ea76`
  (12 311 529 octets ; URL
  `https://raw.githubusercontent.com/rmoffitt/pdacR/master/data/TCGA_PAAD.rds`,
  re-téléchargé le 20 nov. 2026 : SHA identique, taille identique) ;
  publication source Raphael et al. 2017 (PMID 28810144, PMCID
  PMC5964983, DOI 10.1016/j.ccell.2017.07.007, Table S1, colonne
  `DNA.hypermethylation.mode.purity`) ; curation Torre-Healy et
  al. 2023 (doi 10.1038/s42003-023-04461-6). (2) Aran et al. 2015 Suppl.
  Data 1 — non réutilisé ici (0 PAAD, établi au §8.55). (3) Site
  ESTIMATE (MD Anderson) — non réutilisé ici (scores PAAD non récupérés
  au §8.55).
- **Entrées du projet.** Base immunitaire `pdac_immune_tcga_fluxes.csv`,
  SHA-256 `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e` ;
  axe `immune_kras_order_tcga.csv`, SHA-256
  `31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d` ;
  sampInfo transcrit `purity_855_sampinfo.csv`, SHA-256
  `7a09dde3d374d1afb64f1d1d053193fc884c04d62e63e519fcf4dbf17378b014` ;
  écarts §8.51/§8.55 relus en machine dans `purity_851_runs.csv` et
  `purity_855_runs.json` (CD8A : réel 1,2310, nul 0,2472, écart +0,9838 ;
  E-ABS +0,6911 ; E-RES +0,6499).
- **Nature des lignes.** Les flux immunitaires sont des mesures
  instrumentales (séquençage ARN, log2(RSEM+1), brutes) ; METH et
  ABSOLUTE sont des estimations publiées depuis l'ADN (indépendantes de
  l'ARN) ; la fraction leucocytaire est une estimation publiée depuis
  la méthylation de l'ADN ; les résidus sont des valeurs calculées
  (OLS sur [1, METH]) ; les nuls sont des lignes permutées (graine 42)
  — des échantillons hypothétiques, pas des mesures. Aucun mot humain,
  aucun échantillon hypothétique dans les séries réelles.
- **Sorties et scripts de ce chantier.**
  `analyze_purity_861.py` (SHA `ebaecd20…b5bd`) : porte S, jointure,
  T1''–T4'', cohérence, annexe leucocytes.
  `build_purity_861.py` (SHA `5db9b63a…af`) : 4 CSV T5'' (résidus
  vérifiés : moyenne |r| = 0,4235, identique à T2'').
  `extract_purity_861.py` (SHA `eab8340f…e21`) : lecture des 4 runs.
  `purity_861_external.csv` (SHA `cf127ef7…d24b`, 150 tumeurs appariées),
  `purity_861_results.json` (SHA `72dc7d50…1f0`, T1''–T4'' + annexe),
  `purity_861_results.csv` (SHA `074a9db6…69`, T1'' par flux),
  `purity_861_immune_resid.csv` (SHA `10924db4…b7b`, 12 flux résidualisés),
  `purity_861_csv_sha.json` (SHA des 4 CSV T5''),
  `purity_861_runs.json` (SHA `73e1b4da…abb`) / `.csv` (SHA `efee209c…81a`,
  4 runs). Manifeste `manifest_v62_purity_861.txt`
  (SHA `b913638f…f51a`) ; log `runs_v62_purity_861.log`
  (SHA `4a61a0a6…351f`) ; surveillance `watch_v62_purity_861.sh`
  (SHA `0839b680…398`) ; unité systemd `v62-purity-861`.
- **Ce qui manque :** ESTIMATE-purity publiée pour PAAD (non récupérée,
  cf. §8.55.2) ; relecture directe de la Table S1 de Raphael (défi PMC
  non contourné — trois vérifications de cohérence à la place, §8.61.2,
  dont une limite réelle : METH ne reproduit pas la classification
  high/low publiée) ; METH et ABSOLUTE partagent la même Table S1 —
  deux mesures, une seule table, pas deux sources indépendantes ;
  les moitiés T4'' sont à n = 75/75 ; les p de T1'' sont brutes, sans
  correction pour tests multiples ; la fraction leucocytaire n'a été
  testée qu'en corrélation descriptive, jamais en régression ni en run.

## 8.61.11 Ce qui manque, ce qui reste ouvert

- **Infiltration indépendante non testée en run.** L'annexe leucocytes
  (§8.61.9) donne la piste la plus forte depuis le §8.51 : moyenne |r|
  0,5456 avec les flux, plus forte que les deux puretés. Chantier
  jumeau à geler : régression sur la fraction leucocytaire + runs
  contrôle = fraction leucocytaire → flux immunitaires, et résidus
  leucocytaires → CD8A résidualisé. C'est le test décisif manquant
  depuis le §8.51.10 — il départagerait quantité d'infiltrat et
  co-expression propre.
- **Déconvolution (CIBERSORT/xCell).** Toujours non jointe : un score
  par type cellulaire dirait si la corrélation vient d'un type
  (lymphocytes T, macrophages) ou de tous à la fois.
- **Pourquoi METH retire moins qu'ABSOLUTE en linéaire ?** Deux
  lectures non tranchées (§8.61.4) : bruit de METH (classification
  high/low non reproduite) ou facette différente de la pureté. Un
  test direct : régression conjointe [METH, cellularité pathologiste]
  ou [METH, leucocytes] — non fait ici, hors protocole gelé.
- **La régression §8.48 encadre mal METH.** Elle sous-estime M-METH
  de 0,1280 et surestime M-RES de 0,1505 — les deux écarts de sens
  opposés. La prédiction par couplage, calibrée sur IMMROT, n'est pas
  universelle : à noter pour les chantiers suivants, pas un verdict.
- **Déroulement du lot.** Aucun incident : la machine avait redémarré
  AVANT le lot (~11h24 UTC, `uptime` 32 min à 11h56), pas pendant.
  Lot 11h44:59 UTC – 12h29:47 UTC 20 nov., **4/4 exit 0, 0 échec**
  (`=== FIN 2026-11-20T12:29:47Z deja_faits=0 termines=4 echecs=0` ;
  surveillance arrêtée d'elle-même à 4/4, tour 1/12). Ralentissement
  noté : M-METH_NUL ~25 min, M-RES ~15 min — d'autres lots v6.2
  tournaient en parallèle sur la même machine partagée (2 vCPU).
- **Périmètre.** 4 nouveaux runs v6.2 au maximum (protocole §8),
  aucun autre. Aucun nouveau seuil proposé, aucun code modifié, aucun
  push GitHub dans ce chantier (publication sur go séparé ; règle
  permanente « Toujours github et pdf !!! » — par le coordinateur).

— Fin de la §8.61. —
