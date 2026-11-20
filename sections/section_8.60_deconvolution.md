# §8.60 Déconvolution par type cellulaire : aucun type ne porte la corrélation — elle est portée par l'infiltrat dans son ensemble

Date : 20 novembre 2026 (11h45–13h17 UTC ; 06h45–08h17 heure de Montréal).
Go : coordinateur, 20 nov. 2026. Question ouverte des §8.54.8(e) et
§8.55.11.
Protocole gelé avant tout téléchargement, avant tout calcul et avant tout
run : `PROTOCOL_deconvolution_860.md` (SHA-256
`471568b1eb83027d4341c7ec5632b5749cf60aa2d06e8a4ddbf2315ffed86d57`).

## Verdict d'abord

**Aucun type cellulaire ne porte la corrélation intra-famille
immunitaire. Verdict gelé : ZONE GRISE, test par test — ni H1-type ni
H0-type stricte ne sont soutenues.** Les fractions CIBERSORT publiées
(Thorsson et al. 2018, via le miroir imogimap) sont obtenues et jointes
(n effectif 151/178). Les deux types les plus liés aux flux — lymphocytes
B naïfs (moyenne |r| = 0,3314) et T CD8 (0,3293) — ordonnent bel et bien
les flux immunitaires (**écarts S_sep +0,5867 et +0,5609**, au-dessus du
minimum IMMROT +0,4508 et au-dessus des prédictions +0,3900 / +0,3865).
Mais retirer le type le plus porteur ne retire presque rien de la
cohérence : **0,5044 → 0,4805 après régression sur les B naïfs (chute
4,7 %)**, 0,4673 avec les trois premiers types (chute 7,4 %), 0,4692 avec
les deux types qualifiants (chute 7,0 %) — et les flux résidualisés
séparent encore **+0,7692** (78,2 % du brut CD8A +0,9838), contre +0,1982
quand on résidualise sur l'ImmuneScore GLOBAL au §8.54. **Le contraste
avec le §8.54 est l'information : ce qui effondre la corrélation, c'est
la quantité totale d'infiltrat, pas un type particulier.**

**Le bras secondaire le confirme par une voie indépendante de l'ARN.**
La fraction leucocytaire par méthylation (Raphael et al. 2017, Table S1,
déjà détenue) suit les 12 flux (moyenne |r| = 0,5456, toutes p ≤ 0,0069),
retire un tiers de la cohésion (**0,5035 → 0,3372, chute 33,0 %** —
verdict gelé du bras L : PARTIELLE) et ordonne les flux (**écart S_sep
+0,7129**, prédit +0,7552). Une quantité GLOBALE d'infiltrat, mesurée
sans ARN, porte un tiers de la corrélation ; aucun type seul n'en porte
mesurablement. La part restante — deux tiers après la fraction
leucocytaire, un cinquième après l'ImmuneScore — reste une co-expression
propre aux tumeurs, ou une variable latente non testée (sous-type
moléculaire, état d'activation).

**Les trois nuances sont nommées, pas cachées.** (a) Les deux types
porteurs ne sont pas du bruit : leurs écarts dépassent le minimum IMMROT
et leurs prédictions de ~0,18–0,20, et leurs liens aux flux sont
concentrés sur leurs gènes marqueurs (CD19 r = 0,712 avec les B naïfs ;
CD8A r = 0,697 et CD8B r = 0,598 avec les T CD8) — une part mécanique,
nommée au §8.60.8, qui ne suffit pas à expliquer la cohésion entre les
autres paires (T2d : 0,5213 → 0,5104 en excluant les paires contenant
CD19). (b) Les macrophages M0, troisième type, sont ANTI-corrélés aux
flux (moyenne |r| = 0,2878, toutes r négatives sauf CD68) : dans le
compartiment immunitaire, plus de M0 veut dire moins de signal
lymphocytaire — un effet de composition interne à l'infiltrat, pas un
porteur de la corrélation. (c) L'effectif est sélectionné : 27 tumeurs
sur 178 n'ont pas de CIBERSORT (26 tout-NaN + 1 absente), toutes hors du
sous-ensemble whitelisting de Raphael — la brute y passe déjà de 0,5563
à 0,5044 par la seule sélection (−0,0519, même ordre qu'au §8.55).

## 8.60.1 Question, méthode, inventaire des sources (avant le gel)

**Question (§8.54.8(e), §8.55.11).** Le §8.54 a établi que la corrélation
intra-famille immunitaire (0,5563) est expliquée par l'infiltration
immunitaire GLOBALE (ImmuneScore ESTIMATE calculé : 0,5563 → 0,2002,
chute 64,0 % ; I-RES +0,1982, 20,2 % conservés). Le §8.55 a établi que la
pureté ABSOLUTE externe en explique environ un tiers (0,5040 → 0,3757,
chute 25,5 % ; E-RES +0,6499). Reste ouverte la composition de
l'infiltrat : QUELS types cellulaires portent la corrélation — T CD8,
macrophages, B, fibroblastes, autres ? Ce chantier teste cette question.
Il ne re-teste ni l'ImmuneScore global (§8.54) ni ABSOLUTE (§8.55) et
n'importe aucune conclusion d'une autre expérience : seuls les chiffres
de ce chantier (Porte D, T1–T5 du jour) et les écarts relus des
§8.44/§8.48/§8.51/§8.54/§8.55 font le verdict.

**Ce qui existe réellement.** (a) Tarball TCGA-PAAD RSEM, Broad GDAC
Firehose 2016-01-28, MD5 `b09569ce…ac0a` (détenu) — la même matrice que
§8.54/§8.55. (b) Base immunitaire TCGA `pdac_immune_tcga_fluxes.csv`,
n = 178, 12 gènes BRUTS log2(RSEM+1) : CD8A, CD8B, CD4, FOXP3, CD68,
CD163, CD274, PDCD1, CTLA4, GZMB, IFNG, CD19 ; fichier d'axe joint
`immune_kras_order_tcga.csv` (step, sample, kras_raw) — clé de jointure
PAR BARCODE, jamais par index. (c) AUCUNE fraction par type cellulaire
détenue avant ce chantier (recherche §8.54.1 / §8.55.2 : 0 occurrence de
fractions CIBERSORT, xCell, TIMER, MCP-counter par échantillon).
(d) Détenue, non encore testée comme contrôle d'infiltration : la colonne
`DNA.methylation.leukocyte.percent.estimate` du `sampInfo` transcrit au
§8.55 (`purity_855_sampinfo.csv`, 181 lignes × 55 colonnes) — fraction
leucocytaire par méthylation ADN, indépendante de l'ARN, globale (tous
leucocytes confondus) — bras secondaire L, gelé au protocole §7.

**Sources externes tentées (journal complet :
`data_deconvolution_860/deconvolution_860_attempts.log`).**
- **Thorsson et al. 2018, Immunity 48:812–830.e14** (fractions CIBERSORT
  22 types + fraction leucocytaire, PMC5982584, doi
  10.1016/j.immuni.2018.03.023) — route 1a : Europe PMC
  `supplementaryFiles` renvoie HTTP 200, 296 o, XML d'erreur « Article
  with id PMC5982584 is not open access one » (fichier
  `thorsson_europepmc_supp.out` conservé). Routes 1b/1c (PMC direct,
  fichiers `mmc` Cell Press) : non tentées au-delà du constat — défi
  proof-of-work PMC documenté au §8.54.1, porte D ouverte par ailleurs.
- **TIMER2.0 (Li et al. 2020, Nucleic Acids Res, doi 10.1093/nar/gkaa407)**
  : serveur Shiny interactif (`timer.cistrome.org`, HTTP 301) ; aucun
  fichier de scores en vrac identifié ; `cistrome.org/TIMER/misc/AGPall.zip`
  répond 301 (le 404 du §8.54 n'est plus reproduit tel quel, redirection
  non poursuivie). Source écartée : pas de téléchargement en vrac.
- **xCell (Aran, Hu, Butte 2017, Genome Biol 18:220, doi
  10.1186/s13059-017-1349-1, PMC5688663)** : scores précalculés pour
  9 947 échantillons TCGA/TARGET cités (Additional file 6) — existence
  confirmée par recherche web, fichier NON téléchargé : porte D déjà
  ouverte (source 5), le protocole gelé ne prévoit pas de second bras par
  type. Piste nommée au §8.60.10.
- **Voie C (MCP-counter / EPIC recalculés depuis la matrice détenue)** :
  non utilisée — sources publiées obtenues.
- **Source retenue (5) : imogimap (Korkut lab), miroir public des
  fractions CIBERSORT de Thorsson.** Dépôt GitHub `korkutlab/imogimap`,
  documentation des données `R/data.R` (via rdrr.io) : objet
  `TCGA_IMCell_fraction` — « CIBERSORT fraction of each 21 immune cell
  type within immune population », 11 080 lignes, `PATIENT_BARCODE` +
  21 types, source citée `cibersort.stanford.edu` ; objet
  `TCGA_Leukocyte_fraction` — fraction leucocytaire TCGA, source citée
  doi 10.1016/j.cell.2018.03.022. Fichiers téléchargés via
  `raw.githubusercontent.com` (HTTP 200, tailles conformes à l'API
  GitHub) : `TCGA_IMCell_fraction.rda` (1 053 486 o, SHA-256
  `739bfa99…70370c0`), `TCGA_Leukocyte_fraction.rda` (114 032 o, SHA-256
  `f576f5f2…a4e68289`).

**Circularité (comptée en machine, §8.60.2).** La matrice LM22
(Newman et al. 2015, Nat Methods, doi 10.1038/nmeth.3337 — 547 gènes,
22 types), obtenue depuis le miroir public GitHub
`SiYangming/CIBERSORT-DATA`, `LM22.txt` (HTTP 200, 146 759 o, SHA-256
`8b1b4bb2…cd36c`, 547 lignes × 23 colonnes vérifiées), contient comme
lignes 10 des 12 gènes de flux : CD19, CD4, CD68, CD8A, CD8B, CTLA4,
FOXP3, GZMB, IFNG, PDCD1 — absents : CD163, CD274. Les marqueurs
« row-max » (gène dont la colonne du type est le maximum de la ligne
LM22) parmi les 12 flux, par type : B.Cells.Naive → CD19 ;
T.Cells.CD8 → CD8A, CD8B ; T.Cells.CD4.Memory.Activated → IFNG ;
T.Cells.Follicular.Helper → PDCD1 ; T.Cells.Regulatory.Tregs → CTLA4,
FOXP3 ; NK.Cells.Activated → GZMB ; Macrophages.M2 → CD4, CD68.
La sensibilité T2d (§8.60.4) exclut les paires contenant un marqueur
row-max du TOP1.

**Hypothèses gelées.** H1-type : la corrélation est portée par la
quantité d'un ou plusieurs types cellulaires infiltrants — (a) chaque
flux corrèle substantiellement avec au moins un type ; (b) après
régression sur le(s) type(s) porteur(s), la corrélation s'effondre ;
(c) ordonner les flux par la fraction du type porteur les sépare
(S_sep au niveau IMMROT) ; (d) ordonner les flux RÉSIDUALISÉS par CD8A
résidualisé ne sépare plus. H0-type : la corrélation persiste après
contrôle de chaque type et de leur combinaison, par toutes les voies
(a)–(d).

**Critères gelés.** T1 : type « porteur candidat » si moyenne |r| ≥ 0,30
sur les 12 flux ; « faible » si < 0,15 pour tous les types. TOP1/TOP2 =
les deux premiers du classement T1 (égalité départagée par la moyenne
des |ρ|). T2 : EFFONDREMENT si moyenne |r| résiduelle < 0,30 (chute
≥ 45 % depuis la brute appariée) ET fraction |r| > 0,5 < 0,20 ;
PERSISTANCE si chute < 20 % (moyenne résiduelle > 0,80 × brute
appariée) ; entre les deux : partielle. Primaire T2 = résidus sur
[1, TOP1] ; sensibilités (b) TOP1–3, (c) tous les types à moyenne
|r| ≥ 0,30 (max 5), (d) paires sans marqueur row-max du TOP1. T5 :
D-TOP1/D-TOP2 soutiennent H1-type si écart S_sep ≥ 0,45 (minimum IMMROT
sans doublon) ; D-RES soutient H1-type si écart < 0,30, soutient H0-type
si écart ≥ 0,45. Verdict : H1-type SOUTENUE si T2 primaire =
effondrement ET D-RES < 0,30 ET (D-TOP1 ≥ 0,45 OU D-TOP2 ≥ 0,45) ;
H1-type PARTIELLE si T2 = partielle OU (D-TOP1/D-TOP2 entre 0,30 et
0,45) avec D-RES < 0,70 ; H0-type SOUTENUE si T2 = persistance ET
D-TOP1 < 0,30 ET D-TOP2 < 0,30 ET D-RES ≥ 0,45 ; toute autre combinaison :
zone grise, test par test. Bras L (fraction leucocytaire par
méthylation) : mêmes critères T1-L/T2-L, 2 runs D-LEU, verdict séparé —
il ne change pas le verdict par type.

## 8.60.2 Porte D (source) : OUVERTE — jointure, identification, sélection

**Fichiers obtenus, lus en clair.** `TCGA_IMCell_fraction.rda` : objet
unique `TCGA_IMCell_fraction`, 11 080 lignes × 23 colonnes
(`PATIENT_BARCODE` + 22 types — la documentation du package en annonce
21, le fichier en contient 22 : les 22 types LM22, sans les colonnes
P-value/corrélation/RMSE de la sortie CIBERSORT brute). Sommes par ligne :
min 0,0000, médiane 1,0000, max 1,0000 — fractions relatives normalisées,
conformes à la documentation (« values are not absolute values and are
normalized by the sum of all 21 types »). 1 387 lignes tout-NaN
(CIBERSORT indisponible, 12,5 % ; aucun NaN partiel — les NaN sont
tout-ou-rien par ligne, vérifié en machine). `TCGA_Leukocyte_fraction.rda` :
objet unique, 10 718 lignes × 2 colonnes (`Tumor_Sample_ID`,
`Leukocyte_fraction`), 0 NaN, min 0,0000, médiane 0,1709, max 0,9642 —
la documentation rdrr.io du package cite 8 775 lignes / 3 variables :
version postérieure du fichier, écart noté, sans conséquence (les
valeurs sont validées ci-dessous).

**Jointure par patient (12 caractères), puis par échantillon (15).**
IMCell : **177/178 appariées** (≥ 100, porte D OUVERTE) ; absente :
`TCGA-IB-7654-01A-11R-2156-07`. Parmi les 177 : **26 tout-NaN** —
**n effectif complet : 151**. Fraction leucocytaire imogimap :
178/178 appariées. Fraction leucocytaire par méthylation (sampInfo) :
150/178 non nulles. ABSOLUTE (§8.55) : 149/178.

**Identification comme données de Thorsson — trois vérifications.**
(a) Effectif exact : 11 080 lignes = les 11 080 tumeurs de Thorsson et
al. (et d'iAtlas : « TCGA Samples: 11,080 »). (b) Sommes par ligne
médiane 1,0000 (fractions CIBERSORT relatives normalisées). (c) La
fraction leucocytaire imogimap corrèle à **r = +0,9947 (n = 150,
p = 3,4×10⁻¹⁴⁸)** avec la fraction leucocytaire par méthylation de
Raphael (Table S1, détenue) — deux voies indépendantes mesurent la même
quantité à 0,5 % près ; une erreur d'identification est invraisemblable.
Descriptif : LF_imogimap vs ImmuneScore (§8.54) r = +0,8575 (n = 178) ;
leuco_méthyl vs ImmuneScore r = +0,8193 (n = 150) ; LF_imogimap vs
ABSOLUTE r = −0,7021 (n = 149) ; leuco_méthyl vs ABSOLUTE r = −0,6901
(n = 149) — cohérent : plus de leucocytes, moins de pureté, plus
d'ImmuneScore.

**Sélection (effet nommé, comme au §8.55).** Les 27 tumeurs sans
CIBERSORT (26 tout-NaN + 1 absente) sont TOUTES sans ABSOLUTE (27/27,
sur 29 sans ABSOLUTE au total) : ce sont les non-whitelistées de
Raphael. Leur ImmuneScore médian est plus bas (268,8 contre 604,4 chez
les 151 complètes) mais leur fraction leucocytaire imogimap est
identique (médiane 0,2995 contre 0,3003) — la missingness CIBERSORT
n'est pas « peu de leucocytes », c'est le sous-ensemble non-whitelisté.
La fraction leucocytaire par méthylation est indisponible pour les 26
(médiane non calculable, n = 0). Conséquence : la cohésion brute sur
n = 151 est déjà plus faible qu'à n = 178 (**0,5044 contre 0,5563,
−0,0519 par la seule sélection**, même ordre qu'au §8.55 : −0,0523) —
toutes les comparaisons T2 se font sur le même n = 151, brute recalculée,
jamais en mélangeant les n.

## 8.60.3 T1 — Chaque flux immunitaire suit-il un type cellulaire ? Faiblement, deux types à peine au-dessus du seuil

Pearson r (+ Spearman ρ) de chaque flux contre chaque type (n = 151) ;
p brutes bilatérales, sans correction pour tests multiples (264 tests,
~13 faux positifs attendus à p < 0,05 sous le nul — le jugement porte
sur les moyennes, pas sur une p isolée). Moyenne des |r| par type,
classement décroissant :

| Type | moyenne \|r\| | moyenne \|ρ\| | R² médian | R² max |
|---|---|---|---|---|
| **B.Cells.Naive (TOP1)** | **0,3314** | 0,4135 | 0,140 | 0,507 |
| **T.Cells.CD8 (TOP2)** | **0,3293** | 0,3680 | 0,089 | 0,485 |
| Macrophages.M0 (TOP3) | 0,2878 | 0,2633 | 0,072 | 0,271 |
| Macrophages.M2 | 0,2451 | 0,2297 | 0,065 | — |
| Macrophages.M1 | 0,2344 | 0,1690 | 0,031 | — |
| T.Cells.Follicular.Helper | 0,1990 | 0,2135 | 0,031 | — |
| B.Cells.Memory | 0,1766 | 0,2796 | 0,031 | — |
| T.Cells.CD4.Memory.Activated | 0,1735 | 0,1697 | 0,032 | — |
| Plasma.Cells | 0,1617 | 0,1504 | 0,019 | — |
| Mast.Cells.Activated | 0,1605 | 0,1009 | 0,027 | — |
| T.Cells.Regulatory.Tregs | 0,1473 | 0,1919 | 0,029 | — |
| T.Cells.CD4.Naive | 0,1321 | 0,0267 | 0,024 | — |
| Monocytes | 0,1298 | 0,2061 | 0,009 | — |
| NK.Cells.Resting | 0,1268 | 0,1232 | 0,015 | — |
| NK.Cells.Activated | 0,1261 | 0,1137 | 0,012 | — |
| Eosinophils | 0,0992 | 0,0866 | 0,011 | — |
| Neutrophils | 0,0919 | 0,1087 | 0,007 | — |
| Dendritic.Cells.Resting | 0,0853 | 0,1213 | 0,010 | — |
| Mast.Cells.Resting | 0,0762 | 0,0895 | 0,003 | — |
| Dendritic.Cells.Activated | 0,0699 | 0,0771 | 0,004 | — |
| T.Cells.CD4.Memory.Resting | 0,0621 | 0,1000 | 0,003 | — |
| T.Cells.gamma.delta | 0,0497 | 0,0413 | 0,001 | — |

Seuls 2 types sur 22 dépassent le seuil gelé de 0,30 — et de justesse
(0,3314 et 0,3293, soit 1,10× et 1,10× le seuil) ; le troisième est en
dessous (0,2878). À comparer : l'ImmuneScore global (§8.54) donnait une
moyenne |r| de 0,7164 et la fraction leucocytaire par méthylation
(bras L, §8.60.7) 0,5456 — les types seuls sont 2,2× et 1,6× plus faibles
que les mesures globales. Les 20 autres types sont faibles (< 0,30),
dont 12 sous 0,15.

**Par flux, TOP1 (B.Cells.Naive, médiane 0,0218, moyenne 0,0566, max
0,4022 — distribution très asymétrique, beaucoup de zéros).**
r : CD19 **+0,712** (R² 0,507 — son gène marqueur), PDCD1 +0,557, CTLA4
+0,451, CD8A +0,422, FOXP3 +0,392, CD8B +0,388, GZMB +0,359, CD4 +0,242,
IFNG +0,126, CD163 +0,113, CD274 +0,104, CD68 −0,110. Non significatifs
(p ≥ 0,05) : CD68 (0,177), CD163 (0,166), CD274 (0,202), IFNG (0,123).
Le lien est concentré sur les lymphocytes (CD19 en tête) et nul sur les
macrophages/checkpoint CD274. Descriptif : r(B naive, ImmuneScore) =
+0,4723 ; r(B naive, ABSOLUTE) = −0,3000 ; r(B naive, LF_imogimap) =
+0,5582.

**Par flux, TOP2 (T.Cells.CD8, médiane 0,0937, moyenne 0,0966, max
0,2258).** r : CD8A **+0,697** (R² 0,485 — son gène marqueur), CD8B
+0,598, PDCD1 +0,439, GZMB +0,426, CTLA4 +0,356, CD19 +0,307, IFNG
+0,290, FOXP3 +0,228, CD163 +0,198, CD4 +0,176, CD274 +0,095, CD68
−0,142. Non significatifs : CD68 (0,081), CD274 (0,246). Descriptif :
r(CD8, ImmuneScore) = +0,2481 ; r(CD8, ABSOLUTE) = −0,3897 ; r(CD8,
LF_imogimap) = +0,2600. Le type CD8 corrèle moins avec l'ImmuneScore
global (0,2481) que les B naïfs (0,4723) : CD8 n'est pas le meilleur
reflet de l'infiltration globale dans ces données.

**TOP3 (Macrophages.M0, médiane 0,0797, moyenne 0,1028, max 0,5145).**
r TOUTES négatives sauf CD68 (+0,026, p = 0,754, seule non
significative) : CD8A −0,521, PDCD1 −0,407, CD8B −0,394, CTLA4 −0,380,
GZMB −0,340, FOXP3 −0,274, CD4 −0,262, CD19 −0,237, IFNG −0,209, CD163
−0,206, CD274 −0,198. Descriptif : r(M0, ImmuneScore) = −0,3151 ;
r(M0, ABSOLUTE) = +0,2659 ; r(M0, LF_imogimap) = −0,2775. Lecture :
dans le compartiment immunitaire (fractions relatives, somme = 1), une
part M0 élevée va avec un signal lymphocytaire faible — effet de
composition interne, pas un porteur positif de la corrélation.

## 8.60.4 T2 — La corrélation intra-famille survit à la régression sur les types : PERSISTANCE

Matrice 66 paires, sur les n = 151 appariées (la brute de référence est
recalculée sur ce sous-ensemble, jamais importée du §8.54).

| Matrice | Pearson moyenne \|r\| | médiane \|r\| | fraction \|r\| > 0,5 | max \|r\| |
|---|---|---|---|---|
| Brute (n = 151) | **0,5044** | 0,5390 | 0,561 (37/66) | 0,8520 |
| Résidus [1, TOP1 = B.Cells.Naive] (a, PRIMAIRE) | **0,4805** | 0,4965 | **0,500 (33/66)** | 0,8238 |
| Résidus [1, TOP1, TOP2, TOP3] (b) | 0,4673 | 0,4636 | 0,364 (24/66) | 0,7888 |
| Résidus [1, types à moyenne \|r\| ≥ 0,30] (c) | 0,4692 | 0,4639 | 0,394 (26/66) | 0,7912 |
| Paires sans marqueur row-max TOP1 (d) : brute → résiduelle | 0,5213 → **0,5104** | 0,5472 → 0,5237 | 0,582 → 0,564 | — |

**Chute primaire : 4,7 %** (0,5044 → 0,4805) ; (b) 7,4 % ; (c) 7,0 %.
Critère gelé : ni EFFONDREMENT (résiduelle 0,4805 > 0,30 ; chute 4,7 %
< 45 %) ni PARTIELLE (chute 4,7 % < 20 %) : **T2 = PERSISTANCE**.
Retirer linéairement le type le plus porteur — ou les trois premiers,
ou les deux qualifiants — ne retire presque rien de la corrélation.
C'est l'inverse exact du §8.54, où retirer l'ImmuneScore global
retirait 64,0 %, et du bras L ci-dessous (−33,0 %).

**Garde-fou de circularité (d).** En excluant les paires contenant CD19
(seul marqueur row-max LM22 des B naïfs parmi les 12 flux) : 11 gènes,
55 paires, brute 0,5213 → résiduelle 0,5104 (chute 2,1 %). La
persistance n'est pas un artefact du gène marqueur : même entre paires
ne contenant AUCUN marqueur du TOP1, la cohésion ne bouge pas. Le lien
B naïfs ↔ CD19 (r = 0,712) est réel mais local : il ne porte pas la
cohésion de la famille.

## 8.60.5 T3 — Couplage prédit : la régression §8.48 tient, avant comme après

Couplage C par contrôle immunitaire (moyenne des |r| avec les 11 autres
flux), brut contre résidualisé sur TOP1 ; d_ssep prédit par
d = −0,175 + 1,705·C.

| | C moyen | d_ssep prédit moyen |
|---|---|---|
| Brut (n = 151) | 0,5044 | **0,6850** |
| Résidualisé [TOP1] | 0,4805 | **0,6442** |

Sanité : la prédiction brute (0,6850) est dans la gamme des écarts
IMMROT observés — la régression §8.48 se réplique sur ces données.
CD8A seul : C 0,6072 → 0,5770, d_pred 0,8581 → **0,8089**. Le T3 ne fait
que traduire T2 en S_sep prédit ; le verdict se joue au T5 — et c'est
là que la prédiction sera mise en défaut pour D-TOP1/D-TOP2 (§8.60.7).

## 8.60.6 T4 — Stratification : la cohésion persiste dans chaque moitié — et la moitié basse EST une bande étroite

Médiane des B naïfs = 0,0218 (n = 76/75) ; matrice intra-famille dans
chaque moitié.

| Stratification | Moitié haute : moyenne \|r\| (frac. > 0,5) | Moitié basse : moyenne \|r\| (frac. > 0,5) |
|---|---|---|
| B.Cells.Naive (méd. 0,0218) | 0,4659 (0,485, 32/66) | 0,4003 (0,318, 21/66) |

La cohésion persiste dans les deux moitiés (0,47 et 0,40, contre 0,5044
global) — réduite, pas effondrée. Ici, contrairement au §8.54.6, la
moitié BASSE est une vraie bande étroite : l'écart-type des B naïfs y
est de 0,0063, soit 7,6 % de l'écart-type global (0,0827) — la fraction
est quasi nulle pour toute la moitié basse (médiane globale 0,0218,
beaucoup de zéros). Dans cette bande où les B naïfs sont
pratiquement absents, la cohésion reste à 0,4003 : les B naïfs ne
portent pas la cohésion. La moitié haute reste large (écart-type
0,0907 > global) : elle n'est pas tranchante, et n'a pas besoin de
l'être — la moitié basse suffit à l'argument. **T4 soutient H0-type
par une voie non paramétrique, indépendante de toute linéarité.**

## 8.60.7 Bras L — Fraction leucocytaire par méthylation : PARTIELLE (un tiers, voie indépendante de l'ARN)

Source : `purity_855_sampinfo.csv`, colonne
`DNA.methylation.leukocyte.percent.estimate` (Raphael et al. 2017,
Table S1, via pdacR — provenance §8.55.2) ; n = 150 appariées non
nulles. Rappel : cette fraction corrèle à r = +0,9947 avec la fraction
leucocytaire imogimap (§8.60.2) — deux mesures de la même quantité
globale, l'une par méthylation, l'autre par déconvolution ARN.

**T1-L.** Pearson r de chaque flux contre la fraction leucocytaire :
CD8A +0,660, CD8B +0,582, CD4 +0,614, FOXP3 +0,687, CD68 +0,220, CD163
+0,483, CD274 +0,276, PDCD1 +0,704, CTLA4 +0,713, GZMB +0,581, IFNG
+0,325, CD19 +0,702. **Moyenne |r| = 0,5456** (Spearman 0,5294) —
lien SUBSTANTIEL (≥ 0,30, dépassé de 82 %). Tous significatifs à
p ≤ 0,0069 (12/12 ; le plus faible est CD68, r = 0,220). À comparer :
ImmuneScore 0,7164 (§8.54), ABSOLUTE 0,4932 (§8.55) — la fraction
leucocytaire par méthylation se place entre les deux, au-dessus
d'ABSOLUTE.

**T2-L.** Cohésion 66 paires, n = 150 : brute **0,5035** (médiane 0,5422,
fraction > 0,5 : 0,561, 37/66) → résidus [1, leuco_méthyl] **0,3372
(médiane 0,3256, chute 33,0 %)**, fraction |r| > 0,5 : 0,167 (11/66). Critère gelé : ni EFFONDREMENT (résiduelle 0,3372 >
0,30 ; chute 33,0 % < 45 %) ni PERSISTANCE (chute 33,0 % > 20 % ;
résiduelle 0,3372 < 0,80 × 0,5035 = 0,4028) : **T2-L = PARTIELLE**.
Retirer linéairement toute la fraction leucocytaire retire un tiers de
la corrélation — et en laisse deux tiers.

**T3-L.** C brut 0,5035, d_pred 0,6835 ; C résiduel 0,3372, d_pred
0,4000. Descriptif, pas un verdict seul.

**T5-L.** Voir §8.60.8 (D-LEU +0,7129, prédit +0,7552). Le bras L ne
change pas le verdict par type (il ne distingue pas les types) ; il est
rapporté séparément comme test d'infiltration indépendante de l'ARN :
une quantité GLOBALE d'infiltrat, mesurée sans ARN, porte un tiers de
la corrélation.

## 8.60.8 T5 — Runs v6.2 : chaque type ordonne les flux, les résidus aussi

Prédictions calculées AVANT de lire les sorties (depuis T1/T2/T3 du
jour) : D-TOP1 d_pred +0,3900 (C = 0,3314) ; D-TOP2 d_pred +0,3865
(C = 0,3293) ; D-RES d_pred +0,8089 (C_résid CD8A = 0,5770) ; D-LEU
d_pred +0,7552 (C = 0,5456). 8 runs v6.2, mode fast, graine 42, **8/8
exit 0** (lot 11:52:59–13:16:16 UTC 20 nov., unité unique
`v62-deconv-860`, aucune interruption, aucun redémarrage machine
pendant le lot — boot ~11:23 UTC, avant le lot).

| Run | Contrôle → analysés | S_sep réel | S_sep nul | Écart | Prédit | MC réel / nul | Delta réel / nul | w | t0 |
|---|---|---|---|---|---|---|---|---|---|
| D-TOP1 | B.Cells.Naive → 12 imm. bruts | 0,8201 | 0,2333 | **+0,5867** | +0,3900 | 0,4198 / 0,3359 | 3,47 / 2,86 | 26 | 96,92 % |
| D-TOP2 | T.Cells.CD8 → 12 imm. bruts | 0,7766 | 0,2157 | **+0,5609** | +0,3865 | 0,4150 / 0,3330 | 3,42 / 3,42 | 26 | 56,87 % |
| D-RES | CD8A résid. → 11 imm. résid. | 0,9883 | 0,2191 | **+0,7692** | +0,8089 | 0,4413 / 0,3328 | 3,44 / 3,42 | 26 | 1,88 % |
| D-LEU | leuco_méthyl → 12 imm. bruts | 0,9366 | 0,2237 | **+0,7129** | +0,7552 | 0,4327 / 0,3354 | 3,50 / 3,41 | 26 | 67,57 % |

Lecture par critère gelé :
- **D-TOP1 : les B naïfs ordonnent les flux.** Écart +0,5867 — au-dessus
  du seuil H1 (0,45), à 78 % de la moyenne IMMROT (+0,7521), et
  **+0,1967 AU-DESSUS de la prédiction** (+0,3900) : la régression §8.48
  sous-prédit ce contrôle. MC sépare aussi (+0,0839 : 0,4198 contre
  0,3359) ; Delta sépare ici (3,47 contre 2,86) — noté, non utilisé
  pour le verdict (Delta non élucidé, §8.49). L7a sépare en direction
  (up 0,1642 contre down −0,1801) : non utilisé, comme au §8.48/§8.54.
  Le seuil est trouvé TRÈS TARD (t0 = 96,92 %) : la séparation est
  portée par le haut de l'ordonnancement — les tumeurs à forte fraction
  de B naïfs (distribution très asymétrique, médiane 0,0218, max
  0,4022). Critère gelé : D-TOP1 ≥ 0,45 → **soutient H1-type, seul**.
- **D-TOP2 : les T CD8 ordonnent les flux aussi.** Écart +0,5609 —
  au-dessus du seuil H1 (0,45), **+0,1744 au-dessus de la prédiction**
  (+0,3865). MC +0,0820 (0,4150 contre 0,3330) ; Delta quasi égal
  (3,42 contre 3,42, nul devant de 0,004) — noté, non utilisé. Seuil à
  56,87 %. Critère gelé : D-TOP2 ≥ 0,45 → **soutient H1-type, seul**.
  Les deux types porteurs ordonnent les flux — mais ni l'un ni l'autre
  ne retire la cohésion (T2) : ordonner n'est pas porter.
- **D-RES : la séparation survit presque entière.** Écart +0,7692 contre
  +0,9838 pour CD8A brut (**78,2 % conservés, baisse de 21,8 %**) et
  contre +0,8089 prédit (−0,0397 en dessous — la régression §8.48
  prédit bien le résiduel ici). MC +0,1085 (0,4413 contre 0,3328) ;
  Delta quasi égal (3,44 contre 3,42). L7a sépare en direction (up
  0,3958 contre down −0,4282) : non utilisé. Seuil trouvé TRÈS TÔT
  (t0 = 1,88 %). Critère gelé : D-RES ≥ 0,45 → **soutient H0-type,
  seul**. Le contraste avec I-RES (+0,1982, §8.54) est total :
  résidualiser sur le score GLOBAL tue la séparation (20,2 %
  conservés) ; résidualiser sur le meilleur TYPE la laisse à 78,2 %.
- **D-LEU : la fraction leucocytaire (méthylation) ordonne les flux.**
  Écart +0,7129 — au-dessus du seuil (0,45), à 95 % de la moyenne
  IMMROT, contre +0,7552 prédit (−0,0423). MC +0,0973 (0,4327 contre
  0,3354) ; Delta 3,50 contre 3,41. Seuil à 67,57 %. Critère gelé :
  D-LEU ≥ 0,45 → **soutient « infiltration indépendante »**. Cohérent
  avec T2-L (partielle) : la quantité globale d'infiltrat ordonne les
  flux et porte un tiers de la cohésion.

## 8.60.9 Verdict de synthèse

Règle gelée, test par test (bras principal) : T1 = deux types à peine
au-dessus du seuil (0,3314 ; 0,3293), 20 types faibles ; T2 primaire =
PERSISTANCE (0,5044 → 0,4805, chute 4,7 %) ; T2 sensibilités (b) 7,4 %,
(c) 7,0 %, (d) 2,1 % ; T4 = persistance dans les deux moitiés, dont une
bande étroite (moitié basse, ET 7,6 % du global) ; D-TOP1 = +0,5867
(≥ 0,45) ; D-TOP2 = +0,5609 (≥ 0,45) ; D-RES = +0,7692 (≥ 0,45).
**H1-type totale est rejetée** (T2 n'est pas un effondrement, D-RES
n'est pas < 0,30). **H1-type partielle est rejetée** (T2 n'est pas
partielle ; D-TOP1/D-TOP2 ne sont pas entre 0,30 et 0,45 — ils sont
au-dessus). **H0-type stricte est rejetée** (D-TOP1/D-TOP2 ne sont pas
< 0,30). **Verdict gelé : ZONE GRISE.** Aucun consensus exigé entre
les tests : chaque test est rapporté avec son propre critère ; le
verdict suit la règle ci-dessus, pas un vote.

**Ce que cela dit, et ce que cela ne dit pas.** (a) Cela dit qu'aucun
type cellulaire seul — ni les T CD8, ni les B naïfs, ni les macrophages
M0/M1/M2, ni les trois premiers ensemble — ne porte la corrélation
intra-famille immunitaire. (b) Cela dit que les deux types les plus
liés ordonnent réellement les flux (écarts +0,59/+0,56, au-dessus du
minimum IMMROT) : ce ne sont pas des zéros — leurs liens sont
concentrés sur leurs gènes marqueurs (CD19, CD8A/CD8B), une part
mécanique nommée, et le reste de leur signal ne retire pas la cohésion
des autres paires. (c) Cela dit que l'effet de composition identifié
au §8.54 est porté par la quantité TOTALE d'infiltrat : le score
global (ImmuneScore, −64 %) et la fraction leucocytaire globale par
méthylation (−33 %, voie indépendante de l'ARN) bougent la cohésion ;
aucun type seul ne le fait. (d) Cela ne dit pas que les types ne
jouent aucun rôle biologique : une corrélation n'est pas une causalité,
et les fractions CIBERSORT sont relatives (somme = 1 dans le
compartiment immunitaire) — un type ne peut monter sans qu'un autre
baisse. (e) Cela ne dit pas que les deux tiers restants (après la
fraction leucocytaire) ou le cinquième restant (après l'ImmuneScore)
sont « biologiques » au sens d'une régulation : ils peuvent venir
d'une variable latente non testée (sous-type moléculaire, état
d'activation, stroma). (f) La domination IMMROT du §8.48 n'est pas
remise en cause : elle reste expliquée par le couplage, dont la cause
amont est désormais précisée — le couplage est porté par la quantité
globale d'infiltrat, pas par un type dominant.

**Bras L, verdict séparé (critères gelés §7).** T1-L = lien
substantiel (moyenne |r| 0,5456) ; T2-L = PARTIELLE (chute 33,0 %) ;
D-LEU = +0,7129 (≥ 0,45). **La fraction leucocytaire par méthylation
explique environ un tiers de la corrélation intra-famille, par une voie
indépendante de l'ARN.** Comparaison directe des trois mesures
globales : ImmuneScore (ARN, §8.54) −64,0 % ; fraction leucocytaire
(méthylation, §8.60) −33,0 % ; ABSOLUTE (ADN, §8.55) −25,5 % — trois
voies indépendantes, trois chutes partielles ou totales, aucun type
seul.

## 8.60.10 Provenance

- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant les calculs, dans le log du lot, et après l'extraction).
  Mode `fast`, graine 42 (défaut), nul = bloc analysé permuté
  conjointement, graine 42 (default_rng frais par fichier), contrôle
  intact.
- **Protocole.** `PROTOCOL_deconvolution_860.md`, SHA-256
  `471568b1eb83027d4341c7ec5632b5749cf60aa2d06e8a4ddbf2315ffed86d57`,
  gelé le 20 nov. 2026 avant tout téléchargement, tout calcul et tout
  run de ce chantier. Aucun amendement après le gel. (Une coquille du
  protocole est corrigée ici sans toucher aux critères : le §2.3 y cite
  « 21 types » pour `TCGA_IMCell_fraction` d'après la documentation du
  package — le fichier en contient 22, les 22 types LM22, vérifiés en
  machine.)
- **Entrées externes.** (1) imogimap (Korkut lab), dépôt GitHub
  `https://github.com/korkutlab/imogimap`, documentation
  `https://rdrr.io/github/korkutlab/imogimap/src/R/data.R` :
  `data/TCGA_IMCell_fraction.rda`, SHA-256
  `739bfa99495643a926e6f010589044f69969962e2197378bba67e097366370c0`
  (1 053 486 octets ; URL
  `https://raw.githubusercontent.com/korkutlab/imogimap/master/data/TCGA_IMCell_fraction.rda`) ;
  `data/TCGA_Leukocyte_fraction.rda`, SHA-256
  `f576f5f261bbfe4dcc2384c7d90c375e109986f31ad54b544136e5d9a4e68289`
  (114 032 octets ; URL
  `https://raw.githubusercontent.com/korkutlab/imogimap/master/data/TCGA_Leukocyte_fraction.rda`).
  Source primaire des fractions : Thorsson et al. 2018, Immunity
  48:812–830.e14 (PMID 29628290, PMCID PMC5982584, DOI
  10.1016/j.immuni.2018.03.023) ; méthode CIBERSORT : Newman et al.
  2015, Nat Methods 12:453–457 (DOI 10.1038/nmeth.3337). (2) Matrice
  LM22, miroir public GitHub `SiYangming/CIBERSORT-DATA`, `LM22.txt`,
  SHA-256 `8b1b4bb21fffcb10d25ecb6df9aafa3a24b527c35130b9d65e9341a6287cd36c`
  (146 759 octets ; URL
  `https://raw.githubusercontent.com/SiYangming/CIBERSORT-DATA/main/LM22.txt` ;
  accès officiel CIBERSORT = inscription, hors périmètre). (3) Sources
  tentées sans obtention : Europe PMC PMC5982584 `supplementaryFiles`
  (HTTP 200, 296 o, erreur « Article with id PMC5982584 is not open
  access one », fichier `thorsson_europepmc_supp.out`) ; TIMER2.0, Li
  et al. 2020 (DOI 10.1093/nar/gkaa407, `http://timer.cistrome.org/`,
  HTTP 301, serveur interactif, pas de fichier en vrac) ; xCell, Aran
  et al. 2017 (DOI 10.1186/s13059-017-1349-1, PMC5688663, Additional
  file 6 cité, non téléchargé — cf. §8.60.11). (4) Fraction leucocytaire
  par méthylation : Raphael et al. 2017, Cancer Cell 32:185–203.e13
  (PMID 28810144, PMCID PMC5964983, DOI 10.1016/j.ccell.2017.07.007,
  Table S1), via pdacR (Torre-Healy et al. 2023, doi
  10.1038/s42003-023-04461-6), `data/TCGA_PAAD.rds`, SHA-256
  `52020679350d1539d7516f7d38f7bf09e510225eba2f228a4fe874f3c496ea76`
  (provenance §8.55.2).
- **Entrées du projet.** Tarball TCGA-PAAD RSEM, MD5
  `b09569ce3f4721f514bc137bd109ac0a` (vérifié) ; base immunitaire
  `pdac_immune_tcga_fluxes.csv`, SHA-256
  `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e` ;
  axe `immune_kras_order_tcga.csv`, SHA-256
  `31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d` ;
  scores §8.54 `infiltration_854_scores.csv`, SHA-256
  `628732ecbcc30a3281b0df7a5039ec2520a1c5f1a1ae9ce412c4d0d7caf78aa7` ;
  externe §8.55 `purity_855_external.csv`, SHA-256
  `03f34fe07a18ff106e21ce9028ef9ff60d3d95889c3064898442246e486fbd6f` ;
  `purity_855_sampinfo.csv`, SHA-256 complet
  `7a09dde3d374d1afb64f1d1d053193fc884c04d62e63e519fcf4dbf17378b014`
  (le §8.55 cite cette valeur tronquée `7a09dde3…b014` — la valeur
  complète est mesurée ici, le fichier est inchangé) ; écarts §8.44/
  §8.51/§8.54/§8.55 relus en machine (`ssep_844_rotations.csv`,
  `purity_851_runs.json`, `infiltration_854_runs.json`,
  `purity_855_runs.json` ; CD8A : réel 1,2310, nul 0,2472, écart
  +0,9838 ; I-RES +0,1982 ; E-RES +0,6499).
- **Nature des lignes.** Les flux immunitaires sont des mesures
  instrumentales (séquençage ARN, log2(RSEM+1), brutes) ; les fractions
  CIBERSORT sont des estimations publiées depuis l'ARN (déconvolution
  v-SVR sur la signature LM22, 547 gènes) ; la fraction leucocytaire
  par méthylation est une estimation publiée depuis l'ADN (indépendante
  de l'ARN) ; les résidus sont des valeurs calculées (OLS) ; les nuls
  sont des lignes permutées (graine 42) — des échantillons hypothétiques,
  pas des mesures. Aucun mot humain, aucun échantillon hypothétique
  dans les séries réelles. Les 26 lignes CIBERSORT tout-NaN sont des
  valeurs manquantes publiées (déconvolution indisponible), pas des
  zéros — exclues en complete-case, jamais imputées.
- **Sorties et scripts de ce chantier.**
  `extract_deconvolution_860_data.py` (SHA `d5bbc527…e83265`) :
  extraction .rda → CSV en clair (venv
  `data_deconvolution_860/venv860`, parseur `rdata` 1.1.0, pandas).
  `analyze_deconvolution_860.py` (SHA `3af492fb…78fafc`) : porte D,
  jointure, vérifications, T1–T4, bras L.
  `build_deconvolution_860.py` (SHA `f5afd433…9705`) : 8 CSV T5/T5-L
  (résidus vérifiés : moyenne |r| = 0,4805, identique à T2(a)).
  `extract_deconvolution_860.py` (SHA `ab2da5c0…0fed`) : lecture des
  8 runs (SHA des CSV vérifiés, version
  `v6.2.0-L7aL7b-CohenD-short`).
  `data_deconvolution_860/TCGA_IMCell_fraction.csv`,
  `data_deconvolution_860/TCGA_Leukocyte_fraction.csv`,
  `data_deconvolution_860/LM22.txt`,
  `data_deconvolution_860/deconvolution_860_rda_inventory.json`,
  `data_deconvolution_860/deconvolution_860_attempts.log`,
  `data_deconvolution_860/analyze_860_stdout.txt`.
  `deconvolution_860_external.csv` (SHA `438d677a…9cf`, 178 tumeurs :
  sample, 22 fractions, LF imogimap, LF méthylation, ABSOLUTE,
  ImmuneScore),
  `deconvolution_860_results.json` (SHA `1b673cf5…4d`, T1–T4 + bras L),
  `deconvolution_860_results.csv` (SHA `77f22766…67`, T1 par type),
  `deconvolution_860_csv_sha.json` (SHA `a4bba022…9f`, SHA des 8 CSV T5),
  `deconvolution_860_runs.json` (SHA `ce266c39…4dd`) / `.csv`
  (SHA `57f502a1…67`, 8 runs).
  Manifeste `manifest_v62_deconvolution_860.txt`
  (SHA `2120b7cd…80a5b`) ; log `runs_v62_deconvolution_860.log`
  (SHA `19e842b2…c3a`) ; unité systemd `v62-deconv-860`.
- **Ce qui manque :** xCell (Additional file 6, non téléchargé) ; Voie C
  MCP-counter/EPIC non utilisée ; les p de T1 sont brutes, sans
  correction pour tests multiples (264 tests) ; n effectif 151 pour le
  bras principal (sélection non-whitelist, §8.60.2) ; les fractions
  CIBERSORT sont relatives (somme = 1 dans le compartiment immunitaire),
  pas absolues — un type ne peut monter sans qu'un autre baisse.

## 8.60.11 Ce qui manque, ce qui reste ouvert

- **Confirmation indépendante par xCell (64 types, dont fibroblastes /
  stroma).** Les scores xCell précalculés TCGA/TARGET (Aran et al. 2017,
  Additional file 6, PMC5688663) donneraient un second bras par type,
  avec des types stromaux que CIBERSORT ne mesure pas (fibroblastes,
  cellules endothéliales, adipocytes) — la question « stroma ou
  immunité ? » reste ouverte côté stromal (le StromalScore §8.54 est
  global, comme l'ImmuneScore). Chantier jumeau à geler séparément.
- **Fractions ABSOLUES (CIBERSORT absolute mode, EPIC, quanTIseq).**
  Les fractions relatives (somme = 1) confondent composition interne
  et quantité totale : les fractions absolues diraient si c'est la
  quantité absolue de CD8 (et non sa part relative) qui compte — et
  testeraient si M0 est vraiment anti-corrélé ou si c'est un artefact
  de composition.
- **Sous-type moléculaire et état d'activation.** Les deux tiers
  restants après la fraction leucocytaire (et le cinquième après
  l'ImmuneScore) peuvent venir d'une variable latente non testée
  (Bailey / Moffitt / Collisson — colonnes détenues dans le sampInfo,
  non testées ici, autre piste du §8.48.8).
- **Survie par type cellulaire.** Les fractions jointes
  (`deconvolution_860_external.csv`, n = 151) permettent de tester si
  un type prédit la survie — hors protocole gelé, non fait ici.
- **Incident d'exécution.** Aucun : lot unique, unité systemd
  `v62-deconv-860`, 11:52:59–13:16:16 UTC 20 nov., **8/8 exit 0,
  0 échec, 0 relance** (`=== FIN 2026-11-20T13:16:16Z deja_faits=0
  termines=8 echecs=0 ===` ; 8 lignes `EXIT_` à 0 dans le log).
  La machine avait redémarré AVANT le lot (boot ~11:23 UTC, uptime
  32 min à 11:56) ; aucun redémarrage pendant le lot (uptime 1 h 54
  à 13:17).
- **Périmètre.** 8 nouveaux runs v6.2 au maximum (protocole §8 :
  6 principaux + 2 bras L), aucun autre. Aucun nouveau seuil proposé,
  aucun code modifié, aucun push GitHub dans ce chantier (publication
  sur go séparé ; règle permanente « Toujours github et pdf !!! » —
  par le coordinateur).

— Fin de la §8.60. —
