# §8.79 — Nouvelle série indépendante, treizième paire : GSE57495 CONFIRME — après l'arrêt de la candidate GDC (DPCR1 absent de GENCODE v36)

## Verdict d'abord

**CONFIRME — la treizième paire principale indépendante, GSE57495
(n = 63 tumeurs PDAC, 11 flux, GSTM1 absent), donne
`d_maxsep = +0,4494` (réel 0,6381 contre nul 0,1887), très
au-dessus du plancher 0,07 — avec une marge de 0,3794, soit
6,4 fois le plancher, le plus grand écart `maxsep` jamais mesuré
sur une paire GEO à ce jour (devant GSE60979, +0,2045, et TCGA
v4, +0,2928). A2 devient 9/13 au-dessus du plancher, 11/13
positifs, LOO 8/12. La condition C3 du §8.59.8, levée au §8.71,
RESTE LEVÉE (ce chantier est une consolidation supplémentaire,
pas une condition ; il ne rouvre rien).**

**Et, dans la même section, l'autre moitié du verdict : la
candidate C2 (GDC ORGANOID-PANCREATIC, 55 RNA-seq) est
INUTILISABLE comme paire à 12 gènes — DPCR1 est absent de 55/55
fichiers parce que le symbole n'existe plus (Ensembl : « No
valid lookup found for symbol DPCR1 » ; HGNC : DPCR1 est
l'ancien symbole de MUCL3, présent dans 55/55 fichiers).
Aucun remappage n'a été fait, aucun CSV C2, aucun run C2. La
paire courue est donc la cohorte #2, GSE57495 — avec deux
caveats écrits avant tout run et répétés dans cette section :
paire à 11 flux (pas 12) et série déjà tenue comme holdout
direct (§8.66/§8.69, ρ=0,4377), donc JAMAIS une confirmation
indépendante de l'association KRAS–CEACAM5.**

| Porte (protocole-addendum §6, gelé) | Exigé | Mesuré 21 nov. 2026 | Sort |
|---|---|---|---|
| Treizième paire : `d_maxsep > 0,07` et positif | > 0,07 | **+0,4494** (réel 0,6381, nul 0,1887) | **CONFIRME** |
| A2 des paires indépendantes | 8/12, 10/12 positifs | **9/13, 11/13 positifs** | **ÉTENDU** |
| LOO sur 13 paires (pire cas) | 7/11 | **8/12** | **ÉTENDU** |
| Exactitude de l'extraction | 2/2 à 0,0 exact | **2/2, écart max 0,0** | **PASSE** |
| Nuls frais (§6, `d` dans [−0,07 ; +0,14[) | 2 nuls frais si proche du plancher | **Non courus : +0,4494 hors de l'intervalle** | **RÈGLE APPLIQUÉE** |
| C2 (GDC) : 12 gènes v4 présents | 12/12 | **11/12 — DPCR1 absent de 55/55** | **ARRÊT (§3)** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que
le signal `maxsep` se sépare du nul sur une treizième cohorte
indépendante — et avec la plus grande marge mesurée sur une
paire GEO : l'écart vient des deux côtés à la fois (réel
0,6381, le plus haut `maxsep` réel d'une paire GEO ; nul
0,1887, le plus bas `maxsep` nul d'une paire GEO à n ≥ 40).
Il dit aussi que le signal d'ordre est unanime (Δρ médian
+0,337, 11/11 flux positifs) et que les scores compagnons
suivent cette fois dans le même sens (`sep` passe aussi sa
barre descriptive, S_sep +0,4440 ; seul l'ancien MC reste
modeste, +0,0636, et Delta presque plat, +0,0694 — voir
§8.79.5). Il ne dit pas que `maxsep` est validé en général :
c'est une treizième paire, pas une preuve — et elle porte
deux caveats structurels (11 flux au lieu de 12 ; série déjà
utilisée comme holdout direct pour KRAS–CEACAM5, donc ce
verdict ne confirme pas cette association). Il ne dit pas
non plus que l'adoption pleine est « prouvée » par ce
chantier seul : elle a été décidée par Zackary après lecture
des §8.56/§8.59/§8.64, et cette section est la vérification
a posteriori que le protocole prévoyait — elle consolide la
décision, elle ne la fonde pas rétroactivement. Il ne dit
rien de clinique : l'étude porte sur l'instrument, pas sur
un remède — aucune affirmation sur le cancer du pancréas
n'est tirée de ce lot.

**Fragilité, dite en tête.** Le verdict tient à une seule paire
mesurée aujourd'hui — comme tous les verdicts de ce dossier.
La marge est grande (+0,3794), mais le nul est unique (graine
42) et aucun nul frais n'a été couru — la règle gelée ne
l'exige pas quand l'écart est loin du plancher, et c'est
appliqué tel quel. La paire compte 11 flux au lieu de 12 :
toute comparaison directe aux paires à 12 flux doit le
rappeler. Enfin, le `maxsep` réel le plus haut jamais mesuré
sur une paire GEO (0,6381) mérite d'être lu avec prudence :
c'est un score de séparation sur une cohorte, pas une mesure
d'effet biologique.

## 8.79.1 — Les deux cohortes : C2 arrêtée, C3 courue, et pourquoi la paire est indépendante (avec son caveat)

### La candidate C2 : GDC ORGANOID-PANCREATIC — arrêt documenté

La candidate choisie d'abord par le chantier (§8.78, C2,
FORTE) était GDC ORGANOID-PANCREATIC : 55 quantifications
RNA-seq ouvertes (STAR Counts, GENCODE v36), projet GDC
`ORGANOID-PANCREATIC` (Human Cancer Models Initiative / Next
Generation Cancer Models). Le protocole
`PROTOCOL_nouvelle_serie_879.md` a été gelé avant tout
téléchargement ; le téléchargement a ensuite réussi
intégralement : 55/55 fichiers, MD5 conformes au manifeste
(SHA `f713edebf…6220b`), total 232 648 892 o exact
(`download_gdc_879_receipt.json`).

L'association fichier → échantillon, établie par l'API GDC
avant le gel (49 cas, tous pancréas, projet
ORGANOID-PANCREATIC ; 44 fichiers = échantillons Tumor de
cas « Adenocarcinoma, NOS », 11 fichiers = échantillons
Normal de cas au diagnostic « Unknown »), donnait une
cohorte testable de 44 fichiers tumoraux, issus de 38 cas
(3 cas multi-fichiers : 2, 3 et 4 fichiers — dépendance
partielle déclarée dans le protocole, unité gelée = fichier).

**L'arrêt.** La construction des flux
(`build_fluxes_879.py`) s'est arrêtée à la porte « 12 gènes
v4 présents » : **DPCR1 est absent de 55/55 fichiers**
(0 occurrence du symbole exact, vérifié par grep sur les
55 TSV). Les 12 autres gènes utiles (11 v4 + KRAS) sont
présents dans 55/55 fichiers. La cause a été établie le jour
même :

- Ensembl REST (`lookup/symbol/homo_sapiens/DPCR1`) :
  « No valid lookup found for symbol DPCR1 ».
- Les 5 anciens identifiants Ensembl croisés pour DPCR1
  (ENSG00000168631, ENSG00000229284, ENSG00000232308,
  ENSG00000257232, ENSG00000232251) sont absents eux aussi
  du fichier GENCODE v36.
- HGNC (`fetch/symbol/MUCL3`) : **MUCL3 (HGNC:21666,
  « mucin like 3 ») porte DPCR1 en `prev_symbol`** — et
  MUCL3 est présent dans 55/55 fichiers.

Le gène est donc mesuré, sous son symbole actuel. Mais le
protocole gelé exigeait le symbole exact DPCR1 et
interdisait tout gène mappé à la main — changer la porte
après l'avoir vue échouer serait un changement de protocole
sans go. La porte dit ARRÊT (§3 du protocole C2) : **aucun
CSV C2, aucun run C2.** Les 55 TSV téléchargés et vérifiés
restent détenus pour un usage futur ; un protocole futur
pourra pré-enregistrer MUCL3 explicitement — pas celui-ci.
C'est un verdict de construction, pas un échec caché : la
raison est chiffrée (0/55) et sa cause nommée (symbole
retiré de GENCODE v36).

### La cohorte #2 : GSE57495 — 11 flux, pré-enregistrés

L'addendum `PROTOCOL_nouvelle_serie_879_C3.md` a été gelé
avant toute construction de la cohorte #2. La série est
**GSE57495**, « Development of a prognostic gene signature
in pancreatic cancer », PMID 26247463, NCBI GEO
(`https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57495`),
63 tumeurs PDAC microdisséquées congelées, plateforme
**GPL15048**. Matrice détenue localement (aucun nouveau
téléchargement) : 13 487 043 o, SHA
`995dbeff288a14c1cc1a52489e456b7677ede5da8e287069b8298d649b532efc`
(identique au §8.69), 60 608 lignes, valeurs log2 déposées
(min 1,46 / médiane 5,91 / max 15,06, 0 NaN). Mapping
GPL15048 construit au §8.69 : SHA
`93e01ec387ab710dfbfe4b7ad960a90c494b131f62637df3a4476fa9f998f952`,
60 607 lignes, 41 024 sondes avec symbole, 22 115 symboles
uniques, colonne `GeneSymbol`.

**La limitation, connue avant le gel** (donc
pré-enregistrée, pas découverte après coup) : **11/12 gènes
v4 — GSTM1 absent** (aucune sonde à symbole exact GSTM1 ;
seule la sonde partagée `merck-NM_000561_s_at`, annotée
« GSTM1 GSTM2 GSTM4 », exclue comme ambiguë ; aucune sonde
mappée à la main). KRAS présent ; 63/63 cas complets sur
11 gènes. C'est la limitation qui avait fait déclarer
GSE57495 « INUTILISABLE » au §8.69 — pour une paire à
12 gènes. Le présent chantier pré-enregistre explicitement
une paire à **11 flux** : PGC, REG4, CLDN18, MUC17, DPCR1,
CR2, KRT20, MUC2, CEACAM5, CLCA1, MUC16. La comparabilité
aux paires à 12 flux est donc limitée, et c'est dit ici
comme dans le protocole.

**Indépendance — le statut exact.** (1) Jamais courue comme
paire pipeline : aucun CSV de flux, aucun run, aucun JSON,
aucune valeur `maxsep` n'existe pour GSE57495 (§8.69 :
« INUTILISABLE — aucun CSV, aucun run »). (2) **MAIS déjà
tenue comme holdout DIRECT** (§8.66/§8.69 :
Spearman KRAS–CEACAM5 ρ=0,4377, p permutation 0,00024,
IC 95 % [0,1901, 0,6352] ; partielle après scores
acineux/îlots : 0,3521). **Elle n'est donc PAS indépendante
pour l'association KRAS–CEACAM5 et ne doit JAMAIS être
présentée comme une confirmation indépendante de cette
association.** (3) Patients distincts des cohortes tenues :
série GEO propre (63 patients, titres PDAC1..63) ; aucune
inclusion documentée dans TCGA, ICGC, GSE71729, GSE62452,
GSE62165, GSE21501, GSE79668 ou GSE131050. (4) Conséquence
gelée : la paire entre dans le compte A2 comme treizième
paire, avec 11 flux et avec son caveat holdout écrit — elle
compte pour `maxsep` (le critère gelé), elle ne compte jamais
comme confirmation indépendante de KRAS–CEACAM5.

**Construction (variante (a), 11 flux).** Sondes →
symboles par le mapping GPL15048, symboles dupliqués
agrégés par médiane (29 052 lignes dupliquées → 22 115
gènes uniques) ; ordre = KRAS croissant (log2 : min 5,44 /
médiane 7,24 / max 8,78) ; `step` = rang 0..62 ; cas
complets seulement, aucune imputation. Stades
(characteristics_ch1) : 1B:12, 2B:33, 2A:17, 1:1. Nul =
lignes permutées, graine 42, contrôle intact. CSV réel
`pdac_879_geo57495_fluxes.csv` (63 lignes, SHA
`224f98eb9cc7092e05b490b1e053edd14793e3def147890be0bab567630bb51c`) ;
nul SHA
`5cd274594a9a256142eb5fc539645e51a6dca2f0f15b2084b9884f686ab41edf`.

## 8.79.2 — Les runs et l'extraction

- Lot : 2 runs v6.2 mode fast — réel + nul — manifeste
  `manifest_v62_879_c3.txt`, lanceur reprenable
  `run_v62_lot.sh`, journal `runs_v62_879_c3.log`, unité
  systemd `v62-879c3` (leçon AGENTS.md 2026-11-17 : jamais
  nohup). **2/2 runs exit 0** (FIN 21 nov. 2026 12h43:00 UTC ;
  durées allongées par la contention CPU — d'autres lots
  v6.2 tournaient en parallèle sur la VM partagée).
- SHA du pipeline revérifié avant ET après le lot, inchangé :
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
- Extraction `extract_879_c3.py` (réutilise `extract()` de
  `extract_858.py`, original intact) : 2/2 runs, 0 manquant
  (les 2 dossiers de nuls frais sont listés « manquants »
  parce que la règle gelée ne les a pas fait courir —
  voir §8.79.4). Second calcul indépendant `verify_879_c3.py`
  (chemin de code distinct, relecture directe par
  `json.load`) recoupe `maxsep`, ancien MC et stabilité à
  0,0 exact sur les 2 runs (`maxsep_879_c3_verify.json`,
  verdict OK). Version lue :
  `v6.2.0-L7aL7b-CohenD-short` sur les 2 runs.

| Run | n | maxsep | ancien MC | S_sep | Delta | L7a | Cascade (Q1–Q5, %) |
|---|---|---|---|---|---|---|---|
| Réel GSE57495 | 63 | **0,6381** | 0,3920 | 0,6311 | 1,403 | up 0,339 | 0,0 / 36,1 / 69,7 / 85,7 / 85,7 |
| Nul graine 42 | 63 | 0,1887 | 0,3283 | 0,1872 | 1,334 | up 0,168 | 0,0 / 6,3 / 44,4 / 51,6 / 74,5 |

Valeurs complètes : `maxsep` réel 0,6381160120056911 ; nul
s42 0,1887249135434316. Stabilité : réel 0,9890 ; nul 0,9917.
Seuils MC : réel 29,03 ; nul 57,14. F1/F2 après seuil : réel
0,0014 / 0,0001 ; nul s42 0,0027 / 0,0004 (descriptif, voir
§8.79.5). Falsification : INDISPONIBLE sous n = 75 (n = 63) —
les valeurs brutes du pipeline (0,448 / 0,265) figurent dans
`extract_879_c3.json` sans être interprétées, comme aux
§8.74/§8.76. L7b : FRAGILE sur les 2 runs — l'audit L7b est
clos comme non-informatif (il dit FRAGILE sur le réel comme
sur les nuls) ; il n'est pas rapporté comme une mesure de
fragilité.

## 8.79.3 — Le verdict étendu : A2 à 9/13

Table des 13 paires principales indépendantes comptées
(valeurs des §8.56 / §8.69 / §8.70 / §8.71 / §8.74 reprises
telles quelles, jamais recalculées ; GSE57495 mesurée ici).
Écart = maxsep réel − maxsep nul. Plancher 0,07. Le lot FNA
§8.76 n'y figure PAS — il est apparié au §8.74, pas
indépendant.

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
| **GSE57495 (§8.79, 11 flux)** | **0,6381 / 0,1887** | **+0,4494** | **oui** | **oui** |

Bilan : **9/13 au-dessus du plancher, 11/13 positifs.**
LOO pire cas : retirer une paire passante donne 8/12 —
**LOO 8/12** (contre 7/11 avant cette paire). C3 du §8.59.8
RESTE LEVÉE — elle l'était depuis le §8.71 ; cette paire
est une consolidation supplémentaire, pas une condition.

## 8.79.4 — Les nuls frais : aucun, par la règle gelée

`d_maxsep = +0,4494` est hors de l'intervalle
[−0,07 ; +0,14[ qui déclenche les nuls frais (graines 8791,
8792, gelées dans l'addendum). Aucun nul frais n'est donc
couru, et le verdict reste celui de la paire graine 42. La
règle est appliquée telle quelle : un écart à 6,4 fois le
plancher n'a pas besoin de nuls frais pour être lu, et en
courir quand même serait chercher une confirmation
supplémentaire hors protocole.

## 8.79.5 — Les scores compagnons : `maxsep` passe largement, les autres suivent en partie

- **`sep` compagnon passe aussi sa barre descriptive.**
  `sep` réel 0,3895 contre nul 0,1588 : `d_sep = +0,2308`,
  au-dessus du plancher équivalent-sep
  `0,07·(1+m_R)(1+m_N) = 0,1363`. (D4 n'est pas rejoué ici :
  il porte sur les paires V1, déjà tranché.)
- **S_sep suit `maxsep` presque à l'identique.**
  S_sep réel 0,6311 contre nul 0,1872 : `+0,4440` — comme
  au §8.74, S_sep et `maxsep` racontent la même séparation
  ici (à comparer au §8.69, où les trois scores étaient
  inversés ensemble).
- **Ancien MC, positif mais modeste.** MC réel 0,3920
  contre nul 0,3283 : `+0,0636`, sous le plancher 0,07 —
  comme aux §8.70/§8.74, MC ne sépare pas seul. `maxsep`
  reste le score principal par décision de Zackary
  (20 nov. 13h04) ; MC est secondaire.
- **Delta presque plat.** Delta réel 1,403 contre nul 1,334 :
  `+0,0694` — les deux côtés sont hauts et proches, comme
  aux §8.58/§8.66 (Delta ~1,3–1,4 des deux côtés). Aucune
  divergence Delta/`maxsep` ici : Delta ne distingue pas
  le réel du nul sur cette paire, `maxsep` oui. C'est
  consigné tel quel, sans être élucidé sans preuve.
- **L7a : up des deux côtés, confiance double au réel.**
  Réel up 0,3386, nul up 0,1679. Descriptif : L7a n'est pas
  le critère gelé.
- **Cascade : le réel monte plus tôt et plus haut.** Réel
  [0,0 / 36,1 / 69,7 / 85,7 / 85,7], pas [0, 22, 43, 53,
  53] ; nul [0,0 / 6,3 / 44,4 / 51,6 / 74,5], pas [0, 4,
  28, 32, 46]. Le premier seuil (Q2) arrive au pas 22
  (36,1 %) au réel contre le pas 4 (6,3 %) au nul — le nul
  « seuille » tôt et bas, le réel tard et haut.
- **F1/F2 après seuil (descriptif).** Réel : F1 0,0014
  (ratio 0,1206), F2 0,0001 (ratio 0,0826) — les deux
  chutent après le seuil. Nul : F1 0,0027 (ratio 1,5331),
  F2 0,0004 (ratio 1,0547) — les deux montent légèrement
  après le seuil. 23 estimateurs « tous ok » des deux côtés.
  Ces ratios sont descriptifs (formulation du seuil
  critique attendu, §10 des rapports) ; ils ne décident pas.
- **Régime : `criticality` des deux côtés** (comme aux
  paires précédentes) — descriptif, pas un verdict.

## 8.79.6 — Tests directs en appui (ne décident pas)

Script `direct_tests_879_c3.py`, sur les CSV de flux du
chantier (réel + nul graine 42), 11 flux.

1. **Test informatif (correction §8.70, appliquée ici) :**
   corrélation de Spearman de chaque flux avec le pas (ordre
   KRAS), réel vs nul : |ρ| moyen réel **0,264** contre nul
   **0,109** ; **Δρ médian +0,337 ; Δρ positifs 11/11** —
   unanimité des flux dans le sens de l'ordre KRAS (à
   comparer : +0,386 et 10/12 au §8.74 ; +0,524 et 12/12 au
   §8.76 FNA). C'est le test qui porte l'information d'ordre.
2. d de Cohen marginal des 11 flux (réel vs nul) : **d =
   0,0000 pour les 11 gènes** (moyenne des |d| : 3,75×10⁻¹⁶)
   — attendu vacueux par construction : le nul est une
   permutation des lignes, chaque flux garde exactement ses
   63 valeurs. Rapporté tel quel : il valide la construction
   du nul (marginales préservées exactement), il ne mesure
   pas la séparation.

| Gène | d de Cohen | ρ réel | ρ nul | Δρ |
|---|---|---|---|---|
| PGC | +0,0000 | +0,222 | −0,142 | **+0,364** |
| REG4 | −0,0000 | +0,216 | −0,129 | **+0,345** |
| CLDN18 | −0,0000 | +0,468 | −0,059 | **+0,527** |
| MUC17 | +0,0000 | +0,350 | +0,012 | **+0,337** |
| DPCR1 | −0,0000 | +0,242 | −0,134 | **+0,376** |
| CR2 | +0,0000 | +0,038 | −0,188 | **+0,226** |
| KRT20 | −0,0000 | +0,353 | +0,116 | **+0,237** |
| MUC2 | +0,0000 | +0,202 | +0,078 | **+0,123** |
| CEACAM5 | −0,0000 | +0,438 | −0,124 | **+0,562** |
| CLCA1 | +0,0000 | +0,260 | +0,037 | **+0,223** |
| MUC16 | +0,0000 | +0,120 | −0,184 | **+0,304** |

Lecture descriptive : CEACAM5 porte le plus fort Δρ
(+0,562 ; ρ réel +0,438) — cohérent avec le holdout
direct de la même cohorte (ρ KRAS–CEACAM5 = 0,4377,
§8.69), mais ce n'est pas la même mesure (voir §8.79.7).
CLDN18 suit (+0,527). Le plus faible est MUC2 (+0,123),
toujours positif. CR2 a le ρ réel le plus faible (+0,038)
mais un Δρ positif (+0,226) parce que son ρ nul est
négatif (−0,188). Aucun de ces tests ne change le verdict
du §6.

## 8.79.7 — Comparaison descriptive avec le holdout direct : mêmes 63 tumeurs, autre mesure

Le holdout direct (§8.66/§8.69) et la paire pipeline
portent sur les **mêmes 63 tumeurs** de GSE57495, mais ne
mesurent pas la même chose :

| Mesure | Holdout direct (§8.69) | Paire pipeline (§8.79) |
|---|---|---|
| Objet | Corrélation KRAS–CEACAM5 (un gène) | Rupture multi-flux (11 gènes, ordre KRAS) |
| Résultat | ρ = 0,4377, p permut. 0,00024, IC 95 % [0,1901, 0,6352] ; partielle 0,3521 | `d_maxsep = +0,4494` (réel 0,6381, nul 0,1887) |
| Statut | Association directe, déjà tenue | Treizième paire, jamais courue avant |

Aucune des deux lectures ne valide l'autre : une
corrélation forte sur un gène n'implique pas une rupture
multi-flux, et une rupture multi-flux ne prouve pas
l'association sur un gène. Le fait que CEACAM5 porte le
plus fort Δρ (+0,562) dans la paire est cohérent avec le
holdout, pas une confirmation de celui-ci — et le verdict
de la paire ne doit jamais être cité comme une confirmation
indépendante de KRAS–CEACAM5. Cette distinction est le
caveat central de la paire, et elle est écrite ici pour
qu'aucune lecture future ne la confonde.

## 8.79.8 — Ce que le verdict dit, et ce qu'il ne dit pas

Il dit que `maxsep` sépare le réel du nul sur une treizième
cohorte indépendante, avec la plus grande marge GEO mesurée
à ce jour, et que le signal d'ordre est unanime (11/11).
Il dit aussi que la candidate GDC, pourtant la plus forte
de l'inventaire §8.78, est inutilisable comme paire à
12 gènes pour une raison d'annotation (DPCR1 retiré de
GENCODE v36, devenu MUCL3) — une leçon de provenance :
un symbole de gène n'est pas un invariant, et une cohorte
RNA-seq récente peut perdre un flux de la v4 par simple
renommage. Il ne dit pas que `maxsep` est validé en
général, ni que GSE57495 confirme KRAS–CEACAM5 (elle ne
le peut pas — elle est le holdout lui-même). Il ne dit rien
de clinique.

## 8.79.9 — Pistes ouvertes

| Pistes ouvertes | Oui, une de moins | (a) La confirmation indépendante C3 est close depuis le §8.71 — cette treizième paire est une consolidation supplémentaire, pas une condition ; (b) la candidate C1 (Chen et al. 2025, 46 PDO × 63 AUC, supplément MOESM13 SHA vérifié `0e009cd5…`) reste la piste suivante pour un lot drogue v6.2 (cible Gemcitabine, 62 contrôles) — elle ne peut pas devenir une paire A2 ; (c) la candidate C2 (GDC ORGANOID-PANCREATIC) reste utilisable sous un protocole futur qui pré-enregistrerait MUCL3 à la place de DPCR1 — les 55 TSV vérifiés sont détenus ; (d) la candidate C4 (GSE194249) attend toujours son re-audit depuis GEO (n réponse exact, couverture v4) ; (e) la fragilité du nul à petit n (§8.70, §8.53) reste un chantier propre ouvert — ici 1 seul nul, aucune étendue mesurée ; (f) la question ouverte nouvelle : pourquoi le `maxsep` réel de GSE57495 (0,6381) est-il le plus haut d'une paire GEO alors que son nul (0,1887) est le plus bas — effet de cohorte, de plateforme (GPL15048), ou du flux manquant (GSTM1) — aucune décomposition ne tranche ici. |

## 8.79.10 — Annexe : provenance condensée et SHAs

- **Cohorte courue :** GSE57495, PMID 26247463, GPL15048,
  63 tumeurs PDAC. Matrice
  `data/GSE57495_series_matrix.txt.gz` (13 487 043 o, SHA
  `995dbeff288a14c1cc1a52489e456b7677ede5da8e287069b8298d649b532efc`) ;
  mapping `data/GPL15048_probe2symbol.tsv` (SHA
  `93e01ec387ab710dfbfe4b7ad960a90c494b131f62637df3a4476fa9f998f952`).
- **Cohorte arrêtée :** GDC ORGANOID-PANCREATIC, manifeste SHA
  `f713edebf0f8afb20305b1472d480564e45ac31ce79e28350d7dde6ae496220b` ;
  55/55 fichiers MD5 OK, total 232 648 892 o ;
  DPCR1 absent 0/55 ; Ensembl « No valid lookup found for
  symbol DPCR1 » ; HGNC MUCL3 (HGNC:21666), prev_symbol
  DPCR1, présent 55/55.
- **Pipeline :** v6.2, SHA
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
  vérifié avant et après le lot.
- **Protocoles gelés :** `PROTOCOL_nouvelle_serie_879.md`
  (C2, SHA `84b1adfa36503c9e5cc2bd11853b725d183706d9215e853b1f8af3c020e27538`) ;
  `PROTOCOL_nouvelle_serie_879_C3.md` (C3, addendum, SHA
  `a4399737d105af6b9ff2fc9906fad4bfe23bb6d941508119e762f38509ce3d01`).
- **Provenance complète :** `PROVENANCE_879.md`.
- **CSV de flux :** réel SHA
  `224f98eb9cc7092e05b490b1e053edd14793e3def147890be0bab567630bb51c` ;
  nul (graine 42) SHA
  `5cd274594a9a256142eb5fc539645e51a6dca2f0f15b2084b9884f686ab41edf`.
- **Runs :** `results_fast_v62_879_geo57495` et
  `results_fast_v62_879_geo57495_nul`, 2/2 exit 0, FIN 21
  nov. 2026 12h43:00 UTC. Extraction `extract_879_c3.json` /
  `.csv` ; vérification `maxsep_879_c3_verify.json`
  (2/2, écart max 0,0, verdict OK) ; tests directs
  `direct_tests_879_c3.json`.
- **Scripts :** `build_fluxes_879.py` (C2, arrêt),
  `build_fluxes_879_c3.py`, `download_gdc_879.py`,
  `extract_879_c3.py`, `verify_879_c3.py`,
  `direct_tests_879_c3.py` (SHAs consignés dans le rapport
  de livraison).
- **Verdict :** CONFIRME, `d_maxsep = +0,4494`
  (0,6381160120056911 − 0,1887249135434316). A2 : **9/13,
  11/13 positifs, LOO 8/12.** C3 reste levée.

— Fin de la §8.79. —
