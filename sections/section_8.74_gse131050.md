# §8.74 — GSE131050 (PurIST), lot Yeh_seq FF : la douzième paire principale CONFIRME — de justesse, et consolidée par les nuls frais

## Verdict d'abord

**CONFIRME — la douzième paire principale indépendante, GSE131050
lot Yeh_seq FF (n = 42 tumeurs indépendantes), donne
`d_maxsep = +0,0739` (réel 0,3220 contre nul 0,2481), au-dessus
du plancher 0,07 — de 0,0039 seulement. Elle passe. A2 étendu :
8/12 au-dessus du plancher, 10/12 positifs — la condition C3 du
§8.59.8, levée au §8.71, RESTE LEVÉE (ce chantier est une
confirmation supplémentaire, pas une condition ; il ne rouvre
rien). Le passage est CONSOLIDÉ par les nuls frais : les trois
écarts (graine 42 : +0,0739 ; graine 8741 : +0,0976 ; graine
8742 : +0,1113) sont tous au-dessus du plancher, min +0,0739,
médiane +0,0976, max +0,1113. L'adoption pleine de `maxsep`,
décidée par Zackary le 20 nov. 2026 à 13h04, reste sa décision :
ce chantier ne la rouvre pas — il la consolide par une
confirmation indépendante mesurée, comme le protocole le
prévoyait.**

| Porte (PROTOCOL_maxsep_gse131050_874.md §7, gelé) | Exigé | Mesuré 20 nov. 2026 | Sort |
|---|---|---|---|
| Paire indépendante : `d_maxsep > 0,07` et positif | > 0,07 | **+0,0739** (réel 0,3220, nul 0,2481) | **CONFIRME** |
| A2 étendu (12 paires) | 8/12 et 10/12 positifs | **8/12, 10/12 positifs** | **PASSE** |
| LOO sur 12 paires (descriptif) | Retrait d'une paire passante : 7/11 | **7/11** après retrait de chaque paire passante | **PASSE** |
| Exactitude de l'extraction | 4/4 à 0,0 exact | **4/4, écart max 0,0** | **PASSE** |
| Nuls frais (§7, `d` dans [−0,07 ; +0,14[) | 2 nuls frais si proche du plancher | **Courus : +0,0739 dans l'intervalle ; 3/3 écarts > 0,07** | **CONSOLIDÉ** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que la
douzième paire principale, mesurée aujourd'hui sur une cohorte
jamais utilisée dans ce projet (UNC, 42 tumeurs PDAC primaires
flash-frozen, plateforme Illumina NextSeq 500), sépare le réel
du nul en `maxsep` dans le bon sens et au-delà du plancher gelé —
mais de justesse : +0,0739 contre 0,07 exigé, soit 0,0039 de
marge sur la paire graine 42. Il dit aussi que cette marge
étroite ne tient pas à un tirage de nul chanceux : les deux nuls
frais donnent des écarts PLUS grands (+0,0976 et +0,1113), et
l'étendue des trois nuls (0,0374) est petite devant l'écart
médian (+0,0976) — à la différence du §8.70, où le verdict
tenait au tirage du nul (étendue 0,0972 entre 3 nuls à n = 51,
écart 0,0567). Il dit enfin que le verdict de suffisance ne
tient plus à une seule paire : retirer n'importe laquelle des 8
paires passantes laisse 7/11, qui satisfait encore la barre A2
d'origine (≥ 6/8). Il ne dit pas que `maxsep` est validé en
général : c'est une confirmation sur 12 paires comptées, dont 4
restent non passantes (GSE71729, GSE62452, GSE21501, GSE79668),
et les scores compagnons ne suivent pas tous (MC à peine positif
+0,0114, Delta plat +0,041 — voir §8.74.5). Il ne dit pas non
plus que l'adoption pleine est « prouvée » par ce chantier seul :
elle a été décidée par Zackary après lecture des §8.56/§8.59/
§8.64, et cette section est la vérification a posteriori que le
protocole prévoyait — elle consolide la décision, elle ne la
fonde pas rétroactivement.

**Fragilité, dite en tête.** Le verdict tient à une seule paire
mesurée aujourd'hui — comme tous les verdicts de ce dossier.
Ici la fragilité a un nom précis : la marge sur la paire graine
42 est de 0,0039, soit 5,6 % du plancher. Deux lectures
s'opposent et toutes deux sont consignées : (a) la lecture
« consolidée » — les trois nuls donnent des écarts au-dessus du
plancher, et le plus petit écart (+0,0739) est celui du nul
graine 42, c'est-à-dire que le verdict ne dépend pas d'un nul
favorable ; (b) la lecture « étroite » — si le nul graine 42
avait été tiré 0,004 plus haut, la paire aurait été PARTIELLE
comme GSE79668, et l'écart médian des trois nuls (+0,0976)
reste modeste devant les écarts des paires TCGA (+0,2928,
+0,3675) et devant le +0,2045 du §8.71. La règle gelée tranche
le vocabulaire, pas la prudence : le passage est dit
« consolidé » parce que 3/3 écarts dépassent le plancher — la
marge étroite reste écrite en tête de cette section, et le
lecteur juge. En revanche, la paire échoue à la barre
descriptive du plancher équivalent-sep (écart `sep` 0,0448
contre 0,1155 exigé — voir §8.74.5) : `sep` ne suit pas `maxsep`
jusqu'à sa propre barre, comme aux §8.59/§8.64/§8.71 où `sep`
seul avait été rejeté. C'est consigné tel quel, sans sauver ni
condamner le verdict, dont le critère gelé est `maxsep` et lui
seul.

Protocole gelé : `PROTOCOL_maxsep_gse131050_874.md` (20 nov.
2026, SHA `3f34f4ff…1d5f` au gel, inchangé). Critère de passage
écrit AVANT tout run (§7 du protocole) ; aucune repondération,
aucun nouveau terme, aucune redéfinition du plancher après avoir
vu les chiffres. Les nombres des §8.56/§8.59/§8.64/§8.69/§8.70/
§8.71 étaient la motivation, pas le verdict : le verdict repose
sur les 4 runs mesurés ci-dessous.

## 8.74.1 — La paire mesurée : GSE131050, lot Yeh_seq FF, et pourquoi elle est indépendante

**Cohorte : GSE131050, NCBI GEO** — Rashid et coll., 42 tumeurs
PDAC primaires réséquées, flash-frozen, plateforme Illumina
NextSeq 500 GPL18573, article Rashid et coll. 2020 (*Clin Cancer
Res*, 26(1):82–92, PMID 31754050, doi
10.1158/1078-0432.CCR-19-1467). Provenance complète :
`PROVENANCE_874.md`.

**Indépendance, en cinq points (protocole §2).**
1. **Jamais utilisée dans ce projet.** Aucun CSV de flux, aucun
   run, aucun JSON, aucune valeur `maxsep` n'existait pour
   GSE131050 avant ce chantier. Vérifié par grep avant le gel :
   la chaîne exacte « GSE131050 » ne figurait que comme « piste
   restante non vérifiée » dans les trois fichiers du §8.71 et
   dans le livre blanc aux mêmes endroits.
2. **Nouveaux patients, nouveau centre, nouvelle plateforme.**
   Données nouvelles générées pour l'étude PurIST : lot Yeh
   collecté de novo à l'UNC (Lineberger Comprehensive Cancer
   Center, Tissue Procurement Core Facility) — tumeurs
   réséquées, congelées flash en azote liquide ; patients
   distincts de TCGA, ICGC PACA-AU et des cohortes GEO déjà
   utilisées ; plateforme Illumina NextSeq 500 (GPL18573),
   distincte de toutes les plateformes V1 et des confirmations
   (RNA-seq TCGA, Illumina ICGC, Affymetrix GPL20769/GPL6244/
   GPL13667/GPL15048/GPL570, Agilent GPL4133/GPL7264/GPL14550,
   Illumina HiSeq GPL11154/GPL16791).
3. **Les jeux publics de la méta-analyse PurIST ne sont pas dans
   GSE131050.** L'article utilise, pour la méta-analyse et
   l'entraînement de PurIST, des jeux publics (TCGA_PAAD,
   PACA_AU_seq/array, Moffitt_GEO_array, Aguirre, COMPASS) —
   ces jeux ne sont PAS redéposés dans GSE131050 : la série ne
   contient que les deux fichiers supplémentaires Yeh_seq et
   Linehan_seq, données nouvelles. GSE131050 n'est donc pas un
   re-découpage d'une cohorte déjà tenue. Caveat consigné :
   les titres étant anonymisés (codes `S###` / `MMDDT#`), une
   exclusion formelle, identifiant par identifiant, d'un
   recouvrement avec TCGA_PAAD est impossible — aucun
   échantillon ne porte de code-barres TCGA et la collecte est
   décrite comme de novo dans l'article ; c'est le même
   standard que le §8.71 (titres / GSM inspectés, aucun
   code-barres TCGA).
4. **Même construction que les autres paires principales GEO.**
   Variante (a) : les 12 mêmes gènes que la v4 TCGA (PGC, REG4,
   CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5,
   CLCA1, MUC16), ordre = KRAS croissant, sans correction, cas
   complets, nul = lignes permutées graine 42. La paire est donc
   comparable aux 11 paires comptées par construction. Une
   seule adaptation, gelée au protocole §4.4 et justifiée au
   §8.74.7 : l'unité d'analyse est la TUMEUR INDÉPENDANTE, pas
   la colonne — les réplicats FF d'une même tumeur sont agrégés
   par médiane (précédent du projet : agrégation par médiane
   des sondes multiples vers un même symbole).
5. **Pas un re-test déguisé.** Ce n'est ni une relecture d'un JSON
   existant (§8.64.7 : « pas une relecture »), ni une rotation
   déjà comptée, ni un sous-ensemble d'une paire V1, ni un
   nouvel ordre sur des CSV existants (nouveaux CSV, nouveaux
   runs, 4 runs v6.2 frais). La sous-série NanoString GSE131051
   n'est pas utilisée : ce n'est pas de l'expression RNA-seq
   codante en comptages géniques.

**Ce que GSE131050 n'est pas.** Ce n'est pas une cohorte choisie
pour ses résultats : aucun `maxsep` GSE131050 n'existait quand
le protocole a été gelé. Ce n'est pas non plus la série prise en
bloc : seuls les 42 FF primaires (une ligne par tumeur
indépendante) servent à la paire — les 28 PDX, les 45 FNA et
les 5 FFPE primaires du lot Yeh, et les 66 biopsies du lot
Linehan, sont exclus et comptés (§8.74.7).

## 8.74.2 — Les runs et l'extraction

**Runs v6.2 mode fast : 4/4, exits 0/0/0/0.** Manifeste
`manifest_v62_874.txt` (réel + nul graine 42), lanceur
reprenable `run_v62_lot.sh`, journal `runs_v62_874.log`
(FIN 2026-11-20T23:22:49Z, 2/2 terminés, 0 échec) ; manifeste
`manifest_v62_874_frais.txt` (nuls graines 8741/8742), journal
`runs_v62_874_frais.log` (FIN 2026-11-20T23:29:08Z, 2/2
terminés, 0 échec). Unités systemd `v62-874` et `v62-874b`
(jamais nohup). **Incident consigné : la machine a redémarré
entre les deux lots** (uptime 0 min constaté à 23h24 UTC) — le
lot principal était déjà terminé (FIN consignée 23:22:49Z) ;
aucune reprise à l'aveugle, aucun dossier de run touché, le lot
des nuls frais a été lancé après le redémarrage sur une machine
saine. SHA du pipeline revérifié avant ET après chaque lot :
`f07567c4…c3abf`, inchangé.

**Extraction : 4/4 à 0,0 exact.** `extract_874.py` (réutilise
`extract()` de `extract_858.py`, original intact) lit les 4
`master_results.json` ; `verify_874.py` (chemin distinct,
relecture directe par `json.load`) recoupe `maxsep`, ancien MC
et stabilité à 0,0 exact sur les 4 runs
(`maxsep_874_verify.json`, verdict OK). Version lue :
`v6.2.0-L7aL7b-CohenD-short` sur les 4 runs.

| Run | n | maxsep | ancien MC | S_sep | Delta | L7a | Cascade (Q1–Q5, %) |
|---|---|---|---|---|---|---|---|
| Réel Yeh FF | 42 | **0,3220** | 0,3985 | 0,3187 | 1,470 | up 0,335 | 45,7 / 68,7 / 76,0 / 80,8 / 90,4 |
| Nul graine 42 | 42 | 0,2481 | 0,3871 | 0,2445 | 1,429 | up 0,347 | 0,0 / 21,3 / 28,4 / 33,2 / 43,1 |
| Nul graine 8741 | 42 | 0,2244 | 0,3835 | 0,2207 | 1,368 | up 0,328 | 48,5 / 73,6 / 80,8 / 88,0 / 100,0 |
| Nul graine 8742 | 42 | 0,2106 | 0,3833 | 0,2099 | 1,250 | up 0,345 | 11,8 / 78,4 / 83,2 / 90,4 / 100,0 |

Valeurs complètes : `maxsep` réel 0,32197053707321405 ; nul s42
0,24805139580066674 ; nul s8741 0,2243751034172152 ; nul s8742
0,21064775318011728. Stabilité : réel 0,9899 ; nuls 0,9857 /
0,9838 / 0,9966. Seuils MC : réel 40,91 ; nuls 50,00 / 54,55 /
59,09. F1/F2 après seuil : réel 0,4775 / 0,5248 ; nul s42
1,7075 / 1,0350 ; s8741 2,1622 / 0,3382 ; s8742 1,3190 / 1,7240
(descriptif, voir §8.74.5). Falsification : INDISPONIBLE sous
n = 75 (n = 42) — les valeurs brutes du pipeline (1,302 /
1,313 / 1,678 / 1,370) figurent dans `extract_874.json` sans
être interprétées, comme au §8.71. L7b : FRAGILE sur les 4 runs
— l'audit L7b est clos comme non-informatif (il dit FRAGILE
sur le réel comme sur les nuls) ; il n'est pas rapporté comme
une mesure de fragilité.

## 8.74.3 — Le verdict étendu : A2 à 12 paires

Table des 12 paires principales comptées (valeurs des §8.56 /
§8.69 / §8.70 / §8.71 reprises telles quelles, jamais
recalculées ; §8.74 mesuré ici). Écart = maxsep réel − maxsep
nul. Plancher 0,07.

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
| **GSE131050 Yeh FF (§8.74)** | **0,3220 / 0,2481** | **+0,0739** | **oui** | **oui** |

**Bilan : 8/12 au-dessus du plancher, 10/12 positifs.** Les
seules paires négatives restent GSE62452 (−0,0036) et GSE21501
(−0,0100). **LOO (descriptif) :** retirer n'importe laquelle
des 8 paires passantes laisse 7/11, qui satisfait encore la
barre A2 d'origine (≥ 6/8) — le verdict de suffisance ne tient
plus à une seule paire, et il ne tenait déjà plus à une seule
paire depuis le §8.71 (6/10). **C3 reste LEVÉE** : elle l'était
depuis le §8.71 (7 paires passantes) ; ce chantier ajoute une
huitième paire passante et ne rouvre rien.

Lecture honnête du rang : +0,0739 est le plus petit écart
passant du dossier (devant ICGC +0,0970 et GSE60979 +0,2045) et
le deuxième plus petit écart positif après GSE71729 (+0,0402)
et GSE79668 (+0,0567). La douzième paire ne renforce pas
l'adoption par sa taille d'effet — elle la renforce par son
nombre : 8 paires passantes sur 12, dont 3 confirmations GEO
indépendantes consécutives qui passent ou frôlent le plancher
(GSE79668 +0,0567, GSE60979 +0,2045, GSE131050 +0,0739), et
par la consolidation des nuls frais (§8.74.4).

## 8.74.4 — Les nuls frais : le passage est consolidé, la marge reste étroite

Règle gelée (§7 du protocole) : `d_maxsep = +0,0739` est dans
[−0,07 ; +0,14[, donc 2 nuls frais sont courus (graines 8741 et
8742, gelées avant tout run). Construction identique au nul
graine 42 (permutation des lignes du CSV réel, `rng(seed)`,
contrôle intact) ; CSV
`pdac_874_yeh_ff_fluxes_nul_s8741.csv` (SHA `627bbf22…771c5`) et
`pdac_874_yeh_ff_fluxes_nul_s8742.csv` (SHA `68d95935…483`).

| Nul | maxsep | Écart réel − nul |
|---|---|---|
| Graine 42 (verdict) | 0,2481 | **+0,0739** |
| Graine 8741 | 0,2244 | **+0,0976** |
| Graine 8742 | 0,2106 | **+0,1113** |

**Min +0,0739, médiane +0,0976, max +0,1113 — les trois écarts
sont au-dessus du plancher 0,07 : le passage est dit
« consolidé » par la règle gelée.** Étendue des trois nuls :
0,0374 (0,2481 − 0,2106) — petite devant l'écart médian
(+0,0976) et devant l'étendue mesurée au §8.70 à n comparable
(0,0972 entre 3 nuls à n = 51). Le verdict de la paire graine
42 n'est JAMAIS changé par les nuls frais (règle gelée) : il
est CONFIRME, et les nuls frais le consolident au lieu de le
fragiliser — le nul graine 42 est le PLUS HAUT des trois nuls,
donc le moins favorable au passage, et le passage tient quand
même.

Deux lectures restent vraies en même temps, et toutes deux
sont écrites ici. Lecture consolider : aucun des trois nuls
n'inverse le passage ; le tirage de nul le plus défavorable
donne encore +0,0739. Lecture étroite : la marge du verdict
(+0,0039 sur la paire graine 42) est inférieure à l'étendue
des nuls (0,0374) — un autre tirage de nul aurait pu donner
+0,06 ou +0,11 avec la même facilité, et la médiane des trois
écarts (+0,0976) reste modeste. C'est exactement la situation
que la règle des nuls frais est faite pour décrire : le passage
tient sur trois tirages, pas sur un — et sa marge reste
étroite. Rien de plus n'est affirmé.

## 8.74.5 — Les scores compagnons : `maxsep` passe seul, les autres ne suivent pas

Convention d'affichage §8.64.6 : `maxsep` score principal,
ancien MC secondaire, `sep` compagnon, mention de fragilité en
tête de table (voir le verdict). Les scores compagnons sont
descriptifs : aucun ne décide.

- **Ancien MC (secondaire) :** réel 0,3985 contre nuls 0,3871 /
  0,3835 / 0,3833 — écart +0,0114 contre le nul graine 42,
  +0,0150 / +0,0152 contre les nuls frais. À peine positif, et
  très loin du plancher 0,07 : MC ne sépare pas ici. C'est le
  même motif qu'aux §8.70 (+0,05) et §8.71 (+0,026) : `maxsep`
  voit quelque chose que l'ancien MC ne voit presque pas.
- **Delta :** réel 1,470 contre nuls 1,429 / 1,368 / 1,250 —
  écart +0,041 contre le nul graine 42. Plat, comme aux §8.70
  (+0,05) et §8.71 (−0,015). La divergence Delta/`maxsep` du
  §8.69 (Delta +2,01 contre maxsep −0,01) ne se reproduit pas
  ici : Delta et `maxsep` vont dans le même sens, Delta
  simplement beaucoup plus faible. Delta n'est toujours pas
  élucidé (§8.57, §8.63) ; rien n'est élucidé ici sans preuve.
- **S_sep :** réel 0,3187 contre nuls 0,2445 / 0,2207 / 0,2099 —
  écart +0,0742 contre le nul graine 42. S_sep suit `maxsep`
  (il en est proche par construction, §8.38) et passe le même
  plancher en descriptif.
- **`sep` compagnon :** réel 0,2436 contre nul 0,1988 — écart
  0,0448, contre un plancher équivalent-sep de 0,1155
  (= 0,07·(1+0,3220)(1+0,2481)). **La paire ÉCHOUE à la barre
  descriptive du plancher équivalent-sep**, comme au §8.71
  (0,1146 contre 0,1249 exigé). `sep` ne suit pas `maxsep`
  jusqu'à sa propre barre — cohérent avec le rejet de `sep`
  seul aux §8.59/§8.64. Rapporté, non décisif : D4 n'est pas
  rejoué ici.
- **Cascade :** réelle [45,7 / 68,7 / 76,0 / 80,8 / 90,4] contre
  nul graine 42 [0,0 / 21,3 / 28,4 / 33,2 / 43,1] — la cascade
  réelle est nettement au-dessus à tous les quantiles, Q1 45,7
  contre 0,0. Mais les nuls frais ont des cascades élevées
  aussi ([48,5 / 73,6 / 80,8 / 88,0 / 100,0] et [11,8 / 78,4 /
  83,2 / 90,4 / 100,0]) : la cascade seule ne sépare pas le
  réel des nuls — le nul graine 42 a une cascade basse, les
  nuls frais des cascades hautes. C'est consigné tel quel : la
  cascade n'est pas un critère de passage et ne l'a jamais été.
- **L7a :** up partout (réel 0,335 ; nuls 0,347 / 0,328 / 0,345)
  — L7a ne sépare pas ici, comme dans la plupart des paires
  principales. **L7b :** FRAGILE sur les 4 runs — non
  informatif (audit clos, §8.56/§8.64 : il dit FRAGILE sur le
  réel comme sur les nuls).
- **F1/F2 après seuil :** réel 0,4775 / 0,5248 ; nul s42 1,7075 /
  1,0350 ; s8741 2,1622 / 0,3382 ; s8742 1,3190 / 1,7240.
  Descriptif, sans lecture imposée : les ratios F1/F2 varient
  fortement entre nuls (F1 de 1,32 à 2,16, F2 de 0,34 à 1,72),
  ils ne portent pas le verdict.

## 8.74.6 — Tests directs en appui (ne décident pas)

Script `direct_tests_874.py` (SHA `be58861e…5781b`), sur les
CSV de flux du chantier (réel + nul graine 42). Sortie :
`direct_tests_874.json` (SHA `1d18f6dc…8d71`).

**1. d de Cohen marginal (correction §8.70, appliquée ici).**
d = 0,0000 pour les 12 gènes (CR2 : −0,0000, arrondi) — vacueux
par construction, comme attendu : le nul est une permutation
des lignes, chaque flux garde exactement ses 42 valeurs. Le
test valide la construction du nul (marginales préservées
exactement) ; il ne mesure pas la séparation et ne décide rien.

**2. Test informatif : Spearman de chaque flux contre le pas
(ordre KRAS), réel vs nul.** |ρ| moyen : réel 0,336 contre nul
0,146. Δρ médian **+0,386**. Δρ positifs **10/12**. Table
complète, sans sélection :

| Gène | ρ réel | ρ nul | Δρ |
|---|---|---|---|
| PGC | −0,003 | −0,002 | −0,001 |
| REG4 | −0,040 | +0,059 | −0,099 |
| CLDN18 | +0,670 | −0,370 | **+1,041** |
| MUC17 | +0,415 | −0,108 | +0,523 |
| DPCR1 | +0,535 | −0,282 | +0,817 |
| CR2 | +0,296 | −0,046 | +0,342 |
| KRT20 | +0,217 | −0,152 | +0,369 |
| MUC2 | +0,143 | +0,017 | +0,126 |
| GSTM1 | +0,400 | −0,002 | +0,402 |
| CEACAM5 | +0,629 | −0,315 | +0,944 |
| CLCA1 | +0,217 | −0,049 | +0,266 |
| MUC16 | +0,468 | −0,352 | +0,821 |

Lecture : l'ordre par KRAS porte une information réelle et
forte — 10 flux sur 12 montent avec KRAS (CLDN18, CEACAM5,
DPCR1, MUC16 en tête, Δρ de +0,82 à +1,04), deux ne montent
pas (PGC −0,001, REG4 −0,099). C'est le test qui porte
l'information d'ordre, et il est cohérent avec le `maxsep`
qui passe : le réel est ordonné, le nul ne l'est pas. Aucun
de ces tests ne change le verdict du §7 — ils l'éclairent.
Comparaison descriptive avec les §8.70/§8.71 (valeurs relues dans
`direct_tests_870.json` / `direct_tests_871.json`, jamais
recalculées) : au §8.70, Δρ médian +0,186, 9/12 positifs, |ρ|
moyen réel 0,245 contre nul 0,075 ; au §8.71, Δρ médian +0,180,
8/12 positifs, |ρ| moyen réel 0,228 contre nul 0,097. Ici le
signal d'ordre est PLUS FORT sur les trois mesures (Δρ médian
+0,386, 10/12 positifs, |ρ| 0,336 contre 0,146) — cohérent
avec un `maxsep` qui passe ici (+0,0739) alors qu'il était
PARTIEL au §8.70 (+0,0567) ; au §8.71 il passait plus largement
(+0,2045) avec un Δρ médian pourtant plus faible (+0,180) — les
deux mesures ne sont pas proportionnelles, et aucune loi n'est
inférée de trois points.

## 8.74.7 — La structure appariée Yeh et le lot Linehan : ce qui a été écarté, et pourquoi

**Le lot Yeh_seq est un lot APPARIÉ — c'est la découverte
méthodologique du chantier, et elle a décidé de la
construction.** Les 125 échantillons Yeh ne sont pas 125
tumeurs : les 97 échantillons primaires proviennent de 43
tumeurs indépendantes seulement (codes `MMDDT#`), chaque
tumeur étant échantillonnée jusqu'à trois fois (FF, FNA, FFPE)
— 41 codes ont à la fois un FF et un FNA. L'article le décrit :
FNA ex-vivo au moment de la résection (3 passages, aiguille
22G), FFPE relus par un pathologiste. Prendre les 97 colonnes
comme 97 tumeurs aurait compté 54 fois la même tumeur — la
paire aurait été invalide par construction. La construction
gelée (§4.2/§4.4) prend donc UNE ligne par tumeur : FF
primaire, médiane des réplicats pour les 4 codes à réplicats
FF (0417T1 ×3, 0523T1 ×2, 0806T1 ×2, 1119T1 ×2), n = 42. Le
code 0921T1 (FNA seul, sans FF) n'entre pas dans le lot FF.
Les 28 PDX sont exclus : ce ne sont pas des tumeurs primaires.
Les 45 FNA et 5 FFPE primaires ne sont pas mélangés au lot FF :
autres types d'échantillons, autre kit (TruSeq RNA Exome
contre TruSeq pour les FF).

**Le lot Linehan_seq est écarté comme paire principale, pour
une raison structurelle écrite d'avance (protocole §2.3).**
66 biopsies pour 37 patients seulement (29 × 2, 8 × 1) ;
l'article confirme le mélange pré/post-traitement (« The
Linehan Phase 1b trial captured both pre- and post-treatment
biopsies », fig. 2C : transitions de sous-types, Kappa de
Cohen 1,0 pour le schéma Moffitt) ; les métadonnées GEO ne
labellisent pas pré/post (seulement `sample type: tumor
biopsies`, `tissue: pancreatic ductal adenocarcinoma`) — le
partage n'est pas extractible sans la table supplémentaire 2
de l'article. Le plus grand sous-ensemble homogène de tumeurs
indépendantes pré-traitement est d'au plus 37 < 40 : la porte
n ≥ 40 échoue. Aucun CSV, aucun run pour ce lot. Le fichier
`GSE131050_PurIST_Linehan_seq.tsv.gz` est téléchargé et
conservé dans `data/` (SHA `729bb794…efc16`) mais aucun flux
ni run n'en est issu dans ce chantier.

**Ce que cela change pour la suite.** La série GSE131050 ne
contient plus de paire principale évidente non testée : le lot
Yeh FNA (un FNA par tumeur, n = 42 codes) est la seule piste
suivante nommée (§8.74.9) — un lot FNA, échantillons faible
volume, qui testerait la même cohorte par un autre type
d'échantillon, pas une cohorte nouvelle. Toute autre paire
GSE131050 serait un re-test déguisé (mêmes 43 tumeurs).

## 8.74.8 — Ce que le verdict dit, et ce qu'il ne dit pas

Il dit que la douzième paire principale passe le plancher gelé,
de justesse, et que le passage tient sur trois tirages de nul.
Il dit que l'ordre KRAS porte une information réelle sur ces
42 tumeurs (Δρ médian +0,386, 10/12 positifs) — c'est le
signal que `maxsep` lit. Il dit que le dossier compte
désormais 8 paires passantes sur 12, et que le verdict de
suffisance ne tient à aucune paire seule (LOO 7/11).

Il ne dit pas que `maxsep` sépare toujours le réel du nul :
4 paires sur 12 restent non passantes, et les scores compagnons
(MC +0,0114, Delta +0,041) ne suivent presque pas. Il ne dit
pas que la marge est confortable : +0,0039 sur la paire graine
42, c'est la plus petite marge passante du dossier. Il ne dit
pas que l'adoption pleine est prouvée : elle a été décidée par
Zackary le 20 nov. 2026 à 13h04, et ce chantier est la
vérification a posteriori que le protocole prévoyait. Il ne dit
rien de clinique : l'étude porte sur l'instrument, pas sur un
remède — aucune affirmation sur le cancer du pancréas n'est
tirée de cette paire.

**Biais et limites nommés.** (a) n = 42 : petit effectif, proche
du plancher n ≥ 40 ; la fragilité du nul à petit n (§8.70 :
étendue 0,0972 à n = 51 ; §8.53 : ~200 nuls pour un plancher
stable à petit n) reste un chantier ouvert — ici l'étendue
mesurée (0,0374 sur 3 nuls) est petite, mais 3 nuls ne font
pas un plancher stable. (b) Médiane des réplicats FF : pour
4 tumeurs sur 42, la valeur retenue est une médiane de 2–3
mesures, pas une mesure unique — règle gelée avant tout run,
précédent du projet, mais c'est une agrégation, pas une
mesure brute. (c) Nature FPKM vs TPM indéterminée
(PROVENANCE_874 §3) — valeurs prises telles que fournies,
sans transformation ; le pipeline ne voit que l'ordre
relatif, mais la nature exacte reste inconnue. (d) Recouvrement
avec TCGA_PAAD non excluable formellement par identifiants
(titres anonymisés) — voir §8.74.1.3. (e) Une seule plateforme
(NextSeq 500), un seul centre (UNC), un seul type
d'échantillon (FF) : la paire ne teste pas la robustesse
inter-plateformes — c'est le rôle des autres paires, pas de
celle-ci.

## 8.74.9 — Pistes ouvertes

| Pistes ouvertes | Oui, une de moins | (a) La confirmation indépendante C3 est close depuis le §8.71 — aucune autre paire indépendante n'est requise par ce critère ; GSE131050 ajoute une huitième paire passante et ne rouvre rien ; (b) la fragilité du nul à petit n (§8.70, §8.53) reste un chantier propre ouvert — ici 3 nuls, étendue 0,0374, médiane des écarts +0,0976 ; (c) la divergence Delta/`maxsep` du §8.69 ne se reproduit pas sur cette cohorte non plus (Delta +0,041, même sens, beaucoup plus faible) ; (d) piste suivante nommée, non vérifiée : le lot Yeh_seq FNA (un FNA par tumeur, n = 42 codes) — même cohorte, autre type d'échantillon, pas une cohorte nouvelle ; (e) le lot Linehan_seq reste inutilisable comme paire principale (37 patients, pré/post mélangées). |

## 8.74.10 — Annexe : provenance condensée et SHAs

- **Source :** GSE131050, NCBI GEO ; Rashid et coll., *Clin
  Cancer Res* 2020, 26(1):82–92, PMID 31754050,
  doi 10.1158/1078-0432.CCR-19-1467 ; UNC Lineberger, Chapel
  Hill, USA. Série soumise 10 mai 2019, publique 10 déc. 2019.
  Plateformes : GPL16791 Illumina HiSeq 2500 (Linehan),
  GPL18573 Illumina NextSeq 500 (Yeh). BioProject PRJNA542388,
  SRA SRP197641. Provenance complète : `PROVENANCE_874.md`.
- **Fichiers officiels (`data/`) :** Yeh_seq
  `2fc0a66e…be5b1` (9 468 179 o) ; Linehan_seq
  `729bb794…efc16` (5 157 464 o) ; matrice GPL18573
  `9b333eb6…7843e` (6 864 o) ; matrice GPL16791
  `03aa8ca6…1df94` (4 859 o). SHA identiques aux copies
  d'enquête pré-gel.
- **Protocole :** `PROTOCOL_maxsep_gse131050_874.md`, SHA
  `3f34f4ff…1d5f` (gelé avant tout téléchargement officiel).
- **Pipeline :** v6.2 SHA `f07567c4…c3abf`, vérifié avant et
  après le lot, inchangé. (Note : 8 occurrences de
  `temperature|Onsager|2.269` dans le fichier, toutes dans
  l'annexe génératrice d'exemple Ising, hors cœur — état connu
  du fichier adopté.)
- **CSV de flux :** réel `db258c99…58fe44` (42 lignes) ; nul s42
  `e9468376…2305b` ; nul s8741 `627bbf22…771c5` ; nul s8742
  `68d95935…483`.
- **Extraction / vérification :** `extract_874.json`
  `82ade747…fcb47` ; `extract_874.csv` `163de3bf…73fe` ;
  `direct_tests_874.json` `1d18f6dc…8d71` ;
  `maxsep_874_verify.json` `1c29544c…e55e6f` (4/4 à 0,0 exact).
- **Scripts :** `build_fluxes_874.py` `02910920…846c13` ;
  `build_nul_874.py` `4b949d3b…7faa` ;
  `extract_874.py` `395909c3…8b8f` ;
  `verify_874.py` `ac7fac6d…dc13` ;
  `direct_tests_874.py` `be58861e…5781b`.
- **Manifestes / journaux :** `manifest_v62_874.txt`
  `d130c20b…29f` ; `manifest_v62_874_frais.txt` `4df63561…9094` ;
  `runs_v62_874.log` `7a15d398…63` ;
  `runs_v62_874_frais.log` `e45027c6…716`.
- **Recoupements (reprises telles quelles, jamais
  recalculées) :** `sep_maxsep_856_table.json`
  `ec5ee638…34f8b` ; `extract_869.json` `644339e4…882b` ;
  `extract_870.json` `4ffa851a…444f` ; `extract_871.json`
  `85e9089a…55e3b`.
- **KRAS (ordre, valeurs fournies) :** min 1,152, médiane 6,955,
  max 19,7 (après médiane des réplicats FF).
- **Livre blanc NON édité. PDF NON régénéré. Rien poussé sur
  GitHub** (convention des chantiers ; fusion par le
  coordinateur).

— Fin de la section §8.74. —
