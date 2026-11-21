# PROVENANCE_879 — Nouvelle série indépendante, 13e paire (§8.79) : C2 arrêtée, C3 courue

**Date :** 21 novembre 2026, ~12h10–13h00 EST. **Agent :** TagPrint
(subagent, piste B). **Chantier :** §8.79.
**Protocoles gelés avant tout run :** `PROTOCOL_nouvelle_serie_879.md`
(C2, SHA `84b1adfa…27538`) puis addendum
`PROTOCOL_nouvelle_serie_879_C3.md` (C3, gelé avant toute
construction C3).
**Pipeline :** v6.2, SHA
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
— vérifié avant et après le lot, jamais modifié, jamais exécuté
ailleurs que dans ce chantier.
**Livre blanc local vérifié :**
`~/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md`,
SHA-256 (16 premiers caractères) `e4804934fa832131`, §8.1–§8.77.

## 1. Candidates examinées (vérifications pré-gel, 21 nov. 2026)

### 1.1 C1 — Chen et al. 2025, Nat. Commun. (46 PDO × 63 AUC) — NON CHOISIE

- Article : *Pathogenic germline variants in Chinese pancreatic
  adenocarcinoma patients*, Nature Communications 2025,
  DOI 10.1038/s41467-025-57520-3.
- Supplément MOESM13 (feuille « All Drugs AUC ») :
  `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM13_ESM.xlsx`
  — re-téléchargé le 21 nov. 2026, 35 732 o, SHA-256
  `0e009cd56d2f6c25b0b355590becc4abfee3e1080633173bc33606d1bf325340`
  — IDENTIQUE à l'empreinte du manifeste du pilote
  (`PIPELINE_INPUT_MANIFEST.json`, §8.78).
- Protocole pilote et manifeste lus depuis `universal-log-research`
  (`pancréas/ANALYSE_THERAPEUTIQUE_2026-11-20/candidate_NatureComm2025_PAAD/` :
  `PILOT_PROTOCOL_LOCK_2026-11-20.md`, SHA blob `0068c4eb…` ;
  `PIPELINE_INPUT_MANIFEST.json`, SHA blob `4fffd48f…`) :
  cible Gemcitabine, 62 contrôles, 46 PDO, 63 flux AUC, 0 valeur
  manquante, aucune imputation, transposition seule.
- Input CSV local (`NatureComm2025_46PDO_63Drug_AUC.csv`, SHA
  `296681b6…`) INTROUVABLE sur cette VM (recherche par nom,
  21 nov. 2026) — reconstructible depuis MOESM13, non reconstruit
  ici.
- Raison du non-choix : axe drogue (62 contrôles, 124 runs),
  pas une paire KRAS / 12 gènes — elle ne peut pas devenir une
  13e paire A2. Reste la piste suivante pour un lot drogue v6.2.

### 1.2 C2 — GDC ORGANOID-PANCREATIC (55 RNA-seq) — CHOISIE puis ARRÊTÉE

- Projet GDC `ORGANOID-PANCREATIC` (Human Cancer Models
  Initiative / Next Generation Cancer Models), RNA-seq, STAR
  Counts, accès ouvert.
- Manifeste :
  `https://raw.githubusercontent.com/FindPrint/pdac-systems-evidence-preclinical/main/data/external-links/GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST.tsv`
  — re-téléchargé le 21 nov. 2026, SHA-256
  `f713edebf0f8afb20305b1472d480564e45ac31ce79e28350d7dde6ae496220b`
  — IDENTIQUE à l'empreinte gelée dans
  `build_gdc_unstranded_matrix.py` du dépôt
  `pdac-systems-evidence-preclinical`. Copie locale :
  `data/GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST_879.tsv`
  (même SHA).
- Cas GDC interrogés par API le 21 nov. 2026
  (`POST https://api.gdc.cancer.gov/cases`, 49/49 retrouvés) :
  tous `primary_site = Pancreas`, tous projet
  `ORGANOID-PANCREATIC` ; diagnostics : 38 « Adenocarcinoma,
  NOS », 11 « Unknown ». Fichiers interrogés
  (`POST https://api.gdc.cancer.gov/files`, 55/55) :
  44 fichiers = échantillons Tumor (cas « Adenocarcinoma,
  NOS »), 11 fichiers = échantillons Normal (cas 61–71,
  diagnostic « Unknown »). Réponses API conservées en scratch
  `/tmp/b879/gdc_cases_detail.json` et `gdc_files_detail2.json`
  (métadonnées, pas des données d'expression) ; table
  d'association figée :
  `gdc_organoid_879_file_sample_map.tsv`, SHA-256
  `282d8b8319dbbc82279fa4bed08fcb7bc34a8fa9a6320ad3be46b443b109594a`.
- Téléchargement (APRÈS le gel du protocole C2) :
  `https://api.gdc.cancer.gov/data/<file_id>` pour les 55
  `file_id`, script `download_gdc_879.py` (curl, reprise Range,
  8 réessais) — **55/55 OK, MD5 conformes au manifeste,
  total 232 648 892 o exact**. Reçu :
  `download_gdc_879_receipt.json` (SHA-256 de chaque fichier).
  Dossier : `data/gdc_organoid_879/`.
  Incident documenté : deux premières tentatives en
  `systemd-run` ont échoué (lectures tronquées, `IncompleteRead`
  puis reprises lentes) — cause trouvée : les unités
  `systemd-run` n'héritent PAS des variables proxy de
  l'environnement d'exécution (`https_proxy` vers le proxy
  d'egress), donc leur egress direct est dégradé ; le
  téléchargement a abouti en exécution directe (232 Mo en
  ~3 min, 55/55 MD5 OK). Leçon consignée pour les futurs
  téléchargements : ne pas lancer de téléchargement réseau
  en `systemd-run` sans proxy.
- En-tête vérifié (GENCODE v36) :
  `gene_id, gene_name, gene_type, unstranded, stranded_first,
  stranded_second, tpm_unstranded, fpkm_unstranded,
  fpkm_uq_unstranded` ; 60 660 lignes de gènes + 4 techniques
  STAR (`N_unmapped`, `N_multimapping`, `N_noFeature`,
  `N_ambiguous`).
- **ARRÊT : DPCR1 absent de 55/55 fichiers** (0 occurrence du
  symbole exact ; les 12 autres gènes utiles — 11 v4 + KRAS —
  présents dans 55/55). Vérifications de la cause, 21 nov. 2026 :
  Ensembl REST
  `https://rest.ensembl.org/lookup/symbol/homo_sapiens/DPCR1`
  → « No valid lookup found for symbol DPCR1 » ; les 5 anciens
  identifiants Ensembl croisés (ENSG00000168631,
  ENSG00000229284, ENSG00000232308, ENSG00000257232,
  ENSG00000232251) absents eux aussi du fichier GENCODE v36 ;
  HGNC (`https://rest.genenames.org/fetch/symbol/MUCL3`) :
  **MUCL3 (HGNC:21666, « mucin like 3 »), `prev_symbol` :
  ['DPCR1']** — et MUCL3 est présent dans 55/55 fichiers.
  Aucun remappage fait (protocole gelé §4.2/§5 : symbole exact,
  aucun gène mappé à la main). **Aucun CSV C2, aucun run C2.**
  Les 55 TSV restent détenus pour un usage futur (protocole
  qui pré-enregistrerait MUCL3) ; ils ne portent aucun verdict.

### 1.3 C3 — GSE57495 (GPL15048, n=63) — COURUE (cohorte #2)

- Série : GSE57495, « Development of a prognostic gene signature
  in pancreatic cancer », PMID 26247463, NCBI GEO.
  URL : `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57495`.
- Matrice détenue localement (aucun nouveau téléchargement) :
  `data/GSE57495_series_matrix.txt.gz`, 13 487 043 o, SHA-256
  `995dbeff288a14c1cc1a52489e456b7677ede5da8e287069b8298d649b532efc`
  — IDENTIQUE au §8.69. 60 608 lignes, 63 échantillons, valeurs
  log2 déposées (min 1,46 / médiane 5,91 / max 15,06, 0 NaN).
- Mapping : `data/GPL15048_probe2symbol.tsv`, SHA-256
  `93e01ec387ab710dfbfe4b7ad960a90c494b131f62637df3a4476fa9f998f952`
  — IDENTIQUE au §8.69. 60 607 lignes, 41 024 sondes avec
  symbole, 22 115 symboles uniques, colonne `GeneSymbol`.
- Plateforme lue dans l'en-tête : `!Series_platform_id "GPL15048"`.
- 11/12 gènes v4 (GSTM1 absent — sonde partagée
  `merck-NM_000561_s_at` exclue comme ambiguë, §8.69) ; KRAS
  présent ; 63/63 cas complets sur 11 gènes.
- Antériorité déclarée : déjà tenue comme holdout DIRECT
  (§8.66/§8.69 : Spearman KRAS–CEACAM5 ρ=0,4377, p permutation
  0,00024, IC 95 % [0,1901, 0,6352] ; partielle 0,3521) —
  JAMAIS une confirmation indépendante de KRAS–CEACAM5.
  Jamais courue comme paire pipeline avant ce chantier.
- CSV de flux : `pdac_879_geo57495_fluxes.csv`, SHA-256
  `224f98eb9cc7092e05b490b1e053edd14793e3def147890be0bab567630bb51c`
  (63 lignes) ; nul (graine 42) :
  `pdac_879_geo57495_fluxes_nul.csv`, SHA-256
  `5cd274594a9a256142eb5fc539645e51a6dca2f0f15b2084b9884f686ab41edf`.
  KRAS (log2) : min 5,44 / médiane 7,24 / max 8,78.
  Stades (characteristics_ch1) : 1B:12, 2B:33, 2A:17, 1:1.

### 1.4 C4–C6 — non vérifiées / écartées (statut §8.78 repris)

- C4 GSE194249 (84 PDPCOs, Nat. Commun. 2022,
  DOI 10.1038/s41467-022-29857-6) : audit scripté, sortie
  d'audit absente du dépôt ; n réponse exact et couverture v4
  NON vérifiés — audit à refaire depuis GEO. Non choisie.
- C5 GSE262627 (circadien, 7 temps) : 7 < 40 — écartée.
- C6 OrganoIDNetData (Zenodo 10643410, imagerie) : flux
  morphologiques à définir, archive 4,6 Go non téléchargée —
  écartée pour v6.2 inchangé.
- Leads d'accès seulement (pas de matrice) : Nicholson/JHH 2024
  (95 PDO), Feizi AACR 2025 (120 PDO) — aucune demande envoyée.

## 2. Indépendance (grep livre blanc §8.1–§8.77, 21 nov. 2026)

« HCMI » 0 mention ; « organoid » 0 ; « GDC » 2 mentions
(toutes deux = accès TCGA via Xena/GDC, lignes 4919 et 6486 —
pas ORGANOID-PANCREATIC) ; « Chen et al » 0 ; « 57520 » 0 ;
« GSE194249 » 0 ; « STAR » 0 ; « GSE57495 » 11 mentions
(holdout direct §8.66/§8.69, jamais paire pipeline).
C2 : jamais utilisée ; non-recouvrement établi par programme
et système d'identifiants (UUID GDC / `submitter_id` entiers
vs barres TCGA, GSM GEO, ICGC) — limite déclarée : aucun
identifiant commun n'existe entre les systèmes, donc pas de
preuve par jointure. C3 : patients distincts des cohortes
tenues (série GEO propre, titres PDAC1..63) ; antériorité
holdout déclarée (§1.3).

## 3. Nature des lignes

- Les 55 TSV GDC sont des quantifications RNA-seq STAR
  (GENCODE v36), colonne utilisée `tpm_unstranded` (TPM du
  fournisseur, pas un calcul de ce chantier). Les 11 fichiers
  Normal n'ont pas été utilisés.
- La matrice GSE57495 porte des valeurs log2 déposées ;
  le mapping GPL15048 est une table sonde → symbole
  construite au §8.69 (médiane des sondes multiples par gène).
- Les résultats d'autres dépôts cités ici (pilote Chen,
  holdout GSE57495 ρ=0,4377, écran du 20 nov. 2026) sont des
  RÉSULTATS RAPPORTÉS, repris avec leur source — pas des
  mesures de ce chantier, pas des verdicts importés.
- Les SHA des fichiers du chantier sont consignés dans la
  section §8.79 et dans le rapport de livraison ; le SHA de
  cette provenance est calculé après écriture (auto-référence
  impossible dans le fichier lui-même).

## 4. Ce qui manque / limites

- C2 : DPCR1 n'existe plus comme symbole (devenu MUCL3) —
  une paire C2 à 12 gènes est impossible sous GENCODE v36
  sans pré-enregistrer MUCL3 ; un protocole futur devra le
  faire explicitement avant toute construction.
- C3 : paire à 11 flux (pas 12) — comparabilité limitée aux
  paires à 12 flux ; antériorité holdout — jamais une
  confirmation indépendante de KRAS–CEACAM5.
- Les réponses API GDC (cas/fichiers) sont conservées en
  scratch `/tmp/b879/` (éphémère) ; seule la table
  d'association figée est versionnée dans le chantier.
- Le MOESM13 Chen re-téléchargé (35 732 o, SHA vérifié) est
  conservé en scratch `/tmp/b879/` (vérification seulement,
  C1 non choisie) ; l'input CSV du pilote n'a pas été
  reconstruit ici.

## 5. Fichiers produits par ce chantier (à hasher après écriture)

- `~/workspace/runs/pdac-v6/section_8.79_nouvelle_serie.md`
- `~/workspace/runs/pdac-v6/PROTOCOL_nouvelle_serie_879.md`
- `~/workspace/runs/pdac-v6/PROTOCOL_nouvelle_serie_879_C3.md`
- `~/workspace/runs/pdac-v6/PROVENANCE_879.md` (ce fichier)
- `~/workspace/runs/pdac-v6/download_gdc_879.py`,
  `download_gdc_879_receipt.json`, `download_gdc_879.log`
- `~/workspace/runs/pdac-v6/build_fluxes_879.py`
  (C2, arrêt DPCR1 — aucun CSV produit)
- `~/workspace/runs/pdac-v6/build_fluxes_879_c3.py`,
  `pdac_879_geo57495_fluxes.csv`,
  `pdac_879_geo57495_fluxes_nul.csv`
- `~/workspace/runs/pdac-v6/manifest_v62_879_c3.txt`,
  `runs_v62_879_c3.log`, `results_fast_v62_879_geo57495*`,
  `extract_879_c3.json` / `.csv`, `verify_879_c3.py`,
  `direct_tests_879_c3.py`, `direct_tests_879_c3.json`
- `~/workspace/runs/pdac-v6/gdc_organoid_879_file_sample_map.tsv`
- `~/workspace/runs/pdac-v6/data/GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST_879.tsv`
- `~/workspace/runs/pdac-v6/data/gdc_organoid_879/` (55 TSV)
