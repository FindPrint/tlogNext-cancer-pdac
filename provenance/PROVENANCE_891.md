# PROVENANCE — §8.91 : re-dérivation de GSE194249 depuis les lectures brutes (SRA)

Date : 21 novembre 2026, ~11h10–11h30 EST.
Chantier §8.91, piste 1 du lot du 21 nov. 2026. Go de Zackary :
21 nov. 2026, 11h09.
Protocole gelé : `PROTOCOL_gse194249_sra_891.md` (ce chantier).
Auteur : TagPrint (coordinateur des 2 pistes).
Statut : vérification d'accès aux métadonnées — aucune donnée
d'expression lue, aucune lecture brute téléchargée, aucun run.

## 1. Série et article (repris des §8.86/§8.88, jamais recalculés)

- Série : **GSE194249**, Shi et al., *Nature Communications* 2022,
  13:2169, DOI 10.1038/s41467-022-29857-6 (CC BY 4.0).
  GEO : https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE194249
  (page directe bloquée par reCAPTCHA le 21 nov. 2026, comme au
  §8.86 ; métadonnées via E-utilities).
- Plateforme : GPL31265, dépôt 2022/02/23, *Homo sapiens*,
  87 échantillons (84 PDPCOs + 3 normaux `NPC-*`).
- Matrice FPKM déposée déjà couverte aux §8.86/§8.88 :
  `GSE194249_PDPCOs_FPKM.txt.gz`, 4 927 876 o, SHA-256
  `479517fbed1d8f5bb9d141b6b932b6ab56ba2ba72d4394d13aea2a3da0a50f27`,
  15 609 lignes de gènes, DPCR1 0 occurrence, MUCL3 0 occurrence.

## 2. Accès aux lectures brutes — sources consultées (21 nov. 2026)

| # | Source | Requête / URL | Résultat | Reçu (SHA-256) |
|---|---|---|---|---|
| 1 | NCBI E-utilities, esummary BioProject | `esummary.fcgi?db=bioproject&id=799993,801501&retmode=json` | PRJNA799993 : « Raw data are not available for this Series due to human genetic resources policy in China. » ; PRJNA801501 : données brutes vers NODE, accès contrôlé, OEP001744 | `gse194249_bioproject_891.json`, `e5a85000f939c6a88d59f546624dc851ecdbb12e4afbe6759435d0ce76b0e455` |
| 2 | NCBI E-utilities, esearch SRA | `esearch.fcgi?db=sra&term=PRJNA799993&retmode=json` | count **0** | `sra_esearch_PRJNA799993_891.json`, `a6df6133df098ed299a26cdc05ba79c745f440dd83063a796d63602403b18155` |
| 3 | NCBI E-utilities, esearch SRA | `esearch.fcgi?db=sra&term=PRJNA801501&retmode=json` | count **0** | `sra_esearch_PRJNA801501_891.json`, `014a217cd4fb85bab77d0d46d4546903d7c5d344700da3de72d5b3a8e9abb7c2` |
| 4 | NCBI E-utilities, elink GDS→SRA | `elink.fcgi?dbfrom=gds&db=sra&id=200194249&retmode=json` | aucun lien (linksets sans `linksetdbs`) | `elink_gds_sra_891.json`, `e7498743d2ce11d1356af7ee0d4d4faacc55f322823d150ab2d74bd62d2f87c5` |
| 5 | NCBI E-utilities, esearch SRA | `esearch.fcgi?db=sra&term=GSE194249&retmode=json` | count **0** | (réponse en ligne, non conservée en fichier — même résultat que #2) |
| 6 | ENA, portail de recherche | `https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=study_accession%3DPRJNA799993&format=json&fields=run_accession,library_strategy` | liste vide `[]` — 0 run | `ena_readrun_PRJNA799993_891.json`, `2ba33ca0557f1bb5b7ba88d67f9d0093c7185a36ec51fe2b7bd9372d3e001d6d` |
| 7 | NODE (biosino.org) | `https://www.biosino.org/node/project/detail/OEP001744` | HTTP 200, 906 o (coquille JS, fiche non lisible) ; accès contrôlé établi par la fiche PRJNA801501, pas par cette page | (aucun reçu utile — page coquille) |
| 8 | Recherche web exacte | `"OEP001744" NODE biosino` | aucun résultat utilisable | (recherche du 21 nov. 2026, ~11h30 EST) |

Citations verbatim (fiches BioProject, reçues #1) :

- PRJNA799993 : « Raw data are not available for this Series due
  to human genetic resources policy in China. »
- PRJNA801501 : « Please note that the raw data has been uploaded
  to a domestic repository National Omics Data Encyclopedia (NODE;
  https://www.biosino.org/node/index) with controlled access
  mechanisms under accession number OEP001744. »

## 3. Ce qui n'a PAS été fait

- Aucune lecture brute téléchargée (aucune n'existe en libre accès).
- Aucune demande d'accès contrôlé à NODE (hors périmètre, sans go).
- Aucun contact des auteurs.
- Aucun fichier d'expression lu, aucun CSV de flux construit,
  **0 run v6.2**.
- Aucune substitution de cohorte ni de gène.

## 4. Outillage et machine (contexte, 21 nov. 2026)

- Quantification absente : `salmon`, `kallisto`, `samtools`,
  `STAR`, `hisat2`, `fasterq-dump`, `prefetch`, `pysradb` —
  tous absents de la machine.
- Disque : 121 Go libres sous `/home/hatch`.
- Pipeline v6.2 vérifié inchangé, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié le 21 nov. 2026 avant travaux ; aucun run lancé).
- Livre blanc au moment du chantier : SHA
  `39d3abd65eda029efb959934ecdf17a10f14ba85b0b15f9c03c9e86fc8358696`,
  22 783 lignes, §8.1–§8.89 (fusion §8.90 en cours par le
  finisseur, non touchée).

## 5. Ce qui manque

- Les lectures brutes elles-mêmes (inaccessibles en libre accès).
- La réponse à « DPCR1/MUCL3 sont-ils quantifiables depuis les
  lectures brutes ? » — elle exige les lectures.
- Toute information sur les conditions d'accès à NODE OEP001744
  (délai, critères, formulaire) — non recherchée au-delà de la
  fiche BioProject.

— Fin de la provenance §8.91. —
