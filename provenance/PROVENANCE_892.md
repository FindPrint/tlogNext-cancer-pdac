# PROVENANCE — §8.92 : vérification vopimetostat + daraxonrasib, phase 3

Date : 21 novembre 2026, ~11h15–12h00 EST.
Chantier §8.92, piste 2 du lot du 21 nov. 2026. Go de Zackary :
21 nov. 2026, 11h09.
Protocole gelé : `PROTOCOL_vopimetostat_verification_892.md`.
Auteur : TagPrint (coordinateur des 2 pistes).
Statut : veille documentaire — aucune donnée nouvelle mesurée ici.

## 1. Interrogation directe de ClinicalTrials.gov (API v2, 21 nov. 2026)

| # | Requête | Résultat | Reçu (SHA-256) |
|---|---|---|---|
| 1 | `api/v2/studies?query.term=vopimetostat&pageSize=20` | **2 études** : NCT07938463 (TAP-ALK, CBNPC, première publication 2026-11-16) et NCT07897734 (TNG462-C103, déjà au §8.80) | `ctg_vopimetostat_892.json`, `354da6c2664dc0b95ca4988d8a17f171f0105c2020891dff6c0b9af9fcb1e599` |
| 2 | `api/v2/studies?query.term=daraxonrasib&pageSize=20` | **16 études**, aucune n'est la phase 3 vopimetostat + daraxonrasib | `ctg_daraxonrasib_892.json`, `96e16a4dc6b690397b74276e127800e8fad8b3bf7b015650ac1b59fa9332833b` |
| 3 | `api/v2/studies?query.term=TNG462-C102` | **1 étude** : NCT06922591 (la phase 1/2 de la combinaison) | (réponse en ligne, non conservée — même étude que #4) |
| 4 | `api/v2/studies/NCT06922591` (TNG462-C102) | RECRUITING, première publication 2025-04-10, **dernière mise à jour 2026-10-23**, début 2025-05-31, fin primaire estimée 2027-06, effectif estimé 183, **aucun résultat publié** | `ctg_NCT06922591_892.json`, `d53ad88b45d4c7b97f9e108a63968a9277c1bc7e247ef7af74f34edf1293b7e7` |
| 5 | `api/v2/studies/NCT07938463` (TAP-ALK) | TNG462 + lorlatinib, CBNPC ALK+ MTAP-délété, Dana-Farber, NOT_YET_RECRUITING, première publication **2026-11-16**, début estimé 2027-04-30, 30 patients prévus | `ctg_NCT07938463_892.json`, `13d56de2be76a872002f24bfb96162fea9fb92f3b77da0c274579283cc860bf1` |

Détail NCT07897734 (TNG462-C103, déjà au §8.80) : première
publication 2026-10-27, NOT_YET_RECRUITING, début estimé 2026-11,
promoteur Tango Therapeutics, bras vopimetostat + ERAS-0015
(requête API, 21 nov. 2026 ; fiche non conservée en fichier, les
faits sont repris du §8.80 et confirmés par cette requête).

## 2. Dépôt SEC — Tango Therapeutics, formulaire 10-Q (source primaire)

- Formulaire 10-Q, trimestre clos le 30 septembre 2026, déposé le
  **9 novembre 2026**, accession SEC **0001193125-26-452634**,
  document `tngx-20260930.htm`.
  URL : https://www.sec.gov/Archives/edgar/data/1819133/000119312526452634/tngx-20260930.htm
- Extrait (Risk Factors, verbatim, conservé) :
  « While we are pursuing multiple pathways to obtain clinical
  supply of daraxonrasib for the planned trial, there is no
  assurance that we will be able to secure clinical supply of
  daraxonrasib on our anticipated timeline, on commercially
  reasonable terms, or at all. »
  Reçu : `tango_10q_supply_excerpt_892.txt`, SHA-256
  `e229daafe0d45d4b420e4537a3ae689c272e6a9bd4eb65718111d14782ed7466`.
- Le même 10-Q reprend le plan de phase 3 (randomisation 1:1,
  vopimetostat 200 mg + daraxonrasib 100 mg 1×/jour contre
  chimiothérapie standard, doubles critères ORR/PFS, OS secondaire
  clé, démarrage 1er semestre 2027) et le projet d'essai MTAP
  wild-type (~25 patients, 1er semestre 2027) — faits déjà au
  §8.80 via le communiqué du 9 nov. 2026, confirmés ici à la source
  primaire.
- Formulaire 8-K du 9 novembre 2026 (accession
  0001193125-26-452635, résultats T3) : repéré via les dépôts SEC,
  contenu repris du communiqué (déjà au §8.80).

## 3. Autres sources consultées (21 nov. 2026)

- Recherche web « vopimetostat daraxonrasib phase 3 trial NCT
  Tango Therapeutics Revolution Medicines November 2026 » :
  communiqués Tango du 9 nov. 2026 (résultats T3, repris par
  Morningstar/GlobeNewswire, Readthrough, VigiEye), 10-Q résumé
  par WhyMyStockMoved (12 nov. 2026) et FrontierPicks (13 nov.
  2026). Aucune annonce postérieure au 9 nov. 2026 sur la
  combinaison.
- Recherche web « SITC 2026 vopimetostat daraxonrasib pancreatic
  Tango presentation » : aucune présentation SITC sur la
  combinaison trouvée (seuls les communiqués ESMO de juin et
  d'octobre 2026 et leurs reprises) — confirme le §8.80.
- Section §8.80 du livre blanc (vérification du 21 nov. 2026,
  07h00–07h15 EST) : baseline reprise telle quelle, avec ses
  sources (liste complète en fin de §8.80) ; le présent chantier
  ne re-vérifie pas les faits du §8.80 un par un, sauf les points
  listés aux §1–2 ci-dessus.

## 4. Ce qui n'a PAS été fait

- Aucune donnée clinique mesurée ici (veille documentaire).
- Aucune recommandation clinique formulée.
- Aucun contact avec Tango, Revolution Medicines, la FDA ou un
  investigateur.
- Aucun accès payant (paywall) contourné ; aucune source non
  lisible affirmée.

## 5. Ce qui manque

- Le numéro NCT de la phase 3 vopimetostat + daraxonrasib
  (toujours inexistant au 21 nov. 2026).
- Une nouvelle coupe de données TNG462-C102 (toujours la coupure
  du 20 août 2026 ; dernière mise à jour du registre : 23 oct.
  2026).
- Toute donnée d'efficacité ou de sécurité post-ESMO sur la
  combinaison.

— Fin de la provenance §8.92. —
