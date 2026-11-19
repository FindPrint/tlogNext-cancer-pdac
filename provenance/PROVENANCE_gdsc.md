# PROVENANCE — GDSC2 dose-réponse, criblage ciblé KRAS (PDAC v6)

Date : 16 novembre 2026. Auteur : agent TagPrint (bras « médicaments ciblés KRAS »).
Protocole gelé par la mission parente ; script `gdsc_kras_screen.py` (sauvegardé).

## Sources des données

### GDSC2 — dose-réponse ajustée (source première, RÉUSSIE)
- **Projet :** Genomics of Drug Sensitivity in Cancer (GDSC2), Wellcome Sanger Institute.
  969 lignées, 297 composés (286 noms uniques dans le fichier), essais de viabilité
  72 h, courbes ajustées par le modèle à effets mixtes non linéaires de Vis et al.
  (paquet R gdscIC50) → LN_IC50, AUC, RMSE, Z-score.
- **Fichier :** `GDSC2_fitted_dose_response_27Oct23.xlsx`
- **URL exacte :** https://cmp.cog.sanger.ac.uk/download/GDSC2_fitted_dose_response_27Oct23.xlsx
- **Chemin d'accès :** site GDSC (cancerrxgene.org/downloads/bulk_download) → intégré à
  Sanger DepMap / Cell Model Passports → API publique
  https://api.cellmodelpassports.sanger.ac.uk/download_files (include=groups.files),
  catégorie 10 « Drug Sensitivity Data », groupe 46 « GDSC2 IC50 Data », fichier 22870.
- **Taille :** 22 112 537 octets exacts (taille annoncée par l'API : 22 112 537).
- **SHA-256 :** `0e99120a14a003dcbd3c27c020f1cfd35e38ee091067a2406f66c0d4dbc1c899`
- **Téléchargement :** 16 nov. 2026, 3 tentatives (serveur lent, ~25 Ko/s, coupures
  curl exit 18 à 11 124 736 puis à 20 512 768 octets ; reprises `curl -C -`,
  HTTP 206, fichier complet vérifié par taille exacte + type xlsx). Voir `gdsc_access.log`.
- **Contenu vérifié :** 242 036 lignes, 16 colonnes (DATASET, NLME_RESULT_ID,
  NLME_CURVE_ID, CELL_LINE_NAME, SANGER_MODEL_ID, CANCER_TYPE, DRUG_ID, DRUG_NAME,
  PUTATIVE_TARGET, PATHWAY_NAME, MIN_CONC, MAX_CONC, LN_IC50, AUC, RMSE, Z_SCORE).
  286 DRUG_NAME uniques, 295 DRUG_ID uniques, 969 lignées.

### Annotation des composés (recoupement)
- **Fichier :** `screened_compounds_rel_8.5.csv` (46 414 octets exacts, annoncés par l'API)
- **URL :** https://cmp.cog.sanger.ac.uk/download/screened_compounds_rel_8.5.csv
- **SHA-256 :** `d3cbb8b595980b36bf92d54af1da1dd995d2e2ce624c7cc70aacf2a754dce782`
- Colonnes : DRUG_ID, SCREENING_SITE, DRUG_NAME, SYNONYMS, TARGET, TARGET_PATHWAY.
- Sert à confirmer la présence/absence des composés prioritaires.

### DepMap CRISPR 24Q4 (déjà présent, axe KRAS)
- `data/CRISPRGeneEffect.csv` : 428 678 699 octets, SHA `3d8f3ec6…` (vérifié le 15 nov.).
- `data/Model.csv` : 645 696 octets, SHA `b7a0c138…`.
- Axe : effet Chronos KRAS, colonne « KRAS (3845) », convention de `prism_screen.py`.
- Un seul SangerModelID dupliqué dans Model.csv (SIDM00117 → 2 lignées poumon,
  NCI-H322 / NCI-H322M) : première occurrence gardée, sans effet sur le pancréas.

## Méthode (script `gdsc_kras_screen.py`, exit 0)
1. Jointure GDSC2 → DepMap par SANGER_MODEL_ID → Model.csv SangerModelID → ModelID ;
   filtre OncotreeLineage == « Pancreas » : 31 lignées GDSC2, **27 avec Chronos KRAS**
   (KRAS Chronos : min −4,14 ; médiane −1,89 ; max −0,36).
2. Agrégation par DRUG_NAME (moyenne sur DRUG_ID dupliqués : 9 composés sur 272).
3. Par composé (n ≥ 15 lignées, comme PRISM) : Spearman LN_IC50 vs Chronos KRAS
   et Spearman AUC vs Chronos KRAS ; moyennes par tertile de DÉPENDANCE
   (fort = Chronos le plus négatif = le plus dépendant — étiquettes corrigées,
   voir § « Signalement ») ; FDR Benjamini-Hochberg sur les 269 composés testés.
4. Sens : rho > 0 = les lignées KRAS-dépendantes sont plus sensibles (IC50/AUC plus bas).
5. Effets de classe : médiane des rho par voie (PATHWAY_NAME) et par cible
   (PUTATIVE_TARGET), groupes de ≥3 composés.

## Résultats (fichiers `data/gdsc_kras_screen.csv`, `_pathways.csv`, `_targets.csv`)
- 269 composés testés (n = 23 à 27 lignées). Médiane rho LN_IC50 = −0,295
  (5,9 % des composés seulement ont rho > 0) : les lignées KRAS-dépendantes sont
  globalement PLUS résistantes à la plupart des médicaments.
- FDR < 0,05 : **1 seul composé, la staurosporine** (rho IC50 −0,715, p = 2,8e-5,
  FDR 0,0075 ; rho AUC −0,684, p = 8,3e-5, FDR 0,022 ; IC50 tertile dépendant
  −0,97 contre −2,84 ln µM chez les indépendantes). Direction NÉGATIVE :
  les lignées KRAS-dépendantes sont plus RÉSISTANTES à la staurosporine.
  Inhibiteur de kinases à large spectre, non spécifique : curiosité, pas un candidat.
- Voie KRAS, tous non significatifs (FDR 0,25 à 0,86) :
  sélumétinib rho +0,217 (p = 0,276, FDR 0,402), tramétinib +0,164 (p = 0,415),
  PD0325901 +0,120, SCH772984 +0,085, ERK_2440 +0,246 (p = 0,258),
  ERK_6604 +0,191, refametinib +0,128, ulixertinib −0,294, dabrafenib −0,283,
  KRAS (G12C) Inhibitor-12 −0,053 (p = 0,809), SB590885 −0,411, PLX-4720 −0,543.
  Médiane rho du groupe KRAS/MEK/ERK/RAF/SHP2/SOS1 : −0,039 (15 composés).
  Médiane rho voie « ERK MAPK signaling » : +0,085 (13 composés) ;
  cible MEK1/MEK2 : +0,146 (4 composés) — direction attendue, amplitude faible,
  aucune significativité.
- **Verdict : NON.** Le groupe KRAS fort ne répond pas mieux aux inhibiteurs
  de la voie KRAS en dose-réponse GDSC2. Tendance faible dans le bon sens pour
  MEK/ERK, rien de significatif.

## Ce qui manque / limites
- **Absents de GDSC2** (vérifié dans le fichier et dans l'annotation) :
  sotorasib (AMG-510), adagrasib (MRTX849), MRTX1133 (KRAS G12D), cobimétinib,
  binimétinib, SHP099, TNO155, BI-3406 (SOS1), vémurafénib, encorafénib.
  Seul inhibiteur direct de KRAS présent : « KRAS (G12C) Inhibitor-12 »
  (composé-outil, rho −0,053, rien). Les inhibiteurs KRAS G12C/G12D de clinique
  ne sont donc PAS testables ici — il faudrait une autre source (ou un criblage
  dédié), et la plupart des PDAC sont KRAS G12D, pas G12C.
- Seulement 27 lignées pancréatiques avec Chronos KRAS (31 dans GDSC2, 47 dans
  DepMap) : puissance faible, un Spearman à n=27 a un large intervalle.
- GDSC1 non testé (même question, autre jeu de données, 403 composés).
- n par composé : 27 (134 composés), 23 (101), 26 (33), 25 (1) — certains
  composés n'ont pas été criblés sur toutes les lignées.

## Signalement — étiquettes de tertiles (à vérifier côté parent)
Dans `prism_screen.py` (15 nov.), les tertiles étaient étiquetés
`pd.qcut(kk, 3, labels=["faible", "moyen", "fort"])` : qcut étiquette par
ordre croissant des valeurs, donc « fort » = Chronos le PLUS ÉLEVÉ = le
MOINS dépendant de KRAS. Si « KRAS-fort » y était lu comme « le plus
dépendant », la direction des tertiles PRISM est inversée (les rho eux-mêmes
sont corrects ; le verdict PRISM — négatif, FDR 0,286 — ne change pas).
Dans `gdsc_kras_screen.py`, les étiquettes sont corrigées
(`labels=["fort", "moyen", "faible"]`, « fort » = Chronos le plus négatif =
le plus dépendant) et les deltas ont été vérifiés indépendamment, composé
par composé (sélumétinib, tramétinib, staurosporine, ERK_2440 : rho et
moyennes par tertile reproduits à l'identique).

## Fichiers produits
- `gdsc_kras_screen.py` — script (exit 0, ~48 s)
- `data/gdsc_kras_screen.csv` — 269 composés, tous les résultats (rho, p, FDR,
  deltas par tertile, IC50/AUC par tertile)
- `data/gdsc_kras_screen_pathways.csv` — médianes par voie
- `data/gdsc_kras_screen_targets.csv` — médianes par cible
- `gdsc_kras_screen.log`, `gdsc_kras_screen_stdout.txt` — journaux
- `data/GDSC2_fitted_dose_response_27Oct23.xlsx`, `data/screened_compounds_rel_8.5.csv`
- `PROVENANCE_gdsc.md` (ce fichier), `gdsc_access.log`
