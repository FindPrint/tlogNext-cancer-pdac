# MTAP / PRMT5 et pan-cancer — rapport combiné (16 nov. 2026)

**Verdicts d'abord :**
1. **MTAP/PRMT5 — NON, la délétion MTAP n'est pas démontrée enrichie chez les KRAS-forts** (6/12 contre 37/165, Fisher p = 0,073 — puissance limitée par n = 12). Le ciblage MTAP est orthogonal à l'axe KRAS. **Fait nouveau : l'expression PRMT5 monte avec KRAS** (rho +0,196, p = 0,0087 ; top-12 +0,83 sd), mais expression ≠ dépendance (CRISPR PRMT5 rho −0,189, NS) : hypothèse à tester, pas une cible validée.
2. **Pan-cancer — NON, l'axe KRAS → CA125/CEA ne se réplique pas.** CA125 plat dans le poumon et le côlon ; CEA garde seulement un lien monotone faible, sans enrichissement des KRAS-forts. **L'axe est spécifique au pancréas.** Fait nouveau : le côlon a son propre programme lié à KRAS (MUC2, REG4, CLCA1, KRT20).
3. **Ce que ça change :** rien n'affaiblit les pistes établies (daraxonrasib, vopimetostat + daraxonrasib, IBI343, ATR seul). CA125 reste un marqueur pancréatique. La combinaison vopimetostat s'adresse aux MTAP-délétés (24 % des tumeurs), un sous-groupe distinct qui recoupe la moitié des KRAS-forts sans être le même groupe.

---

## Bras 1 — MTAP / PRMT5 et l'axe KRAS (TCGA PAAD, 178 tumeurs)

**Données :** expression Firehose PAAD (matrice déjà sur disque, MD5 `b09569ce…`) ; copy-number GISTIC2 Level 4 Firehose analyses 2016-01-28, tarball `data/tcga_paad_gistic.tar.gz` (26 189 717 octets, MD5 vérifié `816034f7…`, SHA256 `6edc20f3…`) — **délétion mesurée, aucun proxy utilisé**. 177/178 tumeurs appariées (TCGA-FB-A4P6 sans GISTIC, hors top-12 — sans effet sur les comptes). Script `mtap_kras_tests.py` (SHA `162aeff7…`), protocole gelé en en-tête avant les tests.

**Faits cités sans réimport** (balayage CRISPR génome entier, 47 lignées) : dépendance Chronos contre KRAS — PRMT5 rho −0,189 (FDR 0,87), MTAP +0,071 (FDR 0,96), CDKN2A +0,161 (FDR 0,89) — tous non significatifs.

**Résultats (tests directs, `mtap_direct_tests.csv` SHA `9b445ac0…`) :**

| Test | Résultat |
|---|---|
| MTAP délétion profonde (−2), top-12 KRAS-forts contre reste | 6/12 (50 %) contre 37/165 (22 %) ; OR 3,46 ; **Fisher bilatéral p = 0,073 — non significatif** (critère pré-enregistré) ; permutation unilatérale p = 0,038 ; attendu sous hasard 2,9/12 |
| MTAP expression contre KRAS | rho +0,125, p = 0,097 ; top-12 −0,27 sd, Welch p = 0,45 ; identique après correction pureté (rho +0,135, p = 0,073) |
| **PRMT5 expression contre KRAS** | **rho +0,196, p = 0,0087 (Bonferroni 3 gènes OK) ; top-12 +0,83 sd, Welch p = 0,0007, d de Cohen +0,84 ; 7/12 >Q3 (attendu 3) ; après correction pureté rho +0,216, p = 0,0039, top-12 +0,90 sd** |
| CDKN2A expression contre KRAS | rho −0,063, p = 0,40 ; rien |
| CDKN2A délétion profonde (−2) | 6/12 contre 43/165, Fisher p = 0,095 |
| Perte quelconque (−2 ou −1), secondaire | MTAP 11/12 contre 94/165, p = 0,029 ; CDKN2A 12/12 contre 97/165, p = 0,0037 — mais la perte −1 **n'abaisse pas** l'expression MTAP (médiane 9,18 contre 9,09 diploïde) : ce n'est pas une délétion fonctionnelle, ne pas la lire comme « 11/12 délétés » |
| Co-délétion 9p21 | toute MTAP −2 est co-délétée avec CDKN2A (43/43) ; CDKN2A −2 seul : 6 |
| Contrôle qualité GISTIC | expression MTAP médiane −2 : 7,69 contre 0 : 9,09 — la délétion profonde abaisse bien l'expression, les appels sont cohérents |
| Contrôles | MTAP contre PRMT5 rho +0,237, p = 0,0015 (montent ensemble) ; MTAP insensible à la pureté (rho acineux +0,094, p = 0,21 ; R² 5,1 %) — pureté non confondante |

**Interprétation :** la combinaison vopimetostat + daraxonrasib ne s'adresse pas aux mêmes patients que l'axe KRAS. Elle cible les MTAP-délétés — 24 % des tumeurs (43/177) — un sous-groupe qui recoupe partiellement les KRAS-forts (la moitié d'entre eux) sans être le même groupe. Seule une cohorte plus grande peut confirmer/infirmer l'enrichissement (puissance limitée par n = 12). Angle suivant possible : dépendance PRMT5 contre statut MTAP **mesuré** dans DepMap, plutôt que contre KRAS — puisque l'expression PRMT5 monte avec KRAS mais que la dépendance ne le suit pas.

Fichiers : `mtap.md`, `PROVENANCE_mtap.md`, `mtap_kras_tests.py`, `mtap_direct_tests.csv` (`9b445ac0…`), `mtap_controls.csv` (`51e1f93c…`), `mtap_gistic_status.csv` (`b54cb94f…`), `mtap_direct_tests.txt` (`02c693eb…`).

---

## Bras 2 — Pan-cancer : l'axe KRAS → CA125/CEA est-il spécifique au pancréas ? (runs v6)

**Données :** Firehose stddata 2016-01-28, même route que PAAD. LUAD : tarball 47 043 687 octets, MD5 `4c36eec3f6df75630292c5a569cfc8f4`, 20 503 gènes × 576 échantillons, **515 tumeurs primaires** (61 écartées). COAD : tarball 26 401 036 octets, MD5 `e703a630556d42f098cf0df87d4712bb`, 20 503 gènes × 328 échantillons, **285 tumeurs primaires** (43 écartées). Aucun MD5 de référence publié par Firehose pour LUAD/COAD — MD5 observés consignés et vérifiés à chaque lecture. Valeurs log2(RSEM+1). Protocole gelé : `PROTOCOL_pancancer.md`.

**Flux :** les 12 mêmes gènes v4, tous présents avec ≥50 valeurs valides dans les deux cohortes, 0 NaN, **aucun remplacement nécessaire** (la liste v3 hors sexe ne contient que des gènes déjà dans les 12 — documenté). Ordre KRAS brut croissant. Flux CSV : LUAD `d407849b…` (515 lignes), nul `93766e8c…` ; COAD `79e23912…` (285 lignes), nul `9172a004…`.

**Runs v6 fast** (pipeline `universal_v6.0.0_cohen.py`, SHA `bb8bbdba…c0773` vérifié, jamais modifié ; 19h39–19h56 UTC, tous exit 0, log `runs_pancancer_v6.log`) :

| Run | T_-2 / T_-1 / T_0 / T_+1 / T_+2 | Delta | L7a |
|---|---|---|---|
| LUAD réel (n=515) | 0,76 / 46,69 / **68,62** / 80,82 / 80,82 % | 2,511 | UP 42,11 % |
| LUAD nul | 0,00 / 0,61 / 3,61 / 69,61 / 69,61 % | 2,497 | DOWN 23,25 % |
| COAD réel (n=285) | 0,00 / 33,92 / **86,76** / 98,02 / 98,02 % | 4,619 | DOWN 20,95 % |
| COAD nul | 0,00 / 1,36 / 68,07 / 94,73 / 94,73 % | 4,599 | UP 41,04 % |

**Delta réel ≈ nul et cascades complètes dans les nuls : le v6 ne sépare pas réel et nul ici — le verdict vient des tests directs**, comme le veut la règle. L7b FRAGILE (mode light) dans les 4 runs, réel comme nul — non-informatif.

**Tests directs (`pancancer_direct_tests.csv` SHA `1e3786c2…`, 48 lignes) — le verdict principal :**

| Gène | LUAD rho (p) | LUAD top-12 (sd) | COAD rho (p) | COAD top-12 (sd) | Référence pancréas (top-12) |
|---|---|---|---|---|---|
| **MUC16 (CA125)** | +0,020 (p=0,65) | +0,26, Welch p=0,27 | +0,019 (p=0,75) | +0,29, Welch p=0,53 | **+0,64 / +0,67 / +0,48** |
| **CEACAM5 (CEA)** | **+0,173 (p=7,6e-05, Bonferroni)** | +0,17, Welch p=0,57 (= niveau du nul +0,18) | **+0,176 (p=0,0028)** | −0,04, Welch p=0,92 | **+0,43 / +0,38 / +0,63** |

**Critère gelé** (les deux gènes : top12_sd > 0, rho > 0 p < 0,05, au-dessus du nul) : **non atteint dans les deux cohortes.** CA125 est plat ; CEA garde un lien monotone faible avec KRAS hors pancréas (rho ~+0,17 dans les deux cohortes), sans enrichissement des KRAS-forts — sans valeur de stratification. Nuls : 0/12 p < 0,05 dans les deux cohortes.

**Fait nouveau inattendu : le côlon a son propre programme lié à KRAS** — 7/12 gènes p < 0,05, 5 après Bonferroni : MUC2 rho +0,302 (p=2,1e-07), REG4 +0,250, CLCA1 +0,242, KRT20 +0,218, CEACAM5 +0,176 ; PGC −0,142 et CLDN18 +0,144 (p < 0,05, non Bonferroni). MUC16 n'en fait pas partie (à peine exprimée, médiane +0,81). LUAD : 3/12 p < 0,05, 1 après Bonferroni (CEACAM5 seul) ; GSTM1 −0,121 et CLCA1 +0,096.

**Limites :** axe = expression KRAS (pas le statut mutationnel) ; MUC16 à peine exprimée dans le côlon (médiane +0,81) et MUC17 quasi absente du poumon (médiane 0,00) ; deux cohortes seulement — endomètre/ovaire non testés.

Fichiers : `PROTOCOL_pancancer.md`, `pancancer.md`, `PROVENANCE_pancancer.md`, `build_fluxes_pancancer.py`, `pancancer_direct_tests.py`, `run_pancancer_v6.sh`, `pdac_luad_fluxes.csv` (+ nul), `pdac_coad_fluxes.csv` (+ nul), `pancancer_direct_tests.csv/.txt`, `results_fast_pancancer_*` (4 dossiers), `runs_pancancer_v6.log`.

---

## Ce que ça change pour la recherche du remède

- **CA125 reste un marqueur pancréatique**, pas une lecture universelle de KRAS. Les pistes CA125 ne se transfèrent pas au poumon/côlon, et rien ici ne les affaiblit pour le pancréas.
- **La combinaison vopimetostat + daraxonrasib cible un sous-groupe distinct** (MTAP-délétés, 24 %) — orthogonal à l'axe KRAS dans les limites de cette cohorte. Elle ne se substitue pas à l'axe, elle le complète.
- **PRMT5 monte avec KRAS en expression** mais sans dépendance CRISPR liée à KRAS : une hypothèse à tester (dépendance PRMT5 contre statut MTAP mesuré dans DepMap), pas une cible validée.
- **Le côlon a son propre programme KRAS** (MUC2/REG4/CLCA1/KRT20) : une piste neuve, hors pancréas, à noter — pas une piste de remède pancréatique.
- **Rien ne change aux pistes établies** : daraxonrasib (approuvé), vopimetostat + daraxonrasib (82 % en MTAP-délétés), IBI343 anti-CLDN18.2 (phase III), ATR seul (hypothèse d'expression).

## Fichiers (tous dans `~/workspace/runs/pdac-v6/`)

- Ce rapport : `mtap_pancancer.md`
- Provenance combinée : `PROVENANCE_mtap_pancancer.md` (détail par bras : `PROVENANCE_mtap.md`, `PROVENANCE_pancancer.md`)
- Bras 1 : `mtap.md`, `mtap_kras_tests.py`, `mtap_direct_tests.csv`, `mtap_controls.csv`, `mtap_gistic_status.csv`, `mtap_direct_tests.txt`, `data/tcga_paad_gistic.tar.gz`
- Bras 2 : `PROTOCOL_pancancer.md`, `pancancer.md`, `build_fluxes_pancancer.py`, `pancancer_direct_tests.py`, `run_pancancer_v6.sh`, `pdac_luad_fluxes.csv` (+ nul), `pdac_coad_fluxes.csv` (+ nul), `pancancer_direct_tests.csv/.txt`, `data/tcga_luad_rsem.tar.gz`, `data/tcga_coad_rsem.tar.gz`, `results_fast_pancancer_*`, `runs_pancancer_v6.log`
