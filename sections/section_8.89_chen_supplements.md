### 8.89 Suppléments Chen non téléchargés (MOESM1, MOESM2, MOESM16) et dépôts : aucune table par-PDO KRAS / MTAP nulle part — piste fermée (21 novembre 2026)

Piste 3 du lot du 21 nov. 2026 ; protocole gelé 21 nov. 2026 ~10h15
EST avant tout téléchargement nouveau, toute copie et tout calcul
(`PROTOCOL_chen_supplements_889.md`, SHA `d4296ddd…07de792b`,
feu vert de Zackary 21 nov. 2026 10h07) ; provenance
`PROVENANCE_889.md`.

## Verdict d'abord

**PISTE FERMÉE — aucune table par-PDO (KRAS, MTAP, ou autre
variable recevable) n'existe dans les trois derniers suppléments
Chen (MOESM1, MOESM2, MOESM16, tous téléchargés et vérifiés
ici) ni dans les dépôts consultables : les tests directs
drogue × KRAS (D3) et drogue × MTAP (D4) restent IMPOSSIBLES,
et la question de savoir si les deux hits du §8.84 (paclitaxel,
mitomycine C) survivent quand on fixe KRAS / MTAP reste sans
réponse — pas tranchée, pas négative. La seule variable
par-organoïde nouvelle, le statut CFTR MT/WT de la Fig. 14c
(MOESM1), est non recevable comme base de test (38/46 PDO
criblés couverts, seuil gelé 40 ; MT n = 4 ; définition en
conflit avec la Fig. 6e pour DAC_24 et DAC_84) : aucun test
analogue n'a été couru dessus. Le §8.84 est inchangé (paire
exploratoire CONFIRME consolidée, hors A2) ; A2 inchangé.**

| Porte (protocole §3/§4/§6, gelé) | Exigé | Mesuré 21 nov. 2026 | Sort |
|---|---|---|---|
| Inventaire exhaustif des suppléments | MOESM1–17, aucun autre | **17 fichiers, MOESM18 absent (HTTP 403, aucun fichier servi)** | **COMPLET** |
| Fichiers déjà détenus re-vérifiés | SHA PROVENANCE_884 | **13/13 + MOESM13 identiques** | **PASSE** |
| MOESM1 / 2 / 16 téléchargés + hachés | HTTP 200, SHA consignés | **200 / 200 / 200 ; 24 268 877 / 4 586 550 / 3 947 814 o** | **PASSE** |
| Table KRAS par PDO recevable (≥ 40/46) | table ≥ 40/46 | **aucune — 0 statut KRAS par PDO dans les 17 suppléments** | **ABSENTE** |
| Table MTAP par PDO recevable (≥ 40/46) | table ≥ 40/46 | **aucune — « MTAP » 0 occurrence dans tout l'article** | **ABSENTE** |
| Autre table par-PDO recevable | table ≥ 40/46 | **aucune table ; Fig. 14c : figure, pas table, 38/46 < 40** | **ABSENTE** |
| T1/T2/T3 (condition : table recevable) | courus si table | **non courus — condition non remplie** | **NON APPLICABLE** |
| Dépôts consultés | GSA-Human, MW, Code Ocean | **MW : lignées PANC-1, pas d'organoïdes ; GSA-Human : accès contrôlé, bloqué ; Code Ocean : code seulement** | **DOCUMENTÉS** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que
l'inventaire des données publiées de Chen et al. 2025 est
désormais exhaustif et vérifié fichier par fichier : 17
suppléments sur 17, plus les 4 dépôts cités — et qu'aucun ne
porte le statut KRAS ou MTAP par organoïde. Il dit aussi, en
passant, deux faits mesurés : l'organoïde KRAS p.G12C est bien
unique (les auteurs l'ont corrigé de « deux » à « un » dans
leur réponse aux rapporteurs, MOESM2), mais il reste sans
identifiant DAC ; et l'article porte deux définitions
incompatibles du « CFTR mutation MT » (Fig. 6e contre Fig. 14c).
Il ne dit pas que KRAS ou MTAP sont sans effet sur ces PDO :
sans table, la question est intestable ici, pas tranchée. Il ne
dit pas que les hits D1 sont faux : leur survie sous KRAS/MTAP
n'a pas pu être testée, elle n'a pas échoué.

## 8.89.1 — Ce qui a été fait (après le gel, dans l'ordre du protocole)

1. **Re-vérification des détenus (§3.1).** SHA-256 + taille
   recalculés pour MOESM3–MOESM15 et MOESM17
   (`chen884_scratch/`) et MOESM13 (`data/`) : **13/13 +
   MOESM13 identiques** aux empreintes PROVENANCE_884.
   Rien n'a été re-téléchargé.
2. **Téléchargements nouveaux (§3.2).** Exécution directe
   (curl), jamais systemd-run sans proxy : MOESM1
   (Supplementary Information, 24 268 877 o, SHA
   `4b70d25b…60aa61f`), MOESM2 (Peer Review File,
   4 586 550 o, SHA `ce939f22…65d67`), MOESM16 (Reporting
   Summary, 3 947 814 o, SHA `69a959c3…95c499`) — HTTP 200
   pour les trois. Sondes MOESM18 `.pdf` et `.xlsx` :
   HTTP 403, aucun fichier servi — l'inventaire MOESM1–17
   est complet.
3. **Examen (§3.3).** Script `examine_889.py` (SHA
   `ef282880…e3645`), sortie `examine_889.json` (SHA
   `0f828245…bef946`) : extraction de texte (`pdftotext
   -layout`), comptages exacts, lecture des 4 Supplementary
   Tables de MOESM1, des 17 Supplementary Figures, mesure
   de la barre d'annotation de la Fig. 14c sur le rendu
   200 dpi de la p. 21 (positions `pdftotext -bbox`),
   relecture de la Fig. 6e dans MOESM17, recoupement avec
   les 46 colonnes MOESM13.
4. **Dépôts (§3.4).** Pages publiques consultées :
   Metabolomics Workbench ST003734 (lue en direct),
   GSA-Human HRA005195 (tentée : échec réseau, sans statut
   HTTP — page live non confirmée, non répétée),
   Code Ocean 1432248 (tentée : HTTP 403, non répétée).
   Aucune demande d'accès, aucun compte créé, aucun
   téléchargement de données brutes contrôlées.

## 8.89.2 — MOESM1 : Supplementary Information (39 pages) — pas de table par-PDO

- **4 Supplementary Tables.** Table 1 : statistiques agrégées
  seulement (N = 458 découverte, N = 842 ; sexe, âge, IMC,
  diabète, pancréatite, tabac, alcool, antécédents, pathologie,
  grade, TNM) — aucune ligne par patient, aucun identifiant.
  Tables 2 et 3 : significativité statistique des comparaisons
  PANC-1 (Fig. 5) et AsPC-1 (Supp. Fig. 7) — des lignées, pas
  des organoïdes. Table 4 (« Small molecule screening data ») :
  métadonnées d'essai seulement (63+15 composés, 7
  concentrations, CellTiter-Glo, AUC GraphPad Prism 9,
  normalisation par le maximum ; taux de hits : correcteurs
  CFTR 26,7 %, inhibiteurs KRAS p.G12C 2,2 % = 1/46,
  HRD 13,0 %) — aucune valeur par PDO, aucun génotype.
- **17 Supplementary Figures (Fig. 1–17), 1 Supplementary
  Note.** Comptages exacts : `DAC` 59, `KRAS` 6, `MTAP` 0,
  `9p21` 0, `G12C` 2, `CDKN2A` 0. Les 6 `KRAS` : 4 libellés de
  voies `HALLMARK_KRAS_SIGNALING` (Supp. Fig. 15,
  enrichissement, pas un génotype) et 2 dans la Table 4.
  Les seuls `DAC` du fichier sont dans la Fig. 14c (57) et
  le mot `PDAC` de la Table 1.
- **Supp. Fig. 14c — la seule variable par-organoïde nouvelle.**
  Heatmap de 18 DEGs, 57 organoïdes en colonnes, barre
  d'annotation `CFTR mutation` MT/WT. Ordre visuel vérifié
  par `pdftotext -bbox` (x croissant) ; mesure de la barre
  (rendu 200 dpi) : segment teal x_pts 51,9–74,8, orange dès
  74,9, pas des colonnes 5,719 pts → (74,9−51,9)/5,719 =
  **4,02 colonnes** : MT = **DAC_13, DAC_30, DAC_72,
  DAC_73** ; WT = les 53 autres. Recoupement avec les 46
  PDO criblés : **38/46** — non couverts : DAC_99, DAC_102,
  DAC_103, DAC_104, DAC_109, DAC_110, DAC_114, DAC_115.
  Les 4 MT sont tous parmi les 46 criblés.
- **Conflit interne mesuré.** La Fig. 6e de la Source Data
  (MOESM17, relue ici : 15 PDO, MT = DAC13, DAC24, DAC72,
  DAC84 ; WT = 11 autres — identique au §8.84) définit
  `CFTR mutation MT` différemment : **DAC_24 et DAC_84 sont
  MT en Fig. 6e mais WT en Fig. 14c** ; DAC_30 et DAC_73
  sont MT en Fig. 14c mais absents des 15 de la Fig. 6e.
  Seuls DAC_13 et DAC_72 sont MT dans les deux figures.
  Les deux groupements ne peuvent pas être vrais sous la
  même définition — les définitions de variants sous-jacentes
  ne sont pas publiées par PDO.
- **Supp. Fig. 15.** Cohortes découverte (tumeurs) et TCGA,
  annotations `CFTR expression` et `CFTR aaChange`
  (p.C1355Y, p.E681V, p.L69F, p.R1097C) — des tumeurs de
  patients, pas des organoïdes, aucun identifiant DAC.
- **Non-recevabilité de la Fig. 14c (application du §4).**
  (a) Ce n'est pas une table, c'est une barre d'annotation
  de figure. (b) Couverture 38/46 < 40 (seuil gelé) — 8 PDO
  criblés non classés, dont DAC_110, porteur CFTR VUS_D
  nommé au §8.84 (D2b). (c) Effectif MT n = 4. (d) Définition
  en conflit avec la Fig. 6e pour DAC_24 et DAC_84.
  **Aucun test analogue n'a donc été couru dessus** (§5 :
  le test analogue est conditionné à une table trouvée ;
  §4 : couverture < 40/46 = non recevable). Courir un
  Mann-Whitney 4 contre 34 sur un groupement lu dans une
  figure, contre un groupement contradictoire du même
  article, serait inventer un résultat, pas en mesurer un.

## 8.89.3 — MOESM2 : Peer Review File — un seul organoïde G12C, toujours sans DAC

- Comptages exacts : `DAC` 2, `KRAS` 15, `MTAP` 0, `9p21` 0,
  `G12C` 7, `CDKN2A` 1, `Supplementary Table` 0. Les 2 `DAC`
  sont dans une formule de politesse du rapporteur n° 3 ;
  les 15 `KRAS` / 7 `G12C` sont de la discussion
  d'évaluation, aucune table.
- Point décisif (rapporteur n° 2, point 13) : « In Fig.6b,
  there seems to be only one sample with a KRAS G12C
  mutation. However, according to line 363-364, two organoids
  bore the mutation. Please clarify this inconsistency. »
  Réponse des auteurs (2.13) : « We corrected this mistake
  in Lines 363-364: “One organoid bearing the KRAS p.G12C
  mutation exhibited sensitivity to AMG510 and MRTX849.” »
  **L'organoïde KRAS p.G12C est unique — et toujours sans
  identifiant DAC nommé.** Le test ciblé T4 (rangs d'AUC
  AMG510 / MRTX849 de ce PDO) reste impossible.

## 8.89.4 — MOESM16 : Reporting Summary (4 pages) — formulaire, aucune donnée

- Formulaire Nature Portfolio, PDF image (sans texte
  extractible ; les 4 pages ont été rendues en images et
  lues une par une). Sections : Statistics, Software and
  code, Data (reprend la déclaration de disponibilité :
  HRA005195, HRA010277, ST003734, Code Ocean 1432248),
  Research involving human participants, Life sciences study
  design, Antibodies, Eukaryotic cell lines, Animals,
  Plants, Flow Cytometry. **Aucune table de données, aucun
  génotype, aucun identifiant DAC.**

## 8.89.5 — Dépôts : un dépôt ouvert sans organoïde, deux accès contrôlés, du code seulement

| Dépôt | Statut mesuré 21 nov. 2026 | Table par-PDO ? |
|---|---|---|
| GSA-Human HRA005195 (WGS/WES/RNA-seq découverte + WGS 69 organoïdes) | Accès contrôlé (données humaines ; MTA pour partager, selon l'article). Page publique tentée : échec réseau, sans statut HTTP — page live non confirmée. Aucune demande d'accès, aucun compte, aucun téléchargement de lectures brutes. Des lectures brutes, pas une table : KRAS/MTAP n'y seraient lisibles qu'après ré-analyse des WGS. | Non — et non téléchargeable ici |
| GSA-Human HRA010277 (RNA/ATAC organoïdes + RNA lignées) | Même statut, mêmes limites. Page non consultée (même échec, non répété). | Non |
| Metabolomics Workbench ST003734 (PR002320, DOI 10.21228/M8R83M) | Page lue en direct : **lipidomique de la lignée PANC-1**, 52 échantillons (CFTR OE / EV / p.L88X / p.E681V / p.C1355Y + QC) — pas des organoïdes, aucun DAC, aucun KRAS/MTAP. | Non |
| Code Ocean 1432248 (DOI 10.24433/CO.1432248.v1) | **Code seulement** (article § Code availability ; MOESM16 p. 1). Page DOI tentée : HTTP 403, non répétée ; la qualification repose sur l'article et MOESM16. | Non |

## 8.89.6 — Ce que ce lot change, et ce qu'il ne change pas

- **D3/D4 restent IMPOSSIBLES** — désormais sur la base de
  l'inventaire complet : 17/17 suppléments vérifiés
  (MOESM1–17) + 4 dépôts consultés ou qualifiés. Le §8.84
  disait « aucune table dans les 12 Supplementary Data ni
  dans la Source Data » ; le §8.89 étend ce verdict à
  **toutes les données publiées de Chen et al. 2025**.
- **A2 inchangé** (paire Chen hors compte, exploratoire) ;
  §8.84 inchangé (paire CONFIRME consolidée, D1/D2a/D2c
  inchangés). Aucun run pipeline dans ce chantier.
- **Les 2 hits D1 ne sont ni confirmés ni infirmés sous
  KRAS/MTAP** : T3 n'a pas été couru (condition non
  remplie), la question reste ouverte.
- **Pistes ouvertes (pas des verdicts) :** (a) demander aux
  auteurs une table KRAS/MTAP par DAC pour les 46 PDO
  criblés — seule voie directe vers D3/D4 ; (b) accès
  approuvé GSA-Human (demande + MTA) puis ré-analyse des
  WGS des 69 organoïdes pour appeler KRAS (dont G12C) et
  le nombre de copies 9p21/MTAP par DAC — travail lourd,
  hors de ce chantier, à décider par Zackary ; (c) la
  contradiction Fig. 6e / Fig. 14c sur le statut CFTR
  (DAC_24, DAC_84) mériterait la même table des auteurs —
  elle ne change rien à D3/D4.
- **C3 reste LEVÉE** (elle l'était depuis le §8.71) ; ce
  chantier ne rouvre rien.

## 8.89.7 — Provenance (complète, liens cliquables)

- Article : Yin, X. *et al.*, *Nat. Commun.* **16**, 2214 (2025),
  DOI 10.1038/s41467-025-57520-3,
  https://doi.org/10.1038/s41467-025-57520-3 (CC BY-NC-ND 4.0).
- MOESM1 (Supplementary Information) :
  https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM1_ESM.pdf
  — 24 268 877 o, SHA-256
  `4b70d25b078f21cc2612963d807e9a1ab27782ccc8aa721482043b16e60aa61f`.
- MOESM2 (Peer Review File) :
  https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM2_ESM.pdf
  — 4 586 550 o, SHA-256
  `ce939f2227d92a7147e3d5c6681bd9fe0e8ab70c5a8c7fad99695016bfd65d67`.
- MOESM16 (Reporting Summary) :
  https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM16_ESM.pdf
  — 3 947 814 o, SHA-256
  `69a959c3ff56eff607dfa561b8734f537780e16dcf8376ade26c1b0afb95c499`.
- MOESM3–MOESM15, MOESM17 : SHA re-vérifiés identiques à
  PROVENANCE_884 (§3) ; MOESM13 :
  `0e009cd5…5340`, 35 732 o.
- Dépôts : GSA-Human HRA005195 et HRA010277
  (https://ngdc.cncb.ac.cn/gsa-human) ; Metabolomics
  Workbench ST003734
  (https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST003734,
  projet PR002320, DOI 10.21228/M8R83M) ; Code Ocean 1432248
  (https://doi.org/10.24433/CO.1432248.v1).
- Protocole gelé : `PROTOCOL_chen_supplements_889.md`, SHA-256
  `d4296ddd0c43b44c3a4e943ff12b73cf2eca4cc6960f2eb4f9a3c93a07de792b`.
- Provenance : `PROVENANCE_889.md`, SHA-256
  `bd33f8da8c08d8ee37ad6523eb80d398200eb443e3720372fd0b6a89ef37e4f1`.
- Examen : `chen889_scratch/examine_889.py` SHA
  `ef2828805ef6e64f88a14f10575c54901619fa689dbc97ccbe483678a51e3645`,
  `examine_889.json` SHA
  `0f828245cfad1a2b996c61886aef2f54557e1576035f684668890e9e3aadadb0`.

## 8.89.8 — Ce qui manque

- Table KRAS par PDO (46 DAC) : absente partout ; table MTAP
  par PDO : absente partout (`MTAP` 0 occurrence dans
  l'article entier) ; identifiant DAC de l'organoïde G12C
  unique : absent partout ; T1/T2/T3 non courus (condition
  non remplie) ; pages live GSA-Human non confirmées (échec
  réseau) et page Code Ocean non consultée (HTTP 403) —
  leurs qualifications reposent sur l'article et MOESM16,
  pas sur les pages live. Tous les SHA de cette section sont
  relevés des fichiers et re-vérifiés ; aucun nombre n'est un
  placeholder.

— Fin de la §8.89. —
