# Provenance — Bras 2 : paysage réparation / PARP (TCGA-PAAD, v6)

```json
{
  "date": "2026-11-16",
  "bras": "Bras 2 — paysage réparation de l'ADN / PARP le long de l'axe KRAS",
  "protocole": "gelé avant les runs (16 nov. 2026) ; TCGA-PAAD seulement pour les runs v6 ; GEO GSE71729 en contrôle direct seulement (pas de run v6)",
  "source_tcga": {
    "dépôt": "Broad GDAC Firehose stddata 2016-01-28, PAAD",
    "fichier": "gdac.broadinstitute.org_PAAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz",
    "url": "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/PAAD/20160128/",
    "taille_octets": 15296232,
    "md5_vérifié": "b09569ce3f4721f514bc137bd109ac0a",
    "matrice_interne": "gdac.broadinstitute.org_PAAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0/PAAD.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt",
    "matrice": "20532 gènes x 183 échantillons",
    "données": "RNA-seq V2 RSEM normalisé (TCGA, UNC Illumina HiSeq)",
    "téléchargement": "aucun — fichier déjà sur disque, MD5 vérifié"
  },
  "patients_tcga": {
    "critère": "échantillons tumoraux primaires, code TCGA 01",
    "retenus": 178,
    "écartés": 5,
    "transformation": "log2(RSEM normalisé + 1), valeurs BRUTES"
  },
  "gènes_flux": {
    "méthode": "liste FIXÉE par le protocole gelé (pas de sélection par variance)",
    "gènes": ["PARP1", "PARP2", "BRCA1", "BRCA2", "ATM", "ATR", "CHEK1", "CHEK2", "RAD51", "XRCC1", "POLQ", "FANCD2"],
    "n_valides_par_gène": "178/178 partout (règle >= 50 satisfaite)",
    "absents": [],
    "remplacements": "aucun — les 12 gènes sont présents ; aucune imputation",
    "médianes_log2": {"PARP1": 11.3405, "PARP2": 8.3647, "BRCA1": 7.6029, "BRCA2": 6.2352, "ATM": 9.9092, "ATR": 9.3448, "CHEK1": 7.0904, "CHEK2": 7.0758, "RAD51": 6.6832, "XRCC1": 9.74, "POLQ": 5.9625, "FANCD2": 7.5317}
  },
  "ordre": "expression KRAS BRUTE croissante (log2(RSEM+1), la plus faible d'abord) ; KRAS = axe d'ordonnancement, jamais un flux",
  "KRAS_log2_brut": {"min": 8.5697, "médiane": 10.2816, "max": 11.7273},
  "différence_v4": "v4 = résidus après régression pureté (acineux/îlots) + ordre KRAS résiduel. Ici = valeurs brutes + ordre KRAS brut, selon le protocole gelé de ce bras. La v4 reste intacte comme témoin.",
  "flux_csv": {"fichier": "pdac_tcga_fluxes_parp.csv", "sha256": "c9549b68280b2f4ca3d9b62020efa21ab97249b10e176de87ec528a0258c4309", "lignes": 178, "colonnes": ["step", "PARP1", "PARP2", "BRCA1", "BRCA2", "ATM", "ATR", "CHEK1", "CHEK2", "RAD51", "XRCC1", "POLQ", "FANCD2"]},
  "nul_csv": {"fichier": "pdac_tcga_fluxes_parp_nul.csv", "sha256": "57245c728dacf264654f77a4b4d6d608bbe3fb8c300b287061063bd062ab1360", "méthode": "mêmes lignes permutées, graine 42"},
  "script_construction": "build_fluxes_tcga_parp.py",
  "pipeline_v6": {
    "fichier": "runs/biophysique-hp35/universal_v6.0.0_cohen.py",
    "sha256_vérifié_avant_runs": "bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773",
    "modifié": false,
    "mode": "fast, cohen_d partout",
    "invocation": "python3 <v6> --input <csv> --mode fast --output <dir> (reprise de run_icgc_v6.sh)",
    "script_lancement": "run_parp_v6.sh",
    "journal": "runs_parp_v6.log"
  },
  "runs_v6": {
    "réel": {"sortie": "results_fast_parp", "exit": 0, "MC_meilleur_score": 0.355, "MC_règle": "uniform, 93 candidats, résolution 1,087 %, w_size 30, min_grp 6", "cascade": {"T_-2": "0,00 % (step 2)", "T_-1": "0,19 % (step 2)", "T_0": "3,19 % (step 6)", "T_+1": "25,55 % (step 45)", "T_+2": "25,55 % (step 45)"}, "L7a": "UP 16,84 %, désaccord (cible up, régime down)", "L7b": "FRAGILE (mode light)", "Delta": 4.3, "régime": "divergence", "CSD_majorité": "0/12 flux", "bruit_score_moyen": 0.487},
    "nul": {"sortie": "results_fast_parp_nul", "exit": 0, "MC_meilleur_score": 0.331, "MC_règle": "uniform, 93 candidats, résolution 1,087 %, w_size 30, min_grp 6", "cascade": {"T_-2": "0,00 % (step 2)", "T_-1": "15,48 % (step 28)", "T_0": "54,38 % (step 96)", "T_+1": "61,80 % (step 110)", "T_+2": "62,50 % (step 111)"}, "L7a": "UP 39,28 %, accord", "L7b": "FRAGILE (mode light)", "Delta": 4.04, "régime": "divergence", "CSD_majorité": "0/12 flux", "bruit_score_moyen": 0.691}
  },
  "tests_directs": {
    "script": "parp_direct_tests.py",
    "sorties": ["parp_direct_tests.csv (sha256 6feafa32aec9c10c50c82962b1795a2f8d6edc3a430b0f489369a9b058c5f7e9)", "parp_direct_tests.txt"],
    "conventions": "top12 = 12 dernières lignes (KRAS fort) ; top12_sd = (moy. top12 - moy. reste) / écart-type du gène (ddof=0) ; rho = Spearman gène vs rang KRAS (= vs KRAS brut) ; Q3 : attendu 3/12 sous indépendance ; seuil Bonferroni 12 tests : p < 0,0042"
  },
  "contrôle_geo71729": {
    "source": "GEO GSE71729, matrice déjà sur disque (data/GSE71729_series_matrix.txt.gz), plateforme GPL20769 Agilent, ID_REF déjà des symboles de gènes",
    "patients": "145 tumeurs primaires (Primary), cas complets 145/145, log-expression puce brute, ordre KRAS croissant",
    "script": "build_fluxes_geo71729_parp.py",
    "flux_csv": {"fichier": "pdac_geo71729_fluxes_parp.csv", "sha256": "99abbd6e08d7d2e1bc9ef60cb3b158f5d7d55e70ebbfec98cacebea1d936722c"},
    "nul_csv": {"fichier": "pdac_geo71729_fluxes_parp_nul.csv", "sha256": "3a8b076456f20bf5a66b6ec7354a70ddc290e04bec0a29fc0c425e963e684ce3"},
    "tests_directs": ["parp_direct_tests_geo71729.csv (sha256 b880679e9c8eac9b42ae163c15f8c3ec1bc416694f12980b159a02bd34bb73c8)", "parp_direct_tests_geo71729.txt"],
    "runs_v6": "aucun sur cette cohorte (contrôle direct seulement, comme le permet le protocole)",
    "KRAS_puce": {"min": 1.55, "médiane": 3.28, "max": 4.15}
  },
  "cohortes_non_faites": "ICGC PACA-AU et GSE62452 non testées dans ce bras (temps ; TCGA + GEO71729 suffisent pour le verdict, comme le permet le protocole)",
  "faits_antérieurs_cités_sans_réimport": {
    "CRISPR_génome_entier": "PARP1 rho +0,157 (FDR 0,89), PARP2 -0,120, BRCA1 -0,131, CHEK1 +0,260 (FDR 0,75) — tous non significatifs (rho = dépendance Chronos vs dépendance KRAS, pas expression)",
    "PRISM_15_nov": "aucun effet de classe PARP (médiane rho +0,032 sur 25 inhibiteurs PARP)"
  },
  "limites": [
    "ARN bulk BRUT, sans correction de pureté (choix du protocole gelé) : la composition tissulaire peut contribuer aux corrélations ; un re-test corrigé pureté (style v4) est nécessaire avant de dire 'tumeur-intrinsèque'.",
    "Expression ARN ≠ protéine ≠ statut mutationnel : ce bras ne teste ni les mutations BRCA1/2 ni l'indication PARP validée (mutation germinale BRCA, olaparib / essai POLO), qui reste indépendante de l'expression KRAS.",
    "Prolifération non contrôlée : BRCA2/ATR/CHEK1/RAD51 sont aussi des gènes du cycle cellulaire ; l'axe KRAS peut refléter en partie la prolifération.",
    "Corrélation ≠ causalité ; KRAS = expression ARN, pas statut mutationnel KRAS.",
    "L7b FRAGILE des deux côtés : l'audit de robustesse L7b est non informatif ici (comme établi : il dit FRAGILE sur réel et nul alike)."
  ]
}
```

## Vérifications effectuées le 16 nov. 2026

- SHA-256 du pipeline v6 vérifié avant les runs : `bb8bbdba…c0773` — conforme, fichier non modifié.
- MD5 du tarball Firehose vérifié : `b09569ce3f4721f514bc137bd109ac0a` — conforme, rien re-téléchargé.
- 12 gènes présents, 178/178 valeurs valides chacun ; aucun remplacement, aucune imputation.
- CSV : 178 lignes + en-tête, 13 colonnes (`step` + 12 flux), même format que la v1.
- Runs v6 fast séquentiels, exit 0 / 0. Un autre bras (immune) tournait en parallèle sur la même VM : les runs ont duré ~10 min au total au lieu de ~8.
- Cible du pipeline : PARP1 (première colonne numérique hors contrôles, politique fixed) — cible fixée, pas choisie par les données du jour.
