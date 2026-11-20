# §8.52 — Recomposition du MC par la récurrence-concentration : proposition v6.4 REJETÉE

## Verdict d'abord

**La recomposition du MC par la concentration des seuils améliore
fortement le contrôle positif mais ne franchit pas ses propres critères :
la proposition v6.4 est REJETÉE.** Sur les rotations sans doublon, MC2
sépare 28/48 paires au plancher 0,07 contre 12/48 pour l'ancien MC et
31/48 pour la v6.3 (porte A1 franchie, ≥24/48). Sur HP35, l'écart bondit
à +0,5529 contre +0,1950 (ancien) et +0,2271 (v6.3) — porte A3 franchie
(≥0,30), et de loin. Mais sur les 8 paires principales, MC2 ne sépare
que 4/8 au plancher (porte A2 : ≥6/8 exigés), et n'est positif que sur
5/8 (≥7/8 exigés) : **la porte A2 échoue sur ses deux sous-critères**.
Le code v6.4, lui, fait ce qu'on lui demande (porte A4 franchie : 10/10
runs, best_config et cascade identiques à v6.2, MC2 en code = hors-ligne
à 0,0 près) — mais un code correct ne sauve pas un score qui échoue à
ses propres critères. La v6.2 reste la version de travail ; l'ancien MC
reste le score affiché, avec ses défauts connus (§8.49.3). La piste
« récurrence par concentration des seuils » (§8.49.8) est testée et
fermée telle que définie ici ; la piste « suppression de stability »
est testée isolément par la variante E et ne suffit pas non plus (4/8
aux principales).

Protocole gelé : `PROTOCOL_v6.4_mc.md` (19 nov. 2026). Critères
d'adoption écrits AVANT tout calcul de MC2 (§5 du protocole) ; aucune
repondération, aucun nouveau terme après avoir vu les chiffres. La
décision finale d'adoption revient à Zackary ; ce chantier propose ou
rejette — il rejette.

## 8.52.1 — Les quatre portes, et leur sort

| Porte (PROTOCOL_v6.4_mc.md §5) | Exigé | Mesuré | Sort |
|---|---|---|---|
| A1 — rotations sans doublon (48 paires), MC2 sépare au plancher 0,07 | ≥ 24/48 | **28/48** (direction réel > nul, somme +4,744, moyenne +0,099) | FRANCHIE |
| A2 — paires principales, MC2 > 0,07 et positif | ≥ 6/8 > 0,07 et ≥ 7/8 positifs | **4/8** > 0,07 ; **5/8** positifs | **ÉCHEC** |
| A3 — HP35 (contrôle positif), écart MC2 | ≥ 0,30 | **+0,5529** (ancien +0,1950 ; v6.3 +0,2271) | FRANCHIE |
| A4 — code v6.4 : best_config, cascade, S_sep identiques à v6.2 ; MC2 en code = hors-ligne | 10/10 | **10/10** (exit 0, best_config + cascade + S_sep identiques, MC2 code = hors-ligne à 0,0 près, gigue 0) | FRANCHIE |

Références : ancien MC — rotations 12/48 (moyenne +0,0152),
principales 1/8 au plancher 0,07 (7/8 positifs), HP35 +0,1950 ;
v6.3 MC_new — rotations 31/48, principales 4/8 (7/8 positifs),
HP35 +0,2271.

## 8.52.2 — Définition exacte du MC2 proposé (formule gelée)

```
MC2    = 0.70 · sep + 0.30 · conc
sep    = max_separation / (1 + max_separation)     (best_config ANCIEN)
conc   = 1 − médiane_i(|θ_i − θ*|) / (θ_max − θ_min)
```

`θ_i` = seuils des 12 tirages de `all_results` (champ `threshold`,
vérifié présent avant le gel) ; `θ*` = seuil du best_config (l'un des
tirages) ; `θ_max`, `θ_min` = max et min des `θ_i`. Règles de bord
gelées : `conc = 1,0` si l'étendue est nulle (seuils tous identiques) ;
`conc = 0` si moins de 2 seuils lisibles (aucun cas rencontré : 12/12
seuils lisibles sur les 120 runs lus) ; `conc` bornée à [0, 1] par
construction. Poids fixés par principe avant tout calcul : la part
0,25 de `stability` supprimée est réallouée +0,10 à `sep` et +0,15 à
`conc` — le terme sous test reçoit un poids réel, sinon un écart de
concentration de 0,5 ne déplacerait MC2 que de 0,075, tout juste le
plancher.

**Pourquoi cette définition (rappel du protocole §2) :** la récurrence
médiane/best de la v6.3 mesurait si les autres tirages montent aussi
haut que le meilleur — elle punit un pic vrai mais isolé en hauteur
(HP35 recur réel 0,453 contre nul 0,876). La concentration mesure si
les tirages placent leur rupture AU MÊME ENDROIT, quelle que soit leur
hauteur : une vraie rupture a une position, un pic de chance n'en a
pas. **Supprimés :** `robustness` (D1), `sharpness` (D3) comme en
v6.3, `stability` (D2 : quasi constante sur le PDAC, 0,978–0,997, et
anti-discriminante sur HP35, réel 0,869 < nul 0,983) et `recur`
médiane/best (cause d'échec de la v6.3, §8.49.6). La sélection du
best_config est inchangée : MC2 est une relecture, comme S_sep et
MC_new avant lui.

Variante E (exploratoire, NON candidate) : `MC_E = 0.80·sep +
0.20·recur`, la v6.3 renormalisée sans stability (rapports sep:recur
conservés) — elle isole l'effet de la suppression de stability seule.

## 8.52.3 — Validation hors-ligne (60 paires, JSON v6.2 existants, aucun run)

Extracteur `extract_mc64.py` : 60/60 paires lues, 0 manquante, 0 version
non attendue ; ancien MC relu sans écart vs §8.44 et phase 2 v6.2
(tol. 1e-9) ; MC_new v6.3 recalculé depuis les mêmes JSON et vérifié
égal à `v63_mc_table.json` (tol. 1e-9) — garde-fou de régression du
lecteur. Gigue_eff = max(gigue mesurée, 0,07) = 0,07 (même plancher que
S_sep et que la v6.3).

### Paires principales (V1) — MC2 4/8, MC_E 4/8, sep seul 5/8, maxsep 6/8

| Paire | MC ancien R/N (écart) | MC2 R/N (écart) | MC_E (écart) | sep (écart) | conc R/N | maxsep (écart) |
|---|---|---|---|---|---|---|
| HP35 | 0,6035 / 0,4086 (+0,1950) | 0,7248 / 0,1719 (**+0,5529**) | (+0,3408) | +0,5316 | 0,924 / 0,322 | +1,6512 |
| TCGA v4 | 0,3720 / 0,3268 (+0,0453) | 0,4702 / 0,1821 (**+0,2881**) | (+0,1459) | +0,1712 | 0,830 / 0,269 | +0,2928 |
| GSE71729 | 0,3393 / 0,3335 (+0,0059) | 0,3803 / 0,4003 (−0,0200) | (+0,0271) | +0,0262 | 0,787 / 0,915 | +0,0402 |
| GSE62452 | 0,3454 / 0,3485 (−0,0031) | 0,3568 / 0,3845 (−0,0277) | (−0,0512) | −0,0021 | 0,637 / 0,725 | −0,0036 |
| ICGC | 0,3600 / 0,3450 (+0,0150) | 0,3638 / 0,2572 (**+0,1066**) | (+0,0313) | +0,0525 | 0,537 / 0,304 | +0,0970 |
| Immunitaire TCGA | 0,3785 / 0,3240 (+0,0545) | 0,4112 / 0,3103 (**+0,1009**) | (+0,1233) | +0,2063 | 0,562 / 0,707 | +0,3675 |
| PARP TCGA | 0,3555 / 0,3311 (+0,0244) | 0,4098 / 0,3499 (+0,0600) | (+0,1142) | +0,1029 | 0,738 / 0,779 | +0,1688 |
| DepMap | 0,3615 / 0,3499 (+0,0115) | 0,3535 / 0,4083 (−0,0548) | (+0,0584) | +0,1052 | 0,461 / 0,890 | +0,1904 |

MC2 passe le plancher sur HP35, TCGA v4, ICGC et immunitaire ; il
échoue de peu sur PARP (+0,0600, à 0,0100 du plancher) et reste négatif
sur GSE71729 (−0,0200), GSE62452 (−0,0277) et DepMap (−0,0548).
Positifs : 5/8 — les deux sous-critères de A2 échouent. La somme des
écarts MC2 (+1,0059) dépasse pourtant celle de la v6.3 (+0,5562) : le
gain est réel mais concentré sur HP35 (+0,5529) et TCGA v4 (+0,2881),
qui portent à eux deux 84 % de la somme.

### Rotations sans doublon (V2) — MC2 28/48, MC_E 34/48, v6.3 31/48, sep seul 35/48

| Famille | MC2 > 0,07 | Positifs | Écart moyen MC2 | Écart moyen MC_E | Écart moyen sep seul |
|---|---|---|---|---|---|
| IMMROT (n=178) | **12/12** | 12/12 | +0,197 | +0,250 | +0,301 |
| V4ROT (n=178) | **7/12** | 9/12 | +0,099 | +0,142 | +0,153 |
| PARPROT (n=178) | **7/12** | 11/12 | +0,097 | +0,137 | +0,162 |
| DEPMAPROT (n=45) | **2/12** | 6/12 | +0,003 | +0,029 | +0,045 |
| **Toutes** | **28/48** | 38/48 | **+0,099** | **+0,139** | **+0,165** |

Échecs MC2 (20 paires, écart ≤ 0,07) : les 10 DEPMAPROT restantes,
PARPROT ATM (+0,0359), ATR (+0,0461), BRCA2 (+0,0081), PARP1
(−0,0502), RAD51 (+0,0195), V4ROT CLCA1 (+0,0239), CR2 (−0,0063),
GSTM1 (−0,1613), KRT20 (+0,0153), MUC16 (−0,0648). MC2 est partout en
retrait de MC_E (34/48) et de `sep` seul (35/48) sur les rotations —
la concentration coûte plus qu'elle ne rapporte hors des grandes
cohortes, et MC2 (28/48) fait moins bien que la v6.3 (31/48) sur cet
ensemble. Table complète par paire : `v64_mc_table.csv` / `.json`.

### Contrôles descriptifs (V3–V5, ne décident pas de l'adoption)

| Paire | MC ancien (écart) | MC2 R/N (écart) | MC_E (écart) | sep (écart) | maxsep (écart) | Lecture |
|---|---|---|---|---|---|---|
| Test A (prolifération) | −0,0948 | 0,3723 / 0,2267 (**+0,1456**) | +0,0917 | +0,1567 | +0,2501 | Suit maxsep, comme prévu ; ne ressuscite pas Test A (verdict NON du §8.34 portait sur la chaîne et MC/Delta) |
| MTAP série PRMT5-flux (§8.43) | +0,0004 | 0,3277 / 0,4131 (**−0,0854**) | −0,0115 | −0,0671 | −0,1036 | Reste négatif, cohérent avec le verdict NON du §8.43 ; conc R 0,717 contre N 0,845 — le nul est plus concentré |
| MTAP série (§8.31) | −0,1642 | 0,4260 / 0,2258 (**+0,2002**) | +0,0928 | +0,1278 | +0,1957 | Suit maxsep ; l'ancien MC était fortement inversé ici |
| V4R_PURITY (artefact §8.31) | +0,1520 | 0,1966 / 0,3163 (**−0,1197**) | −0,0446 | −0,0483 | −0,0670 | **Artefact CORRIGÉ**, plus nettement qu'en v6.3 (−0,0353) : MC2 reprend le sens de maxsep |

## 8.52.4 — Pourquoi ça ne suffit pas : la concentration récompense le nul

Décomposition de l'écart HP35 (+0,5529) : terme de séparation
0,70×(0,639 − 0,108) = **+0,372** ; terme de concentration
0,30×(0,924 − 0,322) = **+0,181**. Sur HP35, l'hypothèse fonctionne
exactement comme prévu : le vrai pic est haut ET ses seuils se
concentrent (0,924), le nul est plat ET ses seuils se dispersent
(0,322). La suppression de stability aide aussi : MC_E (qui garde
`recur` mais supprime `stability`) monte à +0,3408 sur HP35 contre
+0,2271 en v6.3 — le terme de stabilité coûtait bien −0,029, et le
terme `recur` −0,085 dans MC_E.

Mais l'hypothèse ne généralise pas. Sur les 8 paires principales,
`conc` moyen réel 0,685 contre nul 0,614 — à peine favorable. Sur les
48 rotations, `conc` moyen réel **0,568 contre nul 0,624 : le nul est
en moyenne PLUS concentré que le réel**. Les cas les plus parlants :
DepMap, conc réel 0,461 contre nul 0,890 (écart −0,428 — le pire
déficit de concentration du lot, qui renverse à lui seul l'écart de
séparation +0,105 en MC2 −0,0548) ; GSE71729, conc 0,787 contre 0,915 ;
PARPROT BRCA2, 0,087 contre 0,563 ; PARPROT RAD51, 0,085 contre 0,664 ;
V4ROT GSTM1, 0,201 contre 0,518. Le mécanisme est lisible : sur un
scan nul plat, l'argmax retombe sans cesse sur le même artefact de
grille — les seuils des tirages se concentrent parce qu'il n'y a rien
à trouver, pas parce qu'une rupture revient. Sur un scan réel, les
tirages secondaires explorent des seuils genuinely différents : la
dispersion des seuils y mesure la richesse du scan, pas son bruit.
La concentration, telle que définie ici, confond « les tirages sont
d'accord » et « les tirages n'ont rien à départager ».

Attribution (comparaison C vs E vs v6.3) : la suppression de stability
seule améliore les rotations (31/48 → 34/48 pour MC_E) et HP35
(+0,2271 → +0,3408), mais MC_E échoue lui aussi à A2 (4/8, 7/8
positifs — le sous-critère des positifs est franchi exactement, pas
celui du plancher). La concentration, elle, coûte sur les rotations :
MC2 28/48 contre MC_E 34/48, alors qu'elle rapporte sur HP35 et
TCGA v4. Et `sep` seul (35/48, 5/8) reste devant les deux variantes
sur les rotations : tout terme annexe essayé jusqu'ici — `stability`,
`recur`, `conc` — coûte plus qu'il ne rapporte hors du contrôle
positif. MC2 reste partout en retrait de max_separation seul
(rotations 28/48 contre 37/48 ; principales 4/8 contre 6/8), qui
existe déjà comme indicateur (§8.37–§8.38, S_sep). Adopter MC2
ajouterait un second indicateur plus faible que celui qu'on a déjà,
sans rien apporter que max_separation ne donne — la même conclusion
qu'au §8.49.6, avec un score différent.

Leçon : un terme qui sépare sur le contrôle positif ne sépare pas
forcément sur le PDAC — HP35 est un pic isolé dans un bruit faible,
le PDAC est un paysage de petits écarts. La concentration des seuils
est un bon détecteur de pic isolé ; ce n'est pas un bon détecteur de
rupture faible. La piste est fermée telle que définie ici : la
retoucher (autre résumé que la médiane, autre normalisation que
l'étendue) serait exactement la retouche interdite par le protocole
gelé, et exigerait un nouveau protocole avec ses propres barres.

## 8.52.5 — Code v6.4 et validation en code (porte A4 : FRANCHIE)

Construction : copie exacte de la v6.2 →
`universal_v6.4.0_cohen.py`, SHA-256
`9ed728da7168925f629258e671971d3e2724c35c812a60d9bd95f5fd8199ea3d`
(script `build_v6.4.py`, SHA
`684ff8a01a77e6196181d4bcf0ab3943f14bd71c83a23853c01989885be9b3b0`) ;
3 remplacements seuls (version C1, fonction pure `mc_v64_score` C2,
appel en lecture seule C3), 3 blocs différants vérifiés par diff,
`py_compile` exit 0. La fonction est appelée APRÈS la sélection du
best_config et n'écrit que les champs nouveaux `mc_v64`
(`best_config` et `threshold_optimization`, distincts de
`mc_recomposed` de la v6.3 pour ne jamais confondre les deux scores) ;
`score`, `threshold` et cascade ne sont jamais touchés. Jamais
construite depuis la v6.3 rejetée.

Validation en code (§7.2 du protocole) : HP35, TCGA v4, rotations
CEACAM5 (cas fort) et GSTM1 (cas négatif), Test A — 10 runs, mode fast,
graine 42, dossiers `results_fast_v64_*`, journal `runs_v64_mc.log`
(lanceur `run_v64_mc.sh`, manifeste `manifest_v64_mc.txt`).
Incident consigné : le premier lancement (unité systemd `v64-mc-lot`,
23h31 UTC) a été tué par un redémarrage du runtime vers 23h43, avant
toute écriture complète (dossier HP35 partiel, aucun
`master_results.json`, aucun run perdu, aucune sortie partielle
exploitable) ; relance reprenable (`v64-mc-lot2`, 23h44 UTC), terminée
01h19:41 UTC le 20 nov. **10/10 exit 0, 0 échec.**

Vérification (`extract_v64_check.py` → `v64_mc_check.json`, SHA
`5b8263584fb434cf1f3e582de6dd42874cfdc36004097aa5125b638e28bf3d5d`) :
MC2 calculé en code = MC2 hors-ligne sur 10/10, écart 0,0 exact
(tol. 1e-9) — HP35 0,7248 / 0,1719 ; TCGA v4 0,4702 / 0,1821 ;
CEACAM5 0,4584 / 0,1739 ; GSTM1 0,1402 / 0,3015 ; Test A 0,3723 /
0,2267. best_config (score ancien, seuil, métriques), cascade
T_-2…T_+2 et S_sep IDENTIQUES aux JSON v6.2 sur 10/10 (tol. 0).
Gigue MC2 mesurée (code vs hors-ligne) : **0,00**. Versions :
v6.4.0-L7aL7b-CohenD-short sur 10/10 JSON v6.4. SHA revérifiés après
le lot : v6.2 `f07567c4…c3abf`, v6.1 `2af5e5ce…c1c9`, v6
`bb8bbdba…c0773`, v6.3 `552e7359…44ffb` — inchangés. **Porte A4
franchie.** Le rejet de la proposition ne vient donc pas du code : il
vient du score lui-même (A2).

## 8.52.6 — Limites et ce qui reste

- La validation hors-ligne réutilise les JSON v6.2 : elle ne teste que
  la RELECTURE, pas une nouvelle mesure. La porte A4 (§8.52.5) est le
  seul contrôle en code, sur 10 runs.
- Le plancher 0,07 est une convention du projet (même que S_sep), pas
  une propriété statistique de MC2 ; avec une gigue 0, MC2 séparerait
  38/48 rotations (positifs) et 5/8 principales — le verdict de rejet
  tient au plancher gelé, et il est dit tel quel. À noter : même sans
  plancher, A2 échouerait (5/8 positifs < 7/8 exigés) — le rejet ne
  tient pas à 0,07 seul.
- DEPMAPROT (n=45) reste le point faible commun à MC ancien, MC_new,
  MC2, MC_E, `sep` seul et maxsep : les petites cohortes séparent mal,
  quel que soit le score.
- La variante E (v6.3 sans stability) passe A1 (34/48) et A3 (+0,3408)
  mais échoue à A2 (4/8) : elle ne peut pas être adoptée dans ce
  chantier (non candidate, et elle garde le terme `recur` condamné au
  §8.49.6). Si un chantier ultérieur veut la proposer, il lui faut son
  propre protocole gelé et ses propres barres — pas une adoption par
  ricochet.
- Ce qui reste, après deux recompositions rejetées (v6.3, v6.4) : les
  termes annexes essayés jusqu'ici saturent, punissent le vrai pic ou
  récompensent le nul. La question ouverte n'est plus « quel terme
  ajouter à `sep` » mais « `sep` seul, ou max_separation lui-même,
  suffisent-ils comme score MC » — `sep` seul fait 35/48 et 5/8,
  maxsep 37/48 et 6/8, sans terme annexe. Aucune proposition en ce sens
  n'est faite ici : elle exigerait son propre protocole.
- Rien de clinique : l'étude porte sur l'instrument.

## 8.52.7 — Provenance

- Protocole gelé : `PROTOCOL_v6.4_mc.md`, SHA
  `074b1bce34c20c5067855b3a387ec1e64d3e59c23cc6bda2c905f21e359051f6`.
- Extracteur hors-ligne : `extract_mc64.py`, SHA
  `4db02411bdf2bd92a9ca146abb35b09488aae8132d2bb18ebce8475e7b582e20` ;
  sorties `v64_mc_table.csv` / `v64_mc_table.json` (SHA
  `591c530dc095a618efdbfce1ce7f1f4f37dad834e8ea804ad552470c370c544f`) /
  `v64_mc_table.md`.
- Construction : `build_v6.4.py` ; v6.4 SHA
  `9ed728da7168925f629258e671971d3e2724c35c812a60d9bd95f5fd8199ea3d`.
- Validation code : `run_v64_mc.sh`, manifeste `manifest_v64_mc.txt`,
  journal `runs_v64_mc.log`, vérification `extract_v64_check.py`
  (SHA `141369a1f4fddb3db9ddcb430aa0fa8cb7b15a99a1488692262506c6a232ae81`)
  → `v64_mc_check.json`.
- Données : JSON v6.2 existants (lots §8.44, phase 2, §8.43, Test A) ;
  CSV inchangés, SHA déjà publiés dans `PROVENANCE_rotations_dedup_844.md`,
  `PROVENANCE_tcga_v4.md`, `PROVENANCE_mtap_prmt5_flux.md`,
  `PROVENANCE_testA_proliferation.md`. Nuls = lignes permutées, graine
  42 — échantillons hypothétiques, pas des mesures. Séries réelles =
  résidus d'expression génique ou de dépendance CRISPR (mesures
  instrumentales transformées). Aucune valeur inventée ; aucune valeur
  recopiée à la main (tables générées depuis `v64_mc_table.json`).
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`), v6.1 (`2af5e5ce…c1c9`),
  v6 (`bb8bbdba…c0773`), v6.3 (`552e7359…44ffb`).
