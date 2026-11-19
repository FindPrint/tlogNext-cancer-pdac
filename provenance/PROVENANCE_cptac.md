# PROVENANCE — CPTAC PDAC protéine (mission de confirmation v4)

Date : 15 novembre 2026. Auteur du traitement : TagPrint (agent de Zackary Drasse-Ménard).
Référence du projet : livre blanc PDAC v6 (`workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md`).

## 1. Source des données

- **Étude :** CPTAC PDAC — Cao et al., 2021, *Cell*, « Proteogenomic characterization of pancreatic ductal adenocarcinoma ». Étude PDC **PDC000393** (Proteomic Data Commons, NCI).
- **Voie d'accès réelle :** les fichiers ont été téléchargés depuis le miroir Zenodo du paquet Python `cptac` (PayneLab), record **8394329** (« CPTAC - first test », DOI 10.5281/zenodo.8394329), lui-même issu du PDC PDC000393. L'API GraphQL du PDC (https://pdc.cancer.gov/graphql, accès ouvert, sans authentification) a été testée et répond, mais l'exploration de son schéma (studyCatalog) était lente et l'introspection désactivée ; le miroir Zenodo contient les mêmes fichiers sources (mêmes sommes MD5 que celles du PDC). **L'accès PDC n'était pas contrôlé ni bloqué** — le miroir a été choisi pour sa simplicité, pas par nécessité. La voie de secours RPPA/cBioPortal n'a pas été nécessaire (données de spectrométrie de masse obtenues).
- **Date de téléchargement :** 15 novembre 2026, 13h48–13h49 UTC.

## 2. Fichiers téléchargés (vérifiés)

| Fichier | Taille (octets) | MD5 (Zenodo = local, exact) | SHA-256 local |
|---|---|---|---|
| `umich-pdac-proteomics-Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz` | 20 504 572 | `a8c89b796b8ddacd48609e8ca7aac676` | `336d148faa5ca48054acdb6c03c723b6da9873eaeb6b641b028390ecaaad29a5` |
| `umich-pdac-mapping-aliquot_to_patient_ID.tsv.gz` | 22 881 | `b013fad4a8f9fa26aa3915c0ef636754` | `ed16d5287a2a5121a9ad91f3b74325e0e6d6cca24dd9ff75e715ead4da5c6ddc` |
| `bcm-pdac-proteomics-PDAC_proteomics_gene_abundance_log2_reference_intensity_normalized_Tumor.txt.gz` | 7 382 441 | `988150c28a2c1db14a3c0e62d08c06d2` | `682b725cef0f2f815f6dc1b3966376450d414c30ffc2a561ca78a1211038375f` |
| `cptac_genes.csv` | 462 309 | `afc250790ed6d18a7624a38fb872f62a` | `db232c7cbf76d1791972fef41a830783a9b5db29f37ed83832648e114691b6fe` |

Tous les MD5 correspondent exactement à ceux annoncés par Zenodo (record 8394329, consulté le 15 nov. 2026). Journal de téléchargement : tailles et sommes contrôlées dans la session (aucun fichier de log séparé ; les sommes ci-dessus sont la preuve).

## 3. Nature des lignes et traitement

- **Matrice utilisée (principale) :** UMich, niveau protéine → agrégée au niveau gène. Chaque valeur est un ratio log (abondance TMT 11-plex moins l'intensité de référence du plex), c'est-à-dire une mesure instrumentale d'abondance protéique relative, pas une valeur inventée ni un mot humain.
- **Script :** `build_matrix_umich.py` — logique reprise du paquet `cptac` (UmichPdac.load_proteomics) : Index découpé (ENSP champ 0, symbole champ 6) ; suppression des colonnes métadonnées ; transposition ; soustraction de la ligne ReferenceIntensity ; suppression des QC/références/pools (ReferenceIntensity, QC1–QC6, KoreanReference1–3, Pool-24-2, WU-PDA1, WU-Pool-25) ; correspondance aliquote → patient (fichier de mapping + 8 correspondances manuelles du paquet, toutes normales `.N`) ; tumeurs = patient_ID `C3L-*` sans suffixe `.N` ; doublons patient : 0 ; agrégation au niveau gène par **médiane des isoformes** (documenté).
- **Cohorte obtenue :** 68 tumeurs, 11 419 gènes. 238 aliquotes mappées, 0 sans correspondance.
- **Flux :** `build_fluxes_cptac.py` — 7 flux (PGC, REG4, CLDN18, KRT20, CEACAM5, CLCA1, MUC16, ordre v4 ARN conservé), 63 tumeurs à données complètes, ordre = KRAS protéique croissant (KRAS = axe, jamais un flux), nul = mêmes lignes permutées (graine 42).
  - `pdac_cptac_fluxes.csv` — SHA-256 `ec45290fb2f368f6844bf65f4c08d70e7c5842067f4c05638bb758fc37c2f656`
  - `pdac_cptac_fluxes_nul.csv` — SHA-256 `9598aeef0a744d1e7fd5989257545033d61a2bd2c26ee0d601e9d9167a848051`
- **Pipeline :** v6.0.0-L7aL7b-CohenD, original intact (`workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py`, SHA `bb8bbdba…c0773`), mode fast, contrôle step. Sorties `results_fast_cptac/` et `results_fast_cptac_nul/`, log `runs_cptac_v6.log`.

## 4. Couverture des 12 gènes v4 ARN (sur 68 tumeurs UMich)

| Gène | Valides / 68 | Retenu ? |
|---|---|---|
| KRAS (axe) | 68 | oui (axe, jamais flux) |
| CLDN18 | 68 | oui |
| CEACAM5 | 68 | oui |
| PGC | 68 | oui |
| KRT20 | 68 | oui |
| CLCA1 | 68 | oui |
| REG4 | 68 | oui |
| MUC16 | 63 | oui (5 tumeurs retirées, cas complets) |
| CR2 | 44 | non (< 50) |
| MUC17 | 11 | non (< 50) |
| GSTM1 | 20 | non (< 50) |
| MUC2 | 30 | non (< 50) |
| DPCR1 | — | non (symbole ambigu, voir §5) |

## 5. Ce qui manque / limites (à ne pas cacher)

- **DPCR1 non résolu :** le symbole DPCR1 renvoie 5 ID Ensembl candidats (xrefs Ensembl) ; le premier vérifié (ENSG00000168631) est en réalité MUCL3. Aucune correspondance univoque n'a pu être vérifiée (Ensembl REST inaccessible au moment de la vérification : timeout 60 s). DPCR1 est donc listé comme manquant, pas remplacé par MUCL3.
- **5 tumeurs retirées** (sans MUC16) : rangs KRAS 13, 20, 38, 58, 61 sur 68 — réparties, pas concentrées en haut (médiane KRAS 0,16 contre 0,09 pour les autres). Pas de biais d'ordonnancement détecté.
- **68 tumeurs, pas 140 :** l'étude PDC000393 compte ~140 tumeurs au total, mais elles sont réparties entre centres : la matrice UMich en contient 68, la matrice BCM 52 (téléchargée aussi, voir §2, non utilisée pour les flux — autre centre, autre normalisation, les combiner mélangerait les échelles). Le chevauchement BCM/UMich n'a pas été établi. La confirmation porte donc sur 68 tumeurs UMich, pas sur la cohorte entière.
- **Agrégation par médiane des isoformes** : un choix de traitement (documenté §3), pas une mesure brute. Les valeurs brutes par isoforme restent dans le fichier UMich d'origine.
- **Cohorte différente de TCGA :** les 68 tumeurs CPTAC ne sont pas les 178 patients TCGA (cohortes indépendantes, pas d'appariement patient à patient). La confirmation est donc au niveau du *motif* (chaîne en deux temps le long de KRAS), pas des mêmes individus.
- **Le fichier BCM** (52 tumeurs C3L + 53 normales C3N dans le fichier dit « Tumor ») reste disponible comme contre-vérification secondaire, non exploitée dans cette mission.
- **Contre-vérification BCM réalisée le 15 nov. 2026** (voir §6) : 52 tumeurs, 6 flux (PGC, REG4, CLDN18, KRT20, CEACAM5, CLCA1 — MUC16 exclue, 48/52 < 50), cas complets, ordre KRAS croissant, nul graine 42. `pdac_cptac_bcm_fluxes.csv` SHA-256 `196d9bc1b18188e3e86a8859da8092b746d4e554f4b4a80e4b64bed14ac2de37` ; `_nul.csv` SHA-256 `2525764ec08347dde28d2deb8e570e3b97212dad90c843571fe8057a84719aca`. Runs v6 exit 0 (`results_fast_cptac_bcm/` et `_nul/`, log `runs_cptac_v6.log`). Sorties : 35 fichiers au lieu de 36 — il manque seulement `csd_consensus.png` (figure non générée, données JSON/CSV présentes ; cosmétique, cause non diagnostiquée).

## 6. Résultats (15 nov. 2026, 4 runs v6, tous exit 0)

### 6.1 Matrice principale UMich (63 tumeurs, 7 flux)

| | Réel | Nul (graine 42) |
|---|---|---|
| Cascade | 0 / 1,69 % → 1 / **T_0 4,69 % → 3** / 25,00 % → 16 (×2) | 0 / 44,40 / **51,65** / 54,91 / 68,15 |
| MC optimum | 19,35 % | 58,06 % |
| L7a | UP, probabilités **NaN**, conf. 0,5 (dégénéré, aucun vote utilisable) | UP, probabilités **NaN**, conf. 0,5 (dégénéré aussi) |
| L7b | FRAGILE (non informatif) | FRAGILE |
| Régime / Delta | criticité, Delta 1,48 | criticité, Delta 1,49 |
| Falsification delta_vs_null | 0,229 (< 0,5) | 0,235 |

Lecture flux par flux aux seuils détectés : à T_-1 (step 1) et T_0 (step 3), les « avant » n'ont que 1 et 3 points — les sauts (+1,2 à +1,9 sd) sont portés par la seule patiente au KRAS le plus faible (step 0), pas par un changement de régime. À T_+1 (step 16) : hausses modestes (+0,39 à +0,43 sd pour CLDN18/CEACAM5/CLCA1/MUC16), sens inverse de la chaîne ARN. **Test direct de l'hypothèse v4** (CLDN18 tombe, MUC16 monte chez les KRAS-les-plus-forts) : top 4 → CLDN18 −0,28 sd, MUC16 +0,99 sd, CEACAM5 +0,54 sd ; top 12 → CLDN18 **+0,41 sd**, MUC16 **−0,25 sd**, CEACAM5 −0,06 sd. Le motif s'inverse quand le groupe s'élargit de 4 à 12. **Spearman flux vs rang KRAS : tous |rho| ≤ 0,14, tous p > 0,28** — aucune relation monotone.

### 6.2 Contre-vérification BCM (52 tumeurs, 6 flux)

| | Réel | Nul (graine 42) |
|---|---|---|
| Cascade | 5,71 / 59,64 / **T_0 63,26 % → 33** / 69,04 (×2) | 0 / 15,22 / **20,93** / 32,40 / 46,64 |
| MC optimum | 23,81 % | 23,81 % |
| L7a | UP, probabilités **NaN**, conf. 0,5 (dégénéré) | UP, probabilités **NaN**, conf. 0,5 (dégénéré) |
| L7b | FRAGILE | ROBUSTE (non informatif — verdict L7b clos) |
| Régime / Delta | criticité, Delta 1,55 | criticité, Delta 1,52 |
| Falsification delta_vs_null | 0,273 | 0,178 |

Lecture flux par flux : aux seuils détectés (steps 31/33/36), tous les mouvements sont minuscules (+0,01 à +0,33 sd) — le seuil T_0 à 63 % n'a aucun mouvement de flux derrière lui. **Test direct :** top 4 → CLDN18 −0,52 sd, CEACAM5 +0,46 sd ; top 7 → CLDN18 −0,03 sd ; top 12 → CLDN18 **+0,57 sd**. Même instabilité qu'en UMich. **Spearman : tous |rho| ≤ 0,20, tous p > 0,16.**

### 6.3 Verdict

**NON — la chaîne en deux temps (CLDN18 qui tombe, MUC16 qui monte chez les KRAS-les-plus-forts) n'est PAS confirmée au niveau protéine, sur aucune des deux matrices.** Le pipeline ne sépare pas le réel du nul en protéine (Delta réel/nul : 1,48/1,49 en UMich, 1,55/1,52 en BCM ; L7a dégénéré des deux côtés) ; aucun seuil tardif analogue au T_0 93,22 % de l'ARN ; le test direct s'inverse entre top 4 et top 12. **Ce que ça n'invalide pas :** le résultat ARN v4 (autre cohorte — 178 patients TCGA contre 63/52 tumeurs CPTAC —, autre couche de mesure ; l'ARN et la protéine ne se recouvrent pas forcément, surtout pour des mucines bruyantes en protéomique). La piste CLDN18/MUC16/CEACAM5 reste une hypothèse ARN, en attente d'une confirmation indépendante (autre cohorte ARN, ou réponse aux médicaments GDSC/PRISM).
**Limite technique notée :** L7a dégénéré (probabilités NaN, confiance 0,5) sur les 4 runs CPTAC, réel comme nul — cause non diagnostiquée (hors mission : la v6 ne doit pas être modifiée ici) ; à investiguer avant de réutiliser ces sorties L7a.
