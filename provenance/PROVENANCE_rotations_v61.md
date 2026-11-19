# Provenance — rotations de contrôle systématiques v6.1 (16 nov. 2026)

Construction : `build_rotations_v61.py`, même méthode que `build_rotations.py` (15 nov. 2026). Contrôle = 1re colonne, lignes triées par le flux-contrôle croissant, nul = lignes permutées (graine 42, un générateur par jeu, tirages séquentiels dans l'ordre des flux), colonne de contrôle intacte.

```json
{
  "date": "2026-11-16",
  "graine_nul": 42,
  "regle_lecture": "lire l'ordre de réaction des estimateurs, le test de bruit et les F1/F2 avant/après seuil ; jamais de consensus exigé ; plusieurs seuils critiques peuvent se succéder en chaîne causale ; un flux qui seuille avant un autre n'est pas faux.",
  "jeux": {
    "tcga_v4": {
      "base": "pdac_tcga_fluxes_v4.csv",
      "sha256_base": "e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0",
      "lignes": 178,
      "flux": [
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
      "rotations": {
        "PGC": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_PGC.csv",
          "sha256": "66d1f01b65cb1634c6daabf6a9b02b5e68a77adf649f28336c042e8e8aed089c",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_PGC_nul.csv",
          "sha256_nul": "30b1a0a3110987eacfb305bb872cf1f3bec06d0a0a619cc0a6e4abb141936f70"
        },
        "REG4": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_REG4.csv",
          "sha256": "cbb7aeb5a42675a9cadc64fcb37603bee4043345d14802ffce52ddfa3be93116",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_REG4_nul.csv",
          "sha256_nul": "246f5f0a6b63d6dd164fec3b19fe17686a856520bf1f28768629ea8d57b689c9"
        },
        "CLDN18": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_CLDN18.csv",
          "sha256": "ef90c6de14c8b5431888be41acbef8d1903bb84005d6834ebb4ede8d69ca70be",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_CLDN18_nul.csv",
          "sha256_nul": "081d15a126de852e55dafe3d6f2480d63ba27283a690935a4b70a739cc29cc8f"
        },
        "MUC17": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_MUC17.csv",
          "sha256": "f9b4c4a31fd87861dec7d6491218ff2d9aeb1fdbcca7deebcecb80a051223308",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_MUC17_nul.csv",
          "sha256_nul": "5dbd8d4b383b70ef9af51e57215592ed8dc8fcf76e9fc04a9678345ef449d6da"
        },
        "DPCR1": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_DPCR1.csv",
          "sha256": "32a350758e66094111eaec94650bb58a069dc618fd4aede1d002b52ebca69a85",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_DPCR1_nul.csv",
          "sha256_nul": "ae46cb91fd17ef9ee98f1ea9323ed841da84e67ec23c9eb1e9b16c6b07d07594"
        },
        "CR2": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_CR2.csv",
          "sha256": "a8a27df0441386ad8ebf5ed8db10ea44fb8a6a2a1ae4245ef14499b65bba0cc8",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_CR2_nul.csv",
          "sha256_nul": "eaf3858b0d6b1a5ae443d643db98fa759889dd7e6efe4fb45026d653443e7f2a"
        },
        "KRT20": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_KRT20.csv",
          "sha256": "60340eac1fd1fb02e61a0b4204586bab2e45715e38c3a6156b1d0d9976269eee",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_KRT20_nul.csv",
          "sha256_nul": "ce4e9b3fb8f5ca64a5b98fe40d46af9e57266600ba20fb83f03af5f384b9c81c"
        },
        "MUC2": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_MUC2.csv",
          "sha256": "58fb9d13d62afcaeb754dea36992db4f38f155b6844928fba75c8a651a272f09",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_MUC2_nul.csv",
          "sha256_nul": "d865b739f13538d1521388f5810ba1e783513f983bc959928d9974a52f62e044"
        },
        "GSTM1": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_GSTM1.csv",
          "sha256": "fdbbd8ba0e740d9b358ad9027bdc2059311658488529615d4b50884689684db0",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_GSTM1_nul.csv",
          "sha256_nul": "af009a17b5229676e491b4938f863f96ac54b316187cc94d71fcf00c642828aa"
        },
        "CEACAM5": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_CEACAM5.csv",
          "sha256": "533cf720b0dc8b8fb2caae913e824024372e9db88d39b3926e0fad0dcf236f30",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_CEACAM5_nul.csv",
          "sha256_nul": "172a0cfdc8a1613d7135743ab84ca2331352673c8554527b2fdb8bdc1b755295"
        },
        "CLCA1": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_CLCA1.csv",
          "sha256": "84bdaa03e4121861e40e03d4de761be03f322542468f9c263e9cb8cf9adb46d2",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_CLCA1_nul.csv",
          "sha256_nul": "dfe0d0718322fe0af4d4b67d8aaeeeeda516cf4565b4d90fb080717e905c0302"
        },
        "MUC16": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_MUC16.csv",
          "sha256": "3cc5fcd6c71fd96bacbac51726f2ce1d41b2a71e466b82d7689331f650a90566",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_v4_fluxes_v4rot_MUC16_nul.csv",
          "sha256_nul": "e90ea7d6383294f31d58c1b2b889a1826db9c7e1c411593066b0b701b2783322"
        }
      }
    },
    "depmap": {
      "base": "pdac_depmap_fluxes.csv",
      "sha256_base": "7d605fefb412fe16151a1b2508dffa6a1c2b8353600dccffd4af3333198e37f8",
      "lignes": 45,
      "flux": [
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
      ],
      "rotations": {
        "EFR3A": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_EFR3A.csv",
          "sha256": "0ae462f1f33cdb19bf6854d0c533e6da03e5ffc5efab8b5de042f8c30b3be596",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_EFR3A_nul.csv",
          "sha256_nul": "59748f72657a576288f43f13ada6bccfa980e5015dc871807556a4f0618fca83"
        },
        "RAB10": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_RAB10.csv",
          "sha256": "e50a710ffb118ebc29922cd9a2ade1e2e74cb42d4115df24da3374984358d738",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_RAB10_nul.csv",
          "sha256_nul": "f1ebcd8d664f23f1af3ca394d365a01a326b5d968a02e41bf4d6dd117ad617b2"
        },
        "CCND1": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_CCND1.csv",
          "sha256": "79299311905f21c58ae986678060b5c188d262bff3b4bcffbc8c733506a93926",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_CCND1_nul.csv",
          "sha256_nul": "a02a3b04c03421876d0786714a762fd44a1b6f16b56f9719ea3aeb721a0a0483"
        },
        "UROD": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_UROD.csv",
          "sha256": "4e798d792bb6883b5d2f780756bb81423fd8ad75d93a41a3555bc72863d9700e",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_UROD_nul.csv",
          "sha256_nul": "cde538fb4f0c28190efb00c59eecb7cf77486948d2079c6d5f02d1181ea02b26"
        },
        "CFLAR": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_CFLAR.csv",
          "sha256": "6720cefa5f36071d9a19d51e8b1dc2accdf744d23642dab361f0fe018d3e8366",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_CFLAR_nul.csv",
          "sha256_nul": "c3c7e60e1afbb7cbc7fd517cdf5ee2c088d4d924617db149fa637e9bdd3263ac"
        },
        "DOCK5": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_DOCK5.csv",
          "sha256": "2eea6d7ad17c93eb62039316c2fb4cdb08defa94206deffa586ec0230741b40c",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_DOCK5_nul.csv",
          "sha256_nul": "c42beae3d26281bdbced25e70284b9c3197892c0e6291cabb124793323b48467"
        },
        "MYH9": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_MYH9.csv",
          "sha256": "db8012b758613d275d49fb956e532611080ad84e8e6954a7cca6a2977ec5a319",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_MYH9_nul.csv",
          "sha256_nul": "1405978cb5c0aa06bb889b472510188940b772a78ed2a76fdf732ea5fa9a1f45"
        },
        "SCAP": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_SCAP.csv",
          "sha256": "7d3ef4d8efcd0303b2f701e5e13fcbbaa90da7719f406c8d159ee03e61df3ace",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_SCAP_nul.csv",
          "sha256_nul": "2999b706a4f55b0592ca0aba2dd3c8e4e463b2244d232cb6f748f279a0b8701f"
        },
        "RAB6A": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_RAB6A.csv",
          "sha256": "874f3c7b8d1fb5c53d6a0b64ca24e736085beefd056aad33164df7b0ec40c1d0",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_RAB6A_nul.csv",
          "sha256_nul": "7005594ebbe9ab66f3dbe2b382b74447b7f2e21f70d5d5c309049332272b5489"
        },
        "CRKL": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_CRKL.csv",
          "sha256": "6a476e240c76794eba077ad780a5fbcd79d642d12891993b2f3f18aa2de7c247",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_CRKL_nul.csv",
          "sha256_nul": "ab972182f806bde3bca4aab9bc126275f59b59c93854e1041bff5778c324d24c"
        },
        "MYC": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_MYC.csv",
          "sha256": "8032f8a13e6e3d97d900643f59328f4b9ce5c3424f61b5943585beeaae5879a5",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_MYC_nul.csv",
          "sha256_nul": "cc71aa4415fde5b466e5fa932b9b64fd5595f0957d25f8d5912cdccfd0adea4a"
        },
        "ACO2": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_ACO2.csv",
          "sha256": "e4bab2d862a876d8f739cf4d62342898983233ed3f431a3d942e26d1aa16ddf8",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_depmaprot_ACO2_nul.csv",
          "sha256_nul": "d42bd5bf85897db01b892b3b64799cf340ef82c6f1d2bfde6fa0ebdaf9fd21a5"
        }
      }
    },
    "immune_tcga": {
      "base": "pdac_immune_tcga_fluxes.csv",
      "sha256_base": "66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e",
      "lignes": 178,
      "flux": [
        "CD8A",
        "CD8B",
        "CD4",
        "FOXP3",
        "CD68",
        "CD163",
        "CD274",
        "PDCD1",
        "CTLA4",
        "GZMB",
        "IFNG",
        "CD19"
      ],
      "rotations": {
        "CD8A": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD8A.csv",
          "sha256": "9ecdcbcc35566afad254b2e021868243ae6ae510abca1544748f572e3c5502a1",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD8A_nul.csv",
          "sha256_nul": "273c0fbd63620a7325b91c330319360330339c81f791f3d7f06c26e5978a03bc"
        },
        "CD8B": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD8B.csv",
          "sha256": "d6d7f561072152343c2d6d5f9502756238f541e542c97d6b2019b06891468674",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD8B_nul.csv",
          "sha256_nul": "259cd12e854e30d2211c8ba7d45213639b7690af57f2880b1a2b57d9c2efc5ba"
        },
        "CD4": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD4.csv",
          "sha256": "a6d35be5f94bd979b0dfd409dc5730eff8a3dcfe6453e8ddd9d818612571df2e",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD4_nul.csv",
          "sha256_nul": "92fbe0c5297e15c2bdebb3ead5491f0a7a48bd5e5f6930a4ef804249a8488b75"
        },
        "FOXP3": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_FOXP3.csv",
          "sha256": "619657f06a35fb9f6eae74dd6752807dc0438c2f4ba63e9d6dc430fb04f49bc6",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_FOXP3_nul.csv",
          "sha256_nul": "a53651c0f652d6cceea7f5fbe874c288039ffc81d2ad970cbb0d95c032c0ef0a"
        },
        "CD68": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD68.csv",
          "sha256": "cd819c3924ed2c562a68773923b02f50bec28e6af078ad3c365444e09f785533",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD68_nul.csv",
          "sha256_nul": "fed095f084f3d200d006806e58935b2a3ff68c7702b505a88f1f6cd749a8838b"
        },
        "CD163": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD163.csv",
          "sha256": "00ae60f823df9f0f65dbff2750b5ae1a58a7f892e74c873062afe3b2aa57d0a8",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD163_nul.csv",
          "sha256_nul": "65bdc79766da9156288288bec23efb97511aada6bb6939f8edc6bc550e6f387f"
        },
        "CD274": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD274.csv",
          "sha256": "5b6833233229d8111e2cd859242307a3ca4e84471f1ad70081d58a0fc798df41",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD274_nul.csv",
          "sha256_nul": "191048aa2fde5d872e18a5ea097d6ccece7d2c0ee991c94b0bb4e6c0c55a002b"
        },
        "PDCD1": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_PDCD1.csv",
          "sha256": "192bfa7316d503f9c225ee4d43da21b68f9723b108f42a37a27f20d02432685d",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_PDCD1_nul.csv",
          "sha256_nul": "f40ee53558d164d9fc63ff7690c64c0bf8cf8e4d14048e53d2d8f19b8c5b9d81"
        },
        "CTLA4": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CTLA4.csv",
          "sha256": "00a34871d5b0693fd4b36b2e5a19917302d64b84bffcfcbc1e4315b321b7ad13",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CTLA4_nul.csv",
          "sha256_nul": "2e4c130ba080ab4ef4025e63ae3ee92b3507070f151fc2ac0ac8aa40be4dcb46"
        },
        "GZMB": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_GZMB.csv",
          "sha256": "ed4556f09263434ccb4dc959756711cca67192fdfdd14a8ce50cbe556a1a63ae",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_GZMB_nul.csv",
          "sha256_nul": "930f7eea8ab4408cd1a88970bfa7410c505da7adef3774a09b32069f1c81be13"
        },
        "IFNG": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_IFNG.csv",
          "sha256": "9a5fd89120455a2af3487e43147e50ad193657748517899d4dc37696333f0493",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_IFNG_nul.csv",
          "sha256_nul": "2ab8cd39bd28b052844f90ee8f980ea97a51f04a7eea2fe5924c9e369dfd0502"
        },
        "CD19": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD19.csv",
          "sha256": "18d8ae84e360f7cda1880f48d15d1f4db1a224f940206711197393c5c59d928c",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_immune_tcga_fluxes_immrot_CD19_nul.csv",
          "sha256_nul": "bc5c0555b622a6602919d1badcc01cacb208b30c4c56d138061c59221b6f39a3"
        }
      }
    },
    "parp_tcga": {
      "base": "pdac_tcga_fluxes_parp.csv",
      "sha256_base": "c9549b68280b2f4ca3d9b62020efa21ab97249b10e176de87ec528a0258c4309",
      "lignes": 178,
      "flux": [
        "PARP1",
        "PARP2",
        "BRCA1",
        "BRCA2",
        "ATM",
        "ATR",
        "CHEK1",
        "CHEK2",
        "RAD51",
        "XRCC1",
        "POLQ",
        "FANCD2"
      ],
      "rotations": {
        "PARP1": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_PARP1.csv",
          "sha256": "a5657638dff944d4c3e5d4915aacf8e119950cd0c99922af3569e8af910199f4",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_PARP1_nul.csv",
          "sha256_nul": "9de93308572d94dafb41a0c4b3bb84ac7ef8c03232e7fc4e06b43bb7a48da735"
        },
        "PARP2": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_PARP2.csv",
          "sha256": "a0c7d8d8ba581ffd403a398e8d14fd257c84651939b86944f935c56a222347e3",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_PARP2_nul.csv",
          "sha256_nul": "de9e33658538786fc2f0b3df8d1e43b2ba7bbdce1d563965d14ad52f8e3444be"
        },
        "BRCA1": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_BRCA1.csv",
          "sha256": "9632dec804931e59ea5cfc0af1587559490132b6b73db0cc85f03d79f4728b35",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_BRCA1_nul.csv",
          "sha256_nul": "31c5b201bfbe627cd1b332f0c3504d3b915c3fb5a1d5e86d30a65347233a6b1e"
        },
        "BRCA2": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_BRCA2.csv",
          "sha256": "afd6da72d10b46c015812d83a21ee204478011fe217f7f7975a908b9e363f65d",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_BRCA2_nul.csv",
          "sha256_nul": "6cac3ad7e14b686a32a0bc5504428cd33dd51aa2099c0aefb9d6c4c955b932d0"
        },
        "ATM": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_ATM.csv",
          "sha256": "b48f42f27da3e3ec2b0572cb81fd752e4254cd70b9617b6db5bddb84bf33a14b",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_ATM_nul.csv",
          "sha256_nul": "50b03adb7069762a6ddd87d1262052099218edcfef5ccf48a036310fba439122"
        },
        "ATR": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_ATR.csv",
          "sha256": "cc3f974f43cf7bb77c2a4d342e3f2e558dec9e14e073263c5d2889c1d3512ed6",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_ATR_nul.csv",
          "sha256_nul": "7cd5e670bf7049e5638d7aef1686fb2fa7d167dd9c9dbf038be1c904221117ce"
        },
        "CHEK1": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_CHEK1.csv",
          "sha256": "80205add1afec628af172826c7d1d0442223a6c2312a7f7121015f01261a79bb",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_CHEK1_nul.csv",
          "sha256_nul": "3006137fa379ee03c99c43bc38b62127b01ba2e3ee32ff3b41a76c9fe6350c58"
        },
        "CHEK2": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_CHEK2.csv",
          "sha256": "6f2dc84c2303dd68db7a66fde53b703319fdde09bc0a8ae78041b124406c6e22",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_CHEK2_nul.csv",
          "sha256_nul": "d630c26618518b3fe5fa115d2faa788cd1a46ac021680fceeb0d989c6263d037"
        },
        "RAD51": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_RAD51.csv",
          "sha256": "ad4554ccb151325131c526493037f4a3f4d7bd243929d3f165311a40dbbfe86e",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_RAD51_nul.csv",
          "sha256_nul": "00d4947c359c3a7cb804fafdd42b1b99e9720b2e0b387038b1b6367d96f9e4cc"
        },
        "XRCC1": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_XRCC1.csv",
          "sha256": "82f6c3294a461ea8876ea52fd6693aad63e2f97e26cd6c99f230b55152aef8a6",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_XRCC1_nul.csv",
          "sha256_nul": "ea7a0014bc57939c99899756b9c5965da5dd3aa1e35d6f83ce99eb46bcb5e36e"
        },
        "POLQ": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_POLQ.csv",
          "sha256": "6ec6ae8e7c52c87550f8d29044d4fb05fba08484c9e18ff173d1d68f146887a4",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_POLQ_nul.csv",
          "sha256_nul": "b8fd97042e24a1d424175a715ba87b61942e9611d91570399272e9a8a364221d"
        },
        "FANCD2": {
          "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_FANCD2.csv",
          "sha256": "999a79d6bdc58fa2155e887543b82c6951f8b9d3b4e1b4b9c10d49f49b65f326",
          "nul": "/home/hatch/workspace/runs/pdac-v6/pdac_parp_tcga_fluxes_parprot_FANCD2_nul.csv",
          "sha256_nul": "67a8ee7d7b104691816b4d2ebb5c84089f4a37c5d2bbab5b61a136f2b5e94231"
        }
      }
    }
  }
}
```
