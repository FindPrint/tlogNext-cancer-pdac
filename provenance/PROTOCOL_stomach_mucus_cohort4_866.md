# PROTOCOLE GELÉ — §8.66 : Bloc estomac / mucus, quatrième cohorte

Date : 20 nov. 2026. Chantier §8.66, mission parent du 20 nov. 2026.
Ce protocole est gelé AVANT tout téléchargement, toute construction et
tout run. Aucun téléchargement sans ce fichier. Aucun paramètre ne
change après les résultats. Le livre blanc N'EST PAS édité, le PDF
N'EST PAS régénéré, rien n'est poussé sur GitHub (instruction
explicite). La section §8.66 est écrite dans un FICHIER SÉPARÉ
(`section_8.66_stomach_mucus_cohort4.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié ; v6.1
`2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`).

## 0. Question à trancher

Au §8.58, le bloc estomac/mucus et le programme neuroendocrine (G5)
sont confirmés sur trois cohortes (TCGA-PAAD, GSE71729, GSE62452) :
G5 s'efface quand KRAS monte (SYP, INSM1, CHGA/CHGB chutent ;
KRT7/KRT19 montent) et baisse avec le stade ; le mucus étendu (G1)
monte partiellement avec KRAS (AGR2 partout, MUC4 seulement en
TCGA, MUC6 chute en GSE71729) et avec le stade (TFF1) ; le volatil
(G4) confirme (AOX1 chute dans les trois cohortes, UGT1A1 monte,
NOS1 chute dans les deux GEO) ; les odeurs (G3) chutent avec KRAS,
aucun OR ne monte. Question : ces lectures tiennent-elles dans une
QUATRIÈME cohorte indépendante, jamais utilisée dans ce projet ?
Un gène absent de la matrice est noté ABSENT, jamais remplacé,
jamais imputé. Un négatif est un résultat.

## 1. Cohorte choisie — avant tout téléchargement

Cohortes DÉJÀ utilisées dans ce projet (exclues comme « quatrième ») :
TCGA-PAAD, GSE71729, GSE62452, ICGC PACA-AU, CPTAC PDC000393
(UMich + BCM). GSE28735 est seulement citée en passant dans
`PROVENANCE_geo62452.md` (effet de lot) : elle n'a jamais servi
de cohorte dans ce projet, mais elle n'est PAS retenue ici (pas
de stade par échantillon exploitable ; voir §1.3).

### 1.1 Cohorte primaire : GSE62165

- Dépôt : NCBI GEO, série GSE62165, plateforme GPL13667
  (Affymetrix Human Genome U219 Array).
- Déposants : Janky et coll. (dépôt GEO) ; analyse par stade :
  Wang et coll., *Cancer Cell Int* 2018, « Analysis of dynamic
  molecular networks for pancreatic ductal adenocarcinoma
  progression » (doi 10.1186/s12935-018-0718-5).
- Effectif publié : 118 PDAC réséqués + 13 témoins non tumoraux ;
  stades publiés : I 8, IIa 30, IIb 62, III 5, IV 13.
- URL exacte (même convention FTP que les provenances
  `PROVENANCE_geo71729.md` et `PROVENANCE_geo62452.md`) :
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62165/matrix/GSE62165_series_matrix.txt.gz`
- Mapping sondes → symboles : annotation de plateforme GPL13667,
  `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL13nnn/GPL13667/annot/GPL13667.annot.gz`
  (si 404 : repli sur le SOFT de plateforme
  `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL13nnn/GPL13667/soft/GPL13667_family.soft.gz`,
  colonne « Gene Symbol » ; si les deux échouent, la cohorte est
  déclarée inutilisable pour cause de mapping indisponible et le
  repli §1.2 s'applique — aucun mapping deviné, aucune sonde
  mappée à la main).
- Hachage : SHA-256 de chaque fichier téléchargé, consigné dans
  `PROVENANCE_866.md` avant toute construction.

### 1.2 Cohorte de repli : GSE57495

Si GSE62165 s'avère inutilisable (téléchargement impossible,
stade absent par échantillon ET KRAS absent, n < 40 tumeurs,
ou mapping impossible) : GSE57495, NCBI GEO, 63 patients PDAC
(Chen et coll. 2015), plateforme GPL6244 (même plateforme que
GSE62452, mapping `GPL6244_probe2symbol.tsv` déjà détenu),
URL `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE57nnn/GSE57495/matrix/GSE57495_series_matrix.txt.gz`.
Stade publié : I 13, II 50 (Frontiers Public Health 2022,
tableau clinique) — à vérifier par échantillon dans la matrice ;
si le stade par échantillon y est absent, ordre KRAS seul.
Même construction, mêmes critères, mêmes tests.

### 1.3 Candidats écartés (raisons écrites d'avance)

- GSE15471 : 39 tumeurs < 40 (minimum v6.2 fast).
- GSE16515 : 36 tumeurs < 40 (et 16 seulement selon une source).
- GSE32676 : 25 tumeurs < 40.
- GSE28735 : 45 tumeurs mais pas de stade par échantillon
  exploitable (NA dans les tableaux cliniques publiés).
- GSE21501 : 102 patients mais la répartition des stades
  publiée est incohérente (73 stade I, 0 stade II) et la
  plateforme est Agilent GPL4133 (mapping à construire) ;
  écartée comme primaire, non retenue comme repli.
- GSE91035 : 25 tumeurs < 40.
- ICGC PACA-CA / E-MTAB-6134 : autre cohorte ICGC, mais accès
  et retraitement hors du périmètre de ce chantier (pas de
  matrice d'expression simple téléchargeable par FTP GEO) ;
  écartée, nommée ici.

## 2. Critères d'acceptation de la cohorte (vérifiés après téléchargement, avant construction)

- n ≥ 40 tumeurs PDAC (minimum v6.2 fast) ; sinon ARRÊT, verdict
  négatif documenté, repli §1.2.
- Gènes des groupes §8.58 présents dans la matrice (comptes par
  groupe consignés) ; groupe non construit si < 3 gènes retenus
  présents ; absents notés, jamais remplacés.
- Information de stade par échantillon OU KRAS présent comme
  ligne de matrice ; si le stade est absent, série stade non
  construite (ordre KRAS seul) et c'est dit tel quel.
- Tumeurs seules (témoins normaux exclus) ; cas complets
  seulement (KRAS + tous les gènes du groupe présents), jamais
  d'imputation.

## 3. Groupes repris du §8.58 — listes retenues TCGA, inchangées

Mêmes listes que `build_fluxes_858_geo.py` (RETAINED), reprises
sans ajout ni retrait :

- G1 mucus/gastrique (20) : TFF1, TFF2, MUC6, MUC5B, MUC4, AQP5,
  REG1A, TFF3, GKN1, PGA3, REG3A, MUC21, PGA4, GKN2, AGR2, GAST,
  SPDEF, FCGBP, MUC13, REG1B.
- G2 enzymes digestives (20) : PRSS1, PRSS3, AMY1A, PNLIPRP2,
  AMY2B, AMY2A, CPB2, CELA2A, CPA3, CELA2B, PNLIP, PLA2G1B, CEL,
  CPB1, PNLIPRP1, CLPS, CPA2, CTRB2, CTRB1, CELA3B.
- G3 récepteurs olfactifs (20) : OR7D2, OR13A1, OR2A4, OR52N4,
  OR2B6, OR51E2, OR51E1, OR2A7, OR52N2, OR2L13, OR1J2, OR2W3,
  OR10H1, OR2A1, OR4C6, OR7A5, OR3A2, OR5K2, OR2T10, OR2C1.
- G4 volatil / signalisation (20) : UGT1A1, ALDH3A1, CYP2C9,
  CYP3A4, ADH1B, UGT2B7, ADH4, ADH1C, ADH6, ADH1A, AOX1, FMO1,
  CYP2E1, NOS1, NOS2, CYP2A6, CBS, TAS1R3, ALDH3B1, TAS2R38.
- G5 intestinal / neuroendocrine (15) : CDX1, CDX2, VIL1, SI,
  LCT, FABP2, APOA4, APOB, KRT7, KRT19, CHGA, CHGB, SYP, INSM1,
  NEUROD1.
- TEMOIN acineux (11, témoin de construction seulement, pas de
  run de confirmation) : PNLIP, CTRB2, CELA3A, CTRB1, CPA1,
  CELA2A, CPB1, CELA3B, CLPS, CTRC, CPA2.
- Référence §8.58 (listes complètes candidates) : G1 36, G2 30,
  G4 65 symboles ; l'inventaire de présence porte sur les
  listes RETENUES (20/20/20/20/15) et, pour G3, sur le scan
  regex `^OR[0-9]+[A-Z]?[0-9]*$` de l'univers de la matrice.

## 4. Construction des flux (variante (a) du §8.58)

Même méthode que `build_fluxes_858_geo.py` (variante (a) des
scripts du projet) : mêmes gènes que les listes retenues TCGA
(ceux présents dans la cohorte), ordre = KRAS (valeurs puce
brutes, croissant), sans correction de pureté, cas complets
seulement. Ordre stade en plus si le stade par échantillon est
exploitable (règle figée ici, avant la construction) :
IA/IB → I, IIA/IIB → II, III → III, IVA/IVB/IV → IV ; valeur
ambiguë (« >IIB » ou autre) → EXCLUE ; stade manquant → exclu ;
départage des ex æquo dans un même stade : GSM, ordre
lexicographique croissant (neutre). Si la série stade tombe
sous 40 lignes, AUCUNE série stade n'est construite, aucun run
stade lancé. Sondes dupliquées vers un même symbole : agrégées
par médiane (règle du projet). Valeurs : log2 telles que
fournies dans la matrice série (valeurs déjà normalisées par
les déposants ; aucune renormalisation, aucune transformation
ajoutée — la nature exacte des valeurs est consignée dans
`PROVENANCE_866.md` d'après l'en-tête de la matrice).
Nuls : bloc des flux permuté par lignes, graine 42, `rng(42)`,
contrôle intact. Le contrôle n'est JAMAIS un flux.
Sorties : `pdac_866_<cohorte>_<groupe>_<ordre>.csv`
(+ `_nul.csv`), préfixe `_866_` pour tous les fichiers du
chantier. Script neuf : `build_fluxes_866.py` (originaux
intacts).

## 5. Runs v6.2 (mode fast)

- Lot : pour chaque groupe construit (G1–G5) : ordres
  disponibles (KRAS ; stade si construite) × 2 (réel/nul),
  soit jusqu'à 20 runs (10 KRAS + 10 stade). Manifeste
  `manifest_v62_866.txt`, lanceur reprenable `run_v62_lot.sh`
  (existant, saute les sorties déjà complètes), journal
  `runs_v62_866.log` (SHA du pipeline en tête, exits consignés).
  Lancement en `systemd-run --unit=v62-866 --collect` (jamais
  nohup), surveillance qui s'arrête d'elle-même à N/N. Ne JAMAIS
  supprimer le dossier d'un run en cours.
- Lecture (extracteur copié, original intact ; clés §8.38) :
  cascade, MC (score + seuil), max_separation, stability,
  S_sep = max_separation × stability, Delta, L7a,
  falsification, bruit, F1/F2 « Tous ».

## 6. Tests directs (harnais, hors pipeline)

Même méthode que `reading_858_geo.py` (copie, original intact) :
- (D1) top-12 contre reste, gène par gène (d de Cohen ; ordre
  stade : 12 dernières lignes = plus haut stade ; ordre KRAS :
  12 dernières lignes = plus KRAS), réel et nul aux mêmes indices.
- (D3) tendance ordinale : Spearman rho de chaque flux contre
  le rang de contrôle (KRAS : pas/step ; stade : rang 1–4) ;
  mêmes rho sur le nul. p nominales bilatérales (scipy).
- Seuils de Bonferroni : 0,05 / (nombre de lignes du tableau
  direct), calculé après construction du tableau et consigné
  dans la section.
- Références de comparaison (valeurs §8.58, reprises telles
  quelles) :
  - G5/KRAS TCGA : SYP −0,392, INSM1 −0,343, KRT19 +0,333,
    CHGB −0,311, KRT7 +0,308 ; GSE62452 : SYP −0,503,
    KRT19 +0,416 ; GSE71729 : CHGA −0,359, INSM1 −0,296,
    KRT19 +0,281.
  - G5/stade TCGA : SYP −0,276, CHGB −0,250 ; GSE62452 :
    NEUROD1 −0,416, CHGA −0,348.
  - G1/KRAS TCGA : MUC4 +0,313, AGR2 +0,328, MUC5B +0,222 ;
    GSE71729 : AGR2 +0,383, MUC6 −0,436.
  - G1/stade TCGA : TFF1 rho +0,204, AGR2 +0,208.
  - G4/KRAS TCGA : UGT1A1 +0,378, ALDH3B1 +0,303, ADH1A
    −0,313, AOX1 −0,289 ; GSE62452 : AOX1 −0,611, UGT1A1
    +0,541, NOS1 −0,529 ; GSE71729 : NOS1 −0,369,
    ALDH3A1 +0,367.
  - G3/KRAS : TCGA OR2A4 +0,259 (seul montant) ; GSE71729
    OR2W3 −0,338 ; GSE62452 OR13A1 −0,423, OR2T10 −0,418.
  - G2/KRAS : chute acineuse (témoin), TCGA CELA2A −0,76 (D1).

## 7. Critères de confirmation — écrits avant les runs

Par groupe et par question, le verdict est CONFIRME / PARTIEL /
NON CONFIRME, porté par les TESTS DIRECTS (réel contre nul),
le pipeline n'étant lu qu'en second (pistes, jamais preuves ;
aucun seuil de séparation réel/nul pré-enregistré pour MC,
Delta, L7a, falsification) :

- Q1 (G1/stade) : CONFIRME si TFF1 ou AGR2 (ou ≥ 2 gènes G1)
  rho > 0 avec p < 0,05 ET au-delà du nul (max |rho| du nul
  du groupe) dans le même sens qu'en TCGA ; PARTIEL si un seul
  gène confirme ou si le sens tient sans p < 0,05 ; NON
  CONFIRME sinon.
- Q2 (G5/KRAS) : CONFIRME si ≥ 2 marqueurs neuroendocrines
  (SYP, INSM1, CHGA, CHGB, NEUROD1) chutent (rho < 0, p < 0,05)
  ET ≥ 1 kératine (KRT7, KRT19) monte (rho > 0, p < 0,05),
  au-delà du nul ; PARTIEL si un seul sens tient ; NON
  CONFIRME sinon.
- Q3 (G3/KRAS) : CONFIRME (dans le sens chute) si ≥ 2 OR
  chutent (rho < 0, p < 0,05) ET aucun OR ne monte
  significativement (rho > 0, p < 0,05) ; le cas OR2A4 est
  rapporté séparément (présent/absent, rho, p) ; NON CONFIRME
  si un OR monte significativement ou si aucun ne chute.
- Q4 (G4/KRAS) : CONFIRME si AOX1 chute (rho < 0, p < 0,05)
  ET UGT1A1 monte (rho > 0, p < 0,05) — les deux sens
  concordants avec TCGA+GSE62452 — au-delà du nul ; PARTIEL
  si un seul des deux tient ; NON CONFIRME sinon.
- Q5 (G1/KRAS) : CONFIRME si AGR2 monte (rho > 0, p < 0,05)
  au-delà du nul ; PARTIEL si MUC4 monte sans AGR2 ou
  l'inverse ; NON CONFIRME sinon. MUC6 est rapporté
  séparément (chute en GSE71729, plat en TCGA).
- Ne JAMAIS exiger de consensus entre flux ou contrôles :
  les groupes ne bougent pas ensemble — G1 monte quand G5
  descend sous KRAS, et c'est l'information.
- Si aucune quatrième cohorte utilisable n'existe (taille,
  accès, gènes absents, mapping impossible), le verdict est
  négatif documenté : la section §8.66 est quand même écrite
  avec ce verdict, les tentatives chiffrées (effectifs,
  codes HTTP, absences) et aucune valeur inventée.

## 8. Livrables

- Ce protocole (gelé avant téléchargement, construction et runs).
- `PROVENANCE_866.md` (source, auteur, date, dépôt, URL,
  SHA-256 des fichiers téléchargés, effectifs, exclus, jointure).
- `build_fluxes_866.py` + inventaire de présence
  (`inventory_866.csv` : présent/absent par gène retenu et par
  cohorte ; scan OR de l'univers).
- `manifest_v62_866.txt`, `runs_v62_866.log`, dossiers
  `results_fast_v62_866_*`.
- Lecture flux par flux (`reading_866.py` + table vérifiée
  `direct_tests_866.csv` + `extract_866.json` / `.csv`).
- §8.66 dans le FICHIER SÉPARÉ
  `section_8.66_stomach_mucus_cohort4.md` (le livre blanc
  n'est PAS édité).
- PDF NON régénéré. Rien poussé sur GitHub.

## 9. Limites nommées d'avance

- Les matrices RNA mesurent des transcrits, pas des protéines
  ni des odeurs : aucun composé volatil n'est mesuré dans ce
  chantier. Un OR présent à expression quasi nulle n'est PAS
  une preuve d'olfaction.
- Le stade est une variable clinique (AJCC), pas une mesure du
  système : niveaux, ties massives, ordre intra-stade
  arbitraire, sommet mince — mêmes limites qu'aux §8.45/§8.58.
- G2 / pureté : biais de construction nommé au §8.58 (8/20
  flux retenus sont des gènes du score acineux) ; ses lectures
  sous KRAS sont rapportées avec cette réserve et comparées
  au témoin acineux du §8.58, pas lues comme « nouvelles ».
- OR : familles multigéniques à forte homologie — les symboles
  sont ceux des annotations détenues ; aucun réalignement ni
  réannotation n'est fait ici.
- Les valeurs de puce sont prises telles que fournies par les
  déposants (normalisation des auteurs) ; aucune
  renormalisation n'est faite ici — la nature exacte des
  valeurs est consignée dans la provenance.
- Pas de données single-cell, spatiales, longitudinales, ni
  de volatilome (§8.33).
