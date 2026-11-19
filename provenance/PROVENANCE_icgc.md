# PROVENANCE — ICGC PACA-AU, 4e cohorte (16 nov. 2026)

## Question
Tester une 4e fois le résultat robuste « le groupe KRAS-le-plus-fort a CA125
(MUC16) et CEA (CEACAM5) élevés » et une 2e fois la survie (KRAS et CA125
prédisent une survie plus courte sans seuil, en TCGA).

## Sources et accès — ce qui a été essayé, dans l'ordre

### 1. Portail ICGC DCC — HORS SERVICE (vérifié 16 nov. 2026)
- URL tentée : `https://dcc.icgc.org/api/v1/download?fn=/current/Projects/PACA-AU/donor.PACA-AU.tsv.gz`
  et `.../exp_seq.PACA-AU.tsv.gz`, puis `/release_28/` et `/release_29/`.
- Résultat : HTTP 301 puis 200 vers `https://dcc.icgc.org/index.html` (page HTML,
  2 733 octets). L'API `/api/v1/download` et `/api/v1/releases` ne servent plus
  de fichiers : le portail DCC est décommissionné. Le patron d'URL est confirmé
  par la littérature (ICGCtoolsR, gist mschubert) mais ne fonctionne plus.
- Conséquence : les fichiers `donor.PACA-AU.tsv.gz` / `exp_seq.PACA-AU.tsv.gz`
  (avec `donor_survival_time`, `donor_vital_status`) n'ont PAS pu être
  téléchargés à la source. Ils sont remplacés ci-dessous par deux sources
  vérifiées qui portent les MÊMES patients (Bailey et al. 2016).

### 2. Expression — UCSC Xena, hub ICGC (miroir vérifié)
- Table de référence : `XenaData` du paquet UCSCXenaTools
  (https://raw.githubusercontent.com/ShixiangWang/UCSCXenaTools/master/data/XenaData.rda,
  2 314 jeux), lue avec pyreadr.
- Jeu : `PACA-AU/nature16965-s2_normalised_exp.txt`, cohorte PACA-AU,
  96 échantillons, gene expression, log2(cpm), version 2016-09-09,
  citation : Bailey et al., Nature 531, 47-52 (2016), doi:10.1038/nature16965.
- Téléchargement : le hub `https://icgc.xenahubs.net/download/...` redirige
  (302) vers le bucket S3 `icgc-xena-hub` ; l'objet non-gzippé renvoie 403,
  l'objet `.gz` existe :
  `https://icgc-xena-hub.s3.amazonaws.com/download/PACA-AU/nature16965-s2_normalised_exp.txt.gz`
- Fichier local : `data/icgc_pacaau_exp.txt.gz`
  - Taille exacte : 9 841 881 octets
  - SHA-256 : `c2cb57af3ba4c3d7fdac292e66c81067d36e16aae9efdd8005147e20820f49fa`
  - Contenu vérifié : 18 278 gènes (Ensembl) x 96 échantillons (ICGC_0006…),
    valeurs log2(cpm), 0 valeur manquante.
- Mapping gènes : probe map Xena
  `PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp`
  - Fichier local : `data/icgc_pacaau_probemap.gz`
  - Taille : 353 314 octets
  - SHA-256 : `b09a746f6084215beea3632b72e87834ea577d18fcb52add3641de5d0d975537`
  - 18 108 ENSG -> 18 077 symboles ; médiane par symbole en cas de duplicata.
  - Les 13 gènes (12 flux + KRAS) mappent chacun à un seul ENSG.
- Sous-types : `PACA-AU/nature16965-s2_NMF_class_assignment.txt`
  - Fichier local : `data/icgc_pacaau_nmf.txt.gz`
  - Taille : 447 octets
  - SHA-256 : `f1e84b997c24903c216fbe9806c1b048cd9f552894e018ca54d02b5413921e2f`
  - 96 échantillons : Pancreatic Progenitor 30, Squamous 25, Immunogenic 25, ADEX 16.

### 3. Clinique et survie — Bailey et al. 2016, Supplementary Tables 1-13
- Source : Nature, article nature16965, fichier MOESM270
  `https://static-content.springer.com/esm/art%3A10.1038%2Fnature16965/MediaObjects/41586_2016_BFnature16965_MOESM270_ESM.xlsx`
  (« This file contains Supplementary Tables 1-13 », XLSX 21 586 ko).
- Fichier local : `data/bailey2016_suppl_tables1-13.xlsx`
  - Taille exacte : 22 104 569 octets
  - SHA-256 : `778224b36343c6c65b6df49b0149219ba2038cbdec2333b96e4e8798ff74258a`
  - Feuille utilisée : 'Supp Table 1 Clinical' (458 patients, 24 colonnes).
  - Colonnes de survie : `Status` + `Length of Follow Up (months)`.
  - Statuts : Deceased - Of Disease 246, Alive - Without Disease 65,
    Alive - With Disease 50, Unknown 36, Alive - Disease Status Unknown 25,
    Deceased - Of Other Cause 23, Deceased - Of Unknown Cause 5,
    Not documented 4, Lost to Follow Up 2 (sur 458).
- Autres sources de survie vérifiées et ÉCARTÉES (noté pour traçabilité) :
  - cBioPortal `paad_qcmg_uq_2016` (QCMG, Nature 2016, 456 patients) : le
    fichier clinique datahub n'a pas de OS_MONTHS/OS_STATUS ; `STATUS` +
    `DAYS_TO_LAST_FOLLOWUP` ne sont renseignés que pour 134/456 patients, et
    les identifiants patients (3.014, A10.7…) ne correspondent pas aux
    identifiants ICGC (ICGC_0006…) — pas de jointure possible, non utilisé.
  - cBioPortal `paad_icgc` (ICGC, Nature 2012, 99 patients) : mutations
    seulement, pas d'expression — non utilisé.

## Construction des flux (script `build_fluxes_icgc.py`)
- Jointure expression x clinique sur `icgc_id` : 96/96 retrouvés.
- Filtre : `Sample type == 'Primary tumour'` ET
  `HistoSubtype == 'Pancreatic Ductal Adenocarcinoma'` -> **70 tumeurs**.
  (Les 26 autres échantillons Xena sont d'autres histologies : adénosquameux,
  IPMN avec invasion, etc.)
- Flux (variante a) : les 12 MÊMES gènes que la v4 TCGA, ordre KRAS croissant
  (KRAS log2cpm min 5,16 / médiane 6,36 / max 7,35), sans imputation.
  Nul : lignes permutées, graine 42.
- `pdac_icgc_fluxes.csv` (70 lignes, 13 colonnes)
  SHA-256 : `710d41e55d32360b95f81113579eac4b6de023130b77410bd9ac3df906b61941`
- `pdac_icgc_fluxes_nul.csv`
  SHA-256 : `e020a2c4a7950692ae0e08353db411ceec9b90f564e1f618fc19ef49a065f25e`
- `icgc_clinical_70.csv` (jointure clinique des 70, ordre KRAS)
  SHA-256 : `cd24e4821ef4c4399a274a8b73392d0a11b0deb9556b7270ca27078bcae9ae21`
  Statuts des 70 : Deceased - Of Disease 42, Alive - Without Disease 17,
  Alive - With Disease 6, Deceased - Of Other Cause 4,
  Deceased - Of Unknown Cause 1. Suivi renseigné 70/70.
- Variante (b) (re-sélection fraîche protocole v4) : NON FAITE — optionnelle
  selon le protocole ; la variante (a) étant plate sur les 12 gènes, une
  re-sélection aurait été de la pêche.

## Runs v6 (pipeline ORIGINAL, jamais modifié)
- Fichier : `~/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py`
  SHA-256 : `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`
- Commandes : `python3 universal_v6.0.0_cohen.py --input <csv> --mode fast --output <dir>`
  (script `run_icgc_v6.sh`, journal `runs_icgc_v6.log`).
- `V6_ICGC_EXIT:0` — `results_fast_icgc/` (36 fichiers).
- `V6_ICGC_NUL_EXIT:0` — `results_fast_icgc_nul/` (36 fichiers).

## Survie (script `survival_icgc.py`)
- Survie globale (OS, comme en TCGA §8.12) : temps = Length of Follow Up
  (months) ; événement = tout statut 'Deceased…' (47 décès sur 70).
  Sensibilité DSS : événement = 'Deceased - Of Disease' seul (42 décès).
- Définitions testées, TOUTES rapportées : top12/top7/top20 KRAS,
  quartiles supérieurs MUC16 / CEACAM5 / KRAS seuls, double-quartile CA125+CEA.
- Cox continu (VRAIS univariés : un gène à la fois — cf. correction TCGA du
  16 nov. 07h40, le tableau §8.12 du 15 nov. était l'ajustement à 6 gènes mal
  étiqueté), puis multivarié KRAS+MUC16+CEACAM5, puis DSS.
- Contrôle supplémentaire : Cox MUC16 ajusté sur le sous-type Bailey
  (indicatrices ADEX/Immunogenic/Progenitor/Squamous).

## Résultats (détail dans le rapport de mission)
- EXPRESSION : NON. MUC16 top12 +0,13 sd (rho +0,048, p=0,69) ;
  CEACAM5 top12 +0,28 (rho +0,062, p=0,61). Le nul produit −0,53 à +1,28 :
  les valeurs réelles sont dans le bruit du nul. Pipeline : T_0 52,31 %
  contre nul 32,43 %, Delta 1,44 contre 1,37, L7a NaN (n=70 < 75, cause
  diagnostiquée par le bras parallèle : le diagnostic de bruit exige
  5 bins x 15 points = 75 points).
- SURVIE : PARTIEL. CA125 fort et indépendant — quartile sup. 9,5 contre
  23,8 mois (log-rank p=0,002, DSS p=0,003) ; Cox univarié HR 1,57 (p=0,0076),
  multivarié HR 1,56 (p=0,0082), DSS HR 1,68 (p=0,0043), ajusté sous-type
  HR 1,75 (p=0,0040). KRAS direction seule (HR 1,25, p=0,12 ; top12 p=0,58).
  CEA rien (HR 0,80, p=0,16). Top12 KRAS 14,1 contre 17,7 mois (p=0,58).

## Ce qui manque
- Le fichier donneur ICGC original (`donor.PACA-AU.tsv.gz`, DCC) : inaccessible
  (portail mort). La survie vient du tableau supplémentaire de Bailey 2016,
  mêmes patients, mêmes identifiants ICGC.
- Variante (b) non faite (optionnelle).
- 26/96 échantillons Xena exclus (histologies non-PDAC) — le filtre est
  documenté, pas une perte silencieuse.
