# Provenance — confirmation GEO GSE71729 (PDAC, ARN)

## Source
- **Série :** GEO GSE71729 — « Virtual Microdissection of Pancreatic Ductal
  Adenocarcinoma Reveals Tumor and Stroma Subtypes » (Moffitt et al., 2015).
- **Dépôt :** NCBI Gene Expression Omnibus (GEO).
- **URL :** https://ftp.ncbi.nlm.nih.gov/geo/series/GSE71nnn/GSE71729/matrix/GSE71729_series_matrix.txt.gz
- **Téléchargé :** 2026-11-15, 14:17 UTC.
- **Taille :** 15 622 315 octets (exactement la taille attendue, vérifiée).
- **SHA-256 :** `b228789314ec4d866ec51b65724664abaa24b822577c55d3727820c867536a54`
- **Plateforme :** GPL20769 — Agilent-014850 Whole Human Genome Microarray
  4x44K G4112F (version « Gene Symbol », mise à jour juillet 2014),
  technologie : oligonucléotides in situ, organisme Homo sapiens.
  Annotation de la plateforme : fichier SOFT de la famille GPL20769
  (37 588 662 octets, téléchargé 2026-11-15) — table de 19 749 lignes.
  Le fichier `.annot.gz` n'existe pas sur le FTP (HTTP 404) ; le SOFT a
  servi à la place.
- **Traitement des données (auteurs, champ `!Sample_data_processing`) :**
  « log2 Cy5 signal was analyzed after setting negative values to zero.
  Probe data were collapsed by gene symbol via mean expression. Samples
  were quantile normalized to the subset of genes with less than 0.5
  standard deviation across primary, metastatic, and normal samples.
  Data were processed in MATLAB R2013a. »
  Donc : valeurs = log2 des intensités Cy5 (pas des ratios), négatifs mis
  à zéro, sondes déjà agrégées par symbole par MOYENNE par les auteurs.

## Nature des lignes
- **Matrice :** 19 749 symboles de gènes × 357 échantillons ; 0 valeur
  manquante ; valeurs de 0,00 à 13,11 (médiane 2,93) ; 0 valeur négative,
  23 zéros sur 7 050 393 valeurs (cohérent avec la mise à zéro des négatifs).
- **Les ID_REF de la matrice sont déjà des symboles de gènes** (vérifié :
  même ensemble que la table de la plateforme, 18 528 symboles
  conventionnels ; 0 symbole dupliqué — aucune agrégation supplémentaire
  n'a été nécessaire).
- **Échantillons (caractéristiques ch2, champ `tissue type`) :**
  145 tumeurs primaires, 61 métastases, 134 normaux, 17 lignées cellulaires
  (total 357 — conforme au descriptif de la série).
- **Retenus : les 145 tumeurs primaires uniquement** (cohérent avec la
  cohorte TCGA, tumeurs primaires). Métastases, normaux et lignées exclus.

## Flux construits (script `build_fluxes_geo71729.py`)
- **Variante (a) [prioritaire] :** les 12 mêmes gènes que la v4 TCGA —
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5,
  CLCA1, MUC16. **Tous les 12 présents sur la puce, KRAS présent,
  145/145 cas complets** (aucune imputation). Ordre = expression KRAS
  croissante (KRAS min 1,55, médiane 3,28, max 4,15 — valeurs log2 Cy5).
  KRAS = axe, jamais un flux.
  - `pdac_geo71729_fluxes.csv` — SHA-256
    `7d69fa888f15e9a1a128e149e35f9eeacac106198c33929dfc51e113ee8c0cf1`
  - `pdac_geo71729_fluxes_nul.csv` — mêmes lignes permutées, graine 42,
    SHA-256 `13b1ac801faccfa1410382d329625a4d65ed8e1ed26e03f2331c73ca66f246ec`
- **Variante (b) [re-sélection protocole v4] :** correction de pureté par
  régression sur scores acineux/îlots (acineux : 8 gènes présents sur 11 —
  CELA3A, CELA2A, CELA3B absents de la puce ; îlots : 4/4), exclusion des
  gènes du sexe, top 12 par variance des résidus. Variance expliquée par
  pureté (médiane des gènes) : 4,2 % (TCGA v3 : 2,0 %) ; KRAS R² pureté :
  1,4 % (TCGA : 0,3 %). Corrélation acineux-îlots : +0,502.
  Top 12 : CABP7, DMBT1, PPY, C4orf7, TFF2, RPA4, DES, PPY2, IGH@, REG4,
  CCL19, SPINK4 (seul REG4 recoupe la v4 TCGA).
  - `pdac_geo71729_fluxes_v4b.csv` — SHA-256 `9ef597cd97acc90f924964fcaece849ee3d4ee63684d7b6ca98142124fa1561d`
  - `pdac_geo71729_fluxes_v4b_nul.csv` — SHA-256 `7990898951704871df96b15bc175566b11359416a6a72ca3de29d29eb759b2d7`
- **Variante (c) [ajoutée après les premiers runs — test de l'objection la
  plus directe] :** les 12 mêmes gènes que la v4 TCGA, MAIS corrigés de la
  pureté par régression (même protocole que la v3/v4 TCGA) et ordonnés par
  résidu KRAS. R² pureté KRAS : 1,4 % ; médiane des 12 gènes : 4,6 %.
  Résidu KRAS : min −1,80, médiane −0,01, max +0,89.
  - `pdac_geo71729_fluxes_v4c.csv` — SHA-256
    `3ea678dfadf34777f67461060d4684d9e7d49b6be5a8dd2de482ec81c35dbe80`
  - `pdac_geo71729_fluxes_v4c_nul.csv` — SHA-256
    `872ef77707b675cf270edfbf53b0e811824a72b7a4399efae4feabdd162f1fe0`

## Runs v6
- Pipeline : `universal_v6.0.0_cohen.py` (v6.0.0-L7aL7b-CohenD), mode fast,
  contrôle step. Fichier v6 original jamais modifié.
## Runs v6
- Pipeline : `universal_v6.0.0_cohen.py` (v6.0.0-L7aL7b-CohenD), mode fast,
  contrôle step. Fichier v6 original jamais modifié.
- Sorties : `results_fast_geo71729/`, `results_fast_geo71729_nul/`,
  `results_fast_geo71729_v4b/`, `results_fast_geo71729_v4b_nul/`,
  `results_fast_geo71729_v4c/`, `results_fast_geo71729_v4c_nul/` (36 fichiers
  chacun) ; log `runs_geo71729_v6.log` (6× exit 0).

## Résultats (6 runs, exit 0) — verdict : NON, la chaîne v4 n'apparaît pas
- **Variante (a) [mêmes 12 gènes, bruts] :** réel cascade 1,31 / 43,85 /
  **T_0 76,77 % → step 111** / 89,70 / 89,70 ; L7a UP 82,1 % (conf. 0,416) ;
  Delta 2,16, criticité. Nul : T_0 7,84 %, L7a UP 84,6 % (conf. 0,402),
  Delta 2,20. **Le réel ne se distingue pas du nul** (même sens, même
  force, Delta quasi identiques). À T_0, mouvements petits et vers le HAUT
  (KRT20 +0,65 sd, MUC17 +0,30, DPCR1 +0,30, PGC +0,29, CLDN18 +0,24,
  CEACAM5 +0,18, MUC16 −0,17) — l'inverse de l'effondrement TCGA.
- **Variante (b) [re-sélection fraîche] :** réel T_0 25,09 %, L7a UP 82,8 %,
  Delta 2,96 ; nul T_0 24,44 %, L7a UP 44,6 %, Delta 2,90. **Même position
  de seuil pour le réel et le nul** — pas de chaîne.
- **Variante (c) [mêmes 12 gènes, corrigés pureté] :** réel T_0 41,11 %,
  L7a UP 83,1 % (conf. 0,429), Delta 2,93 ; nul T_0 85,68 %, L7a UP 45,5 %
  (conf. 0,174), Delta 2,66. À T_0 : CEACAM5 −0,70 sd, REG4 −0,46,
  KRT20 −0,37, MUC2 −0,35, PGC +0,29, DPCR1 +0,22, CLDN18 −0,19,
  MUC16 +0,05 — aucun effondrement. La correction de pureté ne change
  pas le sens : les gènes montent avec KRAS dans cette cohorte.
- **Test direct (top 12 KRAS contre le reste, en sd) :**
  (a) CLDN18 +0,68, MUC16 +0,67, CEACAM5 +0,38, PGC +0,25, DPCR1 +0,60,
  KRT20 +0,60 ; (c) CLDN18 +0,71, MUC16 +0,65, CEACAM5 +0,33, PGC +0,51,
  DPCR1 +0,47, KRT20 +0,68. Top 7 : (c) CLDN18 +1,28, MUC16 +0,73,
  DPCR1 +0,90, KRT20 +0,93. **Tout est vers le HAUT — l'inverse de TCGA
  pour CLDN18, PGC, DPCR1, KRT20.**
- **Spearman flux contre rang KRAS (a) :** CLDN18 +0,278 (p=0,001),
  CEACAM5 +0,273 (p=0,001), DPCR1 +0,197 (p=0,017), REG4 +0,186 (p=0,025),
  MUC2 −0,337 (p<0,001), MUC16 +0,037 (p=0,66 — pas de tendance monotone,
  élévation seulement dans le groupe extrême).
- **Accord partiel (2 gènes sur 7) :** MUC16 et CEACAM5 sont plus élevés
  dans le groupe KRAS-le-plus-fort dans les DEUX cohortes (MUC16 : TCGA
  +0,64 sd, GEO (c) +0,65 top 12 / +0,73 top 7 ; CEACAM5 : TCGA +0,43 sd
  à T_-1, GEO +0,38 / +0,33 top 12). La moitié « marqueurs qui montent »
  de la chaîne tient ; la moitié « marqueurs de différenciation qui
  s'effondrent » s'inverse.
- **Hypothèses (non testées) sur la différence :** technologie différente
  (puce Agilent, intensités log2 Cy5, normalisation par quantile, contre
  ARN-seq log2 RSEM+1) ; cohortes différentes (Moffitt 2015, chirurgie,
  contre TCGA mixte) ; ou la chaîne TCGA est spécifique à sa cohorte.
  Les rotations v4 (parent) montrent que la chaîne est réelle DANS TCGA
  et propre à l'axe KRAS — la non-confirmation ici porte sur la
  généralisation, pas sur l'existence du motif dans TCGA.
- L7b FRAGILE sur les 6 runs (non informatif, verdict clos).

## Ce qui manque
- Les 3 gènes acineux CELA3A, CELA2A, CELA3B ne sont pas sur la puce
  (score acineux construit sur 8 gènes au lieu de 11).
- Pas de données de survie utilisées dans les runs (les champs
  `survival_months` / `death_event` existent dans les caractéristiques
  mais ne servent pas au pipeline — l'ordre est KRAS uniquement).
- La cohorte est indépendante de TCGA (patients différents, pas
  d'appariement possible) : c'est une confirmation entre cohortes, pas
  une réplication sur les mêmes patients.
