# Provenance — flux PDAC du jour (TCGA-PAAD, variante v2)

```json
{
  "date": "2026-11-15",
  "variante": "v2 (exclusions pureté/sexe)",
  "base": "même source et même protocole que pdac_tcga_fluxes.csv (v1) ; voir PROVENANCE_tcga.md",
  "exclusions": {
    "raison": "la sélection par variance (v1) a choisi presque uniquement des enzymes digestives du pancréas normal et XIST : ces gènes mesurent la quantité de pancréas normal dans la biopsie (pureté) et le sexe, pas le cancer. La v1 reste intacte comme témoin.",
    "liste": [
      "AMY2A",
      "AMY2B",
      "CELA1",
      "CELA2A",
      "CELA3A",
      "CELA3B",
      "CLPS",
      "CPA1",
      "CPA2",
      "CPB1",
      "CPB2",
      "CTRB1",
      "CTRB2",
      "CTRC",
      "CUZD1",
      "DDX3Y",
      "EIF1AY",
      "KDM5D",
      "NLGN4Y",
      "PNLIP",
      "PRKY",
      "PRSS1",
      "PRSS2",
      "PRSS3",
      "REG1A",
      "REG1B",
      "REG3A",
      "REG3G",
      "RPS4Y1",
      "RPS4Y2",
      "SRY",
      "SYCN",
      "TSIX",
      "TSPY1",
      "TSPY2",
      "TTTY15",
      "TTTY2",
      "USP9Y",
      "UTY",
      "XIST",
      "ZFY"
    ],
    "présents_dans_la_matrice": [
      "AMY2A",
      "AMY2B",
      "CELA1",
      "CELA2A",
      "CELA3A",
      "CELA3B",
      "CLPS",
      "CPA1",
      "CPA2",
      "CPB1",
      "CPB2",
      "CTRB1",
      "CTRB2",
      "CTRC",
      "CUZD1",
      "DDX3Y",
      "EIF1AY",
      "KDM5D",
      "NLGN4Y",
      "PNLIP",
      "PRKY",
      "PRSS1",
      "PRSS3",
      "REG1A",
      "REG1B",
      "REG3A",
      "REG3G",
      "RPS4Y1",
      "RPS4Y2",
      "SRY",
      "SYCN",
      "TSIX",
      "TSPY1",
      "TSPY2",
      "TTTY15",
      "TTTY2",
      "USP9Y",
      "UTY",
      "XIST",
      "ZFY"
    ]
  },
  "sélection_gènes": {
    "méthode": "variance entre les patients, par gène, sur log2(RSEM+1) ; top 12 hors KRAS et hors liste d'exclusion",
    "gènes": [
      {
        "gène": "PNLIPRP1",
        "variance": 27.2632,
        "médiane_log2": 5.9064
      },
      {
        "gène": "PNLIPRP2",
        "variance": 27.2064,
        "médiane_log2": 6.4442
      },
      {
        "gène": "CELA2B",
        "variance": 27.0725,
        "médiane_log2": 4.3582
      },
      {
        "gène": "PLA2G1B",
        "variance": 27.0612,
        "médiane_log2": 6.6414
      },
      {
        "gène": "GP2",
        "variance": 26.8769,
        "médiane_log2": 9.5752
      },
      {
        "gène": "CELP",
        "variance": 25.2292,
        "médiane_log2": 1.7573
      },
      {
        "gène": "GCG",
        "variance": 25.0717,
        "médiane_log2": 12.2265
      },
      {
        "gène": "CEL",
        "variance": 25.0328,
        "médiane_log2": 9.5164
      },
      {
        "gène": "INS",
        "variance": 23.0023,
        "médiane_log2": 13.6351
      },
      {
        "gène": "PGC",
        "variance": 20.6471,
        "médiane_log2": 8.1363
      },
      {
        "gène": "PPY",
        "variance": 20.0687,
        "médiane_log2": 8.4965
      },
      {
        "gène": "TRY6",
        "variance": 19.9399,
        "médiane_log2": 9.3537
      }
    ]
  },
  "ordre": "expression KRAS croissante (log2(RSEM+1)) ; KRAS = axe d'ordonnancement, jamais un flux",
  "flux_csv": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v2.csv",
    "sha256": "9d0b1ca8a2ba6a500ec45afdc7ac263f72a18629d634e7ea5bc2df06a89e6f2c",
    "lignes": 178,
    "colonnes": [
      "step",
      "PNLIPRP1",
      "PNLIPRP2",
      "CELA2B",
      "PLA2G1B",
      "GP2",
      "CELP",
      "GCG",
      "CEL",
      "INS",
      "PGC",
      "PPY",
      "TRY6"
    ]
  },
  "nul_csv": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v2_nul.csv",
    "sha256": "031baf684cf96c0432cc6fcb7ed45ec9288bc9d4927433ddd30324ef2029e411",
    "méthode": "mêmes lignes permutées, graine 42"
  }
}
```
