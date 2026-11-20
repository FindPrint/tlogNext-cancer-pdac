# PROTOCOLE GELÉ — §8.73 : Déclencheur du pic étroit (§8.63, résidu ouvert)
# (20 novembre 2026)

Go : parent orchestrator, 20 nov. 2026. Ce protocole est gelé AVANT tout
nouveau script, toute nouvelle construction, tout nouveau run et tout
nouveau calcul de ce chantier. Aucun paramètre ne change après les
résultats. Livre blanc NON édité directement (section dans un fichier
séparé `section_8.73_pic_etroit.md`). PDF NON régénéré. Rien poussé sur
GitHub. Pipeline v6.2 JAMAIS modifié (SHA attendu
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`).

## 0. Question

§8.63 a expliqué M1 (le MC haut est une propriété de la permutation, le
Delta bas une propriété de w=27) et M2 partiellement, mais le résidu
ouvert, commun à M1a et M2d, est : **QU'EST-CE QUI DÉCLENCHE le pic
étroit de la courbe de scan (FWHM ≈ 11–15 %, rob > 0,5) quand on
permute — quelle propriété de la matrice permutée (ou du tirage) le
fait apparaître, et pourquoi certaines permutations le déclenchent et
d'autres non ?**

Faits d'entrée (relus avant gel dans `section_8.63_mechanisms.md` et
`mechanisms_863_extract.json`, SHA
`2224df358546285afa1332d6ea09f28afd12742b2ce3a9e716adbea0d557c62e`,
jamais des verdicts réimportés) :
- Courbes rob-on (rob > 0,5) : 8 en MTAP, ~27 en immunitaire, sur
  82 runs × 12 configs = 984 courbes. Leurs pics sont presque tous
  près d'un bord (seuil 10–33 % ou 76–89 %) et, pour un même CSV, le
  pic tombe à la MÊME position (±2 candidats) sous plusieurs configs
  (ex. s11111 : 11,11 % et 10,87 % ; s123 : 88,89 % et 88,04 % ;
  s35/s37 : 19,05 % et 17,65 %) — compatible avec un bloc fixe dans
  l'ordre des lignes, pas avec une propriété de la grille.
- Aucun flux ne porte le pic (part maximale 0,18–0,25, §8.63.4).
- Le nul est une permutation des lignes entières (les 12 flux d'une
  tumeur voyagent ensemble), colonne de contrôle (`MTAPCN` / `step`)
  inchangée ; la réplique §8.63 utilise l'axe de progression
  `_build_mc_progress_axis(np.arange(n))`, monotone en l'indice de
  ligne : l'ordre des lignes EST la progression.

Ensemble de test relu avant gel — les 11 courbes GAGNANTES rob-on
(rob > 0,5 à la config gagnante), qui sont l'objet des interventions :
- MTAP : NUL42 (46, 42, 7), MC 0,5153, rob 0,9756, FWHM 11,11,
  seuil 84,44 ; NUL_S123 (28, 27, 6), MC 0,4518, rob 0,6290,
  FWHM 14,81, seuil 88,89 ; NUL_S11111 (28, 27, 6), MC 0,5192,
  rob 0,9756, FWHM 11,11, seuil 11,11.
- Immunitaires : icgc_s1 (39, 24, 9), MC 0,5262, rob 0,9945,
  FWHM 10,53, seuil 28,95 ; geo62452_nul_s12 (22, 16, 7), MC 0,4639,
  rob 0,6926, FWHM 14,29, seuil 23,81 ; tcga_s2 (37, 84, 5),
  MC 0,5144, rob 0,9756, FWHM 11,11, seuil 27,78 ; tcga_nul_s11
  (93, 30, 6), MC 0,5324, rob 0,9991, FWHM 9,78, seuil 11,96 ;
  tcga_nul_s12 (22, 42, 7), MC 0,4715, rob 0,6926, FWHM 14,29,
  seuil 19,05 ; icgc_nul_s32 (14, 23, 2), MC 0,4320, rob 0,5600,
  FWHM 15,38, seuil 76,92 ; icgc_nul_s35 (22, 16, 7), MC 0,4682,
  rob 0,6926, FWHM 14,29, seuil 19,05 ; icgc_nul_s37 (22, 16, 7),
  MC 0,4935, rob 0,6926, FWHM 14,29, seuil 19,05.
- Contrôles (config gagnante rob < 0,05, vérifié avant gel :
  rob = 0,0000 pour les 6) : MTAP s7 et s1011 (93, 30, 6) ;
  ICGC s31 et s33 (35, 16, 6) ; GSE62452 s11 (34, 16, 6) ;
  TCGA s13 (93, 30, 6). Règle de sélection gelée : par série,
  premiers runs (graines croissantes) dont la gagnante a rob < 0,05
  — 2 MTAP, 2 ICGC, 1 GSE62452, 1 TCGA.

## 1. Mécanique (lue dans le code v6.2, lignes citées, pas devinée)

- Scan (`_scan_critical_threshold_fast`, lignes 3125–3287) : lignes
  triées par l'axe de progression (monotone en l'indice de ligne) ;
  fenêtres glissantes de longueur w (n_windows = n − w + 1) ; chaque
  fenêtre a une progression moyenne win_progress, monotone en son
  indice de départ (vérifié : win_order = identité pour n=177, w=27
  et n=70, w=16 — le script l'assert à chaque usage, et consigne
  l'exclusion de la courbe si l'identité est violée) ; candidats =
  linspace(0, 100, ncand) ; à chaque candidat c, split(c) = nombre de
  fenêtres avec win_progress < c ; score(c) = moyenne sur les 12 flux
  du |d de Cohen| entre les contenus des fenêtres basses et hautes
  (chaque ligne apparaît dans jusqu'à w fenêtres, avec recouvrement).
- Robustesse (`evaluate_scan_quality`, lignes 3314–3389) :
  rob = exp(−((FWHM − 10)²)/(2·5²)), FWHM = largeur à mi-hauteur
  contiguë autour du pic, en % de la plage des candidats. rob > 0,5
  ⟺ FWHM ∈ [5,9 % ; 15,9 %] environ ; rob < 0,1 ⟺ FWHM ≤ ~1 % ou
  ≥ ~21 %.
- Conséquence mécanique (dérivée, pas devinée) : deux candidats
  voisins ne diffèrent que par le passage d'environ
  n_windows/ncand fenêtres d'un groupe à l'autre. Un pic ÉTROIT
  (score haut à c*, bas à c*±1 pas) exige donc que les fenêtres qui
  franchissent la coupure à c* aient des contenus collectivement
  très différents du reste — et que le petit côté de la coupure
  (près d'un bord : split petit, min_grp fenêtres) soit dominé par
  ces fenêtres. Le « déclencheur » est donc cherché comme un BLOC
  DE LIGNES : les lignes du petit côté à c*, définies ci-dessous
  sans utiliser la courbe de scan (sauf pour localiser c*).

## 2. Définitions gelées (appliquées par les scripts, sans exception)

- Colonnes de flux : toutes les colonnes du CSV sauf la colonne de
  contrôle (`MTAPCN` ou `step`), dans l'ordre du CSV.
- Extrémité de ligne : par flux j, med_j = médiane, mad_j =
  médiane(|x − med_j|) (si mad_j = 0, z = 0 pour ce flux) ;
  z_ij = (x_ij − med_j)/(1,4826·mad_j) ; e_i = moyenne sur j de
  |z_ij|.
- Extrémité de fenêtre : pour une config de w, E_k = moyenne de e_i
  sur les lignes k..k+w−1, k = 0..n−w.
- Petit côté à un candidat c : split(c) fenêtres basses contre
  n_windows − split(c) hautes ; le petit côté est le groupe le plus
  petit en fenêtres ; ses lignes distinctes sont 0..split+w−2
  (côté bas) ou split..n−1 (côté haut).
- G(c) = moyenne de e_i sur les lignes distinctes du petit côté
  (extrémité non signée, sans cohérence de signe entre flux).
- H(c) = moyenne sur j de |moyenne de z_ij sur les lignes
  distinctes du petit côté| (écart cohérent — voisin du numérateur
  du |d| du scan ; sa valeur prédictive hors échantillon mesure si
  le déclencheur est localisable à un petit groupe, elle n'est PAS
  une preuve indépendante du scan, et elle est rapportée comme
  telle).
- Candidats de bord : min(split, n_windows − split) ≤ 0,20 ×
  n_windows.
- Bloc déclencheur candidat B d'une courbe rob-on : à son seuil de
  pic thr (stocké), split = #{fenêtres : win_progress < thr} ;
  fenêtres frontières split−1 et split ; B = lignes
  [split−1, split+w−1] (w+1 lignes consécutives). Assertions :
  0 ≤ split−1 et split+w−1 ≤ n−1, sinon courbe exclue et consignée.
- Seuil de prédiction T_H par config C (ICGC, n=70) : calculé sur le
  corpus EXISTANT (35 runs ICGC de l'extract §8.63), APRÈS le gel
  de ce protocole mais AVANT toute lecture des résultats frais, et
  consigné horodaté dans le fichier de prédictions :
  T_H(C) = (max{H_max sur les courbes à C avec rob < 0,05} +
  min{H_max sur les courbes à C avec rob > 0,5})/2, où
  H_max = max sur les candidats de bord de H(c). Si l'un des deux
  ensembles est vide, la config C est exclue du test P2 (consigné).

## 3. Hypothèses nommées d'avance

- **H1 (principale — bloc extrême au bord).** Le pic étroit est
  déclenché par un bloc de w+1 lignes consécutives aux valeurs
  extrêmes sur plusieurs flux, isolé comme petit groupe par un
  seuil proche d'un bord. Prédictions : (a) déplacer le bloc tue
  le pic à l'ancienne position ; (b) winsoriser le bloc tue le pic ;
  (c) transplanter des valeurs de bloc déclencheur au bord d'un
  contrôle crée un pic ; (d) le pic prédit par G(c) tombe sur le
  vrai pic à ±2 candidats.
- **H2 (une seule ligne).** Le pic est porté par UNE seule ligne
  extrême du bloc, pas par le bloc entier. Test : A2 (winsoriser
  la seule ligne la plus extrême du bloc) contre A1 (tout le bloc).
- **H3 (queues globales).** Les CSV rob-on ont des queues plus
  lourdes (max e_i, kurtosis) que les rob-off, indépendamment de
  la position des lignes extrêmes. Test : Mann-Whitney + AUC de
  E_max et de max e_i entre gagnantes rob-on (11) et gagnantes
  rob-off (rob < 0,05) du corpus ; si A tue le pic, H3 seule est
  écartée comme explication (une queue globale ne se déplace pas
  avec un bloc).
- **H4/H5 (bord seul — levier du petit groupe).** Un seuil proche
  du bord suffit, même sans bloc extrême. Test : B0 (bloc
  d'extrémité médiane déplacé au bord) — aucun pic attendu.
- **H0 (fluctuation d'ordre / comparaisons multiples).** Aucun
  bloc, aucune propriété de ligne ne déclenche le pic : c'est le
  max sur ~12 configs × ~30–90 candidats de courbes bruitées.
  H0 est ce qui reste si A échoue (déplacer/winsoriser ne tue pas
  le pic) et si B échoue : le pic persiste ou se déplace
  aléatoirement, sans suivre le bloc.

## 4. Méthodes — dans l'ordre, sans retour en arrière

### A. Calibration de la réplique (fonctions DU PIPELINE, importées)

Même pattern que §8.63 (étape B) : `_build_mc_progress_axis` +
`scan_critical_threshold` + `evaluate_scan_quality`, importées sans
modification. Calibration : reproduire à |Δ| ≤ 10⁻⁶ (métriques et
courbes) (i) les 5 entrées §8.63 × 12 configs (MTAP réel, s11111,
s123, ICGC réel, ICGC nul s29) et (ii) les 11 courbes rob-on + 6
contrôles à leur config gagnante (métriques + courbe, contre les
`all_results` stockés). Si la calibration échoue sur une courbe,
la courbe est exclue des interventions et consignée ; si elle
échoue sur une entrée (i), la réplique est rejetée et les volets
qui en dépendent sont consignés « non élucidables par cette voie ».

### B. Statistiques de corpus (lecture des CSV existants, aucun run)

Pour chaque run des 82 (14 MTAP + 68 immunitaires) à sa config
gagnante, et pour chaque courbe des 35 runs ICGC à chacune des 12
configs : e_i, E_k, G(c), H(c) sur les candidats de bord, H_max,
E_max, max e_i, kurtosis moyenne des flux. Mann-Whitney (rob-on
gagnantes 11 contre gagnantes rob-off rob<0,05) + AUC pour E_max,
H_max, max e_i. Position (descriptif, en échantillon) : sur les
11 courbes rob-on, fraction dont le pic réel est à ±2 candidats
du argmax_c G(c) sur les candidats de bord.

### C. Interventions sur les 11 courbes rob-on (réplique, pas de run v6.2)

Toutes à la config gagnante de la courbe, sur le CSV d'origine
(flux seuls modifiés, colonne de contrôle inchangée, n et ordre
des autres lignes inchangés sauf mention).
- **A — déplacement (swap).** Bloc B ↔ bloc médian M = lignes
  [m, m+w], m = n//2 − w//2 (w+1 lignes ; si M chevauche B,
  décaler m de w+1 vers le bord opposé, consigné). Les lignes de
  B vont à la position m, celles de M à la position de B.
  Succès : score de la nouvelle courbe au vieux seuil thr
  < 0,5 × maxsep ancien ET aucun candidat à ±2 pas du vieux thr
  n'a un score > 0,5 × maxsep ancien.
- **A1 — winsorisation du bloc (échelle).** Remplacer chaque
  valeur de flux des lignes du bloc par la médiane du flux sur le
  CSV d'origine. Échelle : (a) 2 fenêtres frontières (lignes
  [split−1, split+w−1]) ; (b) 4 fenêtres (split−2..split+1) ;
  (c) 8 fenêtres (split−4..split+3). Succès par échelon :
  rob de la nouvelle courbe < 0,1. On rapporte le plus petit
  échelon tuant le pic, par courbe.
- **A2 — winsorisation d'une seule ligne.** Remplacer la seule
  ligne argmax e_i dans B par les médianes des flux. Succès :
  rob de la nouvelle courbe < 0,1.
- Les CSV modifiés sont écrits sous `pic873_interv_<run>_<variante>.csv`
  (SHA consignés), jamais en place.

### D. Interventions sur les 6 contrôles (réplique)

À la config gagnante du contrôle.
- **B1 — transplantation du propre bloc extrême au bord.**
  k* = argmax_k E_k ; bloc Bc = lignes [k*, k*+w] ; retirer Bc
  et l'insérer en position 0 (lignes 0..w), les autres lignes
  gardant leur ordre relatif. Succès : rob de la nouvelle courbe
  > 0,5 ET pic à ±2 pas du candidat prédit (candidat de la grille
  le plus proche de win_progress[1]).
- **B0 — contrôle négatif (bloc médian au bord).** Même
  construction avec k_med = argmin_k |E_k − médiane(E)|, sur les
  2 contrôles GSE62452 s11 et TCGA s13. Succès de H5 (bord seul) :
  rob > 0,5. Attendu sous H1 : 0/2.
- **B2 — transplantation de valeurs donneuses.** Donneurs gelés :
  MTAP s11111 (bloc B à (28, 27, 6), L=28 lignes) → contrôle MTAP
  s1011 ; ICGC s37 (bloc B à (22, 16, 7), L=17 lignes) →
  contrôles ICGC s31 et s33. Écraser les lignes 0..L−1 du
  contrôle (flux seuls) par les valeurs du bloc donneur, dans
  l'ordre. Succès : rob de la nouvelle courbe > 0,5 ET pic à ±2
  pas du candidat prédit (même définition que B1).

### E. Lot frais hors échantillon — prédiction AVANT lecture (20 runs v6.2)

- **Construction** (`build_nulls_icgc_873.py`, neuf) : 20 nuls
  ICGC frais, même méthode que `build_nulls_icgc_863.py`
  (`default_rng(graine)`, `permutation(n)`, lignes entières,
  colonne step inchangée), graines 41–60 — jamais utilisées
  (§8.47 : 1–3, 42 ; §8.53 : 11–30 ; §8.63 : 31–40). Entrée
  vérifiée par SHA avant construction : `pdac_immune_icgc_fluxes.csv`
  `10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc`.
  Sorties : `pdac_immune_icgc_fluxes_nul_s<graine>.csv` (+ SHA-256
  dans `nulls_icgc_873_files.json`).
- **Prédictions** (`pic_etroit_873_predictions.json`, écrit AVANT
  la fin du lot et AVANT toute lecture des résultats frais) :
  pour chaque CSV frais et chacune des 12 configs ICGC (n=70,
  ensemble fixe relu §8.63), G(c), H(c) sur les candidats de
  bord, H_max, E_max, candidat prédit ĉ = argmax_c G(c), et
  prédiction rob-on (H_max ≥ T_H(C), T_H calibré au §2 sur le
  corpus existant). SHA du fichier consigné dans la section.
- **Runs** : v6.2 mode fast, 20 runs, sorties
  `results_fast_v62_873_icgc_nul_s<graine>/`, lanceur reprenable
  `run_v62_873.sh`, surveillance `watch_v62_873.sh`, manifeste
  `manifest_v62_873.txt`, `systemd-run` (jamais nohup), journal
  `runs_v62_873.log` (SHA v6.2 avant/après, exits). Exit 0 exigé
  pour les 20 runs ; un run interrompu (redémarrage machine) est
  relancé tel quel après suppression de son dossier partiel (sans
  `master_results.json`) ; jamais remplacé par une autre graine.
  Le lot §8.72 tourne en parallèle au lancement : les deux lots
  sont indépendants (manifestes et préfixes distincts) et chacun
  est reprenable.
- **Lecture** : réplique exacte (calibrée §4 A) des 20×12 courbes
  + lecture des `master_results.json` frais ; comparaison aux
  prédictions (P1, P2, §5). Aucun autre run v6.2 nouveau.

### F. Ce qui n'est PAS fait

- Aucune modification du pipeline, aucun nouveau seuil, aucune
  sélection d'indicateur après coup, aucune imputation, aucune
  valeur inventée, aucun nouveau nul construit après lecture des
  résultats (les graines 41–60 sont gelées ici avant tout run).
- Aucune conclusion importée d'autres bras (rotations, tests A/C,
  PARP, §8.54–§8.72) : seules les données et runs de ce chantier
  font verdict, sauf citation explicite « relu §8.63 » pour les
  faits de départ.
- Aucun test direct nouveau (PRMT5, prolifération, survie).
- Le plancher 0,07 (§8.46/§8.50) et les planchers p95 (§8.53) ne
  sont ni re-testés ni redéfinis ici.

## 5. Règles de décision — écrites avant

**Calibration.** Si (i) ou (ii) du §4 A échoue, les volets
dépendants sont « non élucidables par cette voie » et le verdict
global est NON ÉLUCIDÉ (avec ce qui a été tenté).

**DÉCLENCHEUR IDENTIFIÉ (H1)** si TOUTES : (i) calibration OK ;
(ii) A-swap : succès sur ≥ 9/11 courbes rob-on ; (iii) A1 :
succès (rob < 0,1) sur ≥ 9/11 courbes à l'échelon (a) ou (b) ;
(iv) B2 : succès sur ≥ 2/3 contrôles ; (v) B0 : 0/2.
Le déclencheur est alors nommé avec sa taille mesurée (plus petit
échelon A1 tuant le pic, médiane sur les courbes) et sa règle de
position (bloc isolé comme petit groupe à un candidat de bord).
Précision H2 : si A2 tue le pic (rob < 0,1) sur ≥ 9/11, le
déclencheur est « une seule ligne » ; si A2 ≤ 3/11 alors que A1
≥ 9/11, c'est « un bloc de ~w lignes, pas une ligne ».

**PARTIELLEMENT IDENTIFIÉ** si (ii) et (iii) tiennent (≥ 9/11)
mais (iv) échoue (< 2/3) ou (v) échoue (≥ 1/2) : nécessité
établie (le bloc porte le pic), suffisance non établie (ou bord
seul partiellement suffisant).

**NON ÉLUCIDÉ** si (ii) < 9/11 ou (iii) < 9/11 à tous les
échelons : H1 rejetée ; consigner ce qui est éliminé (H1, et H2
selon A2, H3 selon §4 B, H5 selon B0) ; H0 reste l'explication
de repli, nommée comme telle.

**Confirmation hors échantillon P1/P2 (qualification, pas
condition du verdict primaire sauf mention).**
- P1 (position) : parmi les courbes fraîches rob-on (rob > 0,5),
  fraction dont |seuil réel − ĉ| ≤ 2 pas de candidat. Succès si
  ≥ 70 % ET au moins 5 courbes rob-on fraîches ; sinon P1 est
  descriptive seulement (consigné).
- P2 (magnitude) : AUC de H_max (score) contre rob > 0,5 (label)
  sur les courbes fraîches (configs à T_H défini ; les autres
  exclues et comptées). Succès si AUC ≥ 0,80 (descriptif si
  < 5 courbes rob-on fraîches).
- Si P1/P2 échouent alors que le verdict primaire est IDENTIFIÉ,
  le verdict reste IDENTIFIÉ avec la qualification explicite
  « généralisation non confirmée sur 20 nuls frais » ; si P1/P2
  confirment, la généralisation est consignée comme confirmée.

**H3 (descriptif).** Mann-Whitney + AUC (§4 B) rapportés tels
quels ; AUC < 0,7 sur E_max et H_max écarte H3 comme explication
à elle seule.

## 6. Sorties

- Ce protocole `PROTOCOL_pic_etroit_873.md` (SHA noté dans la
  section).
- Scripts neufs : `build_nulls_icgc_873.py`, `run_v62_873.sh`,
  `watch_v62_873.sh`, `pic_etroit_873.py` (calibration, corpus,
  interventions, lecture des frais), `predict_pic_etroit_873.py`
  (prédictions hors échantillon, avant lecture des frais).
  (SHA notés dans la section.)
- Données/résultats : `nulls_icgc_873_files.json` (SHA des 20
  nuls frais), `pic_etroit_873_predictions.json` (prédictions +
  T_H par config, SHA noté), `pic_etroit_873_extract.json`,
  `pic_etroit_873_results.csv`, `pic_etroit_873_interv.csv`
  (toutes les interventions), `pic_etroit_873_interv_*.csv`
  (CSV modifiés, SHA consignés), `manifest_v62_873.txt`,
  `runs_v62_873.log` (20/20, exit 0), dossiers
  `results_fast_v62_873_icgc_nul_s<graine>/`.
- Section `section_8.73_pic_etroit.md` (verdict d'abord, chiffres,
  méthode, limites, provenance — format des sections précédentes).

## 7. Limites connues d'avance

- Mode fast seulement : 12 configs par run. Les nombres (taux,
  échelons) sont propres au mode fast.
- La réplique est exacte à 10⁻⁶ ou rejetée — mais elle ne couvre
  que le scan ; Delta n'est pas touché ici (déjà expliqué §8.63,
  propriété de w).
- H(c) est voisin du numérateur du |d| du scan : P2 mesure la
  localisabilité du déclencheur, pas une indépendance vis-à-vis
  du scan. Le poids causal repose sur A/B (interventions), pas
  sur P2.
- 20 nuls frais donnent ~2–3 gagnantes rob-on attendues
  (taux ~13 % sur le corpus) et ~9 courbes rob-on attendues
  (~3,6 % des 240 courbes) : P1/P2 peuvent manquer de puissance
  et rester descriptives — c'est prévu au §5, pas un échec.
- Le lot §8.72 tourne en parallèle : les deux lots se partagent
  le CPU (2 vCPU, 1,5 partagé) et durent plus longtemps ; chaque
  lot est reprenable et indépendant.
- Un mécanisme fermé comme non élucidé est un résultat, pas un
  échec : il est consigné comme tel, avec ce qui a été tenté.
