# PROTOCOLE GELÉ — §8.79 : GDC ORGANOID-PANCREATIC, 13e paire principale indépendante pour `maxsep`

Date : 21 novembre 2026, ~12h30 EST. Chantier §8.79, piste B.
Protocole gelé AVANT tout téléchargement des données (les 55 TSV GDC ne
sont pas encore téléchargés ; seules des vérifications de métadonnées
— manifeste, cas GDC, suppléments publics — ont eu lieu avant ce gel,
documentées au §2). Aucun paramètre ne change après les résultats.
Le livre blanc N'EST PAS édité, le PDF N'EST PAS régénéré, rien n'est
poussé sur GitHub dans ce chantier (convention des chantiers ; fusion
par le coordinateur). La section §8.79 est écrite dans un FICHIER
SÉPARÉ (`section_8.79_nouvelle_serie.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié ; v6.1
`2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`).
Chemin : `/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`.

Note de cécité (état connu du fichier v6.2, inchangé depuis son
adoption) : un grep `temperature|Onsager|2.269` sur le fichier
retourne 8 occurrences, TOUTES confinées à l'annexe génératrice
d'exemple Ising (fonction `generate_example_ising_csv`, marquée
« EXEMPLE UNIQUEMENT, hors cœur du pipeline »). Le cœur d'analyse
ne voit ni T ni Tc ; le fichier est celui adopté, SHA vérifié
ci-dessus, jamais modifié.

## 0. Contexte décisionnel — à lire avant tout le reste

- §8.56 : `maxsep` seul SUFFIT aux barres gelées ; `sep` seul
  REJETÉ.
- §8.59 : ADOPTER SOUS CONDITION (D1, D2, D5 passent ; D3 et D4
  échouent). Condition C3 (§8.59.8) : 7 paires passantes au total,
  LOO pire cas à la barre A2 d'origine.
- §8.71 : onzième paire, GSE60979, **CONFIRME** (`d_maxsep =
  +0,2045`) ; A2 étendu **7/11, 9/11 positifs**, LOO 6/10 —
  **C3 LEVÉE**.
- 20 nov. 2026, 13h04 : Zackary a décidé d'**ADOPTER maxsep
  pleinement** (maxsep score principal, MC secondaire, aucun
  changement de code).
- §8.74 : douzième paire, GSE131050 lot Yeh_seq FF (n = 42),
  **CONFIRME** (`d_maxsep = +0,0739`) ; A2 étendu **8/12,
  10/12 positifs**, LOO 7/11. **C3 RESTE LEVÉE.**
- §8.76 : lot Yeh_seq FNA, mêmes tumeurs — test de robustesse
  APPARIÉ, pas une paire (41/42 codes communs) ; A2 INCHANGÉ.
- §8.77 : reproductibilité réparée (19/19 gaps fermés).
- §8.78 : inventaire des dépôts (piste A) — 6 candidates pour
  la piste B, dont 2 fortes (C1 Chen 2025, C2 GDC
  ORGANOID-PANCREATIC). Le présent chantier est la piste B :
  choisir UNE candidate, geler le protocole, courir la paire.
- **Ce chantier ne rouvre pas C3, quelle que soit son issue.**
  Si la paire passe, elle consolide l'adoption par une
  treizième paire indépendante ; si elle échoue, l'adoption
  pleine reste la décision de Zackary du 20 nov. 13h04 — à dire
  plainement dans les deux cas, dans la section comme dans le
  rapport. Ce chantier ne rouvre pas les §8.56/§8.59/§8.64/
  §8.69/§8.70/§8.71/§8.74/§8.76 et ne change aucune décision
  de Zackary.
- §8.70/§8.72 : correction de méthode notée au §8.70 (§8.70.5,
  §8.70.7) et APPLIQUÉE ici (§9) : le test de Cohen marginal
  est vacueux par construction quand le nul est une permutation
  de lignes (d = 0,0000 pour les 12 gènes) — le test informatif
  est le Spearman de chaque flux contre le pas (Δρ médian,
  nombre de positifs). Le Cohen marginal est quand même rapporté
  (il valide la construction du nul), mais il ne porte aucune
  information d'ordre et ne décide rien.

## 1. Les 12 paires principales indépendantes déjà comptées

Valeurs reprises des §8.56/§8.69/§8.70/§8.71/§8.74, jamais
recalculées. Écart = maxsep réel − maxsep nul. Plancher 0,07.

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

Bilan : **8/12 au-dessus du plancher, 10/12 positifs.** LOO
7/11. Rotations V2 (48 paires, §8.44, sans doublon) : 37/48
pour `maxsep`. Elles ne sont PAS rejouées ici.

## 2. Choix de la candidate : C2, GDC ORGANOID-PANCREATIC — et vérifications pré-gel

### 2.1 Les candidates examinées avant le gel (vérifications de métadonnées seulement)

| # | Candidate | Vérification pré-gel (21 nov. 2026) | Décision |
|---|---|---|---|
| C1 | Chen et al. 2025, Nat. Commun., 46 PDO × 63 AUC | Supplément MOESM13 re-téléchargé et SHA VÉRIFIÉ EXACT : `0e009cd56d2f6c25b0b355590becc4abfee3e1080633173bc33606d1bf325340` (35 732 o). Input CSV non détenu localement (introuvable sur cette VM) mais reconstructible (manifeste `PIPELINE_INPUT_MANIFEST.json`, SHA input `296681b6…`). Protocole pilote et script de run lus depuis `universal-log-research`. | NON CHOISIE : axe drogue (cible Gemcitabine, 62 contrôles, 124 runs), pas une paire KRAS / 12 gènes — elle ne peut pas devenir une 13e paire A2 ; son statut reste celui d'un lot drogue à part, comme Tiriac. Non écartée comme ressource : reste la piste suivante pour un lot drogue v6.2. |
| **C2** | **GDC ORGANOID-PANCREATIC, 55 RNA-seq ouvertes** | **CHOISIE (§2.2).** Manifeste re-téléchargé, SHA VÉRIFIÉ EXACT `f713edebf0f8afb20305b1472d480564e45ac31ce79e28350d7dde6ae496220b` (attendu gelé dans `build_gdc_unstranded_matrix.py`). Cas GDC interrogés par API (49/49 retrouvés, tous pancréas, projet ORGANOID-PANCREATIC). Fichiers associés interrogés (55/55). | **CHOISIE : 13e paire.** |
| C3 | GSE57495 (GPL15048, n=63) | Matrice locale SHA VÉRIFIÉ EXACT `995dbeff288a14c1cc1a52489e456b7677ede5da8e287069b8298d649b532efc` (§8.69). 11/12 v4 (GSTM1 absent), déjà tenue comme holdout direct (§8.66/§8.69, ρ=0,4377). | NON CHOISIE : 11 gènes seulement (paire non comparable à 12 flux) + antériorité holdout. Reste le repli documenté si C2 échoue aux portes du §5. |
| C4 | GSE194249 (84 PDPCOs) | Audit scripté, sortie d'audit absente du dépôt (§8.78) ; n réponse exact et couverture v4 NON vérifiés — audit à refaire depuis GEO. | NON VÉRIFIÉE : pas de décision possible sans re-audit ; non choisie. |
| C5 | GSE262627 (circadien, 7 temps) | 7 < 40. | ÉCARTÉE (déjà au §8.78). |
| C6 | OrganoIDNetData (Zenodo, imagerie) | Flux morphologiques à définir, archive 4,6 Go non téléchargée, inventaire metadata-only requis + autorisation explicite. | ÉCARTÉE pour v6.2 inchangé (déjà au §8.78). |

Vérifications d'indépendance contre le livre blanc (grep,
§8.1–§8.77, 21 nov. 2026) : « HCMI » 0 mention, « organoid »
0, « GDC » 2 mentions (toutes deux = accès TCGA via Xena/GDC,
lignes 4919 et 6486 — pas ORGANOID-PANCREATIC), « Chen et
al » 0, « 57520 » 0, « GSE194249 » 0, « STAR » 0. La candidate
C2 n'a JAMAIS été utilisée dans ce projet.

### 2.2 Indépendance de C2 — ce qui est établi avant tout run

1. **Jamais courue.** Aucun CSV de flux, aucun run, aucun JSON,
   aucune valeur `maxsep` n'existe pour GDC
   ORGANOID-PANCREATIC dans ce projet (grep §2.1).
2. **Patients distincts par construction de programme.** Les 49
   cas sont du projet GDC `ORGANOID-PANCREATIC` (Human Cancer
   Models Initiative / Next Generation Cancer Models),
   identifiants de cas UUID GDC et `submitter_id` entiers
   (1–71) — système d'identifiants sans aucun recouvrement
   possible par jointure avec les cohortes tenues (barres
   TCGA `TCGA-XX-XXXX`, GSM GEO, ICGC). Aucun `TCGA` dans le
   manifeste ni dans les cas interrogés. Les programmes sont
   distincts (modèles organoïdes dérivés de patients enrôlés
   pour HCMI, pas la cohorte chirurgicale TCGA PAAD).
   **Limite déclarée :** aucun identifiant commun n'existe
   entre les deux systèmes, donc le non-recouvrement ne peut
   pas être prouvé par une jointure d'identifiants — il est
   établi par programme, par système d'identifiants et par
   absence de tout lien documenté ; c'est une limite, pas une
   preuve formelle.
3. **Composition exacte établie par l'API GDC avant le gel**
   (requêtes `cases` et `files`, 21 nov. 2026, réponses
   conservées en scratch `/tmp/b879/gdc_cases_detail.json` et
   `gdc_files_detail2.json` — métadonnées, pas des données
   d'expression) :
   - 55 fichiers, 49 cas, tous `primary_site = Pancreas`,
     tous projet `ORGANOID-PANCREATIC`.
   - Association fichier → échantillon (1 échantillon par
     fichier, via l'expansion `cases.samples` de l'API
     `files`) : **44 fichiers = échantillons Tumor** de cas
     au diagnostic « Adenocarcinoma, NOS » ; **11 fichiers =
     échantillons Normal** de cas au diagnostic « Unknown »
     (cas 61–71, échantillons S158–S215).
   - Les 11 fichiers Normal sont EXCLUS par le protocole (§4)
     : ce ne sont pas des tumeurs. La cohorte testée est donc
     **44 fichiers tumoraux**, pas 55.
   - Les 44 fichiers tumoraux proviennent de **38 cas**
     (diagnostic « Adenocarcinoma, NOS ») : 35 cas à 1
     fichier, 1 cas à 2 fichiers, 1 cas à 3 fichiers,
     1 cas à 4 fichiers (9 fichiers pour 3 cas).
   - **Unité d'analyse gelée : le FICHIER (échantillon
     organoïde), n = 44.** Chaque fichier est un modèle
     organoïde distinct (échantillon `submitter_id` distinct).
     Les 3 cas multi-fichiers sont DÉCLARÉS plainement (§4.4,
     §8.79) : 9 lignes sur 44 proviennent de 3 patients — une
     dépendance partielle, nommée, non cachée. L'agrégation
     par cas (médiane, précédent §8.76) donnerait n = 38 cas,
     SOUS le minimum v6.2 fast (40) — elle n'est donc pas le
     repli : si l'unité fichier était jugée invalide, la
     candidate serait inutilisable, pas ré-agrégée.
4. **Pas un re-test déguisé.** Ni une relecture d'un JSON
   existant, ni une rotation déjà comptée, ni un sous-ensemble
   d'une paire V1, ni un nouvel ordre sur des CSV existants
   (nouveaux CSV, nouveaux runs, 2 runs v6.2 frais, données
   jamais courues).
5. **Statut de la cohorte.** Transversale, ordonnée par un flux
   (KRAS, comme TCGA/ICGC) — même statut que les paires
   TCGA/ICGC, pas de pseudo-temps. Les organoïdes sont des
   modèles dérivés de patients, pas des tumeurs primaires
   directes : c'est dit plainement au §8.79, et le verdict
   porte sur l'instrument, pas sur une affirmation clinique.

## 3. Arrêt borné — AUCUN repli technique dans ce chantier

**Une seule cohorte dans ce chantier : GDC
ORGANOID-PANCREATIC, fichiers tumoraux, n = 44.** Si elle est
INUTILISABLE selon les critères d'acceptation du §5
(manifeste SHA différent, téléchargement incomplet ou MD5 en
échec, n tumoraux < 40, KRAS absent, < 12 gènes v4 mappés,
< 40 cas complets), le chantier s'arrête sur un blocage
documenté : section §8.79 écrite quand même, avec les
tentatives chiffrées, aucune valeur inventée, et la piste
suivante nommée comme piste seulement (C3 GSE57495, avec son
caveat 11/12 + holdout, ou C1 lot drogue — aucun run lancé
pour elle dans ce chantier).
Il n'y a PAS de cohorte #2 courue dans ce chantier.

## 4. Construction des flux — variante (a), comme les paires GEO V1

Nouveau script `build_fluxes_879.py`. Préfixe `_879_` pour tous
les fichiers du chantier.

### 4.1 Source et téléchargement (APRÈS ce gel)

- Manifeste : `GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST.tsv`,
  SHA-256 `f713edebf0f8afb20305b1472d480564e45ac31ce79e28350d7dde6ae496220b`
  (vérifié avant le gel, re-vérifié au téléchargement).
- Téléchargement : `https://api.gdc.cancer.gov/data/<file_id>`
  pour chacun des 55 `file_id` du manifeste (accès ouvert),
  3 tentatives max par fichier, dans
  `data/gdc_organoid_879/` (noms `<file_id>.tsv`).
  Taille totale attendue 232 648 892 o.
- Vérification : MD5 de chaque fichier contre le manifeste
  (55/55 exigés) + SHA-256 de chaque fichier consigné. Tout
  écart = ARRÊT (§3).
- Format attendu (vérifié sur le script
  `build_gdc_unstranded_matrix.py` du dépôt
  `pdac-systems-evidence-preclinical`, en-tête gelé) :
  colonnes `gene_id, gene_name, gene_type, unstranded,
  stranded_first, stranded_second, tpm_unstranded,
  fpkm_unstranded, fpkm_uq_unstranded` ; 60 660 lignes de
  gènes + 4 lignes techniques STAR (`N_unmapped`,
  `N_multimapping`, `N_noFeature`, `N_ambiguous`). Si
  l'en-tête diffère, c'est consigné tel quel et la
  construction s'arrête (arrêt borné §3).

### 4.2 Identification des gènes

- Symbole lu dans la colonne `gene_name` (symbole exact,
  sensible à la casse). Aucun gène mappé à la main.
- Les 13 gènes utiles (12 v4 + KRAS) doivent être présents,
  UNE ligne chacun, sans doublon de symbole, dans CHAQUE
  fichier retenu. Tout doublon ou absence = ARRÊT (§3).
- Valeurs : colonne **`tpm_unstranded`** telle que fournie
  par GDC (normalisation TPM du fournisseur, pas un calcul
  de ce chantier). Aucune renormalisation, aucune
  transformation log, aucune imputation ajoutée. Les 4
  lignes techniques STAR sont exclues.

### 4.3 Série réelle (variante (a))

- Gènes v4 (les 12 mêmes que TCGA v4, ordre de la liste) :
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1,
  CEACAM5, CLCA1, MUC16.
- Contrôle : KRAS (expression TPM, croissant). Le contrôle
  n'est JAMAIS un flux : pas de doublon. Justification de
  l'ordre KRAS : identique aux paires principales V1 — KRAS
  est le contrôle monotone du projet, et l'ordre par son
  expression est celui de toutes les paires GEO à 12 gènes.
- Fichiers retenus : les **44 fichiers tumoraux** (§2.2) ;
  les 11 fichiers Normal sont exclus et comptés. Le
  diagnostic « Adenocarcinoma, NOS » est celui des 38 cas
  sources ; les 44 fichiers sont tous des échantillons
  Tumor (`tissue_type = Tumor`).
- **Unité = fichier (§2.2 point 3).** Aucune agrégation entre
  fichiers d'un même cas. Les 3 cas multi-fichiers (2, 3 et
  4 fichiers) entrent tels quels, déclarés au §8.79.
- Cas complets seulement (KRAS + 12 gènes présents), jamais
  d'imputation. Attendu : 44/44 cas complets (0 NaN attendu
  sur les 13 lignes × 44 fichiers — vérifié, sinon ARRÊT
  si < 40 complets).
- Tri : KRAS TPM croissant ; `step` = rang 0..43.
- Sorties : `pdac_879_gdc_organoid_fluxes.csv` (+ `_nul.csv`).
  Colonnes : `step` + 12 flux. SHA-256 consignés.

### 4.4 Nul

Bloc des flux permuté par lignes, graine 42, `rng(42)`,
contrôle (ordre KRAS, `step`) intact — même convention que
les paires V1 (§8.56.8, PROTOCOL_phase2 §2). Le nul est un
échantillon hypothétique, pas une mesure.

### 4.5 Nuls frais (conditionnels, §7)

Si et seulement si l'écart mesuré sur la paire graine 42 est
PROCHE du plancher (§7 : `d_maxsep` dans [−0,07 ; +0,14[),
2 nuls frais sont construits par la même méthode, graines
**8791** et **8792** (graines jamais utilisées dans ce projet,
gelées ici avant tout run), et courus en runs frais
(`pdac_879_gdc_organoid_fluxes_nul_s8791.csv`,
`pdac_879_gdc_organoid_fluxes_nul_s8792.csv`,
`results_fast_v62_879_gdc_organoid_nul_s8791`,
`results_fast_v62_879_gdc_organoid_nul_s8792`). Le verdict
reste celui de la paire graine 42 (§7) ; les nuls frais sont
un contrôle de robustesse descriptif (min / médiane / max des
écarts), jamais un moyen de choisir le nul qui arrange.

## 5. Critères d'acceptation de la cohorte (vérifiés sur les fichiers téléchargés, avant construction)

- Manifeste SHA-256 `f713edebf…6220b` (re-vérifié) ; 55 lignes.
- 55/55 fichiers téléchargés, MD5 conformes au manifeste ;
  taille totale 232 648 892 o (± tolérance d'arrondi nulle —
  la somme exacte est vérifiée).
- En-tête de chaque fichier = les 9 colonnes gelées (§4.1) ;
  60 660 lignes de gènes + 4 techniques ; sinon ARRÊT (§3).
- n ≥ 40 fichiers tumoraux (`tissue_type = Tumor` par
  l'association fichier → échantillon de l'API GDC, vérifiée
  avant le gel et re-vérifiée sur les cas téléchargés via le
  reçu d'association) ; sinon ARRÊT (§3).
- Aucun fichier porteur d'un code-barres TCGA ou déjà présent
  dans une cohorte du projet ; sinon ARRÊT (§3). (Caveat
  §2.2 point 2 : le non-recouvrement est établi par programme
  et système d'identifiants, pas par jointure.)
- KRAS présent comme ligne mappée (`gene_name` exact) dans
  chaque fichier retenu ; sinon ARRÊT (§3).
- Les 12 gènes v4 présents (une ligne chacun, symbole exact)
  dans chaque fichier retenu ; sinon ARRÊT (§3) (aucun gène
  remplacé, aucun absent toléré pour une paire comparable).
- Cas complets (KRAS + 12 gènes) ≥ 40 ; sinon ARRÊT (§3).

## 6. Runs v6.2 (mode fast)

- Lot : 2 runs — réel + nul — manifeste `manifest_v62_879.txt`,
  lanceur reprenable existant `run_v62_lot.sh` (saute les sorties
  déjà complètes), journal `runs_v62_879.log` (SHA du pipeline
  en tête, exits consignés).
- Dossiers : `results_fast_v62_879_gdc_organoid` et
  `results_fast_v62_879_gdc_organoid_nul` (nuls frais éventuels :
  `results_fast_v62_879_gdc_organoid_nul_s8791` /
  `..._s8792`).
- Lancement en `systemd-run --unit=v62-879 --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance qui
  s'arrête d'elle-même à 2/2 (ou 4/4 si nuls frais). Ne JAMAIS
  supprimer le dossier d'un run en cours. Si la machine
  redémarre, reprise sans perte (SKIP des dossiers complets,
  jamais de relance à l'aveugle).
- SHA du pipeline revérifié avant ET après le lot.
- Durée attendue : ~2–3 min par run (référence §8.76 :
  n=42, 12 flux, ~2 min/run) ; le lot complet tient en
  ~10 min hors téléchargement.

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
- **CONFIRME** : `d_maxsep > 0,07` — treizième paire
  indépendante passante.
- **PARTIEL** : `0 < d_maxsep ≤ 0,07` — positif mais sous le
  plancher (même catégorie que GSE71729, +0,0402, et GSE79668,
  +0,0567).
- **NON** : `d_maxsep ≤ 0` — négatif ou nul (même catégorie que
  GSE62452 et GSE21501).

**Ce que le verdict change (gelé) :**
- Si CONFIRME : A2 devient **9/13 au-dessus du plancher** (et
  11/13 positifs si le signe est positif — à compter sur les
  chiffres mesurés, pas à pré-écrire) ; LOO recalculé sur
  13 paires (pire cas sur 12).
- Si PARTIEL : A2 devient **8/13 au-dessus du plancher,
  11/13 positifs** ; LOO recalculé sur 13 paires.
- Si NON : A2 devient **8/13 au-dessus du plancher,
  10/13 positifs** ; LOO recalculé sur 13 paires.
- Dans tous les cas, la paire entre dans le compte A2 : c'est
  une paire principale indépendante (contrairement au lot FNA
  §8.76, apparié). **C3 reste LEVÉE** dans tous les cas — elle
  l'était déjà depuis le §8.71 ; ce chantier est une
  consolidation supplémentaire, pas une condition.
- Le leave-one-out sur les paires indépendantes est recalculé
  ici (il change : la paire y entre).

**Nuls frais (§4.5, règle gelée).** La paire graine 42 fait le
verdict, dans tous les cas. Si `d_maxsep` est PROCHE du
plancher — défini ici comme `d_maxsep` dans [−0,07 ; +0,14[,
soit à moins d'une largeur de plancher du seuil, de part et
d'autre — les 2 nuls frais (graines 8791, 8792) sont courus et
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
- Falsification : INDISPONIBLE sous n = 75 — GDC organoid
  n = 44 : noter « indisponible », ne pas imputer.
- Plancher équivalent-sep (descriptif) : la paire passe-t-elle
  aussi `0,07·(1+m_R)(1+m_N)` ? Rapporté, non décisif (D4 n'est
  pas rejoué ici : il porte sur les paires V1, déjà tranché).
- Aucun autre critère, aucune repondération, aucune redéfinition
  du plancher après avoir vu les chiffres.

## 8. Extraction et vérification

1. Extracteur propre du chantier, `extract_879.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_866.py` / `extract_869.py` / `extract_871.py` /
   `extract_874.py` / `extract_876.py`) ; lit `maxsep`,
   `mc_score`, `stability`, `ssep`, `delta`, `l7a`, cascade,
   falsification dans les 2 (ou 4) `master_results.json` ;
   sorties `extract_879.json` / `extract_879.csv`.
2. Second calcul indépendant : relecture directe des
   `master_results.json` par un chemin distinct (script
   `verify_879.py`, SHA noté) — `maxsep` et ancien MC recoupés
   à 0,0 exact ; tout écart = résultat à diagnostiquer, pas un
   bruit.
3. Recoupements : les 12 valeurs déjà comptées reprises telles
   quelles du §8.56 (table `sep_maxsep_856_table.json`, SHA
   `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`),
   du §8.69 (`extract_869.json`, SHA
   `644339e47b05e1445c1e78df053f9f8dc77a48e609a76a7f54b7aefd372d882b`),
   du §8.70 (`extract_870.json`, SHA
   `4ffa851a83668b2369097703862e0413ff9af54af3a66ef70aea9333b40c444f`),
   du §8.71 (`extract_871.json`, SHA
   `85e9089a…55e3b`) et du §8.74 (`extract_874.json`, SHA
   `82ade74701245021dfdb965bdc689ac98262c70f12ecec7f39e1b5b742dfcb47`),
   jamais recalculées ici — ce chantier ne re-vérifie pas les
   §8.56/§8.59/§8.64/§8.69/§8.70/§8.71/§8.74/§8.76 (déjà clos).
4. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 9. Tests directs en appui (ne décident pas)

Script `direct_tests_879.py` (SHA noté), sur les CSV de flux
du chantier (réel + nul graine 42) :
1. **Test informatif (correction §8.70, appliquée ici) :**
   corrélation de Spearman de chaque flux avec le pas (ordre
   KRAS), réel vs nul : |ρ| moyen, Δρ médian, nombre de Δρ
   positifs (sur 12), table complète sans sélection. C'est le
   test qui porte l'information d'ordre.
2. d de Cohen marginal des 12 flux (réel vs nul) : pour chaque
   gène v4, moyenne et écart-type des valeurs ordonnées, d de
   Cohen réel−nul ; table complète, sans sélection. **Attendu
   vacueux par construction : d = 0,0000 pour les 12 gènes**
   (le nul est une permutation des lignes, chaque flux garde
   exactement ses 44 valeurs). Rapporté tel quel : il valide
   la construction du nul (marginales préservées exactement),
   il ne mesure pas la séparation.
3. Comparaison descriptive avec les paires précédentes
   (Δρ médian, 10/12 positifs au §8.74 ; valeurs reprises
   telles quelles, jamais recalculées). Si le signal d'ordre
   est plus faible, c'est consigné tel quel, sans être élucidé
   sans preuve ; si une divergence Delta/`maxsep` apparaît
   ici, elle est nommée telle quelle.
4. Aucun de ces tests ne change le verdict du §7.

## 10. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et le
  jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict : les résultats des autres dépôts (écran du 20 nov.,
  holdout GSE57495, pilote Chen) ne prédisent rien ici — seul
  l'écart `maxsep` mesuré sur les runs du présent chantier fait
  le verdict.
- Un nul qui invalide une piste est un résultat ; un échec du lot
  est un verdict, pas un échec caché.
- Ne jamais présenter une lecture préliminaire comme un verdict.
- Aucun consensus exigé entre flux ou contrôles ; aucune
  affirmation clinique — l'étude porte sur l'instrument.
- **Compter cette paire comme treizième paire indépendante
  UNIQUEMENT si les portes du §5 sont passées** (44 fichiers
  tumoraux, 12/12 gènes, n ≥ 40). Toute lecture future qui
  compterait aussi les 11 fichiers Normal serait fausse.

## 11. Livrables

- Ce protocole (gelé avant téléchargement des données et runs).
- `PROVENANCE_879.md` (source, auteur, date, dépôt, URL, SHA-256
  du manifeste et de chaque fichier téléchargé, plateforme,
  effectifs, exclus, identification des gènes, vérifications
  d'indépendance du §2).
- `download_gdc_879.py` (téléchargement + vérification MD5) +
  reçus, `build_fluxes_879.py` + CSV de flux (`pdac_879_*`,
  SHA consignés).
- `manifest_v62_879.txt`, `runs_v62_879.log`, dossiers
  `results_fast_v62_879_*`, `extract_879.json` / `.csv`,
  `verify_879.py` + sortie de vérification,
  `direct_tests_879.py` + sortie.
- §8.79 dans le FICHIER SÉPARÉ
  `section_8.79_nouvelle_serie.md` (verdict d'abord, une phrase :
  CONFIRME / PARTIEL / NON ; chiffres ensuite ; détail complet
  après ; provenance nommée partout ; C3 reste levée dans tous
  les cas ; A2 recalculé sur 13 paires, dit explicitement).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin du protocole gelé §8.79. —
