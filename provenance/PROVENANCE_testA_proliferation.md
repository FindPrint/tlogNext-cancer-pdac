# Provenance — Test A : série TCGA v4 ordonnée par prolifération (18 nov. 2026)

```json
{
  "date": "2026-11-18",
  "test": "Test A — série TCGA v4 ordonnée par prolifération",
  "protocole": "PROTOCOL_testA_proliferation.md (gelé avant les runs)",
  "go": "Zackary, 18 nov. 2026, 15h06",
  "source": "Broad GDAC Firehose stddata 2016-01-28, PAAD, RSEM genes normalized, tarball déjà sur disque",
  "tarball": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/data/tcga_paad_rsem.tar.gz",
    "md5": "b09569ce3f4721f514bc137bd109ac0a"
  },
  "base_v4": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v4.csv",
    "sha256": "e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0"
  },
  "verification_reproduction": {
    "méthode": "résidus v4 recalculés depuis le tarball, triés par résidu KRAS croissant, comparés au CSV v4",
    "échantillon": 178,
    "écart_max_12_flux": 1.7763568394002505e-15,
    "écart_max_PGC": 1.7763568394002505e-15,
    "atol": 1e-09,
    "résultat": "reproduction exacte (écart <= atol)"
  },
  "score_prolifération": {
    "définition": "médiane des résidus (correction pureté v4) de MKI67, TOP2A, PCNA, CCNB1 — §8.25 (c)",
    "spearman_vs_rang_KRAS_résidus": {
      "rho": 0.3394,
      "p": 3.5737596171577535e-06
    },
    "spearman_vs_rang_KRAS_brut": {
      "rho": 0.3817,
      "p": 1.4666075429220424e-07
    },
    "spearman_score_résidus_vs_brut": 0.9439,
    "recouvrement_top12_résidus_vs_brut": 9,
    "recouvrement_top12_prolif_vs_KRAS": 1,
    "min": -4.111,
    "médiane": 0.0377,
    "max": 1.8525
  },
  "série": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v4_prolif.csv",
    "sha256": "c87a4e0ac588b41f4138d1eed2d1bb77714989710b67a22c46fe91f57e0e5700",
    "lignes": 178,
    "colonnes": [
      "PROLIF",
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
    "ordre": "score de prolifération (résidus) croissant",
    "contrôle": "PROLIF (1re colonne, pas un flux — pas de doublon)"
  },
  "nul": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v4_prolif_nul.csv",
    "sha256": "99cbc3778c093d31be32cc46a8016dd4793551c549bef26e7cfaca19ab830719",
    "méthode": "mêmes lignes permutées, graine 42, contrôle intact"
  },
  "script": "build_fluxes_tcga_v4_prolif.py"
}
```
