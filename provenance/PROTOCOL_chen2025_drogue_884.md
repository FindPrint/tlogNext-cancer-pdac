# PROTOCOLE GELÉ — Lot drogue Chen 2025 (§8.84)

Date : 21 novembre 2026, ~14h10 EST. Chantier : §8.84 (PISTE 1 du lot
du 21 nov. 2026). Agent : TagPrint (subagent).
Ce protocole est gelé AVANT toute copie de données dans le chantier,
AVANT tout téléchargement nouveau et AVANT tout calcul ou run.
Aucun paramètre ne change après les résultats.
Le livre blanc N'EST PAS édité, le PDF N'EST PAS régénéré, rien n'est
poussé sur GitHub dans ce chantier (convention des chantiers ; fusion
par le coordinateur). La section §8.84 est écrite dans un FICHIER
SÉPARÉ (`section_8.84_chen2025_drogue.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié).

## 0. Question et ce qui est nouveau ici

**Question :** dans l'écran d'organoïdes de Chen et al. 2025
(46 PDO PDAC, 63 drogues, AUC de viabilité), une drogue distingue-t-elle
un groupe défini par KRAS ou par MTAP — et la sensibilité à la
gemcitabine ordonne-t-elle les autres drogues (paire pipeline
exploratoire) ?

**Ce qui est nouveau par rapport aux écrans déjà NÉGATIFS (§8.7, §8.40) :**
- **Autre système :** organoïdes 3D dérivés de patients (PDO), cohorte
  chinoise (Shanghai Changhai Hospital), contre lignées 2D DepMap
  (PRISM primaire 24Q2 : 6 790 composés, 0 FDR < 0,05, FDR min 0,959 ;
  PRISM secondaire 19Q4 : 1 437, 0 FDR < 0,05, FDR min 0,625 ;
  GDSC2 : 269, 0 FDR < 0,05, FDR min 0,561 / 0,882 — §8.7, §8.40.3).
- **Autre mesure :** AUC de viabilité CellTiter-Glo sur 7 concentrations
  en duplicata, 5 jours d'incubation (Chen, Methods), contre viabilité à
  dose unique 2,5 µM (PRISM primaire) et LN_IC50 / AUC (GDSC2).
- **Autre bibliothèque :** 63 composés bespoke (chimiothérapie n = 8,
  cycle cellulaire n = 4, dommages ADN n = 5, cascades classiques n = 34,
  autres n = 12 — article § Drug screening), dont les inhibiteurs KRAS
  G12C AMG510 et MRTX849, absents des écrans PRISM/GDSC2 comme cibles
  KRAS G12C testées sur lignées G12C nommées.
- **Recoupement partiel déclaré :** Gemcitabine, Fluorouracil,
  Oxaliplatin, Irinotecan, Cisplatin, Paclitaxel, Docetaxel, Olaparib,
  Trametinib, Palbociclib sont présents dans les deux mondes — c'est donc
  aussi un re-test partiel sur un système nouveau, et il vaut la peine
  pour cette raison : un négatif 2D ne prouve pas un négatif 3D PDO.
- **Absences communes, à ne pas re-présenter comme découverte :**
  vopimetostat absent des 63 (vérifié sur la liste §2.2) comme des trois
  écrans §8.40 ; aucun inhibiteur PRMT5 ni MAT2A dans les 63 (vérifié
  sur la liste §2.2) comme dans les écrans §8.40 — la sensibilité
  différentielle au vopimetostat lui-même reste intestable partout.
- **Autre groupement :** PRISM/GDSC2 groupaient par dépendance Chronos
  KRAS (continue) ; ici le groupement direct KRAS/MTAP dépend d'une
  table par-PDO (conditionnel, §4) et l'axe pipeline est la sensibilité
  à la gemcitabine, pas KRAS — question différente, pas une répétition.

## 1. Source exacte

- Article : Yin, X., Shen, H., Wang, H. *et al.* « Pathogenic germline
  variants in Chinese pancreatic adenocarcinoma patients »,
  *Nature Communications* **16**, 2214 (2025). Reçu 21 janv. 2024,
  accepté 25 févr. 2025, publié 5 mars 2025.
  DOI : 10.1038/s41467-025-57520-3.
  URL : https://doi.org/10.1038/s41467-025-57520-3.
  Licence : CC BY-NC-ND 4.0. Auteurs correspondants : Haojie Jin,
  Hongbo Yang, Jing Li, Gang Jin. Cohorte : Shanghai Changhai Hospital.
- Fichier source : Supplementary Data 10 =
  `41467_2025_57520_MOESM13_ESM.xlsx` (MOESM13).
  URL complète :
  `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM13_ESM.xlsx`
- Empreinte gelée (§8.79, PROVENANCE_879 §1.1) : 35 732 o, SHA-256
  `0e009cd56d2f6c25b0b355590becc4abfee3e1080633173bc33606d1bf325340`.
  Copie de travail : `data/Chen2025_MOESM13_SupplData10.xlsx` — copie
  du fichier déjà détenu et vérifié au §8.79 (scratch `/tmp/b879/`),
  SHA re-vérifié après copie (§3, porte G1). Ce n'est PAS un nouveau
  téléchargement ; aucun téléchargement n'a lieu avant ce gel, sauf
  les tentatives §4 (après gel, en exécution directe, jamais en
  systemd-run sans proxy — leçon AGENTS.md 2026-11-17 / §8.79).
- Antériorité : pilote exploratoire v5.9.4 (`pilot.md`,
  `run_chen.py`, dossier `universal-log-research`) — JAMAIS couru :
  bloqué avant tout run, N = 46 < 50 (minimum v5.9.4), cible
  Gemcitabine, 62 contrôles prévus, 0 run lancé, 0 résultat.
  Le pilote ne prédit rien ici ; ses choix (cible Gemcitabine, ordre
  source) sont repris en partie au §5, explicitement.

## 2. Nature des lignes (vérifiée 21 nov. 2026 sur MOESM13, avant ce gel)

### 2.1 Feuille « All Drugs AUC » (la matrice du chantier)

- 63 lignes = drogues (colonne 1 = nom, colonne 2 = `cluster`,
  catégorie descriptive, exclue des flux numériques), 46 colonnes =
  PDO, identifiants `DAC_61 … DAC_115` (ordre source conservé pour
  l'identité, pas pour l'ordre d'analyse — voir §5).
- Valeurs : AUC normalisée publiée (Methods : viabilité CellTiter-Glo,
  7 concentrations log10-transformées, AUC GraphPad Prism 9,
  « normalized AUC was obtained by dividing each AUC by the maximum
  AUC for that drug » ; viabilités au-dessus de la ligne de base
  plafonnées à 100). **Valeurs publiées, sans transformation,
  sans imputation, sans renormalisation dans ce chantier.**
- Qualité mesurée (21 nov. 2026, avant gel) : 63 × 46 = 2 898 cellules,
  **0 NaN** ; min 0,0000 (Valproic acid, DAC_22) ; médiane 0,9107 ;
  max 1,1746 (CCT245737) ; **8 drogues avec max > 1** (Sorafenib 1,0564 ;
  Lenvatinib 1,0496 ; AZD6738 1,0986 ; AZD5363 1,1668 ; CCT245737
  1,1746 ; Palbociclib 1,0929 ; Everolimus 1,1018 ; Rapamycin 1,1085)
  — la normalisation « par le maximum » telle que décrite ne plafonne
  donc pas les valeurs à 1 dans le fichier déposé, anomalie consignée
  telle quelle, sans correction ; 6 drogues avec max exactement 1,0 ;
  valeur plafond répétée **0,9985714285714287 (= 699/700) dans
  362/2 898 cellules (12,5 %)**, concentrée dans Valproic acid (36/46),
  APR-246 (32/46), Dacarbazine (29/46), Hydroxychloroquine (27/46),
  Pemetrexed (25/46), Olaparib (20/46) — lue comme un plafond de
  non-réponse (viabilité plafonnée), pas comme une mesure fine ;
  28 drogues sans aucune occurrence de cette valeur.
- Gemcitabine (ancre, §5) : min 0,1399 / médiane 0,4384 / max 0,8167 /
  écart-type 0,1861 (n = 46) — dispersion suffisante pour ordonner.
- Liste des 63 (ordre MOESM13, repris tel quel pour les flux §5) :
  APR-246, Dacarbazine, Artesunate, Bleomycin sulfate, Erlotinib,
  Fludarabine, Gimeracil, Ifosfamide, Lapatinib, Pazopanib,
  Pomalidomide, Sorafenib, Sunitinib, Valproic acid, Alpelisib,
  Enasidenib, Entrectinib, Glasdegib, Ibrutinib, Imatinib, Lenvatinib,
  Lorlatinib, Metformin HCl, Olaparib, Olmutinib, Osimertinib,
  Pemigatinib, Regorafenib, AZD6738, AZD5363, CCT245737, LY3214996,
  Sulfatinib, Masitinib, Avapritinib, Encorafenib, RMC-4550, TNO155,
  Hydroxychloroquine, Motixafortide, Pemetrexed, Palbociclib,
  Capmatinib, BI-3406, COTI-2, Dasatinib, Docetaxel, Mitomycin C,
  Vinblastine sulfate, Adavosertib, Binimetinib, Everolimus, Rapamycin,
  Trametinib, Navitoclax, MRTX849, AMG510, Oxaliplatin, Fluorouracil,
  Paclitaxel, Gemcitabine, Irinotecan, Cisplatin.
- `cluster` (20 valeurs + 8 vides) : DNA Damage 5, VEGFR 5, MAPK 5,
  PI3K/Akt/mTOR 5, Apoptosis 4, EGFR 4, Cell Cycle 4, Metabolism 3,
  Angiogenesis 3, PDGFR 3, JAK/STAT 2, ALK 2, SHP-2 2, RAS 2,
  Ubiquitin 1, Epigenetics 1, Smoothened 1, Autophagy 1, CXCR4 1,
  Met 1, vide 8. Descripteur seulement, jamais un flux.

### 2.2 Ce qui N'EST PAS dans MOESM13 (limites connues avant ce gel)

- **Aucun statut KRAS par PDO, aucun statut MTAP par PDO, aucune
  donnée d'expression ou de nombre de copies par PDO.** MOESM13 ne
  contient que les AUC et la catégorie `cluster`.
- L'article NOMME seulement, dans son texte : 6 organoïdes BRCA2
  (DAC102, DAC58, DAC81, DAC85, DAC53 somatiques ; DAC4 germinal),
  5 organoïdes CFTR VUS_D chimio-résistants (DAC13, DAC73, DAC110,
  DAC32, DAC30), 2 organoïdes Olaparib-sensibles sans BRCA1/2
  (DAC76, DAC99 — dont DAC99 avec mutation somatique ATM),
  et **un seul** organoïde KRAS p.G12C **sans identifiant DAC nommé**,
  sensible à AMG510 et MRTX849. Ces identifiants nommés sont les
  seuls groupements utilisables sans table supplémentaire (§6, D2).
- La feuille « CFTR Drugs AUC » (15 drogues CFTR × 15 PDO :
  DAC2, DAC5, DAC6, DAC13, DAC18, DAC20, DAC24, DAC29, DAC31, DAC32,
  DAC53, DAC54, DAC34, DAC84, DAC72 ; 0 NaN ; min 0,6462 / max 1,0000)
  ne nomme pas lesquels des 15 sont les 4 CFTR-mutants (p.R297Q,
  p.E681V × 2, p.H949P) : **intestable sans la Source Data Fig. 6**
  (§4, D2c conditionnel). n = 15 < 40 : aucune paire pipeline
  sur ce volet, dans tous les cas.

## 3. Portes d'acceptation (vérifiées après le gel, avant construction)

- G1 : copie `data/Chen2025_MOESM13_SupplData10.xlsx` SHA-256 =
  `0e009cd5…5340`, taille 35 732 o ; sinon ARRÊT (section écrite
  quand même, blocage documenté).
- G2 : feuille « All Drugs AUC » = 63 drogues × 46 PDO, 0 NaN,
  Gemcitabine présente, les 46 identifiants DAC distincts ;
  sinon ARRÊT.
- G3 : les 6 organoïdes BRCA2 nommés et les 5 CFTR VUS_D nommés
  sont tous présents parmi les 46 colonnes ; sinon les tests D2
  concernés sont déclarés impossibles (pas de substitution).
- G4 : pipeline v6.2 SHA re-vérifié avant ET après le lot
  (`f07567c4…c3abf`) ; jamais modifié.

## 4. Table par-PDO KRAS / MTAP — tentative gelée (conditionnelle)

Après le gel, et seulement après, tentative de récupération d'une
table somatique par organoïde mappable par identifiant DAC, dans
cet ordre (chaque tentative consignée avec son issue exacte,
succès ou échec, URL et SHA le cas échéant) :

1. **Source Data de la Fig. 6** (panneau supérieur : mutations
   germinales et somatiques par organoïde) — fichier « Source Data »
   de l'article, URL à relever sur la page de l'article au moment
   de la tentative (motif Springer static-content, MOESM suivant).
2. **Autres Supplementary Data (MOESM1–MOESM12)** — en particulier
   toute table WGS des 69 organoïdes (mutations somatiques KRAS /
   nombre de copies 9p21-MTAP) ; chaque fichier examiné est nommé,
   son contenu utile (ou son absence d'utilité) est consigné.
3. Aucune autre source (pas de demande aux auteurs, pas de dépôt
   tiers, pas d'inférence depuis la Fig. 6b en image).

**Critère de recevabilité de la table (gelé) :** statut KRAS
(mutant / sauvage, allèle si disponible) et/ou statut MTAP
(délétion / intact, ou nombre de copies) pour **≥ 40 des 46 PDO
criblés**, mappage par identifiant DAC exact, sans ambiguïté,
sans imputation. Si la table est recevable → tests D3 (KRAS)
et/ou D4 (MTAP) courus (§6). **Si aucune table recevable n'est
obtenue → D3 et/ou D4 sont déclarés IMPOSSIBLES, avec la raison
exacte** (table absente / non mappable / couverture < 40/46) —
c'est un verdict, pas un échec caché. L'absence de table MTAP est
l'issue attendue (MTAP n'est nommé nulle part dans l'article) ;
elle sera mesurée, pas supposée.

## 5. Construction des flux — paire pipeline exploratoire

Script neuf `build_fluxes_884_chen.py` (SHA noté), copie de travail
`data/Chen2025_MOESM13_SupplData10.xlsx` → CSV de flux.

- **Lignes :** les 46 PDO, **ordonnés par AUC Gemcitabine
  croissante** (le plus sensible d'abord) ; `step` = rang 0..45.
  L'ordre source n'est pas un ordre biologique ; l'ordre par
  Gemcitabine est l'axe testé (la sensibilité à la gemcitabine
  ordonne-t-elle les autres drogues ?). Aucun tri secondaire.
- **Flux :** les 62 autres drogues, AUC publiées, dans l'ordre
  MOESM13 (§2.1). Aucune transformation, aucune imputation
  (0 NaN), aucune exclusion (le plafond 0,9985714… est conservé
  tel quel — c'est une valeur publiée, pas une erreur).
- **Contrôle :** `step` (rang Gemcitabine). Le contrôle n'est
  JAMAIS un flux : pas de doublon. La Gemcitabine elle-même
  n'est pas un flux.
- **Cible :** défaut du pipeline (première colonne numérique hors
  contrôle, comme au §8.79 : PGC) — ici APR-246, première drogue
  MOESM13 hors Gemcitabine. Notée dans l'extraction, non choisie
  à la main.
- **Nul :** bloc des flux permuté par lignes, graine 42, `rng(42)`,
  contrôle (`step`) intact — même convention que les paires V1
  (§8.56.8, PROTOCOL_phase2 §2). Le nul est un échantillon
  hypothétique, pas une mesure.
- **Sorties :** `pdac_884_chen_fluxes.csv` (+ `_nul.csv`).
  Colonnes : `step` + 62 flux. SHA-256 consignés.
- **Statut de la paire (gelé) :** n = 46. Le minimum fast v6.2 est
  40 (`min_len: 40`, code v6.2 ligne 243) — la paire est
  techniquement courable, contrairement au pilote v5.9.4 (minimum
  50, bloqué). MAIS n = 46 < 50 (plancher du pilote, repris ici) :
  **paire EXPLORATOIRE, hors compte A2, jamais présentée comme une
  paire principale ni comme une confirmation.** L7a peut être
  indisponible/NaN sous n = 75 (précédents §8.8, §8.79) — descriptif
  seulement, jamais décisif.

## 6. Tests directs (gelés avant tout calcul)

Tous les tests sont calculés par le script neuf
`direct_tests_884_chen.py` (SHA noté), sur les valeurs MOESM13
telles que publiées. Sens des AUC : **AUC basse = sensible**
(l'article : « A low z-score or blue indicates high sensitivity » ;
les AUC basses sont les sensibles). Tous les p sont bilatéraux.
Correction FDR = Benjamini-Hochberg.

- **D1 — Co-sensibilité à la gemcitabine (toujours couru).**
  Pour chacune des 62 autres drogues : Spearman (AUC drogue,
  AUC Gemcitabine), n = 46 paires complètes. FDR BH sur 62.
  **Hit : FDR < 0,05.** Sens : rho > 0 = les PDO sensibles à la
  gemcitabine le sont aussi à la drogue. Table complète sans
  sélection ; top-10 par |rho| rapporté avec p brutes et FDR.
- **D2a — Réplication du contrôle positif Olaparib / BRCA2
  (toujours couru, un seul test pré-enregistré).** Olaparib AUC,
  BRCA2-mutants n = 6 (DAC102, DAC58, DAC81, DAC85, DAC53, DAC4 —
  nommés dans l'article) contre n = 40 autres. Mann-Whitney
  bilatéral. **Hit : p < 0,05** (pas de FDR : un seul test,
  réplication d'une affirmation nommée). Sens attendu : mutants
  plus sensibles (AUC plus basse). DAC76 et DAC99 (Olaparib-
  sensibles sans BRCA1/2 selon l'article) sont rapportés
  descriptivement (rangs d'AUC Olaparib), pas testés.
- **D2b — CFTR VUS_D chimio-résistants (toujours couru).**
  Les 5 nommés (DAC13, DAC73, DAC110, DAC32, DAC30) contre n = 41,
  Mann-Whitney bilatéral sur les 63 drogues, FDR BH sur 63.
  **Hit : FDR < 0,05.** Sens attendu (article) : résistants
  (AUC plus haute). Le sous-ensemble « chimiothérapie n = 8 »
  n'est PAS identifiable dans MOESM13 (aucun drapeau) : aucun
  sous-test chimiothérapie inventé — la limite est nommée.
- **D2c — Volet CFTR (conditionnel §4).** Si la Source Data
  identifie les 4 PDO CFTR-mutants parmi les 15 du volet CFTR :
  Wilcoxon bilatéral (comme l'article) sur les 5 correcteurs
  (Tezacaftor, Lumacaftor, FDL169, Galicaftor, Elexacaftor),
  n = 4 contre n = 11, p brutes rapportées face aux p de
  l'article (0,006 / 0,005 / 0,006 / 0,016 / 0,002). Sinon
  IMPOSSIBLE, raison nommée. Jamais de paire pipeline (n = 15).
- **D3 — Drogue × KRAS (conditionnel §4, table recevable).**
  Mann-Whitney bilatéral par drogue, KRAS-mutant contre
  KRAS-sauvage, 63 drogues, FDR BH sur 63. **Hit : FDR < 0,05.**
  Focus pré-enregistré, rapporté même si NS : MRTX849 et AMG510
  (inhibiteurs KRAS G12C ; p brutes citées). Si l'allèle G12C est
  connu : sous-test descriptif G12C contre reste (aucun hit
  déclaré si n_G12C < 5 — effectif nommé).
- **D4 — Drogue × MTAP (conditionnel §4, table recevable).**
  Même structure que D3, groupes MTAP-délété contre intact,
  63 drogues, FDR BH sur 63. **Hit : FDR < 0,05.** Focus
  pré-enregistré : inhibiteurs PRMT5 / MAT2A / vopimetostat —
  **absents des 63** (vérifié §2.1) : l'absence est constatée,
  aucun test sur eux n'est possible ; si un composé PRMT5
  apparaissait dans une table étendue, il serait rapporté.
  Si la table MTAP est absente → D4 IMPOSSIBLE, raison nommée.
- **D5 — Appui pipeline (descriptif, ne décide pas).** Sur les
  CSV de flux du chantier (réel + nul graine 42) : Spearman de
  chaque flux avec le pas (ordre Gemcitabine), réel contre nul ;
  |rho| moyen, Δrho médian, nombre de Δrho positifs (sur 62),
  table complète sans sélection. d de Cohen marginal des 62 flux
  (réel contre nul) : **attendu 0,0000 pour les 62** (le nul est
  une permutation des lignes, chaque flux garde exactement ses
  46 valeurs) — il valide la construction du nul, il ne mesure
  pas la séparation.

## 7. Runs v6.2 (mode fast)

- Lot : 2 runs — réel + nul — manifeste `manifest_v62_884.txt`,
  lanceur reprenable existant `run_v62_lot.sh` (saute les sorties
  déjà complètes), journal `runs_v62_884.log` (SHA du pipeline
  en tête, exits consignés).
- Dossiers : `results_fast_v62_884_chen` et
  `results_fast_v62_884_chen_nul` (nuls frais éventuels :
  `results_fast_v62_884_chen_nul_s8841` / `..._s8842`).
- Lancement en `systemd-run --unit=v62-884chen --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance qui
  s'arrête d'elle-même à 2/2 (ou 4/4 si nuls frais). Ne JAMAIS
  supprimer le dossier d'un run en cours. Si la machine
  redémarre, reprise sans perte (SKIP des dossiers complets,
  jamais de relance à l'aveugle).
- SHA du pipeline revérifié avant ET après le lot.
- Durée attendue : ~2–3 min par run à n = 46, 11 flux (§8.79 :
  n = 63, ~2 min/run) — 62 flux peuvent allonger le run ;
  aucune limite de durée n'est un critère d'arrêt.
- Si exit ≠ 0 : verdict = blocage technique, exit et queue de
  log cités, aucun paramètre changé, aucune relance déguisée.

## 8. Critère de passage — GELÉ avant tout run

**La paire PASSE si et seulement si :**
`d_maxsep = maxsep_R − maxsep_N > 0,07` (plancher, en unités |d|)
**ET** `d_maxsep > 0` (positif — impliqué par > 0,07, mais consigné
séparément comme au §8.56).

`maxsep` = `best_config.metrics.max_separation`, |d de Cohen|
maximal du scan, lu sur le best_config ANCIEN (sélection par
l'ancien composite) — mêmes définitions que §8.56.2. Le seuil MC,
la cascade, S_sep, Delta, L7a sont inchangés par construction.

**Catégories de verdict (gelées) :**
- **CONFIRME (exploratoire)** : `d_maxsep > 0,07` — la paire
  exploratoire passe ; **hors compte A2** (reste 9/13, 11/13
  positifs) ; ne rouvre ni ne ferme aucune condition.
- **PARTIEL** : `0 < d_maxsep ≤ 0,07` — positif mais sous le
  plancher.
- **NON** : `d_maxsep ≤ 0` — négatif ou nul.

**Nuls frais (§5, règle gelée, comme §8.79 §3.5/§6).** La paire
graine 42 fait le verdict, dans tous les cas. Si `d_maxsep` est
PROCHE du plancher — `d_maxsep` dans [−0,07 ; +0,14[ — les
2 nuls frais (graines **8841** et **8842**, gelées ici avant tout
run, jamais utilisées dans ce projet) sont construits par la même
méthode et courus en runs frais. Lecture gelée : si les 3 écarts
sont > 0,07, le passage est dit « consolidé » ; si l'un des 3
est ≤ 0,07, le passage (ou l'échec) est dit « fragile,
non consolidé » — le verdict de la paire graine 42 n'est JAMAIS
changé par les nuls frais. Si `d_maxsep` est hors de
[−0,07 ; +0,14[, aucun nul frais n'est couru.

**Contrôles descriptifs (à publier, ne décident pas) :**
- `sep` compagnon (= maxsep/(1+maxsep)), ancien MC (secondaire),
  S_sep, Delta, L7a, cascade, falsification — affichés selon la
  convention §8.64.6 (maxsep principal, ancien MC secondaire,
  sep compagnon, mention de fragilité en tête de table).
- Falsification : INDISPONIBLE sous n = 75 — n = 46 : noter
  « indisponible », ne pas imputer.
- Les tests directs D1–D4 ne changent pas le verdict du §8 :
  ils sont rapportés à côté, avec leurs propres critères (§6).
  Un D1/D3/D4 positif ne « confirme » pas la paire, et un
  D1/D3/D4 négatif ne l'invalide pas — ce sont deux lectures
  différentes de la même matrice.

## 9. Extraction et vérification

1. Extracteur propre du chantier, `extract_884.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_879_c3.py`) ; lit `maxsep`, `mc_score`,
   `stability`, `ssep`, `delta`, `l7a`, cascade, falsification
   dans les 2 (ou 4) `master_results.json` ; sorties
   `extract_884.json` / `extract_884.csv`.
2. Second calcul indépendant : relecture directe des
   `master_results.json` par un chemin distinct (script
   `verify_884.py`, SHA noté) — `maxsep` et ancien MC
   recoupés à 0,0 exact ; tout écart = résultat à
   diagnostiquer, pas un bruit. Les chiffres des tests directs
   D1–D4 sont re-vérifiés par un second calcul indépendant
   (script `verify_884_direct.py`, SHA noté : relecture des
   CSV + recalcul Spearman/Mann-Whitney/FDR par un chemin
   distinct — scipy d'un côté, implémentation rang-moyenne
   indépendante de l'autre, accord exigé à 1e-9 près sur rho
   et à l'unité près sur les comptes FDR).
3. SHA-256 de v6.2 revérifié après travaux, inchangé.
4. Aucun résultat d'une autre expérience n'est importé comme
   verdict : les écrans PRISM/GDSC2 (§8.7, §8.40), le pilote
   Chen (0 run), les p de l'article (D2a/D2c : réplications
   à re-mesurer ici) ne prédisent rien — seuls les chiffres
   mesurés sur les runs et calculs du présent chantier font
   le verdict.

## 10. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et le
  jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict.
- Un nul qui invalide une piste est un résultat ; un échec du lot
  est un verdict, pas un échec caché.
- Ne jamais présenter une lecture préliminaire comme un verdict.
- Aucun consensus exigé entre flux ou contrôles ; aucune
  affirmation clinique — l'étude porte sur l'instrument et sur
  des écrans ex vivo, pas sur un traitement.
- Ne jamais présenter cette paire exploratoire (n = 46, hors A2)
  comme une paire principale ni comme une confirmation.

## 11. Livrables

- Ce protocole gelé (`PROTOCOL_chen2025_drogue_884.md`, SHA à
  noter après écriture).
- `PROVENANCE_884.md` (source, auteur, date, dépôt, URL, SHA-256
  de MOESM13 et des CSV construits, effectifs, exclus, identification
  des drogues et des PDO, issue exacte des tentatives §4).
- `build_fluxes_884_chen.py` + CSV de flux (`pdac_884_chen_*`,
  SHA consignés).
- `direct_tests_884_chen.py` + sortie, `verify_884_direct.py` +
  sortie de vérification.
- `manifest_v62_884.txt`, `runs_v62_884.log`, dossiers
  `results_fast_v62_884_chen_*`, `extract_884.json` / `.csv`,
  `verify_884.py` + sortie de vérification.
- §8.84 dans le FICHIER SÉPARÉ
  `section_8.84_chen2025_drogue.md` (verdict d'abord, une phrase ;
  chiffres ensuite ; détail complet après ; provenance nommée
  partout ; statut exploratoire hors A2 dit explicitement ;
  D3/D4 : verdicts ou impossibilité avec la raison exacte).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin du protocole gelé §8.84 (lot drogue Chen 2025). —
