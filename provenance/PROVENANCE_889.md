# PROVENANCE_889 — Suppléments Chen non téléchargés (§8.89)

**Date :** 21 novembre 2026, ~10h15–15h20 EST. **Agent :** TagPrint
(subagent, piste 3 du lot du 21 nov. 2026). **Chantier :** §8.89.
**Protocole gelé avant tout téléchargement nouveau, toute copie et
tout calcul :** `PROTOCOL_chen_supplements_889.md`,
SHA-256 `d4296ddd0c43b44c3a4e943ff12b73cf2eca4cc6960f2eb4f9a3c93a07de792b`.
**Feu vert de Zackary :** 21 nov. 2026, 10h07.
**Antériorité reprise telle quelle :** §8.84 (paire exploratoire
CONFIRME consolidée, d_maxsep +0,0982 ; D1 : paclitaxel
FDR 0,0191, mitomycine C FDR 0,0257 ; D2a/D2c répliqués ;
D3/D4 IMPOSSIBLES dans MOESM3–MOESM15 + MOESM17) ;
PROVENANCE_884 (SHA `1eb03395…bca43` après correction des
suffixes MOESM5/7/8, cf. §8.84 correction datée).

## 1. Source

- Article : Yin, X., Shen, H., Wang, H. *et al.* « Pathogenic germline
  variants in Chinese pancreatic adenocarcinoma patients »,
  *Nature Communications* **16**, 2214 (2025). Reçu 21 janv. 2024,
  accepté 25 févr. 2025, publié 5 mars 2025.
  DOI 10.1038/s41467-025-57520-3.
  URL : https://doi.org/10.1038/s41467-025-57520-3.
  Licence CC BY-NC-ND 4.0. Cohorte : Shanghai Changhai Hospital.
- Inventaire exhaustif des suppléments : page de l'article relue
  le 21 nov. 2026 (`chen884_scratch/article.html`, 734 178 o, SHA
  `b9ee6c7e6b47a8079c72c02ebb34cd6c9ecc17f565b0b23a47b13a4a393f4f4d`)
  — exactement MOESM1 à MOESM17, aucun MOESM18 dans le HTML.
  Confirmation par requête : MOESM18 `.pdf` et `.xlsx` retournent
  HTTP 403 (aucun fichier servi) le 21 nov. 2026 ~15h10 EST.
- Motif URL Springer :
  `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM{n}_ESM.{pdf,xlsx}`

## 2. Nouveaux téléchargements (exécution directe, jamais systemd-run sans proxy)

Téléchargés le 21 nov. 2026 ~15h10 EST, en exécution directe (curl),
dans `chen889_scratch/` (leçon AGENTS.md 2026-11-17 : les unités
systemd-run n'héritent pas du proxy d'egress) :

| Fichier | Taille | SHA-256 | HTTP |
|---|---|---|---|
| MOESM1 `41467_2025_57520_MOESM1_ESM.pdf` (Supplementary Information) | 24 268 877 o | `4b70d25b078f21cc2612963d807e9a1ab27782ccc8aa721482043b16e60aa61f` | 200 |
| MOESM2 `41467_2025_57520_MOESM2_ESM.pdf` (Peer Review File) | 4 586 550 o | `ce939f2227d92a7147e3d5c6681bd9fe0e8ab70c5a8c7fad99695016bfd65d67` | 200 |
| MOESM16 `41467_2025_57520_MOESM16_ESM.pdf` (Reporting Summary) | 3 947 814 o | `69a959c3ff56eff607dfa561b8734f537780e16dcf8376ade26c1b0afb95c499` | 200 |

## 3. Fichiers déjà détenus — re-vérifiés sans re-téléchargement

SHA-256 re-calculés le 21 nov. 2026, **tous identiques** aux
empreintes PROVENANCE_884 :

| Fichier | SHA-256 (re-vérifié) | Conforme |
|---|---|---|
| MOESM3_description.pdf (140 637 o) | `3a84243b…5313c569` | oui |
| MOESM4.xlsx | `09968fbc…171dfd` | oui |
| MOESM5.xlsx | `c759ab51…ef25eb` | oui |
| MOESM6.xlsx | `af69c390…01392` | oui |
| MOESM7.xlsx | `bf5cab3f…a194fe` | oui |
| MOESM8.xlsx | `9b440dd9…d5e389` | oui |
| MOESM9.xlsx | `017632df…1957` | oui |
| MOESM10.xlsx | `2e65713b…48ccaa` | oui |
| MOESM11.xlsx | `da2c4583…ff25c` | oui |
| MOESM12.xlsx | `70a0ff03…904b` | oui |
| MOESM14.xlsx | `55c35f4a…3864` | oui |
| MOESM15.xlsx | `10ce1ef8…7a44` | oui |
| MOESM17_sourcedata.xlsx (5 454 570 o) | `917a1011…511f7b1` | oui |
| `data/Chen2025_MOESM13_SupplData10.xlsx` (35 732 o) | `0e009cd5…5340` | oui |

## 4. Examen des trois fichiers nouveaux (mesuré, script `examine_889.py`)

Script d'examen `chen889_scratch/examine_889.py` (SHA
`ef2828805ef6e64f88a14f10575c54901619fa689dbc97ccbe483678a51e3645`),
sortie `examine_889.json` (SHA
`0f828245cfad1a2b996c61886aef2f54557e1576035f684668890e9e3aadadb0`).
Textes extraits par `pdftotext -layout` : `MOESM1.txt` (SHA
`0f87343e…1b06`, 3 971 lignes), `MOESM2.txt` (SHA
`9084f5eb…5318`, 1 760 lignes), `MOESM16.txt` (SHA
`c97ac254…4132d`, 1 ligne — PDF image, sans texte extractible ;
les 4 pages ont été rendues en images et lues visuellement).

### 4.1 MOESM1 — Supplementary Information (39 pages)

- 17 Supplementary Figures (Fig. 1–17), 4 Supplementary Tables,
  1 Supplementary Note (interprétation des VUS, classification
  CFTR, multi-omique, prévalence féminine, limites du modèle
  murin, modulateurs CFTR).
- Comptages exacts sur le texte extrait : `DAC` 59, `KRAS` 6,
  `MTAP` 0, `9p21` 0, `G12C` 2, `CDKN2A` 0, `organoid` 4 /
  `Organoid` 4, `Supplementary Table` 4, `Supplementary Fig` 34.
- Les 6 `KRAS` : 4 = libellés de voies `HALLMARK_KRAS_SIGNALING`
  (Supp. Fig. 15, enrichissement, pas un génotype) ; 2 = Table 4
  (`KRAS p.G12C-inhibitor` comme cible d'écran, taux de hits
  2,2 % = 1/46). Les 2 `G12C` sont dans la Table 4.
- Table 1 : statistiques agrégées seulement (N = 458 découverte,
  N = 842 ; sexe, âge, IMC, diabète, pancréatite, tabac, alcool,
  antécédents, pathologie, grade, TNM) — **aucune ligne par
  patient, aucun identifiant**.
- Table 2 : significativité statistique, comparaisons PANC-1
  (Fig. 5). Table 3 : idem, AsPC-1 (Supp. Fig. 7). Lignées
  cellulaires, pas des organoïdes.
- Table 4 (« Small molecule screening data ») : métadonnées
  d'essai seulement (63+15 composés, 7 concentrations, CellTiter-Glo,
  AUC GraphPad Prism 9, normalisation par le maximum) — **aucune
  valeur par PDO, aucun génotype**.
- Supp. Fig. 14c (p. 21) : heatmap de 18 DEGs, 57 organoïdes en
  colonnes (DAC_13 … DAC_89, 57 identifiants uniques), avec une
  barre d'annotation `CFTR mutation` MT/WT. Ordre visuel des
  colonnes vérifié par `pdftotext -bbox` (x croissant) et mesure
  de la barre sur le rendu 200 dpi : segment teal (MT)
  x_pts 51,9–74,8, orange (WT) dès 74,9, pas des colonnes
  5,719 pts, bord gauche 51,9 → (74,9−51,9)/5,719 = **4,02
  colonnes** : MT = **DAC_13, DAC_30, DAC_72, DAC_73** (4) ;
  WT = les 53 autres. Recoupement avec les 46 PDO criblés
  (MOESM13) : **38/46** — non couverts : DAC_99, DAC_102,
  DAC_103, DAC_104, DAC_109, DAC_110, DAC_114, DAC_115 (8).
  Les 4 MT sont tous parmi les 46 criblés.
- **Conflit interne à l'article (mesuré) :** la Fig. 6e de la
  Source Data (MOESM17, relue ici : 15 PDO, MT = DAC13, DAC24,
  DAC72, DAC84 ; WT = les 11 autres — identique au §8.84)
  définit `CFTR mutation MT` différemment : DAC_24 et DAC_84
  sont MT en Fig. 6e mais WT en Fig. 14c ; DAC_30 et DAC_73
  sont MT en Fig. 14c mais absents des 15 de la Fig. 6e.
  Seuls DAC_13 et DAC_72 sont MT dans les deux figures.
- Supp. Fig. 15 (p. 22) : cohortes découverte (tumeurs) et TCGA,
  annotations `CFTR expression` et `CFTR aaChange` (p.C1355Y,
  p.E681V, p.L69F, p.R1097C) — **tumeurs de patients, pas des
  organoïdes, aucun identifiant DAC**.
- Aucune autre figure ne porte d'identifiant DAC (recherche
  `DAC` sur tout le texte : seuls la Fig. 14c et le mot `PDAC`
  de la Table 1).

### 4.2 MOESM2 — Peer Review File

- Comptages exacts : `DAC` 2, `KRAS` 15, `MTAP` 0, `9p21` 0,
  `G12C` 7, `CDKN2A` 1, `organoid` 71, `Supplementary Table` 0.
- Les 2 `DAC` : formule de politesse du rapporteur n° 3
  (« In this manuscript Yin et al describe… »), aucune donnée.
- Les 15 `KRAS` / 7 `G12C` : discussion d'évaluation par les
  pairs uniquement, aucune table. Point décisif (rapporteur n° 2,
  point 13) : « In Fig.6b, there seems to be only one sample
  with a KRAS G12C mutation. However, according to line 363-364,
  two organoids bore the mutation. Please clarify this
  inconsistency. » Réponse des auteurs (2.13) : « We corrected
  this mistake in Lines 363-364: “One organoid bearing the KRAS
  p.G12C mutation exhibited sensitivity to AMG510 and
  MRTX849.” » — **UN seul organoïde KRAS p.G12C, toujours sans
  identifiant DAC nommé**.

### 4.3 MOESM16 — Reporting Summary (4 pages)

- Formulaire Nature Portfolio (image, sans texte extractible ;
  4 pages rendues en PNG et lues : `rs16-1.png` à `rs16-4.png`).
- Section Data : reprend la déclaration de disponibilité des
  données (HRA005195, HRA010277, ST003734, Code Ocean 1432248) ;
  sections Statistics, Software and code, Research involving
  human participants, Life sciences study design, Antibodies,
  Eukaryotic cell lines, Animals, Plants, Flow Cytometry.
- **Aucune table de données, aucun génotype, aucun identifiant
  DAC.**

## 5. Dépôts cités dans « Data availability »

- **GSA-Human (NGDC) HRA005195** : séquences brutes WGS/WES/
  RNA-seq de la cohorte découverte + WGS de la cohorte de
  validation fonctionnelle (69 organoïdes). **Accès contrôlé**
  (données humaines ; l'article : « Data and materials that can
  be shared will be released via a material transfer agreement
  to protect patient privacy »). Page publique de l'accession
  tentée le 21 nov. 2026 : `browser.open` en échec (erreur
  réseau, sans statut HTTP) — page live non confirmée ; **aucune
  demande d'accès, aucun compte créé, aucun téléchargement de
  lectures brutes** (protocole §2/§3.4 : un accès contrôlé est
  un blocage à nommer, pas à contourner). Contenu : des lectures
  brutes, pas une table par-PDO — KRAS/MTAP n'y seraient
  lisibles qu'après ré-analyse des WGS, hors de ce chantier.
- **GSA-Human (NGDC) HRA010277** : RNA-seq et ATAC-seq des
  organoïdes + RNA-seq des lignées. Même statut : accès contrôlé,
  mêmes limites ; page non consultée (même échec réseau, non
  répété). Pas une table par-PDO.
- **Metabolomics Workbench ST003734** (projet PR002320, DOI
  10.21228/M8R83M) : page d'étude consultée en direct le
  21 nov. 2026 — **lipidomique de la lignée PANC-1** (52
  échantillons : CFTR OE / EV / p.L88X / p.E681V / p.C1355Y +
  QC, 4 réplicats techniques), pas des organoïdes, aucun
  identifiant DAC, aucun KRAS/MTAP. Aucune table par-PDO.
- **Code Ocean 1432248** (DOI 10.24433/CO.1432248.v1) : **code
  seulement** — article § Code availability (« All original code
  has been deposited in Code Ocean … under an MIT License ») et
  MOESM16 p. 1 (« All original code has been deposited in Code
  Ocean (capsule number 1432248) »). Page DOI tentée le
  21 nov. 2026 : HTTP 403 (accès refusé en amont), non répétée ;
  la qualification « code seulement » repose sur l'article et
  sur MOESM16, pas sur la page live. Aucun génotype attendu.

## 6. Ce qui manque / limites (verdicts d'intestabilité, pas des échecs cachés)

- **Aucune table KRAS par PDO, aucune table MTAP par PDO, dans
  aucun des 17 suppléments ni dans les dépôts consultables.**
  `MTAP` : 0 occurrence dans MOESM1, MOESM2 et dans tout le
  texte de l'article. `KRAS` : 0 statut par PDO partout.
- L'organoïde KRAS p.G12C est unique (confirmé par MOESM2)
  mais toujours sans identifiant DAC : le test ciblé T4 reste
  impossible.
- La Fig. 14c donne une variable par organoïde (CFTR MT/WT,
  57 organoïdes) mais elle est **non recevable** comme base de
  test : (a) ce n'est pas une table, c'est une barre
  d'annotation de figure ; (b) couverture 38/46 < 40 (seuil
  gelé §4) — 8 PDO criblés non classés, dont DAC_110 (porteur
  CFTR VUS_D nommé au §8.84) ; (c) effectif MT n = 4 ;
  (d) définition en conflit avec la Fig. 6e pour DAC_24 et
  DAC_84. **Aucun test analogue n'a donc été couru dessus**
  (protocole §5 : le test analogue est conditionné à une table
  trouvée ; §4 : couverture < 40/46 = non recevable).
- Conséquence : T1 (D3), T2 (D4), T3 (survie des hits D1 sous
  KRAS/MTAP) n'ont pas été courus — condition non remplie.
  La question « les hits paclitaxel / mitomycine C
  survivent-ils quand on fixe KRAS / MTAP ? » reste **sans
  réponse, pas tranchée négativement**.
- Ce qui débloquerait D3/D4 : une table des auteurs reliant
  KRAS/MTAP aux 46 DAC, ou un accès approuvé GSA-Human
  (demande + MTA) suivi d'une ré-analyse des WGS des 69
  organoïdes — hors de ce chantier, à décider par Zackary.

## 7. Fichiers produits par ce chantier (à hasher après écriture)

- `~/workspace/runs/pdac-v6/PROTOCOL_chen_supplements_889.md`
  (SHA `d4296ddd…07de792b`)
- `~/workspace/runs/pdac-v6/PROVENANCE_889.md` (ce fichier)
- `~/workspace/runs/pdac-v6/section_8.89_chen_supplements.md`
- `~/workspace/runs/pdac-v6/chen889_scratch/` :
  `MOESM1_SupplInfo.pdf` (SHA `4b70d25b…60aa61f`),
  `MOESM2_PeerReview.pdf` (SHA `ce939f22…65d67`),
  `MOESM16_ReportingSummary.pdf` (SHA `69a959c3…95c499`),
  `MOESM1.txt` (SHA `0f87343e…1b06`), `MOESM2.txt` (SHA
  `9084f5eb…5318`), `MOESM16.txt` (SHA `c97ac254…4132d`),
  `examine_889.py` (SHA `ef282880…e3645`),
  `examine_889.json` (SHA `0f828245…bef946`),
  `examine_889.log`, `fig14_bbox.html` (SHA
  `4704be41…dce`), `fig14hi-21.png`, `fig14_15-21.png`,
  `fig14_15-22.png`, `fig14c_bar.png`, `fig14c_bar2.png`,
  `fig14c_bar3.png`, `rs16-1.png` à `rs16-4.png`
- Aucun script de test direct produit (condition non remplie) ;
  aucun run pipeline ; livre blanc non édité ; rien poussé.

## Addendum — 21 novembre 2026 (audit §8.90, I-1)

Coquille de transcription au §7 ci-dessus : lire `examine_889.json`
(SHA `0f828245…aadadb0`) au lieu de `0f828245…bef946`. SHA complet
vérifié par `sha256sum` :
`0f828245cfad1a2b996c61886aef2f54557e1576035f684668890e9e3aadadb0` —
conforme au §4 de la même provenance et au §40 de DATA_SOURCES.md.
Le texte d'origine ci-dessus est intact ; aucun verdict n'est touché
(le fichier `examine_889.json` lui-même est intact et conforme).
