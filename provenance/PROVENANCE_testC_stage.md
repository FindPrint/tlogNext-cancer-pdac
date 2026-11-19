# Provenance — Test C : série TCGA v4 ordonnée par stade clinique (19 nov. 2026)

```json
{
  "date": "2026-11-19",
  "test": "Test C — série TCGA v4 ordonnée par stade clinique",
  "protocole": "PROTOCOL_testC_stage.md (gelé avant les runs)",
  "go": "chantier 3, go parent 19 nov. 2026",
  "source": "Broad GDAC Firehose stddata 2016-01-28, PAAD, RSEM genes normalized, tarball déjà sur disque",
  "tarball": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/data/tcga_paad_rsem.tar.gz",
    "md5": "b09569ce3f4721f514bc137bd109ac0a"
  },
  "base_v4": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v4.csv",
    "sha256": "e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0"
  },
  "clinique": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/data_clinical_patient.txt",
    "sha256": "0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5",
    "contenu": "TCGA PanCanAtlas, 184 patients PAAD, 0 doublon PATIENT_ID",
    "colonne": "AJCC_PATHOLOGIC_TUMOR_STAGE (7e colonne)",
    "edition_ajcc": "7e (colonne AJCC_STAGING_EDITION)",
    "stades_bruts_184_patients": {
      "STAGE IIB": 121,
      "STAGE IIA": 30,
      "STAGE IB": 15,
      "STAGE III": 5,
      "STAGE IV": 5,
      "STAGE IA": 5,
      "(vide)": 2,
      "STAGE I": 1
    },
    "patients_sans_stade": 2,
    "provenance_acquisition": "MANQUANTE — fichier déjà sur le disque au début du chantier (15 nov. 2026, 15h13 UTC) ; aucune entrée dans fetch_tcga.log, download_firehose.log ni PROVENANCE_tcga*.md ; premier hachage consigné ici ; rien re-téléchargé"
  },
  "verification_reproduction": {
    "méthode": "résidus v4 recalculés depuis le tarball, triés par résidu KRAS croissant, comparés au CSV v4",
    "échantillon": 178,
    "écart_max_12_flux": 1.7763568394002505e-15,
    "écart_max_PGC": 1.7763568394002505e-15,
    "atol": 1e-09,
    "résultat": "reproduction exacte (écart <= atol)"
  },
  "jointure": {
    "méthode": "patient = 12 premiers caractères du code-barres échantillon RSEM (code 01) vers PATIENT_ID clinique",
    "tumeurs_appariées_stade_connu": 175,
    "tumeurs_exclues_sans_stade": [
      "TCGA-3A-A9I5-01A-11R-A38C-07",
      "TCGA-3A-A9IO-01A-11R-A38C-07",
      "TCGA-IB-7654-01A-11R-2156-07"
    ],
    "patients_cliniques_sans_rsem": 7
  },
  "ordre": {
    "définition": "rang du stade principal I=1, II=2, III=3, IV=4 ; sous-stades repliés (IA/IB -> I, IIA/IIB -> II)",
    "départage_ex_aequo": "code-barres échantillon TCGA, ordre lexicographique croissant (neutre)",
    "effectifs_par_stade": {
      "I": 21,
      "II": 146,
      "III": 4,
      "IV": 4
    },
    "sous_stades_par_stade": {
      "I": {
        "STAGE IB": 15,
        "STAGE IA": 5,
        "STAGE I": 1
      },
      "II": {
        "STAGE IIB": 118,
        "STAGE IIA": 28
      },
      "III": {
        "STAGE III": 4
      },
      "IV": {
        "STAGE IV": 4
      }
    },
    "spearman_rang_stade_vs_rang_KRAS": {
      "rho": 0.1364,
      "p": 0.07186255847316378
    },
    "recouvrement_top12_stade_vs_KRAS": 1,
    "composition_12_dernières_lignes": {
      "STAGE IV": 4,
      "STAGE III": 4,
      "STAGE IIB": 2,
      "STAGE IIA": 2
    }
  },
  "série": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v4_stage.csv",
    "sha256": "d7608bc90c861d62eb3c5cd9b9bf859d56a800e029f6f7f7c5191f46c45ea39c",
    "lignes": 175,
    "colonnes": [
      "STAGE",
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
    "ordre": "(rang de stade, code-barres) croissants",
    "contrôle": "STAGE (1re colonne, pas un flux — pas de doublon)"
  },
  "nul": {
    "fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_tcga_fluxes_v4_stage_nul.csv",
    "sha256": "4e37368458c8aed9c1981aaeb38f76e77ad9796a2a6d9a88ab20644a0ff534fe",
    "méthode": "bloc des 12 flux permuté par lignes, graine 42, contrôle intact"
  },
  "script": "build_fluxes_tcga_v4_stage.py"
}
```

## Runs et lecture (ajout après 2/2, 19 nov. 2026)

```json
{
  "pipeline": {
    "fichier": "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py",
    "sha256": "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf",
    "revérifié_avant_et_après_runs": true,
    "v6.1_sha256": "2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9",
    "v6_sha256": "bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773"
  },
  "lot": {
    "manifeste": "manifest_v62_stage.txt",
    "lanceur": "run_v62_lot.sh (reprenable, saute les sorties complètes)",
    "unité_systemd": "v62-stage (lancement 2026-11-19T13:20:58Z, arrêtée d'elle-même à 2/2)",
    "surveillance": "watch_v62_stage.sh (tour 1/48, complets=2/2)",
    "journal": "runs_v62_stage.log",
    "fin": "2026-11-19T13:56:15Z, deja_faits=0 termines=2 echecs=0",
    "durée": "35 min (machine partagée, 3 runs en parallèle, charge moyenne jusqu'à 6,5)",
    "incident": "aucun (pas de redémarrage tué, aucun dossier supprimé)"
  },
  "runs": {
    "réel": {
      "entrée": "pdac_tcga_fluxes_v4_stage.csv",
      "sortie": "results_fast_v62_stage",
      "exit": 0,
      "fichiers": 36,
      "cascade_pct": [1.08, 29.0, 98.41, 100.0, 100.0],
      "cascade_pas": [2, 50, 171, 174, 174],
      "mc_score": 0.3472,
      "mc_seuil_pct": 10.99,
      "max_separation": 0.2898,
      "stability": 0.9818,
      "s_sep": 0.2846,
      "delta": 3.852,
      "l7a": "UP 0.164",
      "falsification": 0.642,
      "l7b": "FRAGILE"
    },
    "nul": {
      "entrée": "pdac_tcga_fluxes_v4_stage_nul.csv",
      "sortie": "results_fast_v62_stage_nul",
      "exit": 0,
      "fichiers": 36,
      "cascade_pct": [1.62, 44.23, 60.75, 69.93, 69.93],
      "cascade_pas": [3, 77, 106, 122, 122],
      "mc_score": 0.3507,
      "mc_seuil_pct": 10.99,
      "max_separation": 0.1998,
      "stability": 0.9917,
      "s_sep": 0.1981,
      "delta": 3.83,
      "l7a": "DOWN 0.415",
      "falsification": 0.774,
      "l7b": "FRAGILE"
    },
    "écarts_réel_moins_nul": {
      "mc": -0.0036,
      "delta": 0.0225,
      "falsification": -0.1318,
      "max_separation": 0.09,
      "s_sep": 0.0864
    }
  },
  "lecture": {
    "script": "stage_reading.py",
    "script_sha256": "7fe2e49f4e3f72a49fd0b4e6ad5f061bab64ca57285c5f2e690e7ad1c22adc44",
    "sorties": {
      "stage_direct_tests.csv": "76292bfd05f9f3c3ff294044ea79f91486910ae9e8f161cdc15fe252663a34e0",
      "stage_extract.json": "d7f0da2afcd3d2e3126d2e80b1d8a81d59454f4373e3f612bc43d5147e03c01f"
    }
  },
  "section": {
    "fichier": "section_8.45_testC_stage.md",
    "sha256": "9add43f019b9e5429e10c34e2e1f4f2f537a353363a5e8f1e4fc80442e661506",
    "note": "fichier séparé ; livre blanc NON édité, PDF NON régénéré, rien poussé sur GitHub"
  },
  "verdict": "NON — la chaîne ne réapparaît pas sous l'ordre stade (bloc en hausse, MUC16 plate) ; pipeline ne sépare pas réel et nul"
}
```
