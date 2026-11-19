# §8.44 Rotations de contrôle sans doublon — le vrai compteur : 37/48 sous (A), 42/48 sous (B)

Date : 19 novembre 2026. Go : Zackary, « Fait tes 3 propositions, je reviens plus tard », 19 nov. 2026 ~08h16 (2e des 3 propositions ; suite mesurée du §8.41, annoncée au §8.41.7).

## Verdict d'abord

**Sans le doublon de construction, S_sep sépare le réel du nul sur 37 des 48 rotations sous la règle gelée (A) 0,07, et 42/48 sous la règle (B) gigue 0.** L'estimation du §8.41 — 36/48 en retranchant 0,20 à chaque écart — est confirmée, à une paire près : le vrai compteur est **37/48 sous (A), 42/48 sous (B)**. Le 48/48 avec doublon n'était donc pas doublon-fabriqué : il était doublon-assisté à la marge, et la marge se mesure maintenant paire par paire — 11 paires tombent sous (A), 6 sous (B).

| Famille | Paires | S_sep (A) 0,07 | S_sep (B) gigue 0 | max_sep (A) | max_sep (B) | Somme des écarts S_sep | Écart min | Écart max |
|---|---|---|---|---|---|---|---|---|
| V4ROT (TCGA v4) | 12 | 10/12 | 10/12 | 10/12 | 10/12 | +3.6063 | -0.1342 (GSTM1) | +0.6761 (CLDN18) |
| DEPMAPROT (CRISPR DepMap) | 12 | 6/12 | 8/12 | 6/12 | 8/12 | +0.9036 | -0.1380 (MYC) | +0.2596 (DOCK5) |
| IMMROT (immunitaire TCGA) | 12 | 12/12 | 12/12 | 12/12 | 12/12 | +9.0256 | +0.4508 (CD68) | +0.9838 (CD8A) |
| PARPROT (réparation de l'ADN TCGA) | 12 | 9/12 | 12/12 | 9/12 | 12/12 | +3.6259 | +0.0169 (PARP1) | +0.6093 (POLQ) |
| **TOUTES** | **48** | **37/48** | **42/48** | **37/48** | **42/48** | **+17,1614** | **−0,1380 (MYC)** | **+0,9838 (CD8A)** |

Sur les 44 paires refaites dans ce chantier seules : **35/44 sous (A), 39/44 sous (B)** (somme des écarts +15,5906). Les 4 paires du §8.41 ajoutent 2/4 sous (A) — CLDN18, CTLA4 — et 3/4 sous (B) — +PARP1 — pour le compteur combiné 37/48 et 42/48.

**Réserves à garder avec le chiffre, avant toute lecture biologique :**

1. **Ce n'est toujours pas une preuve de rupture ni de remède.** Comme au §8.41, S_sep mesure que la série réelle est ordonnée par l'un de ses propres flux et que les autres flux suivent cet ordre — vrai par construction, sans doublon comme avec. Le 37/48 ne dit rien d'une transition biologique, et aucune des 48 rotations ne devient une cible.
2. **La perte vient du réel, pas du nul.** Retirer le doublon fait chuter S_sep réel de 0,7570 à 0,5780 en moyenne (−0,1790) et ne bouge quasiment pas le nul (0,2209 → 0,2205, −0,0005). Le doublon ne créait pas un faux nul bas : il gonflait le réel d'une colonne parfaitement triée. Les 11 paires qui tombent sous (A) sont celles dont le réel tenait en grande partie sur cette seule colonne.
3. **DEPMAPROT est la famille fragile.** 6/12 sous (A), 8/12 sous (B) — la seule famille sous les deux tiers sous (A). À n=45, le nul varie de 0,13 à 0,36 et quatre réels s'effondrent sans le doublon (CCND1 0,4236 → 0,1566 ; MYC 0,4477 → 0,1993 ; CFLAR 0,6002 → 0,2981 ; ACO2 déjà au §8.41). IMMROT, à l'inverse, tient intégralement : 12/12 sous les deux règles, plus petit écart +0,4508 (CD68).
4. **MUC16 passe de justesse.** Écart +0,0712 sous (A), soit 0,0012 au-dessus du plancher 0,07 : un verdict qui ne tient qu'à un cheveu, à lire comme fragile, pas comme acquis.
5. **S_sep n'apporte toujours rien au-delà de max_separation.** Mêmes listes sous les deux règles, partout, dans les 4 familles : les écarts S_sep diffèrent des écarts max_separation de moins de 0,024 partout (maximum 0,0237). La stabilité est quasi saturée (0,9463–0,9986) : S_sep ≈ max_separation × ~0,99, et le garde-fou anti-pic-bruité ne s'est déclenché sur aucune des 96 runs.

## 8.44.1 Question, méthode, règles

**Question.** Le §8.41 laissait le compteur global sans doublon inconnu : 4 paires contrôlées sur 48, estimation ~36/48. Ce chantier refait les 44 restantes, sans doublon, à permutation de nul identique — et mesure le compteur.

**Méthode — construction des 44 paires, puis 88 runs v6.2.** Pour chaque paire, le CSV réel dédoublonné est le CSV original moins la colonne doublon du flux contrôle (colonne k, valeurs identiques à la colonne 0 vérifiées) ; contrôle, ordre et autres flux inchangés, ligne par ligne. Le CSV nul dédoublonné part du CSV `_nul.csv` ORIGINAL — même permutation que la rotation avec doublon — moins la colonne doublon (multi-ensemble égal à la colonne 0 vérifié ; les 11 autres colonnes identiques ligne par ligne au nul original). Aucune valeur recalculée ni imputée. C'est la méthode « même permutation » du §8.41.3 (`build_dedup_841_sameperm.py`), généralisée aux 44 paires par `build_dedup_844.py` : le §8.41 avait montré que le nul à nouvelle permutation mélangeait deux effets (retrait du doublon + nouvelle permutation) et faisait varier le nul de 0,26 à 0,43 à n=45 — ici un seul effet change à la fois. Les 4 paires du §8.41 ne sont pas refaites : CLDN18 (run v6.1 préexistant, S_sep identique entre v6.1 et v6.2 sur 29/29 paires, §8.38), CTLA4 (nul à nouvelle permutation — seul disponible, passe sous les deux règles avec +0,8986, la permutation ne change pas son verdict), ACO2 et PARP1 (nuls à permutation identique, canoniques §8.41.3).

**Vérifications avant construction (0 écart partout) :** SHA-256 des 96 CSV d'origine vérifiés un par un contre `PROVENANCE_rotations_v61.md` : **96/96 conformes**, 0 mismatch, 0 absent ; SHA des 4 bases conformes (TCGA v4 `e7a2adab…13a0b0`, DepMap `7d605fef…98e37f8`, immunitaire TCGA `66dbb672…bbd2e`, PARP TCGA `c9549b68…c4309`). Pipelines SHA revérifiés à la fin du chantier : v6.2 `f07567c4…ec3abf`, v6.1 `2af5e5ce…a9c9` — inchangés, aucun code modifié.

**Vérifications après extraction :** 88/88 runs v6.2 lus (+8/8 existants), 48/48 paires, version `v6.2.0-L7aL7b-CohenD-short` sur les 88 (v6.1 attendue pour CLDN18 seul) ; SHA-256 des 88 CSV dédoublonnés vérifiés contre `dedup_844_csv_sha.json` : **88/88 conformes** ; les 4 écarts S_sep du §8.41 relus dans leurs `master_results.json` : **0 écart** (tolérance 10⁻⁴).

**Règles de comptage.** Comme `verdict()` de `extract_phase2.py` et comme en §8.38/§8.41 : direction majoritaire = signe de la somme des écarts réel−nul (calculée par famille et sur les 48 paires — elle est positive partout) ; une paire « sépare » si |écart| > gigue ET signe = direction majoritaire. Deux gigues : **(A)** la règle gelée §3.4, gigue effective = max(gigue mesurée 0,00 ; plancher 0,07) = **0,07** (gigue S_sep mesurée en validation v6.2 : 0,0000) ; **(B)** la gigue mesurée seule, **0,00**, rapportée à part. Nul : lignes permutées, graine 42, colonne de contrôle intacte (convention du projet). Aucun nouveau seuil, aucune sélection d'indicateur après coup. Extraction par `extract_ssep_844_rotations.py` (SHA-256 `24a07f9f…f02`), sorties `ssep_844_rotations.json` (SHA `06f41b65…b362`) et `ssep_844_rotations.csv` (SHA `d1abc0ab…f999`).

## 8.44.2 Résultats par famille (sans doublon)

Toutes les valeurs sont S_sep réel / nul (écart réel−nul), relues dans les JSON v6.2 (v6.1 pour CLDN18). « Écart avec » est l'écart du §8.41 (avec doublon) ; « Perte » = écart avec − écart sans. Le flux contrôle est exclu de toute lecture par flux (comme au §8.32) ; aucune lecture par flux n'est faite dans ce chantier — S_sep est global, et la lecture par flux du §8.32 (`v61_rotations_flux_reading.md`, doublon exclu) reste la référence pour le détail flux par flux.

### V4ROT — TCGA v4, ARN tumeurs, n=178 — 10/12 sous (A), 10/12 sous (B)

| Contrôle | S_sep réel / nul | Écart sans | Écart avec | Perte | max_sep réel / nul | Écart max_sep | MC réel / nul | Écart MC | Delta réel / nul | Écart Delta | Stabilité R / N | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CEACAM5 | 0.6783 / 0.1680 | **+0.5104** | +0.6485 | +0.1381 | 0.6831 / 0.1688 | +0.5143 | 0.402 / 0.395 | +0.007 | 3.867 / 3.825 | +0.042 | 0.9930 / 0.9953 | passe (A+B) |
| CLCA1 | 0.4691 / 0.1643 | **+0.3048** | +0.5198 | +0.2150 | 0.4711 / 0.1658 | +0.3053 | 0.370 / 0.327 | +0.043 | 3.842 / 3.828 | +0.014 | 0.9958 / 0.9908 | passe (A+B) |
| CLDN18 | 0.8633 / 0.1872 | **+0.6761** | +0.8783 | +0.2022 | 0.8709 / 0.1877 | +0.6831 | 0.426 / 0.331 | +0.094 | 3.862 / 3.854 | +0.008 | 0.9913 / 0.9972 | passe (A+B) |
| CR2 | 0.1261 / 0.1552 | **-0.0291** | +0.2441 | +0.2732 | 0.1263 / 0.1555 | -0.0292 | 0.320 / 0.325 | -0.005 | 3.795 / 3.161 | +0.634 | 0.9986 / 0.9982 | échoue |
| DPCR1 | 0.6229 / 0.2062 | **+0.4166** | +0.6372 | +0.2205 | 0.6278 / 0.2092 | +0.4186 | 0.393 / 0.346 | +0.047 | 3.835 / 3.230 | +0.605 | 0.9922 / 0.9859 | passe (A+B) |
| GSTM1 | 0.1285 / 0.2626 | **-0.1342** | +0.2215 | +0.3556 | 0.1287 / 0.2641 | -0.1354 | 0.347 / 0.342 | +0.005 | 2.315 / 3.798 | -1.482 | 0.9980 / 0.9944 | échoue |
| KRT20 | 0.4337 / 0.1779 | **+0.2558** | +0.4834 | +0.2276 | 0.4354 / 0.1788 | +0.2565 | 0.365 / 0.328 | +0.038 | 3.788 / 3.874 | -0.085 | 0.9963 / 0.9950 | passe (A+B) |
| MUC16 | 0.3159 / 0.2447 | **+0.0712** | +0.2996 | +0.2285 | 0.3183 / 0.2480 | +0.0703 | 0.353 / 0.506 | -0.153 | 3.819 / 3.838 | -0.019 | 0.9922 / 0.9865 | passe (A+B) |
| MUC17 | 0.7432 / 0.1848 | **+0.5584** | +0.7423 | +0.1839 | 0.7542 / 0.1854 | +0.5688 | 0.413 / 0.328 | +0.085 | 3.867 / 3.785 | +0.082 | 0.9855 / 0.9972 | passe (A+B) |
| MUC2 | 0.4268 / 0.2260 | **+0.2008** | +0.4152 | +0.2143 | 0.4280 / 0.2278 | +0.2002 | 0.366 / 0.335 | +0.031 | 3.800 / 3.773 | +0.026 | 0.9972 / 0.9921 | passe (A+B) |
| PGC | 0.4817 / 0.2467 | **+0.2349** | +0.4113 | +0.1764 | 0.4856 / 0.2478 | +0.2378 | 0.374 / 0.341 | +0.034 | 3.829 / 3.758 | +0.070 | 0.9918 / 0.9956 | passe (A+B) |
| REG4 | 0.6837 / 0.1432 | **+0.5405** | +0.7022 | +0.1617 | 0.6875 / 0.1437 | +0.5439 | 0.402 / 0.322 | +0.079 | 4.264 / 3.801 | +0.463 | 0.9945 / 0.9968 | passe (A+B) |

Somme des écarts S_sep +3.6063 (moyenne +0.3005 par paire).

### DEPMAPROT — CRISPR DepMap, lignées, n=45 — 6/12 sous (A), 8/12 sous (B)

| Contrôle | S_sep réel / nul | Écart sans | Écart avec | Perte | max_sep réel / nul | Écart max_sep | MC réel / nul | Écart MC | Delta réel / nul | Écart Delta | Stabilité R / N | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ACO2 | 0.2395 / 0.2603 | **-0.0208** | +0.0829 | +0.1037 | 0.2400 / 0.2629 | -0.0229 | 0.348 / 0.338 | +0.010 | 1.743 / 1.913 | -0.170 | 0.9982 / 0.9901 | échoue |
| CCND1 | 0.1566 / 0.2709 | **-0.1143** | +0.1600 | +0.2743 | 0.1575 / 0.2769 | -0.1195 | 0.335 / 0.338 | -0.003 | 1.624 / 1.917 | -0.293 | 0.9944 / 0.9782 | échoue |
| CFLAR | 0.2981 / 0.2797 | **+0.0183** | +0.3115 | +0.2932 | 0.3016 / 0.2850 | +0.0166 | 0.356 / 0.339 | +0.017 | 1.740 / 1.928 | -0.188 | 0.9884 / 0.9817 | passe (B seul) |
| CRKL | 0.4377 / 0.2565 | **+0.1812** | +0.2066 | +0.0254 | 0.4625 / 0.2576 | +0.2049 | 0.356 / 0.351 | +0.006 | 1.877 / 1.681 | +0.196 | 0.9463 / 0.9958 | passe (A+B) |
| DOCK5 | 0.3933 / 0.1337 | **+0.2596** | +0.4179 | +0.1583 | 0.4018 / 0.1344 | +0.2674 | 0.355 / 0.332 | +0.023 | 1.897 / 1.669 | +0.229 | 0.9789 / 0.9948 | passe (A+B) |
| EFR3A | 0.4602 / 0.2363 | **+0.2239** | +0.3880 | +0.1642 | 0.4723 / 0.2425 | +0.2297 | 0.364 / 0.332 | +0.033 | 1.936 / 1.925 | +0.011 | 0.9744 / 0.9743 | passe (A+B) |
| MYC | 0.1993 / 0.3373 | **-0.1380** | +0.0969 | +0.2349 | 0.2001 / 0.3435 | -0.1434 | 0.342 / 0.352 | -0.010 | 1.775 / 1.933 | -0.158 | 0.9964 / 0.9821 | échoue |
| MYH9 | 0.2741 / 0.1842 | **+0.0899** | +0.2556 | +0.1657 | 0.2776 / 0.1862 | +0.0913 | 0.339 / 0.339 | +0.000 | 1.900 / 1.737 | +0.163 | 0.9875 / 0.9891 | passe (A+B) |
| RAB10 | 0.4169 / 0.3565 | **+0.0604** | +0.2075 | +0.1471 | 0.4256 / 0.3635 | +0.0621 | 0.359 / 0.351 | +0.008 | 1.899 / 1.936 | -0.037 | 0.9796 / 0.9807 | passe (B seul) |
| RAB6A | 0.4056 / 0.1678 | **+0.2378** | +0.4330 | +0.1952 | 0.4084 / 0.1682 | +0.2402 | 0.359 / 0.339 | +0.021 | 1.912 / 1.703 | +0.208 | 0.9931 / 0.9977 | passe (A+B) |
| SCAP | 0.3562 / 0.2224 | **+0.1338** | +0.3445 | +0.2108 | 0.3688 / 0.2257 | +0.1431 | 0.347 / 0.344 | +0.003 | 1.907 / 1.827 | +0.080 | 0.9657 / 0.9852 | passe (A+B) |
| UROD | 0.2674 / 0.2955 | **-0.0282** | +0.1576 | +0.1857 | 0.2721 / 0.3010 | -0.0289 | 0.339 / 0.342 | -0.003 | 1.895 / 1.894 | +0.002 | 0.9826 / 0.9818 | échoue |

Somme des écarts S_sep +0.9036 (moyenne +0.0753 par paire).

### IMMROT — immunitaire TCGA, ARN tumeurs, n=178 — 12/12 sous (A), 12/12 sous (B)

| Contrôle | S_sep réel / nul | Écart sans | Écart avec | Perte | max_sep réel / nul | Écart max_sep | MC réel / nul | Écart MC | Delta réel / nul | Écart Delta | Stabilité R / N | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CD163 | 1.0673 / 0.2925 | **+0.7748** | +0.9013 | +0.1265 | 1.0904 / 0.2959 | +0.7945 | 0.454 / 0.346 | +0.107 | 4.329 / 4.222 | +0.107 | 0.9788 / 0.9885 | passe (A+B) |
| CD19 | 0.7485 / 0.2976 | **+0.4509** | +0.6685 | +0.2177 | 0.7518 / 0.3054 | +0.4464 | 0.409 / 0.484 | -0.076 | 4.297 / 3.212 | +1.086 | 0.9956 / 0.9744 | passe (A+B) |
| CD274 | 0.7216 / 0.2209 | **+0.5006** | +0.6551 | +0.1545 | 0.7237 / 0.2215 | +0.5022 | 0.407 / 0.335 | +0.072 | 4.345 / 4.051 | +0.295 | 0.9970 / 0.9974 | passe (A+B) |
| CD4 | 1.1593 / 0.4222 | **+0.7372** | +0.8830 | +0.1458 | 1.1686 / 0.4254 | +0.7431 | 0.460 / 0.364 | +0.096 | 4.230 / 4.179 | +0.051 | 0.9921 / 0.9924 | passe (A+B) |
| CD68 | 0.6322 / 0.1814 | **+0.4508** | +0.5942 | +0.1435 | 0.6429 / 0.1819 | +0.4610 | 0.402 / 0.328 | +0.073 | 4.195 / 3.100 | +1.096 | 0.9833 / 0.9972 | passe (A+B) |
| CD8A | 1.2310 / 0.2472 | **+0.9838** | +1.0877 | +0.1039 | 1.2457 / 0.2501 | +0.9955 | 0.468 / 0.541 | -0.073 | 4.264 / 3.818 | +0.446 | 0.9883 / 0.9883 | passe (A+B) |
| CD8B | 1.0608 / 0.2211 | **+0.8398** | +1.0029 | +0.1631 | 1.0674 / 0.2225 | +0.8450 | 0.449 / 0.335 | +0.114 | 4.261 / 3.843 | +0.418 | 0.9938 / 0.9937 | passe (A+B) |
| CTLA4 | 1.2195 / 0.3209 | **+0.8986** | +1.1227 | +0.2240 | 1.2317 / 0.3228 | +0.9089 | 0.468 / 0.354 | +0.114 | 4.203 / 4.104 | +0.099 | 0.9901 / 0.9939 | passe (A+B) |
| FOXP3 | 1.1556 / 0.3127 | **+0.8428** | +0.9852 | +0.1423 | 1.1646 / 0.3166 | +0.8480 | 0.459 / 0.554 | -0.094 | 4.303 / 3.838 | +0.465 | 0.9922 / 0.9878 | passe (A+B) |
| GZMB | 1.1108 / 0.2055 | **+0.9053** | +1.0083 | +0.1030 | 1.1289 / 0.2075 | +0.9215 | 0.457 / 0.500 | -0.043 | 4.242 / 4.201 | +0.040 | 0.9839 / 0.9904 | passe (A+B) |
| IFNG | 0.8070 / 0.0828 | **+0.7242** | +0.8634 | +0.1391 | 0.8130 / 0.0843 | +0.7287 | 0.419 / 0.391 | +0.028 | 4.259 / 1.841 | +2.418 | 0.9926 / 0.9813 | passe (A+B) |
| PDCD1 | 1.0732 / 0.1564 | **+0.9167** | +1.0818 | +0.1650 | 1.0766 / 0.1567 | +0.9199 | 0.448 / 0.325 | +0.123 | 4.291 / 3.065 | +1.226 | 0.9968 / 0.9980 | passe (A+B) |

Somme des écarts S_sep +9.0256 (moyenne +0.7521 par paire).

### PARPROT — réparation de l'ADN TCGA, ARN tumeurs, n=178 — 9/12 sous (A), 12/12 sous (B)

| Contrôle | S_sep réel / nul | Écart sans | Écart avec | Perte | max_sep réel / nul | Écart max_sep | MC réel / nul | Écart MC | Delta réel / nul | Écart Delta | Stabilité R / N | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATM | 0.3158 / 0.1482 | **+0.1676** | +0.3345 | +0.1669 | 0.3179 / 0.1541 | +0.1638 | 0.348 / 0.488 | -0.140 | 4.129 / 3.120 | +1.009 | 0.9936 / 0.9616 | passe (A+B) |
| ATR | 0.3967 / 0.1583 | **+0.2384** | +0.3890 | +0.1506 | 0.3976 / 0.1595 | +0.2381 | 0.361 / 0.487 | -0.126 | 4.267 / 3.003 | +1.263 | 0.9977 / 0.9925 | passe (A+B) |
| BRCA1 | 0.6748 / 0.1508 | **+0.5241** | +0.6859 | +0.1618 | 0.6813 / 0.1513 | +0.5300 | 0.399 / 0.324 | +0.075 | 4.257 / 4.192 | +0.065 | 0.9905 / 0.9965 | passe (A+B) |
| BRCA2 | 0.5770 / 0.1792 | **+0.3978** | +0.5530 | +0.1552 | 0.5836 / 0.1808 | +0.4028 | 0.387 / 0.327 | +0.060 | 4.239 / 3.089 | +1.150 | 0.9887 / 0.9910 | passe (A+B) |
| CHEK1 | 0.5423 / 0.1660 | **+0.3763** | +0.5623 | +0.1860 | 0.5540 / 0.1668 | +0.3872 | 0.384 / 0.327 | +0.057 | 4.362 / 4.153 | +0.209 | 0.9789 / 0.9949 | passe (A+B) |
| CHEK2 | 0.4235 / 0.1712 | **+0.2523** | +0.4000 | +0.1477 | 0.4363 / 0.1715 | +0.2648 | 0.370 / 0.326 | +0.044 | 4.341 / 4.233 | +0.107 | 0.9707 / 0.9981 | passe (A+B) |
| FANCD2 | 0.6559 / 0.2220 | **+0.4339** | +0.5871 | +0.1531 | 0.6650 / 0.2237 | +0.4414 | 0.398 / 0.335 | +0.063 | 4.340 / 4.132 | +0.208 | 0.9863 / 0.9923 | passe (A+B) |
| PARP1 | 0.2678 / 0.2510 | **+0.0169** | +0.1968 | +0.1799 | 0.2712 / 0.2521 | +0.0191 | 0.343 / 0.341 | +0.002 | 4.317 / 4.352 | -0.036 | 0.9874 / 0.9954 | passe (B seul) |
| PARP2 | 0.2757 / 0.2464 | **+0.0293** | +0.2253 | +0.1960 | 0.2764 / 0.2560 | +0.0203 | 0.342 / 0.531 | -0.189 | 4.250 / 3.149 | +1.101 | 0.9975 / 0.9624 | passe (B seul) |
| POLQ | 0.8082 / 0.1990 | **+0.6093** | +0.7595 | +0.1502 | 0.8191 / 0.2040 | +0.6151 | 0.417 / 0.466 | -0.049 | 4.342 / 2.976 | +1.366 | 0.9867 / 0.9753 | passe (A+B) |
| RAD51 | 0.6742 / 0.1501 | **+0.5242** | +0.6652 | +0.1410 | 0.6863 / 0.1504 | +0.5359 | 0.397 / 0.324 | +0.073 | 3.128 / 4.298 | -1.170 | 0.9825 / 0.9977 | passe (A+B) |
| XRCC1 | 0.2667 / 0.2108 | **+0.0558** | +0.2545 | +0.1987 | 0.2685 / 0.2144 | +0.0542 | 0.341 / 0.333 | +0.007 | 4.301 / 2.388 | +1.913 | 0.9930 / 0.9836 | passe (B seul) |

Somme des écarts S_sep +3.6259 (moyenne +0.3022 par paire).

## 8.44.3 Le doublon, mesuré paire par paire

**Le retrait du doublon coûte 0,1786 d'écart en moyenne** (minimum 0,0254, CRKL ; maximum 0,3556, GSTM1) — moins que les 0,20 retranchés dans l'estimation du §8.41, d'où 37/48 mesurés contre 36/48 estimés. L'effet est presque entièrement du côté réel : S_sep réel moyen 0,7570 → 0,5780 (−0,1790) ; S_sep nul moyen 0,2209 → 0,2205 (−0,0005). Par famille, le réel perd −0,2132 (V4ROT), −0,1973 (DEPMAPROT), −0,1421 (IMMROT), −0,1636 (PARPROT) ; le nul ne bouge que de −0,0174 à +0,0103 selon la famille. La plus forte hausse du nul est CTLA4 (+0,1086), déjà connue au §8.41 — toutes les autres sont sous +0,018.

**Six réels chutent de plus de 0,22 sans le doublon — et c'est là que se joue le verdict.** GSTM1 0,4713 → 0,1285 (−0,3429), CFLAR 0,6002 → 0,2981 (−0,3022), CCND1 0,4236 → 0,1566 (−0,2670), CR2 0,3865 → 0,1261 (−0,2604), MYC 0,4477 → 0,1993 (−0,2484), MUC16 0,5411 → 0,3159 (−0,2253). Sur ces paires, le flux contrôle portait l'essentiel de la séparation du réel : les 11 autres flux, ordonnés par lui, ne montrent pas de marche nette au seuil sans lui. À l'inverse, les gros écarts survivent largement : CD8A +1,0877 → +0,9838, CTLA4 +1,1227 → +0,8986, CD8B +1,0029 → +0,8398, GZMB +1,0083 → +0,9053, PDCD1 +1,0818 → +0,9167 — sur ces paires, les flux se suivent mutuellement, doublon ou non.

**Les 11 paires qui tombent sous (A).** Six s'inversent (écart négatif) : CR2 −0,0291, GSTM1 −0,1342, ACO2 −0,0208, CCND1 −0,1143, MYC −0,1380, UROD −0,0282. Cinq restent positives mais sous le plancher : CFLAR +0,0183, RAB10 +0,0604, PARP1 +0,0169, PARP2 +0,0293, XRCC1 +0,0558. Sous (B), seules les six inversées échouent : 42/48. Aucune des 11 n'est une paire IMMROT — la famille immunitaire ne perd aucune paire, la famille CRISPR en perd la moitié.

## 8.44.4 Ce que disent les autres indicateurs sur les mêmes runs (sans doublon)

Le 37/48 est porté par un seul indicateur, comme le 48/48 l'était. Sur les mêmes 96 runs (88 nouveaux + 8 du §8.41) :

- **MC best_score** : ne dépasse le plancher 0,07 que sur **12/48** paires en positif sous (A) (35/48 sous (B), somme des écarts +0,729, moyenne +0,015) ; il est sous −0,07 sur 4/48 (ATM −0,140, ATR −0,126, PARP2 −0,189, MUC16 −0,153). Avec doublon, MC faisait 17/48 sous (A) : retirer le doublon lui coûte 5 paires, pas la tendance. Le composite reste écrasé par la composante robustness (~10⁻⁴¹ sur ces séries, PROTOCOL_v6.2.md §3.2) : il ne voit toujours pas la séparation que max_separation voit seul.
- **Delta** : positif sur 29/48 paires sous (A) (38/48 sous (B), somme +15,330, moyenne +0,319), avec des écarts de ±1 à ±2 (ex. IFNG +2,418, XRCC1 +1,913, RAD51 −1,170, GSTM1 −1,482) — il ne sépare pas, il disperse, comme avec doublon (30/48 positifs au §8.41).
- **L7a** : directions et confiances mélangées des deux côtés ; la direction réel diffère de celle du nul sur 15/48 paires (ex. PARPROT RAD51, POLQ, ATR ; IMMROT CD4, PDCD1) — pas de lecture nette, comme au §8.41.
- **Falsification** : non retenue sous n = 75 (convention §8.35 ; DEPMAPROT, n=45, exclue) ; non recalculée ici — la lecture du §8.41 (nul devant sur 20/36) n'est pas modifiée par ce chantier, qui ne touche pas aux runs avec doublon.

C'est le même tableau qu'au §8.41, inchangé : **aucun contrôle ne sépare réel et nul en MC, Delta ou L7a. Ce qui change, c'est le compteur de max_separation / S_sep sans doublon : 37/48 sous (A), 42/48 sous (B), au lieu de 48/48 avec doublon.** Les deux lectures coexistent sans se contredire : elles ne mesurent pas la même chose.

## 8.44.5 Pourquoi S_sep ≈ max_separation ici, et ce que le 37/48 veut dire

La stabilité est quasi saturée sur les 96 runs : **0,9463–0,9986** (minimum 0,9463, CRKL réel, DEPMAPROT). S_sep vaut donc max_separation × ~0,99 partout : les écarts S_sep diffèrent des écarts max_separation de moins de 0,024 partout (maximum 0,0237), et les deux indicateurs donnent exactement les mêmes listes sous les deux règles, dans les 4 familles. Le garde-fou anti-pic-bruité ne s'est déclenché sur aucune rotation — les pics sont localement plats partout, y compris sur les nuls.

**Pourquoi max_separation sépare-t-il sur 37/48 rotations sans doublon, et seulement 6/8 sur les paires principales ?** La réponse du §8.41.5 tient, précisée : le scan trie les lignes par le contrôle, puis mesure, à chaque seuil candidat, la moyenne sur les flux du |d de Cohen| entre fenêtres pré- et post-seuil. Sur une rotation réelle, le contrôle est l'un des flux : trier par lui, c'est trier par une variable que les 11 autres flux suivent — chacun montre une marche au seuil, la moyenne des |d| est grande — max_separation réel 0,13 à 1,25 sans doublon. Sur le nul, les lignes sont permutées : aucun flux ne montre de marche, la moyenne reste basse — max_separation nul 0,08 à 0,43 (médiane 0,22). Sur les paires principales, le contrôle est KRAS (externe aux flux) : les flux ne le suivent que partiellement, et deux paires échouent. Le 37/48 est donc une mesure d'ordre, pas une mesure de rupture : il dit que l'instrument voit l'ordre quand il y en a un — et il le voit encore sans la colonne parfaitement triée qui le gonflait — il ne dit pas que cet ordre est une transition critique, et encore moins qu'il porte un remède.

**Conséquence pour le §8.32 et le §8.41.** Le titre du §8.32 — « aucun contrôle ne sépare réel et nul » — doit toujours être lu avec sa portée exacte : il portait sur MC, Delta, L7a et la falsification. Le §8.41 l'avait corrigé pour max_separation / S_sep avec doublon (48/48) ; ce chantier corrige la correction : **max_separation / S_sep séparent sur 37/48 rotations sans doublon sous la règle gelée, 42/48 sous gigue nulle.** Le 48/48 avec doublon reste vrai comme mesure — avec doublon — et le 37/48 est désormais la mesure sans doublon. Ni l'un ni l'autre ne devient une piste thérapeutique.

## 8.44.6 Provenance

- **Codes (jamais modifiés).** Pipeline v6.2 `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` ; pipeline v6.1 (CLDN18 seul) `~/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py`, SHA-256 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`. Mode `fast`, graine 42 (défaut), nul = lignes permutées, graine 42, contrôle intact.
- **Formule et règles.** PROTOCOL_v6.2.md §3 (S_sep, exclusions de s_norm / robustness / sharpness, plancher 0,07) et §3.4 (direction = signe de la somme des écarts) ; règles de comptage de `extract_phase2.py` ; gigue S_sep mesurée en validation v6.2 : 0,0000 (`v62_validation_table.json`).
- **Entrées.** 96 CSV de rotations construits par `build_rotations_v61.py` (16 nov. 2026), SHA-256 vérifiés un par un contre `PROVENANCE_rotations_v61.md` : 96/96 conformes (bases : TCGA v4 `e7a2adab…13a0b0`, DepMap `7d605fef…98e37f8`, immunitaire TCGA `66dbb672…bbd2e`, PARP TCGA `c9549b68…c4309`). Sources : TCGA-PAAD ARN Broad GDAC Firehose 2016-01-28 (RSEM) ; DepMap CRISPR 24Q2 (figshare Corsello et al.) ; GEO GSE62452/GSE71729 ; ICGC PACA-AU. Voir PROVENANCE_tcga_v4.md, PROVENANCE_depmap.md, PROVENANCE_immune_v6.md, PROVENANCE_parp_v6.md, PROVENANCE_rotations_v61.md. CSV dédoublonnés : `build_dedup_844.py` (SHA `47447e77…f57d7`) ; SHA-256 des 88 CSV dans `dedup_844_csv_sha.json` (SHA `9dc283c8…b5235c7`) et dans PROVENANCE_rotations_dedup_844.md.
- **Nature des lignes.** Les CSV sont des résidus d'expression génique ou de dépendance CRISPR (mesures instrumentales — séquençage ARN, criblage CRISPR — transformées : correction de pureté, résidus) ordonnés par un flux-contrôle croissant, 11 flux analysés après retrait du doublon ; les nuls sont des lignes permutées, graine 42 — des échantillons hypothétiques, pas des mesures. Aucun mot humain, aucun échantillon hypothétique dans les séries réelles.
- **Sorties et scripts.** Extraction de ce chantier : `extract_ssep_844_rotations.py` (SHA-256 `24a07f9f…f02`), sorties brutes `ssep_844_rotations.json` (SHA `06f41b65…b362`, 72 130 octets) et `ssep_844_rotations.csv` (SHA `d1abc0ab…f999`) — le tableau complet par paire est au §8.44.2 de cette section et dans le CSV. Runs v6.2 : dossiers `results_fast_v62_<famille>_<contrôle>_dedup[_nul]` (88) ; manifeste `manifest_v62_dedup_844.txt` (SHA `1831e0d0…cd7`) ; log `runs_v62_dedup_844.log` (SHA `3951ff67…5a4cd`) ; surveillance `watch_v62_dedup_844.sh` (SHA `f3afa779…b9b9`) ; lanceur `run_v62_lot.sh` (SHA `7e501733…35b`) ; pilote CEACAM5 : log `runs_v62_dedup_844_pilot.log`, 2/2 exit 0, 13h18–13h52 UTC. Runs du §8.41 réutilisés : `results_fast_v61_v4r_cldn18_dedup[_nul]`, `results_fast_v62_immrot_ctla4_dedup[_nul]`, `results_fast_v62_depmaprot_aco2_dedup` + `_nul_sp`, `results_fast_v62_parprot_parp1_dedup` + `_nul_sp`. Section rédigée dans `section_8.44_rotations_dedup.md` (ce fichier).
- **Ce qui manque :** les valeurs exactes de S_sep par flux analysé (hors contrôle) n'ont pas été extraites — S_sep est global, pas par flux ; la lecture par flux du §8.32 reste la référence, doublon exclu ; le nul dédoublonné de CTLA4 est à nouvelle permutation (pas à permutation identique) — son verdict ne dépend pas de ce choix (+0,8986, large marge), mais la comparaison stricte « un seul effet change » ne vaut que pour les 47 autres paires ; MUC16 passe (A) de 0,0012 — un re-run ne changerait rien (v6.2 déterministe, gigue 0), mais le verdict est fragile par construction.

## 8.44.7 Ce qui manque, ce qui reste ouvert

- **Le 37/48 ne devient pas une piste thérapeutique.** Il mesure l'ordre, pas une rupture. Aucun des 48 contrôles ne devient une cible, et aucun flux ne devient un biomarqueur sur cette seule base.
- **MC reste presque aveugle sur les rotations (12/48 en positif sous (A), 4/48 inversés sous −0,07).** L'écart entre MC (composite écrasé par robustness ~10⁻⁴¹) et max_separation (pic seul) sur les mêmes runs est le fait le plus net de ce chantier après le 37/48 : le composite cache ce que le pic voit. Une piste serait de revoir la composition du score MC — hors protocole, non lancée.
- **La famille IMMROT domine (+0,752 en moyenne, 12/12).** Pourquoi les flux immunitaires se suivent-ils plus que les autres familles ? Aucune explication mesurée à ce jour — corrélation inter-flux non quantifiée ici. Une mesure directe (matrice de corrélation par famille, réel contre nul) trancherait si c'est la cohésion de la famille ou l'effet du contrôle.
- **DEPMAPROT est la famille fragile (6/12 sous (A)).** À n=45, le nul varie de 0,13 à 0,36 entre permutations et paires ; quatre réels s'effondrent sans le doublon. La question ouverte est si un nul à plusieurs permutations (distribution, pas un seul tirage) changerait les verdicts limites de cette famille — hors protocole, non lancée.
- **Incident d'exécution.** La machine a redémarré deux fois pendant le lot (~17h43 et ~19h51 UTC) ; l'unité de surveillance `v62-dedup-844-watch` est morte avec elle à chaque fois (aucune entrée dans `journalctl`, cause non établie — comme au §8.41). Les sorties complètes étaient intactes (41/88 puis 82/88) et n'ont pas été touchées ; la relance reprenable a repris où le lot s'était arrêté (SCAP_NUL puis POLQ) et terminé les 6 runs restants, 88/88 exit 0 au total (86 dans le log principal + 2 du pilote). Aucun run perdu, aucun dossier partiel à nettoyer (le run interrompu n'avait pas encore créé son dossier). Leçon confirmée : surveiller `systemctl is-active` pendant les longs lots et consigner toute mort d'unité avec son horodatage, sans supposer le mécanisme.
- **Périmètre.** Les rotations en v6.2 n'ont pas été relancées intégralement avec doublon (96 runs) : inutile pour S_sep, prouvé identique entre v6.1 et v6.2 (§8.38, 29/29 paires). Seules les 44 paires restantes ont été refaites sans doublon (88 runs), plus le pilote CEACAM5 (2 runs, comptés dans les 88).
- **Livre blanc.** Le livre blanc sur disque a changé entre la remise de ce chantier (SHA `de3aa316…`, 2 750 lignes) et la fin du lot (SHA `c5537270…`, 2 752 lignes, modifié 13h17 UTC par un autre processus — ce chantier ne l'a jamais touché) ; il s'arrête toujours au §8.42, sans §8.43 ni §8.44 insérés. Cette section et sa provenance sont des fichiers séparés, à insérer et publier par le coordinateur (règle permanente de Zackary, 19 nov. 09h45 : « Toujours github et pdf !!! » — après chaque lot de sections écrites au livre blanc, régénérer le PDF et pousser sur GitHub).
- **Aucun nouveau seuil proposé, aucun code modifié, aucun push GitHub dans ce chantier** (publication sur go séparé, comme au §8.37).

— Fin de la §8.44. —
