# PROVENANCE — Thérapies ciblées MUC16 (CA125) et CLDN18.2, cancer du pancréas

**Date :** 16 novembre 2026. **Projet :** PDAC v6. **Bras :** suite du mandat « continuer jusqu'à trouver un remède » (ordre de Zackary, 16 nov. 2026, 07h41).

## 1. Ce qui a été fait

1. **Revue des thérapies** (agent de recherche web, 16 nov. 2026, 07h42–07h45) : recherche web (browser.search / browser.open), sources nommées une par une. Brouillon de travail : `literature_muc16_cldn182_draft.md` (40 193 octets, 31 sources numérotées, §5 points non vérifiés).
2. **Vérification des trois affirmations pivots** (par le coordinateur, 16 nov. 2026) :
   - Échec GLEAM : confirmé par deux sources indépendantes — communiqué Astellas, 14 oct. 2025 (relayé par Drugs.com) ET présentation ESMO GI 2026 (Park et al., résumé 342O) : SG médiane 13,7 vs 13,6 mois, HR 0,999 (IC 95 % 0,776–1,286), p = 0,4987 ; 2 529 patients dépistés, 393 randomisés. La revue *Drugs* 2026 ;86:507–532 confirme l'échec.
   - IBI343 : confirmé par le résumé ASCO 2025 (Yu X. et al., *J Clin Oncol* 2025 ;43:4017), le communiqué Innovent / PR Newswire Asia (2 juin 2025) et la revue ASCO 2025 highlights (Springer) — chiffres identiques : ORR confirmée 22,7 %, DCR 81,8 %, SSP méd. 5,4 mois, SG méd. 9,1 mois (n = 44, 6 mg/kg, CLDN18.2 ≥ 60 %).
   - DMUC5754A : confirmé par le résumé de Liu et al., *Ann Oncol* 2016 (via ScienceDirect) et deux revues concordantes — 66 ovaires + 11 pancréas ; réponses confirmées (1 RC, 6 RP) uniquement ovariennes ; « PaC patients did not respond as well ».
   - Écart noté : la revue *World J Gastroenterol* 2026 cite une SG médiane IBI343 de 8,5 mois contre 9,1 mois à l'ASCO 2025 — différence de date de censure probable ; les deux chiffres sont rapportés dans le rapport final.
3. **Vérification mesurée sur nos cohortes** (scripts sauvegardés, sorties vérifiées) :
   - `check_expression_muc16_cldn18.py` — fractions MUC16/CLDN18 au-dessus des seuils + chevauchement avec le groupe KRAS fort, 4 cohortes, CSV de flux déjà construits (aucune reconstruction). Sorties : `expression_muc16_cldn18_check.csv` / `.txt`.
   - `check_tcga_radiation.py` — radiothérapie × CA125, jointure par patient, protocole v4 recopié, Firehose MD5 vérifié. Sortie : `tcga_radiation_ca125_check.txt`.
   - Correction d'un bug de lecture du fichier clinique pendant la vérification : le fichier `data_clinical_patient.txt` a 4 lignes de métadonnées + une ligne d'en-tête réelle (ligne 5, noms courts : PATIENT_ID, RADIATION_THERAPY, HISTORY_NEOADJUVANT_TRTYN). La première version du script a compté 185 patients (ligne d'en-tête incluse) ; corrigé : **184 patients**, radiothérapie Oui 44 / Non 123 / manquant 17, néoadjuvant Non pour les 184.
4. **Rapport final :** `muc16_cldn182_therapies.md` (ce dossier : revue + chiffres mesurés + limites + sources).

## 2. Données utilisées (déjà construites, non modifiées)

| Fichier | Contenu | SHA / vérification |
|---|---|---|
| `pdac_tcga_fluxes_v4.csv` | TCGA 178 tumeurs, résidus corrigés pureté, ordre KRAS résiduel croissant | SHA `e7a2adab…` (vérifié inchangé) |
| `pdac_geo71729_fluxes.csv` | GSE71729 145 tumeurs, log-expression puce Agilent | SHA `7d69fa88…8c0cf1` |
| `pdac_geo62452_fluxes.csv` | GSE62452 69 tumeurs, log-expression puce Affymetrix | SHA `d7419c0e…03abf` |
| `pdac_icgc_fluxes.csv` | ICGC 70 tumeurs, log2(cpm) Xena | SHA `710d41e5…b61941` |
| `data/tcga_paad_rsem.tar.gz` | Firehose PAAD RSEM, matrice d'expression | MD5 `b09569ce3f4721f514bc137bd109ac0a` (re-vérifié par le script radiation) |
| `data_clinical_patient.txt` | Clinique TCGA, 184 patients | 38 colonnes ; aucune colonne chimiothérapie |

## 3. Ce qui manque / limites nommées

- **Aucune donnée de chimiothérapie dans le fichier clinique TCGA** : la question « les CA125-élevés ont-ils reçu une chimio différente / répondu différemment ? » ne peut pas être répondue avec ce fichier. Seule la radiothérapie était testable.
- **ARN ≠ IHC** : l'expression ARN de CLDN18 (et de MUC16) n'est pas la mesure IHC protéique qui décide de l'éligibilité aux thérapies anti-CLDN18.2 / anti-MUC16. Aucun seuil ARN de ce bras ne peut dire qui serait éligible.
- **Revue web du 16 nov. 2026** : sources secondaires incluses (communiqués d'entreprise pour IBI343/IBI389/satri-cel adjuvant) ; statuts d'essais « en recrutement » datés de nov. 2026, à revérifier sur ClinicalTrials.gov avant toute citation publique ; le numéro NCT de l'essai de phase I CAR-T anti-MUC16 de Memorial Sloan Kettering (O'Cearbhaill 2020) n'a pas pu être vérifié — non cité.
- **Échelles non comparables entre cohortes** (résidus TCGA, log-expression GEO, log2cpm ICGC) : seules les fractions et les rangs à l'intérieur d'une cohorte sont comparables.
- Les chiffres de survie GLEAM (ESMO GI 2026) proviennent d'une présentation de congrès (résumé 342O), pas encore d'un article revu par les pairs au 16 nov. 2026.

## 4. Fichiers de ce bras (tous dans `~/workspace/runs/pdac-v6/`)

- `muc16_cldn182_therapies.md` — rapport final (revue + chiffres mesurés + limites + sources).
- `literature_muc16_cldn182_draft.md` — brouillon de la revue (31 sources, §5 points non vérifiés).
- `PROVENANCE_muc16_cldn182.md` — ce fichier.
- `check_expression_muc16_cldn18.py` + `expression_muc16_cldn18_check.csv` / `.txt`.
- `check_tcga_radiation.py` + `tcga_radiation_ca125_check.txt`.

## 5. Règle respectée

Aucune conclusion importée d'autres expériences : les chiffres de ce bras et les sources citées font le verdict. Un médicament approuvé dans un autre cancer (zolbetuximab en gastrique, oregovomab/abagovomab en ovaire) n'est jamais présenté comme une preuve pancréatique.
