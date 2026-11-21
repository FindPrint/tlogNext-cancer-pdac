# PROTOCOL_reproductibilite_877 — §8.77 : réparation de la reproductibilité des dépôts

**Protocole gelé AVANT tout travail de récupération — 21 nov. 2026, 01h37 UTC
(20 nov. 2026, 20h37 EST).**

## 0. Règles gelées (non négociables)

1. **Section à part** (règle de Zackary, 20 nov. 2026, 19h40) : cette réparation
   ne se confond PAS avec l'état actuel. Aucune section existante du livre
   blanc n'est modifiée, le livre blanc n'est pas édité par ce chantier
   (fusion par le coordinateur après), aucun verdict n'est rouvert. Le test C
   (§8.45) reste ce qu'il est : sa reproductibilité est marquée limitée,
   rien de plus. Aucune poussée GitHub par ce chantier, aucune régénération
   du PDF.
2. **Provenance toujours nommée** (règle permanente, 27 oct. 2026) : chaque
   URL est copiée depuis une source lue, ou reconstruite puis VÉRIFIÉE par
   le SHA du fichier re-téléchargé. **Aucune URL n'est inventée.** Une URL
   reconstruite qui ne vérifie pas le SHA est consignée comme telle et le
   gap reste ouvert.
3. **Pipeline v6.2 intact** : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
   SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
   — vérifié avant le gel (01h37 UTC) et à vérifier après chaque lot de runs.
   Le code n'est JAMAIS modifié. Les scripts de construction des flux ne
   sont pas modifiés non plus ; pour le test à froid, une COPIE de
   `build_fluxes_tcga_v4.py` est faite dans le dossier froid avec pour
   seules différences les deux constantes de chemins (`DATA`, `OUT`) —
   diff consigné dans le journal du chantier.
4. **Lots longs en `systemd-run`** (jamais `nohup`) ; fichiers de travail
   sous `~/workspace` (jamais `/tmp`) ; si la machine redémarre, reprendre
   sans relancer à l'aveugle (vérifier ce qui est déjà terminé, ne jamais
   toucher un dossier de run en cours).
5. **Critère de succès par gap** : URL retrouvée depuis une source lue +
   fichier re-téléchargé + SHA-256 (ou MD5 / taille quand aucun SHA n'est
   consigné) identique au SHA consigné dans `DATA_SOURCES.md` ou dans la
   provenance. Sinon le gap est déclaré **IRRÉCUPÉRABLE** avec la raison
   exacte, ou **PARTIEL** (URL retrouvée, SHA non vérifiable — préciser
   pourquoi).
6. **Dossier de travail** : `~/workspace/runs/pdac-v6/repro_877/` ;
   re-téléchargements dans `repro_877/downloads/` ; test à froid dans
   `repro_877/cold/`. Les fichiers locaux originaux de `data/` ne sont
   jamais écrasés ni déplacés : la comparaison se fait par SHA, pas par
   remplacement.

## 1. État des lieux de départ (vérifié 20 nov. 2026, 19h38)

Source : `DATA_SOURCES.md` §17 (copie locale de référence
`~/workspace/push_v62_875_build/snap/DATA_SOURCES.md`, SHA-256 à vérifier
avant usage ; version distante identique, blob SHA `863ffd80…`).

**19 fichiers bruts sans URL de téléchargement consignée** (le compte du
§17) :

| # | Gap | Fichiers | SHA consignés (référence) |
|---|---|---|---|
| G1 | Suppléments Nature Moffitt ng3398, MOESM59–63 | 5 | §3.2 (SHA-256 complets calculés localement 19 nov.) |
| G2 | Suppléments Springer Birnbaum MOESM1–5 | 5 | §13 (SHA-256 complets calculés localement 19 nov.) |
| G3 | ICGC probe map + NMF (Xena) | 2 | §5.3, §5.4 (SHA-256 vérifiés) |
| G4 | PRISM 24Q2 métadonnées lignées | 1 | §7 (SHA-256 consigné) |
| G5 | PRISM 19Q4, 4 fichiers via API (pas d'URL directe par fichier) | 4 | §8 (MD5 vérifiés ; SHA-256 : 2 consignés, 2 calculés localement) |
| G6 | QCMG clinique patient + échantillon (cBioPortal datahub) | 2 | §12 (SHA-256 calculés localement 19 nov.) |

**Hors des 19, à traiter aussi :**

| # | Gap | Référence |
|---|---|---|
| G7 | SOFT GPL20769 (37 588 662 o, non conservé, URL non consignée) | §3.1, §15.4 — critère : taille exacte + contenu (table 19 749 lignes) |
| G8 | `data_clinical_patient.txt` (test C) — AUCUNE provenance d'acquisition | §11, §15.6 — SHA `0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5` |
| G9 | `mit_test.csv` PANC-1 — URL reconstruite, à vérifier avant usage | §10 — SHA `9f3ae18976136412802831487b6187fcf062db8f4ca753990689d3ac62006e27` |
| G10 | CPTAC, 4 fichiers via API Zenodo (pas d'URL directe par fichier) | §6 — MD5 vérifiés ; le script les télécharge déjà via l'API |

**Voies cassées de `download_data.sh`** (à corriger, §4 ci-dessous) : tarball
PANC-1 tronqué ; PRISM 19Q4 2/4 fichiers ; suppléments non téléchargés ;
SOFT GPL20769 non conservé ; PRISM 24Q2 primaire sans vérification de
hachage dans le script (les SHA existent au §7).

## 2. Méthode de récupération par gap (gelée)

### G1 — ng3398 MOESM59–63 (Moffitt et al. 2015, *Nat Genet*, doi 10.1038/ng.3398)

- Méthode : lire la page de l'article Nature
  (`https://www.nature.com/articles/ng.3398`) et/ou sa page de suppléments ;
  relever les liens des fichiers supplémentaires MOESM59–63. Patron attendu
  (à CONFIRMER par lecture, pas à supposer) : domaine
  `static-content.springer.com`, chemin
  `/esm/art%3A10.1038%2Fng.3398/MediaObjects/…_MOESM59_ESM.pdf` (même
  patron que le fichier Bailey MOESM270 déjà consigné au §5.5).
- Télécharger chaque candidat dans `repro_877/downloads/ng3398/` et comparer
  taille + SHA-256 aux valeurs du §3.2.
- Succès : 5/5 SHA identiques. Échec partiel consigné fichier par fichier.

### G2 — Birnbaum MOESM1–5 (PMC5674743)

- Méthode : lire la page PMC (`https://pmc.ncbi.nlm.nih.gov/articles/PMC5674743/`)
  et relever les liens des suppléments ; sinon, interroger l'API Europe PMC
  des fichiers supplémentaires
  (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5674743/supplementaryFiles`)
  — voie déjà utilisée avec succès pour Aran 2015 (§18.2) et xCell (§21).
- Télécharger dans `repro_877/downloads/birnbaum/` et comparer taille +
  SHA-256 aux valeurs du §13.
- Succès : 5/5 SHA identiques.

### G3 — ICGC probe map + NMF (Xena, hub ICGC)

- Méthode : les jeux sont nommés au §5.3–5.4
  (`PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp`,
  `PACA-AU/nature16965-s2_NMF_class_assignment.txt`) ; le hub est
  `icgc.xenahubs.net`, bucket S3 `icgc-xena-hub` (confirmés par §5.2).
  Lister le bucket (`https://icgc-xena-hub.s3.amazonaws.com/?list-type=2&prefix=download/PACA-AU/`)
  et/ou interroger le hub Xena pour retrouver les URL exactes des deux
  objets. Candidats à tester SEULEMENT s'ils sortent de cette lecture :
  `…/download/PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp.gz`
  et `…/download/PACA-AU/nature16965-s2_NMF_class_assignment.txt` (le
  second n'est pas gzippé dans le jeu nommé ; l'extension réelle est à
  relever dans la lecture, pas à deviner).
- Télécharger dans `repro_877/downloads/icgc/` et comparer taille +
  SHA-256 aux valeurs des §5.3–5.4 (`probemap.gz` 353 314 o,
  SHA `b09a746f…75537` ; `nmf.txt.gz` 447 o, SHA `f1e84b99…21e2f`).
  Attention : le fichier local `nmf.txt.gz` est gzippé (447 o) alors que le
  jeu Xena nommé est `.txt` — si l'objet distant est le `.txt` non gzippé,
  comparer le contenu décompressé (nombre de lignes, classes 30/25/25/16)
  et le SHA du fichier gzippé localement, et le consigner comme tel.
- Succès : 2/2 vérifiés (SHA ou, pour le NMF, contenu identique + SHA du
  re-gzippage documenté).

### G4 — PRISM 24Q2 `Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv`

- Méthode : interroger l'API figshare de l'article 25917643
  (`https://api.figshare.com/v2/articles/25917643`), relever le
  `download_url` du fichier `Cell_Line_Meta_Data` dans la réponse JSON
  (champ lu, pas deviné).
- Télécharger dans `repro_877/downloads/prism24q2/` et comparer taille
  (157 294 o) + SHA-256 (`13a85da9…3b0526`, §7).
- Succès : SHA identique. Conséquence script : ajouter le fichier au
  `download_data.sh` avec vérification de hachage (voir §4).

### G5 — PRISM 19Q4, 4 fichiers (figshare article 9393293)

- Méthode : interroger l'API figshare
  (`https://api.figshare.com/v2/articles/9393293`), relever les 4
  `download_url` (champs lus). Les 2 fichiers déjà dans le script
  (dose-response, replicate-collapsed) servent de témoins : leurs
  `download_url` doivent correspondre à des fichiers dont le MD5 vérifie
  les valeurs du §8.
- Télécharger les 2 fichiers manquants du script
  (`secondary-screen-cell-line-info.csv`, 40 979 o, MD5
  `6737b4aa9fd85404fd2f0cf825b037e4` ; `secondary-screen-readme.txt`,
  7 647 o, MD5 `421d0bbadec381adc0d7981ee7e16bd7`) dans
  `repro_877/downloads/prism19q4/` et vérifier MD5 + SHA-256 (§8).
- Succès : 4/4 fichiers re-téléchargeables par URL directe consignée
  (les URL `download_url` figshare sont stables par ID de fichier ;
  consigner l'URL complète lue dans la réponse API).

### G6 — QCMG clinique (cBioPortal, étude `paad_qcmg_uq_2016`)

- Méthode : lire la page d'étude cBioPortal
  (`https://www.cbioportal.org/study/summary?id=paad_qcmg_uq_2016`) et le
  dépôt datahub cBioPortal (GitHub `cBioPortal/datahub`, dossier
  `public/paad_qcmg_uq_2016`) — lister les fichiers par l'API GitHub
  (contenu du dossier lu, pas deviné) et relever les `download_url`.
- Télécharger `data_clinical_patient.txt` (49 042 o) et
  `data_clinical_sample.txt` (57 215 o) dans `repro_877/downloads/qcmg/`
  et comparer taille + SHA-256 (§12 : patient `ae7fc6d7…6a95`,
  échantillon `c70daf3e…ceca`).
- Succès : 2/2 SHA identiques. Rappel : fichiers ÉCARTÉS pour les
  verdicts (non utilisés) — la récupération ne change rien à leur statut,
  elle ne fait que fermer le gap de provenance.

### G7 — SOFT GPL20769

- Méthode : chemin FTP GEO standard, à VÉRIFIER par lecture du répertoire
  (`https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL2nnn/GPL20769/soft/`) :
  fichier attendu `GPL20769_family.soft.gz`. Télécharger dans
  `repro_877/downloads/gpl20769/` ; critère : taille 37 588 662 o exacts
  (aucun SHA consigné) + contenu : table de 19 749 lignes (même compte
  que la matrice GSE71729, §3).
- Succès : taille exacte + 19 749 lignes. Le fichier est ensuite à
  conserver comme re-téléchargeable par URL (pas besoin de le pousser :
  37 Mo, hors limite snapshot) ; le script corrigé le télécharge et
  vérifie sa taille.

### G8 — `data_clinical_patient.txt` (test C, PanCanAtlas)

- Méthode (hypothèse à TESTER, pas une affirmation) : le format
  `data_clinical_patient.txt` est le format cBioPortal ; l'étude
  PanCanAtlas PAAD existe sur cBioPortal (`paad_tcga_pan_can_atlas_2018`).
  Lister le dossier correspondant dans le dépôt datahub
  (`public/paad_tcga_pan_can_atlas_2018`) par l'API GitHub, télécharger
  le candidat dans `repro_877/downloads/pancanatlas/` et comparer le
  SHA-256 à `0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5`.
  Si le SHA diffère : comparer le contenu (184 patients PAAD, stades AJCC
  7e, colonnes) et chercher une autre voie (GDC, supplément PanCanAtlas
  Raphael et al. 2017) — UNE seule autre tentative documentée, puis
  déclaration.
- Succès : SHA identique → gap fermé, provenance d'acquisition consignée
  (cBioPortal datahub, étude nommée, URL exacte).
- Échec : **IRRÉCUPÉRABLE** — déclaré tel quel dans la section et dans
  `DATA_SOURCES.md` §17 révisé, avec l'implication : verdict du test C
  inchangé (les chiffres ne bougent pas), reproductibilité du test C
  limitée (le fichier reste vérifiable par son SHA, pas re-téléchargeable
  depuis une source connue). Aucune autre URL n'est proposée sans
  vérification SHA.

### G9 — `mit_test.csv` PANC-1

- Méthode : télécharger l'URL reconstruite
  `https://raw.githubusercontent.com/ncats/PANC1/main/MIT/test.csv`
  dans `repro_877/downloads/panc1/` et comparer taille (3 249 228 o) +
  SHA-256 (`9f3ae189…6e27`, §10).
- Succès : SHA identique → URL consignée comme vérifiée. Échec : gap
  ouvert, URL retirée de `DATA_SOURCES.md` (reste « à vérifier »).

### G10 — CPTAC, 4 fichiers via API Zenodo

- Méthode : interroger l'API Zenodo (`https://zenodo.org/api/records/8394329`),
  relever les 4 `links.self` (champs lus) ; vérifier que le script actuel
  les télécharge déjà correctement (il le fait — voir §0.1). Ne PAS
  re-télécharger les 28 Mo sauf si l'API a changé : consigner les URL
  `links.self` lues dans `DATA_SOURCES.md` §6 révisé (elles sont stables
  par record) et marquer G10 comme **fermé par consignation d'URL lues**,
  avec la note que la vérification MD5 complète a déjà été faite à
  l'acquisition (15 nov. 2026) et par le script.
- Si l'API ne répond plus ou si les fichiers ont changé : re-télécharger
  et vérifier les MD5 du §6, consigner l'écart.

## 3. Test à froid (TCGA v4, réel + nul)

- **Paire** : TCGA v4 (paire principale, 178 tumeurs), flux
  `pdac_tcga_fluxes_v4.csv` (SHA `e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0`)
  et nul graine 42 (`pdac_tcga_fluxes_v4_nul.csv`, SHA
  `895a456295d2b0553a2a62910461aedecb1aeccca59f57751c87b75ce0b97da4`).
- **Chiffres tenus (v6.2, validation §8.37, rep1 = rep2 à l'octet)**,
  extraits le 21 nov. 2026 01h36 UTC par `extract_858.extract` sur
  `results_fast_v62_tcga_v4` et `results_fast_v62_tcga_v4_nul` :
  - Réel : n=178, cascade [0,0 ; 74,0617 ; 93,2217 ; 98,4358 ; 98,9572],
    MC=0,3720465146241378, maxsep=0,46234232096887146,
    S_sep=0,4548206606358036, Delta=4,181387, L7a down 0,4051910172618019,
    fals=0,849386. `master_results.json` SHA
    `1506f23dcfe44ab604cec21ff977b025b8f90cdd8c6acb202e7974e08164df76`.
  - Nul : n=178, cascade [0,0 ; 10,6496 ; 15,9571 ; 67,119 ; 67,119],
    MC=0,326773250583873, maxsep=0,1695801283296793,
    S_sep=0,1687743461786773, Delta=3,765664, L7a up 0,16715778704330952,
    fals=0,642205. `master_results.json` SHA
    `0d939a4045482ef980d47be9eb61ad0f3a4b645e0b739a409354e9493a62bc5a`.
  - d_maxsep tenu : +0,29276219.
- **Procédure** (dossier propre `repro_877/cold/`, RIEN dans `pdac-v6/`
  n'est touché) :
  1. Copier le script CORRIGÉ `download_data.sh` (version §4) dans
     `repro_877/cold/` ; l'exécuter avec pour destination
     `repro_877/cold/data` MAIS en ne re-téléchargeant que la section
     TCGA (le script complet téléchargerait ~2 Go : on l'exécute en
     entier si le temps le permet, sinon on extrait la section TCGA
     dans un script froid dédié `cold_tcga.sh` qui reprend LITTÉRALEMENT
     les 4 commandes `get`/`check` TCGA du script corrigé — consigner
     le choix et pourquoi).
  2. Vérifier MD5 du tarball PAAD RSEM
     (`b09569ce3f4721f514bc137bd109ac0a`) et taille (15 296 232 o).
  3. Copier `build_fluxes_tcga_v4.py` dans `repro_877/cold/` en ne
     changeant que `DATA` et `OUT` (chemins froids) ; consigner le diff
     (`diff -u` original/copie) ; exécuter la copie ; comparer les SHA
     des flux reconstruits aux SHA tenus ci-dessus (attendu : identiques
     à l'octet, le script étant déterministe, graine 42 pour le nul).
  4. Lancer v6.2 en mode `fast`, `--seed 42` (défaut), depuis
     `repro_877/cold/` :
     `python3 /home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py --input <flux_froid>.csv --mode fast --output results_fast_cold_tcga_v4`
     (réel puis nul), en unité `systemd-run` reprenable, journal
     `runs_cold_877.log` avec SHA v6.2 avant/après et exit codes.
  5. Extraire avec `extract_858.extract` (original intact, import
     depuis `pdac-v6/`) et comparer : cascade, MC, maxsep, S_sep,
     Delta, L7a, fals — réel et nul — aux chiffres tenus.
- **Critère de réussite** : flux reconstruits SHA-identiques aux flux
  tenus ET chiffres v6.2 identiques aux chiffres tenus (tolérance 0,0
  exact pour la cascade et les scores, v6.2 étant déterministe — rep1 =
  rep2 à l'octet au §8.37 ; toute différence, même petite, est consignée
  chiffre par chiffre, pas lissée).
- **En cas d'échec** : nommer ce qui diffère (fichier, champ, valeurs
  tenues vs froides), et dire si l'écart vient du téléchargement, de la
  reconstruction des flux ou du run.

## 4. Correction de `download_data.sh`

- Fichier de travail : copie de `~/workspace/staging-pdac/download_data.sh`
  dans `repro_877/download_data_877.sh` ; l'original n'est pas modifié par
  ce chantier (la copie corrigée est livrée au coordinateur avec le diff).
- Corrections (chacune avec un commentaire nommant l'ancienne voie et
  pourquoi elle était cassée ; l'historique n'est pas effacé) :
  1. **PANC-1** : remplacer le tarball `codeload.github.com/ncats/PANC1/tar.gz/refs/heads/main`
     (tronqué en pratique, 569 815 185 o, gzip « unexpected end of file »)
     par le téléchargement fichier par fichier via
     `raw.githubusercontent.com/ncats/PANC1/main/…` (8 fichiers §10 +,
     si G9 vérifie, `MIT/test.csv`), avec vérification taille + SHA-256
     par fichier.
  2. **PRISM 19Q4** : compléter le dictionnaire `want` avec les 2 fichiers
     manquants (`secondary-screen-cell-line-info.csv`,
     `secondary-screen-readme.txt`) et, si G5 les fournit, leurs URL
     directes `download_url` figshare en plus de la voie API.
  3. **Suppléments** : ajouter les sections ng3398 (G1) et Birnbaum (G2)
     si leurs URL vérifient, avec vérification taille + SHA-256 ;
     sinon, ajouter un bloc commenté « URL non retrouvée — voir §8.77 »
     (pas d'URL devinée dans le script).
  4. **SOFT GPL20769** : ajouter le téléchargement (G7) avec vérification
     de taille (37 588 662 o) ; noter que le fichier n'est pas conservé
     dans `data/` (annotation extraite puis fichier supprimé à l'origine)
     et que le script le re-télécharge à la demande.
  5. **PRISM 24Q2 primaire** : ajouter la vérification SHA-256/MD5
     (valeurs §7) au lieu de `check … - -` ; ajouter le fichier de
     métadonnées (G4) avec vérification.
  6. **ICGC probe map / NMF** (G3), **QCMG** (G6) : ajouter les sections
     si leurs URL vérifient, avec vérification taille + SHA-256.
  7. **`data_clinical_patient.txt`** (G8) : ajouter la section SEULEMENT
     si G8 vérifie le SHA ; sinon, bloc commenté « provenance
     d'acquisition manquante — voir §8.77 » (le script ne peut pas le
     re-télécharger).
- Après correction : `bash -n` (syntaxe) + test réel de la section TCGA
  dans le test à froid (§3). Le script complet (~2 Go) n'est pas exécuté
  en entier dans ce chantier sauf si le temps le permet — consigner ce
  qui a été testé et ce qui ne l'a pas été.

## 5. Mise à jour de `DATA_SOURCES.md`

- Produire le fichier révisé COMPLET dans
  `~/workspace/runs/pdac-v6/DATA_SOURCES_877.md` (ne pas écraser
  l'original ; ne pas pousser — poussée par le coordinateur).
- Contenu : toutes les URL vérifiées ajoutées à leur section (§3.1,
  §3.2, §5.3, §5.4, §6, §7, §8, §10, §11, §12), §17 révisé (bilan
  gap par gap : fermé / partiel / ouvert), nouvelle §28 pour les sources
  du §8.76 (GSE131050 FNA — réutilisation du téléchargement §8.74, SHA
  re-vérifiés, voir `PROVENANCE_876.md`), et nouvelle §29 consignant
  ce chantier §8.77 (méthode, résultats, ce qui reste ouvert).
- Livrer aussi un diff résumé section par section
  (`DATA_SOURCES_877_diff.md`).

## 6. Section §8.77

- Fichier `~/workspace/runs/pdac-v6/section_8.77_reproductibilite.md`,
  ~500 lignes, style des sections précédentes (verdict d'abord, chiffres
  ensuite), avec son SHA-256.
- Verdict : **REPRODUCTIBILITÉ RÉPARÉE** (gaps comblés sur le total) ou
  **PARTIELLEMENT RÉPARÉE** (liste exacte de ce qui reste ouvert).
- Contenu : méthode, résultat gap par gap (URL retrouvée / SHA vérifié /
  irrécupérable + raison), correction du script, test à froid (chiffres
  comparés), ce qui reste ouvert, ce que cela implique (test C inclus).

## 7. Journal du chantier

- `repro_877/JOURNAL_877.md` : chaque téléchargement (URL, date UTC,
  taille, SHA, conforme ou non), chaque run (commande, exit code, SHA
  v6.2 avant/après), chaque décision (dont les échecs et les voies
  abandonnées).

— Fin du protocole gelé. Tout écart à ce protocole est consigné dans le
journal avec sa raison, pas passé sous silence. —
