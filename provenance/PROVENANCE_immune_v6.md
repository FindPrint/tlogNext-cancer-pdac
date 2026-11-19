# Provenance — paysage immunitaire le long de l'axe KRAS (Bras 1, v6)

Date : 16 novembre 2026. Protocole gelé avant les runs. Pipeline v6 privé
(règle permanente) ; ce fichier et le rapport sont publics, le code du
pipeline ne l'est pas.

## 1. Question

Le paysage immunitaire change-t-il le long de l'axe KRAS dans le PDAC ?
12 gènes immunitaires, 4 cohortes, ordre = expression KRAS brute croissante.

## 2. Pipeline

- Fichier : `~/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py`
- SHA-256 vérifié avant lancement :
  `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`
  (conforme à l'attendu). Fichier jamais modifié.
- Mode : fast, cohen_d partout. Invocation (retrouvée dans
  `run_icgc_v6.sh` / `run_geo62452_v6.sh`) :
  `python3 $V6 --input <csv> --mode fast --output results_fast_<nom>`,
  lancée depuis `~/workspace/runs/pdac-v6/`.
- Script de lancement : `run_immune_v6.sh`, log `runs_immune_v6.log`.
- 8 runs séquentiels : réel + nul × 4 cohortes.
- Note de contention : un autre bras (PARP, `pdac_tcga_fluxes_parp.csv`)
  tournait en parallèle sur la même VM (2 vCPU, 7,7 Go RAM) pendant ces
  runs — chaque run a duré plus longtemps que les ~4 min habituelles.
  La contention ralentit, elle ne change pas les sorties (mêmes entrées,
  même code, mêmes graines côté pipeline).

## 3. Sources (déjà sur disque, rien re-téléchargé)

| Cohorte | Fichier matrice | Hachage vérifié |
|---|---|---|
| TCGA PAAD | `data/tcga_paad_rsem.tar.gz` | MD5 `b09569ce3f4721f514bc137bd109ac0a` (conforme) |
| GSE71729 | `data/GSE71729_series_matrix.txt.gz` | SHA-256 `b228789314ec4d866ec51b65724664abaa24b822577c55d3727820c867536a54` (conforme) |
| GSE62452 | `data/GSE62452_series_matrix.txt.gz` | SHA-256 `8f41d5b3f11451e653fd6bfc0c6b216c219d46711a7676d1e453dee16a078cba` (conforme) |
| ICGC PACA-AU | `data/icgc_pacaau_exp.txt.gz` | SHA-256 `c2cb57af3ba4c3d7fdac292e66c81067d36e16aae9efdd8005147e20820f49fa` (conforme) |

Détail des sources : TCGA Firehose PAAD, log2(RSEM+1) ; GEO GSE71729,
plateforme GPL20769 (symboles directs) ; GEO GSE62452, plateforme GPL6244
(mapping `data/GPL6244_probe2symbol.tsv`, médiane par symbole) ; ICGC
PACA-AU, UCSC Xena `nature16965-s2_normalised_exp.txt`, log2(cpm),
mapping Ensembl→symbole `data/icgc_pacaau_probemap.gz`, clinique Bailey
et al. 2016 Suppl. Table 1. Voir aussi `PROVENANCE_tcga.md`,
`PROVENANCE_geo71729.md`, `PROVENANCE_geo62452.md`, `PROVENANCE_icgc.md`.

## 4. Construction des flux

Script : `build_fluxes_immune.py` (log `immune_build.log`,
résumé `immune_build_summary.json`).

- Flux : CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274 (PD-L1), PDCD1 (PD-1),
  CTLA4, GZMB, IFNG, CD19. Aucune imputation ; cas complets seulement ;
  règle ≥ 50 valeurs valides par gène (tenue partout : 178/178, 145/145,
  69/69, 70/70 cas complets).
- Ordre : KRAS BRUT croissant, même axe partout. Différence documentée
  avec la v4 TCGA : la v4 ordonnait par le résidu KRAS corrigé de la
  pureté ; ici KRAS brut, pour être comparable aux cohortes GEO/ICGC
  (aucune correction de pureté nulle part dans ce bras). Conséquence :
  la composition tissulaire (pureté) n'est pas retirée ici — une baisse
  d'un marqueur T peut refléter moins de lymphocytes infiltrants, une
  cellularité tumorale plus haute, ou les deux ; le rapport le dit.
- Échantillons : TCGA 178 tumeurs (code barre positions 13:15 = "01") ;
  GSE71729 145 tumeurs primaires (sur 357 échantillons) ; GSE62452 69
  tumeurs (sur 130) ; ICGC 70 tumeurs primaires PDAC (Sample type =
  "Primary tumour" ET HistoSubtype = "Pancreatic Ductal Adenocarcinoma",
  sur 96 échantillons).
- Symboles dupliqués : agrégation par médiane (GSE71729, GSE62452, ICGC),
  comme dans les scripts précédents.
- Format CSV : identique aux CSV existants — colonne `step` 0..n-1, puis
  les 12 flux, lignes ordonnées par KRAS croissant, `index=False`.
- Nul : mêmes lignes permutées, graine 42 (rng frais par fichier).
- Fichier d'axe joint : `immune_kras_order_<cohorte>.csv` (step,
  échantillon, valeur KRAS brute) — KRAS n'est pas un flux, il n'apparaît
  pas dans le CSV de flux ; ce fichier rend les tests directs
  reproductibles.

### Remplacements (ICGC seulement)

- IFNG absent de la matrice ICGC → remplacé par PRF1 (règle du protocole :
  remplaçant nommé ; PRF1 = effecteur cytotoxique, voisin fonctionnel de
  IFNG/GZMB).
- CD19 absent AUSSI de la matrice ICGC → remplacé par MS4A1 (CD20),
  marqueur de la lignée B comme CD19. ÉCART DOCUMENTÉ au protocole : le
  protocole ne nommait qu'un seul remplaçant (PRF1) ; deux absences
  exigent un second remplaçant. Dupliquer PRF1 aurait créé deux colonnes
  identiques — méthodologiquement pire. MS4A1 suit la même logique de
  substitution par voisin fonctionnel direct.
- Les 12 gènes demandés sont présents sans remplacement dans TCGA,
  GSE71729 et GSE62452 (vérifié par sonde avant construction).

### SHA-256 des fichiers produits

| Fichier | SHA-256 |
|---|---|
| `pdac_immune_tcga_fluxes.csv` (178×13) | `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e` |
| `pdac_immune_tcga_fluxes_nul.csv` | `9100d181e3391d558eec6bc97e82f93b16c118b807b4a5f0c0992f4bda51a405` |
| `pdac_immune_geo71729_fluxes.csv` (145×13) | `8987ffcaeb9cac848bd220c2a1816f63ecbcd63e5cd68c4f698e7c3234952219` |
| `pdac_immune_geo71729_fluxes_nul.csv` | `b96b1f744db30193098e588326db33c3bca448bb87615fd011d9302e7c605fc7` |
| `pdac_immune_geo62452_fluxes.csv` (69×13) | `97c4689a6ecacd0a73a77804200a72a90994d60bea7e6b2c079195acbffd79a3` |
| `pdac_immune_geo62452_fluxes_nul.csv` | `b0496cb923d49ef4913f90b895d856e3c02a1b1b4d78a2cc11a9f198c367d3a9` |
| `pdac_immune_icgc_fluxes.csv` (70×13) | `10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc` |
| `pdac_immune_icgc_fluxes_nul.csv` | `3393ecd662e6decfa41416b535e509089cb43bd63345097fe3f25ad9b7860955` |
| `immune_kras_order_tcga.csv` | `31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d` |
| `immune_kras_order_geo71729.csv` | `2113e24c5b82303f4f808fc99a418ead53436ecbc530af0da02a623cffa76515` |
| `immune_kras_order_geo62452.csv` | `4a8549998b38021559724a08dcd5a882d170256f98d487cc45eeff3bd303c095` |
| `immune_kras_order_icgc.csv` | `67d41da9c93538e8670026bdfef0b3bddbc49df39bca3dc4d67af3101a720860` |

KRAS brut (unités propres à chaque plateforme, non comparables entre
cohortes) : TCGA min 8,570 / médiane 10,282 / max 11,727 (log2(RSEM+1)) ;
GSE71729 min 1,550 / médiane 3,278 / max 4,151 ; GSE62452 min 5,277 /
médiane 6,396 / max 7,361 ; ICGC min 5,162 / médiane 6,359 / max 7,352
(log2(cpm)).

## 5. Tests directs (verdict principal)

Script : `direct_tests_immune.py` (log `immune_direct_tests_run.log`).
Sorties : `immune_direct_tests.csv`, `immune_direct_tests.txt`.

- Spearman rho de chaque gène contre KRAS brut (p bilatérale).
- Top-12 KRAS-fort contre reste : d de Cohen (différence des moyennes /
  SD poolée) + test t de Welch (p bilatérale). n_top = 12 partout.
- p brutes, sans correction pour tests multiples : 48 tests
  (12 gènes × 4 cohortes) ; ~2,4 faux positifs attendus à p < 0,05 sous
  le nul. Le rapport juge la cohérence du signe entre cohortes avant
  toute p isolée.

## 6. Runs v6 (16 nov. 2026, 13h59–14h25 UTC, log `runs_immune_v6.log`)

8 runs, tous exit 0. Cible v6 = CD8A partout (première colonne numérique
hors contrôles, mode single). Extraction : `extract_immune_v6.py`,
`immune_v6_runs_summary.json`.

| Run | n | T_-2 % | T_-1 % | T_0 % | T_+1 % | T_+2 % | MC | Delta | L7a |
|---|---|---|---|---|---|---|---|---|---|
| TCGA réel | 178 | 1,60 | 29,15 | 59,91 | 75,10 | 75,10 | 0,379 | 4,21 | DOWN 18,33 % (désaccord) |
| TCGA nul | 178 | 0,00 | 2,13 | 8,52 | 35,34 | 35,34 | 0,324 | 2,30 | UP 34,29 % |
| GSE71729 réel | 145 | 0,00 | 33,38 | 92,27 | 95,49 | 99,36 | 0,344 | 2,86 | DOWN 39,46 % |
| GSE71729 nul | 145 | 2,61 | 21,10 | 38,82 | 86,48 | 86,48 | 0,324 | 2,67 | UP 16,72 % (désaccord) |
| GSE62452 réel | 69 | 7,12 | 62,58 | 66,59 | 91,29 | 92,74 | 0,369 | 1,37 | UP 50,00 % = repli NaN |
| GSE62452 nul | 69 | 0,00 | 1,27 | 4,27 | 8,55 | 46,38 | 0,348 | 1,41 | UP 50,00 % = repli NaN |
| ICGC réel | 70 | 4,22 | 25,30 | 29,52 | 33,76 | 52,31 | 0,334 | 1,50 | UP 50,00 % = repli NaN |
| ICGC nul | 70 | 0,00 | 19,68 | 23,90 | 63,02 | 72,80 | 0,368 | 1,32 | UP 50,00 % = repli NaN |

L7a à n = 69/70 : `noise_diagnostic.json` donne `status =
scores_unavailable`, `n_complete_scores = 0` (réel et nul) — le
diagnostic de bruit exige 5 bins × 15 points (≥ 75) ; le « UP 50 % »
est le repli sur NaN, pas un vote. À n = 145/178, 12 scores complets.
Sorties : `results_fast_immune_<cohorte>(_nul)/`.
Lecture : pas de séparation réel/nul propre (MC réel < nul en ICGC ;
Delta réel ≈ nul sauf TCGA) — voir `immune_v6.md` §2.

## 7. Ce qui manque / limites

- ARN total en vrac (bulk) : les marqueurs mesurent l'abondance d'un type
  cellulaire autant que l'expression par cellule. Aucune déconvolution
  (CIBERSORT, xCell) dans ce bras.
- Pas de correction de pureté (choix documenté §4) : la baisse des
  marqueurs T peut être un effet de composition.
- CD274 (PD-L1) est mesuré en ARN total, pas en protéine tumorale ni en
  score CPS/IHC — l'éligibilité immunothérapie ne se lit pas ici.
- ICGC : IFNG et CD19 remplacés (PRF1, MS4A1) — les colonnes ne sont pas
  strictement les mêmes gènes que dans les 3 autres cohortes.
- L7a : le diagnostic de bruit exige 5 bins × 15 points (≥ 75) ; à
  n = 69/70 le score est NaN — artefact connu, jamais lu comme un vote.
  À n = 145/178, L7a est calculable mais reste un vote interne, pas une
  preuve (règle du projet).
- Aucune donnée de réponse à l'immunothérapie dans ces cohortes : la
  conclusion « piste ou non » pour KRAS+immunothérapie est une lecture
  du paysage, pas un test de traitement.
