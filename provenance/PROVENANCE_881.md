# PROVENANCE — Piste Œil §8.81 : privilège immunitaire de l'œil contre évasion immunitaire du pancréas (21 nov. 2026)

Protocole gelé : `PROTOCOL_oeil_privilege_881.md`, SHA-256 `c985a03aae699b56084ffda045a887419707c06fc63ee9bea0c5b518a993a4ce`
(gelé avant toute construction et tout run ; inchangé).
Go : parent, 21 nov. 2026 (piste proposée par Zackary le 21 nov., lancée le jour même).
Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

## 1. Pipeline (jamais modifié)

- `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`
  SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  vérifié avant le lot ET après (21 nov. 2026, 12h50 UTC), inchangé. Minimum fast = 40 points.
  Version lue dans les 4 runs : `v6.2.0-L7aL7b-CohenD-short`.

## 2. Sources PDAC (déjà sur le disque, rien de re-téléchargé)

| Cohorte | Fichier source | Effectif retenu | Provenance antérieure |
|---|---|---|---|
| TCGA-PAAD | `data/tcga_paad_rsem.tar.gz`, MD5 `b09569ce3f4721f514bc137bd109ac0a` (Broad GDAC Firehose stddata 2016-01-28, RSEM genes normalized) | 178 tumeurs primaires (code 01) | `PROVENANCE_tcga_v4.md` ; base v4 `pdac_tcga_fluxes_v4.csv` SHA `e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0` |
| GSE71729 | `data/GSE71729_series_matrix.txt.gz` (GPL20769 Agilent, symboles directs) | 145 tumeurs primaires, 145 cas complets | `PROVENANCE_geo71729.md` |
| GSE62452 | `data/GSE62452_series_matrix.txt.gz` (GPL6244 Affymetrix HuGene-1.0-ST) + mapping `data/GPL6244_probe2symbol.tsv` (médiane par symbole) | 69 tumeurs, 69 cas complets | `PROVENANCE_geo62452.md` |
| ICGC PACA-AU | `data/icgc_pacaau_exp.txt.gz` (log2 CPM, Bailey et al. 2016) + `data/icgc_pacaau_probemap.gz` (Ensembl → symbole, médiane) + clinique `data/bailey2016_suppl_tables1-13.xlsx` (Supp Table 1) | 70 tumeurs primaires PDAC, 70 cas complets | `PROVENANCE_icgc.md` |

Vérification de reproduction v4 (dans `direct_tests_881.py` ET `build_priv_881.py`, avant toute construction) :
résidus v4 recalculés depuis le tarball PAAD, triés par résidu KRAS croissant, comparés au CSV v4 —
écart max = 1,776e-15 (atol 1e-9). Reproduction exacte.

## 3. Source UVM (nouveau téléchargement, 21 nov. 2026)

- URL : `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/UVM/20160128/gdac.broadinstitute.org_UVM.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz`
  (même série Firehose stddata 2016-01-28 que le tarball PAAD ; pattern vérifié contre l'URL PAAD connue).
- Téléchargé le 21 nov. 2026, 12h15 UTC, par `curl` (exit 0, 1re tentative, aucune voie de repli nécessaire).
- Fichier : `data/tcga_uvm_rsem.tar.gz`, 6 311 998 o,
  SHA-256 `b50fdadb00d5c4095ffbe55ad4192cfca892c947cd657d032be128ba074a9975`.
  Contenu vérifié : `gzip compressed data`, membre `.data.txt` de 14 049 280 o.
- Retenus : 80 tumeurs primaires (code 01) sur 80 échantillons — n = 80, ≥ 40, runs UVM lancés comme prévu.
- Référence cohorte : TCGA Uveal Melanoma (UVM), 80 tumeurs ; aucune donnée clinique UVM utilisée.

## 4. Gènes : présence par matrice (nommée, pas imputée)

- Les 7 gènes de privilège (FASLG, TGFB1, TGFB2, IDO1, HLA-G, CD47, CD274) sont PRÉSENTS dans les 5 matrices
  (TCGA, GSE71729, GSE62452, ICGC, UVM). Aucun absent nulle part. Score PRIV = 7 gènes partout.
- Les 12 gènes v4 sont PRÉSENTS dans les 5 matrices. Aucun absent.
- Témoins « froid » (PDCD1, CD8A, GZMB, IFNG) : présents partout SAUF **IFNG, ABSENT de la matrice ICGC**
  (le symbole IFNG ne figure pas dans `icgc_pacaau_exp.txt.gz` après mapping Ensembl → symbole ;
  vérifié directement : `'IFNG' in exp.index` = False). IFNG-ICGC est donc absent du tableau T1 (case vide),
  pas zéro, pas imputé. Les 3 autres témoins sont présents en ICGC.
- KRAS : présent dans les 4 cohortes PDAC (ordre KRAS : résidu TCGA ; expression brute GEO/ICGC).
  KRAS TCGA (résidu) : min / médiane / max consignés dans `priv_direct_tests_881.json`.

## 5. Fichiers écrits (SHA-256, 21 nov. 2026)

| Fichier | SHA-256 |
|---|---|
| `PROTOCOL_oeil_privilege_881.md` | `c985a03aae699b56084ffda045a887419707c06fc63ee9bea0c5b518a993a4ce` |
| `direct_tests_881.py` | `01c8b74431073d052b92ae614f1a5ac342ae738542aca33468a023fc94397d91` |
| `build_priv_881.py` | `4a4693ca0e0aa2f8f2d8fb4a4b133c5ecff7728011f76f0b6138db4a9d557a69` |
| `uvm_881.py` | `9af4dfb9f235c2991c893f46d83fe6b6777179fdbdb771343af517647fa7fdfa` |
| `extract_881.py` | `2150c39de29e8a6fd64405cf8899b66eb898f2f3bf38c342b5c86d30d0c98acc` |
| `priv_direct_tests_881.csv` | `3301bfc35febddfa0bfd239e09a5d6ed9177c53796f71c79db9a91b3a98cb37b` |
| `priv_direct_tests_881.json` | `be4277fc61db031bc37bf2eff72933782950e659d3877385c2ae035c37e35955` |
| `priv_direct_tests_881_series.csv` | `42701d53118ee86c491f427e7cdfd6e92a976984e103fbfb9c3ef0ba9b7a6c40` |
| `priv_extract_881.json` | `ec1dfdb6917ffa4ee06aaca36398fe1db97620df2d0ce1a16a0b3b479c3369d0` |
| `uvm_direct_tests_881.csv` | `bbb0501722b24acda312d4ab4d547f153ca5fc2f17cd5866bfba1ae3b850033b` |
| `uvm_881.json` | `bc95f3ac0147dd526b1a33cf0fa2433a627f01cb1ab8ea3199db492fec8c29c0` |
| `pdac_tcga_fluxes_v4_priv.csv` (178 lignes) | `348401cb3d0db12eb92a86fc15d164461c0be2ea3296a6d74719d3368c92db39` |
| `pdac_tcga_fluxes_v4_priv_nul.csv` (nul s42) | `54eec127823c1509486df6d7331990f68b9b6ab3f52393fa26be4612ba83d824` |
| `pdac_uvm_fluxes_priv.csv` (80 lignes) | `422898b77047043cefe8c88f6a69ad59bf44bc2717c6df56969d434fccd63d65` |
| `pdac_uvm_fluxes_priv_nul.csv` (nul s42) | `56be6c56276d4e1e59fe7842a01f371ed5d0a72f4b0a5fc2ed945c1e4598f178` |
| `manifest_v62_881.txt` | `033c2b38b4ffd9391243ff03296d2669796cdc454c52c8ccadcee993bcf2c82c` |
| `runs_v62_881.log` | `f839421577a48b7b8692be37340cc95c33523035d544d05a3f8417a1c3b21a4a` |
| `PROVENANCE_priv_881.json` | `14c3331dac06755369650c16bfe617c462ca6eaa1cbb94cd76238c9467ed587b` |
| `section_8.81_oeil_privilege.md` | (SHA calculé après écriture, rapporté au coordinateur) |

## 6. Runs (4, mode fast, v6.2)

- Manifeste `manifest_v62_881.txt` (4 lignes), lanceur reprenable `run_v62_lot.sh`,
  unité systemd `v62-881` (jamais nohup), journal `runs_v62_881.log`.
- FIN 2026-11-21T12:50:55Z : `deja_faits=0 termines=4 echecs=0`.
  Exits : réel PRIV TCGA 0, nul PRIV TCGA 0, réel PRIV UVM 0, nul PRIV UVM 0.
- Dossiers : `results_fast_v62_881_priv/`, `results_fast_v62_881_priv_nul/`,
  `results_fast_v62_881_priv_uvm/`, `results_fast_v62_881_priv_uvm_nul/`
  (4 `master_results.json` présents).
- Extraction : `extract_881.py` (copie adaptée de `extract_858.py`, original intact) ;
  recoupement indépendant par relecture directe des 4 `master_results.json` :
  `maxsep` identique (TCGA réel 0,3534 ; TCGA nul 0,1885 ; UVM réel 0,2661 ; UVM nul 0,2165),
  MC identique — écart 0,0.
- Note : la métrique `sep` n'existe pas dans les métriques v6.2 lues ici
  (clés : `max_separation`, `robustness`, `s_norm`, `sharpness`, `stability`) —
  `sep` est donc rapporté indisponible, pas zéro.

## 7. Méthode des tests directs (rappel gelé)

- TCGA : RÉSIDUS après correction de pureté (régression [1, score acineux, score îlots], comme la v4).
  GEO/ICGC : valeurs fournies, cas complets, jamais d'imputation.
- UVM : log2(RSEM+1), sans correction de pureté (pas de scores acineux/îlots pour l'œil).
- Test principal T1 : Spearman rho contre le rang KRAS (correction §8.70/§8.71 : le d de Cohen marginal
  réel-vs-nul est vacueux par construction — vérifié numériquement : FASLG/TGFB1/CD274 TCGA,
  d marginal = −0,0000 / +0,0000 / −0,0000 ; il valide la construction du nul et ne décide rien).
- Score PRIV : moyenne des z-scores intra-cohorte des 7 gènes de privilège (7 gènes dans les 5 cohortes).
  PRIV TCGA : min −2,050, médiane +0,063, max +1,425. PRIV UVM : min −1,133, médiane −0,155, max +1,565.
- Recouvrement top-12 PRIV/KRAS (TCGA) : 1/12. Spearman PRIV vs rang KRAS (TCGA) : rho +0,1462 (p = 0,0515).

## 8. Ce qui manque / limites nommées

- Aucune donnée d'œil normal (le privilège est mesuré sur un cancer de l'œil, pas sur l'œil sain) ;
  aucune donnée single-cell, spatiale, protéique de l'œil ; aucune mesure fonctionnelle (cytotoxicité, ACAID).
- Comparaison de niveaux bruts UVM vs PAAD (U1) : deux types tumoraux différents — la spécificité tissulaire
  domine pour les gènes v4 (médiane 0 en UVM pour 9 gènes sur 12) ; lecture descriptive seulement.
- IFNG absent de la matrice ICGC (voir §4) — le témoin « froid » en ICGC repose sur PDCD1, CD8A, GZMB.
- Un seul nul par paire (graine 42) ; ~200 nuls seraient nécessaires pour un plancher stable à petit n (§8.53).
