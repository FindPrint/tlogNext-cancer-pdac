# PROTOCOLE GELÉ — Inversion immunitaire ICGC (§8.47)

Date de gel : 19 novembre 2026, avant tout run et toute analyse neuve.
Chantier 2/4 (coordinateur : fusion dans le livre blanc ensuite).
Règle durable : protocole gelé AVANT les runs ; provenance complète nommée ;
verdicts seulement sur les données et runs du jour ; ne jamais importer de
conclusions d'autres expériences ; ne pas exiger de consensus entre
flux/contrôles ; un nul qui invalide une piste est un résultat ; ne jamais
inventer de valeur. Pipeline v6.2 JAMAIS modifié.

## 1. Question

Pourquoi S_sep immunitaire ICGC est-il INVERSÉ (−0,2200) alors que les trois
autres cohortes sont positives (TCGA +0,3659 ; GSE62452 +0,1534 ;
GSE71729 +0,1343, §8.38) ? Pistes : taille (n=70), composition de la
cohorte, définition des flux immunitaires, artefact de construction.

## 2. Faits de départ (relus le 19 nov. 2026, §8.38 / ssep_838_verify.json)

S_sep = max_separation × stability (PROTOCOL_v6.2.md §3), lu dans
`run_pipeline.threshold_metadata.threshold_optimization.best_config` des
`master_results.json` v6.2 (vérifié identique en v6.1 sur 29/29 paires).

| Paire | n | maxsep réel | maxsep nul | d_maxsep | stab R/N | S_sep R | S_sep N | d_S_sep | MC R/N | Delta R/N |
|---|---|---|---|---|---|---|---|---|---|---|
| IMMUNE_TCGA | 178 | 0,5309 | 0,1634 | +0,3675 | 0,9914/0,9819 | 0,5263 | 0,1604 | +0,3659 | 0,379/0,324 | 4,21/2,30 |
| IMMUNE_GEO71729 | 145 | 0,2925 | 0,1563 | +0,1362 | 0,9916/0,9964 | 0,2900 | 0,1557 | +0,1343 | 0,344/0,324 | 2,86/2,67 |
| IMMUNE_GEO62452 | 69 | 0,4804 | 0,3154 | +0,1650 | 0,9692/0,9899 | 0,4656 | 0,3122 | +0,1534 | 0,369/0,348 | 1,37/1,41 |
| IMMUNE_ICGC | 70 | 0,2299 | 0,4500 | −0,2200 | 0,9955/0,9976 | 0,2289 | 0,4489 | −0,2200 | 0,334/0,368 | 1,50/1,32 |

Décomposition déjà établie (lecture seule, 19 nov.) :
- La stabilité est saturée partout (0,97–1,00) : S_sep ≈ max_separation.
  L'inversion vient ENTIÈREMENT de max_separation, pas de la stabilité.
- Le nul ICGC (0,4500) est le PLUS ÉLEVÉ des 8 maxsep immunitaires
  (réels 0,23–0,53 ; nuls 0,16 / 0,32 / 0,16 / 0,45) ; le réel ICGC
  (0,2299) est le PLUS FAIBLE des 4 réels. Inversion à deux côtés.
- Courbes de scan relues (run_pipeline.scan_curve) : réel ICGC plat
  (0,18–0,23 sur toute la plage, max à 23,5 %) ; nul ICGC en plateau haut
  précoce (0,450 à 19,0 %, 0,445 à 23,8 % et 28,6 %, puis décroissance
  lisse) — pas un pic isolé sur un seul candidat. Réel TCGA en rampe
  jusqu'à 0,53 à ~79 % ; réel GSE62452 en rampe jusqu'à 0,48 à 81,8 %.
- max_separation = max sur les candidats du score de scan = moyenne sur
  les 12 flux de |d de Cohen| entre groupes pré/post-seuil de fenêtres
  (code v6.2, `_scan_critical_threshold_fast` + `evaluate_scan_quality`,
  lu le 19 nov.). C'est une statistique de MAXIMUM : elle favorise le
  nul qui « a de la chance » sur un candidat.
- Biologie (tests directs §8.23, `immune_direct_tests.csv`) : ICGC N'EST
  PAS inversée biologiquement — PDCD1 rho −0,223 (top-12 d −0,85,
  p Welch 0,016), CTLA4 rho −0,243 (d −0,74, p 0,039), FOXP3 rho −0,196
  (d −0,70, p 0,032), CD8A rho −0,146 (d −0,45, p 0,22). Le froid
  tumoral est présent en ICGC comme ailleurs. L'inversion est donc une
  propriété de la MÉTRIQUE, pas du signal biologique — à expliquer,
  pas à « corriger » en changeant la biologie.

## 3. Hypothèses (critères écrits AVANT les analyses)

- **H1 — Fluke du nul graine 42.** Le nul graine 42 est un tirage
  ordinaire de la distribution des nuls à n=70 et 0,45 est dans sa plage
  courante. Critère de RETENUE : sur K=500 permutations répliquées du
  fichier ICGC (réplique exacte du scan, §5), P(maxsep_nul ≥ 0,45) ≥ 0,05
  ET médiane des maxsep nuls ≥ 0,30. Critère de REJET : P < 0,01
  (le nul 42 serait alors un tirage exceptionnel, autre explication
  requise).
- **H2 — Substitution de flux (IFNG→PRF1, CD19→MS4A1, ICGC seulement).**
  Les deux colonnes substituées portent l'inversion. Critère de
  RETENUE : la variante 10 gènes (sans IFNG/CD19, donc sans PRF1/MS4A1
  en ICGC — mêmes 10 gènes partout) donne d_ssep ICGC ≥ 0 en réplique
  ET en confirmation pipeline, alors que 12 gènes donnent −0,22.
  Critère de REJET : d_ssep 10 gènes reste ≤ −0,10 en réplique et en
  pipeline. Complément : décomposition par flux du score nul à son
  meilleur candidat (si PRF1 ou MS4A1 domine le 0,45, mécanisme nommé).
- **H3 — Petit n structurel.** À n≈70, la distribution des maxsep nuls
  est décalée vers le haut par rapport à n=145/178, et le réel ICGC
  reste dans sa bande nulle. Critère de RETENUE : médiane du maxsep nul
  répliqué (500 tirages, config fixe) ICGC ≈ GSE62452 > GSE71729 >
  TCGA, ET la courbe de scan réelle ICGC reste partout dans la bande
  interquartile nulle. Critère de REJET : pas de gradient avec n.
- **H4 — Composition / sous-type Bailey.** Les tumeurs du sous-type
  Immunogenic (Bailey 2016) se concentrent à une extrémité de l'axe
  KRAS des 70, ou quelques lignes à fardeau immunitaire extrême
  dominent le scan. Critère de RETENUE : test de Mann-Whitney du rang
  KRAS Immunogenic vs autres p < 0,05, OU ≥ 3 lignes avec |z| moyen
  multi-flux > 2,5 dont le retrait change le maxsep nul de > 0,10.
  Sinon REJET. (Test direct seulement, aucun run.)
- **H5 — Mécanisme : corrélation inter-flux préservée par le nul.**
  Le nul du projet permute les LIGNES entières (les 12 flux d'une
  tumeur voyagent ensemble) : la structure de corrélation entre flux
  (tumeurs « chaudes » vs « froides ») survit dans le nul, donc un
  tirage qui met plus de tumeurs chaudes d'un côté produit un grand
  |d| moyen. Critère de RETENUE : en réplique, les nuls à permutation
  par ligne donnent un maxsep médian nettement supérieur aux nuls à
  permutation indépendante par flux (chaque flux permuté séparément,
  corrélations brisées) — écart de médianes > 0,10 en ICGC. Ce test est
  DIAGNOSTIQUE : le nul du projet reste la permutation par ligne ; la
  variante indépendante ne le remplace pas, elle nomme le mécanisme.

## 4. Méthodes (ordre d'exécution)

### (a) Vérification des entrées (aucun run, script neuf)
`verify_icgc_immune_847.py`. Re-vérifie les SHA-256 des 8 CSV de flux
immunitaires + 4 fichiers d'axe contre PROVENANCE_immune_v6.md ; vérifie
que chaque nul est une permutation par ligne du réel (même multi-ensemble
de lignes, colonne step inchangée) ; statistiques par gène et par cohorte
(moyenne, écart-type, min, max, valeurs manquantes) ; statistiques de
l'axe KRAS (min/médiane/max, écart top-12 vs reste) ; fardeau immunitaire
par ligne (moyenne des z-scores des 12 flux) et lignes extrêmes ;
jointure sous-type Bailey (NMF, `data/icgc_pacaau_nmf.txt.gz`) aux 70
tumeurs et répartition des sous-types le long de l'axe KRAS
(Mann-Whitney + tertiles). Sorties : `icgc_immune_inversion_verify.json`
+ `.csv` + log.

### (b) Tests directs par cohorte (aucun run, script neuf)
`direct_tests_icgc_847.py`. Mêmes définitions que
`direct_tests_immune.py` : Spearman de chaque gène contre KRAS brut
(p bilatérale) ; top-12 KRAS-fort contre reste : d de Cohen + Welch.
Gènes focaux : GZMB, CD8A, IFNG (PRF1 en ICGC), PDCD1 — plus les 8
autres pour le tableau complet. Réel vs nul graine 42, 4 cohortes.
Ajout : distribution de permutation (200 tirages, graines 1000–1199)
du rho de Spearman et du d top-12 pour PDCD1, CD8A, GZMB, PRF1/IFNG
par cohorte — le nul direct, pas le nul pipeline. Sorties :
`icgc_immune_inversion_direct.csv` + `.json` + log.

### (c) Réplique exacte du scan (aucun run pipeline, script neuf)
`replica_scan_847.py`. Ré-implémente `_scan_critical_threshold_fast`
+ `evaluate_scan_quality` (max_separation) à partir du code v6.2 lu
(mode fast, contrôle = step, fenêtres w_size, tri par progression,
score = moyenne sur les flux de |d de Cohen| pré/post-seuil).
CALIBRATION D'ABORD : avec la best_config exacte de chacun des 8 runs
v6.2 existants (w_size, min_grp, n_candidates/resolution relus dans
leur master_results.json), la réplique doit reproduire max_separation
à ±0,001 — sinon la réplique est rejetée et le chantier s'arrête sur
la calibration. PUIS, sous configs fixes (config réelle et config
nulle de chaque cohorte) : 500 permutations par ligne par cohorte
(graines 2000–2499) → distribution du maxsep nul ; 500 permutations
indépendantes par flux (graines 3000–3499) → test H5 ; décomposition
par flux du score au meilleur candidat (réel et nul 42, ICGC) ;
variante 10 gènes (sans IFNG/CD19) réel + nul 42, 4 cohortes → H2 ;
courbe de scan réelle vs bande nulle (médiane, IQR) par candidat.
Sorties : `icgc_immune_inversion_replica.json` + `.csv` + log.

### (d) Lot de confirmation pipeline v6.2 (runs réels, seulement après (c))
Fichier v6.2 : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
SHA-256 `f07567c4…` (à re-vérifier avant chaque lancement, jamais modifié).
Mode fast, `--input <csv> --mode fast --output <dir>`, lancé depuis
`~/workspace/runs/pdac-v6/` via `systemd-run` (leçon AGENTS.md :
les lots longs survivent à la session) + journal des exit codes.
Construction des fichiers (script neuf `build_icgc_immune_847.py`,
même méthode que `build_fluxes_immune.py` : `default_rng(graine)`,
`permutation(n)`, lignes entières permutées, step inchangé) :
- 3 nuls ICGC immunitaire (graines 1, 2, 3) ;
- 2 nuls GSE62452 immunitaire (graines 1, 2) ;
- 2 nuls TCGA immunitaire (graines 1, 2) ;
- variante 10 gènes : ICGC réel + nul 42, TCGA réel + nul 42.
Soit 11 runs. Extraction : `extract_icgc_immune_847.py` (lecture des
`master_results.json` : maxsep, stabilité, S_sep, MC, Delta, L7a,
seuil). Critère de calibration : la réplique (§5c) doit prédire le
maxsep pipeline de ces 11 runs à ±0,05 (tolérance large car
l'optimiseur choisit sa propre config par run) ; sinon, la réplique
est déclarée non prédictive et le verdict repose sur les 11 runs
seuls. Sorties : `icgc_immune_inversion_confirm.json` + log
`runs_icgc_immune_847.log`.

## 5. Règles de verdict (écrites avant)

- Verdict « EXPLIQUÉ » si au moins une hypothèse est retenue par son
  critère ET confirmée par le lot (d) quand elle le requiert (H1/H2/H3).
  Plusieurs hypothèses peuvent être retenues ensemble ; les nommer
  toutes, avec leur part (ex. H1 quantitative, H5 mécanisme).
- Verdict « NON EXPLIQUÉ » honnête si aucune hypothèse ne passe son
  critère : le dire, avec les chiffres qui excluent chaque piste.
- Ne jamais présenter le nul graine 42 comme « le » nul : c'est UN
  tirage. Le verdict porte sur la distribution.
- Ne jamais importer de conclusions d'autres expériences (MTAP, test C,
  rotations) : seules les données et runs de ce chantier font foi ici.
- La biologie n'est pas en cause : les tests directs montrent le froid
  tumoral en ICGC comme ailleurs ; l'inversion est une propriété de la
  métrique max_separation (maximum sur candidats d'une moyenne de |d|).

## 6. Livrables

1. Ce protocole (SHA noté dans la section).
2. Section complète §8.47 :
   `~/workspace/runs/pdac-v6/section_8.47_icgc_immune_inversion.md`
   (verdict d'abord, chiffres, méthode, limites, provenance).
3. Scripts : `verify_icgc_immune_847.py`, `direct_tests_icgc_847.py`,
   `replica_scan_847.py`, `build_icgc_immune_847.py`,
   `extract_icgc_immune_847.py` (SHA notés dans la section).
4. Données/résultats : `icgc_immune_inversion_verify.json/.csv`,
   `icgc_immune_inversion_direct.csv/.json`,
   `icgc_immune_inversion_replica.json/.csv`,
   `icgc_immune_inversion_confirm.json`,
   fichiers de flux du lot (d) : `pdac_immune_icgc_fluxes_nul_s1.csv`,
   `..._s2.csv`, `..._s3.csv`, `pdac_immune_geo62452_fluxes_nul_s1.csv`,
   `..._s2.csv`, `pdac_immune_tcga_fluxes_nul_s1.csv`, `..._s2.csv`,
   `pdac_immune_icgc_fluxes_10g.csv`, `pdac_immune_icgc_fluxes_10g_nul.csv`,
   `pdac_immune_tcga_fluxes_10g.csv`, `pdac_immune_tcga_fluxes_10g_nul.csv`
   (SHA-256 notés), dossiers `results_fast_v62_847_*`, log
   `runs_icgc_immune_847.log`.

## 7. Provenance des entrées (déjà sur disque, rien re-téléchargé)

- Flux immunitaires : `pdac_immune_{tcga,geo71729,geo62452,icgc}_fluxes(_nul).csv`,
  SHA dans PROVENANCE_immune_v6.md (ICGC réel `10823879…`, nul `3393ecd6…`).
- Matrices sources : TCGA Firehose PAAD MD5 `b09569ce…` ; GSE71729 SHA
  `b2287893…` ; GSE62452 SHA `8f41d5b3…` ; ICGC Xena SHA `c2cb57af…`
  (Bailey et al. Nature 2016, doi:10.1038/nature16965).
- Pipeline v6.2 : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA `f07567c4…` (à re-vérifier ; §8.37).
- Livre blanc : `~/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md`,
  SHA `00f344b9…`, 3 104 lignes, §8.1–§8.45.
## 8. Limites connues d'avance

- La réplique ne reproduit pas l'optimiseur de configs du pipeline
  (12 itérations, choix par score MC) : elle fixe les configs. Le lot
  (d) est là pour calibrer cet écart.
- n=70 : toute distribution estimée sur 500 permutations reste une
  distribution du scan, pas une preuve biologique.
- ARN bulk sans correction de pureté (choix du bras §8.23) : la baisse
  des marqueurs T peut être un effet de composition ; ce chantier
  n'y touche pas.
- ICGC : IFNG et CD19 absents de la matrice (remplacés par PRF1 et
  MS4A1) — H2 teste exactement ce point ; aucune donnée IFNG/CD19
  ICGC n'existe sur le disque pour un test direct de remplacement.
- Sous-type Bailey : 96 échantillons NMF, jointure aux 70 par
  identifiant ICGC ; si la jointure est incomplète, H4 est déclarée
  non testable, pas rejetée.

## 9. ADDENDUM — correction de méthode avant tout résultat (19 nov. 2026)

La première version de la réplique (§4c) ré-implémentait le scan avec le
step brut comme contrôle et ÉCHOUAIT sa propre calibration : TCGA réel
0,3229 contre 0,5309 pipeline ; 4/8 exacts seulement. Cause trouvée par
lecture du code v6.2 : le scan n'utilise pas le step brut — il utilise
l'axe MC `progress_pct` (`_build_mc_progress_axis`, médiane de 200
trajectoires harmoniques, graine 42, à partir du rang du contrôle ;
`run_pipeline` l. 6817-6818). La réplique corrigée utilise les fonctions
du pipeline elles-mêmes (import en lecture seule, aucune modification) :
`_build_mc_progress_axis` + `scan_critical_threshold` (appel identique à
celui du worker Monte-Carlo : n_candidates, resolution=None, w_size,
min_grp) + `evaluate_scan_quality`. Calibration corrigée : 8/8 EXACTS
(écart 0,00e+00 sur maxsep, stabilité, seuil et courbe complète).
Aucun résultat de permutation n'a été produit avec la version fautive
(le script s'arrêtait à la calibration, comme prévu). Cet addendum ne
change ni la question, ni les hypothèses, ni les critères : il corrige
l'instrument de mesure avant usage. Fait notable pour la section : l'axe
de scan est un axe MC déformé (médiane de trajectoires), pas le step
brut — écart max à la linéarité mesuré par cohorte dans la réplique.
