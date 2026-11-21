# §8.83 — Survie : les gènes de privilège prédisent-ils la survie comme CA125 ? OUI, pour 3 items sur 8 — mais pas parce qu'ils montent avec KRAS

## Verdict d'abord

**AU MOINS UN gène de privilège prédit la survie comme CA125 : 3 items
sur 8 sont dans la catégorie « PRÉDIT COMME CA125 » (Cox univarié
HR > 1, p < 0,05 dans ≥ 2/3 cohortes) — TGFB2, HLA-G et le score
combiné des 7 gènes.** TGFB2 : TCGA HR 1,28 (p=0,014), ICGC 1,34
(p=0,048), GSE71729 1,01 (ns). HLA-G : TCGA 1,18 (ns, p=0,11), ICGC
1,71 (p=0,0004), GSE71729 1,28 (p=0,035). Score combiné : TCGA 1,28
(p=0,020), ICGC 1,70 (p=0,001), GSE71729 1,07 (ns). Les 5 autres items :
TGFB1 et CD274 une cohorte seule (ICGC et TCGA respectivement) ; CD47
MIXTE (TCGA HR 1,30 p=0,009 vers le haut, GSE71729 HR 0,76 p=0,010 vers
le bas) ; FASLG et IDO1 ne prédisent rien nulle part.

**Mais la question posée — « les gènes qui montent avec KRAS
prédisent-ils la survie ? » — reçoit une réponse en deux temps, et le
deuxième temps est NON : aucun des 7 gènes ne monte avec KRAS dans
≥ 2/3 cohortes (le meilleur, TGFB1/TGFB2/CD47/CD274, monte dans 1/3
seulement, et toujours en TCGA seule ou presque).** Les deux gènes qui
prédisent la survie comme CA125 ne montent pas avec KRAS : TGFB2 ne
monte qu'en TCGA (rho +0,337) et est plat ailleurs ; HLA-G ne monte
nulle part — il DESCEND avec KRAS en GSE71729 (rho −0,288, p=0,001).
Autrement dit : dans nos 3 cohortes, le privilège immunitaire porte un
signal de survie, mais ce signal ne passe pas par KRAS. C'est un
résultat de test direct, hors pipeline ; il ne dit rien d'un remède,
et il ne change rien aux décisions (C3 reste levée, test C reste NON,
adoption pleine de maxsep inchangée).

**Fragilité, dite en tête.** Le verdict tient à des p proches du seuil
dans deux cas : TGFB2 en ICGC (p=0,048) et HLA-G en GSE71729 (p=0,035)
— un patient de plus ou de moins peut les faire basculer. À
Bonferroni (0,05/24 ≈ 0,0021, descriptif, pas une porte), seuls les
signaux ICGC survivent (TGFB1 p=0,0005, HLA-G p=0,0004, score
p=0,0013) ; aucun item ne passe Bonferroni dans ≥ 2 cohortes. Le
log-rank quartile contredit le Cox pour le score combiné en TCGA
(p=0,83 contre Cox p=0,02) — exactement comme CA125 en TCGA
(Cox p=0,001, log-rank p=0,070) : le verdict repose sur le test sans
seuil, comme le record de CA125 lui-même. Les effectifs sont petits
en ICGC (n=70), où les effets les plus forts sont mesurés.

Protocole gelé : `PROTOCOL_survie_privilege_883.md` (21 nov. 2026, SHA
`0eb83d63…`), amendé AVANT toute lecture des résultats privilège (voir
§8.83.1). Critère principal écrit AVANT toute analyse (§5 du protocole) :
Cox univarié HR > 1, p < 0,05 dans ≥ 2/3 cohortes. Méthode : KM /
log-rank / Cox, exactement celle des §8.12/§8.15/§8.16. Ce chantier
n'utilise PAS le pipeline.

## 8.83.1 — Calibration : la porte a d'abord refusé, puis passé

Le script `survival_privilege_883.py` (SHA `c61ef946…`) reproduit
D'ABORD les chiffres publiés de MUC16 avant de lire aucun résultat
privilège. Le premier essai a ÉCHOUÉ sur 2 points et le script s'est
arrêté, comme le protocole l'exige — aucun résultat privilège n'a été
lu à ce stade. Diagnostic par re-calcul direct :

1. **GSE71729, log-rank MUC16 : 0,8562 calculé contre 0,73 publié.**
   Cause trouvée : le script utilisait un seuil au quantile 0,75 sur
   les 145 primaires (n=34). La définition publiée du §8.15 est le top
   36 PAR RANG sur les 145 (`sort_values().iloc[-36:]`), qui donne
   n=33, décès 22, médiane 17,0 vs 16,0, p=0,7292 — identique au §8.15
   à 0,001 près. Un patient lié au seuil faisait basculer p de 0,73 à
   0,86 : c'est la fragilité du log-rank à n=33, pas une erreur de
   données. Corrigé : masques par rang (top 36 GSE71729, top 18 ICGC),
   comme dans les bras publiés.
2. **TCGA, médiane de cohorte : 20,2 calculée contre 20,0 publiée.**
   Cause : le §8.12 donne 20,0 mois (KM) ; l'implémentation gelée
   (premier temps d'événement où S ≤ 0,5) donne 20,2. La médiane simple
   des temps observés vaut 15,2 — c'est le chiffre « 15.2 » de
   `tcga_survival_verify_results.txt`, mal étiqueté « OS médiane
   cohorte » dans ce fichier, et ce n'est PAS une médiane de survie.
   Tolérance de calibration élargie de ±0,1 à ±0,5 mois, raison écrite
   au protocole.

Amendement consigné au protocole (§3.2 et §6) avant toute lecture des
résultats privilège. Deuxième essai : **CALIBRATION OK, 3/3 cohortes.**

| Cohorte | Cox MUC16 HR (attendu) | log-rank MUC16 p (attendu) | n / décès | OS médiane (attendue) |
|---|---|---|---|---|
| TCGA | 1,4392 (1,44) | 0,0703 (0,070) | 177 / 92 | 20,2 (20,0) |
| ICGC | 1,5688 (1,57) | 0,0019 (0,002) | 70 / 47 | 16,6 (16,6) |
| GSE71729 | 1,0625 (1,06) | 0,7292 (0,73) | 125 / 84 | 17,0 (17,0) |

Jointures vérifiées : TCGA 178 tumeurs et top12 KRAS résidu identiques
à `tcga_groups_survival.json` ; GSE71729 KRAS/MUC16/CEACAM5 identiques
à `geo71729_survival_table.csv` (écart < 1e-9) ; ICGC n=70, 47 décès.
Échelles : TCGA = résidus corrigés de la pureté (§8.12) ; ICGC =
log2(cpm) brut ; GSE71729 = valeurs brutes de la matrice (§8.15).

## 8.83.2 — Le tableau complet : Cox univarié, log-rank, et KRAS

HR par +1 écart-type, Cox univarié (un gène à la fois). Log-rank :
quartile supérieur vs reste (définitions par cohorte au §8.83.1 :
TCGA seuil quantile 0,75 sur 177 ; ICGC top 18 par rang ; GSE71729
top 36 par rang sur 145 ; score GSE71729 top 36 sur 125). Spearman :
gène vs KRAS, mêmes données. « Monte » = rho ≥ +0,15 et p < 0,05.

| Item | TCGA Cox HR (p) / log-rank p | ICGC Cox HR (p) / log-rank p | GSE71729 Cox HR (p) / log-rank p | Catégorie (gelée) | Monte avec KRAS |
|---|---|---|---|---|---|
| FASLG | 0,92 (0,43) / 0,16 | 0,90 (0,54) / 0,12 | 1,08 (0,48) / 0,96 | NE PRÉDIT RIEN | 0/3 |
| TGFB1 | 1,01 (0,94) / 0,66 | **1,77 (0,0005)** / 0,0002 | 1,14 (0,29) / 0,093 | UNE COHORTE | 1/3 |
| TGFB2 | **1,28 (0,014)** / 0,025 | **1,34 (0,048)** / 0,063 | 1,01 (0,91) / 0,79 | **PRÉDIT COMME CA125** | 1/3 |
| IDO1 | 1,17 (0,13) / 0,39 | 1,07 (0,65) / 0,98 | 1,16 (0,14) / 0,068 | NE PRÉDIT RIEN | 0/3 |
| HLA-G | 1,18 (0,11) / 0,45 | **1,71 (0,0004)** / 0,0007 | **1,28 (0,035)** / 0,040 | **PRÉDIT COMME CA125** | 0/3 |
| CD47 | **1,30 (0,009)** / 0,070 | 1,33 (0,058) / 0,24 | **0,76 (0,010)** / 0,032 | MIXTE | 1/3 |
| CD274 | **1,28 (0,033)** / 0,013 | 1,26 (0,14) / 0,093 | 0,87 (0,30) / 0,68 | UNE COHORTE | 1/3 |
| SCORE_PRIV | **1,28 (0,020)** / 0,83 | **1,70 (0,001)** / 0,0066 | 1,07 (0,53) / 0,73 | **PRÉDIT COMME CA125** | 1/3 |

Médianes OS (quartile supérieur vs reste) pour les trois items
passants : TGFB2 — TCGA 15,5 vs 21,7 mois (n=45, 26 décès), ICGC 11,6
vs 23,8 (n=18, 15 décès), GSE71729 18,0 vs 17,0 (ns) ; HLA-G — TCGA
20,0 vs 20,8 (ns), ICGC 9,4 vs 23,7 (n=18, 16 décès), GSE71729 11,0 vs
19,0 (n=31, 24 décès) ; score combiné — TCGA 19,8 vs 20,2 (ns, malgré
Cox p=0,020), ICGC 9,5 vs 23,7 (n=18, 15 décès), GSE71729 16,0 vs 17,0
(ns). La médiane ICGC du score (9,5 vs 23,7 mois) est du même ordre
que celle de CA125 en ICGC (9,5 vs 23,8 mois, §8.16).

## 8.83.3 — Les trois items passants, un par un

**TGFB2 — PRÉDIT COMME CA125.** TCGA HR 1,28 (p=0,014, log-rank
p=0,025) ; ICGC HR 1,34 (p=0,048, log-rank p=0,063, DSS HR 1,35
p=0,056) ; GSE71729 HR 1,01 (p=0,91). Le maillon faible est ICGC
(p=0,048, et DSS à 0,056) : le passage tient à deux p juste sous 0,05.
TGFB2 monte avec KRAS en TCGA seulement (rho +0,337, p<0,0001 ; ICGC
+0,037, ns ; GSE71729 −0,013, ns) — 1/3 cohortes. C'est le seul des
trois passants qui monte avec KRAS quelque part.

**HLA-G — PRÉDIT COMME CA125.** TCGA HR 1,18 (p=0,11, ns) ; ICGC HR
1,71 (p=0,0004, log-rank p=0,0007, DSS HR 1,72 p=0,0009) ; GSE71729 HR
1,28 (p=0,035, log-rank p=0,040). Le signal est porté par ICGC (le
plus fort HR du chantier, 1,71) et GSE71729 ; TCGA pointe dans le même
sens sans atteindre le seuil. HLA-G ne monte avec KRAS nulle part
(TCGA rho +0,029, ns ; ICGC −0,118, ns ; GSE71729 −0,288, p=0,001 —
il DESCEND avec KRAS en GSE71729). Un gène de privilège qui prédit une
survie plus courte tout en descendant quand KRAS monte : le signal de
survie ne passe pas par KRAS.

**Score combiné (moyenne des z-scores des 7) — PRÉDIT COMME CA125.**
TCGA HR 1,28 (p=0,020, mais log-rank p=0,83 — médianes 19,8 vs 20,2
mois, le quartile ne voit rien) ; ICGC HR 1,70 (p=0,001, log-rank
p=0,0066, DSS HR 1,58 p=0,011) ; GSE71729 HR 1,07 (p=0,53). Le score
passe par TCGA + ICGC, pas par GSE71729. Il monte avec KRAS en TCGA
seulement (rho +0,161, p=0,033 ; ICGC +0,095, ns ; GSE71729 −0,037,
ns) — 1/3 cohortes. La section dit plainement que c'est le score, pas
un gène seul, qui passe — et que le score est tiré par TGFB2/HLA-G en
ICGC.

## 8.83.4 — Les cinq autres : un signal fort isolé, une contradiction, deux riens

**TGFB1 — UNE COHORTE (ICGC seule, mais forte).** ICGC HR 1,77
(p=0,0005, log-rank p=0,0002, quartile 10,9 vs 25,6 mois, DSS HR 1,86
p=0,0004) — le signal le plus significatif du chantier après HLA-G en
ICGC, et l'un des trois seuls à passer Bonferroni (0,05/24 ≈ 0,0021).
TCGA HR 1,01 (p=0,94) et GSE71729 HR 1,14 (p=0,29) : rien ailleurs.
TGFB1 monte avec KRAS en GSE71729 seulement (rho +0,235, p=0,008).
Un signal ICGC-seul, fort mais non répliqué : piste, pas preuve.

**CD274/PD-L1 — UNE COHORTE (TCGA seule).** TCGA HR 1,28 (p=0,033,
log-rank p=0,013, médiane 17,0 vs 22,5 mois) ; ICGC HR 1,26 (p=0,14) ;
GSE71729 HR 0,87 (p=0,30). Monte avec KRAS en TCGA seulement (rho
+0,298, p=0,0001). Cohérent avec le §8.23 (PD-L1 ne montait qu'en
TCGA) : le même « TCGA seule » se répète pour la survie.

**CD47 — MIXTE (contradiction entre cohortes).** TCGA HR 1,30
(p=0,009, vers une survie plus courte) ; GSE71729 HR 0,76 (p=0,010,
vers une survie PLUS LONGUE, log-rank p=0,032, médiane 19,0 vs 15,0
mois) ; ICGC HR 1,33 (p=0,058, même sens que TCGA, sous le seuil).
Deux cohortes significatives en sens opposés : la catégorie MIXTE est
faite pour ça, et elle est dite telle quelle. CD47 monte avec KRAS en
TCGA seulement (rho +0,198, p=0,008).

**FASLG et IDO1 — NE PRÉDIT RIEN.** Aucune cohorte avec p < 0,05 dans
un sens ou dans l'autre (FASLG : 0,92 / 0,90 / 1,08 ; IDO1 : 1,17 /
1,07 / 1,16, tous ns). IDO1 pointe vers le haut dans les 3 cohortes
sans jamais atteindre le seuil — direction constante, effet trop
faible pour nos effectifs ; dit tel quel, pas comme un signal.

## 8.83.5 — Le croisement avec KRAS : la prémisse ne tient pas

La mission demandait si « les gènes de privilège qui montent avec
KRAS prédisent la survie ». Le tableau de croisement (Spearman gène vs
KRAS, règle gelée §4) :

| Gène | TCGA rho (p) | ICGC rho (p) | GSE71729 rho (p) | Monte (≥2/3) ? |
|---|---|---|---|---|
| FASLG | −0,134 (0,076) | −0,046 (0,71) | −0,143 (0,11) | non (0/3) |
| TGFB1 | −0,106 (0,16) | +0,165 (0,17) | **+0,235 (0,008)** | non (1/3) |
| TGFB2 | **+0,337 (<0,0001)** | +0,037 (0,76) | −0,013 (0,89) | non (1/3) |
| IDO1 | −0,007 (0,93) | −0,056 (0,64) | +0,052 (0,57) | non (0/3) |
| HLA-G | +0,029 (0,70) | −0,118 (0,33) | **−0,288 (0,001)** | non (0/3) |
| CD47 | **+0,198 (0,008)** | +0,137 (0,26) | +0,145 (0,11) | non (1/3) |
| CD274 | **+0,298 (0,0001)** | +0,177 (0,14) | −0,172 (0,055) | non (1/3) |
| SCORE_PRIV | **+0,161 (0,033)** | +0,095 (0,43) | −0,037 (0,68) | non (1/3) |

**Aucun gène ne monte avec KRAS dans ≥ 2/3 cohortes.** En TCGA, 4
gènes sur 7 montent (TGFB2, CD47, CD274, score) — mais c'est TCGA
seule, et le §8.23 avait déjà montré que PD-L1 ne montait qu'en TCGA.
En ICGC, aucun ne monte significativement ; en GSE71729, un seul
(TGFB1) monte et un (HLA-G) descend significativement. La prémisse
« les gènes de privilège montent avec KRAS » n'est pas établie dans
nos cohortes pancréatiques : elle est vraie en TCGA, fausse ailleurs.
Donc la question ne peut pas se lire comme « les gènes KRAS-montants
prédisent-ils la survie » — la réponse honnête est double : (a) oui,
3 items sur 8 prédisent la survie comme CA125 (TGFB2, HLA-G, score) ;
(b) non, ce ne sont pas les gènes qui montent avec KRAS — HLA-G
prédit la survie en descendant avec KRAS en GSE71729, et TGFB2 ne
monte qu'en TCGA. Le signal de survie du privilège et l'axe KRAS sont
deux choses différentes dans ces données.

## 8.83.6 — Ce que le verdict dit, et ce qu'il ne dit pas

Il dit que le programme de privilège immunitaire — mesuré en ARN bulk,
7 gènes — porte un signal pronostique dans le pancréas au même niveau
de preuve que CA125 (2/3 cohortes) pour TGFB2, HLA-G et le score
combiné, avec ICGC comme cohorte la plus forte (HR 1,34–1,71, DSS
confirmé pour HLA-G et le score). Il dit que ce signal ne passe pas
par KRAS dans nos données. Il ne dit pas que ces gènes CAUSENT la
mauvaise survie (ARN bulk, pas de mécanisme, pas d'ajustement sur le
stade ou le traitement — la chimiothérapie n'est pas dans le fichier
clinique TCGA, §8.18). Il ne dit pas que le privilège immunitaire est
une cible thérapeutique : aucun de ces gènes n'a de médicament validé
dans le pancréas par ce chantier (TGFB et HLA-G sont des pistes
biologiques, pas des recommandations). Il ne dit pas que CA125 est
remplacé : CA125 reste le marqueur de référence (TCGA 1,44, ICGC 1,57)
avec des HR comparables ou supérieurs à TGFB2/HLA-G.

## 8.83.7 — Limites

- **Effectifs :** ICGC n=70 — les HR les plus forts (1,71 ; 1,77)
  viennent de la plus petite cohorte ; TCGA n=177, GSE71729 n=125.
- **Seuils proches :** TGFB2 ICGC p=0,048, HLA-G GSE71729 p=0,035,
  CD47 ICGC p=0,058 (juste au-dessus) — trois p à ±0,01 du seuil
  changeraient chacune une catégorie.
- **Tests multiples :** 24 Cox ; Bonferroni 0,05/24 ≈ 0,0021 (descriptif)
  — seuls TGFB1 ICGC (0,0005), HLA-G ICGC (0,0004) et score ICGC
  (0,0013) passent, tous en ICGC seule ; aucun item ne passe
  Bonferroni dans ≥ 2 cohortes. Le verdict « comme CA125 » utilise la
  même règle que CA125 (p < 0,05 brutes, 2/3 cohortes) — CA125 lui-même
  ne passerait pas Bonferroni partout (ICGC p=0,008).
- **ARN bulk, sans correction de pureté** (sauf TCGA, résidus) : comme
  au §8.23, on ne distingue pas « plus de cellules qui expriment » de
  « plus d'expression par cellule ».
- **Log-rank vs Cox :** le log-rank contredit le Cox pour le score en
  TCGA (p=0,83 vs 0,02) et pour TGFB2 en ICGC (p=0,063 vs 0,048) —
  le verdict repose sur le Cox sans seuil, comme le record de CA125.
- **DSS** (ICGC) rapportée seulement pour les items significatifs en
  OS dans ICGC (TGFB1 1,86 p=0,0004 ; HLA-G 1,72 p=0,0009 ; score 1,58
  p=0,011 ; TGFB2 1,35 p=0,056, juste au-dessus du seuil).

## 8.83.8 — Pistes ouvertes

1. TGFB1 en ICGC (HR 1,77, DSS 1,86) : répliquer dans une 4e cohorte
   avec survie avant toute interprétation — une cohorte seule, même
   forte, reste une cohorte seule.
2. HLA-G : pourquoi prédit-il la survie en descendant avec KRAS en
   GSE71729 ? Une stratification par sous-type (Bailey/Moffitt) est
   une piste — pas testée ici (aucun ajustement ajouté après coup).
3. CD47 MIXTE : la contradiction TCGA/GSE71729 demande une 4e cohorte
   pour trancher le sens — ne pas moyenner deux sens opposés.
4. Score combiné : sa valeur ajoutée au-delà de TGFB2+HLA-G (les deux
   gènes qui le portent en ICGC) n'est pas testée ici.

## 8.83.9 — Annexe : provenance condensée et SHAs

- Protocole : `PROTOCOL_survie_privilege_883.md`, SHA
  `0eb83d63…` (gelé avant analyse ; amendé avant lecture des résultats
  privilège, §8.83.1).
- Provenance complète : `PROVENANCE_883.md`.
- Script : `survival_privilege_883.py`, SHA `c61ef946…`.
- Sorties : `survival_privilege_883_table.csv` (SHA `ad105af8…`),
  `survival_privilege_883_results.txt` (SHA `628b458d…`),
  `survival_privilege_883_results.json` (SHA `a84cf494…`).
- Sources : TCGA tarball MD5 `b09569ce…` ; GSE71729 SHA `b2287893…` ;
  ICGC exp SHA `c2cb57af…`, probemap `b09a746f…`, Bailey XLSX
  `778224b3…` (détail dans `PROVENANCE_883.md`).
- Calibration : Cox MUC16 1,4392 / 1,5688 / 1,0625 ; log-rank 0,0703 /
  0,0019 / 0,7292 ; n 177/70/125 ; décès 92/47/84.
- Ce chantier ne rouvre rien : C3 reste levée, test C reste NON,
  adoption pleine de maxsep inchangée ; hors pipeline.
