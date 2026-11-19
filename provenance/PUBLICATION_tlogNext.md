# Publication — nouveau dépôt (18 nov. 2026, 19h10, Zackary)

## Dépôt à utiliser pour toute publication future

**https://github.com/FindPrint/tlogNext-cancer-pdac**
— vérifié le 18 nov. 2026 : existe, commit initial `baf1e02f9218ac188680177ccd2dd7426be22dad`
(« Initial commit », ZivotPrint, 2026-11-19T00:07:23Z), lecture OK.

## Anciens dépôts — NE PLUS Y POUSSER

- `FindPrint/pancreatic-cancer-open-data-reproducibility` (dernier commit poussé `8c88810b`)
- `FindPrint/Code` (dernier commit poussé `70f52ad5`, v6.1)
— Zackary les a mis **PUBLICS** lui-même le 18 nov. 2026. Ne plus y pousser :
le pipeline doit rester privé, et le travail continue dans le nouveau dépôt.

## Règles pour la prochaine publication

- Rien n'est poussé sans le feu vert de Zackary (adoption v6.2 à présenter, pas automatique).
- Avant de pousser dans `tlogNext-cancer-pdac`, vérifier que l'App GitHub
  (meta-muse-ai) est installée sur ce dépôt — sinon le push échouera en 403
  et il faudra le dire à Zackary (lien d'installation :
  https://github.com/apps/meta-muse-ai/installations/new).
  La lecture seule ne prouve PAS l'installation pour l'écriture.
- Contenu à publier quand le moment viendra : PDF régénéré avec §8.37,
  v6.2 si adoptée (sinon v6.1, déjà dans Code).
- Le PDF binaire ne va dans AUCUN dépôt (limite snapshot) ; pas de Release
  via le connecteur.

## Tentative du 19 nov. 2026 — NON FAITE (approbation expirée)

- Adoption v6.2 faite le 19 nov. 2026 (~05h47, go « Lance tout cela ») ;
  PDF régénéré avec §8.37 (500 pages, SHA `0d53ad1a…`, puis reconstruit
  avec la ligne « Ce qui manque » corrigée).
- Poussée tentée le 19 nov. 2026 vers `tlogNext-cancer-pdac` : approbation
  d'écriture expirée sans réponse après ~30 min (`approval_expired`,
  approval_id `connector-attempt-a6d281f8…`) — rien poussé, tête distante
  inchangée (`baf1e02f`). Snapshot prêt et vérifié (8 fichiers,
  991 746 octets, UTF-8, dans `/tmp/push_v62/` — à reconstruire depuis
  les sources locales avant une nouvelle tentative : le dossier /tmp
  est éphémère).
- À retenter après une nouvelle approbation de Zackary, sans relancer
  en boucle.
