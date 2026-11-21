# §8.85 — GDC ORGANOID-PANCREATIC avec remappage DPCR1 → MUCL3 : quatorzième paire CONFIRME, fragile et non consolidée (21 novembre 2026)

Piste 2 du lot du 21 nov. 2026 ; protocole gelé 21 nov. 2026
~08h55 EST avant toute vérification de remappage, toute
construction et tout run (`PROTOCOL_gdc_mucl3_885.md`, SHA
`2dfeeade…79cdf`) ; provenance `PROVENANCE_885.md`, SHA
`fe26f4e0…69f2b`. Cette section exécute la piste ouverte du
§8.79.9 (c) : la candidate GDC, arrêtée au §8.79 parce que
DPCR1 était absent de GENCODE v36, est courue ici avec son
symbole actuel MUCL3, pré-enregistré explicitement.

## Verdict d'abord

**CONFIRME, FRAGILE ET NON CONSOLIDÉ — la quatorzième paire
principale indépendante, GDC ORGANOID-PANCREATIC (n = 44
organoïdes tumoraux, 12 flux dont MUCL3 ex-DPCR1), donne
`d_maxsep = +0,0884` (réel 0,2542 contre nul 0,1658), au-dessus
du plancher 0,07 — avec une marge de 0,0184 seulement, soit
1,3 fois le plancher. A2 devient 10/14 au-dessus du plancher,
12/14 positifs, LOO 9/13. La condition C3 du §8.59.8, levée au
§8.71, RESTE LEVÉE (ce chantier est une consolidation
supplémentaire, pas une condition ; il ne rouvre rien).**

**Et, dans la même phrase, la fragilité : l'écart est dans
l'intervalle [−0,07 ; +0,14[ qui déclenche les nuls frais, et
les 2 nuls frais courus selon la règle gelée ne confirment
pas le passage ensemble — `d_maxsep` contre le nul frais
s8851 n'est que +0,0376 (sous le plancher), contre +0,0936
pour s8852. Les 3 écarts sont +0,0376 / +0,0884 / +0,0936
(min / médiane / max) : 2 sur 3 au-dessus du plancher, 1 en
dessous. Le verdict de la paire graine 42 (CONFIRME) n'est
JAMAIS changé par les nuls frais (règle gelée) — mais le
passage est dit « fragile, non consolidé », et c'est écrit
dans le verdict lui-même, pas en note de bas de page.**

| Porte (protocole §6/§8, gelé) | Exigé | Mesuré 21 nov. 2026 | Sort |
|---|---|---|---|
| Remappage DPCR1 → MUCL3 vérifié (R1–R5) | 5/5 portes | **5/5 — HGNC, Ensembl, NCBI, TSV** | **TIENT** |
| Quatorzième paire : `d_maxsep > 0,07` et positif | > 0,07 | **+0,0884** (réel 0,2542, nul 0,1658) | **CONFIRME** |
| Marge au-dessus du plancher | — | **+0,0184** (1,3 × le plancher) | **ÉTROITE** |
| Nuls frais (§8, `d` dans [−0,07 ; +0,14[) | 2 nuls frais | **+0,0376 / +0,0936** (2/3 > 0,07) | **FRAGILE, NON CONSOLIDÉ** |
| A2 des paires indépendantes | 9/13, 11/13 positifs | **10/14, 12/14 positifs** | **ÉTENDU** |
| LOO sur 14 paires (pire cas) | 8/12 | **9/13** | **ÉTENDU** |
| Exactitude de l'extraction | 4/4 à 0,0 exact | **4/4, écart max 0,0** | **PASSE** |
| 12 flux présents dont MUCL3, DPCR1 absent | 12/12, 0 DPCR1 | **12/12, DPCR1 0/44, MUCL3 ENSG00000168631.13** | **PASSE** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que
le signal `maxsep` se sépare du nul sur une quatorzième
cohorte indépendante — la première cohorte d'organoïdes du
projet, et la première paire rendue possible par un remappage
de nomenclature vérifié — mais avec une marge de 0,0184
seulement, la deuxième plus petite marge passante du compte
A2 (derrière GSE131050, +0,0039), et avec un nul frais qui
l'annule presque (+0,0376). Il dit aussi que le signal d'ordre direct est
faible (Δρ médian +0,088, 8/12 flux positifs — voir §8.85.6) :
`maxsep` sépare ici sans que les flux individuels montrent
une tendance monotone forte — la séparation vient d'une
rupture multi-flux, pas d'un gradient par flux. Il ne dit pas
que `maxsep` est validé en général : c'est une quatorzième
paire, fragile, pas une preuve. Il ne dit pas que l'adoption
pleine est « prouvée » par ce chantier seul : elle a été
décidée par Zackary après lecture des §8.56/§8.59/§8.64, et
cette section est la vérification a posteriori que le
protocole prévoyait — elle consolide la décision, elle ne la
fonde pas rétroactivement. Il ne dit rien de clinique :
l'étude porte sur l'instrument, pas sur un remède — aucune
affirmation sur le cancer du pancréas n'est tirée de ce lot.

**Fragilité, dite en tête.** Le verdict tient à une seule paire
mesurée aujourd'hui, avec une marge de 0,0184 — plus petite
que l'étendue des `maxsep` nuls mesurés ici (0,1606 à 0,2166,
étendue 0,0560). Un seul tirage de nul sur trois suffit à
faire passer l'écart sous le plancher. C'est la fragilité du
nul à petit n (§8.53, §8.70), mesurée ici en direct, pas
supposée. La paire compte 12 flux, mais l'un d'eux porte un
nom changé en 2018 (MUCL3 ex-DPCR1) : toute comparaison aux
paires à 12 flux doit le rappeler. Enfin, le test direct
d'ordre est faible alors que `maxsep` passe — cette divergence
est consignée telle quelle au §8.85.6, sans être élucidée sans
preuve.

## 8.85.1 — Le remappage vérifié, la cohorte, et pourquoi la paire est indépendante

### Le remappage DPCR1 → MUCL3 : cinq portes, cinq passages

Le §8.79 s'était arrêté parce que DPCR1 n'existe plus comme
symbole (Ensembl : « No valid lookup found for symbol
DPCR1 ») et que son protocole gelé interdisait tout gène
mappé à la main. Le présent protocole pré-enregistre
explicitement le remappage et exige sa vérification par des
sources nommées et lues, avant toute construction. Les cinq
portes (§3 du protocole) ont été vérifiées le 21 nov. 2026
(~13h57 UTC), réponses brutes conservées dans le chantier :

- **R1 — HGNC, symbole actuel :**
  `https://rest.genenames.org/fetch/symbol/MUCL3` :
  **symbol MUCL3, HGNC:21666, name « mucin like 3 », status
  Approved, prev_symbol ['DPCR1']**, prev_name ['diffuse
  panbronchiolitis critical region 1'], alias_symbol ['PBLT',
  'bCX105N19.6', 'C6orf37'], ensembl_gene_id ENSG00000168631,
  entrez_id 135656, location 6p21.33, **date_symbol_changed
  2018-03-19**. Le nom a changé en 2018 — DPCR1 est l'ancien
  symbole, pas un synonyme courant.
- **R2 — HGNC, recherche par ancien symbole :**
  `https://rest.genenames.org/fetch/prev_symbol/DPCR1` :
  **numFound = 1, un seul résultat — le même enregistrement
  (HGNC:21666, MUCL3)**. DPCR1 n'est le symbole approuvé
  actuel d'aucun autre gène.
- **R3 — NCBI RefSeq, corroboration :** RefSeq Gene MUCL3
  (NM_080870.4, Validated) : **Synonyms: C6orf37,DPCR1,PBLT ;
  HGNC 21666 ; Entrez Gene 135656 ; chr6:30940973-30954221**
  — coordonnées identiques à l'enregistrement Ensembl MUCL3.
  Corroborations par recherche : GeneCards MUCL3 (« Prev.
  Symbol: DPCR1 »), Broad GPP (« Gene: Human MUCL3
  (135656) »). GTEx V8 utilise encore DPCR1 comme symbole
  pour ENSG00000168631 — confirmation indépendante que DPCR1
  désignait ce même gène Ensembl.
- **R4 — Ensembl :** MUCL3 résout
  (`id ENSG00000168631`, description « mucin like 3
  [Source:HGNC Symbol;Acc:HGNC:21666] », GRCh38, chr 6,
  30940973–30954221) ; DPCR1 ne résout pas
  (« No valid lookup found for symbol DPCR1 », comme au
  §8.79).
- **R5 — Croisement avec les données détenues :** la ligne
  `gene_name = MUCL3` des TSV GDC porte le `gene_id`
  **ENSG00000168631.13** dans **55/55 fichiers** ; DPCR1 :
  **0 occurrence** dans 55/55 fichiers.

**Le remappage tient.** Une seule chose est autorisée : lire
la ligne MUCL3 comme la mesure du flux v4 historiquement
nommé DPCR1. Le flux est nommé **MUCL3 (ex-DPCR1)** partout —
jamais « DPCR1 » seul. Aucun autre gène n'est mappé à la
main.

### La cohorte : GDC ORGANOID-PANCREATIC, 44 organoïdes tumoraux

La candidate est celle du §8.79 (C2, FORTE) : 55
quantifications RNA-seq ouvertes (STAR Counts, GENCODE v36),
projet GDC `ORGANOID-PANCREATIC` (Human Cancer Models
Initiative / Next Generation Cancer Models). **Aucun nouveau
téléchargement dans ce chantier** : les 55 TSV sont détenus
depuis le §8.79 et ont été re-vérifiés avant construction —
**MD5 55/55 conformes au manifeste** (SHA
`f713edebf…6220b`), **SHA-256 55/55 conformes au reçu
§8.79**, total **232 648 892 o exact**.

L'association fichier → échantillon (API GDC, §8.79) donne
**44 fichiers Tumor** (38 cas, diagnostic « Adenocarcinoma,
NOS » ; 3 cas multi-fichiers : 2, 3 et 4 fichiers — 9 lignes
sur 44, dépendance partielle déclarée, unité gelée =
fichier) et **11 fichiers Normal exclus** (cas 61–71,
diagnostic « Unknown »). L'agrégation par cas donnerait
n = 38, sous le minimum v6.2 fast (40) — elle n'est donc pas
le repli.

**Construction (variante (a), 12 flux).** Valeurs
`tpm_unstranded` telles que fournies par GDC, sans
renormalisation, sans transformation log, sans imputation.
Flux : PGC, REG4, CLDN18, MUC17, **MUCL3 (ex-DPCR1)**, CR2,
KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16. Contrôle : KRAS
(TPM : min 11,92 / médiane 31,83 / max 165,1) ; `step` =
rang 0..43. Cas complets : 44/44, 0 NaN. Portes §6 : 10/10
OK — dont MUCL3 `gene_id = ENSG00000168631.13` dans 44/44
et DPCR1 absent de 44/44. CSV réel
`pdac_885_gdc_organoid_fluxes.csv` (SHA
`a83b9817…45eaf`) ; nul graine 42 (SHA `c3f8399c…ed12e`).

**Indépendance — le statut exact.** (1) Jamais courue comme
paire pipeline : aucun CSV, aucun run, aucun JSON, aucune
valeur `maxsep` n'existait pour GDC ORGANOID-PANCREATIC
avant ce chantier. (2) Patients distincts par construction
de programme (UUID GDC / `submitter_id` entiers vs barres
TCGA, GSM GEO, ICGC) — limite déclarée : aucun identifiant
commun n'existe entre les systèmes, donc pas de preuve par
jointure. (3) Grep du livre blanc §8.1–§8.83 :
« ORGANOID-PANCREATIC » 14 mentions, « MUCL3 » 8 mentions,
toutes au §8.79 (arrêt C2 + piste ouverte (c)) — la seule
antériorité est la piste qui autorise ce chantier. (4) Le
remappage ne crée pas une dépendance : MUCL3 est le symbole
actuel du même gène ; aucune autre cohorte du projet n'a
utilisé MUCL3 comme flux. (5) Statut : transversale, ordonnée
par KRAS — même statut que TCGA/ICGC, pas de pseudo-temps ;
des organoïdes dérivés de patients, pas des tumeurs primaires
directes — le verdict porte sur l'instrument.

## 8.85.2 — Les runs et l'extraction

- Lot : 4 runs v6.2 mode fast — réel + nul graine 42, puis
  2 nuls frais (graines 8851, 8852) selon la règle gelée —
  manifeste `manifest_v62_885.txt` + `manifest_v62_885_frais.txt`,
  lanceur reprenable `run_v62_lot.sh`, unités systemd
  `v62-885` et `v62-885frais` (leçon AGENTS.md 2026-11-17 :
  jamais nohup). **4/4 runs exit 0** (FIN 21 nov. 2026
  14h04:35Z pour la paire, 14h14:19Z pour les nuls frais ;
  durées allongées par la contention CPU — d'autres lots
  v6.2 tournaient en parallèle sur la VM partagée).
- SHA du pipeline revérifié avant ET après les lots, inchangé :
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
- Extraction `extract_885.py` (réutilise `extract()` de
  `extract_858.py`, original intact) : 4/4 runs, 0 manquant.
  Second calcul indépendant `verify_885.py` (chemin de code
  distinct, relecture directe par `json.load`) recoupe
  `maxsep`, ancien MC et stabilité à **0,0 exact sur les
  4 runs** (`maxsep_885_verify.json`, verdict OK). Version
  lue : `v6.2.0-L7aL7b-CohenD-short` sur les 4 runs. Second
  calcul indépendant des écarts `d_maxsep` depuis les
  `master_results.json` : +0,0884 / +0,0376 / +0,0936,
  identiques à l'extraction (écart < 1e-15).

| Run | n | maxsep | ancien MC | S_sep | Delta | L7a | Cascade (Q1–Q5, %) |
|---|---|---|---|---|---|---|---|
| Réel GDC organoid | 44 | **0,2542** | 0,3880 | 0,2496 | 1,468 | up 0,337 | 41,0 / 72,5 / 79,4 / 84,0 / 95,4 |
| Nul graine 42 | 44 | 0,1658 | 0,3766 | 0,1649 | 1,229 | up 0,348 | 0,0 / 20,3 / 27,0 / 33,9 / 33,9 |
| Nul frais s8851 | 44 | 0,2166 | 0,3841 | 0,2147 | 0,734 | up 0,339 | 13,5 / 31,7 / 61,3 / 67,9 / 67,9 |
| Nul frais s8852 | 44 | 0,1606 | 0,3731 | 0,1579 | 1,027 | up 0,363 | 0,0 / 13,5 / 77,1 / 84,0 / 84,0 |

Valeurs complètes : `maxsep` réel 0,2542142849980612 ; nul
s42 0,1657676706638558 ; s8851 0,2165939226122164 ; s8852
0,1605986015484797. Stabilité : réel 0,9818 ; nul 0,9948 ;
s8851 0,9912 ; s8852 0,9833. Seuils MC : réel 40,91 ; nul
59,09 ; s8851 45,45 ; s8852 59,09. Pas de cascade : réel
[18, 31, 34, 36, 41] ; nul [0, 9, 12, 15, 15] ; s8851
[6, 14, 26, 29, 29] ; s8852 [0, 6, 33, 36, 36]. F1/F2 après
seuil : réel 0,3218 / 0,5852 ; nul 1,7323 / 0,6137 ; s8851
0,6370 / 0,6379 ; s8852 2,3393 / 3,8567 (descriptif, voir
§8.85.5). Falsification : INDISPONIBLE sous n = 75 (n = 44) —
les valeurs brutes du pipeline (1,517713 / 1,409825 /
1,801595 / 1,552522) figurent dans `extract_885.json` sans
être interprétées, comme aux §8.74/§8.76/§8.79. L7b :
FRAGILE sur les 4 runs — l'audit L7b est clos comme
non-informatif (il dit FRAGILE sur le réel comme sur les
nuls) ; il n'est pas rapporté comme une mesure de fragilité.
Régime : `criticality` pour le réel et le nul s42,
`saturation` pour les 2 nuls frais. Estimateurs « tous ok » :
22 (réel), 23 (nul), 22, 22 (frais).

## 8.85.3 — Le verdict étendu : A2 à 10/14

Table des 14 paires principales indépendantes comptées
(valeurs des §8.56 / §8.69 / §8.70 / §8.71 / §8.74 / §8.79
reprises telles quelles, jamais recalculées ; GDC
ORGANOID-PANCREATIC mesurée ici). Écart = maxsep réel −
maxsep nul. Plancher 0,07. Le lot FNA §8.76 n'y figure PAS —
il est apparié au §8.74, pas indépendant.

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
| **GDC ORGANOID-PANCREATIC (§8.85, 12 flux, MUCL3 ex-DPCR1)** | **0,2542 / 0,1658** | **+0,0884** | **oui** | **oui** |

Bilan : **10/14 au-dessus du plancher, 12/14 positifs.**
LOO pire cas : retirer une paire passante donne 9/13 —
**LOO 9/13** (contre 8/12 avant cette paire). C3 du §8.59.8
RESTE LEVÉE — elle l'était depuis le §8.71 ; cette paire
est une consolidation supplémentaire, pas une condition.

## 8.85.4 — Les nuls frais : passage fragile, non consolidé

`d_maxsep = +0,0884` est dans l'intervalle [−0,07 ; +0,14[
qui déclenche les nuls frais (graines 8851, 8852, gelées
dans le protocole, jamais utilisées dans ce projet). Les
2 nuls frais ont donc été construits par la même méthode et
courus en runs frais, comme la règle gelée l'exige :

| Écart contre | maxsep nul | `d_maxsep` | > 0,07 ? |
|---|---|---|---|
| Nul graine 42 (verdict) | 0,1658 | **+0,0884** | oui |
| Nul frais s8851 | 0,2166 | **+0,0376** | NON |
| Nul frais s8852 | 0,1606 | **+0,0936** | oui |

Écarts min / médiane / max : **+0,0376 / +0,0884 / +0,0936**.
2 sur 3 au-dessus du plancher. Lecture gelée : l'un des 3
écarts est ≤ 0,07 — le passage est donc dit **« fragile,
non consolidé »**. Le verdict de la paire graine 42
(CONFIRME) n'est JAMAIS changé par les nuls frais, et il ne
l'est pas ici. Mais la marge (+0,0184) est plus petite que
l'étendue des `maxsep` nuls mesurés (0,1606 à 0,2166,
étendue 0,0560) : le tirage du nul décide presque à lui seul
si cette paire passe ou non. C'est la fragilité du nul à
petit n (§8.53, §8.70), mesurée ici en direct sur 3 tirages —
et c'est la première fois, sur une paire passante avec nuls
frais, qu'un nul frais passe sous le plancher : le §8.50
avait montré 10/10 au-dessus du plancher (min +0,1110) et
le §8.74 une consolidation 3/3 (+0,0976 et +0,1113). Le
libellé « fragile, non consolidé » existait déjà au §8.70,
pour le cas miroir — une paire PARTIEL (+0,0567) dont les
deux nuls frais passaient (+0,0890 et +0,1538) ; ici c'est
l'inverse : la paire graine 42 passe et un nul frais échoue.

## 8.85.5 — Les scores compagnons : `maxsep` passe seul, les autres divergent

- **`sep` compagnon ne passe PAS sa barre descriptive.**
  `sep` réel 0,2027 contre nul 0,1422 : `d_sep = +0,0605`,
  sous le plancher équivalent-sep
  `0,07·(1+m_R)(1+m_N) = 0,1023`. (D4 n'est pas rejoué ici :
  il porte sur les paires V1, déjà tranché.) Au §8.79, `sep`
  passait aussi sa barre ; ici il ne passe pas — comme au
  §8.74, où `maxsep` passait (+0,0739) sans que `sep` suive
  sa barre (écart `sep` 0,0448 contre 0,1155 exigé).
- **S_sep suit `maxsep` presque à l'identique, et partage sa
  fragilité.** S_sep réel 0,2496 contre nul 0,1649 :
  `+0,0847` ; contre les nuls frais : +0,0349 (s8851) et
  +0,0917 (s8852) — même lecture que `maxsep` : 2/3
  au-dessus du plancher.
- **Ancien MC, positif mais minuscule.** MC réel 0,3880
  contre nul 0,3766 : `+0,0113`, très sous le plancher 0,07 —
  comme aux §8.70/§8.74/§8.79, MC ne sépare pas seul. Les
  nuls frais sont à 0,3841 et 0,3731 : le réel ne dépasse
  s8851 que de 0,0039. `maxsep` reste le score principal
  par décision de Zackary (20 nov. 13h04) ; MC est secondaire.
- **Delta : écart réel–nul positif, mais dans l'étendue
  nulle.** Delta réel 1,468 contre nul 1,229 : `+0,2387` —
  mais les nuls frais sont à 0,734 et 1,027 : Delta varie de
  0,734 à 1,229 entre les trois nuls (étendue 0,495), soit
  deux fois l'écart réel–nul. Aucune divergence
  Delta/`maxsep` à élucider ici : Delta ne distingue pas le
  réel du nul sur cette paire de façon stable, `maxsep`
  oui — et cette instabilité de Delta entre nuls est
  consignée telle quelle.
- **L7a : up des quatre côtés, sans écart.** Réel up 0,3372,
  nul up 0,3476, s8851 up 0,3391, s8852 up 0,3633 — le nul
  s42 et le nul frais s8852 sont au-dessus du réel.
  Descriptif : L7a n'est pas le critère gelé.
- **Cascade : le réel monte plus tôt et plus haut que le nul
  s42, mais les nuls frais montent aussi.** Réel
  [41,0 / 72,5 / 79,4 / 84,0 / 95,4], pas [18, 31, 34, 36,
  41] — le premier seuil (Q1) est déjà à 41,0 %, au pas 18 ;
  nul s42 [0,0 / 20,3 / 27,0 / 33,9 / 33,9], pas
  [0, 9, 12, 15, 15]. Mais le nul frais s8852 atteint
  77,1 % dès Q3 (pas 33) et 84,0 % en Q4–Q5 : à n = 44, un
  nul peut monter presque aussi haut que le réel. La cascade
  ne sépare pas seule ici.
- **F1/F2 après seuil (descriptif).** Réel : F1 0,3218,
  F2 0,5852 — les deux chutent après le seuil. Nul s42 :
  F1 1,7323 (monte), F2 0,6137 (chute). Nuls frais : s8851
  0,6370 / 0,6379 (chutent), s8852 2,3393 / 3,8567
  (montent fortement). Ces ratios sont descriptifs ; ils ne
  décident pas.
- **Régime : `criticality` pour le réel et le nul s42,
  `saturation` pour les 2 nuls frais** — descriptif, pas un
  verdict.

## 8.85.6 — Tests directs en appui (ne décident pas)

Script `direct_tests_885.py`, sur les CSV de flux du
chantier (réel + nul graine 42), 12 flux.

1. **Test informatif (correction §8.70, appliquée ici) :**
   corrélation de Spearman de chaque flux avec le pas (ordre
   KRAS), réel vs nul : |ρ| moyen réel **0,124** contre nul
   **0,131** ; **Δρ médian +0,088 ; Δρ positifs 8/12** —
   loin de l'unanimité du §8.79 (+0,337, 11/11) et du §8.74
   (+0,386, 10/12). C'est le test qui porte l'information
   d'ordre — et ici il est faible.
2. d de Cohen marginal des 12 flux (réel vs nul) : **d =
   0,0000 pour les 12 gènes** (moyenne des |d| : 3,50×10⁻¹⁷,
   maximum 1,17×10⁻¹⁶) — attendu vacueux par construction :
   le nul est une permutation des lignes, chaque flux garde
   exactement ses 44 valeurs. Rapporté tel quel : il valide
   la construction du nul (marginales préservées exactement),
   il ne mesure pas la séparation.

| Gène | d de Cohen | ρ réel | ρ nul | Δρ |
|---|---|---|---|---|
| PGC | +0,0000 | +0,003 | −0,019 | **+0,022** |
| REG4 | −0,0000 | +0,011 | −0,121 | **+0,132** |
| CLDN18 | −0,0000 | −0,120 | +0,059 | −0,179 |
| MUC17 | +0,0000 | +0,044 | −0,057 | **+0,101** |
| MUCL3 (ex-DPCR1) | +0,0000 | +0,023 | −0,168 | **+0,192** |
| CR2 | +0,0000 | −0,213 | +0,093 | −0,306 |
| KRT20 | −0,0000 | +0,135 | −0,505 | **+0,640** |
| MUC2 | −0,0000 | +0,141 | +0,067 | **+0,075** |
| GSTM1 | +0,0000 | −0,198 | −0,086 | −0,112 |
| CEACAM5 | −0,0000 | +0,106 | −0,150 | **+0,256** |
| CLCA1 | +0,0000 | −0,169 | +0,110 | −0,279 |
| MUC16 | +0,0000 | +0,326 | −0,138 | **+0,464** |

Lecture descriptive : le plus fort Δρ est KRT20 (+0,640),
mais il est porté par le nul, pas par le réel — ρ nul
−0,505 (forte corrélation négative fortuite du nul graine
42 sur ce flux), ρ réel seulement +0,135. Le seul flux avec
une tendance réelle substantielle est MUC16 (ρ réel +0,326,
Δρ +0,464) ; CEACAM5 suit (+0,256, ρ réel +0,106). Quatre
flux descendent avec KRAS (CR2 −0,213, GSTM1 −0,198, CLCA1
−0,169, CLDN18 −0,120). MUCL3 lui-même est plat (ρ réel
+0,023, Δρ +0,192 porté par un ρ nul négatif, −0,168).
**Divergence à consigner : `maxsep` passe (+0,0884) alors
que le signal d'ordre direct est faible (Δρ médian +0,088,
|ρ| réel 0,124 ≈ |ρ| nul 0,131).** La séparation `maxsep`
vient ici d'une rupture multi-flux, pas d'un gradient
monotone par flux — et c'est dit tel quel, sans être élucidé
sans preuve. Aucun de ces tests ne change le verdict du §8.

## 8.85.7 — Comparaison descriptive avec le §8.79 : mêmes 55 TSV, un flux renommé, un verdict nouveau

Le §8.79 et la présente section portent sur les **mêmes
55 TSV** de GDC ORGANOID-PANCREATIC, mais ne mesurent pas
la même chose — et le §8.79 n'a rien mesuré du tout sur
cette cohorte :

| | §8.79 (C2) | §8.85 (cette section) |
|---|---|---|
| Objet | Porte de construction « 12 gènes v4 présents » | Rupture multi-flux (12 flux, ordre KRAS) |
| Résultat | ARRÊT — DPCR1 absent de 55/55, aucun CSV, aucun run | `d_maxsep = +0,0884` (réel 0,2542, nul 0,1658), fragile |
| Flux | DPCR1 exigé au symbole exact | MUCL3 (ex-DPCR1), remappage vérifié R1–R5 |

Aucune des deux lectures ne valide l'autre : un arrêt de
construction ne prédit pas le verdict d'une paire, et un
verdict de paire ne rouvre pas l'arrêt — le §8.79 reste vrai
sous son protocole (symbole exact, aucun mappage), et le
§8.85 est vrai sous le sien (remappage pré-enregistré et
vérifié). Le fait que MUCL3 soit plat (ρ réel +0,023) ne
diminue ni n'augmente le verdict : le flux compte comme
douzième flux de la rupture, pas comme porteur d'un gradient.
Cette distinction est écrite ici pour qu'aucune lecture
future ne confonde l'arrêt §8.79 avec un échec de la
cohorte, ni le verdict §8.85 avec une révision du §8.79.

## 8.85.8 — Ce que le verdict dit, et ce qu'il ne dit pas

Il dit que `maxsep` sépare le réel du nul sur une quatorzième
cohorte indépendante — la première cohorte d'organoïdes, et
la première paire rendue possible par un remappage de
nomenclature vérifié — mais avec la deuxième plus petite
marge passante du compte A2 (+0,0184, derrière GSE131050 à
+0,0039) et un nul frais qui l'annule presque. Il dit aussi que le remappage DPCR1 → MUCL3 tient
sur cinq portes indépendantes (HGNC, Ensembl, NCBI, TSV) —
une leçon de provenance : un symbole de gène n'est pas un
invariant, et une cohorte RNA-seq récente peut perdre un
flux de la v4 par simple renommage, puis le retrouver par
une vérification de nomenclature. Il dit enfin que la
fragilité du nul à petit n n'est plus une hypothèse : à
n = 44, trois tirages de nul donnent des `maxsep` de 0,1606
à 0,2166, et un seul suffit à faire passer l'écart sous le
plancher. Il ne dit pas que `maxsep` est validé en général,
ni que la paire est consolidée (elle ne l'est pas), ni que
la rupture multi-flux vient d'un gradient par flux (les
tests directs disent le contraire). Il ne dit rien de
clinique.

## 8.85.9 — Pistes ouvertes

| Pistes ouvertes | Oui, une de plus | (a) La confirmation indépendante C3 est close depuis le §8.71 — cette quatorzième paire est une consolidation supplémentaire, pas une condition ; (b) la candidate C1 (Chen et al. 2025, 46 PDO × 63 AUC, supplément MOESM13 SHA vérifié `0e009cd5…`) reste la piste suivante pour un lot drogue v6.2 (cible Gemcitabine, 62 contrôles) — elle ne peut pas devenir une paire A2 ; (c) la candidate C4 (GSE194249) attend toujours son re-audit depuis GEO (n réponse exact, couverture v4) ; (d) la fragilité du nul à petit n est désormais mesurée sur 3 tirages ici (0,1606 / 0,1658 / 0,2166) — la question ouverte devient : combien de nuls frais faut-il pour stabiliser le verdict d'une paire à n = 44, et le plancher 0,07 doit-il dépendre de n (voir §8.53, 200 nuls pour un plancher stable à petit n) ; (e) la divergence `maxsep` passe / ordre direct faible (Δρ médian +0,088, 8/12) est une question ouverte nouvelle : sur quelles paires la rupture multi-flux existe-t-elle sans gradient monotone par flux, et que dit-elle de l'instrument — aucune décomposition ne tranche ici ; (f) le `sep` compagnon ne passe pas sa barre descriptive ici (+0,0605 contre 0,1023) alors que `maxsep` passe — à suivre sur les prochaines paires : si `sep` décroche systématiquement quand la marge `maxsep` est étroite, la barre équivalent-sep devient un signal d'alerte de fragilité, pas seulement un contrôle descriptif. |

## 8.85.10 — Annexe : provenance condensée et SHAs

- **Remappage :** HGNC MUCL3 (HGNC:21666), prev_symbol
  DPCR1, statut Approved, date_symbol_changed 2018-03-19,
  ensembl ENSG00000168631, entrez 135656, 6p21.33 —
  `https://rest.genenames.org/fetch/symbol/MUCL3` et
  `https://rest.genenames.org/fetch/prev_symbol/DPCR1`
  (réponses `hgnc_mucl3_885.json` SHA `c6dfe860…6049`,
  `hgnc_prev_dpcr1_885.json` SHA `8b6d99f7…b183`) ;
  Ensembl MUCL3 ENSG00000168631, DPCR1 « No valid lookup
  found for symbol DPCR1 » (`ensembl_mucl3_885.json` SHA
  `21191898…bc56`, `ensembl_dpcr1_885.json` SHA
  `3cb0e234…bfc0`) ; NCBI RefSeq MUCL3 NM_080870.4,
  Synonyms C6orf37,DPCR1,PBLT, Entrez 135656, HGNC 21666,
  chr6:30940973-30954221.
- **Cohorte courue :** GDC ORGANOID-PANCREATIC, manifeste SHA
  `f713edebf0f8afb20305b1472d480564e45ac31ce79e28350d7dde6ae496220b` ;
  55/55 fichiers MD5 OK et SHA-256 OK, total 232 648 892 o ;
  44 fichiers Tumor (38 cas, « Adenocarcinoma, NOS »),
  11 Normal exclus (cas 61–71) ; MUCL3 gene_id
  ENSG00000168631.13 dans 44/44, DPCR1 0/44 ; KRAS TPM min
  11,92 / médiane 31,83 / max 165,1.
- **Pipeline :** v6.2, SHA
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
  vérifié avant et après les lots.
- **Protocole gelé :** `PROTOCOL_gdc_mucl3_885.md`, SHA
  `2dfeeade0eceb85c7a5f109bcc589c0aab723909f483348a46a3f5e5d7379cdf`.
- **Provenance complète :** `PROVENANCE_885.md`, SHA
  `fe26f4e0d2b5de30f9f666ccfedda07e1cfa5386905abba71823e53f66869f2b`.
- **CSV de flux :** réel SHA
  `a83b98175bdbc33525ba8a175aa898504d2cc44125b891d0902c6c6c26345eaf` ;
  nul (graine 42) SHA
  `c3f8399cb423d7691136ed25860567186fb5e94e383283ddc081f83916bed12e` ;
  nul frais s8851 SHA
  `a6fd59ed651ab3bd3bb58e4f9587322f239ae622abbdb7b19e666aec8d114ccd` ;
  nul frais s8852 SHA
  `3801a71972c5e21c97c294b21352cc653a77e929aeea065acbec86a041185032`.
- **Runs :** `results_fast_v62_885_gdc_organoid`,
  `results_fast_v62_885_gdc_organoid_nul`,
  `results_fast_v62_885_gdc_organoid_nul_s8851`,
  `results_fast_v62_885_gdc_organoid_nul_s8852`, 4/4 exit 0,
  FIN 21 nov. 2026 14h04:35Z (paire) et 14h14:19Z (frais).
  Extraction `extract_885.json` / `.csv` ; vérification
  `maxsep_885_verify.json` (4/4, écart max 0,0, verdict OK) ;
  tests directs `direct_tests_885.json`.
- **Scripts :** `build_fluxes_885.py` (SHA
  `9dc2f667…0799`), `extract_885.py` (SHA `1742a314…dee0`),
  `verify_885.py` (SHA `c7b0977d…f65`), `direct_tests_885.py`
  (SHA `67878fa0…88d`) — originaux §8.79 intacts.
- **Verdict :** CONFIRME, FRAGILE, NON CONSOLIDÉ,
  `d_maxsep = +0,0884`
  (0,2542142849980612 − 0,1657676706638558) ; nuls frais
  +0,0376 / +0,0936 (min / max, médiane +0,0884). A2 :
  **10/14, 12/14 positifs, LOO 9/13.** C3 reste levée.

— Fin de la §8.85. —

---

## 8.85.11 — Note de fin de chantier (pour le coordinateur)

- Livre blanc NON édité, PDF NON régénéré, rien poussé sur
  GitHub (convention des chantiers ; fusion par le
  coordinateur).
- Titre à normaliser à la fusion : « ### 8.85 GDC
  ORGANOID-PANCREATIC avec remappage DPCR1 → MUCL3 :
  quatorzième paire CONFIRME, fragile et non consolidée
  (21 novembre 2026) ».
- Entrée de journal à ajouter : §8.85, protocole gelé
  ~08h55 EST, 4/4 runs exit 0, CONFIRME fragile
  (+0,0884 ; nuls frais +0,0376 / +0,0936), A2 10/14.
