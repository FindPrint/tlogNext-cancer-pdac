# PROTOCOLE GELÉ — §8.70 : Confirmation indépendante pour `maxsep` (C3) sur GSE79668

Date : 20 novembre 2026, ~14h45 EST. Chantier §8.70, mission parent du
20 nov. 2026 (« piste GSE79668 », go de Zackary « Allez s'y », 14h29).
Ce protocole est gelé AVANT tout téléchargement, toute construction et
tout run. Aucun téléchargement sans ce fichier. Aucun paramètre ne
change après les résultats. Le livre blanc N'EST PAS édité, le PDF
N'EST PAS régénéré, rien n'est poussé sur GitHub dans ce chantier
(convention des chantiers ; fusion par le coordinateur). La section
§8.70 est écrite dans un FICHIER SÉPARÉ
(`section_8.70_gse79668.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié ; v6.1
`2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`).

## 0. Contexte décisionnel — à lire avant tout le reste

- §8.56 : `maxsep` seul SUFFIT aux barres gelées (A1 37/48, A2 6/8
  avec 7/8 positifs, A3 HP35 +1,6512) ; `sep` seul REJETÉ (A2 5/8).
- §8.59 : ADOPTER SOUS CONDITION (D1, D2, D5 passent ; D3 et D4
  échouent — le verdict de suffisance tient à une paire et à
  l'échelle du plancher). Condition C3 : pleine adoption différée
  jusqu'à une confirmation indépendante portant A2 à 7 paires
  passantes.
- §8.64 : adoption sous condition CONFIRMÉE par troisième lecture
  (0 écart), convention d'affichage figée (maxsep principal, ancien
  MC secondaire, sep compagnon borné, mention de fragilité en tête
  de chaque table).
- **Le 20 nov. 2026 à 13h04, Zackary a décidé d'ADOPTER maxsep
  pleinement dès maintenant** (convention d'affichage : maxsep score
  principal, MC secondaire, aucun changement de code). **La
  confirmation indépendante du présent chantier devient donc une
  vérification a posteriori, pas une condition.** Si elle passe,
  elle consolide l'adoption ; si elle échoue, l'adoption pleine
  reste sa décision et la confirmation reste ouverte — à dire
  plainement dans les deux cas, dans la section comme dans le
  rapport. Ce chantier ne rouvre pas les §8.56/§8.59/§8.64/§8.69 et
  ne change aucune décision de Zackary.
- §8.69 : la neuvième paire principale indépendante, GSE21501
  (n = 132), a donné **NON** (`d_maxsep = −0,0100`, réel 0,2121
  contre nul 0,2221) ; A2 étendu **6/9** (7/9 positifs), LOO 5/8 —
  C3 NON levée. GSE79668 est la piste restante nommée au §8.69
  (§8.69.4, §8.69.6) : « seule piste restante nommée, non
  vérifiée ». Le présent chantier la vérifie, avec son propre
  protocole gelé.

## 1. Les 9 paires principales déjà utilisées (V1 + §8.69)

Valeurs reprises du §8.56.3 (re-vérifiées à l'identique aux §8.59
et §8.64, 0 écart) et du §8.69.2 (GSE21501, 2/2 à 0,0 exact).
Écart = maxsep réel − maxsep nul (|d| de Cohen). Plancher 0,07
en |d|.

| Paire | maxsep R / N | Écart | > 0,07 ? | Positif ? |
|---|---|---|---|---|
| HP35 | 1,7718 / 0,1206 | **+1,6512** | oui | oui |
| TCGA v4 | 0,4623 / 0,1696 | **+0,2928** | oui | oui |
| GSE71729 | 0,2593 / 0,2191 | +0,0402 | non | oui |
| GSE62452 | 0,3100 / 0,3136 | −0,0036 | non | NON (négatif, quasi nul) |
| ICGC | 0,4080 / 0,3110 | **+0,0970** | oui | oui |
| Immunitaire TCGA | 0,5309 / 0,1634 | **+0,3675** | oui | oui |
| PARP TCGA | 0,3680 / 0,1992 | **+0,1688** | oui | oui |
| DepMap | 0,4436 / 0,2532 | **+0,1904** | oui | oui |
| GSE21501 (§8.69) | 0,2121 / 0,2221 | −0,0100 | non | NON (négatif, quasi nul) |

Bilan : **6/9 au-dessus du plancher, 7/9 positifs.** Échecs :
GSE71729 (+0,0402, sous le plancher), GSE62452 (−0,0036) et
GSE21501 (−0,0100), tous deux négatifs quasi nuls.
Rotations V2 (48 paires, §8.44, sans doublon) : 37/48 pour
`maxsep`. Elles ne sont PAS rejouées ici : le présent chantier
ne porte que sur UNE paire principale supplémentaire (C3), pas
sur les rotations.

## 2. Paire choisie : GSE79668 — et pourquoi elle est vraiment indépendante

### 2.1 Choix

**Cohorte : GSE79668, NCBI GEO** — « RNA-sequencing of human
pancreatic adenocarcinoma cancer tissues », 51 échantillons,
plateforme GPL11154 (Illumina HiSeq 2000, Homo sapiens),
soumise le 11 juin 2016, BioProject PRJNA316673, SRA SRP072492.
Étude d'origine : Kirby et coll., *Molecular Oncology* 2016,
10(8):1169–1182 (PMID 27282075, PMCID PMC5423196,
doi 10.1016/j.molonc.2016.05.004) — « RNA sequencing of
pancreatic adenocarcinoma tumors yields novel expression
patterns associated with long-term survival and reveals a role
for ANGPTL4 ». 51 tissus tumoraux de patients opérés par
résection chirurgicale, University of Alabama at Birmingham
(HudsonAlpha Institute for Biotechnology + UAB, Birmingham, AL,
USA) ; bibliothèques Tn-RNAseq, analyse DESeq2 ; 323 transcrits
associés à la survie, modèle prédictif à 19 transcrits.
URL (même convention FTP que les autres provenances) :
`https://ftp.ncbi.nlm.nih.gov/geo/series/GSE79nnn/GSE79668/matrix/GSE79668_series_matrix.txt.gz`
Nombre de gènes attendu : 19 175 (tableau des cohortes, Posta
et coll., *Clin Transl Sci* 2023 — GSE79668 : GPL11154,
19 175 gènes, 51 échantillons).

### 2.2 Justification d'indépendance (écrite avant tout téléchargement)

1. **Désignée comme piste, jamais utilisée.** GSE79668 n'apparaît
   dans ce projet que comme « piste restante non vérifiée »
   (protocole §8.69, provenance §8.69, section §8.69, livre
   blanc §8.69) — jamais comme cohorte, paire principale,
   rotation ou bras descriptif. Aucun CSV de flux, aucun run,
   aucun JSON, aucune valeur `maxsep` n'existe pour GSE79668
   dans `~/workspace/runs/pdac-v6/`. Vérifié par grep avant le
   gel (20 nov. 2026) : la chaîne exacte « GSE79668 » ne figure
   que dans ces trois fichiers du chantier §8.69 (plus le livre
   blanc, au même sens) ; aucun fichier de données, aucun CSV,
   aucun dossier de résultats ne la porte. Les 2 257 fichiers
   JSON contenant la sous-chaîne nue « 79668 » sont des
   coïncidences numériques (ex. 65,79668663986135 dans
   `results_fast_tcga_v1/master_results.json`) — vérifié par
   lecture du contexte, pas des occurrences de GSE79668.
2. **Nouveaux patients, nouveau centre, nouvelle plateforme.**
   Cohorte monocentrique UAB (Birmingham, AL) — aucun
   recoupement avec TCGA (multi-centres, 178 cas), ICGC PACA-AU,
   ni les cohortes GEO déjà utilisées (NCI pour GSE62452,
   autres centres pour GSE71729/GSE62165, Stratford Royaume-Uni
   pour GSE21501, Moffitt Tampa pour GSE57495). Plateforme
   RNA-seq Illumina HiSeq 2000 (GPL11154), distincte de toutes
   les plateformes V1 (RNA-seq TCGA, Illumina ICGC, Affymetrix
   GPL20769/GPL6244/GPL13667/GPL15048, Agilent GPL4133).
   Patients distincts : 51 tumeurs réséquées, cohorte UAB 2016.
3. **Traitée comme indépendante par la littérature.** Liu et
   coll., *Oncol Rep* 2019, 41:1521–1530
   (doi 10.3892/or.2019.6979) utilisent GSE79668 (n = 51) comme
   jeu de validation INDÉPENDANT face à l'entraînement TCGA
   (n = 178), aux côtés de GSE62452 (n = 69) — les trois jeux
   sont disjoints dans leur analyse (tableau I : effectifs et
   statistiques distincts par jeu).
4. **Même construction que les autres paires principales GEO.**
   Variante (a) des builders `build_fluxes_geo71729.py` /
   `build_fluxes_geo62452.py` / `build_fluxes_869.py` : les 12
   mêmes gènes que la v4 TCGA, ordre = KRAS croissant, sans
   correction, cas complets, nul = lignes permutées graine 42
   (§4). La paire est donc comparable aux 9 paires déjà
   comptées par construction, et son issue est inconnue : aucun
   `maxsep` GSE79668 n'existe à ce jour, et rien dans les
   résultats publiés (signature de survie à 19 transcrits,
   ANGPTL4) ne prédit l'écart réel−nul du pipeline.
5. **Pas un re-test déguisé.** Ce n'est ni une relecture d'un JSON
   existant (§8.64.7 : « pas une relecture »), ni une rotation
   déjà comptée, ni un sous-ensemble d'une paire V1, ni un nouvel
   ordre sur des CSV existants (nouveaux CSV, nouveaux runs,
   2 runs v6.2 frais).

**Nuance consignée avant le gel.** L'article Kirby et coll. a
lui-même utilisé TCGA comme cohorte de validation de sa
signature (survie, ANGPTL4) — les 51 échantillons GSE79668
restent des patients UAB, pas des échantillons TCGA : la
comparaison publiée ne crée aucun recouvrement d'échantillons.
Après téléchargement, les identifiants d'échantillons (GSM,
titres) seront inspectés : aucun ne doit porter un code-barres
TCGA ; tout recouvrement constaté serait consigné et la
cohorte écartée comme non indépendante (porte §5).

### 2.3 Candidats écartés (enquête §8.66 §1.3 + addendum §8.69, reprise telle quelle)

GSE78229 (échantillons déjà inclus dans GSE62452), GSE28735
(échantillons 1–90 de GSE62452), COAD / LUAD (autres cancers +
lots déjà courus = relecture), CPTAC (protéine, 7/6 flux, lots
déjà courus), GSE15471 / GSE16515 / GSE32676 / GSE91035 /
GSE84219 / GSE179351 (n < 40), ICGC PACA-CA / E-MTAB-6134
(accès hors périmètre), GSE57495 et GSE62165 (portes §5
échouées au §8.69 : GSTM1, DPCR1 absents — construction à
12 gènes inchangée ici, elles restent inutilisables sous cette
construction). GSE21501 a servi au §8.69 : exclue comme
re-test.

## 3. Arrêt borné — AUCUN repli technique

**Une seule cohorte dans ce chantier : GSE79668.** Si elle est
INUTILISABLE selon les critères d'acceptation du §5
(téléchargement impossible, plateforme sans table exploitable,
n < 40, KRAS absent, < 12 gènes v4 mappés, < 40 cas complets,
ou recouvrement d'échantillons avec une cohorte déjà utilisée),
le chantier s'arrête sur un blocage documenté : section §8.70
écrite quand même, avec les tentatives chiffrées, aucune valeur
inventée, et la piste suivante nommée comme piste seulement
(aucune autre cohorte forcée, aucun run lancé pour elle).
Il n'y a PAS de cohorte #2 dans ce chantier — contrairement au
§8.69, qui disposait d'un repli puis d'un addendum, le présent
chantier est borné à GSE79668 par décision de mission (« lancer
la piste GSE79668 »).

## 4. Construction des flux — variante (a), comme les paires GEO V1

Nouveau script `build_fluxes_870.py` (copie adaptée de
`build_fluxes_869.py`, original intact). Préfixe `_870_` pour
tous les fichiers du chantier.

### 4.1 Identification gènes (GSE79668 / GPL11154, RNA-seq)

- La matrice est une matrice RNA-seq : ses lignes sont des
  identifiants de gènes (symboles HGNC, Entrez ou Ensembl selon
  le dépôt), PAS des sondes de puce. La règle est donc :
  (a) si les identifiants de lignes sont déjà des symboles de
  gènes HGNC, ils sont utilisés directement — consigné tel quel
  dans `PROVENANCE_870.md`, sans mapping ; (b) sinon, le
  mapping est construit à neuf depuis la table de plateforme
  GPL11154 téléchargée en streaming
  (`https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL11nnn/GPL11154/soft/GPL11154_family.soft.gz`,
  arrêt après `!platform_table_end`, même méthode que
  `download_gpl15048_mapping_869.py`), colonne de symbole
  identifiée sur la table réelle et consignée (jamais devinée).
- Sortie éventuelle : `data/GPL11154_probe2symbol.tsv` (SHA
  consigné) — seulement si le cas (b) s'applique.
- Identifiants multiples vers un même symbole : agrégation par
  médiane (règle du projet). Identifiant sans symbole : non
  mappé. Identifiant vers plusieurs symboles : exclu si ambigu
  (aucun gène mappé à la main).
- La plateforme réelle est confirmée par l'en-tête de la
  matrice (`!Series_platform_id`) et consignée dans
  `PROVENANCE_870.md` ; si l'en-tête dit autre chose que
  GPL11154, c'est consigné tel quel et la construction s'adapte
  à la plateforme réelle (le mapping se construit depuis la
  table de LA plateforme indiquée par la matrice, jamais depuis
  un mapping d'une autre plateforme).

### 4.2 Série réelle (variante (a))

- Gènes v4 (les 12 mêmes que TCGA v4, ordre de la liste) :
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1,
  CEACAM5, CLCA1, MUC16.
- Contrôle : KRAS (expression RNA-seq, croissant). Le contrôle
  n'est JAMAIS un flux : pas de doublon. Justification de
  l'ordre KRAS : identique aux paires principales V1 — KRAS
  est le contrôle monotone du projet, et l'ordre par son
  expression est celui de toutes les paires GEO à 12 gènes ;
  aucun ordre stade n'est construit (les paires principales V1
  sont en ordre KRAS ; la survie publiée ne sert pas d'ordre
  ici — l'ordre KRAS est le seul ordre gelé).
- Tumeurs seules (caractéristiques `!Sample_characteristics_ch1`
  et titres `!Sample_title` ; si la matrice ne contient que
  des tumeurs, c'est consigné tel quel ; si des non-tumeurs
  existent, elles sont exclues et comptées). Cas complets
  seulement (KRAS + 12 gènes présents), jamais d'imputation.
  Valeurs : telles que fournies par les déposants (nature exacte
  — comptages, FPKM/RPKM, log2 ou autre — consignée dans
  `PROVENANCE_870.md` d'après l'en-tête de la matrice et la
  plage des valeurs ; aucune renormalisation, aucune
  transformation log ajoutée).
- Sorties : `pdac_870_geo79668_fluxes.csv` (+ `_nul.csv`).
  Colonnes : `step` + 12 flux. SHA-256 consignés.

### 4.3 Nul

Bloc des flux permuté par lignes, graine 42, `rng(42)`, contrôle
(KRAS, ordre) intact — même convention que les paires V1
(§8.56.8, PROTOCOL_phase2 §2). Le nul est un échantillon
hypothétique, pas une mesure.

### 4.4 Nuls frais (conditionnels, §7)

Si et seulement si l'écart mesuré sur la paire graine 42 est
PROCHE du plancher (§7 : `d_maxsep` dans [−0,07 ; +0,14[),
2 nuls frais sont construits par la même méthode, graines
**8701** et **8702** (graines jamais utilisées dans ce projet,
gelées ici avant tout run), et courus en runs frais
(`pdac_870_geo79668_fluxes_nul_s8701.csv`,
`pdac_870_geo79668_fluxes_nul_s8702.csv`,
`results_fast_v62_870_geo79668_nul_s8701`,
`results_fast_v62_870_geo79668_nul_s8702`). Le verdict reste
celui de la paire graine 42 (§7) ; les nuls frais sont un
contrôle de robustesse descriptif (min / médiane / max des
écarts), jamais un moyen de choisir le nul qui arrange.

## 5. Critères d'acceptation de la cohorte (vérifiés après téléchargement, avant construction)

- Matrice téléchargée, HTTP 200, lecture complète vérifiée
  (nombre de lignes, 0 NaN ou NaN comptés) ; SHA-256 consigné
  dans `PROVENANCE_870.md` avant toute construction.
- Plateforme lue dans l'en-tête de la matrice ; table de
  plateforme téléchargeable et exploitable si un mapping est
  nécessaire (§4.1, cas (b)) — sinon ARRÊT (§3).
- n ≥ 40 tumeurs PDAC (minimum v6.2 fast) ; sinon ARRÊT (§3).
- Aucun échantillon porteur d'un code-barres TCGA ou déjà
  présent dans une cohorte du projet (GSM/titres inspectés) ;
  sinon ARRÊT (§3).
- KRAS présent comme ligne mappée ; sinon ARRÊT (§3).
- Les 12 gènes v4 présents (mappés) ; sinon ARRÊT (§3)
  (aucun gène remplacé, aucun absent toléré pour une paire
  principale — la comparabilité aux 9 paires comptées
  l'exige).
- Cas complets (KRAS + 12 gènes) ≥ 40 ; sinon ARRÊT (§3).

## 6. Runs v6.2 (mode fast)

- Lot : 2 runs — réel + nul — manifeste `manifest_v62_870.txt`,
  lanceur reprenable existant `run_v62_lot.sh` (saute les sorties
  déjà complètes), journal `runs_v62_870.log` (SHA du pipeline
  en tête, exits consignés).
- Dossiers : `results_fast_v62_870_geo79668` et
  `results_fast_v62_870_geo79668_nul` (nuls frais éventuels :
  `results_fast_v62_870_geo79668_nul_s8701` /
  `..._s8702`).
- Lancement en `systemd-run --unit=v62-870 --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance qui
  s'arrête d'elle-même à 2/2 (ou 4/4 si nuls frais). Ne JAMAIS
  supprimer le dossier d'un run en cours. Si la machine
  redémarre, reprise sans perte (SKIP des dossiers complets,
  jamais de relance à l'aveugle).
- SHA du pipeline revérifié avant ET après le lot.

## 7. Critère de passage — GELÉ avant tout run

**La paire PASSE si et seulement si :**
`d_maxsep = maxsep_R − maxsep_N > 0,07` (plancher, en unités |d|,
gigue_eff = max(gigue mesurée, 0,07) — v6.2 déterministe, gigue
attendue 0, comme §8.56 §3) **ET** `d_maxsep > 0` (positif —
impliqué par > 0,07, mais consigné séparément comme au §8.56).

`maxsep` = `best_config.metrics.max_separation`, |d de Cohen|
maximal du scan, lu sur le best_config ANCIEN (sélection par
l'ancien composite) — mêmes définitions que §8.56.2. Le seuil MC,
la cascade, S_sep, Delta, L7a sont inchangés par construction.

**Catégories de verdict (gelées) :**
- **CONFIRME** : `d_maxsep > 0,07` — la paire passe.
- **PARTIEL** : `0 < d_maxsep ≤ 0,07` — positif mais sous le
  plancher (même catégorie que GSE71729, +0,0402).
- **NON** : `d_maxsep ≤ 0` — négatif ou nul (même catégorie que
  GSE62452 et GSE21501).

**Verdict étendu (A2 à 10 paires) :**
- Si la paire passe : A2 étendu = **7/10 au-dessus du plancher,
  8/10 positifs** (les 9 paires gardent leurs valeurs : 6/9 et
  7/9 positifs). La condition C3 du §8.59.8 est levée — la
  confirmation indépendante consolide l'adoption pleine décidée
  par Zackary le 20 nov. 13h04. Le leave-one-out sur les 10
  paires est calculé en descriptif : retirer n'importe quelle
  paire passante laisse 6/9, qui satisfait encore la barre A2
  d'origine (≥ 6/8) — l'adoption ne tient plus à une seule
  paire.
- Si la paire est PARTIELLE : A2 étendu = **6/10, 8/10
  positifs**. C3 reste OUVERTE.
- Si la paire échoue (NON) : A2 étendu = **6/10, 7/10 positifs**.
  C3 reste OUVERTE, la confirmation reste à trouver, et
  l'adoption pleine reste la décision de Zackary du 20 nov.
  13h04 — ce chantier ne la rouvre pas et ne la conditionne
  pas.

**Note sur le libellé « 7/8 » de la mission et du §8.59.8.**
« Porter A2 à 7/8 » y est écrit de façon lâche. La lecture
précise retenue ici est celle du §8.69 §7, qui corrige ce
libellé : **7 paires passantes au total** — soit 7/10 avec la
dixième paire, et un leave-one-out dont le pire cas (retrait
d'une paire passante) laisse 6/9, soit la barre A2 d'origine
toujours satisfaite. C'est le sens opératoire de « l'adoption
ne tient plus à une paire ». Le chiffre 7 (nombre de paires
passantes) est le même que dans la mission ; seul le
dénominateur change (10 paires comptées, pas 8).

**Nuls frais (§4.4, règle gelée).** La paire graine 42 fait le
verdict, dans tous les cas. Si `d_maxsep` est PROCHE du
plancher — défini ici comme `d_maxsep` dans [−0,07 ; +0,14[,
soit à moins d'une largeur de plancher du seuil, de part et
d'autre — les 2 nuls frais (graines 8701, 8702) sont courus et
les écarts `d` contre chaque nul frais sont rapportés
(min / médiane / max des 3 écarts). Lecture gelée : si les
3 écarts sont > 0,07, le passage est dit « consolidé » ; si
l'un des 3 est ≤ 0,07, le passage (ou l'échec) est dit
« fragile, non consolidé » — le verdict de la paire graine 42
n'est JAMAIS changé par les nuls frais. Si `d_maxsep` est
hors de [−0,07 ; +0,14[, aucun nul frais n'est couru.

**Contrôles descriptifs (à publier, ne décident pas) :**
- `sep` compagnon (= maxsep/(1+maxsep)), ancien MC (secondaire),
  S_sep, Delta, L7a, cascade, falsification — affichés selon
  la convention §8.64.6 (maxsep principal, ancien MC secondaire,
  sep compagnon, mention de fragilité en tête de table).
- Falsification : INDISPONIBLE sous n = 75 — GSE79668 n = 51 :
  noter « indisponible », ne pas imputer.
- Plancher équivalent-sep (descriptif) : la paire passe-t-elle
  aussi `0,07·(1+m_R)(1+m_N)` ? Rapporté, non décisif (D4 n'est
  pas rejoué ici : il porte sur les paires V1, déjà tranché).
- Aucun autre critère, aucune repondération, aucune redéfinition
  du plancher après avoir vu les chiffres.

## 8. Extraction et vérification

1. Extracteur propre du chantier, `extract_870.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_866.py` / `extract_869.py`) ; lit `maxsep`,
   `mc_score`, `stability`, `ssep`, `delta`, `l7a`, cascade,
   falsification dans les 2 (ou 4) `master_results.json` ;
   sorties `extract_870.json` / `extract_870.csv`.
2. Second calcul indépendant : relecture directe des
   `master_results.json` par un chemin distinct (script
   `verify_870.py`, SHA noté) — `maxsep` et ancien MC recoupés
   à 0,0 exact ; tout écart = résultat à diagnostiquer, pas un
   bruit.
3. Recoupements : les 9 valeurs déjà comptées reprises telles
   quelles du §8.56 (table `sep_maxsep_856_table.json`, SHA
   `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`)
   et du §8.69 (`extract_869.json`, SHA
   `644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b`),
   jamais recalculées ici — ce chantier ne re-vérifie pas les
   §8.56/§8.59/§8.64/§8.69 (déjà clos).
4. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 9. Tests directs en appui (ne décident pas)

Script `direct_tests_870.py` (SHA noté), sur les CSV de flux
du chantier (réel + nul graine 42) :
1. d de Cohen des 12 flux (réel vs nul) : pour chaque gène v4,
   moyenne et écart-type des valeurs ordonnées, d de Cohen
   réel−nul ; table complète, sans sélection.
2. Si l'ordre est KRAS (cas attendu) : comparaison descriptive
   avec le §8.69 — au §8.69, Delta +2,01 contre maxsep −0,01.
   Si la même divergence apparaît ici (Delta nettement en
   faveur du réel, maxsep plat ou négatif), elle est nommée
   telle quelle, sans être élucidée sans preuve ; si elle
   n'apparaît pas, c'est consigné aussi.
3. Aucun de ces tests ne change le verdict du §7.

## 10. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et le
  jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict : les tests directs du §8.66, la signature pronostique
  Kirby et coll. (19 transcrits, ANGPTL4), les scores de Liu et
  coll. ne prédisent rien ici — seul l'écart `maxsep` mesuré
  sur les runs du présent chantier fait le verdict.
- Un nul qui invalide une piste est un résultat ; un échec de la
  paire est un verdict, pas un échec caché.
- Ne jamais présenter une lecture préliminaire comme un verdict.
- Aucun consensus exigé entre flux ou contrôles ; aucune
  affirmation clinique — l'étude porte sur l'instrument.

## 11. Livrables

- Ce protocole (gelé avant téléchargement, construction et runs).
- `PROVENANCE_870.md` (source, auteur, date, dépôt, URL, SHA-256
  des fichiers téléchargés, plateforme réelle, effectifs, exclus,
  identification des gènes — avec la vérification d'indépendance
  du §2.2).
- `download_gpl11154_mapping_870.py` (seulement si le cas (b) du
  §4.1 s'applique) + éventuellement `data/GPL11154_probe2symbol.tsv`.
- `build_fluxes_870.py` + CSV de flux (`pdac_870_*`, SHA consignés).
- `manifest_v62_870.txt`, `runs_v62_870.log`, dossiers
  `results_fast_v62_870_*`, `extract_870.json` / `.csv`,
  `verify_870.py` + sortie de vérification,
  `direct_tests_870.py` + sortie.
- §8.70 dans le FICHIER SÉPARÉ
  `section_8.70_gse79668.md` (verdict d'abord, une phrase :
  C3 levée ou non ; chiffres ensuite ; détail complet après ;
  provenance nommée partout).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin du protocole gelé §8.70. —
