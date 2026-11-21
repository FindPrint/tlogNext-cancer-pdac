# PROVENANCE_876 — §8.76 : GSE131050 (PurIST), lot Yeh_seq FNA

Chantier §8.76, piste nommée au §8.74.9 (lot Yeh_seq FNA, n = 42
codes) et au livre blanc (journal, entrée §8.74). Protocole gelé :
`PROTOCOL_maxsep_gse131050_fna_876.md`, SHA-256
`dd7937ee1b877fefcf675f96e39d4be9a1250375c8c231e4e13294835023bc5f`
(20 nov. 2026, ~21h30 EST, avant toute construction et tout run).
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
  - `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/matrix/GSE131050-GPL18573_series_matrix.txt.gz`

## 2. Fichiers source (réutilisation du téléchargement officiel §8.74)

Aucun nouveau téléchargement dans ce chantier : le fichier source
est celui téléchargé officiellement au §8.74 (20 nov. 2026),
SHA re-vérifié identique avant le gel et avant la construction.

| Fichier | Taille (o) | SHA-256 |
|---|---|---|
| `data/GSE131050_PurIST_Yeh_seq.tsv.gz` | 9 468 179 | `2fc0a66ef0ac62aab17e9bda1c78561786f887a9122591a9346a868f852be5b1` |
| `data/GSE131050-GPL18573_series_matrix.txt.gz` | 6 864 | `9b333eb6b9181fedfc793b9a61f5970af459a5b37b8aa8f7808a3b6c34c7843e` |

## 3. Nature des lignes

- **Fichier supplémentaire TSV : table gène × échantillon**,
  première colonne `geneID` de la forme `ENSG…;SYMBOLE`
  (ex. `ENSG00000133703;KRAS`), 26 267 gènes, 125 échantillons.
  Valeurs numériques ≥ 0, non log-transformées, allure TPM/FPKM ;
  l'article indique « FPKM ou TPM selon l'étude » sans préciser
  pour ce fichier : **nature exacte consignée comme
  indéterminée entre FPKM et TPM**, aucune renormalisation,
  aucune transformation log ajoutée. 0 NaN, 0 cellule vide sur
  les 13 lignes utiles × 125 colonnes.
- **Matrice de série : en-tête seul** (6,7 Ko), sans table
  d'expression — elle porte GSM, titres, plateforme et
  caractéristiques. Plateforme lue dans l'en-tête : GPL18573 =
  Illumina NextSeq 500 (lot Yeh, 125 échantillons).
- **Échantillons :** 191 au total. Lot Yeh (125) : 97 tumeurs
  primaires (Pi) + 28 xénogreffes dérivées de patients (PDX).
  Primaires : 47 FF + 5 FFPE + 45 FNA. Lot Linehan (66) :
  biopsies tumorales de 37 patients (essai de phase 1b
  Nywening et coll.) — écarté au §8.74, non utilisé ici.
- **Lignes = mesures instrumentales** (RNA-seq, comptages
  géniques fournis par les déposants). Le nul (permutation de
  lignes, graine 42) est un échantillon hypothétique, pas une
  mesure.

## 4. Identification des gènes et construction

- Symboles lus après le `;` de `geneID`, sans mapping
  sonde→symbole (table déjà génique). Les 13 gènes utiles
  (12 v4 + KRAS) sont présents, UNE ligne chacun, sans doublon :
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1,
  CEACAM5, CLCA1, MUC16, KRAS. Aucun gène mappé à la main.
  Aucun gène v4 manquant (contrairement à GSE57495 : GSTM1
  absent ; GSE62165 : 10/12).
- **Lot FNA : une tumeur indépendante = une ligne, n = 42.** Les
  45 colonnes FNA primaires (`S###.FNA.Pi.<code>`) sont
  regroupées par code-tumeur (`MMDDT#`, 42 codes) ; les 2 codes
  à réplicats FNA (0417T1 ×3, 1119T1 ×2) sont agrégés par
  MÉDIANE par gène (précédent du projet). Le code 0921T1
  (FNA seul) ENTRE dans le lot FNA. Ordre = KRAS croissant ;
  contrôle jamais flux ; cas complets 42/42, jamais
  d'imputation.
- **KRAS FNA (médiane par code) : min 0,0482, médiane 1,569,
  max 5,803** — contre KRAS FF min 1,152, médiane 6,955,
  max 19,7 (§8.74) : échelle ~4 fois plus basse (échantillons
  faible volume, kit TruSeq RNA Exome contre TruSeq pour les
  FF). Différence de mesure entre types d'échantillons,
  consignée, aucune correction appliquée.
- **Exclus et comptés :** 28 PDX Yeh (pas des tumeurs
  primaires) ; 47 FF primaires Yeh (lot du §8.74 — apparié,
  voir §5) ; 5 FFPE primaires Yeh (autres types
  d'échantillons / kits : TruSeq RNA Exome — non mélangés) ;
  66 biopsies Linehan (37 patients, pré/post-traitement
  mélangées — voir §8.74) ; 0 échantillon normal adjacent (la
  série n'en contient pas).

## 5. Appariement — le lot FNA n'est PAS une cohorte indépendante

Enquête pré-gel (`enquete_876/check_fna_876.py`, SHA
`46c586489b8e913df013ee93346d9995647785ef7e35ba59fe8f39a9ad540d93`,
vérification de portes uniquement, aucun maxsep, aucun run) :

1. Grep avant le gel : « FNA » ne figure que comme « piste
   restante non vérifiée » dans les fichiers du §8.71 et du
   §8.74 et le livre blanc aux mêmes endroits — aucun CSV, run,
   JSON ni valeur `maxsep` n'existait pour le lot FNA. Les
   graines 8761/8762 et le préfixe `_876_` ne figurent dans
   aucun fichier du projet.
2. **Recouvrement FNA ∩ FF : 41 codes sur 42 (97,6 %).**
   Code FNA seul (sans FF) : 0921T1. Code FF seul (sans FNA) :
   PancT6. Total : 43 tumeurs distinctes. **Le lot FNA est
   donc les MÊMES tumeurs que le lot FF du §8.74, vues par un
   autre type d'échantillon** (FNA ex-vivo au moment de la
   résection, 3 passages, aiguille 22G ; kit TruSeq RNA Exome
   contre TruSeq pour les FF ; échantillons faible volume).
3. **Conséquence gelée (protocole §2.2) : le lot FNA N'EST PAS
   une treizième paire principale indépendante et N'ENTRE PAS
   dans le compte A2.** Le compte des paires indépendantes
   reste 12 (8/12, 10/12 positifs, LOO 7/11). Le lot FNA est
   un **test de robustesse apparié** : le signal `maxsep`
   mesuré sur les mêmes tumeurs en FF survit-il au changement
   de type d'échantillon (FNA) ?
4. Données nouvelles générées pour PurIST (UNC), centres
   distincts de toutes les cohortes du projet ; plateforme
   GPL18573 distincte de toutes les plateformes V1 et des
   confirmations.
5. Titres anonymes (`S001…S125`, codes `MMDDT#`), aucun
   code-barres TCGA — vérifié sur le fichier officiel.
   **Caveat :** les titres étant anonymisés, une exclusion
   formelle identifiant par identifiant d'un recouvrement avec
   TCGA_PAAD est impossible ; aucun échantillon ne porte de
   code-barres TCGA et la collecte est décrite comme de novo
   dans l'article (même standard que le §8.71).

## 6. Fichiers produits (SHA-256)

| Fichier | SHA-256 |
|---|---|
| `pdac_876_yeh_fna_fluxes.csv` (42 lignes) | `70697b3aaa125e65b562f63b06bce28e49f0448cc38b1219de5df832ac210324` |
| `pdac_876_yeh_fna_fluxes_nul.csv` (graine 42) | `2474ceaf263a6418bc462202c83c8b3c7059204683efb69ef52d186709ea4d35` |
| `extract_876.json` | `ae14101ee0996193749092c601ed21fa1cbe897cb0e3d0eec158bd46dec02e43` |
| `extract_876.csv` | `a3cb4f9b24fe9b5bf62a5d6b89afa130797147655d50d219b6d13325c03f996e` |
| `direct_tests_876.json` | `55b386dcce81d0188bfcf5a24a496a0ad77be6c4fda9da42771afaa5abf0b823` |
| `maxsep_876_verify.json` | `0dc536a413371e42f167bc79987060b376b9998eac2266b8f2eaf9b984c820ce` |

Scripts (originaux §8.74 intacts) :
`build_fluxes_876.py` `c1b66ac4b35d00257b1345e4d8ce0db1cd76dfef069d7a757656ada4a2913698`,
`build_nul_876.py` `673f1fc277f037141b8879a37c86154789087f4835bfe049ceb73bb2d8477a38`,
`extract_876.py` `041e0f89ca215eb386b2b3c6e8dec6d7bde134b92642091205ceed1302604f7f`,
`verify_876.py` `533cd03a2248252d85a0cd4513636e028a8b61bc78f9997e5ab8310ceea9c400`,
`direct_tests_876.py` `bf0a8b8b64a8a44ae3d6d782b161f3bf05ccc5d8f6b5e612a4fdcf2a304f0660`.
Manifeste : `manifest_v62_876.txt` `0e63d732fbbeb5210b53f37abec1b7432ef0c00cd3075ffea0366695fee539f7`.
Journal : `runs_v62_876.log` `cd6e55fd1b6828546e28807e7da897d2a5c52853a208d442fd174e333c275e22`.
Enquête pré-gel : `enquete_876/check_fna_876.py` `46c586489b8e913df013ee93346d9995647785ef7e35ba59fe8f39a9ad540d93`.

Runs v6.2 mode fast : 2/2, exits 0/0
(`results_fast_v62_876_yeh_fna`, `..._nul`). Unités systemd
`v62-876` (lot principal, réel terminé EXIT 0) et `v62-876b`
(reprise après redémarrage, SKIP réel, nul terminé EXIT 0,
FIN 2026-11-21T01:32:02Z). **Incident consigné : la machine a
redémarré entre les deux runs** (uptime 0 min constaté à
01h30 UTC) — le run réel était déjà terminé (EXIT 0 consigné,
`master_results.json` complet, 8 099 157 o) ; le run nul,
interrompu en cours (dossier partiel : un seul fichier,
`landscape_complexity.png`), a été relancé par le lanceur
reprenable qui a sauté le réel déjà complet — aucune reprise à
l'aveugle, aucun dossier de run touché. Extraction 2/2 à 0,0
exact (vérification indépendante, `verify_876.py`).
**Aucun nul frais** : `d_maxsep = +0,1642` est hors de
l'intervalle gelé [−0,07 ; +0,14[ (protocole §7) — la règle
gelée ne les prévoit pas ici. Les graines 8761/8762 restent
inutilisées.

## 7. Ce qui manque

- Nature exacte FPKM vs TPM du fichier Yeh_seq : indéterminée
  (article : « FPKM ou TPM selon l'étude ») — aucune
  transformation ajoutée, valeurs prises telles que fournies.
- Exclusion formelle d'un recouvrement avec TCGA_PAAD :
  impossible par identifiants (titres anonymisés) — voir §5.5.
- Données cliniques individuelles (stade, survie, réponse) :
  non utilisées — l'ordre est KRAS, comme toutes les paires
  principales GEO.
- Le fichier `GSE131050_PurIST_Linehan_seq.tsv.gz` n'est pas
  re-téléchargé ici (déjà dans `data/` depuis le §8.74, SHA
  `729bb794…efc16`) et AUCUN flux ni run n'en est issu dans ce
  chantier. Le lot FFPE (5 échantillons) n'est pas un repli :
  n = 5 < 40.

— Fin de PROVENANCE_876. —
