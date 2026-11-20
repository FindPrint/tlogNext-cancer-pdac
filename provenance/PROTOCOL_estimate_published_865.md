# PROTOCOLE — Scores ESTIMATE publiés pour TCGA-PAAD (§8.65)

Date de gel : 20 novembre 2026 (avant tout téléchargement de score publié,
avant tout calcul de ce chantier, avant tout nouveau run).
Chantier §8.65 du projet PDAC (chantier 2, confié 20 nov. 2026 ~09h36).
Règle permanente (27 oct. 2026) : provenance toujours nommée — source complète,
nature des lignes, comment chaque valeur a été produite, hachages des données,
et ce qui manque. Publication GitHub/PDF par le coordinateur, pas dans ce chantier.
Ne jamais modifier v6 / v6.1 / v6.2 ; aucune modification du livre blanc ici ;
ne pas toucher à tlogNext-pdac-phase2.

## 1. Question (§8.55.11 et §8.54.10, restée ouverte)

Le §8.54 a recalculé l'ImmuneScore ESTIMATE depuis la matrice détenue
(port Python de tidyestimate, validé à ~10⁻⁸ sur la vignette) : cohésion
0,5563 → 0,2002 (−64,0 %), I-IMM +1,1942, I-STR +0,9407, I-RES +0,1982 —
verdict H1 totale (infiltration explique la corrélation immunitaire).
Le §8.55 n'a pas pu obtenir les scores ESTIMATE PUBLIÉS pour PAAD
(site MD Anderson piloté par JS, fichier JS non récupéré) et a testé
ABSOLUTE à la place (H1 partielle, un tiers porté par la pureté).
Ce chantier cherche les scores ESTIMATE publiés pour TCGA-PAAD et, s'ils
sont obtenus, refait le test du §8.51/§8.55 avec ces scores publiés et les
compare directement (a) à ABSOLUTE (§8.55) et (b) à l'ImmuneScore
recalculé au §8.54. Deux questions distinctes, jugées séparément :
(Q1) les scores publiés confirment-ils le score recalculé du §8.54
(même méthode, mêmes données TCGA RNAseqV2) ? (Q2) le test refait avec
les scores publiés donne-t-il le même verdict que le §8.54 (H1 totale)
ou un verdict différent ?

## 2. Sources candidates (ordre de priorité, gelé)

1. **Yoshihara et al., Nat Commun 2013, 4:2612** — « Inferring tumour
   purity and stromal and immune cell admixture from expression data »,
   doi 10.1038/ncomms3612, PMCID PMC3826632. Supplementary Data 2
   (scores stromal / immunitaire / ESTIMATE publiés par tumeur TCGA,
   RNAseqV2) : fichier `ncomms3612-s3.xlsx` ; Supplementary Data 1
   (les 141+141 gènes) : `ncomms3612-s2.xlsx`.
   Accès visés : (a) Europe PMC `supplementaryFiles` pour PMC3826632
   (voie qui a fonctionné pour Aran et al. 2015 au §8.55) ; (b) PMC
   direct ; (c) Nature static-content ; (d) miroirs publics du même
   fichier — seulement si le fichier est identifiable comme le
   Supplementary Data 2 de Yoshihara (mêmes colonnes, couverture
   pan-cancer incluant PAAD, valeurs à l'échelle ESTIMATE), avec URL
   et hash notés.
2. **Site ESTIMATE, MD Anderson** (`bioinformatics.mdanderson.org/estimate/`) :
   téléchargement des scores par maladie (« Pancreatic ductal
   adenocarcinoma — RNA-seqV2 179 »). Accès visés : (a) récupération du
   fichier JS (`js/disease_histogram.js`, fonction `startDownload`) et
   de l'URL de données qu'il appelle ; (b) toute URL exacte de fichier
   trouvée par recherche web publique — jamais devinée. Pas de navigateur
   vivant dans ce chantier (sous-agent sans navigateur) : si la source
   n'est accessible que par navigateur vivant, elle est consignée comme
   telle, non contournée.
3. **Aran et al., Nat Commun 2015, 6:8971, Suppl. Data 1** — déjà détenu
   (`data/aran2015_supp_data1_ncomms9971-s2.xlsx`, SHA
   `fce1ba13…7529`) : contient une colonne ESTIMATE (pureté estimée par
   ESTIMATE) mais 0 ligne PAAD au §8.55 — re-vérifié en machine dans ce
   chantier, non compté comme source nouvelle ; si PAAD y apparaissait
   (inattendu), il serait utilisé et l'écart avec le §8.55 expliqué.
4. **UCSC Xena / dépôts publics** : copie du tableau de Yoshihara ou des
   scores ESTIMATE par échantillon TCGA, seulement si identifiable comme
   ci-dessus (point 1d).

Critère d'acceptation d'une source : fichier téléchargeable gratuitement,
sans compte et sans paiement, contenant des scores ESTIMATE par échantillon
TCGA identifiables par barcode, avec URL exacte et SHA-256 du fichier
téléchargé notés. Le score recalculé du §8.54 n'est JAMAIS présenté comme
un score publié : il est le comparateur, pas la source.

## 3. Porte S (source) — AVANT tout test

- Télécharger le fichier candidat ; noter URL exacte, date/heure UTC,
  taille en octets, SHA-256.
- Vérifier qu'il contient des colonnes de scores (ImmuneScore /
  StromalScore / ESTIMATEScore et/ou pureté tumorale estimée) et une
  colonne d'identifiant TCGA (barcode échantillon ou patient).
- Compter la couverture PAAD : nombre de lignes PAAD et nombre
  d'appariements avec nos 178 tumeurs (jointure §4).
- **Porte S OUVERTE** si et seulement si : fichier obtenu + au moins une
  colonne de score ESTIMATE publié + couverture appariée ≥ 100 tumeurs
  (sur 178).
- **Porte S FERMÉE** : si aucune source accessible ne satisfait ces
  conditions après les tentatives documentées (au moins les sources 1a,
  1b et 2 tentées, erreurs notées) → **arrêt du chantier** : section
  §8.65 écrite avec le verdict « données inaccessibles », journal des
  tentatives, AUCUNE valeur inventée, aucun run, aucun test sur des
  scores fictifs.

## 4. Jointure (si porte S ouverte)

- Clé de jointure : barcode échantillon TCGA, comme au §8.55 : jointure
  sur les **15 premiers caractères** (`TCGA-XX-XXXX-01`, code échantillon
  tumoral) ; si une ligne externe n'a que 12 caractères, jointure sur
  les **12 premiers** (patient) — la règle appliquée par ligne est
  consignée, et toute collision (2 tumeurs pour 1 clé externe) est
  signalée et exclue.
- Vérifications : n apparié, n non apparié (listés par barcode), 0 doublon
  de clé, plausibilité des scores (ImmuneScore/StromalScore à l'échelle
  ESTIMATE, typiquement [−3000, +5000] ; pureté dans [0, 1] si présente)
  — toute valeur hors intervalle est signalée et exclue, jamais corrigée
  silencieusement.
- Les analyses T1''–T5'' portent sur les tumeurs APPARIÉES uniquement
  (n ≤ 178, noté) ; la base immunitaire reste `pdac_immune_tcga_fluxes.csv`
  (SHA `66dbb672…bd2e`), restreinte aux lignes appariées, ordre KRAS brut
  conservé. Les scores recalculés du §8.54 sont relus en machine dans
  `infiltration_854_scores.csv` (SHA `628732ec…aa7`), jamais recopiés à
  la main.

## 5. Définitions gelées (miroir des §8.54/§8.55)

- Scores publiés : `immune_pub` (ImmuneScore publié), `stromal_pub`
  (StromalScore publié), `estimate_pub` (ESTIMATEScore publié, somme des
  deux si présente), `purity_estimate_pub` (pureté ESTIMATE publiée si
  présente — formule cosinus réservée aux puces Affymetrix par Yoshihara :
  si la colonne existe pour RNAseqV2, elle est rapportée telle quelle,
  jamais recalculée).
- Le score immunitaire ESTIMATE publié n'est PAS utilisé comme contrôle
  des flux immunitaires sans la mise en garde de circularité : il dérive
  d'une signature immunitaire ARN qui contient GZMB, l'un des 12 gènes de
  flux (même raison qu'au §8.54 : variante wo12 du recalculé comme
  garde-fou ; ici la variante publiée sans GZMB n'existe pas — la
  comparaison publié ↔ recalculé wo12, r ≈ 1 au §8.54, sert de garde-fou).
- Résidus : pour chaque gène immunitaire g, OLS de g sur [1, score(s)
  publié(s)] (moindres carrés, n apparié) ; résidu = observé − prédit.
  Variantes : résidus sur [ImmuneScore_pub] seul, sur
  [ImmuneScore_pub, StromalScore_pub] ensemble (sensibilité).
- Cohésion H : moyenne des |r de Pearson| sur les 66 paires intra-famille
  (12 gènes : CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274, PDCD1, CTLA4,
  GZMB, IFNG, CD19). Couplage C : moyenne des |r| entre le contrôle et les
  flux analysés (définition §8.48). Nul du projet : bloc analysé permuté
  conjointement, default_rng(42), colonne de contrôle intacte.
- Références relues en machine (non recalculées) : §8.54 — H brute 0,5563 ;
  H résiduelle [ImmuneScore recalculé] 0,2002 ; I-IMM +1,1942 (réel 1,4063,
  nul 0,2121) ; I-STR +0,9407 ; I-RES +0,1982 ; r(Immune, Stromal)
  recalculés 0,7831. §8.55 — H brute (n = 149) 0,5040 ; H résiduelle
  [ABSOLUTE] 0,3757 ; E-ABS +0,6911 ; E-RES +0,6499 ; CD8A brut +0,9838
  (réel 1,2310, nul 0,2472) ; régression §8.48 d_ssep = −0,175 + 1,705·C.

## 6. Hypothèses gelées

- H1-pub (les scores publiés confirment le §8.54) : le test refait avec
  les scores publiés donne le même verdict que le §8.54 (effondrement de
  la cohésion, séparation par le score publié, effondrement des résidus)
  et les scores publiés corrèlent quasi parfaitement avec les recalculés.
  Prédictions : (a) chaque flux corrèle substantiellement avec
  l'ImmuneScore publié ; (b) après régression sur les scores publiés, la
  corrélation intra-famille s'effondre ; (c) ordonner les flux par
  l'ImmuneScore publié les sépare (S_sep au niveau IMMROT) ; (d) ordonner
  les flux RÉSIDUALISÉS (publiés) par CD8A résidualisé ne sépare plus.
- H0-pub (les scores publiés infirment le §8.54) : la corrélation persiste
  après contrôle des scores publiés, par toutes les voies (a)–(d), ou les
  scores publiés divergent fortement des recalculés (r < 0,90).
- Question annexe (comparaison ABSOLUTE) : la pureté ESTIMATE publiée
  (si présente) est comparée à ABSOLUTE (r, et chute de cohésion
  [ABSOLUTE] 25,5 % contre chute [ESTIMATE-pub]) — descriptif, sans
  verdict propre.

## 7. Tests gelés et critères de décision (avant les calculs)

Critères = ceux des §8.54/§8.55, appliqués aux scores publiés (mêmes
seuils, pas de nouveau seuil inventé après coup).

### T0 — Validation publié ↔ recalculé (avant tout test T1''–T5'')
Pearson r + Spearman ρ entre scores publiés et recalculés (§8.54) :
ImmuneScore, StromalScore, ESTIMATEScore, sur les n appariées.
Critère gelé : CONCORDANCE si r ≥ 0,95 pour l'ImmuneScore (et ≥ 0,90
pour les deux autres) ; DIVERGENCE si r < 0,90 pour l'ImmuneScore.
La pureté ESTIMATE publiée (si présente) est corrélée à ABSOLUTE
(n = 149 appariées §8.55) et à la pureté par méthylation — descriptif.

### T1'' — Chaque flux immunitaire suit-il le score publié ?
Pearson r + Spearman ρ (+ p bilatérale, brutes, sans correction) de chaque
flux contre ImmuneScore_pub, StromalScore_pub, ESTIMATEScore_pub ; R² par
flux (OLS sur [ImmuneScore_pub] et sur [ImmuneScore_pub, StromalScore_pub]).
Critère : lien substantiel si moyenne |r| ≥ 0,30 pour l'ImmuneScore publié ;
lien faible si < 0,15 pour les deux scores publiés.

### T2'' — La corrélation intra-famille survit-elle à la régression publiée ?
Matrice 66 paires : brute (sur les n appariées — la valeur brute de
référence est recalculée sur ce sous-ensemble, pas importée du §8.54)
vs résidus [ImmuneScore_pub] (et sensibilité [ImmuneScore_pub,
StromalScore_pub]). Rapportés : moyenne |r|, médiane |r|,
fraction |r| > 0,5.
Critère gelé : EFFONDREMENT si moyenne |r| résiduelle < 0,30 (chute
≥ 45 % depuis la brute appariée) ET fraction > 0,5 < 0,20 ; PERSISTANCE
si chute < 20 % (moyenne résiduelle > 0,80 × brute appariée) ; entre les
deux : partielle, à dire.

### T3'' — Couplage prédit (sans nouveau run)
C par contrôle immunitaire avant/après résidualisation publiée (12
contrôles) ; d_ssep prédit par la régression §8.48, moyenne prédite brute
vs résidualisée. Descriptif, pas un verdict seul.

### T4'' — Stratification par score publié (non paramétrique)
Médiane de l'ImmuneScore publié : matrice intra-famille dans chaque
moitié (moyenne |r|, fraction > 0,5). Critère : si la cohésion venait de
l'infiltration, elle devrait s'effondrer dans chaque moitié ; persistance
dans les deux moitiés = argument contre H1-pub, indépendant de toute
linéarité. Rappel §8.54.6 : ce test est faible si les moitiés restent
larges — écart-type intra-moitié rapporté, et T4'' n'entre pas dans la
règle de verdict gelée.

### T5'' — Runs v6.2 (6 maximum, prédictions AVANT lecture des sorties)
CSV construits par `build_estimate_published_865.py` (nuls graine 42,
construction du projet) :
- E-PIMM : contrôle ImmuneScore publié, analysés = 12 flux immunitaires
  bruts (n appariées), lignes triées par ImmuneScore_pub croissant.
  Réel + nul.
- E-PSTR : contrôle StromalScore publié, idem. Réel + nul.
- E-PRES : contrôle CD8A RÉSIDUALISÉ ([ImmuneScore_pub]), analysés =
  11 autres flux RÉSIDUALISÉS (sans doublon, comme §8.44/§8.54/§8.55).
  Réel + nul.
Prédictions (calculées à partir de T1''/T2'' AVANT de lire les sorties) :
d_pred = −0,175 + 1,705·C_mesuré pour E-PIMM/E-PSTR ; pour E-PRES, d_pred
depuis C_résid, et comparaison directe à CD8A brut (+0,9838) et à I-RES
(+0,1982, §8.54).
Critères gelés : E-PIMM ou E-PSTR SOUTIENT H1-pub si son écart S_sep
≥ 0,45 (minimum IMMROT sans doublon) ; E-PRES SOUTIENT H1-pub si son
écart < 0,30 ; E-PRES SOUTIENT H0-pub si son écart ≥ 0,45.
Si un seul des deux scores publiés est disponible, les runs du score
absent sont remplacés par un run sur ESTIMATEScore_pub (si présent) +
un run résidualisé sur ce seul score ; le nombre de runs reste ≤ 6 et la
substitution est consignée avant les runs.

### Verdict de synthèse (règle gelée, miroir du §8.54)
- H1-pub TOTALE SOUTENUE si T2'' = effondrement ET E-PRES < 0,30 ET
  (E-PIMM ≥ 0,45 OU E-PSTR ≥ 0,45) ET T0 = concordance.
- H1-pub PARTIELLE si T2'' = partielle OU (E-PIMM/E-PSTR entre 0,30 et
  0,45) avec E-PRES réduit (écart < 0,70, sous les 0,9838 de CD8A brut).
- H0-pub SOUTENUE si T2'' = persistance ET E-PIMM < 0,30 ET E-PSTR < 0,30
  ET E-PRES ≥ 0,45.
- DIVERGENCE (scores publiés ≠ recalculés) si T0 = divergence, quel que
  soit T2'' : le §8.54 est alors remis en question sur sa mesure, et le
  verdict H1/H0 porte sur les scores publiés seuls, dit comme tel.
- Toute autre combinaison : zone grise, à dire comme telle, test par test.
Aucun consensus exigé entre les tests : chaque test est rapporté avec son
propre critère ; le verdict suit la règle ci-dessus, pas un vote.
Comparaison explicite avec le §8.54 (scores recalculés) et le §8.55
(ABSOLUTE) : T1''/T2''/T5'' mis côte à côte avec T1/T2/T5 et T1'/T2'/T5',
mêmes définitions, n apparié noté.

## 8. Nouveaux runs : 6 maximum
Mode fast, graine 42 (défaut pipeline), pipeline v6.2
SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
jamais modifié, vérifié avant et après les runs. Lanceur existant
`run_v62_lot.sh` + manifeste `manifest_v62_estimate_published_865.txt`,
log `runs_v62_estimate_published_865.log`, unité systemd-run
`v62-estpub-865` (+ relance reprenable si mort d'unité). Sorties
`results_fast_v62_estpub865_*`. Extraction par script dédié
`extract_estimate_published_865.py` (mêmes champs que
`extract_purity_855.py` : max_separation, stability, S_sep = produit).

## 9. Vérifications gelées
- SHA-256 du pipeline v6.2, de la base immunitaire, du fichier d'axe :
  revérifiés avant tout calcul ; tout mismatch arrête le chantier.
- SHA-256 + taille + URL du fichier externe téléchargé ; couverture
  appariée comptée en machine, barcodes non appariés listés.
- Aucune valeur S_sep recopiée à la main ; écarts §8.54/§8.55 relus en
  machine dans `infiltration_854_runs.csv` / `purity_855_runs.csv`.
- Aucune conclusion d'une autre expérience n'est importée : seuls les
  chiffres de ce chantier (T0, T1''–T5'' du jour) et les écarts relus des
  §8.44/§8.48/§8.54/§8.55 font le verdict.
- Aucun seuil nouveau, aucune sélection d'indicateur après coup.
- Si la porte S est fermée : aucun calcul T1''–T5'', aucun run, aucune
  valeur de score publié inventée ou approximée.

## 10. Livrables
1. Ce protocole (SHA noté dans le rapport final).
2. Section §8.65 : `~/workspace/runs/pdac-v6/section_8.65_estimate_published.md`.
3. Scripts : `analyze_estimate_published_865.py` (porte S, jointure,
   T0–T4''), `build_estimate_published_865.py` (6 CSV T5''),
   `extract_estimate_published_865.py`.
4. Données : fichier externe brut téléchargé (nommé avec sa source, SHA
   noté — jamais modifié), `estimate_published_865_external.csv`
   (tumeurs appariées : barcode, scores publiés, + colonnes source),
   `estimate_published_865_results.json/.csv` (T0–T4'' + 6 runs),
   `estimate_published_865_csv_sha.json`, manifeste + log du lot.
5. Aucun push GitHub, aucune modification du livre blanc, aucune touche à
   tlogNext-pdac-phase2.

## 11. Ce qui manque (connu d'avance)
- La disponibilité réelle du Supplementary Data 2 de Yoshihara en accès
  libre direct (Europe PMC / PMC / Nature) n'est pas établie avant la
  tentative : c'est l'objet de la porte S. Au §8.54, Europe PMC a renvoyé
  502 et Nature 403 pour ce même fichier ; la voie Europe PMC a
  fonctionné pour Aran au §8.55 — à re-tenter, sans présumer du résultat.
- Le site MD Anderson est piloté par JS et son fichier JS n'a pas pu être
  récupéré au §8.55 (curl 000, 3 tentatives) : à re-tenter une fois, avec
  la recherche web publique comme autre voie vers l'URL exacte du fichier.
- n apparié ≤ 178 : si la couverture publiée est partielle, les
  comparaisons §8.54 se font sur le sous-ensemble apparié, avec la brute
  recalculée sur ce même sous-ensemble (jamais en mélangeant les n).
- La variante publiée sans GZMB n'existe pas : la circularité du score
  immunitaire publié (1 gène de flux sur 141) est traitée par la
  comparaison au recalculé wo12 (r = 0,9999948 au §8.54), pas par une
  re-dérivation.
