# Registre des sources — Projet PDAC v6

**Projet :** recherche non clinique sur le cancer du pancréas (pipeline v6, livre blanc public).
**Date de compilation :** 16 novembre 2026.
**Règle appliquée (Zackary, 27 oct. 2026) :** provenance toujours nommée — aucune source citée sans son URL complète. Aucune URL n'a été inventée : quand une recherche web n'a pas confirmé l'URL, la source est marquée « non vérifiée » et listée en §7.
**Périmètre :** toutes les sources citées dans les 25 fichiers `PROVENANCE_*.md` et les 39 fichiers `*.md` de `~/workspace/runs/pdac-v6/`, ainsi que dans le livre blanc `livre-blanc-pdac-v6.md`. Le code du pipeline v6 lui-même n'y figure pas : il reste privé par règle permanente de Zackary.
**Vérification :** les URL marquées « vérifiée » figuraient déjà dans un fichier de provenance ; celles marquées « trouvée par recherche web » ont été confirmées par recherche le 16 novembre 2026.

## Légende des statuts

- ✅ **Vérifiée** — URL présente dans un fichier de provenance du dossier `pdac-v6` (ou dans un rapport du même dossier).
- 🔎 **Trouvée par recherche web** — URL confirmée par recherche web le 16 novembre 2026 (absente des fichiers de provenance).
- ⚠️ **Lien mort + miroir** — l'URL d'origine ne fonctionne plus ; le miroir indiqué fonctionne.
- ❌ **Introuvable / non vérifiée** — aucune URL confirmée ; la source est reprise en §7 avec la raison.

## Compteurs par catégorie

| Catégorie | Nombre |
|---|---|
| 1. Jeux de données | 23 |
| 2. Articles scientifiques | 71 |
| 3. Essais cliniques | 59 |
| 4. Communiqués / pages web | 21 |
| 5. Dépôts GitHub | 3 |
| 6. Outils / logiciels / bases de données | 12 |
| **Total (sources tabulées)** | **189** |

---

## 1. Jeux de données

| Source (nom exact) | Type | URL complète | Statut | Noté où |
|---|---|---|---|---|
| DepMap Public 24Q4 — CRISPRGeneEffect.csv | Jeu de données | https://ndownloader.figshare.com/files/51064667 (figshare, article 27993248, DOI 10.25452/figshare.plus.27993248.v1 ; 428 678 699 o, SHA `3d8f3ec6…167e3b`) | ✅ Vérifiée | PROVENANCE_depmap.md |
| DepMap Public 24Q4 — Model.csv | Jeu de données | https://ndownloader.figshare.com/files/51065297 | ✅ Vérifiée | PROVENANCE_depmap.md |
| DepMap Public 24Q4 — OmicsSomaticMutationsMatrixHotspot.csv | Jeu de données | https://ndownloader.figshare.com/files/51065750 | ✅ Vérifiée | PROVENANCE_depmap.md |
| DepMap Public 24Q4 — OmicsSomaticMutationsMAFProfile.maf | Jeu de données | https://ndownloader.figshare.com/files/51065741 | ✅ Vérifiée | PROVENANCE_depmap.md |
| DepMap Public 24Q4 — OmicsProfiles.csv | Jeu de données | https://ndownloader.figshare.com/files/51065723 | ✅ Vérifiée | PROVENANCE_depmap.md |
| DepMap Public 24Q4 — OmicsCNGene.csv | Jeu de données | https://api.figshare.com/v2/file/download/51065324 (1 394 554 236 o, MD5 `4696565fa74dc805983bc278b4a41802`) | ✅ Vérifiée | PROVENANCE_depmap.md |
| TCGA-PAAD, Firehose stddata 2016-01-28 (RNA-seq RSEM) | Jeu de données | https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/PAAD/20160128/ (tarball RSEM MD5 `b09569ce3f4721f514bc137bd109ac0a` ; 178 tumeurs primaires) | ✅ Vérifiée | PROVENANCE_tcga.md, PROVENANCE_tcga_v2.md, PROVENANCE_tcga_v3.md, PROVENANCE_tcga_v4.md |
| TCGA-PAAD GISTIC2 (copy-number) | Jeu de données | https://gdac.broadinstitute.org/runs/analyses__2016_01_28/data/PAAD/20160128/ (tarball `PAAD-TP.CopyNumber_Gistic2.Level_4.2016012800.0.0.tar.gz`, MD5 `816034f742e8f89ca8734ca2cf4404d5`) | ✅ Vérifiée | PROVENANCE_tcga_v2.md |
| TCGA-LUAD, Firehose stddata 2016-01-28 | Jeu de données | https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/LUAD/20160128/ (MD5 observé `4c36eec3f6df75630292c5a569cfc8f4` ; 515 tumeurs) | ✅ Vérifiée | PROVENANCE_pancancer.md |
| TCGA-COAD, Firehose stddata 2016-01-28 | Jeu de données | https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/COAD/20160128/ (MD5 observé `e703a630556d42f098cf0df87d4712bb` ; 285 tumeurs) | ✅ Vérifiée | PROVENANCE_pancancer.md |
| GEO GSE71729 (Moffitt 2015, 145 tumeurs primaires, plateforme GPL20769) | Jeu de données | https://ftp.ncbi.nlm.nih.gov/geo/series/GSE71nnn/GSE71729/matrix/GSE71729_series_matrix.txt.gz (15 622 315 o, SHA `b2287893…536a54`) ; fiche : https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE71729 | ✅ Vérifiée | PROVENANCE_geo71729.md, PROVENANCE_geo71729_survival.md |
| GEO GSE62452 (69 tumeurs + 61 tissus normaux, plateforme GPL6244, PMID 27197190) | Jeu de données | https://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62452/matrix/GSE62452_series_matrix.txt.gz (SHA `8f41d5b3…078cba`) ; fiche : https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE62452 | ✅ Vérifiée | PROVENANCE_geo62452.md |
| ICGC PACA-AU — portail DCC (origine) | Jeu de données | https://dcc.icgc.org/api/v1/download?fn=/current/Projects/PACA-AU/donor.PACA-AU.tsv.gz | ⚠️ Lien mort + miroir | PROVENANCE_icgc.md |
| ICGC PACA-AU — miroir expression UCSC Xena | Jeu de données | https://icgc-xena-hub.s3.amazonaws.com/download/PACA-AU/nature16965-s2_normalised_exp.txt.gz (SHA `c2cb57af…0f49fa`) ; sous-types NMF : `nature16965-s2_NMF_class_assignment.txt` (même dossier) | ✅ Vérifiée | PROVENANCE_icgc.md |
| ICGC PACA-AU — clinique / survie (Bailey et al. 2016, Supplementary Tables 1–13) | Jeu de données | https://static-content.springer.com/esm/art%3A10.1038%2Fnature16965/MediaObjects/41586_2016_BFnature16965_MOESM270_ESM.xlsx (SHA `778224b3…4258a`) | ✅ Vérifiée | PROVENANCE_icgc.md |
| CPTAC PDAC (PDC000393) — miroir Zenodo du paquet `cptac` (PayneLab) | Jeu de données | https://zenodo.org/records/8394329 (DOI 10.5281/zenodo.8394329) ; API PDC : https://pdc.cancer.gov/graphql | ✅ Vérifiée | PROVENANCE_cptac.md |
| PRISM Repurposing 24Q2 — matrice primaire étendue | Jeu de données | https://figshare.com/articles/dataset/Repurposing_Public_24Q2/25917643 (DOI 10.6084/m9.figshare.25917643.v1) ; matrice : https://ndownloader.figshare.com/files/46630984 (72 456 953 o) ; liste des composés : https://ndownloader.figshare.com/files/46630981 | 🔎 Trouvée par recherche web | PROVENANCE_prism_secondary.md (article cité, fichiers confirmés par recherche) |
| PRISM Repurposing 19Q4 — matrice secondaire | Jeu de données | https://api.figshare.com/v2/articles/9393293 (figshare, article 9393293, DOI 10.6084/m9.figshare.9393293.v4) ; portail DepMap bloqué par Cloudflare Turnstile (vérifié 16 nov. 2026) | ⚠️ Portail bloqué, contournement API | PROVENANCE_prism_secondary.md |
| GDSC2 — fitted dose response (27 oct. 2023) | Jeu de données | https://cmp.cog.sanger.ac.uk/download/GDSC2_fitted_dose_response_27Oct23.xlsx (22 112 537 o, SHA `0e99120a…c899`) ; annotation des composés : https://cmp.cog.sanger.ac.uk/download/screened_compounds_rel_8.5.csv ; API : https://api.cellmodelpassports.sanger.ac.uk/download_files | ✅ Vérifiée | PROVENANCE_gdsc.md |
| PANC-1 (NCATS) — données CRISPR / lignées | Jeu de données | https://github.com/ncats/PANC1 (fichiers obtenus un par un via `raw.githubusercontent.com` ; git clone bloqué, tarball tronqué) ; Zenodo : https://doi.org/10.5281/zenodo.14230972 | ✅ Vérifiée | PROVENANCE_crispr_scan.md |
| HP35 — validation v6 (hors PDAC, données de référence) | Jeu de données | https://zenodo.org/records/23895045 (DOI 10.5281/zenodo.23895045 ; auteurs Wang, Bian, Ma) ; code associé : https://github.com/wyqmath/protein-backbone-elasticity | ✅ Vérifiée | ~/workspace/runs/biophysique-hp35/PROVENANCE.md ; livre blanc §8 |
| cBioPortal — études `paad_qcmg_uq_2016` et `paad_icgc` | Jeu de données | https://www.cbioportal.org/study/summary?id=paad_qcmg_uq_2016 et https://www.cbioportal.org/study/summary?id=paad_icgc | ⚠️ Écartées après vérification (ne correspondent pas aux données ICGC utilisées) | PROVENANCE_icgc.md |
| Synapse — identifiant syn4231880 (cité sans détail dans les fichiers) | Jeu de données | — (voir §7) | ❌ Introuvable / non vérifiée | Fichiers pdac-v6 (identifiant cité) |

---

## 2. Articles scientifiques

| Source (nom exact) | Type | URL complète | Statut | Noté où |
|---|---|---|---|---|
| Bailey et al., *Nature* 2016 (sous-types génomiques PDAC, ICGC PACA-AU) | Article | https://doi.org/10.1038/nature16965 | ✅ Vérifiée | PROVENANCE_icgc.md ; livre blanc §8 |
| Moffitt et al., *Nat Genet* 2015 (GSE71729, sous-types PDAC) | Article | https://doi.org/10.1038/ng.3398 | ✅ Vérifiée | PROVENANCE_geo71729.md |
| Hallin et al., *Nat Med* 2022 (MRTX1133, KRAS G12D) | Article | https://doi.org/10.1038/s41591-022-02007-7 | ✅ Vérifiée | PROVENANCE_kras_g12d.md |
| Drosten & Barbacid, *Mol Oncol* 2022 (KRAS, revue) | Article | https://doi.org/10.1002/1878-0261.13341 | ✅ Vérifiée | PROVENANCE_kras_g12d.md |
| Wolpin et al., *NEJM* 2026 ;394(18):1790–1802 (daraxonrasib phase I/II, NCT05379985) | Article | https://doi.org/10.1056/NEJMoa2505783 | ✅ Vérifiée | PROVENANCE_kras_combinations.md ; kras_combinations.md |
| O'Reilly et al., *N Engl J Med* 2026 ;395(4):325–337 (RASolute-302, daraxonrasib phase III) | Article | https://doi.org/10.1056/NEJMoa2605555 | 🔎 Trouvée par recherche web | Absent des fichiers (trouvé par recherche, 16 nov. 2026) |
| Kinsey et al., *Nat Med* 2019 (autophagie + MEK, PDAC) | Article | https://doi.org/10.1038/s41591-019-0367-9 | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| Witte et al., 2024 (titre non relevé dans les fichiers) | Article | https://doi.org/10.1007/s00432-024-05954-5 | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| Tang et al., *BMC Cancer* 2023 (titre non relevé dans les fichiers) | Article | https://doi.org/10.1186/s12885-023-11464-3 | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| Bedard et al. (titre non relevé dans les fichiers) | Article | https://doi.org/10.1158/1078-0432.CCR-14-1814 | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| Ma et al., *Cancers* 2022 (titre non relevé dans les fichiers) | Article | https://doi.org/10.3390/cancers14184467 | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| *Cancers* 2025, 17:1152 (titre non relevé dans les fichiers) | Article | https://doi.org/10.3390/cancers17071152 | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| Tapia Contreras et al., *Mol Oncol* 2025 ;19:295–310 (MRTX1133 + olaparib, modèles murins) | Article | https://doi.org/10.1002/1878-0261.13725 | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| *Nat Commun* 2026, 17:3118 (MRTX1133 + olaparib, PMID 41735281) | Article | https://doi.org/10.1038/s41467-026-69695-4 | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| *Cell Rep Med* 2025 (titre non relevé dans les fichiers) | Article | https://doi.org/10.1016/j.xcrm.2025.101966 | ✅ Vérifiée | PROVENANCE_immune_parp_v6.md |
| *Sci Rep* 2024 (titre non relevé dans les fichiers) | Article | https://doi.org/10.1038/s41598-024-57417-z | ✅ Vérifiée | PROVENANCE_immune_parp_v6.md |
| *J Hematol Oncol* 2026 (revue Springer, daraxonrasib + chimiothérapie 1re ligne, ORR 58 %) | Article | https://doi.org/10.1186/s13045-026-01863-x | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| *Front Immunol* 2026 (titre non relevé dans les fichiers) | Article | https://doi.org/10.3389/fimmu.2026.1845921 | ✅ Vérifiée | PROVENANCE_immune_v6.md |
| *J Clin Med* 2026 (titre non relevé dans les fichiers) | Article | https://doi.org/10.3390/jcm15145521 | ✅ Vérifiée | PROVENANCE_immune_v6.md |
| *Cancers* 2025, 17:2453 (titre non relevé dans les fichiers) | Article | https://doi.org/10.3390/cancers17152453 | ✅ Vérifiée | PROVENANCE_immune_v6.md |
| *Cancers* 2026, 18:3519 (revue, daraxonrasib, approbation FDA) | Article | https://doi.org/10.3390/cancers18213519 | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| *Front Oncol* 2024 (titre non relevé dans les fichiers) | Article | https://doi.org/10.3389/fonc.2024.1402128 | ✅ Vérifiée | PROVENANCE_parp_v6.md |
| *Turk J Gastroenterol* 2026 (titre non relevé dans les fichiers) | Article | https://doi.org/10.5152/tjg.2026.25595 | ✅ Vérifiée | PROVENANCE_parp_v6.md |
| *Front Immunol* 2023 (titre non relevé dans les fichiers) | Article | https://doi.org/10.3389/fimmu.2023.1223433 | ✅ Vérifiée | PROVENANCE_immune_v6.md |
| *Front Med* 2024 (titre non relevé dans les fichiers) | Article | https://doi.org/10.3389/fmed.2024.1369136 | ✅ Vérifiée | PROVENANCE_immune_v6.md |
| Zagidullin et al., *Nucleic Acids Res* 2019 (DrugComb) | Article | https://doi.org/10.1093/nar/gkz337 | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| Menden et al., *Nat Commun* 2019 (AZ-DREAM, combinaisons) | Article | https://doi.org/10.1038/s41467-019-09799-2 | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| Liu et al., *Ann Oncol* 2016 (DMUC5754A, anti-MUC16 ADC) | Article | https://doi.org/10.1093/annonc/mdw401 | ✅ Vérifiée | PROVENANCE_muc16_cldn182.md |
| Lin et al., *Mol Ther Oncolytics* 2024 ;32(4):200868 (« Muc16CD is a novel CAR T cell target antigen for the treatment of pancreatic cancer ») | Article | https://doi.org/10.1016/j.omton.2024.200868 ; PMC : https://pmc.ncbi.nlm.nih.gov/articles/PMC11426034/ | ✅ Vérifiée | PROVENANCE_muc16_cldn182.md ; muc16_cldn182_therapies.md |
| *Sci Rep* 2025, 15:9909 (« A bispecific anti-MUC16/anti-death receptor 5 antibody… ») | Article | https://doi.org/10.1038/s41598-025-93927-0 ; PMC : https://pmc.ncbi.nlm.nih.gov/articles/PMC11929789/ | ✅ Vérifiée | PROVENANCE_muc16_cldn182.md |
| *J Ovarian Res* 2023 (titre non relevé dans les fichiers) | Article | https://doi.org/10.1186/s13048-023-01325-9 | ✅ Vérifiée | PROVENANCE_muc16_cldn182.md |
| « Resistance mechanisms and countermeasures in CLDN18.2-positive tumors », *Front Oncol* 2026 | Article | https://doi.org/10.3389/fonc.2026.1910011 | ✅ Vérifiée | muc16_cldn182_therapies.md |
| *Front Oncol* 2026 (titre non relevé dans les fichiers) | Article | https://doi.org/10.3389/fonc.2026.1960663 | ✅ Vérifiée | PROVENANCE_muc16_cldn182.md |
| *Front Immunol* 2026 (titre non relevé dans les fichiers) | Article | https://doi.org/10.3389/fimmu.2026.1998845 | ✅ Vérifiée | PROVENANCE_immune_v6.md |
| « Research advances in targeting claudin 18.2 in pancreatic ductal adenocarcinoma treatment », *World J Gastroenterol* 2026 ;32(45):122906 | Article | http://www.wjgnet.com/1007-9327/full/v32/i45/122906.htm | ✅ Vérifiée | muc16_cldn182_therapies.md |
| Cao et al., *Cell* 2021 (dépendance MTAP/PRMT5, CRISPR) | Article | https://doi.org/10.1016/j.cell.2021.08.023 ; PMC : https://pmc.ncbi.nlm.nih.gov/articles/PMC8654574/ | 🔎 Trouvée par recherche web | PROVENANCE_mtap.md (cité sans DOI) |
| Mavrakis et al., *Science* 2016 (MTAP, délétion, PRMT5) | Article | https://doi.org/10.1126/science.aad5944 | 🔎 Trouvée par recherche web | PROVENANCE_mtap.md (cité sans DOI) |
| Kryukov et al., *Science* 2016 (MTAP, délétion, PRMT5) | Article | https://doi.org/10.1126/science.aad5214 | 🔎 Trouvée par recherche web | PROVENANCE_mtap.md (cité sans DOI) |
| Holbeck et al., 2017 (ALMANAC, criblage de combinaisons NCI) | Article | https://doi.org/10.1158/0008-5472.CAN-17-0489 ; données : https://dtp.cancer.gov/ncialmanac | 🔎 Trouvée par recherche web | PROVENANCE_kras_combinations.md (cité sans DOI) |
| O'Neil et al., 2016 (criblage de combinaisons, PDAC) | Article | https://doi.org/10.1158/1535-7163.MCT-15-0843 | 🔎 Trouvée par recherche web | PROVENANCE_kras_combinations.md (cité sans DOI) |
| Langdon et al., 2017 (criblage de combinaisons ; cité « Forcina et al. » dans les fichiers — voir §8) | Article | https://doi.org/10.1158/1535-7163.MCT-16-0794 | 🔎 Trouvée par recherche web | PROVENANCE_kras_combinations.md (cité sans DOI, premier auteur erroné) |
| Shitara et al., *Lancet* 2023 (SPOTLIGHT, zolbetuximab + mFOLFOX6) | Article | https://doi.org/10.1016/S0140-6736(23)00620-7 | 🔎 Trouvée par recherche web | PROVENANCE_muc16_cldn182.md (cité sans DOI) |
| Shah et al., *Nat Med* 2023 (GLOW, zolbetuximab + CAPOX) | Article | https://doi.org/10.1038/s41591-023-02465-7 | 🔎 Trouvée par recherche web | PROVENANCE_muc16_cldn182.md (cité sans DOI) |
| Qi et al., *Nat Med* 2022 (CT041 phase I, CAR-T CLDN18.2) | Article | https://doi.org/10.1038/s41591-022-01800-8 | 🔎 Trouvée par recherche web | PROVENANCE_muc16_cldn182.md (cité sans DOI) |
| Qi et al., *Lancet* 2025 (CT041-ST-01, CAR-T CLDN18.2) | Article | https://doi.org/10.1016/S0140-6736(25)00860-8 | 🔎 Trouvée par recherche web | PROVENANCE_muc16_cldn182.md (cité sans DOI) |
| Qi et al., *Nat Med* 2024 (CT041 phase I, résultats finaux) | Article | https://doi.org/10.1038/s41591-024-03037-z | 🔎 Trouvée par recherche web | PROVENANCE_muc16_cldn182.md (cité sans DOI) |
| Liu et al., *Gynecol Oncol* 2021 (DMUC4064A, ADC anti-MUC16) | Article | https://doi.org/10.1016/j.ygyno.2021.09.023 ; texte intégral : https://www.gynecologiconcology-online.net/article/S0090-8258(21)01403-7/fulltext | 🔎 Trouvée par recherche web | PROVENANCE_muc16_cldn182.md (cité sans DOI) |
| Wang et al., *Front Pharmacol* 2022 ;13:1093666 (revue ADC gynécologiques, DMUC5754A) | Article | https://doi.org/10.3389/fphar.2022.1093666 | 🔎 Trouvée par recherche web | PROVENANCE_muc16_cldn182.md (cité sans DOI) |
| Berek et al., *J Clin Oncol* 2009 (oregovomab, anti-CA125) | Article | https://doi.org/10.1200/JCO.2008.17.8400 | 🔎 Trouvée par recherche web | PROVENANCE_muc16_cldn182.md (cité sans DOI) |
| Sabbatini et al., *J Clin Oncol* 2013 (MIMOSA, abagovomab) | Article | https://doi.org/10.1200/JCO.2012.46.4057 | 🔎 Trouvée par recherche web | PROVENANCE_muc16_cldn182.md (cité sans DOI) |
| Xing et al., *Front Immunol* 2026 ;16:1638585 (« VHH-based CAR-T cells targeting Claudin 18.2 show high efficacy in pancreatic cancer models ») | Article | https://doi.org/10.3389/fimmu.2025.1638585 ; PMC : https://pmc.ncbi.nlm.nih.gov/articles/PMC12808354/ | 🔎 Trouvée par recherche web | muc16_cldn182_therapies.md (cité sans DOI ; 59,2 % de PDAC CLDN18.2+) |
| Kemp et al., *Cancer Discov* 2023 ;13:298–311 (« Efficacy of a Small-Molecule Inhibitor of KrasG12D in Immunocompetent Models of Pancreatic Cancer », MRTX1133) | Article | https://doi.org/10.1158/2159-8290.CD-22-1066 ; PMC : https://pmc.ncbi.nlm.nih.gov/articles/PMC9900321/ | 🔎 Trouvée par recherche web | PROVENANCE_kras_g12d.md (cité « Cancer Cell / Developmental Cell » — voir §8) |
| Ke et al., *Oxid Med Cell Longev* 2022 (« Systematic Analysis of Molecular Subtypes Based on the Expression Profile of Immune-Related Genes in Pancreatic Cancer », survie GSE71729) | Article | https://doi.org/10.1155/2022/3124122 | 🔎 Trouvée par recherche web | PROVENANCE_geo71729_survival.md (GSE71729 : 125 échantillons, 84 décès / 41 vivants) |
| Pourmousa et al., *Nat Commun* 2025 ;16:4020 (PANC-1, NCATS) | Article | https://doi.org/10.1038/s41467-025-56818-6 | ✅ Vérifiée | PROVENANCE_crispr_scan.md |
| Corsello et al., *Nat Cancer* 2020 ;1:235–248 (PRISM Repurposing) | Article | https://doi.org/10.1038/s43018-019-0018-6 | ✅ Vérifiée | PROVENANCE_prism_secondary.md |
| Koneru et al., *J Transl Med* 2015 ;13:102 (protocole phase I, CAR-T MUC16 sécrétant IL-12) | Article | https://doi.org/10.1186/s12967-015-0460-x ; PMC : https://pmc.ncbi.nlm.nih.gov/articles/PMC4438636/ | 🔎 Trouvée par recherche web | PROVENANCE_muc16_cldn182.md (cité sans DOI) |
| Cheng et al., *EBioMedicine* 2019 ;40:382–393 (biomarqueurs PDAC, GSE62452) | Article | https://doi.org/10.1016/j.ebiom.2019.01.003 | 🔎 Trouvée par recherche web | PROVENANCE_geo62452.md (PMID 27197190 cité pour GSE62452) |
| *Gastroenterology* 2024 (organoïdes PDAC, MRTX1133 ± EGFR, synergie spécifique G12D, 19 organoïdes) | Article | https://doi.org/10.1016/S0016-5085(24)05027-3 | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| *Clin Cancer Res* 2024 ;30(4):655–662 (MRTX1133 + anti-CTLA-4 + anti-PD-1, modèles murins autochtones) | Article | https://pmc.ncbi.nlm.nih.gov/articles/PMC10922474/ (DOI non relevé dans les fichiers) | ✅ Vérifiée | PROVENANCE_kras_combinations.md |
| *Cancer Immunol Immunother* 2023 ;72(11):3773–3786 (revue, cite O'Cearbhaill 2020) | Article | https://pmc.ncbi.nlm.nih.gov/articles/PMC10991175/ (DOI non relevé dans les fichiers) | ✅ Vérifiée | literature_muc16_cldn182_draft.md |
| « Emerging role of mucins in antibody drug conjugates for ovarian cancer therapy », *J Ovarian Res* 2024 ;17:161 | Article | https://pmc.ncbi.nlm.nih.gov/articles/PMC11308542/ (DOI non relevé dans les fichiers) | ✅ Vérifiée | literature_muc16_cldn182_draft.md |
| « Advances in KRAS-Targeted Therapies for Pancreatic Cancer » (revue) | Article | https://pmc.ncbi.nlm.nih.gov/articles/PMC13604613/ (DOI non relevé dans les fichiers) | ✅ Vérifiée | PROVENANCE_kras_g12d.md |
| « Therapeutic Advances in Medical Oncology » 2026 (revue) | Article | https://pmc.ncbi.nlm.nih.gov/articles/PMC13129282/ (DOI non relevé dans les fichiers) | ✅ Vérifiée | PROVENANCE_kras_g12d.md |
| Birnbaum et al., 2017 (titre non relevé dans les fichiers) | Article | https://pmc.ncbi.nlm.nih.gov/articles/PMC5674743/ (DOI non relevé dans les fichiers) | ✅ Vérifiée | PROVENANCE_muc16_cldn182.md |
| Mahadevan et al., *Cancer Cell* 2023 (MRTX1133 + blocage des points de contrôle immunitaires, 16 modèles) | Article | https://www.cell.com/cancer-cell/fulltext/S1535-6108(23)00242-8 (DOI non vérifié) | 🔎 Trouvée par recherche web (URL éditeur ; DOI non vérifié) | PROVENANCE_kras_g12d.md (cité via Kemp et al.) |
| Paquet `cptac` — article *Cell Systems* (accès unifié aux données protéogénomiques du cancer) | Article | https://www.sciencedirect.com/science/article/pii/S1535390721001906 (DOI non vérifié) | 🔎 Trouvée par recherche web (URL éditeur ; DOI non vérifié) | PROVENANCE_cptac.md |
| « CAR-T Cell Therapy in Ovarian Cancer: Where Are We Now ? » (revue, 2024) | Article | https://www.mdpi.com/2075-4418/14/8/819 | 🔎 Trouvée par recherche web | literature_muc16_cldn182_draft.md |
| « The Landscape of Adoptive Cellular Therapies in Ovarian Cancer » (revue, entrée encyclopédique) | Article | https://encyclopedia.pub/entry/history/show/113627 | 🔎 Trouvée par recherche web | literature_muc16_cldn182_draft.md |
| PMC5457712 (référence citée sans titre relevé dans les fichiers) | Article | https://pmc.ncbi.nlm.nih.gov/articles/PMC5457712/ | ✅ Vérifiée (identifiant présent ; titre non relevé) | Fichiers pdac-v6 |
| PMC5499996 (référence citée sans titre relevé dans les fichiers) | Article | https://pmc.ncbi.nlm.nih.gov/articles/PMC5499996/ | ✅ Vérifiée (identifiant présent ; titre non relevé) | Fichiers pdac-v6 |
| PMC10427418 (référence citée sans titre relevé dans les fichiers) | Article | https://pmc.ncbi.nlm.nih.gov/articles/PMC10427418/ | ✅ Vérifiée (identifiant présent ; titre non relevé) | Fichiers pdac-v6 |

---

## 3. Essais cliniques

URL construite mécaniquement selon la règle de la tâche : `https://clinicaltrials.gov/study/NCTxxxxxxxx`. Statut « vérifiée » quand le numéro figure dans un fichier de provenance ou un rapport du dossier.

| Source (nom exact) | Type | URL complète | Statut | Noté où / contexte |
|---|---|---|---|---|
| NCT01335958 | Essai clinique | https://clinicaltrials.gov/study/NCT01335958 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT02146313 | Essai clinique | https://clinicaltrials.gov/study/NCT02146313 | ✅ Vérifiée | PROVENANCE_muc16_cldn182.md — DMUC4064A (ADC anti-MUC16) |
| NCT02498912 | Essai clinique | https://clinicaltrials.gov/study/NCT02498912 | 🔎 Trouvée par recherche web | Phase I MSK, CAR-T MUC16 sécrétant IL-12 (O'Cearbhaill 2020, Koneru 2015) |
| NCT03114319 | Essai clinique | https://clinicaltrials.gov/study/NCT03114319 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT03504397 | Essai clinique | https://clinicaltrials.gov/study/NCT03504397 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT03564340 | Essai clinique | https://clinicaltrials.gov/study/NCT03564340 | ✅ Vérifiée | muc16_cldn182_therapies.md — ubamatamab (IGCS 2026) |
| NCT03600883 | Essai clinique | https://clinicaltrials.gov/study/NCT03600883 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT03634982 | Essai clinique | https://clinicaltrials.gov/study/NCT03634982 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT03653507 | Essai clinique | https://clinicaltrials.gov/study/NCT03653507 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT03785249 | Essai clinique | https://clinicaltrials.gov/study/NCT03785249 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT03816163 | Essai clinique | https://clinicaltrials.gov/study/NCT03816163 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT03825289 | Essai clinique | https://clinicaltrials.gov/study/NCT03825289 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT03874897 | Essai clinique | https://clinicaltrials.gov/study/NCT03874897 | ✅ Vérifiée | PROVENANCE_muc16_cldn182.md — CT041 phase I (CAR-T CLDN18.2, Qi 2022) |
| NCT03907527 | Essai clinique | https://clinicaltrials.gov/study/NCT03907527 | ✅ Vérifiée | literature_muc16_cldn182_draft.md — CAR-T MUC16 (recrutement signalé) |
| NCT04000529 | Essai clinique | https://clinicaltrials.gov/study/NCT04000529 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT04111458 | Essai clinique | https://clinicaltrials.gov/study/NCT04111458 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT04185883 | Essai clinique | https://clinicaltrials.gov/study/NCT04185883 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT04330664 | Essai clinique | https://clinicaltrials.gov/study/NCT04330664 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT04404595 | Essai clinique | https://clinicaltrials.gov/study/NCT04404595 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT04498117 | Essai clinique | https://clinicaltrials.gov/study/NCT04498117 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT04528836 | Essai clinique | https://clinicaltrials.gov/study/NCT04528836 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT04581473 | Essai clinique | https://clinicaltrials.gov/study/NCT04581473 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT04590326 | Essai clinique | https://clinicaltrials.gov/study/NCT04590326 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT04613596 | Essai clinique | https://clinicaltrials.gov/study/NCT04613596 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT04627142 | Essai clinique | https://clinicaltrials.gov/study/NCT04627142 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT04699188 | Essai clinique | https://clinicaltrials.gov/study/NCT04699188 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT04835714 | Essai clinique | https://clinicaltrials.gov/study/NCT04835714 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT05054725 | Essai clinique | https://clinicaltrials.gov/study/NCT05054725 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT05164458 | Essai clinique | https://clinicaltrials.gov/study/NCT05164458 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT05379985 | Essai clinique | https://clinicaltrials.gov/study/NCT05379985 | ✅ Vérifiée | PROVENANCE_kras_combinations.md — RMC-6236-001, daraxonrasib phase I/II (Wolpin 2026) |
| NCT05382559 | Essai clinique | https://clinicaltrials.gov/study/NCT05382559 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT05458219 | Essai clinique | https://clinicaltrials.gov/study/NCT05458219 | ✅ Vérifiée | muc16_cldn182_therapies.md — IBI343 phase I pancréas (Yu 2025, ASCO) |
| NCT05518110 | Essai clinique | https://clinicaltrials.gov/study/NCT05518110 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT05533463 | Essai clinique | https://clinicaltrials.gov/study/NCT05533463 | ✅ Vérifiée | Fichiers pdac-v6 (statut « non vérifié » noté dans les fichiers ; URL mécanique) |
| NCT05737706 | Essai clinique | https://clinicaltrials.gov/study/NCT05737706 | ✅ Vérifiée | PROVENANCE_kras_g12d.md — MRTX1133 phase I/II, TERMINATED début 2025 (statut « non vérifié » noté dans les fichiers) |
| NCT05846516 | Essai clinique | https://clinicaltrials.gov/study/NCT05846516 | ✅ Vérifiée | Fichiers pdac-v6 (statut « non vérifié » noté dans les fichiers ; URL mécanique) |
| NCT05920356 | Essai clinique | https://clinicaltrials.gov/study/NCT05920356 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06040541 | Essai clinique | https://clinicaltrials.gov/study/NCT06040541 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06119581 | Essai clinique | https://clinicaltrials.gov/study/NCT06119581 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06128551 | Essai clinique | https://clinicaltrials.gov/study/NCT06128551 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06162221 | Essai clinique | https://clinicaltrials.gov/study/NCT06162221 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06219941 | Essai clinique | https://clinicaltrials.gov/study/NCT06219941 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06346392 | Essai clinique | https://clinicaltrials.gov/study/NCT06346392 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06351020 | Essai clinique | https://clinicaltrials.gov/study/NCT06351020 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06385925 | Essai clinique | https://clinicaltrials.gov/study/NCT06385925 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06445062 | Essai clinique | https://clinicaltrials.gov/study/NCT06445062 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06520488 | Essai clinique | https://clinicaltrials.gov/study/NCT06520488 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06586515 | Essai clinique | https://clinicaltrials.gov/study/NCT06586515 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06607185 | Essai clinique | https://clinicaltrials.gov/study/NCT06607185 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06625320 | Essai clinique | https://clinicaltrials.gov/study/NCT06625320 | ✅ Vérifiée | PROVENANCE_kras_combinations.md — RASolute-302, daraxonrasib phase III (O'Reilly 2026) |
| NCT06625775 | Essai clinique | https://clinicaltrials.gov/study/NCT06625775 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT06922591 | Essai clinique | https://clinicaltrials.gov/study/NCT06922591 | ✅ Vérifiée | PROVENANCE_mtap.md — vopimetostat + daraxonrasib phase 1/2 (MTAP-délétés) |
| NCT07066098 | Essai clinique | https://clinicaltrials.gov/study/NCT07066098 | ✅ Vérifiée | PROVENANCE_muc16_cldn182.md — IBI343 phase III |
| NCT07066995 | Essai clinique | https://clinicaltrials.gov/study/NCT07066995 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT07108504 | Essai clinique | https://clinicaltrials.gov/study/NCT07108504 | ✅ Vérifiée | muc16_cldn182_therapies.md — voir aussi DecenTrialz, §4 |
| NCT07252232 | Essai clinique | https://clinicaltrials.gov/study/NCT07252232 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT07385703 | Essai clinique | https://clinicaltrials.gov/study/NCT07385703 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT07491445 | Essai clinique | https://clinicaltrials.gov/study/NCT07491445 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |
| NCT07805954 | Essai clinique | https://clinicaltrials.gov/study/NCT07805954 | ✅ Vérifiée | Fichiers pdac-v6 (contexte non précisé) |

---

## 4. Communiqués / pages web

| Source (nom exact) | Type | URL complète | Statut | Noté où |
|---|---|---|---|---|
| FDA — approbation du zolbetuximab (18 oct. 2024) | Communiqué / page web | https://www.fda.gov/drugs/resources-information-approved-drugs/fda-approves-zolbetuximab-clzb-chemotherapy-gastric-or-gastroesophageal-junction-adenocarcinoma | ✅ Vérifiée | PROVENANCE_muc16_cldn182.md |
| FDA — approbation du daraxonrasib (RASONQUE™, 26 août 2026) | Communiqué / page web | https://www.fda.gov/news-events/press-announcements/fda-approves-first-class-targeted-therapy-metastatic-pancreatic-cancer | 🔎 Trouvée par recherche web | PROVENANCE_kras_combinations.md (cité sans URL) |
| Astellas — communiqué GLEAM (14 oct. 2025, essai n'ayant pas atteint le critère principal) | Communiqué / page web | https://www.drugs.com/clinical_trials/astellas-confirms-phase-2-gleam-trial-did-not-meet-primary-endpoint-overall-survival-patients-22199.html (relais Drugs.com) | ✅ Vérifiée | PROVENANCE_muc16_cldn182.md |
| Tango Therapeutics — communiqué du 23 oct. 2026 (vopimetostat + daraxonrasib, ORR 82 %, 18/22, coupure 20 août 2026, phase 3 prévue 1H 2027) | Communiqué / page web | https://www.nasdaq.com/press-release/tango-presents-promising-results-phase-1-2-study-vopimetostat-and-daraxonrasib (relais GlobeNewswire) ; dépôt SEC 8-K exhibit 99.1 confirmé | 🔎 Trouvée par recherche web | PROVENANCE_mtap.md (cité sans URL exacte) |
| CARsgen — communiqué du 20 oct. 2025 | Communiqué / page web | http://www.m2pharma.com/news/therapy-areas/oncology/article.php?id=106851 (relais M2 Pharma) | ✅ Vérifiée | PROVENANCE_muc16_cldn182.md |
| OnCo — dossier CLDN18.2 | Page web | https://onco.cc/dossiers/cldn18-2/ | ✅ Vérifiée | muc16_cldn182_therapies.md |
| DecenTrialz — fiche NCT07108504 | Page web | https://decentrialz.com/clinical-trials/NCT07108504/ | ✅ Vérifiée | muc16_cldn182_therapies.md |
| Innovent — communiqué IBI343 (PR Newswire Asia, ASCO 2025) | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | muc16_cldn182_therapies.md |
| Innovent — communiqué IBI389 (ASCO 2024) | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | muc16_cldn182_therapies.md |
| Revolution Medicines — communiqué RASolute-303 (2 avril 2026) | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | PROVENANCE_kras_combinations.md |
| Revolution Medicines — communiqué RASolute-309 (5 oct. 2026) | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | PROVENANCE_kras_combinations.md |
| ESMO 2026 — poster 3149P (Spira et al., daraxonrasib) | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | PROVENANCE_kras_combinations.md |
| ESMO 2026 — analyses de sous-groupes daraxonrasib | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | kras_combinations.md |
| Avis positif CHMP / EMA (15 oct. 2026, daraxonrasib) | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | kras_combinations.md |
| OncLive — 23 oct. 2026 (ubamatamab, Van Nieuwenhuysen, IGCS 2026) | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | muc16_cldn182_therapies.md |
| Whitehawk Therapeutics — transcription d'appel résultats (fév. 2026, HWK-016, arrêt de DMUC4064A) | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | literature_muc16_cldn182_draft.md |
| Park et al. — ESMO GI 2026, résumé 342O | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | muc16_cldn182_therapies.md |
| INCB161734 (honcology.com) | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | PROVENANCE_kras_g12d.md |
| Setidegrasib (cité sans référence exploitable) | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | PROVENANCE_kras_g12d.md |
| *Drug Discov Ther* 2026 ;20:400–402 (daraxonrasib) | Communiqué / page web | — (voir §7) | ❌ Introuvable / non vérifiée | PROVENANCE_kras_combinations.md |
| Brevet américain (cité sans numéro dans les fichiers) | Page web | — (voir §7) | ❌ Introuvable / non vérifiée | PROVENANCE_kras_g12d.md |

---

## 5. Dépôts GitHub

| Source (nom exact) | Type | URL complète | Statut | Noté où |
|---|---|---|---|---|
| ncats/PANC1 (données PANC-1, NCATS) | Dépôt GitHub | https://github.com/ncats/PANC1 | ✅ Vérifiée | PROVENANCE_crispr_scan.md |
| wyqmath/protein-backbone-elasticity (code associé à HP35) | Dépôt GitHub | https://github.com/wyqmath/protein-backbone-elasticity | ✅ Vérifiée | ~/workspace/runs/biophysique-hp35/PROVENANCE.md |
| PayneLab/cptac (paquet Python `cptac`) | Dépôt GitHub | https://github.com/PayneLab/cptac ; documentation : https://paynelab.github.io/cptac/ | 🔎 Trouvée par recherche web | PROVENANCE_cptac.md (paquet cité, URL confirmée par recherche) |

*Note : aucun dépôt du pipeline v6 n'est listé ici — le pipeline reste privé par règle permanente.*

---

## 6. Outils / logiciels / bases de données

| Source (nom exact) | Type | URL complète | Statut | Noté où |
|---|---|---|---|---|
| DrugComb (base de données de combinaisons, Zagidullin 2019) | Outil / base de données | https://drugcomb.org/ ; téléchargements : https://drugcomb.org/downloads ; https://drugcombdb.drugcomb.org/ | ⚠️ Injoignable depuis la VM le 16 nov. 2026 (curl HTTP 000, exit 52 ; contrôle google.com OK) | PROVENANCE_kras_combinations.md |
| ALMANAC (NCI DTP, criblage de combinaisons) | Outil / base de données | https://dtp.cancer.gov/ncialmanac | 🔎 Trouvée par recherche web | PROVENANCE_kras_combinations.md |
| ChEMBL (MRTX1133 : CHEMBL4858364, 45 activités ; daraxonrasib : CHEMBL6168538, 85 activités ; RMC-9805 / ASP3082 : 0 résultat) | Outil / base de données | https://www.ebi.ac.uk/chembl/ (identifiants CHEMBL4858364 et CHEMBL6168538 cités dans les fichiers) | ✅ Vérifiée | PROVENANCE_kras_g12d.md ; PROVENANCE_kras_combinations.md |
| DGIdb (Drug Gene Interaction Database) | Outil / base de données | https://dgidb.org/ (API REST non exploitable — renvoie la page JS ; GraphQL sans réponse — « à vérifier », rien inventé) | ⚠️ Accès API non vérifié | PROVENANCE_kras_combinations.md |
| cBioPortal (portail) | Outil / base de données | https://www.cbioportal.org/ | ✅ Vérifiée | PROVENANCE_icgc.md |
| UCSC Xena (portail et hub ICGC) | Outil / base de données | https://xenabrowser.net/datapages/ | ✅ Vérifiée | PROVENANCE_icgc.md |
| Cell Model Passports (portail GDSC2) | Outil / base de données | https://cellmodelpassports.sanger.ac.uk/ ; API : https://api.cellmodelpassports.sanger.ac.uk/download_files | ✅ Vérifiée | PROVENANCE_gdsc.md |
| DepMap Portal | Outil / base de données | https://depmap.org/portal/ (bloqué par Cloudflare Turnstile, vérifié 16 nov. 2026, 12h43) | ⚠️ Portail bloqué | PROVENANCE_prism_secondary.md |
| figshare (API, articles 27993248, 25917643, 9393293) | Outil / base de données | https://api.figshare.com/v2/articles/9393293 | ✅ Vérifiée | PROVENANCE_depmap.md ; PROVENANCE_prism_secondary.md |
| PDC API (Proteomic Data Commons, GraphQL) | Outil / base de données | https://pdc.cancer.gov/graphql (testée, répond, introspection désactivée) | ✅ Vérifiée | PROVENANCE_cptac.md |
| ICGC DCC Portal (origine, mort) | Outil / base de données | https://dcc.icgc.org/ (redirige vers https://dcc.icgc.org/index.html ; vérifié 16 nov. 2026) | ⚠️ Lien mort + miroir (UCSC Xena, §1) | PROVENANCE_icgc.md |
| Paquet Python `cptac` (PayneLab) | Outil / logiciel | https://github.com/PayneLab/cptac ; https://paynelab.github.io/cptac/ | 🔎 Trouvée par recherche web | PROVENANCE_cptac.md |

---

## 7. Sources sans URL (aucune URL confirmée)

### 7a. Sources tabulées ci-dessus, marquées ❌ (15)

| Source | Raison de l'absence d'URL |
|---|---|
| Synapse — identifiant syn4231880 | Identifiant cité dans les fichiers ; URL exacte du dossier Synapse non vérifiée par recherche. |
| Innovent — communiqué IBI343 (PR Newswire Asia, ASCO 2025) | Communiqué cité dans `muc16_cldn182_therapies.md` ; URL exacte non retrouvée par recherche. |
| Innovent — communiqué IBI389 (ASCO 2024) | Communiqué cité ; URL exacte non retrouvée par recherche. |
| Revolution Medicines — communiqué RASolute-303 (2 avril 2026) | Événement confirmé (GlobeNewswire) ; URL exacte non retrouvée. |
| Revolution Medicines — communiqué RASolute-309 (5 oct. 2026) | Événement confirmé (GlobeNewswire) ; URL `ir.revmed.com` citée tronquée dans une source secondaire (`…/revolution-medicines-begins-treating-patients-phase-3-rasolute-0`) — non utilisable telle quelle ; miroir CentralCharts signalé, URL non relevée. |
| ESMO 2026 — poster 3149P (Spira et al., daraxonrasib) | Résumé/poster cité ; URL exacte non retrouvée. |
| ESMO 2026 — analyses de sous-groupes daraxonrasib | Cité dans `kras_combinations.md` ; URL exacte non retrouvée. |
| Avis positif CHMP / EMA (15 oct. 2026, daraxonrasib) | Avis cité ; URL exacte de l'avis EMA non retrouvée. |
| OncLive — 23 oct. 2026 (ubamatamab, Van Nieuwenhuysen, IGCS 2026) | Article relayé cité ; URL exacte non retrouvée. |
| Whitehawk Therapeutics — transcription d'appel résultats (fév. 2026, HWK-016, arrêt de DMUC4064A) | Déclaration d'entreprise citée ; URL exacte non retrouvée. |
| Park et al. — ESMO GI 2026, résumé 342O | Résumé de congrès cité ; URL exacte non retrouvée. |
| INCB161734 (honcology.com) | Molécule citée avec un site de référence ; URL exacte non retrouvée. |
| Setidegrasib | Nom cité sans référence exploitable (ni auteur, ni essai, ni DOI). |
| *Drug Discov Ther* 2026 ;20:400–402 (daraxonrasib) | Référence citée ; DOI non vérifié, URL non retrouvée. |
| Brevet américain (cité sans numéro) | Aucun numéro de brevet dans les fichiers ; impossible de construire l'URL. |

### 7b. Références citées dans les fichiers, sans URL vérifiable et sans ligne de tableau propre (6)

| Source | Raison |
|---|---|
| O'Cearbhaill et al., *Gynecol Oncol* 2020 ;159:42 (résumé SGO 2020, CAR-T MUC16 IL-12, 18 patientes) | Résumé de congrès ; pas de DOI retrouvé. L'essai correspondant est NCT02498912 (§3) et le protocole est Koneru et al. 2015 (§2). |
| Yu X. et al., *J Clin Oncol* 2025 ;43:4017 (résumé ASCO 2025, IBI343 phase I pancréas, NCT05458219) | Résumé de congrès ; DOI non vérifié. |
| Lin H.K. et al., *J Clin Oncol* 2024 ;42(16_suppl):2558 (résumé ASCO 2024, CAR/VIPRa) | Résumé de congrès ; DOI non vérifié. |
| Chekmasova et al. (CAR-T anti-MUC16, modèles murins) | Citation incomplète dans les fichiers (ni revue, ni année, ni DOI) ; DOI non vérifié. |
| « Understanding the Unique Attributes of MUC16 (CA125) », *Cancer Res* 2015 | Titre cité sans auteurs ni DOI ; DOI non vérifié. |
| *Frontiers* 2026 — survie GSE71729 (123 patients, 83 événements) | Article cité sans titre ni DOI précis dans les fichiers ; l'article correspondant n'a pas été identifié avec certitude (à ne pas confondre avec Ke et al. 2022, §2, qui rapporte 125 échantillons et 84 décès / 41 vivants). |

**Bilan des sources sans URL : 21 au total (15 tabulées + 6 références citées). Aucune URL n'a été devinée pour ces sources.**

---

## 8. Corrections et écarts relevés pendant la compilation

Ces écarts ont été trouvés en vérifiant les citations ; ils ne changent pas les verdicts du projet, mais le registre les signale pour que le PDF et le README ne les recopient pas.

1. **« Forcina et al. 2017 »** (PROVENANCE_kras_combinations.md) : le premier auteur réel est **Langdon et al.** — DOI 10.1158/1535-7163.MCT-16-0794 (§2).
2. **« Kemp et al. 2023, *Cancer Cell* / *Developmental Cell* »** : l'article est paru dans ***Cancer Discovery* 2023 ;13:298–311**, DOI 10.1158/2159-8290.CD-22-1066 (§2).
3. **« *Front Immunol* 2026 ;16:1638585 »** : le DOI exact est **10.3389/fimmu.2025.1638585** (année de volume 2025 dans le DOI, publication janvier 2026) — Xing et al. (§2).
4. **GSE62452** : la plateforme est bien **GPL6244** (et non GPL570, comme écrit dans un brouillon) ; 69 tumeurs + 61 tissus normaux ; PMID 27197190 (§1, §2).
5. **ICGC PACA-AU** : les études cBioPortal `paad_qcmg_uq_2016` et `paad_icgc` ont été **écartées** après vérification — elles ne correspondent pas aux données utilisées (§1).
6. **TCGA survie (15 nov. 2026)** : le tableau présenté ce jour-là était l'ajustement à six gènes étiqueté à tort « univarié » ; les vrais chiffres univariés sont plus forts, non plus faibles (corrigé dans le livre blanc §8 — rappelé ici pour la provenance, sans changer les sources).
7. **Essais NCT05737706, NCT05533463, NCT05846516** : les fichiers les marquent « non vérifié » ; l'URL `clinicaltrials.gov` est mécanique et donc donnée, mais le statut clinique (ex. TERMINATED pour NCT05737706, début 2025) n'a pas été re-vérifié essai par essai sur le registre (§3).

---

## 9. Méthode et limites

- **Sources lues :** 25 fichiers `PROVENANCE_*.md` et 39 fichiers `*.md` de `~/workspace/runs/pdac-v6/` (provenances + rapports), plus le livre blanc `livre-blanc-pdac-v6.md` et `~/workspace/runs/biophysique-hp35/PROVENANCE.md` (HP35).
- **Extraction :** toutes les URL, tous les DOI et tous les numéros NCT présents dans ces fichiers (23 URL distinctes dans les provenances, 22 dans les rapports, 58 numéros NCT dans les fichiers + NCT02498912 trouvé par recherche = 59).
- **Vérification web :** recherches effectuées le 16 novembre 2026 pour chaque DOI et chaque communiqué absent des fichiers de provenance. Les URL `clinicaltrials.gov` sont construites mécaniquement à partir du numéro NCT (règle autorisée par la tâche) ; les URL PMC sont construites mécaniquement à partir de l'identifiant PMCID cité dans les fichiers.
- **Ce qui n'a pas été vérifié :** le statut clinique actuel de chaque essai NCT (recrutement, terminé, etc.) n'a pas été contrôlé un par un sur ClinicalTrials.gov ; seuls les statuts mentionnés dans les fichiers (ex. NCT05737706 TERMINATED) sont repris. Les titres de certains articles ne figuraient pas dans les fichiers : ils sont signalés « titre non relevé dans les fichiers » plutôt que reconstitués.
- **Comptage final :** 189 sources tabulées — 135 vérifiées dans un fichier de provenance, 32 trouvées par recherche web, 7 liens morts / accès bloqué avec miroir ou contournement, 15 introuvables. Avec les 6 références citées sans ligne de tableau (§7b), **195 références citées au total, dont 21 sans URL**.

---

*Registre compilé le 16 novembre 2026. Fichier : `~/workspace/runs/pdac-v6/source_registry.md`. Ne pas modifier les fichiers de provenance — ce registre est un document de synthèse distinct.*

## 10. Compléments vérifiés le 16 novembre 2026 (après compilation du registre)

Vérification complémentaire effectuée lors de la construction du PDF. Ces
sources figuraient au §7 (sans URL) ; leur URL est désormais confirmée.
Les autres sources du §7 restent sans URL vérifiable — voir §7 pour la
raison (résumés de congrès sans DOI, communiqués non retrouvés, citations
incomplètes). État après ces compléments : 17 sources sans URL (au lieu de 21).

| Source | Type | URL complète | Statut |
|---|---|---|---|
| Sun Y., Pang C., Gao J. — « Daraxonrasib: The first-in-class RAS(ON) multi-selective inhibitor approved for treatment of metastatic pancreatic adenocarcinoma », *Drug Discov Ther* 2026 ;20(5):400–402 | Article | https://doi.org/10.5582/ddt.2026.01067 (PubMed : https://pubmed.ncbi.nlm.nih.gov/42802048/ — PMID 42802048) | ✅ Vérifiée par recherche web, 16 nov. 2026 |
| Revolution Medicines — communiqué RASolute-303 (2 avril 2026, début de traitement des patients) | Communiqué / page web | https://marketwirenews.com/stock/rvmd/news/revolution-medicines-begins-treating-patients-in-pha-8070093570132129.html (relais GlobeNewswire, texte intégral du communiqué) | ✅ Vérifiée par recherche web, 16 nov. 2026 |
| Innovent — communiqué IBI343 (ASCO 2025, ORR 22,7 %, DCR 81,8 %) | Communiqué / page web | https://pharmabiz.com/ArticleDetails.aspx?aid=178290&sid=2 (republication du communiqué Innovent) ; revue citant le résumé ASCO 2025 #4017 : https://link.springer.com/article/10.1007/s12254-025-01078-9 | ✅ Vérifiée par recherche web, 16 nov. 2026 (le DOI JCO du résumé #4017 lui-même n'a pas été deviné — il n'est pas cité) |
| Avis positif CHMP / EMA (oct. 2026, daraxonrasib) | Communiqué / page web | https://www.watchlistnews.com/what-revolution-medicines-rvmd-said-on-its-q3-earnings-call/11296595.html (dépêche confirmant l'avis positif du CHMP en octobre 2026) | ✅ Vérifiée par recherche web, 16 nov. 2026 (relais ; la page EMA elle-même n'a pas été retrouvée) |
