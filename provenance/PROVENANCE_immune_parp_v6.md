# PROVENANCE — Paysages immunitaire et réparation/PARP le long de l'axe KRAS (runs v6, 16 nov. 2026)

## Instrument

Pipeline v6 : `~/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py`, SHA-256 `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`, vérifié avant et après les runs, jamais modifié. Mode fast, cohen_d partout, minimum 50 points. 10 runs, tous exit 0. Les deux bras ont tourné en parallèle sur la même VM (2 vCPU, 7,7 Go RAM) — runs ralentis (~10 min au lieu de ~8), sans effet sur les sorties.

## Données sources (rien re-téléchargé)

- TCGA PAAD : Firehose `data/tcga_paad_rsem.tar.gz`, MD5 `b09569ce3f4721f514bc137bd109ac0a` (vérifié), 20 532 gènes × 183 échantillons, 178 tumeurs primaires, log2(RSEM+1), ordre KRAS brut croissant.
- GSE71729 : matrice GEO déjà sur disque, SHA `b2287893…536a54`, 145 tumeurs.
- GSE62452 : matrice GEO déjà sur disque, SHA `8f41d5b3…078cba`, 69 tumeurs.
- ICGC PACA-AU : fichier Xena déjà sur disque, SHA `c2cb57af…0f49fa`, 70 tumeurs.

## Flux construits

- Immunitaire (12 gènes) : CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274, PDCD1, CTLA4, GZMB, IFNG, CD19. Écart documenté : en ICGC, IFNG→PRF1 et CD19→MS4A1 (CD20) — le protocole ne nommait qu'un seul remplaçant ; dupliquer PRF1 aurait créé deux colonnes identiques. SHA des CSV : TCGA `66dbb672…`, GSE71729 `8987ffca…`, GSE62452 `97c4689a…`, ICGC `10823879…`.
- Réparation/PARP (12 gènes) : PARP1, PARP2, BRCA1, BRCA2, ATM, ATR, CHEK1, CHEK2, RAD51, XRCC1, POLQ, FANCD2. Tous présents, 178/178 valeurs valides, aucun remplacement. SHA : TCGA `c9549b68…c4309`, nul `57245c72…b1360` ; GEO `99abbd6e…722c`.
- Nuls : mêmes lignes permutées, graine 42, même construction que les nuls existants. Aucune imputation ; règle ≥50 valeurs valides.

## Runs v6

- Immunitaire : 8 runs (`results_fast_immune_{tcga,geo71729,geo62452,icgc}(_nul)/`), cible CD8A, extraction `immune_v6_runs_summary.json`, log `runs_immune_v6.log`.
- PARP : 2 runs (`results_fast_parp/`, `results_fast_parp_nul/`, 36 fichiers chacun), cible PARP1, log `runs_parp_v6.log`.
- Le pipeline ne sépare pas réel et nul sur ces flux (MC et Delta proches, nul au-dessus en ICGC immune ; MC 0,355 vs 0,331 et Delta 4,30 vs 4,04 en PARP). L7a : DOWN 18 %/39 % (TCGA/GSE71729 immune), UP 50 % = repli NaN en GSE62452/ICGC (`scores_unavailable`, n < 75 — artefact connu, §8.14 du livre blanc).

## Tests directs (verdicts)

- Immunitaire : `direct_tests_immune.py`, `immune_direct_tests.csv/.txt` — Spearman contre KRAS + top-12 vs reste (d de Cohen, p Welch) par cohorte. 16/48 tests p < 0,05 contre ~2,4 attendus sous le nul.
- PARP : `parp_direct_tests.py`, `parp_direct_tests.csv/.txt` (TCGA) et `parp_direct_tests_geo71729.csv/.txt` (contrôle GEO).

## Limites

- ARN en vrac sans correction de pureté dans les deux bras (la baisse des marqueurs T peut être une composition ; re-test style v4 nécessaire avant « tumeur-intrinsèque »).
- Prolifération non contrôlée pour le bras PARP (BRCA2/ATR/CHEK1/RAD51 sont aussi des gènes du cycle).
- Expression ≠ protéine ≠ mutation : l'indication PARP validée (mutation germinale BRCA, olaparib/POLO) n'est pas testée et n'est pas remise en cause.
- ICGC/GSE62452 non faites pour le bras PARP.

## Rapports par bras

`immune_v6.md` + `PROVENANCE_immune_v6.md` ; `parp_v6.md` + `PROVENANCE_parp_v6.md`. Rapport combiné : `immune_parp_v6.md`.
