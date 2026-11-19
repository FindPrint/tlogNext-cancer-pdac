# Provenance — Bras 2 pan-cancer (TCGA-LUAD, TCGA-COAD, Firehose)

```json
{
  "date": "2026-11-16",
  "protocole": "PROTOCOL_pancancer.md",
  "cohortes": {
    "luad": {
      "label": "TCGA-LUAD (adénocarcinome pulmonaire)",
      "source": {
        "dépôt": "Broad GDAC Firehose stddata 2016-01-28",
        "fichier": "LUAD.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt",
        "url": "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/LUAD/20160128/",
        "taille_octets": 47043687,
        "md5_observé": "4c36eec3f6df75630292c5a569cfc8f4",
        "matrice_interne": "gdac.broadinstitute.org_LUAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0/LUAD.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt",
        "matrice": "20503 gènes x 576 échantillons",
        "données": "RNA-seq V2 RSEM normalisé (TCGA, UNC Illumina HiSeq)"
      },
      "patients": {
        "critère": "échantillons tumoraux primaires, code TCGA 01",
        "retenus": 515,
        "écartés": 61,
        "transformation": "log2(RSEM normalisé + 1)"
      },
      "gènes": {
        "demandés_v4": [
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
        "retenus": [
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
        "absents": [],
        "moins_de_50_valides": [],
        "remplacements_v3_hors_sexe_disponibles": [],
        "remplacement_effectué": null
      },
      "KRAS_log2": {
        "n": 515,
        "min": 8.921,
        "médiane": 10.4127,
        "max": 14.8647
      },
      "ordre": "expression KRAS brute croissante ; KRAS = axe, jamais un flux",
      "flux_csv": {
        "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_luad_fluxes.csv",
        "sha256": "d407849b991aa758398c85796662f51787cc54bbac62e824308f29787238091e",
        "lignes": 515,
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
        "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_luad_fluxes_nul.csv",
        "sha256": "93766e8c14e140f6b7946b67db9c0f2ad4beff0c1790d84a9c1357c56f978a6b",
        "méthode": "mêmes lignes permutées, graine 42"
      }
    },
    "coad": {
      "label": "TCGA-COAD (colorectal)",
      "source": {
        "dépôt": "Broad GDAC Firehose stddata 2016-01-28",
        "fichier": "COAD.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt",
        "url": "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/COAD/20160128/",
        "taille_octets": 26401036,
        "md5_observé": "e703a630556d42f098cf0df87d4712bb",
        "matrice_interne": "gdac.broadinstitute.org_COAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0/COAD.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt",
        "matrice": "20503 gènes x 328 échantillons",
        "données": "RNA-seq V2 RSEM normalisé (TCGA, UNC Illumina HiSeq)"
      },
      "patients": {
        "critère": "échantillons tumoraux primaires, code TCGA 01",
        "retenus": 285,
        "écartés": 43,
        "transformation": "log2(RSEM normalisé + 1)"
      },
      "gènes": {
        "demandés_v4": [
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
        "retenus": [
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
        "absents": [],
        "moins_de_50_valides": [],
        "remplacements_v3_hors_sexe_disponibles": [],
        "remplacement_effectué": null
      },
      "KRAS_log2": {
        "n": 285,
        "min": 8.9248,
        "médiane": 10.2225,
        "max": 11.3531
      },
      "ordre": "expression KRAS brute croissante ; KRAS = axe, jamais un flux",
      "flux_csv": {
        "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_coad_fluxes.csv",
        "sha256": "79e23912158dfe1a4acabde40f9b0e59cff5fdee8bd1fb02d2010aded528281f",
        "lignes": 285,
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
        "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_coad_fluxes_nul.csv",
        "sha256": "9172a00431f9da32ecb89d9671c75f3b962411d93cbc0291bc66eadff970fc5c",
        "méthode": "mêmes lignes permutées, graine 42"
      }
    }
  }
}
```

## Runs v6 (16 nov. 2026, 19h39–19h56 UTC)
- Pipeline : `~/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py`,
  SHA256 vérifié avant lancement : `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`, jamais modifié.
- Mode fast, 4 runs, tous exit 0 (log `runs_pancancer_v6.log`) :
  `results_fast_pancancer_luad`, `results_fast_pancancer_luad_nul`,
  `results_fast_pancancer_coad`, `results_fast_pancancer_coad_nul`.
- Cascades (T_-2 / T_-1 / T_0 / T_+1 / T_+2, en %) et Delta :
  - LUAD réel (n=515) : 0,76 / 46,69 / 68,62 / 80,82 / 80,82 ; Delta 2,511 ; L7a UP 42,11 %.
  - LUAD nul : 0,00 / 0,61 / 3,61 / 69,61 / 69,61 ; Delta 2,497 ; L7a DOWN 23,25 %.
  - COAD réel (n=285) : 0,00 / 33,92 / 86,76 / 98,02 / 98,02 ; Delta 4,619 ; L7a DOWN 20,95 %.
  - COAD nul : 0,00 / 1,36 / 68,07 / 94,73 / 94,73 ; Delta 4,599 ; L7a UP 41,04 %.
  - MC prédictif : 48 scénarios, terminé, dans les 4 runs. L7b FRAGILE (mode light) dans les 4 runs,
    réel comme nul — non-informatif (règle du projet : L7b dit FRAGILE sur réel et nul alike).
- SHA256 des CSV :
  - `pdac_luad_fluxes.csv` : `d407849b991aa758398c85796662f51787cc54bbac62e824308f29787238091e`
  - `pdac_luad_fluxes_nul.csv` : `93766e8c14e140f6b7946b67db9c0f2ad4beff0c1790d84a9c1357c56f978a6b`
  - `pdac_coad_fluxes.csv` : `79e23912158dfe1a4acabde40f9b0e59cff5fdee8bd1fb02d2010aded528281f`
  - `pdac_coad_fluxes_nul.csv` : `9172a00431f9da32ecb89d9671c75f3b962411d93cbc0291bc66eadff970fc5c`
  - `pancancer_direct_tests.csv` : `1e3786c279acac7e343ea66a2d5a3be226b2ba8f721fa0095afe7fb536cd322f`
- Taille des matrices brutes : LUAD 47 043 687 octets (MD5 `4c36eec3f6df75630292c5a569cfc8f4`),
  COAD 26 401 036 octets (MD5 `e703a630556d42f098cf0df87d4712bb`).
  Aucun MD5 de référence publié par Firehose pour LUAD/COAD ; les MD5 observés sont consignés ici
  et vérifiés à chaque lecture par `build_fluxes_pancancer.py`.
- Gènes : 12/12 présents avec ≥50 valeurs valides dans les deux cohortes, 0 NaN dans les flux,
  aucun remplacement nécessaire (la liste de remplacement v3 hors sexe ne contient que des gènes
  déjà dans les 12 — documenté dans le protocole gelé).
