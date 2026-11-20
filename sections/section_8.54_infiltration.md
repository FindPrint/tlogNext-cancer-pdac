# §8.54 Infiltration par déconvolution indépendante : la corrélation immunitaire EST expliquée par l'infiltration

Date : 20 novembre 2026. Go : 5 pistes PDAC approuvées le 19 nov. 2026 au
soir (dont celle-ci : « infiltration par déconvolution indépendante ») ;
tâche confiée 19 nov. 22h15. Chantier jumeau du §8.51 ; question ouverte
du §8.51.10.
Protocole gelé avant tout calcul et avant tout run :
`PROTOCOL_infiltration_854.md` (SHA-256 `f0f12473…bdc7` — version amendée,
cf. §8.54.9).

## Verdict d'abord

**La corrélation intra-famille immunitaire EST expliquée par
l'infiltration immunitaire — en totalité selon la règle gelée.** Les trois
conditions de H1 totale sont remplies, test par test. Après régression de
chaque gène immunitaire sur l'ImmuneScore ESTIMATE (calculé depuis la
matrice détenue, 141 gènes, indépendant des flux à 140/141 près), la
corrélation moyenne intra-famille s'effondre : **0,5563 → 0,2002, chute
de 64,0 %** (fraction de paires |r| > 0,5 : 41/66 → 3/66). Ordonner les
flux immunitaires par l'ImmuneScore les sépare massivement (**écart S_sep
+1,1942**, réel 1,4063 contre nul 0,2121 — au-dessus du +1,0466 prédit et
au-dessus du +0,9838 de CD8A brut) ; ordonner par le StromalScore les
sépare aussi (**+0,9407**). Et le test décisif : ordonner les flux
immunitaires RÉSIDUALISÉS par CD8A résidualisé ne sépare presque plus —
**écart +0,1982 contre +0,9838 pour CD8A brut (20,2 % conservés)**,
sous le seuil gelé de 0,30. **Le contraste avec le §8.51 est total : la
pureté laissait 93,3 % de la séparation ; l'infiltration n'en laisse que
20,2 %. La corrélation immunitaire est un effet de composition — la
quantité de cellules immunitaires infiltrantes — pas une propriété
propre aux tumeurs.**

**Les trois nuances sont nommées, pas cachées.** (a) Le résidu n'est pas
zéro : +0,1982, et 3 paires restent fortes après régression, en tête
CD8A–CD8B (0,6409) — deux chaînes du même récepteur, un reste structuré,
pas du bruit (§8.54.8). (b) La stratification T4 ne s'effondre pas
(moitiés 0,3638 / 0,3926) — mais ses moitiés restent larges (écart-type
554 / 475 contre 815 global), la prémisse de bande étroite n'est pas
remplie : T4 est non concluant ici, pas une réfutation (§8.54.6). (c) Le
bras stromal n'est pas une preuve indépendante : r(Immune, Stromal) =
0,7831, les deux scores co-varient — I-STR est une seconde vue du même
axe de composition (§8.54.7).

## 8.54.1 Question, méthode, inventaire des données (avant le gel)

**Question (§8.51.10).** Le §8.51 a établi que la corrélation
intra-famille immunitaire (0,5563) n'est PAS expliquée par la pureté
tumorale telle que le projet la mesure (0,5480 après régression, chute
1,5 % ; P-RES +0,9174, 93,3 % conservés). Reste ouverte la seconde
branche du §8.48.8 : l'infiltration immunitaire INDÉPENDANTE — un score
de déconvolution ou un score ESTIMATE immunitaire par tumeur —
explique-t-elle la corrélation ? Ce chantier teste cette branche. Il ne
re-teste pas la pureté (§8.51) et n'importe aucune conclusion d'une autre
expérience : seuls les chiffres de ce chantier (T1–T5 du jour) et les
écarts relus des §8.44/§8.48/§8.51 font le verdict.

**Ce qui existe réellement.** (a) Tarball TCGA-PAAD RSEM, Broad GDAC
Firehose 2016-01-28, MD5 `b09569ce…ac0a` (détenu) — la même matrice que
§8.51. (b) Base immunitaire TCGA `pdac_immune_tcga_fluxes.csv`, n = 178,
12 gènes BRUTS log2(RSEM+1) : CD8A, CD8B, CD4, FOXP3, CD68, CD163,
CD274, PDCD1, CTLA4, GZMB, IFNG, CD19, lignes ordonnées par KRAS brut
croissant ; fichier d'axe joint `immune_kras_order_tcga.csv` (step,
barcode, KRAS brut) — clé de jointure PAR BARCODE, jamais par index.
(c) AUCUN score d'infiltration détenu : recherche dans tout
`~/workspace/runs/pdac-v6/` — 0 occurrence de CIBERSORT, xCell, TIMER,
ESTIMATE, déconvolution (hors le mot « estimateurs » du pipeline, sans
rapport).

**Sources externes publiées : tentées, inaccessibles en accès direct.**
Toutes gratuites en principe, toutes bloquées par un obstacle d'accès
concret (accès direct curl, sans navigateur vivant) — AUCUNE contournée,
AUCUNE donnée inventée pour les remplacer :
- **Yoshihara et al. 2013, Suppl. Data 2** — scores stromal/immunitaire/
  ESTIMATE publiés par tumeur TCGA (RNAseqV2), la source externe idéale —
  et **Suppl. Data 1** (les 141+141 gènes) : fichiers
  `ncomms3612-s3.xlsx` (551,5 Ko) et `ncomms3612-s2.xlsx` (168,6 Ko),
  PMC3826632, doi 10.1038/ncomms3612. Téléchargement PMC direct renvoie
  une page interstitielle « Preparing to download... » avec défi
  proof-of-work JS (cookie `cloudpmc-viewer-pow`) — non franchi. Miroir
  Nature static-content : 403 AccessDenied. Europe PMC
  `supplementaryFiles` : 502 Bad Gateway. Statut : ACCESSIBLE PAR
  NAVIGATEUR VIVANT (tâche pour le coordinateur, hors de ce chantier —
  sous-agent sans navigateur). La comparaison de mes scores calculés aux
  scores publiés devient un chantier ultérieur (§8.54b), pas un ajout
  rétroactif.
- **Aran et al. 2015, Suppl. Data 1** — pureté ESTIMATE/ABSOLUTE/LUMP/
  IHC/CPE par tumeur, `ncomms9971-s2.xlsx` (540,1 Ko), PMC4671203,
  doi 10.1038/ncomms9971 : même interstitiel proof-of-work PMC, même
  statut (navigateur vivant).
- **Thorsson et al. 2018 / CRI iAtlas** — fractions CIBERSORT 22 types,
  fraction leucocytaire, PMC5982584, doi 10.1016/j.immuni.2018.03.023 :
  tableaux supplémentaires derrière le même interstitiel PMC ; API
  GraphQL iAtlas exige le package R `iatlasGraphQLClient` (pas de R sur
  cette machine) ; magasin Synapse exige un compte. Inaccessible ici.
- **TIMER / TIMER2.0** (Li et al., doi 10.1093/nar/gkaa407) : serveur web,
  pas de fichier de scores en vrac ; lien historique
  `http://cistrome.org/TIMER/misc/AGPall.zip` → 404 Not Found. Mort.
- **CIBERSORTx** (Newman et al. 2019) : accès web, compte requis — non
  tenté au-delà du constat (compte = hors périmètre).
- **UCSC Xena** : aucune route d'accès directe vérifiée sans navigateur
  dans ce chantier. Nommée comme ouverte.
Les fichiers HTML d'échec ont été supprimés ; rien de ces tentatives
n'entre dans les calculs.

**Voie retenue : ESTIMATE calculé depuis les données détenues (Voie C).**
Faute de scores publiés accessibles, le score d'infiltration est CALCULÉ
dans ce chantier, par une méthode publiée, depuis la matrice détenue :
ESTIMATE (Yoshihara et al., Nat Commun 2013) — ssGSEA (Barbie et al.,
Nature 2009, doi 10.1038/nature08460) sur deux signatures publiées de
141 gènes chacune (stromale, immunitaire). Implémentation : PORT PYTHON
FIDÈLE de `tidyestimate::estimate_score` (Aragaki, CRAN 1.1.1, 2023),
code source lu en clair (`R/estimate_score.R`, GitHub
KaiAragaki/tidyestimate) : rangs par échantillon (ex æquo moyennés),
rangs remis à l'échelle 10000/n, ssGSEA exposant 0,25, ES = somme des
écarts cumulés. Filtre aux gènes communs aux six plateformes (10 391
symboles HGNC uniques) AVEC appariement d'alias conservateur
(`find_alias`, 1-à-1) tel qu'utilisé dans la vignette.
`is_affymetrix = FALSE` : pas de conversion en pureté (formule cosinus
réservée aux puces Affymetrix par Yoshihara) — les scores sont relatifs,
comme le prescrit la méthode pour le RNA-seq. Signatures extraites du
tarball CRAN `tidyestimate` 1.1.1 (SHA-256 `cc747f78…514b`), fichiers
`data/gene_sets.rda` (SHA `5d058439…69a`) et `data/common_genes.rda`
(SHA `f09453b2…2ff3`), lus en Python avec le parseur `rdata` (venv
dédié `/tmp/venv854`, pas de R sur cette machine). Les mises à jour
d'alias de tidyestimate sont conservées (ex. FYB→FYB1, WISP1→CCN4) et
listées dans les sorties JSON.

**Circularité vérifiée à l'inventaire, avant le gel.** La signature
immunitaire (141 gènes) ne contient qu'UN des 12 gènes de flux : GZMB.
La signature stromale n'en contient qu'un : CD163. Les deux signatures
sont disjointes (recouvrement 0). Le score immunitaire est donc
indépendant des flux à 140/141 gènes près — et la variante
« leave-12-out » (ImmuneScore_wo12 : signature immunitaire moins GZMB,
140 gènes) est le test strictement non circulaire, pré-enregistré.

**Ce que « infiltration » veut dire ici — et sa limite.** L'ImmuneScore
ESTIMATE est un score d'enrichissement ssGSEA sur 141 gènes — une mesure
ARN d'infiltration, pas un comptage de cellules. Il partage la mesure
ARN avec les flux (même matrice), mais pas les gènes (140/141
indépendants) : une corrélation flux↔score n'est pas circulaire par
construction — et la variante wo12 le vérifie. Il ne distingue pas les
types cellulaires (pas de fractions CD8/macrophages/B) — ce que ferait
CIBERSORT, toujours inaccessible. Le StromalScore (141 gènes, 0 gène de
flux sauf CD163) sert de bras de contrôle (stroma, pas immunité).

**Hypothèses gelées.** H1 (infiltration explique) : (a) chaque flux
corrèle substantiellement avec l'ImmuneScore ; (b) la corrélation
intra-famille s'effondre après régression ; (c) ordonner par
l'ImmuneScore sépare les flux (S_sep au niveau IMMROT) ; (d) ordonner
les flux RÉSIDUALISÉS par CD8A résidualisé ne sépare plus. H0 (propriété
propre) : la corrélation persiste après contrôle de l'infiltration, par
toutes les voies (a)–(d).

**Critères gelés.** T1 : lien substantiel si moyenne |r| ≥ 0,30 pour
l'ImmuneScore (ou wo12) ; faible si < 0,15 pour les deux scores
immunitaires. T2 : EFFONDREMENT si moyenne |r| résiduelle < 0,30
(chute ≥ 45 % depuis 0,5563) ET fraction |r| > 0,5 < 0,20 ;
PERSISTANCE si chute < 20 % (moyenne résiduelle > 0,44) ; entre les
deux : partielle, à dire. T5 : I-IMM ou I-STR soutient H1 si écart
S_sep ≥ 0,45 (minimum IMMROT sans doublon) ; I-RES soutient H1 si écart
< 0,30, soutient H0 si écart ≥ 0,45. Verdict de synthèse : H1 totale si
T2 = effondrement ET I-RES < 0,30 ET (I-IMM ≥ 0,45 OU I-STR ≥ 0,45) ;
H1 partielle si T2 = partielle OU (I-IMM/I-STR entre 0,30 et 0,45) avec
I-RES < 0,70 ; H0 si T2 = persistance ET I-IMM < 0,30 ET I-STR < 0,30
ET I-RES ≥ 0,45 ; toute autre combinaison : zone grise. Références :
IMMROT sans doublon, moyenne +0,7521, minimum +0,4508 (CD68), CD8A
écart +0,9838 (réel 1,2310, nul 0,2472) ; P-RES §8.51 +0,9174 ;
régression §8.48 d_ssep = −0,175 + 1,705·C.

## 8.54.2 Porte J (jointure + validation du port) : OUVERTE

Rechargement du tarball (MD5 conforme) : 178 tumeurs primaires
(code 01) ; 0 NaN sur KRAS + 12 gènes immunitaires ; ordre KRAS brut
recalculé = `immune_kras_order_tcga.csv` (178/178 barcodes, valeurs
KRAS et immunitaires égales à 10⁻⁹ près). Signatures : 141 + 141 gènes
présents dans la matrice TCGA, disjointes, 1 seul gène de flux dans
chacune (GZMB immunitaire, CD163 stromale) — re-vérifié en machine.
**Porte J OUVERTE, les trois conditions tiennent.**

**Validation du port ssGSEA sur les données `ov` de tidyestimate**
(17 256 gènes × 10 échantillons, `data/ov.rda`, SHA
`3fe246db…478`) : 10 364 gènes communs trouvés (9 903 exacts + 461
récupérés par alias — l'attendu de la vignette est 10 364). Les 4
valeurs publiées de la vignette sont reproduites très en dessous du
critère gelé de 1 % relatif :

| Échantillon | Score | Calculé | Publié | Erreur relative |
|---|---|---|---|---|
| s516 | stromal | −285,49841 | −285,50 | 1,7×10⁻⁸ |
| s516 | immune | +165,75062 | +165,75 | 6,8×10⁻⁹ |
| s520 | stromal | +1927,51431 | +1927,51 | 6,9×10⁻¹⁰ |
| s520 | immune | +2326,15984 | +2326,16 | 1,5×10⁻⁹ |

Dans la matrice TCGA : 10 363 / 10 391 gènes communs (99,73 % ;
9 903 exacts + 460 alias). Les 460–461 renommages par alias sont
listés dans `infiltration_854_results.json` (ex. CTGF→CCN2, IL8→CXCL8,
WISP1→CCN4, FYB→FYB1).

Scores (n = 178) :

| Score | min | médiane | max | moyenne | écart-type |
|---|---|---|---|---|---|
| ImmuneScore (141 gènes) | −1556,6 | 598,5 | 3022,7 | 621,0 | 814,6 |
| ImmuneScore_wo12 (140 gènes) | −1546,5 | 620,3 | 3044,6 | 641,9 | 816,9 |
| StromalScore (141 gènes) | −1839,1 | 692,4 | 2166,6 | 581,7 | 825,7 |
| ESTIMATEScore (somme) | −3170,8 | 1267,1 | 4410,0 | 1202,6 | 1548,8 |

**r(ImmuneScore, StromalScore) = 0,7831** — les deux scores co-varient
fortement (tissu non tumoral partagé). **r(ImmuneScore,
ImmuneScore_wo12) = 0,9999948** — la variante non circulaire est quasi
identique au score complet : le seul gène partagé (GZMB) ne porte rien.
Descriptif vs pureté §8.51 : r(ImmuneScore, score acineux) = 0,133 ;
r(ImmuneScore, score îlots) = 0,221 ; StromalScore : 0,139 / 0,245.
L'infiltration ne re-mesure pas les proxys de pureté.

## 8.54.3 T1 — Chaque flux immunitaire suit l'infiltration : OUI, fortement

Pearson r (+ Spearman ρ) de chaque flux contre les trois scores ; R²
par flux (OLS sur [ImmuneScore] et sur [ImmuneScore, StromalScore]) ;
p brutes bilatérales, sans correction pour tests multiples (36 tests,
~1,8 faux positifs attendus à p < 0,05 sous le nul — le jugement porte
sur la moyenne, pas sur une p isolée).

| Gène | r Immune (p) | ρ Immune | r wo12 | r Stromal (p) | R² Immune |
|---|---|---|---|---|---|
| CD4 | **+0,893 (9,2×10⁻⁶³)** | +0,920 | +0,893 | +0,834 (2,9×10⁻⁴⁷) | **0,797** |
| CTLA4 | +0,851 (3,9×10⁻⁵¹) | +0,816 | +0,851 | +0,654 (4,1×10⁻²³) | 0,724 |
| FOXP3 | +0,827 (6,5×10⁻⁴⁶) | +0,817 | +0,827 | +0,725 (2,3×10⁻³⁰) | 0,684 |
| PDCD1 | +0,811 (6,6×10⁻⁴³) | +0,765 | +0,811 | +0,545 (3,9×10⁻¹⁵) | 0,658 |
| CD8A | +0,797 (2,4×10⁻⁴⁰) | +0,790 | +0,796 | +0,639 (8,1×10⁻²²) | 0,635 |
| CD163 | +0,731 (5,7×10⁻³¹) | +0,777 | +0,731 | +0,827 (6,5×10⁻⁴⁶) | 0,534 |
| CD8B | +0,721 (6,9×10⁻³⁰) | +0,702 | +0,721 | +0,535 (1,4×10⁻¹⁴) | 0,520 |
| GZMB | +0,696 (4,1×10⁻²⁷) | +0,665 | +0,694 | +0,491 (3,6×10⁻¹²) | 0,484 |
| CD19 | +0,678 (2,7×10⁻²⁵) | +0,623 | +0,678 | +0,449 (3,1×10⁻¹⁰) | 0,460 |
| CD68 | +0,661 (1,1×10⁻²³) | +0,633 | +0,661 | +0,613 (9,3×10⁻²⁰) | 0,436 |
| IFNG | +0,480 (1,2×10⁻¹¹) | +0,510 | +0,479 | +0,369 (4,0×10⁻⁷) | 0,231 |
| CD274 | +0,451 (2,6×10⁻¹⁰) | +0,490 | +0,451 | +0,521 (9,2×10⁻¹⁴) | 0,204 |

Moyenne |r| : **ImmuneScore 0,7164**, **wo12 0,7161**, StromalScore
0,6002 (Spearman 0,7089 / 0,7086 / 0,5928). **R² médian 0,527
(52,7 %), maximum 0,797 (CD4).** Avec [Immune, Stromal] : R² médian
0,579, maximum 0,844 (CD4). Critère gelé : lien SUBSTANTIEL
(≥ 0,30), largement dépassé — 2,4× le seuil. Les 12 corrélations sont
POSITIVES et toutes significatives à p ≤ 2,6×10⁻¹⁰. Les deux plus
faibles (CD274 0,451, IFNG 0,480) restent au-dessus du seuil gelé.
Deux remarques : (a) CD4 est le gène le plus lié à l'infiltration
(R² 79,7 %) — c'était aussi le plus lié à la pureté au §8.51 (R²
13,2 %) : CD4 est le gène le plus sensible à la composition, par les
deux voies, avec un ordre de grandeur d'écart ; (b) la variante wo12
donne les mêmes chiffres à la 3e décimale — le résultat n'est pas
porté par le gène partagé GZMB (r wo12 de GZMB lui-même : 0,694 contre
0,696 brut).

## 8.54.4 T2 — La corrélation intra-famille s'effondre après régression infiltration

Matrice 66 paires, brute contre résidus OLS ([1, ImmuneScore] et
sensibilités [wo12], [ImmuneScore, StromalScore]).

| Matrice | Pearson moyenne \|r\| | médiane \|r\| | fraction \|r\| > 0,5 | max \|r\| | Spearman moyenne \|r\| |
|---|---|---|---|---|---|
| Brute | **0,5563** | 0,5677 | 0,621 (41/66) | 0,8430 | 0,5403 |
| Résidus [ImmuneScore] | **0,2002** | 0,1739 | **0,045 (3/66)** | 0,6409 | 0,2044 |
| Résidus [wo12] | 0,2007 | 0,1761 | 0,045 (3/66) | 0,6412 | 0,2049 |
| Résidus [Imm, Strom] | 0,1902 | 0,1575 | 0,030 (2/66) | 0,6458 | 0,1992 |

**Chute : 64,0 % avec l'ImmuneScore, 63,9 % avec wo12, 65,8 % avec
les deux scores.** Critère gelé : EFFONDREMENT (moyenne résiduelle
0,2002 < 0,30 ET fraction > 0,5 de 0,045 < 0,20) — rempli sur les trois
variantes, à l'identique pour la variante non circulaire. La fraction
de paires fortes passe de 41/66 à 3/66. Retirer linéairement
l'infiltration mesurable retire les deux tiers de la corrélation
immunitaire — l'inverse exact du §8.51, où retirer la pureté ne
retirait rien (chute 1,5 %).

Les 3 paires qui restent fortes après régression : CD8A–CD8B (0,6409),
CD4–CD163 (0,5811), GZMB–IFNG (0,5202) ; suivent CD68–CD19 (0,4905)
et PDCD1–CTLA4 (0,4419). Le résidu n'est pas du bruit uniforme : il
est concentré sur quelques paires, en tête les deux chaînes du même
récepteur CD8 — un reste structuré, nommé au §8.54.8.

## 8.54.5 T3 — Couplage prédit : la régression §8.48 tient, avant comme après

Couplage C par contrôle immunitaire (moyenne des |r| avec les 11 autres
flux), brut contre résidualisé ; d_ssep prédit par d = −0,175 + 1,705·C.

| | C moyen | d_ssep prédit moyen |
|---|---|---|
| Brut | 0,5563 | **0,7735** (observé IMMROT : 0,7521) |
| Résidualisé [ImmuneScore] | 0,2002 | **0,1663** |

Sanité : la prédiction brute retrouve la moyenne IMMROT observée à 0,02
près (0,7735 contre 0,7521) — la régression §8.48 se réplique sur ces
données, comme au §8.51. Après résidualisation, la prédiction tombe à
0,1663 (d_pred résiduel par contrôle : 0,058 à 0,297). CD8A seul :
C 0,6514 → 0,2766, d_pred 0,9356 → **0,2966**. Le T3 ne fait que
traduire T2 en S_sep prédit ; le verdict se joue au T5.

## 8.54.6 T4 — Stratification : la cohésion persiste dans chaque moitié — test faible ici

Médiane de l'ImmuneScore (598,5), n = 89/89 ; matrice intra-famille
dans chaque moitié. La stratification wo12 (médiane 620,3) donne la
partition identique (r ≈ 1 entre les deux scores).

| Stratification | Moitié haute : moyenne \|r\| (frac. > 0,5) | Moitié basse : moyenne \|r\| (frac. > 0,5) |
|---|---|---|
| ImmuneScore (méd. 598,5) | 0,3638 (0,288) | 0,3926 (0,303) |

Si la cohésion venait de l'infiltration, elle devrait s'effondrer dans
chaque moitié (bande d'infiltration étroite). Elle ne s'effondre pas :
0,3638 / 0,3926 contre 0,5563 global — baisse de ~35 % / ~29 %, pas
d'effondrement. **Mais la prémisse de bande étroite n'est pas remplie
ici** : l'écart-type de l'ImmuneScore reste de 553,9 dans la moitié
haute et 474,8 dans la moitié basse, contre 814,6 global (58–68 %
conservés) ; les plages restent [601, 3023] et [−1557, 596]. Une
médiane ne fait pas une bande étroite : chaque moitié couvre encore une
énorme plage d'infiltration, et la cohésion résiduelle dans la moitié
est cohérente avec le résidu de T2 (0,2002) plus la variance
d'infiltration restante. **T4 est donc non concluant ici** — il ne
soutient pas H1, mais il ne la réfute pas non plus : c'est un test
faible, à refaire par terciles ou quartiles pour être tranchant (non
fait ici, §8.54.10). T4 n'entre pas dans la règle de verdict gelée.

## 8.54.7 T5 — Runs v6.2 : l'infiltration ordonne l'immunitaire, les résidus presque plus

Prédictions calculées AVANT de lire les sorties (depuis T1/T2 du jour) :
I-IMM d_pred +1,0466 (C = 0,7164) ; I-STR d_pred +0,8483
(C = 0,6002) ; I-RES d_pred +0,2966 (C_résid CD8A = 0,2766). 6 runs
v6.2, mode fast, graine 42, **6/6 exit 0** (lot 03:27–05:51 UTC
20 nov. ; §8.54.10 pour les deux redémarrages machine).

| Run | Contrôle → analysés | S_sep réel | S_sep nul | Écart | Prédit | MC réel / nul | Delta réel / nul | w | t0 |
|---|---|---|---|---|---|---|---|---|---|
| I-IMM | ImmuneScore → 12 imm. bruts | 1,4063 | 0,2121 | **+1,1942** | +1,0466 | 0,4832 / 0,3320 | 3,27 / 3,82 | 27 | 75,10 % |
| I-STR | StromalScore → 12 imm. bruts | 1,1248 | 0,1841 | **+0,9407** | +0,8483 | 0,4575 / 0,3627 | 4,30 / 4,55 | 30 | 49,11 % |
| I-RES | CD8A résid. → 11 imm. résid. | 0,4716 | 0,2733 | **+0,1982** | +0,2966 | 0,3696 / 0,3445 | 3,06 / 4,24 | 27 | 75,10 % |

Lecture par critère gelé :
- **I-IMM : séparation massive, au-dessus de la prédiction.** Écart
  +1,1942 — 1,14× la prédiction (+1,0466, +0,1476 au-dessus), 2,65× le
  minimum IMMROT (+0,4508), 1,21× CD8A brut (+0,9838). MC +0,1512
  (0,4832 contre 0,3320) : ici MC sépare, contrairement aux rotations
  §8.44 — noté, non utilisé pour le verdict (le verdict porte sur
  S_sep, gelé). L7a sépare en direction (up 0,2617 contre down
  −0,3500) : non utilisé, comme au §8.48. Seuil à 75,10 % de la série
  ordonnée. Critère gelé : I-IMM ≥ 0,45 → **soutient H1, fortement**.
- **I-STR : séparation massive aussi — mais pas une preuve
  indépendante.** Écart +0,9407 — 1,11× la prédiction (+0,8483,
  +0,0924 au-dessus), 2,09× le minimum IMMROT. MC +0,0948 (0,4575
  contre 0,3627). Seuil à 49,11 %. Critère gelé : I-STR ≥ 0,45 →
  **soutient H1**. Mais r(ImmuneScore, StromalScore) = 0,7831 : le
  score stromal porte l'axe de composition partagé (et CD163, gène
  de flux, est dans sa signature) — I-STR est une seconde vue du
  même axe, pas une confirmation indépendante d'I-IMM. Les deux bras
  disent la même chose parce qu'ils mesurent en partie la même chose.
- **I-RES : la séparation s'effondre, sans disparaître.** Écart
  +0,1982 contre +0,9838 pour CD8A brut (**20,2 % conservés, baisse
  de 79,8 %**) et contre +0,2966 prédit (−0,0984 en dessous — la
  régression §8.48 sur-prédit légèrement le résiduel ici). MC
  +0,0251 (0,3696 contre 0,3445) : MC ne sépare presque plus. L7a ne
  sépare pas (up 0,4183 contre up 0,1815, même direction) : non
  utilisé. Seuil à 75,10 %, comme I-IMM. Critère gelé : I-RES < 0,30
  → **soutient H1**. Mais +0,1982 n'est pas zéro : un résidu de
  séparation subsiste, cohérent avec les 3 paires fortes de T2 —
  c'est le reste structuré du §8.54.8, pas une réfutation de H1
  (le critère gelé est < 0,30, pas = 0).
- **Delta ne sépare pas** (nul supérieur au réel sur les 3 paires :
  3,82 contre 3,27 ; 4,55 contre 4,30 ; 4,24 contre 3,06) — rapporté
  descriptivement, comme au §8.51, non utilisé pour le verdict
  (Delta non élucidé, §8.49).

## 8.54.8 Verdict de synthèse

Règle gelée, test par test : T2 = EFFONDREMENT (0,5563 → 0,2002,
chute 64,0 %, fraction 0,621 → 0,045) ; I-IMM = +1,1942 (≥ 0,45) ;
I-STR = +0,9407 (≥ 0,45) ; I-RES = +0,1982 (< 0,30).
**Les trois conditions de H1 totale sont remplies : H1 est SOUTENUE.
La corrélation intra-famille immunitaire est expliquée par
l'infiltration immunitaire (score ESTIMATE calculé depuis la matrice
détenue).** H1 partielle est rejetée (les conditions de la totale sont
remplies) ; H0 est rejetée (aucune de ses conditions n'est remplie :
T2 n'est pas une persistance ; I-IMM/I-STR ne sont pas < 0,30 ; I-RES
n'est pas ≥ 0,45). Aucun consensus exigé entre les tests : le verdict
suit la règle gelée, et T4 — non concluant ici — est rapporté comme
tel, pas moyenné.

**Ce que cela ne dit pas.** (a) Cela ne dit pas que TOUTE la
corrélation est de l'infiltration : le résidu +0,1982 (20,2 % de CD8A
brut) et les 3 paires fortes restantes (CD8A–CD8B 0,6409, CD4–CD163
0,5811, GZMB–IFNG 0,5202) sont un reste structuré. CD8A–CD8B sont les
deux chaînes du même récepteur CD8 : une part du résidu peut être de
la biologie de récepteur (co-régulation des deux chaînes), pas de la
composition — non tranché ici. (b) Cela ne dit pas que la stratification
T4 est réfutée : ses moitiés sont trop larges pour être tranchantes ;
un découpage par terciles/quartiles reste à faire. (c) Cela ne dit pas
que le stroma explique quoi que ce soit indépendamment : I-STR suit
l'axe partagé (r = 0,7831). (d) Cela ne dit pas que l'infiltration
CAUSE la corrélation : le score partage la mesure ARN avec les flux
(la variante wo12 écarte la circularité au niveau des gènes, pas au
niveau de la mesure) ; une corrélation n'est pas une causalité, et
T4/T5 sont les garde-fous, pas une preuve causale. (e) Cela ne dit pas
quelles cellules portent la corrélation : pas de fractions par type
cellulaire (CIBERSORT/xCell toujours inaccessibles) — T CD8,
macrophages ou B, la question reste ouverte. (f) Cela ne dit pas que
la pureté est innocentée par une autre voie : le §8.51 reste valide
pour les proxys acineux/îlots — l'infiltration et la pureté sont deux
axes de composition différents, et c'est l'infiltration qui porte la
corrélation, pas la pureté. **En revanche, cela RÉVISE
l'interprétation du §8.51.8** : la corrélation immunitaire n'est pas
une « propriété propre aux tumeurs » — elle est largement un effet de
composition (infiltration). Le §8.51 avait raison sur la pureté, et
son H0 ne portait que sur la pureté ; la cause amont de la domination
IMMROT du §8.48 est désormais identifiée : le couplage contrôle↔flux
est porté par l'infiltration, pas par un artefact de pureté ni par une
co-régulation tumorale intrinsèque — à 80 % près, le reste nommé en
(a). (g) Les scores publiés de Yoshihara n'ont pas été comparés :
la validation externe du score calculé reste ouverte (§8.54b).

## 8.54.9 Provenance

- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant les calculs, dans les trois logs de lot, et après
  l'extraction). Mode `fast`, graine 42 (défaut), nul = bloc analysé
  permuté conjointement, graine 42 (default_rng frais par fichier),
  contrôle intact.
- **Protocole.** `PROTOCOL_infiltration_854.md`, SHA-256
  `f0f1247345941e9b014fa41cd842b9d5f1de07d833c0c2c74756c117e19fbdc7`,
  gelé le 20 nov. 2026 avant tout calcul et avant tout run de ce
  chantier. **Amendement, AVANT tout calcul T1–T5** : la première
  version (SHA `89be31ed…6918`) disait l'appariement d'alias NON
  appliqué ; la porte J a montré que la vignette de référence
  l'applique (461/488 gènes manquants récupérés dans `ov`) — sans lui,
  la validation du port sur `ov` est impossible (premier essai :
  9 903 gènes trouvés au lieu de 10 364, assertion échouée, arrêt
  propre avant tout résultat). L'amendement applique le port fidèle de
  `find_alias` (conservateur 1-à-1) ; le critère de validation (1 %
  relatif sur s516/s520) est inchangé. Aucun autre changement au
  protocole après le gel.
- **Entrées.** Tarball TCGA-PAAD RSEM, MD5
  `b09569ce3f4721f514bc137bd109ac0a` (vérifié) ; base immunitaire
  `pdac_immune_tcga_fluxes.csv`, SHA-256
  `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e` ;
  axe `immune_kras_order_tcga.csv`, SHA-256
  `31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d` ;
  écarts §8.44/§8.51 relus en machine dans `ssep_844_rotations.csv` /
  `purity_851_runs.json` (CD8A : réel 1,2310, nul 0,2472, écart
  +0,9838 ; P-RES : réel 1,1240, nul 0,2066, écart +0,9174). Sources :
  TCGA Firehose PAAD 2016-01-28 ; méthode ESTIMATE : Yoshihara et al.,
  Nat Commun 2013, doi 10.1038/ncomms3612 ; ssGSEA : Barbie et al.,
  Nature 2009, doi 10.1038/nature08460 ; implémentation de référence :
  tidyestimate 1.1.1 (CRAN, GitHub KaiAragaki/tidyestimate), tarball
  SHA-256 `cc747f787b6548a62219f3388ff6d93ad93cfcb60fe75f322fd712f41509514b`.
- **Nature des lignes.** Les flux immunitaires sont des mesures
  instrumentales (séquençage ARN, log2(RSEM+1), brutes) ; les scores
  ESTIMATE sont des valeurs calculées (ssGSEA sur 141 gènes, port
  Python validé à ~10⁻⁸ sur les valeurs publiées de la vignette) ;
  les résidus sont des valeurs calculées (OLS sur [1, ImmuneScore]) ;
  les nuls sont des lignes permutées (graine 42) — des échantillons
  hypothétiques, pas des mesures. Aucun mot humain, aucun échantillon
  hypothétique dans les séries réelles. Les scores publiés externes
  (Yoshihara Suppl. Data 2) n'ont pas été obtenus : aucune valeur
  externe n'entre dans ce chantier.
- **Sorties et scripts de ce chantier.**
  `estimate_ssgsea.py` (SHA `5e1205b0…4330`) : port ssGSEA +
  `filter_common_genes` (alias conservateur).
  `extract_estimate_data_854.py` : extraction .rda → CSV en clair
  (venv `/tmp/venv854`, parseur `rdata`).
  `analyze_infiltration_854.py` (SHA `cc20bbdb…42b`) : porte J, T1–T4.
  `build_infiltration_854.py` (SHA `7b9942de…ccd`) : scores + 6 CSV T5
  (résidus vérifiés : moyenne |r| = 0,2002, identique à T2).
  `extract_infiltration_854.py` (SHA `0135e1de…2f`) : lecture des
  6 runs (SHA des CSV vérifiés, version
  `v6.2.0-L7aL7b-CohenD-short`).
  `infiltration_854_gene_sets.csv` (SHA `35ea4150…9f8`, 141+141 gènes),
  `infiltration_854_scores.csv` (SHA `628732ec…aa7`, 178 tumeurs :
  barcode, KRAS brut, ImmuneScore, ImmuneScore_wo12, StromalScore,
  ESTIMATEScore),
  `infiltration_854_results.json` (SHA `2810bb3b…61`, T1–T4),
  `infiltration_854_results.csv` (SHA `7f6d4b4c…c0`, T1 par flux),
  `infiltration_854_immune_resid.csv` (SHA `61e0ecff…57b`, 12 flux
  résidualisés),
  `infiltration_854_csv_sha.json` (SHA `d98e0659…923`, SHA des 6 CSV T5),
  `infiltration_854_runs.json` (SHA `c04df5c5…af12`) / `.csv`
  (SHA `4386d766…fa3`, 6 runs).
  `data_infiltration_854/` : tarball tidyestimate + `.rda` extraits +
  `filter_common_genes.R` (SHA `1a6a1822…62fb`).
  Manifeste `manifest_v62_infiltration_854.txt`
  (SHA `3a8ca68c…bd5`) ; log `runs_v62_infiltration_854.log` ; unités
  systemd `v62-infil-854`, `v62-infil-854b`, `v62-infil-854c`.
- **Ce qui manque :** scores publiés externes (Yoshihara Suppl. Data 2,
  Aran Suppl. Data 1, Thorsson CIBERSORT/LF) — tentés, inaccessibles en
  accès direct (cf. §8.54.1) ; fractions par type cellulaire ; les
  moitiés T4 sont à n = 89 (estimations plus bruitées) et larges
  (§8.54.6) ; les p de T1 sont brutes, sans correction pour tests
  multiples.

## 8.54.10 Ce qui manque, ce qui reste ouvert

- **Comparaison aux scores publiés de Yoshihara (§8.54b).** Les scores
  ESTIMATE publiés par tumeur (Suppl. Data 2, PMC3826632) sont la
  validation externe du score calculé ici (même méthode, mêmes données
  TCGA RNAseqV2) : corrélation score calculé ↔ score publié, et
  re-lecture de T2/T5 avec le score publié. Nécessite un navigateur
  vivant (défi proof-of-work PMC) — tâche pour le coordinateur.
- **Fractions par type cellulaire.** CIBERSORT/xCell diraient si la
  corrélation est portée par les T CD8, les macrophages, les B, ou
  tous ensemble — et si le résidu CD8A–CD8B suit une fraction
  particulière. Inaccessible ici (compte CIBERSORTx, interstitiel PMC).
- **Stratification fine (T4 tranchant).** Terciles ou quartiles
  d'ImmuneScore, ou bandes étroites (±0,5 écart-type) : la médiane ne
  suffit pas (§8.54.6). Non fait ici.
- **Le résidu structuré.** CD8A–CD8B 0,6409, CD4–CD163 0,5811,
  GZMB–IFNG 0,5202 après régression : biologie de récepteur, autre
  variable latente (sous-type moléculaire — autre piste du §8.48.8,
  toujours non testée), ou queue de l'infiltration non linéaire ?
  Non tranché ici.
- **Pureté par scores externes.** Autre piste approuvée le 19 nov. au
  soir (chantier jumeau de celui-ci, non lancé) : les estimations
  ABSOLUTE / ESTIMATE / CPE d'Aran et al. 2015 donneraient le contrôle
  indépendant des proxys ARN du projet — et fermeraient la boucle
  pureté/infiltration (ESTIMATE publie aussi une pureté).
- **Incident d'exécution.** La machine a redémarré DEUX fois pendant
  le lot : ~03h44 UTC (uptime 0 min à 03h45:38) et ~05h43 UTC (uptime
  0 min à 05h43:53) — cause non établie, comme aux §8.41/§8.44/§8.48/
  §8.51 ; unités `--collect`, donc introuvables après leur mort. La
  première unité `v62-infil-854` est morte avec le 1er redémarrage
  (1/6 terminé, EXIT 0, aucune sortie perdue) ; la relance reprenable
  `v62-infil-854b` a repris au 2e run à 03h45 et en a terminé 4 autres
  avant de mourir au 2e redémarrage (5/6 terminés, EXIT 0) ; la
  relance `v62-infil-854c` a terminé le dernier run à 05h51:19 UTC.
  Bilan final : **6/6 exit 0, 0 échec**, lot 03:27:11–05:51:19 UTC
  20 nov. (`=== FIN 2026-11-20T05:51:19Z deja_faits=5 termines=1
  echecs=0 ===` ; 6 lignes `EXIT_` à 0 dans le log).
- **Périmètre.** 6 nouveaux runs v6.2 au maximum (protocole §6), aucun
  autre. Aucun nouveau seuil proposé, aucun code modifié, aucun push
  GitHub dans ce chantier (publication sur go séparé ; règle permanente
  « Toujours github et pdf !!! » — par le coordinateur).

— Fin de la §8.54. —
