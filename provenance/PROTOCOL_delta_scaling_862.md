# PROTOCOLE GELÉ — §8.62 : loi d'échelle en n pour Delta

Date : 20 novembre 2026.
Statut : **PROTOCOLE GELÉ AVANT TOUTE MODÉLISATION ET AVANT TOUT RUN.**
Aucune analyse lancée avant l'écriture de ce fichier. Toute déviation arrête
le travail et se consigne, elle ne se corrige pas en silence.
Auteur : TagPrint.
Dossier : `~/workspace/runs/pdac-v6/`.
Demande : chantier §8.62 du projet PDAC v6.2 (20 nov. 2026), voie ouverte au
§8.42.9 point 2 et rappelée au §8.57.9 point 1 (« la loi d'échelle en n,
analytiquement »).

## 0. Verdict d'abord — ce qui est gelé ici

Le §8.42.5 a établi que `log(n)` est le meilleur trait unique pour 12
cibles sur 13 (BoxCounting r=+0,932, Petrosian −0,949, Katz −0,922,
LevinaBickel +0,868, MFA +0,847, LocalPCA +0,824) et que « les magnitudes
portent l'échelle de n, pas le contenu des flux ». Le §8.57 a confirmé que
les magnitudes sont presque recalculées par la moitié de leur propre
construction, sans que Delta soit élucidé (89,2 % / 90,5 % en LOCO, sous
le critère). Ce protocole teste deux questions distinctes, à ne pas
confondre :

- **(Q1) Existe-t-il une loi d'échelle explicite en n** — une forme
  fonctionnelle f(n), la même pour chaque cible, qui prédit les magnitudes
  (13 médianes, d_div, d_sat, Delta) ?
- **(Q2) Cette loi suffit-elle à expliquer pourquoi Delta ne sépare pas
  le réel du nul ?** Une loi en n pur ne peut prédire qu'une seule valeur
  de Delta par n ; or le réel et son nul partagent le même n. La réponse à
  Q2 exige donc de mesurer ce qui reste quand on retire f(n) — le résidu —
  et de vérifier si ce résidu sépare, ou si réel et nul suivent la même
  courbe en n.

## 1. Ce qui est acquis (rappels chiffrés, §8.42 et §8.57)

- Ensemble gelé identique aux §8.39/§8.42/§8.57 : 222 runs (156 v6.1 +
  66 v6.2), 156 matrices distinctes, 9 cohortes.
- Identités de construction vérifiées 222/222 (0 écart) : d_div = moyenne
  des 3e et 4e médianes divergence triées (k=6) ; d_sat = 4e médiane
  saturation triée ; Delta = d_div − d_sat.
- Delta sur les 222 runs (inventaire) : moyenne 3,15, écart-type 1,10,
  étendue 1,26–4,62. d_div : moyenne 4,67, écart-type 1,18. d_sat :
  moyenne 1,52, écart-type 0,12 seulement — la variance de Delta est
  portée par d_div, pas par d_sat.
- n sur les 222 runs (inventaire) : 11 valeurs distinctes — 45 (30 runs),
  52 (4), 63 (4), 69 (14), 70 (10), 145 (20), 177 (2), 178 (124), 285 (4),
  515 (4), 1000 (6). Par cohorte (inventaire, 156 matrices) : hp35 n=1000,
  coad n=285, cptac n=52/63, depmap n=45, geo62452 n=69, geo71729 n=145,
  icgc n=70, luad n=515, tcga n=177/178. **n est donc (quasi) constant
  dans chaque cohorte** : dans l'ensemble A, « effet n » et « effet
  cohorte » sont presque parfaitement confondus. C'est la limite centrale
  de l'ensemble A, et la raison d'être de l'ensemble B (même matrice,
  n qui varie).
- DFA extrême : 22 runs avec |DFA| > 10 (min −38,16, max 1,73) — DFA est
  un membre de saturation, rarement la 4e valeur triée ; une sensibilité
  sans ces 22 runs est gelée (§5.4).
- Un run v6.2 fast dure ~1 min (lot §8.53 : 45 runs, 45/45 exit 0 ;
  premier run plus lent, compilation numba). Budget de ce chantier :
  31 runs.

## 2. Données

### 2.1 Ensemble A — descriptif, aucun run nouveau (222 runs détenus)

- Cibles : les 13 médianes par estimateur (6 divergence + 7 saturation),
  parsées depuis les colonnes `div_sorted` / `sat_sorted` de
  `v62_delta_levels.csv` (arrondies à 4 décimales, erreur ≤ 0,00005,
  négligeable devant ±0,10), plus `d_div`, `d_sat`, `delta` du CSV.
  Vérification préalable dans le script : d_div et d_sat recalculés
  depuis les médianes parsées = valeurs du CSV à 10⁻³ près sur 222/222 ;
  sinon arrêt et diagnostic.
- n : colonne `n` du CSV, vérifiée égale au nombre de lignes de la
  matrice d'entrée (0 écart attendu, comme aux §8.42/§8.57).
- Paires réel/nul : appariement par nom de dossier (le nul est le dossier
  `_nul` correspondant, même version) — 106 dossiers `_nul` dans les 222.

### 2.2 Ensemble B — causal, nouveaux runs v6.2 fast sur sous-échantillons

- Matrices sources (toutes à contrôle `step`, SHA-256 notés par le
  script avant troncature) :
  - HP35 réel : `/home/hatch/workspace/runs/biophysique-hp35/test_biophysique_input.csv`
    (n=1000, p=7 flux) ; HP35 nul :
    `/home/hatch/workspace/runs/biophysique-hp35/test_biophysique_input_nul.csv`
    (n=1000, p=7).
  - LUAD réel : `pdac_luad_fluxes.csv` (n=515, p=12).
  - TCGA v4 réel : `pdac_tcga_fluxes_v4.csv` (n=178, p=12).
- Sous-échantillons PRÉFIXE (primaires) : les k premières lignes de la
  matrice source, en-tête conservée, colonne `step` réécrite explicitement
  0..k−1 (identique aux valeurs d'origine, qui sont déjà 0..n−1
  consécutifs — vérifié par le script, sinon arrêt). Le préfixe conserve
  l'ordre, l'espacement et le début de la série ; il ne change que sa
  longueur. Limite nommée d'avance : le préfixe change aussi le segment
  couvert (les k premières positions du contrôle) ; si la série est
  non stationnaire le long du contrôle, segment et longueur sont
  confondus — c'est pourquoi trois matrices d'origines différentes sont
  utilisées, et pourquoi une sensibilité par stride est gelée (§2.3).
- Grille de tailles gelée : k ∈ {45, 70, 100, 145, 178, 285, 515, 1000},
  avec k ≤ n et k ≥ 45 (minimum 40 points du mode fast v6.1/v6.2, marge
  incluse). Soit HP35 réel 8 runs, HP35 nul 8 runs, LUAD 7 runs,
  TCGA v4 5 runs = **28 runs préfixe**.
- Fichiers : `pdac_862_hp35_n<k>.csv`, `pdac_862_hp35nul_n<k>.csv`,
  `pdac_862_luad_n<k>.csv`, `pdac_862_tcga_n<k>.csv` ; sorties
  `results_fast_v62_862_hp35_n<k>`, etc. ; SHA-256 de chaque CSV
  sous-échantillonné noté par le script de construction.
- Commande (identique aux lots précédents, §8.53) :
  `python3 universal_v6.2.0_cohen.py --input <csv> --mode fast --output <dir>`,
  répertoire de travail `~/workspace/runs/pdac-v6/`, SHA v6.2 vérifié
  avant et après le lot, lancement via `systemd-run` (jamais `nohup` —
  leçon AGENTS.md 2026-11-17), journal des exit codes.
  Un run est VALIDE si `master_results.json` existe et si d_div, d_sat,
  Delta y sont finis ; sinon il est compté en échec et rapporté comme tel.
  Extraction des cibles d'un run B : mêmes champs que
  `extract_delta_levels.py` (`holographic_tension_state.D_vector` pour
  d_div/d_sat, `reading_synthesis.Delta_tension` pour Delta, médianes
  triées du même état) ; identités d_div/d_sat re-vérifiées sur les runs B.

### 2.3 Sensibilité schéma — stride (3 runs)

- Pour HP35 réel seulement, sous-échantillon STRIDE : k lignes
  régulièrement espacées couvrant toute la série (indices
  arrondis de linspace(0, n−1, k)), mêmes k ∈ {100, 285, 515}, colonne
  `step` réécrite 0..k−1.
- *Correction du 20 nov. 2026, avant tout run du lot : la première
  version de ce protocole définissait le stride par « une ligne sur m,
  m = arrondi(n/k) » — cette règle ne donne pas k lignes (ex. n=1000,
  k=285, m=4 → 250 lignes, constaté à la construction). Remplacée par
  des indices régulièrement espacés de linspace(0, n−1, k), qui
  conservent le sens gelé (même couverture, pas régulier) et le nombre
  de lignes. Aucun run du pipeline n'avait encore eu lieu.*
- Fichiers : `pdac_862_hp35_stride_n<k>.csv`, sorties
  `results_fast_v62_862_hp35_stride_n<k>`.
- Rôle gelé : si préfixe et stride donnent la même courbe en n (écarts
  de Delta ≤ 0,10 aux 3 tailles), la loi ne dépend pas du schéma ;
  sinon la « loi » est dépendante du schéma et le verdict s'affaiblit
  d'autant. Total du lot B : **31 runs**.

## 3. Formes candidates gelées (OLS, numpy/scipy/pandas seulement)

Mêmes 7 formes pour chaque cible y (13 médianes + d_div + d_sat + Delta),
ajustées par moindres carrés ordinaires, ln = logarithme népérien
(ln n et log10 n ne diffèrent que d'un facteur d'échelle) :

- **F0** : y = a (constante — base).
- **F1** : y = a + b·ln n.
- **F2** : y = a + b·ln n + c·(ln n)².
- **F3** : y = a + b·n.
- **F4** : y = a + b/n.
- **F5** : y = a + b/√n.
- **F6** : y = a + b·√n.

**Aucune autre forme, aucun hyperparamètre ajusté sur le test.** Si aucune
forme n'atteint les critères (§6), le verdict est « loi non trouvée », pas
une recherche de forme supplémentaire. MFA, quasi discret (9 valeurs),
est traité comme les autres cibles pour F1–F6 (régression linéaire), et
son cas est commenté séparément si F1 y échoue.

## 4. Hold-outs et unités d'indépendance

- Ensemble A : l'unité est la MATRICE (156 distinctes). LOCO
  leave-one-cohort-out (9 plis, mêmes règles de cohorte que §8.42 §5.1)
  pour F1 seulement (la forme de référence) : R² LOCO poolé par cible.
  La forme F1 ajustée sur les 222 runs sert aussi au transfert A→B (§5.3).
- Ensemble B : l'unité est la MATRICE SOURCE (4 courbes : hp35 réel,
  hp35 nul, luad, tcga). R² intra-matrice (F1, par courbe) et R² poolé
  (toutes courbes B, F1–F6). Le transfert A→B est le test décisif de
  portabilité : mêmes coefficients, nouvelles tailles, mêmes matrices
  pour hp35/luad/tcga (les matrices sources figurent dans A à leur n
  plein — le transfert teste donc l'interpolation/extrapolation en n,
  pas une matrice nouvelle ; c'est nommé, pas caché).

## 5. Mesures gelées (toutes rapportées)

### 5.1 Ensemble A — la loi sur les runs détenus

- Pour chaque cible (16) et chaque forme (F0–F6) : R², MAE, Pearson
  r(y, ln n). Tableau complet.
- F1 en LOCO (9 plis) : R² poolé par cible ; par pli pour Delta, d_div,
  d_sat.
- À n fixé : écart-type et étendue de Delta (et d_div) dans chaque cohorte
  à n unique (tcga n=178, depmap n=45, geo71729 n=145, icgc n=70,
  geo62452 n=69, luad n=515, coad n=285, hp35 n=1000) — la variation de
  Delta à n fixé est la part que AUCUNE loi en n ne peut expliquer.
- Variance expliquée : R² de F1 pour Delta, d_div, d_sat sur les 222 runs
  et sur les 156 moyennes par matrice (pour écarter la pseudo-réplication
  des rep2 / v6.1+v6.2).

### 5.2 Le résidu — ce qui reste quand on retire f(n)

- Résidu r = Delta − F1(ln n) (F1 ajustée sur les 222 runs).
- Paires réel/nul (appariement §2.1) : distribution de
  Delta_réel − Delta_nul (moyenne, écart-type, fraction |diff| ≤ 0,10)
  ET de r_réel − r_nul (mêmes statistiques). Si retirer f(n) ne change
  rien aux différences réel/nul, c'est que f(n) ne portait pas la
  différence — elle était déjà nulle en n.
- Corrélation Delta vs ln n séparément sur les runs réels seuls et les
  nuls seuls (mêmes pente/intercept à l'erreur près ?).
- Test de séparation du résidu : le résidu distingue-t-il réel de nul
  mieux que le hasard ? Moyenne |r_réel − r_nul| vs 0,10 ; un résidu qui
  séparerait (écart systématique) est rapporté comme tel.

### 5.3 Ensemble B — la loi causale, même matrice, n qui varie

- Par courbe (hp35 réel, hp35 nul, luad, tcga) et par cible : R² de F1
  intra-matrice ; pente b de F1 par courbe (même signe ? même ordre de
  grandeur ?).
- Poolé B (31 runs) : R² et MAE de F0–F6 par cible.
- Transfert A→B : F1 et F2 ajustées sur A (222 runs) appliquées aux
  points B ; fraction des points B prédits à ±0,10 (Delta, d_div, d_sat)
  et MAE de transfert par cible ; mêmes chiffres pour les 13 médianes
  (fraction à ±0,10).
- Réel vs nul en B (HP35, 8 tailles) : |Delta_réel(k) − Delta_nul(k)| par
  k, fraction ≤ 0,10 ; pentes F1 réel vs nul (écart) ; mêmes chiffres
  pour d_div et d_sat.
- Stride vs préfixe (HP35, 3 tailles) : |Delta_stride − Delta_prefixe|
  par k ; fraction ≤ 0,10.

### 5.4 Sensibilités

- Sans DFA extrême : F1 pour Delta, d_div, d_sat et les 13 médianes
  refaite sur A sans les 22 runs |DFA| > 10 — les deux jeux de chiffres
  rapportés.
- Sans hp35 (n=1000, seul point au-delà de 515) : F1 pour Delta refaite
  sur A sans les 6 runs hp35 — la loi tient-elle sans son point extrême ?
- Déduplication (§8.39.6, 153 runs) : F1 pour Delta refaite — stabilité.

## 6. Critères de succès (écrits avant les résultats)

### 6.1 LOI D'ÉCHELLE TROUVÉE (par cible ; Delta est la cible primaire)

**TROUVÉE** si et seulement si UNE MÊME forme parmi F1–F6 atteint à la
fois :
(a) R² ≥ 0,80 sur l'ensemble A (222 runs) ;
(b) R² ≥ 0,80 sur l'ensemble B poolé (31 runs) ;
(c) transfert A→B : ≥ 90 % des points B prédits à ±0,10 (Delta, d_div,
d_sat ; pour les 13 médianes : MAE de transfert ≤ 0,10 sur ≥ 90 % des
points).
Sinon **NON TROUVÉE** pour cette cible (les chiffres de chaque forme sont
rapportés). Une forme qui passe (a) mais pas (b)/(c) est une corrélation
inter-cohortes, pas une loi d'échelle — le verdict le dit.

### 6.2 LA LOI SUFFIT À EXPLIQUER LA NON-SÉPARATION RÉEL/NUL

**SUFFIT** si et seulement si la loi est TROUVÉE pour Delta (§6.1) ET :
(i) à n fixé, l'écart-type intra-cohorte de Delta est ≤ 0,10 dans au
moins 6 des 8 cohortes à n unique (sinon l'essentiel de la variance de
Delta n'est pas en n) ;
(ii) le résidu r = Delta − F1(ln n) ne sépare pas réel de nul :
fraction des paires avec |r_réel − r_nul| ≤ 0,10 ≥ 90 % ET
|moyenne(r_réel − r_nul)| ≤ 0,10 ;
(iii) en B, courbes HP35 réel vs nul coïncidentes : |Delta_réel(k) −
Delta_nul(k)| ≤ 0,10 sur au moins 7 des 8 tailles.
Si la loi n'est pas trouvée, ou si (i)/(ii)/(iii) échoue, le verdict est
**NE SUFFIT PAS**, avec le volet qui échoue nommé. Un échec est un
résultat, pas un défaut à cacher.

## 7. Ce que ce protocole ne fera pas

- Aucune modification d'un code (v6, v6.1, v6.2 intacts — SHA vérifiés
  avant travail, voir §8) ; les 31 runs B sont des runs du pipeline
  v6.2 **non modifié**, en mode fast, sur des CSV sous-échantillonnés.
- Aucune forme ajoutée après avoir vu les résultats ; la liste du §3 est
  gelée. Aucune sélection d'indicateur après coup ; aucune affirmation
  clinique.
- Aucun ajout de runs hors des 31 gelés (ni les 185 dossiers v62
  postérieurs §8.47/§8.53, ni d'autres matrices) à l'ensemble B.
- Aucun push GitHub, aucune régénération du PDF (hors de ce chantier).

## 8. Traçabilité et provenance

- Script unique de ce chantier : `v62_delta_scaling_862.py` (lecture
  seule des JSON/CSV pour A ; construction des sous-échantillons B ;
  analyse A et B ; écritures : `v62_delta_scaling_862.log`,
  `v62_delta_scaling_862.json`, `v62_delta_scaling_862.md`,
  `v62_delta_scaling_862_features.csv` — cibles, n, résidus par run,
  SHA-256 de chaque matrice source et de chaque CSV sous-échantillonné).
- Lanceur du lot B : `run_delta_scaling_862.sh` (systemd-run, journal
  des exit codes `runs_delta_scaling_862.log`).
- Pipeline : v6.2 `universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant travail, jamais modifié) ; v6.1 SHA-256
  `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ;
  v6 SHA-256 `bb8bbdba…c0773` (forme courte du dossier ; complet dans
  `PROVENANCE_v6.2.md`).
- Données A : les 222 `master_results.json` (156 v6.1 + 66 v6.2), base de
  cibles `v62_delta_levels.csv` ; 156 matrices de flux distinctes (TCGA,
  GEO, ICGC, CPTAC, DepMap, COAD, LUAD, HP35 — voir les
  `PROVENANCE_*.md` du dossier — et leurs nuls permutés, graine 42).
  Nature des lignes : sorties instrumentales du pipeline (médianes par
  estimateur) ; matrices de flux = mesures omiques publiques (TCGA v4,
  LUAD) ou série biophysique simulée (HP35) ; contrôles = noms de flux
  (étiquettes, mots humains) sauf `step`.
- Données B : 4 matrices sources ci-dessus (§2.2) et leurs 31
  sous-échantillons préfixe/stride, construits par troncature déterministe
  (pas d'aléa) ; SHA-256 notés dans `v62_delta_scaling_862_features.csv`.
- Consignation : verdict au livre blanc en §8.62, ligne correspondante
  au §7, entrée de journal datée. PDF non régénéré (hors de ce chantier).
- Ce qui manque (déclaré d'avance) : dans A, n et cohorte sont presque
  parfaitement confondus (n constant intra-cohorte) ; B ne teste que 3
  matrices sources et 1 nul ; le transfert A→B partage les matrices
  sources (il teste n, pas une matrice nouvelle) ; le préfixe confond
  longueur et segment (sensibilité stride sur 1 matrice, 3 tailles) ;
  aucune source entièrement nouvelle au-delà des 9 cohortes n'est testée.

— Fin du protocole gelé. —
