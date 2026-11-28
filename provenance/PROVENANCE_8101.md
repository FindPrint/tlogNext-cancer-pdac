# PROVENANCE §8.101 — Consolidation GSE184585 à 200 nuls (28 novembre 2026)

Provenance complète du chantier §8.101 (consolidation à 200 nuls
de la seizième paire, GSE184585). Règle permanente du projet :
source complète, nature des lignes, comment chaque valeur a été
produite, hachages, ce qui manque. Auteur du chantier : TagPrint
(agent), sous la direction de Zackary Drasse-Ménard. Date :
28 novembre 2026. Dossier de travail :
`~/workspace/runs/pdac-v6/`. Livre blanc en lecture seule, non
modifié ; rien poussé sur GitHub ; aucun PDF ; aucune Release.
La section §8.101 est `section_8.101_consolidation_gse184585_200nuls.md`
(SHA `cb443b8adaa282f7b11a3b517bb7ea95c986488135062d92f6df8f799c0f0037`,
554 lignes).

## 1. Source des données (données brutes) — reprise du §8.99

Aucune nouvelle donnée brute n'est téléchargée dans ce chantier :
la source est la même qu'au §8.99, dont la provenance complète
est `PROVENANCE_899.md` (reprise ici par renvoi, sans re-saisie).

- **Série :** GSE184585, « Gene expression data from patients with
  pancreatic ductal adenocarcinoma », NCBI GEO, soumise le
  2021-09-23. Tissus PDAC primaires, Memorial-Sloan Kettering
  Cancer Center (NY, USA).
- **URL de la série :**
  `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE184585`
- **Matrice série :**
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE184nnn/GSE184585/matrix/GSE184585_series_matrix.txt.gz`
  - SHA-256 : `e2be8441979ee9210033fac588ed99e2605cdaa598e39e6d1e0d5304aad6de01`
  - Taille : 22 632 266 octets ; 70 523 sondes × 82 échantillons ;
    0 NaN ; plateforme GPL17586 (Affymetrix Human Transcriptome
    Array 2.0).
- **Annotation :** Bioconductor `hta20transcriptcluster.db` 8.8.0
  (tarball SHA `70680ab9…92f` ; SQLite extrait SHA
  `405837e1…a4dac`) + `org.Hs.eg.db` 3.23.1 (SQLite extrait SHA
  `bbdf1a4d…f3dba`) ; mapping `GPL17586_probe2symbol.tsv` (SHA
  `2592d258…9e`). Remappage DPCR1 → MUCL3 vérifié 5/5 (§8.99.1,
  `PROVENANCE_899.md` §3).
- **CSV réel :** `pdac_899_gse184585_fluxes.csv`
  - SHA-256 : `07540af57ef27974178036ea333f4ad51d9a19e49d7993f1d997b80fe6b99d13`
  - Forme : 82 lignes × 13 colonnes (`step` + 12 flux : PGC, REG4,
    CLDN18, MUC17, MUCL3 (ex-DPCR1), CR2, KRT20, MUC2, GSTM1,
    CEACAM5, CLCA1, MUC16). Ordre KRAS ascendant ; KRAS = axe
    d'analyse, jamais un flux. 0 NaN. Inchangé depuis §8.99
    (même SHA, re-vérifié 27 nov. 2026 14h35 UTC avant le gel).

## 2. Protocole gelé

- **Fichier :** `PROTOCOL_8101_gse184585_200nulls.md`
  - SHA-256 : `14e752c238fc4348222ac1f0c76b6a8b62c570927386846718dab5f998af22bf`
  - Gelé 27 nov. 2026 14h40 UTC (09h40 EST), avant toute
    construction de nul et avant tout run du lot §8.101.
  - Contenu : 190 nuls frais (graines 9311–9500), split gelé
    local blocs 0–9 (9311–9410) / GitHub blocs 10–18
    (9411–9500), règle de verdict gelée §8.93 §4 (plancher 0,07),
    garde-fou d'agrégation (refus d'un lot incomplet), registre
    A2/LOO au coordinateur.
  - Correction consignée dans le protocole lui-même (§0, 27 nov.
    14h50 UTC, avant tout run) : la première version du §5
    affirmait à tort que GSE184585 était l'une des 15 paires de
    la table A2-distrib ; vérification faite,
    `nulls_dist_893_table.json` contient 15 paires SANS
    GSE184585, 5 SOLIDE. La formulation corrigée la remplace.

## 3. Nuls frais (graines 9311–9500)

- **Script gelé :** `nulls_lot_next/scripts/build_null_893.py`
  - SHA-256 : `572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467`
  - Méthode : permutation de lignes entières (`rng =
    np.random.default_rng(graine)`, `perm =
    rng.permutation(n)`), colonne de contrôle (`step`)
    inchangée ; assertions (contrôle inchangé, mêmes lignes en
    multiset, 0 valeur manquante).
  - Correction de chemin consignée dans le protocole (§0) : le
    chemin `scripts/build_null_893.py` n'existe pas ; le fichier
    au SHA attendu est
    `~/workspace/runs/pdac-v6/nulls_lot_next/scripts/build_null_893.py`
    (même SHA confirmé sur les 5 copies du disque).
  - Absence de collision vérifiée avant le gel (calcul exact) :
    9311–9500 ∩ 9301–9310 = vide ; ∩ 9111–9300 = vide ;
    ∩ 9101–9110 = vide ; ∩ 3000–3999 = vide ; ∩ {42} = vide.
- **Construction locale (100 nuls, s9311–s9410) :**
  `build_nulls_8101.sh` (SHA
  `e6c22012ff050d89ee743c2f61b81c7040fc280bf0ab943461c6ceddda9665e8`),
  journal `build_nulls_8101.log` (14 484 o).
- **SHA-256 des 100 CSV nuls locaux** (fichier de référence
  `nulls_8101_local_sha256.json`, SHA
  `aa869640a00ddc3539499c686cb4eb5466fa32fd8b4a7e6b209a08aa6120803a`,
  100 entrées, 100 SHAs distincts) :

  - s9311 : `476dbede2cf0bb67319d5881ce80cb615ccc431b09dc191782c579e1e126623c`
  - s9312 : `d3c23537393bf8b595544d6087e603c59f0fc9435f6b85ca413e7f4d3bd6e144`
  - s9313 : `4274f3e75282c0b94331e8e5ce103b2db512d0a3cfe1ff7307aeeac2e9be5f43`
  - s9314 : `313502762b24e85057c2a9db81dc1deff2e52e191b2363b5151a2ca0e9dbab44`
  - s9315 : `35abb403baf1c3c562a328f1fed9ab005595bfa7e0d414d417ab7ab19974790a`
  - s9316 : `1266e177cc771f5b808d188ebdca8b39634bda66f2aa67dc34c1e335cae14a13`
  - s9317 : `57003585d7924e6b90fc80afdc16ecc70419c96999029d0b69b0390615765c71`
  - s9318 : `4b8eb28bf943b5b488c546d1f017f44b473f7a4e01a601fa7911a30603387f0b`
  - s9319 : `dcc2aa4b95a145e6eff84abc021fd7a06ac78ab97e6963505f3d8d6702a23ae8`
  - s9320 : `136c2d8486fffbce4ee21585fef9d2cbad85d98d296e2f74aa7ac35baaa60c93`
  - s9321 : `2a92723aa86828de2466c28886ace97544a193311770ec142d817f7c7216412a`
  - s9322 : `68bcb55dc01013fcf654c577ec1554984b5f32c58f48b711018b96222b42fb3c`
  - s9323 : `bb349cc9b21fb7c78c25d4722ac506758723b6652ff16653467390b56c7b270b`
  - s9324 : `95f420b1a99f035fa2197cc4d127b4b686de64b88e3169199a301c6ee9327de5`
  - s9325 : `a9c3f4c5d56d5fac7349dceae7958cf6181c0bb4a9b4b677d09cff5d4f32030c`
  - s9326 : `06badf5caac7a656af5109cc059c3aeae6a5755d3ac7c2d0b6db09c960e27715`
  - s9327 : `f18ddf95ff1b8efce7c0d8adc10b0ba302f3efd3cd8cd25da2ead556f95dd7c6`
  - s9328 : `02cf14d8ae8ffbc36ac22daf95610d6ef5a6a31ff094d2386148193a1e906f9f`
  - s9329 : `bd698b864b5988b96ce94c0766281eb9b8498d4447edda7bc6931d7cccc42628`
  - s9330 : `7d15827fb9f78fb47aba53490ddbc0237d8aba6657d3bba59a81b9e7e02c0808`
  - s9331 : `8b403485aaae8f6f063ee7a9078698fb3a0d25b87c102ef5f951a85e27f328df`
  - s9332 : `5d9aad2c76f50a8da4d705bb35a58c6246db4f4eed4394b94022d80b443fbab8`
  - s9333 : `5bbd4b05d01960c419b4bc90de220dd642a1e44115726b66956d0d08643fd26a`
  - s9334 : `893cb7cb017befe5edd25e34a9bdc7b543453a13b58b9109a9e9b6e93b2c75b7`
  - s9335 : `1efb81a7c93470eb6a5e7fac4059a54209c720dd112a967f9db0f02a1e599af0`
  - s9336 : `81a49432ab94a210b56b0d45895418b3dcc24ad6b8b8b1eef6cd57659b22d35a`
  - s9337 : `42c3450216e3b348840caaa1fa6010f0fb35a3b0136d043ef1dfcf5f52b77bf9`
  - s9338 : `53389000cfec852d4b722b2cbda5aa6c6e5f84ced3e1151981de1cd17de06b92`
  - s9339 : `a10c04f7b4b3c3d2165361059786426e92cf07317f98637fee3d23484c5acee2`
  - s9340 : `a3d6abeb719954251fdc4add8c3e1e8bc209fa9b2edb828bcfae207b9c16fe82`
  - s9341 : `486c6d43e22b5dd6ec9c96607d2aaca03526cac3bc54bc3beb51bfd955cb6c66`
  - s9342 : `8cb3c547b315a259a891fdb9b0e72f86ab2167a499313304460c66b6a6e7a87b`
  - s9343 : `9afc683c0412310c5890d3846c830116b60ae9654ae699f541758d3c2d6a7c64`
  - s9344 : `dc3192dfd8c7a5abf8a2584c009af1cf05ed19059a6db78bdae3dff43d2beb65`
  - s9345 : `26e65d98a908ed388c7eca6095b9dbcd1014fa63da642dd32cc984d677a46435`
  - s9346 : `15b9b82899cb8b3c2ba03bd123e28237f56958805e013724d8236f03d3080418`
  - s9347 : `14bf6307daedd6278902d0f881fc97d5364225ec943335e9cbc2b97ef66d7f93`
  - s9348 : `9bae149b2cd07b0db4e9a30e27e8bf5fe4007e9ad74d289b1e6b3d9bdb287bfc`
  - s9349 : `4846e4b2fb3bf6272bdca3c7cd3dca2e84dc4fdf67d61a421271bcfbc4e16970`
  - s9350 : `3bbfde7cb971f20d328bbb473c0375f8d2b82462fc1cb50d609a5c0ab9582035`
  - s9351 : `b91ec3adc63cc785ed31385557b421a54b0c1b6e20bd7befc40555ccd87338c6`
  - s9352 : `ffc4a86ab96826f6649e71be6e0fe960c0f1795d439ec55c40d25b6b01eb0ef9`
  - s9353 : `13aa7ad627759d2124acbc11bf2ea64c7ef175e53c9d9ec13ad116d6f94c9feb`
  - s9354 : `bd833e94c7a4dcda11d577550d4f6d4900ad67ca9790a2be1dd7682dab4f8181`
  - s9355 : `3ca3f30e91680f082c09aeb58e34be9238770926d9db67a29a881b275038a485`
  - s9356 : `a6d32f24d965acc6124053d158c09a2a8a8b25b73645b16d8ca9b0c18c27297d`
  - s9357 : `b959f24a863074619bd0a999c0b620a8aaf9863cf7a98d8893c67eb8ec561bc9`
  - s9358 : `c3d883ee06b90cb18bf5ec7c0297519d16c1f37b2738e35dc441066f976841ca`
  - s9359 : `8b2f0ca6f2ab4a74b097629303d48cce820529fe55f5dbe36dc3f98e3cd23d74`
  - s9360 : `a34318f36a8121063400f6a1e86521d1eb3ccf0f41f2b6cd3d70a2b2c168aec9`
  - s9361 : `fa2f2af4891f6def2a73066d3288d76a27b6379fe9d9e4aa225735b0a17c2db2`
  - s9362 : `1a207c2132aa213818735ef02d1007c1e8403dac273d4b11fc5bb22c0e14c689`
  - s9363 : `5060b842083bcba344042c7353e05b2112c23dd21b0392a087cb6f3e087df0f0`
  - s9364 : `7929cf9ce175b00e2e0607819a2e2be85e0a5359f380cc36c5631a6e1be6987c`
  - s9365 : `636dbdd99fbb52689c8603d65acc19919b83494010914cb3cc4b61aa6e027e26`
  - s9366 : `7dbfefdd10f6b887c1287fafc5af7b69e8303bc85ad7ab677822fecca9105675`
  - s9367 : `da6902e9bdb10c0b10494479e387942615402a43f8ebebb0e279dc0cde613bff`
  - s9368 : `59210937206f90cb0df8951d82de36257af624c4d2e51824400e589c9037a202`
  - s9369 : `b92b7589d8436cbf2b284f6492d029b37c93f61182ed39def5bff30df1d51557`
  - s9370 : `7af0564b580f873fb30ad8fd609e0501cb3bfdb96282915c05dd7cd133b59ba1`
  - s9371 : `a99d4be22219417e4d67ef20d9cc116f05cb419b53029dcbdf5bb2b05f959fc3`
  - s9372 : `3fd3388f3ade23de259e173c5e5fc312ab14cf62e5024857cddcd3be6f2fee17`
  - s9373 : `a10da0e4b529e3dee9b0eb9191e2bfe532b75ec64be08d978fef2695f18880d3`
  - s9374 : `a33bc7558fe97faa908af467f665d14823ec57154e30172e9241fc360c8595ab`
  - s9375 : `2e1b19e4b4d2ae9dad4f1b4e65ebcebeffccbe622f942dacb5d0f823b3d20ba3`
  - s9376 : `4b6f08f517dded337401b3a34470b651ec05c58d4277475de380125da6bc59be`
  - s9377 : `a25fb4810af135a2616ebeba34bf6d01351bd0b3b0fd8b1ca36c083b1cfcfec2`
  - s9378 : `3cba887c9b7698b5d8615e0db84aac9bb46da2796efd02504d61c84fd5bbfd55`
  - s9379 : `b69c140e6a9f637fc81d68409bb7419a44405bf24fa6d0007d1d3dbca9b3dcd0`
  - s9380 : `59cb08cd0f9ffdd3746da97b4ec64ffdb10d445d78364fe9678cc21e1a1de309`
  - s9381 : `5e9592c94443dbb4aeba0caae58b1f9726fa63f9ac75fd48184c8ede648dbc96`
  - s9382 : `414c58745af1d12832522305c25f81da1baff33fcb6929b92a95c31256777319`
  - s9383 : `8c4432170d5b1bd662a8e8c5508bc7bf2b2c54e6866e671ec98d4eb73809c658`
  - s9384 : `b7af1990432fa9ce27cd32b8723b961290873f257b9d6af39c6c2645a60000c9`
  - s9385 : `304c46b562265a38712dfd2426353d75a2e902f4179535482d0aef2905cf2cca`
  - s9386 : `c87e8ad57358b79806b7be21820355e9cfda6d4787638ed5763fab7e5274eb37`
  - s9387 : `e26d0f1936b08b8e7db5d16a168b3e966c7dd59f5452326b752067e5d02cd72e`
  - s9388 : `040a86c42d59f734b0194302279ec008d102c75bf4da13fd3b9eae2ab142af4e`
  - s9389 : `3f8465c0af0924fded0df66e0c0178a6c9f5b4c78da95eaefebff2dee0b38f9e`
  - s9390 : `3dc7ffa087a3510ef45f0efff895d1f68d2eb17e25338d05ef37da6ac6301131`
  - s9391 : `5e75f32c4e49e85afcc30c7d5e74f3de4c363f4a9c7ec16880628cf3d2d2e97f`
  - s9392 : `2eeffe1bc243a751d4843185beaa78003bb1d114f4e350468443fefcd0f4ddcd`
  - s9393 : `8894a50f0f749e855fdfbefc1083d161b38447cc22acdd6ddc9c030190c3535a`
  - s9394 : `9c6106bfb2ab90d4f390d0cef4c58547197d919c05b1791bc75d049c27c905db`
  - s9395 : `bb1a49b468589d14a65c472e953674e28f22c9f71b6486e6fc2a3889ef2766d4`
  - s9396 : `952f58b4a2c105a48c5cce77a4ef7daa3b28f234818ada170674955fcb6567c3`
  - s9397 : `a3d4c172768ee0c181f537460bb12e41c83ff6d6c26c31c32a15a10fb8be8617`
  - s9398 : `ff37fc2203f8c40ba038e6a2508d24a22873ce08096002b4b1c60c2d206e238f`
  - s9399 : `8a0b5b7388a884c2b27406276957208ce9ddcbbb29edc1025f71431063e09fef`
  - s9400 : `9d15da1bfe817acec8d6bd0246da2202293ae91797025f387ae0c12f2ef46221`
  - s9401 : `8d43f9155249af3935688223437e471d03796a0b3e1960cabbff1838269a062b`
  - s9402 : `b40a13cb2eefa3ad66062bf08a14709d6e9e849e75da993a3a22db6d871177d1`
  - s9403 : `410d54709cb5c6d4d8f2ab673ec3542c2a6dc41c158629f9a7899261db6aafa5`
  - s9404 : `34f9dc9066e763ade7b158954cd1e4858f0f43a7ed87a49946c4809423a350d3`
  - s9405 : `656a9e737b1625adccceb617fd02f108a7bd7bdcf843767bb42056be87271883`
  - s9406 : `8d9947046796d08db135f530160cf3c9e2c9529c577d737efb1f1a1fa2e824e3`
  - s9407 : `b08b7b0828f8dd50f0bb5b30d6f93653c76f0e1adf0f2170e6fc67e4abf0dd71`
  - s9408 : `6c7622a1b702080e796c7192c03a2cd327a25b3ca22cec17fb3f52b231688a94`
  - s9409 : `22d1127bc788fa6ce1a55b1dd191a6d468b3051a95cc34ccae3c487cf12b1f3e`
  - s9410 : `e58cf727b036e278b717fa6319b3cabf0c9623b6e33fb1310b39d879cc384919`

- **10 anciens nuls (s9301–s9310, §8.99) :** SHAs dans
  `PROVENANCE_899.md` §5 (s9301 `e67eb8bf…6397`, s9302
  `d153a6db…abf4`, s9303 `35d94cfc…cb4`, s9304 `bcf812b4…ba30`,
  s9305 `0edc936a…2b7`, s9306 `2edea177…50fe`, s9307
  `9b3e5791…424`, s9308 `5978da32…d904`, s9309 `58e90221…77d8`,
  s9310 `3f8dd192…1bba` ; empreintes complètes dans
  `PROVENANCE_899.md`). Dossiers
  `results_fast_v62_899_gse184585_nul_s9301` … `s9310`, déjà
  sur disque, inchangés.
- **90 nuls GitHub (s9411–s9500) :** construits sur le coureur
  GitHub Actions avec le même builder gelé (même graine → même
  fichier, le builder est déterministe : `default_rng(graine)`).
  Les CSV nuls eux-mêmes ne sont pas détenus localement (le
  workflow ne renvoie que `master_results.json.gz`, voir §4) ;
  leur identité repose sur le builder gelé + la formule des
  graines (`FIRST = 9311 + bloc*10`) + les vérifications SHA du
  workflow (v6.2, CSV réel, builder — `sha256sum -c -` pour
  v6.2 et le CSV réel), pas sur une comparaison bit-à-bit
  locale. Limite nommée au §8.101.8, même limite qu'au §8.98
  pour les 2 090 nuls GitHub.
- **Intégrité vérifiée après construction (locaux) :** 100/100
  (contrôle inchangé, mêmes lignes en multiset, 0 NaN, même
  forme 82 × 13).

## 4. Pipeline et runs

- **Pipeline :** `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`
  - SHA-256 : `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  - 624 157 octets, 13 033 lignes. Vérifié avant le lot
    (27 nov. 2026 14h35 UTC), en fin de lot local (marqueur
    `LOT_8101_DONE`, 28 nov. 2026 12h33:20Z, V6_SHA_OK) et
    avant l'extraction : inchangé. Fichier jamais modifié.
  - Version de travail v6.2 (adoptée 19 nov. 2026) ; v6.1 =
    référence (SHA `2af5e5ce…`) ; v6.0 historique (SHA
    `bb8bbdba…`).
- **Piste locale (100 runs, s9311–s9410) :**
  - Lanceur : `run_lot_parallel2.sh` (SHA
    `493423a334669e5e1008e47c4eabd6286c8b99f47d4b02b63ca8cc64559ef121`),
    tel quel, non modifié, 2 workers en parallèle ; fichier de
    tâches `tasks_8101.txt` (SHA
    `7131bbb2b622a883f9e6f5ef73c42e253f1a338634a24ef1d12dc930ccd11e3a`) ;
    logs `logs_8101/` (un log par run + résumés) ; hook de
    surveillance `watch_8101.sh` (SHA
    `9790d5634b27be3972d718e8a9cd99601c93c5203853f1001c3a3d7474b618d1`,
    96 tours × 900 s).
  - Lancement : `systemd-run --unit=v62-lot-8101 --collect`,
    jamais `nohup`, aucun dossier de run écrasé ; lanceur
    reprenable (saute tout run dont `master_results.json`
    existe).
  - Validation du lanceur parallèle avant le lot (27 nov. 2026
    14h48 UTC, protocole §2) : 2/2 runs parallèles exit 0, SHA
    v6.2 inchangé ; `csd_consensus.json` et
    `csd_fractal_estimators.csv` bit à bit identiques à la
    référence séquentielle, maxsep identique (s9311 : 0,2217) ;
    `master_results.json` diffère sur 8 feuilles seulement,
    toutes hors calcul (`memory_cap`, `available_memory_bytes`,
    `dashboard_status/path`, `telemetry_path`). Aucune valeur
    calculée ne diffère.
  - Déroulement : 27 nov. 14h49 → 28 nov. 12h33 UTC (~22 h),
    100/100 `master_results.json`, 0 échec. Journal
    `watch_8101.log` ; marqueur `LOT_8101_DONE` (SHA
    `6ac3d92b281223d961830c9fa168ed6cdadfb8481da148c73ca487bf9634e8c8`,
    voir §7). Redémarrages machine pendant le
    lot (8 comptés au 28 nov. 06h42), 0 run perdu ; nuit
    immobile ~18h00 (27 nov.) → 05h45 (28 nov.) après un
    redémarrage probable vers 18h00 (probable, pas prouvé —
    journal système = boot courant seulement) ; ralentissements
    s9384/s9385 (34 min) et s9386/s9387 (bloqués ~80 min après
    la phase paysage, terminés en 4 min après redémarrage à
    neuf), cause non établie.
  - Dossiers : `results_fast_v62_8101_gse184585_nul_s9311` …
    `s9410` (100 dossiers).
- **Piste GitHub (90 runs, s9411–s9500) :**
  - Workflow : `pipeline-nulls-lot-899-consolidation.yml`
    (SHA `5e4587b1202464f71218472f4fe53f894df0c2556196ae9f05548d014dae76e2`),
    dépôt FindPrint/tlogNext-cancer-pdac, commit `8bb5d29c`.
    Matrice `pair: [gse184585]` × `block: [10..18]` (9 jobs,
    max-parallel 9), déclenchement manuel
    (`workflow_dispatch`), régénération des nuls sur le coureur
    avec le builder gelé, vérification SHA de v6.2 + CSV réel
    avant de tourner, artefacts `master_results.json.gz`
    seulement (`nulls-8101-gse184585-s9411-s9420` …
    `s9491-s9500`), rétention 7 jours, `timeout-minutes: 120`.
  - Run nº 1, ID **46045446830**, déclenché 27 nov. 2026
    ~12h56 EST : **9/9 jobs `completed success`**, vérifié
    13h41 EST via l'endpoint jobs de l'API GitHub.
  - Artefacts téléchargés 27 nov. 2026 13h42–13h43 EST via le
    navigateur : 9/9 zips (~84 Mo), décompressés dans
    `results_fast_gha_8101_gse184585_nul_s<graine>/` — **90/90
    `master_results.json` présents** ; contrôle ponctuel s9411 :
    maxsep 0,1351.
- **Réel :** `results_fast_v62_899_gse184585` (§8.99, inchangé,
  maxsep 0,3712, seuil 72,50).
- **Commande (identique aux lots précédents) :**
  `python3 universal_v6.2.0_cohen.py --input <csv> --mode fast
  --output <dossier>`

## 5. Extraction et jugement

- **Script :** `extract_8101.py`
  - SHA-256 : `5d623974c03117b8f8c082c27d4a745ca6fff2e33f1481cc46ea5f96636f3fdb`
  - Adapté de `extract_899.py` (SHA
    `939b90f6545672c6609980b82e8b0beac36efdf7c8f312481558e7c949c9d0fe`).
  - Lit `master_results.json` →
    `run_pipeline/threshold_metadata/threshold_optimization/best_config`
    (metrics : max_separation, s_norm, stability, robustness,
    sharpness ; threshold). MC pipeline = 0,3·s_norm +
    0,3·stabilité + 0,2·robustesse + 0,2·sharpness (formule
    réplique §8.93 ; facteur 0,8 non appliqué : w_size fast 80
    ≥ n//10 = 8). Lit aussi `reading_synthesis.Delta_tension`
    et `falsification_vs_null` (delta_vs_null,
    is_significant_nonlinearity), `prediction_levels.L7a_coherence`
    et `L7b_robustesse`, `five_threshold_cascade`
    (max_F1_velocity, max_F2_curvature, T_-2..T_+2).
  - Tests directs : Spearman de chaque flux vs KRAS (valeurs
    KRAS relues depuis la matrice série via le mapping gelé,
    méthode `pandas` Spearman ; mêmes valeurs qu'au §8.99, le
    réel est inchangé).
  - Verdict selon la règle gelée §8.93 §4 (plancher 0,07) ;
    quantiles par interpolation linéaire (position p×(n−1),
    n = 200) ; valeurs arrondies à 4 décimales.
  - GARDE-FOU : le script REFUSE d'agréger un lot incomplet
    (exit 2 + liste des `master_results.json` manquants) —
    lancé seulement après les 201 `master_results.json`
    vérifiés présents.
- **Sorties :**
  - `extraction_8101.json` (SHA
    `34f1b79ff2278e225166eac89ed5232328590e5e95cb457a5cbafd0b7f873002`,
    15 857 o) : réel + 200 maxsep + 200 MC + statistiques +
    tests directs + scores compagnons + lecture A2.
  - `nulls_8101_gse184585_table.csv` (SHA
    `c3dfc1f932bac6075883104f0313208fe98e34f77846234ba690dd6862bfe227`,
    202 lignes : en-tête + réel + 200 nuls, colonnes graine,
    piste, maxsep, mc, écart réel−nul).
- **Vérification croisée de l'extraction :** les valeurs du
  réel et des 10 anciens nuls sont reprises de
  `extraction_899.json` (SHA `ee175155…7`) à 0,0 exact (même
  chemin de lecture, même script d'extraction adapté) ; les
  190 nouveaux nuls sont lus une fois, sans re-saisie.
- **Résultats (valeurs produites par le pipeline et par
  l'extraction, pas par une main humaine) :**
  - maxsep réel 0,3712 (seuil 72,50 ; s_norm 0,1835 ; stabilité
    0,9905 ; robustesse 5,3×10⁻²⁷ ; sharpness 0,0152).
  - Nuls maxsep (200) : min 0,1351 (s9411) ; médiane 0,2257 ;
    p95 0,3014 ; max 0,3969 (s9337). 199/200 nuls sous le réel.
  - Écarts réel−nul : 188/200 > 0,07 (94,0 %) ; min −0,0257
    (s9337, au-dessus du réel) ; max +0,2361 (s9411) ;
    d contre médiane +0,1455 ; d contre p95 +0,0698 ;
    rang 200/201.
  - MC réel 0,3552 ; MC nuls médiane 0,3337, p95 0,3494, min
    0,3205, max 0,5032 (4 nuls > 0,40 : s9323 0,5032, s9402
    0,4013, s9412 0,4039, s9426 0,4520).
  - Delta réel 1,2804 ; falsification Δ vs nul 0,2974, non
    significative ; L7a down (confiance 0,1914) ; L7b FRAGILE
    (light) ; F1 vitesse max 0,6418 ; F2 courbure max 0,1415 ;
    cascade T : 6,01 / 22,84 / 94,05 / 97,05 / 100,00.
  - Spearman vs KRAS : PGC +0,029 ; REG4 −0,048 ; CLDN18
    +0,224 ; MUC17 +0,117 ; MUCL3 +0,176 ; CR2 −0,237 ;
    KRT20 −0,393 ; MUC2 −0,072 ; GSTM1 −0,304 ; CEACAM5
    +0,550 ; CLCA1 −0,531 ; MUC16 +0,057. Δρ médian −0,0098 ;
    6/12 positifs.
  - **Verdict : FRAGILE** (réel > p95 des nuls, mais 94,0 %
    des nuls sous le plancher < 95 % exigés ; règle §8.93 §4).
    Le verdict SOLIDE à 10 nuls du §8.99 ne survit pas à la
    consolidation.

## 6. Registre A2-distrib (lectures, pas mise à jour)

- Le registre A2/LOO appartient au coordinateur (§8.99.4) ;
  ce chantier ne met à jour AUCUN registre.
- Lecture du script d'agrégation (`extraction_8101.json`,
  champ `a2_lecture`) : table §8.93 (`nulls_dist_893_table.json`,
  5 SOLIDE / 15) + GSE184585 FRAGILE → **5/16**. Cette lecture
  reprend la table §8.93 telle que publiée, où ICGC est encore
  FRAGILE.
- Lecture à 200 nuls (§8.98 + §8.101) : **paires PDAC seules
  5/16** (TCGA v4, Immunitaire TCGA, PARP TCGA, GSE57495,
  ICGC) ; **en comptant HP35 (témoin positif biophysique,
  SOLIDE à 200 nuls) 6/16**.
- LOO (convention §8.98.5 : retirer un SOLIDE) : 16 paires,
  6 SOLIDES → **5/15** ; paires PDAC seules (15 paires,
  5 SOLIDES) → **4/14**.
- A2 classique : non touché par ce lot (le nul graine 42 de
  GSE184585 a déjà été couru au §8.99 : maxsep 0,1833, écart
  réel−s42 +0,1879 > 0,07, déjà compté dans le 11/16 du
  §8.99).

## 7. Fichiers du chantier (avec SHA-256)

- `PROTOCOL_8101_gse184585_200nulls.md` :
  `14e752c238fc4348222ac1f0c76b6a8b62c570927386846718dab5f998af22bf`
  (gelé 27 nov. 2026 14h40 UTC, avant toute construction et tout run)
- `section_8.101_consolidation_gse184585_200nuls.md` :
  `cb443b8adaa282f7b11a3b517bb7ea95c986488135062d92f6df8f799c0f0037`
  (554 lignes)
- `PROVENANCE_8101.md` : ce fichier.
- `build_nulls_8101.sh` :
  `e6c22012ff050d89ee743c2f61b81c7040fc280bf0ab943461c6ceddda9665e8`
- `tasks_8101.txt` :
  `7131bbb2b622a883f9e6f5ef73c42e253f1a338634a24ef1d12dc930ccd11e3a`
- `run_lot_parallel2.sh` :
  `493423a334669e5e1008e47c4eabd6286c8b99f47d4b02b63ca8cc64559ef121`
- `watch_8101.sh` :
  `9790d5634b27be3972d718e8a9cd99601c93c5203853f1001c3a3d7474b618d1`
- `pipeline-nulls-lot-899-consolidation.yml` :
  `5e4587b1202464f71218472f4fe53f894df0c2556196ae9f05548d014dae76e2`
- `nulls_8101_local_sha256.json` :
  `aa869640a00ddc3539499c686cb4eb5466fa32fd8b4a7e6b209a08aa6120803a`
- `extract_8101.py` :
  `5d623974c03117b8f8c082c27d4a745ca6fff2e33f1481cc46ea5f96636f3fdb`
- `extraction_8101.json` :
  `34f1b79ff2278e225166eac89ed5232328590e5e95cb457a5cbafd0b7f873002`
- `nulls_8101_gse184585_table.csv` :
  `c3dfc1f932bac6075883104f0313208fe98e34f77846234ba690dd6862bfe227`
- `LOT_8101_DONE` :
  `6ac3d92b281223d961830c9fa168ed6cdadfb8481da148c73ca487bf9634e8c8`
  (contenu : `LOT_8101_DONE 100/100 2026-11-28T12:33:20Z V6_SHA_OK`)
- `pdac_899_gse184585_fluxes.csv` :
  `07540af57ef27974178036ea333f4ad51d9a19e49d7993f1d997b80fe6b99d13`
- `universal_v6.2.0_cohen.py` :
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
- `nulls_lot_next/scripts/build_null_893.py` :
  `572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467`
- Données sources : voir §1 et `PROVENANCE_899.md`.

## 8. Nature des lignes et ce qui manque

- **Nature des lignes :** chaque ligne du CSV réel est une tumeur
  PDAC primaire (MSKCC, réséquée) ; chaque colonne de flux est
  une mesure instrumentale d'expression (microarray HTA 2.0,
  valeurs déposées dans la matrice série) ; `step` est un rang
  humain (0..81, ordre KRAS ascendant), pas une mesure ; MUCL3
  est la mesure du gène historiquement nommé DPCR1 (remappage
  vérifié 5/5, §8.99.1). Chaque ligne d'un CSV nul est une
  permutation des lignes du réel (les flux d'une tumeur
  voyagent ensemble) ; chaque `master_results.json` est une
  sortie du pipeline v6.2 sur un CSV (réel ou nul). Aucune
  valeur n'est inventée, imputée ou mise à l'échelle. Le pipeline
  ne voit jamais la variable de contrôle physique ni la vérité
  terrain ; l'ordre KRAS est un axe d'analyse, pas un temps.
- **Ce qui manque / dettes nommées :**
  1. Mise à jour du registre A2/LOO (coordinateur ; §6).
  2. Les 90 CSV nuls GitHub ne sont pas détenus localement
     (§3) — identité par builder gelé + graines + SHA du
     workflow, pas par comparaison bit-à-bit locale.
  3. SOFT GEO GPL17586 complet (abandonné, > 1,2 Go —
     remplacé par les bases Bioconductor, §8.99.1).
  4. Étude aval Zhao et al. (BMC Genomics 2023, 24:101) ayant
     fusionné GSE184585 à d'autres jeux : non lue pour ce
     chantier.
  5. Aucune archive Release séparée pour ce lot (à la
     différence du lot §8.98, archivé en 43 morceaux,
     Release `v6.2-8.98-nulls-2850`) : les 201
     `master_results.json` sont détenus localement (dossiers de
     runs + `extraction_8101.json` + table CSV) ; les artefacts
     GitHub expirent ~4 déc. 2026 (rétention 7 jours).
- **Ce qui n'a pas été fait :** aucune modification du livre
  blanc, aucun PDF, aucune Release, aucun push GitHub ;
  `tlogNext-pdac-phase2`, `universal-log-research` et Kaggle non
  touchés ; pipeline jamais modifié ; aucune affirmation
  clinique ; aucune formulation de prédiction (formulations
  d'analyse uniquement).
