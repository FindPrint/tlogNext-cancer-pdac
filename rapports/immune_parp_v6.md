# Paysages immunitaire et réparation/PARP le long de l'axe KRAS — runs v6 mesurés (16 nov. 2026)

**Verdict d'abord :**
1. **Paysage immunitaire — OUI, il change : la tumeur devient « froide » quand KRAS monte.** Les lymphocytes T baissent dans les 4 cohortes (PDCD1/PD-1 significatif dans les 4), et PD-L1 ne monte pas de façon fiable. **Combinaison KRAS + anti-PD-(L)1 : NON soutenue.**
2. **Paysage réparation/PARP — OUI, il change, mais PAS du côté PARP.** Ce qui monte avec KRAS, répliqué dans 2 cohortes, c'est l'axe BRCA2 / ATR / RAD51. PARP1/PARP2 sont plats partout. **Combinaison KRAS + PARP : NON soutenue** — trois angles indépendants convergent vers le négatif.
3. **La piste cohérente qui sort de ces deux bras : ATR / CHEK1 (stress de réplication)** — une hypothèse à tester, pas une conclusion. Et dans les deux bras, le pipeline v6 ne sépare pas réel et nul : les verdicts viennent des tests directs, comme le protocole l'exigeait.

Protocole : ordre KRAS **brut** croissant partout (différence documentée avec la v4 TCGA, qui utilisait le résidu corrigé pureté). Runs v6 fast, mode cohen_d, SHA `bb8bbdba…c0773` vérifié avant et après, fichier jamais modifié. Nuls = lignes permutées, graine 42. Aucune imputation ; règle ≥50 valeurs valides.

---

## Bras 1 — Paysage immunitaire (4 cohortes, 8 runs v6)

**Flux :** CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274 (PD-L1), PDCD1 (PD-1), CTLA4, GZMB, IFNG, CD19. **Écart documenté :** en ICGC, IFNG→PRF1 (règle du protocole) **et** CD19→MS4A1 (CD20, marqueur B comme CD19) — le protocole ne nommait qu'un seul remplaçant, deux absences exigeaient un second ; dupliquer PRF1 aurait créé deux colonnes identiques. Cible v6 = CD8A partout. Matrices vérifiées, rien re-téléchargé : TCGA MD5 `b09569ce…`, GSE71729 SHA `b2287893…`, GSE62452 `8f41d5b3…`, ICGC Xena `c2cb57af…`.

### Tests directs (verdict principal) — Spearman contre KRAS, par cohorte (TCGA / GSE71729 / GSE62452 / ICGC)

| Gène | rho TCGA | rho GSE71729 | rho GSE62452 | rho ICGC | Direction |
|---|---|---|---|---|---|
| CD8A | −0,19 (p 0,0097) | −0,16 (p 0,063) | −0,35 (p 0,0034) | −0,15 (p 0,23) | ↓ partout |
| CD8B | −0,22 (p 0,0037) | −0,18 (p 0,035) | −0,40 (p 0,0006) | +0,04 (ns) | ↓ 3/4 |
| CD4 | −0,15 (p 0,043) | −0,30 (p 0,0003) | −0,15 (ns) | −0,16 (ns) | ↓ partout |
| FOXP3 | −0,10 (ns) | −0,09 (ns) | −0,34 (p 0,0043) | −0,20 (ns) | ↓ partout |
| PDCD1 (PD-1) | −0,25 (p 0,0008) | −0,24 (p 0,0036) | −0,22 (p 0,076) | −0,22 (p 0,064) | ↓ partout |
| CD19 | −0,18 (p 0,016) | −0,09 (ns) | −0,42 (p 0,0004) | absent → MS4A1 −0,05 (ns) | ↓ 3/3 mesurés |
| CTLA4 | −0,20 (p 0,0069) | +0,03 (ns) | −0,03 (ns) | −0,24 (p 0,043) | ↓ 3/4 |
| CD68 | +0,07 (ns) | +0,22 (p 0,0068) | +0,17 (ns) | +0,18 (ns) | ↑ faible partout |
| CD274 (PD-L1) | **+0,26 (p 0,0006)** | −0,11 (ns) | +0,18 (ns) | +0,18 (ns) | ↑ TCGA seulement |
| CD163 | −0,03 (ns) | +0,11 (ns) | −0,12 (ns) | −0,05 (ns) | plat |
| GZMB | −0,11 (ns) | +0,14 (ns) | +0,06 (ns) | −0,04 (ns) | plat |
| IFNG | −0,04 (ns) | +0,08 (ns) | −0,09 (ns) | absent → PRF1 −0,04 (ns) | plat |

**Top-12 KRAS-fort contre reste (d de Cohen) :** PDCD1 −0,61 / −0,88 / −0,70 / −0,85, significatif (Welch) dans les 4 cohortes (p 0,005 / 0,000 / 0,019 / 0,016). CD8A −0,45 / −0,82 / −0,93 / −0,45. CD274 +0,52 / −0,13 / +0,34 / −0,03 — significatif **nulle part**. Au total 16/48 tests p < 0,05 contre ~2,4 attendus sous le nul.

**Runs v6 (8, exit 0) : ne séparent pas réel et nul.** MC optimum réel vs nul : TCGA 0,379/0,324 ; GSE71729 0,344/0,324 ; GSE62452 0,369/0,348 ; ICGC 0,334/**0,368 (réel sous le nul)**. Delta net seulement en TCGA (4,21 vs 2,30) ; ailleurs ~égal ou nul au-dessus. L7a : DOWN faible en TCGA (18 %) et GSE71729 (39 %) ; UP 50 % en GSE62452/ICGC = repli NaN confirmé (`scores_unavailable`, 0 score complet, n < 75 — artefact connu, §8.14). Le nul fabrique lui aussi des cascades complètes.

**Limite majeure :** ARN en vrac sans correction de pureté — la baisse des marqueurs T peut être une composition (moins de T / plus de tumeur) autant qu'une expression par cellule ; le mécanisme n'est pas établi.

**Verdict KRAS + anti-PD-(L)1 : NON.** La cible (PD-L1) n'est pas plus haute là où KRAS est fort, et les T à débloquer sont moins nombreux. La piste qui reste : comprendre pourquoi les T disparaissent quand KRAS monte. Macrophages (CD68) : direction positive cohérente mais faible (1 p < 0,05 sur 4) — hypothèse, pas une cible.

Fichiers : `immune_v6.md`, `PROVENANCE_immune_v6.md`, `build_fluxes_immune.py`, `direct_tests_immune.py`, `extract_immune_v6.py`, `run_immune_v6.sh`, `runs_immune_v6.log`, `pdac_immune_{tcga,geo71729,geo62452,icgc}_fluxes.csv` + `_nul.csv` (SHA : TCGA `66dbb672…`, GSE71729 `8987ffca…`, GSE62452 `97c4689a…`, ICGC `10823879…`), `immune_direct_tests.csv/.txt`, `immune_v6_runs_summary.json`, `results_fast_immune_*(_nul)/` (8 dossiers).

---

## Bras 2 — Paysage réparation de l'ADN / PARP (TCGA, 2 runs v6 + contrôle GEO)

**Flux :** PARP1, PARP2, BRCA1, BRCA2, ATM, ATR, CHEK1, CHEK2, RAD51, XRCC1, POLQ, FANCD2. Tous présents, 178/178 valeurs valides, aucune imputation, aucun remplacement. Flux bruts log2(RSEM+1), ordre KRAS brut croissant. MD5 tarball vérifié `b09569ce…`, rien re-téléchargé.

### Tests directs TCGA-PAAD (178 tumeurs, verdict principal)

| Gène | rho | p | top12 (sd) |
|---|---|---|---|
| **BRCA2** | **+0,420** | **5,2×10⁻⁹** | **+0,54** |
| **ATR** | **+0,407** | **1,7×10⁻⁸** | **+0,44** |
| **POLQ** | **+0,289** | **9,1×10⁻⁵** | **+0,41** |
| RAD51 | +0,184 | 0,014 | +0,33 |
| FANCD2 | +0,176 | 0,019 | +0,08 |
| BRCA1 | +0,161 | 0,032 | +0,11 |
| XRCC1 | −0,187 | 0,013 | −0,60 |
| CHEK1 | +0,121 (ns) | 0,11 | +0,60 |
| PARP1 | −0,047 (ns) | 0,54 | −0,15 |
| PARP2 | −0,088 (ns) | 0,24 | −0,19 |
| ATM | +0,021 (ns) | 0,78 | −0,51 |
| CHEK2 | −0,062 (ns) | 0,41 | +0,11 |

7/12 gènes p < 0,05 ; 3 survivent à Bonferroni (p < 0,0042) : BRCA2, ATR, POLQ. Nul graine 42 : 1/12 p < 0,05, |rho| max 0,190.

### Contrôle GEO GSE71729 (145 tumeurs, tests directs seulement)

6/12 p < 0,05 ; 4 survivent à Bonferroni : CHEK1 +0,505 (p 9,5×10⁻¹¹), **BRCA2 +0,481 (p 9,4×10⁻¹⁰)**, RAD51 +0,427 (p 8,5×10⁻⁸), **ATR +0,250 (p 0,0024)**. Nul : 0/12. **Répliqués : BRCA2, ATR, RAD51** (et BRCA1 nominal dans les deux, +0,161/+0,181, p ≈ 0,03 ; XRCC1 baisse nominale répliquée, −0,187/−0,178). **Non répliqués : POLQ** (TCGA +0,289, GEO −0,023, p 0,79) et **CHEK1** (forme différente : TCGA rho ns +0,121 mais top12 +0,60 sd ; GEO rho +0,505) — signalés comme tels, pas comptés comme réplications propres. PARP1/PARP2 plats aussi en GEO (−0,138 / +0,014, ns).

### Runs v6 (2, exit 0) : ne séparent pas réel et nul

MC 0,355 vs 0,331 ; Delta 4,30 vs 4,04 (tous deux « divergence ») ; L7b FRAGILE des deux côtés ; CSD 0/12 des deux côtés ; T_0 3,19 % (step 6) vs 54,38 % (step 96) ; L7a UP 16,84 % (désaccord) vs UP 39,28 %. La cascade seule ne porte pas le verdict — les tests directs oui. Cible du pipeline : PARP1.

### Faits déjà mesurés, cités sans être réimportés comme verdicts

Balayage CRISPR génome entier : PARP1 rho +0,157 (FDR 0,89), PARP2 −0,120, BRCA1 −0,131, CHEK1 +0,260 (FDR 0,75) — tous non significatifs. Criblage PRISM du 15 nov. : aucun effet de classe PARP (médiane rho +0,032 sur 25 inhibiteurs PARP).

**Limites :** ARN bulk brut sans correction de pureté (re-test style v4 nécessaire avant « tumeur-intrinsèque ») ; prolifération non contrôlée (BRCA2/ATR/CHEK1/RAD51 sont aussi des gènes du cycle) ; expression ≠ protéine ≠ mutation — l'indication PARP validée (mutation germinale BRCA, olaparib/POLO) n'est pas testée ici et n'est pas remise en cause ; ICGC/GSE62452 non faites.

**Verdict KRAS + PARP : NON.** Trois angles indépendants convergent vers le négatif : expression plate ici (2 cohortes), CRISPR sans dépendance, PRISM sans effet de classe. La piste cohérente qui sort de ce bras, c'est **ATR / CHEK1 (stress de réplication)**, à tester — pas une conclusion.

Fichiers : `parp_v6.md`, `PROVENANCE_parp_v6.md`, `build_fluxes_tcga_parp.py`, `pdac_tcga_fluxes_parp.csv` (SHA `c9549b68…c4309`), `pdac_tcga_fluxes_parp_nul.csv` (SHA `57245c72…b1360`), `run_parp_v6.sh`, `runs_parp_v6.log`, `results_fast_parp/` et `results_fast_parp_nul/` (36 fichiers chacun), `parp_direct_tests.py`, `parp_direct_tests.csv/.txt`, contrôle GEO : `build_fluxes_geo71729_parp.py`, `pdac_geo71729_fluxes_parp.csv` (SHA `99abbd6e…722c`), `parp_direct_tests_geo71729.csv/.txt`.

---

## Synthèse — ce que ça veut dire pour les combinaisons

| Combinaison | Verdict | Pourquoi |
|---|---|---|
| KRAS + anti-PD-(L)1 | **NON** | PD-L1 ne monte pas avec KRAS (TCGA seulement, top-12 ns partout) ; les T baissent dans les 4 cohortes (PD-1 significatif partout). Tumeur froide : rien à débloquer là où KRAS est fort. |
| KRAS + PARP | **NON** | PARP1/PARP2 plats en expression (2 cohortes) + CRISPR sans dépendance + PRISM sans effet de classe. Trois négatifs indépendants. L'indication par mutation BRCA germinale n'est pas concernée. |
| KRAS + ATR/CHEK1 | **Hypothèse à tester** | BRCA2/ATR/RAD51 répliqués en hausse avec KRAS ; CHEK1 fort en GEO. Confondant possible : prolifération. Prochain test : re-test corrigé pureté + ajustement prolifération (MKI67/PCNA) + contrôles ICGC/GSE62452. |

Le pipeline v6 a tourné sur les 10 runs demandés (exit 0 partout) et n'a séparé réel et nul dans aucun des deux bras — c'est un résultat d'instrument consigné, pas un échec du test : les verdicts reposent sur les tests directs, qui eux séparent réel et nul nettement (immune : 16/48 p < 0,05 contre ~2,4 attendus ; PARP TCGA : 7/12, nul 1/12 ; GEO : 6/12, nul 0/12).
