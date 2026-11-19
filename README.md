# PDAC v6.2 — Archives (15–19 novembre 2026)

> **Travail de suite (phase 2) :** le recentrage, les nouveaux protocoles et le livre blanc vivant se poursuivent dans le dépôt dédié  
> **[FindPrint/tlogNext-pdac-phase2](https://github.com/FindPrint/tlogNext-pdac-phase2)**  
> Ce dépôt (`tlogNext-cancer-pdac`) est conservé comme **archive** des travaux v6.0–v6.2 et du livre blanc jusqu’au §8.42. Ne plus y pousser de nouveau contenu principal.

---

**Travail non clinique, bénévole, sans financement, sur données publiques.**  
Ce dépôt contient le travail reproductible du projet PDAC (15–19 novembre 2026) : livre blanc, scripts, provenances, résultats. Le livre blanc complet (PDF, 565 pages, 19 nov. 2026, §8.1–§8.42) est partagé séparément ; sa source Markdown est ici (`livre-blanc-pdac-v6.md`).

**État au 19 novembre 2026 — v6.2 adoptée comme version de travail** (go de Zackary le 19 nov. 2026, « Lance tout cela »). Code ici : `universal_v6.2.0_cohen.py`, SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` ; la v6.1.0 devient la référence, SHA-256 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ; la v6.0.0 reste la référence historique, SHA-256 `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`.  
Le pipeline reste un instrument privé, jamais commercialisé ; ce dépôt est public par décision de Zackary (19 nov. 2026).

## En une phrase — état au 19 novembre 2026

Parmi les ~12 patients dont la tumeur exprime le plus KRAS, **CA125 (MUC16) et CEA (CEACAM5) sont élevés** — confirmé en expression dans **3 cohortes sur 4** (TCGA, GSE71729, GSE62452 oui ; ICGC non), et CA125 prédit une survie plus courte dans **2 cohortes sur 3** (TCGA : Cox 1,44 univarié ; ICGC : quartile 9,5 contre 23,8 mois, p = 0,002, Cox 1,57).

**Avance clinique réelle, trouvée hors pipeline :** le daraxonrasib (pan-RAS, approuvé par la FDA le 26 août 2026) double la survie médiane en phase III (13,2 contre 6,7 mois, HR 0,40 — O'Reilly et al., *N Engl J Med* 2026, https://doi.org/10.1056/NEJMoa2605555).  
**Piste la plus solide du projet :** vopimetostat + daraxonrasib, 82 % de réponses (18/22) chez les patients MTAP-délétés prétraités (phase 1/2, non randomisée ; phase 3 prévue 1er semestre 2027), avec un appui mesuré (dépendance PRMT5 plus forte en pancréas, p = 0,0036 ; l'effet suit MTAP, pas CDKN2A — 4 confirmations indépendantes, §8.40).  
**Seule piste ouverte :** ATR seul (hypothèse d'expression, sans appui CRISPR ni médicament).

## Ce que la v6.2 apporte — et ce qu'elle n'apporte pas (§8.37–§8.42)

- **Hachage stable L5 : la gigue est tombée à 0.** 20 runs sur 20, cascades identiques à la v6.1 sur les 10 paires, chaque run relancé donne exactement les mêmes chiffres. L'instrument est devenu fiable et reproductible.
- **S_sep ne sépare pas mieux que la v6.1** (§8.38) : sur 29/29 paires, il donne exactement les mêmes chiffres que max_separation en v6.1. Aucun bras reclassé. Contradiction non résolue pour MTAP (S_sep +0,20 contre MC/Delta négatifs) ; immunitaire ICGC inversé (−0,22).
- **Delta n'est pas élucidé** (§8.39, §8.42) : meilleur score honnête 87,9 % des paires en hold-out (§8.39), puis 68,9 % par modélisation des magnitudes (§8.42), sous les 90 % exigés. Mesuré : les magnitudes portent l'échelle du nombre de points, pas le contenu des flux ; la permutation ne change pas la paire, ce qui explique pourquoi Delta ne sépare pas le réel du nul.
- **MTAP arbitré partiellement** (§8.40) : le groupe MTAP-délété se distingue par la dépendance PRMT5 (−1,385 contre −1,010, p = 0,0036, reproduit à l'identique) ; aucun écran de médicaments ne le distingue (0 FDR < 0,05 sur PRISM primaire, PRISM secondaire, GDSC2) et vopimetostat est absent des trois bibliothèques — ce négatif ne touche pas au rationnel vopimetostat + daraxonrasib ; lien KRAS non (Fisher p = 0,073). La contradiction instrumentale (S_sep contre MC/Delta) reste ouverte.
- **S_sep sur les 48 rotations : 48/48** (§8.41), premier 48/48 du projet — mais S_sep détecte l'ordre, pas une rupture (une rotation réelle est ordonnée par un de ses propres flux, le nul est permuté) ; sans le doublon de construction, ~36/48 resteraient au-dessus de la barre (estimation, pas une mesure).
- **Travaux v6.1 (17–18 nov. 2026) :** 140 runs, aucun contrôle ne sépare le réel du nul (lot étendu §8.31, rotations §8.32, test A §8.34, Phase 2 §8.35, enrichissements §8.36) ; trois blocs de co-expression confirmés (estomac/mucus, immunitaire, réparation ADN) ; la chaîne KRAS ne réapparaît sous aucun autre contrôle.

## Contenu du dépôt

- `livre-blanc-pdac-v6.md` — le livre blanc complet, §8.1–§8.42 (SHA-256 `de3aa31618504989f4de7b1b43e197cf796549b20e8701fe0fce2385963a4029`).
- `universal_v6.2.0_cohen.py` — le pipeline v6.2 (version de travail).
- `scripts/build_v6.2.py` — construction de la v6.2 depuis la v6.1.
- `scripts/mtap_arbitration_840.py`, `scripts/extract_ssep_841_rotations.py`, `scripts/v62_delta_magnitudes.py` — scripts des §8.40–§8.42.
- `provenance/` — protocoles et provenances (`PROTOCOL_v6.2.md`, `PROTOCOL_delta_magnitudes.md`, `PROVENANCE_*.md` : sources, auteurs, dates, dépôts, hachages).
- `results/` — tables de validation, Phase 2, élucidation de Delta et modélisation des magnitudes (v6.2), S_sep des 48 rotations.
- `sections/` — textes des §8.38 (S_sep), §8.39 (Delta), §8.40 (arbitrage MTAP) et §8.41 (S_sep rotations). Le §8.42 vit dans le livre blanc et dans `results/v62_delta_magnitudes.md`.

Le PDF (565 pages, SHA-256 `996434e56937720e03d225d00af06bd70294d55f5b00724853894ee57e0f7bc4`) n'est pas dans ce dépôt (limites de taille des dépôts) ; il est partagé séparément. Les matrices brutes (~2 Go) vivent hors dépôt, avec leurs URL, hachages et un script de re-téléchargement (voir le livre blanc).

## Honnêteté

Aucune promesse clinique. Un « remède » ici = un médicament ou une combinaison avec des preuves mesurées, jamais une promesse de guérison. Chaque verdict négatif est rapporté aussi plainement que chaque positif.
