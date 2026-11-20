# PROTOCOLE GELÉ — §8.50 : Consolidation de l'arbitrage MTAP (10 nuls frais) (19 novembre 2026)

Go : parent orchestrator, 19 nov. 2026 (chantier 1/4). Ce protocole est gelé
AVANT toute nouvelle construction, tout nouveau run et tout nouveau calcul
de ce chantier. Aucun paramètre ne change après les résultats. Livre blanc
NON édité directement (section dans un fichier séparé
`section_8.50_mtap_consolidation.md`). PDF NON régénéré. Rien poussé sur
GitHub. Pipeline v6.2 JAMAIS modifié (SHA attendu
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`).

## 0. Question

Le §8.46 a arbitré « S_sep VOIT DU RÉEL » (marche de niveau multi-flux,
pas une rupture) sur la série TCGA v4 ordonnée par CN MTAP (177 tumeurs,
contrôle MTAPCN), mais avec 3 nuls seulement et une marge fragile :
l'écart S_sep réel − nul graine 7 (+0,0715) ne dépasse le plancher 0,07
que de 0,0015. Question : avec 10 nuls FRAIS, la distribution des écarts
S_sep réel − nul tient-elle au-dessus du plancher 0,07, ou l'arbitrage
de §8.46 s'effondre-t-il ?

Faits d'entrée (attendus de reproduction, jamais des verdicts réimportés) :
- MTAP réel v6.2 (§8.46, §8.38) : S_sep 0,3378 ; max_separation 0,3392 ;
  stabilité 0,9959 ; MC 0,3511 (seuil 69,57 %) ; Delta 3,8051 ;
  cascade 0,54 / 60,74 / 72,77 / 92,11 / 92,11 % ; L7a DOWN 0,427 ;
  falsification 0,733.
- Nuls existants : graine 42 S_sep 0,1409 (écart +0,1968), MC 0,5153,
  Delta 4,3466 ; graine 7 S_sep 0,2663 (écart +0,0715), MC 0,3422,
  Delta 3,8085 ; graine 123 S_sep 0,2031 (écart +0,1347), MC 0,4518,
  Delta 3,1415.
- Plancher 0,07 : celui du protocole §8.46 (§4), repris tel quel —
  aucun nouveau plancher n'est choisi ici.

## 1. Mécanique (rappel §8.46, lue dans le code v6.2, pas devinée)

- `S_sep = max_separation × stability`, lus dans `best_config.metrics`.
- `max_separation` = MAX, sur les seuils candidats du scan, de la moyenne
  sur les flux du |d de Cohen| entre groupes pré- et post-seuil.
- MC `best_score` = composite 0,3·s_norm + 0,3·stabilité +
  0,2·robustesse + 0,2·acuité (poids par défaut, code lignes 3727–3730).
- Delta = d_div − d_sat (médianes BRUTES de dimensions, correction
  §8.46.1 — pas des médianes T_log) ; largeur spectrale globale,
  sans rapport avec un seuil.
- Un nul = une permutation conjointe des lignes (mêmes marginales,
  ordre brisé) ; il ne teste que l'ordre, pas la structure marginale.

## 2. Méthodes — dans l'ordre, sans retour en arrière

### A. Construction de 10 nuls frais (graines nouvelles, jamais utilisées)
Graines : 1011, 2022, 3033, 4044, 5055, 6066, 7077, 8088, 9099, 11111.
Aucune n'a servi dans ce projet (les seules graines de nuls MTAP
utilisées jusque-là sont 42, 7 et 123 ; les motifs `nul_s1/2/3` vus
ailleurs appartiennent à d'autres chantiers, pas à des nuls MTAP).
Même méthode que le nul graine 42 (`build_fluxes_tcga_v4_mtap.py`
lignes 167–169 ; `build_mtap_nuls_846.py`) : `rng(seed).permutation`,
lignes permutées ensemble, colonne MTAPCN intacte. Script neuf
`build_mtap_nuls_850.py` (adaptation propre de `build_mtap_nuls_846.py`,
même assertion SHA sur l'entrée). Sorties :
`pdac_tcga_fluxes_v4_mtap_nul_s<graine>.csv` (+ SHA-256 de chacune).
Entrée vérifiée par SHA avant construction :
`pdac_tcga_fluxes_v4_mtap.csv`
`578b8d3b9b26099d0784ed23754d1cc9717be7f9292eb47e201d186cdbc90df6`
(177 lignes, 1re colonne MTAPCN monotone croissante).

### B. Runs v6.2 fast — 11 runs : 1 réel de reproduction + 10 nuls frais
- Réel de reproduction : même entrée `pdac_tcga_fluxes_v4_mtap.csv`,
  sortie DISTINCTE `results_fast_v62_mtap_850` (l'original
  `results_fast_v62_mtap` n'est ni écrasé ni effacé). Attendu :
  valeurs identiques à l'original (v6.2 déterministe, hachage stable,
  §8.37). Si l'écart sur S_sep dépasse 10⁻⁶, la non-reproductibilité
  est consignée et la valeur du jour est celle du re-run 850.
- Nuls frais : sorties `results_fast_v62_mtap_nul_s<graine>/`.
- Lanceur reprenable `run_v62_lot.sh`, manifeste
  `manifest_v62_mtap_nuls850.txt` (format NOM|ENTREE|SORTIE),
  `systemd-run` (jamais nohup), exit 0 exigés pour les 11 runs.
  Journal `runs_v62_mtap_nuls850.log` (SHA v6.2 avant/après, exits).
- Les 3 nuls existants (42, 7, 123) ne sont PAS relancés : leurs
  `master_results.json` sont relus tels quels.

### C. Lecture et statistiques (extracteur neuf, aucun seuil choisi après coup)
Script neuf `mtap_consolidation_850.py` : lit `master_results.json`
des 14 dossiers (réel original, réel 850, 3 nuls anciens, 10 nuls
frais) et extrait, pour chacun, S_sep, max_separation, stabilité, MC
best_score + seuil, Delta, D-vector, cascade, L7a, falsification.
Puis, sur les 10 écarts frais g_i = S_sep réel (valeur du jour, §B)
− S_sep nul frais i :
- médiane, min, max, 1er et 3e quartiles, moyenne ;
- nombre (et part) de g_i > 0,07, de g_i ≤ 0,07, de g_i ≤ 0
  (nul ≥ réel) ;
- mêmes comptages sur les 13 nuls regroupés (3 anciens + 10 frais),
  à titre secondaire.
Re-vérification MC et Delta : réel du jour dans ou hors de
l'intervalle des 10 nuls frais (min–max) ; nombre de nuls frais
avec MC > réel et avec Delta > réel. Re-vérification du MC composite
(recomposition 0,3·s_norm + 0,3·stabilité + 0,2·robustesse +
0,2·acuité, écart toléré 10⁻⁶) sur le réel 850 et les 10 nuls frais.
Sorties : `mtap_consolidation_850_results.csv` (tous les nombres cités)
et `mtap_consolidation_850_extract.json` (relecture brute).

### D. Ce qui n'est PAS fait
- Aucune modification du pipeline, aucun nouveau seuil, aucune
  sélection d'indicateur après coup, aucune imputation, aucune valeur
  inventée, aucun nouveau nul construit après lecture des résultats.
- Aucun test direct nouveau (PRMT5, prolifération) : le §8.46 les a
  déjà faits ; ce chantier ne teste que la distribution nulle de
  S_sep/MC/Delta sur cette série.
- Aucune conclusion importée d'autres bras (rotations, tests A/C,
  immunitaire, PARP, §8.43–§8.49) : seules les données et runs du
  jour font verdict.
- Si un run échoue (exit ≠ 0, redémarrage machine), il est relancé
  tel quel via le lanceur reprenable ; un run relancé n'est jamais
  remplacé par une autre graine.

## 3. Règles de décision — écrites avant (critère de consolidation)

Le plancher 0,07 est celui du §8.46. Sur les 10 écarts FRAIS seuls
(les 3 anciens servent de contexte, pas de verdict) :

- **TIENT** — si min(g_i) > 0,07 : les 10 nuls frais restent tous sous
  le S_sep réel de plus du plancher. L'arbitrage §8.46 est consolidé :
  la marge fragile sur le nul 7 était un tirage, pas la règle.
- **SE FRAGILISE** — si médiane(g_i) > 0,07 mais min(g_i) ≤ 0,07 :
  l'écart médian tient, mais au moins un nul frais passe sous le
  plancher. L'arbitrage §8.46 survit comme tendance médiane, pas
  comme séparation systématique ; la condition (1) du §8.46 ne tient
  plus à 10 nuls, et S_sep ne doit plus être cité comme séparant
  « le réel des nuls » sans la distribution complète.
- **TOMBE** — si médiane(g_i) ≤ 0,07 : la moitié au moins des nuls
  frais atteint ou dépasse le plancher. L'arbitrage §8.46 tombe :
  S_sep ne sépare pas le réel des nuls sur cette série au critère
  §8.46, et le verdict redevient NON ARBITRÉ / artefact possible —
  la marche de niveau (C2/C3 du §8.46, faits directs hors pipeline)
  reste un fait d'expression, mais S_sep ne la mesure pas de façon
  discriminante.

Cas limite consigné d'avance : un écart exactement égal à 0,07 compte
comme ≤ 0,07 (le plancher exige un dépassement strict, comme au §8.46).
La marche de niveau multi-flux (d de groupe GISTIC, Spearman, §8.46
§8.46.4) n'est PAS re-testée ici : elle vit dans les CSV, pas dans
S_sep, et aucun verdict de ce chantier ne la confirme ni ne l'infirme.
Le verdict §8.36 (pas de rupture, pas de chaîne KRAS sous l'ordre
MTAP) n'est pas touché par ce chantier.

## 4. Sorties

- Ce protocole `PROTOCOL_mtap_consolidation_850.md` (SHA noté dans la
  section).
- Script neuf `build_mtap_nuls_850.py` (SHA noté dans la section).
- 10 CSV nuls frais + SHA ; manifeste `manifest_v62_mtap_nuls850.txt` ;
  journal `runs_v62_mtap_nuls850.log` (11/11, exit 0).
- Script neuf `mtap_consolidation_850.py` (SHA noté dans la section) ;
  `mtap_consolidation_850_results.csv` ;
  `mtap_consolidation_850_extract.json`.
- Section `section_8.50_mtap_consolidation.md` (verdict d'abord,
  chiffres, méthode, limites, provenance — format des sections
  précédentes).

## 5. Limites connues d'avance

- n = 177 tumeurs, 12 flux d'expression ; le nul est une permutation
  conjointe — il ne teste que l'ordre, pas la structure marginale.
- 10 nuls frais + 3 anciens = 13 permutations : c'est une distribution
  nulle empirique, pas une loi ; les quantiles restent bruités
  (écart-type d'une médiane sur 10 tirages ~ ordre de l'écart
  interquartile / 3).
- Le plancher 0,07 est un critère hérité du §8.46, pas une loi
  physique : il mesure un écart absolu de S_sep, sans normalisation
  par la dispersion nulle.
- S_sep ≈ max_separation (stabilité 0,97–1,00) : la distribution
  mesurée est celle d'un maximum sur les seuils, sensible au choix
  de `best_config` d'un run à l'autre (configurations différentes
  possibles, §8.46.3).
- Un run v6.2 fast dure ~5 min ; le lot de 11 runs dure de l'ordre
  d'une heure, avec risque de redémarrage du service — d'où le
  lanceur reprenable et `systemd-run`, jamais nohup.
