# Volet 1 — Audit §8.90 : la phrase du podcast (« mieux que juste les tests nuls », « quelque chose à voir avec MC »)

**Audit de lecture seule — aucun run de pipeline lancé, livre blanc et fichiers de résultats non modifiés.**
Livre blanc lu : `~/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md`,
22 783 lignes, SHA-256 `39d3abd65eda029efb959934ecdf17a10f14ba85b0b15f9c03c9e86fc8358696` (mesuré avant rédaction).
Pipeline v6.2 SHA `f07567c4…ec3abf` (revérifié dans le code, voir §6).
Date d'audit : 21 novembre 2026. État du dossier au moment de la lecture : §8.1–§8.89 fusionnés ;
A2 étendu (paires principales, maxsep, plancher 0,07) = **10/15** après §8.88 (12/15 positifs, LOO 9/14) ;
14e paire (§8.85) CONFIRME fragile, 15e paire (§8.88) NON.

**En tête — les trois corrections de Zackary (21 nov. 2026), intégrées ici :**
1. **11h00 — MC n'est JAMAIS seul.** MC sort toujours avec toute la batterie (29 estimateurs, F1/F2, test de bruit,
   L7a/L7b, falsification, Delta, maxsep) ; aucun verdict ne repose sur MC seul, ni sur maxsep seul. Voir §4.
2. **11h01 — « MC, c'est du pur bruit ».** Tranché avec les chiffres en deux parties : comme discriminateur réel/nul
   sur le cancer, MC ne sépare pas (c'est mesuré) ; comme nombre, MC n'est pas aléatoire sans structure
   (terme de robustesse, pic étroit). Voir §5.
3. **11h03 — Le pipeline utilise LES DEUX.** MC et maxsep sont calculés ensemble dans le même run (code v6.2 vérifié,
   lignes 3333 et 10095) ; l'adoption de maxsep n'a changé que l'ordre d'affichage, pas le calcul. Voir §6.

**Méthode.** Pour chaque candidat : chiffres cités tels qu'écrits dans le livre blanc (section + ligne approximative),
puis re-vérification du chiffre principal contre le fichier de résultats cité par la section
(`~/workspace/runs/pdac-v6/`, extracteurs et JSON). « Vérifié » ci-dessous veut dire : recompté à partir du JSON
cité, écart 0,0 ou à l'arrondi près (écarts signalés quand il y en a).

## 1. Tableau des candidats

| Candidat | Chiffres vérifiés (livre blanc → fichier) | Jugement | Reformulation simple |
|---|---|---|---|
| **A. §8.35 / §8.56 / §8.59 / §8.64 — maxsep sépare là où MC échoue** (§8.35 L883 ; §8.56 L6874 ; §8.59 L8225 ; §8.64 L10558) | Phase 2, 8 paires principales : MC **1/8** (HP35 seul, +0,1950 ; TCGA +0,0453 ; GSE71729 +0,0059 ; GSE62452 −0,0031 ; ICGC +0,0150 ; immunitaire +0,0545 ; PARP +0,0244 ; DepMap +0,0115) contre maxsep **6/8** (HP35 +1,6512 ; TCGA +0,2928 ; ICGC +0,0970 ; immunitaire +0,3675 ; PARP +0,1688 ; DepMap +0,1904 ; échecs GSE71729 +0,0402, GSE62452 −0,0036). Delta aussi 6/8. Vérifié dans `v61_phase2_table.json` (verdicts 1/8 et 6/8 exacts ; seul micro-écart : le livre blanc écrit DepMap d_MC +0,0116, le JSON donne +0,0115 — arrondi, 0,0001). §8.56/§8.59/§8.64 (re-vérifié 3 fois, 120/120 à 0,0 exact) : maxsep **37/48** rotations sans doublon et **6/8** principales, HP35 +1,6512 ; sep seul 35/48 et 5/8 ; ancien MC 12/48 et 1/8. Vérifié dans `sep_maxsep_856_table.json` (V1 : 6/8, 5/8, 1/8 ; V2 : 37/48, 35/48, 12/48 — exacts). | **JUSTE sur les chiffres, EXAGÉRÉE comme résumé général** — les chiffres sont exacts et re-vérifiés, mais le verdict « maxsep suffit » tient à une seule paire (ICGC +0,0970, marge +0,0270 au-dessus du plancher) et à l'échelle du plancher : D3 échoue (retirer n'importe quelle paire passante donne 5/7) et D4 échoue (au plancher équivalent-sep, 5/8, ICGC tombe). | On a trouvé un chiffre, maxsep, qui voit une différence entre les vraies données et les données mélangées là où l'ancien chiffre MC ne voyait rien — sur 6 cas sur 8. Mais ça tient à un cheveu : enlevez un seul cas, et ça ne passe plus. Ce n'est pas une victoire générale, c'est un indice fragile. |
| **B. §8.50 — consolidation MTAP, 10 nuls frais** (L4618) | Écarts S_sep réel−nul frais : **min +0,1110, médiane +0,1595, max +0,1981 — 10/10 au-dessus du plancher 0,07 ; 13/13 avec les 3 nuls anciens** (min +0,0715, le nul graine 7). Réel S_sep 0,3378. MC réel 0,3511 devant 9 nuls frais sur 10 (médiane nulle 0,3288 ; seul s11111 devant, 0,5192) ; Delta réel 3,8051 sous 8 nuls frais sur 10. Vérifié dans `mtap_consolidation_850_extract.json` (`stats_frais` et `stats_13_nuls` exacts ; MC et Delta frais exacts). | **JUSTE** — la distribution tient, la marge fragile du §8.46 (+0,0715) était bien la queue basse d'un tirage, pas la règle. | Sur une seule série (les tumeurs rangées selon la perte du gène MTAP), la différence entre vrai et mélangé tient contre 10 mélanges tout neufs, pas juste contre un seul. Mais c'est une seule série, et les deux autres chiffres (MC, Delta) ne séparent toujours pas. |
| **C. §8.72 — renverse de GSE79668 contre la distribution des nuls** (L14950) | Réel maxsep 0,4104 ; médiane des 13 nuls 0,2657 ; **d_médian +0,1447** (2,07 fois le plancher) ; **12/13 écarts au-dessus du plancher, rang 14/14** ; seul le nul graine 42 (+0,0567) est sous le plancher — et c'est le plus haut des 13 nuls (0,3538). Vérifié dans `extract_872.json` (réel 0,410448, médiane 0,2657, d_médian +0,1447, 12/13 — exacts). | **JUSTE** — le renversement est réel et mesuré sur 13 tirages, pas sur un seul. Mais la règle gelée interdit de recompter : C3 (au sens gelé, paires graine 42) n'est PAS levée par ce chantier seul, A2 gelé reste 6/10. | Une cohorte toute neuve, jugée d'abord ratée de justesse (+0,0567), passe en fait largement (+0,1447) quand on la compare à 13 mélanges au lieu d'un seul — parce que le premier mélange tiré était le pire possible. La lecture change, le verdict gelé, lui, ne change pas. |
| **D. §8.41 / §8.44 — S_sep sur les rotations** (§8.41 L2229 ; §8.44 L2854) | Avec doublon : **48/48** (somme +25,7324 ; min +0,0829 ACO2 ; max +1,1227 CTLA4) ; MC 17/48. Sans doublon (vrai compteur) : **37/48 sous la règle (A) 0,07, 42/48 sous (B) gigue 0** (somme +17,1614 ; min −0,1380 MYC ; max +0,9838 CD8A) ; MC 12/48. Vérifié dans `ssep_841_rotations.json` (48/48, somme 25,7324 — exacts) et `ssep_844_rotations.json` (37/48, 42/48, somme 17,1614 — exacts). | **EXAGÉRÉE si citée comme 48/48 ; JUSTE si citée comme 37/48 sans doublon.** Le 48/48 est doublon-assisté à la marge (11 paires tombent sans le doublon) et, surtout, c'est une mesure d'ordre par construction — trier par un flux que les autres suivent — pas une rupture ni un remède. Le livre blanc le dit lui-même (§8.41.5, §8.44.5). | Quand on range les tumeurs par un gène qui fait partie des gènes mesurés, l'instrument voit bien que les vraies données sont rangées et que les mélangées ne le sont pas — 37 fois sur 48 quand on enlève le trucage de construction. Ça prouve que l'instrument voit l'ordre, pas qu'il a trouvé une cassure du cancer. |
| **E. §8.79 — GSE57495, 13e paire** (L18554) | **d_maxsep +0,4494** (réel 0,6381 contre nul 0,1887), plus grand écart maxsep jamais mesuré sur une paire GEO ; A2 **9/13** (11/13 positifs), LOO 8/12 ; aucun nul frais (règle gelée : écart hors de l'intervalle [−0,07 ; +0,14[). Vérifié dans `extract_879_c3.json` (réel 0,6381, nul 0,1887, d +0,4494 ; MC réel 0,3920 contre nul 0,3283 — exacts). | **JUSTE** — le chiffre est exact et c'est le plus gros écart du dossier. Mais caveat écrit dans la section elle-même : GSE57495 était déjà le holdout direct (§8.66/§8.69) — jamais une confirmation indépendante de KRAS–CEACAM5. | Une cohorte neuve comme paire principale donne le plus gros écart jamais vu (+0,4494, plus de 6 fois le plancher). C'est le résultat le plus fort du dossier — mais cette cohorte avait déjà servi de test de contrôle ailleurs, donc ce n'est pas une confirmation toute neuve. |
| **F. §8.84 — lot drogue Chen 2025, paire exploratoire** (L20105) | **d_maxsep +0,0982** (réel 0,3478 contre nul 0,2496), consolidé 3/3 nuls au-dessus du plancher (+0,1528, +0,1607) ; 2 hits FDR < 0,05 (paclitaxel, mitomycine C) ; MC d +0,0015 (ne sépare pas). Vérifié dans `extract_884.json` (réel 0,3478, nul 0,2496, frais 0,1950 et 0,1870 — exacts). | **JUSTE** — chiffres exacts, consolidation réelle. Mais paire exploratoire, hors A2 (n = 46 organoïdes), axe gemcitabine et non KRAS ; drogue × KRAS et drogue × MTAP intestables (aucune table par-PDO publiée). | Sur des organoïdes de patients triés par leur sensibilité à un médicament, les autres médicaments suivent le même ordre — et deux médicaments ressortent après correction statistique. Intéressant, mais ce n'est pas l'axe KRAS et ce n'est pas compté dans le score principal. |

**Contre-candidats — ce qui contredit toute lecture générale de « mieux » (à mettre dans la balance) :**
- **§8.87 (L21395), consolidation GDC : FRAGILE CONFIRMÉ.** d_médian **+0,0314** (réel 0,2542 contre nul médian 0,2229), sous le plancher ; rang 13/14 ; seuls 2/13 écarts au-dessus du plancher ; aucun des 10 nuls frais ne passe. Vérifié dans `dist_887.json` (d_médian +0,0314, médiane 0,2229, rang 13/14 — exacts). La 14e paire (§8.85, +0,0884, marge 0,0184) tenait au tirage le plus favorable.
- **§8.88 (L21808), GSE194249 à 11 flux : 15e paire NON.** d_maxsep **−0,0239** (réel 0,2306 contre nul 0,2545) — le nul sépare plus que le réel. Vérifié dans `extract_888.json` (réel 0,2306, nul 0,2545, d −0,0239 — exact).
- **§8.69, GSE21501 : −0,0100** (réel 0,2121 contre nul 0,2221) ; **§8.70, GSE79668 graine 42 : +0,0567 PARTIEL**, A2 gelé 6/10, C3 non levée.
- Bilan net après §8.88 : A2 = 10/15. Les deux paires les plus récentes après §8.85 vont dans le sens inverse de « mieux » (une fragile confirmée, une négative).

## 2. Verdict global (une phrase)

Le podcast a dit juste que maxsep voit une différence entre vrai et mélangé là où l'ancien MC ne voit rien, mais il a exagéré en laissant croire à une victoire générale du pipeline, alors que c'est un seul indicateur, fragile à une paire près, jugé contre une batterie entière qui ne sépare pas et contredit par les paires les plus récentes.

## 3. Phrases du livre blanc qui ont pu nourrir une sur-interprétation

Ces formulations sont exactes dans leur contexte gelé, mais lues vite — ou par un résumé automatique — elles disent
« maxsep décide seul ». Elles appellent un addendum daté (voir §4.3), pas une réécriture de l'histoire :
- §8.56, titre et verdict (L6874–6885) : « **`maxsep` seul SUFFIT aux quatre barres gelées** » ; §7, ligne 62 : même formule.
- §8.59, titre (L8225) et §8.64 (L10558) : « **ADOPTER `maxsep` seul comme score MC** » ; §7, ligne 65.
- « **le critère gelé est `maxsep`, et lui seul** » — 5 occurrences : L13354 (§8.69), L15154 (§8.72), L15879, L16851 (§8.74/§8.76), L21632 (§8.87). C'est vrai du critère gelé de ces chantiers-là ; faux comme règle générale du projet.
- §8.70/§8.74, sous-sections « Les scores compagnons : **`maxsep` passe seul, les autres ne suivent pas** » (L16087, L17050).
- §8.41, verdict (L2229) : « **S_sep sépare le réel du nul sur les 48 rotations — 48/48** » — cité sans le « avec doublon » ni le « mesure d'ordre, pas rupture » qui suivent dans la même section, il devient une preuve qu'il n'est pas.
- §7, ligne 70 (§8.64) : « **30 changements de classe ancien → maxsep, tous en gain, 0 en perte** » — vrai, mais c'est un changement d'affichage, pas 30 découvertes.
- En revanche, le garde-fou existe déjà dans le livre blanc : §8.64.6 (L10768) fige la convention — maxsep principal **AFFICHÉ**,
  ancien MC secondaire affiché en second partout, sep compagnon, plancher publié, **mention de fragilité en tête de chaque table**,
  sélection inchangée (ancien composite), aucun changement de code. Et la décision de Zackary du 20 nov. 13h04 (L11014–11020) dit
  explicitement « **convention d'affichage uniquement** ». Le problème n'est pas l'absence de garde-fou, c'est que les titres et les
  résumés §7 ne le répètent pas — et c'est exactement ce qu'un podcast retient.

## 4. Correction de Zackary, 21 nov. 2026 11h00 — MC n'est JAMAIS seul (batterie complète)

### 4.1 Ce que dit la correction
Dans le pipeline, MC est accompagné de toute la batterie de diagnostics : les 29 estimateurs, les questions Q1–Q6,
les tests de bruit, les F1/F2 avant et après seuil, et le reste (L7a/L7b, falsification, Delta, maxsep).
Aucun verdict ne repose sur MC seul, ni sur maxsep seul.

### 4.2 Vérification dans le livre blanc : la batterie est documentée, mais comme décor, pas comme règle obligatoire
Comptages mesurés par grep dans le livre blanc (22 783 lignes) :
- « F1 » : **97 lignes, 116 occurrences** (le chiffre « 97 fois » de la consigne correspond aux lignes, pas aux occurrences).
- « 29 estimateurs » : **9 lignes, 11 occurrences**.
- « bruit » : **96 lignes, 100 occurrences** ; « Test de bruit » : **5 occurrences** (+ 1 « test de bruit » minuscule) ;
  `noise_diagnostic` : 1 ligne. **Le chiffre « 19 fois » pour les tests de bruit n'a pas pu être reproduit par aucun comptage
  lancé ici** — ni 19 lignes, ni 19 occurrences d'aucune des formes cherchées ; à ne pas reprendre tel quel sans re-compter.
- « batterie » : **0 occurrence**. « obligatoire » : **0 occurrence**.
- « Q1–Q6 » comme batterie de six questions : **non trouvée**. Q1–Q5 sont les positions de la cascade dans les tables
  (« Cascade (Q1–Q5, %) », ex. L15984) ; « Q6 » n'apparaît qu'une fois (L17854, nom d'estimateur dans une liste de NaN).
  « 4 tests de bruit » / « quatre tests » : **non trouvés**. Il y a un seul « test de bruit » par run
  (`noise_diagnostic.json`), dont les composantes (Hurst, etc.) ne sont pas présentées comme « 4 tests » dans le livre blanc.
  La liste de la correction ne se recopie donc pas telle quelle dans le vocabulaire du livre blanc — à reformuler dans
  l'addendum avec les noms que le livre blanc utilise vraiment (voir §4.2, liste ci-dessous).

Là où la batterie est documentée, c'est réel et précis :
- §8.31 (L728–733) : « Ce qui vient **du pipeline** : la cascade et le seuil MC, avec les composantes du score ;
  F1/F2 avant et après le seuil (`transition_analysis.json`, colonne « Tous », 29 estimateurs) ;
  le test de bruit (`noise_diagnostic.json`) » — plus les lectures de harnais (flux à chaque seuil, ordre de réaction).
- §8.32 (L819) : « **L7a, falsification, bruit, F1/F2 — rien ne sépare.** » — la batterie entière est lue, paire par paire.
- §8.35 (Phase 2) : 8 indicateurs lus ensemble sur les mêmes 8 paires (MC, Delta, maxsep, T_0, falsification, cohérence, L7a, cascade).
- §8.84.5 / §8.85.5 / §8.87 / §8.88 : chaque paire récente publie sa table complète (maxsep, ancien MC, sep, S_sep, Delta,
  cascade, stabilité, L7a, L7b, falsification, F1/F2, estimateurs tous OK).

Mais — et c'est le point de l'audit — **aucun endroit du livre blanc ne dit que la batterie est obligatoire pour le verdict**.
Les portes de décision sont toutes à un seul indicateur : A1/A2/A3 (§8.56), D1–D5 (§8.59/§8.64), C3 (§8.59.8, une paire
maxsep supplémentaire), A2 étendu (comptage de paires maxsep). La batterie est lue et publiée, puis le verdict est rendu
sur maxsep seul. La correction de Zackary est donc **une règle nouvelle à ajouter, pas la reformulation d'une règle existante** —
et c'est pour cela qu'elle doit entrer dans §8.90 comme une correction datée du 21 nov. 2026, apportée par lui.

### 4.3 Survente à corriger par addendum daté
Oui : le livre blanc présente maxsep comme « le » score qui décide seul — titres §8.56/§8.59 (§3 ci-dessus),
« le critère gelé est `maxsep`, et lui seul » (5 occurrences), et la formule « **maxsep score principal affiché** »
(§7 ligne 70 ; §8.64.6 point 1 : « Le score MC AFFICHÉ devient `maxsep` ») perd son qualificatif « affiché » dès qu'on
la résume. **Addendum proposé pour §8.90 (daté, 21 nov. 2026, correction de Zackary) : « `maxsep` est le score principal
AFFICHÉ, pas le verdict ; le verdict, c'est la batterie entière — cascade, MC et ses composantes, maxsep, S_sep, Delta,
L7a/L7b, falsification, test de bruit, F1/F2 sur les 29 estimateurs, lectures flux par flux. Aucune paire ne se décide
sur maxsep seul. »** Les portes à un seul indicateur (A2, C3) restent des portes d'affichage et de suivi, pas des verdicts.

### 4.4 Re-jugement du podcast contre la batterie entière (pas contre MC seul)
Jugée contre MC seul, la phrase du podcast (« mieux que les tests nuls ») est vraie pour maxsep et fausse pour MC —
c'est le piège. Jugée contre la batterie entière, elle devient : **EXAGÉRÉE**. Sur les paires principales, la batterie
entière ne sépare pas : MC 1/8, cohérence 2/8, L7a 4/8 (§8.35) ; seuls maxsep et Delta atteignent 6/8, et Delta n'est
pas élucidé (§8.37/§8.42). Sur les rotations sans doublon, MC 12/48, Delta dispersé, L7a mélangé (§8.44.4).
Si le podcast a fait croire que maxsep remplace toute la batterie, il faut le dire plainement : **c'est faux, et c'est à
corriger** — maxsep est une sortie parmi la batterie, affichée en premier depuis le 20 nov. 2026, et rien d'autre n'a changé.

## 5. Précision de Zackary, 21 nov. 2026 11h01 — « MC, c'est du pur bruit » : tranché en deux parties

### 5.1 Première partie — comme discriminateur réel contre nul sur le cancer, MC ne sépare PAS (c'est mesuré, pas une impression)
- **Phase 2, §8.35 (L883) : MC 1/8** (HP35 seul, +0,1950) ; sur les 7 paires PDAC, écarts +0,0453 / +0,0059 / −0,0031 / +0,0150 / +0,0545 / +0,0244 / +0,0115 — 7/8 positifs mais tous sous la gigue (±0,07) : MC penche du bon côté sans jamais dépasser le bruit. Vérifié dans `v61_phase2_table.json` (voir §1, candidat A).
- **Lot étendu, §8.31 (L688) : « Dans l'ensemble, le pipeline ne sépare pas le réel du nul : ni le score MC, ni Delta, ni la falsification »** ; falsification 16/21 réels contre 15/21 nuls — le nul fait presque aussi bien que le réel.
- **Rotations, §8.32 (L807) : MC 17/48** au-dessus du plancher 0,07 (vérifié dans `ssep_841_rotations.json` : 17/48, somme des écarts MC non publiée ici mais comptage exact) ; écart moyen **+0,044** ; le nul dépasse le réel sur 9/48 paires ; sans doublon (§8.44) : **MC 12/48** (vérifié dans `ssep_844_rotations.json`).
- **Test A, §8.34 (L869) : MC réel 0,3638 contre nul 0,4587 — le nul est au-dessus** (de +0,0949) ; même figure sous l'ordre MTAP (§8.36, L1060 : réel 0,3512 contre nul 0,5153) et sous le test C (§8.45 : 0,3472 contre 0,3507, ex æquo).
- Sur les paires PDAC principales, MC se comporte comme un tirage : il ne dit pas « ceci est réel, ceci est un nul ». Le dire plainement : **cette partie de l'affirmation de Zackary est vraie, et elle est mesurée.**

### 5.2 Deuxième partie — mais MC n'est pas un bruit pur au sens structurel (il a une structure mesurée)
MC est un composite à formule connue : `0,3·s_norm + 0,3·stability + 0,2·robustness + 0,2·sharpness` (§8.49, §8.56.2 ; code v6.2,
`evaluate_scan_quality`, L3314). Sa structure explique ses propres échecs, ce qu'un nombre aléatoire ne ferait pas :
- **§8.46 (arbitrage MTAP, L3040 et §7 ligne 52) :** l'inversion MC est portée par le seul terme de robustesse —
  réel **robustness 3,37×10⁻⁴¹, FWHM 78,26 %** (pic haut mais large) contre nul graine 42 **robustness 0,9756, FWHM 11,11 %**
  (pic étroit). Le MC récompense un pic étroit ; la marche réelle est haute mais large. Vérifié dans
  `mtap_consolidation_850_extract.json` (réel : robustness 3,3705048381947964e-41 ; nul 42 : 0,9756109800648465 — exacts).
- **§8.63 (L10142), M1 EXPLIQUÉ :** le MC haut est une propriété de la permutation — un pic étroit de la courbe de scan
  (FWHM ≈ 11–15 %) qui allume la robustesse — et le Delta bas une propriété de w = 27 (à w = 30, le réel lui-même tombe à 3,09).
  M2 partiellement expliqué : l'optimiseur maximise le MC sur 12 configurations fixes par n, il ne « reconnaît » rien du réel.
- **§8.73 (L15326) : le déclencheur du pic étroit est NON ÉLUCIDÉ** (bloc extrême 1/11, transplantations 0/3 et 0/6,
  AUC 0,31–0,47) — mais l'étroitesse est « une caractéristique réelle de la matrice, pas un artefact de calcul ».
  Structure mesurée, cause non élucidée : ce n'est pas la même chose que du bruit.
- **Contrôle positif HP35 — correction d'un chiffre de la consigne :** la consigne cite « HP35 il sépare (1,772 contre 0,121) ».
  Ces deux nombres sont ceux de **maxsep** (réel 1,7718 contre nul 0,1206, écart +1,6512 — vérifiés dans `v61_phase2_table.json`),
  **pas de MC**. Le MC sur HP35 vaut **0,6035 contre 0,4086 (écart +0,1950)** — il sépare aussi, mais modestement, et HP35 est
  le témoin positif connu (série synthétique de contrôle), pas une tumeur. Citer 1,772/0,121 comme « MC » serait faux ;
  comme maxsep, c'est exact.

### 5.3 Formulation simple, prête à reprendre dans §8.90
> « Le chiffre MC ne dit pas si des données sont vraies ou mélangées quand il s'agit du cancer du pancréas : sur les cas
> principaux, il ne sépare qu'une fois sur huit, et il arrive même que le mélange obtienne un meilleur chiffre que le vrai.
> Mais MC n'est pas un nombre tiré au hasard : on sait exactement pourquoi il se trompe — il récompense les pics étroits,
> et ce sont souvent les mélanges qui en produisent. Donc : MC ne porte pas de signal pour dire vrai ou faux sur le cancer,
> mais ce n'est pas du bruit sans forme. Et ça ne veut pas dire que le pipeline ne vaut rien : le pipeline sort aussi
> maxsep et toute la batterie, et c'est l'ensemble qu'il faut regarder, pas MC tout seul. »

Ni « MC = bruit » lu comme « le pipeline ne vaut rien », ni « MC = signal » lu comme « le pipeline prouve » : les deux
lectures sont fausses, et les chiffres ci-dessus disent pourquoi.

## 6. Réponse vérifiée dans le code v6.2 lui-même, 21 nov. 2026 11h03 — le pipeline utilise LES DEUX

Fichier vérifié : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` (conforme au SHA v6.2 du livre blanc).
- **Ligne 3333, dans `evaluate_scan_quality` (définie L3314) : `max_separation = scores[max_idx]`** — le maximum de la
  courbe de scan (|d de Cohen| pré/post-seuil). La fonction retourne ensemble `max_separation`, `s_norm`, `stability`,
  `robustness`, `sharpness` (retour anticipé L3324–3326 avec les cinq champs à 0,0 si courbe trop courte ; même
  dictionnaire en retour normal). Appelée L3477 (`quality_metrics = evaluate_scan_quality(...)`). **maxsep était donc
  déjà émis par v6.2, dans chaque run.**
- **Ligne 10095, `def compare_monte_carlo_regimes(...)`** — le calcul Monte Carlo (3 paradigmes : marche aléatoire,
  semi-harmonique, et troisième régime dans la docstring). Appelée L10486 (`ablation_res = compare_monte_carlo_regimes(...)`),
  et son résultat est retourné dans le dictionnaire de sortie, **L10536 : `"mc": mc`**. **MC est donc toujours calculé
  et toujours rapporté, dans le même run que maxsep.**
- **Aucun des deux n'a été ajouté après coup, et l'adoption de maxsep comme score principal affiché n'a demandé AUCUN
  changement de code (pas de v6.5)** — confirmé par §8.59/§8.64 (« aucune v6.5 créée, aucun code modifié : l'adoption,
  si elle est décidée, est une décision d'AFFICHAGE sur la v6.2 existante ») et par la décision de Zackary du 20 nov. 13h04
  (§8.64, L11014–11020 : « convention d'affichage uniquement »).

**Bonne formulation, à mettre dans §8.90 : le pipeline sort MC et maxsep ensemble, avec toute la batterie. Ce qui a
changé, c'est seulement lequel on affiche en premier dans le livre blanc — pas ce que le pipeline calcule. Si le livre
blanc ou le podcast laisse croire que le pipeline « utilise maxsep au lieu de MC », c'est faux et c'est à corriger.**

## 7. Limites de ce volet
- Le podcast lui-même n'a pas été écouté ni transcrit : sa phrase n'est connue que par le résumé de Zackary
  (« mieux que juste les tests nuls, quelque chose à voir avec MC »). Les jugements ci-dessus portent sur ce résumé,
  pas sur les mots exacts du podcast.
- §8.31 (lot étendu) et §8.34 (Test A) : chiffres repris du livre blanc sans re-vérification JSON dans ce volet
  (les JSON existent — `v61_phase2_table.json` couvre les paires principales, `testa_extract.json` le test A —
  mais n'ont pas été relus ici pour ces deux sections) ; §8.32 : comptage MC 17/48 re-vérifié, moyenne +0,044 reprise du livre blanc.
- Le comptage « 19 fois » pour les tests de bruit (consigne 11h00) n'a pas pu être reproduit (voir §4.2) — à re-compter
  avant toute reprise dans §8.90.
- Aucun addendum n'a été écrit dans le livre blanc par ce volet (lecture seule) : les addendums proposés (§4.3, §6)
  sont des textes à faire valider et insérer par le coordinateur.

## 8. Résumé (5 lignes maximum)
- **Corrections de Zackary (21 nov.) : MC n'est jamais seul — la batterie entière fait le verdict, pas maxsep seul ;
  MC ne sépare pas le vrai du mélangé sur le cancer mais n'est pas un nombre sans structure ;
  le code v6.2 calcule MC et maxsep ensemble (lignes 3333 et 10095), seul l'ordre d'affichage a changé.**
- Le podcast a vu juste sur un point précis : maxsep sépare 6/8 paires principales là où l'ancien MC n'en sépare qu'1/8
  (chiffres exacts, re-vérifiés), et GSE79668 renverse à +0,1447 contre 13 nuls, MTAP tient 10/10.
- Il a exagéré en généralisant : le 6/8 tient à une paire (ICGC), les rotations sans doublon font 37/48 et non 48/48,
  et les paires récentes contredisent « mieux » (GDC fragile confirmé +0,0314, GSE194249 NON à −0,0239).
- Le livre blanc nourrit la sur-interprétation par ses titres (« maxsep seul SUFFIT », « critère gelé est maxsep, et lui seul »),
  alors que sa propre convention (§8.64.6) dit « affichage uniquement » — addendum daté proposé au §4.3.
- Verdict global : ce qui a été trouvé de vrai, c'est qu'un seul chiffre (maxsep) voit une différence là où l'ancien MC
  ne voyait rien — pas une preuve générale, pas un remède, et pas un remplacement de la batterie.
