# Provenance — Bras 1 : MTAP / PRMT5 et l'axe KRAS (TCGA-PAAD)

```json
{
  "date": "2026-11-16",
  "bras": "Bras 1 — MTAP / PRMT5 et l'axe KRAS (test direct, pas de run v6)",
  "script": "mtap_kras_tests.py",
  "expression": {
    "dépôt": "Broad GDAC Firehose stddata 2016-01-28, PAAD",
    "fichier": "gdac.broadinstitute.org_PAAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz",
    "md5_vérifié": "b09569ce3f4721f514bc137bd109ac0a",
    "patients": "178 tumeurs primaires (code TCGA 01)",
    "transformation": "log2(RSEM normalisé + 1)",
    "gènes_écartés_NaN": 1
  },
  "copy_number": {
    "dépôt": "Broad GDAC Firehose analyses 2016-01-28, PAAD",
    "fichier": "gdac.broadinstitute.org_PAAD-TP.CopyNumber_Gistic2.Level_4.2016012800.0.0.tar.gz",
    "url": "https://gdac.broadinstitute.org/runs/analyses__2016_01_28/data/PAAD/20160128/",
    "taille_octets": 26189717,
    "md5_vérifié": "816034f742e8f89ca8734ca2cf4404d5",
    "sha256_vérifié": "6edc20f365d2f828bf5b4ef90a93f67344928d069cdd138eb946ed3275eed0ed",
    "fichier_interne": "gdac.broadinstitute.org_PAAD-TP.CopyNumber_Gistic2.Level_4.2016012800.0.0/all_thresholded.by_genes.txt",
    "matrice": "24776 gènes x 183 échantillons",
    "définition": "GISTIC2 all_thresholded.by_genes.txt : -2 = délétion profonde (homozygote), -1 = perte peu profonde (hétérozygote), 0 = diploïde, +1/+2 = gains",
    "tumeurs_appariées_expression": 177,
    "échantillons_gistic_totaux": 183
  },
  "définitions": {
    "axe_KRAS": "expression KRAS brute log2(RSEM+1) croissante",
    "KRAS_fort": "12 tumeurs à plus forte expression KRAS",
    "top12_sd": "(moyenne top12 - moyenne reste) / écart-type (ddof=0)",
    "seuil_Bonferroni": "p < 0,0167 (3 gènes, Spearman)",
    "permutation": "10 000 mélanges des 12 étiquettes KRAS-fort, graine 42",
    "correction_pureté_v3": "régression par gène sur [1, score acineux, score îlots] ; résidus (même définition que build_fluxes_tcga_v3.py)"
  },
  "faits_cités_sans_réimport": {
    "source": "balayage CRISPR génome entier DepMap 24Q4, 47 lignées pancréas (PROVENANCE_crispr_scan.md)",
    "dépendance_Chronos_contre_KRAS": {
      "PRMT5": "rho -0,189 (FDR 0,87)",
      "MTAP": "rho +0,071 (FDR 0,96)",
      "CDKN2A": "rho +0,161 (FDR 0,89)"
    },
    "note": "tous non significatifs ; cités comme contexte, pas comme verdicts de ce bras"
  },
  "contexte_clinique_cité": {
    "combinaison": "vopimetostat (inhibiteur PRMT5) + daraxonrasib",
    "résultat": "82 % de réponses chez les patients MTAP-délétés, phase 1/2 NCT06922591, ESMO 2026",
    "note": "résultat clinique externe, vérifié par le bras combinaisons ; pas une prédiction du pipeline"
  },
  "sorties": {
    "mtap_direct_tests.csv": "9b445ac01d625e42fe876889515f48d7ffea9f6b7836a506f572e907c2d47b83",
    "mtap_controls.csv": "51e1f93cb61b06facd3bbf35a342d2e133510352cb9ad18885cfbc3953a445e0",
    "mtap_gistic_status.csv": "b54cb94ff6aaba67e71524476d4e47c567f20ca8d49c09c52a9118977a7c38cb",
    "mtap_direct_tests.txt": "02c693ebfd170d454a294103faa0784dd77d05d7d0cf9dc2a397119a713152f5"
  },
  "règle": "Aucune imputation ; aucun proxy « MTAP bas » utilisé (le GISTIC mesuré était accessible) ; un négatif est un résultat ; données du jour uniquement pour les verdicts."
}
```
