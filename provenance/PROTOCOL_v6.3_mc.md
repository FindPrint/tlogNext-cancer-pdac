# PROTOCOLE GELÉ — v6.3 : recomposition du score MC

Date : 19 novembre 2026.
Statut : **PROTOCOLE GELÉ. Aucun calcul du nouveau score, aucun code v6.3
écrit, aucun run lancé avant ce gel. Toute déviation arrête le travail et
se consigne, elle ne se corrige pas en silence.**
Auteur : TagPrint (chantier 4/4, coordinateur : fusion au livre blanc ensuite).
Dossier : `~/workspace/runs/pdac-v6/`.
Pipeline de travail : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout travail ; v6.2, v6.1 et v6 ne sont JAMAIS modifiées —
la v6.3 est construite sur une COPIE).
Références : livre blanc §8.31, §8.34, §8.37–§8.38, §8.43–§8.44 ;
`PROTOCOL_v6.2.md` §3 (S_sep) ; `PROTOCOL_phase2_discrimination.md`.

## 0. Verdict d'abord — ce qui est gelé ici

Une seule proposition, en deux variantes dont UNE SEULE est candidate à
l'adoption :

- **Variante R (primaire, candidate) — RESCORE sans toucher à la
  sélection** : le meilleur tirage MC reste choisi par l'ancien composite
  (seuil, cascade, S_sep, Delta inchangés par construction) ; seul le
  SCORE affiché change, recalculé depuis les métriques du best_config
  et des 12 tirages stockés (§3). C'est la variante jugée aux critères
  d'adoption (§5).
- **Variante S (exploratoire, NON candidate) — RESÉLECTION** : le meilleur
  tirage est choisi par le nouveau composite (§4). Rapportée à part, avec
  le déplacement de seuil et de cascade qu'elle entraîne. Elle ne peut
  pas être adoptée dans ce chantier, quel que soit son score.

Règle du projet rappelée : aucun consensus exigé entre flux ou contrôles ;
aucun seuil pré-enregistré au-delà de ceux écrits ici ; aucune affirmation
clinique — l'étude porte sur l'instrument, pas sur le cancer. La décision
finale d'adoption revient à Zackary ; ce chantier PROPOSE ou REJETTE,
il n'adopte pas.

## 1. Définition exacte de l'ancien MC (lue dans le code v6.2, pas devinée)

Fichier `universal_v6.2.0_cohen.py`. Mode `fast` : `optimization_iterations
= 12` (ligne 243) — 12 tirages MC, pas 100 (100 est le défaut de la
fonction, ligne 3704 ; le mode fast le remplace).

**Par tirage** (`_monte_carlo_worker`, lignes 3453–3490) : un scan de seuil
donne une courbe de scores = |d de Cohen| pré/post-seuil ; `evaluate_scan_quality`
(lignes 3314–3390) en tire 5 métriques :

- `max_separation` = score maximal de la courbe (ligne ~3330).
- `s_norm = tanh(max_separation / 2.0)` (ligne 3336).
- `stability = 1 / (1 + écart-type des scores locaux)` sur une fenêtre de
  `max(3, len(scores) // 20)` points autour du pic (ligne 3344).
- `robustness = exp(-((FWHM - 10)²) / (2 × 5²))`, FWHM = largeur à
  mi-hauteur en % de la plage des candidats, idéal 10 % (lignes 3346–3364).
- `sharpness = tanh(max |dS/dx| local / 0.5)` (lignes 3365–3381).

**Score composite du tirage** (lignes 3480–3484, poids lignes 3727–3731,
défauts `mode_cfg.get(..., 0.3 / 0.3 / 0.2 / 0.2)`) :

```
score_tirage = 0.3·s_norm + 0.3·stability + 0.2·robustness + 0.2·sharpness
```

avec pénalité ×0,8 si `w_size < n_pts // 10` (lignes 3486–3488).

**MC (ancien) = score du meilleur tirage** = `best_config.score`
(`run_pipeline.threshold_metadata.threshold_optimization.best_config.score`).
Le seuil MC (`best_config.threshold`) et la cascade T_0 en découlent.
Les 12 tirages sont conservés dans le JSON : `threshold_optimization.
all_results[i].{score, threshold, metrics.{max_separation, s_norm,
stability, robustness, sharpness}}` (vérifié sur HP35 et TCGA v4 v6.2 :
12 entrées, `n_iterations = 12`).

## 2. Défauts mesurés de l'ancien MC (faits déjà publiés, pas devinés)

- **D1 — robustness morte.** `PROTOCOL_v6.2.md` §3.2, mesuré sur 16 JSON
  v6.1 : robustness ≤ 2×10⁻⁷ sur 14/16 (TCGA v4 : 3,37×10⁻⁴¹ ;
  GSE71729 : 6,66×10⁻³⁵ ; PARP : 3,37×10⁻⁴¹), contre 0,984 / 0,899 sur
  HP35 réel/nul. La FWHM des scans PDAC est très loin de l'idéal
  arbitraire de 10 % : le poids 0,2 est perdu sur tout le PDAC, et sur
  HP35 il récompense un accident de forme.
- **D2 — stability saturée.** Sur les 8 paires principales v6.2 :
  stability 0,978–0,997 sur le PDAC (quasi constante), 0,869 / 0,983 sur
  HP35 (le réel y est MOINS stable que le nul). Le terme 0,3·stability
  ajoute ≈ 0,29–0,30 à chaque score, réel comme nul : il dilue le signal
  de séparation au lieu de le porter.
- **D3 — sharpness récompense le bruit.** Une pointe d'un seul point a
  elle aussi une dérivée locale maximale. Direction incohérente en
  phase 2 : le nul est plus « sharp » que le réel sur GSE71729, sur
  l'immunitaire TCGA et sur PARP TCGA.
- **D4 — s_norm sature là où vit le PDAC.** tanh(maxsep/2) : maxsep 0,15
  → 0,075 ; 0,46 → 0,226 ; 1,77 → 0,709. Les écarts PDAC (maxsep réel
  0,26–0,53 contre nul 0,14–0,31) sont comprimés à ~0,14 en s_norm, puis
  à ~0,04 après le poids 0,3.
- **D5 — sélection par le maximum (malédiction du vainqueur).** Le MC
  prend le MAX sur 12 tirages d'un composite bruité ; un nul peut lui
  aussi tirer un maximum élevé. Les 12 tirages contiennent pourtant
  l'information de RÉCURRENCE (le pic revient-il quand w_size / min_grp
  changent ?) — elle n'est jamais utilisée.

**Conséquences mesurées (rappels, à ne pas re-mesurer comme « nouveau ») :**

- Rotations sans doublon, 48 paires (§8.44, `ssep_844_rotations.csv`) :
  ancien MC sépare 12/48 au plancher 0,07 (35/48 positifs, écart moyen
  +0,0152, médiane +0,0219) ; max_separation sépare 37/48 ; S_sep 37/48.
- Paires principales v6.2 (`v62_phase2_table.csv`) : ancien MC 7/8
  positifs avec gigue 0 (écarts PDAC +0,0059 à +0,0545), 1/8 au plancher
  0,07 (HP35 seul, +0,1950) ; GSE62452 inversé (−0,0031).
- Test A (§8.34) : MC réel 0,3638 contre nul 0,4587 (écart −0,0948,
  inversé) alors que max_separation est réel 0,3943 contre nul 0,1442
  (écart +0,2501).
- Série MTAP-PRMT5 (§8.43) : MC réel 0,3390 contre nul 0,3386 (écart
  +0,0004, égalité) ; S_sep et max_separation meilleurs au nul.
- Artefact pureté (§8.31, paire V4R_PURITY, `v62_phase2_table.csv`) :
  ancien MC réel 0,4841 contre nul 0,3321 (écart +0,1520, le MC
  « sépare ») alors que max_separation est réel 0,1444 contre nul
  0,2114 (écart −0,0670, inversé) : les termes annexes du composite
  renversent la séparation elle-même. C'est l'artefact nommé par la
  mission (« écart de pureté +0,16, séparation réelle 0,144 vs nul
  0,211 », arrondis de la mission).
- HP35, contrôle positif (v6, mission) : MC réel 1,772… non — précision :
  en v6 le MC HP35 cité par la mission est « 1,772 vs 0,121 » ; ce sont
  les valeurs de max_separation, pas du MC best_score (v6.2 : MC
  0,6035 contre 0,4086, écart +0,1950 ; max_separation 1,7718 contre
  0,1206). La mission confond les deux colonnes ; le présent protocole
  retient les valeurs v6.2 lues dans `v62_phase2_table.csv` et le dit.

## 3. Définition exacte du MC recomposé proposé (variante R, primaire)

Formule gelée, UNE SEULE (aucune variante de poids après avoir vu les
résultats) :

```
MC_new = 0.60 · sep + 0.25 · stability + 0.15 · recur
sep    = max_separation / (1 + max_separation)
recur  = médiane_i(max_separation_i) / max_separation_best
```

où `max_separation`, `stability` sont ceux du best_config ANCIEN
(sélection inchangée), et `max_separation_i` parcourt les
`n_success` tirages de `all_results` (12 en mode fast). Règles de bord,
gelées : si `max_separation_best = 0`, `recur = 0` ; `recur` est
borné à [0, 1] (écrêtage) ; si `all_results` est absent ou vide,
`recur = 0` et le cas est consigné, jamais imputé.

**Justification de chaque terme (principe, pas ajustement) :**

- `sep = maxsep/(1+maxsep)` : fonction croissante bornée [0, 1), d'ordre
  identique à max_separation (aucun renversement possible), avec point
  d'ancrage non arbitraire : sep = 0,5 exactement quand |d de Cohen| = 1
  (effet « large » conventionnel). Elle sature MOINS que tanh(·/2) dans
  la plage PDAC : maxsep 0,17 → 0,145 (tanh : 0,085) ; 0,46 → 0,315
  (tanh : 0,226) ; 1,77 → 0,639 (tanh : 0,709).
- `stability` gardée, poids réduit 0,3 → 0,25 : c'est le seul garde-fou
  contre le pic bruité déjà présent ; elle ne peut plus dominer, et son
  rôle à la sélection (déjà exercé par l'ancien composite) est conservé.
- `recur` (NOUVEAU, sans paramètre) : rapport médiane/best des
  max_separation sur les 12 tirages. C'est la récurrence que le terme
  « robustesse » prétendait mesurer : une vraie rupture revient quand
  les paramètres de scan changent (médiane proche du best, recur → 1) ;
  un pic de chance est isolé à un tirage (médiane ≪ best, recur → 0).
  Aucun seuil 0,5, aucune largeur idéale, aucune dérivée : la médiane
  est le seul résumé utilisé.
- **Poids 0,60 / 0,25 / 0,15, fixés par principe** : la séparation
  domine (c'est le signal) ; la stabilité garde un rôle de garde-fou
  minoritaire ; la récurrence, terme NOUVEAU et non prouvé, est
  volontairement minoritaire (0,15) : même si recur ne discrimine pas,
  elle ne peut pas renverser à elle seule un écart de séparation.
- **Termes SUPPRIMÉS** : `robustness` (D1, morte sur PDAC, idéal 10 %
  arbitraire) et `sharpness` (D3, récompense le bruit) — suppression
  motivée par les mesures D1/D3, pas par un ajustement aux rotations.
- **Ce qui ne change PAS (variante R)** : la sélection du best_config
  (ancien composite), donc le seuil MC, la cascade T_-2…T_+2, S_sep,
  Delta, L7a, L5/L4. MC_new est une RELECTURE du même best_config,
  comme S_sep l'était en v6.2. Plage : MC_new ∈ [0, 1].

## 4. Variante S (exploratoire, non candidate) — définition gelée

Sélection du tirage par le nouveau composite SANS le terme de récurrence
(la récurrence dépend du tirage sélectionné : elle ne peut pas servir à
sélectionner) :

```
score_S(i) = 0.60 · maxsep_i/(1+maxsep_i) + 0.25 · stability_i
MC_new_S   = 0.60 · sep_sel + 0.25 · stability_sel + 0.15 · recur_sel
recur_sel  = médiane_i(maxsep_i) / maxsep_sel
```

où `sel` est le tirage maximisant `score_S(i)` (premier en cas d'égalité,
comme l'ancien code). Rapportée par paire : MC_new_S réel/nul, écart,
seuil sélectionné, déplacement de T_0 vs v6.2. **Non candidate à
l'adoption dans ce chantier** : elle change le seuil et la cascade, et
son évaluation complète exigerait de re-valider les cascades sur tout
le lot — hors périmètre. Si elle sépare nettement mieux, c'est une
PISTE pour un chantier v6.4, pas un verdict d'adoption ici.

## 5. Critères d'adoption (écrits AVANT tout calcul de MC_new)

Règle de comptage (comme `verdict()` de `extract_phase2.py` et §8.44) :
direction = signe de la somme des écarts réel−nul sur l'ensemble jugé ;
une paire « sépare » si |écart| > gigue_eff ET signe = direction
majoritaire. Gigue : MC_new est une fonction déterministe des JSON
(gigue attendue 0, mesurée au §7 sur les re-runs v6.3) ; **gigue_eff =
max(gigue mesurée, 0,07)** — le plancher 0,07 est le même que pour S_sep
(`PROTOCOL_v6.2.md` §3.4) : sans lui, « écart > 0 » rendrait le critère
trivial. La direction attendue est réel > nul.

**Ensembles jugés (tous lus dans les `master_results.json` v6.2 déjà sur
disque, AUCUN nouveau run pour le score) :**

- **V1 — 8 paires principales** (phase 2) : HP35, TCGA v4, GSE71729,
  GSE62452, ICGC, immunitaire TCGA, PARP TCGA, DepMap.
- **V2 — 48 paires rotations sans doublon** (§8.44 : 44 du lot
  `manifest_v62_dedup_844.txt` + 4 du §8.41 : CLDN18 v6.1, CTLA4, ACO2,
  PARP1 — mêmes dossiers que `extract_ssep_844_rotations.py`).
- **V3 — Test A** (prolifération, `results_fast_v62_prolif[_nul]`) :
  contrôle DESCRIPTIF, pas une porte d'adoption (§6).
- **V4 — bras MTAP** : série PRMT5-flux (`results_fast_v62_prmt5flux
  [_nul]`, §8.43, primaire) et série MTAP (`results_fast_v62_mtap
  [_nul]`, secondaire) : contrôles DESCRIPTIFS (§6).
- **V5 — artefact pureté** (`results_fast_v62_v4r_purity[_nul]`) :
  contrôle DESCRIPTIF (§6).

**Proposition d'adoption (variante R) si ET SEULEMENT SI les 4 portes
sont franchies :**

- **A1 — rotations (V2) : MC_new sépare ≥ 24/48** au plancher 0,07,
  direction réel > nul. Référence ancien MC : 12/48. Le seuil 24/48
  est le DOUBLE de l'ancien — « nettement mieux » au sens de la
  mission, écrit d'avance, pas ajusté après lecture.
- **A2 — principales (V1) : écart > 0,07 sur ≥ 6/8 paires, et écart
  positif sur ≥ 7/8.** Référence ancien MC : 1/8 au plancher 0,07,
  7/8 positifs avec gigue 0.
- **A3 — HP35 (contrôle positif) : écart MC_new ≥ 0,30.** Référence
  ancien MC : +0,1950. Le positif doit rester largement au-dessus du
  plancher, pas seulement le passer.
- **A4 — rien ne casse : sur le sous-ensemble re-lancé en v6.3 (§7),
  best_config (seuil, score ancien, métriques), cascade T_-2…T_+2 et
  S_sep sont IDENTIQUES aux JSON v6.2 (tolérance 0, numérique exact
  après parsing JSON) ; MC_new calculé en code = MC_new hors-ligne
  (tolérance 1e-9) ; v6.2 SHA inchangé.**

**Si une seule porte échoue : la proposition est REJETÉE, plainement,
avec les chiffres — aucune repondération, aucun nouveau terme, aucune
redéfinition après coup.** Les portes A1–A4 sont les seules ; Test A,
MTAP et pureté ne peuvent ni sauver ni condamner la proposition, mais
leurs chiffres DOIVENT être publiés (§6).

## 6. Contrôles descriptifs (à publier, ne décident pas de l'adoption)

- **Test A (V3)** : d_MCnew rapporté tel quel. Rappel ancien : MC
  −0,0948 (inversé), maxsep +0,2501. Si MC_new suit maxsep (positif),
  c'est cohérent avec sa construction (sep dominante) et c'est dit —
  le verdict NON du §8.34 portait sur la chaîne et sur MC/Delta, pas
  sur maxsep seul ; MC_new ne ressuscite pas Test A.
- **MTAP (V4)** : d_MCnew rapporté tel quel. Rappel ancien : série
  PRMT5-flux MC +0,0004 (égalité), maxsep −0,1036, S_sep −0,0977.
  Si MC_new devient positif là où maxsep est négatif, c'est une
  anomalie à nommer (la récurrence ou la stabilité aurait renversé la
  séparation) ; si MC_new reste ≈ 0 ou négatif, c'est cohérent avec le
  verdict NON du §8.43.
- **Pureté (V5)** : d_MCnew rapporté tel quel. Rappel ancien : MC
  +0,1520 contre maxsep −0,0670. Si MC_new redevient négatif (sens de
  maxsep), l'artefact est CORRIGÉ sur cette paire ; s'il reste positif,
  l'artefact SURVIT à la recomposition et c'est dit.

## 7. Construction de la v6.3 et validation en code (après le §5 hors-ligne)

### 7.1 Construction (copie seulement, script miroir de `build_v6.1.py`)

Fichier de départ : copie exacte de la v6.2 →
`~/workspace/runs/biophysique-hp35/universal_v6.3.0_cohen.py`.
Changements autorisés, et RIEN d'autre :

- **C1 — version** (ligne 9212) : `VERSION_MASTER =
  "v6.3.0-L7aL7b-CohenD-short"` + note d'en-tête v6.3 (seul changement :
  ajout du score MC recomposé en lecture ; sélection inchangée).
- **C2 — fonction pure** `mc_recomposed_score(best_metrics,
  all_maxseps)` implémentant EXACTEMENT la formule du §3 (même
  constantes 0.60 / 0.25 / 0.15, même `sep`, même médiane, mêmes
  règles de bord), appelée APRÈS la sélection du best_config, sans
  jamais écrire dans `best_config.score`, `threshold` ou la cascade.
- **C3 — écriture** : `best_config["mc_recomposed"]` (valeur +
  formule + poids + `recur` + `sep`) et
  `threshold_optimization["mc_recomposed"]` (même contenu), + une
  ligne de log `MC recomposé : …`.

Vérifications de construction (assertions du script, arrêt si échec) :

- SHA-256 de la v6.2 source = `f07567c4…c3abf` (complet noté) avant
  toute copie ; SHA-256 de la v6.2 et de la v6.1 revérifiés inchangés
  après travaux.
- `diff` v6.2 → v6.3 : seules les lignes C1–C3 diffèrent (le script
  liste chaque bloc différant ; tout autre diff = arrêt).
- `python3 -m py_compile universal_v6.3.0_cohen.py` : exit 0.

### 7.2 Runs v6.3 (sous-ensemble, mode fast, graine 42)

Dix runs, dossiers NEUFS `results_fast_v63_*` (jamais écraser les
`results_fast_v62_*`), commande `python3 universal_v6.3.0_cohen.py
--input <csv> --mode fast --output <dossier>`, lancés en arrière-plan
persistant (`systemd-run`, leçon AGENTS.md 2026-11-17 : un `nohup`
meurt avec la session), journal `runs_v63_mc.log` (commandes, exit
codes, SHA v6.2/v6.3) :

| # | Paire | Entrée | Sortie |
|---|---|---|---|
| 1–2 | HP35 réel/nul | `~/workspace/runs/biophysique-hp35/test_biophysique_input[_nul].csv` | `results_fast_v63_hp35[_nul]` |
| 3–4 | TCGA v4 réel/nul | `pdac_tcga_fluxes_v4[_nul].csv` | `results_fast_v63_tcga_v4[_nul]` |
| 5–6 | Rotation CEACAM5 réel/nul (cas fort, §8.44) | CSV dédoublonnés §8.44 | `results_fast_v63_v4rot_ceacam5_dedup[_nul]` |
| 7–8 | Rotation GSTM1 réel/nul (cas négatif, §8.44) | CSV dédoublonnés §8.44 | `results_fast_v63_v4rot_gstm1_dedup[_nul]` |
| 9–10 | Test A réel/nul | `pdac_tcga_fluxes_v4_prolif[_nul].csv` | `results_fast_v63_prolif[_nul]` |

Choix CEACAM5 / GSTM1 gelé ici : un cas fort et un cas négatif, pour
que l'équivalence code ↔ hors-ligne soit testée aux deux extrêmes —
c'est un choix de VÉRIFICATION DU CODE, pas du verdict (le verdict
utilise les 48 paires hors-ligne).

Critères (§5 A4 + gigue) : 10/10 exit 0 ; MC_new en code = hors-ligne
(tol. 1e-9) sur 10/10 ; best_config/cascade/S_sep identiques à v6.2
(tol. 0) sur 10/10 ; gigue MC_new mesurée = max |MC_new(v6.3) −
MC_new(v6.2 hors-ligne)| = 0 attendu (mêmes entrées, code déterministe
en v6.2) ; tout écart = résultat à diagnostiquer, pas un bruit.

## 8. Ce que ce protocole ne fera pas

- Aucune modification de v6.2, v6.1, v6 (copie séparée seulement).
- Aucune repondération, aucun nouveau terme, aucune variante de plus
  après avoir vu les chiffres de MC_new (les deux variantes R et S
  sont les seules, gelées ici).
- Aucun nouveau run du pipeline pour le SCORE : la validation V1–V5
  est une lecture des JSON v6.2 existants ; seuls les 10 runs du §7.2
  servent à valider le CODE v6.3.
- Aucun push GitHub, aucune modification du livre blanc dans ce
  chantier (section §8.49 séparée, fusion par le coordinateur).
- Aucune affirmation clinique : l'étude porte sur l'instrument.
- Aucun consensus exigé entre flux ou contrôles ; aucune sélection
  d'indicateur après coup.

## 9. Traçabilité et provenance

- Protocole : ce fichier, `PROTOCOL_v6.3_mc.md` (SHA noté au rapport).
- Extraction hors-ligne : `extract_mc63.py` (SHA noté), sorties
  `v63_mc_table.csv` / `v63_mc_table.json` (+ `.md` de lecture).
- Construction : `build_v6.3.py` (SHA noté), SHA-256 v6.2 source,
  v6.3 construite, v6.1/v6 revérifiées.
- Validation code : `runs_v63_mc.log`, manifeste `manifest_v63_mc.txt`.
- Section : `section_8.49_mc_recomposition.md` (verdict d'abord).
- Données : CSV inchangés depuis §8.44 / phase 2 / §8.43 / Test A
  (SHA déjà publiés dans `PROVENANCE_rotations_dedup_844.md`,
  `PROVENANCE_tcga_v4.md`, `PROVENANCE_mtap_prmt5_flux.md`,
  `PROVENANCE_testA_proliferation.md`) ; nuls = lignes permutées,
  graine 42 — échantillons hypothétiques, pas des mesures ; séries
  réelles = résidus d'expression / dépendance CRISPR (mesures
  instrumentales transformées). Aucune valeur inventée.

— Fin du protocole gelé v6.3. —
