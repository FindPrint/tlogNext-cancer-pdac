### 8.96 Universalité : le pipeline sur un autre cancer — LUAD NON, BRCA CONFIRME (partiel) ; la confirmation totale reste non testée (21–22 novembre 2026)

Piste 4/4 du lot du 21 nov. 2026 (go de Zackary « Faite tout cela »,
21 nov. 2026 11h36) ; protocole gelé 21 nov. 2026 avant tout
téléchargement nouveau, toute copie et tout calcul
(`PROTOCOL_universalite_896.md`, SHA `1349b996…848d8`) ; provenance
`PROVENANCE_896.md`, SHA `d9554cf3…a92c68`. Pipeline v6.2, SHA
`f07567c4…c3abf`, vérifié avant et après chaque lot, inchangé.
Correction de Zackary du 21 nov. 2026 12h03 (portée : tout le projet,
précisée 12h04 ; `ADDENDUM_correction_20261121_896.md`, SHA
`ff840864…97f132`) : MC jamais seul — la batterie entière fait le
verdict ; un flux en axe de contrôle n'est jamais un flux analysé ;
formulation en analyse, jamais en prédiction. Choix de l'axe BRCA
par addendum daté (`ADDENDUM_axe_brca_896.md`, SHA `aed56a92…48ba`).

## Verdict d'abord

**Bras A — LUAD : NON.** Le réel ne se sépare pas du nul sur la
barre gelée : écart `maxsep` réel − nul graine 42 de **+0,0140**
(réel 0,1502 contre nul 0,1362), très sous le plancher 0,07 — et
les deux nuls frais confirment le NON (+0,0321 et +0,0436, tous
deux sous le plancher). L'ancien MC ne sépare pas non plus
(−0,0203 contre le nul graine 42, le nul au-dessus du réel),
Delta non plus (+0,0137 contre le nul graine 42 ; le nul frais
s9601 est même très au-dessus du réel, 4,6279 contre 2,5108).
La lecture en LUAD est donc : le pipeline ne sépare pas le réel
du nul sur ces données, avec ces 12 flux, sous l'axe KRAS — un
NON qui ne retire rien aux résultats PAAD, il borne
l'universalité.

**Bras B — BRCA : CONFIRME (partiel).** Le réel se sépare du nul
sur la barre gelée : écart `maxsep` réel − nul graine 42 de
**+0,2182** (réel 0,3200 contre nul 0,1018), au-dessus du plancher
0,07, avec Delta positif dans le même sens (+0,5357) et L7a
concordant (réel UP 38,43 % contre nul DOWN 18,08 %) — et les
deux nuls frais confirment (écarts +0,2056 et +0,1990, 2/2
au-dessus du plancher). MAIS la confirmation est partielle
seulement : l'ancien MC ne sépare pas (−0,0092 contre le nul
graine 42, −0,0088 contre le nul frais s9602), la falsification
est plus haute sur les trois nuls que sur le réel, L7b est
FRAGILE sur les 8 runs du lot, et Delta échoue contre le nul
frais s9601 (−0,0352). La séparation en BRCA est portée par
`maxsep`, Delta (contre 2 nuls sur 3) et L7a (contre le nul
graine 42 seulement), pas par la batterie entière.

**Confirmation totale : NON TESTÉE, donc non écrite.** La barre
gelée exigeait en plus la structure analogue — le bloc
estomac/mucus (ou un bloc de co-expression équivalent) variant
avec l'axe, comme en PAAD (§8.33/§8.66). Aucun test direct de ce
type n'a été fait dans ce chantier, sur aucun des deux bras :
aucun fichier de test ne figure sur disque, et cette section
n'invente pas le test après coup. Le verdict « total » n'est
donc pas rendu, ni pour LUAD ni pour BRCA.

| Porte (protocole §1.4, gelé) | Exigé | Mesuré 21 nov. 2026 | Sort |
|---|---|---|---|
| LUAD : écart `maxsep` réel − nul 42 | > 0,07 | **+0,0140** (0,1502 contre 0,1362) | **ÉCHOUE** |
| LUAD : 2e indicateur concordant (MC / Delta / L7a) | positif | MC −0,0203 ; Delta +0,0137 ; L7a UP contre DOWN | **NON** |
| LUAD : nuls frais ≥ 1/2 au-dessus du plancher | ≥ 1/2 | **+0,0321 et +0,0436 — 0/2** | **NON** |
| BRCA : écart `maxsep` réel − nul 42 | > 0,07 | **+0,2182** (0,3200 contre 0,1018) | **PASSE** |
| BRCA : 2e indicateur concordant | positif | Delta +0,5357 ; L7a UP 38,43 % contre DOWN 18,08 % | **PASSE** |
| BRCA : nuls frais ≥ 1/2 au-dessus du plancher | ≥ 1/2 | **+0,2056 et +0,1990 — 2/2** | **PASSE** |
| Structure analogue (bloc estomac/mucus variant avec l'axe) | test direct, mêmes gènes/seuils que §8.33/§8.66 | **aucun test fait — absent du disque** | **NON TESTÉ** |
| 8 runs v6.2, exit 0, SHA v6.2 vérifié | 8/8 | **8/8 exit 0** (LUAD 16h42–17h03 UTC, BRCA 17h03–18h21 UTC) | **PASSE** |
| Contrôle jamais analysé (correction 21 nov. 12h03) | KRAS / ESR1 absents des flux | **vérifié sur les fichiers construits** | **PASSE** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que,
sur les deux cancers testés ici avec les mêmes 12 flux, le
pipeline sépare le réel du nul dans un cas (BRCA, par `maxsep`
surtout) et pas dans l'autre (LUAD, par aucun indicateur) — une
universalité partielle, mesurée, pas un principe général. Il dit
aussi que la séparation en BRCA ne tient pas à toute la
batterie : MC, falsification et L7b ne la portent pas, et un nul
frais sur deux renverse Delta. Il ne dit pas que le pipeline
séparera le réel du nul sur un troisième cancer (analyse, pas
prédiction — correction du 21 nov. 12h03). Il ne dit rien de
clinique : ce sont des ARN tumoraux ordonnés par un gène, pas
des réponses de patients — aucune affirmation sur un traitement
n'est tirée de ce lot. Il ne dit pas que la structure KRAS du
pancréas existe ou non dans le poumon ou le sein : le test qui
l'aurait dit n'a pas été fait.

**Fragilité, dite en tête.** Le verdict BRCA tient à une seule
paire réelle (n = 1 093) contre trois nuls, avec un écart
`maxsep` large (+0,2182) mais un réel dont le diagnostic de
bruit est le plus fort du lot (score moyen 0,6945,
« proxy de variance modéré », MEDIUM_HIGH — le seul run du lot
à ce niveau) et dont la cascade est comprimée très tôt
(T0 11,25 %, T+1/T+2 23,19 % contre 83–94 % pour les nuls).
Le verdict LUAD tient à l'inverse : le réel reproduit presque
exactement les chiffres v6.0/v6.1 du §8.27 (Delta 2,5108 contre
2,511 ; L7a UP 42,05 % contre 42,11 %), mais le nul graine 42
est presque au même niveau sur tous les indicateurs — la
différence réel/nul est un bruit de fond, pas un signal manqué
de peu. Enfin, deux runs BRCA nuls (graine 42 et s9602) portent
une anomalie de recomposition MC (§8.96.7) : le score MC stocké
ne suit pas la formule de recomposition du §8.50 (écart 0,0900)
— l'anomalie ne change pas le sens des écarts MC (négatifs dans
les deux lectures), mais elle est consignée telle quelle.

## §8.96.1 Question et protocole gelé

Tout le travail PDAC est pancréas-spécifique. La question porte
sur l'instrument, pas sur le cancer : le pipeline sépare-t-il le
réel du nul ailleurs, et trouve-t-il une structure analogue ?
Deux bras, dans cet ordre : (A) LUAD — données déjà détenues,
axe analogue déjà construit (KRAS, même gène pilote, même sens
qu'en PAAD) ; (B) BRCA — données à sourcer, construction neuve,
axe choisi après lecture de la matrice et avant tout run (ESR1).
Le témoin COAD est lu, pas recouru : son programme KRAS est
déjà connu différent (§8.27), et aucun run COAD neuf ne fait
partie de ce lot. La batterie entière fait le verdict (correction
du 21 nov. 12h03) : 29 estimateurs, Q1–Q6, 4 tests de bruit,
F1/F2, L7a/L7b, falsification, Delta, `maxsep` — `maxsep` est
le score principal affiché, pas le verdict. Le pipeline v6.2
ne change jamais (SHA `f07567c4…c3abf`).

## §8.96.2 Données et axes

**Bras A — TCGA-LUAD (données détenues, rien à télécharger).**
Source : Broad GDAC Firehose stddata 2016-01-28,
`LUAD.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt`,
47 043 687 octets, MD5 observé `4c36eec3f6df75630292c5a569cfc8f4`
(aucun MD5 de référence publié par Firehose). Matrice
20 503 gènes × 576 échantillons ; retenus : 515 tumeurs primaires
(code TCGA 01) ; transformation log2(RSEM normalisé + 1). Flux :
`pdac_luad_fluxes.csv`, SHA `d407849b…38091e`, 515 lignes,
12 flux — les 12 MÊMES gènes que PAAD v4 (PGC, REG4, CLDN18,
MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16),
12/12 présents, 0 NaN, aucun remplacement. Nul graine 42 :
`pdac_luad_fluxes_nul.csv`, SHA `93766e8c…978a6b`. Nuls frais
(graines gelées 9601, 9602, jamais utilisées dans ce projet) :
`pdac_luad_fluxes_nul_s9601.csv`, SHA `6e652a42…c72d1` ;
`pdac_luad_fluxes_nul_s9602.csv`, SHA `358188cf…336f`. Axe :
**expression KRAS brute croissante ; KRAS = axe, jamais un
flux** (KRAS log2 : n = 515, min 8,921, médiane 10,4127, max
14,8647). Gate 12/12, 0 NaN — déjà vérifié au §8.27, re-vérifié
avant les runs.

**Bras B — TCGA-BRCA (données sourcées, construction neuve).**
Source : Broad GDAC Firehose stddata 2016-01-28, cohorte BRCA,
tarball `gdac.broadinstitute.org_BRCA.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz`,
97 981 987 octets, MD5 observé `b4eed57d14ca2fa563ca0dd05d4fba7f`
(conforme au `.md5` publié par Firehose) ; matrice interne
212 145 748 octets, MD5 observé `96d707af16947605116dfbec6e3c050e`.
Matrice : 20 503 gènes × 1 212 échantillons ; retenues :
1 093 tumeurs primaires (code TCGA 01) ; log2(RSEM normalisé + 1).
Script de construction neuf `build_fluxes_brca_896.py`, SHA
`7f60c0fe…62b4`, calqué sur `build_fluxes_pancancer.py`. Les 12
gènes v4 PAAD sont présents avec 1 093/1 093 valeurs valides —
gate 12/12 PASSÉ, 0 remplacement, 0 NaN. Flux :
`pdac_brca_fluxes.csv`, SHA `c08ebf41…2d84` ; nul graine 42 :
`pdac_brca_fluxes_nul.csv`, SHA `f8234a33…c88b29` ; nuls frais :
`pdac_brca_fluxes_nul_s9601.csv`, SHA `5713da1f…57f7e` ;
`pdac_brca_fluxes_nul_s9602.csv`, SHA `88a1b9aa…62a8`.
Axe (addendum daté, après lecture de la matrice, avant tout run) :
**expression ESR1 brute croissante ; ESR1 = axe, jamais un flux.**
ESR1 (n = 1 093, min 1,901, médiane 12,795, max 16,137,
écart-type 3,190) a été choisi sur les trois critères gelés —
présence (1 093 ≥ 50), variance inter-tumeurs la plus forte des
trois candidats (TP53 : 0,862 ; MKI67/prolifération : 1,300),
pertinence (ESR1 définit les sous-types BRCA, luminal contre
basal/triple-négatif). TP53 écarté pour faible variance, MKI67
écarté comme axe principal. KRAS n'est pas l'axe en BRCA
(exclu par le protocole : rarement pilote du sein). Aucun
chiffre de run n'a influencé le choix.

**Règle du contrôle (correction du 21 nov. 12h03).** Vérifiée
sur les fichiers construits : KRAS est absent des 12 flux LUAD,
ESR1 est absent des 12 flux BRCA (KRAS absent aussi). Le
pipeline exclut en outre la colonne de contrôle des flux
analysés par construction (v6.2, ligne 6787 :
`c != control_col`). Le défaut connu des 96 rotations
d'origine (§8.32) ne concerne pas cette piste.

## §8.96.3 Runs : 8/8 exit 0, SHA vérifié

Huit runs v6.2 fast, commande identique aux lots précédents
(`python3 universal_v6.2.0_cohen.py --input <csv> --mode fast
--output <dir>`), lots systemd, SHA v6.2 vérifié au lancement
et à la fin de chaque lot (`f07567c4…c3abf`, attendu identique).
Lot LUAD 21 nov. 2026 16h42–17h03 UTC : réel, nul 42, nuls
frais s9601, s9602 — 4/4 exit 0 (`runs_luad_896.log`). Lot BRCA
21 nov. 2026 17h03–18h21 UTC : réel, nul 42, nuls frais s9601,
s9602 — 4/4 exit 0 (`runs_brca_896.log`, reprises après
redémarrages de la file, 0 run perdu). Aucun run relancé, aucun
dossier de run touché après coup.

Lecture des résultats : script `extract_universalite_896.py`
(SHA `583397ed…fa210`, lecture seule — il reprend la logique
de lecture de `mtap_consolidation_850.py` : S_sep =
`max_separation` × stabilité ; MC recomposé
0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·acuité).
Sorties : `universalite_896_table.json` (SHA
`cfddd6d8…fe24`) et `universalite_896_table.csv` (SHA
`47807fd2…ef2cfc`). Les médianes Q1–Q6 sont calculées ici sur
les 348 entrées flux × estimateur de chaque `scores.json`
(12 flux × 29 estimateurs) ; les résumés des 4 tests de bruit
sont les médianes sur les 1 044 lignes de chaque
`estimator_four_tests.csv` (12 flux × 29 estimateurs × 3
trajectoires : estimateur, F1, F2). Ces deux agrégations sont
des lectures de cette section, pas des sorties du pipeline —
elles sont définies ici pour être reproductibles.

## §8.96.4 Batterie complète : les 8 runs

| Run | n | `maxsep` | S_sep | MC | Delta | L7a | Falsification | Régime |
|---|---|---|---|---|---|---|---|---|
| LUAD réel | 515 | 0,1502 | 0,1500 | 0,3236 | 2,5108 | UP 42,05 % | 0,6389 | criticality |
| LUAD nul 42 | 515 | 0,1362 | 0,1349 | 0,3439 | 2,4971 | DOWN 23,25 % | 0,6325 | criticality |
| LUAD nul s9601 | 515 | 0,1181 | 0,1175 | 0,3206 | 4,6279 | UP 40,57 % | 1,0553 | divergence |
| LUAD nul s9602 | 515 | 0,1067 | 0,1060 | 0,3171 | 2,5267 | UP 38,48 % | 0,6439 | criticality |
| BRCA réel | 1 093 | 0,3200 | 0,3181 | 0,3508 | 5,0557 | UP 38,43 % | 0,6919 | divergence |
| BRCA nul 42 | 1 093 | 0,1018 | 0,1012 | 0,3600 | 4,5200 | DOWN 18,08 % | 0,8708 | divergence |
| BRCA nul s9601 | 1 093 | 0,1144 | 0,1140 | 0,3198 | 5,0909 | UP 17,16 % | 0,8284 | divergence |
| BRCA nul s9602 | 1 093 | 0,1210 | 0,1194 | 0,3596 | 4,5139 | UP 18,81 % | 0,8281 | divergence |

Écarts réel − nul (par bras) :

| Écart | LUAD vs nul 42 | LUAD vs s9601 | LUAD vs s9602 | BRCA vs nul 42 | BRCA vs s9601 | BRCA vs s9602 |
|---|---|---|---|---|---|---|
| d_`maxsep` | +0,0140 | +0,0321 | +0,0436 | **+0,2182** | **+0,2056** | **+0,1990** |
| d_S_sep | +0,0152 | +0,0325 | +0,0440 | +0,2168 | +0,2041 | +0,1987 |
| d_MC | −0,0203 | +0,0030 | +0,0064 | −0,0092 | +0,0310 | −0,0088 |
| d_Delta | +0,0137 | −2,1171 | −0,0159 | +0,5357 | −0,0352 | +0,5418 |
| d_falsification | +0,0064 | −0,4164 | −0,0051 | −0,1788 | −0,1365 | −0,1362 |

Cascades (T−2 / T−1 / T0 / T+1 / T+2, en %) et dérivées :

| Run | Cascade | max F1 | max F2 |
|---|---|---|---|
| LUAD réel | 0,7610 / 46,6916 / 68,6177 / 80,8214 / 80,8214 | 5,4057 | 17,2461 |
| LUAD nul 42 | 0,0000 / 0,6145 / 3,6145 / 69,6060 / 69,6060 | 5,3803 | 10,6233 |
| LUAD nul s9601 | 0,0000 / 13,2595 / 80,8214 / 91,6903 / 91,6903 | 4,4897 | 13,6409 |
| LUAD nul s9602 | 0,1902 / 38,9868 / 47,0299 / 69,6060 / 69,6060 | 5,0645 | 13,6210 |
| BRCA réel | 0,0000 / 0,0894 / 11,2527 / 23,1883 / 23,1883 | 6,7877 | 30,1192 |
| BRCA nul 42 | 0,1789 / 13,3938 / 35,6115 / 94,3074 / 94,3074 | 6,8615 | 25,4989 |
| BRCA nul s9601 | 0,4472 / 21,9367 / 86,3148 / 94,3794 / 94,3794 | 7,6125 | 32,2386 |
| BRCA nul s9602 | 0,0000 / 7,7648 / 72,3868 / 83,1000 / 83,1000 | 6,1820 | 31,0386 |

SHA-256 des `master_results.json` : LUAD réel `b8b995f4…2a113`,
nul 42 `5738ffdf…93d26`, s9601 `f026e4df…4f`, s9602
`25e6d69c…45a8` ; BRCA réel `5859072b…1d7ab2`, nul 42
`326b7694…ab763`, s9601 `5cb7ffcb…f418`, s9602 `e84d68aa…723da2`
(SHA complets dans `universalite_896_table.json`).

## §8.96.5 Bras A — LUAD : NON

La barre gelée exige d'abord un écart `maxsep` réel − nul 42
supérieur à 0,07 : mesuré **+0,0140**, soit un cinquième du
plancher. Les deux nuls frais ne sauvent rien : +0,0321 et
+0,0436, tous deux sous le plancher — 0/2, alors que la barre
exigeait au moins 1/2. Le deuxième indicateur ne compense pas :
MC est négatif contre le nul graine 42 (−0,0203, le nul
au-dessus du réel) et quasi nul contre les frais (+0,0030,
+0,0064) ; Delta est quasi nul contre le nul graine 42
(+0,0137) et négatif contre les frais (−2,1171 contre s9601,
−0,0159 contre s9602). Seul L7a donne une direction
concordante contre le nul graine 42 (réel UP 42,05 % contre nul
DOWN 23,25 %, avec désaccord interne sur le nul) — mais les
deux nuls frais votent UP comme le réel (40,57 % et 38,48 %),
donc L7a ne sépare pas le réel des nuls frais. La falsification
déclenche partout (0,6389 réel ; 0,6325 / 1,0553 / 0,6439
nuls) : elle ne discrimine rien ici, et son maximum du lot est
un nul (s9601, 1,0553). Les cascades ne séparent pas non plus :
le réel (0,7610 / 46,6916 / 68,6177 / 80,8214 / 80,8214) est
entouré de nuls qui couvrent toute la gamme (T0 nul : 3,61 %,
80,82 %, 47,03 %). F1/F2 non plus : F1 réel 5,4057 contre
5,3803 / 4,4897 / 5,0645 ; F2 réel 17,2461 contre 10,6233 /
13,6409 / 13,6210 — le réel est le plus haut en F2, mais sans
barre gelée sur F1/F2, ce n'est qu'une observation, pas un
verdict. Le régime ne sépare pas : réel criticality, nuls
criticality / divergence / criticality.

Reproduction du §8.27 : le run v6.2 réel reproduit presque
exactement les chiffres v6.0/v6.1 — cascade 0,7610 / 46,6916 /
68,6177 / 80,8214 / 80,8214 contre 0,76 / 46,69 / 68,62 / 80,82 /
80,82 ; Delta 2,5108 contre 2,511 ; L7a UP 42,05 % contre
42,11 %. Le NON en LUAD n'est donc pas un artefact de version :
le même instrument, sur les mêmes données, donne les mêmes
chiffres et ne sépare toujours pas. C'est cohérent avec le
§8.27 (v6 ne séparait pas réel/nul en LUAD : Delta 2,511 contre
2,497) et avec l'audit §8.90 (volet 2) : sur les paires
inventoriées, le nul dépasse le réel en MC sur LUAD (−0,020,
déjà noté).

## §8.96.6 Bras B — BRCA : CONFIRME (partiel)

La barre gelée est franchie sur ses trois conditions. Écart
`maxsep` réel − nul 42 : **+0,2182** (0,3200 contre 0,1018),
trois fois le plancher 0,07. Deuxième indicateur concordant :
Delta **+0,5357** contre le nul graine 42 (5,0557 contre
4,5200) — un écart cinq fois supérieur à l'échelle typique
|Δ| ≤ 0,10 observée sur la moitié des paires au §8.62 — et
L7a UP 38,43 % contre DOWN 18,08 % (désaccord interne sur le
nul). Nuls frais : **+0,2056 et +0,1990, 2/2 au-dessus du
plancher**. S_sep suit `maxsep` (stabilité 0,9872–0,9988 sur
les 8 runs) : écarts +0,2168 / +0,2041 / +0,1987. La cascade
réelle est comprimée très tôt (0,0000 / 0,0894 / 11,2527 /
23,1883 / 23,1883) contre des nuls tardifs (T0 35,61 % /
86,31 % / 72,39 % ; T+1/T+2 83–94 %) : le réel et les nuls
n'ont pas la même forme de cascade, dans le même sens que
l'écart `maxsep`.

Les réserves, mesurées, pas minimisées : (1) MC ne sépare pas
— −0,0092 contre le nul graine 42, +0,0310 contre s9601,
−0,0088 contre s9602, le nul au-dessus du réel sur 2 nuls sur
3 ; (2) Delta échoue contre le nul frais s9601 (−0,0352 ;
5,0557 contre 5,0909) ; (3) la falsification est plus haute
sur les trois nuls (0,8708 / 0,8284 / 0,8281) que sur le réel
(0,6919), alors qu'elle déclenche partout (> 0,5 sur les 8
runs) — elle ne discrimine rien ici non plus ; (4) L7a ne
sépare que contre le nul graine 42 : les deux nuls frais
votent UP comme le réel (17,16 % et 18,81 %, avec désaccord
interne), à des confiances plus faibles ; (5) L7b est FRAGILE
sur les 8 runs (§8.96.7) ; (6) le diagnostic de bruit du réel
est le plus fort du lot (§8.96.7). La confirmation est donc
partielle au sens gelé du terme : elle porte sur `maxsep`,
Delta (2 nuls sur 3) et L7a (1 nul sur 3), pas sur la batterie
entière — et elle ne dit rien d'un troisième cancer.

## §8.96.7 La batterie entière, loupe par loupe

**Q1–Q6 (médianes sur 348 entrées flux × estimateur).**

| Run | Q1 | Q2 | Q3 (= Q1) | Q4 | Q5 | Q6 |
|---|---|---|---|---|---|---|
| LUAD réel | 0,3048 | 0,4999 | 0,3048 | 0,2202 | 9,0143 | 17,7422 |
| LUAD nul 42 | 0,2868 | 1,8172 | 0,2868 | 0,2395 | 7,6272 | 20,0937 |
| LUAD nul s9601 | 0,3423 | 1,4440 | 0,3423 | 0,2236 | 8,7164 | 12,8356 |
| LUAD nul s9602 | 0,2956 | 1,1538 | 0,2956 | 0,2358 | 8,5081 | 17,4259 |
| BRCA réel | 0,3483 | 3,5171 | 0,3483 | 0,1536 | 11,0289 | 32,3646 |
| BRCA nul 42 | 0,3655 | 0,6806 | 0,3655 | 0,2094 | 12,3843 | 42,1275 |
| BRCA nul s9601 | 0,3164 | 1,3328 | 0,3164 | 0,1520 | 11,4002 | 30,1946 |
| BRCA nul s9602 | 0,3238 | 1,0365 | 0,3238 | 0,2185 | 13,3576 | 38,7783 |

Q3 recopie Q1 sur les 8 runs (couverture faible, règle connue
du pipeline). Q1, Q4, Q5, Q6 ne séparent pas le réel des nuls
dans aucun des deux bras (les médianes réelles sont au milieu
des médianes nulles). Q2 est le seul score Q qui bouge :
LUAD réel 0,4999, le plus bas des 4 runs LUAD (nuls 1,8172 /
1,4440 / 1,1538) ; BRCA réel 3,5171, le plus haut des 4 runs
BRCA (nuls 0,6806 / 1,3328 / 1,0365) — dans des sens opposés
selon le bras, sans barre gelée : c'est une observation, pas
un discriminateur.

**Quatre tests de bruit (médianes sur 1 044 lignes ;
comptages « computed » entre parenthèses).**

| Run | Étape 1 : ratio candidat/bruit blanc | Étape 2 : Δ corrélation | Étape 3 : Hurst moyen | Étape 4 : Δ pente |
|---|---|---|---|---|
| LUAD réel | 0,3700 (959) | +0,0339 (927) | 0,7889 (957) | −0,1111 (963) |
| LUAD nul 42 | 1,7470 (964) | −0,5346 (912) | 0,7918 (963) | +0,7810 (947) |
| LUAD nul s9601 | 3,1384 (1008) | −0,6105 (978) | 0,7899 (969) | +0,8037 (984) |
| LUAD nul s9602 | 6,6088 (961) | −0,3237 (927) | 0,7759 (963) | +0,4431 (952) |
| BRCA réel | 1,6688 (1015) | −0,6649 (926) | 0,7455 (974) | +0,7414 (992) |
| BRCA nul 42 | 1,8494 (993) | −0,0658 (959) | 0,7833 (993) | −0,1464 (999) |
| BRCA nul s9601 | 1,0596 (1018) | −0,4943 (966) | 0,7733 (984) | +0,9103 (1001) |
| BRCA nul s9602 | 26,8547 (987) | +0,1278 (953) | 0,7934 (996) | +0,0450 (996) |

Lecture : l'étape 1 ne sépare pas — en LUAD, les nuls ont des
ratios plus hauts que le réel (1,75 / 3,14 / 6,61 contre 0,37),
en BRCA le réel est au milieu des nuls (1,67 contre 1,85 /
1,06 / 26,85). L'étape 3 (Hurst moyen) ne sépare pas non plus
(0,7455–0,7934 sur les 8 runs, sans ordre réel/nul). Les étapes
2 et 4 séparent en LUAD seulement, par le signe : Δ corrélation
réel +0,0339 contre −0,53 / −0,61 / −0,32 ; Δ pente réel
−0,1111 contre +0,78 / +0,80 / +0,44 — mais en BRCA le réel
(−0,6649 ; +0,7414) est indiscernable des nuls. Aucun des
quatre tests ne sépare sur les deux bras à la fois.

**Diagnostic de bruit (score proxy moyen, 12 flux).** LUAD :
réel 0,4848 (« Mixte », MEDIUM, colonne MUC17) contre nuls
0,5048 / 0,3974 / 0,3738 — pas de séparation. BRCA : réel
**0,6945** (« Proxy de variance modéré », MEDIUM_HIGH, colonne
PGC) contre nuls 0,4634 / 0,5111 / 0,5183 — le réel BRCA porte
le diagnostic de bruit le plus fort des 8 runs du lot, au-dessus
de tous ses nuls. Ce n'est pas une preuve contre la séparation
BRCA (le diagnostic est un proxy, non décisionnel), mais c'est
une réserve nommée : la paire BRCA qui sépare le plus en
`maxsep` est aussi celle dont le réel porte le plus de
signature de variance résiduelle.

**L7a / L7b.** L7a : réel UP dans les deux bras (LUAD 42,05 %,
BRCA 38,43 %) ; nul graine 42 DOWN dans les deux bras (23,25 %,
18,08 %, désaccord interne) ; nuls frais UP dans les deux bras
(LUAD 40,57 % / 38,48 % sans désaccord ; BRCA 17,16 % /
18,81 % avec désaccord). L7b : **FRAGILE (mode light) sur les
8 runs**, sans exception. Le check de stabilité walk-forward
échoue sur les 8 runs (T0 variable, t0_std > 10 partout) ; la
stabilité d'horizon échoue sur 3 runs (LUAD nul 42, LUAD nul
s9602, BRCA réel) ; la cohérence interne échoue sur 4 nuls
(LUAD nul 42, BRCA nul 42, BRCA s9601, BRCA s9602) et passe
sur les deux réels. Comme au §8.27 et dans les rotations
(§8.32), L7b est non-informatif ici : il dit FRAGILE sur le
réel et sur les nuls alike — il ne porte aucun des deux
verdicts, et ne doit jamais être rapporté seul comme une
mesure de fragilité de l'instrument.

**Régimes et vecteur D.** LUAD réel : criticality
(d_sat 1,6563, d_crit 3,1463, d_div 4,1671, d_null 2,5074) ;
BRCA réel : divergence (d_sat 1,6454, d_crit 3,1876,
d_div 6,7011, d_null 2,4957). Mais les nuls portent les mêmes
étiquettes : LUAD nuls criticality / divergence / criticality,
BRCA nuls divergence / divergence / divergence. Le régime ne
sépare pas. Delta, lui, est la différence d_sat/d_div portée
par la couche géométrique : en LUAD le nul s9601 (Delta 4,6279,
d_div 6,2790) dépasse le réel ; en BRCA le nul s9601
(Delta 5,0909, d_div 6,7306) dépasse aussi le réel — dans les
deux bras, le nul frais s9601 est le Delta le plus haut du
bras. C'est la même fragilité que celle du §8.62 : Delta ne
suffit pas comme discriminateur.

**MC : recomposition et anomalie.** Le score MC stocké est
reproduit exactement (écart 0,0) par la formule du §8.50
(0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·acuité)
sur 6 runs sur 8. Sur 2 runs — BRCA nul graine 42 et BRCA nul
s9602 — l'écart est de **0,0900** (recomposé 0,4499 contre
stocké 0,3600 ; recomposé 0,4495 contre stocké 0,3596). Ces
deux runs sont les seuls du lot dont la robustesse est haute
(0,6634 et 0,6376, contre ≤ 0,12 ailleurs). Aucune explication
n'est inventée ici : l'anomalie est consignée telle quelle.
Elle ne change pas le sens des écarts MC en BRCA — avec les
valeurs recomposées, les écarts réel − nul seraient −0,0991
et −0,0987 au lieu de −0,0092 et −0,0088, toujours négatifs :
MC ne sépare pas en BRCA dans les deux lectures. En LUAD, la
recomposition est exacte sur les 4 runs et MC ne sépare pas
non plus.

## §8.96.8 Ce qui n'a pas été testé (nommé, pas comblé)

- **La structure analogue (confirmation totale).** Aucun test
  direct de corrélation bloc/axe n'a été fait : ni le bloc
  estomac/mucus variant avec KRAS en LUAD, ni un bloc
  équivalent variant avec ESR1 en BRCA. Les fichiers
  `luad_896_fresh.json`, `luad_896_table.json`,
  `brca_896_fresh.json`, `brca_896_table.json` annoncés au
  §4 du protocole n'existent pas sur disque ; les tables
  produites pour cette section sont `universalite_896_table.json`
  et `universalite_896_table.csv` (§8.96.3). Le verdict
  « total » n'est pas rendu : il attendrait son propre
  protocole, avec les mêmes gènes et les mêmes seuils que
  §8.33/§8.66.
- **La série LUAD n = 45…515 (§8.62, ensemble B).** Le
  protocole prévoyait de la relire en sensibilité (le pipeline
  sépare-t-il à petit n en LUAD comme en PAAD ?). Elle n'a pas
  été relue dans cette section : le NON en LUAD porte sur
  n = 515 seul.
- **Le témoin COAD.** Aucun run COAD neuf dans ce lot. Les
  valeurs §8.27 sont rappelées seulement : réel Delta 4,619
  contre nul 4,599 — le v6 ne séparait pas non plus en COAD,
  comme attendu (§8.27 : programme KRAS du côlon différent).
- **Aucun autre cancer.** GBM / UVM (§8.33) ne sont pas
  rouverts, comme gelé.

## §8.96.9 Ce que ça change pour l'universalité

Avant ce chantier, l'universalité tenait à trois points
(§8.90, volet 4) : `maxsep` seul 6/8, rotations sans doublon
37/48, A2 10/15 — tous pancréas, plus l'Ising jamais tourné
en v6/v6.1/v6.2 dans ce livre blanc. Après ce chantier, le
tableau est mixte et mesuré : le pipeline sépare le réel du
nul sur un cancer hors pancréas (BRCA, par `maxsep` surtout)
et ne le sépare pas sur un autre (LUAD, par aucun
indicateur) — avec les mêmes 12 flux, le même pipeline, la
même barre. Trois lectures en découlent. Premièrement, le mot
« universel » reste exagéré tel quel (§8.90.4) : un bras sur
deux, et une confirmation partielle seulement. Deuxièmement,
le bras qui sépare (BRCA) est celui dont l'axe est un vrai
classificateur biologique du cancer (ESR1 sépare ER+ / ER−,
écart-type 3,190, le plus fort des candidats) — alors que
l'axe KRAS, analogue exact de PAAD, ne sépare pas en LUAD :
ce qui voyage, ce n'est pas l'axe KRAS, c'est la capacité de
l'instrument à lire un ordre fort quand il existe. C'est une
lecture d'analyse, pas une règle : un seul bras la porte.
Troisièmement, la fragilité de Delta est confirmée hors
pancréas (§8.62) : dans les deux bras, un nul frais dépasse
le réel en Delta. Pour la suite : un troisième cancer ne se
prédit pas, il se teste — avec sa propre barre gelée, son
propre axe choisi avant les runs, et le test de structure
analogue fait cette fois, pas seulement annoncé.

## §8.96.10 Limites

- Deux bras seulement, une paire réelle par bras, trois nuls
  par bras : les écarts reposent sur 8 runs. La distribution
  nulle est empirique (3 permutations par bras), ses quantiles
  sont bruités.
- LUAD et PAAD partagent les 12 mêmes flux : en LUAD, une
  structure analogue trouvée aurait pu tenir aux gènes
  choisis, pas au cancer — le bras BRCA (mêmes 12 flux aussi,
  gate 12/12 sans remplacement) ne lève pas cette limite
  autant que prévu : les flux n'ont pas été adaptés au sein,
  ils ont passé le gate tels quels.
- Firehose 2016-01-28 est un millésime figé (2016) : les
  résultats portent sur ces données, pas sur TCGA actuel —
  choix de comparabilité, consigné, pas limite cachée.
- Les sous-échantillons préfixe du §8.62 ne sont pas des
  cohortes indépendantes (rappel du protocole).
- L7b light seulement (pas de `--l7b-full`) ; la recomposition
  MC présente une anomalie non élucidée sur 2 runs (§8.96.7).
- Aucune recommandation clinique, jamais ; données d'essais
  seulement, à discuter avec un oncologue (règle de sécurité
  §8.90).

## §8.96.11 Provenance

- Protocole gelé : `PROTOCOL_universalite_896.md`, SHA-256
  `1349b9963a1a267dafaacaa8fd5df215d680ba1fa11d5e0e29dad635efe848d8`
  (le SHA `24566611…5fc9` cité dans `PROVENANCE_896.md` est
  celui de la version au gel du squelette ; le fichier a été
  complété ensuite par l'addendum de correction — le texte
  gelé est intact, l'addendum l'applique).
- Provenance : `PROVENANCE_896.md`, SHA
  `d9554cf3923155696d3773c3fc5c2d52c94bb15f1bd9aea4eb0567cc15a92c68`.
- Addendum correction (Zackary, 21 nov. 2026 12h03) :
  `ADDENDUM_correction_20261121_896.md`, SHA
  `ff8408644894898ae82b63a702f1595bf29f58e511af0244ee2df4daff97f132`.
- Addendum axe BRCA : `ADDENDUM_axe_brca_896.md`, SHA
  `aed56a92aee3c7cb545bcafcb9af786172246449fcf04a08222ddc9345f048ba`.
- Code : pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié par `sha256sum` et dans les logs des deux lots).
- Construction BRCA : `build_fluxes_brca_896.py`, SHA
  `7f60c0feeaf90df64700635826f8915fa875ff493fc5745b8dd1348f447f62b4` ;
  nuls LUAD : `build_luad_nulls_896.py`, SHA
  `5e79c90fb9313bef874e1c6758a7562860c9117af02f2fd6916dea71c25b7e04`.
- Téléchargement BRCA : `brca_896_download.json`, SHA
  `80d0f7ce8a07987f8f441d23c9f768e0f6159910930fd33f88b62eb2481c244e`
  (tarball MD5 `b4eed57d14ca2fa563ca0dd05d4fba7f`, matrice
  interne MD5 `96d707af16947605116dfbec6e3c050e`).
- Nuls LUAD frais : `luad_896_nulls_files.json`, SHA
  `d75c13018c4843257f978c40eb92e9b1512c3f307fc50101ab6305e625195488`.
- Flux (SHA-256) : LUAD réel `d407849b…38091e`, nul 42
  `93766e8c…978a6b`, s9601 `6e652a42…c72d1`, s9602
  `358188cf…336f` ; BRCA réel `c08ebf41…2d84`, nul 42
  `f8234a33…c88b29`, s9601 `5713da1f…57f7e`, s9602
  `88a1b9aa…62a8` (SHA complets dans
  `universalite_896_table.json`).
- Logs des lots : `runs_luad_896.log`, `runs_brca_896.log`
  (8/8 exit 0, SHA v6.2 vérifié au lancement et à la fin).
- Lecture : `extract_universalite_896.py`, SHA
  `583397ed853eae6a48a0ee1d7e8d27cf625b2f7107a8e70792a41795974fa210` ;
  tables `universalite_896_table.json` (SHA
  `cfddd6d8a1d46d78ae107b08f3dd541069a25e01af94d13450c1e1eb4df1fe24`)
  et `universalite_896_table.csv` (SHA
  `47807fd2116813f9695ddefc5cef8b28055ce3c9a616c5ddab0352b7b3ef2cfc`).
- Sources externes : Broad GDAC Firehose stddata 2016-01-28
  (LUAD : `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/LUAD/20160128/` ;
  BRCA : `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/BRCA/20160128/`).
  Antériorités citées : §8.27 (pan-cancer), §8.33 (flux et
  blocs), §8.62 (Delta, série LUAD n = 45…515), §8.90 (audit,
  volet 4 : universalité).

## §8.96.12 Ce qui manque (déclaré)

- Le test direct de la structure analogue (bloc estomac/mucus
  ou équivalent variant avec l'axe) : absent, à faire sous son
  propre protocole avant tout verdict « total ».
- Les fichiers `luad_896_fresh.json`, `luad_896_table.json`,
  `brca_896_fresh.json`, `brca_896_table.json` annoncés au §4
  du protocole : non produits ; remplacés ici par
  `universalite_896_table.json` / `.csv` (même contenu :
  8 runs, écarts, SHAs).
- La relecture de la série §8.62 en sensibilité de n (LUAD).
- L'élucidation de l'anomalie de recomposition MC sur les
  deux nuls BRCA à robustesse haute (§8.96.7).
- La mise à jour de `PROVENANCE_896.md` (squelette) avec les
  SHAs des flux BRCA et des runs : les SHAs sont dans cette
  section et dans `universalite_896_table.json`, pas encore
  reportés dans le fichier de provenance — dette de
  consignation, pas de résultat.
