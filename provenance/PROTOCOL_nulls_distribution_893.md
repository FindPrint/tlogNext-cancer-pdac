# PROTOCOLE GELÉ — §8.93 : chaque paire jugée contre une distribution de nuls

Date de gel : 21 novembre 2026, avant tout run et tout calcul neuf.
Statut : **PROTOCOLE GELÉ. Aucun calcul, aucun run lancé avant ce gel. Toute déviation arrête le travail et se consigne, elle ne se corrige pas en silence.**
Coordinateur : TagPrint. Go de Zackary « Faite tout cela », 21 nov. 2026 11h36, piste 1/4.
Dossier : `~/workspace/runs/pdac-v6/`.
Pipeline : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256 vérifié avant gel `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` (v6.1 `2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`, revérifiés inchangés le 21 nov. 2026). v6.2, v6.1, v6 ne sont JAMAIS modifiées.
Références : livre blanc §8.47 (réplique 500 permutations), §8.50 (MTAP 10/10 nuls frais), §8.53 (distribution des nuls à n≈70, 1000 tirages), §8.70 (GSE79668 renverse), §8.72 (renverse), §8.88.3 (table des 15 paires A2), §8.90.1.2 (correction de Zackary : le verdict, c'est la batterie entière, jamais un score seul — `maxsep` = score principal AFFICHÉ).

## 0. Question

Un seul nul peut renverser un verdict (§8.50 : 10/10 ; §8.72 : renverse ; §8.70 : GSE79668 renverse +0,1447 contre 13 nuls). Chaque paire est donc rejugée ici contre une DISTRIBUTION de nuls, pas contre un seul tirage : rang du réel, p95 des nuls, combien de nuls passent le plancher 0,07. A2 est recalculé contre les distributions.

## 1. Faits de départ (relus, jamais recalculés ici)

- §8.53 : à n≈70, il faut ≈200 nuls pour un plancher stable ; plancher nul relevé de ~+0,07 à n≈70 par rapport à n=178 ; réel ICGC maxsep 0,2289 battu par un nul dans 61 % des cas (500 permutations).
- A2 actuel (§8.88.3) : **10/15, 12/15 positifs, LOO 9/14** — table reprise telle quelle, jamais recalculée, comme base de comparaison.
- 1 run v6.2 fast dure ~5 min (`PROTOCOL_mtap_consolidation_850.md`).

## 2. FAISABILITÉ — vérifiée AVANT le gel (c'est le point de ce protocole)

| Option | Runs | Temps (5 min/run, 2 vCPU, séquentiel) | Verdict faisabilité |
|---|---|---|---|
| 200 nuls pipeline × 15 paires | 3 000 | ~250 h ≈ 10,4 jours continus | **INFAISABLE en lot unique** |
| 200 nuls pipeline × 8 paires principales | 1 600 | ~133 h ≈ 5,5 jours continus | **INFAISABLE en lot unique** |
| Réplique 1000 permutations × paire (machinerie pipeline en lecture seule, précédent §8.47/§8.53 : 1000 tirages × 3 cohortes × 2 configs dans un seul chantier) | 0 run pipeline | heures, pas jours | **FAISABLE — voie principale** |
| 10 nuls frais pipeline × 8 paires (validation) | 80 | ~7 h, lot systemd avec surveillance | **FAISABLE — étape 1** |
| 10 nuls frais pipeline × 7 paires A2 restantes (validation) | 70 | ~6 h | **FAISABLE — étape 2** |

**Décision gelée : la distribution est mesurée par RÉPLIQUE (1000 permutations par ligne, config fixe), calibrée contre les runs pipeline existants ; les nuls frais pipeline (10 par paire) servent de validation hors réplique, pas de distribution principale.** Si la calibration échoue (§3a), le chantier s'arrête sur la calibration, comme §8.47 §9.

## 3. Paires et méthode (ordre d'exécution)

### 3a. Calibration (aucun run neuf)
Script neuf `replica_nulls_893.py`, réutilisant la machinerie calibrée de `replica_nulls_n70_853.py` / `replica_scan_847.py` (fonctions DU PIPELINE, import en lecture seule, aucune modification : `_build_mc_progress_axis` + `scan_critical_threshold` + `evaluate_scan_quality` ; axe progress_pct identique pour réel et nuls d'une même cohorte).
- Reproduire `maxsep` des runs v6.2 existants (réel + nul graine 42) des 8 paires principales à ±0,001, courbe comprise — sinon arrêt et diagnostic.
- Vérifier les SHA-256 des CSV de flux de chaque paire contre les provenances publiées ; chaque nul graine 42 est une permutation par ligne du réel ; 0 valeur manquante ; n par paire.

### 3b. Étape 1 — les 8 paires principales (V1, §8.56)
HP35, TCGA v4, GSE71729, GSE62452, ICGC, Immunitaire TCGA, PARP TCGA, DepMap (mêmes dossiers `results_fast_v62_*` que §8.56).
- Par paire : réplique 1000 permutations par ligne (graines 3000–3999, tirage maître `default_rng(20261121)` — NOUVELLE graine maîtresse, distincte de §8.47 et §8.53), sous les DEUX configs fixes (config réelle et config nulle du run v6.2 existant). Chaque tirage donne maxsep ET stabilité, donc S_sep = maxsep × stab, ET MC (le composite est recalculé depuis les métriques du tirage, même code que le pipeline). Les 1000 valeurs brutes par (paire, config) sont conservées intégralement (JSON + CSV).
- Validation pipeline : 10 nuls frais par paire (graines gelées ici, jamais utilisées dans ce projet : 9101, 9102, 9103, 9104, 9105, 9106, 9107, 9108, 9109, 9110), runs v6.2 fast, lot systemd avec surveillance, journal des exit codes. 80 runs ≈ 7 h.
- Question subsidiaire, lue sur les mêmes données : le p95 des nuls frais pipeline tombe-t-il dans l'intervalle de la réplique ? (Écart consigné, pas corrigé.)

### 3c. Étape 2 — les 7 paires A2 restantes
GSE21501 (§8.69), GSE79668 (§8.70), GSE60979 (§8.71), GSE131050 Yeh FF (§8.74), GSE57495 (§8.79, 11 flux), GDC ORGANOID-PANCREATIC (§8.85, 12 flux, MUCL3 ex-DPCR1), GSE194249 (§8.88, 11 flux, DPCR1 absent).
- Même méthode qu'en 3b (réplique 1000 tirages × 2 configs + 10 nuls frais pipeline par paire, mêmes graines 9101–9110). 70 runs ≈ 6 h.
- Les paires à 11 flux gardent leurs 11 flux tels quels (DPCR1 absent : fait, pas défaut à corriger) ; la paire GDC garde MUCL3 ex-DPCR1 (§8.85).

## 4. Lecture gelée (avant tout résultat)

Par paire, depuis la distribution réplique (config réelle ; config nulle en sensibilité) :
- rang du réel (ascendant, /1001 avec le réel inclus), p95 des nuls, médiane des nuls, nombre de nuls avec écart réel−nul > 0,07.
- **SOLIDE** si réel > p95 des nuls ET ≥ 950/1000 nuls sous le plancher (écart > 0,07 contre au moins 95 % des nuls).
- **FRAGILE** si réel > médiane des nuls mais ≤ p95, OU si 50–95 % des nuls sous le plancher.
- **NON** si réel ≤ médiane des nuls, OU si < 50 % des nuls sous le plancher.
- La lecture par paire utilise la BATTERIE entière (§8.90.1.2) : maxsep, MC, Delta, L7a, falsification, F1/F2 sont rapportés par paire depuis les runs existants + les nuls frais ; `maxsep` ne porte jamais le verdict seul. Un nul frais qui contredit la réplique est consigné et discuté, pas écarté.
- **A2 recalculé** : une paire compte comme passante si et seulement si elle est SOLIDE au sens ci-dessus (réel > p95, ≥ 95 % des nuls sous le plancher). A2-distrib, positifs-distrib et LOO-distrib sont publiés à côté de A2 classique (10/15) — les deux comptes coexistent, l'ancien n'est pas réécrit.
- Sensibilités rapportées, non décisives : (a) config nulle au lieu de config réelle ; (b) plancher 0,05 et 0,10 au lieu de 0,07 ; (c) S_sep au lieu de maxsep.

## 5. Ce qui n'est PAS fait ici

- Aucun nouveau run réel (les réels sont ceux des runs existants, relus tels quels).
- Aucune paire hors des 15 A2 (ni FNA §8.76 apparié, ni drogue §8.84 hors compte, ni rotations — les rotations ont leur propre distribution au §8.44/§8.56).
- Aucune modification du pipeline, aucune repondération après coup, aucune exclusion de paire parce qu'elle échoue.

## 6. Livrables

- `replica_nulls_893.py` + `nulls_dist_893_verify.json` + log de calibration.
- `nulls_dist_893_replica.json` + CSV bruts (1000 valeurs par paire × config, intégrales).
- `nulls_dist_893_fresh.json` (80 + 70 runs frais, exit codes, maxsep/MC/Delta/L7a par run).
- `nulls_dist_893_table.json` (par paire : rang, p95, médiane, % sous plancher, verdict SOLIDE/FRAGILE/NON, A2-distrib).
- Section `section_8.93_nulls_distribution.md` (fichier séparé ; livre blanc NON édité directement ; PDF NON régénéré ; rien poussé).
- Provenance `PROVENANCE_893.md` (SHA des scripts, des CSV, des JSON ; graines ; lots systemd).

## 7. Limites déclarées d'avance

- La réplique est à config fixe ; l'optimiseur libre (qui choisit sa config par run) élargit légèrement la distribution des nuls (§8.53) — l'écart réplique vs nuls frais pipeline est mesuré ici (§3b), pas supposé nul.
- Les nuls sont des permutations par ligne : ils brisent la structure temporelle/ordonnée, pas les marginales — c'est le nul du projet depuis §8.31, pas un nul biologique.
- 10 nuls frais par paire ne font pas une distribution à 200 : ils valident la réplique, ils ne la remplacent pas.

---
## ADDENDUM — Correction de Zackary du 21 novembre 2026, 12h03 (portée : tout le projet, précisée 12h04)
**Ajouté le 21 novembre 2026, après le gel du protocole — le texte gelé
ci-dessus est intact, cet addendum l'applique.**

Trois points, à appliquer dans cette piste :

**1. Contrôle jamais analysé.** Un flux utilisé comme axe de contrôle
ne doit JAMAIS être un flux analysé. Vérification faite le 21 novembre
2026 AVANT le lancement des runs de cette piste (les 150 CSV de nuls
frais étaient construits, aucun run lancé) : les 15 paires ont toutes
le contrôle `step`, et KRAS (la variable d'ordre) est ABSENT des
colonnes de flux de chacun des 15 CSV (12 flux, 11 pour GSE57495 et
GSE194249) — vérifié par lecture des en-têtes. Les 150 nuls frais sont
des permutations de ces mêmes CSV : même propriété. La réplique
(`replica_nulls_893.py`) exclut la colonne de contrôle des flux
analysés par construction (même règle que le pipeline, ligne 6787 de
`universal_v6.2.0_cohen.py` : `c != control_col`). Le pipeline lui-même
exclut la colonne de contrôle des flux analysés quand aucun
`flux_mapping` n'est fourni (cas de tous nos runs) — vérifié par
lecture du code. **Règle respectée dans cette piste.** Le défaut connu
des 96 fichiers de rotations d'origine (§8.32 — le flux d'ordre
dupliqué en `X.1` parmi les flux analysés) ne concerne pas cette
piste ; il est traité au §8.97, partie 1.

**2. Contrôles non monotones.** Aucun seuil n'est écarté dans cette
piste au motif de non-monotonie. La monotonie aide à lire, elle n'est
pas une condition pour que le seuil compte : les seuils des contrôles
non monotones sont lus comme des résultats d'analyse à part entière.
(Ici le contrôle est `step`, monotone par construction ; la nuance
s'applique à la lecture des distributions, pas à un tri.)

**3. Analyse, pas prédiction.** Tous les verdicts de cette piste sont
formulés comme de l'analyse (« les données montrent », « on observe »),
jamais comme des prédictions. Le verdict par paire (SOLIDE / FRAGILE /
NON) décrit la position du réel dans la distribution des nuls — il ne
prédit rien sur un futur échantillon.
