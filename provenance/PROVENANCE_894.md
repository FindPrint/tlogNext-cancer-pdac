# Provenance — §8.94 : élucider Delta, nouvelle tentative

Date : 21 novembre 2026. Statut : **SQUELETTE — protocole gelé, AUCUN calcul neuf à ce jour.** À compléter par les résultats, sans réécrire ce fichier (addenda datés seulement).

## 1. Protocole gelé

- `PROTOCOL_delta_elucidation_894.md`, SHA-256 `79e5567c19d90cdd78d39f4d90888b5e8d00c5a25f56f7ac5789a8dd9bc5229d`.
- Go de Zackary « Faite tout cela », 21 nov. 2026 11h36, piste 2/4. Coordinateur : TagPrint.

## 2. Code (vérifié avant gel, inchangé)

- Pipeline v6.2 `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
- v6.1 SHA `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ; v6 SHA `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`.
- À compléter : SHA de `v62_delta_elucidation_894.py`, des JSON/CSV de résultats.

## 3. Données d'entrée (détenues, relues)

- `v62_delta_levels.csv` : 222 runs (156 v6.1 + 66 v6.2), 223 lignes avec en-tête — ensemble gelé des §8.39/§8.42/§8.57.
- Ensemble B (§8.62) : 31 runs v6.2 fast (HP35 réel/nul, LUAD, TCGA v4).
- `df_feat.csv` présent dans 222/222 dossiers de run ; `fluxes_raw.csv` présent dans 222/222.
- Coefficients F2(ln n) repris du §8.62, NON ré-estimés (à citer avec leur SHA au moment du calcul).
- Pistes non closes inventoriées : §8.39/§8.42 (paire médiane + d_div), M1c (§8.63), M2d (§8.63/§8.75), §8.57 (séries complètes), §8.62 (résidu après loi en n, jamais testé seul), §8.73 (déclencheur du pic étroit), Delta à w égal (neuf, suite de §8.63 M1 : +0,7 entre w=27 et w=30).
- Barres : critère §8.39 — paire médiane ≥ 90 % ET d_div à ±0,10 près sur ≥ 90 % des runs, en hold-out LOCO, vérifié sur l'ensemble B.
- À compléter : SHA des fichiers d'entrée relus, résultats A1–A4, vérifications préalables (d_div à 10⁻³, raw_median à 10⁻⁶).

## 4. Ce qui manque (déclaré)

- Tout le reste : aucun calcul, aucune modélisation à ce jour. Aucun nouveau run pipeline prévu (lecture seule des sorties détenues ; si un angle exige un run neuf, il s'arrête et le besoin est consigné).
