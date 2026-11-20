### 8.58 Bloc estomac / mucus : nouveaux flux inattendus (y compris les odeurs) (19–20 nov. 2026)

**Verdict d'abord : les flux inattendus existent et bougent, mais
pas comme un seul programme, et pas comme la chaîne KRAS — et le
pipeline ne les sépare pas nettement du nul.** Le signal le plus
net vient du groupe qu'on n'attendait pas là : les marqueurs
neuroendocrines (G5) s'effondrent quand KRAS monte — SYP
rho −0,392 (p = 6,1e-08), INSM1 −0,343, CHGB −0,311, pendant que
les kératines KRT19 (+0,333) et KRT7 (+0,308) montent — et ils
baissent aussi avec le stade (SYP −0,276, CHGB −0,250).
**Confirmations (30/30 runs, GSE71729 + GSE62452) : le programme
neuroendocrine tient dans les deux cohortes** (GSE62452 SYP
−0,503, KRT19 +0,416 ; GSE71729 CHGA −0,359, INSM1 −0,296,
KRT19 +0,281) **et le volatil aussi, plus fort qu'en TCGA**
(GSE62452 AOX1 −0,611, UGT1A1 +0,541, NOS1 −0,529 ; GSE71729
NOS1 −0,369, ALDH3A1 +0,367). **Le mucus ne confirme que
partiellement** (AGR2 +0,383 dans GSE71729, mais MUC4 plat et
MUC6 en chute −0,436). **Les odeurs confirment dans l'autre
sens : plusieurs OR CHUTENT avec KRAS dans les deux cohortes**
(OR2W3 −0,338, OR13A1 −0,423, OR2T10 −0,418) **et aucun ne
monte** ; OR2A4, le seul OR montant de TCGA, est absent des
deux puces. Le mucus
étendu (G1) fait l'inverse du bloc v4 sous KRAS : MUC4, AGR2 et
MUC5B MONTENT avec KRAS (rho +0,313, +0,328, +0,222), et montent
aussi avec le stade (TFF1 top-12 +0,54) — même sens que le bloc
v4 avec le stade, sens opposé avec KRAS. Les odeurs (G3) ne
portent pas de signal de groupe : 356 gènes OR sont présents
comme lignes dans TCGA, mais 336 d'entre eux sont quasi
silencieux (médiane 0, détectés dans moins de 25 % des tumeurs) ;
seuls 19 OR sont détectés dans plus de la moitié des tumeurs,
et un seul d'entre eux, OR2A4, monte avec KRAS (rho +0,259).
Les enzymes digestives (G2) chutent avec KRAS, mais exactement
comme le témoin acineux (CELA2A −0,76 dans les deux) : c'est la
perte du programme acineux, pas un nouveau signal — et c'est un
artefact de construction (les flux G2 sont des résidus après
régression sur un score construit à partir d'eux-mêmes). Le
métabolisme volatil (G4) est partagé : UGT1A1 (+0,378) et
ALDH3B1 (+0,303) montent avec KRAS, ADH1A (−0,313) et AOX1
(−0,289) descendent — des pistes par gène, pas un programme.
Côté pipeline (lot complet, 24/24, exits 0/0) : MC favorise le
réel sur les 12 paires (+0,006 à +0,161), S_sep sur 10/12
(exceptions : G1/stage −0,058 et G3/stage 0,000), mais Delta et
la falsification sont partagés et L7b est FRAGILE partout sauf
sur 2 nuls — aucune séparation démontrée, seulement des pistes
dans le sens réel, comme partout ailleurs dans ce projet. Les
deux plus grands écarts MC sont sur le stade (G3 +0,161,
G5 +0,152, G1 +0,138), là où les tests directs ne montrent
pourtant rien de cohérent pour G3 : un score seul ne fait pas
un signal. Aucun composé volatil n'est mesuré ici : la piste
« odeurs » est testée au niveau des gènes, pas des molécules.

**Le lot.** Chantier §8.58, mission parent 19 nov. 2026 (5 pistes
approuvées le soir du 19 nov., dont « bloc estomac/mucus avec flux
inattendus — récepteurs olfactifs, métabolisme volatil — cherchés
seulement dans les matrices déjà détenues, absent noté absent, rien
inventé »). Protocole gelé `PROTOCOL_stomach_mucus_flux_858.md`
(SHA `3a0762ef…7935`, écrit avant tout inventaire, toute
construction et tout run). Listes candidates définies AVANT tout
regard aux matrices (protocole §1) ; inventaire
`inventory_858.py` (SHA `5105603f…88cd`) ; construction
`build_fluxes_858_tcga.py` (SHA `e861cbd3…2d25`) ; tests directs
`reading_858.py` (SHA `949eb28d…48ff7`) ; extraction pipeline
`extract_858.py` (SHA `a6765721…f6af`) ; construction confirmation
`build_fluxes_858_geo.py` (SHA `3f7d4978…69a4b`).
Provenance complète `PROVENANCE_858.md`.
Pipeline `universal_v6.2.0_cohen.py`, SHA `f07567c4…c3abf`,
revérifié inchangé avant ET après le lot (v6.1 `2af5e5ce…c1c9`,
v6 `bb8bbdba…c0773`) ; mode fast ; 24 runs TCGA (6 groupes ×
2 ordres × réel/nul), exits 0/0, 36 fichiers chacun.
Lancement en `systemd-run` (unités `v62-858` et `v62-858b`,
cette dernière pour G4+G5 en parallèle), surveillance
`watch_v62_858.sh` (arrêtée d'elle-même à 24/24, tour 2,
06h44:36Z) ; journaux `runs_v62_858.log` (FIN 06h44:16Z,
déjà faits 13, terminés 11, échecs 0) et `runs_v62_858b.log`
(FIN 06h16:50Z, déjà faits 3, terminés 5, échecs 0).
Incidents : la machine a redémarré deux fois pendant le lot
(20 nov. vers 03h44 UTC et vers 05h43 UTC), tuant les unités
à chaque fois — relancées à chaque fois, reprise sans perte
(jamais de dossier de run supprimé, le lanceur saute les
sorties déjà complètes). Durée totale du lot TCGA : 03h20Z →
06h44Z (~3 h 24, charge partagée avec les autres chantiers).
Aucun dossier de run supprimé, aucun CSV modifié. Le livre
blanc n'est PAS édité, le PDF N'EST PAS régénéré, rien n'est
poussé sur GitHub dans ce chantier.

**Construction des flux (TCGA, méthode v4 exacte).**
log2(RSEM+1), scores acineux (médiane des 11 gènes) et îlots (INS,
GCG, PPY, SST), régression linéaire par gène sur [1, acineux,
îlots], flux = résidu. Vérification de reproduction du CSV v4
(`pdac_tcga_fluxes_v4.csv`, SHA `e7a2adab…a0b0`) : écart max
1,776e-15 (atol 1e-9) — PASSÉE avant toute construction.
Matrice source : `data/tcga_paad_rsem.tar.gz`, MD5
`b09569ce3f4721f514bc137bd109ac0a`. Stade clinique :
`data_clinical_patient.txt`, SHA-256 `0c274268…efe5` (même
fichier qu'au §8.45). Séries : KRAS 178 lignes (ordre = résidu
KRAS croissant, colonne `step`) ; stade 175 lignes (rang
principal I=1..IV=4, départage ex æquo par code-barres, colonne
`STAGE`), mêmes 3 tumeurs exclues qu'au §8.45
(TCGA-3A-A9I5-01, TCGA-3A-A9IO-01, TCGA-IB-7654-01).
Règle de plafonnement gelée : plus de 20 gènes présents → les
20 de plus forte variance des résidus. Nuls : bloc des flux
permuté par lignes, graine 42, `rng(42)`, contrôle intact.
Le contrôle n'est jamais un flux : pas de doublon.
SHA des fichiers dans `manifest_858_files.txt` et
`PROVENANCE_858.md`.

**Groupes construits (flux retenus).**
- G1 mucus/gastrique étendu : 33/36 présents dans TCGA
  (absents : MUC3A, MUC5AC, MUC19), 20 retenus : TFF1, TFF2,
  MUC6, MUC5B, MUC4, AQP5, REG1A, TFF3, GKN1, PGA3, REG3A,
  MUC21, PGA4, GKN2, AGR2, GAST, SPDEF, FCGBP, MUC13, REG1B.
- G2 enzymes digestives : 24/30 présents (absents : AMY1B,
  AMY1C, PRSS2, ELA2A, ELA3A, ELA3B), 20 retenus : PRSS1,
  PRSS3, AMY1A, PNLIPRP2, AMY2B, AMY2A, CPB2, CELA2A, CPA3,
  CELA2B, PNLIP, PLA2G1B, CEL, CPB1, PNLIPRP1, CLPS, CPA2,
  CTRB2, CTRB1, CELA3B. Dont 8 gènes du score acineux
  (PNLIP, CELA2A, CPB1, CLPS, CPA2, CTRB2, CTRB1, CELA3B) —
  voir la réserve G2 ci-dessous.
- G3 récepteurs olfactifs : 356 présents dans TCGA (355 par
  regex `^OR[0-9]+[A-Z]?[0-9]*$` + OR2AT4 par la liste
  fermée), 20 retenus par variance des résidus : OR7D2,
  OR13A1, OR2A4, OR52N4, OR2B6, OR51E2, OR51E1, OR2A7, OR52N2,
  OR2L13, OR1J2, OR2W3, OR10H1, OR2A1, OR4C6, OR7A5, OR3A2,
  OR5K2, OR2T10, OR2C1.
- G4 métabolisme volatil / signalisation : 63/65 présents
  (absents : TAS2R44, TAS2R45), 20 retenus : UGT1A1, ALDH3A1,
  CYP2C9, CYP3A4, ADH1B, UGT2B7, ADH4, ADH1C, ADH6, ADH1A,
  AOX1, FMO1, CYP2E1, NOS1, NOS2, CYP2A6, CBS, TAS1R3,
  ALDH3B1, TAS2R38.
- G5 intestinal / neuroendocrine : 15/15 présents, 15 retenus :
  CDX1, CDX2, VIL1, SI, LCT, FABP2, APOA4, APOB, KRT7, KRT19,
  CHGA, CHGB, SYP, INSM1, NEUROD1.
- TEMOIN acineux (11 gènes du score de pureté) : 11/11
  présents, 11 retenus : PNLIP, CTRB2, CELA3A, CTRB1, CPA1,
  CELA2A, CPB1, CELA3B, CLPS, CTRC, CPA2.

**Inventaire — présence/absence par matrice (comptes exacts).**
Fichier vérifié `inventory_858.csv` (SHA `808de016…3ae9`),
scan OR `or_scan_858.csv` (SHA `5e90a9e4…b73`), résumé
`inventory_858_summary.txt`. Univers : TCGA 20 502 symboles
(178 tumeurs) ; GSE71729 19 749 (matrice complète 357
échantillons, dont les 145 tumeurs PDAC du projet) ; GSE62452
27 086 (matrice complète 130 échantillons, dont les 69 tumeurs
du projet ; mapping GPL6244, 25 293 sondes avec symbole) ;
ICGC 18 247 (96 échantillons → 70 tumeurs) ; CPTAC UMich
11 419 gènes-protéines (68 tumeurs) ; CPTAC BCM 11 403
(52 tumeurs) ; DepMap CRISPR 17 916 gènes (dépendance, pas
expression). Comptes présents / listés :

| Groupe (n listé) | TCGA | GSE71729 | GSE62452 | ICGC | CPTAC UMich | CPTAC BCM | DepMap CRISPR |
|---|---|---|---|---|---|---|---|
| G1 mucus/gastrique (36) | 33 | 32 | 33 | 27 | 26 | 26 | 27 |
| G2 enzymes digestives (30) | 24 | 21 | 23 | 21 | 23 | 22 | 21 |
| G4 volatil/signalisation (65) | 63 | 58 | 62 | 38 | 26 | 26 | 60 |
| G5 intestinal/neuroendocrine (15) | 15 | 15 | 15 | 15 | 12 | 12 | 15 |
| REF bloc v4 (12) | 12 | 12 | 12 | 12 | 11 | 11 | 10 |
| G3 OR, liste fermée (6) | 6 | 4 | 6 | 1 | 0 | 0 | 6 |
| TEMOIN acineux (11) | 11 | 8 | 10 | 11 | 11 | 10 | 11 |

Absents notables (listes complètes dans `inventory_858.csv`) :
TCGA — G1 : MUC3A, MUC5AC, MUC19 ; G2 : AMY1B, AMY1C, PRSS2,
ELA2A, ELA3A, ELA3B ; G4 : TAS2R44, TAS2R45 ; G5 : aucun.
ICGC — G1 : MUC7, MUC19, PGA3, PGA4, PGA5, ATP4A, ATP4B,
LIPF, GAST ; G2 : CELA1, CPB2, AMY1A, AMY1B, AMY1C, PRSS2,
ELA2A, ELA3A, ELA3B ; G4 : ADH1A, ADH7, CYP2A6, CYP2A13,
CYP1A2, tous les TAAR (1, 2, 5, 6, 8, 9), TAS1R1, TAS1R2,
et 17 TAS2R (dont TAS2R38, TAS2R44, TAS2R45) ; G5 : aucun.
CPTAC (UMich et BCM, identiques à un gène près) — G1 :
MUC7, MUC12, MUC15, MUC19, MUC21, PGA3, PGA4, PGA5, ATP4B,
GIF ; G4 : tous les TAAR, tous les TAS1R/TAS2R, CYP2E1,
CYP2A6, CYP2A13, CYP1A2, CBS (39 absents sur 65) ; G5 :
CDX2, INSM1, NEUROD1. Les récepteurs du goût et de l'odorat
sont absents des matrices protéiques : une protéine
membranaire à 7 domaines transmembranaires, exprimée à bas
niveau, n'y est pas détectée — c'est une limite de mesure,
pas une preuve d'absence biologique.
DepMap CRISPR (dépendance, pas expression) — G1 absents :
MUC3A, MUC5AC, MUC13, MUC19, PGA3, PGA4, PGA5, GIF, FCGBP ;
G2 : PNLIPRP2, AMY2B, AMY1A, AMY1B, AMY1C, PRSS2, ELA2A,
ELA3A, ELA3B ; G4 : ADH1C, ALDH3B1, TAAR9, TAS2R44, TAS2R45 ;
REF : DPCR1, MUC2 absents (DPCR1 est un symbole ambigu,
déjà exclu en protéine au §8.33).

**Les odeurs, en chiffres (G3).** Scan regex sur les univers :
TCGA 355 symboles OR, GSE71729 113, GSE62452 360, ICGC 3
(OR2A7, OR51E1, OR7D2), CPTAC UMich 1, CPTAC BCM 1,
DepMap CRISPR 302. La présence comme ligne de matrice ne dit
rien de l'expression : dans TCGA, la fraction médiane de
tumeurs avec RSEM > 0 est de 0,011 sur les 355 OR ; 19 OR
seulement sont détectés (RSEM > 0) dans plus de la moitié des
tumeurs, 34 dans plus du quart. Les plus exprimés
(médiane log2(RSEM+1) ; fraction de tumeurs RSEM > 0) :
OR2A7 7,569 ; 1,000 — OR2A4 4,845 ; 1,000 — OR51E1 4,179 ;
1,000 — OR51E2 2,783 ; 0,994 — OR2A1 2,260 ; 0,972 —
OR13A1 2,097 ; 0,966 — OR7D2 1,182 ; 0,871 — OR2W3 1,028 ;
0,764 — OR52N4 1,239 ; 0,747 — OR1L8 0,592 ; 0,702.
Les 6 OR de la liste fermée sont présents dans TCGA (6/6) ;
dans GSE71729, OR2AT4 et OR2J3 sont absents ; dans ICGC,
seul OR51E1 est présent sur les 6 (OR51E2, OR2AT4, OR1A1,
OR2J3, OR10J5 absents) — la matrice ICGC a filtré les
gènes à basse expression, ce n'est pas une mesure d'absence.
En protéine (CPTAC), aucun des 6 n'est détecté. Une
expression mesurée n'est PAS une preuve de fonction
olfactive ; un OR présent à expression quasi nulle n'est
PAS une preuve d'olfaction. Aucun composé volatil n'est
mesuré dans ce chantier (pas de volatilome détenu).

**Tests directs (harnais, hors pipeline ; `direct_tests_858.csv`,
SHA `6ff4d9aa…8ba`, 212 lignes ; d de Cohen, + = plus haut
chez les 12 dernières lignes ; rho de Spearman contre le rang
de contrôle ; mêmes indices sur le nul).** Seuil de Bonferroni
sur les 212 rho : 0,05/212 ≈ 0,00024. Les p sont nominales,
bilatérales, sauf mention.

- G5 / KRAS — le signal le plus net du chantier : SYP
  rho −0,392 (p = 6,1e-08), INSM1 −0,343 (p = 2,8e-06),
  KRT19 +0,333 (p = 5,5e-06), CHGB −0,311 (p = 2,4e-05),
  KRT7 +0,308 (p = 2,9e-05), CHGA −0,212 (p = 0,0046) —
  tous au-delà du nul (max |rho| du nul : 0,090) et tous
  sauf CHGA sous le seuil de Bonferroni. Tertiles haut
  contre bas (D2b) : SYP −0,88 (p = 5,9e-06, nul −0,01),
  KRT19 +0,79 (p = 8,3e-05, nul −0,02), INSM1 −0,77
  (p = 9,1e-05, nul −0,06), KRT7 +0,74 (p = 0,00034,
  nul −0,08). Lecture : le programme neuroendocrine
  (SYP, CHGB, CHGA, INSM1, NEUROD1) s'efface quand KRAS
  monte, pendant que les kératines ductales (KRT7, KRT19)
  montent. Top-12 (D1) : SYP −0,58 (nul +0,47), CHGB
  −0,47 (nul +0,62) — le nul va dans l'autre sens.
- G5 / stade — même sens, plus faible : SYP rho −0,276
  (p = 0,00022), CHGB −0,250 (p = 0,00084), NEUROD1 −0,210
  (p = 0,0052), INSM1 −0,198 (p = 0,0085) ; nul max |rho|
  0,206. Top-12 : VIL1 +0,40, SYP −0,30. D2a (IV contre I,
  n = 4 contre 21) : SYP −0,91 (p = 0,047), mais le nul
  atteint +2,13 (SI) sur ce contraste — non distinctif
  à n = 4, comme au §8.45.
- G1 / KRAS — le mucus étendu MONTE avec KRAS, à l'inverse
  du bloc v4 qui chute : MUC4 rho +0,313 (p = 2,0e-05),
  AGR2 +0,328 (p = 7,7e-06), MUC5B +0,222 (p = 0,0028),
  SPDEF +0,192 (p = 0,010) ; nul max |rho| 0,088. D2b :
  MUC4 +0,80 (p = 4,9e-05, nul −0,15), AGR2 +0,76
  (p = 1,3e-05, nul −0,13), MUC5B +0,66 (p = 0,0074,
  nul +0,02). Top-12 : MUC6 −0,52, MUC4 +0,51 — le top-12
  seul mélange les sens, la tendance (rho, tertiles) est
  la lecture qui tient.
- G1 / stade — même sens que le bloc v4 (§8.45 : PGC +0,51,
  CLDN18 +0,57) : TFF1 top-12 +0,54 (nul −0,24),
  rho +0,204 (p = 0,0067) ; GKN1 +0,46 ; AQP5 +0,45 ;
  AGR2 rho +0,208 (p = 0,0056) ; nul max |rho| 0,096.
  D2b : REG1B −0,59 (p = 0,10), PGA4 +0,59 (p = 0,19) —
  non significatifs, lus contre le nul seulement.
- G4 / KRAS — partagé, par gène : UGT1A1 rho +0,378
  (p = 2,0e-07), ALDH3B1 +0,303 (p = 3,9e-05), ADH1A
  −0,313 (p = 2,1e-05), AOX1 −0,289 (p = 9,2e-05),
  TAS2R38 top-12 +0,85 mais rho +0,151 seulement ;
  nul max |rho| 0,174. D2b : UGT1A1 +0,83 (p = 1,8e-05,
  nul −0,01), ALDH3B1 +0,74 (p = 0,00038, nul −0,13),
  ADH1A −0,59 (p = 0,00045, nul +0,03), AOX1 −0,58
  (p = 0,0012, nul +0,04). Pas un programme unique :
  une détoxification (UGT1A1, ALDH3B1) qui monte et un
  métabolisme de l'alcool (ADH1A, AOX1) qui descend.
- G4 / stade — faible : CYP2C9 rho +0,237 (p = 0,0016),
  UGT1A1 +0,203 (p = 0,0072), UGT2B7 +0,177 (p = 0,019) ;
  top-12 max +0,44 (CYP2C9), nul max +0,55 — dans
  l'enveloppe du nul. D2b : rien de significatif
  (ADH4 +0,61, p = 0,055).
- G3 / KRAS — pas de signal de groupe : rho max 0,259
  (OR2A4, p = 0,00048 ; D2b +0,65, p = 0,00078,
  nul +0,26), OR2C1 −0,208, OR2L13 −0,192 ; top-12 :
  OR7A5 +0,77 mais rho +0,071 (artefact de top-12, pas
  de tendance), OR2A1 −0,64, OR52N4 −0,49 ; le nul
  atteint +0,72 (OR7D2) en top-12 — dans l'enveloppe.
  Un seul OR, OR2A4 — le deuxième plus exprimé de la
  famille (médiane 4,845, détecté dans 100 % des tumeurs)
  — monte avec KRAS : une piste par gène, pas un
  programme olfactif.
- G3 / stade — rien : rho max 0,223, top-12 max 0,57
  (OR10H1), nul max 0,73 — dans l'enveloppe du nul.
- G2 / KRAS — chute, mais c'est le témoin : CELA2A −0,76,
  AMY2B −0,70, AMY1A −0,69 (D2b, p ≤ 0,0024, nul ≤ +0,37),
  CELA3B −0,48, AMY2A −0,42 ; rho max 0,262. Le TEMOIN
  acineux donne les mêmes chiffres gène pour gène
  (CELA2A −0,76, rho −0,228 ; CELA3B −0,48 ; CLPS −0,40)
  parce que ce sont les mêmes résidus : la chute G2 avec
  KRAS EST la perte du programme acineux, déjà connue
  (§8.31–§8.33), pas un nouveau signal.
- G2 / stade — rien au-delà du nul : rho max 0,244
  (PLA2G1B, p = 0,0011, non significatif après
  Bonferroni) ; top-12 max 0,57 (CPB1), nul max 0,64.
- TEMOIN / KRAS : chute acineuse (CELA2A −0,76 D1,
  CTRC rho −0,269, p = 0,00028) ; TEMOIN / stade : plat
  (rho max 0,166, top-12 dans l'enveloppe du nul).
  Le témoin fait exactement ce qu'il doit faire : il
  valide que la méthode voit la perte acineuse sous
  KRAS et rien sous le stade — et il disqualifie toute
  lecture « nouvelle » de G2 sous KRAS.

**Le pipeline (lot complet — 24/24 runs, exits 0/0).**
Lecture `extract_858.py` (`extract_858.json`, `extract_858.csv`) ;
cascade en % (T_-2 / T_-1 / T_0 / T_+1 / T_+2) ; MC = best_config
score (seuil entre parenthèses, en %) ; S_sep = max_separation ×
stability ; Delta ; L7a (direction, confiance) ; falsification ;
L7b ; bruit (score moyen) ; F1/F2 « Tous » (rapport après/avant,
médiane sur 29 estimateurs). Aucun seuil de séparation n'était
pré-enregistré : les écarts sont des pistes, jamais des preuves.

| Groupe / ordre | MC réel (seuil) | MC nul | ΔMC | S_sep réel | S_sep nul | ΔS_sep | Delta réel | Delta nul | L7a réel | fals réel | fals nul | L7b |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 / KRAS | 0,3606 (10,9 %) | 0,3173 | +0,043 | 0,3711 | 0,1126 | +0,259 | 4,088 | 3,922 | UP 0,181 | 0,737 | 0,700 | FRAGILE / FRAGILE |
| G1 / stade | 0,5106 (25,7 %) | 0,3731 | +0,138 | 0,1325 | 0,1908 | −0,058 | 4,026 | 3,178 | UP 0,344 | 0,424 | 0,678 | FRAGILE / ROBUSTE (nul) |
| G2 / KRAS | 0,3390 (65,2 %) | 0,3225 | +0,017 | 0,2538 | 0,1467 | +0,107 | 4,243 | 3,094 | UP 0,172 | 0,856 | 0,903 | FRAGILE / FRAGILE |
| G2 / stade | 0,3358 (11,0 %) | 0,3260 | +0,010 | 0,2204 | 0,1608 | +0,060 | 4,267 | 3,947 | UP 0,208 | 0,838 | 0,837 | FRAGILE / FRAGILE |
| G3 / KRAS | 0,3417 (89,3 %) | 0,3272 | +0,015 | 0,2795 | 0,1763 | +0,103 | 3,125 | 3,820 | DOWN 0,198 | 0,669 | 0,671 | FRAGILE / FRAGILE |
| G3 / stade | 0,4862 (17,4 %) | 0,3252 | +0,161 | 0,1605 | 0,1609 | −0,000 | 3,996 | 3,819 | UP 0,203 | 1,041 | 0,839 | FRAGILE / FRAGILE |
| G4 / KRAS | 0,3472 (10,9 %) | 0,3287 | +0,019 | 0,3046 | 0,1798 | +0,125 | 4,260 | 4,248 | UP 0,241 | 0,903 | 0,823 | FRAGILE / FRAGILE |
| G4 / stade | 0,3405 (11,0 %) | 0,3301 | +0,010 | 0,2441 | 0,1765 | +0,068 | 4,203 | 4,209 | UP 0,395 | 0,830 | 0,900 | FRAGILE / ROBUSTE (nul) |
| G5 / KRAS | 0,3557 (76,1 %) | 0,3290 | +0,027 | 0,3609 | 0,1856 | +0,175 | 3,785 | 3,759 | UP 0,399 | 0,682 | 0,593 | FRAGILE / FRAGILE |
| G5 / stade | 0,5607 (11,0 %) | 0,4085 | +0,152 | 0,3843 | 0,2892 | +0,095 | 3,827 | 3,808 | UP 0,191 | 0,716 | 0,707 | FRAGILE / FRAGILE |
| TEMOIN / KRAS | 0,3409 (67,4 %) | 0,3243 | +0,017 | 0,2679 | 0,1561 | +0,112 | 4,166 | 3,085 | DOWN 0,168 | 0,889 | 1,014 | FRAGILE / FRAGILE |
| TEMOIN / stade | 0,3348 (14,3 %) | 0,3286 | +0,006 | 0,2178 | 0,1718 | +0,046 | 4,287 | 3,937 | DOWN 0,408 | 0,914 | 0,839 | FRAGILE / FRAGILE |

Cascades : G1/KRAS réelle 0,0 / 2,1 / 99,0 / 100 / 100 %
(T_0 au pas 176, dégénérée en bout d'axe) contre nul 0,0 / 8,5 /
79,5 / 96,9 / 96,9 % ; G2/KRAS réelle 0,0 / 8,5 / 99,0 / 100 /
100 % (même dégénérescence) ; G1/stade réelle 0,0 / 1,3 / 4,3 /
54,1 / 54,1 % (T_0 au pas 7, très précoce) contre nul 0,5 /
10,3 / 23,2 / 88,8 / 88,8 % ; G5/stage réelle 0,0 / 0,2 / 3,2 /
37,8 / 37,8 % (T_0 au pas 5) contre nul 1,1 / 69,9 / 97,9 /
100 / 100 % ; G3/KRAS réelle 0,0 / 1,6 / 5,9 / 61,3 / 61,3 %
(T_0 précoce) contre nul 0,0 / 11,2 / 47,1 / 76,2 / 76,2 % ;
G5/KRAS réelle 0,0 / 3,7 / 8,0 / 97,4 / 97,4 % contre nul 0,5 /
6,9 / 70,0 / 75,6 / 76,7 % ; TEMOIN/KRAS réelle 0,0 / 84,0 /
96,9 / 99,9 / 100 % (T_-1 à 84 %, cascade tardive) contre nul
2,1 / 39,3 / 43,0 / 93,2 / 93,2 %. Les cascades stade ont
leur T_0 très tôt (pas 5–9 sur 174) et leur T_+1 = T_+2
figé : avec 4 niveaux de stade et 146 tumeurs au stade II,
un « seuil » précoce tombe dans le bloc des ties — il ne
mesure rien, comme au §8.45. Les cascades KRAS ont leur
T_0 très tard (pas 171–176 sur 177) pour G1 et G2 : il ne
reste que 1–2 lignes après le seuil.
Lecture d'ensemble : MC favorise le réel sur les 12 paires
(+0,006 à +0,161 ; les trois plus grands écarts sont sur le
stade : G3 +0,161, G5 +0,152, G1 +0,138) ; S_sep favorise
le réel sur 10/12 (exceptions G1/stade −0,058 et G3/stade
−0,000) ; Delta est partagé (réel devant sur 9/12, dont
G2/KRAS +1,149 et TEMOIN/KRAS +1,081, mais G3/KRAS −0,695) ;
la falsification est partagée (réel devant sur 6/12) ;
L7a est UP partout dans le réel sauf G3/KRAS et TEMOIN
(DOWN), et UP partout dans le nul sauf G4/KRAS (DOWN) ;
L7b est FRAGILE partout sauf sur 2 nuls (G1/stade,
G4/stade) ; régime divergence partout ; bruit « proxy de
variance modéré » presque partout (scores 0,46–0,78).
F1/F2 « Tous » : les rapports après/avant s'effondrent ou
explosent sans direction cohérente (F1 ×0,010 à ×28,2 réel
contre ×0,019 à ×33,7 nul ; F2 ×0,008 à ×68,5 réel contre
×0,011 à ×53,1 nul) et le signe de F1 change chez 19 à 27
estimateurs sur 29 des deux côtés. Même figure qu'aux
§8.31/§8.32/§8.34/§8.36/§8.45 : des pistes dans le sens
réel sur MC et S_sep, contredites ou non confirmées par
Delta, la falsification et L7b — pas une séparation
démontrée. Le cas G3/stade est l'avertissement : le plus
grand écart MC du lot (+0,161) avec S_sep à égalité
(0,1605 contre 0,1609), Delta +0,177 seulement, et des
tests directs plats — un score seul ne fait pas un signal.

**Confirmation sur autres cohortes (règle conditionnelle gelée,
protocole §6 — statuée à 24/24 TCGA).** Critère : (MC réel − MC
nul > 0,05) OU (S_sep réel − S_sep nul > 0,05) OU (un test direct
D1 |d| ≥ 0,50 au-delà du nul), sur au moins un ordre TCGA.
- G1 : QUALIFIÉ (MC stade +0,138 ; S_sep KRAS +0,259 ;
  D1 TFF1 +0,54 stade, D2b MUC4 +0,80 / AGR2 +0,76 KRAS).
- G2 : QUALIFIÉ (S_sep KRAS +0,107, stade +0,060 ; D1 CELA2A
  −0,76 KRAS) — avec la réserve que ses tests directs sont
  expliqués par le témoin acineux (voir G2 ci-dessus) : la
  confirmation teste si la même chute se retrouve ailleurs,
  pas si elle est « nouvelle ».
- G3 : QUALIFIÉ (MC stade +0,161 ; S_sep KRAS +0,103 ; D1
  OR7A5 +0,77 KRAS) — avec l'avertissement que ses tests
  directs sont plats et sa S_sep stade à égalité : la
  confirmation dira si l'écart MC stade tient ailleurs.
- G4 : QUALIFIÉ (S_sep KRAS +0,125, stade +0,068 ; D1 ADH1C
  −0,86, TAS2R38 +0,85 KRAS).
- G5 : QUALIFIÉ (MC stade +0,152 ; S_sep KRAS +0,175, stade
  +0,095 ; D2b SYP −0,88, KRT19 +0,79 KRAS).
- TEMOIN : non candidat (témoin de construction), pas de
  confirmation.
Les 5 groupes qualifiés sont donc confirmés. Construction
`build_fluxes_858_geo.py` (SHA `3f7d4978…69a4b`, variante (a)
des scripts du projet : mêmes gènes que les listes retenues
TCGA — ceux présents dans la cohorte — ordre KRAS brut,
sans correction de pureté, cas complets) :
- GSE71729 (145 tumeurs primaires) : 5 groupes × KRAS
  (réel + nul) = 10 runs. Gènes retenus présents : G1 17/20
  (absents : MUC5B, MUC21, PGA4), G2 15/20 (absents : AMY1A,
  AMY2A, CELA2A, CELA2B, CELA3B), G3 11/20 (absents :
  OR13A1, OR2A4, OR52N4, OR52N2, OR1J2, OR2A1, OR4C6,
  OR5K2, OR2T10 — dont OR2A4, la piste OR/KRAS de TCGA :
  elle ne peut pas être confirmée sur cette puce, c'est
  dit tel quel), G4 17/20 (absents : UGT1A1, ADH1B,
  TAS1R3 — dont UGT1A1, le plus fort rho G4/KRAS de TCGA :
  non confirmable ici), G5 15/15.
- GSE62452 (69 tumeurs) : 5 groupes × (KRAS + stade)
  (réel + nul) = 20 runs. Gènes retenus présents : G1 19/20
  (absent : PGA4), G2 18/20 (absents : AMY1A, CTRB1),
  G3 17/20 (absents : OR2A4, OR2A1, OR3A2 — OR2A4 absent
  ici aussi : la piste OR2A4/KRAS n'est confirmable dans
  aucune des deux cohortes), G4 20/20, G5 15/15. Stade
  GSE62452 (règle gelée dans `build_fluxes_858_geo.py`
  avant la construction : IA/IB → I, IIA/IIB → II,
  III → III, IVA/IVB/IV → IV, « >IIB » exclu car ambigu,
  départage GSM lexicographique) : I 4, II 45, III 13,
  IV 6, 1 exclue (« >IIB ») — série stade 68 lignes
  (≥ 40, seuil respecté).
Lots de confirmation lancés le 20 nov. (unités `v62-858c`
pour GSE71729, 10 runs, manifeste `manifest_v62_858_71729.txt` ;
`v62-858d` pour GSE62452, 20 runs, manifeste
`manifest_v62_858_62452.txt` ; surveillance
`watch_v62_858_geo.sh`). **TERMINÉS 30/30, exits 0/0** :
`WATCH 858-71729 TERMINE 10/10`, `WATCH 858-62452 TERMINE
20/20` (20 nov. 08h37Z). Trois redémarrages de machine
durant le lot (vers 07h21 UTC et avant), unités relancées
à chaque fois, reprise sans perte. Pipeline revérifié
inchangé après le lot : SHA `f07567c48a562506…c3abf`.
Lecture `extract_858_geo.py` (`extract_858_geo.json` /
`extract_858_geo.csv`, 30 runs, 0 manquant).

**Table pipeline — confirmations (réel contre nul).**
MC / S_sep / Delta / L7a / falsification ; écart réel − nul
entre parenthèses.

GSE71729, ordre KRAS (n=145) :
| Groupe | MC réel | MC nul | S_sep réel | S_sep nul | Delta réel | Delta nul | L7a | fals. réel | fals. nul |
|---|---|---|---|---|---|---|---|---|---|
| G1 | 0,352 | 0,337 (+0,015) | 0,328 | 0,243 (+0,085) | 2,885 | 2,916 (−0,031) | up / down | 0,523 | 0,592 |
| G2 | 0,350 | 0,348 (+0,002) | 0,322 | 0,295 (+0,027) | 2,829 | 2,025 (+0,804) | down / down | 0,443 | 0,496 |
| G3 | 0,357 | 0,344 (+0,013) | 0,365 | 0,284 (+0,082) | 2,893 | 2,902 (−0,009) | up / up | 0,536 | 0,560 |
| G4 | 0,342 | 0,323 (+0,019) | 0,267 | 0,142 (+0,125) | 2,877 | 2,872 (+0,005) | up / up | 0,552 | 0,500 |
| G5 | 0,335 | 0,328 (+0,007) | 0,233 | 0,183 (+0,050) | 2,901 | 2,883 (+0,018) | down / up | 0,620 | 0,559 |

GSE62452, ordre KRAS (n=69) :
| Groupe | MC réel | MC nul | S_sep réel | S_sep nul | Delta réel | Delta nul | L7a | fals. réel | fals. nul |
|---|---|---|---|---|---|---|---|---|---|
| G1 | 0,361 | 0,338 (+0,023) | 0,422 | 0,251 (+0,171) | 1,425 | 1,342 (+0,083) | up / up | 0,127 | 0,263 |
| G2 | 0,386 | 0,335 (+0,051) | 0,603 | 0,229 (+0,374) | 1,648 | 1,221 (+0,427) | down / down | 0,221 | 0,201 |
| G3 | 0,348 | 0,329 (+0,020) | 0,334 | 0,193 (+0,141) | 1,474 | 1,438 (+0,036) | up / down | 0,027 | 0,109 |
| G4 | 0,376 | 0,331 (+0,045) | 0,533 | 0,206 (+0,327) | 1,447 | 1,376 (+0,071) | up / up | 0,139 | 0,190 |
| G5 | 0,367 | 0,342 (+0,024) | 0,462 | 0,286 (+0,176) | 1,393 | 1,429 (−0,036) | up / down | 0,102 | 0,140 |

GSE62452, ordre stade (n=68) :
| Groupe | MC réel | MC nul | S_sep réel | S_sep nul | Delta réel | Delta nul | L7a | fals. réel | fals. nul |
|---|---|---|---|---|---|---|---|---|---|
| G1 | 0,345 | 0,335 (+0,010) | 0,316 | 0,241 (+0,075) | 1,474 | 1,531 (−0,057) | up / up | 0,128 | 0,159 |
| G2 | 0,381 | **0,519 (−0,138)** | 0,469 | 0,220 (+0,249) | 1,619 | 1,399 (+0,220) | down / down | 0,322 | 0,180 |
| G3 | 0,330 | 0,336 (−0,006) | 0,207 | 0,251 (−0,044) | 1,453 | 1,380 (+0,073) | down / up | 0,012 | 0,103 |
| G4 | 0,337 | 0,333 (+0,004) | 0,245 | 0,215 (+0,030) | 1,451 | 1,361 (+0,090) | up / up | 0,116 | 0,237 |
| G5 | 0,333 | 0,333 (+0,000) | 0,233 | 0,224 (+0,009) | 1,490 | 1,402 (+0,088) | down / flat | 0,183 | 0,105 |

Lecture d'ensemble (15 paires réel/nul) : MC favorise le
réel 13/15 (écarts +0,002 à +0,051 ; exceptions : G2/stade
−0,138 — le nul y atteint 0,519, plus haut que n'importe
quel réel du chantier — et G3/stade −0,006) ; S_sep
favorise le réel 14/15 (seule exception G3/stade −0,044) ;
Delta favorise le réel 11/15 ; falsification 5/15. L7a :
réel up dans 9/15, nul up dans 7/15 — sans direction
propre. L7b FRAGILE dans 28/30 runs (ROBUSTE seulement
G3/stade réel et G4/stade réel, GSE62452) — même
non-informativité que dans TCGA : FRAGILE partout, réel
comme nul. Delta : 1,39–2,90 dans ces cohortes contre
~3,8–4,2 dans TCGA — l'échelle suit n (n=69/145 contre
178), cohérent avec §8.40. Le pipeline, dans ces
confirmations comme dans TCGA, donne de petits écarts
favorables au réel sur MC et S_sep, partagés sur Delta,
inversés ou plats sur la falsification : il ne sépare pas
nettement du nul — le même verdict que dans TCGA, tenu
sur trois cohortes.

**Tests directs — confirmations** (`reading_858_geo.py`,
`direct_tests_858_geo.csv`, 253 lignes, mêmes D1/D3 que
TCGA ; seuil de Bonferroni 0,05/253 ≈ 0,0002 ; nul max
|rho| indiqué par groupe).
- G5 (neuroendocrine) CONFIRME dans les deux cohortes,
  ordre KRAS : GSE62452 SYP rho −0,503 (p 1,1e-05),
  KRT19 +0,416, INSM1 −0,413, KRT7 +0,398, CDX1 −0,387
  (nul max 0,283) ; GSE71729 CHGA −0,359 (p 9,2e-06),
  INSM1 −0,296, KRT19 +0,281, KRT7 +0,278 (nul max
  0,137). SYP est plat dans GSE71729 (rho −0,086, p 0,31)
  — la confirmation porte sur le programme (CHGA/INSM1
  chutent, KRT7/KRT19 montent), pas sur chaque gène.
  Ordre stade (GSE62452) : NEUROD1 −0,416 (p 0,00042),
  CHGA −0,348 (nul max 0,202) — même sens que TCGA
  (SYP −0,276, CHGB −0,250).
- G4 (volatil) CONFIRME, ordre KRAS, et plus fort qu'en
  TCGA : GSE62452 AOX1 −0,611 (p 2,6e-08), UGT1A1 +0,541
  (p 1,6e-06), NOS1 −0,529 (p 3,0e-06), NOS2 −0,424,
  CBS −0,423 (nul max 0,336) ; GSE71729 NOS1 −0,369
  (p 4,9e-06), ALDH3A1 +0,367 (p 5,7e-06), CBS −0,275,
  AOX1 −0,253 (nul max 0,173). Deux nuances : NOS1 était
  plat dans TCGA (rho +0,067) — sa chute n'apparaît que
  dans les deux cohortes GEO ; UGT1A1 est absent de
  GSE71729 (confirmé seulement dans GSE62452). Ordre
  stade (GSE62452) : rien (rho max 0,291, FMO1) — comme
  dans TCGA.
- G1 (mucus étendu) CONFIRME PARTIELLEMENT, ordre KRAS :
  AGR2 +0,383 (p 1,9e-06) dans GSE71729, même sens que
  TCGA (+0,328) ; MUC13 +0,264, TFF1 +0,236. Mais MUC4
  est plat dans GSE71729 (rho −0,083, contre +0,313 dans
  TCGA) et MUC6 CHUTE dans GSE71729 (rho −0,436,
  p 4,2e-08 ; D1 −0,29) alors qu'il était plat dans TCGA
  (rho +0,035). La montée du mucus avec KRAS n'est donc
  pas un programme : AGR2 monte dans les deux, MUC4
  seulement dans TCGA, MUC6 chute dans GSE71729.
- G3 (odeurs) : le sens est une CHUTE, pas une montée.
  GSE71729 ordre KRAS : OR2W3 −0,338 (p 3,3e-05),
  OR10H1 −0,275, OR3A2 −0,246, OR2B6 −0,220, OR2C1
  −0,212 (nul max 0,154) ; GSE62452 ordre KRAS :
  OR13A1 −0,423 (p 0,00029, D1 −1,16), OR2T10 −0,418
  (p 0,00036), OR5K2 −0,302 (nul max 0,207). Dans TCGA
  ces mêmes gènes étaient déjà négatifs ou plats
  (OR13A1 −0,152, OR2T10 −0,154, OR2C1 −0,208) —
  la chute de plusieurs OR avec KRAS est cohérente sur
  les trois cohortes, mais aucun OR ne monte. OR2A4, le
  seul OR qui montait dans TCGA (+0,259), est absent des
  deux puces : sa piste reste non confirmable, et le
  bilan des odeurs est donc : plusieurs OR chutent avec
  KRAS, aucun ne monte. Ordre stade (GSE62452) : rien
  de net (rho max 0,303, OR2B6, p 0,012, non significatif
  après Bonferroni).
- G2 (enzymes digestives) : chute acineuse retrouvée,
  ordre KRAS : GSE62452 PNLIP −0,381, PNLIPRP1 −0,378,
  CTRB2 −0,374 (nul max 0,138) ; GSE71729 faible
  (CPA3 +0,273 en tête, puis CEL −0,175, CTRB2 −0,173)
  — comme dans TCGA, c'est la perte acineuse, pas un
  nouveau signal. Ordre stade : rien (rho max 0,163).

**Réserve de méthode — à lire avec le verdict.** Les flux sont
des résidus après correction de pureté : ils mesurent
l'expression tumorale une fois retirée la composante tissu
normal acineux/îlots, sous l'hypothèse linéaire de la v4.
G2 est biaisé par construction (8/20 flux retenus sont des
gènes du score acineux) : ses lectures sous KRAS sont
disqualifiées comme « nouvelles » par le témoin, et ses
lectures sous le stade sont nulles. Le stade est une variable
clinique (AJCC 7e édition), pas une mesure du système :
4 niveaux, ties massives (IIB 118/175), ordre intra-stade
arbitraire, sommet mince (III + IV = 8 tumeurs) — mêmes
limites qu'au §8.45 ; un d à n = 4 bouge de ~0,5 quand une
seule tumeur change. Les OR sont mesurés comme transcrits :
aucune odeur, aucun ligand, aucun test fonctionnel dans ce
chantier. Les p sont nominales ; seul le seuil de Bonferroni
0,05/212 ≈ 0,00024 protège contre les 212 tests directs —
les rho G5/KRAS (SYP, INSM1, KRT19, KRT7, CHGB) et G4/KRAS
(UGT1A1, ALDH3B1, ADH1A) le passent ; les autres sont des
pistes. Ne jamais exiger de consensus entre flux ou
contrôles : les groupes ne bougent pas ensemble — G1 monte
quand G5 descend sous KRAS, et c'est l'information.

**Ce que ça change.** Trois choses neuves, toutes mesurées
aujourd'hui, aucune importée : (1) le programme
neuroendocrine s'efface quand KRAS monte et quand le stade
avance, pendant que les kératines ductales montent — c'est
le seul groupe cohérent dans les deux ordres, et il passe
Bonferroni ; **il tient dans les deux cohortes de
confirmation, gène par gène dans les deux sens** — c'est le
signal le plus solide du chantier ; (2) le mucus étendu
(MUC4/AGR2/MUC5B) monte avec KRAS alors que le bloc v4 chute
— le « bloc estomac/mucus » n'est pas un bloc unique : une
partie monte, l'autre chute, sous le même axe ; **mais la
confirmation est partielle : AGR2 monte partout, MUC4
seulement dans TCGA, MUC6 chute dans GSE71729** — il n'y a
pas de programme mucus unique ; (3) les odeurs existent
comme transcrits (19 OR détectés dans plus de la moitié des
tumeurs, OR2A7/OR2A4/OR51E1 en tête) mais ne forment pas un
programme : un seul OR, OR2A4, suit KRAS — et il est absent
des deux puces de confirmation, donc non confirmable
ailleurs. **Quatrième chose, venue des confirmations : le
volatil (G4) est le deuxième signal confirmé — AOX1 chute
dans les trois cohortes (−0,289 / −0,253 / −0,611), UGT1A1
monte dans TCGA et GSE62452 (+0,378 / +0,541), NOS1 chute
dans les deux cohortes GEO (−0,369 / −0,529) alors qu'il
était plat dans TCGA ; et les odeurs, confirmées dans
l'autre sens : plusieurs OR chutent avec KRAS dans les deux
cohortes GEO, aucun ne monte.** Le reste — enzymes
digestives, volatil sous le stade, OR sous le stade — ne
sort pas du nul. Le pipeline, dans les confirmations comme
dans TCGA, donne de petits écarts favorables au réel sur MC
(13/15) et S_sep (14/15), partagés sur Delta (11/15),
inversés sur la falsification (5/15) : il ne sépare pas
nettement du nul — le même verdict, tenu sur trois cohortes.
Prochaines étapes : intégration au livre blanc et publication
(PDF + GitHub) sur go de Zackary ; rien n'a été poussé, rien
n'a été régénéré dans ce chantier.
