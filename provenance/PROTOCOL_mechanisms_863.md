# PROTOCOLE GELÉ — §8.63 : Mécanismes non élucidés §8.50 / §8.53 (20 novembre 2026)

Go : parent orchestrator, 20 nov. 2026. Ce protocole est gelé AVANT tout
nouveau script, toute nouvelle construction, tout nouveau run et tout
nouveau calcul de ce chantier. Aucun paramètre ne change après les
résultats. Livre blanc NON édité directement (section dans un fichier
séparé `section_8.63_mechanisms.md`). PDF NON régénéré. Rien poussé sur
GitHub. Pipeline v6.2 JAMAIS modifié (SHA attendu
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`).

## 0. Questions

Deux mécanismes sont restés ouverts dans les sections précédentes, lus
dans `section_8.50_mtap_consolidation.md` et `section_8.53_nulls_n70.md`
avant toute écriture de ce protocole :

- **M1 (§8.50.4).** Pourquoi la configuration (28, 27, 6) — choisie par
  les nuls MTAP graine 123 et s11111 — produit-elle à la fois un MC
  élevé et un Delta bas (s11111 : MC 0,5192, Delta 3,0168 ; s123 :
  MC 0,4518, Delta 3,1415), alors que les 9 autres nuls frais restent
  en MC ~0,32–0,34 et Delta ~3,80–3,85, et que le nul 42, lui, donne
  MC 0,5153 avec Delta HAUT (4,3466) ? La configuration CAUSE-t-elle
  le MC haut et le Delta bas, ou les deux phénomènes sont-ils des
  propriétés des permutations, dont la configuration ne serait que
  l'étiquette gagnante ?
- **M2 (§8.53.4).** Par quel mécanisme l'optimiseur choisit-il la
  configuration RÉELLE pour un nul — 17 des 20 nuls frais ICGC
  tournent en w=16/ncand=35 (config réelle ICGC) contre w=16/ncand=22
  pour la config nulle de la réplique ; en TCGA, les deux tirages
  extrêmes (s13 0,4014, s14 0,4811) tournent en w=30/ncand=93, la
  config réelle TCGA, contre w=43/ncand=46 pour la config nulle ?
  L'optimiseur « reconnaît-il » quelque chose du réel, ou la
  « config réelle » n'est-elle que le point d'une grille fixe qui
  maximise le score sur presque toute entrée ?

Faits d'entrée (relus, jamais des verdicts réimportés) :
- MTAP réel v6.2 : S_sep 0,3378 ; MC 0,3511 ; Delta 3,8051 ; config
  (ncand 93, w 30, min_grp 6) ; cascade 0,54 / 60,74 / 72,77 / 92,11 /
  92,11 %. 13 nuls MTAP : 11 en config (93, 30, 6) avec rob ≈ 0,00 ;
  s11111 et s123 en (28, 27, 6) avec rob 0,9756 et 0,6290 ; nul 42 en
  (46, 42, 7) avec rob 0,9756.
- Immunitaires v6.2 : réel ICGC (35, 16, 6), MC 0,3342, maxsep 0,2299 ;
  réel GSE62452 (34, 16, 6), MC 0,3694, maxsep 0,4804 ; réel TCGA
  (93, 30, 6), MC 0,3785, maxsep 0,5309. Nuls frais §8.53 : ICGC 17/20
  en (35, 16, 6), GSE62452 17/20 en (34, 16, 6) (s12 en (22, 16, 7),
  s18 en (38, 24, 9), s26 en (38, 23, 5)), TCGA 4/5 en (93, 30, 6).
- Plancher et distributions §8.53 NON re-testés ici ; ce chantier ne
  touche à aucun verdict de séparation, seulement aux deux mécanismes.

## 1. Mécanique (lue dans le code v6.2, lignes citées, pas devinée)

- **Score MC** (`optimize_threshold_scan_parameters_monte_carlo`,
  lignes 3704–3731 ; `evaluate_scan_quality`, lignes 3314–3389) :
  MC = 0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·acuité, avec
  s_norm = tanh(maxsep/2). La robustesse est une gaussienne sur la
  largeur à mi-hauteur (FWHM) de la courbe de scan :
  rob = exp(−((FWHM − 10)²)/(2·5²)), FWHM mesurée en % de la plage
  des candidats (ligne 3364). Donc rob ≈ 1 si FWHM ≈ 10 %, rob ≈ 0
  si FWHM ≥ ~32 % (pic large / plateau), rob ≈ 0,63 si FWHM ≈ 5 %
  ou ≈ 15 %. Le MC peut donc sauter de ~+0,19 par la seule
  robustesse, sans que maxsep bouge.
- **Optimiseur** (lignes 3453–3461, 243) : mode fast =
  `optimization_iterations: 12`. Chaque itération i tire sa config
  avec `rng = default_rng(random_seed + i)` (random_seed = 42,
  ligne 215), indépendamment des données ; la config ne dépend que
  de n (via `max_w_size = n//2` et `loupe_candidate_bounds`) et de
  la graine fixe. Le gagnant est l'argmax du MC sur ces 12 configs
  (lignes 3800–3870) ; en cas d'égalité, le premier tirage gagne.
  La « configuration choisie » est donc un argmax sur un ensemble
  FIXE par n, pas un échantillonnage adaptatif aux données.
- **Scan** (`_scan_critical_threshold_fast`, lignes 3125–3287) :
  w_size = longueur des fenêtres glissantes (n_windows = n − w + 1) ;
  n_candidates = nombre de seuils candidats sur 0–100 % ;
  min_grp = nombre minimal de fenêtres de chaque côté du seuil.
  Le score d'un candidat est la moyenne sur les flux du |d de Cohen|
  entre groupes pré/post-seuil ; maxsep est le max sur les candidats.
  Plus il y a de candidats et plus les fenêtres sont courtes, plus le
  max sur les candidats est tiré vers le haut (biais de max).
- **Delta** (`compute_holographic_tension_state`, lignes 7928–8022) :
  Delta = d_div − d_sat, où d_sat est la médiane des estimateurs de
  la classe « saturation » (Higuchi, Katz, Petrosian, Sevcik,
  BoxCounting, Hurst2mH, DFA) et d_div celle de la classe
  « divergence » (LevinaBickel, PCAIntrinsic, LocalPCA,
  GraphDimension, PersistentHomology, MFA) — lignes 1927–1935.
  Ces médianes sont calculées sur `df_feat`, construit dans
  `run_pipeline` (lignes 7075–7187) à partir des flux triés par
  progression, avec le **w_size du best_config** (lignes 7079–7081).
  Delta dépend donc de DEUX choses : l'ordre des lignes du CSV
  (permutation) ET le w choisi. Les deux causes sont à séparer
  expérimentalement (voir §2 C2).
- **Axe de progression** (`_build_mc_progress_axis`, lignes 6526–6640) :
  ne dépend que du rang du contrôle et de la graine 42, pas de w ni
  des flux. Pour un contrôle monotone, il ne dépend que de n.

## 2. Méthodes — dans l'ordre, sans retour en arrière

### A. Lecture des `all_results` existants (aucun run, script neuf)

Script neuf `mechanisms_863.py` (lecture seule des
`master_results.json` déjà sur disque) : pour chaque run MTAP (14 :
réel, réel 850, nul 42, s7, s123, 10 frais) et immunitaire (48 :
3 réels, 45 nuls §8.53 dont 5 TCGA), extrait la liste complète des
12 configs évaluées (`threshold_optimization.all_results`) avec,
par config : (ncand, w, min_grp, règle), seuil, MC, s_norm,
stabilité, robustesse, acuité, maxsep. Vérifie : (A1) l'ensemble
des 12 configs est-il identique entre runs de même n (MTAP n=177 :
14/14 ; ICGC n=70 : 20 frais + 4 anciens §8.47 + réel ; GSE62452
n=69 : 20 frais + 3 anciens + réel ; TCGA n=178 : 5 frais + 3
anciens + réel) ? (A2) recomposition du MC
0,3·s_norm + 0,3·stab + 0,2·rob + 0,2·acuité, écart toléré 10⁻⁶.
(A3) FWHM recalculée depuis chaque `scan_curve` stockée
(extension contiguë autour du pic au-dessus de maxsep/2, en % des
candidats, même algorithme que les lignes 3340–3364) et rob
recomposée par la gaussienne — écart toléré 10⁻⁶ sur rob, sur les
12 configs × 14 runs MTAP et 12 configs × 3 runs TCGA extrêmes
(s13, s14) + ICGC s26/s29. (A4) D_vector et médianes par estimateur
(`reading_synthesis.per_estimator`) des 14 runs MTAP : d_sat,
d_div, d_crit, d_null, et pour chacun des 6 estimateurs de
divergence et 7 de saturation, sa médiane brute.

### B. Réplique du scan (fonctions DU PIPELINE, import en lecture seule)

Même pattern que `replica_nulls_n70_853.py` (calibration 8/8 EXACTS
en §8.53) : `_build_mc_progress_axis` + `scan_critical_threshold`
+ `evaluate_scan_quality`, importés sans modification.
- **Calibration d'abord** : reproduire, pour 5 entrées (MTAP réel,
  MTAP s11111, MTAP s123, ICGC réel, ICGC nul s29), le score MC et
  les métriques des 12 configs stockées à |Δ| ≤ 10⁻⁶ (courbe
  comprise à 10⁻⁶). Si la calibration échoue, la réplique est
  rejetée et les sous-questions qui en dépendent sont consignées
  « non élucidables par cette voie » — arrêt sur ce volet, pas de
  contournement.
- **Puis, M1a** : le tableau complet 12 configs × 5 entrées MTAP
  (réel, s11111, s123, nul42, s1011 comme témoin rob-off) est
  re-vérifié par la réplique (il doit coïncider avec les
  `all_results` stockés ; sinon, l'écart est consigné et la lecture
  s'arrête aux valeurs stockées).
- **Puis, M1c (porteurs du pic)** : pour chaque run rob-on MTAP
  (s11111, s123, nul42) et 3 témoins rob-off (s1011, s2022, s9099),
  sous la config gagnante, courbes de scan par flux SEUL (appel du
  scan avec un seul flux : le score rendu est alors le |d| de ce
  flux ; la moyenne des 12 courbes doit reproduire la courbe
  complète à 10⁻⁶ — calibration interne). Lecture au candidat du
  pic complet : |d| par flux, part du flux dominant dans la somme
  des |d|.

### C. Réplique Delta : séparer w de la permutation (miroir du code)

Script neuf `replica_delta_863.py` : miroir EXACT du bloc
`run_pipeline` lignes 7075–7187 (scan_points = 120 points sur
l'axe de progression MC ; tol ; fenêtres triées par progression ;
séries concaténées par flux ; `apply_complexity` importée du
pipeline ; `mode_cfg_dynamic` avec min_len = max(10, w//2), mode
fast, n_est=1, boot=False) suivi de `compute_holographic_tension_state`
importée du pipeline. Seul paramètre libre : w.
- **Calibration d'abord** : reproduire le D_vector stocké
  (d_sat, d_crit, d_div, d_null) à |Δ| < 10⁻⁶ pour 5 CSV
  (MTAP réel, s11111, s123, nul42, s1011) à leur w propre
  (30, 27, 27, 42, 30). Si la calibration échoue sur un CSV, le
  volet C s'arrête pour ce CSV et le Delta est consigné
  « non élucidable par cette voie ».
- **Puis, croisement** : w ∈ {27, 30} × CSV ∈ {réel, s11111, s123}
  (6 cellules) + w=42 sur s11111 et s123 à titre de contrôle
  (le w du nul 42) : Delta, d_sat, d_div par cellule. La part de
  l'écart portée par w se lit en comparant, à CSV fixé,
  Delta(w=27) − Delta(w=30) à l'écart entre CSV à w fixé.
- **Puis, porteurs de d_div** : pour chaque cellule, médianes des
  6 estimateurs de divergence (et des 7 de saturation) ; l'estimateur
  qui porte la chute de d_div est celui dont l'écart entre s11111
  (ou s123) et réel, à w fixé, est le plus grand en valeur absolue.

### D. Lot pipeline v6.2 — réplication hors échantillon de M2 (10 runs)

- **Construction** (`build_nulls_icgc_863.py`, neuf) : 10 nuls ICGC
  frais, même méthode que `build_nulls_n70_853.py`
  (`default_rng(graine)`, `permutation(n)`, lignes entières,
  colonne step inchangée), graines 31–40 — jamais utilisées
  (§8.47 : 1–3, 42 ; §8.53 : 11–30). Entrée vérifiée par SHA avant
  construction : `pdac_immune_icgc_fluxes.csv` (SHA relu dans
  `nulls_n70_853_verify.json`, re-vérifié ici). Sorties :
  `pdac_immune_icgc_fluxes_nul_s<graine>.csv` (+ SHA-256).
- **Runs** : v6.2 mode fast, 10 runs, sorties
  `results_fast_v62_863_icgc_nul_s<graine>/`, lanceur reprenable
  `run_v62_863.sh`, manifeste `manifest_v62_863.txt`,
  `systemd-run` (jamais nohup), journal `runs_v62_863.log`
  (SHA v6.2 avant/après, exits). Exit 0 exigé pour les 10 runs ;
  un run interrompu (redémarrage machine) est relancé tel quel
  après suppression de son dossier partiel (sans
  `master_results.json`) ; jamais remplacé par une autre graine.
- **Lecture** : les 10 runs entrent dans les tableaux de l'étape A
  (ensemble de configs, vainqueur, marge) et dans le critère M2d
  (§3). Aucun autre run v6.2 nouveau dans ce chantier : M1 ne
  nécessite aucun run neuf (tout est dans les 14 runs existants +
  répliques calibrées).

### E. Ce qui n'est PAS fait

- Aucune modification du pipeline, aucun nouveau seuil, aucune
  sélection d'indicateur après coup, aucune imputation, aucune
  valeur inventée, aucun nouveau nul construit après lecture des
  résultats (les graines 31–40 sont gelées ici avant tout run).
- Aucune conclusion importée d'autres bras (rotations, tests A/C,
  PARP, §8.54–§8.62) : seules les données et runs de ce chantier
  font verdict, sauf citation explicite « relu §8.50 / §8.53 »
  pour les faits de départ.
- Aucun test direct nouveau (PRMT5, prolifération, survie).
- Le plancher 0,07 (§8.46/§8.50) et les planchers p95 (§8.53) ne
  sont ni re-testés ni redéfinis ici.

## 3. Règles de décision — écrites avant (par sous-question)

**M1a — le MC haut vient-il de la config (28, 27, 6) ?**
- **EXPLIQUÉ (par la permutation, pas la config)** si (i) la FWHM
  recalculée reproduit rob à 10⁻⁶ sur toutes les configs testées
  (§2 A3) ; ET (ii) sur s11111 ET s123, la config (93, 30, 6) donne
  aussi MC > 0,44 avec rob > 0,5 sur la MÊME entrée ; ET (iii) les
  11 autres runs MTAP ont max rob < 0,1 sur leurs 12 configs.
  Alors le MC haut est une propriété de la permutation (pic étroit
  de la courbe de scan) et la config (28, 27, 6) ne fait que gagner
  de ~0,005 sur (93, 30, 6).
- **PARTIELLEMENT EXPLIQUÉ** si (i) tient mais (ii) ne tient que
  sur un des deux nuls, ou si (iii) échoue (d'autres runs ont des
  configs rob-on sans MC haut).
- **NON ÉLUCIDÉ** si (i) échoue (la formule rob ne se reproduit pas
  depuis les courbes stockées).

**M1b — le Delta bas vient-il de w=27 ou de la permutation ?**
- **EXPLIQUÉ** si la calibration Delta tient à 10⁻⁶ sur les 5 CSV
  ET, sur le croisement w×CSV, l'écart de Delta entre CSV à w fixé
  est au moins 5 fois l'écart entre w à CSV fixé (la permutation
  porte ≥ 5/6 de l'écart — verdict « permutation ») OU l'inverse
  (w porte ≥ 5/6 — verdict « w »). Le verdict nomme le porteur.
- **PARTIELLEMENT EXPLIQUÉ** si la calibration tient mais le
  partage w/permutation est entre 1/6 et 5/6.
- **NON ÉLUCIDÉ** si la calibration Delta échoue (la réplique ne
  reproduit pas le D_vector stocké).

**M1c — MC haut et Delta bas ont-ils une cause commune ?**
- **CAUSE COMMUNE** si un même flux porte ≥ 50 % de la somme des
  |d| au seuil gagnant dans les 3 runs rob-on (s11111, s123, nul42)
  ET le même estimateur de divergence porte la plus grande chute
  de d_div dans s11111 et s123 (même signe, à w fixé).
- **DEUX CONSÉQUENCES INDÉPENDANTES** si les porteurs diffèrent
  entre le pic (MC) et d_div (Delta), ou entre runs, ou si le nul
  42 (rob-on, Delta HAUT) contredit le lien.
- **NON TRANCHÉ** si les porteurs ne sont identifiables ni dans un
  sens ni dans l'autre (parts diffuses, < 50 % partout, estimateurs
  dispersés).
- Verdict global **M1 = EXPLIQUÉ** seulement si M1a ET M1b sont
  expliqués (M1c qualifie le lien : cause commune / indépendance /
  non tranché) ; **PARTIELLEMENT EXPLIQUÉ** si l'un des deux est
  partiel et l'autre au moins partiel ; sinon **NON ÉLUCIDÉ**.

**M2a — l'ensemble des configs est-il fixe par n ?**
- **EXPLIQUÉ** si 1 seul ensemble distinct de 12 configs par n sur
  tous les runs relus + lot frais (ICGC, GSE62452, TCGA, MTAP).
  Sinon le mécanisme est infirmé tel que formulé (consigné).

**M2b — pourquoi la config réelle gagne-t-elle sur les nuls ?**
- **EXPLIQUÉ** si, sur les nuls frais, la config réelle a le maxsep
  moyen le plus élevé des 12 configs dans les DEUX cohortes
  n≈70 (ICGC et GSE62452) ET le maxsep moyen croît avec
  n_candidates à w comparable (Spearman > 0,5 entre maxsep moyen et
  n_candidates sur les 12 configs, ou, à défaut de monotonie
  globale, la config gagnante est la plus fine grille parmi les
  configs de petit w dans chaque cohorte). Alors le choix est un
  biais de max (grille fine × fenêtre courte), et la « config
  réelle » n'est que l'étiquette du point de grille qui maximise le
  max — l'optimiseur ne reconnaît rien du réel.
- **PARTIELLEMENT EXPLIQUÉ** si une seule des deux cohortes
  vérifie la condition.
- **NON ÉLUCIDÉ** si aucune des deux, ou si le maxsep moyen de la
  config réelle n'est pas le plus élevé.

**M2c — marges (qualification, pas un critère d'explication).**
Médiane et distribution des marges vainqueur − 2e sur les 45 runs
§8.53 + 3 réels + 10 frais. Une marge médiane < 0,01 est consignée
comme « choix quasi-ex-aequo » : l'étiquette de config gagnante est
instable d'un tirage à l'autre.

**M2d — réplication hors échantillon (lot frais ICGC s31–s40).**
- **CONFIRME** si ≥ 7/10 choisissent (35, 16, 6).
- **INFIRME** si ≤ 4/10.
- **INDÉCIS** entre 5 et 6 (p binomial exact rapporté, H0 p = 0,85).
- Verdict global **M2 = EXPLIQUÉ** si M2a ET M2b expliqués et M2d
  confirme ; **PARTIELLEMENT EXPLIQUÉ** si M2a et M2b expliqués
  mais M2d indécis, ou si M2b partiel ; sinon **NON ÉLUCIDÉ**.

## 4. Sorties

- Ce protocole `PROTOCOL_mechanisms_863.md` (SHA noté dans la
  section).
- Scripts neufs : `mechanisms_863.py`, `replica_delta_863.py`,
  `build_nulls_icgc_863.py`, `run_v62_863.sh` (SHA notés dans la
  section).
- Données/résultats : `mechanisms_863_extract.json`,
  `mechanisms_863_results.csv` (tableaux par config et par run),
  `replica_delta_863.json` (calibration + croisement w×CSV),
  `mechanisms_863_perflux.csv` (porteurs du pic, M1c),
  `nulls_icgc_863_files.json` (SHA des 10 nuls frais),
  `manifest_v62_863.txt`, `runs_v62_863.log` (10/10, exit 0),
  dossiers `results_fast_v62_863_icgc_nul_s<graine>/`.
- Section `section_8.63_mechanisms.md` (verdict d'abord, chiffres,
  méthode, limites, provenance — format des sections précédentes).

## 5. Limites connues d'avance

- n = 177 (MTAP), 70/69/178 (immunitaires) ; 12 configs seulement
  par run en mode fast — l'« optimiseur » étudié est celui du mode
  fast, pas celui des modes robust/stable/full (plus d'itérations).
- La réplique Delta est un miroir de code inline : sa calibration
  à 10⁻⁶ est la porte d'entrée, pas une formalité — si elle échoue,
  le volet Delta reste non élucidé.
- Les 10 nuls frais ICGC testent la réplication du TAUX de choix
  de la config réelle, pas le mécanisme lui-même (le mécanisme est
  lu dans le code + les `all_results`).
- Un mécanisme fermé comme non élucidable est un résultat, pas un
  échec : il est consigné comme tel, avec ce qui a été tenté.
- La FWHM est mesurée sur la courbe discrète des candidats : sa
  valeur dépend de la grille (n_candidates) autant que de la forme
  de la courbe — cet effet de grille fait partie du mécanisme, il
  est mesuré (M2b), pas corrigé.
