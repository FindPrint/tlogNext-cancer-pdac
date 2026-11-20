# PROTOCOLE — Pureté par méthylation pour TCGA-PAAD (§8.61)

Date de gel : 20 novembre 2026 (avant tout calcul de ce chantier, avant
tout nouveau run ; avant tout téléchargement NOUVEAU — voir §2).
Chantier §8.61 du projet PDAC (chantier jumeau du §8.55, nommé au
§8.55.11 : « Pureté par méthylation … candidate pour un chantier
jumeau »).
Règle permanente (27 oct. 2026) : provenance toujours nommée — source
complète, nature des lignes, comment chaque valeur a été produite,
hachages des données, et ce qui manque. Publication GitHub/PDF par le
coordinateur, pas dans ce chantier. Ne jamais modifier v6 / v6.1 / v6.2 ;
aucune modification du livre blanc ici ; ne pas toucher à
tlogNext-pdac-phase2.

## 1. Question (§8.55.11, restée ouverte)

§8.55 a établi, avec la pureté ABSOLUTE (ADN, nombre de copies), que la
corrélation intra-famille immunitaire est portée pour environ un tiers
par la pureté tumorale : 0,5040 → 0,3757 après régression (chute 25,5 %),
écart S_sep E-ABS +0,6911, E-RES +0,6499 (66,1 % du brut) — verdict
H1-ext PARTIELLE. La même Table S1 de Raphael et al. 2017 contient une
TROISIÈME mesure de pureté, par méthylation de l'ADN
(`DNA.hypermethylation.mode.purity`), indépendante de l'ARN elle aussi
mais par une voie différente d'ABSOLUTE (mode d'hyperméthylation, pas
nombre de copies). Question : cette mesure indépendante donne-t-elle le
même chiffre — même part de pureté (~un tiers), même chute, même
séparation — ou un chiffre différent ? Si les deux mesures ADN
s'accordent, la part de pureté est robuste à la méthode ; si elles
divergent, c'est une information, à rapporter telle quelle.

Note d'honnêteté sur l'ordre des opérations : la présence de la colonne
méthylation dans le fichier détenu n'est PAS une découverte de ce
chantier — elle était déjà nommée au §8.55.2/§8.55.11 (150/178
appariées, r = 0,856 avec ABSOLUTE, calculé au §8.55 comme vérification
de cohérence, n = 149). Ce qui est gelé ici, avant tout calcul NOUVEAU,
ce sont : la porte S (§3), la jointure (§4), les définitions (§5), les
tests et critères (§7), le nombre de runs (§8). Aucun chiffre T1''–T5''
n'a été calculé avant ce gel ; le r = 0,856 du §8.55 est cité comme
référence relue, jamais comme résultat de ce chantier.

## 2. Source (gelée)

**Source unique, déjà détenue (aucun nouveau téléchargement requis).**
La pureté par méthylation vient de la MÊME table que l'ABSOLUTE du
§8.55, déjà obtenue et vérifiée :

- Publication primaire : Raphael et al., « Integrated Genomic
  Characterization of Pancreatic Ductal Adenocarcinoma », Cancer Cell
  2017, 32(2):185–203.e13 (PMID 28810144, PMCID PMC5964983,
  DOI 10.1016/j.ccell.2017.07.007), Table S1 — colonne
  `DNA.hypermethylation.mode.purity`.
- Copie curée détenue : pdacR (Torre-Healy et al., Commun Biol 2023,
  6:163, doi 10.1038/s42003-023-04461-6), GitHub `rmoffitt/pdacR`,
  fichier `data/TCGA_PAAD.rds`, URL
  `https://raw.githubusercontent.com/rmoffitt/pdacR/master/data/TCGA_PAAD.rds`,
  SHA-256 `52020679350d1539d7516f7d38f7bf09e510225eba2f228a4fe874f3c496ea76`
  (12 311 529 octets ; copie dans `data/pdacR_TCGA_PAAD.rds`).
- Transcription détenue : `purity_855_sampinfo.csv`, SHA-256
  `7a09dde3d374d1afb64f1d1d053193fc884c04d62e63e519fcf4dbf17378b014`
  (181 lignes × 55 colonnes, extraite au §8.55 par
  `extract_pdacr_sampinfo_855.py`, SHA `70e72a53…5990` — lecture seule
  par le package `rdata`, aucune valeur calculée). La colonne
  `DNA.hypermethylation.mode.purity` y est lue telle quelle, sans
  transformation.

**Tentative de re-vérification (documentée, non bloquante).** Avant les
calculs, une tentative de re-téléchargement du fichier pdacR depuis son
URL est faite UNE fois (curl, timeout) pour vérifier que la source reste
accessible et que le hash reproduit ; si elle échoue (réseau, défi PMC),
le chantier continue sur la copie détenue vérifiée par SHA — la copie
détenue, avec son hash, EST la source vérifiable, et l'échec est
consigné. Le téléchargement direct de la Table S1 de Raphael depuis PMC
reste bloqué par le défi de preuve de travail (constaté au §8.55, non
re-tenté ici sauf si le navigateur du coordinateur le permet — hors de
ce chantier).

**Colonne annexe (descriptive seulement, hors verdict).** La même Table
S1 contient `DNA.methylation.leukocyte.percent.estimate` (fraction
leucocytaire par méthylation) : piste d'infiltration indépendante,
non circulaire (elle ne dérive pas des gènes immunitaires testés).
Elle est rapportée en annexe descriptive (corrélations avec les flux et
avec les deux puretés) — AUCUN run, AUCUN rôle dans le verdict. Son
analyse ne peut ni soutenir ni rejeter H1-meth.

## 3. Porte S (source) — AVANT tout test

- Vérifier les SHA-256 gelés : pdacR RDS, sampInfo transcrit,
  base immunitaire, axe, pipeline v6.2. Tout mismatch arrête le chantier.
- Compter la couverture méthylation : nombre de tumeurs du projet (178)
  appariées avec une valeur `DNA.hypermethylation.mode.purity` non nulle.
- **Porte S OUVERTE** si et seulement si : fichier détenu vérifié par
  SHA + colonne de pureté par méthylation présente + couverture
  appariée ≥ 100 tumeurs (sur 178) + toutes les valeurs dans [0, 1].
- **Porte S FERMÉE** : si la couverture est < 100 ou si un SHA ne
  correspond pas → **arrêt du chantier** : section §8.61 écrite avec le
  verdict « données inaccessibles / incohérentes », journal des
  tentatives, AUCUNE valeur inventée, aucun run, aucun test sur des
  scores fictifs.

## 4. Jointure (si porte S ouverte)

- Clé de jointure : barcode échantillon TCGA, **15 premiers caractères**
  (`TCGA-XX-XXXX-01`, code échantillon tumoral) — même règle que le
  §8.55, protocole §4. 0 collision de clé tolérée des deux côtés.
- Vérifications : n apparié, n non apparié (listés par barcode), aucune
  valeur de pureté méthylation hors [0, 1] — toute valeur hors intervalle
  est signalée et exclue, jamais corrigée silencieusement.
- Les analyses T1''–T5'' portent sur les tumeurs APPARIÉES uniquement
  (n ≤ 178, noté) ; la base immunitaire reste
  `pdac_immune_tcga_fluxes.csv` (SHA `66dbb672…bd2e`), restreinte aux
  lignes appariées, ordre KRAS brut conservé.
- La brute de référence est recalculée sur le sous-ensemble apparié
  méthylation (n = 150 attendu) — jamais importée du §8.51 (n = 178)
  ni du §8.55 (n = 149). Les comparaisons §8.51/§8.55 se font à n
  apparié égal quand c'est possible, sinon avec le n noté à chaque fois.

## 5. Définitions gelées (miroir du §8.55)

- Pureté par méthylation : `purity_meth` =
  `DNA.hypermethylation.mode.purity` (ADN, mode d'hyperméthylation —
  mesure primaire de ce chantier). ABSOLUTE (`purity_absolute`) n'est
  utilisé ici que pour la vérification de cohérence (corrélation
  METH↔ABSOLUTE recalculée en machine, référence §8.55 : r = 0,856,
  n = 149) et pour la sensibilité conjointe (§7, T2''-sens).
- Résidus : pour chaque gène immunitaire g, OLS de g sur [1, METH]
  (moindres carrés, n apparié) ; résidu = observé − prédit.
  Sensibilité : résidus sur [1, ABSOLUTE, METH] ensemble (les deux
  mesures ADN conjointes).
- Cohésion H : moyenne des |r de Pearson| sur les 66 paires
  intra-famille (12 gènes : CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274,
  PDCD1, CTLA4, GZMB, IFNG, CD19). Couplage C : moyenne des |r| entre
  le contrôle et les flux analysés (définition §8.48). Nul du projet :
  bloc analysé permuté conjointement, default_rng(42), colonne de
  contrôle intacte.
- Références relues (non recalculées, sauf la brute appariée) :
  §8.51 : H brute 0,5563 (n = 178) ; H résiduelle interne 0,5480 ;
  CD8A brut écart S_sep +0,9838 (réel 1,2310, nul 0,2472) ;
  §8.55 : H brute 0,5040 (n = 149) ; H résiduelle ABSOLUTE 0,3757
  (chute 25,5 %) ; E-ABS +0,6911 ; E-RES +0,6499 (66,1 % du brut) ;
  régression §8.48 d_ssep = −0,175 + 1,705·C.

## 6. Hypothèses gelées

- H1-meth (la pureté par méthylation explique, comme ABSOLUTE) : la
  corrélation intra-famille est portée par la pureté telle que la
  mesure la méthylation. Prédictions : (a) chaque flux corrèle
  substantiellement avec METH ; (b) après régression sur METH, la
  corrélation intra-famille chute comme après ABSOLUTE (~25 %) ;
  (c) ordonner les flux par METH les sépare (S_sep au niveau IMMROT) ;
  (d) ordonner les flux RÉSIDUALISÉS (METH) par CD8A résidualisé ne
  sépare plus qu'en partie (~deux tiers conservés).
- H0-meth (propriété propre, §8.51 confirmé par une seconde mesure ADN) :
  la corrélation persiste après contrôle de METH, par toutes les voies
  (a)–(d). Un écart METH↔ABSOLUTE (chute ou S_sep nettement différents)
  n'est ni H1 ni H0 : c'est un désaccord entre deux mesures ADN, à
  rapporter tel quel avec ses chiffres.

## 7. Tests gelés et critères de décision (avant les calculs)

Critères = ceux du §8.55, appliqués à la pureté par méthylation (mêmes
seuils, pas de nouveau seuil inventé après coup).

### T1'' — Chaque flux immunitaire suit-il la pureté par méthylation ?
Pearson r + Spearman ρ (+ p bilatérale, brutes, sans correction) de
chaque flux contre METH ; R² par flux (OLS sur [1, METH]). Critère :
lien substantiel si moyenne |r| ≥ 0,30 ; lien faible si < 0,15.
Comparaison directe, flux par flux, avec T1' (ABSOLUTE) du §8.55.

### T2'' — La corrélation intra-famille survit-elle à la régression méthylation ?
Matrice 66 paires : brute (sur les n appariées méthylation) vs résidus
[1, METH] (et sensibilité [1, ABSOLUTE, METH] sur les n = 149 communes
aux deux mesures). Rapportés : moyenne |r|, médiane |r|,
fraction |r| > 0,5. Critère gelé : EFFONDREMENT si moyenne |r|
résiduelle < 0,30 (chute ≥ 45 % depuis la brute appariée) ET
fraction > 0,5 < 0,20 ; PERSISTANCE si chute < 20 % (moyenne
résiduelle > 0,80 × brute appariée) ; entre les deux : partielle, à dire.
Comparaison directe avec T2' (ABSOLUTE : chute 25,5 %).

### T3'' — Couplage prédit (sans nouveau run)
C par contrôle immunitaire avant/après résidualisation METH (12
contrôles) ; d_ssep prédit par la régression §8.48, moyenne prédite
brute vs résidualisée. Descriptif, pas un verdict seul.

### T4'' — Stratification par pureté méthylation (non paramétrique)
Médiane de METH : matrice intra-famille dans chaque moitié (moyenne
|r|, fraction > 0,5). Critère : si la cohésion venait de la pureté,
elle devrait s'effondrer dans chaque moitié ; persistance dans les
deux moitiés = argument contre H1-meth, indépendant de toute linéarité.

### T5'' — Runs v6.2 (4 maximum, prédictions AVANT lecture des sorties)
CSV construits par `build_purity_861.py` (nuls graine 42, construction
du projet) :
- M-METH : contrôle pureté METH, analysés = 12 flux immunitaires
  bruts (n appariées méthylation), lignes triées par METH croissant.
  Réel + nul.
- M-RES : contrôle CD8A RÉSIDUALISÉ ([1, METH]), analysés = 11 autres
  flux RÉSIDUALISÉS (sans doublon, comme §8.44/§8.51/§8.55). Réel + nul.
Prédictions (calculées à partir de T1''/T2'' AVANT de lire les sorties) :
d_pred = −0,175 + 1,705·C_mesuré pour M-METH ; pour M-RES, d_pred
depuis C_résid, et comparaison directe à CD8A brut IMMROT (+0,9838)
et à E-RES (+0,6499).
Critères gelés : M-METH SOUTIENT H1-meth si son écart S_sep ≥ 0,45
(minimum IMMROT sans doublon) ; M-RES SOUTIENT H1-meth si son écart
< 0,30 ; M-RES SOUTIENT H0-meth si son écart ≥ 0,45.
Aucun run sur la fraction leucocytaire (annexe descriptive seulement).

### Verdict de synthèse (règle gelée, miroir du §8.55)
- H1-meth SOUTENUE si T2'' = effondrement ET M-RES < 0,30 ET
  M-METH ≥ 0,45.
- H1-meth PARTIELLE si T2'' = partielle OU (M-METH entre 0,30 et 0,45)
  avec M-RES réduit (écart < 0,70, sous les 0,9838 de CD8A brut).
- H0-meth SOUTENUE (§8.51 confirmé par la méthylation) si T2'' =
  persistance ET M-METH < 0,30 ET M-RES ≥ 0,45.
- Toute autre combinaison : zone grise, à dire comme telle, test par test.
Aucun consensus exigé entre les tests : chaque test est rapporté avec
son propre critère ; le verdict suit la règle ci-dessus, pas un vote.
Comparaison explicite avec le §8.51 (scores internes) et le §8.55
(ABSOLUTE) : T1''/T2''/T5'' mis côte à côte avec T1/T2/T5 et
T1'/T2'/T5', mêmes définitions, n apparié noté. Accord ou désaccord
METH↔ABSOLUTE jugé sur les chiffres, pas sur une impression.

## 8. Nouveaux runs : 4 maximum
Mode fast, graine 42 (défaut pipeline), pipeline v6.2
SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
jamais modifié, vérifié avant et après les runs. Lanceur existant
`run_v62_lot.sh` + manifeste `manifest_v62_purity_861.txt`, log
`runs_v62_purity_861.log`, unité systemd-run `v62-purity-861` (+ relance
reprenable si mort d'unité). Sorties `results_fast_v62_purity861_*`.
Extraction par script dédié `extract_purity_861.py` (mêmes champs que
`extract_purity_855.py` : max_separation, stability, S_sep = produit).

## 9. Vérifications gelées
- SHA-256 du pipeline v6.2, de la base immunitaire, du fichier d'axe,
  du RDS pdacR et du sampInfo transcrit : revérifiés avant tout calcul ;
  tout mismatch arrête le chantier.
- SHA-256 + taille + URL du fichier externe (copie détenue) ; couverture
  appariée comptée en machine, barcodes non appariés listés.
- Aucune valeur S_sep recopiée à la main ; écarts §8.51/§8.55 relus en
  machine dans `purity_851_runs.csv` / `purity_855_runs.json`.
- Aucune conclusion d'une autre expérience n'est importée : seuls les
  chiffres de ce chantier (T1''–T5'' du jour) et les écarts relus des
  §8.44/§8.48/§8.51/§8.55 font le verdict. Le r = 0,856 METH↔ABSOLUTE
  du §8.55 est une référence relue, pas un résultat de ce chantier —
  il est RECALCULÉ en machine ici comme vérification de cohérence.
- Aucun seuil nouveau, aucune sélection d'indicateur après coup.
- Si la porte S est fermée : aucun calcul T1''–T5'', aucun run, aucune
  valeur de pureté par méthylation inventée ou approximée.

## 10. Livrables
1. Ce protocole (SHA noté dans le rapport final).
2. Section §8.61 : `~/workspace/runs/pdac-v6/section_8.61_methylation_purity.md`.
3. Scripts : `analyze_purity_861.py` (porte S, jointure, T1''–T4'',
   cohérence METH↔ABSOLUTE, annexe leucocytes),
   `build_purity_861.py` (4 CSV T5''), `extract_purity_861.py`.
4. Données : `purity_861_external.csv` (tumeurs appariées : barcode,
   pureté méthylation, pureté ABSOLUTE, fraction leucocytaire,
   + colonnes source), `purity_861_results.json/.csv` (T1''–T4''),
   `purity_861_csv_sha.json`, manifeste + log du lot.
5. Aucun push GitHub, aucune modification du livre blanc, aucune touche à
   tlogNext-pdac-phase2.

## 11. Ce qui manque (connu d'avance)
- La relecture directe de la Table S1 de Raphael (défi PMC non
  contourné au §8.55) : la colonne méthylation vient de la transcription
  pdacR, vérifiée par trois cohérences au §8.55 pour ABSOLUTE — pour
  METH, les cohérences disponibles sont : corrélation avec ABSOLUTE
  (r = 0,856 attendu), distribution, et accord avec la classification
  high/low publiée. Une erreur de transcription reste invraisemblable
  mais non exclue par relecture directe.
- METH et ABSOLUTE partagent la même Table S1 : ce ne sont pas deux
  sources indépendantes au sens de la provenance — deux MESURES
  indépendantes (voies ADN différentes), une seule table. À dire.
- n apparié ≤ 178 (150 attendus) : les comparaisons §8.51/§8.55 se font
  sur le sous-ensemble apparié, avec la brute recalculée sur ce même
  sous-ensemble (jamais en mélangeant les n).
- METH est une pureté par le MODE d'hyperméthylation : sa définition
  exacte (Raphael et al. 2017, méthodes) n'est pas relue ici au-delà de
  la colonne ; la fraction leucocytaire reste descriptive.
