# §8.38 S_sep appliqué aux bras existants

Date : 19 novembre 2026. Go : Zackary, « Lance tout cela », 19 nov. 2026 ~05h47.
Statut : section prête à insérer au livre blanc. Le livre blanc n'a pas été
modifié (un autre chantier y écrit en parallèle).

## Verdict d'abord

**S_sep ne classe aucun bras autrement que max_separation en v6.1.**
Sur les 29 paires distinctes relues (8 principales + 20 secondaires
distinctes + MTAP ; l'annexe compte 23 lignes dont 3 doublons des
paires principales),
S_sep en v6.2 est **identique à S_sep en v6.1 au chiffre près**
(max |Δ| = 0,0000 sur S_sep, max_separation, MC et Delta) : le hachage
stable L5 ne touche pas ces champs, comme le prévoyait le protocole §2.3.
La seule chose qui change un compteur, c'est la règle de gigue — et elle
change max_separation exactement pareil :

| Règle | S_sep, paires principales | max_separation, même règle |
|---|---|---|
| (A) gelée §3.4 : écart > 0,07 | **6/8** : HP35, TCGA v4, ICGC, immunitaire TCGA, PARP TCGA, DepMap ; échecs GSE71729 (+0,0405), GSE62452 (−0,0072) | v6.1 : 6/8, **mêmes paires** |
| (B) gigue 0 : écart > 0 | **7/8** : + GSE71729 ; échec GSE62452 seul | v6.2 : 7/8, **mêmes paires** |

En annexe (23 paires) : S_sep (A) **16/23**, exactement max_separation v6.1
(16/23, mêmes paires) ; S_sep (B) **20/23**, exactement max_separation v6.2
à gigue 0 (20/23, mêmes paires).

**Réserve explicite, à garder avec le chiffre : le passage de 6/8 à 7/8
(et de 16/23 à 20/23) vient uniquement du passage de la gigue appliquée
de 0,07 à 0,00. Les écarts réel−nul eux-mêmes sont identiques à ceux de
la v6.1 au chiffre près. Ce n'est pas une amélioration de l'instrument —
c'est le même écart mesuré contre un seuil devenu nul.** Le plancher 0,07
du protocole (§3.4) existe précisément pour que « écart > 0 » ne devienne
pas trivial ; la règle (B) est rapportée ici à la demande du chantier,
elle ne remplace pas la règle gelée (A).

Verdict par bras (détail au §8.38.2) :

| Bras | Paires | S_sep (A) 0,07 | S_sep (B) gigue 0 | Classe autrement que v6.1 ? |
|---|---|---|---|---|
| ATR | ATR_TCGA | passe (+0,2262) | passe | **Non** — identique à max_sep v6.1 (+0,2262, passait) |
| MTAP | MTAP (TCGA v4 ordonnée par CN MTAP) | passe (+0,1968) | passe | **Non** sur S_sep — mais MC (−0,1642) et Delta (−0,5416) restent inversés : bras contrasté, verdict §8.36 non renversé |
| Immunitaire | TCGA, GSE62452, GSE71729, ICGC | 3/4 passent ; ICGC inversé (−0,2200) | 3/4 passent ; ICGC inversé | **Non** — identique à max_sep v6.1 sur les 4 |
| PARP | TCGA, GSE71729 | 2/2 passent | 2/2 passent | **Non** — identique à max_sep v6.1 sur les 2 |
| Principales (Phase 2) | 8 paires | 6/8 | 7/8 | **Non** — identique à max_sep sous chaque règle |

## 8.38.1 Question, méthode, règles

**Question.** S_sep (formule gelée, PROTOCOL_v6.2.md §3 :
`S_sep = max_separation × stability`, lus dans le `best_config` de chaque
run) classe-t-il les pistes autrement que la v6.1, quand on le réapplique
aux bras déjà faits — ATR, MTAP, immunitaire, PARP — et aux paires
principales de la Phase 2 ?

**Méthode — relecture, pas recopie.** Toutes les valeurs ci-dessous ont été
relues dans les `master_results.json` par un extracteur indépendant,
`extract_ssep_838.py` (SHA-256
`d7b8bd663fb36340779ebb4d7ce307775d4e9896afee4a75236192cf026bb14a`),
écrit pour ce chantier ; les tables existantes n'ont servi que de
comparaison. Résultat de la comparaison :

- **0 écart** entre les valeurs relues et `v62_phase2_table.json`
  (max_separation, stabilité, S_sep, MC, Delta, L7a — 29 paires, tolérance
  10⁻⁶) ;
- **0 écart** entre les valeurs v6.1 relues et `v61_phase2_table.csv`
  (champs comparables, tolérance 5×10⁻⁵, le CSV étant arrondi) ;
- **S_sep v62 = S_sep v61 exactement sur 29/29 paires comparées**
  (max |Δ| = 0,0000) ; max_separation, MC et Delta aussi (0,0000).
  Seul le L7a signé bouge entre v6.1 et v6.2 (max 0,0304, sur TCGA_V2 ;
  ≤ 0,0041 partout ailleurs) — effet attendu du hachage stable L5 sur
  les votes, sans changement de verdict L7a sur les paires principales
  (4/8 inchangé).

**Règles de comptage.** Direction majoritaire = signe de la somme des
écarts réel−nul (comme `verdict()` de `extract_phase2.py`) ; une paire
« sépare » si |écart| > gigue ET signe = direction majoritaire. Deux
gigues sont appliquées et distinguées partout : **(A)** la règle gelée
§3.4, gigue effective = max(gigue mesurée 0,00 ; plancher 0,07) = **0,07** ;
**(B)** la gigue mesurée seule, **0,00** (commande de ce chantier), rapportée
à part avec la réserve ci-dessus. Nul : lignes permutées, graine 42,
colonne de contrôle intacte (convention du projet). Aucun nouveau seuil,
aucune sélection d'indicateur après coup.

**Nouveaux runs — un seul bras en demandait.** ATR, immunitaire et PARP
avaient déjà leurs runs v6.2 dans le lot phase 2 (66 dossiers). MTAP
n'y était pas : seuls les runs v6.1 existaient (`results_fast_v61_mtap`,
`results_fast_v61_mtap_nul`). Deux runs v6.2 ont donc été lancés pour ce
chantier, avec les CSV et le protocole existants, sans modifier aucun code :
manifeste `manifest_v62_mtap.txt`, lanceur reprenable `run_v62_lot.sh`
(existant), surveillance `watch_v62_mtap.sh` (miroir de
`watch_v61_mtap.sh`), unité systemd `v62-mtap-838`, log
`runs_v62_mtap.log` — 19 nov. 2026, 11h27–11h34 UTC, **2/2, exit 0**,
SHA v6.2 `f07567c4…` et SHA v6.1 `2af5e5ce…` confirmés dans le log.
Cascades MTAP v6.2 = v6.1 exactement (réel 0,54 / 60,74 / 72,77 / 92,11 /
92,11 % ; nul 1,07 / 2,14 / 8,57 / 15,58 / 15,58 %), comme l'exigeait le
protocole §5.3.

## 8.38.2 Résultats par bras

Les stabilités sont données parce qu'elles expliquent pourquoi S_sep ≈
max_separation ici (voir §8.38.3). Toutes les valeurs sont S_sep réel /
nul (écart réel−nul), relues dans les JSON v6.2.

### ATR — 1 paire (annexe Phase 2)

Série TCGA, 178 tumeurs, 12 flux de réparation de l'ADN (PARP1, PARP2,
BRCA1, BRCA2, ATM, ATR, CHEK1, CHEK2, RAD51, XRCC1, POLQ, FANCD2),
lignes ordonnées par résidu KRAS croissant, contrôle `step`
(PROVENANCE_atr_chek1.md).

| Paire | n | S_sep réel / nul | Écart | Stabilité R / N | (A) 0,07 | (B) 0 |
|---|---|---|---|---|---|---|
| ATR_TCGA | 178 | 0,3784 / 0,1522 | **+0,2262** | 0,9968 / 0,9917 | passe | passe |

Contexte, mêmes JSON v6.2 : max_separation +0,2262 (identique à v6.1),
MC +0,0331 (sous 0,07), Delta +0,0944, L7a signé −0,566 (réel down 0,161
contre nul up 0,406). **S_sep ne reclasse pas ATR** : il passait déjà en
max_separation v6.1 sous la gigue 0,07, il passe pareil en S_sep sous les
deux règles. Le bras ATR reste une piste à écart positif net (+0,23),
portée par max_separation/S_sep seuls — MC et Delta ne dépassent pas le
bruit historique sur cette paire.

### MTAP — 1 paire, nouveaux runs v6.2 (§8.36)

Série TCGA v4 ordonnée par nombre de copies MTAP croissant (perte profonde
d'abord), 177 tumeurs (177/178 appariées), contrôle `MTAPCN`, monotone
croissant (Spearman ordre vs valeur 0,99996). Voir
PROVENANCE_mtap_series.md.

| Paire | n | S_sep réel / nul | Écart | Stabilité R / N | (A) 0,07 | (B) 0 |
|---|---|---|---|---|---|---|
| MTAP | 177 | 0,3378 / 0,1409 | **+0,1968** | 0,9959 / 0,9825 | passe | passe |

Valeurs v6.2 vérifiées : max_separation 0,3392 / 0,1434 (+0,1957),
identiques à la v6.1 au chiffre près, ainsi que MC et Delta. **Mais les
autres indicateurs disent l'inverse, avec de gros écarts : MC 0,3511 /
0,5153 (−0,1642, le nul devant) et Delta 3,8051 / 4,3466 (−0,5416, le nul
devant)** ; L7a signé −0,7579 (réel down 0,427 contre nul up 0,331).
C'est le seul bras où S_sep/max_separation et MC/Delta se contredisent
aussi franchement.

**Lecture honnête : S_sep « sépare » sur MTAP, mais il ne renverse pas le
verdict §8.36 (NON).** Le NON de §8.36 était porté par le MC
(nul 0,515 > réel 0,351) ; ce fait est confirmé en v6.2, au chiffre près,
et Delta l'aggrave (−0,54). Un seul indicateur positif (S_sep, qui est
max_separation pondéré par ~0,99) contre deux indicateurs inversés ne
suffit pas à rouvrir la piste. MTAP reste le cas d'école de ce chantier :
S_sep hérite exactement des forces et des faiblesses de max_separation,
il ne les corrige pas.

### Immunitaire — 4 paires (1 principale + 3 secondaires)

Séries ordonnées par KRAS croissant, contrôle `step`, 12 flux immunitaires
(CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274, PDCD1, CTLA4, GZMB, IFNG,
CD19 — sauf ICGC : PRF1 et MS4A1 remplacent IFNG et CD19, voir
PROVENANCE_immune_v6.md).

| Paire | n | S_sep réel / nul | Écart | Stabilité R / N | (A) 0,07 | (B) 0 |
|---|---|---|---|---|---|---|
| IMMUNE_TCGA | 178 | 0,5263 / 0,1604 | **+0,3659** | 0,9914 / 0,9819 | passe | passe |
| IMMUNE_GEO62452 | 69 | 0,4656 / 0,3122 | **+0,1534** | 0,9692 / 0,9899 | passe | passe |
| IMMUNE_GEO71729 | 145 | 0,2900 / 0,1557 | **+0,1343** | 0,9916 / 0,9964 | passe | passe |
| IMMUNE_ICGC | 70 | 0,2289 / 0,4489 | **−0,2200** | 0,9955 / 0,9976 | échoue (inversé) | échoue (inversé) |

Contexte v6.2 : max_separation +0,3675 / +0,1650 / +0,1362 / −0,2200 —
**les mêmes verdicts que S_sep sous les deux règles, et les mêmes que
max_separation v6.1 sous 0,07** (l'annexe v6.1 comptait déjà ces trois
premières parmi ses 16/23). MC : +0,0545 / +0,0217 / +0,0204 / −0,0343
(tous sous 0,07) ; Delta : +1,9142 / −0,0417 / +0,1903 /
+0,1782 ; L7a signé : −0,526 / −0,282 (réel flat 0,280) / −0,562 /
+0,033. **Le bras immunitaire se lit 3/4 en S_sep, avec ICGC inversé de
−0,22 — le nul y sépare plus que le réel.** S_sep n'y change rien par
rapport à la v6.1 : ni la hiérarchie des cohortes, ni l'inversion ICGC,
ni le fait que TCGA porte l'essentiel de l'écart (+0,37 contre +0,13 à
+0,15 ailleurs).

### PARP — 2 paires (1 principale + 1 secondaire)

Séries ordonnées par expression KRAS croissante, contrôle `step`, mêmes
12 flux de réparation de l'ADN que le bras ATR
(PROVENANCE_parp_v6.md).

| Paire | n | S_sep réel / nul | Écart | Stabilité R / N | (A) 0,07 | (B) 0 |
|---|---|---|---|---|---|---|
| PARP_TCGA | 178 | 0,3667 / 0,1987 | **+0,1680** | 0,9963 / 0,9973 | passe | passe |
| GEO71729_PARP | 145 | 0,3356 / 0,2290 | **+0,1066** | 0,9923 / 0,9921 | passe | passe |

Contexte v6.2 : max_separation +0,1688 / +0,1074 ; MC +0,0244 / +0,0139 ;
Delta +0,2616 / −0,0139 ; L7a signé −0,220 / +0,006. **PARP est le bras
le plus régulier : 2/2 en S_sep sous les deux règles, 2/2 en max_sep
v6.1 sous 0,07.** Rien ne change — ni les écarts, ni leur ordre
(TCGA > GSE71729), ni le fait que MC et Delta restent faibles ou nuls
sur GSE71729.

### Paires principales (Phase 2) — rappel vérifié

| Paire | n | S_sep réel / nul (v6.2) | Écart | (A) 0,07 | (B) 0 | max_sep v6.1 (0,07) |
|---|---|---|---|---|---|---|
| HP35 | 1000 | 1,5391 / 0,1185 | +1,4206 | passe | passe | passait (+1,6512) |
| TCGA v4 | 178 | 0,4548 / 0,1688 | +0,2860 | passe | passe | passait (+0,2928) |
| GSE71729 | 145 | 0,2579 / 0,2174 | +0,0405 | échoue | passe | échouait (+0,0402) |
| GSE62452 | 69 | 0,3044 / 0,3116 | −0,0072 | échoue | échoue | échouait (−0,0036) |
| ICGC | 70 | 0,4034 / 0,3073 | +0,0960 | passe | passe | passait (+0,0970) |
| IMMUNE_TCGA | 178 | 0,5263 / 0,1604 | +0,3659 | passe | passe | passait (+0,3675) |
| PARP_TCGA | 178 | 0,3667 / 0,1987 | +0,1680 | passe | passe | passait (+0,1688) |
| DEPMAP | 45 | 0,4339 / 0,2524 | +0,1815 | passe | passe | passait (+0,1904) |

**Total (A) : 6/8 ; total (B) : 7/8.** La seule paire qui change de
verdict entre (A) et (B) est GSE71729 (+0,0405) ; GSE62452 reste négative
sous les deux règles. Sous chaque règle, S_sep et max_separation donnent
exactement les mêmes listes. Pour mémoire, MC v6.2 à gigue 0 donne aussi
7/8 (mêmes paires) contre 1/8 en v6.1 à 0,07 — même mécanisme, même
réserve : les écarts MC sont identiques à la v6.1, seul le seuil a bougé.

### Annexe (23 paires secondaires) — contrôle d'ensemble

S_sep (A) **16/23** : ATR_TCGA, GEO62452_V4B, GEO71729_PARP, GEO71729_V4B,
GEO71729_V4C, IMMUNE_GEO62452, IMMUNE_GEO71729, IMMUNE_TCGA, PARP_TCGA,
TCGA_V2, TCGA_V3, V4R_CLDN18, V4R_KRASDESC, V4R_KRASVAL, TESTA_PROLIF,
COAD — **exactement les 16 paires de max_separation v6.1**. Échecs (A) :
CPTAC_BCM, CPTAC_UMICH, GEO71729, IMMUNE_ICGC, LUAD, TCGA_V1, V4R_PURITY.
S_sep (B) **20/23** — exactement max_separation v6.2 à gigue 0 (20/23,
mêmes paires) ; échecs (B) : CPTAC_BCM, IMMUNE_ICGC, V4R_PURITY. Les
quatre paires qui ne passent qu'à gigue 0 sont CPTAC_UMICH (+0,0212),
GEO71729 (+0,0405), LUAD (+0,0152) et TCGA_V1 (+0,0049) — toutes sous
0,07, toutes déjà positives en max_separation v6.1.

## 8.38.3 Pourquoi S_sep ≈ max_separation ici (et ce que ça veut dire)

La stabilité est quasi saturée sur toutes les paires PDAC : 0,9692 à
0,9976 sur les bras de ce chantier (ATR 0,9968/0,9917 ; MTAP 0,9959/
0,9825 ; immunitaire 0,9692–0,9976 ; PARP 0,9921–0,9973), et 0,9782 à
0,9973 sur les paires principales. S_sep vaut donc max_separation ×
~0,99 : les écarts S_sep diffèrent des écarts max_separation de moins
de 0,01 partout sauf sur HP35 (réel 0,8687 contre nul 0,9827 : S_sep
+1,4206 contre max_sep +1,6512 — le seul cas où le garde-fou mord un
peu, sans changer le verdict). **Le garde-fou anti-pic-bruité ne s'est
déclenché sur aucune série PDAC de ce chantier.** Ce n'est pas une
preuve qu'il ne servirait jamais — c'est le constat qu'il n'a rien eu à
pénaliser ici : les pics sont localement plats partout, y compris sur
les nuls. S_sep atteint la barre ≥ 6/8 du protocole (§3.4), mais il
hérite exactement des forces et des faiblesses de max_separation :
mêmes paires qui passent, mêmes paires qui échouent (GSE71729 de peu,
GSE62452 plat, ICGC immunitaire inversé), même fragilité face au nul
sur MTAP quand on regarde MC et Delta.

## 8.38.4 Provenance

- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` ;
  v6.1 de référence SHA-256
  `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`.
  Mode `fast`, graine 42 (défaut), nul = lignes permutées, graine 42,
  contrôle intact.
- **Formule et règles.** PROTOCOL_v6.2.md §3 (S_sep, exclusions de
  s_norm / robustness / sharpness, plancher 0,07) et §3.4 (critère ≥ 6/8) ;
  règles de comptage de `extract_phase2.py` (direction = signe de la
  somme des écarts).
- **Entrées (SHA-256 vérifiés avant les runs MTAP ; les autres relus
  depuis les JSON des lots existants).** MTAP :
  `pdac_tcga_fluxes_v4_mtap.csv`
  `578b8d3b9b26099d0784ed23754d1cc9717be7f9292eb47e201d186cdbc90df6`,
  `pdac_tcga_fluxes_v4_mtap_nul.csv`
  `e6786a47ce107dbf9785d83981ab413f8afb4e75fbdbae4da56da8c1e46453b9`
  (PROVENANCE_mtap_series.md : Broad GDAC Firehose stddata 2016-01-28,
  PAAD, RSEM ; GISTIC2 Level 4 ; 177/178 appariées). ATR :
  `pdac_tcga_fluxes_atr.csv`
  `88e52311a2cc10371647ff0b9ebbe909b49afe58cf8f8a72e67b7ee31c5fe849`,
  nul `e70011545f230f77d64d4b084addcab83a8cc40508f97cc47e54b08f95f1b090`.
  Immunitaire TCGA `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e`
  / nul `9100d181e3391d558eec6bc97e82f93b16c118b807b4a5f0c0992f4bda51a405` ;
  GSE62452 `97c4689a6ecacd0a73a77804200a72a90994d60bea7e6b2c079195acbffd79a3`
  / nul `b0496cb923d49ef4913f90b895d856e3c02a1b1b4d78a2cc11a9f198c367d3a9` ;
  GSE71729 `8987ffcaeb9cac848bd220c2a1816f63ecbcd63e5cd68c4f698e7c3234952219`
  / nul `b96b1f744db30193098e588326db33c3bca448bb87615fd011d9302e7c605fc7` ;
  ICGC `10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc`
  / nul `3393ecd662e6decfa41416b535e509089cb43bd63345097fe3f25ad9b7860955`.
  PARP TCGA `c9549b68280b2f4ca3d9b62020efa21ab97249b10e176de87ec528a0258c4309`
  / nul `57245c728dacf264654f77a4b4d6d608bbe3fb8c300b287061063bd062ab1360` ;
  PARP GSE71729 `99abbd6e08d7d2e1bc9ef60cb3b158f5d7d55e70ebbfec98cacebea1d936722c`
  / nul `3a8b076456f20bf5a66b6ec7354a70ddc290e04bec0a29fc0c425e963e684ce3`.
  Sources : TCGA-PAAD ARN Broad GDAC Firehose 2016-01-28 (RSEM, tarball
  MD5 `b09569ce3f4721f514bc137bd109ac0a`) ; GEO GSE62452 et GSE71729 ;
  ICGC PACA-AU (UCSC Xena, Bailey et al. 2016). Voir PROVENANCE_atr_chek1.md,
  PROVENANCE_immune_v6.md, PROVENANCE_parp_v6.md, PROVENANCE_mtap_series.md.
- **Nature des lignes.** Les CSV sont des résidus d'expression génique
  (mesures instrumentales — séquençage ARN — transformées : correction
  de pureté, résidus) ordonnés par une variable de contrôle (KRAS, CN
  MTAP, ou index `step`) ; les nuls sont des lignes permutées, graine 42
  — des échantillons hypothétiques, pas des mesures. Aucun mot humain,
  aucun échantillon hypothétique dans les séries réelles.
- **Sorties et scripts.** Runs MTAP v6.2 :
  `results_fast_v62_mtap/master_results.json`,
  `results_fast_v62_mtap_nul/master_results.json` ; log
  `runs_v62_mtap.log` (2/2, exit 0, 19 nov. 2026 11h27–11h34 UTC) ;
  manifeste `manifest_v62_mtap.txt` ; surveillance `watch_v62_mtap.sh` ;
  unité systemd `v62-mtap-838` (arrêtée d'elle-même à 2/2). Les autres
  paires sont relues depuis les 66 dossiers `results_fast_v62_*` du lot
  phase 2 (§8.37) et les 156 dossiers `results_fast_v61_*`. Extraction
  de ce chantier : `extract_ssep_838.py` (SHA-256
  `d7b8bd663fb36340779ebb4d7ce307775d4e9896afee4a75236192cf026bb14a`),
  sortie brute `ssep_838_verify.json` (SHA-256
  `d10727a30afc91886495ba64d882bc692ad1348625ee4f6982560db96600dbbd`).
  Tables comparées : `v62_phase2_table.json` (0 écart),
  `v61_phase2_table.csv` (0 écart, champs comparables).

## 8.38.5 Ce qui manque, ce qui reste ouvert

- **S_sep ne devient pas un discriminateur recommandé au-delà de
  max_separation** : il ne sépare ni mieux ni autrement, sous aucune
  des deux règles de gigue. Le garde-fou stabilité ne s'est jamais
  déclenché sur ces séries ; il faudrait une série à pic bruité
  (stabilité basse côté réel, haute côté nul) pour tester s'il sert à
  quelque chose — aucune série de ce chantier ne présente ce cas.
- **MTAP : contradiction non résolue.** S_sep/max_sep disent réel > nul
  (+0,20) pendant que MC (−0,16) et Delta (−0,54) disent nul > réel.
  Aucun des quatre indicateurs ne suffit seul ; la piste reste fermée
  comme en §8.36, et S_sep ne fournit pas l'arbitrage.
- **Immunitaire ICGC inversé (−0,22).** Le nul y sépare plus que le
  réel en S_sep comme en max_sep, alors que Delta y est positif
  (+0,18). La cohorte ICGC (n=70, flux PRF1/MS4A1 au lieu de IFNG/CD19)
  reste le point faible du bras immunitaire ; pas d'explication
  mesurée à ce jour.
- **Périmètre.** Les rotations (§8.32 : 96 paires, contrôle = flux) et
  les bras parprot / immrot / depmaprot n'ont pas été réappliqués en
  S_sep — hors périmètre de ce chantier (bras nommés : ATR, MTAP,
  immunitaire, PARP, paires principales). À faire sur demande, avec le
  même extracteur ; attention au doublon contrôle=flux (§8.32), qui
  fausserait la lecture par flux mais pas S_sep (best_config).
- **Répétition.** MTAP v6.2 n'a qu'une répétition (comme la phase 2) ;
  la gigue 0 mesurée en validation porte sur 10 autres runs, pas sur
  MTAP. Mais S_sep, max_separation, MC et Delta sont déterministes
  hors L5 et identiques entre v6.1 et v6.2 : une 2e répétition MTAP
  n'apporterait rien sur S_sep (elle ne testerait que L5/L7a, déjà
  validés à gigue 0 sur 10 runs).
- **Falsification.** Indisponible sous n = 75 (GSE62452, ICGC, DepMap)
  — rappel des §8.31/§8.35, inchangé par S_sep.
- **L7a.** Bouge de ≤ 0,0304 entre v6.1 et v6.2 (TCGA_V2, annexe) ;
  aucun verdict L7a ne change sur les paires principales.
- **Aucun nouveau seuil proposé, aucun code modifié, aucun push GitHub
  dans ce chantier** (publication sur go séparé, comme au §8.37).

— Fin de la §8.38. —
