# §8.78 — Inventaire utile des dépôts GitHub Ising / cancer (PISTE A)

**Date d'inventaire :** 21 novembre 2026 (lecture seule, connecteur GitHub, compte FindPrint).
**Statut :** PISTE — rien ici n'est un verdict importé. Tout résultat cité d'un autre dépôt est une
hypothèse à tester, jamais une preuve (règle du 15 novembre 2026). Aucun run n'a été lancé dans ce
chantier, aucun fichier n'a été téléchargé, modifié ni poussé.
**Pipeline de référence :** v6.2, SHA `f07567c4…` (inchangé, jamais modifié).
**Livre blanc :** `livre-blanc-pdac-v6.md`, §8.1–§8.77, SHA local vérifié `e4804934fa832131…`
(16 premiers caractères hexadécimaux, 21 nov. 2026 12h07 UTC).
**Protocole :** `PROTOCOL_inventaire_depots_878.md`. **Provenance :** `PROVENANCE_878.md`.
**Périmètre :** les 17 dépôts du compte FindPrint ont été dénombrés par recherche
(`user:FindPrint`, 17 résultats, 21 nov. 2026). Six ont été inventoriés en profondeur ;
quatre dépôts PDAC déjà connus sont seulement nommés ; `tlogNext-pdac-phase2` (autre IA)
n'a été ni lu ni ouvert au-delà de son nom dans la liste des 17 — il est seulement nommé
ci-dessous, sans aucune lecture de son contenu. Six autres dépôts hors périmètre sont
nommés à partir de la seule liste de recherche, sans lecture.

---

## Verdict d'abord

**Utile comme piste — 4 dépôts.**

1. **`universal-log-research`** (public, dernier commit 21 nov. 2026 00h21 UTC) — LE dépôt
   le plus riche de la piste : benchmarks Ising classiques et quantique, calibration des
   29 estimateurs, versions historiques du pipeline (v5.3 → v5.9.4), et surtout les analyses
   PDAC des 16–20 novembre 2026 (Tiriac 2018, écran de réplication externe, GSE271300,
   GSE194249, holdout GSE57495, carte inter-dépôts `REPOSITORY_MAP_2026-11-20.md`).
   C'est lui qui porte les candidates pour la piste B.
2. **`pdac-systems-evidence-preclinical`** (public, dernier commit 17 sept. 2026) — registre
   de gouvernance et de provenance préclinique : protocoles de recherche de séries ordonnées
   (`PROTOCOL_003`), inventaire de sources PDAC ordonnées du 27 août 2026 (GSE262627,
   OrganoIDNetData, GSE186960, GDC organoid), scripts d'import GDC et reçus d'intégrité
   (55 RNA-seq ouvertes). Utile comme méthode et comme source de candidates, pas comme résultat.
3. **`T_log-`** (public, dernier commit 15 nov. 2026) — archive des versions du pipeline,
   de v3.2 à v6.0 (`universal_v6.0.0_cohen.py`, `v5.9.0f`, v4.2.5 → v5.9.2). Utile comme
   provenance des versions et comme référence historique ; aucune donnée cancer nouvelle.
4. **`apamea-artificial-spin-ice-multiflux`** (privé, dernier commit 17 sept. 2026) — carte
   multi-flux 17 contrôles sur glace de spin artificielle (données Zenodo DOI
   10.5281/zenodo.8250892, 685 frames). Utile comme MÉTHODE : rotation des contrôles,
   ablations, leave-one-temperature-out — le précédent méthodologique direct de la rotation
   des contrôles du §8.32. Aucune donnée cancer.

**Archive / sans rapport direct — 2 dépôts.**

5. **`TLOG`** (public, dernier commit 17 sept. 2026) — notes de théorie seulement : deux
   fichiers texte (`Tlog_n_d_d4log_n.txt`, `InverseTlog_n_d_d4log_n.txt`) et un PDF
   (`Tlog(Part2).pdf`). README d'un mot (« # TLOG »). Rien d'exécutable, rien de PDAC.
6. **`Simulation-tlog`** (public, dernier commit 14 oct. 2026) — 48 notebooks Jupyter
   `ModeFast` / `ModeRobust` générés (Ising 2D, Ising quantique, Bio-ising2d, BioCancer,
   Cosmo, Climat, Finance, pharmacovigilance, son, impression, molécule) avec leurs PDF.
   README d'un mot. Archive de sorties générées, sans code de pipeline ni matrice PDAC
   exploitable en l'état. Les deux notebooks `ModeFast_BioCancer_Tlog` /
   `ModeRobust_BioCancer_Tlog` sont une piste documentaire seulement (contenu non lu :
   notebooks de ~1 Mo, hors lecture utile pour un inventaire).

**Candidates pour la piste B — 6, dont 2 fortes (détail au §8.78.8) :**

| # | Candidate | Série / plateforme | n | Gènes v4 | Statut |
|---|---|---|---|---|---|
| C1 | **Chen et al. 2025, Nature Communications** (matrice AUC 46 PDO × 63 médicaments) | PDO, AUC médicaments | 46 | N/A (flux = AUC, pas des gènes) | **FORTE** — input CSV déjà préparé (SHA `296681b6…`), rejetée sous v5.9.4 (minimum 50) mais 46 ≥ 40 (minimum v6.2 fast) |
| C2 | **GDC ORGANOID-PANCREATIC** (RNA-seq ouverte) | Organoïdes, RNA-seq | 55 | Non vérifié (transcriptome complet) | **FORTE** — transversale, matrice 60 660 gènes × 55, scripts d'import + reçus dans le dépôt |
| C3 | **GSE57495** (GPL15048) | Tumeurs microdisséquées, microarray | 63 | **11/12** (GSTM1 absent) | Candidate avec caveat : matrice déjà détenue (SHA `995dbeff…`), mais déjà tenue comme holdout direct (§8.66/§8.69) — pas indépendante pour KRAS–CEACAM5 |
| C4 | **GSE194249** (Nat. Commun. 2022, 84 PDPCOs) | PDPCO, FPKM + réponse médicaments | 84 (expression) ; n réponse < 50 sous v5.9.4, exact non versé | Non vérifié | À VÉRIFIER — audit scripté, sortie d'audit non versée au dépôt |
| C5 | **GSE262627** (circadien PDA) | Organoïdes + lignées, RNA-seq, 7 temps | 68 échantillons, 7 positions | Non vérifié | NON RETENU pour v6.2 inchangé (7 < 40) ; piste design temporel authentique |
| C6 | **OrganoIDNetData** (Zenodo 10643410) | Imagerie organoïdes, toutes les 4 h jusqu'à 100 h | ~26 positions/trajectoire potentielle | N/A (flux morphologiques à définir) | CONDITIONNEL — inventaire metadata-only seulement, archive 4,6 Go non téléchargée |

**Leads d'accès seulement (pas de matrice publique exploitable) :** Nicholson et al. 2024 /
JHH pharmacotyping (95 PDO, pas de matrice par PDO dans le supplément inspecté) ;
Feizi et al. AACR 2025 (120 PDO, pas de matrice ligne à ligne liée).

**Non-candidates (déjà tenues ou exclues, raisons écrites au §8.78.8) :** GSE271300 (souris,
3/3 et 4/3 souris — trop petit) ; GSE186960 (un seul temps) ; Tiriac 2018 (déjà couru,
25/25 contrôles) ; GSE21501, GSE79668 (déjà courues §8.69/§8.70/§8.72) ; GSE62165
(4e cohorte, §8.64–§8.66) ; GSE78229, GSE28735 (incluses dans GSE62452) ;
GSE15471, GSE16515, GSE32676, GSE91035, GSE84219, GSE179351 (n < 40).

---

## 8.78.1 — Méthode de l'inventaire (résumé ; protocole complet : `PROTOCOL_inventaire_depots_878.md`)

Recherche `user:FindPrint` (17 dépôts, 21 nov. 2026) ; pour chaque dépôt cible : dernier
commit (`list_commits`, 2 derniers), README (`get_file_contents`, SHA blob consigné),
arborescence racine puis sous-dossiers pertinents, et lecture des documents de synthèse
(cartes, écrans, protocoles, rapports). Lecture seule : aucune écriture, aucun push, aucun
téléchargement de données, aucun run. Le dépôt `tlogNext-pdac-phase2` n'a pas été lu.
La classification « tenue / non tenue » d'une cohorte a été vérifiée contre le livre blanc
local (§8.1–§8.77) par recherche textuelle (`grep`) — voir `PROVENANCE_878.md`.

---

## 8.78.2 — `universal-log-research` — LE dépôt utile

- **Lien :** https://github.com/FindPrint/universal-log-research
- **Visibilité :** public. **Description :** « UNIVERSAL_LOG research pipeline, theory notes,
  reproducible audits, Ising benchmarks, and exploratory PDAC analyses. »
- **Créé :** 20 nov. 2026 23h49 UTC. **Dernier commit :** 21 nov. 2026 00h21:36 UTC,
  SHA `c9e23e2eb91438b00272685503d78237da8f8e28` (« Document related repository versions
  and evidence ») ; précédent 20 nov. 2026 23h49 UTC, SHA `26e54688…` (« Prepare public
  source release »). C'est le dépôt le plus récent du compte.
- **README :** SHA blob `16317faf463127d81927b4f58cf56126b8589691` (6 480 o). Il se présente
  comme un « audit-first research pipeline » pour données multi-flux ordonnées, avec un
  instantané de preuves au 20 novembre 2026 : Ising classique (dont un run aveugle L64
  avec seuil proche de Tc 2D — « prometteur, pas une preuve »), pilote synthétique
  (faux positifs possibles, une seule réalisation par cas), calibration (puissance limitée
  pour transitions faibles), et trois analyses PDAC (Tiriac 2018, Nature Communications
  2025, KRAS G12D + PARP souris). Avertissement explicite : pas d'usage médical.
- **Structure (61 entrées à la racine) :** versions du pipeline (`UNIVERSAL_LOG_v5.3.py`,
  `v5.8.py`, `v5.8_COHEND_ONLY.py`, `v5.9.0_COHEND_ONLY.py`, `v5.9.2.py`, `v5.9.3.py`,
  `v5.9.4.py`, `v5.9.4_profiled.py`, `v5.9.0f`, `v6.0.0_cohen` — copies, PAS v6.2) ;
  théorie et guides (`TLog.txt`, `GUIDE_DEBUTANT_UNIVERSAL_LOG.md`,
  `MATRICE_29_ESTIMATEURS_TLOG.md`, `D_KIND_TAXONOMIE_V5_8.md`,
  `CONTRAT_D_TLOG_ET_CALIBRATION.md`, `INDIVIDUAL_ESTIMATOR_EXTENSION_PLAN.md`,
  `TLOG_TRANSITION_VALIDATION_PROTOCOL.md`, `ISING_MCMC_MULTIFLUX_PROTOCOL.md`) ;
  audits (`AUDIT_DECISION_LOG.md`, `AUDIT_SUPPLEMENT_2026-11-14.md`,
  `AUDIT_SUPPLEMENT_2026-11-15.md`, `README_AUDIT_REPRODUCTION*.md`,
  `REPRODUCE_AUDIT*.ps1`, `SHA256SUMS*.txt`, `PUBLICATION_MANIFEST_2026-11-20.csv`,
  `PROJECT_FILE_CATALOG*.csv`, `SUPPLEMENT_ATTACHMENT_INDEX*.csv`,
  `REPOSITORY_MAP_2026-11-20.md`) ; dossiers `ising_classique_test/`,
  `ising_quantique_test/`, `calibration_29/`, `calibration_29_v58/`,
  `tlog_d_kind_v58_results/`, `audit_release/`, `output/`, `pancréas/`.
- **Ising classique (`ising_classique_test/`) :** `PIPELINE_BENCHMARKS.md` (v5.3, 7 nov. 2026 —
  18 tests sémantiques réussis, intégration sur balayage Ising L=16, 105 observations,
  profils T_log multi-échelle, sensibilité aux blocs bootstrap, transfert quantique),
  `finite_size/` (audit v6.0 : `synthetic_pilot_v1`, `calibration_v1`, `REPRODUCTION_FR.md`,
  `tlog_sensitivity_report.md`), `generate_ising.py`, `finite_size_ising.py`,
  `ising_temperature_sweep.csv`, `ising_field_sweep.csv`,
  `multiflux_mcmc_pipeline_test.py`, `test_pipeline_semantics.py`,
  `tlog_independent_chains*.py`, `tlog_block_sensitivity.py`, dossiers de résultats
  (`results_temperature/`, `results_field/`, `results_tlog_profiles/`,
  `results_tlog_uncertainty*/`, `replicate_sweep_data/`).
  Utilisable comme piste : benchmarks reproductibles v5.3/v6.0 et calibration — mais ce sont
  des versions ANTERIEURES à v6.2 ; aucun de ces résultats ne se transfère tel quel à v6.2.
- **Ising quantique (`ising_quantique_test/`) :** `RAPPORT_ISING_QUANTIQUE.md` (chaîne
  transverse TFIM, N=8/10/12, diagonalisation exacte, g_c=1 ; le pipeline v5.3 ne localise
  PAS g_c avec les ancres — d_crit ≈ 0,96, loin de la référence 4 — résultat négatif utile),
  `run_tfim_exact_pipeline.py`, `data/tfim_ground_state_N8/N10/N12.csv`,
  `quantum_ising_pipeline_summary.json` (180 962 o), `results/N8|N10|N12`.
- **Calibration 29 estimateurs (`calibration_29/`, `calibration_29_v58/`) :**
  `RAPPORT_CALIBRATION.md`, `calibrate_29_estimators.py`, `calibration_29_results.json`,
  `estimator_outputs.csv`, `targeted_calibration*.csv`, heatmap d'erreurs. Piste
  méthodologique pour la calibration des estimateurs (ne pas importer les valeurs).
- **PDAC (`pancréas/`) :** quatre dossiers `ANALYSE_THERAPEUTIQUE_2026-11-16|17|19|20`,
  `REVUE_INDEPENDANTE_2026-11-15`, `_audit_pdf_text`, et deux copies `.txt` de v6.0/v5.9.0f.
  - **11-16 :** audit PRISM PDAC (`AUDIT_PRISM_PDACS_v1.md`, `analyze_pdac_prism_multicontrol.py`,
    `pdac_prism_KRAS_corrected_all_compounds.csv` 2,2 Mo, `pdac_models_exact_diagnosis_and_controls.csv`,
    `daraxonrasib_resistance_2026/`, `Repurposing_Public_24Q2_Readme.txt`). Dépôt PRISM :
    criblage médicaments sur modèles PDAC — piste de contradiction / drug-response, pas une
    cohorte v4.
  - **11-17 :** `candidate_combination_g12d_parp/` (réanalyse souris KRAS G12D + PARP),
    `external_validation_g12c/`, `multi_axis_resistance/`.
  - **11-19 :** Tiriac 2018 (runs multi-contrôles, `Tiriac2018_Gemcitabine_all_controls_PDACDomain/`,
    `pipeline_runs*/`, `pipeline_inputs_balanced_15|50/`), `GSE271300_H5AD_METADATA_AUDIT.json`
    (342 093 o — métadonnées single-cell souris), `audit_GSE194249_candidate.py`,
    `package_GSE194249_candidate_audit.py`, `analyze_GSE271300_mouse_level.py`,
    `prepare_mouse_level_pipeline_input.py`, `mouse_level_pipeline_trial/`.
  - **11-20 :** `EXTERNAL_REPLICATION_SCREEN_REPORT_2026-11-20.md`,
    `SCREENING_SOURCE_MANIFEST_2026-11-20.json` (SHA `d29590b4…`),
    `TIRIAC2018_ALL_CONTROL_RUN_SUMMARY.md`, `JHH_PDAC_pharmacotyping/` (supplément
    Nicholson 2024 inspecté : `SUPPLEMENT_STRUCTURE.txt`, pas de matrice par PDO),
    `candidate_NatureComm2025_PAAD/` (structure du supplément, manifeste d'input,
    protocole pilote gelé `PILOT_PROTOCOL_LOCK_2026-11-20.md`, script
    `run_NatureComm2025_all_controls.py` — l'input CSV préparé est local, non versé).
  - **REVUE 11-15 :** holdout GSE57495 (`PROTOCOLE_HOLDOUT_GSE57495.md`,
    `RESULTATS_HOLDOUT_GSE57495.md`, `analyze_gse57495_holdout.py`,
    `all_gene_spearman_vs_KRAS.csv` 10 397 483 o — table génome entier Spearman vs KRAS,
    piste utile pour la piste B : quels gènes corrèlent avec KRAS au-delà des 12 v4),
    `cohort_replication_summary.csv`, `survival_cox_audit.csv`,
    `REVUE_SCIENTIFIQUE_PDACS.md` (19 544 o).
  - **`REPOSITORY_MAP_2026-11-20.md`** (SHA `d8f2b66a…`) : carte inter-dépôts lue ici —
    elle rapporte, sans que ce chantier les vérifie, que le dépôt suite (autre IA) décrit
    une association KRAS–CEACAM5 dans GSE71729 (n=145, d=0,52, p permut. 0,008) et
    GSE62452 (n=69, d=0,68, p=0,0185) sans ajustement de pureté, et que les tables
    d'entrée nommées n'y sont pas reproductibles depuis ce seul dépôt. Cité uniquement
    depuis cette carte ; le dépôt concerné n'a pas été lu.
- **Ce qui est utilisable :** benchmarks et calibrations Ising (méthode) ; écran de
  réplication 11-20 et ses candidates (C1, C4) ; table Spearman génome entier vs KRAS ;
  scripts d'audit GSE194249/GSE271300 (méthode d'audit, pas de données).
- **Ce qui ne l'est pas :** les versions de pipeline incluses (≤ v5.9.4 / v6.0) ne sont
  PAS v6.2 ; les résultats PDAC cités dans le README sont des rapports d'analyses
  antérieures, pas des verdicts du livre blanc ; les matrices d'entrée des pilotes
  (Tiriac bundle ZIP, NatureComm2025 CSV, données GSE) sont locales, non versées.

## 8.78.3 — `pdac-systems-evidence-preclinical` — registre de gouvernance et de sources

- **Lien :** https://github.com/FindPrint/pdac-systems-evidence-preclinical
- **Visibilité :** public, description vide.
- **Créé :** 26 août 2026. **Dernier commit :** 17 sept. 2026 17h39:24 UTC,
  SHA `d4b329a388e8709fae737dca07a1f2d5765e0b4f` (« Add files via upload ») ; précédent
  27 août 2026, SHA `e86171a4…` (« Inventory ordered PDAC data sources », Manus AI).
  Dépôt figé depuis le 17 septembre 2026 — état initial, aucune hypothèse active.
- **README :** SHA blob `e0e6b2e4dab58608c500b0428afb6f3556cc85b6`. « Recherche préclinique
  uniquement » — ni diagnostic, ni recommandation thérapeutique. État initial déclaré :
  gouvernance définie, sources candidates vérifiées comme références (non téléchargées),
  AUCUNE donnée expérimentale importée, AUCUN code de modélisation non audité, AUCUNE
  hypothèse de combinaison active. Sept principes non négociables (provenance + version +
  licence + empreinte avant toute analyse ; couches distinctes ; jamais de pseudo-temps
  depuis une variable clinique future ; simulation ≠ efficacité ; hypothèse falsifiable
  avec contradiction connue ; résultats négatifs conservés ; manifeste SHA-256).
- **Structure (11 entrées) :** `README.md`, `STATUS.md` (SHA `d16d7320…`),
  `MANIFEST_SHA256.txt`, `docs/` (`architecture/`, `decisions/`, `governance/`,
  `sources/`), `protocols/`, `registry/` (`hypotheses/`, `parameters/`, `variables/`),
  `data/` (`external-links/`, `processed/`, `raw/`), `results/` (`.gitkeep` seul —
  AUCUN résultat), `scripts/`.
- **Contenu utile :**
  - `docs/sources/INVENTAIRE_SOURCES_PDAC_ORDONNEES_20260827.md`
    (SHA `25e0d300…`) : quatre sources vérifiées — GSE262627 (circadien, 7 temps, non
    présélectionné pour v3 inchangé), OrganoIDNetData (présélectionné, inventaire
    metadata-only seulement), GSE186960 (non retenu, un seul temps), GDC
    ORGANOID-PANCREATIC (55 RNA-seq, conservé pour analyse transversale). C'est la
    source documentaire des candidates C2, C5, C6.
  - `docs/sources/SOURCES_PRECLINIQUES_PDAC_VERIFIEES.md` (SHA `f003dbb8…`) :
    organoïdes GDC/AWS, essai HOPE (Grossman et al. 2022), SYNERGxDB, Therapeutics
    Data Commons DrugComb/DrugSyn — références de benchmarking de synergie, pas des
    cohortes v4.
  - `protocols/` : `PROTOCOL_003_RECHERCHE_SERIES_PDAC_ORDONNEES.md`
    (SHA `d999797d…`, critères d'inclusion/exclusion pour séries ordonnées —
    réutilisable tel quel comme grille par la piste B),
    `PROTOCOL_000_REGISTRE_EVIDENCE_PRECLINIQUE.md`,
    `PROTOCOL_001_SELECTION_SOURCE_ET_FLUX.md`,
    `PROTOCOL_002_CONSTRUCTION_MATRICE_RNASEQ_TECHNIQUE.md`,
    `CONTRAT_FLUX_001_ORGANOID_TRANSCRIPTOME.md`.
  - `scripts/` : six scripts GDC (`import_gdc_open_rnaseq.py`,
    `build_gdc_unstranded_matrix.py`, `build_gdc_metadata_receipt.py`,
    `inspect_gdc_rnaseq_schema.py`, `inventory_gdc_open_metadata_axes.py`,
    `qc_gdc_rnaseq_numeric.py`) — la voie d'accès concrète à la candidate C2.
  - `data/external-links/` : reçus d'import GDC
    (`GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST.tsv`,
    `*_RECEIPT.json`, `*_QC_RECEIPT.json`, `SOURCES.tsv`) — provenance vérifiable
    de la candidate C2 ; les 55 TSV et la matrice 60 660 × 55 sont LOCAUX, hors Git.
  - `registry/` : quasi vide — `HYPOTHESIS_TEMPLATE.yaml` (884 o),
    `PARAMETER_REGISTRY.tsv` (116 o), `VARIABLE_REGISTRY.tsv` (79 o). Registre
    jamais rempli : aucune hypothèse enregistrée.
  - `STATUS.md` (27 août 2026) : confirme 55/55 MD5 vérifiés, schéma homogène, QC
    conforme, AUCUN axe expérimental admissible dans les métadonnées GDC, v3/F1′/F2″
    non exécutés, prochain jalon conditionnel = inventaire Zenodo metadata-only
    d'OrganoIDNetData après autorisation explicite.
- **Ce qui est utilisable :** la grille PROTOCOL_003, l'inventaire du 27 août 2026,
  les scripts et reçus GDC (accès C2), les références de synergie (piste de
  contradiction). **Ce qui ne l'est pas :** aucune donnée, aucun résultat, aucun
  verdict — dépôt d'infrastructure, figé depuis le 17 septembre 2026.

## 8.78.4 — `T_log-` — archive des versions du pipeline

- **Lien :** https://github.com/FindPrint/T_log-
- **Visibilité :** public, description vide.
- **Créé :** 25 août 2026. **Dernier commit :** 15 nov. 2026 16h41:28 UTC,
  SHA `e41f97e23277bb3eedab3f99c60adbff23595675` (« Add files via upload ») ;
  précédent le même jour 13h40, SHA `21e74ea4…`.
- **README :** SHA blob `73e55b36f81c4c97872c6a7b34350b28fe95d7ba` — un mot : « # T_log- ».
  Aucune documentation.
- **Structure (37 entrées) :** `Archive/` (un `readme.txt` de 1 octet — vide),
  et les versions du pipeline : `pipeline_autonome_v3_2 - Copie.txt`,
  `pipeline_autonomev3_propre.py` et variantes (`_0_4rpz`, `_proprefix`),
  `pipeline_autonome_v3_3_fixed.py`, `pipeline_autonome_v3_3_harmonic_v1/v2.py`,
  `Tlog-V3-5-5-HP-V1.py`, `Tlog_v3_5_2/3/4_harmonic_v1.py`,
  `Tlog_prediction_multilevel_v1.py` (et copie `(1)`),
  `UNIVERSAL_LOG_v4_2_5_CORRIGE.py`, `v4_2_7_DUAL_ZSCORE.py`, `v4_2_8.py`,
  `v4_2_9.py`, `v4_3_1.py`, `v4_3_3.py`, `v4_3_5.py`, `v4_4_0.py`, `v4_4_1.py`,
  `v4_4_2.py`, `v4_4_3.py`, `v4_4_4-.py`, `v4_4_5.py`, `v4_4_7.py`,
  `UNIVERSAL-LOG-V4-4-3c0.py`, `UNIVERSAL_LOG_v5_3.py`, `UNIVERSAL_LOG_v5.8.py`,
  `UNIVERSAL_LOG_v5.9.2.py`, `universal_v6.0.0_cohen.py` (622 526 o),
  `universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f.py` (622 212 o),
  `module_f1_f2_csd.py`.
- **Utilisable :** provenance des versions — c'est l'archive qui établit la lignée
  v3.2 → v6.0 et conserve v5.9.0f et v6.0 intacts ; utile pour vérifier qu'une version
  citée ailleurs est bien celle-ci (par taille et par comparaison de hachage).
  **Non utilisable :** aucune donnée, aucune cohorte, aucune documentation ; v6.2
  n'y figure PAS (v6.2 vit dans `tlogNext-cancer-pdac` / `Code`) ; aucune de ces
  versions ne doit être exécutée à la place de v6.2.

## 8.78.5 — `apamea-artificial-spin-ice-multiflux` — méthode de rotation des contrôles (pas de cancer)

- **Lien :** https://github.com/FindPrint/apamea-artificial-spin-ice-multiflux
- **Visibilité :** privé. **Créé :** 26 août 2026. **Dernier commit :**
  17 sept. 2026 17h41:09 UTC, SHA `d4c3982a97cfe3929995b53f5d01d80432c18d63`
  (« Add files via upload ») ; précédent 26 août 2026, SHA `e9eae06e…`
  (« Audit calibration provenance and metadata eligibility », Manus AI).
- **README :** SHA blob `533e37ecf8af5e3ed7dbbd48a71a345055039b6e` (7 588 o) — le README
  le plus méthodologique des six. Principe central : en v3, le seuil est décidé
  uniquement par l'optimisation Monte Carlo ; c'est un rang dans la colonne de
  contrôle, ni une température, ni un Tc physique. 17 flux (orientation/M, énergie,
  dynamique de flips, morphologie/local), employés à tour de rôle comme colonne de
  contrôle : carte multi-régimes dépendante du contrôle, pas de seuil global unique.
  Ablations, leave-one-temperature-out (119 sorties), blocs temporels contigus
  (51 sorties), synthèse croisée de robustesse (238 sorties réutilisées), audit
  topologique global (685 frames bruts — identités inter-températures insuffisamment
  validées : aucun flux vertex/charge/transitions ajouté), audit de calibration /
  provenance (aucune métadonnée éligible comme 18e flux). Données : Zenodo Apamea,
  DOI 10.5281/zenodo.8250892. Sept rapports listés (`RAPPORT_MULTIFAMILLE_17FLUX_*`,
  `*_LEAVE_ONE_TEMPERATURE_OUT_*`, `*_ABLATIONS_*`, `*_BLOCS_TEMPORELS_*`,
  `*_SYNTHESE_CROISEE_ROBUSTESSE_*`, `*_AUDIT_TOPOLOGIE_*`, `*_AUDIT_CALIBRATION_*`).
  Reproduction : Python/NumPy/pandas/SciPy/Matplotlib/seaborn, v3 mode `stable`,
  graine 42 ; archives complètes en releases GitHub, référencées par SHA-256 dans
  `release-assets/ARCHIVES_COMPLETES_SHA256.tsv`.
- **Structure (12 entrées) :** `README.md`, `STATUS.md` (SHA `1a7382b4…`),
  `MANIFEST_SHA256.txt` (77 084 o), `data/` (`derived/`), `docs/` (`methodology/`,
  `provenance/`, `reports/`), `pipelines/` (`original/` — v2/v3 intacts),
  `scripts/`, `results/` (`control_views/`, `synthese/`), `release-assets/`.
- **Utilisable :** la MÉTHODE — c'est le précédent direct de la rotation des contrôles
  (§8.32) et des diagnostics de dépendance de représentation (ablations, LOTO,
  blocs contigus) ; les conventions CSD/F1′/F2″ y sont documentées. **Non utilisable :**
  aucune donnée cancer, aucun flux transcriptomique, aucune cohorte PDAC ; les 17 flux
  sont des observables de glace de spin, non transférables tels quels.

## 8.78.6 — `TLOG` — notes de théorie seulement

- **Lien :** https://github.com/FindPrint/TLOG
- **Visibilité :** public, description vide.
- **Créé :** 16 juillet 2026. **Dernier commit :** 17 sept. 2026 17h38:52 UTC,
  SHA `092bc4baa77ebfebd4a9a94c857b42bb66a536ed` (« Add files via upload ») ;
  précédent 25 août 2026, SHA `77c5f1b6…` (« Revise analysis in Tlog_n_d_d4log_n.txt »).
- **README :** SHA blob `19faf0ae0d7eb1f4dbe0cd9e33039b1803b1a797` — un mot : « # TLOG ».
- **Structure (5 entrées) :** `Tlog_n_d_d4log_n.txt` (5 099 o),
  `InverseTlog_n_d_d4log_n.txt` (5 626 o), `Tlog(Part2).pdf` (214 336 o),
  `README.md`, `LICENSE.txt`.
- **Verdict :** notes de théorie TLog à l'état brut, sans code, sans données, sans
  protocole. Rien d'utilisable comme piste pour le PDAC au-delà de l'historique
  doctrinal (déjà consigné dans `TLog.txt` de `universal-log-research` et dans le
  canevas local). Abandonné depuis le 17 septembre 2026.

## 8.78.7 — `Simulation-tlog` — archive de notebooks générés

- **Lien :** https://github.com/FindPrint/Simulation-tlog
- **Visibilité :** public, description vide.
- **Créé :** 14 oct. 2026. **Dernier commit :** 14 oct. 2026 16h32:35 UTC,
  SHA `c9ff4a3e1099bb64e37279bf0028096688030f7b` (« Add files via upload ») ;
  précédent le même jour 16h30, SHA `4b156152…`. Dépôt créé et figé le même jour.
- **README :** SHA blob `89ed4e8e967aa466b5c0ce4e32436bd48fadaa98` — un mot :
  « # Simulation-tlog ».
- **Structure (50 entrées) :** 24 paires notebook + PDF, en deux modes
  (`ModeFast_*`, `ModeRobust_*`) : `ising 2D-1`, `Ising2DQuantique`,
  `Bio-ising2d`, `BioCancer_Tlog`, `Cosmo_Tlog`, `Climat_Tlog`, `Tlog_Finance`,
  `pharmacovigilance_OWID_Tlog`, `pharmacovigilance_VAERS_Tlog`,
  `MOLECULE_PERSIST_LOG`, `Printing_Tlog`, `SOUND_LOG v2.0`, plus `LICENSE`.
  Tailles : notebooks de ~0,5 à 2,3 Mo, PDF de ~0,45 à 1,6 Mo.
- **Verdict :** archive de sorties générées (notebooks + PDF), sans code de pipeline
  versionné ni matrice de données. Les deux notebooks `BioCancer_Tlog` (869 092 o et
  968 584 o) sont une piste documentaire seulement — leur contenu n'a pas été lu
  (notebooks de ~1 Mo, hors lecture utile pour un inventaire) et rien ne permet
  d'affirmer qu'ils contiennent une cohorte PDAC exploitable. À ne rouvrir que si la
  piste B manque de matière : lecture ciblée des deux notebooks BioCancer, avec
  protocole propre.

## 8.78.8 — Candidates pour la piste B (détail)

Rappel de la règle : une candidate n'est pas un verdict. La piste B devra, pour chacune,
geler son propre protocole AVANT tout run (construction du CSV, mapping, contrôles, nuls),
et vérifier l'indépendance contre les cohortes déjà tenues (TCGA, ICGC PACA-AU, GSE71729,
GSE62452, GSE62165, GSE21501, GSE79668, CPTAC UMich/BCM, Tiriac 2018). Les gènes v4 :
PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16.

### C1 — Chen et al. 2025, Nature Communications (matrice AUC 46 PDO × 63 médicaments) — FORTE

- **Série :** 46 modèles organoïdes PDAC (PDO), 63 colonnes AUC médicaments.
  Article DOI 10.1038/s41467-025-57520-3.
- **Plateforme :** réponse médicamenteuse (AUC), pas d'expression — les gènes v4 sont
  N/A ; les flux seraient les 63 colonnes AUC, cible Gemcitabine fixée d'avance
  (même design que Tiriac 2018).
- **n :** 46. **Pourquoi elle devient candidate maintenant :** le pilote du 20 novembre
  2026 a été REJETÉ par `UNIVERSAL_LOG_v5.9.4.py` (minimum 50 points, 1 contrôle lancé
  sur 62 prévus, APR-246, erreur « Série trop courte : 46 points valides »). Mais le
  minimum v6.1/v6.2 en mode fast est de **40 points** — 46 ≥ 40. La porte qui l'a
  fermée sous v5.9.4 n'existe plus sous v6.2. C'est la candidate la plus avancée :
  input déjà préparé sans imputation ni mise à l'échelle.
- **Accès :** supplément Springer MOESM13
  (https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM13_ESM.xlsx,
  SHA `0e009cd56d2f6c25b0b355590becc4abfee3e1080633173bc33606d1bf325340`) ;
  input pipeline local `candidate_NatureComm2025_PAAD/NatureComm2025_46PDO_63Drug_AUC.csv`
  (SHA `296681b64d3ad5309aab349696439257185f0e679cf50a35858a898b046cb3fd`) ;
  protocole pilote gelé `PILOT_PROTOCOL_LOCK_2026-11-20.md` (SHA `0068c4eb…`) ;
  script de run `run_NatureComm2025_all_controls.py` (SHA `0c178bb2…`).
  Source : `universal-log-research`, `pancréas/ANALYSE_THERAPEUTIQUE_2026-11-20/`,
  `EXTERNAL_REPLICATION_SCREEN_REPORT_2026-11-20.md` (SHA `11b0c220…`) et
  `SCREENING_SOURCE_MANIFEST_2026-11-20.json` (SHA `d29590b4…`).
- **Caveat :** matrice médicament × PDO, pas une cohorte d'expression — elle teste la
  réplication du design Tiriac, pas la chaîne v4 ; n=46 reste petit (falsification
  indisponible sous n=75, comme GSE79668).

### C2 — GDC ORGANOID-PANCREATIC (RNA-seq ouverte, 55 fichiers) — FORTE

- **Série :** organoïdes pancréatiques (patients), RNA-seq ouverte GDC.
- **Plateforme :** RNA-seq (quantifications `unstranded`), transcriptome complet.
- **n :** 55 fichiers (55/55 MD5 et tailles vérifiés, schéma homogène, QC numérique
  conforme). Matrice technique locale : 60 660 `gene_id` × 55 `file_id`.
- **Gènes v4 :** NON VÉRIFIÉS depuis le dépôt (aucune liste de gènes lue ; le
  transcriptome complet les contient vraisemblablement — à vérifier par la piste B
  avant tout run, pas à affirmer ici).
- **Accès :** scripts dans `pdac-systems-evidence-preclinical/scripts/`
  (`import_gdc_open_rnaseq.py`, `build_gdc_unstranded_matrix.py`,
  `build_gdc_metadata_receipt.py`, `inspect_gdc_rnaseq_schema.py`,
  `inventory_gdc_open_metadata_axes.py`, `qc_gdc_rnaseq_numeric.py`) ; reçus dans
  `data/external-links/` (manifeste TSV, reçus JSON d'import, de schéma et de QC).
  Les 55 TSV et la matrice sont LOCAUX, exclus de Git — la piste B devra les
  re-télécharger ou les retrouver localement avec leurs hachages.
- **Caveat :** transversale, AUCUN axe expérimental admissible identifié dans les
  55 métadonnées examinées (STATUS.md du 27 août 2026) — pas de pseudo-temps ;
  testable uniquement comme cohorte transversale ordonnée par un flux (même statut
  que TCGA/ICGC), avec les garde-fous du livre blanc.

### C3 — GSE57495 (GPL15048, 63 tumeurs microdisséquées) — candidate avec caveat

- **Série :** GSE57495, 63 tumeurs PDAC microdisséquées congelées, plateforme GPL15048.
- **Plateforme :** microarray (valeurs log2 déposées).
- **n :** 63. **Gènes v4 : 11/12 — GSTM1 absent** (aucune sonde à symbole exact GSTM1 ;
  seule la sonde partagée `merck-NM_000561_s_at`, annotée « GSTM1 GSTM2 GSTM4 »,
  exclue comme ambiguë ; aucune sonde mappée à la main). KRAS présent ; 63/63 cas
  complets sur 11 gènes. Vérifié au §8.69 du livre blanc.
- **Accès :** matrice détenue localement (13 487 043 o, SHA `995dbeff…532efc`,
  60 608 lignes, 0 NaN) et mapping GPL15048 construit à neuf (SHA `93e01ec3…998f952`),
  selon la correction consignée au §8.69 (la plateforme est GPL15048, pas GPL6244
  comme l'affirmait à tort le §8.66 §1.2). GEO :
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57495.
- **Caveat MAJEUR :** déjà tenue comme holdout DIRECT (§8.66/§8.69 et
  `REVUE_INDEPENDANTE_2026-11-15/RESULTATS_HOLDOUT_GSE57495.md` : Spearman
  KRAS–CEACAM5 ρ=0,4377, p permutation 0,00024, IC 95 % [0,1901, 0,6352] ;
  partielle après scores acineux/îlots : 0,3521). Elle n'est donc PAS indépendante
  pour l'association KRAS–CEACAM5. Comme paire pipeline v6.2 (jamais courue : §8.69
  la marquait « INUTILISABLE — aucun CSV, aucun run » au moment du chantier, la
  matrice n'ayant été construite qu'après), elle reste utilisable — à condition que
  la piste B déclare explicitement cette antériorité et ne la présente jamais comme
  une confirmation indépendante de l'association.

### C4 — GSE194249 (84 PDPCOs, Nat. Commun. 2022) — À VÉRIFIER

- **Série :** GSE194249, 84 PDPCOs (organoïdes dérivés de patients pancréatiques).
  Article DOI 10.1038/s41467-022-29857-6 (CC BY 4.0).
- **Plateforme :** FPKM (matrice `GSE194249_PDPCOs_FPKM.txt.gz`) + réponse aux
  médicaments (Suppl. Data 8, MOESM11) + suivi clinique (Suppl. Data 10, MOESM13)
  + cohorte 84 PDPCOs (Suppl. Data 1, MOESM4).
- **n :** expression 84 PDPCOs (colonnes exactes non versées) ; n réponse
  médicamenteuse < 50 sous le minimum v5.9.4 fast — le nombre exact n'est PAS
  vérifiable depuis le dépôt : le script d'audit
  (`audit_GSE194249_candidate.py`, SHA `ae3c85cd…`) existe, mais son dossier de
  sortie `candidate_GSE194249_sources/` (avec `CANDIDATE_DATA_AUDIT.json/.md`)
  est ABSENT du dépôt (données locales non versées). La piste B devra refaire
  l'audit depuis GEO avant toute candidature.
- **Gènes v4 :** NON VÉRIFIÉS. **Accès :** GEO
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE194249 + suppléments
  Springer MOESM4/11/13. **Statut :** candidate conditionnelle à la vérification
  de n et de la couverture v4 — ne pas lancer sans l'audit refait et gelé.

### C5 — GSE262627 (série circadienne PDA, 7 temps) — NON RETENU pour v6.2 inchangé

- **Série :** GSE262627, 7 temps (0, 4, 8, 12, 16, 20, 24 h), 6 organoïdes PDAC et
  4 lignées cellulaires, 68 échantillons GEO, comptages `featureCounts`.
  Article : Sharma et al., JCI Insight 2024 (PMC11141942).
- **Plateforme :** RNA-seq. **Gènes v4 :** non vérifiés (sans objet : série trop courte).
- **n :** 7 positions par système — inférieur au minimum le plus permissif de v3
  comme de v6.2 (40 en fast). La mise en commun organoïdes/lignées ne serait pas
  une série répétée unique.
- **Accès :** GEO https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262627.
- **Valeur :** référence utile de DESIGN temporel authentique — le seul axe de temps
  réel mesuré de tout l'inventaire. Piste pour un protocole futur à fenêtre courte
  explicitement gelée, ou pour un autre instrument — pas pour v6.2 inchangé.

### C6 — OrganoIDNetData (imagerie organoïdes, Zenodo 10643410) — CONDITIONNEL

- **Série :** imagerie d'organoïdes PDAC humains et murins, acquisition toutes les 4 h
  jusqu'à 100 h, co-culture immunitaire pour certains champs. Archive Zenodo ouverte
  CC BY 4.0, 4,6 Go, 180 images selon la notice Zenodo et l'article (190 selon le
  README du dépôt public associé — discordance consignée, à résoudre par inventaire).
  Article : Kulkarni et al., Scientific Data 2024 (s41597-024-03631-3).
- **Plateforme :** imagerie (champs de vue). **n :** ~26 positions par trajectoire
  complète potentielle — à vérifier, les 180 images ne forment pas une unique série
  (systèmes, champs de vue et dérivés artificiels mélangés dans l'archive).
- **Gènes v4 :** N/A — les flux seraient morphologiques, à définir (taille, forme,
  texture des organoïdes), jamais des gènes.
- **Accès :** Zenodo https://zenodo.org/records/10643410. Archive NON téléchargée ;
  seule action recommandée (inventaire du 27 août 2026) : inventaire metadata-only
  (noms, tailles, MD5, structure, correspondance culture/champ/heure), après
  autorisation explicite de Zackary. Aucune image consultée, aucun flux défini,
  aucun run.
- **Statut :** seule présélection de l'inventaire du 27 août 2026 — conditionnelle à
  l'inventaire metadata-only et à une configuration v3/v6.2 courte gelée.

### Leads d'accès seulement (pas de matrice publique exploitable au 20 nov. 2026)

- **Nicholson et al. 2024, Annals of Surgery (JHH pharmacotyping)** — 95 PDOs, IC50
  pour 5 agents ; le supplément inspecté (NIHMS2020869, SHA `3d6d24a5…`) contient
  méthodes, code R et tables agrégées, PAS de matrice PDO × médicament. DOI
  10.1097/SLA.0000000000006517. Ne pas reconstruire de valeurs depuis des graphiques.
- **Feizi et al., AACR 2025 (résumé)** — ~3 000 composés à une dose, 600 à six doses,
  120 PDOs PDAC ; aucune matrice ligne à ligne liée dans les actes inspectés.
  Piste de demande d'accès seulement ; aucune demande envoyée.
- **Toronto 58/120-PDO screening program** — cité dans l'écran du 20 nov. 2026 comme
  piste de demande d'accès ; aucune demande envoyée.

### Non-candidates (raisons écrites)

- **GSE271300** (Singhal et al., scRNA souris, PC69/PC106 : 3/3 et 4/3 souris par
  traitement) — échantillon trop petit pour le minimum du pipeline ; ne pas utiliser
  les comptages cellulaires comme réplicats biologiques indépendants. Écran du
  20 nov. 2026. Métadonnées auditées localement (`GSE271300_H5AD_METADATA_AUDIT.json`).
- **GSE186960** (Panc1 + gemcitabine scRNA-seq) — un seul temps explicite, conditions
  hétérogènes. Non retenu (inventaire du 27 août 2026).
- **Tiriac et al. 2018** — déjà couru : 60 PDO complets, 26 AUC, 25/25 contrôles,
  T0 ambigu partout, contrôle non monotone partout (v5.9.4, 19–20 nov. 2026). Pas
  une nouvelle cohorte ; le bundle d'audit complet est local
  (`output/pdac_pipeline_audit_2026-11-19/`), non versé.
- **GSE21501, GSE79668** — déjà courues (§8.69 : d_maxsep −0,0100, NON ;
  §8.70/§8.72 : PARTIEL puis renversé sur 13 nuls, d_médian +0,1447).
- **GSE62165** — 4e cohorte, déjà tenue (§8.64–§8.66 : bloc estomac/mucus confirmé,
  10/12 gènes v4 — DPCR1 et GSTM1 absents).
- **GSE78229, GSE28735** — échantillons déjà inclus dans GSE62452 (re-test déguisé
  de la paire V1). Écartées au §8.69.
- **GSE15471, GSE16515, GSE32676, GSE91035, GSE84219, GSE179351** — n < 40
  (enquête §8.66 §1.3).
- **ICGC PACA-CA / E-MTAB-6134** — accès hors périmètre (§8.66 §1.3).
- **COAD / LUAD** — autres cancers, lots déjà courus (relecture interdite §8.64.7).
- **CPTAC (UMich / BCM)** — protéine, 7/6 flux (pas 12), lots déjà courus.
- **SYNERGxDB / Therapeutics Data Commons DrugComb** — bases de synergie (benchmarks
  de contradiction pour hypothèses de combinaison), pas des cohortes PDAC v4 ;
  le jeu NCI-60 n'est pas spécifique au PDAC.

## 8.78.9 — Dépôts déjà connus (nommés seulement, non relus en profondeur)

- **tlogNext-cancer-pdac** — https://github.com/FindPrint/tlogNext-cancer-pdac
  (public, dépôt de travail PDAC v6.2, mis à jour 20 nov. 2026 22h21 UTC).
- **tlogNext-cancer-pdac-suite** — https://github.com/FindPrint/tlogNext-cancer-pdac-suite
  (privé, suite du livre blanc v6.2 §8.74 et suivantes, mis à jour 20 nov. 2026 23h07 UTC).
- **Code** — https://github.com/FindPrint/Code (public, pipeline v6.1 de référence,
  mis à jour 19 nov. 2026 00h05 UTC).
- **pancreatic-cancer-open-data-reproducibility** — https://github.com/FindPrint/pancreatic-cancer-open-data-reproducibility
  (public, « Private non-clinical reproducibility framework for open pancreatic cancer
  data research », mis à jour 19 nov. 2026 00h04 UTC).
- **tlogNext-pdac-phase2** — https://github.com/FindPrint/tlogNext-pdac-phase2
  (public, autre IA — NOMMÉ SEULEMENT, contenu non lu dans ce chantier).

## 8.78.10 — Autres dépôts du compte (nommés depuis la seule liste de recherche, non lus)

Ces six dépôts n'entrent pas dans le périmètre de la piste A (ni Ising, ni cancer PDAC
d'après leurs noms et dates) ; ils sont nommés ici pour que l'inventaire des 17 soit
complet, sans lecture de leur contenu :

- **Canvas** — https://github.com/FindPrint/Canvas (public, mis à jour 26 oct. 2026).
- **Dissertation-** — https://github.com/FindPrint/Dissertation- (public, mis à jour
  26 oct. 2026).
- **BTC_Tlog** — https://github.com/FindPrint/BTC_Tlog (public, Jupyter Notebook, mis à
  jour 17 sept. 2026).
- **seismologie-retrospective-cadrage** — https://github.com/FindPrint/seismologie-retrospective-cadrage
  (privé, « Cadrage sûr et reproductible d'un pilote sismologique rétrospectif, sans
  prédiction ni alerte opérationnelle », mis à jour 17 sept. 2026).
- **seismologie-retrospective-catalogue** — https://github.com/FindPrint/seismologie-retrospective-catalogue
  (privé, « Catalogue sismologique historique figé, provenance et audit de qualité pour
  étude rétrospective non prédictive », mis à jour 17 sept. 2026).
- **UNIVERSAL_LOG_30_10_2026** — https://github.com/FindPrint/UNIVERSAL_LOG_30_10_2026
  (privé, Python, mis à jour 30 oct. 2026).

## 8.78.11 — Ce que la piste B doit faire (recommandations, pas des verdicts)

1. **C1 d'abord :** NatureComm2025, 46 PDO × 63 AUC — protocole gelé avant tout run
   (cible Gemcitabine, 62 contrôles prévus, nuls assortis), v6.2 mode fast (minimum 40).
   Vérifier d'abord que l'input local (SHA `296681b6…`) est toujours détenu et intact.
2. **C2 ensuite :** GDC ORGANOID-PANCREATIC — vérifier la présence des 12 gènes v4 dans
   la matrice 60 660 × 55 et l'intégrité des 55 fichiers (re-téléchargement via les
   scripts du dépôt si les locaux sont absents), puis protocole gelé de cohorte
   transversale (même statut que TCGA/ICGC, pas de pseudo-temps).
3. **C3 avec son caveat écrit :** GSE57495 comme paire pipeline — jamais comme
   confirmation indépendante de KRAS–CEACAM5.
4. **C4 après re-audit :** GSE194249 — refaire l'audit de sélection depuis GEO
   (n réponse exact, couverture v4) et geler le protocole avant toute décision.
5. **C5/C6 :** ne pas lancer sous v6.2 inchangé ; C6 exige l'inventaire metadata-only
   d'OrganoIDNetData (autorisation explicite de Zackary) avant toute définition de flux.
6. **Ne pas rouvrir** les cohortes déjà courues ni les lots déjà courus (relecture
   interdite §8.64.7) ; ne pas importer les résultats des autres dépôts comme des
   verdicts — chaque candidate se juge sur ses propres runs, avec ses propres nuls.

---

*Fin de la section §8.78. Inventaire en lecture seule, 21 novembre 2026. Aucun run, aucun
téléchargement de données, aucune modification de dépôt. Les SHA des fichiers lus sont
consignés dans `PROVENANCE_878.md`.*
