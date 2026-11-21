# DATA_SOURCES_877_diff — résumé du diff section par section (§8.77)

**Référence :** `~/workspace/push_v62_875_build/snap/DATA_SOURCES.md`
(SHA-256 `2b58ec3533ee7c7837dbeeaf9cd2aaed2ec3560b5240082a358256b3fb1caea2`,
702 lignes) → **`~/workspace/runs/pdac-v6/DATA_SOURCES_877.md`** (900 lignes).
Diff complet : `diff -u` entre les deux fichiers (à produire par le
coordinateur au moment de la fusion ; les remplacements sont listés ici
un par un, avec leur justification). Aucune section existante du livre
blanc n'est modifiée par ce fichier — c'est le document de sources qui
est révisé, pas le livre blanc.

## En-tête

- Ajout d'une ligne « Révision §8.77 : 21 novembre 2026 » (toutes les URL
  manquantes retrouvées et vérifiées par SHA-256 ; nouvelles §28 et §29 ;
  aucun verdict modifié).

## §0.1 — Script maître

- Réécrit : les « limites connues » deviennent les « limites CORRIGÉES au
  §8.77 » (PRISM 19Q4 4/4, PANC-1 fichier par fichier, suppléments +
  SOFT + ICGC + QCMG + PanCanAtlas ajoutés, hachages PRISM 24Q2 ajoutés),
  avec la référence au script corrigé (`repro_877/download_data_877.sh`)
  et au test du script complet (9 exécutions, résultat final EXIT:0,
  journal `cold/full_script_877i.log` ; incidents consignés : 403
  transitoire, blocages 0 o/s par proxy manquant dans les unités, S3
  ICGC 403, redémarrage machine, blocage PANC-1 calc.csv).

## §0.3 — Inventaire rapide

- « Sources avec URL complète » : 8/16 → **16/16**.
- « Sources partielles (API) » : 4/16 → **0/16** (URL directes aussi
  consignées pour CPTAC, PRISM 24Q2, PRISM 19Q4, QCMG).
- « Sources sans URL » : 4/16 → **0/16**.

## §2.3 — LUAD (SHA corrigé)

- SHA-256 consigné sur 65 caractères (`…cf73f1daf2`, un `d` en trop,
  faute préexistante du 19 nov. 2026) → vrai SHA `…cf73f1af2`, vérifié
  sur le fichier local et le re-téléchargement à froid, identiques.

## §3.1 — SOFT GPL20769

- Ajout : URL exacte `…/GPL20nnn/GPL20769/soft/GPL20769_family.soft.gz`,
  MD5 `4c39e802…`, SHA-256 `ecb1b79a…`, taille 37 588 662 o, table
  19 749 lignes, titre confirmé. Note : le chemin `GPL2nnn/` donne 404.

## §3.2 — Suppléments ng3398

- Ajout : patron d'URL Springer `…/41588_2015_BFng3398_MOESM{n}_ESM.{ext}`,
  5/5 re-téléchargés et vérifiés par SHA-256 le 21 nov. 2026.

## §5.2 — ICGC expression (URL corrigée)

- URL S3 directe (`icgc-xena-hub.s3.amazonaws.com/…`) → URL du hub
  `https://icgc.xenahubs.net/download/PACA-AU/nature16965-s2_normalised_exp.txt.gz`
  (la S3 directe renvoie HTTP 403, 4 tentatives, exécution full5) ;
  re-téléchargée : 9 841 881 o, SHA `c2cb57af…` identique au consigné.

## §5.3 — ICGC probe map

- Ajout : URL exacte du hub `https://icgc.xenahubs.net/download/PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp.gz`,
  vérifiée (353 314 o, SHA `b09a746f…`). Note : listing S3 403, URL S3
  directe 403 — c'est le hub qui fonctionne.

## §5.4 — ICGC NMF

- Ajout : URL exacte du hub `…/nature16965-s2_NMF_class_assignment.txt.gz`
  (le `.txt` nu = 404), vérifiée (447 o, SHA `f1e84b99…`).

## §6 — CPTAC

- Ajout : les 4 URL directes `links.self` Zenodo (Report UMich, BCM
  Tumor, mapping UMich, `cptac_genes.csv`), lues dans l'API le
  21 nov. 2026, tailles et MD5 conformes.

## §7 — PRISM 24Q2

- Ligne `Cell_Line_Meta_Data.csv` : URL `https://ndownloader.figshare.com/files/46630978`
  (fichier 46630978, API 25917643), re-téléchargée et vérifiée (SHA
  `13a85da9…`), ajoutée au script corrigé.

## §8 — PRISM 19Q4

- Ajout : les 4 URL directes `ndownloader` (fichiers 20237739, 20237763,
  20237769, 20238123), 4/4 re-téléchargées et vérifiées (tailles, MD5,
  SHA-256).

## §10 — PANC-1

- Ligne `mit_test.csv` : URL reconstruite `…/MIT/test.csv` marquée
  **VÉRIFIÉE §8.77** (3 249 228 o, SHA `9f3ae189…`).

## §11 — Clinique TCGA PanCanAtlas (test C)

- Titre : « PROVENANCE D'ACQUISITION MANQUANTE » → « provenance
  d'acquisition RETROUVÉE au §8.77 ».
- Remplacement du bloc « URL non consignée / non re-téléchargeable » par
  l'URL exacte datahub (`paad_tcga_pan_can_atlas_2018`, via
  `media.githubusercontent.com`), taille 58 621 o, SHA `0c274268…`
  vérifié, avec la double confirmation du pointeur LFS (son `oid`
  sha256 est le SHA du fichier). Conséquence mise à jour : lacune close,
  verdict du test C inchangé.

## §12 — QCMG

- Ajout : URL exactes datahub (`paad_qcmg_uq_2016`, via
  `media.githubusercontent.com`), 2/2 vérifiées par SHA-256. Note LFS
  (pointeur 130 o via `raw.githubusercontent.com`).

## §13 — Birnbaum

- Ajout : DOI `10.1186/s12943-017-0739-z`, *Mol Cancer* 16:174, PMID
  29110659, et le patron d'URL Springer `…/12943_2017_739_MOESM{n}_ESM.xlsx`,
  5/5 vérifiés par SHA-256.
- Ligne « URL non consignée » remplacée par « URL : voir ci-dessus
  (§8.77) ».
- SHA-256 MOESM3 corrigé : la consignation ne faisait que 62 caractères
  (`…a9b8ae…` au lieu de `…a9d9b8ae…`, faute de frappe trouvée par le
  test du script complet — trois téléchargements indépendants d'accord
  sur la vraie valeur `8bfbdcd6…6b1a13`).

## §15.4 — Fichiers non conservés

- Ligne SOFT GPL20769 : URL retrouvée et vérifiée (§3.1), chemin
  `GPL20nnn/` (le `GPL2nnn/` donne 404).

## §15.6 — Lacune PanCanAtlas

- Titre : « Lacune de provenance » → « Lacune de provenance — CLOSE au
  §8.77 ». Texte réécrit : provenance retrouvée le 21 nov. 2026, avec
  l'historique conservé (la lacune a existé du 15 au 21 nov. 2026).

## §17 — Bilan des URL manquantes

- Remplacement du bilan (« 19 fichiers + 4 CPTAC + 1 clinique + 1 SOFT »)
  par le bilan révisé : **19/19 fermés + CPTAC + clinique test C + SOFT**,
  aucune URL manquante restante ; voies infructueuses consignées au §29.
- Chaque ligne du tableau mise à jour (« FERMÉ §8.77 » + URL, historique
  conservé dans la 3e colonne) ; lignes §16 (ng3398 MOESM59/60) : « URL
  retrouvée §8.77 ».

## §28 — NOUVELLE : lot Yeh_seq FNA (§8.76)

- Sources du §8.76 (aucun nouveau téléchargement : réutilisation du
  téléchargement §8.74, SHA re-vérifiés) : Yeh_seq TSV (9 468 179 o,
  SHA `2fc0a66e…`), matrice GPL18573 (6 864 o, SHA `9b333eb6…`), 42
  codes FNA, test apparié (41/42 mêmes tumeurs que FF), verdict
  CONFIRME d_maxsep +0,1642, flux SHA `70697b3a…` / nul `2474ceaf…`,
  manifeste `manifest_v62_876.txt`.

## §29 — NOUVELLE : chantier §8.77

- §29.1 : tableau gap par gap (11 lignes : ng3398, Birnbaum, probe map,
  NMF, PRISM 24Q2 meta, PRISM 19Q4, QCMG, clinique test C, SOFT GPL20769,
  `mit_test.csv`, CPTAC) avec URL et vérification.
- §29.2 : voies infructueuses consignées (S3 403, Europe PMC 500, Nature
  303, `GPL2nnn/` 404, pointeur LFS).
- §29.3 : script corrigé (SHA `55811136…`, diff 323 lignes,
  corrections 1–12, original intact ; deux fautes de frappe SHA
  corrigées : MOESM3 §13, LUAD §2.3).
- §29.4 : test à froid (chaîne complète, résultat renvoyé au §8.77) +
  script complet EXIT:0 (52 fichiers, 2,4 Go) et les 5 incidents
  consignés.
- §29.5 : ce qui reste ouvert — rien sur les fichiers bruts.

## Annexe A — Commandes de vérification

- §2 réécrit : la plupart des fichiers sont désormais DANS le script
  corrigé ; il ne reste hors script que la table GPL6244 (dérivée du
  SOFT). Rappels des commandes API figshare 19Q4 et Zenodo conservés.

## Annexe B — inchangée

- Liste des provenances lues (le chantier §8.77 ajoute ses propres
  sources lues : pages PMC5674743 et Nature ng.3398, API figshare
  25917643 et 9393293, API Zenodo 8394329, API GitHub datahub,
  hub Xena, FTP GEO — toutes citées au §29 et dans le journal
  `repro_877/JOURNAL_877.md`).
