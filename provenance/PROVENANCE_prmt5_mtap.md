# Provenance — dépendance PRMT5 contre statut MTAP mesuré (DepMap 24Q4)

Date : 16 nov. 2026. Script : `prmt5_mtap_dependency.py` (log `prmt5_mtap_dependency.log`).

## Sources (toutes vérifiées par hachage)

| Fichier | Dépôt | Taille (octets) | SHA-256 | MD5 |
|---|---|---|---|---|
| `data/CRISPRGeneEffect.csv` | DepMap Public 24Q4, figshare article 27993248, DOI 10.25452/figshare.plus.27993248.v1 (fichier 51064667) | 428 678 699 | `3d8f3ec6dbf2db7ff834b79b508622ec0b226f3518003fe96ecf5a4fcf167e3b` | `6edf7ade09b9b34199210b559d4745d3` |
| `data/Model.csv` | Même article (fichier 51065297) | 645 696 | `b7a0c1385e6cef30132b56aff61f1261d11e3f490490b355c430d32ee0dbdcfa` | `675210d17675f3517b0ce39a3c274f16` |
| `data/OmicsCNGene.csv` | Même article (fichier 51065324), téléchargé le 16 nov. 2026 via l'API figshare (`https://api.figshare.com/v2/file/download/51065324`), log `data/download_omicscn.log` | 1 394 554 236 | `4851d3e939d48837a39a0f01294deb90fa507a85703586a927b77474f999134c` | `4696565fa74dc805983bc278b4a41802` (exact, MD5 figshare annoncé) |

## Échelle du fichier CN — point de méthode important

`OmicsCNGene.csv` est en CN relatif **linéaire** (1,0 = diploïde ; 0 = délétion
homozygote), **pas** en log2. Depuis la release 24Q2, DepMap ne log-transforme
plus la matrice CN relative (« to be consistent with absolute copy number
data, the relative copy number matrix is no longer log2 transformed », annonce
24Q2 ; confirmé par le forum DepMap : valeurs linéaires, min 0 et non négatif).
Vérifié sur les données : médiane globale toutes colonnes = 1,012 ; MTAP min
0,00, 12,8 % des modèles < 0,01 ; CDKN2A 23,2 % < 0,01 ; aucune valeur négative.

Seuils appliqués (protocole gelé) :
- Délétion profonde (principal) : CN relatif < 0,5 (< 1 copie).
- Sensibilité : CN relatif < 1 (sous-diploïde).

## Méthode

- Lignées pancréas : `OncotreeLineage == 'Pancreas'` dans Model.csv (68),
  intersectées avec GeneEffect → 47 (45 adénocarcinomes + 2 adénosquameux).
- Colonnes Chronos : PRMT5 (10419), CDKN2A (1029), KRAS (3845), ACTB (60),
  lues par blocs (fichier 428 Mo). Colonnes CN : MTAP (4507), CDKN2A (1029),
  lues par blocs (fichier 1,4 Go). Jointure sur ModelID : 1 178 modèles
  avec les deux données.
- Tests : Mann-Whitney bilatéral (médianes, n par groupe) + Spearman continu.
  Aucune imputation, paires complètes uniquement.
- Contrôles : CDKN2A (co-délété 9p21), KRAS et ACTB (témoins non liés).
- Vérification interne : Spearman PRMT5–KRAS sur les 47 pancréas = −0,189,
  identique au balayage génome entier.

## Corrections en cours de route (traçabilité)

1. **Échelle CN** : la v1 du script supposait log2 (seuils log2 < −1 et < 0) —
   zéro lignée classée délétée, tous les tests impossibles. Corrigé après
   vérification de l'échelle (forum DepMap + distribution empirique).
2. **Étiquettes de colonnes** : la v1 renommait les colonnes Chronos par
   position ; le fichier les trie alphabétiquement (ACTB, CDKN2A, KRAS, PRMT5)
   alors que le dict du script était dans l'ordre PRMT5, CDKN2A, KRAS, ACTB —
   PRMT5 et ACTB étaient échangés (contrôle de cohérence raté : +0,060 au lieu
   de −0,189). Corrigé : renommage par le nom. Après correction, le contrôle
   de cohérence passe exactement (−0,189).

## Sorties

| Fichier | Contenu | SHA-256 |
|---|---|---|
| `data/prmt5_mtap_results.csv` | 25 lignes de résultats (MW + Spearman) | `e7c90e9a847c…` |
| `data/prmt5_mtap_pancreas_lines.csv` | 47 lignées pancréas (CN MTAP/CDKN2A, statut, Chronos PRMT5/CDKN2A/KRAS/ACTB) | `348ccfa975ed…` |
| `prmt5_mtap_dependency.log` | Journal complet du run (exit 0, 31 s) | — |

Règle : données du jour uniquement (DepMap 24Q4). Aucune donnée ni conclusion
d'une autre expérience importée (règle 15 nov. 2026).
