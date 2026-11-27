# PROVENANCE — §8.100 : fusion des cinq dépôts, archivage, smoke-test (27 novembre 2026)

Chantier A du 27 nov. 2026. Rédaction seule : aucune fusion dans
le livre blanc, aucun PDF, aucun push GitHub, aucune Release,
aucune modification du pipeline. Formulation en analyse
uniquement, jamais de prédiction ; aucun jugement clinique.

## 1. Sources

### 1.1 Les cinq dépôts (têtes avant fusion, vérifiées le 27 nov. 2026 par API + connecteur)

| Dépôt | Tête | Date de la tête | URL |
|---|---|---|---|
| FindPrint/tlogNext-cancer-pdac (principal, PUBLIC) | `48b9e69f` | 27 nov. 2026 13:36:38 UTC | https://github.com/FindPrint/tlogNext-cancer-pdac |
| FindPrint/tlogNext-cancer-pdac-suite (PRIVÉ) | `14bff2ff` | 27 nov. 2026 13:39:19 UTC | https://github.com/FindPrint/tlogNext-cancer-pdac-suite |
| FindPrint/tlogNext-pipeline-actions (PUBLIC) | `0dba356` | 23 nov. 2026 11:59:12 UTC | https://github.com/FindPrint/tlogNext-pipeline-actions |
| FindPrint/pancreatic-cancer-open-data-reproducibility (PUBLIC) | `8c88810b` | 18 nov. 2026 23:06:52 UTC | https://github.com/FindPrint/pancreatic-cancer-open-data-reproducibility |
| FindPrint/Code (PUBLIC) | `1ef321a` | 27 nov. 2026 12:28:43 UTC | https://github.com/FindPrint/Code |

### 1.2 Tête après fusion et archivage (vérifiées par le parent, non re-vérifiées ici)

- Dépôt unique : `FindPrint/tlogNext-cancer-pdac`, tête finale
  `0aaf7116a43d37cfafe5be883e9d6cb343935ea7`.
- Archivage le 27 nov. 2026, `archived:true` vérifié par API
  sur les 3 dépôts : suite, tête `f2bfdf31` (README de
  redirection) ; actions, tête `111b1e66` ; repro, tête
  `a7a98d43`. Jamais supprimés, lecture seule.

### 1.3 Documents sources lus pour rédiger cette section

- `~/workspace/runs/pdac-v6/coordinateur_fusion_20261127_etat.md`
  — état complet de la fusion (décisions, tableau maître,
  écarts MANIFEST, test_biophysique, commits, points ouverts).
- `~/workspace/push_fusion_build/tableau_fusion_20261127.md`
  (SHA `0a3eb186…`) et `tableau_fusion_20261127.csv`
  (SHA `527998df…`) — tableau maître fichier → destination
  → SHA-256, 59 nouveaux chemins + README.md mis à jour.
- `~/workspace/runs/pdac-v6/smoke_test_fusion_20261127/COMPARAISON_SMOKE_FUSION_20261127.md`
  — comparaison du smoke-test de bascule (run GitHub nº 1,
  ID 46014415035).
- Livre blanc sur disque
  `~/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md`
  — format de la §8.99 (titre, verdict d'abord, sous-sections,
  marqueur de fin) et ligne §7 nº 105 ; chiffres MTAP/PRMT5
  (§8.28–§8.50) et addendum Cox §8.12 (27 nov. 2026).

## 2. Nature des lignes

- **Commits, vérifications SHA, archivages, smoke-test :**
  lignes d'archive et de vérification, pas de runs pipeline.
  **Aucun run pipeline dans ce chantier.** Aucune donnée
  biologique nouvelle, aucune mesure, aucun échantillon.
- **Décisions de Zackary (27 nov. 2026, 08h47) :** mots
  humains rapportés par le coordinateur, pas des mesures
  instrumentales.
- **Scores du smoke-test :** sorties du pipeline v6.2
  (SHA `f07567c4…`, inchangé) exécuté sur GitHub Actions
  (runner, 15,6 Go) et en local (2 Go) ; comparaison feuille
  par feuille par `compare_smoke_fusion.py`.
- **SHA-256 cités :** empreintes de fichiers, produites par
  hachage cryptographique des contenus exacts ; les préfixes
  tronqués (`…`) renvoient aux SHA complets consignés dans
  le tableau maître ou dans les fichiers sources cités.

## 3. Comment chaque valeur a été produite

- **7 commits de fusion :** construits par le script
  `build_fusion_snapshots.py` (SHA `9f8ac261…`, snapshots
  `snap_c1/` … `snap_c7/` + `commitN.paths`) puis poussés
  par le parent. Commit 1 `69d6a561` (v6.0 + v6.1 à la
  racine) ; commit 2 : 4 commits navigateur `f43d4f0` /
  `efaf456` / `4222803` / `83f378a` (tête intermédiaire
  `83f378a5dfff56cc05218869f94bc2b84a7d85cf`) — créés via le
  navigateur car l'API GitHub refuse les fichiers de
  workflows à l'App (403 « Resource not accessible by
  integration ») ; commit 3 `53d0053e` (protocoles) ;
  commit 4 `e381b80b` ; commit 5 `152e918a` ; commit 6
  `a34f09d4` ; commit 7 `0aaf7116`.
- **MANIFEST régénéré (1 718 entrées) :** 1 651 + 8
  réconciliés + 59 nouveaux ; distant = local bit à bit,
  SHA-256 `309008e0…` (valeur communiquée par le parent).
- **60/60 nouveaux chemins vérifiés par blob SHA, 0 écart :**
  chaque SHA re-calculé depuis le staging par le
  coordinateur ; tableau maître généré par
  `generate_tableau_fusion.py` (SHA `3e062e9c…`).
- **Écarts MANIFEST (9 fichiers) :** comparaison arbre
  principal à `48b9e69f` (1 666 entrées : 1 660 blobs +
  6 arbres) contre MANIFEST (1 651) ; contenu des 9
  fichiers vérifié bit à bit (copies dans `tree_only/`).
- **`test_biophysique_input.csv` :** copie locale depuis
  actions @ `0dba356`, SHA re-vérifié
  `6b656540598579a37cbc97c9dfbee26bf6186611f84f397cf9e7e6f1e88bb35e`
  (90 716 o) ; concordance 10/10 des autres CSV E1/E2 avec
  les `real_sha` des YAML.
- **Smoke-test :** run GitHub Actions `pipeline-smoke-test`
  nº 1, ID 46014415035, 27 nov. 2026 09:16 HNE, 8 min 11 s,
  Success ; artefact `master-results-tcga-v4.zip`
  (2 100 650 o, SHA-256
  `7b44f33198432152f897631d303124c0a75e9ad5445f019bde45dc12d29b50e4`) ;
  scores de décision comparés bit à bit aux références
  locales `runs/pdac-v6/results_fast_v62_tcga_v4[_nul]/master_results.json`.
  Gigue Delta (+0,14 %) : écart observé entre deux
  plateformes, cause attribuée aux tirages MC /
  permutations (les entrées sont vérifiées par SHA par le
  workflow lui-même, le code est identique) ; référence
  run-à-run : deux runs locaux entre eux ne diffèrent que
  de 10 clés.
- **README_EN.md :** rédigé le 27 nov. 2026 (traduction
  fidèle du README FR), SHA-256
  `8815e25005705a989c9c2061187a4d5ac156f3ad8618e6e1e9dcbbb506ef683f`,
  30 733 o ; chiffres MTAP/PRMT5 vérifiés contre le livre
  blanc (§8.28–§8.50 : −1,385 contre −1,010, p=0,0036 ;
  CDKN2A fixé p=0,76).
- **README FR :** reconstruction chirurgicale par
  `rebuild_readme_fr_20261127.py` (SHA `03de66f2…`),
  SHA `4d9ddcd6…`, 30 653 o.
- **Déduplication repro :** 223 candidats, 48 uniques
  (4 799 757 o), 175 doublons ; 0 collision avec les
  7 fichiers hors MANIFEST ; 0 fichier non UTF-8.
- **Annotation Cox :** `check_cox_tcga_results.txt`
  (68 lignes, SHA avant annotation
  `c50fb788915016321c08de0978427e2697b2bf35afa2090d60763ce718626bf8`)
  annoté en tête le 27 nov. 2026, contenu d'origine conservé
  tel quel ; SHA après annotation
  `526daef6d2c6ee791ba392309c385bb2cf703451d879def37a0625097310d682`
  (94 lignes). Valeurs correctes de référence :
  `survival_tcga_recalc_20261127_results.txt`, SHA-256
  `fa5cff07f74e52107357286581b443f6eb776db0eb33af8b4edad2db6f206b20`
  (94 lignes), reproduites par 3 implémentations ; script
  d'origine du 15 nov. introuvable (confirmé le 27 nov. 2026).

## 4. Hachages des livrables de ce chantier

| Fichier | Lignes | SHA-256 |
|---|---|---|
| `section_8.100_fusion_depots.md` | 321 | `71be6cd61b35a05d70762711a6ae200999d2ee49a546ee53ee55514590876657` |
| `PROVENANCE_8100.md` (ce fichier) | 170 | auto-référence impossible (comme le MANIFEST) — SHA consigné dans le rapport de livraison du chantier A |
| `check_cox_tcga_results.txt` (annoté) | 94 | `526daef6d2c6ee791ba392309c385bb2cf703451d879def37a0625097310d682` |
| `check_cox_tcga_results.txt` (avant annotation) | 68 | `c50fb788915016321c08de0978427e2697b2bf35afa2090d60763ce718626bf8` |

Chemins : `~/workspace/runs/pdac-v6/section_8.100_fusion_depots.md`,
`~/workspace/runs/pdac-v6/PROVENANCE_8100.md`,
`~/workspace/runs/pdac-v6/check_cox_tcga_results.txt`.

## 5. Ce qui manque

- **Traduction du livre blanc entier en anglais :** piste
  future, non commencée (seul le README est traduit).
- **`LICENSE_OR_DATA_NOTICES.md`** (repro, 1 896 o) : non
  fusionné, non téléchargé ni comparé ; il reste dans le
  dépôt repro archivé.
- **`check_cox_tcga.py` :** doublon non rapatrié — déjà dans
  le principal (SHA `5aa4548a…`) ; le script importe depuis
  un chemin absolu local (`/home/hatch/workspace/runs/pdac-v6`),
  non portable.
- **Fusion dans le livre blanc :** NON faite dans ce
  chantier (c'est le parent qui fusionne) ; le livre blanc
  sur disque (26 794 lignes, SHA `bf80f029…`) n'est pas
  poussé.
- **Kicker de couverture du PDF** (« 19–22 novembre 2026 »)
  à passer au 27 nov. 2026 : à la prochaine construction du
  PDF, par le parent.
- **Consolidation GSE184585 à 200 nuls :** toujours non
  faite, nommée comme suite (§8.99.7).
- **Vérifications distantes :** non refaites ici — têtes,
  commits, archivages et MANIFEST distant vérifiés par le
  parent avant ce chantier ; les valeurs sont reprises
  telles que communiquées, avec leur source nommée.
- **Dépôts jamais touchés :** `tlogNext-pdac-phase2`
  (autre IA), `universal-log-research`, Kaggle.
