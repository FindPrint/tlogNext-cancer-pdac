# PROTOCOLE GELÉ — v6.2 : hachage stable L5, score S_sep, élucidation de Delta

Date : 18 novembre 2026.
Statut : **PROTOCOLE GELÉ. Aucun code écrit, aucun run lancé, aucun changement
de la v6.1. La construction de la v6.2 attend le go séparé de Zackary, suivi
du cycle de validation complet décrit au §5. Toute déviation de ce protocole
arrête le travail et se consigne, elle ne se corrige pas en silence.**
Auteur : TagPrint.
Dossier : `~/workspace/runs/pdac-v6/`.
Pipeline de travail : `~/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py`,
SHA-256 `2af5e5ce…c1c9` (vérifié avant tout travail ; la v6.1 et la v6 ne sont
JAMAIS modifiées — la v6.2 est construite sur une COPIE).
Proposition d'origine : `PROTOCOLE_v6.2_proposition.md` (18 nov. 2026) — ce
protocole la transforme en conception gelée, il ne la modifie pas.

## 0. Verdict d'abord — ce qui est gelé ici

Trois pistes, dans l'ordre, une seule à la fois, chacune validée avant la
suivante :

1. **(a) Hachage stable L5** — UN SEUL changement de code : remplacer
   `hash(metric)` (ligne 8985 de la v6.1) par un hachage SHA-256 stable
   (§2, formule littérale). But : gigue L5 = 0 entre deux runs du même
   processus séparé.
2. **(b) Score S_sep = max_separation × stability** — lecture NOUVELLE
   d'un sous-produit existant, calculée HORS du pipeline à partir de
   `master_results.json` (§3). Aucune modification du pipeline pour ça.
3. **(c) Élucidation des niveaux de Delta** — lecture de code + mesures
   sur les sorties déjà sur disque, AVANT tout usage de Delta comme
   discriminateur (§4).

Règle du projet rappelée : aucun consensus exigé entre flux ou contrôles ;
aucun seuil pré-enregistré au-delà de ceux écrits ici ; aucune affirmation
clinique — l'étude porte sur l'instrument, pas sur le cancer.

## 1. Ce que la phase 2 a mesuré (rappel, §8.35, `v61_phase2_table.md`)

Protocole : `PROTOCOL_phase2_discrimination.md` (16 nov. 2026). Extracteur :
`extract_phase2.py` (SHA `5eb3ac24…75aa`). 8 paires principales (HP35,
TCGA v4, GSE71729, GSE62452, ICGC, immunitaire TCGA, PARP TCGA, DepMap),
nul = lignes permutées, graine 42, colonne de contrôle intacte.

- MC best_score : sépare 1/8 (HP35 seul) ; écarts PDAC +0,0059 à +0,0545,
  tous sous la gigue ±0,07 — 7/8 positifs mais noyés.
- max_separation : sépare 6/8 (HP35 +1,6512 ; écarts PDAC +0,10 à +0,37) ;
  échoue sur GSE71729 (+0,0402) et GSE62452 (−0,0036). Annexe : 16/23.
- Delta : 6/8, mais échoue sur HP35 (témoin positif, nul 4,57 > réel 4,48)
  et deux écarts ≤ 0,15. Annexe : 13/23.
- L7a : 4/8, direction majoritaire négative. Cohérence par flux : 2/8.
- Gigue L5 mesurée : ±0,07, cause identifiée au §8.30 — `hash()` Python,
  aléatoire d'un processus à l'autre (`PROVENANCE_v6.1.md` §5 :
  `hash('PersistentHomology') % 1000` = 14 puis 133 dans deux processus ;
  sur HP35, L4 risque 0,84 → 0,91, L7a conf 0,377 → 0,382 entre v6 et v6.1).

## 2. (a) Changement de code exact et unique — hachage stable L5

### 2.1 Ce que le code fait aujourd'hui (vérifié par lecture, lignes citées)

- L'unique occurrence de `hash(` dans tout le fichier v6.1 est la ligne
  8985, dans `level_complexity` (lignes 8965–9029, « L5 mono-horizon ») :

```python
paths = mc_paths(progress, series, threshold, h, max(6, min(int(n_sc), 12)), risk_prof, int(seed) + (hash(metric) % 1000))
```

  Vérifié par `grep -n "hash(" universal_v6.1.0_cohen.py` : 1 seule occurrence.
  `hashlib` n'est importé NULLE PART dans le fichier (grep : 0 occurrence).
- Contexte : la ligne ne s'exécute que si l'alerte EWS de la métrique est
  présente, finie et ≥ 0,25 (`if alert is not None and np.isfinite(alert)
  and float(alert) >= 0.25`, ligne 8984). `mc_paths` (lignes 8698–8745)
  graine son générateur par `rng = np.random.default_rng(seed)` ; le seed
  varie donc d'un processus à l'autre parce que `hash()` des chaînes est
  aléatoire par processus en Python (`PYTHONHASHSEED` non fixé).
- `seed` arrive de la ligne de commande (`--seed`, défaut 42, ligne 12767 ;
  `RANDOM_SEED = 42`, ligne 215) et traverse `level_complexity_universal`
  (lignes 9081–9125, `seed=42` par défaut) puis `level_complexity`
  (appel ligne 11779 : `seed=seed`).

### 2.2 Le remplacement gelé (UNE SEULE formule, écrite littéralement)

Fichier de départ : copie exacte de la v6.1 →
`~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`.
Construction par script miroir de `build_v6.1.py` (remplacements exacts,
assertions, comptage ; l'original n'est jamais modifié), avec ces deux
remplacements et rien d'autre :

**Remplacement H1 — import (en tête du fichier, avec les autres imports) :**

```python
import hashlib
```

**Remplacement H2 — ligne 8985, ancien texte exact :**

```python
int(seed) + (hash(metric) % 1000)
```

**nouveau texte exact :**

```python
int(seed) + (int.from_bytes(hashlib.sha256(metric.encode('utf-8')).digest()[:8], 'little') % 1000)
```

La ligne complète devient donc :

```python
paths = mc_paths(progress, series, threshold, h, max(6, min(int(n_sc), 12)), risk_prof, int(seed) + (int.from_bytes(hashlib.sha256(metric.encode('utf-8')).digest()[:8], 'little') % 1000))
```

**Remplacement V — version (ligne 9211) :**

```python
VERSION_MASTER = "v6.2.0-L7aL7b-CohenD-short"
```

avec une note d'en-tête v6.2 (comme la note v6.1) disant : seul changement,
le hachage stable L5 ; renvoi au présent protocole.

Vérifications de construction (assertions du script de build, arrêt si
échec) :

- SHA-256 de la v6.1 source = `2af5e5ce…c1c9` (complet à noter dans le
  rapport de build) avant toute copie ; SHA-256 de la v6 revérifié
  inchangé après travaux.
- Chaque remplacement : exactement 1 occurrence de l'ancien texte,
  1 remplacement.
- Après construction : `grep -n "hash(" universal_v6.2.0_cohen.py` doit
  retourner **0 occurrence** du `hash(` natif (la nouvelle ligne utilise
  `hashlib.sha256(`, qui ne contient pas la sous-chaîne `hash(`) ;
  `grep -n "hashlib" ` doit retourner exactement 2 occurrences (l'import
  + l'usage ligne 8985).
- `python3 -m py_compile universal_v6.2.0_cohen.py` : exit 0.
- Aucun autre fichier modifié, aucun autre remplacement, même « évident ».
  Si un remplacement échoue (texte introuvable, comptage ≠ 1) : arrêt,
  diagnostic, pas de retouche à la main.

Note : fixer `PYTHONHASHSEED=0` dans l'environnement NE suffit PAS et
n'est PAS la correction : la correction est dans le code, robuste quel
que soit l'environnement d'exécution.

### 2.3 Chaîne de dépendance exacte du seed — ce qui bouge, ce qui ne bouge pas

Lue dans le code, pas devinée. `mc_paths` retourne des chemins dont seule
la **médiane** est utilisée dans L5 (lignes 8986–8991) :

```python
drift_rel = (med[-1] - med[0]) / (abs(med[0]) + 1e-9)
alert_proj = clip(alert + 0.15 * tanh(drift_rel * h / 6.0), 0.0, 1.0)
```

puis, par métrique (`ALL_METRICS` = les 29 estimateurs, ligne 1965) :

- `score = 0.5 * max(0, r2) + 0.5 * alert_proj` (si alerte finie) ;
- `alerts` : la métrique entre dans la liste si `alert_proj ≥ alert_threshold`
  du profil de risque (profil `moderate` par défaut : 0,55, lignes 8283–8291) ;
- sortie L5 mono-horizon : `ranking` (trié par score), `alerts`,
  `top_metric` (1er du ranking), `confidence =
  clip(0.3 + 0.5 * ranking[0].score + 0.1 * min(len(ranking), 5) / 5, 0.1, 0.9)`,
  `n_alerts`, `details[metric].alert`.

Agrégation multi-horizons (`level_complexity_universal`, lignes 9081–9125 ;
`_aggregate_multi_horizon_complexity`, lignes 9023–9080 ; horizons
défaut 1..12, `_resolve_horizons` lignes 8574–8586) :

- `alerts` finales = union sur les horizons (max de l'alerte par métrique) ;
- `top_metric` final = métrique la plus votée sur les horizons ;
- `stability` = fraction d'horizons d'accord sur le top ; `confidence`
  finale = `median_confidence` de l'agrégat.

**Champs de `master_results.json` qui DÉPENDENT de ce seed (donc gigotent
en v6.1 et doivent être stables en v6.2) :**

1. `prediction_levels.L5_complexity` : `ranking[].score`, `alerts`,
   `top_metric`, `confidence`, `n_alerts`, `details[].alert`,
   `multi_horizon.{stability, consensus_top_metric, median_confidence}`.
2. `prediction_levels.L4_risk` — `level_risk` (lignes 8928–8963, appelé
   ligne 11780 avec `L5.get("alerts", [])`) :
   `risk_score = clip(0.40 * avg_proxy + 0.25 * top_csd + 0.35 * mean_alert, 0, 1)`
   où `mean_alert` est la moyenne des alertes L5 ; `level` (high/medium/low,
   seuils 0,65 / 0,40) et `confidence` en découlent.
3. `prediction_levels.L7a_coherence` — `level_coherence_universal`
   (lignes ~11007–11100) : L5 vote SEULEMENT si `status == "ok"` ET
   `alerts` non vide, avec poids
   `w = poids_domaine(L5_complexity) * L5.confidence * _l5_stab`
   (`_l5_stab` = `multi_horizon.stability` de L5, ligne 11008) :
   `votes[trans_dir] += w * 0.50`, `votes["flat"] += w * 0.20` ; L5 entre
   aussi dans `global_confidence` (moyenne pondérée des confiances des
   niveaux). L4 y contribue séparément : si `level == "high"`,
   `votes[trans_dir] += w * 0.60`, sinon `votes["flat"] += w * 0.35`.
   Donc la gigue atteint L7a par DEUX routes (votes L5 directs + niveau L4).
   `consensus_direction` et `global_confidence` de L7a gigotent.
4. `prediction_levels.L7b_robustness` (mode light, `level_robustness_L7b_light`,
   lignes 10762–10831) : lit `L7.l5_horizon_stability` (min de L1/L3/L5) ;
   le hash peut faire basculer le top_metric d'un horizon et donc la
   stabilité (seuils PASS ≥ 0,80 / FAIL < 0,50). L7b ne lit PAS les valeurs
   d'alerte directement.

**Champs qui NE dépendent PAS de ce seed (vérifié : aucun chemin de lecture
de L5 ne les atteint ; l'optimisation du seuil tourne AVANT L5, lignes
6911–6970, et L5 ne renvoie rien vers elle) :**

- `run_pipeline.threshold_metadata.threshold_optimization.best_config`
  (`threshold`, `score`, `metrics.*`, `w_size`, `min_grp`,
  `n_candidates`, `resolution`, `rule`) — donc **MC best_score et
  max_separation ne gigotent PAS à cause du hash** ;
- `run_pipeline.scan_curve`, `five_threshold_cascade` (T_-2…T_+2),
  `harmonic_validation` ;
- `holographic_tension_state` entier (`D_vector`, `Delta_tension`,
  `falsification_vs_null`, `geometric_layer`, `per_estimator`),
  `reading_synthesis.Delta_tension` ;
- Q-scores (`run_pipeline.scores`) : le code déclare
  `enters_threshold_score: False` et `q_numeric_scores_modified: False`
  pour l'état holographique ; L5 n'y entre pas.

**Correction d'une attribution de la phase 2 :** le protocole phase 2
appliquait la gigue ±0,07 comme un forfait à MC best_score, max_separation
et L7a (`extract_phase2.py`, `checks`). Or ±0,07 n'a été MESURÉ que sur
L4/L7a (`PROVENANCE_v6.1.md` §5 : mean_alert 0,7687 contre 0,7783 entre
v5.9.0f et v6 ; HP35 L4 0,84 → 0,91). La chaîne ci-dessus montre que le
hash ne peut pas mouvoir best_score ni max_separation. En v6.2, la gigue
de CHAQUE indicateur est re-mesurée par répétition (§5) ; aucun forfait
de gigue n'est supposé. Si la validation mesure une gigue non nulle sur
best_score ou max_separation, c'est un résultat en soi (autre source de
non-déterminisme à identifier), pas un bruit à ignorer.

## 3. (b) Score de discrimination S_sep — définition exacte, hors pipeline

### 3.1 Formule gelée (UNE SEULE)

```
S_sep = max_separation × stability
```

où `max_separation` et `stability` sont lus dans le `best_config` du run :

```
run_pipeline.threshold_metadata.threshold_optimization.best_config.metrics.max_separation
run_pipeline.threshold_metadata.threshold_optimization.best_config.metrics.stability
```

Définition dans le code (`evaluate_scan_quality`, lignes 3313–3390) :

- `max_separation` = score maximal de la courbe de scan = max du |d de Cohen|
  entre groupes pré-seuil et post-seuil, au seuil choisi.
- `stability = 1 / (1 + écart-type des scores locaux)` sur une fenêtre de
  `max(3, len(scores) // 20)` points autour du pic (0 si un seul point).
  Un pic haut mais entouré de scores dispersés (pic bruité, pointe isolée)
  a un écart-type local élevé donc une stabilité basse ; un pic haut et
  localement plat a une stabilité proche de 1.

Pourquoi cette formule récompense un pic net et stable plutôt qu'un pic
bruité : le premier facteur mesure la hauteur de la séparation, le second
pénalise la dispersion locale autour du pic. Un pic d'une seule pointe
(pointu, instable) voit sa stabilité s'effondrer ; un pic large et plat
garde `stability ≈ 1` et conserve sa hauteur. S_sep est sans unité,
≥ 0, sans borne supérieure ; en pratique ≈ max_separation × ~0,98 sur
les séries PDAC (voir §3.3).

### 3.2 Pourquoi les autres composantes sont EXCLUES (mesuré, pas deviné)

- **`s_norm` exclue** : `s_norm = tanh(max_separation / 2.0)` (ligne 3335),
  fonction strictement croissante de `max_separation`. Multiplier ou
  remplacer par `s_norm` ne change aucun ordre, aucune direction, aucun
  verdict — elle n'apporte rien.
- **`robustness` exclue** : `robustness = exp(-((FWHM - 10)²) / (2 × 5²))`
  (lignes 3346–3362), pénalité gaussienne qui préfère une largeur à
  mi-hauteur (FWHM) de 5–20 % de la plage. Mesuré sur les 16 JSON
  des paires principales v6.1 : robustness vaut 3,37×10⁻⁴¹ (TCGA v4),
  6,66×10⁻³⁵ (GSE71729), 1,03×10⁻²⁵ / 1,39×10⁻¹⁷ (GSE62452),
  5,31×10⁻²⁴ / 5,18×10⁻¹⁹ (ICGC), 1,84×10⁻¹⁰ / 1,99×10⁻⁷ (immunitaire),
  3,37×10⁻⁴¹ (PARP), 2,51×10⁻¹⁶ / 0,0635 (DepMap) — soit ≤ 2×10⁻⁷ sur
  14/16 JSON, contre 0,984 / 0,899 sur HP35 réel/nul. Multiplier par
  robustness annulerait le score sur toutes les séries PDAC (S_sep ≈ 0
  partout, écarts ≈ 0) : la FWHM de ces scans est très loin de l'idéal
  10 %, c'est un fait de forme des courbes, pas une discrimination.
  Ce zéro quasi systématique est consigné comme résultat, pas corrigé.
- **`sharpness` exclue** : `sharpness = tanh(max |dS/dx| local / 0.5)`
  (lignes 3365–3380). Une pointe de bruit d'un seul point a elle aussi
  une dérivée locale maximale — sharpness récompense la raideur, y compris
  celle du bruit. Direction incohérente en phase 2 : le nul est plus
  « sharp » que le réel sur GSE71729 (0,0152 contre 0,0113), immunitaire
  TCGA (0,0251 contre 0,0165) et PARP TCGA (0,0106 contre 0,0100).
- **`score` composite MC exclu comme base** : c'est le best_score déjà
  testé (1/8 en phase 2) ; S_sep est une lecture différente du même
  `best_config`, pas une repondération du composite.

### 3.3 Valeurs de référence v6.1 (calculées ici, à partir des JSON existants)

S_sep = max_separation × stability, paires principales (réel / nul) :

| Paire | S_sep réel | S_sep nul | Écart |
|---|---|---|---|
| HP35 | 1,5391 | 0,1185 | +1,4206 |
| TCGA v4 | 0,4548 | 0,1688 | +0,2860 |
| GSE71729 | 0,2579 | 0,2174 | +0,0405 |
| GSE62452 | 0,3044 | 0,3116 | −0,0072 |
| ICGC | 0,4034 | 0,3073 | +0,0960 |
| Immunitaire TCGA | 0,5263 | 0,1604 | +0,3659 |
| PARP TCGA | 0,3667 | 0,1987 | +0,1680 |
| DepMap | 0,4339 | 0,2524 | +0,1815 |

À titre de repère seulement (le critère du §3.4 utilise la gigue mesurée
en v6.2, pas celle-ci) : avec le plancher historique 0,07, S_sep séparerait
6/8 en v6.1 — les mêmes 6 que max_separation, GSE71729 (+0,0405) et
GSE62452 (−0,0072) échouant. Réserve honnête : `stability` seule ne
sépare pas — elle vaut 0,978–0,997 sur toutes les paires PDAC (quasi
saturée) et, sur HP35, le réel est MOINS stable que le nul (0,8687 contre
0,9827). Son rôle est un garde-fou contre le pic bruité, pas un
discriminateur à elle seule ; la discrimination vient de max_separation,
la stabilité ne fait que la pondérer.

### 3.4 Seuil de succès écrit d'avance

- **Gigue de S_sep** : mesurée en validation (§5) comme le max, sur les
  10 runs × 2 répétitions, de |S_sep(répétition 1) − S_sep(répétition 2)|.
  La gigue effective utilisée est :

```
gigue_eff(S_sep) = max(gigue mesurée, 0,07)
```

  0,07 est le plancher historique de lisibilité du projet (phase 2) : la
  gigue mesurée ne peut que le relever, jamais l'abaisser. Si la gigue
  mesurée est 0, le plancher 0,07 s'applique quand même — sinon le critère
  « écart > 0 » deviendrait trivial (n'importe quel écart non nul
  passerait).
- **Direction** : comme en phase 2 (`verdict()` de `extract_phase2.py`),
  la direction majoritaire est le signe de la somme des écarts réel−nul
  sur les 8 paires principales. La direction attendue est réel > nul
  (celle de max_separation en phase 2) ; si la somme change de signe, la
  direction observée est celle de la somme, et le verdict le dit tel quel.
- **Une paire « sépare »** si |écart| > gigue_eff(S_sep) ET le signe de
  l'écart est celui de la direction majoritaire.
- **Succès** : S_sep sépare sur **≥ 6/8 paires principales**
  (HP35, TCGA v4, GSE71729, GSE62452, ICGC, immunitaire TCGA, PARP TCGA,
  DepMap). Sinon, verdict « Sépare sur X/8 : [liste], échoue sur [liste] »
  avec les chiffres, sans arrondir le verdict.
- Aucun autre seuil, aucune re-définition après avoir vu les résultats.

## 4. (c) Élucidation des niveaux discrets de Delta

### 4.1 Ce que le code dit (vérifié par lecture)

`compute_holographic_tension_state` (lignes 7927–8260) :

- **Médiane par estimateur** (lignes 7970–7994) : pour chacun des 29
  estimateurs, on prend les colonnes du paysage se terminant par
  `_<nom>_mean` (`_estimator_mean_columns`, lignes 7642–7645) ; dans
  chaque colonne, médiane des valeurs finies (`_column_finite` +
  `_median_finite`, lignes 7634–7650 — les non-finis sont jetés, jamais
  imputés) ; puis médiane de ces médianes sur les flux. Résultat :
  `raw_medians[nom]` (None si aucune valeur finie).
- **Valeurs de classe** (lignes 7996–8021) : pour chaque classe de
  `DIMENSION_FOR_TLOG` (lignes 1926–1931), médiane des `raw_medians` des
  membres **finis** — les membres absents sont ignorés silencieusement
  (listés dans `estimators_without_finite_values`, jamais remplacés) :

```python
DIMENSION_FOR_TLOG = {
    "saturation":   ["Higuchi", "Katz", "Petrosian", "Sevcik", "BoxCounting", "Hurst2mH", "DFA"],  # 7
    "criticality":  ["CorrelationD2", "GrassbergerProcaccia", "InformationD1", "VisibilityGraph", "TwoNN", "DANCo", "Fisher"],  # 7
    "divergence":   ["LevinaBickel", "PCAIntrinsic", "LocalPCA", "GraphDimension", "PersistentHomology", "MFA"],  # 6
    "null_reference": ["SpectralDimension"],  # 1
}
```

  (À ne pas confondre avec `ESTIMATOR_CLASSES`, lignes 1904–1925, qui
  compte 8 / 7 / 7 / 7 membres : PermutationEntropy et KolmogorovLZ ne
  sont PAS dans la couche géométrique ; seuls les membres de
  `DIMENSION_FOR_TLOG` entrent dans d_sat / d_crit / d_div.)
- **d_sat** = médiane des 7 médianes saturation = **4e valeur triée**.
  **d_div** = médiane des 6 médianes divergence = **moyenne des 3e et 4e
  valeurs triées**. **d_crit** = médiane des 7 médianes criticité.
  **Delta = d_div − d_sat** (ligne 8021 ; écrit ligne 8226 comme
  `Delta_tension`, et recopié dans `reading_synthesis.Delta_tension`).
  Si d_sat ou d_div est None (classe entièrement vide) : Delta = None.
- `_tension_gap_diagnostics` (lignes 7806–7925) recalcule le même écart
  (`tension_gap_E`, `tension_gap_E_same_as_Delta: True`) et ajoute
  l'écart **trio** : trio par défaut Higuchi / InformationD1 /
  LevinaBickel (`DEFAULT_TRIANGULATION`, ligne ~7755), `trio_gap_E =
  trio_div − trio_sat` si le trio est équilibré, sinon max−min des 3.
  Les seuils de lecture (divergence si d_div ≥ 5,5 ou Delta > 3 ;
  criticité si d_crit ∈ [3,5, 4,5] ou Delta ∈ [1,2, 3]) sont des
  conventions de lecture, pas des théorèmes (lignes 7916–7921).

**Les valeurs par estimateur SONT dans `master_results.json`** — aucun
accès au pipeline n'est nécessaire :

```
holographic_tension_state.per_estimator.<nom>.{raw_median, n_fluxes_used, n_columns, estimator_class, enters_geometric_D}
holographic_tension_state.geometric_layer.axes.<classe>.{dimension_median, n_dimension_estimators_used, estimators_used, estimators_without_finite_values}
holographic_tension_state.D_vector.{d_sat, d_crit, d_div, d_null}
holographic_tension_state.Delta_tension
holographic_tension_state.tension_gap_diagnostics.triangulation.{trio_gap_E, trio_values}
reading_synthesis.Delta_tension
reading_synthesis.n_samples
metadata.control
run_pipeline.threshold_metadata.threshold_optimization.best_config.metrics.{max_separation, stability, robustness, sharpness}
```

### 4.2 Ce qui est déjà mesuré sur les 156 runs v6.1 (18 nov. 2026)

Extraction en lecture seule des `results_fast_v61_*/master_results.json`
(156 runs : 140 du lot + validation + test A + rotations partielles).
Vérifications d'identité (0 écart sur 156 runs) :

- d_div = moyenne des 3e et 4e médianes divergence triées (0 mismatch) ;
- d_sat = 4e médiane saturation triée (0 mismatch).

Faits :

- **d_div prend 133 valeurs distinctes** (à 10⁻³) sur 156 runs — ce ne
  sont PAS « quelques niveaux fixes » au sens brut. Les « niveaux » sont
  des **grappes** : valeurs arrondies à 0,01 les plus fréquentes : 5,39
  (×7), 2,89 (×6), 3,11 (×6), 5,42 (×6), 3,12 (×5), 5,41 (×5).
- **MFA est quasi discret** : 9 valeurs distinctes seulement, dans
  [3,000 ; 7,000], médiane 6,000. Les autres membres divergence sont
  continus (LevinaBickel 121 distincts, PCAIntrinsic 144, LocalPCA 124,
  GraphDimension 104, PersistentHomology 118).
- **Composition finie variable** : LevinaBickel absent (raw_median None)
  sur 31/156 runs ; PersistentHomology absent sur 25/156 (25 runs
  manquent les deux, 6 manquent Levina seule). Quand un membre manque,
  la médiane est calculée sur 5 ou 4 valeurs au lieu de 6 — le rang
  médian change de nature, c'est un saut discret de construction.
  Saturation : **jamais** incomplète (156/156, 7/7 membres).
- **d_div par n** (moyenne ± écart-type) : n=45 → 3,10 ± 0,03 (26 runs) ;
  n=52 → 3,000 exactement (2 runs) ; n=63 → 2,90 ± 0,01 ; n=69 →
  2,86 ± 0,06 ; n=70 → 2,89 ± 0,01 ; n=145 → 4,28 ± 0,27 ;
  n=178 → 5,45 ± 0,47 (98 runs) ; n=285 → 6,24 ± 0,01 ; n=515 →
  4,16 ± 0,01 ; n=1000 → 6,12 ± 0,10. n prédit la grappe mais pas
  monotonement (515 < 285) : n seul ne suffit pas.
- **Corrélations avec d_div** (Pearson, 156 runs) : MFA +0,970 ;
  LocalPCA +0,967 ; GraphDimension +0,880 ; LevinaBickel +0,794 ;
  PCAIntrinsic +0,764 ; PersistentHomology +0,754. Avec le scan :
  max_separation +0,189 ; stability +0,163 ; robustness +0,144 ;
  sharpness +0,205 — toutes faibles. d_sat est quasi constant par
  famille (valeurs arrondies les plus fréquentes : 1,58 ×20, 1,59 ×19,
  1,60 ×18, 1,56 ×17, 1,57 ×16) : la variation de Delta ≈ celle de d_div.
- **Anomalie à consigner** : DFA `raw_median` = −38,16 sur un run
  (les autres DFA sont dans [−38,16 ; 1,73], médiane 1,58). Une médiane
  d'estimateur extrême isolée : vérifier si elle tombe en rang médian
  (4e) sur ce run, et si oui, quel effet sur d_sat.

### 4.3 Hypothèses à mesurer, une par une (script externe, lecture seule)

Nouveau script `extract_delta_levels.py` (même dossier, lecture seule
dans les `master_results.json`, AUCUN run du pipeline, AUCUNE modification
du pipeline). Pour chaque run il extrait une ligne : dossier, n
(`reading_synthesis.n_samples`), contrôle (`metadata.control`), d_sat,
d_crit, d_div, Delta, les 6 médianes divergence triées AVEC leur nom
(identité de la paire médiane 3e/4e), les 7 médianes saturation triées,
le masque fini/absent par membre, `n_fluxes_used` par estimateur,
MFA brut, max_separation / stability / robustness / sharpness du
best_config, direction + confiance L7a, `trio_gap_E`.

Puis, dans l'ordre, sans deviner :

- **H1 — composition finie** : le niveau de d_div dépend-il du masque
  fini/absent (LevinaBickel et/ou PersistentHomology absents) ? Table
  masque × (paire médiane, d_div moyen). Prédit si le masque détermine
  la paire médiane.
- **H2 — MFA discret** : la valeur de MFA (9 valeurs) et le rang qu'elle
  occupe déterminent-ils la paire médiane ? Table MFA × paire médiane.
- **H3 — n et taille d'échantillon** : n, `n_samples`, et `n_fluxes_used`
  (12 flux vs 7 / 6 / 11 dans les rotations et petites cohortes)
  prédisent-ils la paire médiane ? Table par (n, n_fluxes).
- **H4 — largeur du pic** : FWHM/robustness du best_config (corrélation
  déjà faible : +0,144) — confirmer ou infirmer sur les 156 runs +
  v6.2, par corrélation et par table en quartiles.
- **H5 — contrôle** : le contrôle (`metadata.control`, y compris les
  rotations où le contrôle est un flux) change-t-il la composition
  finie (H1) ou la paire médiane ? Table contrôle × masque × paire.
- **H6 — paire médiane** : c'est le mécanisme exact — d_div est
  ENTIÈREMENT déterminé par l'identité des 3e/4e estimateurs et leurs
  valeurs. L'élucidation passe par la prédiction de cette paire.
- **H7 — d_sat quasi constant** : vérifier que d_sat est la médiane
  DFA (ou quel membre est 4e) par famille de séries, et que Delta ≈
  d_div − constante par famille. Si d_sat saute aussi (ex. DFA −38,16
  en rang médian), le dire.

Méthode : corrélations de Pearson/Spearman pour les variables continues,
tables de contingence pour les variables discrètes (masque, MFA, paire
médiane, contrôle). Aucune variable n'est ajoutée après avoir vu les
résultats ; la liste H1–H7 ci-dessus est gelée.

### 4.4 Critère d'élucidation (écrit d'avance)

Le mécanisme est **élucidé** si, sur l'ensemble des runs analysés
(156 v6.1 d'abord, puis confirmés sur les runs v6.2 du §5 et du §6) :

- (a) une variable ou un petit ensemble nommé (parmi H1–H7) prédit
  **l'identité de la paire médiane** (les deux estimateurs 3e/4e) sur
  **≥ 90 % des runs**, ET
- (b) la même variable prédit **la valeur de d_div à ±0,10 près** sur
  **≥ 90 % des runs**.

Sinon le rapport dit **« non élucidé »** avec les chiffres (taux de
prédiction par hypothèse, meilleure variable et son taux). En
particulier : tant que le mécanisme n'est pas élucidé, le 6/8 de Delta
en phase 2 reste une piste fragile (il échoue sur HP35, deux écarts
≤ 0,15, 13/23 en annexe) et Delta ne devient PAS un discriminateur
recommandé. Le `trio_gap_E` est rapporté descriptivement dans la même
table (réel/nul par paire) comme contrôle de lecture — il ne devient
PAS un 10e indicateur de discrimination (aucune sélection d'indicateur
après coup).

## 5. (d) Plan de validation — 10 runs fast + déterminisme

### 5.1 Runs (mêmes commandes que la validation v6.1, `run_v6.1_validation.sh`)

Pipeline : `universal_v6.2.0_cohen.py` (copie construite au §2), mode
`fast`, `--seed 42` (défaut). Dossier de travail `~/workspace/runs/pdac-v6`.
Sorties dans des dossiers NEUFS `results_fast_v62_*` (jamais écraser les
`results_fast_v61_*`).

| # | Série | Entrée | Sortie |
|---|---|---|---|
| 1 | HP35 réel | `~/workspace/runs/biophysique-hp35/test_biophysique_input.csv` | `results_fast_v62_hp35` |
| 2 | HP35 nul | `~/workspace/runs/biophysique-hp35/test_biophysique_input_nul.csv` | `results_fast_v62_hp35_nul` |
| 3 | TCGA v4 réel | `pdac_tcga_fluxes_v4.csv` | `results_fast_v62_tcga_v4` |
| 4 | TCGA v4 nul | `pdac_tcga_fluxes_v4_nul.csv` | `results_fast_v62_tcga_v4_nul` |
| 5 | GSE62452 réel | `pdac_geo62452_fluxes.csv` | `results_fast_v62_geo62452` |
| 6 | GSE62452 nul | `pdac_geo62452_fluxes_nul.csv` | `results_fast_v62_geo62452_nul` |
| 7 | ICGC réel | `pdac_icgc_fluxes.csv` | `results_fast_v62_icgc` |
| 8 | ICGC nul | `pdac_icgc_fluxes_nul.csv` | `results_fast_v62_icgc_nul` |
| 9 | DepMap réel | `pdac_depmap_fluxes.csv` | `results_fast_v62_depmap` |
| 10 | DepMap nul | `pdac_depmap_fluxes_nul.csv` | `results_fast_v62_depmap_nul` |

**Déterminisme : chaque run est lancé 2 fois**, chaque répétition dans
son propre processus `python3` (le hachage Python est aléatoire PAR
PROCESSUS : deux répétitions dans le même processus partageraient le
même `hash()` et cacheraient le défaut). Les deuxièmes répétitions vont
dans `results_fast_v62_*_rep2` (mêmes entrées). Ordre : contrôles
d'identité d'abord (HP35, TCGA v4), puis petits n, puis DepMap — comme
pour la v6.1. Journalisation : log horodaté `runs_v62_validation.log`
avec SHA-256 de la v6.2 et de la v6.1, commandes exactes, exit codes.

### 5.2 Comparaison bit-à-bit — horodatages

**`master_results.json` ne contient AUCUN horodatage.** Vérifié sur le
JSON HP35 v6.1 : aucune clé nommée `timestamp`, `date`, `generated_at`,
`run_date` ou `created_at` dans tout l'arbre. Le seul `ts` du code est
dans `_telemetry_emit` (ligne 561), qui écrit dans `telemetry.jsonl`
(fichier SÉPARÉ, non comparé ici) ; le rapport `.txt` porte une date de
génération mais ce n'est pas le JSON. L'écriture du JSON est
`json.dump(final_output, f, indent=2, default=str)` (lignes 12143 et
12157) ; `final_output['runtime']` ne contient que des chemins et des
statuts (`telemetry.jsonl`, `dashboard.html`, `dashboard_status`),
aucune date.

Comparaison primaire : **sha256sum des deux `master_results.json`** de
chaque paire de répétitions — ils doivent être **octet pour octet
identiques**. Si (et seulement si) la comparaison d'octets échoue, repli
documenté : comparer les champs numériques après parsing JSON, lister
chaque chemin divergent avec ses deux valeurs, et consigner l'écart
comme un résultat (pas comme un bruit à ignorer). `telemetry.jsonl` et
`dashboard.html` sont exclus de la comparaison (le premier contient des
`ts`, le second est un rendu).

### 5.3 Critères d'acceptation (écrits avant les runs)

- Les 10 runs × 2 répétitions terminent, exit 0.
- **Cascades identiques à la v6.1** (le hash ne touche pas la cascade :
  tout changement de cascade signale une erreur de construction, pas un
  effet du hachage — arrêt et diagnostic) :
  HP35 réel 0 / 16 / 90 / 376 ; HP35 nul identique au nul v6 ;
  TCGA v4 réel 0 / 74,06 / 93,22 / 98,44 / 98,96.
- **L7a fini sur les petites cohortes** : GSE62452 (n=69) et ICGC (n=70)
  ne sortent plus de faux « up » / 0,50 (même critère que la v6.1 §4 :
  « indeterminate » / 0,0 si tous les poids sont nuls, ou vote fini
  issu de L1/L3/L5 — rapporter tel quel, sans forcer).
- **DepMap réel + nul (45 lignes)** : runs complets, exit 0 ; cascade,
  L7a, MC, Delta rapportés.
- **Gigue L5 = 0** : entre les deux répétitions de chaque run, identité
  exacte (octet pour octet du JSON, §5.2) de `prediction_levels.L5_complexity`
  (`ranking`, `alerts`, `top_metric`, `confidence`, `n_alerts`),
  de `prediction_levels.L4_risk` (`risk_score`, `level`) et de
  `prediction_levels.L7a_coherence` (`consensus_direction`,
  `global_confidence`). Toute différence > 0 sur l'un de ces champs =
  échec de la piste (a) : arrêt, diagnostic, retour à la v6.1.
- **Gigue S_sep mesurée** : max |ΔS_sep| entre répétitions sur les
  10 runs, consigné avec les 10 valeurs (sert au §3.4). De même,
  consigner les gigues mesurées de MC best_score, max_separation, Delta
  et L7a (confiance signée) — attendues à 0 pour Delta/cascade (déjà
  déterministes en v6.1) et à mesurer pour les autres, sans supposer
  le forfait ±0,07.
- Si un critère échoue : diagnostiquer, corriger la copie, re-valider,
  le dire dans le rapport. Ne jamais forcer. L'adoption de la v6.2 comme
  version de travail attend le go de Zackary après validation, comme
  pour la v6.1.

## 6. (e) Plan du test de discrimination — protocole Phase 2 sur sorties v6.2

- **Quand** : après validation (§5) réussie. **Aucun nouveau run du
  pipeline au-delà du §5** : tout est lu dans les `master_results.json`
  v6.2 déjà sur disque (10 runs de validation + les runs v6.2 des paires
  PDAC restantes, lancés avec les mêmes commandes fast et les mêmes
  entrées que le lot v6.1, dans des dossiers `results_fast_v62_*`).
- **Paires** : les 8 paires principales du protocole Phase 2 (§2 de
  `PROTOCOL_phase2_discrimination.md`) + les 23 paires secondaires en
  annexe (mêmes règles, mêmes gigues, nul graine 42, contrôle intact).
- **Extracteur** : `extract_phase2_v62.py`, copie de `extract_phase2.py`
  étendue d'un 9e indicateur, mêmes règles de comptage (fonction
  `verdict()` inchangée : direction = signe de la somme des écarts ;
  une paire sépare si |écart| > gigue ET signe = direction majoritaire).
  Chemins JSON exacts (cf. §3.1 et §4.1) ; sorties
  `v62_phase2_table.csv` et `v62_phase2_table.json` (même format que
  les fichiers v6.1, avec une colonne `S_sep` en plus).
- **9e indicateur, S_sep** : `S_sep = max_separation × stability` (§3),
  gigue effective = max(gigue mesurée au §5, 0,07) (§3.4). **Critère de
  succès : ≥ 6/8 paires principales** (même barre que la phase 2).
- **Les 8 indicateurs d'origine sont re-calculés sur les sorties v6.2**
  (Delta, MC best_score, max_separation, |ΔT_0|, falsification,
  cohérence par flux, L7a, écart cascade) avec leurs gigues propres :
  Delta/cascade/falsification gigue 0 (déterministes) ; MC best_score,
  max_separation, L7a avec les gigues MESURÉES au §5 (pas le forfait
  ±0,07). But : vérifier que rien d'autre n'a bougé avec le hachage
  stable — un indicateur qui changerait de verdict entre v6.1 et v6.2
  serait un signal d'alarme sur la construction, à diagnostiquer avant
  tout verdict sur S_sep.
- **Verdict** : « S_sep sépare sur X/8 : [liste], échoue sur [liste] »
  avec les chiffres ; si X < 6, la piste (b) est fermée comme les
  autres, sans retouche après coup. Les réserves de la phase 2 restent :
  T_0 et écart cascade sont triviaux par construction (8/8 ne prouve
  rien) ; la falsification est une comparaison interne, pas au nul
  permuté, et indisponible sous n = 75.
- **Élucidation Delta** : le §4.3 est exécuté sur les runs v6.2 en
  même temps (même script, mêmes critères ≥ 90 %) ; le verdict
  « élucidé / non élucidé » est consigné avec le test de discrimination,
  séparément du verdict S_sep.

## 7. Ce que ce protocole ne fera pas

- Aucune modification de la v6.1 ni de la v6 (copie séparée seulement).
- Aucune modification du pipeline pour calculer S_sep (lecture d'un
  sous-produit existant, hors pipeline).
- Aucun nouveau seuil de séparation pré-enregistré au-delà des critères
  des §3.4, §4.4, §5.3 et §6.
- Aucune affirmation clinique : l'étude porte sur l'instrument.
- Aucun consensus exigé entre flux ou contrôles ; aucune sélection
  d'indicateur après coup (la liste des 9 indicateurs est gelée ici).
- Aucun changement de code avant le go de Zackary sur CE protocole, et
  aucun run de validation avant la construction gelée au §2.
- Aucun push GitHub dans ce protocole : la publication suit les règles
  de traçabilité du projet (§8), sur go séparé, après validation.

## 8. Traçabilité et provenance

- Construction : script de build (miroir de `build_v6.1.py`) conservé
  dans `~/workspace/runs/pdac-v6/` ; SHA-256 de la v6.1 source, de la
  v6.2 construite et de la v6 notés dans le rapport de build.
- Validation : `runs_v62_validation.log` (commandes, exit codes,
  SHA-256), `v62_validation_compare.md` (cascades v6.1 vs v6.2,
  gigues mesurées par indicateur, dont S_sep).
- Discrimination : `extract_phase2_v62.py` (SHA noté),
  `v62_phase2_table.csv` / `.json` / `.md`.
- Élucidation Delta : `extract_delta_levels.py` (SHA noté),
  `v62_delta_levels.csv` / `.md` (tables H1–H7, taux de prédiction).
- Consignation au livre blanc (§8.37 : construction v6.2, validation,
  test de discrimination S_sep, élucidation Delta) et `PROVENANCE_v6.2.md`
  (même forme que `PROVENANCE_v6.1.md`), avec les hachages des données
  d'entrée (CSV inchangés depuis la phase 2) et la nature des lignes
  (mesures instrumentales vs mots humains vs échantillons hypothétiques),
  comme l'exige la règle permanente de provenance.
- Versions : `VERSION_MASTER` v6.2.0-L7aL7b-CohenD-short ; la v6.1 reste
  la version de travail jusqu'au go d'adoption de Zackary.

## Annexe A — Chemins JSON exacts (référence pour les extracteurs)

| Valeur | Chemin dans `master_results.json` |
|---|---|
| max_separation, stability, robustness, sharpness, s_norm | `run_pipeline.threshold_metadata.threshold_optimization.best_config.metrics.*` |
| MC best_score, seuil MC | `run_pipeline.threshold_metadata.threshold_optimization.best_config.{score, threshold}` |
| Cascade T_-2…T_+2 | `five_threshold_cascade.{T_-2_F2_pre_onset, T_-1_F1_pre_inflection, T_0_Monte_Carlo_Central, T_+1_F1_post_deceleration, T_+2_F2_post_attractor}` |
| Delta | `reading_synthesis.Delta_tension` (= `holographic_tension_state.Delta_tension`) |
| d_sat, d_crit, d_div, d_null | `holographic_tension_state.D_vector.*` |
| Médianes par estimateur | `holographic_tension_state.per_estimator.<nom>.{raw_median, n_fluxes_used}` |
| Axes géométriques | `holographic_tension_state.geometric_layer.axes.<classe>.{dimension_median, estimators_used, estimators_without_finite_values}` |
| Écart trio | `holographic_tension_state.tension_gap_diagnostics.triangulation.{trio_gap_E, trio_values}` |
| Falsification | `holographic_tension_state.falsification_vs_null.delta_vs_null` |
| L7a | `prediction_levels.L7a_coherence.{consensus_direction, global_confidence}` |
| L5 | `prediction_levels.L5_complexity.{ranking, alerts, top_metric, confidence, n_alerts}` |
| L4 | `prediction_levels.L4_risk.{risk_score, level}` |
| n, contrôle | `reading_synthesis.n_samples`, `metadata.control` |
| Version | `version` (= `v6.2.0-L7aL7b-CohenD-short` après construction) |

## Annexe B — Références chiffrées v6.1 (à comparer, pas à réutiliser comme seuils)

- S_sep par paire : §3.3. max_separation par paire : §1 / `v61_phase2_table.md`.
- d_div par n (156 runs) : §4.2. MFA : 9 valeurs distinctes dans [3,000 ; 7,000].
- Robustness sur les 16 JSON principaux : HP35 0,984 / 0,899 ; PDAC
  ≤ 2×10⁻⁷ sauf DepMap nul 0,0635 (§3.2).
- Gigue historique L4/L7a : ±0,07 (`PROVENANCE_v6.1.md` §5).

— Fin du protocole gelé v6.2. —
