# PROTOCOLE — Pureté externe ABSOLUTE / ESTIMATE pour TCGA-PAAD (§8.55)

Date de gel : 19 novembre 2026 (avant tout téléchargement de score externe,
avant tout calcul de ce chantier, avant tout nouveau run).
Chantier §8.55 du projet PDAC (go du coordinateur, 19 nov. 2026 ~22h15).
Règle permanente (27 oct. 2026) : provenance toujours nommée — source complète,
nature des lignes, comment chaque valeur a été produite, hachages des données,
et ce qui manque. Publication GitHub/PDF par le coordinateur, pas dans ce chantier.
Ne jamais modifier v6 / v6.1 / v6.2 ; aucune modification du livre blanc ici ;
ne pas toucher à tlogNext-pdac-phase2.

## 1. Question (§8.51.10, restée ouverte)

§8.51 a établi, avec les proxys de pureté INTERNES du projet (scores acineux /
îlots, médianes d'expression ARN du même tarball), que la corrélation
intra-famille immunitaire n'est pas expliquée par la pureté : 0,5563 → 0,5480
après régression (chute 1,5 %), écart S_sep CD8A résidualisé +0,9174 contre
+0,9838 brut (93,3 % conservés). Les proxys internes partagent la mesure ARN
avec les flux : une pureté EXTERNE, indépendante, pourrait donner un autre
chiffre. Ce chantier teste si le verdict H0 du §8.51 survit à une pureté
externe (ABSOLUTE, fondée sur le nombre de copies ADN, donc indépendante de
l'ARN ; ESTIMATE, fondée sur l'ARN mais par une signature et un algorithme
différents de ceux du projet).

## 2. Sources candidates (ordre de priorité, gelé)

1. **Aran et al., Nat Commun 2015, 6:8971** — « Systematic pan-cancer analysis
   of tumour purity » : tableau supplémentaire avec, par échantillon TCGA,
   les puretés ABSOLUTE, ESTIMATE, LUMP, IHC et le consensus CPE.
   Accès visés : (a) supplément Nature (ncomms9971) ; (b) UCSC Xena
   (hub TCGA PANCAN, jeu « Aran et al. 2015 purity ») ; (c) miroirs
   publics du même tableau (dépôts GitHub, Zenodo) — seulement si le fichier
   est identifiable comme le tableau d'Aran et al. (mêmes colonnes, même
   couverture pan-cancer), avec URL et hash notés.
2. **ESTIMATE (Yoshihara et al., Nat Commun 2013, 4:2612)** : scores stromal /
   immunitaire / ESTIMATE / pureté tumorale estimée publiés (site MD Anderson,
   supplément, ou package R `estimate` sur GitHub — recalcul depuis notre
   tarball RSEM = re-dérivation par un algorithme externe, PAS un score
   publié ; autorisé seulement en repli, étiqueté comme tel, jamais présenté
   comme score publié).
3. **GDC / autres portails TCGA** : pureté ABSOLUTE si exposée par échantillon.

Critère d'acceptation d'une source : fichier téléchargeable gratuitement,
sans compte et sans paiement, contenant des scores de pureté par échantillon
TCGA identifiables par barcode, avec URL exacte et SHA-256 du fichier
téléchargé notés. Un score calculé par nos soins depuis une autre méthode
n'est accepté qu'en repli explicite (cf. point 2), jamais comme « publié ».

## 3. Porte S (source) — AVANT tout test

- Télécharger le fichier candidat ; noter URL exacte, date/heure UTC,
  taille en octets, SHA-256.
- Vérifier qu'il contient une colonne de pureté ABSOLUTE et/ou ESTIMATE et
  une colonne d'identifiant TCGA (barcode échantillon ou patient).
- Compter la couverture PAAD : nombre de lignes dont le barcode commence
  par un code TCGA-PAAD, et nombre d'appariements avec nos 178 tumeurs
  (jointure §4).
- **Porte S OUVERTE** si et seulement si : fichier obtenu + au moins une
  colonne de pureté externe + couverture appariée ≥ 100 tumeurs (sur 178)
  sur au moins une des deux puretés (ABSOLUTE prioritaire).
- **Porte S FERMÉE** : si aucune source accessible ne satisfait ces
  conditions après les tentatives documentées (au moins les sources 1a, 1b
  et 2 tentées, erreurs notées) → **arrêt du chantier** : section §8.55
  écrite avec le verdict « données inaccessibles », journal des tentatives,
  AUCUNE valeur inventée, aucun run, aucun test sur des scores fictifs.

## 4. Jointure (si porte S ouverte)

- Clé de jointure : barcode échantillon TCGA. Nos 178 tumeurs portent le
  barcode complet (28 car., ex. TCGA-HV-A7OP-01A-11R-A33R-07).
  Le tableau d'Aran et al. identifie les échantillons par barcode
  échantillon (16 car., `TCGA-XX-XXXX-01A`) ou patient (12 car.).
  Jointure sur les **15 premiers caractères** (`TCGA-XX-XXXX-01`, code
  échantillon tumoral) ; si une ligne externe n'a que 12 caractères,
  jointure sur les **12 premiers** (patient) — la règle appliquée par ligne
  est consignée, et toute collision (2 tumeurs pour 1 clé externe) est
  signalée et exclue.
- Vérifications : n apparié, n non apparié (listés par barcode), 0 doublon
  de clé, aucune valeur de pureté hors [0, 1] (ABSOLUTE/CPE/ESTIMATE-purity
  sont des fractions) — toute valeur hors intervalle est signalée et exclue,
  jamais corrigée silencieusement.
- Les analyses T1'–T5' portent sur les tumeurs APPARIÉES uniquement
  (n ≤ 178, noté) ; la base immunitaire reste `pdac_immune_tcga_fluxes.csv`
  (SHA `66dbb672…bd2e`), restreinte aux lignes appariées, ordre KRAS brut
  conservé.

## 5. Définitions gelées (miroir du §8.51)

- Puretés externes : `purity_absolute` (ABSOLUTE, ADN, indépendante de
  l'ARN — mesure primaire), `purity_estimate` (ESTIMATE, ARN, signature
  indépendante — mesure secondaire). Le score immunitaire ESTIMATE n'est
  PAS utilisé comme contrôle des flux immunitaires : il est dérivé d'une
  signature immunitaire ARN qui recouvre les gènes testés — ce serait
  circulaire (même raison qu'au §8.51.1 pour l'infiltration).
- Résidus : pour chaque gène immunitaire g, OLS de g sur [1, pureté(s)
  externe(s)] (moindres carrés, n apparié) ; résidu = observé − prédit.
  Deux variantes : résidus sur ABSOLUTE seul, sur ESTIMATE seul, sur
  [ABSOLUTE, ESTIMATE] ensemble (sensibilité).
- Cohésion H : moyenne des |r de Pearson| sur les 66 paires intra-famille
  (12 gènes : CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274, PDCD1, CTLA4,
  GZMB, IFNG, CD19). Couplage C : moyenne des |r| entre le contrôle et les
  flux analysés (définition §8.48). Nul du projet : bloc analysé permuté
  conjointement, default_rng(42), colonne de contrôle intacte.
- Références §8.51 (relues, non recalculées) : H brute 0,5563 ; H résiduelle
  interne 0,5480 ; CD8A brut écart S_sep +0,9838 (réel 1,2310, nul 0,2472) ;
  P-AC +0,0118 ; P-IS +0,2876 ; P-RES +0,9174 ; régression §8.48
  d_ssep = −0,175 + 1,705·C.

## 6. Hypothèses gelées

- H1-ext (pureté externe explique) : la corrélation intra-famille est
  portée par la pureté telle que la mesurent ABSOLUTE/ESTIMATE.
  Prédictions : (a) chaque flux corrèle substantiellement avec au moins
  une pureté externe ; (b) après régression sur les puretés externes,
  la corrélation intra-famille s'effondre ; (c) ordonner les flux par une
  pureté externe les sépare (S_sep au niveau IMMROT) ; (d) ordonner les
  flux RÉSIDUALISÉS (externes) par CD8A résidualisé ne sépare plus.
- H0-ext (propriété propre, §8.51 confirmé) : la corrélation persiste
  après contrôle des puretés externes, par toutes les voies (a)–(d).

## 7. Tests gelés et critères de décision (avant les calculs)

Critères = ceux du §8.51, appliqués aux puretés externes (mêmes seuils,
pas de nouveau seuil inventé après coup).

### T1' — Chaque flux immunitaire suit-il la pureté externe ?
Pearson r + Spearman ρ (+ p bilatérale, brutes, sans correction) de chaque
flux contre ABSOLUTE et contre ESTIMATE-purity ; R² par flux (OLS sur
[ABSOLUTE, ESTIMATE]). Critère : lien substantiel si moyenne |r| ≥ 0,30
pour au moins une des deux puretés ; lien faible si < 0,15 pour les deux.

### T2' — La corrélation intra-famille survit-elle à la régression externe ?
Matrice 66 paires : brute (sur les n appariées — la valeur brute de
référence est recalculée sur ce sous-ensemble, pas importée du §8.51)
vs résidus [ABSOLUTE, ESTIMATE] (et sensibilités ABSOLUTE seul, ESTIMATE
seul). Rapportés : moyenne |r|, médiane |r|, fraction |r| > 0,5.
Critère gelé : EFFONDREMENT si moyenne |r| résiduelle < 0,30 (chute
≥ 45 % depuis la brute appariée) ET fraction > 0,5 < 0,20 ; PERSISTANCE
si chute < 20 % (moyenne résiduelle > 0,80 × brute appariée) ; entre les
deux : partielle, à dire.

### T3' — Couplage prédit (sans nouveau run)
C par contrôle immunitaire avant/après résidualisation externe (12
contrôles) ; d_ssep prédit par la régression §8.48, moyenne prédite brute
vs résidualisée. Descriptif, pas un verdict seul.

### T4' — Stratification par pureté externe (non paramétrique)
Médiane d'ABSOLUTE (et médiane d'ESTIMATE-purity) : matrice intra-famille
dans chaque moitié (moyenne |r|, fraction > 0,5). Critère : si la cohésion
venait de la pureté, elle devrait s'effondrer dans chaque moitié ;
persistance dans les deux moitiés = argument contre H1-ext, indépendant
de toute linéarité.

### T5' — Runs v6.2 (6 maximum, prédictions AVANT lecture des sorties)
CSV construits par `build_purity_855.py` (nuls graine 42, construction
du projet) :
- E-ABS : contrôle pureté ABSOLUTE, analysés = 12 flux immunitaires
  bruts (n appariées), lignes triées par ABSOLUTE croissant. Réel + nul.
- E-EST : contrôle pureté ESTIMATE, idem. Réel + nul.
- E-RES : contrôle CD8A RÉSIDUALISÉ ([ABSOLUTE, ESTIMATE]), analysés =
  11 autres flux RÉSIDUALISÉS (sans doublon, comme §8.44/§8.51). Réel + nul.
Prédictions (calculées à partir de T1'/T2' AVANT de lire les sorties) :
d_pred = −0,175 + 1,705·C_mesuré pour E-ABS/E-EST ; pour E-RES, d_pred
depuis C_résid, et comparaison directe à CD8A brut IMMROT (+0,9838).
Critères gelés : E-ABS ou E-EST SOUTIENT H1-ext si son écart S_sep
≥ 0,45 (minimum IMMROT sans doublon) ; E-RES SOUTIENT H1-ext si son
écart < 0,30 ; E-RES SOUTIENT H0-ext si son écart ≥ 0,45.
Si ABSOLUTE est indisponible mais ESTIMATE disponible (ou l'inverse),
les runs correspondants sont remplacés par les runs de la pureté
disponible + un run résidualisé sur cette seule pureté ; le nombre de
runs reste ≤ 6 et la substitution est consignée avant les runs.

### Verdict de synthèse (règle gelée, miroir du §8.51)
- H1-ext SOUTENUE si T2' = effondrement ET E-RES < 0,30 ET (E-ABS ≥ 0,45
  OU E-EST ≥ 0,45).
- H1-ext PARTIELLE si T2' = partielle OU (E-ABS/E-EST entre 0,30 et 0,45)
  avec E-RES réduit (écart < 0,70, sous les 0,9838 de CD8A brut).
- H0-ext SOUTENUE (§8.51 confirmé par l'externe) si T2' = persistance ET
  E-ABS < 0,30 ET E-EST < 0,30 ET E-RES ≥ 0,45.
- Toute autre combinaison : zone grise, à dire comme telle, test par test.
Aucun consensus exigé entre les tests : chaque test est rapporté avec son
propre critère ; le verdict suit la règle ci-dessus, pas un vote.
Comparaison explicite avec le §8.51 (scores internes) : T1'/T2'/T5' mis
côte à côte avec T1/T2/T5, mêmes définitions, n apparié noté.

## 8. Nouveaux runs : 6 maximum
Mode fast, graine 42 (défaut pipeline), pipeline v6.2
SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
jamais modifié, vérifié avant et après les runs. Lanceur existant
`run_v62_lot.sh` + manifeste `manifest_v62_purity_855.txt`, log
`runs_v62_purity_855.log`, unité systemd-run `v62-purity-855` (+ relance
reprenable si mort d'unité). Sorties `results_fast_v62_purity855_*`.
Extraction par script dédié `extract_purity_855.py` (mêmes champs que
`extract_purity_851.py` : max_separation, stability, S_sep = produit).

## 9. Vérifications gelées
- SHA-256 du pipeline v6.2, de la base immunitaire, du fichier d'axe :
  revérifiés avant tout calcul ; tout mismatch arrête le chantier.
- SHA-256 + taille + URL du fichier externe téléchargé ; couverture
  appariée comptée en machine, barcodes non appariés listés.
- Aucune valeur S_sep recopiée à la main ; écarts §8.51 relus en machine
  dans `purity_851_runs.csv`.
- Aucune conclusion d'une autre expérience n'est importée : seuls les
  chiffres de ce chantier (T1'–T5' du jour) et les écarts relus des
  §8.44/§8.48/§8.51 font le verdict.
- Aucun seuil nouveau, aucune sélection d'indicateur après coup.
- Si la porte S est fermée : aucun calcul T1'–T5', aucun run, aucune
  valeur de pureté externe inventée ou approximée.

## 10. Livrables
1. Ce protocole (SHA noté dans le rapport final).
2. Section §8.55 : `~/workspace/runs/pdac-v6/section_8.55_purity_external.md`.
3. Scripts : `analyze_purity_855.py` (porte S, jointure, T1'–T4'),
   `build_purity_855.py` (6 CSV T5'), `extract_purity_855.py`.
4. Données : fichier externe brut téléchargé (nommé avec sa source, SHA
   noté — jamais modifié), `purity_855_external.csv` (tumeurs appariées :
   barcode, pureté ABSOLUTE, pureté ESTIMATE, + colonnes source),
   `purity_855_results.json/.csv` (T1'–T4' + 6 runs),
   `purity_855_csv_sha.json`, manifeste + log du lot.
5. Aucun push GitHub, aucune modification du livre blanc, aucune touche à
   tlogNext-pdac-phase2.

## 11. Ce qui manque (connu d'avance)
- La disponibilité réelle du tableau d'Aran et al. en accès libre direct
  (supplément Nature / Xena) n'est pas établie avant la tentative : c'est
  l'objet de la porte S.
- Le score immunitaire ESTIMATE et toute déconvolution (CIBERSORT/xCell)
  restent hors de ce chantier (circularité pour le premier, accès avec
  compte pour le second) ; l'infiltration indépendante reste non testée.
- n apparié ≤ 178 : si la couverture externe est partielle, les
  comparaisons §8.51 se font sur le sous-ensemble apparié, avec la brute
  recalculée sur ce même sous-ensemble (jamais en mélangeant les n).
- ABSOLUTE et ESTIMATE mesurent la pureté par des voies différentes
  (ADN vs ARN) : un désaccord entre les deux n'est pas une erreur, c'est
  une information à rapporter telle quelle.
