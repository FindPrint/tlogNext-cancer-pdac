# Re-test ATR/CHEK1 — la hausse BRCA2/ATR/CHEK1/RAD51 survit-elle aux contrôles ?

**Date : 16 nov. 2026. Pipeline v6, SHA `bb8bbdba…c0773`, mode fast, non modifié. Protocole gelé avant les runs.**

## Verdict

**La hausse survit à la pureté — pas à la prolifération, sauf pour ATR seul.**

- **Pureté : OUI, le signal est réel.** La correction v3 (acineux + îlots) n'explique que 0,02 % à 3,2 % de la variance de ces 7 gènes. Après correction : BRCA2 rho +0,425, ATR +0,409 — inchangés par rapport au brut (+0,420 / +0,407).
- **Prolifération : NON pour le « stress de réplication » large.** Les tumeurs KRAS-fortes prolifèrent plus (score prolifération vs rang KRAS : +0,386, p = 1,1×10⁻⁷). Une fois la prolifération retirée, **CHEK1, RAD51 et POLQ disparaissent** (partiels −0,143 / −0,171 / +0,023, tous ns) — ce sont des marqueurs de prolifération, pas un signal KRAS-spécifique. **BRCA2 survit à TCGA seulement** (partiel +0,305, p = 3,6×10⁻⁵) mais pas à GSE62452 (+0,094, ns).
- **ATR est le seul gène qui survit aux deux contrôles dans deux cohortes indépendantes** : partiel TCGA +0,366 (p = 5,6×10⁻⁷) et GSE62452 +0,488 (p = 2,4×10⁻⁵) ; brut significatif dans 3 cohortes sur 4. C'est aussi le « monteur » le moins lié à la prolifération (rho gène-prolif +0,214 en TCGA, contre +0,65 à +0,92 pour CHEK1/RAD51/POLQ/BRCA2).
- **ICGC : rien du tout.** Aucun des 7 gènes ne bouge (0/7 p < 0,05) — et l'axe KRAS-expression lui-même y est plat (prolifération vs KRAS +0,080, ns), comme déjà vu pour CA125/CEA dans cette cohorte.
- **Médicaments : NON.** Aucun inhibiteur ATR/CHEK1 ne montre un signal KRAS dans les 3 criblages existants (0/60 composés FDR < 0,05). Le plus fort (VE-821 en GDSC2, rho −0,374, FDR 0,194 ; inhibiteur WEE1/CHEK1 −0,408, FDR 0,174) ne survit pas à la correction.
- **Dépendance CRISPR (balayage génome entier, déjà mesuré) : NON.** ATR rho +0,191 (FDR 0,865), CHEK1 +0,260 (FDR 0,748), BRCA2 −0,042, RAD51 −0,024, POLQ −0,246 — tous non significatifs. Les lignées KRAS-dépendantes ne dépendent pas plus d'ATR/CHEK1.

**Conclusion : piste ATR/CHEK1 REDRESSÉE, pas fermée.** Le « stress de réplication » comme signature large est fermé — c'était de la prolifération. Ce qui reste ouvert, c'est **ATR seul, comme hypothèse d'expression** (pas comme cible validée) : il monte avec KRAS au-delà de la prolifération dans 2 cohortes sur 3 où l'axe existe, mais sans appui en dépendance CRISPR ni en médicaments. CHEK1 est un marqueur de prolifération, pas une piste KRAS. Aucun test ici ne justifie une combinaison KRAS + ATR/CHEK1 — il faudrait d'abord une preuve de dépendance ou de sensibilité, qui n'existe pas dans ces données.

## 1. Re-test TCGA (178 tumeurs) — pureté puis prolifération

Versions : (a) BRUT, ordre KRAS brut — reproduction de `parp_direct_tests.csv` ; (b) RÉSIDUS pureté v3, ordre KRAS résidu (11/12 patients communs dans le top12 brut vs résidu) ; (c) DOUBLY-CORRIGÉ (résidus régressés sur le score de prolifération = médiane de MKI67, TOP2A, PCNA, CCNB1), ordre KRAS résidu ; partiel = Spearman gène vs rang KRAS contrôlé sur le score de prolifération. La reproduction (a) matche `parp_direct_tests.csv` à l'identique (rho et top12 à 6 décimales, 12/12 gènes).

### Les 7 gènes du protocole

| Gène | (a) brut rho | (b) résidus rho | (c) doubly rho | partiel prolif |
|---|---|---|---|---|
| **BRCA2** | **+0,420** (p 5,2e-9, top12 +0,54) | **+0,425** (p 3,3e-9, +0,47) | **+0,266** (p 3,3e-4, +0,08) | **+0,305** (p 3,6e-5) |
| **ATR** | **+0,407** (p 1,7e-8, +0,44) | **+0,409** (p 1,5e-8, +0,55) | **+0,273** (p 2,3e-4, +0,36) | **+0,366** (p 5,6e-7) |
| CHEK1 | +0,121 (ns, +0,60) | +0,116 (ns, +0,51) | −0,087 (ns, +0,20) | −0,143 (ns) |
| RAD51 | +0,184 (p 0,014, +0,33) | +0,170 (p 0,023, +0,27) | −0,187 (p 0,013, −0,53) | −0,171 (p 0,023) |
| POLQ | +0,289 (p 9,1e-5, +0,41) | +0,275 (p 2,1e-4, +0,37) | −0,008 (ns, −0,34) | +0,023 (ns) |
| PARP1 | −0,047 (ns) | −0,042 (ns) | −0,076 (ns) | −0,103 (ns) |
| PARP2 | −0,088 (ns) | −0,111 (ns) | −0,118 (ns) | −0,206 (p 0,006) |

Gènes (sur 7) avec p < 0,05 : brut 4/7 ; résidus 4/7 ; doubly 3/7 (BRCA2, ATR, et RAD51 inversé). Seuil Bonferroni 7 tests : p < 0,0071. Nul (graine 42, version b) : |rho| maximal 0,171 (ATR, p = 0,022, un hit nominal par hasard) ; BRCA2 −0,103.

### Pourquoi la pureté ne change rien, et pourquoi la prolifération change tout

- **R² pureté** (part de variance expliquée par acineux + îlots) : BRCA2 0,85 %, ATR 0,57 %, CHEK1 3,2 %, RAD51 2,6 %, POLQ 3,0 %, PARP1 0,02 %, PARP2 0,73 %. La pureté n'explique presque rien de ces gènes — contrairement aux marqueurs de la v4 (PGC/DPCR1/CLDN18), dont l'effondrement dépendait de la correction.
- **Le score de prolifération suit KRAS** : rho +0,386 (p = 1,1×10⁻⁷) en brut, +0,339 (p = 3,6×10⁻⁶) en résidus. Le confondant est réel.
- **Rho gène–prolifération** (résidus) : RAD51 +0,791, POLQ +0,768, CHEK1 +0,645, FANCD2 +0,633, BRCA1 +0,603, BRCA2 +0,543, CHEK2 +0,417, PARP2 +0,226, **ATR +0,214**, PARP1 +0,159, XRCC1 +0,110, ATM −0,229. ATR est le « monteur » le moins lié à la prolifération — c'est pour cela qu'il survit.
- **Sensibilité** : le score de prolifération calculé sur les valeurs brutes donne les mêmes partiels (BRCA2 +0,259, ATR +0,339, CHEK1 −0,172, RAD51 −0,187, POLQ −0,027) — le verdict ne dépend pas du choix du score.
- **Signal secondaire (non prévu au protocole, à noter) : CHEK2 devient négatif après contrôle prolifération** (doubly −0,312, p = 2,2×10⁻⁵ ; partiel −0,273, p = 2,4×10⁻⁴), alors qu'il était plat en brut (−0,092). Une fois la prolifération retirée, CHEK2 BAISSE avec KRAS. Curiosité, pas un verdict — non répliqué (ICGC partiel −0,142 ns ; GSE62452 +0,191 ns).

## 2. Contrôles ICGC (70) et GSE62452 (69) — mêmes tests directs que GEO71729

Valeurs brutes, ordre KRAS croissant, cas complets, nul graine 42. Secondaire : contrôle prolifération (même score, même Spearman partiel).

### ICGC — rien ne réplique (0/7)

| Gène | rho | p | top12 (sd) | partiel prolif |
|---|---|---|---|---|
| BRCA2 | −0,023 | 0,85 | +0,11 | −0,086 |
| ATR | +0,056 | 0,64 | +0,03 | +0,053 |
| CHEK1 | +0,163 | 0,18 | +0,13 | +0,153 |
| RAD51 | +0,063 | 0,60 | −0,19 | +0,009 |
| POLQ | +0,037 | 0,76 | −0,01 | −0,019 |
| PARP1 | −0,027 | 0,83 | +0,10 | −0,058 |
| PARP2 | +0,108 | 0,38 | +0,59 | +0,093 |

Score prolifération vs rang KRAS : +0,080 (p = 0,51) — **KRAS ne suit même pas la prolifération dans cette cohorte**. L'axe KRAS-expression y est plat, comme déjà vu pour MUC16 (+0,13) et CEA (+0,28). Nul : 0/7 p < 0,05.

### GSE62452 — tout monte, mais c'est de la prolifération (sauf ATR)

| Gène | rho | p | top12 (sd) | partiel prolif |
|---|---|---|---|---|
| **BRCA2** | **+0,495** (p 1,5e-5) | | +0,80 | +0,094 (ns) |
| **ATR** | **+0,656** (p 9,4e-10) | | +0,98 | **+0,488** (p 2,4e-5) |
| **CHEK1** | **+0,610** (p 2,7e-8) | | +1,17 | +0,192 (ns) |
| **RAD51** | **+0,352** (p 0,003) | | +0,49 | −0,164 (ns) |
| **POLQ** | **+0,447** (p 1,2e-4) | | +0,69 | −0,137 (ns) |
| PARP1 | +0,223 (p 0,065) | | +0,52 | +0,052 |
| PARP2 | +0,137 (ns) | | +0,42 | −0,029 |

5/7 gènes p < 0,05 en brut (nul 0/7) — mais le score de prolifération suit KRAS très fort (+0,597, p = 6,1×10⁻⁸), et les rho gène–prolifération sont extrêmes : CHEK1 +0,920, BRCA1 +0,851, POLQ +0,847, FANCD2 +0,795, BRCA2 +0,746, RAD51 +0,738, ATR +0,552. Après contrôle, **seul ATR survit** (+0,488). BRCA1, BRCA2, CHEK1, RAD51, POLQ, FANCD2 : tous morts ou inversés.

### Tableau de réplication — rho brut, 4 cohortes

| Gène | TCGA (178) | GEO71729 (145) | ICGC (70) | GSE62452 (69) | Brut significatif |
|---|---|---|---|---|---|
| **ATR** | **+0,407** | **+0,250** | +0,056 | **+0,656** | **3/4** |
| **BRCA2** | **+0,420** | **+0,481** | −0,023 | **+0,495** | **3/4** |
| CHEK1 | +0,121 ns | **+0,505** | +0,163 ns | **+0,610** | 2/4 |
| RAD51 | **+0,184** | **+0,427** | +0,063 ns | **+0,352** | 3/4 |
| POLQ | **+0,289** | −0,023 ns | +0,037 ns | **+0,447** | 2/4 |
| PARP1 | −0,047 ns | −0,138 ns | −0,027 ns | +0,223 ns | 0/4 |
| PARP2 | −0,088 ns | +0,014 ns | +0,108 ns | +0,137 ns | 0/4 |

### Après contrôle prolifération (Spearman partiel) — 3 cohortes

| Gène | TCGA | ICGC | GSE62452 | Survit où le signal existait |
|---|---|---|---|---|
| **ATR** | **+0,366** (p 5,6e-7) | +0,053 (ns) | **+0,488** (p 2,4e-5) | **2/2** |
| BRCA2 | **+0,305** (p 3,6e-5) | −0,086 | +0,094 (ns) | 1/2 |
| CHEK1 | −0,143 | +0,153 | +0,192 (ns) | 0/2 |
| RAD51 | −0,171 | +0,009 | −0,164 | 0/2 |
| POLQ | +0,023 | −0,019 | −0,137 | 0/2 |

## 3. Runs v6 — flux TCGA corrigés pureté (12 gènes réparation, ordre KRAS résidu)

| | Réel (`results_fast_atr`) | Nul graine 42 (`results_fast_atr_nul`) |
|---|---|---|
| Exit | 0 | 0 |
| Cible v6 | PARP1 (1re colonne, comme le bras PARP) | PARP1 |
| MC, meilleur score | 0,358 | 0,325 |
| T_-2 | 0,00 % | 0,00 % |
| T_-1 | 0,19 % (step 2) | 4,79 % |
| T_0 | 3,19 % (step 6) | 8,52 % |
| T_+1 | 45,12 % | 90,09 % |
| T_+2 | 45,12 % | 90,09 % |
| L7a | DOWN 16,06 %, désaccord (cible up, régime down) | UP 40,59 %, accord |
| L7b | FRAGILE (mode light) | FRAGILE (mode light) |
| Delta | 4,096, régime divergence | 4,001, régime divergence |

**Le pipeline v6 ne sépare pas le réel du nul ici non plus** (Delta 4,096 contre 4,001, même régime, même L7b FRAGILE, MC 0,358 contre 0,325) — comme sur le bras PARP brut (Delta 4,30 contre 4,04). Le T_0 réel est identique au bras brut (3,19 %) : la correction de pureté ne change pas la cascade. Comme établi, la cascade seule n'est pas un verdict : ce sont les tests directs (sections 1–2) qui le portent.

## 4. Médicaments ATR/CHEK1 dans les criblages existants — NON

Recherche par nom, MOA (mot entier — « MATRIX » ne matche pas « ATR ») et cible dans les 3 CSV existants. Aucun nouveau téléchargement. 60 vrais inhibiteurs ATR/CHEK1 trouvés au total, **0/60 avec FDR < 0,05**. Conventions : PRISM rho > 0 = lignées KRAS-dépendantes plus sensibles ; GDSC rho_LN_IC50 < 0 = plus sensibles.

| Composé | Cible | Criblage | rho | p | FDR |
|---|---|---|---|---|---|
| Ceralasertib (AZD6738) | ATR | PRISM primaire | +0,132 | 0,49 | 0,956 |
| Ceralasertib (AZD6738) | ATR | GDSC2 (LN_IC50) | −0,137 | 0,49 | 0,605 |
| Elimusertib (BAY-1895344) | ATR | PRISM primaire | −0,100 | 0,55 | 0,961 |
| VE-821 | ATR | GDSC2 (LN_IC50) | −0,374 | 0,055 | 0,194 |
| VE-821 | ATR | PRISM secondaire (AUC) | +0,254 | 0,20 | 0,913 |
| VE-822 | ATR | GDSC2 (LN_IC50) | −0,239 | 0,27 | 0,400 |
| ETP-46464 | ATR | PRISM secondaire (AUC) | +0,330 | 0,092 | 0,865 |
| ETP-46464 | ATR | PRISM primaire | −0,184 | 0,33 | 0,934 |
| AZ20 | ATR | PRISM primaire | +0,171 | 0,37 | 0,939 |
| Prexasertib (LY2606368) | CHEK1 | PRISM primaire | +0,059 | 0,75 | 0,974 |
| Prexasertib (LY2606368) | CHEK1 | PRISM secondaire (AUC) | −0,050 | 0,80 | 0,998 |
| Rabusertib (LY2603618) | CHEK1 | PRISM primaire | +0,046 | 0,81 | 0,979 |
| AZD7762 | CHEK1/CHEK2 | GDSC2 (LN_IC50) | −0,270 | 0,17 | 0,316 |
| MK-8776 | CHEK1/CHEK2/CDK2 | GDSC2 (LN_IC50) | −0,263 | 0,18 | 0,329 |
| Inhibiteur WEE1 (cible WEE1, CHEK1) | WEE1/CHEK1 | GDSC2 (LN_IC50) | −0,408 | 0,035 | 0,174 |
| SB-218078 | CHEK1 | PRISM secondaire (AUC) | −0,371 | 0,057 | 0,833 |

Plus forts signaux dans le sens « sensible » : inhibiteur WEE1/CHEK1 en GDSC2 (−0,408, p = 0,035, FDR 0,174) et ETP-46464 en PRISM secondaire (+0,330, p = 0,092, FDR 0,865) — aucun ne survit à la correction. **Berzosertib (VX-970) et SRA737 sont absents des 3 criblages** — non testables ici.

## 5. Dépendance CRISPR — déjà mesuré, pas d'appui

Balayage génome entier (47 lignées, `data/crispr_genome_scan.csv`) : ATR rho +0,191 (p = 0,197, FDR 0,865), CHEK1 +0,260 (p = 0,077, FDR 0,748), BRCA2 −0,042 (FDR 0,983), RAD51 −0,024 (FDR 0,989), POLQ −0,246 (FDR 0,761), PARP1 +0,157 (FDR 0,891), PARP2 −0,120 (FDR 0,922). Aucun significatif. L'expression ATR qui monte avec KRAS n'a **pas** de contrepartie en dépendance : les lignées KRAS-dépendantes ne dépendent pas plus d'ATR.

## 6. Ce que ça veut dire pour la piste ATR/CHEK1

**La piste est redressée, pas fermée — mais réduite à ATR seul, et sans appui fonctionnel.**

1. **Le « stress de réplication » large est fermé.** BRCA2/ATR/CHEK1/RAD51/POLQ qui montent ensemble avec KRAS, c'était en grande partie la prolifération : les tumeurs KRAS-fortes prolifèrent plus, et ces gènes sont des gènes du cycle. Une fois la prolifération retirée, il ne reste que BRCA2 (TCGA seulement) et ATR.
2. **ATR reste ouvert comme hypothèse d'expression.** Il monte avec KRAS au-delà de la prolifération dans 2 cohortes indépendantes (TCGA, GSE62452), survit à la pureté, et c'est le « monteur » le moins lié à la prolifération. Mais : pas de réplication en ICGC (où l'axe lui-même est plat), pas de dépendance CRISPR, pas de sensibilité aux inhibiteurs ATR dans les criblages. Une hypothèse d'expression, pas une cible.
3. **CHEK1 est un marqueur de prolifération.** Son rho brut (+0,505 en GEO, +0,610 en GSE62452, top12 jusqu'à +1,17 sd) s'effondre à zéro dès qu'on contrôle la prolifération (rho gène-prolif +0,645 à +0,920). Il ne porte pas une piste KRAS.
4. **PARP reste plat partout** (0/4 cohortes) — confirmé une fois de plus, y compris après les deux contrôles.
5. **Aucun test ici ne justifie une combinaison KRAS + ATR/CHEK1.** Il faudrait d'abord une preuve de dépendance (CRISPR : non) ou de sensibilité (criblages : non). Ce qui pourrait rouvrir la question : un criblage dose-réponse d'inhibiteurs ATR sur des lignées pancréas avec allèles KRAS connus (comme le test MRTX1133 par allèle), ou des données de combinaison KRAS + ATR en clinique — aucune des deux n'existe dans les données de ce projet.

## 7. Limites — à lire avant d'utiliser ce résultat

- **ARN bulk, pas de protéine.** L'expression ATR n'est pas l'activité ATR, ni sa phosphorylation, ni le statut mutationnel.
- **Le score de prolifération est un proxy** (4 gènes, médiane). Il capture la prolifération, mais il peut aussi capturer autre chose (cycle cellulaire au sens large). La sensibilité au score brut donne le même verdict — robuste au choix du score, mais le score reste un proxy.
- **Corriger pour la prolifération peut sur-corriger** : si KRAS *cause* la prolifération, retirer la prolifération retire une partie de l'effet KRAS lui-même. Le partiel mesure ce qui reste *au-delà* de la prolifération — c'est la bonne question pour « vraie biologie vs artefact », mais ce n'est pas la seule lecture possible.
- **ICGC est une cohorte où l'axe KRAS-expression est plat** : son nul ne dit pas « ATR ne monte pas avec KRAS en général », il dit « dans cette cohorte, KRAS n'ordonne rien ».
- **n = 69–70 dans les contrôles** : la puissance y est plus faible qu'en TCGA/GEO ; un effet modeste (rho ~0,25) y serait manqué. Mais les effets bruts de GSE62452 (+0,50 à +0,66) sont trop forts pour être des artefacts de puissance.
- **L7b FRAGILE des deux côtés** : l'audit de robustesse L7b est non informatif ici, comme déjà établi.

## 8. Fichiers livrés (tous dans `~/workspace/runs/pdac-v6/`)

| Fichier | Contenu | SHA-256 |
|---|---|---|
| `atr_chek1_retest.py` | Re-test TCGA (pureté + prolifération + flux v6) | `df6d1ddf…` |
| `atr_chek1_direct_tests_tcga.csv` | Tests directs TCGA, 4 versions × 12 gènes + partiels | `c19bbb70…` |
| `atr_chek1_direct_tests_tcga.txt` | Mêmes résultats en texte | `fd04b8ef…` |
| `atr_chek1_cohorts.py` | Tests directs ICGC + GSE62452 | `c5d5505e…` |
| `atr_chek1_direct_tests_cohorts.csv` | Tests directs ICGC + GSE62452 (réel, partiel, nul) | `1358f742…` |
| `atr_chek1_direct_tests_cohorts.txt` | Mêmes résultats en texte | `569ee9aa…` |
| `atr_chek1_drugs.py` | Recherche inhibiteurs ATR/CHEK1 dans les 3 criblages | `d4e81d76…` |
| `atr_chek1_drugs.csv` | 60 inhibiteurs ATR/CHEK1, rho/p/FDR par criblage | `f1321d38…` |
| `atr_chek1_drugs.txt` | Mêmes résultats en texte | `af87cdc6…` |
| `pdac_tcga_fluxes_atr.csv` | 12 gènes réparation en résidus pureté, ordre KRAS résidu (178 × 13) | `88e52311…` |
| `pdac_tcga_fluxes_atr_nul.csv` | Nul, graine 42 | `e7001154…` |
| `run_atr_v6.sh` | Lancement des 2 runs v6 fast | `5c96574f…` |
| `runs_atr_v6.log` | Journal des 2 runs (exit 0 / 0, SHA v6 vérifié) | `b6bdb084…` |
| `results_fast_atr/` | Sortie complète du run réel | — |
| `results_fast_atr_nul/` | Sortie complète du run nul | — |
| `atr_chek1_retest_provenance_tcga.json` | Provenance JSON du re-test TCGA | — |
| `atr_chek1_retest.md` | Ce rapport | — |
| `PROVENANCE_atr_chek1.md` | Provenance complète du re-test | — |
