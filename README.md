# Cancer du pancréas (PDAC) — pipeline universel v6.2

Dépôt public de travail du projet PDAC : recherche d'un remède pour le
cancer du pancréas avec le pipeline universel de détection de ruptures
(v6.2), données ouvertes, protocoles gelés, résultats vérifiés.

## État au 19 novembre 2026

- Livre blanc : `livre-blanc-pdac-v6.md`, 609 pages (PDF partagé séparément),
  SHA-256 `10c7696321bb6c24833cd908df3c5396ab5f84a27a96139056535b30956e5317`,
  sections §8.1–§8.45. Le fichier Markdown ici a pour SHA-256
  `00f344b9fa717d21bfea7035f7bb8fd09d5f072d2367e6f9caec3d24d940af1a`
  (3 104 lignes).
- Pipeline : `universal_v6.2.0_cohen.py`, version de travail, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
  v6.1 = référence, v6 = historique.
- Les 3 verdicts §8.43–§8.45 : (§8.43) série MTAP ordonnée par la
  dépendance PRMT5 elle-même : NON — le nul sépare mieux que le réel.
  (§8.44) rotations des contrôles refaites sans le doublon de construction :
  37/48 sous (A) / 42/48 sous (B) — l'ordre est détecté, pas une rupture.
  (§8.45) test C, 175 tumeurs TCGA avec stade (3 exclues sans stade)
  la chaîne n'y réapparaît pas ; le seuil réel à 98,41 % est le stade IV
  lui-même, pas une découverte du pipeline.

## Structure

- `livre-blanc-pdac-v6.md` — livre blanc complet (§8.1–§8.45).
- `universal_v6.2.0_cohen.py` — pipeline v6.2 (Cohen-d partout).
- `README.md`, `DATA_SOURCES.md`, `MANIFEST_SHA256.txt` — ce fichier,
  les sources des données, les SHA-256 de chaque fichier du dépôt.
- `provenance/` — protocoles gelés (`PROTOCOL_*.md`) et provenances
  (`PROVENANCE_*.md`) de chaque lot, plus `PUBLICATION_tlogNext.md`.
- `results/` — tables vérifiées v6.1/v6.2 (validation, phase 2, Delta).
- `sections/` — sections §8.38–§8.45 du livre blanc, fichiers sources.
- `scripts/` — scripts de construction des flux et d'extraction.
- `data_flux/` — 295 CSV/JSON d'extraits + 5 JSON de provenance :
  flux d'entrée des runs, tests directs, extraits ssep / v62_delta.

## Données brutes

Les matrices brutes (~2 Go) ne sont pas dans ce dépôt (limite snapshot
GitHub : 2 000 fichiers, 16 Mio). Voir `DATA_SOURCES.md` : chaque source
(URL, accès, hachage) et le script pour les re-télécharger et reconstruire
les flux de `data_flux/`.

## PDF

Le PDF du livre blanc (609 pages, binaire) est partagé séparément : les
snapshots GitHub n'acceptent que des fichiers UTF-8 de moins de 16 Mio
au total. Son SHA-256 est rappelé ci-dessus.

## Suite

La suite du travail (phase 2) se poursuit dans le dépôt
`tlogNext-pdac-phase2`, travail d'un autre agent — ce dépôt-ci reste
l'état vérifié du travail v6.2 au 19 novembre 2026.

Projet : FindPrint / TagPrint. Données ouvertes, code reproductible,
résultats négatifs rapportés comme les positifs.
