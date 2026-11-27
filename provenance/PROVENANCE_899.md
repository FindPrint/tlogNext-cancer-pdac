# PROVENANCE §8.99 — GSE184585 (27 novembre 2026)

Provenance complète du chantier §8.99 (seizième paire, GSE184585).
Règle permanente du projet : source complète, nature des lignes,
comment chaque valeur a été produite, hachages, ce qui manque.
Auteur du chantier : TagPrint (agent), sous la direction de Zackary
Drasse-Ménard. Date : 27 novembre 2026. Dossier de travail :
`~/workspace/runs/pdac-v6/`. Livre blanc en lecture seule, non
modifié ; rien poussé sur GitHub ; aucun PDF ; aucune Release.

## 1. Source des données (données brutes)

- **Série :** GSE184585, « Gene expression data from patients with
  pancreatic ductal adenocarcinoma », NCBI GEO, soumise le
  2021-09-23. Auteurs/déposants : tels que déclarés dans
  l'enregistrement GEO (tissus collectés au Memorial-Sloan
  Kettering Cancer Center, NY, USA — résumé GEO).
- **URL de la série :**
  `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE184585`
- **Fichier téléchargé (FTP GEO, 27 nov. 2026, ~12h30 UTC) :**
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE184nnn/GSE184585/matrix/GSE184585_series_matrix.txt.gz`
  - SHA-256 : `e2be8441979ee9210033fac588ed99e2605cdaa598e39e6d1e0d5304aad6de01`
  - Taille : 22 632 266 octets
  - Contenu : 70 523 sondes × 82 échantillons, valeurs min 2,40 /
    médiane 5,19 / max 19,93, 0 NaN. Plateforme lue dans l'en-tête :
    GPL17586. `disease state: Pancreatic ductal adecnocarcinoma`
    (sic, faute du dépôt) pour 82/82 échantillons ; titres PDAC-1
    à PDAC-82.
- **BioProject :** PRJNA765314 (déclaré dans les métadonnées GEO
  miroir).

## 2. Annotation sondes → symboles

- **Bioconductor `hta20transcriptcluster.db` 8.8.0** (sonde HTA 2.0
  → Entrez Gene), téléchargé le 27 nov. 2026 depuis
  `https://bioconductor.org/packages/release/data/annotation/src/contrib/hta20transcriptcluster.db_8.8.0.tar.gz`
  (version confirmée dans l'index PACKAGES Bioconductor) :
  - SHA-256 du tarball : `70680ab930d4290431c312449e0ab6b46f933d55c61012e903baefbaae07a92f`
  - SHA-256 du SQLite extrait (`hta20transcriptcluster.sqlite`) :
    `405837e13af445ccf8686c7f2985cbd5c685109d57b5c7e2ec946a2c562a4dac`
  - Source Entrez Gene déclarée dans la base : 2021-04-14.
  - Contenu : 72 618 sondes, 32 120 mappées vers un symbole
    (40 453 sans gene_id : non codant / non annoté).
- **Bioconductor `org.Hs.eg.db` 3.23.1** (Entrez → symbole),
  déjà détenu dans le dossier (`data/org.Hs.eg.db_3.23.1.tar.gz`),
  SQLite extrait le 27 nov. 2026 :
  - SHA-256 du SQLite extrait (`org.Hs.eg.sqlite`) :
    `bbdf1a4d9181ac0873d8993b6c25742d6658eaa6c14a10b2df1a19dfba1f3dba`
- **Mapping écrit :** `data/GPL17586_probe2symbol.tsv`
  (30 262 sondes) :
  - SHA-256 : `2592d2586af7f166121849c67b35e504e43e37e4176c022768abf0fc49ce929e`
  - Méthode : jointure SQLite, aucune sonde mappée à la main.
- **Voies abandonnées (consignées, pas cachées) :**
  `GPL17586.annot.gz` sur le FTP GEO répond 404 « Object not
  found! » (fichier de 990 o, page d'erreur HTML, supprimé) ;
  `GPL17586_family.soft.gz` (> 1,2 Go après ~4 min de
  téléchargement, toujours en cours) abandonné au profit des
  bases Bioconductor — précédent déjà utilisé dans le dossier
  (`hgu219.db`, `org.Hs.eg.db`).

## 3. Remappage DPCR1 → MUCL3 (vérification 5/5, 27 nov. 2026)

- **R1 — HGNC REST** `https://rest.genenames.org/fetch/symbol/MUCL3`
  : MUCL3, HGNC:21666, « mucin like 3 », Approved,
  prev_symbol ['DPCR1'], date_symbol_changed 2018-03-19,
  ensembl ENSG00000168631, entrez 135656, location 6p21.33.
- **R2 — HGNC REST** `https://rest.genenames.org/fetch/prev_symbol/DPCR1`
  : numFound = 1, même enregistrement (HGNC:21666, MUCL3).
- **R3 — org.Hs.eg.db 3.23.1 :** Entrez 135656 → RefSeq NM_080870,
  Ensembl ENSG00000168631 (+ 4 autres, les mêmes que §8.79) ;
  alias DPCR1 et MUCL3 → même _id 18000.
- **R4 — Ensembl REST** `https://rest.ensembl.org/lookup/symbol/homo_sapiens/MUCL3`
  (résout : ENSG00000168631, chr 6, 30940973–30954221, GRCh38) et
  `.../DPCR1` (« No valid lookup found for symbol DPCR1 »).
- **R5 — Données détenues :** MUCL3 = 5 sondes (Entrez 135656)
  présentes dans la matrice ; DPCR1 = 0 sonde, aucune entrée
  Entrez dans org.Hs.eg.db 3.23.1.
- Référence de la méthode : §8.85 (mêmes 5 portes, mêmes sources).

## 4. Construction du CSV réel

- **Script :** `build_fluxes_899.py`
  - SHA-256 : `a9ede3eefae47a7d12fa6accd9400e7da4ed1afef3d0ce30b848e2c326956388`
  - Adapté de `build_fluxes_879_c3.py` (méthode copiée, pas les valeurs).
- **CSV réel :** `pdac_899_gse184585_fluxes.csv`
  - SHA-256 : `07540af57ef27974178036ea333f4ad51d9a19e49d7993f1d997b80fe6b99d13`
  - Forme : 82 lignes × 13 colonnes (`step` + 12 flux).
  - Flux, dans l'ordre v4 : PGC, REG4, CLDN18, MUC17, MUCL3
    (ex-DPCR1), CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16.
  - Sondes par flux : PGC 1, REG4 1, CLDN18 1, MUC17 3, MUCL3 5,
    CR2 2, KRT20 1, MUC2 3, GSTM1 1, CEACAM5 1, CLCA1 1, MUC16 1.
  - Agrégation des sondes multiples par médiane (même méthode que §8.79).
  - Ordre des lignes : KRAS ascendant ; KRAS = axe d'analyse,
    jamais un flux. KRAS (1 sonde) : min 7,50 / médiane 8,00 /
    max 9,17. `step` = rang 0..81 (mot humain, pas une mesure).
  - Valeurs : telles que déposées dans la matrice série, sans
    imputation, sans mise à l'échelle, sans correction. 0 NaN.
  - Portes §1–§2 du protocole : 5/5 OK (KRAS présent ; 11 gènes
    v4 exacts présents, DPCR1 absent ; MUCL3 présent ; DPCR1
    0 sonde ; 82/82 cas complets ≥ 40).

## 5. Nuls frais (graines 9301–9310)

- **Script gelé :** `nulls_lot_next/scripts/build_null_893.py`
  - SHA-256 : `572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467`
  - Méthode : permutation de lignes entières (les flux d'une
    tumeur voyagent ensemble), colonne de contrôle (`step`)
    inchangée ; assertions (contrôle inchangé, mêmes lignes en
    multiset, 0 valeur manquante).
  - Absence de collision vérifiée avant le gel (calcul exact) :
    9301–9310 ∩ {9101–9110, 9111–9300, 3000–3999, 42} = vide.
- **SHA-256 des 10 CSV nuls :**
  - s9301 : `e67eb8bf9058999cb50ead979dcb85cf9eaed89ef8c194f97162b1572eb96397`
  - s9302 : `d153a6db069cb4978e32dfd6881aa1f9b9f639c8ce3025d6d9ade01fa8d9abf4`
  - s9303 : `35d94cfc38ac3a360909abd338672017e04958567fa6eab1967a4e5dbf480cb4`
  - s9304 : `bcf812b45b99942a7e5b8d3e26bd5683a2cf17ed49d8d48b5ba8f7bdb1c5ba30`
  - s9305 : `0edc936ae72129322c0d3e4c477b0000a2d6108f0d5865c465720c829d0c12b7`
  - s9306 : `2edea177fd22c07f3b4a3ae1b1139d397febd77b2ccc28979e7e1ebbd89c50fe`
  - s9307 : `9b3e5791b62261cadcf855eec4324326eb35e64cba55ba4b216da81b8657b424`
  - s9308 : `5978da323470f4b05f37c7354b5e7584276c75195cd4f1d88c465dd3bb5ed904`
  - s9309 : `58e902210eadf30694d6e69a7c52dad581d49694e34673c310493209045777d8`
  - s9310 : `3f8dd19227385fca24611d0a179c380f2f83106a238e2d08230007738fd76bba`
- **Intégrité vérifiée après construction :** 10/10 (contrôle
  inchangé, mêmes lignes en multiset, 0 NaN, même forme 82 × 13).

## 6. Pipeline et runs

- **Pipeline :** `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`
  - SHA-256 : `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  - Vérifié avant le lot (12:37:38 UTC), après le lot (13:06:35 UTC)
    et avant l'extraction : inchangé 3/3. Fichier jamais modifié.
- **Lanceur :** `run_899.sh`
  - SHA-256 : `5741e9dddde2f507eebd08f7b1a4785eacf78515da0cb5dbda96c80e99ec3b7b`
  - Séquentiel, reprenable (saute tout run dont
    `master_results.json` existe), journal des exit codes.
  - Lancement : `systemd-run --unit=v62-899-gse184585 --collect`,
    jamais `nohup`, aucun dossier de run écrasé.
- **Journal :** `runs_899.log`
  - SHA-256 : `0ebca397af29f806eb0a83ad983ed76a71504ef4aee33e0fa981a73d3ac895ee`
  - Lot 27 nov. 2026 12:37:38 → 13:06:35 UTC (~29 min), 11/11 exit 0.
- **Dossiers de runs :** `results_fast_v62_899_gse184585` (réel) et
  `results_fast_v62_899_gse184585_nul_s9301` … `s9310` (10 nuls),
  11 `master_results.json` présents.
- **Commande (identique aux lots précédents) :**
  `python3 universal_v6.2.0_cohen.py --input <csv> --mode fast --output <dossier>`

## 7. Extraction et jugement

- **Script :** `extract_899.py`
  - SHA-256 : `939b90f6545672c6609980b82e8b0beac36efdf7c8f312481558e7c949c9d0fe`
  - Lit `master_results.json` →
    `run_pipeline/threshold_metadata/threshold_optimization/best_config`
    (metrics : max_separation, s_norm, stability, robustness,
    sharpness ; threshold). MC pipeline = 0,3·s_norm +
    0,3·stabilité + 0,2·robustesse + 0,2·sharpness (formule
    réplique §8.93, `replica_nulls_893.py` ; facteur 0,8 non
    appliqué : w_size fast 80 ≥ n//10 = 8).
  - Tests directs : Spearman de chaque flux vs KRAS (valeurs KRAS
    relues depuis la matrice série via le mapping gelé, méthode
    `pandas` Spearman).
  - Verdict selon la règle gelée §8.93 §4 (plancher 0,07).
- **Sortie :** `extraction_899.json`
  - SHA-256 : `ee175155cf8a867fe22d458f5b6e7beeb8bb47e6adbc90fb4830eb661a65abd7`
- **Vérification croisée de l'extraction :** `best_config` vs
  `raw_best_config`, 11/11 à 0,0 exact.
- **Résultats (valeurs produites par le pipeline et par
  l'extraction, pas par une main humaine) :**
  - maxsep réel 0,3712 (seuil 72,50 ; s_norm 0,1835 ; stabilité
    0,9905 ; robustesse 5,3×10⁻²⁷ ; sharpness 0,0152).
  - Nuls maxsep : s9301 0,2180 ; s9302 0,2251 ; s9303 0,2180 ;
    s9304 0,2737 ; s9305 0,2234 ; s9306 0,2032 ; s9307 0,1777 ;
    s9308 0,2935 ; s9309 0,2229 ; s9310 0,2822.
  - Médiane des nuls 0,2231 ; p95 0,2884 ; min 0,1777 ; max 0,2935.
  - Écarts réel−nul : 10/10 > 0,07 (100,0 %) ; min +0,0777
    (s9308) ; max +0,1935 (s9307) ; d contre médiane +0,1480 ;
    d contre p95 +0,0828 ; rang 11/11.
  - MC réel 0,3552 ; MC nuls médiane 0,3341, p95 0,3722.
  - Spearman vs KRAS : PGC +0,029 ; REG4 −0,048 ; CLDN18 +0,224 ;
    MUC17 +0,117 ; MUCL3 +0,176 ; CR2 −0,237 ; KRT20 −0,393 ;
    MUC2 −0,072 ; GSTM1 −0,304 ; CEACAM5 +0,550 ; CLCA1 −0,531 ;
    MUC16 +0,057. Δρ médian −0,0098 ; 6/12 positifs.
  - **Verdict : SOLIDE** (réel > p95 ET 100 % des nuls sous le
    plancher, règle §8.93 §4).

## 8. Fichiers du chantier (avec SHA-256)

- `PROTOCOL_899_gse184585.md` :
  `00f04748fe1d5416ffa47df467b878ab0c630afc6c7ba5a41090c4cea943057c`
  (gelé 27 nov. 2026 12h30 UTC, avant toute construction et tout run)
- `section_8.99_gse184585.md` :
  `6d423d5c124bec5c3c62c17eecb582f2c6771a423bc55d8d1bc13e74c28d9437`
- `PROVENANCE_899.md` : ce fichier.
- `build_fluxes_899.py` :
  `a9ede3eefae47a7d12fa6accd9400e7da4ed1afef3d0ce30b848e2c326956388`
- `pdac_899_gse184585_fluxes.csv` :
  `07540af57ef27974178036ea333f4ad51d9a19e49d7993f1d997b80fe6b99d13`
- 10 CSV nuls : voir §5.
- `run_899.sh`, `runs_899.log` : voir §6.
- `extract_899.py`, `extraction_899.json` : voir §7.
- Données sources : voir §1–§2.

## 9. Nature des lignes et ce qui manque

- **Nature des lignes :** chaque ligne du CSV réel est une tumeur
  PDAC primaire (MSKCC, réséquée) ; chaque colonne de flux est
  une mesure instrumentale d'expression (microarray HTA 2.0,
  valeurs déposées dans la matrice série) ; `step` est un rang
  humain (0..81, ordre KRAS ascendant), pas une mesure ; MUCL3
  est la mesure du gène historiquement nommé DPCR1 (remappage
  vérifié 5/5, §3). Aucune valeur n'est inventée, imputée ou
  mise à l'échelle. Le pipeline ne voit jamais la variable de
  contrôle physique ni la vérité terrain ; l'ordre KRAS est un
  axe d'analyse, pas un temps.
- **Ce qui manque / dettes nommées :**
  1. Consolidation à 200 nuls (non faite : 200 runs ≈ 12 h) —
     suite à faire, graines à geler par le coordinateur sans
     collision avec 9301–9310.
  2. Scores compagnons non extraits : Delta, L7a, falsification,
     F1/F2 après seuil.
  3. Mise à jour du registre A2/LOO (coordinateur ; A2 défini
     contre le nul graine 42, non couru ici).
  4. SOFT GEO GPL17586 complet (abandonné, > 1,2 Go — remplacé
     par les bases Bioconductor, §2).
  5. Étude aval Zhao et al. (BMC Genomics 2023, 24:101) ayant
     fusionné GSE184585 à d'autres jeux : non lue pour ce chantier.
- **Ce qui n'a pas été fait :** aucune modification du livre
  blanc, aucun PDF, aucune Release, aucun push GitHub ;
  `tlogNext-pdac-phase2` et `universal-log-research` non touchés ;
  pipeline jamais modifié ; aucune affirmation clinique ; aucune
  formulation de prédiction (formulations d'analyse uniquement).
