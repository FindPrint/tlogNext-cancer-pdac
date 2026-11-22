# Provenance — §8.93 : chaque paire jugée contre une distribution de nuls

Date : 21 novembre 2026. Statut : **SQUELETTE — protocole gelé, AUCUN calcul, AUCUN run lancé à ce jour.** À compléter par les résultats, sans réécrire ce fichier (addenda datés seulement).

## 1. Protocole gelé

- `PROTOCOL_nulls_distribution_893.md`, SHA-256 `d2cdbc3d589d3be61a506f7be2a250d3d4a1c9adc21d1327c8ffc7a61f6529a0`.
- Go de Zackary « Faite tout cela », 21 nov. 2026 11h36, piste 1/4. Coordinateur : TagPrint.

## 2. Code (vérifié avant gel, inchangé)

- Pipeline v6.2 `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
- v6.1 SHA `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ; v6 SHA `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`.
- À compléter : SHA de `replica_nulls_893.py`, des JSON de vérification, des CSV bruts, des tables.

## 3. Données d'entrée (relues, jamais recalculées ici)

- Table A2 (§8.88.3, livre blanc) : 10/15, 12/15 positifs, LOO 9/14 — reprise telle quelle.
- Faits de départ : §8.53 (≈200 nuls pour un plancher stable à n≈70) ; §8.47 (réplique 500 permutations) ; §8.50 (10/10) ; §8.70/§8.72 (renverses).
- Faisabilité vérifiée avant gel : 200 nuls pipeline × 15 paires = 3 000 runs ≈ 250 h — INFAISABLE ; voie principale = réplique 1000 permutations (précédent §8.47/§8.53) + 10 nuls frais pipeline par paire en validation (80 runs étape 1 ≈ 7 h ; 70 runs étape 2 ≈ 6 h).
- Graines gelées : réplique 3000–3999, maître `default_rng(20261121)` ; nuls frais pipeline 9101–9110.
- À compléter : SHA des CSV de flux par paire (vérifiés contre les provenances publiées avant la calibration), SHA des sorties, lots systemd, exit codes.

## 4. Ce qui manque (déclaré)

- Tout le reste : aucun calcul, aucun run, aucune table à ce jour. Les résultats seront ajoutés par addendum daté, avec leurs SHA.
