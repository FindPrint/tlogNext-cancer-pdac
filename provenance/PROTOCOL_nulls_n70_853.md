# PROTOCOLE GELÉ — Distribution des nuls à n≈70 (§8.53)

Date de gel : 19 novembre 2026, avant tout run et toute analyse neuve.
Chantier 4/4 (coordinateur : fusion dans le livre blanc ensuite).
Règle durable : protocole gelé AVANT les runs ; provenance complète nommée ;
verdicts seulement sur les données et runs du jour ; ne jamais importer de
conclusions d'autres expériences ; ne pas exiger de consensus entre
flux/contrôles ; un nul qui invalide une piste est un résultat ; ne jamais
inventer de valeur. Pipeline v6.2 JAMAIS modifié.

## 1. Question

À n≈70, S_sep lu sur un seul nul est un tirage, pas une mesure (§8.47) :
réel ICGC maxsep 0,2299 battu par un nul dans 61 % des cas (500
permutations) ; nul graine 42 haut (0,4500, ~98e percentile) mais ordinaire
(1 nul frais sur 3 atteint 0,4564). Ce chantier mesure la DISTRIBUTION
complète des S_sep nuls à n≈70, pour en déduire (a) le plancher honnête à
n≈70 — quel écart réel−nul faut-il pour parler de mesure ? — et (b) combien
de nuls faut-il en pratique pour qu'un écart S_sep devienne une mesure.

## 2. Faits de départ (relus le 19 nov. 2026, §8.47 — lecture seule)

- S_sep = max_separation × stabilité ; stabilité saturée (0,97–1,00),
  donc S_sep ≈ max_separation. La distribution mesurée ici est celle de
  S_sep (maxsep × stab par tirage), avec maxsep rapporté en parallèle.
- Réplique §8.47 (500 permutations par ligne, config fixe) :
  médiane maxsep nul ICGC 0,2458 [p2,5 0,157 ; p97,5 0,443] (n=70) ;
  GSE62452 0,2426 [0,159 ; 0,395] (n=69) ; TCGA 0,1700 [0,089 ; 0,324]
  (n=178) ; GSE71729 0,1757 (n=145). Plancher nul relevé de ~+0,07 à
  n≈70 par rapport à n=178.
- Lot pipeline §8.47 (11 runs v6.2 fast, 11/11 exit 0) : nuls frais
  ICGC s1/s2/s3 S_sep 0,1769 / 0,2396 / 0,4497 ; GSE62452 s1/s2 0,2780 /
  0,1861 ; TCGA s1/s2 0,2465 / 0,1390. 6/7 dans l'intervalle 95 % de la
  réplique ; l'optimiseur (libre de choisir sa config par run) élargit
  légèrement la distribution des nuls au-delà de la réplique à config
  fixe — écart à quantifier ici.
- Réels (pipeline v6.2, §8.38) : ICGC S_sep 0,2289 (n=70) ; GSE62452
  0,4656 (n=69) ; TCGA 0,5263 (n=178).

## 3. Bras et choix justifiés

- **Bras principal : immunitaire ICGC (n=70)** — c'est le bras de
  l'inversion §8.47 ; la question porte sur lui.
- **Bras témoin : immunitaire GSE62452 (n=69)** — même taille (69
  contre 70), même bras immunitaire, mêmes 12 flux, mais réel qui
  sépare nettement (0,4804, P(nul ≥ réel) = 0,004). Si le plancher nul
  y égale celui d'ICGC, le plancher est un effet de n, pas de cohorte ;
  si les planchers diffèrent, le plancher dépend aussi de la cohorte.
- **Bras de contraste : immunitaire TCGA (n=178)** — même bras, n
  grand ; quantifie l'effet de n sur le plancher (médiane, p95).
  GSE71729 (n=145) n'est pas refait : sa médiane §8.47 (0,1757) est
  citée en référence seulement, pas comme résultat de ce chantier.

## 4. Méthodes (ordre d'exécution)

### (a) Vérification des entrées (aucun run, script neuf)
`verify_nulls_n70_853.py`. Re-vérifie les SHA-256 des 6 CSV de flux
(réel + nul graine 42, ICGC / GSE62452 / TCGA) contre
PROVENANCE_immune_v6.md ; vérifie que chaque nul graine 42 est une
permutation par ligne du réel ; 0 valeur manquante ; n par bras.
Sorties : `nulls_n70_853_verify.json` + log.

### (b) Réplique du scan : distribution des S_sep nuls, 1000 tirages (aucun run pipeline)
Script neuf `replica_nulls_n70_853.py`, réutilisant la machinerie
calibrée de `replica_scan_847.py` (fonctions DU PIPELINE, import en
lecture seule, aucune modification : `_build_mc_progress_axis` +
`scan_critical_threshold` + `evaluate_scan_quality` ; axe progress_pct
identique pour réel et nuls d'une même cohorte).
- CALIBRATION D'ABORD : reproduire max_separation des 8 runs v6.2
  existants (réel + nul42, 4 cohortes) à ±0,001, courbe comprise —
  sinon la réplique est rejetée et le chantier s'arrête sur la
  calibration (comme §8.47 §9).
- PUIS, par cohorte (ICGC, GSE62452, TCGA), sous les DEUX configs
  fixes (config réelle et config nulle du run v6.2 existant) :
  1000 permutations par ligne (graines 2000–2999, tirage maître
  `default_rng(20261119)` — NOUVELLE graine maîtresse, distincte de
  §8.47, pour que les tirages soient frais), chaque tirage donnant
  maxsep ET stabilité, donc S_sep = maxsep × stab. Les 1000 valeurs
  brutes par (cohorte, config) sont conservées intégralement
  (JSON + CSV) : aucune statistique ne doit être recomputable
  seulement d'un résumé.
- Convergence (sur ces 1000 tirages, par cohorte, config nulle) :
  pour k = 1, 2, 3, 5, 10, 20, 30, 50, 100, 200, 500, 1000,
  200 sous-échantillons sans remise de taille k → médiane des
  médianes, écart-type des médianes (SE empirique de la médiane),
  médiane et intervalle [p2,5 ; p97,5] du p95 estimé ; même chose
  pour l'écart-type. Le nombre de nuls requis est lu sur ces courbes
  (§5, critères gelés).

### (c) Construction des nuls frais (aucun run, script neuf)
`build_nulls_n70_853.py`, même méthode que `build_icgc_immune_847.py`
(`default_rng(graine)`, `permutation(n)`, lignes entières permutées,
colonne step inchangée) :
- ICGC : graines 11–30 (20 nuls frais, `pdac_immune_icgc_fluxes_nul_s11.csv` … `s30`) ;
- GSE62452 : graines 11–30 (20 nuls frais) ;
- TCGA : graines 11–15 (5 nuls frais, contraste n=178).
Graines 11+ : nouvelles, jamais utilisées (§8.47 : 1–3 ; graine 42).
Aucune graine réutilisée. SHA-256 de chaque fichier consignés dans
`nulls_n70_853_files.json`.

### (d) Lot pipeline v6.2 (runs réels, seulement après (a)–(c))
Fichier v6.2 : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(à re-vérifier avant chaque lancement et après le lot, jamais modifié).
Mode fast, `--input <csv> --mode fast --output <dir>`, lancé depuis
`~/workspace/runs/pdac-v6/` via `systemd-run` (leçon AGENTS.md : les
lots longs survivent à la session) + journal des exit codes
(`runs_nulls_n70_853.log`, unité `v62-853`). 45 runs : 20 ICGC + 20
GSE62452 + 5 TCGA. Dossiers `results_fast_v62_853_*`.
Extraction : `extract_nulls_n70_853.py` (lecture des
`master_results.json` : maxsep, stabilité, S_sep, MC, Delta, L7a,
seuil, config choisie) + jointure avec les nuls pipeline déjà
existants (§8.47 : ICGC s1–s3 + nul42 ; GSE62452 s1–s2 + nul42 ;
TCGA s1–s2 + nul42) pour les distributions pipeline complètes :
ICGC 24 tirages, GSE62452 23, TCGA 8. Sortie :
`nulls_n70_853_confirm.json` + log.

## 5. Règles de verdict et critères (écrits avant toute analyse)

- **Plancher honnête à n≈70** : le p95 de la distribution des S_sep
  nuls (config nulle, réplique 1000 tirages, confirmé par le lot
  pipeline). Un réel est dit « indistinguable d'un tirage nul » si
  S_sep réel < p95 nul ; « au-dessus du plancher » si ≥ p95 nul.
  Le plancher est rapporté aussi en écart : d_plancher = p95 − médiane
  nulle, et en unités d'écart-type nul : (réel − médiane) / SD nul.
  Règle d'interprétation : un écart réel−médiane nulle inférieur à
  l'IQR nul est un bruit de tirage, pas une mesure.
- **Nombre de nuls requis** : le plus petit k tel que, sur les courbes
  de convergence (§4b), (i) l'écart-type empirique de la médiane
  estimée sur k tirages ≤ 0,01 ET (ii) la demi-largeur de
  l'intervalle 95 % du p95 estimé sur k tirages ≤ 0,03. Si aucun k
  ≤ 1000 ne satisfait (i) et (ii) ensemble, le dire : le nombre requis
  dépasse 1000. Le nombre est rapporté séparément pour la médiane et
  pour le p95 ; le nombre « en pratique » est le max des deux.
  Vérification croisée : l'écart-type de la médiane sur les ~24 nuls
  pipeline ICGC (bootstrap) doit être cohérent avec la courbe
  réplique à k=24 (tolérance ±0,01).
- **Validation réplique ↔ pipeline** : la réplique est déclarée
  prédictive du pipeline si, par bras, |médiane pipeline −
  médiane réplique (config nulle)| ≤ 0,03 ET |p95 pipeline − p95
  réplique| ≤ 0,05 (tolérance large : le lot pipeline n'a que 24
  tirages, l'optimiseur choisit sa config). Sinon, la réplique est
  déclarée non prédictive et les verdicts de plancher reposent sur
  le lot pipeline seul (avec ses limites : 24 tirages).
- **Effet de n** : quantifié par Δ médiane et Δ p95 entre n≈70
  (ICGC, GSE62452) et n=178 (TCGA), en réplique et en pipeline.
  Un effet est dit « de n » si les deux bras n≈70 s'accordent entre
  eux (médianes à ±0,03) et diffèrent tous deux de TCGA dans le même
  sens ; sinon, l'effet est « de cohorte autant que de n ».
- **Un nul qui invalide une piste est un résultat** : si la
  distribution pipeline des nuls ICGC recouvre le réel (réel sous le
  p95 nul), le verdict est « le réel ICGC ne se distingue pas d'un
  nul à n≈70 », pas un échec de mesure.
- Ne jamais présenter un seul nul comme « le » nul ; ne jamais
  importer de conclusions d'autres expériences (MTAP, test C,
  rotations, §8.47 au-delà des faits relus §2) : seules les données
  et runs de ce chantier font foi ici, sauf citation explicite
  « relu §8.47 » pour les faits de départ.

## 6. Livrables

1. Ce protocole (SHA noté dans la section).
2. Section complète §8.53 :
   `~/workspace/runs/pdac-v6/section_8.53_nulls_n70.md`
   (verdict d'abord, chiffres, méthode, limites, provenance).
3. Scripts : `verify_nulls_n70_853.py`, `replica_nulls_n70_853.py`,
   `build_nulls_n70_853.py`, `extract_nulls_n70_853.py`,
   `run_nulls_n70_853.sh` (SHA notés dans la section).
4. Données/résultats : `nulls_n70_853_verify.json`,
   `nulls_n70_853_replica.json` (+ `.csv` des 1000 tirages bruts par
   cohorte/config : `nulls_n70_853_replica_raw.csv`),
   `nulls_n70_853_convergence.json` (+ `.csv`),
   `nulls_n70_853_files.json` (SHA des 45 fichiers de nuls),
   `nulls_n70_853_confirm.json`, dossiers `results_fast_v62_853_*`,
   log `runs_nulls_n70_853.log` (unité systemd `v62-853`).

## 7. Provenance des entrées (déjà sur disque, rien re-téléchargé)

- Flux immunitaires : `pdac_immune_{tcga,geo62452,icgc}_fluxes(_nul).csv`,
  SHA dans PROVENANCE_immune_v6.md (ICGC réel `10823879…`, nul
  `3393ecd6…` ; GSE62452 réel `97c4689a…` ; TCGA réel `66dbb672…`).
- Matrices sources : TCGA Firehose PAAD MD5 `b09569ce…` ; GSE62452
  SHA `8f41d5b3…` ; ICGC Xena SHA `c2cb57af…` (Bailey et al., Nature
  2016, doi:10.1038/nature16965).
- Pipeline v6.2 : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA `f07567c4…` (§8.37).
- Livre blanc : `~/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md`,
  SHA `31bc39a1…`, §8.1–§8.49.
- Faits de départ §8.47 : `section_8.47_icgc_immune_inversion.md`,
  protocole `PROTOCOL_icgc_immune_inversion.md` SHA `b55283ee…`
  (amendé `f1a5a37c…`).

## 8. Limites connues d'avance

- La réplique fixe les configs ; l'optimiseur en choisit une par run —
  la distribution des nuls du pipeline tel qu'il tourne est un peu plus
  large que celle de la réplique (§8.47 : 1 nul frais sur 3 au-dessus
  de p97,5). Le lot (d) est là pour calibrer cet écart.
- 24 tirages pipeline par bras n≈70 : la queue (p95) y est estimée
  avec une large incertitude — la réplique 1000 tirages porte
  l'estimation du p95, le lot pipeline la confirme ou la conteste.
- n=70 : toute distribution estimée reste une distribution du scan,
  pas une preuve biologique.
- ARN bulk sans correction de pureté (choix du bras §8.23) : ce
  chantier n'y touche pas.
- Les graines 11–30 sont nouvelles mais le générateur de nuls reste
  la permutation par ligne (corrélations inter-flux préservées) :
  la distribution mesurée est celle du nul du projet, pas d'un nul
  à corrélations brisées (§8.47 H5 : écart de médianes 0,0115 en
  ICGC — petit, mais nommé).
