# PROVENANCE — GEO GSE62452 (troisième cohorte ARN, confirmation CA125/CEA)

## Source
- **Série :** GEO GSE62452 — « Microarray gene-expression profiles of 69
  pancreatic tumors and 61 adjacent non-tumor tissue from patients with
  pancreatic ductal adenocarcinoma ».
- **Auteurs / contact :** S. P. Hussain et al., Laboratory of Human
  Carcinogenesis, National Cancer Institute (Bethesda, MD, USA).
  Contact : hussainp@mail.nih.gov. PMID **27197190**.
- **Dates :** soumise 17 oct. 2014, publique 1er juil. 2016, mise à jour
  26 juil. 2018. BioProject PRJNA264183.
- **Dépôt / URL :** NCBI GEO (FTP),
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62452/matrix/GSE62452_series_matrix.txt.gz`
- **Fichier :** `data/GSE62452_series_matrix.txt.gz`, **14 447 291 octets**,
  SHA-256 `8f41d5b3f11451e653fd6bfc0c6b216c219d46711a7676d1e453dee16a078cba`,
  téléchargé 2026-11-15 15:23 UTC, lecture complète vérifiée (33 364 lignes).
  **Premier téléchargement tronqué** (12 943 600 octets, EOFError après
  29 864 lignes) — re-téléchargé, le SHA ci-dessus est celui du fichier
  complet et vérifié.

## Plateforme — CORRECTION : GPL6244, pas GPL570
- La tâche annonçait GPL570 (HG-U133 Plus 2.0) ; **la matrice dit
  GPL6244** (`!Series_platform_id "GPL6244"`) et les ID_REF sont
  numériques (7892501, …) : **[HuGene-1_0-st] Affymetrix Human Gene 1.0
  ST Array, 33 297 transcript clusters**.
- **Annotation :** table de la plateforme, colonne `gene_assignment`,
  forme `accession // SYMBOLE // description // bande // Entrez`
  (plusieurs assignations séparées par ` /// `, première prise).
  Extraite en streaming du fichier
  `.../geo/platforms/GPL6nnn/GPL6244/soft/GPL6244_family.soft.gz`
  (script `download_gpl6244_mapping.py`) : le transfert a été coupé
  après le marqueur `!platform_table_end` car ce fichier est un monstre
  de plusieurs centaines de Mo (table plateforme + tables
  d'échantillons). **Table complète vérifiée : 33 297 lignes, marqueur
  de fin vu, 25 293 sondes avec symbole, 23 307 symboles uniques.**
  Sauvegarde : `data/GPL6244_probe2symbol.tsv` (819 249 octets).
- **Fausse piste documentée :** un mapping GPL570 a d'abord été extrait
  (`data/GPL570_probe2symbol.tsv`, 45 782 sondes, 22 880 symboles) avant
  de constater que la plateforme était GPL6244 — **il n'est PAS utilisé**.
  Les URL `.../GPL5nnn/GPL570/annot/GPL570.annot.gz` et
  `.../GPL5nnn/GPL570/soft/GPL570_family.soft.gz` renvoient 404
  (GPL570 est en fait sous `GPLnnn/`, pas `GPL5nnn/`).

## Nature des lignes
- Intensités de puce **normalisées log2** (RMA-like, valeurs 0,22–13,60,
  médiane 4,31, **0 valeur manquante**). Ce ne sont pas des comptages
  ARN-seq : l'échelle et la technologie diffèrent de TCGA (log2 RSEM+1)
  et de GSE71729 (intensités Cy5 Agilent).
- **Avertissement des auteurs (résumé de la série) :** les données sont
  la fusion de deux lots (les échantillons 1–90 avaient été soumis
  comme GSE28735), l'effet de lot a été retiré par les auteurs avec
  Partek Genomic Suite. La correction ne peut pas être vérifiée depuis
  la matrice seule.

## Échantillons
- **130 échantillons : 69 tumeurs, 61 tissus adjacents non tumoraux**
  (`!Sample_characteristics_ch1` : « tissue: Pancreatic tumor » /
  « tissue: adjacent pancreatic non-tumor »). **Retenues : les 69
  tumeurs uniquement.**
- Contre-vérification par les titres : accord 113/130 — les 17
  désaccords sont les titres ambigus du second lot (numéros seuls contre
  numéros + « T ») ; `characteristics_ch1` fait foi.

## Flux construits (script `build_fluxes_geo62452.py`)
- Sondes → symboles : médiane par gène en cas de duplicata
  (3 274 lignes dupliquées → 23 307 gènes uniques).
- **Variante (a) :** les 12 mêmes gènes que la v4 TCGA, tous présents,
  KRAS présent (1 sonde, 7961865). **69/69 cas complets**, ordre KRAS
  croissant (KRAS : min 5,28, médiane 6,40, max 7,36). Nul = lignes
  permutées, graine 42.
  - `pdac_geo62452_fluxes.csv` — SHA
    `d7419c0ec3ed649d98ba920411ef5f41a056caa69b38c6b9a5e3ab702cc03abf`
  - `pdac_geo62452_fluxes_nul.csv` — SHA
    `d396e5f58cfadbc37171a2d9015941be9807c6e53f31753ccaded0761f71502d`
- **Variante (b) :** re-sélection fraîche protocole v4. Scores pureté :
  acineux 10 gènes, îlots 4 gènes, corrélation +0,336. Variance
  expliquée par la pureté : médiane 5,2 %, **KRAS 19,6 %** (plus élevée
  qu'en TCGA 0,3 % et GSE71729 1,4 % — KRAS est davantage lié à la
  pureté ici). Top 12 par variance des résidus (hors KRAS, hors sexe) :
  DPCR1, CEACAM5, PPY, SLC6A14, CRP, OLFM4, GABRP, CRISP3, CP, IGJ,
  RNU5D-1, HLA-DRB5.
  - `pdac_geo62452_fluxes_v4b.csv` — SHA
    `45f0217eadb3f4f75e20f5b910f2d5d723e5c0753f91b418ce0d2af84a0f421f`
  - `pdac_geo62452_fluxes_v4b_nul.csv` — SHA
    `cf690b5cbe8dd1611276b370b32d5f303ddcc776b98e447df054f9be21f3a781`
- Jamais d'imputation.

## Pipeline
- **v6** `~/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py`,
  SHA-256 `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`,
  **jamais modifiée**. Mode fast, cible = première colonne numérique
  hors contrôles (PGC pour la variante (a)).

## Runs v6 (log `runs_geo62452_v6.log`, 15 nov. 2026, 15:24–15:34 UTC)
- (a) réel → `results_fast_geo62452/` (36 fichiers) — **exit 0**.
  Cascade 1,42 / 35,67 / **95,64 % → step 66** / 98,64 / 100,00.
  L7a UP, **probabilités NaN (dégénéré, conf. 0,5)**. Delta 1,41,
  régime criticité, falsification 0,199 (< 0,5). MC optimum 18,18 %
  (≠ cascade T_0 95,64 % — deux quantités différentes). L7b FRAGILE
  (non informatif). L1 DOWN, R² attracteur −0,051.
- (a) nul → `results_fast_geo62452_nul/` (36 fichiers) — **exit 0**.
  Cascade 0 / 12,82 / **17,10** / 21,37 / 21,37. L7a UP, NaN. Delta 1,26.
- (b) réel → `results_fast_geo62452_v4b/` (36 fichiers) — **exit 0**.
  Cascade 0 / 48,05 / **79,67** / 84,02 / 85,48. L7a UP, NaN. Delta 1,37,
  falsification 0,152. MC optimum 18,18 %. L7b FRAGILE. Cible DPCR1.
- (b) nul → `results_fast_geo62452_v4b_nul/` (36 fichiers) — **exit 0**.
  Cascade 0 / 63,94 / **84,02** / 88,38 / 95,64. L7a UP, NaN. Delta 1,40.
- **L7a NaN sur les 4 runs** — comme sur CPTAC (n=63/52). Piste
  (observation, pas une preuve) : L7a dégénère aux petits n (52, 63, 69)
  alors qu'il fonctionne à n=145 (GSE71729), 178 (TCGA), 1000 (HP35).
- **Le pipeline ne sépare pas réel et nul ici** : Delta réel ≈ Delta nul
  (1,41 contre 1,26 ; 1,37 contre 1,40) et L7a NaN des deux côtés.
  En (b), réel et nul placent leur T_0 presque au même endroit
  (79,67 % contre 84,02 %).

## Ce qui manque
- **Données cliniques / survie :** absentes de la matrice. Le fichier
  supplémentaire `GSE62452_paired_sample_information.xlsx` (listé dans
  la série) n'a pas été téléchargé — il pourrait contenir des données
  cliniques ; non vérifié.
- Pas de protéomique, pas de CRISPR, pas de sensibilité aux médicaments
  dans cette série.
- La correction d'effet de lot des auteurs (Partek) n'est pas
  vérifiable depuis la matrice.
