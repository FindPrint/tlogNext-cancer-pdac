# PROTOCOLE GELÉ — Chantier 3 (suite) : élucider Delta par modélisation des magnitudes

Date : 19 novembre 2026.
Statut : **PROTOCOLE GELÉ AVANT TOUTE EXÉCUTION.** Aucune analyse lancée avant
l'écriture de ce fichier. Toute déviation arrête le travail et se consigne,
elle ne se corrige pas en silence.
Auteur : TagPrint.
Dossier : `~/workspace/runs/pdac-v6/`.
Demande : chantier 3 du projet PDAC v6.2 (19 nov. 2026), suite du §8.39.

## 0. Verdict d'abord — ce qui est gelé ici

Le §8.39 a clos la voie « variables structurelles » : meilleur score honnête
hold-out v6.1 → v6.2 = **87,9 % paires / 81,8 % valeurs** (H9e :
famille, masque, MFA, n), sous les 90 % exigés ; le résidu est intra-groupe
(§8.39.3 : dans le groupe LP / MFA 6,0 / n=178, n=62, trois paires
coexistent ; d_div s'étale de 4,62 à 5,46). Ce protocole teste la seule voie
restée ouverte au §8.39.10 point 1 : **prédire les magnitudes des
estimateurs elles-mêmes depuis les matrices de flux**, avant toute médiane,
puis en déduire la paire médiane et d_div par la construction connue.

## 1. Ce qui est acquis (rappels chiffrés, §8.39 et `PROTOCOL_v6.2.md` §4)

- Identités de construction vérifiées 222/222 (0 écart) : d_div = moyenne des
  3e et 4e médianes divergence triées (k=6) ; médiane seule si k=5 ;
  moyenne des 2e et 3e si k=4 ; d_sat = 4e médiane saturation triée.
- Structure des rangs (222 runs) : GraphDimension et PersistentHomology
  toujours les deux plus basses (222/222) ; LocalPCA toujours 3e ou 4e
  (222/222, 3e dans 212 cas) ; LevinaBickel jamais sous le rang 3.
  Donc d_div = (LocalPCA + X) / 2, où X = le plus petit de
  {MFA, LevinaBickel, PCAIntrinsic} dans 176/176 cas à k=6 avec LocalPCA 3e.
  La question se réduit à : **lequel des trois estimateurs hauts est le plus
  petit, et à quelle magnitude**.
- Paires non ordonnées observées : {LocalPCA, MFA} 129, {LocalPCA,
  PCAIntrinsic} 50, {LocalPCA, LevinaBickel} 31, {LocalPCA} 7, {MFA} 5.
  Base sans prédicteur (paire la plus fréquente) : 44,6 %.
- MFA quasi discret : 9 valeurs [3,0 ; 4,0 ; 4,5 ; 5,0 ; 6,0 ; 6,25 ; 6,5 ;
  6,75 ; 7,0]. Masques : LP 181, -P 12, -- 29.
- La permutation réel/nul ne change pas la paire (H10 = base, 44,6 %) :
  la paire est une propriété de l'échelle des estimateurs sur la série.
- Critère §4.4 repris tel quel : élucidé si (a) identité de la paire
  médiane prédite sur ≥ 90 % des runs ET (b) valeur de d_div à ±0,10 près
  sur ≥ 90 % des runs — mesurés ici en hold-out (voir §5), pas en
  échantillon.

## 2. Données

### 2.1 Cibles (sorties du pipeline, lecture seule)

- Base : `v62_delta_levels.csv` (222 runs : 156 v6.1 + 66 v6.2), dérivé des
  `master_results.json` par `extract_delta_levels.py`.
- Cibles : les 13 médianes par estimateur, parsées depuis les colonnes
  `div_sorted` / `sat_sorted` du CSV (arrondies à 4 décimales ; erreur
  d'arrondi ≤ 0,00005, négligeable devant la tolérance ±0,10) :
  divergence : LevinaBickel, PCAIntrinsic, LocalPCA, GraphDimension,
  PersistentHomology, MFA ; saturation : Higuchi, Katz, Petrosian, Sevcik,
  BoxCounting, Hurst2mH, DFA. Les valeurs `d_div`, `d_sat`, `pair`, `mask`
  du CSV sont les vérités terrain de l'évaluation.
- Vérification préalable (dans le script, avant modélisation) : d_div
  recalculé depuis les médianes parsées = d_div du CSV à 10⁻³ près sur
  222/222 ; sinon arrêt et diagnostic.

### 2.2 Prédicteurs (matrices de flux, lecture seule) — et rien d'autre

- Pour chaque run, la matrice d'entrée est lue via `metadata.csv_path`
  dans son `master_results.json` (inventaire préalable : 222 runs, 0 JSON
  manquant, 0 `csv_path` manquant, **156 matrices distinctes** — les
  répétitions rep2 et les paires v6.1/v6.2 partagent la même matrice).
- **INTERDIT comme prédicteur :** `df_feat.csv` (il contient les colonnes
  `<flux>_<estimateur>_mean` / `_std` dont la médiane par estimateur EST
  la cible — l'utiliser serait circulaire) ; tout champ de
  `master_results.json` autre que les cibles, n, contrôle et masque
  (voir §2.3) ; les noms des flux/gènes (mots humains, pas des mesures) ;
  l'étiquette réel/nul (ce n'est pas une mesure de la matrice — et §8.39
  H10 a montré qu'elle ne porte pas la paire) ; la famille/cohorte comme
  variable du modèle principal (elle a déjà été testée au §8.39, H9e ;
  le modèle flux doit se tenir seul).
- **AUTORISÉ :** uniquement des résumés numériques calculés sur la
  matrice CSV elle-même. Première colonne = contrôle (exclue des flux) ;
  autres colonnes = flux, dans l'ordre du contrôle (l'ordre compte :
  les estimateurs sont calculés le long de cet ordre).
- Vérification préalable : existence de chaque matrice distincte, SHA-256
  noté ; nombre de lignes = n du run ; sinon arrêt et diagnostic.

### 2.3 Variables structurelles connues (autorisées comme aux §8.39)

- Le **masque vrai** (LevinaBickel et/ou PersistentHomology finis) est
  autorisé pour appliquer la construction aux prédictions (comme H1–H15
  l'utilisaient comme variable de groupe). C'est une propriété structurelle
  observée du run, pas une magnitude. Une variante « masque ignoré »
  (tous les 6 membres prédits, k=6 forcé) est rapportée en sensibilité
  (§6.4) : si elle seule passait, le verdict le dirait.
- n (lignes) et p (nombre de flux) sont des propriétés de la matrice :
  autorisés comme prédicteurs.

## 3. Prédicteurs gelés — résumés de la matrice de flux

Pour chaque flux j (série x_j de n valeurs, dans l'ordre du contrôle) :

- 13 statistiques par flux : moyenne, écart-type (ddof=1), min, max,
  étendue, skewness (moment, Fisher), kurtosis excédentaire, autocorrélation
  lag-1 (Pearson x_t vs x_{t+1}), moyenne |Δ| (différences successives),
  écart-type des Δ, |dernier − premier| / écart-type (dérive), rho de
  Spearman vs indice de ligne (tendance le long de l'ordre du contrôle),
  r de Pearson vs indice de ligne.
- Agrégation sur les flux (chaque statistique résumée par moyenne,
  écart-type, min, max, médiane) : ensemble COMPLET = 13 × 5 = 65 traits ;
  ensemble RÉDUIT (primaire) = moyenne + écart-type seulement = 13 × 2 = 26.
- Traits inter-flux (7) : moyenne des |r| de Pearson par paires de flux,
  écart-type des r par paires, fraction des paires |r| > 0,8, part de
  variance PC1 et PC2 de la matrice de corrélation (valeurs propres /
  somme), part de variance PC1+PC2 (somme des deux), moyenne |chargement PC1|.
- *Correction du 19 nov. 2026, avant toute exécution : la première version de
  ce protocole comptait 7 traits inter-flux (total 41/80) mais n'en
  énumérait que 6 — le 7e, « part de variance PC1+PC2 », manquait dans
  l'énumération. Il est ajouté ici ; les totaux 41 (réduit) et 80 (complet)
  sont inchangés.*
- Traits du contrôle (4) : nombre de valeurs distinctes, étendue,
  écart-type, indicatrice « step » (contrôle = entiers consécutifs 0..n−1).
- Traits globaux (4) : n, p, n×p, log(n).
- Tailles : RÉDUIT = 26 + 7 + 4 + 4 = 41 traits ; COMPLET = 65 + 7 + 4 + 4
  = 80 traits. Standardisation par moyenne/écart-type du TRAIN seulement.
- Fait structurel consigné d'avance : les traits invariants par permutation
  des lignes (moyenne, écart-type, corrélations entre flux, PC) sont
  IDENTIQUES entre un réel et son nul permuté (mêmes valeurs, autre ordre) ;
  seuls les traits sensibles à l'ordre (autocorrélation lag-1, |Δ|,
  dérive, tendance vs indice) peuvent différer réel/nul. Le script le
  vérifie et le compte (paires réel/nul où les traits invariants sont
  égaux à 10⁻⁹ près).

## 4. Modèles gelés (numpy/scipy seulement — sklearn non installé)

- **M1 (primaire) :** régression ridge, λ = 10, traits RÉDUITS, un modèle
  par cible (13 modèles). Forme fermée, intercept non pénalisé.
- **M2 :** ridge λ = 10, traits COMPLETS (sensibilité à la richesse des
  traits).
- **M3 :** k plus proches voisins, k = 5, traits RÉDUITS standardisés,
  distance euclidienne, prédiction = moyenne simple des 5 voisins.
- **M4 :** par cible, le meilleur trait unique (|Pearson| sur le TRAIN),
  régression linéaire simple (OLS) sur ce trait.
- **B0 (base) :** constante = médiane du TRAIN par cible.
- MFA : prédiction rapportée brute ET « snapée » sur la plus proche des
  9 valeurs MFA observées au TRAIN (règle gelée, les deux taux rapportés).
- **Aucun autre modèle, aucun hyperparamètre ajusté sur le test.** La
  sensibilité λ ∈ {1, 100} pour M1 est rapportée en diagnostic, pas comme
  sélection de modèle.

## 5. Hold-out gelés — l'unité d'indépendance est la MATRICE, pas le run

Constat qui motive ce plan (inventaire, §2.2) : les 222 runs ne reposent
que sur 156 matrices distinctes ; un hold-out v6.1 → v6.2 partage les
mêmes matrices des deux côtés, avec des cibles Delta déterministes
identiques — il mesurerait de la mémorisation, pas de la généralisation.
Donc :

### 5.1 PRIMAIRE — leave-one-cohort-out (LOCO), groupé par matrice

- Cohorte d'une matrice, par règles gelées appliquées dans CET ordre à
  `csv_path` (premier motif qui correspond gagne) : `biophysique-hp35`
  → hp35 ; `geo62452` → geo62452 ; `geo71729` → geo71729 ; `icgc` →
  icgc ; `cptac` → cptac ; `depmap` → depmap ; `coad` → coad ; `luad`
  → luad ; `tcga` → tcga. (L'ordre place tcga en dernier attrape-tout :
  les rotations/parp/atr/immunitaires TCGA retombent dans tcga, les
  immunitaires GEO dans leur GEO.)
- 9 plis : entraîner sur 8 cohortes, tester sur la cohorte tenue à l'écart.
  Toutes les lignes (v6.1, v6.2, rep2) d'une même matrice restent du même
  côté. Scores POOLÉS sur les 222 runs, et par pli.
- **Critère (primaire) :** paires ≥ 90 % ET valeurs ±0,10 ≥ 90 % poolés.

### 5.2 SECONDAIRE A — split aléatoire par matrice (graine 42)

- 70 % des 156 matrices distinctes au TRAIN, 30 % au TEST (tirage
  stratifié par cohorte autant que possible, graine 42) ; toutes les lignes
  d'une matrice du même côté. Rapporté seulement (comparaison avec LOCO,
  et re-mesure de H9e sur ce split pour référence).

### 5.3 SECONDAIRE B — hold-out version v6.1 → v6.2 (DIAGNOSTIC, FUITE NOMMÉE)

- Majorités/modèles appris sur les 156 runs v6.1, testés sur les 66 runs
  v6.2. Les matrices se recouvrent : score attendu gonflé, rapporté avec
  la mention **FUITE — mêmes matrices des deux côtés, ne compte pas pour
  le critère**. Sert uniquement à quantifier la fuite (comparaison avec
  LOCO).

### 5.4 Critère de succès (écrit avant les résultats)

**ÉLUCIDÉ** si et seulement si AU MOINS UN des modèles gelés M1–M4 atteint
**à la fois** (a) paires ≥ 90 % ET (b) valeurs ±0,10 ≥ 90 % sur le LOCO
poolé (§5.1) **ET** les mêmes deux volets ≥ 90 % sur le split aléatoire
par matrice (§5.2). Sinon le verdict est **NON ÉLUCIDÉ**, avec les chiffres
de chaque modèle et de chaque hold-out. (Exiger les deux hold-outs évite
qu'un split chanceux fasse verdict.) La base B0 est rapportée partout.

## 6. Mesures gelées (toutes rapportées, en hold-out)

### 6.1 Dérivation des prédictions (construction, §1)

- Pour chaque run test : prédire les 6 médianes divergence ; retirer les
  membres masqués (masque vrai, §2.3) ; trier ; paire prédite et d_div
  prédit par la règle de parité (k=6 : moyenne 3e/4e ; k=5 : 3e seule ;
  k=4 : moyenne 2e/3e). Même règle côté saturation (7 membres, toujours
  complets) : d_sat prédit = 4e valeur triée prédite ; Delta prédit =
  d_div prédit − d_sat prédit.
- Paire : exactitude sur la paire NON ORDONNÉE (primaire, comme §8.39 :
  ordonné ≈ non ordonné) ; paire ordonnée en secondaire.
- Valeur : fraction des runs avec |d_div prédit − d_div vrai| ≤ 0,10.

### 6.2 Par cible (LOCO poolé, modèle M1 et meilleur modèle)

- R² (hold-out) et MAE pour chacune des 13 médianes ; corrélation de
  Pearson prédit/vrai. MFA : taux d'exactitude après snap (§4).

### 6.3 Le concours des trois hauts (k=6, LocalPCA 3e, n=176)

- Classification à 3 classes : lequel de {MFA, LevinaBickel, PCAIntrinsic}
  est le plus petit (vrai) vs prédit par le modèle. Exactitude vs hasard
  1/3 et vs majorité du TRAIN. Rapportée pour M1 et pour le meilleur modèle.

### 6.4 Résidu intra-groupe (la question posée)

- Dans les deux plus gros groupes structurels (LP, MFA 6,0, n=178) et
  (LP, MFA 7,0, n=178) : corrélation de Pearson (d_div prédit, d_div vrai)
  et écart-type résiduel, en LOCO. Même mesure poolée sur tous les groupes
  (masque, MFA, n) de taille ≥ 10 (corrélation intra-groupe).
- Variante « masque ignoré » (k=6 forcé) : paires/valeurs LOCO pour M1.
- Variante « d_sat seul » : MAE de d_sat prédit et fraction à ±0,10.

### 6.5 Contrôles d'honnêteté

- Traits invariants réel/nul : comptage des paires où ils sont égaux à
  10⁻⁹ près (§3) ; paires prédites identiques réel vs nul (fraction).
- En-échantillon (TRAIN sur tout, test sur tout) rapporté pour référence
  seulement, marqué SURAJUSTEMENT POSSIBLE, jamais comme verdict.
- Déduplication : les scores LOCO sont re-calculés sur les 153 runs
  distincts du §8.39.6 (sans rep2, sans `div_sorted` identiques) en
  sensibilité.

## 7. Ce que ce protocole ne fera pas

- Aucun run du pipeline, aucune modification d'un code (v6, v6.1, v6.2
  intacts — SHA vérifiés avant travail, voir §8).
- Aucun nouveau prédicteur ajouté après avoir vu les résultats ; la liste
  du §3 est gelée. Aucun modèle hors §4.
- Aucune sélection d'indicateur après coup ; aucune affirmation clinique.
- Aucun push GitHub, aucune régénération du PDF (hors de ce chantier).

## 8. Traçabilité et provenance

- Script unique de ce chantier : `v62_delta_magnitudes.py` (lecture seule
  des JSON/CSV, écritures : `v62_delta_magnitudes.log`,
  `v62_delta_magnitudes.json`, `v62_delta_magnitudes.md`,
  `v62_delta_magnitudes_flux_features.csv` — traits par matrice, avec
  SHA-256 de chaque matrice d'entrée).
- Pipeline : v6.2 `universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` ;
  v6.1 SHA-256
  `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ;
  v6 SHA-256 `bb8bbdba…c0773` (forme courte du dossier ; complet dans
  `PROVENANCE_v6.2.md`). **Aucun run du pipeline dans ce chantier.**
- Données : les 222 `master_results.json` (156 v6.1 + 66 v6.2) et les 156
  matrices de flux (TCGA, GEO, ICGC, CPTAC, DepMap, COAD, LUAD, HP35 —
  voir les `PROVENANCE_*.md` du dossier — et leurs nuls permutés,
  graine 42). Nature des lignes : sorties instrumentales du pipeline
  (médianes par estimateur) ; matrices de flux = mesures omiques
  publiques ; contrôles = noms de flux (étiquettes, mots humains).
- Consignation : verdict au livre blanc en §8.42 (avant le §8.5), ligne
  correspondante au §7, entrée de journal datée. PDF non régénéré.
- Ce qui manque (déclaré d'avance) : les valeurs brutes par flux ne sont
  pas les cibles — seules les médianes par estimateur figurent dans les
  JSON lus ; les traits du §3 sont des résumés, pas les séries complètes ;
  aucune famille entièrement nouvelle au-delà des 9 cohortes n'est testée
  (LOCO teste la généralisation à une cohorte tenue à l'écart, pas à une
  source inconnue).

— Fin du protocole gelé. —
