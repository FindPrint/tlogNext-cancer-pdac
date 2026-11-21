# §8.76 — GSE131050 (PurIST), lot Yeh_seq FNA : le signal survit au changement d'échantillon — CONFIRME, sur les mêmes tumeurs

## Verdict d'abord

**CONFIRME — le lot Yeh_seq FNA de GSE131050 (n = 42 tumeurs
indépendantes), test de robustesse APPARIÉ au lot FF du §8.74,
donne `d_maxsep = +0,1642` (réel 0,4083 contre nul 0,2441),
au-dessus du plancher 0,07 — avec une marge de 0,0942, plus de
deux fois l'écart mesuré en FF (+0,0739). Le signal `maxsep`
mesuré sur les mêmes tumeurs en flash-frozen SURVIT au
changement de type d'échantillon : en FNA ex-vivo, faible
volume, kit TruSeq RNA Exome, il est même PLUS FORT qu'en FF.
La condition C3 du §8.59.8, levée au §8.71, RESTE LEVÉE (ce
chantier est une consolidation supplémentaire, pas une
condition ; il ne rouvre rien). Le compte A2 des paires
indépendantes NE CHANGE PAS — 8/12 au-dessus du plancher,
10/12 positifs, LOO 7/11 — parce que le lot FNA n'est PAS une
paire indépendante : 41 codes sur 42 sont les mêmes tumeurs
que le lot FF du §8.74. Le compter comme treizième paire
serait un double comptage, et le protocole gelé l'interdit
explicitement.**

| Porte (PROTOCOL_maxsep_gse131050_fna_876.md §7, gelé) | Exigé | Mesuré 20–21 nov. 2026 | Sort |
|---|---|---|---|
| Robustesse appariée : `d_maxsep > 0,07` et positif | > 0,07 | **+0,1642** (réel 0,4083, nul 0,2441) | **CONFIRME** |
| A2 des paires indépendantes | Inchangé : 8/12, 10/12 positifs | **8/12, 10/12 positifs** (FNA non compté) | **INCHANGÉ** |
| LOO sur 12 paires (descriptif) | 7/11 | **7/11** (inchangé, non recalculé) | **INCHANGÉ** |
| Exactitude de l'extraction | 2/2 à 0,0 exact | **2/2, écart max 0,0** | **PASSE** |
| Nuls frais (§7, `d` dans [−0,07 ; +0,14[) | 2 nuls frais si proche du plancher | **Non courus : +0,1642 hors de l'intervalle** | **RÈGLE APPLIQUÉE** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que le
signal `maxsep` n'est pas un artefact du type d'échantillon
FF : lu sur les mêmes 41 tumeurs par aspiration à l'aiguille
fine ex-vivo — autre prélèvement, autre kit, autre échelle
d'expression (KRAS FNA médiane 1,569 contre 6,955 en FF) — il
sépare le réel du nul dans le bon sens et au-delà du plancher
gelé, avec une marge confortable (+0,0942, soit 135 % du
plancher). Il dit aussi que l'écart FNA est plus de deux fois
celui du FF (+0,1642 contre +0,0739) et que cette différence
vient du côté réel (0,4083 contre 0,3220, +0,0863) et non du
nul (0,2441 contre 0,2481, −0,0040) : les mêmes tumeurs, lues
en FNA, portent un `maxsep` réel plus haut. Il dit enfin que
le signal d'ordre est plus fort en FNA qu'en FF (Δρ médian
+0,524, 12/12 positifs, contre +0,386 et 10/12 au §8.74) — les
deux gènes qui ne montaient pas en FF (PGC, REG4) montent en
FNA. Il ne dit pas que `maxsep` est validé en général : c'est
une confirmation sur les mêmes tumeurs, pas une treizième
cohorte, et les scores compagnons ne suivent pas tous (MC à
peine positif +0,0252, `sep` sous sa barre descriptive — voir
§8.76.5). Il ne dit pas non plus que l'adoption pleine est
« prouvée » par ce chantier seul : elle a été décidée par
Zackary après lecture des §8.56/§8.59/§8.64, et cette section
est la vérification a posteriori que le protocole prévoyait —
elle consolide la décision, elle ne la fonde pas
rétroactivement. Il ne dit rien de clinique : l'étude porte
sur l'instrument, pas sur un remède — aucune affirmation sur
le cancer du pancréas n'est tirée de ce lot.

**Fragilité, dite en tête.** Le verdict tient à une seule paire
mesurée aujourd'hui — comme tous les verdicts de ce dossier.
Ici la fragilité a deux noms précis. D'abord, la paire n'est
pas indépendante du §8.74 : si le §8.74 portait un biais de
cohorte (les 43 tumeurs Yeh), le lot FNA le partage — il ne
peut pas l'exclure. Ce qu'il exclut, c'est le biais de type
d'échantillon FF : le signal n'est pas propre au
flash-frozen. Ensuite, la cascade réelle FNA est BASSE
([8,2 / 11,2 / 14,2 / 21,3 / 37,9]) alors que le nul a une
cascade HAUTE ([2,4 / 66,3 / 73,6 / 78,4 / 97,6]) — l'inverse
exact du §8.74, où la cascade réelle était haute et le nul
graine 42 bas. La cascade ne sépare pas le réel du nul ici,
et elle ne l'a jamais été comme critère — mais son renversement
entre FF et FNA sur les mêmes tumeurs dit plainement que la
cascade est une lecture instable entre types d'échantillons,
tandis que `maxsep` reste dans le bon sens des deux côtés.
C'est consigné tel quel, sans sauver ni condamner le verdict,
dont le critère gelé est `maxsep` et lui seul.

Protocole gelé : `PROTOCOL_maxsep_gse131050_fna_876.md` (20 nov.
2026, SHA `dd7937ee…35023bc5f` au gel, inchangé). Critère de
passage écrit AVANT toute construction et tout run (§7 du
protocole) ; aucune repondération, aucun nouveau terme, aucune
redéfinition du plancher après avoir vu les chiffres. Les
nombres des §8.56/§8.59/§8.64/§8.69/§8.70/§8.71/§8.74 étaient
la motivation, pas le verdict : le verdict repose sur les 2
runs mesurés ci-dessous.

## 8.76.1 — La paire mesurée : GSE131050, lot Yeh_seq FNA, et pourquoi elle n'est PAS indépendante

**Cohorte : GSE131050, NCBI GEO** — Rashid et coll., 42 tumeurs
PDAC primaires, plateforme Illumina NextSeq 500 GPL18573,
article Rashid et coll. 2020 (*Clin Cancer Res*, 26(1):82–92,
PMID 31754050, doi 10.1158/1078-0432.CCR-19-1467). Provenance
complète : `PROVENANCE_876.md`.

**Appariement, en cinq points (protocole §2.2, vérifié avant le
gel).**
1. **Jamais utilisé dans ce projet.** Aucun CSV de flux, aucun
   run, aucun JSON, aucune valeur `maxsep` n'existait pour le
   lot FNA avant ce chantier. Vérifié par grep avant le gel :
   la chaîne « FNA » ne figurait que comme « piste restante
   non vérifiée » dans les fichiers du §8.71 et du §8.74 et
   dans le livre blanc aux mêmes endroits.
2. **Mêmes patients, même centre, même plateforme, autre
   échantillon.** Données nouvelles générées pour l'étude
   PurIST : lot Yeh collecté de novo à l'UNC (Lineberger
   Comprehensive Cancer Center, Tissue Procurement Core
   Facility) — tumeurs réséquées ; plateforme Illumina NextSeq
   500 (GPL18573), la même que le lot FF du §8.74. Ce qui
   change : le type d'échantillon. FNA ex-vivo au moment de la
   résection (3 passages, aiguille 22G), kit TruSeq RNA Exome
   contre TruSeq pour les FF, échantillons faible volume.
3. **Le recouvrement est mesuré, pas supposé.** Enquête pré-gel
   (`enquete_876/check_fna_876.py`, portes uniquement, aucun
   maxsep) : **41 codes-tumeurs sur 42 sont communs aux lots
   FF et FNA (97,6 %)**. Code FNA seul (sans FF) : 0921T1.
   Code FF seul (sans FNA) : PancT6. Total : 43 tumeurs
   distinctes. Les 45 colonnes FNA primaires proviennent de
   42 codes ; les 47 colonnes FF primaires, de 42 codes. Le
   lot Yeh est apparié par construction (§8.74.7) : 97
   échantillons primaires pour 43 tumeurs, chaque tumeur
   échantillonnée jusqu'à trois fois (FF, FNA, FFPE).
4. **Même construction que les autres paires principales GEO.**
   Variante (a) : les 12 mêmes gènes que la v4 TCGA (PGC, REG4,
   CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5,
   CLCA1, MUC16), ordre = KRAS croissant, sans correction, cas
   complets, nul = lignes permutées graine 42. La paire est
   donc comparable au §8.74 par construction — mais appariée,
   pas indépendante. Une seule adaptation, gelée au protocole
   §4.4 et justifiée au §8.76.7 : l'unité d'analyse est la
   TUMEUR INDÉPENDANTE, pas la colonne — les réplicats FNA
   d'une même tumeur sont agrégés par médiane (0417T1 ×3,
   1119T1 ×2 ; précédent du projet : agrégation par médiane
   des sondes multiples vers un même symbole, et des réplicats
   FF au §8.74).
5. **Pas un re-test déguisé.** Ce n'est ni une relecture d'un JSON
   existant (§8.64.7 : « pas une relecture »), ni une rotation
   déjà comptée, ni un sous-ensemble d'une paire V1, ni un
   nouvel ordre sur des CSV existants (nouveaux CSV, nouveaux
   runs, 2 runs v6.2 frais, données FNA jamais courues). La
   sous-série NanoString GSE131051 n'est pas utilisée : ce
   n'est pas de l'expression RNA-seq codante en comptages
   géniques. Le lot Linehan_seq reste écarté (§8.74,
   protocole §2.3 : 37 patients, pré/post mélangées).

**Ce que GSE131050 FNA n'est pas.** Ce n'est pas une cohorte
choisie pour ses résultats : aucun `maxsep` FNA n'existait
quand le protocole a été gelé. Ce n'est pas non plus une
treizième paire indépendante : c'est le même matériel tumoral
que le §8.74, lu par un autre prélèvement. Toute lecture
future qui compterait 13 paires avec le FNA serait un double
comptage — le protocole gelé l'interdit explicitement
(§10), et cette section le répète : **A2 reste 8/12**.

**Différence d'échelle KRAS, consignée d'avance (protocole
§2.2).** KRAS FNA (médiane par code) : min 0,0482, médiane
1,569, max 5,803 — contre KRAS FF min 1,152, médiane 6,955,
max 19,7 (§8.74). L'échelle FNA est ~4 fois plus basse :
échantillons faible volume, kit TruSeq RNA Exome. L'ordre
reste KRAS croissant (même règle que toutes les paires), sans
renormalisation ni transformation log. Si le verdict diffère
de celui du §8.74, cette différence d'échelle est une piste
d'explication nommée, pas une excuse — et de fait le verdict
diffère par sa taille, pas par son sens (§8.76.7).

## 8.76.2 — Les runs et l'extraction

**Runs v6.2 mode fast : 2/2, exits 0/0.** Manifeste
`manifest_v62_876.txt` (réel + nul graine 42), lanceur
reprenable `run_v62_lot.sh`, journal `runs_v62_876.log`
(FIN 2026-11-21T01:32:02Z, deja_faits=1, termines=1,
echecs=0). Unités systemd `v62-876` et `v62-876b` (jamais
nohup). **Incident consigné : la machine a redémarré entre
les deux runs** (uptime 0 min constaté à 01h30 UTC) — le run
réel était déjà terminé (EXIT 0 consigné, `master_results.json`
complet, 8 099 157 o) ; le run nul, interrompu en cours
(dossier partiel : un seul fichier, `landscape_complexity.png`),
a été relancé par le lanceur reprenable qui a sauté le réel
déjà complet (SKIP consigné) — aucune reprise à l'aveugle,
aucun dossier de run touché. SHA du pipeline revérifié avant
ET après le lot : `f07567c4…c3abf`, inchangé.

**Extraction : 2/2 à 0,0 exact.** `extract_876.py` (réutilise
`extract()` de `extract_858.py`, original intact) lit les 2
`master_results.json` ; `verify_876.py` (chemin distinct,
relecture directe par `json.load`) recoupe `maxsep`, ancien MC
et stabilité à 0,0 exact sur les 2 runs
(`maxsep_876_verify.json`, verdict OK). Version lue :
`v6.2.0-L7aL7b-CohenD-short` sur les 2 runs.

| Run | n | maxsep | ancien MC | S_sep | Delta | L7a | Cascade (Q1–Q5, %) |
|---|---|---|---|---|---|---|---|
| Réel Yeh FNA | 42 | **0,4083** | 0,4120 | 0,4062 | 1,476 | up 0,338 | 8,2 / 11,2 / 14,2 / 21,3 / 37,9 |
| Nul graine 42 | 42 | 0,2441 | 0,3869 | 0,2409 | 1,343 | up 0,336 | 2,4 / 66,3 / 73,6 / 78,4 / 97,6 |

Valeurs complètes : `maxsep` réel 0,4083181001358463 ; nul s42
0,24407093788906223. Stabilité : réel 0,9949 ; nul 0,9871.
Seuils MC : réel 40,91 ; nul 40,91. F1/F2 après seuil : réel
1,1040 / 0,8387 ; nul s42 0,2366 / 0,2832 (descriptif, voir
§8.76.5). Falsification : INDISPONIBLE sous n = 75 (n = 42) —
les valeurs brutes du pipeline (1,288 / 1,514) figurent dans
`extract_876.json` sans être interprétées, comme au §8.74.
L7b : FRAGILE sur les 2 runs — l'audit L7b est clos comme
non-informatif (il dit FRAGILE sur le réel comme sur les nuls) ;
il n'est pas rapporté comme une mesure de fragilité.

## 8.76.3 — Le verdict étendu : A2 inchangé, par construction

Table des 12 paires principales indépendantes comptées (valeurs
des §8.56 / §8.69 / §8.70 / §8.71 / §8.74 reprises telles
quelles, jamais recalculées). Écart = maxsep réel − maxsep
nul. Plancher 0,07. Le lot FNA n'y figure PAS — il est
apparié au §8.74, pas indépendant.

| Paire | maxsep R / N | Écart | > 0,07 ? | Positif ? |
|---|---|---|---|---|
| HP35 | 1,7718 / 0,1206 | **+1,6512** | oui | oui |
| TCGA v4 | 0,4623 / 0,1696 | **+0,2928** | oui | oui |
| GSE71729 | 0,2593 / 0,2191 | +0,0402 | non | oui |
| GSE62452 | 0,3100 / 0,3136 | −0,0036 | non | NON |
| ICGC | 0,4080 / 0,3110 | **+0,0970** | oui | oui |
| Immunitaire TCGA | 0,5309 / 0,1634 | **+0,3675** | oui | oui |
| PARP TCGA | 0,3680 / 0,1992 | **+0,1688** | oui | oui |
| DepMap | 0,4436 / 0,2532 | **+0,1904** | oui | oui |
| GSE21501 (§8.69) | 0,2121 / 0,2221 | −0,0100 | non | NON |
| GSE79668 (§8.70) | 0,4104 / 0,3538 | +0,0567 | non | oui |
| GSE60979 (§8.71) | 0,4418 / 0,2373 | **+0,2045** | oui | oui |
| GSE131050 Yeh FF (§8.74) | 0,3220 / 0,2481 | **+0,0739** | oui | oui |

**Bilan : 8/12 au-dessus du plancher, 10/12 positifs —
INCHANGÉ.** Les seules paires négatives restent GSE62452
(−0,0036) et GSE21501 (−0,0100). **LOO (descriptif) :**
7/11 après retrait de chaque paire passante — inchangé, non
recalculé ici, puisque le lot FNA n'entre pas dans le compte.
**C3 reste LEVÉE** : elle l'était depuis le §8.71 (7 paires
passantes) ; le §8.74 a ajouté une huitième paire passante,
et ce chantier ajoute une confirmation appariée — il ne
rouvre rien.

Lecture honnête du rang : +0,1642 est le quatrième plus grand
écart du dossier (derrière HP35 +1,6512, Immunitaire TCGA
+0,3675 et TCGA v4 +0,2928, devant GSE60979 +0,2045 et PARP
+0,1688) — mais ce rang ne se compare pas aux paires
indépendantes : c'est le même matériel que le §8.74, et son
écart FF n'était que +0,0739, le plus petit écart passant du
dossier. La paire FNA ne renforce pas l'adoption par son
nombre — elle la renforce par sa nature : le signal tient
quand on change le prélèvement sur les mêmes tumeurs, et il
tient plus fort (+0,1642 contre +0,0739). C'est une robustesse
de mesure, pas une confirmation de cohorte.

## 8.76.4 — Les nuls frais : aucun, par la règle gelée

Règle gelée (§7 du protocole) : les 2 nuls frais (graines 8761
et 8762, gelées avant tout run) ne sont courus que si
`d_maxsep` est dans [−0,07 ; +0,14[. Ici `d_maxsep = +0,1642`
est HORS de l'intervalle — au-dessus de sa borne haute de
0,0242. **Aucun nul frais n'est donc couru, et les graines
8761/8762 restent inutilisées.** Ce n'est pas un oubli : c'est
l'application de la règle écrite avant tout run, la même
règle qui avait fait courir les nuls frais au §8.74
(+0,0739, dans l'intervalle) et ne pas en courir au §8.71
(+0,2045, hors intervalle). Le verdict de la paire graine 42
est CONFIRME, sans consolidation par nuls frais — la marge
(+0,0942 au-dessus du plancher) est la consolidation : elle
est plus de deux fois l'étendue des nuls mesurée au §8.74
(0,0374 sur 3 nuls) et plus grande que l'étendue mesurée au
§8.70 à n comparable (0,0972 entre 3 nuls à n = 51) — un
autre tirage de nul devrait monter de plus de 0,09 pour
inverser le passage, soit plus que toute l'étendue observée
entre nuls dans ce dossier à n comparable. C'est une lecture,
pas une preuve : 1 nul ne fait pas un plancher stable
(§8.53 : ~200 nuls pour un plancher stable à petit n), et
c'est consigné comme tel.

## 8.76.5 — Les scores compagnons : `maxsep` passe seul, les autres ne suivent pas

Convention d'affichage §8.64.6 : `maxsep` score principal,
ancien MC secondaire, `sep` compagnon, mention de fragilité en
tête de table (voir le verdict). Les scores compagnons sont
descriptifs : aucun ne décide.

- **Ancien MC (secondaire) :** réel 0,4120 contre nul 0,3869 —
  écart +0,0252 contre le nul graine 42. À peine positif, et
  très loin du plancher 0,07 : MC ne sépare presque pas ici.
  C'est le même motif qu'aux §8.70 (+0,05), §8.71 (+0,026) et
  §8.74 (+0,0114) : `maxsep` voit quelque chose que l'ancien
  MC ne voit presque pas. MC est pourtant plus haut en absolu
  ici qu'en FF (0,4120 contre 0,3985) — le réel FNA score
  plus haut sur les deux mesures, mais l'écart MC reste petit
  parce que le nul FNA score haut aussi (0,3869 contre 0,3871
  en FF).
- **Delta :** réel 1,476 contre nul 1,343 — écart +0,133 contre
  le nul graine 42. Plus fort qu'au §8.74 (+0,041) et au §8.70
  (+0,05), dans le même sens que `maxsep`, beaucoup plus
  faible. La divergence Delta/`maxsep` du §8.69 (Delta +2,01
  contre maxsep −0,01) ne se reproduit pas ici non plus :
  Delta et `maxsep` vont dans le même sens. Delta n'est
  toujours pas élucidé (§8.57, §8.63) ; rien n'est élucidé ici
  sans preuve.
- **S_sep :** réel 0,4062 contre nul 0,2409 — écart +0,1653
  contre le nul graine 42. S_sep suit `maxsep` (il en est
  proche par construction, §8.38) et passe le même plancher
  en descriptif.
- **`sep` compagnon :** réel 0,2899 contre nul 0,1962 — écart
  0,0937, contre un plancher équivalent-sep de 0,1226
  (= 0,07·(1+0,4083)(1+0,2441)). **Le lot ÉCHOUE à la barre
  descriptive du plancher équivalent-sep**, comme aux §8.71
  (0,1146 contre 0,1249 exigé) et §8.74 (0,0448 contre 0,1155
  exigé). `sep` ne suit pas `maxsep` jusqu'à sa propre barre
  — cohérent avec le rejet de `sep` seul aux §8.59/§8.64.
  Rapporté, non décisif : D4 n'est pas rejoué ici.
- **Cascade :** réelle [8,2 / 11,2 / 14,2 / 21,3 / 37,9] contre
  nul graine 42 [2,4 / 66,3 / 73,6 / 78,4 / 97,6] — la cascade
  réelle est BASSE à tous les quantiles, le nul est HAUT dès
  Q2. C'est l'inverse exact du §8.74 (réelle [45,7 / 68,7 /
  76,0 / 80,8 / 90,4] contre nul [0,0 / 21,3 / 28,4 / 33,2 /
  43,1]). Sur les mêmes tumeurs, la cascade change de sens
  entre FF et FNA : elle ne porte pas le verdict, et ce
  renversement le confirme — la cascade n'est pas un critère
  de passage et ne l'a jamais été. C'est consigné tel quel.
- **L7a :** up partout (réel 0,338 ; nul 0,336) — L7a ne sépare
  pas ici, comme dans la plupart des paires principales.
  **L7b :** FRAGILE sur les 2 runs — non informatif (audit
  clos, §8.56/§8.64 : il dit FRAGILE sur le réel comme sur
  les nuls).
- **F1/F2 après seuil :** réel 1,1040 / 0,8387 ; nul s42
  0,2366 / 0,2832. Descriptif, sans lecture imposée : le réel
  FNA a un F1/F2 proche de 1 (peu de changement après seuil),
  le nul un F1/F2 bas — l'inverse du §8.74 (réel 0,4775 /
  0,5248 ; nul 1,7075 / 1,0350). Les ratios F1/F2 ne portent
  pas le verdict.

## 8.76.6 — Tests directs en appui (ne décident pas)

Script `direct_tests_876.py` (SHA `bf0a8b8b…0660`), sur les
CSV de flux du chantier (réel + nul graine 42). Sortie :
`direct_tests_876.json` (SHA `55b386dc…0b823`).

**1. d de Cohen marginal (correction §8.70, appliquée ici).**
d = 0,0000 pour les 12 gènes (CR2 : +0,0000 ; REG4, GSTM1,
CLCA1 : −0,0000, arrondi) — vacueux par construction, comme
attendu : le nul est une permutation des lignes, chaque flux
garde exactement ses 42 valeurs. Le test valide la
construction du nul (marginales préservées exactement) ; il
ne mesure pas la séparation et ne décide rien.

**2. Test informatif : Spearman de chaque flux contre le pas
(ordre KRAS), réel vs nul.** |ρ| moyen : réel 0,449 contre nul
0,142. Δρ médian **+0,524**. Δρ positifs **12/12**. Table
complète, sans sélection :

| Gène | ρ réel | ρ nul | Δρ |
|---|---|---|---|
| PGC | +0,208 | −0,238 | **+0,446** |
| REG4 | +0,443 | −0,188 | **+0,630** |
| CLDN18 | +0,695 | −0,282 | **+0,977** |
| MUC17 | +0,579 | −0,056 | **+0,634** |
| DPCR1 | +0,600 | −0,262 | **+0,862** |
| CR2 | +0,291 | +0,227 | +0,064 |
| KRT20 | +0,361 | +0,123 | +0,238 |
| MUC2 | +0,538 | −0,063 | **+0,601** |
| GSTM1 | +0,241 | +0,129 | +0,112 |
| CEACAM5 | +0,671 | −0,102 | **+0,774** |
| CLCA1 | +0,411 | +0,013 | **+0,397** |
| MUC16 | +0,351 | +0,027 | +0,324 |

Lecture : l'ordre par KRAS porte une information réelle et
forte — les 12 flux montent avec KRAS (CLDN18, DPCR1, CEACAM5
en tête, Δρ de +0,77 à +0,98), aucun ne descend. C'est le test
qui porte l'information d'ordre, et il est cohérent avec le
`maxsep` qui passe : le réel est ordonné, le nul ne l'est pas.
Aucun de ces tests ne change le verdict du §7 — ils
l'éclairent. Comparaison descriptive avec le §8.74 (valeurs
relues dans `direct_tests_874.json`, jamais recalculées) : au
§8.74, Δρ médian +0,386, 10/12 positifs, |ρ| moyen réel 0,336
contre nul 0,146. Ici le signal d'ordre est PLUS FORT sur les
trois mesures (Δρ médian +0,524, 12/12 positifs, |ρ| 0,449
contre 0,142) — et les deux gènes qui ne montaient pas en FF
(PGC −0,001, REG4 −0,099) montent en FNA (+0,446 et +0,630).
Cohérent avec un `maxsep` qui passe plus largement ici
(+0,1642) qu'en FF (+0,0739) ; au §8.71 il passait encore plus
largement (+0,2045) avec un Δρ médian pourtant plus faible
(+0,180) — les deux mesures ne sont pas proportionnelles, et
aucune loi n'est inférée de trois points.

## 8.76.7 — Comparaison appariée FF vs FNA : mêmes 41 codes, autre prélèvement

C'est la comparaison que ce chantier existe pour faire — les
valeurs FF sont reprises du §8.74 telles quelles, jamais
recalculées ; les valeurs FNA sont mesurées ici. Les 41 codes
communs portent les deux lectures ; les codes uniques (0921T1
en FNA seul, PancT6 en FF seul) sont 1 sur 42 de chaque côté
et ne peuvent pas porter la différence.

| Mesure | FF (§8.74) | FNA (§8.76) | Différence FNA − FF |
|---|---|---|---|
| maxsep réel | 0,3220 | **0,4083** | **+0,0863** |
| maxsep nul s42 | 0,2481 | 0,2441 | −0,0040 |
| d_maxsep | +0,0739 | **+0,1642** | **+0,0903** |
| MC réel / nul | 0,3985 / 0,3871 | 0,4120 / 0,3869 | +0,0135 / −0,0002 |
| Delta réel / nul | 1,470 / 1,429 | 1,476 / 1,343 | +0,006 / −0,086 |
| S_sep réel / nul | 0,3187 / 0,2445 | 0,4062 / 0,2409 | +0,0875 / −0,0036 |
| Cascade réelle Q1–Q5 | 45,7 / 68,7 / 76,0 / 80,8 / 90,4 | 8,2 / 11,2 / 14,2 / 21,3 / 37,9 | renversée |
| Cascade nul Q1–Q5 | 0,0 / 21,3 / 28,4 / 33,2 / 43,1 | 2,4 / 66,3 / 73,6 / 78,4 / 97,6 | renversée |
| Δρ médian / positifs | +0,386 / 10/12 | **+0,524 / 12/12** | +0,138 / +2 |
| \|ρ\| moyen réel / nul | 0,336 / 0,146 | 0,449 / 0,142 | +0,113 / −0,004 |

**Lecture.** L'écart FNA est plus de deux fois l'écart FF, et
la décomposition dit d'où il vient : le nul ne bouge presque
pas (0,2441 contre 0,2481, −0,0040), le réel monte de +0,0863.
Le même matériel tumoral, lu en FNA, donne un `maxsep` réel
plus haut — et un signal d'ordre plus fort sur les trois
mesures de Spearman. Deux lectures s'opposent et toutes deux
sont consignées : (a) la lecture « robustesse » — le signal
n'est pas un artefact du flash-frozen ni du kit TruSeq : il
survit au changement de prélèvement et de kit, et il est même
plus net en FNA, ce qui est exactement ce qu'on attend d'un
signal porté par les tumeurs elles-mêmes plutôt que par la
préparation ; (b) la lecture « prudence » — l'échelle KRAS
FNA est ~4 fois plus basse (médiane 1,569 contre 6,955) et
la cascade se renverse entre FF et FNA : la lecture FNA n'est
pas la même mesure que la lecture FF, et un `maxsep` plus haut
en FNA pourrait tenir en partie à cette autre échelle plutôt
qu'à un signal plus fort — aucune décomposition ne permet de
trancher ici, et aucune n'est inventée. Ce qui est établi :
le passage tient des deux côtés, sur les mêmes tumeurs, avec
le même protocole et le même plancher. Ce qui ne l'est pas :
pourquoi il tient plus fort en FNA.

**Ce que cela change pour la suite.** La série GSE131050 ne
contient plus de lot non testé qui puisse faire une paire
principale ou un test apparié : le lot FF (§8.74) et le lot
FNA (§8.76) sont courus, le lot Linehan est écarté (37
patients, pré/post mélangées), le lot FFPE compte 5
échantillons (< 40). Toute autre paire GSE131050 serait un
re-test déguisé (mêmes 43 tumeurs). La piste suivante doit
être une autre série, pas un autre découpage de celle-ci.

## 8.76.8 — Ce que le verdict dit, et ce qu'il ne dit pas

Il dit que le signal `maxsep` mesuré au §8.74 sur 42 tumeurs
FF survit au changement de type d'échantillon : en FNA, sur
les mêmes tumeurs, il passe le plancher gelé avec une marge
de +0,0942, et l'écart (+0,1642) est plus de deux fois celui
du FF (+0,0739). Il dit que l'ordre KRAS porte une
information réelle plus forte en FNA (Δρ médian +0,524,
12/12 positifs) qu'en FF (+0,386, 10/12) — c'est le signal
que `maxsep` lit. Il dit que le dossier compte toujours 8
paires indépendantes passantes sur 12, et que ce chantier
n'en ajoute aucune — par construction, pas par échec.

Il ne dit pas que `maxsep` sépare toujours le réel du nul :
4 paires indépendantes sur 12 restent non passantes, et les
scores compagnons (MC +0,0252, `sep` sous sa barre
descriptive) ne suivent presque pas. Il ne dit pas que la
marge est à l'abri d'un tirage de nul : 1 nul couru ici, pas
3 — la règle gelée ne prévoyait pas de nuls frais hors de
l'intervalle, et ~200 nuls seraient nécessaires pour un
plancher stable à petit n (§8.53). Il ne dit pas pourquoi le
signal est plus fort en FNA : l'échelle KRAS différente et
la cascade renversée interdisent d'attribuer la différence à
une seule cause. Il ne dit pas que l'adoption pleine est
prouvée : elle a été décidée par Zackary le 20 nov. 2026 à
13h04, et ce chantier est la vérification a posteriori que le
protocole prévoyait. Il ne dit rien de clinique : l'étude
porte sur l'instrument, pas sur un remède — aucune
affirmation sur le cancer du pancréas n'est tirée de ce lot.

**Biais et limites nommés.** (a) n = 42 : petit effectif,
proche du plancher n ≥ 40 ; la fragilité du nul à petit n
(§8.70 : étendue 0,0972 à n = 51 ; §8.53 : ~200 nuls pour un
plancher stable à petit n) reste un chantier ouvert — ici
1 seul nul, aucune étendue mesurée. (b) Médiane des
réplicats FNA : pour 2 tumeurs sur 42, la valeur retenue est
une médiane de 2–3 mesures, pas une mesure unique — règle
gelée avant tout run, précédent du projet, mais c'est une
agrégation, pas une mesure brute. (c) Nature FPKM vs TPM
indéterminée (PROVENANCE_876 §3) — valeurs prises telles que
fournies, sans transformation ; le pipeline ne voit que
l'ordre relatif, mais la nature exacte reste inconnue.
(d) Recouvrement avec TCGA_PAAD non excluable formellement
par identifiants (titres anonymisés) — voir PROVENANCE_876 §5.5.
(e) Une seule plateforme (NextSeq 500), un seul centre (UNC),
un seul type d'échantillon (FNA) : le lot ne teste pas la
robustesse inter-plateformes — c'est le rôle des autres
paires, pas de celui-ci. (f) Appariement au §8.74 : un biais
de cohorte des 43 tumeurs Yeh serait partagé par les deux
lots — le FNA exclut le biais de type d'échantillon, pas le
biais de cohorte.

## 8.76.9 — Pistes ouvertes

| Pistes ouvertes | Oui, une de moins | (a) La confirmation indépendante C3 est close depuis le §8.71 — aucune autre paire indépendante n'est requise par ce critère ; GSE131050 ajoute une huitième paire passante (§8.74) et une confirmation appariée (§8.76), et ne rouvre rien ; (b) la fragilité du nul à petit n (§8.70, §8.53) reste un chantier propre ouvert — ici 1 seul nul, aucune étendue mesurée ; (c) la divergence Delta/`maxsep` du §8.69 ne se reproduit pas sur cette cohorte non plus, ni en FF (Delta +0,041) ni en FNA (Delta +0,133, même sens, beaucoup plus faible) ; (d) la série GSE131050 est épuisée comme source de paires : FF et FNA courus, Linehan écarté, FFPE à n = 5 — la piste suivante doit être une autre série ; (e) la question ouverte nouvelle : pourquoi le signal est-il plus fort en FNA qu'en FF sur les mêmes tumeurs — échelle KRAS, kit, ou signal tumoral plus net — aucune décomposition ne tranche ici. |

## 8.76.10 — Annexe : provenance condensée et SHAs

- **Source :** GSE131050, NCBI GEO ; Rashid et coll., *Clin
  Cancer Res* 2020, 26(1):82–92, PMID 31754050,
  doi 10.1158/1078-0432.CCR-19-1467 ; UNC Lineberger, Chapel
  Hill, USA. Série soumise 10 mai 2019, publique 10 déc. 2019.
  Plateformes : GPL16791 Illumina HiSeq 2500 (Linehan),
  GPL18573 Illumina NextSeq 500 (Yeh). BioProject PRJNA542388,
  SRA SRP197641. Provenance complète : `PROVENANCE_876.md`.
- **Fichiers source (téléchargement officiel §8.74, réutilisé,
  SHA re-vérifiés) :** Yeh_seq `2fc0a66e…be5b1`
  (9 468 179 o) ; matrice GPL18573 `9b333eb6…7843e`
  (6 864 o). Aucun nouveau téléchargement.
- **Protocole :** `PROTOCOL_maxsep_gse131050_fna_876.md`, SHA
  `dd7937ee…35023bc5f` (gelé avant toute construction et tout
  run).
- **Pipeline :** v6.2 SHA `f07567c4…c3abf`, vérifié avant et
  après le lot, inchangé. (Note : 8 occurrences de
  `temperature|Onsager|2.269` dans le fichier, toutes dans
  l'annexe génératrice d'exemple Ising, hors cœur — état connu
  du fichier adopté.)
- **CSV de flux :** réel `70697b3a…10324` (42 lignes) ; nul s42
  `2474ceaf…4d35`.
- **Extraction / vérification :** `extract_876.json`
  `ae14101e…02e43` ; `extract_876.csv` `a3cb4f9b…f996e` ;
  `direct_tests_876.json` `55b386dc…0b823` ;
  `maxsep_876_verify.json` `0dc536a4…20ce` (2/2 à 0,0 exact).
- **Scripts :** `build_fluxes_876.py` `c1b66ac4…13698` ;
  `build_nul_876.py` `673f1fc2…477a38` ;
  `extract_876.py` `041e0f89…604f7f` ;
  `verify_876.py` `533cd03a…c400` ;
  `direct_tests_876.py` `bf0a8b8b…0660`.
- **Enquête pré-gel :** `enquete_876/check_fna_876.py`
  `46c58648…40d93`.
- **Manifestes / journaux :** `manifest_v62_876.txt`
  `0e63d732…539f7` ; `runs_v62_876.log` `cd6e55fd…75e22`.
- **Recoupements (reprises telles quelles, jamais
  recalculées) :** `sep_maxsep_856_table.json`
  `ec5ee638…34f8b` ; `extract_869.json` `644339e4…882b` ;
  `extract_870.json` `4ffa851a…444f` ; `extract_871.json`
  `85e9089a…55e3b` ; `extract_874.json` `82ade747…fcb47`.
- **KRAS FNA (ordre, valeurs fournies) :** min 0,0482,
  médiane 1,569, max 5,803 (après médiane des réplicats FNA) —
  contre min 1,152, médiane 6,955, max 19,7 en FF (§8.74).
- **Livre blanc NON édité. PDF NON régénéré. Rien poussé sur
  GitHub** (convention des chantiers ; fusion par le
  coordinateur).

— Fin de la section §8.76. —

