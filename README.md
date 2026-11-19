# Cancer du pancréas (PDAC) — pipeline universel v6.2

Dépôt public de travail du projet PDAC : recherche d'un remède pour le
cancer du pancréas avec le pipeline universel de détection de ruptures
(v6.2), données ouvertes, protocoles gelés, résultats vérifiés.

## État au 19 novembre 2026

- Livre blanc : `livre-blanc-pdac-v6.md`, 675 pages (PDF partagé séparément),
  SHA-256 `40643a828ea22879f0d976b319c939fa1b65022c7999c79ad17994e9c55d605c`,
  sections §8.1–§8.49. Le fichier Markdown ici a pour SHA-256
  `31bc39a1d8d4b09d0704aede16734c2034b77a9221af01fa86184054954eebda`
  (4 692 lignes).
- Pipeline : `universal_v6.2.0_cohen.py`, version de travail, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
  v6.1 = référence, v6 = historique. `universal_v6.3.0_cohen.py`
  (recomposition du score MC) est joint pour vérification : proposition
  REJETÉE (§8.49), v6.2 reste la version de travail.
- Les 4 verdicts §8.46–§8.49 : (§8.46) contradiction MTAP arbitrée —
  S_sep voit une marche de niveau multi-flux réelle (réel 0,3378 contre
  nuls 0,1409 / 0,2663 / 0,2031), MC et Delta ne la mesurent pas, marge
  fragile. (§8.47) inversion immunitaire ICGC expliquée — le réel ne
  sépare pas (maxsep 0,2299), le nul graine 42 est haut (0,4500) mais
  ordinaire, le signal est une falaise diluée par les fenêtres, petit n.
  (§8.48) domination IMMROT expliquée — effet de corrélation
  contrôle↔flux (r = 0,954, R² = 0,909), pas une rupture. (§8.49)
  recomposition du MC (v6.3) rejetée — 31/48 rotations mais 4/8
  principales et HP35 +0,227, sous les critères gelés.

## Structure

- `livre-blanc-pdac-v6.md` — livre blanc complet (§8.1–§8.49).
- `universal_v6.2.0_cohen.py` — pipeline v6.2 (Cohen-d partout).
- `universal_v6.3.0_cohen.py` — proposition v6.3 REJETÉE (§8.49).
- `README.md`, `DATA_SOURCES.md`, `MANIFEST_SHA256.txt` — ce fichier,
  les sources des données, les SHA-256 de chaque fichier du dépôt.
- `provenance/` — 50 fichiers : protocoles gelés (`PROTOCOL_*.md`) et
  provenances (`PROVENANCE_*.md`) de chaque lot, plus
  `PUBLICATION_tlogNext.md`.
- `results/` — 11 tables vérifiées v6.1/v6.2/v6.3 (validation, phase 2,
  Delta, MC recomposé).
- `sections/` — sections §8.38–§8.49 du livre blanc, fichiers sources.
- `scripts/` — 98 scripts de construction des flux, d'extraction et
  d'analyse.
- `data_flux/` — 348 CSV/JSON : flux d'entrée des runs, tests directs,
  extraits ssep / v62_delta / §8.46–§8.49.

## Données brutes

Les matrices brutes (~2 Go) ne sont pas dans ce dépôt (limite snapshot
GitHub : 2 000 fichiers, 16 Mio). Voir `DATA_SOURCES.md` : chaque source
(URL, accès, hachage) et le script pour les re-télécharger et reconstruire
les flux de `data_flux/`.

## PDF

Le PDF du livre blanc (675 pages, binaire) est partagé séparément : les
snapshots GitHub n'acceptent que des fichiers UTF-8 de moins de 16 Mio
au total. Son SHA-256 est rappelé ci-dessus.

## Suite

La suite du travail (phase 2) se poursuit dans le dépôt
`tlogNext-pdac-phase2`, travail d'un autre agent — ce dépôt-ci reste
l'état vérifié du travail v6.2 au 19 novembre 2026.

Projet : FindPrint / TagPrint. Données ouvertes, code reproductible,
résultats négatifs rapportés comme les positifs.
