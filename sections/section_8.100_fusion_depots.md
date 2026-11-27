### 8.100 Fusion des cinq dépôts en un dépôt unique, archivage des trois anciens dépôts et smoke-test de bascule (27 novembre 2026)

Chantier d'archive, pas chantier de mesure : aucun run pipeline,
aucune modification du pipeline, aucune donnée nouvelle, aucun
verdict sur le cancer. Le 27 novembre 2026, les cinq dépôts du
projet ont été fusionnés en un dépôt unique,
`FindPrint/tlogNext-cancer-pdac` (PUBLIC), tête finale
`0aaf7116a43d37cfafe5be883e9d6cb343935ea7`, en 7 commits ; les
trois anciens dépôts (suite, actions, repro) ont été archivés
le même jour, jamais supprimés ; un smoke-test déclenché sur
la tête fusionnée a reproduit les scores de décision du local
à l'identique. Le livre blanc sur disque (26 794 lignes,
SHA `bf80f029…`) n'a pas été poussé dans ce chantier : il sort
au prochain lot.

## Verdict d'abord

**La fusion est terminée et vérifiée.** MANIFEST régénéré :
1 718 entrées, distant = local bit à bit (SHA-256 `309008e0…`) ;
60/60 nouveaux chemins vérifiés par blob SHA, 0 écart ; les
9 écarts MANIFEST d'origine sont élucidés un par un ; le
fichier `data_flux/test_biophysique_input.csv`
(SHA `6b656540…`), absent de l'arbre principal, a été retrouvé
et ajouté — sans lui les jobs HP35 auraient échoué le contrôle
SHA. Les trois anciens dépôts sont archivés (`archived:true`
vérifié par API sur les trois), jamais supprimés, en lecture
seule. Le smoke-test de bascule (run GitHub nº 1,
ID 46014415035, 8 min 11 s, Success) donne des scores de
décision EXACTEMENT identiques au local : cascade, `maxsep`
0,46234232096887146 / 0,1695801283296793, MC 0,372047 /
0,326773, falsification 0,849386 / 0,642205, seuils
10,869565217391305 / 81,52173913043478, L7a DOWN des deux
côtés. Seule nouveauté par rapport au test du 22 novembre :
Delta 4,187035 (GitHub Actions) contre 4,181387 (local),
+0,14 %, gigue de plateforme, sans effet sur aucun verdict.

## 8.100.1 — Décisions de Zackary (27 nov. 2026, 08h47) et décisions du parent

Les décisions de Zackary, dans ses mots, appliquées telles
quelles :

1. Anciens dépôts GARDÉS, ARCHIVÉS si possible, JAMAIS
   supprimés — suite, actions et repro archivés après la
   fusion (voir §8.100.4) ; `Code` NON archivé, dépôt
   généraliste vivant.
2. Données des workflows : `data_flux/` (pas de dossier
   `data/` dupliqué).
3. Protocoles `PROTOCOL_v6.1.md` et `PROTOCOL_v6.2.md` À LA
   RACINE du dépôt unique (« racine du dépôt si possible »).
4. `pdf-build/` À LA RACINE.
5. VERSION EN ANGLAISE demandée : `README_EN.md` à la racine
   + lien visible en tête du README français (voir §8.100.6).
   La traduction du livre blanc entier (1 474 pages) est une
   piste future, pas dans ce lot.
6. Archiver actions et repro aussi, avec README de
   redirection.

Le reste a été décidé par le parent (coordinateur) :

- Périmètre repro : `rapports/` + `docs/` + `pdf-build/` +
  uniques repro (scripts/results/provenance après déduplication
  SHA) ; `STATUS.md` NON fusionné.
- Coupure de l'historique des runs Actions acceptée + mention
  du dépôt actions archivé (URL) dans le README.
- `pipeline_autonome_v3_3_harmonic_v1.py` laissé où il est,
  NON rapatrié.
- `SOURCES_CANDIDATES.tsv` versé sous `provenance/`
  (registre unique, 1 304 o) — décision du coordinateur,
  réversible en une ligne.

Têtes avant fusion, vérifiées le 27 novembre 2026 (API +
connecteur) : principal `48b9e69f` (27 nov. 13:36:38 UTC),
suite `14bff2ff` (27 nov. 13:39:19 UTC), actions `0dba356`
(23 nov. 11:59:12 UTC), repro `8c88810b`
(18 nov. 23:06:52 UTC), Code `1ef321a`
(27 nov. 12:28:43 UTC).

## 8.100.2 — Les 7 commits de fusion (tête finale `0aaf7116`)

| Commit | Contenu | Fichiers | Octets |
|---|---|---|---|
| 1 — `69d6a561` | v6.0 + v6.1 à la racine | 2 | 1 246 021 |
| 2 — `f43d4f0` / `efaf456` / `4222803` / `83f378a` | `.github/workflows/` (4 YAML adaptés `data_flux/`) | 4 | 17 212 |
| 3 — `53d0053e` | `PROTOCOL_v6.1.md` + `PROTOCOL_v6.2.md` à la racine | 2 | 45 649 |
| 4 — `e381b80b` | `rapports/` + `docs/` + `pdf-build/` + `scripts/` uniques repro | 26 | 333 725 |
| 5 — `152e918a` | `results/` gros repro (CRISPR + 2 PRISM) | 3 | 3 768 465 |
| 6 — `a34f09d4` | `results/` reste repro (19) + `data_flux/test_biophysique_input.csv` + `provenance/SOURCES_CANDIDATES.tsv` | 21 | 789 587 |
| 7 — `0aaf7116` | MANIFEST régénéré (1 718 entrées) + README.md + README_EN.md | 3 | 242 908 |

Tête finale : `0aaf7116a43d37cfafe5be883e9d6cb343935ea7`.
Total préparé : 60 fichiers (59 nouveaux chemins + README.md
mis à jour), 6 262 045 o. Tous les commits sont < 4 Mo.

Le commit 2 mérite une note : les 4 workflows ont été créés
via le navigateur, car l'API GitHub refuse les fichiers de
workflows à l'App (403 « Resource not accessible by
integration ») — 4 commits navigateur `f43d4f0`, `efaf456`,
`4222803`, `83f378a`, tête intermédiaire
`83f378a5dfff56cc05218869f94bc2b84a7d85cf`. Les YAML adaptés
ont été vérifiés : 18 occurrences `data_flux/`, 0 `data/`,
0 `actions-test`.

v6.2 à la racine N'A PAS été re-poussé : il y était déjà,
SHA `f07567c4…`, vérifié. v6.0 (SHA `bb8bbdba…`) et v6.1
(SHA `2af5e5ce…`) sont à la racine depuis le commit 1.

Déduplication repro : 223 candidats, 48 uniques
(4 799 757 o), 175 doublons (82 changent de préfixe
`results/` → `data_flux/`, contenu identique). 0 collision
entre les 48 uniques et les 7 fichiers hors MANIFEST
(vérifié). 0 fichier non UTF-8 parmi les 223.

## 8.100.3 — Vérifications

- **MANIFEST régénéré : 1 718 entrées** (1 651 + 8
  réconciliés + 59 nouveaux). Distant = local bit à bit,
  SHA-256 `309008e0…`.
- **60/60 nouveaux chemins vérifiés par blob SHA, 0 écart.**
  Chaque SHA a été re-calculé depuis le staging ; le tableau
  maître fichier → destination → SHA est consigné dans
  `tableau_fusion_20261127.md` (SHA `0a3eb186…`) et
  `.csv` (SHA `527998df…`).
- **Écarts MANIFEST élucidés.** Arbre principal à `48b9e69f` :
  1 666 entrées (1 660 blobs + 6 arbres) ; MANIFEST : 1 651.
  9 fichiers dans l'arbre mais absents du MANIFEST :
  `LICENSE`, `MANIFEST_SHA256.txt` lui-même (auto-référence
  impossible — écart structurel attendu), 2 JSON `data_flux/`
  (`v62_delta_magnitudes.json`, `v62_validation_table.json`),
  5 fichiers `results/` v62 (`ssep_841_rotations.json`,
  `v62_delta_elucidation.md`, `v62_delta_magnitudes.md`,
  `v62_phase2_table.md`, `v62_validation_table.md`).
  0 fichier dans le sens inverse. Cause : ajouts postérieurs
  non repris dans le MANIFEST ; contenu vérifié bit à bit.
  4 SHA partagés par 2 chemins dans le MANIFEST (état
  préexistant, non modifié).
- **Point majeur résolu : `test_biophysique_input.csv`.**
  Le CSV réel HP35 (`data_flux/test_biophysique_input.csv`,
  SHA `6b656540598579a37cbc97c9dfbee26bf6186611f84f397cf9e7e6f1e88bb35e`,
  90 716 o) était ABSENT de l'arbre principal (seuls ses
  10 nuls s9101–s9110 y sont). Les workflows E1 + rerun le
  référencent avec `real_sha 6b656540…` : sans ce fichier,
  les jobs HP35 auraient échoué le contrôle SHA. Il a été
  ajouté au commit 6 (copie locale depuis actions @
  `0dba356`, SHA re-vérifié). Les 10 autres CSV E1/E2 sont
  présents et leurs SHA MANIFEST concordent 10/10 avec les
  `real_sha` des YAML.
- **README FR reconstruit chirurgicalement** (remplacements
  exacts sur le distant, pas de reformatage global) ; ligne
  de dette périmée §8.98 corrigée (« 203 des 209… à
  refaire » → « Dette SHA soldée 209/209 ») ; compteurs
  Structure mis à jour après fusion (results 215, scripts
  272, data_flux 989, provenance 136).

## 8.100.4 — Archivage des trois anciens dépôts (27 nov. 2026)

| Dépôt | Tête au moment de l'archivage | Statut vérifié |
|---|---|---|
| `FindPrint/tlogNext-cancer-pdac-suite` | `f2bfdf31` (README de redirection) | `archived:true` par API |
| `FindPrint/tlogNext-pipeline-actions` | `111b1e66` | `archived:true` par API |
| `FindPrint/pancreatic-cancer-open-data-reproducibility` | `a7a98d43` | `archived:true` par API |

Archivés, jamais supprimés, en lecture seule. `Code` n'est
pas archivé : dépôt généraliste vivant, tête `1ef321a`.
`tlogNext-pdac-phase2` (autre IA) n'a jamais été touché ;
`universal-log-research` n'a jamais été touché ; Kaggle
n'a jamais été touché dans ce chantier.

## 8.100.5 — Smoke-test de bascule : le dépôt unique fonctionne de bout en bout

Run GitHub Actions : `pipeline-smoke-test` nº 1,
ID 46014415035, 27 nov. 2026 09:16 HNE, 8 min 11 s, statut
Success, sur la tête fusionnée `0aaf7116`. Artefact
`master-results-tcga-v4.zip`, 2 100 650 o, SHA-256
`7b44f33198432152f897631d303124c0a75e9ad5445f019bde45dc12d29b50e4`
(vérifié). Références locales :
`runs/pdac-v6/results_fast_v62_tcga_v4[_nul]/master_results.json`.

Scores de décision — EXACTEMENT identiques (bit à bit) :

- Cascade réelle : 0 / 74,0617 / 93,2217 / 98,4358 /
  98,9572 — identique ; cascade nul identique.
- `maxsep` : 0,46234232096887146 (réel) /
  0,1695801283296793 (nul) — identiques.
- MC calculé (0,3·s_norm + 0,3·stabilité + 0,2·robustesse
  + 0,2·sharpness) : 0,372047 / 0,326773 — identiques.
- Falsification delta_vs_null : 0,849386 / 0,642205 —
  identiques.
- Seuils best_config : 10,869565217391305 /
  81,52173913043478 — identiques.
- best_config : 0 différence ; scan curves (default + raw
  MC) : 0 différence.
- L7a : direction DOWN des deux côtés (réel + nul,
  7 horizons) ; confiance globale 0,403955 (GitHub Actions)
  contre 0,405191 (local), écart 0,3 % ; L7_consensus :
  4–5 clés différentes.

Différences nommées (aucune ne porte un verdict) :

- **Delta (holographique) : réel 4,187035 (GitHub Actions)
  contre 4,181387 (local), +0,14 % ; nul 3,765445 contre
  3,765664.** Le 22 novembre, Delta était identique des
  deux côtés (4,181387). Écart réel−nul préservé : 0,4216
  (GitHub Actions) contre 0,4157 (local). Cause : gigue de
  plateforme (tirages MC / tests de permutation) — les
  entrées sont vérifiées par SHA par le workflow lui-même,
  le code est identique. Référence run-à-run : deux runs
  locaux entre eux ne diffèrent que de 10 clés — le
  pipeline est déterministe en local, mais les tirages
  MC/permutations ne se reproduisent pas bit à bit entre
  machines.
- Sections MC-complexité et diagnostics de bruit : quelques
  milliers de feuilles différentes sur ~204 000 (comparaison
  feuille par feuille, égalité exacte). Exemples :
  MultifractalDeltaAlpha std 0,390 contre 0,342 ;
  corr_after (permutation) 0,125 contre 0,109 ; une moyenne
  DFA isolée (CEACAM5, Q1) 0,769 contre 0,248. La plupart
  des autres feuilles diffèrent à 1e-14/1e-15 près (bruit
  flottant).
- Environnement : mémoire 15,6 Go (runner) contre 2 Go
  (local) ; plotly absent sur le runner (tableau HTML de
  secours) ; avertissement Node.js 20 déprécié
  (actions/checkout@v4, setup-python@v5, upload-artifact@v4
  forcées sur Node 24), sans échec.

Lecture : SUCCÈS — la bascule est validée : le dépôt unique
fonctionne de bout en bout (workflows + `data_flux/` +
v6.2), tous les scores de décision sont identiques. La seule
nouveauté par rapport au test du 22 novembre est la gigue
de Delta (+0,14 %), sans effet sur aucun verdict (Delta
n'est pas élucidé et ne porte aucun verdict).

## 8.100.6 — `README_EN.md` : la version anglaise demandée

`README_EN.md` à la racine du dépôt unique, SHA-256
`8815e25005705a989c9c2061187a4d5ac156f3ad8618e6e1e9dcbbb506ef683f`,
30 733 o, ajouté au commit 7. Lien en tête du README
français (ligne 3). Avertissement médical en tête, comme
le README français. Chiffres MTAP/PRMT5 vérifiés contre le
livre blanc (§8.28–§8.50 : −1,385 contre −1,010,
p=0,0036 ; CDKN2A fixé p=0,76). La traduction du livre
blanc entier reste une piste future, non commencée.

## 8.100.7 — Ce que la fusion dit, et ce qu'elle ne dit pas ; limites et dettes

Ce chantier ne dit rien sur le cancer : il dit que
l'archive est désormais unique, vérifiée et fonctionnelle.
Les verdicts scientifiques du dossier (§8.1–§8.99) sont
inchangés ; aucun n'a été rouvert, recalculé ou réinterprété
ici. La question §8.12 (Cox) reste close par §8.99 ;
`check_cox_tcga.py` est un doublon (déjà dans le principal,
SHA `5aa4548a…`), non rapatrié — le script importe depuis un
chemin absolu local (`/home/hatch/workspace/runs/pdac-v6`),
non portable, consigné.

Dettes nommées, non soldées dans ce chantier :

- **Kicker de couverture du PDF** (« 19–22 novembre 2026 »)
  doit passer au 27 nov. 2026 à la prochaine construction
  du PDF — c'est le parent qui construit le PDF, pas ce
  chantier.
- **Traduction du livre blanc entier en anglais** : piste
  future, non commencée (seul le README est traduit).
- **`LICENSE_OR_DATA_NOTICES.md`** (repro, 1 896 o) : non
  fusionné, non téléchargé ni comparé ; il reste dans le
  dépôt repro archivé.
- **Dette d'archive Cox soldée dans ce chantier :**
  `check_cox_tcga_results.txt` (68 lignes) contient le bloc
  pré-correction buggué (MUC16 1,58). Le contenu d'origine
  n'a pas été effacé : un encadré daté du 27 nov. 2026 a été
  ajouté en tête, expliquant que le bloc pré-correction est
  buggué, que les valeurs correctes sont celles du §8.12
  (addendum du 27 nov.) reproduites par 3 implémentations
  (`survival_tcga_recalc_20261127_results.txt`,
  SHA `fa5cff07…`), et que le script d'origine du 15 nov.
  est introuvable. SHA du fichier avant annotation
  `c50fb788…26bf8`, après annotation consigné dans
  `PROVENANCE_8100.md`.
- **Consolidation GSE184585 à 200 nuls** : toujours non
  faite, nommée comme suite (§8.99.7).
- Le livre blanc sur disque après ce chantier (26 794
  lignes, SHA `bf80f029…`) n'est pas poussé : il sort au
  prochain lot, avec cette section.

## 8.100.8 — Provenance

- **Sources de ce chantier :** `PROVENANCE_8100.md`
  (provenance complète : les 5 dépôts, têtes avant/après
  fusion, URLs, hachages, ce qui manque).
- **État de la fusion :**
  `coordinateur_fusion_20261127_etat.md` ; tableau maître
  `tableau_fusion_20261127.md` (SHA `0a3eb186…`) et
  `.csv` (SHA `527998df…`) ; scripts de construction
  `build_fusion_snapshots.py` (SHA `9f8ac261…`),
  `generate_tableau_fusion.py` (SHA `3e062e9c…`),
  `rebuild_readme_fr_20261127.py` (SHA `03de66f2…`).
- **Smoke-test :**
  `COMPARAISON_SMOKE_FUSION_20261127.md`, artefact
  `master-results-tcga-v4.zip` (SHA `7b44f331…50e4`),
  script de comparaison `compare_smoke_fusion.py`.
- **Dépôt unique :**
  `https://github.com/FindPrint/tlogNext-cancer-pdac`,
  tête `0aaf7116a43d37cfafe5be883e9d6cb343935ea7`.
  Anciens dépôts archivés :
  `https://github.com/FindPrint/tlogNext-cancer-pdac-suite`
  (tête `f2bfdf31`),
  `https://github.com/FindPrint/tlogNext-pipeline-actions`
  (tête `111b1e66`),
  `https://github.com/FindPrint/pancreatic-cancer-open-data-reproducibility`
  (tête `a7a98d43`).
- **Code :** v6.0 SHA `bb8bbdba…`, v6.1 SHA `2af5e5ce…`,
  v6.2 SHA `f07567c4…` — inchangés, jamais modifiés dans
  ce chantier.
- **Aucun run pipeline, aucun PDF, aucun push, aucune
  Release dans ce chantier.** `tlogNext-pdac-phase2`,
  `universal-log-research` et Kaggle jamais touchés.

## Ligne §7

| 106 | 27 nov. 2026 | **Fusion des cinq dépôts en un dépôt unique, archivage des trois anciens dépôts et smoke-test de bascule (§8.100)** (décisions de Zackary 27 nov. 08h47 : anciens dépôts gardés, archivés si possible, jamais supprimés — suite, actions, repro archivés, Code non archivé ; protocoles et `pdf-build/` à la racine ; `README_EN.md` à la racine + lien en tête du README FR, traduction du livre blanc entier piste future ; 7 commits, tête finale `0aaf7116a43d37cfafe5be883e9d6cb343935ea7` — v6.0+v6.1 à la racine `69d6a561`, 4 workflows via le navigateur (API GitHub refuse les workflows à l'App, 403) `f43d4f0`/`efaf456`/`4222803`/`83f378a`, protocoles `53d0053e`, rapports/docs/pdf-build/scripts `e381b80b`, résultats gros repro `152e918a`, reste repro + `test_biophysique_input.csv` retrouvé `a34f09d4`, MANIFEST + README + README_EN `0aaf7116` ; MANIFEST régénéré 1 718 entrées, distant = local bit à bit SHA `309008e0…`, 60/60 chemins vérifiés par blob SHA, 0 écart, 9 écarts MANIFEST élucidés ; archivage vérifié par API `archived:true` sur les 3 dépôts, jamais supprimés ; smoke-test run GitHub nº 1 ID 46014415035, 8 min 11 s, Success sur `0aaf7116` — scores de décision EXACTEMENT identiques au local : cascade, `maxsep` 0,46234232096887146 / 0,1695801283296793, MC 0,372047 / 0,326773, falsification 0,849386 / 0,642205, seuils, L7a DOWN des deux côtés ; seule nouveauté vs 22 nov. : Delta 4,187035 contre 4,181387, +0,14 %, gigue de plateforme, sans effet sur aucun verdict ; `README_EN.md` SHA `8815e250…`, 30 733 o ; kicker PDF à passer au 27 nov. 2026 à la prochaine construction ; dette Cox annotée dans `check_cox_tcga_results.txt` ; aucun run pipeline, aucun PDF, aucun push, aucune Release dans ce chantier). Détail au §8.100. |

— Fin de la §8.100. —
