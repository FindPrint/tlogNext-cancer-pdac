# PROVENANCE — Combinaisons KRAS / pancréas (16 nov. 2026)

## 1. Cadre

- **Projet :** PDAC v6, bras « combinaisons » du mandat « remède » (ordre de Zackary,
  16 nov. 2026, 07h47 : « Continue jusqu'à ce que tu trouve un remède »).
- **Question :** une combinaison réussit-elle là où chaque médicament seul échoue,
  chez le pancréas KRAS-dépendant ?
- **Règle appliquée :** aucune affirmation sans source nommée ; aucune conclusion
  importée d'autres expériences — les chiffres de ce bras et les sources citées
  font le verdict ; une combinaison sans preuve mesurée reste une hypothèse.
- **Auteur :** TagPrint (agent). **Date :** 16 novembre 2026.

## 2. Revue des combinaisons (sources web, 16 nov. 2026)

Recherches web ciblées (moteur de recherche, résultats horodatés 16 nov. 2026) +
lecture des pages d'articles et de registres d'essais. Chaque affirmation du
rapport renvoie à une source nommée (auteur, revue, année, PMID/DOI ou
identifiant NCT) — voir §12 du rapport (`kras_combinations.md`).
Limites : les chiffres d'essais proviennent des publications et communiqués
cités, pas d'une relecture des données individuelles ; les communiqués
d'entreprises (Tango, Revolution Medicines) sont des sources primaires
d'entreprise, pas des publications revues par les pairs — le rapport le dit.

## 3. Données de combinaisons — accès et échecs documentés

### 3.1 DrugComb — INJOIGNABLE (échec documenté, pas supposé)

| Tentative | Date | Résultat |
|---|---|---|
| `curl https://drugcomb.org/downloads` (sans user-agent) | 16 nov. 2026 | HTTP 000, 0 octet |
| `curl https://drugcomb.org/` + `/downloads` + `drugcomb.fimm.fi` (user-agent navigateur) | 16 nov. 2026 | HTTP 000, 0 octet, 3/3 |
| `curl -sI https://drugcomb.org/` | 16 nov. 2026 | « 200 Connection Established » (proxy) puis réponse vide, exit 52 |
| `curl https://drugcombdb.drugcomb.org/` | 16 nov. 2026 | HTTP 000 |
| `browser.open https://drugcomb.org/downloads` | 16 nov. 2026 | Échec : DNS / connexion refusée |
| Contrôle : `curl https://www.google.com` | 16 nov. 2026 | HTTP 200 — le réseau de la VM fonctionne |

- DNS résout drugcomb.org (198.18.134.92) et drugcomb.fimm.fi (198.18.134.93).
- Les fichiers HTML vides de ces tentatives ont été supprimés (0 octet, sans
  contenu) ; l'échec est consigné ici, pas par des fichiers vides.
- Contenu connu du portail (Zagidullin et al., *Nucleic Acids Res* 2019,
  doi 10.1093/nar/gkz337) : 437 932 combinaisons, 2 276 médicaments, 93 lignées,
  10 tissus ; études ALMANAC (103 médicaments, 303 737 combinaisons, 60 lignées),
  ONEIL (38 médicaments, 92 208 combinaisons, 39 lignées), FORCINA (1 818
  combinaisons, 1 lignée), CLOUD (283 médicaments, 40 160 combinaisons, 1 lignée).

### 3.2 NCI ALMANAC — pas de lignée pancréas (vérifié par la liste des lignées)

- 104 médicaments approuvés, 5 050 combinaisons, 293 565 ComboScores, panel
  NCI-60. Liste des lignées vérifiée dans le supplément de l'étude ALMANAC
  (biorxiv 2018, tableau supplémentaire 1) : leucémie, mélanome, poumon, côlon,
  SNC, ovaire, rein, prostate, sein — **aucune lignée pancréas** (le NCI-60
  n'a pas de panel pancréas). Les données ALMANAC n'ont pas été téléchargées :
  leur composition suffit à les écarter pour cette question.

### 3.3 AZ-DREAM — pas de lignée pancréas (vérifié dans l'article)

- Menden et al., *Nat Commun* 2019, 10:2674 (PMID 31209238) : 11 576 expériences,
  910 combinaisons, 118 médicaments, 85 lignées — **sein 34, poumon 22, vessie 14,
  tractus gastro-intestinal 12. Aucune lignée pancréas.** Données sur Synapse
  (syn4231880, compte requis) — non téléchargées, composition suffisante pour
  écarter.

### 3.4 O'Neil — pas de lignée pancréas (vérifié dans l'article)

- O'Neil et al., *Mol Cancer Ther* 2016, 15:1155–62 : 38 médicaments,
  583 combinaisons, 39 lignées, 22 737 expériences — **sein 6, côlon 8, poumon 8,
  mélanome 6, ovaire 9, prostate 2. Aucune lignée pancréas.**

### 3.5 PANC-1 (NCATS) — TÉLÉCHARGÉ ET VÉRIFIÉ

- **Source :** dépôt GitHub `ncats/PANC1`, branche `main` (article : Pourmousa
  et al., *Nat Commun* 2025, 16:4020, doi 10.1038/s41467-025-56818-6 ;
  dépôt Zenodo 10.5281/zenodo.14230972).
- **Accès :** `git clone` bloqué (aucune sortie après 174 s, processus arrêté) ;
  tarball `codeload.github.com/ncats/PANC1/tar.gz/refs/heads/main` téléchargé
  mais **tronqué** (569 815 185 octets, erreur gzip « unexpected end of file » à
  l'extraction — archive supprimée). **Fichiers finalement obtenus un par un via
  `raw.githubusercontent.com`** (HTTP 200, tailles identiques à celles annoncées
  par l'API GitHub).
- **Fichiers** (`data/panc1_ncata/`, 8 fichiers) :

| Fichier | Octets | SHA-256 (début) |
|---|---|---|
| 9191_calc.csv | 24 780 | 7a5c88d74a0b512b… |
| 9191_metadata.csv | 80 936 | e12c0251d3c1708e… |
| 9191_metadata_smiles.csv | 120 243 | 4e0f0119e1c31336… |
| 9191_responses.csv | 760 685 | f5cc98d3442d3754… |
| 9197_calc.csv | 24 165 | 3c50bb1b32d451e1… |
| 9197_metadata.csv | 71 459 | 1240777419d25e98… |
| 9197_metadata_smiles.csv | 108 941 | d45b7d730c002e96… |
| 9197_responses.csv | 750 256 | cdece93912122bc6… |

  SHA-256 complets : `data/panc1_ncata/panc1_sha256.txt`.
- **Contenu :** 496 combinaisons (C(32,2)), matrices 10×10, lignée PANC-1 seule
  (KRAS G12D). `calc.csv` : scores Gamma, Beta, ExcessHSA par bloc (un réplicat
  par bloc dans les fichiers déposés). Gamma < 0,95 = synergique (définition
  de l'article).
- **Fichier exclu :** `MIT/test.csv` (10 000 lignes, 3 249 228 octets) — scores
  Gamma_Score de moyenne −0,34 (échelle différente des gamma mesurés ~0,9),
  3 lignes seulement en recouvrement avec les 496 paires mesurées : ce sont des
  **scores prédits par modèle** sur une bibliothèque virtuelle, pas des mesures.
  Exclu de l'analyse, gardé pour traçabilité.
- **Analyse :** script `analyze_panc1_combos.py` (runs/pdac-v6), sortie
  `data/panc1_combinations_summary.csv` (497 lignes = en-tête + 496 paires),
  SHA-256 `423ac17579416e64421595fbb3e2fc9bb966b4bc3a43f92e1851ba649f541f77`.
  Résultats : 280/496 synergiques (56,5 %), 12 fortes (gamma < 0,5) ;
  **0 paire avec inhibiteur MEK/KRAS/ERK/RAF/SHP2/SOS1 ou HCQ**.
- **Contexte KRAS :** PANC-1, Chronos KRAS (DepMap 24Q4, `data/CRISPRGeneEffect.csv`,
  déjà sur disque, SHA `3d8f3ec6…`) = **−1,658** (médiane pancréas −1,76),
  modèle ACH-000164. Une seule lignée : **aucun test de corrélation
  inter-lignées possible** (documenté, pas contourné).

### 3.6 FORCINA — cité, non téléchargé

- Forcina et al., *Mol Cancer Ther* 2017, 16(6):1041–1053 : 4 lignées PDAC
  (MiaPaCa-2, PANC-1, PL45, SU-86-86), 40 agents, 7 503 combinaisons dose.
  Données supplémentaires sur le site AACR, non téléchargées : 4 lignées toutes
  KRAS-mutantes, n=4 — aucun test de corrélation KRAS possible. Les résultats
  cités (JQ1 + MLN4924) viennent de l'article, pas d'une re-analyse.

## 4. Ce qui manque

- Accès DrugComb (portail injoignable depuis cette VM) — même accessible, son
  seul contenu pancréatique serait FORCINA (1 lignée dans la curation).
- Aucune matrice publique de synergie sur plusieurs lignées pancréas en accès
  libre — le test « dépendance KRAS → bénéfice de la combinaison » n'a pas pu
  être fait sur données.
- Données individuelles des essais cités (Tango, Revolution Medicines) :
  chiffres repris des communiqués et publications, non re-calculés.
- Statut des essais NCT05737706, NCT05533463, NCT05846516 (trametinib + HCQ,
  phase I, cités dans Tang 2023) : non vérifié.

## 5. Fichiers livrés

- `runs/pdac-v6/kras_combinations.md` — rapport (verdict, 11 sections, sources).
- `runs/pdac-v6/PROVENANCE_kras_combinations.md` — ce fichier.
- `runs/pdac-v6/analyze_panc1_combos.py` — script d'analyse PANC-1.
- `runs/pdac-v6/data/panc1_combinations_summary.csv` — 496 paires, gamma moyens.
- `runs/pdac-v6/data/panc1_ncata/` — 8 fichiers sources PANC-1 + `mit_test.csv`
  (prédictions, exclu) + `panc1_sha256.txt` + `panc1_README.md`.
