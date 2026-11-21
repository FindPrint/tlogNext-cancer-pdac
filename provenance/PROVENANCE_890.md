# Provenance — Audit complet §8.90 (21 novembre 2026)

Audit en lecture seule des §8.1–§8.89 du livre blanc PDAC. Aucun run de
pipeline lancé, aucun fichier de résultats modifié. Les chiffres clés ont
été recomptés depuis les fichiers cités par chaque section ; le code v6.2
a été relu (lignes 3333 et 10095).

## 1. Rapports d'audit (sources de §8.90)

- `audit_890/volet1_podcast_mc.md` (SHA `c5d90180…c22100`) — le podcast,
  MC contre `maxsep`, corrections de Zackary 11h00 / 11h01 / 11h03.
- `audit_890/volet2_verdicts.md` (SHA `a5025999…5913013e`) — relecture
  des verdicts, 9 chiffres clés, 8 incohérences I-1 à I-8, classement
  6 SOLIDE / 9 FRAGILE / 6 NON PROUVÉ / FERMÉ.
- `audit_890/volet3_securite.md` (SHA `37c72a69…5be`) — sécurité médicale,
  avertissement absent, 0 recommandation directe, faits cliniques F1–F7,
  8 reformulations R1–R8, addendum §3.2.
- `audit_890/volet4_universalite.md` (SHA `e7911335…a32`) — universalité,
  32 systèmes, tableaux de séparation, 16 limites, listes peut / ne peut
  pas, redéfinition en une phrase.

SHA complets (mesurés par `sha256sum` le 21 nov. 2026) :

- volet 1 : `c5d90180992c93d5018bc7b1bf9b33ecd21d8fca6e7f2cd0d266266dc4c22100`
- volet 2 : `a50259994611e238ce8353c14a580b3525836d45367f6bbce55f54c5913013e1`
- volet 3 : `37c72a693c27a79883f11221640a3d737dcfd1576d392cd4dfc4bfea4b1050be`
- volet 4 : `e7911335070ba1d219100acb4decf1844b5712587ddbd1270efb882d79e07a32`

## 2. Section §8.90

- `section_8.90_audit_complet.md` (443 lignes, SHA
  `40de98b9647d77a4994cae4c25c2e5c2047eccb85a81a4eb5cd435658a7bc9b9`,
  mesuré avant fusion ; SHA à re-mesurer après fusion dans le journal).

## 3. Code vérifié (non modifié)

- `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (conforme au SHA v6.2 du livre blanc) : ligne 3333
  (`max_separation`, dans `evaluate_scan_quality`, retourne aussi
  `s_norm`, `stability`, `robustness`, `sharpness`) et ligne 10095
  (`def compare_monte_carlo_regimes`, appelée L10486, résultat retourné
  L10536 `"mc": mc`). Les deux sont calculés dans le même run ;
  l'adoption de `maxsep` n'a changé que l'ordre d'affichage, pas de v6.5.
- v6 SHA `bb8bbdba…c0773`, v6.1 SHA `2af5e5ce…c1c9` : inchangés.

## 4. Fichiers de résultats cités par l'audit (déjà détenus, non modifiés)

`v61_phase2_table.json`, `sep_maxsep_856_table.json`,
`mtap_consolidation_850_extract.json`, `extract_872.json`,
`ssep_841_rotations.json`, `ssep_844_rotations.json`,
`extract_879_c3.json`, `extract_884.json`, `extract_885.json`,
`extract_887.json`, `extract_888.json`, `dist_887.json`,
`direct_tests_884_chen.json`, `survival_privilege_883_results.json`,
`mtap_consolidation_850_results.csv`, `data/prmt5_mtap_results.csv`,
`chen889_scratch/examine_889.json`,
`results_fast_tcga_v4/master_results.json`.

## 5. Corrections appliquées par addendum daté dans ce lot

- I-1 : PROVENANCE_889 §7, SHA `examine_889.json` corrigé en
  `0f828245…aadadb0` (vérifié par `sha256sum` :
  `0f828245cfad1a2b996c61886aef2f54557e1576035f684668890e9e3aadadb0`).
- I-2 à I-8 : addenda au §8.50.2 / §8.51 / §8.55.9 / §8.83 / §8.87 et
  aux lignes §7 209, 210, 242, 243 (texte d'origine intact).
- Volet 3, addendum §3.2 points 2–4 : §8.80 §0 (ventilation),
  §8.20 (indication FDA), §8.80 §4.2 (NCCN).
- R1–R5, R7 : addenda datés aux endroits concernés ; R6/R8 : appliqués
  par la formulation de l'entrée de journal de fusion du §8.90.
- Correction de Zackary (21 nov. 2026, 11h00) : `maxsep` score principal
  AFFICHÉ, pas le verdict ; le verdict, c'est la batterie entière.
- Avertissement médical renforcé : texte au §8.90.3.4 ; sa mise en tête
  du document est une DETTE pour la prochaine révision du gabarit.

## 6. Données

Aucune donnée nouvelle dans ce lot — relecture des §8.1–§8.89 et des
fichiers de résultats déjà détenus. DATA_SOURCES.md inchangée (aucune
source nouvelle).

## 7. Fichiers produits par ce chantier (à hasher après écriture)

- `~/workspace/runs/pdac-v6/section_8.90_audit_complet.md`
- `~/workspace/runs/pdac-v6/PROVENANCE_890.md` (ce fichier)
- `~/workspace/push_v62_890_build/fuse_890.py`
- `~/workspace/push_v62_890_build/build_snapshot_890.py`
- `~/workspace/push_v62_890_build/build_suite_890.py`
- `~/workspace/push_v62_890_build/pdf_build_890.sh`
- `~/workspace/push_v62_890_build/update_cover_890.py`
- `~/workspace/push_v62_890_build/add_journal_890.py`
- `~/workspace/push_v62_890_build/fetch_remote_890.py`
- `~/workspace/push_v62_890_build/verify_remote_890.py`
- `~/workspace/push_v62_890_build/verify_remote_suite_890.py`
- Aucun run pipeline ; livre blanc édité par addenda datés uniquement ;
  rien poussé par ce script.
