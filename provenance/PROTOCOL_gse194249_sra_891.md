# PROTOCOLE GELÉ — §8.91 : re-dérivation de GSE194249 depuis les lectures brutes (SRA) — suite (d2) du §8.86.4

Date : 21 novembre 2026, ~11h10 EST. Chantier §8.91, piste 1 du lot du
21 nov. 2026. Go de Zackary : 21 nov. 2026, 11h09 (« Allez s'y »).
Protocole gelé AVANT toute tentative de téléchargement de lectures
brutes et avant tout run. Aucun paramètre ne change après les
résultats. Le livre blanc N'EST PAS édité, le PDF N'EST PAS régénéré,
rien n'est poussé sur GitHub dans ce chantier (convention des
chantiers ; fusion par le coordinateur, après le finisseur §8.90).
La section §8.91 est écrite dans un FICHIER SÉPARÉ
(`section_8.91_gse194249_sra.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié ; v6.1
`2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`).
Chemin : `/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`.

Note d'honnêteté sur l'ordre des opérations : les vérifications
d'ACCÈS aux lectures brutes (§2 — E-utilities NCBI, ENA, fiches
BioProject) sont des vérifications de métadonnées, pas des données
d'expression ; elles ont été effectuées le 21 nov. 2026 ~11h10–11h30
EST comme travail pré-gel de repérage de la source exacte, selon le
même geste que le §8.86 §2 (métadonnées avant le gel). Aucune lecture
brute n'a été téléchargée, aucun fichier d'expression n'a été lu,
aucun run n'a été lancé avant ce gel. Le présent protocole gèle les
portes et le critère de verdict ; la section §8.91 applique ces portes
aux faits du §2.

## 0. Contexte décisionnel — à lire avant tout le reste

- §8.86 : GSE194249 (84 PDPCOs, Shi et al., Nat. Commun. 2022, 13:2169,
  DOI 10.1038/s41467-022-29857-6) **INUTILISABLE comme paire à 12 flux**
  — DPCR1 absent de la matrice FPKM déposée (0/15 609 lignes),
  MUCL3 également absent, **0 run, 0 CSV**. Piste fermée comme paire
  à 12 flux, avec deux suites nommées au §8.86.4 (d) : (d1) paire à
  11 flux, (d2) re-dérivation depuis les lectures brutes (SRA) avec
  une annotation actuelle, « qui serait un autre produit de données,
  pas la matrice déposée ».
- §8.88 : la suite (d1) est faite — paire à 11 flux, **NON**
  (`d_maxsep −0,0239`, 15e paire) ; **A2 10/15, 12/15 positifs**,
  LOO 9/14. **C3 reste LEVÉE** (depuis §8.71 ; décision de Zackary,
  20 nov. 13h04, adoption pleine de `maxsep`).
- **Le présent chantier EST la suite (d2).** Il ne rouvre ni C3, ni
  les §8.86/§8.88, ni aucune décision de Zackary. Son seul objet :
  dire si une matrice à 12 flux peut être re-dérivée depuis les
  lectures brutes, et si oui la construire et la courir ; sinon,
  fermer la piste avec la raison exacte.
- Méthodes de l'article (§8.86.5) : TopHat sur hg19, FPKM par
  Cufflinks, filtre FPKM < 1 dans les 87 échantillons, 15 819 gènes
  protéiques annoncés contre 15 609 déposés (écart 210, non élucidé).

## 1. Les 15 paires principales indépendantes déjà comptées

Valeurs reprises des §8.56/§8.69/§8.70/§8.71/§8.74/§8.79/§8.85/
§8.88, jamais recalculées. Écart = maxsep réel − maxsep nul.
Plancher 0,07. Bilan : **10/15 au-dessus du plancher, 12/15
positifs**, LOO 9/14. (Table complète au §8.88.1 ; reprise telle
quelle ici par référence.)

## 2. Ce qui est déjà connu sur l'accès aux lectures brutes avant le gel (vérifications de métadonnées seulement)

### 2.1 BioProject PRJNA799993 (transcriptome) — via E-utilities esummary, 21 nov. 2026

Fiche conservée `gse194249_bioproject_891.json`, SHA-256
`e5a85000f939c6a88d59f546624dc851ecdbb12e4afbe6759435d0ce76b0e455`
(métadonnées, pas des données d'expression) :

- Accession **PRJNA799993**, titre identique à l'article, organisme
  *Homo sapiens*, enregistrement 2022/01/24, soumissionnaire
  « Center for Excellence in Molecular Cell Science, CAS ».
- Description, phrase décisive, citée verbatim : **« Raw data are
  not available for this Series due to human genetic resources
  policy in China. »** (« Les données brutes ne sont pas
  disponibles pour cette série en raison de la politique chinoise
  sur les ressources génétiques humaines. »)
- La description confirme par ailleurs le protocole RNA-seq :
  ARN total de 84 PDPCOs + 3 NPOs, kit NEBNext Ultra RNA Library
  Prep, paires d'extrémités, Illumina HiSeq X Ten, TopHat sur hg19,
  FPKM par Cufflinks, filtre FPKM < 1, 15 819 gènes protéiques.

### 2.2 BioProject PRJNA801501 (même étude, second volet) — via E-utilities esummary, 21 nov. 2026

Même fichier `gse194249_bioproject_891.json` (SHA ci-dessus) :

- Accession **PRJNA801501**, même titre, type « Epigenomics |
  Genome » (volet ATAC-seq / WGS de la même étude).
- Description, phrase décisive, citée verbatim : **« Please note
  that the raw data has been uploaded to a domestic repository
  National Omics Data Encyclopedia (NODE;
  https://www.biosino.org/node/index) with controlled access
  mechanisms under accession number OEP001744. »** (« Veuillez
  noter que les données brutes ont été téléversées vers un dépôt
  national, la National Omics Data Encyclopedia (NODE), avec des
  mécanismes d'accès contrôlé, sous le numéro d'accession
  OEP001744. »)
- La matrice transcriptomique est « represented in GEO under
  GSE194249 » — c'est la matrice FPKM déjà couverte aux §8.86/§8.88.

### 2.3 SRA — 0 expérience (E-utilities esearch, 21 nov. 2026)

- `esearch db=sra term=PRJNA799993` : **count 0**.
  Reçu `sra_esearch_PRJNA799993_891.json`, SHA
  `a6df6133df098ed299a26cdc05ba79c745f440dd83063a796d63602403b18155`.
- `esearch db=sra term=PRJNA801501` : **count 0**.
  Reçu `sra_esearch_PRJNA801501_891.json`, SHA
  `014a217cd4fb85bab77d0d46d4546903d7c5d344700da3de72d5b3a8e9abb7c2`.
- `elink dbfrom=gds db=sra id=200194249` (GSE194249 → SRA) :
  **aucun lien** (linksets sans `linksetdbs`).
  Reçu `elink_gds_sra_891.json`, SHA
  `e7498743d2ce11d1356af7ee0d4d4faacc55f322823d150ab2d74bd62d2f87c5`.
- `esearch db=sra term=GSE194249` : **count 0** (vérifié avant le
  gel, même jour).

### 2.4 ENA (miroir européen de l'INSDC) — 0 run

- Requête portail ENA `result=read_run`,
  `query=study_accession=PRJNA799993` : **liste vide `[]`**.
  Reçu `ena_readrun_PRJNA799993_891.json`, SHA
  `2ba33ca0557f1bb5b7ba88d67f9d0093c7185a36ec51fe2b7bd9372d3e001d6d`.
- L'étude existe dans ENA comme métadonnée (fiche
  `study_accession=PRJNA799993`, même titre), sans aucun run —
  cohérent avec l'absence SRA : les lectures n'ont jamais été
  versées dans l'INSDC (SRA/ENA/DDBJ).

### 2.5 NODE OEP001744 — accès contrôlé, page non lisible directement

- Page projet NODE `https://www.biosino.org/node/project/detail/OEP001744`
  consultée le 21 nov. 2026 : HTTP 200 mais contenu de 906 octets
  (coquille d'application JavaScript, pas de fiche lisible sans
  session). Recherche web exacte `"OEP001744" NODE biosino` :
  **aucun résultat utilisable** (le dépôt NODE n'est pas indexé
  par les moteurs généralistes).
- Ce qui est établi ne dépend pas de cette page : la fiche
  BioProject PRJNA801501 (§2.2) dit elle-même « controlled access
  mechanisms » pour OEP001744. Aucune demande d'accès n'a été
  faite dans ce chantier (hors périmètre, §5).

### 2.6 Outillage local — contexte, pas motif de clôture

- Aucun outil de quantification installé sur la machine :
  `salmon`, `kallisto`, `samtools`, `STAR`, `hisat2`,
  `fasterq-dump`, `prefetch` absents ; `pysradb` absent.
  Disque : 121 Go libres sous `/home/hatch`.
- Ces faits ne décident rien : la piste se ferme sur l'ACCÈS
  (§2.1–§2.4), pas sur l'outillage. Ils sont consignés pour que
  toute reprise future sache d'où repartir.

## 3. Arrêt borné — AUCUNE tentative de contournement

**Une seule question dans ce chantier : les lectures brutes
RNA-seq de GSE194249 sont-elles accessibles en libre accès ?**
Si la porte G1 (§4) échoue, le chantier s'arrête sur un blocage
documenté : section §8.91 écrite quand même, avec les tentatives
chiffrées, aucune valeur inventée, et la piste **fermée**. Il n'y a
PAS de : demande d'accès contrôlé (NODE), contact des auteurs,
substitution d'une autre cohorte, substitution d'un autre gène,
ni construction d'une matrice à partir d'autre chose que les
lectures brutes de cette série. Chacun de ces gestes demanderait
un go explicite de Zackary et son propre protocole.

## 4. Portes d'acceptation (gelées)

- **G1 — Accès libre aux lectures brutes.** Au moins un run
  RNA-seq ouvertement téléchargeable par échantillon (84 PDPCOs
  + 3 NPOs attendus) dans SRA, ENA, ou un miroir ouvert
  équivalent. **ÉCHEC CONSTATÉ AVANT LE GEL (§2) : 0 run SRA,
  0 run ENA, aucun lien GEO→SRA, et les fiches BioProject
  déclarent les données brutes indisponibles (politique chinoise)
  ou sous accès contrôlé (NODE OEP001744).** La porte dit ARRÊT.
- **G2 — Effectif.** n ≥ 40 échantillons PDPCO après contrôle
  qualité. Non évaluable (G1 échouée).
- **G3 — Couverture des 12 gènes v4.** Sous annotation actuelle,
  DPCR1 et/ou MUCL3 (symbole actuel, `prev_symbol` DPCR1,
  HGNC:21666) comptés comme symboles distincts, sans fusion
  arbitraire ; les 12 gènes v4 doivent être quantifiables.
  Non évaluable (G1 échouée).
- **G4 — Méthode de quantification (nommée, non exécutée).**
  Si G1 avait passé : Salmon (ou kallisto) sur transcriptome
  GENCODE actuel (GRCh38), comptages au niveau gène, TPM,
  construction des flux identique aux paires V1 (ordre KRAS
  croissant, `step` = rang, valeurs telles que quantifiées, aucune
  renormalisation ajoutée, aucune transformation log, aucune
  imputation, cas complets seulement, nul par permutation des
  lignes graine 42). Version exacte de l'outil et de GENCODE
  gelées au moment de l'exécution — qui n'a pas lieu.

## 5. Critère de verdict — GELÉ avant tout téléchargement et tout run

- **PISTE FERMÉE (INUTILISABLE comme re-dérivation)** : si G1
  échoue — c'est le cas constaté (§2). **0 téléchargement de
  lectures brutes, 0 CSV de flux, 0 run v6.2.** La question
  « DPCR1/MUCL3 sont-ils quantifiables depuis les lectures
  brutes ? » reste **sans réponse** : elle exige les lectures,
  qui ne sont pas accessibles.
- **CONFIRME / PARTIEL / NON** (mêmes définitions que §8.86 §7,
  plancher `d_maxsep > 0,07`, paire comptée comme 16e paire
  principale indépendante, A2 recalculé sur 16 paires) : seulement
  si G1–G4 passent et qu'une matrice à 12 flux est construite et
  vérifiée (SHA, n, provenance). Non applicable ici.
- **A2 inchangé : 10/15 au-dessus du plancher, 12/15 positifs,
  LOO 9/14.** C3 reste LEVÉE dans tous les cas.

## 6. Ce qui débloquerait la piste (nommé, non entrepris)

- Une demande d'accès contrôlé auprès de NODE
  (https://www.biosino.org/node/index, projet OEP001744), dans le
  cadre de la politique chinoise sur les ressources génétiques
  humaines — demande formelle, identité institutionnelle,
  justification, délai inconnu, issue incertaine. **Aucune demande
  faite dans ce chantier ; aucune ne sera faite sans go explicite
  de Zackary.** Une telle demande est un geste administratif et
  juridique, pas un calcul.
- Ou une republication ouverte des lectures par les auteurs ou
  par un tiers autorisé (aucune connue au 21 nov. 2026).

## 7. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et le
  jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict : seul l'écart `maxsep` mesuré sur les runs du chantier
  fait un verdict de paire — ici il n'y a pas de runs, donc pas de
  verdict de paire, seulement un verdict d'accès.
- Un nul qui invalide une piste est un résultat ; un échec d'accès
  est un verdict, pas un échec caché.
- Ne jamais présenter une lecture préliminaire comme un verdict.
- Aucun consensus exigé entre flux ou contrôles ; aucune
  affirmation clinique — l'étude porte sur l'instrument.
- Provenance toujours nommée : source, auteur, date, dépôt, URL,
  SHA-256 de chaque reçu.

## 8. Livrables

- Ce protocole (gelé avant toute tentative de téléchargement et
  tout run).
- `PROVENANCE_891.md` (sources, URLs, SHA-256 des reçus,
  citations verbatim des fiches BioProject, outillage, disque).
- Reçus : `gse194249_bioproject_891.json` (SHA `e5a85000…0e455`),
  `sra_esearch_PRJNA799993_891.json` (SHA `a6df6133…18155`),
  `sra_esearch_PRJNA801501_891.json` (SHA `014a217c…b7c2`),
  `ena_readrun_PRJNA799993_891.json` (SHA `2ba33ca0…01d6d`),
  `elink_gds_sra_891.json` (SHA `e7498743…2f87c5`).
- §8.91 dans le FICHIER SÉPARÉ `section_8.91_gse194249_sra.md`
  (verdict d'abord, une phrase : PISTE FERMÉE ; faits ensuite ;
  détail complet après ; provenance nommée partout ; A2 inchangé
  dit explicitement).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin du protocole gelé §8.91. —
