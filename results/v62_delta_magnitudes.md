# Modélisation des magnitudes — chantier 3 (suite), §8.42

Protocole gelé : `PROTOCOL_delta_magnitudes.md`,
SHA-256 `2562ee22dd38c0a5e8f4f52a76cc89ccb2d85c4c38abb4f6edf7ab4cba3b0419`
(amendé avant toute exécution : ajout du 7e trait inter-flux, part
PC1+PC2, qui manquait dans l'énumération ; totaux 41/80 inchangés).
Script : `v62_delta_magnitudes.py`,
SHA-256 `cefedf77bc7e1d01cc12c604e3227b7b6539f2f4a67dbd2343f402e2e861debc`.
Supplément descriptif : `v62_delta_magnitudes_m4_features.py` (nomme le
meilleur trait unique par cible, règle M4, 222 runs).

## Verdict §5.4 — NON ÉLUCIDÉ

Aucun des 4 modèles gelés n'atteint ≥ 90 % paires ET ≥ 90 % valeurs, ni en
leave-one-cohort-out (LOCO, primaire), ni en split aléatoire par matrice.
Le meilleur hold-out honnête (LOCO, paires) est M2 à 68,9 % ; le meilleur
hold-out honnête (valeurs) est M3 à 6,3 % en LOCO et 42,4 % en split.
**Delta reste non élucidé, piste fragile, pas un discriminateur recommandé.**

## Résultats (paires non ordonnées / valeur d_div ±0,10)

| Hold-out | Modèle | Paires | Valeurs | MAE d_div | 3-voies |
|---|---|---|---|---|---|
| LOCO (222 runs) | B0 constante | 136/222 (61,3 %) | 0/222 (0,0 %) | 2,129 | 56,2 % (= majorité) |
| LOCO | **M1 ridge λ=10, réduit (primaire)** | 136/222 (61,3 %) | 5/222 (2,3 %) | 1,180 | 56,2 % |
| LOCO | M2 ridge λ=10, complet | 153/222 (68,9 %) | 2/222 (0,9 %) | 1,163 | 65,9 % |
| LOCO | M3 kNN k=5 | 134/222 (60,4 %) | 14/222 (6,3 %) | 1,479 | 55,1 % |
| LOCO | M4 meilleur trait unique | 136/222 (61,3 %) | 0/222 (0,0 %) | 0,967 | 54,0 % |
| Split matrices 70/30 (66 runs) | B0 | 38/66 (57,6 %) | 16/66 (24,2 %) | 0,949 | 55,6 % |
| Split matrices 70/30 | M1 | 55/66 (83,3 %) | 15/66 (22,7 %) | 0,303 | 83,3 % |
| Split matrices 70/30 | M2 | 52/66 (78,8 %) | 12/66 (18,2 %) | 0,313 | 77,8 % |
| Split matrices 70/30 | M3 | 48/66 (72,7 %) | 28/66 (42,4 %) | 0,352 | 70,4 % |
| Split matrices 70/30 | M4 | 41/66 (62,1 %) | 0/66 (0,0 %) | 0,518 | 57,4 % |
| Version v6.1→v6.2 — FUITE (66 runs) | M1 | 49/66 (74,2 %) | 14/66 (21,2 %) | 0,289 | 75,9 % |
| Version v6.1→v6.2 — FUITE | M2 | 51/66 (77,3 %) | 19/66 (28,8 %) | 0,258 | 77,8 % |
| Version v6.1→v6.2 — FUITE | M3 | 50/66 (75,8 %) | 19/66 (28,8 %) | 0,385 | 74,1 % |
| En-échantillon (222 runs) | M3 (meilleur) | 181/222 (81,5 %) | 113/222 (50,9 %) | 0,189 | 76,7 % |

LOCO par pli (M1, paire/valeur) : coad 1,00/0,00 (n=4) ; cptac 0,00/0,00
(n=8) ; depmap 0,97/0,07 (n=30) ; geo62452 1,00/0,00 (n=14) ; geo71729
0,80/0,00 (n=20) ; hp35 0,50/0,00 (n=6) ; icgc 1,00/0,00 (n=10) ; luad
1,00/0,00 (n=4) ; **tcga 0,44/0,02 (n=126 — le pli dominant échoue)**.

## Par cible, LOCO poolé (R² / MAE)

- M1 : tous les R² sont NÉGATIFS (pire que la constante du train) :
  LevinaBickel −1,85/1,39 ; PCAIntrinsic −7,44/1,37 ; LocalPCA −0,95/0,99 ;
  GraphDimension −4,60/0,24 ; PersistentHomology −3,47/0,53 ; MFA −0,76/1,74 ;
  Higuchi −3,14/0,017 ; Katz −3,63/0,045 ; Petrosian −3,59/0,014 ;
  Sevcik −3,60/0,064 ; BoxCounting −3,77/0,58 ; Hurst2mH −2,98/0,095 ;
  DFA −2,50/15,35 (MAE dominée par les extrêmes, dont −38,16).
- M4 (un seul trait) : seuls R² positifs — LevinaBickel +0,47/0,66 ;
  GraphDimension +0,56/0,096 ; MFA +0,25/1,17 ; Petrosian +0,75/0,005 ;
  Katz +0,61/0,018 ; Sevcik +0,56/0,029 ; BoxCounting +0,58/0,25. Mais
  LocalPCA −0,16/0,84, PCAIntrinsic −1,81/0,99, PersistentHomology
  −0,26/0,31, Higuchi −0,15/0,014, Hurst2mH −3,81/0,14, DFA −3,64/18,80.
  **LocalPCA — toujours dans la paire — n'est prédite par aucun modèle
  en LOCO : la paire ne peut pas être élucidée.**
- MFA exact (snapé sur les 9 valeurs du train) en LOCO : 22,5 % (M1/M2),
  13,5 % (M3), 18,9 % (M4) ; en split 45–55 % ; en échantillon 59,5 %
  (M3). MFA n'est pas prédite par les résumés de flux entre cohortes.

## Le trait qui porte (supplément descriptif, 222 runs)

Le meilleur trait unique (Pearson) est `log(n)` pour 12 cibles sur 13 :
LevinaBickel r=+0,868 ; LocalPCA +0,824 ; GraphDimension +0,852 ;
MFA +0,847 ; Katz −0,922 ; Petrosian −0,949 ; Sevcik +0,886 ;
BoxCounting +0,932 ; Hurst2mH +0,689 ; DFA +0,547 ; PersistentHomology
+0,655 ; PCAIntrinsic +0,455 (seul Higuchi échappe : moyenne des
autocorrélations lag-1, r=−0,590). **Les magnitudes portent l'échelle de
n, pas le contenu des flux.** Comme chaque cohorte a son propre n (45,
69, 70, 145, 178, 285, 515, 1000), tenir une cohorte à l'écart, c'est
tenir ses n à l'écart : l'extrapolation échoue. En split (mêmes cohortes
des deux côtés), M1 atteint 83,3 % de paires — l'information est
cohorte-locale, pas portable.

## Résidu intra-groupe (LOCO)

- Groupe (LP, MFA 6,0, n=178), n=62 : r(prédit, vrai) = +0,06 (M1),
  écart-type résiduel 0,98 ; d_div vrai 4,62–5,46.
- Groupe (LP, MFA 7,0, n=178), n=53 : r = +0,14 (M1), résiduel 0,92 ;
  d_div vrai 5,58–6,13.
- Corrélation intra-groupe poolée (groupes ≥ 10 runs, n=183) : r = +0,09
  (M1), −0,10 (M2, M3, M4). **Le résidu est intra-groupe et imprévisible
  par ces résumés : à groupe structurel fixé, le modèle ne voit plus
  rien.** M4 prédit ~la constante du groupe (résiduel 0,29 / 0,11, r ≈ 0) :
  il retrouve le niveau, pas la variation.

## Contrôles d'honnêteté

- Invariance réel/nul : traits invariants (marginales par flux +
  corrélations inter-flux + PC) égaux à 10⁻⁹ près sur **78/78** paires
  de matrices → le nul permute les lignes **conjointement** (la structure
  de corrélation est préservée) ; seuls les traits sensibles à l'ordre
  diffèrent. Paire prédite identique réel vs nul (LOCO M1, même version) :
  101/121 (83,5 %) — cohérent avec §8.39 H10 (la vraie paire est
  insensible à la permutation).
- Déduplication (153 runs, §8.39.6), LOCO M1 : 58,2 % / 2,6 % — stable,
  pas un artefact de duplication.
- Variante masque ignoré (k=6 forcé), LOCO M1 : 59,9 % / 2,3 % — le
  masque n'est pas le blocage.
- Sensibilité λ (M1, LOCO) : λ=1 → 55,4 % / 1,4 % ; λ=100 → 61,3 % /
  4,1 %. Aucun λ ne sauve le modèle.
- d_sat seule : ±0,10 en LOCO 22,1 % (M1) / 56,3 % (M3) ; en split
  90,9 % (M3) — d_sat, quasi constante par famille, se prédit bien
  intra-cohorte, mais cela ne sauve pas d_div.
- Version hold-out (FUITE, mêmes matrices) : même fuité, aucun modèle ne
  dépasse 28,8 % en valeur. Attention : ce test mesure ces classes de
  modèles (ridge/kNN ne mémorisent pas), pas l'information contenue dans
  les matrices — un modèle mémorisant scorerait 100 % sur X identique.
  Il ne prouve pas l'absence d'information, il prouve l'échec de ces
  résumés + ces modèles.

## Ce qui reste ouvert

1. **Modéliser depuis les séries entières, pas des résumés.** Les
   estimateurs sont des fonctionnelles non linéaires de la série ordonnée
   complète ; 41 résumés (moyennes, corrélations, PC) ne les déterminent
   pas entre cohortes. Une voie serait d'apprendre les magnitudes depuis
   les séries elles-mêmes (ou depuis des fonctionnelles proches des
   estimateurs) — nouveau protocole, go requis, et risque circulaire à
   surveiller : un modèle trop proche de l'estimateur le recalcule, il ne
   l'explique pas.
2. **L'échelle de n.** `log(n)` porte presque toute l'information
   transférable mesurée ici. Comprendre POURQUOI chaque estimateur croît
   (ou décroît) avec n — loi d'échelle propre à chaque estimateur — est
   une question analytique, pas un modèle de plus.
3. **d_sat.** Prédite à 90,9 % ±0,10 en split (M3) mais 56,3 % en LOCO :
   même limite de portabilité entre cohortes.
4. **Delta reste une piste fragile** (6/8 phase 2, échec HP35) ; son
   6/8 ne devient pas un critère de décision.

## Provenance (§8.42)

- Protocole gelé `PROTOCOL_delta_magnitudes.md`, SHA-256
  `2562ee22dd38c0a5e8f4f52a76cc89ccb2d85c4c38abb4f6edf7ab4cba3b0419`.
- Script `v62_delta_magnitudes.py`, SHA-256
  `cefedf77bc7e1d01cc12c604e3227b7b6539f2f4a67dbd2343f402e2e861debc` ;
  supplément `v62_delta_magnitudes_m4_features.py` (descriptif).
- Sorties : `v62_delta_magnitudes.log`, `v62_delta_magnitudes.json`,
  `v62_delta_magnitudes_flux_features.csv` (traits par matrice + SHA-256
  de chaque matrice), `v62_delta_magnitudes_m4_features.json` / `.log`.
- Pipelines vérifiés avant travail, jamais modifiés : v6.2
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
  v6.1 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`,
  v6 `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`.
  **Aucun run du pipeline dans ce chantier.**
- Données : 222 `master_results.json` (156 v6.1 + 66 v6.2) ;
  `v62_delta_levels.csv` comme base de cibles ; 156 matrices de flux
  distinctes (9 cohortes : tcga 100, depmap 26, geo71729 10, geo62452 6,
  cptac 4, icgc 4, coad 2, luad 2, hp35 2), SHA-256 notés dans
  `v62_delta_magnitudes_flux_features.csv`. Nuls = lignes permutées
  conjointement, graine 42, colonne de contrôle intacte (vérifié 78/78).
- Ce qui manque : l'identité du meilleur trait M4 par pli LOCO n'est pas
  enregistrée (seulement sur les 222 runs, supplément) ; les traits sont
  des résumés, pas les séries complètes ; aucune cohorte entièrement
  nouvelle au-delà des 9 n'est testée ; `df_feat.csv` volontairement
  exclu (circulaire).
- Date de rédaction : 19 novembre 2026. Auteur : TagPrint.
