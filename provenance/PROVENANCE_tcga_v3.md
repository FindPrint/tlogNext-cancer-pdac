# Provenance — flux PDAC du jour (TCGA-PAAD, variante v3)

```json
{
  "date": "2026-11-15",
  "variante": "v3 (correction de pureté par régression)",
  "base": "même source que v1/v2 (Firehose, voir PROVENANCE_tcga.md)",
  "correction": {
    "raison": "v1/v2 mesurent que la variance dominante est la composition du tissu (acineux + îlots). La v3 enlève cette composante par régression linéaire, méthode standard (comme retirer un effet de lot).",
    "score_acineux": {
      "gènes": [
        "PNLIP",
        "CTRB2",
        "CELA3A",
        "CTRB1",
        "CPA1",
        "CELA2A",
        "CPB1",
        "CELA3B",
        "CLPS",
        "CTRC",
        "CPA2"
      ],
      "définition": "médiane log2(RSEM+1) par patient"
    },
    "score_îlots": {
      "gènes": [
        "INS",
        "GCG",
        "PPY",
        "SST"
      ],
      "définition": "médiane log2(RSEM+1) par patient"
    },
    "corrélation_acineux_îlots": 0.4826,
    "variance_expliquée_médiane": 0.0204,
    "R2_pureté_KRAS": 0.0029,
    "méthode": "moindres carrés par gène sur [1, score_acineux, score_îlots] ; flux = résidus"
  },
  "sélection_gènes": {
    "méthode": "variance des résidus entre les patients, par gène ; top 12 hors KRAS",
    "gènes": [
      {
        "gène": "XIST",
        "variance_résidu": 31.4702,
        "R2_pureté": 0.0051
      },
      {
        "gène": "RPS4Y1",
        "variance_résidu": 27.2109,
        "R2_pureté": 0.0074
      },
      {
        "gène": "DDX3Y",
        "variance_résidu": 21.2165,
        "R2_pureté": 0.0062
      },
      {
        "gène": "KDM5D",
        "variance_résidu": 20.5729,
        "R2_pureté": 0.0088
      },
      {
        "gène": "PGC",
        "variance_résidu": 18.6228,
        "R2_pureté": 0.098
      },
      {
        "gène": "USP9Y",
        "variance_résidu": 16.3269,
        "R2_pureté": 0.0132
      },
      {
        "gène": "REG4",
        "variance_résidu": 16.2484,
        "R2_pureté": 0.0113
      },
      {
        "gène": "EIF1AY",
        "variance_résidu": 15.9966,
        "R2_pureté": 0.0055
      },
      {
        "gène": "CLDN18",
        "variance_résidu": 15.7248,
        "R2_pureté": 0.0307
      },
      {
        "gène": "MUC17",
        "variance_résidu": 15.5475,
        "R2_pureté": 0.0139
      },
      {
        "gène": "DPCR1",
        "variance_résidu": 15.1806,
        "R2_pureté": 0.0546
      },
      {
        "gène": "UTY",
        "variance_résidu": 14.9799,
        "R2_pureté": 0.0076
      }
    ]
  },
  "ordre": "résidu KRAS croissant (KRAS corrigé de la pureté) ; KRAS = axe d'ordonnancement, jamais un flux",
  "flux_csv": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v3.csv",
    "sha256": "c26b65e47ba45bbc14faca76244713114f11f86210eb35519e389abf4ef04f94",
    "lignes": 178,
    "colonnes": [
      "step",
      "XIST",
      "RPS4Y1",
      "DDX3Y",
      "KDM5D",
      "PGC",
      "USP9Y",
      "REG4",
      "EIF1AY",
      "CLDN18",
      "MUC17",
      "DPCR1",
      "UTY"
    ]
  },
  "nul_csv": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v3_nul.csv",
    "sha256": "ad79c098181b4242ee6dc8410b4204933e408a95ac91ce823e3d652db0629ac7",
    "méthode": "mêmes lignes permutées, graine 42"
  }
}
```
