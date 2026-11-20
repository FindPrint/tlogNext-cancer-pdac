### 8.66 Bloc estomac / mucus : quatrième cohorte, GSE62165 (20 nov. 2026)

**Verdict d'abord : la quatrième cohorte confirme le cœur du
§8.58 et en casse deux bords.** Le programme neuroendocrine
(G5) s'efface quand KRAS monte — c'est la quatrième cohorte
d'affilée, et la plus forte : KRT19 rho +0,577 (p = 7,7e-12),
KRT7 +0,420, INSM1 −0,350, NEUROD1 −0,341, CHGA −0,338, tous
sous le seuil de Bonferroni ; SYP est plat (−0,131), comme en
GSE71729. Le mucus étendu (G1) monte avec KRAS — AGR2 +0,414,
MUC13 +0,422, MUC4 +0,264 — troisième cohorte pour AGR2,
deuxième pour MUC4. Le volatil (G4) confirme à moitié : AOX1
chute dans les quatre cohortes (−0,382 ici), ALDH3B1 monte
(+0,356), FMO1 chute le plus fort du groupe (−0,421), mais
UGT1A1 est ABSENT de la puce et NOS1 est plat — le bras
« détox qui monte » n'est pas testable ici. **En revanche, le
mucus ne monte PAS avec le stade dans cette cohorte — il
descend** (MUC4 −0,238, TFF1 −0,115, AGR2 −0,137, sens
inverse de TCGA) **et le programme neuroendocrine ne baisse
pas avec le stade** (rho max 0,102, plat) : les deux lectures
« stade » du §8.58 ne tiennent pas ici. **Et les odeurs
cassent leur bilan : un OR MONTE avec KRAS pour la première
fois dans une cohorte de confirmation — OR2B6 +0,293
(p = 0,0013, D1 +0,51), au-delà du nul (max 0,144) — pendant
qu'aucun OR ne chute significativement** (chute max OR2T10
−0,131, p = 0,16) ; OR2A4 est absent de la puce, comme dans
les deux cohortes GEO, et OR2W3 aussi. Le pipeline (lot
complet, 20/20, exits 0/0) ne sépare pas le réel du nul :
MC favorise le réel sur 4/10 paires seulement, S_sep sur 5/10,
falsification sur 5/10, L7b FRAGILE 20/20 — et le plus grand
écart MC du lot (G2/stade +0,199, en faveur du réel) tombe
sur des tests directs plats : un score seul ne fait pas un
signal, comme au §8.58 pour G3/stade.

**Le lot.** Chantier §8.66, mission parent du 20 nov. 2026
(« bloc estomac/mucus, quatrième cohorte »). Protocole gelé
`PROTOCOL_stomach_mucus_cohort4_866.md` (SHA
`3a25a391…58d91bc`, écrit avant tout téléchargement).
Provenance complète `PROVENANCE_866.md` (SHA
`aedc47d3…a408`). Construction `build_fluxes_866.py` (SHA
`9975fad0…10de563`) ; mapping sondes → symboles
`build_probe2symbol_866.py` (SHA `004c8339…1a563b`) ;
tests directs `reading_866.py` (SHA `cf972deb…5710`) ;
extraction `extract_866.py` (SHA `87337cfe…fea76`, corrigée
d'une parenthèse après le lot — même correction que
`reading_866.py`, vérifiée par relecture avant extraction) ;
manifeste des fichiers `manifest_866_files.txt` (SHA
`92542116…a1802`, 41 lignes).
Pipeline `universal_v6.2.0_cohen.py`, SHA
`f07567c4…c3abf`, revérifié inchangé avant ET après le lot ;
mode fast ; 20 runs (5 groupes × 2 ordres × réel/nul),
exits 0/0, 36 fichiers chacun.
Lancement en `systemd-run` (unité `v62-866`), surveillance
`watch_v62_866.sh` (arrêtée d'elle-même à 20/20,
`WATCH 866-62165 TERMINE 20/20`, tour 2, 17h25:47Z) ;
journal `runs_v62_866.log` (FIN 17h25:27Z, déjà faits 19,
terminés 1, échecs 0 — dernier lancement).
Incidents : la machine a redémarré deux fois pendant le lot
(entre 15h13Z et 15h22Z, puis entre 17h07Z et 17h22Z), tuant l'unité à
chaque fois — relancée à chaque fois, reprise sans perte
(6 SKIP puis 19 SKIP, jamais de dossier de run supprimé,
jamais de CSV modifié ; le premier lancement avait terminé
6 runs, le deuxième 13 de plus, le troisième le dernier).
Durée totale du lot : 14h53Z → 17h25Z (~2 h 32, charge
partagée avec les autres chantiers). Le livre blanc n'est
PAS édité, le PDF N'EST PAS régénéré, rien n'est poussé
sur GitHub dans ce chantier.

**La cohorte.** GSE62165, NCBI GEO, déposants Rekin's Janky
et coll. (Nucleomics Core, VIB, Leuven) ; soumission 8 oct.
2014, publique 17 août 2016, dernière mise à jour 21 mars
2019 ; PMID 27520560 ; analyse par stade : Wang et coll.,
*Cancer Cell Int* 2018 (doi 10.1186/s12935-018-0718-5).
Plateforme GPL13667 (Affymetrix Human Genome U219 Array).
Fichier `data/GSE62165_series_matrix.txt.gz`, URL
`https://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62165/matrix/GSE62165_series_matrix.txt.gz`,
HTTP 200, 51 179 939 o, SHA-256
`fd50fc415a31…03727f`. Contenu vérifié : 49 386 sondes × 131
échantillons, 0 NaN ; 118 tumeurs PDAC + 13 tissus non
tumoraux (exclus) ; valeurs log2 déjà normalisées par les
déposants (min 2,084 ; max 14,447 ; médiane 4,707) — aucune
renormalisation faite ici. Stade par échantillon
(`!Sample_characteristics_ch1`, champ « Stage: ») : 1a 1,
1b 7, 2a 30, 2b 62, 3 5, 4 13 — soit rangs I 8, II 92,
III 5, IV 13, identiques aux effectifs publiés ; 0 exclue,
série stade 118 lignes (≥ 40, seuil respecté). Critères
d'acceptation du protocole §2 : n = 118 ≥ 40 — PASSÉ ;
stade par échantillon présent — PASSÉ ; KRAS présent comme
ligne — PASSÉ ; cohorte jamais utilisée dans ce projet
(ni TCGA, ni GSE71729, ni GSE62452, ni ICGC PACA-AU, ni
CPTAC) — PASSÉ. La cohorte de repli GSE57495 (protocole
§1.2) n'a pas été téléchargée ni utilisée.

**Mapping sondes → symboles — adaptation documentée.**
Le protocole §1.1 prévoyait l'annotation GEO
(`GPL13667.annot.gz`, repli SOFT). Constaté après le gel :
`.annot.gz` → HTTP 403 (page d'erreur, 980 o, pas un
fichier) ; `GPL13667_family.soft.gz` → HTTP 200 mais
Content-Length 6 038 451 838 o (~6,0 Go, infaisable sur
cette VM — téléchargement interrompu à 1 511 849 984 o,
fichier supprimé) ; `GPL13667_family.xml.tgz` (MINiML,
539 314 653 o, SHA `ed094f67…ab21f`) → l'archive ne
contient QUE des tables d'échantillons GSM, aucun fichier
GPL (vérifié par `tar -tzf` puis extraction
`--wildcards '*GPL13667*'` : « Not found in archive ») —
archive supprimée. Adaptation (même nature d'annotation,
aucune sonde mappée à la main) : chaîne Bioconductor
AnnotationDbi standard pour la puce hgu219, sonde →
Entrez Gene (`hgu219.db` 3.2.3, SHA
`64847ad0…567fb`, 2 002 040 o, source Entrez Gene
2015-Sep-27) puis Entrez Gene → symbole courant
(`org.Hs.eg.db` 3.23.1, SHA `47062066…49cfe`,
103 790 170 o ; la version 3.23.0 n'existe pas, HTTP 404
vérifié, version exacte lue sur la page du paquet).
Règles gelées dans `build_probe2symbol_866.py` avant la
construction : sonde vers plusieurs Entrez ID → EXCLUE ;
sonde sans Entrez ID → non mappée ; plusieurs sondes vers
un même symbole → médiane. Résultat
(`data/GPL13667_probe2symbol.tsv`, SHA
`c0a5e8fc…8c2b2`) : 46 083 sondes mappées vers 18 448
symboles distincts ; 2 662 sondes multi-gènes exclues ;
641 sondes sans symbole ; journal
`GPL13667_mapping_866.txt`. Limite nommée : la
correspondance sonde → Entrez date de 2015, le symbole
est celui d'aujourd'hui via l'Entrez ID stable (ex.
HIST1H3H → H3C8) ; aucun symbole n'est inventé ni
corrigé à la main.

**Construction des flux (variante (a) du §8.58).**
Mêmes gènes que les listes retenues TCGA (ceux présents
dans la cohorte), ordre = KRAS (valeurs puce brutes,
croissant), sans correction de pureté, cas complets
seulement (118/118 pour chaque groupe). Ordre stade :
IA/IB → I, IIA/IIB → II, III → III, IV → IV ; départage
ex æquo par GSM lexicographique ; 0 exclue.
Sondes multiples vers un même symbole : médiane.
Nuls : bloc des flux permuté par lignes, graine 42,
`rng(42)`, contrôle intact. Le contrôle n'est jamais un
flux : pas de doublon. SHA des fichiers dans
`manifest_866_files.txt` et `PROVENANCE_866.md`.

**Groupes construits (flux retenus).**
- G1 mucus/gastrique : 18/20 présents (absents : PGA3,
  PGA4) : TFF1, TFF2, MUC6, MUC5B, MUC4, AQP5, REG1A,
  TFF3, GKN1, REG3A, MUC21, GKN2, AGR2, GAST, SPDEF,
  FCGBP, MUC13, REG1B.
- G2 enzymes digestives : 14/20 présents (absents : PRSS1,
  AMY1A, AMY2B, AMY2A, CTRB1, CELA3B) : PRSS3, PNLIPRP2,
  CPB2, CELA2A, CPA3, CELA2B, PNLIP, PLA2G1B, CEL, CPB1,
  PNLIPRP1, CLPS, CPA2, CTRB2.
- G3 récepteurs olfactifs : 16/20 présents (absents :
  OR2A4, OR2A7, OR2W3, OR2A1) : OR7D2, OR13A1, OR52N4,
  OR2B6, OR51E2, OR51E1, OR52N2, OR2L13, OR1J2, OR10H1,
  OR4C6, OR7A5, OR3A2, OR5K2, OR2T10, OR2C1.
- G4 volatil / signalisation : 18/20 présents (absents :
  UGT1A1, CYP2A6) : ALDH3A1, CYP2C9, CYP3A4, ADH1B,
  UGT2B7, ADH4, ADH1C, ADH6, ADH1A, AOX1, FMO1, CYP2E1,
  NOS1, NOS2, CBS, TAS1R3, ALDH3B1, TAS2R38.
- G5 intestinal / neuroendocrine : 15/15 présents, 15
  retenus : CDX1, CDX2, VIL1, SI, LCT, FABP2, APOA4,
  APOB, KRT7, KRT19, CHGA, CHGB, SYP, INSM1, NEUROD1.
- TEMOIN acineux (inventaire seulement, pas de run) :
  9/11 présents (absents : CTRB1, CELA3B).

**Inventaire — présence/absence (comptes exacts).**
Fichier vérifié `inventory_866.csv` (SHA
`5c7508a2…68b2`), scan OR `or_scan_866.csv` (SHA
`7e75903c…0ecb`). Univers mappé : 18 448 symboles
(118 tumeurs). Scan regex `^OR[0-9]+[A-Z]?[0-9]*$` :
321 symboles OR dans l'univers (TCGA 355, GSE71729 113,
GSE62452 360). Liste fermée OR du §8.58 : 6/6 présents
(OR51E2, OR51E1, OR2AT4, OR1A1, OR2J3, OR10J5).
Absents notables : G1 PGA3, PGA4 (aussi absents en ICGC
et CPTAC) ; G2 PRSS1, AMY1A, AMY2B, AMY2A, CTRB1,
CELA3B — dont 3 gènes du score acineux (CTRB1, CELA3B)
et les deux amylases : la lecture G2 est affaiblie par
construction ici, comme en GSE71729 ; G3 OR2A4, OR2A7,
OR2W3, OR2A1 — OR2A4 absent pour la troisième cohorte
de confirmation d'affilée, OR2W3 (le plus fort OR en
chute en GSE71729) absent aussi ; G4 UGT1A1, CYP2A6 —
UGT1A1, le plus fort rho G4/KRAS de TCGA (+0,378), est
absent ici comme en GSE71729 : son bras « monte » n'est
testable que dans TCGA et GSE62452.

**Les odeurs, en chiffres (G3).** Les 321 OR ont tous une
médiane log2 < 5,0 dans les tumeurs (médiane des médianes
2,99) ; les plus exprimés : OR2A14 4,99, OR5H1 4,42,
OR2F2 3,90, OR2T4 3,84. Les OR de la liste fermée sont
tous près du plancher : OR51E1 3,51, OR13A1 3,34, OR51E2
3,21, OR2J3 3,09, OR2AT4 2,98, OR1A1 2,97, OR10J5 2,86 —
et OR2B6, le seul OR qui monte avec KRAS ici, est à
2,80 (min 2,51, max 3,26), c'est-à-dire au niveau du
bruit de fond de la puce (les valeurs vont de 2,08 à
14,45, médiane 4,71). Une expression mesurée n'est PAS
une preuve de fonction olfactive ; un OR présent à
expression quasi nulle n'est PAS une preuve d'olfaction.
Aucun composé volatil n'est mesuré dans ce chantier
(pas de volatilome détenu).

**Tests directs (harnais, hors pipeline ; `direct_tests_866.csv`,
SHA `148a389f…30daf`, 162 lignes ; d de Cohen, + = plus haut
chez les 12 dernières lignes ; rho de Spearman contre le rang
de contrôle ; mêmes indices sur le nul).** Seuil de Bonferroni
sur les 162 rho : 0,05/162 ≈ 0,00031. Les p sont nominales,
bilatérales, sauf mention.

- G5 / KRAS — CONFIRME, le plus fort du chantier : KRT19
  rho +0,577 (p = 7,7e-12), KRT7 +0,420 (p = 2,3e-06),
  INSM1 −0,350 (p = 0,00010), NEUROD1 −0,341
  (p = 0,00016), CHGA −0,338 (p = 0,00019), CHGB −0,266
  (p = 0,0036) — tous au-delà du nul (max |rho| du nul :
  0,165) et tous sauf CHGB sous le seuil de Bonferroni.
  D1 : CHGA −1,33, NEUROD1 −1,12, INSM1 −0,89, KRT7
  +0,74, KRT19 +0,73 (nuls entre −0,45 et +0,06). SYP est
  plat (rho −0,131, p = 0,16 ; D1 −0,47) — comme en
  GSE71729 (rho −0,086) : la confirmation porte sur le
  programme (CHGA/INSM1/NEUROD1 chutent, KRT7/KRT19
  montent), pas sur chaque gène. VIL1 monte (+0,257,
  p = 0,0050), CDX1/CDX2 plats.
- G5 / stade — NON CONFIRME, plat : rho max 0,102 (APOB),
  SYP +0,025, CHGB −0,037, CHGA −0,091, INSM1 −0,061,
  NEUROD1 −0,096, KRT7 −0,095, KRT19 −0,061 ; nul max
  |rho| 0,172. D1 : CHGA −0,89, NEUROD1 −0,83, INSM1
  −0,72, KRT7 −0,71 — mais les nuls atteignent +0,78
  (CHGB) et +0,46 (NEUROD1) sur les mêmes contrastes :
  dans l'enveloppe du nul. Contrairement à TCGA
  (SYP −0,276, CHGB −0,250) et à GSE62452 (NEUROD1
  −0,416, CHGA −0,348), le programme neuroendocrine ne
  baisse pas avec le stade ici.
- G1 / KRAS — CONFIRME : MUC13 rho +0,422 (p = 1,9e-06),
  AGR2 +0,414 (p = 3,2e-06), SPDEF +0,357 (p = 7,1e-05),
  TFF2 +0,323 (p = 0,00035), MUC4 +0,264 (p = 0,0039),
  TFF1 +0,246, TFF3 +0,252 ; nul max |rho| 0,161. D1 :
  SPDEF +0,71, MUC13 +0,70, AGR2 +0,62, MUC4 +0,45
  (nuls −0,44 à +0,21). AGR2 monte dans les trois cohortes
  chiffrées (TCGA +0,328, GSE71729 +0,383, GSE62165 +0,414 ;
  GSE62452 non chiffrée au §8.58) ; MUC4 monte en TCGA (+0,313) et
  ici (+0,264), plat en GSE71729 (−0,083). MUC6 est plat
  (−0,005) : ni chute comme en GSE71729 (−0,436), ni
  plat-haut comme en TCGA (+0,035). MUC5B +0,147 (p 0,11).
- G1 / stade — NON CONFIRME, sens inverse de TCGA :
  MUC4 rho −0,238 (p = 0,0095), MUC5B −0,182 (p = 0,048),
  TFF2 −0,152, AGR2 −0,137, TFF1 −0,115, TFF3 −0,119 ;
  nul max |rho| 0,208. D1 : TFF1 −0,96, TFF2 −0,81,
  TFF3 −0,79 — mais le contraste top-12 oppose 12 des
  13 tumeurs de stade IV au reste, et les nuls
  atteignent +0,44 (TFF2) et +0,42 (TFF3) : un d à
  n = 13 bouge de ~0,5 quand une seule tumeur change.
  En TCGA, TFF1 montait avec le stade (rho +0,204) et
  AGR2 aussi (+0,208) : ici les deux descendent. Le
  mucus ne monte pas avec le stade dans cette cohorte.
- G4 / KRAS — PARTIEL : AOX1 rho −0,382 (p = 2,0e-05),
  FMO1 −0,421 (p = 2,1e-06), ADH1B −0,372
  (p = 3,4e-05), ALDH3B1 +0,356 (p = 7,4e-05),
  ALDH3A1 +0,343 (p = 0,00014), ADH1A −0,249
  (p = 0,0065) — tous au-delà du nul (max |rho| 0,174)
  et tous sauf ADH1A sous le seuil de Bonferroni. D1 :
  FMO1 −1,12, ALDH3B1 +0,96, AOX1 −0,90, ADH1B −0,81
  (nuls −0,39 à +0,36). AOX1 chute dans les quatre
  cohortes (−0,289 / −0,253 / −0,611 / −0,382) ;
  ALDH3B1 monte en TCGA (+0,303) et ici (+0,356) ;
  ALDH3A1 monte en GSE71729 (+0,367) et ici (+0,343).
  Mais UGT1A1 est ABSENT : le critère gelé Q4
  (AOX1 chute ET UGT1A1 monte) ne peut pas être rempli
  — PARTIEL, pas CONFIRME. NOS1 est plat (−0,097,
  p = 0,30 ; D1 +0,01) alors qu'il chutait dans les deux
  cohortes GEO (−0,369 / −0,529) : sa chute n'est pas
  universelle. FMO1, plat en TCGA, est ici la plus forte
  chute du groupe : une piste par gène, pas un programme.
- G4 / stade — rien (rho max 0,177, ADH4 ; nul max
  0,179) — comme dans TCGA et GSE62452.
- G3 / KRAS — NON CONFIRME : OR2B6 rho +0,293
  (p = 0,0013 ; D1 +0,51, nul −0,09) MONTE — premier OR
  qui monte significativement dans une cohorte de
  confirmation, au-delà du nul (max |rho| 0,144), mais
  sans passer Bonferroni (0,0013 > 0,00031) et sur un
  transcrit au niveau du bruit de fond (médiane 2,80).
  Aucun OR ne chute significativement : chute max
  OR2T10 −0,131 (p = 0,16), OR52N4 −0,111, OR7A5
  −0,100, OR13A1 −0,076 (p = 0,41), OR2C1 −0,018 —
  contre OR13A1 −0,423 et OR2T10 −0,418 en GSE62452,
  OR2W3 −0,338 en GSE71729. OR2A4, le seul OR montant
  de TCGA (+0,259), est ABSENT ici (troisième cohorte
  de confirmation où il est absent) ; OR2W3 et OR2A7
  sont absents aussi. Le bilan des odeurs n'est donc
  plus « plusieurs OR chutent, aucun ne monte » : dans
  cette cohorte, un OR monte et aucun ne chute.
  En GSE71729, OR2B6 chutait (−0,220) : il change de
  sens entre cohortes.
- G3 / stade — rien : rho max 0,163 (OR2L13, p 0,078),
  nul max 0,174 — dans l'enveloppe du nul.
- G2 / KRAS — chute faible : CPA3 rho −0,218
  (p = 0,018), CPA2 −0,154, CPB1 −0,145, CEL −0,133,
  CELA2A −0,127, CTRB2 −0,127 ; nul max 0,147. D1 :
  CEL −0,53, CPB1 −0,52, CPA2 −0,53, CTRB2 −0,50 —
  mais les nuls atteignent +0,54 (CELA2A) et +0,50
  (PNLIPRP1) : dans l'enveloppe. Comme dans TCGA et
  GSE62452, c'est la perte acineuse, pas un nouveau
  signal — et ici elle est affaiblie parce que 3 gènes
  du score acineux (CTRB1, CELA3B) et les amylases
  sont absents de la puce.
- G2 / stade — rien (rho max 0,150, CPA3 ; nul max
  0,278).

**Verdicts par question (critères gelés, protocole §7).**
- Q1 (G1/stade) : NON CONFIRME — aucun gène G1 ne monte
  avec le stade ; TFF1 et AGR2 descendent (sens inverse
  de TCGA).
- Q2 (G5/KRAS) : CONFIRME — ≥ 2 marqueurs
  neuroendocrines chutent sous Bonferroni (INSM1,
  NEUROD1, CHGA) et les deux kératines montent
  (KRT19, KRT7), au-delà du nul.
- Q3 (G3/KRAS) : NON CONFIRME — OR2B6 monte
  significativement (p = 0,0013) et aucun OR ne chute
  significativement ; OR2A4 absent.
- Q4 (G4/KRAS) : PARTIEL — AOX1 chute (4/4 cohortes),
  ALDH3B1/ALDH3A1 montent, mais UGT1A1 est absent :
  le critère « AOX1 chute ET UGT1A1 monte » n'est pas
  testable en entier.
- Q5 (G1/KRAS) : CONFIRME — AGR2 monte (p = 3,2e-06,
  sous Bonferroni), MUC4 aussi (p = 0,0039), au-delà
  du nul.
- Hors critères : G5/stade NON CONFIRME (plat) ;
  G4/stade rien ; G2 chute acineuse faible.

**Le pipeline (lot complet — 20/20 runs, exits 0/0).**
Lecture `extract_866.py` (`extract_866.json`,
`extract_866.csv`, 20 runs, 0 manquant) ; cascade en %
(T_-2 / T_-1 / T_0 / T_+1 / T_+2) ; MC = best_config
score (seuil entre parenthèses, en %) ; S_sep =
max_separation × stability ; Delta ; L7a (direction,
confiance) ; falsification ; L7b ; bruit (score moyen) ;
F1/F2 « Tous » (rapport après/avant, médiane sur 29
estimateurs). Aucun seuil de séparation n'était
pré-enregistré : les écarts sont des pistes, jamais des
preuves.

| Groupe / ordre | MC réel (seuil) | MC nul | ΔMC | S_sep réel | S_sep nul | ΔS_sep | Delta réel | Delta nul | L7a réel | fals réel | fals nul | L7b |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 / KRAS | 0,3560 (13,3 %) | 0,3863 | −0,030 | 0,3676 | 0,2144 | +0,153 | 2,048 | 1,870 | UP 0,325 | 0,238 | 0,235 | FRAGILE / FRAGILE |
| G1 / stade | 0,3432 (86,7 %) | 0,3288 | +0,014 | 0,2903 | 0,1859 | +0,104 | 2,018 | 2,040 | UP 0,167 | 0,274 | 0,222 | FRAGILE / FRAGILE |
| G2 / KRAS | 0,5078 (88,2 %) | 0,5231 | −0,015 | 0,1801 | 0,3086 | −0,129 | 1,859 | 1,249 | DOWN 0,335 | 0,070 | 0,161 | FRAGILE / FRAGILE |
| G2 / stade | 0,5378 (86,7 %) | 0,3392 | +0,199 | 0,2554 | 0,2524 | +0,003 | 1,945 | 2,003 | DOWN 0,180 | 0,242 | 0,196 | FRAGILE / FRAGILE |
| G3 / KRAS | 0,3291 (85,0 %) | 0,3281 | +0,001 | 0,1929 | 0,1896 | +0,003 | 2,036 | 1,942 | UP 0,325 | 0,260 | 0,281 | FRAGILE / FRAGILE |
| G3 / stade | 0,3336 (62,1 %) | 0,3384 | −0,005 | 0,2169 | 0,2494 | −0,033 | 1,584 | 2,031 | UP 0,320 | 0,749 | 0,333 | FRAGILE / FRAGILE |
| G4 / KRAS | 0,3508 (13,3 %) | 0,3341 | +0,017 | 0,3341 | 0,2218 | +0,112 | 2,023 | 1,990 | UP 0,269 | 0,225 | 0,247 | FRAGILE / FRAGILE |
| G4 / stade | 0,3283 (13,3 %) | 0,3336 | −0,005 | 0,1824 | 0,2205 | −0,038 | 2,035 | 1,993 | DOWN 0,191 | 0,292 | 0,229 | FRAGILE / FRAGILE |
| G5 / KRAS | 0,3584 (13,3 %) | 0,3293 | +0,029 | 0,3879 | 0,1926 | +0,195 | 2,010 | 1,990 | UP 0,302 | 0,172 | 0,261 | FRAGILE / FRAGILE |
| G5 / stade | 0,3304 (86,7 %) | 0,3339 | −0,004 | 0,1994 | 0,2188 | −0,019 | 1,991 | 1,984 | UP 0,147 | 0,183 | 0,217 | FRAGILE / FRAGILE |

Cascades : G5/KRAS réelle 1,7 / 83,5 / 86,6 / 95,3 / 100 %
(T_0 au pas 101) contre nul 0,0 / 2,8 / 5,8 / 14,9 / 22,6 %
— le plus grand contraste de cascade du lot, cohérent
avec les tests directs G5/KRAS, les plus forts du
chantier. G1/KRAS réelle 4,1 / 16,6 / 20,0 / 43,0 / 43,0 %
(T_0 au pas 23) contre nul 2,5 / 87,4 / 90,5 / 93,7 /
100 % ; G4/KRAS réelle 1,7 / 74,8 / 97,6 / 100 / 100 %
contre nul 0,0 / 81,9 / 85,0 / 88,2 / 90,5 % ; G2/stade
réelle 0,0 / 23,5 / 27,1 / 30,9 / 38,2 % (T_0 au pas 32,
MC 0,5378 au seuil 86,7 %) contre nul 1,7 / 65,2 / 86,6 /
89,8 / 89,8 % — cascade réelle basse malgré le MC le
plus haut du lot : le score vient d'un seuil tardif, pas
d'une rupture visible. Les cascades stade ont leur T_0
tôt ou figé (G4/stade réelle 0,0 / 5,8 / 97,6 / 100 /
100 %, T_0 au pas 114 ; G1/stade réelle 0,0 / 39,0 /
81,1 / 84,2 / 92,1 %) : avec 4 niveaux de stade et 92
tumeurs au stade II sur 118, un « seuil » tombe dans le
bloc des ties — il ne mesure rien, comme aux §8.45/§8.58.
Lecture d'ensemble : MC favorise le réel sur 4/10
seulement (+0,014 à +0,199 ; le plus grand écart,
G2/stade +0,199, tombe sur des tests directs plats) ;
S_sep favorise le réel sur 5/10 (les trois plus grands :
G5/KRAS +0,195, G1/KRAS +0,153, G4/KRAS +0,112 — les
trois groupes dont les tests directs confirment sous
KRAS) ; Delta favorise le réel sur 7/10 mais par de
petits écarts (sauf G2/KRAS +0,610 et G3/stade −0,447) ;
la falsification est partagée (réel devant sur 5/10) ;
L7a est UP partout dans le réel sauf G2 (DOWN) et
G4/stade (DOWN), et UP partout dans le nul sauf G2/KRAS
(DOWN), G4/stade (DOWN) et G5/KRAS (DOWN) ; L7b est
FRAGILE sur les 20 runs — même non-informativité que
dans TCGA et les confirmations GEO : FRAGILE partout,
réel comme nul. Delta vaut ~1,6–2,0 partout (contre
~3,8–4,2 en TCGA à n = 178, ~2,9 en GSE71729 à n = 145,
~1,4–1,5 en GSE62452 à n = 69) : l'échelle suit n,
cohérent avec §8.40/§8.62. Régime « criticality »
partout ; bruit « proxy de variance modéré » ou
« mixte » presque partout (scores 0,37–0,73).
F1/F2 « Tous » : les rapports après/avant s'effondrent
ou explosent sans direction cohérente (F1 ×0,017 à
×84,8 réel contre ×0,024 à ×114,7 nul ; F2 ×0,011 à
×152,4 réel contre ×0,022 à ×292,9 nul). Même figure
qu'aux §8.31/§8.32/§8.34/§8.36/§8.45/§8.58 : des pistes
dans le sens réel sur S_sep pour les groupes qui
confirment en direct, contredites ou non confirmées par
MC, Delta, la falsification et L7b — pas une séparation
démontrée. Le cas G2/stade est l'avertissement de ce
lot : le plus grand écart MC (+0,199) avec S_sep à
égalité (+0,003), Delta −0,058, et des tests directs
plats — un score seul ne fait pas un signal.

**Comparaison directe avec les trois cohortes du §8.58
(rho de Spearman, ordre KRAS sauf mention).**

| Lecture | TCGA (n=178) | GSE71729 (n=145) | GSE62452 (n=69) | GSE62165 (n=118) |
|---|---|---|---|---|
| G5/KRAS : SYP | −0,392 | −0,086 (plat) | −0,503 | −0,131 (plat) |
| G5/KRAS : INSM1 | −0,343 | −0,296 | −0,413 | −0,350 |
| G5/KRAS : CHGA | −0,212 | −0,359 | — | −0,338 |
| G5/KRAS : KRT19 | +0,333 | +0,281 | +0,416 | +0,577 |
| G5/KRAS : KRT7 | +0,308 | +0,278 | +0,398 | +0,420 |
| G5/stade : SYP | −0,276 | — | — | +0,025 (plat) |
| G5/stade : NEUROD1 | −0,210 | — | −0,416 | −0,096 (plat) |
| G1/KRAS : AGR2 | +0,328 | +0,383 | — | +0,414 |
| G1/KRAS : MUC4 | +0,313 | −0,083 (plat) | — | +0,264 |
| G1/KRAS : MUC6 | +0,035 (plat) | −0,436 | — | −0,005 (plat) |
| G1/stade : TFF1 | +0,204 | — | — | −0,115 (inverse) |
| G1/stade : AGR2 | +0,208 | — | — | −0,137 (inverse) |
| G4/KRAS : AOX1 | −0,289 | −0,253 | −0,611 | −0,382 |
| G4/KRAS : UGT1A1 | +0,378 | ABSENT | +0,541 | ABSENT |
| G4/KRAS : NOS1 | +0,067 (plat) | −0,369 | −0,529 | −0,097 (plat) |
| G4/KRAS : ALDH3B1 | +0,303 | — | — | +0,356 |
| G3/KRAS : OR2A4 | +0,259 | ABSENT | ABSENT | ABSENT |
| G3/KRAS : OR2W3 | — | −0,338 | — | ABSENT |
| G3/KRAS : OR13A1 | −0,152 | — | −0,423 | −0,076 (plat) |
| G3/KRAS : OR2T10 | −0,154 | — | −0,418 | −0,131 (plat) |
| G3/KRAS : OR2B6 | — | −0,220 | — | +0,293 (MONTE) |

(« — » : valeur non rapportée au §8.58 pour cette
cohorte ; « ABSENT » : gène absent de la matrice, noté
tel quel, jamais remplacé. Les valeurs GSE62452 G1/KRAS
et G1/stade ne sont pas chiffrées au §8.58 : elles ne
sont pas inventées ici.)

Bilan à quatre cohortes : G5/KRAS est le seul signal
cohérent partout (4/4 cohortes, dans les deux sens :
marqueurs neuroendocrines chutent, kératines montent) —
avec SYP plat dans deux cohortes sur quatre, la
confirmation porte sur le programme, pas sur chaque
gène. G1/KRAS tient pour AGR2 (3/3 cohortes chiffrées :
TCGA +0,328, GSE71729 +0,383, GSE62165 +0,414 ;
GSE62452 non chiffrée au §8.58) et MUC4
(2/3 cohortes testables). G4/KRAS tient pour AOX1
(4/4 cohortes, toujours en chute) et ALDH3B1 (2/2
cohortes testables) ; UGT1A1 n'est testable que dans
2 cohortes sur 4 ; NOS1 chute dans 2 cohortes sur 4
et est plat dans les deux autres. G1/stade et G5/stade
ne tiennent que dans TCGA (et G5/stade dans GSE62452)
: ils ne tiennent pas dans GSE62165 — les lectures
« stade » du §8.58 sont les plus fragiles du chantier,
et la structure du stade ici (92/118 au stade II)
les affaiblit encore. G3/KRAS ne tient plus comme
« chute sans montée » : dans cette cohorte, un OR
monte (OR2B6, près du bruit de fond) et aucun ne chute
significativement ; OR2A4 reste non confirmable
ailleurs (absent des trois cohortes de confirmation).

**Réserve de méthode — à lire avec le verdict.** Les flux
sont ici des valeurs de puce brutes (variante (a) du
§8.58, sans correction de pureté) : ils mesurent
l'expression telle que déposée, sans retrait de la
composante tissu normal acineux/îlots — contrairement
à TCGA, où les flux sont des résidus après régression.
G2 est biaisé par construction (8/20 flux retenus sont
des gènes du score acineux) et affaibli ici par
l'absence de 6 gènes dont 2 du score acineux : ses
lectures sous KRAS sont rapportées avec cette réserve
et ne sont pas lues comme « nouvelles ». Le stade est
une variable clinique (AJCC), pas une mesure du
système : 4 niveaux, ties massives (II 92/118, soit
78 %), ordre intra-stade arbitraire (GSM
lexicographique), sommet mince (III + IV = 18 tumeurs)
— mêmes limites qu'aux §8.45/§8.58, aggravées ici par
la domination du stade II. Les OR sont mesurés comme
transcrits, près du bruit de fond de la puce (médiane
des médianes 2,99 en log2) : aucune odeur, aucun
ligand, aucun test fonctionnel dans ce chantier. Les p
sont nominales ; seul le seuil de Bonferroni
0,05/162 ≈ 0,00031 protège contre les 162 tests
directs — les rho G5/KRAS (KRT19, KRT7, INSM1,
NEUROD1, CHGA), G1/KRAS (MUC13, AGR2, SPDEF) et
G4/KRAS (FMO1, AOX1, ADH1B, ALDH3B1, ALDH3A1) le
passent ; OR2B6 (+0,293, p = 0,0013) ne le passe pas
et reste une piste. Ne jamais exiger de consensus
entre flux ou contrôles : les groupes ne bougent pas
ensemble — G1 monte quand G5 descend sous KRAS, et
c'est l'information. Le mapping (chaîne Bioconductor,
sonde → Entrez 2015 → symbole courant) est documenté
dans `PROVENANCE_866.md` avec ses limites ; un symbole
renommé depuis 2015 apparaît sous son nom actuel.

**Ce que ça change.** Trois choses neuves, toutes
mesurées aujourd'hui, aucune importée : (1) le
programme neuroendocrine qui s'efface quand KRAS monte
tient dans une quatrième cohorte, et c'est la plus
forte (KRT19 +0,577, p = 7,7e-12) — c'est désormais
le signal le plus solide du chantier, 4/4 cohortes ;
(2) le mucus étendu qui monte avec le stade ne tient
pas ici — il descend — et le neuroendocrine ne baisse
pas avec le stade ici non plus : les deux lectures
« stade » du §8.58 sont fragiles, et la domination du
stade II (78 %) dans cette cohorte en est une cause
plausible, pas une preuve ; (3) les odeurs perdent
leur bilan « chute sans montée » : un OR monte
(OR2B6) et aucun ne chute significativement dans
cette cohorte, sur des transcrits proches du bruit de
fond — la piste « odeurs » reste une piste par gène,
pas un programme, et OR2A4 reste non confirmable
ailleurs (absent des trois cohortes de confirmation).
Le volatil (G4) reste partiel : AOX1 chute partout
(4/4), mais UGT1A1 n'est testable que dans 2 cohortes
sur 4 et NOS1 chute dans 2 sur 4. Le pipeline, dans
cette quatrième cohorte comme dans les trois
premières, donne de petits écarts favorables au réel
sur S_sep pour les groupes qui confirment en direct
(G5/KRAS +0,195, G1/KRAS +0,153, G4/KRAS +0,112),
mais MC ne favorise le réel que sur 4/10 paires et
L7b est FRAGILE 20/20 : il ne sépare pas nettement du
nul — le même verdict, tenu sur quatre cohortes.
Prochaines étapes : intégration au livre blanc et
publication (PDF + GitHub) sur go de Zackary ; rien
n'a été poussé, rien n'a été régénéré dans ce chantier.
