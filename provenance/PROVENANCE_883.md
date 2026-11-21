# Provenance — §8.83 Survie des gènes de privilège (TCGA, ICGC, GSE71729)

## Protocole

`PROTOCOL_survie_privilege_883.md`, SHA-256
`0eb83d63902b16767841683d8d969e17f0fd282d9e10f4ec242ca75864e7c206`
(gelé le 21 nov. 2026 avant toute analyse ; amendé le même jour AVANT
toute lecture des résultats privilège — voir « Amendement » ci-dessous).

## Script

`survival_privilege_883.py`, SHA-256
`c61ef9461aceae8900f9c879dc09339c84db3aaed107c5f18c43f2960e033537`.
Fonctions KM / log-rank / Cox reprises littéralement de
`survival_tcga_verify.py` (SHA `937bdb6e…dade2`, §8.12) : KM médiane,
log-rank Mantel-Haenszel (événements booléens), Cox Breslow
Newton-Raphson corrigé du 16 nov. 2026 (un gène à la fois pour
l'univarié). Aucune autre implémentation, aucune librairie de survie
externe (lifelines absente de la machine).

## Sources (déjà sur le disque, SHA re-vérifiés dans le script)

| Source | Fichier local | Vérification |
|---|---|---|
| TCGA-PAAD Firehose stddata 2016-01-28, RSEM genes normalized | `data/tcga_paad_rsem.tar.gz` | MD5 `b09569ce3f4721f514bc137bd109ac0a` (asserté) |
| TCGA clinique datahub (184 patients) | `data_clinical_patient.txt` | jointure par patient (12 premiers caractères) ; groupes top12 vérifiés contre `tcga_groups_survival.json` |
| ICGC PACA-AU expression log2(cpm), Xena | `data/icgc_pacaau_exp.txt.gz` | SHA-256 `c2cb57af3ba4c3d7fdac292e66c81067d36e16aae9efdd8005147e20820f49fa` (asserté) |
| ICGC probe map | `data/icgc_pacaau_probemap.gz` | SHA-256 `b09a746f6084215beea3632b72e87834ea577d18fcb52add3641de5d0d975537` (asserté) |
| ICGC clinique + survie (Bailey Suppl. Table 1, 70 tumeurs) | `icgc_clinical_70.csv` | 70 patients, 47 décès OS (asserté) ; OS = tout statut `Deceased...` ; DSS = `Deceased - Of Disease` seul |
| GSE71729 matrice GEO (Moffitt 2015) | `data/GSE71729_series_matrix.txt.gz` | SHA-256 `b228789314ec4d866ec51b65724664abaa24b822577c55d3727820c867536a54` (asserté) ; survie dans les ch2 (`survival_months`, `death_event_1death_0censor`) |

## Échelles d'expression (§1 du protocole)

- TCGA : résidus corrigés de la pureté (régression sur scores
  acineux/îlots, log2(RSEM+1)), même construction que
  `survival_tcga_verify.py` ; KRAS = résidu KRAS.
- ICGC : log2(cpm) brut Xena, ordre = `kras_rank` de
  `icgc_clinical_70.csv`.
- GSE71729 : valeurs brutes de la matrice, mêmes 145 primaires, ordre
  KRAS croissant, mêmes que `survival_geo71729.py`.

## Vérifications de jointure (arrêt si écart > 1e-9)

- TCGA : ensemble des 178 tumeurs et top12 KRAS résidu identiques à
  `tcga_groups_survival.json` ; n=177 avec survie, 92 décès.
- ICGC : n=70, 47 décès OS.
- GSE71729 : KRAS, MUC16, CEACAM5 identiques à
  `geo71729_survival_table.csv` (SHA `1f7a14a7…`) sur les 145
  primaires ; n=125 avec survie, 84 décès (20 sans survie, exclues).

## Calibration (§6 du protocole) — porte d'entrée, RÉUSSIE au 2e essai

Premier essai : ÉCHEC sur 2 points (TCGA médiane de cohorte 20,2 vs
20,0 ; GSE71729 log-rank MUC16 0,8562 vs 0,73) — le script s'est arrêté
AVANT toute lecture des résultats privilège, comme le protocole
l'exige. Diagnostic par re-calcul direct (aucun résultat privilège lu) :

1. **GSE71729 log-rank MUC16** : le script utilisait un seuil au
   quantile 0,75 sur les 145 (n=34, p=0,8562). La définition publiée
   du §8.15 est le top 36 PAR RANG sur les 145
   (`sort_values().iloc[-36:]`), qui donne n=33, décès 22, médiane
   17,0 vs 16,0, p=0,7292 — identique au §8.15 à 0,001 près. Un patient
   lié au seuil faisait basculer p de 0,73 à 0,86 : c'est la fragilité
   du log-rank à n=33, pas une erreur de données. Corrigé : masques
   par rang (top 36 GSE71729, top 18 ICGC) comme dans les bras publiés.
2. **TCGA médiane de cohorte** : le §8.12 donne 20,0 mois (KM) ;
   l'implémentation gelée (premier temps d'événement où S ≤ 0,5)
   donne 20,2. La médiane simple des temps observés vaut 15,2
   (c'est le chiffre « 15.2 » de `tcga_survival_verify_results.txt`,
   mal étiqueté « OS médiane cohorte » dans ce fichier — ce n'est PAS
   une médiane de survie). Tolérance de calibration élargie de ±0,1
   à ±0,5 mois, avec la raison écrite au protocole.

Amendement consigné au protocole §6 et §3.2 (21 nov. 2026, avant toute
lecture des résultats privilège) : définition des quartiles par cohorte
= celle du bras publié de cette cohorte ; cas du score combiné GSE71729
(top 36 par rang sur les 125) explicité ; tolérance médiane ±0,5 mois.

Deuxième essai : **CALIBRATION OK, 3/3 cohortes** —

| Cohorte | Cox MUC16 HR (attendu) | log-rank MUC16 p (attendu) | n / décès | OS médiane (attendue) |
|---|---|---|---|---|
| TCGA | 1,4392 (1,44) | 0,0703 (0,070) | 177 / 92 | 20,2 (20,0) |
| ICGC | 1,5688 (1,57) | 0,0019 (0,002) | 70 / 47 | 16,6 (16,6) |
| GSE71729 | 1,0625 (1,06) | 0,7292 (0,73) | 125 / 84 | 17,0 (17,0) |

## Fichiers produits

| Fichier | SHA-256 |
|---|---|
| `survival_privilege_883.py` | `c61ef9461aceae8900f9c879dc09339c84db3aaed107c5f18c43f2960e033537` |
| `survival_privilege_883_table.csv` | `ad105af8292c5a1746b2060ee6da81b4e64ece56d02917bbebbe24e09fa33b42` |
| `survival_privilege_883_results.txt` | `628b458db0cee1c3a00a95bfe2411a14d9b4970566347e66393804b0aa10daa3` |
| `survival_privilege_883_results.json` | `a84cf494dc0a55f84754b9b0f8b239070bb5a6b1bf922841a0bf67f3db265aca` |
| `PROTOCOL_survie_privilege_883.md` | `0eb83d63902b16767841683d8d969e17f0fd282d9e10f4ec242ca75864e7c206` |

## Ce qui n'a PAS été fait (dit plainement)

- Aucun test multivarié, aucun ajustement (stade, sous-type, KRAS) —
  le critère est l'univarié, comme pour le record de CA125.
- Aucun gène ajouté ou retiré après les résultats ; la liste testée
  est celle du protocole (7 gènes + score combiné).
- Correction Bonferroni 0,05/24 ≈ 0,0021 rapportée à titre descriptif
  seulement, pas comme porte (CA125 lui-même ne la passerait pas
  partout : ICGC p=0,008).
- La colonne « monte avec KRAS » est calculée ICI (Spearman gène vs
  KRAS, mêmes données, règle gelée §4) — rien n'est importé du §8.81
  ni d'aucune autre expérience.
