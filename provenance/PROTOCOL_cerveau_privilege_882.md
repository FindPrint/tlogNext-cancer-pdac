# PROTOCOLE GELÉ — §8.82 : Cerveau, deuxième site à privilège immunitaire (TCGA-GBM)

Date : 21 novembre 2026, ~07h20 EST (12h20 UTC). Chantier §8.82, deuxième bras
supplémentaire autorisé par Zackary (idées propres). Ce protocole est gelé
AVANT toute construction de flux, tout run et toute analyse. Aucun paramètre
ne change après les résultats. Le livre blanc N'EST PAS édité, le PDF N'EST
PAS régénéré, rien n'est poussé sur GitHub dans ce chantier (convention des
chantiers ; fusion par le coordinateur). La section §8.82 est écrite dans un
FICHIER SÉPARÉ (`section_8.82_cerveau_privilege.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié ; v6.1
`2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`).
Chemin : `/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`.

Note de cécité (état connu du fichier v6.2, inchangé depuis son adoption) :
un grep `temperature|Onsager|2.269` sur le fichier retourne 8 occurrences,
TOUTES confinées à l'annexe génératrice d'exemple Ising (lignes ~10211 et
~12571–12817, fonction `generate_example_ising_csv`, marquée « EXEMPLE
UNIQUEMENT, hors cœur du pipeline »). Le cœur d'analyse ne voit ni T ni Tc ;
le fichier est celui adopté, SHA vérifié ci-dessus, jamais modifié.

## 0. Contexte décisionnel — à lire avant tout le reste

- §8.81 (bras œil, autre agent, en cours au moment de ce gel) définit les
  gènes du privilège immunitaire. Ce chantier REPREND la liste telle que
  donnée dans la mission, il ne la redéfinit pas : FASLG, TGFB1, TGFB2,
  IDO1, HLA-G, CD47, CD274/PD-L1 (7 gènes). Aucun gène ajouté ou retiré
  après avoir vu les chiffres. Si le §8.81 redéfinit la liste ensuite, ce
  chantier NE SUIT PAS la redéfinition : il rapporte ses résultats pour
  CETTE liste, et l'écart éventuel est consigné, pas corrigé après coup.
- §8.23 : la tumeur du pancréas devient « froide » quand KRAS monte —
  lymphocytes T en baisse dans les 4 cohortes (CD8A, CD4, FOXP3, PDCD1
  négatifs partout ; PDCD1 top-12 d −0,61 à −0,88, significatif partout ;
  CD274/PD-L1 ne monte qu'en TCGA, +0,26). La comparaison « froid de la
  même façon » se fait contre CES chiffres, repris tels quels, jamais
  recalculés.
- §8.11 : la chaîne PDAC = les 12 gènes v4 ordonnés par KRAS croissant
  (PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5,
  CLCA1, MUC16). La question du bras pipeline est si cette même chaîne
  apparaît dans le glioblastome quand on ordonne par agressivité.
- **Ce chantier ne rouvre rien :** C3 reste LEVÉE (§8.71), le test C reste
  NON (§8.45), l'adoption pleine de maxsep reste la décision de Zackary
  du 20 nov. 13h04. Le GBM n'est PAS une 13e paire indépendante PDAC :
  le compte A2 (8/12, 10/12 positifs, LOO 7/11) NE CHANGE PAS, quel que
  soit le verdict. Le GBM est un autre cancer, pas une cohorte
  pancréatique.
- §8.70/§8.72 : correction de méthode APPLIQUÉE ici (§9) — le test de
  Cohen marginal est vacueux par construction quand le nul est une
  permutation de lignes ; le test informatif est le Spearman de chaque
  flux contre le pas (Δρ médian, nombre de positifs). Le Cohen marginal
  est rapporté (il valide la construction du nul) mais ne décide rien.

## 1. Source — TCGA-GBM, déjà téléchargée, vérifiée avant ce gel

- **Dépôt :** Broad GDAC Firehose stddata 2016-01-28, même route que PAAD,
  LUAD et COAD.
- **Fichier :**
  `gdac.broadinstitute.org_GBM.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz`
- **URL :**
  `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/GBM/20160128/`
  (fichier ci-dessus ; le fichier `.md5` servi à la même adresse a été lu
  avant téléchargement).
- **Fichier local :** `data/tcga_gbm_rsem.tar.gz`
  (renommé depuis le nom long servi ; contenu identique, vérifié par MD5).
  - Taille : 30 268 366 octets (matrice interne, voir ci-dessous).
  - MD5 observé : `cfc6cf0a2c3c2e9f0ea7a11f2ba32d28` — ÉGAL au MD5 servi
    par le dépôt (vérifié le 21 nov. 2026 avant ce gel).
  - SHA-256 : `9996a653f26c8cf8f0a5c56db49e2c847b49c0d1c9823daa5bb050d13749eb83`.
  - Matrice interne :
    `GBM.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt`
    (30 268 366 octets).
  - Données : RNA-seq V2 RSEM normalisé (TCGA, UNC Illumina HiSeq),
    même technologie que PAAD/LUAD/COAD.
- **Échantillons (vérifiés par lecture d'en-tête avant ce gel, sans
  statistique) :** 20 503 gènes × 171 échantillons ; tumeurs primaires
  (code TCGA 01) : 153 ; autres codes : 02 et 11. Le nombre exact retenu
  est recompté dans le script de construction et rapporté ; la mission
  disait « n ≈ 160 », le nombre mesuré est 153 primaires.
- **Présence des gènes (vérifiée avant ce gel, sans statistique) :**
  les 7 gènes de privilège, les 12 gènes v4, les 6 gènes de
  prolifération (§2) et les 12 gènes immunitaires (§8.23) sont TOUS
  présents dans la matrice GBM (7/7, 12/12, 6/6, 12/12 ; aucun
  absent). Aucun remplacement n'est donc prévu ; si un gène manquait
  à la construction, la règle est celle du §8.27 (procéder avec les
  flux restants, minimum 10, sans imputation) et l'absence est
  consignée.
- Aucun nouveau téléchargement n'est requis ni effectué pour ce
  chantier. Aucun fichier clinique GBM n'est téléchargé : l'axe
  d'agressivité est construit depuis l'expression seule (§2).

## 2. Axes — définitions gelées avant toute mesure

### 2.1 Agressivité = score de prolifération (axe primaire)

Le glioblastome n'a pas d'équivalent de KRAS comme axe d'ordonnancement
pancréatique, et le grade NE PEUT PAS servir d'axe dans cette cohorte :
**tous les TCGA-GBM sont des glioblastomes, WHO grade IV, par définition
de la cohorte** — il n'existe pas de gradient de grade intra-cohorte à
tester. C'est dit plainement, ce n'est pas une lacune découverte après
coup : c'est la raison pour laquelle l'axe est un score d'expression.

- **Score de prolifération** (par patient) = moyenne des valeurs
  log2(RSEM normalisé + 1) des 6 gènes gelés : **MKI67, TOP2A, PCNA,
  CCNB1, BUB1, AURKB** (marqueurs de prolifération classiques : MKI67 =
  Ki-67 ; TOP2A, PCNA, CCNB1, BUB1, AURKB = cycle cellulaire / mitose).
  Aucun autre gène n'entre dans le score. Le statut IDH n'est pas dans
  la matrice RSEM et n'est pas utilisé (pas de fichier clinique dans ce
  chantier ; un bras IDH serait un autre chantier, avec son protocole).
- **Ordre primaire :** score de prolifération croissant (pas 0 = tumeur
  la moins proliférante, pas n−1 = la plus proliférante).

### 2.2 Score de privilège (axe secondaire)

- **Score de privilège** (par patient) = moyenne des z-scores (centrés
  réduits DANS la cohorte GBM, un gène à la fois) des 7 gènes de
  privilège : FASLG, TGFB1, TGFB2, IDO1, HLA-G, CD47, CD274.
- **Ordre secondaire :** score de privilège croissant. Il sert à la
  paire pipeline secondaire (§6) et à un test direct descriptif.

### 2.3 Score immunitaire « froid » (comparaison au §8.23)

- **Score froid** (par patient) = moyenne des z-scores (dans la cohorte
  GBM) de **CD8A, CD4, FOXP3, PDCD1** — les 4 gènes dont le signe était
  constant (négatif) dans les 4 cohortes du §8.23. Les 12 gènes
  immunitaires du §8.23 (CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274,
  PDCD1, CTLA4, GZMB, IFNG, CD19) sont tous testés un par un (§5).
- **Transformation commune :** log2(RSEM normalisé + 1), comme
  PAAD/LUAD/COAD. **Aucune correction de pureté** : les scores
  acineux/îlots sont spécifiques au pancréas et n'ont pas d'équivalent
  gelé ici. Limite dite d'avance (même limite que le bras §8.23 :
  ARN bulk, composition ou expression, mécanisme non établi).

## 3. Construction des flux GBM

Script `build_fluxes_gbm_882.py` (SHA noté dans la section) :

1. MD5 du tarball revérifié (`cfc6cf0a…`) avant lecture ; arrêt sinon.
2. Lecture de la matrice, symboles avant `|`, déduplication
   (premier conservé), tumeurs primaires (code 01) uniquement.
3. log2(RSEM normalisé + 1). Aucune imputation ; cas complets
   (score de prolifération + 12 gènes v4 + 7 privilège + 12 immunitaires)
   — **minimum 40 cas complets, sinon ARRÊT** (le seuil de 40 est le
   minimum fast du pipeline v6.2 ; n attendu 153).
4. Fichiers produits :
   - `pdac_882_gbm_prolif_fluxes.csv` : `step` (0..n−1, ordre
     prolifération croissant) + 12 gènes v4, valeurs log2.
   - `pdac_882_gbm_prolif_fluxes_nul.csv` : mêmes lignes permutées,
     graine 42 (même construction que tous les nuls du dossier).
   - `pdac_882_gbm_privilege_fluxes.csv` : `step` (ordre score de
     privilège croissant) + 12 gènes v4.
   - `pdac_882_gbm_privilege_fluxes_nul.csv` : nul graine 42.
   - `gbm_882_direct_table.csv` : par patient (code TCGA anonymisé
     en rang, pas d'identifiant clinique) : step prolifération, score
     de prolifération, score de privilège, score froid, les 7 gènes
     de privilège, les 12 gènes immunitaires, les 12 gènes v4
     (valeurs log2, dans l'ordre prolifération).
   - Contrôle anti-doublon (§8.44) : le contrôle du pipeline est la
     colonne `step` ; ni le score de prolifération ni le score de
     privilège ne figurent parmi les 12 flux analysés — il n'y a pas
     de doublon contrôle/flux dans ce chantier, et c'est vérifié par
     assertion dans le script (les 12 colonnes de flux sont
     exactement les 12 gènes v4).
5. SHA-256 de chaque CSV consigné dans `PROVENANCE_882.md`.

## 4. Tests directs (1) — les gènes de privilège montent-ils avec l'agressivité ?

Script `direct_tests_882.py` (SHA noté), sur `gbm_882_direct_table.csv`
(réel seulement ; le nul ne sert qu'au pipeline) :

1. **Test informatif (correction §8.70) :** corrélation de Spearman de
   chaque gène de privilège avec le pas de prolifération (ordre
   croissant), rho + p bilatérale (scipy). Table complète des 7 gènes,
   sans sélection. Médiane des 7 rho ; nombre de rho > 0 ; nombre de
   p < 0,05.
2. **Top-quartile vs reste :** pour chaque gène de privilège,
   différence (quartile supérieur de prolifération, n≈38, moins le
   reste) en écart-type, test de Welch (p descriptive). Table complète.
3. **Score de privilège lui-même :** Spearman(score de privilège, pas
   de prolifération) — attendu positif par construction partielle ?
   NON : le score de privilège est une moyenne de z-scores, le pas est
   l'ordre de prolifération — aucune contrainte mathématique ne lie
   les deux. Rapporté comme un 8e test, avec sa p.
4. **d de Cohen marginal (réel vs nul, pipeline) :** rapporté tel quel,
   attendu vacueux (≈ 0,0000) — il valide la construction du nul, il
   ne mesure pas l'ordre et ne décide rien (§8.70).

**Catégories de verdict direct (gelées, sur la médiane des 7 rho) :**

| Catégorie | Condition gelée | Lecture |
|---|---|---|
| MONTE | médiane rho ≥ +0,15 ET ≥ 4/7 rho > 0 | les gènes de privilège montent avec l'agressivité dans le GBM |
| PLAT | \|médiane rho\| < 0,10 | pas de lien monotone avec l'agressivité |
| DESCEND | médiane rho ≤ −0,15 ET ≥ 4/7 rho < 0 | les gènes de privilège descendent quand l'agressivité monte |
| INDÉTERMINÉ | entre les deux | signal faible, ni montée ni plat — dit tel quel |

Le seuil +0,15 est choisi parce qu'à n≈153, |rho| ≈ 0,16 est le seuil
de p < 0,05 (Spearman) : une médiane à +0,15 est donc un signal dont
la moitié des gènes est individuellement au bord de la significativité.
Aucun ajustement de ces seuils après avoir vu les chiffres.

## 5. Tests directs (2) — le glioblastome est-il « froid » de la même façon ?

Même script, mêmes définitions que le §8.23, transposées à l'axe
prolifération :

1. Spearman de chacun des 12 gènes immunitaires avec le pas de
   prolifération (rho + p). Table complète, sans sélection.
2. Spearman du score froid (moyenne z de CD8A, CD4, FOXP3, PDCD1)
   avec le pas. Top-quartile vs reste en sd (Welch p descriptive)
   pour PDCD1 et CD8A (les deux marqueurs les plus forts au §8.23).
3. CD274/PD-L1 seul : Spearman + top-quartile — au §8.23 il ne montait
   qu'en TCGA (+0,26) et était plat ailleurs ; la question est posée
   de la même façon ici.

**Catégories de verdict froid (gelées, sur la médiane des 4 rho du
score froid) :**

| Catégorie | Condition gelée | Lecture |
|---|---|---|
| FROID | médiane rho ≤ −0,10 ET ≥ 3/4 rho < 0 | froid comme le pancréas (référence TCGA : CD8A −0,19, CD4 −0,15, FOXP3 −0,10, PDCD1 −0,25 ; médiane ≈ −0,17) |
| PAS FROID | médiane rho > −0,05 | pas de baisse des T avec l'agressivité |
| INDÉTERMINÉ | entre les deux | baisse faible, dite telle quelle |

## 6. Bras pipeline v6.2 — la chaîne PDAC apparaît-elle dans le GBM ?

- Lot : 4 runs — paire primaire (prolifération, réel + nul) et paire
  secondaire (privilège, réel + nul) — manifeste `manifest_v62_882.txt`,
  lanceur reprenable existant `run_v62_lot.sh` (saute les sorties déjà
  complètes), journal `runs_v62_882.log` (SHA du pipeline en tête,
  exits consignés).
- Dossiers : `results_fast_v62_882_gbm_prolif`,
  `results_fast_v62_882_gbm_prolif_nul`,
  `results_fast_v62_882_gbm_privilege`,
  `results_fast_v62_882_gbm_privilege_nul`
  (nuls frais éventuels : `..._prolif_nul_s8821` / `..._prolif_nul_s8822`).
- Lancement en `systemd-run --unit=v62-882 --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance qui
  s'arrête d'elle-même à 4/4 (ou 6/6 si nuls frais). Ne JAMAIS
  supprimer le dossier d'un run en cours. Si la machine redémarre,
  reprise sans perte (SKIP des dossiers complets, jamais de relance
  à l'aveugle).
- SHA du pipeline revérifié avant ET après le lot.
- Mode fast, graine 42 pour les deux nuls (construction), contrôle
  `step` (repli automatique du pipeline sur la première colonne
  numérique, comme dans tous les lots précédents), cible = premier
  flux numérique hors contrôle (PGC, comme partout).

## 7. Critère de passage — GELÉ avant tout run

**La paire PRIMAIRE (prolifération) PASSE si et seulement si :**
`d_maxsep = maxsep_R − maxsep_N > 0,07` (plancher, mêmes définitions
que §8.56.2 : `maxsep` = `best_config.metrics.max_separation`, |d de
Cohen| maximal du scan, lu sur le best_config ANCIEN) **ET**
`d_maxsep > 0` (positif — impliqué par > 0,07, consigné séparément).

**Catégories de verdict pipeline (gelées, paire primaire) :**

- **CONFIRME** : `d_maxsep > 0,07` — la chaîne PDAC (12 gènes v4)
  apparaît dans le GBM ordonné par agressivité.
- **PARTIEL** : `0 < d_maxsep ≤ 0,07` — positif mais sous le plancher
  (même catégorie que GSE71729, +0,0402, et GSE79668, +0,0567).
- **NON** : `d_maxsep ≤ 0` — négatif ou nul (même catégorie que
  GSE62452 et GSE21501).

**Paire secondaire (privilège) :** même calcul, rapporté, mais elle NE
CHANGE PAS le verdict : si la primaire échoue et la secondaire passe,
la section dit « chaîne visible quand on ordonne par privilège, pas par
agressivité » et le verdict reste celui de la primaire. Si les deux
passent, les deux sont rapportées. Aucune combinaison des deux paires
(en moyenne, en « au moins une ») n'est autorisée après coup.

**Nuls frais (règle gelée, reprise du §8.76) :** la paire graine 42 fait
le verdict, dans tous les cas. Si `d_maxsep` (paire primaire) est
PROCHE du plancher — défini comme `d_maxsep` dans [−0,07 ; +0,14[ —
les 2 nuls frais (graines 8821, 8822) sont courus sur la paire primaire
seulement, et les écarts `d` contre chaque nul frais sont rapportés
(min / médiane / max des 3 écarts). Lecture gelée : si les 3 écarts
sont > 0,07, le passage est dit « consolidé » ; si l'un des 3 est
≤ 0,07, le passage (ou l'échec) est dit « fragile, non consolidé » —
le verdict de la paire graine 42 n'est JAMAIS changé par les nuls
frais. Si `d_maxsep` est hors de [−0,07 ; +0,14[, aucun nul frais
n'est couru.

**Contrôles descriptifs (à publier, ne décident pas) :**
`sep` compagnon (= maxsep/(1+maxsep)), ancien MC (secondaire), S_sep,
Delta, L7a, cascade, falsification — affichés selon la convention
§8.64.6 (maxsep principal, ancien MC secondaire, sep compagnon,
mention de fragilité en tête de table). Falsification : disponible
seulement si n ≥ 75 — GBM n≈153, donc disponible ; sinon noter
« indisponible », ne pas imputer.

**Ce que le verdict change, et ce qu'il ne change pas (gelé) :**
- Le compte A2 des paires PDAC indépendantes NE CHANGE PAS (8/12,
  10/12 positifs, LOO 7/11), quel que soit le verdict. Le GBM n'y
  entre pas — autre cancer, pas une cohorte pancréatique.
- **C3 reste LEVÉE** dans tous les cas ; le test C reste NON ; l'adoption
  pleine de maxsep reste la décision de Zackary du 20 nov. 13h04.
- Aucune affirmation clinique : l'étude porte sur l'instrument et sur
  la question « le privilège immunitaire se comporte-t-il pareil dans
  un deuxième site ? », pas sur un remède.

## 8. Extraction et vérification

1. Extracteur propre du chantier, `extract_882.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact, comme
   `extract_866.py` / `extract_869.py` / `extract_871.py` /
   `extract_874.py` / `extract_876.py`) ; lit `maxsep`, `mc_score`,
   `stability`, `ssep`, `delta`, `l7a`, cascade, falsification dans
   les 4 (ou 6) `master_results.json` ; sorties `extract_882.json` /
   `extract_882.csv`.
2. Second calcul indépendant : relecture directe des
   `master_results.json` par un chemin distinct (script `verify_882.py`,
   SHA noté) — `maxsep` et ancien MC recoupés à 0,0 exact ; tout écart
   = résultat à diagnostiquer, pas un bruit.
3. Recoupements : les valeurs du §8.23 et du §8.56 reprises telles
   quelles du livre blanc, jamais recalculées ici — ce chantier ne
   re-vérifie pas les §8.23/§8.56/§8.59/§8.64 (déjà clos).
4. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 9. Tests directs en appui (ne décident pas)

Script `direct_tests_882.py` (SHA noté), sur les CSV de flux du
chantier (réel + nul graine 42) :

1. **Test informatif (correction §8.70, appliquée ici) :**
   corrélation de Spearman de chaque flux v4 avec le pas (ordre de
   prolifération, puis ordre de privilège pour la paire secondaire),
   réel vs nul : |ρ| moyen, Δρ médian, nombre de Δρ positifs (sur 12),
   table complète sans sélection. C'est le test qui porte
   l'information d'ordre.
2. d de Cohen marginal des 12 flux (réel vs nul) : pour chaque gène v4,
   moyenne et écart-type des valeurs ordonnées, d de Cohen réel−nul ;
   table complète, sans sélection. **Attendu vacueux par construction :
   d = 0,0000 pour les 12 gènes** (le nul est une permutation des
   lignes). Rapporté tel quel : il valide la construction du nul
   (marginales préservées exactement), il ne mesure pas la séparation.
3. Comparaison descriptive avec le pancréas (TCGA v4, §8.56) : `maxsep`
   réel/nul, MC, Delta, Δρ médian — reprise des valeurs du §8.56
   telles quelles, jamais recalculées.

## 10. Fichiers produits (liste gelée)

- `PROTOCOL_cerveau_privilege_882.md` (ce fichier).
- `PROVENANCE_882.md` (source GBM, MD5/SHA, construction, SHAs des CSV).
- `build_fluxes_gbm_882.py`, `direct_tests_882.py`, `extract_882.py`,
  `verify_882.py`.
- `pdac_882_gbm_prolif_fluxes.csv` (+ `_nul.csv`),
  `pdac_882_gbm_privilege_fluxes.csv` (+ `_nul.csv`),
  `gbm_882_direct_table.csv`.
- `manifest_v62_882.txt`, `runs_v62_882.log`,
  `results_fast_v62_882_gbm_prolif(_nul)`,
  `results_fast_v62_882_gbm_privilege(_nul)`,
  `extract_882.json`, `extract_882.csv`.
- `section_8.82_cerveau_privilege.md` (verdict d'abord, chiffres ensuite).
