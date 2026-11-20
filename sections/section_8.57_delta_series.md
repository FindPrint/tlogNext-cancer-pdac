# §8.57 Modélisation depuis les séries complètes — chantier 3 (suite, 19 novembre 2026)

**Verdict d'abord : Delta reste NON ÉLUCIDÉ.** La voie ouverte au §8.42.9
point 1 — modéliser depuis les séries entières, pas des résumés — a été
testée avec un protocole gelé, sept modèles honnêtes et trois hold-outs :
aucun n'atteint le critère ≥ 90 % paires ET valeurs. Le meilleur,
**S2d (médiane calculée sur la moitié des flux seulement), manque le
critère de 2 runs en leave-one-cohort-out — 198/222 paires (89,2 %) et
201/222 valeurs (90,5 %) — et de 1 run en split aléatoire par matrice —
59/66 (89,4 %) aux deux volets.** La série complète, elle, recalcule la
cible exactement (diagnostic C0 : 2886/2886) : l'échec des modèles
honnêtes est un manque d'information, pas un manque de capacité. Delta
garde son statut de **piste fragile** et ne devient **pas** un
discriminateur recommandé.

## §8.57.1 Ce qui était acquis avant ce chantier

Le §8.39 avait clos la voie « variables structurelles » (meilleur hold-out
87,9 % / 81,8 %, H9e) et le §8.42 la voie « résumés de flux » (meilleur
score honnête LOCO : 68,9 % paires / 6,3 % valeurs ; split par matrice :
83,3 % / 42,4 %). Le §8.42 avait réduit la question à : lequel des trois
estimateurs hauts {MFA, LevinaBickel, PCAIntrinsic} est le plus petit,
une fois LocalPCA fixée en 3e position — et à quelle magnitude. Sa leçon
positive était nette : « les magnitudes des estimateurs sont des
fonctionnelles de la série ordonnée complète, pas de ses résumés — et leur
échelle est portée par n », avec l'avertissement joint : « un modèle qui
voudrait les prédire devrait partir des séries entières, et il devra
prouver qu'il ne se contente pas de recalculer l'estimateur » (§8.42.8).
Ce chantier est cette preuve : il nomme la circularité d'avance et ne
donne jamais à un modèle la série complète de sa cible.

## §8.57.2 Méthode du chantier

Protocole gelé `PROTOCOL_delta_series_857.md` avant toute modélisation
(SHA `965a88dc90c8af0ca701af2da1c31d124ceccef059d13a0972fae15ba6266bdc`) ;
script `v62_delta_series_857.py`
(SHA `59c1b78b4cdc0d2997660f9eb953a7b605b8575cc2c1ed2fd220d0a8dbb964f0`).
Lecture seule, aucun run du pipeline, aucun code modifié. Cibles : les 13
médianes par estimateur (6 divergence + 7 saturation), parsées depuis
`v62_delta_levels.csv` ; identités d_div / d_sat re-vérifiées depuis les
médianes parsées : 0 écart > 10⁻³ sur 222/222.

**La série d'estimateurs — ce qu'elle est.** Chaque run possède
`df_feat.csv` (120 lignes, Progress 0 → 100) dont les colonnes
`<flux>_<estimateur>_mean` portent, pour chaque flux et chaque estimateur,
la valeur de l'estimateur le long des positions de scan. Dans le pipeline,
la médiane brute d'un estimateur est la médiane-sur-flux des
médianes-sur-scan de sa colonne (NaN écartés). Vérification d'inventaire,
avant le gel, sur 12 runs × 13 estimateurs (156/156 à 10⁻⁶ près), puis
refaite sur tout l'ensemble par le script (diagnostic C0, §8.57.7) :
**2886/2886**. Disponibilité : `df_feat.csv` présent dans 222/222
dossiers, 120 lignes partout, 60 lignes Progress ≤ 50 partout ;
`fluxes_raw.csv` présent dans 222/222 ; p (nombre de flux) de 6 à 12.
Les 185 dossiers v62 postérieurs (§8.47, §8.53) sont hors de l'ensemble
gelé de 222 runs, pour garder la comparabilité avec §8.39/§8.42.

**La circularité — nommée, et traitée.** La cible `raw_median(e)` EST une
fonctionnelle déterministe de la série complète de e (médiane-de-médianes
sur les 120 lignes). Tout modèle nourri de la série complète de e peut
donc recalculer la cible exactement : ce serait une recomputation
déguisée, pas une élucidation. Le traitement gelé : un prédicteur honnête
n'utilise qu'une **partie stricte** de la série de la cible, ou aucune
information de cet estimateur, ou la série d'entrée brute :

- **S1d / S1r — PRÉFIXE :** seules les lignes de scan Progress ≤ 50
  (les 60 premières lignes). S1d est le prédicteur direct, sans
  apprentissage : la médiane-de-médianes du préfixe. S1r est un ridge
  λ = 10 sur 15 traits (médiane-de-médianes du préfixe de e, IQR
  inter-flux, médianes-de-médianes du préfixe des 12 autres estimateurs,
  log n).
- **S2d / S2r — DEMI-FLUX :** seuls les flux d'indice pair (0, 2, 4, …
  dans l'ordre des colonnes de `df_feat`), sur tout le scan. S2d est le
  prédicteur direct : la médiane-de-médianes sur la moitié des flux.
  S2r est le ridge λ = 10 analogue (15 traits).
- **S3r — TRANS-ESTIMATEUR PRÉFIXE :** ridge λ = 10 sur 13 traits —
  le préfixe des 12 AUTRES estimateurs et log n. Aucune information de
  l'estimateur cible.
- **S4r / S4k — SÉRIES DE FLUX ENTIÈRES :** la matrice de flux
  d'entrée seule, en pleine résolution : chaque série de flux
  rééchantillonnée à K = 20 positions par interpolation linéaire ; à
  chaque position, moyenne, écart-type, min, max, médiane inter-flux
  (100 traits), plus log n et p (102 traits). S4r est un ridge λ = 10,
  S4k un kNN k = 5. Aucune colonne d'estimateur n'entre.
- **B0 (base) :** constante = médiane du TRAIN par cible.
- **C0 (diagnostic circulaire, hors critère) :** recomputation directe
  de la médiane-de-médianes depuis la série complète (120 lignes, tous
  les flux). Étiqueté CIRCULAIRE, exclu de la candidature : il sert à
  prouver le plafond (100 %) et donc à montrer que l'échec des modèles
  honnêtes est un manque d'information, pas un manque de capacité.

Interprétation fixée d'avance : un succès de S1 ou S2 aurait signifié
« déjà déterminé » — la magnitude déjà fixée par la moitié de la
construction, une réduction, pas une explication causale du pourquoi de
la valeur. Un succès de S3 aurait signifié une redondance
inter-estimateurs. Seul un succès de S4 aurait compté comme explication
depuis un contenu indépendant (la série d'entrée brute, avant tout
estimateur). Traits manquants (préfixe ou demi-flux sans aucune valeur
finie alors que la cible existe) : imputés par la médiane du TRAIN de ce
trait ; pour les prédicteurs directs, repli sur la médiane du TRAIN de la
cible — un seul cas dans tout l'ensemble (voir §8.57.7). MFA : prédiction
rapportée brute ET snapée sur la plus proche des valeurs MFA observées
au TRAIN.

**L'unité d'indépendance est la matrice, pas le run.** Inventaire
préalable : les 222 runs ne reposent que sur **156 matrices distinctes**,
réparties en 9 cohortes (tcga 100 matrices / 126 runs, depmap 26/30,
geo71729 10/20, geo62452 6/14, cptac 4/8, icgc 4/10, coad 2/4, luad 2/4,
hp35 2/6) — identique au §8.42. Trois hold-outs gelés, repris du §8.42 :
**PRIMAIRE — leave-one-cohort-out (LOCO)**, 9 plis, toutes les lignes
d'une matrice du même côté, scores poolés sur 222 runs ; **SECONDAIRE A
— split aléatoire par matrice** (graine 42, 70/30 : 108 matrices / 156
runs au train, 48 / 66 au test) ; **SECONDAIRE B — version v6.1 → v6.2,
DIAGNOSTIC, FUITE NOMMÉE** (mêmes matrices, ne compte pas pour le
critère). Critère §5.4 : ÉLUCIDÉ si au moins un modèle honnête S1d, S1r,
S2d, S2r, S3r, S4r, S4k atteint paires ≥ 90 % ET valeurs ±0,10 ≥ 90 %
sur le LOCO poolé ET sur le split par matrice. Les prédictions sont
dérivées par la construction connue (paire = 3e/4e triées après application
du masque vrai ; d_div et d_sat recalculés depuis les médianes prédites ;
Delta = d_div − d_sat).

Les séries `csd_fractal_estimators.json` (trajectoires par fenêtres,
dérivées du même paysage `df_feat`) sont disponibles mais NON utilisées :
même information, même statut circulaire — les utiliser serait compter
deux fois la même série. `scan_curve.json` (score en fonction du
candidat) n'est pas une série d'estimateurs et n'est pas utilisée.

## §8.57.3 Résultats : aucun modèle, aucun hold-out ne passe — de peu pour S2d

| Hold-out | Modèle | Paires | Valeurs ±0,10 | MAE d_div | 3-voies |
|---|---|---|---|---|---|
| LOCO (222 runs) | B0 constante | 136/222 (61,3 %) | 0/222 (0,0 %) | 2,129 | 56,2 % (= majorité) |
| LOCO | **S1d préfixe direct** | 189/222 (85,1 %) | 188/222 (84,7 %) | 0,061 | 81,3 % |
| LOCO | S1r ridge préfixe | 119/222 (53,6 %) | 43/222 (19,4 %) | 0,304 | 55,7 % |
| LOCO | **S2d demi-flux direct** | **198/222 (89,2 %)** | **201/222 (90,5 %)** | **0,037** | **86,4 %** |
| LOCO | S2r ridge demi-flux | 116/222 (52,3 %) | 54/222 (24,3 %) | 0,434 | 55,1 % |
| LOCO | S3r ridge trans-estimateur | 113/222 (50,9 %) | 22/222 (9,9 %) | 2,403 | 52,8 % |
| LOCO | S4r ridge séries de flux | 139/222 (62,6 %) | 2/222 (0,9 %) | 1,027 | 55,7 % |
| LOCO | S4k kNN séries de flux | 138/222 (62,2 %) | 5/222 (2,3 %) | 1,373 | 58,0 % |
| Split matrices (66 runs) | B0 | 38/66 (57,6 %) | 16/66 (24,2 %) | 0,949 | 55,6 % |
| Split matrices | S1d | 60/66 (90,9 %) | 53/66 (80,3 %) | 0,074 | 88,9 % |
| Split matrices | **S2d** | **59/66 (89,4 %)** | **59/66 (89,4 %)** | **0,037** | **87,0 %** |
| Split matrices | S1r | 51/66 (77,3 %) | 40/66 (60,6 %) | 0,105 | 72,2 % |
| Split matrices | S2r | 48/66 (72,7 %) | 51/66 (77,3 %) | 0,084 | 66,7 % |
| Split matrices | S3r | 43/66 (65,2 %) | 23/66 (34,8 %) | 0,177 | 57,4 % |
| Split matrices | S4r | 42/66 (63,6 %) | 9/66 (13,6 %) | 0,512 | 59,3 % |
| Split matrices | S4k | 46/66 (69,7 %) | 23/66 (34,8 %) | 0,368 | 66,7 % |
| Version v6.1→v6.2 — FUITE (66 runs) | S1d | 57/66 (86,4 %) | 57/66 (86,4 %) | 0,055 | 83,3 % |
| Version v6.1→v6.2 — FUITE | S2d | 59/66 (89,4 %) | 61/66 (92,4 %) | 0,031 | 87,0 % |
| En-échantillon (222 runs) | S2d (= LOCO, sans apprentissage) | 198/222 (89,2 %) | 201/222 (90,5 %) | 0,037 | 86,4 % |
| En-échantillon | S1d (= LOCO, sans apprentissage) | 189/222 (85,1 %) | 188/222 (84,7 %) | 0,061 | 81,3 % |

Lecture :

- **Le critère est manqué de peu, et des deux côtés.** S2d passe le
  volet valeur en LOCO (201/222, 90,5 %) mais manque les paires de 2
  runs (198/222 au lieu des 200 requis) ; en split, il manque les deux
  volets de 1 run (59/66 au lieu de 60). S1d passe les paires en split
  (60/66, 90,9 %) mais échoue aux valeurs (53/66, 80,3 %) et aux deux
  volets en LOCO (85,1 % / 84,7 %). Aucun modèle ne remplit les deux
  volets sur les deux hold-outs.
- **Même avec la fuite, S2d ne passe pas.** En hold-out version
  (mêmes matrices des deux côtés), S2d fait 89,4 % / 92,4 % : les
  paires restent sous 90 % alors même que le test voit les matrices du
  train. L'échec n'est pas un artefact du hold-out : la médiane sur la
  moitié des flux ne détermine pas la paire à 90 %.
- **La médiane est plus stable d'un flux à l'autre que d'une moitié de
  scan à l'autre.** S2d (89,2 % / 90,5 % en LOCO) bat nettement S1d
  (85,1 % / 84,7 %) : la seconde moitié du scan déplace les médianes
  davantage que l'autre moitié des flux. d_sat, elle, est entièrement
  déterminée par la moitié des flux : S2d 222/222 (100 %) en LOCO et
  66/66 en split ; S1d aussi 222/222 et 66/66 en d_sat.
- **LOCO par pli (S2d, paire/valeur) :** coad 1,00/1,00 (n=4) ; cptac
  1,00/1,00 (n=8) ; depmap 1,00/0,97 (n=30) ; geo62452 1,00/1,00
  (n=14) ; geo71729 0,80/0,90 (n=20) ; hp35 1,00/1,00 (n=6) ; icgc
  1,00/1,00 (n=10) ; luad 1,00/1,00 (n=4) ; **tcga 0,84/0,86 (n=126
  — le pli dominant porte presque tout l'échec : 20 des 24 échecs de
  paire, 18 des 21 échecs de valeur)**. À l'inverse, S1d échoue aussi
  sur tcga (0,74/0,79) et vaut 0,00 en valeur sur luad (0/4) là où
  S2d fait 4/4.
- **Les modèles appris font pire que les fonctionnelles directes.**
  S1r (53,6 % / 19,4 %) et S2r (52,3 % / 24,3 %) sont loin derrière
  S1d et S2d en LOCO, alors qu'ils reçoivent strictement plus
  d'information (les mêmes médianes partielles, plus les autres
  estimateurs, plus log n). Les poids appris sur 8 cohortes explosent
  sur la 9e : R² LOCO jusqu'à −35 pour MFA (S1r), −388 pour Hurst2mH
  (S1r), −50 pour PCAIntrinsic (S2r). L'apprentissage linéaire dégrade
  l'information que la médiane partielle porte déjà — la fonctionnelle
  directe EST le modèle, et toute repondération apprise n'ajoute que de
  l'erreur inter-cohortes. En split (mêmes cohortes des deux côtés),
  les ridge remontent (S2r 72,7 % / 77,3 %), sans jamais approcher S2d.

## §8.57.4 Par cible : tout est presque déterminé, sauf LevinaBickel et PersistentHomology

R² hold-out (LOCO poolé) et MAE, meilleur modèle honnête S2d :

LevinaBickel 0,961 / 0,155 ; PCAIntrinsic 0,978 / 0,078 ; LocalPCA
0,998 / 0,025 ; GraphDimension 0,995 / 0,009 ; PersistentHomology
0,728 / 0,110 ; MFA 0,989 / 0,048 ; Higuchi 0,666 / 0,007 ; Katz
0,994 / 0,002 ; Petrosian 0,984 / 0,001 ; Sevcik 0,982 / 0,005 ;
BoxCounting 0,998 / 0,010 ; Hurst2mH 0,933 / 0,012 ; DFA 0,946 / 0,383.

Les deux cibles les plus faibles sont les deux estimateurs masqués
(PersistentHomology R² 0,728) et la cible de plus petite variance
(Higuchi R² 0,666 pour une MAE de 0,007 — le R² y est sévère pour de
petits écarts absolus). MFA exact (snapé sur les valeurs du train) en
LOCO : 91,0 % (202/222) pour S2d, 84,7 % (188/222) pour S1d ; brut :
90,5 % (201/222) et 82,4 % (183/222). Le concours des trois hauts
(k=6, LocalPCA 3e, n=176 ; majorité globale MFA, 56,2 %) : S2d 86,4 %
(152/176) en LOCO, 87,0 % (47/54) en split ; S1d 81,3 % / 88,9 %.

**Dérive préfixe / demi-flux — le plafond direct, par cible**
(fraction des runs avec |médiane partielle − médiane complète| ≤ 0,10 ;
écart moyen entre parenthèses) :

| Cible | Préfixe ≤ 0,10 | Demi-flux ≤ 0,10 |
|---|---|---|
| LevinaBickel | 27,1 % (0,231) | 46,4 % (0,155) |
| PCAIntrinsic | 68,5 % (0,086) | 72,5 % (0,078) |
| LocalPCA | 93,7 % (0,052) | 95,9 % (0,025) |
| GraphDimension | 100 % (0,011) | 100 % (0,009) |
| PersistentHomology | 72,0 % (0,078) | 56,8 % (0,105) |
| MFA | 82,4 % (0,095) | 90,5 % (0,048) |
| Higuchi | 100 % (0,011) | 100 % (0,007) |
| Katz | 100 % (0,003) | 100 % (0,002) |
| Petrosian | 100 % (0,001) | 100 % (0,001) |
| Sevcik | 100 % (0,006) | 100 % (0,005) |
| BoxCounting | 100 % (0,008) | 98,6 % (0,010) |
| Hurst2mH | 100 % (0,017) | 100 % (0,012) |
| DFA | 90,5 % (0,771) | 91,0 % (0,383) |

Dix cibles sur treize sont déjà déterminées à ±0,10 par la moitié des
flux sur plus de 90 % des runs — et la saturation presque partout à
100 %. Seules LevinaBickel (46,4 %) et PersistentHomology (56,8 %)
résistent, avec PCAIntrinsic (72,5 %) entre les deux. Côté préfixe, la
dérive est pire encore pour LevinaBickel (27,1 % seulement ≤ 0,10) :
sa valeur bouge le long du scan — la seconde moitié du scan la déplace
davantage que l'autre moitié des flux.

## §8.57.5 Pourquoi ça résiste : LevinaBickel au bord de la paire

Les 24 échecs de paire de S2d en LOCO se répartissent par vraie paire :
LocalPCA+LevinaBickel 13, LocalPCA+PCAIntrinsic 8, LocalPCA+MFA 3.
LevinaBickel figure dans la vraie paire ou dans la paire prédite sur
17/24. La dérive |demi-flux − complet| de LevinaBickel vaut en moyenne
0,190 (médiane 0,197) sur les runs en échec de paire, contre 0,150
(médiane 0,094) sur les réussites. Le mécanisme est le même que celui
du §8.39.3, vu de plus près : LevinaBickel est l'estimateur dont la
médiane par flux varie le plus d'un flux à l'autre, et c'est lui qui
occupe le plus souvent la 4e place — la place décisive. Quand il est
proche du seuil entre la 3e et la 4e valeur triée, la médiane sur la
moitié des flux le fait basculer, et la paire change ; quand il est
loin du seuil, la paire tient. La structure qui résiste n'est donc pas
un niveau — c'est le **basculement de LevinaBickel au bord de la
paire**, porté par la dispersion inter-flux de ses médianes par flux.

Les trois autres voies honnêtes échouent pour des raisons distinctes,
et il faut les nommer séparément :

- **S4 (séries de flux entières, seule voie à contenu indépendant) :**
  62,6 % / 0,9 % (ridge) et 62,2 % / 2,3 % (kNN) en LOCO — pas mieux
  que les résumés du §8.42 (68,9 % / 6,3 %). La pleine résolution
  n'ajoute rien : les magnitudes ne se lisent pas dans le contenu des
  séries de flux par ces modèles. En split, S4r monte à 63,6 % / 13,6 %
  et S4k à 69,7 % / 34,8 % — toujours loin du critère, et le kNN
  en-échantillon (82,0 % / 46,4 %) montre que même en mémorisant, il
  plafonne.
- **S3r (préfixe des 12 autres estimateurs) :** 50,9 % / 9,9 % en LOCO,
  65,2 % / 34,8 % en split. Il n'y a pas de redondance inter-estimateurs
  qui porte la magnitude de la cible : chaque estimateur tient sa
  valeur de sa propre série, pas de celles des autres.
- **S1r / S2r (ridge) :** l'apprentissage dégrade (voir §8.57.3). Ce
  n'est pas un manque de données d'entraînement : en-échantillon, S1r
  plafonne à 77,5 % / 63,5 % et S2r à 78,8 % / 76,1 %, quand les
  fonctionnelles directes font 85,1 % / 84,7 % et 89,2 % / 90,5 %
  sans aucun apprentissage.

## §8.57.6 Le résidu intra-groupe est capturé — mais la paire bascule quand même

C'est la nouveauté de ce chantier par rapport au §8.42.6. Le résidu
intra-groupe, déclaré imprévisible au §8.42 (r = +0,06 / +0,14 dans les
deux plus gros groupes, r poolée +0,09), est CAPTURÉ par S2d en LOCO :
groupe (LP, MFA 6,0, n=178), n=62 : r(prédit, vrai) = **0,977**,
écart-type résiduel 0,069 (d_div vrai 4,62–5,46) ; groupe (LP, MFA 7,0,
n=178), n=53 : r = **0,726**, résiduel 0,092 (d_div vrai 5,58–6,13) ;
corrélation intra-groupe poolée (groupes ≥ 10 runs, n=183) : r =
**0,937**. La moitié des flux suffit à retrouver le niveau de d_div
dans chaque groupe structurel — ce que les résumés du §8.42 ne faisaient
pas. Ce qui reste, ce n'est plus le niveau intra-groupe, c'est le
basculement de la paire sur les cas limites (§8.57.5) : 24 runs sur 222
où la paire prédite n'est pas la vraie, concentrés dans le pli tcga.
Le critère paire est donc manqué non par ignorance du niveau, mais par
l'instabilité de l'identité du 4e membre.

## §8.57.7 Contrôles d'honnêteté

- **C0 (diagnostic circulaire) :** recomputation de la
  médiane-de-médianes depuis la série complète : **2886/2886 à 10⁻⁶
  près** (222 runs × 13 cibles, contre `raw_median` des
  `master_results.json`). Le plafond est 100 % : un modèle nourri de la
  série complète atteint le critère trivialement — c'est pourquoi C0
  est exclu de la candidature. L'échec des modèles honnêtes est un
  manque d'information, pas un manque de capacité.
- **Paire prédite identique réel/nul (LOCO, S2d) :** 66/106 (62,3 %).
  C'est moins que §8.42 M1 (101/121, 83,5 %) et plus que la base H10
  (44,6 %) : la prédiction demi-flux est plus bruitée que la paire
  complète, donc elle diverge entre réel et nul plus souvent que la
  paire vraie, qui est insensible à la permutation (§8.39 H10). S2d
  n'hérite pas de l'invariance réel/nul de la paire complète.
- **Déduplication** (153 runs, §8.39.6), LOCO S2d : 137/153 (89,5 %) /
  137/153 (89,5 %) — stable, pas un artefact de duplication.
- **Variante masque ignoré** (k=6 forcé), LOCO S2d : 89,2 % / 90,5 % —
  inchangée : le masque n'est pas le blocage.
- **Sensibilité λ** (S1r, LOCO) : λ=1 → 58,1 % / 47,3 % ; λ=100 →
  51,8 % / 7,2 %. Aucun λ ne sauve le modèle.
- **Un seul cas de repli gelé.** PersistentHomology sur
  `results_fast_v61_depmaprot_aco2` : un seul flux fini (n_fluxes_used
  = 1), d'indice impair — la médiane demi-flux est donc indéfinie
  alors que la cible existe (0,5975). La règle gelée (repli sur la
  médiane du TRAIN) s'applique une seule fois dans tout l'ensemble, et
  ce run est un succès de paire grâce à elle : sans ce repli, S2d LOCO
  serait à 197/222 (88,7 %) en paires. Le préfixe, lui, ne déclenche
  aucun repli (0 cas).
- Les 156 matrices ont été lues avec SHA-256 noté (traits de série
  dans `v62_delta_series_857_features.csv`) ; 0 écart entre n matrice
  et n run ; 70 cibles manquantes, toutes LevinaBickel (41) ou
  PersistentHomology (29), c'est-à-dire le masque — aucune autre.

## §8.57.8 Conséquence : Delta reste une piste fragile

Quatre voies ont maintenant échoué à élucider Delta au critère ≥ 90 % :
les variables structurelles (§8.39 : 87,9 % / 81,8 %), les rangs
eux-mêmes (§8.39.5 : même en connaissant le rang, la valeur plafonne à
80,3 %), les résumés de flux (§8.42 : 68,9 % / 6,3 % en LOCO), et
maintenant les séries entières (ce chantier : 89,2 % / 90,5 % en LOCO
pour le meilleur modèle honnête, 89,4 % / 89,4 % en split). Le 6/8 de
Delta en phase 2 reste une piste fragile (échec sur HP35, deux écarts
≤ 0,15, 13/23 en annexe) et Delta ne devient pas un discriminateur
recommandé. La leçon positive est nette, et elle déplace la question :
**la moitié des flux suffit presque à déterminer Delta** — la médiane
est déjà écrite à ~90 % dans la moitié de sa propre construction, le
niveau intra-groupe est capturé (r = 0,937), d_sat l'est entièrement
(222/222) — **mais l'identité du 4e membre, LevinaBickel le plus
souvent, bascule sur les cas limites, et rien dans les séries d'entrée
ne la prédit** (S4 : 62,6 % / 0,9 %). Delta n'est pas expliqué par les
séries : il est presque recalculé par elles, sans l'être tout à fait.
La différence entre 89,2 % et 90 % n'est pas un bruit d'échantillonnage
à combler en ajoutant des runs du même plan : elle est portée par la
dispersion inter-flux de LevinaBickel dans le pli tcga, structure
déjà visible sur 126 runs.

## §8.57.9 Ce qui reste ouvert

1. **La loi d'échelle en n, analytiquement.** Pourquoi chaque estimateur
   croît ou décroît avec n, et avec quelle forme (log ? puissance ?) —
   à établir estimateur par estimateur, y compris pour DFA et ses
   extrêmes (−38,16). Les séries n'ont pas répondu ; la question reste
   analytique, pas un modèle de plus.
2. **La dispersion inter-flux de LevinaBickel.** Pourquoi ses médianes
   par flux s'étalent-elles davantage que celles des autres estimateurs,
   et que se passe-t-il sur les flux qui la font basculer ? Une lecture
   par flux (quels flux portent la médiane, lesquels la déplacent),
   pas un nouveau modèle global.
3. **d_sat.** Entièrement déterminée par la moitié des flux (222/222)
   : son élucidation est acquise au sens de ce chantier — la question
   se déplace vers pourquoi la saturation est si stable entre flux,
   quand la divergence ne l'est pas.
4. **Généralisation à une source nouvelle.** LOCO teste une cohorte
   tenue à l'écart, pas une source inconnue (nouvel omique, nouvel
   organisme) — les scores s'y dégraderaient probablement encore, et
   le pli tcga montre déjà que la portabilité n'est pas acquise
   intra-cohorte.

## Provenance (§8.57)

- **Demande et go :** chantier §8.57 du projet PDAC v6.2, 19 novembre
  2026 (suite du §8.42, voie ouverte au §8.42.9 point 1). Protocole
  gelé avant toute modélisation : `PROTOCOL_delta_series_857.md`,
  SHA-256
  `965a88dc90c8af0ca701af2da1c31d124ceccef059d13a0972fae15ba6266bdc`.
- **Pipeline :** v6.2 `universal_v6.2.0_cohen.py`,
  SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant travail, jamais modifié) ; v6.1
  `universal_v6.1.0_cohen.py`,
  SHA-256 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ;
  v6 SHA-256
  `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`.
  **Aucun run du pipeline dans ce chantier.**
- **Données lues (lecture seule) :** 222 `master_results.json`
  (156 `results_fast_v61_*`, 66 `results_fast_v62_*`) dans
  `~/workspace/runs/pdac-v6/` ; les 222 `df_feat.csv` (séries
  d'estimateurs, 120 lignes de scan par run) ; les 156 matrices de flux
  d'entrée (`metadata.csv_path` : TCGA, GEO, ICGC, CPTAC, DepMap, COAD,
  LUAD, HP35 — voir les `PROVENANCE_*.md` du dossier — et leurs nuls
  permutés, graine 42). Nature des lignes : sorties instrumentales du
  pipeline (médianes par estimateur) ; séries d'estimateurs = valeurs
  de l'estimateur le long du scan, par flux ; matrices de flux =
  mesures omiques publiques ; contrôles = noms de flux (étiquettes,
  mots humains).
- **Script et sorties :** `v62_delta_series_857.py` (SHA-256
  `59c1b78b4cdc0d2997660f9eb953a7b605b8575cc2c1ed2fd220d0a8dbb964f0`),
  `v62_delta_series_857.log` (SHA-256
  `7916fdd320c035a33d2f0393575b836de56ebcbfed39171646befb4d60ee8ed8`),
  `v62_delta_series_857.json` (SHA-256
  `c41e13103b802c41498f8993e42d2b086bdefd2773b97b5180d05185311db931`),
  `v62_delta_series_857.md` (résumé d'exécution),
  `v62_delta_series_857_features.csv` (SHA-256
  `5e515fd253269ee0a545f9f1bbe9eaa2f234ca8b3bb8f7aa2ef2e2d9cca74c4e` :
  médianes préfixe / demi-flux / complètes par cible et par run, SHA
  de chaque `df_feat.csv` et de chaque matrice d'entrée).
- **Vérifications préalables :** C0 2886/2886 à 10⁻⁶ près ; identités
  d_div / d_sat 0 écart > 10⁻³ sur 222/222 ; 60 lignes Progress ≤ 50
  dans chaque `df_feat.csv` ; 0 écart n matrice vs n run ; 70 cibles
  manquantes (LevinaBickel 41, PersistentHomology 29) — le masque.
- **Limites déclarées :** les séries `df_feat` ne sont pas les séries
  de flux brutes (ce sont des valeurs d'estimateurs le long du scan) ;
  les traits S1–S3 sont des médianes de parties de séries, pas les
  séries point par point ; les 185 dossiers v62 postérieurs (§8.47,
  §8.53) ne sont pas dans l'ensemble gelé de 222 runs ; aucune famille
  entièrement nouvelle au-delà des 9 cohortes n'est testée ; les
  trajectoires `csd_fractal_estimators.json` n'ont pas été utilisées
  (dérivées du même paysage `df_feat`).
- Section rédigée dans `section_8.57_delta_series.md` (ce fichier) ;
  le livre blanc et le PDF ne sont pas régénérés dans ce chantier
  (coordinateur) ; rien n'est poussé sur GitHub dans ce chantier.

— Fin de la §8.57. —
