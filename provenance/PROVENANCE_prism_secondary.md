# PROVENANCE — PRISM Repurposing Secondary Screen 19Q4, dose-réponse KRAS

## Source
- **Jeu :** PRISM Repurposing 19Q4 Dataset, Corsello et al., *Nat Cancer* 2020, 1:235–248, DOI 10.1038/s43018-019-0018-6.
- **Dépôt :** figshare, article **9393293**, DOI **10.6084/m9.figshare.9393293.v4**, publié 2019-12-17.
- **Accès :** le portail DepMap (`depmap.org/portal/download/all/?releasename=PRISM+Repurposing+19Q4`) renvoie une page de vérification Cloudflare Turnstile (vérifié 16 nov. 2026, 12h43 : le fichier téléchargé n'est que du HTML, 4 937 octets). Contournement : téléchargement direct via l'API figshare (`api.figshare.com/v2/articles/9393293`), mêmes fichiers, MD5 vérifiés. Journal des tentatives : `prism_secondary_access.log`.

## Fichiers téléchargés (tous dans `data/`, MD5 vérifiés exacts)
| Fichier | Taille (octets) | MD5 |
|---|---|---|
| `secondary-screen-dose-response-curve-parameters.csv` | 264 340 589 | `e629b9d505ad3d6bf65fde96f1c54bee` |
| `secondary-screen-cell-line-info.csv` | 40 979 | `6737b4aa9fd85404fd2f0cf825b037e4` |
| `secondary-screen-readme.txt` | 7 647 | `421d0bbadec381adc0d7981ee7e16bd7` |
| `secondary-screen-replicate-collapsed-treatment-info.csv` | 3 788 355 | `54765b3639f91cede751378d694e3583` |

## Contenu du fichier principal
- 701 004 lignes ; colonnes utilisées : `broad_id`, `depmap_id`, `screen_id`, `auc`, `ic50`, `name`, `moa`, `target`, `passed_str_profiling`.
- Écrans : HTS002 (602 495), MTS010 (64 203, redos techniques des 147 composés d'oncologie), MTS006 (33 472), MTS005 (834).
- 1 502 broad_id, 1 448 noms de composés, 480 lignées. AUC jamais manquante ; IC50 manquante sur 339 092 lignes (48 % — courbe n'atteignant jamais 50 % de viabilité).
- IC50 == 0 sur 14 lignes (log10 = −inf) : **aucune ne concerne une lignée pancréas** (vérifié) — sans effet sur ce criblage.
- Lignes sans `depmap_id` : 10 812 (barcodes contrôles) — ce sont aussi les seules lignes STR=False ; retirées, rien d'autre à écarter.
- Déduplication (broad_id, depmap_id) : 90 383 lignes en doublon entre écrans ; priorité MTS010 > HTS002 > MTS006 > MTS005 (le readme recommande MTS010 quand disponible). Après dédup : 644 798 lignes.
- Agrégation par nom de composé (54 noms ont 2 broad_id : médiane AUC et médiane log10 IC50).

## Axe KRAS et jointure
- Chronos KRAS : DepMap Public 24Q4, `CRISPRGeneEffect.csv` (428 678 699 octets, SHA `3d8f3ec6…`, déjà vérifié le 15 nov.).
- Lignées pancréas : `Model.csv`, `OncotreeLineage == Pancreas` (68 modèles).
- **33 lignées pancréas dans le secondaire PRISM, 29 communes avec Chronos KRAS** (min −4,14, médiane −1,83, max −0,36). Pour comparaison : le primaire 24Q2 en avait 38.

## Méthode (`prism_secondary_screen.py`, exit 0)
- Par composé (nom), n_auc ≥ 15 : Spearman AUC contre Chronos KRAS ; Spearman log10(IC50) contre Chronos KRAS quand n_ic50 ≥ 15. Sens : rho > 0 = les lignées KRAS-dépendantes sont plus sensibles (AUC/IC50 plus bas).
- Tertiles : `pd.qcut(kk, 3, labels=["fort", "moyen", "faible"])` — « fort » = Chronos le plus négatif = le plus dépendant. **Vérifié par assertion dans le script** (la lignée au Chronos minimum est étiquetée « fort » ; moyenne Chronos « fort » < « faible »). C'est le sens corrigé — dans `prism_screen.py` (15 nov.) les étiquettes étaient inversées.
- FDR Benjamini-Hochberg sur l'ensemble testé (AUC et IC50 séparément).
- Aucune imputation.

## Résultats (chiffres du criblage seul)
- **1 427 composés testés** (n_auc ≥ 15) ; 641 avec n_ic50 ≥ 15.
- **FDR AUC < 0,05 : 0. FDR IC50 < 0,05 : 0.** p AUC < 0,001 : 2/1 427 (attendu ~1,4 par hasard). Médiane rho AUC −0,013 ; 47,7 % des rho > 0 — symétrique autour de zéro.
- Meilleurs rho AUC : naloxone +0,679 (p=0,004, FDR 0,558, n=16), P22077 (USP7) +0,563 (FDR 0,558), estradiol +0,560, benzydamine +0,547, PF-04217903 (c-Met) +0,528 — tous FDR ≥ 0,42, sans effet de classe : curiosités, pas des candidats.
- Voie KRAS : MEK (18 composés) médiane rho +0,008 ; RAF (9) −0,056 ; groupe KRAS/MEK/ERK/RAF/SHP2/SOS1 (16) −0,059. Tramétinib +0,065, sélumétinib +0,043, cobimétinib +0,095, PD-0325901 −0,129, réfametinib −0,063 — rien.
- PARP (9 composés) médiane rho −0,080 — pas d'effet de classe (cohérent avec le primaire : +0,032).
- Direction négative la plus forte : pepstatin −0,668, uprosertib (AKT) −0,625, buparlisib (PI3K) −0,605 — FDR 0,42–0,50, non significatifs ; classes PI3K/AKT/mTOR médianes −0,065/−0,050/−0,054.
- **Composés ciblés KRAS absents du secondaire 19Q4** (vérifié sur les noms du fichier) : MRTX1133, RMC-6236, sotorasib (AMG-510), adagrasib (MRTX849), BI-3406, SHP099, TNO155, binimétinib, ulixertinib, SCH772984, ERK_2440, ERK_6604, encorafenib. Le secondaire date de 2019 : ces inhibiteurs n'existaient pas encore ou n'étaient pas dans la bibliothèque.
- **Vérification indépendante :** rhos AUC recalculés à l'identique pour tramétinib (+0,065), cobimétinib (+0,095), sélumétinib (+0,043), naloxone (+0,679), P22077 (+0,563).

## Sorties
- `data/prism_secondary_kras_screen.csv` (1 427 composés ; SHA-256 `49f974103d787a181feb952e18b10b9f0f998300a32c7fa1c8ed165829e0e063`)
- `data/prism_secondary_kras_screen_moa.csv` (médianes par MOA ; SHA `c686fbf9922d058ad5871cfe02180cdeaeee26f2dde103991e5c5da89d846a6c`)
- `data/prism_secondary_kras_screen_targets.csv` (médianes par cible ; SHA `dc048c9e3017e5790bb2b88fb65a9cef915be7085a2d62ba3e1a3d12a9f3e12d`)
- `prism_secondary_screen.py`, `prism_secondary_screen.log`, `prism_secondary_screen_stdout.txt`, `prism_secondary_access.log`

## Limites
- Le secondaire 19Q4 est un sous-ensemble **sélectionné** du primaire (1 448 composés choisis pour activité/sélectivité) — pas un criblage neutre de toute la bibliothèque.
- 29 lignées pancréas seulement (contre 38 au primaire) : puissance limitée ; un effet faible pourrait être raté, mais aucun effet fort n'apparaît (FDR min 0,418).
- Les inhibiteurs KRAS directs de clinique ne sont pas testables dans cette base (absents, 2019).
- Ce criblage ne dit rien sur les combinaisons de médicaments ni sur les modèles in vivo.
