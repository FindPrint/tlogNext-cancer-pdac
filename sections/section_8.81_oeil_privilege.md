# §8.81 — Piste Œil : la tumeur du pancréas copie-t-elle le privilège immunitaire de l'œil ? — MIXTE

## Verdict d'abord

**MIXTE — la tumeur du pancréas ne copie pas le privilège immunitaire de l'œil comme un programme
cohérent.** Sur les 7 gènes du privilège oculaire testés aujourd'hui dans 4 cohortes PDAC ordonnées par KRAS
(TCGA n = 178, GSE71729 n = 145, GSE62452 n = 69, ICGC n = 70), 3 montent avec KRAS selon les critères
gelés d'avance — CD47, TGFB1, CD274 — 4 ne montent pas (FASLG descend partout sans atteindre le seuil gelé,
TGFB2 monte partout mais trop faiblement, IDO1 et HLA-G sont incohérents d'une cohorte à l'autre), et le
score de privilège PRIV monte partout mais trop faiblement (rho médian +0,122, sous le seuil gelé de +0,15 ;
seule GSE62452 dépasse le seuil, +0,343, p = 0,004). Le critère gelé d'un OUI (≥ 4 gènes sur 7 qui montent,
ou score > +0,15 sur ≥ 3 cohortes) n'est pas atteint ; le critère d'un NON (≤ 1 gène qui monte, score plat)
ne l'est pas non plus. **Le bras pipeline v6.2 ne sauve pas la piste :** ordonnées par PRIV, les tumeurs TCGA
donnent `d_maxsep = +0,1649` (réel 0,3534 contre nul 0,1885, au-dessus du plancher 0,07), mais la chaîne du
§8.11 ne réapparaît pas — PGC et DPCR1 sont plats en Spearman (−0,057 et +0,009), MUC16 monte autant dans le
nul que dans le réel en top-12 (+0,408 contre +0,423). **Et le cancer de l'œil lui-même ne porte pas le
programme :** le mélanome uvéal TCGA-UVM (n = 80, téléchargé aujourd'hui) exprime MOINS — pas plus — les
7 gènes de privilège que le pancréas (d de Cohen −0,35 à −3,00), tout en étant plus « froid » (PDCD1 −1,30,
CD8A −1,33, GZMB −1,60), et sous l'ordre PRIV ses gènes v4 MONTENT (PGC +0,321, CLDN18 +0,306, CR2 +0,289)
au lieu de chuter — l'image miroir de la chaîne pancréatique, pas sa réapparition. Ce chantier ne rouvre
rien : C3 reste levée, test C reste NON, adoption pleine de maxsep reste la décision de Zackary.

| Porte (PROTOCOL_oeil_privilege_881.md, gelé) | Exigé | Mesuré 21 nov. 2026 | Sort |
|---|---|---|---|
| Gènes de privilège qui MONTENT avec KRAS (≥ 3 cohortes +, rho médian > +0,15) | ≥ 4/7 pour OUI | **3/7** (CD47, TGFB1, CD274) | **MIXTE** |
| Score PRIV vs KRAS (rho médian > +0,15 sur ≥ 3 cohortes) | ≥ 3 cohortes | **1/4** (GSE62452 seule, +0,343) | **MIXTE** |
| Chaîne du §8.11 sous l'ordre PRIV (D1 + D2, réel contre nul) | PGC/DPCR1/CLDN18 ↓ et MUC16 ↑ au-delà du nul | **Non** : PGC/DPCR1 plats en rho, MUC16 = nul en top-12 | **NON** |
| `d_maxsep` TCGA PRIV (plancher gelé) | > 0,07 | **+0,1649** (0,3534 − 0,1885) | **PASSE, piste seule** |
| `d_maxsep` UVM PRIV (plancher gelé) | > 0,07 | **+0,0496** (0,2661 − 0,2165) | **NE PASSE PAS** |
| UVM : privilège exprimé PLUS qu'en PAAD | d > 0 | **d −0,35 à −3,00** (moins partout) | **NON** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que trois pièces du privilège oculaire — le
« ne me mange pas » CD47, le TGF-β1 et le PD-L1 — montent bien avec KRAS dans le pancréas, et que c'est
cohérent avec la tumeur qui devient froide (PDCD1 chute dans les 4 cohortes, −0,21 à −0,24 ; CD8A chute
dans les 4, −0,15 à −0,35 — le témoin « froid » du §8.23 se reproduit aujourd'hui). Il dit que le reste du
programme ne suit pas : ni le FasL qui tue les lymphocytes (FASLG négatif partout), ni l'IDO1, ni HLA-G —
donc pas de copie du programme oculaire entier. Il dit que le score PRIV ordonne faiblement les tumeurs
et que le pipeline y voit un écart `maxsep` au-dessus du plancher sans y voir la chaîne : l'ordre existe,
la rupture cherchée n'y est pas. Il dit enfin que le mélanome uvéal, cancer d'un site à privilège, n'exprime
pas davantage ces gènes que le pancréas — le privilège de l'œil ne se lit pas comme une surexpression
tumorale de ces 7 gènes. Il ne dit pas que la tumeur n'échappe pas au système immunitaire — seulement
qu'elle ne le fait pas par ces 7 gènes le long de l'axe KRAS, dans ces cohortes. Il ne dit rien de
clinique : aucune affirmation sur un remède n'est tirée de ce chantier.

Protocole gelé : `PROTOCOL_oeil_privilege_881.md` (21 nov. 2026, SHA `c985a03a…a4ce`, inchangé).
Critères écrits AVANT toute construction et tout run (§3, §6 du protocole) ; aucune repondération,
aucun nouveau terme, aucune redéfinition du plancher après avoir vu les chiffres.

## 8.81.1 — Les tests directs : 3 gènes montent, 4 ne montent pas, le score monte trop faiblement

**Méthode (gelée).** T1, test PRINCIPAL : Spearman rho de chaque gène contre le rang KRAS, par cohorte.
TCGA : résidus après correction de pureté (même régression que la v4, reproduction vérifiée : écart max
1,776e-15, atol 1e-9). GEO/ICGC : valeurs fournies, cas complets, jamais d'imputation. Les 7 gènes de
privilège sont présents dans les 4 cohortes — aucun absent. Seule absence du chantier : **IFNG est ABSENT
de la matrice ICGC** (le symbole ne figure pas dans le fichier d'expression après mapping ; vérifié
directement) — case vide, pas zéro, pas imputé. Correction §8.70/§8.71 appliquée : le d de Cohen marginal
réel-vs-nul est vacueux par construction (vérifié : FASLG −0,0000, TGFB1 +0,0000, CD274 −0,0000) — il
valide la construction du nul et ne décide rien ; c'est le Spearman contre le pas qui porte l'information.

| Gène | TCGA (n=178) | GSE71729 (n=145) | GSE62452 (n=69) | ICGC (n=70) | rho médian | Verdict gelé |
|---|---|---|---|---|---|---|
| **CD47** | **+0,180** (p=0,016) | **+0,231** (p=0,005) | **+0,623** (p=1,1e-08) | **+0,137** (p=0,26) | **+0,206** | **MONTE** |
| **TGFB1** | −0,115 (p=0,13) | **+0,282** (p=0,0006) | **+0,210** (p=0,083) | **+0,165** (p=0,17) | **+0,188** | **MONTE** |
| **CD274 / PD-L1** | **+0,286** (p=0,0001) | −0,106 (p=0,20) | **+0,183** (p=0,13) | **+0,177** (p=0,14) | **+0,180** | **MONTE** |
| TGFB2 | +0,320 (p=1,4e-05) | +0,058 (p=0,49) | +0,159 (p=0,19) | +0,038 (p=0,76) | +0,108 | MIXTE (4/4 +, trop faible) |
| FASLG | −0,138 (p=0,066) | −0,060 (p=0,47) | −0,110 (p=0,37) | −0,046 (p=0,71) | −0,085 | MIXTE (4/4 −, sous le seuil) |
| IDO1 | −0,016 (p=0,83) | +0,150 (p=0,071) | −0,066 (p=0,59) | −0,056 (p=0,64) | −0,036 | MIXTE |
| HLA-G | +0,041 (p=0,59) | −0,253 (p=0,002) | +0,038 (p=0,76) | −0,118 (p=0,33) | −0,040 | MIXTE |
| **SCORE PRIV** | **+0,146** (p=0,051) | **+0,098** (p=0,24) | **+0,343** (p=0,004) | **+0,095** (p=0,43) | **+0,122** | **MIXTE** |
| *PDCD1 (témoin)* | *−0,213 (p=0,004)* | *−0,240 (p=0,004)* | *−0,215 (p=0,076)* | *−0,223 (p=0,064)* | *−0,219* | *chute, témoin reproduit* |
| *CD8A (témoin)* | *−0,165 (p=0,028)* | *−0,154 (p=0,064)* | *−0,348 (p=0,003)* | *−0,146 (p=0,23)* | *−0,160* | *chute, témoin reproduit* |
| *GZMB (témoin)* | *−0,108* | *+0,144* | *+0,059* | *−0,035* | *—* | *mixte* |
| *IFNG (témoin)* | *−0,021* | *+0,086* | *−0,086* | *absent* | *—* | *mixte / absent ICGC* |

**Lecture.** Les trois qui montent sont les trois pièces « passives » du privilège : CD47 (« ne me mange
pas », signal anti-phagocytose), TGFB1 (cytokine immunosuppressive) et CD274/PD-L1 (frein des lymphocytes
T). Les trois pièces « actives » ne suivent pas : FASLG — le ligand qui fait mourir les lymphocytes
attaquants, pièce maîtresse du privilège oculaire — DESCEND partout (−0,05 à −0,14, 4/4 négatif, sans
atteindre le seuil gelé de −0,15) ; IDO1 (enzyme qui affame les lymphocytes en tryptophane) et HLA-G
(molécule HLA tolérogène) changent de signe d'une cohorte à l'autre. TGFB2 monte partout mais trop
faiblement (médiane +0,108, porté par TCGA +0,320, p = 1,4e-05, seul). Le score PRIV — moyenne des
z-scores des 7 gènes — monte dans les 4 cohortes (+0,095 à +0,343), mais sa médiane (+0,122) reste sous
le seuil gelé (+0,15) et une seule cohorte le dépasse significativement (GSE62452, +0,343, p = 0,004).

**T2, descriptif : d de Cohen top-12 KRAS-fort contre reste.** Le tableau confirme la faiblesse et ajoute
une nuance : le score PRIV a un d top-12 NÉGATIF dans 3 cohortes sur 4 (TCGA −0,11 ; GSE71729 −0,39 ;
ICGC −0,32 ; seule GSE62452 +0,32) alors que son rho est positif partout. La relation PRIV–KRAS est donc
graduelle, pas un saut à l'extrême : les 12 tumeurs KRAS le plus fort ne sont PAS les plus « privilège ».
Recouvrement top-12 PRIV/KRAS (TCGA) : 1/12. Par gène, les d top-12 les plus forts sont CD47 en GSE62452
(+1,13, cohérent avec son rho +0,623) et CD274 en TCGA (+0,65) ; TGFB1 a un d top-12 de −0,45 en TCGA
malgré un rho positif en GEO — le signal TGFB1 n'est pas porté par l'extrême TCGA. Aucun d top-12 ne
contredit le verdict T1 ; aucun ne le renforce au point de changer un verdict gelé.

## 8.81.2 — Bras pipeline v6.2 (TCGA, ordre PRIV) : `maxsep` passe, la chaîne ne réapparaît pas

**Runs : 2/2, exits 0/0.** Manifeste `manifest_v62_881.txt`, lanceur reprenable `run_v62_lot.sh`, unité
systemd `v62-881` (jamais nohup), FIN 2026-11-21T12:50:55Z, `deja_faits=0 termines=4 echecs=0`
(les 2 runs UVM sont dans le même lot, voir §8.81.3). SHA du pipeline revérifié avant ET après le lot :
`f07567c4…c3abf`, inchangé. Série réelle `pdac_tcga_fluxes_v4_priv.csv` (178 lignes, PRIV en 1re colonne,
12 flux v4, tri par PRIV croissant ; PRIV min −2,050, médiane +0,063, max +1,425 ; 7 gènes au score,
aucun doublon contrôle/flux) ; nul graine 42 (bloc des 12 flux permuté, PRIV intact).
Extraction 2/2 recoupée par relecture directe indépendante des 4 `master_results.json` : `maxsep` et MC
identiques à 0,0 exact. Version lue : `v6.2.0-L7aL7b-CohenD-short` sur les 4 runs. L7b : FRAGILE sur les
4 runs — audit clos comme non-informatif, non rapporté comme mesure de fragilité.

| Run | n | maxsep | ancien MC | S_sep | Delta | L7a | Cascade (Q1–Q5, %) |
|---|---|---|---|---|---|---|---|
| Réel PRIV TCGA | 178 | **0,3534** | 0,3550 | 0,3507 | 3,858 | up 0,416 | 0,0 / 0,7 / 3,7 / 37,7 / 37,7 |
| Nul graine 42 | 178 | 0,1885 | 0,3308 | 0,1874 | 3,804 | up 0,193 | 0,0 / 1,1 / 5,9 / 28,5 / 28,5 |

`d_maxsep = +0,1649` — au-dessus du plancher gelé 0,07, avec une marge de +0,0949. MC à peine positif
(+0,0242), Delta à peine positif (+0,054), falsification 0,674 contre 0,721 (le nul « falsifie » autant
que le réel), L7a up des deux côtés. La cascade est TRÈS BASSE des deux côtés (T_0 au pas 7 sur 178 dans
le réel, au pas 10 dans le nul — ~4–6 % de la série, c'est-à-dire au tout début) : elle ne sépare pas
le réel du nul ici, et elle ne l'a jamais été comme critère.

**Tests directs sur la série PRIV (D1 + D2) — c'est eux qui décident de la chaîne, pas `maxsep`.**
Signature cherchée (référence §8.4) : PGC −0,89, DPCR1 −0,85, CLDN18 −0,46, MUC16 +0,64.

| Flux | D1 top-12 PRIV (d, réel) | D1 top-12 (d, nul) | D2 rho vs rang PRIV (réel) | D2 rho (nul) |
|---|---|---|---|---|
| PGC | −0,165 | −0,063 | −0,057 | −0,094 |
| REG4 | −0,744 | −0,385 | −0,125 | −0,043 |
| CLDN18 | −0,271 | −0,094 | −0,166 | −0,080 |
| DPCR1 | −0,417 | +0,187 | +0,009 | +0,001 |
| MUC16 | +0,408 | **+0,423** | **+0,402** | +0,136 |
| CR2 | +0,506 | −0,033 | +0,286 | +0,119 |
| GSTM1 | +0,319 | −0,412 | +0,167 | −0,085 |

La chaîne ne réapparaît pas. PGC chute faiblement en top-12 mais son rho est plat (−0,057, nul −0,094) :
pas de pente, pas de rupture. DPCR1 chute en top-12 (−0,417 contre +0,187 au nul) mais son rho est
exactement 0 (+0,009) : l'écart top-12 est un effet d'extrême, pas une tendance. CLDN18 chute
modestement des deux côtés (−0,271 ; rho −0,166 contre −0,080 au nul). MUC16 monte — mais en top-12
il monte AUTANT dans le nul (+0,423) que dans le réel (+0,408) ; seul son rho se distingue du nul
(+0,402 contre +0,136). CR2 monte (+0,286 contre +0,119 au nul) — CR2 ne fait pas partie de la
signature cherchée. Autour de T_0 (pas 7, ±20 lignes) : PGC +1,412, DPCR1 +0,994, MUC16 +0,892 dans le
réel — mais le nul, à son propre T_0 (pas 10), montre les mêmes ordres de grandeur (PGC +0,994,
CLDN18 +1,318, MUC17 +1,066). Un T_0 au pas 7 sur 178 n'est pas un seuil lisible, c'est le début de
la série ; la lecture autour du seuil ne porte rien ici, et c'est dit tel quel.

**Lecture du bras pipeline.** Le `maxsep` qui passe (+0,1649) dit que l'ordre PRIV porte une information
réelle — les flux ne sont pas dans un ordre aléatoire sous PRIV (MUC16 rho +0,402, CR2 +0,286). Mais
l'information portée n'est PAS la chaîne du §8.11 : les trois gènes qui doivent chuter sont plats ou
faibles en pente, et le gène qui doit monter monte aussi dans le nul en top-12. C'est le même motif
qu'aux §8.70/§8.71/§8.74 : `maxsep` voit quelque chose que les scores compagnons voient à peine
(MC +0,024, Delta +0,054) — et ici, ce quelque chose n'est pas la chaîne. Le verdict du bras est donc
double et il est consigné double : `maxsep` passe le plancher (piste), la chaîne ne réapparaît pas (NON).

## 8.81.3 — Le cancer de l'œil : TCGA-UVM (n = 80) — moins de privilège, plus froid, image miroir

**Source (nouveau téléchargement, réussi du 1er coup).** Broad GDAC Firehose stddata 2016-01-28, UVM,
RSEM genes normalized, URL `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/UVM/20160128/gdac.broadinstitute.org_UVM.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz`,
téléchargé le 21 nov. 2026, 12h15 UTC (curl, exit 0), 6 311 998 o,
SHA-256 `b50fdadb00d5c4095ffbe55ad4192cfca892c947cd657d032be128ba074a9975`.
80 tumeurs primaires (code 01). Les 12 gènes v4, les 7 gènes de privilège et les 4 témoins sont tous
présents en UVM. Valeurs : log2(RSEM+1), sans correction de pureté (pas de scores acineux/îlots pour
l'œil — importer la correction pancréatique aurait été une erreur). Score PRIV UVM (z intra-UVM, 7 gènes) :
min −1,133, médiane −0,155, max +1,565.

**U1 — Niveaux médians, UVM contre TCGA-PAAD brut (même échelle, d de Cohen entre cohortes, + = plus
haut en UVM).** Le mélanome uvéal exprime MOINS les gènes de privilège que le pancréas, sur les 7 :

| Gène | Médiane UVM | Médiane PAAD | d UVM vs PAAD |
|---|---|---|---|
| FASLG | 1,611 | 3,375 | −0,878 |
| TGFB1 | 9,000 | 10,917 | −2,206 |
| TGFB2 | 4,962 | 9,067 | −2,999 |
| IDO1 | 1,735 | 6,745 | −1,945 |
| HLA-G | 6,856 | 7,348 | −0,349 |
| CD47 | 10,276 | 11,208 | −1,985 |
| CD274 / PD-L1 | 3,658 | 4,724 | −0,700 |
| *PDCD1 (témoin)* | *2,201* | *5,059* | *−1,296* |
| *CD8A (témoin)* | *4,329* | *7,407* | *−1,330* |
| *GZMB (témoin)* | *2,361* | *5,529* | *−1,599* |
| *IFNG (témoin)* | *0,000* | *1,171* | *−0,380* |

Les gènes tueurs sont AUSSI plus bas en UVM (PDCD1 −1,30, CD8A −1,33, GZMB −1,60) : l'UVM est plus
« froid » que le pancréas en niveaux absolus — mais ce froid ne s'accompagne pas d'une surexpression
des gènes de privilège, il s'en accompagne de l'inverse. Deux réserves, nommées d'avance au protocole
§8 et confirmées ici : (a) la comparaison de niveaux bruts entre deux types tumoraux est descriptive —
elle conflue pureté, composition et spécificité tissulaire ; (b) pour les gènes v4, la spécificité
tissulaire DOMINE : 9 gènes sur 12 ont une médiane de 0,000 en UVM (PGC, REG4, MUC17, CR2, KRT20,
MUC2, CEACAM5, CLCA1, MUC16 ; CLDN18 0,539, DPCR1 0,905, GSTM1 7,771 — seul GSTM1 est plus haut en
UVM, d +0,29) — ce sont des gènes de pancréas/estomac/mucus, simplement pas exprimés dans l'œil, et
leurs d (−1,0 à −3,85) ne mesurent pas un privilège, ils mesurent un tissu. Pour les 7 gènes de
privilège et les 4 témoins, en revanche, les médianes UVM sont non nulles (TGFB1 9,0, CD47 10,3,
HLA-G 6,9) : la lecture « moins exprimés en UVM » tient pour eux, avec la réserve (a).

**U2 — Pipeline v6.2 sur UVM ordonné par PRIV : 2/2, exits 0/0, ne passe pas le plancher.**

| Run | n | maxsep | ancien MC | S_sep | Delta | L7a | Cascade (Q1–Q5, %) |
|---|---|---|---|---|---|---|---|
| Réel PRIV UVM | 80 | 0,2661 | 0,3386 | 0,2637 | 0,559 | down 0,169 | 13,6 / 89,0 / 92,7 / 95,7 / 98,7 |
| Nul graine 42 | 80 | 0,2165 | 0,3320 | 0,2154 | 0,538 | up 0,346 | 11,1 / 19,7 / 23,5 / 28,4 / 42,8 |

`d_maxsep = +0,0496` — sous le plancher 0,07. MC +0,0066, Delta +0,020, falsification 0,217 contre
0,220, L7a en sens opposé (down 0,169 contre up 0,346). La cascade réelle est très haute et se
distingue du nul (T_0 au pas 73 sur 80, ~92 % de la série, contre pas 19 au nul) — c'est consigné
en descriptif : la cascade n'est pas un critère de passage et ne l'a jamais été, et un T_0 à 92 %
de la série ne ressemble pas à un seuil central. F1/F2 après seuil : réel 0,0116 / 0,00133 contre
nul 0,00387 / 0,00044 (descriptif).

**U3 — La chaîne v4 sous l'ordre PRIV, dans l'UVM : image miroir, pas réapparition.**

| Flux | rho vs rang PRIV (réel) | p | d top-12 PRIV (réel) | rho (nul) | d top-12 (nul) |
|---|---|---|---|---|---|
| PGC | **+0,321** | 0,004 | **+0,960** | +0,103 | −0,060 |
| CLDN18 | **+0,306** | 0,006 | **+0,956** | +0,172 | +0,138 |
| CR2 | **+0,289** | 0,009 | **+1,752** | +0,025 | −0,172 |
| MUC2 | +0,191 | 0,090 | +0,533 | −0,132 | −0,056 |
| DPCR1 | −0,189 | 0,093 | −0,641 | +0,026 | +0,113 |
| REG4 | −0,159 | 0,16 | −0,399 | +0,153 | −0,195 |
| MUC16 | +0,030 | 0,79 | +0,236 | −0,106 | −0,167 |

Dans l'œil, sous l'ordre PRIV, PGC, CLDN18 et CR2 MONTENT significativement — exactement les gènes qui
CHUTENT au bout de l'axe KRAS dans le pancréas. DPCR1 chute (−0,189, d −0,641), comme dans le pancréas,
mais seul ; MUC16 est plat (+0,030). Ce n'est pas la chaîne du §8.11 : c'est son image miroir partielle.
Réserve majeure, consignée : PGC, CLDN18 et CR2 ont une médiane de 0,000 en UVM — plus de la moitié
des tumeurs ne les expriment pas du tout — donc ces rho sont portés par la minorité de tumeurs qui les
expriment, pas par un gradient sur toute la cohorte. Aucune lecture biologique n'est tirée d'un rho
porté par des zéros sans le dire.

## 8.81.4 — Ce que le verdict dit, et ce qu'il ne dit pas

Il dit que le pancréas KRAS-fort active trois pièces du privilège (CD47, TGFB1, PD-L1) mais pas les
quatre autres, et pas le programme comme un tout — avec un score PRIV qui monte partout mais trop
faiblement pour le seuil gelé, et sans saut à l'extrême KRAS-fort (d top-12 du score négatif dans
3 cohortes sur 4). Il dit que le pipeline voit un écart `maxsep` au-dessus du plancher sous l'ordre
PRIV (+0,1649) sans y voir la chaîne : l'ordre porte une information, la rupture cherchée n'y est pas.
Il dit que le cancer de l'œil n'exprime pas davantage ces gènes — il en exprime moins — et que, rangé
par PRIV, il montre l'image miroir de la chaîne pancréatique. Il dit enfin que le témoin « froid »
(PDCD1, CD8A en chute dans les 4 cohortes) se reproduit aujourd'hui, ce qui rend le négatif partiel
plus crédible : l'instrument de mesure du froid fonctionne, c'est le programme de privilège qui ne
suit pas.

Il ne dit pas que CD47/TGFB1/PD-L1 sont des cibles : ce sont des corrélations d'expression le long
de KRAS, pas des preuves de mécanisme, et PD-L1 avait déjà échoué comme rationnel combiné au §8.23
(KRAS + anti-PD-(L)1 : pas de rationnel — ce chantier ne rouvre pas ce verdict, il le laisse intact :
CD274 qui monte avec KRAS ne suffit pas à faire un rationnel, pas plus au §8.81 qu'au §8.23).
Il ne dit pas que l'œil n'a pas de privilège immunitaire : le privilège est une propriété du tissu
oculaire normal, mesurée ici sur un cancer de l'œil, pas sur l'œil sain — l'UVM ne peut pas réfuter
le privilège, il peut seulement dire que la tumeur de l'œil ne surexprime pas ces 7 gènes. Il ne dit
pas que `maxsep` est validé par ce chantier : un écart au-dessus du plancher sur une paire, avec des
scores compagnons à peine positifs et une chaîne absente, est une piste, pas une preuve. Il ne dit
rien de clinique : l'étude porte sur l'instrument et sur des corrélations d'expression, pas sur un
remède — aucune affirmation sur le cancer du pancréas n'est tirée de ce chantier au-delà des
corrélations mesurées.

**Biais et limites nommés.** (a) 7 gènes mesurent une expression, pas le privilège lui-même (barrières,
ACAID, FasL tissulaire ne sont pas mesurés). (b) Un seul nul par paire (graine 42) ; ~200 nuls pour
un plancher stable à petit n (§8.53) — la marge TCGA (+0,0949 au-dessus du plancher) est une marge
sur un nul, pas sur une distribution de nuls. (c) Hétérogénéité des plateformes (RNA-seq TCGA/ICGC,
puces Agilent/Affymetrix) : les rho intra-cohorte sont comparables, les niveaux bruts inter-cohortes
ne le sont qu'en descriptif. (d) IFNG absent de la matrice ICGC (voir §8.81.1). (e) UVM : médianes à
zéro pour 9 gènes v4 sur 12 — les rho U3 sont portés par une minorité de tumeurs exprimantes.
(f) TCGA : le d top-12 et le rho divergent pour TGFB1 et pour le score PRIV — la relation est
graduelle, pas une rupture à l'extrême ; aucun seuil n'est inféré d'une divergence entre deux mesures.

## 8.81.5 — Pistes ouvertes

| Pistes ouvertes | (a) Les 3 gènes qui montent (CD47, TGFB1, CD274) méritent un test direct ciblé — pas comme « programme
de privilège », mais comme trois pièces séparées : CD47 a le signal le plus fort et le plus cohérent
(rho +0,14 à +0,62, 4/4 positifs, d top-12 +1,13 en GSE62452) ; (b) le `maxsep` TCGA PRIV (+0,1649)
sans chaîne pose la même question qu'aux §8.70/§8.71/§8.74 — ce que `maxsep` lit quand la chaîne
n'y est pas — sans réponse ici ; (c) l'image miroir UVM (PGC/CLDN18/CR2 qui montent avec PRIV) est
une curiosité portée par des zéros, pas une piste thérapeutique ; (d) la piste Œil, comme question de
copie d'un programme, est CLOSE par ce verdict MIXTE : la relancer demanderait une autre définition du
privilège (protéine, single-cell, œil normal) — pas un autre découpage de ces mêmes matrices ; (e) la
fragilité du nul à petit n (§8.70, §8.53) reste un chantier propre ouvert — ici 1 seul nul par paire,
aucune étendue mesurée. |

## 8.81.6 — Annexe : provenance condensée et SHAs

- **Question :** Zackary, 21 nov. 2026 — « la tumeur du pancréas copie-t-elle les mécanismes du
  privilège immunitaire de l'œil pour se cacher ? » Piste acceptée et lancée le jour même.
- **Protocole :** `PROTOCOL_oeil_privilege_881.md`, SHA `c985a03a…a4ce` (gelé avant toute construction
  et tout run). Critères §3 et §6 écrits avant les runs ; plancher maxsep 0,07.
- **Pipeline :** v6.2 SHA `f07567c4…c3abf`, vérifié avant et après le lot, inchangé.
- **Sources PDAC (déjà sur disque) :** TCGA-PAAD Firehose stddata 2016-01-28 (MD5
  `b09569ce…ac0a`), GSE71729, GSE62452 (+ mapping GPL6244), ICGC PACA-AU (Bailey et al. 2016).
  Reproduction v4 vérifiée : écart max 1,776e-15 (atol 1e-9).
- **Source UVM (nouveau téléchargement 21 nov. 2026, 12h15 UTC) :** Firehose stddata 2016-01-28, UVM,
  RSEM genes normalized, `data/tcga_uvm_rsem.tar.gz` (6 311 998 o),
  SHA `b50fdadb…9975`. URL complète en `PROVENANCE_881.md`.
- **CSV de flux :** TCGA PRIV réel `348401cb…2db39` (178 lignes) ; nul s42 `54eec127…3d824` ;
  UVM PRIV réel `422898b7…3d65` (80 lignes) ; nul s42 `56be6c56…f178`.
- **Tests directs :** `priv_direct_tests_881.csv` `3301bfc3…8cb37b` ;
  `priv_direct_tests_881.json` `be4277fc…35955` ;
  `uvm_direct_tests_881.csv` `bbb05017…0033b` ; `uvm_881.json` `bc95f3ac…9c0`.
- **Extraction :** `priv_extract_881.json` `ec1dfdb6…3369d0` ;
  `priv_direct_tests_881_series.csv` `42701d53…6c40`.
  Recoupement indépendant : `maxsep` et MC identiques à 0,0 exact sur les 4 runs.
- **Scripts :** `direct_tests_881.py` `01c8b744…397d91` ; `build_priv_881.py` `4a4693ca…57a69` ;
  `uvm_881.py` `9af4dfb9…7fdfa` ; `extract_881.py` `2150c39d…98acc`.
- **Manifestes / journaux :** `manifest_v62_881.txt` `033c2b38…f82c` ;
  `runs_v62_881.log` `f8394215…21a4a` (FIN 2026-11-21T12:50:55Z, 4/4, exits 0).
- **Provenance complète :** `PROVENANCE_881.md` (+ `PROVENANCE_priv_881.json` `14c3331d…587b`).
- **Recoupements (reprises telles quelles, jamais recalculées) :** §8.23 (PDCD1 rho −0,25/−0,24/−0,22/−0,22 ;
  top-12 d −0,61 à −0,88 ; KRAS + anti-PD-(L)1 sans rationnel) ; §8.4 (signature de la chaîne :
  PGC −0,89, DPCR1 −0,85, CLDN18 −0,46, MUC16 +0,64) ; §8.53 (~200 nuls pour un plancher stable).
- **Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub** (convention des chantiers ;
  fusion par le coordinateur).

— Fin de la section §8.81. —
