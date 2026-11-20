# PROTOCOLE GELÉ — §8.64 : adoption de `maxsep`, dossier de décision

Date : 20 novembre 2026.
Statut : **PROTOCOLE GELÉ. Aucune extraction du présent chantier, aucun
calcul de verdict, aucun comptage, avant ce gel. Toute déviation arrête le
travail et se consigne, elle ne se corrige pas en silence.**
Auteur : TagPrint (chantier §8.64, coordinateur : fusion au livre blanc ensuite).
Dossier : `~/workspace/runs/pdac-v6/`.
Pipeline de travail : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant le gel ; v6.2, v6.1, v6, v6.3, v6.4 ne sont JAMAIS modifiées —
ce chantier ne construit AUCUNE nouvelle version, ne crée PAS de v6.5 :
l'adoption, si elle est recommandée, est une décision d'AFFICHAGE sur la
v6.2 existante, et la décision finale revient à Zackary après lecture de
la section §8.64).
Références : livre blanc §8.59 (`section_8.59_maxsep_adoption.md`, SHA-256
`9951d22c1e3de415914f5ed9cf1271972a7e6a17bb5c0489684240177dee36f4`) ;
`PROTOCOL_maxsep_adoption_859.md` (SHA-256
`efb5da799d245d8e5db570945acc480f1c5bae42d63ed29b7cfeb780610e675b`) ;
§8.56 (`section_8.56_sep_maxsep.md`, SHA-256
`9015ab0cf8d4b577a5ba3bd37512032461762f31f9daa177f63ba41120fe9012`).

## 0. Verdict d'abord — ce qui est gelé ici

Le §8.59 a recommandé l'ADOPTION SOUS CONDITION (provisoire) de `maxsep`
seul comme score MC affiché : D1, D2, D5 passent, D3 et D4 échouent.
Le présent chantier est le DOSSIER DE DÉCISION : il re-vérifie une
dernière fois les chiffres du §8.59 par un second calcul indépendant
(troisième lecture des sorties détenues : extracteur §8.59 + vérifieur
§8.59 + présent chantier) et il rédige la décision d'adoption
provisoire comme CONVENTION D'AFFICHAGE, applicable aux sections
futures si Zackary donne son go. Il ne tranche rien de nouveau sur le
score : il confirme ou il retire la recommandation du §8.59, chiffres
à l'appui, et il fige la forme exacte de la convention.

**Avertissement consigné AVANT tout calcul :** les nombres du §8.59
sont la MOTIVATION de ce chantier, pas son verdict : le verdict repose
sur la RE-VÉRIFICATION ci-dessous. Si elle contredit le §8.59, ce sont
les chiffres re-vérifiés qui font foi et l'écart est consigné, paire
par paire, sans arrondi ni silence.

## 1. Définitions exactes (reprises du §8.59, inchangées)

- **`maxsep`** = `best_config.metrics.max_separation` (|d de Cohen|,
  [0, ∞[), lu dans les JSON v6.2/v6.1 existants.
- **`sep`** = `maxsep / (1 + maxsep)` ([0, 1[), transformée strictement
  croissante de `maxsep`.
- **Ancien MC** = `best_config.score` = composite
  `0.3·s_norm + 0.3·stability + 0.2·robustness + 0.2·sharpness`
  (sélection du best_config, inchangée par toute décision ici).
- **Classe de séparation d'une paire** (au plancher 0,07, dans les
  unités propres du score jugé) : « sépare » si l'écart réel−nul est
  > 0,07 et de signe égal à la direction majoritaire (réel > nul) ;
  « ne sépare pas » sinon. Le signe seul (positif / négatif) est la
  « classe de signe ».
- **Plancher équivalent-sep** d'une paire :
  `0,07·(1 + maxsep_R)·(1 + maxsep_N)`.

## 2. Ensembles jugés — les MÊMES 60 paires que §8.56 / §8.59

Tous lus dans les `master_results.json` v6.2/v6.1 déjà sur disque,
AUCUN nouveau run :

- **V1 — 8 paires principales** (phase 2) : HP35, TCGA v4, GSE71729,
  GSE62452, ICGC, IMMUNE_TCGA, PARP_TCGA, DEPMAP.
- **V2 — 48 paires rotations sans doublon** (§8.44 : 44 du lot
  `manifest_v62_dedup_844.txt` + 4 du §8.41 : CLDN18 v6.1, CTLA4,
  ACO2, PARP1).
- **V3–V5 — descriptifs** : Test A (prolifération), bras MTAP
  (série PRMT5-flux, série MTAP), artefact pureté V4R_PURITY.

Total : 8 + 48 + 4 = **60 paires, 120 runs**. Plancher : 0,07,
appliqué dans les unités propres de chaque score (même convention
que §8.56, §8.59, S_sep, v6.3, v6.4).

## 3. Ce que « adoption provisoire » voudrait dire — convention gelée

Si Zackary donne son go après lecture de la §8.64, la convention
d'affichage suivante s'applique à toutes les sections FUTURES du
livre blanc (les sections §8.1–§8.63 gardent leurs valeurs
historiques, avec mention du changement et sa date) :

1. Le score MC AFFICHÉ devient `best_config.metrics.max_separation`
   (le |d de Cohen| maximal du scan), à la place de l'ancien composite.
2. L'ancien MC reste AFFICHÉ EN SECOND, comme score secondaire,
   partout où `maxsep` est affiché comme score principal.
3. `sep` (= maxsep/(1+maxsep)) est affiché EN COMPAGNON borné [0, 1]
   partout où `maxsep` est affiché.
4. Le plancher 0,07 est publié EN UNITÉS |d| à chaque table.
5. Chaque table qui cite le score porte en tête la mention :
   « adoption provisoire (§8.59, §8.64) — le verdict de suffisance
   tient à une paire aux principales (ICGC) et à l'échelle du
   plancher », tant que la condition C3 du §8.59.8 n'est pas levée.
6. La SÉLECTION du best_config continue d'utiliser l'ancien composite
   — ce chantier ne propose pas de changer la sélection. Seuil MC,
   cascade, S_sep, Delta, L7a inchangés.
7. AUCUNE nouvelle version de code : pas de v6.5, pas de modification
   de v6.2. L'adoption est une décision d'affichage consignée, pas un
   changement de pipeline.

Conditions du §8.59.8 reprises telles quelles : **C1** go explicite de
Zackary après lecture de la section (sans ce go, rien ne change) ;
**C2** affichage conjoint et fragilité en tête (points 2–5 ci-dessus) ;
**C3** pleine adoption différée jusqu'à confirmation indépendante
portant A2 à 7/8 — une paire principale supplémentaire indépendante
qui sépare au plancher 0,07 en `maxsep`, ou un lot de paires nouvelles
confirmant A2 à ≥ 7/8 — à consigner dans une section ultérieure, avec
son propre protocole gelé.

## 4. Portes D1–D5 (reprises du §8.59, barres inchangées)

- **D1 — re-confirmation de la suffisance :** A1 ≥ 30/48 rotations,
  A2 ≥ 6/8 principales ET ≥ 7/8 positifs, A3 HP35 ≥ 0,30.
- **D2 — exactitude de la re-vérification :** (a) le présent second
  calcul indépendant reproduit `sep` et `maxsep` à **0,0 exact** sur
  les 120/120 runs ; (b) les valeurs recoupées contre
  `maxsep_adoption_859_table.json` et contre
  `sep_maxsep_856_table.json` concordent à 1e-9 ; (c) l'ancien MC relu
  concorde sans écart avec §8.44 (rotations) et phase 2 v6.2
  (principales) à 1e-9 ; (d) SHA-256 de v6.2, v6.1, v6, v6.3, v6.4
  revérifiés inchangés après travaux.
- **D3 — robustesse à une paire (leave-one-out) :** en retirant
  N'IMPORTE QUELLE paire unique de V1, le nombre de paires restantes
  > 0,07 reste ≥ 6 (sur 7 restantes) ; en retirant n'importe quelle
  paire unique de V2, le nombre restant > 0,07 reste ≥ 30 (sur 47
  restantes).
- **D4 — robustesse d'échelle :** `maxsep` franchit A2 (≥ 6/8 et
  ≥ 7/8 positifs) quand le plancher est le plancher ÉQUIVALENT-sep,
  propre à chaque paire.
- **D5 — stabilité des classes :** (a) 0 changement de classe de
  séparation `maxsep` entre la re-vérification et le §8.56 publié,
  sur les 60 paires ; (b) 0 changement de classe de signe entre
  `d_maxsep` et `d_sep`, sur les 60 paires.

### Règle de verdict (gelée)

- **ADOPTER** (pleine) si et seulement si D1 ∧ D2 ∧ D3 ∧ D4 ∧ D5.
- **ADOPTER SOUS CONDITION** si D1 ∧ D2 ∧ D5 passent mais D3 ou D4
  échoue : la recommandation du §8.59 est CONFIRMÉE, et la convention
  du §3 ci-dessus est la forme exacte de l'adoption provisoire
  proposée à Zackary.
- **NE PAS ADOPTER** si D1, D2 ou D5 échoue : la recommandation du
  §8.59 est RETIRÉE, le statu quo tient (v6.2, ancien MC affiché avec
  ses défauts connus §8.49.3), et la section dit pourquoi, chiffres
  à l'appui. Aucune repondération, aucun nouveau terme, aucune
  redéfinition du plancher après coup.
- **ÉCART, MÊME MINIME :** tout écart entre la présente re-vérification
  et le §8.59 (une valeur, un comptage, un classement) est consigné
  paire par paire dans la section et dans le rapport final, avec son
  ampleur exacte. Un écart sur D1, D2 ou D5 entraîne le retrait de la
  recommandation ; un écart sur D3 ou D4 qui en changerait le sens
  (une porte passante devenant échouante, ou l'inverse) est consigné
  et le verdict est re-déterminé par la règle ci-dessus sur les
  chiffres re-vérifiés, pas sur les chiffres du §8.59.

## 5. Méthode de re-vérification (lecture seule)

1. Script propre du chantier, `verify_maxsep_decision_864.py`
   (SHA noté au rapport) : lecture SEULE des 120
   `master_results.json` ; pour chaque run, lit
   `best_config.metrics.max_separation` et `best_config.score`
   (ancien MC, garde-fou), calcule `sep = maxsep/(1+maxsep)`.
   Le script ne réutilise AUCUNE fonction de
   `extract_maxsep_adoption_859.py` ni de `verify_maxsep_adoption_859.py`
   : autre parcours des JSON (descente récursive générique à la
   recherche de `best_config`, comme le vérifieur §8.59, mais
   re-écrit), autres noms, autre structure de comptage ; la liste des
   dossiers est reconstruite depuis le manifest §8.44 et les listes
   figées du protocole §8.59. Sortie :
   `maxsep_decision_864_verify.json`.
2. Recoupements : `sep`/`maxsep`/ancien MC par paire vs
   `maxsep_adoption_859_table.json` (tol. 1e-9) et vs
   `sep_maxsep_856_table.json` (tol. 1e-9) ; ancien MC relu vs
   `ssep_844_rotations.csv` (V2) et `v62_phase2_table.csv` (V1)
   (tol. 1e-9) ; versions JSON consignées (v6.2 attendue partout
   sauf CLDN18 en v6.1).
3. Re-calcul des portes dans le même script, après les recoupements :
   D1 (comptages A1/A2/A3), D3 (leave-one-out exhaustif sur V1 et V2),
   D4 (comptage au plancher équivalent-sep par paire), D5a/D5b
   (comparaisons de classes), marges des paires charnières (ICGC,
   MYH9, MUC16 et toute paire à moins de 0,01 du plancher),
   sensibilités S1 (sans plancher), S5 (plancher de Cohen 0,20) et
   S7 (changements de classe ancien MC → `maxsep` seul).
4. **Runs du pipeline : AUCUN run n'est prévu.** La re-vérification
   est hors-ligne. Si un `master_results.json` était absent ou
   corrompu (champ manquant, version inattendue, maxsep non fini),
   le cas serait consigné, le run v6.2 correspondant serait relancé
   avec `systemd-run` (JAMAIS `nohup`), l'exit code noté, et la
   re-vérification refaite sur le JSON régénéré — avec la cause de
   l'absence consignée. Aucun run préventif, aucun run « pour confirmer ».
5. Aucune modification de code, aucun push GitHub, aucune Release,
   aucune modification du livre blanc dans ce chantier (section
   `section_8.64_maxsep_decision.md` séparée, fusion par le
   coordinateur).

## 6. Contrôles descriptifs (à publier, ne décident pas)

- **Test A (V3)** : écarts `sep` / `maxsep` / ancien MC rapportés
  tels quels. Rappel §8.59 : ancien MC −0,0948, maxsep +0,2501,
  sep +0,1567.
- **MTAP (V4)** : écarts rapportés tels quels. Rappel série
  PRMT5-flux : ancien MC +0,0004, maxsep −0,1036, sep −0,0671 ;
  série MTAP : ancien MC −0,1642, maxsep +0,1957, sep +0,1278.
- **Pureté (V5)** : écart rapporté tel quel. Rappel : ancien MC
  +0,1520, maxsep −0,0670, sep −0,0483 (artefact CORRIGÉ).

## 7. Règles du projet rappelées

- Aucun consensus exigé entre flux ou contrôles ; aucun seuil
  pré-enregistré au-delà de ceux écrits ici ; aucune affirmation
  clinique — l'étude porte sur l'instrument, pas sur le cancer.
- Verdicts seulement sur les données et runs du jour (relectures du
  20 nov. 2026 des JSON v6.2 existants) ; les diagnostics §8.56 et
  §8.59 sont une motivation, pas une preuve. Ne jamais importer de
  conclusions d'autres expériences.
- Si le résultat est négatif ou ambigu, il est dit tel quel. En
  particulier : si D3 ou D4 échoue, la recommandation CONDITIONNELLE
  doit nommer la porte échouée, la paire qui la fait échouer, et la
  condition précise qui la lèverait — pas une formule vague.
- La décision finale d'adoption revient à Zackary ; ce chantier
  recommande (adopter / adopter sous condition / ne pas adopter),
  il n'adopte pas. Aucune v6.5, aucune modification de code.

## 8. Traçabilité et provenance

- Protocole : ce fichier, `PROTOCOL_maxsep_decision_864.md` (SHA noté
  au rapport).
- Re-vérification indépendante : `verify_maxsep_decision_864.py`
  (SHA noté), sortie `maxsep_decision_864_verify.json`.
- Section : `section_8.64_maxsep_decision.md` (verdict d'abord).
- Données : JSON v6.2 existants (lots §8.44, phase 2, §8.43, Test A) ;
  CSV inchangés, SHA déjà publiés dans `PROVENANCE_rotations_dedup_844.md`,
  `PROVENANCE_tcga_v4.md`, `PROVENANCE_mtap_prmt5_flux.md`,
  `PROVENANCE_testA_proliferation.md`. Nuls = lignes permutées, graine
  42 — échantillons hypothétiques, pas des mesures ; séries réelles =
  résidus d'expression / dépendance CRISPR (mesures instrumentales
  transformées). Aucune valeur inventée ; aucune valeur recopiée à la
  main (tables générées depuis `maxsep_decision_864_verify.json`,
  vérifiées paire par paire contre `maxsep_adoption_859_table.json`
  à 1e-9).
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`), v6.1 (`2af5e5ce…c1c9`),
  v6 (`bb8bbdba…c0773`), v6.3 (`552e7359…44ffb`), v6.4 (`9ed728da…9ea3d`).
  Aucune nouvelle version construite dans ce chantier.

— Fin du protocole gelé §8.64. —
