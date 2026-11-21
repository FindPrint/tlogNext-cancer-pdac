# PROVENANCE_884 — Lot drogue Chen 2025 (§8.84)

**Date :** 21 novembre 2026, ~14h00–15h00 EST. **Agent :** TagPrint
(subagent, piste 1). **Chantier :** §8.84.
**Protocole gelé avant tout téléchargement nouveau, toute copie et
tout calcul :** `PROTOCOL_chen2025_drogue_884.md`,
SHA-256 `62ee265e2e8b71d0970b3dc58e2d8cdfe8c8aad727b43c687a6b37230fd13c00`.
**Pipeline :** v6.2, SHA
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
— vérifié avant et après le lot, jamais modifié.
**Livre blanc local vérifié :**
`~/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md`,
SHA-256 (16 premiers caractères) `ef511c1049018c6b`, §8.1–§8.83,
20 256 lignes.

## 1. Source

- Article : Yin, X., Shen, H., Wang, H. *et al.* « Pathogenic germline
  variants in Chinese pancreatic adenocarcinoma patients »,
  *Nature Communications* **16**, 2214 (2025). Reçu 21 janv. 2024,
  accepté 25 févr. 2025, publié 5 mars 2025.
  DOI 10.1038/s41467-025-57520-3.
  URL : https://doi.org/10.1038/s41467-025-57520-3.
  Licence CC BY-NC-ND 4.0. Auteurs correspondants : Haojie Jin,
  Hongbo Yang, Jing Li, Gang Jin. Cohorte : Shanghai Changhai Hospital.
- Fichier source : Supplementary Data 10 =
  `41467_2025_57520_MOESM13_ESM.xlsx` (MOESM13).
  URL complète :
  `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM13_ESM.xlsx`
- Empreinte : 35 732 o, SHA-256
  `0e009cd56d2f6c25b0b355590becc4abfee3e1080633173bc33606d1bf325340`
  — IDENTIQUE à l'empreinte du §8.79 (PROVENANCE_879 §1.1).
  Copie de travail : `data/Chen2025_MOESM13_SupplData10.xlsx`
  (copie du fichier déjà détenu et vérifié au §8.79, scratch
  `/tmp/b879/` ; SHA re-vérifié après copie, conforme).
- Page article relue le 21 nov. 2026 (texte intégral, 1 450 lignes) :
  section « Drug screening for pathogenic germline mutations »
  (63 composés, 46/69 organoïdes criblés en duplicata, > 7 000
  mesures ; 7 concentrations ; CellTiter-Glo après 5 jours ;
  AUC GraphPad Prism 9, AUC normalisée = AUC / AUC maximale de
  la drogue ; viabilités au-dessus de la ligne de base plafonnées
  à 100) et Methods « Organoid drug screening ».

## 2. Nature des lignes

- Feuille « All Drugs AUC » : 63 drogues en lignes (colonne
  `cluster` descriptive, exclue des flux), 46 PDO en colonnes
  (`DAC_61 … DAC_115`), valeurs = AUC normalisée publiée.
  63 × 46 = 2 898 cellules, **0 NaN** ; min 0,0000 (Valproic acid,
  DAC_22) ; médiane 0,9107 ; max 1,1746 (CCT245737).
  **8 drogues avec max > 1** (Sorafenib 1,0564 ; Lenvatinib 1,0496 ;
  AZD6738 1,0986 ; AZD5363 1,1668 ; CCT245737 1,1746 ; Palbociclib
  1,0929 ; Everolimus 1,1018 ; Rapamycin 1,1085) — la normalisation
  « par le maximum » telle que décrite ne plafonne donc pas les
  valeurs à 1 dans le fichier déposé ; anomalie consignée, aucune
  correction appliquée. Valeur plafond répétée
  0,9985714285714287 (= 699/700) dans 362/2 898 cellules (12,5 %),
  concentrée dans Valproic acid (36/46), APR-246 (32/46),
  Dacarbazine (29/46), Hydroxychloroquine (27/46), Pemetrexed
  (25/46), Olaparib (20/46) — lue comme un plafond de non-réponse,
  conservée telle quelle.
- Gemcitabine (ancre) : min 0,1399 / médiane 0,4384 / max 0,8167 /
  écart-type 0,1882 (ddof = 1, n = 46) ; PDO le plus sensible
  DAC_1 (0,1399) ; le plus résistant DAC_110 (0,8167).
- Feuille « CFTR Drugs AUC » : 15 drogues CFTR × 15 PDO, 0 NaN,
  min 0,6462 / max 1,0000.
- **Forme des identifiants :** l'article et la Source Data écrivent
  DAC102, MOESM13 écrit DAC_102 — même identifiant, underscore en
  plus dans le fichier. Mappage par suppression de '_' (bijectif
  sur les 46). Les 6 organoïdes BRCA2 nommés (DAC102, DAC58, DAC81,
  DAC85, DAC53, DAC4) et les 5 CFTR VUS_D nommés (DAC13, DAC73,
  DAC110, DAC32, DAC30) sont tous présents parmi les 46 colonnes.
- Les CSV de flux du chantier (`pdac_884_chen_fluxes.csv`,
  `pdac_884_chen_fluxes_nul.csv`) sont des transpositions des AUC
  publiées, ordonnées par AUC Gemcitabine croissante ; aucune
  transformation, aucune imputation. Le nul (graine 42) est un
  échantillon hypothétique (lignes permutées), pas une mesure.

## 3. Tentative §4 — table par-PDO KRAS / MTAP (après le gel)

Tentatives effectuées le 21 nov. 2026, en exécution directe
(jamais en systemd-run sans proxy), consignées avec leur issue :

1. **Source Data, Fig. 6 (MOESM17)** — téléchargée :
   `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM17_ESM.xlsx`,
   5 454 570 o, SHA-256
   `917a1011426c5ee749343ccabf8126e35923a65c4719ec929f84aa29a511f7b1`.
   Contenu : feuille « Figure 6 », 121 lignes × 151 colonnes.
   Fig. 6a : disponibilité WGS/RNA/ATAC/Drug Screen/CFTR_drug par
   organoïde (0/1, sans identifiant de statut). Fig. 6b : **Z-scores
   des AUC seulement** (63 drogues × 46 PDO), aucune ligne
   d'annotation mutationnelle. Fig. 6c : Z-scores CFTR (15 × 15).
   Fig. 6d : courbes dose-réponse (viabilités brutes). Fig. 6e :
   **statut CFTR par PDO pour les 15 du volet CFTR** — MT :
   DAC13, DAC24, DAC72, DAC84 (4) ; WT : DAC18, DAC2, DAC20,
   DAC29, DAC31, DAC32, DAC34, DAC5, DAC53, DAC54, DAC6 (11) —
   avec les AUC des 5 correcteurs. **Aucune ligne KRAS, aucune
   ligne MTAP dans toute la feuille.**
   Recoupement : AUC Fig. 6e vs MOESM13 feuille CFTR, 75/75 paires,
   écart max 4,96e-08 — les deux fichiers portent les mêmes AUC.
2. **Description des suppléments (MOESM3)** — téléchargée :
   140 637 o, SHA-256
   `3a84243b7b4c3bbab172a4ead61725663fd076cd00664091ea0fad3c5313c569`.
   Aucune des Data 1–12 n'est une table somatique par organoïde :
   Data 1 = cohortes 1 123 patients (clinique) ; Data 2 = SNP
   contrôles sains ; Data 3 = variants germinaux délétères,
   cohorte découverte ; Data 4 = liste des 150 CSG ; Data 5 =
   variants germinaux, validation + validation fonctionnelle ;
   Data 6 = fréquences BRCA2 ; Data 7–9 = CFTR ; Data 10 = écran
   de drogues (MOESM13) ; Data 11 = amorces CFTR ; Data 12 =
   métabolites.
3. **Autres Supplementary Data (MOESM4–MOESM12, MOESM14, MOESM15)**
   — tous téléchargés et examinés cellule par cellule
   (recherche `DAC`, `KRAS`, `MTAP` exacts) :
   - MOESM4 (Data 1) : 1 124 × 18, 0 DAC, 0 KRAS, 0 MTAP.
     Identifiants patients GN1, GN2, … (pas de DAC) ; aucune
     colonne KRAS/MTAP ; aucun mappage GN → DAC.
   - MOESM5 (Data 2) : 785 × 14, 0 DAC, 0 KRAS, 0 MTAP.
   - MOESM6 (Data 3) : 8 408 × 38, 0 vrai DAC (4 « HDAC »,
     faux positifs de la recherche), 0 KRAS, **1 MTAP** : une
     variante germinale VUS_D missense p.P41L (chr 9:21816715,
     C>T) chez un patient de la cohorte découverte (échantillon
     EN233) — une variante germinale, pas un statut de délétion
     MTAP, pas un PDO.
   - MOESM7 (Data 4) : liste des 150 CSG ; KRAS et MTAP y
     figurent comme simples entrées de liste (KRAS : « Driver
     Genes With Frequent Somatic Mutations » ; MTAP : 9p21.3,
     syndrome DMS-MFH) — pas de statut par patient.
   - MOESM8 (Data 5) : 4 145 × 25 (+ listes PANEL1/PANEL2),
     0 vrai DAC, 0 KRAS (hors listes de gènes), 1 MTAP (liste).
   - MOESM9 (Data 6) : 70 × 8 et 187 × 8, 0 partout.
   - MOESM10 (Data 7) : 69 × 20 (sites de mutation CFTR),
     0 partout.
   - MOESM11 (Data 8) : 21 × 8, 0 partout.
   - MOESM12 (Data 9) : 20 × 14, 0 partout.
   - MOESM14 (Data 11) : 15 × 3, 0 partout.
   - MOESM15 (Data 12) : 535 × 47, 0 partout.
   SHA-256 : MOESM4 `09968fbc…171dfd`, MOESM5 `c759ab51…ef25eb`,
   MOESM6 `af69c390…01392`, MOESM7 `bf5cab3f…a194fe`,
   MOESM8 `9b440dd9…d5e389`, MOESM9 `017632df…1957`,
   MOESM10 `2e65713b…48ccaa`, MOESM11 `da2c4583…ff25c`,
   MOESM12 `70a0ff03…904b`, MOESM14 `55c35f4a…3864`,
   MOESM15 `10ce1ef8…7a44`.
   - Figure 1 de la Source Data (oncoprint, 208 × 124) : une
     ligne KRAS (somatique) existe, mais **aucun identifiant DAC
     dans toute la feuille** — les 122 colonnes sont des tumeurs
     de la cohorte découverte, sans mappage vers les organoïdes.

**Conclusion §4 (mesurée, pas supposée) :**
- **D3 (drogue × KRAS) : IMPOSSIBLE** — aucune table du statut
  KRAS somatique par PDO dans les suppléments ni dans la Source
  Data ; l'article nomme un seul organoïde KRAS p.G12C sans
  identifiant DAC.
- **D4 (drogue × MTAP) : IMPOSSIBLE** — aucune table du statut
  MTAP (délétion / nombre de copies 9p21) par PDO ; MTAP n'est
  nommé dans l'article que comme gène de susceptibilité, jamais
  comme statut par organoïde.
- **D2c (volet CFTR) : POSSIBLE** — statut CFTR MT/WT des 15 PDO
  obtenu de la Source Data Fig. 6e (MT : DAC13, DAC24, DAC72,
  DAC84).

## 4. Antériorité et indépendance

- Pilote v5.9.4 (`pilot.md`, `run_chen.py`, dossier
  `universal-log-research`) : JAMAIS couru — bloqué avant tout
  run, N = 46 < 50 (minimum v5.9.4). 0 run, 0 résultat. Le pilote
  ne prédit rien ici.
- Écrans déjà négatifs, repris tels quels (jamais recalculés) :
  PRISM primaire 24Q2 (6 790 composés, 0 FDR < 0,05, FDR min
  0,959 — §8.7) ; PRISM secondaire 19Q4 (1 437, 0 FDR < 0,05,
  FDR min 0,625) ; GDSC2 (269, 0 FDR < 0,05, FDR min 0,561 /
  0,882 — §8.40.3).
- Les p de l'article (correcteurs CFTR : 0,006 / 0,005 / 0,006 /
  0,016 / 0,002, Wilcoxon) sont des RÉSULTATS RAPPORTÉS, re-mesurés
  ici (D2c) — pas des verdicts importés.
- Les 46 PDO sont des patients chinois distincts des cohortes
  TCGA / ICGC / GEO du projet (système d'identifiants DAC propre,
  aucune inclusion documentée ailleurs) ; limite déclarée : aucun
  identifiant commun n'existe entre les systèmes, donc pas de
  preuve par jointure.

## 5. Fichiers produits par ce chantier (à hasher après écriture)

- `~/workspace/runs/pdac-v6/section_8.84_chen2025_drogue.md`
- `~/workspace/runs/pdac-v6/PROTOCOL_chen2025_drogue_884.md`
  (SHA `62ee265e…fd13c00`)
- `~/workspace/runs/pdac-v6/PROVENANCE_884.md` (ce fichier)
- `~/workspace/runs/pdac-v6/data/Chen2025_MOESM13_SupplData10.xlsx`
  (SHA `0e009cd5…5340`, 35 732 o)
- `~/workspace/runs/pdac-v6/chen884_scratch/` (article.html,
  MOESM3_description.pdf, MOESM4–MOESM15.xlsx, MOESM17_sourcedata.xlsx)
- `~/workspace/runs/pdac-v6/build_fluxes_884_chen.py`
  (SHA `d37973c8…9cd`), `pdac_884_chen_fluxes.csv`
  (SHA `73fefc10…4554`), `pdac_884_chen_fluxes_nul.csv`
  (SHA `43866a01…200a`)
- `~/workspace/runs/pdac-v6/direct_tests_884_chen.py`
  (SHA `68811366…dd3`), `direct_tests_884_chen.json`
  (SHA `53602a86…dba`), `direct_tests_884_chen_D1.csv`,
  `direct_tests_884_chen_D2b.csv`
- `~/workspace/runs/pdac-v6/verify_884_direct.py`,
  `verify_884_direct.json`
- `~/workspace/runs/pdac-v6/extract_884.py` (SHA
  `1d5a25c93c1d92b5dc8121517772d7447423096692d1b5f1cd382cdd5394d363`),
  `verify_884.py` (SHA
  `19d778ed796cac911542525572692086628c9ec5b4568ef2b7fdfa60f3298c5a`),
  `manifest_v62_884.txt` (SHA
  `608d0a5f6226f5db35993b4ef582d2b1f674ac0185f8dd8bc85d8b25e5f18b7f`),
  `runs_v62_884.log` (SHA
  `1ef7edaa7c81f656c0415c4d8fbf338e3773b97421ba0ddd31cb0aec9e5b1f3d`),
  `manifest_v62_884_fresh.txt` (SHA
  `40ff4cb6c35ce7e68ff7521174726a1c02c1a0541bb6da384a8bb265f5e4f4d7`),
  `runs_v62_884_fresh.log` (SHA
  `1dcd14fcde0bc032c2e968f91e5861d67c7a0c83504b397776123ab6c4b10a48`),
  `results_fast_v62_884_chen`, `results_fast_v62_884_chen_nul`,
  `results_fast_v62_884_chen_nul_s8841`,
  `results_fast_v62_884_chen_nul_s8842`,
  `extract_884.json` (SHA
  `d5380813224462a372f5dfd7ecee630fafd0636a333c5819a6ab691474139b9e`) /
  `extract_884.csv` (SHA
  `622278cd5519734d9a71e2e1fd665931399ceceee2441eb774c6e700cff08d71`),
  `maxsep_884_verify.json` (SHA
  `7a6bc2022ec06f801e48426cf693a061647b239213499b8db4457c2d129aaf96`)
- `~/workspace/runs/pdac-v6/pdac_884_chen_fluxes_nul_s8841.csv` (SHA
  `09e8e31efdfcf5dc89d942a9c2f50a37a4e0e6b2f9a50a168114e78129206da7`),
  `pdac_884_chen_fluxes_nul_s8842.csv` (SHA
  `adc95aa8b411cc9598802ff0a81e76bbb12227bfdea11ecf85c7f54fd164dd3a`)
- `~/workspace/runs/pdac-v6/direct_tests_884_chen_D1.csv` (SHA
  `08573f5bd822b91e6ea4276dc79ead11225a2632033f20de263ec7bbb723c22e`),
  `direct_tests_884_chen_D2b.csv` (SHA
  `18e6455eff8c33f63413e0c965178d2afbf7acb18bbbc1144be55f105231f4c5`),
  `verify_884_direct.py` (SHA
  `dae9478e1c3be59f770352fdbb46793d7dec4f74c6bdcfb38c4836221fe05f3a`),
  `verify_884_direct.json` (SHA
  `f3786eccd78ad35fb5039bf406e5756dfc3a71a70e5ee31266db5b3cc77f4a22`)

## 6. Ce qui manque / limites

- Aucun statut KRAS ni MTAP par PDO dans les données publiées —
  D3 et D4 impossibles (voir §3) ; le lot ne teste donc pas
  l'hypothèse « drogue × KRAS » sur ces PDO, il la déclare
  intestable ici.
- n = 46 < 50 (plancher du pilote) : paire pipeline
  EXPLORATOIRE, hors compte A2, jamais une paire principale.
- Les AUC publiées portent un plafond répété (0,9985714…, 12,5 %
  des cellules) et 8 drogues dépassent 1 — valeurs conservées
  telles quelles, sans correction ; les tests de rang (Spearman,
  Mann-Whitney) sont robustes à ces plafonds, mais les médianes
  proches du plafond (ex. Olaparib reste 0,9984) doivent être
  lues comme « non-réponse plafonnée », pas comme une mesure fine.
- Le sous-ensemble « chimiothérapie n = 8 » de l'article n'est
  pas identifiable dans MOESM13 (aucun drapeau) : D2b teste les
  63 drogues, aucun sous-test chimiothérapie inventé.
- Vopimetostat, inhibiteurs PRMT5 et MAT2A absents des 63 drogues
  comme des écrans §8.40 — la sensibilité différentielle au
  vopimetostat lui-même reste intestable partout.
- Les réponses et fichiers MOESM4–MOESM17 sont conservés dans
  `chen884_scratch/` (données publiées, pas des mesures du chantier).
