# Provenance — Étape 4 (c) : série TCGA v4 ordonnée par CN MTAP (18 nov. 2026)

```json
{
  "date": "2026-11-18",
  "test": "Étape 4 (c) — série TCGA v4 ordonnée par CN MTAP",
  "protocole": "PROTOCOL_enrichissements_833.md (gelé avant les runs)",
  "go": "Zackary, 18 nov. 2026, 15h06",
  "source_rsem": "Broad GDAC Firehose stddata 2016-01-28, PAAD, RSEM genes normalized, tarball déjà sur disque",
  "tarball_rsem": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/data/tcga_paad_rsem.tar.gz",
    "md5": "b09569ce3f4721f514bc137bd109ac0a"
  },
  "base_v4": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v4.csv",
    "sha256": "e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0"
  },
  "source_gistic": "Broad GDAC Firehose, PAAD-TP CopyNumber GISTIC2 Level 4, 2016-01-28, tarball déjà sur disque",
  "tarball_gistic": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/data/tcga_paad_gistic.tar.gz",
    "md5": "816034f742e8f89ca8734ca2cf4404d5"
  },
  "verification_reproduction": {
    "méthode": "résidus v4 recalculés depuis le tarball, triés par résidu KRAS croissant, comparés au CSV v4",
    "échantillon": 178,
    "écart_max_12_flux": 1.7763568394002505e-15,
    "atol": 1e-09,
    "résultat": "reproduction exacte (écart <= atol)"
  },
  "controle_mtap": {
    "définition": "CN MTAP continue GISTIC (all_data_by_genes.txt, log2 ratio), tri croissant (perte profonde d'abord)",
    "fichier_seuille": "all_thresholded.by_genes.txt (cohérence seulement)",
    "appariement": "177/178 tumeurs (patient, 15 premiers caractères)",
    "min": -1.293,
    "médiane": -0.181,
    "max": 1.922,
    "seuille_178": {
      "-2": 43,
      "-1": 62,
      "0": 69,
      "1": 2,
      "2": 1
    },
    "spearman_vs_rang_KRAS": {
      "rho": -0.3088,
      "p": 2.8879714742790136e-05
    },
    "recouvrement_top12_mtap_vs_kras": 1
  },
  "série": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v4_mtap.csv",
    "sha256": "578b8d3b9b26099d0784ed23754d1cc9717be7f9292eb47e201d186cdbc90df6",
    "lignes": 177,
    "colonnes": [
      "MTAPCN",
      "PGC",
      "REG4",
      "CLDN18",
      "MUC17",
      "DPCR1",
      "CR2",
      "KRT20",
      "MUC2",
      "GSTM1",
      "CEACAM5",
      "CLCA1",
      "MUC16"
    ],
    "ordre": "CN MTAP croissant",
    "contrôle": "MTAPCN (1re colonne, pas un flux — pas de doublon)"
  },
  "nul": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v4_mtap_nul.csv",
    "sha256": "e6786a47ce107dbf9785d83981ab413f8afb4e75fbdbae4da56da8c1e46453b9",
    "méthode": "mêmes lignes permutées, graine 42, contrôle intact"
  },
  "script": "build_fluxes_tcga_v4_mtap.py"
}
```
