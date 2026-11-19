# Provenance — flux PDAC du jour (TCGA-PAAD, variante v3)

```json
{
  "date": "2026-11-15",
  "variante": "v4 (correction de pureté par régression + exclusion sexe)",
  "base": "même source et même correction que v3 (Firehose, voir PROVENANCE_tcga.md et PROVENANCE_tcga_v3.md) ; la v3 reste intacte comme témoin",
  "exclusion_sexe": "les gènes du sexe dominent la variance des résidus v3 (XIST, gènes Y) : ils mesurent le sexe du patient, pas la tumeur. Exclus de la sélection v4 (liste consignée dans le script).",
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
        "gène": "PGC",
        "variance_résidu": 18.6228,
        "R2_pureté": 0.098
      },
      {
        "gène": "REG4",
        "variance_résidu": 16.2484,
        "R2_pureté": 0.0113
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
        "gène": "CR2",
        "variance_résidu": 14.7376,
        "R2_pureté": 0.0341
      },
      {
        "gène": "KRT20",
        "variance_résidu": 14.565,
        "R2_pureté": 0.0081
      },
      {
        "gène": "MUC2",
        "variance_résidu": 14.4029,
        "R2_pureté": 0.0197
      },
      {
        "gène": "GSTM1",
        "variance_résidu": 13.9219,
        "R2_pureté": 0.009
      },
      {
        "gène": "CEACAM5",
        "variance_résidu": 13.6512,
        "R2_pureté": 0.0091
      },
      {
        "gène": "CLCA1",
        "variance_résidu": 13.6126,
        "R2_pureté": 0.0373
      },
      {
        "gène": "MUC16",
        "variance_résidu": 13.5095,
        "R2_pureté": 0.0183
      }
    ]
  },
  "ordre": "résidu KRAS croissant (KRAS corrigé de la pureté) ; KRAS = axe d'ordonnancement, jamais un flux",
  "flux_csv": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v4.csv",
    "sha256": "e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0",
    "lignes": 178,
    "colonnes": [
      "step",
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
    ]
  },
  "nul_csv": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v4_nul.csv",
    "sha256": "895a456295d2b0553a2a62910461aedecb1aeccca59f57751c87b75ce0b97da4",
    "méthode": "mêmes lignes permutées, graine 42"
  }
}
```
