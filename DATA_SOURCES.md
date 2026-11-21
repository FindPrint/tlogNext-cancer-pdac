# DATA_SOURCES.md — Matrices brutes du projet PDAC v6 : reconstruction depuis zéro

**Objet :** permettre à un autre AI de reconstruire **toutes** les matrices brutes du projet PDAC (pipeline v6, livre blanc) depuis zéro, sans rien deviner.
**Projet :** `~/workspace/runs/pdac-v6/` — recherche non clinique sur le cancer du pancréas (mandat : trouver un remède, livre blanc public).
**Date de rédaction :** 19 novembre 2026.
**Révision §8.77 :** 21 novembre 2026 — toutes les URL manquantes du §17 ont été retrouvées et vérifiées par SHA-256 (voir §29, chantier §8.77) ; nouvelle §28 (sources du §8.76) et §29 (bilan du chantier). Aucun verdict du livre blanc n'est modifié par cette révision.
**Révision §8.83 :** 21 novembre 2026 — nouvelles §30 (inventaire §8.78, supplément Chen MOESM13), §31 (13e paire GSE57495 + arrêt C2 GDC, §8.79), §32 (TCGA-UVM, §8.81), §33 (TCGA-GBM, §8.82) et §34 (survie §8.83, aucune source nouvelle) ; §8.80 (veille clinique) sans donnée nouvelle. GSE57495 déjà couverte (ligne §21 / §8.69) — rappelée, pas re-ajoutée. Aucun verdict du livre blanc n'est modifié par cette révision.
**Périmètre :** tous les fichiers de `~/workspace/runs/pdac-v6/data/` (87 fichiers, ~2,44 Go) + un fichier brut hors `data/` (`data_clinical_patient.txt`, racine de `pdac-v6/`).
**Règle appliquée (Zackary, 27 oct. 2026 — provenance toujours nommée) :** chaque URL est copiée telle quelle depuis une provenance lue ; **aucune URL n'a été inventée**. Quand une URL n'est pas dans une provenance, c'est écrit noir sur blanc : « URL non consignée dans les provenances ».

## 0. Mode d'emploi

### 0.1 Script maître de re-téléchargement (existe déjà)

**`~/workspace/staging-pdac/download_data.sh`** — re-télécharge TOUS les jeux de données depuis leurs sources publiques et vérifie taille + MD5/SHA-256. Usage : `bash download_data.sh [dossier-destination, défaut : ./data]`.

**Limites connues du script — CORRIGÉES au §8.77** (voir §29 ; le script
corrigé est `repro_877/download_data_877.sh`, diff `repro_877/download_data_877.diff`) :
- PRISM 19Q4 : le script d'origine ne téléchargeait que **2 des 4** fichiers
  (`secondary-screen-cell-line-info.csv` et `secondary-screen-readme.txt`
  manquaient dans son dictionnaire `want`) — **corrigé** : les 4 fichiers
  sont téléchargés, avec leurs URL directes figshare en commentaire (§8).
- PANC-1 : la section d'origine téléchargeait le tarball
  `codeload.github.com/ncats/PANC1/tar.gz/refs/heads/main`, qui s'est révélé
  **tronqué** en pratique (569 815 185 o, erreur gzip « unexpected end of
  file ») — **corrigé** : téléchargement fichier par fichier via
  `raw.githubusercontent.com`, avec vérification taille + SHA-256 (§10).
- Le script d'origine ne téléchargeait pas : les suppléments Nature/Springer
  (ng3398 MOESM59–63, Birnbaum MOESM1–5), le SOFT GPL20769, les fichiers
  ICGC probe map / NMF, les fichiers cliniques QCMG,
  `Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv`, ni
  `data_clinical_patient.txt` — **corrigé** : toutes ces sections sont
  ajoutées, URL vérifiées par SHA-256 (§8.77).
- PRISM 24Q2 primaire : le script d'origine ne vérifiait **aucun hachage**
  (`check ... - -`) — **corrigé** : SHA-256/MD5 vérifiés (§7) et fichier de
  métadonnées des lignées ajouté.
- Le script corrigé complet (~2,4 Go) a été exécuté le 21 nov. 2026 dans
  le chantier §8.77 (unités `repro877-cold-full` puis
  `repro877-cold-full2` après un 403 transitoire, journaux
  `repro_877/cold/full_script_877.log` et `full_script_877b.log`) —
  résultat consigné au §29.

### 0.2 Conventions de ce document

- **Taille** : en octets exacts, tels que mesurés sur disque (`stat`) et consignés dans les provenances.
- **Hachage « consigné »** : valeur lue dans un fichier de provenance (fichier source cité entre parenthèses après chaque bloc).
- **Hachage « calculé localement le 19 nov. 2026 »** : SHA-256 (ou MD5) que j'ai calculé moi-même sur le fichier local (`sha256sum`/`md5sum`) quand la provenance ne donnait que l'autre hachage, une valeur tronquée (`…`), ou rien. Ces valeurs complètent les provenances, elles ne les remplacent pas ; quand les deux existent, elles concordent (vérifié fichier par fichier).
- **Date d'acquisition** : date du téléchargement consignée dans la provenance, ou date de modification du fichier local quand la provenance ne la donne pas (signalé).
- **Fichier dérivé** : produit par un script du projet à partir d'un brut (reconstructible, §14) — pas une source brute.

### 0.3 Inventaire rapide

| Catégorie | Nombre |
|---|---|
| Sources brutes distinctes couvertes | 16 |
| Fichiers `data/` de plus de 5 Mo | 19 — **19/19 couverts (§16)** |
| Fichiers `data/` au total | 87 (~2,44 Go) |
| Sources brutes avec URL complète pour leur(s) fichier(s) principal(aux) | **16 sur 16 (depuis §8.77, voir §17 révisé et §29)** |
| Sources brutes partielles (accès via API : figshare/Zenodo, pas d'URL directe par fichier) | 0 sur 16 — CPTAC, PRISM 24Q2, PRISM 19Q4 et QCMG ont désormais aussi leurs URL directes consignées (§6, §7, §8, §12) ; l'accès par API reste la voie du script quand elle fonctionne |
| Sources brutes sans URL | **0 sur 16 (depuis §8.77)** |

---

## 1. DepMap Public 24Q4 (Broad Institute) — CRISPR, copy-number, mutations

**Dépôt :** DepMap Public 24Q4, figshare article **27993248**, DOI `10.25452/figshare.plus.27993248.v1`.
**Page de l'article :** `https://doi.org/10.25452/figshare.plus.27993248.v1`
**Date d'acquisition :** 15 nov. 2026 (CRISPRGeneEffect.csv, Model.csv — journal `data/download_depmap.log`) ; 16 nov. 2026 (OmicsCNGene.csv, MAF, Hotspot, OmicsProfiles.csv).
**Re-téléchargement :** `~/workspace/staging-pdac/download_data.sh` (section DepMap 24Q4).

| Fichier local | Taille (octets) | URL exacte | SHA-256 consigné | MD5 consigné |
|---|---|---|---|---|
| `data/CRISPRGeneEffect.csv` | 428 678 699 | `https://ndownloader.figshare.com/files/51064667` | `3d8f3ec6dbf2db7ff834b79b508622ec0b226f3518003fe96ecf5a4fcf167e3b` | `6edf7ade09b9b34199210b559d4745d3` |
| `data/Model.csv` | 645 696 | `https://ndownloader.figshare.com/files/51065297` | `b7a0c1385e6cef30132b56aff61f1261d11e3f490490b355c430d32ee0dbdcfa` | `675210d17675f3517b0ce39a3c274f16` |
| `data/OmicsCNGene.csv` | 1 394 554 236 | `https://api.figshare.com/v2/file/download/51065324` (URL d'origine) — **voie utilisée dans le script corrigé §8.77 : `https://ndownloader.figshare.com/files/51065324`** (même fichier, ID 51065324 ; l'endpoint API est resté bloqué à 0 octet pendant 9+ min le 21 nov. 2026 alors que ndownloader servait le fichier immédiatement — test range HTTP 206, 672 Ko/s) | `4851d3e939d48837a39a0f01294deb90fa507a85703586a927b77474f999134c` | `4696565fa74dc805983bc278b4a41802` (exact, MD5 figshare annoncé) |
| `data/OmicsSomaticMutationsMAFProfile.maf` | 98 439 503 | `https://ndownloader.figshare.com/files/51065741` | `86b8530b31125305391dcffb7dffc5426535df63705a2bf76565368f3955e96f` | — (non consigné) |
| `data/OmicsSomaticMutationsMatrixHotspot.csv` | 4 210 723 | `https://ndownloader.figshare.com/files/51065750` | `6444ce819a28d4228ff7b748e309611c5830c551620d8d2c7f86052e2675e3d8` | — (non consigné) |
| `data/OmicsProfiles.csv` | 254 733 | `https://ndownloader.figshare.com/files/51065723` | `0bb19ee57935d4b213d378a4db9caacaa1db7318a63ae81485d84f91c20a3bf2` | — (non consigné) |

**Contenu :** `CRISPRGeneEffect.csv` = effets Chronos CRISPR (1re colonne sans nom = ModelID index ; colonnes « SYMBOLE (Entrez) ») ; `Model.csv` = métadonnées des lignées (68 pancréas `OncotreeLineage == Pancreas`, 45 adénocarcinomes dans GeneEffect) ; `OmicsCNGene.csv` = copy-number relatif **linéaire** (1,0 = diploïde ; 0 = délétion homozygote — **pas** log2 depuis 24Q2) ; MAF = mutations somatiques (colonne `Protein_Change` pour les allèles KRAS) ; Hotspot = matrice 0/1/2 ; `OmicsProfiles.csv` = jointure ProfileID `PR-…` → ModelID `ACH-…`.
**Journaux :** `data/download_depmap.log` (CRISPR + Model, 15 nov. 2026), `data/download_omicscn.log` (**vide, 0 octet** — le téléchargement OmicsCN est consigné dans `PROVENANCE_prmt5_mtap.md`, pas dans un log).
(Source : `PROVENANCE_depmap.md`, `PROVENANCE_prmt5_mtap.md`, `PROVENANCE_kras_g12d.md`, `PROVENANCE_mtap_arbitration_840.md`, `~/workspace/staging-pdac/download_data.sh`)

---

## 2. TCGA — Broad GDAC Firehose, run 2016-01-28 (PAAD, LUAD, COAD)

**Dépôt :** Broad GDAC Firehose `stddata__2016_01_28` (ARN-seq RSEM) et `analyses__2016_01_28` (GISTIC2 copy-number).
**Date d'acquisition :** 15 nov. 2026 (PAAD RSEM — journal `data/download_firehose.log`) ; 16 nov. 2026 (LUAD, COAD, GISTIC — dates de fichiers 16 nov. 19h38).
**Re-téléchargement :** `~/workspace/staging-pdac/download_data.sh` (section TCGA Firehose 2016-01-28).

### 2.1 PAAD — ARN-seq RSEM normalisé

- **Fichier local :** `data/tcga_paad_rsem.tar.gz` — **15 296 232 octets**
- **URL du répertoire (consignée) :** `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/PAAD/20160128/`
- **URL exacte du tarball (dans `download_data.sh`) :** `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/PAAD/20160128/gdac.broadinstitute.org_PAAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz`
- **MD5 vérifié (consigné) :** `b09569ce3f4721f514bc137bd109ac0a` (aussi dans `data/tcga_paad_rsem.tar.gz.md5`)
- **SHA-256 (calculé localement le 19 nov. 2026 ; les provenances ne consignent que le MD5) :** `c3dd138b3257ad5bae5a58160f5607d2ad9c2871c83f6cdb5959cc9116d262c9`
- **Contenu :** matrice interne `PAAD.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt`, 20 503 gènes × 183 échantillons, RNA-seq V2 RSEM normalisé (TCGA, UNC Illumina HiSeq) ; 178 tumeurs primaires retenues (code TCGA 01), transformation log2(RSEM+1).
(Source : `PROVENANCE_tcga.md`, `PROVENANCE_parp_v6.md`, `~/workspace/staging-pdac/download_data.sh`)

### 2.2 PAAD — Copy-number GISTIC2

- **Fichier local :** `data/tcga_paad_gistic.tar.gz` — **26 189 717 octets**
- **URL du répertoire (consignée) :** `https://gdac.broadinstitute.org/runs/analyses__2016_01_28/data/PAAD/20160128/`
- **URL exacte du tarball (dans `download_data.sh`) :** `https://gdac.broadinstitute.org/runs/analyses__2016_01_28/data/PAAD/20160128/gdac.broadinstitute.org_PAAD-TP.CopyNumber_Gistic2.Level_4.2016012800.0.0.tar.gz`
- **MD5 vérifié (consigné) :** `816034f742e8f89ca8734ca2cf4404d5` (aussi dans `data/tcga_paad_gistic.tar.gz.md5`)
- **SHA-256 vérifié (consigné) :** `6edc20f365d2f828bf5b4ef90a93f67344928d069cdd138eb946ed3275eed0ed`
- **Contenu :** fichier interne `all_thresholded.by_genes.txt` (24 776 gènes × 183 échantillons) ; −2 = délétion profonde, −1 = perte peu profonde, 0 = diploïde, +1/+2 = gains ; 177 tumeurs appariées à l'expression. (Le fichier `all_data_by_genes.txt`, log2 ratio, est dans le même tarball et sert pour le CN MTAP continu, §8.33/PROVENANCE_mtap_series.md.)
(Source : `PROVENANCE_mtap.md`, `PROVENANCE_mtap_pancancer.md`, `PROVENANCE_mtap_series.md`, `~/workspace/staging-pdac/download_data.sh`)

### 2.3 LUAD — ARN-seq RSEM normalisé

- **Fichier local :** `data/tcga_luad_rsem.tar.gz` — **47 043 687 octets**
- **URL du répertoire (consignée) :** `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/LUAD/20160128/`
- **URL exacte du tarball (dans `download_data.sh`) :** `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/LUAD/20160128/gdac.broadinstitute.org_LUAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz`
- **MD5 observé (consigné ; aucun MD5 de référence publié par Firehose pour LUAD) :** `4c36eec3f6df75630292c5a569cfc8f4` (aussi dans `data/tcga_luad_rsem.tar.gz.md5`)
- **SHA-256 (calculé localement le 19 nov. 2026 ; corrigé §8.77, 21 nov. 2026 — la consignation d'origine portait 65 caractères, un `d` en trop : `…cf73f1daf2` au lieu de `…cf73f1af2`) :** `472c88d09aa5d3efa05da3cd0645f411191f6518e01f493f1d960abcf73f1af2` (vérifié sur le fichier local et sur le re-téléchargement à froid, identiques)
- **Contenu :** 20 503 gènes × 576 échantillons ; 515 tumeurs primaires retenues (61 écartées), log2(RSEM+1).
(Source : `PROVENANCE_pancancer.md`, `~/workspace/staging-pdac/download_data.sh`)

### 2.4 COAD — ARN-seq RSEM normalisé

- **Fichier local :** `data/tcga_coad_rsem.tar.gz` — **26 401 036 octets**
- **URL du répertoire (consignée) :** `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/COAD/20160128/`
- **URL exacte du tarball (dans `download_data.sh`) :** `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/COAD/20160128/gdac.broadinstitute.org_COAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz`
- **MD5 observé (consigné ; aucun MD5 de référence publié par Firehose pour COAD) :** `e703a630556d42f098cf0df87d4712bb` (aussi dans `data/tcga_coad_rsem.tar.gz.md5`)
- **SHA-256 (calculé localement le 19 nov. 2026) :** `7df21e8e851382d1927bf76ca1fe7ac540420babf9595047c5a4a41dfc39ee6e`
- **Contenu :** 20 503 gènes × 328 échantillons ; 285 tumeurs primaires retenues (43 écartées), log2(RSEM+1).
(Source : `PROVENANCE_pancancer.md`, `~/workspace/staging-pdac/download_data.sh`)

---

## 3. GEO GSE71729 — Moffitt et al. 2015, PDAC (ARN, puce Agilent)

**Série :** GEO GSE71729 — « Virtual Microdissection of Pancreatic Ductal Adenocarcinoma Reveals Tumor and Stroma Subtypes » (Moffitt et al., 2015, *Nat Genet* 47:1168–78, DOI `10.1038/ng.3398`).
**Fiche GEO :** `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE71729`
**Date d'acquisition :** 15 nov. 2026, 14:17 UTC.
**Re-téléchargement :** `~/workspace/staging-pdac/download_data.sh` (section GEO).

- **Fichier local :** `data/GSE71729_series_matrix.txt.gz` — **15 622 315 octets**
- **URL exacte (consignée) :** `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE71nnn/GSE71729/matrix/GSE71729_series_matrix.txt.gz`
- **SHA-256 vérifié (consigné) :** `b228789314ec4d866ec51b65724664abaa24b822577c55d3727820c867536a54`
- **Plateforme :** GPL20769 — Agilent-014850 Whole Human Genome Microarray 4x44K G4112F (version « Gene Symbol », juil. 2014).
- **Contenu :** 19 749 symboles de gènes × 357 échantillons (145 tumeurs primaires, 61 métastases, 134 normaux, 17 lignées) ; valeurs log2 Cy5, sondes déjà agrégées par symbole par les auteurs (moyenne), normalisation par quantile ; survie par patient DANS la matrice (champs `survival_months` / `death_event_1death_0censor`, 125 patients, 84 décès).
(Source : `PROVENANCE_geo71729.md`, `PROVENANCE_geo71729_survival.md`)

### 3.1 Annotation GPL20769 (fichier SOFT — NON conservé ; fichier .annot.gz = page 404)

- **Fichier SOFT de la famille GPL20769 : 37 588 662 octets, téléchargé le 15 nov. 2026** (table de 19 749 lignes) — **fichier absent de `data/`** (non conservé après extraction).
- **URL exacte (retrouvée et vérifiée §8.77, 21 nov. 2026) :** `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL20nnn/GPL20769/soft/GPL20769_family.soft.gz` — re-téléchargé le 21 nov. 2026 : taille 37 588 662 o exactement, table 19 750 lignes (en-tête + 19 749 lignes), titre confirmé (« Agilent-014850 Whole Human Genome Microarray 4x44K G4112F (Gene Symbol Version; updated July 2014) »). **MD5 :** `4c39e802ec78170d7ed5c8c2cc2b0bec` ; **SHA-256 :** `ecb1b79a6b89e521a1116a3113fcb9a5af1c181329eec8257e044e0683822d3e` (calculés le 21 nov. 2026 sur le fichier re-téléchargé). **Note :** le chemin deviné au §15.4 (`GPL2nnn/`) donne 404 — le regroupement GEO masque les 3 derniers chiffres (20769 → `GPL20nnn`, comme 6244 → `GPL6nnn` au §4.1).
- **Fichier local :** `data/GPL20769.annot.gz` — **990 octets** — ce n'est PAS une annotation : vérifié le 19 nov. 2026, c'est une page HTML d'erreur « Object not found! » (le `.annot.gz` n'existe pas sur le FTP GEO, HTTP 404 — consigné dans `PROVENANCE_geo71729.md`). À ne pas utiliser ; le SOFT a servi à la place.
(Source : `PROVENANCE_geo71729.md`)

### 3.2 Suppléments Nature de Moffitt et al. 2015 (ng3398, MOESM59–63)

Téléchargés le 16 nov. 2026 (dates de fichiers 16 nov. 12:09). **URL retrouvées et vérifiées §8.77 (21 nov. 2026)** — patron Springer `static-content.springer.com/esm/art%3A10.1038%2Fng.3398/MediaObjects/41588_2015_BFng3398_MOESM{n}_ESM.{ext}` (code revue 41588 = *Nature Genetics* ; même patron que le fichier Bailey MOESM270 du §5.5) ; les 5 fichiers ont été re-téléchargés le 21 nov. 2026 et leurs tailles + SHA-256 vérifiés identiques à ceux ci-dessous. (Avant §8.77 : URL non consignée dans `PROVENANCE_geo71729_survival.md` — seuls noms, tailles et SHA tronqués.) Les SHA-256 complets ci-dessous ont été calculés localement le 19 nov. 2026 ; leurs préfixes correspondent aux valeurs tronquées consignées.

| Fichier local | Taille (octets) | SHA-256 (calculé localement, préfixe conforme au consigné) | Contenu (selon la provenance) |
|---|---|---|---|
| `data/ng3398_MOESM59_ESM.pdf` | 5 339 711 | `c18dbc59b72733e170720f50c2d7f39c1cfdbac2ceb4d1bbdf16af0fb5d320c0` | Figures suppl. + tableau 3 — pas de survie par patient |
| `data/ng3398_MOESM60_ESM.txt` | 19 393 438 | `516cf2eb976adb580b69979a0fae787e9728c463d924b574f8b56ac78a44c7db` | Matrice d'expression + annotations (mutation KRAS, CAF, PDX, lignée, primaire, sous-type Collisson) — aucune ligne de survie |
| `data/ng3398_MOESM61_ESM.xlsx` | 460 785 | `ec26858b1b3394c4dcb65b17310612e84d0b58b8cc2309d6d2cba65a8c1c01ad` | Tableau 1, enrichissements de signatures par facteur NMF |
| `data/ng3398_MOESM62_ESM.xlsx` | 2 612 836 | `25c35346ec98bf067b563c943b7f74ac5bb78454a0191f22216a982196d08b5c` | Tableau 2, factorisation des gènes |
| `data/ng3398_MOESM63_ESM.xlsx` | 14 141 | `3d508a54d97f93d5f203ed9f431efe0e5f4699df41613c9b377257bb48020905` | Tableau 4, correspondance ID Moffitt ↔ GSM Stratford |
(Source : `PROVENANCE_geo71729_survival.md`)

---

## 4. GEO GSE62452 — Hussain et al., PDAC (ARN, puce Affymetrix HuGene-1.0-ST)

**Série :** GEO GSE62452 — « Microarray gene-expression profiles of 69 pancreatic tumors and 61 adjacent non-tumor tissue from patients with pancreatic ductal adenocarcinoma » (soumise 17 oct. 2014, publique 1er juil. 2016, mise à jour 26 juil. 2018 ; BioProject PRJNA264183 ; PMID **27197190**).
**Fiche GEO :** `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE62452`
**Date d'acquisition :** 15 nov. 2026, 15:23 UTC (premier téléchargement tronqué à 12 943 600 o — re-téléchargé complet ; le SHA ci-dessous est celui du fichier complet vérifié).
**Re-téléchargement :** `~/workspace/staging-pdac/download_data.sh` (section GEO).

- **Fichier local :** `data/GSE62452_series_matrix.txt.gz` — **14 447 291 octets**
- **URL exacte (consignée) :** `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62452/matrix/GSE62452_series_matrix.txt.gz`
- **SHA-256 vérifié (consigné) :** `8f41d5b3f11451e653fd6bfc0c6b216c219d46711a7676d1e453dee16a078cba`
- **Plateforme :** **GPL6244** — [HuGene-1_0-st] Affymetrix Human Gene 1.0 ST Array, 33 297 transcript clusters (la tâche annonçait GPL570 par erreur ; la matrice dit GPL6244, `!Series_platform_id "GPL6244"`, ID_REF numériques).
- **Contenu :** intensités normalisées log2 (RMA-like, 0,22–13,60, médiane 4,31, 0 valeur manquante) ; 130 échantillons : 69 tumeurs + 61 tissus adjacents non tumoraux ; les auteurs ont fusionné deux lots (échantillons 1–90 soumis comme GSE28735) et retiré l'effet de lot avec Partek (non vérifiable depuis la matrice). Données cliniques / survie absentes ; le fichier supplémentaire `GSE62452_paired_sample_information.xlsx` (listé dans la série) **n'a pas été téléchargé**.
(Source : `PROVENANCE_geo62452.md`)

### 4.1 Annotation GPL6244 (table sonde → symbole, dérivée du SOFT)

- **Fichier local (dérivé) :** `data/GPL6244_probe2symbol.tsv` — **382 034 octets** — SHA-256 (calculé localement le 19 nov. 2026) : `d1a9cf25c68e4ffbf6c65ec2ab2f2b07610d0ad0d0a3c0ff1bc388336c836815`
  - **Écart relevé :** `PROVENANCE_geo62452.md` indique « 819 249 octets » pour ce fichier — c'est la taille de `GPL570_probe2symbol.tsv` (voir §4.2). Vérifié le 19 nov. 2026 : le fichier GPL6244 contient bien 25 293 sondes avec symbole (25 294 lignes avec l'en-tête, IDs numériques `7896738…`), conforme au contenu décrit dans la provenance ; seule la taille consignée est erronée (copie de la taille GPL570).
- **URL exacte du SOFT source (dans le script `download_gpl6244_mapping.py`) :** `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL6nnn/GPL6244/soft/GPL6244_family.soft.gz`
- **Méthode :** extraction en streaming du SOFT (plusieurs centaines de Mo, transfert coupé après le marqueur `!platform_table_end`) ; colonne `gene_assignment`, forme `accession // SYMBOLE // description // bande // Entrez` (première assignation prise) ; table complète vérifiée : 33 297 lignes, 25 293 sondes avec symbole, 23 307 symboles uniques. **Le SOFT lui-même n'est pas conservé dans `data/`** (re-téléchargeable par l'URL ci-dessus).
- **Script :** `~/workspace/runs/pdac-v6/download_gpl6244_mapping.py`
(Source : `PROVENANCE_geo62452.md`, `download_gpl6244_mapping.py`)

### 4.2 Fausse piste GPL570 (fichier dérivé, NON utilisé)

- **Fichier local (dérivé, non utilisé) :** `data/GPL570_probe2symbol.tsv` — **819 249 octets** — SHA-256 (calculé localement le 19 nov. 2026) : `e712097617d3a8811bbf96975cf32db988946ff2a4ea67c425c04899d5af7771` (45 782 sondes, 22 880 symboles). Extrait avant de constater que la plateforme était GPL6244.
- **URL tentées (consignées, HTTP 404 — GPL570 est en fait sous `GPLnnn/`, pas `GPL5nnn/`) :** `.../GPL5nnn/GPL570/annot/GPL570.annot.gz` et `.../GPL5nnn/GPL570/soft/GPL570_family.soft.gz` (chemins consignés avec préfixe `...` = `ftp.ncbi.nlm.nih.gov/geo/platforms/`).
(Source : `PROVENANCE_geo62452.md`)

---

## 5. ICGC PACA-AU — expression (miroir UCSC Xena) + clinique Bailey 2016

### 5.1 Portail ICGC DCC d'origine — MORT (voir §15)

- **URL tentée (consignée) :** `https://dcc.icgc.org/api/v1/download?fn=/current/Projects/PACA-AU/donor.PACA-AU.tsv.gz` (et `.../exp_seq.PACA-AU.tsv.gz`, puis `/release_28/` et `/release_29/`).
- **Résultat vérifié le 16 nov. 2026 :** HTTP 301 puis 200 vers `https://dcc.icgc.org/index.html` (page HTML, 2 733 octets). L'API `/api/v1/download` et `/api/v1/releases` ne servent plus de fichiers : le portail DCC est décommissionné. Les fichiers `donor.PACA-AU.tsv.gz` / `exp_seq.PACA-AU.tsv.gz` (avec `donor_survival_time`, `donor_vital_status`) n'ont **pas** pu être téléchargés à la source ; remplacés par les sources vérifiées ci-dessous (mêmes patients, Bailey et al. 2016).
(Source : `PROVENANCE_icgc.md`)

### 5.2 Expression — UCSC Xena, hub ICGC (miroir vérifié)

- **Fichier local :** `data/icgc_pacaau_exp.txt.gz` — **9 841 881 octets**
- **URL exacte (corrigée §8.77, 21 nov. 2026) :** `https://icgc.xenahubs.net/download/PACA-AU/nature16965-s2_normalised_exp.txt.gz` (hub Xena, redirige 302 vers le bucket) — re-téléchargée le 21 nov. 2026 : 9 841 881 o, SHA-256 `c2cb57af3ba4c3d7fdac292e66c81067d36e16aae9efdd8005147e20820f49fa` (identique au consigné). **Ancienne URL S3 directe `https://icgc-xena-hub.s3.amazonaws.com/download/PACA-AU/nature16965-s2_normalised_exp.txt.gz` : HTTP 403 (4 tentatives, exécution full5 du script complet, 21 nov. 2026) — ne plus utiliser.**
- **SHA-256 vérifié (consigné) :** `c2cb57af3ba4c3d7fdac292e66c81067d36e16aae9efdd8005147e20820f49fa`
- **Jeu Xena :** `PACA-AU/nature16965-s2_normalised_exp.txt`, cohorte PACA-AU, 96 échantillons, gene expression, log2(cpm), version 2016-09-09 ; citation : Bailey et al., *Nature* 531, 47–52 (2016), doi `10.1038/nature16965`. Table de référence `XenaData` du paquet UCSCXenaTools (`https://raw.githubusercontent.com/ShixiangWang/UCSCXenaTools/master/data/XenaData.rda`, 2 314 jeux). Le hub `https://icgc.xenahubs.net/download/...` redirige (302) vers le bucket S3 `icgc-xena-hub` ; l'objet non-gzippé renvoie 403, l'objet `.gz` existe.
- **Contenu vérifié :** 18 278 gènes (Ensembl) × 96 échantillons (ICGC_0006…), valeurs log2(cpm), 0 valeur manquante ; 70 tumeurs primaires PDAC retenues après filtre (`Sample type == 'Primary tumour'` ET `HistoSubtype == 'Pancreatic Ductal Adenocarcinoma'`).
- **Date d'acquisition :** 16 nov. 2026 (date de fichier 16 nov. 12:13).
- **Re-téléchargement :** `~/workspace/staging-pdac/download_data.sh` (section ICGC / Xena).
(Source : `PROVENANCE_icgc.md`)

### 5.3 Mapping gènes Ensembl → symbole (probe map Xena)

- **Fichier local :** `data/icgc_pacaau_probemap.gz` — **353 314 octets**
- **SHA-256 vérifié (consigné) :** `b09a746f6084215beea3632b72e87834ea577d18fcb52add3641de5d0d975537`
- **Jeu Xena (consigné) :** `PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp`
- **URL exacte (retrouvée et vérifiée §8.77, 21 nov. 2026) :** `https://icgc.xenahubs.net/download/PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp.gz` — re-téléchargée le 21 nov. 2026 : taille 353 314 o, SHA-256 `b09a746f6084215beea3632b72e87834ea577d18fcb52add3641de5d0d975537` (identique au consigné). **Note :** le listing du bucket S3 renvoie 403 et l'URL S3 directe (`icgc-xena-hub.s3.amazonaws.com/download/PACA-AU/…`) renvoie 403 aussi — c'est l'URL du hub qui fonctionne (le hub redirige vers le bucket).
- **Contenu :** 18 108 ENSG → 18 077 symboles ; médiane par symbole en cas de duplicata ; les 13 gènes (12 flux + KRAS) mappent chacun à un seul ENSG.
- **Date d'acquisition :** 16 nov. 2026 (date de fichier 16 nov. 12:13).
(Source : `PROVENANCE_icgc.md`)

### 5.4 Sous-types NMF (Bailey et al. 2016)

- **Fichier local :** `data/icgc_pacaau_nmf.txt.gz` — **447 octets**
- **SHA-256 vérifié (consigné) :** `f1e84b997c24903c216fbe9806c1b048cd9f552894e018ca54d02b5413921e2f`
- **Jeu Xena (consigné) :** `PACA-AU/nature16965-s2_NMF_class_assignment.txt`
- **URL exacte (retrouvée et vérifiée §8.77, 21 nov. 2026) :** `https://icgc.xenahubs.net/download/PACA-AU/nature16965-s2_NMF_class_assignment.txt.gz` — re-téléchargée le 21 nov. 2026 : taille 447 o, SHA-256 `f1e84b997c24903c216fbe9806c1b048cd9f552894e018ca54d02b5413921e2f` (identique au consigné). **Note :** le fichier distant est bien `.txt.gz` (le `.txt` nu renvoie 404 sur le hub) ; même remarque que §5.3 pour l'URL S3 directe (403).
- **Contenu :** 96 échantillons : Pancreatic Progenitor 30, Squamous 25, Immunogenic 25, ADEX 16.
- **Date d'acquisition :** 16 nov. 2026 (date de fichier 16 nov. 12:13).
(Source : `PROVENANCE_icgc.md`)

### 5.5 Clinique et survie — Bailey et al. 2016, Supplementary Tables 1–13

- **Fichier local :** `data/bailey2016_suppl_tables1-13.xlsx` — **22 104 569 octets**
- **URL exacte (consignée) :** `https://static-content.springer.com/esm/art%3A10.1038%2Fnature16965/MediaObjects/41586_2016_BFnature16965_MOESM270_ESM.xlsx`
- **SHA-256 vérifié (consigné) :** `778224b36343c6c65b6df49b0149219ba2038cbdec2333b96e4e8798ff74258a`
- **Source :** *Nature*, article nature16965, fichier MOESM270 (« This file contains Supplementary Tables 1-13 », XLSX 21 586 ko).
- **Feuille utilisée :** 'Supp Table 1 Clinical' (458 patients, 24 colonnes) ; colonnes de survie `Status` + `Length of Follow Up (months)`.
- **Date d'acquisition :** 16 nov. 2026 (date de fichier 16 nov. 12:15).
- **Re-téléchargement :** `~/workspace/staging-pdac/download_data.sh` (section ICGC / Xena).
(Source : `PROVENANCE_icgc.md`)

---

## 6. CPTAC PDAC — protéomique (étude PDC000393, Cao et al. 2021, *Cell*)

**Étude :** CPTAC PDAC — Cao et al., 2021, *Cell*, « Proteogenomic characterization of pancreatic ductal adenocarcinoma ». Étude PDC **PDC000393** (Proteomic Data Commons, NCI).
**Voie d'accès réelle :** miroir Zenodo du paquet Python `cptac` (PayneLab), record **8394329** (« CPTAC - first test », DOI `10.5281/zenodo.8394329`), lui-même issu du PDC PDC000393. L'API GraphQL du PDC (`https://pdc.cancer.gov/graphql`, accès ouvert, sans authentification) a été testée et répond, mais l'exploration de son schéma était lente et l'introspection désactivée ; le miroir Zenodo contient les mêmes fichiers sources (mêmes sommes MD5 que celles du PDC). **L'accès PDC n'était pas contrôlé ni bloqué** — le miroir a été choisi pour sa simplicité, pas par nécessité.
**Page du record :** `https://zenodo.org/records/8394329` — **API Zenodo (utilisée par `download_data.sh`) :** `https://zenodo.org/api/records/8394329` (les URL de fichiers individuels sont lues dans la réponse de l'API — champ `links.self` de chaque fichier — par le script).
**URL directes par fichier (lues dans la réponse de l'API le 21 nov. 2026, §8.77 ; tailles et MD5 conformes au tableau ci-dessous) :**
- Report UMich : `https://zenodo.org/api/records/8394329/files/umich-pdac-proteomics-Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz/content`
- BCM Tumor : `https://zenodo.org/api/records/8394329/files/bcm-pdac-proteomics-PDAC_proteomics_gene_abundance_log2_reference_intensity_normalized_Tumor.txt.gz/content`
- Mapping UMich : `https://zenodo.org/api/records/8394329/files/umich-pdac-mapping-aliquot_to_patient_ID.tsv.gz/content`
- `cptac_genes.csv` : `https://zenodo.org/api/records/8394329/files/cptac_genes.csv/content`
**Date d'acquisition :** 15 nov. 2026, 13h48–13h49 UTC.
**Re-téléchargement :** `~/workspace/staging-pdac/download_data.sh` (section CPTAC, via API Zenodo).

| Fichier local | Taille (octets) | MD5 vérifié (consigné, Zenodo = local, exact) | SHA-256 vérifié (consigné) |
|---|---|---|---|
| `data/cptac/umich-pdac-proteomics-Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz` | 20 504 572 | `a8c89b796b8ddacd48609e8ca7aac676` | `336d148faa5ca48054acdb6c03c723b6da9873eaeb6b641b028390ecaaad29a5` |
| `data/cptac/bcm-pdac-proteomics-PDAC_proteomics_gene_abundance_log2_reference_intensity_normalized_Tumor.txt.gz` | 7 382 441 | `988150c28a2c1db14a3c0e62d08c06d2` | `682b725cef0f2f815f6dc1b3966376450d414c30ffc2a561ca78a1211038375f` |
| `data/cptac/umich-pdac-mapping-aliquot_to_patient_ID.tsv.gz` | 22 881 | `b013fad4a8f9fa26aa3915c0ef636754` | `ed16d5287a2a5121a9ad91f3b74325e0e6d6cca24dd9ff75e715ead4da5c6ddc` |
| `data/cptac/cptac_genes.csv` | 462 309 | `afc250790ed6d18a7624a38fb872f62a` | `db232c7cbf76d1791972fef41a830783a9b5db29f37ed83832648e114691b6fe` |

**Contenu :** matrice UMich = protéomique TMT 11-plex niveau protéine (ratios log, abondance moins intensité de référence du plex) ; matrice BCM = abondances gène log2 normalisées sur référence (52 tumeurs C3L + 53 normales C3N dans le fichier dit « Tumor ») ; mapping aliquote → patient ; `cptac_genes.csv` = table de gènes du paquet. Cohorte UMich reconstruite : 68 tumeurs, 11 419 gènes ; BCM : 52 tumeurs (contre-vérification).
**Fichiers dérivés (voir §14) :** `data/cptac/pdac_umich_protein_gene_matrix.csv` (12 365 808 o, reconstruite par `scripts/build_matrix_umich.py` depuis le Report UMich) et `data/cptac/pdac_umich_coverage.json` (2 251 o).
(Source : `PROVENANCE_cptac.md`, `~/workspace/staging-pdac/download_data.sh`)

---

## 7. PRISM Repurposing Public 24Q2 — criblage primaire (Broad Institute)

**Jeu :** PRISM Repurposing Public 24Q2 (Broad Institute), figshare article **25917643**, DOI `10.6084/m9.figshare.25917643.v1`.
**Page de l'article :** `https://figshare.com/articles/dataset/Repurposing_Public_24Q2/25917643` (DOI `https://doi.org/10.6084/m9.figshare.25917643.v1` — URL de la page trouvée par recherche web et consignée dans `source_registry.md`, pas dans une provenance du projet).
**Date d'acquisition :** 15 nov. 2026 (dates de fichiers 15 nov. 13:36–13:37).
**Re-téléchargement :** `~/workspace/staging-pdac/download_data.sh` (section PRISM, primaire 24Q2) — **sans vérification de hachage** (le script passe `- -`) ; les hachages ci-dessous proviennent de `PROVENANCE_mtap_arbitration_840.md` et ont été re-vérifiés localement le 19 nov. 2026 (concordants).

| Fichier local | Taille (octets) | URL exacte | SHA-256 consigné | MD5 consigné |
|---|---|---|---|---|
| `data/Repurposing_Public_24Q2_Extended_Primary_Data_Matrix.csv` | 72 456 953 | `https://ndownloader.figshare.com/files/46630984` | `3b6554cfc6c765af53088a676edc7bce00ee7d84fe808b93bbfa892de607bc3d` | `042b15d3ebcc138a80a571b9286451ae` |
| `data/Repurposing_Public_24Q2_Extended_Primary_Compound_List.csv` | 719 567 | `https://ndownloader.figshare.com/files/46630981` | `7e78f5901c1a97d2baab0789ab89832e716388da4eacaa9f094e7d2f2f5a3463` | — (non consigné) |
| `data/Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv` | 157 294 | `https://ndownloader.figshare.com/files/46630978` (**retrouvée §8.77** via l'API figshare `https://api.figshare.com/v2/articles/25917643`, fichier 46630978 ; re-téléchargée le 21 nov. 2026, taille et SHA-256 identiques ; ajoutée au script corrigé) | `13a85da9e45656c455d3911a4491f3636d7d0975a9d2333dc3d0a3e2cd3b0526` | — (non consigné) |

**Contenu :** matrice primaire étendue = log-fold-change de viabilité, une seule dose (2,5 µM) ; 6 790 composés (6 789 uniques après déduplication d'un ID BRD en double, AZ-628) ; liste des composés (6 790 lignes) ; métadonnées des lignées.
(Source : `PROVENANCE_kras_g12d.md`, `PROVENANCE_mtap_arbitration_840.md`, `source_registry.md`, `~/workspace/staging-pdac/download_data.sh`)

---

## 8. PRISM Repurposing 19Q4 — écran secondaire, dose-réponse (Corsello et al. 2020)

**Jeu :** PRISM Repurposing 19Q4 Dataset, Corsello et al., *Nat Cancer* 2020, 1:235–248, DOI `10.1038/s43018-019-0018-6`.
**Dépôt :** figshare, article **9393293**, DOI `10.6084/m9.figshare.9393293.v4`, publié 2019-12-17.
**Accès :** le portail DepMap (`depmap.org/portal/download/all/?releasename=PRISM+Repurposing+19Q4`) renvoie une page de vérification Cloudflare Turnstile (vérifié 16 nov. 2026, 12h43 : le fichier téléchargé n'est que du HTML, 4 937 octets). Contournement : téléchargement direct via l'API figshare (`https://api.figshare.com/v2/articles/9393293`), mêmes fichiers, MD5 vérifiés. Journal des tentatives : `prism_secondary_access.log` (racine de `pdac-v6/`).
**Date d'acquisition :** 16 nov. 2026, 12:43.
**Re-téléchargement :** `~/workspace/staging-pdac/download_data.sh` (section PRISM, secondaire 19Q4) — **mais seulement 2 des 4 fichiers** (voir §0.1) ; les 4 fichiers s'obtiennent via l'API figshare ci-dessus (champ `download_url` de chaque fichier dans la réponse JSON).

| Fichier local | Taille (octets) | MD5 vérifié (consigné) | SHA-256 |
|---|---|---|---|
| `data/secondary-screen-dose-response-curve-parameters.csv` | 264 340 589 | `e629b9d505ad3d6bf65fde96f1c54bee` | `88d1013506e0cd6f191a51c5f3fdd3fb2be54f8afb4e19a5d1f8538e81fbfec8` (consigné, `PROVENANCE_mtap_arbitration_840.md`) |
| `data/secondary-screen-replicate-collapsed-treatment-info.csv` | 3 788 355 | `54765b3639f91cede751378d694e3583` | `9d0d1fb4faa87a63cd84965ec5e2b55a9df5680520a41b029abb679cfd4384f7` (calculé localement le 19 nov. 2026) |
| `data/secondary-screen-cell-line-info.csv` | 40 979 | `6737b4aa9fd85404fd2f0cf825b037e4` | `b93436b5f4bcf5fd14589697be4ca8f99ffd99d639223080380bc514c3718d27` (calculé localement le 19 nov. 2026) |
| `data/secondary-screen-readme.txt` | 7 647 | `421d0bbadec381adc0d7981ee7e16bd7` | `ed453e2bbaecff26cf923d8a69290f2c18fd7488d5a7d6903821980e6d49c99d` (calculé localement le 19 nov. 2026) |

**URL exactes des fichiers individuels (lues dans la réponse de l'API figshare `https://api.figshare.com/v2/articles/9393293` le 21 nov. 2026, §8.77 ; les 4 fichiers ont été re-téléchargés et vérifiés — tailles, MD5 et SHA-256 conformes au tableau ci-dessous) :**
- `secondary-screen-dose-response-curve-parameters.csv` : `https://ndownloader.figshare.com/files/20237739`
- `secondary-screen-replicate-collapsed-treatment-info.csv` : `https://ndownloader.figshare.com/files/20237763`
- `secondary-screen-cell-line-info.csv` : `https://ndownloader.figshare.com/files/20237769`
- `secondary-screen-readme.txt` : `https://ndownloader.figshare.com/files/20238123`
(Avant §8.77 : pas d'URL `ndownloader` par fichier dans les provenances ; accès via l'API ci-dessus, champ `download_url`.)
**Contenu :** 701 004 lignes (dose-réponse) ; écrans HTS002 (602 495), MTS010 (64 203), MTS006 (33 472), MTS005 (834) ; 1 502 broad_id, 1 448 noms de composés, 480 lignées ; AUC jamais manquante, IC50 manquante sur 48 % des lignes.
(Source : `PROVENANCE_prism_secondary.md`, `PROVENANCE_mtap_arbitration_840.md`, `~/workspace/staging-pdac/download_data.sh`)

---

## 9. GDSC2 — dose-réponse ajustée (Wellcome Sanger Institute)

**Projet :** Genomics of Drug Sensitivity in Cancer (GDSC2), Wellcome Sanger Institute. 969 lignées, 297 composés (286 noms uniques), essais de viabilité 72 h, courbes ajustées par le modèle à effets mixtes non linéaires de Vis et al. (paquet R gdscIC50) → LN_IC50, AUC, RMSE, Z-score.
**Chemin d'accès :** site GDSC (`cancerrxgene.org/downloads/bulk_download`) → intégré à Sanger DepMap / Cell Model Passports → API publique `https://api.cellmodelpassports.sanger.ac.uk/download_files` (include=groups.files), catégorie 10 « Drug Sensitivity Data », groupe 46 « GDSC2 IC50 Data », fichier 22870.
**Date d'acquisition :** 16 nov. 2026 (3 tentatives, serveur lent ~25 Ko/s, coupures curl exit 18 à 11 124 736 puis 20 512 768 octets ; reprises `curl -C -`, HTTP 206 ; fichier complet vérifié par taille exacte + type xlsx — voir `gdsc_access.log`).
**Re-téléchargement :** `~/workspace/staging-pdac/download_data.sh` (section GDSC2).

| Fichier local | Taille (octets) | URL exacte (consignée) | SHA-256 consigné | MD5 consigné |
|---|---|---|---|---|
| `data/GDSC2_fitted_dose_response_27Oct23.xlsx` | 22 112 537 | `https://cmp.cog.sanger.ac.uk/download/GDSC2_fitted_dose_response_27Oct23.xlsx` | `0e99120a14a003dcbd3c27c020f1cfd35e38ee091067a2406f66c0d4dbc1c899` | `7303bf3b53a3cfb8f03e739f51cc810d` (`PROVENANCE_mtap_arbitration_840.md` ; re-vérifié localement le 19 nov. 2026) |
| `data/screened_compounds_rel_8.5.csv` | 46 414 | `https://cmp.cog.sanger.ac.uk/download/screened_compounds_rel_8.5.csv` | `d3cbb8b595980b36bf92d54af1da1dd995d2e2ce624c7cc70aacf2a754dce782` | — (non consigné) |

**Contenu vérifié :** 242 036 lignes, 16 colonnes (DATASET, NLME_RESULT_ID, NLME_CURVE_ID, CELL_LINE_NAME, SANGER_MODEL_ID, CANCER_TYPE, DRUG_ID, DRUG_NAME, PUTATIVE_TARGET, PATHWAY_NAME, MIN_CONC, MAX_CONC, LN_IC50, AUC, RMSE, Z_SCORE) ; 286 DRUG_NAME uniques, 295 DRUG_ID uniques, 969 lignées. Annotation : DRUG_ID, SCREENING_SITE, DRUG_NAME, SYNONYMS, TARGET, TARGET_PATHWAY.
(Source : `PROVENANCE_gdsc.md`, `PROVENANCE_mtap_arbitration_840.md`, `~/workspace/staging-pdac/download_data.sh`)

---

## 10. PANC-1 (NCATS) — combinaisons de médicaments, lignée PANC-1 seule

**Source :** dépôt GitHub `ncats/PANC1`, branche `main` (article : Pourmousa et al., *Nat Commun* 2025, 16:4020, doi `10.1038/s41467-025-56818-6` ; dépôt Zenodo `10.5281/zenodo.14230972`).
**Dépôt :** `https://github.com/ncats/PANC1`
**Accès :** `git clone` bloqué (aucune sortie après 174 s, processus arrêté) ; tarball `codeload.github.com/ncats/PANC1/tar.gz/refs/heads/main` téléchargé mais **tronqué** (569 815 185 octets, erreur gzip « unexpected end of file » à l'extraction — archive supprimée). **Fichiers finalement obtenus un par un via `raw.githubusercontent.com`** (HTTP 200, tailles identiques à celles annoncées par l'API GitHub).
**Date d'acquisition :** 16 nov. 2026 (dates de fichiers 16 nov. 13:07–13:08).
**Re-téléchargement :** `~/workspace/staging-pdac/download_data.sh` (section PANC-1) télécharge le tarball — **voie connue-tronquée en pratique** ; préférer les URL fichier par fichier ci-dessous (base confirmée par les réponses JSON de l'API GitHub conservées dans `data/panc1_9191.json` et `data/panc1_9197.json`, champs `download_url`).

| Fichier local | Taille (octets) | URL exacte (champ `download_url` de l'API GitHub, conservé dans les JSON) | SHA-256 (calculé localement le 19 nov. 2026 ; préfixes conformes aux valeurs tronquées consignées) |
|---|---|---|---|
| `data/panc1_ncata/9191_calc.csv` | 24 780 | `https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9191/calc.csv` | `7a5c88d74a0b512b451755d62287b3d62bcb28cb82847e58debbe409e6e916be` |
| `data/panc1_ncata/9191_metadata.csv` | 80 936 | `https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9191/metadata.csv` | `e12c0251d3c1708e15b4dc7cc1fafb551b8c1bcbc25be96c4d42eea2f6a97e70` |
| `data/panc1_ncata/9191_metadata_smiles.csv` | 120 243 | `https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9191/metadata_smiles.csv` | `4e0f0119e1c3133689d586cca2237d7199c49b6e72018cc29041f4aa209ed662` |
| `data/panc1_ncata/9191_responses.csv` | 760 685 | `https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9191/responses.csv` | `f5cc98d3442d3754f49d3e1c36e6d427e38f3c109eeebfae85486303cf18c90f` |
| `data/panc1_ncata/9197_calc.csv` | 24 165 | `https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9197/calc.csv` | `3c50bb1b32d451e18384c525e3c3315609f9aa27a3ed7f50fad0fb33985d397b` |
| `data/panc1_ncata/9197_metadata.csv` | 71 459 | `https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9197/metadata.csv` | `1240777419d25e985f9cf6ae998cd4393b2d2f53be404c9b595cb66178bba0f0` |
| `data/panc1_ncata/9197_metadata_smiles.csv` | 108 941 | `https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9197/metadata_smiles.csv` | `d45b7d730c002e96340778396e222a76910c98d54060e2e221d4e1151b822cfa` |
| `data/panc1_ncata/9197_responses.csv` | 750 256 | `https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9197/responses.csv` | `cdece93912122bc6599942ee050c87501455d433d94ebf1d7e43960237ea1173` |
| `data/panc1_ncata/mit_test.csv` | 3 249 228 | Chemin consigné `MIT/test.csv` (`PROVENANCE_kras_combinations.md`) ; base `https://raw.githubusercontent.com/ncats/PANC1/main/` confirmée par les JSON — URL reconstruite `https://raw.githubusercontent.com/ncats/PANC1/main/MIT/test.csv` (**VÉRIFIÉE §8.77, 21 nov. 2026** : re-téléchargée, taille 3 249 228 o, SHA-256 identique) | `9f3ae18976136412802831487b6187fcf062db8f4ca753990689d3ac62006e27` (calculé localement) |

**Contenu :** 496 combinaisons (C(32,2)), matrices 10×10, lignée PANC-1 seule (KRAS G12D) ; `calc.csv` : scores Gamma, Beta, ExcessHSA par bloc (un réplicat par bloc dans les fichiers déposés) ; Gamma < 0,95 = synergique (définition de l'article). `mit_test.csv` : **exclu de l'analyse** — scores Gamma_Score de moyenne −0,34 (échelle différente des gamma mesurés ~0,9), 3 lignes seulement en recouvrement avec les 496 paires mesurées : ce sont des **scores prédits par modèle** sur une bibliothèque virtuelle, pas des mesures. Gardé pour traçabilité.
**Fichiers annexes (métadonnées API, pas des données) :** `data/panc1_api.json` (7 436 o), `data/panc1_9191.json` (3 513 o), `data/panc1_9197.json` (3 513 o), `data/panc1_ncats.json` (5 003 o), `data/panc1_README.md` (959 o, README du dépôt), `data/panc1_ncata/panc1_sha256.txt` (680 o, SHA-256 complets des 8 fichiers sources).
**Fichier dérivé (voir §14) :** `data/panc1_combinations_summary.csv` (58 977 o, 496 paires, script `analyze_panc1_combos.py`).
(Source : `PROVENANCE_kras_combinations.md` — note : `source_registry.md` attribue par erreur cette source à `PROVENANCE_crispr_scan.md`, qui ne mentionne pas PANC-1 ; la provenance réelle est `PROVENANCE_kras_combinations.md`)

---

## 11. TCGA PanCanAtlas — clinique patient PAAD (stades, test C) — provenance d'acquisition RETROUVÉE au §8.77

- **Fichier local :** `~/workspace/runs/pdac-v6/data_clinical_patient.txt` — **58 621 octets** (⚠️ **hors de `data/`**, à la racine de `pdac-v6/`)
- **SHA-256 (consigné dans `PROVENANCE_testC_stage.md`, re-vérifié localement le 19 nov. 2026) :** `0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5`
- **Contenu :** TCGA PanCanAtlas, 184 patients PAAD, 0 doublon PATIENT_ID ; colonne `AJCC_PATHOLOGIC_TUMOR_STAGE` (7e colonne), édition AJCC 7e ; stades bruts : STAGE IIB 121, IIA 30, IB 15, III 5, IV 5, IA 5, (vide) 2, STAGE I 1. Utilisé par le test C (§8.45) : 175 tumeurs appariées à l'expression RSEM avec stade connu.
- **Date d'acquisition :** fichier déjà sur le disque au début du chantier, **15 nov. 2026, 15h13 UTC** (date de modification du fichier).
- **URL exacte (retrouvée et vérifiée §8.77, 21 nov. 2026) :** `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_tcga_pan_can_atlas_2018/data_clinical_patient.txt` — dépôt GitHub `cBioPortal/datahub`, étude cBioPortal `paad_tcga_pan_can_atlas_2018` (TCGA PanCanAtlas PAAD). Re-téléchargé le 21 nov. 2026 : taille 58 621 o, SHA-256 `0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5` (identique au consigné). **Double confirmation :** les fichiers de ce dépôt sont en Git LFS — le `download_url` de l'API GitHub (`raw.githubusercontent.com/…`) renvoie le pointeur LFS (130 o), et ce pointeur porte lui-même `oid sha256:0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5` et `size 58621`. C'est le contenu réel, servi par `media.githubusercontent.com`, qui a été vérifié.
- **Conséquence (mise à jour §8.77) :** la lacune de provenance la plus grave du projet est **close** : le fichier est désormais re-téléchargeable depuis une source connue et vérifiable. (Avant §8.77 : provenance d'acquisition MANQUANTE, cité dans `PROVENANCE_testC_stage.md` : « MANQUANTE — fichier déjà sur le disque au début du chantier (15 nov. 2026, 15h13 UTC) ; aucune entrée dans fetch_tcga.log, download_firehose.log ni PROVENANCE_tcga*.md ; premier hachage consigné ici ; rien re-téléchargé ».) Le verdict du test C (§8.45) est inchangé — seule sa reproductibilité est réparée.
(Source : `PROVENANCE_testC_stage.md`)

---

## 12. cBioPortal — études QCMG (paad_qcmg_uq_2016) — fichiers téléchargés puis ÉCARTÉS

- **Fichiers locaux :** `data/qcmg_clinical_patient.txt` — **49 042 octets** (SHA-256 calculé localement le 19 nov. 2026 : `ae7fc6d7a8c887bb890090f1fc1c3770b94fb31dde38e209c684bc0ffbfd6a95`) ; `data/qcmg_clinical_sample.txt` — **57 215 octets** (SHA-256 calculé localement : `c70daf3e772cdcf99b62ca20f8a85f748df80631fd915b7da465e670a1fcceca`)
- **Étude :** cBioPortal `paad_qcmg_uq_2016` (QCMG, *Nature* 2016, 456 patients). Pages d'étude : `https://www.cbioportal.org/study/summary?id=paad_qcmg_uq_2016` et `https://www.cbioportal.org/study/summary?id=paad_icgc` (consignées dans `source_registry.md`).
- **URL exactes des fichiers cliniques (retrouvées et vérifiées §8.77, 21 nov. 2026) :** dépôt GitHub `cBioPortal/datahub`, étude `paad_qcmg_uq_2016` — `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_qcmg_uq_2016/data_clinical_patient.txt` et `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_qcmg_uq_2016/data_clinical_sample.txt` — re-téléchargés le 21 nov. 2026 : tailles 49 042 o / 57 215 o, SHA-256 identiques aux valeurs ci-dessus. **Note LFS :** comme au §11, le `download_url` de l'API GitHub (`raw.githubusercontent.com/…`) renvoie le pointeur LFS (130 o) ; le contenu réel est servi par `media.githubusercontent.com`. (Avant §8.77 : « fichier clinique datahub » sans URL, `PROVENANCE_icgc.md`.)
- **Statut : ÉCARTÉS après vérification** (`PROVENANCE_icgc.md`) : le fichier clinique datahub n'a pas de OS_MONTHS/OS_STATUS ; `STATUS` + `DAYS_TO_LAST_FOLLOWUP` ne sont renseignés que pour 134/456 patients, et les identifiants patients (3.014, A10.7…) ne correspondent pas aux identifiants ICGC (ICGC_0006…) — pas de jointure possible, **non utilisés** pour les verdicts. Conservés dans `data/` pour traçabilité.
- **Date d'acquisition :** 16 nov. 2026 (dates de fichiers 16 nov. 12:14).
(Source : `PROVENANCE_icgc.md`, `source_registry.md`)

---

## 13. Birnbaum et al. 2017 — suppléments Springer (validation des classifications)

- **Article :** Birnbaum et al., 2017, « Validation and comparison of the molecular classifications of pancreatic carcinomas », *Mol Cancer* 16:174, DOI `10.1186/s12943-017-0739-z` (PMC5674743 — `https://pmc.ncbi.nlm.nih.gov/articles/PMC5674743/`, PMID 29110659).
- **URL exactes (retrouvées et vérifiées §8.77, 21 nov. 2026) :** patron Springer `static-content.springer.com/esm/art%3A10.1186%2Fs12943-017-0739-z/MediaObjects/12943_2017_739_MOESM{n}_ESM.xlsx` (n = 1–5) — les 5 fichiers ont été re-téléchargés le 21 nov. 2026 et leurs tailles + SHA-256 vérifiés identiques à ceux ci-dessous. (Avant §8.77 : « via static-content Springer, MOESM1–5 », sans URL.)
- **Fichiers locaux (téléchargés le 16 nov. 2026, dates de fichiers 16 nov. 12:10) :**

| Fichier local | Taille (octets) | SHA-256 (calculé localement le 19 nov. 2026 ; la provenance disait « SHA à vérifier dans les fichiers » — c'est fait ici) |
|---|---|---|
| `data/birnbaum_springer_MOESM1.xlsx` | 11 209 | `3d9df7b9bdbb2cf8c0ee20a62c1b798f5faed4eec053b4e785f9f8e0dff4945b` |
| `data/birnbaum_springer_MOESM2.xlsx` | 15 240 | `721e19d95710413762ea92ba6ae216b18bdf25f0d736ffd78bcfafd34a8b77c3` |
| `data/birnbaum_springer_MOESM3.xlsx` | 9 119 | `8bfbdcd618ea2a9d9b8ae480c763b857c3e23e2022462ab61cff0aaa8c6b1a13` |
| `data/birnbaum_springer_MOESM4.xlsx` | 15 040 | `49fff4c84c8859ee12072282f4e69f02cf10cce90a638506c6888ea9fa7df361` |
| `data/birnbaum_springer_MOESM5.xlsx` | 8 767 | `94af1f7351a9028cab962c160c51ceea47f882705496db5e00f266a06fdb6ccb` |

- **URL : voir ci-dessus (§8.77).**
- **Contenu :** tableaux récapitulatifs seulement, pas de survie par patient.
(Source : `PROVENANCE_geo71729_survival.md`, `source_registry.md`)

---

## 14. Fichiers dérivés présents dans `data/` — reconstructibles, pas des sources brutes

Ces fichiers sont des **sorties de scripts du projet** appliqués aux bruts ci-dessus. Ils n'ont pas besoin d'être re-téléchargés : ils se reconstruisent (script + brut + graine indiqués). SHA-256 calculés localement le 19 nov. 2026 (sauf mention contraire).

| Fichier local | Taille (octets) | Dérivé de | Script / méthode |
|---|---|---|---|
| `data/cptac/pdac_umich_protein_gene_matrix.csv` | 12 365 808 | Report UMich (§6) | `scripts/build_matrix_umich.py` (logique du paquet `cptac` : découpage Index, transposition, soustraction ReferenceIntensity, suppression QC/pools, mapping aliquote→patient, agrégation gène par médiane des isoformes) |
| `data/cptac/pdac_umich_coverage.json` | 2 251 | Report UMich (§6) | Couverture des 12 gènes v4 (voir `PROVENANCE_cptac.md` §4) |
| `data/crispr_genome_scan.csv` | 1 372 514 | CRISPRGeneEffect.csv + Model.csv (§1) | `crispr_genome_scan.py` — Spearman Chronos gène vs Chronos KRAS, 47 lignées, 17 916 gènes ; SHA consigné `673e7080…` (`PROVENANCE_crispr_scan.md`) |
| `data/prism_kras_screen.csv`, `data/prism_kras_screen_named.csv`, `data/prism_kras_screen_pvalues.csv`, `data/prism_compounds_saved.csv` | 744 943 / 1 420 310 / 975 641 / 719 571 | PRISM 24Q2 (§7) + CRISPRGeneEffect (§1) | `prism_screen.py` — Spearman viabilité vs Chronos KRAS (note : étiquettes de tertiles inversées dans ce script, voir `PROVENANCE_gdsc.md` § Signalement) |
| `data/prism_secondary_kras_screen.csv`, `data/prism_secondary_kras_screen_moa.csv`, `data/prism_secondary_kras_screen_targets.csv` | 328 532 / 9 213 / 3 979 | PRISM 19Q4 (§8) + CRISPRGeneEffect (§1) | `prism_secondary_screen.py` — SHA consignés dans `PROVENANCE_prism_secondary.md` |
| `data/gdsc_kras_screen.csv`, `data/gdsc_kras_screen_pathways.csv`, `data/gdsc_kras_screen_targets.csv` | 71 464 / 1 353 / 809 | GDSC2 (§9) + CRISPRGeneEffect + Model (§1) | `gdsc_kras_screen.py` |
| `data/kras_mutations_maf.csv` | 15 705 | MAF (§1) | Extraction KRAS du MAF, 390 lignes ; SHA consigné `fcf0eed2…` (`PROVENANCE_kras_g12d.md`) |
| `data/kras_alleles_pancreas.csv` | 1 470 | MAF + Hotspot + OmicsProfiles (§1) | `mrtx1133_prism_allele.py` ; SHA consigné `9ac803ad…` |
| `data/mrtx1133_prism_kras_allele.csv` | 3 536 | PRISM 24Q2 (§7) + allèles KRAS | `mrtx1133_prism_allele.py` ; SHA consigné `7a449c92…` |
| `data/mutation_table_pancreas.csv` | 4 790 | MAF (§1) | `build_mutation_table_pancreas.py` (18 nov. 2026) ; SHA consigné `f3fa2bd2…` (`PROVENANCE_mtap_arbitration_840.md`) |
| `data/prmt5_mtap_results.csv` | 2 856 | CRISPRGeneEffect + Model + OmicsCNGene (§1) | `prmt5_mtap_dependency.py` ; SHA consigné `e7c90e9a…` |
| `data/prmt5_mtap_pancreas_lines.csv` | 8 423 | idem | `prmt5_mtap_dependency.py` ; SHA consigné `348ccfa975ed…` |
| `data/prmt5_mtap_pancancer_lines.csv` | 183 190 | idem (toutes lignées) | `prmt5_mtap_dependency.py` (variante pan-cancer) ; SHA consigné `1085cbb1…` |
| `data/panc1_combinations_summary.csv` | 58 977 | PANC-1 (§10) | `analyze_panc1_combos.py` ; SHA consigné `423ac17579416e64421595fbb3e2fc9bb966b4bc3a43f92e1851ba649f541f77` |
| `data/tcga_paad_rsem.tar.gz.md5`, `data/tcga_luad_rsem.tar.gz.md5`, `data/tcga_coad_rsem.tar.gz.md5`, `data/tcga_paad_gistic.tar.gz.md5` | 56–178 | — | Fichiers de contrôle MD5 des tarballs (§2) — valeurs vérifiées conformes aux provenances |
| `data/download_depmap.log`, `data/download_firehose.log`, `data/download_omicscn.log` | 8 637 / 1 305 / 0 | — | Journaux de téléchargement (15 nov. 2026). `download_omicscn.log` est **vide (0 octet)** |
| `data/panc1_api.json`, `data/panc1_9191.json`, `data/panc1_9197.json`, `data/panc1_ncats.json`, `data/panc1_README.md` | 7 436 / 3 513 / 3 513 / 5 003 / 959 | API GitHub ncats/PANC1 (§10) | Réponses JSON de l'API GitHub (listes de fichiers + `download_url`) et README du dépôt |

**Fichiers de flux du pipeline (`pdac_*_fluxes*.csv` à la racine de `pdac-v6/`) :** dérivés des bruts par les scripts `build_fluxes_*.py` ; leurs SHA-256 sont consignés dans chaque `PROVENANCE_*.md` — hors périmètre de ce document (matrices brutes uniquement), sauf mention dans les sections ci-dessus.

---

## 15. Ce qui ne peut pas être re-téléchargé tel quel

### 15.1 Portail mort — ICGC DCC

- **Portail ICGC DCC (`https://dcc.icgc.org/`) : décommissionné (vérifié 16 nov. 2026).** L'API `/api/v1/download` et `/api/v1/releases` ne servent plus de fichiers (redirection vers la page d'accueil HTML).
- **Fichiers concernés :** `donor.PACA-AU.tsv.gz` / `exp_seq.PACA-AU.tsv.gz` (avec `donor_survival_time`, `donor_vital_status`) — **jamais obtenus à la source**.
- **Alternative utilisée (vérifiée, mêmes patients Bailey et al. 2016) :** expression via UCSC Xena (§5.2–5.4) + clinique/survie via le supplément de Bailey 2016 (§5.5). Les identifiants patients ICGC (`ICGC_0006…`) correspondent entre les deux.
(Source : `PROVENANCE_icgc.md`)

### 15.2 Portail bloqué — DepMap (PRISM secondaire) et Cloudflare

- **Portail DepMap (`depmap.org/portal/download/all/?releasename=PRISM+Repurposing+19Q4`) : bloqué par Cloudflare Turnstile** (vérifié 16 nov. 2026, 12h43 : le fichier téléchargé n'est que du HTML, 4 937 octets).
- **Alternative utilisée :** API figshare `https://api.figshare.com/v2/articles/9393293` (§8) — mêmes fichiers, MD5 vérifiés.
- Le reste de DepMap 24Q4 se télécharge normalement via `ndownloader.figshare.com` (§1).
(Source : `PROVENANCE_prism_secondary.md`)

### 15.3 Site injoignable depuis la VM — DrugComb (aucune donnée obtenue)

- **DrugComb (`https://drugcomb.org/downloads`, `https://drugcomb.org/`, `https://drugcombdb.drugcomb.org/`, `drugcomb.fimm.fi`) : injoignable depuis cette VM le 16 nov. 2026** (curl HTTP 000, 0 octet, 3/3 ; `curl -sI` : « 200 Connection Established » (proxy) puis réponse vide, exit 52 ; `browser.open` : DNS / connexion refusée ; contrôle `curl https://www.google.com` : HTTP 200 — le réseau fonctionne). DNS résout (198.18.134.92 / 198.18.134.93).
- **Conséquence :** aucune donnée DrugComb téléchargée (437 932 combinaisons, 2 276 médicaments, 93 lignées selon Zagidullin et al., *Nucleic Acids Res* 2019, doi `10.1093/nar/gkz337`). Même accessible, son seul contenu pancréatique serait FORCINA (1 lignée dans la curation).
- **Autres bases de combinaisons écartées sans téléchargement (pas de lignée pancréas, vérifié dans les articles) :** NCI ALMANAC (données : `https://dtp.cancer.gov/ncialmanac` — panel NCI-60, aucune lignée pancréas), AZ-DREAM (Menden et al., *Nat Commun* 2019, 10:2674 ; données Synapse syn4231880, compte requis — 85 lignées, aucune pancréas), O'Neil (O'Neil et al., *Mol Cancer Ther* 2016, 15:1155–62 ; 39 lignées, aucune pancréas). FORCINA (Langdon et al., *Mol Cancer Ther* 2017, 16(6):1041–1053 — cité « Forcina et al. » par erreur dans les fichiers ; doi `10.1158/1535-7163.MCT-16-0794`) : 4 lignées PDAC, données supplémentaires sur le site AACR, **non téléchargées** (n=4, aucun test de corrélation KRAS possible).
(Source : `PROVENANCE_kras_combinations.md`, `source_registry.md`)

### 15.4 Fichiers téléchargés mais non conservés sur disque

- **SOFT GPL20769 (37 588 662 o)** : téléchargé le 15 nov. 2026, **absent de `data/`** ; URL retrouvée et vérifiée §8.77 (§3.1) : `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL20nnn/GPL20769/soft/GPL20769_family.soft.gz` (le chemin `GPL2nnn/` donne 404 — voir §3.1). Re-téléchargeable et vérifié par taille + SHA-256.
- **SOFT GPL6244 (plusieurs centaines de Mo)** : non conservé, mais re-téléchargeable par l'URL exacte du §4.1.
- **Tarball PANC-1** (`codeload.github.com/ncats/PANC1/tar.gz/refs/heads/main`) : téléchargé tronqué puis **supprimé** ; voie de remplacement : fichiers un par un (§10).
- **HTML vides des tentatives DrugComb** (0 octet) : supprimés ; l'échec est consigné dans `PROVENANCE_kras_combinations.md`, pas par des fichiers vides.

### 15.5 Fichiers jamais téléchargés (cités dans les provenances, absents de `data/`)

- `GSE62452_paired_sample_information.xlsx` (supplément GSE62452, pourrait contenir des données cliniques — non vérifié).
- `GSE71729_RAW.tar` (3,9 Go, données brutes Agilent, répertoire `suppl/` GEO) — pas de clinique dedans.
- GDSC1 (403 composés) — non testé (même question, autre jeu).
- Données individuelles des essais cités (Tango, Revolution Medicines) — chiffres repris des communiqués/publications, non re-calculés.
- ChEMBL (MRTX1133 `CHEMBL4858364`, daraxonrasib `CHEMBL6168538`) et DGIdb : requêtes API uniquement, aucun fichier conservé (DGIdb : API REST inexploitable — renvoie la page JS ; GraphQL sans réponse — « à vérifier », rien inventé).

### 15.6 Lacune de provenance — clinique TCGA PanCanAtlas — CLOSE au §8.77

- `data_clinical_patient.txt` (§11) : provenance d'acquisition **retrouvée le 21 nov. 2026** (cBioPortal datahub, étude `paad_tcga_pan_can_atlas_2018`, URL exacte au §11, SHA-256 vérifié identique). Avant §8.77, la provenance était manquante (voir `PROVENANCE_testC_stage.md`) et le fichier non re-téléchargeable depuis une source connue. Cette sous-section est conservée pour l'historique : la lacune a existé du 15 au 21 nov. 2026, elle est désormais close.
(Source : `PROVENANCE_testC_stage.md`, chantier §8.77)

---

## 16. Vérification exhaustive — fichiers `data/` de plus de 5 Mo (19/19)

Liste exhaustive mesurée le 19 nov. 2026 (`find data/ -type f -size +5M`, tri décroissant). Chaque fichier apparaît dans ce document.

| # | Fichier local | Taille (octets) | Section | Statut |
|---|---|---|---|---|
| 1 | `data/OmicsCNGene.csv` | 1 394 554 236 | §1 | Brut DepMap 24Q4 ✓ |
| 2 | `data/CRISPRGeneEffect.csv` | 428 678 699 | §1 | Brut DepMap 24Q4 ✓ |
| 3 | `data/secondary-screen-dose-response-curve-parameters.csv` | 264 340 589 | §8 | Brut PRISM 19Q4 ✓ |
| 4 | `data/OmicsSomaticMutationsMAFProfile.maf` | 98 439 503 | §1 | Brut DepMap 24Q4 ✓ |
| 5 | `data/Repurposing_Public_24Q2_Extended_Primary_Data_Matrix.csv` | 72 456 953 | §7 | Brut PRISM 24Q2 ✓ |
| 6 | `data/tcga_luad_rsem.tar.gz` | 47 043 687 | §2.3 | Brut Firehose ✓ |
| 7 | `data/tcga_coad_rsem.tar.gz` | 26 401 036 | §2.4 | Brut Firehose ✓ |
| 8 | `data/tcga_paad_gistic.tar.gz` | 26 189 717 | §2.2 | Brut Firehose ✓ |
| 9 | `data/GDSC2_fitted_dose_response_27Oct23.xlsx` | 22 112 537 | §9 | Brut GDSC2 ✓ |
| 10 | `data/bailey2016_suppl_tables1-13.xlsx` | 22 104 569 | §5.5 | Brut Bailey 2016 ✓ |
| 11 | `data/cptac/umich-pdac-proteomics-Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz` | 20 504 572 | §6 | Brut CPTAC/Zenodo ✓ |
| 12 | `data/ng3398_MOESM60_ESM.txt` | 19 393 438 | §3.2 | Brut suppl. Moffitt ✓ (URL retrouvée §8.77) |
| 13 | `data/GSE71729_series_matrix.txt.gz` | 15 622 315 | §3 | Brut GEO ✓ |
| 14 | `data/tcga_paad_rsem.tar.gz` | 15 296 232 | §2.1 | Brut Firehose ✓ |
| 15 | `data/GSE62452_series_matrix.txt.gz` | 14 447 291 | §4 | Brut GEO ✓ |
| 16 | `data/cptac/pdac_umich_protein_gene_matrix.csv` | 12 365 808 | §6 / §14 | **Dérivé** (reconstruit depuis le Report UMich) ✓ |
| 17 | `data/icgc_pacaau_exp.txt.gz` | 9 841 881 | §5.2 | Brut Xena ✓ |
| 18 | `data/cptac/bcm-pdac-proteomics-PDAC_proteomics_gene_abundance_log2_reference_intensity_normalized_Tumor.txt.gz` | 7 382 441 | §6 | Brut CPTAC/Zenodo ✓ |
| 19 | `data/ng3398_MOESM59_ESM.pdf` | 5 339 711 | §3.2 | Brut suppl. Moffitt ✓ (URL retrouvée §8.77) |

**Total `data/` : 87 fichiers, ~2,44 Go.** Les 68 autres fichiers (≤ 5 Mo) sont couverts aux §1–§14 (bruts : Model.csv, OmicsProfiles.csv, Hotspot, listes PRISM, fichiers PRISM 19Q4, screened_compounds, probemap/NMF ICGC, mapping CPTAC, fichiers PANC-1, MOESM61–63, Birnbaum MOESM1–5, QCMG, GPL ; dérivés : §14).

---

## 17. Bilan des URL manquantes

Aucune URL n'a été devinée. Voici, fichier par fichier, ce qui manquait et comment chaque gap a été fermé au §8.77 (l'historique est conservé dans la 3e colonne).

| Fichier(s) | Ce qui manque | Raison (consignée) |
|---|---|---|
| `data/ng3398_MOESM59_ESM.pdf`, `MOESM60_ESM.txt`, `MOESM61_ESM.xlsx`, `MOESM62_ESM.xlsx`, `MOESM63_ESM.xlsx` | **FERMÉ §8.77** — URL `static-content.springer.com/esm/art%3A10.1038%2Fng.3398/MediaObjects/41588_2015_BFng3398_MOESM{n}_ESM.{ext}` (5/5 SHA vérifiés) | Avant §8.77 : non consignée dans `PROVENANCE_geo71729_survival.md` (noms, tailles, SHA tronqués seulement). Suppléments Nature de Moffitt et al. 2015 (doi `10.1038/ng.3398`). SHA-256 complets re-calculés ici (§3.2). |
| `data/birnbaum_springer_MOESM1.xlsx` à `MOESM5.xlsx` | **FERMÉ §8.77** — URL `static-content.springer.com/esm/art%3A10.1186%2Fs12943-017-0739-z/MediaObjects/12943_2017_739_MOESM{n}_ESM.xlsx` (5/5 SHA vérifiés) | Avant §8.77 : non consignée (« via static-content Springer, MOESM1–5 », sans URL). Article PMC5674743, DOI 10.1186/s12943-017-0739-z. SHA-256 complets re-calculés ici (§13). |
| SOFT GPL20769 (37 588 662 o, **non conservé**) | **FERMÉ §8.77** — URL `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL20nnn/GPL20769/soft/GPL20769_family.soft.gz` (taille exacte + SHA `ecb1b79a…` vérifiés) | Avant §8.77 : non consignée dans `PROVENANCE_geo71729.md`. |
| `data/icgc_pacaau_probemap.gz`, `data/icgc_pacaau_nmf.txt.gz` | **FERMÉ §8.77** — URL `https://icgc.xenahubs.net/download/PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp.gz` et `…/nature16965-s2_NMF_class_assignment.txt.gz` (2/2 SHA vérifiés) | Avant §8.77 : jeux Xena nommés (§5.3, §5.4) mais URL non consignée littéralement ; hub `icgc.xenahubs.net`, bucket S3 `icgc-xena-hub` (confirmés par §5.2). |
| `data/Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv` | **FERMÉ §8.77** — URL `https://ndownloader.figshare.com/files/46630978` (fichier 46630978, API 25917643 ; SHA vérifié) | Avant §8.77 : non consignée ; fichier absent de `download_data.sh`. SHA-256 consigné (§7). |
| `data/secondary-screen-*.csv` (4 fichiers, §8) | **FERMÉ §8.77** — URL directes `https://ndownloader.figshare.com/files/20237739` (dose-response), `…/20237763`, `…/20237769`, `…/20238123` (4/4 SHA vérifiés) | Avant §8.77 : pas d'URL `ndownloader` par fichier dans les provenances : accès via l'API figshare `https://api.figshare.com/v2/articles/9393293` (champ `download_url`). |
| Fichiers CPTAC (§6) | **FERMÉ §8.77** — URL directes `https://zenodo.org/api/records/8394329/files/<nom>/content` (champ `links.self` lu ; MD5 conformes) | Avant §8.77 : accès via l'API Zenodo `https://zenodo.org/api/records/8394329` (champ `links.self`) ; page du record `https://zenodo.org/records/8394329` consignée. |
| `data/qcmg_clinical_patient.txt`, `data/qcmg_clinical_sample.txt` | **FERMÉ §8.77** — URL `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_qcmg_uq_2016/data_clinical_patient.txt` (+ `…_sample.txt`) (2/2 SHA vérifiés) | Avant §8.77 : « Fichier clinique datahub » sans URL (`PROVENANCE_icgc.md`) ; pages d'étude cBioPortal consignées (§12). Fichiers **écartés** (non utilisés). |
| `~/workspace/runs/pdac-v6/data_clinical_patient.txt` | **FERMÉ §8.77** — provenance retrouvée : `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_tcga_pan_can_atlas_2018/data_clinical_patient.txt` (SHA `0c274268…` vérifié ; pointeur LFS porte le même SHA) | Avant §8.77 : provenance **MANQUANTE** (déclaré dans `PROVENANCE_testC_stage.md`). Fichier hors `data/`, non re-téléchargeable depuis une source connue. |
| `data/panc1_ncata/mit_test.csv` | **FERMÉ §8.77** — URL `https://raw.githubusercontent.com/ncats/PANC1/main/MIT/test.csv` **vérifiée** (SHA `9f3ae189…`) | Avant §8.77 : chemin `MIT/test.csv` consigné ; URL reconstruite à partir de la base confirmée (§10) — **à vérifier avant usage**. |
| `data/GPL20769.annot.gz` (990 o) | — | Pas une URL manquante : c'est une **page 404** conservée par erreur (§3.1). Ne pas utiliser. |
| `data/GPL570_probe2symbol.tsv` | URL valides | Les URL tentées renvoient 404 (chemins consignés, §4.2). Fichier dérivé **non utilisé**. |

**Bilan révisé §8.77 (21 nov. 2026) : 19/19 fichiers FERMÉS, plus les 4 fichiers CPTAC (URL directes désormais consignées, §6), le fichier clinique du test C (provenance retrouvée, §11) et le SOFT GPL20769 (URL retrouvée et vérifiée, §3.1).** Le détail gap par gap est au §29. Il ne reste **aucun fichier brut sans URL de téléchargement** dans ce document : chaque URL a été retrouvée depuis une source lue (page DOI, FTP GEO, API figshare/Zenodo/GitHub, hub Xena) ou reconstruite puis **vérifiée par le SHA-256 du fichier re-téléchargé**. Les deux voies restées infructueuses en cours de route sont consignées au §29 (listing S3 403, Europe PMC supplementaryFiles HTTP 500, chemin `GPL2nnn/` 404) — elles ne cachent aucun gap restant.

---

## 18. Nouvelles sources brutes §8.55 (pureté externe, 20 nov. 2026)

Trois fichiers bruts ajoutés dans `data/` pour le chantier §8.55 (pureté
externe ABSOLUTE / ESTIMATE). Ils ne sont PAS dans ce dépôt (limite snapshot)
mais sont documentés ici avec URL exacte et hachage vérifié, comme les autres
sources. Provenance complète : `section_8.55_purity_external.md` §8.55.1 et
`PROTOCOL_purity_external_855.md` (protocole gelé SHA `734a9b17…`).

### 18.1 pdacR — TCGA_PAAD.rds (ABSOLUTE pour PAAD)

- **Fichier local :** `data/pdacR_TCGA_PAAD.rds`, 12 311 529 octets.
- **SHA-256 :** `52020679350d1539d7516f7d38f7bf09e510225eba2f228a4fe874f3c496ea76`
  (vérifié localement le 20 nov. 2026).
- **URL exacte :** `https://raw.githubusercontent.com/rmoffitt/pdacR/master/data/TCGA_PAAD.rds`
- **Origine :** pdacR (Torre-Healy et al., *Commun Biol* 2023, 6:163,
  doi `10.1038/s42003-023-04461-6`), dépôt GitHub `rmoffitt/pdacR` ;
  curation de la Table S1 de Raphael et al. 2017 (*Cancer Cell*,
  PMID 28810144, PMCID PMC5964983, doi `10.1016/j.ccell.2017.07.007`).
  Colonne ABSOLUTE (pureté par analyse de nombre de copies) pour 178
  tumeurs PAAD, non nulle pour 149/178 (83,7 %).
- **Usage :** §8.55 — jointure par barcode (15 premiers caractères),
  178/178 appariées ; ABSOLUTE corrèle r = +0,8556 avec la pureté par
  méthylation de la même table (mesure ADN indépendante).

### 18.2 Aran et al. 2015 — Suppl. Data 1 (tableau de pureté pan-cancer)

- **Fichier local :** `data/aran2015_supp_data1_ncomms9971-s2.xlsx`, 553 082 octets.
- **SHA-256 :** `fce1ba13ff3a6432b7e4f260eb516e407c967d615ca87bc8dffa7765baf97529`
  (vérifié localement le 20 nov. 2026).
- **URL exacte :** via Europe PMC,
  `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4671203/supplementaryFiles`
  (zip SHA `4685a8b2…541a5`).
- **Origine :** Aran et al., *Nat Commun* 2015, 6:8971 — « Systematic
  pan-cancer analysis of tumour purity » (jeu « Aran et al. 2015 purity »,
  tableau `tcga_purity.rda` du package UCSCXenaShiny 2.2.1).
- **Usage :** §8.55 — obtenu, mais **0 PAAD** dans le tableau : non utilisé
  pour les tests (les scores ESTIMATE publiés pour PAAD n'ont pas pu être
  récupérés — site piloté par JS, non contourné, cf. §8.55.2).

### 18.3 ShrinkageTrees 2.1.1 — sous-ensemble `pdac` (vérification de distribution)

- **Fichier local :** `data/shrinkagetrees_pdac.csv` (transcription de
  `data/pdac.rda`), 3 885 250 octets.
- **SHA-256 :** `a582bc6f62c68e9a419c39a665b9e45a52baea7f31f5afee944147be587a5bab`
  (vérifié localement le 20 nov. 2026).
- **Origine :** package R ShrinkageTrees 2.1.1 (CRAN), `data/pdac.rda`,
  n = 130, sans barcode — comparaison de distribution seulement
  (tarball CRAN SHA `7c55b4d3…3c85c`).
- **Usage :** §8.55 — la distribution ABSOLUTE reproduit ce sous-ensemble
  indépendant (moyenne 0,3557 contre 0,3517, min 0,09, max 0,89 identiques).

### 18.4 Outil exclu du dépôt (binaire, documenté en provenance §8.54)

- `data_infiltration_854/tidyestimate_1.1.1.tar.gz` — tarball du package R
  tidyestimate (déconvolution ESTIMATE) : binaire, non poussé (snapshots
  UTF-8 uniquement) ; documenté dans la provenance §8.54
  (`section_8.54_infiltration.md`).

---

## 19. Matrices DepMap découpées pour la Release (20 nov. 2026)

Go de Zackary, 20 nov. 2026 08h17 : les deux matrices DepMap doivent être
dans la prochaine Release, découpées car le navigateur refuse les fichiers
de 428 Mo et 1,3 Go. Préparation faite le 20 nov. 2026 (coordinateur
§8.59–§8.63). Les morceaux ne sont PAS dans ce dépôt (limite snapshot) :
ce sont des actifs de Release uniquement. Détail et réassemblage :
`depmap_split/README_depmap_split.md` (dossier de travail
`~/workspace/push_v62_863_build/depmap_split/`).

- `CRISPRGeneEffect.csv` (DepMap Public 24Q4, figshare 27993248),
  428 678 699 o, SHA-256
  `3d8f3ec6dbf2db7ff834b79b508622ec0b226f3518003fe96ecf5a4fcf167e3b` →
  `CRISPRGeneEffect.csv.gz` (192 011 215 o, SHA-256
  `14041b48060e698ae13da2c59874faa92b92531c8d5001196fc2a7ac2d1a94c8`)
  en 4 morceaux de 50 Mo (`part-00` à `part-03`).
- `OmicsCNGene.csv` (DepMap Public 24Q4, figshare 27993248),
  1 394 554 236 o, SHA-256
  `4851d3e939d48837a39a0f01294deb90fa507a85703586a927b77474f999134c` →
  `OmicsCNGene.csv.gz` (148 274 624 o, SHA-256
  `d12e6b4c1b2aa755e31e0f3eb3e5fd8fcc776174efcfa92c8b047021aa1158e3`)
  en 3 morceaux de 50 Mo (`part-00` à `part-02`).
- Réassemblage vérifié le 20 nov. 2026 : `cat *.part-* | gunzip -c` retrouve
  les deux SHA-256 sources exacts. Commandes complètes dans
  `depmap_split/README_depmap_split.md`. En cas de refus d'un morceau de
  50 Mo par le navigateur : tester UN morceau d'abord, puis redescendre à
  15 Mo (`split -b 15M`).

---

## 20. Scores ESTIMATE publiés et quatrième cohorte GSE62165 (20 nov. 2026)

- **Table ESTIMATE publiée, TCGA-PAAD RNA-seqV2** (Yoshihara et al. 2013,
  site MD Anderson ESTIMATE) — URL exacte :
  `https://bioinformatics.mdanderson.org/estimate/tables/pancreatic_ductal_adenocarcinoma_RNAseqV2.txt`
  — SHA-256 `46004731c2bc4479931ec19e50e12ce5f1656c890ba09e16a4e166316d59fce1`,
  6 928 octets, 179 lignes (178 tumeurs + en-tête), colonnes ID,
  Stromal_score, Immune_score, ESTIMATE_score. Obtenue le 20 nov. 2026
  en lisant le JS du site (`disease_histogram.js`) et les menus de
  `disease.html` — la voie qui avait échoué au §8.55 (curl 000) a
  fonctionné du premier coup. Preuves jointes dans le dépôt :
  `data_flux/pancreatic_ductal_adenocarcinoma_RNAseqV2.txt`,
  `data_flux/disease_865.html`, `data_flux/disease_histogram_865.js`.
  Pas de colonne de pureté ESTIMATE dans cette table : la comparaison
  ABSOLUTE ↔ pureté ESTIMATE publiée reste impossible. Détail au §8.65.
- **GSE62165** (NCBI GEO, Janky et coll., VIB Leuven, PMID 27520560 ;
  plateforme GPL13667, HG-U219) — URL exacte :
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62165/matrix/GSE62165_series_matrix.txt.gz`
  (HTTP 200) — SHA-256
  `fd50fc415a31a4d19a4af82e29afc6909e913f4f223d0b4cd4b637ae4a03727f`,
  51 179 939 octets, **n = 118 tumeurs PDAC** (13 témoins exclus),
  stades I 8 / II 92 / III 5 / IV 13, valeurs log2 déjà normalisées par
  les déposants. Chaîne de mapping documentée au §8.66 (sonde → Entrez
  Gene 2015 via `hgu219.db` 3.2.3, puis → symbole courant via
  `org.Hs.eg.db` 3.23.1 ; 46 083 sondes → 18 448 symboles). Détail au
  §8.66 et dans `PROVENANCE_866.md`.

---

## 21. Fraction leucocytaire décisive, xCell et confirmation indépendante GSE21501 (20 nov. 2026)

- **Fraction leucocytaire par méthylation** (Raphael et al. 2017, Table S1, colonne `DNA.methylation.leukocyte.percent.estimate`) — déjà détenue via pdacR `TCGA_PAAD.rds`, SHA `52020679…ea76` (voir §8.61 et `PROVENANCE_866.md` pour la source) ; aucune nouvelle source externe dans le §8.67, qui re-teste la colonne détenue (`purity_855_sampinfo.csv`, 181 lignes × 55 colonnes) comme contrôle décisif. Détail au §8.67.
- **Scores xCell publiés** (Aran et al. 2017, *Genome Biology* 18:220, doi 10.1186/s13059-017-1349-1) — Additional file 6, scores de 64 types cellulaires pour 9 947 échantillons TCGA/TARGET. Obtenus le 20 nov. 2026 via Europe PMC, URL exacte : `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5688663/supplementaryFiles` (HTTP 200, 3e essai en unité systemd `xcell-dl-868`, 12 092 617 octets, SHA-256 `93c9a7b0cd93d7c35ea844e917a9144c00f3f69dbe1488a87097372d3581d20c`, 17 fichiers ; le serveur ne supporte pas les byte ranges, 1er essai tronqué supprimé). Fichier utilisé : `13059_2017_1349_MOESM6_ESM.tsv`, 7 164 910 octets, SHA-256 `c731427c4a69f82c82bc2f3592116cc6fdc32e8f52b515e1055a9bb9822c51ec`, 64 lignes types × 9 947 colonnes, 0 NaN. Le fichier de 7,1 Mo n'est pas dans le dépôt (limite de 4 Mo par poussée) : il se re-télécharge vérifié depuis l'URL ci-dessus. Additional file 3 (`MOESM3_ESM.xlsx`, 427 029 o, SHA `31a7d8c4…32bc`, 489 signatures) et Additional file 7 (`MOESM7_ESM.xlsx`, 113 661 o, SHA `5f559c5b…03c`, spillover + calibration) dans le même zip. Détail au §8.68 et dans `PROTOCOL_xcell_868.md`.
- **GSE21501** (NCBI GEO, Stratford et coll. 2010, *PLoS Medicine*, PMID 20644708 ; plateforme Agilent GPL4133) — URL exacte : `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE21nnn/GSE21501/matrix/GSE21501_series_matrix.txt.gz` (HTTP 200, 20 nov. 2026) — SHA-256 `1bbbd9d2f1a89b26b73b32ef1e781b5ad46aa2f80ebc1d8c94d0ac5dcb6d9b7b`, 12 575 998 octets, 132 échantillons, valeurs = log2 RATIOS (tumeur / référence Stratagene), 0 NaN. Mapping sonde → symbole : `data_flux/GPL4133_probe2symbol.tsv`, SHA-256 `5630ff23418af6d5241cda8d82a22421e8159a160e6b44123eac3f38eb7a3129` (script `download_gpl4133_mapping_869.py`). Détail au §8.69 et dans `PROVENANCE_869.md`.
- **GSE57495 — CORRECTION de plateforme** (Chen et coll. 2015, *PLoS ONE* 10(8): e0133562, PMID 26247463) — URL exacte : `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE57nnn/GSE57495/matrix/GSE57495_series_matrix.txt.gz` (HTTP 200, 20 nov. 2026) — SHA-256 `995dbeff288a14c1cc1a52489e456b7677ede5da8e287069b8298d649b532efc`, 13 487 043 octets, 63 échantillons PDAC, 60 608 lignes de données. Plateforme lue dans l'en-tête de la matrice : **`GPL15048`** (Rosetta/Merck Human RSTA Custom Affymetrix 2.0) — le §8.66 §1.2 affirmait GPL6244 à tort ; le mapping GPL6244 détenu n'a PAS été utilisé pour GSE57495 (confirmé par deux sources secondaires concordantes : Wu et coll., *Sci Rep* 2025 ; tableau supplémentaire Springer). Mapping sonde → symbole : `data_flux/GPL15048_probe2symbol.tsv`, SHA-256 `93e01ec387ab710dfbfe4b7ad960a90c494b131f62637df3a4476fa9f998f952` (script `download_gpl15048_mapping_869.py`). Détail au §8.69 et dans `PROVENANCE_869.md`.
- **GSE79668** (piste restante nommée au §8.69, non vérifiée, non téléchargée) — aucune donnée détenue, aucun run ; à tester dans un chantier futur avec son propre protocole gelé.

---

## 22. Confirmation indépendante GSE79668 (20 nov. 2026)

- **GSE79668** (NCBI GEO, Kirby et coll. 2016, *Molecular Oncology* 10(8):1169–1182, PMID 27282075 ; plateforme Illumina HiSeq 2000 GPL11154 ; cohorte monocentrique UAB, Birmingham, AL, USA) — URL exacte de la matrice : `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE79nnn/GSE79668/matrix/GSE79668_series_matrix.txt.gz` (HTTP 200, 20 nov. 2026) — SHA-256 `b2226fd096f27a9e5caf32cca3491d1f1e52082ce6e9876b2b1c1f67d88e4754`, 3 724 octets, 80 lignes décompressées, **0 ligne de données** : la table de la matrice ne contient que l'en-tête. Les valeurs sont dans le fichier supplémentaire de la série elle-même, nommé dans l'en-tête (`!Series_supplementary_file`) : `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE79nnn/GSE79668/suppl/GSE79668_51_tumors_sharedgenecounts.txt.gz` (HTTP 200, 20 nov. 2026) — SHA-256 `721cd3a0d1155375ea054f410f65497568284135f32ad59157d62a564cba54f8`, 3 588 753 octets, 48 957 lignes décompressées (48 956 gènes x 51 échantillons, 0 NaN), **comptages bruts de transcrits** (entiers, min 0 / médiane 17 / max 17 823 551), GENCODE v.9, d'après `!Sample_data_processing`. Aucun mapping GPL11154 construit (non nécessaire — identifiants de lignes de la forme `SYMBOLE_ENSG...`, symbole = préfixe avant `_ENSG`, extraction mécanique 48 956/48 956 ; doublons agrégés par médiane, les 13 gènes utiles ont chacun exactement 1 ligne). 12/12 gènes v4 présents, 51/51 cas complets, 7/7 portes §5 OK. Flux : `data_flux/pdac_870_geo79668_fluxes.csv` (51 lignes, SHA `7744bc5a…6107a`), nul graine 42 SHA `50ae9a36…423e3`, nuls frais s8701 SHA `6fffd4fa…baee`, s8702 SHA `69c95e26…08b3`. Détail au §8.70 et dans `PROVENANCE_870.md`.

---

## 23. Confirmation indépendante GSE60979 (20 nov. 2026)

- **GSE60979** (NCBI GEO, Sandhu et coll. 2015, *Molecular Oncology* 9:758–771, PMID 25579086 ; plateforme Agilent SurePrint G3 Human GE 8x60K GPL14550 ; cohorte monocentrique d'Oslo, Oslo University Hospital, Norvège) — URL exacte de la matrice : `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE60nnn/GSE60979/matrix/GSE60979_series_matrix.txt.gz` (HTTP 200, 20 nov. 2026) — SHA-256 `819408bf8dacb01c38eede69287d255eea76f74e2b1b18ec8863933f4700c4eb`, 20 547 348 octets, 49 tumeurs PDAC réséquées (tissus frais congelés) retenues par caractéristique ch1 « tissue: pancreatic ductal adenocarcinoma » (12 normaux adjacents et 32 autres adénocarcinomes périampullaires exclus et comptés). Mapping `data/GPL14550_probe2symbol.tsv`, SHA-256 `cc034a76285b0785bff4dd5249d68becb58acacedb157a8032d0c9309dac3909` (42 545 lignes, 30 436 sondes avec symbole, 22 070 symboles uniques). Intensités log2 normalisées par les déposants (correction de fond + normalisation quantile), sondes agrégées par médiane, ordre par KRAS. Flux : `data_flux/pdac_871_geo60979_fluxes.csv` (49 lignes, SHA `51a7fa56…554e`), nul graine 42 SHA `d427359a…4740`. Cohortes écartées documentées : GSE77858 (MUC17 absent du mapping GPL7264, SHA `41a47160…27e`), GSE43797, GSE161369, GSE63158, GSE79670 (mêmes patients que §8.70). Piste restante nommée : GSE131050. Détail au §8.71 et dans `PROVENANCE_871.md`.

---

## 24. Nuls frais GSE79668 — consolidation §8.72 (20 nov. 2026)

- **10 nuls frais** (graines 8721–8730, lignes permutées, même construction que §8.70, CSV réel inchangé SHA `7744bc5a…6107a`), joints aux 3 nuls anciens (graines 42 / 8701 / 8702) : médiane des 13 nuls 0,2657, écart médian `d_médian = +0,1447` (réel 0,4104 contre nul médian 0,2657), rang 14/14, 12/13 écarts au-dessus du plancher 0,07. Le nul graine 42 (0,3538) est le PLUS HAUT des 13 nuls : le verdict PARTIEL du §8.70 tenait au tirage le plus défavorable. SHA des 10 nuls consignés dans `results/nulls_872_files.json` (SHA `15731361…f8`). Données relues, rien re-téléchargé (matrice SHA `b2226fd0…88e4754`, comptages SHA `721cd3a0…54f8`, voir §22). Addendum daté ajouté au §8.70, texte original intact. Détail au §8.72.

---

## 25. Pic étroit — interventions §8.73 (20 nov. 2026)

- **Aucune donnée nouvelle** hors des CSV déjà sur disque et de 20 nuls ICGC frais (graines 41–60, `data_flux/pdac_immune_icgc_fluxes_nul_s41.csv` … `s60.csv`, SHA dans `results/nulls_icgc_873_files.json`). Corpus : 82 runs existants (14 MTAP + 68 immunitaires) relus ; 11 courbes rob-on (MTAP NUL42, NUL_S123, NUL_S11111 ; icgc_s1, geo62452_nul_s12, tcga_s2, tcga_nul_s11, tcga_nul_s12, icgc_nul_s32, icgc_nul_s35, icgc_nul_s37) et 6 contrôles (MTAP s7, s1011 ; ICGC s31, s33 ; GSE62452 s11 ; TCGA s13). Interventions : déplacement du bloc (swap), winsorisation du bloc (échelle 2/4/8 fenêtres), winsorisation d'une seule ligne, transplantations B1/B0/B2 — CSV modifiés `data_flux/pic873_interv_<run>_<variante>.csv` (66 fichiers, constructions explicites, jamais des mesures), SHA consignés dans `results/pic_etroit_873_extract.json` (SHA `4d0a52cb…e767`). Verdict : NON ÉLUCIDÉ — aucun déclencheur identifiable ; artefact winsorisation documenté (le maxsep monte par déflation de variance). Détail au §8.73.

---

## 26. Douzième paire principale GSE131050 (20 nov. 2026)

- **GSE131050** (NCBI GEO ; Rashid et coll. 2020, *Clin Cancer Res* 26(1):82–92, PMID 31754050, doi 10.1158/1078-0432.CCR-19-1467 ; UNC Lineberger, Chapel Hill, USA ; série soumise 10 mai 2019, publique 10 déc. 2019 ; BioProject PRJNA542388, SRA SRP197641) — fichiers officiels : Yeh_seq `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/suppl/GSE131050_PurIST_Yeh_seq.tsv.gz` (SHA `2fc0a66e…be5b1`, 9 468 179 o) ; Linehan_seq `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/suppl/GSE131050_PurIST_Linehan_seq.tsv.gz` (SHA `729bb794…efc16`, 5 157 464 o) ; matrices GPL18573 `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/matrix/GSE131050-GPL18573_series_matrix.txt.gz` (SHA `9b333eb6…7843e`, 6 864 o) et GPL16791 `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/matrix/GSE131050-GPL16791_series_matrix.txt.gz` (SHA `03aa8ca6…1df94`, 4 859 o). Lot Yeh_seq FF : 42 tumeurs PDAC primaires flash-frozen (plateforme GPL18573 Illumina NextSeq 500), médiane des réplicats FF pour 4 tumeurs sur 42 ; nature FPKM vs TPM indéterminée (valeurs prises telles que fournies). Flux : `data_flux/pdac_874_yeh_ff_fluxes.csv` (42 lignes, SHA `db258c99…58fe44`), nuls graine 42 (`e9468376…2305b`), 8741 (`627bbf22…771c5`), 8742 (`68d95935…483`). Extraction 4/4 à 0,0 exact (`results/maxsep_874_verify.json`). Manifestes `manifest_v62_874.txt` (`d130c20b…29f`) et `manifest_v62_874_frais.txt` (`4df63561…9094`). Piste suivante nommée : lot Yeh_seq FNA (n = 42 codes), non vérifiée ; lot Linehan_seq inutilisable comme paire principale (37 patients, pré/post mélangées). Détail au §8.74 et dans `PROVENANCE_874.md`.

---

## 27. Clôture du résidu M2 — 40 nuls frais ICGC / GSE62452 (20–21 nov. 2026)

- **Aucune donnée nouvelle** hors des CSV déjà sur disque et de 40 nuls frais : ICGC s61–s90 (`data_flux/pdac_immune_icgc_fluxes_nul_s61.csv` … `s90.csv`) et GSE62452 s31–s40 (`data_flux/pdac_immune_geo62452_fluxes_nul_s31.csv` … `s40.csv`), SHA dans `results/nulls_icgc_gse_875_files.json` (SHA `40ac6212…04b`). Réels relus, jamais re-téléchargés : ICGC `10823879…8adc`, GSE62452 `97c4689a…79a3` (provenances `PROVENANCE_immune_v6.md`, `PROVENANCE_icgc.md`, `PROVENANCE_geo62452.md`). Nuls existants relus : ICGC s11–s30 (§8.53), s31–s40 (§8.63), s41–s60 (§8.73) ; GSE62452 s11–s30 (§8.53). Lot v6.2 fast 40/40 exit 0 (FIN 21 nov. 2026 00:50:42Z), manifeste `manifest_v62_875.txt` (`a8f815b6…`). Verdict : TRANCHÉ–CONFIRMÉ — 24/30 et 9/10 choisissent la config réelle, taux stabilisé 80 %, M2 EXPLIQUÉ. Erreur de transcription documentée et corrigée dans `m2_cloture_875.py` (copie de `fwhm_rob_from_curve`, rob reproduite à 0,00e+00 sur 1 320 configs). Détail au §8.75 et dans `PROVENANCE_875.md`.

---

## 28. Lot Yeh_seq FNA — GSE131050, robustesse appariée (§8.76, 20–21 nov. 2026)

**Aucun nouveau téléchargement dans ce chantier** : le fichier source est
celui téléchargé officiellement au §8.74 (20 nov. 2026), SHA re-vérifié
identique avant le gel et avant la construction (voir `PROVENANCE_876.md`,
SHA `82672091…`). Protocole gelé `PROTOCOL_maxsep_gse131050_fna_876.md`
(SHA `dd7937ee…`).

- **Série : GSE131050**, NCBI GEO — Rashid et coll., *Clin Cancer Res*
  2020, 26(1):82–92, PMID 31754050, doi 10.1158/1078-0432.CCR-19-1467
  (UNC Lineberger, Chapel Hill, USA). BioProject PRJNA542388, SRA
  SRP197641. Sous-série [RNA-Seq] de la SuperSeries GSE131049.
- **Fichiers source (déjà dans `data/`, §26) :**
  - `data/GSE131050_PurIST_Yeh_seq.tsv.gz` — 9 468 179 o, SHA-256
    `2fc0a66ef0ac62aab17e9bda1c78561786f887a9122591a9346a868f852be5b1`
    — URL : `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/suppl/GSE131050_PurIST_Yeh_seq.tsv.gz`
  - `data/GSE131050-GPL18573_series_matrix.txt.gz` — 6 864 o, SHA-256
    `9b333eb6b9181fedfc793b9a61f5970af459a5b37b8aa8f7808a3b6c34c7843e`
    — URL : `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/matrix/GSE131050-GPL18573_series_matrix.txt.gz`
- **Lot FNA :** 42 codes-tumeurs (45 colonnes FNA primaires regroupées
  par code `MMDDT#`, médiane pour les 2 codes à réplicats) ; 41 codes sur
  42 sont les MÊMES tumeurs que le lot FF du §8.74 — le lot FNA n'est PAS
  une treizième paire principale indépendante et n'entre pas dans le compte
  A2 (12 paires) : c'est un test de robustesse apparié (mêmes tumeurs,
  autre type d'échantillon : FNA ex-vivo, kit TruSeq RNA Exome, échelle
  KRAS ~4 fois plus basse que FF). Verdict §8.76 : CONFIRME, d_maxsep
  +0,1642 (réel 0,4104+… — voir §8.76 ; test apparié, mêmes patients
  que FF).
- **Flux produits :** `data_flux/pdac_876_yeh_fna_fluxes.csv` (42 lignes,
  SHA `70697b3a…210324`), nul graine 42 SHA `2474ceaf…4d35`. Manifeste
  `manifest_v62_876.txt` (SHA `0e63d732…9f7`). Détail au §8.76 et dans
  `PROVENANCE_876.md`.

---

## 29. Chantier §8.77 — réparation de la reproductibilité (21 nov. 2026)

**Objet :** fermer les gaps du §17 (19 fichiers bruts sans URL + SOFT
GPL20769 + clinique du test C sans provenance + URL reconstruite de
`mit_test.csv` + URL directes CPTAC) **sans toucher aux verdicts déjà
écrits** (règle de Zackary, 20 nov. 2026, 19h40 : section à part, sans
réécrire l'histoire). Protocole gelé avant les travaux :
`PROTOCOL_reproductibilite_877.md` (SHA-256
`dbe1746f7233e69a3052407576ebf6043080016c97a12d41f76244fc569a4030`,
21 nov. 2026, 01h37 UTC). Pipeline v6.2 SHA
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant et après les runs, inchangé). Dossier de travail :
`~/workspace/runs/pdac-v6/repro_877/` (re-téléchargements dans
`repro_877/downloads/`, test à froid dans `repro_877/cold/` ; journal
`repro_877/JOURNAL_877.md`).

### 29.1 Résultat gap par gap (toutes les URL vérifiées par SHA-256)

| Gap | Fichiers | URL retrouvée (source lue) | Vérification |
|---|---|---|---|
| ng3398 MOESM59–63 | 5 | `static-content.springer.com/esm/art%3A10.1038%2Fng.3398/MediaObjects/41588_2015_BFng3398_MOESM{n}_ESM.{ext}` (patron Springer attesté par Bailey MOESM270, §5.5 ; page Nature ng.3398 lue) | 5/5 tailles + SHA-256 identiques (§3.2) |
| Birnbaum MOESM1–5 | 5 | `static-content.springer.com/esm/art%3A10.1186%2Fs12943-017-0739-z/MediaObjects/12943_2017_739_MOESM{n}_ESM.xlsx` (page PMC5674743 lue, DOI 10.1186/s12943-017-0739-z) | 5/5 tailles + SHA-256 identiques (§13) |
| ICGC probe map | 1 | `https://icgc.xenahubs.net/download/PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp.gz` (hub Xena) | taille 353 314 o, SHA `b09a746f…75537` (§5.3) |
| ICGC NMF | 1 | `https://icgc.xenahubs.net/download/PACA-AU/nature16965-s2_NMF_class_assignment.txt.gz` (hub Xena ; le `.txt` nu = 404) | taille 447 o, SHA `f1e84b99…21e2f` (§5.4) |
| PRISM 24Q2 meta | 1 | `https://ndownloader.figshare.com/files/46630978` (API figshare 25917643, fichier 46630978) | taille 157 294 o, SHA `13a85da9…3b0526` (§7) |
| PRISM 19Q4 (4 fichiers) | 4 | `https://ndownloader.figshare.com/files/20237739` (dose-response), `…/20237763` (replicate-collapsed), `…/20237769` (cell-line-info), `…/20238123` (readme) — API figshare 9393293 | 4/4 tailles + MD5 + SHA-256 identiques (§8) |
| QCMG clinique | 2 | `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_qcmg_uq_2016/data_clinical_patient.txt` (+ `…_sample.txt`) | SHA `ae7fc6d7…6a95` / `c70daf3e…ceca` (§12) |
| Clinique test C | 1 | `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_tcga_pan_can_atlas_2018/data_clinical_patient.txt` (étude `paad_tcga_pan_can_atlas_2018`) | taille 58 621 o, SHA `0c274268…2efe5` (§11) |
| SOFT GPL20769 | 1 | `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL20nnn/GPL20769/soft/GPL20769_family.soft.gz` | taille 37 588 662 o exactement, table 19 749 lignes, MD5 `4c39e802…`, SHA `ecb1b79a…22d3e` (§3.1) |
| `mit_test.csv` | 1 | `https://raw.githubusercontent.com/ncats/PANC1/main/MIT/test.csv` (URL reconstruite, vérifiée) | taille 3 249 228 o, SHA `9f3ae189…6e27` (§10) |
| CPTAC (4 fichiers) | 4 | `https://zenodo.org/api/records/8394329/files/<nom>/content` (champ `links.self` lu dans l'API Zenodo) | tailles + MD5 conformes (§6) |

**Bilan : 19/19 fichiers du §17 fermés + SOFT GPL20769 + clinique du test
C + `mit_test.csv` + URL directes CPTAC. Aucun gap irrécupérable. Aucune
URL inventée sans vérification SHA.**

### 29.2 Voies infructueuses consignées (échecs honnêtes, aucun gap caché)

- Listing du bucket S3 Xena : HTTP 403 ; URL S3 directes des fichiers
  ICGC : 403 — c'est l'URL du hub `icgc.xenahubs.net` qui fonctionne.
- Europe PMC `supplementaryFiles` pour PMC5674743 : HTTP 500 (page HTML
  d'erreur, 19 606 o) — les suppléments Birnbaum ont été récupérés par
  le patron Springer direct, vérifié par SHA.
- Page Nature ng.3398 via curl : HTTP 303, section suppléments non
  lisible par ce moyen ; la page lue par le navigateur confirme le titre
  et l'article, les URL ont été vérifiées par SHA.
- Chemin FTP GEO `GPL2nnn/GPL20769/` : 404 — le bon chemin est
  `GPL20nnn/` (règle des 3 derniers chiffres masqués).
- `raw.githubusercontent.com` pour les fichiers datahub : renvoie le
  pointeur Git LFS (130 o), pas le contenu — le contenu réel est servi
  par `media.githubusercontent.com`. Le pointeur LFS du fichier test C
  porte lui-même `oid sha256:0c274268…` (double confirmation).

### 29.3 Script corrigé

`repro_877/download_data_877.sh` (SHA-256
`558111360ceda48bece577d7176a5ad5e46630f0a39fc85c03e8c3635564c78f`,
diff `repro_877/download_data_877.diff`, 323 lignes changées) — corrections
§4 du protocole : PANC-1 fichier par fichier (tarball tronqué), PRISM
19Q4 4/4, PRISM 24Q2 avec hachages + métadonnées, suppléments ng3398 et
Birnbaum, SOFT GPL20769 (chemin corrigé), ICGC probe map/NMF, QCMG,
clinique PanCanAtlas ; CPTAC : URL directes en commentaire (voie API
conservée) ; durcissement `--retry-all-errors --retry-delay 5` partout ;
OmicsCN via ndownloader (endpoint API figshare bloqué) ; anti-blocage
`--speed-limit 1000 --speed-time 300` ; ICGC expression via l'URL du hub
(S3 directe = 403) ; reprise `get_checked()` (fichier déjà présent et
vérifié sauté, fichier partiel re-téléchargé). L'original
`~/workspace/staging-pdac/download_data.sh` (SHA `4e151d59…`) n'a pas été
modifié par ce chantier. Deux fautes de frappe dans des SHA consignés ont
été trouvées et corrigées par le test du script complet : Birnbaum MOESM3
§13 (62 caractères au lieu de 64) et LUAD §2.3 (65 caractères au lieu de
64) — voir §29.4.

### 29.4 Test à froid (TCGA v4, réel + nul)

Voir §8.77 §5 pour les chiffres comparés. Chaîne complète, dossier
propre `repro_877/cold/` : re-téléchargement TCGA via l'extrait littéral
du script corrigé (`cold/cold_tcga.sh`, 4 tarballs OK, MD5 vérifiés ;
PAAD RSEM SHA-256 `c3dd138b…62c9` = §2.1) → reconstruction des flux par
copie de `build_fluxes_tcga_v4.py` (seules les 2 constantes de chemins
changées, diff consigné) → flux reconstruits **SHA-identiques** aux flux
tenus (`e7a2adab…0b0`, `895a4562…da4`) → runs v6.2 mode `fast`
(unités `repro877-cold-runs`, journal `cold/runs_cold_877.log`) →
extraction par `extract_858.extract`, comparaison aux chiffres tenus
(§8.37). Le script corrigé complet (~2,4 Go, 52 fichiers) a aussi été exécuté en
entier — **résultat final : EXIT:0** (journal `cold/full_script_877i.log`,
21 nov. 2026, 04:15–04:17 UTC : 36 fichiers « DÉJÀ PRÉSENT ET VÉRIFIÉ »
+ 16 OK frais, 0 erreur, « TERMINE : tous les jeux de données
téléchargés et vérifiés »). **Incidents consignés (tous surmontés, aucun
maquillé) :** (1) première exécution arrêtée au tout premier fichier
(CRISPRGeneEffect.csv, `ndownloader.figshare.com`) sur un HTTP 403
transitoire, après ~90 s à 0 octet ; la même URL répondait 302 quelques
minutes plus tard (limitation de débit figshare probable) — correctif
`--retry-all-errors --retry-delay 5` ; (2) blocages à 0 octet de
l'endpoint API figshare (OmicsCN, 9+ min) et de GDAC (13+ min) —
diagnostic : les unités systemd n'héritent pas des variables proxy de
l'environnement d'exécution ; en accès direct, api.figshare.com et
gdac.broadinstitute.org restent bloqués alors que ndownloader fonctionne
— les lots longs doivent être lancés AVEC le proxy
(`--setenv=https_proxy=http://hatch-egress-proxy:3128`, sans
identifiants) ; correctifs `--speed-limit 1000 --speed-time 300` et
OmicsCN via ndownloader ; (3) URL S3 directe ICGC = HTTP 403
(4 tentatives) — correctif : URL du hub (même fichier, SHA identique) ;
(4) redémarrage machine pendant l'exécution (27 fichiers OK, unité
transiente perdue) — correctif : reprise `get_checked()` ; (5) PANC-1
calc.csv bloqué à 0 octet (4 tentatives) dans l'unité alors que le même
fichier se télécharge en < 2 s depuis l'outil exec — cause exacte non
élucidée, consignée comme telle ; la reprise depuis l'outil exec a
passé. **Deux fautes de frappe dans des SHA consignés, trouvées par le
test :** Birnbaum MOESM3 §13 (valeur de 62 caractères,
`…a9b8ae…` au lieu de `…a9d9b8ae…` — la comparaison par SHA tronqués ne
l'avait pas vue ; trois téléchargements indépendants d'accord sur la
vraie valeur) et LUAD §2.3 (65 caractères, un `d` en trop) — corrigées
ici et dans le script. Détail complet au §8.77 (§8.77.5–§8.77.6) et dans
`repro_877/JOURNAL_877.md`.

### 29.5 Ce qui reste ouvert

**Rien** sur les fichiers bruts : chaque fichier brut du projet a
désormais une URL de téléchargement vérifiée par SHA-256. Restent hors
périmètre (déjà documentés, non rouverts) : les fichiers dérivés se
reconstruisent par scripts (§14) ; les résultats `results_fast_*` (~7 Go)
ne sont pas dans le dépôt par limite snapshot mais se reconstruisent par
les runs (le test à froid le démontre pour la paire TCGA v4) ; les
matrices brutes (~2,4 Go) ne sont pas dans le dépôt par limite snapshot
mais se re-téléchargent vérifiées par le script corrigé.

## 30. Inventaire des dépôts §8.78 — supplément Chen et al. 2025 (21 nov. 2026)

**Aucun nouveau téléchargement de données dans ce chantier** (inventaire en lecture seule,
`PROTOCOL_inventaire_depots_878.md`, SHA `39667dc4…` ; provenance `PROVENANCE_878.md`, SHA
`802e22cf…`). Une seule source de données NOUVELLE est citée avec son hachage vérifié — la
candidate C1 pour la piste B :

- **Chen et al. 2025, *Nature Communications* (matrice AUC 46 PDO × 63 médicaments)**,
  DOI 10.1038/s41467-025-57520-3. Supplément Springer MOESM13 :
  `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM13_ESM.xlsx`,
  SHA-256 `0e009cd56d2f6c25b0b355590becc4abfee3e1080633173bc33606d1bf325340` (vérifié §8.78 §8.78.8 C1) ;
  input pipeline local `candidate_NatureComm2025_PAAD/NatureComm2025_46PDO_63Drug_AUC.csv`
  (SHA `296681b64d3ad5309aab349696439257185f0e679cf50a35858a898b046cb3fd`, non versé).
  n = 46 PDO — rejetée sous v5.9.4 (minimum 50), candidate sous v6.2 fast (minimum 40).
  Piste suivante nommée au §8.79.9 (lot drogue, cible Gemcitabine) — pas encore courue.

---

## 31. Treizième paire GSE57495 et arrêt C2 GDC (§8.79, 21 nov. 2026)

**GSE57495 — déjà couverte** (voir §21 / §8.69 : matrice `GSE57495_series_matrix.txt.gz`,
13 487 043 o, SHA `995dbeff288a14c1cc1a52489e456b7677ede5da8e287069b8298d649b532efc`, 63 tumeurs,
plateforme **GPL15048**, mapping `GPL15048_probe2symbol.tsv` SHA `93e01ec3…998f952`). Rappetée ici
parce que la paire pipeline §8.79 la court pour la première fois (11 flux, GSTM1 absent) —
**avec son caveat** : déjà tenue comme holdout direct (§8.66/§8.69, ρ KRAS–CEACAM5 = 0,4377),
donc JAMAIS une confirmation indépendante de KRAS–CEACAM5. CSV de flux réel
`pdac_879_geo57495_fluxes.csv` SHA `224f98eb9cc7092e05b490b1e053edd14793e3def147890be0bab567630bb51c`,
nul SHA `5cd274594a9a256142eb5fc539645e51a6dca2f0f15b2084b9884f686ab41edf`.

- **GDC ORGANOID-PANCREATIC — candidate C2 ARRÊTÉE (§8.79 §3).** Projet GDC
  `ORGANOID-PANCREATIC` (Human Cancer Models Initiative / Next Generation Cancer Models),
  55 quantifications RNA-seq ouvertes (STAR Counts, GENCODE v36). Manifeste :
  `https://raw.githubusercontent.com/FindPrint/pdac-systems-evidence-preclinical/main/data/external-links/GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST.tsv`,
  SHA-256 `f713edebf0f8afb20305b1472d480564e45ac31ce79e28350d7dde6ae496220b` ;
  copie locale `data/GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST_879.tsv`.
  Téléchargement réussi 55/55 fichiers, MD5 conformes au manifeste, **total 232 648 892 o exact**
  (`download_gdc_879_receipt.json`) ; accès par `https://api.gdc.cancer.gov/data/<file_id>`
  (cas interrogés par `POST https://api.gdc.cancer.gov/cases`, 49/49 ; fichiers par
  `POST https://api.gdc.cancer.gov/files`, 55/55). **Arrêt : DPCR1 absent de 55/55 fichiers**
  (symbole retiré de GENCODE v36 ; HGNC : DPCR1 = ancien symbole de MUCL3, présent 55/55) —
  aucun CSV C2, aucun run C2. Les 55 TSV restent détenus pour un protocole futur qui
  pré-enregistrerait MUCL3. Protocoles `PROTOCOL_nouvelle_serie_879.md` (C2, SHA `84b1adfa…`)
  et `PROTOCOL_nouvelle_serie_879_C3.md` (addendum C3, SHA `a4399737…`) ;
  provenance `PROVENANCE_879.md` (SHA `a42060fe…`).

---

## 32. Piste Œil — TCGA-UVM (§8.81, 21 nov. 2026)

**Nouveau téléchargement (réussi du 1er coup, 21 nov. 2026, 12h15 UTC).**
Broad GDAC Firehose stddata 2016-01-28, UVM, RSEM genes normalized :
`https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/UVM/20160128/gdac.broadinstitute.org_UVM.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz`,
fichier local `data/tcga_uvm_rsem.tar.gz`, **6 311 998 o**,
SHA-256 `b50fdadb00d5c4095ffbe55ad4192cfca892c947cd657d032be128ba074a9975`.
**80 tumeurs primaires** (code 01) ; les 12 gènes v4, les 7 gènes de privilège et les 4 témoins
sont tous présents en UVM. Valeurs log2(RSEM+1), sans correction de pureté (pas de scores
acineux/îlots pour l'œil). Sources PDAC du chantier déjà sur disque (TCGA-PAAD MD5 `b09569ce…`,
GSE71729, GSE62452, ICGC) — aucun nouveau téléchargement pour elles. Protocole
`PROTOCOL_oeil_privilege_881.md` (SHA `c985a03a…`) ; provenance `PROVENANCE_881.md`
(SHA `3755cd98…`). Verdict §8.81 : MIXTE (voir §8.81).

---

## 33. Cerveau — TCGA-GBM (§8.82, 21 nov. 2026)

**Nouveau téléchargement (21 nov. 2026 ; première URL tentée portait une coquille — `20160128`
au lieu de `2016012800` — 404 ; l'adresse du répertoire listait le bon nom).**
Broad GDAC Firehose stddata 2016-01-28, GBM, RSEM genes normalized, répertoire :
`https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/GBM/20160128/`,
fichier local `data/tcga_gbm_rsem.tar.gz`, **14 116 395 o**,
MD5 `cfc6cf0a2c3c2e9f0ea7a11f2ba32d28` (égal au MD5 servi par le dépôt, vérifié avant le gel),
SHA-256 `9996a653f26c8cf8f0a5c56db49e2c847b49c0d1c9823daa5bb050d13749eb83`.
Matrice interne : 20 532 lignes, 20 503 gènes uniques après déduplication, × 171 échantillons ;
matrice interne 30 268 366 o. **153 tumeurs primaires** (code TCGA 01) ; 18 écartées (codes 02 et 11) ;
153/153 cas complets, aucune imputation. Transformation log2(RSEM+1), aucune correction de pureté.
Protocole `PROTOCOL_cerveau_privilege_882.md` (SHA `487fc59d…`) ; provenance `PROVENANCE_882.md`
(SHA `837622d9…`). Verdict §8.82 : privilège DESCEND, GBM FROID, pipeline PARTIEL fragile.

---

## 34. Survie des gènes de privilège (§8.83, 21 nov. 2026)

**Aucune source nouvelle dans ce chantier** (hors pipeline) : TCGA (tarball MD5 `b09569ce…`,
fichier clinique SHA `0c274268…`), GSE71729 (SHA `b2287893…`), ICGC (exp SHA `c2cb57af…`,
probemap `b09a746f…`, Bailey XLSX `778224b3…`) — toutes déjà couvertes (voir §§1, 5, 11).
Calibration reproduite 3/3 (Cox MUC16 1,4392 / 1,5688 / 1,0625 ; log-rank 0,0703 / 0,0019 / 0,7292 ;
n 177/70/125 ; décès 92/47/84). Protocole `PROTOCOL_survie_privilege_883.md` (SHA `0eb83d63…`,
amendé avant lecture des résultats privilège) ; provenance `PROVENANCE_883.md` (SHA `5f249140…`).
Verdict §8.83 : 3 items sur 8 prédisent la survie comme CA125, mais le signal ne passe pas par KRAS.

**§8.80 (veille clinique vopimetostat + daraxonrasib) : aucune donnée nouvelle mesurée ni
téléchargée** — veille documentaire (protocole `PROTOCOL_vopimetostat_nouvelles_880.md`,
SHA `169b9d7e…` ; provenance `PROVENANCE_880.md`, SHA `3b17b776…`) ; sources citées dans la
section §8.80 (communiqués Tango / Revolution Medicines, ESMO 2026, ENA 2026), pas des matrices.

---

## Annexe A — Commandes de vérification (après re-téléchargement)

```bash
# 1. Tout re-télécharger + vérifier (script maître ; voir ses limites au §0.1)
bash ~/workspace/staging-pdac/download_data.sh ./data

# 2. Vérifications manuelles complémentaires (depuis §8.77, la plupart des
# fichiers sont désormais DANS le script corrigé ; il ne reste hors script
# que la table GPL6244, dérivée du SOFT)
python3 ~/workspace/runs/pdac-v6/download_gpl6244_mapping.py   # GPL6244_probe2symbol.tsv
# PRISM 19Q4 : les 4 fichiers sont dans le script corrigé (§8.77) ; rappel
# des URL directes (API figshare) :
curl -s https://api.figshare.com/v2/articles/9393293 | python3 -c "import json,sys; [print(f['name'], f['download_url']) for f in json.load(sys.stdin)['files']]"
# CPTAC : dans le script corrigé via l'API Zenodo (§8.77) ; rappel :
curl -s https://zenodo.org/api/records/8394329 | python3 -c "import json,sys; [print(f['key'], f['links']['self']) for f in json.load(sys.stdin)['files']]"

# 3. Vérifier les hachages contre ce document (exemples)
cd ~/workspace/runs/pdac-v6/data
sha256sum CRISPRGeneEffect.csv Model.csv OmicsCNGene.csv OmicsSomaticMutationsMAFProfile.maf
sha256sum GSE71729_series_matrix.txt.gz GSE62452_series_matrix.txt.gz icgc_pacaau_exp.txt.gz bailey2016_suppl_tables1-13.xlsx
sha256sum GDSC2_fitted_dose_response_27Oct23.xlsx secondary-screen-dose-response-curve-parameters.csv
md5sum tcga_paad_rsem.tar.gz tcga_luad_rsem.tar.gz tcga_coad_rsem.tar.gz tcga_paad_gistic.tar.gz
md5sum cptac/*.gz

# 4. Vérifier que le fichier clinique test C est le bon (SHA consigné, provenance manquante)
sha256sum ~/workspace/runs/pdac-v6/data_clinical_patient.txt
# attendu : 0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5
```

## Annexe B — Provenances lues pour rédiger ce document

`PROVENANCE_depmap.md`, `PROVENANCE_tcga.md`, `PROVENANCE_tcga_v2.md`, `PROVENANCE_tcga_v3.md`, `PROVENANCE_tcga_v4.md`, `PROVENANCE_cptac.md`, `PROVENANCE_geo71729.md`, `PROVENANCE_geo62452.md`, `PROVENANCE_geo71729_survival.md`, `PROVENANCE_icgc.md`, `PROVENANCE_gdsc.md`, `PROVENANCE_prism_secondary.md`, `PROVENANCE_kras_g12d.md`, `PROVENANCE_kras_combinations.md`, `PROVENANCE_crispr_scan.md`, `PROVENANCE_mtap.md`, `PROVENANCE_mtap_pancancer.md`, `PROVENANCE_mtap_series.md`, `PROVENANCE_prmt5_mtap.md`, `PROVENANCE_mtap_prmt5_flux.md`, `PROVENANCE_mtap_arbitration_840.md`, `PROVENANCE_pancancer.md`, `PROVENANCE_parp_v6.md`, `PROVENANCE_immune_v6.md`, `PROVENANCE_immune_parp_v6.md`, `PROVENANCE_atr_chek1.md`, `PROVENANCE_muc16_cldn182.md`, `PROVENANCE_rotations.md`, `PROVENANCE_rotations_v61.md`, `PROVENANCE_rotations_dedup_844.md`, `PROVENANCE_testA_proliferation.md`, `PROVENANCE_testC_stage.md`, `PROVENANCE_v6.1.md`, `PROVENANCE_v6.2.md`, `PROVENANCE_878.md`, `PROVENANCE_879.md`, `PROVENANCE_880.md`, `PROVENANCE_881.md`, `PROVENANCE_882.md`, `PROVENANCE_883.md`, `PROVENANCE_priv_881.json`, `source_registry.md` (registre de synthèse du 16 nov. 2026), `~/workspace/staging-pdac/download_data.sh`, `~/workspace/runs/pdac-v6/download_gpl6244_mapping.py`, journaux `data/download_depmap.log`, `data/download_firehose.log`, `data/download_omicscn.log`, réponses JSON `data/panc1_api.json`, `data/panc1_9191.json`, `data/panc1_9197.json`, `data/panc1_ncats.json`.

**Écarts relevés pendant la rédaction (signalés dans le texte) :**
1. `PROVENANCE_geo62452.md` indique 819 249 octets pour `GPL6244_probe2symbol.tsv` — c'est la taille de `GPL570_probe2symbol.tsv` ; le fichier GPL6244 fait 382 034 octets (25 293 sondes, contenu conforme).
2. `source_registry.md` attribue la source PANC-1 à `PROVENANCE_crispr_scan.md` — la provenance réelle est `PROVENANCE_kras_combinations.md`.
3. `PROVENANCE_icgc.md` (et `source_registry.md`) citent le premier auteur « Forcina et al. 2017 » pour l'étude de combinaisons PDAC — le premier auteur réel est Langdon et al. (doi `10.1158/1535-7163.MCT-16-0794`).

*Rien n'a été modifié dans `~/workspace/runs/pdac-v6/` (lecture seule). Hachages « calculés localement le 19 nov. 2026 » : `sha256sum`/`md5sum` sur les fichiers locaux, sans modification.*
