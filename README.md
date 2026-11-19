# PDAC v6.2 — À la recherche d'un remède pour le cancer du pancréas

**Travail non clinique, bénévole, sans financement, sur données publiques.**
Ce dépôt contient le travail reproductible du projet PDAC (15–19 novembre
2026) : livre blanc, scripts, provenances, résultats. Le livre blanc complet
(PDF, 521 pages, 19 nov. 2026, §8.1–§8.39) est partagé séparément ; sa source
Markdown est ici (`livre-blanc-pdac-v6.md`).

**État au 19 novembre 2026 — v6.2 adoptée comme version de travail** (go de
Zackary le 19 nov. 2026, « Lance tout cela »). Code ici :
`universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` ;
la v6.1.0 devient la référence, SHA-256
`2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ;
la v6.0.0 reste la référence historique, SHA-256
`bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`.
Le pipeline reste un instrument privé, jamais commercialisé ; ce dépôt est
public par décision de Zackary (19 nov. 2026).

## En une phrase — état au 19 novembre 2026

Parmi les ~12 patients dont la tumeur exprime le plus KRAS, **CA125
(MUC16) et CEA (CEACAM5) sont élevés** — confirmé en expression dans
**3 cohortes sur 4** (TCGA, GSE71729, GSE62452 oui ; ICGC non), et CA125
prédit une survie plus courte dans **2 cohortes sur 3** (TCGA : Cox 1,44
univarié ; ICGC : quartile 9,5 contre 23,8 mois, p = 0,002, Cox 1,57).

**Avance clinique réelle, trouvée hors pipeline :** le daraxonrasib
(pan-RAS, approuvé par la FDA le 26 août 2026) double la survie médiane
en phase III (13,2 contre 6,7 mois, HR 0,40 — O'Reilly et al.,
*N Engl J Med* 2026, https://doi.org/10.1056/NEJMoa2605555).
**Piste la plus solide du projet :** vopimetostat + daraxonrasib, 82 % de
réponses (18/22) chez les patients MTAP-délétés prétraités (phase 1/2,
non randomisée ; phase 3 prévue 1er semestre 2027), avec un appui mesuré
(dépendance PRMT5 plus forte en pancréas, p = 0,0036 ; l'effet suit MTAP,
pas CDKN2A — 3 confirmations indépendantes).
**Seule piste ouverte :** ATR seul (hypothèse d'expression, sans appui
CRISPR ni médicament).

## Ce que la v6.2 apporte — et ce qu'elle n'apporte pas (§8.37–§8.39)

- **Hachage stable L5 : la gigue est tombée à 0.** 20 runs sur 20,
  cascades identiques à la v6.1 sur les 10 paires, chaque run relancé donne
  exactement les mêmes chiffres. L'instrument est devenu fiable et
  reproductible.
- **S_sep ne sépare pas mieux que la v6.1** (§8.38) : sur 29/29 paires, il
  donne exactement les mêmes chiffres que max_separation en v6.1. Aucun
  bras reclassé. Contradiction non résolue pour MTAP (S_sep +0,20 contre
  MC/Delta négatifs) ; immunitaire ICGC inversé (−0,22).
- **Delta n'est pas élucidé** (§8.39) : meilleur score honnête 87,9 % des
  paires en hold-out, sous les 90 % exigés. Mesuré : la permutation ne
  change pas la paire, ce qui explique pourquoi Delta ne sépare pas le
  réel du nul.
- **Travaux v6.1 (17–18 nov. 2026) :** 140 runs, aucun contrôle ne sépare
  le réel du nul (lot étendu §8.31, rotations §8.32, test A §8.34, Phase 2
  §8.35, enrichissements §8.36) ; trois blocs de co-expression confirmés
  (estomac/mucus, immunitaire, réparation ADN) ; la chaîne KRAS ne
  réapparaît sous aucun autre contrôle.

## Contenu du dépôt

- `livre-blanc-pdac-v6.md` — le livre blanc complet, §8.1–§8.39
  (SHA-256 `937d565487248ab49cfb5a6973e03ab6ed5e72ec90bae79992653b8e3b86420c`).
- `universal_v6.2.0_cohen.py` — le pipeline v6.2 (version de travail).
- `scripts/build_v6.2.py` — construction de la v6.2 depuis la v6.1.
- `provenance/` — protocoles et provenances (`PROTOCOL_v6.2.md`,
  `PROVENANCE_*.md` : sources, auteurs, dates, dépôts, hachages).
- `results/` — tables de validation, Phase 2 et élucidation de Delta (v6.2).
- `sections/` — textes des §8.38 (S_sep) et §8.39 (Delta).

Le PDF (521 pages, SHA-256
`673f3de56d871e73136912eb76d75dfb890ab286ffa2c3591701905e74ada63e`) n'est
pas dans ce dépôt (limites de taille des dépôts) ; il est partagé
séparément. Les matrices brutes (~2 Go) vivent hors dépôt, avec leurs
URL, hachages et un script de re-téléchargement (voir le livre blanc).

## Honnêteté

Aucune promesse clinique. Un « remède » ici = un médicament ou une
combinaison avec des preuves mesurées, jamais une promesse de guérison.
Chaque verdict négatif est rapporté aussi plainement que chaque positif.
