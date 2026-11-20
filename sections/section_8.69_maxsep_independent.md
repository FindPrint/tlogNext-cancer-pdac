# §8.69 — Confirmation indépendante pour `maxsep` (C3) : la paire GSE21501 ne sépare pas

## Verdict d'abord

**NON — la paire principale indépendante GSE21501 ne sépare pas :
`d_maxsep = −0,0100` (négatif, quasi nul), très loin sous le plancher
0,07. A2 étendu : 6/9 au-dessus du plancher, 7/9 positifs — la condition
C3 du §8.59.8 n'est PAS levée. L'adoption pleine de `maxsep`, décidée
par Zackary le 20 nov. 2026 à 13h04, reste sa décision : ce chantier
ne la rouvre pas et ne la conditionne pas. La confirmation
indépendante reste ouverte — à trouver ailleurs, ou à ne pas trouver.**

| Porte (PROTOCOL_maxsep_independent_869.md §7, gelé) | Exigé | Mesuré 20 nov. 2026 | Sort |
|---|---|---|---|
| Paire indépendante : `d_maxsep > 0,07` et positif | > 0,07 | **−0,0100** (réel 0,2121, nul 0,2221) | **ÉCHOUE** |
| A2 étendu (9 paires) | 7/9 et 8/9 positifs | **6/9, 7/9 positifs** | **ÉCHOUE** |
| LOO sur 9 paires (descriptif) | Retrait d'une paire passante : 6/8 | **5/8** après retrait de chaque paire passante | **ÉCHOUE** |
| Exactitude de l'extraction | 2/2 à 0,0 exact | **2/2, écart max 0,0** | **PASSE** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que la
neuvième paire principale, mesurée aujourd'hui sur une cohorte
jamais utilisée dans ce projet, ne sépare pas le réel du nul en
`maxsep` — elle est même légèrement négative, comme GSE62452
(−0,0036), l'autre paire négative du dossier. Il ne dit pas que
`maxsep` est un mauvais score : les 8 paires V1 gardent leurs
valeurs (6/8, 7/8 positifs), les rotations 37/48, HP35 +1,6512 —
rien de tout cela n'est rouvert ici. Il ne dit pas non plus que
l'adoption pleine est annulée : elle a été décidée par Zackary
après lecture des §8.56/§8.59/§8.64, et cette section est une
vérification a posteriori, pas une condition — comme le protocole
le dit depuis son §0. Ce qu'il dit, plainement : **la confirmation
indépendante attendue par C3 n'existe pas ce soir**, et l'étiquette
« provisoire » aurait donc tenu si l'adoption n'avait pas déjà été
décidée pleine par Zackary. Les deux faits coexistent : adoption
pleine décidée, confirmation ouverte. Aucun des deux n'efface
l'autre.

**Fragilité, dite en tête.** Le verdict tient à une seule paire
mesurée aujourd'hui — comme tous les verdicts de ce dossier
tiennent à une paire près. La paire n'est pas « presque passante » :
−0,0100 est à 0,0800 du plancher, dans le mauvais sens. Ce n'est
pas un échec de justesse, c'est un nul quasi exact entre réel et
nul (0,2121 contre 0,2221). En revanche, Delta favorise
fortement le réel (+2,01) sur cette même paire, et L7a change de
sens (UP réel 0,16, DOWN nul 0,37) — deux lectures descriptives
qui vont dans l'autre sens que `maxsep` et qui sont rapportées
telles quelles au §8.69.5, sans sauver ni condamner le verdict :
le critère gelé est `maxsep`, et lui seul.

Protocole gelé : `PROTOCOL_maxsep_independent_869.md` (20 nov.
2026, SHA `86c239b4…e61a52` au gel ; fichier actuel SHA
`be0a02ca…e2e8ab9`, corps gelé inchangé, addendum « cohorte #3 »
ajouté après les deux échecs de portes — voir §8.69.4). Critère
de passage écrit AVANT tout run (§7 du protocole) ; aucune
repondération, aucun nouveau terme, aucune redéfinition du
plancher après avoir vu les chiffres. Les nombres des §8.56/§8.59/
§8.64 étaient la motivation, pas le verdict : le verdict repose
sur les 2 runs mesurés ci-dessous.

## 8.69.1 — La paire mesurée : GSE21501, et pourquoi elle est indépendante

**Cohorte : GSE21501, NCBI GEO** — Stratford et coll., 102
patients PDAC avec données cliniques + 30 échantillons
Nebraska/UNC sans données cliniques, plateforme Agilent GPL4133,
article Stratford et coll. 2010 (*PLoS Medicine*, PMID 20644708).
Provenance complète : `PROVENANCE_869.md`.

**Indépendance, en quatre points (protocole §2, addendum).**
1. **Jamais utilisée dans ce projet.** Aucun CSV de flux, aucun
   run, aucun JSON, aucune valeur `maxsep` n'existait pour
   GSE21501 avant ce chantier. Vérifié par grep avant le gel :
   seules mentions = enquête §8.66 §1.3 (écartée pour son stade,
   raison inapplicable ici — voir point 4).
2. **Nouveaux patients, nouveau centre, nouvelle plateforme.**
   Cohorte Stratford (Royaume-Uni), patients distincts de TCGA,
   ICGC PACA-AU et des cohortes GEO déjà utilisées ; plateforme
   Agilent GPL4133, distincte de toutes les plateformes V1
   (RNA-seq TCGA, Illumina ICGC, Affymetrix GPL20769/GPL6244/
   GPL13667/GPL15048).
3. **Même construction que les autres paires principales GEO.**
   Variante (a) : les 12 mêmes gènes que la v4 TCGA (PGC, REG4,
   CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1,
   MUC16), ordre = KRAS croissant, sans correction, cas complets,
   nul = lignes permutées graine 42. La paire est donc comparable
   aux 8 paires V1 par construction.
4. **Pas un re-test déguisé.** Ce n'est ni une relecture d'un JSON
   existant (§8.64.7 : « pas une relecture »), ni une rotation déjà
   comptée, ni un sous-ensemble d'une paire V1, ni un nouvel ordre
   sur des CSV existants (nouveaux CSV, nouveaux runs, 2 runs
   v6.2 frais). L'exclusion §8.66 reposait sur le stade
   (répartition publiée incohérente : 73 stade I, 0 stade II) —
   inapplicable ici car l'ordre est KRAS uniquement (aucun ordre
   stade construit, protocole §4.2).

**Ce que GSE21501 n'est pas.** Ce n'est pas la cohorte primaire
du protocole (GSE57495) ni son repli (GSE62165) : les deux ont
échoué aux portes d'acceptation (§8.69.4), et GSE21501 est la
cohorte #3, désignée par addendum daté AVANT tout téléchargement
et tout run la concernant, avec les mêmes portes et le même
critère gelés. Ce n'est pas non plus une cohorte choisie pour ses
résultats : aucun `maxsep` GSE21501 n'existait quand l'addendum
a été écrit.

**Convention d'affichage (§8.64.6, adoption provisoire — le
verdict de suffisance tient à une paire aux principales (ICGC) et
à l'échelle du plancher).** La table ci-dessous affiche `maxsep`
comme score principal, l'ancien MC en second, `sep` en compagnon
borné [0, 1], plancher 0,07 en unités |d|.

## 8.69.2 — Le résultat : GSE21501 réel contre nul (v6.2, mode fast, 2 runs, exits 0/0)

| Indicateur | Réel | Nul | Écart (réel − nul) | Lecture |
|---|---|---|---|---|
| **`maxsep` (principal, \|d\|, plancher 0,07)** | **0,2121** | **0,2221** | **−0,0100** | **ÉCHOUE — négatif** |
| `sep` (compagnon borné [0, 1]) | 0,1750 | 0,1817 | −0,0068 | Négatif, comme `maxsep` (monotonie) |
| Ancien MC (secondaire) | 0,3337 (seuil 86,57 %) | 0,3758 (seuil 15,63 %) | −0,0421 | Inversé aussi |
| S_sep (= maxsep × stability) | 0,2094 | 0,2183 | −0,0089 | Inversé, quasi nul |
| Delta | 2,8126 | 0,7998 | **+2,0128** | Favorise le réel — voir §8.69.5 |
| L7a | UP 0,1622 | DOWN 0,3651 | sens opposé | Descriptif — voir §8.69.5 |
| L7b | FRAGILE | FRAGILE | — | Non-informatif, comme partout |
| Falsification | 0,2583 (ok) | 0,5791 (ok) | −0,3208 | Nul devant |
| Cascade (%) | 0,0 / 13,8 / 17,5 / 88,6 / 88,6 (pas 0/18/23/116/116) | 1,5 / 20,4 / 34,5 / 80,3 / 80,3 (pas 2/27/45/105/105) | proches | T_0 réel 17,5 %, nul 34,5 % |
| Régime | criticality | saturation | — | Descriptif |
| Bruit | Proxy de variance modéré (0,6968) | Proxy de variance modéré (0,7841) | — | Même verdict |
| F1 / F2 « Tous » (après/avant) | ×41,85 / ×46,21 | ×0,029 / ×0,023 | sens opposé, sans direction | Descriptif — voir §8.69.5 |

Valeurs exactes (extraction) : réel `maxsep` 0,21205616945238437,
`stability` 0,9873216330006853, MC 0,33365553042301804 ; nul
`maxsep` 0,22208123228935195, `stability` 0,9830485317846254, MC
0,37578979379227523. Écart exact `d_maxsep` =
−0,01002506283696758. `d_sep` = −0,0067680612810066265 ;
`d_MC` = −0,042134263369257186 ; `d_Ssep` =
−0,008948985827369582 ; `d_Delta` = +2,012762. Plancher
équivalent-sep (descriptif, §8.69.3) :
0,07·(1+0,2121)·(1+0,2221) = 0,1037 — la paire échoue aussi à
cette barre, trivialement puisqu'elle est négative.

**Lecture.** Les deux scores `maxsep` sont presque identiques
(0,2121 contre 0,2221) : le pipeline ne voit pas de différence
entre la série réelle ordonnée par KRAS et son nul permuté, sur
cette cohorte, à ce flux. L'écart est négatif de 0,0100 — du même
ordre que GSE62452 (−0,0036), l'autre paire négative du dossier,
et sans commune mesure avec les écarts passants (HP35 +1,6512,
immunitaire +0,3675, TCGA v4 +0,2928). L'ancien MC et S_sep sont
inversés dans le même sens, par de petits écarts : rien, dans
cette paire, ne sépare le réel du nul sur les scores de
séparation. Les cascades sont proches (T_0 réel au pas 23, nul
au pas 45 — un écart de position sans écart de score). La paire
est un nul quasi exact : c'est un résultat, pas un bruit de
mesure — la vérification indépendante le confirme à 0,0 exact
(§8.69.3).

**Lot.** Pipeline `universal_v6.2.0_cohen.py`, SHA
`f07567c4…c3abf`, revérifié inchangé avant ET après le lot ;
mode fast ; 2 runs, exits 0/0, 36 fichiers chacun. Lancement en
`systemd-run` (unité `v62-869`), surveillance `watch_v62_869.sh`
(arrêtée d'elle-même à 2/2, `WATCH 869 TERMINE 2/2`, tour 2,
18h33:41Z) ; journal `runs_v62_869.log` (FIN 18h33:21Z,
déjà faits 0, terminés 2, échecs 0). Durée du lot : 18h19:28Z →
18h33:21Z (~14 min). Aucun redémarrage de machine pendant le
lot. Le livre blanc n'est PAS édité, le PDF N'EST PAS régénéré,
rien n'est poussé sur GitHub dans ce chantier.

## 8.69.3 — A2 étendu, leave-one-out, exactitude

**A2 étendu (9 paires).** Les 8 paires V1 gardent leurs valeurs
(§8.56.3, re-vérifiées à l'identique aux §8.59/§8.64) ; la
neuvième, GSE21501, est négative :

| Paire | Écart `maxsep` | > 0,07 ? | Positif ? |
|---|---|---|---|
| HP35 | +1,6512 | oui | oui |
| TCGA v4 | +0,2928 | oui | oui |
| GSE71729 | +0,0402 | non | oui |
| GSE62452 | −0,0036 | non | non |
| ICGC | +0,0970 | oui | oui |
| Immunitaire TCGA | +0,3675 | oui | oui |
| PARP TCGA | +0,1688 | oui | oui |
| DepMap | +0,1904 | oui | oui |
| **GSE21501 (nouvelle)** | **−0,0100** | **non** | **non** |
| **Total** | — | **6/9** | **7/9** |

**Leave-one-out sur les 9 paires (descriptif, même règle que
D3).** Retirer n'importe laquelle des 6 paires passantes donne
5/8 — sous la barre A2 d'origine (≥ 6/8). Retirer GSE71729,
GSE62452 ou GSE21501 (les trois non passantes) donne 6/8. Le
verdict de suffisance tient donc toujours à une paire — et
désormais à six paires à la fois, comme au §8.59 : chaque paire
passante reste charnière. L'ajout d'une paire qui échoue ne
consolide rien ; il aggrave même le LOO en apparence (6/8
passants sur 9 au lieu de 6/8 sur 8) — en réalité il dit
simplement que la neuvième paire n'apporte pas la septième
passante attendue par C3.

**Exactitude.** Extracteur `extract_869.py` (2/2 runs, 0
manquant, versions `v6.2.0-L7aL7b-CohenD-short` partout) ;
second calcul indépendant `verify_869.py` (chemin de code
distinct, relecture directe des 2 JSON) : **2/2 comparaisons,
écart max 0,0 exact** sur `maxsep`, ancien MC et `stability`,
verdict OK. SHA du pipeline revérifié après travaux, inchangé.
Les 8 valeurs V1 sont reprises telles quelles de
`sep_maxsep_856_table.json` (SHA
`ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`),
jamais recalculées ici — les §8.56/§8.59/§8.64 sont clos.

## 8.69.4 — La recherche de cohorte : ce qui a été vérifié (et ce qui a échoué)

La paire GSE21501 est la troisième cohorte tentée dans ce
chantier. Les deux premières ont échoué à des portes de
construction — pas à des résultats : aucun run n'a été lancé
pour elles, aucun `maxsep` ne les concerne.

| Cohorte | Porte §5 | Résultat vérifié | Sort |
|---|---|---|---|
| GSE57495 (primaire, pré-enregistrée §8.66 §1.2) | 12 gènes v4 présents | **11/12 — GSTM1 absent** (aucune sonde à symbole exact GSTM1 ; seule la sonde partagée `merck-NM_000561_s_at`, annotée « GSTM1 GSTM2 GSTM4 », exclue comme ambiguë, protocole §4.1 ; aucune sonde mappée à la main) ; KRAS présent ; 63/63 cas complets sur 11 gènes | **INUTILISABLE** — aucun CSV, aucun run |
| GSE62165 (repli §3) | 12 gènes v4 présents | **10/12 — DPCR1 et GSTM1 absents** ; KRAS présent ; 118/118 cas complets sur 10 gènes | **INUTILISABLE** — aucun CSV, aucun run |
| GSE21501 (cohorte #3, addendum) | 12 gènes v4 présents | **12/12** ; KRAS présent ; 132/132 cas complets | **UTILISABLE** — paire mesurée (§8.69.2) |

**Correction consignée.** Le protocole §8.66 §1.2 affirmait
GSE57495 sur « plateforme GPL6244 (mapping déjà détenu) ».
C'est faux : la plateforme est **GPL15048** (confirmé par
l'en-tête de la matrice `!Series_platform_id "GPL15048"` et
par deux sources secondaires concordantes). Le mapping GPL6244
n'a PAS été utilisé pour GSE57495 ; un mapping GPL15048 a été
construit à neuf (60 607 lignes, 41 024 sondes avec symbole,
22 115 symboles uniques ; colonne `GeneSymbol` — adaptation
documentée : le protocole prévoyait « Gene Symbol » ou
« gene_assignment », la table réelle porte `GeneSymbol`, même
sémantique). La matrice GSE57495 (13 487 043 o, SHA
`995dbeff…532efc`, 60 608 lignes, 63 tumeurs, valeurs log2
min 1,46 / médiane 5,91 / max 15,06, 0 NaN) et son mapping
(SHA `93e01ec3…998f952`) restent détenus pour un usage futur —
ils ne portent aucun verdict ici.

**Cohortes examinées et écartées (raisons écrites).**
- GSE78229 (50 échantillons, GPL6244) : ses échantillons sont
  déjà inclus dans GSE62452 (résumé de la série : « The
  Affymetrix gene-expression data of these 50 samples were also
  included in the earlier submission by us as GEO accession
  number GSE62452 ») — re-test déguisé de la paire V1 GSE62452.
- GSE28735 (45 tumeurs + 45 normaux, GPL6244) : ses
  échantillons sont ceux de GSE62452 (les échantillons 1–90 de
  GSE62452 avaient été soumis comme GSE28735) — re-test déguisé
  de la paire V1 GSE62452.
- COAD / LUAD : autres cancers, pas des paires principales PDAC,
  ET lots déjà courus (relecture, interdite par §8.64.7).
- CPTAC (UMich / BCM) : protéine, 7/6 flux (pas 12), lots déjà
  courus.
- GSE15471, GSE16515, GSE32676, GSE91035, GSE84219, GSE179351 :
  n < 40 (enquête §8.66 §1.3).
- ICGC PACA-CA / E-MTAB-6134 : accès hors périmètre (§8.66 §1.3).
- **Piste restante non vérifiée : GSE79668** (51 cas, GPL11154,
  Illumina — indépendance et couverture génique inconnues). Elle
  n'a pas été tentée dans ce chantier (arrêt borné de
  l'addendum : aucune cohorte #4) ; elle est nommée ici comme
  piste pour un chantier futur, pas comme un résultat.

**La cohorte GSE21501, en détail.** Matrice
`data/GSE21501_series_matrix.txt.gz`, 12 575 998 o, SHA
`1bbbd9d2…c5dcb6d9b7b`, HTTP 200, 45 220 lignes de données,
132 échantillons, valeurs = log2 RATIOS (tumeur / référence
Stratagene), min −11,33 / médiane 0,04 / max +11,67, 0 NaN.
KRAS (log-ratio) : min −2,08 / médiane −0,34 / max +0,73.
Annotation ragged, vérifiée positionnellement : le libellé
« tissue: Patient Primary Pancreatic Tumor » est en ligne ch2
n°0 pour les colonnes 0–29 (30 Nebraska/UNC, sans données
cliniques) et en ligne ch2 n°4 pour les colonnes 30–131 (102
Stratford) ; règle mécanique : tumeur si le libellé figure
dans une ligne ch2 de l'échantillon → 132/132. Les 30 sans
données cliniques sont gardés (la paire n'a besoin d'aucune
donnée clinique). Mapping GPL4133 construit à neuf (45 220
lignes, 32 696 sondes avec symbole, 19 749 symboles uniques,
colonne `GENE_SYMBOL`, SHA `5630ff23…eb7a3129`). CSV de flux :
`pdac_869_geo21501_fluxes.csv` (132 lignes, SHA
`3d7c1bfe…cd46ba9`), nul SHA `4fc8e79d…280e7d439`.

## 8.69.5 — Contrôles descriptifs (à publier, ne décident pas)

**Delta diverge de `maxsep` sur cette paire.** Delta réel 2,8126
contre nul 0,7998 (+2,0128 en faveur du réel) — le plus grand
écart Delta en faveur du réel sur une paire à n ≈ 130 depuis
les §8.58/§8.66 (où Delta valait ~1,6–2,0 des deux côtés à
n = 118). Le nul est ici anormalement bas (0,80) autant que le
réel est haut (2,81). Cette divergence est rapportée telle
quelle : elle ne sauve pas le verdict, parce que le critère
gelé est `maxsep` — et `maxsep`, MC et S_sep sont tous les
trois (légèrement) inversés sur la même paire. Trois scores de
séparation disent « pas de séparation », un score de tension
dit « le réel est plus tendu » : c'est une piste pour un
chantier futur (que mesure Delta quand `maxsep` est plat ?),
pas une preuve, et pas un sauvetage du présent verdict. À
rapprocher du §8.62 (l'échelle de Delta suit n) : à n = 132,
un Delta réel de 2,81 n'est pas hors d'échelle ; c'est le
Delta nul de 0,80 qui est bas.

**L7a change de sens.** Réel UP 0,1622, nul DOWN 0,3651 — la
direction du vote de cohérence s'inverse entre réel et nul,
avec une confiance plus forte au nul. Descriptif : L7a n'est
pas le critère gelé, et sa confiance réelle (0,16) est faible.

**Falsification et cascade.** Falsification disponible ici
(n = 132 ≥ 75) : réel 0,2583, nul 0,5791 — le nul est devant
de 0,32. Cascade réelle [0,0 / 13,8 / 17,5 / 88,6 / 88,6]
contre nul [1,5 / 20,4 / 34,5 / 80,3 / 80,3] : proches, T_0
réel au pas 23 (17,5 %), nul au pas 45 (34,5 %). Aucune
rupture visible qui distinguerait les deux séries.

**F1/F2 sans direction.** Réel ×41,85 / ×46,21, nul ×0,029 /
×0,023 — les rapports après/avant explosent d'un côté et
s'effondrent de l'autre, sans direction cohérente (même figure
qu'aux §8.58/§8.66 : des rapports sans direction ne font pas
un signal). L7b est FRAGILE des deux côtés — même
non-informativité que dans TCGA et les confirmations GEO.

**Nature des valeurs.** Les flux sont des log-ratios
(tumeur/référence), pas des log-intensités comme les autres
cohortes V1 : chaque gène, KRAS compris, est relatif à la même
référence Stratagene. L'ordre par KRAS reste un ordre par
KRAS. Cette différence de nature est nommée ; elle n'est pas
une excuse au verdict — les autres paires GEO (intensités)
comptent des échecs (GSE71729, GSE62452) comme des succès, et
rien ne permet de dire que le log-ratio, plutôt que la cohorte,
explique l'échec. Un chantier futur qui voudrait tester
l'hypothèse « nature des valeurs » devrait comparer des
cohortes, pas invoquer la nature après coup.

## 8.69.6 — Ce que ça change, et ce que ça ne change pas

| Poste | Change ? | Détail |
|---|---|---|
| Condition C3 (§8.59.8) | **Non levée** | Une paire indépendante mesurée, elle échoue : A2 étendu 6/9 (7/9 positifs). La confirmation indépendante reste ouverte. |
| Adoption pleine de `maxsep` | **Non — décidée par Zackary le 20 nov. 13h04** | Ce chantier est une vérification a posteriori, pas une condition. L'adoption pleine reste sa décision ; la présente section la consolide par son honnêteté, pas par son verdict. |
| Score MC affiché (convention §8.64.6) | Non | `maxsep` principal, ancien MC secondaire, `sep` compagnon, mention de fragilité — inchangée. |
| Sélection du best_config, seuil MC, cascade, S_sep, Delta, L7a | Non | Inchangés par construction. |
| Code v6.2 / v6.1 / v6 | Non | Aucune modification, aucune v6.5. |
| Verdicts des §8.56, §8.59, §8.64 | Non | Confirmés, pas rouverts ; les 8 paires V1 gardent leurs valeurs. |
| Pistes ouvertes | Oui, une de plus | (a) Une autre paire indépendante (GSE79668, seule piste restante nommée, non vérifiée) pourrait encore lever C3 — avec son propre protocole gelé ; (b) la divergence Delta/`maxsep` sur cette paire (Delta +2,01, `maxsep` −0,01) mérite un chantier propre : que mesure Delta quand `maxsep` est plat ? |

**Suite du dossier.** Si Zackary veut une nouvelle tentative de
confirmation : un chantier ultérieur, avec son propre protocole
gelé, sur GSE79668 (ou une autre cohorte vérifiée indépendante)
— pas une relecture, pas un re-test déguisé. Si Zackary ne veut
pas de nouvelle tentative : C3 reste ouverte, l'adoption pleine
tient par sa décision du 20 nov. 13h04, et la présente section
consigne l'échec mesuré avec ses chiffres — elle n'est pas
effacée. Dans les deux cas, le PDF et GitHub sont régénérés et
poussés par le coordinateur (règle permanente « Toujours github
et pdf !!! »), avec la présente section fusionnée.

## 8.69.7 — Limites et ce qui reste

- Une seule paire nouvelle a été mesurée : le verdict porte sur
  elle, pas sur « `maxsep` en général ». 6/9 et 7/9 sont des
  comptages sur 9 paires, pas des estimations de population.
- La paire est construite sur des log-ratios (Agilent deux
  couleurs), nature différente des autres paires V1
  (log-intensités, RNA-seq) : la comparaison est faite à
  construction égale (variante (a), 12 gènes, ordre KRAS), pas
  à nature de mesure égale — c'est nommé au §8.69.5, pas corrigé
  après coup.
- L'identification des tumeurs repose sur une annotation
  ragged (ch2), vérifiée positionnellement (30 + 102 = 132,
  contigus) : la règle est mécanique, mais le format de
  l'annotation est celui du déposant, et les 30 échantillons
  sans données cliniques sont gardés par cette règle. Le
  sous-ensemble des 102 cliniquement annotés existe et n'a pas
  été testé ici : c'est une variante pour un chantier futur, pas
  un résultat tu.
- Deux cohortes (GSE57495, GSE62165) ont échoué aux portes de
  construction sur la couverture génique (GSTM1, DPCR1) : le
  gène GSTM1, en particulier, est absent ou non mappable comme
  flux propre sur deux plateformes Affymetrix sur trois testées
  ici — une limite de la construction à 12 gènes fixes, pas du
  score. Un chantier futur pourrait geler une construction à
  11 gènes (sans GSTM1) et tester GSE57495/GSE62165 sous cette
  construction — mais ce serait une AUTRE construction, avec
  son propre protocole gelé, et elle ne serait plus comparable
  aux 8 paires V1 à 12 gènes : à trancher explicitement, pas en
  silence.
- Delta diverge de `maxsep` sur cette paire (+2,01 contre
  −0,01) : la divergence est rapportée, pas expliquée. L7b est
  FRAGILE des deux côtés — non-informatif, comme partout.
- Rien de clinique : l'étude porte sur l'instrument.

## 8.69.8 — Provenance

- Protocole gelé : `PROTOCOL_maxsep_independent_869.md`, SHA-256
  `86c239b438e68202d375f7baa59bc90d16d65974742071f1552d937431e61a52`
  (au gel, avant téléchargement) ; fichier actuel SHA-256
  `be0a02ca7ffdc75dbf8bd069b48890b227143d4888c16cd92b751599be2e8ab9`
  (corps gelé inchangé, addendum « cohorte #3 » ajouté après
  les deux échecs de portes, avant tout téléchargement et tout
  run de GSE21501).
- Provenance complète : `PROVENANCE_869.md`, SHA-256
  `f310d197dd57bb43a97d210c828a38d98be2d0e61e32535f188cfb1b033893e0`.
- Construction : `build_fluxes_869.py`, SHA-256
  `c27eefb3745d67ceb9cf42cae4d88b645d0039350fd03525847436b101a5d417`
  (variante (a) seulement ; branches 57495 / 62165 / 21501).
- Mappings : `download_gpl15048_mapping_869.py`, SHA-256
  `16b5ce64c1b262186fc5d87f001da66d4e1d4b688290550eb4c1c226efd71c45`
  → `data/GPL15048_probe2symbol.tsv`, SHA-256
  `93e01ec387ab710dfbfe4b7ad960a90c494b131f62637df3a4476fa9f998f952` ;
  `download_gpl4133_mapping_869.py`, SHA-256
  `df345675f92fceebdf9390f83aace50579ee385fc66c698b85769559e82fda0b`
  → `data/GPL4133_probe2symbol.tsv`, SHA-256
  `5630ff23418af6d5241cda8d82a22421e8159a160e6b44123eac3f38eb7a3129`.
- Données : `data/GSE57495_series_matrix.txt.gz`, 13 487 043 o,
  SHA-256
  `995dbeff288a14c1cc1a52489e456b7677ede5da8e287069b8298d649b532efc`
  (HTTP 200, 20 nov. 2026) ; `data/GSE21501_series_matrix.txt.gz`,
  12 575 998 o, SHA-256
  `1bbbd9d2f1a89b26b73b32ef1e781b5ad46aa2f80ebc1d8c94d0ac5dcb6d9b7b`
  (HTTP 200, 20 nov. 2026) ; GSE62165 déjà détenue, SHA-256
  `fd50fc415a31a4d19a4af82e29afc6909e913f4f223d0b4cd4b637ae4a03727f`
  (`PROVENANCE_866.md`).
- Flux : `pdac_869_geo21501_fluxes.csv` (132 lignes), SHA-256
  `3d7c1bfe1a4ce02cc7bc4087791e8175efc03338e0643c98463a836e9cd46ba9` ;
  `pdac_869_geo21501_fluxes_nul.csv`, SHA-256
  `4fc8e79ddb8991f91276881d58631a6b03ef82654fdd74d9a3323db280e7d439`.
- Runs : manifeste `manifest_v62_869.txt`, SHA-256
  `051ba5855bc52279a181a3609f5db48857b08630e1a64702ff07a12df0eadf65` ;
  journal `runs_v62_869.log` (94 lignes) ; surveillance
  `watch_v62_869.sh`, SHA-256
  `ee4ed3135da4ef09c5c2dd634a201c6e45562bbe57bf05c5a56bb5040ec7c93c` ;
  dossiers `results_fast_v62_869_geo21501[_nul]` (2 runs, exits
  0/0, 36 fichiers chacun).
- Extraction : `extract_869.py`, SHA-256
  `37c31a507edfbfb4ccea6815f0e7bf3339e4b8e199c5eea2307fce29a5ad25fe`
  → `extract_869.json`, SHA-256
  `644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b` /
  `extract_869.csv`, SHA-256
  `52c05841394c2ee79bbb982c717a55b75f6039def5dc0cc1d93b1de19ca9c4a9`.
- Vérification indépendante : `verify_869.py`, SHA-256
  `21f402ba9e1cd28b601591842acdd49a873de93558ea6d6c0374e60a7f0db514`
  → `maxsep_869_verify.json`, SHA-256
  `99afa51717e534f3d2bfccd23fbf2c1e583bc2d2b7b4ed9595bf6f13454d2daa`
  (2/2 comparaisons, écart max 0,0 exact, verdict OK).
- Référence re-vérifiée : `sep_maxsep_856_table.json`, SHA-256
  `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`
  (8 paires V1 reprises telles quelles, jamais recalculées ici) ;
  protocole §8.56 `PROTOCOL_sep_maxsep_856.md` (SHA-256
  `06e36725eedb3d52b1549290e1e8cccff381650928fbf4e6a28a090aec27fd4e`) ;
  section §8.56 `section_8.56_sep_maxsep.md` (SHA-256
  `9015ab0cf8d4b577a5ba3bd37512032461762f31f9daa177f63ba41120fe9012`) ;
  protocole §8.59 `PROTOCOL_maxsep_adoption_859.md` (SHA-256
  `efb5da799d245d8e5db570945acc480f1c5bae42d63ed29b7cfeb780610e675b`) ;
  protocole §8.64 `PROTOCOL_maxsep_decision_864.md` (SHA-256
  `69c40d73258bab6855fe65c65198fc8ec524f455ac1ff15ef7641d1f578b4ae8`).
- Livre blanc de référence consulté :
  `livre-blanc-pdac-v6.md`, 12 138 lignes, SHA-256
  `f0c8af71e9578a5f21af2369607745e8376c1c7b0b97c2d01202f7e4086c6417`
  (§8.1–§8.66, état au 20 nov. 2026) — le livre blanc n'a PAS
  été modifié par ce chantier. Fusion de la présente section par
  le coordinateur.
- Données : séries réelles = intensités / log-ratios de puce
  (mesures instrumentales transformées : log2 par les déposants,
  agrégation des sondes par médiane, ordre par KRAS). Nuls =
  lignes permutées, graine 42 — échantillons hypothétiques, pas
  des mesures. Aucune valeur inventée ; aucune valeur recopiée
  à la main (tables générées depuis `extract_869.json`, vérifiées
  paire par paire à 0,0 exact par `verify_869.py` ; les valeurs
  des §8.69.2–§8.69.3 sont lues dans cette sortie, pas recopiées
  des §8.56/§8.59/§8.64).
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`, revérifié avant
  ET après le lot), v6.1 (`2af5e5ce…c1c9`), v6
  (`bb8bbdba…c0773`). Aucune nouvelle version construite dans ce
  chantier — pas de v6.5. Deux runs du pipeline lancés dans ce
  chantier (GSE21501 réel + nul, exits 0/0) ; aucun push GitHub,
  aucune Release dans ce chantier.
- Section : `section_8.69_maxsep_independent.md` (ce fichier ;
  SHA noté au rapport).
