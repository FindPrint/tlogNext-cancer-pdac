# PROTOCOLE GELÉ — §8.46 : Arbitrage de la contradiction MTAP (S_sep contre MC/Delta) (19 novembre 2026)

Go : parent orchestrator, 19 nov. 2026 (chantier 1/4). Ce protocole est gelé
AVANT tout nouveau calcul, toute nouvelle construction et tout nouveau run
de ce chantier. Aucun paramètre ne change après les résultats. Livre blanc
NON édité directement (section dans un fichier séparé
`section_8.46_mtap_arbitration.md`). PDF NON régénéré. Rien poussé sur
GitHub. Pipeline v6.2 JAMAIS modifié (SHA attendu
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`).

## 0. Question

Sur la série TCGA v4 ordonnée par CN MTAP (177 tumeurs, contrôle MTAPCN,
§8.36), le pipeline v6.2 donne S_sep = +0,1968 (réel > nul) alors que
MC = −0,1642 et Delta = −0,5416 sont inversés (réel < nul), valeurs
revérifiées au §8.38 (S_sep v6.2 = v6.1 exactement). Question : S_sep
voit-il quelque chose de réel que MC et Delta ratent, ou est-ce un
artefact de construction de S_sep ?

Faits d'entrée (attendus de reproduction, jamais des verdicts réimportés) :
- MTAP réel v6.2 : cascade 0,54 / 60,74 / 72,77 / 92,11 / 92,11 % ;
  MC 0,3511 (seuil 69,57 %) ; max_separation 0,3392 ; stabilité 0,9959 ;
  S_sep 0,3378 ; Delta 3,8051 ; L7a DOWN 0,427 ; falsification 0,733.
- MTAP nul v6.2 (graine 42) : cascade 1,07 / 2,14 / 8,57 / 15,58 / 15,58 % ;
  MC 0,5153 (seuil 84,44 %) ; max_separation 0,1434 ; stabilité 0,9825 ;
  S_sep 0,1409 ; Delta 4,3466 ; L7a UP 0,331 ; falsification 0,816.
- Effet PRMT5 suit MTAP, pas CDKN2A (§8.40 : pancréas −1,385 contre
  −1,010, p = 0,0036 ; effet CDKN2A disparaît quand MTAP est fixé, p = 0,76).

## 1. Mécanique connue AVANT les calculs (lue dans le code v6.2, pas devinée)

Formules gelées (PROTOCOL_v6.2.md §3 ; code `universal_v6.2.0_cohen.py`) :
- `S_sep = max_separation × stability`, lus dans `best_config.metrics`.
- `max_separation` = MAX, sur les seuils candidats du scan, de la moyenne
  sur les flux du |d de Cohen| entre groupes pré- et post-seuil
  (`evaluate_scan_quality`, lignes 3314–3390). C'est une hauteur de pic :
  un maximum sur les seuils, sans pénalité de largeur.
- `stability` = 1 / (1 + écart-type des scores locaux autour du pic)
  (fenêtre ± max(3, n_scores/20)). Quasi saturée ici (0,98–1,00) :
  S_sep ≈ max_separation.
- MC `best_score` = score COMPOSITE (lignes 3460–3484, poids par défaut
  lignes 3727–3730) : 0,3·s_norm + 0,3·stabilité + 0,2·robustesse +
  0,2·acuité, où s_norm = tanh(max_separation/2),
  robustesse = exp(−((FWHM − 10)²)/(2·5²)) avec FWHM = largeur en % de
  la plage des candidats où le score ≥ moitié du max (idéal 10 %),
  acuité = tanh(max |dS/dx| local / 0,5). MC récompense donc la FORME
  du pic (étroit, ~10 %, net), pas seulement sa hauteur.
- Delta = d_div − d_sat (`compute_holographic_tension_state`, ligne
  ~8022), où d_* sont des médianes T_log = (d − 4)·log(n) sur les
  seuls estimateurs de dimension. Delta est une largeur spectrale
  GLOBALE de la matrice de flux entière : il ne dépend d'aucun seuil
  et ne mesure pas une rupture localisée.
- Rappel §8.42 : les magnitudes des estimateurs portent l'échelle de n
  (log(n) meilleur trait unique) ; Delta NON élucidé (hold-out 68,9 %).

Conséquence pré-enregistrée : MC, S_sep et Delta ne mesurent PAS la même
chose. Un désaccord entre eux n'est pas en soi une contradiction
biologique : il peut être une différence de construction. L'arbitrage
consiste à identifier QUELLE quantité chaque indicateur mesure sur
cette série, et si la quantité vue par S_sep est réelle.

## 2. Hypothèses testées (toutes falsifiables, aucune privilégiée)

- H1 (forme contre hauteur) : l'inversion MC vient de la robustesse
  (FWHM) : le pic réel est HAUT mais LARGE (plateau), le pic du nul est
  BAS mais ÉTROIT (≈10 %). Alors MC pénalise le réel par construction,
  et S_sep ne voit pas une rupture mais une marche large.
- H2 (marche de groupe, pas rupture) : la séparation réelle est une
  différence de NIVEAU entre tumeurs MTAP-délétées et intactes (deux
  groupes), pas un saut localisé à un seuil. Test : d de Cohen par flux
  entre groupes GISTIC (−2/−1 contre 0/+) ; si la séparation max est
  portée par un écart de niveau stable sur tout l'axe, le pic est large
  par nature.
- H3 (un ou deux flux portent tout) : le max_separation réel est porté
  par 1–2 flux seulement (dont un sans support direct), alors que le
  nul répartit sa séparation. Test : décomposition par flux du |d| au
  seuil du max (lecture du scan, recalcul direct depuis les CSV).
- H4 (Delta global) : l'inversion Delta vient de ses ancres
  (d_div et/ou d_sat), pas d'une rupture : le nul permuté élargit le
  spectre de dimension. Test : D-vector réel contre nul, estimateur
  par estimateur (df_feat / csd_fractal_estimators).
- H5 (variabilité du nul) : l'écart S_sep +0,1968 tient à LA permutation
  graine 42. Test : deux nuls frais (graines 7 et 123), même méthode
  (lignes permutées ensemble, contrôle intact), runs v6.2 fast.
- H6 (confondant prolifération) : l'effet PRMT5–MTAP, et/ou les écarts
  de flux le long de l'axe MTAP, sont portés par la prolifération.
  Test : Spearman partiel PRMT5 ~ CN MTAP en contrôlant la prolifération
  (lignées DepMap : proxy défini au §4 ; tumeurs TCGA : score §8.25c).

## 3. Méthodes — dans l'ordre, sans retour en arrière

### A. Relecture vérifiée des deux runs v6.2 existants (aucun nouveau run)
Relire `results_fast_v62_mtap/master_results.json` et
`results_fast_v62_mtap_nul/master_results.json` avec un extracteur neuf
(`mtap_arbitration_846.py`) : cascade, best_config complet (score,
seuil, max_separation, s_norm, stabilité, robustesse, acuité), Delta et
D-vector, L7a, falsification. RECALCULER le MC composite à la main
depuis ses 4 composantes et comparer au score lu (écart toléré 10⁻⁶) :
c'est le test direct de H1 — identifier la composante qui porte
l'inversion (−0,1642).

### B. Forme du scan (H1/H2) — lecture des scan_curve.json existants
Pour réel et nul : courbe score(seuil) complète ; position du max ;
FWHM recalculée depuis la courbe (largeur où score ≥ max/2, en % de la
plage des candidats) et comparée à la robustesse lue ; nombre et part
des candidats au-dessus de la moitié du max ; score au seuil MC contre
score au seuil du max. Si FWHM réel > 50 % et FWHM nul ≈ 10 %,
H1 est confirmée mécaniquement.

### C. Loupe par loupe (H2/H3) — recalcul direct depuis les CSV (harnais)
Sur `pdac_tcga_fluxes_v4_mtap.csv` et son nul (SHA §0 / PROVENANCE) :
- (C1) d de Cohen par flux, pré/post, au seuil MC et au seuil du max
  (pas des deux runs), réel contre nul ; part de chaque flux dans la
  moyenne qui définit max_separation ; nombre de flux qui portent 80 %
  de la séparation.
- (C2) d de Cohen par flux entre groupes GISTIC : délétées profondes
  (−2, n=12) et délétées (−2/−1) contre intactes (0/+), avec les mêmes
  d sur le nul (mêmes groupes, flux permutés) comme référence interne.
- (C3) Spearman flux contre rang MTAP, réel contre nul (déjà au §8.36
  pour le top-12 ; refait ici flux par flux avec p, mêmes définitions).
Aucun seuil choisi après coup : les seuils lus sont ceux du pipeline
(MC et max), jamais optimisés dans ce script.

### D. Décomposition de Delta (H4)
D-vector (d_sat, d_crit, d_div, d_null) réel contre nul, lus dans les
`holographic_tension_state` des deux JSON ; puis médianes par estimateur
de dimension (`csd_fractal_estimators.csv` / `df_feat.csv` des deux
dossiers) : quel(s) estimateur(s) porte(nt) l'écart Delta −0,5416.
Rappel : Delta ne dépend d'aucun seuil ; une inversion Delta ne dit
rien, à elle seule, sur l'existence d'une rupture.

### E. Deux nuls frais (H5) — seuls nouveaux runs du chantier
Construire `pdac_tcga_fluxes_v4_mtap_nul_s7.csv` et
`..._nul_s123.csv` par la MÊME méthode que le nul graine 42
(`build_fluxes_tcga_v4_mtap.py` lignes 167–169 : `rng(seed).permutation`,
lignes permutées ensemble, colonne MTAPCN intacte), graines 7 et 123,
script neuf `build_mtap_nuls_846.py`. Lancer 2 runs v6.2 fast via le
lanceur reprenable `run_v62_lot.sh` (manifeste
`manifest_v62_mtap_nuls846.txt`), `systemd-run` (jamais nohup), exit 0
exigés. Lire S_sep, max_separation, MC, Delta, cascade des deux nuls
frais avec le même extracteur. Aucun autre run.

### F. Tests directs PRMT5 contre MTAP, avec et sans prolifération (H6)
Sources déjà détenues, SHA revérifiés avant calcul (DepMap 24Q4) :
`data/CRISPRGeneEffect.csv` `3d8f3ec6…167e3b`,
`data/OmicsCNGene.csv` `4851d3e9…134c`,
`data/Model.csv` `b7a0c138…dcfa`.
- (F1) Reproduction §8.40 : 47 lignées pancréas (OncotreeLineage
  Pancreas, jointure GeneEffect), CN MTAP linéaire, délétion profonde
  CN < 0,5 : médianes PRMT5, Mann-Whitney bilatéral, Spearman continu.
  Attendu : −1,385 / −1,010, p = 0,0036 ; rho +0,497.
- (F2) Prolifération, lignées : proxy gelé = médiane des Chronos
  MKI67, TOP2A, PCNA, CCNB1 par lignée (mêmes 4 gènes que le score
  TCGA §8.25c, mais en dépendance CRISPR, pas en expression — la
  différence est nommée, le proxy est une hypothèse de travail, pas
  une mesure de vitesse de division). Spearman partiel PRMT5 ~ CN MTAP
  en contrôlant ce proxy (résidus de régression sur les rangs), n, rho,
  p. Sensibilité : même calcul en contrôlant Chronos KRAS seul.
- (F3) Prolifération, tumeurs TCGA : score de prolifération §8.25c
  (médiane des résidus MKI67/TOP2A/PCNA/CCNB1, 1re colonne de
  `pdac_tcga_fluxes_v4_prolif.csv`, ordre prolifération) relu dans
  l'ordre MTAP : Spearman score-prolif contre CN MTAP ; d de Cohen du
  score entre top-12 MTAP-délétées et reste ; corrélations partielles
  flux ~ MTAP (Spearman partiel sur les rangs, contrôle prolif) pour
  les 12 flux, réel contre nul.
- (F4) Relecture des 4 confirmations « PRMT5 suit MTAP, pas CDKN2A » :
  §8.28 (prmt5_mtap_results.csv, ligne pancréas profond),
  §8.29 (stratification CN pan-cancer, p = 0,26),
  §8.36 (stratification mutation pancréas, p = 0,76),
  §8.40 (stratifications CN pancréas p = 0,46 et pan-cancer p = 0,257).
  Chaque valeur est RELUE dans son fichier source, pas recopiée de la
  section ; tout écart est consigné. Les résultats antérieurs servent
  d'attendus, jamais de verdicts réimportés.

### G. Ce qui n'est PAS fait
- Aucune modification du pipeline, aucun nouveau seuil, aucune sélection
  d'indicateur après coup, aucune imputation, aucune valeur inventée.
- Aucun run sur une série « PRMT5 comme flux » ou autre série neuve :
  hors périmètre (déjà fait au §8.43, NON).
- Aucune conclusion importée d'autres bras (rotations, test A/C,
  immunitaire, PARP) : seules les données et runs du jour font verdict.

## 4. Règles de décision — écrites avant (critère d'arbitrage)

Trois issues possibles, une seule retenue à la fin :

- **ARBITRÉ — S_sep VOIT DU RÉEL (et MC/Delta ratent une marche).**
  Il faut les TROIS : (1) les deux nuls frais restent sous le S_sep réel
  de plus de 0,07 (écart réel − nul frais > 0,07 dans les deux cas) ;
  (2) la décomposition par flux montre ≥ 2 flux portant la séparation
  réelle avec un support direct (d de groupe GISTIC et/ou Spearman
  dans le même sens, au-dessus du nul) ; (3) le mécanisme est nommé :
  MC pénalise la FORME (robustesse) et Delta mesure une largeur
  spectrale globale — ni l'un ni l'autre ne nie la hauteur vue par
  S_sep. Alors le verdict §8.36 est précisé, pas renversé : pas de
  rupture localisée, mais une marche de niveau réelle.
- **ARBITRÉ — ARTEFACT DE CONSTRUCTION DE S_sep.**
  Il suffit d'UNE des deux : (1) au moins un nul frais atteint ou
  dépasse le S_sep réel (écart réel − nul frais ≤ 0,07, ou nul frais
  > réel) ; (2) la séparation réelle est portée par UN seul flux sans
  support direct, ou par un plateau sans seuil localisable (FWHM > 50 %
  ET aucun flux avec d de groupe GISTIC au-dessus du nul). Alors
  S_sep ne voit rien que le nul ne voie aussi, et le verdict §8.36
  (NON) est confirmé.
- **ARBITRÉ — DÉSACCORD APPARENT, LES DEUX ONT RAISON SUR DES OBJETS
  DIFFÉRENTS.** Si (H1) est confirmée mécaniquement (inversion MC
  portée par la robustesse seule, s_norm faveur réelle) ET (H4) est
  confirmée (Delta = largeur globale, sans rapport avec un seuil),
  mais que ni la condition (1) ni la condition (2) ci-dessus n'est
  remplie nettement : alors S_sep mesure la hauteur d'une marche de
  niveau, MC mesure l'absence de pic étroit, Delta mesure une largeur
  spectrale — les trois sont exacts, ils ne se contredisent pas, et
  aucun ne prouve une rupture. Le verdict §8.36 (pas de rupture,
  pas de séparation réel/nul au sens du pipeline) est maintenu, avec
  le mécanisme expliqué.
- **NON ARBITRÉ (honnête).** Si les tests se contredisent sans
  mécanisme identifié (par exemple nuls frais partagés, un pour
  chaque camp, sans explication), le dire tel quel : la contradiction
  reste ouverte, comme au §8.40.

Dans tous les cas : le verdict §8.36 (la chaîne KRAS ne réapparaît pas
sous l'ordre MTAP) n'est pas touché par ce chantier — il porte sur la
chaîne, pas sur S_sep. Et l'effet PRMT5–MTAP (§8.40) n'est ni confirmé
ni infirmé ici au-delà de sa reproduction (F1/F4) : il vit dans les
lignées, pas dans la série ordonnée.

## 5. Sorties

- Script neuf `mtap_arbitration_846.py` (relecture + décompositions
  A–D + tests directs F ; SHA noté dans la section).
- Script neuf `build_mtap_nuls_846.py` (nuls graines 7 et 123 ; SHA noté).
- `mtap_arbitration_846_results.csv` (tous les nombres cités),
  `mtap_arbitration_846_extract.json` (relecture brute des JSON),
  `mtap_arbitration_846_prolif.csv` (tests F2/F3).
- CSV nuls frais + SHA ; manifeste `manifest_v62_mtap_nuls846.txt` ;
  journal `runs_v62_mtap_nuls846.log` (exit codes, systemd-run).
- Section `section_8.46_mtap_arbitration.md` (verdict d'abord, chiffres,
  méthode, limites, provenance — format des sections précédentes).
- Provenance complète dans la section : sources, SHA, nature des lignes,
  ce qui manque.

## 6. Limites connues d'avance

- n = 177 tumeurs, 12 flux d'expression ; le nul est une permutation
  conjointe (mêmes marginales, ordre brisé) — il ne teste que l'ordre,
  pas la structure marginale.
- Le proxy prolifération lignées (F2, Chronos MKI67/TOP2A/PCNA/CCNB1)
  n'est pas une vitesse de division mesurée : c'est une dépendance
  génétique, interprétée comme proxy, avec sa limite nommée.
- Deux nuls frais seulement : c'est un test de variabilité, pas une
  distribution nulle complète (un nul = une permutation ; 3 nuls au
  total après ce chantier).
- Delta n'est pas élucidé (§8.42) : sa décomposition (D) décrit où
  bouge la largeur spectrale, elle n'explique pas pourquoi la
  permutation l'élargit.
- FWHM et robustesse sont lues dans le code v6.2 : la lecture de la
  forme du scan dépend de la définition gelée du pipeline (idéal 10 %,
  sigma 5 %) — un idéal arbitraire, pas une loi physique.
