# PROVENANCE_874 — §8.74 : GSE131050 (PurIST), lot Yeh_seq FF

Chantier §8.74, piste 2/3 du lot du 20 nov. 2026 (go de Zackary
« Les 3 allez s'y », 18h04). Protocole gelé :
`PROTOCOL_maxsep_gse131050_874.md`, SHA-256
`3f34f4ff408c5a3cb71252c46c6193c68588b7fe409021e2b8e4cd2c2d7e1d5f`
(20 nov. 2026, ~23h20 EST, avant tout téléchargement officiel).
Pipeline v6.2 SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant et après le lot, inchangé ; v6.1 `2af5e5ce…c1c9`).

## 1. Source

- **Série : GSE131050**, NCBI GEO — « Purity Independent Subtyping
  of Tumors (PurIST), a clinically robust single-sample classifier
  for tumor subtyping in pancreatic cancer (RNA-Seq) ».
- **Étude d'origine : Rashid NU et coll., *Clin Cancer Res* 2020,
  26(1):82–92.** PMID 31754050, doi 10.1158/1078-0432.CCR-19-1467.
  Centre : Lineberger Comprehensive Cancer Center, University of
  North Carolina at Chapel Hill (UNC), USA. Contacts GEO :
  Jen Jen Yeh, Naim U. Rashid, Xianlu L. Peng
  (xianlu.peng@gmail.com).
- **Dates :** série soumise le 10 mai 2019, publique le 10 déc.
  2019, dernière mise à jour 18 fév. 2022. Sous-série [RNA-Seq]
  de la SuperSeries GSE131049 (l'autre sous-série, GSE131051,
  est NanoString — non utilisée). BioProject PRJNA542388,
  SRA SRP197641. Second PMID cité sur la série : 35155218
  (réutilisation ultérieure — non utilisée ici).
- **URLs (FTP NCBI, convention des autres provenances) :**
  - `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/suppl/GSE131050_PurIST_Yeh_seq.tsv.gz`
  - `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/suppl/GSE131050_PurIST_Linehan_seq.tsv.gz`
  - `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/matrix/GSE131050-GPL18573_series_matrix.txt.gz`
  - `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/matrix/GSE131050-GPL16791_series_matrix.txt.gz`

## 2. Fichiers téléchargés (téléchargement officiel, après le gel)

| Fichier | Taille (o) | SHA-256 |
|---|---|---|
| `data/GSE131050_PurIST_Yeh_seq.tsv.gz` | 9 468 179 | `2fc0a66ef0ac62aab17e9bda1c78561786f887a9122591a9346a868f852be5b1` |
| `data/GSE131050_PurIST_Linehan_seq.tsv.gz` | 5 157 464 | `729bb794f969bacc56807dc3b9bd1674df64a91f90ae7845ecef45eb80fefc16` |
| `data/GSE131050-GPL18573_series_matrix.txt.gz` | 6 864 | `9b333eb6b9181fedfc793b9a61f5970af459a5b37b8aa8f7808a3b6c34c7843e` |
| `data/GSE131050-GPL16791_series_matrix.txt.gz` | 4 859 | `03aa8ca6b1f5d44f827f819ee91c256ab9c1df5dfa78b9ca23f27cbb49b1df94` |

Les quatre SHA officiels sont IDENTIQUES à ceux des copies
d'enquête pré-gel (enquête du 20 nov. 2026, copies temporaires
dans `enquete_874/`, supprimées après le gel ; scripts d'enquête
conservés : `parse_matrix.py`, `parse_yeh.py`,
`yeh_patients.py`, `yeh_ff_detail.py`, `linehan_titles.py`,
`check_genes.py`, `check_values.py`). Aucun écart : les portes
§5 n'ont pas eu à être re-vérifiées sur une version différente.

## 3. Nature des lignes

- **Fichiers supplémentaires TSV : tables gène × échantillon**,
  première colonne `geneID` de la forme `ENSG…;SYMBOLE`
  (ex. `ENSG00000133703;KRAS`), 26 267 gènes (Yeh) / 23 686
  gènes (Linehan). Valeurs numériques ≥ 0, non log-transformées,
  allure TPM/FPKM ; l'article indique « FPKM ou TPM selon
  l'étude » sans préciser pour ces deux fichiers : **nature
  exacte consignée comme indéterminée entre FPKM et TPM**,
  aucune renormalisation, aucune transformation log ajoutée.
  0 NaN, 0 cellule vide sur les 13 lignes utiles × 125 colonnes
  (Yeh) et × 66 colonnes (Linehan).
- **Matrices de série : en-têtes seuls** (4,7 Ko / 6,7 Ko), sans
  table d'expression — elles portent GSM, titres, plateforme et
  caractéristiques. Plateformes lues dans les en-têtes :
  GPL16791 = Illumina HiSeq 2500 (lot Linehan, 66 échantillons),
  GPL18573 = Illumina NextSeq 500 (lot Yeh, 125 échantillons)
  — titres confirmés par les fichiers SOFT des plateformes
  (`!Platform_title`).
- **Échantillons :** 191 au total. Lot Yeh (125) : 97 tumeurs
  primaires (Pi) + 28 xénogreffes dérivées de patients (PDX).
  Primaires : 47 FF + 5 FFPE + 45 FNA. Lot Linehan (66) :
  biopsies tumorales de 37 patients (essai de phase 1b
  Nywening et coll., FOLFIRINOX ± inhibiteur CCR2, PDAC
  localement avancé, patients sans traitement préalable,
  biopsies avant traitement puis après traitement).
- **Lignes = mesures instrumentales** (RNA-seq, comptages
  géniques fournis par les déposants). Le nul (permutation de
  lignes, graine 42, puis graines 8741/8742) est un échantillon
  hypothétique, pas une mesure.

## 4. Identification des gènes et construction

- Symboles lus après le `;` de `geneID`, sans mapping
  sonde→symbole (table déjà génique). Les 13 gènes utiles
  (12 v4 + KRAS) sont présents, UNE ligne chacun, sans doublon,
  dans les DEUX fichiers supplémentaires :
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1,
  CEACAM5, CLCA1, MUC16, KRAS. Aucun gène mappé à la main.
- **Paire primaire : lot Yeh_seq FF, une tumeur indépendante =
  une ligne, n = 42.** Les 47 colonnes FF primaires
  (`S###.FF.Pi.<code>`) sont regroupées par code-tumeur
  (`MMDDT#`, 42 codes) ; les 4 codes à réplicats FF (0417T1 ×3,
  0523T1 ×2, 0806T1 ×2, 1119T1 ×2) sont agrégés par MÉDIANE par
  gène (précédent du projet). Le code 0921T1 (FNA seul) n'entre
  pas dans le lot FF. Ordre = KRAS croissant ; contrôle jamais
  flux ; cas complets 42/42, jamais d'imputation.
- **Exclus et comptés :** 28 PDX Yeh (pas des tumeurs
  primaires) ; 45 FNA + 5 FFPE primaires Yeh (autres types
  d'échantillons / kits : TruSeq RNA Exome contre TruSeq pour
  les FF — non mélangés) ; 66 biopsies Linehan (37 patients,
  pré/post-traitement mélangées, métadonnées GEO sans label
  pré/post — voir §5) ; 0 échantillon normal adjacent (la
  série n'en contient pas).

## 5. Indépendance — vérifications faites

1. Grep avant le gel : « GSE131050 » ne figure que comme « piste
   restante non vérifiée » dans les trois fichiers du §8.71 et
   le livre blanc aux mêmes endroits — aucun CSV, run, JSON ni
   valeur `maxsep` n'existait pour GSE131050.
2. Données nouvelles générées pour PurIST (UNC + essai Linehan),
   centres distincts de toutes les cohortes du projet ;
   plateforme GPL18573 distincte de toutes les plateformes V1
   et des confirmations.
3. Les jeux publics de la méta-analyse PurIST (TCGA_PAAD,
   PACA_AU, Moffitt_GEO_array, Aguirre, COMPASS) ne sont PAS
   redéposés dans GSE131050 — la série ne contient que Yeh_seq
   et Linehan_seq. GSE131050 n'est pas un re-découpage d'une
   cohorte déjà tenue.
4. Titres anonymes (`S001…S125`, codes `MMDDT#`), aucun
   code-barres TCGA — vérifié sur le téléchargement officiel
   (porte §5). **Caveat :** les titres étant anonymisés, une
   exclusion formelle identifiant par identifiant d'un
   recouvrement avec TCGA_PAAD est impossible ; aucun
   échantillon ne porte de code-barres TCGA et la collecte est
   décrite comme de novo dans l'article (même standard que
   le §8.71).
5. **Lot Linehan écarté d'avance (protocole §2.3) :** 66 biopsies
   pour 37 patients ; l'article confirme le mélange pré/post-
   traitement (« The Linehan Phase 1b trial captured both pre-
   and post-treatment biopsies », fig. 2C) ; les métadonnées
   GEO ne labellisent pas pré/post ; le plus grand sous-ensemble
   homogène de tumeurs indépendantes pré-traitement est d'au
   plus 37 < 40. Aucun CSV, aucun run pour ce lot.

## 6. Fichiers produits (SHA-256)

| Fichier | SHA-256 |
|---|---|
| `pdac_874_yeh_ff_fluxes.csv` (42 lignes) | `db258c9900e0f6c603ff62f008e7cee6a4621ee1632a9d69d1544db86d58fe44` |
| `pdac_874_yeh_ff_fluxes_nul.csv` (graine 42) | `e9468376d87ebbe5d4af51276af8ce64a3852ee2d3aec9c1471889eb78c2305b` |
| `pdac_874_yeh_ff_fluxes_nul_s8741.csv` | `627bbf220672225be688ac362cc8a663c70d773838406a56c9d4835373b771c5` |
| `pdac_874_yeh_ff_fluxes_nul_s8742.csv` | `68d95935f57f120631a03bbce5dfe1089c988392665c8fb61df50e620992c483` |
| `extract_874.json` | `82ade74701245021dfdb965bdc689ac98262c70f12ecec7f39e1b5b742dfcb47` |
| `extract_874.csv` | `163de3bf04b4e15b7c653240ff164e68e4dd5f1dd946d5507748b34e8eb773fe` |
| `direct_tests_874.json` | `1d18f6dc3dbbc09cceecfdf256c0ebe9dc4aea83a5591669c99035f7ba488d71` |
| `maxsep_874_verify.json` | `1c29544c7f1b14eb91a73d51fcd63d36191c64a4c7f11ae52db67f6c69e55e6f` |

Scripts (originaux §8.71 intacts) :
`build_fluxes_874.py` `02910920…846c13`,
`build_nul_874.py` `4b949d3b…7faa`,
`extract_874.py` `395909c3…8b8f`,
`verify_874.py` `ac7fac6d…dc13`,
`direct_tests_874.py` `be58861e…5781b`.
Manifestes : `manifest_v62_874.txt` `d130c20b…29f`,
`manifest_v62_874_frais.txt` `4df63561…9094`.
Journaux : `runs_v62_874.log` `7a15d398…63`,
`runs_v62_874_frais.log` `e45027c6…716`.

Runs v6.2 mode fast : 4/4, exits 0/0/0/0
(`results_fast_v62_874_yeh_ff`, `..._nul`, `..._nul_s8741`,
`..._nul_s8742`). Unités systemd `v62-874` (lot principal,
FIN 2026-11-20T23:22:49Z) et `v62-874b` (nuls frais, FIN
2026-11-20T23:29:08Z). La machine a redémarré entre les deux
lots (uptime 0 min constaté à 23h24 UTC) — le lot principal
était déjà terminé (2/2, FIN consignée) ; aucune reprise à
l'aveugle, aucun dossier de run touché. Extraction 4/4 à 0,0
exact (vérification indépendante, `verify_874.py`).

## 7. Ce qui manque

- Nature exacte FPKM vs TPM des deux fichiers supplémentaires :
  indéterminée (article : « FPKM ou TPM selon l'étude ») —
  aucune transformation ajoutée, valeurs prises telles que
  fournies.
- Label pré/post-traitement des 66 biopsies Linehan : absent
  des métadonnées GEO (table supplémentaire 2 de l'article
  non récupérée — le lot est écarté pour une raison
  structurelle, ce label ne changerait pas la décision).
- Exclusion formelle d'un recouvrement avec TCGA_PAAD :
  impossible par identifiants (titres anonymisés) — voir §5.4.
- Données cliniques individuelles (stade, survie, réponse) :
  non utilisées — l'ordre est KRAS, comme toutes les paires
  principales GEO.
- Le fichier `GSE131050_PurIST_Linehan_seq.tsv.gz` est
  téléchargé et conservé dans `data/` (SHA consigné §2) mais
  AUCUN flux ni run n'en est issu dans ce chantier.

— Fin de PROVENANCE_874. —
