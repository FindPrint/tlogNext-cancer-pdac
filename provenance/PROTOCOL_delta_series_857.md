# PROTOCOLE GELÉ — §8.57 : élucider Delta à partir des séries complètes

Date : 19 novembre 2026.
Statut : **PROTOCOLE GELÉ AVANT TOUTE MODÉLISATION.** Aucun modèle lancé avant
l'écriture de ce fichier. Toute déviation arrête le travail et se consigne,
elle ne se corrige pas en silence.
Auteur : TagPrint.
Dossier : `~/workspace/runs/pdac-v6/`.
Demande : chantier §8.57 du projet PDAC v6.2 (19 nov. 2026), suite du §8.42.

## 0. Verdict d'abord — ce qui est gelé ici

Le §8.42 a clos la voie « résumés de flux » : meilleur score honnête
leave-one-cohort-out = **68,9 % paires / 6,3 % valeurs** (M2/M3), et sa
leçon positive : « les magnitudes des estimateurs sont des fonctionnelles
de la série ordonnée complète, pas de ses résumés — et leur échelle est
portée par n ». Ce protocole teste la seule voie restée ouverte au
§8.42.9 point 1 : **modéliser depuis les séries entières** — et il le fait
en nommant d'avance le piège qui l'accompagne : **un modèle trop proche de
l'estimateur le recalcule, il ne l'explique pas** (§8.42.8).

## 1. Ce qui est acquis (rappels chiffrés, §8.39 et §8.42)

- Identités de construction vérifiées 222/222 (0 écart) : d_div = moyenne
  des 3e et 4e médianes divergence triées (k=6) ; médiane seule si k=5 ;
  moyenne des 2e et 3e si k=4 ; d_sat = 4e médiane saturation triée.
- Structure des rangs (222 runs) : GraphDimension et PersistentHomology
  toujours les deux plus basses (222/222) ; LocalPCA toujours 3e ou 4e
  (222/222, 3e dans 212 cas). La question se réduit à : lequel des trois
  estimateurs hauts {MFA, LevinaBickel, PCAIntrinsic} est le plus petit,
  et à quelle magnitude.
- Paires non ordonnées observées : {LocalPCA, MFA} 129, {LocalPCA,
  PCAIntrinsic} 50, {LocalPCA, LevinaBickel} 31, {LocalPCA} 7, {MFA} 5.
  Base sans prédicteur (paire la plus fréquente) : 44,6 %.
- MFA quasi discret : 9 valeurs [3,0 ; 4,0 ; 4,5 ; 5,0 ; 6,0 ; 6,25 ; 6,5 ;
  6,75 ; 7,0]. Masques : LP 181, -P 12, -- 29.
- Critère repris tel quel (§8.39 §4.4, §8.42 §5.4) : élucidé si (a) identité
  de la paire médiane prédite sur ≥ 90 % des runs ET (b) valeur de d_div
  à ±0,10 près sur ≥ 90 % des runs — mesurés ici en hold-out (voir §5),
  pas en échantillon.

## 2. Données et séries — inventaire préalable (fait avant le gel)

### 2.1 Ensemble (identique aux §8.39/§8.42, pour comparabilité)

- Base : `v62_delta_levels.csv` (222 runs : 156 v6.1 + 66 v6.2).
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

### 2.2 La série d'estimateurs — ce qu'elle est vraiment

Chaque run possède `df_feat.csv` (120 lignes, Progress 0 → 100) dont les
colonnes `<flux>_<estimateur>_mean` portent, pour chaque flux et chaque
estimateur, la valeur de l'estimateur le long des positions de scan.
Dans le pipeline (`universal_v6.2.0_cohen.py`, fonction de tension
holographique), la médiane brute d'un estimateur est :

> `raw_median(e) = médiane sur les flux f de ( médiane sur les 120 lignes
> de scan de <f>_<e>_mean )`, NaN écartés.

**Vérification d'inventaire (avant gel, 12 runs × 13 estimateurs = 156
contrôles) : la recomputation depuis `df_feat.csv` égale `raw_median`
du `master_results.json` à 10⁻⁶ près sur 156/156.** Le script la refait
sur les 222 runs × 13 cibles avant toute modélisation (diagnostic C0,
§4.1) ; tout écart > 10⁻⁶ arrête le travail.

Disponibilité : `df_feat.csv` présent dans 222/222 dossiers de run,
120 lignes partout ; `fluxes_raw.csv` présent dans 222/222 ; p (nombre de
flux) : 12 sur 283 dossiers v61+v62 au total, 11 sur 104, 7 sur 10,
6 sur 4, 10 sur 4, 9 sur 2 (compté sur 407 dossiers ; la répartition sur
les 222 est rapportée par le script). Les 185 dossiers v62 supplémentaires
(§8.47, §8.53 : `results_fast_v62_847_*`, `results_fast_v62_853_*`, …)
sont HORS de l'ensemble gelé de 222 runs : ils ne sont pas ajoutés ici,
pour garder la comparabilité avec §8.39/§8.42 (c'est une limite déclarée,
§7).

### 2.3 Autres séries existantes — statut

- `csd_fractal_estimators.json` : trajectoires par fenêtres (variance /
  AR1 / skewness, fenêtres de 40 sur 120 positions) pour chaque couple
  (flux, estimateur). **Disponible, NON utilisée** : elle est dérivée du
  même paysage `df_feat` — même information, même statut circulaire ;
  l'utiliser serait compter deux fois la même série.
- `scan_curve.json` : série score-en-fonction-du-candidat du balayage de
  seuil. **Non utilisée** : ce n'est pas une série d'estimateurs, et elle
  ne porte pas les médianes.
- `fluxes_raw.csv` (série de flux d'entrée, n × p, première colonne =
  contrôle) et la matrice d'entrée (`metadata.csv_path`) : utilisées pour
  le modèle S4 seulement (§3.4).

## 3. La circularité — nommée explicitement, et traitée

### 3.1 Le piège

La cible `raw_median(e)` EST une fonctionnelle déterministe de la série
complète de l'estimateur e (médiane-de-médianes sur les 120 lignes).
**Tout modèle nourri de la série complète de e peut donc recalculer la
cible exactement.** Ce ne serait pas une élucidation, ce serait une
recomputation déguisée. Le §8.39.5 l'a déjà montré sous une autre forme :
même en connaissant le rang (donc les 6 valeurs elles-mêmes), la valeur
plafonne à 70,3 % / 80,3 % — seule l'identité de construction (la moyenne
des deux valeurs médianes elles-mêmes) atteint 100 %.

### 3.2 Le traitement gelé : ne jamais donner la série complète de la cible

Un prédicteur honnête n'utilise qu'une **PARTIE STRICTE** de la série
de l'estimateur cible, ou aucune information de cet estimateur, ou la
série d'entrée brute (qui ne contient aucun estimateur calculé) :

- **S1 PRÉFIXE** (§3.1) : seules les lignes de scan Progress ≤ 50
  (les 60 premières lignes). La cible utilise les 120 lignes : la
  seconde moitié est strictement exclue.
- **S2 DEMI-FLUX** (§3.2) : seuls les flux d'indice pair (0, 2, 4, …
  dans l'ordre des colonnes de `df_feat` pour cet estimateur), sur tout
  le scan. La cible utilise tous les flux : la moitié impaire est
  strictement exclue.
- **S3 TRANS-ESTIMATEUR PRÉFIXE** (§3.3) : aucune information de
  l'estimateur cible — seulement le préfixe (Progress ≤ 50) des 12
  AUTRES estimateurs.
- **S4 SÉRIES DE FLUX ENTIÈRES** (§3.4) : la matrice de flux d'entrée
  seule, en pleine résolution (rééchantillonnée à longueur fixe).
  Aucune colonne d'estimateur n'entre.

### 3.3 Diagnostic circulaire C0 (hors critère, étiqueté CIRCULAIRE)

Recomputation directe de la médiane-de-médianes depuis la série
complète (120 lignes, tous les flux), pour les 222 runs × 13 cibles.
Résultat attendu : égalité à 10⁻⁶ près partout. **C0 ne compte pas pour
le critère** : il sert à prouver le plafond (un modèle nourri de la série
complète atteint 100 %) et donc à montrer que l'échec éventuel des
modèles honnêtes est un manque d'information, pas un manque de capacité
du modèle.

### 3.4 Interprétation fixée d'avance (pas après les résultats)

- Succès de S1 ou S2 = **« déjà déterminé »** : la magnitude est déjà
  fixée par la moitié de la construction. C'est une RÉDUCTION (la
  seconde moitié / l'autre moitié des flux n'ajoute rien), pas une
  explication causale du POURQUOI de la valeur.
- Succès de S3 = redondance inter-estimateurs : la magnitude d'un
  estimateur est déjà écrite dans les trajectoires des autres.
- Succès de S4 = seule forme qui compterait comme explication depuis un
  contenu indépendant (la série d'entrée brute, avant tout estimateur).
- Échec de tous = les magnitudes exigent la construction entière ; Delta
  n'est pas élucidé par les séries non plus, et la structure qui résiste
  est à analyser (§6.5), pas à contourner.

## 4. Modèles gelés (numpy/scipy/pandas seulement — sklearn non installé)

Cibles : les 13 médianes. Pour chaque cible, l'entraînement n'utilise que
les runs où la cible est finie (masque : LevinaBickel absent sur 41 runs,
PersistentHomology sur 29 — comme au §8.42). Prédiction d'un run où la
cible est absente : non requise (la construction l'exclut par le masque).
Traits manquants (préfixe ou demi-flux sans aucune valeur finie alors que
la cible existe — possible en principe) : imputés par la MÉDIANE DU TRAIN
de ce trait (règle gelée, calculée sur le train seul) ; le nombre de cas
est compté et rapporté.

- **S1d (direct, sans apprentissage) :** prédiction = médiane-de-médianes
  du PRÉFIXE (60 premières lignes, tous les flux). Aucun paramètre.
- **S1r (ridge) :** 15 traits — [médiane-de-médianes du préfixe de e,
  IQR inter-flux des médianes-préfixe par flux de e, médiane-de-médianes
  du préfixe de chacun des 12 autres estimateurs, log(n)].
  Ridge λ = 10, forme fermée, intercept non pénalisé, standardisation
  par moyenne/écart-type du TRAIN seulement.
- **S2d (direct, sans apprentissage) :** prédiction = médiane-de-médianes
  sur les FLUX PAIRS seuls (tout le scan).
- **S2r (ridge) :** 15 traits — [médiane-de-médianes demi-flux de e,
  IQR inter-flux des médianes demi-flux par flux de e,
  médiane-de-médianes demi-flux de chacun des 12 autres estimateurs,
  log(n)]. Ridge λ = 10, comme S1r.
- **S3r (ridge) :** 13 traits — [médiane-de-médianes du préfixe de
  chacun des 12 autres estimateurs, log(n)]. Ridge λ = 10. Aucune
  information de e.
- **S4r (ridge) :** 102 traits depuis la matrice d'entrée : chaque série
  de flux rééchantillonnée à K = 20 positions par interpolation linéaire
  sur l'indice (0..n−1 → 0..19) ; à chaque position, moyenne, écart-type
  (ddof=1, 0 si p=1), min, max, médiane inter-flux (5 × 20 = 100) ;
  plus log(n) et p. Valeurs telles que stockées (aucune
  re-standardisation par flux — l'échelle fait partie de l'information).
  Ridge λ = 10.
- **S4k (kNN) :** mêmes 102 traits que S4r, standardisés (train seul),
  k = 5, distance euclidienne, prédiction = moyenne simple des 5 voisins.
- **B0 (base) :** constante = médiane du TRAIN par cible.
- MFA : prédiction rapportée brute ET « snapée » sur la plus proche des
  valeurs MFA observées au TRAIN (règle gelée, les deux taux rapportés).
- **Aucun autre modèle, aucun hyperparamètre ajusté sur le test.** La
  sensibilité λ ∈ {1, 100} pour S1r est rapportée en diagnostic, pas
  comme sélection de modèle.

## 5. Hold-outs gelés — l'unité d'indépendance est la MATRICE, pas le run

Reprise exacte du §8.42 §5 (mêmes règles, même code de découpage) :
les 222 runs ne reposent que sur 156 matrices distinctes.

### 5.1 PRIMAIRE — leave-one-cohort-out (LOCO), groupé par matrice

- Cohorte d'une matrice, par règles gelées appliquées dans CET ordre à
  `csv_path` (premier motif qui correspond gagne) : `biophysique-hp35`
  → hp35 ; `geo62452` → geo62452 ; `geo71729` → geo71729 ; `icgc` →
  icgc ; `cptac` → cptac ; `depmap` → depmap ; `coad` → coad ; `luad`
  → luad ; `tcga` → tcga.
- 9 plis : entraîner sur 8 cohortes, tester sur la cohorte tenue à l'écart.
  Toutes les lignes (v6.1, v6.2, rep2) d'une même matrice restent du même
  côté. Scores POOLÉS sur les 222 runs, et par pli.
- **Critère (primaire) :** paires ≥ 90 % ET valeurs ±0,10 ≥ 90 % poolés.

### 5.2 SECONDAIRE A — split aléatoire par matrice (graine 42)

- 70 % des 156 matrices distinctes au TRAIN, 30 % au TEST (tirage
  stratifié par cohorte autant que possible, graine 42) ; toutes les lignes
  d'une matrice du même côté. Rapporté seulement (comparaison avec LOCO).

### 5.3 SECONDAIRE B — hold-out version v6.1 → v6.2 (DIAGNOSTIC, FUITE NOMMÉE)

- Modèles appris sur les 156 runs v6.1, testés sur les 66 runs v6.2. Les
  matrices se recouvrent : score attendu gonflé, rapporté avec la mention
  **FUITE — mêmes matrices des deux côtés, ne compte pas pour le critère**.
  Sert uniquement à quantifier la fuite (comparaison avec LOCO).

### 5.4 Critère de succès (écrit avant les résultats)

**ÉLUCIDÉ** si et seulement si AU MOINS UN des modèles honnêtes
S1d, S1r, S2d, S2r, S3r, S4r, S4k atteint **à la fois** (a) paires
≥ 90 % ET (b) valeurs ±0,10 ≥ 90 % sur le LOCO poolé (§5.1) **ET** les
mêmes deux volets ≥ 90 % sur le split aléatoire par matrice (§5.2).
Sinon le verdict est **NON ÉLUCIDÉ**, avec les chiffres de chaque modèle
et de chaque hold-out. C0 est exclu de la candidature par construction
(§3.3). (Exiger les deux hold-outs évite qu'un split chanceux fasse
verdict.)

## 6. Mesures gelées (toutes rapportées, en hold-out)

### 6.1 Dérivation des prédictions (construction, §1)

- Pour chaque run test : prédire les 6 médianes divergence ; retirer les
  membres masqués (masque vrai, §2.1 — autorisé comme aux §8.39/§8.42) ;
  trier ; paire prédite et d_div prédit par la règle de parité (k=6 :
  moyenne 3e/4e ; k=5 : 3e seule ; k=4 : moyenne 2e/3e). Même règle côté
  saturation (7 membres, toujours complets) : d_sat prédit = 4e valeur
  triée prédite ; Delta prédit = d_div prédit − d_sat prédit.
- Paire : exactitude sur la paire NON ORDONNÉE (primaire) ; paire
  ordonnée en secondaire.
- Valeur : fraction des runs avec |d_div prédit − d_div vrai| ≤ 0,10.

### 6.2 Par cible (LOCO poolé, meilleur modèle honnête et S1r)

- R² (hold-out) et MAE pour chacune des 13 médianes ; corrélation de
  Pearson prédit/vrai. MFA : taux d'exactitude après snap (§4).

### 6.3 Le concours des trois hauts (k=6, LocalPCA 3e, n=176)

- Classification à 3 classes : lequel de {MFA, LevinaBickel, PCAIntrinsic}
  est le plus petit (vrai) vs prédit par le modèle. Exactitude vs hasard
  1/3 et vs majorité du TRAIN. Rapportée pour le meilleur modèle honnête.

### 6.4 Dérive préfixe / demi-flux (ce que S1d/S2d peuvent au mieux faire)

- Par estimateur : distribution de |préfixe-MoM − médiane complète| et
  de |demi-flux-MoM − médiane complète| ; fraction ≤ 0,10 ; moyenne et
  médiane de l'écart. C'est le plafond direct de S1d/S2d par cible, avant
  tout apprentissage.

### 6.5 Résidu intra-groupe (la question posée)

- Dans les deux plus gros groupes structurels (LP, MFA 6,0, n=178) et
  (LP, MFA 7,0, n=178) : corrélation de Pearson (d_div prédit, d_div vrai)
  et écart-type résiduel, en LOCO, meilleur modèle honnête. Même mesure
  poolée sur tous les groupes (masque, MFA, n) de taille ≥ 10
  (corrélation intra-groupe).
- Si le meilleur modèle honnête échoue : analyse du POURQUOI — quelle
  structure résiste (dérive préfixe par estimateur, concours des trois
  hauts, résidu intra-groupe, portabilité LOCO vs split).

### 6.6 Contrôles d'honnêteté

- C0 : recomputation série complète 222 × 13 (§3.3).
- Paires prédites identiques réel vs nul : pour chaque paire de runs
  (réel, nul) de même matrice et même version dans l'ensemble de 222
  (appariement par nom de dossier : le nul est le dossier `_nul`
  correspondant), fraction où le meilleur modèle honnête (LOCO) prédit
  la même paire — à comparer à §8.39 H10 (base 44,6 %) et §8.42
  (101/121, 83,5 %).
- En-échantillon (TRAIN sur tout, test sur tout) rapporté pour référence
  seulement, marqué SURAJUSTEMENT POSSIBLE, jamais comme verdict.
- Déduplication : les scores LOCO du meilleur modèle honnête sont
  re-calculés sur les 153 runs du §8.39.6 (sans les 10 rep2, sans les
  doublons de `div_sorted`, premier exemplaire gardé) en sensibilité ;
  le compte effectif est vérifié et rapporté (attendu : 153).
- Variante « masque ignoré » (k=6 forcé) : paires/valeurs LOCO pour le
  meilleur modèle honnête.
- Variante « d_sat seul » : MAE de d_sat prédit et fraction à ±0,10,
  LOCO, meilleur modèle honnête.
- Sensibilité λ ∈ {1, 100} pour S1r (LOCO).

## 7. Ce que ce protocole ne fera pas

- Aucun run du pipeline, aucune modification d'un code (v6, v6.1, v6.2
  intacts — SHA vérifiés avant travail, voir §8).
- Aucune série complète de l'estimateur cible comme prédicteur (C0 est un
  diagnostic, pas un modèle) ; aucun nouveau prédicteur ajouté après
  avoir vu les résultats ; la liste du §4 est gelée. Aucun modèle hors §4.
- Aucun ajout des 185 dossiers v62 postérieurs (§8.47/§8.53) à
  l'ensemble gelé de 222 runs ; ils restent hors de ce chantier.
- Aucune sélection d'indicateur après coup ; aucune affirmation clinique.
- Aucun push GitHub, aucune régénération du PDF (hors de ce chantier).

## 8. Traçabilité et provenance

- Script unique de ce chantier : `v62_delta_series_857.py` (lecture seule
  des JSON/CSV, écritures : `v62_delta_series_857.log`,
  `v62_delta_series_857.json`, `v62_delta_series_857.md`,
  `v62_delta_series_857_features.csv` — traits de série par run, avec
  SHA-256 de chaque matrice d'entrée et de chaque `df_feat.csv`).
- Pipeline : v6.2 `universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` ;
  v6.1 SHA-256
  `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ;
  v6 SHA-256 `bb8bbdba…c0773` (forme courte du dossier ; complet dans
  `PROVENANCE_v6.2.md`). **Aucun run du pipeline dans ce chantier.**
- Données : les 222 `master_results.json` (156 v6.1 + 66 v6.2), les 222
  `df_feat.csv` (séries d'estimateurs, 120 lignes de scan) et les 156
  matrices de flux (TCGA, GEO, ICGC, CPTAC, DepMap, COAD, LUAD, HP35 —
  voir les `PROVENANCE_*.md` du dossier — et leurs nuls permutés,
  graine 42). Nature des lignes : sorties instrumentales du pipeline
  (médianes par estimateur) ; séries d'estimateurs = valeurs de
  l'estimateur le long du scan, par flux ; matrices de flux = mesures
  omiques publiques ; contrôles = noms de flux (étiquettes, mots humains).
- Consignation : verdict au livre blanc en §8.57, ligne correspondante
  au §7, entrée de journal datée. PDF non régénéré (hors de ce chantier).
- Ce qui manque (déclaré d'avance) : les séries `df_feat` ne sont pas
  les séries de flux brutes (ce sont des valeurs d'estimateurs le long
  du scan, pas des mesures directes) ; les traits S1–S3 sont des
  médianes de parties de séries, pas les séries point par point ;
  aucune famille entièrement nouvelle au-delà des 9 cohortes n'est testée
  (LOCO teste la généralisation à une cohorte tenue à l'écart, pas à une
  source inconnue) ; les 185 runs v62 postérieurs ne sont pas dans
  l'ensemble.

— Fin du protocole gelé. —
