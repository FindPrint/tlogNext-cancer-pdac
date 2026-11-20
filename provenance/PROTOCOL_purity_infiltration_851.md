# PROTOCOLE — Test pureté / infiltration pour la corrélation immunitaire (§8.51)

Date de gel : 19 novembre 2026 (avant tout calcul de ce chantier, avant tout nouveau run).
Chantier 2/4 des étapes v6.2 approuvées par Zackary le 19 nov. 2026 ~08h16.
Règle permanente (27 oct. 2026) : provenance toujours nommée — source complète,
nature des lignes, comment chaque valeur a été produite, hachages des données,
et ce qui manque. Publication GitHub/PDF par le coordinateur, pas dans ce chantier.

## 1. Question (§8.48.8, restée ouverte)

§8.48 a établi que la domination IMMROT est un effet de couplage contrôle↔flux :
r = 0,954, R² = 0,909 (n = 48) ; IMMROT |r| moyen intra-famille 0,556 contre
0,25 / 0,27 / 0,17 pour les autres familles. Le nul conserve exactement la
cohésion (H identique à 10⁻¹⁶ près) en brisant le couplage. Reste ouverte la
cause de la corrélation intra-famille immunitaire elle-même : vient-elle de la
pureté tumorale et de l'infiltration immunitaire (composition cellulaire), ou
d'une biologie propre aux tumeurs ? Ce chantier teste la première branche.

## 2. Données existantes réellement (inventaire fait avant le gel)

### 2.1 Détenues (sur disque, hachages vérifiés dans ce chantier)
- Tarball TCGA-PAAD RSEM, Broad GDAC Firehose 2016-01-28 :
  `data/tcga_paad_rsem.tar.gz`, MD5 `b09569ce3f4721f514bc137bd109ac0a`.
- Base immunitaire TCGA : `pdac_immune_tcga_fluxes.csv`, n = 178, SHA-256
  `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e`
  (PROVENANCE_immune_v6.md). 12 gènes BRUTS (log2(RSEM+1), AUCUNE correction
  de pureté — choix documenté du bras immunitaire) : CD8A, CD8B, CD4, FOXP3,
  CD68, CD163, CD274, PDCD1, CTLA4, GZMB, IFNG, CD19. Lignes ordonnées par
  KRAS brut croissant.
- Fichier d'axe joint : `immune_kras_order_tcga.csv`, SHA
  `31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d`
  (step, barcode échantillon, KRAS brut) — clé de jointure par barcode.
- Proxys de pureté du projet (définitions v3/v4, PROVENANCE_tcga_v3.md) :
  score acineux = médiane log2(RSEM+1) des 11 gènes PNLIP, CTRB2, CELA3A,
  CTRB1, CPA1, CELA2A, CPB1, CELA3B, CLPS, CTRC, CPA2 ; score îlots =
  médiane log2(RSEM+1) de INS, GCG, PPY, SST. NON sauvegardés comme fichier
  autonome : ils sont RECALCULÉS dans ce chantier depuis le tarball
  (mêmes listes de gènes que `build_fluxes_tcga_v3.py`), puis joints aux
  lignes immunitaires PAR BARCODE (jamais par index — les ordres v4 et
  immunitaire diffèrent : résidu KRAS vs KRAS brut).
  Sanité : le score acineux recalculé doit égaler la colonne `score_acineux`
  de `pdac_tcga_fluxes_v4r_purity.csv` (triée) à 10⁻⁹ près.
  Rappel v3 : variance expliquée médiane par [acineux, îlots] = 2,0 % sur
  tous les gènes ; R² pureté de KRAS = 0,29 % ; corrélation acineux–îlots
  = 0,4826 (valeurs à recalculer ici, pas à importer).
- Écarts S_sep de référence (§8.48, relus, non recalculés) : IMMROT sans
  doublon, moyenne +0,7521, minimum +0,4508 (CD68), maximum +0,9838 (CD8A) ;
  CD8A réel S_sep 1,2310, nul 0,2472. Régression §8.48 :
  d_ssep = −0,175 + 1,705·C.

### 2.2 NON détenues (manquantes, nommées honnêtement)
- AUCUNE estimation de pureté externe : ni ABSOLUTE, ni ESTIMATE, ni CPE,
  ni cellularité histologique par tumeur. AUCUN score d'infiltration par
  déconvolution : ni CIBERSORT / CIBERSORTx, ni xCell, ni TIMER, ni
  MCP-counter. Vérifié par recherche dans `~/workspace/runs/pdac-v6/`
  (fichiers, scripts, provenances) : 0 occurrence.
- Sources qui permettraient de les obtenir (NON téléchargées dans ce
  chantier) : pureté consensus TCGA d'Aran et al., Nat Commun 2015
  (ABSOLUTE, ESTIMATE, LUMP, IHC ; tableau supplémentaire, via UCSC Xena /
  GDC) ; ESTIMATE (Yoshihara et al., Nat Commun 2013, score stromal /
  immunitaire / pureté estimée depuis l'ARN) ; CIBERSORTx (Newman et al.,
  Nat Biotechnol 2019, fractions de 22 types leucocytaires — accès web,
  compte requis) ; TIMER2.0 (Li et al.). Raison de ne pas les télécharger
  ici : budget zéro respecté (données gratuites mais accès / vérification /
  appariement par barcode = chantier propre), et le test décisif interne
  est faisable avec les proxys du projet — qui sont la définition même de
  « pureté » dans v3/v4. Une pureté externe reste un contrôle indépendant
  ouvert (cf. §8.51.8), pas une donnée de ce chantier.

### 2.3 Ce que « pureté » veut dire ici (limite de mesure, gelée)
Le score acineux mesure la contamination par du pancréas normal acineux
(score haut = plus de tissu normal = pureté tumorale BASSE) ; le score
îlots mesure la contamination endocrine. Ce sont des proxys d'expression,
pas une pureté absolue : ils partagent la même mesure ARN que les flux
immunitaires. Conséquence : une corrélation flux↔score peut refléter une
composition commune sans prouver une causalité ; le test T5 (runs) est le
garde-fou pipeline, et la stratification T4 le garde-fou non paramétrique.
« Infiltration » n'est mesurée ici qu'indirectement : les 12 gènes
immunitaires EUX-MÊMES sont les marqueurs d'infiltration (CD8A/CD8B = T
cytotoxiques, CD68/CD163 = macrophages, CD19 = B, etc.) — il n'existe pas
de score d'infiltration indépendant des flux testés dans ce chantier.
Tester « l'infiltration explique la corrélation » avec les seuls gènes
immunitaires serait circulaire : ce chantier teste la PURETÉ (scores
acineux/îlots, indépendants des 12 gènes), et dit explicitement que
l'infiltration indépendante reste non testée.

## 3. Hypothèses gelées (avant les calculs)
- H1 (pureté explique) : la corrélation intra-famille immunitaire est
  portée par la composition tissulaire (pureté). Prédictions : (a) chaque
  flux immunitaire corrèle substantiellement avec les scores de pureté ;
  (b) après régression sur [acineux, îlots], la corrélation intra-famille
  s'effondre ; (c) ordonner les flux immunitaires par la pureté les sépare
  (S_sep au niveau IMMROT) ; (d) ordonner les flux RÉSIDUALISÉS par CD8A
  résidualisé ne sépare plus.
- H0 (propriété propre) : la corrélation persiste après contrôle de la
  pureté, par toutes les voies (a)–(d). La corrélation est alors une
  propriété des tumeurs (co-expression immunitaire), pas de la composition.

## 4. Définitions gelées
- Base immunitaire : `pdac_immune_tcga_fluxes.csv`, 178 lignes, 12 flux.
- Scores : score_ac (acineux), score_is (îlots), par barcode, log2(RSEM+1).
- Résidus : pour chaque gène immunitaire g, OLS de g sur [1, score_ac,
  score_is] (moindres carrés, 178 patients) ; résidu = observé − prédit.
  Sensibilités : résidus sur [1, score_ac] seul et [1, score_is] seul.
- Couplage C (définition §8.48) : moyenne des |r de Pearson| entre le
  contrôle et les flux analysés. Cohésion H : moyenne des |r| sur les 66
  paires intra-famille.
- Nul du projet : bloc analysé permuté conjointement, default_rng(42),
  colonne de contrôle intacte (même construction que §8.41/§8.44/§8.48).

## 5. Tests gelés et critères de décision (avant les calculs)

### Porte J (jointure, AVANT tout test)
Recharger le tarball (MD5 vérifié), filtrer tumeurs primaires (code 01),
log2(RSEM+1), 0 NaN sur KRAS + 12 gènes immunitaires + 11 acineux +
4 îlots ; ordre KRAS brut recalculé = `immune_kras_order_tcga.csv`
(178/178 barcodes) ; score_ac recalculé = colonne `score_acineux` de
`pdac_tcga_fluxes_v4r_purity.csv` triée, à 10⁻⁹ près. J est OUVERTE si et
seulement si ces trois conditions tiennent. Si J est FERMÉE : arrêt du
chantier, aucun test par index, raison consignée.

### T1 — Chaque flux immunitaire suit-il la pureté ?
Pearson r + Spearman ρ (+ p bilatérale) de chaque flux contre score_ac et
contre score_is ; R² par flux (OLS sur [ac, is]) ; moyenne des |r| sur les
12 flux, pour ac et is. Critère : lien substantiel si moyenne |r| ≥ 0,30
pour au moins un des deux scores ; lien faible si < 0,15 pour les deux.

### T2 — La corrélation intra-famille survit-elle à la régression pureté ?
Matrice 66 paires : brute vs résidus [ac, is] (et sensibilités ac seul,
is seul). Rapportés : moyenne |r|, médiane |r|, fraction |r| > 0,5.
Critère gelé : EFFONDREMENT si moyenne |r| résiduelle < 0,30 (chute
≥ 45 % depuis 0,5563) ET fraction > 0,5 < 0,20 ; PERSISTANCE si chute
< 20 % (moyenne résiduelle > 0,44) ; entre les deux : partielle, à dire.

### T3 — Couplage prédit (sans nouveau run)
C par contrôle immunitaire avant/après résidualisation (12 contrôles) ;
d_ssep prédit par la régression §8.48 (d = −0,175 + 1,705·C), moyenne
prédite brute (doit retrouver ≈ +0,75, sanité) vs résidualisée.
Descriptif, pas un verdict seul : il hérite de la régression §8.48.

### T4 — Stratification par pureté (non paramétrique)
Médiane de score_ac (n = 89/89) et médiane de score_is : matrice
intra-famille dans chaque moitié (moyenne |r|, fraction > 0,5).
Critère : si la cohésion venait de la pureté, elle devrait s'effondrer
dans chaque moitié (bande de pureté étroite) ; persistance dans les deux
moitiés = argument contre H1, indépendant de toute linéarité.

### T5 — Runs v6.2 (6 maximum, prédictions AVANT lecture des sorties)
CSV construits par `build_purity_851.py` (nuls graine 42, construction
du projet) :
- P-AC : contrôle score_acineux, analysés = 12 flux immunitaires bruts,
  lignes triées par score_ac croissant. Réel + nul (2 runs).
- P-IS : contrôle score_îlots, idem. Réel + nul (2 runs).
- P-RES : contrôle CD8A RÉSIDUALISÉ ([ac, is]), analysés = 11 autres flux
  RÉSIDUALISÉS (sans doublon, comme §8.44). Réel + nul (2 runs).
Prédictions (calculées à partir de T1/T2 AVANT de lire les sorties) :
d_pred = −0,175 + 1,705·C_mesuré pour P-AC/P-IS (C = moyenne |r| entre le
score et les 12 flux) ; pour P-RES, d_pred depuis C_résid, et comparaison
directe à CD8A IMMROT observé (écart +0,9838 ; réel 1,2310, nul 0,2472).
Critères gelés : P-AC ou P-IS SOUTIENT H1 si son écart S_sep ≥ 0,45
(minimum IMMROT sans doublon) ; P-RES SOUTIENT H1 si son écart < 0,30
(moyenne des autres familles) ; P-RES SOUTIENT H0 si son écart ≥ 0,45.

### Verdict de synthèse (règle gelée)
- H1 SOUTENUE (pureté explique, en totalité) si T2 = effondrement ET
  P-RES < 0,30 ET (P-AC ≥ 0,45 OU P-IS ≥ 0,45).
- H1 PARTIELLE si T2 = partielle OU (P-AC/P-IS entre 0,30 et 0,45) avec
  P-RES réduit (écart < 0,70, sous les 0,9838 de CD8A brut).
- H0 SOUTENUE (propriété propre aux tumeurs) si T2 = persistance ET
  P-AC < 0,30 ET P-IS < 0,30 ET P-RES ≥ 0,45.
- Toute autre combinaison : zone grise, à dire comme telle, test par test.
Aucun consensus exigé entre les tests : chaque test est rapporté avec son
propre critère ; le verdict suit la règle ci-dessus, pas un vote.

## 6. Nouveaux runs : 6 maximum
Mode fast, graine 42 (défaut pipeline), pipeline v6.2
SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
jamais modifié, vérifié avant et après les runs. Lanceur existant
`run_v62_lot.sh` + manifeste `manifest_v62_purity_851.txt`, log
`runs_v62_purity_851.log`, unité systemd-run `v62-purity-851` (+ relance
reprenable si mort d'unité). Sorties `results_fast_v62_purity851_*`.
Extraction par script dédié `extract_purity_851.py` (mêmes champs que
`extract_immrot_848.py` : max_separation, stability, S_sep = produit).

## 7. Vérifications gelées
- SHA-256 du pipeline v6.2, de la base immunitaire, du fichier d'axe, du
  tarball (MD5) : revérifiés par les scripts avant tout calcul ; tout
  mismatch arrête le chantier (à dire dans la section).
- Aucune valeur S_sep recopiée à la main ; écarts §8.48 relus en machine
  dans `immrot_848_correlations.csv` / `ssep_844_rotations.csv`.
- Aucune conclusion d'une autre expérience n'est importée : seuls les
  chiffres de ce chantier (T1–T5 du jour) et les écarts relus des §8.44/
  §8.48 font le verdict. La variance expliquée v3 (2,0 %) est un fait de
  provenance, pas un résultat de ce chantier.
- Aucun seuil nouveau, aucune sélection d'indicateur après coup.

## 8. Livrables
1. Ce protocole (SHA noté dans le rapport final).
2. Section §8.51 : `~/workspace/runs/pdac-v6/section_8.51_purity_infiltration.md`.
3. Scripts : `analyze_purity_851.py` (porte J, T1–T4),
   `build_purity_851.py` (scores + 6 CSV), `extract_purity_851.py`.
4. Données : `purity_851_scores.csv` (178 tumeurs : barcode, score_ac,
   score_is), `purity_851_results.json/.csv` (T1–T4 + 6 runs),
   `purity_851_csv_sha.json`, manifeste + log du lot.
5. Aucun push GitHub, aucune modification du livre blanc, aucune touche à
   tlogNext-pdac-phase2.

## 9. Ce qui manque (connu d'avance)
- Pas de pureté externe (ABSOLUTE/ESTIMATE) ni de score d'infiltration
  indépendant (CIBERSORT/xCell) : l'infiltration indépendante reste non
  testée (cf. §2.3 — circulaire avec les seuls gènes immunitaires).
- n = 178 : corrélations estimées sur 178 points ; les moitiés T4 sont
  à n = 89 (incertitude plus grande, le dire).
- Les proxys acineux/îlots partagent la mesure ARN avec les flux : une
  corrélation n'est pas une causalité ; T4/T5 sont les garde-fous.
- Ce chantier ne teste pas le sous-type moléculaire (autre variable
  latente du §8.48.8).
