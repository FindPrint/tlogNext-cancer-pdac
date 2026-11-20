# PROTOCOLE — Déconvolution par type cellulaire (§8.60)

Date de gel : 20 novembre 2026 (avant tout téléchargement de ce chantier,
avant tout calcul de ce chantier, avant tout nouveau run).
Chantier §8.60 du projet PDAC (go du coordinateur, 20 nov. 2026).
Question ouverte des §8.54.8(e) et §8.55.11 : « Cela ne dit pas quelles
cellules portent la corrélation : pas de fractions par type cellulaire
(CIBERSORT/xCell toujours inaccessibles) — T CD8, macrophages ou B, la
question reste ouverte. »
Règle permanente (27 oct. 2026) : provenance toujours nommée — source
complète, nature des lignes, comment chaque valeur a été produite, hachages
des données, et ce qui manque. Publication GitHub/PDF par le coordinateur,
pas dans ce chantier. Ne jamais modifier v6 / v6.1 / v6.2 ; aucune
modification du livre blanc ici ; ne pas toucher à tlogNext-pdac-phase2.

## 1. Question

Le §8.54 a établi que la corrélation intra-famille immunitaire (0,5563)
est expliquée par l'infiltration immunitaire GLOBALE (ImmuneScore ESTIMATE
calculé : 0,5563 → 0,2002 après régression, chute 64,0 % ; I-RES +0,1982,
20,2 % conservés). Le §8.55 a établi que la pureté ABSOLUTE externe en
explique environ un tiers (0,5040 → 0,3757, chute 25,5 % ; E-RES +0,6499).
Reste ouverte la composition de l'infiltrat : QUELS types cellulaires
portent la corrélation — lymphocytes T CD8, macrophages, lymphocytes B,
fibroblastes / stroma, autres ? Ce chantier teste cette question. Il ne
re-teste ni l'ImmuneScore global (§8.54) ni ABSOLUTE (§8.55) et n'importe
aucune conclusion d'une autre expérience : seuls les chiffres de ce
chantier (Porte D, T1–T5 du jour) et les écarts relus des §8.44/§8.48/
§8.51/§8.54/§8.55 font le verdict.

## 2. Inventaire des sources (fait avant le gel)

### 2.1 Détenu avant le chantier : AUCUNE fraction par type cellulaire
Recherche dans `~/workspace/runs/pdac-v6/` (fichiers, scripts, provenances,
§8.54.1 / §8.55.2) : 0 occurrence de fractions CIBERSORT, xCell, TIMER,
MCP-counter, EPIC, quanTIseq par échantillon. Les seuls scores détenus
sont globaux : ImmuneScore / StromalScore ESTIMATE calculés (§8.54,
`infiltration_854_scores.csv`, SHA `628732ec…aa7`) et pureté ABSOLUTE
externe (§8.55, `purity_855_external.csv`, SHA `03f34fe0…bd6f`).

### 2.2 Détenu, non encore testé comme contrôle d'infiltration : fraction leucocytaire par méthylation
Le `sampInfo` transcrit au §8.55 (`purity_855_sampinfo.csv`, SHA
`7a09dde3…b014`, 181 lignes × 55 colonnes, transcription mécanique du
`TCGA_PAAD.rds` de pdacR, lui-même issu de la Table S1 de Raphael et al.
2017) contient la colonne `DNA.methylation.leukocyte.percent.estimate`
(colonne 16/55, vérifiée à l'en-tête avant le gel). C'est une estimation
de la fraction leucocytaire par méthylation ADN — indépendante de l'ARN,
donc non circulaire avec les flux — mais GLOBALE (tous leucocytes
confondus), pas par type cellulaire. Elle ne peut pas répondre seule à
la question « quel type », mais elle constitue un bras secondaire gelé
(§7, bras L) : infiltration indépendante, déjà détenue, testable sans
aucun téléchargement.

### 2.3 Sources externes candidates (ordre de priorité, gelé)
1. **Thorsson et al. 2018, Immunity 48(4):812–830.e14** — « The Immune
   Landscape of Cancer », doi 10.1016/j.immuni.2018.03.023, PMC5982584 :
   fractions CIBERSORT (22 types leucocytaires, LM22) + fraction
   leucocytaire par échantillon TCGA, tableaux supplémentaires. Accès
   visés : (a) Europe PMC `supplementaryFiles` — route PROUVÉE au §8.55
   pour Aran et al. (zip obtenu, SHA noté) ; (b) téléchargement direct
   PMC (défi proof-of-work attendu, cf. §8.54.1 — tenté, documenté, non
   contourné) ; (c) fichiers `mmc` Cell Press. Source prioritaire : c'est
   la seule qui donne des fractions CIBERSORT publiées par échantillon
   pour PAAD.
2. **TIMER2.0 (Li et al. 2020, Nucleic Acids Res, doi 10.1093/nar/gkaa407)**
   — estimations d'infiltration pour TCGA par six méthodes (TIMER,
   CIBERSORT, xCell, MCP-counter, EPIC, quanTIseq). Accès visés : pages
   de téléchargement `timer.cistrome.org` / `cistrome.shinyapps.io/timer`,
   fichier en vrac par cancer si existant (URL exacte notée). Serveur
   web interactif seul = insuffisant (pas de scores en vrac → source
   écartée, documentée).
3. **xCell (Aran, Hu, Butte 2017, Genome Biol, doi 10.1186/s13059-017-1349-1)**
   — scores xCell (64 types cellulaires) pan-cancer TCGA. Accès visés :
   supplément de l'article, dépôt GitHub / Zenodo du package xCell,
   miroirs publics identifiables (mêmes colonnes, couverture pan-cancer,
   URL + hash notés).
4. **Voie C (repli, calcul depuis la matrice détenue — PAS des scores
   publiés).** Si et seulement si 1–3 échouent : déconvolution calculée
   dans ce chantier depuis le tarball TCGA-PAAD RSEM détenu (MD5
   `b09569ce…ac0a`), avec des signatures publiées : MCP-counter (Becht
   et al. 2016, Nat Commun, doi 10.1038/ncomms13404 — 10 populations,
   marqueurs publiés), EPIC (Racle et al. 2017, eLife, doi
   10.7554/eLife.26476 — 7 types + fraction non caractérisée) ou
   CIBERSORT-LM22 (Newman et al. 2015, Nat Methods, doi
   10.1038/nmeth.3337 — 547 gènes, 22 types ; matrice LM22 depuis une
   source publique identifiable, URL + SHA notés). Toute valeur calculée
   par cette voie est étiquetée « calculée, pas publiée », jamais
   présentée comme score publié.
5. **Autres miroirs publics** (dépôts GitHub, Zenodo, Figshare, R packages
   avec données TCGA embarquées, ex. `IOBR`, `immunedeconv` — données
   d'exemple seulement, à vérifier) : acceptés seulement si le fichier
   est identifiable comme les fractions publiées d'une des sources 1–3
   (mêmes colonnes, mêmes valeurs de contrôle), avec URL et hash notés.

### 2.4 Critères d'acceptation d'une estimation par type cellulaire
- Fichier téléchargeable gratuitement, sans compte et sans paiement.
- Scores par échantillon TCGA identifiables par barcode (échantillon ou
  patient), avec méthode + version + référence nommées.
- Couverture appariée ≥ 100 tumeurs sur nos 178 (Porte D, §4).
- Valeurs documentées : fractions dans [0, 1] (CIBERSORT, EPIC,
  quanTIseq) ou scores d'enrichissement à échelle documentée (xCell,
  MCP-counter) — toute valeur hors intervalle documenté est signalée
  et exclue, jamais corrigée silencieusement.
- URL exacte, date/heure UTC, taille en octets, SHA-256 du fichier
  téléchargé notés ; fichier brut jamais modifié.
- **Circularité (gelée).** Les fractions publiées sont calculées depuis
  des signatures qui CONTIENNENT certains des 12 gènes de flux (ex.
  CD8A/CD8B dans LM22, CD19, CD68/CD163 dans les marqueurs
  macrophagiques) : le recouvrement signature ∩ 12 flux est compté en
  machine et rapporté par type (nombre de gènes de flux dans la
  signature du type, sur 12). Pour la Voie C, la variante
  « leave-12-out » (signature moins les 12 gènes de flux) est
  OBLIGATOIRE et primaire : toute fraction calculée dont la signature
  perdrait tous ses marqueurs après retrait des 12 est déclarée
  incalculable par cette voie (à dire, pas contournée). L'interprétation
  tient compte du recouvrement : une fraction CD8 corrélant avec CD8A
  est en partie mécanique ; le test décisif reste T2/T5 — l'effondrement
  de la cohésion entre paires NE contenant PAS le gène marqueur (ex.
  CD4–FOXP3 après régression sur la fraction CD8) — rapporté
  explicitement (§7, T2-sensibilité « paires sans marqueur »).

## 3. Porte D (source) — AVANT tout test
- Tenter les sources 1–3 dans l'ordre ; noter pour chaque tentative :
  URL exacte, date/heure UTC, code HTTP / nature de la réponse, taille,
  SHA-256 si fichier obtenu. Les fichiers HTML d'échec sont supprimés ;
  rien de ces tentatives n'entre dans les calculs.
- **Porte D OUVERTE (bras principal)** si et seulement si : fichier
  obtenu + au moins une estimation par type cellulaire + couverture
  appariée ≥ 100 tumeurs sur 178 (jointure §4).
- **Porte D FERMÉE (bras principal)** : si aucune des sources 1–3 ne
  satisfait ces conditions après les tentatives documentées, ET que la
  Voie C (source 4) est elle-même impossible (signatures inaccessibles
  ou incalculables leave-12-out) → **arrêt du bras principal** : section
  §8.60 écrite avec le verdict « données par type cellulaire
  inaccessibles », journal des tentatives, AUCUNE valeur inventée,
  aucun run principal, aucun test sur des fractions fictives. Le bras
  secondaire L (fraction leucocytaire par méthylation, déjà détenue)
  est alors quand même exécuté (T1-L, T2-L, T5-L, §7) : c'est le seul
  résultat numérique nouveau du chantier dans ce cas, et il est
  rapporté comme tel — infiltration globale indépendante, pas par type.

## 4. Jointure (si porte D ouverte)
- Clé de jointure : barcode échantillon TCGA, sur les **15 premiers
  caractères** (`TCGA-XX-XXXX-01`, protocole §4 du §8.55) ; si une ligne
  externe n'a que 12 caractères, jointure sur les **12 premiers**
  (patient) — la règle appliquée par ligne est consignée, et toute
  collision (2 tumeurs pour 1 clé externe) est signalée et exclue.
- Vérifications : n apparié, n non apparié (listés par barcode),
  0 doublon de clé, valeurs dans l'intervalle documenté.
- Les analyses T1–T5 portent sur les tumeurs APPARIÉES uniquement
  (n ≤ 178, noté) ; la base immunitaire reste
  `pdac_immune_tcga_fluxes.csv` (SHA `66dbb672…bd2e`), restreinte aux
  lignes appariées, ordre KRAS brut conservé. La cohésion brute de
  référence est RECALCULÉE sur le sous-ensemble apparié, jamais
  importée du §8.54 (cf. §8.55 : 0,5563 à n = 178, 0,5040 à n = 149).

## 5. Définitions gelées (miroir des §8.51/§8.54/§8.55)
- Types cellulaires : chaque colonne de fraction/score par type de la
  source acceptée (CIBERSORT : 22 types ; xCell : jusqu'à 64 ; MCP-counter :
  10 populations ; EPIC : 7 types). Les types testés sont ceux de la
  source, sans sélection après coup sauf la règle du §7 (top par T1).
- Flux immunitaires : les 12 gènes bruts log2(RSEM+1) : CD8A, CD8B, CD4,
  FOXP3, CD68, CD163, CD274, PDCD1, CTLA4, GZMB, IFNG, CD19.
- Résidus : pour chaque gène immunitaire g, OLS de g sur [1, fraction(s)]
  (moindres carrés, n apparié) ; résidu = observé − prédit.
- Cohésion H : moyenne des |r de Pearson| sur les 66 paires
  intra-famille. Couplage C : moyenne des |r| entre le contrôle et les
  flux analysés (définition §8.48). Nul du projet : bloc analysé permuté
  conjointement, default_rng(42), colonne de contrôle intacte.
- Références relues (non recalculées) : H brute 0,5563 (n = 178) ;
  IMMROT sans doublon, moyenne +0,7521, minimum +0,4508 (CD68), CD8A
  écart +0,9838 (réel 1,2310, nul 0,2472) ; I-IMM +1,1942 ; I-STR
  +0,9407 ; I-RES +0,1982 ; P-RES +0,9174 ; E-RES +0,6499 ; régression
  §8.48 : d_ssep = −0,175 + 1,705·C.

## 6. Hypothèses gelées
- H1-type (un ou plusieurs types portent la corrélation) : la corrélation
  intra-famille est portée par la quantité d'un ou plusieurs types
  cellulaires infiltrants. Prédictions : (a) chaque flux immunitaire
  corrèle substantiellement avec au moins un type ; (b) après régression
  sur le(s) type(s) porteur(s), la corrélation intra-famille s'effondre ;
  (c) ordonner les flux immunitaires par la fraction du type porteur les
  sépare (S_sep au niveau IMMROT) ; (d) ordonner les flux RÉSIDUALISÉS
  par CD8A résidualisé ne sépare plus.
- H0-type (aucun type ne porte la corrélation) : la corrélation persiste
  après contrôle de chaque type et de leur combinaison, par toutes les
  voies (a)–(d). La corrélation est alors portée par l'infiltration
  globale sans type dominant identifiable, ou par une co-expression
  propre aux tumeurs.

## 7. Tests gelés et critères de décision (avant les calculs)

### T1 — Chaque flux immunitaire suit-il un type cellulaire ?
Pearson r + Spearman ρ (+ p bilatérale, brutes, sans correction pour
tests multiples — le jugement porte sur les moyennes, pas sur une p
isolée) de chaque flux contre chaque type ; R² par flux et par type
(OLS sur [type]) ; moyenne des |r| sur les 12 flux, POUR CHAQUE TYPE.
Critère : type « porteur candidat » si moyenne |r| ≥ 0,30 ; « faible »
si < 0,15 pour tous les types. Les types sont classés par moyenne |r|
décroissante ; TOP1 et TOP2 sont les deux premiers de ce classement
(égalité départagée par la moyenne des |ρ|). Descriptif : r(type,
ImmuneScore §8.54) et r(type, ABSOLUTE §8.55) — le type re-mesure-t-il
l'infiltration globale ou la pureté ? (Contexte, pas un critère.)

### T2 — La corrélation intra-famille survit-elle à la régression sur le(s) type(s) ?
Matrice 66 paires, sur les n appariées : brute vs résidus. PRIMAIRE :
résidus OLS sur [1, TOP1] (un seul type, le plus porteur). Sensibilités
gelées : (b) résidus sur [1, TOP1, TOP2, TOP3] (les trois types à plus
forte moyenne |r|, si ≥ 0,30, sinon les trois premiers quand même —
règle notée telle qu'appliquée) ; (c) résidus sur [1, tous les types à
moyenne |r| ≥ 0,30] (maximum 5 — au-delà, sur-ajustement : plafonné
aux 5 premiers) ; (d) paires sans marqueur : moyenne |r| résiduelle
recalculée sur les seules paires dont AUCUN des deux gènes n'est dans
la signature du TOP1 (garde-fou de circularité, §2.4).
Rapportés : moyenne |r|, médiane |r|, fraction |r| > 0,5. Critère gelé
(même que §8.54) : EFFONDREMENT si moyenne |r| résiduelle < 0,30
(chute ≥ 45 % depuis la brute appariée) ET fraction > 0,5 < 0,20 ;
PERSISTANCE si chute < 20 % (moyenne résiduelle > 0,80 × brute
appariée) ; entre les deux : partielle, à dire. Le verdict de synthèse
utilise le PRIMAIRE (a) ; (b)–(d) sont des sensibilités rapportées.

### T3 — Couplage prédit (sans nouveau run)
C par contrôle immunitaire avant/après résidualisation sur TOP1
(12 contrôles) ; d_ssep prédit par la régression §8.48
(d = −0,175 + 1,705·C), moyenne prédite brute (doit retrouver ≈ +0,75,
sanité) vs résidualisée. Descriptif, pas un verdict seul.

### T4 — Stratification par type porteur (non paramétrique)
Médiane du TOP1 (n ≈ moitiés) : matrice intra-famille dans chaque
moitié (moyenne |r|, fraction > 0,5). Critère : si la cohésion venait
du TOP1, elle devrait s'effondrer dans chaque moitié (bande de
fraction étroite) ; persistance dans les deux moitiés = argument contre
H1-type, indépendant de toute linéarité. Limite connue (§8.54.6) : une
médiane ne fait pas une bande étroite — l'écart-type résiduel dans
chaque moitié est rapporté, et T4 est dit non concluant si les moitiés
restent larges (> 50 % de l'écart-type global).

### T5 — Runs v6.2 (6 maximum pour le bras principal, prédictions AVANT lecture des sorties)
CSV construits par `build_deconvolution_860.py` (nuls graine 42,
construction du projet) :
- D-TOP1 : contrôle TOP1, analysés = 12 flux immunitaires bruts,
  lignes triées par TOP1 croissant. Réel + nul (2 runs).
- D-TOP2 : contrôle TOP2, idem. Réel + nul (2 runs).
- D-RES : contrôle CD8A RÉSIDUALISÉ ([1, TOP1]), analysés = 11 autres
  flux RÉSIDUALISÉS (sans doublon, comme §8.44/§8.51/§8.54). Réel + nul
  (2 runs).
Prédictions (calculées à partir de T1/T2 AVANT de lire les sorties) :
d_pred = −0,175 + 1,705·C_mesuré pour D-TOP1/D-TOP2 (C = moyenne |r|
entre le type et les 12 flux) ; pour D-RES, d_pred depuis C_résid, et
comparaison directe à CD8A IMMROT observé (+0,9838), à I-RES (+0,1982)
et à E-RES (+0,6499).
Critères gelés : D-TOP1 ou D-TOP2 SOUTIENT H1-type si son écart S_sep
≥ 0,45 (minimum IMMROT sans doublon) ; D-RES SOUTIENT H1-type si son
écart < 0,30 ; D-RES SOUTIENT H0-type si son écart ≥ 0,45.

### Bras secondaire L — fraction leucocytaire par méthylation (déjà détenue)
Source : `purity_855_sampinfo.csv`, colonne
`DNA.methylation.leukocyte.percent.estimate` (Raphael et al. 2017,
Table S1, via pdacR — provenance §8.55.2, SHA du .rds
`52020679…ea76`). Jointure par barcode sur 15 caractères, n apparié
compté en machine (attendu ≈ 150, comme ABSOLUTE ; seuil ≥ 100).
- T1-L : r/ρ de chaque flux contre la fraction leucocytaire ;
  moyenne |r| ; critère : lien substantiel si ≥ 0,30.
- T2-L : cohésion 66 paires brute (n apparié) vs résidus [1, leuco%] ;
  critères d'effondrement / persistance identiques à T2.
- T5-L : 2 runs v6.2 maximum (D-LEU réel + nul : contrôle fraction
  leucocytaire, analysés = 12 flux bruts, triés par fraction
  croissante). Prédiction d_pred par la régression §8.48, avant lecture.
  Critère : D-LEU soutient « infiltration indépendante » si écart
  ≥ 0,45.
- Le bras L NE CHANGE PAS le verdict par type (il ne distingue pas les
  types) ; il est rapporté séparément comme test d'infiltration
  indépendante de l'ARN. Si la Porte D est fermée, le bras L est le
  seul résultat numérique nouveau du chantier (§3).

### Verdict de synthèse (règle gelée, bras principal)
- H1-type SOUTENUE si T2 primaire = effondrement ET D-RES < 0,30 ET
  (D-TOP1 ≥ 0,45 OU D-TOP2 ≥ 0,45).
- H1-type PARTIELLE si T2 = partielle OU (D-TOP1/D-TOP2 entre 0,30 et
  0,45) avec D-RES réduit (écart < 0,70, sous les 0,9838 de CD8A brut).
- H0-type SOUTENUE si T2 = persistance ET D-TOP1 < 0,30 ET D-TOP2
  < 0,30 ET D-RES ≥ 0,45.
- Toute autre combinaison : zone grise, à dire comme telle, test par test.
Aucun consensus exigé entre les tests : chaque test est rapporté avec
son propre critère ; le verdict suit la règle ci-dessus, pas un vote.
Si la Porte D est fermée : verdict « DONNÉES PAR TYPE CELLULAIRE
INACCESSIBLES » (ni H1 ni H0) + verdict séparé du bras L selon ses
propres critères (T2-L + D-LEU).

## 8. Nouveaux runs : 8 maximum (6 principaux + 2 bras L)
Mode fast, graine 42 (défaut pipeline), pipeline v6.2
SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
jamais modifié, vérifié avant et après les runs. Lanceur existant
`run_v62_lot.sh` + manifeste `manifest_v62_deconvolution_860.txt`, log
`runs_v62_deconvolution_860.log`, unité systemd-run `v62-deconv-860`
(+ relance reprenable si mort d'unité ; jamais de nohup — leçon du
17 nov.). Sorties `results_fast_v62_deconv860_*`. Extraction par script
dédié `extract_deconvolution_860.py` (mêmes champs que
`extract_infiltration_854.py` : max_separation, stability,
S_sep = produit).

## 9. Vérifications gelées
- SHA-256 du pipeline v6.2, de la base immunitaire, du fichier d'axe, du
  tarball (MD5), du `sampInfo` : revérifiés avant tout calcul ; tout
  mismatch arrête le chantier (à dire dans la section).
- SHA-256 + taille + URL de tout fichier externe téléchargé ; couverture
  appariée comptée en machine, barcodes non appariés listés.
- Recouvrement signature ∩ 12 flux compté en machine par type (publié)
  ou par signature (Voie C, avec variante leave-12-out obligatoire).
- Aucune valeur S_sep recopiée à la main ; écarts §8.48/§8.51/§8.54/§8.55
  relus en machine dans `ssep_844_rotations.csv` / `purity_851_runs.csv` /
  `infiltration_854_runs.csv` / `purity_855_runs.csv`.
- Aucune conclusion d'une autre expérience n'est importée : seuls les
  chiffres de ce chantier (Porte D, T1–T5 du jour) et les écarts relus
  font le verdict.
- Aucun seuil nouveau, aucune sélection d'indicateur après coup. TOP1 /
  TOP2 sont définis par T1 AVANT les runs T5, pas choisis après les
  avoir vus.

## 10. Livrables
1. Ce protocole (SHA noté dans le rapport final).
2. Section §8.60 : `~/workspace/runs/pdac-v6/section_8.60_deconvolution.md`.
3. Scripts : `analyze_deconvolution_860.py` (porte D, jointure, T1–T4,
   bras L), `build_deconvolution_860.py` (CSV T5/T5-L),
   `extract_deconvolution_860.py`.
4. Données : fichier externe brut téléchargé (nommé avec sa source, SHA
   noté — jamais modifié), `deconvolution_860_external.csv` (tumeurs
   appariées : barcode + fractions par type + colonnes source),
   `deconvolution_860_results.json/.csv` (T1–T4 + bras L),
   `deconvolution_860_csv_sha.json`, manifeste + log du lot ;
   `data_deconvolution_860/` : signatures éventuelles (Voie C) + journal
   des tentatives `deconvolution_860_attempts.log`.
5. Aucun push GitHub, aucune modification du livre blanc, aucune touche à
   tlogNext-pdac-phase2.

## 11. Ce qui manque (connu d'avance)
- La disponibilité réelle des fractions CIBERSORT de Thorsson et al. en
  accès libre direct n'est pas établie avant la tentative : c'est
  l'objet de la porte D. Le §8.54 a échoué sur PMC (proof-of-work), le
  §8.55 a réussi via Europe PMC pour Aran — la même route est la
  première tentée ici.
- CIBERSORTx exige un compte (hors périmètre, cf. §8.54.1) ; le serveur
  TIMER2.0 est interactif, pas un fichier en vrac.
- n apparié ≤ 178 : si la couverture externe est partielle, les
  comparaisons se font sur le sous-ensemble apparié, avec la brute
  recalculée sur ce même sous-ensemble (jamais en mélangeant les n).
- Les fractions publiées partagent la mesure ARN avec les flux (même
  matrice TCGA) : une corrélation n'est pas une causalité ; T4/T5 sont
  les garde-fous, et la sensibilité « paires sans marqueur » (§7, T2d)
  est le garde-fou de circularité. La fraction leucocytaire par
  méthylation (bras L) est la seule mesure d'infiltration du chantier
  indépendante de l'ARN.
- Ce chantier ne teste pas le sous-type moléculaire (autre variable
  latente du §8.48.8), ni la survie par type cellulaire.
