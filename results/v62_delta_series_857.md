# §8.57 — Delta depuis les séries complètes (résumé d'exécution)

Date : 19 novembre 2026 (exécution 20 nov. 2026, ~03h22).
Protocole gelé : `PROTOCOL_delta_series_857.md`,
SHA-256 `965a88dc90c8af0ca701af2da1c31d124ceccef059d13a0972fae15ba6266bdc`.
Script : `v62_delta_series_857.py`,
SHA-256 `59c1b78b4cdc0d2997660f9eb953a7b605b8575cc2c1ed2fd220d0a8dbb964f0`.
Lecture seule, aucun run du pipeline, aucun code modifié.

## Vérifications préalables (toutes passées)

- C0 (diagnostic circulaire) : recomputation de la médiane-de-médianes
  depuis la série complète `df_feat.csv` = `raw_median` à 10⁻⁶ près sur
  **2886/2886** (222 runs × 13 cibles). La série complète recalcule la
  cible exactement : elle est exclue du critère, comme gelé.
- Identités d_div / d_sat depuis les médianes parsées : 0 écart > 10⁻³
  sur 222/222.
- `df_feat.csv` présent dans 222/222 dossiers, 120 lignes partout,
  60 lignes Progress ≤ 50 partout. 156 matrices lues pour S4, 0 colonne
  NaN, 0 écart n matrice vs n run.
- Cibles manquantes : 70 (LevinaBickel 41, PersistentHomology 29) — le
  masque, comme au §8.42.
- Déduplication vérifiée : 153 runs (sans rep2, sans doublons div_sorted).

## Résultats (paires / valeurs ±0,10)

| Hold-out | Modèle | Paires | Valeurs | MAE d_div | 3-voies |
|---|---|---|---|---|---|
| LOCO (222) | B0 | 136/222 (61,3 %) | 0/222 (0,0 %) | 2,129 | 56,2 % |
| LOCO | **S1d préfixe direct** | 189/222 (85,1 %) | 188/222 (84,7 %) | 0,061 | 81,3 % |
| LOCO | S1r ridge préfixe | 119/222 (53,6 %) | 43/222 (19,4 %) | 0,304 | 55,7 % |
| LOCO | **S2d demi-flux direct** | **198/222 (89,2 %)** | **201/222 (90,5 %)** | **0,037** | **86,4 %** |
| LOCO | S2r ridge demi-flux | 116/222 (52,3 %) | 54/222 (24,3 %) | 0,434 | 55,1 % |
| LOCO | S3r ridge trans-estimateur | 113/222 (50,9 %) | 22/222 (9,9 %) | 2,403 | 52,8 % |
| LOCO | S4r ridge séries de flux | 139/222 (62,6 %) | 2/222 (0,9 %) | 1,027 | 55,7 % |
| LOCO | S4k kNN séries de flux | 138/222 (62,2 %) | 5/222 (2,3 %) | 1,373 | 58,0 % |
| Split matrices (66) | S1d | 60/66 (90,9 %) | 53/66 (80,3 %) | 0,074 | 88,9 % |
| Split matrices | **S2d** | **59/66 (89,4 %)** | **59/66 (89,4 %)** | **0,037** | **87,0 %** |
| Split matrices | S1r / S2r / S3r / S4r / S4k | 77,3 / 72,7 / 65,2 / 63,6 / 69,7 % | 60,6 / 77,3 / 34,8 / 13,6 / 34,8 % | — | — |
| Version v6.1→v6.2 — FUITE (66) | S2d | 59/66 (89,4 %) | 61/66 (92,4 %) | 0,031 | 87,0 % |
| En-échantillon (222) | S2d (= LOCO, sans apprentissage) | 198/222 (89,2 %) | 201/222 (90,5 %) | 0,037 | 86,4 % |

## Verdict

**NON ÉLUCIDÉ.** Aucun modèle honnête n'atteint paires ≥ 90 % ET valeurs
≥ 90 % sur le LOCO poolé ET sur le split par matrice. Le meilleur,
S2d (médiane sur la moitié des flux), manque le critère de **2 runs en
LOCO (paires : 198/222 au lieu de 200)** et de **1 run en split (paires
et valeurs : 59/66 au lieu de 60)**. S1d passe les paires en split
(60/66) mais échoue partout ailleurs.

## Ce qui résiste (analyse)

- La dérive demi-flux est concentrée sur LevinaBickel (46,4 % ≤ 0,10,
  écart moyen 0,155) et PersistentHomology (56,8 %, 0,105) — les deux
  estimateurs masqués, dont les médianes par flux varient le plus d'un
  flux à l'autre. Sur les 24 échecs de paire S2d (LOCO), 13 ont pour
  vraie paire LocalPCA+LevinaBickel, 8 LocalPCA+PCAIntrinsic, 3
  LocalPCA+MFA ; LevinaBickel figure dans la vraie ou la prédite paire
  sur 17/24. Dérive |demi−complet| de LevinaBickel : moyenne 0,190 /
  médiane 0,197 sur les échecs, contre 0,150 / 0,094 sur les réussites.
- Échecs concentrés dans le pli tcga (paires 106/126, valeurs 108/126)
  et geo71729 (16/20, 18/20) ; tous les autres plis sont à 100 % en
  paires pour S2d, sauf depmap en valeurs (29/30).
- Le résidu intra-groupe, imprévisible au §8.42 (r = +0,06 / +0,14),
  est CAPTURÉ par S2d : r = 0,977 dans (LP, MFA 6,0, n=178, n=62),
  0,726 dans (LP, MFA 7,0, n=178, n=53), 0,937 poolé (groupes ≥ 10,
  n=183). Ce qui reste, ce n'est plus le niveau intra-groupe, c'est le
  basculement de la paire sur les cas limites.
- Les modèles appris (ridge) font PIRE que les fonctionnelles directes
  (S1r 53,6 % / 19,4 % contre S1d 85,1 % / 84,7 %) : les poids appris
  sur 8 cohortes explosent sur la 9e (R² LOCO jusqu'à −35 pour MFA,
  −388 pour Hurst2mH). L'apprentissage dégrade l'information que la
  médiane partielle porte déjà.
- S4 (séries de flux entières, seule voie à contenu indépendant) échoue
  comme les résumés du §8.42 : 62,6 % / 0,9 % (ridge), 62,2 % / 2,3 %
  (kNN) en LOCO. La pleine résolution n'ajoute rien.
- S3r (préfixe des 12 autres estimateurs, aucune info de la cible) :
  50,9 % / 9,9 % en LOCO — pas de redondance inter-estimateurs.
- d_sat est entièrement déterminée par la moitié des flux : S2d
  222/222 (100 %) en LOCO, 66/66 en split.
- Paire prédite identique réel/nul (LOCO, S2d) : 66/106 (62,3 %) —
  moins que §8.42 M1 (101/121, 83,5 %) : la prédiction demi-flux est
  plus bruitée que la paire complète (H10).
- Déduplication S2d (LOCO, 153 runs) : 137/153 (89,5 %) / 137/153
  (89,5 %) — stable. Masque ignoré : 89,2 % / 90,5 % — inchangé.
  Sensibilité λ S1r : λ=1 → 58,1 % / 47,3 % ; λ=100 → 51,8 % / 7,2 %.
- Un seul cas de repli gelé (médiane du train) : PersistentHomology sur
  `results_fast_v61_depmaprot_aco2` (1 seul flux fini, d'indice impair,
  donc demi-flux indéfini) ; sans ce repli, S2d LOCO serait à 197/222
  (88,7 %) en paires.

## Fichiers

- `v62_delta_series_857.py` (SHA `59c1b78b…64f0`), `.log` (SHA
  `7916fdd3…e8ed8`), `.json` (SHA `c41e1310…31`), `.md` (ce fichier),
  `v62_delta_series_857_features.csv` (SHA `5e515fd2…c4e`, 222 runs :
  médianes préfixe / demi-flux / complètes par cible, SHA df_feat et
  SHA matrice).
- Section : `section_8.57_delta_series.md`.
