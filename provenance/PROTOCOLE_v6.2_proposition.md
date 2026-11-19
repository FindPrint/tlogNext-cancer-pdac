# PROPOSITION v6.2 — conception gelée (à valider, rien n'est construit)

Date : 18 novembre 2026.
Statut : **PROPOSITION SEULEMENT, issue de la phase 2 (§8.35). Aucun code
écrit, aucun run lancé, aucun changement de la v6.1. Toute construction
attend le go séparé de Zackary, suivi d'un nouveau cycle de validation
complet (comme pour la v6.1, §8.30).**
Auteur : TagPrint, sur la base de la phase 2 (protocole gelé
`PROTOCOL_phase2_discrimination.md`, 16 nov. 2026 ; résultats
`v61_phase2_table.md`).

## 1. Ce que la phase 2 a mesuré (rappel, pas une opinion)

- MC best_score : sépare 1/8 paires principales (HP35 seul) ; écarts PDAC
  +0,0059 à +0,0545, tous sous la gigue ±0,07 — 7/8 positifs mais noyés.
- max_separation : sépare 6/8 principales et 16/23 secondaires, sens
  réel > nul ; HP35 +1,6512, écarts PDAC +0,10 à +0,37.
- Delta : 6/8, mais échoue sur HP35 (témoin positif) et deux écarts ≤ 0,15.
- L7a : 4/8, direction majoritaire négative. Cohérence par flux : 2/8.
- Falsification : 4/5 disponibles, mais comparaison interne, pas au nul
  permuté ; direction inversée en annexe (7/18).
- Gigue L5 mesurée : ±0,07, cause identifiée au §8.30 — `hash()` Python,
  aléatoire d'un processus à l'autre (`hash(metric)` non déterministe).

## 2. Pistes proposées (dans l'ordre, une seule à la fois, chacune validée avant la suivante)

### (a) Hachage stable L5 — PRIORITAIRE, déjà proposée au §8.30
Remplacer `hash(metric)` par `hashlib.sha256` (ou équivalent stable) dans
le calcul L5, sur une COPIE (`universal_v6.2.0_cohen.py`), v6.1 intacte.
But : faire tomber la gigue run-to-run, pour que les écarts MC de +0,01 à
+0,05 deviennent lisibles au lieu d'être noyés. Validation exigée : mêmes
runs de validation que la v6.1 (10 runs fast : HP35, TCGA v4, GSE62452,
ICGC, DepMap, réel + nul) + relecture des cascades — toute cascade qui
change doit être expliquée, pas cachée. Si les cascades changent, la piste
s'arrête là et on revient à la v6.1.

### (b) Score fondé sur max_separation — À TESTER, jamais affirmé d'avance
En protocole gelé séparé, tester si un score de discrimination fondé sur
`metrics.max_separation` (plutôt que sur le best_score MC) sépare mieux
réel et nul — mêmes 8 paires principales, mêmes gigues, même critère
(≥ 6/8). Ce n'est pas une correction du pipeline : c'est une lecture
nouvelle d'un sous-produit existant. Si le test échoue, la piste est
fermée comme les autres, sans retouche après coup.

### (c) Élucider les niveaux discrets de Delta — AVANT tout usage de Delta comme discriminateur
Le §8.32 a montré que Delta est une différence entre deux mesures dont
l'une (d_div) ne prend que quelques niveaux fixes, et que les plus grands
écarts viennent d'un nul ou d'un réel tombé au niveau bas. Avant de
présenter Delta comme un indicateur de discrimination, élucider le
mécanisme qui choisit le niveau — lecture de code + tests ciblés, hors
pipeline si possible. Si Delta s'explique par des sauts de niveau, son
6/8 de phase 2 est un artefact de construction, pas une séparation.

## 3. Ce que cette proposition ne fera pas

- Aucune modification de la v6.1 ni de la v6 (copie séparée seulement).
- Aucun nouveau seuil de séparation pré-enregistré au-delà des critères
  déjà gelés (phase 2, §4 du protocole).
- Aucune affirmation clinique : l'étude porte sur l'instrument.
- Aucun consensus exigé entre flux ou contrôles.
- Aucun changement de code avant le go de Zackary sur CETTE proposition,
  et aucun run de validation avant la conception gelée de chaque piste.

## 4. Décision attendue

Go / non de Zackary, piste par piste, dans l'ordre (a) puis (b) puis (c).
Un « non » sur (a) n'empêche pas de discuter (b) et (c) ; un « oui » sur
(a) n'autorise pas (b) et (c).
