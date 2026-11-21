# PROVENANCE_887 — Consolidation de §8.85 avec 10 nuls frais sur GDC ORGANOID-PANCREATIC (§8.87)

**Date :** 21 novembre 2026, ~10h07–11h00 EST (15h07–16h00 UTC).
**Agent :** TagPrint (subagent, piste 1 du lot du 21 nov. 2026).
**Chantier :** §8.87.
**Protocole gelé avant toute construction et tout run :**
`PROTOCOL_consolidation_gdc_887.md`, SHA-256
`956d5e447f0aad67a937f6bbd75c711960d94e75696b004b580f0cd69aa30ed2`.
**Pipeline :** v6.2, SHA
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
— vérifié avant et après le lot, jamais modifié, jamais exécuté
ailleurs que dans ce chantier.
**Livre blanc local vérifié (non édité) :**
`~/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md`
— lu pour la méthode §8.72, jamais modifié dans ce chantier.

## 1. Faits de départ : §8.85 (relus, jamais recalculés)

- Section §8.85 (`section_8.85_gdc_mucl3.md`, SHA-256
  `0e314d9f3d1a01dc19a1ae48552fa5a57c1d1ddd9de60853682b0c76f108aca7`) :
  GDC ORGANOID-PANCREATIC, n = 44, 12 flux dont MUCL3 ex-DPCR1,
  CONFIRME fragile non consolidé, `d_maxsep = +0,0884`
  (réel 0,2542142849980612 contre nul graine 42
  0,1657676706638558), nuls frais +0,0376 (s8851) / +0,0936
  (s8852), A2 10/14, LOO 9/13, C3 levée.
- Provenance §8.85 : `PROVENANCE_885.md`, SHA-256
  `fe26f4e0d2b5de30f9f666ccfedda07e1cfa5386905abba71823e53f66869f2b`
  (cohorte GDC, 55 TSV, manifeste SHA
  `f713edebf0f8afb20305b1472d480564e45ac31ce79e28350d7dde6ae496220b`,
  44 fichiers Tumor, MUCL3 `gene_id` ENSG00000168631.13 dans
  44/44, DPCR1 0/44, remappage vérifié R1–R5). Rien
  re-téléchargé dans ce chantier.
- Méthode de consolidation : §8.72 (`section_8.72_nulls_gse79668.md`,
  protocole `PROTOCOL_nulls_gse79668_872.md` SHA
  `95acdd45…cf41`) — 10 nuls frais, distribution primaire de 13
  nuls, `d_médian`, bande ±0,02 autour du plancher, catégories
  renommées pour le sens de la consolidation (protocole §8.87
  §4.3). Le §8.72 est cité comme méthode, pas comme résultat.

## 2. Nature des lignes

- Le CSV réel `pdac_885_gdc_organoid_fluxes.csv` est le même
  que §8.85 (44 lignes + en-tête, TPM GDC `tpm_unstranded`,
  ordre KRAS, MUCL3 ex-DPCR1) : mesures instrumentales du
  fournisseur, relues, jamais reconstruites ici.
- Les 10 nuls frais (graines 8871–8880) sont des échantillons
  hypothétiques (permutation des lignes du bloc des flux,
  `rng(graine)`, colonne `step` intacte), pas des mesures.
- Les résultats d'autres expériences cités dans la section
  (§8.85 : `d_maxsep = +0,0884` ; §8.72 : `d_médian = +0,1447`)
  sont des RÉSULTATS RAPPORTÉS, repris avec leur source — pas
  des mesures de ce chantier, pas des verdicts importés.

## 3. Graines gelées : nouveauté vérifiée avant le gel

- Graines 8871–8880, écrites dans le protocole avant toute
  construction. Vérifié le 21 nov. 2026 ~10h08 EST : aucun
  fichier `pdac_885_gdc_organoid_fluxes_nul_s887*` ni `*_s888*`,
  aucune occurrence de `nul_s88[78]`, `s88[78][0-9]`,
  `nul-seed 88[78]` ou `graine 88[78]` dans les `.py` / `.md` /
  `.txt` / `.sh` / `.json` de `~/workspace/runs/pdac-v6/` ; les
  deux occurrences nues « 8871 » du livre blanc sont des
  chiffres à l'intérieur d'une valeur `maxsep`
  (0,46234232096887146, TCGA v4), pas des graines — vérifié par
  lecture du contexte. Distinctes de 8721–8730 (§8.72) et de
  8851/8852 (§8.85).

## 4. Construction et runs

- Constructeur `build_nulls_887.py` (SHA-256
  `4da79e8a912b62634e96ed3a2f2a4ef681c0ef5e4b2587b2c4bfa4ec2be61e05`,
  script neuf de ce chantier) : permute le bloc des flux du
  CSV réel pour chaque graine, sans réécrire le CSV réel. Le
  constructeur `build_fluxes_885.py` (original intact) n'accepte
  pas de graine arbitraire (il ne construit que 8851/8852 avec
  `--fresh`) : il n'est PAS modifié et PAS invoqué ici — la
  permutation directe du CSV réel est la même méthode, sur la
  même entrée, et le CSV réel est vérifié inchangé graine par
  graine. Vérification de construction : 10/10 nuls — même
  en-tête que le réel, `step` intact, marginales préservées
  exactement par colonne, ordre différent du réel.
- CSV de flux :
  - réel `pdac_885_gdc_organoid_fluxes.csv`, SHA-256
    `a83b98175bdbc33525ba8a175aa898504d2cc44125b891d0902c6c6c26345eaf`
    (inchangé avant, pendant et après la construction) ;
  - nuls frais (SHA-256 complets dans `nulls_887_files.json`,
    SHA-256
    `7703708b79018d833479fa4528bc4f3c85e01876baff8cdb085c387d40bbe360`) :
    s8871 `4ad645ca2a9938d4aedffd84c8e5d32134a10a3838f19b879655b526cc6266d9`,
    s8872 `7888cdfdad7bab463a14b4ba1f4fd5462bf43f3571e9cfa38419742c5d940f46`,
    s8873 `804571d744a434f8884c0d9fd7e493d27c385592eddf98f9f736714226d87d47`,
    s8874 `605ae0228ce9425b945481e6c35de8c16d866b4e8f7563517d17fcbc58e65acb`,
    s8875 `2e74c5a0f5dd1cab4bcb0c52faffeed94565261ab7db73e9fc314bc9ee8622c8`,
    s8876 `ec2ca1a72869543574004acfa114fe0c92a3b1bd71dfa63be67e329c97b77a98`,
    s8877 `64e1eb438b9acd7ed528601cb9ce04d276484347c8dc4511adae229beacf2b59`,
    s8878 `7f46f5812ac75c41da930af17017e266e1815c754a53fa9e186acb87ecb69e50`,
    s8879 `5460483f94235e4b9205c278f4e9066c6633ca161ce24936b5b84a30307b7b63`,
    s8880 `449eff62d0c151689ae27e5ae5f24f659ef997bd4ae4276651915689bb99fd79`.
- Runs v6.2 mode fast, lanceur `run_v62_lot.sh` (reprenable,
  SKIP des sorties complètes), unité systemd `v62-887`
  (jamais nohup), surveillance `watch_v62_887.sh` (SHA-256
  `b3cdffb1eb32b6e539041567a2b790692946293e2fc04a0b1a87f7a2ef5f44e0`,
  modèle `watch_v62_872.sh`) :
  - manifeste `manifest_v62_887.txt` (SHA
    `d013077a1d01686c7730adcb6f027e872babb5a81237c6f8a93df38582c70913`),
    journal `runs_v62_887.log` (SHA
    `b9a0e84a1af568297c8e917c6bee90de339195ddbd404949e5c736e64247a698`),
    journal de surveillance `watch_v62_887.log` (SHA
    `98a986b13e8fe78bcdd616601733f9661ee60a6f98075ab64d013f8c66e5aa33`),
    début 2026-11-21T15:09:50Z, FIN 2026-11-21T15:41:40Z
    (~32 min, durées allongées par la contention CPU —
    d'autres lots v6.2 tournaient en parallèle sur la VM
    partagée), **10/10 exit 0, 0 déjà fait, 0 échec**,
    surveillance arrêtée d'elle-même à 10/10 (tour 2).
  - Aucun redémarrage de machine pendant le lot, aucune
    relance, aucun dossier supprimé.
  - Version lue sur les 14 runs (10 neufs + 4 relus) :
    `v6.2.0-L7aL7b-CohenD-short`.
- Extraction `extract_887.py` (SHA
  `1f608c82ee58400b59f039ac2d0207237daf1f0abaa54875009116281c98f57c`,
  réutilise `extract()` de `extract_858.py`, original intact),
  sorties `extract_887.json` (SHA
  `ca66461a50df41ec38e8cd3001e2fb6377b461c687d7902a98baa404a4cb5e74`)
  et `extract_887.csv` (SHA
  `5dfad9318d743cdf1d32083b5f2bb0465fdf420f38d009ff6f97e9471e7a7b5b`)
  et `dist_887.json` (SHA
  `aacd01c3e99554c3e6b8861a88c590602892ef9ea01d19256d818b5880cc28fd`).
- Vérification indépendante `verify_887.py` (SHA
  `b173c3733d4a5141d7ade7daeb6dec3992874054b328c7e2222ec3695f3298af`,
  relecture directe des `master_results.json` par `json.load`,
  chemin distinct) : **14/14 runs, écart max 0,0, verdict OK**,
  sortie `maxsep_887_verify.json` (SHA
  `9926c87de071ce4fddbdd14648e76c5d6bb727e28393737b841d12a6186cb381`).
  Second calcul indépendant des écarts `d_maxsep` depuis les
  `master_results.json` : identiques à l'extraction
  (écart < 1e-15, arrondi à 4 décimales identique).
- Relecture des valeurs §8.85 dans `extract_887.py` : réel
  0,2542142849980612, nuls 0,1657676706638558 /
  0,2165939226122164 / 0,1605986015484797 — 4/4 à 0,0 exact.

## 5. Ce qui manque / limites

- 13 nuls ne font pas un plancher stable : §8.53 estime ~200
  nuls pour un plancher stable à petit n. La médiane de 13
  nuls porte ~±0,02 — d'où la bande d'inconclusivité gelée
  (±0,02 autour du plancher). Ici `d_médian` (+0,0314) est sous
  la bande (0,05) : le verdict FRAGILE CONFIRMÉ ne tient pas à
  la bande. Mais la queue de la distribution (p95) reste
  estimée sur 13 tirages seulement.
- Le nul est une permutation par lignes (corrélations
  inter-flux préservées) : la distribution mesurée est celle
  du nul du projet, pas d'un nul à corrélations brisées
  (même réserve qu'au §8.53 §8).
- Le nul graine 42 est un tirage légitime, pas une erreur :
  il est sous le Q1, mais il appartient à la distribution.
- La section §8.87 (`section_8.87_consolidation_gdc.md`) est le
  livrable de ce chantier ; son SHA est calculé après
  écriture (auto-référence impossible dans ce fichier).
- Aucune note de correction ajoutée au §8.85 : la catégorie
  gelée FRAGILE CONFIRMÉ ne prévoit pas d'addendum (la lecture
  du §8.85 était déjà la bonne) — le fichier
  `section_8.85_gdc_mucl3.md` est intact (SHA
  `0e314d9f3d1a01dc19a1ae48552fa5a57c1d1ddd9de60853682b0c76f108aca7`
  vérifié après le chantier).

## 6. Fichiers produits par ce chantier (à hasher après écriture)

- `~/workspace/runs/pdac-v6/section_8.87_consolidation_gdc.md`
- `~/workspace/runs/pdac-v6/PROTOCOL_consolidation_gdc_887.md`
- `~/workspace/runs/pdac-v6/PROVENANCE_887.md` (ce fichier)
- `~/workspace/runs/pdac-v6/build_nulls_887.py`,
  `nulls_887_files.json`, `pdac_885_gdc_organoid_fluxes_nul_s8871.csv`
  … `pdac_885_gdc_organoid_fluxes_nul_s8880.csv`
- `~/workspace/runs/pdac-v6/manifest_v62_887.txt`,
  `runs_v62_887.log`, `watch_v62_887.sh`, `watch_v62_887.log`,
  `results_fast_v62_887_gdc_organoid_nul_s8871` … `..._s8880`
  (10 dossiers)
- `~/workspace/runs/pdac-v6/extract_887.py`,
  `extract_887.json` / `.csv`, `dist_887.json`,
  `verify_887.py`, `maxsep_887_verify.json`
- Données réutilisées du §8.85 (non re-téléchargées, non
  reconstruites) : `pdac_885_gdc_organoid_fluxes.csv`,
  `pdac_885_gdc_organoid_fluxes_nul.csv`,
  `pdac_885_gdc_organoid_fluxes_nul_s8851.csv`,
  `pdac_885_gdc_organoid_fluxes_nul_s8852.csv`,
  `results_fast_v62_885_gdc_organoid*` (4 dossiers),
  `extract_885.json`
