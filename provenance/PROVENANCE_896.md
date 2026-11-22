# Provenance — §8.96 : universalité — le pipeline sur un autre cancer

Date : 21 novembre 2026. Statut : **SQUELETTE — protocole gelé, AUCUN téléchargement nouveau, AUCUN run lancé à ce jour.** À compléter par les résultats, sans réécrire ce fichier (addenda datés seulement).

## 1. Protocole gelé

- `PROTOCOL_universalite_896.md`, SHA-256 `24566611175003dfac7a5364f8848b929d479e7b00135acfaf3a82e137ce5fc9`.
- Go de Zackary « Faite tout cela », 21 nov. 2026 11h36, piste 4/4. Coordinateur : TagPrint.

## 2. Code (vérifié avant gel, inchangé)

- Pipeline v6.2 `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
- v6.1 SHA `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ; v6 SHA `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`.
- À compléter : SHA de `build_fluxes_brca_896.py`, des JSON de vérification et des tables.

## 3. Bras A — TCGA-LUAD (données DÉTENUES)

- Source : Broad GDAC Firehose stddata 2016-01-28, `LUAD.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt`, URL `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/LUAD/20160128/`, 47 043 687 octets, MD5 observé `4c36eec3f6df75630292c5a569cfc8f4` (aucun MD5 de référence publié par Firehose). Matrice 20 503 gènes × 576 échantillons ; 515 tumeurs primaires (code 01) ; log2(RSEM + 1).
- Flux : `pdac_luad_fluxes.csv`, SHA-256 `d407849b991aa758398c85796662f51787cc54bbac62e824308f29787238091e`, 515 lignes, 12 flux (PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16), 12/12 présents, 0 NaN, aucun remplacement.
- Nul : `pdac_luad_fluxes_nul.csv`, SHA-256 `93766e8c14e140f6b7946b67db9c0f2ad4beff0c1790d84a9c1357c56f978a6b`, graine 42.
- Axe : expression KRAS brute croissante ; KRAS = axe, jamais un flux (KRAS log2 : min 8,921, médiane 10,4127, max 14,8647).
- Runs déjà détenus (relus) : `results_fast_pancancer_luad[_nul]` (§8.27 ; réel Delta 2,511, L7a UP 42,11 % ; nul Delta 2,497, L7a DOWN 23,25 %) ; `results_fast_v62_luad[_nul]` + série §8.62 n=45…515.
- Témoin COAD (détenu) : `pdac_coad_fluxes.csv`, SHA `79e23912158dfe1a4acabde40f9b0e59cff5fdee8bd1fb02d2010aded528281f`, n=285 ; nul SHA `9172a00431f9da32ecb89d9671c75f3b962411d93cbc0291bc66eadff970fc5c` ; réel Delta 4,619 ; nul 4,599.
- Runs neufs gelés : 2 runs v6.2 (LUAD réel n=515 + nul 42) + 2 nuls frais (graines 9601, 9602) — ~20 min, lot systemd.
- Provenance détaillée : `PROVENANCE_pancancer.md` (bras 2), `PROTOCOL_pancancer.md`.

## 4. Bras B — TCGA-BRCA (données À SOURCER)

- Source visée : Broad GDAC Firehose stddata 2016-01-28, cohorte BRCA, URL patron `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/BRCA/20160128/` (à vérifier avant téléchargement). Secours : GDC (TCGA-BRCA, RNA-seq STAR counts) — changement de source à consigner, jamais équivalent silencieux.
- État au gel : **BRCA n'est détenu NULLE PART dans ce projet** (0 occurrence dans DATA_SOURCES.md et annexes ; les seuls flux PARP BRCA1/BRCA2 existants portent sur TCGA-PAAD, pas sur TCGA-BRCA).
- Axe BRCA : à choisir APRÈS lecture de la matrice, AVANT tout run, consigné par addendum daté au protocole — candidats gelés : ESR1, TP53, ou prolifération (Test A). KRAS n'est PAS l'axe en BRCA.
- Gate : 12 flux, 12/12 présents ≥ 50 valeurs valides, 0 NaN ; remplacements par la liste v3 hors sexe, nommés gène par gène. Nul graine 42 + 2 nuls frais (9601, 9602). n minimum 40, visé ≥ 100.
- Si le téléchargement échoue : bras B = PISTE FERMÉE (données non accessibles), 5 contrôles d'accès nommés, comme §8.91.
- À compléter : URL exacte, taille, MD5/SHA observés, SHA des CSV de flux, choix de l'axe (addendum daté), runs (4 runs v6.2, ~20 min), tables.

## 5. Ce qui manque (déclaré)

- Tout le reste : aucun téléchargement, aucune construction de flux BRCA, aucun run neuf à ce jour. Aucune recommandation clinique, jamais (règle de sécurité §8.90).
