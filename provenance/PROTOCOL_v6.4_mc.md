# PROTOCOLE GELÉ — v6.4 : recomposition du MC par la récurrence-concentration

Date : 19 novembre 2026.
Statut : **PROTOCOLE GELÉ. Aucun calcul du nouveau score, aucun code v6.4
écrit, aucun run lancé avant ce gel. Toute déviation arrête le travail et
se consigne, elle ne se corrige pas en silence.**
Auteur : TagPrint (chantier 3/4, coordinateur : fusion au livre blanc ensuite).
Dossier : `~/workspace/runs/pdac-v6/`.
Pipeline de travail : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout travail ; v6.2, v6.1, v6 et v6.3 ne sont JAMAIS modifiées —
la v6.4 est construite sur une COPIE de la v6.2, jamais de la v6.3 rejetée).
Références : livre blanc §8.49 ; `PROTOCOL_v6.3_mc.md` (SHA
`acc74e943d60757e90b8800a0caac178b6b38222c94d197895615d2d3a5cea0b`) ;
`PROTOCOL_v6.2.md` §3 (S_sep) ; `PROTOCOL_phase2_discrimination.md`.

## 0. Verdict d'abord — ce qui est gelé ici

Une seule proposition, en deux variantes dont UNE SEULE est candidate à
l'adoption. Elle reprend les DEUX pistes nommées au §8.49.8, qui n'avaient
jamais été calculées :

- **Variante C (primaire, candidate) — CONCENTRATION des seuils, SANS
  stability** : le meilleur tirage MC reste choisi par l'ancien composite
  (seuil, cascade, S_sep, Delta inchangés par construction) ; seul le
  SCORE affiché change, recalculé depuis les métriques du best_config
  et des 12 tirages stockés (§3). C'est la variante jugée aux critères
  d'adoption (§5).
- **Variante E (exploratoire, NON candidate) — v6.3 SANS stability,
  récurrence médiane/best conservée** : même formule que la v6.3
  renormalisée sans le terme de stabilité. Rapportée à part. Elle ne
  peut pas être adoptée dans ce chantier, quel que soit son score. Son
  rôle est l'attribution : si E sépare et C ne sépare pas, c'est la
  concentration qui échoue ; si C sépare et E ne sépare pas, c'est la
  concentration qui porte le gain ; si les deux échouent, la suppression
  de stability seule ne suffit pas non plus.

Règle du projet rappelée : aucun consensus exigé entre flux ou contrôles ;
aucun seuil pré-enregistré au-delà de ceux écrits ici ; aucune affirmation
clinique — l'étude porte sur l'instrument, pas sur le cancer. La décision
finale d'adoption revient à Zackary ; ce chantier PROPOSE ou REJETTE,
il n'adopte pas.

## 1. Rappel : l'ancien MC et la v6.3 rejetée (faits publiés, §8.49)

Ancien MC (v6.2) = score du meilleur tirage, composite
`0.3·s_norm + 0.3·stability + 0.2·robustness + 0.2·sharpness`
(`s_norm = tanh(maxsep/2)`). Défauts mesurés : robustness morte (D1),
stability saturée (D2), sharpness récompense le bruit (D3), s_norm
sature dans la plage PDAC (D4), malédiction du vainqueur (D5).

v6.3 : `MC_new = 0.60·sep + 0.25·stability + 0.15·recur`,
`sep = maxsep/(1+maxsep)`, `recur = médiane_i(maxsep_i)/maxsep_best`.
Validation 60 paires : rotations 31/48 (porte A1 franchie, ≥24/48),
principales 4/8 (porte A2 ≥6/8 EN ÉCHEC), HP35 +0,2271 (porte A3 ≥0,30
EN ÉCHEC), code 10/10 (porte A4 franchie). **REJETÉE (§8.49).**
Cause identifiée (§8.49.6) : la récurrence médiane/best punit le vrai
pic — HP35 recur réel 0,453 contre nul 0,876 ; sur les 8 paires
principales, recur moyen réel 0,717 contre nul 0,820 (le nul est en
moyenne PLUS récurrent que le réel) ; terme de récurrence sur HP35 :
0,15×(0,453 − 0,876) = −0,063 ; terme de stabilité sur HP35 :
0,25×(0,869 − 0,983) = −0,029 (le réel HP35 est moins stable que son
nul, D2). Les deux termes annexes coûtent ensemble −0,092 sur l'écart
HP35, soit plus du tiers de la barre A3.

## 2. Les deux pistes du §8.49.8, et pourquoi elles sont testées ensemble dans C

**Piste 1 — récurrence par concentration des seuils.** La récurrence
médiane/best mesure si les AUTRES tirages montent aussi haut que le
meilleur : elle punit un pic vrai mais isolé en hauteur. La concentration
des seuils mesure autre chose : si les tirages, quel que soit leur
maxsep, placent leur rupture AU MÊME ENDROIT. Une vraie rupture a une
position ; un pic de chance n'en a pas — ses tirages dispersent leurs
seuils sur toute la plage. La concentration ne punit donc pas le pic
isolé en hauteur : elle récompense l'accord sur la position.

**Piste 2 — suppression de stability.** D2 est mesuré, pas supposé :
stability est quasi constante sur le PDAC (0,978–0,997) et
anti-discriminante sur HP35 (réel 0,869 < nul 0,983). Un terme qui ne
varie pas ne sépare pas ; un terme qui varie à l'envers coûte −0,029
sur HP35. S_sep montre déjà que la stabilité ne porte rien sur le PDAC
(§8.49.8). La supprimer ne peut pas coûter de séparation mesurée —
c'est ce que la variante E vérifie isolément.

**Pourquoi les deux dans la candidate C :** l'adoption porte sur une
FORMULE, pas sur chaque piste séparément. Si C passe les quatre portes,
la formule est adoptée telle quelle ; l'attribution (quelle piste a
porté le gain) est donnée par la comparaison C vs E vs v6.3, rapportée
mais non décisive. Si C échoue, E dit si la suppression de stability
seule aurait suffi — et la piste « concentration » est alors fermée
comme définie ici, sans retouche.

## 3. Définition exacte du MC recomposé v6.4 (variante C, primaire)

Formule gelée, UNE SEULE (aucune variante de poids après avoir vu les
résultats) :

```
MC2    = 0.70 · sep + 0.30 · conc
sep    = max_separation / (1 + max_separation)     (best_config ANCIEN)
conc   = 1 − médiane_i(|θ_i − θ*|) / (θ_max − θ_min)
```

où `max_separation` est celui du best_config ANCIEN (sélection
inchangée) ; `θ_i` parcourt les seuils des `n_success` tirages de
`all_results` (12 en mode fast, champ `threshold` de chaque tirage,
vérifié présent sur HP35/TCGA v4 v6.2 avant le gel) ; `θ*` est le
seuil du best_config (l'un des tirages) ; `θ_max`, `θ_min` sont le max
et le min des `θ_i`. Règles de bord, gelées : si `all_results` est
absent ou vide, ou si moins de 2 seuils lisibles, `conc = 0` et le cas
est consigné, jamais imputé ; si `θ_max = θ_min` (tous les seuils
identiques), `conc = 1,0` ; `conc` est bornée à [0, 1] par construction
(la médiane des écarts ne dépasse jamais l'étendue). Plage :
MC2 ∈ [0, 1].

**Justification de chaque terme (principe, pas ajustement) :**

- `sep = maxsep/(1+maxsep)` : reprise de la v6.3 (ancrage non arbitraire
  sep = 0,5 quand |d de Cohen| = 1 ; sature moins que tanh(·/2) dans la
  plage PDAC ; ordre identique à max_separation, aucun renversement
  possible).
- `conc` (NOUVEAU, sans paramètre) : écart médian des seuils à θ*,
  normalisé par l'étendue des seuils. Sans paramètre : pas de tolérance
  en %, pas de largeur idéale, pas de bin — la médiane et l'étendue
  sont les seuls résumés utilisés, et la normalisation rend `conc`
  sans dimension et comparable entre runs (les seuils sont en unités
  du flux de contrôle, arbitraires d'un run à l'autre). `conc → 1`
  quand tous les tirages placent leur seuil au même endroit que le
  gagnant ; `conc → 0` quand les seuils se dispersent sur toute la
  plage. La médiane (pas la moyenne) rend `conc` insensible à un ou
  deux tirages aberrants.
- **Poids 0,70 / 0,30, fixés par principe** : la séparation domine
  (c'est le signal) ; la part 0,25 de stability supprimée est
  réallouée +0,10 à `sep` (dominance renforcée) et +0,15 à `conc`
  (le terme sous test reçoit un poids réel — avec 0,15, un écart de
  concentration de 0,5 ne déplacerait MC2 que de 0,075, tout juste le
  plancher ; avec 0,30, le même écart pèse 0,15 et peut décider A3).
  Aucun poids n'a été choisi après lecture d'un chiffre de MC2 : les
  poids sont écrits ici avant tout calcul.
- **Termes SUPPRIMÉS** : `robustness` (D1) et `sharpness` (D3) comme
  en v6.3 ; `stability` (D2, piste 2) ; `recur` médiane/best (cause
  d'échec de la v6.3, §8.49.6).
- **Ce qui ne change PAS (variante C)** : la sélection du best_config
  (ancien composite), donc le seuil MC, la cascade T_-2…T_+2, S_sep,
  Delta, L7a, L5/L4. MC2 est une RELECTURE du même best_config,
  comme S_sep en v6.2 et MC_new en v6.3.

## 4. Variante E (exploratoire, non candidate) et diagnostics — définitions gelées

```
MC_E = 0.80 · sep + 0.20 · recur          (v6.3 renormalisée sans stability)
recur = médiane_i(maxsep_i) / maxsep_best (définition v6.3, §3 du protocole v6.3)
```

Renormalisation par principe : 0,60/0,75 = 0,80 ; 0,15/0,75 = 0,20 —
les rapports sep:recur de la v6.3 sont conservés, la part de stability
est redistribuée proportionnellement. **Non candidate à l'adoption
dans ce chantier** : elle garde le terme `recur` dont le §8.49.6 a
montré qu'il punit le vrai pic ; son seul rôle est l'attribution (§0).

**Diagnostics descriptifs (rapportés, ne décident pas) :**

- `sep` seul (poids 1,00) : plafond de la composante séparation —
  dit si un échec de C vient de `sep` elle-même ou de `conc`.
- `MC_new` v6.3 recalculé depuis les mêmes JSON (formule §3 du
  protocole v6.3) et vérifié égal aux valeurs de `v63_mc_table.json`
  (tol. 1e-9) : garde-fou de régression du lecteur, pas un nouveau
  résultat.
- `conc` réel/nul par paire, et `recur` réel/nul : publiés tels quels
  pour lire quelle composante porte ou coûte la séparation.

## 5. Critères d'adoption (écrits AVANT tout calcul de MC2)

Identiques au §5 du protocole v6.3, sans changement de seuil — la barre
ne bouge pas parce que la formule change. Règle de comptage (comme
`verdict()` de `extract_phase2.py` et §8.44) : direction = signe de la
somme des écarts réel−nul sur l'ensemble jugé ; une paire « sépare »
si |écart| > gigue_eff ET signe = direction majoritaire. Gigue : MC2
est une fonction déterministe des JSON (gigue attendue 0, mesurée au
§7 sur les re-runs v6.4) ; **gigue_eff = max(gigue mesurée, 0,07)** —
le plancher 0,07 est le même que pour S_sep (`PROTOCOL_v6.2.md` §3.4)
et que pour la v6.3. La direction attendue est réel > nul.

**Ensembles jugés (tous lus dans les `master_results.json` v6.2 déjà sur
disque, AUCUN nouveau run pour le score) — les MÊMES 60 paires que la
v6.3 :**

- **V1 — 8 paires principales** (phase 2) : HP35, TCGA v4, GSE71729,
  GSE62452, ICGC, immunitaire TCGA, PARP TCGA, DepMap.
- **V2 — 48 paires rotations sans doublon** (§8.44 : 44 du lot
  `manifest_v62_dedup_844.txt` + 4 du §8.41 : CLDN18 v6.1, CTLA4, ACO2,
  PARP1 — mêmes dossiers que `extract_ssep_844_rotations.py` et
  `extract_mc63.py`).
- **V3 — Test A** (prolifération, `results_fast_v62_prolif[_nul]`) :
  contrôle DESCRIPTIF, pas une porte d'adoption (§6).
- **V4 — bras MTAP** : série PRMT5-flux (`results_fast_v62_prmt5flux
  [_nul]`, §8.43, primaire) et série MTAP (`results_fast_v62_mtap
  [_nul]`, secondaire) : contrôles DESCRIPTIFS (§6).
- **V5 — artefact pureté** (`results_fast_v62_v4r_purity[_nul]`) :
  contrôle DESCRIPTIF (§6).

**Proposition d'adoption (variante C) si ET SEULEMENT SI les 4 portes
sont franchies :**

- **A1 — rotations (V2) : MC2 sépare ≥ 24/48** au plancher 0,07,
  direction réel > nul. Référence ancien MC : 12/48 ; v6.3 : 31/48.
  Le seuil 24/48 est le DOUBLE de l'ancien — inchangé depuis la v6.3.
- **A2 — principales (V1) : écart > 0,07 sur ≥ 6/8 paires, et écart
  positif sur ≥ 7/8.** Référence ancien MC : 1/8 au plancher 0,07,
  7/8 positifs ; v6.3 : 4/8, 7/8 positifs.
- **A3 — HP35 (contrôle positif) : écart MC2 ≥ 0,30.** Référence
  ancien MC : +0,1950 ; v6.3 : +0,2271.
- **A4 — rien ne casse : sur le sous-ensemble re-lancé en v6.4 (§7),
  best_config (seuil, score ancien, métriques), cascade T_-2…T_+2 et
  S_sep sont IDENTIQUES aux JSON v6.2 (tolérance 0, numérique exact
  après parsing JSON) ; MC2 calculé en code = MC2 hors-ligne
  (tolérance 1e-9) ; v6.2 SHA inchangé.**

**Si une seule porte échoue : la proposition est REJETÉE, plainement,
avec les chiffres — aucune repondération, aucun nouveau terme, aucune
redéfinition après coup.** Les portes A1–A4 sont les seules ; Test A,
MTAP et pureté ne peuvent ni sauver ni condamner la proposition, mais
leurs chiffres DOIVENT être publiés (§6). La variante E ne peut pas
sauver C : si C échoue et E passe les portes, le verdict reste REJETÉ
pour C, avec E consignée comme piste pour un chantier ultérieur (elle
garde le terme `recur` condamné au §8.49.6, elle ne peut pas être
adoptée sans un protocole propre).

## 6. Contrôles descriptifs (à publier, ne décident pas de l'adoption)

- **Test A (V3)** : d_MC2 rapporté tel quel. Rappel ancien : MC
  −0,0948 (inversé), maxsep +0,2501 ; v6.3 MC_new +0,0666. Si MC2
  suit maxsep (positif), c'est cohérent avec sa construction (sep
  dominante) — le verdict NON du §8.34 portait sur la chaîne et sur
  MC/Delta, pas sur maxsep seul ; MC2 ne ressuscite pas Test A.
- **MTAP (V4)** : d_MC2 rapporté tel quel. Rappel ancien : série
  PRMT5-flux MC +0,0004 (égalité), maxsep −0,1036, S_sep −0,0977 ;
  v6.3 MC_new −0,0046. Si MC2 devient positif là où maxsep est
  négatif, c'est une anomalie à nommer (la concentration aurait
  renversé la séparation) ; si MC2 reste ≈ 0 ou négatif, c'est
  cohérent avec le verdict NON du §8.43.
- **Pureté (V5)** : d_MC2 rapporté tel quel. Rappel ancien : MC
  +0,1520 contre maxsep −0,0670 ; v6.3 MC_new −0,0353 (artefact
  CORRIGÉ). Si MC2 redevient positif (sens inverse de maxsep),
  l'artefact SURVIT à la recomposition et c'est dit ; s'il reste
  négatif, la correction tient.

## 7. Construction de la v6.4 et validation en code (après le §5 hors-ligne)

### 7.1 Construction (copie de la v6.2 seulement, script miroir de `build_v6.3.py`)

Fichier de départ : copie exacte de la v6.2 →
`~/workspace/runs/biophysique-hp35/universal_v6.4.0_cohen.py`.
JAMAIS une copie de la v6.3 (rejetée). Changements autorisés, et RIEN
d'autre :

- **C1 — version** : `VERSION_MASTER = "v6.4.0-L7aL7b-CohenD-short"` +
  note d'en-tête v6.4 (seul changement : ajout du score MC v6.4 en
  lecture ; sélection inchangée).
- **C2 — fonction pure** `mc_v64_score(best_metrics, all_thresholds,
  best_threshold)` implémentant EXACTEMENT la formule du §3 (mêmes
  constantes 0,70 / 0,30, même `sep`, même médiane des écarts, mêmes
  règles de bord), appelée APRÈS la sélection du best_config, sans
  jamais écrire dans `best_config.score`, `threshold` ou la cascade.
  Champs écrits sous le nom `mc_v64` (distinct de `mc_recomposed` de
  la v6.3, pour ne jamais confondre les deux scores).
- **C3 — écriture** : `best_config["mc_v64"]` (valeur + formule +
  poids + `conc` + `sep`) et `threshold_optimization["mc_v64"]`
  (même contenu), + une ligne de log `MC v6.4 : …`.

Vérifications de construction (assertions du script, arrêt si échec) :

- SHA-256 de la v6.2 source = `f07567c4…c3abf` (complet noté) avant
  toute copie ; SHA-256 de la v6.2, de la v6.1, de la v6 et de la v6.3
  revérifiés inchangés après travaux.
- `diff` v6.2 → v6.4 : seules les lignes C1–C3 diffèrent (le script
  liste chaque bloc différant ; tout autre diff = arrêt) ; exactement
  3 blocs différants.
- `python3 -m py_compile universal_v6.4.0_cohen.py` : exit 0.

### 7.2 Runs v6.4 (sous-ensemble, mode fast, graine 42)

Dix runs, dossiers NEUFS `results_fast_v64_*` (jamais écraser les
`results_fast_v62_*` ni les `results_fast_v63_*`), commande
`python3 universal_v6.4.0_cohen.py --input <csv> --mode fast --output
<dossier>`, lancés en arrière-plan persistant (`systemd-run`, leçon
AGENTS.md 2026-11-17 : un `nohup` meurt avec la session), journal
`runs_v64_mc.log` (commandes, exit codes, SHA v6.2/v6.4) :

| # | Paire | Entrée | Sortie |
|---|---|---|---|
| 1–2 | HP35 réel/nul | `~/workspace/runs/biophysique-hp35/test_biophysique_input[_nul].csv` | `results_fast_v64_hp35[_nul]` |
| 3–4 | TCGA v4 réel/nul | `pdac_tcga_fluxes_v4[_nul].csv` | `results_fast_v64_tcga_v4[_nul]` |
| 5–6 | Rotation CEACAM5 réel/nul (cas fort, §8.44) | CSV dédoublonnés §8.44 | `results_fast_v64_v4rot_ceacam5_dedup[_nul]` |
| 7–8 | Rotation GSTM1 réel/nul (cas négatif, §8.44) | CSV dédoublonnés §8.44 | `results_fast_v64_v4rot_gstm1_dedup[_nul]` |
| 9–10 | Test A réel/nul | `pdac_tcga_fluxes_v4_prolif[_nul].csv` | `results_fast_v64_prolif[_nul]` |

Choix CEACAM5 / GSTM1 gelé ici : un cas fort et un cas négatif, pour
que l'équivalence code ↔ hors-ligne soit testée aux deux extrêmes —
c'est un choix de VÉRIFICATION DU CODE, pas du verdict (le verdict
utilise les 48 paires hors-ligne). Mêmes entrées que la v6.3 (§7.2 du
protocole v6.3).

Critères (§5 A4 + gigue) : 10/10 exit 0 ; MC2 en code = hors-ligne
(tol. 1e-9) sur 10/10 ; best_config/cascade/S_sep identiques à v6.2
(tol. 0) sur 10/10 ; gigue MC2 mesurée = max |MC2(v6.4) −
MC2(v6.2 hors-ligne)| = 0 attendu (mêmes entrées, code déterministe
en v6.2) ; tout écart = résultat à diagnostiquer, pas un bruit.

## 8. Ce que ce protocole ne fera pas

- Aucune modification de v6.2, v6.1, v6, v6.3 (copie séparée de la v6.2
  seulement).
- Aucune repondération, aucun nouveau terme, aucune variante de plus
  après avoir vu les chiffres de MC2 (les deux variantes C et E sont
  les seules, gelées ici ; `sep` seul et `MC_new` v6.3 sont des
  diagnostics, pas des candidates).
- Aucun nouveau run du pipeline pour le SCORE : la validation V1–V5
  est une lecture des JSON v6.2 existants ; seuls les 10 runs du §7.2
  servent à valider le CODE v6.4.
- Aucun push GitHub, aucune modification du livre blanc dans ce
  chantier (section §8.52 séparée, fusion par le coordinateur).
- Aucune affirmation clinique : l'étude porte sur l'instrument.
- Aucun consensus exigé entre flux ou contrôles ; aucune sélection
  d'indicateur après coup.

## 9. Traçabilité et provenance

- Protocole : ce fichier, `PROTOCOL_v6.4_mc.md` (SHA noté au rapport).
- Extraction hors-ligne : `extract_mc64.py` (SHA noté), sorties
  `v64_mc_table.csv` / `v64_mc_table.json` (+ `.md` de lecture).
- Construction : `build_v6.4.py` (SHA noté), SHA-256 v6.2 source,
  v6.4 construite, v6.1/v6/v6.3 revérifiées.
- Validation code : `runs_v64_mc.log`, manifeste `manifest_v64_mc.txt`,
  vérification `extract_v64_check.py` → `v64_mc_check.json`.
- Section : `section_8.52_mc_recurrence.md` (verdict d'abord).
- Données : CSV inchangés depuis §8.44 / phase 2 / §8.43 / Test A
  (SHA déjà publiés dans `PROVENANCE_rotations_dedup_844.md`,
  `PROVENANCE_tcga_v4.md`, `PROVENANCE_mtap_prmt5_flux.md`,
  `PROVENANCE_testA_proliferation.md`) ; nuls = lignes permutées,
  graine 42 — échantillons hypothétiques, pas des mesures ; séries
  réelles = résidus d'expression / dépendance CRISPR (mesures
  instrumentales transformées). Aucune valeur inventée.

— Fin du protocole gelé v6.4. —
