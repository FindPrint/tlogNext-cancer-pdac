# Provenance — flux PDAC du jour (TCGA-PAAD, Firehose)

```json
{
  "date": "2026-11-15",
  "source": {
    "dépôt": "Broad GDAC Firehose stddata 2016-01-28, PAAD",
    "fichier": "gdac.broadinstitute.org_PAAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz",
    "url": "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/PAAD/20160128/",
    "taille_octets": 15296232,
    "md5_vérifié": "b09569ce3f4721f514bc137bd109ac0a",
    "matrice_interne": "gdac.broadinstitute.org_PAAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0/PAAD.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt",
    "matrice": "20503 gènes x 183 échantillons",
    "données": "RNA-seq V2 RSEM normalisé (TCGA, UNC Illumina HiSeq)"
  },
  "patients": {
    "critère": "échantillons tumoraux primaires, code TCGA 01",
    "retenus": 178,
    "écartés": 5,
    "transformation": "log2(RSEM normalisé + 1)"
  },
  "sélection_gènes": {
    "méthode": "variance entre les patients, par gène, sur log2(RSEM+1) ; top 12 hors KRAS (la variance ne dépend pas de l'ordre des lignes)",
    "gènes": [
      {
        "gène": "PNLIP",
        "variance": 39.751,
        "médiane_log2": 8.2308
      },
      {
        "gène": "CTRB2",
        "variance": 37.9435,
        "médiane_log2": 10.2841
      },
      {
        "gène": "CELA3A",
        "variance": 36.9028,
        "médiane_log2": 9.316
      },
      {
        "gène": "CTRB1",
        "variance": 36.2006,
        "médiane_log2": 9.2275
      },
      {
        "gène": "CPA1",
        "variance": 35.7006,
        "médiane_log2": 9.3039
      },
      {
        "gène": "CELA2A",
        "variance": 35.6024,
        "médiane_log2": 6.0561
      },
      {
        "gène": "CPB1",
        "variance": 33.1185,
        "médiane_log2": 9.8754
      },
      {
        "gène": "CELA3B",
        "variance": 32.842,
        "médiane_log2": 7.0378
      },
      {
        "gène": "CLPS",
        "variance": 31.6656,
        "médiane_log2": 7.2396
      },
      {
        "gène": "XIST",
        "variance": 31.6319,
        "médiane_log2": 4.6797
      },
      {
        "gène": "CTRC",
        "variance": 31.3092,
        "médiane_log2": 7.8583
      },
      {
        "gène": "CPA2",
        "variance": 31.2729,
        "médiane_log2": 7.8656
      }
    ],
    "gènes_écartés_NaN": 1
  },
  "ordre": "expression KRAS croissante (log2(RSEM+1), la plus faible d'abord) ; KRAS = axe d'ordonnancement, jamais un flux",
  "KRAS_log2": {
    "min": 8.5697,
    "médiane": 10.2816,
    "max": 11.7273
  },
  "flux_csv": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes.csv",
    "sha256": "e012e9fdb4993f53bd08364e713d3755cf3c74bfe7ad5a1d5d911f974180fcc4",
    "lignes": 178,
    "colonnes": [
      "step",
      "PNLIP",
      "CTRB2",
      "CELA3A",
      "CTRB1",
      "CPA1",
      "CELA2A",
      "CPB1",
      "CELA3B",
      "CLPS",
      "XIST",
      "CTRC",
      "CPA2"
    ]
  },
  "nul_csv": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_nul.csv",
    "sha256": "5a845531466f226cd358e0b1d98b98571a74aa0bbecf3d400d52b3bbaf758067",
    "méthode": "mêmes lignes permutées, graine 42"
  },
  "règle": "Données du jour uniquement (téléchargement frais depuis Firehose). Aucune donnée ni conclusion d'une autre expérience importée (règle 15 nov. 2026)."
}
```
