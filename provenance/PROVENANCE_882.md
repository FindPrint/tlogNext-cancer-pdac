# Provenance — §8.82 Cerveau, TCGA-GBM (Firehose)

```json
{
  "date": "2026-11-21",
  "protocole": "PROTOCOL_cerveau_privilege_882.md",
  "source": {
    "dépôt": "Broad GDAC Firehose stddata 2016-01-28, GBM",
    "fichier": "GBM.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt",
    "url": "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/GBM/20160128/",
    "fichier_local": "/home/hatch/workspace/runs/pdac-v6/data/tcga_gbm_rsem.tar.gz",
    "taille_octets": 14116395,
    "md5_observé": "cfc6cf0a2c3c2e9f0ea7a11f2ba32d28",
    "sha256": "9996a653f26c8cf8f0a5c56db49e2c847b49c0d1c9823daa5bb050d13749eb83",
    "matrice_interne": "gdac.broadinstitute.org_GBM.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0/GBM.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt",
    "matrice": "20503 gènes x 171 échantillons",
    "données": "RNA-seq V2 RSEM normalisé (TCGA, UNC Illumina HiSeq)"
  },
  "patients": {
    "critère": "échantillons tumoraux primaires, code TCGA 01",
    "retenus": 153,
    "écartés": 18,
    "cas_complets": 153,
    "transformation": "log2(RSEM normalisé + 1)",
    "correction_pureté": "aucune (scores acineux/îlots spécifiques au pancréas)"
  },
  "axes": {
    "prolifération": {
      "gènes": [
        "MKI67",
        "TOP2A",
        "PCNA",
        "CCNB1",
        "BUB1",
        "AURKB"
      ],
      "définition": "moyenne log2(RSEM+1) par patient"
    },
    "privilège": {
      "gènes": [
        "FASLG",
        "TGFB1",
        "TGFB2",
        "IDO1",
        "HLA-G",
        "CD47",
        "CD274"
      ],
      "définition": "moyenne des z-scores (dans la cohorte GBM) par patient"
    },
    "froid": {
      "gènes": [
        "CD8A",
        "CD4",
        "FOXP3",
        "PDCD1"
      ],
      "définition": "moyenne des z-scores (dans la cohorte GBM) par patient"
    },
    "grade": "non utilisable : tous les TCGA-GBM sont WHO grade IV par définition de la cohorte"
  },
  "gènes_v4_retenus": [
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
  "anti_doublon": "contrôle = colonne step ; scores de prolifération et de privilège absents des 12 flux (vérifié par assertion)",
  "prolif": {
    "ordre": "score de prolifération croissant",
    "flux_csv": {
      "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_882_gbm_prolif_fluxes.csv",
      "sha256": "426375d3596222ac2b41ddd76ee8c1c5dfee66333a869e6656b4407efd1442cb",
      "lignes": 153,
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
      "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_882_gbm_prolif_fluxes_nul.csv",
      "sha256": "7205fc40a0f674bebe30ea8e8ce1c2b30dd8917762e23d055a0a8bd606c3fa70",
      "méthode": "mêmes lignes permutées, graine 42"
    }
  },
  "privilege": {
    "ordre": "score de privilège croissant",
    "flux_csv": {
      "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_882_gbm_privilege_fluxes.csv",
      "sha256": "0f14466370d9db2ef42f4207a16171e6bd9128f9589ebcc0ead15caa0453133a",
      "lignes": 153,
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
      "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_882_gbm_privilege_fluxes_nul.csv",
      "sha256": "42213249ebaa0ae01745072f777e7f17610b4ce894760d51b084d6f41f1e74b0",
      "méthode": "mêmes lignes permutées, graine 42"
    }
  },
  "table_directe": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/gbm_882_direct_table.csv",
    "sha256": "72f3003d2095b0d9544b83c43edea92aee42ef1bcaf3e613b5b07f69e0fdc53e",
    "lignes": 153,
    "colonnes": [
      "step",
      "sample",
      "score_prolif",
      "score_privilege",
      "score_froid",
      "FASLG",
      "TGFB1",
      "TGFB2",
      "IDO1",
      "HLA-G",
      "CD47",
      "CD274",
      "CD8A",
      "CD8B",
      "CD4",
      "FOXP3",
      "CD68",
      "CD163",
      "PDCD1",
      "CTLA4",
      "GZMB",
      "IFNG",
      "CD19",
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
      "MUC16",
      "KRAS"
    ],
    "ordre": "score de prolifération croissant"
  }
}
```

## Runs v6.2 et extraction (21 nov. 2026)

- Pipeline : `universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
  vérifié avant ET après le lot, jamais modifié.
- Lot principal : `manifest_v62_882.txt` (SHA
  `bd3eb803797873ee0135786ebb626529918467f6bd67ec220f20574901274d50`),
  lanceur `run_v62_lot.sh`, journal `runs_v62_882.log` (SHA
  `c069b6e2b73b55cb26b13f8cc918ecec7b80cceb46c766ec21548b30b44e4d1c`) —
  4/4 runs, exits 0, FIN 2026-11-21T12:53:10Z. Unités systemd
  `v62-882` (lot) et `v62-882-frais` (nuls frais), jamais nohup.
- Nuls frais (règle gelée §7 : d = +0,0283 dans [−0,07 ; +0,14[) :
  `build_nulls_frais_882.py` (SHA
  `063be8c1542bf50d9631939e55c53c43aee2c72cc92d4c717fd2f9be5f98f77f`),
  `manifest_v62_882_frais.txt` (SHA
  `84215ef2b5635fa79470c3902579843703fa1ace6e51bd097af87af50acdd016`),
  journal `runs_v62_882_frais.log` (SHA
  `5a2a5a92f8868ce0820b74fe062ccede83923f64981715cbec0e981645eedac4`) —
  2/2 runs, exits 0, FIN 2026-11-21T13:02:35Z.
- Nuls frais (graines 8821 / 8822, mêmes lignes permutées) :
  `pdac_882_gbm_prolif_fluxes_nul_s8821.csv`, SHA-256
  `a76d10f18875926c2d7baf1f51046db38de63e6bc60367d377b4379914f9d68b` ;
  `pdac_882_gbm_prolif_fluxes_nul_s8822.csv`, SHA-256
  `65ed87f73e4fcd53d4e6fa101a697301120bb76a1aa75bd4141183ed33c6cad5`.
- Extraction : `extract_882.py` (SHA
  `ac0aa6ec80484338339c42dc63e36ba9c4f96f942cceeb9668f045c1a5d93bfa`),
  sorties `extract_882.json` (SHA
  `c3f97591046eabf7c6191e478d270bffe00a4e4dfad87a8fe27dfb15113ca783`) et
  `extract_882.csv` (SHA
  `3316e823b7dace407cf63c91b1329497f77f9681e17f496f5f769bc04400b06e`) —
  6 runs. Vérification indépendante `verify_882.py` (SHA
  `c47b94df0142e22e6506065eca7e94d8670e81a5b01dbba8cb8d39324e54cabb`) :
  maxsep et ancien MC recoupés à 0,0 exact sur les 6 runs.
- Tests directs : `direct_tests_882.py` (SHA
  `c901496af3cb15f3dca880b14881696042e650edf7b69ece241cbb620828dec4`),
  sorties `direct_tests_882.json` (SHA
  `58d6b4cf0867f46ba0af0774b86d2253dbe2a642479ba4bfb8bb8712c9a99330`) et
  `direct_tests_882.txt` (SHA
  `a6b08f275b6ce214efcee26c32ca089c4b10627e6019ec7843e2531f5f192316`).
- Construction : `build_fluxes_gbm_882.py` (SHA
  `dc58b600c2e214b3a2cbd4f04b486125f5ef4870c1443e172c8f6d9c8022779c`).

## Résultats (rappel, détail dans `section_8.82_cerveau_privilege.md`)

- Directs : privilège DESCEND (médiane rho −0,287, 0/7 positifs, 7/7
  p < 0,05 ; score privilège rho −0,477) ; froid FROID (médiane rho
  des 4 gènes T −0,129, 4/4 négatifs ; score froid rho −0,239,
  p=0,003).
- Pipeline paire primaire : d_maxsep +0,0283 (réel 0,2123 / nul
  0,1840) — PARTIEL ; nuls frais +0,0175 / +0,0402 — fragile, non
  consolidé. Paire secondaire : +0,0116.
- Taille : tarball 14 116 395 octets ; matrice interne 30 268 366
  octets, 20 532 lignes avant déduplication, 20 503 gènes uniques
  après (le champ `matrice` du JSON ci-dessus donne le nombre après
  déduplication).

## Ce qui n'a PAS été fait

- Aucun fichier clinique GBM téléchargé (pas de survie GBM, pas de
  statut IDH, pas de sous-type Verhaak dans ce chantier).
- Aucune correction de pureté (pas d'équivalent gelé pour le cerveau).
- Le GBM n'entre pas dans le compte A2 des paires PDAC ; C3 reste
  levée, test C reste NON, adoption pleine de maxsep inchangée.
