# PROTOCOLE — xCell, 64 types de cellules (§8.68)

Date de gel : 20 novembre 2026 (avant tout téléchargement de ce chantier,
avant tout calcul de ce chantier, avant tout nouveau run).
Chantier §8.68 du projet PDAC (go de Zackary « Fait tout cela »,
20 nov. 2026 13h04 heure de Montréal, 18h04 UTC).
Question ouverte du §8.60.11 : « Confirmation indépendante par xCell
(64 types, dont fibroblastes / stroma). Les scores xCell précalculés
TCGA/TARGET (Aran et al. 2017, Additional file 6, PMC5688663) donneraient
un second bras par type, avec des types stromaux que CIBERSORT ne mesure
pas (fibroblastes, cellules endothéliales, adipocytes) — la question
« stroma ou immunité ? » reste ouverte côté stromal (le StromalScore
§8.54 est global, comme l'ImmuneScore). Chantier jumeau à geler
séparément. »
Règle permanente (27 oct. 2026) : provenance toujours nommée — source
complète, nature des lignes, comment chaque valeur a été produite, hachages
des données, et ce qui manque. Publication GitHub/PDF par le coordinateur,
pas dans ce chantier. Ne jamais modifier v6 / v6.1 / v6.2 ; aucune
modification du livre blanc ici ; ne pas toucher à tlogNext-pdac-phase2.

## 1. Question

Le §8.54 a établi que la corrélation intra-famille immunitaire (0,5563)
est expliquée par l'infiltration immunitaire GLOBALE (ImmuneScore ESTIMATE
calculé : 0,5563 → 0,2002 après régression, chute 64,0 % ; I-RES +0,1982,
20,2 % conservés). Le §8.60 a établi qu'aucun des 22 types CIBERSORT ne
porte la corrélation seul (TOP1 B naïfs +0,5867, TOP2 T CD8 +0,5609
ordonnent les flux, mais retirer le meilleur type ne retire que 4,7 %
de la cohésion ; D-RES +0,7692, 78,2 % du brut) — verdict ZONE GRISE —
tandis que la fraction leucocytaire globale par méthylation en retire
un tiers (−33,0 %, PARTIELLE). Reste ouverte la confirmation par une
seconde méthode de déconvolution, avec des types que CIBERSORT ne mesure
pas : QUELS types xCell (64 types, immunitaires + stromaux) portent la
corrélation — T CD8, macrophages, B, fibroblastes, endothélium, autres ?
Et la question stromale : un type stromal ordonne-t-il les flux, ou
l'effet est-il purement immunitaire ? Ce chantier teste ces questions.
Il ne re-teste ni l'ImmuneScore global (§8.54), ni ABSOLUTE (§8.55), ni
les fractions CIBERSORT (§8.60), et n'importe aucune conclusion d'une
autre expérience : seuls les chiffres de ce chantier (Porte D, T1–T5 du
jour) et les écarts relus des §8.44/§8.48/§8.51/§8.54/§8.55/§8.60 font
le verdict.

## 2. Inventaire des sources (fait avant le gel)

### 2.1 Détenu avant le chantier : AUCUN score xCell
Recherche dans `~/workspace/runs/pdac-v6/` (fichiers, scripts, provenances,
§8.54.1 / §8.55.2 / §8.60.1) : 0 occurrence de scores xCell par échantillon.
Les seuls scores par type détenus sont les fractions CIBERSORT publiées
(§8.60, `deconvolution_860_external.csv`, SHA `438d677a…9cf`) et les
scores globaux ESTIMATE calculés (§8.54, `infiltration_854_scores.csv`,
SHA `628732ec…aa7`).

### 2.2 Détenu, base de travail (vérifié avant le gel)
- Tarball TCGA-PAAD RSEM, Broad GDAC Firehose 2016-01-28, MD5
  `b09569ce3f4721f514bc137bd109ac0a` (re-vérifié en machine avant le gel,
  20 nov. 2026) — la même matrice que §8.54/§8.55/§8.60.
- Base immunitaire `pdac_immune_tcga_fluxes.csv`, SHA-256
  `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e`,
  n = 178, 12 gènes BRUTS log2(RSEM+1) : CD8A, CD8B, CD4, FOXP3, CD68,
  CD163, CD274, PDCD1, CTLA4, GZMB, IFNG, CD19 ; axe joint
  `immune_kras_order_tcga.csv`, SHA-256
  `31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d`.
- Pipeline v6.2 `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (re-vérifié avant le gel).
- Machine : Python 3 + numpy/pandas/scipy présents ; R ABSENT
  (`Rscript` introuvable, 20 nov. 2026) — toute voie exigeant R est
  impraticable sans installation, et aucune installation n'est prévue
  dans ce protocole (si la Voie C l'exigeait, elle serait déclarée
  impraticable, pas contournée). Venv §8.60
  `data_deconvolution_860/venv860` (parseur `rdata` 1.1.0) réutilisable
  pour lire un `.rda` si besoin.

### 2.3 Sources externes candidates (ordre de priorité, gelé)
1. **Aran, Hu, Butte 2017, Genome Biol 18:220, doi
   10.1186/s13059-017-1349-1, PMC5688663** — Additional file 6 :
   « xCell scores of 9947 samples from TCGA and TARGET » (TSV, 6,8 Mo
   annoncés). Article en libre accès (CC-BY 4.0 ; données sous CC0
   selon l'article) — contrairement à Thorsson et al. 2018, la route
   Europe PMC ne devrait pas renvoyer l'erreur « not open access ».
   Accès visés, dans l'ordre : (a) Europe PMC `supplementaryFiles`
   `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5688663/supplementaryFiles`
   (route PROUVÉE au §8.55 pour Aran et al. et au §8.65) ; (b) liens
   des fichiers supplémentaires depuis la page PMC
   `https://pmc.ncbi.nlm.nih.gov/articles/PMC5688663/` (fichiers servis
   par PMC, sans contournement du défi proof-of-work : si PMC bloque,
   la route est notée en échec, non contournée) ; (c) dépôt Zenodo du
   package xCell, doi 10.5281/zenodo.1004662. Dans le même zip, si
   disponible : Additional file 3 (« The 489 cell type gene signatures »,
   xlsx, 417 ko annoncés — nécessaire au comptage de circularité §2.4)
   et Additional file 7 (« The spillover matrix and calibrating
   coefficients », xlsx, 111 ko annoncés — nécessaire à la Voie C).
   Source prioritaire : ce sont les scores xCell PUBLIÉS, par échantillon,
   pour TCGA — la voie symétrique du §8.60 (fractions CIBERSORT publiées).
2. **Package xCell (GitHub `dviraran/xCell`, GPL-3.0 ; Bioconda `r-xcell`)**
   — objet `xCell.data` (signatures + spillover + calibration) embarqué
   dans le package. Voie C (§2.5) : calcul des scores depuis la matrice
   TCGA détenue. Accepté comme source de SIGNATURES (pour la circularité
   et la Voie C) même si la source 1 aboutit ; comme source de SCORES,
   seulement si la source 1 échoue (les scores calculés sont alors
   étiquetés « calculés, pas publiés », jamais présentés comme scores
   publiés).
3. **TIMER2.0 (Li et al. 2020, Nucleic Acids Res, doi 10.1093/nar/gkaa407)**
   — estimations xCell pour TCGA. Accepté seulement si un fichier de
   scores xCell en vrac par cancer est identifiable (URL + hash notés).
   Serveur web interactif seul = insuffisant (déjà constaté au §8.60).
4. **Autres miroirs publics** (dépôts GitHub, Zenodo, Figshare, packages
   R avec données TCGA embarquées, ex. `IOBR`, `immunedeconv` — données
   d'exemple seulement, à vérifier) : acceptés seulement si le fichier
   est identifiable comme les scores publiés d'Aran et al. (mêmes
   colonnes, mêmes valeurs de contrôle, §4), avec URL et hash notés.
5. **Voie C (repli, calcul depuis la matrice détenue — PAS des scores
   publiés).** Si et seulement si 1, 3 et 4 échouent : calcul des scores
   xCell dans ce chantier depuis le tarball TCGA-PAAD RSEM détenu
   (MD5 `b09569ce…ac0a`), avec les signatures publiées (Additional file 3
   ou `xCell.data` du package, source 2) et la matrice de spillover
   (Additional file 7 ou `xCell.data`), par implémentation Python de la
   méthode publiée (ssGSEA par échantillon et par signature, puis
   compensation de spillover, puis calibration — Aran et al. 2017,
   Méthodes). Contraintes gelées : (a) l'implémentation est validée AVANT
   tout usage pour le verdict, en reproduisant les scores publiés sur
   au moins un échantillon de contrôle indépendant (si aucun score publié
   n'est disponible pour valider, la Voie C est déclarée NON VALIDÉE et
   ses scores ne servent pas au verdict) ; (b) variante « leave-12-out »
   OBLIGATOIRE et primaire (signatures moins les 12 gènes de flux) ;
   toute signature qui perdrait tous ses marqueurs après retrait des 12
   est déclarée incalculable par cette voie (à dire, pas contournée) ;
   (c) les scores calculés sont étiquetés « calculés, pas publiés ».

### 2.4 Critères d'acceptation d'un score par type cellulaire
- Fichier téléchargeable gratuitement, sans compte et sans paiement.
- Scores par échantillon TCGA identifiables par barcode (échantillon ou
  patient), avec méthode + version + référence nommées.
- Couverture appariée ≥ 100 tumeurs sur nos 178 (Porte D, §4).
- Valeurs documentées : scores d'enrichissement xCell à échelle
  documentée (Aran et al. 2017 : scores bruts ssGSEA transformés,
  compensation de spillover ; scores nuls mis à zéro sous le seuil
  documenté) — toute valeur hors intervalle documenté est signalée
  et exclue, jamais corrigée silencieusement.
- URL exacte, date/heure UTC, taille en octets, SHA-256 du fichier
  téléchargé notés ; fichier brut jamais modifié.
- **Circularité (gelée).** Les signatures xCell CONTIENNENT certains des
  12 gènes de flux (à compter en machine) : le recouvrement
  signature ∩ 12 flux est compté et rapporté par type (nombre de gènes
  de flux dans la signature du type, sur 12). Pour la source 1 (scores
  publiés), le comptage exige les signatures (Additional file 3 ou
  `xCell.data`, source 2) ; si les signatures sont inaccessibles, la
  sensibilité T2(d) est déclarée NON APPLICABLE avec la raison notée —
  jamais remplacée par une approximation. L'interprétation tient compte
  du recouvrement : un score CD8 corrélant avec CD8A est en partie
  mécanique ; le test décisif reste T2/T5 — l'effondrement de la cohésion
  entre paires NE contenant PAS le gène marqueur — rapporté
  explicitement (§7, T2-sensibilité « paires sans marqueur »).

### 2.5 Voie C — garde-fous (gelés, cf. §2.3 point 5)
- Implémentation Python nouvelle, écrite dans ce chantier, jamais dans
  le pipeline. Validation obligatoire avant usage pour le verdict :
  reproduction des scores publiés (source 1 ou, à défaut, d'un
  échantillon témoin publié dans l'article) à une tolérance notée
  (corrélation de Pearson ≥ 0,99 par type sur les échantillons de
  contrôle, et écart relatif médian < 5 %) — sinon Voie C NON VALIDÉE,
  arrêt du bras principal.
- Si la Voie C est la seule voie et qu'elle est non validée, le verdict
  du chantier est « données xCell inaccessibles / non validées » (§3).

## 3. Porte D (source) — AVANT tout test
- Tenter les sources 1–4 dans l'ordre ; noter pour chaque tentative :
  URL exacte, date/heure UTC, code HTTP / nature de la réponse, taille,
  SHA-256 si fichier obtenu. Les fichiers HTML d'échec sont supprimés ;
  rien de ces tentatives n'entre dans les calculs.
- **Porte D OUVERTE (bras principal)** si et seulement si : fichier
  obtenu + au moins un score par type cellulaire + couverture appariée
  ≥ 100 tumeurs sur 178 (jointure §4).
- **Porte D FERMÉE (bras principal)** : si aucune des sources 1–4 ne
  satisfait ces conditions après les tentatives documentées, ET que la
  Voie C (source 5) est elle-même impossible ou non validée → **arrêt
  du bras principal** : section §8.68 écrite avec le verdict « données
  xCell inaccessibles », journal des tentatives, AUCUNE valeur inventée,
  aucun run principal, aucun test sur des scores fictifs. Il n'y a PAS
  de bras secondaire dans ce chantier (la fraction leucocytaire par
  méthylation a déjà été testée au §8.60, bras L — non re-testée ici).

## 4. Jointure (si porte D ouverte)
- Clé de jointure : barcode échantillon TCGA, sur les **15 premiers
  caractères** (`TCGA-XX-XXXX-01`, protocole §4 du §8.55) ; si une ligne
  externe n'a que 12 caractères, jointure sur les **12 premiers**
  (patient) — la règle appliquée par ligne est consignée, et toute
  collision (2 tumeurs pour 1 clé externe) est signalée et exclue.
- Vérifications : n apparié, n non apparié (listés par barcode),
  0 doublon de clé, valeurs dans l'intervalle documenté.
- Identification comme scores d'Aran et al. — trois vérifications
  gelées : (a) effectif du fichier ≈ 9 947 lignes/colonnes échantillons
  (nombre annoncé pour l'Additional file 6) ; (b) les types présents
  sont les 64 types xCell documentés (familles : lymphoïde, myéloïde,
  progéniteurs, épithéliaux, stroma) — liste vérifiée en machine ;
  (c) validation croisée : le score xCell « CD8+ T-cells » corrèle
  positivement et fortement avec la fraction CIBERSORT T.Cells.CD8 du
  §8.60 (n apparié, r rapporté) et avec le flux CD8A ; le score
  « ImmuneScore » xCell (somme des types immunitaires, si présent dans
  le fichier) corrèle avec l'ImmuneScore ESTIMATE calculé du §8.54
  (r rapporté). Un échec de (c) (r < 0,5 sur CD8) est signalé et
  discuté, pas masqué — il remettrait l'identification en question.
- Les analyses T1–T5 portent sur les tumeurs APPARIÉES uniquement
  (n ≤ 178, noté) ; la base immunitaire reste
  `pdac_immune_tcga_fluxes.csv`, restreinte aux lignes appariées, ordre
  KRAS brut conservé. La cohésion brute de référence est RECALCULÉE sur
  le sous-ensemble apparié, jamais importée du §8.54 (cf. §8.55 :
  0,5563 à n = 178, 0,5040 à n = 149 ; §8.60 : 0,5044 à n = 151).

## 5. Définitions gelées (miroir des §8.51/§8.54/§8.55/§8.60)
- Types cellulaires : chaque colonne de score xCell de la source
  acceptée (64 types attendus ; si le fichier contient en plus les
  scores agrégés ImmuneScore / StromaScore / MicroenvironmentScore,
  ils sont rapportés comme descriptif d'identification (§4c), PAS comme
  des types dans le classement T1 — un agrégat ne concourt pas avec ses
  parties).
- Flux immunitaires : les 12 gènes bruts log2(RSEM+1) : CD8A, CD8B, CD4,
  FOXP3, CD68, CD163, CD274, PDCD1, CTLA4, GZMB, IFNG, CD19.
- Résidus : pour chaque gène immunitaire g, OLS de g sur [1, score(s)]
  (moindres carrés, n apparié) ; résidu = observé − prédit.
- Cohésion H : moyenne des |r de Pearson| sur les 66 paires
  intra-famille. Couplage C : moyenne des |r| entre le contrôle et les
  flux analysés (définition §8.48). Nul du projet : bloc analysé permuté
  conjointement, default_rng(42) FRAIS par fichier, colonne de contrôle
  intacte.
- Références relues (non recalculées) : H brute 0,5563 (n = 178) ;
  IMMROT sans doublon, moyenne +0,7521, minimum +0,4508 (CD68), CD8A
  écart +0,9838 (réel 1,2310, nul 0,2472) ; I-IMM +1,1942 ; I-STR
  +0,9407 ; I-RES +0,1982 ; P-RES +0,9174 ; E-RES +0,6499 ; §8.60 :
  D-TOP1 (B naïfs) +0,5867, D-TOP2 (T CD8) +0,5609, D-RES +0,7692,
  D-LEU +0,7129 ; régression §8.48 : d_ssep = −0,175 + 1,705·C.
- Famille stromale : les types xCell documentés comme stromaux
  (fibroblastes, cellules endothéliales, adipocytes, et apparentés —
  liste exacte lue dans la documentation du fichier obtenu, notée en
  machine). Le meilleur type stromal (TOP-STROM = premier stromal du
  classement T1) est rapporté descriptivement, qu'il qualifie ou non.

## 6. Hypothèses gelées
- H1-xcell (un ou plusieurs types portent la corrélation) : la
  corrélation intra-famille est portée par la quantité d'un ou plusieurs
  types cellulaires xCell (immunitaires ou stromaux). Prédictions :
  (a) chaque flux immunitaire corrèle substantiellement avec au moins
  un type ; (b) après régression sur le(s) type(s) porteur(s), la
  corrélation intra-famille s'effondre ; (c) ordonner les flux
  immunitaires par le score du type porteur les sépare (S_sep au niveau
  IMMROT) ; (d) ordonner les flux RÉSIDUALISÉS par CD8A résidualisé ne
  sépare plus.
- H0-xcell (aucun type ne porte la corrélation) : la corrélation
  persiste après contrôle de chaque type et de leur combinaison, par
  toutes les voies (a)–(d). La corrélation est alors portée par
  l'infiltration globale sans type dominant identifiable, ou par une
  co-expression propre aux tumeurs — comme au §8.60, par une seconde
  méthode indépendante.

## 7. Tests gelés et critères de décision (avant les calculs)

### T1 — Chaque flux immunitaire suit-il un type xCell ?
Pearson r + Spearman ρ (+ p bilatérale, brutes, sans correction pour
tests multiples — le jugement porte sur les moyennes, pas sur une p
isolée ; 64 types × 12 flux = 768 tests, ~38 faux positifs attendus à
p < 0,05 sous le nul) de chaque flux contre chaque type ; R² par flux
et par type (OLS sur [type]) ; moyenne des |r| sur les 12 flux, POUR
CHAQUE TYPE. Critère : type « porteur candidat » si moyenne |r| ≥ 0,30 ;
« faible » si < 0,15 pour tous les types. Les types sont classés par
moyenne |r| décroissante ; TOP1 et TOP2 sont les deux premiers de ce
classement (égalité départagée par la moyenne des |ρ|). TOP-STROM =
premier type stromal du classement. Descriptif : r(type, ImmuneScore
§8.54) et r(type, ABSOLUTE §8.55) — le type re-mesure-t-il
l'infiltration globale ou la pureté ? (Contexte, pas un critère.)

### T2 — La corrélation intra-famille survit-elle à la régression sur le(s) type(s) ?
Matrice 66 paires, sur les n appariées : brute vs résidus. PRIMAIRE :
résidus OLS sur [1, TOP1] (un seul type, le plus porteur). Sensibilités
gelées : (b) résidus sur [1, TOP1, TOP2, TOP3] (les trois types à plus
forte moyenne |r|) ; (c) résidus sur [1, tous les types à moyenne
|r| ≥ 0,30] (maximum 5 — au-delà, sur-ajustement : plafonné aux
5 premiers) ; (d) paires sans marqueur : moyenne |r| résiduelle
recalculée sur les seules paires dont AUCUN des deux gènes n'est dans
la signature du TOP1 (garde-fou de circularité, §2.4 — NON APPLICABLE
si les signatures sont inaccessibles, raison notée). Rapportés :
moyenne |r|, médiane |r|, fraction |r| > 0,5. Critère gelé (même que
§8.54/§8.60) : EFFONDREMENT si moyenne |r| résiduelle < 0,30
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
du TOP1, elle devrait s'effondrer dans chaque moitié (bande de score
étroite) ; persistance dans les deux moitiés = argument contre
H1-xcell, indépendant de toute linéarité. Limite connue (§8.54.6) : une
médiane ne fait pas une bande étroite — l'écart-type résiduel dans
chaque moitié est rapporté, et T4 est dit non concluant si les moitiés
restent larges (> 50 % de l'écart-type global).

### T5 — Runs v6.2 (6 maximum pour le bras principal + 2 conditionnels stromaux, prédictions AVANT lecture des sorties)
CSV construits par `build_xcell_868.py` (nuls graine 42, construction
du projet) :
- D-XTOP1 : contrôle TOP1, analysés = 12 flux immunitaires bruts,
  lignes triées par TOP1 croissant. Réel + nul (2 runs).
- D-XTOP2 : contrôle TOP2, idem. Réel + nul (2 runs).
- D-XRES : contrôle CD8A RÉSIDUALISÉ ([1, TOP1]), analysés = 11 autres
  flux RÉSIDUALISÉS (sans doublon, comme §8.44/§8.51/§8.54/§8.60).
  Réel + nul (2 runs).
- D-XSTROM (CONDITIONNEL, gelé) : contrôle TOP-STROM, analysés = 12 flux
  bruts. Réel + nul (2 runs) — lancé SI ET SEULEMENT SI TOP-STROM n'est
  ni TOP1 ni TOP2 ET sa moyenne |r| ≥ 0,30 (décision prise sur les
  seuls chiffres T1, avant tout run). Sinon, non lancé, raison notée.
Prédictions (calculées à partir de T1/T2 AVANT de lire les sorties) :
d_pred = −0,175 + 1,705·C_mesuré pour D-XTOP1/D-XTOP2/D-XSTROM
(C = moyenne |r| entre le type et les 12 flux) ; pour D-XRES, d_pred
depuis C_résid, et comparaison directe à CD8A IMMROT observé (+0,9838),
à I-RES (+0,1982), à E-RES (+0,6499) et à D-RES du §8.60 (+0,7692).
Critères gelés : D-XTOP1 ou D-XTOP2 SOUTIENT H1-xcell si son écart
S_sep ≥ 0,45 (minimum IMMROT sans doublon) ; D-XRES SOUTIENT H1-xcell
si son écart < 0,30 ; D-XRES SOUTIENT H0-xcell si son écart ≥ 0,45 ;
D-XSTROM SOUTIENT « porteur stromal » si son écart ≥ 0,45.

### Verdict de synthèse (règle gelée, miroir §8.60)
- H1-xcell SOUTENUE si T2 primaire = effondrement ET D-XRES < 0,30
  ET (D-XTOP1 ≥ 0,45 OU D-XTOP2 ≥ 0,45).
- H1-xcell PARTIELLE si T2 = partielle OU (D-XTOP1/D-XTOP2 entre 0,30
  et 0,45) avec D-XRES < 0,70.
- H0-xcell SOUTENUE si T2 = persistance ET D-XTOP1 < 0,30 ET D-XTOP2
  < 0,30 ET D-XRES ≥ 0,45.
- Toute autre combinaison : zone grise, test par test. Aucun consensus
  exigé entre les tests : chaque test est rapporté avec son propre
  critère ; le verdict suit la règle ci-dessus, pas un vote.
- Le bras stromal (D-XSTROM, si lancé) ne change pas le verdict
  principal : il est rapporté séparément comme test de la question
  « stroma ou immunité ? » — un écart ≥ 0,45 avec un T2 stromal en
  effondrement serait une H1-stromale séparée, à dire comme telle.

## 8. Exécution
- SHA v6.2 vérifié avant le lot et noté dans le log.
- Lanceur reprenable `run_v62_lot.sh` (déjà détenu, non modifié) +
  manifeste `manifest_v62_xcell_868.txt` + log
  `runs_v62_xcell_868.log`, unité systemd-run `v62-xcell-868`
  (JAMAIS `nohup`, leçon AGENTS.md). Reprise sans relancer à l'aveugle
  en cas de redémarrage (le lanceur saute les sorties complètes).
- Extracteur `extract_xcell_868.py` (miroir de
  `extract_deconvolution_860.py`) : lecture des `master_results.json`,
  S_sep = max_separation × stabilité, MC, Delta, L7a, t0, w.
- Fichiers de travail sous `~/workspace/runs/pdac-v6/` (jamais /tmp),
  sous-dossier `data_xcell_868/` pour les fichiers bruts téléchargés.
- Section `section_8.68_xcell.md` dans `~/workspace/runs/pdac-v6/` :
  verdict d'abord (une phrase), chiffres ensuite, détail complet après.
  Provenance nommée partout, hashes, ce qui manque, limites honnêtes.

## 9. Périmètre
- 8 nouveaux runs v6.2 au maximum (6 principaux + 2 stromaux
  conditionnels), aucun autre. Aucun nouveau seuil proposé, aucun code
  modifié, aucun push GitHub dans ce chantier (publication sur go
  séparé ; règle permanente « Toujours github et pdf !!! » — par le
  coordinateur).
