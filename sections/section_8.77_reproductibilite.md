# §8.77 — Réparation de la reproductibilité : 19/19 gaps fermés, test à froid réussi — REPRODUCTIBILITÉ RÉPARÉE

## Verdict d'abord

**REPRODUCTIBILITÉ RÉPARÉE — les 19 fichiers bruts sans URL de
téléchargement consignée (DATA_SOURCES.md §17) ont TOUS retrouvé une URL
vérifiée par SHA-256, ainsi que le SOFT GPL20769 non conservé, le fichier
clinique du test C sans aucune provenance d'acquisition, l'URL reconstruite
de `mit_test.csv` et les URL directes des 4 fichiers CPTAC. Aucun gap
irrécupérable. Le script de re-téléchargement est corrigé (toutes les voies
cassées documentées remplacées, reprise après interruption, et il a été
exécuté en entier jusqu'à EXIT:0 — 52 fichiers, 2,4 Go, tous vérifiés).
Le test à froid le prouve de
bout en bout sur la paire principale TCGA v4 : tarball re-téléchargé par
le script corrigé, flux reconstruits SHA-IDENTIQUES aux flux tenus, et
runs v6.2 donnent les chiffres tenus à 0,0 exact sur les deux côtés
(cascade, MC, maxsep, S_sep, Delta, L7a, fals — voir §8.77.6).**

| Porte (PROTOCOL_reproductibilite_877.md, gelé) | Exigé | Mesuré 21 nov. 2026 | Sort |
|---|---|---|---|
| Gaps du §17 fermés (URL + SHA vérifié) | 19/19 | **19/19** (5 ng3398 + 5 Birnbaum + 2 ICGC + 1 PRISM 24Q2 meta + 4 PRISM 19Q4 + 2 QCMG) | **FERMÉ** |
| SOFT GPL20769 (taille + contenu) | 37 588 662 o, 19 749 lignes | **37 588 662 o, 19 749 lignes** (chemin corrigé `GPL20nnn/`) | **FERMÉ** |
| Clinique test C (provenance) | SHA vérifié ou IRRÉCUPÉRABLE déclaré | **SHA `0c274268…` vérifié** — provenance retrouvée (cBioPortal datahub) | **FERMÉ** |
| `mit_test.csv` (URL reconstruite) | SHA vérifié | **SHA `9f3ae189…` vérifié** | **FERMÉ** |
| CPTAC (URL directes) | 4/4 consignées | **4/4 lues dans l'API Zenodo, MD5 conformes** | **FERMÉ** |
| Script corrigé | voies cassées remplacées, `bash -n` OK | **`download_data_877.sh`, syntaxe OK, 323 lignes de diff** | **FAIT** |
| Script complet (~2,4 Go, 52 fichiers) | EXIT:0, tous fichiers vérifiés | **EXIT:0** (36 déjà présents et vérifiés + 16 OK frais, 0 erreur) | **PASSE** |
| Test à froid, flux reconstruits | SHA identiques aux flux tenus | **`e7a2adab…` et `895a4562…` identiques à l'octet** | **PASSE** |
| Test à froid, runs v6.2 | chiffres identiques aux chiffres tenus | **Identiques à 0,0 exact, réel et nul** (cascade, MC, maxsep, S_sep, Delta, L7a, fals) | **PASSE** |
| Aucune URL inventée | toute URL lue ou vérifiée par SHA | **0 URL sans vérification SHA** | **PASSE** |
| Aucun verdict rouvert | aucune section existante modifiée | **0 section modifiée, 0 verdict rouvert** | **PASSE** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que les dépôts
du projet sont désormais reconstructibles depuis zéro par un autre AI
sans rien deviner : chaque fichier brut a une URL de téléchargement
copiée depuis une source lue ou reconstruite puis vérifiée par son
SHA-256, et le script maître corrigé les re-télécharge tous avec
vérification. Il dit que la lacune de provenance la plus grave du projet
— le fichier clinique du test C, sans aucune provenance d'acquisition —
est close : le fichier est celui de l'étude cBioPortal
`paad_tcga_pan_can_atlas_2018`, et le pointeur Git LFS lui-même porte
son SHA. Il dit que le test à froid reconstruit la paire TCGA v4 à
l'octet près depuis un re-téléchargement propre, et que les runs v6.2
redonnent les chiffres tenus à 0,0 exact des deux côtés
(d_maxsep froid +0,29276219, égal au tenu). Il ne dit pas que les verdicts du livre blanc sont
« prouvés » par ce chantier : ce chantier ne mesure rien sur le cancer,
il répare la traçabilité — les verdicts restent exactement ce qu'ils
étaient, avec les mêmes chiffres et les mêmes réserves. Il ne dit pas
que tout le projet tient dans le dépôt GitHub : les matrices brutes
(~2,4 Go) et les résultats `results_fast_*` (~7 Go) restent hors dépôt
par limite snapshot — ils se re-téléchargent et se reconstruisent, ce qui
est précisément ce que ce chantier vérifie. Il ne dit rien de clinique.

**Fragilité, dite en tête.** Le verdict tient à des vérifications SHA,
c'est-à-dire à des comparaisons d'octets — la forme de preuve la plus
forte de ce dossier, et la plus étroite. Trois fragilités précises. (1)
Une URL vérifiée aujourd'hui peut mourir demain : figshare, Zenodo,
Springer, le FTP GEO, le hub Xena et le dépôt datahub sont des services
tiers, et ce chantier ne contrôle aucun d'eux. Ce qui est garanti, c'est
l'état du 21 nov. 2026 et les SHA qui permettent de détecter tout
changement — pas la pérennité des liens. (2) Le test à froid ne couvre
qu'une paire (TCGA v4, réel + nul) : il prouve la chaîne complète sur
cette paire, pas sur les 12 paires ni sur les 140 runs. Les autres
sources sont vérifiées fichier par fichier (SHA), pas par re-run — c'est
la limite honnête du test, écrite dans le protocole gelé avant les runs.
(3) Le script complet a échoué une fois pendant ce chantier sur un HTTP
403 transitoire de figshare (§8.77.5) : le correctif appliqué
(`--retry-all-errors`) durcit les réessais, il ne supprime pas la
possibilité qu'un fournisseur bloque un téléchargement un jour donné.
Ces trois fragilités ne rouvrent aucun gap : elles disent ce que la
réparation garantit, et jusqu'où.

Protocole gelé : `PROTOCOL_reproductibilite_877.md` (21 nov. 2026,
01h37 UTC, SHA `dbe1746f7233e69a3052407576ebf6043080016c97a12d41f76244fc569a4030`,
inchangé). Critère de succès écrit AVANT tout travail de récupération
(§0.5 du protocole) ; aucune URL ajoutée après coup sans vérification
SHA ; aucun gap déclaré fermé sur une promesse. Pipeline v6.2 SHA
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant le gel et après chaque lot de runs, inchangé ; le code
n'a jamais été modifié). Dossier de travail :
`~/workspace/runs/pdac-v6/repro_877/` (re-téléchargements dans
`repro_877/downloads/`, test à froid dans `repro_877/cold/`, journal
`repro_877/JOURNAL_877.md`).

## 8.77.1 — L'état des lieux : ce qui manquait, et pourquoi c'était grave

**Le constat (20 nov. 2026, 19h38, DATA_SOURCES.md §17).** Les dépôts
étaient « partiellement reproductibles depuis zéro » : le livre blanc,
le pipeline v6.2, les flux et les protocoles sont dans les dépôts et les
runs sont déterministes — mais 19 fichiers bruts n'avaient pas d'URL de
téléchargement consignée, le fichier clinique du test C n'avait AUCUNE
provenance d'acquisition, et le script de re-téléchargement avait des
voies cassées. Autrement dit : un autre AI pouvait relire ce qui avait
été fait, mais pas tout reconstruire depuis zéro sans deviner — et
deviner une URL, c'est exactement ce que la règle de provenance (27 oct.
2026) interdit.

**Les 19 fichiers, par groupe (DATA_SOURCES.md §17).**

| Groupe | Fichiers | Ce qui manquait |
|---|---|---|
| Suppléments Nature Moffitt ng3398 (MOESM59–63) | 5 | URL de téléchargement (noms, tailles, SHA tronqués seulement) |
| Suppléments Springer Birnbaum (MOESM1–5) | 5 | URL de téléchargement (« via static-content Springer », sans URL) |
| ICGC probe map + NMF (Xena) | 2 | URL exacte (jeux nommés, URL non consignée littéralement) |
| PRISM 24Q2 métadonnées lignées | 1 | URL (n° de fichier figshare non consigné ; absent du script) |
| PRISM 19Q4 (4 fichiers) | 4 | URL directe par fichier (accès via API seulement) |
| QCMG clinique patient + échantillon | 2 | URL exacte (« fichier clinique datahub », sans URL) |

**Hors des 19, quatre gaps nommés en plus.** Le SOFT GPL20769
(37 588 662 o, téléchargé le 15 nov. 2026, non conservé, URL non
consignée) ; le fichier clinique du test C
(`data_clinical_patient.txt`, 58 621 o, hors de `data/`, sans aucune
provenance — la lacune la plus grave, §11 et §15.6) ; l'URL reconstruite
de `mit_test.csv` (PANC-1, « à vérifier avant usage », §10). Et les 4
fichiers CPTAC, accessibles uniquement via l'API Zenodo (page du record
consignée, pas d'URL par fichier, §6).

**Les voies cassées du script (DATA_SOURCES.md §0.1).** Le tarball
PANC-1 tronqué (569 815 185 o, gzip « unexpected end of file ») ; PRISM
19Q4 2/4 fichiers ; suppléments non téléchargés ; SOFT GPL20769 non
conservé ; PRISM 24Q2 primaire sans vérification de hachage
(`check … - -`). La réparation a été reportée à la demande de Zackary
(20 nov. 2026, 19h40) jusqu'à la fin du lot §8.74/§8.75, et menée comme
une section à part, sans toucher à l'état actuel — c'est ce chantier.

## 8.77.2 — Méthode : retrouver sans inventer

**La règle, appliquée gap par gap.** Pour chaque gap : retrouver l'URL
depuis une source lue (page DOI, FTP GEO, API figshare, hub Xena,
dépôt datahub) — jamais inventée. Une URL reconstruite (patron
d'URL déduit d'un cas attesté) n'est acceptée que si le fichier
re-téléchargé vérifie le SHA-256 consigné : le SHA est le juge, pas le
patron. Un gap dont l'URL ne vérifie pas reste ouvert, ou est déclaré
IRRÉCUPÉRABLE avec sa raison. Les fichiers locaux originaux de `data/`
n'ont jamais été écrasés ni déplacés : la comparaison se fait par SHA,
pas par remplacement.

**Les sources lues.** Page PMC de Birnbaum et al. 2017 (PMC5674743, DOI
10.1186/s12943-017-0739-z) ; page Nature de Moffitt et al. 2015
(ng.3398) ; API figshare des articles 25917643 (PRISM 24Q2) et 9393293
(PRISM 19Q4) ; API Zenodo du record 8394329 (CPTAC) ; API GitHub du
dépôt `cBioPortal/datahub` (dossiers `public/paad_qcmg_uq_2016` et
`public/paad_tcga_pan_can_atlas_2018`) ; hub Xena ICGC
(`icgc.xenahubs.net`) ; FTP GEO (`ftp.ncbi.nlm.nih.gov/geo/platforms/`) ;
réponses JSON de l'API GitHub ncats/PANC1 (déjà détenues).

**Les voies infructueuses, consignées (aucune n'a été passée sous
silence, aucune ne cache un gap restant).**

1. **Listing du bucket S3 Xena : HTTP 403.** Le bucket
   `icgc-xena-hub` n'autorise pas le listage. Les URL S3 directes des
   fichiers ICGC renvoient 403 aussi — c'est l'URL du hub
   (`icgc.xenahubs.net/download/…`) qui fonctionne (le hub redirige
   vers le bucket).
2. **Europe PMC `supplementaryFiles` pour PMC5674743 : HTTP 500**
   (page HTML d'erreur, 19 606 o). Les suppléments Birnbaum ont été
   récupérés par le patron Springer direct, vérifié par SHA.
3. **Page Nature ng.3398 via curl : HTTP 303**, section suppléments non
   lisible par ce moyen. La page lue par le navigateur confirme le titre
   et l'article ; les URL ont été vérifiées par SHA.
4. **Chemin FTP GEO `GPL2nnn/GPL20769/` : 404.** Le bon chemin est
   `GPL20nnn/` — le regroupement GEO masque les 3 derniers chiffres
   (20769 → `GPL20nnn`, comme 6244 → `GPL6nnn` au §4.1 de
   DATA_SOURCES.md). Le chemin deviné au §15.4 était faux ; le chemin
   vérifié le remplace.
5. **`raw.githubusercontent.com` pour les fichiers datahub : renvoie le
   pointeur Git LFS (130 o), pas le contenu.** Le contenu réel est servi
   par `media.githubusercontent.com`. Détail décisif au §8.77.4.

## 8.77.3 — Résultats gap par gap : 19/19 fermés

**Toutes les vérifications ci-dessous sont des comparaisons taille +
SHA-256 (ou MD5) entre le fichier re-téléchargé le 21 nov. 2026 dans
`repro_877/downloads/` et le SHA consigné dans DATA_SOURCES.md ou dans
la provenance. « FERME » veut dire : URL retrouvée depuis une source
lue + fichier re-téléchargé + SHA identique.**

### ng3398 MOESM59–63 — 5/5 FERMÉS

Patron Springer, code revue 41588 (*Nature Genetics*), attesté par le
fichier Bailey MOESM270 déjà consigné au §5.5 :
`static-content.springer.com/esm/art%3A10.1038%2Fng.3398/MediaObjects/41588_2015_BFng3398_MOESM{n}_ESM.{ext}`.

| Fichier | Taille (o) | SHA-256 re-téléchargé | Conforme §3.2 |
|---|---|---|---|
| `ng3398_MOESM59_ESM.pdf` | 5 339 711 | `c18dbc59…320c0` | Oui |
| `ng3398_MOESM60_ESM.txt` | 19 393 438 | `516cf2eb…4c7db` | Oui |
| `ng3398_MOESM61_ESM.xlsx` | 460 785 | `ec26858b…1c01ad` | Oui |
| `ng3398_MOESM62_ESM.xlsx` | 2 612 836 | `25c35346…08b5c` | Oui |
| `ng3398_MOESM63_ESM.xlsx` | 14 141 | `3d508a54…20905` | Oui |

### Birnbaum MOESM1–5 — 5/5 FERMÉS

Article : Birnbaum et al. 2017, « Validation and comparison of the
molecular classifications of pancreatic carcinomas », *Mol Cancer*
16:174, DOI `10.1186/s12943-017-0739-z`, PMID 29110659 (page PMC5674743
lue ; le DOI n'était pas relevé dans les fichiers — il l'est désormais).
Patron Springer :
`static-content.springer.com/esm/art%3A10.1186%2Fs12943-017-0739-z/MediaObjects/12943_2017_739_MOESM{n}_ESM.xlsx`.

| Fichier | Taille (o) | SHA-256 re-téléchargé | Conforme §13 |
|---|---|---|---|
| `birnbaum_springer_MOESM1.xlsx` | 11 209 | `3d9df7b9…f4945b` | Oui |
| `birnbaum_springer_MOESM2.xlsx` | 15 240 | `721e19d9…77c3` | Oui |
| `birnbaum_springer_MOESM3.xlsx` | 9 119 | `8bfbdcd6…6b1a13` | Oui |
| `birnbaum_springer_MOESM4.xlsx` | 15 040 | `49fff4c8…df361` | Oui |
| `birnbaum_springer_MOESM5.xlsx` | 8 767 | `94af1f73…db6ccb` | Oui |

(La taille de MOESM5, 8 767 o, correspond aux « 8.6KB » affichés sur la
page PMC pour « Additional file 5: Table S5 » — recoupement indépendant
du patron.)

### ICGC probe map + NMF — 2/2 FERMÉS

| Fichier | URL (hub Xena) | Taille (o) | SHA-256 | Conforme |
|---|---|---|---|---|
| `icgc_pacaau_probemap.gz` | `https://icgc.xenahubs.net/download/PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp.gz` | 353 314 | `b09a746f…75537` | §5.3 Oui |
| `icgc_pacaau_nmf.txt.gz` | `https://icgc.xenahubs.net/download/PACA-AU/nature16965-s2_NMF_class_assignment.txt.gz` | 447 | `f1e84b99…21e2f` | §5.4 Oui |

Note : le fichier distant est bien `.txt.gz` — le `.txt` nu renvoie 404
sur le hub. Le fichier local est donc nommé correctement.

### PRISM 24Q2 métadonnées — 1/1 FERMÉ

API figshare lue (`https://api.figshare.com/v2/articles/25917643`) :
fichier 46630978, `Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv`,
URL `https://ndownloader.figshare.com/files/46630978`. Re-téléchargé :
157 294 o, SHA-256 `13a85da9e45656c455d3911a4491f3636d7d0975a9d2333dc3d0a3e2cd3b0526`
= §7. Ajouté au script corrigé avec vérification.

### PRISM 19Q4 — 4/4 FERMÉS (URL directes désormais consignées)

API figshare lue (`https://api.figshare.com/v2/articles/9393293`) :
les 4 `download_url` directs ont été relevés et les 4 fichiers
re-téléchargés et vérifiés.

| Fichier | URL directe (fichier figshare) | Taille (o) | MD5 | SHA-256 | Conforme §8 |
|---|---|---|---|---|---|
| `secondary-screen-dose-response-curve-parameters.csv` | `…/files/20237739` | 264 340 589 | `e629b9d5…` | `88d10135…fec8` | Oui |
| `secondary-screen-replicate-collapsed-treatment-info.csv` | `…/files/20237763` | 3 788 355 | `54765b36…` | `9d0d1fb4…84f7` | Oui |
| `secondary-screen-cell-line-info.csv` | `…/files/20237769` | 40 979 | `6737b4aa…` | `b93436b5…8d27` | Oui |
| `secondary-screen-readme.txt` | `…/files/20238123` | 7 647 | `421d0bba…` | `ed453e2b…9c99` | Oui |

(Le fichier dose-response, 264 Mo, a été téléchargé en unité systemd
dédiée `repro877-dose-response`, Result=success, exit 0 — il ne
transitait pas par un appel d'outil interactif.)

### QCMG clinique — 2/2 FERMÉS

Dépôt GitHub `cBioPortal/datahub`, étude `paad_qcmg_uq_2016`, dossier
listé par l'API GitHub. Contenu réel via `media.githubusercontent.com`
(remarque LFS au §8.77.4).

| Fichier | Taille (o) | SHA-256 | Conforme §12 |
|---|---|---|---|
| `qcmg_clinical_patient.txt` | 49 042 | `ae7fc6d7…6a95` | Oui |
| `qcmg_clinical_sample.txt` | 57 215 | `c70daf3e…ceca` | Oui |

Rappel : ces fichiers restent ÉCARTÉS pour les verdicts (non utilisés,
§12) — la récupération ne change rien à leur statut, elle ne fait que
fermer le gap de provenance.

### SOFT GPL20769 — FERMÉ (taille + contenu)

URL : `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL20nnn/GPL20769/soft/GPL20769_family.soft.gz`.
Re-téléchargé le 21 nov. 2026 : **37 588 662 o exactement** (= §3.1 à
l'octet), table **19 750 lignes = en-tête + 19 749 lignes** (= §3.1),
titre de plateforme confirmé (« Agilent-014850 Whole Human Genome
Microarray 4x44K G4112F (Gene Symbol Version; updated July 2014) »).
MD5 `4c39e802ec78170d7ed5c8c2cc2b0bec`, SHA-256
`ecb1b79a6b89e521a1116a3113fcb9a5af1c181329eec8257e044e0683822d3e`
(nouveaux, à consigner — aucun hachage n'était consigné pour ce fichier).

### `mit_test.csv` (PANC-1) — FERMÉ (URL reconstruite, vérifiée)

URL reconstruite `https://raw.githubusercontent.com/ncats/PANC1/main/MIT/test.csv`
(§10). Re-téléchargée : 3 249 228 o, SHA-256
`9f3ae18976136412802831487b6187fcf062db8f4ca753990689d3ac62006e27` = §10.
La mention « à vérifier avant usage » est levée.

### CPTAC — 4/4 URL directes consignées

API Zenodo lue (`https://zenodo.org/api/records/8394329`) : les 4
fichiers sont présents, tailles et MD5 conformes au §6. URL directes
(champ `links.self`) désormais consignées au §6 et en commentaire dans
le script corrigé :

| Fichier | MD5 (conforme §6) |
|---|---|
| `umich-pdac-proteomics-Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz` | `a8c89b79…ac676` |
| `bcm-pdac-proteomics-PDAC_proteomics_gene_abundance_log2_reference_intensity_normalized_Tumor.txt.gz` | `988150c2…0c06d2` |
| `umich-pdac-mapping-aliquot_to_patient_ID.tsv.gz` | `b013fad4…36754` |
| `cptac_genes.csv` | `afc25079…72f62a` |

Le script conserve le téléchargement via l'API (qui fonctionne) ; les
URL directes sont consignées pour la traçabilité.

## 8.77.4 — La fermeture la plus grave : le fichier clinique du test C

**Le gap.** `data_clinical_patient.txt` (58 621 o, hors de `data/`, à la
racine de `pdac-v6/`) était le fichier du test C (§8.45, ordre des 178
tumeurs TCGA par stade AJCC) — et il n'avait AUCUNE provenance
d'acquisition : déjà sur le disque au début du chantier (15 nov. 2026,
15h13 UTC), aucune entrée dans aucun journal de téléchargement, premier
hachage consigné dans `PROVENANCE_testC_stage.md`. Le test C était donc
le seul verdict du livre blanc dont la source brute n'était pas
re-téléchargeable depuis une source connue. Son verdict n'a jamais été
contesté sur ses chiffres — mais sa reproductibilité était limitée, et
c'était la lacune la plus grave du projet pour la reconstruction.

**L'hypothèse testée, pas affirmée.** Le format `data_clinical_patient.txt`
est le format cBioPortal, et l'étude PanCanAtlas PAAD existe sur
cBioPortal (`paad_tcga_pan_can_atlas_2018`). Le dossier correspondant a
été listé dans le dépôt `cBioPortal/datahub` par l'API GitHub (contenu
du dossier lu, pas deviné), et le fichier candidat téléchargé.

**La vérification, en deux temps.**

1. Le contenu réel, servi par `media.githubusercontent.com`
   (`https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_tcga_pan_can_atlas_2018/data_clinical_patient.txt`),
   fait 58 621 o et son SHA-256 est
   `0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5` —
   **identique au SHA consigné au §11**.
2. **Double confirmation par le pointeur LFS lui-même.** Les fichiers de
   ce dépôt sont en Git LFS : le `download_url` de l'API GitHub
   (`raw.githubusercontent.com/…`) renvoie un pointeur de 130 o, pas le
   contenu — et ce pointeur porte lui-même :
   `oid sha256:0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5`
   et `size 58621`. Le dépôt déclare donc lui-même, dans son pointeur,
   que le fichier qu'il sert a exactement ce SHA et cette taille.

**Ce que cela change, et ce que cela ne change pas.** La provenance
d'acquisition du fichier clinique du test C est désormais : dépôt GitHub
`cBioPortal/datahub`, étude `paad_tcga_pan_can_atlas_2018`, URL exacte
ci-dessus. Le test C devient re-téléchargeable et vérifiable depuis une
source connue. **Le verdict du test C est inchangé** (il reste ce qu'il
est au §8.45 : NON — le bloc estomac/mucus monte avec le stade au lieu
de s'effondrer, MUC16 est plat) : seule sa reproductibilité est réparée.
C'est exactement la règle de la section à part — réparer la traçabilité
sans réécrire l'histoire.

## 8.77.5 — Le script corrigé

**Fichier livré :** `repro_877/download_data_877.sh` (SHA-256
`558111360ceda48bece577d7176a5ad5e46630f0a39fc85c03e8c3635564c78f`,
diff `repro_877/download_data_877.diff`, 323 lignes changées).
L'original `~/workspace/staging-pdac/download_data.sh` (SHA
`4e151d59…`) n'a pas été modifié par ce chantier ; la copie corrigée est
livrée au coordinateur avec son diff. `bash -n` : syntaxe OK.

**Les corrections, une par une (chaque ancienne voie est nommée avec la
raison de son échec — l'historique n'est pas effacé, il est documenté).**

| # | Correction | Ancienne voie et pourquoi elle était cassée |
|---|---|---|
| 1 | PANC-1 fichier par fichier (8 fichiers + `mit_test.csv`), vérification taille + SHA-256 par fichier | Tarball `codeload.github.com/ncats/PANC1/tar.gz/refs/heads/main` : tronqué en pratique (569 815 185 o, gzip « unexpected end of file ») |
| 2 | PRISM 19Q4 : 2 fichiers ajoutés au dictionnaire `want` + 4 URL directes en commentaire | Le script ne téléchargeait que 2 des 4 fichiers |
| 3 | PRISM 24Q2 primaire : vérification SHA-256/MD5 ajoutée + métadonnées des lignées ajoutées | Le script passait `check … - -` (aucun hachage vérifié) |
| 4 | Suppléments ng3398 (MOESM59–63) et Birnbaum (MOESM1–5) : sections ajoutées, vérification taille + SHA-256 | Non téléchargés par le script d'origine (URL non consignées) |
| 5 | SOFT GPL20769 : section ajoutée, vérification taille exacte + SHA-256 | Non conservé, URL non consignée ; de plus l'ancien chemin deviné `GPL2nnn/` donne 404 (le bon est `GPL20nnn/`) |
| 6 | ICGC probe map + NMF, QCMG clinique, clinique PanCanAtlas : sections ajoutées, vérification taille + SHA-256 | URL non consignées (jeux nommés / « fichier clinique datahub » / provenance manquante) |
| 7 | CPTAC : URL directes consignées en commentaire | Voie API conservée (elle fonctionne) ; URL directes ajoutées pour la traçabilité |
| 8 | Durcissement : `--retry-all-errors --retry-delay 5` sur tous les appels curl (`get()` et les deux blocs python) | Voir l'incident (1) ci-dessous : curl ne réessaie pas les 403 par défaut |
| 9 | OmicsCNGene.csv : endpoint API figshare remplacé par ndownloader (même fichier, ID 51065324) | L'endpoint API est resté bloqué à 0 octet pendant 9+ min (voir incident (2)) ; ndownloader servait le fichier immédiatement (test range : HTTP 206, 672 Ko/s) |
| 10 | Anti-blocage : `--speed-limit 1000 --speed-time 300` sur `get()` | Deux connexions sont restées bloquées à 0 o/s sans jamais échouer (voir incident (2)) — sans limite de vitesse, curl attend indéfiniment et `--retry` ne se déclenche jamais |
| 11 | ICGC expression : URL S3 directe remplacée par l'URL du hub (même fichier, SHA identique) | La S3 directe renvoie HTTP 403 (4 tentatives, exécution full5 — voir incident (3)) |
| 12 | Reprise : `get_checked()` remplace les 44 paires `get` + `check` (fichier déjà présent et vérifié sauté, fichier partiel/corrompu re-téléchargé) | Le script complet a été interrompu 3 fois (incidents (2)–(4)) ; sans reprise chaque incident coûtait ~30 min de re-téléchargement intégral |

**Les incidents du script complet (consignés, pas maquillés).** Le script
complet a demandé 9 exécutions avant EXIT:0 — chacune a fait avancer le
diagnostic, aucune n'a été effacée.

1. **Le 403 transitoire.** La première exécution s'est arrêtée au TOUT
   PREMIER fichier (CRISPRGeneEffect.csv, `ndownloader.figshare.com`)
   sur un HTTP 403, après ~90 s à 0 octet ; le script s'arrête
   (`set -e`) et le journal `cold/full_script_877.log` se termine par
   `curl: (22) … 403` / `EXIT:22`. Quelques minutes plus tard, la même
   URL répondait 302 (redirection normale vers S3). Cause probable :
   limitation de débit figshare après ~10 téléchargements rapprochés
   dans ce chantier. Ce n'est pas une voie cassée du script : c'est un
   refus transitoire du fournisseur. Correctif : item 8.
2. **Les blocages à 0 octet (API figshare, GDAC) — le diagnostic
   principal.** La relance (full2) s'est bloquée 9+ min à 0 octet sur
   OmicsCN via l'endpoint API figshare ; la suivante (full3) 13+ min à
   0 octet sur le tarball GDAC PAAD RSEM ; la suivante (full4) 3
   tentatives de 5 min chacune sur le même tarball. Les tests directs
   prouvaient pourtant que les hôtes fonctionnaient (GDAC : HTTP 206 à
   768 Ko/s en range, puis 15 Mo en 7 s à 2,17 Mo/s en GET complet ;
   ndownloader : HTTP 206 à 672 Ko/s). Le test décisif : un curl GDAC
   lancé DANS une unité systemd donne HTTP 000, timeout 30 s, et un
   curl API figshare pareil — alors que le même curl depuis l'outil
   exec télécharge en quelques secondes. **Cause : les unités systemd
   lancées par `systemd-run` n'héritent PAS des variables proxy de
   l'environnement d'exécution.** En accès direct (sans proxy),
   `ndownloader.figshare.com` fonctionne, mais `api.figshare.com` et
   `gdac.broadinstitute.org` restent bloqués à 0 octet. Ce n'est donc
   pas un défaut des hôtes ni du script : c'est un artefact de la
   méthode de lancement. Les lots longs doivent être lancés AVEC le
   proxy (`systemd-run --setenv=https_proxy=http://hatch-egress-proxy:3128
   --setenv=http_proxy=http://hatch-egress-proxy:3128` — sans
   identifiants : le proxy fonctionne sans). Le script lui-même ne code
   pas le proxy en dur (c'est propre à l'environnement d'exécution).
   Correctifs : items 9 et 10.
3. **Le 403 S3 ICGC — un défaut du script corrigé, trouvé par le
   test.** L'exécution full5 (avec proxy) : 12 fichiers OK, puis arrêt
   sur l'URL S3 directe de l'expression ICGC
   (`icgc-xena-hub.s3.amazonaws.com/…/nature16965-s2_normalised_exp.txt.gz`,
   HTTP 403, 4 tentatives, EXIT:22). Cause : le script corrigé gardait
   la section ICGC d'origine avec l'URL S3 directe, alors que la
   section ajoutée (probe map + NMF) utilisait déjà le hub. L'URL du
   hub pour le même fichier
   (`icgc.xenahubs.net/download/PACA-AU/nature16965-s2_normalised_exp.txt.gz`)
   fonctionne (302 vers le bucket) : 9 841 881 o, SHA-256 identique au
   consigné. Correctif : item 11. DATA_SOURCES §5.2 mis à jour
   (ancienne URL S3 marquée 403, ne plus utiliser).
4. **Le redémarrage machine.** L'exécution full6 (avec proxy) : 27
   fichiers OK, puis la machine a redémarré (~03:18–03:22 UTC) pendant
   le téléchargement PANC-1 `calc.csv` (curl 52, en retry) ; l'unité
   transiente n'a pas survécu, aucune ligne EXIT dans le journal
   `cold/full_script_877f.log` (coupé net). Correctif : item 12
   (reprise).
5. **Le blocage PANC-1 `calc.csv` — cause exacte non élucidée.**
   L'exécution full7 (avec proxy) : 27 fichiers OK, puis `calc.csv`
   (24 780 o) bloqué à 0 octet, 4 tentatives toutes tuées par le
   speed-limit. Le même fichier se télécharge en 0,3–1,3 s depuis
   l'outil exec — avec proxy authentifié, sans identifiants, en IPv4
   comme en IPv6 — et le curl bloqué de l'unité avait pourtant les
   bonnes variables proxy (vérifié dans `/proc/PID/environ`) et une
   connexion ESTABLISHED vers le proxy. Consigné comme tel : les tests
   directs prouvent que l'URL et l'hôte fonctionnent. La reprise depuis
   l'outil exec a passé sans difficulté.

**Deux fautes de frappe dans des SHA consignés, trouvées par le test.**
La reprise 877h s'est arrêtée sur `birnbaum_springer_MOESM3.xlsx` :
SHA-256 INCORRECT. Enquête : le fichier re-téléchargé (9 119 o) porte
`8bfbdcd618ea2a9d9b8ae480c763b857c3e23e2022462ab61cff0aaa8c6b1a13`
(64 car.), IDENTIQUE au fichier local d'origine (16 nov. 2026) et au
fichier vérifié à 01:40 — trois téléchargements indépendants d'accord.
La valeur consignée au §13 et recopiée dans le script ne faisait que
62 caractères (`…a9b8ae…` au lieu de `…a9d9b8ae…`) : faute de frappe dans
la consignation, que la comparaison par SHA tronqués
(`8bfbdcd6…6b1a13`) n'avait pas vue. Le fichier est bon ; c'est la
consignation qui était fausse. Corrigé dans DATA_SOURCES §13 et dans le
script. Balayage systématique ensuite : une deuxième faute, préexistante
(19 nov. 2026) — SHA-256 LUAD §2.3 consigné sur 65 caractères
(`…cf73f1daf2`, un `d` en trop) ; vrai SHA `…cf73f1af2`, vérifié sur le
fichier local et le re-téléchargement à froid, identiques. Corrigé dans
DATA_SOURCES §2.3. Aucune autre chaîne hex suspecte dans le script
(balayage : 0) ni dans DATA_SOURCES (après correction). **Le test du
script complet a donc déjà servi : il a attrapé une erreur latente que
les comparaisons tronquées avaient manquée.**

**Ce qui a été testé, et ce qui ne l'a pas été.** Chaque NOUVELLE section
du script a été testée individuellement pendant ce chantier (chaque
fichier re-téléchargé et vérifié par SHA — c'est le §8.77.3). La section
TCGA a été testée par l'extrait littéral `cold/cold_tcga.sh` (§8.77.6).
Le script complet (~2,4 Go, 52 fichiers) a été exécuté en entier jusqu'à
EXIT:0 — voir §8.77.6 étape 4 pour le résultat.

## 8.77.6 — Test à froid : la paire TCGA v4, du re-téléchargement au run

**Chiffres tenus (v6.2, validation §8.37, rep1 = rep2 à l'octet), extraits
le 21 nov. 2026 par `extract_858.extract` sur `results_fast_v62_tcga_v4`
et `results_fast_v62_tcga_v4_nul`.**

| | Réel (TCGA v4) | Nul (graine 42) |
|---|---|---|
| Flux CSV (SHA) | `pdac_tcga_fluxes_v4.csv`, `e7a2adab…0b0` | `pdac_tcga_fluxes_v4_nul.csv`, `895a4562…da4` |
| n | 178 | 178 |
| Cascade (%) | [0,0 ; 74,0617 ; 93,2217 ; 98,4358 ; 98,9572] | [0,0 ; 10,6496 ; 15,9571 ; 67,119 ; 67,119] |
| MC | 0,3720465146241378 | 0,326773250583873 |
| maxsep | 0,46234232096887146 | 0,1695801283296793 |
| S_sep | 0,4548206606358036 | 0,1687743461786773 |
| Delta | 4,181387 | 3,765664 |
| L7a | down 0,4051910172618019 | up 0,16715778704330952 |
| fals | 0,849386 | 0,642205 |
| `master_results.json` (SHA) | `1506f23d…df76` | `0d939a40…c5a` |

d_maxsep tenu : **+0,29276219**.

**Étape 1 — re-téléchargement par le script corrigé.** Extrait littéral
de la section TCGA du script corrigé (`cold/cold_tcga.sh`, mêmes
commandes `get`/`check`) : les 4 tarballs téléchargés et vérifiés (MD5
conformes) ; PAAD RSEM SHA-256 `c3dd138b3257ad5bae5a58160f5607d2ad9c2871c83f6cdb5959cc9116d262c9`
= §2.1. Dossier propre `repro_877/cold/data`, rien dans `pdac-v6/` n'a
été touché.

**Étape 2 — reconstruction des flux.** Copie de `build_fluxes_tcga_v4.py`
dans `repro_877/cold/` avec pour SEULES différences les deux constantes
de chemins (`DATA`, `OUT` — diff consigné) ; original intact. Exécutée
sur le tarball froid : flux reconstruits **SHA-IDENTIQUES** aux flux
tenus — `pdac_tcga_fluxes_v4.csv` `e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0`
et `pdac_tcga_fluxes_v4_nul.csv`
`895a456295d2b0553a2a62910461aedecb1aeccca59f57751c87b75ce0b97da4`.
La chaîne téléchargement → reconstruction est bit-à-bit fidèle.

**Étape 3 — runs v6.2 (21 nov. 2026, 01h44–01h51 UTC).** Commandes :
`python3 /home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py --input <flux_froid>.csv --mode fast --output results_fast_cold_tcga_v4[_nul]`,
depuis `repro_877/cold/`, unité systemd `repro877-cold-runs` (lanceur
reprenable `cold/run_cold_877.sh`, journal `cold/runs_cold_877.log` :
réel EXIT 0, nul EXIT 0, FIN 01h51:36Z, SHA v6.2 avant = après =
`f07567c4…`). Extraction par `extract_858.extract` (original intact,
via `cold/extract_cold_877.py` ; `extract_cold_877.json` /
`extract_cold_877.csv`). Comparaison au champ près des deux
`master_results.json` (tenu vs froid, NaN traités comme égaux) :

| | Réel froid | Réel tenu | Écart | Nul froid | Nul tenu | Écart |
|---|---|---|---|---|---|---|
| Cascade (%) | [0,0 ; 74,0617 ; 93,2217 ; 98,4358 ; 98,9572] | [0,0 ; 74,0617 ; 93,2217 ; 98,4358 ; 98,9572] | **0,0** | [0,0 ; 10,6496 ; 15,9571 ; 67,119 ; 67,119] | [0,0 ; 10,6496 ; 15,9571 ; 67,119 ; 67,119] | **0,0** |
| MC | 0,3720465146241378 | 0,3720465146241378 | **0,0** | 0,326773250583873 | 0,326773250583873 | **0,0** |
| maxsep | 0,46234232096887146 | 0,46234232096887146 | **0,0** | 0,1695801283296793 | 0,1695801283296793 | **0,0** |
| S_sep | 0,4548206606358036 | 0,4548206606358036 | **0,0** | 0,1687743461786773 | 0,1687743461786773 | **0,0** |
| Delta | 4,181387 | 4,181387 | **0,0** | 3,765664 | 3,765664 | **0,0** |
| L7a | down 0,4051910172618019 | down 0,4051910172618019 | **0,0** | up 0,16715778704330952 | up 0,16715778704330952 | **0,0** |
| fals | 0,849386 | 0,849386 | **0,0** | 0,642205 | 0,642205 | **0,0** |

d_maxsep froid : **+0,2927621926391921** (tenu +0,29276219 — identique).
Critère gelé (tolérance 0,0 exact) : **PASSE**.

**Lecture honnête des écarts qui existent.** Les deux
`master_results.json` froids n'ont pas le même SHA-256 que les tenus
(réel froid `59dec82b…47ab2`, tenu `1506f23d…df76` ; nul froid `26e79888…40e68`,
tenu `0d939a40…`). La comparaison au champ près montre que les seuls
champs divergents sont des diagnostics d'environnement et des chemins,
jamais des résultats : 18 champs pour le réel, 8 pour le nul — tous des
`worker_budget` / `n_workers` / `chunksize` / `available_memory_bytes`
(la mémoire disponible au moment du run différait : 3 workers tenus
contre 2 froids pour le réel, et inversement 1,6 Go tenus contre 6,9 Go
froids pour le nul, le téléchargement complet tournant en parallèle) et
les chemins `runtime.dashboard_status.path` / `runtime.telemetry_path`
(nom du dossier de sortie, différent par construction). Deux champs
`Q6 … MUC2_SingularityFmax_mean` valent NaN des deux côtés (comparaison
NaN ≠ NaN, artefact — valeurs identiques). **Aucun champ scientifique
ne diverge.** C'est le comportement attendu d'un re-run dans un autre
dossier, sur une machine dont la charge a changé — et c'est pourquoi le
critère gelé portait sur les chiffres, pas sur l'octet du JSON.

**Étape 4 — script complet : EXIT:0.** Le script corrigé entier (~2,4 Go,
52 fichiers) a été exécuté en entier jusqu'à succès, journal final
`cold/full_script_877i.log` (21 nov. 2026, 04:15–04:17 UTC) : **36
fichiers « DÉJÀ PRÉSENT ET VÉRIFIÉ » + 16 OK frais, 0 erreur, ligne
finale « TERMINE : tous les jeux de données téléchargés et vérifiés »,
EXIT:0.** Dossier `cold/data_full/` : 52 fichiers, 2,4 Go — 6 DepMap,
4 TCGA, 2 GEO (GSE71729, GSE62452), ICGC expression + Bailey MOESM270,
3 PRISM 24Q2, 4 PRISM 19Q4, GDSC2, screened compounds, 4 CPTAC,
9 PANC-1, 5 ng3398, 5 Birnbaum, SOFT GPL20769, ICGC probe map + NMF,
2 QCMG, clinique PanCanAtlas. Chaque fichier a été vérifié par taille +
SHA/MD5 dans l'invocation finale (36 vérifiés sur place + 16
re-téléchargés). Les 8 exécutions précédentes (journaux
`cold/full_script_877.log`, `877b.log`, `877c.log`, `877d.log`,
`877e.log`, `877f.log`, `877g.log`, `877h.log`) sont consignées au
§8.77.5 avec leurs incidents — elles ont fait avancer le diagnostic,
aucune n'a été effacée. Le script livré est la version avec reprise
(`get_checked()`, SHA `55811136…`) : une interruption (incident
transitoire, redémarrage) ne coûte plus un re-téléchargement intégral.

## 8.77.7 — DATA_SOURCES.md révisé : ce qui change, section par section

**Fichier livré :** `~/workspace/runs/pdac-v6/DATA_SOURCES_877.md`
(900 lignes ; référence : `~/workspace/push_v62_875_build/snap/DATA_SOURCES.md`,
SHA `2b58ec35…`, 702 lignes). Diff résumé section par section :
`repro_877/DATA_SOURCES_877_diff.md`. Ne pas pousser par ce chantier —
poussée par le coordinateur.

**Les changements.** En-tête : ligne « Révision §8.77 ». §0.1 : limites
du script réécrites comme corrigées. §0.3 : inventaire — sources avec
URL complète 8/16 → **16/16**, sources partielles 4/16 → **0/16**,
sources sans URL 4/16 → **0/16**. §3.1 : URL + MD5 + SHA-256 du SOFT
GPL20769 (chemin corrigé `GPL20nnn/`). §3.2 : patron d'URL ng3398.
§5.3/§5.4 : URL du hub Xena (probe map, NMF). §6 : 4 URL directes
CPTAC. §7 : URL du fichier de métadonnées PRISM 24Q2. §8 : 4 URL
directes PRISM 19Q4. §10 : URL de `mit_test.csv` marquée vérifiée.
§11 : titre changé (provenance retrouvée), bloc de la lacune remplacé
par l'URL datahub et la double confirmation LFS. §12 : URL QCMG.
§13 : DOI Birnbaum + patron d'URL Springer. §15.4 : SOFT
re-téléchargeable (chemin corrigé). §15.6 : lacune PanCanAtlas marquée
CLOSE, historique conservé (la lacune a existé du 15 au 21 nov. 2026).
§17 : bilan révisé — **19/19 fermés**, aucune URL manquante restante,
chaque ligne du tableau mise à jour (« FERMÉ §8.77 » + URL, historique
conservé). §2.3 : SHA-256 LUAD corrigé (faute de frappe de 65
caractères). §5.2 : URL ICGC expression corrigée (hub au lieu de S3
directe = 403). §13 : SHA-256 Birnbaum MOESM3 corrigé (faute de frappe
de 62 caractères). Annexe A §2 : la plupart des fichiers sont désormais
dans le script corrigé (il ne reste hors script que la table GPL6244,
dérivée du SOFT).

**Nouvelle §28 — sources du §8.76.** Aucun nouveau téléchargement :
réutilisation du téléchargement §8.74 (Yeh_seq TSV SHA `2fc0a66e…`,
matrice GPL18573 SHA `9b333eb6…`, SHA re-vérifiés) ; lot FNA 42 codes,
test apparié (41/42 mêmes tumeurs que FF), verdict CONFIRME d_maxsep
+0,1642 ; flux SHA `70697b3a…`, nul `2474ceaf…`.

**Nouvelle §29 — ce chantier.** Tableau gap par gap (§29.1), voies
infructueuses (§29.2), script corrigé (§29.3), test à froid (§29.4),
ce qui reste ouvert (§29.5 : rien sur les fichiers bruts).

## 8.77.8 — Ce qui reste ouvert

**Sur les fichiers bruts : rien.** Chaque fichier brut du projet a
désormais une URL de téléchargement vérifiée par SHA-256. Il n'y a
aucun gap irrécupérable dans ce chantier — y compris le fichier clinique
du test C, dont la provenance a été retrouvée au lieu d'être déclarée
irrécupérable.

**Hors périmètre (déjà documentés, non rouverts).** Les fichiers dérivés
se reconstruisent par scripts (§14 de DATA_SOURCES.md). Les résultats
`results_fast_*` (~7 Go) ne sont pas dans le dépôt par limite snapshot
mais se reconstruisent par les runs — le test à froid le démontre pour
la paire TCGA v4. Les matrices brutes (~2,4 Go) ne sont pas dans le
dépôt par limite snapshot mais se re-téléchargent vérifiées par le
script corrigé. Les URL vérifiées aujourd'hui peuvent mourir demain
(services tiers) : les SHA consignés permettent de détecter tout
changement — c'est la garantie, pas la pérennité des liens.

## 8.77.9 — Ce que cette section ne change pas

**Rien, dans le livre blanc, n'est modifié par ce chantier.** Aucune
section existante n'est touchée, aucun verdict n'est rouvert, aucun
chiffre n'est corrigé. Le test C reste NON (§8.45) — sa reproductibilité
est réparée, son verdict est le même. Les fichiers QCMG restent écartés
(§12). Le lot FNA reste un test apparié, pas une treizième paire (§8.76).
Les scores ESTIMATE, xCell et les autres sources des §8.54–§8.76 ne sont
pas concernés par ce chantier (leurs URL étaient déjà consignées et
vérifiées dans leurs sections). Cette section est une réparation de
traçabilité, à part, comme Zackary l'a ordonné le 20 nov. 2026 à 19h40 :
elle ne se confond pas avec l'état actuel, elle le rend reconstructible.

## 8.77.10 — Fichiers produits (SHA-256)

| Fichier | SHA-256 |
|---|---|
| `PROTOCOL_reproductibilite_877.md` (gelé 21 nov. 2026, 01h37 UTC) | `dbe1746f7233e69a3052407576ebf6043080016c97a12d41f76244fc569a4030` |
| `repro_877/download_data_877.sh` (script corrigé) | `558111360ceda48bece577d7176a5ad5e46630f0a39fc85c03e8c3635564c78f` |
| `repro_877/download_data_877.diff` (323 lignes) | `e333ae041c5918bccc59cdbe262ea318546f7cf0e0e8fafc2ed311a35fc58f26` |
| `DATA_SOURCES_877.md` (révisé, 900 lignes) | `17b8428b2f066d45f74eca2373a0d53c4dfd31f8850178308b117f8496a408fc` |
| `repro_877/DATA_SOURCES_877_diff.md` (diff résumé, 179 lignes) | `de00f940704a07a2b9645d8fb1881fe64d6d168fcc39cfc6b7437953ecec60b2` |
| `repro_877/JOURNAL_877.md` (journal du chantier, 297 lignes) | `c3bdda5d708a96db8cc300373881e11e31d05eefb4a045e9fc25e327dcd50c34` |
| `section_8.77_reproductibilite.md` (cette section, 649 lignes) | SHA calculé après gel du texte — consigné dans `JOURNAL_877.md` (entrée de livraison) et dans le rapport de livraison au coordinateur (l'auto-référence est impossible dans le fichier lui-même) |

Pipeline v6.2 SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant le gel et après chaque lot de runs, inchangé).
Original du script : `~/workspace/staging-pdac/download_data.sh`, SHA
`4e151d59391164e49d24c4bd590f927f67dfb1bc09a2f3e041202f580006c448`
(intact). Référence DATA_SOURCES.md :
`~/workspace/push_v62_875_build/snap/DATA_SOURCES.md`, SHA
`2b58ec3533ee7c7837dbeeaf9cd2aaed2ec3560b5240082a358256b3fb1caea2`
(intacte).

— Fin de la section §8.77. —
