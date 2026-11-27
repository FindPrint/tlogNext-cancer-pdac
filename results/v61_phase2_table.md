# Phase 2 — discrimination réel / nul : table des 8 indicateurs × 8 paires principales (v6.1, 18 nov. 2026)

Protocole gelé : `PROTOCOL_phase2_discrimination.md` (16 nov. 2026). Go de Zackary :
18 nov. 2026, 15h06 (2e des 4 propositions, dans l'ordre, après le test A §8.34).
Pipeline : `universal_v6.1.0_cohen.py`, SHA `2af5e5ce…c1c9`, vérifié inchangé avant
l'extraction, jamais modifié. **Aucun nouveau run du pipeline** : tout est lu dans
les `master_results.json` déjà sur disque (lots 140/140 terminés + test A) et dans
les CSV d'entrée pour l'indicateur 6. Nul : lignes permutées, graine 42, colonne de
contrôle intacte (convention du projet). Extracteur : `extract_phase2.py`
(SHA `5eb3ac24…75aa`), log `v61_phase2_extract.log`. Données brutes :
`v61_phase2_table.csv` (8 principales + 23 secondaires) et `v61_phase2_table.json`.

## Règles de comptage (écrites dans l'extracteur avant tout calcul)

- Gigue : Delta, cascade, falsification = déterministes, gigue 0 (tout écart compte).
  MC best_score, MC max_separation, L7a (confiance signée) : gigue ±0,07
  (L5/L7a, §8.30 / PROVENANCE_v6.1) — écart |.| > 0,07 requis.
- Direction : pour chaque indicateur, la direction majoritaire est le signe de la
  somme des écarts réel−nul sur les 8 paires. Une paire « sépare » si son écart
  dépasse la gigue ET a le signe majoritaire. Critère du protocole (§4) : un
  indicateur sépare s'il tient sur ≥ 6/8 paires.
- Indicateur 2 (MC) : le verdict porte sur le best_score ; le seuil MC (%) est
  descriptif (pas de gigue pré-enregistrée pour un seuil argmax).
- Indicateur 5 (falsification) : « indisponible » si n < 75 (protocole §3) —
  non imputé. Ici : GSE62452 (n=69), ICGC (n=70), DepMap (n=45). De plus, la
  « falsification » (`delta_vs_null`) est une comparaison INTERNE (d_crit
  géométrique contre SpectralDimension), PAS une comparaison au nul permuté
  malgré son nom (§8.31) — ce qu'elle sépare n'est donc pas le nul permuté.
- Indicateur 6 : d de Cohen par flux à T_0 (méthode `per_flux_reading.py` :
  z-score global, fenêtre ±20, ou ±10 si n < 100), signe comparé au vote L7a DE
  LA SÉRIE ELLE-MÊME ; pas T_0 = arrondi(T_0% × n / 100). Sépare si fraction
  réel > fraction nul ET |d| médian réel > |d| médian nul. Doublon
  contrôle=flux : aucun à exclure sur les paires principales (contrôle =
  « step », 1re colonne, pas un flux — contrairement aux rotations §8.32).
- Indicateur 7 (L7a) : confiance signée s = +conf si up, −conf si down, 0 si
  flat ; écart = s_réel − s_nul.
- Indicateurs 4 (|T_0 réel − T_0 nul|) et 8 (somme |Δ| cascade) : le critère du
  protocole (écart > 0) ne peut échouer que sur égalité exacte. Ils sont
  rapportés au pied de la lettre, AVEC la mise en garde que ce « succès » est
  trivial et ne prouve pas une discrimination — deux séries quelconques ont
  presque toujours des T_0 différents.

## Table principale — valeurs réel / nul (écart réel−nul)

| Paire | n | Delta R/N (écart) | MC score R/N (écart) | MC seuil R/N % | max_sep R/N (écart) | T_0 R/N % (\|écart\|) | fals R/N | frac. coh. R/N | \|d\| méd. R/N | L7a R / N | Σ\|Δ\| casc. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HP35 | 1000 | 4,48 / 4,57 (−0,09) | 0,6035 / 0,4086 (+0,1950) | 6,62 / 4,91 | 1,7718 / 0,1206 (+1,6512) | 9,08 / 27,41 (18,33) | 1,266 / 1,118 (+0,148) | 0,71 / 0,14 | 2,78 / 0,51 | up 0,382 / up 0,338 | 109,21 |
| TCGA v4 | 178 | 4,18 / 3,77 (+0,42) | 0,3720 / 0,3268 (+0,0453) | 10,87 / 81,52 | 0,4623 / 0,1696 (+0,2928) | 93,22 / 15,96 (77,26) | 0,849 / 0,642 (+0,207) | 0,67 / 0,33 | 0,25 / 0,15 | down 0,405 / up 0,167 | 203,83 |
| GSE71729 | 145 | 2,16 / 2,20 (−0,04) | 0,3393 / 0,3335 (+0,0059) | 22,73 / 22,73 | 0,2593 / 0,2191 (+0,0402) | 76,77 / 7,84 (68,92) | 0,601 / 0,487 (+0,114) | 0,67 / 0,67 | 0,25 / 0,31 | up 0,415 / up 0,354 | 263,68 |
| GSE62452 | 69 | 1,41 / 1,26 (+0,15) | 0,3454 / 0,3485 (−0,0031) | 18,18 / 51,35 | 0,3100 / 0,3136 (−0,0036) | 95,64 / 17,10 (78,54) | indisponible (brut 0,199 / 0,340) | 0,42 / 0,58 | 0,66 / 0,22 | down 0,197 / down 0,336 | 258,71 |
| ICGC | 70 | 1,44 / 1,37 (+0,07) | 0,3600 / 0,3450 (+0,0150) | 70,59 / 79,41 | 0,4080 / 0,3110 (+0,0970) | 52,31 / 32,43 (19,88) | indisponible (brut 0,238 / 0,135) | 0,50 / 0,58 | 0,43 / 0,42 | up 0,181 / down 0,350 | 142,46 |
| Immunitaire TCGA | 178 | 4,21 / 2,30 (+1,91) | 0,3785 / 0,3240 (+0,0545) | 79,35 / 15,56 | 0,5309 / 0,1634 (+0,3675) | 59,91 / 8,52 (51,39) | 0,985 / 1,132 (−0,147) | 0,92 / 1,00 | 0,24 / 0,76 | down 0,183 / up 0,343 | 159,54 |
| PARP TCGA | 178 | 4,30 / 4,04 (+0,26) | 0,3555 / 0,3311 (+0,0244) | 35,87 / 10,87 | 0,3680 / 0,1992 (+0,1688) | 3,19 / 54,38 (51,19) | 0,867 / 0,698 (+0,169) | 0,67 / 0,83 | 0,26 / 0,19 | up 0,173 / up 0,393 | 139,68 |
| DepMap | 45 | 1,93 / 1,69 (+0,24) | 0,3615 / 0,3499 (+0,0116) | 57,14 / 60,87 | 0,4436 / 0,2532 (+0,1904) | 4,40 / 17,61 (13,21) | indisponible (réel absent du JSON, nul brut 0,043) | 0,50 / 0,67 | 0,89 / 0,24 | down 0,196 / up 0,345 | 40,43 |

Détail indicateur 6 (pas T_0 réel/nul, fenêtre, flux lus) : HP35 pas 91/274, ±20,
7 flux ; TCGA v4 pas 166/28, ±20, 12 flux ; GSE71729 pas 111/11, ±20, 12 flux ;
GSE62452 pas 66/12, ±10, 12 flux ; ICGC pas 37/23, ±10, 12 flux ; immunitaire
pas 107/15, ±20, 12 flux ; PARP pas 6/97, ±20, 12 flux ; DepMap pas 2/8, ±10,
12 flux. Fenêtre « avant » de DepMap réel : 2 points seulement (pas 2) — fragile,
même leçon que CPTAC (§8.8) et test A (§8.34).

## Verdicts par indicateur (formulation du protocole, §4)

1. **Delta — « Sépare sur 6/8 : [TCGA v4, GSE62452, ICGC, immunitaire TCGA,
   PARP TCGA, DepMap], échoue sur [HP35, GSE71729]. »** Direction majoritaire :
   réel > nul. Réserve : échoue sur HP35, le témoin positif connu (le nul y a
   le Delta le plus haut, 4,57 contre 4,48) ; deux des six écarts sont petits
   (ICGC +0,07 ; GSE62452 +0,15) ; en annexe, seulement 13/23.
2. **MC best_score — « Sépare sur 1/8 : [HP35], échoue sur [TCGA v4, GSE71729,
   GSE62452, ICGC, immunitaire TCGA, PARP TCGA, DepMap]. »** Le score vedette
   du pipeline ne dépasse la gigue (±0,07) sur aucune série PDAC. Nuance :
   7/8 écarts sont positifs (seul GSE62452 est négatif, −0,0031) mais tous sous
   la gigue (de +0,0059 à +0,0545) : le MC penche du bon côté sans jamais
   dépasser le bruit. Seuil MC descriptif : il saute d'un bout à l'autre
   (TCGA v4 : 10,87 % réel contre 81,52 % nul ; immunitaire : 79,35 % contre
   15,56 %) — pas une position stable.
3. **max_separation — « Sépare sur 6/8 : [HP35, TCGA v4, ICGC, immunitaire
   TCGA, PARP TCGA, DepMap], échoue sur [GSE71729, GSE62452]. »** Direction
   majoritaire : réel > nul. C'est l'indicateur le plus solide : HP35 écrase
   (+1,65), les écarts PDAC vont de +0,10 à +0,37 ; GSE71729 échoue de peu
   (+0,0402 < 0,07) et GSE62452 est plat (−0,0036). En annexe : 16/23.
4. **Position de T_0 — « Sépare sur toutes les paires » (8/8) — MAIS TRIVIAL.**
   |T_0 réel − T_0 nul| va de 13,21 (DepMap) à 78,54 points (GSE62452) : jamais
   nul. Le critère du protocole (écart > 0, gigue 0) ne peut échouer que sur
   égalité exacte. Ce 8/8 ne prouve pas une discrimination : il prouve que le
   nul place son seuil ailleurs, ce qu'on savait déjà (§8.31/§8.32).
5. **Falsification delta_vs_null — « Sépare sur 4/5 disponibles : [HP35,
   TCGA v4, GSE71729, PARP TCGA], échoue sur [immunitaire TCGA] ;
   indisponible sur [GSE62452, ICGC, DepMap] (n < 75). »** Direction
   majoritaire : réel > nul. Réserves : ce n'est pas une comparaison au nul
   permuté (comparaison interne, §8.31) ; immunitaire TCGA s'inverse
   (0,985 réel contre 1,132 nul) ; en annexe la direction majoritaire
   s'inverse (7/17, direction − : TCGA v1/v2/v3 ont une falsification plus
   haute au nul qu'au réel).
6. **Cohérence par flux à T_0 — « Sépare sur 2/8 : [HP35, TCGA v4], échoue
   sur [GSE71729, GSE62452, ICGC, immunitaire TCGA, PARP TCGA, DepMap]. »**
   Fraction seule : 2/8 (HP35 0,71 contre 0,14 ; TCGA v4 0,67 contre 0,33).
   |d| médian seul : 6/8 (échoue sur GSE71729 et immunitaire TCGA). Le point
   dur : le nul est parfois PLUS cohérent que le réel à son propre T_0 —
   immunitaire TCGA nul 1,00 (12/12 flux, |d| médian 0,76) contre réel 0,92
   (0,24) ; PARP nul 0,83 contre réel 0,67 ; DepMap nul 0,67 contre réel 0,50.
   La cohérence des flux autour d'un seuil ne distingue pas réel et nul.
7. **L7a — « Sépare sur 4/8 : [TCGA v4, immunitaire TCGA, PARP TCGA, DepMap],
   échoue sur [HP35, GSE71729, GSE62452, ICGC]. »** Confiance signée
   (s = ±conf) : direction majoritaire NÉGATIVE (le réel vote plus « down »
   / moins confiant « up » que le nul). Écarts signés : TCGA v4 −0,572 ;
   immunitaire −0,526 ; PARP −0,220 ; DepMap −0,541 ; HP35 +0,044 ;
   GSE71729 +0,061 ; GSE62452 +0,139 (sens inverse) ; ICGC +0,531 (sens
   inverse : réel up 0,181 contre nul down 0,350). Le vote L7a ne sépare pas.
8. **Écart cascade complet — « Sépare sur toutes les paires » (8/8) — MAIS
   TRIVIAL.** Somme |Δ| de 40,43 (DepMap) à 263,68 (GSE71729) : jamais nulle.
   Même réserve que l'indicateur 4 : le critère (somme > 0) ne peut échouer
   que sur deux cascades identiques chiffre par chiffre. Ce 8/8 ne prouve pas
   une discrimination.

## Verdict global (selon la règle écrite du protocole, §4)

La phrase globale « le pipeline, en l'état, ne sépare pas réel et nul sur ces
séries PDAC » ne s'applique PAS au pied de la lettre : deux indicateurs
non triviaux atteignent la barre des 6/8 — **Delta (6/8) et max_separation
(6/8)**. Mais elle reste vraie pour l'essentiel de l'instrument :

- **Ce qui sépare (6/8) :** Delta et max_separation, tous deux dans le sens
  réel > nul. max_separation est le plus convaincant (HP35 +1,65, écarts
  PDAC +0,10 à +0,37) ; Delta est fragile (échoue sur le témoin HP35,
  deux écarts ≤ 0,15, 13/23 en annexe).
- **Ce qui ne sépare pas :** le MC best_score (1/8 — le score vedette),
  la cohérence par flux (2/8), le L7a (4/8), la falsification (4/5
  disponibles, et ce n'est pas une comparaison au nul permuté).
- **Ce qui « sépare » sans rien prouver :** la position de T_0 (8/8) et
  l'écart cascade complet (8/8) — critères triviaux par construction.
- **En annexe (23 paires secondaires, mêmes règles) :** Delta 13/23, MC 2/23,
  max_separation 16/23, T_0 23/23, falsification 7/18 (direction inversée),
  cohérence fraction 8/22, L7a 12/23, cascade 23/23. Le tableau d'ensemble
  confirme les paires principales : seul max_separation tient à peu près
  partout, le MC ne tient presque nulle part.

**En une phrase : le pipeline, en l'état, ne sépare pas réel et nul sur ces
séries PDAC par ses scores principaux (MC, L7a, cohérence des flux) ; seuls
Delta et surtout max_separation montrent un écart réel > nul cohérent sur
6/8 paires — une piste, pas une discrimination démontrée.**

## Annexe — paires secondaires (23, mêmes règles, mêmes gigues)

| Paire | n | ΔDelta | ΔMC | Δmax_sep | \|ΔT_0\| | Δfals | Δfrac | Δ\|d\| méd. | ΔL7a signé | Σ\|Δ\| casc. |
|---|---|---|---|---|---|---|---|---|---|---|
| COAD | 285 | +0,02 | +0,0195 | +0,1201 | 18,69 | +0,004 | −0,33 | +0,10 | −0,621 | 57,84 |
|---|---|---|---|---|---|---|---|---|---|---|
| ATR_TCGA | 178 | +0,09 | +0,0331 | +0,2262 | 5,32 | +0,076 | +0,08 | +0,29 | −0,567 | 99,87 |
| CPTAC_BCM | 52 | +0,04 | −0,0174 | −0,1180 | 42,33 | indisp. | −0,50 | −0,21 | −0,475 | 151,49 |
| CPTAC_UMICH | 63 | −0,01 | +0,0039 | +0,0186 | 46,96 | indisp. | −0,14 | +0,05 | +0,211 | 162,72 |
| GEO62452_V4B | 69 | −0,02 | +0,0168 | +0,1389 | 4,36 | indisp. | +0,25 | −0,13 | −0,370 | 34,78 |
| GSE71729 | 145 | −0,04 | +0,0059 | +0,0402 | 68,92 | +0,114 | 0,00 | −0,07 | +0,061 | 263,68 |
| GEO71729_PARP | 145 | −0,01 | +0,0139 | +0,1074 | 53,73 | +0,021 | 0,00 | +0,02 | +0,006 | 144,06 |
| GEO71729_V4B | 145 | +0,06 | +0,0247 | +0,1700 | 0,65 | +0,006 | +0,08 | +0,04 | +0,220 | 36,80 |
| GEO71729_V4C | 145 | +0,27 | −0,1641 | +0,1418 | 44,56 | −0,058 | +0,17 | −0,07 | +0,257 | 62,63 |
| IMMUNE_GEO62452 | 69 | −0,04 | +0,0217 | +0,1650 | 62,32 | indisp. | indisp. (L7a réel flat) | −0,15 | −0,282 | 259,84 |
| IMMUNE_GEO71729 | 145 | +0,19 | +0,0204 | +0,1362 | 53,45 | −0,439 | +0,75 | +0,23 | −0,562 | 90,24 |
| IMMUNE_ICGC | 70 | +0,18 | −0,0343 | −0,2200 | 5,62 | indisp. | +0,25 | +0,26 | +0,033 | 65,21 |
| IMMUNE_TCGA | 178 | +1,91 | +0,0545 | +0,3675 | 51,39 | −0,147 | −0,08 | −0,52 | −0,526 | 159,54 |
| LUAD | 515 | +0,01 | −0,0203 | +0,0140 | 65,00 | +0,006 | 0,00 | −0,17 | +0,656 | 134,27 |
| PARP_TCGA | 178 | +0,26 | +0,0244 | +0,1688 | 51,19 | +0,169 | −0,17 | +0,07 | −0,220 | 139,68 |
| TCGA_V1 | 178 | −0,62 | +0,0005 | +0,0043 | 51,32 | −0,163 | 0,00 | −0,10 | −0,536 | 251,83 |
| TCGA_V2 | 178 | −0,56 | +0,0115 | +0,0752 | 39,12 | −0,191 | −0,08 | −0,07 | −0,579 | 155,78 |
| TCGA_V3 | 178 | −0,05 | +0,0176 | +0,1181 | 28,25 | −0,097 | −0,17 | +0,02 | +0,245 | 72,15 |
| V4R_CLDN18 | 178 | +0,07 | +0,1192 | +0,8708 | 24,04 | +0,100 | −0,50 | +0,17 | −0,001 | 52,06 |
| V4R_KRASDESC | 178 | +0,06 | +0,0322 | +0,2124 | 38,06 | +0,085 | −0,25 | −0,22 | −0,834 | 84,60 |
| V4R_KRASVAL (= TCGA v4) | 178 | +0,42 | +0,0453 | +0,2928 | 77,26 | +0,207 | +0,33 | +0,10 | −0,573 | 203,83 |
| V4R_PURITY | 178 | −0,67 | +0,1520 | −0,0670 | 38,99 | −0,045 | −0,33 | −0,00 | +0,422 | 146,78 |
| TESTA_PROLIF | 178 | −0,79 | −0,0948 | +0,2501 | 1,60 | +0,003 | +0,67 | +1,17 | +0,608 | 47,25 |

Notes d'annexe : le COAD réel, manquant dans `v61_extended_compare.csv`
(43/44, §8.31), a été refait ensuite (lot final 140/140, §8.32) et entre ici
directement depuis son `master_results.json` sur disque. V4R_KRASVAL est la
même série que TCGA v4 (doublon de nom, mêmes chiffres — pas un 9e point).
TESTA_PROLIF est le test A (§8.34) comme paire secondaire : Delta et MC y
sont inversés (nul devant), max_separation reste positif (+0,2501).
