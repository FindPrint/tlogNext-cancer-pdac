# §8.49 — Recomposition du score MC : proposition v6.3 REJETÉE

## Verdict d'abord

**La recomposition du score MC améliore nettement la séparation, mais pas
assez : la proposition v6.3 est REJETÉE.** Sur les rotations sans doublon,
MC_new sépare 31/48 paires au plancher 0,07 contre 12/48 pour l'ancien MC
(écart moyen +0,104 contre +0,015, ×6,9) — la porte A1 est franchie. Mais
sur les 8 paires principales, MC_new ne sépare que 4/8 (porte A2 : ≥6/8
exigés), et sur HP35, le contrôle positif, l'écart n'est que de +0,227
(porte A3 : ≥0,30 exigé). La variante avec resélection (S) ne change rien
(4/8, 31/48, HP35 +0,246). Le code v6.3, lui, fait ce qu'on lui demande
(porte A4 franchie : 10/10 runs, best_config et cascade identiques à
v6.2, MC_new en code = hors-ligne à 0,0 près) — mais un code correct ne
sauve pas un score qui échoue à ses propres critères. La v6.2 reste la
version de travail ; l'ancien MC reste le score affiché, avec ses défauts
connus (§8.49.3) — un score imparfait et documenté vaut mieux qu'un score
recomposé qui ne franchit pas ses propres critères.

Protocole gelé : `PROTOCOL_v6.3_mc.md` (19 nov. 2026). Critères d'adoption
écrits AVANT tout calcul de MC_new (§5 du protocole) ; aucune repondération,
aucun nouveau terme après avoir vu les chiffres. La décision finale
d'adoption revient à Zackary ; ce chantier propose ou rejette — il rejette.

## 8.49.1 — Les quatre portes, et leur sort

| Porte (PROTOCOL_v6.3_mc.md §5) | Exigé | Mesuré | Sort |
|---|---|---|---|
| A1 — rotations sans doublon (48 paires), MC_new sépare au plancher 0,07 | ≥ 24/48 | **31/48** (direction réel > nul, somme +5,008, moyenne +0,104) | FRANCHIE |
| A2 — paires principales, MC_new > 0,07 et positif | ≥ 6/8 > 0,07 et ≥ 7/8 positifs | **4/8** > 0,07 ; 7/8 positifs | **ÉCHEC** |
| A3 — HP35 (contrôle positif), écart MC_new | ≥ 0,30 | **+0,2271** (ancien +0,1950) | **ÉCHEC** |
| A4 — code v6.3 : best_config, cascade, S_sep identiques à v6.2 ; MC_new en code = hors-ligne | 10/10 | **10/10** (exit 0, best_config + cascade + S_sep identiques, MC_new code = hors-ligne à 0,0 près, gigue 0) | FRANCHIE |

Références ancien MC : rotations 12/48 (moyenne +0,0152) ; principales
1/8 au plancher 0,07 (7/8 positifs avec gigue 0) ; HP35 +0,1950.

## 8.49.2 — Définition exacte de l'ancien MC (lue dans le code v6.2)

Fichier `universal_v6.2.0_cohen.py`. Mode `fast` : 12 tirages MC
(`optimization_iterations = 12`, ligne 243 ; 100 est le défaut de la
fonction, ligne 3704). Par tirage (`_monte_carlo_worker`, lignes
3453–3490), `evaluate_scan_quality` (lignes 3314–3390) tire 5 métriques
de la courbe de scan (|d de Cohen| pré/post-seuil) :

- `max_separation` = score maximal de la courbe ;
- `s_norm = tanh(max_separation / 2.0)` (ligne 3336) ;
- `stability = 1 / (1 + écart-type des scores locaux)` (ligne 3344) ;
- `robustness = exp(-((FWHM − 10)²) / (2 × 5²))`, FWHM en % de la plage,
  idéal 10 % (lignes 3346–3364) ;
- `sharpness = tanh(max |dS/dx| local / 0.5)` (lignes 3365–3381).

Score composite du tirage (lignes 3480–3484, poids lignes 3727–3731) :

```
score_tirage = 0.3·s_norm + 0.3·stability + 0.2·robustness + 0.2·sharpness
```

(×0,8 si `w_size < n_pts // 10`). **MC (ancien) = score du meilleur
tirage** = `best_config.score`. Les 12 tirages sont conservés dans le
JSON (`threshold_optimization.all_results[i].metrics.*`, vérifié :
12 entrées sur HP35 et TCGA v4).

## 8.49.3 — Défauts mesurés de l'ancien MC

- **D1 — robustness morte.** `PROTOCOL_v6.2.md` §3.2, 16 JSON v6.1 :
  robustness ≤ 2×10⁻⁷ sur 14/16 (TCGA v4 : 3,37×10⁻⁴¹), contre 0,984 /
  0,899 sur HP35. La FWHM des scans PDAC est très loin de l'idéal
  arbitraire de 10 % : le poids 0,2 est perdu sur tout le PDAC.
- **D2 — stability saturée.** 0,978–0,997 sur le PDAC (quasi constante),
  0,869 / 0,983 sur HP35 (le réel y est MOINS stable que le nul). Le
  terme 0,3·stability ajoute ≈ 0,29–0,30 à chaque score, réel comme nul.
- **D3 — sharpness récompense le bruit.** Le nul est plus « sharp » que
  le réel sur GSE71729, l'immunitaire TCGA et PARP TCGA (phase 2).
- **D4 — s_norm sature là où vit le PDAC.** tanh(maxsep/2) : 0,15 → 0,075 ;
  0,46 → 0,226 ; 1,77 → 0,709. Les écarts PDAC sont comprimés à ~0,14
  en s_norm, puis à ~0,04 après le poids 0,3.
- **D5 — malédiction du vainqueur.** Le MC prend le MAX sur 12 tirages
  d'un composite bruité ; l'information de RÉCURRENCE des 12 tirages
  n'est jamais utilisée.

Conséquences déjà publiées : rotations 12/48 (§8.44) ; Test A MC inversé
(−0,0948) alors que max_separation est à +0,2501 (§8.34) ; série
MTAP-PRMT5 MC égal à 0,0004 près (§8.43) ; artefact pureté (§8.31,
V4R_PURITY) : ancien MC +0,1520 (réel > nul) alors que max_separation
est à −0,0670 (inversé) — les termes annexes renversent la séparation
elle-même. Précision : la mission citait « MC HP35 1,772 vs 0,121 » —
ce sont les valeurs de max_separation, pas du MC best_score (v6.2 : MC
0,6035 contre 0,4086 ; max_separation 1,7718 contre 0,1206).

## 8.49.4 — Le MC recomposé proposé (formule gelée)

```
MC_new = 0.60 · sep + 0.25 · stability + 0.15 · recur
sep    = max_separation / (1 + max_separation)
recur  = médiane_i(max_separation_i) / max_separation_best   (12 tirages)
```

`max_separation` et `stability` sont ceux du best_config ANCIEN
(sélection inchangée) ; `recur` est borné à [0, 1], vaut 0 si best = 0
ou si `all_results` est absent. Justification (principe, pas ajustement) :
`sep` a le même ordre que max_separation (aucun renversement possible)
avec un ancrage non arbitraire — sep = 0,5 quand |d de Cohen| = 1 — et
sature moins que tanh(·/2) dans la plage PDAC (0,17 → 0,145 ; 0,46 →
0,315 ; 1,77 → 0,639). `stability` est gardée à poids réduit comme
garde-fou. `recur` est la récurrence que « robustesse » prétendait
mesurer, sans paramètre : une vraie rupture revient quand les paramètres
de scan changent, un pic de chance est isolé à un tirage. Poids fixés
par principe : séparation dominante (0,60), récurrence minoritaire
(0,15) car terme nouveau et non prouvé. **Supprimés : `robustness` (D1)
et `sharpness` (D3).** Variante R (primaire) : rescore seul — seuil,
cascade, S_sep, Delta, L7a inchangés par construction. Variante S
(exploratoire, non candidate) : resélection du tirage par
0,60·sep_i + 0,25·stab_i, puis MC_new_S avec recur du tirage sélectionné.

## 8.49.5 — Validation hors-ligne (60 paires, JSON v6.2 existants, aucun run)

Extracteur `extract_mc63.py` : 60/60 paires lues, 0 manquante, 0 version
non attendue ; ancien MC relu sans écart vs §8.44 et phase 2 v6.2
(tol. 1e-9). Gigue_eff = max(gigue mesurée, 0,07) = 0,07 (même plancher
que S_sep, `PROTOCOL_v6.2.md` §3.4).

### Paires principales (V1) — MC_new 4/8, ancien 1/8, maxsep 6/8

| Paire | MC ancien R/N (écart) | MC_new R/N (écart) | MC_new_S (écart) | maxsep (écart) | recur R/N |
|---|---|---|---|---|---|
| HP35 | 0,6035 / 0,4086 (+0,1950) | 0,6687 / 0,4416 (**+0,2271**) | (+0,2459) | +1,6512 | 0,453 / 0,876 |
| TCGA v4 | 0,3720 / 0,3268 (+0,0453) | 0,5331 / 0,4266 (**+0,1065**) | (+0,1065) | +0,2928 | 0,650 / 0,605 |
| GSE71729 | 0,3393 / 0,3335 (+0,0059) | 0,4885 / 0,4676 (+0,0209) | (+0,0168) | +0,0402 | 0,775 / 0,745 |
| GSE62452 | 0,3454 / 0,3485 (−0,0031) | 0,4981 / 0,5394 (−0,0414) | (−0,0395) | −0,0036 | 0,737 / 0,985 |
| ICGC | 0,3600 / 0,3450 (+0,0150) | 0,5373 / 0,5137 (+0,0236) | (+0,0236) | +0,0970 | 0,775 / 0,829 |
| Immunitaire TCGA | 0,3785 / 0,3240 (+0,0545) | 0,5519 / 0,4571 (**+0,0949**) | (+0,0949) | +0,3675 | 0,640 / 0,849 |
| PARP TCGA | 0,3555 / 0,3311 (+0,0244) | 0,5356 / 0,4502 (**+0,0854**) | (+0,0854) | +0,1688 | 0,834 / 0,675 |
| DepMap | 0,3615 / 0,3499 (+0,0115) | 0,5596 / 0,5204 (+0,0392) | (+0,0375) | +0,1904 | 0,871 / 1,000 |

MC_new passe le plancher sur HP35, TCGA v4, immunitaire et PARP ; il
échoue sur GSE71729 (+0,0209), ICGC (+0,0236), DepMap (+0,0392) et
reste négatif sur GSE62452 (−0,0414, pire que l'ancien −0,0031).
Positifs : 7/8 (seul GSE62452 est négatif).

### Rotations sans doublon (V2) — MC_new 31/48, ancien 12/48, maxsep 37/48

| Famille | MC_new > 0,07 | Positifs | Écart moyen MC_new | Écart moyen ancien MC |
|---|---|---|---|---|
| IMMROT (n=178) | **12/12** | 12/12 | +0,187 | +0,037 |
| V4ROT (n=178) | **10/12** | 11/12 | +0,106 | +0,025 |
| PARPROT (n=178) | **8/12** | 11/12 | +0,103 | −0,010 |
| DEPMAPROT (n=45) | **1/12** | 7/12 | +0,020 | +0,009 |
| **Toutes** | **31/48** | 41/48 | **+0,104** | **+0,015** |

Échecs MC_new (17 paires, écart ≤ 0,07) : les 11 DEPMAPROT restantes
(AC02, CCND1, CFLAR, CRKL, DOCK5, MYC, MYH9, RAB10, RAB6A, SCAP, UROD),
PARPROT ATR (+0,0696, à 0,0004 du plancher), PARP1, PARP2, XRCC1,
V4ROT CR2 et GSTM1. Le gain est réel mais concentré sur les grandes
cohortes (n=178) ; sur les petites cohortes DepMap (n=45), MC_new ne
sépare presque rien (1/12) — comme maxsep y sépare moins aussi, mais
moins mal. Table complète par paire : `v63_mc_table.csv` / `.json`.

### Contrôles descriptifs (V3–V5, ne décident pas de l'adoption)

| Paire | MC ancien (écart) | MC_new R/N (écart) | maxsep (écart) | Lecture |
|---|---|---|---|---|
| Test A (prolifération) | −0,0948 | 0,5056 / 0,4389 (**+0,0666**) | +0,2501 | Suit maxsep, comme prévu par construction ; ne ressuscite pas Test A (verdict NON du §8.34 portait sur la chaîne et MC/Delta) |
| MTAP série PRMT5-flux (§8.43) | +0,0004 | 0,4937 / 0,4983 (−0,0046) | −0,1036 | Reste ≈ 0 : cohérent avec le verdict NON du §8.43 |
| MTAP série (§8.31) | −0,1642 | 0,5269 / 0,4540 (**+0,0729**) | +0,1957 | Suit maxsep ; l'ancien MC était fortement inversé ici |
| V4R_PURITY (artefact §8.31) | +0,1520 | 0,4438 / 0,4791 (**−0,0353**) | −0,0670 | **Artefact CORRIGÉ** : MC_new reprend le sens de maxsep, l'ancien MC « séparait » à tort |

### Variante S (resélection) — ne sauve rien

MC_new_S : principales 4/8, rotations 31/48, HP35 +0,2459 — les mêmes
verdicts que R. |d_S − d_R| ≤ 0,0293 sur les 56 paires jugées (max :
IMMROT_IFNG +0,0293) ; sur 4 des 8 paires principales, la resélection
choisit le même tirage que l'ancien composite (écart 0,0000 : TCGA v4,
ICGC, immunitaire TCGA, PARP TCGA). La
sélection n'était pas le goulot : changer le tirage gagnant ne change
presque rien, parce que le composite ancien et le nouveau classent les
tirages presque pareil. La piste « resélectionner » est fermée par ce
résultat, pas reportée.

## 8.49.6 — Pourquoi ça ne suffit pas : la récurrence punit le vrai pic

Décomposition de l'écart HP35 (+0,2271) : terme de séparation
0,60×(0,639 − 0,108) = **+0,319** ; terme de stabilité
0,25×(0,869 − 0,983) = **−0,029** (le réel HP35 est moins stable que
son nul, D2) ; terme de récurrence 0,15×(0,453 − 0,876) = **−0,063**.
La récurrence, telle que définie (médiane/best), punit exactement le
cas qu'elle devait récompenser : sur HP35 réel, le meilleur tirage est
un pic isolé (maxsep 1,77, médiane des tirages 0,80, recur 0,453),
tandis que le nul est plat (maxsep 0,12, médiane 0,11, recur 0,876).
Sur les 8 paires principales, recur moyen réel 0,717 contre nul 0,820 :
**le nul est en moyenne PLUS récurrent que le réel**. Sur les rotations,
recur est à peine favorable (réel 0,755 contre nul 0,719). Le terme
nouveau ne discrimine pas ; il dilue. Et MC_new reste partout en
retrait de max_separation seul (rotations 31/48 contre 37/48 ;
principales 4/8 contre 6/8) : les deux termes annexes (stability,
recur) coûtent plus qu'ils ne rapportent. L'amélioration 12 → 31/48
vient presque entièrement de `sep` (moins saturante que `s_norm`) et
de la suppression de `robustness`/`sharpness` — pas de la récurrence.

Leçon : un score composite ne sépare pas mieux que sa meilleure
composante quand les autres composantes sont saturées ou
anti-discriminantes. MC_new n'est pas un mauvais score — il est
meilleur que l'ancien sur tous les ensembles — mais il ne franchit
pas la barre qu'il s'était fixée, et il reste inférieur à
max_separation, qui existe déjà comme indicateur (§8.37–§8.38, S_sep).
Adopter MC_new ajouterait un second indicateur plus faible que celui
qu'on a déjà, sans rien apporter que max_separation ne donne.

## 8.49.7 — Code v6.3 et validation en code (porte A4 : FRANCHIE)

Construction : copie exacte de la v6.2 →
`universal_v6.3.0_cohen.py`, SHA-256
`552e735910a1fac183ad2ce5713ffa2888e9214c764b103707eeef1787044ffb`
(script `build_v6.3.py`, SHA
`96165bcbba08a0f16c7f51be274653ee71d8fdc41c77e890d26adfd248c31fe2`) ;
3 remplacements seuls (version C1, fonction pure `mc_recomposed_score`
C2, appel en lecture seule C3), 3 blocs différants vérifiés par diff,
`py_compile` exit 0. La fonction est appelée APRÈS la sélection du
best_config et n'écrit que les champs nouveaux `mc_recomposed`
(`best_config` et `threshold_optimization`) ; `score`, `threshold` et
cascade ne sont jamais touchés.

Validation en code (§7.2 du protocole) : HP35, TCGA v4, rotations
CEACAM5 (cas fort) et GSTM1 (cas négatif), Test A — 10 runs, mode fast,
graine 42, dossiers `results_fast_v63_*`, journal `runs_v63_mc.log`
(lanceur `run_v63_mc.sh`, manifeste `manifest_v63_mc.txt`).
Incident consigné : le premier lancement (unité systemd `v63-mc-lot`,
21h36 UTC) a été tué par un redémarrage du runtime vers 21h41, avant
toute écriture (dossier HP35 vide, aucun run perdu, aucune sortie
partielle) ; relance reprenable (`v63-mc-lot2`, 21h41 UTC), terminée
23h01:27 UTC. **10/10 exit 0, 0 échec.**

Vérification (`extract_v63_check.py` → `v63_mc_check.json`, SHA
`eb17ddf0d9cb44c8844c7a0a35a411a027a73108e15872c0d9cd99166aae7009`) :
MC_new calculé en code = MC_new hors-ligne sur 10/10, écart 0,0
exact (tol. 1e-9) — HP35 0,6687 / 0,4416 ; TCGA v4 0,5331 / 0,4266 ;
CEACAM5 0,6080 / 0,4364 ; GSTM1 0,4513 / 0,4747 ; Test A 0,5056 /
0,4389. best_config (score ancien, seuil, métriques), cascade
T_-2…T_+2 et S_sep IDENTIQUES aux JSON v6.2 sur 10/10 (tol. 0).
Gigue MC_new mesurée (code vs hors-ligne) : **0,00**. Versions :
v6.3.0-L7aL7b-CohenD-short sur 10/10 JSON v6.3. SHA revérifiés après
le lot : v6.2 `f07567c4…c3abf`, v6.1 `2af5e5ce…c1c9`, v6
`bb8bbdba…c0773` — inchangés. **Porte A4 franchie.** Le rejet de la
proposition ne vient donc pas du code : il vient du score lui-même
(A2, A3).

## 8.49.8 — Limites et ce qui reste

- La validation hors-ligne réutilise les JSON v6.2 : elle ne teste que
  la RELECTURE, pas une nouvelle mesure. La porte A4 (§8.49.7) est le
  seul contrôle en code, sur 10 runs.
- Le plancher 0,07 est une convention du projet (même que S_sep), pas
  une propriété statistique de MC_new ; avec une gigue 0, MC_new
  séparerait 41/48 rotations (positifs) et 7/8 principales — le verdict
  de rejet tient au plancher gelé, et il est dit tel quel.
- DEPMAPROT (n=45) reste le point faible commun à MC ancien, MC_new et
  maxsep : les petites cohortes séparent mal, quel que soit le score.
- Piste NON testée (pour un chantier ultérieur, pas une proposition
  ici) : une récurrence définie autrement — par exemple la concentration
  des SEUILS des tirages autour du seuil gagnant, plutôt que le rapport
  des maxsep — ou la suppression pure et simple de `stability` du
  score, puisque S_sep montre déjà que la stabilité ne porte rien sur
  le PDAC. Aucune de ces pistes n'a été calculée dans ce chantier : les
  ajouter après le rejet serait exactement la retouche interdite par le
  protocole gelé.
- Rien de clinique : l'étude porte sur l'instrument.

## 8.49.9 — Provenance

- Protocole gelé : `PROTOCOL_v6.3_mc.md`, SHA
  `acc74e943d60757e90b8800a0caac178b6b38222c94d197895615d2d3a5cea0b`.
- Extracteur hors-ligne : `extract_mc63.py`, SHA
  `9cb813039d19f3892ad2a503adee9c2419ffbf9a6e3809f59dbb58c236d61206` ;
  sorties `v63_mc_table.csv` / `v63_mc_table.json` / `v63_mc_table.md`.
- Construction : `build_v6.3.py` ; v6.3 SHA
  `552e735910a1fac183ad2ce5713ffa2888e9214c764b103707eeef1787044ffb`.
- Validation code : `run_v63_mc.sh`, manifeste `manifest_v63_mc.txt`,
  journal `runs_v63_mc.log`, vérification `extract_v63_check.py` →
  `v63_mc_check.json`.
- Données : JSON v6.2 existants (lots §8.44, phase 2, §8.43, Test A) ;
  CSV inchangés, SHA déjà publiés dans `PROVENANCE_rotations_dedup_844.md`,
  `PROVENANCE_tcga_v4.md`, `PROVENANCE_mtap_prmt5_flux.md`,
  `PROVENANCE_testA_proliferation.md`. Nuls = lignes permutées, graine
  42 — échantillons hypothétiques, pas des mesures. Séries réelles =
  résidus d'expression génique ou de dépendance CRISPR (mesures
  instrumentales transformées). Aucune valeur inventée ; aucune valeur
  recopiée à la main (tables générées depuis `v63_mc_table.json`).
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`), v6.1 (`2af5e5ce…c1c9`),
  v6 (`bb8bbdba…c0773`).
