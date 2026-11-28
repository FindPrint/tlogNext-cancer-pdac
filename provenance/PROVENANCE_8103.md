# PROVENANCE — §8.103 Chantier D : nouvelle tentative d'élucidation de Delta

Date : 27 novembre 2026. Go : Zackary, 27 nov. 2026 09h52 (« il faudrait
regarder le delta, il ne faudrait pas l'oublier »). Agent : TagPrint
(agent du chantier D). Protocole gelé avant tout calcul neuf.

## 1. Protocole et code

- Protocole gelé : `~/workspace/runs/pdac-v6/PROTOCOL_8103_delta_w.md`,
  SHA-256 `1c896cbb7fdd0ddfddf9b1a6b869eb4a4f07835ca5eb6b933635298a280b548a`.
- Pipeline v6.2 : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`,
  SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  — vérifié avant travail, avant chaque lot et après chaque lot ;
  jamais modifié. **Aucun run du pipeline dans ce chantier.**
- Builder de nuls gelé : `~/workspace/runs/pdac-v6/nulls_lot_next/scripts/build_null_893.py`,
  SHA-256 `572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467`.
- Réplique B4 : `~/workspace/runs/pdac-v6/replica_w_894.py` (chantier
  §8.94, importée, non modifiée) — `build_df_feat`, miroir des lignes
  7075–7187 du pipeline v6.2.

## 2. Corpus B1 (§8.98) — ce qui est présent, ce qui manque

- Dossiers candidats : 3 015 (`results_fast_gha_893_*` 2 090 +
  `results_fast_v62_893_*` 910 + 15 réels) dans
  `~/workspace/runs/pdac-v6/`. Extraits : **3 015/3 015, 0 erreur**,
  0 dossier sans `master_results.json` dans le périmètre 893.
- Chaque paire : 200 nuls (graines 9101–9300) + 1 réel, vérifié par
  comptage. Réels E1 : `results_fast_v62_hp35|tcga_v4|geo71729|
  geo62452|icgc|immune_tcga|parp_tcga|depmap`. Réels E2 :
  `results_fast_v62_869_geo21501`, `870_geo79668`, `871_geo60979`,
  `874_yeh_ff`, `879_geo57495`, `885_gdc_organoid`, `888_gse194249`.
- Nature des lignes : sorties instrumentales du pipeline
  (`master_results.json` : D_vector, `per_estimator.raw_median`,
  `best_config.w_size`) ; matrices d'entrée = mesures omiques
  publiques (TCGA, GEO, ICGC, DepMap) ou série biophysique simulée
  (HP35) et leurs nuls permutés (graines 9101–9300, règle gelée
  `default_rng(graine)`, lignes entières permutées, contrôle inchangé).
- Ce qui manque : rien dans le périmètre 893 — le corpus §8.98 est
  complet sur disque (3 000 nuls + 15 réels). Les 2 dossiers sans
  `master_results.json` trouvés par l'inventaire initial
  (`results_fast_v62_8101_gse184585_nul_s9312|s9313`) appartiennent au
  lot §8.101, hors périmètre de ce chantier, et ne sont pas comptés.

## 3. Scripts et sorties du chantier

- `v62_delta_8103.py` — extraction B1 (SHA-256
  `dce2c857081cd3c27cdae799f724699b4a89359bfb265e964931f850f39a5337`,
  log `v62_delta_8103.log`, lanceur `run_delta_8103_extract.sh`
  SHA-256
  `688690e3b4117718f0080b5145a09ed7aa1ce868d9604abc2c22994eca45031b`,
  gardien `watch_8103_extract.sh` SHA-256
  `1542b6752158c86e9932562eba037f01244266c7d3415b732201bb6ebad1fbf5`,
  unité `delta-8103-extract`).
- `delta_8103_corpus.csv` — 3 015 lignes + en-tête, SHA-256
  `fa012d2dd57a7d7fc8f14ccbe3a38d45fdc741a80fce1c45711af5a9ebfa16a3` ;
  `delta_8103_corpus.partial.csv` — partiel incrémental (reprise après
  redémarrage machine).
- `v62_delta_8103_analyse.py` — tests B1/B3 (SHA-256
  `98f76ce77ee63715797ae22b406fd52aa1a5834229a12da4ee8a3f7a5543dc4b` ;
  log `v62_delta_8103_analyse.log`).
- `delta_8103_results.json` — résultats B1/B3/B4 + extraction, SHA-256
  `6a672d7ebdd168542df85dd4b9de10303129a01372e95bedd4bfca50eebb8e59`.
- `v62_delta_8103_b2.py` (SHA-256
  `f32755204f028bf28f8902305c604a605fe099c70eef7be3cd522184a659a53d`),
  `v62_delta_8103_b2_detail.py` (SHA-256
  `47bdb347c9eaf17ac05c1992d3b5c0a4de8618ea96681dca3fdabbed0af2c2d5`)
  — B2 (logs `v62_delta_8103_b2.log`) ; sorties `delta_8103_b2.json`
  (SHA-256
  `58fa8c1a1a281a6fb54c9d1f1692c193843269035beeec451c2db81a1c6cb90a`),
  `delta_8103_b2_detail.json` (SHA-256
  `a186fa47baddbb6d1fd20100c8ec43e8899049cc3eb20ae0d4e8f6b637f616f6`).
- `v62_delta_8103_b4.py` (SHA-256
  `0c776cd30fb8f1a2b293791acd765a777ea5eeb5bf0721e92c033dd92d368bb6`),
  `v62_delta_8103_b4par.py` (SHA-256
  `a7b8a01e7153ebcc9158edce78de34aa0a2d5ac5339e09562e284330bbb5a4f3`),
  `v62_delta_8103_b4_analyse.py` (SHA-256
  `9ceab5a0e2b102cf4421076f71595996144e0f61960ec8053350ee66a7d5fdf1`)
  — B4 (lanceur `run_delta_8103_b4.sh`, SHA-256
  `8d588b4efdae4bfb190dcc3b4e1ba3edfe35163c3c07059d839e2a2ad4f38d5d`,
  gardien `watch_8103_b4a.sh`, SHA-256
  `d82809cba2b715b3b2cbc49daf2730d7fb072575d3868f09afa25e2ce40e9e36`,
  unités `delta-8103-b4` / `delta-8103-b4-watch`) ; sorties
  `delta_8103_b4.json` (SHA-256
  `4abcf9ed3c920b993941c8ce09907f0cffaf66b9a8cfecf4169c4f6595461148`),
  `delta_8103_b4_analyse.json` (SHA-256
  `0c978fab9fad23f5cc89208dfcc81aa51528a158acdddfa02c28df78c3bb7182`),
  `delta_8103_b4_table.csv` (SHA-256
  `31e3cbf5b62a8d2231c7aba5afe1179544517691ff489f9e6e1ccb55d0c9bf02`) ;
  121 partiels `delta_8103_b4_parts/*.json` (121/121) ;
  CSV nuls régénérés `delta_8103_nulls_tcga/pdac_tcga_fluxes_v4_nul_s*.csv`
  (graines 9101–9110) : s9101
  `22f39bf7…e8fa`, s9102 `5cad403a…dbeb`, s9103 `4854f45a…ab37`,
  s9104 `d9a98a13…7947`, s9105 `d55a9f60…f3f0`, s9106 `200f758d…e301`,
  s9107 `f8f247a9…27f6`, s9108 `477c789a…d2246e9`, s9109
  `732ac069…7b79`, s9110 `74d6d15a…d2c2`.
- Section : `section_8.103_delta_elucidation.md`, SHA-256
  `ce8f20df08ee5c5d025f4823cb373da939bf6f21524ef2d9b7259dac221ef38d`
  (426 lignes). Ce fichier-ci : `PROVENANCE_8103.md`, SHA-256 à
  noter après la dernière écriture (voir ci-dessous).

## 4. Incidents et reprises

- Redémarrage machine le 27 nov. ~15h04 UTC : première passe
  d'extraction tuée à 1 000/3 015 (travail en mémoire perdu, aucun CSV
  écrit) ; reprise par le partiel incrémental, 3 015/3 015 à 15h11 UTC.
- Calibration B4 : première passe tuée par `timeout 280` pendant le
  build s9102 (résultats de calibration non sauvegardés — sauvegarde
  ajoutée après chaque entrée) ; reprise complète, 4/4 OK.
- Durées de build réplique (calibration) : réel 112,2 s puis 120,6 s ;
  s9101 115,9 s ; s9102 122,1 s ; s9103 118,2 s — moyenne ≈ 117 s >
  90 s : règle d'arrêt du protocole déclenchée, B4a = réel + 10 nuls
  (graines 9101–9110) × 11 w = 121 builds.

## 5. Ce qui n'a pas été fait

- Aucune fusion dans le livre blanc, aucun PDF, aucun push GitHub,
  aucune Release. Rien touché dans `tlogNext-pdac-phase2`,
  `universal-log-research`, ni Kaggle. Aucun run du pipeline.
- Phase B4b : déclencheur gelé atteint (plus grand pas Delta(w) 2,51
  > 0,10 sur le réel), extension NON lancée — décision consignée
  §8.103.6 : le critère (i) tranche déjà le verdict (conjonction
  (i) ET (ii) ET (iii)) et (ii)/(iii) passent déjà sur B4a
  (10/10 et 113/121) ; l'extension (200 nuls × 3–4 w, ≈ 800 builds,
  ≈ 19 h estimées) ne peut pas changer le verdict. Script prêt
  (`v62_delta_8103_b4.py --b4b`, grille {40, 50, 60, 80}).
- Pipeline v6.2 vérifié une dernière fois après tous les lots :
  SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  — inchangé.
- Ce fichier (PROVENANCE_8103.md) : son SHA-256 final est relevé
  dans le rapport de fin de chantier remis au coordinateur (le
  fichier ne peut pas contenir son propre hachage).
