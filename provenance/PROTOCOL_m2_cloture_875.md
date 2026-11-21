# PROTOCOLE GELÉ — §8.75 : Clore le résidu M2 du §8.63 (20 novembre 2026)

Go : parent orchestrator, 20 nov. 2026, « Les 3 allez s'y » (3e des 3
pistes du lot du 20 nov. 18h04). Ce protocole est gelé AVANT tout
nouveau script, toute nouvelle construction, tout nouveau run et tout
nouveau calcul de ce chantier. Aucun paramètre ne change après les
résultats. Livre blanc NON édité directement (section dans un fichier
séparé `section_8.75_m2_cloture.md`). PDF NON régénéré. Rien poussé
sur GitHub. Pipeline v6.2 JAMAIS modifié (SHA attendu
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`).

## 0. Question

Le §8.63 a expliqué M2a (ensemble des 12 configs fixe par n) et M2b
(petit w + grille fine gagne : la « config réelle » est le point de
grille qui maximise le max), mais M2d — la réplication hors
échantillon du taux de choix de la config réelle — est restée
INDÉCISE : 6/10 nuls frais ICGC s31–s40 choisissent (35, 16, 6),
P(X ≤ 6 | p = 0,85) = 0,050, à la frontière. Le taux de §8.53
(17/20 = 85 %) ne se reproduisait pas à l'identique, il se tassait
(23/30 = 76,7 % sur les nuls frais ICGC s11–s40).

**Question précise.** La réplication hors échantillon de M2
tient-elle avec un échantillon plus large ET un critère gelé
d'avance ? Deux volets : (A) primaire — 30 nuls ICGC frais
(graines 61–90, jamais utilisées) ; (B) secondaire — 10 nuls
GSE62452 frais (graines 31–40, jamais utilisées), pour vérifier que
la réplication n'est pas propre à une seule cohorte.

**Ce qui n'est PAS rouvert.** M1 (expliqué au §8.63 : MC haut =
propriété de la permutation, Delta bas = propriété de w) n'est pas
re-testé. Le déclencheur du pic étroit n'est pas recherché : le
§8.73 l'a clos comme NON ÉLUCIDÉ (ni bloc extrême, ni ligne unique
en général, ni queues globales, ni bord seul) — ce chantier ne
rouvre pas cette question, il ne fait que COMPTER les basculements
de robustesse sur le nouveau lot, par une définition gelée (§2 E),
sans en chercher la cause. Aucun verdict de séparation n'est
touché ; aucun plancher n'est re-testé ni redéfini.

## 1. Faits de départ (relus, jamais des verdicts réimportés)

- §8.63 (`section_8.63_mechanisms.md`, protocole
  `PROTOCOL_mechanisms_863.md` SHA `4e05dfc2…f35e`) : M2a EXPLIQUÉ
  (1 seul ensemble de 12 configs par n ; `rng = default_rng(42 +
  itération)`, lignes 243 et 3461) ; M2b EXPLIQUÉ (config réelle =
  maxsep moyen le plus élevé dans les deux cohortes n≈70 +
  clause alternative : plus fine grille parmi les configs de
  petit w) ; marges médianes vainqueur–2e : 0,0029 (ICGC), 0,0028
  (GSE62452), 0,0037 (TCGA) — choix quasi-ex-aequo ; M2d INDÉCIS
  (6/10, P = 0,050). Formule MC vérifiée à 0,00e+00 :
  MC = 0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·acuité,
  s_norm = tanh(maxsep/2), rob = exp(−((FWHM − 10)²)/(2·5²)).
- §8.73 (`section_8.73_pic_etroit.md`, protocole
  `PROTOCOL_pic_etroit_873.md` SHA `28d2326c…51a4c`) : lot frais
  ICGC s41–s60, 20/20 exit 0 — la gagnante est (35, 16, 6) dans
  17/20 cas et (22, 16, 7) dans 3/20 (s42, s47, s51) ; 0 courbe
  rob-on sur 240 (rob > 0,1 : 3/240 ; rob > 0,5 : 0/240).
- **Corpus existant relu (baseline, connue avant ce chantier).**
  Nuls frais ICGC s11–s60 : 40/50 choisissent (35, 16, 6)
  (17/20 §8.53 + 6/10 §8.63 + 17/20 §8.73), soit 80,0 %,
  intervalle de Wilson 95 % [0,670 ; 0,888], test binomial
  exact unilatéral vs p = 0,85 : P(X ≤ 40 | n = 50) = 0,209
  (0,85 non rejeté). Nuls frais GSE62452 s11–s30 : 17/20
  choisissent (34, 16, 6) (§8.53). Ces nombres sont la baseline
  DÉCLARÉE, pas le critère : le critère porte sur le lot NEUF
  seul (§3), dont le résultat est inconnu à l'écriture de ce
  protocole.
- Configs réelles (définies par les runs réels, §8.63.6) :
  ICGC (35, 16, 6) ; GSE62452 (34, 16, 6).

## 2. Hypothèses nommées d'avance

- **H_A (réplication tient).** Le taux de choix de la config
  réelle est stable autour de 75–85 % : c'est une propriété de
  la grille (M2b), le 85 % de §8.53 n'était pas un tirage haut,
  et le 6/10 de §8.63 était la fluctuation d'un petit
  échantillon (P = 0,050 à la frontière).
- **H_B (réplication ne tient pas).** Le 85 % de §8.53 était un
  tirage haut ; le taux réel est ≤ 60 % et le choix de la
  config est dominé par les basculements de robustesse, pas
  par le biais de grille.
- **H_0 (quasi-ex-aequo instable).** Le taux est intermédiaire
  (~65–75 %) : la config réelle gagne le plus souvent, mais les
  marges médianes ~0,003 rendent l'étiquette instable et les
  basculements de robustesse fréquents — la réplication est
  alors une question de taux, pas de oui/non.

## 3. Méthodes — dans l'ordre, sans retour en arrière

### A. Construction des nuls frais (aucun run)

Script neuf `build_nulls_icgc_gse_875.py` : même méthode que
`build_nulls_icgc_863.py` / `build_nulls_n70_853.py`
(`default_rng(graine)`, `permutation(n)`, lignes entières, les
12 flux d'une tumeur voyagent ensemble, colonne `step`
inchangée, même multi-ensemble de lignes vérifié par assert).
Graines NOUVELLES, jamais utilisées : ICGC 61–90 (30 nuls),
GSE62452 31–40 (10 nuls). Entrées vérifiées par SHA avant
construction : ICGC réel
`10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc`
(relu dans `nulls_n70_853_verify.json`, re-vérifié ici) ;
GSE62452 réel
`97c4689a6ecacd0a73a77804200a72a90994d60bea7e6b2c079195acbffd79a3`
(idem). Sorties : `nulls_icgc_gse_875_files.json` (SHA-256 de
chaque fichier) + `PROVENANCE_875.md`.

### B. Lots pipeline v6.2 (40 runs fast)

- **Lot A (primaire) :** 30 runs ICGC s61–s90, sorties
  `results_fast_v62_875_icgc_nul_s<graine>/`.
- **Lot B (secondaire) :** 10 runs GSE62452 s31–s40, sorties
  `results_fast_v62_875_geo62452_nul_s<graine>/`.
- Lanceur reprenable `run_v62_875.sh` (copie de
  `run_v62_lot.sh`), manifeste `manifest_v62_875.txt`,
  `systemd-run` (jamais nohup), journal `runs_v62_875.log`
  (SHA v6.2 avant/après, exits), surveillance `watch_v62_875.sh`
  (reprend le lanceur tant que les 40 `master_results.json`
  ne sont pas présents ; ne supprime jamais un dossier).
  Exit 0 exigé pour les 40 runs ; un run interrompu
  (redémarrage machine) est relancé tel quel après suppression
  de son dossier partiel (sans `master_results.json`) ; jamais
  remplacé par une autre graine. SHA v6.2 vérifié avant le lot,
  avant toute relance et après le lot.

### C. Extraction (lecture seule des `master_results.json`)

Script neuf `m2_cloture_875.py` : reprend le lecteur de
`mechanisms_863.py` (`read_all_results` :
`run_pipeline.threshold_metadata.threshold_optimization`,
12 configs par run, champs `score`, `s_norm`, `stability`,
`robustness`, `sharpness`, `max_separation`, `scan_curve`,
`best_config`). Pour chaque run lu (80 ICGC frais s11–s90
+ 30 GSE frais s11–s40) : config gagnante, MC, rob, maxsep,
marge vainqueur–2e, ensemble des 12 configs (contrôle M2a :
1 seul ensemble par n). **Vérification d'extraction** :
recomposition du MC (0,3·s_norm + 0,3·stab + 0,2·rob +
0,2·acuité) comparée au `score` stocké, écart toléré 10⁻⁶,
sur TOUTES les configs de TOUS les runs lus ; la lecture
n'est validée que si l'écart max est ≤ 10⁻⁶ (comme §8.63,
écart 0,00e+00). Sorties : `m2_cloture_875_extract.json`,
`m2_cloture_875_results.csv`.

### D. Comptages gelés (critère §4)

- X = nombre de runs du lot A (n = 30) dont la gagnante est
  (35, 16, 6). Y = nombre de runs du lot B (n = 10) dont la
  gagnante est (34, 16, 6).
- Lectures secondaires (rapportées, hors critère) : taux
  poolés ICGC (80 nuls : s11–s90) et GSE (30 nuls : s11–s40)
  avec intervalles de Wilson 95 % ; test binomial exact
  unilatéral vs p = 0,85 (H0 : p = 0,85, alternative p < 0,85)
  sur le lot neuf seul et sur le poolé ; médiane des marges
  vainqueur–2e sur les lots neufs (références §8.63 : 0,0029
  ICGC, 0,0028 GSE) ; nombre de courbes rob-on (rob > 0,1 et
  rob > 0,5) sur les 480 courbes neuves (référence §8.73 :
  3/240 rob > 0,1, 0/240 rob > 0,5 sur le lot frais).

### E. Attribution des écarts (descriptive, hors critère gelé)

Pour chaque run neuf dont la gagnante N'EST PAS la config
réelle : recomposition du MC SANS le terme de robustesse,
MC_sans_rob = (MC − 0,2·rob) / 0,8, pour la gagnante et pour
la config réelle (lues dans les `all_results` du run). Un
écart est classé **« basculement de robustesse »** si et
seulement si MC_sans_rob(config réelle) > MC_sans_rob(gagnante)
ET rob(gagnante) > 0,1 ; sinon il est classé « autre »
(avec les deux nombres rapportés). Cette classification ne
cherche PAS la cause du pic (§8.73, clos) : elle mesure
seulement si le terme de robustesse a renversé l'ordre,
comme au §8.63.7.

### F. Ce qui n'est PAS fait

- Aucune modification du pipeline, aucun nouveau seuil, aucune
  sélection d'indicateur après coup, aucune imputation, aucune
  valeur inventée, aucun nouveau nul construit après lecture
  des résultats (les graines 61–90 et 31–40 sont gelées ici
  avant tout run).
- Aucune conclusion importée d'autres bras (rotations, tests
  A/C, PARP, §8.54–§8.74) : seules les données et runs de ce
  chantier font verdict, sauf citation explicite « relu §8.63 /
  §8.73 » pour les faits de départ.
- Aucun test direct nouveau (PRMT5, prolifération, survie).
- Le plancher 0,07 (§8.46/§8.50) et les planchers p95 (§8.53)
  ne sont ni re-testés ni redéfinis ici. M1 n'est pas re-testé.

## 4. Règles de décision — écrites avant (par volet)

Nombres binomiaux exacts calculés avant tout run (H0 p = 0,85,
unilatéral, alternative p < 0,85) :
- Lot A (n = 30) : P(X ≤ 20) = 0,0097 ; P(X ≤ 12) < 0,0001.
- Lot B (n = 10) : P(Y ≤ 6) = 0,0500 ; P(Y ≤ 4) = 0,0014.
- Poolé ICGC (n = 80, baseline 40 connue) : P(pool ≤ 62) =
  0,0480 ; P(pool ≤ 61) = 0,0259.

**Lot A (primaire, ICGC, n = 30).**
- **CONFIRME** si X ≥ 21/30 (≥ 70 %) — même seuil proportionnel
  que M2d au §8.63 (≥ 7/10) ; un X ≤ 20 rejetterait p = 0,85
  à α = 0,01.
- **INFIRME** si X ≤ 12/30 (≤ 40 %) — même seuil proportionnel
  que M2d au §8.63 (≤ 4/10).
- **INDÉCIS** si 13 ≤ X ≤ 20.

**Lot B (secondaire, GSE62452, n = 10).**
- **CONFIRME** si Y ≥ 7/10 ; **INFIRME** si Y ≤ 4/10 ;
  **INDÉCIS** si 5 ≤ Y ≤ 6 — reprise exacte de la règle M2d
  du §8.63.

**Verdict global M2.**
- **TRANCHÉ–CONFIRMÉ** si le lot A CONFIRME et le lot B
  n'INFIRME pas (confirme ou indécis) : la réplication hors
  échantillon tient, H_A retenue.
- **TRANCHÉ–INFIRMÉ** si le lot A INFIRME : la réplication ne
  tient pas, H_B retenue.
- **TRANCHÉ–DIVERGENT** si le lot A CONFIRME et le lot B
  INFIRME : la réplication tient en ICGC, pas en GSE62452 —
  à nommer comme tel, sans généralisation.
- **FERMÉ COMME NON CONCLUANT** si le lot A est INDÉCIS : le
  taux poolé sur 80 nuls ICGC est rapporté avec son intervalle
  de Wilson 95 % et son p binomial vs 0,85, ce qui a été testé
  et éliminé est nommé, et la question du taux exact est close
  comme non conclusive — un nouvel échantillon ne serait
  justifié que par un protocole neuf, pas par une extension de
  celui-ci.
- Dans tous les cas, le verdict M2 global du §8.63
  (PARTIELLEMENT EXPLIQUÉ : M2a et M2b expliqués, M2d indécis)
  est mis à jour par le verdict ci-dessus, et le résidu
  « pourquoi la robustesse bascule » reste renvoyé au §8.73
  (NON ÉLUCIDÉ), non rouvert ici.

## 5. Sorties

- Ce protocole `PROTOCOL_m2_cloture_875.md` (SHA noté dans la
  section).
- Scripts neufs : `build_nulls_icgc_gse_875.py`,
  `run_v62_875.sh`, `watch_v62_875.sh`, `m2_cloture_875.py`
  (SHA notés dans la section).
- Données/résultats : `nulls_icgc_gse_875_files.json` (SHA des
  40 nuls frais), `manifest_v62_875.txt`, `runs_v62_875.log`
  (40/40, exit 0), `watch_v62_875.log`,
  `m2_cloture_875_extract.json`, `m2_cloture_875_results.csv`,
  dossiers `results_fast_v62_875_icgc_nul_s61/` … `s90/` et
  `results_fast_v62_875_geo62452_nul_s31/` … `s40/`.
- Section `section_8.75_m2_cloture.md` (verdict d'abord,
  chiffres, méthode, limites, provenance — format des
  sections précédentes, ~400–500 lignes).
- `PROVENANCE_875.md` (40 nuls frais : entrées, méthode,
  SHA, nature des lignes).

## 6. Limites connues d'avance

- Mode fast seulement : 12 configs par run. Les nombres
  (taux de choix, marges) sont propres au mode fast ; le
  mécanisme de grille fixe reste le même en nature dans les
  autres modes (graine fixe + itération), mais les taux
  pourraient différer.
- Le lot A (n = 30) tranche entre un taux ~0,85 et un taux
  ~0,60–0,70, pas entre 0,85 et 0,80 : si le taux réel est
  0,75–0,80, le lot A CONFIRME (X ≥ 21) tout en restant
  compatible avec un tassement — c'est pourquoi le taux poolé
  sur 80 nuls et son intervalle de Wilson sont rapportés
  dans tous les cas.
- La baseline poolée 40/50 était connue avant le lot : le
  critère primaire porte sur le lot NEUF seul (X), jamais
  sur le poolé — le poolé est une lecture secondaire.
- L'attribution des écarts (§2 E) mesure le rôle du terme de
  robustesse dans l'ordre des configs, pas la cause du pic :
  elle ne rouvre pas le §8.73.
- n = 70 (ICGC) et 69 (GSE62452) ; un seul contrôle (`step`) ;
  aucune donnée nouvelle hors des CSV déjà sur disque et des
  40 nuls frais ; aucun test direct ; aucun verdict biologique.
