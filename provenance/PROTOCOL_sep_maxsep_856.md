# PROTOCOLE GELÉ — §8.56 : « sep seul ou maxsep seul suffisent-ils comme score MC ? »

Date : 19 novembre 2026 (soir).
Statut : **PROTOCOLE GELÉ. Aucune extraction du présent chantier, aucun
calcul de verdict, aucun comptage, avant ce gel. Toute déviation arrête le
travail et se consigne, elle ne se corrige pas en silence.**
Auteur : TagPrint (chantier §8.56, coordinateur : fusion au livre blanc ensuite).
Dossier : `~/workspace/runs/pdac-v6/`.
Pipeline de travail : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant le gel ; v6.2, v6.1, v6, v6.3, v6.4 ne sont JAMAIS modifiées —
ce chantier ne construit AUCUNE nouvelle version : les deux candidats sont
des RELECTURES de champs déjà émis par v6.2).
Références : livre blanc §8.49, §8.52 (dont §8.52.6, question ouverte) ;
`PROTOCOL_v6.3_mc.md` (SHA `acc74e943d60757e90b8800a0caac178b6b38222c94d197895615d2d3a5cea0b`) ;
`PROTOCOL_v6.4_mc.md` (SHA `074b1bce34c20c5067855b3a387ec1e64d3e59c23cc6bda2c905f21e359051f6`) ;
`PROTOCOL_v6.2.md` §3 (S_sep) ; `PROTOCOL_phase2_discrimination.md`.

## 0. Verdict d'abord — ce qui est gelé ici

La question ouverte du §8.52.6, après deux recompositions rejetées (v6.3
§8.49, v6.4 §8.52) : **les termes annexes essayés jusqu'ici — `stability`,
`recur`, `conc` — coûtent plus qu'ils ne rapportent hors du contrôle
positif. Reste à trancher si la composante de séparation SEULE suffit
comme score MC.** Deux candidats, et rien d'autre :

- **Candidat S — `sep` seul** : score = `sep` du best_config ANCIEN.
- **Candidat M — `maxsep` seul** : score = `max_separation` du
  best_config ANCIEN.

Les deux sont des relectures (sélection du best_config inchangée, donc
seuil MC, cascade, S_sep, Delta, L7a inchangés par construction). Aucun
nouveau terme, aucune repondération, aucune resélection, aucune variante
de poids après avoir vu les chiffres. Ce chantier TRANCHE et PROPOSE ou
REJETTE — il n'adopte pas : la décision finale d'adoption revient à
Zackary.

**Avertissement consigné AVANT tout calcul (honnêteté de la question) :**
les diagnostics du §8.52.3/§8.52.6 ont DÉJÀ publié, à titre de
diagnostics, `sep` seul 35/48 rotations et 5/8 principales, `maxsep`
37/48 et 6/8. Ces nombres sont la MOTIVATION de ce chantier, pas son
verdict : le verdict repose sur la RE-VÉRIFICATION indépendante ci-dessous
(extracteur propre + second calcul indépendant + recoupements §5/§6).
Si la re-vérification contredit les diagnostics publiés, ce sont les
chiffres re-vérifiés qui font foi et l'écart est consigné.

## 1. Définitions exactes (lues dans le code v6.2, pas devinées)

Fichier `universal_v6.2.0_cohen.py`, fonction `evaluate_scan_quality`
(lignes 3314–3390). Par tirage, le scan de seuil donne une courbe de
scores = |d de Cohen| pré/post-seuil :

- **`maxsep`** = score maximal de la courbe (ligne 3333 :
  `max_separation = scores[max_idx]`, `scores` = |d de Cohen|).
  C'est un |d de Cohen|, sans dimension mais NON borné (plage [0, ∞[).
  Champ JSON lu :
  `run_pipeline.threshold_metadata.threshold_optimization.best_config.metrics.max_separation`.
- **`sep`** = `maxsep / (1 + maxsep)` (définition des protocoles v6.3
  §4 et v6.4 §3, reprise telle quelle ; absente du code v6.2, qui
  émet `s_norm = tanh(maxsep/2)` à la ligne 3336 — `sep` est une
  relecture, pas un champ v6.2). Plage [0, 1[. Ancrage non arbitraire :
  sep = 0,5 quand |d| = 1. **Ordre identique à maxsep** (fonction
  strictement croissante) : aucun renversement possible entre les deux
  candidats ; seule l'ÉCHELLE diffère — c'est le point central de ce
  chantier (§7).

Règles de bord, gelées : `maxsep` est un max de |d| donc ≥ 0 par
construction ; si un `maxsep` lu était < 0 ou non fini, le cas serait
consigné et exclu du comptage (jamais imputé) — aucun cas de ce type
n'est attendu (0 rencontré dans les lots v6.3/v6.4) ; `sep = 0` si
`maxsep = 0`. Les deux scores sont lus sur le best_config ANCIEN
(sélection par l'ancien composite
`0.3·s_norm + 0.3·stability + 0.2·robustness + 0.2·sharpness`,
lignes 3480–3484) : la question porte sur le SCORE AFFICHÉ, pas sur
la sélection du tirage.

**Conséquence mathématique consignée avant le calcul (elle ne décide
de rien, elle s'interprète après) :** pour une paire (R, N),
`d_sep = sep_R − sep_N = d_maxsep / ((1 + maxsep_R)·(1 + maxsep_N))`.
Le plancher 0,07 appliqué en unités `sep` équivaut donc, en unités
`maxsep`, à un plancher `0,07·(1 + maxsep_R)·(1 + maxsep_N)` — TOUJOURS
plus grand que 0,07 dès que les maxsep sont > 0. Autrement dit, le
même plancher numérique 0,07 est PLUS FACILE à franchir en unités
`maxsep` qu'en unités `sep`, d'un facteur (1+m_R)(1+m_N) qui vaut
typiquement ~1,5–2 sur le PDAC. Toute différence de verdict entre S
et M ne peut venir que de là (les ordres sont identiques, les signes
des écarts sont identiques) — la section §8.56 devra le dire, quel
que soit le verdict.

## 2. Ensembles jugés — les MÊMES 60 paires que v6.3 et v6.4

Tous lus dans les `master_results.json` v6.2 déjà sur disque, AUCUN
nouveau run pour le score :

- **V1 — 8 paires principales** (phase 2) : HP35, TCGA v4, GSE71729,
  GSE62452, ICGC, IMMUNE_TCGA, PARP_TCGA, DEPMAP.
  Dossiers `results_fast_v62_<nom>` / `results_fast_v62_<nom>_nul`
  (HP35 : `results_fast_v62_hp35[_nul]` ; GSE71729 :
  `results_fast_v62_geo71729[_nul]` ; GSE62452 :
  `results_fast_v62_geo62452[_nul]` ; ICGC :
  `results_fast_v62_icgc[_nul]` ; immunitaire :
  `results_fast_v62_immune_tcga[_nul]` ; PARP :
  `results_fast_v62_parp_tcga[_nul]` ; DepMap :
  `results_fast_v62_depmap[_nul]`).
- **V2 — 48 paires rotations sans doublon** (§8.44 : 44 du lot
  `manifest_v62_dedup_844.txt` + 4 du §8.41 : CLDN18 v6.1, CTLA4,
  ACO2, PARP1 — mêmes dossiers que `extract_ssep_844_rotations.py`,
  `extract_mc63.py` et `extract_mc64.py`). Familles : IMMROT (12),
  V4ROT (12), PARPROT (12), DEPMAPROT (12). La paire CLDN18 est lue
  dans un JSON v6.1 (`results_fast_v61_v4r_cldn18_dedup[_nul]`,
  version `v6.1.0-L7aL7b-CohenD-short` acceptée comme en §8.49/§8.52) ;
  les 47 autres en v6.2.
- **V3 — Test A** (prolifération, `results_fast_v62_prolif[_nul]`) :
  contrôle DESCRIPTIF, pas une porte (§6).
- **V4 — bras MTAP** : série PRMT5-flux
  (`results_fast_v62_prmt5flux[_nul]`, §8.43, primaire) et série MTAP
  (`results_fast_v62_mtap[_nul]`, secondaire) : contrôles DESCRIPTIFS (§6).
- **V5 — artefact pureté** (`results_fast_v62_v4r_purity[_nul]`) :
  contrôle DESCRIPTIF (§6).

Total : 8 + 48 + 1 + 2 + 1 = **60 paires, 120 runs**.

## 3. Règle de comptage (identique à v6.3/v6.4 §5, sans changement)

Comme `verdict()` de `extract_phase2.py` et §8.44 : direction = signe
de la somme des écarts réel−nul sur l'ensemble jugé ; une paire
« sépare » si |écart| > gigue_eff ET signe = direction majoritaire.
Gigue : les deux scores sont des fonctions déterministes des JSON
(gigue attendue 0, mesurée au §6 par la double extraction) ;
**gigue_eff = max(gigue mesurée, 0,07)** — le plancher 0,07 est le même
que pour S_sep (`PROTOCOL_v6.2.md` §3.4) et que pour v6.3/v6.4, et il
est appliqué **dans les unités propres de chaque candidat** (0,07 en
unités `sep` pour S ; 0,07 en unités |d| pour M). C'est la convention
du projet, appliquée littéralement aux deux candidats — l'asymétrie
d'échelle qu'elle entraîne est consignée au §1 et discutée au §7,
elle n'est pas corrigée après coup. La direction attendue est
réel > nul.

## 4. Barres A1–A4 (écrites AVANT tout calcul ; la barre ne bouge pas)

Un candidat « SUFFIT » comme score MC **si ET SEULEMENT SI** il
franchit les 4 portes. Références (ancien MC : rotations 12/48,
principales 1/8 au plancher 0,07 avec 7/8 positifs, HP35 +0,1950 ;
v6.3 : 31/48, 4/8, +0,2271 ; v6.4 : 28/48, 4/8, +0,5529) :

- **A1 — rotations (V2) : le candidat sépare ≥ 30/48** au plancher
  0,07, direction réel > nul. (Barre de la mission §8.56 — plus
  stricte que les 24/48 des protocoles v6.3/v6.4, qui exigeaient le
  double de l'ancien MC ; le comptage à 24/48 sera rapporté en
  sensibilité au §7, le verdict porte sur 30/48.)
- **A2 — principales (V1) : écart > 0,07 sur ≥ 6/8 paires, ET écart
  positif sur ≥ 7/8.** (Inchangée depuis v6.3/v6.4.)
- **A3 — HP35 (contrôle positif) : écart ≥ 0,30**, dans les unités
  du candidat. (Inchangée depuis v6.3/v6.4.)
- **A4 — rien ne casse, relecture exacte :** AUCUN nouveau code
  pipeline n'étant construit dans ce chantier (les deux scores sont
  déjà émis/calculables depuis les JSON v6.2), A4 se traduit ainsi :
  (a) la re-extraction indépendante (§5, second script, chemin de
  code distinct) reproduit `sep` et `maxsep` à **0,0 exact** sur les
  120/120 runs ; (b) les valeurs recoupées contre les tables
  `v63_mc_table.json` / `v64_mc_table.json` concordent à 1e-9 ;
  (c) l'ancien MC relu concorde sans écart avec §8.44 (rotations) et
  phase 2 v6.2 (principales) à 1e-9 (garde-fou du lecteur) ;
  (d) SHA-256 de v6.2, v6.1, v6, v6.3, v6.4 revérifiés inchangés
  après travaux.

**Si une seule porte échoue : le candidat est REJETÉ comme score MC
unique, plainement, avec les chiffres — aucune repondération, aucun
nouveau terme, aucune redéfinition du plancher après coup.** Les
portes A1–A4 sont les seules ; Test A, MTAP et pureté ne peuvent ni
sauver ni condamner un candidat, mais leurs chiffres DOIVENT être
publiés (§6).

## 5. Méthode d'extraction et de vérification (lecture seule)

1. Extracteur propre du chantier, `extract_sep_maxsep_856.py`
   (SHA noté au rapport) : lecture SEULE des 120
   `master_results.json` v6.2/v6.1 ; pour chaque run, lit
   `best_config.metrics.max_separation` et `best_config.score`
   (ancien MC, garde-fou), calcule `sep = maxsep/(1+maxsep)` ;
   sorties `sep_maxsep_856_table.csv` / `sep_maxsep_856_table.json`.
   Écrit APRÈS ce gel, jamais avant.
2. Second calcul indépendant, `verify_sep_maxsep_856.py` (SHA noté) :
   chemin de code distinct (re-lecture directe des JSON par un autre
   parcours, sans réutiliser les fonctions de l'extracteur), recalcule
   `sep` et `maxsep` pour les 120 runs et compare à la table de
   l'étape 1 : écart attendu 0,0 exact sur 120/120. Tout écart =
   résultat à diagnostiquer, pas un bruit.
3. Recoupements : `sep`/`maxsep` par paire vs `v64_mc_table.json`
   (tol. 1e-9) ; ancien MC relu vs `ssep_844_rotations.csv` (V2) et
   `v62_phase2_table.csv` (V1) (tol. 1e-9) ; versions JSON consignées
   (v6.2 attendue partout sauf CLDN18 en v6.1).
4. Aucun run du pipeline, aucune modification de code, aucun push
   GitHub, aucune modification du livre blanc dans ce chantier
   (section `section_8.56_sep_maxsep.md` séparée, fusion par le
   coordinateur).

## 6. Contrôles descriptifs (à publier, ne décident pas)

- **Test A (V3)** : écarts `sep` / `maxsep` rapportés tels quels.
  Rappel : ancien MC −0,0948 (inversé), maxsep +0,2501 (§8.34) ;
  v6.3 +0,0666 ; v6.4 +0,1456. Les deux candidats suivent maxsep par
  construction — le verdict NON du §8.34 portait sur la chaîne et sur
  MC/Delta, pas sur maxsep seul ; ni S ni M ne ressuscite Test A.
- **MTAP (V4)** : écarts rapportés tels quels. Rappel série
  PRMT5-flux : ancien MC +0,0004, maxsep −0,1036, S_sep −0,0977 ;
  v6.3 −0,0046 ; v6.4 −0,0854. Si S ou M devenait positif là où
  maxsep est négatif, ce serait impossible par construction (même
  ordre, mêmes signes) — tout écart de signe serait une erreur de
  lecture à diagnostiquer.
- **Pureté (V5)** : écart rapporté tel quel. Rappel : ancien MC
  +0,1520 contre maxsep −0,0670 ; v6.3 −0,0353 ; v6.4 −0,1197
  (artefact CORRIGÉ). S et M reprennent le sens de maxsep par
  construction.

## 7. Sensibilités descriptives (rapportées, ne décident pas)

- **S1 — sans plancher** : comptage des positifs seuls (direction
  réel > nul) sur V1 et V2, pour S et M (identiques par construction,
  les signes des écarts étant les mêmes — à vérifier, pas à supposer).
- **S2 — barre A1 à 24/48** (protocoles v6.3/v6.4) : le verdict A1
  change-t-il si la barre est l'ancienne ? Rapporté, non décisif.
- **S3 — équivalence d'échelle** : pour chaque paire, plancher
  `maxsep` équivalent au plancher `sep` :
  `0,07·(1 + maxsep_R)·(1 + maxsep_N)` ; nombre de paires M qui
  passent le plancher littéral 0,07 mais PAS le plancher équivalent —
  c'est exactement l'écart entre les comptages M et S, et il sera
  nommé paire par paire (la paire charnière attendue, d'après les
  diagnostics §8.52, est ICGC : maxsep +0,0970 contre sep +0,0525 —
  à CONFIRMER par la re-vérification, pas à recopier).
- **S4 — ventilation par famille** (IMMROT / V4ROT / PARPROT /
  DEPMAPROT) pour S et M sur V2, avec écarts moyens.

## 8. Règles du projet rappelées

- Aucun consensus exigé entre flux ou contrôles ; aucun seuil
  pré-enregistré au-delà de ceux écrits ici ; aucune affirmation
  clinique — l'étude porte sur l'instrument, pas sur le cancer.
- Verdicts seulement sur les données et runs du jour (relectures du
  19–20 nov. 2026 des JSON v6.2 existants) ; les diagnostics §8.52
  sont une motivation, pas une preuve.
- Si le résultat est négatif ou ambigu, il est dit tel quel. En
  particulier : si M franchit les barres et S échoue, le verdict
  « M suffit, S ne suffit pas » devra être accompagné de sa fragilité
  mesurée (de combien de paires, et par quel mécanisme d'échelle —
  §1/§7) ; adopter `maxsep` comme score MC reviendrait à afficher
  un |d de Cohen| brut, non borné, comme « score » — la section dira
  ce que cela implique (pas de plafond, pas de comparabilité
  inter-études sans contexte, mais aucune saturation artificielle).
- La décision finale d'adoption revient à Zackary ; ce chantier
  propose ou rejette.

## 9. Traçabilité et provenance

- Protocole : ce fichier, `PROTOCOL_sep_maxsep_856.md` (SHA noté au rapport).
- Extraction : `extract_sep_maxsep_856.py` (SHA noté), sorties
  `sep_maxsep_856_table.csv` / `sep_maxsep_856_table.json`.
- Vérification indépendante : `verify_sep_maxsep_856.py` (SHA noté),
  sortie `sep_maxsep_856_verify.json`.
- Section : `section_8.56_sep_maxsep.md` (verdict d'abord).
- Données : JSON v6.2 existants (lots §8.44, phase 2, §8.43, Test A) ;
  CSV inchangés, SHA déjà publiés dans `PROVENANCE_rotations_dedup_844.md`,
  `PROVENANCE_tcga_v4.md`, `PROVENANCE_mtap_prmt5_flux.md`,
  `PROVENANCE_testA_proliferation.md`. Nuls = lignes permutées, graine
  42 — échantillons hypothétiques, pas des mesures ; séries réelles =
  résidus d'expression / dépendance CRISPR (mesures instrumentales
  transformées). Aucune valeur inventée.

— Fin du protocole gelé §8.56. —
