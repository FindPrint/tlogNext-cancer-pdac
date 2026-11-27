# Bras 2 — Pan-cancer : l'axe KRAS → CA125/CEA est-il spécifique au pancréas ?

16 novembre 2026. Protocole gelé avant les runs : `PROTOCOL_pancancer.md`.
Provenance complète : `PROVENANCE_pancancer.md`.

## Verdict d'abord — NON, il ne se réplique ni dans le poumon ni dans le côlon

- **CA125 (MUC16) : NON dans les deux cohortes.** Le gène ne suit pas KRAS du tout :
  LUAD rho +0,020 (p=0,65), COAD rho +0,019 (p=0,75). Le top-12 (+0,26 / +0,29 sd)
  est petit et au niveau du nul (LUAD nul +0,36 ; COAD nul +0,07).
- **CEA (CEACAM5) : signal monotone faible seulement, sans enrichissement des KRAS-forts.**
  Le rho est positif et significatif dans les deux cohortes (LUAD +0,173, p=7,6e-05 ;
  COAD +0,176, p=0,0028), mais le top-12 ne tient pas : LUAD +0,17 sd, exactement le
  niveau du nul (+0,18) avec Welch p=0,57 ; COAD −0,04 sd, Welch p=0,92.
  Dans le côlon, CEACAM5 est en plus saturé (médiane +16,43, Q3 +16,94) : presque
  toutes les tumeurs l'expriment très fort, il ne reste rien à séparer en haut.
- **Critère gelé** (MUC16 ET CEACAM5 avec top12_sd > 0, rho > 0 p < 0,05, au-dessus du nul) :
  non atteint dans les deux cohortes. Ce n'est pas une réplication partielle non plus
  au sens du critère — MUC16 échoue partout, et CEACAM5 échoue au top-12 partout.
- **L'axe KRAS → CA125/CEA, tel que mesuré dans le pancréas, est donc spécifique au
  pancréas** (du moins : il n'est pas une propriété générale de KRAS).

Référence pancréas (3/4 cohortes) : MUC16 top-12 +0,64 / +0,67 / +0,48 sd ;
CEACAM5 +0,43 / +0,38 / +0,63 sd. Ici, aucun des deux gènes n'approche ces niveaux
au top-12, dans aucune des deux cohortes.

## 1. Données

| Cohorte | Source | Matrice brute | Tumeurs primaires (01) | KRAS log2(RSEM+1) médiane |
|---|---|---|---|---|
| TCGA-LUAD (poumon) | Firehose stddata 2016-01-28 | 20 532 lignes (20 503 symboles uniques) × 576 échantillons ; tarball 47 043 687 o, MD5 `4c36eec3…` | 515 (61 écartés : 02, 11) | 10,41 (min 8,92 ; max 14,87) |
| TCGA-COAD (côlon) | Firehose stddata 2016-01-28 | 20 532 lignes × 328 échantillons ; tarball 26 401 036 o, MD5 `e703a630…` | 285 (43 écartés : 02, 06, 11) | 10,22 (min 8,93 ; max 11,35) |

Même route que PAAD, valeurs log2(RSEM+1), ordre KRAS brut croissant, KRAS = axe jamais flux.
Les 12 gènes v4 (PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5,
CLCA1, MUC16) sont tous présents avec ≥50 valeurs valides dans les deux cohortes,
0 NaN dans les flux, **aucun remplacement nécessaire**. (La liste de remplacement v3 hors
sexe ne contient que des gènes déjà dans les 12 — documenté dans le protocole gelé.)
Nul : mêmes lignes permutées, graine 42.

## 2. Tests directs — le verdict principal

Groupe KRAS fort = 12 dernières lignes. top12_sd = (moyenne top12 − moyenne reste) /
écart-type du gène (ddof=0). rho = Spearman gène vs rang KRAS. Welch = test t de Welch
top12 contre reste. Q3 : KRAS-forts au-dessus du quartile supérieur (attendu 3/12).
Seuil Bonferroni 12 tests : p < 0,0042. Détail complet : `pancancer_direct_tests.csv/.txt`.

### 2.1 TCGA-LUAD (n=515) — réel

| Gène | médiane | rho KRAS | p (rho) | top12 (sd) | Welch p | >Q3 |
|---|---|---|---|---|---|---|
| PGC | +8,87 | −0,030 | 0,50 | −0,46 | 0,13 | 1/12 |
| REG4 | +0,93 | +0,061 | 0,17 | +0,37 | 0,40 | 4/12 |
| CLDN18 | +7,93 | −0,060 | 0,17 | −0,39 | 0,12 | 1/12 |
| MUC17 | 0,00 | +0,056 | 0,20 | −0,11 | 0,49 | 3/12 |
| DPCR1 | +5,64 | −0,044 | 0,32 | **−0,52** | **0,0004** | 0/12 |
| CR2 | +6,67 | −0,045 | 0,31 | −0,58 | 0,063 | 0/12 |
| KRT20 | +0,44 | −0,060 | 0,17 | +0,22 | 0,51 | 4/12 |
| MUC2 | +0,91 | +0,010 | 0,82 | +0,69 | 0,18 | 5/12 |
| GSTM1 | +4,73 | **−0,121** | **0,0059** | −0,68 | 0,012 | 1/12 |
| **CEACAM5** | +12,32 | **+0,173** | **7,6e-05** | +0,17 | 0,57 | 4/12 |
| CLCA1 | 0,00 | +0,096 | 0,030 | +0,40 | 0,51 | 4/12 |
| **MUC16** | +8,87 | +0,020 | 0,65 | +0,26 | 0,27 | 2/12 |

Nul LUAD (graine 42) : 0/12 gènes p < 0,05 ; CEACAM5 nul rho +0,066 (p=0,14),
top12 +0,18 — le même top-12 que le réel ; MUC16 nul rho +0,004, top12 +0,36.
3/12 gènes p < 0,05 en réel (CEACAM5, GSTM1, CLCA1) ; seul CEACAM5 survit à Bonferroni.
À noter : dans le poumon, MUC17 est quasi non exprimée (médiane 0,00, Q3 0,00), et
plusieurs flux vont dans le sens inverse de KRAS (DPCR1, CR2, GSTM1 négatifs).

### 2.2 TCGA-COAD (n=285) — réel

| Gène | médiane | rho KRAS | p (rho) | top12 (sd) | Welch p | >Q3 |
|---|---|---|---|---|---|---|
| PGC | +2,39 | −0,142 | 0,017 | −0,48 | 0,16 | 1/12 |
| REG4 | +10,36 | **+0,250** | **2,0e-05** | +0,54 | 0,043 | 5/12 |
| CLDN18 | +1,72 | +0,144 | 0,015 | +0,71 | 0,16 | 4/12 |
| MUC17 | +7,76 | +0,103 | 0,083 | +0,70 | 0,027 | 6/12 |
| DPCR1 | +0,90 | +0,095 | 0,11 | +0,56 | 0,16 | 6/12 |
| CR2 | +4,12 | +0,085 | 0,15 | −0,10 | 0,70 | 1/12 |
| KRT20 | +12,18 | **+0,218** | **2,1e-04** | +0,63 | 0,024 | 8/12 |
| MUC2 | +12,11 | **+0,302** | **2,1e-07** | +0,11 | 0,78 | 4/12 |
| GSTM1 | +3,46 | +0,003 | 0,96 | −0,11 | 0,67 | 2/12 |
| **CEACAM5** | +16,43 | **+0,176** | **0,0028** | −0,04 | 0,92 | 6/12 |
| CLCA1 | +8,47 | **+0,242** | **3,6e-05** | +0,37 | 0,29 | 6/12 |
| **MUC16** | +0,81 | +0,019 | 0,75 | +0,29 | 0,53 | 4/12 |

Nul COAD (graine 42) : 0/12 gènes p < 0,05 ; MUC16 nul rho −0,011, top12 +0,07 ;
CEACAM5 nul rho +0,005, top12 +0,28.
7/12 gènes p < 0,05 en réel, 5 survivent à Bonferroni (MUC2, REG4, CLCA1, KRT20, CEACAM5).
**Le côlon montre un programme intestinal entier qui monte avec KRAS** (MUC2, REG4, KRT20,
CLCA1, CLDN18, MUC17, DPCR1 positifs) — mais MUC16 n'en fait pas partie (rho +0,019,
p=0,75 ; à peine exprimée : médiane +0,81), et CEACAM5, saturé, ne sépare pas les
KRAS-forts (top-12 −0,04 sd).

### 2.3 Comparaison directe avec le pancréas

| Gène | Pancréas (3/4 cohortes, top-12 sd) | LUAD top-12 / rho | COAD top-12 / rho |
|---|---|---|---|
| MUC16 (CA125) | +0,64 / +0,67 / +0,48 | +0,26 / +0,020 (p=0,65) | +0,29 / +0,019 (p=0,75) |
| CEACAM5 (CEA) | +0,43 / +0,38 / +0,63 | +0,17 / +0,173 (p=7,6e-05) | −0,04 / +0,176 (p=0,0028) |

Le contraste est net : dans le pancréas, les deux marqueurs sont élevés chez les
KRAS-forts dans 3 cohortes sur 4 ; ici, MUC16 est plat partout et CEACAM5 ne se
distingue qu'en rho monotone, sans enrichissement du groupe KRAS-fort.

## 3. Runs v6 (cascade, MC, L7a, Delta)

Pipeline v6.0.0 Cohen, SHA `bb8bbdba…c0773` vérifié, mode fast, 4 runs exit 0
(19h39–19h56 UTC, log `runs_pancancer_v6.log`).

| Run | n | T_-2 | T_-1 | T_0 | T_+1 | T_+2 | Delta | L7a |
|---|---|---|---|---|---|---|---|---|
| LUAD réel | 515 | 0,76 % | 46,69 % | 68,62 % | 80,82 % | 80,82 % | 2,511 | UP 42,11 % |
| LUAD nul | 515 | 0,00 % | 0,61 % | 3,61 % | 69,61 % | 69,61 % | 2,497 | DOWN 23,25 % |
| COAD réel | 285 | 0,00 % | 33,92 % | 86,76 % | 98,02 % | 98,02 % | 4,619 | DOWN 20,95 % |
| COAD nul | 285 | 0,00 % | 1,36 % | 68,07 % | 94,73 % | 94,73 % | 4,599 | UP 41,04 % |

Lecture, comme dans les bras précédents :
- **Delta réel ≈ Delta nul** dans les deux cohortes (LUAD 2,511 contre 2,497 ;
  COAD 4,619 contre 4,599). Le Delta mesure ici une propriété des distributions
  marginales des flux, pas de l'ordre KRAS — le nul, qui brise l'ordre, donne le même.
- **Les nuls produisent eux aussi des cascades complètes** avec des T_0 nets
  (3,61 % et 68,07 %). Une cascade n'est pas un verdict.
- **L7a est faible (< 50 %) et discordant** : LUAD réel UP 42 % contre nul DOWN 23 % ;
  COAD réel DOWN 21 % contre nul UP 41 %. Il ne tranche rien.
- L7b FRAGILE (mode light) dans les 4 runs, réel comme nul — non-informatif
  (règle du projet).
- MC prédictif : 48 scénarios, terminé, dans les 4 runs.
- **Le v6 ne sépare pas réel et nul ici. Le verdict vient des tests directs (§2).**

## 4. Ce que ça change pour la recherche du remède

1. **CA125 reste un marqueur pancréatique, pas une lecture universelle de KRAS.**
   Le fait que MUC16 ne suive pas KRAS dans le poumon ni dans le côlon renforce
   l'idée que le signal pancréas tient au tissu (ou au sous-type pancréatique),
   pas à KRAS seul. Les pistes « cibler CA125 » ne se transfèrent pas aux cancers
   KRAS du poumon et du côlon — et rien ici ne les affaiblit pour le pancréas.
2. **CEA : un lien monotone faible avec KRAS existe hors pancréas** (rho +0,17 dans
   les deux cohortes, significatif après Bonferroni), mais sans enrichissement des
   KRAS-forts : il ne sert pas à repérer les tumeurs KRAS-fortes, et dans le côlon
   il est saturé. Pas une piste de stratification, un fait descriptif.
3. **Le côlon a son propre programme lié à KRAS** (MUC2 +0,302, REG4 +0,250,
   CLCA1 +0,242, KRT20 +0,218 — tous p < 0,0042). C'est une piste distincte,
   intestinale, non testée ici comme cible ; elle ne concerne pas le remède
   pancréatique, sauf à suggérer que chaque tissu répond à KRAS avec son propre
   programme — ce qui cadre avec la spécificité pancréatique du signal CA125/CEA.
4. **Rien ne change aux pistes déjà établies** (daraxonrasib approuvé FDA,
   vopimetostat + daraxonrasib 82 % chez les MTAP-délétés, IBI343 précoce,
   ATR seul en hypothèse ouverte). Ce bras ferme une question — la généralité
   de l'axe — par un négatif propre, avec deux grandes cohortes (515 et 285 tumeurs).

## 5. Limites

- Une seule mesure d'expression par tumeur (ARN total, pas de protéine, pas de
  statut mutationnel KRAS — l'axe est l'expression KRAS, comme dans tout le projet).
- Le top-12 compare 12 patients contre le reste : sensible aux extrêmes, mais
  c'est la convention du projet, appliquée partout, avec le nul en témoin.
- MUC16 est à peine exprimée dans le côlon (médiane +0,81) et MUC17 quasi absente
  du poumon (médiane 0,00) : pour ces gènes-là, l'absence de signal peut aussi
  refléter une absence d'expression dans le tissu, pas seulement une absence de lien.
- Deux cohortes seulement (poumon, côlon) : la question reste ouverte pour d'autres
  cancers KRAS (ex. endomètre, ovaire), non testés ici.

## 6. Fichiers

- `PROTOCOL_pancancer.md` — protocole gelé avant les runs.
- `build_fluxes_pancancer.py`, `pancancer_direct_tests.py`, `run_pancancer_v6.sh`
- `data/tcga_luad_rsem.tar.gz` (+ `.md5`), `data/tcga_coad_rsem.tar.gz` (+ `.md5`)
- `pdac_luad_fluxes.csv`, `pdac_luad_fluxes_nul.csv`, `pdac_coad_fluxes.csv`, `pdac_coad_fluxes_nul.csv`
- `pancancer_direct_tests.csv`, `pancancer_direct_tests.txt`
- `results_fast_pancancer_luad/`, `results_fast_pancancer_luad_nul/`,
  `results_fast_pancancer_coad/`, `results_fast_pancancer_coad_nul/`
- `PROVENANCE_pancancer.md` (JSON + runs v6 + SHA256)
