# PROTOCOLE GELÉ — §8.72 : Consolider §8.70 avec PLUS DE NULS FRAIS sur GSE79668

Date : 20 novembre 2026, ~15h45 EST. Chantier §8.72, piste 2 de la
mission parent du 20 nov. 2026 (« consolider §8.70 avec plus de nuls
frais sur GSE79668 »). Ce protocole est gelé AVANT toute construction
et tout run. Aucun nul frais n'est construit sans ce fichier. Aucun
paramètre ne change après les résultats. Le livre blanc N'EST PAS
édité, le PDF N'EST PAS régénéré, rien n'est poussé sur GitHub dans
ce chantier (convention des chantiers ; fusion par le coordinateur).
La section §8.72 est écrite dans un FICHIER SÉPARÉ
(`section_8.72_nulls_gse79668.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié ; v6.1
`2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`).

## 0. Contexte décisionnel — à lire avant tout le reste

- §8.70 (GSE79668, Kirby et coll. Mol Oncol 2016, GPL11154,
  51 tumeurs) : **PARTIEL, C3 non levée**. `d_maxsep = +0,0567`
  (réel 0,4104 contre nul graine 42 0,3538), sous le plancher
  0,07. Les 2 nuls frais passent le plancher (+0,0890 et
  +0,1538). Verdict fragile : 3 nuls seulement, et leur écart
  entre eux (0,0972) est plus grand que l'écart mesuré (0,0567).
  Le nul graine 42 est le plus haut des trois.
- **Ce chantier ne rejoue pas la paire.** Il ne change JAMAIS le
  verdict de la paire graine 42 (PARTIEL) — règle gelée §8.70 §7 :
  « le verdict de la paire graine 42 n'est JAMAIS changé par les
  nuls frais ». Ce qu'il juge, c'est la LECTURE « sous le
  plancher » : tient-elle contre la DISTRIBUTION des nuls, ou
  était-elle un artefact du tirage graine 42 ?
- L'adoption pleine de `maxsep`, décidée par Zackary le 20 nov.
  2026 à 13h04, n'est ni rouverte ni conditionnée par ce
  chantier. Si le verdict est RENVERSE (§4), la correction porte
  sur la lecture du §8.70, pas sur l'adoption.
- Précédent de méthode : §8.50 / §8.53 (PROTOCOL_nulls_n70_853.md)
  — 10 nuls frais pour consolider un arbitrage ; ~200 nuls pour
  un plancher stable à petit n. Ici, 10 nuls frais de plus, soit
  13 nuls au total : une distribution, pas un plancher stable —
  c'est nommé comme limite (§6).

## 1. Faits de départ (relus du §8.70 — lecture seule, jamais recalculés ici)

- CSV réel : `pdac_870_geo79668_fluxes.csv` (51 lignes), SHA-256
  `7744bc5a82fe80055b5ab9231fc7ae5395354f643b5b7cd1fdfce8aa6656107a`
  — le MÊME CSV que §8.70, réutilisé tel quel, jamais reconstruit
  à la main. Le builder le réécrit à chaque invocation
  (déterministe) : son SHA doit rester `7744bc5a…6107a` après
  chaque construction (§2) — tout changement = arrêt et
  diagnostic.
- Réel `maxsep` : **0,41044843843771645** (`extract_870.json`,
  vérifié 4/4 à 0,0 exact par `verify_870.py`). Aucun nouveau
  run réel : le run réel §8.70
  (`results_fast_v62_870_geo79668`) est relu, pas relancé.
- Les 3 nuls déjà mesurés (`extract_870.json`, mêmes vérifications) :

| Nul | `maxsep` nul | `d_maxsep` (réel − nul) | > 0,07 ? |
|---|---|---|---|
| Graine 42 (paire gelée) | 0,3537953187066359 | **+0,05665311973108055** | non |
| Graine 8701 | 0,3214731637696184 | **+0,08897527466809805** | oui |
| Graine 8702 | 0,2566001863019332 | **+0,15384825213178325** | oui |

- Distribution des 3 écarts : min +0,0567, médiane +0,0890,
  max +0,1538. Étendue des 3 nuls : 0,3538 − 0,2566 = **0,0972**.
- Construction des nuls (rappel §8.70 §4.3) : bloc des flux
  permuté par lignes, `rng(graine)`, contrôle (KRAS, ordre)
  intact, colonne `step` intacte. Le nul est un échantillon
  hypothétique, pas une mesure.

## 2. Nuls frais : 10, graines 8721–8730, gelées ici avant tout run

- Graines : **8721, 8722, 8723, 8724, 8725, 8726, 8727, 8728,
  8729, 8730** — dix graines, jamais utilisées dans ce projet.
  Vérifié par grep AVANT le gel (20 nov. 2026) : aucun fichier
  `pdac_870_geo79668_fluxes_nul_s872*`, aucun
  `results_fast_v62_872_*`, aucune occurrence de `nul_s872*`,
  `_s872[0-9]`, `--nul-seed 872*` dans les `.py` / `.md` /
  `.txt` / `.sh` / `.log` de `~/workspace/runs/pdac-v6/`.
  Les occurrences nues « 8721 »…« 8730 » dans des fichiers de
  données (`data/ng3398_MOESM60_ESM.txt`, rapports
  `universal_master_report.txt`) sont des coïncidences
  numériques, pas des graines — vérifié par lecture du contexte,
  comme pour « 79668 » au §8.70.
- Construction : script neuf `build_nulls_872.py`, qui invoque
  `build_fluxes_870.py --nul-seed <graine>` (original intact)
  pour chaque graine, vérifie après chaque invocation que le CSV
  réel garde son SHA `7744bc5a…6107a`, et consigne les SHA des
  10 CSV de nuls dans `nulls_872_files.json`. Aucune autre
  méthode, aucun autre paramètre.
- Sorties : `pdac_870_geo79668_fluxes_nul_s8721.csv` …
  `pdac_870_geo79668_fluxes_nul_s8730.csv` (51 lignes chacun).
- Aucun run n'est lancé avant que les 10 CSV existent avec
  leurs SHA consignés.

## 3. Runs v6.2 (mode fast) — 10 runs, aucun run réel

- Lot : 10 runs — les 10 nuls frais uniquement. Manifeste
  `manifest_v62_872.txt` (format `NOM|ENTREE|SORTIE`, même
  convention que `manifest_v62_870.txt`), lanceur reprenable
  existant `run_v62_lot.sh` (saute les sorties déjà complètes),
  journal `runs_v62_872.log` (SHA du pipeline en tête, exits
  consignés).
- Dossiers : `results_fast_v62_872_geo79668_nul_s8721` …
  `..._s8730`.
- Lancement en `systemd-run --unit=v62-872 --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance
  `watch_v62_872.sh` (modèle `watch_v62_870.sh`, TOTAL=10,
  s'arrête d'elle-même à 10/10). Ne JAMAIS supprimer le dossier
  d'un run en cours. Si la machine redémarre, reprise sans perte
  (SKIP des dossiers complets, jamais de relance à l'aveugle).
- SHA du pipeline revérifié avant ET après le lot. Exits 0
  exigés sur les 10 runs ; tout exit non nul = diagnostic,
  pas de saut silencieux.

## 4. Distribution et critère de verdict — GELÉS avant tout run

### 4.1 Distributions

- **Distribution primaire : les 13 nuls** — les 3 anciens
  (graines 42, 8701, 8702, valeurs §1 relues) + les 10 frais.
  Les 3 anciens sont inclus parce que ce sont des tirages du
  même nul, par la même méthode, sur le même CSV réel : les
  exclure jetterait des mesures. La distribution primaire est
  celle qui fait le verdict.
- **Distribution secondaire (contrôle) : les 10 frais seuls.**
  Médiane, p95 et étendue rapportés aussi sur les 10 frais.
  Si |médiane fraîche − médiane totale| > 0,03, le dire
  plainement dans la section : les 3 anciens tireraient alors
  la distribution.
- Mesures rapportées sur chaque distribution : médiane, p95
  (`numpy.percentile`, interpolation linéaire — méthode nommée),
  min, max, étendue (max − min), IQR, écart-type ; rang du réel
  parmi les 14 valeurs (13 nuls + réel) ; nombre de nuls battus
  par le réel ; fraction des 13 écarts `d_i = m_R − nul_i`
  supérieurs au plancher 0,07 ; `d` contre p95 (`m_R − p95`).

### 4.2 Grandeur de verdict

- `m_R` = 0,41044843843771645 (réel, §1 — relu du run §8.70,
  re-vérifié par relecture dans `extract_872.py`, §5).
- `M` = médiane des `maxsep` des 13 nuls.
- **`d_médian` = `m_R` − `M`.** C'est l'écart du réel contre le
  nul TYPIQUE (médian), pas contre un tirage unique. La
  médiane des écarts vaut `d_médian` par construction (le réel
  est constant).

### 4.3 Catégories de verdict (trois, mutuellement exclusives)

- **CONSOLIDÉ** : `d_médian < 0,05` — le « sous le plancher »
  tient contre le nul médian, AVEC marge : le plancher 0,07
  est manqué de plus de 0,02. Le PARTIEL du §8.70 est consolidé :
  la paire est sous le plancher non par tirage, mais contre le
  nul typique. Aucune note de correction au §8.70.
- **RENVERSE** : `d_médian > 0,09` — le réel PASSE le plancher
  contre le nul médian, AVEC marge. La lecture « sous le
  plancher » du §8.70 était un artefact du tirage graine 42
  (le plus haut des nuls). Le verdict de la paire graine 42
  reste PARTIEL (règle gelée §8.70 §7 — l'histoire n'est pas
  réécrite), mais la section §8.72 le dit plainement et une
  NOTE DATÉE DE CORRECTION est ajoutée en addendum au fichier
  `section_8.70_gse79668.md` (texte original intact, addendum
  daté du 20 nov. 2026, signé §8.72). L'A2 étendu gelé (6/10,
  paires graine 42) n'est PAS recompté : le renversement est
  une correction de lecture, pas un recomptage.
- **INCONCLUSIF** : `0,05 ≤ d_médian ≤ 0,09` — la médiane est
  trop proche du plancher pour trancher. Bande ±0,02 autour du
  plancher : l'erreur-type de la médiane de 13 nuls à n = 51
  est de l'ordre de 0,015–0,02 (cf. §8.53 : ~200 nuls pour un
  plancher stable à petit n ; 13 nuls ne stabilisent pas la
  médiane à mieux que ~±0,02) — un écart médian dans la bande
  ne permet pas de dire si « sous le plancher » tient ou non.
  Aucune note de correction au §8.70 ; la fragilité du §8.70
  reste entière, désormais chiffrée sur 13 nuls.

### 4.4 Ce qui ne change pas le verdict

- Le rang du réel, `d` contre p95, la fraction des écarts
  > 0,07, MC, Delta, L7a, les cascades : descriptifs, publiés,
  ne décident pas. Le critère gelé est `d_médian` seul.
- Si le réel est battu par ≥ 1 nul (rang < 14/14), c'est dit
  dans la section quelle que soit la catégorie — un réel battu
  par un nul n'est pas un réel qui sépare.
- Aucune repondération, aucune redéfinition du plancher, aucun
  nouveau terme après avoir vu les chiffres.

## 5. Extraction et vérification

1. Extracteur propre du chantier, `extract_872.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_870.py`) ; lit les 10 `master_results.json`
   neufs ET relit les 4 anciens (réel + 3 nuls) — 14 entrées ;
   sorties `extract_872.json` / `extract_872.csv` ; calcule la
   distribution (§4.1) et `d_médian` (§4.2) depuis les valeurs
   extraites, jamais recopiées à la main. Vérifie que le
   `maxsep` réel relu égale 0,41044843843771645 à 0,0 exact et
   que les 3 nuls anciens relus égalent leurs valeurs §1 à 0,0
   exact — tout écart = diagnostic, pas un bruit.
2. Second calcul indépendant : relecture directe des 14
   `master_results.json` par un chemin distinct (script
   `verify_872.py`, SHA noté, modèle `verify_870.py`) —
   `maxsep`, ancien MC et `stability` recoupés à 0,0 exact ;
   sortie `maxsep_872_verify.json`, verdict OK si et seulement
   si 14/14 comparaisons et écart max 0,0.
3. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 6. Limites connues d'avance

- 13 nuls ne font pas un plancher stable : §8.53 estime ~200
  nuls pour un plancher stable à petit n. La médiane de 13
  nuls porte ~±0,02 — d'où la bande d'inconclusivité du §4.3.
  Ce chantier consolide ou renverse une LECTURE, il ne mesure
  pas un plancher.
- Le nul est une permutation par lignes (corrélations
  inter-flux préservées) : la distribution mesurée est celle
  du nul du projet, pas d'un nul à corrélations brisées
  (même réserve qu'au §8.53 §8).
- À n = 51, la distribution des nuls est large (étendue 0,0972
  sur 3 tirages) : 10 tirages de plus ne la resserrent pas,
  ils la décrivent mieux.
- Rien de clinique : l'étude porte sur l'instrument.

## 7. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et
  le jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict : seuls les écarts mesurés sur les runs du présent
  chantier font le verdict ; les §8.50/§8.53 sont cités comme
  méthode, pas comme résultats.
- Un nul qui invalide une piste est un résultat ; un échec de la
  paire est un verdict, pas un échec caché.
- Ne jamais présenter une lecture préliminaire comme un verdict.
- Aucun consensus exigé entre flux ou contrôles ; aucune
  affirmation clinique — l'étude porte sur l'instrument.

## 8. Livrables

- Ce protocole (gelé avant construction et runs ; SHA noté
  dans la section).
- `build_nulls_872.py` + `nulls_872_files.json` (SHA des 10 CSV
  de nuls + SHA du CSV réel re-vérifié).
- `manifest_v62_872.txt`, `runs_v62_872.log`,
  `watch_v62_872.sh` (+ `watch_v62_872.log`), dossiers
  `results_fast_v62_872_*` (10 runs, exits 0).
- `extract_872.json` / `extract_872.csv`, `verify_872.py` +
  `maxsep_872_verify.json` (14/14 à 0,0 exact).
- §8.72 dans le FICHIER SÉPARÉ
  `section_8.72_nulls_gse79668.md` (verdict d'abord, en une
  phrase : CONSOLIDÉ, RENVERSE ou INCONCLUSIF ; chiffres
  ensuite ; détail complet après ; provenance nommée partout).
- Le cas échéant (RENVERSE seulement) : addendum daté en fin de
  `section_8.70_gse79668.md`, texte original intact.
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur
  GitHub.

— Fin du protocole gelé §8.72. —
