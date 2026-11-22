# PROTOCOLE GELÉ — §8.95 : score composite gelé, candidate v6.5

Date de gel : 21 novembre 2026, avant tout calcul du nouveau score et toute écriture de code v6.5.
Statut : **PROTOCOLE GELÉ. Aucun calcul du candidat, aucun code v6.5 écrit, aucun run lancé avant ce gel. Toute déviation arrête le travail et se consigne, elle ne se corrige pas en silence.**
Coordinateur : TagPrint. Go de Zackary « Faite tout cela », 21 nov. 2026 11h36, piste 3/4.
Dossier : `~/workspace/runs/pdac-v6/`.
Pipeline de travail : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256 vérifié avant gel `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` (v6.1 `2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`, revérifiés inchangés le 21 nov. 2026).
Références : livre blanc §8.49 (v6.3 REJETÉE), §8.52 (v6.4 REJETÉE), §8.56 (barres A1–A4, 60 paires, `sep` vs `maxsep`), §8.59/§8.64 (adoption maxsep, D1–D5), §8.90.1.2 (correction de Zackary : `maxsep` = score principal AFFICHÉ, pas le verdict — le verdict, c'est la batterie entière ; MC calculé dans le même run que maxsep, lignes 3333 et 10095 du code v6.2).

## 0. Verdict d'abord — ce qui est gelé ici

Une seule proposition, en UNE SEULE variante candidate (pas de variante exploratoire dans ce chantier — les variantes exploratoires ont été les v6.3/v6.4 et le `sep` du §8.56) :

- **Variante C (primaire, candidate) — COMPOSITE GELÉ, RESCORE sans toucher à la sélection** : le meilleur tirage MC reste choisi par l'ancien composite (seuil, cascade, S_sep, Delta inchangés par construction) ; seul le SCORE affiché change, recalculé depuis les métriques du best_config et des 12 tirages stockés (§3). C'est la variante jugée aux barres d'adoption (§5). Elle ne peut pas être adoptée dans ce chantier, quel que soit son score : ce chantier PROPOSE ou REJETTE ; l'adoption finale revient à Zackary, et seulement si TOUTES les barres passent — alors v6.5 devient candidate.

Règle du projet rappelée : aucun consensus exigé entre flux ou contrôles ; aucun seuil pré-enregistré au-delà de ceux écrits ici ; aucune affirmation clinique — l'étude porte sur l'instrument, pas sur le cancer. Le composite ne remplace JAMAIS la batterie : même adopté comme score principal affiché, le verdict reste la batterie entière (§8.90.1.2).

## 1. Définitions (lues dans le code v6.2, pas devinées)

Fichier `universal_v6.2.0_cohen.py`. Mode `fast` : `optimization_iterations = 12` (ligne 243) — 12 tirages MC.
Par tirage (`_monte_carlo_worker`, lignes 3453–3490) : `evaluate_scan_quality` (lignes 3314–3390) donne `max_separation` (ligne ~3330), `s_norm = tanh(max_separation / 2.0)` (ligne 3336), `stability` (ligne 3344), `robustness = exp(-((FWHM − 10)²) / (2 × 5²))` (lignes 3346–3364), `sharpness` (lignes 3365–3381). Score composite du tirage (lignes 3480–3484, poids 0.3/0.3/0.2/0.2) = ancien MC. `max_separation` et MC sont calculés dans le même run (lignes 3333 et 10095, vérifié au §8.90).
L7a : vote signé par run, lu dans `master_results.json` : valeur signée L7a (UP positif, DOWN négatif, neutre 0) telle que publiée aux §8.31/§8.38 (ex. CPTAC UMich down 0,148 ; immune ICGC up 0,358).

## 2. Ensembles jugés — les MÊMES 60 paires que §8.56

Tous lus dans les `master_results.json` v6.2 déjà sur disque, AUCUN nouveau run pour le score :
- **V1 — 8 paires principales** (phase 2) : HP35, TCGA v4, GSE71729, GSE62452, ICGC, IMMUNE_TCGA, PARP_TCGA, DEPMAP (dossiers `results_fast_v62_*`, comme §8.56 §2).
- **V2 — 48 paires rotations sans doublon** (§8.44 : 44 du lot `manifest_v62_dedup_844.txt` + 4 du §8.41 : CLDN18 v6.1, CTLA4, ACO2, PARP1 ; mêmes dossiers que `extract_ssep_844_rotations.py`, `extract_mc63.py`, `extract_mc64.py`).
- **V3 — Test A** (prolifération) : contrôle DESCRIPTIF, pas une porte.
- **V4 — bras MTAP** (série PRMT5-flux primaire, série MTAP secondaire) : contrôles DESCRIPTIFS.
- **V5 — artefact pureté** : contrôle DESCRIPTIF.
Total : 8 + 48 + 1 + 2 + 1 = **60 paires, 120 runs**.

## 3. Règle de combinaison — ÉCRITE AVANT TOUT TEST (c'est le point de ce protocole)

Le candidat est défini AU NIVEAU PAIRE (écart réel−nul), pas au niveau run, pour que chaque terme ait le même sens (positif = le réel sépare plus que le nul) :

```
C_pair = (maxsep_R − maxsep_N)
       + 0,50 × (MC_R − MC_N)
       + 0,50 × (robustness_R − robustness_N)
       + 0,25 × (L7a_R − L7a_N)
```

où, pour chaque côté, `maxsep` = max_separation du best_config, `MC` = score MC du best_config (ancien composite 0,3/0,3/0,2/0,2), `robustness` = robustness du best_config, `L7a` = vote L7a signé du run. Les poids (1 / 0,50 / 0,50 / 0,25) sont GELÉS ici : `maxsep` porte le score (unités |d|), MC et robustesse le modulent à moitié, L7a apporte la direction à un quart. Aucun poids n'est ré-estimé, optimisé ou ajusté après lecture d'un seul chiffre.
Comptage : identique à §8.56 §3 (direction = signe de la somme des écarts sur l'ensemble jugé ; une paire « sépare » si |écart| > gigue_eff ET signe = direction majoritaire ; gigue_eff = max(gigue mesurée, 0,07) ; direction attendue réel > nul). Le plancher 0,07 est appliqué dans les unités propres du candidat C, comme au §8.56 (convention du projet ; l'asymétrie d'échelle est consignée, pas corrigée après coup).

## 4. Travail sur COPIE uniquement (règle dure)

- La candidate v6.5 est construite sur une COPIE de v6.2 : `universal_v6.5.0_cohen.py`, copie octet à octet de v6.2, puis SEULE modification autorisée : l'ajout du calcul de C depuis les métriques déjà stockées (aucun changement de sélection, de seuil, de cascade, de S_sep, de Delta, de MC). v6.2, v6.1, v6, v6.3, v6.4 ne sont JAMAIS modifiées.
- SHA-256 de v6.2 vérifié AVANT tout travail (ci-dessus) et APRÈS tous les travaux (barre A4) ; SHA de v6.1, v6, v6.3, v6.4 revérifiés aussi.
- La re-extraction indépendante (second script, chemin de code distinct) reproduit C à 0,0 exact sur les 120/120 runs (§5, A4).

## 5. Barres C1–C4 (écrites AVANT tout calcul ; la barre ne bouge pas)

Un candidat est PROPOSÉ comme v6.5 **si ET SEULEMENT SI** il franchit les 4 portes. Références (ancien MC : rotations 12/48, principales 1/8 au plancher 0,07 avec 7/8 positifs, HP35 +0,1950 ; v6.3 : 31/48, 4/8, +0,2271 ; v6.4 : 28/48, 4/8, +0,5529 ; `maxsep` §8.56 : 37/48, 6/8, HP35 +1,6512) :
- **C1 — rotations (V2) : le candidat sépare ≥ 30/48** au plancher 0,07, direction réel > nul. (Barre de la mission §8.56, reprise telle quelle ; le comptage à 24/48 sera rapporté en sensibilité, le verdict porte sur 30/48.)
- **C2 — principales (V1) : écart > 0,07 sur ≥ 6/8 paires, ET écart positif sur ≥ 7/8.** (Inchangée depuis v6.3/v6.4/§8.56.)
- **C3 — HP35 (contrôle positif) : écart ≥ 0,30**, dans les unités du candidat C. (Inchangée depuis v6.3/v6.4/§8.56.)
- **C4 — rien ne casse, relecture exacte :** (a) la re-extraction indépendante reproduit C à **0,0 exact** sur les 120/120 runs ; (b) les valeurs recoupées contre les tables `v63_mc_table.json` / `v64_mc_table.json` / `sep_maxsep_856_table.json` concordent à 1e-9 ; (c) l'ancien MC relu concorde sans écart avec §8.44 (rotations) et phase 2 v6.2 (principales) à 1e-9 (garde-fou du lecteur) ; (d) SHA-256 de v6.2, v6.1, v6, v6.3, v6.4 revérifiés inchangés après travaux.
**Si une seule porte échoue : la candidate est REJETÉE, plainement, avec les chiffres — aucune repondération, aucun nouveau terme, aucune redéfinition du plancher après coup — comme v6.3 (§8.49) et v6.4 (§8.52).** Les portes C1–C4 sont les seules ; Test A, MTAP et pureté ne peuvent ni sauver ni couler la candidate (contrôles descriptifs, §6).
Sensibilités rapportées, non décisives : (a) barre C1 à 24/48 ; (b) plancher 0,05 et 0,10 ; (c) C sans le terme L7a (attribution : le terme L7a porte-t-il un gain ?) ; (d) C sans le terme robustesse.

## 6. Contrôles descriptifs (lus, pas jugés)

- V3 Test A : C sépare-t-il la prolifération du nul ? (Attendu NON, comme §8.34 — un OUI serait consigné comme anomalie, pas comme succès.)
- V4 MTAP : C sur la série PRMT5-flux et la série MTAP (§8.43) — le candidat voit-il la même contradiction S_sep/MC que §8.40 ?
- V5 pureté : C sur le bras pureté (§8.51) — le candidat bouge-t-il avec la composition ?

## 7. Livrables

- Copie `universal_v6.5.0_cohen.py` (SHA avant/après, diff contre v6.2 publié — la seule différence autorisée est le calcul de C).
- `extract_c65.py` + second script indépendant de re-extraction + `c65_table.json` (60 paires, C_R, C_N, écart, passe/non, direction).
- Section `section_8.95_composite_v65.md` (fichier séparé ; livre blanc NON édité directement ; PDF NON régénéré ; rien poussé).
- Provenance `PROVENANCE_895.md` (SHA des scripts, des JSON d'entrée, de la copie v6.5 et de son diff).

## 8. Limites déclarées d'avance

- Le candidat est un rescore, pas un nouvel instrument : il ne peut pas voir ce que les 120 runs n'ont pas vu ; s'il sépare, c'est que les métriques détenues séparaient déjà, sous une autre pondération.
- Les poids sont un choix gelé, pas un optimum : un autre choix de poids donnerait un autre score — c'est pourquoi ils sont écrits avant tout test et ne bougent plus.
- L'adoption, même si les 4 portes passent, reste à Zackary ; ce chantier ne crée pas de v6.5 adoptée, seulement une v6.5 candidate.

---
## ADDENDUM — Correction de Zackary du 21 novembre 2026, 12h03 (portée : tout le projet, précisée 12h04)
**Ajouté le 21 novembre 2026, après le gel du protocole — le texte gelé
ci-dessus est intact, cet addendum l'applique.**

**1. Contrôle jamais analysé.** Aucun run pipeline dans cette piste
(rescore depuis les JSON détenus). Vérification faite le 21 novembre
2026 sur les 60 paires rescorées : V1 (8 principales) — contrôle
`step`, KRAS absent des flux ; V2 (48 rotations) — fichiers DEDUP du
§8.44 (`manifest_v62_dedup_844.txt`) : le flux d'ordre est la première
colonne (contrôle) et N'EST PAS parmi les flux analysés — vérifié sur
les 48 fichiers réels (44 du manifeste + 4 `ROTATIONS_EXISTANTES`),
0 colonne `.1`, 0 doublon ; descriptifs — Test A : contrôle PROLIF
(score de prolifération), MKI67 absent des flux ; MTAP_PRMT5FLUX :
contrôle `step`, PRMT5 absent ; MTAP_SERIES : contrôle MTAPCN, 12 flux ;
V4R_PURITY : contrôle `score_acineux`, 12 flux. **Règle respectée dans
cette piste.** Le défaut connu — les 96 fichiers de rotations
d'origine (§8.32), où le flux d'ordre apparaissait deux fois
(`CEACAM5` en contrôle ET `CEACAM5.1` parmi les flux analysés) —
n'est PAS utilisé ici : ces fichiers restent sur le disque comme
témoins du défaut, documenté au §8.32 et corrigé au §8.44 ; il est
traité au §8.97, partie 1. Le composite V2 (31/48) est donc mesuré
sur les mêmes fichiers PROPRES que le 37/48 de maxsep seul — la
comparaison est faite à base identique.

**2. Contrôles non monotones.** Aucun seuil écarté au motif de
non-monotonie dans ce rescore. Les seuils des contrôles non monotones
seraient lus comme des résultats d'analyse à part entière.

**3. Analyse, pas prédiction.** Le verdict REJETÉE décrit ce que le
composite montre sur les 60 paires détenues — il ne prédit pas la
performance du composite sur d'autres paires. La recommandation de ne
pas adopter est une lecture d'analyse, pas une prédiction.
