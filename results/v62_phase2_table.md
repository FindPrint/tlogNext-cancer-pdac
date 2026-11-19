# Phase 2 — discrimination reel / nul : sorties v6.2 (PROTOCOL_v6.2.md §6)

Protocole gele : `PROTOCOL_v6.2.md` §6 (phase 2 : `PROTOCOL_phase2_discrimination.md`, 16 nov. 2026). Pipeline : `universal_v6.2.0_cohen.py`, SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`, jamais modifie. **Aucun nouveau run du pipeline au-dela du §5** : tout est lu dans les `master_results.json` v6.2 deja sur disque (10 runs de validation x 2 + 46 runs phase 2, 66 dossiers ; 3 redemarrages machine pendant les lots, reprise par le lanceur reprenable). Nul : lignes permutees, graine 42, colonne de controle intacte. Extracteur : `extract_phase2_v62.py` (copie de `extract_phase2.py`, SHA `5eb3ac24…75aa`, etendue du 9e indicateur S_sep), log `v62_phase2_extract.log`. Donnees brutes : `v62_phase2_table.csv` et `v62_phase2_table.json`.

## Gigues appliquees (mesurees en validation v6.2, §5 — pas le forfait ±0,07)

- MC best_score : gigue mesuree **0.0** (v6.1 : forfait 0,07).
- max_separation : gigue mesuree **0.0** (v6.1 : forfait 0,07).
- L7a (confiance signee) : gigue mesuree **0.0** (v6.1 : forfait 0,07).
- S_sep : gigue effective = max(gigue mesuree 0,00 ; plancher 0,07) = **0.07** (§3.4).
- Delta, cascade, falsification : gigue 0 (deterministes).

**Lecture honnete, a garder en tete pour tout le tableau :** la gigue mesuree est 0, donc pour MC, max_separation et L7a, « ecart > gigue » devient « ecart non nul ». Les ecarts eux-memes sont **identiques** a ceux de la v6.1 au chiffre pres (voir § Comparaison) : l'instrument n'a pas change, c'est la regle qui a change. Un 7/8 en v6.2 la ou la v6.1 donnait 1/8 ne veut PAS dire que le pipeline separe mieux — il veut dire que le meme ecart, mesure contre une gigue 0 au lieu de 0,07, passe le seuil.

## Table principale — valeurs reel / nul (ecart reel−nul), v6.2

| Paire | n | Delta R/N (ecart) | MC score R/N (ecart) | MC seuil R/N % | max_sep R/N (ecart) | stab. R/N | S_sep R/N (ecart) | T_0 R/N % (|ecart|) | fals R/N | frac. coh. R/N | |d| med. R/N | L7a R / N | Σ|Δ| casc. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HP35 | 1000 | 4.48 / 4.57 (-0.09) | 0.6035 / 0.4086 (0.1950) | 6.62 / 4.91 | 1.7718 / 0.1206 (1.6512) | 0.8687 / 0.9827 | 1.5391 / 0.1185 (1.4206) | 9.08 / 27.41 (18.33) | 1.266 / 1.118 | 0.71 / 0.14 | 2.78 / 0.51 | up 0.378 / up 0.338 | 109.21 |
| TCGA_v4 | 178 | 4.18 / 3.77 (0.42) | 0.3720 / 0.3268 (0.0453) | 10.87 / 81.52 | 0.4623 / 0.1696 (0.2928) | 0.9837 / 0.9952 | 0.4548 / 0.1688 (0.2860) | 93.22 / 15.96 (77.26) | 0.849 / 0.642 | 0.67 / 0.33 | 0.25 / 0.15 | down 0.405 / up 0.167 | 203.83 |
| GSE71729 | 145 | 2.16 / 2.20 (-0.04) | 0.3393 / 0.3335 (0.0059) | 22.73 / 22.73 | 0.2593 / 0.2191 (0.0402) | 0.9947 / 0.9923 | 0.2579 / 0.2174 (0.0405) | 76.77 / 7.84 (68.92) | 0.601 / 0.487 | 0.67 / 0.67 | 0.25 / 0.31 | up 0.415 / up 0.354 | 263.68 |
| GSE62452 | 69 | 1.41 / 1.26 (0.15) | 0.3454 / 0.3485 (-0.0031) | 18.18 / 51.35 | 0.3100 / 0.3136 (-0.0036) | 0.9820 / 0.9939 | 0.3044 / 0.3116 (-0.0072) | 95.64 / 17.10 (78.54) | 0.199 / 0.340 | 0.42 / 0.58 | 0.66 / 0.22 | down 0.197 / down 0.336 | 258.71 |
| ICGC | 70 | 1.44 / 1.37 (0.07) | 0.3600 / 0.3450 (0.0150) | 70.59 / 79.41 | 0.4080 / 0.3110 (0.0970) | 0.9887 / 0.9882 | 0.4034 / 0.3073 (0.0960) | 52.31 / 32.43 (19.87) | 0.238 / 0.135 | 0.50 / 0.58 | 0.43 / 0.42 | up 0.181 / down 0.350 | 142.46 |
| IMMUNE_TCGA | 178 | 4.21 / 2.30 (1.91) | 0.3785 / 0.3240 (0.0545) | 79.35 / 15.56 | 0.5309 / 0.1634 (0.3675) | 0.9914 / 0.9819 | 0.5263 / 0.1604 (0.3659) | 59.91 / 8.52 (51.39) | 0.985 / 1.132 | 0.92 / 1.00 | 0.24 / 0.76 | down 0.183 / up 0.343 | 159.54 |
| PARP_TCGA | 178 | 4.30 / 4.04 (0.26) | 0.3555 / 0.3311 (0.0244) | 35.87 / 10.87 | 0.3680 / 0.1992 (0.1688) | 0.9963 / 0.9973 | 0.3667 / 0.1987 (0.1680) | 3.19 / 54.38 (51.19) | 0.867 / 0.698 | 0.67 / 0.83 | 0.26 / 0.19 | up 0.173 / up 0.393 | 139.68 |
| DEPMAP | 45 | 1.93 / 1.69 (0.24) | 0.3615 / 0.3499 (0.0115) | 57.14 / 60.87 | 0.4436 / 0.2532 (0.1904) | 0.9782 / 0.9968 | 0.4339 / 0.2524 (0.1815) | 4.40 / 17.61 (13.21) | — / 0.043 | 0.50 / 0.67 | 0.89 / 0.24 | down 0.196 / up 0.345 | 40.43 |

Detail indicateur 6 (pas T_0 reel/nul, fenetre, flux lus) : identique a la v6.1 (memes entrees, memes cascades) — voir `v62_phase2_table.csv` (colonnes step_R/step_N, window, nflux).

## Verdicts par indicateur — v6.2 contre v6.1 (paires principales)

| Indicateur | v6.2 (gigue appliquee) | v6.1 (gigue 0,07) | Ce qui a change, et pourquoi |
|---|---|---|---|
| 1 Delta | 6/8 : [TCGA v4, GSE62452, ICGC, immunitaire TCGA, PARP TCGA, DepMap], echoue sur [HP35, GSE71729] | 6/8, memes paires | Rien. Ecarts identiques ; gigue 0 dans les deux versions. |
| 2 MC best_score | 7/8 : [HP35, TCGA v4, GSE71729, ICGC, immunitaire TCGA, PARP TCGA, DepMap], echoue sur [GSE62452] | 1/8 : [HP35] | Seule la gigue a change (0,07 → 0,00 mesuree). Les 7 ecarts positifs (+0,0059 a +0,0545 sur PDAC) passent un seuil 0 mais pas 0,07. Le score vedette ne separe toujours pas au-dela du bruit historique. |
| 3 max_separation | 7/8 : [HP35, TCGA v4, GSE71729, ICGC, immunitaire TCGA, PARP TCGA, DepMap], echoue sur [GSE62452] | 6/8 (GSE71729 et GSE62452 en echec) | Seule la gigue a change. GSE71729 (+0,0402) passe avec gigue 0 ; GSE62452 reste plat (−0,0036). Ecarts identiques a la v6.1. |
| 9 S_sep | 6/8 : [HP35, TCGA v4, ICGC, immunitaire TCGA, PARP TCGA, DepMap], echoue sur [GSE71729 (+0,0405 < 0,07), GSE62452 (−0,0072)] | — (nouveau ; prevu 6/8 au §3.3 sur valeurs v6.1) | Atteint la barre ≥ 6/8, exactement comme max_separation en v6.1, meme paires. La stabilite (~0,98–1,00 sur PDAC) ne change presque rien : S_sep ≈ max_separation ; le garde-fou anti-pic-bruite ne s'est pas declenche ici. |
| 4 |T0| | 8/8 — TRIVIAL | 8/8 — TRIVIAL | Rien (voir reserves phase 2). |
| 5 falsification | 4/5 disponibles : [HP35, TCGA v4, GSE71729, PARP TCGA], echoue sur [immunitaire TCGA] ; indisponible sur [GSE62452, ICGC, DepMap] (n < 75) | 4/5, memes paires | Rien. Comparaison interne, pas au nul permute (§8.31). |
| 6 coherence (fraction) | 2/8 : [HP35, TCGA v4] | 2/8, memes paires | Rien. |
| 6b |d| median | 6/8 | 6/8 | Rien. |
| 7 L7a | 4/8 : [TCGA v4, immunitaire TCGA, PARP TCGA, DepMap], direction majoritaire NEGATIVE | 4/8, memes paires | Ecarts signes quasi identiques (plus grand mouvement : TCGA V2 en annexe, −0,579 → −0,548 ; principal : HP35 +0,044 → +0,040). Verdict inchange. |
| 8 cascade | 8/8 — TRIVIAL | 8/8 — TRIVIAL | Rien (voir reserves phase 2). |

## Verdict global

**S_sep separe sur 6/8 paires principales : [HP35, TCGA v4, ICGC, immunitaire TCGA, PARP TCGA, DepMap], echoue sur [GSE71729, GSE62452]. La barre ≥ 6/8 du protocole (§3.4) est atteinte, exactement.**

Mais la reponse a la question « la v6.2 separe-t-elle mieux que la v6.1 ? » est **non** :
- Tous les ecarts reel−nul sont identiques a ceux de la v6.1 au chiffre pres, sauf les ecarts L7a signes (mouvements ≤ 0,031, verdicts inchanges) et le nouvel indicateur S_sep.
- S_sep (6/8) ne fait pas mieux que max_separation en v6.1 (6/8, memes paires) : la stabilite est quasi saturee (~0,98–1,00) sur toutes les paires PDAC, donc S_sep ≈ max_separation. Le 6/8 etait deja predit au §3.3 du protocole a partir des valeurs v6.1.
- Les seuls compteurs qui montent (MC 1/8 → 7/8, max_separation 6/8 → 7/8) montent parce que la gigue appliquee est passee de 0,07 (forfait historique) a 0,00 (mesuree en validation v6.2, comme le protocole §6 l'ordonne), pas parce que l'instrument a change. Avec le forfait 0,07, les verdicts v6.2 seraient exactement ceux de la v6.1.
- Delta reste a 6/8, fragile (echoue sur HP35, le temoin positif ; deux ecarts ≤ 0,15), et **non elucide** (§8.37, partie Delta) : il ne devient pas un discriminateur recommande.

En une phrase : **la v6.2 ne separe pas mieux que la v6.1 ; elle separe pareil, et de facon deterministe (gigue 0).** S_sep atteint la barre ≥ 6/8, mais il herite exactement des forces et des faiblesses de max_separation.

## Annexe — paires secondaires (23, memes regles, memes gigues)

| Paire | n | ΔDelta | ΔMC | Δmax_sep | ΔS_sep | |ΔT_0| | Δfals | Δfrac | Δ|d| med. | ΔL7a signe | Σ|Δ| casc. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ATR_TCGA | 178 | 0.09 | 0.0331 | 0.2262 | 0.2262 | 5.32 | 0.076 | 0.08 | 0.29 | -0.566 | 99.87 |
| CPTAC_BCM | 52 | 0.04 | -0.0174 | -0.1180 | -0.1165 | 42.33 | — | -0.50 | -0.21 | -0.475 | 151.49 |
| CPTAC_UMICH | 63 | -0.01 | 0.0039 | 0.0186 | 0.0212 | 46.96 | — | -0.14 | 0.05 | 0.211 | 162.72 |
| GEO62452_V4B | 69 | -0.02 | 0.0168 | 0.1389 | 0.1295 | 4.36 | — | 0.25 | -0.13 | -0.370 | 34.78 |
| GEO71729 | 145 | -0.04 | 0.0059 | 0.0402 | 0.0405 | 68.92 | 0.114 | 0.00 | -0.07 | 0.061 | 263.68 |
| GEO71729_PARP | 145 | -0.01 | 0.0139 | 0.1074 | 0.1066 | 53.73 | 0.021 | 0.00 | 0.02 | 0.006 | 144.06 |
| GEO71729_V4B | 145 | 0.06 | 0.0247 | 0.1700 | 0.1673 | 0.65 | 0.006 | 0.08 | 0.04 | 0.220 | 36.80 |
| GEO71729_V4C | 145 | 0.27 | -0.1641 | 0.1418 | 0.1435 | 44.56 | -0.058 | 0.17 | -0.07 | 0.256 | 62.63 |
| IMMUNE_GEO62452 | 69 | -0.04 | 0.0217 | 0.1650 | 0.1534 | 62.32 | — | — | -0.15 | -0.282 | 259.84 |
| IMMUNE_GEO71729 | 145 | 0.19 | 0.0204 | 0.1362 | 0.1343 | 53.45 | -0.439 | 0.75 | 0.23 | -0.562 | 90.24 |
| IMMUNE_ICGC | 70 | 0.18 | -0.0343 | -0.2200 | -0.2200 | 5.62 | — | 0.25 | 0.26 | 0.033 | 65.21 |
| IMMUNE_TCGA | 178 | 1.91 | 0.0545 | 0.3675 | 0.3659 | 51.39 | -0.147 | -0.08 | -0.52 | -0.526 | 159.54 |
| LUAD | 515 | 0.01 | -0.0203 | 0.0140 | 0.0152 | 65.00 | 0.006 | 0.00 | -0.17 | 0.653 | 134.27 |
| PARP_TCGA | 178 | 0.26 | 0.0244 | 0.1688 | 0.1680 | 51.19 | 0.169 | -0.17 | 0.07 | -0.220 | 139.68 |
| TCGA_V1 | 178 | -0.62 | 0.0005 | 0.0043 | 0.0049 | 51.32 | -0.163 | 0.00 | -0.10 | -0.535 | 251.83 |
| TCGA_V2 | 178 | -0.56 | 0.0115 | 0.0752 | 0.0757 | 39.12 | -0.191 | -0.08 | -0.07 | -0.548 | 155.78 |
| TCGA_V3 | 178 | -0.05 | 0.0176 | 0.1181 | 0.1182 | 28.25 | -0.097 | -0.17 | 0.02 | 0.248 | 72.15 |
| V4R_CLDN18 | 178 | 0.07 | 0.1192 | 0.8708 | 0.8653 | 24.04 | 0.100 | -0.50 | 0.17 | -0.002 | 52.06 |
| V4R_KRASDESC | 178 | 0.16 | 0.0322 | 0.2124 | 0.2032 | 38.06 | 0.085 | -0.25 | -0.22 | -0.834 | 84.60 |
| V4R_KRASVAL | 178 | 0.42 | 0.0453 | 0.2928 | 0.2860 | 77.26 | 0.207 | 0.33 | 0.10 | -0.572 | 203.83 |
| V4R_PURITY | 178 | -0.67 | 0.1520 | -0.0670 | -0.0679 | 38.99 | -0.045 | -0.33 | -0.00 | 0.423 | 146.78 |
| TESTA_PROLIF | 178 | -0.79 | -0.0948 | 0.2501 | 0.2427 | 1.60 | 0.003 | 0.67 | 1.17 | 0.608 | 47.25 |
| COAD | 285 | 0.02 | 0.0195 | 0.1201 | 0.1167 | 18.69 | 0.004 | -0.33 | 0.10 | -0.618 | 57.84 |

Verdicts annexe v6.2 contre v6.1 (memes regles) :

- Delta : **13/23** (v6.1 : 13/23), direction +.
- MC : **18/23** (v6.1 : 2/23), direction +.
- max_separation : **20/23** (v6.1 : 16/23), direction +.
- S_sep : **16/23** (v6.1 : — (nouveau ; max_sep v6.1 : 16/23)), direction +.
- T0 : **23/23** (v6.1 : 23/23), direction +.
- falsification : **7/18** (v6.1 : 7/18, direction inversee), direction −.
- coherence (fraction) : **8/22** (v6.1 : 8/22), direction +.
- L7a : **13/23** (v6.1 : 12/23), direction −.
- cascade : **23/23** (v6.1 : 23/23), direction +.

Lecture : en annexe, S_sep fait 16/23 — exactement le score de max_separation en v6.1 (16/23). MC passe de 2/23 a 18/23 et max_separation de 16/23 a 20/23 uniquement par la gigue 0 (voir § Gigues). L7a passe de 12/23 a 13/23 (V4R_CLDN18, ecart −0,002, compte avec gigue 0, pas avec 0,07).

Donnees brutes : `v62_phase2_table.csv`, `v62_phase2_table.json`, `v62_phase2_extract.log`.
