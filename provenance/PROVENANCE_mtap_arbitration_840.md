# Provenance — §8.40 Arbitrage de la contradiction MTAP (19 nov. 2026)

```json
{
  "date": "2026-11-19",
  "chantier": "Chantier 1 — Arbitrer la contradiction MTAP (S_sep +0,1968 contre MC -0,1642 et Delta -0,5416, §8.38)",
  "go": "Parent orchestrator, 19 nov. 2026, 06h55 (heure de Montréal) — chantier 1 du projet PDAC v6.2",
  "script": "mtap_arbitration_840.py",
  "script_sha256": "1fccc2f60d2c032c803b8ec26748200d6eb9296d4d464c455e6a68803ab4e7af",
  "execution": "systemd-run, unité mtap-840c, 19 nov. 2026, exit 0, durée 144,8 s (deux lancements antérieurs : mtap-840, exit 1 — bug de melt PRISM ; mtap-840b, exit 0 — avec les trois erreurs de comptage corrigées ensuite, voir § Corrections)",
  "sources": {
    "CRISPRGeneEffect.csv": {"depot": "DepMap Public 24Q4, figshare article 27993248, fichier 51064667", "taille_octets": 428678699, "sha256": "3d8f3ec6dbf2db7ff834b79b508622ec0b226f3518003fe96ecf5a4fcf167e3b"},
    "Model.csv": {"depot": "DepMap Public 24Q4, figshare article 27993248, fichier 51065297", "taille_octets": 645696, "sha256": "b7a0c1385e6cef30132b56aff61f1261d11e3f490490b355c430d32ee0dbdcfa"},
    "OmicsCNGene.csv": {"depot": "DepMap Public 24Q4, figshare article 27993248, fichier 51065324", "taille_octets": 1394554236, "sha256": "4851d3e939d48837a39a0f01294deb90fa507a85703586a927b77474f999134c", "md5_verifie": "4696565fa74dc805983bc278b4a41802 (exact, MD5 figshare annoncé)"},
    "Repurposing_Public_24Q2_Extended_Primary_Data_Matrix.csv": {"depot": "PRISM Repurposing Public 24Q2 (DepMap), déjà sur disque", "sha256": "3b6554cfc6c765af53088a676edc7bce00ee7d84fe808b93bbfa892de607bc3d", "md5": "042b15d3ebcc138a80a571b9286451ae"},
    "Repurposing_Public_24Q2_Extended_Primary_Compound_List.csv": {"depot": "PRISM Repurposing Public 24Q2, déjà sur disque", "sha256": "7e78f5901c1a97d2baab0789ab89832e716388da4eacaa9f094e7d2f2f5a3463"},
    "Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv": {"depot": "PRISM Repurposing Public 24Q2, déjà sur disque", "sha256": "13a85da9e45656c455d3911a4491f3636d7d0975a9d2333dc3d0a3e2cd3b0526"},
    "secondary-screen-dose-response-curve-parameters.csv": {"depot": "PRISM Repurposing 19Q4, Corsello et al. Nat Cancer 2020, figshare article 9393293", "taille_octets": 264340589, "sha256": "88d1013506e0cd6f191a51c5f3fdd3fb2be54f8afb4e19a5d1f8538e81fbfec8", "md5_verifie": "e629b9d505ad3d6bf65fde96f1c54bee"},
    "GDSC2_fitted_dose_response_27Oct23.xlsx": {"depot": "Cell Model Passports, groupe 46 GDSC2 IC50 Data, fichier 22870", "taille_octets": 22112537, "sha256": "0e99120a14a003dcbd3c27c020f1cfd35e38ee091067a2406f66c0d4dbc1c899", "md5": "7303bf3b53a3cfb8f03e739f51cc810d"},
    "mutation_table_pancreas.csv": {"depot": "Construite le 18 nov. 2026 (build_mutation_table_pancreas.py), MAF DepMap 24Q4", "sha256": "f3fa2bd2ddafdec83795211cd45de19ce88de674a2d660f47a5e72d813063f36"},
    "mtap_gistic_status.csv": {"depot": "Bras 1, 16 nov. 2026 (mtap_kras_tests.py), GISTIC2 Firehose 2016-01-28", "sha256": "b54cb94ff6aaba67e71524476d4e47c567f20ca8d49c09c52a9118977a7c38cb"}
  },
  "definitions_gelees": {
    "CN_DepMap": "relatif LINÉAIRE (1,0 = diploïde ; 0 = délétion homozygote), vérifié : médiane MTAP 0,832 sur 1 929 modèles, min 0,00, 0 valeur négative",
    "deletion_profonde": "CN < 0,5 (< 1 copie)",
    "sensibilite": "CN < 1 (sous-diploïde)",
    "Chronos": "plus négatif = plus dépendant",
    "PRISM_primaire": "log-fold-change viabilité, plus bas = plus sensible (une seule dose, 2,5 µM)",
    "PRISM_secondaire": "AUC dose-réponse, plus bas = plus sensible",
    "GDSC2": "LN_IC50 et AUC, plus bas = plus sensible",
    "seuil_test_par_compose": "n_délétées >= 5 ET n_intactes >= 5 (valeurs non manquantes)",
    "FDR": "Benjamini-Hochberg sur l'ensemble testé, par écran et par mesure",
    "Fisher": "exact bilatéral, critère pré-enregistré (§8.26)"
  },
  "corrections_en_cours_de_route": [
    "Fisher TCGA : la première version comptait la tumeur sans GISTIC (TCGA-FB-A4P6, NaN) dans la case « reste, non délétée » (166 au lieu de 165) et donnait p = 0,0409 au lieu de 0,0732. Corrigé : exclusion des NaN avant le test (n = 177 appariées, comme au §8.26). La sensibilité du Fisher à une seule tumeur est consignée dans la §8.40.",
    "GDSC2 : 242 036 lignes pour 235 748 paires (médicament, lignée) uniques — plusieurs courbes par paire. Sans déduplication, le Mann-Whitney comptait plusieurs fois la même lignée (ex. Acetalax n = 16/22 pour 8 délétées seulement, en tête du top-10). Corrigé : agrégation par médiane par paire avant tout test (5 783 lignes pancréas). Acetalax disparaît du top-10 corrigé.",
    "PRISM primaire : 1 ID BRD en double dans la liste des composés (AZ-628, REP.1M et REP.300) gonflait le comptage à 6 791 composés testés. Corrigé : déduplication des IDs (6 789 uniques, 6 790 lignes de matrice testées).",
    "PRISM secondaire : 54 noms de composés ont 2 broad_id — agrégation par (nom, lignée), médiane AUC, avant tout test (convention PROVENANCE_prism_secondary.md)."
  ],
  "sorties": {
    "mtap_arbitration_840.py": "1fccc2f60d2c032c803b8ec26748200d6eb9296d4d464c455e6a68803ab4e7af",
    "mtap_arbitration_840.log": "718139c607ee7b5a52b812a863b4af24e2bcc477b9eef4c4d5d8fd6ddde41a4a",
    "mtap_arbitration_840_stdout.txt": "e10c34e2b1295b9b1522cefa9b9c79a4597d5dcb5d885c2becb743cce566f286",
    "mtap_arbitration_840_results.csv": "277ca482c252899be0a4431f5031622734f4f1ca23b62a7c400ac845dafae135 (27 lignes : tous les tests directs a/c)",
    "mtap_arbitration_840_pancreas_lines.csv": "a10fd028186ed4c41126cd575e1e462b3fa07e7921ed284ca31b5d1f3a0b68a0 (47 lignées)",
    "mtap_arbitration_840_prism_primary.csv": "67466b24d200f84ffa96e9d325a82b4f9d4f5f791aa3c3522fb087f7f13bd928 (6 790 composés)",
    "mtap_arbitration_840_prism_secondary.csv": "39a63c42b4d013b19b9db080356b551155dc6bb516ef332f1bee23c189c9a926 (1 437 composés)",
    "mtap_arbitration_840_gdsc.csv": "ceaedd89138dffb915da3b4cdde694de5c79e5fefce2ffa8fd2a485da4a6c7ae (269 médicaments)"
  },
  "nature_des_lignes": "Dépendance CRISPR Chronos et copies CN = mesures instrumentales (criblage CRISPR, séquençage) ; viabilités PRISM et IC50 GDSC2 = mesures instrumentales de criblage ; statuts GISTIC = appels mesurés ; nuls : aucun nul dans ce chantier (tests directs, pas de run de pipeline). Aucun mot humain, aucun échantillon hypothétique.",
  "regle": "Données du jour uniquement pour les verdicts (19 nov. 2026). Les résultats antérieurs (§8.26/§8.28/§8.29/§8.36/§8.38) sont cités comme attendus de reproduction, pas réimportés comme verdicts. Aucun code original modifié ; aucun run de pipeline dans ce chantier ; PDF non régénéré, rien poussé sur GitHub."
}
```
