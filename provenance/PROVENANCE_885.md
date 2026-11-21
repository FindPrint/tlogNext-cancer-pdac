# PROVENANCE_885 — GDC ORGANOID-PANCREATIC avec remappage DPCR1 → MUCL3, 14e paire (§8.85)

**Date :** 21 novembre 2026, ~08h55–09h15 EST (13h55–14h15 UTC).
**Agent :** TagPrint (subagent, piste 2).
**Chantier :** §8.85.
**Protocole gelé avant toute vérification de remappage, toute
construction et tout run :** `PROTOCOL_gdc_mucl3_885.md`, SHA-256
`2dfeeade0eceb85c7a5f109bcc589c0aab723909f483348a46a3f5e5d7379cdf`.
**Pipeline :** v6.2, SHA
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
— vérifié avant et après les lots, jamais modifié, jamais exécuté
ailleurs que dans ce chantier.
**Livre blanc local vérifié (non édité) :**
`~/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md`,
SHA-256 `ef511c1049018c6bb5971ead20a5c8887212e8c356b7cc4e6785a2395d059ba6`,
§8.1–§8.83, 20 256 lignes — identique avant et après le chantier.

## 1. Vérification du remappage DPCR1 → MUCL3 (étape 1 du protocole, après le gel)

Quatre sources lues le 21 nov. 2026 (~13h57 UTC), réponses brutes
conservées dans le chantier. Toutes concordent : DPCR1 est
l'ancien symbole du même gène que MUCL3.

### 1.1 HGNC — source primaire de nomenclature (portes R1, R2)

- `https://rest.genenames.org/fetch/symbol/MUCL3`
  (fichier `hgnc_mucl3_885.json`, SHA-256
  `c6dfe86065fc96e1e8dcfc932d08491f078f7967aa38c1fa0ca9985377c96049`,
  2 051 o, HTTP 200, XML — le REST HGNC répond en XML par défaut) :
  **symbol MUCL3, hgnc_id HGNC:21666, name « mucin like 3 »,
  status Approved, locus_group protein-coding gene,
  prev_symbol ['DPCR1'], prev_name ['diffuse panbronchiolitis
  critical region 1'], alias_symbol ['PBLT', 'bCX105N19.6',
  'C6orf37'], ensembl_gene_id ENSG00000168631, entrez_id 135656,
  location 6p21.33, date_symbol_changed 2018-03-19,
  date_name_changed 2018-03-19, refseq_accession NM_080870,
  uniprot_ids ['Q3MIW9'], omim_id ['613928'],
  date_approved_reserved 2004-02-03.**
- `https://rest.genenames.org/fetch/prev_symbol/DPCR1`
  (fichier `hgnc_prev_dpcr1_885.json`, SHA-256
  `8b6d99f7463bf57256b773c6d9fbcf4d094287bb52439e2d63982a464a62b183`,
  2 051 o, HTTP 200, XML) : **numFound = 1, un seul résultat —
  le même enregistrement (HGNC:21666, MUCL3)**. DPCR1 n'est
  donc le symbole approuvé actuel d'aucun autre gène.
- Portes R1 et R2 : PASSÉES.

### 1.2 Ensembl REST (porte R4)

- `https://rest.ensembl.org/lookup/symbol/homo_sapiens/MUCL3?content-type=application/json`
  (fichier `ensembl_mucl3_885.json`, SHA-256
  `21191898bb0a291bb78e17db7ccc706855bcea0b5f6f0d1b6307f10a5f1ebc56`,
  422 o, HTTP 200, JSON) : **id ENSG00000168631, display_name
  MUCL3, description « mucin like 3 [Source:HGNC Symbol;Acc:
  HGNC:21666] », biotype protein_coding, assembly GRCh38,
  seq_region_name 6, start 30940973, end 30954221, strand 1,
  canonical_transcript ENST00000462446.6.**
- `https://rest.ensembl.org/lookup/symbol/homo_sapiens/DPCR1?content-type=application/json`
  (fichier `ensembl_dpcr1_885.json`, SHA-256
  `3cb0e234af5c59db12642bcd763608cdf223ab6710fa0d9be8c239688f72bfc0`,
  50 o, HTTP 400, JSON) : **{"error": "No valid lookup found
  for symbol DPCR1"}** — identique au §8.79.
- Porte R4 : PASSÉE.

### 1.3 NCBI RefSeq — corroboration (porte R3)

- Page lue : NCBI RefSeq genes, curated subset, NM_080870.4,
  miroir UCSC
  `https://rloopbase.nju.edu.cn/browser/cgi-bin/hgc?hgsid=4496_QWvvN0LAoIYc1bLzAWvVQgk38RS2&db=hg38&c=chr6&l=30944375&r=30945124&o=30940972&t=30954221&g=ncbiRefSeqCurated&i=NM_080870.4`
  (lue le 21 nov. 2026 ~13h57 UTC) : **RefSeq Gene MUCL3,
  RefSeq NM_080870.4, Status Validated, Description « mucin
  like 3 », Synonyms: C6orf37,DPCR1,PBLT, OMIM 613928, Protein
  NP_543146.2, HGNC 21666, Entrez Gene 135656, Position
  chr6:30940973-30954221** — coordonnées identiques à
  l'enregistrement Ensembl MUCL3.
- Corroboration par recherche (même jour) : NCBI GeneID 135656
  = MUCL3, synonymes DPCR1/PBLT/C6orf37, HGNC:21666
  (Promega FindMyGene, page NCBI-sourcée ;
  GeneCards MUCL3 : « Prev. Symbol: DPCR1 » ; Broad GPP :
  « Gene: Human MUCL3 (135656) »). La recherche GTEx V8
  montre en outre que GTEx V8 utilise encore DPCR1 comme
  symbole pour ENSG00000168631 — confirmation indépendante
  que DPCR1 désignait ce même gène Ensembl.
- Porte R3 : PASSÉE.

### 1.4 Croisement avec les données détenues (porte R5)

- La ligne `gene_name = MUCL3` des TSV GDC porte le
  `gene_id` **ENSG00000168631.13** (Ensembl ENSG00000168631,
  version 13) dans **55/55 fichiers** — vérifié par grep
  avant construction, puis par le script de construction sur
  les 44 fichiers tumoraux (porte R5 du protocole, §6).
- DPCR1 : **0 occurrence** dans 55/55 fichiers.
- Porte R5 : PASSÉE.

**Bilan étape 1 : R1, R2, R3, R4, R5 PASSÉES — le remappage
tient. Le flux est nommé MUCL3 (ex-DPCR1) partout.**

## 2. Données : GDC ORGANOID-PANCREATIC, déjà détenues (aucun nouveau téléchargement)

- Projet GDC `ORGANOID-PANCREATIC` (Human Cancer Models
  Initiative / Next Generation Cancer Models), RNA-seq, STAR
  Counts, accès ouvert, GENCODE v36.
- Manifeste :
  `data/GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST_879.tsv`,
  SHA-256
  `f713edebf0f8afb20305b1472d480564e45ac31ce79e28350d7dde6ae496220b`
  — re-vérifié dans ce chantier, IDENTIQUE au §8.79.
  55 lignes. Source :
  `https://raw.githubusercontent.com/FindPrint/pdac-systems-evidence-preclinical/main/data/external-links/GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST.tsv`
  (§8.79).
- Les 55 TSV détenus (`data/gdc_organoid_879/`) re-vérifiés
  dans ce chantier, avant construction : **MD5 55/55 conformes
  au manifeste, SHA-256 55/55 conformes à
  `download_gdc_879_receipt.json`** (SHA-256 du reçu
  `56ba7363b2e48ed910259138a281916c8de0b2a671911b9b02f3564274e987f0`,
  reçu daté 2026-11-21T12:23:24Z, n_ok 55, total 232 648 892 o),
  **total 232 648 892 o exact**.
- En-tête vérifié par le constructeur : 9 colonnes
  (`gene_id, gene_name, gene_type, unstranded, stranded_first,
  stranded_second, tpm_unstranded, fpkm_unstranded,
  fpkm_uq_unstranded`), 60 660 lignes de gènes + 4 techniques
  STAR par fichier.
- Association fichier → échantillon (API GDC, §8.79) :
  `gdc_organoid_879_file_sample_map.tsv`, SHA-256
  `282d8b8319dbbc82279fa4bed08fcb7bc34a8fa9a6320ad3be46b443b109594a`
  — **44 fichiers Tumor** (38 cas, diagnostic
  « Adenocarcinoma, NOS » ; 3 cas multi-fichiers : 2, 3 et
  4 fichiers), **11 fichiers Normal exclus** (cas 61–71,
  diagnostic « Unknown »).
- Valeurs utilisées : colonne `tpm_unstranded` telle que
  fournie par GDC. Aucune renormalisation, aucune
  transformation log, aucune imputation.

## 3. Indépendance (grep livre blanc §8.1–§8.83, 21 nov. 2026)

« ORGANOID-PANCREATIC » 14 mentions, toutes au §8.79 (arrêt
C2 + piste ouverte (c)) ; « MUCL3 » 8 mentions, toutes au
§8.79 (remappage noté + piste ouverte) ; aucune mention dans
une autre section, aucun CSV, aucun run, aucune valeur
`maxsep` pour cette cohorte ailleurs dans le livre blanc.
La seule antériorité est la piste ouverte du §8.79.9 (c) —
et c'est elle qui autorise ce chantier. **Aucun CSV C2,
aucun run C2** n'existait avant ce chantier
(`pdac_879_gdc_organoid*` inexistant, vérifié avant le gel).
Patients distincts par construction de programme (UUID GDC /
`submitter_id` entiers vs barres TCGA, GSM GEO, ICGC) —
limite déclarée : aucun identifiant commun n'existe entre les
systèmes, donc pas de preuve par jointure ; établi par
programme, par système d'identifiants et par absence de tout
lien documenté.

## 4. Nature des lignes

- Les 55 TSV GDC sont des quantifications RNA-seq STAR
  (GENCODE v36), colonne utilisée `tpm_unstranded` (TPM du
  fournisseur, pas un calcul de ce chantier). Les 11 fichiers
  Normal n'ont pas été utilisés.
- Les 4 réponses de nomenclature (HGNC ×2, Ensembl ×2) sont
  des métadonnées de nomenclature, pas des données
  d'expression.
- Les résultats d'autres expériences cités dans la section
  (§8.79 : `d_maxsep = +0,4494` ; §8.70/§8.74 : Δρ médians)
  sont des RÉSULTATS RAPPORTÉS, repris avec leur source — pas
  des mesures de ce chantier, pas des verdicts importés.
- Le nul (graine 42, nuls frais 8851/8852) est un échantillon
  hypothétique (permutation de lignes), pas une mesure.

## 5. Construction et runs

- Constructeur `build_fluxes_885.py` (copie adaptée de
  `build_fluxes_879.py`, original intact SHA
  `c03151e882a2723bff575fb3f2deee9fed8b229447470e6e2283bdebbb3f6ac1`),
  SHA-256
  `9dc2f6678862af0065a2e3f139c2a6f5c05df8ceb2d51d6696641cfe28d30799`,
  journal `build_fluxes_885.log` (SHA
  `22d19aaaeb41d00c8a704540a78d33236ca603fb6fe8a63e521a0a24f27c2f0e`).
  Portes §6 : 10/10 OK. 44/44 cas complets, 0 NaN.
  KRAS TPM : min 11,92 / médiane 31,83 / max 165,1.
  1 233 symboles en double hors 13 utiles par fichier (1re
  ligne conservée, même comportement qu'au §8.79).
- CSV de flux :
  - réel `pdac_885_gdc_organoid_fluxes.csv`, SHA-256
    `a83b98175bdbc33525ba8a175aa898504d2cc44125b891d0902c6c6c26345eaf`
    (44 lignes + en-tête ; en-tête
    `step,PGC,REG4,CLDN18,MUC17,MUCL3,CR2,KRT20,MUC2,GSTM1,CEACAM5,CLCA1,MUC16`) ;
  - nul graine 42 `pdac_885_gdc_organoid_fluxes_nul.csv`, SHA-256
    `c3f8399cb423d7691136ed25860567186fb5e94e383283ddc081f83916bed12e` ;
  - nul frais s8851, SHA-256
    `a6fd59ed651ab3bd3bb58e4f9587322f239ae622abbdb7b19e666aec8d114ccd` ;
  - nul frais s8852, SHA-256
    `3801a71972c5e21c97c294b21352cc653a77e929aeea065acbec86a041185032`.
- Runs v6.2 mode fast, lanceur `run_v62_lot.sh` (reprenable,
  SKIP des sorties complètes), unités systemd `v62-885`
  et `v62-885frais` (jamais nohup) :
  - manifeste `manifest_v62_885.txt` (SHA
    `1aebd9a83397f2a436b841030a88acc867bdc8158be84b7d181bce64b8a8a205`),
    journal `runs_v62_885.log` (SHA
    `7573ebfa5e6672787b1747b2cdbe8d26d03605e03bf061aceeae737363abb848`),
    FIN 2026-11-21T14:04:35Z, **2/2 exit 0** ;
  - manifeste frais `manifest_v62_885_frais.txt` (SHA
    `8553743adc459da385fe5d7a95e4cbfca380172e0fad81d655055442109285a9`),
    journal `runs_v62_885_frais.log` (SHA
    `733dd20114a0ade5bbe3cb3c65dd0a5db1dfef9873c189c6b92e85e163960741`),
    FIN 2026-11-21T14:14:19Z, **2/2 exit 0**.
  - **Total : 4 runs, 4/4 exit 0.** Version lue sur les 4 runs :
    `v6.2.0-L7aL7b-CohenD-short`.
- Extraction `extract_885.py` (SHA
  `1742a3142f898ada85e537fb54e4f468f418d3f348aa4dba1ff6dc6b3d75dee0`,
  réutilise `extract()` de `extract_858.py`, original intact),
  sorties `extract_885.json` (SHA
  `bc1147b08547bba1d075af81f40a317d783712f02bf72bad9fe10e94adda2394`)
  et `extract_885.csv` (SHA
  `f3a411b92eb26548435e5247ed0dfbc75853010a3ae5ccb1193e2548b55edd14`),
  journal `extract_885.log` (SHA
  `d0362a3433eaa2e8b6e3cba127aa4fc48af332305f103c007c197f231ac96f39`).
- Vérification indépendante `verify_885.py` (SHA
  `c7b0977db30d951c68b75d2357a7cc3e7698157687f8d23521cbe31ce57e1f65`,
  relecture directe des `master_results.json` par `json.load`,
  chemin distinct) : **4/4 runs, écart max 0,0, verdict OK**,
  sortie `maxsep_885_verify.json` (SHA
  `7487e5019bae13b01e817ccad4d93a3f4a06577cd9082edc01a1cb4f58829768`),
  journal `verify_885.log` (SHA
  `d09257f5443fbda0f2939834eec94c5bf42aa66c80f0d7cfd5c7782387adc027`).
  Second calcul indépendant des écarts `d_maxsep` depuis les
  `master_results.json` : +0,0884 / +0,0376 / +0,0936,
  identiques à l'extraction (écart < 1e-15, arrondi à 4
  décimales identique).
- Tests directs `direct_tests_885.py` (SHA
  `67878fa004428ca219b4e8e2b28afec96b361c0e113ef7dd3a4ad989f102288d`),
  sortie `direct_tests_885.json` (SHA
  `ab2323b3ffbfdc81cc3bbbe864b14c7027aa5d1e6a6366b3bc5c6a5b8e5b4300`),
  journal `direct_tests_885.log` (SHA
  `77678556e209709862cb8d19dfdc35503b767120303ab9decb0098b1d20ad60b`).

## 6. Ce qui manque / limites

- Le remappage repose sur la nomenclature (HGNC/Ensembl/NCBI)
  : MUCL3 est le symbole actuel du même gène — la mesure est
  la même ligne, mais le nom du flux a changé en 2018
  (`date_symbol_changed` 2018-03-19). Toute lecture future qui
  écrirait « DPCR1 » sans « MUCL3 (ex-DPCR1) » serait fausse.
- Indépendance établie par programme et système
  d'identifiants, pas par jointure (§3, limite déclarée).
- 3 cas multi-fichiers (2, 3 et 4 fichiers tumoraux, 9 lignes
  sur 44) : dépendance partielle déclarée, unité = fichier
  (comme au §8.79) ; l'agrégation par cas donnerait n = 38,
  sous le minimum fast (40).
- Les réponses API GDC (cas/fichiers, §8.79) restent en
  scratch `/tmp/b879/` (éphémère) ; seule la table
  d'association figée est versionnée dans le chantier.
- Les fichiers bruts de nomenclature HGNC sont en XML
  (le REST HGNC répond en XML par défaut) ; les champs cités
  ont été extraits par parseur XML et recoupés avec la lecture
  navigateur de la même URL.
- La section §8.85 (`section_8.85_gdc_mucl3.md`) est le
  livrable de ce chantier ; son SHA est calculé après
  écriture (auto-référence impossible dans ce fichier).

## 7. Fichiers produits par ce chantier (à hasher après écriture)

- `~/workspace/runs/pdac-v6/section_8.85_gdc_mucl3.md`
- `~/workspace/runs/pdac-v6/PROTOCOL_gdc_mucl3_885.md`
- `~/workspace/runs/pdac-v6/PROVENANCE_885.md` (ce fichier)
- `~/workspace/runs/pdac-v6/hgnc_mucl3_885.json`,
  `hgnc_prev_dpcr1_885.json`, `ensembl_mucl3_885.json`,
  `ensembl_dpcr1_885.json`
- `~/workspace/runs/pdac-v6/build_fluxes_885.py`,
  `build_fluxes_885.log`, `pdac_885_gdc_organoid_fluxes*.csv`
  (réel, nul s42, nuls frais s8851/s8852)
- `~/workspace/runs/pdac-v6/manifest_v62_885.txt`,
  `manifest_v62_885_frais.txt`, `runs_v62_885.log`,
  `runs_v62_885_frais.log`,
  `results_fast_v62_885_gdc_organoid*` (4 dossiers)
- `~/workspace/runs/pdac-v6/extract_885.py`,
  `extract_885.json` / `.csv`, `extract_885.log`,
  `verify_885.py`, `maxsep_885_verify.json`, `verify_885.log`,
  `direct_tests_885.py`, `direct_tests_885.json`,
  `direct_tests_885.log`
- Données réutilisées du §8.79 (non re-téléchargées) :
  `data/gdc_organoid_879/` (55 TSV),
  `data/GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST_879.tsv`,
  `gdc_organoid_879_file_sample_map.tsv`,
  `download_gdc_879_receipt.json`
