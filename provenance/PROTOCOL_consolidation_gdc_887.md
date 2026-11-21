# PROTOCOLE GELÉ — §8.87 : Consolider §8.85 avec PLUS DE NULS FRAIS sur GDC ORGANOID-PANCREATIC (MUCL3 ex-DPCR1)

Date : 21 novembre 2026, ~10h09 EST (15h09 UTC). Chantier §8.87,
piste 1 du lot du 21 nov. 2026 (go de Zackary, 21 nov. 2026 10h07).
Ce protocole est gelé AVANT toute construction et tout run. Aucun
nul frais n'est construit sans ce fichier. Aucun paramètre ne change
après les résultats. Le livre blanc N'EST PAS édité, le PDF N'EST PAS
régénéré, rien n'est poussé sur GitHub dans ce chantier (convention
des chantiers ; fusion par le coordinateur). La section §8.87 est
écrite dans un FICHIER SÉPARÉ
(`section_8.87_consolidation_gdc.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié ; v6.1
`2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`).
Chemin : `/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`.

## 0. Contexte décisionnel — à lire avant tout le reste

- §8.85 (GDC ORGANOID-PANCREATIC, n = 44 organoïdes tumoraux,
  12 flux dont MUCL3 ex-DPCR1) : **CONFIRME, FRAGILE ET NON
  CONSOLIDÉ**. `d_maxsep = +0,0884` (réel 0,2542 contre nul
  graine 42 0,1658), au-dessus du plancher 0,07 — avec une marge
  de 0,0184 seulement. Les 2 nuls frais courus selon la règle
  gelée ne confirment pas le passage ensemble : +0,0376 (s8851,
  sous le plancher) et +0,0936 (s8852). Écarts min / médiane /
  max sur 3 nuls : +0,0376 / +0,0884 / +0,0936 — 2 sur 3
  au-dessus du plancher. A2 : 10/14, 12/14 positifs, LOO 9/13.
  C3 du §8.59.8 RESTE LEVÉE.
- **Ce chantier ne rejoue pas la paire.** Il ne change JAMAIS le
  verdict de la paire graine 42 (CONFIRME) — règle gelée §8.85
  §7 : « le verdict de la paire graine 42 n'est JAMAIS changé
  par les nuls frais ». Ce qu'il juge, c'est la LECTURE
  « fragile, non consolidé » : tient-elle contre la
  DISTRIBUTION des nuls, ou était-elle un artefact du tirage
  s8851 (le plus haut des trois nuls mesurés, 0,2166) ?
- L'adoption pleine de `maxsep`, décidée par Zackary le 20 nov.
  2026 à 13h04, n'est ni rouverte ni conditionnée par ce
  chantier. Si le verdict est CONSOLIDÉ (§4), la correction
  porte sur la lecture du §8.85, pas sur l'adoption.
- Précédent de méthode : §8.72 (PROTOCOL_nulls_gse79668_872.md)
  — 10 nuls frais pour consolider une lecture fragile ; le
  verdict fragile y avait été RENVERSE par la distribution
  (d_médian +0,1447, rang 14/14, 12/13 écarts au-dessus du
  plancher). Ici, 10 nuls frais de plus, soit 13 nuls au total :
  une distribution, pas un plancher stable — c'est nommé comme
  limite (§6). Le présent protocole est le miroir du protocole
  §8.72, avec les catégories renommées pour le sens de la
  consolidation (§4.3) : au §8.72 la lecture à renverser était
  « sous le plancher » (PARTIEL) ; ici la lecture à confirmer
  ou à renverser est « fragile, non consolidé » (CONFIRME
  fragile).

## 1. Faits de départ (relus du §8.85 — lecture seule, jamais recalculés ici)

- CSV réel : `pdac_885_gdc_organoid_fluxes.csv` (44 lignes +
  en-tête ; en-tête
  `step,PGC,REG4,CLDN18,MUC17,MUCL3,CR2,KRT20,MUC2,GSTM1,CEACAM5,CLCA1,MUC16`),
  SHA-256
  `a83b98175bdbc33525ba8a175aa898504d2cc44125b891d0902c6c6c26345eaf`
  — le MÊME CSV que §8.85, réutilisé tel quel, jamais reconstruit.
  Le script de construction le relit sans le réécrire : son SHA
  doit rester `a83b9817…45eaf` avant et après chaque construction
  (§2) — tout changement = arrêt et diagnostic.
- Réel `maxsep` : **0,2542142849980612** (`extract_885.json`,
  vérifié 4/4 à 0,0 exact par `verify_885.py`). Aucun nouveau
  run réel : le run réel §8.85
  (`results_fast_v62_885_gdc_organoid`) est relu, pas relancé.
- Les 3 nuls déjà mesurés (`extract_885.json`, mêmes
  vérifications) :

| Nul | `maxsep` nul | `d_maxsep` (réel − nul) | > 0,07 ? |
|---|---|---|---|
| Graine 42 (paire gelée) | 0,1657676706638558 | **+0,08844661433420540** | oui |
| Graine 8851 (frais) | 0,2165939226122164 | **+0,03762036238584480** | non |
| Graine 8852 (frais) | 0,1605986015484797 | **+0,09361568344958150** | oui |

- Distribution des 3 écarts : min +0,0376, médiane +0,0884,
  max +0,0936. Étendue des 3 nuls : 0,2166 − 0,1606 = **0,0560**
  — plus grande que la marge de la paire (+0,0184).
- Construction des nuls (rappel §8.85 §5.4/§5.5) : bloc des flux
  permuté par lignes, `rng(graine)`, contrôle (KRAS, ordre)
  intact, colonne `step` intacte. Le nul est un échantillon
  hypothétique, pas une mesure.

## 2. Nuls frais : 10, graines 8871–8880, gelées ici avant tout run

- Graines : **8871, 8872, 8873, 8874, 8875, 8876, 8877, 8878,
  8879, 8880** — dix graines, jamais utilisées dans ce projet.
  Vérifié AVANT le gel (21 nov. 2026 ~10h08 EST) : aucun fichier
  `pdac_885_gdc_organoid_fluxes_nul_s887*` ni `*_s888*`, aucune
  occurrence de `nul_s88[78]`, `s88[78][0-9]`, `nul-seed 88[78]`
  ou `graine 88[78]` dans les `.py` / `.md` / `.txt` / `.sh` /
  `.json` de `~/workspace/runs/pdac-v6/` ; les deux occurrences
  nues « 8871 » du livre blanc sont des chiffres à l'intérieur
  d'une valeur `maxsep` (0,46234232096887146, TCGA v4), pas des
  graines — vérifié par lecture du contexte. Les graines
  8721–8730 (§8.72) et 8851/8852 (§8.85) sont distinctes de
  celles-ci et ne sont pas réutilisées.
- Construction : script neuf `build_nulls_887.py`, qui permute
  le bloc des flux du CSV réel (même méthode que §8.85 §5.4 :
  `rng(graine)`, permutation des lignes du bloc des flux,
  colonne `step` intacte) pour chaque graine, sans réécrire le
  CSV réel, et vérifie après chaque graine que le CSV réel
  garde son SHA `a83b9817…45eaf` ; il consigne les SHA des 10
  CSV de nuls dans `nulls_887_files.json`. Le constructeur
  `build_fluxes_885.py` (original intact) n'accepte pas de
  graine arbitraire (il ne construit que 8851/8852 avec
  `--fresh`) : il n'est PAS modifié et PAS invoqué ici — la
  permutation directe du CSV réel est la même méthode, sur la
  même entrée, et le CSV réel est vérifié inchangé graine par
  graine. Aucune autre méthode, aucun autre paramètre.
- Sorties : `pdac_885_gdc_organoid_fluxes_nul_s8871.csv` …
  `pdac_885_gdc_organoid_fluxes_nul_s8880.csv` (44 lignes +
  en-tête chacun, même en-tête que le réel).
- Aucun run n'est lancé avant que les 10 CSV existent avec
  leurs SHA consignés.

## 3. Runs v6.2 (mode fast) — 10 runs, aucun run réel

- Lot : 10 runs — les 10 nuls frais uniquement. Manifeste
  `manifest_v62_887.txt` (format `NOM|ENTREE|SORTIE`, même
  convention que `manifest_v62_872.txt`), lanceur reprenable
  existant `run_v62_lot.sh` (saute les sorties déjà complètes),
  journal `runs_v62_887.log` (SHA du pipeline en tête, exits
  consignés).
- Dossiers : `results_fast_v62_887_gdc_organoid_nul_s8871` …
  `..._s8880`.
- Lancement en `systemd-run --unit=v62-887 --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance
  `watch_v62_887.sh` (modèle `watch_v62_872.sh`, TOTAL=10,
  s'arrête d'elle-même à 10/10). Ne JAMAIS supprimer le dossier
  d'un run en cours. Si la machine redémarre, reprise sans perte
  (SKIP des dossiers complets, jamais de relance à l'aveugle).
- SHA du pipeline revérifié avant ET après le lot. Exits 0
  exigés sur les 10 runs ; tout exit non nul = diagnostic,
  pas de saut silencieux.

## 4. Distribution et critère de verdict — GELÉS avant tout run

### 4.1 Distributions

- **Distribution primaire : les 13 nuls** — les 3 anciens
  (graines 42, 8851, 8852, valeurs §1 relues) + les 10 frais.
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

- `m_R` = 0,2542142849980612 (réel, §1 — relu du run §8.85,
  re-vérifié par relecture dans `extract_887.py`, §5).
- `M` = médiane des `maxsep` des 13 nuls.
- **`d_médian` = `m_R` − `M`.** C'est l'écart du réel contre le
  nul TYPIQUE (médian), pas contre un tirage unique. La
  médiane des écarts vaut `d_médian` par construction (le réel
  est constant).

### 4.3 Catégories de verdict (trois, mutuellement exclusives)

La bande d'inconclusivité est la même qu'au §8.72 : ±0,02
autour du plancher 0,07 — l'erreur-type de la médiane de 13
nuls à n = 44 est de l'ordre de 0,015–0,02 (cf. §8.53 : ~200
nuls pour un plancher stable à petit n ; 13 nuls ne stabilisent
pas la médiane à mieux que ~±0,02).

- **CONSOLIDÉ** : `d_médian > 0,09` — le réel PASSE le plancher
  contre le nul médian, AVEC marge. La lecture « fragile, non
  consolidé » du §8.85 est renversée : le passage tenait au
  tirage s8851 (le plus haut des nuls). Le verdict de la paire
  graine 42 reste CONFIRME (règle gelée §8.85 §7 — l'histoire
  n'est pas réécrite), mais la section §8.87 le dit plainement
  et une NOTE DATÉE DE CONSOLIDATION est ajoutée en addendum au
  fichier `section_8.85_gdc_mucl3.md` (texte original intact,
  addendum daté du 21 nov. 2026, signé §8.87). L'A2 étendu gelé
  (10/14, paires graine 42) n'est PAS recompté : la
  consolidation est une correction de lecture, pas un
  recomptage.
- **FRAGILE CONFIRMÉ** : `d_médian < 0,05` — le passage ne tient
  pas contre le nul médian. La lecture « fragile, non
  consolidé » du §8.85 est confirmée : la paire est fragile non
  par tirage, mais contre le nul typique. Aucune note de
  correction au §8.85 ; le verdict de la paire graine 42 reste
  CONFIRME (règle gelée) et l'A2 gelé reste 10/14.
- **INCONCLUSIF** : `0,05 ≤ d_médian ≤ 0,09` — la médiane est
  trop proche du plancher pour trancher. Aucune note de
  correction au §8.85 ; la fragilité du §8.85 reste entière,
  désormais chiffrée sur 13 nuls.

### 4.4 Ce qui ne change pas le verdict

- Le rang du réel, `d` contre p95, la fraction des écarts
  > 0,07, MC, Delta, L7a, les cascades : descriptifs, publiés,
  ne décident pas. Le critère gelé est `d_médian` seul.
- Si le réel est battu par ≥ 1 nul (rang < 14/14), c'est dit
  dans la section quelle que soit la catégorie — un réel battu
  par un nul n'est pas un réel qui sépare.
- Aucune repondération, aucune redéfinition du plancher, aucun
  nouveau terme après avoir vu les chiffres.
- C3 reste LEVÉE dans tous les cas — elle l'était déjà depuis
  le §8.71 ; ce chantier est une consolidation supplémentaire,
  pas une condition.

## 5. Extraction et vérification

1. Extracteur propre du chantier, `extract_887.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_872.py`) ; lit les 10 `master_results.json`
   neufs ET relit les 4 anciens (réel + nuls graines 42, 8851,
   8852) — 14 entrées ; sorties `extract_887.json` /
   `extract_887.csv` ; calcule la distribution (§4.1) et
   `d_médian` (§4.2) depuis les valeurs extraites, jamais
   recopiées à la main. Vérifie que le `maxsep` réel relu égale
   0,2542142849980612 à 0,0 exact et que les 3 nuls anciens
   relus égalent leurs valeurs §1 à 0,0 exact — tout écart =
   diagnostic, pas un bruit.
2. Second calcul indépendant : relecture directe des 14
   `master_results.json` par un chemin distinct (script
   `verify_887.py`, SHA noté, modèle `verify_872.py`) —
   `maxsep`, ancien MC et `stability` recoupés à 0,0 exact ;
   sortie `maxsep_887_verify.json`, verdict OK si et seulement
   si 14/14 comparaisons et écart max 0,0.
3. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 6. Limites connues d'avance

- 13 nuls ne font pas un plancher stable : §8.53 estime ~200
  nuls pour un plancher stable à petit n. La médiane de 13
  nuls porte ~±0,02 — d'où la bande d'inconclusivité du §4.3.
  Ce chantier consolide ou confirme une LECTURE, il ne mesure
  pas un plancher.
- Le nul est une permutation par lignes (corrélations
  inter-flux préservées) : la distribution mesurée est celle
  du nul du projet, pas d'un nul à corrélations brisées
  (même réserve qu'au §8.53 §8).
- À n = 44, la distribution des nuls est large (étendue 0,0560
  sur 3 tirages, plus grande que la marge de la paire +0,0184) :
  10 tirages de plus ne la resserrent pas, ils la décrivent
  mieux.
- Rien de clinique : l'étude porte sur l'instrument.

## 7. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et
  le jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict : seuls les écarts mesurés sur les runs du présent
  chantier font le verdict ; les §8.72/§8.85 sont cités comme
  méthode et comme faits de départ, pas comme résultats.
- Un nul qui invalide une piste est un résultat ; un échec de la
  paire est un verdict, pas un échec caché.
- Ne jamais présenter une lecture préliminaire comme un verdict.
- Aucun consensus exigé entre flux ou contrôles ; aucune
  affirmation clinique — l'étude porte sur l'instrument.

## 8. Livrables

- Ce protocole (gelé avant construction et runs ; SHA noté
  dans la section).
- `build_nulls_887.py` + `nulls_887_files.json` (SHA des 10 CSV
  de nuls + SHA du CSV réel re-vérifié).
- `manifest_v62_887.txt`, `runs_v62_887.log`,
  `watch_v62_887.sh` (+ `watch_v62_887.log`), dossiers
  `results_fast_v62_887_*` (10 runs, exits 0).
- `extract_887.json` / `extract_887.csv`, `dist_887.json`,
  `verify_887.py` + `maxsep_887_verify.json` (14/14 à 0,0 exact).
- §8.87 dans le FICHIER SÉPARÉ
  `section_8.87_consolidation_gdc.md` (verdict d'abord, en une
  phrase : CONSOLIDÉ, FRAGILE CONFIRMÉ ou INCONCLUSIF ; chiffres
  ensuite ; détail complet après ; provenance nommée partout).
- Le cas échéant (CONSOLIDÉ seulement) : addendum daté en fin de
  `section_8.85_gdc_mucl3.md`, texte original intact.
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur
  GitHub.

— Fin du protocole gelé §8.87. —
