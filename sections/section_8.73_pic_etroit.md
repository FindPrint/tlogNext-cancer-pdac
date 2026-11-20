### 8.73 Le déclencheur du pic étroit — non élucidé, le bloc extrême écarté (20 novembre 2026)

**Verdict d'abord, en trois phrases. (a) NON ÉLUCIDÉ — aucun déclencheur
identifiable du pic étroit : le bloc de lignes extrêmes au bord ne porte
pas le pic (déplacement du bloc : succès 1/11 au critère gelé ;
transplantation de valeurs donneuses au bord : 0/3 ; transplantation du
propre bloc extrême : 0/6), aucune statistique globale ne sépare les
courbes rob-on des rob-off (AUC 0,31–0,47), et un bloc d'extrémité
médiane déplacé au bord crée même un pic (1/2). (b) Ce qui est établi :
l'étroitesse est une propriété fragile de l'arrangement exact des
lignes — le déplacement du bloc détruit la robustesse (rob < 0,1) dans
10/11 cas sans détruire le niveau du pic (10/11), tandis que le pic
étroit survit à la poussière numérique (0/11 bascule à 10⁻³) : c'est une
caractéristique réelle de la matrice, pas un artefact de calcul, mais
elle n'est portée par aucun bloc, aucune ligne en général (une seule
ligne tue le pic dans 4/11 cas seulement, contre 5/33 pour une ligne
prise au hasard) et aucune queue de distribution. (c) La winsorisation
du bloc, qui semblait tuer le pic (10/11 à l'échelon 4 fenêtres), est
un artefact de déflation de variance — elle fait MONTER le maxsep dans
8/11 cas à l'échelon 2 fenêtres (0,1434 → 0,2916 ; 0,2072 → 0,3583) en
aplatissant la courbe, et winsoriser n'importe quel autre bloc fait la
même chose (6/11) : le critère gelé A1 compte un effet générique, pas
la suppression d'un déclencheur, et il est rapporté comme tel sans
peser dans le verdict.**

## 8.73.1 Question, méthode, règles

**Question.** §8.63 a expliqué M1 (le MC haut est une propriété de la
permutation, le Delta bas une propriété de w = 27) mais a laissé ouvert
le résidu : qu'est-ce qui DÉCLENCHE le pic étroit de la courbe de scan
(FWHM ≈ 11–15 %, rob > 0,5) quand on permute — quelle propriété de la
matrice permutée le fait apparaître, et pourquoi certaines permutations
le déclenchent et d'autres non ? Les pics tombent presque tous près
d'un bord (seuil 10–33 % ou 76–89 %) et, pour un même CSV, à la MÊME
position (±2 candidats) sous plusieurs configs — compatible avec un
bloc fixe dans l'ordre des lignes, pas avec une propriété de la grille.

**Hypothèses nommées d'avance (protocole §3).** **H1 (principale — bloc
extrême au bord)** : un bloc de w+1 lignes consécutives aux valeurs
extrêmes sur plusieurs flux, isolé comme petit groupe par un seuil
proche d'un bord, déclenche le pic. **H2 (une seule ligne)** : le pic
est porté par une seule ligne extrême du bloc. **H3 (queues
globales)** : les CSV rob-on ont des queues plus lourdes, indépendamment
de la position des lignes extrêmes. **H4/H5 (bord seul)** : un seuil
proche du bord suffit, même sans bloc extrême. **H0 (fluctuation
d'ordre / comparaisons multiples)** : aucun bloc, aucune propriété de
ligne ne déclenche le pic — c'est le max sur ~12 configs × ~30–90
candidats de courbes bruitées.

**Méthode.** Protocole gelé `PROTOCOL_pic_etroit_873.md` (SHA
`28d2326c3ae83676d3e15f7283f0b37ae69a1791bcaa1f50c7b06ee368651a4c`,
écrit avant tout nouveau script, toute nouvelle construction et tout
nouveau run). Quatre volets, dans l'ordre : (A) calibration de la
réplique du scan (fonctions DU PIPELINE importées en lecture seule) ;
(B) statistiques de corpus sur les 82 runs existants (14 MTAP + 68
immunitaires) ; (C) interventions sur les 11 courbes GAGNANTES rob-on
(relues §8.63 : MTAP NUL42, NUL_S123, NUL_S11111 ; icgc_s1,
geo62452_nul_s12, tcga_s2, tcga_nul_s11, tcga_nul_s12, icgc_nul_s32,
icgc_nul_s35, icgc_nul_s37) — déplacement du bloc (swap), winsorisation
du bloc (échelle 2/4/8 fenêtres), winsorisation d'une seule ligne ;
(D) interventions sur 6 contrôles (gagnante rob = 0,0000 : MTAP s7,
s1011 ; ICGC s31, s33 ; GSE62452 s11 ; TCGA s13) — transplantation du
propre bloc extrême au bord (B1), bloc médian au bord (B0),
transplantation de valeurs donneuses (B2 : s11111 → s1011,
s37 → s31, s33) ; (E) lot frais hors échantillon de 20 nuls ICGC
(graines 41–60, jamais utilisées), avec prédictions écrites AVANT toute
lecture des résultats frais (§8.73.6).

**Mécanique lue dans le code v6.2 (pas devinée).** Scan
(`_scan_critical_threshold_fast`, lignes 3125–3287) : lignes triées par
l'axe de progression (monotone en l'indice de ligne) ; fenêtres
glissantes de longueur w ; candidats = linspace(0, 100, ncand) ; à
chaque candidat c, split(c) = nombre de fenêtres avec win_progress < c ;
score(c) = moyenne sur les 12 flux du |d de Cohen| entre les contenus
des fenêtres basses et hautes (chaque ligne apparaît dans jusqu'à w
fenêtres, avec recouvrement ; win_order = identité, vérifié et asserté
à chaque usage). Robustesse (lignes 3314–3389) :
rob = exp(−((FWHM − 10)²)/(2·5²)), FWHM = largeur à mi-hauteur contiguë
autour du pic. Deux candidats voisins ne diffèrent que par le passage
d'environ n_windows/ncand fenêtres d'un groupe à l'autre : un pic
étroit exige que les fenêtres qui franchissent la coupure aient des
contenus collectivement très différents du reste — d'où la recherche
du déclencheur comme un BLOC DE LIGNES (w+1 lignes : les deux fenêtres
frontières au seuil du pic).

**Définitions gelées.** Extrémité de ligne e_i = moyenne sur les 12
flux de |z_ij|, z robuste (médiane/MAD, facteur 1,4826). Extrémité de
fenêtre E_k = moyenne de e_i sur les lignes k..k+w−1. G(c) = moyenne de
e_i sur les lignes distinctes du petit côté à c (non signée, sans
cohérence de signe) ; H(c) = moyenne sur les flux de |moyenne de z sur
le petit côté| (écart cohérent — voisin du numérateur du |d| du scan ;
sa valeur prédictive mesure si le déclencheur est localisable à un
petit groupe, pas une preuve indépendante du scan). Candidats de bord :
min(split, n_windows − split) ≤ 20 % des fenêtres.

**Règles de décision écrites avant (protocole §5).** DÉCLENCHEUR
IDENTIFIÉ (H1) si calibration OK ET A-swap ≥ 9/11 ET A1 ≥ 9/11
(échelon 2 ou 4 fenêtres) ET B2 ≥ 2/3 ET B0 = 0/2. PARTIELLEMENT
IDENTIFIÉ si A-swap et A1 tiennent mais B2 ou B0 échoue.
NON ÉLUCIDÉ si A-swap < 9/11 ou A1 < 9/11 à tous les échelons.
P1/P2 hors échantillon : qualification seulement (succès P1 si ≥ 70 %
des pics frais à ±2 pas du candidat prédit par G, avec ≥ 5 courbes
rob-on fraîches ; succès P2 si AUC de H_max ≥ 0,80).

## 8.73.2 Calibration — la réplique est exacte, 22/22 à 0,00e+00

La réplique du scan (fonctions du pipeline importées, même pattern que
§8.63) reproduit à **0,00e+00** (métriques et courbes) les 5 entrées
§8.63 × 12 configs (MTAP réel, s11111, s123, ICGC réel, ICGC nul s29)
ET les 11 courbes rob-on + 6 contrôles à leur config gagnante — 22/22,
aucune exclusion. Toutes les interventions ci-dessous sont donc lues
sur des courbes exactes, pas approchées.

## 8.73.3 Corpus — aucune statistique globale ne sépare rob-on de rob-off (H3 écartée)

Sur les 82 gagnantes (11 rob-on, 67 rob-off avec rob < 0,05) :

| Statistique (gagnante) | Médiane rob-on | Médiane rob-off | AUC | p (Mann-Whitney) |
|---|---|---|---|---|
| H_max (écart cohérent du petit côté) | 0,2287 | 0,2785 | 0,309 | 0,044 |
| E_max (fenêtre la plus extrême) | 1,0018 | 1,0191 | 0,400 | 0,29 |
| max e_i (ligne la plus extrême) | 2,1878 | 2,1878 | 0,468 | 0,73 |
| Kurtosis moyenne des flux | 0,0457 | 0,0457 | 0,387 | 0,24 |

Aucune ne sépare — et H_max est même INVERSÉE (plus faible chez les
rob-on, p = 0,044) : les courbes à pic étroit ont un écart cohérent du
petit côté plus petit que les courbes sans pic. **H3 est écartée** : ce
n'est pas une histoire de queues lourdes. La position du pic n'est pas
non plus prédite par l'extrémité des lignes : le candidat argmax G(c)
tombe à ±2 pas du vrai pic dans 5/11 cas seulement — le niveau du
hasard (~45 % sur ~11 candidats de bord). Les fenêtres frontières
elles-mêmes sont banales : leur rang d'extrémité parmi toutes les
fenêtres est de 63/70 (s11111), 86/88 (s123), 112/130 (NUL42, parmi
les MOINS extrêmes), 37/36 (icgc_s1) — seules geo s12 (11/14), s35
(17/20) et s37 (16/12) ont des frontières plutôt extrêmes. Le bloc
n'est pas extrême là où le pic se produit : H1 est déjà fragilisée
avant toute intervention.

## 8.73.4 Interventions sur les 11 courbes rob-on — le bloc ne porte pas le pic

### A-swap (déplacer le bloc au milieu) : 1/11 — le niveau survit, l'étroitesse meurt

| Run | Score au vieux seuil après swap | 0,5 × maxsep ancien | rob après swap | FWHM avant → après |
|---|---|---|---|---|
| NUL42 | 0,0857 | 0,0717 | 0,0000 | 11,11 → 68,89 |
| NUL_S123 | 0,1171 | 0,1046 | 0,0000 | 14,81 → 77,78 |
| NUL_S11111 | 0,2194 | 0,0941 | 0,2343 | 11,11 → 18,52 |
| icgc_s1 | 0,1630 | 0,0898 | 0,0869 | 10,53 → 21,05 |
| geo62452_nul_s12 | 0,1926 | 0,1036 | 0,0000 | 14,29 → 52,38 |
| tcga_s2 | 0,1050 | 0,0707 | 0,9756 | 11,11 → 11,11 |
| tcga_nul_s11 | 0,0816 | 0,0995 | 0,0000 | 9,78 → 78,26 |
| tcga_nul_s12 | 0,2904 | 0,1149 | 0,0010 | 14,29 → 28,57 |
| icgc_nul_s32 | 0,1082 | 0,0905 | 0,0000 | 15,38 → 46,15 |
| icgc_nul_s35 | 0,1752 | 0,1242 | 0,0000 | 14,71 → 57,14 |
| icgc_nul_s37 | 0,1888 | 0,2077 | 0,0000 | 14,29 → 33,33 |

Succès au critère gelé (score au vieux seuil < 0,5 × maxsep ET aucun
voisin à ±2 pas au-dessus) : **1/11** (seule tcga_nul_s11). Dans 10/11
cas le niveau au vieux seuil survit au déplacement du bloc — il monte
même dans 3 cas (s11111 : 0,1882 → 0,2194 ; tcga_nul_s12 :
0,2298 → 0,2904 ; le maxsep après swap monte aussi pour s35 et s37
en partie). Mais la ROBUSTESSE, elle, s'effondre : rob < 0,1 dans
10/11 cas (toutes sauf tcga_s2, où rob reste 0,9756 et FWHM 11,11 —
le pic survit intégralement au swap, seul contre-exemple). Lecture :
le déplacement du bloc détruit l'ÉTROITESSE, pas le niveau. Le bloc
ne porte donc pas le pic comme un objet (son niveau survit à son
départ) ; sa position participe à la forme étroite — avec une réserve
de lecture (§8.73.7) : le swap confond le départ de B et l'arrivée du
bloc médian M à sa place, on ne peut pas départager les deux moitiés
de l'intervention. Après le swap, le nouveau pic reste à l'ancienne
position dans 6/11 cas, suit le bloc B dans 1/11 cas seulement
(NUL42), et va ailleurs dans 4/11 cas : le pic ne suit pas le bloc.

### A1 (winsoriser le bloc) : le critère gelé compte 10/11 — mais c'est un artefact

| Échelon | Succès (rob < 0,1) |
|---|---|
| (a) 2 fenêtres frontières | 8/11 |
| (b) 4 fenêtres | 10/11 |
| (c) 8 fenêtres | 11/11 |

Ce comptage est trompeur, et il est rapporté comme tel : à l'échelon
(a), le maxsep MONTE dans 8/11 cas (NUL42 : 0,1434 → 0,2916 ; s123 :
0,2092 → 0,2750 ; s11111 : 0,1882 → 0,2644 ; geo s12 :
0,2072 → 0,3583 ; s35 : 0,2484 → 0,2771 ; s37 : 0,4154 → 0,2770 est
une des 3 baisses, avec tcga_s11 0,1989 → 0,1483 et s32
0,1810 → 0,1774) et le score au vieux seuil devient le maximum (ou
presque) de la nouvelle courbe : la courbe ne s'effondre pas, elle
MONTE partout et s'aplatit. Mécanisme : winsoriser des lignes à la
médiane les rend constantes, ce qui déflate l'écart-type poolé du |d|
de Cohen et gonfle les scores sur tous les candidats — la courbe
plate à haut niveau a une FWHM énorme, donc rob → 0. Le critère
« rob < 0,1 » mesure l'aplatissement, pas la mort du pic. Preuve par
le contrôle (diagnostic post-hoc D1, §8.73.7) : winsoriser le bloc
médian M, qui n'a rien à voir avec le pic, tue rob dans 6/11 cas de
la même façon. **A1 ne prouve donc pas que le bloc porte le pic** —
il prouve que la winsorisation déflate la variance. Le comptage gelé
(10/11 à l'échelon b) est consigné tel quel, mais il ne pèse pas
dans l'interprétation du verdict.

### A2 (winsoriser une seule ligne) : 4/11 — parfois une ligne, jamais en général

Winsoriser la seule ligne la plus extrême du bloc (argmax e_i) tue
rob dans 4/11 cas : NUL42 (ligne 126, e = 1,85, rob 0,9756 → 0,0000),
NUL_S11111 (ligne 31, e = 2,05, 0,9756 → 0,0000), icgc_nul_s32
(ligne 42, e = 1,86, 0,5600 → 0,0000), icgc_nul_s35 (ligne 10,
e = 1,85, 0,6926 → 0,0221). Dans les 7 autres cas rob reste > 0,1
(0,1945 à 0,9991 ; s123, geo s12 et tcga_s2 inchangés à la 4e
décimale). **H2 est partielle** : dans 4 cas le pic tient à une
seule ligne, dans 7 cas non — ce n'est pas le déclencheur général.
Et le contrôle post-hoc D5 relativise même ces 4 cas : winsoriser
une ligne prise AU HASARD tue le pic dans 5/33 cas (15 %), contre
4/11 (36 %) pour la ligne la plus extrême — la ligne extrême compte
plus qu'une ligne quelconque, mais la sensibilité à une seule ligne
est en partie une fragilité générique de ces courbes (NUL42 et s35 :
2/3 lignes aléatoires tuent aussi le pic ; s11111 et s32 : 0/3 et
1/3 — là, c'est bien la ligne extrême qui compte).

## 8.73.5 Interventions sur les contrôles — l'extrême au bord ne crée rien, l'ordinaire crée un pic

| Contrôle | B1 (propre bloc extrême au bord) | B2 (valeurs donneuses au bord) | B0 (bloc médian au bord) |
|---|---|---|---|
| MTAP s7 | rob 0,0000, maxsep 0,2685 | — | — |
| MTAP s1011 | rob 0,0000, maxsep 0,2178 | rob ~0, maxsep 0,2283 (donneur s11111) | — |
| ICGC s31 | rob 0,0000, maxsep 0,2557 | rob ~0, maxsep 0,2483 (donneur s37) | — |
| ICGC s33 | rob 0,0000, maxsep 0,2480 | rob 0,0257, maxsep 0,2235 (donneur s37) | — |
| GSE62452 s11 | rob 0,0000, maxsep 0,3704 | — | rob ~0, pas de pic |
| TCGA s13 | rob 0,0000, maxsep 0,4670 | — | **rob 0,9263, maxsep 0,3012, seuil 10,87 % : pic créé** |

**B1 : 0/6.** Déplacer le propre bloc le plus extrême d'un contrôle
au bord ne crée AUCUN pic étroit : rob = 0,0000 partout, avec des
maxsep de 0,22 à 0,47 — la courbe devient un plateau large. Un bloc
extrême au bord élève les scores sur une large plage de candidats
(il reste dans le petit groupe tant que la coupure ne l'a pas
dépassé), il ne crée pas un pic étroit. **B2 : 0/3.** Transplanter
les valeurs exactes d'un bloc donneur rob-on (s11111, s37) au bord
d'un contrôle ne crée rien non plus (rob ~0 à 0,026) : les valeurs
ne suffisent pas. **B0 : 1/2.** Déplacer un bloc d'extrémité MÉDIANE
au bord crée un pic étroit chez TCGA s13 (rob 0,9263, FWHM ≈ 10,9 %,
seuil 10,87 %, au bord comme prédit) et rien chez GSE62452 s11.
L'extrémité n'est donc ni nécessaire (un bloc médian crée un pic) ni
suffisante (un bloc extrême n'en crée pas). Le pic apparaît ou non
selon le réarrangement exact — c'est la signature d'une fluctuation
d'arrangement (H0), pas d'un déclencheur identifiable.

## 8.73.6 Confirmation hors échantillon (lot frais s41–s60) — aucun pic étroit, la prédiction H_max échoue

Lot v6.2 fast terminé le 20 nov. 2026 à 21:44:34Z (unité systemd
`v62-873`, 20 runs, graines 41–60 ; **20/20 exit 0, 0 échec** — dont
une reprise après redémarrage machine vers 21:21Z : le run s52,
interrompu sans `master_results.json`, a été relancé tel quel après
suppression de son dossier partiel, sans changer de graine ;
SHA v6.2 vérifié avant le lot, avant la relance et après le lot :
`f07567c4…ec3abf`). Prédictions écrites AVANT toute lecture des
résultats frais : `pic_etroit_873_predictions.json`
(SHA `10c599f7c6d460bda9b294a553808abc9d81bd0776cc9633540c80b57779f2cd`,
20:46:17Z, 0 résultat frais existant alors). Réplique des 240 courbes
fraîches : écart **0,00e+00** (métriques et courbes).

**Résultat : 0 courbe rob-on sur 240, 0 gagnante rob-on sur 20.**
La gagnante est (35, 16, 6) dans 17/20 cas et (22, 16, 7) dans 3/20
(s42, s47, s51) ; MC gagnant 0,319–0,409 (médiane 0,340) ; rob
gagnante 0,0000 partout sauf s50 (0,3105) et s51 (0,0010). Le max de
rob sur les 12 configs d'un run est ≤ 0,0327 pour 19/20 runs (seul
s50 atteint 0,3105) ; 3/240 courbes dépassent rob > 0,1, 1/240
dépasse 0,3, aucune ne dépasse 0,5. Dans le corpus existant, 25/996
courbes (2,51 %) et 11/83 gagnantes (13,25 %) sont rob-on — mais
concentrées dans 11 runs seulement (5, 4, 2, 2, 2, 2, 2, 2, 2, 1, 1
courbes par run ; 72 runs à zéro). L'absence observée ici n'est donc
PAS significative au niveau run, le seul niveau honnête vu la
corrélation des 12 courbes d'un run : P(0/20 gagnantes | p = 0,1325)
= 0,058 ; le p naïf par courbe (0,002) surestime la significativité
et il est rapporté comme tel, avec sa réserve.

**P1 (position) : non testable.** Aucune courbe rob-on fraîche :
0/0 — descriptive seulement, comme prévu au protocole §5 quand il y
a moins de 5 courbes rob-on fraîches. **P2 (magnitude) : échec.**
Sur les 140 courbes à T_H défini (100 exclues, T_H indéfini pour 4
configs sur 12), H_max prédit 23 courbes rob-on — **0 réelle** :
TP = 0, FP = 23, FN = 0, TN = 117 ; AUC indéfinie (aucun positif).
H_max sur-prédit (16 % de faux positifs) et ne prédit rien de vrai :
la prédiction par l'écart cohérent du petit côté ne se généralise
pas hors échantillon. La généralisation du déclencheur n'est donc
pas confirmée — et, avec 0 courbe rob-on fraîche, il n'y avait rien
à généraliser dans ce lot. Ce lot ne change pas le verdict
(NON ÉLUCIDÉ) : il le renforce en montrant que le pic étroit est
rare et imprévisible par H_max, et que le taux de gagnantes rob-on
(13 % dans le corpus) ne se reproduit pas sur 20 tirages frais
(0/20, p = 0,058).

## 8.73.7 Diagnostics post-hoc (hors protocole gelé — interprétation seulement)

Ajoutés après lecture des premiers résultats d'intervention, ils
n'entrent pas dans les règles de décision du §5.

- **D1 — winsoriser le bloc médian M tue rob dans 6/11 cas.** Même
  ordre de grandeur qu'A1 à l'échelon (a) (8/11) : la winsorisation
  tue la robustesse quel que soit le bloc, par déflation de variance
  (§8.73.4, A1). Le maxsep après winsorisation de M monte lui aussi
  (ex. NUL42 : 0,1434 → 0,1533 ; s123 : 0,2092 → 0,2283).
- **D2 — la courbe de scan n'est pas l'excursion de la moyenne
  cumulative.** Spearman entre le score par candidat et l'écart de
  la moyenne du groupe bas : de −0,49 (tcga_s2) à +0,69
  (tcga_nul_s12), médiane ~0,26, sans signe systématique. Le pic
  n'est pas porté par la moyenne cumulative des premières lignes.
- **D3 — après le swap, le pic ne suit pas le bloc.** Nouveau pic à
  l'ancienne position dans 6/11 cas, à la position du bloc déplacé
  dans 1/11 cas (NUL42), ailleurs dans 4/11 cas.
- **D5 — sensibilité à une ligne quelconque : 5/33 (15 %).** Contre
  4/11 (36 %) pour la ligne la plus extrême (A2). La ligne extrême
  compte plus qu'une ligne au hasard, mais la sensibilité à une
  seule ligne est en partie générique.
- **D6 — le pic survit à la poussière numérique.** Arrondi à 6
  décimales : 0/11 bascule de rob ; bruit gaussien 10⁻³ de
  l'écart-type du flux : 0/11 ; bruit 10⁻² : 2/11 (NUL42, s37).
  Le pic est une caractéristique réelle de la matrice, pas un
  artefact de calcul en virgule flottante — sa fragilité est au
  réarrangement des lignes, pas au bruit numérique.

## 8.73.8 Ce que ça change, et ce que ça ne change pas

**Change.** (1) Le résidu ouvert de §8.63 est fermé comme question
de déclencheur identifiable : il n'y a PAS de bloc déclencheur — ni
bloc extrême (A-swap 1/11, B1 0/6, B2 0/3), ni ligne unique en
général (A2 4/11), ni queues globales (AUC ≤ 0,47), ni bord seul
(B0 1/2, dans les deux sens). Ce qui déclenche le pic étroit, c'est
l'arrangement exact des lignes : une fluctuation de la courbe de
scan dont l'étroitesse meurt au réarrangement (rob < 0,1 dans
10/11 swaps) et qui peut naître d'un réarrangement ordinaire
(B0 1/2). (2) La robustesse du MC est un interrupteur fragile à
l'arrangement : une seule ligne peut la faire basculer (4/11 pour
la ligne extrême, 5/33 pour une ligne au hasard), et la winsorisation
la tue par déflation de variance — toute lecture « rob-on = signal »
doit en tenir compte, et le critère « rob < 0,1 » ne prouve pas à
lui seul qu'un pic est mort (§8.73.4, A1). (3) Le niveau du pic et
son étroitesse sont deux choses différentes : le niveau survit au
réarrangement (10/11), l'étroitesse non (10/11) — les lectures
futures doivent les séparer. (4) Le lot frais ne reproduit pas le
taux de pics étroits du corpus (0/20 gagnantes rob-on, 0/240
courbes ; §8.73.6) et la prédiction H_max y échoue (23 faux positifs,
0 vrai positif) : le pic étroit est rare et imprévisible par les
statistiques locales testées.
**Ne change pas.** Aucun verdict de séparation n'est touché : S_sep
sépare toujours sur la série MTAP (§8.50), le réel ICGC reste sous
le plancher n≈70 (§8.53), le rationnel vopimetostat + daraxonrasib
n'est ni renforcé ni affaibli. La marche de niveau multi-flux (§8.46)
vit dans les CSV, pas dans ces mécanismes. Le Delta reste une
propriété de w (§8.63). Le taux de courbes rob-on sur les nuls
frais (§8.73.6) ne change rien à ces verdicts.

## 8.73.9 Méthode

Protocole gelé avant tout nouveau script et tout nouveau run :
`PROTOCOL_pic_etroit_873.md`, SHA
`28d2326c3ae83676d3e15f7283f0b37ae69a1791bcaa1f50c7b06ee368651a4c`.
**(A)** `pic_etroit_873.py` (SHA `33821df3d894a0e2a7eb4b882a546fe2f4f66fa21366c239b155aa26de24bba7`) :
calibration 22/22 EXACTE (écart 0,00e+00 sur métriques et courbes).
**(B)** Corpus : 82 gagnantes relues (extract §8.63), H(c)/G(c)/E_max/
kurtosis calculés depuis les CSV. **(C)** Interventions A/A1/A2 sur
les 11 courbes rob-on (réplique exacte, CSV modifiés
`pic873_interv_<run>_<variante>.csv`, SHA consignés dans l'extract).
**(D)** Interventions B1/B0/B2 sur les 6 contrôles. **(E)** Lot v6.2 :
`build_nulls_icgc_873.py` (SHA `3e0e222eedb9600c53a94daa97ae570614b9d6c3749852722cb098bf51cd2d2e`),
`run_v62_873.sh` (SHA `3d9093efae9678fa2c66953d71c807904cc8d7382d9b3b6c9cc6ee1a84065768`),
`watch_v62_873.sh` (SHA `5c38496482785eee4a28d826b6a6ff4d7ec5fa27cc268609ba712bdc0e5b6404`),
manifeste `manifest_v62_873.txt`, unité systemd `v62-873` (lancée
20:43:56Z, 11/20 à 21:20:25Z ; redémarrage machine vers 21:21Z,
reprise 21:22:44Z après suppression du dossier partiel s52 ;
terminée 21:44:34Z, 20/20 exit 0, 0 échec). **Prédictions** :
`predict_pic_etroit_873.py` (SHA `473e4dddfa7559f1406b3a773c92f879b766b15b2e480dc0b344c5128cc63627`),
`pic_etroit_873_predictions.json` (SHA `10c599f7c6d460bda9b294a553808abc9d81bd0776cc9633540c80b57779f2cd`,
écrit 20:46:17Z, avant toute lecture des frais). Diagnostics post-hoc
D1/D2/D3/D5/D6 : mêmes scripts, volets `diag`/`diag2`, hors protocole
gelé, étiquetés comme tels.

## 8.73.10 Limites

- Mode fast seulement : 12 configs par run. Les nombres (taux,
  échelons) sont propres au mode fast.
- Le critère gelé A-swap porte sur le NIVEAU au vieux seuil, pas sur
  l'étroitesse : il échoue (1/11) alors que l'étroitesse, elle, meurt
  dans 10/11 swaps — la distinction niveau/étroitesse n'était pas
  dans le protocole, elle est consignée ici comme lecture
  descriptive, pas comme un succès d'A-swap.
- Le critère gelé A1 (rob < 0,1) est confondu par la déflation de
  variance de la winsorisation (§8.73.4) : son comptage (10/11 à
  l'échelon b) est rapporté mais ne prouve pas que le bloc porte le
  pic ; le contrôle D1 (6/11 en winsorisant un autre bloc) le montre.
- Le swap confond le départ de B et l'arrivée de M à sa place : on
  ne peut pas départager les deux moitiés de l'intervention. Un
  contrôle par rotation/décalage pur des lignes (sans bloc
  désigné) départagerait — piste, non faite ici.
- H(c) est voisin du numérateur du |d| du scan : P2 mesure la
  localisabilité du déclencheur, pas une indépendance vis-à-vis du
  scan (protocole §7).
- 20 nuls frais donnent ~2–3 gagnantes rob-on attendues et ~9
  courbes rob-on attendues : P1/P2 peuvent manquer de puissance et
  rester descriptives (protocole §5, §7).
- Le lot §8.72 tourne en parallèle : les deux lots se partagent le
  CPU et durent plus longtemps ; chaque lot est reprenable et
  indépendant.
- Aucune donnée nouvelle hors des CSV déjà sur disque et des 20
  nuls frais ; aucun test direct ; aucun verdict biologique.

## 8.73.11 Provenance

- **Protocole gelé.** `PROTOCOL_pic_etroit_873.md` (SHA-256
  `28d2326c3ae83676d3e15f7283f0b37ae69a1791bcaa1f50c7b06ee368651a4c`),
  écrit avant tout nouveau script, toute nouvelle construction et
  tout nouveau run de ce chantier.
- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant le lot, avant la relance après redémarrage et après
  le lot : `f07567c4…ec3abf` à chaque fois). Scripts neufs :
  `pic_etroit_873.py` (SHA-256
  `33821df3d894a0e2a7eb4b882a546fe2f4f66fa21366c239b155aa26de24bba7`),
  `predict_pic_etroit_873.py` (SHA-256
  `473e4dddfa7559f1406b3a773c92f879b766b15b2e480dc0b344c5128cc63627`),
  `build_nulls_icgc_873.py` (SHA-256
  `3e0e222eedb9600c53a94daa97ae570614b9d6c3749852722cb098bf51cd2d2e`),
  `run_v62_873.sh` (SHA-256
  `3d9093efae9678fa2c66953d71c807904cc8d7382d9b3b6c9cc6ee1a84065768`),
  `watch_v62_873.sh` (SHA-256
  `5c38496482785eee4a28d826b6a6ff4d7ec5fa27cc268609ba712bdc0e5b6404`).
- **Entrées (SHA-256 vérifiés).** Série MTAP :
  `pdac_tcga_fluxes_v4_mtap.csv` et ses 13 nuls (§8.63.11, relus) ;
  flux immunitaires `pdac_immune_{tcga,geo62452,icgc}_fluxes.csv`
  (SHA dans PROVENANCE_immune_v6.md, re-vérifiés §8.53.6a ; ICGC
  réel `10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc`,
  re-vérifié avant construction des nuls s41–s60). Nuls ICGC frais
  s41–s60 : SHA dans `nulls_icgc_873_files.json` (s41
  `ac80ea4c3daf…`, s42 `3393ecd662e6…`, s43 `7bc0b6c79f22…`, s44
  `664300c0a761…`, s45 `6f7de0889c02…`, s46 `8827790ab7b6…`, s47
  `be67bf2ee612…`, s48 `d392f52668b5…`, s49 `0d7c337e1604…`, s50
  `b90fc3f97dc0…`, s51 `58cda104a89d…`, s52 `e8cc77c6ade9…`, s53
  `524b91f1996a…`, s54 `fbe7e6c34c76…`, s55 `61f6d571f41b…`, s56
  `22c48d622d52…`, s57 `ab4f10f6a591…`, s58 `9158bef95ccf…`, s59
  `07817ecf1408…`, s60 `1a2e17d00d57…`). Extract §8.63 relu :
  `mechanisms_863_extract.json` (SHA
  `2224df358546285afa1332d6ea09f28afd12742b2ce3a9e716adbea0d557c62e`).
- **Sorties.** `pic_etroit_873_extract.json` (SHA-256
  `4d0a52cba0ddb331760964c7ca91195b62e8e3022ae32f9eb638e733ec2ea767`),
  `pic_etroit_873_results.csv`
  (SHA `3a07fc97e36140b0…`), `pic_etroit_873_interv.csv` (SHA
  `4e7da4eb4a7ccdc0…`), `pic_etroit_873_predictions.json` (SHA
  `10c599f7c6d460bda9b294a553808abc9d81bd0776cc9633540c80b57779f2cd`),
  `nulls_icgc_873_files.json`, `manifest_v62_873.txt`,
  `runs_v62_873.log` (SHA `f7c41c1ec7f22adc90279a981f53117d4942dba8fa6fc6f44e834b7e9e1b3018`,
  20/20 exit 0), dossiers
  `results_fast_v62_873_icgc_nul_s41/` … `s60/`.
- **Faits de départ.** `section_8.63_mechanisms.md` (protocole
  `PROTOCOL_mechanisms_863.md` SHA `4e05dfc2…f35e`) — relus, jamais
  réimportés comme verdicts.
- **Nature des lignes.** Résidus d'expression TCGA (mesures
  instrumentales — séquençage ARN — transformées) ordonnés par CN
  MTAP ; flux immunitaires (ARN bulk) ; nuls = lignes permutées
  (échantillons hypothétiques, pas des mesures) ; CSV modifiés des
  interventions = constructions explicites (valeurs médianes ou
  blocs déplacés/copiés), étiquetés comme tels, jamais des mesures ;
  aucune autre donnée nouvelle dans ce chantier.
- **Ce qui manque, ce qui reste ouvert.** Le mécanisme fin de
  l'étroitesse (ce qui, dans l'arrangement exact, fait la largeur
  de 11–15 % plutôt que 40–70 %) ; le départage départ de B /
  arrivée de M dans le swap (contrôle par rotation pure) ;
  P1 non testable sur ce lot (0 courbe rob-on fraîche) et P2 en
  échec (23 faux positifs, 0 vrai positif) — un second lot frais
  avec des courbes rob-on serait nécessaire pour tester la
  position ; les modes autres que fast (12 configs) ; PDF non
  régénéré, rien poussé sur GitHub (hors de ce chantier).

— Fin de la §8.73. —
