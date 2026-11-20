# PROTOCOLE GELÉ — §8.58 : Bloc estomac / mucus : nouveaux flux inattendus (y compris les odeurs)

Date : 19 nov. 2026. Chantier §8.58, mission parent du 19 nov. 2026.
Ce protocole est gelé AVANT tout inventaire chiffré, toute construction
et tout run. Aucun run sans ce fichier. Aucun paramètre ne change après
les résultats. Le livre blanc N'EST PAS édité, le PDF N'EST PAS régénéré,
rien n'est poussé sur GitHub (instruction explicite). La section §8.58
est écrite dans un FICHIER SÉPARÉ (`section_8.58_stomach_mucus_flux.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié ; v6.1
`2af5e5ce…c1c9`, v6 `bb8bbdba…c0773` revérifiés à la fin).

## 0. Question à trancher

Au §8.45 (test C), le bloc estomac/mucus MONTE avec le stade clinique
au lieu de s'effondrer (top-12 stade : PGC +0,51, CLDN18 +0,57,
DPCR1 +0,40 ; MUC16 plate −0,10), à l'inverse de la chaîne KRAS (§8.4).
Zackary demande d'explorer des flux auxquels on n'avait pas pensé,
y compris les odeurs et autres. Question : existe-t-il, dans les
matrices DÉJÀ DÉTENUES, d'autres flux cohérents autour de ce bloc —
mucus/gastrique étendu, enzymes digestives, récepteurs olfactifs
exprimés hors nez, métabolisme volatil / signalisation chimique, autres
groupes cohérents — et que font-ils avec le stade et avec KRAS ?
Un gène absent d'une matrice est noté ABSENT, jamais remplacé, jamais
imputé. Un négatif est un résultat.

## 1. Listes candidates — définies AVANT tout regard aux matrices

Les listes ci-dessous sont fixées avant l'inventaire ; l'inventaire ne
fait que cocher présent/absent. Aucun gène n'est ajouté après avoir vu
les données, sauf dans le groupe (e) qui est défini ici comme
« groupes cohérents repérés dans l'univers des matrices » et dont la
composition exacte est alors écrite dans la section avec sa règle de
repérage (préfixe de symbole ou famille HUGO), jamais choisie sur les
résultats.

- (a) G1 MUCUS / GASTRIQUE ÉTENDU (35 symboles) :
  MUC1, MUC3A, MUC4, MUC5AC, MUC5B, MUC6, MUC7, MUC12, MUC13, MUC15,
  MUC19, MUC20, MUC21, TFF1, TFF2, TFF3, GKN1, GKN2, PGA3, PGA4, PGA5,
  ATP4A, ATP4B, GIF, LIPF, GAST, GHRL, SST, REG1A, REG1B, REG3A, REG3G,
  FCGBP, AGR2, SPDEF, AQP5.
  Référence (déjà v4, non recomptés ici comme « nouveaux ») : PGC,
  REG4, CLDN18, MUC17, DPCR1, MUC2, MUC16.
- (b) G2 ENZYMES DIGESTIVES (30 symboles) :
  PNLIP, PNLIPRP1, PNLIPRP2, CEL, CELA1, CELA2A, CELA2B, CELA3A,
  CELA3B, CPA1, CPA2, CPB1, CPB2, CTRB1, CTRB2, CTRC, AMY2A, AMY2B,
  AMY1A, AMY1B, AMY1C, PLA2G1B, CLPS, PRSS1, PRSS2, PRSS3, CPA3,
  ELA2A, ELA3A, ELA3B.
  (PNLIP/CTRB2/CELA3A/CTRB1/CPA1/CELA2A/CPB1/CELA3B/CLPS/CTRC/CPA2
  sont les 11 gènes du score acineux v4 : ils servent AUSSI de
  contrôle de cohérence — un flux qui les contient ne peut pas être
  lu comme indépendant de la correction de pureté ; c'est nommé,
  pas caché.)
- (c) G3 RÉCEPTEURS OLFACTIFS : TOUS les symboles de la forme
  `OR<n><lettre><n>` (familles OR1 à OR14, OR51, OR52, …) présents
  dans l'univers de chaque matrice, repérés par l'expression
  régulière `^OR[0-9]+[A-Z]?[0-9]*$` appliquée aux symboles de la
  matrice, PLUS la liste fermée des OR ectopiques cités dans la
  mission : OR51E2, OR51E1, OR2AT4, OR1A1, OR2J3, OR10J5 (s'ils ne
  sont pas déjà couverts par la regex). Un OR absent est noté
  absent. Les OR sont des gènes codants ; leur présence comme ligne
  de matrice ne prouve aucune expression fonctionnelle — la
  médiane d'expression et la variance sont rapportées par gène
  pour chaque matrice RNA, et un OR à expression quasi nulle est
  dit tel, pas interprété.
- (d) G4 MÉTABOLISME VOLATIL / SIGNALISATION CHIMIQUE (62 symboles) :
  ADH1A, ADH1B, ADH1C, ADH4, ADH5, ADH6, ADH7, ALDH1A1, ALDH2,
  ALDH3A1, ALDH3B1, CYP2E1, CYP2A6, CYP2A13, CYP1A2, CYP3A4, CYP2C9,
  UGT1A1, UGT2B7, SULT1A1, AOX1, FMO1, FMO3, TAAR1, TAAR2, TAAR5,
  TAAR6, TAAR8, TAAR9, TAS1R1, TAS1R2, TAS1R3, TAS2R1, TAS2R3,
  TAS2R4, TAS2R5, TAS2R7, TAS2R8, TAS2R9, TAS2R10, TAS2R13, TAS2R14,
  TAS2R16, TAS2R19, TAS2R20, TAS2R30, TAS2R31, TAS2R38, TAS2R39,
  TAS2R40, TAS2R41, TAS2R42, TAS2R43, TAS2R44, TAS2R45, TAS2R46,
  TAS2R50, NOS1, NOS2, NOS3, CBS, CTH, MPST, HMOX1, HMOX2.
- (e) G5 AUTRE GROUPE COHÉRENT — marqueurs intestinaux et
  neuroendocrines (15 symboles, définis a priori) :
  CDX1, CDX2, VIL1, SI, LCT, FABP2, APOA4, APOB, KRT7, KRT19, CHGA,
  CHGB, SYP, INSM1, NEUROD1.
  Tout groupe supplémentaire repéré pendant l'inventaire (par
  préfixe/famille, jamais sur les résultats) est ajouté ici avec
  sa règle de repérage et sa liste fermée, avant les runs.

## 2. Inventaire — matrices déjà détenues, rien de re-téléchargé

Matrices (univers de symboles = lignes après les mappings déjà
documentés du projet) :
- TCGA-PAAD : `data/tcga_paad_rsem.tar.gz`, MD5
  `b09569ce3f4721f514bc137bd109ac0a` (Firehose stddata 2016-01-28,
  RSEM genes normalized ; 178 tumeurs, code 01).
- GSE71729 : `data/GSE71729_series_matrix.txt.gz` (GPL20769,
  ID_REF déjà des symboles, 19 749 lignes ; 145 échantillons).
- GSE62452 : `data/GSE62452_series_matrix.txt.gz` (GPL6244,
  ID_REF numériques, mapping plateforme GPL6244, 25 293 sondes
  avec symbole ; 69 échantillons).
- ICGC PACA-AU : `data/icgc_pacaau_exp.txt.gz` + probemap
  `data/icgc_pacaau_probemap.gz` (Ensembl → symbole, médiane par
  symbole ; 96 échantillons → 70 tumeurs primaires PDAC).
- CPTAC protéine : `data/cptac/pdac_umich_protein_gene_matrix.csv`
  (UMich) et `data/cptac/bcm-pdac-proteomics-…-Tumor.txt.gz` (BCM),
  abondances protéiques par gène (pas de l'ARN : la nature
  différente est nommée dans chaque ligne du tableau).
- DepMap CRISPR : `data/CRISPRGeneEffect.csv` (dépendance
  génique, pas d'expression ; présence = ligne du fichier,
  nature nommée ; 45 lignées pancréas dans le flux DepMap
  du projet).

Pour chaque candidat et chaque matrice : PRÉSENT ou ABSENT, avec
comptes exacts (n présents / n listés par groupe et par matrice ;
pour G3 : nombre total d'OR présents + liste). Aucune imputation.
Les symboles dupliqués sont agrégés par médiane (règle déjà
utilisée aux §8.31–§8.45). Les gènes à variance nulle ou à
expression quasi nulle sont signalés, pas exclus en silence.

## 3. Construction des flux (TCGA, primaire)

- Méthode : EXACTEMENT celle de la v4 (`build_fluxes_tcga_v4.py`) :
  log2(RSEM+1), scores acineux (médiane des 11 gènes) et îlots
  (INS, GCG, PPY, SST), régression linéaire par gène sur
  [1, acineux, îlots], flux = résidu. Vérification de reproduction
  : les résidus recalculés reproduisent le CSV v4 à atol 1e-9
  (comme au §8.45) avant toute construction ; sinon ARRÊT.
- Un fichier de flux par groupe G1–G5 et par ordre :
  `pdac_tcga_858_<groupe>_kras.csv` (ordre = résidu KRAS
  croissant, 178 lignes, 1re colonne `step`) et
  `pdac_tcga_858_<groupe>_stage.csv` (ordre = rang de stade
  principal I=1..IV=4, départage ex æquo par code-barres
  lexicographique, 175 lignes, 1re colonne `STAGE` ; 3 tumeurs
  sans stade exclues, mêmes codes qu'au §8.45).
  Colonnes de flux = gènes du groupe PRÉSENTS dans TCGA.
  Règle de plafonnement, gelée avant tout calcul : si un groupe
  compte plus de 20 gènes présents, seuls les 20 de plus forte
  variance des résidus sont retenus comme flux (les autres sont
  listés comme présents-non-retenus dans la section ; la règle
  s'applique surtout à G3 si des dizaines d'OR sont présents).
- Groupe non construit si < 3 gènes présents dans TCGA (flux
  dégénéré) : noté, sans run. Groupes à 3–19 gènes : tous retenus.
- Nuls : mêmes lignes permutées, graine 42, générateur frais
  `rng(42)`, colonne de contrôle intacte (même convention que
  tous les nuls du projet). Le contrôle (step/STAGE/KRAS) n'est
  JAMAIS un flux : pas de doublon contrôle/flux.
- G2 et pureté : les 11 gènes acineux du score de pureté sont
  AUSSI dans G2 — les flux G2 sont donc des résidus après
  régression sur un score construit à partir d'eux-mêmes. C'est
  un biais de construction nommé d'avance : les lectures G2
  sont rapportées avec cette réserve et comparées au témoin
  « acineux seuls » si le groupe est construit (les 11 gènes
  acineux comme flux, même protocole, mêmes ordres) — ce témoin
  est un 6e lot, décidé ici, avant les runs.
- Script : `build_fluxes_858_tcga.py` (neuf, originaux intacts),
  provenance `PROVENANCE_858.md` (SHA des CSV réel/nul, du
  script, du pipeline, du tarball, du fichier clinique ;
  effectifs ; exclus ; jointure).

## 4. Runs v6.2 (mode fast, TCGA)

- Lot primaire : pour chaque groupe construit (G1–G5 + témoin
  acineux) : 2 ordres × 2 (réel/nul) = 4 runs, soit jusqu'à
  24 runs. Manifeste `manifest_v62_858.txt`, lanceur reprenable
  `run_v62_lot.sh` (saute les sorties déjà complètes), journal
  `runs_v62_858.log` (SHA du pipeline en tête, exits consignés).
  Lancement en `systemd-run --unit=v62-858 --collect` (jamais
  nohup — un nohup meurt avec la session), surveillance qui
  s'arrête d'elle-même à N/N. Ne JAMAIS supprimer le dossier
  d'un run en cours.
- Minimum pipeline : 40 points (v6.1). Séries TCGA : 178
  (KRAS) et 175 (stade) lignes — au-dessus du minimum.
- Lecture (extracteur copié, original intact ; clés §8.38) :
  cascade, MC (score + seuil), max_separation, stability,
  S_sep = max_separation × stability, Delta, L7a, falsification,
  bruit, F1/F2 « Tous ».

## 5. Tests directs (harnais, hors pipeline)

Même méthode que §8.34/§8.36/§8.45, script neuf
`reading_858.py` sur copie, originaux intacts :
- (D1) top-12 contre reste, gène par gène (d de Cohen ; ordre
  stade : 12 dernières lignes = plus haut stade ; ordre KRAS :
  12 dernières lignes = plus KRAS), réel et nul aux mêmes indices.
- (D2) contrastes par groupes : stade IV contre I ; III+IV
  contre I+II (d + Mann-Whitney bilatéral, p nominales) ;
  ordre KRAS : tertile haut contre tertile bas.
- (D3) tendance ordinale : Spearman rho de chaque flux contre
  le rang de stade (1–4) et contre le rang KRAS ; mêmes rho
  sur le nul.
- (D4) autour de T_0 si un T_0 existe (fenêtres ±20 lignes).
- Références de comparaison : bloc v4 au §8.45 (stade : PGC
  +0,51, CLDN18 +0,57, DPCR1 +0,40, MUC16 −0,10) et au §8.4
  (KRAS : PGC −0,89, DPCR1 −0,85, CLDN18 −0,46, MUC16 +0,64).

## 6. Confirmation sur autres cohortes — règle conditionnelle gelée

Pour chaque groupe, SI au moins un des deux ordres TCGA donne
(MC réel − MC nul > 0,05) OU (S_sep réel − S_sep nul > 0,05)
OU (un test direct D1 |d| ≥ 0,50 au-delà du nul), ALORS :
confirmation GSE71729 ordre KRAS (2 runs : réel + nul, mêmes
gènes, sans correction de pureté — variante (a) comme aux
§8.31–§8.32) et, si le stade y est exploitable sans nouveau
téléchargement, GSE62452 ordre KRAS + ordre stade (4 runs).
Sinon : pas de runs de confirmation — l'inventaire seul fait
foi pour les autres cohortes, et c'est dit tel quel. Les
cohortes ICGC (pas de stade exploitable sans retraitement
clinique), CPTAC (protéine, pas d'ordre KRAS résiduel construit)
et DepMap (dépendance CRISPR, pas expression) ne font l'objet
que de l'inventaire, pas de runs v6.2 dans ce chantier — nommé,
pas caché.

## 7. Critères — écrits avant les runs

- Aucun seuil de séparation réel/nul n'est pré-enregistré pour
  MC, Delta, L7a, falsification : les écarts sont présentés
  comme des pistes, jamais comme des preuves (convention
  §8.31/§8.32/§8.34/§8.36/§8.45).
- Gigue v6.2 mesurée = 0,00 (§8.37) : un écart réel − nul non
  nul est au-delà du bruit de l'instrument — ce qui ne suffit
  pas à en faire une séparation démontrée.
- Le verdict par groupe repose sur les tests directs (D1–D4,
  réel contre nul), pas sur un score du pipeline seul. Ne
  JAMAIS exiger de consensus entre flux ou contrôles : plusieurs
  seuils critiques peuvent se succéder en chaîne causale.
- Les OR : aucune affirmation d'« odorat tumoral » ou de
  fonction olfactive — seule l'expression mesurée (ou son
  absence) est rapportée. Un OR présent à expression quasi
  nulle n'est PAS une preuve d'olfaction, et un OR absent
  n'est pas une preuve d'absence de signalisation chimique.

## 8. Livrables

- Ce protocole (gelé avant inventaire, construction et runs).
- `build_fluxes_858_tcga.py` + `PROVENANCE_858.md` + inventaire
  `inventory_858.csv` (présent/absent par gène et par matrice).
- `manifest_v62_858.txt`, `runs_v62_858.log`, dossiers
  `results_fast_v62_858_*`.
- Lecture flux par flux (`reading_858.py` + table vérifiée
  `direct_tests_858.csv` + `extract_858.json`).
- §8.58 dans le FICHIER SÉPARÉ
  `section_8.58_stomach_mucus_flux.md` (le livre blanc n'est
  PAS édité).
- PDF NON régénéré. Rien poussé sur GitHub.

## 9. Limites nommées d'avance

- Les matrices RNA mesurent des transcrits, pas des protéines
  ni des odeurs : aucun composé volatil n'est mesuré dans ce
  chantier (pas de données de volatilome détenues) — la piste
  « odeurs » est testée au niveau des gènes (récepteurs et
  enzymes), pas au niveau des molécules odorantes elles-mêmes.
- TCGA : 4 niveaux de stade seulement, ties massives (IIB
  118/175), ordre intra-stade arbitraire, sommet mince
  (III + IV = 8 tumeurs) — mêmes limites qu'au §8.45.
- G2 / pureté : biais de construction nommé au §3.
- OR : familles multigéniques à forte homologie — les
  symboles sont ceux des annotations détenues ; aucun
  réalignement ni réannotation n'est fait ici.
- Pas de données single-cell, spatiales, longitudinales,
  ni de volatilome (§8.33).
