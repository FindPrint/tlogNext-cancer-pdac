# §8.91 — GSE194249 : re-dérivation depuis les lectures brutes (SRA) — PISTE FERMÉE, lectures non accessibles en libre accès (21 novembre 2026)

**Projet :** PDAC — livre blanc v6.2
**Section :** §8.91 (la §8.86 est le ré-audit à 12 flux, la §8.88 la
paire à 11 flux)
**Date :** 21 novembre 2026, ~11h10–11h30 EST
**Go de Zackary :** 21 novembre 2026, 11h09
**Protocole gelé :** `PROTOCOL_gse194249_sra_891.md` (gelé AVANT
toute tentative de téléchargement et tout run)
**Provenance :** `PROVENANCE_891.md`
**Statut :** vérification d'accès — aucune donnée nouvelle mesurée
ici ; tous les faits ci-dessous sont des métadonnées publiques
d'accès aux données.

---

## Verdict

**PISTE FERMÉE : la re-dérivation de GSE194249 depuis les lectures
brutes est impossible — il n'existe aucune lecture brute en libre
accès.** SRA : 0 expérience pour les deux BioProjects de l'étude
(PRJNA799993 et PRJNA801501). ENA : 0 run. La fiche BioProject
PRJNA799993 le dit elle-même : « Raw data are not available for
this Series due to human genetic resources policy in China. » Les
lectures existent, mais seulement sous accès contrôlé, dans le dépôt
national chinois NODE (accession OEP001744), et aucune demande
d'accès n'a été faite — ce serait un geste administratif et
juridique, pas un calcul, et il n'a pas de go. **0 téléchargement,
0 CSV de flux, 0 run v6.2.** La question « DPCR1 et MUCL3
sont-ils quantifiables depuis les lectures brutes ? » reste sans
réponse. **A2 inchangé : 10/15 au-dessus du plancher, 12/15
positifs, LOO 9/14. C3 reste levée.**

---

## 0. Rappel — pourquoi cette piste existait

- §8.86 : GSE194249 **INUTILISABLE comme paire à 12 flux** —
  DPCR1 absent de la matrice FPKM déposée (0/15 609 lignes),
  MUCL3 également absent, 0 run, 0 CSV. La porte gelée « 12 gènes
  v4 présents » avait dit ARRÊT.
- §8.88 : la suite (d1), paire à 11 flux sans DPCR1, est faite —
  **NON** (`d_maxsep −0,0239`, le nul graine 42 sépare plus que le
  réel) ; A2 10/15, 12/15 positifs, LOO 9/14.
- §8.86.4 (d2) nommait la seconde suite : « une re-dérivation de
  l'expression depuis les lectures brutes (SRA) avec une annotation
  actuelle, qui serait un autre produit de données, pas la matrice
  déposée ». **Le présent chantier EST cette suite (d2).** Son seul
  objet : dire si une matrice à 12 flux peut être re-dérivée, et si
  oui la construire et la courir.

## 1. Ce qui a été vérifié — cinq contrôles d'accès, tous négatifs

| # | Contrôle | Source | Résultat |
|---|---|---|---|
| 1 | SRA, BioProject transcriptome | E-utilities `esearch db=sra term=PRJNA799993` | **count 0** — aucune expérience |
| 2 | SRA, BioProject second volet | E-utilities `esearch db=sra term=PRJNA801501` | **count 0** — aucune expérience |
| 3 | Lien GEO → SRA | E-utilities `elink dbfrom=gds db=sra id=200194249` | **aucun lien** |
| 4 | SRA, par accession GEO | E-utilities `esearch db=sra term=GSE194249` | **count 0** |
| 5 | ENA (miroir européen) | Portail ENA `result=read_run`, `study_accession=PRJNA799993` | **liste vide `[]`** — 0 run |

Chaque contrôle est conservé en reçu horodaté avec son SHA-256
(voir `PROVENANCE_891.md`) : `sra_esearch_PRJNA799993_891.json`
(SHA `a6df6133…18155`), `sra_esearch_PRJNA801501_891.json` (SHA
`014a217c…b7c2`), `elink_gds_sra_891.json` (SHA `e7498743…2f87c5`),
`ena_readrun_PRJNA799993_891.json` (SHA `2ba33ca0…01d6d`).

## 2. Pourquoi il n'y a rien à télécharger — les fiches BioProject le disent

### 2.1 PRJNA799993 (transcriptome) : données brutes indisponibles

Fiche BioProject PRJNA799993 (E-utilities esummary, reçue
`gse194249_bioproject_891.json`, SHA `e5a85000…0e455`), citée
verbatim :

> « Raw data are not available for this Series due to human
> genetic resources policy in China. »

La même fiche confirme le protocole RNA-seq de l'article (ARN
total de 84 PDPCOs + 3 NPOs, kit NEBNext Ultra, paires
d'extrémités, Illumina HiSeq X Ten, TopHat sur hg19, FPKM par
Cufflinks) — les lectures ont bien été produites, elles ne sont
simplement pas versées en libre accès.

### 2.2 PRJNA801501 (second volet, ATAC/WGS) : accès contrôlé chez NODE

Fiche BioProject PRJNA801501 (même reçu, même SHA), citée verbatim :

> « Please note that the raw data has been uploaded to a domestic
> repository National Omics Data Encyclopedia (NODE;
> https://www.biosino.org/node/index) with controlled access
> mechanisms under accession number OEP001744. »

Les données brutes de l'étude (RNA-seq, ATAC-seq, WGS) sont donc
centralisées chez NODE, dépôt national chinois, sous le numéro
**OEP001744**, avec des « mécanismes d'accès contrôlé ». La page
projet NODE (`https://www.biosino.org/node/project/detail/OEP001744`)
a été consultée le 21 nov. 2026 : HTTP 200 mais 906 octets
(coquille d'application JavaScript, fiche non lisible sans
session) ; une recherche web exacte `"OEP001744" NODE biosino` ne
retourne aucun résultat utilisable — le dépôt NODE n'est pas
indexé par les moteurs généralistes. Ce qui est établi ne dépend
pas de cette page : la fiche BioProject dit elle-même « controlled
access mechanisms ».

## 3. Ce que la fermeture ne dit pas

- Elle ne dit **pas** que DPCR1/MUCL3 seraient absents des lectures
  brutes : sans les lectures, la question est sans réponse. La
  matrice FPKM déposée (15 609 lignes) ne contient ni DPCR1 ni
  MUCL3, mais une re-dérivation avec une annotation actuelle aurait
  pu les compter autrement — c'était précisément l'intérêt de la
  piste, et c'est précisément ce qui est inaccessible.
- Elle ne dit **pas** que les lectures n'existent pas : elles
  existent chez NODE (OEP001744). Elle dit qu'elles ne sont pas
  accessibles en libre accès depuis cette machine, sans demande
  formelle.
- Elle ne change **rien** aux §8.86 et §8.88 : la matrice déposée
  reste inutilisable à 12 flux et NON à 11 flux ; la paire à 11 flux
  reste comptée comme 15e paire, avec son caveat.
- Elle ne rouvre **pas** C3 : levée depuis le §8.71, l'adoption
  pleine de `maxsep` (décision de Zackary, 20 nov. 13h04) ne
  dépendait pas de cette piste.

## 4. Ce qui débloquerait la piste (nommé, non entrepris)

Une demande d'accès contrôlé auprès de NODE
(https://www.biosino.org/node/index, projet OEP001744), dans le
cadre de la politique chinoise sur les ressources génétiques
humaines : demande formelle, identité institutionnelle,
justification, délai inconnu, issue incertaine. **Aucune demande
faite dans ce chantier ; aucune ne sera faite sans go explicite de
Zackary.** C'est un geste administratif et juridique, pas un
calcul — et il sort du périmètre de ce lot.

Une republication ouverte des lectures par les auteurs ou par un
tiers autorisé débloquerait aussi la piste ; aucune n'est connue
au 21 novembre 2026.

## 5. Bilan du chantier

- Accès vérifiés : 5 contrôles (SRA ×3, lien GEO→SRA ×1, ENA ×1),
  tous négatifs, tous conservés avec SHA.
- Téléchargements de lectures brutes : **0**.
- CSV de flux construits : **0**.
- Runs v6.2 lancés : **0**.
- Pipeline v6.2 vérifié inchangé, SHA
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
- A2 : **10/15 au-dessus du plancher, 12/15 positifs, LOO 9/14 —
  INCHANGÉ.** C3 reste levée.
- Contexte consigné (non décisif) : aucun outil de quantification
  installé sur la machine (`salmon`, `kallisto`, `samtools`,
  `STAR`, `hisat2`, `fasterq-dump`, `prefetch`, `pysradb`
  absents) ; 121 Go libres sous `/home/hatch`. La piste se ferme
  sur l'accès, pas sur l'outillage.

## 6. Sécurité — rappel

Cette section porte sur l'accès à des données d'expression et sur
un instrument d'analyse. Elle ne contient aucune recommandation
clinique. Le livre blanc n'est pas un conseil médical : toute
question de traitement se discute avec un oncologue.

---

*Fin de la section §8.91. Piste (d2) du §8.86.4 fermée. La suite
(d1) est faite au §8.88 ; il ne reste aucune suite nommée pour
GSE194249, sauf une demande d'accès contrôlé à NODE (sans go) ou
une republication ouverte des lectures.*
