# PROVENANCE — UNIVERSAL_LOG v6.2.0 « hachage stable L5 »

Date : 18 novembre 2026, ~18h15–18h16 (heure de Montréal).
Auteur : TagPrint (sous-agent), étape 2 de la construction v6.2 (go de Zackary
du 18 nov. 18h07).
Statut : **copie construite, compilée, diff vérifié ; AUCUN run de validation
lancé (étape suivante) ; AUCUN push GitHub ; adoption comme version de travail
= go de Zackary, NON DÉCLARÉE ici. La v6.1 reste la version de travail.**

## 1. D'où vient v6.2

- **Parent :** `~/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py`,
  SHA-256 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`,
  623 495 octets, VERSION_MASTER `v6.1.0-L7aL7b-CohenD-short`.
- **Grand-parent v6 jamais modifié :** SHA-256
  `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`,
  622 526 octets — revérifié inchangé APRÈS construction (voir §4).
- **Construction :** `~/workspace/runs/pdac-v6/build_v6.2.py`,
  SHA-256 `5348636e0633b2b25a418bfa162adbec9277025fff72565f4bfb2c6efd951fa0`
  — 3 remplacements exacts avec assertions et comptage, miroir de
  `build_v6.1.py`.
- **Copie v6.2 :** `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
  624 157 octets, VERSION_MASTER `v6.2.0-L7aL7b-CohenD-short`.
- **Conception gelée avant code :** `~/workspace/runs/pdac-v6/PROTOCOL_v6.2.md`
  (696 lignes), SHA-256 vérifié
  `6e9324a2f2ff0720c6dd23d403a281e7f15bf5c7b4a8d04f8bba41ed7f84dfad`.

## 2. Écart de SHA du protocole — signalé, pas corrigé en silence

L'agent qui a écrit `PROTOCOL_v6.2.md` a annoncé un SHA `fb27b39a…` qui NE
correspond PAS au fichier : le SHA-256 mesuré avant travaux est
`6e9324a2f2ff0720c6dd23d403a281e7f15bf5c7b4a8d04f8bba41ed7f84dfad`
(vérifié par `sha256sum`, et revérifié après construction — identique).
C'est le SHA mesuré qui fait foi ici ; l'annonce `fb27b39a…` est consignée
comme erronée. Le contenu du protocole suivi est celui du fichier mesuré
(§2.2, remplacement gelé littéral).

## 3. Défaut mesuré (v6.1) et changements gelés

Cause de la gigue L5 (±0,07, phase 2 §8.35, `PROVENANCE_v6.1.md` §5) :
`level_complexity` graine les chemins MC avec `int(seed) + (hash(metric) % 1000)`
(ligne 8985 de la v6.1) et le hachage Python des chaînes est aléatoire par
processus. Vérifié avant travaux : exactement 1 occurrence de `hash(` dans
toute la v6.1, 0 occurrence de `hashlib`.

- **H1 — import** : `import hashlib` ajouté ligne 392, bloc IMPORTS
  (après `import sys` / `import json`).
- **H2 — ligne 8985 (8986 après H1)** : ancien texte exact
  `int(seed) + (hash(metric) % 1000)` remplacé par le texte gelé
  `int(seed) + (int.from_bytes(hashlib.sha256(metric.encode('utf-8')).digest()[:8], 'little') % 1000)`.
  Seule la graine MC de L5 change ; la formule `% 1000` et tout le reste de
  la ligne sont identiques.
- **V — version** : `VERSION_MASTER` `v6.1.0-L7aL7b-CohenD-short` →
  `v6.2.0-L7aL7b-CohenD-short` (ligne 9212) + note d'en-tête v6.2
  (10 lignes) : seul changement, hachage stable L5 ; renvoi au
  protocole §2.2. La note v6.1 reste en dessous, comme la v6.1 avait
  conservé l'historique précédent.

**Ne changent pas :** estimateurs (29), cascade, seuils, Delta, scores MC
(best_score, max_separation), modes, Cohen-d, chemin predict/MC, tout le
reste du code. S_sep (§3 du protocole) et l'élucidation Delta (§4) sont des
lectures hors pipeline — aucun code pour ça dans v6.2.

## 4. Vérifications faites (construction)

- Pré-conditions avant copie : SHA v6.1 source = `2af5e5ce…c1c9` (complet
  ci-dessus) ; `hash(` = 1 occurrence ; `hashlib` = 0 occurrence.
- Script : 3 remplacements, chacun exactement 1 occurrence de l'ancien
  texte, 1 remplacement ; assertions post-construction toutes passées.
- `python3 -m py_compile universal_v6.2.0_cohen.py` : exit 0.
- Après construction : `grep -n "hash("` = **0 occurrence** ;
  `grep -n "hashlib"` = **exactement 2 occurrences** (import ligne 392 +
  usage ligne 8986) ; `hash(metric)` absent ; ancienne version absente.
- `diff -u` v6.1 → v6.2 : **exactement 3 hunks, vérifiés à la main** —
  (1) `+import hashlib`, (2) la ligne du seed L5, (3) VERSION_MASTER +
  note d'en-tête. Aucune autre ligne ne diffère.
- v6.1 et v6 revérifiées INCHANGÉES après travaux (SHA complets §1 ;
  horodatages des fichiers inchangés : v6.1 du 16 nov., v6 du 15 nov.).
- Incident de construction, consigné : la première exécution de
  `build_v6.2.py` s'est ARRÊTÉE sur assertion — la note d'en-tête
  contenait elle-même la chaîne littérale `hash(metric)`, ce qui aurait
  violé l'exigence « 0 occurrence de `hash(` ». La note a été reformulée
  (sans la chaîne littérale), le script relancé : construction propre.
  Le SHA v6.2 final est celui de la seconde construction
  (`f07567c4…ec3abf`).

## 5. Ce qui n'a PAS été fait (hors étape 2)

- Aucun run de validation (10 runs fast × 2 répétitions, §5 du protocole)
  — c'est l'étape suivante, sur go séparé.
- Aucun run du pipeline d'aucune sorte avec la v6.2 ; la gigue L5 = 0
  n'est PAS encore mesurée, seulement attendue.
- Aucun push GitHub ; aucune modification de la v6.1 ni de la v6.

## 6. Fichiers

- `~/workspace/runs/pdac-v6/PROTOCOL_v6.2.md` (conception gelée, SHA §1)
- `~/workspace/runs/pdac-v6/build_v6.2.py` (construction, 3 remplacements)
- `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py` (copie, SHA §1)
- `~/workspace/runs/pdac-v6/PROVENANCE_v6.2.md` (ce fichier)

## 7. Addendum — adoption, 19 novembre 2026, ~05h47 (heure de Montréal)

- **Go de Zackary :** « Lance tout cela » (feu vert pour les 3 chantiers :
  adoption v6.2, PDF, GitHub).
- **Statut nouveau : la v6.2 devient la version de travail ; la v6.1
  devient la référence ; la v6.0.0 reste la référence historique.**
  Tous les runs PDAC suivants utilisent la v6.2.
- **SHA revérifiés inchangés le 19 nov. 2026 avant adoption**
  (`sha256sum`, fichiers non modifiés depuis leur construction) :
  - v6.0.0 `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`
    (622 526 octets)
  - v6.1.0 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`
    (623 495 octets)
  - v6.2.0 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
    (624 157 octets)
- **Validation rappelée (§8.37 du livre blanc) :** 20/20 runs exit 0,
  cascades identiques à la v6.1 sur 10/10, gigue L5 mesurée = 0,0000 ;
  S_sep 6/8 = max_separation v6.1 (mêmes paires) ; Delta non élucidé
  (222 runs, meilleur 80,2 % paire / 61,7 % valeur < 90 %).
  La v6.2 ne sépare pas mieux que la v6.1 ; le gain adopté est le
  déterminisme.
- **Consignation :** en-tête du livre blanc, ligne 43 au §7, §8.37
  (intro, §8.37.5, provenance « Ce qui manque ») et journal §10 (entrée
  du 19 nov. 2026).
- **PDF et GitHub :** PDF régénéré le 19 nov. 2026 avec le §8.37 (chaîne
  `.src/`, WeasyPrint 70.0) : **500 pages A4, 10 398 134 octets, SHA-256
  `0d53ad1aa66ae332516ba14fa4a84175f4d560695c5811f7221039669dbf82ef`**
  (ancien 471 pages, 10 266 464 octets, SHA `12c36228…`) ; couverture
  corrigée (date 19 nov. 2026, §8.1–§8.37, nouveau dépôt) ; §8.37 vérifié
  présent par lecture du PDF.
- **Poussée GitHub NON FAITE, 19 nov. 2026 :** approbation d'écriture
  expirée sans réponse après ~30 min d'attente (`approval_expired`,
  approval_id
  `connector-attempt-a6d281f83b6bb0a4878e3f5593c007415af7b191885e3d5ca50422fba2dd1f7f`) ;
  rien n'a été poussé, rien n'a changé sur GitHub (tête distante
  vérifiée inchangée après l'expiration : `baf1e02f`, commit initial).
  Snapshot prêt et vérifié (`/tmp/push_v62/`, 8 fichiers, 991 746
  octets, UTF-8 ; livre blanc SHA `9ccc6570…e599`) — à retenter après
  une nouvelle approbation de Zackary, sans relancer en boucle.
  La lecture seule préalable avait réussi (tête `baf1e02f`, seul un
  `LICENSE` à la racine) ; elle ne prouve pas l'installation de l'App
  pour l'écriture.
- **PDF reconstruit le 19 nov. 2026 :** le premier PDF (SHA `0d53ad1a…`)
  portait au §8.37 une ligne « Ce qui manque » affirmant la poussée
  GitHub faite — fausse, l'approbation ayant expiré. Ligne corrigée
  dans le livre blanc, PDF reconstruit avec la chaîne `.src/`
  (WeasyPrint 70.0) — **PDF reconstruit, 19 nov. 2026 : 501 pages A4,
  10 404 235 octets, SHA-256
  `640c7a6e285790562b2f1d43978722cb071a96e92d6e78e5c89bf76b0da83889`**
  (premier PDF du jour : 500 pages, 10 398 134 octets, SHA
  `0d53ad1a…` — retiré, il portait la ligne fausse). §8.37, adoption
  et ligne « Ce qui manque » corrigée vérifiés présents par lecture
  du PDF reconstruit (`pdftotext`, 60 occurrences de « 8.37 »).

## 8. Addendum — §8.38 et §8.39, 19 novembre 2026, ~06h40 (heure de Montréal)

- **Fusion au livre blanc :** sections `section_8.38_ssep.md` (SHA `92e62bbb…`, 344 lignes) et `section_8.39_delta.md` (SHA `e9f1f1ca…`, 369 lignes) fusionnées par le coordinateur dans `livre-blanc-pdac-v6.md` (lignes 44–45 au §7, entrée de journal §10). Incident consigné : la première fusion avait perdu les deux titres de section (bug du script de fusion — `lines[0]` remplacé mais jamais recopié dans la sortie) ; titres réinsérés et ligne « Statut : section prête à insérer » retirée, fusion revérifiée (2176 lignes, SHA livre blanc `937d565487248ab49cfb5a6973e03ab6ed5e72ec90bae79992653b8e3b86420c`).
- **PDF régénéré le 19 nov. 2026 : 521 pages A4, 10 502 925 octets, SHA-256 `673f3de56d871e73136912eb76d75dfb890ab286ffa2c3591701905e74ada63e`** (ancien 501 pages, 10 404 235 octets, SHA `640c7a6e…`). Chaîne `.src/` : `build_appendix.py` puis `build_pdf.py` (qui n'écrit que `index.html`), puis rendu WeasyPrint 70.0 en CLI (`weasyprint index.html ../livre-blanc-pdac-v6.pdf`) — le rendu n'est pas dans `build_pdf.py`. Deux échecs de lancement consignés : `markdown` introuvable puis chemin `/root/workspace` — corrigés par `HOME=/home/hatch` et `PYTHONPATH=/home/hatch/.local/lib/python3.12/site-packages` (venv WeasyPrint sans `markdown`, python système sans `weasyprint`). Couverture corrigée : §8.1–§8.39. Vérifié par lecture du PDF (`pdftotext`) : §8.38 présent (66 occurrences de « 8.38 »), §8.39 présent (45 occurrences de « 8.39 »).
- **Poussée GitHub : TOUJOURS EN ATTENTE.** Première tentative (chantier 1) expirée (`approval_expired`, ~30 min sans réponse) ; rien n'a été poussé, tête distante `tlogNext-cancer-pdac` toujours `baf1e02f` (commit initial). Le snapshot doit être reconstruit depuis les fichiers locaux (le livre blanc a changé depuis : §8.38/§8.39 + PDF 521 pages) avant toute nouvelle tentative, après une nouvelle approbation de Zackary. Les 8 chemins de dépôt restent les mêmes ; le binaire PDF n'y va pas.
- **SHA des 3 pipelines revérifiés à la fin :** v6 `bb8bbdba…c0773`, v6.1 `2af5e5ce…c1c9`, v6.2 `f07567c4…` — inchangés, aucun code modifié.

## 9. Addendum — §8.40–§8.42, PDF régénéré, 19 novembre 2026, ~08h05 (heure de Montréal)

- **Go :** Zackary, « Allez s'y », 19 nov. 2026 ~08h05 (régénérer le PDF, puis pousser sur GitHub ; disponible pour approuver la carte vite). Livre blanc inchangé depuis le §8.42 : SHA `de3aa31618504989f4de7b1b43e197cf796549b20e8701fe0fce2385963a4029`, 2 750 lignes, §8.1–§8.42.
- **Couverture mise à jour dans `.src/build_pdf.py` (chaîne, pas le livre blanc) :** plage §8.1–§8.39 → §8.1–§8.42 ; ligne « Pipeline » complétée (v6.2 version de travail, SHA `f07567c4…`, gigue 0 ; v6.1 référence, v6 référence historique) ; note de bas de page corrigée — le pipeline n'est plus « privé » : v6.2 public dans tlogNext depuis le 19 nov. 2026, par décision de Zackary (anciens dépôts rendus publics par lui le 18 nov. 2026). L'annexe D embarque toujours le code intégral de la v6.0.0 + les scripts du projet (dont `build_v6.2.py`) ; les codes v6.1/v6.2 ne sont pas embarqués dans le PDF — ils sont dans le dépôt GitHub.
- **PDF régénéré le 19 nov. 2026 : 565 pages A4, 10 721 134 octets, SHA-256 `996434e56937720e03d225d00af06bd70294d55f5b00724853894ee57e0f7bc4`** (ancien 521 pages, 10 502 925 octets, SHA `673f3de5…`). Chaîne `.src/` : `build_appendix.py` (appendix.html 13 744 313 caractères) puis `build_pdf.py` (index.html 14 202 998 caractères), puis rendu WeasyPrint 70.0 en CLI (`/home/hatch/workspace/venv_weasyprint/bin/weasyprint index.html ../livre-blanc-pdac-v6.pdf`, ~4 min). Vérifié par lecture du PDF (`pdftotext`) : §8.40 présent (47 occurrences de « 8.40 »), §8.41 présent (44), §8.42 présent (39) ; couverture « §8.1–§8.42 » présente.
- **Vérification anti-fausse-poussée :** le PDF ne contient AUCUNE affirmation de poussée non faite (aucune occurrence de « e0e282d9 »). Réserve honnête, sens inverse : le journal (§10) dit encore la poussée tlogNext « en attente » — texte du livre blanc figé au SHA `de3aa316…`, alors que la poussée du contenu §8.1–§8.39 a réussi le 19 nov. 2026 à 06h51 (commit `e0e282d9`) ; le livre blanc ne porte aucune entrée de journal pour cette poussée à ce jour — à ajouter au prochain tour, elle entrera dans le PDF à la régénération suivante (règle établie).
- **SHA des 3 pipelines revérifiés :** v6 `bb8bbdba…c0773`, v6.1 `2af5e5ce…c1c9`, v6.2 `f07567c4…` — inchangés, aucun code modifié.

## 10. Addendum — §8.43–§8.45, PDF régénéré, 19 novembre 2026, ~20h25 (heure de Montréal)

- **Go :** Zackary, « Fait tes 3 propositions, je reviens plus tard », 19 nov. 2026 ~08h16 (3 chantiers : série PRMT5 §8.43, rotations sans doublon §8.44, test C stade §8.45) ; puis règle permanente « Toujours github et pdf !!! » (19 nov. 09h45) — après chaque lot de sections, régénérer le PDF et pousser sur GitHub. Livre blanc fusionné par le coordinateur : SHA `00f344b9…` (3 104 lignes), lignes 49–51 au §7, 3 entrées de journal ; une ligne « Statut : section prête à insérer » résiduelle au §8.41 retirée ; une attribution de go erronée au §8.44 corrigée (le go était « Fait tes 3 propositions », pas « Lance tout cela »).
- **Couverture mise à jour dans `.src/build_pdf.py` (chaîne, pas le livre blanc) :** plage §8.1–§8.42 → §8.1–§8.45.
- **PDF régénéré le 19 nov. 2026 : 609 pages A4, 10 964 223 octets, SHA-256 `10c7696321bb6c24833cd908df3c5396ab5f84a27a96139056535b30956e5317`** (ancien 565 pages, 10 721 134 octets, SHA `996434e5…`). Vérifié par lecture du PDF (`pdftotext`) : §8.43 (61 occurrences), §8.44 (73), §8.45 (23) ; couverture « §8.1–§8.45 » présente ; A4 confirmé. Premier rendu en échec (index.html introuvable — il est écrit dans `.src/`, pas dans le dossier du livre blanc) ; relance depuis `.src/` réussie.
- **Vérification anti-fausse-poussée :** le PDF ne contient aucune affirmation de poussée non faite — la seule mention du commit `0a5ef225` est l'entrée de journal historique du 19 nov. 08h14, vraie.
- **SHA des 3 pipelines revérifiés :** v6 `bb8bbdba…c0773`, v6.1 `2af5e5ce…c1c9`, v6.2 `f07567c4…` — inchangés, aucun code modifié.
