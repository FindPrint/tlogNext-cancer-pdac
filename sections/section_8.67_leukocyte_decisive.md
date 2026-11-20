# §8.67 Test décisif sur la fraction leucocytaire : elle porte un tiers de la corrélation, pas la séparation — PARTIEL

Date : 20 novembre 2026 (13h05–13h45 heure de Montréal, 18h05–18h45 UTC).
Go : Zackary, 20 nov. 2026 13h04 (« Fait tout cela »). Question ouverte
des §8.60.9–§8.60.11 et §8.61.11 (« piste la plus forte pour la suite »).
Protocole gelé avant tout calcul nouveau et avant tout run :
`PROTOCOL_leukocyte_decisive_867.md` (SHA-256
`571adf826f455b8dfd49c63f2c0e94fc73a7ae03a6e98b5bfda2bb0648ae59ad`).

## Verdict d'abord

**La fraction leucocytaire PORTE une partie de l'effet, pas tout.
Verdict gelé : PARTIEL.** La question décisive était : l'écart S_sep
s'effondre-t-il quand on FIXE la fraction leucocytaire ? Réponse en
deux temps, les deux mesurés dans ce chantier. (a) Oui, la fraction
leucocytaire ordonne les flux bruts (D-LEU +0,7129, §8.60) et retire
un tiers de la cohésion (0,5035 → 0,3372, −33,0 %, re-vérifié ici à
la décimale près) — et une fois les flux résidualisés, elle ne les
ordonne PLUS DU TOUT (**L-ORD −0,0099**, réel 0,2214 contre nul
0,2313, le nul devant : la régression linéaire a épuisé tout
l'ordonnancement leucocytaire, sans reste non linéaire mesurable).
(b) Mais non, la séparation ne s'effondre pas : ordonner les flux
RÉSIDUALISÉS par CD8A résidualisé sépare encore **+0,5662** (réel
0,7771 contre nul 0,2109), soit **57,6 % du brut CD8A +0,9838
conservés** — presque exactement la prédiction de la régression §8.48
(+0,5409, à 0,0253 près). La fraction leucocytaire porte donc un
tiers de la cohésion et tout son propre ordonnancement, mais la
co-expression qui reste après l'avoir fixée est toujours réelle et
sépare toujours : elle n'est pas portée par la quantité de leucocytes.

**La place de ce résultat dans l'échelle des porteurs est l'information.**
Cohésion retirée / séparation résiduelle conservée : ImmuneScore
global −64,0 % / 20,2 % (PORTE, §8.54) ; fraction leucocytaire −33,0 %
/ 57,6 % (PARTIEL, ici) ; ABSOLUTE −25,5 % / 66,1 % (PARTIEL, §8.55) ;
pureté méthylation −15,9 % / 55,2 % (ZONE GRISE, §8.61) ; B naïfs
(TOP1) −4,7 % / 78,2 % (NE PORTE PAS, §8.60). La fraction leucocytaire
se comporte, sur la séparation résiduelle, comme la pureté par
méthylation (57,6 % contre 55,2 %) alors qu'elle retire DEUX FOIS
plus de cohésion linéaire (−33,0 % contre −15,9 %) : la séparation
résiduelle n'est PAS proportionnelle à la cohésion linéaire retirée.
Et le score global (ImmuneScore) retire bien plus que la fraction
leucocytaire sur les deux voies — la question du porteur se déplace
donc : qu'est-ce que l'ImmuneScore capte AU-DELÀ de la quantité de
leucocytes (état d'activation ? types conjoints ? stroma ?) ?
C'est la piste ouverte du §8.67.10, pas un verdict de ce chantier.

**Les trois nuances sont nommées, pas cachées.** (a) Le gain conjoint
[T2-J1] est marginal : ajouter la fraction leucocytaire à
l'ImmuneScore ne retire que 2,7 points de chute de plus (−54,9 % →
−57,6 %) — entre la bande « rien ajouté » (± 2 points) et le seuil
de part indépendante (≥ 10 points) : la fraction leucocytaire est
presque entièrement contenue dans ce que mesure le score global.
(b) Le gain conjoint [T2-J2] est au contraire juste au-dessus du
seuil : ajouter la fraction leucocytaire à ABSOLUTE retire 10,8
points de plus (−25,5 % → −36,3 %) — la fraction leucocytaire porte
une part INDÉPENDANTE de la pureté ABSOLUTE, de justesse. (c) La
stratification T4-L est intermédiaire : dans la moitié basse — une
vraie bande étroite (écart-type 41,3 % du global) — la cohésion ne
tombe qu'à 0,3856 (76,6 % de la brute, chute 23,4 %), ni
effondrement (< 0,30) ni persistance (≥ 0,80 × brute = 0,4028) :
fixer la fraction leucocytaire en bande étroite ne tue pas la
cohésion non plus.

## 8.67.1 Question, méthode, inventaire des sources (avant le gel)

**Question (§8.60.11, §8.61.11).** Le §8.54 a établi que la corrélation
intra-famille immunitaire (0,5563) est expliquée par l'infiltration
GLOBALE (ImmuneScore : 0,5563 → 0,2002, chute 64,0 % ; I-RES +0,1982).
Le §8.60 (bras L) a établi, par une voie indépendante de l'ARN, que la
fraction leucocytaire par méthylation retire un tiers de la cohésion
(0,5035 → 0,3372, chute 33,0 %, PARTIELLE) et ordonne les flux
(D-LEU +0,7129) — mais le run RÉSIDUEL manquait : on ne savait pas si
la séparation survit quand on FIXE la fraction leucocytaire. Ce
chantier fait ce test décisif. Il ne re-teste ni l'ImmuneScore global
(§8.54) ni ABSOLUTE (§8.55) ni les types cellulaires (§8.60) et
n'importe aucune conclusion d'une autre expérience : seuls les chiffres
de ce chantier (Porte L, T1-L2–T5-L2 du jour) et les écarts relus des
§8.44/§8.48/§8.54/§8.55/§8.60/§8.61 font le verdict. Les chiffres
T1-L/T2-L/D-LEU du §8.60 sont des références relues en machine et
RE-VÉRIFIÉES ici (T1-L2, T2-L2), jamais le verdict.

**Ce qui existe réellement.** (a) Tarball TCGA-PAAD RSEM, Broad GDAC
Firehose 2016-01-28, MD5 `b09569ce…ac0a` (détenu) — la même matrice
que §8.54/§8.55/§8.60/§8.61. (b) Base immunitaire TCGA
`pdac_immune_tcga_fluxes.csv`, n = 178, 12 gènes BRUTS log2(RSEM+1) :
CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274, PDCD1, CTLA4, GZMB, IFNG,
CD19 ; fichier d'axe joint `immune_kras_order_tcga.csv` (step, sample,
kras_raw) — clé de jointure PAR BARCODE, jamais par index.
(c) Fraction leucocytaire par méthylation : colonne
`DNA.methylation.leukocyte.percent.estimate` du `sampInfo` transcrit
au §8.55 (`purity_855_sampinfo.csv`, 181 lignes × 55 colonnes) —
estimation publiée depuis l'ADN (Raphael et al. 2017, Table S1, via
pdacR), indépendante de l'ARN, globale (tous leucocytes confondus).
(d) Mesures de soutien déjà détenues : fraction leucocytaire imogimap
(Thorsson et al. 2018, via le miroir imogimap, §8.60), ImmuneScore
ESTIMATE calculé (§8.54), pureté ABSOLUTE externe (§8.55).
**Aucun nouveau téléchargement dans ce chantier** : toutes les sources
sont détenues et vérifiées par SHA avant tout calcul (protocole §9).

**Définition opérationnelle gelée de « porter l'effet » (protocole
§1, §7).** La fraction leucocytaire PORTE l'effet si, une fois fixée,
la séparation S_sep entre flux résidualisés s'effondre (L-RES < 0,30,
soit ≤ 30,5 % du brut +0,9838 — le niveau de l'ImmuneScore I-RES
+0,1982) ET si elle n'ordonne plus les résidus (L-ORD < 0,30). Elle
NE PORTE PAS l'effet si la séparation survit à ≥ 0,70 (≥ 71 % du brut
— le niveau du D-RES par type +0,7692). Entre les deux : PARTIELLE.
Point gelé : T2-L est déjà connue PARTIELLE (−33,0 %), donc
l'effondrement de la COHÉSION globale est exclu d'avance — le verdict
PORTE ne peut pas l'exiger ; il exige l'effondrement de la SÉPARATION
(L-RES, L-ORD) et, si une bande étroite existe, de la cohésion en
bande étroite (T4-L). La question décisive est si la séparation
s'effondre PLUS que la cohésion (porteur non linéaire / à seuil) ou
MOINS (part linéaire seulement).

**Hypothèses gelées.** H1-leu (la fraction leucocytaire PORTE
l'effet) : (a) chaque flux corrèle substantiellement avec la fraction
leucocytaire (déjà établi au §8.60 : moyenne |r| = 0,5456) ;
(b) après régression, la cohésion chute d'au moins un tiers (déjà
établi : −33,0 %) ; (c) ordonner les flux par la fraction leucocytaire
les sépare (déjà établi : D-LEU +0,7129) ; (d) NOUVEAU, décisif :
ordonner les flux RÉSIDUALISÉS par CD8A résidualisé ne sépare PLUS
(L-RES < 0,30) et la fraction leucocytaire n'ordonne plus les résidus
(L-ORD < 0,30) ; (e) la cohésion s'effondre dans une bande étroite
de fraction leucocytaire (T4-L). H0-leu (NE PORTE PAS — simple
corrélat de la composition) : la corrélation et la séparation
persistent après fixation, par toutes les voies (b)–(e).

## 8.67.2 Porte L (source) : OUVERTE — jointure, identification, sélection

**Vérifications SHA (9/9 conformes, avant tout calcul).** Base
immunitaire, axe, pipeline v6.2, RDS pdacR, sampInfo, transcriptions
`purity_861_external.csv` et `deconvolution_860_external.csv`, scores
§8.54, externe §8.55 — tous conformes aux valeurs gelées au
protocole §2.

**Jointure par patient (12 caractères), puis par échantillon (15).**
178/178 tumeurs du projet appariées (0 collision de clé des deux
côtés) ; fraction leucocytaire par méthylation non nulle pour
**150/178 (84,3 %)** — au-dessus du seuil gelé (≥ 100) ; toutes les
valeurs dans [0, 1] (min 0,0212, médiane 0,2491, moyenne 0,2590,
écart-type 0,1519, max 0,8081). **Porte L OUVERTE.** Les 3 échantillons
externes hors projet sont les mêmes qu'aux §8.55/§8.61
(TCGA-HZ-A9TJ-06A, métastase ; TCGA-H6-8124-11A et TCGA-YB-A89D-11A,
tissu normal adjacent) — correctement exclus par le critère « tumeurs
primaires code 01 ». Les 28 tumeurs sans fraction leucocytaire sont
les non-whitelistées de Raphael, comme aux §8.55/§8.60/§8.61 (une
seule tumeur, TCGA-2J-AAB9-01A-11R-A41B-07, a METH/leuco mais pas
ABSOLUTE — c'est pourquoi `purity_855_external.csv` ne compte que
149 lignes : la jointure ABSOLUTE du §8.67.4 utilise un `reindex`
tolérant, documenté dans le script).

**Égalité des transcriptions (assertée en machine).** La colonne
leucocytaire re-dérivée du sampInfo est IDENTIQUE (tolérance 10⁻⁹)
aux deux transcriptions détenues du projet : `purity_861_external.csv`
(colonne `leukocyte_methyl_percent`) et
`deconvolution_860_external.csv` (colonne
`Leukocyte_fraction_methylation_Raphael`) — deux transcriptions
indépendantes du même sampInfo s'accordent à la décimale près.

**Cohérence (vérifications, pas des tests du verdict).** Fraction
leucocytaire par méthylation vs imogimap : **r = +0,9947 (n = 150,
p = 3,4×10⁻¹⁴⁸)** — reproduction EXACTE à 4 décimales de la valeur
du §8.60 (0,9947) ; vs ImmuneScore : r = +0,8193 (n = 150, réf.
§8.60 : 0,8193) ; vs ABSOLUTE : r = −0,6901 (n = 149, réf. §8.60 :
−0,6901). Trois vérifications reproduites à la décimale près : une
erreur d'identification ou de transcription est invraisemblable.

**Sélection (effet nommé, comme aux §8.55/§8.60/§8.61).** La cohésion
brute sur n = 150 est déjà plus faible qu'à n = 178 (**0,5035 contre
0,5563, −0,0528 par la seule sélection**) — toutes les comparaisons
T2 se font sur le même n = 150, brute recalculée, jamais en mélangeant
les n.

## 8.67.3 T1-L2 — Chaque flux immunitaire suit la fraction leucocytaire : fortement (re-vérification exacte)

Pearson r (+ Spearman ρ) de chaque flux contre la fraction
leucocytaire (n = 150) ; p brutes bilatérales, sans correction pour
tests multiples (12 tests — le jugement porte sur la moyenne, pas sur
une p isolée).

| Gène | r leuco (p) | ρ leuco | R² leuco |
|---|---|---|---|
| CD8A | **+0,660 (4,3×10⁻²⁰)** | +0,641 | **0,435** |
| CD8B | +0,582 (5,7×10⁻¹⁵) | +0,552 | 0,339 |
| CD4 | +0,614 (6,2×10⁻¹⁷) | +0,612 | 0,377 |
| FOXP3 | +0,687 (3,1×10⁻²²) | +0,649 | 0,471 |
| CD68 | +0,220 (6,9×10⁻³) | +0,227 | 0,048 |
| CD163 | +0,483 (4,0×10⁻¹⁰) | +0,518 | 0,233 |
| CD274 | +0,276 (6,2×10⁻⁴) | +0,298 | 0,076 |
| PDCD1 | +0,704 (9,3×10⁻²⁴) | +0,652 | 0,496 |
| CTLA4 | **+0,713 (1,4×10⁻²⁴)** | +0,672 | **0,508** |
| GZMB | +0,581 (6,2×10⁻¹⁵) | +0,556 | 0,338 |
| IFNG | +0,325 (5,0×10⁻⁵) | +0,348 | 0,106 |
| CD19 | +0,702 (1,3×10⁻²³) | +0,628 | 0,493 |

**Moyenne |r| = 0,5456** (Spearman 0,5294) — écart de −0,00003 avec
le §8.60 (0,5456) : **reproduction exacte**, dans la tolérance gelée
(± 0,005). Lien SUBSTANTIEL (≥ 0,30, dépassé de 82 %). Tous
significatifs à p ≤ 0,0069 (12/12 ; le plus faible est CD68,
r = 0,220). R² médian 0,3580, maximum 0,5082 (CTLA4). À comparer :
ImmuneScore 0,7164 (§8.54), ABSOLUTE 0,4932 (§8.55), METH 0,4228
(§8.61) — la fraction leucocytaire se place entre l'ImmuneScore et
ABSOLUTE. Les 12 corrélations sont POSITIVES — le sens attendu : plus
de leucocytes estimés, plus de signal immunitaire. CD68 est
l'exception comme partout (r = 0,220, R² = 4,8 %) — les macrophages
suivent moins l'infiltration que les lymphocytes, quelle que soit la
mesure.

## 8.67.4 T2-L2 — La corrélation chute d'un tiers, ni plus ni moins (re-vérification exacte) + sensibilités

Matrice 66 paires, sur les n = 150 appariées (la brute de référence est
recalculée sur ce sous-ensemble, jamais importée du §8.54 ou du §8.60).

| Matrice | Pearson moyenne \|r\| | médiane \|r\| | fraction \|r\| > 0,5 | max \|r\| |
|---|---|---|---|---|
| Brute (n = 150) | **0,5035** | 0,5422 | 0,561 (37/66) | 0,8526 |
| Résidus [1, leuco] (PRIMAIRE) | **0,3372** | 0,3256 | **0,167 (11/66)** | 0,7669 |
| Résidus [1, LF imogimap] (sens.) | 0,3311 | — | 0,167 (11/66) | — |
| Résidus [1, ImmuneScore] (J1) | 0,2273 | — | — | — |
| Résidus [1, leuco, ImmuneScore] (J1) | 0,2136 | — | — | — |
| Brute (n = 149, J2) → résidus [1, ABSOLUTE] | 0,5040 → 0,3757 | — | — | — |
| Résidus [1, leuco] (J2, n = 149) | 0,3378 | — | — | — |
| Résidus [1, leuco, ABSOLUTE] (J2) | 0,3213 | — | — | — |

**Chute primaire : 33,0 %** (0,5035 → 0,3372) — écart de 0,0000 avec
le §8.60 : **reproduction exacte**, dans la tolérance gelée (± 0,005).
Critère gelé : ni EFFONDREMENT (résiduelle 0,3372 > 0,30 ; chute
33,0 % < 45 %) ni PERSISTANCE (chute 33,0 % > 20 % ; résiduelle
0,3372 < 0,80 × 0,5035 = 0,4028) : **T2-L2 = PARTIELLE**. Retirer
linéairement toute la fraction leucocytaire retire un tiers de la
corrélation — et en laisse deux tiers. La fraction de paires fortes
passe de 37/66 à 11/66.

**Sensibilité T2-L-imog (robustesse à la mesure).** Résidus sur la
fraction leucocytaire imogimap (Thorsson, ARN — r = 0,9947 avec la
méthylation) : 0,5035 → **0,3311 (chute 34,2 %)**, même fraction
> 0,5 (11/66). La part d'un tiers est robuste à la mesure de la
fraction leucocytaire : deux voies quasi identiques donnent le même
chiffre à 1,2 point près. (Limite : la voie imogimap est calculée
depuis l'ARN, donc non indépendante des flux — c'est une sensibilité,
pas une preuve.)

**Conjointe T2-J1 (leucocytes + ImmuneScore, n = 150).** ImmuneScore
seul : 0,5035 → **0,2273 (chute 54,9 %)** — moins que les −64,0 % du
§8.54 à n = 178, parce que la brute est déjà plus faible à n = 150
(0,5035 contre 0,5563) ; la comparaison se fait dans le même n.
Conjoint [leuco, ImmuneScore] : 0,5035 → **0,2136 (chute 57,6 %)**,
soit un gain de **2,7 points** seulement au-delà de l'ImmuneScore
seul. Critère gelé : dans [−2, +2] points = rien ajouté ; ≥ +10
points = part indépendante. **2,7 points est entre les deux** :
la fraction leucocytaire n'ajoute presque rien au-delà du score
global — elle est presque entièrement contenue dans ce que mesure
l'ImmuneScore — mais pas rigoureusement rien. Lecture honnête :
marginale, en dessous du seuil d'indépendance.

**Conjointe T2-J2 (leucocytes + ABSOLUTE, n = 149).** ABSOLUTE seul :
0,5040 → **0,3757 (chute 25,5 %)** — reproduction EXACTE du §8.55
à n = 149. Leuco seul (n = 149) : → 0,3378 (chute 33,0 %).
Conjoint [leuco, ABSOLUTE] : 0,5040 → **0,3213 (chute 36,3 %)**,
soit un gain de **10,8 points** au-delà d'ABSOLUTE seul. Critère
gelé : ≥ +10 points = part indépendante. **10,8 points dépasse le
seuil, de justesse** : la fraction leucocytaire porte une part
INDÉPENDANTE de la pureté ABSOLUTE — de justesse, à dire comme telle
(0,8 point au-dessus du seuil, pas une marge confortable).

## 8.67.5 T3-L2 — Couplage prédit : la régression §8.48 tient, avant comme après — et le plancher de L-ORD

Couplage C par contrôle immunitaire (moyenne des |r| avec les 11 autres
flux), brut contre résidualisé sur `leuco` ; d_ssep prédit par
d = −0,175 + 1,705·C.

| | C moyen | d_ssep prédit moyen |
|---|---|---|
| Brut (n = 150) | 0,5035 | **0,6835** |
| Résidualisé [leuco] | 0,3372 | **0,4000** |

CD8A seul : C 0,6056 → 0,4199, d_pred 0,8575 → **+0,5409** (c'est la
prédiction L-RES). Le T3-L2 ne fait que traduire T2-L2 en S_sep
prédit ; le verdict se joue au T5-L2.

**Le plancher de L-ORD (point de méthode, gelé au protocole §5).**
Les résidus OLS sur [1, leuco] sont ORTHOGONAUX à `leuco` par
construction : la moyenne |r| entre la fraction leucocytaire brute
et les 12 flux résidualisés vaut **C_ord = 2,75×10⁻¹⁶** (zéro à la
précision machine, flux par flux entre 10⁻¹⁷ et 10⁻¹⁶) — donc
d_pred(L-ORD) = −0,175 + 1,705 × 0 = **−0,1750**. Ce n'est pas une
prédiction au sens ordinaire : c'est le plancher LINÉAIRE. Toute
séparation en L-ORD (écart ≥ 0,45) ne pourrait venir QUE d'une
structure NON LINÉAIRE (seuil, saturation, interaction) entre la
fraction leucocytaire et les résidus — et un écart ≈ 0 confirme que
la régression linéaire a épuisé tout l'ordonnancement leucocytaire.
C'est ce qui rend L-ORD décisif comme garde-fou : il teste le reste
non linéaire, pas le linéaire déjà retiré.

## 8.67.6 T4-L — Stratification : la cohésion persiste dans chaque moitié — et la moitié basse EST une bande étroite

Médiane de la fraction leucocytaire = 0,2491 (n = 75/75) ; matrice
intra-famille dans chaque moitié.

| Stratification | Moitié haute : moyenne \|r\| (frac. > 0,5) | Moitié basse : moyenne \|r\| (frac. > 0,5) |
|---|---|---|
| Leuco (méd. 0,2491) | 0,4559 (0,470, 31/66) | 0,3856 (0,288, 19/66) |

La cohésion persiste dans les deux moitiés (0,46 et 0,39, contre
0,5035 global) — réduite, pas effondrée. Ici la moitié BASSE est une
vraie bande étroite : l'écart-type de la fraction leucocytaire y est
de 0,0628, soit **41,3 % de l'écart-type global (0,1519)** — sous le
seuil gelé de 50 %. Dans cette bande où la fraction leucocytaire est
quasi fixée (basse et resserrée), la cohésion reste à **0,3856
(76,6 % de la brute, chute 23,4 %)** : ni effondrement (< 0,30,
critère H1-leu) ni persistance (≥ 0,80 × brute = 0,4028, critère
H0-leu) — **intermédiaire, à 0,0172 sous le seuil de persistance**.
La moitié haute est large (écart-type 81,7 % du global) et persistante
(0,4559, 90,5 % de la brute). **T4-L ne tranche pas seul** : il
soutient H0-leu par une voie non paramétrique, indépendante de toute
linéarité — fixer la fraction leucocytaire en bande étroite ne tue
pas la cohésion — mais il ne remplit pas le critère gelé de
persistance dans la bande étroite, et n'entre donc pas comme condition
du verdict NON. Il est rapporté tel quel, sans arrondissement de
seuil.

## 8.67.7 T5-L2 — Runs v6.2 : la séparation survit à 57,6 %, l'ordonnancement leucocytaire est mort

Prédictions calculées AVANT de lire les sorties (depuis T1-L2/T2-L2
du jour) : L-RES d_pred +0,5409 (C_résid CD8A = 0,4199) ; L-ORD
d_pred −0,1750 (C_ord = 2,75×10⁻¹⁶, plancher linéaire, §8.67.5).
4 runs v6.2, mode fast, graine 42, **4/4 exit 0** (lot 18:09:33–
18:30:58 UTC 20 nov., unité unique `v62-leuko-867`, aucune
interruption, aucun redémarrage machine pendant le lot — boot
~17:22 UTC, avant le lot).

| Run | Contrôle → analysés | S_sep réel | S_sep nul | Écart | Prédit | MC réel / nul | Delta réel / nul | w | t0 |
|---|---|---|---|---|---|---|---|---|---|
| L-RES | CD8A résid. → 11 imm. résid. | 0,7771 | 0,2109 | **+0,5662** | +0,5409 | 0,4140 / 0,3321 | 3,44 / 3,42 | 26 | 49,30 % |
| L-ORD | leuco brute → 12 imm. résid. | 0,2214 | 0,2313 | **−0,0099** | −0,1750 | 0,3346 / 0,3365 | 3,50 / 3,43 | 26 | 67,57 % |

Lecture par critère gelé :
- **L-RES : la séparation survit réduite, presque exactement comme
  prédit.** Écart +0,5662 contre +0,9838 pour CD8A brut (**57,6 %
  conservés, baisse de 42,4 %**) et contre +0,5409 prédit (**+0,0253
  au-dessus — la régression §8.48 prédit bien le résiduel ici**,
  contrairement à METH au §8.61 où elle le surestimait de 0,1505).
  MC sépare aussi (+0,0819 : 0,4140 contre 0,3321) ; Delta quasi égal
  (3,44 contre 3,42) — noté, non utilisé pour le verdict (Delta non
  élucidé, §8.49). L7a sépare en direction (up 0,3871 contre down
  −0,3932) : non utilisé, comme au §8.48/§8.54/§8.60/§8.61. Seuil à
  mi-course (t0 = 49,30 %). Critère gelé : L-RES ∈ [0,30 ; 0,70[ →
  **soutient PARTIEL, seul**. Il n'est ni < 0,30 (PORTE) ni ≥ 0,70
  (NE PORTE PAS).
- **L-ORD : la fraction leucocytaire n'ordonne plus rien.** Écart
  −0,0099 — le NUL est devant de 0,0099 (réel 0,2214 contre nul
  0,2313) ; MC ne sépare pas (−0,0019 : 0,3346 contre 0,3365, nul
  devant aussi). C'est le plancher attendu (§8.67.5) : les résidus
  sont orthogonaux à `leuco` par construction, et AUCUNE structure
  non linéaire ne vient les réordonner par la fraction leucocytaire.
  Critère gelé : L-ORD < 0,30 → **soutient H1-leu, seul** (au sens
  du critère : plus rien n'est ordonné par la fraction leucocytaire
  une fois fixée) ; L-ORD ≥ 0,45 aurait soutenu H0-leu. Le contraste
  avec D-LEU (+0,7129, §8.60) est total : ordonner les flux BRUTS
  par la fraction leucocytaire sépare fortement ; ordonner les flux
  RÉSIDUALISÉS par la même fraction ne sépare plus du tout.
- **Les deux runs ensemble disent deux choses différentes, et c'est
  le résultat.** L-ORD ≈ 0 dit que la fraction leucocytaire a tout
  donné : son ordonnancement est épuisé par la régression. L-RES =
  +0,5662 dit que la co-expression restante, elle, ne vient pas de
  la fraction leucocytaire : les résidus se séparent entre eux
  (par CD8A résidualisé) sans être ordonnés par la fraction
  leucocytaire. Un porteur aurait tué les deux ; un simple corrélat
  n'aurait tué aucun des deux ; la fraction leucocytaire tue l'un
  et pas l'autre — **c'est la signature d'un porteur partiel**.

## 8.67.8 Verdict de synthèse — PARTIEL

Règle gelée, test par test : T1-L2 = lien substantiel (moyenne |r|
0,5456, reproduction exacte du §8.60) ; T2-L2 = PARTIELLE (chute
33,0 %, reproduction exacte) ; T2-L-imog = chute 34,2 % (robuste à
la mesure) ; T2-J1 = gain 2,7 points (marginal, entre « rien ajouté »
et « part indépendante ») ; T2-J2 = gain 10,8 points (part
indépendante d'ABSOLUTE, de justesse) ; T4-L = persistance dans la
moitié haute (90,5 %), intermédiaire dans la bande étroite basse
(76,6 %, ni effondrement ni persistance) ; L-RES = **+0,5662**
(∈ [0,30 ; 0,70[) ; L-ORD = **−0,0099** (< 0,70).
**PORTE — DÉCISIF est rejeté** (L-RES n'est pas < 0,30).
**NE PORTE PAS est rejeté** (L-RES n'est pas ≥ 0,70 ; T4-L n'est pas
une persistance dans les deux moitiés).
**Verdict gelé : PARTIEL** — L-RES ∈ [0,30 ; 0,70[ ET L-ORD < 0,70,
avec T2-L2 partielle en soutien. Aucun consensus exigé entre les
tests : chaque test est rapporté avec son propre critère ; le verdict
suit la règle ci-dessus, pas un vote.

**Ce que cela dit, et ce que cela ne dit pas.** (a) Cela dit que la
quantité de leucocytes porte un tiers de la corrélation
intra-famille immunitaire et tout son propre ordonnancement — et que
les deux tiers restants de la cohésion et 57,6 % de la séparation ne
sont PAS portés par elle. (b) Cela dit que la fraction leucocytaire
est presque entièrement contenue dans l'ImmuneScore global (gain
conjoint 2,7 points) mais porte une part indépendante d'ABSOLUTE
(gain 10,8 points) : elle n'est ni le score global, ni la pureté.
(c) Cela dit que la régression §8.48 prédit bien la séparation
résiduelle leucocytaire (+0,5409 prédit contre +0,5662 observé) —
elle encadre mal METH, bien la fraction leucocytaire : la prédiction
par couplage n'est pas universelle, elle dépend de la mesure.
(d) Cela ne dit pas que les deux tiers restants sont « biologiques »
au sens d'une régulation : ils peuvent venir d'une variable latente
non testée (état d'activation, sous-type moléculaire, stroma,
autres types conjoints). (e) Cela ne dit pas que l'infiltration est
expliquée : l'ImmuneScore global retire bien plus (−64,0 % de
cohésion, 20,2 % de séparation conservés) — ce qu'il capte au-delà
de la quantité de leucocytes reste ouvert (§8.67.10). (f) La
domination IMMROT du §8.48 n'est pas remise en cause : elle reste
expliquée par le couplage, dont la cause amont est désormais
précisée — le couplage est porté pour un tiers par la quantité de
leucocytes, pour le reste par ce que mesure le score global.

**Comparaison directe des porteurs (mêmes définitions, n apparié noté) :**

| Test | §8.54 ImmuneScore (n = 178) | §8.60 TOP1 B naïfs (n = 151) | §8.55 ABSOLUTE (n = 149) | §8.61 METH (n = 150) | §8.67 Leuco (n = 150) |
|---|---|---|---|---|---|
| T1 moyenne \|r\| | 0,7164 | 0,3314 | 0,4932 | 0,4228 | **0,5456** |
| T2 brute → résiduelle | 0,5563 → 0,2002 (−64,0 %) | 0,5044 → 0,4805 (−4,7 %) | 0,5040 → 0,3757 (−25,5 %) | 0,5035 → 0,4235 (−15,9 %) | **0,5035 → 0,3372 (−33,0 %)** |
| T2 verdict | EFFONDREMENT | PERSISTANCE | PARTIELLE | PERSISTANCE | **PARTIELLE** |
| T5 contrôle → flux | I-IMM +1,1942 | D-TOP1 +0,5867 | E-ABS +0,6911 | M-METH +0,6739 | D-LEU +0,7129 (§8.60) |
| T5 résidualisé | I-RES +0,1982 (20,2 %) | D-RES +0,7692 (78,2 %) | E-RES +0,6499 (66,1 %) | M-RES +0,5427 (55,2 %) | **L-RES +0,5662 (57,6 %)** |
| T5 ordonne les résidus | — | — | — | — | **L-ORD −0,0099** |
| Verdict | H1 SOUTENUE | ZONE GRISE | H1 PARTIELLE | ZONE GRISE | **PARTIEL** |

## 8.67.9 Provenance

- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant les calculs, dans le log du lot, et après
  l'extraction). Mode `fast`, graine 42 (défaut), nul = bloc analysé
  permuté conjointement, graine 42 (default_rng frais par fichier),
  contrôle intact.
- **Protocole.** `PROTOCOL_leukocyte_decisive_867.md`, SHA-256
  `571adf826f455b8dfd49c63f2c0e94fc73a7ae03a6e98b5bfda2bb0648ae59ad`,
  gelé le 20 nov. 2026 avant tout calcul nouveau et avant tout run de
  ce chantier. Aucun amendement après le gel.
- **Entrées externes.** (1) Raphael et al. 2017, Cancer Cell
  32:185–203.e13 (PMID 28810144, PMCID PMC5964983, DOI
  10.1016/j.ccell.2017.07.007, Table S1), via pdacR (Torre-Healy et
  al. 2023, doi 10.1038/s42003-023-04461-6), `data/TCGA_PAAD.rds`,
  SHA-256 `52020679350d1539d7516f7d38f7bf09e510225eba2f228a4fe874f3c496ea76`
  (12 311 529 octets ; URL
  `https://raw.githubusercontent.com/rmoffitt/pdacR/master/data/TCGA_PAAD.rds`) ;
  transcription `purity_855_sampinfo.csv`, SHA-256
  `7a09dde3d374d1afb64f1d1d053193fc884c04d62e63e519fcf4dbf17378b014`.
  (2) Thorsson et al. 2018, Immunity 48:812–830.e14 (PMID 29628290,
  PMCID PMC5982584, DOI 10.1016/j.immuni.2018.03.023), fractions
  CIBERSORT via le miroir imogimap (Korkut lab), `.rda` SHA-256
  `f576f5f2…a4e68289` (§8.60.10) — sensibilité seulement.
  (3) Scores ESTIMATE calculés au §8.54, `infiltration_854_scores.csv`,
  SHA-256 `628732ecbcc30a3281b0df7a5039ec2520a1c5f1a1ae9ce412c4d0d7caf78aa7`.
- **Entrées du projet.** Tarball TCGA-PAAD RSEM, MD5
  `b09569ce3f4721f514bc137bd109ac0a` (vérifié) ; base immunitaire
  `pdac_immune_tcga_fluxes.csv`, SHA-256
  `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e` ;
  axe `immune_kras_order_tcga.csv`, SHA-256
  `31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d` ;
  transcriptions `purity_861_external.csv`, SHA-256
  `cf127ef7310b35483c7fa7712fe69bf07a858726fb44f2d4e05613acc575d24b`,
  et `deconvolution_860_external.csv`, SHA-256
  `438d677aded8eaf74504f8bd89bfc2e578df32b4b31c64e94e64120b0f22d9cf` ;
  externe §8.55 `purity_855_external.csv`, SHA-256
  `03f34fe07a18ff106e21ce9028ef9ff60d3d95889c3064898442246e486fbd6f` ;
  écarts §8.44/§8.54/§8.55/§8.60/§8.61 relus en machine
  (`ssep_844_rotations.csv`, `infiltration_854_runs.json`,
  `purity_855_runs.json`, `deconvolution_860_runs.json`,
  `purity_861_runs.json` ; CD8A : réel 1,2310, nul 0,2472, écart
  +0,9838 ; I-RES +0,1982 ; E-RES +0,6499 ; D-RES +0,7692 ;
  D-LEU +0,7129 ; M-RES +0,5427).
- **Nature des lignes.** Les flux immunitaires sont des mesures
  instrumentales (séquençage ARN, log2(RSEM+1), brutes) ; la fraction
  leucocytaire par méthylation est une estimation publiée depuis
  l'ADN (indépendante de l'ARN) ; la fraction imogimap est une
  estimation publiée depuis l'ARN (déconvolution CIBERSORT — non
  indépendante des flux, sensibilité seulement) ; les résidus sont des
  valeurs calculées (OLS) ; les nuls sont des lignes permutées
  (graine 42) — des échantillons hypothétiques, pas des mesures.
  Aucun mot humain, aucun échantillon hypothétique dans les séries
  réelles. Les 28 tumeurs sans fraction leucocytaire sont des valeurs
  manquantes publiées (non-whitelistées de Raphael), pas des zéros —
  exclues en complete-case, jamais imputées.
- **Sorties et scripts de ce chantier.**
  `analyze_leukocyte_867.py` (SHA
  `d6b5f506c350850f1188f9f11077d3dc8f81c5254ba6bd36008b71dc513ffcb7`) :
  porte L, jointure, T1-L2–T4-L, sensibilités, prédictions T3-L2.
  `build_leukocyte_867.py` (SHA
  `2863c4a14681abc9922be50a0546264b51cef7980cf9cdd91433144c510ed86f`) :
  4 CSV T5-L2 (résidus vérifiés : moyenne |r| = 0,3372, identique à
  T2-L2 ; orthogonalité C_ord = 2,75×10⁻¹⁶).
  `extract_leukocyte_867.py` (SHA
  `2e4eee4e4e8dbb33491ee901f164b31a8bca9e9d8b45b3dc10e468d37e749b03`) :
  lecture des 4 runs (SHA des CSV vérifiés, version
  `v6.2.0-L7aL7b-CohenD-short`).
  `leukocyte_867_external.csv` (SHA
  `2114e71bd05a7297d6b9f4d4efa20c644fb5f44f00930dbfbcfef9edf32cb815`,
  150 tumeurs : sample, fraction leucocytaire méthylation + imogimap,
  ImmuneScore, ABSOLUTE, METH),
  `leukocyte_867_results.json` (SHA
  `b8ed9eb5cc018caff225356c0d0be568817168a3c1346625b16a1d12eb3b3670`,
  T1-L2–T4-L + sensibilités),
  `leukocyte_867_results.csv` (SHA
  `0a54697ab49dc7f3b0e2acf348b0a8d880967691cf00248225265f6804c6c9e3`,
  T1-L2 par flux),
  `leukocyte_867_predictions.json` (SHA
  `1b405ee9eb1fd2c7a888a72430a88476cffc8c5db759397f6b2e795eaeb3cf1c`,
  T3-L2, écrit AVANT les runs),
  `leukocyte_867_immune_resid.csv` (SHA
  `9ee6e743482476cafe10876f83216bea8571b8338ba29a98bb9de65884b6a518`,
  12 flux résidualisés),
  `leukocyte_867_csv_sha.json` (SHA
  `92d02c084e80c143bc9a5d389ada4d00ff97ff816c85ba2bc7c1af45ae40b731`,
  SHA des 4 CSV T5-L2),
  `leukocyte_867_runs.json` (SHA
  `c761afbdf91f1a8bed4e16e6bd75df8bee83390c066046dc50b5a095fa883e2c`) /
  `.csv` (SHA
  `0b4a22009632cf55de55b79efccffdfbbf0f33c796cb65f0a015f127748d9822`,
  4 runs). Manifeste `manifest_v62_leukocyte_867.txt`
  (SHA `2d2482c31297421b7ddaf0516bd1bfd52766e89d6dbbbcefba192f165b8b0e4a`) ;
  log `runs_v62_leukocyte_867.log`
  (SHA `93b00e49a56b1d4e7a23553b81ec00e693d37a69fcb03adbe31fab08668318ab`) ;
  unité systemd `v62-leuko-867`.
- **Ce qui manque :** relecture directe de la Table S1 de Raphael
  (défi PMC non contourné — trois vérifications de cohérence
  reproduites à la décimale près à la place, §8.67.2) ; METH,
  ABSOLUTE et la fraction leucocytaire partagent la même Table S1 —
  trois mesures, une seule table, pas trois sources indépendantes ;
  les p de T1-L2 sont brutes, sans correction pour tests multiples ;
  n effectif 150 pour ce chantier (sélection non-whitelist, §8.67.2) ;
  la résidualisation OLS ne retire que la part LINÉAIRE — un porteur
  non linéaire aurait survécu aux résidus, mais L-ORD ≈ 0 et T4-L
  intermédiaire excluent un reste non linéaire ordonné par la
  fraction leucocytaire (à la précision de ce test).

## 8.67.10 Ce qui manque, ce qui reste ouvert

- **Ce que l'ImmuneScore capte au-delà de la quantité de leucocytes.**
  Le score global retire −64,0 % de cohésion et ne laisse que 20,2 %
  de séparation ; la fraction leucocytaire, presque entièrement
  contenue en lui (gain conjoint 2,7 points), n'en retire que
  −33,0 % / 57,6 %. La différence — activation, état, types conjoints,
  stroma — est la prochaine question. Pistes : scores xCell par type
  (§8.60.11, toujours ouvert), signatures d'activation (IFNG,
  cytolytique) comme contrôles, StromalScore conjoint.
- **Les deux tiers restants après la fraction leucocytaire.** Ni
  portés par un type seul (§8.60), ni par la pureté seule (§8.55,
  §8.61), ni par la quantité de leucocytes (ici) : sous-type
  moléculaire (Bailey / Moffitt / Collisson — colonnes détenues dans
  le sampInfo, non testées ici, piste du §8.48.8), état d'activation,
  variable latente non testée.
- **Seuils limites.** Le gain conjoint T2-J2 (10,8 points) dépasse le
  seuil d'indépendance (10 points) de 0,8 point seulement ; le gain
  T2-J1 (2,7 points) tombe entre les deux bandes gelées ; la cohésion
  en bande étroite T4-L (0,3856) tombe à 0,0172 sous le seuil de
  persistance. Trois chiffres près de leurs seuils : à ne pas
  sur-interpréter — ils sont rapportés à la décimale près, avec leurs
  seuils, pour que le lecteur juge.
- **Survie par fraction leucocytaire.** La fraction jointe
  (`leukocyte_867_external.csv`, n = 150) permet de tester si elle
  prédit la survie — hors protocole gelé, non fait ici.
- **Incident d'exécution.** Aucun : lot unique, unité systemd
  `v62-leuko-867`, 18:09:33–18:30:58 UTC 20 nov., **4/4 exit 0,
  0 échec, 0 relance** (`=== FIN 2026-11-20T18:30:58Z deja_faits=0
  termines=4 echecs=0 ===` ; 4 lignes `EXIT_` à 0 dans le log).
  La machine avait redémarré AVANT le lot (boot ~17:22 UTC, uptime
  45 min à 18:06) ; aucun redémarrage pendant le lot (uptime 1 h 13
  à 18:35). Un correctif de script en cours de chantier : la jointure
  ABSOLUTE de `analyze_leukocyte_867.py` utilisait `.loc` sur
  `purity_855_external.csv` (149 lignes) et échouait sur la tumeur
  TCGA-2J-AAB9 (METH/leuco sans ABSOLUTE, §8.61.2) — corrigée en
  `reindex` tolérant AVANT tout calcul de test (le script n'avait
  produit aucune sortie de test avant la correction ; la porte L et
  les SHA étaient déjà validés).
- **Périmètre.** 4 nouveaux runs v6.2 au maximum (protocole §8),
  aucun autre. Aucun nouveau seuil proposé, aucun code modifié, aucun
  push GitHub dans ce chantier (publication sur go séparé ; règle
  permanente « Toujours github et pdf !!! » — par le coordinateur).

— Fin de la §8.67. —
