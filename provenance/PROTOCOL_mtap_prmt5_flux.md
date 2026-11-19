# PROTOCOLE GELÉ — §8.43 : série MTAP avec la dépendance PRMT5 comme flux (19 nov. 2026)

Go : parent orchestrator, 19 nov. 2026 (chantier 1). Ce protocole est gelé
AVANT toute construction de CSV et tout run. Aucun paramètre ne change
après les résultats. Livre blanc NON édité directement (section dans un
fichier séparé `section_8.43_mtap_prmt5_flux.md`). PDF NON régénéré.
Rien poussé sur GitHub.

## 0. Question

Sortie de l'arbitrage §8.40 : le groupe MTAP-délété existe comme groupe
biologique (dépendance PRMT5 plus forte, −1,385 contre −1,010, p=0,0036)
mais n'est pas le groupe KRAS-fort, et la série ordonnée par CN MTAP
(§8.36) ne porte pas la chaîne. Hypothèse testée ici : au lieu d'ordonner
par la copie MTAP, ordonner par la dépendance PRMT5 elle-même — la chaîne
KRAS (bloc estomac/mucus qui chute + MUC16 qui monte) apparaît-elle sous
cet ordre ?

## 1. Données sources (vérifiées avant construction)

| Fichier | Dépôt | Taille (octets) | SHA-256 vérifié |
|---|---|---|---|
| `data/CRISPRGeneEffect.csv` | DepMap Public 24Q4, figshare article 27993248, fichier 51064667 | 428 678 699 | `3d8f3ec6dbf2db7ff834b79b508622ec0b226f3518003fe96ecf5a4fcf167e3b` |
| `data/Model.csv` | Même article, fichier 51065297 | 645 696 | `b7a0c1385e6cef30132b56aff61f1261d11e3f490490b355c430d32ee0dbdcfa` |

Valeurs : effets Chronos (plus négatif = plus dépendant). Aucune
imputation, jamais de valeur inventée.

## 2. Lignées : 45 adénocarcinomes pancréatiques

Critère : `OncotreePrimaryDisease == 'Pancreatic Adenocarcinoma'` dans
`Model.csv` (64 modèles), intersecté avec `CRISPRGeneEffect.csv` (45).
Les 19 adénocarcinomes absents de GeneEffect sont listés par le script
de construction.

Écart nommé d'avance par rapport à la consigne : les tests directs
§8.28/§8.29/§8.40 portaient sur 47 lignées pancréas (45 adénocarcinomes
+ 2 adénosquameux KP-3 ACH-000108 et L3.3 ACH-000685). La série de flux
utilise les 45 adénocarcinomes seuls — c'est l'ensemble des séries de
flux DepMap du projet (`pdac_depmap_fluxes.csv`, 45 lignes, §8.30) et le
nombre fixé par la consigne du chantier. Les 2 adénosquameux sont donc
hors série, et c'est dit ici, pas découvert après.

## 3. Flux : 9 des 12 gènes v4 — 3 exclus, pour des raisons mesurées

Les 12 gènes v4 sont PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2,
GSTM1, CEACAM5, CLCA1, MUC16. Vérification faite AVANT de geler (lecture
des en-têtes de `CRISPRGeneEffect.csv`, 17 917 colonnes) :

- **DPCR1 : ABSENT de la matrice Chronos 24Q4** (aucune colonne DPCR).
  DPCR1 n'a pas de mesure de dépendance CRISPR dans DepMap 24Q4.
- **MUC2 : ABSENT de la matrice Chronos 24Q4** (aucune colonne MUC2 ;
  la famille MUC présente : MUC1, MUC4, MUC5B, MUC6, MUC7, MUC12, MUC15,
  MUC16, MUC17, MUC20, MUC21, MUC22, MUCL1, MUCL3).
- **GSTM1 : PRÉSENT mais 8 NaN sur les 45 lignées** — exclu, sans
  imputation (règle du projet : aucun NaN dans les flux). Exclure les
  8 lignées au lieu du gène donnerait n=37 < 40 (minimum fast) : la
  série deviendrait impossible. Le gène est donc retiré, les lignées
  gardées.

**Flux retenus (9) : PGC (5225), REG4 (83998), CLDN18 (51208),
MUC17 (140453), CR2 (1380), KRT20 (54474), CEACAM5 (1048), CLCA1 (1179),
MUC16 (94025)** — valeurs Chronos par lignée, 0 NaN vérifié par le
script de construction (arrêt sinon).

Conséquence pour la chaîne : la chaîne KRAS de référence (§8.4) est
PGC / DPCR1 / CLDN18 / MUC16. **DPCR1 n'est pas testable en Chronos** :
la chaîne est testée sur 3 de ses 4 gènes (PGC, CLDN18, MUC16). C'est
une limite de la source, pas un choix d'analyse.

## 4. Ordre et contrôle

- **Ordre : Chronos PRMT5 (10419) croissant** — lignée la plus
  PRMT5-dépendante d'abord. PRMT5 est l'axe, JAMAIS un flux, et ne
  figure pas dans le CSV (comme KRAS dans la série DepMap §8.30).
  PRMT5 sur les 45 lignées (vérifié avant gel) : min −2,937, médiane
  −1,089, max −0,647 — toutes les lignées sont PRMT5-dépendantes à
  des degrés divers, ordre sans ex æquo (vérifié par le script).
- **Contrôle : `step`** (0..44, 1re colonne) — même convention que la
  série DepMap v6.2 (`results_fast_v62_depmap`, contrôle `step`, n=45).
  Le pipeline, sans `--control`, replie sur la 1re colonne numérique.
- **Cible : PGC** (1er flux, repli du pipeline — même convention que
  les séries MTAP §8.36 et DepMap §8.30).

## 5. CSV réel et nul

- Réel : `pdac_depmap_fluxes_prmt5.csv` — colonnes
  `step,PGC,REG4,CLDN18,MUC17,CR2,KRT20,CEACAM5,CLCA1,MUC16`, 45 lignes.
- Nul : `pdac_depmap_fluxes_prmt5_nul.csv` — mêmes lignes permutées,
  **graine 42** (convention du projet), `step` intact, flux permutés
  ensemble (même méthode que `build_fluxes_depmap.py`).
- Les deux SHA-256 sont notés dans la provenance. Longueur vérifiée :
  **45 lignes — le minimum fast v6.2 est 40, ça passe de 5 points.**

## 6. Runs

Pipeline : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
SHA-256 attendu `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(revérifié avant et après les runs ; le fichier n'est JAMAIS modifié).
Références : v6.0.0 `bb8bbdba…c0773`, v6.1 `2af5e5ce…c1c9`.
Mode **fast**, 2 runs (réel + nul), exit 0 exigés, via le lanceur
reprenable `run_v62_lot.sh` (manifeste `manifest_v62_prmt5flux.txt`,
journal `runs_v62_prmt5flux.log`), lancé par `systemd-run`
(jamais nohup). Sorties : `results_fast_v62_prmt5flux/` et
`results_fast_v62_prmt5flux_nul/`.

## 7. Critères de succès — écrits avant

Succès = **séparation réel > nul au-delà de la gigue mesurée 0,00**
(v6.2 : gigue L5 = 0, §8.37, 20/20 runs identiques ; en v6.2 aucun
forfait de gigue ne s'applique à MC best_score ni à max_separation,
PROTOCOL_v6.2.md §2). Indicateurs lus dans `master_results.json`
(même méthode que `mtap_reading.py` / `extract_ssep_838.py`) :

- cascade T_-2…T_+2 (%, pas) ;
- MC best_score et seuil ;
- **S_sep = max_separation × stability** (formule gelée PROTOCOL_v6.2.md
  §3, lus dans `best_config.metrics`) — indicateur principal de
  discrimination, avec max_separation et stability séparément ;
- Delta (tension holographique) ;
- L7a (direction, confiance) — vote interne, ne prouve rien seul ;
- falsification (`delta_vs_null`, statut) ;
- L7b, bruit, F1/F2 médians avant/après (méthode `mtap_reading.py`).

Un négatif est un résultat. Aucun consensus exigé entre flux ou
contrôles. Aucun seuil de séparation pré-enregistré au-delà de la
gigue 0,00.

## 8. Tests directs (harnais, hors pipeline — même méthode que §8.11/§8.34/§8.36)

Script `prmt5_flux_reading.py` (adaptation de `mtap_reading.py`,
mêmes fonctions `cohen_d`, `direct_tests`, `around_threshold`) :

- **Top-12 contre reste, flux par flux (d de Cohen)** : les 12
  lignées les plus PRMT5-dépendantes (premières lignes) contre les 33
  autres ; + = plus haut chez les 12 plus dépendantes. Mêmes unités
  que §8.4/§8.34/§8.36.
- **Spearman de chaque flux contre le rang** (rang 0 = plus dépendante).
- **Lecture autour de T_0** (pas du seuil MC réel, fenêtres ±20, d de
  Cohen après − avant), réel et nul.
- Référence chaîne KRAS (§8.4, axe KRAS) : PGC −0,89, DPCR1 −0,85,
  CLDN18 −0,46, MUC16 +0,64. La chaîne « apparaît » si le bloc
  (PGC, CLDN18) chute et MUC16 monte chez les 12 plus dépendantes,
  au-delà du nul — DPCR1 hors test (voir §3).
- **Autre chaîne ?** lecture complète des 9 flux : tout mouvement
  top-12 |d| ≥ 0,5 dépassant le maximum du nul est rapporté, quel
  que soit le gène.

## 9. Sorties attendues

- `build_fluxes_depmap_prmt5.py` (+ SHA) ;
- `pdac_depmap_fluxes_prmt5.csv` et `pdac_depmap_fluxes_prmt5_nul.csv`
  (+ SHA-256) ;
- `manifest_v62_prmt5flux.txt`, `runs_v62_prmt5flux.log` ;
- `results_fast_v62_prmt5flux/` et `results_fast_v62_prmt5flux_nul/`
  (`master_results.json` chacun) ;
- `prmt5_flux_reading.py`, `prmt5_flux_direct_tests.csv`,
  `prmt5_flux_extract.json` ;
- `section_8.43_mtap_prmt5_flux.md` (section complète, livre blanc
  non édité) et `PROVENANCE_mtap_prmt5_flux.md`.

## 10. Règles durables rappelées

Provenance toujours nommée (source complète, hachages, ce qui manque).
Seuls les données et runs du jour font les verdicts — les résultats
antérieurs (§8.28/§8.29/§8.36/§8.40) sont des attendus de comparaison,
jamais réimportés comme verdicts. Ne jamais modifier un code original.
