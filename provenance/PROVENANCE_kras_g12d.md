# PROVENANCE — Inhibiteurs directs de KRAS G12D et pan-RAS (16 nov. 2026)

Mission : trouver des données publiques de dose-réponse pour les inhibiteurs directs
de KRAS G12D et pan-RAS dans le pancréas, ou nommer exactement ce qui manque.
Auteur : agent TagPrint (sous-agent, bras D du mandat « continuer jusqu'à trouver
un remède »). Date : 16 novembre 2026.

## 1. Données déjà sur disque (vérifiées, non re-téléchargées)

| Fichier | Taille (octets) | SHA-256 | Source |
|---|---|---|---|
| `data/Repurposing_Public_24Q2_Extended_Primary_Data_Matrix.csv` | 72 456 953 | (vérifié le 15 nov. 2026, voir PROVENANCE du projet) | PRISM Repurposing Public 24Q2, Broad Institute, figshare article 25917643 |
| `data/Repurposing_Public_24Q2_Extended_Primary_Compound_List.csv` | — | — | idem (6 790 composés) |
| `data/CRISPRGeneEffect.csv` | 428 678 699 | `3d8f3ec6…` (vérifié le 15 nov.) | DepMap Public 24Q4, Broad, figshare article 27993248, DOI 10.25452/figshare.plus.27993248.v1 |
| `data/Model.csv` | 645 696 | `b7a0c138…` (vérifié le 15 nov.) | idem |
| `data/GDSC2_fitted_dose_response_27Oct23.xlsx` | 22 112 537 | `0e99120a…c899` (vérifié le 16 nov., bras GDSC) | GDSC2 via Cell Model Passports (Sanger), groupe 46 |
| `data/prism_secondary_kras_screen.csv` + fichiers `secondary-screen-*.csv` | — | — | PRISM secondaire 19Q4, téléchargé par le bras parallèle (16 nov. 07h47) ; vérifié présent sur disque, non re-téléchargé ici |

## 2. Données téléchargées pour cette mission (16 nov. 2026)

| Fichier | Taille exacte (octets) | SHA-256 | Source / URL |
|---|---|---|---|
| `data/OmicsSomaticMutationsMatrixHotspot.csv` | 4 210 723 | `6444ce819a28d4228ff7b748e309611c5830c551620d8d2c7f86052e2675e3d8` | DepMap 24Q4, figshare article 27993248, fichier 51065750 (`ndownloader.figshare.com/files/51065750`) |
| `data/OmicsSomaticMutationsMAFProfile.maf` | 98 439 503 | `86b8530b31125305391dcffb7dffc5426535df63705a2bf76565368f3955e96f` | DepMap 24Q4, figshare article 27993248, fichier 51065741 |
| `data/OmicsProfiles.csv` | 254 733 | `0bb19ee57935d4b213d378a4db9caacaa1db7318a63ae81485d84f91c20a3bf2` | DepMap 24Q4, figshare article 27993248, fichier 51065723 |

Limite connue : la matrice hotspot ne donne que des codes 0/1/2 (muté ou non),
pas l'allèle. L'allèle vient du MAF (colonne `Protein_Change`), joint aux modèles
par `OmicsProfiles.csv` (ProfileID `PR-…` → ModelID `ACH-…`). Jointure vérifiée :
390/390 lignes KRAS jointes ; 54 lignées pancréas avec allèle (G12D 23, G12V 20,
G12R 5, Q61H 2, Q61R 1, G12C 1, G12A 1, G12I 1) ; 14 lignées pancréas sans mutation
KRAS dans le MAF (cohérent avec des lignées KRAS WT connues, ex. BxPC-3 — non
vérifié ligne par ligne ici).

## 3. Sources web consultées (16 nov. 2026, recherche textuelle, pas de navigation)

- Hallin et al., *Nature Medicine* 2022, 28:2171–2182, DOI 10.1038/s41591-022-02007-7,
  PMID 36216931 (MRTX1133, préclinique + 8/11 modèles PDAC).
- Drosten & Barbacid, *Molecular Oncology* 2022, 16:3911–3915, doi 10.1002/1878-0261.13341
  (commentaire Hallin : combinaisons MRTX1133 + cetuximab / BYL-719 ; MEK/ERK/SHP2/SOS1 sans effet).
- Kemp et al. 2023, *Cancer Cell* / *Developmental Cell* (MRTX1133 + immunothérapie,
  modèles immunocompétents — via MD Anderson TRACTION, résumé consulté).
- *Gastroenterology* 2024, doi 10.1016/S0016-5085(24)05027-3 (organoïdes PDAC,
  MRTX1133 ± EGFR, synergie spécifique G12D, 19 organoïdes).
- Wolpin et al., *NEJM* 2026, 394(18):1790–1802, doi 10.1056/NEJMoa2505783
  (daraxonrasib phase I/II, n=168 PDAC prétraités, ORR 29 %).
- Revolution Medicines, communiqué phase III RASolute-302 (NCT06625320) + ESMO 2026
  (OS 13,2 contre 6,7 mois, HR 0,40) — via k-dense.ai et pharmacally.com, sources
  secondaires ; l'approbation FDA est confirmée par la revue *Cancers* 2026
  (doi 10.3390/cancers18213519, « first regulatory approval of a RAS-targeted
  inhibitor in pancreatic ductal adenocarcinoma »).
- *Cancers* 2025, 17, 2453, doi 10.3390/cancers17152453 (tableau 2 : MRTX1133
  NCT05737706, ASP3082 NCT05382559, RMC-9805 NCT06040541 ; sotorasib/adagrasib PDAC).
- *Advances in KRAS-Targeted Therapies for Pancreatic Cancer*, PMC13604613
  (MRTX1133 NCT05737706 TERMINATED début 2025, formulation/PK après rachat Mirati
  par BMS ; HRS-4642 + gem/nab-paclitaxel DCR 93,3 %).
- *Frontiers in Oncology* 2024, doi 10.3389/fonc.2024.1402128 (sotorasib CodeBreaK 100
  PDAC n=38 ORR 21 % ; adagrasib KRYSTAL-1 n=21 ORR 33 % ; RMC-6236 ESMO 2023 préliminaire).
- *Therapeutic Advances in Medical Oncology* 2026, PMC13129282 (mêmes chiffres
  sotorasib/adagrasib confirmés).
- *Turkish Journal of Gastroenterology* 2026, 37(4):409–419, doi 10.5152/tjg.2026.25595
  (tableau 1 : essais et combinaisons KRAS dans le PDAC).
- *Cancers* 2026, 18, 3519, doi 10.3390/cancers18213519 (combinaisons RAS, RASolute-303/305,
  RMC-6236 + PI3Kα/δ Köse et al.).
- *Frontiers in Immunology* 2023, doi 10.3389/fimmu.2023.1223433 (BI-3406 / BI-1701963,
  SOS1 ; NCT04111458).
- *Frontiers in Medicine* 2024, doi 10.3389/fmed.2024.1369136 (TNO155 NCT03114319, 118
  patients, 20 % maladie stable ; BI-1701963, 31 patients, 7/31 stables à 18 mois).
- ClinicalTrials.gov (via Selleckchem, données au 27 août 2026) : NCT05737706 TERMINATED ;
  NCT05379985, NCT06625320, NCT07252232, NCT07805954, NCT06040541, NCT06445062,
  NCT04111458, NCT03114319, NCT03600883, NCT03785249, NCT05382559, NCT04185883.
- ChEMBL (API publique EBI, consultée le 16 nov. 2026) : MRTX-1133 `CHEMBL4858364`
  (45 activités) ; daraxonrasib `CHEMBL6168538` (85 activités, 80 d'un seul document
  CHEMBL6115029) ; RMC-9805 / zoldonrasib : 0 résultat ; ASP3082 : 0 résultat.

## 4. Scripts et sorties de cette mission

- `mrtx1133_prism_allele.py` — SHA `932fcafc99c712b665d2c0fbfedc1ac16cf1a9b9d253d76c6cfd4b58a0ab85be`.
  Reproduit les chiffres à l'identique (vérifié : CSV des allèles identique,
  valeurs MRTX1133 identiques ; seule différence : une colonne ajoutée pour
  K-RAS(G12C)-INHIBITOR-6).
- `data/kras_alleles_pancreas.csv` — SHA `9ac803adaba4b634a3b4a4dac5e51c81e4f9c0027209634322ce3b4195bc0d42`.
- `data/mrtx1133_prism_kras_allele.csv` — SHA `7a449c92e992fa347819e94ac188f78dc3c93316ea7119672ea886b226e6e5ef6`.
- `data/kras_mutations_maf.csv` — 390 lignes KRAS extraites du MAF,
  SHA `fcf0eed222d9c87de4d0bb081a14fc50ff5ffdff5aaa5b63794d00a11293380c`.
- `kras_g12d_inhibitors.md` — rapport composé par composé.
- `PROVENANCE_kras_g12d.md` — ce fichier.

## 5. Ce qui n'a pas été fait / limites

- Les tableaux supplémentaires de Hallin et al. 2022 n'ont pas été téléchargés
  séparément : leurs valeurs par lignée sont déjà extraites dans ChEMBL (45
  activités MRTX1133) et citées depuis là.
- Aucune donnée d'entreprise non publique n'a été demandée ni obtenue
  (Revolution Medicines, Mirati/BMS, Astellas, Amgen, Boehringer, Novartis).
- Les essais cliniques sont cités comme essais, jamais comme données de
  sensibilité cellulaire.
- La combinaison KRAS + autophagie n'a pas été fouillée (hors périmètre :
  aucune source trouvée dans les recherches menées ; à traiter séparément).
- Le résultat PRISM secondaire (bras parallèle, 16 nov. 07h47) est cité comme
  tel, pas comme un résultat de cette mission ; seule la vérification d'absence
  des composés cibles dans ses fichiers (sur disque) a été refaite ici.
- Les chiffres RASolute-302 / FDA proviennent en partie de sources secondaires
  (communiqué de presse, ESMO 2026) ; l'approbation FDA est corroborée par une
  revue à comité de lecture (*Cancers* 2026). À confirmer sur le site de la FDA
  avant toute citation publique.
