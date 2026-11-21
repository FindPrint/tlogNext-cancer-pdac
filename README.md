# Cancer du pancréas (PDAC) — pipeline universel v6.2

Dépôt public de travail du projet PDAC : recherche d'un remède pour le
cancer du pancréas avec le pipeline universel de détection de ruptures
(v6.2), données ouvertes, protocoles gelés, résultats vérifiés.

## État au 21 novembre 2026

- Livre blanc : `livre-blanc-pdac-v6.md`, 1348 pages (PDF partagé séparément),
  SHA-256 `9331f107a1d8aac858eb1108ab522deb0c1b038b48abdaf872329ea3d796096d`
  (14747138 octets), sections §8.1–§8.90. Le fichier Markdown ici a pour SHA-256
  `5fbaba28d22608e1a9cdc15bdbc88a7a4651f7aae67ff7c0fe2466079500017a`
  (23274 lignes).
- Pipeline : `universal_v6.2.0_cohen.py`, version de travail, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
  v6.1 = référence, v6 = historique. `universal_v6.3.0_cohen.py`
  (recomposition du score MC) est joint pour vérification : proposition
  REJETÉE (§8.49), v6.2 reste la version de travail.
  `universal_v6.4.0_cohen.py` (recomposition du MC par la
  récurrence-concentration) est joint pour vérification : proposition
  REJETÉE (§8.52), v6.2 reste la version de travail.
- Le verdict §8.90 (audit complet, 21 nov. 2026, lecture seule, 4 volets, aucun run) :
  le podcast a dit juste sur un point précis (`maxsep` 6/8 contre MC 1/8, chiffres exacts
  re-vérifiés ; GSE79668 renverse +0,1447 contre 13 nuls ; MTAP 10/10) mais a exagéré en
  généralisant (6/8 tient à une paire, ICGC charnière ; rotations sans doublon 37/48, pas
  48/48 ; paires récentes contraires : GDC fragile confirmé +0,0314, GSE194249 NON −0,0239) ;
  0 écart numérique sur 9 chiffres clés re-vérifiés, 1 coquille de SHA corrigée par addendum
  daté (PROVENANCE_889 §7) et 7 autres incohérences corrigées (dont le titre §8.51, révisé
  par le §8.54) ; aucun avertissement médical visible (0 occurrence de « conseil médical »
  ou « oncologue »), aucune recommandation clinique directe, faits cliniques tous conformes
  — texte d'avertissement renforcé au §8.90.3.4, sa mise en tête du document est une dette
  de gabarit ; le mot « universel » est exagéré tel quel (l'Ising n'a jamais tourné en
  v6/v6.1/v6.2 ici). Corrections de Zackary (21 nov. 2026) : MC n'est jamais seul — la
  batterie entière fait le verdict ; `maxsep` est le score principal AFFICHÉ, pas le verdict.
- Les 3 verdicts §8.87–§8.89 : (§8.87) consolidation de la quatorzième paire
  GDC avec 10 nuls frais (graines 8871–8880, + 3 anciens = 13 nuls) —
  **FRAGILE CONFIRMÉ** : d_médian +0,0314 (réel 0,2542 contre nul médian
  0,2229), sous le seuil de consolidation 0,09 et sous le plancher 0,07 ;
  réel battu par 1 nul sur 13 (s8880, 0,2689 — rang 13/14), sous le p95 des
  nuls (d contre p95 = −0,0042) ; **2/13 écarts au-dessus du plancher** ;
  **A2 inchangé 10/14** ; 10/10 runs exit 0, vérification 14/14 à 0,0 exact ;
  C3 reste levée. (§8.88) GSE194249 à 11 flux, quinzième paire — **NON** :
  d_maxsep −0,0239 (réel 0,2306 contre nul 0,2545), le nul graine 42 sépare
  plus que le réel ; **A2 devient 10/15** (12/15 positifs), LOO 9/14 ; nuls
  frais +0,0517 / +0,0354 ; 4/4 runs exit 0, vérification 4/4 à 0,0 exact ;
  C3 reste levée ; caveat « 11 flux, DPCR1 absent » écrit. (§8.89) trois
  derniers suppléments Chen (MOESM1, MOESM2, MOESM16) et dépôts consultables
  — **PISTE FERMÉE** : aucune table par-PDO KRAS / MTAP dans les 17
  suppléments ni dans les dépôts consultables (HRA005195 et HRA010277 :
  accès contrôlé, lectures brutes ; ST003734 : lipidomique PANC-1 ;
  Code Ocean 1432248 : code seulement) ; **drogue × KRAS et drogue × MTAP
  IMPOSSIBLES** ; la question des hits du §8.84 reste sans réponse, pas
  tranchée négativement ; seule variable par-organoïde nouvelle, le statut
  CFTR MT/WT de la Fig. 14c (MOESM1), non recevable (38/46 couverts,
  MT n = 4, en conflit avec la Fig. 6e).
- Les 3 verdicts §8.84–§8.86 : (§8.84) lot drogue Chen 2025 (46 PDO × 63 AUC,
  ordonnés par sensibilité à la gemcitabine) — **CONFIRME (exploratoire, consolidée)** :
  d_maxsep +0,0982 (réel 0,3478 contre nul 0,2496), 3/3 nuls au-dessus du plancher
  (+0,1528 / +0,1607) ; **2 hits FDR < 0,05** (paclitaxel rho +0,5085, FDR 0,0191 ;
  mitomycine C rho +0,4759, FDR 0,0257) ; **Olaparib/BRCA2 répliqué** (p = 0,00015) ;
  **5/5 correcteurs CFTR répliqués** ; **drogue × KRAS et drogue × MTAP IMPOSSIBLES**
  (aucune table par-PDO) ; **hors compte A2** (n = 46 < 50). (§8.85) quatorzième paire
  GDC ORGANOID-PANCREATIC, remappage DPCR1 → MUCL3 vérifié 5/5 portes (HGNC MUCL3
  HGNC:21666, prev_symbol DPCR1, 2018-03-19) — **CONFIRME, FRAGILE ET NON CONSOLIDÉ** :
  d_maxsep +0,0884 (réel 0,2542 contre nul 0,1658), marge 0,0184 ; nul frais s8851
  +0,0376 sous le plancher ; **A2 10/14** (12/14 positifs), LOO 9/13 ; C3 reste levée.
  (§8.86) GSE194249, ré-audit — **INUTILISABLE** comme 14e paire : DPCR1 absent de la
  matrice FPKM déposée (0 occurrence, 0/15 609 lignes), la porte gelée dit ARRÊT ;
  **0 run** ; **A2 reste 10/14** ; piste fermée comme paire à 12 flux.
- Les 6 verdicts §8.78–§8.83 : (§8.78) inventaire des dépôts GitHub Ising / cancer
  (piste A, lecture seule) — **4 dépôts utiles** (universal-log-research le plus riche :
  benchmarks Ising, calibration des 29 estimateurs, analyses PDAC 16–20 nov. ;
  pdac-systems-evidence-preclinical, T_log-, apamea-artificial-spin-ice-multiflux) et
  **6 candidates pour la piste B, dont 2 fortes** (C1 Chen et al. 2025, 46 PDO × 63 AUC,
  MOESM13 SHA `0e009cd5…` ; C2 GDC ORGANOID-PANCREATIC, 55 RNA-seq) ; tlogNext-pdac-phase2
  nommé seulement, contenu non lu ; 0 run, 0 téléchargement — rien ici n'est un verdict
  importé. (§8.79) treizième paire principale GSE57495 — **CONFIRME** : d_maxsep +0,4494
  (réel 0,6381 contre nul 0,1887), plus grand écart maxsep jamais mesuré sur une paire GEO ;
  A2 9/13 (11/13 positifs), LOO 8/12 ; **C3 RESTE LEVÉE** ; candidate C2 ARRÊTÉE (DPCR1
  absent de 55/55 fichiers GDC, devenu MUCL3) ; **caveat** : GSE57495 est la cohorte #2,
  déjà tenue comme holdout direct — jamais une confirmation indépendante de KRAS–CEACAM5 ;
  C1 (lot drogue) piste suivante. (§8.80) veille vopimetostat + daraxonrasib — **aucune
  nouvelle donnée sur la combinaison depuis ESMO 2026**, phase 3 sans NCT (design précisé,
  démarrage 1er semestre 2027) ; **approbation européenne de daraxonrasib seul le 16 nov.
  2026** ; 1re ligne daraxonrasib + GnP plus mature (ENA 2026, PFS médiane 12,8 mois) ;
  rationnel MTAP/PRMT5 mesuré ici intact. (§8.81) piste Œil — **MIXTE** : la tumeur ne
  copie pas le privilège oculaire comme un programme cohérent (3/7 gènes montent avec KRAS :
  CD47, TGFB1, CD274 ; score PRIV rho médian +0,122, sous le seuil +0,15 ; bras pipeline
  TCGA ordre PRIV d_maxsep +0,1649 mais chaîne absente ; UVM n = 80 : gènes de privilège
  MOINS exprimés, d −0,35 à −3,00, image miroir) ; piste CLOSE comme question de copie.
  (§8.82) cerveau GBM — les gènes de privilège **DESCENDENT** avec la prolifération
  (médiane rho −0,287, 0/7 positifs, 7/7 p < 0,05 ; score PRIV −0,477) ; GBM **FROID**
  mais pas par les mêmes gènes (CD4, FOXP3) ; pipeline **PARTIEL fragile** (+0,0283, sous
  le plancher) ; chaîne PDAC absente ; A2 inchangé. (§8.83) survie — **3 items sur 8
  PRÉDISENT COMME CA125** (TGFB2, HLA-G, score combiné), **mais aucun ne monte avec KRAS
  dans ≥ 2/3 cohortes** — le signal de survie ne passe pas par KRAS ; CD47 MIXTE ;
  hors pipeline.
- Les 2 verdicts §8.76–§8.77 : (§8.76) lot Yeh_seq FNA de GSE131050
  (n = 42, 41/42 mêmes tumeurs que le lot FF du §8.74) — **CONFIRME** :
  le signal `maxsep` survit au changement de type d'échantillon et il
  est même plus fort en FNA : d_maxsep +0,1642 (réel 0,4083 contre nul
  0,2441), marge de 0,0942 au-dessus du plancher 0,07, plus de deux fois
  l'écart FF (+0,0739) ; A2 INCHANGÉ 8/12 (10/12 positifs), LOO 7/11 —
  le lot FNA n'est pas une treizième paire indépendante ; extraction
  2/2 à 0,0 exact ; **C3 RESTE LEVÉE** (consolidation supplémentaire,
  ne rouvre rien). (§8.77) réparation de la reproductibilité —
  **REPRODUCTIBILITÉ RÉPARÉE** : 19/19 gaps fermés (URL retrouvée +
  fichier re-téléchargé + SHA vérifié, dont le SOFT GPL20769, le
  fichier clinique du test C et les 4 fichiers CPTAC) ; script de
  re-téléchargement corrigé (`download_data.sh`, SHA `55811136…`,
  12 corrections, `bash -n` OK), exécuté en entier jusqu'à EXIT:0
  (52 fichiers, 2,4 Go, tous vérifiés) ; test à froid TCGA v4 :
  flux reconstruits SHA-IDENTIQUES et runs v6.2 identiques aux
  chiffres tenus à 0,0 exact des deux côtés ; DATA_SOURCES.md révisé
  (900 lignes, SHA `17b8428b…`, nouvelles §28 sources §8.76 et §29
  chantier §8.77, §17 révisé 19/19 fermés) ; deux fautes de frappe de
  SHA latentes corrigées (Birnbaum MOESM3 §13, LUAD §2.3) ; **0
  section modifiée, 0 verdict rouvert** — le test C reste NON (§8.45).
- Les 2 verdicts §8.74–§8.75 : (§8.74) douzième paire principale
  GSE131050 lot Yeh_seq FF (n = 42, Rashid et coll. 2020, PMID 31754050,
  GPL18573, UNC) — **CONFIRME**, de justesse : d_maxsep +0,0739 (réel
  0,3220 contre nul 0,2481), marge de 0,0039 au-dessus du plancher 0,07,
  la plus petite marge passante du dossier ; A2 étendu 8/12 (10/12
  positifs), LOO 7/11 ; passage consolidé par deux nuls frais (3/3 écarts
  au-dessus du plancher, +0,0976 et +0,1113) ; extraction 4/4 à 0,0
  exact ; **C3 RESTE LEVÉE** (confirmation supplémentaire, ne rouvre
  rien) ; piste suivante nommée : lot Yeh_seq FNA (n = 42 codes), non
  vérifiée. (§8.75) clôture du résidu M2 du §8.63 — **TRANCHÉ–CONFIRMÉ** :
  la réplication hors échantillon tient (24/30 nuls ICGC frais, 80,0 %,
  et 9/10 nuls GSE62452 frais choisissent la config réelle) ; le taux
  stabilisé est **80 %**, pas 85 % (poolé ICGC 64/80, GSE 26/30) ; M2
  passe de PARTIELLEMENT EXPLIQUÉ à **EXPLIQUÉ** ; 40/40 runs exit 0 ;
  le déclencheur du pic étroit reste NON ÉLUCIDÉ (§8.73).
- Les 3 verdicts §8.71–§8.73 : (§8.71) confirmation indépendante maxsep (C3) —
  CONFIRME : la paire GSE60979 (n = 49, Sandhu et coll. 2015, PMID 25579086,
  GPL14550, Oslo) donne d_maxsep +0,2045 (réel 0,4418 contre nul 0,2373),
  nettement au-dessus du plancher 0,07 ; A2 étendu 7/11 (9/11 positifs), LOO
  6/10 — **C3 LEVÉE** (7 paires passantes au total, LOO pire cas 6/10) ;
  extraction 2/2 à 0,0 exact ; aucun nul frais (règle gelée §7) ; la
  confirmation indépendante est désormais close sur ce critère.
  (§8.72) consolidation de §8.70 — **RENVERSE** : contre 13 nuls (10 frais,
  graines 8721–8730, + 3 anciens), GSE79668 passe — d_médian +0,1447 (réel
  0,4104 contre nul médian 0,2657), rang 14/14, 12/13 écarts au-dessus du
  plancher ; le nul graine 42 (0,3538), qui faisait le verdict PARTIEL, est
  le PLUS HAUT des 13 nuls ; extraction 14/14 à 0,0 exact ; C3 au sens gelé
  (paires graine 42) n'est pas levée par ce chantier seul (A2 gelé 6/10) —
  §8.71 la lève par la onzième paire ; addendum daté ajouté au §8.70, texte
  original intact. (§8.73) déclencheur du pic étroit — **NON ÉLUCIDÉ** :
  aucun déclencheur identifiable (bloc extrême 1/11, transplantation 0/3 et
  0/6, ligne unique 4/11, queues globales AUC 0,31–0,47) ; l'étroitesse est
  une propriété fragile de l'arrangement exact des lignes ; la winsorisation
  qui semblait tuer le pic est un artefact de déflation de variance (le
  maxsep monte) ; calibration 22/22 à 0,00e+00, lot frais 20/20 exit 0.
- Le verdict §8.70 : confirmation indépendante maxsep (C3) —
  PARTIEL : la paire GSE79668 (n = 51, Kirby et coll. 2016, PMID 27282075,
  GPL11154) donne d_maxsep +0,0567 (réel 0,4104 contre nul 0,3538), positif
  mais sous le plancher 0,07 ; A2 étendu 6/10 (8/10 positifs), LOO 5/9 —
  C3 NON levée (elle exige 7 paires passantes au total, soit 7/10 avec la
  dixième paire, LOO pire cas 6/9) ; 2 nuls frais passent le plancher
  (+0,0890 et +0,1538), verdict fragile, non consolidé ; MC inversé
  (−0,0053), Delta plat (+0,0467), L7a UP des deux côtés, falsification
  indisponible (n = 51 < 75) ; extraction 4/4 à 0,0 exact. La table de la
  matrice est vide (0 ligne de données) : les valeurs viennent du fichier
  supplémentaire de la série (comptages bruts GENCODE v.9). Le test de
  Cohen marginal est vacueux par construction (d = 0,0000, 12 gènes) ;
  le test de Spearman contre le pas porte l'information (Δρ médian
  +0,186, 9/12 positifs). L'adoption pleine de maxsep, décidée par
  Zackary le 20 nov. 2026 à 13h04, reste sa décision — la confirmation
  reste ouverte. Addendum 20 nov. 2026 (§8.72) : lecture RENVERSE — contre 13 nuls, GSE79668 passe (d_médian +0,1447, rang 14/14) ; le verdict de la paire graine 42 reste PARTIEL (+0,0567), l'A2 gelé reste 6/10.
- Les 3 verdicts §8.67–§8.69 : (§8.67) fraction leucocytaire —
  PARTIEL : elle retire un tiers de la cohésion (0,5035 → 0,3372,
  −33,0 %) et ordonne les flux bruts (+0,7129), mais une fois les flux
  résidualisés elle ne les ordonne plus du tout (−0,0099) et la
  séparation survit (+0,5662, 57,6 % du brut CD8A conservés) ; la
  quantité de leucocytes ne porte pas la séparation. (§8.68) xCell
  64 types — H1-xcell PARTIELLE SOUTENUE : les cellules dendritiques
  activées (aDC) retirent à elles seules 41,2 % de la cohésion
  (0,5563 → 0,3270) ; les DC ordonnent les flux à +1,1804 ; mais les
  flux résidualisés séparent encore +0,6040 (61,4 % du brut) — aucun
  type ne porte tout. (§8.69) confirmation indépendante maxsep (C3) —
  NON : la paire GSE21501 ne sépare pas (d_maxsep −0,0100), A2 étendu
  6/9, C3 non levée ; l'adoption pleine de maxsep, décidée par Zackary
  le 20 nov. 2026 à 13h04 (note §8.64.12), reste sa décision — la
  confirmation reste ouverte (piste GSE79668) ; correction : la
  plateforme GSE57495 est GPL15048, pas GPL6244 comme l'affirmait le
  §8.66 §1.2.
- Les 3 verdicts §8.64–§8.66 : (§8.64) adoption de maxsep —
  ADOPTER SOUS CONDITION CONFIRMÉ par une troisième lecture indépendante
  (0 écart contre le §8.59 : 37/48, 6/8, HP35 +1,6512, 120/120 à 0,0
  exact) ; maxsep devient le score principal affiché, MC reste
  secondaire, aucune v6.5 créée, v6.2 reste la version de travail.
  (§8.65) scores ESTIMATE publiés — H1-pub TOTALE SOUTENUE : la table
  publiée MD Anderson confirme le §8.54 à la décimale près (scores
  publiés ↔ recalculés r = 0,9999998, cohésion 0,5563 → 0,2001,
  −64,0 %, jointure 178/178) ; la question ouverte du §8.54 est fermée.
  (§8.66) bloc estomac/mucus, quatrième cohorte GSE62165 (118 tumeurs)
  — le cœur du §8.58 est confirmé et deux bords cassent : G5/KRAS
  CONFIRME 4/4 (KRT19 +0,577, p = 7,7e-12) et G1/KRAS CONFIRME, mais
  G1/stade NON CONFIRMÉ (sens inverse de TCGA) et G3 NON CONFIRMÉ
  (OR2B6 MONTE +0,293, premier OR montant en confirmation) ; le
  pipeline ne sépare pas du nul (MC 4/10, S_sep 5/10).
- Les 5 verdicts §8.59–§8.63 : (§8.59) maxsep seul — ADOPTER SOUS
  CONDITION (provisoire, pas pleine) : re-confirmé 37/48, 6/8, HP35
  +1,6512 ; le verdict tient à une paire (retirer l'une des 6 paires
  passantes → 5/7) et à la convention du plancher 0,07 (au plancher
  équivalent-sep, 5/8) ; 30 changements de classe ancien → maxsep, tous
  en gain, 0 en perte ; aucune v6.5 créée, v6.2 reste la version de
  travail. (§8.60) déconvolution — ZONE GRISE : aucun type cellulaire
  seul ne porte la corrélation immunitaire (retirer le meilleur type ne
  retire que 4,7 % de la cohésion) ; c'est la quantité totale
  d'infiltrat qui la porte ; la fraction leucocytaire par méthylation
  en explique un tiers (PARTIELLE, −33,0 %). (§8.61) pureté par
  méthylation — ZONE GRISE : elle ordonne les flux presque comme
  ABSOLUTE (+0,6739, 97,5 % d'E-ABS) mais ne retire que 15,9 % de la
  corrélation en linéaire, contre 25,5 % pour ABSOLUTE. (§8.62) loi
  d'échelle en n pour Delta — NON TROUVÉE (LOCO R² = −0,005) et elle NE
  SUFFIT PAS (réel/nul |Δ| ≤ 0,10 sur 53/106 paires) ; une loi est en
  revanche TROUVÉE pour quatre estimateurs (Katz, Petrosian, Sevcik,
  GraphDimension), qui ne portent pas Delta. (§8.63) mécanismes §8.50 /
  §8.53 — M1 EXPLIQUÉ (MC haut = permutation, Delta bas = w = 27, qui
  porte 96,8 % de l'effet) ; M2 PARTIELLEMENT EXPLIQUÉ (l'optimiseur
  maximise le MC sur 12 configs fixes, réplication hors échantillon
  indécise 6/10) ; Delta doit se comparer à w égal. Clos au §8.75 : réplication confirmée (24/30 nuls ICGC frais et 9/10 nuls GSE62452 frais), taux stabilisé 80 %, M2 EXPLIQUÉ.
- Les 5 verdicts §8.54–§8.58 : (§8.54) infiltration — H1 SOUTENUE : la
  corrélation immunitaire est largement un effet de composition — après
  déconvolution ESTIMATE, la cohésion intra-famille tombe de 0,5563 à
  0,2002 (−64,0 %) ; ordonner par ImmuneScore sépare de +1,1942 ; le
  verdict « propriété propre aux tumeurs » du §8.51 est révisé.
  (§8.55) pureté externe — H1-ext PARTIELLE : ABSOLUTE (pdacR, 149/178)
  explique une partie de la corrélation immunitaire (0,5040 → 0,3757,
  −25,5 %) ; 66,1 % de la séparation conservés après régression ; le
  verdict « H0 soutenue » du §8.51 est qualifié, pas renversé.
  (§8.56) maxsep seul SUFFIT (rotations 37/48, paires principales 6/8,
  HP35 +1,6512) ; sep seul est REJETÉ (35/48, 5/8) — décision d'adoption
  à prendre, v6.2 reste la version de travail. (§8.57) Delta reste NON
  ÉLUCIDÉ depuis les séries complètes (meilleur modèle 89,2 % paires /
  90,5 % valeurs en LOCO). (§8.58) flux inattendus du bloc estomac/mucus
  confirmés sur 3 cohortes : le programme neuroendocrine s'efface avec
  KRAS (SYP −0,503), le métabolisme volatil confirme plus fort qu'en TCGA
  (AOX1 −0,611), les récepteurs d'odeurs chutent, aucun ne monte.
- Les 4 verdicts §8.50–§8.53 : (§8.50) arbitrage MTAP TIENT — sur 10 nuls
  frais (graines 1011 à 11111), l'écart S_sep réel − nul vaut au minimum
  +0,1110 (médiane +0,1595, maximum +0,1981), 10/10 au-dessus du plancher
  0,07, 13/13 avec les 3 nuls anciens ; la marge fragile du §8.46 était la
  queue basse de la distribution nulle. (§8.51) la pureté n'explique PAS
  la corrélation immunitaire — après régression de chaque gène immunitaire
  sur les deux scores de pureté, la corrélation intra-famille demeure
  (0,5563 → 0,5480, chute de 1,5 %) ; ordonner les flux immunitaires
  résidualisés par CD8A résidualisé sépare presque autant que le brut
  (+0,9174 contre +0,9838, 93,3 % conservés), comme prédit par la
  régression §8.48 (+0,9185, à 0,0011 près). (§8.52) recomposition du MC (v6.4) REJETÉE — MC2 suit
  maxsep sans ressusciter Test A ni renverser les verdicts NON (§8.34,
  §8.43), sous les critères gelés. (§8.53) plancher honnête des S_sep
  nuls à n≈70 : 0,38 en ICGC, 0,36 en GSE62452 (p95, réplique 1000
  tirages) — le réel ICGC (0,2289) est sous ce plancher, le réel GSE62452
  (0,4656) est au-dessus ; ≈200 nuls au total, la médiane converge dès
  ~50–100, le p95 exige davantage.

## Structure

- `livre-blanc-pdac-v6.md` — livre blanc complet (§8.1–§8.90).
- `universal_v6.2.0_cohen.py` — pipeline v6.2 (Cohen-d partout).
- `universal_v6.3.0_cohen.py` — proposition v6.3 REJETÉE (§8.49).
- `universal_v6.4.0_cohen.py` — proposition v6.4 REJETÉE (§8.52).
- `README.md`, `DATA_SOURCES.md`, `MANIFEST_SHA256.txt` — ce fichier,
  les sources des données, les SHA-256 de chaque fichier du dépôt.
- `download_data.sh` — script de re-téléchargement des matrices brutes,
  version corrigée §8.77 (SHA `55811136…`, 52 fichiers, EXIT:0, test à froid
  à 0,0 exact ; original `~/workspace/staging-pdac/download_data.sh`,
  SHA `4e151d59…`).
- `provenance/` — 120 fichiers : protocoles gelés (`PROTOCOL_*.md`) et
  provenances (`PROVENANCE_*.md`) de chaque lot, plus
  `PUBLICATION_tlogNext.md`.
- `results/` — 166 tables vérifiées v6.1/v6.2/v6.3/v6.4 (validation, phase 2,
  Delta, MC recomposé, infiltration, pureté externe, sep/maxsep, Delta séries, estomac/mucus, adoption maxsep, déconvolution, pureté méthylation, loi d'échelle Delta, mécanismes, décision maxsep, ESTIMATE publiés, quatrième cohorte GSE62165, fraction leucocytaire, xCell, confirmation indépendante GSE21501, confirmation indépendante GSE79668, confirmation indépendante GSE60979, consolidation GSE79668, déclencheur du pic étroit, douzième paire GSE131050, clôture du résidu M2, lot FNA GSE131050, réparation de la reproductibilité, treizième paire GSE57495, piste Œil (UVM), cerveau GBM, survie privilège, lot drogue Chen 2025, quatorzième paire GDC MUCL3, ré-audit GSE194249, consolidation GDC 10 nuls frais, GSE194249 à 11 flux, suppléments Chen MOESM1/2/16).
- `sections/` — sections §8.38–§8.90 du livre blanc, fichiers sources.
- `scripts/` — 236 scripts de construction des flux, d'extraction et
  d'analyse.
- `data_flux/` — 820 CSV/JSON : flux d'entrée des runs, tests directs,
  extraits ssep / v62_delta / §8.46–§8.89.

## Données brutes

Les matrices brutes (~2 Go) ne sont pas dans ce dépôt (limite snapshot
GitHub : 2 000 fichiers, 16 Mio). Voir `DATA_SOURCES.md` : chaque source
(URL, accès, hachage) et le script pour les re-télécharger et reconstruire
les flux de `data_flux/`.

## PDF

Le PDF du livre blanc (1348 pages, binaire) est partagé séparément : les
snapshots GitHub n'acceptent que des fichiers UTF-8 de moins de 16 Mio
au total. Son SHA-256 est rappelé ci-dessus.

## Suite

La suite du travail (phase 2) se poursuit dans le dépôt
`tlogNext-pdac-phase2`, travail d'un autre agent — ce dépôt-ci reste
l'état vérifié du travail v6.2 au 21 novembre 2026.

Projet : FindPrint / TagPrint. Données ouvertes, code reproductible,
résultats négatifs rapportés comme les positifs.
