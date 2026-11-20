# §8.51 Pureté / infiltration : la corrélation immunitaire n'est pas un artefact de composition

Date : 19–20 novembre 2026. Go : Zackary, « Fait tes 3 propositions, je reviens
plus tard », 19 nov. 2026 ~08h16 (2e des 4 chantiers v6.2 ; question ouverte
du §8.48.8).
Protocole gelé avant tout calcul et avant tout run :
`PROTOCOL_purity_infiltration_851.md` (SHA-256 `568d93d2…ab5`).

## Verdict d'abord

**La corrélation intra-famille immunitaire n'est PAS expliquée par la pureté
tumorale : c'est une propriété propre aux tumeurs, pas un artefact de
composition.** Les quatre conditions gelées de H0 sont toutes remplies.
Après régression de chaque gène immunitaire sur les deux scores de pureté
du projet (acineux + îlots), la corrélation moyenne intra-famille ne bouge
presque pas : **0,5563 → 0,5480, chute de 1,5 %** (fraction de paires
|r| > 0,5 inchangée, 41/66). Ordonner les flux immunitaires par le score
acineux ne les sépare pas du tout (**écart S_sep +0,0118**, nul 0,2748 contre
réel 0,2866) ; ordonner par le score îlots les sépare faiblement
(**+0,2876**, sous le seuil gelé de 0,30 et sous le minimum IMMROT de
+0,4508). Et le test décisif : ordonner les flux immunitaires
RÉSIDUALISÉS par CD8A résidualisé sépare presque autant que le brut —
**écart +0,9174 contre +0,9838 pour CD8A brut (93,3 % conservés)**,
prédit +0,9185 par la régression §8.48 à 0,0011 près. **La pureté
explique au plus une petite part (îlots), et ne porte pas la corrélation.**

**Le petit effet îlots est réel et il est nommé, pas caché.** Le score îlots
ordonne les flux immunitaires mieux que prédit (+0,2876 observé contre
+0,1625 prédit, 1,77×) et CD4 est le gène le plus lié à la pureté
(r = +0,357 avec les îlots, R² = 13,2 %). Mais cet effet est 2,6 fois plus
petit que la moyenne IMMROT (+0,7521) et la régression sur les îlots seuls
ne fait chuter la corrélation intra-famille que de 2,0 %. Il y a donc un
léger couplage composition–immunité dans ces tumeurs — pas une explication
de la corrélation.

## 8.51.1 Question, méthode, inventaire des données (avant le gel)

**Question (§8.48.8).** Le §8.48 a expliqué la domination IMMROT par le
couplage contrôle↔flux (r = 0,954, R² = 0,909, n = 48 ; IMMROT |r| moyen
0,556 contre 0,25 / 0,27 / 0,17 ailleurs). Reste ouverte la cause de la
corrélation intra-famille elle-même : pureté tumorale et infiltration
immunitaire (composition cellulaire), ou biologie propre aux tumeurs ?

**Ce qui existe réellement.** (a) Tarball TCGA-PAAD RSEM, Broad GDAC Firehose
2016-01-28, MD5 `b09569ce…ac0a` (détenu). (b) Base immunitaire TCGA
`pdac_immune_tcga_fluxes.csv`, n = 178, 12 gènes BRUTS log2(RSEM+1), AUCUNE
correction de pureté (choix documenté de PROVENANCE_immune_v6.md) :
CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274, PDCD1, CTLA4, GZMB, IFNG, CD19,
lignes ordonnées par KRAS brut croissant ; fichier d'axe joint
`immune_kras_order_tcga.csv` (step, barcode, KRAS brut) — clé de jointure
par barcode. (c) Proxys de pureté du projet (définitions v3/v4,
PROVENANCE_tcga_v3.md) : score acineux = médiane log2(RSEM+1) des 11 gènes
PNLIP, CTRB2, CELA3A, CTRB1, CPA1, CELA2A, CPB1, CELA3B, CLPS, CTRC, CPA2 ;
score îlots = médiane log2(RSEM+1) de INS, GCG, PPY, SST. Non sauvegardés
comme fichier autonome : RECALCULÉS ici depuis le tarball (mêmes listes que
`build_fluxes_tcga_v3.py`), joints aux lignes immunitaires PAR BARCODE —
jamais par index (les ordres v4 et immunitaire diffèrent : résidu KRAS
contre KRAS brut).

**Ce qui n'existe pas (manquant, nommé).** AUCUNE estimation de pureté
externe : ni ABSOLUTE, ni ESTIMATE, ni CPE, ni cellularité histologique.
AUCUN score d'infiltration par déconvolution : ni CIBERSORT / CIBERSORTx,
ni xCell, ni TIMER, ni MCP-counter (recherche dans tout
`~/workspace/runs/pdac-v6/` : 0 occurrence). Sources qui permettraient de
les obtenir (NON téléchargées ici) : pureté consensus TCGA d'Aran et al.,
Nat Commun 2015 (ABSOLUTE, ESTIMATE, LUMP, IHC ; tableau supplémentaire,
via UCSC Xena / GDC) ; ESTIMATE (Yoshihara et al., Nat Commun 2013) ;
CIBERSORTx (Newman et al., Nat Biotechnol 2019 ; accès web, compte requis) ;
TIMER2.0 (Li et al.).

**Ce que « pureté » veut dire ici — et la limite sur « infiltration ».**
Le score acineux mesure la contamination par du pancréas normal acineux
(score haut = plus de tissu normal = pureté tumorale BASSE) ; le score
îlots, la contamination endocrine. Ce sont des proxys d'expression, pas
une pureté absolue, et ils partagent la mesure ARN avec les flux. Surtout :
« infiltration » n'est mesurée ici qu'indirectement — les 12 gènes
immunitaires EUX-MÊMES sont les marqueurs d'infiltration (CD8A/CD8B = T
cytotoxiques, CD68/CD163 = macrophages, CD19 = B). Il n'existe pas de
score d'infiltration indépendant des flux testés : tester « l'infiltration
explique la corrélation » avec les seuls gènes immunitaires serait
circulaire. **Ce chantier teste la PURETÉ (scores acineux/îlots,
indépendants des 12 gènes) ; l'infiltration indépendante reste non testée**
(§8.51.10).

**Hypothèses gelées.** H1 (pureté explique) : (a) chaque flux corrèle
substantiellement avec les scores ; (b) la corrélation intra-famille
s'effondre après régression ; (c) ordonner par la pureté sépare les flux ;
(d) ordonner les flux résidualisés ne sépare plus. H0 (propriété propre) :
la corrélation persiste par toutes les voies.

**Critères gelés.** T1 : lien substantiel si moyenne |r| ≥ 0,30 pour au
moins un score ; faible si < 0,15 pour les deux. T2 : EFFONDREMENT si
moyenne |r| résiduelle < 0,30 (chute ≥ 45 %) ET fraction |r| > 0,5 < 0,20 ;
PERSISTANCE si chute < 20 % (moyenne résiduelle > 0,44). T5 : P-AC ou P-IS
soutient H1 si écart S_sep ≥ 0,45 (minimum IMMROT sans doublon) ; P-RES
soutient H1 si écart < 0,30, soutient H0 si écart ≥ 0,45. Verdict de
synthèse : H1 totale si T2 = effondrement ET P-RES < 0,30 ET (P-AC ≥ 0,45
OU P-IS ≥ 0,45) ; H1 partielle si T2 = partielle OU (P-AC/P-IS entre 0,30
et 0,45) avec P-RES < 0,70 ; H0 si T2 = persistance ET P-AC < 0,30 ET
P-IS < 0,30 ET P-RES ≥ 0,45 ; toute autre combinaison : zone grise.
Références : IMMROT sans doublon, moyenne +0,7521, minimum +0,4508 (CD68),
CD8A écart +0,9838 (réel 1,2310, nul 0,2472) ; régression §8.48
d_ssep = −0,175 + 1,705·C.

## 8.51.2 Porte J (jointure) : OUVERTE

Rechargement du tarball (MD5 conforme) : 178 tumeurs primaires (code 01) ;
0 NaN sur KRAS + 12 gènes immunitaires + 11 acineux + 4 îlots ; ordre KRAS
brut recalculé = `immune_kras_order_tcga.csv` (178/178 barcodes, valeurs
KRAS égales à 10⁻⁹ près) ; score acineux recalculé = colonne
`score_acineux` de `pdac_tcga_fluxes_v4r_purity.csv` triée, à 10⁻⁹ près ;
valeurs immunitaires reproduites depuis le tarball à 10⁻⁹ près. **Porte J
OUVERTE, les trois conditions tiennent.**

Scores (n = 178, ordre KRAS brut) : acineux min 0,00, médiane 8,54,
max 20,93 (7,9 % de zéros, 14/178) ; îlots min 0,00, médiane 11,53,
max 16,01 (0,6 % de zéros, 1/178). Corrélation acineux–îlots
**r = +0,4826 (p = 9,0×10⁻¹²)** — elle reproduit exactement la valeur v3
(0,4826, PROVENANCE_tcga_v3.md), sanité de la reconstruction.

## 8.51.3 T1 — Chaque flux immunitaire suit-il la pureté ? Faiblement

Pearson r (+ Spearman ρ) de chaque flux contre les deux scores ; R² par
flux (OLS sur [acineux, îlots]) ; p brutes bilatérales, sans correction
pour tests multiples (24 tests, ~1,2 faux positifs attendus à p < 0,05
sous le nul — le jugement porte sur la moyenne, pas sur une p isolée).

| Gène | r acineux (p) | ρ acineux | r îlots (p) | ρ îlots | R² pureté |
|---|---|---|---|---|---|
| CD8A | +0,271 (2,6×10⁻⁴) | +0,271 | +0,277 (1,8×10⁻⁴) | +0,307 | 0,101 |
| CD8B | +0,212 (4,5×10⁻³) | +0,198 | +0,208 (5,3×10⁻³) | +0,264 | 0,060 |
| CD4 | +0,234 (1,7×10⁻³) | +0,206 | **+0,357 (1,0×10⁻⁶)** | +0,371 | **0,132** |
| FOXP3 | +0,057 (0,45) | +0,088 | +0,157 (0,036) | +0,158 | 0,025 |
| CD68 | +0,159 (0,034) | +0,122 | +0,228 (2,2×10⁻³) | +0,131 | 0,055 |
| CD163 | +0,258 (5,0×10⁻⁴) | +0,243 | +0,227 (2,3×10⁻³) | +0,269 | 0,081 |
| CD274 | +0,085 (0,26) | +0,109 | +0,168 (0,025) | +0,153 | 0,028 |
| PDCD1 | +0,158 (0,035) | +0,182 | +0,243 (1,1×10⁻³) | +0,296 | 0,061 |
| CTLA4 | +0,101 (0,18) | +0,101 | +0,242 (1,1×10⁻³) | +0,257 | 0,059 |
| GZMB | +0,091 (0,23) | +0,111 | −0,007 (0,93) | +0,030 | 0,012 |
| IFNG | +0,109 (0,15) | +0,145 | +0,110 (0,14) | +0,165 | 0,016 |
| CD19 | −0,021 (0,78) | +0,023 | +0,151 (0,044) | +0,235 | 0,034 |

Moyenne |r| : **acineux 0,146**, **îlots 0,198** (Spearman 0,150 et 0,220).
**R² médian 0,057 (5,7 %), maximum 0,132 (CD4).** Critère gelé : ni
substantiel (≥ 0,30) ni uniformément faible (< 0,15 pour les deux — les
îlots sont à 0,198) : lien FAIBLE À MODÉRÉ, porté par les îlots plus que
par l'acineux. Significatifs à p < 0,05 (brut) : 6/12 contre l'acineux,
10/12 contre les îlots — mais tous les |r| restent ≤ 0,36. Deux remarques :
(a) 22 des 24 corrélations sont POSITIVES — les gènes immunitaires montent
légèrement avec les scores de tissu normal (seules CD19–acineux, −0,021,
et GZMB–îlots, −0,007, sont ~nulles) ; le sens est celui d'une co-variation
avec le tissu non tumoral, pas d'une dilution par la tumeur — magnitude
trop faible pour porter une explication ; (b) la pureté explique au plus
13 % de la variance d'UN gène (CD4) et 5,7 % en médiane — à comparer aux
2,0 % médians de la v3 sur tous les gènes (les gènes immunitaires sont un
peu plus liés à la composition que le gène médian, sans changer d'ordre
de grandeur).

## 8.51.4 T2 — La corrélation intra-famille survit à la régression pureté

Matrice 66 paires, brute contre résidus OLS (même définition que v3/v4 :
[1, score_acineux, score_îlots]).

| Matrice | Pearson moyenne \|r\| | médiane \|r\| | fraction \|r\| > 0,5 | Spearman moyenne \|r\| |
|---|---|---|---|---|
| Brute | **0,5563** | 0,5677 | 0,621 (41/66) | 0,5403 |
| Résidus [ac, is] | **0,5480** | 0,5676 | 0,621 (41/66) | 0,5243 |
| Résidus acineux seul | 0,5528 | 0,5628 | 0,636 (42/66) | 0,5337 |
| Résidus îlots seul | 0,5452 | 0,5608 | 0,606 (40/66) | 0,5236 |

**Chute : 1,5 % avec les deux scores, 0,6 % acineux seul, 2,0 % îlots
seul.** Critère gelé : PERSISTANCE (chute < 20 %, moyenne résiduelle
0,5480 > 0,44 — très loin du seuil d'effondrement 0,30). La fraction de
paires fortes ne bouge pas (41/66 avant comme après). Retirer
linéairement toute la pureté mesurable ne retire rien de la corrélation
immunitaire : la corrélation n'est pas portée par ces deux scores.

## 8.51.5 T3 — Couplage prédit : la régression §8.48 tient, avant comme après

Couplage C par contrôle immunitaire (moyenne des |r| avec les 11 autres
flux), brut contre résidualisé ; d_ssep prédit par d = −0,175 + 1,705·C.

| | C moyen | d_ssep prédit moyen |
|---|---|---|
| Brut | 0,5563 | **0,7735** (observé IMMROT : 0,7521) |
| Résidualisé [ac, is] | 0,5480 | **0,7593** |

Sanité : la prédiction brute retrouve la moyenne IMMROT observée à 0,02
près (0,7735 contre 0,7521) — la régression §8.48 se réplique sur ces
données. Après résidualisation, la prédiction ne baisse que de 0,014.
CD8A seul : C 0,6514 → 0,6414, d_pred 0,9356 → **0,9185**. Le T3 ne fait
que traduire T2 en S_sep prédit ; le verdict se joue au T5.

## 8.51.6 T4 — Stratification : la cohésion persiste dans chaque moitié

Médiane du score, n = 89/89 ; matrice intra-famille dans chaque moitié
(estimations plus bruitées à n = 89, le dire — mais les deux moitiés
restent à ≥ 0,50, près du 0,5563 global).

| Stratification | Moitié haute : moyenne \|r\| (frac. > 0,5) | Moitié basse : moyenne \|r\| (frac. > 0,5) |
|---|---|---|
| Score acineux (méd. 8,54) | 0,4987 (0,530) | **0,5813** (0,621) |
| Score îlots (méd. 11,53) | 0,5327 (0,636) | 0,5649 (0,621) |

Si la cohésion venait de la pureté, elle devrait s'effondrer dans chaque
moitié (bande de pureté étroite). Elle persiste dans les quatre moitiés,
et elle est même PLUS forte dans la moitié BASSE en acineux (0,5813 contre
0,4987) — le sens opposé à celui qu'un artefact de composition produirait.
Argument non paramétrique, indépendant de toute linéarité : il confirme T2
par une autre voie.

## 8.51.7 T5 — Runs v6.2 : la pureté n'ordonne pas l'immunitaire, les résidus si

Prédictions calculées AVANT de lire les sorties (depuis T1/T2 du jour) :
P-AC d_pred +0,0745 (C = 0,1463) ; P-IS d_pred +0,1625 (C = 0,1980) ;
P-RES d_pred +0,9185 (C_résid CD8A = 0,6414). 6 runs v6.2, mode fast,
graine 42, 6/6 exit 0 (lot 23h32 UTC 19 nov. – 00h38 UTC 20 nov. ;
§8.51.9 pour l'incident de redémarrage machine).

| Run | Contrôle → analysés | S_sep réel | S_sep nul | Écart | Prédit | MC réel / nul | Delta réel / nul | w |
|---|---|---|---|---|---|---|---|---|
| P-AC | score acineux → 12 imm. bruts | 0,2866 | 0,2748 | **+0,0118** | +0,0745 | 0,3440 / 0,3425 | 4,10 / 3,84 | 30 |
| P-IS | score îlots → 12 imm. bruts | 0,4532 | 0,1656 | **+0,2876** | +0,1625 | 0,3713 / 0,3256 | 4,22 / 4,08 | 30 |
| P-RES | CD8A résid. → 11 imm. résid. | 1,1240 | 0,2066 | **+0,9174** | +0,9185 | 0,4551 / 0,3311 | 4,28 / 3,18 | 30 |

Lecture par critère gelé :
- **P-AC : rien.** Écart +0,0118, MC +0,0015 (0,3440 contre 0,3425) :
  ordonner par le score acineux ne sépare pas les flux immunitaires —
  le réel et le nul sont indiscernables. Sous le seuil H1 (0,45) et sous
  le seuil H0 (0,30) : soutient H0.
- **P-IS : un petit effet réel, sous les seuils.** Écart +0,2876 — au-dessus
  de sa prédiction (+0,1625, 1,77×) mais sous le seuil gelé de 0,30 (de
  0,0124) et sous le minimum IMMROT (+0,4508) ; 38 % de la moyenne IMMROT
  (+0,7521). MC +0,0457 (0,3713 contre 0,3256). Le S_sep réel absolu
  (0,4532) est au niveau du minimum IMMROT, mais c'est l'ÉCART qui compte
  et le nul est bas (0,1656). Le seuil est trouvé très tard (84,78 %) :
  la séparation, quand elle existe, est en fin de course, pas une marche
  nette. Ne soutient pas H1 (critère ≥ 0,45 non atteint) ; entre dans la
  condition H0 (< 0,30), de justesse — à dire comme tel.
- **P-RES : la séparation survit presque intacte.** Écart +0,9174 contre
  +0,9838 pour CD8A brut (**93,3 % conservés, baisse de 6,8 %**) et contre
  +0,9185 prédit (**écart à la prédiction −0,0011** — la régression §8.48
  prédit le résiduel aussi exactement que le brut). MC +0,1240 (0,4551
  contre 0,3311) : ici MC sépare, contrairement aux rotations §8.44 —
  noté, non utilisé pour le verdict (le verdict porte sur S_sep, gelé).
  L7a ne sépare pas (up 0,1705 contre up 0,2015) : L7a n'est pas utilisé
  ici, comme au §8.48. Critère gelé : P-RES ≥ 0,45 → soutient H0,
  fortement.

## 8.51.8 Verdict de synthèse

Règle gelée, test par test : T2 = PERSISTANCE (chute 1,5 %) ; P-AC = +0,0118
(< 0,30) ; P-IS = +0,2876 (< 0,30, de justesse) ; P-RES = +0,9174 (≥ 0,45).
**Les quatre conditions de H0 sont remplies : H0 est SOUTENUE. La
corrélation intra-famille immunitaire est une propriété propre aux
tumeurs — co-expression immunitaire réelle dans les tumeurs TCGA-PAAD —
et non un artefact de la pureté tumorale telle que le projet la mesure
(scores acineux/îlots).** H1 totale et H1 partielle sont toutes deux
rejetées par la règle gelée : aucune condition de H1 n'est remplie
(T2 n'est ni effondrement ni partielle ; P-AC/P-IS ne sont ni ≥ 0,45 ni
entre 0,30 et 0,45 ; P-RES n'est pas < 0,70).

**Ce que cela ne dit pas.** (a) Cela ne dit pas que la pureté ne joue
AUCUN rôle : l'effet îlots (+0,2876, CD4 r = +0,357) est réel, petit, et
il reste à expliquer — il ne porte simplement pas la corrélation.
(b) Cela ne dit pas que l'infiltration est innocentée : aucune
infiltration INDÉPENDANTE n'a été testée ici (cf. §8.51.1) — les gènes
immunitaires sont eux-mêmes les marqueurs d'infiltration, et un score de
déconvolution (CIBERSORT/xCell) pourrait encore séparer ce qui, dans la
co-expression, vient de la quantité de cellules immunitaires infiltrantes
de ce qui vient de leur état. (c) Cela ne dit pas que la corrélation est
« biologique » au sens d'une régulation : elle peut venir d'une variable
latente non testée (sous-type moléculaire — autre piste du §8.48.8 —,
micro-environnement stromal, état d'activation). (d) La mesure de pureté
elle-même est un proxy ARN : une pureté ABSOLUTE/ESTIMATE externe pourrait
donner un autre chiffre — le contrôle indépendant reste ouvert (§8.51.10).
(e) La domination IMMROT du §8.48 n'est pas remise en cause : elle reste
expliquée par le couplage ; ce chantier en explique la CAUSE AMONT —
le couplage n'est pas un artefact de composition.

## 8.51.9 Provenance

- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant les calculs, dans les deux logs de lot, et après
  l'extraction). Mode `fast`, graine 42 (défaut), nul = lignes permutées,
  graine 42 (default_rng frais par fichier), contrôle intact.
- **Protocole.** `PROTOCOL_purity_infiltration_851.md`, SHA-256
  `568d93d2459db1b78219a91fb1620486ecb4a2f5f61ac478629f7508f0867ab5`,
  gelé le 19 nov. 2026 avant tout calcul et avant tout run de ce chantier.
- **Entrées.** Tarball TCGA-PAAD RSEM, MD5 `b09569ce3f4721f514bc137bd109ac0a`
  (vérifié) ; base immunitaire `pdac_immune_tcga_fluxes.csv`, SHA-256
  `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e` ;
  axe `immune_kras_order_tcga.csv`, SHA-256
  `31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d` ;
  écarts §8.48 relus en machine dans `ssep_844_rotations.csv` (CD8A :
  réel 1,2310, nul 0,2472, écart +0,9838). Sources : TCGA Firehose PAAD
  2016-01-28 ; définitions des scores : PROVENANCE_tcga_v3.md ;
  base immunitaire : PROVENANCE_immune_v6.md.
- **Nature des lignes.** Les flux immunitaires sont des mesures
  instrumentales (séquençage ARN, log2(RSEM+1), brutes) ; les scores de
  pureté sont des médianes de ces mêmes mesures sur des gènes de tissu
  normal ; les résidus sont des valeurs calculées (OLS sur [1, ac, is]) ;
  les nuls sont des lignes permutées (graine 42) — des échantillons
  hypothétiques, pas des mesures. Aucun mot humain, aucun échantillon
  hypothétique dans les séries réelles.
- **Sorties et scripts de ce chantier.**
  `analyze_purity_851.py` (SHA `c102a11c…bf03`) : porte J, T1–T4.
  `build_purity_851.py` (SHA `2d5c99e0…a3c`) : scores + 6 CSV T5
  (résidus vérifiés : moyenne |r| = 0,5480, identique à T2).
  `extract_purity_851.py` (SHA `9b6d61bb…330b`) : lecture des 6 runs.
  `purity_851_scores.csv` (SHA `fe3ff0e9…3d7`, 178 tumeurs : barcode,
  KRAS brut, score acineux, score îlots),
  `purity_851_results.json` (SHA `df715e03…b0c`, T1–T4),
  `purity_851_results.csv` (SHA `1955d2aa…cda`, T1 par flux),
  `purity_851_immune_resid.csv` (SHA `fc0a1ad1…415`, 12 flux résidualisés),
  `purity_851_csv_sha.json` (SHA `d8630e38…4a`, SHA des 6 CSV T5),
  `purity_851_runs.json` (SHA `5b15d7e2…51b`) / `.csv` (SHA `b125ad74…cda`,
  6 runs). Manifeste `manifest_v62_purity_851.txt`
  (SHA `32300e5d…fec`) ; log `runs_v62_purity_851.log` ; surveillance
  `watch_v62_purity_851.sh` (SHA `ac41ab79…34f`) ; unités systemd
  `v62-purity-851` puis `v62-purity-851b`.
- **Ce qui manque :** pureté externe (ABSOLUTE/ESTIMATE/CPE) et scores
  d'infiltration indépendants (CIBERSORT/xCell/TIMER) — non détenus,
  non téléchargés (cf. §8.51.1) ; les moitiés T4 sont à n = 89
  (estimations plus bruitées) ; les p de T1 sont brutes, sans correction
  pour tests multiples.

## 8.51.10 Ce qui manque, ce qui reste ouvert

- **Infiltration indépendante non testée.** Le test décisif manquant est
  une déconvolution (CIBERSORTx, xCell) ou un score ESTIMATE immunitaire
  par tumeur, joint par barcode, puis : (a) corrélation flux↔score
  d'infiltration, (b) résidus après régression sur ce score, (c) run
  contrôle = score d'infiltration → flux immunitaires. Sources nommées
  au §8.51.1. C'est le chantier jumeau de celui-ci, non lancé.
- **Pureté externe.** Les estimations ABSOLUTE / ESTIMATE / CPE d'Aran
  et al. 2015 (TCGA, tableau supplémentaire) donneraient un contrôle
  indépendant des proxys ARN du projet. Si elles confirmaient T2/T5, H0
  serait renforcée ; si elles effondraient la corrélation, H1 serait
  rouverte — avec la question de savoir pourquoi les proxys du projet ne
  la voient pas.
- **Le petit effet îlots.** +0,2876 au T5, CD4 le plus lié (R² 13,2 %),
  seuil tardif (84,78 %) : est-ce une vraie queue de distribution
  (tumeurs très riches en îlots = plus de signal immunitaire) ou un
  artefact de seuil ? Un découpage par terciles d'îlots et une lecture
  par flux (quel gène porte l'écart P-IS) le trancheraient — non fait ici.
- **Sous-type moléculaire.** Autre variable latente du §8.48.8, toujours
  non testée : la corrélation immunitaire pourrait suivre le sous-type
  (Bailey et al. 2016 : squameux, immunogénique, etc.) plutôt que la
  pureté. Les sous-types ICGC existent dans `data/` (fichier NMF) ; la
  jointure TCGA reste à établir.
- **Incident d'exécution.** La machine a redémarré pendant le lot
  (~23h44 UTC, `uptime` : 0 min à 23h44) ; la première unité
  `v62-purity-851` est morte avec elle (aucune entrée dans `journalctl`,
  cause non établie — comme aux §8.41/§8.44/§8.48 ; unité `--collect`,
  donc introuvable après sa mort). Aucune sortie n'était perdue (1/6
  terminé, EXIT 0) ; la relance reprenable `v62-purity-851b` a repris au
  2e run à 23h44:23 UTC. Bilan final : **6/6 exit 0, 0 échec**, lot
  23h32:19 UTC 19 nov. – 00h38:48 UTC 20 nov.
  (`=== FIN 2026-11-20T00:38:48Z deja_faits=1 termines=5 echecs=0` ;
  surveillance arrêtée d'elle-même à 6/6, tour 1/12).
- **Périmètre.** 6 nouveaux runs v6.2 au maximum (protocole §6), aucun
  autre. Aucun nouveau seuil proposé, aucun code modifié, aucun push
  GitHub dans ce chantier (publication sur go séparé ; règle permanente
  « Toujours github et pdf !!! » — par le coordinateur).

— Fin de la §8.51. —
