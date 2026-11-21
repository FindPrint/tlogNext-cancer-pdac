# PROVENANCE_886 — Ré-audit GSE194249 (§8.86)

**Date :** 21 novembre 2026, ~14h00–14h10 EST.
**Agent :** TagPrint (subagent, piste B, §8.86).
**Protocole gelé :** `PROTOCOL_gse194249_886.md`, SHA-256
`b620238b9b5087c0167b975747b39cd0eb89dce9d5f99e169d58359887c9b1cf`
(gelé AVANT tout téléchargement de données d'expression).
**Pipeline :** v6.2, SHA
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
vérifié avant les travaux, inchangé — **aucun run lancé** (arrêt à
la porte « 12 gènes v4 », §3 du protocole).
**Livre blanc :** non édité. PDF non régénéré. Rien poussé sur GitHub.

## 1. Source des données

- **Série :** GSE194249, NCBI GEO.
- **Article :** Shi X, Li Y, Yuan Q, Tang S, Guo S, et al.
  « Integrated profiling of human pancreatic cancer organoids
  reveals chromatin accessibility features associated with drug
  sensitivity », *Nature Communications* 2022, 13:2169.
  DOI 10.1038/s41467-022-29857-6 (CC BY 4.0).
  URL : https://www.nature.com/articles/s41467-022-29857-6
  (PDF : https://www.nature.com/articles/s41467-022-29857-6.pdf).
  Affiliations : Changhai Hospital, Second Military Medical
  University (Naval Medical University), Shanghai, Chine ;
  Shanghai Institute of Biochemistry and Cell Biology, Chinese
  Academy of Sciences, Shanghai, Chine ; et autres (voir
  l'article, p. 1).
- **Page GEO :** https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE194249
  (accès direct bloqué par reCAPTCHA le 21 nov. 2026 — les
  métadonnées viennent de l'API E-utilities, voir §2).
- **Fichier téléchargé (unique source d'expression) :**
  `GSE194249_PDPCOs_FPKM.txt.gz`, URL
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194249/suppl/GSE194249_PDPCOs_FPKM.txt.gz`
  (miroir HTTPS du FTP GEO, 1re tentative, 21 nov. 2026).
- **Fichier local :** `data/GSE194249_PDPCOs_FPKM.txt.gz`,
  4 927 876 o, SHA-256
  `479517fbed1d8f5bb9d141b6b932b6ab56ba2ba72d4394d13aea2a3da0a50f27`,
  gzip intègre. Reçu : `download_gse194249_886_receipt.json`,
  SHA `fd9bd625a3869086d06b11bb4896b5e5de7f05da91bf5867bca8d1bf83a016ea`.
  Script de téléchargement : `download_gse194249_886.py`, SHA
  `d0e1be23c34ea85a4661ffe6a7ecddf551372d2d0def08caf821a955254c4cc1`.
- **Aucun SHA attendu pré-connu :** GEO ne publie pas de SHA
  pour ce fichier ; la vérification est l'intégrité gzip + les
  comptages (voir §4).

## 2. Métadonnées pré-gel (aucune donnée d'expression lue)

- **NCBI E-utilities, esummary GDS** (`db=gds&id=200194249`,
  21 nov. 2026), réponse conservée
  `gse194249_esummary_886.json`, SHA-256
  `73934e46a717a5db1ed8cd8e1c4349435683a0eed1dda85fe7b097ec448f460e` :
  titre, accession GSE194249, plateforme GPL31265, dépôt
  2022/02/23, *Homo sapiens*, « Expression profiling by high
  throughput sequencing », fichier supplémentaire de type TXT,
  **87 échantillons** : 75 `CAS-DAC-*`, 4 `CAS-NEN-*`,
  4 `CAS-IPMN-*`, 1 `CAS-ACC-1`, 3 `NPC-*`.
- **Article (résumé et méthodes, lus le 21 nov. 2026) :**
  84 lignées PDPCO (75 PDAC, 4 IPMN, 1 ACC, 4 NEN) + 6 NPO
  établis ; échantillons prélevés par chirurgie ou biopsie
  EUS-FNA. Méthodes RNA-seq : lectures mappées sur hg19 par
  TopHat ; FPKM par Cufflinks ; « Genes with FPKM values <1 in
  all 87 samples were filtered out. Finally, 15,819
  protein-coding genes remained for further analysis. »
  (p. 12 des méthodes). Les 87 échantillons du filtre sont
  les 84 PDPCOs + 3 NPOs — le même décompte que GEO.
- **Livre blanc (§8.78, C4 ; §8.79.9 (d)) :** GSE194249 nommée
  uniquement comme candidate à vérifier ; « PDPCO » :
  6 occurrences, toutes au §8.78 ; « CAS-DAC » : 0 ; jamais
  courue, jamais tenue comme holdout, aucune valeur `maxsep`.
- **Script d'audit antérieur :**
  `universal-log-research/pancréas/ANALYSE_THERAPEUTIQUE_2026-11-19/audit_GSE194249_candidate.py`,
  SHA `ae3c85cdec3da83c8877bebde1037e284df4a911` (cité au §8.78 ;
  sa sortie `candidate_GSE194249_sources/` est absente du dépôt
  — le présent chantier est l'audit refait depuis GEO, pas une
  relecture de ce script).

## 3. Nature des lignes

- La matrice téléchargée est un **fichier déposé par les auteurs**
  (FPKM Cufflinks, hg19, filtré FPKM < 1) : ce sont des valeurs
  mesurées, transformées par le pipeline des auteurs (mapping +
  quantification + filtre), pas des mesures brutes de ce chantier.
- Les comptages de ce chantier (lignes, colonnes, présence des
  gènes) sont des **vérifications** sur le fichier déposé, pas des
  mesures biologiques.
- Aucune valeur biologique n'a été mesurée ici, aucun run
  pipeline lancé, aucun CSV de flux construit : l'arrêt est un
  verdict de construction, pas un échec caché.
- Les résultats de l'article (sous-types, pics ATAC, signature de
  sensibilité, mutations KRAS 96 %, etc.) sont des RÉSULTATS
  RAPPORTÉS par leurs auteurs, repris avec leur source — pas des
  mesures de ce chantier, pas des verdicts importés.

## 4. Vérifications effectuées (chiffres, deux chemins indépendants)

- Fichier : 15 610 lignes (en-tête + 15 609 lignes de gènes),
  88 colonnes (`GeneSymbol` + 87 échantillons) — mise en page
  (A) du protocole. En-tête : `GeneSymbol, CAS-DAC-1,
  CAS-IPMN-1, CAS-DAC-11, …`, dernière colonne `NPC-7`.
- Colonnes : les 87 titres correspondent EXACTEMENT aux
  87 échantillons de l'esummary (0 inattendu, 0 manquant).
  Normaux `NPC-4`, `NPC-5`, `NPC-7` : 3 colonnes, à exclure
  selon le protocole (exclusion non exécutée — l'arrêt a eu
  lieu avant toute construction) ; PDPCOs : 84.
- Symboles dupliqués : 0 ligne. Gènes uniques : 15 609.
- **Présence des 13 gènes utiles (symbole exact, une ligne
  chacun) :** PGC 1, REG4 1, CLDN18 1, MUC17 1, **DPCR1 0**,
  CR2 1, KRT20 1, MUC2 1, GSTM1 1, CEACAM5 1, CLCA1 1,
  MUC16 1, KRAS 1. **MUCL3 (descriptif) : 0.**
- **Second calcul indépendant (grep sur le fichier brut) :**
  `DPCR1` exact : 0 occurrence dans tout le fichier ;
  insensible à la casse : 0 ; `MUCL3` : 0 ; aucun symbole
  contenant `DPCR`. Symboles `MUC*` présents : MUC1, MUC12,
  MUC13, MUC16, MUC17, MUC2, MUC20, MUC3A, MUC4, MUC5B,
  MUC6, MUC7.
- Script de construction : `build_fluxes_886.py`, SHA
  `04965dd4367b6e0709d679629b681e4a7e8808b21426d99dccee360731b79c52` ;
  audit : `build_fluxes_886_audit.json`, SHA
  `60eeb3c73860f92bd180f7a9fbd4e25522de1fe8d798c8543f0272e6320b440a`.
  Le script s'est arrêté à la porte « 12 gènes v4 présents »
  (§3 du protocole) : **aucun CSV de flux, aucun run, aucun
  manifeste, aucun journal de lot, aucun extracteur, aucun test
  direct** — confirmé par l'absence des fichiers
  `pdac_886_*`, `results_fast_v62_886_*`, `manifest_v62_886.txt`,
  `runs_v62_886.log`, `extract_886.*`, `verify_886.py`,
  `direct_tests_886.py` (21 nov. 2026).

## 5. Indépendance

- Jamais courue dans ce projet (grep livre blanc §8.1–§8.83).
- Patients distincts par construction de programme : biobanque
  PDPCO de Shanghai (Changhai Hospital, Second Military Medical
  University), chirurgie ou EUS-FNA, identifiants `CAS-*` /
  `NPC-*` — sans recouvrement possible par jointure avec les
  cohortes tenues (barres TCGA, GSM GEO des autres séries,
  ICGC). Aucun lien documenté avec TCGA PAAD, ICGC PACA-AU,
  GSE71729, GSE62452, GSE62165, GSE21501, GSE79668, GSE60979,
  GSE131050, GSE57495, ni avec les organoïdes GDC HCMI (§8.79),
  ni avec les PDO de Chen et al. 2025 (46 PDO, autre article),
  ni avec Tiriac et al. 2018 (CSHL).
- **Limite déclarée :** aucun identifiant commun n'existe entre
  les systèmes, donc le non-recouvrement est établi par
  programme, par système d'identifiants et par absence de tout
  lien documenté — c'est une limite, pas une preuve formelle
  (même caveat que §8.79 §2.2 point 2).
- L'indépendance ne change rien au verdict : la cohorte est
  indépendante mais INUTILISABLE comme paire à 12 flux — les
  deux constats sont séparés.

## 6. Ce qui manque / limites

- **Cause exacte de l'absence de DPCR1 non établie :** le gène
  n'est dans le fichier déposé sous aucun des deux symboles
  (DPCR1 : 0 ; MUCL3 : 0). Compatible avec le filtre des
  auteurs (FPKM < 1 dans les 87 échantillons, Méthodes p. 12),
  mais les valeurs FPKM par gène de DPCR1/MUCL3 ne sont pas
  dans le fichier déposé — le filtre ne peut pas être vérifié
  gène par gène. L'absence est un fait du fichier déposé ; sa
  cause exacte reste une hypothèse.
- **Écart 15 609 / 15 819 :** les Méthodes annoncent 15 819
  gènes protéiques restants après filtre ; la matrice déposée
  en compte 15 609 — écart de 210 gènes, non élucidé (version
  du dépôt, annotation, ou autre — non tranché ici).
- Les suppléments de réponse aux médicaments (Suppl. Data 8,
  MOESM11) et de suivi clinique (Suppl. Data 10, MOESM13) n'ont
  PAS été téléchargés (hors périmètre de la paire, §4.1 du
  protocole) ; le n de réponse exact reste donc non vérifié,
  comme au §8.78.
- Les 6 NPOs établis par l'article ne sont que 3 dans GEO
  (`NPC-4/5/7`) — les 3 autres ne sont pas dans la série
  déposée ; sans objet ici (normaux exclus de toute façon).
- La page GEO directe n'a pas pu être lue (reCAPTCHA) ;
  les métadonnées GEO viennent de l'API E-utilities, dont la
  réponse est conservée et hashée (§2).

## 7. Fichiers du chantier

- `PROTOCOL_gse194249_886.md` — SHA `b620238b…1cf`.
- `PROVENANCE_886.md` — ce fichier.
- `download_gse194249_886.py` — SHA `d0e1be23…c1`.
- `download_gse194249_886_receipt.json` — SHA `fd9bd625…ea`.
- `gse194249_esummary_886.json` — SHA `73934e46…0e`.
- `build_fluxes_886.py` — SHA `04965dd4…52`.
- `build_fluxes_886_audit.json` — SHA `60eeb3c7…0a`.
- `data/GSE194249_PDPCOs_FPKM.txt.gz` — SHA `479517fb…27`.
- `section_8.86_gse194249.md` — section (verdict : INUTILISABLE).
- **Absents (par l'arrêt §3) :** `pdac_886_*`, `results_fast_v62_886_*`,
  `manifest_v62_886.txt`, `runs_v62_886.log`, `extract_886.*`,
  `verify_886.py`, `direct_tests_886.py`.

— Fin de la PROVENANCE_886. —
