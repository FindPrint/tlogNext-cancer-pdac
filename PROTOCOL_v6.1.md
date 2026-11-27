# PROTOCOLE GELÉ — v6.1.0 « séries courtes + L7a honnête »

Date de gel : 16 novembre 2026.
Auteur : TagPrint (pour Zackary Drasse-Ménard).
Fichier source : `~/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py`
SHA-256 v6 (vérifié avant travaux) : `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`
Fichier produit : `universal_v6.1.0_cohen.py`, VERSION_MASTER
`v6.1.0-L7aL7b-CohenD-short`.
Original v6 jamais modifié ; original v5.9.0f jamais modifié (SHA `4f80f6a7…8260`).

## 1. Défauts mesurés (faits, pas des hypothèses)

### (a) Faux vote L7a sous n = 75 — chaîne vérifiée sur les sorties réelles
1. Le diagnostic de bruit découpe la série en 5 bins et exige ≥ 15 points
   par bin (code, lignes ~4118–4154) → minimum 75 points.
   À n = 52/63/69/70, `hurst_computed = False` pour chaque flux.
2. `variance_proxy_score = NaN` pour chaque flux ; `csd_ranking` ne contient
   que des NaN (construction lignes ~7549–7557 : `float(variance_proxy_score)`
   sans garde).
3. `level_risk` (L4, lignes ~8943–8948) : `top_csd = float(csd[0][1])` SANS
   garde NaN → `top_csd = NaN` → `risk_score = NaN` → `level = "low"`
   (les comparaisons `NaN >= 0.65` sont fausses) → `confidence = NaN`.
4. `level_coherence_universal` (L7a, lignes ~11020–11040) : le poids L4 vaut
   `0.20 × NaN = NaN` → `votes["flat"] = NaN` → `raw_total = NaN` →
   le test `raw_total <= 1e-9` est faux (NaN) → le retour
   `indeterminate` existant n'est jamais atteint → `max(probs, key=probs.get)`
   sur des NaN retourne "up" (premier élément, comparaisons fausses) →
   `global_confidence = NaN` → repli 0,50.
5. Conséquence : le « up » et la confiance 0,50 des petits runs ne sont pas
   un vote — L7a ne dit rien sur ces cohortes.

### (b) Séries courtes bloquées
Porte d'entrée `run_pipeline` (lignes ~6761–6769) :
`min_required = max(20, min(min_len, w_size))`. Mode fast : min_len 50,
w_size 80 → 50 points minimum. Le bras CRISPR DepMap (45 lignées adéno)
échoue en 4 s : « Série trop courte: 45 points valides. Au moins 50 sont
requis ». C'est le seul endroit où le pipeline n'a pas pu tester.

### (c) Discrimination faible réel/nul (ÉTUDE, pas un changement de code)
Le 16 nov., 18 runs v6 (immunitaire 8, PARP 2, ATR 2, pan-cancer 4, ICGC 2),
tous exit 0, AUCUN ne sépare réel et nul (Delta, MC). Sur HP35 (n=1000) le
pipeline sépare nettement (MC max 1,772 réel contre 0,121 nul) ; sur TCGA v4
il sépare par la falsification (delta 0,849) et L7a DOWN 86,3 % contre UP
45,1 % au nul. La phase 2 de cette mission est un protocole d'étude gelé —
aucun changement de code pour (c) dans la v6.1.

## 2. Changements gelés (rien d'autre ne change)

### C1 — Garde `top_csd` dans `level_risk` (~l.8943–8948)
- Avant : `top_csd = float(csd[0][1])` (ou `.get("score", 0)`).
- Après : la valeur brute passe par `_sf(..., 0.0)` — repli 0.0 si non finie.
  `_sf` est la garde déjà utilisée à la ligne 8942 pour `avg_proxy`.
  Le repli 0.0 est celui du cas `csd` vide (ligne 8943) : aucun nouveau
  comportement, on restaure le comportement du cas vide.
- Défense en profondeur, même fonction : `risk_score = _sf(risk_score, 0.0)`
  après le clip — sans effet quand les entrées sont finies.

### C2 — Garde `csd` du Monte-Carlo (~l.10435–10439)
- Même défaut : `csd = float(csd_ranking[0][1])` sans garde, alimente
  `complexity_guided_mc_paths(csd=...)`.
- Après : `_sf(..., 0.50)` — repli 0.50 = la valeur du `except` de ce même
  bloc, et la valeur initiale de `csd` (ligne ~10421). Sans effet quand
  la valeur est finie.

### C3 — Gardes des poids de vote L7a (`level_coherence_universal`)
- Chaque poids `w` (L1, L3, L4, L5) et l'incrément de magnitude L1 passent
  par `_sf(..., 0.0)`.
- Effet : si tous les poids sont nuls ou non finis, `raw_total <= 1e-9`
  → le retour EXISTANT se déclenche :
  `{"status": "insufficient_data", "consensus_direction": "indeterminate",
  "global_confidence": 0.0}`. Le faux « up » par `max()` sur des NaN
  disparaît. Aucun nouveau chemin de code.
- Le repli existant `global_conf = 0.50` quand non fini est conservé tel
  quel (défense en profondeur).
- L7b lit déjà `status != "ok"` comme INDETERMINE : le statut
  « indéterminé » de L7a se propage honnêtement à L7b.

### C4 — Séries courtes, mode fast uniquement
- `'fast': {... 'min_len': 50 ...}` → `'min_len': 40`.
- Effet sur la porte : `min_required = max(20, min(40, 80)) = 40`.
  Les 45 lignées DepMap passent.
- Justification du nombre 40 :
  - Cible : DepMap 45 lignées (marge 5 points).
  - 40 est le seuil que le code utilise déjà comme point de bascule
    (Higuchi : `if n_s < 40` → implémentation native ; en dessous de 40,
    le comportement des estimateurs est moins caractérisé).
  - Le scan à fenêtre glissante bloque déjà `w_size` à `n // 2`
    (22 à n=45 → 24 fenêtres), suffisant pour le scan.
  - Tous les autres planchers du code sont ≤ 20 (walk-forward 20,
    divers 10) — 40 reste au-dessus.
  - La formule de la porte est inchangée.
- Modes robust / full / stable / analyze / predict INCHANGÉS
  (min_len 100 / 150 / MIN_SERIES_LENGTH / 80 / 80).
- Le diagnostic de bruit reste dégénéré sous n=75 (5 bins × 15) — fait
  connu, désormais gardé (C1–C3), pas corrigé ici. Les bins adaptatifs
  (option c du 16 nov.) restent une conception séparée, hors de cette
  version.

### C5 — Version et en-tête
- `VERSION_MASTER` : `v6.0.0-L7aL7b-CohenD` → `v6.1.0-L7aL7b-CohenD-short`
  (`VERSION` devient `v6.1.0` automatiquement par le split existant).
- En-tête : note v6.1 expliquant C1–C4 et leur raison, comme pour la v6.

## 3. Ce qui ne change PAS
- Tous les estimateurs (29), tous les modes sauf le min_len fast,
  Cohen-d partout, la cascade, les seuils, la falsification, le chemin
  predict/MC (`min_len=50` codé en dur dans
  `_evaluate_predictive_mc_complexity_paths` — hors scope ; dégradation
  gracieuse par NaN déjà prévue, sans crash).
- Aucun paramètre n'est retouché après les runs.

## 4. Critères d'acceptation (écrits avant les runs)
- HP35 réel (n=1000) : cascade IDENTIQUE à v6 (0 / 16 / 90 / 376).
- HP35 nul : cascade identique au nul v6.
- TCGA v4 réel (n=178) : cascade identique à v6
  (0 / 74,06 / 93,22 / 98,44 / 98,96), L7a DOWN ~86 %.
- GSE62452 (n=69) et ICGC (n=70) : L7a ne sort PLUS de faux « up » / 0,50.
  Comportement attendu : « indeterminate » / 0,0 si tous les poids sont
  nuls, ou vote fini issu de L1/L3/L5 — rapporter tel quel, sans forcer.
- DepMap réel + nul (45 lignes) : runs complets, exit 0 ; cascade, L7a,
  MC, Delta rapportés.
- Si un critère échoue : diagnostiquer, corriger la copie, re-valider,
  le dire dans le rapport. Ne jamais forcer.

## 5. Traçabilité
- Construction par script `build_v6.1.py` : remplacements exacts, assertions,
  comptage. SHA-256 de la copie noté ; SHA-256 de la v6 revérifié inchangé
  après travaux.
- Rapport : `PROVENANCE_v6.1.md` (même dossier que ce protocole).
- Adoption : la v6.1 devient version de travail UNIQUEMENT sur le go de
  Zackary, après validation. En attendant, la v6 reste la version de travail.
