# VERSION_STATUS.md — Statut des versions du pipeline UNIVERSAL_LOG

28 novembre 2026 — publié à la racine du dépôt `FindPrint/tlogNext-cancer-pdac`
avec §8.101/§8.102/§8.103 (corrections de l'audit externe du 27 nov. 2026).

## Règle de lecture

- **Version de travail** : la seule version utilisée pour les nouveaux runs.
- **Version de référence** : la version antérieure, conservée intacte pour
  reproduire les résultats historiques.
- **Version rejetée** : testée, jugée insuffisante selon des critères gelés,
  ne jamais utiliser pour un nouveau run. Le code reste dans l'arbre pour
  la traçabilité, avec la section du livre blanc qui motive le rejet.
- **Version historique** : conservée intacte, ne plus utiliser.
- Le code d'origine n'est JAMAIS modifié : toute évolution passe par une
  copie, vérifiée par compilation, avec son SHA noté et l'original inchangé.

## Table des versions

| Version | Fichier | SHA-256 | Statut | Résultats |
|---|---|---|---|---|
| v5.9.0f (originale, fournie par Zackary) | `universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f_0_n0z8.py` | `4f80f6a7d0809e802cbc9ec30c0bed552c1c8a95eb58687fd78e4ffd8e808260` | Historique (ancêtre) | Lots v5, Ising, HP35 (premiers runs) |
| v6.0 | `universal_v6.0.0_cohen.py` | `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773` | Historique | cohen_d partout, Cliff supprimé ; référence historique |
| v6.1 | `universal_v6.1.0_cohen.py` | `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` | Référence (antérieure) | Gardes NaN L7a ; fast min_len 40 ; cascades identiques à v6 sur 41/41 runs |
| **v6.2** | **`universal_v6.2.0_cohen.py`** | **`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`** | **Version de travail — résultats publiés** | Graine L5 stable (SHA-256 du nom de métrique) ; déterministe (gigue 0, test à froid exact) ; tous les résultats §8.31 et suivants, lots §8.93/§8.98/§8.99/§8.101, §8.102, §8.103 |
| **v6.2.1** | `universal_v6.2.1_cohen.py` | `11a533e65e6bc41023c4c5e147232c426eea7f26bc2d1a9192b04ba27b035fd4` | Candidate (non adoptée — v6.2 reste la version de travail) | v6.2 + masque inf dans `compute_harmonic_mc_progress_axis` (audit externe 27 nov. 2026) ; non-régression 28 nov. 2026 : TCGA v4 réel + nul graine 42, scores de décision identiques à v6.2 à 0,0 exact (maxsep 0,46234232 / 0,16958013, MC 0,372047 / 0,326773, seuils 10,8696 / 81,5217) ; entrée inf synthétique (1 cellule MUC16 = inf) : scores identiques entre v6.2 et v6.2.1 (maxsep 0,46167456, MC 0,371953, Delta 4,19, exit 0), 5 feuilles NaN/inf identiques (diagnostics Q6) — le masque ne change rien d'observable sur ce test (défense en profondeur) |
| v6.3 | `universal_v6.3.0_cohen.py` | `552e735910a1fac183ad2ce5713ffa2888e9214c764b103707eeef1787044ffb` | REJETÉE (§8.49) | Recomposition MC ; ne pas utiliser |
| v6.4 | `universal_v6.4.0_cohen.py` | `9ed728da7168925f629258e671971d3e2724c35c812a60d9bd95f5fd8199ea3d` | REJETÉE (§8.52) | Recomposition MC par concentration de récurrence ; ne pas utiliser |
| v6.5 | `universal_v6.5.0_cohen.py` | `983ec65dc607a2ca8445bed095e5d86b3e6560534c7e7ecf9eda587fb6420bf6` | REJETÉE (§8.95) | Composite gelé (maxsep + MC + robustesse + L7a) ; comparable à maxsep seul (37/48) ; ne pas utiliser |

## Quelle version pour quel résultat

- Tous les résultats publiés depuis le §8.31 (novembre 2026) sont en **v6.2**,
  sauf mention explicite dans la section (v6.0/v6.1 pour les lots antérieurs,
  v6.3/v6.4/v6.5 uniquement dans leurs sections de rejet respectives).
- `maxsep` est le score principal **affiché** depuis le 20 novembre 2026
  (décision de Zackary, §8.64.12) : c'est une convention d'affichage, pas
  un changement de code et pas un verdict. MC reste calculé dans chaque run,
  avec toute la batterie (29 estimateurs, Q1–Q6, 4 tests de bruit, F1/F2
  avant/après seuil, L7a/L7b, falsification, Delta, maxsep).

## À ne pas confondre

- `UNIVERSAL_LOG_v6.0.1_control_flux_exclusion.py`, présent dans le dépôt
  `universal-log-research` (autre dépôt, autre IA), N'EST PAS plus récent
  que v6.2 : c'est un fork de v6.0.0 qui conserve la graine L5 salée
  `hash(metric)` (gigue ±~0,07). v6.2 reste la référence. Voir §8.100 et
  l'audit du 27 novembre 2026.
- Le présent dépôt est le dépôt unique du projet depuis la fusion du
  27 novembre 2026 (§8.100). Les anciens dépôts (`-suite`,
  `-pipeline-actions`, `-reproducibility`) sont archivés, jamais supprimés.
