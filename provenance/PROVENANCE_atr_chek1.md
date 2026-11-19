# Provenance — Re-test ATR/CHEK1 (16 nov. 2026)

Protocole gelé avant les runs. Aucune donnée d'une autre expérience n'entre
ici, sauf les chiffres cités comme « déjà mesurés » (bras PARP, balayage
CRISPR, criblages PRISM/GDSC2) et vérifiés par reproduction ou relecture
directe des CSV existants.

## Sources

| Donnée | Source | Vérification |
|---|---|---|
| TCGA-PAAD ARN | Broad GDAC Firehose stddata 2016-01-28, PAAD, RSEM genes normalized, `data/tcga_paad_rsem.tar.gz` (15 296 232 octets) | MD5 `b09569ce3f4721f514bc137bd109ac0a` vérifié avant chaque script ; 178 tumeurs primaires (code 01) ; log2(RSEM+1) |
| ICGC PACA-AU | UCSC Xena, `data/icgc_pacaau_exp.txt.gz` (log2 CPM, Bailey et al. 2016) + probemap Xena + clinique Bailey Suppl. Table 1 | 70 tumeurs primaires PDAC (même filtre que `build_fluxes_icgc.py`) |
| GSE62452 | GEO, `data/GSE62452_series_matrix.txt.gz` + mapping `data/GPL6244_probe2symbol.tsv` | 69 tumeurs (« tissue: Pancreatic tumor » ; même filtre que `build_fluxes_geo62452.py`) |
| GEO71729 (cité) | GEO GSE71729, `parp_direct_tests_geo71729.csv` (bras PARP, 16 nov.) | Chiffres repris du fichier, non recalculés |
| Criblages (point 5) | `data/prism_kras_screen_named.csv` (SHA `e7c100b4…`, 6 791 composés), `data/gdsc_kras_screen.csv` (SHA `e3bbdc17…`, 269 composés), `data/prism_secondary_kras_screen.csv` (SHA `49f97410…`, 1 427 composés) | Aucun nouveau téléchargement ; lecture seule |
| CRISPR (point 6) | `data/crispr_genome_scan.csv` (SHA `673e7080…`, balayage génome entier, 47 lignées) | Relecture directe des lignes ATR/CHEK1/BRCA2/RAD51/POLQ/PARP1/PARP2 |

## Méthodes

- **Correction pureté (v3)** : scores acineux (médiane des 11 gènes acineux
  de v1) + îlots (INS, GCG, PPY, SST) ; régression linéaire par gène sur
  [1, acineux, îlots] ; flux = résidus. Code identique à
  `build_fluxes_tcga_v4.py`. Ordre = résidu KRAS croissant.
- **Score de prolifération** : médiane de MKI67, TOP2A, PCNA, CCNB1.
  Primaire : médiane des résidus ; sensibilité : médiane des valeurs
  brutes (même verdict). Doubly-corrigé = résidu de chaque gène régressé
  sur le score. Spearman partiel = Pearson sur rangs régressés sur le
  rang du score (ddl n−3).
- **Tests directs** : rho = Spearman gène vs rang KRAS ; top12 = 12
  KRAS-forts, en écarts-types (ddof=0) ; recouvrement Q3 (attendu 3/12).
  Mêmes conventions que `parp_direct_tests.py`. Nul : lignes permutées,
  graine 42.
- **Runs v6** : pipeline v6 SHA
  `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`,
  mode fast, non modifié, cible = PARP1 (1re colonne, comme le bras PARP).
  Exit 0 / 0. Sorties complètes : `results_fast_atr/` (36 fichiers),
  `results_fast_atr_nul/` (36 fichiers).
- **Recherche médicaments** : nom de composé (normalisé), MOA par mot
  entier (`\bATR\b|\bCHK1\b|\bCHEK1\b` — « MATRIX » ne matche pas),
  cible par mot entier. Première version du script matchait « ATR »
  en sous-chaîne et attrapait les inhibiteurs de métalloprotéases
  (MATRIX) : bug trouvé et corrigé avant le rapport, CSV régénéré
  (60 vrais inhibiteurs, 0/60 FDR < 0,05). Les valeurs des vrais
  inhibiteurs sont identiques dans les deux versions.

## Résultats — chiffres clés

- TCGA brut → résidus → doubly → partiel : BRCA2 +0,420 → +0,425 →
  +0,266 → +0,305 ; ATR +0,407 → +0,409 → +0,273 → +0,366 ;
  CHEK1 +0,121 → +0,116 → −0,087 → −0,143 ; RAD51 +0,184 → +0,170 →
  −0,187 → −0,171 ; POLQ +0,289 → +0,275 → −0,008 → +0,023.
- R² pureté : BRCA2 0,85 %, ATR 0,57 %, CHEK1 3,2 %, RAD51 2,6 %,
  POLQ 3,0 %, PARP1 0,02 %, PARP2 0,73 %.
- Score prolifération vs rang KRAS : TCGA +0,386 (p 1,1e-7) brut /
  +0,339 (p 3,6e-6) résidus ; ICGC +0,080 (ns) ; GSE62452 +0,597
  (p 6,1e-8).
- GSE62452 partiels : ATR +0,488 (p 2,4e-5) ; BRCA2 +0,094 (ns) ;
  CHEK1 +0,192 (ns) ; RAD51 −0,164 (ns) ; POLQ −0,137 (ns).
- ICGC : 0/7 gènes p < 0,05 (BRCA2 −0,023, ATR +0,056, CHEK1 +0,163,
  RAD51 +0,063, POLQ +0,037).
- v6 : réel T_0 3,19 %, MC 0,358, Delta 4,096, L7a DOWN 16,06 %,
  L7b FRAGILE ; nul T_0 8,52 %, MC 0,325, Delta 4,001, L7a UP 40,59 %,
  L7b FRAGILE — ne sépare pas réel et nul.
- Médicaments : 0/60 FDR < 0,05. Plus forts : inhibiteur WEE1/CHEK1
  GDSC2 rho_LN_IC50 −0,408 (FDR 0,174) ; ETP-46464 secondaire
  rho_AUC +0,330 (FDR 0,865) ; VE-821 GDSC2 −0,374 (FDR 0,194).
  Ceralasertib : PRISM +0,132 (FDR 0,956), GDSC2 −0,137 (FDR 0,605).
  Prexasertib : PRISM +0,059, secondaire −0,050. Berzosertib et SRA737
  absents des 3 criblages.
- CRISPR : ATR +0,191 (FDR 0,865), CHEK1 +0,260 (FDR 0,748),
  BRCA2 −0,042, RAD51 −0,024, POLQ −0,246 — tous ns.

## Fichiers et SHA-256 (12 premiers caractères)

- `atr_chek1_retest.py` — `df6d1ddf9920`
- `atr_chek1_direct_tests_tcga.csv` — `c19bbb700659`
- `atr_chek1_direct_tests_tcga.txt` — `fd04b8ef7249`
- `atr_chek1_cohorts.py` — `c5d5505e6ed5`
- `atr_chek1_direct_tests_cohorts.csv` — `1358f742f093`
- `atr_chek1_direct_tests_cohorts.txt` — `569ee9aa15a7`
- `atr_chek1_drugs.py` — `d4e81d76f008`
- `atr_chek1_drugs.csv` — `f1321d38542e`
- `atr_chek1_drugs.txt` — `af87cdc697d5`
- `pdac_tcga_fluxes_atr.csv` — `88e52311a2cc`
- `pdac_tcga_fluxes_atr_nul.csv` — `e70011545f23`
- `run_atr_v6.sh` — `5c96574f52d5`
- `runs_atr_v6.log` — `b6bdb084443b`
- `atr_chek1_retest.md` — `498b5ca46053`
- `atr_chek1_retest_provenance_tcga.json` — provenance JSON du re-test TCGA

## Limites

- ARN bulk, pas de protéine ; score de prolifération = proxy (4 gènes).
- Corriger pour la prolifération peut sur-corriger si KRAS cause la
  prolifération (le partiel mesure ce qui reste au-delà de la
  prolifération).
- ICGC : axe KRAS-expression plat ; n = 69–70 dans les contrôles
  (puissance plus faible).
- CHEK2 négatif après contrôle prolifération (TCGA seulement) : signal
  secondaire non prévu au protocole, non répliqué — curiosité, pas un
  verdict.
