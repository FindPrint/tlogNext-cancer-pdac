# Paysage immunitaire le long de l'axe KRAS — Bras 1 (v6)

Date : 16 novembre 2026. Protocole gelé avant les runs ; provenance complète
dans `PROVENANCE_immune_v6.md`. Pipeline v6, SHA vérifié
`bb8bbdba…c0773`, mode fast, cohen_d partout. 8 runs v6, tous exit 0.

## Verdict d'abord

**Oui, le paysage immunitaire change le long de l'axe KRAS — et il va dans
le sens « tumeur froide », pas « tumeur à cibler par anti-PD-(L)1 ».**

En une phrase : plus KRAS est fort, moins il y a de signal des lymphocytes
T (les cellules qui tuent la tumeur), dans les 4 cohortes ; en revanche
PD-L1, la cible des immunothérapies anti-PD-(L)1, ne monte pas de façon
fiable avec KRAS. Donc **la combinaison KRAS + anti-PD-(L)1 n'est PAS une
piste soutenue par ces données** : la cible n'est pas plus haute là où
KRAS est fort, et les cellules qui devraient faire le travail sont moins
nombreuses. Ce qui reste une piste, c'est de comprendre pourquoi les T
disparaissent quand KRAS monte — avant de parler de combinaison.

Le pipeline v6, lui, ne sépare pas proprement réel et nul sur ces flux :
la cascade ne porte pas le verdict ici. Ce sont les tests directs
(Spearman + top-12 contre reste) qui le portent, comme le protocole
l'exigeait.

## 1. Tests directs (verdict principal)

Ordre = KRAS brut croissant partout. Top-12 = les 12 patients KRAS-les-
plus-forts contre le reste. 48 tests (12 gènes × 4 cohortes), p brutes ;
~2,4 faux positifs attendus à p < 0,05 sous le nul — on en observe 16,
mais c'est la cohérence du signe entre cohortes qui compte, pas une p
isolée. Détail complet : `immune_direct_tests.csv` / `.txt`.

### 1.1 Les lymphocytes T baissent quand KRAS monte — 4 cohortes sur 4

| Gène (rôle) | rho Spearman vs KRAS par cohorte (TCGA / GSE71729 / GSE62452 / ICGC) | d top-12 (TCGA / GSE71729 / GSE62452 / ICGC) |
|---|---|---|
| CD8A (T tueurs) | −0,19* / −0,16 / −0,35* / −0,15 | −0,45 / −0,82* / −0,93* / −0,45 |
| CD8B (T tueurs) | −0,22* / −0,18* / −0,40* / +0,04 | −0,50 / −0,50 / −1,09* / +0,02 |
| CD4 (T auxiliaires) | −0,15* / −0,30* / −0,15 / −0,16 | −0,49 / −0,28 / −0,33 / −0,43 |
| PDCD1 (PD-1, T) | −0,25* / −0,24* / −0,22 / −0,22 | −0,61* / −0,88* / −0,70* / −0,85* |
| FOXP3 (T régulateurs) | −0,10 / −0,09 / −0,34* / −0,20 | −0,29 / +0,30 / −0,93* / −0,70* |
| CD19 (lymphocytes B) | −0,18* / −0,09 / −0,42* / (MS4A1 −0,05) | −0,59* / −0,52* / −0,76 / (MS4A1 −0,26) |

\* p < 0,05 (brute). n : TCGA 178, GSE71729 145, GSE62452 69, ICGC 70.

- **Signe constant sur les 4 cohortes** : CD8A, CD4, FOXP3, PDCD1 (tous
  négatifs) — et CD68 (positif, voir §1.3). CD8B négatif dans 3/4 (ICGC
  plat, +0,04). CD19 négatif dans les 3 cohortes où il est mesuré ; en
  ICGC son remplaçant MS4A1 (CD20) est aussi négatif (−0,05).
- PDCD1 est le signal le plus régulier : rho entre −0,22 et −0,25 dans
  les 4 cohortes, et d top-12 entre −0,61 et −0,88, significatif (p Welch
  < 0,05) dans les 4 cohortes. Mais attention à l'interprétation (§3) :
  PD-1 baisse parce que les T sont moins nombreux, pas parce que chaque
  T exprime moins de PD-1 — l'ARN en vrac ne distingue pas les deux.
- FOXP3 baisse aussi : ce n'est donc pas un tableau « plus de T
  régulateurs qui étouffent la réponse », c'est une baisse globale du
  signal T — y compris régulateur.
- GZMB et IFNG (armes des T tueurs) : pas de direction cohérente
  (GZMB −0,11 / +0,14 / +0,06 / −0,04 ; IFNG −0,04 / +0,09 / −0,09 /
  PRF1 −0,04 en ICGC). Les effecteurs ne montent pas quand KRAS monte ;
  ils ne baissent pas non plus proprement. Le signal le plus net est la
  quantité de T (CD8A/CD8B/CD4), pas leur activité par cellule.

### 1.2 PD-L1 (CD274) ne monte pas de façon fiable avec KRAS

| Cohorte | rho CD274 vs KRAS | p | d top-12 | p Welch |
|---|---|---|---|---|
| TCGA (n=178) | +0,26 | 0,0006 | +0,52 | 0,15 |
| GSE71729 (n=145) | −0,11 | 0,21 | −0,13 | 0,63 |
| GSE62452 (n=69) | +0,18 | 0,13 | +0,34 | 0,34 |
| ICGC (n=70) | +0,18 | 0,14 | −0,03 | 0,94 |

Positif dans 3 cohortes sur 4, mais significatif dans une seule (TCGA),
et le top-12 n'est significatif nulle part. Il n'y a pas de phénotype
« KRAS-fort = PD-L1-haut » robuste. La hausse TCGA isolée ne survit pas
aux 3 autres cohortes — c'est exactement le genre de signal
mono-cohorte que le protocole à 4 cohortes est fait pour écarter.

### 1.3 Macrophages : stables, peut-être en légère hausse

- CD68 (macrophages) : rho positif dans les 4 cohortes (+0,07 / +0,22* /
  +0,17 / +0,18), significatif seulement en GSE71729. Direction
  cohérente mais effet faible — à lire comme « les macrophages ne
  baissent pas avec KRAS, contrairement aux T », pas comme une hausse
  démontrée.
- CD163 (macrophages M2) : aucune direction (−0,03 / +0,11 / −0,13 /
  −0,05). Rien.

## 2. Runs v6 (cascade, MC, L7a, Delta)

Cible v6 = CD8A partout (première colonne numérique hors contrôles —
comportement standard du mode single, identique aux bras précédents).
Sorties : `results_fast_immune_<cohorte>(_nul)/`, extraction
`immune_v6_runs_summary.json` (script `extract_immune_v6.py`).

| Run | n | T_-2 | T_-1 | T_0 | T_+1 | T_+2 | MC | Delta | L7a |
|---|---|---|---|---|---|---|---|---|---|
| TCGA réel | 178 | 1,60 | 29,15 | 59,91 | 75,10 | 75,10 | 0,379 | 4,21 | DOWN 18 % (désaccord) |
| TCGA nul | 178 | 0,00 | 2,13 | 8,52 | 35,34 | 35,34 | 0,324 | 2,30 | UP 34 % |
| GSE71729 réel | 145 | 0,00 | 33,38 | 92,27 | 95,49 | 99,36 | 0,344 | 2,86 | DOWN 39 % |
| GSE71729 nul | 145 | 2,61 | 21,10 | 38,82 | 86,48 | 86,48 | 0,324 | 2,67 | UP 17 % (désaccord) |
| GSE62452 réel | 69 | 7,12 | 62,58 | 66,59 | 91,29 | 92,74 | 0,369 | 1,37 | UP 50 % = repli NaN |
| GSE62452 nul | 69 | 0,00 | 1,27 | 4,27 | 8,55 | 46,38 | 0,348 | 1,41 | UP 50 % = repli NaN |
| ICGC réel | 70 | 4,22 | 25,30 | 29,52 | 33,76 | 52,31 | 0,334 | 1,50 | UP 50 % = repli NaN |
| ICGC nul | 70 | 0,00 | 19,68 | 23,90 | 63,02 | 72,80 | 0,368 | 1,32 | UP 50 % = repli NaN |

Lecture, réel contre nul :

- **MC optimum** : réel au-dessus du nul de justesse en TCGA (0,379 vs
  0,324), GSE71729 (0,344 vs 0,324) et GSE62452 (0,369 vs 0,348) — mais
  **en dessous du nul en ICGC (0,334 vs 0,368)**. Aucune séparation
  propre : 3/4 dans le bon sens, de justesse, 1/4 inversé.
- **Delta** : seul TCGA montre un écart net (4,21 vs 2,30). GSE71729
  2,86 vs 2,67 (rien), GSE62452 1,37 vs 1,41 (nul au-dessus), ICGC 1,50
  vs 1,32 (rien). Aucune séparation propre.
- **T_0** : réel et nul tombent à des endroits différents partout, mais
  le nul produit lui aussi des cascades complètes avec des T_0 nets
  (8,52 % / 38,82 % / 4,27 % / 23,90 %) — une cascade n'est pas une
  preuve en soi, le nul en fabrique aussi.
- **L7a** : TCGA DOWN 18 % avec désaccord cible/régime, GSE71729 DOWN
  39 % — votes faibles, non concluants. GSE62452 et ICGC : UP 50,00 %
  dans le réel ET dans le nul — c'est le repli connu : le diagnostic de
  bruit exige 5 bins × 15 points (≥ 75), à n = 69/70 le score est NaN
  (`noise_diagnostic.json` : `status = scores_unavailable`,
  `n_complete_scores = 0`). Ce « UP 50 % » n'est pas un vote. À
  n = 145/178 le diagnostic est complet (12 scores), et L7a y reste un
  vote interne faible, jamais une preuve.
- **Conclusion v6** : pas de séparation réel/nul sur les flux immunitaires.
  La cascade seule ne dit rien ici. Le verdict vient des tests directs
  (§1), qui eux sont cohérents entre cohortes. C'est un résultat négatif
  pour l'instrument sur ces flux, et un résultat positif pour les tests
  directs — les deux sont consignés.

## 3. Ce que ça veut dire pour KRAS + immunothérapie

- **Anti-PD-(L)1 en combinaison : NON, pas soutenu.** Deux raisons
  mesurées : (1) PD-L1 ne monte pas de façon fiable avec KRAS (§1.2) ;
  (2) les lymphocytes T — les cellules que l'anti-PD-(L)1 doit
  « débloquer » — sont moins présents quand KRAS est fort (§1.1).
  Débloquer des T absents ne fait rien. Les essais anti-PD-1/PD-L1 dans
  le PDAC ont d'ailleurs été décevants en monothérapie ; ces données
  disent que le sous-groupe KRAS-fort n'est pas celui où il faudrait
  les attendre.
- **« Tumeur froide » : OUI, c'est la lecture.** Le gradient KRAS-fort
  → moins de T est cohérent dans 4 cohortes indépendantes, 3
  plateformes, 2 continents. La question qui suit n'est pas « quel
  checkpoint ajouter » mais « pourquoi les T n'entrent pas / ne
  restent pas quand KRAS est fort ».
- **Macrophages : piste faible, à ne pas sur-vendre.** CD68 ne baisse
  pas et tend à monter (§1.3) pendant que les T baissent. Si quelque
  chose remplit l'espace laissé par les T, ce sont plutôt les
  macrophages que les T régulateurs (FOXP3 baisse). Mais l'effet est
  faible (un seul p < 0,05 sur 4) : une hypothèse à tester, pas une
  cible.
- **Limite majeure, à ne pas oublier** : ARN en vrac, sans correction de
  pureté (choix documenté, pour être comparable entre cohortes). Une
  baisse de CD8A peut vouloir dire « moins de T dans le morceau de
  tumeur » ou « plus de cellules tumorales qui diluent le signal » —
  ou les deux. La direction est robuste, le mécanisme ne l'est pas.
  La suite logique serait une déconvolution (estimation des fractions
  cellulaires) ou de l'IHC, pas une autre cascade.

## 4. Fichiers livrés (`~/workspace/runs/pdac-v6/`)

- `build_fluxes_immune.py` — construction des 4 CSV de flux (+ nuls, + axes KRAS).
- `pdac_immune_{tcga,geo71729,geo62452,icgc}_fluxes.csv` et `..._nul.csv`
  — SHA dans `PROVENANCE_immune_v6.md` §4.
- `immune_kras_order_{tcga,geo71729,geo62452,icgc}.csv` — axe KRAS brut.
- `immune_build_summary.json`, `immune_build.log`.
- `direct_tests_immune.py`, `immune_direct_tests.csv`, `immune_direct_tests.txt`.
- `run_immune_v6.sh`, `runs_immune_v6.log` (8 runs, exit 0 partout).
- `results_fast_immune_{tcga,geo71729,geo62452,icgc}(_nul)/` — sorties v6.
- `extract_immune_v6.py`, `immune_v6_runs_summary.json`.
- `PROVENANCE_immune_v6.md`, `immune_v6.md` (ce rapport).
