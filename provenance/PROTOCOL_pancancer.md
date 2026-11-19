# Protocole gelé — Bras 2 pan-cancer : l'axe KRAS → CA125/CEA est-il spécifique au pancréas ?

Date : 16 novembre 2026. Gelé AVANT tout téléchargement et tout run.

## Question
Le résultat robuste du projet PDAC — patients KRAS-forts = CA125 (MUC16) et CEA (CEACAM5) élevés,
3/4 cohortes pancréas : MUC16 top-12 +0,64 / +0,67 / +0,48 sd ; CEACAM5 +0,43 / +0,38 / +0,63 sd —
est-il une propriété générale de KRAS, visible dans d'autres cancers KRAS ?

## Cohortes
- TCGA LUAD (adénocarcinome pulmonaire), TCGA COAD (colorectal).
- Source : Broad GDAC Firehose stddata 2016-01-28, même route que PAAD :
  `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/<COHORTE>/20160128/`
  `gdac.broadinstitute.org_<COHORTE>.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz`
- Pour chaque matrice : taille + MD5 observés (aucun MD5 de référence publié par Firehose pour LUAD/COAD ;
  le MD5 observé est consigné et vérifié à chaque lecture).

## Construction des flux (script `build_fluxes_pancancer.py`, modèle `build_fluxes_tcga.py`)
- Tumeurs primaires uniquement (code TCGA 01, positions 14-15 du barcode).
- Valeurs log2(RSEM normalisé + 1), comme pour PAAD.
- Ordre : expression KRAS brute croissante. KRAS = axe, jamais un flux.
- Flux : les 12 mêmes gènes v4 que le pancréas, dans le même ordre :
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16.
  (Pas de correction de pureté : les scores acineux/îlots sont spécifiques au pancréas ;
  pas de re-sélection par variance — les flux sont FIXÉS par la question, sinon on ne testerait
  pas la réplication du même axe.)
- Règle ≥ 50 valeurs valides par gène, jamais d'imputation. Si un gène est absent ou a < 50 valeurs
  valides : le noter, et le remplacer par le gène suivant de la liste v3 hors gènes de sexe
  (PGC, REG4, CLDN18, MUC17, DPCR1 — tous déjà dans les 12, donc aucun remplacement sensé n'existe
  en pratique ; documenter ce fait) ; si aucun remplacement sensé n'existe, procéder avec les flux
  restants (minimum 10) et le dire.
- Nul : mêmes lignes permutées, graine 42 (même convention que tout le projet).

## Runs v6
- Pipeline `~/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py`,
  SHA vérifié avant lancement : `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`, jamais modifié.
- Mode fast, réel + nul par cohorte = 4 runs. Sorties complètes (cascade, MC, L7a, Delta).
- La cascade seule n'est PAS un verdict (règle du projet).

## Tests directs (verdict principal, script `pancancer_direct_tests.py`)
Conventions reprises EXACTEMENT de `parp_direct_tests.py` :
- Groupe KRAS fort = 12 dernières lignes (ordre KRAS croissant).
- top12_sd = (moyenne top12 − moyenne reste) / écart-type du gène (ddof=0).
- rho = Spearman entre l'indice de ligne (rang KRAS) et le gène ; p associée.
- Recouvrement Q3 : KRAS-forts au-dessus du quartile supérieur du gène (attendu 3/12).
- En plus : test de Welch top12 contre reste (t + p), comme demandé dans la mission.
- Mêmes tests sur le nul (graine 42) en témoin.
- Comparaison explicite avec le pancréas (référence mission : MUC16 +0,64/+0,67/+0,48 ;
  CEACAM5 +0,43/+0,38/+0,63).

## Critère de réplication (écrit avant les runs)
- Réplication : MUC16 ET CEACAM5 avec top12_sd > 0 dans la même direction que le pancréas,
  rho > 0 avec p < 0,05, et effet nettement au-dessus du nul.
- Réplication partielle : un seul des deux gènes.
- Non-réplication : aucun des deux, ou direction inversée.
- Un négatif est un résultat.

## Livrables (`~/workspace/runs/pdac-v6/`)
- `build_fluxes_pancancer.py`, `pancancer_direct_tests.py`, `run_pancancer_v6.sh`
- `data/tcga_luad_rsem.tar.gz`, `data/tcga_coad_rsem.tar.gz` (+ `.md5`)
- `pdac_luad_fluxes.csv`, `pdac_luad_fluxes_nul.csv`, `pdac_coad_fluxes.csv`, `pdac_coad_fluxes_nul.csv`
- `results_fast_pancancer_luad/`, `results_fast_pancancer_luad_nul/`,
  `results_fast_pancancer_coad/`, `results_fast_pancancer_coad_nul/`
- `pancancer_direct_tests.csv`, `pancancer_direct_tests.txt`
- `PROVENANCE_pancancer.md`, `pancancer.md`
