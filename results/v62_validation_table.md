# Validation v6.2 — 10 runs fast x 2 repetitions (PROTOCOL_v6.2.md §5)

Pipeline : `universal_v6.2.0_cohen.py`, SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` ; v6.1 de reference SHA `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ; v6 SHA `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773` (inchangee). Mode `fast`, `--seed 42` (defaut).
Lanceur reprenable : `run_v62_lot.sh` + `manifest_v62_validation.txt`, surveille par `watch_v62_validation.sh` (systemd-run). Log : `runs_v62_validation.log`. Extraction : `extract_v62_validation.py`.
Deux redemarrages machine pendant le lot (18 nov. ~23h25 UTC et 19 nov. ~00h05 UTC) : le lanceur a repris la ou il s'etait arrete (2 runs deja complets conserves, 1 run partiel tue — TCGA v4 reel puis DepMap nul rep2 — refait proprement). 20/20 exit 0.

## Resultats par run (repetition 1 ; repetition 2 entre parentheses quand elle differe)

| Run | n | Cascade v6.2 rep1 (% T_-2 / T_-1 / T_0 / T_+1 / T_+2) | Cascade = v6.1 ? | MC best_score (v6.1) | max_sep | stab. | S_sep | Delta (v6.1) | L7a v6.2 (v6.1) | L5 top / conf / n_alerts | L4 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HP35 reel | 1000 | 0.00 / 1.55 / 9.08 / 37.78 / 37.78 | oui | 0.6035 (0.6035) | 1.7718 | 0.8687 | 1.5391 | 4.48 (4.48) | up 0.378 (up 0.377) | TwoNN / 0.661 / 2 | high 0.844 |
| HP35 nul | 1000 | 0.00 / 20.60 / 27.41 / 73.70 / 73.70 | oui | 0.4086 (0.4086) | 0.1206 | 0.9827 | 0.1185 | 4.57 (4.57) | up 0.338 (up 0.337) | MultifractalDeltaAlpha / 0.687 / 9 | medium 0.549 |
| TCGA v4 reel | 178 | 0.00 / 74.06 / 93.22 / 98.44 / 98.96 | oui | 0.3720 (0.3720) | 0.4623 | 0.9837 | 0.4548 | 4.18 (4.18) | down 0.405 (down 0.405) | BoxCounting / 0.802 / 9 | high 0.849 |
| TCGA v4 nul | 178 | 0.00 / 10.65 / 15.96 / 67.12 / 67.12 | oui | 0.3268 (0.3268) | 0.1696 | 0.9952 | 0.1688 | 3.77 (3.77) | up 0.167 (up 0.167) | Higuchi / 0.722 / 3 | high 0.785 |
| GSE62452 reel | 69 | 1.42 / 35.67 / 95.64 / 98.64 / 100.00 | oui | 0.3454 (0.3454) | 0.3100 | 0.9820 | 0.3044 | 1.41 (1.41) | down 0.197 (down 0.197) | Petrosian / 0.597 / 0 | low 0.000 |
| GSE62452 nul | 69 | 0.00 / 12.82 / 17.10 / 21.37 / 21.37 | oui | 0.3485 (0.3485) | 0.3136 | 0.9939 | 0.3116 | 1.26 (1.26) | down 0.336 (down 0.336) | PersistentHomology / 0.648 / 0 | low 0.000 |
| ICGC reel | 70 | 1.41 / 9.84 / 52.31 / 94.27 / 94.27 | oui | 0.3600 (0.3600) | 0.4080 | 0.9887 | 0.4034 | 1.44 (1.44) | up 0.181 (up 0.181) | Sevcik / 0.571 / 0 | low 0.000 |
| ICGC nul | 70 | 0.00 / 28.12 / 32.43 / 36.54 / 49.10 | oui | 0.3450 (0.3450) | 0.3110 | 0.9882 | 0.3073 | 1.37 (1.37) | down 0.350 (down 0.350) | Sevcik / 0.571 / 0 | low 0.000 |
| DepMap reel | 45 | 0.00 / 1.40 / 4.40 / 11.01 / 26.42 | oui | 0.3615 (0.3615) | 0.4436 | 0.9782 | 0.4339 | 1.93 (1.93) | down 0.196 (down 0.196) | DFA / 0.649 / 0 | low 0.000 |
| DepMap nul | 45 | 0.00 / 13.21 / 17.61 / 26.42 / 26.42 | oui | 0.3499 (0.3499) | 0.2532 | 0.9968 | 0.2524 | 1.69 (1.69) | up 0.345 (up 0.345) | Higuchi / 0.609 / 0 | low 0.000 |

Notes :
- HP35 reel : les valeurs brutes du controle (`thresholds_in_control_units`, controle `step`) sont [0, 16, 90, 376, 376] en v6.2 (rep1 et rep2) comme en v6.1 — exactement le « 0 / 16 / 90 / 376 » du protocole §5.3. Les cascades en % sont identiques a la v6.1 au chiffre pres sur les 10 runs.
- L7a HP35 reel 0,378 (v6.1 : 0,377) et TCGA v4 reel 0,405 (v6.1 : 0,405) : la graine L5 stable change legerement les alertes L5 donc le vote L7a (< 0,001, direction inchangee partout). Petites cohortes : L7a strictement identique a la v6.1 (GSE62452 down 0,197 ; ICGC up 0,181 ; DepMap down 0,196) — votes finis, pas de faux « up » / 0,50.
- DepMap reel : falsification absente du JSON (comme en v6.1) ; DepMap nul : fals 0,043.

## Determinisme — repetition 1 contre repetition 2 (processus separes)

| Run | JSON octet-pour-octet ? | Divergences (comparaison NaN-aware) : total / chemins runtime / budget workers / autres | L5 identique ? | L4 identique ? | L7a identique ? | Cles horodatage exactes ? |
|---|---|---|---|---|---|---|
| HP35 reel | non | 18 / 2 / 16 / 0 | oui | oui | oui | aucune |
| HP35 nul | non | 8 / 2 / 6 / 0 | oui | oui | oui | aucune |
| TCGA v4 reel | non | 8 / 2 / 6 / 0 | oui | oui | oui | aucune |
| TCGA v4 nul | non | 8 / 2 / 6 / 0 | oui | oui | oui | aucune |
| GSE62452 reel | non | 8 / 2 / 6 / 0 | oui | oui | oui | aucune |
| GSE62452 nul | non | 8 / 2 / 6 / 0 | oui | oui | oui | aucune |
| ICGC reel | non | 8 / 2 / 6 / 0 | oui | oui | oui | aucune |
| ICGC nul | non | 8 / 2 / 6 / 0 | oui | oui | oui | aucune |
| DepMap reel | non | 8 / 2 / 6 / 0 | oui | oui | oui | aucune |
| DepMap nul | non | 8 / 2 / 6 / 0 | oui | oui | oui | aucune |

Lecture du « non » octet-pour-octet (repli documente §5.2 du protocole) : les seules divergences entre repetitions sont (1) les deux chemins `/runtime/dashboard_status/path` et `/runtime/telemetry_path` — ils contiennent le nom du dossier de sortie, qui differe par construction (`_rep2`) ; (2) les champs `worker_budget` (`available_memory_bytes`, `memory_cap`, `chosen`, `safe_cap`, `n_workers`, `chunksize`), dans `/runtime/worker_budget` et recopies dans `optimization_diagnostics` / `raw_optimization_diagnostics` — ils refletent la RAM libre au lancement (la machine a redemarre deux fois pendant le lot). **Aucun champ scientifique ne differe sur les 10 runs (0 divergence « autre »).** Aucune cle d'horodatage exacte (`timestamp`, `date`, `generated_at`, `run_date`, `created_at`) dans aucun `master_results.json` (10/10) — la premiere version du controle comptait a tort « candidate » comme date (sous-chaine), corrige en controle par nom exact.

## Gigue mesuree par indicateur (max |rep1 − rep2| sur les 10 runs)

| Indicateur | Gigue mesuree |
|---|---|
| mc_score | 0.0 |
| max_sep | 0.0 |
| stability | 0.0 |
| s_sep | 0.0 |
| delta | 0.0 |
| fals | 0.0 |
| l4_risk | 0.0 |
| l5_conf | 0.0 |
| l5_stability | 0.0 |
| l7a_signed | 0.0 |
| cascade_max | 0.0 |

**Gigue L5 = 0** (ainsi que L4, L7a, MC, max_separation, S_sep, Delta, falsification et cascade) : la piste (a) — hachage stable — fonctionne. Gigue effective S_sep pour la phase 2 (§3.4) : max(0,00 mesuree ; 0,07 plancher) = **0,07**.

## Verdict §5.3

- 20/20 runs exit 0. Cascades identiques a la v6.1 : **10/10**.
- L7a fini sur les petites cohortes : oui (GSE62452, ICGC, DepMap — votes finis, identiques a la v6.1).
- Gigue L5 = 0 (L5, L4, L7a identiques entre repetitions sur 10/10 ; JSON non octet-pour-octet uniquement pour chemins runtime + budget workers, 0 champ scientifique divergent).
- **Validation REUSSIE.** La v6.2 reste une proposition : l'adoption comme version de travail attend le go de Zackary.

Donnees brutes : `v62_validation_table.json`, `v62_validation_extract.log`.
