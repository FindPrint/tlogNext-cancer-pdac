# §8.82 — Cerveau, deuxième site à privilège immunitaire (TCGA-GBM) : les gènes de privilège DESCENDENT quand l'agressivité monte, la tumeur est froide, et la chaîne PDAC n'apparaît pas

## Verdict d'abord

**Trois verdicts, tous mesurés aujourd'hui sur les mêmes 153 tumeurs
primaires TCGA-GBM — et ils ne vont pas dans le même sens.**

1. **Tests directs — DESCEND : les 7 gènes de privilège DESCENDENT
   quand l'agressivité (score de prolifération) monte.** Médiane des
   rho de Spearman −0,287 ; 0/7 positifs ; 7/7 avec p < 0,05 (TGFB2
   −0,323, CD274 −0,350, CD47 −0,290, TGFB1 −0,287, FASLG −0,180,
   HLA-G −0,181, IDO1 −0,168). Score de privilège lui-même : rho
   −0,477 (p < 0,0001). C'est l'INVERSE de l'hypothèse de départ
   (l'œil et le pancréas suggéraient que le privilège monte avec
   l'agressivité pour cacher la tumeur) : dans le glioblastome, plus
   la tumeur prolifère, MOINS elle exprime les gènes de privilège.
2. **Froid — FROID : le glioblastome est froid comme le pancréas.**
   Médiane des rho des 4 gènes T du §8.23 (CD8A, CD4, FOXP3, PDCD1)
   −0,129 ; 4/4 négatifs ; score froid rho −0,239 (p=0,003). Mais pas
   par les mêmes gènes qu'au pancréas : ce sont CD4 (−0,365) et FOXP3
   (−0,219) qui portent la baisse, CD8A (−0,038) et PDCD1 (−0,037)
   sont plats — au pancréas, PDCD1 était le plus fort (−0,25).
   Les macrophages baissent aussi (CD68 −0,327, CD163 −0,259), alors
   qu'ils montaient faiblement au pancréas ; et CD274/PD-L1 baisse
   (−0,350), alors qu'il montait en TCGA pancréas (+0,26).
3. **Bras pipeline v6.2 — PARTIEL, fragile, non consolidé : la chaîne
   PDAC n'apparaît pas dans le GBM.** Paire primaire (ordre par
   prolifération) : `d_maxsep = +0,0283` (réel 0,2123 contre nul
   0,1840), positif mais SOUS le plancher 0,07. Les 2 nuls frais
   (graines 8821, 8822, courus parce que d était dans [−0,07 ; +0,14[)
   donnent +0,0175 et +0,0402 — les 3 écarts sont ≤ 0,07 : passage
   « fragile, non consolidé » selon la règle gelée ; le verdict de la
   paire graine 42 n'est pas changé. Paire secondaire (ordre par score
   de privilège) : `d_maxsep = +0,0116`, encore plus faible — elle ne
   sauve rien. Les tests directs en appui confirment l'absence
   d'ordre : Δρ médian −0,044 (4/12 positifs) sur la paire primaire,
   |ρ| moyen réel 0,069 contre nul 0,074.

**Ce que ces trois verdicts disent ensemble.** Le cerveau n'est pas
l'œil : le privilège immunitaire n'y monte pas avec l'agressivité, il
y descend — l'hypothèse « la tumeur copie le privilège de l'œil pour
se cacher quand elle devient agressive » ne se transfère pas au
glioblastome, en tout cas pas en ARN bulk ordonné par prolifération.
Le froid, lui, se transfère — mais avec une autre composition
cellulaire que le pancréas. Et le pipeline ne voit pas la chaîne PDAC
dans le GBM, dans aucun des deux ordres : ce n'est pas une 13e paire,
ce n'est pas un échec du pancréas, c'est un NON/PARTIEL sur un autre
cancer. C3 reste LEVÉE, le test C reste NON, l'adoption pleine de
maxsep reste la décision de Zackary du 20 nov. 13h04 ; le compte A2
(8/12, 10/12 positifs, LOO 7/11) NE CHANGE PAS.

**Fragilité, dite en tête.** Le verdict pipeline tient à une seule
paire primaire mesurée aujourd'hui, avec des écarts petits (+0,0283 ;
nuls frais +0,0175 / +0,0402) et un nul graine 42 déjà haut (0,1840).
L'axe d'agressivité est un score d'expression (prolifération), pas une
mesure clinique : le grade ne pouvait pas servir (tous les GBM sont
grade IV), le statut IDH n'est pas dans la matrice, et il n'y a pas
de correction de pureté (ARN bulk, même limite qu'au §8.23). Les
verdicts directs, eux, sont forts (7/7 gènes significatifs dans le
même sens) — c'est le contraste entre des directs solides et un
pipeline qui ne sépare pas, comme dans la plupart des bras du dossier.

Protocole gelé : `PROTOCOL_cerveau_privilege_882.md` (21 nov. 2026, SHA
`487fc59d…`, corrigé de fuseau horaire avant les runs — « 12h20 EST »
devenait « 07h20 EST (12h20 UTC) », étiquette d'horloge seulement,
aucun paramètre). Critères écrits AVANT tout run (§§4, 5, 7 du
protocole). Pipeline v6.2, SHA `f07567c4…`, vérifié avant et après le
lot, jamais modifié. 6 runs, exits 0.

## 8.82.1 — Données et axes (gelés)

- **Source :** Broad GDAC Firehose stddata 2016-01-28, TCGA-GBM, RSEM
  genes normalized — même route et même technologie que PAAD/LUAD/COAD.
  Fichier local `data/tcga_gbm_rsem.tar.gz`, MD5 `cfc6cf0a…` (égal au
  MD5 servi par le dépôt, vérifié avant le gel), SHA-256
  `9996a653…`. Matrice interne : 20 532 lignes, 20 503 gènes uniques
  après déduplication, × 171 échantillons ; tarball 14 116 395 octets,
  matrice interne 30 268 366 octets. Téléchargé le 21 nov. 2026 (la
  première URL tentée portait une coquille — `20160128` au lieu de
  `2016012800` — 404 ; l'adresse du répertoire listait le bon nom,
  avec une version normalisée, comme pour PAAD).
- **Patients :** 153 tumeurs primaires (code TCGA 01) ; 18 écartées
  (codes 02 et 11) ; 153/153 cas complets (aucune imputation).
  La mission disait « n ≈ 160 » : le nombre mesuré est 153 primaires.
- **Agressivité = score de prolifération** (moyenne log2(RSEM+1) de
  MKI67, TOP2A, PCNA, CCNB1, BUB1, AURKB) : min 5,964, médiane 9,787,
  max 11,219. Le grade NE PEUT PAS servir d'axe : tous les TCGA-GBM
  sont WHO grade IV par définition de la cohorte. Le statut IDH n'est
  pas dans la matrice RSEM et n'est pas utilisé.
- **Score de privilège** (moyenne des z-scores des 7 gènes, dans la
  cohorte) : min −1,700, médiane 0,032, max 1,580.
- **Score froid** (moyenne des z-scores de CD8A, CD4, FOXP3, PDCD1) :
  min −1,536, médiane −0,037, max 2,061.
- **Transformation :** log2(RSEM normalisé + 1), comme PAAD/LUAD/COAD.
  **Aucune correction de pureté** (scores acineux/îlots spécifiques au
  pancréas). **Anti-doublon (§8.44) :** le contrôle du pipeline est la
  colonne `step` ; ni le score de prolifération ni le score de
  privilège ne figurent parmi les 12 flux — vérifié par assertion.
- **Présence des gènes (vérifiée avant le gel) :** 7/7 privilège,
  12/12 v4, 6/6 prolifération, 12/12 immunitaires — aucun absent,
  aucun remplacement.

## 8.82.2 — Tests directs (1) : les gènes de privilège DESCENDENT

Spearman de chaque gène avec le pas de prolifération (ordre croissant),
n=153. Table complète, sans sélection. Top-quartile de prolifération
(n=39) vs reste, en écart-type (Welch p descriptive).

| Gène | rho (p) | d top-quartile (sd) | Welch p |
|---|---|---|---|
| FASLG | −0,180 (0,026) | −0,201 | 0,24 |
| TGFB1 | −0,287 (0,0003) | −0,486 | 0,007 |
| TGFB2 | −0,323 (<0,0001) | −0,763 | <0,0001 |
| IDO1 | −0,168 (0,039) | −0,441 | 0,005 |
| HLA-G | −0,181 (0,026) | −0,177 | 0,35 |
| CD47 | −0,290 (0,0003) | −0,423 | 0,018 |
| CD274/PD-L1 | −0,350 (<0,0001) | −0,722 | 0,0002 |

**Médiane rho = −0,287 ; rho > 0 : 0/7 ; p < 0,05 : 7/7. Score de
privilège vs pas : rho = −0,477 (p < 0,0001). Catégorie gelée :
DESCEND** (médiane ≤ −0,15 ET ≥ 4/7 rho < 0 — ici 7/7).

Lecture : dans le GBM, les gènes de privilège ne montent pas avec
l'agressivité — ils descendent, tous, significativement. Le gène le
plus fort est CD274/PD-L1 (−0,350), celui-là même qui montait en TCGA
pancréas (+0,26, §8.23) : le signe s'inverse entre les deux cancers.
TGFB2 (−0,323) et CD47 (−0,290) suivent. Les différences top-quartile
confirment en ampleur (TGFB2 −0,763 sd, CD274 −0,722 sd), même si deux
Welch p sont non significatives (FASLG, HLA-G) — le signal est
monotone (Spearman), pas un effet de seuil.

## 8.82.3 — Tests directs (2) : le GBM est FROID, mais pas comme le pancréas

Spearman de chacun des 12 gènes immunitaires (§8.23) avec le pas de
prolifération, n=153. Référence pancréas : TCGA / GSE71729 / GSE62452 /
ICGC, axe KRAS.

| Gène | GBM rho (p) | Pancréas TCGA (§8.23) | GBM d top-q (sd) |
|---|---|---|---|
| CD8A | −0,038 (0,64) | −0,19 | −0,064 |
| CD8B | −0,177 (0,029) | — | −0,274 |
| CD4 | −0,365 (<0,0001) | −0,15 | −0,495 |
| FOXP3 | −0,219 (0,007) | −0,10 | −0,217 |
| CD68 | −0,327 (<0,0001) | +0,07 | −0,343 |
| CD163 | −0,259 (0,001) | — | −0,359 |
| CD274/PD-L1 | −0,350 (<0,0001) | +0,26 | −0,722 |
| PDCD1/PD-1 | −0,037 (0,65) | −0,25 | +0,122 |
| CTLA4 | −0,243 (0,003) | — | −0,164 |
| GZMB | −0,244 (0,002) | — | −0,233 |
| IFNG | −0,024 (0,77) | — | +0,299 |
| CD19 | −0,184 (0,023) | −0,18 | −0,338 |

**Score froid (CD8A/CD4/FOXP3/PDCD1) vs pas : rho = −0,239 (p=0,003).
Médiane rho des 4 gènes = −0,129 ; rho < 0 : 4/4. Catégorie gelée :
FROID** (médiane ≤ −0,10 ET ≥ 3/4 négatifs).

Lecture : le froid existe — le score froid baisse quand la
prolifération monte, comme les T baissent quand KRAS monte au
pancréas. Mais la composition diffère sur trois points, dits
plainement : (a) au pancréas, PDCD1 portait la baisse (−0,25, top-12
d −0,61 à −0,88, significatif dans les 4 cohortes) ; ici PDCD1 est
plat (−0,037) et ce sont CD4 (−0,365) et FOXP3 (−0,219) qui portent
la baisse du score — CD8A est plat aussi (−0,038) ; (b) les
macrophages baissent ici (CD68 −0,327, CD163 −0,259) alors qu'au
pancréas CD68 montait faiblement (+0,07 à +0,22) ; (c) CD274 baisse
ici (−0,350) alors qu'il montait en TCGA pancréas (+0,26) — le seul
endroit où il montait. Le « froid » n'est donc pas le même paysage
cellulaire : moins de T CD4/régulateurs et moins de macrophages quand
la tumeur prolifère, sans baisse des marqueurs CD8/PD-1. En ARN bulk,
on ne distingue pas « moins de cellules » de « moins d'expression par
cellule » (même limite qu'au §8.23).

## 8.82.4 — Bras pipeline v6.2 : PARTIEL, fragile, non consolidé

Lot : 4 runs (paire primaire prolifération réel + nul ; paire
secondaire privilège réel + nul), mode fast, graine 42, contrôle
`step`, cible PGC (premier flux hors contrôle, comme partout).
Lancement en `systemd-run` (unités `v62-882` puis `v62-882-frais`),
journal `runs_v62_882.log` / `runs_v62_882_frais.log`, SHA du pipeline
revérifié avant et après : `f07567c4…`, inchangé. Extraction
`extract_882.py` (SHA `ac0aa6ec…`), vérification indépendante
`verify_882.py` (SHA `c47b94df…`) : maxsep et ancien MC recoupés à 0,0
exact sur les 4 runs (puis 6 avec les nuls frais).

| Paire | maxsep réel / nul | d_maxsep | MC réel / nul | S_sep R / N | Delta R / N | L7a R / N | Fals. R / N |
|---|---|---|---|---|---|---|---|
| Primaire (prolifération) | 0,2123 / 0,1840 | **+0,0283** | 0,3324 / 0,3283 | 0,2111 / 0,1834 | 2,848 / 2,719 | up 0,39 / up 0,20 | 0,116 / 0,037 |
| Secondaire (privilège) | 0,2175 / 0,2059 | **+0,0116** | 0,3333 / 0,3324 | 0,2170 / 0,2053 | 2,922 / 2,843 | down 0,24 / up 0,37 | 0,071 / 0,123 |
| Nuls frais (primaire) | 0,2123 / 0,1948 ; 0,1721 | +0,0175 ; +0,0402 | 0,3324 / 0,3300 ; 0,3271 | — | 2,848 / 2,861 ; 2,864 | up 0,39 / down 0,18 ; up 0,42 | 0,116 / 0,083 ; 0,122 |

Cascades (descriptives) : primaire réelle [3,1 / 60,8 / 95,1 / 98,1 /
100,0], nul [0,0 / 90,9 / 93,9 / 97,0 / 97,6] ; secondaire réelle
[4,9 / 54,3 / 59,1 / 62,7 / 62,7], nul [6,2 / 13,0 / 42,0 / 45,4 /
53,7] ; nul frais s8821 [0,0 / 1,2 / 6,8 / 29,8 / 29,8] — le nul
frais s8821 a une cascade effondrée mais un maxsep de 0,1948, plus
haut que le nul graine 42 : la cascade et maxsep ne bougent pas
ensemble, comme déjà vu au §8.76 (FNA).

**Catégorie gelée (paire primaire) : PARTIEL** (0 < d_maxsep ≤ 0,07).
**Nuls frais :** d = +0,0283 dans [−0,07 ; +0,14[, donc 2 nuls frais
courus (graines 8821, 8822) : écarts +0,0175 et +0,0402. Min / médiane /
max des 3 écarts : +0,0175 / +0,0283 / +0,0402 — les 3 sont ≤ 0,07 :
le passage est dit **« fragile, non consolidé »** (règle gelée) ; le
verdict de la paire graine 42 n'est JAMAIS changé par les nuls frais.
La paire secondaire (+0,0116) ne change rien : même en ordonnant par
le privilège lui-même, la chaîne ne sépare pas le réel du nul. Les
scores compagnons ne suivent pas non plus : MC +0,0041 (primaire) et
+0,0009 (secondaire), Delta +0,129 et +0,079 — tous sous la gigue
historique ±0,07 pour MC, et L7a est up des deux côtés sur la primaire.

**Tests directs en appui (ne décident pas) :** Spearman des 12 flux v4
contre le pas, réel vs nul (§8.70) — paire primaire : |ρ| moyen réel
0,069 contre nul 0,074, Δρ médian −0,044, Δρ positifs 4/12 (le réel
n'a pas plus d'ordre que le nul) ; paire secondaire : |ρ| moyen réel
0,080 contre nul 0,074, Δρ médian +0,050, Δρ positifs 10/12 (un petit
signal d'ordre, +0,050, sans séparation maxsep). d de Cohen marginal
réel vs nul : 0,000000 pour les 12 gènes, les 2 paires — attendu
vacueux (le nul est une permutation des lignes), il valide la
construction du nul. Comparaison descriptive au pancréas TCGA v4
(§8.56) : maxsep réel 0,4623 / nul 0,1696, d +0,2928 — le GBM
(0,2123 / 0,1840, +0,0283) est dix fois plus faible en écart, avec un
nul deux fois plus haut que le nul pancréatique.

## 8.82.5 — Ce que les verdicts disent, et ce qu'ils ne disent pas

Ils disent que le deuxième site à privilège immunitaire ne se comporte
pas comme le premier : dans le cerveau, le privilège descend quand la
tumeur devient agressive, et la chaîne PDAC n'y apparaît pas — ni
ordonnée par agressivité, ni ordonnée par privilège. Ils disent que le
froid, lui, se retrouve dans le GBM, avec une autre composition. Ils
ne disent pas que l'hypothèse de l'œil est fausse : elle est testée
au §8.81 dans l'œil lui-même, et le GBM est un autre tissu, une autre
biologie (pas de KRAS comme axe, pas de grade, pas de statut IDH dans
ce chantier). Ils ne disent rien de clinique : aucune affirmation sur
le glioblastome comme maladie, aucun remède, aucune cible — l'étude
porte sur l'instrument et sur la question posée. Ils ne rouvrent rien :
le GBM n'entre pas dans le compte A2, C3 reste levée, le test C reste
NON.

## 8.82.6 — Limites

- **Axe d'agressivité = score d'expression.** La prolifération est un
  proxy transcriptomique, pas une mesure clinique d'agressivité ; le
  grade est inutilisable (tous grade IV), l'IDH absent de ce chantier.
  Un autre axe (IDH, sous-type Verhaak, survie GBM) donnerait peut-être
  une autre réponse — ce serait un autre chantier, avec son protocole.
- **ARN bulk, sans correction de pureté** : la baisse des gènes de
  privilège avec la prolifération peut être une composition (plus de
  tumeur, moins de stroma) autant qu'une régulation — le mécanisme
  n'est pas établi, comme au §8.23.
- **Une seule cohorte, un seul axe, une seule paire par ordre** : le
  verdict pipeline tient à +0,0283 sur une paire ; les nuls frais
  confirment la fragilité, ils ne la résolvent pas.
- **Le nul graine 42 est haut** (maxsep 0,1840, contre 0,1696 en TCGA
  pancréas) et les nuls frais varient de 0,1721 à 0,1948 : à n=153, le
  plancher 0,07 reste la bonne échelle, et le réel (0,2123) n'en est
  qu'à 40 %.

## 8.82.7 — Pistes ouvertes

1. Refaire la question avec l'axe IDH (muté vs sauvage) ou les
   sous-types Verhaak (proneural / neural / classique / mésenchymateux)
   — si le privilège monte dans un sous-type agressif, la descente vue
   ici est un effet de mélange, pas une loi.
2. Tester la survie GBM des gènes de privilège (comme au §8.83 pour le
   pancréas) : ils descendent avec la prolifération, mais prédisent-ils
   la survie ? Ce serait le §8.83 du cerveau — pas fait ici.
3. Comparer œil (§8.81) et cerveau sur la même question : si l'œil
   monte et le cerveau descend, le privilège n'est pas un programme
   unique — chaque site a sa règle.

## 8.82.8 — Annexe : provenance condensée et SHAs

- Protocole : `PROTOCOL_cerveau_privilege_882.md`, SHA `487fc59d…`
  (gelé avant tout run ; correction de fuseau horaire « 12h20 EST » →
  « 07h20 EST (12h20 UTC) » avant les runs, étiquette d'horloge
  seulement).
- Provenance complète : `PROVENANCE_882.md`.
- Source : Firehose stddata 2016-01-28, GBM, RSEM genes normalized ;
  tarball MD5 `cfc6cf0a…`, SHA-256 `9996a653…` ; URL
  `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/GBM/20160128/`.
- Scripts : `build_fluxes_gbm_882.py` (SHA `dc58b600…`),
  `direct_tests_882.py` (SHA `c901496a…`), `extract_882.py` (SHA
  `ac0aa6ec…`), `verify_882.py` (SHA `c47b94df…`),
  `build_nulls_frais_882.py` (SHA `063be8c1…`).
- CSV : `pdac_882_gbm_prolif_fluxes.csv` (SHA `426375d3…`),
  `_nul.csv` (`7205fc40…`), `pdac_882_gbm_privilege_fluxes.csv`
  (`0f144663…`), `_nul.csv` (`42213249…`),
  `gbm_882_direct_table.csv` (`72f3003d…`), nuls frais s8821
  (`a76d10f1…`) et s8822 (`65ed87f7…`, SHA complets dans
  `PROVENANCE_882.md`).
- Runs : `manifest_v62_882.txt`, `runs_v62_882.log` (4/4, exits 0,
  FIN 2026-11-21T12:53:10Z) ; `manifest_v62_882_frais.txt`,
  `runs_v62_882_frais.log` (2/2, exits 0, FIN 2026-11-21T13:02:35Z).
  Dossiers `results_fast_v62_882_gbm_prolif(_nul)`,
  `results_fast_v62_882_gbm_privilege(_nul)`,
  `results_fast_v62_882_gbm_prolif_nul_s8821` / `_s8822`.
- Extraction : `extract_882.json` (SHA `c3f97591…`), `extract_882.csv`
  (SHA `3316e823…`) — 6 runs ; vérification 0,0 exact (4/4 puis 6/6).
- Pipeline v6.2 SHA `f07567c4…`, vérifié avant et après le lot,
  inchangé.
