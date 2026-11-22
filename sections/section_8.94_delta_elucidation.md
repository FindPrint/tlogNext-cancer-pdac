### 8.94 Delta, nouvelle tentative d'élucidation — NON ÉLUCIDÉ (21–22 novembre 2026)

Go de Zackary « Faite tout cela » (21 nov. 2026 11h36, piste 2/4 — élucider
Delta, nouvelle tentative ; protocole gelé avant tout calcul neuf et tout
run neuf).

**Verdict d'abord, en quatre phrases. (a) NON ÉLUCIDÉ — quatrième
tentative, quatrième échec au critère gelé du §8.39 (≥ 90 % paires ET
≥ 90 % valeurs à ±0,10 en hold-out, mécanisme nommé et vérifié sur
l'ensemble B) : le meilleur modèle honnête prédit d_div à ±0,10 sur
13,5 % des runs en leave-one-cohort-out (30/222, référence ln n seul
du §8.62) et 9,7 % sur l'ensemble B (3/31), et l'identité de la paire
médiane sur 40,1 % des runs (89/222, kNN LOCO, angle A3). (b) L'élucidation
négative échoue elle aussi : le résidu Delta − F2(ln n) n'est pas du
bruit — il dépasse ±0,10 dans 53/106 paires (50,0 %, écart-type 0,536)
— et à w égal, Delta réel−nul reste dans ±0,10 sur 52/73 paires
seulement (71,2 %), sous la barre de 90 %. (c) Ce qui est établi :
w déplace Delta fortement (r = +0,603 ; la réplique Tier-2 fait passer
Delta de +0,21 à +1,13 entre w = 27 et w = 30 sur les 8 paires
principales, et l'écart réel−nul s'effondre à w égal : 8/8 paires dans
±0,10 à w = 27, 6/8 à w = 30) — mais ni w seul, ni ln n seul, ni
w + ln n ne prédisent le niveau en hold-out, et la structure des flux
ne choisit pas la paire. (d) Le déclencheur du pic étroit reste non
élucidé par cette voie : la position du split prédite par l'extrémité
non signée G tombe à ±2 pas du vrai pic dans 5/11 cas (niveau du
hasard), aucune statistique ne sépare rob-on de rob-off (AUC 0,23–0,47),
et le lot frais ne contient aucune courbe rob-on (P1 non testable, P2
en échec : 0 vrai positif, 23 faux positifs). Delta reste une piste
fragile et ne devient pas un discriminateur recommandé.**

## 8.94.1 Ce qui était acquis avant ce chantier

Le §8.39 avait clos la voie « variables structurelles » (meilleur
hold-out honnête 87,9 % paires / 81,8 % valeurs, H9e) et nommé la
structure : GraphDimension et PersistentHomology toujours les deux plus
basses (222/222), LocalPCA toujours 3e ou 4e (222/222), le choix se
jouant entre trois magnitudes continues séparées de ~0,5. Le §8.42
avait clos la voie « résumés de flux » (meilleur LOCO 68,9 % paires /
6,3 % valeurs ; `log(n)` meilleur trait unique pour 12 cibles sur 13)
et ouvert deux voies : modéliser depuis les séries entières, et la loi
d'échelle en n. Le §8.57 avait clos la voie « séries complètes »
(meilleur modèle honnête S2d : 89,2 % paires / 90,5 % valeurs en LOCO,
manquant le critère de 2 runs ; 89,4 % / 89,4 % en split, manquant de
1 run) et le §8.62 la loi d'échelle en n (F2 R² = 0,673 < 0,80 ;
LOCO R² = −0,005), en laissant ouvert le critère (ii) jamais testé
seul : le résidu Delta − F2(ln n) sépare-t-il réel de nul ? Le §8.63
avait expliqué M1 (MC haut = propriété de la permutation, Delta bas =
propriété de w = 27, écart +0,7 entre w = 27 et w = 30) en laissant
ouvert M1c (MC haut et Delta bas ont-ils une cause commune ?) et M2d
(réplication hors échantillon de l'optimiseur). Le §8.73 avait laissé
non élucidé le déclencheur du pic étroit (ni bloc extrême, ni ligne
unique). Ce chantier reprend les pistes non closes et ajoute trois
angles neufs, tous gelés avant tout calcul : Delta à w égal (A1),
le résidu après la loi en n (A2), la structure des flux (A3), et la
reprise du déclencheur du pic étroit (A4).

## 8.94.2 Méthode du chantier

Protocole gelé `PROTOCOL_delta_elucidation_894.md` (SHA
`79e5567c19d90cdd78d39f4d90888b5e8d00c5a25f56f7ac5789a8dd9bc5229d`,
vérifié par troncature du fichier à l'octet 9376 — voir Provenance),
écrit avant tout calcul neuf ; script Tier-1
`v62_delta_elucidation_894.py`
(SHA `6dc5db1a09a52da30885cf934cf4cdbef476d2f6c3ff3089557b8bc03ef9bc0f`),
log `v62_delta_elucidation_894.log` (21 nov. 2026 16:54–16:55).
Lecture seule des sorties détenues, aucun run du pipeline, aucun code
modifié. Ensemble gelé : 222 runs (156 v6.1 + 66 v6.2), 9 cohortes
(tcga 126, depmap 30, geo71729 20, geo62452 14, icgc 10, cptac 8,
hp35 6, coad 4, luad 4) ; ensemble B (§8.62) : 31 runs v6.2 fast,
31/31 valides. Pipeline v6.2
`universal_v6.2.0_cohen.py`, SHA
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
vérifié sur disque avant et après le chantier (v6.1
`2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`,
v6 `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`).

**Vérification préalable (dans le script, avant modélisation).**
Recomputation de `raw_median` depuis `df_feat.csv` : **2886/2886 à
10⁻⁶** (diagnostic C0, même construction que §8.57) ; identités
d_div / d_sat recalculées depuis les médianes parsées : **0 écart
> 10⁻³ sur 222/222** (div et sat) ; `df_feat.csv` présent dans
222/222 dossiers, `fluxes_raw.csv` présent dans 222/222, JSON et CSV
manquants : 0. Vérification préalable : OK. Les 185 dossiers v62
postérieurs (§8.47, §8.53) restent hors de l'ensemble gelé, comme
au §8.57.

**Barres gelées (§4 du protocole, identiques au §8.39 §5.4 — la barre
ne bouge pas).** ÉLUCIDÉ si et seulement si (a) l'identité de la paire
médiane est prédite sur ≥ 90 % des runs en hold-out (LOCO par cohorte)
ET (b) d_div est prédit à ±0,10 près sur ≥ 90 % des runs en hold-out
— avec le mécanisme NOMMÉ et VÉRIFIÉ sur l'ensemble B (transfert
≥ 90 % à ±0,10). ÉLUCIDATION NÉGATIVE (compte comme élucidation) si
A2 montre que le résidu Delta − F2(ln n) est du bruit (≥ 90 % des
paires |Δrésidu| ≤ 0,10) ET A1 montre qu'à w égal Delta ne sépare
pas : le mécanisme serait alors « Delta est une fonctionnelle de n et
de w, sans contenu de flux », vérifié sur B. NON ÉLUCIDÉ sinon, avec
la liste exacte de ce qui a été exclu. Aucune repondération, aucun
nouveau prédicteur, aucun changement de tolérance après coup. Un
modèle en échantillon ne compte jamais ; seul le hold-out compte.

**Correction de Zackary du 21 novembre 2026, 12h03 (portée : tout le
projet, précisée 12h04) — appliquée ici.** (1) Contrôle jamais
analysé : Tier 1 en lecture seule ; le Tier 2 reconstruit `df_feat`
depuis les CSV détenus avec les fonctions DU PIPELINE
(`replica_w_894.py`, calque de `replica_delta_863.py`) — la colonne
de contrôle (`step`) est exclue des flux analysés par construction
(pipeline, ligne 6787 : `c != control_col`), et la variable d'ordre
(KRAS pour les paires PDAC) est absente des colonnes de flux des CSV
sources, vérifié le 21 novembre 2026 sur les 15 CSV des paires
principales et A2. (2) Contrôles non monotones : aucun seuil n'a été
écarté dans le Tier 1 au motif de non-monotonie — A1 lit Delta à w
égal, A2 le résidu F2, A3 la structure des flux, A4 le pic étroit ;
si un contrôle non monotone donne un seuil différent, c'est de
l'information, pas une erreur. (3) Analyse, pas prédiction : le
verdict décrit ce que les angles testés montrent sur les données
détenues — il ne prédit rien, et Delta n'est jamais présenté comme
discriminateur tant qu'il n'est pas élucidé.

**Tier 2 — réplique à w fixe.** `replica_w_894.py`
(SHA `1677ec2500fdd96377220de311a6dcd5fc8c05b0ddd47ea3fd7adea1a005d781`),
sortie `replica_w_894.json`
(SHA `a3ba1536e36ec23a7ce3ceabd1016a7930521fd8d74a53d50495128eac90730c`) ;
première fin exit = 0 le 21 nov. 2026 19:09:40Z (file
`queue_893_896`, étape 2), 12 passages exit = 0 au total, dernière
réécriture le 22 nov. 2026 12:33:17Z — le fichier relu est cette
dernière réécriture, la calibration étant exacte à chaque passage.
Calibration : reproduction du D_vector stocké (d_sat, d_crit, d_div,
d_null) à |Δ| < 10⁻⁶ pour chacun des 16 CSV à son w propre — **16/16,
écart maximal 0,0** (ex. TCGA v4 réel : d_div répliqué 5,754216 =
stocké, Delta 4,181387 ; HP35 réel : d_div 6,018889, Delta 4,482534).
Puis croisement w ∈ {27, 30} sur les 8 paires principales V1 (§8.56) :
16 CSV × 2 w = 32 builds. Résultats au §8.94.3.

## 8.94.3 A1 — Delta à w égal : w déplace Delta, mais ne le prédit pas

**Tier 1 (222 runs, 106 paires réel/nul).** w récupéré sur 222/222
runs, 0 manquant ; w de 10 à 89, médiane 30, 17 valeurs distinctes —
w = 30 dans 105 runs, w = 10 dans 22, w = 16 dans 21, w = 26 dans 12,
w = 27 dans 10. Paires à w égal des deux côtés : **73/106** (68,9 %) ;
les 33 autres paires ont un w différent entre réel et nul et sont
exclues de la comparaison à w égal. Sur ces 73 paires :
|Delta_réel − Delta_nul| ≤ 0,10 sur **52/73 (71,2 %)**, moyenne
+0,036, écart-type 0,199 ; écart > 0,07 (réel > nul) sur 24/73,
|écart| > 0,07 sur 30/73. La barre de 90 % n'est pas atteinte, dans
les deux sens : ni « Delta sépare à w égal » (l'écart dépasse 0,10
sur 21/73 paires seulement, 28,8 %, loin des ≥ 90 % exigés pour le
mécanisme « le niveau est choisi par w »), ni « Delta ne sépare pas
à w égal » au sens gelé de l'élucidation négative (71,2 % < 90 %).
Corrélations sur les 222 runs : r(Delta, w) = **+0,603**,
r(d_div, w) = **+0,631**, r(Delta, ln n) = **+0,774** — ln n reste
le corrélat simple le plus fort, devant w.

**Prédiction de d_div en LOCO (barre : ≥ 90 % à ±0,10).**

| Modèle (d_div) | ±0,10 en LOCO | MAE |
|---|---|---|
| 1 + ln n (référence §8.62) | 30/222 (13,5 %) | 0,974 |
| 1 + w + ln n | 21/222 (9,5 %) | 1,026 |
| 1 + w + ln n + (ln n)² | 4/222 (1,8 %) | 1,172 |
| 1 + w seul | 0/222 (0,0 %) | 1,200 |

Par pli, le modèle 1 + w + ln n atteint 20/30 (66,7 %) sur depmap
et 1/126 (0,8 %) sur tcga, 0 % partout ailleurs ; la référence
1 + ln n atteint 30/30 (100 %) sur depmap et 0/192 ailleurs — un
artefact de cohorte (n fixe dans depmap), pas un mécanisme. Pour
Delta lui-même, c'est pire : 0/222 (1 + w + ln n, MAE 1,031),
3/222 (1,4 %, avec (ln n)², MAE 1,222), 1/222 (0,5 %, 1 + ln n,
MAE 0,978), 0/222 (1 + w seul, MAE 1,120). **Transfert sur
l'ensemble B (n = 31)** : d_div 3/31 (9,7 %, MAE 0,767) avec
1 + w + ln n comme avec (ln n)² (MAE 0,677) ; Delta 1/31 (3,2 %,
MAE 0,742) et 4/31 (12,9 %, MAE 0,679). Aucun modèle, aucun
hold-out, aucun transfert ne s'approche de 90 %.

**Tier 2 — le croisement w = 27 / w = 30 (8 paires principales).**
À w = 27, |écart réel−nul| ≤ 0,10 sur **8/8 paires** (écarts :
HP35 +0,0017 ; TCGA v4 +0,0453 ; GSE71729 +0,0383 ; GSE62452
−0,0276 ; ICGC +0,0340 ; IMMUNE_TCGA +0,0032 ; PARP_TCGA +0,0700 ;
DEPMAP −0,0415) ; à w = 30, **6/8** (TCGA v4 +0,4157 et PARP_TCGA
+0,2616 dépassent ±0,10 ; les 6 autres restent dans ±0,10, dont
HP35 +0,0679 et ICGC −0,0630). Le passage w = 27 → w = 30 déplace
Delta de **+0,21 à +1,13** sur les 8 paires (réel TCGA v4 :
3,156 → 4,181 ; réel IMMUNE_TCGA : 3,143 → 4,210 ; réel PARP_TCGA :
3,164 → 4,299 ; DEPMAP : 0,000, d_div plafonné à 3,0 aux deux w).
Rappel §8.63, confirmé : l'écart Delta s11111 − réel tombe à
+0,0238 à w = 30 et −0,0718 à w = 27, contre l'écart brut du §8.63 ;
l'écart w27 − w30 vaut −0,7165 (réel), −0,812 (s11111), −0,7099
(s123). Lecture : w est bien le moteur du niveau de Delta — à w
fixé, l'écart réel−nul s'effondre sur les 8 paires principales —
mais sur l'ensemble des 106 paires le compte à w égal (71,2 %)
reste sous la barre gelée, et le niveau lui-même n'est pas
prédictible à ±0,10 en hold-out. A1 exclut « w seul choisit le
niveau » au sens du critère ≥ 90 %, sans établir l'élucidation
négative.

## 8.94.4 A2 — Le résidu après la loi en n n'est pas du bruit

F2(ln n) reprise du §8.62, coefficients gelés NON ré-estimés :
F2 = −12,896435 + 5,27966·ln n − 0,402319·(ln n)² (R² §8.62 =
0,6725). Résidu R = Delta − F2(ln n), sur les 106 paires :
|R_réel − R_nul| ≤ 0,10 sur **53/106 (50,0 %)**, moyenne +0,077,
écart-type 0,536. Critère A2 (≥ 90 % à ±0,10 ET |moyenne| ≤ 0,10) :
**NON ATTEINT** — la moyenne passe (+0,077), la fraction échoue
de 40 points.

Fait de construction, consigné plainement : dans chaque paire, les
deux côtés ont le même n, donc F2(ln n) s'annule exactement —
écart maximal |ΔDelta − ΔR| = **0,00e+00** sur les 106 paires, et
|Delta_réel − Delta_nul| ≤ 0,10 vaut aussi 53/106. A2, tel que
gelé, se réduit donc au test de l'écart brut de Delta entre réel
et nul : dans la moitié des paires, Delta diffère de plus de 0,10
entre une matrice et sa permutation. **Delta porte quelque chose
au-delà de n** — ou, à tout le moins, quelque chose que la loi en
n ne capture pas — dans la moitié des paires. L'élucidation
négative (« Delta est une fonctionnelle de n et de w, sans contenu
de flux ») est exclue par ce seul angle, quelle que soit la
lecture de A1. Le critère (ii) du §8.62, jamais testé seul, est
désormais testé : il échoue.

## 8.94.5 A3 — La structure des flux ne choisit pas la paire

Prédicteurs calculés depuis `fluxes_raw.csv` + `df_feat.csv` SANS
recalculer les estimateurs (piège de circularité du §8.57 §3) :
p (nombre de flux), n, dispersion inter-flux (écart-type des
médianes de flux), corrélation moyenne intra-famille, part de
variance du premier axe (PCA sur les flux bruts), asymétrie (skew)
moyenne des flux. Features calculées sur 222/222 runs, 0 manquant.

(a) Identité de la paire médiane (kNN k = 5, LOCO) : **89/222
(40,1 %)** — barre 90 %. Par pli : coad 4/4 (100 %), icgc 10/10
(100 %), geo62452 8/14 (57,1 %), geo71729 12/20 (60,0 %), tcga
55/126 (43,7 %), cptac 0/8, depmap 0/30, hp35 0/6, luad 0/4.
(b) d_div à ±0,10 (ridge λ = 10, LOCO) : **0/222 (0,0 %)**,
MAE 1,928 (par pli : geo71729 0,408 ; geo62452 0,930 ; icgc 1,094 ;
luad 1,565 ; depmap 1,576 ; cptac 2,109 ; tcga 2,232 ; coad 2,665 ;
hp35 5,578). Pour mémoire, la distribution des paires dans
l'ensemble gelé : LocalPCA+MFA 99, LocalPCA+PCAIntrinsic 46,
LocalPCA+LevinaBickel 31, MFA+LocalPCA 30, LocalPCA 7, MFA 5,
PCAIntrinsic+LocalPCA 4 — LocalPCA figure dans la paire dans
217/222 runs, sans que sa magnitude soit prédictible.

Corrélations descriptives (pas un modèle) : n r = +0,485 (d_div) /
+0,473 (Delta) ; part de PC1 +0,443 / +0,430 ; corrélation moyenne
+0,365 / +0,353 ; dispersion inter-flux +0,302 / +0,291 ; skew
moyen −0,370 / −0,409 ; p +0,164 / +0,177. Aucun prédicteur de
structure ne s'approche du seuil : la voie « résumés de flux » du
§8.42, dans sa dernière variante (structure sans estimateur), est
close. Ce qui résiste n'est ni dans les résumés, ni dans les séries
(§8.57), ni dans w et ln n (A1) — et la paire elle-même n'est pas
choisie par la structure des flux.

## 8.94.6 A4 — Le déclencheur du pic étroit : la position du split ne tient pas

Reprise du §8.73, critères gelés repris tels quels (P1 ≥ 9/11,
P2 ≥ 9/11 — en pratique, qualification hors échantillon : succès
P1 si ≥ 70 % des pics frais à ±2 pas du candidat prédit par G,
avec ≥ 5 courbes rob-on fraîches ; succès P2 si AUC de H_max
≥ 0,80). Corpus relu : 82 courbes gagnantes (11 rob-on, 71
rob-off). Aucune statistique globale ne sépare rob-on de rob-off :
AUC G_max **0,233**, H_max **0,315**, E_max **0,405**, max e_ligne
**0,469** (11 contre 71) ; sur l'ensemble restreint du §8.73.3
(67 rob-off, rob < 0,05) : H_max 0,309 (p = 0,044, inversée),
E_max 0,400, max e_ligne 0,468 — même conclusion. La position du
pic n'est pas prédite par l'extrémité des lignes : le candidat
argmax G(c) tombe à ±2 pas du vrai pic dans **5/11 cas (45,5 %)**,
niveau du hasard sur ~11 candidats de bord.

Interventions relues (identiques au §8.73.4–§8.73.5, chiffres
inchangés) : A-swap (déplacer le bloc) **1/11** ; A1 (winsoriser
le bloc) 8/11 (2 fenêtres), 10/11 (4 fenêtres), 11/11 (8 fenêtres)
— avec l'avertissement du §8.73.7, inchangé : la winsorisation
déflate la variance et fait monter le maxsep dans 8/11 cas à
l'échelon 2 fenêtres, le critère gelé compte un effet générique,
pas la suppression d'un déclencheur ; A2 (winsoriser une seule
ligne) **4/11** ; contrôles B1 (propre bloc extrême au bord)
**0/6**, B2 (valeurs donneuses) **0/3**, B0 (bloc médian au bord)
**1/2**. Le déclencheur « position du split (extrémité non signée,
sans cohérence de signe entre flux) » échoue sur les deux critères
gelés : P1 = 5/11 < 9/11, et P2 n'est pas atteignable.

**Lot frais (celui du §8.73, s41–s60, relu — aucun lot neuf).**
Réplique des 240 courbes fraîches : écart **0,00e+00** (métriques
et courbes), ok. **0 courbe rob-on fraîche, 0 gagnante rob-on sur
20.** P1 : non testable (0/0, succes_70pc null) — comme prévu au
protocole quand il y a moins de 5 courbes rob-on fraîches. P2 :
140 courbes à T_H défini (100 exclues, T_H indéfini), H_max prédit
23 courbes rob-on — **0 réelle : TP = 0, FP = 23, FN = 0, TN = 117**,
AUC indéfinie (aucun positif), succes_auc_080 false. Le déclencheur
est consigné « non élucidable par cette voie » et le verdict global
reste NON ÉLUCIDÉ, comme le protocole l'exigeait si les deux
critères échouaient.

## 8.94.7 Lecture croisée : ce qui est exclu, ce qui reste ouvert

**Exclu par ce chantier (chiffres, pas d'adjectifs).** (1) w seul
choisit le niveau : LOCO d_div 0,0 % à ±0,10 avec w seul, 9,5 %
avec w + ln n ; transfert B 9,7 %. (2) ln n seul : F2 R² = 0,6725,
résidu non-bruit (53/106 à ±0,10). (3) w + ln n conjointement :
9,5 % LOCO, 9,7 % sur B. (4) La structure des flux : paire 40,1 %,
d_div 0,0 % en LOCO. (5) La position du split par l'extrémité non
signée G comme déclencheur du pic étroit : 5/11, AUC ≤ 0,47, P1
non testable et P2 en échec hors échantillon.

**Ce qui reste ouvert, non testé ici.** M1c (§8.63) — MC haut et
Delta bas ont-ils une cause commune ? Non tranché : aucun MC ne
figure dans les sorties du Tier-1, l'angle n'était pas dans le
protocole gelé. M2d (§8.63/§8.75) — réplication hors échantillon
de l'optimiseur (lot frais ICGC s31–s40) : non testée ici, le lot
frais relu en A4 est celui du §8.73 (s41–s60). Le mécanisme qui
choisit LEQUEL des trois estimateurs hauts {MFA, LevinaBickel,
PCAIntrinsic} est le plus petit, et à quelle magnitude, reste
incompris — quatre tentatives, quatre échecs au critère ≥ 90 %.

**Ce qui est établi, et qui ne change pas le verdict.** w est le
moteur du niveau de Delta (corrélations +0,60/+0,63 ; décalage
+0,21 à +1,13 entre w = 27 et w = 30 ; effondrement de l'écart
réel−nul à w égal sur les 8 paires principales). ln n porte
l'échelle (r = +0,774 avec Delta). Mais un moteur n'est pas un
mécanisme de choix : ni w, ni n, ni leur combinaison, ni la
structure des flux ne disent lequel des trois estimateurs hauts
est le plus petit, ni à quelle magnitude, à ±0,10 près sur 90 %
des runs. Delta n'est pas un discriminateur recommandé ; aucune
conclusion de séparation réel/nul n'est tirée de Delta dans ce
chantier, et aucune ne doit l'être tant qu'il n'est pas élucidé.

## 8.94.8 Ce que ça change pour §8.39, §8.42 et §8.57

**§8.39.** Le statut « Delta NON ÉLUCIDÉ » est confirmé une
quatrième fois, avec les deux pistes que le §8.39.10 laissait
ouvertes désormais testées et closes : Delta à w égal (A1 — le
signal le plus fort du chantier, mais 71,2 % sur les paires à w
égal, sous la barre) et le résidu après la loi en n (A2 — 50,0 %,
le résidu n'est pas du bruit). La nouveauté structurelle du §8.39
(LocalPCA toujours 3e ou 4e, choix entre trois magnitudes) est
reconfirmée dans l'ensemble gelé (LocalPCA dans la paire dans
217/222 runs) sans que le choix soit élucidé.

**§8.42.** La voie « résumés de flux » est close dans sa dernière
variante : A3 montre que même la structure des flux sans
estimateur (p, n, dispersion, corrélation, PC1, skew) ne choisit
ni la paire (40,1 %) ni la valeur (0,0 %). La leçon du §8.42 —
« les magnitudes sont des fonctionnelles de la série ordonnée
complète, pas de ses résumés » — tient, avec l'ajout que la série
complète elle-même (§8.57) et w + ln n (A1) ne suffisent pas non
plus en hold-out.

**§8.57.** Le piège de circularité reste évité (aucun recalcul
d'estimateur, `csd_fractal_estimators.json` non utilisée) et la
conclusion tient : l'échec des modèles honnêtes est un manque
d'information, pas un manque de capacité (C0 2886/2886). Le §8.94
ajoute la borne chiffrée : même avec w et ln n conjointement, d_div
n'est prédit qu'à 9,5 % en LOCO et 9,7 % sur B — le niveau n'est
pas une fonction lisse de (w, n) au sens du critère ±0,10.

**Pour le projet.** Delta reste une piste fragile, quatrième
confirmation. Aucun changement de protocole, aucun changement de
pipeline, aucune utilisation de Delta comme discriminateur. Les
deux questions ouvertes (M1c, M2d) restent au journal, non
tranchées, et toute nouvelle tentative exigera un protocole gelé
neuf — la barre de 90 % ne bouge pas.

## 8.94.9 Limites

- L'ensemble gelé de 222 runs est un ensemble de comparabilité,
  pas un échantillon représentatif : les 185 dossiers v62
  supplémentaires (§8.47, §8.53) restent hors ensemble, comme au
  §8.57 ; les cohortes sont très déséquilibrées (tcga 126/222).
- A1 : la comparaison à w égal ne porte que sur 73/106 paires ;
  33 paires ont un w différent entre réel et nul et en sont
  exclues. Le Tier-2 ne couvre que les 8 paires principales V1
  (§8.56), pas les 106 paires.
- A2 : par construction, F2 s'annule exactement dans chaque paire
  (même n des deux côtés) — le test du résidu se réduit au test de
  l'écart brut de Delta. Il exclut « le résidu est du bruit », il
  ne peut pas établir « Delta = F2(ln n) + bruit » au-delà de
  l'écart observé.
- A3 : les prédicteurs sont des résumés ; un modèle qui utiliserait
  les séries entières retomberait dans le piège de circularité du
  §8.57. Le kNN et le ridge sont des modèles de référence, pas une
  recherche exhaustive.
- A4 : le lot frais relu est celui du §8.73 (s41–s60), pas un lot
  neuf ; avec 0 courbe rob-on fraîche, P1 reste non testable et P2
  ne peut qu'échouer par absence de positif. Les comptages A1 de
  winsorisation portent l'avertissement d'artefact du §8.73.7
  (déflation de variance) et ne pèsent pas dans le verdict.
- M1c et M2d n'ont pas été testés dans ce chantier ; les nommer
  « ouverts » n'est pas un verdict sur eux.
- Le verdict est lu sur la batterie gelée A1–A4 + Tier-2, jamais
  sur un seul nombre (MC jamais seul) ; il décrit les données
  détenues, il ne prédit rien.

**Provenance (§8.94)**

- Protocole gelé `PROTOCOL_delta_elucidation_894.md`, SHA-256
  gelé `79e5567c19d90cdd78d39f4d90888b5e8d00c5a25f56f7ac5789a8dd9bc5229d`
  (cité dans `PROVENANCE_894.md` et dans `delta_894_results.json`,
  champ `sha_protocole`). Le fichier sur disque porte aujourd'hui
  le SHA `0e3b33718fb13cba531143822b6328ba1d3f7dc9ebc4a1aa64aee6bf2a625b41`
  parce que l'addendum de Zackary du 21 nov. 2026 12h03 y a été
  annexé après le gel (21 nov. 17h07) ; le texte gelé est intact —
  tronqué à l'octet 9376 (juste avant le marqueur de l'addendum),
  le fichier redonne exactement le SHA gelé
  `79e5567c…5229d`. Un fichier parasite nommé littéralement
  `PROTOCOL_894_*.md` (SHA
  `24847d6c94b632649abace0146868800439b59a92c0addd88f67c31178bb3730`,
  identique au fichier de l'addendum) existe dans le dossier —
  accident de glob, contenu = addendum seul, sans effet sur les
  résultats.
- Addendum : `ADDENDUM_correction_20261121_894.md`, SHA-256
  `24847d6c94b632649abace0146868800439b59a92c0addd88f67c31178bb3730`
  (correction de Zackary, 21 nov. 2026 12h03, précisée 12h04).
- Provenance du chantier : `PROVENANCE_894.md`, SHA-256
  `3d1892f1b671ba88fef45ebda679c07597f5721e08e47369d54f755050115b1b`
  (squelette au moment du gel ; à compléter par addenda datés,
  sans réécrire).
- Code : pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié sur disque ; v6.1 `2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`,
  inchangés) ; script Tier-1 `v62_delta_elucidation_894.py`, SHA-256
  `6dc5db1a09a52da30885cf934cf4cdbef476d2f6c3ff3089557b8bc03ef9bc0f` ;
  script Tier-2 `replica_w_894.py`, SHA-256
  `1677ec2500fdd96377220de311a6dcd5fc8c05b0ddd47ea3fd7adea1a005d781`.
- Résultats : `delta_894_results.json`, SHA-256
  `70ee8d8e09b68c0cef1121d85e8a9c3942a9d445fe8c68c0a88ac75f501e8e56`
  (21 nov. 2026 16:55) ; `delta_894_table.csv` (222 lignes + en-tête),
  SHA-256
  `9a928bacae87efb3a5240710e02fa2ff2296de0a4f8773850717eafc520c4c8c` ;
  log Tier-1 `v62_delta_elucidation_894.log` (21 nov. 16:55) ;
  `replica_w_894.json`, SHA-256
  `a3ba1536e36ec23a7ce3ceabd1016a7930521fd8d74a53d50495128eac90730c`
  (première fin exit = 0 le 21 nov. 2026 19:09:40Z, file
  `queue_893_896` étape 2, 12 passages exit = 0, dernière réécriture
  22 nov. 2026 12:33:17Z).
- Données d'entrée (détenues, relues) : `v62_delta_levels.csv`,
  222 runs (156 v6.1 + 66 v6.2), 223 lignes avec en-tête — ensemble
  gelé des §8.39/§8.42/§8.57 ; ensemble B (§8.62), 31 runs v6.2 fast ;
  `df_feat.csv` présent dans 222/222 dossiers (120 lignes),
  `fluxes_raw.csv` présent dans 222/222 ; coefficients F2(ln n)
  [−12,896435 ; 5,27966 ; −0,402319] repris du §8.62, NON ré-estimés
  (R² §8.62 = 0,6725) ; corpus A4 : 82 courbes gagnantes du §8.73
  (11 rob-on, 71 rob-off) + lot frais §8.73 (20 nuls ICGC, graines
  41–60), relu.
- Go : Zackary « Faite tout cela », 21 nov. 2026 11h36, piste 2/4.
  Coordinateur : TagPrint.
- Ce qui manque : M1c et M2d (non testés ici, voir §8.94.7) ; aucun
  nouveau run pipeline dans ce chantier (lecture seule des sorties
  détenues, Tier-2 = réplique depuis les CSV détenus avec les
  fonctions du pipeline) ; le livre blanc n'est pas modifié par ce
  fichier — section séparée, à fusionner par le coordinateur ;
  PDF non régénéré, rien poussé.

— Fin de la §8.94. —
