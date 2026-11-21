# Volet 4 — Universalité du pipeline (audit §8.90)

**Audit du projet PDAC, volet 4/5 — lecture seule, 21 novembre 2026.**
Auteur du volet : sous-agent d'audit (lecture seule). Aucun run de pipeline lancé,
aucun fichier du livre blanc ni des résultats modifié ; seul ce fichier a été écrit.

**Sources.** Livre blanc `~/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md`
(§8.1–§8.89, 22 783 lignes, vérifié par `wc -l` le 21 nov. 2026) ; dossiers de runs
`~/workspace/runs/pdac-v6/` (750 dossiers `results_fast_*` comptés) et
`~/workspace/runs/biophysique-hp35/` (provenance HP35) ; un `master_results.json`
réel lu en lecture seule (`results_fast_tcga_v4/master_results.json`, v6.2).
Versions : v6 SHA `bb8bbdba…c0773` (référence historique, intacte) ;
v6.1 SHA `2af5e5ce…c1c9` (référence depuis le 19 nov.) ;
v6.2 SHA `f07567c4…ec3abf` (version de travail, déterministe, adoptée le 19 nov. 2026, §8.37).
maxsep adopté pleinement par décision de Zackary le 20 nov. 2026, 13h04 (§8.64.12) —
décision, pas preuve nouvelle (voir §5 ci-dessous).

**Méthode.** Chaque chiffre ci-dessous renvoie à sa section. « Séparer » veut dire ici,
sauf mention contraire : écart réel − nul positif, au-dessus de la gigue / du plancher
gelé (0,07 en |d| pour maxsep/S_sep ; ±0,07 en v6.1, 0,00 mesurée en v6.2),
dans le sens attendu, sur le comptage pré-enregistré. Le « nul » du projet est
toujours le même objet : les lignes de la série réelle permutées (graine 42),
colonne de contrôle intacte. Ce n'est pas un nul biologique, c'est un ordre détruit.

---

## §0 — CORRECTION DE ZACKARY, 21 NOV. 2026, 11h00 (point central, à porter au §8.90)

> **MC n'est JAMAIS seul. Dans le pipeline, MC est accompagné de toute la batterie
> de diagnostics : les 29 estimateurs, les 6 questions (Q1–Q6), les tests de bruit,
> les F1/F2 avant et après seuil, et le reste (L7a/L7b, falsification, Delta, maxsep).
> Aucun verdict ne repose sur MC seul, ni sur maxsep seul.**

Cette correction est traitée en pleine section (§5) : vérification par grep et par
lecture du `master_results.json`, lieux exacts de la survente (« maxsep seul SUFFIT »,
§8.56/§8.59), et texte d'addendum daté proposé. **Elle est signalée en tête du
résumé final (§6), comme demandé.** En une phrase : *maxsep est le score principal
AFFICHÉ, pas le verdict ; le verdict, c'est la batterie entière — et aucun élément
seul ne porte un verdict.*

---

## (1) Tableau des systèmes sur lesquels le pipeline a VRAIMENT tourné

« Vraiment tourné » = runs v6 / v6.1 / v6.2 comptés dans le livre blanc (§8.1–§8.89),
avec dossier `results_fast_*` sur disque. Tout le reste est signalé comme tel.

| # | Système | Nature des données | n | Ce qui a été ordonné (axe) | Version | Résultat principal | Section |
|---|---|---|---|---|---|---|---|
| 1 | **HP35** (repliement protéique, dynamique moléculaire) | Trajectoire MD 500 ns, 1 000 frames ; 7 flux (RMSD, Rg, liaisons H, SASA, RMSF moyenne, PC1, énergie potentielle) | 1 000 | Temps de production (vrai temps, 10 ps → 499 510 ps) | v6, v6.1, v6.2 | **Témoin positif, seul système où MC sépare nettement** : MC 0,6035 vs nul 0,4086 (+0,1950) ; maxsep +1,6512 ; Delta −0,09 (nul devant) ; cascade 0/16/90/376 | §8.30, §8.35, §8.37 ; provenance `runs/biophysique-hp35/PROVENANCE.md` (Zenodo 23895045, Wang et al.) |
| 2 | **TCGA-PAAD v1–v4** (tumeurs pancréas) | ARN bulk tumeurs, 12 flux | 178 | Expression / résidu KRAS croissant | v6, v6.1, v6.2 | Chaîne KRAS (§8.4) : bloc estomac/mucus qui chute (PGC −0,89, DPCR1 −0,85, CLDN18 −0,46 sd) pendant que MUC16 monte (+0,64 sd) ; MC +0,045, maxsep +0,293 | §8.1–§8.4, §8.31, §8.35 |
| 3 | **TCGA-PAAD, variantes v4r** (KRAS-valeur, KRAS-desc, CLDN18, pureté) | ARN tumeurs, 12 flux | 178 | KRAS brut / décroissant / CLDN18 / score acinaire | v6, v6.1 | CLDN18 : artefact doublon (Spearman 1,000) + vraie co-expression ; sans doublon, ne sépare toujours pas (MC 0,4257 vs 0,3313, Delta 3,862 vs 3,854) | §8.9, §8.31 (4) |
| 4 | **DepMap CRISPR** (lignées pancréas) | Dépendance Chronos, 12 gènes | 45 | Chronos KRAS croissant | v6.1 (v6 bloqué : min 50), v6.2 | **Ne sépare pas** : MC 0,3615 vs 0,3499 ; Delta 1,93 vs 1,69 ; maxsep +0,190 ; falsification indisponible (n < 75) | §8.30, §8.35 |
| 5 | **CPTAC protéine UMich** (tumeurs) | Protéine (spectrométrie de masse), 7 flux | 63 | KRAS protéine croissant | v6, v6.1 | **NON-confirmation** : T_0 au pas 3 ; Delta 1,48 vs 1,49 ; L7a NaN en v6 | §8.8, §8.14, §8.31 |
| 6 | **CPTAC protéine BCM** (tumeurs) | Protéine, 6 flux (MUC16 exclue) | 52 | KRAS protéine croissant | v6, v6.1 | **NON-confirmation** : Delta 1,55 vs 1,52 ; L7a NaN en v6 | §8.8, §8.14, §8.31 |
| 7 | **GSE71729** (Moffitt, puce Agilent) | ARN tumeurs | 145 | KRAS brut croissant | v6, v6.1, v6.2 | Moitié « marqueurs qui montent » tient ; MC +0,006, maxsep +0,040 (sous plancher), Delta −0,04 | §8.10, §8.35 |
| 8 | **GSE62452** (puce Affymetrix) | ARN tumeurs | 69 | KRAS brut croissant | v6, v6.1, v6.2 | Confirmation expression 3/3 cohortes (avec TCGA, GSE71729) ; MC −0,003, maxsep −0,004, Delta +0,15 ; L7a NaN en v6 | §8.13, §8.35 |
| 9 | **ICGC PACA-AU** (Bailey 2016) | ARN tumeurs (log2 CPM) | 70 | KRAS brut croissant | v6, v6.1, v6.2 | Expression NON (MUC16 +0,13 sd, dans le bruit du nul) ; survie CA125 OUI par test direct ; MC +0,015, maxsep +0,097, Delta +0,07 | §8.16, §8.35 |
| 10 | **Immunitaire TCGA** (12 gènes marqueurs) | ARN bulk tumeurs | 178 | KRAS brut croissant | v6, v6.1, v6.2 | Tumeur froide : chute cytotoxique en haut de l'axe (GZMB −1,65) ; MC +0,055, maxsep +0,368, Delta +1,91 — mais Delta vient d'un nul anormalement bas (2,30) | §8.23, §8.31 (3), §8.35 |
| 11 | **Immunitaire GSE71729 / GSE62452 / ICGC** | ARN bulk tumeurs | 145 / 69 / 70 | KRAS brut croissant | v6 (§8.23) | Même lecture directionnelle (tumeur froide) ; pas de séparation par scores dans le lot étendu | §8.23, §8.33 |
| 12 | **PARP / réparation TCGA** (12 gènes) | ARN tumeurs | 178 | KRAS brut / résidu | v6, v6.1, v6.2 | Axe BRCA2/ATR/RAD51 ; KRAS + PARP NON ; MC +0,024, maxsep +0,169, Delta +0,26 | §8.24, §8.25, §8.35 |
| 13 | **TCGA-LUAD** (poumon, pan-cancer) | ARN tumeurs, 12 gènes v4 | 515 | KRAS brut croissant | v6, v6.1 | Axe KRAS → CA125/CEA **ne se réplique pas** ; Delta 2,511 vs 2,497 ; MUC16 plat (+0,020) | §8.27, §8.33 |
| 14 | **TCGA-COAD** (côlon, pan-cancer) | ARN tumeurs, 12 gènes v4 | 285 | KRAS brut croissant | v6, v6.1 | Programme KRAS propre au côlon (MUC2 +0,302) ; Delta 4,619 vs 4,599 ; MUC16 plat (+0,019) | §8.27, §8.33 |
| 15 | **Rotations de contrôle** (4 familles × 12 flux) | Mêmes natures que les séries mères | 178 / 45 / 178 / 178 | Un flux à tour de rôle, croissant | v6.1 (96 runs), v6.2 (88 runs sans doublon) | Aucun contrôle ne sépare par MC/Delta/L7a/falsification (§8.32) ; maxsep/S_sep 37/48 sans doublon (§8.44) ; 3 blocs de co-expression confirmés par tests directs | §8.32, §8.41, §8.44 |
| 16 | **Test A — TCGA v4 par prolifération** | ARN tumeurs | 178 | Score prolifération (MKI67, TOP2A, PCNA, CCNB1) | v6.1 | **NON** : chaîne absente ; MC nul devant (0,3638 vs 0,4587), Delta nul devant (3,798 vs 4,590) | §8.34 |
| 17 | **Test C — TCGA v4 par stade clinique** | ARN tumeurs | 175 | Stade AJCC (I–IV, 4 marches) | v6.2 | **NON** : bloc MONTE au lieu de s'effondrer ; MC 0,3472 vs 0,3507, Delta 3,852 vs 3,830, falsification 0,642 vs 0,774 | §8.45 |
| 18 | **Série TCGA v4 par CN MTAP** | ARN tumeurs | 177 | Nombre de copies MTAP (GISTIC) | v6.1 | **NON** : MC, Delta, falsification tous meilleurs au nul (0,3512 vs 0,5153 ; 3,805 vs 4,347 ; 0,733 vs 0,816) | §8.36 |
| 19 | **Série MTAP par dépendance PRMT5** | ARN tumeurs | 177 | Dépendance PRMT5 comme flux | v6.2 | **NON** : chaîne ne réapparaît pas ; MC 0,3390 vs nul 0,3386 | §8.43 |
| 20 | **GSE21501** (paire indépendante, Stratford 2010) | ARN tumeurs PDAC | 132 | KRAS croissant | v6.2 | **NON** : d_maxsep −0,0100 ; A2 étendu 6/9 ; C3 non levée | §8.69 |
| 21 | **GSE79668** (Kirby 2016) | ARN tumeurs PDAC | 51 | KRAS croissant | v6.2 | **PARTIEL** : d_maxsep +0,0567 (sous plancher) ; consolidation §8.72 **RENVERSE** (d_médian +0,1447 sur 13 nuls) | §8.70, §8.72 |
| 22 | **GSE60979** (Sandhu 2015, Oslo) | ARN tumeurs PDAC | 49 | KRAS croissant | v6.2 | **CONFIRME** : d_maxsep +0,2045 ; A2 7/11 ; **C3 LEVÉE** | §8.71 |
| 23 | **GSE131050 FF** (Rashid 2020, Yeh_seq) | ARN tumeurs PDAC | 42 | KRAS croissant | v6.2 | **CONFIRME de justesse** : d_maxsep +0,0739 (marge 0,0039) ; A2 8/12 ; consolidée par 2 nuls frais | §8.74 |
| 24 | **GSE131050 FNA** (mêmes tumeurs) | ARN tumeurs PDAC | 42 | KRAS croissant | v6.2 | **CONFIRME, appariée** : d_maxsep +0,1642 ; non comptée comme paire nouvelle | §8.76 |
| 25 | **GSE57495** (13e paire) | ARN tumeurs PDAC, 11 flux | 63 | KRAS croissant | v6.2 | **CONFIRME** : d_maxsep +0,4494 (plus grand écart GEO) ; A2 9/13 | §8.79 |
| 26 | **GDC ORGANOID-PANCREATIC** (organoïdes) | ARN organoïdes, 12 flux (DPCR1 → MUCL3) | 44 | KRAS croissant | v6.2 | **CONFIRME, fragile** : d_maxsep +0,0884 (marge 0,0184) ; A2 10/14 ; consolidation §8.87 **FRAGILE CONFIRMÉ** (d_médian +0,0314, rang 13/14, 2/13 nuls au-dessus du plancher, réel sous p95) | §8.85, §8.87 |
| 27 | **GSE194249** (11 flux, DPCR1 absent) | ARN tumeurs (FPKM) | 84 | KRAS croissant | v6.2 | **NON** (15e paire) : d_maxsep −0,0239, nul devant ; A2 10/15 | §8.86, §8.88 |
| 28 | **Chen 2025, lot drogue** (46 PDO × 63 AUC) | Sensibilité drogue (AUC), axe gemcitabine | 46 | Sensibilité à la gemcitabine | v6.2 | **CONFIRME, exploratoire, hors A2** (n < 50) : d_maxsep +0,0982 ; 2 hits FDR < 0,05 ; drogue × KRAS et drogue × MTAP intestables (aucune table par-PDO publiée) | §8.84, §8.89 |
| 29 | **GSE62165** (Janky, 4e cohorte bloc mucus) | ARN tumeurs PDAC | 118 | KRAS croissant (tests directs) | v6.2 (20 runs) | Cœur du bloc confirmé par tests directs (G5/KRAS 4/4, G1/KRAS) ; **pipeline : pas de séparation du nul** (MC 4/10, S_sep 5/10, L7b FRAGILE 20/20) | §8.66 |
| 30 | **TCGA-GBM** (cerveau, privilège immunitaire) | ARN tumeurs | 153 | Prolifération, puis score PRIV | v6.2 | Chaîne PDAC absente ; d_maxsep +0,0283 (prolif.), +0,0116 (PRIV) — ne passe pas | §8.82 |
| 31 | **TCGA-UVM** (mélanome uvéal, œil) | ARN tumeurs | 80 | Score PRIV (7 gènes) | v6.2 | Privilège MOINS exprimé qu'en PAAD (d −0,35 à −3,00) ; d_maxsep +0,0496 — ne passe pas ; image miroir, pas réapparition | §8.81 |
| 32 | **TCGA ordre PRIV** (pancréas, piste Œil) | ARN tumeurs | 178 | Score PRIV (7 gènes) | v6.2 | d_maxsep +0,1649 (au-dessus du plancher) **mais la chaîne ne réapparaît pas** ; piste Œil CLOSE comme copie d'un programme | §8.81 |

**Total compté dans le livre blanc.** Lot v6.1 : 140/140 runs (44 étendus + 96 rotations,
§8.31–§8.32) ; v6.2 : validation 20/20 (§8.37), 88 runs sans doublon (§8.44),
paires indépendantes 2 runs chacune (§8.69–§8.88), plus les lots §8.50/§8.53/§8.66/§8.73.
Le §8.33 recense 24 séries de base PDAC (hors rotations et nuls), de **quatre natures
seulement** : ARN de tumeurs, ARN de lignées, protéine de tumeurs, dépendance CRISPR.

### Ce qui n'a PAS tourné en v6 / v6.1 / v6.2 dans ce livre blanc (à ne pas compter)

- **Ising 2D classique et Ising quantique.** Aucun run Ising dans les §8.1–§8.89.
  Les benchmarks Ising appartiennent à des versions antérieures et à d'autres dépôts :
  v5.3, balayage L=16, 105 observations, 18 tests sémantiques (§8.78, inventaire des
  dépôts `universal-log-research`, `ising_classique_test/`, `ising_quantique_test/`) ;
  un run aveugle L=64 est cité dans ce même inventaire, pas comme un run du présent
  livre blanc. Le pipeline *ancêtre* a donc vu l'Ising, le pipeline v6 du présent
  dossier, non — et la traduction en température / comparaison à Tc n'est jamais dans
  le code (0 occurrence de `temperature` / `Onsager` / `2.269`, règle §8.31 et mémoire).
- **Cosmo, Climat, Finance** (`Cosmo_Tlog`, `Climat_Tlog`, `Tlog_Finance`, cités §8.78
  comme noms `ModeFast_*` dans un autre dépôt) : jamais courus en v6.2 ici.
- **Fs et (AAQAA)3** (les deux autres systèmes du record Zenodo 23895045) : seul HP35
  a été traité ; les deux autres n'ont jamais tourné.
- **Single-cell PDAC** (TISCH2 / GSE155698, GSE154778, GSE111672) : listées en réserve
  au §6 du livre blanc, jamais courues.

---

## (2) Tableau séparation réel / nul, score par score

Règle de lecture : « ✓ » = sépare au critère pré-enregistré ; « ✗ » = ne sépare pas ;
« ~ » = partiel / fragile / inversé. MC = ancien composite
(0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·netteté) ; maxsep = |d de Cohen|
maximal du scan ; S_sep = maxsep × stabilité ; Delta = d_div − d_sat ;
L7a = vote de cohérence up/down/flat ; falsification = comparaison interne
d_crit géométrique vs SpectralDimension (seuil 0,5) — **pas** une comparaison au
nul permuté (§8.31, §8.35).

### 2a. Les 8 paires principales — Phase 2, §8.35 (v6.1, critère ≥ 6/8 écrit d'avance)

| Paire (n) | MC | Delta | maxsep | L7a | Falsification | Cohérence flux à T_0 |
|---|---|---|---|---|---|---|
| HP35 (1 000) | ✓ +0,1950 | ✗ −0,09 | ✓ +1,6512 | ✗ +0,044 | ✓ +0,148 | ✓ 0,71 vs 0,14 |
| TCGA v4 (178) | ✗ +0,0453 | ✓ +0,42 | ✓ +0,2928 | ✓ −0,572 (sens négatif) | ✓ +0,207 | ✓ 0,67 vs 0,33 |
| GSE71729 (145) | ✗ +0,0059 | ✗ −0,04 | ✗ +0,0402 | ✗ +0,061 | ✓ +0,114 | ✗ 0,67 vs 0,67 |
| GSE62452 (69) | ✗ −0,0031 | ✓ +0,15 | ✗ −0,0036 | ✗ +0,139 (sens inverse) | indisponible (n < 75) | ✗ 0,42 vs 0,58 |
| ICGC (70) | ✗ +0,0150 | ✓ +0,07 | ✓ +0,0970 | ✗ +0,531 (sens inverse) | indisponible (n < 75) | ✗ 0,50 vs 0,58 |
| Immunitaire TCGA (178) | ✗ +0,0545 | ✓ +1,91 | ✓ +0,3675 | ✓ −0,526 (sens négatif) | ✗ −0,147 (inversé) | ✗ 0,92 vs 1,00 (nul plus cohérent) |
| PARP TCGA (178) | ✗ +0,0244 | ✓ +0,26 | ✓ +0,1688 | ✓ −0,220 | ✓ +0,169 | ✗ 0,67 vs 0,83 (nul plus cohérent) |
| DepMap (45) | ✗ +0,0116 | ✓ +0,24 | ✓ +0,1904 | ✓ −0,541 (sens négatif) | indisponible (n < 75) | ✗ 0,50 vs 0,67 |
| **Total** | **1/8** | **6/8** | **6/8** | **4/8** | **4/5 dispo.** | **2/8** |

Annexe, 23 paires secondaires (§8.35) : Delta 13/23 ; MC **2/23** ; maxsep **16/23** ;
L7a 12/23 ; falsification 7/18 **avec direction majoritaire inversée** ; T_0 23/23 et
cascade 23/23 — **triviaux par construction** (un nul place toujours son seuil ailleurs),
ils ne prouvent rien (§8.35).

**Le point dur, confirmé chiffre par chiffre.** Sur les bras principaux, les scores
vedettes ne séparent pas : MC 1/8 (HP35 seul ; les 7 écarts PDAC, +0,006 à +0,055,
sont tous sous la gigue v6.1 de ±0,07 — et 7/8 sont positifs, le MC « penche du bon
côté » sans jamais dépasser le bruit) ; L7a 4/8, et dans le sens négatif (le réel vote
plus « down » / moins confiant « up » que le nul) avec deux inversions de sens
(GSE62452, ICGC) ; la falsification n'est pas une comparaison au nul permuté et sa
direction s'inverse en annexe. **Seuls Delta (6/8) et maxsep (6/8) atteignent la
barre — et Delta échoue justement sur HP35, le témoin positif** (−0,09), tandis que
deux de ses six écarts sont petits (ICGC +0,07 ; GSE62452 +0,15). La phrase du
protocole (« le pipeline, en l'état, ne sépare pas réel et nul ») reste vraie pour
l'essentiel de l'instrument (§8.35).

### 2b. Lot étendu v6.1, §8.31 (44 runs, 21 paires complètes)

MC, Delta, falsification **ne séparent pas dans l'ensemble** : falsification > 0,5
sur **16/21 réels contre 15/21 nuls** ; cascades identiques à v6 sur 41/41 comparables.
Les trois plus grands écarts lus flux par flux ne tiennent pas comme preuves :
pureté = artefact du terme robustesse (0,808 contre 0) ; CLDN18 = doublon de
construction + vraie co-expression ; immunitaire = nul anormalement bas (Delta 2,30).

### 2c. Rotations de contrôle, §8.32 (96 runs, 48 paires) — aucun contrôle ne sépare

| Score | Résultat (48 paires) |
|---|---|
| MC | Écart moyen réel−nul **+0,044** (V4ROT +0,051 ; DEPMAPROT +0,033 ; IMMROT +0,056 ; PARPROT +0,035) ; le nul dépasse le réel sur **9/48** paires ; seuls 17/48 écarts positifs dépassent 0,07 (§8.41) ; la robustesse au plancher (~3,4e-41 sur 35/96 runs) fait passer 5 nuls au-dessus de leur réel |
| Delta | Sauts de niveau discrets de d_div, pas une séparation continue (IFNG +2,396 = nul tombé au niveau bas 3,38 ; les deux côtés visitent tous les niveaux) ; Delta = d_div − d_sat, erreur max 0,0009 sur les 96 runs |
| L7a | Directions et confiances se recouvrent entièrement entre réel et nul dans les 4 familles |
| Falsification | > 0,5 presque partout, réel comme nul (V4ROT 12/12 des deux côtés) ; indisponible sur les 24 runs DEPMAPROT (n = 45 < 75) |
| **maxsep / S_sep** | **Avec doublon : 48/48 (§8.41)** — mais voir §2d. **Sans doublon : 37/48 (règle A, 0,07) et 42/48 (règle B, gigue 0) (§8.44)** |

### 2d. Ce qui sépare réellement — et dans quelles conditions

- **maxsep / S_sep est le seul indicateur qui tient sur plusieurs comptages** :
  principales 6/8 (§8.35, §8.56, §8.59), annexe 16/23, rotations sans doublon
  37/48 (A) / 42/48 (B) (§8.44), paires indépendantes A2 **10/15** au plancher,
  12/15 positifs (§8.88), HP35 +1,6512. S_sep ≈ maxsep × ~0,99 partout (stabilité
  saturée 0,95–1,00) : **S_sep n'apporte rien au-delà de maxsep** (§8.37, §8.38,
  §8.41, §8.44).
- **Conditions et fragilités, toutes mesurées.**
  - Le 48/48 avec doublon (§8.41) était doublon-assisté à la marge : sans doublon,
    la perte vient du réel (S_sep réel 0,7570 → 0,5780, −0,1790 ; nul 0,2209 →
    0,2205, −0,0005). 11 paires tombent sous la règle A ; DEPMAPROT est la famille
    fragile (6/12 sous A) ; MUC16 passe de 0,0012 au-dessus du plancher (+0,0712).
  - maxsep passe A2 exactement au minimum (6/8) ; retirer n'importe laquelle des
    6 paires passantes donne 5/7 (D3 échoue, §8.59) ; au plancher équivalent-sep,
    A2 tombe à 5/8 (D4 échoue, ICGC tombe) ; au plancher 0,20 (petit effet de Cohen),
    maxsep ne sépare plus que 3/8 (§8.59).
  - Les paires indépendantes ne sont pas unanimes : 5 des 15 ne passent pas le
    plancher (GSE21501 −0,0100 ; GSE79668 +0,0567, renversée en consolidation ;
    GSE194249 −0,0239 ; et 2 autres parmi les 8 principales : GSE71729 +0,0402,
    GSE62452 −0,0036). Le LOO de A2 est 9/14 (§8.88).
  - Le §8.41 le dit lui-même : sur une série ordonnée par l'un de ses propres flux,
    « S_sep ne fait que constater que la série réelle est ordonnée et que les flux
    suivent cet ordre — c'est vrai par construction, pas une découverte sur le
    cancer ». Un 37/48 ou 48/48 sur des séries construites pour être ordonnées ne
    dit rien d'une transition biologique ni d'un remède.
- **Consolidations par nuls frais (§8.50, §8.72, §8.87).** MTAP : 10/10 nuls frais
  au-dessus du plancher (d min +0,1110, médiane +0,1595, max +0,1981 ; 13/13 avec
  les 3 anciens) — la consolidation la plus solide du dossier. GSE79668 : RENVERSE.
  GDC : FRAGILE CONFIRMÉ (d_médian +0,0314, rang 13/14, réel sous le p95 des nuls).
  Leçon du §8.53 : à n ≈ 70, un seul nul ne suffit pas — plancher honnête p95 de
  0,38 (ICGC) / 0,36 (GSE62452) sur 1 000 tirages, ~200 nuls requis pour un plancher
  stable ; le réel ICGC (0,2289) est sous ce plancher.
- **Tests A, C, MTAP, PRMT5 (§8.34, §8.45, §8.36, §8.43) : le nul gagne ou égale
  partout en MC/Delta/falsification** (voir tableau §1, lignes 16–19). Seuls maxsep
  et le sens opposé de L7a vont dans le sens réel — pistes, pas preuves.
- **v6.2 ne sépare pas mieux que v6.1** (§8.37) : S_sep 6/8 identique à maxsep v6.1
  (29/29 paires identiques au chiffre près, écart max 0,0000, §8.38) ; MC 7/8 et
  maxsep 7/8 en v6.2 viennent seulement de la gigue appliquée (0,00 mesurée au lieu
  de 0,07) — avec le plancher 0,07, les verdicts seraient ceux de la v6.1.
- **v6.3 et v6.4 rejetées** (§8.49, §8.52) : recompositions du MC, principales 4/8
  dans les deux cas (< 6/8 exigé) ; v6.2 reste la version de travail.

### 2e. Où le pipeline sépare, en une ligne par système

| Système | MC | Delta | L7a | Falsification | maxsep |
|---|---|---|---|---|---|
| HP35 (témoin positif) | ✓ | ✗ (nul devant) | ✗ | ✓ | ✓ (+1,65) |
| TCGA v4 | ✗ | ✓ | ✓ (sens négatif) | ✓ | ✓ |
| GSE71729 | ✗ | ✗ | ✗ | ✓ | ✗ |
| GSE62452 | ✗ | ✓ (petit) | ✗ (inversé) | n/d | ✗ |
| ICGC | ✗ | ✓ (petit) | ✗ (inversé) | n/d | ✓ (fragile, +0,097) |
| Immunitaire TCGA | ✗ | ✓ (nul bas) | ✓ (sens négatif) | ✗ (inversé) | ✓ |
| PARP TCGA | ✗ | ✓ | ✓ | ✓ | ✓ |
| DepMap CRISPR | ✗ | ✓ | ✓ (sens négatif) | n/d | ✓ |
| CPTAC protéine (63/52) | ✗ (non rapporté séparément ; Delta ≈ nul) | ✗ (≈ nul) | NaN en v6, faible en v6.1 | n/d | non séparant (lot §8.31) |
| LUAD / COAD | ✗ | ✗ (≈ nul) | — | — | non séparant (§8.27) |
| Rotations 48 | ✗ (+0,044 moy.) | ✗ (niveaux) | ✗ | ✗ | ✓ 37/48 sans doublon |
| Test A / C / MTAP | ✗ (nul devant) | ✗ (nul devant) | ~ (sens opposé seul) | ✗ (nul devant) | ✓ (piste seule) |
| Paires indépendantes (15) | non compté en MC | non compté | non compté | n/d | ✓ 10/15 |
| GBM / UVM / GSE62165 | — | — | — | — | ✗ |

---

## (3) Liste des limites connues et vérifiables

1. **n minimum 40 en mode fast** (§8.30 : min_len 50 → 40 pour laisser passer DepMap,
   n = 45, marge 5). En dessous de 40, le run est bloqué. Conséquences mesurées :
   série par allèle KRAS impossible (max 23 lignées G12D < 40, §8.36) ; groupes
   TP53/SMAD4/CDKN2A impossibles (plus grand groupe 38 < 40, §8.36).
2. **L7a NaN sous n = 75** (§8.14, cause trouvée de bout en bout) : le diagnostic de
   bruit coupe en 5 bins et exige ≥ 15 points par bin → Hurst échoue → score NaN →
   `top_csd` sans protection → risque NaN → vote « up » par accident, confiance
   repliée à 0,50. Tous les « up 0,500 » des petits runs v6 (CPTAC, GSE62452, ICGC)
   étaient de faux votes. Corrigé en v6.1 par des gardes (§8.30) : votes désormais
   finis mais faibles (0,15–0,36, §8.31).
3. **Falsification indisponible sous n = 75** (§8.30, §8.35) : « comparaison impossible
   sans les deux dimensions » (dimension spectrale dégénérée sous 75). DepMap (45),
   GSE62452 (69), ICGC (70), GSE79668 (51), GSE60979 (49), GSE131050 (42) n'ont pas
   ce test. Et la falsification, quand elle existe, compare d_crit à la dimension
   spectrale — pas au nul permuté (§8.31).
4. **Gigue L5 en v6.1, résolue en v6.2** (§8.30, §8.37) : hachage Python non
   déterministe → gigue ±0,07 sur L4/L7a/MC en v6.1 ; v6.2 (hachage stable SHA-256)
   mesurée à **0,0000 sur tous les indicateurs** (20 runs × 2, §8.37). La gigue ne
   cachait pas une séparation : avec le plancher 0,07, les verdicts v6.2 sont ceux
   de la v6.1.
5. **Doublon contrôle = flux dans les rotations** (§8.32) : les 48 CSV avaient 13
   colonnes, le contrôle figurant aussi parmi les flux ; à T_0, le doublon domine
   partout dans le réel (d de Cohen +2,00 à +4,69, 48/48). Corrigé par re-run sans
   doublon (§8.44) : 37/48 sous la règle A, 42/48 sous la règle B — le compteur
   avec doublon (48/48) était gonflé à la marge.
6. **Delta non élucidé** (§8.39, §8.42, §8.57, §8.62) : 222 runs, meilleure combinaison
   80,2 % (exigé 90 %) ; aucun modèle, aucun hold-out ne passe ; les magnitudes
   portent l'échelle de n (log n), pas le contenu des flux ; pas de loi d'échelle en
   n (R² = 0,599, LOCO R² = −0,005, §8.62). Delta reste « une piste fragile »,
   pas un discriminateur recommandé.
7. **Pic étroit non élucidé** (§8.73) : aucun déclencheur identifiable (bloc extrême
   1/11, transplantation 0/3 et 0/6, AUC 0,31–0,47) ; l'étroitesse est une propriété
   fragile de l'arrangement exact des lignes, pas un artefact de calcul — mais elle
   n'est portée par aucun bloc, aucune ligne, aucune queue de distribution.
8. **Mécanismes §8.63 : 2 sur 3 expliqués, le troisième partiel** ; clôture M2 : la
   réplication tient à 80 %, pas 85 % (§8.75).
9. **Score MC composite défectueux, documenté** (§8.49, défauts D1–D5) : robustesse
   morte (≤ 2×10⁻⁷ sur 14/16 JSON PDAC, souvent ~1e-41), stabilité saturée
   (0,978–0,997), netteté qui récompense le bruit, s_norm qui sature, malédiction
   du vainqueur. C'est pour cela que MC ne voit pas la séparation que maxsep voit
   seul — et que deux recompositions (v6.3, v6.4) ont été construites puis rejetées.
10. **Plancher 0,07 fragile** : 0,07 en |d| est en dessous du « petit » effet de
    Cohen (0,2) ; au plancher 0,20, maxsep ne sépare plus que 3/8 principales
    (§8.59) ; MUC16 passe de 0,0003, GSE131050-FF de 0,0039, GDC de 0,0184.
11. **Le nul est un ordre détruit, pas un faux biologique** : permutation des lignes,
    graine 42, contrôle intact. Un écart réel−nul dit « la série réelle est ordonnée »,
    pas « il y a une rupture biologique » (§8.41). À petit n, un seul tirage de nul
    ne suffit pas (§8.53, §8.70, §8.72).
12. **L7b fermé comme non informatif** (verdict clos le 13 nov., rappelé §8.31 et
    partout : « FRAGILE » sur le réel comme sur le nul, y compris sur HP35).
    Il ne doit jamais être rapporté comme une mesure de fragilité de l'instrument.
13. **Reproductibilité des données réparée, pas celle des verdicts** (§8.77) : 19/19
    gaps d'URL fermés, test à froid TCGA v4 à 0,0 exact — mais sur une seule paire ;
    les matrices brutes (~2,4 Go) et les résultats (~7 Go) restent hors dépôt.
14. **Systèmes jamais testés — nommés explicitement au §8.33** : **pas de vrai temps**
    (l'ordre KRAS ou tout autre flux est un classement, pas une horloge ; un « seuil »
    est une coupure dans un classement, pas un moment) ; **pas de single-cell**
    (tout est du bulk ou des lignées, rien cellule par cellule sur le disque) ;
    **pas de spatial** (aucune coordonnée dans la tumeur) ; **pas de longitudinal**
    (aucune tumeur mesurée deux fois, avant/après traitement). À quoi s'ajoutent :
    pas de dose ni de réponse à un traitement comme axe (sauf le lot drogue Chen,
    exploratoire, §8.84) ; pas d'autre cancer que PAAD / LUAD / COAD / GBM / UVM ;
    pas d'autre protéine que HP35 ; pas d'Ising en v6 (voir §1) ; pas de Cosmo /
    Climat / Finance en v6.2. Ce qui manque pour ces quatre impossibilités, ce sont
    d'autres données, pas d'autres runs du même pipeline (§8.33).
15. **La chaîne KRAS est propre à l'axe KRAS** : elle ne réapparaît ni sous les 48
    contrôles (§8.32), ni sous l'ordre prolifération (§8.34), ni sous l'ordre MTAP
    (§8.36), ni par stade (§8.45), ni dans le GBM (§8.82). Ce qui est réel, c'est
    le bloc et son anti-corrélation avec MUC16 — pas la lecture « rupture ».
16. **Tout verdict clinique vient d'ailleurs** : daraxonrasib, vopimetostat +
    daraxonrasib, IBI343 (§8.20, §8.22) sont des avancées trouvées (essais, FDA),
    pas des prédictions du pipeline ; les 3 blocs de co-expression et la chaîne
    sont des faits de tests directs, pas des verdicts du pipeline (§8.35).

---

## (4) Ce que le pipeline PEUT affirmer, et ce qu'il NE PEUT PAS affirmer

Langage simple, sans jargon. Chaque ligne renvoie à sa section. « Le pipeline »
veut dire ici : la batterie entière (voir §5), jamais un score seul.

### Le pipeline PEUT affirmer

1. **« Sur une série rangée dans un ordre, je place des seuils, et ces seuils ne
   tombent pas au même endroit quand on mélange l'ordre. »** Les cascades réel/nul
   diffèrent sur toutes les paires (§8.35 : T_0 8/8, cascade 8/8 — mais c'est
   trivial par construction, voir « ne peut pas » n° 2).
2. **« Quand une série est rangée par l'un de ses propres ingrédients, mes autres
   ingrédients suivent cet ordre — et un mélange ne le fait pas. »** C'est ce que
   mesure maxsep : 37/48 rotations sans doublon (§8.44), 6/8 paires principales
   (§8.35), 10/15 paires indépendantes (§8.88).
3. **« Sur le repliement d'une petite protéine (HP35), je vois une vraie différence
   entre le réel et le mélange, avec mon score principal comme avec maxsep. »**
   MC +0,1950, maxsep +1,6512 (§8.35). C'est le seul système où les deux tiennent.
4. **« Je peux dire, sur une série, dans quel sens les ingrédients penchent
   (vers le haut ou vers le bas) et avec quelle confiance — quand la série est
   assez longue. »** Vote L7a, fini et honnête en v6.1/v6.2 (§8.30, §8.31) ;
   en dessous de 75 points, il ne disait rien en v6 (faux « up », §8.14).
5. **« Je peux mesurer si des groupes d'ingrédients bougent ensemble. »** Les 3
   blocs de co-expression (estomac/mucus, immunitaire, réparation) sont confirmés
   par tests directs, réel bien au-dessus du bruit des nuls (§8.32).
6. **« Je peux dire où tombe un seuil le long d'un classement, et ce que ce seuil
   mesure (pureté, sexe, tumeur) change selon la couche. »** TCGA v1 → v4 (§8.1–§8.4,
   §8.5) ; chaque version décrit sa propre fenêtre.
7. **« Je suis reproductible : relancé deux fois, je donne exactement les mêmes
   chiffres. »** Gigue v6.2 mesurée à 0,0000 (§8.37) ; test à froid TCGA v4 à 0,0
   exact (§8.77).
8. **« Sur le pancréas, quand on me donne une nouvelle cohorte indépendante, je
   sépare le réel du mélange environ deux fois sur trois avec maxsep. »**
   A2 10/15 (§8.88) — ni plus, ni moins.
9. **« Je peux dire, avec la batterie entière, quand une piste ne tient pas. »**
   Exemples : Test A (§8.34), Test C (§8.45), série MTAP (§8.36), GBM (§8.82),
   GSE194249 (§8.88) — tous NON, chiffres à l'appui.

### Le pipeline NE PEUT PAS affirmer

1. **« Ceci est réel, ceci est un mélange » avec ses scores principaux.** MC 1/8,
   L7a 4/8, cohérence des flux 2/8 (§8.35) ; MC/Delta/falsification ne séparent pas
   dans l'ensemble du lot étendu (§8.31) ; aucun des 48 contrôles ne sépare par
   MC/Delta/L7a/falsification (§8.32). Le MC penche du bon côté 7 fois sur 8 mais
   reste sous le bruit.
2. **« Le seuil tombe ailleurs, donc j'ai trouvé quelque chose. »** La position du
   seuil et la cascade diffèrent toujours entre réel et mélange (8/8) — par
   construction, un mélange place son seuil ailleurs (§8.35). Ce n'est pas une preuve.
3. **« J'ai trouvé une rupture biologique / un remède. »** maxsep constate un ordre,
   pas une transition (§8.41) ; aucun remède ne vient du pipeline — les remèdes du
   dossier viennent des essais cliniques (§8.20, §8.22, §8.35).
4. **« La chaîne du pancréas existe partout. »** Elle est propre à l'axe KRAS et ne
   réapparaît sous aucun autre ordre (§8.32, §8.34, §8.36, §8.45, §8.82).
5. **« Mon score Delta prouve quelque chose. »** Delta n'est pas élucidé (§8.39,
   §8.42, §8.57, §8.62) ; ses écarts viennent de sauts de niveau internes (§8.32) ;
   il échoue sur le témoin positif HP35 (§8.35).
6. **« Je suis fragile / robuste. »** L7b dit FRAGILE sur le réel comme sur le nul,
   partout — il est clos comme non informatif (§8.31). Ne jamais le citer comme une
   mesure de fragilité.
7. **« Je fonctionne sur n'importe quelle série. »** Bloqué sous 40 points (§8.30) ;
   L7a muet sous 75 en v6 (§8.14) ; falsification absente sous 75 (§8.30) ; jamais
   testé sur le vrai temps, le single-cell, le spatial, le longitudinal (§8.33).
8. **« Un seul chiffre suffit. »** Aucun élément seul ne porte un verdict — voir §5
   (correction de Zackary, 21 nov. 2026). Ni MC seul, ni maxsep seul, ni un seul
   estimateur, ni un seul nul.
9. **« Je sépare mieux depuis la v6.2. »** Faux : v6.2 sépare pareil que v6.1, de
   façon déterministe (§8.37, §8.38).
10. **« Je suis universel au sens où je marche sur tout, partout, pareil. »**
    Voir le résumé (§6) : ce mot-là, tel quel, est exagéré.

---

## (5) La batterie complète — vérification de la correction de Zackary (21 nov. 2026, 11h00)

### 5.1 Ce que Zackary corrige

> MC n'est JAMAIS seul. Dans le pipeline, MC est accompagné de toute la batterie :
> les 29 estimateurs, les 6 questions (Q1–Q6), les tests de bruit, les F1/F2 avant
> et après seuil, et le reste (L7a/L7b, falsification, Delta, maxsep). Aucun verdict
> ne repose sur MC seul, ni sur maxsep seul.

### 5.2 Vérification 1 — la batterie est-elle réellement émise à chaque run ? OUI, vérifié dans le JSON

Lecture seule de `~/workspace/runs/pdac-v6/results_fast_tcga_v4/master_results.json`
(run v6.2, TCGA v4 réel). Un seul run émet, ensemble, dans le même fichier :

| Élément de la batterie | Présent dans le JSON | Détail vérifié |
|---|---|---|
| 29 estimateurs | ✓ | `run_pipeline.transition_analysis` : 29 noms — Higuchi, DFA, Katz, Hurst, SampleEn, Petrosian, Sevcik, BoxCounting, PermutationEntropy, CorrelationD2, GrassbergerProcaccia, InformationD1, VisibilityGraph, TwoNN, DANCo, Fisher, LevinaBickel, PCAIntrinsic, LocalPCA, GraphDimension, PersistentHomology, MFA, KolmogorovLZ, SpectralBeta, SpectralDimension, Hurst2mH, Lyapunov, MultifractalDeltaAlpha, SingularityFmax. L'agrégation holographique le confirme : `cross_estimator_z_of_29_raw_medians` |
| 6 questions Q1–Q6 | ✓ | `run_pipeline.scores` : Q1_Calme_vs_Chaos, Q2_Tension_Seuil, Q3_Agressivite, Q4_Persistence, Q5_Active_Reactive, Q6_Active_Reactive_Scaled |
| Tests de bruit | ✓ (un bloc par run, par flux) | `run_pipeline.noise_diagnostic` : `diagnostic_label`, `verdict_level` (ici MEDIUM_HIGH, « Proxy de variance modéré »), scores par flux. **Réserve : l'expression « 4 tests de bruit » n'a pas été retrouvée comme un ensemble nommé, ni dans le livre blanc ni dans le JSON** — le diagnostic de bruit existe et sort à chaque run, mais son décompte en « 4 tests » n'est pas vérifiable tel quel (voir §5.4) |
| F1/F2 avant et après seuil | ✓ | `five_threshold_cascade` : T_-2 (F2, pré-début), T_-1 (F1, pré-inflexion), T_0 (Monte-Carlo, central), T_+1 (F1, post-décélération), T_+2 (F2, post-attracteur) ; `max_F1_velocity`, `max_F2_curvature` ; `transition_analysis` par estimateur |
| L7a / L7b | ✓ | `prediction_levels` : L1, L2, L3, L4, L5, L6, L7_consensus, L7a_coherence, L7b_robustesse |
| Falsification | ✓ | `reading_synthesis.falsification_vs_null` : delta_vs_null 0,849386, seuil 0,5 — avec sa note : « Null = cadre de mesure / résidu d'instrumentation, pas un d interchangeable pour T_log » |
| Delta | ✓ | `holographic_tension_state.Delta_tension` = 4,181387 ; D_vector {d_sat, d_crit, d_div, d_null} |
| MC et maxsep, ensemble | ✓ | `threshold_metadata.threshold_optimization.best_config` : `score` 0,3720 (ancien composite) **et** `metrics` {max_separation 0,4623 ; s_norm 0,2271 ; stability 0,9837 ; robustness 3,37e-41 ; sharpness 0,0439} — **MC et maxsep sortent dans le même objet, à chaque run : MC n'est jamais seul dans la sortie** |
| Cascade Q1–Q5 | ✓ | `five_threshold_cascade` (à ne pas confondre avec les questions Q1–Q6 : même lettres, objets différents — voir §5.4) |

**Le code lui-même interdit le verdict à un seul élément.** Le champ `L7b_robustesse.lecture`
du même JSON dit : « Ne pas utiliser L7a seul pour décider. » Et la note du vote L7
précise : « Q1-Q6, T_log et le score de seuil ne sont pas lus » par ce vote — les
éléments sont des lectures parallèles, pas un verdict fusionné. La batterie existe
donc comme sortie ; elle n'existe pas comme une règle écrite « aucun verdict sans
la batterie » — c'est exactement ce que la correction de Zackary ajoute.

### 5.3 Vérification 2 — la batterie est-elle présentée comme obligatoire dans le livre blanc ? NON — documentée, pas codifiée

Comptages refaits par grep sur le livre blanc le 21 nov. 2026 (méthode : `grep -o`,
puis `grep -c` par ligne) :

| Terme | Mesuré ici | Remarque |
|---|---|---|
| « F1 » | 116 occurrences (sous-chaîne) ; 90 en mot entier ; 36 occurrences de « F1/F2 » | Le chiffre 97 transmis avec la mission **ne se reproduit par aucune de ces deux méthodes** — écart à consigner, pas à gommer |
| « 29 estimateurs » | 9 lignes ; 11 occurrences | Le chiffre 9 correspond au comptage **par lignes** |
| « test de bruit » | 6 lignes ; « diagnostic de bruit » 5 lignes ; « bruit » 100 occurrences | Le chiffre 19 transmis **ne se reproduit par aucune de ces méthodes** — écart à consigner |
| « batterie » | **0 occurrence** | Le mot n'existe pas dans le livre blanc : la batterie n'y est jamais nommée comme un tout obligatoire |
| Q1–Q6 (questions) | présentes dans les clés JSON ; dans le texte, « Q1–Q5 » désigne la **cascade** (5 positions), pas les questions | Risque de confusion réel entre les deux usages de « Q1… » |

Conclusion : la batterie est **documentée partout, en pièces détachées** (F1/F2 dans
presque chaque section de lecture flux par flux ; bruit dans chaque diagnostic ;
29 estimateurs dans les sections Delta ; L7a/L7b, falsification, Delta, maxsep dans
chaque table de paires) — mais **jamais présentée comme obligatoire ni comme un
tout** : aucune phrase du livre blanc ne dit « aucun verdict ne repose sur un seul
élément », aucune section n'énumère la batterie comme condition d'un verdict.
Elle est un décor de fait, pas une règle. La correction de Zackary est donc une
règle **nouvelle**, pas un rappel — et c'est comme telle qu'elle doit entrer au §8.90.

### 5.4 Vérification 3 — le livre blanc présente-t-il maxsep comme « le » score qui décide seul ? OUI, à trois endroits — c'est la survente à corriger

**Lieu 1 — §8.56, titre et verdict.** Titre : « sep seul ou maxsep seul
suffisent-ils comme score MC ? » Verdict : « **`maxsep` seul SUFFIT aux quatre
barres gelées** » (A1 37/48, A2 6/8, A3 HP35 +1,6512). Le mot « seul » est dans
le titre, dans le verdict, et dans le journal §7 (ligne 215). « Suffit » y veut
dire : suffit aux quatre barres de *séparation* — mais lu sans le protocole, il
se lit : un seul score suffit. C'est la formulation qui a nourri le podcast
(« on a trouvé mieux que juste les tests nuls, quelque chose à voir avec MC »,
§8.90).

**Lieu 2 — §8.59, titre et verdict.** Titre : « Trancher l'adoption de `maxsep`
seul comme score MC ». Verdict : « ADOPTER SOUS CONDITION » — avec D3 et D4 en
échec, c'est-à-dire : le verdict de suffisance tient à une paire (ICGC) et à
l'échelle du plancher. Le journal §7 (ligne 218) reprend « maxsep seul » sans
la fragilité en tête.

**Lieu 3 — §7 (journal des expériences), lignes 215 et 218.** Le §7 est le
journal, pas un résumé — mais c'est lui que l'on relit en premier, et ses deux
lignes disent « maxsep seul SUFFIT » / « ADOPTER SOUS CONDITION » sans rappeler
que la batterie entière accompagne chaque run.

**Ce qui, à l'inverse, limite déjà la survente — et qu'il faut garder.**
- **§8.64.6, convention d'affichage** (forme exacte, figée) : maxsep score
  principal AFFICHÉ, **ancien MC affiché EN SECOND partout où maxsep est affiché**
  (« Aucune table future n'affiche `maxsep` sans son ancien MC en second »),
  `sep` compagnon borné, plancher publié en unités |d|, mention de fragilité en
  tête de chaque table. **Point 6 : la sélection du best_config continue
  d'utiliser l'ancien composite** — maxsep ne choisit même pas le seuil qu'il
  affiche. « Score principal affiché » ne veut donc pas dire « décide » : il
  veut dire « lu en premier dans la table ».
- **§8.64.12 (20 nov. 2026, 13h04)** : l'adoption pleine est « la décision de
  Zackary, prise après lecture des §8.56/§8.59/§8.64 — **pas une preuve nouvelle**,
  pas un verdict de ce chantier ni d'un autre ».
- **§8.35** : « ses scores vedettes ne discriminent pas » ; §8.41 : S_sep « ne
  fait que constater que la série réelle est ordonnée ».

**Le défaut qui reste, même avec §8.64.6.** La convention d'affichage ne couvre
que **trois** scores (maxsep + ancien MC + sep). Elle n'exige ni L7a, ni Delta,
ni falsification, ni F1/F2, ni bruit, ni cascade dans la table. Une table
conforme à §8.64.6 peut donc encore se lire comme « maxsep décide, les deux
autres accompagnent » — et c'est exactement la lecture que la correction de
Zackary interdit. **La survente n'est pas dans le mot « principal », elle est
dans le mot « seul » (§8.56/§8.59) et dans l'absence de la batterie dans la
convention d'affichage.**

### 5.5 Ce que la batterie COMPLÈTE permet d'affirmer — en langage simple

Un seul élément, c'est une seule question posée à la série. La batterie, c'est
douze questions posées en même temps, qui ne se recouvrent pas :

- les 29 estimateurs disent **quelle forme** a la série (rugueuse ? lisse ?
  qui se répète ?) — un seul estimateur peut mentir, 29 qui se contredisent
  disent « je ne sais pas » ;
- Q1–Q6 disent **dans quel état** est la série (calme ou chaos ? tendue ?
  agressive ? qui persiste ? qui réagit ?) — une seule question peut être
  trompée par un artefact, six qui désaccordent disent « méfiance » ;
- le bruit dit **si ce qu'on voit n'est pas juste du bruit** — sans lui, un
  seuil sur du bruit ressemble à un seuil sur du signal ;
- F1/F2 disent **comment ça bouge avant et après le seuil** (ça accélère ?
  ça se courbe ?) — un seuil sans avant/après n'est qu'une coupure ;
- L7a dit **dans quel sens ça penche**, L7b dit **si ce vote tient quand on
  change de fenêtre** — sans L7b, on ne sait pas si le vote survit à un
  décalage d'une ligne ;
- la falsification dit **si la géométrie interne se contredit** — sans elle,
  on peut annoncer une structure que les propres chiffres contredisent ;
- Delta dit **quelle tension** il y a entre les trois mesures de dimension —
  sans lui, on ne voit pas que l'instrument est tombé dans un niveau discret ;
- MC dit **quel est le meilleur compromis** entre séparation, stabilité,
  robustesse et netteté — et maxsep dit **quelle est la plus grande séparation
  brute**, sans compromis.

**Retirer un seul élément, c'est retirer une question — et la réponse des
autres ne la remplace pas.** Exemples mesurés dans le dossier : sans la
robustesse, on ne voit pas que le MC de la pureté est un artefact (0,808
contre 0, §8.31) ; sans les F1/F2, on ne voit pas que le nul est parfois plus
« cohérent » que le réel à son propre seuil (§8.35) ; sans le bruit, on ne voit
pas que les votes L7a sous 75 points étaient des NaN déguisés en « up »
(§8.14) ; sans les 29 estimateurs, on ne voit pas que Delta tombe dans des
niveaux discrets (§8.32). **Aucun élément seul ne porte un verdict — pas
même maxsep, pas même la batterie moins un.**

Ajouts aux listes du §4 (à lire avec elles) :
- **PEUT (batterie)** : « Avec les douze questions ensemble, je peux dire si
  une séparation tient, ou si c'est un artefact d'un seul ingrédient. »
- **NE PEUT PAS (batterie)** : « Avec un seul chiffre — MC seul, maxsep seul,
  un seul estimateur, un seul nul — je ne peux rien affirmer. Un chiffre seul
  n'est pas un verdict, c'est une lecture. »

### 5.6 Addendum daté proposé pour le §8.90 (correction de Zackary, 21 nov. 2026)

> **Addendum daté — correction apportée par Zackary, 21 novembre 2026, 11h00.
> MC n'est JAMAIS seul.** Dans le pipeline, MC sort toujours accompagné de toute
> la batterie : les 29 estimateurs, les 6 questions (Q1–Q6), les tests de bruit,
> les F1/F2 avant et après seuil, L7a/L7b, la falsification, Delta et maxsep —
> vérifié dans chaque `master_results.json` (ex. TCGA v4, v6.2). **Aucun verdict
> ne repose sur MC seul, ni sur maxsep seul.** Les formulations « `maxsep` seul
> SUFFIT » (§8.56) et « adoption de `maxsep` seul » (§8.59, journal §7 lignes
> 215/218) sont des surventes : elles portaient sur les barres de séparation,
> pas sur le verdict. **maxsep est le score principal AFFICHÉ (§8.64.6, §8.64.12),
> pas le verdict ; le verdict, c'est la batterie entière.** La convention
> d'affichage §8.64.6 est complétée : aucune table future n'affiche un score
> sans rappeler que le verdict exige la batterie entière, et aucun élément seul
> ne porte un verdict. La sélection du best_config continue d'utiliser l'ancien
> composite (§8.64.6, point 6). **Réserve de comptage :** les occurrences
> « F1 » (116 en sous-chaîne, 90 en mot entier) et « test de bruit » (6 lignes)
> mesurées dans ce volet ne reproduisent pas les chiffres 97 et 19 transmis
> avec la mission ; « 29 estimateurs » (9 lignes) se reproduit ; le mot
> « batterie » a 0 occurrence dans le livre blanc ; l'ensemble « 4 tests de
> bruit » n'a pas été retrouvé comme un ensemble nommé — le diagnostic de
> bruit, lui, sort à chaque run. Ces écarts sont consignés, pas gommés.

---

## (6) Résumé final (5 lignes maximum)

**Correction de Zackary (21 nov. 2026, 11h00) en tête : MC n'est jamais seul — la
batterie entière (29 estimateurs, Q1–Q6, bruit, F1/F2, L7a/L7b, falsification,
Delta, maxsep) accompagne chaque run, et les formulations « maxsep seul SUFFIT »
(§8.56/§8.59) sont une survente à corriger par addendum daté : maxsep est le score
principal AFFICHÉ, pas le verdict.**
Ligne 2 : le pipeline a vraiment tourné sur un seul témoin positif (HP35, n = 1 000),
le pancréas sous ~30 formes (TCGA, GEO, ICGC, CPTAC, DepMap, organoïdes, drogue)
et trois autres cancers (LUAD, COAD, GBM, UVM) — jamais sur l'Ising en v6, jamais
sur le vrai temps, le single-cell, le spatial ni le longitudinal.
Ligne 3 : MC, Delta, L7a et la falsification ne séparent pas le réel du nul sur les
bras principaux (MC 1/8, falsification 16/21 contre 15/21, rotations ΔMC +0,044) ;
seul maxsep tient (6/8, 37/48 sans doublon, A2 10/15), fragile (tient à une paire,
au plancher 0,07, à l'ordre construit).
Ligne 4 : le mot « universel » est donc **exagéré** tel quel — le pipeline n'est
ni un détecteur universel de ruptures, ni un instrument qui marche pareil partout.
Ligne 5 : redéfinition honnête en une phrase — **« Le pipeline est un instrument
de lecture ordonnée, reproductible et déterministe, qui place des seuils et mesure
une séparation (maxsep, avec toute sa batterie) sur des séries rangées dans un
ordre choisi, dans les systèmes où il a été testé — et qui ne prouve ni rupture,
ni remède, ni universalité au-delà de ces systèmes. »**

— Fin du volet 4. —
