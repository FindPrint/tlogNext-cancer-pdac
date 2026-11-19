# Provenance — §8.43 : série MTAP avec la dépendance PRMT5 comme flux (19 nov. 2026)

```json
{
  "date": "2026-11-19",
  "chantier": "Chantier 1 — Série MTAP avec la dépendance PRMT5 comme flux (§8.43)",
  "go": "Parent orchestrator, 19 nov. 2026",
  "protocole": "PROTOCOL_mtap_prmt5_flux.md (gelé avant toute construction et tout run)",
  "protocole_sha256": "1e56ed9a127c28c9a86140ae2c088bf046fab6935a6cf8fd51a8e87d66ae161d",
  "pipeline": {
    "fichier": "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py",
    "sha256": "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf",
    "sha256_reverifie_apres_runs": "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf",
    "references": {
      "v6.0.0": "bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773",
      "v6.1": "2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9"
    },
    "mode": "fast",
    "version_dans_json": "v6.2.0-L7aL7b-CohenD-short"
  },
  "sources": {
    "CRISPRGeneEffect.csv": {"depot": "DepMap Public 24Q4, figshare article 27993248, fichier 51064667", "taille_octets": 428678699, "sha256": "3d8f3ec6dbf2db7ff834b79b508622ec0b226f3518003fe96ecf5a4fcf167e3b"},
    "Model.csv": {"depot": "DepMap Public 24Q4, figshare article 27993248, fichier 51065297", "taille_octets": 645696, "sha256": "b7a0c1385e6cef30132b56aff61f1261d11e3f490490b355c430d32ee0dbdcfa"}
  },
  "lignees": {
    "critere": "OncotreePrimaryDisease == 'Pancreatic Adenocarcinoma'",
    "dans_Model.csv": 64,
    "dans_GeneEffect.csv": 45,
    "adeno_absents_de_GeneEffect": ["ACH-000031", "ACH-000107", "ACH-000205", "ACH-000270", "ACH-000933", "ACH-001072", "ACH-001101", "ACH-001171", "ACH-001376", "ACH-001378", "ACH-002164", "ACH-002738", "ACH-002742", "ACH-002743", "ACH-002744", "ACH-002745", "ACH-003429", "ACH-003430", "ACH-003433"],
    "ecart_nomme": "les tests directs §8.28/§8.29/§8.40 portaient sur 47 lignées (45 + 2 adénosquameux KP-3 ACH-000108 et L3.3 ACH-000685, présents dans GeneEffect) ; la série de flux utilise les 45 adénocarcinomes seuls, comme toutes les séries DepMap du projet (§8.30)"
  },
  "flux": {
    "retenus_9": {"PGC": "PGC (5225)", "REG4": "REG4 (83998)", "CLDN18": "CLDN18 (51208)", "MUC17": "MUC17 (140453)", "CR2": "CR2 (1380)", "KRT20": "KRT20 (54474)", "CEACAM5": "CEACAM5 (1048)", "CLCA1": "CLCA1 (1179)", "MUC16": "MUC16 (94025)"},
    "exclus": {
      "DPCR1": "aucune colonne Chronos dans DepMap 24Q4 (17 916 colonnes de gènes vérifiées)",
      "MUC2": "aucune colonne Chronos dans DepMap 24Q4",
      "GSTM1": "GSTM1 (2944) présent mais 8 NaN sur 45 lignées — exclu sans imputation ; exclure les lignées donnerait n=37 < 40 (minimum fast)"
    },
    "nan_flux_retenus": 0,
    "chaine_kras_testable": "3 gènes sur 4 (PGC, CLDN18, MUC16) ; DPCR1 non testable en Chronos"
  },
  "ordre": {
    "axe": "Chronos PRMT5 (10419) croissant, plus dépendante d'abord",
    "prmt5_sur_45": {"min": -2.9369, "mediane": -1.0888, "max": -0.6466},
    "ex_aequo": "aucun (ordre défini)",
    "prmt5_dans_csv": "non — axe seulement, jamais un flux",
    "controle": "step",
    "cible": "PGC (repli du pipeline, 1er flux)"
  },
  "series": {
    "reel": {"fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_prmt5.csv", "sha256": "bb575a2cadaa4f8bc69181032c3f311e3d9ce4cc0905e2667eccb316f63050df", "lignes": 45, "colonnes": ["step", "PGC", "REG4", "CLDN18", "MUC17", "CR2", "KRT20", "CEACAM5", "CLCA1", "MUC16"]},
    "nul": {"fichier": "/home/hatch/workspace/runs/pdac-v6/pdac_depmap_fluxes_prmt5_nul.csv", "sha256": "014a084f1e62b7e7e593297afa6c603b893f78d83432a1fbf9f049f52db9e20e", "methode": "mêmes lignes permutées, graine 42, step intact"},
    "minimum_fast_v6.2": 40,
    "marge": "45 lignes, passe de 5 points"
  },
  "runs": {
    "lanceur": "run_v62_lot.sh, manifeste manifest_v62_prmt5flux.txt",
    "lancement": "systemd-run --unit=prmt5flux-v62 --collect (jamais nohup)",
    "journal": "runs_v62_prmt5flux.log (FIN 2026-11-19T13:39:42Z, deja_faits=0 termines=2 echecs=0)",
    "reel": {"sortie": "results_fast_v62_prmt5flux", "fichiers": 35, "exit": 0},
    "nul": {"sortie": "results_fast_v62_prmt5flux_nul", "fichiers": 35, "exit": 0},
    "incident": "aucun"
  },
  "lecture": {
    "script": "prmt5_flux_reading.py",
    "script_sha256": "3c05a04fe7beda53031f5c938415972cdc117ee4272c6b792fa59c8b064cf48c",
    "direct_tests_csv_sha256": "6e92c43d919adcd8e3a37a42b2c20f4e5b2b18143ae689b198f20e13b664b671",
    "extract_json_sha256": "b58269908b90659ff452630eda0aca5e54cb3c2078d8c0d7be76025906b39121",
    "ordre_lignees_sha256": "92e0b73c9cdd1584e6c699c4b18f34fe7c9fb71d74e25154282eef52dcc8d30b"
  },
  "construction": {
    "script": "build_fluxes_depmap_prmt5.py",
    "script_sha256": "7d68de199d94da5a4c01c832eaca9766bbc6a331090eaf169fda34b488ff69e3"
  },
  "resultats": {
    "cascade_reel_pct": [0.6046, 3.6046, 6.6046, 35.2995, 35.2995],
    "cascade_nul_pct": [2.2015, 66.3827, 73.1061, 82.0708, 84.3119],
    "mc_reel": 0.3390174011746773,
    "mc_nul": 0.3386150962883997,
    "s_sep_reel": 0.18967205881261553,
    "s_sep_nul": 0.2873986375369073,
    "delta_reel": 1.761006,
    "delta_nul": 1.911981,
    "l7a_reel": "DOWN 0.3401",
    "l7a_nul": "DOWN 0.1794",
    "falsification_reel": "delta_vs_null 0.153641, ok, seuil 0.5",
    "falsification_nul": "indisponible (comparaison impossible sans les deux dimensions)",
    "bruit": "indisponible des deux côtés"
  },
  "nature_des_lignes": "Dépendance CRISPR Chronos = mesure instrumentale (criblage CRISPR) ; ordre PRMT5 = classement mesuré, pas un temps ; nul = permutation (graine 42). Aucun mot humain, aucun échantillon hypothétique.",
  "ce_qui_manque": "DPCR1 sans mesure Chronos (chaîne testée sur 3/4 gènes) ; GSTM1 exclu (8 NaN) ; n=45, marge de 5 au-dessus du minimum fast ; 2 adénosquameux hors série ; falsification du nul indisponible ; bruit indisponible des deux côtés ; T_0 réel au pas 3 (seuil de bord, fenêtre avant de 3 points).",
  "regle": "Données et runs du jour uniquement pour les verdicts (19 nov. 2026). Résultats antérieurs (§8.28/§8.29/§8.36/§8.40) cités comme attendus de comparaison, jamais réimportés comme verdicts. Livre blanc non édité directement ; PDF non régénéré ; rien poussé sur GitHub."
}
```
