# PROVENANCE — §8.66 : Bloc estomac / mucus, quatrième cohorte (GSE62165)

Date : 20 nov. 2026. Chantier §8.66, mission parent du 20 nov. 2026.
Protocole gelé `PROTOCOL_stomach_mucus_cohort4_866.md`,
SHA-256 `3a25a39135711d670443c6689bac7efdf8e61e5fb3c0a03497f26474958d91bc`
(écrit avant tout téléchargement).

## Pipeline (jamais modifié)

- `universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant les runs ; v6.1 `2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`).
- Mode fast, graine des nuls 42, `rng(42)`.

## Cohorte : GSE62165 (quatrième cohorte, indépendante)

- Dépôt : NCBI Gene Expression Omnibus (GEO), série GSE62165.
- Déposants : Rekin's Janky et coll., Nucleomics Core, VIB, Leuven
  (Belgique) ; contact : Nucleomics.Bioinformatics@vib.be.
- Soumission : 8 oct. 2014 ; publique : 17 août 2016 ; dernière
  mise à jour : 21 mars 2019. Publication associée : PMID 27520560
  (« Prognostic relevance of molecular subtypes and master
  regulators in pancreatic ductal adenocarcinoma », Janky et coll.).
  Analyse par stade : Wang et coll., *Cancer Cell Int* 2018,
  doi 10.1186/s12935-018-0718-5.
- Plateforme : GPL13667 (Affymetrix Human Genome U219 Array),
  organisme *Homo sapiens* (taxid 9606). BioProject PRJNA263337.
- Fichier téléchargé : `data/GSE62165_series_matrix.txt.gz`
  - URL : `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62165/matrix/GSE62165_series_matrix.txt.gz`
  - HTTP 200, 51 179 939 octets.
  - SHA-256 : `fd50fc415a31a4d19a4af82e29afc6909e913f4f223d0b4cd4b637ae4a03727f`
- Contenu vérifié après téléchargement : 49 386 sondes × 131
  échantillons, 0 NaN ; 118 tumeurs pancréatiques + 13 tissus
  non tumoraux ; valeurs log2 déjà normalisées par les déposants
  (min 2,084 ; max 14,447 ; médiane 4,707) — aucune
  renormalisation faite ici.
- Stade par échantillon (`!Sample_characteristics_ch1`,
  champ « Stage: ») : tumeurs 1a 1, 1b 7, 2a 30, 2b 62, 3 5,
  4 13 — soit rangs I 8, II 92, III 5, IV 13 ; identique aux
  effectifs publiés (Wang et coll. 2018). Témoins : « Stage: NA »
  (13). Champ « grouped stage » : Early 38, LNM 62, Advanced 18,
  NA 13 (non utilisé).
- Critères d'acceptation (§2 du protocole) : n = 118 ≥ 40 — PASSÉ ;
  stade par échantillon présent — PASSÉ ; KRAS présent comme
  ligne (vérifié dans `build_fluxes_866.py`, consigné dans la
  section) ; cohorte jamais utilisée dans ce projet (ni TCGA,
  ni GSE71729, ni GSE62452, ni ICGC PACA-AU, ni CPTAC) — PASSÉ.

## Mapping sondes → symboles (GPL13667) — adaptation documentée

Le protocole §1.1 prévoyait l'annotation de plateforme GEO
(`GPL13667.annot.gz`, repli SOFT). Constaté après le gel :
- `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL13nnn/GPL13667/annot/GPL13667.annot.gz`
  → HTTP 403 « Access forbidden » (page d'erreur, 980 o, pas un
  fichier d'annotation) ;
- `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL13nnn/GPL13667/soft/GPL13667_family.soft.gz`
  → HTTP 200 mais Content-Length 6 038 451 838 o (~6,0 Go) :
  infaisable dans ce chantier (VM 6 Go RAM, décompression de
  plusieurs dizaines de Go) — téléchargement interrompu à
  1 511 849 984 o, fichier supprimé ;
- `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL13nnn/GPL13667/miniml/GPL13667_family.xml.tgz`
  → HTTP 200, 539 314 653 o, SHA-256
  `ed094f679757fa654038e6d73db4a4122f8118739687dca388e2f450d3dab21f`
  : l'archive ne contient QUE des tables d'échantillons GSM
  (aucun fichier GPL, vérifié par `tar -tzf` puis extraction
  `--wildcards '*GPL13667*'` : « Not found in archive ») —
  inutilisable pour le mapping ; archive supprimée.
- Adaptation (même nature d'annotation, aucune sonde mappée à
  la main, règles d'exclusion écrites avant la construction
  dans `build_probe2symbol_866.py`, SHA
  `004c83391bb4e448c94fa7dbe45f0163b87982a8037770f13b90a8158e1a563b`) :
  chaîne Bioconductor AnnotationDbi standard pour la puce
  hgu219 : sonde → Entrez Gene (`hgu219.db`), puis Entrez Gene
  → symbole courant (`org.Hs.eg.db`).
  - `hgu219.db` 3.2.3 (Marc Carlson, Bioconductor Release 3.23,
    doi 10.18129/B9.bioc.hgu219.db) :
    URL `https://bioconductor.org/packages/release/data/annotation/src/contrib/hgu219.db_3.2.3.tar.gz`,
    HTTP 200, 2 002 040 o, SHA-256
    `64847ad0392b2e1f2a79eb24cc90e5359e42c2c8bf265d1ec7d2dd443ee567fb`.
    Table `probes` : 49 386 sondes distinctes ; source Entrez
    Gene 2015-Sep-27 (champ `map_metadata`).
  - `org.Hs.eg.db` 3.23.1 (Marc Carlson, Bioconductor Release
    3.23, doi 10.18129/B9.bioc.org.Hs.eg.db) :
    URL `https://bioconductor.org/packages/release/data/annotation/src/contrib/org.Hs.eg.db_3.23.1.tar.gz`,
    HTTP 200, 103 790 170 o, SHA-256
    `470620665cf49d0319422731164f377e3e74253989f1d33a8a1d100cc3d49cfe`.
    Tables `genes` (gene_id → _id) + `gene_info` (_id → symbol).
    (La version 3.23.0 n'existe pas : HTTP 404 vérifié le
    20 nov. 2026 ; la version exacte 3.23.1 est lue sur la page
    du paquet Bioconductor.)
  - Règles : sonde vers plusieurs Entrez ID → EXCLUE (ambiguë) ;
    sonde sans Entrez ID → non mappée ; plusieurs sondes vers un
    même symbole → médiane (règle du projet).
  - Résultat (`data/GPL13667_probe2symbol.tsv`, SHA-256
    `c0a5e8fcf082cc31160f21300a1edaae9ebc87886a2ca057a2c7228c7768c2b2`,
    46 084 lignes dont en-tête) : 46 083 sondes mappées vers
    18 448 symboles distincts ; 2 662 sondes multi-gènes
    exclues ; 641 sondes sans symbole. Journal :
    `GPL13667_mapping_866.txt`.
  - Limite nommée : la correspondance sonde → Entrez date de
    2015 (hgu219.db), le symbole est celui d'aujourd'hui
    (org.Hs.eg.db 3.23.1) via l'Entrez ID stable ; un symbole
    renommé depuis 2015 apparaît sous son nom actuel (ex.
    HIST1H3H → H3C8). Aucun symbole n'est inventé ni corrigé
    à la main.

## Cohorte de repli (non utilisée)

GSE57495 (protocole §1.2) : non téléchargée, non utilisée —
GSE62165 ayant passé tous les critères d'acceptation.

## Fichiers du chantier (SHA dans la section §8.66)

- `PROTOCOL_stomach_mucus_cohort4_866.md` — SHA ci-dessus.
- `build_probe2symbol_866.py` — SHA
  `004c83391bb4e448c94fa7dbe45f0163b87982a8037770f13b90a8158e1a563b`.
- `build_fluxes_866.py`, `reading_866.py`, `extract_866.py`
  (copies adaptées des scripts §8.58, originaux intacts) —
  SHA consignés dans la section.
- `inventory_866.csv` (présent/absent par gène retenu),
  `or_scan_866.csv` (scan regex des OR dans l'univers mappé),
  `direct_tests_866.csv`, `extract_866.json` / `.csv`,
  `manifest_v62_866.txt`, `runs_v62_866.log`.
- Sorties flux : `pdac_866_geo62165_<G>_<ordre>.csv` (+ `_nul.csv`).
- Dossiers runs : `results_fast_v62_866_*`.
- Section : `section_8.66_stomach_mucus_cohort4.md`.
- Livre blanc NON édité, PDF NON régénéré, rien poussé sur GitHub.
