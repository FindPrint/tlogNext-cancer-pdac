### 8.68 xCell, 64 types de cellules : un type porte une partie de la corrélation — les cellules dendritiques activées en retirent 41 % (20 novembre 2026)

Date : 20 novembre 2026 (13h04–14h00 heure de Montréal, 18h04–19h00 UTC).
Go : Zackary, 20 nov. 2026 13h04 (« Fait tout cela », 2e des 4 étapes
lancées cet après-midi-là : test décisif fraction leucocytaire, xCell
64 types, confirmation indépendante maxsep, adoption pleine).
Question ouverte du §8.60.11.
Protocole gelé avant tout téléchargement, avant tout calcul et avant tout
run : `PROTOCOL_xcell_868.md` (SHA-256
`416de4bcb783e0fc8390539a8104e7cd99b1d75355c42d4bff3e79c204c66c33`).

## Verdict d'abord

**Un type cellulaire porte une partie de la corrélation intra-famille
immunitaire — pas toute. Verdict gelé : H1-xcell PARTIELLE.** Les scores
xCell publiés (Aran et al. 2017, Additional file 6, 9 947 échantillons
TCGA/TARGET) sont obtenus et joints (**178/178 tumeurs, n effectif 178,
aucune sélection** — première fois qu'un chantier par type travaille sur
les 178 tumeurs). Le type le plus lié aux flux — les cellules
dendritiques activées (**aDC, moyenne |r| = 0,6102**) — retire à lui seul
**41,2 % de la cohésion (0,5563 → 0,3270)** après régression linéaire, et
les trois premiers types ensemble (aDC, DC, Macrophages M1) l'effondrent
(0,2600, chute 53,3 %) ; les cinq premiers (0,2239, chute 59,8 %).
Ordonner les flux par les DC les sépare à **+1,1804** — au-dessus de CD8A
brut (+0,9838) et presque au niveau de l'ImmuneScore global lui-même
(I-IMM +1,1942) — et par les aDC à **+0,8820**. Mais les flux
résidualisés séparent encore **+0,6040** (61,4 % du brut), contre +0,1982
quand on résidualise sur l'ImmuneScore GLOBAL au §8.54. **Le contraste
avec le §8.60 est l'information : CIBERSORT ne trouvait aucun porteur
(chute 4,7 % en retirant les B naïfs) ; xCell trouve un porteur partiel
fort — les cellules dendritiques, qui ne contiennent AUCUN des 12 gènes
de flux dans leurs signatures (circularité nulle pour le TOP1).**

**Le bras stromal répond à la question « stroma ou immunité ? » par les
deux.** Le meilleur type stromal — les ostéoblastes (rang 6/64, moyenne
|r| = 0,4823) — anti-corrèle avec TOUS les flux (12/12 r négatifs, tous
p < 0,05) et ordonne les flux à **+0,6099** : un miroir inversé de
l'infiltration, pas une cause séparée. Les fibroblastes, eux, suivent
l'infiltrat positivement (+0,3759, 12/12 p < 0,05). Le stroma ordonne
parce qu'il reflète l'infiltration en miroir, pas parce qu'il la porte.

**Les trois nuances sont nommées, pas cachées.** (a) Les deux types
porteurs re-mesurent en partie l'infiltration globale : aDC corrèle à
+0,8038 et DC à +0,8112 avec l'ImmuneScore ESTIMATE du §8.54 — le type
le plus porteur est aussi le meilleur reflet du global, et la part
« type » ne se sépare pas proprement de la part « quantité totale ».
(b) La cohésion persiste dans les deux moitiés d'aDC (0,3955 / 0,4324),
dont une vraie bande étroite (moitié basse, écart-type 45,5 % du global)
— argument non paramétrique contre « aDC seul porte tout », cohérent
avec PARTIELLE et non totale. (c) La concordance CD8 entre les deux
déconvolutions est modérée : xCell CD8+ T-cells vs CIBERSORT T.Cells.CD8
r = +0,4405, sous le seuil gelé de 0,5 — signalé et discuté au §8.68.2,
pas masqué : les deux méthodes ne mesurent pas la même quantité
(fraction relative vs score d'enrichissement).

## 8.68.1 Question, méthode, inventaire des sources (avant le gel)

**Question (§8.60.11).** Le §8.54 a établi que la corrélation
intra-famille immunitaire (0,5563) est expliquée par l'infiltration
immunitaire GLOBALE (ImmuneScore ESTIMATE calculé : 0,5563 → 0,2002,
chute 64,0 % ; I-RES +0,1982, 20,2 % conservés). Le §8.60 a établi
qu'aucun des 22 types CIBERSORT ne porte la corrélation seul (TOP1 B
naïfs +0,5867, TOP2 T CD8 +0,5609 ordonnent les flux, mais retirer le
meilleur type ne retire que 4,7 % de la cohésion ; D-RES +0,7692, 78,2 %
du brut) — verdict ZONE GRISE — tandis que la fraction leucocytaire
globale par méthylation en retire un tiers (−33,0 %, PARTIELLE). Reste
ouverte la confirmation par une seconde méthode de déconvolution, avec
des types que CIBERSORT ne mesure pas : QUELS types xCell (64 types,
immunitaires + stromaux) portent la corrélation — T CD8, macrophages, B,
cellules dendritiques, fibroblastes, endothélium, autres ? Et la question
stromale : un type stromal ordonne-t-il les flux, ou l'effet est-il
purement immunitaire ? Ce chantier teste ces questions. Il ne re-teste
ni l'ImmuneScore global (§8.54), ni ABSOLUTE (§8.55), ni les fractions
CIBERSORT (§8.60), et n'importe aucune conclusion d'une autre expérience :
seuls les chiffres de ce chantier (Porte D, T1–T5 du jour) et les écarts
relus des §8.44/§8.48/§8.51/§8.54/§8.55/§8.60 font le verdict.

**Ce qui existe réellement.** (a) Tarball TCGA-PAAD RSEM, Broad GDAC
Firehose 2016-01-28, MD5 `b09569ce…ac0a` (détenu, re-vérifié avant le gel)
— la même matrice que §8.54/§8.55/§8.60. (b) Base immunitaire TCGA
`pdac_immune_tcga_fluxes.csv`, n = 178, 12 gènes BRUTS log2(RSEM+1) :
CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274, PDCD1, CTLA4, GZMB, IFNG,
CD19 ; fichier d'axe joint `immune_kras_order_tcga.csv` (step, sample,
kras_raw) — clé de jointure PAR BARCODE, jamais par index. (c) AUCUN
score xCell détenu avant ce chantier (recherche §8.54.1 / §8.55.2 /
§8.60.1 : 0 occurrence). (d) Machine : Python 3 + numpy/pandas/scipy ;
R ABSENT (`Rscript` introuvable, 20 nov. 2026) — aucune voie exigeant R
n'est prévue au protocole.

**Sources externes tentées (journal complet :
`data_xcell_868/xcell_868_attempts.log`).**
- **Aran, Hu, Butte 2017, Genome Biol 18:220** (doi
  10.1186/s13059-017-1349-1, PMC5688663) — route 1a : Europe PMC
  `supplementaryFiles`
  (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5688663/supplementaryFiles`)
  renvoie HTTP 200 ; premier essai tronqué à 10 396 231 o (timeout 120 s,
  zip sans central directory, supprimé) ; le serveur ne supporte pas les
  byte ranges (erreur curl 33, pas de reprise) ; troisième essai en unité
  systemd `xcell-dl-868` : HTTP 200, **12 092 617 o en 132,7 s**,
  CURL_EXIT 0, SHA-256
  `93c9a7b0cd93d7c35ea844e917a9144c00f3f69dbe1488a87097372d3581d20c`,
  17 fichiers. Contenu : Additional file 6 (`MOESM6_ESM.tsv`,
  7 164 910 o, SHA `c731427c…51ec` — scores xCell de 9 947 échantillons
  TCGA/TARGET), Additional file 3 (`MOESM3_ESM.xlsx`, 427 029 o, SHA
  `31a7d8c4…32bc` — les 489 signatures, nécessaires au comptage de
  circularité), Additional file 7 (`MOESM7_ESM.xlsx`, 113 661 o, SHA
  `5f559c5b…03c` — matrice de spillover et coefficients de calibration,
  dont la colonne `Group` documente les familles). **Porte D OUVERTE
  par la source 1a au premier essai utile** : routes 1b/1c, 2 (scores),
  3, 4 non tentées pour les scores (inutiles) ; la Voie C (calcul depuis
  la matrice détenue) n'a pas été utilisée — scores publiés obtenus.
- **xCell, package R (GitHub `dviraran/xCell`, GPL-3.0 ; Zenodo
  10.5281/zenodo.1004662)** : non téléchargé — les signatures sont déjà
  dans l'Additional file 3 obtenu ; la Voie C n'a pas été nécessaire.
- **TIMER2.0 (Li et al. 2020, doi 10.1093/nar/gkaa407)** : non tenté —
  porte D déjà ouverte (source 1) ; serveur interactif sans fichier en
  vrac, déjà constaté au §8.60.

**Circularité (comptée en machine, §8.68.2).** Les 489 signatures
(Additional file 3, 64 préfixes = exactement les 64 types du fichier de
scores, noms identiques) contiennent comme gènes 10 des 12 flux au total
(absents de toutes les signatures : CD68 et CD274 — détail au §8.68.2) ; **23 types sur 64 contiennent ≥ 1 des 12
flux** (43 occurrences). Le TOP1 (aDC) n'en contient AUCUN : sa
signature (6 sources, union comptée en machine) ne contient ni CD8A, ni
CD19, ni aucun des 12 flux. La sensibilité T2(d) (§8.68.4) est donc
identique au primaire — la persistance partielle n'est pas un artefact
du gène marqueur, parce qu'il n'y a pas de gène marqueur.

**Hypothèses gelées.** H1-xcell : la corrélation est portée par la
quantité d'un ou plusieurs types cellulaires xCell (immunitaires ou
stromaux) — (a) chaque flux corrèle substantiellement avec au moins un
type ; (b) après régression sur le(s) type(s) porteur(s), la corrélation
intra-famille s'effondre ; (c) ordonner les flux par le score du type
porteur les sépare (S_sep au niveau IMMROT) ; (d) ordonner les flux
RÉSIDUALISÉS par CD8A résidualisé ne sépare plus. H0-xcell : la
corrélation persiste après contrôle de chaque type et de leur
combinaison, par toutes les voies (a)–(d).

**Critères gelés.** T1 : type « porteur candidat » si moyenne |r| ≥ 0,30
sur les 12 flux ; « faible » si < 0,15 pour tous les types. TOP1/TOP2 =
les deux premiers du classement T1 (égalité départagée par la moyenne
des |ρ|). TOP-STROM = premier type stromal du classement (stromal =
`Group` « Non-Hematopoietic » de MOESM7, feuille « Spill - Seq »,
RNA-seq). T2 : EFFONDREMENT si moyenne |r| résiduelle < 0,30 (chute
≥ 45 % depuis la brute appariée) ET fraction |r| > 0,5 < 0,20 ;
PERSISTANCE si chute < 20 % (moyenne résiduelle > 0,80 × brute
appariée) ; entre les deux : partielle. Primaire T2 = résidus sur
[1, TOP1] ; sensibilités (b) TOP1–3, (c) tous les types à moyenne
|r| ≥ 0,30 (max 5), (d) paires sans marqueur de la signature du TOP1.
T5 : D-XTOP1/D-XTOP2 soutiennent H1-xcell si écart S_sep ≥ 0,45
(minimum IMMROT sans doublon) ; D-XRES soutient H1-xcell si écart
< 0,30, soutient H0-xcell si écart ≥ 0,45 ; D-XSTROM (conditionnel :
lancé si et seulement si TOP-STROM n'est ni TOP1 ni TOP2 ET sa moyenne
|r| ≥ 0,30, décision sur les seuls chiffres T1 avant tout run) soutient
« porteur stromal » si écart ≥ 0,45. Verdict : H1-xcell SOUTENUE si T2
primaire = effondrement ET D-XRES < 0,30 ET (D-XTOP1 ≥ 0,45 OU D-XTOP2
≥ 0,45) ; H1-xcell PARTIELLE si T2 = partielle OU (D-XTOP1/D-XTOP2
entre 0,30 et 0,45) avec D-XRES < 0,70 ; H0-xcell SOUTENUE si T2 =
persistance ET D-XTOP1 < 0,30 ET D-XTOP2 < 0,30 ET D-XRES ≥ 0,45 ; toute
autre combinaison : zone grise, test par test. Le bras stromal ne change
pas le verdict principal : il est rapporté séparément.

## 8.68.2 Porte D (source) : OUVERTE — jointure 178/178, identification, sélection nulle

**Fichiers obtenus, lus en clair.** `13059_2017_1349_MOESM6_ESM.tsv` :
64 lignes types × 9 947 colonnes échantillons (9 358 TCGA + 589 TARGET),
**0 NaN**, valeurs min −0,0000, max 5,3830. Les 64 types documentés :
aDC, Adipocytes, Astrocytes, B-cells, Basophils, CD4+ memory T-cells,
CD4+ naive T-cells, CD4+ T-cells, CD4+ Tcm, CD4+ Tem, CD8+ naive
T-cells, CD8+ T-cells, CD8+ Tcm, CD8+ Tem, cDC, Chondrocytes,
Class-switched memory B-cells, CLP, CMP, DC, Endothelial cells,
Eosinophils, Epithelial cells, Erythrocytes, Fibroblasts, GMP,
Hepatocytes, HSC, iDC, Keratinocytes, ly Endothelial cells, Macrophages,
Macrophages M1, Macrophages M2, Mast cells, Megakaryocytes, Melanocytes,
Memory B-cells, MEP, Mesangial cells, Monocytes, MPP, MSC, mv
Endothelial cells, Myocytes, naive B-cells, Neurons, Neutrophils,
NK cells, NKT, Osteoblast, pDC, Pericytes, Plasma cells, Platelets,
Preadipocytes, pro B-cells, Sebocytes, Skeletal muscle, Smooth muscle,
Tgd cells, Th1 cells, Th2 cells, Tregs. Groupes MOESM7 (« Spill - Seq ») :
Immune 34, Non-Hematopoietic 21, HSC 9. Stromaux (21) : Adipocytes,
Astrocytes, Chondrocytes, Endothelial cells, Epithelial cells,
Fibroblastes, Hepatocytes, Keratinocytes, ly Endothelial cells,
Melanocytes, Mesangial cells, MSC, mv Endothelial cells, Myocytes,
Neurons, Osteoblast, Pericytes, Preadipocytes, Sebocytes, Skeletal
muscle, Smooth muscle.

**Jointure par patient (12 caractères), puis par échantillon (15).**
Les identifiants xCell utilisent des points (`TCGA.V4.A9EE.01`) :
convertis en tirets, jointure sur les 12 premiers caractères, 0 doublon
de clé. **178/178 tumeurs appariées, 0 absente, 0 collision — n effectif
178.** Aucune ligne tout-NaN : il n'y a PAS de sélection dans ce
chantier. La cohésion brute recalculée sur n = 178 est **0,5563** —
exactement la valeur du §8.54 à n = 178 (contre 0,5044 à n = 151 au
§8.60 et 0,5040 à n = 149 au §8.55) : pour la première fois, un chantier
par type travaille sans biais de sélection non-whitelist.

**Identification comme scores d'Aran et al. — trois vérifications.**
(a) Effectif exact : 9 947 colonnes = les 9 947 échantillons annoncés
pour l'Additional file 6 (9 358 TCGA + 589 TARGET). (b) Les 64 types
présents sont les 64 types xCell documentés, avec les signatures
correspondantes (489 signatures, 64 préfixes, noms identiques) et la
matrice de spillover (MOESM7, 64 × 64, diagonale 1). (c) Validation
croisée, par type : xCell CD8+ T-cells vs flux CD8A r = **+0,5851**
(n = 178, p = 9,7×10⁻¹⁸) ; xCell B-cells vs flux CD19 r = **+0,6768**
(p = 3,4×10⁻²⁵) ; xCell Macrophages vs flux CD68 r = **+0,7169**
(p = 2,2×10⁻²⁹) ; xCell CD8+ T-cells vs ImmuneScore (§8.54)
r = +0,4500 (p = 3,0×10⁻¹⁰). **Nuance nommée (§4c) : xCell CD8+
T-cells vs fraction CIBERSORT T.Cells.CD8 (§8.60) r = +0,4405 (n = 151,
p = 1,5×10⁻⁸) — positif et significatif, mais SOUS le seuil gelé de 0,5
pour « fortement ».** L'identification n'est pas remise en cause — (a)
et (b) sont exacts, et trois des quatre contrôles (c) sont forts — mais
la concordance CD8 entre les deux déconvolutions est modérée : CIBERSORT
donne une fraction RELATIVE dans le compartiment immunitaire (somme = 1)
tandis que xCell donne un score d'ENRICHISSEMENT ssGSEA avec compensation
de spillover ; elles ne mesurent pas la même quantité, et le CD8 xCell
corrèle d'ailleurs moins avec l'ImmuneScore (0,4500) que les B naïfs
CIBERSORT (0,4723) ou les aDC xCell (0,8038). Pas de ligne
ImmuneScore/StromaScore/MicroenvironmentScore agrégée dans MOESM6 (64
types seuls) : le contrôle §4c par ImmuneScore xCell est impossible sur
ce fichier — remplacé par les quatre contrôles ci-dessus, noté ici.

**Circularité (comptée en machine).** Union des gènes des signatures
(MOESM3) par type, intersection avec les 12 flux : 23/64 types
contiennent ≥ 1 flux (43 occurrences). Détail : B-cells → CD19 ;
Basophils → GZMB ; CD4+ memory T-cells → CTLA4, PDCD1 ; CD4+ naive
T-cells → CD4, CTLA4 ; CD4+ T-cells → CD4, CTLA4, FOXP3 ; CD4+ Tcm →
CD4, CTLA4 ; CD4+ Tem → CD4, CTLA4, PDCD1 ; CD8+ naive T-cells → CD8A,
CD8B ; CD8+ T-cells → CD8A, CD8B ; CD8+ Tcm → CD8A, CD8B, PDCD1 ; CD8+
Tem → CD8A, CD8B, GZMB, IFNG, PDCD1 (5/12, le plus chargé) ; cDC →
CD163 ; Macrophages → CD163 ; Macrophages M1 → CD163 ; Memory B-cells →
CD19 ; Monocytes → CD163, CD4 ; naive B-cells → CD19 ; NK cells →
GZMB, IFNG ; pDC → GZMB ; Plasma cells → CD19 ; Tgd cells → CTLA4,
GZMB, IFNG ; Th1 cells → IFNG ; Tregs → CTLA4, FOXP3. **aDC, DC et
Macrophages M1 (TOP1/TOP2/TOP3) : aDC contient 0 flux ; DC contient 0
flux ; Macrophages M1 ne contient que CD163 (1/12, sur 188 gènes).**
Les deux types porteurs ne sont pas des artefacts de leurs gènes
marqueurs — ils n'en ont pas parmi les 12 flux.

## 8.68.3 T1 — Chaque flux immunitaire suit les cellules dendritiques : fortement, 29 types au-dessus du seuil

Pearson r (+ Spearman ρ) de chaque flux contre chaque type (n = 178) ;
p brutes bilatérales, sans correction pour tests multiples (768 tests,
~38 faux positifs attendus à p < 0,05 sous le nul — le jugement porte
sur les moyennes, pas sur une p isolée). Moyenne des |r| par type,
classement décroissant :

| Type | Groupe | moyenne \|r\| | moyenne \|ρ\| | R² médian |
|---|---|---|---|---|
| **aDC (TOP1)** | Immune | **0,6102** | 0,6096 | 0,381 |
| **DC (TOP2)** | Immune | **0,5796** | 0,6430 | 0,333 |
| **Macrophages M1 (TOP3)** | Immune | **0,5090** | 0,4965 | 0,257 |
| Macrophages | Immune | 0,4923 | 0,5096 | 0,214 |
| CD8+ Tcm | Immune | 0,4917 | 0,5152 | 0,319 |
| **Osteoblast (TOP-STROM)** | Non-Hematopoietic | **0,4823** | 0,4648 | 0,237 |
| CD4+ memory T-cells | Immune | 0,4593 | 0,5144 | 0,271 |
| CD4+ naive T-cells | Immune | 0,4541 | 0,6038 | 0,267 |
| Monocytes | Immune | 0,4207 | 0,5187 | 0,153 |
| HSC | HSC | 0,3941 | 0,4226 | 0,164 |
| cDC | Immune | 0,3930 | 0,4684 | 0,180 |
| pDC | Immune | 0,3849 | 0,3551 | 0,157 |
| CD4+ Tem | Immune | 0,3788 | 0,3616 | 0,161 |
| Chondrocytes | Non-Hematopoietic | 0,3777 | 0,3768 | 0,145 |
| Fibroblasts | Non-Hematopoietic | 0,3759 | 0,4035 | 0,162 |
| B-cells | Immune | 0,3660 | 0,4864 | 0,173 |
| CD8+ T-cells | Immune | 0,3659 | 0,3575 | 0,153 |
| Endothelial cells | Non-Hematopoietic | 0,3635 | 0,4066 | 0,178 |
| CD4+ Tcm | Immune | 0,3602 | 0,3921 | 0,116 |
| Th1 cells | Immune | 0,3587 | 0,4334 | 0,138 |
| Mast cells | Immune | 0,3536 | 0,3118 | 0,129 |
| iDC | Immune | 0,3483 | 0,3676 | 0,126 |
| Smooth muscle | Non-Hematopoietic | 0,3339 | 0,3024 | 0,131 |
| Megakaryocytes | HSC | 0,3323 | 0,3246 | 0,125 |
| naive B-cells | Immune | 0,3211 | 0,2611 | 0,135 |
| CD8+ Tem | Immune | 0,3207 | 0,1365 | 0,135 |
| ly Endothelial cells | Non-Hematopoietic | 0,3133 | 0,3474 | 0,145 |
| Class-switched memory B-cells | Immune | 0,3090 | 0,2387 | 0,105 |
| Memory B-cells | Immune | 0,3055 | 0,2334 | 0,125 |
| Mesangial cells | Non-Hematopoietic | 0,2843 | 0,2060 | 0,084 |
| NKT | Immune | 0,2813 | 0,2964 | 0,054 |
| mv Endothelial cells | Non-Hematopoietic | 0,2812 | 0,2872 | 0,110 |
| Adipocytes | Non-Hematopoietic | 0,2769 | 0,3495 | 0,100 |
| Melanocytes | Non-Hematopoietic | 0,2716 | 0,3443 | 0,065 |
| MEP | HSC | 0,2677 | 0,3030 | 0,075 |
| Astrocytes | Non-Hematopoietic | 0,2616 | 0,2989 | 0,055 |
| Plasma cells | Immune | 0,2596 | 0,2054 | 0,091 |
| CLP | HSC | 0,2341 | 0,2722 | 0,066 |
| pro B-cells | Immune | 0,2264 | 0,0659 | 0,057 |
| Neurons | Non-Hematopoietic | 0,2250 | 0,1237 | 0,033 |
| Macrophages M2 | Immune | 0,2218 | 0,2097 | 0,034 |
| CD4+ T-cells | Immune | 0,2180 | 0,0809 | 0,058 |
| Skeletal muscle | Non-Hematopoietic | 0,2146 | 0,1015 | 0,070 |
| Preadipocytes | Non-Hematopoietic | 0,2132 | 0,0800 | 0,062 |
| Epithelial cells | Non-Hematopoietic | 0,2015 | 0,3080 | 0,032 |
| Basophils | Immune | 0,2007 | 0,0622 | 0,038 |
| CD8+ naive T-cells | Immune | 0,1957 | 0,1495 | 0,049 |
| GMP | HSC | 0,1835 | 0,1595 | 0,036 |
| Sebocytes | Non-Hematopoietic | 0,1793 | 0,2547 | 0,029 |
| Tregs | Immune | 0,1742 | 0,1614 | 0,024 |
| Neutrophils | Immune | 0,1670 | 0,0430 | 0,038 |
| Tgd cells | Immune | 0,1550 | 0,0766 | 0,029 |
| Pericytes | Non-Hematopoietic | 0,1425 | 0,1331 | 0,019 |
| Keratinocytes | Non-Hematopoietic | 0,1375 | 0,1843 | 0,018 |
| Th2 cells | Immune | 0,1291 | 0,0895 | 0,019 |
| MSC | Non-Hematopoietic | 0,1122 | 0,1156 | 0,009 |
| NK cells | Immune | 0,1079 | 0,0458 | 0,013 |
| Eosinophils | Immune | 0,0852 | 0,0884 | 0,005 |
| Platelets | HSC | 0,0850 | 0,0807 | 0,007 |
| CMP | HSC | 0,0848 | 0,0448 | 0,006 |
| Hepatocytes | Non-Hematopoietic | 0,0742 | 0,0602 | 0,004 |
| Myocytes | Non-Hematopoietic | 0,0554 | 0,0560 | 0,002 |
| Erythrocytes | HSC | 0,0539 | 0,0815 | 0,002 |
| MPP | HSC | 0,0372 | 0,1019 | 0,001 |

**29 types sur 64 dépassent le seuil gelé de 0,30** (dont 8 au-dessus de
0,45) — contre 2 types sur 22 au §8.60 (0,3314 et 0,3293, de justesse).
À comparer : l'ImmuneScore global (§8.54) donnait une moyenne |r| de
0,7164 et la fraction leucocytaire par méthylation (bras L, §8.60)
0,5456 — le TOP1 xCell (0,6102) se place entre les deux, au-dessus de
la fraction leucocytaire ; les 35 autres types sont sous 0,30, dont 12
sous 0,15. Les types xCell sont 1,8× plus liés aux flux que les meilleurs
types CIBERSORT (0,6102 contre 0,3314).

**Par flux, TOP1 (aDC, médiane 0,0951, moyenne 0,0991, max 0,2568, 0
zéro).** r TOUS positifs, 12/12 significatifs (p max 4,2×10⁻⁷) : CD4
+0,748, CTLA4 +0,743, PDCD1 +0,718, CD8A +0,699, FOXP3 +0,676, CD8B
+0,621, GZMB +0,614, CD19 +0,606, CD163 +0,590, IFNG +0,491, CD68
+0,449, CD274 +0,369. Le lien n'est concentré sur aucun gène marqueur —
il n'y en a pas dans la signature aDC — il est diffus sur toute la
famille. Descriptif : r(aDC, ImmuneScore) = **+0,8038** ; r(aDC,
ABSOLUTE) = −0,5346. Les aDC re-mesurent l'infiltration globale presque
aussi bien que l'ImmuneScore lui-même.

**Par flux, TOP2 (DC, médiane 0,0551, moyenne 0,0644, max 0,3803, 1
zéro).** r TOUS positifs, 12/12 significatifs (p max 5,2×10⁻⁶) : CD4
+0,765, FOXP3 +0,740, CTLA4 +0,689, CD163 +0,631, CD8A +0,617, PDCD1
+0,589, CD8B +0,564, GZMB +0,540, CD19 +0,518, CD68 +0,518, CD274
+0,450, IFNG +0,334. Descriptif : r(DC, ImmuneScore) = **+0,8112** ;
r(DC, ABSOLUTE) = −0,5342.

**TOP3 (Macrophages M1, moyenne |r| 0,5090).** r TOUS positifs, 12/12
significatifs (p max 6,1×10⁻⁴) : CD163 +0,707, CD4 +0,695, CD68 +0,684,
CTLA4 +0,538, FOXP3 +0,523, PDCD1 +0,512, GZMB +0,501, IFNG +0,465,
CD8A +0,451, CD8B +0,423, CD274 +0,355, CD19 +0,254.

**TOP-STROM (Osteoblast, rang 6/64, moyenne |r| 0,4823).** r TOUS
NÉGATIFS, 12/12 significatifs (p max 2,7×10⁻⁵) : CD68 −0,671, CD4
−0,615, CTLA4 −0,594, FOXP3 −0,556, CD163 −0,525, PDCD1 −0,492, CD8A
−0,482, CD8B −0,417, CD274 −0,402, GZMB −0,397, CD19 −0,329, IFNG
−0,309. Descriptif : r(Osteoblast, ImmuneScore) = **−0,6387** ;
r(Osteoblast, ABSOLUTE) = +0,3163. Le score ostéoblaste est le miroir
inversé de l'infiltration : plus il est haut, moins le signal
immunitaire est fort. Les fibroblastes, autre stromal notable (rang 15,
0,3759), suivent l'infiltrat POSITIVEMENT (12/12 significatifs, CD8A
+0,486, CD163 +0,496 en tête) : les deux stromaux ne disent pas la même
chose — l'un est un miroir négatif, l'autre un suiveur positif.

## 8.68.4 T2 — La corrélation intra-famille chute de 41 % après régression sur les aDC : PARTIELLE

Matrice 66 paires, sur les n = 178 appariées (la brute de référence est
recalculée sur ce sous-ensemble, jamais importée du §8.54 — elle vaut
ici exactement 0,5563, comme au §8.54).

| Matrice | Pearson moyenne \|r\| | médiane \|r\| | fraction \|r\| > 0,5 | max \|r\| |
|---|---|---|---|---|
| Brute (n = 178) | **0,5563** | 0,5677 | 0,621 (41/66) | 0,8430 |
| Résidus [1, TOP1 = aDC] (a, PRIMAIRE) | **0,3270** | 0,3254 | **0,152 (10/66)** | 0,7294 |
| Résidus [1, TOP1, TOP2, TOP3] (b) | 0,2600 | 0,2348 | 0,121 (8/66) | 0,7115 |
| Résidus [1, types à moyenne \|r\| ≥ 0,30] (c, 5 premiers) | 0,2239 | 0,2069 | 0,076 (5/66) | 0,6608 |
| Paires sans marqueur signature TOP1 (d) : brute → résiduelle | 0,5563 → **0,3270** | 0,5677 → 0,3254 | 0,621 → 0,152 | 0,8430 → 0,7294 |

**Chute primaire : 41,2 %** (0,5563 → 0,3270) ; (b) 53,3 % ; (c)
59,8 %. Critère gelé : ni EFFONDREMENT (résiduelle 0,3270 > 0,30, de
justesse — 0,027 au-dessus du seuil — bien que la fraction > 0,5 soit
déjà sous 0,20 : 0,152) ni PERSISTANCE (chute 41,2 % > 20 %) :
**T2 = PARTIELLE**. Retirer linéairement le type le plus porteur retire
deux cinquièmes de la corrélation ; retirer les trois premiers
l'effondre par les critères (0,2600 < 0,30, fraction 0,121 < 0,20) ;
retirer les cinq premiers la retire aux trois cinquièmes (0,2239).
C'est l'inverse du §8.60, où retirer les B naïfs ne retirait que 4,7 %
et les trois premiers 7,4 % — et c'est moins que le §8.54, où retirer
l'ImmuneScore global retirait 64,0 %.

**Garde-fou de circularité (d).** La signature aDC ne contient AUCUN
des 12 flux : les 12 gènes sont conservés, 66 paires, brute 0,5563 →
résiduelle 0,3270 (chute 41,2 %, identique au primaire). La partielle
n'est pas un artefact du gène marqueur : il n'y a pas de gène marqueur.
Le lien aDC ↔ famille immunitaire est réel et diffus — il ne passe par
aucun des 12 gènes de flux.

## 8.68.5 T3 — Couplage prédit : la régression §8.48 tient, avant comme après

Couplage C par contrôle immunitaire (moyenne des |r| avec les 11 autres
flux), brut contre résidualisé sur TOP1 ; d_ssep prédit par
d = −0,175 + 1,705·C.

| | C moyen | d_ssep prédit moyen |
|---|---|---|
| Brut (n = 178) | 0,5563 | **+0,7735** |
| Résidualisé [aDC] | 0,3270 | **+0,3825** |

Sanité : la prédiction brute (0,7735) est dans la gamme des écarts
IMMROT observés (moyenne +0,7521) — la régression §8.48 se réplique sur
ces données. CD8A seul : C 0,6514 → 0,4218, d_pred 0,9356 → **0,5441**.
Le T3 ne fait que traduire T2 en S_sep prédit ; le verdict se joue au
T5 — et c'est là que la prédiction sera mise en défaut pour D-XTOP2
(§8.68.7).

## 8.68.6 T4 — Stratification : la cohésion persiste dans chaque moitié — et la moitié basse EST une bande étroite

Médiane des aDC = 0,0951 (n = 89/89) ; matrice intra-famille dans
chaque moitié.

| Stratification | Moitié haute : moyenne \|r\| (frac. > 0,5) | Moitié basse : moyenne \|r\| (frac. > 0,5) |
|---|---|---|
| aDC (méd. 0,0951) | 0,3955 (0,409, 27/66) | 0,4324 (0,424, 28/66) |

La cohésion persiste dans les deux moitiés (0,40 et 0,43, contre 0,5563
global) — réduite, pas effondrée. La moitié BASSE est une vraie bande
étroite : l'écart-type des aDC y est de 0,0294, soit 45,5 % de
l'écart-type global (0,0646) — sous le seuil gelé de 50 %. Dans cette
bande où les aDC sont faibles et peu dispersées, la cohésion reste à
0,4324 : les aDC seuls ne portent pas toute la cohésion. **T4 soutient
H0-xcell par une voie non paramétrique, indépendante de toute linéarité
— en tension avec T2 partielle, cohérente avec PARTIELLE et non totale.**
(La moitié haute reste large, écart-type 0,0420, 65,0 % du global :
elle n'est pas tranchante, et n'a pas besoin de l'être — la moitié basse
suffit à l'argument.)

## 8.68.7 T5 — Runs v6.2 : les dendritiques ordonnent les flux, les résidus aussi, le stroma aussi

Prédictions calculées AVANT de lire les sorties (depuis T1/T2/T3 du
jour) : D-XTOP1 d_pred +0,8654 (C = 0,6102) ; D-XTOP2 d_pred +0,8132
(C = 0,5796) ; D-XRES d_pred +0,5441 (C_résid CD8A = 0,4218) ;
D-XSTROM d_pred +0,6473 (C = 0,4823). 8 runs v6.2, mode fast, graine 42,
**8/8 exit 0** (lot 18:15:27–18:52:21 UTC 20 nov., unité unique
`v62-xcell-868`, aucune interruption, aucun redémarrage machine
pendant le lot — uptime 1 h 32 à 18:54, boot avant le lot).

| Run | Contrôle → analysés | S_sep réel | S_sep nul | Écart | Prédit | MC réel / nul | Delta réel / nul | w | t0 |
|---|---|---|---|---|---|---|---|---|---|
| D-XTOP1 | aDC → 12 imm. bruts | 1,1115 | 0,2295 | **+0,8820** | +0,8654 | 0,4527 / 0,4679 | 4,30 / 3,12 | 30 | 78,34 % |
| D-XTOP2 | DC → 12 imm. bruts | 1,3344 | 0,1540 | **+1,1804** | +0,8132 | 0,4759 / 0,3269 | 4,32 / 3,81 | 30 | 43,53 % |
| D-XRES | CD8A résid. → 11 imm. résid. | 0,7842 | 0,1802 | **+0,6040** | +0,5441 | 0,4160 / 0,3284 | 4,24 / 4,22 | 30 | 26,72 % |
| D-XSTROM | Osteoblast → 12 imm. bruts | 0,8071 | 0,1972 | **+0,6099** | +0,6473 | 0,4164 / 0,5248 | 4,25 / 3,04 | 30 | 46,08 % |

Lecture par critère gelé :
- **D-XTOP1 : les aDC ordonnent les flux.** Écart +0,8820 — au-dessus
  du seuil H1 (0,45), à 117 % de la moyenne IMMROT (+0,7521), et
  **+0,0166 au-dessus de la prédiction** (+0,8654) : la régression §8.48
  prédit ce contrôle presque exactement. MC ne sépare PAS (−0,0152 :
  0,4527 contre 0,4679, nul devant) — noté, non utilisé pour le verdict
  (MC n'est pas le critère gelé ; S_sep l'est). Delta sépare ici (4,30
  contre 3,12) — noté, non utilisé (Delta non élucidé, §8.49). L7a
  sépare en direction up des deux côtés (+0,1821 contre +0,3838) :
  non utilisé, comme au §8.48/§8.54/§8.60. Le seuil est trouvé TARD
  (t0 = 78,34 %) : la séparation est portée par le haut de
  l'ordonnancement. Critère gelé : D-XTOP1 ≥ 0,45 → **soutient H1-xcell,
  seul**.
- **D-XTOP2 : les DC ordonnent les flux encore mieux.** Écart +1,1804
  — au-dessus du seuil H1 (0,45), à 157 % de la moyenne IMMROT,
  **+0,3672 AU-DESSUS de la prédiction** (+0,8132) : la régression §8.48
  sous-prédit ce contrôle de plus d'un tiers d'écart — comme au §8.60
  où D-TOP1/D-TOP2 dépassaient leurs prédictions de ~+0,18–0,20, mais
  ici deux fois plus. C'est le deuxième plus fort écart de contrôle
  jamais mesuré dans le chantier, derrière I-IMM (+1,1942, §8.54) et
  devant CD8A brut (+0,9838, §8.48). MC sépare (+0,1490 : 0,4759 contre
  0,3269) ; Delta 4,32 contre 3,81 — noté, non utilisé. Seuil à 43,53 %.
  Critère gelé : D-XTOP2 ≥ 0,45 → **soutient H1-xcell, seul**. Les deux
  types dendritiques ordonnent les flux — et l'un d'eux en retire deux
  cinquièmes en linéaire (T2) : ordonner n'est plus seulement ordonner,
  ici.
- **D-XRES : la séparation survit aux deux tiers.** Écart +0,6040 contre
  +0,9838 pour CD8A brut (**61,4 % conservés, baisse de 38,6 %**) et
  contre +0,5441 prédit (+0,0599 au-dessus — la régression §8.48 prédit
  bien le résiduel ici). MC +0,0876 (0,4160 contre 0,3284) ; Delta quasi
  égal (4,24 contre 4,22). L7a sépare en direction (up +0,1753 contre
  down −0,1496) : non utilisé. Seuil à 26,72 %. Critère gelé : D-XRES
  ≥ 0,45 → **soutient H0-xcell, seul**. Le contraste avec I-RES
  (+0,1982, §8.54) reste net : résidualiser sur le score GLOBAL tue la
  séparation (20,2 % conservés) ; résidualiser sur le meilleur TYPE
  xCell la laisse à 61,4 % — moins que les 78,2 % du §8.60 (D-RES
  +0,7692), davantage que les 20,2 % du §8.54. Un type xCell retire
  plus qu'un type CIBERSORT, mais moins que le global.
- **D-XSTROM : le type stromal ordonne les flux aussi.** Écart +0,6099
  — au-dessus du seuil (0,45), contre +0,6473 prédit (−0,0374). MC ne
  sépare PAS (−0,1084 : 0,4164 contre 0,5248, nul devant) — noté, non
  utilisé. Delta 4,25 contre 3,04 — noté, non utilisé. L7a down des deux
  côtés (−0,2078 contre −0,1710), cohérent avec l'anti-corrélation
  stromale : non utilisé. Seuil à 46,08 %. Critère gelé : D-XSTROM
  ≥ 0,45 → **soutient « porteur stromal » au sens de l'ordre**. Le
  stromal ordonne parce qu'il est le miroir inversé de l'infiltration
  (r = −0,6387 avec l'ImmuneScore) : trier par ostéoblastes croissants,
  c'est trier par infiltration décroissante. Ce n'est pas une cause
  séparée — c'est la même quantité, vue de l'autre côté.

## 8.68.8 Verdict de synthèse

Règle gelée, test par test (bras principal) : T1 = 29 types au-dessus
du seuil (TOP1 aDC 0,6102 ; TOP2 DC 0,5796 ; TOP3 Macrophages M1 0,5090 ;
TOP-STROM Osteoblast 0,4823, rang 6/64) ; T2 primaire = PARTIELLE
(0,5563 → 0,3270, chute 41,2 %) ; T2 sensibilités (b) 53,3 %,
(c) 59,8 %, (d) 41,2 % (identique au primaire, circularité nulle) ;
T4 = persistance dans les deux moitiés, dont une bande étroite (moitié
basse, ET 45,5 % du global) ; D-XTOP1 = +0,8820 (≥ 0,45) ; D-XTOP2 =
+1,1804 (≥ 0,45) ; D-XRES = +0,6040 (≥ 0,45, < 0,70) ; D-XSTROM =
+0,6099 (≥ 0,45).
**H1-xcell totale est rejetée** (T2 n'est pas un effondrement, D-XRES
n'est pas < 0,30). **H0-xcell stricte est rejetée** (T2 n'est pas une
persistance ; D-XTOP1/D-XTOP2 ne sont pas < 0,30). **H1-xcell PARTIELLE
est SOUTENUE** : T2 = partielle ET D-XRES < 0,70. Aucun consensus exigé
entre les tests : chaque test est rapporté avec son propre critère ; le
verdict suit la règle ci-dessus, pas un vote.

**Ce que cela dit, et ce que cela ne dit pas.** (a) Cela dit qu'un type
cellulaire — les cellules dendritiques activées — porte à lui seul deux
cinquièmes de la corrélation intra-famille immunitaire, et que les
trois premiers types ensemble l'effondrent par les critères gelés. C'est
la première fois qu'un type seul retire une part substantielle : au
§8.60, aucun type CIBERSORT ne retirait rien de mesurable (4,7 %). (b)
Cela dit que les deux types dendritiques ordonnent réellement les flux
(écarts +0,88/+1,18, au-dessus du minimum IMMROT, le second presque au
niveau de l'ImmuneScore global) — et que leur lien n'est PAS mécanique :
leurs signatures ne contiennent aucun des 12 gènes de flux. (c) Cela dit
que l'effet de composition identifié au §8.54 est porté en partie par
des types précis, pas seulement par la quantité totale d'infiltrat : le
score global (ImmuneScore, −64 %) reste le plus fort, la fraction
leucocytaire globale par méthylation (−33 %, §8.60) et les aDC (−41 %)
se placent entre les deux, ABSOLUTE (−25,5 %, §8.55) derrière. (d) Cela
ne dit pas que les aDC CAUSENT la corrélation : une corrélation n'est
pas une causalité, et les aDC re-mesurent l'infiltration globale
(r = +0,8038 avec l'ImmuneScore) — la part « type » et la part
« quantité totale » ne se séparent pas proprement ici ; le T4 (persistance
dans la bande étroite basse) rappelle que la cohésion survit sans aDC.
(e) Cela ne dit pas que les deux cinquièmes restants après l'ImmuneScore
sont « biologiques » au sens d'une régulation : ils peuvent venir d'une
variable latente non testée (sous-type moléculaire, état d'activation).
(f) La domination IMMROT du §8.48 n'est pas remise en cause : elle reste
expliquée par le couplage, dont la cause amont est désormais précisée —
le couplage est porté par l'infiltration globale ET, en partie, par les
cellules dendritiques qui la reflètent le mieux.

**Bras stromal, verdict séparé (critères gelés §7).** TOP-STROM =
Osteoblast (0,4823, rang 6/64) ; D-XSTROM = +0,6099 (≥ 0,45).
**Le type stromal ordonne les flux, en miroir inversé de
l'infiltration.** Ce n'est pas un porteur stromal indépendant : ses
corrélations sont toutes négatives, il corrèle à −0,6387 avec
l'ImmuneScore et à +0,3163 avec ABSOLUTE (plus pur = plus d'ostéoblastes
= moins d'immunitaire). La question « stroma ou immunité ? » reçoit une
réponse en miroir : le stroma ordonne parce que l'infiltration le
déplace, pas parce qu'il porte la corrélation par lui-même. Les
fibroblastes (+0,3759, positifs) disent la même chose de l'autre côté :
le stroma suit l'infiltrat.

## 8.68.9 Provenance

- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant les calculs, dans le log du lot, et après l'extraction).
  Mode `fast`, graine 42 (défaut), nul = bloc analysé permuté
  conjointement, graine 42 (default_rng frais par fichier), contrôle
  intact.
- **Protocole.** `PROTOCOL_xcell_868.md`, SHA-256
  `416de4bcb783e0fc8390539a8104e7cd99b1d75355c42d4bff3e79c204c66c33`,
  gelé le 20 nov. 2026 à 18h07 UTC avant tout téléchargement, tout calcul
  et tout run de ce chantier. Aucun amendement après le gel.
- **Entrées externes.** (1) Aran, Hu, Butte 2017, Genome Biol 18:220
  (PMID 29141603, PMCID PMC5688663, DOI 10.1186/s13059-017-1349-1 ;
  méthode xCell : ssGSEA par signature + compensation de spillover +
  calibration ; article CC-BY 4.0, données CC0) — via Europe PMC
  `supplementaryFiles`
  (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5688663/supplementaryFiles`,
  HTTP 200, 20 nov. 2026 18:09–18:12 UTC, 12 092 617 octets, SHA-256
  `93c9a7b0cd93d7c35ea844e917a9144c00f3f69dbe1488a87097372d3581d20c`) :
  `13059_2017_1349_MOESM6_ESM.tsv` (Additional file 6, scores xCell de
  9 947 échantillons TCGA/TARGET, SHA-256
  `c731427c4a69f82c82bc2f3592116cc6fdc32e8f52b515e1055a9bb9822c51ec`,
  7 164 910 octets) ; `13059_2017_1349_MOESM3_ESM.xlsx` (Additional
  file 3, 489 signatures, SHA-256
  `31a7d8c45414100b87bbb25139e106ed95ab3ff5f43e54865f97664a77ad32bc`,
  427 029 octets) ; `13059_2017_1349_MOESM7_ESM.xlsx` (Additional file 7,
  spillover + calibration, SHA-256
  `5f559c5b46b46248228630d8e6cc8e8efc362d94adcb77e5c100ea085b2ac03c`,
  113 661 octets). (2) Sources non utilisées : package xCell GitHub
  `dviraran/xCell` (GPL-3.0, Zenodo 10.5281/zenodo.1004662), TIMER2.0
  (Li et al. 2020, doi 10.1093/nar/gkaa407), Voie C — scores publiés
  obtenus, calcul non nécessaire.
- **Entrées du projet.** Tarball TCGA-PAAD RSEM, MD5
  `b09569ce3f4721f514bc137bd109ac0a` (vérifié) ; base immunitaire
  `pdac_immune_tcga_fluxes.csv`, SHA-256
  `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e` ; axe
  `immune_kras_order_tcga.csv`, SHA-256
  `31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d` ;
  scores §8.54 `infiltration_854_scores.csv`, SHA-256
  `628732ecbcc30a3281b0df7a5039ec2520a1c5f1a1ae9ce412c4d0d7caf78aa7` ;
  externe §8.55 `purity_855_external.csv`, SHA-256
  `03f34fe07a18ff106e21ce9028ef9ff60d3d95889c3064898442246e486fbd6f` ;
  externe §8.60 `deconvolution_860_external.csv`, SHA-256
  `438d677aded8eaf74504f8bd89bfc2e578df32b4b31c64e94e64120b0f22d9cf` ;
  écarts §8.44/§8.51/§8.54/§8.55/§8.60 relus en machine
  (`ssep_844_rotations.csv`, `infiltration_854_runs.json`,
  `purity_855_runs.json`, `deconvolution_860_runs.json` ; CD8A : réel
  1,2310, nul 0,2472, écart +0,9838 ; I-RES +0,1982 ; E-RES +0,6499 ;
  D-RES §8.60 +0,7692).
- **Nature des lignes.** Les flux immunitaires sont des mesures
  instrumentales (séquençage ARN, log2(RSEM+1), brutes) ; les scores
  xCell sont des estimations publiées depuis l'ARN (enrichissement ssGSEA
  par signature, compensation de spillover, calibration — Aran et al.
  2017) ; les résidus sont des valeurs calculées (OLS) ; les nuls sont
  des lignes permutées (graine 42) — des échantillons hypothétiques,
  pas des mesures. Aucun mot humain, aucun échantillon hypothétique
  dans les séries réelles. 0 NaN dans MOESM6 — aucune imputation,
  aucune exclusion.
- **Sorties et scripts de ce chantier.**
  `analyze_xcell_868.py` (SHA `68e1b799…6997`) : porte D, jointure,
  vérifications, circularité, T1–T4.
  `build_xcell_868.py` (SHA `9d6b4e7d…697d`) : 8 CSV T5 (résidus
  vérifiés : moyenne |r| = 0,3270, identique à T2(a)).
  `extract_xcell_868.py` (SHA `0e5a4c36…726`) : lecture des 8 runs
  (SHA des CSV vérifiés, version `v6.2.0-L7aL7b-CohenD-short`).
  `data_xcell_868/epmc_5688663_supp.zip`,
  `data_xcell_868/13059_2017_1349_MOESM6_ESM.tsv`,
  `data_xcell_868/13059_2017_1349_MOESM3_ESM.xlsx`,
  `data_xcell_868/13059_2017_1349_MOESM7_ESM.xlsx`,
  `data_xcell_868/xcell_868_attempts.log`,
  `data_xcell_868/analyze_868_stdout.txt`,
  `data_xcell_868/extract_868_stdout.txt`,
  `data_xcell_868/dl_epmc.sh` (téléchargement, unité `xcell-dl-868`).
  `xcell_868_external.csv` (SHA `c58c8184…fe87`, 178 tumeurs : sample,
  64 scores, ImmuneScore §8.54, ABSOLUTE §8.55),
  `xcell_868_results.json` (SHA `2f4f6a40…83fb`, T1–T4 + circularité),
  `xcell_868_results.csv` (SHA `98e8e9a2…0d93`, T1 par type),
  `xcell_868_csv_sha.json` (SHA `6a6052b7…0591`, SHA des 8 CSV T5),
  `xcell_868_runs.json` (SHA `ced59d39…ea127`) / `.csv`
  (SHA `6a6fe3f8…b92a`, 8 runs).
  Manifeste `manifest_v62_xcell_868.txt`
  (SHA `ff64e133…2de0`) ; log `runs_v62_xcell_868.log`
  (SHA `04cda9ed…b74b`) ; unité systemd `v62-xcell-868`.
- **Ce qui manque :** Voie C non utilisée (scores publiés obtenus) ;
  les p de T1 sont brutes, sans correction pour tests multiples (768
  tests) ; pas de ligne ImmuneScore/StromaScore agrégée dans MOESM6 —
  le contrôle §4c par ImmuneScore xCell est impossible sur ce fichier ;
  la concordance CD8 xCell↔CIBERSORT est modérée (r = +0,4405, sous le
  seuil gelé de 0,5) ; les scores xCell sont des enrichissements, pas
  des fractions — un type ne peut pas être lu comme une proportion de
  cellules ; MC ne sépare pas pour D-XTOP1 (−0,0152) ni D-XSTROM
  (−0,1084), nul devant — noté, non utilisé pour le verdict.

## 8.68.10 Ce qui manque, ce qui reste ouvert

- **Fractions ABSOLUES (CIBERSORT absolute mode, EPIC, quanTIseq).**
  Les scores xCell sont des enrichissements, les fractions CIBERSORT
  sont relatives (somme = 1) : ni l'un ni l'autre ne dit si c'est la
  quantité ABSOLUE de cellules dendritiques qui compte — et si M0 est
  vraiment anti-corrélé ou si c'est un artefact de composition (§8.60.11,
  toujours ouvert).
- **Pourquoi les DC ordonnent-elles mieux que CD8A brut ?** D-XTOP2
  (+1,1804) dépasse sa prédiction de +0,3672 et frôle I-IMM (+1,1942) :
  la régression §8.48 sous-prédit systématiquement les contrôles par
  type (déjà +0,18–0,20 au §8.60). Une piste : les scores DC captent
  l'activation immunitaire globale mieux qu'un gène marqueur unique —
  à tester contre l'ImmuneScore lui-même comme contrôle, ou contre une
  combinaison linéaire de types.
- **Séparer la part « type » de la part « quantité totale ».** aDC et
  DC corrèlent à +0,80/+0,81 avec l'ImmuneScore : le porteur partiel
  est aussi le meilleur reflet du global. Un test décisif serait
  d'ordonner par aDC APRÈS régression sur l'ImmuneScore (ou l'inverse)
  — hors protocole gelé, non fait ici.
- **Sous-type moléculaire et état d'activation.** Les 59 % restants
  après les aDC (et le cinquième après l'ImmuneScore) peuvent venir
  d'une variable latente non testée (Bailey / Moffitt / Collisson —
  colonnes détenues dans le sampInfo, non testées ici, autre piste du
  §8.48.8).
- **Survie par type cellulaire.** Les scores joints
  (`xcell_868_external.csv`, n = 178) permettent de tester si un type
  prédit la survie — hors protocole gelé, non fait ici.
- **Incident d'exécution.** Aucun : lot unique, unité systemd
  `v62-xcell-868`, 18:15:27–18:52:21 UTC 20 nov., **8/8 exit 0,
  0 échec, 0 relance** (`=== FIN 2026-11-20T18:52:21Z deja_faits=0
  termines=8 echecs=0 ===` ; 8 lignes `EXIT_` à 0 dans le log).
  Aucun redémarrage machine pendant le lot (uptime 1 h 32 à 18:54).
  Incident de téléchargement (documenté, sans conséquence) : premier
  essai Europe PMC tronqué à 10 396 231 o (timeout 120 s), serveur sans
  support des byte ranges, re-téléchargement complet en unité systemd
  (12 092 617 o, SHA vérifié).
- **Périmètre.** 8 nouveaux runs v6.2 au maximum (protocole §8 :
  6 principaux + 2 stromaux conditionnels — les 2 stromaux lancés, la
  condition gelée étant remplie), aucun autre. Aucun nouveau seuil
  proposé, aucun code modifié, aucun push GitHub dans ce chantier
  (publication sur go séparé ; règle permanente « Toujours github et
  pdf !!! » — par le coordinateur).

— Fin de la §8.68. —
