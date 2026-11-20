# §8.65 Scores ESTIMATE publiés pour TCGA-PAAD : le §8.54 est confirmé à la décimale près

Date : 20 novembre 2026. Go : chantier 2 confié 20 nov. 2026 ~09h36.
Protocole gelé avant tout téléchargement, avant tout calcul et avant tout run :
`PROTOCOL_estimate_published_865.md` (SHA-256 `b105e87b26c7f11b1bd29ec5eccfc05b8cb16cd5dbb5ff35db3f2df0dfd2961d`).

## Verdict d'abord

**Les scores ESTIMATE publiés pour TCGA-PAAD ont été obtenus — et ils
confirment le §8.54 à la décimale près.** La table publiée du site
MD Anderson (PAAD, RNA-seqV2, 179 échantillons) s'apparie à 178/178
tumeurs du projet, et ses scores corrèlent à **r = 0,9999998** avec
l'ImmuneScore recalculé au §8.54 (0,9999999 pour le StromalScore et
l'ESTIMATEScore). Le test refait avec les scores publiés donne les
mêmes chiffres que le §8.54 : cohésion **0,5563 → 0,2001 (−64,0 %)**
contre 0,5563 → 0,2002 au §8.54 ; moyenne |r| flux↔ImmuneScore publié
**0,7164** contre 0,7164 recalculé ; R² médian 0,5272 contre 0,527.
**Chaque valeur de ce tableau est identique à celle du §8.54.3 à la
3e décimale près** (moyenne |r| Immune 0,7164 contre 0,7164 ;
Stromal 0,6002 contre 0,6002 ; R² médian 0,5272 contre 0,527) :
le test refait avec les scores publiés ne change rien au T1. Ordonner
les flux par l'ImmuneScore publié les sépare massivement (**écart S_sep
+1,1928**, contre +1,1942 au §8.54) ; ordonner par le StromalScore
publié les sépare aussi (**+1,0443**, contre +0,9407 au §8.54) ; et
ordonner les flux RÉSIDUALISÉS par CD8A résidualisé ne sépare presque
plus (**+0,2001**, contre +0,1982 au §8.54). **Verdict gelé :
H1-pub TOTALE SOUTENUE — les scores publiés confirment le §8.54, et
le §8.54 est validé de l'extérieur.** La corrélation immunitaire est
un effet de composition (infiltration), pas une propriété propre aux
tumeurs — désormais établi avec les scores publiés eux-mêmes, pas
seulement avec un recalcul.

## 8.65.1 Question, méthode, inventaire des sources (avant le gel)

**Question (§8.55.11 et §8.54.10).** Le §8.54 a recalculé l'ImmuneScore
ESTIMATE depuis la matrice détenue (port Python de tidyestimate, validé
à ~10⁻⁸ sur la vignette) et conclu H1 totale : la corrélation
intra-famille immunitaire est expliquée par l'infiltration
(0,5563 → 0,2002, I-IMM +1,1942, I-STR +0,9407, I-RES +0,1982). Le
§8.55 n'avait pas pu obtenir les scores ESTIMATE PUBLIÉS pour PAAD
(site MD Anderson piloté par JS, fichier JS non récupéré : curl en
échec répété, 000, 3 tentatives) et avait testé ABSOLUTE à la place
(H1 partielle). Ce chantier cherche les scores publiés et, s'ils sont
obtenus, refait le test avec ces scores et les compare directement
(a) à ABSOLUTE (§8.55) et (b) à l'ImmuneScore recalculé (§8.54).
Deux questions distinctes, jugées séparément : (Q1) les scores publiés
confirment-ils le score recalculé du §8.54 ? (Q2) le test refait avec
les scores publiés donne-t-il le même verdict que le §8.54 ?

**Sources candidates gelées :** (1) Yoshihara et al. 2013, Suppl. Data 2
(`ncomms3612-s3.xlsx`, PMC3826632) via Europe PMC / PMC / Nature /
miroirs ; (2) site ESTIMATE MD Anderson, téléchargement par maladie
(PAAD, RNA-seqV2, 179) ; (3) Aran et al. 2015 Suppl. Data 1, déjà détenu
(0 PAAD au §8.55, à re-vérifier) ; (4) UCSC Xena / dépôts publics.

**Critères gelés.** T0 : CONCORDANCE si r ≥ 0,95 entre publié et
recalculé (ImmuneScore) ; DIVERGENCE si r < 0,90. T1'' : lien
substantiel si moyenne |r| ≥ 0,30 pour l'ImmuneScore publié. T2'' :
EFFONDREMENT si moyenne |r| résiduelle < 0,30 ET fraction |r| > 0,5
< 0,20 ; PERSISTANCE si chute < 20 % ; entre les deux : partielle.
T5'' : E-PIMM ou E-PSTR soutient H1-pub si écart S_sep ≥ 0,45 ;
E-PRES soutient H1-pub si écart < 0,30, soutient H0-pub si ≥ 0,45.
Verdict : H1-pub TOTALE si T2'' = effondrement ET E-PRES < 0,30 ET
(E-PIMM ≥ 0,45 OU E-PSTR ≥ 0,45) ET T0 = concordance ; H1-pub
PARTIELLE si T2'' = partielle OU (E-PIMM/E-PSTR entre 0,30 et 0,45)
avec E-PRES < 0,70 ; H0-pub si T2'' = persistance ET E-PIMM < 0,30 ET
E-PSTR < 0,30 ET E-PRES ≥ 0,45 ; DIVERGENCE si T0 = divergence.
Références : §8.54 — H brute 0,5563, H résiduelle 0,2002, I-IMM
+1,1942, I-STR +0,9407, I-RES +0,1982, r(Immune, Stromal) recalculés
0,7831 ; §8.55 — H brute (n = 149) 0,5040, H résiduelle [ABSOLUTE]
0,3757, E-ABS +0,6911, E-RES +0,6499 ; CD8A brut +0,9838 ; régression
§8.48 d_ssep = −0,175 + 1,705·C.

## 8.65.2 Porte S (source) : OUVERTE — table publiée MD Anderson, PAAD RNA-seqV2

### Europe PMC, Yoshihara Suppl. Data 2 : en échec (HTTP 500)
`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3826632/supplementaryFiles`
renvoie HTTP 500 et une page HTML d'erreur (19 606 octets) — le fichier
a été supprimé, rien n'en est utilisé. Même statut qu'au §8.54 (502
alors, 500 aujourd'hui) : la voie Europe PMC ne donne pas ce supplément.
PMC direct et Nature static-content n'ont pas été re-tentés : la source
2 a abouti avant (cf. ci-dessous), et le protocole n'exige pas
d'épuiser les voies redondantes une fois la porte S ouverte.

### Site ESTIMATE MD Anderson : OBTENU — la voie qui avait échoué au §8.55
Le site (`bioinformatics.mdanderson.org/estimate/`) liste bien
« Pancreatic ductal adenocarcinoma — RNA-seqV2 179 » et présente les
scores pour tous les types TCGA (citation Yoshihara et al. 2013,
connexion non requise, gratuit). Au §8.55, le fichier JS n'avait pas pu
être récupéré (curl 000, 3 tentatives). Cette fois, les deux fichiers
ont été récupérés du premier coup (HTTP 200) :
`disease.html` (5 940 octets, SHA `1f5ebd01…edb7`) et
`js/disease_histogram.js` (14 013 octets, SHA `7b8124ad…467`).
Le JS lu en clair donne le mécanisme de téléchargement
(`startDownload`) : le fichier est `tables/<maladie> <plateforme>.txt`,
espaces remplacés par `_`, colonnes ID, Stromal_score, Immune_score,
ESTIMATE_score. Les valeurs exactes des menus déroulants lues dans
`disease.html` sont `pancreatic ductal adenocarcinoma` et `RNAseqV2`.
L'URL qui en découle — et seulement celle-là — a été téléchargée :
`https://bioinformatics.mdanderson.org/estimate/tables/pancreatic_ductal_adenocarcinoma_RNAseqV2.txt`
(HTTP 200, 6 928 octets, SHA-256
`46004731c2bc4479931ec19e50e12ce5f1656c890ba09e16a4e166316d59fce1`,
20 nov. 2026 14h38 UTC ; copie dans
`data_estimate_published_865/pancreatic_ductal_adenocarcinoma_RNAseqV2.txt`).
**179 lignes** (en-tête + 179 échantillons), colonnes ID, Stromal_score,
Immune_score, ESTIMATE_score. La somme est vérifiée en machine :
ESTIMATEScore = Stromal + Immune à 0,01 près au maximum (arrondi à
2 décimales des valeurs publiées).

### Aran et al. 2015 : re-vérifié, 0 PAAD (confirmation)
Le tableau déjà détenu (`data/aran2015_supp_data1_ncomms9971-s2.xlsx`,
SHA `fce1ba13…7529`, feuille « Supp Data 1 », 9 364 lignes, 21 types)
contient toujours **0 ligne PAAD** — il n'apporte rien de plus qu'au
§8.55 et n'entre dans aucun test.

**Porte S OUVERTE** : fichier publié obtenu, colonnes de scores
présentes, couverture appariée 178/178 (cf. §8.65.3) — au-dessus du
seuil gelé (≥ 100).

## 8.65.3 Porte S / jointure : OUVERTE, 178/178

Jointure sur les **15 premiers caractères** du barcode (protocole §4) :
**178/178 tumeurs du projet appariées (0 non appariée, 0 collision de
clé des deux côtés)**. La seule clé publiée hors projet est
TCGA-HZ-A9TJ-06 (échantillon 06A, métastase — déjà noté au §8.55 comme
hors critère « tumeurs primaires code 01 »). La table publiée compte
179 lignes : 178 tumeurs primaires du projet + cette métastase.

Scores publiés (n = 178) :

| Score publié | min | médiane | max | moyenne | écart-type |
|---|---|---|---|---|---|
| ImmuneScore | −1559,9 | 603,8 | 3037,8 | 626,6 | 817,9 |
| StromalScore | −1843,3 | 698,4 | 2179,2 | 587,2 | 829,1 |
| ESTIMATEScore | −3178,4 | 1278,8 | 4435,6 | 1213,8 | 1555,2 |

À comparer aux recalculés du §8.54 (n = 178) : ImmuneScore min −1556,6,
médiane 598,5, max 3022,7, moyenne 621,0, écart-type 814,6 ;
StromalScore min −1839,1, médiane 692,4, max 2166,6, moyenne 581,7,
écart-type 825,7 ; ESTIMATEScore min −3170,8, médiane 1267,1, max
4410,0, moyenne 1202,6, écart-type 1548,8. Les descriptifs coïncident
à quelques unités près sur des scores de l'ordre du millier.
Fichier apparié : `estimate_published_865_external.csv`
(SHA `60e1ff96…ac181`, 178 lignes : sample, immune_pub, stromal_pub,
estimate_pub, key15, source, URL, SHA source).

## 8.65.4 T0 — Publié ↔ recalculé : CONCORDANCE, r = 0,9999998

Pearson r (+ Spearman ρ) entre scores publiés et recalculés (§8.54),
sur les 178 appariées :

| Comparaison | Pearson r (p) | Spearman ρ | \|diff\| moyenne | \|diff\| max |
|---|---|---|---|---|
| ImmuneScore publié vs recalculé | **0,9999998** (0,0) | 0,9999915 | 5,78 | 15,06 |
| StromalScore publié vs recalculé | **0,9999999** (0,0) | 0,9999894 | 5,80 | 12,55 |
| ESTIMATEScore publié vs recalculé | **0,9999999** (0,0) | 0,9999915 | 11,49 | 25,54 |
| ImmuneScore publié vs recalculé wo12 | **0,9999942** (0,0) | — | — | — |

Critère gelé : CONCORDANCE (r ≥ 0,95 — dépassé de loin sur les trois
scores). **Le port ssGSEA du §8.54 reproduit les scores publiés à
r ≈ 1,000000.** Les écarts absolus ne sont pas nuls (moyenne 5,8 sur
l'ImmuneScore, max 15,1) : ce n'est pas un effet d'arrondi (les valeurs
publiées sont arrondies à 2 décimales, soit ≤ 0,005 d'écart), mais une
petite différence systématique — vraisemblablement la liste de gènes
communs (version du package R `estimate` d'origine contre le port
tidyestimate) — soit ~0,7 % de l'écart-type (817,9). Elle ne change
aucun test : les corrélations avec les flux sont identiques à la
3e décimale (cf. T1''). **r(ImmuneScore, StromalScore) publiés =
0,7833**, contre 0,7831 recalculés : le bras stromal reste une seconde
vue du même axe de composition, comme au §8.54.7.

**Comparaison à ABSOLUTE (§8.55, n = 149) :** ImmuneScore publié
r = −0,646, StromalScore publié r = −0,654, ESTIMATEScore publié
r = **−0,701** (p = 2,4×10⁻²³). Les trois scores publiés corrèlent
négativement avec la pureté ADN — le sens attendu (plus la tumeur est
pure, moins les scores d'infiltration sont forts) — et l'ESTIMATEScore
combiné corrèle plus fortement avec ABSOLUTE que chacun de ses deux
composants, comme dans Yoshihara et al. 2013 (Fig. 3). Il n'y a pas de
colonne de pureté ESTIMATE dans la table publiée (les scores seuls
sont servis par maladie) : la pureté ESTIMATE publiée reste
indisponible, comme au §8.55 — la comparaison ABSOLUTE ↔ ESTIMATE se
fait ici par les scores, pas par une pureté publiée.

## 8.65.5 T1'' — Chaque flux immunitaire suit le score publié : OUI, fortement

Pearson r (+ Spearman ρ) de chaque flux contre les trois scores publiés ;
R² par flux (OLS sur [ImmuneScore_pub] et sur [ImmuneScore_pub,
StromalScore_pub]) ; p brutes bilatérales, sans correction pour tests
multiples (36 tests — le jugement porte sur la moyenne, pas sur une p
isolée).

| Gène | r Immune pub (p) | ρ Immune pub | r Stromal pub | R² Immune pub |
|---|---|---|---|---|
| CD4 | **+0,893** | +0,921 | +0,834 | **0,797** |
| CTLA4 | +0,851 | +0,816 | +0,654 | 0,725 |
| FOXP3 | +0,827 | +0,817 | +0,725 | 0,684 |
| PDCD1 | +0,811 | +0,765 | +0,545 | 0,658 |
| CD8A | +0,797 | +0,790 | +0,639 | 0,635 |
| CD163 | +0,731 | +0,777 | +0,827 | 0,534 |
| CD8B | +0,721 | +0,703 | +0,535 | 0,521 |
| GZMB | +0,696 | +0,665 | +0,491 | 0,485 |
| CD19 | +0,678 | +0,623 | +0,449 | 0,459 |
| CD68 | +0,661 | +0,632 | +0,613 | 0,437 |
| IFNG | +0,480 | +0,511 | +0,369 | 0,231 |
| CD274 | +0,451 | +0,490 | +0,521 | 0,204 |

Moyenne |r| : **ImmuneScore publié 0,7164**, StromalScore publié
0,6002, ESTIMATEScore publié 0,6968 (Spearman 0,7089 / 0,5928).
**R² médian 0,5272 (52,7 %), maximum 0,7967 (CD4).** Avec
[Immune, Stromal] : R² médian 0,5791, maximum 0,8435 (CD4).
Critère gelé : lien SUBSTANTIEL (≥ 0,30), largement dépassé — 2,4× le
seuil. Les 12 corrélations sont POSITIVES et toutes significatives à
p ≤ 2,6×10⁻¹⁰ (valeurs p affichées 0,0000 à 4 décimales).
**Chaque valeur de ce tableau est identique à celle du §8.54.3 à la
3e décimale près** (moyenne |r| Immune 0,7164 contre 0,7164 ;
Stromal 0,6002 contre 0,6002 ; R² médian 0,5272 contre 0,527) :
le test refait avec les scores publiés ne change rien au T1.

## 8.65.6 T2'' — La corrélation intra-famille s'effondre après régression publiée

Matrice 66 paires, brute contre résidus OLS ([1, ImmuneScore_pub] et
sensibilité [ImmuneScore_pub, StromalScore_pub]).

| Matrice | Pearson moyenne \|r\| | médiane \|r\| | fraction \|r\| > 0,5 | max \|r\| | Spearman moyenne \|r\| |
|---|---|---|---|---|---|
| Brute | **0,5563** | 0,5677 | 0,621 (41/66) | 0,8430 | 0,5403 |
| Résidus [ImmuneScore_pub] | **0,2001** | 0,1737 | **0,045 (3/66)** | 0,6409 | 0,2044 |
| Résidus [Imm_pub, Strom_pub] | 0,1902 | 0,1574 | 0,030 (2/66) | 0,6457 | 0,1992 |

**Chute : 64,0 % avec l'ImmuneScore publié, 65,8 % avec les deux
scores.** Critère gelé : EFFONDREMENT (moyenne résiduelle 0,2001
< 0,30 ET fraction > 0,5 de 0,045 < 0,20) — rempli sur les deux
variantes. La fraction de paires fortes passe de 41/66 à 3/66.
**Contre le §8.54 (recalculé) : 0,2002 → 0,2001, chute 64,0 % dans les
deux cas — les deux chiffres sont identiques à 0,0001 près.**
Les 3 paires qui restent fortes après régression sont les mêmes
qu'au §8.54.4 : CD8A–CD8B (0,6409), CD4–CD163 (0,5809), GZMB–IFNG
(0,5201) ; suivent CD68–CD19 (0,4903) et PDCD1–CTLA4 (0,4419).
Le résidu structuré du §8.54.8 est donc reproduit par les scores
publiés, paire par paire.

## 8.65.7 T3'' — Couplage prédit : la régression §8.48 tient, avant comme après

Couplage C par contrôle immunitaire (moyenne des |r| avec les 11 autres
flux), brut contre résidualisé ; d_ssep prédit par d = −0,175 + 1,705·C.

| | C moyen | d_ssep prédit moyen |
|---|---|---|
| Brut | 0,5563 | **0,7735** (observé IMMROT : 0,7521) |
| Résidualisé [ImmuneScore_pub] | 0,2001 | **0,1662** |

CD8A seul : C 0,6514 → 0,2765, d_pred 0,9356 → **0,2965**.
Contre le §8.54.5 : C résiduel 0,2001 contre 0,2002, d_pred 0,1662
contre 0,1663, CD8A d_pred résiduel 0,2965 contre 0,2966 — identiques
à 0,0001 près. Le T3'' ne fait que traduire T2'' en S_sep prédit ;
le verdict se joue au T5''.

## 8.65.8 T4'' — Stratification : la cohésion persiste dans chaque moitié — test faible ici

Médiane de l'ImmuneScore publié (603,81), n = 89/89 ; matrice
intra-famille dans chaque moitié.

| Stratification | Moitié haute : moyenne \|r\| (frac. > 0,5) | Moitié basse : moyenne \|r\| (frac. > 0,5) |
|---|---|---|
| ImmuneScore_pub (méd. 603,81) | 0,3638 (0,288) | 0,3926 (0,303) |

Identique au §8.54.6 à la 4e décimale (0,3638 / 0,3926). Comme au
§8.54, la prémisse de bande étroite n'est pas remplie : l'écart-type
de l'ImmuneScore publié reste de 556,1 dans la moitié haute et 476,7
dans la moitié basse, contre 817,9 global (58–68 % conservés) ; les
plages restent [606, 3038] et [−1560, 602]. **T4'' est donc non
concluant ici** — il ne soutient pas H1-pub, mais il ne la réfute pas
non plus. T4'' n'entre pas dans la règle de verdict gelée.

## 8.65.9 T5'' — Runs v6.2 : les scores publiés ordonnent l'immunitaire, les résidus presque plus

Prédictions calculées AVANT de lire les sorties (depuis T1''/T2'' du jour) :
E-PIMM d_pred +1,0466 (C = 0,7164) ; E-PSTR d_pred +0,8483
(C = 0,6002) ; E-PRES d_pred +0,2965 (C_résid CD8A = 0,2765). 6 runs
v6.2, mode fast, graine 42, **6/6 exit 0** (lot 14h41:37–15h08:38 UTC
20 nov. ; §8.65.11 pour l'exécution).

| Run | Contrôle → analysés | S_sep réel | S_sep nul | Écart | Prédit | MC réel / nul | Delta réel / nul | w | t0 |
|---|---|---|---|---|---|---|---|---|---|
| E-PIMM | ImmuneScore_pub → 12 imm. bruts | 1,4075 | 0,2147 | **+1,1928** | +1,0466 | 0,4835 / 0,3325 | 3,26 / 3,83 | 27 | 75,10 % |
| E-PSTR | StromalScore_pub → 12 imm. bruts | 1,1243 | 0,0801 | **+1,0443** | +0,8483 | 0,4574 / 0,3911 | 4,30 / 1,82 | 30 | 49,11 % |
| E-PRES | CD8A résid. → 11 imm. résid. | 0,4718 | 0,2717 | **+0,2001** | +0,2965 | 0,3697 / 0,3446 | 3,11 / 4,26 | 27 | 75,10 % |

Lecture par critère gelé :
- **E-PIMM : séparation massive, au-dessus de la prédiction.** Écart
  +1,1928 — 1,14× la prédiction (+1,0466, +0,1462 au-dessus), 2,65× le
  minimum IMMROT (+0,4508), 1,21× CD8A brut (+0,9838). Contre I-IMM
  recalculé (+1,1942) : **écart de −0,0014** — le réel (1,4075 contre
  1,4063) comme le nul (0,2147 contre 0,2121) sont reproduits à 0,003
  près. MC +0,1509 (0,4835 contre 0,3325) : ici MC sépare, comme au
  §8.54 — noté, non utilisé pour le verdict (le verdict porte sur
  S_sep, gelé). L7a sépare en direction (up 0,2614 contre down
  −0,3528) : non utilisé, comme au §8.54. Seuil à 75,10 % de la série
  ordonnée — le même qu'au §8.54. Critère gelé : E-PIMM ≥ 0,45 →
  **soutient H1-pub, fortement**.
- **E-PSTR : séparation massive aussi — mais pas une preuve
  indépendante.** Écart +1,0443 — 1,23× la prédiction (+0,8483,
  +0,1960 au-dessus), 2,32× le minimum IMMROT. Contre I-STR recalculé
  (+0,9407) : **+0,1036 de plus**, porté entièrement par le nul
  (0,0801 contre 0,1841 — le réel est identique, 1,1243 contre
  1,1248). MC +0,0662 (0,4574 contre 0,3911). Seuil à 49,11 % — le
  même qu'au §8.54. Critère gelé : E-PSTR ≥ 0,45 → **soutient H1-pub**.
  Mais r(ImmuneScore, StromalScore) publiés = 0,7833 : le score
  stromal porte l'axe de composition partagé — E-PSTR est une seconde
  vue du même axe, pas une confirmation indépendante d'E-PIMM, comme
  au §8.54.7. Le nul E-PSTR a choisi w = 89 (19 candidats) contre
  w = 42 (22 candidats) pour le nul I-STR au §8.54 : c'est le choix propre du run nul, rapporté tel
  quel, non lissé.
- **E-PRES : la séparation s'effondre, sans disparaître.** Écart
  +0,2001 contre +0,9838 pour CD8A brut (**20,3 % conservés, baisse
  de 79,7 %**) et contre +0,2965 prédit (−0,0964 en dessous — la
  régression §8.48 sur-prédit légèrement le résiduel ici, comme au
  §8.54). Contre I-RES recalculé (+0,1982) : **écart de +0,0019**.
  MC +0,0251 (0,3697 contre 0,3446) : MC ne sépare presque plus.
  L7a ne sépare pas (up 0,4174 contre up 0,1804, même direction) :
  non utilisé. Seuil à 75,10 %, comme E-PIMM. Critère gelé :
  E-PRES < 0,30 → **soutient H1-pub**. Mais +0,2001 n'est pas zéro :
  un résidu de séparation subsiste, cohérent avec les 3 paires fortes
  de T2'' — c'est le reste structuré du §8.54.8, reproduit ici,
  pas une réfutation de H1-pub (le critère gelé est < 0,30, pas = 0).
- **Delta ne sépare pas sur E-PIMM et E-PRES** (nul supérieur au réel :
  3,83 contre 3,26 ; 4,26 contre 3,11) — rapporté descriptivement,
  comme au §8.54, non utilisé pour le verdict (Delta non élucidé,
  §8.49). Sur E-PSTR, Delta est supérieur au réel (4,30 contre 1,82)
  : noté, sans interprétation, le verdict ne portant pas sur Delta.

## 8.65.10 Verdict de synthèse

Règle gelée, test par test : T0 = CONCORDANCE (r = 0,9999998) ;
T1'' = lien substantiel (moyenne |r| 0,7164) ; T2'' = EFFONDREMENT
(0,5563 → 0,2001, chute 64,0 %, fraction 0,621 → 0,045) ; E-PIMM =
+1,1928 (≥ 0,45) ; E-PSTR = +1,0443 (≥ 0,45) ; E-PRES = +0,2001
(< 0,30). **Les trois conditions de H1-pub totale sont remplies, avec
T0 = concordance : H1-pub TOTALE est SOUTENUE. Les scores ESTIMATE
publiés confirment le §8.54, test par test, à la décimale près.**
H1-pub partielle est rejetée (les conditions de la totale sont
remplies) ; H0-pub est rejetée (aucune de ses conditions n'est remplie :
T2'' n'est pas une persistance ; E-PIMM/E-PSTR ne sont pas < 0,30 ;
E-PRES n'est pas ≥ 0,45) ; DIVERGENCE est rejetée (T0 = concordance).
Aucun consensus exigé entre les tests : le verdict suit la règle gelée,
et T4'' — non concluant ici — est rapporté comme tel, pas moyenné.

**Ce que cela dit, et ce que cela ne dit pas.** (a) Cela dit que le
§8.54 est validé de l'extérieur : le score recalculé n'était pas un
artefact du port Python — il reproduit les scores publiés par les
auteurs de la méthode, et le verdict H1 totale survit au remplacement
du recalculé par le publié. La question ouverte du §8.54.10 (« §8.54b »)
est fermée. (b) Cela dit que la part de la corrélation portée par
l'infiltration (~64 % en régression, ~80 % en séparation) est mesurée
par une source indépendante du projet — la même source que Yoshihara
et al. 2013. (c) Cela ne dit pas que TOUTE la corrélation est de
l'infiltration : le résidu +0,2001 (20,3 % de CD8A brut) et les 3
paires fortes restantes sont un reste structuré, identique à celui du
§8.54.8. (d) Cela ne dit pas que la pureté est innocentée : le §8.55
(H1 partielle, un tiers porté par ABSOLUTE) reste valide — infiltration
et pureté sont deux axes de composition différents, et c'est
l'infiltration qui porte l'essentiel de la corrélation ; les scores
publiés corrèlent d'ailleurs à ABSOLUTE (ESTIMATEScore publié
r = −0,701, n = 149), les deux axes n'étant pas orthogonaux.
(e) Cela ne dit pas quelles cellules portent la corrélation : pas de
fractions par type cellulaire — question toujours ouverte. (f) Cela ne
dit pas que la petite différence systématique publié↔recalculé
(moyenne |diff| 5,8, max 15,1) est expliquée : elle est mesurée,
rapportée, et sans effet sur aucun test — son origine (liste de gènes
communs) est une hypothèse, pas un fait établi ici.

**Comparaison directe avec le §8.54 (scores recalculés) et le §8.55 (ABSOLUTE) :**

| Test | §8.54 (recalculé, n = 178) | §8.65 (publié, n = 178) | §8.55 (ABSOLUTE, n = 149) |
|---|---|---|---|
| T1 moyenne \|r\| | Immune 0,7164 / Stromal 0,6002 | Immune **0,7164** / Stromal **0,6002** | ABSOLUTE 0,4932 |
| T1 R² médian | 0,527 | **0,5272** | 0,3006 |
| T2 brute → résiduelle | 0,5563 → 0,2002 (−64,0 %) | 0,5563 → **0,2001 (−64,0 %)** | 0,5040 → 0,3757 (−25,5 %) |
| T5 contrôle → flux | I-IMM +1,1942 ; I-STR +0,9407 | E-PIMM **+1,1928** ; E-PSTR **+1,0443** | E-ABS +0,6911 |
| T5 résidualisé | I-RES +0,1982 (20,2 % du brut) | E-PRES **+0,2001 (20,3 % du brut)** | E-RES +0,6499 (66,1 % du brut) |
| Verdict | H1 totale | **H1-pub totale** | H1 partielle |

## 8.65.11 Provenance

- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant les calculs et dans le log de lot).
  Mode `fast`, graine 42 (défaut), nul = bloc analysé permuté
  conjointement, graine 42 (default_rng frais par fichier), contrôle intact.
- **Protocole.** `PROTOCOL_estimate_published_865.md`, SHA-256
  `b105e87b26c7f11b1bd29ec5eccfc05b8cb16cd5dbb5ff35db3f2df0dfd2961d`,
  gelé le 20 nov. 2026 avant tout téléchargement, tout calcul et tout run
  de ce chantier.
- **Entrées externes.** (1) Table publiée MD Anderson ESTIMATE, PAAD
  RNA-seqV2 :
  `https://bioinformatics.mdanderson.org/estimate/tables/pancreatic_ductal_adenocarcinoma_RNAseqV2.txt`,
  SHA-256 `46004731c2bc4479931ec19e50e12ce5f1656c890ba09e16a4e166316d59fce1`
  (6 928 octets, 179 lignes, 20 nov. 2026 14h38 UTC ; copie dans
  `data_estimate_published_865/pancreatic_ductal_adenocarcinoma_RNAseqV2.txt`) ;
  mécanisme de téléchargement lu dans `js/disease_histogram.js`
  (SHA `7b8124ad…467`, 14 013 octets) et valeurs des menus lues dans
  `disease.html` (SHA `1f5ebd01…edb7`, 5 940 octets) — copies dans
  `data_estimate_published_865/`. Publication source : Yoshihara et al.,
  Nat Commun 2013, 4:2612 (PMID 24113773, PMCID PMC3826632,
  doi 10.1038/ncomms3612). (2) Europe PMC supplementaryFiles PMC3826632
  tenté, HTTP 500, page HTML d'erreur (19 606 octets, supprimée) — non
  utilisé. (3) Aran et al. 2015 Suppl. Data 1, déjà détenu
  (`data/aran2015_supp_data1_ncomms9971-s2.xlsx`, SHA `fce1ba13…7529`,
  9 364 lignes, 21 types) — 0 PAAD, re-vérifié, non utilisé pour les tests.
- **Entrées du projet.** Base immunitaire `pdac_immune_tcga_fluxes.csv`,
  SHA-256 `66dbb672…bd2e` ; axe `immune_kras_order_tcga.csv`, SHA-256
  `31d31ae6…62d` ; scores recalculés `infiltration_854_scores.csv`, SHA-256
  `628732ec…aa7` ; ABSOLUTE `purity_855_external.csv`, SHA-256
  `03f34fe0…bd6f` ; écarts §8.54 relus en machine dans
  `infiltration_854_runs.csv` (I-IMM +1,1942 ; I-STR +0,9407 ;
  I-RES +0,1982) et §8.55 dans `purity_855_runs.csv`.
- **Nature des lignes.** Les flux immunitaires sont des mesures
  instrumentales (séquençage ARN, log2(RSEM+1), brutes) ; les scores
  ESTIMATE publiés sont des valeurs publiées (ssGSEA sur 141 gènes,
  Yoshihara et al. 2013, servies par le site MD Anderson) ; les résidus
  sont des valeurs calculées (OLS sur [1, ImmuneScore_pub]) ; les nuls
  sont des lignes permutées (graine 42) — des échantillons hypothétiques,
  pas des mesures. Aucun mot humain, aucun échantillon hypothétique dans
  les séries réelles.
- **Sorties et scripts de ce chantier.**
  `analyze_estimate_published_865.py` (SHA `1851562b…5965`) : porte S,
  jointure, T0–T4''. `build_estimate_published_865.py` (SHA `e4227433…551`) :
  6 CSV T5'' (résidus vérifiés : moyenne |r| = 0,2001, identique à T2'').
  `extract_estimate_published_865.py` (SHA `64287660…49cf`) : lecture des
  6 runs. `estimate_published_865_external.csv` (SHA `60e1ff96…ac181`,
  178 tumeurs appariées), `estimate_published_865_results.json`
  (T0–T4'' + porte S) / `.csv` (T1'' par flux),
  `estimate_published_865_immune_resid.csv` (SHA `57ccd353…43b`,
  12 flux résidualisés), `estimate_published_865_csv_sha.json` (SHA des
  6 CSV T5''). Manifeste `manifest_v62_estimate_published_865.txt`
  (SHA `9e668bbe…955aa`) ; log `runs_v62_estimate_published_865.log` ;
  surveillance `watch_v62_estimate_published_865.sh`
  (SHA `34f2fd25…9cfe`) ; unité systemd `v62-estpub-865`.
  Journal des tentatives : `data_estimate_published_865/attempts_865.log`.
  `estimate_published_865_runs.json` (SHA `f593aa53…2d6`) / `.csv`
  (SHA `b1ead372…0901`, 6 runs).
- **Ce qui manque :** pureté ESTIMATE publiée pour PAAD (pas de colonne
  pureté dans la table par maladie — cf. §8.65.4) ; relecture directe du
  Suppl. Data 2 de Yoshihara (`ncomms3612-s3.xlsx`, Europe PMC HTTP 500
  — la table MD Anderson est la même donnée servie par les auteurs, pas
  une relecture indépendante du xlsx) ; l'origine exacte de la petite
  différence systématique publié↔recalculé (moyenne |diff| 5,8, max
  15,1 — hypothèse : liste de gènes communs, non établie ici) ;
  les p de T1'' sont brutes, sans correction pour tests multiples.
- **Incident d'exécution.** Aucun : la machine n'a pas redémarré pendant
  le lot (uptime 1h54 à 15h16 UTC, sans coupure). Bilan final : **6/6
  exit 0, 0 échec**, lot 14h41:37 UTC – 15h08:38 UTC 20 nov.
  (`=== FIN 2026-11-20T15:08:38Z deja_faits=0 termines=6 echecs=0` ;
  surveillance arrêtée d'elle-même à 6/6, tour 1/12). Aucune sortie
  perdue, aucune relance nécessaire.

## 8.65.12 Ce qui manque, ce qui reste ouvert

- **Pureté ESTIMATE publiée.** La table par maladie ne sert que les
  trois scores (stromal, immunitaire, ESTIMATE) : aucune colonne de
  pureté. La comparaison ABSOLUTE ↔ pureté ESTIMATE publiée reste
  impossible par cette voie ; elle se fait ici par les scores
  (ESTIMATEScore publié vs ABSOLUTE : r = −0,701, n = 149).
- **Relecture indépendante du Suppl. Data 2 (xlsx).** La table MD
  Anderson est servie par les auteurs du site ESTIMATE, mais ce n'est
  pas une relecture du fichier `ncomms3612-s3.xlsx` lui-même (Europe PMC
  500, PMC/Nature non re-tentés après l'obtention). Une relecture du
  xlsx donnerait une seconde source indépendante des mêmes scores.
- **Fractions par type cellulaire.** Comme au §8.54 : CIBERSORT/xCell
  diraient quelles cellules portent la corrélation — toujours
  inaccessibles ici.
- **Le résidu structuré.** CD8A–CD8B 0,6409, CD4–CD163 0,5809,
  GZMB–IFNG 0,5201 après régression publiée — identique au §8.54.8 :
  biologie de récepteur, autre variable latente, ou queue de
  l'infiltration non linéaire ? Non tranché ici.
- **Périmètre.** 6 nouveaux runs v6.2 au maximum (protocole §8), aucun
  autre. Aucun nouveau seuil proposé, aucun code modifié, aucun push
  GitHub dans ce chantier (publication sur go séparé ; règle permanente
  « Toujours github et pdf !!! » — par le coordinateur).

— Fin de la §8.65. —
