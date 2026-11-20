# PROTOCOLE — Infiltration par déconvolution indépendante (§8.54)

Date de gel : 20 novembre 2026 (avant tout calcul de ce chantier, avant tout nouveau run).
Chantier jumeau du §8.51 ; question ouverte du §8.51.10.
Règle permanente (27 oct. 2026) : provenance toujours nommée — source complète,
nature des lignes, comment chaque valeur a été produite, hachages des données,
et ce qui manque. Publication GitHub/PDF par le coordinateur, pas dans ce chantier.

## 1. Question (§8.51.10, restée ouverte)

§8.51 a établi que la corrélation intra-famille immunitaire (0,5563) n'est PAS
expliquée par la pureté tumorale telle que le projet la mesure (0,5480 après
régression, chute 1,5 % ; P-RES +0,9174, 93,3 % conservés). Reste ouverte la
seconde branche du §8.48.8 : l'infiltration immunitaire INDÉPENDANTE — un score
de déconvolution (CIBERSORT/xCell/TIMER) ou un score ESTIMATE immunitaire par
tumeur — explique-t-elle la corrélation ? Ce chantier teste cette branche.
Il ne re-teste pas la pureté (§8.51) et n'importe aucune conclusion d'une autre
expérience : seuls les chiffres de ce chantier (T1–T5 du jour) et les écarts
relus des §8.44/§8.48/§8.51 font le verdict.

## 2. Inventaire des sources (fait avant le gel)

### 2.1 Détenu avant le chantier : RIEN sur l'infiltration
Recherche dans `~/workspace/runs/pdac-v6/` (fichiers, scripts, provenances) :
0 occurrence de CIBERSORT, xCell, TIMER, ESTIMATE, déconvolution (hors le mot
« estimateurs » du pipeline, sans rapport). Aucun score d'infiltration détenu.

### 2.2 Sources externes publiées : TENTÉES, inaccessibles en accès direct
Toutes gratuites en principe, toutes bloquées par un obstacle d'accès concret
(en accès direct curl, sans navigateur vivant) — AUCUNE contournée, AUCUNE
donnée inventée pour les remplacer :
- **Yoshihara et al. 2013, Suppl. Data 2** (scores stromal/immunitaire/ESTIMATE
  publiés par tumeur TCGA, RNAseqV2 — la source externe idéale) et **Suppl.
  Data 1** (les 141+141 gènes) : fichiers `ncomms3612-s3.xlsx` (551,5 Ko) et
  `ncomms3612-s2.xlsx` (168,6 Ko), PMC3826632. Téléchargement PMC direct
  (`https://pmc.ncbi.nlm.nih.gov/articles/instance/3826632/bin/ncomms3612-s3.xlsx`)
  renvoie une page interstitielle « Preparing to download... » avec défi
  proof-of-work JS (cookie `cloudpmc-viewer-pow`) — non franchi en accès
  direct. Miroir Nature static-content essayé : 403 AccessDenied (objet
  inexistant sous le nom tenté). Europe PMC `supplementaryFiles` : 502 Bad
  Gateway. Statut : ACCESSIBLE PAR NAVIGATEUR VIVANT (tâche pour le
  coordinateur, hors de ce chantier — subagent sans navigateur).
- **Aran et al. 2015, Suppl. Data 1** (pureté ESTIMATE/ABSOLUTE/LUMP/IHC/CPE
  par tumeur, `ncomms9971-s2.xlsx`, 540,1 Ko, PMC4671203) : même interstitiel
  proof-of-work PMC — même statut (navigateur vivant).
- **Thorsson et al. 2018 / CRI iAtlas** (fractions CIBERSORT 22 types,
  fraction leucocytaire, sous-types immunitaires, PMC5982584) : tableaux
  supplémentaires derrière le même interstitiel PMC ; l'API GraphQL iAtlas
  exige le package R `iatlasGraphQLClient` (pas de R sur cette machine) ;
  le magasin Synapse sous-jacent exige un compte. Statut : inaccessible ici.
- **TIMER / TIMER2.0** (Li et al.) : serveur web, pas de fichier de scores
  en vrac ; le lien historique de pureté `http://cistrome.org/TIMER/misc/AGPall.zip`
  renvoie 404 Not Found. Statut : mort.
- **CIBERSORTx** (Newman et al. 2019) : accès web, compte requis. Non tenté
  au-delà du constat (compte = hors périmètre). Statut : inaccessible ici.
- **UCSC Xena** : aucune route d'accès directe vérifiée sans navigateur dans
  ce chantier (datapages interactives). Statut : non vérifiée, nommée comme
  ouverte.
Les fichiers HTML d'échec ont été supprimés ; rien de ces tentatives n'entre
dans les calculs. Si le coordinateur récupère les scores publiés de Yoshihara
par navigateur, la comparaison externe devient un chantier ultérieur (§8.54b),
pas un ajout rétroactif à celui-ci.

### 2.3 Voie retenue : ESTIMATE calculé depuis les données détenues (Voie C)
Faute de scores publiés accessibles, le score d'infiltration est CALCULÉ dans
ce chantier, par une méthode publiée, depuis la matrice d'expression détenue :
- **Entrée** : tarball TCGA-PAAD RSEM, Broad GDAC Firehose 2016-01-28,
  `data/tcga_paad_rsem.tar.gz`, MD5 `b09569ce3f4721f514bc137bd109ac0a` (vérifié).
  178 tumeurs primaires (code 01), log2(RSEM+1) — la même matrice que §8.51.
- **Méthode** : ESTIMATE (Yoshihara et al., Nat Commun 2013, doi
  10.1038/ncomms3612) — ssGSEA (Barbie et al., Nature 2009) sur deux
  signatures publiées de 141 gènes chacune (stromale, immunitaire).
  Implémentation : PORT PYTHON FIDÈLE de `tidyestimate::estimate_score`
  (Aragaki, CRAN 1.1.1, 2023), code source lu en clair
  (`R/estimate_score.R`, GitHub KaiAragaki/tidyestimate, main) :
  rangs par échantillon (ex æquo moyennés), rangs remis à l'échelle
  10000/n, ssGSEA exposant 0,25, ES = somme des écarts cumulés
  (récompense des hits − pénalité des non-hits). Filtre aux gènes communs
  aux six plateformes (10 391 symboles HGNC uniques) avant le calcul,
  comme dans `filter_common_genes` (appariement d'alias conservateur :
  NON appliqué — les symboles TCGA sont déjà HGNC ; le nombre de gènes
  communs trouvés est rapporté, et les gènes manquants sont listés).
  `is_affymetrix = FALSE` : pas de conversion en pureté (formule cosinus
  réservée aux puces Affymetrix par Yoshihara) — les scores sont relatifs,
  comme le prescrit la méthode pour le RNA-seq. Le filtre aux gènes communs
  est appliqué AVEC l'appariement d'alias conservateur de tidyestimate
  (`find_alias = TRUE`, tel qu'utilisé dans la vignette : ov = 9 903 gènes
  exacts + 461 récupérés par alias = 10 364 sur 10 391) — port Python fidèle
  de `find_alias` dans `estimate_ssgsea.py` : un gène commun manquant n'est
  récupéré via un synonyme que si ce synonyme ne correspond qu'à UN gène
  des données ET que ce gène des données ne correspond qu'à UN gène commun.
  Les renommages par alias sont listés dans les sorties JSON.
  [Amendement du 20 nov. 2026, AVANT tout calcul T1–T5 : la première version
  de ce protocole disait l'alias NON appliqué ; la porte J a montré que la
  vignette de référence l'applique (461/488 gènes manquants récupérés) —
  sans lui, la validation du port sur `ov` est impossible. Le critère de
  validation (1 % relatif sur s516/s520) est inchangé.]
- **Signatures** : `tidyestimate` 1.1.1, tarball CRAN
  `tidyestimate_1.1.1.tar.gz`, SHA-256
  `cc747f787b6548a62219f3388ff6d93ad93cfcb60fe75f322fd712f41509514b`,
  fichiers `data/gene_sets.rda` (SHA-256
  `5d058439aed4f074b49d623c5bc4ebfbaceab79766249dd87f280c62d1c0469a`) et
  `data/common_genes.rda` (SHA-256
  `f09453b2f12808b0dad73847390593cfee31142eb7490aa81e9d59aa0cba2ff3`),
  lus en Python avec le parseur `rdata` (venv dédié `/tmp/venv854`,
  pas de R sur cette machine). Les listes extraites sont sauvegardées en
  texte clair (`infiltration_854_gene_sets.csv`, 141+141 gènes) avec leurs
  SHA. Les mises à jour d'alias de tidyestimate sont conservées (ex. FYB→
  FYB1, WISP1→CCN4) et nommées dans la section.
- **Recouvrement / circularité (vérifié à l'inventaire, avant le gel)** :
  la signature immunitaire (141 gènes) ne contient qu'UN des 12 gènes de
  flux : GZMB. La signature stromale n'en contient qu'un : CD163. Les deux
  signatures sont disjointes (recouvrement 0). Le score immunitaire est
  donc indépendant des flux à 140/141 gènes près — et la variante
  « leave-12-out » (ImmuneScore_wo12 : signature immunitaire moins GZMB,
  140 gènes) est le test strictement non circulaire, pré-enregistré.
- **Base immunitaire** (inchangée) : `pdac_immune_tcga_fluxes.csv`, n = 178,
  SHA-256 `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e` ;
  axe `immune_kras_order_tcga.csv`, SHA-256
  `31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d` ;
  12 gènes bruts log2(RSEM+1) : CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274,
  PDCD1, CTLA4, GZMB, IFNG, CD19. Jointure PAR BARCODE, jamais par index.
- **Ce que « infiltration » veut dire ici (limite de mesure, gelée)** :
  l'ImmuneScore ESTIMATE est un score d'enrichissement ssGSEA sur 141
  gènes — une mesure ARN d'infiltration, pas un comptage de cellules.
  Il partage la mesure ARN avec les flux (même matrice), mais pas les
  gènes (140/141 indépendants) : une corrélation flux↔score n'est pas
  circulaire par construction. Il ne distingue pas les types cellulaires
  (pas de fractions CD8/macrophages/B) — ce que ferait CIBERSORT, toujours
  inaccessible. Le StromalScore (141 gènes, 0 gène de flux sauf CD163)
  sert de bras de contrôle (stroma, pas immunité).

## 3. Hypothèses gelées (avant les calculs)
- H1 (infiltration explique) : la corrélation intra-famille immunitaire est
  portée par la quantité de cellules immunitaires infiltrantes. Prédictions :
  (a) chaque flux immunitaire corrèle substantiellement avec l'ImmuneScore ;
  (b) après régression sur l'ImmuneScore, la corrélation intra-famille
  s'effondre ; (c) ordonner les flux immunitaires par l'ImmuneScore les
  sépare (S_sep au niveau IMMROT) ; (d) ordonner les flux RÉSIDUALISÉS par
  CD8A résidualisé ne sépare plus.
- H0 (propriété propre) : la corrélation persiste après contrôle de
  l'infiltration, par toutes les voies (a)–(d). La corrélation est alors une
  propriété des tumeurs (co-expression immunitaire), pas de leur
  composition en cellules infiltrantes.

## 4. Définitions gelées
- Scores par tumeur (n = 178) : ImmuneScore (ssGSEA, 141 gènes),
  ImmuneScore_wo12 (ssGSEA, 140 gènes, sans GZMB), StromalScore (ssGSEA,
  141 gènes), ESTIMATEScore = ImmuneScore + StromalScore (somme, comme
  dans Yoshihara). Le test principal porte sur ImmuneScore et sa variante
  wo12 ; StromalScore est un bras de contrôle ; ESTIMATEScore est descriptif.
- Résidus : pour chaque gène immunitaire g, OLS de g sur [1, ImmuneScore]
  (et variantes [1, ImmuneScore_wo12], [1, ImmuneScore, StromalScore]) ;
  résidu = observé − prédit.
- Couplage C (définition §8.48) : moyenne des |r de Pearson| entre le
  contrôle et les flux analysés. Cohésion H : moyenne des |r| sur les 66
  paires intra-famille. Références relues (non recalculées) : corrélation
  brute 0,5563 ; IMMROT sans doublon, moyenne +0,7521, minimum +0,4508
  (CD68), CD8A écart +0,9838 (réel 1,2310, nul 0,2472) ; P-RES §8.51
  +0,9174 ; régression §8.48 : d_ssep = −0,175 + 1,705·C.
- Nul du projet : bloc analysé permuté conjointement, default_rng(42),
  colonne de contrôle intacte (même construction que §8.41/§8.44/§8.48/§8.51).

## 5. Tests gelés et critères de décision (avant les calculs)

### Porte J (jointure + validation du port, AVANT tout test)
(a) Tarball rechargé (MD5 vérifié), 178 tumeurs primaires, 0 NaN sur KRAS +
12 gènes immunitaires ; ordre KRAS brut recalculé = `immune_kras_order_tcga.csv`
(178/178 barcodes) ; valeurs immunitaires reproduites depuis le tarball à
10⁻⁹ près. (b) Signatures : 141 + 141 gènes, disjointes, 1 seul gène de flux
dans chacune (GZMB immunitaire, CD163 stromale) — vérifié à l'inventaire,
re-vérifié en machine. (c) VALIDATION DU PORT : le port Python ssGSEA,
appliqué aux données de test `ov` de tidyestimate (17 256 gènes × 10
échantillons, `data/ov.rda`, SHA-256
`3fe246dbf5c9e1fd73c2a4d094e72d415d06b0018589be9dea341efa572b7478`),
reproduit les scores publiés de la vignette à 1 % relatif près (s516 :
stromal −285,50, immune +165,75 ; s520 : stromal +1927,51, immune +2326,16 ;
après le même filtre aux gènes communs). (d) Nombre de gènes communs
trouvés dans la matrice TCGA et nombre de gènes de signature présents
rapportés. J est OUVERTE si et seulement si (a)–(c) tiennent. Si J est
FERMÉE : arrêt du chantier, raison consignée.

### T1 — Chaque flux immunitaire suit-il l'infiltration ?
Pearson r + Spearman ρ (+ p bilatérale) de chaque flux contre ImmuneScore,
contre ImmuneScore_wo12 et contre StromalScore ; R² par flux (OLS sur
[ImmuneScore] et sur [ImmuneScore, StromalScore]) ; moyenne des |r| sur les
12 flux, pour chaque score. Critère : lien substantiel si moyenne |r| ≥ 0,30
pour l'ImmuneScore (ou sa variante wo12) ; lien faible si < 0,15 pour les
deux scores immunitaires. Descriptif : r(ImmuneScore, score_acineux) et
r(ImmuneScore, score_ilots) — l'infiltration re-mesure-t-elle les proxys de
pureté du §8.51 ? (Contexte, pas un critère de verdict.)

### T2 — La corrélation intra-famille survit-elle à la régression infiltration ?
Matrice 66 paires : brute vs résidus [ImmuneScore] (et sensibilités
[ImmuneScore_wo12], [ImmuneScore, StromalScore]). Rapportés : moyenne |r|,
médiane |r|, fraction |r| > 0,5. Critère gelé (même que §8.51) :
EFFONDREMENT si moyenne |r| résiduelle < 0,30 (chute ≥ 45 % depuis 0,5563)
ET fraction > 0,5 < 0,20 ; PERSISTANCE si chute < 20 % (moyenne résiduelle
> 0,44) ; entre les deux : partielle, à dire.

### T3 — Couplage prédit (sans nouveau run)
C par contrôle immunitaire avant/après résidualisation sur ImmuneScore
(12 contrôles) ; d_ssep prédit par la régression §8.48
(d = −0,175 + 1,705·C), moyenne prédite brute (doit retrouver ≈ +0,75,
sanité) vs résidualisée. Descriptif, pas un verdict seul.

### T4 — Stratification par infiltration (non paramétrique)
Médiane de l'ImmuneScore (n = 89/89) et médiane de l'ImmuneScore_wo12 :
matrice intra-famille dans chaque moitié (moyenne |r|, fraction > 0,5).
Critère : si la cohésion venait de l'infiltration, elle devrait s'effondrer
dans chaque moitié (bande d'infiltration étroite) ; persistance dans les
deux moitiés = argument contre H1, indépendant de toute linéarité.

### T5 — Runs v6.2 (6 maximum, prédictions AVANT lecture des sorties)
CSV construits par `build_infiltration_854.py` (nuls graine 42, construction
du projet) :
- I-IMM : contrôle ImmuneScore, analysés = 12 flux immunitaires bruts,
  lignes triées par ImmuneScore croissant. Réel + nul (2 runs).
- I-STR : contrôle StromalScore, idem. Réel + nul (2 runs).
- I-RES : contrôle CD8A RÉSIDUALISÉ ([1, ImmuneScore]), analysés = 11 autres
  flux RÉSIDUALISÉS (sans doublon, comme §8.44/§8.51). Réel + nul (2 runs).
Prédictions (calculées à partir de T1/T2 AVANT de lire les sorties) :
d_pred = −0,175 + 1,705·C_mesuré pour I-IMM/I-STR (C = moyenne |r| entre le
score et les 12 flux) ; pour I-RES, d_pred depuis C_résid, et comparaison
directe à CD8A IMMROT observé (+0,9838) et à P-RES §8.51 (+0,9174).
Critères gelés : I-IMM ou I-STR SOUTIENT H1 si son écart S_sep ≥ 0,45
(minimum IMMROT sans doublon) ; I-RES SOUTIENT H1 si son écart < 0,30
(moyenne des autres familles) ; I-RES SOUTIENT H0 si son écart ≥ 0,45.

### Verdict de synthèse (règle gelée)
- H1 SOUTENUE (infiltration explique, en totalité) si T2 = effondrement ET
  I-RES < 0,30 ET (I-IMM ≥ 0,45 OU I-STR ≥ 0,45).
- H1 PARTIELLE si T2 = partielle OU (I-IMM/I-STR entre 0,30 et 0,45) avec
  I-RES réduit (écart < 0,70, sous les 0,9838 de CD8A brut).
- H0 SOUTENUE (propriété propre aux tumeurs) si T2 = persistance ET
  I-IMM < 0,30 ET I-STR < 0,30 ET I-RES ≥ 0,45.
- Toute autre combinaison : zone grise, à dire comme telle, test par test.
Aucun consensus exigé entre les tests : chaque test est rapporté avec son
propre critère ; le verdict suit la règle ci-dessus, pas un vote.

## 6. Nouveaux runs : 6 maximum
Mode fast, graine 42 (défaut pipeline), pipeline v6.2
SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
jamais modifié, vérifié avant et après les runs. Lanceur existant
`run_v62_lot.sh` + manifeste `manifest_v62_infiltration_854.txt`, log
`runs_v62_infiltration_854.log`, unité systemd-run `v62-infil-854`
(+ relance reprenable si mort d'unité ; jamais de nohup — leçon du 17 nov.).
Sorties `results_fast_v62_infil854_*`. Extraction par script dédié
`extract_infiltration_854.py` (mêmes champs que `extract_purity_851.py` :
max_separation, stability, S_sep = produit).

## 7. Vérifications gelées
- SHA-256 du pipeline v6.2, de la base immunitaire, du fichier d'axe, du
  tarball (MD5), du tarball tidyestimate et des deux .rda : revérifiés par
  les scripts avant tout calcul ; tout mismatch arrête le chantier (à dire
  dans la section).
- Validation du port ssGSEA sur les données `ov` (Porte J, critère 1 %) :
  sans elle, aucun score n'est utilisé.
- Aucune valeur S_sep recopiée à la main ; écarts §8.48/§8.51 relus en
  machine dans `immrot_848_correlations.csv` / `ssep_844_rotations.csv` /
  `purity_851_runs.json`.
- Aucune conclusion d'une autre expérience n'est importée : seuls les
  chiffres de ce chantier (T1–T5 du jour) et les écarts relus font le verdict.
- Aucun seuil nouveau, aucune sélection d'indicateur après coup.

## 8. Livrables
1. Ce protocole (SHA noté dans le rapport final).
2. Section §8.54 : `~/workspace/runs/pdac-v6/section_8.54_infiltration.md`.
3. Scripts : `analyze_infiltration_854.py` (porte J, T1–T4),
   `build_infiltration_854.py` (scores + 6 CSV),
   `extract_infiltration_854.py`, `estimate_ssgsea.py` (port ssGSEA).
4. Données : `infiltration_854_gene_sets.csv` (signatures en clair),
   `infiltration_854_scores.csv` (178 tumeurs : barcode, ImmuneScore,
   ImmuneScore_wo12, StromalScore, ESTIMATEScore),
   `infiltration_854_results.json/.csv` (T1–T4 + 6 runs),
   `infiltration_854_csv_sha.json`, manifeste + log du lot ;
   `data_infiltration_854/` : tarball tidyestimate + .rda + scripts R lus.
5. Aucun push GitHub, aucune modification du livre blanc, aucune touche à
   tlogNext-pdac-phase2.

## 9. Ce qui manque (connu d'avance)
- Pas de scores publiés externes (Yoshihara Suppl. Data 2, Aran Suppl.
  Data 1, Thorsson CIBERSORT/LF) : inaccessibles en accès direct (défi
  proof-of-work PMC, R-Forge 403, TIMER 404, iAtlas = R + compte Synapse).
  La comparaison de mes scores calculés aux scores publiés de Yoshihara
  (même méthode, mêmes données TCGA RNAseqV2) reste à faire — chantier
  ultérieur, par navigateur vivant.
- Pas de fractions par type cellulaire (CIBERSORT/xCell) : l'ImmuneScore
  est un score global ; il ne dit pas si ce sont les T CD8, les
  macrophages ou les B qui portent la corrélation.
- n = 178 : corrélations estimées sur 178 points ; les moitiés T4 sont
  à n = 89 (incertitude plus grande, le dire).
- Les scores ESTIMATE partagent la mesure ARN avec les flux : une
  corrélation n'est pas une causalité ; T4/T5 sont les garde-fous.
  La variante wo12 (140 gènes) est le garde-fou de circularité.
- Ce chantier ne teste pas le sous-type moléculaire (autre variable
  latente du §8.48.8).
