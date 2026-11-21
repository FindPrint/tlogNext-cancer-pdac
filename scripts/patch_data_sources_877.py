#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch DATA_SOURCES.md -> DATA_SOURCES_877.md (§8.77).
Applique des remplacements exacts sur la copie de reference
~/workspace/push_v62_875_build/snap/DATA_SOURCES.md (SHA 2b58ec35...).
Chaque remplacement est compte ; le script echoue si un motif est absent
ou present plus d'une fois (sauf indication contraire).
"""
import sys

SRC = "/home/hatch/workspace/push_v62_875_build/snap/DATA_SOURCES.md"
DST = "/home/hatch/workspace/runs/pdac-v6/DATA_SOURCES_877.md"

with open(SRC, encoding="utf-8") as f:
    txt = f.read()

applied = []


def rep(old, new, count=1):
    global txt
    n = txt.count(old)
    assert n == count, f"MOTIF x{n} (attendu x{count}) : {old[:90]!r}"
    txt = txt.replace(old, new)
    applied.append(old[:60])


# --- En-tete : mention de la revision §8.77
rep(
    "**Date de rédaction :** 19 novembre 2026.",
    "**Date de rédaction :** 19 novembre 2026.\n"
    "**Révision §8.77 :** 21 novembre 2026 — toutes les URL manquantes du §17 "
    "ont été retrouvées et vérifiées par SHA-256 (voir §29, chantier §8.77) ; "
    "nouvelle §28 (sources du §8.76) et §29 (bilan du chantier). "
    "Aucun verdict du livre blanc n'est modifié par cette révision.",
)

# --- §0.1 : limites du script, corrigees au §8.77
rep(
    """**Limites connues du script (vérifiées, voir §15) :**
- Il ne télécharge que **2 des 4** fichiers PRISM 19Q4 (`secondary-screen-cell-line-info.csv` et `secondary-screen-readme.txt` manquent dans son dictionnaire `want`).
- Sa section PANC-1 télécharge le tarball `codeload.github.com/ncats/PANC1/tar.gz/refs/heads/main`, qui s'est révélé **tronqué** en pratique (569 815 185 o, erreur gzip « unexpected end of file ») : la voie qui a fonctionné est le téléchargement fichier par fichier via `raw.githubusercontent.com` (voir §10).
- Il ne télécharge pas : les suppléments Nature/Springer (ng3398 MOESM59–63, Birnbaum MOESM1–5), le SOFT GPL20769, les fichiers ICGC probe map / NMF, les fichiers cliniques QCMG, `Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv`, ni `data_clinical_patient.txt` (provenance d'acquisition manquante, voir §11).
- Pour PRISM 24Q2 primaire, le script ne vérifie **aucun hachage** (`check ... - -`) : les SHA-256/MD5 consignés au §7 proviennent de `PROVENANCE_mtap_arbitration_840.md` et ont été re-vérifiés localement le 19 nov. 2026.""",
    """**Limites connues du script — CORRIGÉES au §8.77** (voir §29 ; le script
corrigé est `repro_877/download_data_877.sh`, diff `repro_877/download_data_877.diff`) :
- PRISM 19Q4 : le script d'origine ne téléchargeait que **2 des 4** fichiers
  (`secondary-screen-cell-line-info.csv` et `secondary-screen-readme.txt`
  manquaient dans son dictionnaire `want`) — **corrigé** : les 4 fichiers
  sont téléchargés, avec leurs URL directes figshare en commentaire (§8).
- PANC-1 : la section d'origine téléchargeait le tarball
  `codeload.github.com/ncats/PANC1/tar.gz/refs/heads/main`, qui s'est révélé
  **tronqué** en pratique (569 815 185 o, erreur gzip « unexpected end of
  file ») — **corrigé** : téléchargement fichier par fichier via
  `raw.githubusercontent.com`, avec vérification taille + SHA-256 (§10).
- Le script d'origine ne téléchargeait pas : les suppléments Nature/Springer
  (ng3398 MOESM59–63, Birnbaum MOESM1–5), le SOFT GPL20769, les fichiers
  ICGC probe map / NMF, les fichiers cliniques QCMG,
  `Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv`, ni
  `data_clinical_patient.txt` — **corrigé** : toutes ces sections sont
  ajoutées, URL vérifiées par SHA-256 (§8.77).
- PRISM 24Q2 primaire : le script d'origine ne vérifiait **aucun hachage**
  (`check ... - -`) — **corrigé** : SHA-256/MD5 vérifiés (§7) et fichier de
  métadonnées des lignées ajouté.
- Le script corrigé complet (~2,4 Go) a été exécuté le 21 nov. 2026 dans
  le chantier §8.77 (unité `repro877-cold-full`, journal
  `repro_877/cold/full_script_877.log`) — résultat consigné au §29.""",
)

# --- §0.3 : inventaire rapide
rep(
    """| Sources brutes distinctes couvertes | 16 |
| Fichiers `data/` de plus de 5 Mo | 19 — **19/19 couverts (§16)** |
| Fichiers `data/` au total | 87 (~2,44 Go) |
| Sources brutes avec URL complète pour leur(s) fichier(s) principal(aux) | 8 sur 16 |
| Sources brutes partielles (accès via API : figshare/Zenodo, pas d'URL directe par fichier) | 4 sur 16 (CPTAC, PRISM 24Q2, PRISM 19Q4, QCMG) |
| Sources brutes sans URL | 4 sur 16 (PanCanAtlas clinique, Birnbaum, ng3398, SOFT GPL20769) |""",
    """| Sources brutes distinctes couvertes | 16 |
| Fichiers `data/` de plus de 5 Mo | 19 — **19/19 couverts (§16)** |
| Fichiers `data/` au total | 87 (~2,44 Go) |
| Sources brutes avec URL complète pour leur(s) fichier(s) principal(aux) | **16 sur 16 (depuis §8.77, voir §17 révisé et §29)** |
| Sources brutes partielles (accès via API : figshare/Zenodo, pas d'URL directe par fichier) | 0 sur 16 — CPTAC, PRISM 24Q2, PRISM 19Q4 et QCMG ont désormais aussi leurs URL directes consignées (§6, §7, §8, §12) ; l'accès par API reste la voie du script quand elle fonctionne |
| Sources brutes sans URL | **0 sur 16 (depuis §8.77)** |""",
)

# --- §3.1 : SOFT GPL20769, URL + hachages
rep(
    """- **Fichier SOFT de la famille GPL20769 : 37 588 662 octets, téléchargé le 15 nov. 2026** (table de 19 749 lignes) — **fichier absent de `data/`** (non conservé après extraction) et **URL non consignée dans les provenances**.""",
    """- **Fichier SOFT de la famille GPL20769 : 37 588 662 octets, téléchargé le 15 nov. 2026** (table de 19 749 lignes) — **fichier absent de `data/`** (non conservé après extraction).
- **URL exacte (retrouvée et vérifiée §8.77, 21 nov. 2026) :** `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL20nnn/GPL20769/soft/GPL20769_family.soft.gz` — re-téléchargé le 21 nov. 2026 : taille 37 588 662 o exactement, table 19 750 lignes (en-tête + 19 749 lignes), titre confirmé (« Agilent-014850 Whole Human Genome Microarray 4x44K G4112F (Gene Symbol Version; updated July 2014) »). **MD5 :** `4c39e802ec78170d7ed5c8c2cc2b0bec` ; **SHA-256 :** `ecb1b79a6b89e521a1116a3113fcb9a5af1c181329eec8257e044e0683822d3e` (calculés le 21 nov. 2026 sur le fichier re-téléchargé). **Note :** le chemin deviné au §15.4 (`GPL2nnn/`) donne 404 — le regroupement GEO masque les 3 derniers chiffres (20769 → `GPL20nnn`, comme 6244 → `GPL6nnn` au §4.1).""",
)

# --- §3.2 : URLs ng3398
rep(
    """Téléchargés le 16 nov. 2026 (dates de fichiers 16 nov. 12:09). **URL non consignée dans les provenances** pour ces 5 fichiers (seuls les noms, tailles et SHA tronqués sont consignés dans `PROVENANCE_geo71729_survival.md`). Les SHA-256 complets ci-dessous ont été calculés localement le 19 nov. 2026 ; leurs préfixes correspondent aux valeurs tronquées consignées.""",
    """Téléchargés le 16 nov. 2026 (dates de fichiers 16 nov. 12:09). **URL retrouvées et vérifiées §8.77 (21 nov. 2026)** — patron Springer `static-content.springer.com/esm/art%3A10.1038%2Fng.3398/MediaObjects/41588_2015_BFng3398_MOESM{n}_ESM.{ext}` (code revue 41588 = *Nature Genetics* ; même patron que le fichier Bailey MOESM270 du §5.5) ; les 5 fichiers ont été re-téléchargés le 21 nov. 2026 et leurs tailles + SHA-256 vérifiés identiques à ceux ci-dessous. (Avant §8.77 : URL non consignée dans `PROVENANCE_geo71729_survival.md` — seuls noms, tailles et SHA tronqués.) Les SHA-256 complets ci-dessous ont été calculés localement le 19 nov. 2026 ; leurs préfixes correspondent aux valeurs tronquées consignées.""",
)

# --- §5.3 : probe map URL
rep(
    """- **URL exacte : URL non consignée dans les provenances** (le jeu Xena est nommé, l'URL de téléchargement du fichier probe map n'est pas consignée littéralement ; hub : `https://icgc.xenahubs.net/download/...`, bucket S3 `icgc-xena-hub` — voir §5.2).""",
    """- **URL exacte (retrouvée et vérifiée §8.77, 21 nov. 2026) :** `https://icgc.xenahubs.net/download/PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp.gz` — re-téléchargée le 21 nov. 2026 : taille 353 314 o, SHA-256 `b09a746f6084215beea3632b72e87834ea577d18fcb52add3641de5d0d975537` (identique au consigné). **Note :** le listing du bucket S3 renvoie 403 et l'URL S3 directe (`icgc-xena-hub.s3.amazonaws.com/download/PACA-AU/…`) renvoie 403 aussi — c'est l'URL du hub qui fonctionne (le hub redirige vers le bucket).""",
)

# --- §5.4 : NMF URL
rep(
    """- **URL exacte : URL non consignée dans les provenances** (même remarque qu'au §5.3).""",
    """- **URL exacte (retrouvée et vérifiée §8.77, 21 nov. 2026) :** `https://icgc.xenahubs.net/download/PACA-AU/nature16965-s2_NMF_class_assignment.txt.gz` — re-téléchargée le 21 nov. 2026 : taille 447 o, SHA-256 `f1e84b997c24903c216fbe9806c1b048cd9f552894e018ca54d02b5413921e2f` (identique au consigné). **Note :** le fichier distant est bien `.txt.gz` (le `.txt` nu renvoie 404 sur le hub) ; même remarque que §5.3 pour l'URL S3 directe (403).""",
)

# --- §6 : CPTAC URLs directes
rep(
    """**Page du record :** `https://zenodo.org/records/8394329` — **API Zenodo (utilisée par `download_data.sh`) :** `https://zenodo.org/api/records/8394329` (les URL de fichiers individuels ne sont pas consignées littéralement : elles sont lues dans la réponse de l'API — champ `links.self` de chaque fichier — par le script).""",
    """**Page du record :** `https://zenodo.org/records/8394329` — **API Zenodo (utilisée par `download_data.sh`) :** `https://zenodo.org/api/records/8394329` (les URL de fichiers individuels sont lues dans la réponse de l'API — champ `links.self` de chaque fichier — par le script).
**URL directes par fichier (lues dans la réponse de l'API le 21 nov. 2026, §8.77 ; tailles et MD5 conformes au tableau ci-dessous) :**
- Report UMich : `https://zenodo.org/api/records/8394329/files/umich-pdac-proteomics-Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz/content`
- BCM Tumor : `https://zenodo.org/api/records/8394329/files/bcm-pdac-proteomics-PDAC_proteomics_gene_abundance_log2_reference_intensity_normalized_Tumor.txt.gz/content`
- Mapping UMich : `https://zenodo.org/api/records/8394329/files/umich-pdac-mapping-aliquot_to_patient_ID.tsv.gz/content`
- `cptac_genes.csv` : `https://zenodo.org/api/records/8394329/files/cptac_genes.csv/content`""",
)

# --- §7 : PRISM 24Q2 meta URL
rep(
    """| `data/Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv` | 157 294 | **URL non consignée dans les provenances** (n° de fichier figshare non consigné ; le fichier n'est pas téléchargé par `download_data.sh`) | `13a85da9e45656c455d3911a4491f3636d7d0975a9d2333dc3d0a3e2cd3b0526` | — (non consigné) |""",
    """| `data/Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv` | 157 294 | `https://ndownloader.figshare.com/files/46630978` (**retrouvée §8.77** via l'API figshare `https://api.figshare.com/v2/articles/25917643`, fichier 46630978 ; re-téléchargée le 21 nov. 2026, taille et SHA-256 identiques ; ajoutée au script corrigé) | `13a85da9e45656c455d3911a4491f3636d7d0975a9d2333dc3d0a3e2cd3b0526` | — (non consigné) |""",
)

# --- §8 : PRISM 19Q4 URLs directes
rep(
    """**URL exacte des fichiers individuels : URL non consignée dans les provenances** (pas d'URL `ndownloader` par fichier : accès via l'API `https://api.figshare.com/v2/articles/9393293` ; le script `download_data.sh` récupère les `download_url` depuis cette API).""",
    """**URL exactes des fichiers individuels (lues dans la réponse de l'API figshare `https://api.figshare.com/v2/articles/9393293` le 21 nov. 2026, §8.77 ; les 4 fichiers ont été re-téléchargés et vérifiés — tailles, MD5 et SHA-256 conformes au tableau ci-dessous) :**
- `secondary-screen-dose-response-curve-parameters.csv` : `https://ndownloader.figshare.com/files/20237739`
- `secondary-screen-replicate-collapsed-treatment-info.csv` : `https://ndownloader.figshare.com/files/20237763`
- `secondary-screen-cell-line-info.csv` : `https://ndownloader.figshare.com/files/20237769`
- `secondary-screen-readme.txt` : `https://ndownloader.figshare.com/files/20238123`
(Avant §8.77 : pas d'URL `ndownloader` par fichier dans les provenances ; accès via l'API ci-dessus, champ `download_url`.)""",
)

# --- §10 : mit_test.csv URL verifiee
rep(
    """| `data/panc1_ncata/mit_test.csv` | 3 249 228 | Chemin consigné `MIT/test.csv` (`PROVENANCE_kras_combinations.md`) ; base `https://raw.githubusercontent.com/ncats/PANC1/main/` confirmée par les JSON — URL reconstruite `https://raw.githubusercontent.com/ncats/PANC1/main/MIT/test.csv` (**non consignée littéralement**, à vérifier avant usage) | `9f3ae18976136412802831487b6187fcf062db8f4ca753990689d3ac62006e27` (calculé localement) |""",
    """| `data/panc1_ncata/mit_test.csv` | 3 249 228 | Chemin consigné `MIT/test.csv` (`PROVENANCE_kras_combinations.md`) ; base `https://raw.githubusercontent.com/ncats/PANC1/main/` confirmée par les JSON — URL reconstruite `https://raw.githubusercontent.com/ncats/PANC1/main/MIT/test.csv` (**VÉRIFIÉE §8.77, 21 nov. 2026** : re-téléchargée, taille 3 249 228 o, SHA-256 identique) | `9f3ae18976136412802831487b6187fcf062db8f4ca753990689d3ac62006e27` (calculé localement) |""",
)

# --- §11 : PanCanAtlas provenance recuperee
rep(
    """- **URL : URL non consignée dans les provenances — provenance d'acquisition MANQUANTE** (cité mot pour mot dans `PROVENANCE_testC_stage.md` : « MANQUANTE — fichier déjà sur le disque au début du chantier (15 nov. 2026, 15h13 UTC) ; aucune entrée dans fetch_tcga.log, download_firehose.log ni PROVENANCE_tcga*.md ; premier hachage consigné ici ; rien re-téléchargé »).
- **Conséquence :** ce fichier **ne peut pas être re-téléchargé depuis une source connue** à partir de ce document. Le SHA-256 ci-dessus permet au moins de vérifier un fichier retrouvé ailleurs (le contenu — PanCanAtlas PAAD, 184 patients — pointe vers les données cliniques TCGA PanCanAtlas, mais **aucune URL n'est devinée ici**). C'est la lacune de provenance la plus grave du projet pour la reconstruction.""",
    """- **URL exacte (retrouvée et vérifiée §8.77, 21 nov. 2026) :** `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_tcga_pan_can_atlas_2018/data_clinical_patient.txt` — dépôt GitHub `cBioPortal/datahub`, étude cBioPortal `paad_tcga_pan_can_atlas_2018` (TCGA PanCanAtlas PAAD). Re-téléchargé le 21 nov. 2026 : taille 58 621 o, SHA-256 `0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5` (identique au consigné). **Double confirmation :** les fichiers de ce dépôt sont en Git LFS — le `download_url` de l'API GitHub (`raw.githubusercontent.com/…`) renvoie le pointeur LFS (130 o), et ce pointeur porte lui-même `oid sha256:0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5` et `size 58621`. C'est le contenu réel, servi par `media.githubusercontent.com`, qui a été vérifié.
- **Conséquence (mise à jour §8.77) :** la lacune de provenance la plus grave du projet est **close** : le fichier est désormais re-téléchargeable depuis une source connue et vérifiable. (Avant §8.77 : provenance d'acquisition MANQUANTE, cité dans `PROVENANCE_testC_stage.md` : « MANQUANTE — fichier déjà sur le disque au début du chantier (15 nov. 2026, 15h13 UTC) ; aucune entrée dans fetch_tcga.log, download_firehose.log ni PROVENANCE_tcga*.md ; premier hachage consigné ici ; rien re-téléchargé ».) Le verdict du test C (§8.45) est inchangé — seule sa reproductibilité est réparée.""",
)

# --- §11 : titre de section (plus de warning)
rep(
    "## 11. TCGA PanCanAtlas — clinique patient PAAD (stades, test C) — ⚠️ PROVENANCE D'ACQUISITION MANQUANTE",
    "## 11. TCGA PanCanAtlas — clinique patient PAAD (stades, test C) — provenance d'acquisition RETROUVÉE au §8.77",
)

# --- §12 : QCMG URLs
rep(
    """- **URL exacte des fichiers cliniques : URL non consignée dans les provenances** (la provenance parle du « fichier clinique datahub » sans URL).""",
    """- **URL exactes des fichiers cliniques (retrouvées et vérifiées §8.77, 21 nov. 2026) :** dépôt GitHub `cBioPortal/datahub`, étude `paad_qcmg_uq_2016` — `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_qcmg_uq_2016/data_clinical_patient.txt` et `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_qcmg_uq_2016/data_clinical_sample.txt` — re-téléchargés le 21 nov. 2026 : tailles 49 042 o / 57 215 o, SHA-256 identiques aux valeurs ci-dessus. **Note LFS :** comme au §11, le `download_url` de l'API GitHub (`raw.githubusercontent.com/…`) renvoie le pointeur LFS (130 o) ; le contenu réel est servi par `media.githubusercontent.com`. (Avant §8.77 : « fichier clinique datahub » sans URL, `PROVENANCE_icgc.md`.)""",
)

# --- §13 : Birnbaum URLs
rep(
    """- **Article :** Birnbaum et al., 2017 (validation des classifications ; PMC5674743 — `https://pmc.ncbi.nlm.nih.gov/articles/PMC5674743/`, DOI non relevé dans les fichiers).""",
    """- **Article :** Birnbaum et al., 2017, « Validation and comparison of the molecular classifications of pancreatic carcinomas », *Mol Cancer* 16:174, DOI `10.1186/s12943-017-0739-z` (PMC5674743 — `https://pmc.ncbi.nlm.nih.gov/articles/PMC5674743/`, PMID 29110659).
- **URL exactes (retrouvées et vérifiées §8.77, 21 nov. 2026) :** patron Springer `static-content.springer.com/esm/art%3A10.1186%2Fs12943-017-0739-z/MediaObjects/12943_2017_739_MOESM{n}_ESM.xlsx` (n = 1–5) — les 5 fichiers ont été re-téléchargés le 21 nov. 2026 et leurs tailles + SHA-256 vérifiés identiques à ceux ci-dessous. (Avant §8.77 : « via static-content Springer, MOESM1–5 », sans URL.)""",
)
rep(
    """- **URL : URL non consignée dans les provenances** (source : « via static-content Springer, MOESM1–5 » — sans URL ; article PMC5674743).""",
    """- **URL : voir ci-dessus (§8.77).**""",
)

# --- §15.4 : SOFT desormais re-telechargeable (chemin corrige)
rep(
    """- **SOFT GPL20769 (37 588 662 o)** : téléchargé le 15 nov. 2026, **absent de `data/`** ; URL non consignée (§3.1). Re-téléchargeable en principe depuis le FTP GEO (`geo/platforms/GPL2nnn/GPL20769/soft/GPL20769_family.soft.gz` — chemin non consigné littéralement, à vérifier).""",
    """- **SOFT GPL20769 (37 588 662 o)** : téléchargé le 15 nov. 2026, **absent de `data/`** ; URL retrouvée et vérifiée §8.77 (§3.1) : `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL20nnn/GPL20769/soft/GPL20769_family.soft.gz` (le chemin `GPL2nnn/` donne 404 — voir §3.1). Re-téléchargeable et vérifié par taille + SHA-256.""",
)

# --- §15.6 : lacune PanCanAtlas close
rep(
    """### 15.6 Lacune de provenance — clinique TCGA PanCanAtlas

- `data_clinical_patient.txt` (§11) : provenance d'acquisition **manquante**, aucune URL — **non re-téléchargeable depuis une source connue** à partir de ce document. Seul le SHA-256 permet de vérifier un fichier retrouvé ailleurs.
(Source : `PROVENANCE_testC_stage.md`)""",
    """### 15.6 Lacune de provenance — clinique TCGA PanCanAtlas — CLOSE au §8.77

- `data_clinical_patient.txt` (§11) : provenance d'acquisition **retrouvée le 21 nov. 2026** (cBioPortal datahub, étude `paad_tcga_pan_can_atlas_2018`, URL exacte au §11, SHA-256 vérifié identique). Avant §8.77, la provenance était manquante (voir `PROVENANCE_testC_stage.md`) et le fichier non re-téléchargeable depuis une source connue. Cette sous-section est conservée pour l'historique : la lacune a existé du 15 au 21 nov. 2026, elle est désormais close.
(Source : `PROVENANCE_testC_stage.md`, chantier §8.77)""",
)

# --- §17 : bilan revise
rep(
    """**Fichiers bruts dont l'URL est manquante ou partielle : 19 fichiers** (5 ng3398 + 5 Birnbaum + 2 ICGC + 1 PRISM meta + 4 PRISM 19Q4 via API + 2 QCMG) **+ 4 fichiers CPTAC accessibles uniquement via l'API Zenodo** (page du record consignée) **+ 1 fichier hors `data/` sans aucune provenance** (`data_clinical_patient.txt`) **+ 1 fichier non conservé** (SOFT GPL20769). Tous les autres bruts ont une URL exacte consignée et vérifiable.""",
    """**Bilan révisé §8.77 (21 nov. 2026) : 19/19 fichiers FERMÉS, plus les 4 fichiers CPTAC (URL directes désormais consignées, §6), le fichier clinique du test C (provenance retrouvée, §11) et le SOFT GPL20769 (URL retrouvée et vérifiée, §3.1).** Le détail gap par gap est au §29. Il ne reste **aucun fichier brut sans URL de téléchargement** dans ce document : chaque URL a été retrouvée depuis une source lue (page DOI, FTP GEO, API figshare/Zenodo/GitHub, hub Xena) ou reconstruite puis **vérifiée par le SHA-256 du fichier re-téléchargé**. Les deux voies restées infructueuses en cours de route sont consignées au §29 (listing S3 403, Europe PMC supplementaryFiles HTTP 500, chemin `GPL2nnn/` 404) — elles ne cachent aucun gap restant.""",
)

# --- Annexe A : mise a jour (le script corrige couvre desormais les cas manuels)
rep(
    """# 2. Vérifications manuelles complémentaires (fichiers hors script)
python3 ~/workspace/runs/pdac-v6/download_gpl6244_mapping.py   # GPL6244_probe2symbol.tsv
# PRISM 19Q4 (les 2 fichiers manquants du script) : via API figshare
curl -s https://api.figshare.com/v2/articles/9393293 | python3 -c "import json,sys; [print(f['name'], f['download_url']) for f in json.load(sys.stdin)['files']]"
# CPTAC : via API Zenodo
curl -s https://zenodo.org/api/records/8394329 | python3 -c "import json,sys; [print(f['key'], f['links']['self']) for f in json.load(sys.stdin)['files']]""",
    """# 2. Vérifications manuelles complémentaires (depuis §8.77, la plupart des
# fichiers sont désormais DANS le script corrigé ; il ne reste hors script
# que la table GPL6244, dérivée du SOFT)
python3 ~/workspace/runs/pdac-v6/download_gpl6244_mapping.py   # GPL6244_probe2symbol.tsv
# PRISM 19Q4 : les 4 fichiers sont dans le script corrigé (§8.77) ; rappel
# des URL directes (API figshare) :
curl -s https://api.figshare.com/v2/articles/9393293 | python3 -c "import json,sys; [print(f['name'], f['download_url']) for f in json.load(sys.stdin)['files']]"
# CPTAC : dans le script corrigé via l'API Zenodo (§8.77) ; rappel :
curl -s https://zenodo.org/api/records/8394329 | python3 -c "import json,sys; [print(f['key'], f['links']['self']) for f in json.load(sys.stdin)['files']]""",
)

# --- Nouvelles sections §28 (§8.76) et §29 (§8.77), inserees avant l'Annexe A
SECTION_28_29 = """
## 28. Lot Yeh_seq FNA — GSE131050, robustesse appariée (§8.76, 20–21 nov. 2026)

**Aucun nouveau téléchargement dans ce chantier** : le fichier source est
celui téléchargé officiellement au §8.74 (20 nov. 2026), SHA re-vérifié
identique avant le gel et avant la construction (voir `PROVENANCE_876.md`,
SHA `82672091…`). Protocole gelé `PROTOCOL_maxsep_gse131050_fna_876.md`
(SHA `dd7937ee…`).

- **Série : GSE131050**, NCBI GEO — Rashid et coll., *Clin Cancer Res*
  2020, 26(1):82–92, PMID 31754050, doi 10.1158/1078-0432.CCR-19-1467
  (UNC Lineberger, Chapel Hill, USA). BioProject PRJNA542388, SRA
  SRP197641. Sous-série [RNA-Seq] de la SuperSeries GSE131049.
- **Fichiers source (déjà dans `data/`, §26) :**
  - `data/GSE131050_PurIST_Yeh_seq.tsv.gz` — 9 468 179 o, SHA-256
    `2fc0a66ef0ac62aab17e9bda1c78561786f887a9122591a9346a868f852be5b1`
    — URL : `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/suppl/GSE131050_PurIST_Yeh_seq.tsv.gz`
  - `data/GSE131050-GPL18573_series_matrix.txt.gz` — 6 864 o, SHA-256
    `9b333eb6b9181fedfc793b9a61f5970af459a5b37b8aa8f7808a3b6c34c7843e`
    — URL : `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE131nnn/GSE131050/matrix/GSE131050-GPL18573_series_matrix.txt.gz`
- **Lot FNA :** 42 codes-tumeurs (45 colonnes FNA primaires regroupées
  par code `MMDDT#`, médiane pour les 2 codes à réplicats) ; 41 codes sur
  42 sont les MÊMES tumeurs que le lot FF du §8.74 — le lot FNA n'est PAS
  une treizième paire principale indépendante et n'entre pas dans le compte
  A2 (12 paires) : c'est un test de robustesse apparié (mêmes tumeurs,
  autre type d'échantillon : FNA ex-vivo, kit TruSeq RNA Exome, échelle
  KRAS ~4 fois plus basse que FF). Verdict §8.76 : CONFIRME, d_maxsep
  +0,1642 (réel 0,4104+… — voir §8.76 ; test apparié, mêmes patients
  que FF).
- **Flux produits :** `data_flux/pdac_876_yeh_fna_fluxes.csv` (42 lignes,
  SHA `70697b3a…210324`), nul graine 42 SHA `2474ceaf…4d35`. Manifeste
  `manifest_v62_876.txt` (SHA `0e63d732…9f7`). Détail au §8.76 et dans
  `PROVENANCE_876.md`.

---

## 29. Chantier §8.77 — réparation de la reproductibilité (21 nov. 2026)

**Objet :** fermer les gaps du §17 (19 fichiers bruts sans URL + SOFT
GPL20769 + clinique du test C sans provenance + URL reconstruite de
`mit_test.csv` + URL directes CPTAC) **sans toucher aux verdicts déjà
écrits** (règle de Zackary, 20 nov. 2026, 19h40 : section à part, sans
réécrire l'histoire). Protocole gelé avant les travaux :
`PROTOCOL_reproductibilite_877.md` (SHA-256
`dbe1746f7233e69a3052407576ebf6043080016c97a12d41f76244fc569a4030`,
21 nov. 2026, 01h37 UTC). Pipeline v6.2 SHA
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant et après les runs, inchangé). Dossier de travail :
`~/workspace/runs/pdac-v6/repro_877/` (re-téléchargements dans
`repro_877/downloads/`, test à froid dans `repro_877/cold/` ; journal
`repro_877/JOURNAL_877.md`).

### 29.1 Résultat gap par gap (toutes les URL vérifiées par SHA-256)

| Gap | Fichiers | URL retrouvée (source lue) | Vérification |
|---|---|---|---|
| ng3398 MOESM59–63 | 5 | `static-content.springer.com/esm/art%3A10.1038%2Fng.3398/MediaObjects/41588_2015_BFng3398_MOESM{n}_ESM.{ext}` (patron Springer attesté par Bailey MOESM270, §5.5 ; page Nature ng.3398 lue) | 5/5 tailles + SHA-256 identiques (§3.2) |
| Birnbaum MOESM1–5 | 5 | `static-content.springer.com/esm/art%3A10.1186%2Fs12943-017-0739-z/MediaObjects/12943_2017_739_MOESM{n}_ESM.xlsx` (page PMC5674743 lue, DOI 10.1186/s12943-017-0739-z) | 5/5 tailles + SHA-256 identiques (§13) |
| ICGC probe map | 1 | `https://icgc.xenahubs.net/download/PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp.gz` (hub Xena) | taille 353 314 o, SHA `b09a746f…75537` (§5.3) |
| ICGC NMF | 1 | `https://icgc.xenahubs.net/download/PACA-AU/nature16965-s2_NMF_class_assignment.txt.gz` (hub Xena ; le `.txt` nu = 404) | taille 447 o, SHA `f1e84b99…21e2f` (§5.4) |
| PRISM 24Q2 meta | 1 | `https://ndownloader.figshare.com/files/46630978` (API figshare 25917643, fichier 46630978) | taille 157 294 o, SHA `13a85da9…3b0526` (§7) |
| PRISM 19Q4 (4 fichiers) | 4 | `https://ndownloader.figshare.com/files/20237739` (dose-response), `…/20237763` (replicate-collapsed), `…/20237769` (cell-line-info), `…/20238123` (readme) — API figshare 9393293 | 4/4 tailles + MD5 + SHA-256 identiques (§8) |
| QCMG clinique | 2 | `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_qcmg_uq_2016/data_clinical_patient.txt` (+ `…_sample.txt`) | SHA `ae7fc6d7…6a95` / `c70daf3e…ceca` (§12) |
| Clinique test C | 1 | `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_tcga_pan_can_atlas_2018/data_clinical_patient.txt` (étude `paad_tcga_pan_can_atlas_2018`) | taille 58 621 o, SHA `0c274268…2efe5` (§11) |
| SOFT GPL20769 | 1 | `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL20nnn/GPL20769/soft/GPL20769_family.soft.gz` | taille 37 588 662 o exactement, table 19 749 lignes, MD5 `4c39e802…`, SHA `ecb1b79a…22d3e` (§3.1) |
| `mit_test.csv` | 1 | `https://raw.githubusercontent.com/ncats/PANC1/main/MIT/test.csv` (URL reconstruite, vérifiée) | taille 3 249 228 o, SHA `9f3ae189…6e27` (§10) |
| CPTAC (4 fichiers) | 4 | `https://zenodo.org/api/records/8394329/files/<nom>/content` (champ `links.self` lu dans l'API Zenodo) | tailles + MD5 conformes (§6) |

**Bilan : 19/19 fichiers du §17 fermés + SOFT GPL20769 + clinique du test
C + `mit_test.csv` + URL directes CPTAC. Aucun gap irrécupérable. Aucune
URL inventée sans vérification SHA.**

### 29.2 Voies infructueuses consignées (échecs honnêtes, aucun gap caché)

- Listing du bucket S3 Xena : HTTP 403 ; URL S3 directes des fichiers
  ICGC : 403 — c'est l'URL du hub `icgc.xenahubs.net` qui fonctionne.
- Europe PMC `supplementaryFiles` pour PMC5674743 : HTTP 500 (page HTML
  d'erreur, 19 606 o) — les suppléments Birnbaum ont été récupérés par
  le patron Springer direct, vérifié par SHA.
- Page Nature ng.3398 via curl : HTTP 303, section suppléments non
  lisible par ce moyen ; la page lue par le navigateur confirme le titre
  et l'article, les URL ont été vérifiées par SHA.
- Chemin FTP GEO `GPL2nnn/GPL20769/` : 404 — le bon chemin est
  `GPL20nnn/` (règle des 3 derniers chiffres masqués).
- `raw.githubusercontent.com` pour les fichiers datahub : renvoie le
  pointeur Git LFS (130 o), pas le contenu — le contenu réel est servi
  par `media.githubusercontent.com`. Le pointeur LFS du fichier test C
  porte lui-même `oid sha256:0c274268…` (double confirmation).

### 29.3 Script corrigé

`repro_877/download_data_877.sh` (SHA-256
`48a1c41c5deacaf27da778cf535e940458990a1170df9e616e4683aa7b8bf3c3`,
diff `repro_877/download_data_877.diff`, 147 lignes changées) — corrections
§4 du protocole : PANC-1 fichier par fichier (tarball tronqué), PRISM
19Q4 4/4, PRISM 24Q2 avec hachages + métadonnées, suppléments ng3398 et
Birnbaum, SOFT GPL20769 (chemin corrigé), ICGC probe map/NMF, QCMG,
clinique PanCanAtlas ; CPTAC : URL directes en commentaire (voie API
conservée). L'original `~/workspace/staging-pdac/download_data.sh`
(SHA `4e151d59…`) n'a pas été modifié par ce chantier.

### 29.4 Test à froid (TCGA v4, réel + nul)

Voir §8.77 §5 pour les chiffres comparés. Chaîne complète, dossier
propre `repro_877/cold/` : re-téléchargement TCGA via l'extrait littéral
du script corrigé (`cold/cold_tcga.sh`, 4 tarballs OK, MD5 vérifiés ;
PAAD RSEM SHA-256 `c3dd138b…62c9` = §2.1) → reconstruction des flux par
copie de `build_fluxes_tcga_v4.py` (seules les 2 constantes de chemins
changées, diff consigné) → flux reconstruits **SHA-identiques** aux flux
tenus (`e7a2adab…0b0`, `895a4562…da4`) → runs v6.2 mode `fast`
(unités `repro877-cold-runs`, journal `cold/runs_cold_877.log`) →
extraction par `extract_858.extract`, comparaison aux chiffres tenus
(§8.37). Le script corrigé complet (~2,4 Go) a aussi été exécuté en
entier (unité `repro877-cold-full`, journal
`cold/full_script_877.log`) — résultat au §8.77.

### 29.5 Ce qui reste ouvert

**Rien** sur les fichiers bruts : chaque fichier brut du projet a
désormais une URL de téléchargement vérifiée par SHA-256. Restent hors
périmètre (déjà documentés, non rouverts) : les fichiers dérivés se
reconstruisent par scripts (§14) ; les résultats `results_fast_*` (~7 Go)
ne sont pas dans le dépôt par limite snapshot mais se reconstruisent par
les runs (le test à froid le démontre pour la paire TCGA v4) ; les
matrices brutes (~2,4 Go) ne sont pas dans le dépôt par limite snapshot
mais se re-téléchargent vérifiées par le script corrigé.
"""

anchor = "## Annexe A — Commandes de vérification (après re-téléchargement)"
assert txt.count(anchor) == 1, "ancre Annexe A introuvable"
txt = txt.replace(anchor, SECTION_28_29.strip("\n") + "\n\n" + anchor)
applied.append("§28 + §29 inserees avant Annexe A")

with open(DST, "w", encoding="utf-8") as f:
    f.write(txt)

print(f"Remplacements appliques : {len(applied)}")
for a in applied:
    print(" -", a)
