# PROVENANCE — UNIVERSAL_LOG v6.1.0 « séries courtes + L7a gardé »

Date : 16 novembre 2026, 18h05–18h20 (heure de Montréal).
Auteur : TagPrint (sous-agent), sur ordre de Zackary (« Teste mon pipeline », 16 nov. 18h13 ; go confirmé 17h58).
Statut : **copie construite et validée ; adoption comme version de travail = go de Zackary, NON DÉCLARÉE ici.**

## 1. D'où vient v6.1

- **Parent :** `~/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py`,
  SHA-256 `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`,
  622 526 octets, VERSION_MASTER `v6.0.0-L7aL7b-CohenD` (Cohen-d partout, Cliff retiré).
- **Original v5.9.0f jamais modifié :** SHA `4f80f6a7d0809e802cbc9ec30c0bed552c1c8a95eb58687fd78e4ffd8e808260`.
- **Construction :** `~/workspace/runs/pdac-v6/build_v6.1.py` — 10 remplacements exacts
  avec assertions, comptage noté ; copie compilée OK ; SHA du parent revérifié
  inchangé après construction.
- **Copie v6.1 :** `~/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py`,
  SHA-256 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`,
  623 495 octets, VERSION_MASTER `v6.1.0-L7aL7b-CohenD-short`.
- **Conception gelée avant code :** `~/workspace/runs/pdac-v6/PROTOCOL_v6.1.md`.

## 2. Défauts mesurés (v6) et changements gelés

### (a) L7a dégénère sous n = 75
Diagnostic de bruit = 5 bins × ≥ 15 points (code lignes ~4118–4154) → Hurst
échoue → `variance_proxy_score` NaN → `csd_ranking` que des NaN (lignes
~7549–7557, `float(...)` sans garde) → `level_risk` : `top_csd =
float(csd[0][1])` sans garde (lignes ~8943–8948) → risque NaN, niveau « low »,
confiance NaN → `level_coherence_universal` (ligne 10973) : poids L4 NaN →
votes NaN → `raw_total` NaN → le retour `indeterminate` existant n'est pas
atteint → `max()` retourne « up » par accident, confiance repliée à 0,50.
Le « up » des petits runs v6 est un **faux vote**.

- **C1 — garde `top_csd`** : `_sf(..., 0.0)` (helper `_sf` ligne 8447, déjà
  utilisé pour `avg_proxy`).
- **C2 — garde `csd` du Monte-Carlo** : `_sf(..., 0.50)` (lignes ~10435–10439).
- **C3 — gardes des 4 poids de vote L7a + incrément magnitude** (`_sf(..., 0.0)`) :
  quand tous les poids sont nuls/non finis, le retour existant `indeterminate` /
  confiance 0,0 se déclenche — jamais « up » par accident.

### (b) Séries courtes bloquées
Porte `run_pipeline` (lignes ~6761–6769) `min_required = max(20, min(min_len,
w_size))` ; fast min_len 50 → 50 points minimum. DepMap 45 lignes échouait
en 4 s : « Série trop courte : 45 points valides. Au moins 50 sont requis ».

- **C4 — min_len fast 50 → 40.** Justification : cible 45 lignées, marge 5 ;
  40 = seuil déjà utilisé comme bascule par Higuchi (`if n_s < 40`) ; scan
  bloque `w_size` à `n//2` = 22 à n = 45 → 24 fenêtres ; autres planchers ≤ 20 ;
  seuls fast change, autres modes inchangés ; diagnostic de bruit reste
  dégénéré sous n = 75, désormais gardé (pas réparé).

### (c) Discrimination faible — ÉTUDE seulement
Aucun changement de code dans v6.1. Protocole séparé :
`PROTOCOL_phase2_discrimination.md`.

- **C5 — VERSION_MASTER** `v6.1.0-L7aL7b-CohenD-short` + note d'en-tête.

**Ne changent pas :** estimateurs, autres modes, cascade, seuils, Cohen-d,
chemin predict/MC (`min_len=50` codé en dur dans
`_evaluate_predictive_mc_complexity_paths` — hors scope, dégradation
gracieuse par NaN).

## 3. Validation — 10 runs fast, tous exit 0

Lanceur `run_v6.1_validation.sh`, log `runs_v61_validation.log`,
extracteur `extract_v61_validation.py`, sorties `results_fast_v61_*`.
Contrôle = step, cible = première colonne. Fin du lot : 2026-11-16T23:20:09Z.

| Série | Cascade v6.1 (T_-2/T_-1/T_0/T_+1/T_+2 %) | v6 | L7a v6.1 | L7a v6 | Delta | MC opt / best |
|---|---|---|---|---|---|---|
| HP35 réel (n=1000) | 0,00 / 1,55 / 9,08 / 37,78 / 37,78 | **identique** (0/16/90/376) | up 0,382 | up 0,377 | 4,48 | 6,62 / 0,6035 |
| HP35 nul | 0,00 / 20,60 / 27,41 / 73,70 / 73,70 | **identique** | up 0,338 | up 0,337 | 4,57 | 4,91 / 0,4086 |
| TCGA v4 réel (n=178) | 0,00 / 74,06 / 93,22 / 98,44 / 98,96 | **identique** | **DOWN 0,405** (down 0,858) | DOWN 0,408 (0,863) | 4,18 | 10,87 / 0,3720 |
| TCGA v4 nul | 0,00 / 10,65 / 15,96 / 67,12 / 67,12 | **identique** | up 0,167 | up 0,167 | 3,77 | 81,52 / 0,3268 |
| GSE62452 réel (n=69) | 1,42 / 35,67 / 95,64 / 98,64 / 100,00 | identique | **down 0,197** (probs finies) | up 0,500 **NaN** | 1,41 | 18,18 / 0,3454 |
| GSE62452 nul | 0,00 / 12,82 / 17,10 / 21,37 / 21,37 | — | down 0,336 | — | 1,26 | 51,35 / 0,3485 |
| ICGC réel (n=70) | 1,41 / 9,84 / 52,31 / 94,27 / 94,27 | identique | up 0,181 (probs finies) | up 0,500 **NaN** | 1,44 | 70,59 / 0,3600 |
| ICGC nul | 0,00 / 28,12 / 32,43 / 36,54 / 49,10 | — | down 0,350 | — | 1,37 | 79,41 / 0,3450 |
| **DepMap réel (n=45)** | 0,00 / 1,40 / 4,40 / 11,01 / 26,42 | **jamais tourné en v6 (bloqué)** | down 0,196 | — | 1,93 | 57,14 / 0,3615 |
| **DepMap nul** | 0,00 / 13,21 / 17,61 / 26,42 / 26,42 | — | up 0,345 | — | 1,69 | 60,87 / 0,3499 |

**Critères d'acceptation (écrits avant les runs) : tous tenus.**
HP35 réel/nul et TCGA v4 réel/nul : cascades identiques à v6, bit pour bit sur
les positions. GSE62452 et ICGC : plus de faux « up » / 0,50 — les votes sont
désormais finis et honnêtes (confiances 0,18–0,35, faibles). DepMap réel + nul :
exit 0 — le bras CRISPR tourne pour la première fois.

**Falsification TCGA v4 v6.1 :** delta_vs_null 0,849386, status ok — identique
à v6. Sur les séries courtes (n < 75), la falsification est **indisponible**
(« comparaison impossible sans les deux dimensions » : la dimension spectrale
vient du diagnostic de bruit, dégénéré) — limite connue, pas un échec du run.

## 4. Bras CRISPR DepMap — première lecture par le pipeline (v6.1)

- **Flux :** `pdac_depmap_fluxes.csv` (SHA `7d605fef…`), 45 lignées adéno,
  12 gènes (top 12 par Chronos médian pancréas vs autres, hors KRAS : EFR3A,
  RAB10, CCND1, UROD, CFLAR, DOCK5, MYH9, SCAP, RAB6A, CRKL, MYC, ACO2),
  ordre = Chronos KRAS croissant (KRAS = axe, jamais un flux) ; nul
  `pdac_depmap_fluxes_nul.csv` (SHA `ac2e0db5…`, lignes permutées graine 42).
  Source : DepMap CRISPR 24Q4 (figshare 27993248), `CRISPRGeneEffect.csv`
  SHA `3d8f3ec6…`, `Model.csv` SHA `b7a0c138…`.
- **Cascade réelle :** 0,00 / 1,40 / 4,40 / 11,01 / 26,42 % → pas 0 / 1 / 2 / 5 / 12.
  **Cascade nulle :** 0,00 / 13,21 / 17,61 / 26,42 / 26,42 % → pas 0 / 6 / 8 / 12 / 12.
- **Lecture par flux** (`per_flux_reading.py`, z-score global, fenêtres ±10,
  d de Cohen ; méthode propre à ce script, ne pas comparer chiffre à chiffre
  aux lectures du 15 nov.) :
  - Pas 2 (T_0) : fenêtre avant = 2 points seulement — EFR3A z −1,91,
    CCND1 −1,56, UROD −1,31 : les 2 lignées les plus KRAS-dépendantes ont des
    Chronos très négatifs pour ces gènes. Fragile (n = 2 avant).
  - Pas 5 : RAB10 d +1,12, DOCK5 +1,13, SCAP −1,70, CFLAR −1,04.
  - Pas 12 : SCAP −1,77, le reste |d| ≤ 0,61.
  - Top-12 (premières lignes = plus dépendantes) contre reste : DOCK5 −1,03,
    SCAP +0,88, CFLAR −0,74, CRKL −0,67, CCND1 −0,56 — effets modérés,
    signes mêlés, aucun gène dominant.
- **Verdict honnête : le pipeline ne sépare PAS DepMap réel et nul.**
  Les deux cascades tombent tôt dans la série (T_+2 à 26,42 % dans les deux) ;
  MC best_score 0,3615 contre 0,3499 (quasi identiques) ; Delta 1,93 contre
  1,69 ; max_separation 0,4436 contre 0,2532 ; L7a down 0,196 contre up 0,345
  (deux votes faibles). Le T_0 réel (pas 2) est plus tôt que le nul (pas 8),
  mais avec une fenêtre avant de 2 points, ce n'est pas une preuve — c'est
  l'effet de 1–2 lignées extrêmes. Cohérent avec le test direct du 15 nov. :
  dépendances CRISPR des 12 gènes |rho| ≤ 0,23 — marqueurs, pas vulnérabilités.
  La falsification est indisponible à n = 45 (voir §3).

## 5. Découverte d'instrument — gigue L5 (à consigner, pas un défaut v6.1)

Les alertes L5 sont non déterministes d'un run à l'autre **par construction** :
`level_complexity` graine les chemins MC avec `int(seed) + (hash(metric) % 1000)`
et le hachage Python des chaînes est aléatoire par processus (vérifié :
`hash('PersistentHomology') % 1000` = 14 puis 133 dans deux processus).
Sur HP35, l'alerte PersistentHomology (0,559 en v6) disparaît en v6.1 →
L4 risque 0,84 → 0,91, L7a conf 0,377 → 0,382. La cascade et Delta sont
déterministes ; L4/L7a portent une gigue de l'ordre de ±0,07 sur HP35
(v5.9.0f → v6 montrait déjà une gigue de mean_alert 0,7687 contre 0,7783
avec le même code L5).
**Piste future v6.2 (hors scope v6.1, à proposer seulement) :** remplacer
`hash(metric)` par un hachage stable (ex. `hashlib.sha256`).

## 6. Limites connues de v6.1

- Diagnostic de bruit dégénéré sous n = 75 (0/12 complet à n = 45–70) :
  L4 risque = 0,000 (repli gardé, honnête), falsification indisponible.
- `min_len=50` codé en dur dans le chemin predict/MC — hors scope, dégradation
  gracieuse par NaN (pas d'erreur).
- Gigue L5 (±~0,07 sur L4 HP35) — voir §5.
- w_size bloqué à n//2 sur séries courtes (22 à n = 45) → 24 fenêtres de scan.

## 7. Fichiers

- `~/workspace/runs/pdac-v6/PROTOCOL_v6.1.md` (conception gelée)
- `~/workspace/runs/pdac-v6/build_v6.1.py` (construction, 10 remplacements)
- `~/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py` (copie, SHA ci-dessus)
- `~/workspace/runs/pdac-v6/run_v6.1_validation.sh`, `runs_v61_validation.log`,
  `extract_v61_validation.py`, `results_fast_v61_*` (10 sorties)
- `~/workspace/runs/pdac-v6/per_flux_reading.py` (lecture par flux, méthode documentée)
- Lots en cours (lancés 16 nov. 18h23) : `manifest_v61_extended.txt` (44 runs),
  `manifest_v61_rotations.txt` (96 runs), lanceur reprenable `run_v61_lot.sh`,
  logs `runs_v61_extended.log`, `runs_v61_rotations.log`.
