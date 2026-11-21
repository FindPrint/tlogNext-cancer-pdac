# PROVENANCE — §8.75 : Clôture du résidu M2 du §8.63 (20 novembre 2026)

Protocole gelé : `PROTOCOL_m2_cloture_875.md`, SHA-256
`f829fd77fa5c938891814cbd7c80ef229a2dc3cd14f51b30d8babdd1e771d89c`.
Chantier §8.75, go de Zackary « Les 3 allez s'y » (20 nov. 2026 18h04,
3e des 3 pistes). Pipeline v6.2 JAMAIS modifié, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant le lot, avant toute relance et après le lot — voir
`runs_v62_875.log`).

## 1. Données nouvelles (40 nuls frais)

Méthode (identique à `build_nulls_icgc_863.py` et
`build_nulls_n70_853.py`) : `rng = default_rng(graine)`,
`perm = rng.permutation(n)`, lignes entières permutées (les 12 flux
d'une tumeur voyagent ensemble), colonne `step` inchangée, même
multi-ensemble de lignes vérifié par assert. Script neuf
`build_nulls_icgc_gse_875.py`, SHA-256
`0de249cd872640ac7828b82b98973e6c18b83a95e929822c0174bbc734390575`.

### Entrées (vérifiées par SHA avant construction)

| Cohorte | Fichier d'entrée | SHA-256 | Source |
|---|---|---|---|
| ICGC (n = 70) | `pdac_immune_icgc_fluxes.csv` | `10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc` | Relu dans `nulls_n70_853_verify.json`, re-vérifié ici avant construction ; provenance complète dans `PROVENANCE_immune_v6.md` et `PROVENANCE_icgc.md` (ARN bulk, ICGC PACA-AU, flux immunitaires 12 gènes) |
| GSE62452 (n = 69) | `pdac_immune_geo62452_fluxes.csv` | `97c4689a6ecacd0a73a77804200a72a90994d60bea7e6b2c079195acbffd79a3` | Idem ; provenance complète dans `PROVENANCE_geo62452.md` (GEO GSE62452, 69 tumeurs, puce Affymetrix, 14 447 291 octets, SHA `8f41d5b3…078cba`) |

### Sorties (40 fichiers, SHA-256 dans `nulls_icgc_gse_875_files.json`)

- ICGC, graines 61–90 (30 nuls, jamais utilisées ; existants :
  1–3, 11–60) : `pdac_immune_icgc_fluxes_nul_s61.csv` … `s90.csv`.
  Exemples : s61 `fc6abd056097…`, s70 `510768329060…`,
  s90 `89747b5466b4…` (liste complète dans le JSON).
- GSE62452, graines 31–40 (10 nuls, jamais utilisées ; existants :
  1–2, 11–30) : `pdac_immune_geo62452_fluxes_nul_s31.csv` …
  `s40.csv`. Exemples : s31 `61e39aa48def…`, s40 `118bd829d53f…`
  (liste complète dans le JSON).

### Nature des lignes

Nuls = lignes permutées (échantillons hypothétiques, pas des
mesures) : les 12 flux d'une tumeur voyagent ensemble, l'ordre des
lignes est détruit, les valeurs sont celles des mesures
instrumentales d'origine (ARN bulk). Aucune autre donnée nouvelle
dans ce chantier.

## 2. Données existantes relues (aucune modification)

- Nuls frais ICGC s11–s30 (§8.53, 20 runs
  `results_fast_v62_853_icgc_nul_s11/` … `s30/`) ; s31–s40
  (§8.63, 10 runs `results_fast_v62_863_icgc_nul_s31/` …
  `s40/`) ; s41–s60 (§8.73, 20 runs
  `results_fast_v62_873_icgc_nul_s41/` … `s60/`).
- Nuls frais GSE62452 s11–s30 (§8.53, 20 runs
  `results_fast_v62_853_geo62452_nul_s11/` … `s30/`).
- Faits de départ relus : `section_8.63_mechanisms.md` et
  `section_8.73_pic_etroit.md` (jamais réimportés comme verdicts).

## 3. Codes (jamais modifiés)

- Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
- Scripts neufs : `build_nulls_icgc_gse_875.py` (SHA ci-dessus),
  `run_v62_875.sh`, `watch_v62_875.sh`, `m2_cloture_875.py`
  (SHA `0deac752d372588384ebc23116f2bce88e0cb1faa9003e898a7eda70f6ddd90e`
  — version corrigée après détection d'une erreur de transcription
  dans la copie de `fwhm_rob_from_curve`, voir §8.75.9).

## 4. Sorties du chantier

- `manifest_v62_875.txt` (40 runs), `runs_v62_875.log` (40/40,
  exit 0), `watch_v62_875.log` (unité systemd `v62-875-watch`).
- Dossiers `results_fast_v62_875_icgc_nul_s61/` … `s90/` et
  `results_fast_v62_875_geo62452_nul_s31/` … `s40/`.
- `m2_cloture_875_extract.json` (lecture des 110 runs : 80 ICGC
  + 30 GSE), `m2_cloture_875_results.csv`.
- Section `section_8.75_m2_cloture.md`.

## 5. Ce qui manque, ce qui reste ouvert

- Le déclencheur du pic étroit (§8.73, NON ÉLUCIDÉ) n'est pas
  rouvert ici : ce chantier compte les basculements de
  robustesse sur le nouveau lot (définition gelée §2 E), sans
  en chercher la cause.
- Modes autres que fast (12 configs) : les taux mesurés ici
  sont propres au mode fast.
- PDF non régénéré, rien poussé sur GitHub (hors de ce chantier).
