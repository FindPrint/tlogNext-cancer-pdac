# PROTOCOLE GELÉ — §8.59 : trancher l'adoption de `maxsep` seul comme score MC

Date : 20 novembre 2026.
Statut : **PROTOCOLE GELÉ. Aucune extraction du présent chantier, aucun
calcul de verdict, aucun comptage, avant ce gel. Toute déviation arrête le
travail et se consigne, elle ne se corrige pas en silence.**
Auteur : TagPrint (chantier §8.59, coordinateur : fusion au livre blanc ensuite).
Dossier : `~/workspace/runs/pdac-v6/`.
Pipeline de travail : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant le gel ; v6.2, v6.1, v6, v6.3, v6.4 ne sont JAMAIS modifiées —
ce chantier ne construit AUCUNE nouvelle version, ne crée PAS de v6.5 :
l'adoption, si elle est recommandée, est une décision d'AFFICHAGE sur la
v6.2 existante, et elle demandera le go explicite de Zackary après lecture
de la section §8.59).
Références : livre blanc §8.56 (`section_8.56_sep_maxsep.md`, SHA
`9015ab0cf8d4b577a5ba3bd37512032461762f31f9daa177f63ba41120fe9012`) ;
`PROTOCOL_sep_maxsep_856.md` (SHA
`06e36725eedb3d52b1549290e1e8cccff381650928fbf4e6a28a090aec27fd4e`) ;
`PROTOCOL_v6.3_mc.md`, `PROTOCOL_v6.4_mc.md`, `PROTOCOL_v6.2.md` §3.

## 0. Verdict d'abord — ce qui est gelé ici

Le §8.56 a tranché la SUFFISANCE aux barres gelées : `maxsep` seul
SUFFIT (37/48 rotations, 6/8 principales, HP35 +1,6512), `sep` seul
NE SUFFIT PAS (35/48, 5/8, +0,5316) — avec la fragilité nommée : le
verdict tient à trois paires charnières et à l'échelle du plancher
0,07 (ICGC fait passer A2 ; MYH9 et MUC16 font passer A1, MUC16 de
0,0003). Le présent chantier tranche l'ADOPTION, question différente
de la suffisance : **faut-il afficher `maxsep` seul comme score MC à
la place de l'ancien composite ?** L'adoption change le dossier
public ; elle exige donc plus que la suffisance : la re-vérification
exacte (D1–D2), la stabilité des classes (D5), ET la robustesse du
verdict lui-même (D3–D4). Une adoption qui bascule sur une seule
paire ou sur une convention d'échelle n'est pas une adoption pleine :
elle est, au mieux, conditionnelle.

**Avertissement consigné AVANT tout calcul (honnêteté de la question) :**
les nombres du §8.56 sont la MOTIVATION de ce chantier, pas son
verdict : le verdict repose sur la RE-VÉRIFICATION indépendante
ci-dessous (extracteur propre + second calcul indépendant +
recoupements §5/§6). Si la re-vérification contredit le §8.56, ce
sont les chiffres re-vérifiés qui font foi et l'écart est consigné.

## 1. Définitions exactes (reprises du §8.56, inchangées)

- **`maxsep`** = `best_config.metrics.max_separation` (|d de Cohen|,
  [0, ∞[), lu dans les JSON v6.2/v6.1 existants.
- **`sep`** = `maxsep / (1 + maxsep)` ([0, 1[), transformée strictement
  croissante de `maxsep` : mêmes ordres, mêmes signes d'écart sur
  toutes les paires, par construction.
- **Ancien MC** = `best_config.score` = composite
  `0.3·s_norm + 0.3·stability + 0.2·robustness + 0.2·sharpness`
  (sélection du best_config, inchangée par toute décision ici).
- **Classe de séparation d'une paire** (au plancher 0,07, dans les
  unités propres du score jugé) : « sépare » si l'écart réel−nul est
  > 0,07 et de signe égal à la direction majoritaire (réel > nul) ;
  « ne sépare pas » sinon. Le signe seul (positif / négatif) est la
  « classe de signe ».

### 1.1. Ce que « aucune paire ne change de classe » veut dire ici — gelé

La mission demande de « vérifier qu'aucune paire ne change de classe
entre le score v6.2 et un score maxsep-seul ». Pris littéralement
(ancien composite contre `maxsep` seul), ce contrôle est impossible
par construction : l'ancien MC sépare 12/48 rotations et 1/8
principales, `maxsep` 37/48 et 6/8 — des dizaines de paires changent
de classe, et c'est précisément l'objet de l'adoption (remplacer un
score qui sépare mal par un score qui sépare mieux). Traiter ce
changement comme un échec rendrait toute adoption logiquement
impossible, quel que soit le score. Le contrôle est donc gelé sous sa
forme vérifiable, en deux volets (porte D5) :

- **D5a — stabilité de la re-vérification :** aucune paire ne change
  de classe de séparation entre la re-vérification du présent chantier
  et les classes `maxsep` publiées au §8.56, sur les 60 paires.
- **D5b — stabilité de signe entre les deux lectures du même score :**
  aucun changement de classe de signe entre `d_maxsep` et `d_sep`
  sur les 60 paires (attendu par la monotonie, à vérifier, pas à
  supposer).
- **Descriptif (ne décide pas) :** le nombre de paires qui changent de
  classe de séparation entre l'ancien MC et `maxsep` seul est compté
  et publié (§6, sensibilité S7) — c'est la mesure du changement
  proposé, pas un garde-fou.

## 2. Ensembles jugés — les MÊMES 60 paires que §8.56 / v6.3 / v6.4

Tous lus dans les `master_results.json` v6.2/v6.1 déjà sur disque,
AUCUN nouveau run pour le score (sauf §5, règle de rattrapage) :

- **V1 — 8 paires principales** (phase 2) : HP35, TCGA v4, GSE71729,
  GSE62452, ICGC, IMMUNE_TCGA, PARP_TCGA, DEPMAP (mêmes dossiers
  qu'au §8.56).
- **V2 — 48 paires rotations sans doublon** (§8.44 : 44 du lot
  `manifest_v62_dedup_844.txt` + 4 du §8.41 : CLDN18 v6.1, CTLA4,
  ACO2, PARP1 — mêmes dossiers que `extract_sep_maxsep_856.py`).
  Familles : IMMROT (12), V4ROT (12), PARPROT (12), DEPMAPROT (12).
- **V3–V5 — descriptifs** : Test A (prolifération), bras MTAP
  (série PRMT5-flux, série MTAP), artefact pureté V4R_PURITY :
  contrôles DESCRIPTIFS (§6), 4 paires.

Total : 8 + 48 + 4 = **60 paires, 120 runs**. Plancher : 0,07,
appliqué dans les unités propres de chaque score (même convention
que §8.56, S_sep, v6.3, v6.4).

## 3. Ce que « adopter `maxsep` » voudrait dire — gelé avant le verdict

Si Zackary adopte (sur recommandation du présent chantier et après
lecture de la §8.59), l'adoption est STRICTEMENT ceci, rien de plus :

1. Le score MC AFFICHÉ devient `best_config.metrics.max_separation`
   (le |d de Cohen| maximal du scan), à la place de l'ancien composite.
2. La SÉLECTION du best_config continue d'utiliser l'ancien composite
   (lignes 3480–3484 de v6.2) — ce chantier ne propose pas de changer
   la sélection. Seuil MC, cascade, S_sep, Delta, L7a inchangés.
3. `sep` (= maxsep/(1+maxsep)) est affiché EN COMPAGNON borné [0, 1]
   partout où `maxsep` est affiché, pour garder une échelle comparable
   aux scores publiés.
4. Le plancher 0,07 est publié EN UNITÉS |d| à chaque table, avec la
   fragilité du §8.56.4 rappelée (0,07 en |d| est en dessous du « petit »
   effet de Cohen, 0,2).
5. AUCUNE nouvelle version de code : pas de v6.5, pas de modification
   de v6.2. L'adoption est une décision d'affichage consignée, pas un
   changement de pipeline. Le PDF est régénéré et poussé sur GitHub
   (règle permanente « Toujours github et pdf !!! »), et les sections
   qui citent le MC sont mises à jour par le coordinateur.
6. Si la recommandation est CONDITIONNELLE, la pleine adoption est
   différée jusqu'à la levée explicite des conditions (§4, règle de
   verdict) ; en attendant, l'adoption provisoire applique les points
   1–5 avec l'étiquette « provisoire » et la fragilité en tête de
   chaque table.

## 4. Barres d'adoption D1–D5 (écrites AVANT tout calcul ; la barre ne bouge pas)

Références : ancien MC — rotations 12/48, principales 1/8 au plancher
0,07 (7/8 positifs), HP35 +0,1950. §8.56 (motivation, à re-vérifier) :
`maxsep` 37/48, 6/8 (7/8 positifs), HP35 +1,6512 ; `sep` 35/48, 5/8,
+0,5316.

- **D1 — re-confirmation de la suffisance :** le `maxsep` re-vérifié
  franchit les trois barres du §8.56 : A1 ≥ 30/48 rotations,
  A2 ≥ 6/8 principales ET ≥ 7/8 positifs, A3 HP35 ≥ 0,30.
- **D2 — exactitude de la re-vérification :** (a) le second calcul
  indépendant (§5, chemin de code distinct) reproduit `sep` et
  `maxsep` à **0,0 exact** sur les 120/120 runs ; (b) les valeurs
  recoupées contre `sep_maxsep_856_table.json` concordent à 1e-9 ;
  (c) l'ancien MC relu concorde sans écart avec §8.44 (rotations) et
  phase 2 v6.2 (principales) à 1e-9 ; (d) SHA-256 de v6.2, v6.1, v6,
  v6.3, v6.4 revérifiés inchangés après travaux.
- **D3 — robustesse à une paire (leave-one-out) :** en retirant
  N'IMPORTE QUELLE paire unique de V1, le nombre de paires restantes
  > 0,07 reste ≥ 6 (sur 7 restantes) ; en retirant n'importe quelle
  paire unique de V2, le nombre restant > 0,07 reste ≥ 30 (sur 47
  restantes). Autrement dit : le verdict ne doit reposer sur aucune
  paire unique. (Équivaut à exiger 7/8 en V1 et 31/48 en V2 avant
  retrait ; la barre est volontairement plus dure que D1, parce
  qu'adopter n'est pas seulement « suffire ».)
- **D4 — robustesse d'échelle :** `maxsep` franchit A2 (≥ 6/8 et
  ≥ 7/8 positifs) quand le plancher est le plancher ÉQUIVALENT-sep,
  propre à chaque paire : `d_maxsep > 0,07·(1 + maxsep_R)·(1 + maxsep_N)`.
  Autrement dit : le verdict survit à l'expression du plancher à
  échelle égale à celle de `sep`. (Par l'identité du §8.56.2, D4
  équivaut à « `sep` franchit A2 » ; l'équivalence est consignée ici
  avant le calcul, elle ne sera pas découverte après.)
- **D5 — stabilité des classes :** (a) 0 changement de classe de
  séparation `maxsep` entre la re-vérification et le §8.56 publié,
  sur les 60 paires ; (b) 0 changement de classe de signe entre
  `d_maxsep` et `d_sep`, sur les 60 paires.

### Règle de verdict (gelée)

- **ADOPTER** (pleine) si et seulement si D1 ∧ D2 ∧ D3 ∧ D4 ∧ D5.
- **ADOPTER SOUS CONDITION** si D1 ∧ D2 ∧ D5 passent mais D3 ou D4
  échoue : adoption PROVISOIRE selon §3 (points 1–6), avec les
  conditions précises suivantes, toutes vérifiables :
  (C1) go explicite de Zackary après lecture de la §8.59 ;
  (C2) affichage conjoint `maxsep` + `sep` (§3.3) et plancher en
  unités |d| rappelé à chaque table (§3.4) ;
  (C3) pleine adoption différée jusqu'à ce qu'une confirmation
  indépendante lève la fragilité — soit une paire principale
  supplémentaire indépendante qui porte A2 à 7/8, soit un lot de
  paires nouvelles confirmant A2 à ≥ 7/8 — à consigner dans une
  section ultérieure ; en attendant, chaque table porte l'étiquette
  « adoption provisoire ».
- **NE PAS ADOPTER** si D1, D2 ou D5 échoue : le statu quo tient
  (v6.2, ancien MC affiché avec ses défauts connus §8.49.3, `maxsep`
  restant l'indicateur de référence), et la section dit pourquoi,
  chiffres à l'appui. Aucune repondération, aucun nouveau terme,
  aucune redéfinition du plancher après coup.

## 5. Méthode d'extraction et de vérification (lecture seule)

1. Extracteur propre du chantier, `extract_maxsep_adoption_859.py`
   (SHA noté au rapport) : lecture SEULE des 120
   `master_results.json` ; pour chaque run, lit
   `best_config.metrics.max_separation` et `best_config.score`
   (ancien MC, garde-fou), calcule `sep = maxsep/(1+maxsep)` ;
   sorties `maxsep_adoption_859_table.csv` /
   `maxsep_adoption_859_table.json`. Écrit APRÈS ce gel, jamais avant.
   Le code ne réutilise PAS les fonctions de
   `extract_sep_maxsep_856.py` (re-écriture propre, autre parcours).
2. Second calcul indépendant, `verify_maxsep_adoption_859.py` (SHA
   noté) : chemin de code distinct (re-lecture directe des JSON par
   un autre parcours, sans réutiliser les fonctions de l'extracteur),
   recalcule `sep` et `maxsep` pour les 120 runs et compare à la table
   de l'étape 1 : écart attendu 0,0 exact sur 120/120. Tout écart =
   résultat à diagnostiquer, pas un bruit.
3. Recoupements : `sep`/`maxsep`/ancien MC par paire vs
   `sep_maxsep_856_table.json` (tol. 1e-9) ; ancien MC relu vs
   `ssep_844_rotations.csv` (V2) et `v62_phase2_table.csv` (V1)
   (tol. 1e-9) ; versions JSON consignées (v6.2 attendue partout
   sauf CLDN18 en v6.1).
4. Analyses d'adoption (dans l'extracteur, après les recoupements) :
   D1 (comptages A1/A2/A3), D3 (leave-one-out exhaustif sur V1 et V2),
   D4 (comptage au plancher équivalent-sep par paire), D5a/D5b
   (comparaisons de classes), marges des paires charnières (distance
   au plancher : ICGC, MYH9, MUC16 et toute paire à moins de 0,01 du
   plancher), sensibilités S1–S7 (§7).
5. **Runs du pipeline : AUCUN run n'est prévu.** La re-vérification
   est hors-ligne. Si un `master_results.json` était absent ou
   corrompu (champ manquant, version inattendue, maxsep non fini),
   le cas serait consigné, le run v6.2 correspondant serait relancé
   avec `systemd-run` (JAMAIS `nohup`, qui meurt avec la session),
   l'exit code noté, et la re-vérification refaite sur le JSON
   régénéré — avec la cause de l'absence consignée. Aucun run
   préventif, aucun run « pour confirmer ».
6. Aucune modification de code, aucun push GitHub, aucune modification
   du livre blanc dans ce chantier (section
   `section_8.59_maxsep_adoption.md` séparée, fusion par le
   coordinateur).

## 6. Contrôles descriptifs (à publier, ne décident pas)

- **Test A (V3)** : écarts `sep` / `maxsep` / ancien MC rapportés
  tels quels. Rappel §8.56 : ancien MC −0,0948, maxsep +0,2501,
  sep +0,1567. Ni l'adoption ni le rejet ne ressuscite Test A.
- **MTAP (V4)** : écarts rapportés tels quels. Rappel série
  PRMT5-flux : ancien MC +0,0004, maxsep −0,1036, sep −0,0671 ;
  série MTAP : ancien MC −0,1642, maxsep +0,1957, sep +0,1278.
- **Pureté (V5)** : écart rapporté tel quel. Rappel : ancien MC
  +0,1520, maxsep −0,0670, sep −0,0483 (artefact CORRIGÉ).
- **S7 — changement ancien MC → maxsep** : nombre de paires qui
  changent de classe de séparation entre l'ancien MC et `maxsep`
  seul, sur V1 et V2, avec la liste des paires. C'est la mesure du
  changement proposé (§1.1).

## 7. Sensibilités descriptives (rapportées, ne décident pas)

- **S1 — sans plancher** : comptage des positifs seuls (réel > nul)
  sur V1 et V2, pour `sep` et `maxsep`.
- **S2 — barre A1 à 24/48** (protocoles v6.3/v6.4) : le verdict A1
  change-t-il sous l'ancienne barre ? Rapporté, non décisif.
- **S3 — équivalence d'échelle** : pour chaque paire, plancher
  `maxsep` équivalent au plancher `sep` ;
  paires `maxsep` passant le plancher littéral 0,07 mais PAS le
  plancher équivalent — c'est exactement l'écart entre les comptages
  `maxsep` et `sep` (détail de D4, paire par paire).
- **S4 — ventilation par famille** (IMMROT / V4ROT / PARPROT /
  DEPMAPROT) pour `sep` et `maxsep` sur V2, avec écarts moyens.
- **S5 — plancher de Cohen 0,20 en |d|** : comptages V1/V2 de
  `maxsep` au plancher 0,20 (le « petit » effet de Cohen) — pour
  situer la laxité du plancher 0,07, sans rien décider.
- **S6 — marges** : pour chaque paire charnière (ICGC, MYH9, MUC16)
  et toute paire à moins de 0,01 du plancher, distance exacte au
  plancher 0,07 en unités `maxsep` et en unités `sep`.

## 8. Règles du projet rappelées

- Aucun consensus exigé entre flux ou contrôles ; aucun seuil
  pré-enregistré au-delà de ceux écrits ici ; aucune affirmation
  clinique — l'étude porte sur l'instrument, pas sur le cancer.
- Verdicts seulement sur les données et runs du jour (relectures du
  20 nov. 2026 des JSON v6.2 existants) ; les diagnostics §8.56 sont
  une motivation, pas une preuve. Ne jamais importer de conclusions
  d'autres expériences.
- Si le résultat est négatif ou ambigu, il est dit tel quel. En
  particulier : si D3 ou D4 échoue, la recommandation CONDITIONNELLE
  doit nommer la porte échouée, la paire qui la fait échouer, et la
  condition précise qui la lèverait — pas une formule vague.
- La décision finale d'adoption revient à Zackary ; ce chantier
  recommande (adopter / adopter sous condition / ne pas adopter),
  il n'adopte pas. Aucune v6.5, aucune modification de code.

## 9. Traçabilité et provenance

- Protocole : ce fichier, `PROTOCOL_maxsep_adoption_859.md` (SHA noté
  au rapport).
- Extraction : `extract_maxsep_adoption_859.py` (SHA noté), sorties
  `maxsep_adoption_859_table.csv` / `maxsep_adoption_859_table.json`.
- Vérification indépendante : `verify_maxsep_adoption_859.py` (SHA
  noté), sortie `maxsep_adoption_859_verify.json`.
- Section : `section_8.59_maxsep_adoption.md` (verdict d'abord).
- Données : JSON v6.2 existants (lots §8.44, phase 2, §8.43, Test A) ;
  CSV inchangés, SHA déjà publiés dans `PROVENANCE_rotations_dedup_844.md`,
  `PROVENANCE_tcga_v4.md`, `PROVENANCE_mtap_prmt5_flux.md`,
  `PROVENANCE_testA_proliferation.md`. Nuls = lignes permutées, graine
  42 — échantillons hypothétiques, pas des mesures ; séries réelles =
  résidus d'expression / dépendance CRISPR (mesures instrumentales
  transformées). Aucune valeur inventée ; aucune valeur recopiée à la
  main (tables générées depuis `maxsep_adoption_859_table.json`,
  vérifiées paire par paire contre `sep_maxsep_856_table.json` à 1e-9).
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`), v6.1 (`2af5e5ce…c1c9`),
  v6 (`bb8bbdba…c0773`), v6.3 (`552e7359…44ffb`), v6.4 (`9ed728da…9ea3d`).
  Aucune nouvelle version construite dans ce chantier.

— Fin du protocole gelé §8.59. —
