# §8.41 S_sep sur les 48 rotations de contrôle (§8.32)

Date : 19 novembre 2026. Go : Zackary, « Lance tout cela », 19 nov. 2026 ~05h47.
Statut : section prête à insérer au livre blanc (avant le §8.5, comme les §8.38–§8.39).

## Verdict d'abord

**S_sep sépare le réel du nul sur les 48 rotations — 48/48, dans les 4 familles 12/12, sous les deux règles de gigue.** C'est le premier 48/48 du projet, et il ne vient pas de l'instrument qui se serait amélioré : il vient de ce que S_sep / max_separation mesurent sur ces séries-là. La lecture honnête, en une phrase : **sur une série ordonnée par l'un de ses propres flux, l'instrument détecte l'ordre — le réel est ordonné, le nul est permuté — et max_separation est l'indicateur qui le voit, là où MC, Delta et L7a ne le voyaient pas.** Ce verdict ne renverse pas le §8.32 : il le précise — le §8.32 reste vrai pour MC, Delta, L7a et la falsification, il est faux pour max_separation / S_sep, qui n'y avaient pas été appliqués.

| Famille | Paires | S_sep (A) 0,07 | S_sep (B) gigue 0 | max_sep (A) | Somme des écarts S_sep | Écart min | Écart max |
|---|---|---|---|---|---|---|---|
| V4ROT (TCGA v4, ARN tumeurs, n=178) | 12 | 12/12 | 12/12 | 12/12 | +6,2033 | +0,2215 (GSTM1) | +0,8783 (CLDN18) |
| DEPMAPROT (CRISPR DepMap, n=45) | 12 | 12/12 | 12/12 | 12/12 | +3,0620 | +0,0829 (ACO2) | +0,4330 (RAB6A) |
| IMMROT (immunitaire TCGA, n=178) | 12 | 12/12 | 12/12 | 12/12 | +10,8540 | +0,5942 (CD68) | +1,1227 (CTLA4) |
| PARPROT (réparation ADN TCGA, n=178) | 12 | 12/12 | 12/12 | 12/12 | +5,6131 | +0,1968 (PARP1) | +0,7595 (POLQ) |
| **TOUTES** | **48** | **48/48** | **48/48** | **48/48** | **+25,7324** | **+0,0829 (ACO2)** | **+1,1227 (CTLA4)** |

**Réserves à garder avec le chiffre, avant toute lecture biologique :**

1. **Ce n'est pas une preuve de rupture ni de remède.** Les rotations ordonnent les lignes par un flux qui fait partie des 12 analysés. Le nul permute les lignes et détruit tout ordre. S_sep ne fait que constater que la série réelle est ordonnée et que les flux suivent cet ordre — c'est vrai par construction, pas une découverte sur le cancer. Un 48/48 sur des séries construites pour être ordonnées ne dit rien d'une transition biologique.
2. **Le doublon gonfle l'écart, il ne le crée pas — sauf à la marge.** Sans doublon, les gros écarts survivent (CLDN18 +0,6761 contre +0,8783 avec ; CTLA4 +0,8986 contre +1,1227), mais ACO2 passe de +0,0829 à −0,0208 (même permutation) et PARP1 de +0,1968 à +0,0168 : les deux ne passent plus la règle (A). Le 48/48 est donc doublon-assisté à la marge ; il vaut avec doublon et ne se transpose pas tel quel sans doublon (voir §8.41.3).
3. **S_sep n'apporte rien au-delà de max_separation, ici non plus.** La stabilité est quasi saturée (0,9562–0,9992 sur les 96 runs) : S_sep ≈ max_separation × ~0,99, mêmes listes sous les deux règles. Le garde-fou anti-pic-bruité ne s'est déclenché sur aucune rotation.
4. **MC, Delta et L7a disent toujours autre chose sur ces mêmes 96 runs** (voir §8.41.4) : MC ne dépasse le plancher 0,07 que sur 17/48 paires, Delta est partagé (positif 30/48, moyenne +0,11), L7a ne s'aligne pas. Le 48/48 est porté par un seul indicateur — max_separation — et il faut le dire comme tel.

## 8.41.1 Question, méthode, règles

**Question.** La v6.2 ne sépare pas mieux que la v6.1 sur les paires principales (S_sep 6/8 = max_separation v6.1, §8.38). Un contrôle, quelque part parmi les 48 rotations du §8.32, sépare-t-il enfin le réel du nul — en S_sep ?

**Méthode — relecture, pas recopie, aucun nouveau run pour le 48/48.** Toutes les valeurs ci-dessous ont été relues dans les 96 `master_results.json` v6.1 du lot rotations (17–18 nov. 2026, `manifest_v61_rotations.txt`, 96/96 présents, version `v6.1.0-L7aL7b-CohenD-short` vérifiée sur les 96) par un extracteur écrit pour ce chantier, `extract_ssep_841_rotations.py` (SHA-256 `20c07975d8d08170eb05eb186dd3c0aab493f87c663e12907d57986e100f5b4e`). Aucun run v6.2 n'était nécessaire pour S_sep sur ces 96 fichiers : max_separation et stabilité ne dépendent pas du hachage L5 (PROTOCOL_v6.2.md §2.3), et le §8.38 l'a vérifié empiriquement — S_sep v6.2 = S_sep v6.1 exactement sur 29/29 paires (max |Δ| = 0,0000). Les 8 seuls nouveaux runs de ce chantier sont les contrôles dédoublonnés du §8.41.3 (6 runs) et les 2 nuls à permutation identique (2 runs), pas des relances des rotations.

**Vérifications de l'extraction (0 écart partout) :**

- MC et Delta relus comparés à `v61_rotations_extract.csv` (la source du tableau vérifié du §8.32) : **0 écart** (tolérance 10⁻⁹) sur les 96 runs ;
- SHA-256 des 96 CSV d'entrée vérifiés un par un contre `PROVENANCE_rotations_v61.md` : **96/96 conformes**, 0 mismatch, 0 absent ; SHA des 4 CSV de base conformes ;
- doublon contrôle=flux vérifié sur l'en-tête d'un CSV par famille : le flux contrôle y apparaît **2 fois** (1re colonne = contrôle, et colonne analysée renommée `.1` par pandas — par exemple `CEACAM5,PGC,…,CEACAM5,…`).

**Règles de comptage.** Comme `verdict()` de `extract_phase2.py` et comme en §8.38 : direction majoritaire = signe de la somme des écarts réel−nul (calculée par famille et sur les 48 paires — elle est positive partout) ; une paire « sépare » si |écart| > gigue ET signe = direction majoritaire. Deux gigues, comme en §8.38 : **(A)** la règle gelée §3.4, gigue effective = max(gigue mesurée 0,00 ; plancher 0,07) = **0,07** (gigue S_sep mesurée en validation v6.2 : 0,0000 sur tous les indicateurs, `v62_validation_table.json`) ; **(B)** la gigue mesurée seule, **0,00**, rapportée à part avec la même réserve qu'en §8.38 — ici les deux règles donnent exactement les mêmes listes, parce qu'aucun écart S_sep ne tombe entre 0 et 0,07 (le plus petit est +0,0829, ACO2). Nul : lignes permutées, graine 42, colonne de contrôle intacte (convention du projet). Aucun nouveau seuil, aucune sélection d'indicateur après coup.

**Le doublon et S_sep.** Dans chaque CSV de rotation, le flux contrôle est aussi présent comme flux analysé (colonne renommée `.1` par pandas). Le §8.32 a montré qu'il domine la lecture *par flux* et qu'il faut l'exclure de toute lecture par flux — c'est fait ici : aucune lecture par flux n'est faite dans ce chantier, le tableau est par famille et par flux *contrôle*. S_sep, lui, est lu dans le `best_config` (global) : le scan calcule, pour chaque seuil candidat, la moyenne sur les flux du |d de Cohen| entre groupes pré- et post-seuil, et max_separation est le maximum de cette moyenne (`evaluate_scan_quality`, v6.1 lignes 3313–3390 ; scan rapide lignes 3124–3309). Le doublon entre dans cette moyenne comme 1 flux sur 12 — il peut gonfler max_separation, il ne peut pas le créer seul. La mesure du §8.41.3 tranche empiriquement : sans doublon, les gros écarts survivent, les petits tombent (voir §8.41.3).

## 8.41.2 Résultats par famille

Toutes les valeurs sont S_sep réel / nul (écart réel−nul), relues dans les JSON v6.1. Table complète par flux contrôle : `ssep_841_rotations.md` (et `ssep_841_rotations.csv`, 48 lignes). Les stabilités sont données parce qu'elles expliquent pourquoi S_sep ≈ max_separation ici (voir §8.41.5).

### V4ROT — TCGA v4, ARN tumeurs, n=178 — 12/12

| Contrôle | S_sep réel / nul | Écart | max_sep réel / nul | Écart max_sep | Stabilité R / N | MC réel / nul |
|---|---|---|---|---|---|---|
| CEACAM5 | 0.8205 / 0.1720 | **+0.6485** | 0.8243 / 0.1726 | +0.6517 | 0.9954 / 0.9966 | 0.419 / 0.396 |
| CLCA1 | 0.6790 / 0.1591 | **+0.5198** | 0.6828 / 0.1602 | +0.5226 | 0.9943 / 0.9931 | 0.399 / 0.326 |
| CLDN18 | 1.0696 / 0.1913 | **+0.8783** | 1.0759 / 0.1963 | +0.8796 | 0.9941 / 0.9746 | 0.450 / 0.363 |
| CR2 | 0.3865 / 0.1424 | **+0.2441** | 0.3872 / 0.1431 | +0.2441 | 0.9983 / 0.9955 | 0.358 / 0.322 |
| DPCR1 | 0.8290 / 0.1918 | **+0.6372** | 0.8358 / 0.1921 | +0.6437 | 0.9918 / 0.9985 | 0.421 / 0.331 |
| GSTM1 | 0.4713 / 0.2499 | **+0.2215** | 0.4760 / 0.2514 | +0.2245 | 0.9902 / 0.9938 | 0.372 / 0.339 |
| KRT20 | 0.6502 / 0.1668 | **+0.4834** | 0.6532 / 0.1677 | +0.4855 | 0.9954 / 0.9950 | 0.396 / 0.327 |
| MUC16 | 0.5411 / 0.2415 | **+0.2996** | 0.5437 / 0.2446 | +0.2991 | 0.9953 / 0.9875 | 0.385 / 0.505 |
| MUC17 | 0.9271 / 0.1848 | **+0.7423** | 0.9360 / 0.1851 | +0.7509 | 0.9905 / 0.9983 | 0.435 / 0.328 |
| MUC2 | 0.6299 / 0.2147 | **+0.4152** | 0.6317 / 0.2165 | +0.4153 | 0.9970 / 0.9919 | 0.394 / 0.333 |
| PGC | 0.6653 / 0.2540 | **+0.4113** | 0.6670 / 0.2549 | +0.4121 | 0.9974 / 0.9965 | 0.397 / 0.340 |
| REG4 | 0.8619 / 0.1596 | **+0.7022** | 0.8725 / 0.1599 | +0.7127 | 0.9878 / 0.9986 | 0.422 / 0.324 |

Somme des écarts S_sep +6,2033 (moyenne +0,517 par paire). Le plus petit écart (GSTM1 +0,2215) dépasse déjà 3 fois le plancher 0,07. MC, sur les mêmes paires, ne dépasse 0,07 que sur 5/12 (CLCA1 +0,074, CLDN18 +0,087, DPCR1 +0,089, MUC17 +0,107, REG4 +0,098) et il est négatif sur MUC16 (−0,120).

### DEPMAPROT — CRISPR DepMap, lignées, n=45 — 12/12

| Contrôle | S_sep réel / nul | Écart | max_sep réel / nul | Écart max_sep | Stabilité R / N | MC réel / nul |
|---|---|---|---|---|---|---|
| ACO2 | 0.3656 / 0.2827 | **+0.0829** | 0.3666 / 0.2862 | +0.0804 | 0.9972 / 0.9878 | 0.367 / 0.341 |
| CCND1 | 0.4236 / 0.2636 | **+0.1600** | 0.4326 / 0.2698 | +0.1628 | 0.9791 / 0.9769 | 0.361 / 0.336 |
| CFLAR | 0.6002 / 0.2888 | **+0.3115** | 0.6083 / 0.2971 | +0.3112 | 0.9868 / 0.9721 | 0.386 / 0.339 |
| CRKL | 0.5749 / 0.3683 | **+0.2066** | 0.6013 / 0.3771 | +0.2242 | 0.9562 / 0.9768 | 0.378 / 0.354 |
| DOCK5 | 0.5634 / 0.1456 | **+0.4179** | 0.5712 / 0.1462 | +0.4250 | 0.9864 / 0.9959 | 0.381 / 0.334 |
| EFR3A | 0.6423 / 0.2543 | **+0.3880** | 0.6625 / 0.2605 | +0.4020 | 0.9695 / 0.9763 | 0.390 / 0.335 |
| MYC | 0.4477 / 0.3509 | **+0.0969** | 0.4524 / 0.3563 | +0.0961 | 0.9896 / 0.9847 | 0.365 / 0.354 |
| MYH9 | 0.4505 / 0.1948 | **+0.2556** | 0.4539 / 0.1969 | +0.2571 | 0.9923 / 0.9896 | 0.365 / 0.340 |
| RAB10 | 0.5791 / 0.3716 | **+0.2075** | 0.5867 / 0.3815 | +0.2052 | 0.9870 / 0.9739 | 0.383 / 0.352 |
| RAB6A | 0.5924 / 0.1593 | **+0.4330** | 0.6040 / 0.1600 | +0.4441 | 0.9807 / 0.9961 | 0.384 / 0.337 |
| SCAP | 0.5520 / 0.2075 | **+0.3445** | 0.5710 / 0.2081 | +0.3629 | 0.9668 / 0.9972 | 0.376 / 0.344 |
| UROD | 0.4806 / 0.3231 | **+0.1576** | 0.4854 / 0.3298 | +0.1556 | 0.9903 / 0.9797 | 0.372 / 0.346 |

Somme des écarts S_sep +3,0620 (moyenne +0,255 par paire) — la famille la plus faible, et la seule où un écart frôle le plancher : ACO2 +0,0829 (voir §8.41.3 pour ce qu'il devient sans doublon). MC ne dépasse 0,07 sur aucune des 12 (max +0,055, EFR3A).

### IMMROT — immunitaire TCGA, ARN tumeurs, n=178 — 12/12

| Contrôle | S_sep réel / nul | Écart | max_sep réel / nul | Écart max_sep | Stabilité R / N | MC réel / nul |
|---|---|---|---|---|---|---|
| CD163 | 1.1947 / 0.2934 | **+0.9013** | 1.2181 / 0.2966 | +0.9216 | 0.9808 / 0.9892 | 0.467 / 0.346 |
| CD19 | 0.9633 / 0.2948 | **+0.6685** | 0.9680 / 0.3022 | +0.6658 | 0.9952 / 0.9755 | 0.436 / 0.484 |
| CD274 | 0.8636 / 0.2085 | **+0.6551** | 0.8657 / 0.2090 | +0.6567 | 0.9975 / 0.9972 | 0.425 / 0.333 |
| CD4 | 1.3046 / 0.4217 | **+0.8830** | 1.3300 / 0.4253 | +0.9047 | 0.9809 / 0.9915 | 0.472 / 0.364 |
| CD68 | 0.7726 / 0.1784 | **+0.5942** | 0.7830 / 0.1788 | +0.6042 | 0.9867 / 0.9978 | 0.420 / 0.328 |
| CD8A | 1.3339 / 0.2461 | **+1.0877** | 1.3458 / 0.2490 | +1.0968 | 0.9912 / 0.9886 | 0.478 / 0.541 |
| CD8B | 1.2284 / 0.2256 | **+1.0029** | 1.2548 / 0.2271 | +1.0277 | 0.9790 / 0.9934 | 0.464 / 0.335 |
| CTLA4 | 1.3350 / 0.2123 | **+1.1227** | 1.3440 / 0.2139 | +1.1301 | 0.9933 / 0.9926 | 0.479 / 0.333 |
| FOXP3 | 1.3018 / 0.3167 | **+0.9852** | 1.3126 / 0.3206 | +0.9920 | 0.9918 / 0.9879 | 0.475 / 0.555 |
| GZMB | 1.2195 / 0.2112 | **+1.0083** | 1.2366 / 0.2136 | +1.0230 | 0.9862 / 0.9891 | 0.468 / 0.477 |
| IFNG | 0.9461 / 0.0828 | **+0.8634** | 0.9531 / 0.0843 | +0.8688 | 0.9927 / 0.9813 | 0.436 / 0.391 |
| PDCD1 | 1.2282 / 0.1464 | **+1.0818** | 1.2307 / 0.1465 | +1.0841 | 0.9980 / 0.9992 | 0.465 / 0.323 |

Somme des écarts S_sep +10,8540 (moyenne +0,905 par paire) — la famille la plus forte, et de loin : son plus petit écart (CD68 +0,5942) dépasse le plus grand écart de DEPMAPROT (+0,4330). Les flux immunitaires se suivent mutuellement beaucoup plus que les autres familles ne se suivent : ordonner par l'un d'eux ordonne presque tous les autres. MC ne dépasse 0,07 que sur 7/12 (CD163 +0,121, CD274 +0,092, CD4 +0,108, CD68 +0,092, CD8B +0,130, CTLA4 +0,146, PDCD1 +0,142) et il est négatif sur CD19 (−0,048), CD8A (−0,063), FOXP3 (−0,080).

### PARPROT — réparation de l'ADN TCGA, ARN tumeurs, n=178 — 12/12

| Contrôle | S_sep réel / nul | Écart | max_sep réel / nul | Écart max_sep | Stabilité R / N | MC réel / nul |
|---|---|---|---|---|---|---|
| ATM | 0.4828 / 0.1483 | **+0.3345** | 0.4857 / 0.1535 | +0.3322 | 0.9941 / 0.9659 | 0.372 / 0.488 |
| ATR | 0.5799 / 0.1909 | **+0.3890** | 0.5831 / 0.1938 | +0.3893 | 0.9946 / 0.9852 | 0.385 / 0.338 |
| BRCA1 | 0.8401 / 0.1543 | **+0.6859** | 0.8464 / 0.1548 | +0.6916 | 0.9926 / 0.9968 | 0.421 / 0.325 |
| BRCA2 | 0.7200 / 0.1670 | **+0.5530** | 0.7269 / 0.1683 | +0.5587 | 0.9905 / 0.9925 | 0.406 / 0.325 |
| CHEK1 | 0.7220 / 0.1596 | **+0.5623** | 0.7356 / 0.1610 | +0.5746 | 0.9815 / 0.9915 | 0.408 / 0.325 |
| CHEK2 | 0.5678 / 0.1678 | **+0.4000** | 0.5762 / 0.1681 | +0.4081 | 0.9854 / 0.9980 | 0.386 / 0.326 |
| FANCD2 | 0.8112 / 0.2241 | **+0.5871** | 0.8199 / 0.2257 | +0.5942 | 0.9894 / 0.9930 | 0.418 / 0.335 |
| PARP1 | 0.4409 / 0.2441 | **+0.1968** | 0.4455 / 0.2452 | +0.2003 | 0.9897 / 0.9956 | 0.368 / 0.340 |
| PARP2 | 0.4543 / 0.2290 | **+0.2253** | 0.4553 / 0.2367 | +0.2185 | 0.9978 / 0.9672 | 0.368 / 0.469 |
| POLQ | 0.9409 / 0.1814 | **+0.7595** | 0.9508 / 0.1826 | +0.7682 | 0.9896 / 0.9934 | 0.434 / 0.396 |
| RAD51 | 0.8211 / 0.1559 | **+0.6652** | 0.8332 / 0.1563 | +0.6769 | 0.9855 / 0.9974 | 0.417 / 0.325 |
| XRCC1 | 0.4607 / 0.2062 | **+0.2545** | 0.4634 / 0.2073 | +0.2561 | 0.9941 / 0.9945 | 0.368 / 0.333 |

Somme des écarts S_sep +5,6131 (moyenne +0,468 par paire). MC dépasse 0,07 sur 5/12 (BRCA1 +0,096, BRCA2 +0,081, CHEK1 +0,083, FANCD2 +0,083, RAD51 +0,091) et il est négatif sous −0,07 sur 2/12 (ATM −0,117, PARP2 −0,100). PARP1, plus petit écart de la famille (+0,1968), est contrôlé sans doublon au §8.41.3.

## 8.41.3 Contrôle dédoublonné — le doublon gonfle l'écart, surtout à la marge

**Question.** Le 48/48 est-il un artefact du défaut de construction connu (§8.32) : le flux contrôle est aussi présent comme flux analysé, et le scan moyenne les |d de Cohen| sur les flux — dont ce doublon parfaitement trié ?

**Méthode.** Quatre paires refaites sans la colonne doublon (contrôle, ordre et autres flux inchangés ; nul = mêmes lignes permutées, graine 42, contrôle fixe), exactement comme le précédent CLDN18 du §8.32 (`build_v4r_cldn18_dedup.py`) : CLDN18 (V4ROT, run v6.1 déjà existant, `results_fast_v61_v4r_cldn18_dedup`) et trois paires nouvelles en v6.2 dans ce chantier — CTLA4 (IMMROT, plus grand écart, +1,1227), ACO2 (DEPMAPROT, plus petit écart, +0,0829, marginal) et PARP1 (PARPROT, plus petit écart, +0,1968) — construites par `build_dedup_841.py`, lancées en v6.2 via systemd-run (unités `v62-dedup-841` puis `v62-dedup-841b` — la première unité est morte pendant le 5e run, relance reprenable, 6/6 exit 0 au total — lanceur `run_v62_lot.sh`, surveillance `watch_v62_dedup_841.sh`, manifeste `manifest_v62_dedup_841.txt`, log `runs_v62_dedup_841.log`, 11h58–12h29 UTC). La comparaison v6.2 dédoublonné contre v6.1 avec doublon est valide : S_sep est identique entre v6.1 et v6.2 (29/29 paires, §8.38).

**Résultat — le doublon gonfle l'écart, il ne le crée pas, sauf à la marge.** S_sep réel / nul, écart réel−nul :

| Paire | Avec doublon (v6.1) | Sans doublon (v6.2, sauf CLDN18 v6.1) | Écart avec | Écart sans | (A) 0,07 avec → sans | (B) 0 avec → sans |
|---|---|---|---|---|---|---|
| CLDN18 (V4ROT) | 1,0696 / 0,1913 | 0,8633 / 0,1872 | +0,8783 | **+0,6761** | passe → passe | passe → passe |
| CTLA4 (IMMROT) | 1,3350 / 0,2123 | 1,2195 / 0,3209 | +1,1227 | **+0,8986** | passe → passe | passe → passe |
| ACO2 (DEPMAPROT) | 0,3656 / 0,2827 | 0,2395 / 0,4334 | +0,0829 | **−0,1939** | passe → **échoue (inversé)** | passe → **échoue (inversé)** |
| PARP1 (PARPROT) | 0,4409 / 0,2441 | 0,2678 / 0,2510 | +0,1968 | **+0,0168** | passe → **échoue (sous 0,07)** | passe → passe |

Le doublon gonfle S_sep réel sur les 4 paires (−0,12 à −0,21 quand on le retire : CLDN18 1,0696 → 0,8633 ; CTLA4 1,3350 → 1,2195 ; ACO2 0,3656 → 0,2395 ; PARP1 0,4409 → 0,2678) — normal : c'est une colonne parfaitement triée, sa moyenne de |d| est grande. Côté nul, l'effet est irrégulier (CLDN18 0,1913 → 0,1872 ; CTLA4 0,2123 → 0,3209 ; ACO2 0,2827 → 0,4334 ; PARP1 0,2441 → 0,2510) : retirer une colonne bruitée de la moyenne peut relever le nul, surtout à n=45. Bilan (nouvelle permutation) : **les gros écarts survivent largement (CLDN18 +0,68, CTLA4 +0,90), les petits s'effondrent (ACO2 s'inverse à −0,19, PARP1 tombe sous le plancher).** Le contrôle à permutation identique ci-dessous montre que l'inversion d'ACO2 vient surtout de la permutation, pas du doublon. Le 48/48 avec doublon ne se transpose donc pas tel quel sans doublon — mais il ne s'effondre pas non plus : sur les 4 paires contrôlées, 2/4 passent encore sous (A) sans doublon, 3/4 sous (B).

**Contrôle du contrôle — la permutation du nul.** Les nuls dédoublonnés ci-dessus utilisaient un nouveau tirage (default_rng(42) par fichier), comme le précédent CLDN18 : la comparaison changeait donc deux choses à la fois côté nul (retrait du doublon + nouvelle permutation). Pour les deux paires où le verdict est proche, le nul a été refait à permutation identique — le CSV `_nul.csv` original, moins la colonne doublon, permutation inchangée (`build_dedup_841_sameperm.py`, 2 runs v6.2, unité `v62-dedup-841sp`, log `runs_v62_dedup_841_sp.log`, 2/2 exit 0) :

| Paire | Nul sans doublon, nouvelle permutation | Nul sans doublon, même permutation | Écart sans doublon (même permutation) | Verdict (A) |
|---|---|---|---|---|
| ACO2 | 0,4334 | 0,2603 | **−0,0208** | échoue (inversé, |écart| < 0,07) |
| PARP1 | 0,2510 | 0,2510 | **+0,0168** | échoue sous (A) (sous 0,07), passe sous (B) |

**Lecture : l'inversion d'ACO2 à −0,1939 venait surtout de la permutation, pas du doublon.** À permutation identique, retirer le doublon ne bouge le nul d'ACO2 que de 0,2827 à 0,2603 (−0,022) et l'écart de +0,0829 à −0,0208 : ACO2 ne passe plus la règle (A), mais de justesse et par le signe, pas par une inversion franche. Le nul à n=45 varie de 0,26 à 0,43 entre deux permutations — le verdict d'ACO2 est fragile dans les deux sens, et ni +0,08 ni −0,02 n'est une séparation solide. Pour PARP1, les deux nuls dédoublonnés sont le même fichier (SHA `591f88ec…` identique : la permutation originale du nul PARP1 est le premier tirage de default_rng(42), PARP1 étant le premier flux du jeu) : S_sep 0,2510 dans les deux cas, écart +0,0168 — échoue sous (A), passe sous (B), sans ambiguïté de permutation. Bilan à même permutation : sur les 4 paires contrôlées, **2/4 passent sous (A) (CLDN18, CTLA4), 3/4 sous (B) (+PARP1)**. Ordre de grandeur — pas une mesure : le retrait du doublon coûte 0,10 à 0,18 d'écart à même permutation (ACO2 −0,104, PARP1 −0,180) ; en retranchant 0,20 à chaque écart des 48 paires, **36/48 resteraient au-dessus du plancher 0,07** (V4ROT 10/12, DEPMAPROT 5/12, IMMROT 12/12, PARPROT 9/12). Le 48/48 est donc doublon-assisté à la marge, pas doublon-fabriqué : il faut le lire 48/48 avec doublon, et retenir que les paires à petit écart (< ~0,25) sont celles dont le verdict dépend du doublon.

## 8.41.4 Ce que disent les autres indicateurs sur les mêmes 96 runs

Le 48/48 est porté par un seul indicateur. Sur les mêmes paires, relus dans les mêmes JSON :

- **MC best_score** : ne dépasse le plancher 0,07 que sur **17/48** paires en positif (V4ROT 5/12, DEPMAPROT 0/12, IMMROT 7/12, PARPROT 5/12) et il est sous −0,07 sur 4/48 (MUC16 −0,120, ATM −0,117, PARP2 −0,100, FOXP3 −0,080) ; moyenne des écarts +0,044 sur les 48 paires, comme au §8.32. Le composite MC est écrasé par la composante robustness (~10⁻⁴¹ sur ces séries, PROTOCOL_v6.2.md §3.2) : il ne voit pas la séparation que max_separation voit seul.
- **Delta** : positif sur 30/48 paires seulement, moyenne +0,11, avec des écarts de ±1 (ex. IFNG +2,396, CD4 −1,125, RAD51 −1,156, XRCC1 −1,193) — il ne sépare pas, il disperse.
- **L7a** : directions et confiances mélangées des deux côtés (ex. V4ROT MUC16 up 0,178 contre up 0,417 au nul ; PARPROT ATR down 0,192 contre flat 0,265) — pas de lecture nette.
- **Falsification** : non retenue sous n = 75 (convention §8.35 ; DEPMAPROT, n=45, exclue) ; sur les 36 autres paires, le nul est devant sur 20/36 (ex. V4ROT MUC16 0,825 nul contre 0,740 réel).

C'est exactement le tableau du §8.32, inchangé : **aucun contrôle ne sépare réel et nul en MC, Delta, L7a ou falsification. Ce qui change, c'est que max_separation / S_sep séparent partout.** Les deux lectures coexistent sans se contredire : elles ne mesurent pas la même chose — MC mesure un composite écrasé par robustness, Delta mesure un écart géométrique qui disperse, max_separation mesure la hauteur du pic de séparation moyenne entre groupes pré/post-seuil.

## 8.41.5 Pourquoi S_sep ≈ max_separation ici (et ce que le 48/48 veut dire)

La stabilité est quasi saturée sur les 96 runs : **0,9562–0,9992** (minimum 0,9562, CRKL réel, DEPMAPROT). S_sep vaut donc max_separation × ~0,99 partout : les écarts S_sep diffèrent des écarts max_separation de moins de 0,025 partout (maximum 0,0248, CD8B ; CLDN18 : +0,8783 contre +0,8796). Le garde-fou anti-pic-bruité ne s'est déclenché sur aucune rotation — les pics sont localement plats partout, y compris sur les nuls.

**Pourquoi max_separation sépare-t-il partout sur les rotations, et seulement 6/8 sur les paires principales ?** Le scan trie les lignes par le contrôle, puis mesure, à chaque seuil candidat, la moyenne sur les flux du |d de Cohen| entre fenêtres pré- et post-seuil. Sur une rotation réelle, le contrôle est l'un des flux : trier par lui, c'est trier par une variable que les 11 autres flux suivent — chacun montre une marche au seuil, la moyenne des |d| est grande — max_separation réel 0,37 à 1,35. Sur le nul, les lignes sont permutées : aucun flux ne montre de marche, la moyenne reste basse — max_separation nul 0,08 à 0,43 (médiane 0,21). Sur les paires principales, le contrôle est KRAS (externe aux flux) : les flux ne le suivent que partiellement, les écarts PDAC tombent à −0,01 à +0,37 (HP35, témoin positif, à +1,42), et deux paires échouent. Autrement dit : **max_separation détecte qu'une série est ordonnée par une variable que ses flux suivent.** Sur les rotations, c'est vrai par construction ; sur les paires principales, c'est vrai partiellement ; sur MTAP (§8.36), c'est vrai en S_sep (+0,20) mais faux en MC et Delta. Le 48/48 est donc une mesure d'ordre, pas une mesure de rupture : il dit que l'instrument voit l'ordre quand il y en a un, il ne dit pas que cet ordre est une transition critique, et encore moins qu'il porte un remède.

**Conséquence pour le §8.32.** Le titre du §8.32 — « aucun contrôle ne sépare réel et nul » — doit être lu avec sa portée exacte : il portait sur MC, Delta, L7a et la falsification, les quatre indicateurs qui y avaient été appliqués. Il est désormais faux sans cette qualification : **max_separation / S_sep séparent sur les 48 rotations.** La correction n'enlève rien au §8.32 — elle ajoute l'indicateur qui manquait, et elle confirme la leçon du projet : un verdict « ça ne sépare pas » est un verdict sur l'indicateur autant que sur l'instrument.

## 8.41.6 Provenance

- **Codes (jamais modifiés).** Pipeline v6.1 `~/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py`, SHA-256 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ; pipeline v6.2 (runs dédoublonnés seulement) `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`. Mode `fast`, graine 42 (défaut), nul = lignes permutées, graine 42, contrôle intact.
- **Formule et règles.** PROTOCOL_v6.2.md §3 (S_sep, exclusions de s_norm / robustness / sharpness, plancher 0,07) et §3.4 (direction = signe de la somme des écarts) ; règles de comptage de `extract_phase2.py` ; gigue S_sep mesurée en validation v6.2 : 0,0000 (`v62_validation_table.json`).
- **Entrées.** 96 CSV de rotations construits par `build_rotations_v61.py` (16 nov. 2026) ; SHA-256 vérifiés un par un contre `PROVENANCE_rotations_v61.md` : 96/96 conformes (bases : TCGA v4 `e7a2adab…13a0b0`, DepMap `7d605fef…98e37f8`, immunitaire TCGA `66dbb672…bbd2e`, PARP TCGA `c9549b68…c4309`). Sources : TCGA-PAAD ARN Broad GDAC Firehose 2016-01-28 (RSEM) ; DepMap CRISPR 24Q2 (figshare Corsello et al.) ; GEO GSE62452/GSE71729 ; ICGC PACA-AU. Voir PROVENANCE_tcga_v4.md, PROVENANCE_depmap.md, PROVENANCE_immune_v6.md, PROVENANCE_parp_v6.md, PROVENANCE_rotations_v61.md. CSV dédoublonnés : `build_dedup_841.py` (SHA `8718cb07…`) ; CTLA4 dédoublonné `36bce133…`, nul `ac1b3c5d…` ; ACO2 dédoublonné `ef398777…`, nul `3700d844…` ; PARP1 dédoublonné `95750c87…`, nul `591f88ec…`.
- **Nature des lignes.** Les CSV sont des résidus d'expression génique ou de dépendance CRISPR (mesures instrumentales — séquençage ARN, criblage CRISPR — transformées : correction de pureté, résidus) ordonnés par un flux-contrôle croissant ; les nuls sont des lignes permutées, graine 42 — des échantillons hypothétiques, pas des mesures. Aucun mot humain, aucun échantillon hypothétique dans les séries réelles.
- **Sorties et scripts.** Extraction de ce chantier : `extract_ssep_841_rotations.py` (SHA-256 `20c07975d8d08170eb05eb186dd3c0aab493f87c663e12907d57986e100f5b4e`), sorties brutes `ssep_841_rotations.json` (SHA `0caca3bf…`), `ssep_841_rotations.csv` (SHA `1d3b28a4…`), table `ssep_841_rotations.md` (SHA `8b4ce480…`). Runs dédoublonnés v6.2 : `results_fast_v62_immrot_ctla4_dedup[_nul]`, `results_fast_v62_depmaprot_aco2_dedup[_nul]`, `results_fast_v62_parprot_parp1_dedup[_nul]` ; manifeste `manifest_v62_dedup_841.txt` ; log `runs_v62_dedup_841.log` (6/6, exit 0, 11h58–12h29 UTC) ; surveillance `watch_v62_dedup_841.sh` ; unités systemd `v62-dedup-841` puis `v62-dedup-841b` (la première est morte pendant le 5e run — voir §8.41.7 — relance reprenable, 2/2 dans le second tour). Nuls à permutation identique : `build_dedup_841_sameperm.py` (SHA `125865d1…`), CSV ACO2 `33d13387…`, PARP1 `591f88ec…` ; runs `results_fast_v62_depmaprot_aco2_dedup_nul_sp` et `results_fast_v62_parprot_parp1_dedup_nul_sp` ; manifeste `manifest_v62_dedup_841_sp.txt` ; log `runs_v62_dedup_841_sp.log` (2/2, exit 0, 12h31–12h43 UTC) ; unité systemd `v62-dedup-841sp`. Run CLDN18 dédoublonné v6.1 (préexistant, §8.32) : `results_fast_v61_v4r_cldn18_dedup[_nul]`. Section rédigée dans `section_8.41_ssep_rotations.md` (ce fichier).
- **Ce qui manque :** les valeurs exactes de S_sep par flux analysé (hors contrôle) n'ont pas été extraites — S_sep est global, pas par flux ; la lecture par flux du §8.32 (`v61_rotations_flux_reading.md`) reste la référence pour le détail flux par flux, doublon exclu ; les 44 autres paires n'ont pas été refaites sans doublon (le contrôle porte sur 4 paires, une par famille, dont les deux extrêmes de l'éventail).

## 8.41.7 Ce qui manque, ce qui reste ouvert

- **Le 48/48 ne devient pas une piste thérapeutique.** Il mesure l'ordre, pas une rupture. Aucun des 48 contrôles ne devient une cible, et aucun flux ne devient un biomarqueur sur cette seule base.
- **MC reste presque aveugle sur les rotations (17/48 en positif, 4/48 inversés sous −0,07).** L'écart entre MC (composite écrasé par robustness ~10⁻⁴¹) et max_separation (pic seul) sur les mêmes runs est le fait le plus net de ce chantier après le 48/48 : le composite cache ce que le pic voit. Une piste serait de revoir la composition du score MC — hors protocole, non lancée.
- **La famille IMMROT domine (+0,905 en moyenne).** Pourquoi les flux immunitaires se suivent-ils plus que les autres familles ? Aucune explication mesurée à ce jour — corrélation inter-flux non quantifiée ici. Une mesure directe (matrice de corrélation par famille, réel contre nul) trancherait si c'est la cohésion de la famille ou l'effet du contrôle.
- **Sans doublon, ACO2 et PARP1 ne passent plus la règle (A)** (voir §8.41.3 : ACO2 +0,0829 → −0,0208 à même permutation ; PARP1 +0,1968 → +0,0168) — le compteur sans doublon, sur les 4 paires contrôlées, est de 2/4 sous (A) et 3/4 sous (B). Les 44 autres paires n'ont pas été refaites sans doublon : le compteur global sans doublon reste inconnu, et le 48/48 ne vaut qu'avec doublon. Ordre de grandeur : en retranchant 0,20 à chaque écart, 36/48 resteraient au-dessus de 0,07.
- **Incident d'exécution.** La première unité systemd (`v62-dedup-841`) est morte pendant le 5e run (PARP1 réel ; dossier partiel vide — le pipeline n'écrit qu'à la fin) ; cause non établie (aucune entrée dans `journalctl --user -u v62-dedup-841.service`). Les 4 sorties complètes étaient intactes et n'ont pas été touchées ; la relance reprenable (`v62-dedup-841b`) les a sautées et a terminé les 2 runs restants, 2/2 exit 0, 6/6 au total. Leçon : surveiller `systemctl is-active` pendant les longs lots et consigner toute mort d'unité avec son horodatage, sans supposer le mécanisme.
- **Périmètre.** Les rotations en v6.2 n'ont pas été relancées intégralement (96 runs) : inutile pour S_sep, prouvé identique entre v6.1 et v6.2 (§8.38, 29/29 paires). Seules 3 paires dédoublonnées (6 runs) et 2 nuls à permutation identique (2 runs) ont été lancés en v6.2, plus le précédent CLDN18 en v6.1.
- **Aucun nouveau seuil proposé, aucun code modifié, aucun push GitHub dans ce chantier** (publication sur go séparé, comme au §8.37).

— Fin de la §8.41. —
