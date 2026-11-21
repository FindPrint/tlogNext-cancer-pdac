# ADDENDUM GELÉ au protocole §8.79 — Cohorte #2 : GSE57495 (11 flux), après arrêt C2

Date : 21 novembre 2026, ~12h45 EST. Addendum au protocole gelé
`PROTOCOL_nouvelle_serie_879.md` (C2, GDC ORGANOID-PANCREATIC).
Cet addendum est gelé AVANT toute construction de la cohorte #2
et avant tout run. Aucun paramètre ne change après les résultats.
Le livre blanc N'EST PAS édité, le PDF N'EST PAS régénéré, rien
n'est poussé sur GitHub dans ce chantier (convention des
chantiers ; fusion par le coordinateur). La section §8.79 est
écrite dans un FICHIER SÉPARÉ (`section_8.79_nouvelle_serie.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié).

## 0. Pourquoi un addendum : l'arrêt C2 (documenté, pas caché)

La candidate C2 (GDC ORGANOID-PANCREATIC) est INUTILISABLE comme
paire à 12 gènes sous le protocole gelé §5, pour une raison de
construction vérifiée avant tout run (aucun `maxsep` ne la
concerne) :

- Téléchargement réussi : 55/55 fichiers, MD5 conformes au
  manifeste (SHA `f713edebf…6220b`), total 232 648 892 o exact.
- Association fichier → échantillon (API GDC) : 44 Tumor /
  11 Normal ; les 11 Normal exclus par le protocole.
- **DPCR1 absent de 55/55 fichiers** (0 occurrence du symbole
  exact, vérifié par grep sur les 55 TSV). Les 12 autres gènes
  utiles (11 v4 + KRAS) sont présents dans 55/55 fichiers.
- Cause établie : DPCR1 n'est plus un symbole valide.
  Ensembl REST `lookup/symbol/homo_sapiens/DPCR1` :
  « No valid lookup found for symbol DPCR1 » (21 nov. 2026).
  Les 5 anciens identifiants Ensembl croisés pour DPCR1
  (ENSG00000168631, ENSG00000229284, ENSG00000232308,
  ENSG00000257232, ENSG00000232251) sont absents eux aussi du
  fichier GENCODE v36. HGNC : **DPCR1 est le `prev_symbol` de
  MUCL3** (HGNC:21666, « mucin like 3 », alias PBLT) — et MUCL3
  est présent dans 55/55 fichiers.
- **Aucun remappage n'est fait.** Le protocole gelé exige le
  symbole exact DPCR1 et interdit tout gène mappé à la main
  (§4.2, §5) ; changer la porte après l'avoir vue échouer
  serait un changement de protocole sans go. La porte dit
  ARRÊT (§3) : la cohorte C2 s'arrête ici, comme une paire à
  12 gènes. Le gène est mesuré sous son symbole actuel MUCL3
  (55/55) — c'est consigné pour un protocole futur qui
  pré-enregistrerait MUCL3, pas pour celui-ci.
- Conséquence gelée : **aucun CSV C2, aucun run C2.** Les 55
  TSV téléchargés et vérifiés restent détenus (reçu
  `download_gdc_879_receipt.json`) pour un usage futur ; ils
  ne portent aucun verdict ici.

## 1. Cohorte #2 choisie : GSE57495 — et pourquoi elle est recevable ici

**Série : GSE57495**, « Development of a prognostic gene
signature in pancreatic cancer », PMID 26247463, NCBI GEO,
63 tumeurs PDAC microdisséquées congelées, plateforme
**GPL15048**. URL :
`https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57495`.

**Statut de la limitation, connu AVANT ce gel** (donc
pré-enregistré, pas découvert après coup) : **11/12 gènes v4
— GSTM1 absent** (aucune sonde à symbole exact GSTM1 ; seule
la sonde partagée `merck-NM_000561_s_at`, annotée « GSTM1
GSTM2 GSTM4 », exclue comme ambiguë, protocole §8.69 §4.1 ;
aucune sonde mappée à la main). KRAS présent ; 63/63 cas
complets sur 11 gènes (vérifié au §8.69, à re-vérifier ici
avant construction, §5). C'est la limitation qui avait fait
déclarer GSE57495 « INUTILISABLE » au §8.69 — pour une paire
à 12 gènes. Le présent addendum pré-enregistre explicitement
une paire à **11 flux** : la comparabilité aux paires à 12
flux est donc limitée, et c'est dit plainement au §8.79
(§7, §10).

**Indépendance — le statut exact, écrit avant tout run :**
1. **Jamais courue comme paire pipeline.** Aucun CSV de flux,
   aucun run, aucun JSON, aucune valeur `maxsep` n'existe
   pour GSE57495 dans ce projet (§8.69 : « INUTILISABLE —
   aucun CSV, aucun run »).
2. **MAIS déjà tenue comme holdout DIRECT** (§8.66/§8.69 et
   `REVUE_INDEPENDANTE_2026-11-15/RESULTATS_HOLDOUT_GSE57495.md` :
   Spearman KRAS–CEACAM5 ρ=0,4377, p permutation 0,00024, IC
   95 % [0,1901, 0,6352] ; partielle après scores
   acineux/îlots : 0,3521 ; table génome entier
   `all_gene_spearman_vs_KRAS.csv`). **Elle n'est donc PAS
   indépendante pour l'association KRAS–CEACAM5 et ne doit
   JAMAIS être présentée comme une confirmation indépendante
   de cette association.** C'est le caveat du §8.78 (C3) et de
   la tâche de ce chantier, repris tel quel ici.
3. **Patients distincts des cohortes tenues.** GSE57495 est
   une série GEO propre (63 patients, titres PDAC1..63) ;
   aucune inclusion documentée dans TCGA, ICGC, GSE71729,
   GSE62452, GSE62165, GSE21501, GSE79668 ou GSE131050 (grep
   livre blanc §8.1–§8.77 ; §8.69 §4 : les re-tests déguisés
   écartés sont GSE78229/GSE28735, pas GSE57495).
4. **Conséquence gelée : la paire GSE57495 entre dans le
   compte A2 comme treizième paire, avec 11 flux et avec son
   caveat holdout écrit** — elle compte pour `maxsep` (le
   critère gelé), elle ne compte jamais comme confirmation
   indépendante de KRAS–CEACAM5. Si un lecteur futur l'y
   employait, ce serait une erreur documentée ici d'avance.

## 2. Arrêt borné — AUCUNE cohorte #3 dans ce chantier

**Une seule cohorte dans cet addendum : GSE57495 (n = 63).**
Si elle est INUTILISABLE selon les critères d'acceptation du
§5 (matrice ou mapping SHA différent, plateforme autre que
GPL15048, KRAS absent, < 11 gènes v4 mappés, < 40 cas
complets), le chantier s'arrête sur un blocage documenté :
section §8.79 écrite quand même, avec les tentatives
chiffrées (C2 puis C3), aucune valeur inventée, et la piste
suivante nommée comme piste seulement (C1 lot drogue Chen
2025, ou C4 GSE194249 après re-audit — aucun run lancé pour
elle dans ce chantier).

## 3. Construction des flux — variante (a) à 11 flux

Nouveau script `build_fluxes_879_c3.py` (copie adaptée de
`build_fluxes_869.py`, original intact — la porte « 12 gènes »
de l'original ne s'applique pas ici ; tout le reste est
repris). Préfixe `_879_` pour tous les fichiers du chantier.

### 3.1 Source (aucun nouveau téléchargement)

- Matrice : `data/GSE57495_series_matrix.txt.gz`,
  13 487 043 o, SHA-256
  `995dbeff288a14c1cc1a52489e456b7677ede5da8e287069b8298d649b532efc`
  (vérifié avant ce gel, re-vérifié §5). 60 608 lignes,
  63 échantillons, valeurs log2 déposées, 0 NaN (§8.69).
- Mapping : `data/GPL15048_probe2symbol.tsv`, SHA-256
  `93e01ec387ab710dfbfe4b7ad960a90c494b131f62637df3a4476fa9f998f952`
  (vérifié avant ce gel, re-vérifié §5). 60 607 lignes,
  41 024 sondes avec symbole, 22 115 symboles uniques,
  colonne `GeneSymbol` (§8.69).
- Plateforme lue dans l'en-tête de la matrice :
  `!Series_platform_id "GPL15048"` ; sinon ARRÊT (§2).

### 3.2 Identification des gènes

- Sondes → symboles par le mapping GPL15048 ; symboles
  dupliqués agrégés par MÉDIANE (précédent du projet,
  §8.69) ; la sonde partagée `merck-NM_000561_s_at`
  (« GSTM1 GSTM2 GSTM4 ») est exclue comme ambiguë — aucune
  sonde mappée à la main.
- Les 11 gènes utiles présents doivent être UNE ligne chacun
  après agrégation (symbole exact). GSTM1 doit être ABSENT
  (porte §5) — si GSTM1 apparaissait, c'est consigné et la
  construction s'arrête (la paire pré-enregistrée est à
  11 flux, pas à 12).
- Valeurs : log2 déposées, telles que fournies. Aucune
  renormalisation, aucune transformation log, aucune
  imputation ajoutée.

### 3.3 Série réelle (variante (a), 11 flux)

- Gènes v4 retenus (11, ordre de la liste, GSTM1 absent) :
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2,
  CEACAM5, CLCA1, MUC16.
- Contrôle : KRAS (expression log2, croissant). Le contrôle
  n'est JAMAIS un flux : pas de doublon.
- Tumeurs seules : 63 échantillons, titres `PDAC1..PDAC63`
  (règle §8.69) ; aucun normal dans la série.
- Cas complets seulement (KRAS + 11 gènes présents), jamais
  d'imputation. Attendu : 63/63 cas complets.
- Tri : KRAS croissant ; `step` = rang 0..62.
- Sorties : `pdac_879_geo57495_fluxes.csv` (+ `_nul.csv`).
  Colonnes : `step` + 11 flux. SHA-256 consignés.

### 3.4 Nul

Bloc des flux permuté par lignes, graine 42, `rng(42)`,
contrôle (ordre KRAS, `step`) intact — même convention que
les paires V1 (§8.56.8, PROTOCOL_phase2 §2). Le nul est un
échantillon hypothétique, pas une mesure.

### 3.5 Nuls frais (conditionnels, §6)

Si et seulement si l'écart mesuré sur la paire graine 42 est
PROCHE du plancher (§6 : `d_maxsep` dans [−0,07 ; +0,14[),
2 nuls frais sont construits par la même méthode, graines
**8791** et **8792** (gelées ici avant tout run, jamais
utilisées dans ce projet), et courus en runs frais
(`pdac_879_geo57495_fluxes_nul_s8791.csv`,
`pdac_879_geo57495_fluxes_nul_s8792.csv`,
`results_fast_v62_879_geo57495_nul_s8791`,
`results_fast_v62_879_geo57495_nul_s8792`). Le verdict
reste celui de la paire graine 42 (§6) ; les nuls frais sont
un contrôle de robustesse descriptif (min / médiane / max des
écarts), jamais un moyen de choisir le nul qui arrange.

## 4. Critères d'acceptation de la cohorte (vérifiés sur les fichiers détenus, avant construction)

- Matrice SHA-256 `995dbeff…532efc` (re-vérifié) ; mapping
  SHA-256 `93e01ec3…998f952` (re-vérifié).
- Plateforme lue dans l'en-tête : GPL15048 ; sinon ARRÊT (§2).
- n = 63 tumeurs PDAC (titres PDAC1..63) ; sinon ARRÊT (§2).
- Aucun échantillon déjà présent dans une cohorte du projet
  (GSM inspectés) ; sinon ARRÊT (§2). (Caveat §1 point 2 :
  la série a servi de holdout direct — c'est connu et
  déclaré, pas un recouvrement caché.)
- KRAS présent comme gène mappé ; sinon ARRÊT (§2).
- Les 11 gènes v4 présents (une ligne chacun après
  agrégation par médiane, symbole exact) ET GSTM1 absent ;
  sinon ARRÊT (§2) (aucun gène remplacé).
- Cas complets (KRAS + 11 gènes) ≥ 40 ; sinon ARRÊT (§2).

## 5. Runs v6.2 (mode fast)

- Lot : 2 runs — réel + nul — manifeste `manifest_v62_879_c3.txt`,
  lanceur reprenable existant `run_v62_lot.sh` (saute les sorties
  déjà complètes), journal `runs_v62_879_c3.log` (SHA du pipeline
  en tête, exits consignés).
- Dossiers : `results_fast_v62_879_geo57495` et
  `results_fast_v62_879_geo57495_nul` (nuls frais éventuels :
  `results_fast_v62_879_geo57495_nul_s8791` /
  `..._s8792`).
- Lancement en `systemd-run --unit=v62-879c3 --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance qui
  s'arrête d'elle-même à 2/2 (ou 4/4 si nuls frais). Ne JAMAIS
  supprimer le dossier d'un run en cours. Si la machine
  redémarre, reprise sans perte (SKIP des dossiers complets,
  jamais de relance à l'aveugle).
- SHA du pipeline revérifié avant ET après le lot.
- Durée attendue : ~2–3 min par run (référence §8.76 :
  n=42, 12 flux, ~2 min/run).

## 6. Critère de passage — GELÉ avant tout run

**La paire PASSE si et seulement si :**
`d_maxsep = maxsep_R − maxsep_N > 0,07` (plancher, en unités |d|,
gigue_eff = max(gigue mesurée, 0,07) — v6.2 déterministe, gigue
attendue 0, comme §8.56 §3) **ET** `d_maxsep > 0` (positif —
impliqué par > 0,07, mais consigné séparément comme au §8.56).

`maxsep` = `best_config.metrics.max_separation`, |d de Cohen|
maximal du scan, lu sur le best_config ANCIEN (sélection par
l'ancien composite) — mêmes définitions que §8.56.2. Le seuil MC,
la cascade, S_sep, Delta, L7a sont inchangés par construction.

**Catégories de verdict (gelées) :**
- **CONFIRME** : `d_maxsep > 0,07` — treizième paire passante
  (11 flux, caveat holdout écrit).
- **PARTIEL** : `0 < d_maxsep ≤ 0,07` — positif mais sous le
  plancher (même catégorie que GSE71729, +0,0402, et GSE79668,
  +0,0567).
- **NON** : `d_maxsep ≤ 0` — négatif ou nul (même catégorie que
  GSE62452 et GSE21501).

**Ce que le verdict change (gelé) :**
- Si CONFIRME : A2 devient **9/13 au-dessus du plancher** (et
  11/13 positifs si le signe est positif — à compter sur les
  chiffres mesurés, pas à pré-écrire) ; LOO recalculé sur
  13 paires (pire cas sur 12).
- Si PARTIEL : A2 devient **8/13 au-dessus du plancher,
  11/13 positifs** ; LOO recalculé sur 13 paires.
- Si NON : A2 devient **8/13 au-dessus du plancher,
  10/13 positifs** ; LOO recalculé sur 13 paires.
- Dans tous les cas, la paire entre dans le compte A2 comme
  treizième paire (11 flux) : c'est une paire principale
  jamais courue comme paire pipeline (contrairement au lot FNA
  §8.76, apparié). **C3 reste LEVÉE** dans tous les cas — elle
  l'était déjà depuis le §8.71 ; ce chantier est une
  consolidation supplémentaire, pas une condition.
- Le leave-one-out sur les paires indépendantes est recalculé
  ici (il change : la paire y entre).

**Nuls frais (§3.5, règle gelée).** La paire graine 42 fait le
verdict, dans tous les cas. Si `d_maxsep` est PROCHE du
plancher — défini ici comme `d_maxsep` dans [−0,07 ; +0,14[,
soit à moins d'une largeur de plancher du seuil, de part et
d'autre — les 2 nuls frais (graines 8791, 8792) sont courus et
les écarts `d` contre chaque nul frais sont rapportés
(min / médiane / max des 3 écarts). Lecture gelée : si les
3 écarts sont > 0,07, le passage est dit « consolidé » ; si
l'un des 3 est ≤ 0,07, le passage (ou l'échec) est dit
« fragile, non consolidé » — le verdict de la paire graine 42
n'est JAMAIS changé par les nuls frais. Si `d_maxsep` est
hors de [−0,07 ; +0,14[, aucun nul frais n'est couru.

**Contrôles descriptifs (à publier, ne décident pas) :**
- `sep` compagnon (= maxsep/(1+maxsep)), ancien MC (secondaire),
  S_sep, Delta, L7a, cascade, falsification — affichés selon
  la convention §8.64.6 (maxsep principal, ancien MC secondaire,
  sep compagnon, mention de fragilité en tête de table).
- Falsification : INDISPONIBLE sous n = 75 — GSE57495
  n = 63 : noter « indisponible », ne pas imputer.
- Plancher équivalent-sep (descriptif) : la paire passe-t-elle
  aussi `0,07·(1+m_R)(1+m_N)` ? Rapporté, non décisif (D4 n'est
  pas rejoué ici : il porte sur les paires V1, déjà tranché).
- Comparaison descriptive avec le holdout direct (§8.66/§8.69 :
  ρ=0,4377) : la paire pipeline et le holdout direct portent
  sur les mêmes 63 tumeurs mais ne mesurent pas la même chose
  (rupture multi-flux vs corrélation KRAS–CEACAM5) — aucune
  des deux lectures ne valide l'autre ; c'est écrit tel quel.
- Aucun autre critère, aucune repondération, aucune redéfinition
  du plancher après avoir vu les chiffres.

## 7. Extraction et vérification

1. Extracteur propre du chantier, `extract_879_c3.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_876.py`) ; lit `maxsep`, `mc_score`,
   `stability`, `ssep`, `delta`, `l7a`, cascade, falsification
   dans les 2 (ou 4) `master_results.json` ; sorties
   `extract_879_c3.json` / `extract_879_c3.csv`.
2. Second calcul indépendant : relecture directe des
   `master_results.json` par un chemin distinct (script
   `verify_879_c3.py`, SHA noté) — `maxsep` et ancien MC
   recoupés à 0,0 exact ; tout écart = résultat à
   diagnostiquer, pas un bruit.
3. Recoupements : les 12 valeurs déjà comptées reprises telles
   quelles du §8.56 (table `sep_maxsep_856_table.json`, SHA
   `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`),
   du §8.69 (`extract_869.json`, SHA
   `644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b`),
   du §8.70 (`extract_870.json`, SHA
   `4ffa851a83668b2369097703862e0413ff9af54af3a66ef70aea9333b40c444f`),
   du §8.71 (`extract_871.json`, SHA
   `85e9089a…55e3b`) et du §8.74 (`extract_874.json`, SHA
   `82ade74701245021dfdb965bdc689ac98262c70f12ecec7f39e1b5b742dfcb47`),
   jamais recalculées ici — ce chantier ne re-vérifie pas les
   §8.56/§8.59/§8.64/§8.69/§8.70/§8.71/§8.74/§8.76 (déjà clos).
4. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 8. Tests directs en appui (ne décident pas)

Script `direct_tests_879_c3.py` (SHA noté), sur les CSV de flux
du chantier (réel + nul graine 42) :
1. **Test informatif (correction §8.70, appliquée ici) :**
   corrélation de Spearman de chaque flux avec le pas (ordre
   KRAS), réel vs nul : |ρ| moyen, Δρ médian, nombre de Δρ
   positifs (sur 11), table complète sans sélection. C'est le
   test qui porte l'information d'ordre.
2. d de Cohen marginal des 11 flux (réel vs nul) : pour chaque
   gène v4 retenu, moyenne et écart-type des valeurs ordonnées,
   d de Cohen réel−nul ; table complète, sans sélection.
   **Attendu vacueux par construction : d = 0,0000 pour les
   11 gènes** (le nul est une permutation des lignes, chaque
   flux garde exactement ses 63 valeurs). Rapporté tel quel :
   il valide la construction du nul (marginales préservées
   exactement), il ne mesure pas la séparation.
3. Comparaison descriptive avec les paires précédentes
   (Δρ médian, 10/12 positifs au §8.74 ; valeurs reprises
   telles quelles, jamais recalculées) et avec le holdout
   direct de la même cohorte (ρ KRAS–CEACAM5 = 0,4377,
   §8.69 — une corrélation directe, pas une rupture
   multi-flux). Si le signal d'ordre est plus faible, c'est
   consigné tel quel, sans être élucidé sans preuve ; si une
   divergence Delta/`maxsep` apparaît ici, elle est nommée
   telle quelle.
4. Aucun de ces tests ne change le verdict du §6.

## 9. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et le
  jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict : les résultats des autres dépôts (écran du 20 nov.,
  holdout GSE57495 ρ=0,4377, pilote Chen) ne prédisent rien
  ici — seul l'écart `maxsep` mesuré sur les runs du présent
  chantier fait le verdict. **En particulier, le holdout
  ρ=0,4377 ne prédit pas le verdict de cette paire.**
- Un nul qui invalide une piste est un résultat ; un échec du lot
  est un verdict, pas un échec caché.
- Ne jamais présenter une lecture préliminaire comme un verdict.
- Aucun consensus exigé entre flux ou contrôles ; aucune
  affirmation clinique — l'étude porte sur l'instrument.
- **Ne jamais présenter cette paire comme une confirmation
  indépendante de l'association KRAS–CEACAM5** (§1 point 2).

## 10. Livrables

- Ce protocole-addendum (gelé avant construction et runs C3)
  + le protocole C2 (`PROTOCOL_nouvelle_serie_879.md`, arrêt
  documenté au §0).
- `PROVENANCE_879.md` (C2 : arrêt DPCR1/MUCL3 avec sources ;
  C3 : source, auteur, date, dépôt, URL, SHA-256 de la matrice
  et du mapping, plateforme, effectifs, exclus, identification
  des gènes, vérifications d'indépendance).
- `build_fluxes_879_c3.py` + CSV de flux (`pdac_879_geo57495_*`,
  SHA consignés).
- `manifest_v62_879_c3.txt`, `runs_v62_879_c3.log`, dossiers
  `results_fast_v62_879_geo57495_*`, `extract_879_c3.json` /
  `.csv`, `verify_879_c3.py` + sortie de vérification,
  `direct_tests_879_c3.py` + sortie.
- §8.79 dans le FICHIER SÉPARÉ
  `section_8.79_nouvelle_serie.md` (verdict d'abord, une phrase :
  C2 INUTILISABLE (raison) puis C3 CONFIRME / PARTIEL / NON ;
  chiffres ensuite ; détail complet après ; provenance nommée
  partout ; C3 reste levée dans tous les cas ; A2 recalculé sur
  13 paires, dit explicitement, avec le caveat 11 flux et le
  caveat holdout).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin de l'addendum gelé §8.79 (cohorte #2, GSE57495). —
