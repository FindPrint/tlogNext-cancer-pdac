# PROTOCOLE GELÉ — Piste Œil : privilège immunitaire de l'œil contre évasion immunitaire du pancréas (§8.81)

Date : 21 nov. 2026. Go parent 21 nov. 2026 (piste Œil proposée par Zackary le 21 nov., lancée le jour même).
Ce protocole est gelé AVANT toute construction et tout run sur cette question.
Aucun run sans ce fichier. Aucun paramètre ne change après les résultats.
Livre blanc NON édité, PDF NON régénéré, rien poussé sur GitHub (convention des chantiers ; fusion par le coordinateur).
La section §8.81 est écrite dans un FICHIER SÉPARÉ (`section_8.81_oeil_privilege.md`).
Les §8.78 (inventaire), §8.79 (13e paire), §8.80 (vopimetostat) sont pris par d'autres agents — ce numéro n'est utilisé nulle part ailleurs ici.

## 0. Question à trancher

La tumeur du pancréas copie-t-elle les mécanismes du privilège immunitaire de l'œil pour se cacher ?
Contexte vérifié (pas un verdict importé — la motivation, pas la preuve) :
- L'œil est un site à privilège immunitaire : barrières sang-œil, ACAID (déviation immune associée à la chambre antérieure),
  FasL (FASLG), TGF-β, faible expression HLA.
- La tumeur du pancréas devient « froide » quand KRAS monte : les gènes des lymphocytes tueurs chutent
  (PDCD1 rho −0,25 / −0,24 / −0,22 / −0,22 sur 4 cohortes ; top-12 d −0,61 à −0,88 ; §8.23).
  KRAS + anti-PD-(L)1 : pas de rationnel (§8.23).
- Règle du 15 nov. : les données / conclusions d'AUTRES expériences ne sont PAS importées comme verdicts —
  tout ce qui est testé ici l'est avec protocole gelé et runs du jour.

Réponse attendue : OUI / NON / MIXTE, par gène et pour le score, avec les chiffres mesurés aujourd'hui.
Un négatif est un résultat. Les verdicts de ce bras ne rouvrent rien : C3 reste levée, test C reste NON,
adoption pleine de maxsep reste la décision de Zackary (20 nov. 2026, 13h04).

## 1. Gènes gelés

Gènes du privilège oculaire (7, liste fermée, fixée par la tâche) :
FASLG, TGFB1, TGFB2, IDO1, HLA-G, CD47, CD274 (PD-L1).
Gènes de référence « froid » (4, déjà mesurés au §8.23, relus comme témoins, jamais recalculés depuis le §8.23) :
PDCD1, CD8A, GZMB, IFNG. Attendu : ils CHUTENT avec KRAS (rho négatif) — si ce témoin ne se reproduit pas
aujourd'hui, c'est consigné et ça affaiblit la lecture des 7 autres.
Les 12 gènes v4 (chaîne du §8.11) : PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16.
Aucun autre gène n'est ajouté après avoir vu les chiffres. Un gène absent d'une matrice est NOMMÉ, pas imputé,
pas remplacé par un synonyme, pas cherché sous un autre nom.

## 2. Données et versions gelées

- Pipeline : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256 attendu `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant tout run ; le fichier n'est JAMAIS modifié). Minimum fast = 40 points.
- Cohortes PDAC (fichiers déjà sur le disque, rien de re-téléchargé) :
  - TCGA-PAAD : `data/tcga_paad_rsem.tar.gz`, MD5 `b09569ce3f4721f514bc137bd109ac0a`
    (Firehose stddata 2016-01-28, RSEM genes normalized). 178 tumeurs primaires (code 01).
    Base v4 : `pdac_tcga_fluxes_v4.csv`, SHA `e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0`.
  - GSE71729 : `data/GSE71729_series_matrix.txt.gz` (GPL20769, symboles directs). 145 tumeurs primaires.
  - GSE62452 : `data/GSE62452_series_matrix.txt.gz` (GPL6244, mapping `data/GPL6244_probe2symbol.tsv`). 69 tumeurs.
  - ICGC PACA-AU : `data/icgc_pacaau_exp.txt.gz` + `data/icgc_pacaau_probemap.gz` (log2 CPM, Bailey et al. 2016). 70 tumeurs primaires PDAC.
- TCGA-UVM (mélanome uvéal, n = 80 attendu) : À TÉLÉCHARGER (voir §5). Si le téléchargement échoue,
  la partie UVM est déclarée INUTILISABLE avec la raison exacte, et le reste du chantier n'en dépend pas.

## 3. Tests directs (harnais, hors pipeline) — méthode gelée

Pour chaque cohorte PDAC, pour chaque gène des 7 + 4 témoins, présent dans la matrice :
- Valeur utilisée : TCGA = RÉSIDU après correction de pureté (même régression que la v4 : [1, score acineux, score îlots],
  recalculée depuis le tarball et vérifiée contre le CSV v4 à atol 1e-9, comme au test C) ; GEO/ICGC = valeur fournie
  (même règle que les flux variante (a) : sans correction, cas complets seulement, jamais d'imputation).
- Axe KRAS : TCGA = résidu KRAS croissant (même ordre que la v4) ; GEO/ICGC = expression KRAS croissante
  (même ordre que les CSV de flux variante (a)). KRAS n'est jamais un flux.
- (T1, test PRINCIPAL) Spearman rho du gène contre le rang KRAS (n complet), p bilatérale.
  C'est le test informatif (correction §8.70/§8.71 : le d de Cohen marginal réel-vs-nul est VACUEUX par construction
  quand le nul est une permutation de lignes — il est rapporté comme contrôle de construction, valeur attendue 0,0000,
  et ne décide rien).
- (T2, descriptif) d de Cohen top-12 (12 tumeurs KRAS le plus fort) contre reste, réel ET nul (mêmes indices de lignes
  sur le nul graine 42) ; + = plus haut chez les KRAS-fort. Lecture contre le nul, pas contre 0.
- (T3) Score PRIV (voir §4) : rho du score contre le rang KRAS, par cohorte ; rho de chaque gène de privilège
  contre le score PRIV (cohérence interne, descriptif).

Critères gelés AVANT les runs (par gène, sur les cohortes où il est présent) :
- MONTE avec KRAS : rho > 0 dans ≥ 3 cohortes sur 4 (ou toutes les cohortes où présent, si < 4) ET rho médian > +0,15.
- DESCEND avec KRAS : rho < 0 dans ≥ 3 cohortes sur 4 ET rho médian < −0,15.
- MIXTE / SANS SENS : tout le reste. Aucun seuil de p n'est imposé comme condition (les p sont rapportées) :
  avec n = 69–178, |rho| > 0,15 est déjà au-delà du bruit d'un nul permuté (|rho| nul attendu ≤ ~0,10, cf. §8.36/§8.45).
- Verdict global « la tumeur copie le privilège » : OUI si ≥ 4 des 7 gènes MONTENT (ou si le score PRIV monte avec
  rho médian > +0,15 sur ≥ 3 cohortes) ; NON si ≤ 1 gène MONTE et le score PRIV ne monte sur aucune cohorte ;
  MIXTE entre les deux. Le verdict est porté par les tests directs, pas par le pipeline seul.

## 4. Score de privilège immunitaire (définition gelée)

PRIV(tumeur) = moyenne des z-scores (par gène, à l'intérieur de la cohorte : z = (x − moyenne) / écart-type)
des gènes de privilège PRÉSENTS dans la matrice de cette cohorte. Gènes absents : exclus du score, sans imputation,
le nombre de gènes du score est rapporté par cohorte. Le score est calculé AVANT tout run, sur les valeurs du §3.
Le score n'est PAS un flux v4 et n'est PAS parmi les 12 : aucun doublon contrôle/flux.
Bras pipeline (§6) : TCGA uniquement, série ordonnée par PRIV croissant.

## 5. Comparaison avec le cancer de l'œil : TCGA-UVM

- Source tentée en premier : Broad GDAC Firehose stddata 2016-01-28, UVM, RSEM genes normalized —
  même série que le tarball PAAD, URL :
  `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/UVM/20160128/gdac.broadinstitute.org_UVM.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz`
  (pattern vérifié contre l'URL PAAD connue ; si le pattern échoue, repli : API GDC
  `https://api.gdc.cancer.gov/data/...` ou UCSC Xena TCGA-UVM — la voie réellement utilisée est consignée
  dans PROVENANCE_881.md avec URL, date, SHA).
- Si le fichier est obtenu : n attendu 80 tumeurs primaires (code 01). Mêmes gènes testés (12 v4 + 7 privilège + 4 témoins),
  présence nommée par gène, sans correction de pureté (pas de scores acineux/îlots pour l'œil — ce serait importer
  une correction pancréatique ; les valeurs sont prises en log2(RSEM+1), même échelle que TCGA-PAAD brut).
- Tests directs UVM (gelés) :
  (U1) Niveaux médians log2(RSEM+1) par gène, UVM vs TCGA-PAAD brut (même échelle, mêmes gènes) : d de Cohen
  entre cohortes, + = plus haut en UVM. Question : le mélanome uvéal exprime-t-il PLUS les gènes de privilège
  que le pancréas, et MOINS les gènes tueurs (est-il « froid » comme le pancréas KRAS-fort, ou autrement) ?
  (U2) Pipeline v6.2 sur UVM ordonné par score PRIV (même définition §4, z intra-UVM), réel + nul graine 42,
  SI n ≥ 40 ; sinon aucun run UVM, dit plainement.
  (U3) Chaîne v4 dans UVM : d top-12 PRIV vs reste pour les 12 gènes v4 (même lecture que §6 D1) — la chaîne du §8.11
  réapparaît-elle sous l'ordre PRIV dans l'œil ?
- Si TCGA-UVM est inutilisable (téléchargement impossible, n < 40, gènes absents en masse) : le dire plainement
  avec la raison (source, URL tentée, erreur) dans PROVENANCE_881.md et dans §8.81 — AUCUNE substitution
  (pas d'autre cohorte œil inventée, pas de lignée cellulaire à la place).

## 6. Bras pipeline v6.2 (TCGA, ordre PRIV)

- Construction : `build_priv_881.py`. Série réelle `pdac_tcga_fluxes_v4_priv.csv` :
  1re colonne PRIV (contrôle, valeur du score, continue), puis les 12 flux v4 dans l'ordre v4,
  lignes triées par PRIV croissant. Vérification de reproduction v4 (résidus recalculés, atol 1e-9) AVANT
  la construction — arrêt si écart > atol, comme au test C.
- Nul : `pdac_tcga_fluxes_v4_priv_nul.csv`, bloc des 12 flux permuté par lignes, graine 42, générateur frais
  rng(42), colonne PRIV intacte (même convention que les autres nuls).
- Runs : 2, mode fast, v6.2, manifeste `manifest_v62_881.txt`, lanceur reprenable `run_v62_lot.sh`,
  journal `runs_v62_881.log`. Sorties `results_fast_v62_881_priv/` et `results_fast_v62_881_priv_nul/`.
  Lancement résistant aux redémarrages : `systemd-run --unit=v62-881 --collect ...` (jamais nohup).
  Ne JAMAIS supprimer le dossier d'un run en cours.
- Lecture (extracteur : copie adaptée de `extract_ssep_838.py`, original intact) : cascade, MC best_config
  + métriques (max_separation, stabilité, S_sep = max_separation × stabilité), Delta, L7a, falsification,
  bruit, F1/F2 « Tous ». L7b : audit clos comme non-informatif, rapporté sans interprétation.
- Tests directs sur la série PRIV (harnais, `priv_reading_881.py`) :
  (D1) top-12 PRIV contre reste, flux par flux (d de Cohen, + = plus haut chez les 12 PRIV le plus fort),
  réel contre nul. Signature cherchée (référence §8.4) : PGC −0,89, DPCR1 −0,85, CLDN18 −0,46, MUC16 +0,64.
  La chaîne « apparaît » si PGC / DPCR1 / CLDN18 chutent ET MUC16 monte au bout de l'axe PRIV, au-delà du bruit du nul.
  (D2) Spearman rho de chaque flux v4 contre le rang PRIV, réel vs nul (test informatif, correction §8.70/§8.71).
  (D3) Autour de T_0 si un T_0 existe (fenêtres ±20 lignes) : d par flux, réel contre nul. Sinon, le dire.
- Critère gelé : la chaîne réapparaît si D1 + D2 la montrent au-delà du nul. Le pipeline seul ne décide pas :
  d_maxsep > 0,07 (plancher) est rapporté comme piste, jamais comme preuve (convention §8.31/§8.32).
  Si le score PRIV n'ordonne rien (tous les rho ≈ 0, d_maxsep ≤ 0,07, D1 plat), le dire plainement :
  « le score de privilège n'ordonne pas les tumeurs TCGA ».

## 7. Livrables

- Ce protocole (gelé avant les runs).
- `build_priv_881.py` + `direct_tests_881.py` + `priv_reading_881.py` + `extract_881.py` (SHAs en provenance).
- `PROVENANCE_881.md` (sources, URLs, dates, SHA de chaque fichier écrit ; gènes absents par matrice ;
  effectifs ; tentative UVM complète).
- `manifest_v62_881.txt`, `runs_v62_881.log`, dossiers de résultats (2 TCGA + 2 UVM si UVM utilisable).
- Tables vérifiées : `priv_direct_tests_881.csv`, `priv_extract_881.json`, `uvm_direct_tests_881.csv` (si UVM).
- §8.81 dans le FICHIER SÉPARÉ `section_8.81_oeil_privilege.md` (verdict d'abord, chiffres ensuite).
- PDF NON régénéré. Rien poussé sur GitHub.

## 8. Réserve de méthode — nommée d'avance, à reprendre dans §8.81

Le « privilège immunitaire de l'œil » est un concept d'immunologie tissulaire (barrières, ACAID, FasL, TGF-β),
pas une grandeur mesurée ici : ce chantier mesure 7 gènes d'expression, pas le privilège lui-même.
Une corrélation entre ces gènes et KRAS ne prouve pas une copie de mécanisme — elle dit seulement que ces
gènes montent (ou non) avec KRAS dans ces cohortes. Le mélanome uvéal n'est pas « l'œil normal » : c'est un
cancer d'un site à privilège, pas le tissu sain — la comparaison UVM vs PDAC compare deux cancers, pas un
cancer à un privilège intact. Les cohortes sont hétérogènes (RNA-seq TCGA/ICGC, puces Agilent/Affymetrix) :
les rho intra-cohorte sont comparables, les niveaux bruts inter-cohortes ne le sont qu'en descriptif (U1).
Aucune donnée single-cell, spatiale, ni protéique de l'œil ; aucune mesure fonctionnelle (cytotoxicité, ACAID).
Un négatif ne dit pas que la tumeur n'échappe pas au système immunitaire — seulement qu'elle ne le fait pas
par ces 7 gènes le long de l'axe KRAS, dans ces cohortes.
