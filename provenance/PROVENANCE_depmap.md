# Provenance — flux PDAC du jour (DepMap 24Q4)

```json
{
  "date": "2026-11-15",
  "sources": {
    "CRISPRGeneEffect.csv": {
      "depot": "DepMap Public 24Q4, figshare article 27993248, DOI 10.25452/figshare.plus.27993248.v1",
      "fichier": "https://ndownloader.figshare.com/files/51064667",
      "taille_octets": 428678699,
      "sha256": "3d8f3ec6dbf2db7ff834b79b508622ec0b226f3518003fe96ecf5a4fcf167e3b"
    },
    "Model.csv": {
      "depot": "DepMap Public 24Q4, figshare article 27993248",
      "fichier": "https://ndownloader.figshare.com/files/51065297",
      "taille_octets": 645696,
      "sha256": "b7a0c1385e6cef30132b56aff61f1261d11e3f490490b355c430d32ee0dbdcfa"
    }
  },
  "lignées": {
    "critère": "OncotreePrimaryDisease == 'Pancreatic Adenocarcinoma'",
    "dans Model.csv": 64,
    "dans GeneEffect.csv": 45,
    "exclues": "adénosquameux (2), neuroendocrine (1), non cancéreuse (1)",
    "ordre": "effet Chronos KRAS croissant (plus dépendant d'abord)"
  },
  "sélection_gènes": {
    "méthode": "médiane Chronos pancréas moins médiane Chronos autres lignées, par gène ; top 12 hors KRAS",
    "gènes": [
      {
        "gène": "EFR3A",
        "colonne": "EFR3A (23167)",
        "sélectivité": -0.5063,
        "médiane_pancréas": -0.8482,
        "médiane_autres": -0.342
      },
      {
        "gène": "RAB10",
        "colonne": "RAB10 (10890)",
        "sélectivité": -0.4866,
        "médiane_pancréas": -0.8466,
        "médiane_autres": -0.36
      },
      {
        "gène": "CCND1",
        "colonne": "CCND1 (595)",
        "sélectivité": -0.4631,
        "médiane_pancréas": -1.2897,
        "médiane_autres": -0.8266
      },
      {
        "gène": "UROD",
        "colonne": "UROD (7389)",
        "sélectivité": -0.4531,
        "médiane_pancréas": -0.9627,
        "médiane_autres": -0.5095
      },
      {
        "gène": "CFLAR",
        "colonne": "CFLAR (8837)",
        "sélectivité": -0.4488,
        "médiane_pancréas": -0.9645,
        "médiane_autres": -0.5157
      },
      {
        "gène": "DOCK5",
        "colonne": "DOCK5 (80005)",
        "sélectivité": -0.4118,
        "médiane_pancréas": -0.4641,
        "médiane_autres": -0.0523
      },
      {
        "gène": "MYH9",
        "colonne": "MYH9 (4627)",
        "sélectivité": -0.397,
        "médiane_pancréas": -0.791,
        "médiane_autres": -0.3939
      },
      {
        "gène": "SCAP",
        "colonne": "SCAP (22937)",
        "sélectivité": -0.3867,
        "médiane_pancréas": -1.3523,
        "médiane_autres": -0.9656
      },
      {
        "gène": "RAB6A",
        "colonne": "RAB6A (5870)",
        "sélectivité": -0.3866,
        "médiane_pancréas": -0.8467,
        "médiane_autres": -0.4601
      },
      {
        "gène": "CRKL",
        "colonne": "CRKL (1399)",
        "sélectivité": -0.3826,
        "médiane_pancréas": -1.1782,
        "médiane_autres": -0.7956
      },
      {
        "gène": "MYC",
        "colonne": "MYC (4609)",
        "sélectivité": -0.3508,
        "médiane_pancréas": -2.1445,
        "médiane_autres": -1.7937
      },
      {
        "gène": "ACO2",
        "colonne": "ACO2 (50)",
        "sélectivité": -0.3476,
        "médiane_pancréas": -1.0271,
        "médiane_autres": -0.6794
      }
    ],
    "KRAS_Chronos_pancréas": {
      "min": -4.1427,
      "médiane": -1.7596,
      "max": -0.1799
    }
  },
  "flux_csv": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes.csv",
    "sha256": "7d605fefb412fe16151a1b2508dffa6a1c2b8353600dccffd4af3333198e37f8",
    "lignes": 45,
    "colonnes": [
      "step",
      "EFR3A",
      "RAB10",
      "CCND1",
      "UROD",
      "CFLAR",
      "DOCK5",
      "MYH9",
      "SCAP",
      "RAB6A",
      "CRKL",
      "MYC",
      "ACO2"
    ]
  },
  "nul_csv": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_nul.csv",
    "sha256": "ac2e0db558ad2e2c4bf9240b8fab0d0c2125e9890212034a6f3b6a9f08326c80",
    "méthode": "mêmes lignes permutées, graine 42"
  },
  "règle": "Données du jour uniquement (DepMap 24Q4). Aucune donnée ni conclusion d'une autre expérience importée (règle 15 nov. 2026)."
}
```
