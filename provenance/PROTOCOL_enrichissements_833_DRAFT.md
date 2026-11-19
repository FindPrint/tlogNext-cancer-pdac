# Enrichissements §8.33 — BROUILLON de mini-protocoles (18 nov. 2026)

Statut : BROUILLON. Rien n'est gelé, aucun run lancé, aucun CSV de flux
modifié. Devient protocole gelé uniquement sur le go de Zackary, un
enrichissement à la fois. Pipeline : v6.1.0-Cohen (`universal_v6.1.0_cohen.py`,
SHA `2af5e5ce…c1c9`), mode fast, nul permuté graine 42, comme le lot 140/140.

## Ce qui a été fait le 18 nov. (préparation, sans go)

Table `data/mutation_table_pancreas.csv` (45 lignées, script
`build_mutation_table_pancreas.py`, SHA des 5 entrées dans l'en-tête du CSV) :
TP53 mutée 38/45, SMAD4 11/45, CDKN2A 12/45, KRAS 42/45. Les 3 lignées sans
allèle KRAS connu (ACH-000535 BxPC-3, ACH-001377, ACH-001380) sont
exactement les 3 lignées KRAS sauvages au MAF — cohérent, pas une donnée
manquante. Co-occurrences : TP53+SMAD4 10, TP53+CDKN2A 10, SMAD4+CDKN2A 5,
les 3 mutées 5, aucune des 3 : 4.

## A — Série ordonnée par prolifération (TCGA v4, n=178) — la plus faisable

Question gelée avant run : le pipeline voit-il la même chaîne (bloc qui
tombe + MUC16 qui monte) quand l'axe est la prolifération au lieu de KRAS ?
Axe : score prolifération = médiane de MKI67, TOP2A, PCNA, CCNB1, calculé
sur la matrice Firehose TCGA comme au §8.25 (`atr_chek1_retest.py`).
Flux : les 12 mêmes que TCGA v4 (PGC, REG4, CLDN18, MUC17, DPCR1, CR2,
KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16), valeurs v4 corrigées pureté.
Runs : 2 (réel + nul graine 42). Critère écrit avant : séparation réel/nul
sur position du seuil ET sens L7a, comme en v4 (§8.4) — sinon, négatif.
Pourquoi d'abord : ATR seul a survécu au contrôle prolifération (§8.25) ;
ordonner par prolifération teste directement si cet axe porte la chaîne.

## B — Statut mutationnel DepMap (TP53 / SMAD4 / CDKN2A / allèle KRAS)

PAS une série pipeline : effectifs trop petits (TP53 38 contre 7,
SMAD4 11, CDKN2A 12 ; allèles G12D 19, G12V 14 — sous le minimum fast
de 40 points). Tests directs seulement, avec la table du 18 nov. :
dépendance Chronos KRAS / PRMT5 / ATR par groupe (Mann-Whitney + Spearman),
mêmes contrôles que §8.28/§8.29. Question gelée avant test : le statut
TP53/SMAD4/CDKN2A déplace-t-il la dépendance KRAS ou PRMT5 au-delà de
l'effet MTAP déjà mesuré ? Si non, piste fermée comme test direct.

## C — Série ordonnée par stade (TCGA v4, n=178) — possible, avec réserve

Axe : AJCC_PATHOLOGIC_TUMOR_STAGE (`data_clinical_patient.txt`, ligne 5
d'en-tête : STAGE IIB 121, IIA 30, IB 15, III 5, IA 5, IV 5, I 1, vide 2).
Réserve de méthode (§8.33) : le stade est une variable de résultat
clinique, pas un axe neutre — la question devient « le pipeline voit-il
la progression clinique ? », différente de l'axe KRAS. 2 runs (réel + nul)
seulement si Zackary veut cette question-là.

## Non faisable — nommé honnêtement

- Sous-type TCGA : la colonne `SUBTYPE` du fichier clinique vaut « PAAD »
  pour 152 patients sur 184 (32 vides) — c'est le type de cancer, pas un
  sous-type moléculaire. Aucune série par sous-type TCGA n'est possible
  avec ce fichier. (Sous-types Bailey ICGC déjà utilisés au §8.16.)
- Série par allèle KRAS : G12D 19 et G12V 14 lignées dans les 45 — sous
  le minimum de 40 points. L'allèle ne peut servir qu'en test direct
  (déjà fait pour MRTX1133 au §8.20).
- Déconvolution immunitaire, single-cell, spatial, longitudinal : absents
  du disque, impossibles sans nouvelles données (§8.33).
