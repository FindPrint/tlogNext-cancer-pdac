# Cancer du pancréas (PDAC) — pipeline universel v6.2

Dépôt public de travail du projet PDAC : recherche d'un remède pour le
cancer du pancréas avec le pipeline universel de détection de ruptures
(v6.2), données ouvertes, protocoles gelés, résultats vérifiés.

## État au 20 novembre 2026

- Livre blanc : `livre-blanc-pdac-v6.md`, 723 pages (PDF partagé séparément),
  SHA-256 `16fa081114b2aa6c3a1af7985639d908151d671b0a560861425d9a8c8c48b57b`
  (11 522 319 octets), sections §8.1–§8.53. Le fichier Markdown ici a pour SHA-256
  `7da02cca2875e5e31a56b19c21b67b009b6430fa8a123b537e186e1c33af503a`
  (5 989 lignes).
- Pipeline : `universal_v6.2.0_cohen.py`, version de travail, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
  v6.1 = référence, v6 = historique. `universal_v6.3.0_cohen.py`
  (recomposition du score MC) est joint pour vérification : proposition
  REJETÉE (§8.49), v6.2 reste la version de travail.
  `universal_v6.4.0_cohen.py` (recomposition du MC par la
  récurrence-concentration) est joint pour vérification : proposition
  REJETÉE (§8.52), v6.2 reste la version de travail.
- Les 4 verdicts §8.50–§8.53 : (§8.50) arbitrage MTAP TIENT — sur 10 nuls
  frais (graines 1011 à 11111), l'écart S_sep réel − nul vaut au minimum
  +0,1110 (médiane +0,1595, maximum +0,1981), 10/10 au-dessus du plancher
  0,07, 13/13 avec les 3 nuls anciens ; la marge fragile du §8.46 était la
  queue basse de la distribution nulle. (§8.51) la pureté n'explique PAS
  la corrélation immunitaire — après régression de chaque gène immunitaire
  sur les deux scores de pureté, la corrélation intra-famille demeure
  (0,5563 → 0,5480, chute de 1,5 %) ; ordonner les flux immunitaires
  résidualisés par CD8A résidualisé sépare presque autant que le brut
  (+0,9174 contre +0,9838, 93,3 % conservés), comme prédit par la
  régression §8.48 (+0,9185, à 0,0011 près). (§8.52) recomposition du MC (v6.4) REJETÉE — MC2 suit
  maxsep sans ressusciter Test A ni renverser les verdicts NON (§8.34,
  §8.43), sous les critères gelés. (§8.53) plancher honnête des S_sep
  nuls à n≈70 : 0,38 en ICGC, 0,36 en GSE62452 (p95, réplique 1000
  tirages) — le réel ICGC (0,2289) est sous ce plancher, le réel GSE62452
  (0,4656) est au-dessus ; ≈200 nuls au total, la médiane converge dès
  ~50–100, le p95 exige davantage.

## Structure

- `livre-blanc-pdac-v6.md` — livre blanc complet (§8.1–§8.53).
- `universal_v6.2.0_cohen.py` — pipeline v6.2 (Cohen-d partout).
- `universal_v6.3.0_cohen.py` — proposition v6.3 REJETÉE (§8.49).
- `universal_v6.4.0_cohen.py` — proposition v6.4 REJETÉE (§8.52).
- `README.md`, `DATA_SOURCES.md`, `MANIFEST_SHA256.txt` — ce fichier,
  les sources des données, les SHA-256 de chaque fichier du dépôt.
- `provenance/` — 54 fichiers : protocoles gelés (`PROTOCOL_*.md`) et
  provenances (`PROVENANCE_*.md`) de chaque lot, plus
  `PUBLICATION_tlogNext.md`.
- `results/` — 15 tables vérifiées v6.1/v6.2/v6.3/v6.4 (validation, phase 2,
  Delta, MC recomposé).
- `sections/` — sections §8.38–§8.53 du livre blanc, fichiers sources.
- `scripts/` — 110 scripts de construction des flux, d'extraction et
  d'analyse.
- `data_flux/` — 424 CSV/JSON : flux d'entrée des runs, tests directs,
  extraits ssep / v62_delta / §8.46–§8.53.

## Données brutes

Les matrices brutes (~2 Go) ne sont pas dans ce dépôt (limite snapshot
GitHub : 2 000 fichiers, 16 Mio). Voir `DATA_SOURCES.md` : chaque source
(URL, accès, hachage) et le script pour les re-télécharger et reconstruire
les flux de `data_flux/`.

## PDF

Le PDF du livre blanc (723 pages, binaire) est partagé séparément : les
snapshots GitHub n'acceptent que des fichiers UTF-8 de moins de 16 Mio
au total. Son SHA-256 est rappelé ci-dessus.

## Suite

La suite du travail (phase 2) se poursuit dans le dépôt
`tlogNext-pdac-phase2`, travail d'un autre agent — ce dépôt-ci reste
l'état vérifié du travail v6.2 au 20 novembre 2026.

Projet : FindPrint / TagPrint. Données ouvertes, code reproductible,
résultats négatifs rapportés comme les positifs.
