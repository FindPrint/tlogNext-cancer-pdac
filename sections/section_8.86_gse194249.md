# §8.86 — GSE194249, ré-audit : INUTILISABLE comme 14e paire — DPCR1 absent de la matrice FPKM déposée (0/15 609)

## Verdict d'abord

**INUTILISABLE — la candidate C4, GSE194249 (84 PDPCOs, Shi et al., Nat.
Commun. 2022), ne peut pas devenir la quatorzième paire principale
indépendante : DPCR1 est absent de la matrice FPKM déposée
(0 occurrence dans tout le fichier, 0/15 609 lignes de gènes, vérifié
par deux chemins indépendants), donc la porte gelée « 12 gènes v4
présents » dit ARRÊT (§3 du protocole) — aucun CSV de flux, aucun run
v6.2, aucun `d_maxsep`. A2 reste 9/13 au-dessus du plancher, 11/13
positifs, LOO 8/12. La condition C3 du §8.59.8, levée au §8.71,
RESTE LEVÉE (ce chantier ne rouvre rien). La piste GSE194249 comme
paire à 12 flux est FERMÉE.**

| Porte (protocole gelé §5) | Exigé | Mesuré 21 nov. 2026 | Sort |
|---|---|---|---|
| Fichier FPKM téléchargé, gzip intègre | oui | 4 927 876 o, SHA `479517fb…27`, gzip intègre | **PASSE** |
| Mise en page (A) ou (B) | (A) ou (B) | **(A)** : col1 = `GeneSymbol`, 88 colonnes | **PASSE** |
| n PDPCO ≥ 40 (après exclusion des normaux) | ≥ 40 | **84 PDPCOs** (87 colonnes − 3 `NPC-*`) | **PASSE** |
| Aucun code TCGA, aucune cohorte déjà tenue | aucun | Titres `CAS-*` / `NPC-*` uniquement, 0 inattendu | **PASSE** |
| KRAS présent (symbole exact) | oui | **1 ligne** | **PASSE** |
| **12 gènes v4 présents** | **12/12** | **11/12 — DPCR1 absent (0/15 609)** | **ARRÊT (§3)** |
| Cas complets ≥ 40 | ≥ 40 | Non atteint (arrêt avant construction) | — |
| Runs v6.2 réel + nul | 2 runs exit 0 | **0 run lancé** | — |
| `d_maxsep` | > 0,07 pour CONFIRME | **Aucune valeur — pas de paire** | — |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que le ré-audit
demandé par le §8.78 est fait, depuis GEO, avec un protocole gelé avant
tout téléchargement — et que la série échoue à la même porte que la
candidate C2 au §8.79 (DPCR1 absent), mais pour une raison différente
(voir §8.86.2) : ici le gène n'est dans le fichier déposé sous aucun
symbole, pas même MUCL3. Il dit que tout le reste passait : n = 84
PDPCOs confirmés, 87 colonnes conformes aux métadonnées GEO, 12 des
13 gènes utiles présents une fois chacun, 0 symbole dupliqué. Il ne dit
pas que `maxsep` échoue sur cette cohorte : **aucune valeur `maxsep`
n'existe pour GSE194249, et aucune ne doit être citée** — il n'y a pas
eu de paire, donc pas de verdict de séparation, ni positif ni négatif.
Il ne dit pas que la série est sans valeur : ses données (expression,
ATAC, réponse aux médicaments) restent une ressource, mais pas une
paire v6.2 à 12 flux sous ce protocole. Il ne dit rien de clinique.

**Fragilité, dite en tête.** Le verdict tient à un seul gène absent
d'un seul fichier déposé — comme au §8.79 pour la candidate C2. C'est
un verdict de construction, pas une mesure : il ne porte ni sur
l'instrument ni sur la biologie des organoïdes, seulement sur la
compatibilité entre la matrice déposée et la liste v4 gelée. Toute
lecture future qui présenterait GSE194249 comme « testée et négative »
serait fausse : elle n'a pas été testée, elle a été arrêtée à la porte.

## 8.86.1 — Le ré-audit : ce qui était attendu, ce qui est mesuré

### Ce que le §8.78 demandait

La candidate C4 attendait son re-audit depuis GEO : n de réponse exact,
couverture v4 — l'audit scripté existait
(`audit_GSE194249_candidate.py`, SHA `ae3c85cd…`) mais sa sortie
(`candidate_GSE194249_sources/`, avec `CANDIDATE_DATA_AUDIT.json/.md`)
était absente du dépôt `universal-log-research`. Le protocole
`PROTOCOL_gse194249_886.md` (SHA `b620238b…1cf`) a été gelé avant tout
téléchargement, comme l'exige la règle du projet ; le présent chantier
EST cet audit refait.

### Ce qui est confirmé (tout passait, sauf une porte)

- **Source :** `GSE194249_PDPCOs_FPKM.txt.gz`, URL GEO FTP
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194249/suppl/GSE194249_PDPCOs_FPKM.txt.gz`
  (miroir HTTPS, 1re tentative, 21 nov. 2026). Fichier local
  `data/GSE194249_PDPCOs_FPKM.txt.gz`, 4 927 876 o, SHA-256
  `479517fbed1d8f5bb9d141b6b932b6ab56ba2ba72d4394d13aea2a3da0a50f27`,
  gzip intègre. (GEO ne publie pas de SHA pour ce fichier : la
  vérification est l'intégrité gzip + les comptages ci-dessous.)
- **Mise en page (A) :** première colonne `GeneSymbol`, 88 colonnes
  au total, 15 610 lignes (en-tête + 15 609 lignes de gènes).
  En-tête : `GeneSymbol, CAS-DAC-1, CAS-IPMN-1, CAS-DAC-11, …`,
  dernière colonne `NPC-7`.
- **Colonnes :** les 87 titres correspondent EXACTEMENT aux
  87 échantillons des métadonnées NCBI E-utilities
  (`gse194249_esummary_886.json`, SHA `73934e46…0e`) — 0 titre
  inattendu, 0 titre manquant. Composition : 75 `CAS-DAC-*`
  (PDAC), 4 `CAS-NEN-*`, 4 `CAS-IPMN-*`, 1 `CAS-ACC-1`, 3 `NPC-*`
  (normaux). Soit **84 PDPCOs** + 3 normaux, conforme à l'article
  (75 PDAC, 4 IPMN, 1 ACC, 4 NEN ; 6 NPOs établis, dont 3 dans GEO).
- **Symboles dupliqués : 0 ligne.** Gènes uniques après agrégation
  (règle gelée, médiane — sans objet ici) : 15 609.
- **Normaux :** `NPC-4`, `NPC-5`, `NPC-7` — 3 colonnes à exclure
  selon le protocole (exclusion non exécutée : l'arrêt a eu lieu
  avant toute construction ; le nombre retenu aurait été 84).
- **Indépendance :** établie par programme avant le gel (biobanque
  PDPCO de Shanghai, Changhai Hospital, Second Military Medical
  University ; identifiants `CAS-*` / `NPC-*` disjoints des
  cohortes tenues ; aucun lien documenté avec TCGA PAAD, ICGC
  PACA-AU, les séries GEO tenues, les organoïdes GDC HCMI, les
  PDO de Chen et al. 2025, ni Tiriac et al. 2018). Caveat déclaré
  dans le protocole comme au §8.79 : le non-recouvrement est
  établi par programme et système d'identifiants, pas par
  jointure — c'est une limite, pas une preuve formelle.
  L'indépendance ne change rien au verdict : la cohorte est
  indépendante **et** inutilisable — les deux constats sont séparés.

### La porte qui échoue : DPCR1 absent

| Gène | Lignes exactes | Gène | Lignes exactes |
|---|---|---|---|
| PGC | 1 | CR2 | 1 |
| REG4 | 1 | KRT20 | 1 |
| CLDN18 | 1 | MUC2 | 1 |
| MUC17 | 1 | GSTM1 | 1 |
| **DPCR1** | **0** | CEACAM5 | 1 |
| CLCA1 | 1 | MUC16 | 1 |
| KRAS (contrôle) | 1 | MUCL3 (descriptif) | 0 |

- **11/12 gènes v4 + KRAS, une ligne chacun, 0 doublon.** Seul
  DPCR1 manque.
- **Second calcul indépendant (grep sur le fichier brut) :**
  `DPCR1` exact : 0 occurrence dans tout le fichier ;
  insensible à la casse : 0 ; `MUCL3` : 0 ; aucun symbole
  contenant `DPCR`. Les deux chemins (pandas, script
  `build_fluxes_886.py` ; grep brut) donnent 0.
- Symboles `MUC*` présents : MUC1, MUC12, MUC13, MUC16, MUC17,
  MUC2, MUC20, MUC3A, MUC4, MUC5B, MUC6, MUC7 — MUC16 et MUC17
  (deux des trois mucines v4) sont là ; DPCR1, la troisième
  entité de type mucine de la liste, ne l'est pas.
- Le script `build_fluxes_886.py` (SHA `04965dd4…52`) s'est
  arrêté à la porte « 12 gènes v4 présents » avec
  `ARRÊT (§3) : gènes absents ['DPCR1']` ; l'audit
  `build_fluxes_886_audit.json` (SHA `60eeb3c7…0a`) consigne
  l'état exact. **Aucun CSV de flux, aucun run, aucun manifeste,
  aucun journal de lot, aucun extracteur, aucun test direct** —
  confirmé par l'absence des fichiers `pdac_886_*`,
  `results_fast_v62_886_*`, `manifest_v62_886.txt`,
  `runs_v62_886.log`, `extract_886.*`, `verify_886.py`,
  `direct_tests_886.py` (21 nov. 2026).
- Pipeline v6.2 revérifié après travaux, inchangé : SHA
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.

## 8.86.2 — Pourquoi DPCR1 est absent : ce qui est établi, ce qui reste hypothèse

### Ce qui est établi

- Le gène n'est pas dans le fichier déposé sous **aucun** des deux
  symboles connus : DPCR1 : 0 ; MUCL3 (symbole actuel, HGNC:21666,
  `prev_symbol` DPCR1 — établi au §8.79) : 0.
- Ce n'est donc **pas** la même histoire que la candidate C2 au
  §8.79 : là, MUCL3 était présent dans 55/55 fichiers GENCODE v36
  (symbole retiré, gène mesuré sous son nouveau nom) ; ici, le gène
  n'est mesuré sous aucun nom dans la matrice déposée.
- La matrice déposée est un sous-ensemble filtré, pas une
  annotation complète : 15 609 lignes de gènes, contre ~60 000
  pour un GENCODE complet.

### Ce qui est compatible, sans être prouvé

- Les Méthodes de l'article (Shi et al., p. 12) décrivent le
  filtre appliqué avant analyse : lectures mappées sur hg19 par
  TopHat, FPKM par Cufflinks, puis « Genes with FPKM values <1
  in all 87 samples were filtered out. Finally, 15,819
  protein-coding genes remained for further analysis. » Il est
  compatible avec ce filtre que DPCR1/MUCL3 ait eu FPKM < 1 dans
  les 87 échantillons (ou n'ait pas été annoté comme protéique
  dans le pipeline hg19/Cufflinks des auteurs) et ait donc été
  exclu du dépôt. Mais les valeurs FPKM par gène de DPCR1/MUCL3
  ne sont pas dans le fichier déposé : **le filtre ne peut pas
  être vérifié gène par gène**. L'absence est un fait du fichier
  déposé ; sa cause exacte reste une hypothèse.
- **Écart 15 609 / 15 819 :** les Méthodes annoncent 15 819 gènes
  protéiques restants après filtre ; la matrice déposée en compte
  15 609 — écart de 210 gènes, non élucidé (version du dépôt,
  annotation, ou autre — non tranché ici). Cet écart est consigné
  tel quel ; il ne change pas la porte (DPCR1 est absent des
  15 609 lignes déposées, quel que soit le décompte attendu).

### Ce qui n'a pas été fait (règle gelée §4.4)

- **Aucun remappage** : ni DPCR1 → MUCL3 (absent de toute façon),
  ni aucun autre alias, ni reconstruction depuis les lectures
  brutes (SRA). Changer la porte après l'avoir vue échouer
  serait un changement de protocole sans go — comme pour C2
  au §8.79.
- **Aucune paire à 11 flux** : le §8.79 avait pu courir GSE57495
  à 11 flux parce qu'un addendum de protocole avait été gelé
  AVANT toute construction de la cohorte #2, avec son caveat
  écrit. Ici, le §3 du protocole gelé interdit toute cohorte
  #2 dans ce chantier. Une paire à 11 flux sur GSE194249
  exigerait son propre protocole gelé et un go — elle est
  nommée comme piste future au §8.86.4, pas courue ici.

## 8.86.3 — A2 inchangé, et ce que l'arrêt ne dit pas

Table des 13 paires principales indépendantes comptées (valeurs
des §8.56 / §8.69 / §8.70 / §8.71 / §8.74 / §8.79 reprises telles
quelles, jamais recalculées). GSE194249 n'y figure PAS — il n'y a
pas de paire.

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
| GSE57495 (§8.79, 11 flux) | 0,6381 / 0,1887 | **+0,4494** | oui | oui |

Bilan : **9/13 au-dessus du plancher, 11/13 positifs, LOO 8/12 —
INCHANGÉ.** C3 du §8.59.8 RESTE LEVÉE. Les nuls frais (graines
8861, 8862, gelées dans le protocole) ne sont pas courus : la
règle ne les déclenche que sur un `d_maxsep` mesuré proche du
plancher, et il n'y a pas de `d_maxsep` mesuré ici.

L'arrêt ne dit rien sur `maxsep`, sur l'instrument, ni sur la
biologie des PDPCOs. Il dit seulement : la matrice FPKM déposée
par Shi et al. ne contient pas DPCR1, et la liste v4 gelée
l'exige. Deux leçons de provenance, dans la lignée du §8.79 :
(1) un symbole de gène n'est pas un invariant — et ici, même le
symbole actuel ne sauve pas le flux, parce que le gène est absent
du fichier déposé sous tout nom ; (2) une matrice déposée filtrée
(FPKM < 1) peut perdre un flux de la v4 par simple filtrage
d'expression, sans qu'aucun renommage soit en cause.

## 8.86.4 — Pistes ouvertes

| Pistes ouvertes | Oui, une de moins | (a) La confirmation indépendante C3 est close depuis le §8.71 et la quatorzième paire n'a pas eu lieu — l'adoption pleine de `maxsep` (décision de Zackary, 20 nov. 13h04) ne dépend pas de cette piste ; (b) la candidate C1 (Chen et al. 2025, 46 PDO × 63 AUC, supplément MOESM13 SHA vérifié `0e009cd5…`) reste la piste suivante pour un lot drogue v6.2 (cible Gemcitabine, 62 contrôles) — elle ne peut pas devenir une paire A2 ; (c) la candidate C2 (GDC ORGANOID-PANCREATIC) reste utilisable sous un protocole futur qui pré-enregistrerait MUCL3 à la place de DPCR1 — les 55 TSV vérifiés sont détenus ; (d) **GSE194249, piste fermée comme paire à 12 flux** — deux suites possibles, chacune sous son propre protocole gelé et avec un go, jamais dans ce chantier : (d1) une paire à **11 flux** (sans DPCR1), comme la C3 du §8.79, avec son caveat écrit ; (d2) une re-dérivation de l'expression depuis les lectures brutes (SRA) avec une annotation actuelle, qui serait un autre produit de données, pas la matrice déposée ; (e) la réponse aux médicaments de GSE194249 (Suppl. Data 8, MOESM11) et le suivi clinique (Suppl. Data 10, MOESM13) n'ont pas été téléchargés : le n de réponse exact reste non vérifié, comme au §8.78 — une piste drogue sur ces 84 PDPCOs reste possible, sous son propre protocole ; (f) la fragilité du nul à petit n (§8.70, §8.53) reste un chantier propre ouvert — sans objet ici (aucun nul couru). |

## 8.86.5 — Annexe : provenance condensée et SHAs

- **Série :** GSE194249, Shi et al., Nat. Commun. 2022, 13:2169,
  DOI 10.1038/s41467-022-29857-6. GEO
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE194249
  (page directe bloquée par reCAPTCHA le 21 nov. 2026 ;
  métadonnées via E-utilities, réponse conservée
  `gse194249_esummary_886.json`, SHA
  `73934e46a717a5db1ed8cd8e1c4349435683a0eed1dda85fe7b097ec448f460e`).
  Plateforme GPL31265, dépôt 2022/02/23, *Homo sapiens*.
- **Fichier :** `data/GSE194249_PDPCOs_FPKM.txt.gz`, 4 927 876 o,
  SHA `479517fbed1d8f5bb9d141b6b932b6ab56ba2ba72d4394d13aea2a3da0a50f27`,
  gzip intègre ; 15 610 lignes, 88 colonnes ; mise en page (A).
  URL : `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194249/suppl/GSE194249_PDPCOs_FPKM.txt.gz`.
  Reçu `download_gse194249_886_receipt.json`, SHA
  `fd9bd625a3869086d06b11bb4896b5e5de7f05da91bf5867bca8d1bf83a016ea`.
- **Comptages vérifiés deux fois :** 87 colonnes = 84 PDPCOs
  + 3 `NPC-*` ; 15 609 lignes de gènes ; 0 symbole dupliqué ;
  12/13 gènes utiles présents une fois chacun ; **DPCR1 : 0
  occurrence (exact, insensible à la casse, fichier entier) ;
  MUCL3 : 0.**
- **Méthodes (article, p. 12) :** TopHat sur hg19, FPKM par
  Cufflinks, filtre FPKM < 1 dans les 87 échantillons, 15 819
  gènes protéiques annoncés — contre 15 609 déposés (écart 210,
  non élucidé).
- **Pipeline :** v6.2, SHA
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
  vérifié avant et après les travaux, inchangé ; **0 run lancé**.
- **Protocole gelé :** `PROTOCOL_gse194249_886.md`, SHA
  `b620238b9b5087c0167b975747b39cd0eb89dce9d5f99e169d58359887c9b1cf`.
- **Provenance complète :** `PROVENANCE_886.md`.
- **Scripts :** `download_gse194249_886.py` (SHA
  `d0e1be23…c1`), `build_fluxes_886.py` (SHA `04965dd4…52`,
  arrêt à la porte DPCR1), audit `build_fluxes_886_audit.json`
  (SHA `60eeb3c7…0a`).
- **Verdict :** INUTILISABLE comme 14e paire (DPCR1 absent).
  A2 : **9/13, 11/13 positifs, LOO 8/12 — INCHANGÉ.** C3 reste levée.
  Piste fermée comme paire à 12 flux.

— Fin de la §8.86. —
