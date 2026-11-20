# Provenance — lot §8.59–§8.63 (20 novembre 2026)

Go de Zackary « Lance les 5 pistes », 20 nov. 2026 06h42 (5 chantiers, dans
l'ordre : adoption maxsep, déconvolution par type cellulaire, pureté par
méthylation, loi d'échelle en n pour Delta, mécanismes §8.50/§8.53).
Coordinateur : fusion au livre blanc, PDF régénéré, poussée GitHub.
Règle permanente « Toujours github et pdf !!! ».

## Codes (vérifiés inchangés avant et après chaque chantier)

- v6.2 (travail) : `universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
- v6.1 (référence) : SHA `2af5e5ce…c1c9` ; v6 (historique) : SHA `bb8bbdba…c0773`
- v6.3 REJETÉE (§8.49), v6.4 REJETÉE (§8.52) — aucune v6.5 créée dans ce lot
  (l'adoption de maxsep reste SOUS CONDITION, §8.59).

## Protocoles gelés avant tout calcul

| Chantier | Protocole | SHA-256 |
|---|---|---|
| §8.59 adoption maxsep | `PROTOCOL_maxsep_adoption_859.md` | `efb5da799d245d8e5db570945acc480f1c5bae42d63ed29b7cfeb780610e675b` |
| §8.60 déconvolution | `PROTOCOL_deconvolution_860.md` | `471568b1eb83027d4341c7ec5632b5749cf60aa2d06e8a4ddbf2315ffed86d57` |
| §8.61 pureté méthylation | `PROTOCOL_methylation_purity_861.md` | `93f4f777f217d9a03c01b1b79397ed70e59567e53edaf4231864e9c6a50e0993` |
| §8.62 loi d'échelle Delta | `PROTOCOL_delta_scaling_862.md` | `8e67f8c7f17f92d297c5cbf02884e9a82778dd6c20fb8ee681afb3b24fb995b0` |
| §8.63 mécanismes | `PROTOCOL_mechanisms_863.md` | `4e05dfc208725d610c591c2e4845dca277ed0d7d0a64e8ac095491f03c21f35e` |

## Sections

| Section | Fichier | Lignes | SHA-256 |
|---|---|---|---|
| §8.59 | `section_8.59_maxsep_adoption.md` | 394 | `9951d22c1e3de415914f5ed9cf1271972a7e6a17bb5c0489684240177dee36f4` |
| §8.60 | `section_8.60_deconvolution.md` | 651 | `41114ce19f7e2452f958e216b04ddf79796f5013a7d4a8cf23c1d7ea1701afe6` |
| §8.61 | `section_8.61_methylation_purity.md` | 459 | `599aca3b656d47fe72cf8ae4eb37e5c2c4c82cdb4d83e81b9b5f960d19ba21c4` |
| §8.62 | `section_8.62_delta_scaling.md` | 411 | `38674a2214dbfd5f287b28cfa1fd8b11d641f7989d6587847141d7c2ff8b9d14` |
| §8.63 | `section_8.63_mechanisms.md` | 413 | `ec89ccf1b197d0bece964aef133b47011899982c369e85712788ac390aedd1a7` |

## Runs

- §8.59 : re-vérification hors-ligne uniquement (120 `master_results.json`
  existants, second calcul indépendant 120/120 écart 0,0 exact) — aucun run.
- §8.60 : 8/8 runs v6.2 exit 0 (unité systemd `v62-deconv-860`, 11:52:59–
  13:16:16 UTC 20 nov. 2026).
- §8.61 : 4/4 runs v6.2 exit 0 (unité systemd `v62-purity-861`, 11:44:59–
  12:29:47 UTC 20 nov. 2026).
- §8.62 : 31/31 runs v6.2 exit 0 (lot B ; reprise après un redémarrage
  machine ~13h21 UTC, 0 run perdu).
- §8.63 : 10/10 runs v6.2 exit 0 (nuls ICGC frais s31–s40, unité systemd
  `v62-863`, 11:51:36–13:15:32 UTC 20 nov. 2026).

## Nouvelles sources brutes (§8.60, §8.61)

- Fractions CIBERSORT publiées (Thorsson et al. 2018, *Immunity*,
  doi 10.1016/j.immuni.2018.03.023), via le miroir public imogimap
  (Korkut lab, GitHub `korkutlab/imogimap`, doc `R/data.R`) :
  `TCGA_IMCell_fraction.rda` (1 053 486 o,
  SHA `739bfa99495643a926e6f010589044f69969962e2197378bba67e097366370c0`),
  `TCGA_Leukocyte_fraction.rda` (114 032 o,
  SHA `f576f5f261bbfe4dcc2384c7d90c375e109986f31ad54b544136e5d9a4e68289`) ;
  matrice LM22 (Newman et al. 2015), miroir `SiYangming/CIBERSORT-DATA`,
  SHA `8b1b4bb21fffcb10d25ecb6df9aafa3a24b527c35130b9d65e9341a6287cd36c`.
  Fichiers bruts détenus sous `data_deconvolution_860/` (hors dépôt, voir
  DATA_SOURCES.md §18/§19) ; transcriptions CSV dans `data_flux/`.
- Pureté par méthylation (§8.61) : même source que §8.55 — Raphael et al.
  2017 Table S1 via pdacR `TCGA_PAAD.rds` (SHA `52020679…ea76`,
  re-téléchargé et vérifié inchangé le 20 nov. 2026) ; aucune source
  nouvelle.

## Ce qui manque (nommé, pas caché)

- xCell (64 types, stroma/fibroblastes) : existence confirmée, non
  téléchargé (porte D déjà ouverte au §8.60) — piste §8.60.11.
- ESTIMATE publiée pour PAAD : toujours non obtenue (site piloté par JS).
- Thorsson via Europe PMC : « Article with id PMC5982584 is not open
  access one » ; TIMER2.0 : serveur Shiny interactif, pas de fichier en
  vrac ; CIBERSORTx : compte requis.
- Le déclencheur du pic étroit par permutation (§8.63, résidu de M1a/M2d)
  reste non élucidé.

## Livre blanc et PDF de ce lot

- Livre blanc fusionné : 10 666 lignes, SHA-256
  `ba88761dd160afd360dab3c1fc831c3d2a0db54a729bed0f5bf796dc6882eebf`
  (10 662 lignes, SHA `fe036c92…` avant les entrées de journal ;
  une coquille de fusion « ### 8.8.59 » corrigée avant le PDF).
- PDF régénéré : **891 pages A4, 12 322 374 octets, SHA-256
  `69c3594bb086fb2a…`** (chaîne `.src/`, WeasyPrint 70.0, unité systemd
  `pdf-build-863`, FIN 20 nov. 2026 14h28 UTC).
- Matrices DepMap découpées pour la prochaine Release (go de Zackary
  20 nov. 08h17) : `CRISPRGeneEffect.csv.gz` en 4 morceaux de 50 Mo,
  `OmicsCNGene.csv.gz` en 3 morceaux, réassemblage vérifié
  (SHA `3d8f3ec6…` et `4851d3e9…` retrouvés) —
  `depmap_split/README_depmap_split.md` (hors dépôt, actifs de Release).
