# PROTOCOLE GELÉ — Étude de discrimination réel / nul (phase 2)

Date : 16 novembre 2026.
Statut : **PROTOCOLE ÉCRIT, PRÊT À EXÉCUTER. Exécution et tout changement de
code attendent le go de Zackary après la phase 1 (v6.1 validée).**
Auteur : TagPrint, sur ordre de Zackary (mandat « valoriser le pipeline »,
16 nov. 17h45 ; « Teste mon pipeline », 16 nov. 18h13).

## 1. Question

Quels indicateurs dérivés du pipeline séparent une série réelle de son nul
permuté (graine 42) — et lesquels ne séparent pas ?

Contexte mesuré : le 16 nov., 18 runs v6 (immunitaire 8, PARP 2, ATR 2,
pan-cancer 4, ICGC 2), tous exit 0, AUCUN ne sépare réel et nul sur Delta ou
MC. Sur HP35 (n = 1000) le pipeline sépare nettement (MC max 1,772 réel
contre 0,121 nul) ; sur TCGA v4 il sépare par la falsification (delta 0,849)
et L7a DOWN 86,3 % contre UP 45,1 % au nul. Sur DepMap v6.1 (n = 45) :
MC 0,3615 contre 0,3499, Delta 1,93 contre 1,69 — pas de séparation.

## 2. Paires réel / nul (toutes construites, sorties v6 et/ou v6.1 sur disque)

| Paire | n | v6 | v6.1 |
|---|---|---|---|
| HP35 (repliement) | 1000 | oui | oui (validée) |
| TCGA v4 | 178 | oui | oui (validée) |
| TCGA v1 / v2 / v3 | 178 | oui | lot étendu en cours |
| TCGA v4 rotations (4 contrôles, 15 nov.) | 178 | oui | lot étendu en cours |
| GSE71729 (+ v4b, v4c, parp) | 145 | oui | lot étendu en cours |
| GSE62452 (+ v4b) | 69 | oui | oui (v6.1 validée) / lot étendu |
| ICGC | 70 | oui | oui (validée) |
| CPTAC UMich / BCM | 63 / 52 | oui | lot étendu en cours |
| Immunitaire TCGA / GSE71729 / GSE62452 / ICGC | 178 / 145 / 69 / 70 | oui | lot étendu en cours |
| PARP TCGA (+ GEO parp) | 178 / 145 | oui | lot étendu en cours |
| ATR TCGA | 178 | oui | lot étendu en cours |
| LUAD / COAD | 515 / 285 | oui | lot étendu en cours |
| **DepMap CRISPR** | **45** | bloqué (min 50) | **oui (validée)** |
| Rotations v6.1 (TCGA v4, DepMap, immunitaire, PARP — 48 paires) | 178 / 45 / 178 / 178 | non (4 seulement) | rotations en cours |

Nul de chaque paire : lignes permutées, graine 42, colonne de contrôle intacte
(convention du projet depuis le 15 nov.).

## 3. Indicateurs testés (tous lus dans `master_results.json`, aucun nouveau run)

Pour chaque paire, extraire réel et nul :

1. **Delta** (`holographic_tension_state` / tension) — réel contre nul.
2. **MC optimum** (seuil %) et **MC best_score** — réel contre nul.
3. **max_separation** — réel contre nul.
4. **Position de T_0** (cascade, en %) — distance |T_0 réel − T_0 nul|.
5. **Delta de falsification** : `delta_vs_null` (falsification_vs_null) —
   disponible seulement quand le diagnostic de bruit est complet (n ≥ 75) ;
   noter « indisponible » sous n = 75, ne pas imputer.
6. **Cohérence par flux à T_0** : fraction des flux dont le d de Cohen
   (fenêtre ±20, ou ±10 si n < 100 — méthode `per_flux_reading.py`) a le même
   signe que le vote L7a ; et le |d| médian des flux à T_0.
7. **L7a** : direction + confiance — réel contre nul.
8. **Écart cascade complet** : somme des |Δ| sur les 5 positions T_-2…T_+2.

## 4. Critère de succès — écrit d'avance

Un indicateur **sépare** une paire si :
- (a) l'écart réel–nul dépasse la gigue run-to-run connue de l'indicateur
  (L4/L7a : ±0,07 mesuré sur HP35, §5 de PROVENANCE_v6.1 ; cascade et Delta :
  déterministes, gigue 0 — tout écart est un écart), **ET**
- (b) la direction de l'écart est la même dans les deux sens attendus
  (ex. MC réel > MC nul, ou |T_0 réel − T_0 nul| > 0) — pas de direction
  imposée a priori, mais la direction observée doit être **cohérente entre
  paires** (même signe d'écart sur ≥ 6 des 8 paires principales : HP35,
  TCGA v4, GSE71729, GSE62452, ICGC, immunitaire TCGA, PARP TCGA, DepMap).

**Verdict écrit d'avance :**
- « Sépare sur toutes les paires » si l'indicateur tient (a) + (b) sur les
  8 paires principales.
- Sinon : « Sépare sur X/8 paires : [liste], échoue sur [liste] » — avec les
  chiffres, sans arrondir le verdict.
- Si aucun indicateur ne sépare sur ≥ 6/8 : verdict « le pipeline, en l'état,
  ne sépare pas réel et nul sur ces séries PDAC » — et la liste des
  indicateurs testés reste le résultat (un négatif mesuré, pas un échec caché).

## 5. Ce que l'étude ne fera pas

- Aucun changement de code avant le verdict et le go de Zackary.
- Aucune re-définition du nul après avoir vu les résultats (graine 42,
  permutation des lignes — gelé).
- Aucune sélection d'indicateur après coup : la liste du §3 est gelée.
- Aucune affirmation clinique : l'étude porte sur l'instrument, pas sur le cancer.

## 6. Exécution (quand le go sera donné)

1. Attendre la fin des lots v6.1 (étendu + rotations) — toutes les sorties
   v6.1 doivent être sur disque.
2. Extraire avec `extract_v61_lot_compare.py` (à écrire : compare v6.1 et v6
   par série, réel + nul) + `per_flux_reading.py` pour l'indicateur 6.
3. Produire la table des 8 indicateurs × 8 paires principales (+ paires
   secondaires en annexe).
4. Consigner au livre blanc (§8.34) et proposer, **seulement si l'étude le
   justifie**, une piste de changement de code (v6.2) — avec conception gelée
   séparée et nouveau cycle de validation.
