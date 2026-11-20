# PROVENANCE — §8.69 : Confirmation indépendante pour `maxsep` (C3)

Chantier §8.69, 20 nov. 2026. Protocole gelé :
`PROTOCOL_maxsep_independent_869.md`, SHA-256
`86c239b438e68202d375f7baa59bc90d16d65974742071f1552d937431e61a52`.
Pipeline v6.2 : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; jamais modifié).

## Cohorte primaire : GSE57495

- **Série :** GEO GSE57495 — « Development of a prognostic gene
  signature in pancreatic cancer ».
- **Auteurs / centre :** Chen D-T et coll., Moffitt Cancer Center
  & Research Institute, Tampa, FL, USA (département de
  biostatistique et bio-informatique ; contact :
  dung-tsa.chen@moffitt.org). Article : Chen D-T, Davis-Yadley AH,
  Huang P-Y, Husain K, Centeno BA, Permuth-Wey J, et al. (2015),
  « Prognostic Fifteen-Gene Signature for Early Stage Pancreatic
  Ductal Adenocarcinoma », *PLoS ONE* 10(8): e0133562,
  doi 10.1371/journal.pone.0133562, PMID **26247463** (reçu
  12 mars 2015, accepté 28 juin 2015, publié 6 août 2015).
- **Patients :** 63 patients PDAC, stades précoces (IB, IIA, IIB),
  tumeurs réséquées macro-disséquées, tissus frais congelés,
  collectés 2006–2011 sous le protocole Moffitt Total Cancer Care
  et le protocole de recherche MCC 17779 (IRB #10.07.0008).
  Critère : survie globale (OS) comme endpoint primaire.
- **Dates GEO :** publique le 28 août 2015
  (`!Series_status "Public on Aug 28 2015"` dans la matrice).
- **Dépôt / URL :** NCBI GEO (FTP),
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE57nnn/GSE57495/matrix/GSE57495_series_matrix.txt.gz`
- **Fichier :** `data/GSE57495_series_matrix.txt.gz`, **13 487 043
  octets**, SHA-256
  `995dbeff288a14c1cc1a52489e456b7677ede5da8e287069b8298d649b532efc`,
  téléchargé 2026-11-20 ~18:09 UTC, HTTP 200, lecture complète
  vérifiée (60 608 lignes de données).
- **Plateforme :** `!Series_platform_id "GPL15048"` (lu dans
  l'en-tête de la matrice) — Rosetta/Merck Human RSTA Custom
  Affymetrix 2.0.
- **CORRECTION vs protocole §8.66 §1.2 :** le §8.66 affirmait
  GSE57495 sur « plateforme GPL6244 (même plateforme que
  GSE62452, mapping déjà détenu) ». C'est FAUX : la plateforme
  est GPL15048 (confirmé par l'en-tête de la matrice ET par deux
  sources secondaires concordantes : Wu et coll., *Sci Rep* 2025,
  « GSE57495 (GPL15048 platform) comprised 63 tumor pancreatic
  tissue samples » ; tableau supplémentaire Springer,
  « GSE57495 63 GPL15048 »). **Le mapping GPL6244 détenu n'est
  PAS utilisé pour GSE57495.**
- **Échantillons :** 63 échantillons, tous titrés PDAC1…PDAC63
  (`!Sample_title`), tous tumoraux — aucun tissu non tumoral
  dans la série. Caractéristiques par échantillon
  (`!Sample_characteristics_ch1`) : survie globale (mois),
  statut vital (DEAD/ALIVE), stade (1B/2A/2B/1). Aucune
  exclusion.
- **Nature des lignes :** intensités de puce normalisées log2
  (RMA, valeurs ~7–12 — min/médiane/max exacts et NaN comptés
  par `build_fluxes_869.py`, voir § Construction). Ce ne sont
  pas des comptages ARN-seq : l'échelle et la technologie
  diffèrent de TCGA (log2 RSEM+1) et de GSE62452 (log2 RMA-like
  GPL6244). Aucune renormalisation faite ici.

## Mapping sondes → symboles : GPL15048 (construit à neuf)

- **Table de plateforme :**
  `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL15nnn/GPL15048/soft/GPL15048_family.soft.gz`,
  récupérée en streaming, transfert coupé après le marqueur
  `!platform_table_end` (script `download_gpl15048_mapping_869.py`,
  adapté de `download_gpl6244_mapping.py`, original intact).
- **Colonnes de la table :** ID, GB_LIST, EntrezGeneID,
  GeneSymbol, SPOT_ID.
- **ADAPTATION documentée (même nature d'annotation, aucune
  sonde mappée à la main) :** le protocole §8.69 §4.1 prévoyait
  la colonne « Gene Symbol » ou, à défaut, « gene_assignment ».
  La table réelle porte la colonne **`GeneSymbol`** (sans espace).
  Le script accepte donc « Gene Symbol » ou « GeneSymbol »
  (même sémantique : un symbole de gène par sonde), puis
  « gene_assignment ». Colonne utilisée : `GeneSymbol` (index 3).
- **Résultat :** `data/GPL15048_probe2symbol.tsv`, 1 121 947
  octets, SHA-256
  `93e01ec387ab710dfbfe4b7ad960a90c494b131f62637df3a4476fa9f998f952` ;
  60 607 lignes de table, marqueur de fin vu ; 41 024 sondes
  avec symbole, 22 115 symboles uniques. Les ~19 583 sondes
  sans symbole sont des contrôles (AFFX-…) et des sondes non
  annotées — non mappées, jamais devinées.
- Sondes multiples vers un même symbole : agrégation par médiane
  (règle du projet, dans `build_fluxes_869.py`).

## Portes d'acceptation (§5) — résultats

| Cohorte | KRAS présent | 12 gènes v4 | Cas complets ≥ 40 | Sort |
|---|---|---|---|---|
| GSE57495 (primaire) | oui | **non — 11/12, GSTM1 absent** (aucune sonde à symbole exact GSTM1 ; seule la sonde partagée `merck-NM_000561_s_at`, annotée « GSTM1 GSTM2 GSTM4 », exclue comme ambiguë, §4.1) | 63/63 sur 11 gènes | **INUTILISABLE** (§5) — aucun CSV écrit, aucun run lancé |
| GSE62165 (repli §3) | oui | **non — 10/12, DPCR1 et GSTM1 absents** | 118/118 sur 10 gènes | **INUTILISABLE** (§5) — aucun CSV écrit, aucun run lancé |
| GSE21501 (cohorte #3, addendum) | oui | **oui — 12/12** | **132/132** | **UTILISABLE** — paire construite, 2 runs |

Vérifications d'indépendance (exclusions documentées, addendum) :
GSE78229 exclue (50 échantillons déjà inclus dans GSE62452) ;
GSE28735 exclue (échantillons 1–90 de GSE62452) ; COAD/LUAD
exclus (autres cancers + lots déjà courus = relecture) ; CPTAC
exclu (protéine, 7/6 flux, lots déjà courus) ; GSE15471,
GSE16515, GSE32676, GSE91035, GSE84219, GSE179351 exclus
(n < 40). Piste restante non vérifiée : GSE79668 (51 cas,
GPL11154) — pour un chantier futur, pas tentée ici.

## Cohorte #3 : GSE21501 (addendum du 20 nov. 2026, ~13h40 EST)

- **Série :** GEO GSE21501 — « A six-gene signature predicts
  survival of patients with localized pancreatic ductal
  adenocarcinoma ».
- **Auteurs / centre :** Stratford JK et coll. (Royaume-Uni).
  Article : Stratford JK et coll. (2010), *PLoS Medicine*,
  PMID **20644708** (second PMID de la série : 28380042).
  Cohorte de validation indépendante du papier Chen et coll.
  2015 (« evaluated using an independent microarray cohort
  dataset (Stratford et al: n = 102) »).
- **Patients :** 102 patients PDAC avec données cliniques
  (cohorte Stratford) + 30 échantillons Nebraska/UNC sans
  données cliniques (voir annotation ci-dessous) — 132
  échantillons au total dans la matrice, tous annotés
  « Patient Primary Pancreatic Tumor ».
- **Dates GEO :** publique le 19 juil. 2010
  (`!Series_status "Public on Jul 19 2010"`).
- **Dépôt / URL :** NCBI GEO (FTP),
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE21nnn/GSE21501/matrix/GSE21501_series_matrix.txt.gz`
- **Fichier :** `data/GSE21501_series_matrix.txt.gz`, **12 575 998
  octets**, SHA-256
  `1bbbd9d2f1a89b26b73b32ef1e781b5ad46aa2f80ebc1d8c94d0ac5dcb6d9b7b`,
  téléchargé 2026-11-20 ~18:16 UTC, HTTP 200, lecture complète
  vérifiée (45 220 lignes de données + 1 ligne d'en-tête).
- **Plateforme :** `!Series_platform_id "GPL4133"` (lu dans
  l'en-tête de la matrice) — Agilent-014850 Whole Human Genome
  Microarray 4x44K G4112F (deux couleurs, référence Stratagene
  Human reference RNA ; `!Series_overall_design` :
  « reference x sample »).
- **Annotation des échantillons — lecture RAGUÉE, vérifiée
  positionnellement avant la construction :** les
  `!Sample_characteristics_ch2` ne forment pas une table
  régulière. Le libellé « tissue: Patient Primary Pancreatic
  Tumor » est en ligne ch2 n°0 pour les colonnes 0–29 (30
  échantillons Nebraska/UNC) et en ligne ch2 n°4 pour les
  colonnes 30–131 (102 échantillons Stratford) ; les lignes
  ch2 n°2, 3, 5 (t stage, n stage, risk group) ne sont
  renseignées que sur les colonnes 30–131, et le design
  général confirme : « The 30 Nebraska and UNC samples were
  not analyzed with clinical data so it is not provided ».
  Règle mécanique retenue (builder) : tumeur si le libellé
  figure dans UNE ligne ch2 de l'échantillon → **132/132
  tumeurs**. Les 30 sans données cliniques sont gardées : la
  paire n'a besoin d'aucune donnée clinique (ordre KRAS
  uniquement). La répartition des stades publiée (73 stade I,
  0 stade II) est incohérente — raison de l'exclusion §8.66 —
  mais sans effet ici (aucun ordre stade construit).
- **Nature des lignes :** log2 RATIOS (tumeur / référence
  Stratagene), valeurs min −11,33, médiane 0,04, max +11,67,
  0 NaN — pas des log-intensités comme les autres cohortes :
  chaque gène, KRAS compris, est un log-ratio par rapport à
  la même référence. L'ordre par KRAS reste un ordre par
  KRAS (relatif à la référence commune). KRAS (log-ratio) :
  min −2,08, médiane −0,34, max +0,73. Aucune
  renormalisation faite ici.
- **Mapping GPL4133 :** table
  `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL4nnn/GPL4133/soft/GPL4133_family.soft.gz`,
  streaming, arrêt après `!platform_table_end` (script
  `download_gpl4133_mapping_869.py`) ; colonnes : ID, COL, ROW,
  NAME, SPOT_ID, CONTROL_TYPE, REFSEQ, GB_ACC, GENE,
  **GENE_SYMBOL** (index 9), GENE_NAME, … ; 45 220 lignes,
  marqueur de fin vu ; 32 696 sondes avec symbole, 19 749
  symboles uniques. Sortie `data/GPL4133_probe2symbol.tsv`,
  407 146 octets, SHA-256
  `5630ff23418af6d5241cda8d82a22421e8159a160e6b44123eac3f38eb7a3129`.
  Sondes multiples vers un même symbole : médiane (règle du
  projet).
- **Construction :** `build_fluxes_869.py --cohort 21501`
  (variante (a), 12 gènes v4, ordre KRAS croissant, cas
  complets, nul graine 42). Sorties :
  `pdac_869_geo21501_fluxes.csv` (132 lignes), SHA-256
  `3d7c1bfe1a4ce02cc7bc4087791e8175efc03338e0643c98463a836e9cd46ba9` ;
  `pdac_869_geo21501_fluxes_nul.csv`, SHA-256
  `4fc8e79ddb8991f91276881d58631a6b03ef82654fdd74d9a3323db280e7d439`.

## Construction (variante (a) — voir protocole §4)

- Script `build_fluxes_869.py` (copie adaptée de
  `build_fluxes_geo62452.py`, variante (a) seulement, original
  intact). Les 12 mêmes gènes que la v4 TCGA (PGC, REG4, CLDN18,
  MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16),
  ordre = KRAS croissant, sans correction, cas complets
  seulement. Nul : bloc des flux permuté par lignes, graine 42,
  `rng(42)`, contrôle intact. Le contrôle n'est jamais un flux.
- Sorties : `pdac_869_geo57495_fluxes.csv` (+ `_nul.csv`) ;
  SHA-256 consignés dans la section §8.69 (vérification de
  contenu par le builder : voir sa sortie).
- Repli (seulement si la primaire est inutilisable, protocole
  §3) : GSE62165, `data/GSE62165_series_matrix.txt.gz`, SHA-256
  `fd50fc415a31a4d19a4af82e29afc6909e913f4f223d0b4cd4b637ae4a03727f`
  (provenance `PROVENANCE_866.md`), mapping
  `data/GPL13667_probe2symbol.tsv`, SHA-256 `c0a5e8fc…8c2b2`
  (même provenance) ; tumeurs identifiées comme au §8.66
  (« tissue: pancreatic tumor », 118 tumeurs, 13 non-tumoraux
  exclus).

## Nature des lignes (règle de provenance du projet)

- Séries réelles = intensités de puce (mesures instrumentales
  transformées : log2 RMA par les déposants, agrégation des
  sondes par médiane, ordre par KRAS). Nuls = lignes permutées,
  graine 42 — échantillons hypothétiques, pas des mesures.
- Aucune valeur inventée ; aucune valeur recopiée à la main
  (tables générées depuis `extract_869.json`).
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`), v6.1
  (`2af5e5ce…c1c9`), v6 (`bb8bbdba…c0773`). Aucune nouvelle
  version construite dans ce chantier — pas de v6.5.
