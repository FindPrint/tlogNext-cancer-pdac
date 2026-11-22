# Provenance — §8.95 : score composite gelé, candidate v6.5

Date : 21 novembre 2026. Statut : **SQUELETTE — protocole gelé, AUCUN calcul du candidat, AUCUN code v6.5 écrit à ce jour.** À compléter par les résultats, sans réécrire ce fichier (addenda datés seulement).

## 1. Protocole gelé

- `PROTOCOL_composite_v65_895.md`, SHA-256 `f3fcb38ef1d6ce68a14369ccd2a2baa62520fe124641ff8c411eb87692c66ece`.
- Go de Zackary « Faite tout cela », 21 nov. 2026 11h36, piste 3/4. Coordinateur : TagPrint.

## 2. Code (vérifié avant gel, inchangé)

- Pipeline v6.2 `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
- v6.1 SHA `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ; v6 SHA `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`.
- v6.3 et v6.4 (recompositions MC REJETÉES, §8.49 et §8.52) : présentes dans le même dossier, jamais modifiées, jamais réutilisées comme base (la v6.5 est une COPIE de v6.2).
- À compléter : SHA de la copie `universal_v6.5.0_cohen.py` (avant/après), diff contre v6.2, SHA de `extract_c65.py` et du second script de re-extraction, SHA de v6.2/v6.1/v6/v6.3/v6.4 revérifiés après travaux.

## 3. Règle de combinaison gelée (avant tout test)

```
C_pair = (maxsep_R − maxsep_N)
       + 0,50 × (MC_R − MC_N)
       + 0,50 × (robustness_R − robustness_N)
       + 0,25 × (L7a_R − L7a_N)
```
Poids gelés (1 / 0,50 / 0,50 / 0,25), jamais ré-estimés après lecture d'un chiffre. Rescore sans toucher à la sélection (seuil, cascade, S_sep, Delta inchangés par construction).

## 4. Données d'entrée (détenues, relues)

- Mêmes 60 paires que §8.56 (8 principales V1 + 48 rotations sans doublon V2 + Test A V3 + MTAP V4 + pureté V5), lues dans les `master_results.json` v6.2 déjà sur disque — AUCUN nouveau run pour le score.
- Références de barres : ancien MC (rotations 12/48, principales 1/8, HP35 +0,1950) ; v6.3 (31/48, 4/8, +0,2271) ; v6.4 (28/48, 4/8, +0,5529) ; `maxsep` §8.56 (37/48, 6/8, HP35 +1,6512).
- Barres C1–C4 : rotations ≥ 30/48 ; principales ≥ 6/8 et ≥ 7/8 positifs ; HP35 ≥ 0,30 (unités C) ; relecture exacte 0,0 sur 120/120 + concordance tables v63/v64/856 à 1e-9 + SHA inchangés.
- À compléter : `c65_table.json` (60 paires), sensibilités (C1 à 24/48 ; planchers 0,05/0,10 ; C sans L7a ; C sans robustesse), contrôles descriptifs V3–V5.

## 5. Ce qui manque (déclaré)

- Tout le reste : aucun calcul, aucun code v6.5 à ce jour. L'adoption finale, même si les 4 portes passent, reste à Zackary — ce chantier ne crée qu'une candidate.
