# Bras 2 — Paysage réparation de l'ADN / PARP le long de l'axe KRAS (v6)

**Date : 16 nov. 2026. Cohorte principale : TCGA-PAAD, 178 tumeurs. Contrôle : GEO GSE71729, 145 tumeurs. Pipeline v6, SHA `bb8bbdba…c0773`, mode fast, non modifié.**

## Verdict

**OUI, le paysage de la réparation de l'ADN change le long de l'axe KRAS — mais PAS du côté PARP.**

- **PARP1 et PARP2 sont plats** dans les deux cohortes : aucune montée de l'expression PARP quand KRAS monte. Il n'y a donc **aucun argument d'expression** pour combiner un inhibiteur de KRAS avec un inhibiteur de PARP en fonction du niveau de KRAS.
- **Ce qui monte vraiment avec KRAS, répliqué dans les deux cohortes, c'est l'axe BRCA2 / ATR / RAD51** (réparation par recombinaison homologue et réponse au stress de réplication). C'est là que se trouve la piste — vers ATR / CHEK1, pas vers PARP.
- **Le pipeline v6, lui, ne sépare pas le réel du nul ici** (Delta 4,30 contre 4,04, tous deux « divergence », L7b FRAGILE des deux côtés, CSD 0/12 des deux côtés). La cascade seule ne porte pas le verdict : ce sont les tests directs qui le portent.

## 1. Tests directs — le verdict principal

Groupe KRAS fort = 12 dernières lignes (KRAS le plus élevé). `top12_sd` = écart entre la moyenne des 12 KRAS-forts et celle du reste, en écarts-types du gène. `rho` = corrélation de Spearman entre le gène et le rang KRAS. Seuil Bonferroni pour 12 tests : p < 0,0042.

### TCGA-PAAD (178 tumeurs, ARN brut log2(RSEM+1))

| Gène | rho KRAS | p | top12 (sd) | KRAS-forts > Q3 |
|---|---|---|---|---|
| **BRCA2** | **+0,420** | **5,2×10⁻⁹** | +0,54 | 6/12 |
| **ATR** | **+0,407** | **1,7×10⁻⁸** | +0,44 | 6/12 |
| **POLQ** | **+0,289** | **9,1×10⁻⁵** | +0,41 | 5/12 |
| RAD51 | +0,184 | 0,014 | +0,33 | 4/12 |
| FANCD2 | +0,176 | 0,019 | +0,08 | 4/12 |
| BRCA1 | +0,161 | 0,032 | +0,11 | 6/12 |
| CHEK1 | +0,121 | 0,109 | +0,60 | 6/12 |
| CHEK2 | −0,062 | 0,412 | +0,11 | 3/12 |
| ATM | +0,021 | 0,782 | −0,51 | 4/12 |
| PARP1 | −0,047 | 0,535 | −0,15 | 1/12 |
| PARP2 | −0,088 | 0,242 | −0,19 | 3/12 |
| XRCC1 | −0,187 | 0,013 | −0,60 | 2/12 |

7 gènes sur 12 avec p < 0,05 ; 3 survivent à Bonferroni (BRCA2, ATR, POLQ). Nul (graine 42) : 1/12 avec p < 0,05, |rho| maximal 0,190 (PARP2, p = 0,011).

### GEO GSE71729 — contrôle (145 tumeurs, puce Agilent, log-expression brute)

| Gène | rho KRAS | p | top12 (sd) | KRAS-forts > Q3 |
|---|---|---|---|---|
| **CHEK1** | **+0,505** | **9,5×10⁻¹¹** | +0,71 | 7/12 |
| **BRCA2** | **+0,481** | **9,4×10⁻¹⁰** | +0,41 | 5/12 |
| **RAD51** | **+0,427** | **8,5×10⁻⁸** | +0,57 | 5/12 |
| **ATR** | **+0,250** | **0,0024** | +0,45 | 4/12 |
| BRCA1 | +0,181 | 0,029 | +0,06 | 3/12 |
| XRCC1 | −0,178 | 0,032 | −0,41 | 0/12 |
| FANCD2 | +0,114 | 0,171 | +0,32 | 4/12 |
| CHEK2 | +0,033 | 0,697 | +0,28 | 4/12 |
| PARP2 | +0,014 | 0,871 | +0,20 | 3/12 |
| POLQ | −0,023 | 0,786 | +0,03 | 2/12 |
| ATM | −0,065 | 0,436 | −0,33 | 1/12 |
| PARP1 | −0,138 | 0,098 | −0,52 | 2/12 |

6 gènes sur 12 avec p < 0,05 ; 4 survivent à Bonferroni (CHEK1, BRCA2, RAD51, ATR). Nul : 0/12 avec p < 0,05.

### Lecture gène par gène (les deux cohortes ensemble)

- **BRCA2 — répliqué, fort.** rho +0,420 (p = 5,2×10⁻⁹) en TCGA, +0,481 (p = 9,4×10⁻¹⁰) en GEO. Le signal le plus solide du bras.
- **ATR — répliqué.** rho +0,407 (p = 1,7×10⁻⁸) en TCGA, +0,250 (p = 0,0024) en GEO. Survit à Bonferroni dans les deux cohortes.
- **RAD51 — répliqué, direction et force cohérentes.** +0,184 (p = 0,014) en TCGA, +0,427 (p = 8,5×10⁻⁸) en GEO.
- **BRCA1 — nominal dans les deux, même ordre de grandeur.** +0,161 (p = 0,032) et +0,181 (p = 0,029). Ne survit pas à Bonferroni : signal faible, à confirmer.
- **XRCC1 — baisse nominale répliquée.** −0,187 (p = 0,013) et −0,178 (p = 0,032). Ne survit pas à Bonferroni ; top12 −0,60 / −0,41 sd.
- **CHEK1 — divergent entre cohortes.** En TCGA, pas de tendance monotone (rho +0,121, p = 0,109) mais un fort effet de queue (top12 +0,60 sd, 6/12 au-dessus de Q3). En GEO, tendance monotone forte (rho +0,505, p = 9,5×10⁻¹¹, top12 +0,71 sd, 7/12 au-dessus de Q3). CHEK1 monte avec KRAS dans les deux cohortes d'une façon ou d'une autre, mais la forme du signal diffère : on ne peut pas le compter comme une réplication propre du rho.
- **POLQ — TCGA seulement, non répliqué.** +0,289 (p = 9,1×10⁻⁵, survit à Bonferroni) en TCGA, mais −0,023 (p = 0,786) en GEO. Considéré comme un signal d'une seule cohorte, pas comme un résultat du bras.
- **PARP1, PARP2 — plats partout.** TCGA : −0,047 (p = 0,535) et −0,088 (p = 0,242). GEO : −0,138 (p = 0,098) et +0,014 (p = 0,871). Top12 négatifs ou proches de zéro. Aucune montée de PARP avec KRAS.
- **ATM, CHEK2, FANCD2 — plats ou faibles.** ATM : +0,021 / −0,065, non significatifs (malgré un top12 de −0,51 sd en TCGA, sans tendance — effet de queue sans tendance). CHEK2 : −0,062 / +0,033, non significatifs. FANCD2 : +0,176 (p = 0,019) / +0,114 (p = 0,171), faible et non répliqué au seuil.

## 2. Runs v6 — ne séparent pas réel et nul

| | Réel (`results_fast_parp`) | Nul graine 42 (`results_fast_parp_nul`) |
|---|---|---|
| Exit | 0 | 0 |
| MC, meilleur score | 0,355 (uniform, 93 candidats, w = 30, min_grp 6) | 0,331 (mêmes paramètres) |
| T_-2 | 0,00 % (step 2) | 0,00 % (step 2) |
| T_-1 | 0,19 % (step 2) | 15,48 % (step 28) |
| T_0 | 3,19 % (step 6) | 54,38 % (step 96) |
| T_+1 | 25,55 % (step 45) | 61,80 % (step 110) |
| T_+2 | 25,55 % (step 45) | 62,50 % (step 111) |
| L7a | UP 16,84 %, désaccord (cible up, régime down) | UP 39,28 %, accord |
| L7b | FRAGILE (mode light) | FRAGILE (mode light) |
| Delta | 4,30, régime divergence | 4,04, régime divergence |
| CSD (majorité) | 0/12 flux | 0/12 flux |
| Bruit, score moyen | 0,487 | 0,691 |

Le T_0 diffère (3,19 % contre 54,38 %), mais tout le reste est indiscernable : Delta 4,30 contre 4,04, même régime « divergence », même L7b FRAGILE, même CSD 0/12, scores MC 0,355 contre 0,331. Conformément à la règle du projet, la cascade seule n'est pas un verdict : les tests directs (section 1) portent le verdict, et ils séparent nettement le réel du nul (TCGA 7/12 p < 0,05 contre 1/12 ; GEO 6/12 contre 0/12).

## 3. Ce que ça veut dire pour la combinaison KRAS + PARP

**Non, pas une piste — pour PARP, trois angles indépendants convergent vers le négatif :**

1. **Expression (ce bras, 2 cohortes) :** PARP1/PARP2 ne montent pas avec KRAS — ils sont plats, voire légèrement négatifs. Une tumeur KRAS-forte n'exprime pas plus de PARP qu'une tumeur KRAS-faible.
2. **Dépendance CRISPR (balayage génome entier, déjà mesuré) :** PARP1 rho +0,157 (FDR 0,89), PARP2 −0,120 — non significatifs. Les lignées KRAS-dépendantes ne dépendent pas plus de PARP1/2.
3. **Médicaments PRISM (15 nov., déjà mesuré) :** aucun effet de classe PARP — médiane rho +0,032 sur 25 inhibiteurs PARP.

De plus, le sens du signal va à l'encontre d'une vulnérabilité PARP : **BRCA2 monte avec KRAS** dans les deux cohortes. Les inhibiteurs de PARP fonctionnent surtout quand la recombinaison homologue est déficiente (tumeurs BRCA-mutées). Une tumeur KRAS-forte à BRCA2 élevé en ARN ressemble plutôt à une tumeur à recombinaison homologue compétente — ce qui va dans le sens inverse d'une sensibilité PARP. C'est un raisonnement sur l'ARN, pas une preuve : l'expression n'est pas le statut mutationnel.

**La piste cohérente qui sort de ce bras, c'est ATR / CHEK1 (stress de réplication), pas PARP.** BRCA2, ATR, RAD51 et (en GEO) CHEK1 montent ensemble avec KRAS : c'est la signature d'une tumeur qui réplique vite et qui s'appuie davantage sur sa machinerie de réponse au stress de réplication. Si une combinaison doit être testée autour de KRAS, c'est KRAS + ATR ou KRAS + CHEK1 — des hypothèses à tester, pas des conclusions. POLQ, lui, ne tient que dans TCGA : il ne peut pas porter une piste tant qu'il n'est pas répliqué.

**Ce que ce bras ne remet pas en cause :** l'indication PARP validée en clinique pour le pancréas, c'est la **mutation germinale BRCA1/2** (olaparib en maintenance, essai POLO). Elle ne dépend pas du niveau d'expression de KRAS et n'a pas été testée ici — le statut mutationnel BRCA des 178 tumeurs n'a pas été analysé dans ce bras.

## 4. Limites — à lire avant d'utiliser ce résultat

- **ARN bulk brut, sans correction de pureté.** C'est le choix du protocole gelé de ce bras (la v4, elle, corrige la pureté). La composition du tissu (pancréas normal, stroma) peut contribuer aux corrélations. Avant de dire « tumeur-intrinsèque », il faut un re-test avec correction de pureté (style v4).
- **Prolifération non contrôlée.** BRCA2, ATR, CHEK1, RAD51 sont aussi des gènes du cycle cellulaire : une partie du signal peut refléter que les tumeurs KRAS-fortes prolifèrent plus vite. Test de suivi : ajuster sur un score de prolifération (par exemple MKI67 / PCNA) ou sur la pureté.
- **Expression ≠ protéine ≠ mutation.** Corrélation ≠ causalité. KRAS ici, c'est le niveau d'expression ARN de KRAS, pas son statut mutationnel (presque toutes les tumeurs pancréatiques sont mutées KRAS).
- **ICGC et GSE62452 non testées** dans ce bras (temps) ; TCGA + GEO71729 suffisent pour le verdict, comme le permet le protocole.
- **L7b FRAGILE des deux côtés** : l'audit de robustesse L7b est non informatif ici — il dit FRAGILE sur le réel comme sur le nul, comme déjà établi.

## 5. Fichiers livrés (tous dans `~/workspace/runs/pdac-v6/`)

| Fichier | Contenu | SHA-256 |
|---|---|---|
| `build_fluxes_tcga_parp.py` | Construction des flux TCGA (brut, ordre KRAS brut) | — |
| `pdac_tcga_fluxes_parp.csv` | 178 lignes × 13 colonnes | `c9549b68…c4309` |
| `pdac_tcga_fluxes_parp_nul.csv` | Nul, graine 42 | `57245c72…b1360` |
| `run_parp_v6.sh` | Lancement des 2 runs v6 fast | — |
| `runs_parp_v6.log` | Journal des 2 runs (exit 0 / 0) | — |
| `results_fast_parp/` | Sortie complète du run réel | — |
| `results_fast_parp_nul/` | Sortie complète du run nul | — |
| `parp_direct_tests.py` | Tests directs TCGA | — |
| `parp_direct_tests.csv` / `.txt` | Résultats TCGA | `6feafa32…c5f7e9` (csv) |
| `build_fluxes_geo71729_parp.py` | Construction des flux GEO (contrôle) | — |
| `pdac_geo71729_fluxes_parp.csv` | 145 lignes | `99abbd6e…722c` |
| `pdac_geo71729_fluxes_parp_nul.csv` | Nul GEO, graine 42 | `3a8b0764…ce3` |
| `parp_direct_tests_geo71729.csv` / `.txt` | Résultats GEO | `b880679e…73c8` (csv) |
| `PROVENANCE_parp_v6.md` | Provenance complète | — |
| `parp_v6.md` | Ce rapport | — |

## 6. Suivis proposés (non lancés)

1. Re-test des 4 gènes répliqués (BRCA2, ATR, RAD51, BRCA1) avec correction de pureté style v4, pour vérifier que le signal est tumeur-intrinsèque.
2. Ajustement sur un score de prolifération (MKI67/PCNA) pour séparer « réparation » de « prolifération ».
3. Contrôle ICGC / GSE62452 des mêmes tests directs.
4. Statut mutationnel BRCA1/2 des tumeurs TCGA : le croiser avec l'axe KRAS (les tumeurs BRCA-mutées sont-elles KRAS-fortes ou KRAS-faibles ?).
