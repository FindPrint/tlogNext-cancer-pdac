# §8.72 — Consolidation de §8.70 : 10 nuls frais sur GSE79668 — RENVERSE

## Verdict d'abord

**RENVERSE — contre la distribution des 13 nuls, la paire
GSE79668 PASSE le plancher : `d_médian = +0,1447` (réel 0,4104
contre nul médian 0,2657), plus de deux fois le plancher 0,07.
Le réel bat les 13 nuls sur 13 (rang 14/14) et 12 écarts sur 13
dépassent le plancher. La lecture « sous le plancher » du §8.70
(+0,0567 contre le nul graine 42) était un artefact du tirage :
le nul graine 42 est le PLUS HAUT des 13 nuls mesurés (0,3538),
à 0,0881 au-dessus du nul médian. Le verdict de la paire
graine 42 reste PARTIEL — règle gelée §8.70 §7, l'histoire
n'est pas réécrite — mais sa lecture est renversée, et une
note datée de correction est ajoutée en addendum au §8.70.**

| Porte (PROTOCOL_nulls_gse79668_872.md §4.3, gelé) | Exigé | Mesuré 20 nov. 2026 | Sort |
|---|---|---|---|
| `d_médian` (réel − médiane des 13 nuls) | < 0,05 CONSOLIDÉ ; 0,05–0,09 INCONCLUSIF ; > 0,09 RENVERSE | **+0,1447** | **RENVERSE** |
| Médiane 10 frais vs médiane 13 nuls | écart ≤ 0,03 | **−0,0002** | **cohérent** |
| Exactitude de l'extraction | 14/14 à 0,0 exact | **14/14, écart max 0,0** | **PASSE** |
| Relecture des valeurs §8.70 | 4/4 à 0,0 exact | **4/4, écart 0,0** | **PASSE** |
| Exits des 10 runs | 10 × 0 | **10 × 0, 0 échec** | **PASSE** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que
la paire GSE79668, jugée non contre un tirage unique mais
contre la distribution de son nul, sépare le réel du nul en
`maxsep` au-dessus du plancher gelé — et largement : +0,1447
contre 0,07 exigé, avec une marge de 0,0547 au-dessus du seuil
de renversement (0,09). Il dit aussi que le §8.70 avait
raison de se dire fragile : son verdict tenait au tirage le
plus défavorable possible — le nul graine 42, le plus haut des
13. Il ne dit pas que le verdict §8.70 est effacé : la paire
graine 42 reste PARTIELLE par règle gelée, et l'A2 étendu gelé
(6/10, paires graine 42) n'est PAS recompté ici — le
renversement est une correction de lecture, pas un recomptage.
Il ne dit pas non plus que C3 est levée au sens gelé : C3
exige 7 paires passantes comptées en paires graine 42, et ce
chantier ne recompte rien (§8.72.2). Il dit, en substance, que
la dixième paire indépendante passe contre son nul typique —
et que la décision de lever C3 sur cette base appartient à
Zackary et au coordinateur, pas à ce chantier. L'adoption
pleine de `maxsep`, décidée par Zackary le 20 nov. 13h04,
n'est ni rouverte ni conditionnée ici : ce chantier est une
vérification a posteriori, comme le §8.70.

**Le fait nouveau, dit en tête.** Sur 3 nuls, le §8.70 voyait
une étendue de 0,0972 — plus grande que l'écart mesuré
(0,0567) — et concluait « un seul nul ne suffit pas à
trancher ». Sur 13 nuls, la distribution est désormais
décrite : médiane 0,2657, p95 0,3344, étendue 0,1110. Le réel
(0,4104) est au-dessus du p95 des nuls — et même au-dessus du
p95 de plus que le plancher (`d` contre p95 = +0,0760). Le
seul écart sous le plancher, parmi les 13, est celui contre
le nul graine 42 (+0,0567). Les 12 autres vont de +0,0890 à
+0,1676. Ce n'est plus un quasi-passage : c'est un passage
contre le nul typique, confirmé par 12 tirages sur 13.

Protocole gelé : `PROTOCOL_nulls_gse79668_872.md` (20 nov.
2026, SHA `95acdd45…cf41` au gel, inchangé). Critère de
verdict écrit AVANT toute construction et tout run (§4.3 du
protocole) ; aucune repondération, aucun nouveau terme, aucune
redéfinition du plancher après avoir vu les chiffres. Les
nombres du §8.70 étaient la motivation, pas le verdict : le
verdict repose sur les 10 runs neufs mesurés ci-dessous, joints
aux 3 nuls anciens relus à 0,0 exact.

## 8.72.1 — La distribution des 13 nuls : le réel bat tout le monde

**Les 13 nuls, triés par `maxsep` croissant** (réel 0,4104 en
tête de liste, hors distribution) :

| Rang | Nul | `maxsep` nul | `d_maxsep` (réel − nul) | > 0,07 ? |
|---|---|---|---|---|
| 1 (min) | s8725 | 0,2428 | **+0,1676** | oui |
| 2 | s8730 | 0,2508 | **+0,1596** | oui |
| 3 | s8702 | 0,2566 | **+0,1538** | oui |
| 4 | s8723 | 0,2601 | **+0,1504** | oui |
| 5 | s8728 | 0,2614 | **+0,1490** | oui |
| 6 | s8726 | 0,2653 | **+0,1452** | oui |
| 7 (médiane) | **s8721** | **0,2657** | **+0,1447** | **oui** |
| 8 | s8727 | 0,2747 | **+0,1357** | oui |
| 9 | s8729 | 0,3074 | **+0,1031** | oui |
| 10 | s8724 | 0,3160 | **+0,0944** | oui |
| 11 | s8722 | 0,3211 | **+0,0894** | oui |
| 12 | s8701 | 0,3215 | **+0,0890** | oui |
| 13 (max) | **graine 42** | **0,3538** | **+0,0567** | **non** |

Valeurs exactes : réel `maxsep` 0,41044843843771645 ; médiane
des 13 nuls 0,2657078111639579 (le nul s8721) ; `d_médian` =
+0,14474062727375853. Écarts triés : +0,0567 / +0,0890 /
+0,0894 / +0,0944 / +0,1031 / +0,1357 / +0,1447 / +0,1452 /
+0,1490 / +0,1504 / +0,1538 / +0,1596 / +0,1676.

**Statistiques des distributions** (`numpy.percentile`,
interpolation linéaire — méthode gelée §4.1) :

| Statistique | 13 nuls (primaire) | 10 frais seuls (contrôle) |
|---|---|---|
| Médiane | **0,2657** | 0,2655 |
| p95 | **0,3344** | 0,3188 |
| Min / max | 0,2428 / 0,3538 | 0,2428 / 0,3211 |
| Étendue | **0,1110** | 0,0782 |
| Q1 / Q3 | 0,2601 / 0,3160 | 0,2604 / 0,2992 |
| IQR | 0,0560 | 0,0388 |
| Écart-type | 0,0349 | 0,0280 |

Valeurs exactes (13 nuls) : p95 0,33440202574442535 ; étendue
0,11095254467578725 ; IQR 0,055960582020429195 ; écart-type
0,03490438297729817. (10 frais) : médiane
0,2654792677948886 ; p95 0,3188097055470229 ; étendue
0,0782478240669992 ; IQR 0,03879953079455112 ; écart-type
0,02796398531378161.

**Lecture.** La médiane des 10 frais (0,2655) diffère de la
médiane totale (0,2657) de −0,0002 — très loin du seuil
d'alerte gelé (0,03) : les 3 anciens nuls ne tirent pas la
distribution. L'écart contre la médiane des 10 frais seuls
est +0,1450 — identique à `d_médian` (+0,1447) à 0,0003 près :
le verdict ne dépend pas de l'inclusion des 3 anciens nuls. Le nul graine 42 (0,3538) est le maximum des
13 — il dépasse le deuxième plus haut (s8701, 0,3215) de
0,0323 et le p95 (0,3344) : c'est un tirage de queue, pas un
nul typique. Le nul médian (s8721, 0,2657) donne un écart de
+0,1447 — le verdict ne tient donc plus à un tirage : 12
tirages sur 13 passent le plancher, et le réel est au-dessus
du p95 des nuls de +0,0760, soit plus que le plancher lui-même.
À l'inverse du §8.70, où l'étendue des nuls (0,0972)
dépassait l'écart mesuré (0,0567), l'écart médian (+0,1447)
dépasse désormais l'étendue des 10 frais (0,0782) et
l'étendue totale (0,1110) : le signal est plus grand que la
dispersion du nul. Le rang du réel est 14/14 : aucun nul ne
le bat.

**Lot.** Pipeline `universal_v6.2.0_cohen.py`, SHA
`f07567c4…c3abf`, revérifié inchangé avant ET après le lot ;
mode fast ; 10 runs, exits 0/0/0/0/0/0/0/0/0/0, 0 échec,
0 déjà fait. Lancement en `systemd-run` (unité `v62-872`),
surveillance `watch_v62_872.sh` (arrêtée d'elle-même à 10/10,
`WATCH 872 TERMINE 10/10`, tour 3) ; journal
`runs_v62_872.log` (SHA du pipeline en tête, FIN
21h07:33Z, déjà faits 0, terminés 10, échecs 0). Durée du lot :
20h39:33Z → 21h07:33Z (~28 min). Aucun redémarrage de machine
pendant le lot, aucune relance, aucun dossier supprimé. Le
livre blanc n'est PAS édité, le PDF N'EST PAS régénéré, rien
n'est poussé sur GitHub dans ce chantier.

## 8.72.2 — Ce que le renversement dit, et ce qu'il ne dit pas

**Ce qui est renversé.** La lecture du §8.70, pas son verdict.
Le §8.70 disait, sur la paire graine 42 : PARTIEL, +0,0567,
sous le plancher — et il disait aussi que ce verdict était
fragile, parce que les 2 nuls frais passaient. La présente
section confirme la fragilité dans le sens exact où le §8.70
la craignait : le verdict tenait au tirage, et le tirage
gelé était le pire des 13. Contre le nul typique, la paire
passe — et elle passe largement (+0,1447, soit 2,07 fois le
plancher). La note datée de correction ajoutée en addendum au
fichier `section_8.70_gse79668.md` dit exactement cela, sans
toucher au texte original.

**Ce qui n'est pas renversé.** Le verdict de la paire graine
42 reste PARTIEL : la règle gelée §8.70 §7 l'interdit de
changer, et ce chantier la respecte — l'histoire n'est pas
réécrite, elle est complétée. L'A2 étendu gelé reste 6/10
(8/10 positifs) : les 9 paires comptées gardent leurs valeurs,
et la dixième garde sa valeur de paire graine 42 (+0,0567).
Le protocole §4.3 l'a gelé ainsi : le renversement est une
correction de lecture, pas un recomptage.

**C3, dite plainement.** Au sens gelé — 7 paires passantes
comptées en paires graine 42 — C3 n'est PAS levée par ce
chantier : il faudrait 7/10, il y en a 6/10, et ce chantier
ne recompte rien. En substance, en revanche, la dixième paire
indépendante passe contre son nul typique (+0,1447) : c'est
ce que C3 attendait d'une confirmation indépendante, mesuré
sur 13 tirages et non sur un seul. Les deux faits coexistent
et sont dits tels quels : C3 gelée ouverte, confirmation de
substance mesurée. Trancher entre les deux lectures — lever
C3 sur la base de la distribution, ou exiger une onzième
paire en paire graine 42 — est une décision de Zackary et du
coordinateur, pas de ce chantier. Ce chantier mesure ; il ne
recompte pas et ne lève pas de condition.

**Ce que le renversement ne prouve pas.** Il ne prouve pas
que `maxsep` sépare « en général » : c'est une paire, à
n = 51, sur une distribution de 13 nuls — pas un plancher
stable (le §8.53 estime ~200 nuls pour un plancher stable à
petit n). Il ne prouve pas que le nul graine 42 était un
« mauvais » tirage au sens d'une erreur : c'est un tirage
légitime de la même distribution, simplement un tirage de
queue (au-dessus du p95). Il ne change rien à l'adoption
pleine : elle a été décidée par Zackary le 20 nov. 13h04, et
ce chantier la consolide par son honnêteté, comme le §8.70
l'avait fait par la sienne.

## 8.72.3 — Contrôles descriptifs (à publier, ne décident pas)

**Ancien MC : positif contre le nul médian, pas contre tous
les nuls.** Réel 0,3566 ; nuls médiane 0,3388, min 0,3326,
max 0,3790 ; `d_MC` contre le nul médian +0,0178. Un nul
frais (s8722, MC 0,3790) bat le réel en MC — comme au §8.70,
où le MC était inversé (−0,0053) contre graine 42. Le MC ne
porte pas la séparation ici : c'est `maxsep` qui la porte,
et le critère gelé est `maxsep` seul.

**S_sep : même histoire que `maxsep`.** Réel 0,4022 ; nuls
médiane 0,2638 ; `d_Ssep` contre le nul médian +0,1384 —
du même ordre que `d_médian` (+0,1447), comme au §8.70 où
S_sep (+0,0675) suivait `maxsep` (+0,0567).

**Delta : plat, comme au §8.70.** Réel 0,6353 ; nuls médiane
0,6010, min 0,5839, max 0,6387 — un nul frais (s8728, 0,6387)
dépasse le réel. Delta ne diverge pas ici et ne porte rien :
la divergence Delta/`maxsep` du §8.69 ne se reproduit ni au
§8.70 ni ici.

**L7a : UP presque partout.** Réel UP 0,3459. Sur les 13
nuls : 10 UP, 3 DOWN (s8723 0,1757 ; s8724 0,1944 ; s8729
0,1745 — confiances faibles, ~0,17–0,19, contre ~0,33–0,36
pour les UP). Descriptif : L7a n'est pas le critère gelé, et
il ne distingue pas les séries ici — les 3 DOWN sont des
nuls, mais 10 nuls sont UP comme le réel.

**L7b : FRAGILE sur les 14 runs** — même non-informativité
que partout (réel + 13 nuls). **Falsification :
indisponible** (n = 51 < 75, règle du projet) — valeurs
brutes rapportées à titre descriptif seulement, sans statut
de test : réel 1,40578, nuls 1,16613–1,49965, tous au-dessus
du seuil 0,5 du JSON.

**Cascades : formes instables, comme au §8.70.** Réel
[3,9 / 72,4 / 76,3 / 82,2 / 100,0] (pas 2/36/38/41/50).
Nuls frais à T_+2 : de 27,1 % (s8727) à 100,0 % (s8723,
s8729) — la forme de la cascade nulle n'est pas une
caractéristique stable à n = 51 : elle mesure le tirage,
elle ne distingue pas les séries. Aucune rupture visible
qui distinguerait le réel des 13 nuls à la fois — la
séparation est dans le score `maxsep`, pas dans la forme
de la cascade.

## 8.72.4 — Ce que ça change, et ce que ça ne change pas

| Poste | Change ? | Détail |
|---|---|---|
| Lecture du §8.70 (« sous le plancher ») | **Oui — RENVERSE** | Contre le nul médian, la paire passe (+0,1447). Note datée de correction en addendum au §8.70, texte original intact. |
| Verdict de la paire graine 42 (§8.70) | **Non — reste PARTIEL** | Règle gelée §8.70 §7. L'histoire n'est pas réécrite. |
| A2 étendu gelé (paires graine 42) | **Non — reste 6/10, 8/10 positifs** | Pas de recomptage (protocole §4.3). |
| Condition C3 (§8.59.8, sens gelé) | **Non levée par ce chantier** | 7 paires passantes exigées en paires graine 42 ; la décision de lever C3 sur la base de la distribution appartient à Zackary et au coordinateur (§8.72.2). |
| Adoption pleine de `maxsep` | **Non — décidée par Zackary le 20 nov. 13h04** | Ce chantier est une vérification a posteriori, pas une condition. |
| Score MC affiché (convention §8.64.6) | Non | `maxsep` principal, ancien MC secondaire, `sep` compagnon, mention de fragilité — inchangée. |
| Sélection du best_config, seuil MC, cascade, S_sep, Delta, L7a | Non | Inchangés par construction. |
| Code v6.2 / v6.1 / v6 | Non | Aucune modification, aucune v6.5. |
| Verdicts des §8.56, §8.59, §8.64, §8.69, §8.70 | Non | Confirmés, pas rouverts ; les 9 paires comptées et la dixième en paire graine 42 gardent leurs valeurs. |
| Pistes ouvertes | Oui, une de plus | (a) La question « combien de nuls faut-il pour un plancher stable à n ≈ 50 ? » (§8.70.6, §8.53) reste ouverte : 13 nuls décrivent la distribution, ils ne stabilisent pas un plancher — ~200 nuls seraient nécessaires ; (b) la divergence Delta/`maxsep` du §8.69 ne se reproduit ni au §8.70 ni ici — elle reste une piste ouverte, pas une loi ; (c) si Zackary veut lever C3, la voie est soit une décision sur la base de la distribution mesurée ici, soit une onzième paire indépendante avec son propre protocole gelé. |

**Suite du dossier.** Si Zackary veut une nouvelle paire
indépendante : un chantier ultérieur, avec son propre
protocole gelé, sur une autre cohorte vérifiée indépendante —
pas une relecture, pas un re-test déguisé, et pas GSE79668
(mesurée, consolidée par distribution). Si Zackary décide de
lever C3 sur la base de la distribution : la présente section
fournit les chiffres, et la levée est consignée par le
coordinateur avec sa date et sa décision — pas par ce
chantier. Dans les deux cas, le PDF et GitHub sont régénérés
et poussés par le coordinateur (règle permanente « Toujours
github et pdf !!! »), avec la présente section fusionnée.

## 8.72.5 — Limites et ce qui reste

- 13 nuls ne font pas un plancher stable : §8.53 estime ~200
  nuls pour un plancher stable à petit n. La médiane de 13
  nuls porte ~±0,02 — d'où la bande d'inconclusivité gelée
  (±0,02 autour du plancher). Ici `d_médian` (+0,1447) est
  loin au-dessus de la bande (0,09) : le verdict RENVERSE ne
  tient pas à la bande. Mais la queue de la distribution
  (p95) reste estimée sur 13 tirages seulement.
- Le nul est une permutation par lignes (corrélations
  inter-flux préservées) : la distribution mesurée est celle
  du nul du projet, pas d'un nul à corrélations brisées
  (même réserve qu'au §8.53 §8).
- Le nul graine 42 est un tirage légitime, pas une erreur :
  il est au-dessus du p95, mais il appartient à la
  distribution. Le renversement dit que le verdict §8.70
  tenait à ce tirage — il ne dit pas que ce tirage était
  invalide.
- Une seule paire nouvelle a été consolidée : le verdict
  porte sur elle, pas sur « `maxsep` en général ».
- La paire est construite sur des comptages bruts RNA-seq
  (§8.70.4) : la nature des valeurs est nommée comme limite,
  pas corrigée après coup — comme au §8.70.
- Delta ne diverge pas ici (+0,03 contre le nul médian) :
  la divergence du §8.69 (+2,01 contre −0,01) n'est ni
  confirmée ni infirmée comme phénomène — une seule paire
  de plus, dans l'autre sens. L7b est FRAGILE sur les 14 runs
  — non-informatif, comme partout.
- Rien de clinique : l'étude porte sur l'instrument.

## 8.72.6 — Provenance

- Protocole gelé : `PROTOCOL_nulls_gse79668_872.md`, SHA-256
  `95acdd453a2c65e40e4a497231cd189906b0d7bc2d8e242a084e85dbd52bcf41`
  (au gel, avant construction et runs ; fichier inchangé
  depuis).
- Provenance de la cohorte et des données : `PROVENANCE_870.md`,
  SHA-256
  `5e5d26a71d9b1eef7cccfd822496c10ea623b361b517fb31cbaeb6e93b21aad0`
  (GSE79668, Kirby et coll. Mol Oncol 2016, GPL11154, 51
  tumeurs ; matrice SHA `b2226fd0…88e4754`, comptages SHA
  `721cd3a0…54f8` — relus, rien re-téléchargé).
- Construction : `build_fluxes_870.py` (original intact,
  SHA noté au §8.70.8) invoqué par `build_nulls_872.py`,
  SHA-256
  `1ae03f50d56f3591874e4a86b1cd8627cb38ab5e8c8a9dda0d91f6f08450330f`
  (graines gelées 8721–8730 ; CSV réel re-vérifié inchangé
  après chaque invocation).
- Flux : `pdac_870_geo79668_fluxes.csv` (51 lignes), SHA-256
  `7744bc5a82fe80055b5ab9231fc7ae5395354f643b5b7cd1fdfce8aa6656107a`
  (inchangé) ; nuls frais
  `pdac_870_geo79668_fluxes_nul_s8721.csv` …
  `pdac_870_geo79668_fluxes_nul_s8730.csv`, SHA consignés dans
  `nulls_872_files.json`, SHA-256
  `15731361ebdcb0d821c6f8a1a31542cb54c6f2d7cb91cf82220d1ae481600ef8`
  (s8721 `3a2017ec…`, s8722 `19c0aaac…`, s8723 `392974d0…`,
  s8724 `14dac08d…`, s8725 `d246216f…`, s8726 `194130d9…`,
  s8727 `3254083e…`, s8728 `09203dd1…`, s8729 `6fd1f1b3…`,
  s8730 `a8aa618c…`).
- Runs : manifeste `manifest_v62_872.txt`, SHA-256
  `2011af26a0c801047a0d93c3d09ee7cc61757949dd95dc37685c8d0ef4861be7` ;
  journal `runs_v62_872.log`, SHA-256
  `2a2455996fb8114ef7b58aeeb811e250fb93e25291059550c909ec8ab71b6c35` ;
  surveillance `watch_v62_872.sh`, SHA-256
  `8b872b75e3936d3e2a07581dc89635fcb9daff0f2a8d1e39a19418eb4ec18def` ;
  dossiers `results_fast_v62_872_geo79668_nul_s8721` … `s8730`
  (10 runs, exits 0 × 10, 35 fichiers chacun — sans
  `csd_consensus.png`, comme au §8.70).
- Extraction : `extract_872.py`, SHA-256
  `92c68a1c40a3f52222d9d4f1eca0411aaf4dd55a9717f416dae64412b8900a8c`
  → `extract_872.json`, SHA-256
  `2df41832608bd0bc5770fb6b981a2fe5a1c7aa14ba4e89fd7a555ae118deca43` /
  `extract_872.csv`, SHA-256
  `db3564264d9bfac1ae691dcfd5c87bb795ec24693335c60b9cc56cdffaaaa736` /
  `dist_872.json`, SHA-256
  `fa5193eb47d507e180f981f821682fb6dbebe481aec8f557077401bb02ad5619`.
- Vérification indépendante : `verify_872.py`, SHA-256
  `3b9be9d49ca54813647e55af7eaefe17d0e7b0089bd8801ee14339da2c60f921`
  → `maxsep_872_verify.json`, SHA-256
  `a9380adfe83f0636b48403a84dc1e266386bd5fa252065997304042357005f48`
  (14/14 comparaisons, écart max 0,0 exact, verdict OK).
- Valeurs §8.70 relues : `extract_870.json`, SHA-256
  `4ffa851a83668b2369097703862e0413ff9af54af3a66ef70aea9333b40c444f`
  (réel 0,41044843843771645 ; nuls 0,3537953187066359 /
  0,3214731637696184 / 0,2566001863019332 — relecture à 0,0
  exact dans `extract_872.py`).
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`, revérifié
  avant ET après le lot), v6.1 (`2af5e5ce…c1c9`), v6
  (`bb8bbdba…c0773`). Aucune nouvelle version construite dans
  ce chantier — pas de v6.5. Dix runs du pipeline lancés dans
  ce chantier (10 nuls frais, exits 0 × 10) ; aucun run réel
  relancé ; aucun push GitHub, aucune Release dans ce chantier.
- Section : `section_8.72_nulls_gse79668.md` (ce fichier ;
  SHA noté au rapport).
- Données : série réelle = comptages bruts RNA-seq (mesures
  instrumentales transformées : comptages par les déposants,
  symboles extraits mécaniquement, agrégation des doublons par
  médiane, ordre par KRAS). Nuls = lignes permutées, graines
  42 / 8701 / 8702 / 8721–8730 — échantillons hypothétiques,
  pas des mesures. Aucune valeur inventée ; aucune valeur
  recopiée à la main (tables générées depuis
  `extract_872.json` et `dist_872.json`, vérifiées à 0,0 exact
  par `verify_872.py`).
