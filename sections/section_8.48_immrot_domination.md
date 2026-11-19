# §8.48 Pourquoi IMMROT domine — la domination est un effet de corrélation, pas une rupture

Date : 19 novembre 2026. Go : Zackary, « Fait tes 3 propositions, je reviens plus tard »,
19 nov. 2026 ~08h16 (3e des 3 propositions ; suite du §8.44, annoncée au §8.44.7).
Protocole gelé avant tout calcul et avant tout run :
`PROTOCOL_immrot_domination.md` (SHA-256 `465b4f54…b9d`).

## Verdict d'abord

**La domination IMMROT est expliquée, quantitativement, par le couplage
contrôle↔flux — la corrélation entre le flux qui ordonne et les flux ordonnés —
et non par une rupture.** Sur les 48 rotations sans doublon, le couplage moyen
C (moyenne des |r de Pearson| entre le contrôle et les 11 flux analysés) prédit
l'écart S_sep réel−nul avec **r = 0,954, ρ de Spearman = 0,945, R² = 0,909**
(régression d_ssep = −0,175 + 1,705·C, p = 1,3×10⁻²⁵, n = 48). La famille
immunitaire domine parce que ses flux sont fortement corrélés entre eux
(|r| moyen 0,556, 62 % des paires au-dessus de 0,5) : ordonner par l'un d'eux,
c'est ordonner presque tous les autres. Les autres familles ne se suivent pas
autant (|r| moyen 0,25 pour V4ROT, 0,27 pour PARPROT, 0,17 pour DEPMAPROT),
et leurs écarts S_sep sont proportionnellement plus petits — exactement dans
le rapport prédit par la régression.

**Le mécanisme est vérifié flux par flux, pas seulement en corrélation globale.**
À la coupure médiane, le |d de Cohen| observé de chaque flux est prédit par sa
seule corrélation r avec le contrôle, par la formule bivariée-normale
|d| ≈ 1,596·|r| / √(1 − 0,637·r²) : sur les 528 paires flux×rotation,
**r = 0,947, biais moyen −0,002, écart moyen absolu 0,11**. Autrement dit : le
|d| que le scan mesure est celui que la corrélation impose ; il n'y a rien
d'autre à expliquer dans max_separation sur ces rotations — pas de marche
supplémentaire, pas de seuil critique, pas de transition.

**Le nul tranche la spécificité.** Le nul du projet permute les lignes du bloc
analysé conjointement : il conserve EXACTEMENT les corrélations entre flux
analysés (cohésion H identique à 10⁻¹⁶ près) et brise seulement l'alignement
contrôle↔flux (couplage nul moyen 0,068, bruit d'échantillonnage seul). Si la
cohésion entre flux suffisait à produire S_sep, le nul montrerait le même S_sep
que le réel. Il ne le montre pas (S_sep nul 0,08–0,43 contre 0,13–1,25 réel),
et S_sep nul ne corrèle ni avec le couplage (r = 0,09) ni avec la cohésion
(r = 0,14). **Ce n'est donc pas « les flux sont corrélés entre eux » qui fait
S_sep — c'est « les flux suivent le contrôle ».** La corrélation interne de la
famille n'agit que par le couplage qu'elle induit avec chaque contrôle pris
dans la famille.

**Ce que cela ne dit pas.** Cela ne dit pas que les flux immunitaires ne sont
pas co-exprimés dans les tumeurs — ils le sont, et les tests directs du §8.32
l'ont confirmé. Cela dit que S_sep, sur les rotations, mesure cette
co-expression à travers le tri par le contrôle, et rien de plus. La domination
IMMROT (12/12, +0,752 en moyenne) n'est ni une rupture ni une piste
thérapeutique : c'est la signature attendue d'une famille de flux
mutuellement corrélés, ordonnés par l'un des leurs. Le §8.44 parlait d'ordre,
pas de rupture ; ce chantier nomme l'ordre : la corrélation.

**Les deux contrôles par runs confirment le mécanisme.** Dose–réponse (H3) :
casser la moitié de l'alignement fait chuter S_sep d'environ moitié — CD8A
1,2310 → 0,5525 à q=0,5 → 0,1725 à q=0,25 ; CD68 0,6322 → 0,3033 à q=0,5 ;
CLDN18 0,8633 → 0,4423 à q=0,5 — monotone, entre le réel et le nul aux trois
q=0,5, comme prédit (0,63 ; 0,37 ; 0,33). Croisés inter-familles (H2) : un
contrôle immunitaire n'ordonne PAS les flux PARP comme il ordonne les siens
(X1 : écart +0,1649, un cinquième de la moyenne IMMROT), et un contrôle PARP
n'ordonne pas les flux immunitaires du tout (X2 : écart −0,0535, nul devant).
Le petit écart X1 est porté par un seul lien, CD8A–ATM (r = +0,498,
|d| = 0,737 à la médiane, contre ≤ 0,27 pour les 11 autres flux PARP) — pas
par un ordonnancement de la famille. **La domination est donc intra-famille :
elle vient de ce que les flux immunitaires se suivent entre eux, et seulement
entre eux.**

## 8.48.1 Question, méthode, définitions gelées

**Question.** Rotations sans doublon (§8.44) : IMMROT 12/12, somme des écarts
+9,0256, moyenne +0,7521, plus petit écart +0,4508 (CD68) ; V4ROT 10/12
(+3,6063, +0,3005) ; DEPMAPROT 6/12 (+0,9036, +0,0753) ; PARPROT 9/12
(+3,6259, +0,3022). Avec doublon (§8.41) : IMMROT +10,8540 sur +25,7324.
Qu'est-ce qui, dans la construction des flux immunitaires, produit cette
domination ? Est-ce un effet de la corrélation interne des flux plutôt
qu'une rupture ?

**Ce que fait le scan (lu dans le code v6.2, jamais modifié).** Mode `fast` :
w_size = 80 (plafonné à n//2, donc 22 à n=45), min_grp = 2. Le scan trie les
lignes par le contrôle (axe de progression MC, monotone en le contrôle),
construit des fenêtres glissantes de w_size points, puis pour chaque seuil
candidat partage les fenêtres en deux groupes et calcule, par flux analysé,
le |d de Cohen| entre les deux groupes ; le score est la MOYENNE sur les flux
des |d| ; max_separation est le maximum de ce score ; S_sep = max_separation ×
stabilité (quasi saturée, 0,9463–0,9986). Conséquence mécanique : si un flux
analysé j est corrélé au contrôle c avec un coefficient r_j, trier par c trie
partiellement j, et le |d| de j au seuil est grand — sans qu'aucune rupture
n'existe. Le nul permute les lignes du bloc analysé conjointement (graine 42,
contrôle intact) : il conserve les corrélations entre flux et brise seulement
l'alignement contrôle↔flux.

**Définitions gelées.** Pour une rotation de contrôle c (base à 12 flux) :
- Couplage C_c = moyenne sur les 11 flux j≠c de |r_Pearson(c, j)|.
  Robustesse : même quantité en Spearman, C_c^S.
- Cohésion H_c = moyenne sur les 55 paires (j,k), j<k, j,k≠c, de |r_Pearson(j, k)|.
- Mêmes quantités sur le CSV nul dédoublonné : C_c^nul, H_c^nul.
- D_full (réplication analytique transparente, sans l'axe MC ni les fenêtres) :
  sur un CSV dédoublonné, lignes triées par le contrôle, pour chaque coupure
  k = 20..n−20, |d de Cohen| par flux entre les k premières et les n−k
  dernières lignes, moyenne sur les flux ; D_full = maximum sur k.
  Variante à coupure fixe : médiane (k = n//2), D_med.
- Prédiction bivariée-normale par flux, à la médiane :
  d_j^pred = 1,596·r_j / √(1 − 0,637·r_j²), r_j = Pearson(c, j).

**Critères gelés (avant les calculs).** H1 soutenue si r(C_c, d_ssep sans doublon)
> 0,7 ET ρ_Spearman > 0,7 ; rejetée si r < 0,5 ; entre 0,5 et 0,7 : partielle.
Contrôles négatifs : r(H_c, d_ssep) et r(C_c, S_sep nul), attendus |r| < 0,3.
D_full : mécanisme confirmé si r(D_full, maxsep) > 0,95 ET écart moyen < 0,10.
Par flux à la médiane : r(|d_pred|, |d_obs|) > 0,8.

**Hypothèses.** H1 (principale) : l'écart S_sep est prédit par le couplage
contrôle↔flux. H0 (négative) : la cohésion entre flux analysés ne prédit pas
l'écart. H2 : un flux immunitaire comme contrôle ordonne-t-il aussi des flux
non immunitaires ? H3 (dose–réponse) : dégrader l'alignement contrôle↔flux
fait chuter S_sep progressivement.

## 8.48.2 Corrélations internes par famille — l'immunitaire est deux fois plus cohésif

Matrices de corrélation Pearson + Spearman des 12 flux de chaque base
(66 paires hors diagonale). Aucune valeur manquante dans les 4 bases.

| Famille | n | Pearson : moyenne \|r\| | médiane \|r\| | fraction \|r\|>0,5 | Spearman : moyenne \|r\| | Paire la plus forte | Paire la plus faible |
|---|---|---|---|---|---|---|---|
| V4ROT (TCGA v4, ARN tumeurs) | 178 | 0,2481 | 0,1449 | 0,197 (13/66) | 0,2309 | CLDN18–MUC17 +0,714 | PGC–KRT20 +0,006 |
| DEPMAPROT (CRISPR DepMap) | 45 | 0,1732 | 0,1293 | 0,030 (2/66) | 0,1764 | RAB10–RAB6A +0,528 | CCND1–RAB6A +0,002 |
| IMMROT (immunitaire TCGA) | 178 | **0,5563** | **0,5677** | **0,621 (41/66)** | **0,5403** | CD8A–CD8B +0,843 | CD68–CD19 +0,177 |
| PARPROT (réparation ADN TCGA) | 178 | 0,2715 | 0,2127 | 0,182 (12/66) | 0,2690 | RAD51–POLQ +0,823 | CHEK1–XRCC1 +0,000 |

Lecture : la famille immunitaire est environ deux fois plus corrélée
intérieurement que V4ROT et PARPROT, trois fois plus que DEPMAPROT. Sa paire
la plus FAIBLE (CD68–CD19, 0,177) est au niveau de la MOYENNE des autres
familles. 41 des 66 paires immunitaires dépassent 0,5 ; aucune autre famille
n'en a plus de 13. La paire la plus forte de PARPROT (RAD51–POLQ, 0,823) montre
que PARPROT contient, elle aussi, un couple très corrélé — mais un seul couple
ne fait pas une famille : sa moyenne reste à 0,27, et ses écarts S_sep restent
à +0,30 en moyenne. C'est la moyenne du couplage qui compte, pas le maximum
d'une paire — et c'est exactement ce que le test principal mesure.

## 8.48.3 Le couplage prédit S_sep — test principal (48 rotations, sans doublon)

| Test (n = 48) | Pearson r | p | Spearman ρ | p |
|---|---|---|---|---|
| C_c (Pearson) vs d_ssep sans doublon | **0,9535** | 1,3×10⁻²⁵ | **0,9447** | 6,5×10⁻²⁴ |
| C_c (Spearman) vs d_ssep sans doublon | 0,9582 | 1,2×10⁻²⁶ | 0,9528 | 1,9×10⁻²⁵ |
| C_c vs d_ssep AVEC doublon (§8.41) | 0,9337 | 3,7×10⁻²² | 0,9069 | 1,0×10⁻¹⁸ |
| H_c (cohésion) vs d_ssep sans doublon | 0,7035 | 2,5×10⁻⁸ | 0,4731 | 6,8×10⁻⁴ |
| C_c vs S_sep NUL sans doublon | 0,0920 | 0,53 | −0,0661 | 0,66 |
| H_c vs S_sep NUL sans doublon | 0,1379 | 0,35 | −0,0045 | 0,98 |
| C_c vs H_c (global) | 0,7577 | 4,5×10⁻¹⁰ | 0,5022 | 2,8×10⁻⁴ |

Régression (moindres carrés, 48 points) : **d_ssep = −0,1748 + 1,7046·C_c**,
R² = 0,909, p = 1,3×10⁻²⁵, erreur-type de la pente 0,079. Appliquée aux
moyennes par famille, elle prédit : IMMROT +0,773 (observé +0,752), V4ROT
+0,248 (observé +0,301), PARPROT +0,288 (observé +0,302), DEPMAPROT +0,120
(observé +0,075). Les quatre familles tombent sur la même droite, à ±0,05
près : **il n'y a pas d'effet « famille immunitaire » au-delà du couplage.**
Un contrôle immunitaire ne domine pas parce qu'il est immunitaire — il domine
parce que son couplage vaut 0,56 en moyenne, contre 0,17 à 0,27 ailleurs.

Par famille (n = 12, descriptif seulement) : r(C_c, d_ssep) = 0,968 (V4ROT),
0,834 (DEPMAPROT), 0,832 (IMMROT), 0,872 (PARPROT). Le couplage prédit
l'écart DANS chaque famille, pas seulement entre familles : même dans
DEPMAPROT, la plus faible, les contrôles les plus couplés (CRKL 0,270 ;
EFR3A 0,221) sont ceux qui séparent le plus (+0,181 ; +0,224), et les moins
couplés (MYC 0,074 ; CFLAR 0,111) sont ceux qui échouent (−0,138 ; +0,018).
À l'inverse, les rotations qui échouent sont toutes des rotations à couplage
faible : les six écarts négatifs ont tous C_c < 0,13 — CR2 0,043 (−0,029),
GSTM1 0,078 (−0,134), MYC 0,074 (−0,138), ACO2 0,120 (−0,021),
UROD 0,102 (−0,028), CCND1 0,125 (−0,114). Aucune rotation à C_c > 0,40 n'échoue.

### La cohésion H n'est pas un contrôle indépendant — identité algébrique

Le contrôle négatif H, tel que gelé, doit être lu avec une identité que le
chantier a établie en le calculant : DANS une famille, H_c est une fonction
affine DÉCROISSANTE exacte de C_c. Soit S la somme des |r| sur les 66 paires
de la famille. Les 11 paires qui touchent c somment à 11·C_c ; les 55 autres
somment à S − 11·C_c ; donc **H_c = S/55 − C_c/5, exactement**. Vérifié
numériquement : r(C_c, H_c) = −1,000000 dans chaque famille (n = 12), et
r(H_c, d_ssep) = −r(C_c, d_ssep) exactement dans chaque famille (−0,968 ;
−0,834 ; −0,832 ; −0,872). Globalement, r(H_c, d_ssep) = 0,7035 (Pearson)
vient de ce que C et H suivent tous deux la moyenne familiale (r(C, H) = 0,76
globalement, alors qu'il vaut −1 dans chaque famille — structure de
Simpson). **Le critère gelé « si r(H, d_ssep) > 0,7, H1 n'est pas
spécifique » ne peut donc pas être appliqué tel quel : H n'est pas une
variable indépendante, c'est C retourné.** La spécificité ne se joue pas là —
elle se joue sur le nul (paragraphe suivant), qui est le vrai contrôle
négatif : même cohésion H, couplage brisé, S_sep effondré.

### Le nul : même cohésion, couplage brisé, S_sep effondré

Sanité du nul (48 paires) : couplage nul C_c^nul moyen **0,068** (écart-type
0,028, maximum 0,146) — le bruit d'échantillonnage seul, comme attendu d'une
permutation ; cohésion nulle H_c^nul − H_c moyen **−3,3×10⁻¹⁷** (écart-type
2,1×10⁻¹⁶) — la permutation conjointe conserve les corrélations entre flux
exactement, à l'erreur d'arrondi près. Et pourtant S_sep nul reste bas
(0,08–0,43) et ne corrèle ni avec C_c (r = 0,09) ni avec H_c (r = 0,14).
**La cohésion entre flux, seule, ne produit pas S_sep : le nul en est la
preuve contrôlée.** Il faut l'alignement avec le contrôle — c'est-à-dire le
couplage — pour que le tri produise des |d|.

### Avec doublon : même loi, décalée

Le couplage prédit aussi les écarts AVEC doublon (r = 0,934, ρ = 0,907) :
la domination IMMROT ne dépend pas du doublon. La perte d'écart
(avec − sans, moyenne +0,1786) corrèle NÉGATIVEMENT avec le couplage
(r = −0,474, p = 0,0007) : le doublon gonfle surtout les rotations à FAIBLE
couplage — là où le contrôle seul portait la séparation (GSTM1 +0,356 ;
CFLAR +0,293 ; CCND1 +0,274), il ajoute une colonne parfaitement triée qui
vaut 1/12 de la moyenne ; là où le couplage est fort, il n'ajoute presque
rien (CRKL +0,025 ; GZMB +0,103 ; CD8A +0,104). Cohérent avec le §8.44 :
le doublon assiste à la marge, il ne crée pas la domination.

## 8.48.4 Table complète des 48 rotations — couplage, cohésion, écarts S_sep

C_c et H_c calculés sur les bases à 12 flux (la corrélation ne dépend pas de
l'ordre des lignes : C_c recalculé sur les CSV dédoublonnés donne les mêmes
valeurs à 1,8×10⁻¹⁵ près, maximum sur les 48 paires). Écarts S_sep relus dans
`ssep_844_rotations.csv` (sans doublon) et `ssep_841_rotations.csv` (avec
doublon) — aucune valeur recopiée à la main.

| Famille | Contrôle | C couplage | H cohésion | d S_sep sans | d S_sep avec |
|---|---|---|---|---|---|
| DEPMAPROT | ACO2 | 0.1197 | 0.1839 | -0.0208 | +0.0829 |
| DEPMAPROT | CCND1 | 0.1252 | 0.1828 | -0.1143 | +0.1600 |
| DEPMAPROT | CFLAR | 0.1111 | 0.1856 | +0.0183 | +0.3115 |
| DEPMAPROT | CRKL | 0.2699 | 0.1539 | +0.1812 | +0.2066 |
| DEPMAPROT | DOCK5 | 0.2156 | 0.1647 | +0.2596 | +0.4179 |
| DEPMAPROT | EFR3A | 0.2213 | 0.1636 | +0.2239 | +0.3880 |
| DEPMAPROT | MYC | 0.0736 | 0.1931 | -0.1380 | +0.0969 |
| DEPMAPROT | MYH9 | 0.1907 | 0.1697 | +0.0899 | +0.2556 |
| DEPMAPROT | RAB10 | 0.2405 | 0.1598 | +0.0604 | +0.2075 |
| DEPMAPROT | RAB6A | 0.2188 | 0.1641 | +0.2378 | +0.4330 |
| DEPMAPROT | SCAP | 0.1905 | 0.1698 | +0.1338 | +0.3445 |
| DEPMAPROT | UROD | 0.1017 | 0.1875 | -0.0282 | +0.1576 |
| IMMROT | CD163 | 0.5721 | 0.5532 | +0.7748 | +0.9013 |
| IMMROT | CD19 | 0.4723 | 0.5731 | +0.4509 | +0.6685 |
| IMMROT | CD274 | 0.4107 | 0.5855 | +0.5006 | +0.6551 |
| IMMROT | CD4 | 0.6516 | 0.5373 | +0.7372 | +0.8830 |
| IMMROT | CD68 | 0.4261 | 0.5824 | +0.4508 | +0.5942 |
| IMMROT | CD8A | 0.6514 | 0.5373 | +0.9838 | +1.0877 |
| IMMROT | CD8B | 0.5859 | 0.5504 | +0.8398 | +1.0029 |
| IMMROT | CTLA4 | 0.6527 | 0.5371 | +0.8986 | +1.1227 |
| IMMROT | FOXP3 | 0.6241 | 0.5428 | +0.8428 | +0.9852 |
| IMMROT | GZMB | 0.5724 | 0.5531 | +0.9053 | +1.0083 |
| IMMROT | IFNG | 0.4370 | 0.5802 | +0.7242 | +0.8634 |
| IMMROT | PDCD1 | 0.6197 | 0.5436 | +0.9167 | +1.0818 |
| PARPROT | ATM | 0.1618 | 0.2934 | +0.1676 | +0.3345 |
| PARPROT | ATR | 0.2702 | 0.2718 | +0.2384 | +0.3890 |
| PARPROT | BRCA1 | 0.2560 | 0.2746 | +0.5241 | +0.6859 |
| PARPROT | BRCA2 | 0.3901 | 0.2478 | +0.3978 | +0.5530 |
| PARPROT | CHEK1 | 0.2907 | 0.2676 | +0.3763 | +0.5623 |
| PARPROT | CHEK2 | 0.3288 | 0.2600 | +0.2523 | +0.4000 |
| PARPROT | FANCD2 | 0.3713 | 0.2515 | +0.4339 | +0.5871 |
| PARPROT | PARP1 | 0.1396 | 0.2979 | +0.0169 | +0.1968 |
| PARPROT | PARP2 | 0.1196 | 0.3019 | +0.0293 | +0.2253 |
| PARPROT | POLQ | 0.4114 | 0.2435 | +0.6093 | +0.7595 |
| PARPROT | RAD51 | 0.4039 | 0.2450 | +0.5242 | +0.6652 |
| PARPROT | XRCC1 | 0.1144 | 0.3029 | +0.0558 | +0.2545 |
| V4ROT | CEACAM5 | 0.3678 | 0.2241 | +0.5104 | +0.6485 |
| V4ROT | CLCA1 | 0.2712 | 0.2435 | +0.3048 | +0.5198 |
| V4ROT | CLDN18 | 0.3729 | 0.2231 | +0.6761 | +0.8783 |
| V4ROT | CR2 | 0.0434 | 0.2890 | -0.0291 | +0.2441 |
| V4ROT | DPCR1 | 0.2859 | 0.2405 | +0.4166 | +0.6372 |
| V4ROT | GSTM1 | 0.0779 | 0.2821 | -0.1342 | +0.2215 |
| V4ROT | KRT20 | 0.2363 | 0.2504 | +0.2558 | +0.4834 |
| V4ROT | MUC16 | 0.1117 | 0.2754 | +0.0712 | +0.2996 |
| V4ROT | MUC17 | 0.3704 | 0.2236 | +0.5584 | +0.7423 |
| V4ROT | MUC2 | 0.2308 | 0.2515 | +0.2008 | +0.4152 |
| V4ROT | PGC | 0.2319 | 0.2513 | +0.2349 | +0.4113 |
| V4ROT | REG4 | 0.3768 | 0.2223 | +0.5405 | +0.7022 |

## 8.48.5 Réplication analytique : le |d| vient de la corrélation, flux par flux

**À la médiane (528 paires flux×rotation, réel sans doublon).** Pour chaque
flux j, r_j = Pearson(contrôle, j) ; |d| observé = |d de Cohen| entre les deux
moitiés (triées par le contrôle) ; |d| prédit = 1,596·|r_j| / √(1 − 0,637·r_j²)
(formule bivariée-normale, coupure à la médiane).
- |r_j| vs |d| observé : **r = 0,938**, p = 6,1×10⁻²⁴⁴.
- |d| prédit vs |d| observé : **r = 0,947**, p = 1,8×10⁻²⁶²,
  écart moyen absolu 0,11, **biais moyen −0,002** (la formule ne surestime ni
  ne sous-estime en moyenne).
- Contrôle de la convention de signe : d_obs signé (bas−haut) vs −d_pred signé :
  r = 0,955. [Correction consignée : la première version du script comparait
  d_obs signé à d_pred signé, conventions opposées, et donnait r = −0,95 ; la
  comparaison correcte porte sur |d|, puisque le pipeline ne lit que |d|. Les
  valeurs signées restent dans `immrot_848_per_flux_mediane.csv`.]

Exemples. Rotation CD8A (plus fort écart IMMROT, +0,984) : les 11 flux ont
r = 0,36–0,84 avec CD8A ; |d| observés à la médiane 0,59–2,13 (CD8B : r = 0,843,
|d| = 2,13, prédit 1,82 ; CD4 : r = 0,731, |d| = 1,29, prédit 1,44 ; PDCD1 :
r = 0,792, |d| = 1,66, prédit 1,63). Rotation GSTM1 (échoue, −0,134) : les 11
flux ont r ≤ 0,15 avec GSTM1 ; |d| observés ≤ 0,23, prédits ≤ 0,24. Le contrôle
qui n'ordonne rien ne sépare rien — et la formule le dit avant le run.

**D_full (coupure franche, maximum sur toutes les coupures, 96 runs).**
D_full vs max_separation pipeline : **r = 0,970** sur les 96 runs (réels
r = 0,966, nuls r = 0,524 — les nuls sont du bruit, leur corrélation est
faible comme attendu), mais D_full DÉPASSE maxsep de 0,19 en moyenne sur les
réels (écart moyen absolu 0,197 ; 0,132 sur les 96). Le critère gelé (r > 0,95
ET écart moyen < 0,10) n'est donc rempli que sur la corrélation, pas sur le
niveau : D_full est une borne haute, pas une réplique. La raison est mesurée
au paragraphe suivant : le scan du pipeline est fenêtré et optimisé, pas une
coupure franche.

**Pourquoi D_full dépasse maxsep — le scan optimisé (lecture des JSON).**
Le max_separation rapporté n'est pas celui du scan par défaut (w_size = 80) :
c'est le meilleur des 12 itérations d'optimisation Monte Carlo (mode fast,
`optimization_iterations` = 12), qui échantillonnent w_size, min_grp et
n_candidates. Sur les 96 runs v6.2 dédoublonnés (88 du §8.44 + 8 du §8.41,
dont 2 nuls à permutation identique), le w_size retenu est : 30 (57 runs),
10 (16), 19 (9), 27 (8), 53 (3), 43 (2), 89 (1) — le w_size par défaut (80)
n'est jamais retenu.
À n=45 (DEPMAPROT) : 10 (16 runs) et 19 (9). Une fenêtre plus petite recouvre
moins les deux groupes autour du seuil, donc atténue moins le |d| qu'une
fenêtre de 80 — d'où un maxsep entre D_full (coupure franche, borne haute,
+0,19) et la réplication fenêtrée à w = 80 (voir diagnostic ci-dessous, borne
basse, −0,23). Le mécanisme reste le même : le score est une moyenne de |d|
induits par le tri ; seuls le lissage et le choix de fenêtre déplacent son
niveau, pas son ordre.

**Diagnostic post-hoc (hors protocole gelé, hors verdict).** Réplication
fenêtrée D_win — même algorithme que `_scan_critical_threshold_fast`
(w_size = 80, min_grp = 2, candidats linspace(0,100,n_use), n_use = milieu
des bornes de loupe), sauf l'axe de progression remplacé par le percentile de
rang du contrôle (l'axe MC du pipeline est monotone en le rang du contrôle).
D_win vs maxsep : r = 0,974 sur les 96 runs, mais D_win SOUS-estime maxsep de
0,23 en moyenne sur les réels (0,17 sur les 96). La fenêtre de 80 lisse trop
par rapport au w_size optimisé (le plus souvent 30) ; le percentile de rang
n'est pas l'axe MC. Ce diagnostic n'est pas utilisé pour le verdict : il
borne le mécanisme par en bas, comme D_full le borne par en haut, et il montre
que la réplication exacte du niveau demanderait l'axe MC et les paramètres
optimisés — hors périmètre de ce chantier.

## 8.48.6 Prédictions gelées avant les runs, et runs de contrôle (H2, H3)

Les prédictions ci-dessous sont calculées À PARTIR de la régression du §8.48.3
(d = −0,175 + 1,705·C) et des couplages mesurés sur les CSV — AVANT de lire
les sorties des 8 nouveaux runs. Elles ne sont pas ajustées après coup.

**Porte G (jointure inter-familles) : OUVERTE.** Tarball TCGA-PAAD RSEM,
MD5 `b09569ce…ac0a` conforme ; 178 tumeurs primaires (code 01) ; 0 NaN sur
KRAS + 12 gènes immunitaires et sur KRAS + 12 gènes PARP ; ordre KRAS brut
recalculé égal EXACTEMENT à `immune_kras_order_tcga.csv` (178/178 échantillons,
KRAS log2 min 8,5697, médiane 10,2816, max 11,7273). La ligne i est donc le même
patient dans les bases IMMROT et PARPROT (toutes deux ordonnées par KRAS brut
croissant). La base V4ROT est exclue de tout croisement : ses lignes sont
ordonnées par KRAS RÉSIDUEL (corrigé pureté), la jointure par index y serait
fausse.

**Croisés inter-familles (H2) — couplages mesurés, prédictions :**
- X1 : contrôle CD8A (immunitaire) sur les 12 flux PARP. Couplage
  C_X1 = 0,1397 (Spearman 0,1588). Seule corrélation notable : CD8A–ATM
  +0,498 ; les 11 autres sont entre −0,14 et +0,22. Prédiction :
  d_X1 = −0,175 + 1,705×0,140 = **+0,063** — sous le plancher 0,07, ne passe
  pas la règle (A).
- X2 : contrôle POLQ (PARP) sur les 12 flux immunitaires. Couplage
  C_X2 = 0,1306 (Spearman 0,0695). Plus fortes : POLQ–CD68 +0,314,
  POLQ–GZMB +0,223. Prédiction : d_X2 = **+0,048** — ne passe pas la règle (A).
- Critère gelé : si l'un des deux atteint ≥ 0,45 (minimum IMMROT sans doublon),
  H2 est soutenue (le contrôle ordonne hors famille) et H1 doit être
  reformulée ; sous 0,30, la domination est intra-famille.

**Dose–réponse (H3) — permutation partielle, prédictions :** bloc analysé
permuté conjointement, fraction q de lignes fixées (default_rng(1234) frais
par CSV ; l'ensemble fixé à q=0,25 est un sous-ensemble de celui à q=0,5,
même tirage). Couplage effectif ≈ q·C, donc d(q) ≈ −0,175 + 1,705·q·C.
- CD8A (C = 0,6514 ; réel S_sep 1,2310, nul 0,2472) : q=0,5 → S_sep ≈ 0,63 ;
  q=0,25 → S_sep ≈ 0,35.
- CD68 (C = 0,4261 ; réel 0,6322, nul 0,1814) : q=0,5 → S_sep ≈ 0,37.
- CLDN18 (C = 0,3729 ; réel sans doublon 0,8633, nul 0,1872) : q=0,5 →
  S_sep ≈ 0,33.
- Critère gelé : H3 soutenue si S_sep(q=0,5) tombe entre le réel et le nul
  pour les 3 rotations ET S_sep CD8A(q=0,25) < S_sep CD8A(q=0,5).

### Résultats des 8 runs v6.2 (21h41–22h51 UTC, 8/8 exit 0)

Extraction `extract_immrot_848.py` (SHA `98765df1…f48eb0`), version
`v6.2.0-L7aL7b-CohenD-short` sur les 8 runs, SHA des 8 CSV vérifiés (8/8
conformes). Références réels/nuls : §8.44 (`ssep_844_rotations.csv`).

**Dose–réponse (H3) — S_sep :**

| Rotation | Réel (q=1) | q=0,5 (observé / prédit) | q=0,25 (observé / prédit) | Nul (q=0) |
|---|---|---|---|---|
| CD8A (IMMROT) | 1,2310 | **0,5525** / 0,63 | **0,1725** / 0,35 | 0,2472 |
| CD68 (IMMROT) | 0,6322 | **0,3033** / 0,37 | — | 0,1814 |
| CLDN18 (V4ROT) | 0,8633 | **0,4423** / 0,33 | — | 0,1872 |

Critère gelé : H3 soutenue si S_sep(q=0,5) tombe entre le réel et le nul pour
les 3 rotations ET S_sep CD8A(q=0,25) < S_sep CD8A(q=0,5). **Les deux
conditions sont remplies : H3 est SOUTENUE.** La décroissance est monotone
(1,2310 → 0,5525 → 0,1725 pour CD8A) et les trois q=0,5 sont entre le réel et
le nul, à ±0,11 de la prédiction de la régression (0,55 contre 0,63 ; 0,30
contre 0,37 ; 0,44 contre 0,33). Deux réserves honnêtes : (a) à q=0,25,
S_sep (0,1725) tombe SOUS le nul §8.44 (0,2472) — il est dans la bande de bruit
du nul (les nuls varient de 0,08 à 0,43 sur les 48 paires ; un seul tirage de
nul ne définit pas un plancher) et la régression surestime ce point (0,35
prédit contre 0,17 observé) : le modèle linéaire ne tient plus aux faibles
couplages, où l'écart s'annule dans le bruit ; (b) MC ne suit pas la dose
(0,3834 ; 0,3275 ; 0,5381 ; 0,3668) — cohérent avec le §8.44 (MC aveugle sur
les rotations), il n'est pas utilisé ici.

**Croisés inter-familles (H2) — S_sep réel / nul (écart) :**

| Croisement | S_sep réel | S_sep nul | Écart | Prédit | Verdict gelé |
|---|---|---|---|---|---|
| X1 : CD8A (immunitaire) → 12 flux PARP | 0,3310 | 0,1661 | **+0,1649** | +0,06 | < 0,30 : intra-famille |
| X2 : POLQ (PARP) → 12 flux immunitaires | 0,2144 | 0,2679 | **−0,0535** | +0,05 | < 0,30 : intra-famille |

Critère gelé : H2 soutenue si l'un des deux atteint ≥ 0,45 ; intra-famille
si les deux restent sous 0,30. **Les deux restent sous 0,30 (et X2 est
négatif) : H2 est REJETÉE.** Aucun croisement ne reproduit la domination
IMMROT (moyenne +0,752, minimum +0,451) : X1 en fait le cinquième, X2 rien.
X1 passe la règle (A) (> 0,07) — il faut le dire — mais à +0,165, c'est une
séparation faible, pas une domination, et elle est portée par UN seul lien :
à la médiane, ATM a |d| = 0,737 (r = +0,498 avec CD8A, prédit 0,865) quand les
11 autres flux PARP sont à |d| ≤ 0,27 (moyenne |d| 0,190 ; sans ATM, 0,140).
Retirer ATM de la moyenne, c'est retirer un tiers du signal X1. X2, lui,
n'a même pas ce lien : sa plus forte corrélation croisée (POLQ–CD68, +0,314)
donne |d| = 0,027 à la médiane (prédit 0,518) — la corrélation y est portée
par des extrêmes, pas par un décalage de médiane, et la formule
bivariée-normale y échoue : c'est la plus grosse erreur de prédiction
par-flux de ce chantier, consignée comme telle. MC sur X1/X2 (0,35 ; 0,33 ;
0,33 ; 0,53) ne sépare rien non plus ; Delta (4,26 ; 4,23 ; 3,10 ; 3,22)
disperse comme au §8.44.

**Bilan H1/H2/H3.** H1 soutenue (r = 0,954, R² = 0,909, formule par flux
r = 0,947, biais −0,002). H3 soutenue (dose monotone, q=0,5 intermédiaires).
H2 rejetée (aucun ordonnancement hors famille au niveau IMMROT). Les trois
lignes convergent : **S_sep mesure le couplage contrôle↔flux ; la domination
IMMROT est la mesure de la co-expression immunitaire, ordonnée par l'un des
siens, et rien d'autre.**


## 8.48.7 Provenance

- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` (vérifié
  avant les calculs et dans le log du lot). Mode `fast`, graine 42 (défaut),
  nul = lignes permutées, graine 42, contrôle intact. Pipeline v6.1 (CLDN18
  seul, run préexistant §8.32) SHA `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`.
- **Protocole.** `PROTOCOL_immrot_domination.md`, SHA-256
  `465b4f54bc9f3421557914e6d04319170a98e0fe3158189c899125d3d77d4b9d`,
  gelé le 19 nov. 2026 avant tout calcul et avant tout run de ce chantier.
- **Entrées.** 4 bases, SHA-256 vérifiés un par un avant les calculs (4/4
  conformes à PROVENANCE_rotations_v61.md) : TCGA v4 `e7a2adaba5a0…13a0b0`,
  DepMap `7d605fefb412…98e37f8`, immunitaire TCGA `66dbb672ea2a…bbd2e`,
  PARP TCGA `c9549b68280b…c4309`. Écarts S_sep relus en machine dans
  `ssep_844_rotations.csv` (SHA `d1abc0aba2e4…f999`, 48 paires) et
  `ssep_841_rotations.csv` (SHA `1d3b28a4ff…58ab`, 48 paires).
  Sources : TCGA-PAAD ARN Broad GDAC Firehose 2016-01-28 (RSEM, tarball MD5
  `b09569ce3f4721f514bc137bd109ac0a`) ; DepMap CRISPR 24Q2 (figshare Corsello
  et al.) ; GEO GSE62452/GSE71729 ; ICGC PACA-AU. Voir PROVENANCE_tcga_v4.md,
  PROVENANCE_depmap.md, PROVENANCE_immune_v6.md, PROVENANCE_parp_v6.md,
  PROVENANCE_rotations_v61.md, PROVENANCE_rotations_dedup_844.md.
- **Nature des lignes.** Les CSV sont des résidus d'expression génique ou de
  dépendance CRISPR (mesures instrumentales — séquençage ARN, criblage CRISPR
  — transformées : correction de pureté, résidus) ordonnés par un flux-contrôle
  croissant ; les nuls et les CSV partiels sont des lignes permutées
  (graines 42 et 1234) — des échantillons hypothétiques, pas des mesures.
  Aucun mot humain, aucun échantillon hypothétique dans les séries réelles.
- **Sorties et scripts de ce chantier.**
  `analyze_immrot_domination.py` (SHA `bd2ba083…49ee9`) : corrélations,
  D_full, D_win (diagnostic), per-flux, porte G.
  `build_immrot_848.py` (SHA `55f003b8…6ca99`) : 8 CSV de contrôle.
  `extract_immrot_848.py` (SHA `98765df1abe1…f48eb0`) : lecture des 8 runs.
  `immrot_848_correlations.csv/.json` (table des 48 rotations : C, H, écarts),
  `immrot_848_dfull.csv` (D_full sur les 96 runs dédoublonnés),
  `immrot_848_dwin_diagnostic.csv` (diagnostic fenêtré),
  `immrot_848_per_flux_mediane.csv` (528 paires flux×rotation, à la médiane),
  `immrot_848_gate.json` (porte G : OUVERTE),
  `immrot_848_bestconfig_wsize.json` (w_size retenu sur les 96 runs §8.44),
  `immrot_848_csv_sha.json` (SHA des 8 CSV de contrôle),
  `immrot_848_results.csv/.json` (8 runs, 8/8 exit 0 ; CSV SHA
  `2a90e077…6722c3`, JSON SHA `74bcf433…e097`).
  Manifeste `manifest_v62_immrot_848.txt` ; log `runs_v62_immrot_848.log` ;
  surveillance `watch_v62_immrot_848.sh` ; unités systemd `v62-immrot-848`
  puis `v62-immrot-848b`.
- **Ce qui manque :** les valeurs exactes de S_sep par flux analysé (hors
  contrôle) n'ont pas été extraites — S_sep est global, pas par flux ; la
  lecture par flux du §8.32 reste la référence, doublon exclu ; le D_win
  diagnostique ne réplique pas l'axe MC (percentile de rang à la place) et
  sous-estime maxsep de 0,23 — la réplication exacte du niveau demanderait
  l'axe MC et les paramètres optimisés ; les corrélations DEPMAPROT sont
  estimées sur n=45 (incertitude plus grande que sur n=178) ; la cause
  biologique de la corrélation immunitaire elle-même (infiltration, pureté,
  sous-types) est hors périmètre — ce chantier mesure si cette corrélation
  suffit à produire la domination S_sep, pas pourquoi elle existe.

## 8.48.8 Ce qui manque, ce qui reste ouvert

- **La domination IMMROT est expliquée, pas relativisée.** Le 12/12 et le
  +0,752 restent vrais comme mesures ; ils changent de sens : ce sont des
  mesures de co-expression ordonnée, pas des ruptures. Aucun des 12 contrôles
  immunitaires ne devient une cible, et aucun flux immunitaire ne devient un
  biomarqueur sur cette seule base.
- **MC reste aveugle sur les rotations (12/48 en positif sous (A) au §8.44).**
  Ce chantier ne touche pas au composite MC : il explique max_separation /
  S_sep, pas MC. L'écart entre MC et max_separation sur les mêmes runs reste
  le fait le plus net après la domination elle-même — le composite cache ce
  que le pic voit. Revoir la composition du score MC reste hors protocole,
  non lancé.
- **Le niveau exact de maxsep n'est pas répliqué.** D_full (coupure franche)
  le dépasse de 0,19, D_win (fenêtres w=80, percentile de rang) est en
  dessous de 0,23 : le scan optimisé (w_size le plus souvent 30, 12
  itérations) se place entre les deux. L'ordre est expliqué, le niveau exact
  ne l'est pas encore — une réplication avec l'axe MC exact et les paramètres
  optimisés le trancherait, hors périmètre ici.
- **La cause biologique de la corrélation immunitaire reste ouverte.**
  Infiltration lymphocytaire, pureté tumorale, sous-type moléculaire :
  trois variables latentes plausibles, aucune testée ici. Un contrôle
  supplémentaire serait d'ordonner par la pureté ou par un score
  d'infiltration et de mesurer si le couplage immunitaire s'effondre —
  hors protocole, non lancé.
- **Incident d'exécution.** La machine a redémarré pendant le lot
  (~21h41 UTC, `uptime` : 1 min à 21h42) ; la première unité
  `v62-immrot-848` est morte avec elle (aucune entrée dans `journalctl`,
  cause non établie — comme aux §8.41/§8.44 ; unité `--collect`, donc
  introuvable après sa mort). Aucune sortie complète n'était perdue (0/8) ;
  la relance reprenable `v62-immrot-848b` a repris au 1er run à 21h42:43 UTC.
  Bilan final : **8/8 exit 0**, 0 échec, lot 21h41:12–22h51:02 UTC
  (`=== FIN 2026-11-19T22:51:02Z deja_faits=0 termines=8 echecs=0` ;
  surveillance arrêtée d'elle-même à 8/8, tour 1/12). Le 1er run a duré
  ~16 min (3 autres lots v6.2/v6.3 en concurrence sur les 2 vCPU, charge
  3,91) ; les suivants 7 à 9 min. Aucun run perdu, aucun dossier partiel
  à nettoyer.
- **Périmètre.** 8 nouveaux runs v6.2 au maximum (protocole §6), aucun autre.
  Aucun nouveau seuil proposé, aucun code modifié, aucun push GitHub dans ce
  chantier (publication sur go séparé, comme au §8.37 ; règle permanente
  « Toujours github et pdf !!! » — par le coordinateur).

— Fin de la §8.48. —
