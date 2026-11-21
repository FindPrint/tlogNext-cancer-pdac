# PROTOCOLE GELÉ — Suppléments Chen non téléchargés (§8.89)

Date : 21 novembre 2026, ~10h15 EST. Chantier : §8.89 (PISTE 3 du lot
du 21 nov. 2026). Agent : TagPrint (subagent).
Feu vert de Zackary : 21 nov. 2026, 10h07.
Ce protocole est gelé AVANT tout téléchargement nouveau, AVANT toute
copie et AVANT tout calcul. Aucun paramètre ne change après les
résultats. Le livre blanc N'EST PAS édité, le PDF N'EST PAS régénéré,
rien n'est poussé sur GitHub dans ce chantier (convention des
chantiers ; fusion par le coordinateur). La section §8.89 est écrite
dans un FICHIER SÉPARÉ (`section_8.89_chen_supplements.md`).
Fichiers de travail : `~/workspace/runs/pdac-v6/chen889_scratch/`
(jamais /tmp). Ne pas toucher FindPrint/tlogNext-pdac-phase2.

## 0. Question

Le §8.84 a montré que drogue × KRAS (D3) et drogue × MTAP (D4) sont
IMPOSSIBLES dans les 12 Supplementary Data et la Source Data
examinés (MOESM3–MOESM15, MOESM17) : aucune table par-PDO. Mais
trois fichiers de l'article n'ont JAMAIS été téléchargés (MOESM1,
MOESM2, MOESM16), et les dépôts cités dans « Data availability »
n'ont jamais été consultés. **Question : une table par-PDO
(KRAS, MTAP, ou toute variable par organoïde) existe-t-elle dans
l'un de ces fichiers ou dépôts restants, qui rendrait D3/D4
courables sur la matrice 46 PDO × 63 AUC du §8.84 ?**

Antériorité reprise telle quelle (jamais recalculée) : §8.84 —
paire exploratoire CONFIRME consolidée (d_maxsep +0,0982, 3/3 nuls
> 0,07) ; D1 : 2 hits FDR < 0,05 (paclitaxel rho +0,5085,
FDR 0,0191 ; mitomycine C rho +0,4759, FDR 0,0257) ; D2a Olaparib /
BRCA2 répliqué p = 0,00015 ; D2c 5/5 correcteurs CFTR répliqués ;
D3/D4 IMPOSSIBLES dans MOESM3–MOESM15 + MOESM17.

## 1. Inventaire exhaustif des suppléments Chen (établi AVANT ce gel)

Source de l'inventaire : page de l'article relue le 21 nov. 2026
(`chen884_scratch/article.html`, 734 178 o, SHA
`b9ee6c7e6b47a8079c72c02ebb34cd6c9ecc17f565b0b23a47b13a4a393f4f4d`)
+ description des suppléments MOESM3 (détenue) + PROVENANCE_884.
La page de l'article liste exactement MOESM1 à MOESM17 (17 fichiers,
aucun MOESM18 dans le HTML — l'absence de MOESM18 sera confirmée
par une requête HEAD après ce gel, §3.5).

| Fichier | Nom Springer | Contenu attendu | Statut avant ce chantier |
|---|---|---|---|
| MOESM1 | `41467_2025_57520_MOESM1_ESM.pdf` | Supplementary Information : Supplementary Figures + Supplementary Tables (Tables 1, 2, 4 citées dans le texte) | NON TÉLÉCHARGÉ |
| MOESM2 | `41467_2025_57520_MOESM2_ESM.pdf` | Peer Review File | NON TÉLÉCHARGÉ |
| MOESM3 | `41467_2025_57520_MOESM3_ESM.pdf` | Description of Additional Supplementary Files | DÉJÀ DÉTENU, 140 637 o, SHA `3a84243b…5313c569` |
| MOESM4 | Data 1 (xlsx) | Cohortes 1 123 patients (clinique), IDs GN | DÉJÀ DÉTENU + EXAMINÉ §8.84 : 0 DAC, 0 KRAS, 0 MTAP |
| MOESM5 | Data 2 (xlsx) | SNP contrôles sains | DÉJÀ DÉTENU + EXAMINÉ : 0 partout |
| MOESM6 | Data 3 (xlsx) | Variants germinaux délétères, découverte | DÉJÀ DÉTENU + EXAMINÉ : 0 vrai DAC, 0 KRAS, 1 MTAP germinal (VUS_D p.P41L, patient EN233 — pas un PDO) |
| MOESM7 | Data 4 (xlsx) | Liste des 150 CSG | DÉJÀ DÉTENU + EXAMINÉ : KRAS/MTAP simples entrées de liste |
| MOESM8 | Data 5 (xlsx) | Variants germinaux, validation | DÉJÀ DÉTENU + EXAMINÉ : 0 vrai DAC, MTAP en liste seulement |
| MOESM9 | Data 6 (xlsx) | Fréquences BRCA2 | DÉJÀ DÉTENU + EXAMINÉ : 0 partout |
| MOESM10 | Data 7 (xlsx) | Sites de mutation CFTR | DÉJÀ DÉTENU + EXAMINÉ : 0 partout |
| MOESM11 | Data 8 (xlsx) | (CFTR) | DÉJÀ DÉTENU + EXAMINÉ : 0 partout |
| MOESM12 | Data 9 (xlsx) | (CFTR) | DÉJÀ DÉTENU + EXAMINÉ : 0 partout |
| MOESM13 | Data 10 (xlsx) | Écran de drogues, 63 × 46 AUC | DÉJÀ DÉTENU (`data/Chen2025_MOESM13_SupplData10.xlsx`), 35 732 o, SHA `0e009cd5…5340` |
| MOESM14 | Data 11 (xlsx) | Amorces CFTR | DÉJÀ DÉTENU + EXAMINÉ : 0 partout |
| MOESM15 | Data 12 (xlsx) | Métabolites | DÉJÀ DÉTENU + EXAMINÉ : 0 partout |
| MOESM16 | `41467_2025_57520_MOESM16_ESM.pdf` | Nature Portfolio Reporting Summary | NON TÉLÉCHARGÉ |
| MOESM17 | Source Data (xlsx) | Source Data Fig. 1–6 | DÉJÀ DÉTENU + EXAMINÉ §8.84 : Fig. 6b Z-scores AUC seulement, Fig. 6e statut CFTR des 15 PDO, aucune ligne KRAS/MTAP ; Fig. 1 oncoprint sans identifiant DAC |

Faits établis avant ce gel (lecture de `article.html` détenu,
21 nov. 2026) : « MTAP » apparaît 0 fois dans tout le texte de
l'article ; « G12C » 6 fois (un seul organoïde KRAS p.G12C nommé,
sans identifiant DAC) ; « Supplementary Table » 7 fois (Tables 1,
2, 4 citées) ; « Data availability » cite GSA-Human HRA005195 et
HRA010277, Metabolomics Workbench ST003734, Code Ocean 1432248.

## 2. Dépôts cités dans « Data availability » (à consulter, pas à télécharger en bloc)

| Dépôt | Accession | Contenu déclaré | Statut attendu / règle |
|---|---|---|---|
| GSA-Human (NGDC) | HRA005195 | Séquences brutes WGS/WES/RNA-seq cohorte découverte + WGS cohorte de validation fonctionnelle (69 organoïdes) | ACCÈS CONTRÔLÉ (données humaines) : consultation des pages publiques de métadonnées seulement ; AUCUNE demande d'accès, AUCUN compte créé, AUCUN téléchargement de lectures brutes dans ce chantier — un accès contrôlé est un blocage à nommer, pas à contourner |
| GSA-Human (NGDC) | HRA010277 | RNA-seq et ATAC-seq des organoïdes + RNA-seq des lignées | Idem : métadonnées publiques seulement |
| Metabolomics Workbench | ST003734 | Données brutes et matrices lipidomiques | Dépôt ouvert en principe : page d'étude + liste de fichiers consultées ; toute table d'échantillons par organoïde serait relevée, mais la lipidomique ne porte pas de génotype KRAS/MTAP |
| Code Ocean | 1432248 (DOI 10.24433/CO.1432248.v1) | Code original, licence MIT | Code seulement : description de la capsule consultée, aucun génotype attendu |

## 3. Méthode (après le gel)

### 3.1 Vérification des fichiers déjà détenus (sans re-téléchargement)
Re-hachage (SHA-256 + taille) de MOESM3–MOESM15 et MOESM17 dans
`chen884_scratch/` et de MOESM13 dans `data/` ; conformité aux
empreintes PROVENANCE_884 exigée. Tout écart = arrêt et diagnostic,
pas de substitution silencieuse.

### 3.2 Téléchargements nouveaux (exécution directe, JAMAIS systemd-run sans proxy)
Leçon AGENTS.md 2026-11-17 / PROVENANCE_879 §1.2 : les unités
systemd-run n'héritent pas du proxy d'egress — téléchargements en
exécution directe (curl), dans `chen889_scratch/`, URLs motif
Springer `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-57520-3/MediaObjects/41467_2025_57520_MOESM{n}_ESM.{pdf,xlsx}` :
MOESM1, MOESM2, MOESM16. Chaque fichier : SHA-256 + taille
consignés immédiatement. Aucun re-téléchargement des fichiers
déjà détenus et vérifiés (§3.1).

### 3.3 Examen de chaque fichier nouveau
Recherche exacte (insensible à la casse, texte extrait) de `DAC`,
`KRAS`, `MTAP`, `CDKN2A`, `9p21`, `G12C`, `organoid` dans chaque
fichier ; lecture intégrale des Supplementary Tables de MOESM1
(chaque table : titre, dimensions, colonnes, présence/absence
d'identifiants DAC et de variables par organoïde). Chaque fichier
est documenté même si négatif (nom, SHA, taille, contenu résumé).
Les faux positifs de recherche (ex. « HDAC » pour DAC) sont
nommés comme tels, comme au §8.84.

### 3.4 Dépôts
Pages publiques consultées (GSA-Human HRA005195 / HRA010277,
Metabolomics Workbench ST003734, Code Ocean 1432248) : statut
d'accès, liste des échantillons/fichiers si publique, présence ou
absence d'une table par organoïde téléchargeable sans authentification.
Aucune demande d'accès, aucun compte, aucun téléchargement de
données brutes contrôlées.

### 3.5 Confirmation d'exhaustivité
Requête HEAD sur MOESM18 (`..._MOESM18_ESM.pdf` et `.xlsx`) :
404 attendu — confirme que MOESM1–MOESM17 est la liste complète.
Si MOESM18 existait, il serait téléchargé et examiné comme les
autres, et le protocole serait amendé par addendum daté (pas de
changement silencieux).

## 4. Critère de recevabilité d'une table par-PDO (gelé, repris du §8.84 §4)

Une table est RECEVABLE si elle donne, pour **≥ 40 des 46 PDO
criblés**, mappés par identifiant DAC exact, sans ambiguïté, sans
imputation :
- le statut KRAS (mutant / sauvage, allèle si disponible), et/ou
- le statut MTAP (délétion / intact, ou nombre de copies 9p21).
Toute AUTRE table par organoïde (toute variable par PDO : clinique,
histologique, expression, nombre de copies, statut d'un autre gène)
est aussi relevée et documentée — elle ne rend D3/D4 courables que
si elle porte KRAS ou MTAP, mais une table par-PDO d'une autre
variable serait rapportée comme telle avec le test qu'elle
permettrait. Une table portant sur les 69 organoïdes dont < 40 des
46 criblés sont identifiables = NON RECEVABLE (raison nommée).
Une variante germinale isolée (ex. MTAP p.P41L du §8.84) n'est PAS
un statut MTAP par PDO. Un statut nommé dans le texte sans
identifiant DAC (ex. l'organoïde G12C) n'est PAS une table.

## 5. Tests directs SI une table recevable est trouvée (gelés)

Script neuf `direct_tests_889_chen.py`, sur les AUC MOESM13 telles
que publiées (même matrice que §8.84), jointes à la table par DAC.
Sens des AUC : **AUC basse = sensible**. Tous les p bilatéraux.
Correction FDR = Benjamini-Hochberg. Vérification indépendante par
second calcul (script `verify_889_direct.py`, accord exigé à 1e-9
près sur rho, U identiques, comptes FDR à l'unité près).

- **T1 — D3 drogue × KRAS.** Mann-Whitney bilatéral par drogue,
  KRAS-mutant contre KRAS-sauvage, 63 drogues, FDR BH sur 63.
  **Hit : FDR < 0,05.** Focus pré-enregistré, rapporté même si NS :
  MRTX849 et AMG510 (inhibiteurs KRAS G12C ; p brutes citées).
  Si l'allèle G12C est connu : sous-test descriptif G12C contre
  reste, aucun hit déclaré si n_G12C < 5 (effectif nommé).
- **T2 — D4 drogue × MTAP.** Même structure que T1, groupes
  MTAP-délété contre intact, 63 drogues, FDR BH sur 63.
  **Hit : FDR < 0,05.** Focus pré-enregistré : inhibiteurs PRMT5 /
  MAT2A / vopimetostat — absents des 63 (vérifié §8.84 §2.1) :
  l'absence est constatée, aucun test sur eux n'est possible.
- **T3 — Les 2 hits D1 survivent-ils quand on fixe KRAS / MTAP ?**
  Pour paclitaxel et mitomycine C (hits §8.84 : rho +0,5085 /
  +0,4759) : (a) Spearman (AUC drogue, AUC Gemcitabine) DANS chaque
  strate KRAS-mutant et KRAS-sauvage séparément (et MTAP-délété /
  intact si la table MTAP existe), p brutes rapportées, effectifs
  nommés ; (b) Spearman partiel contrôlant le statut KRAS (binaire)
  et, si disponible, MTAP (binaire) — rho partiel et p rapportés.
  Lecture gelée : les hits sont dits « survivre » si le rho reste
  > 0 et p < 0,05 dans les deux strates KRAS (ou, à défaut
  d'effectif, si le rho partiel reste > 0,35 avec p < 0,05) ;
  sinon ils sont dits « non séparables de l'effet KRAS/MTAP »
  ou « non testables par strate » (effectif nommé). Aucun seuil
  n'est ajusté après lecture des chiffres.
- **T4 — Descriptif G12C.** Si l'organoïde KRAS G12C est identifié
  par DAC : rangs d'AUC AMG510 et MRTX849 de ce PDO parmi les 46,
  rapportés descriptivement, jamais un hit (n = 1).
- Si la table trouvée est d'une AUTRE variable par PDO (ni KRAS ni
  MTAP) : un seul test analogue (Mann-Whitney par drogue, FDR BH
  sur 63) est couru sur cette variable, rapporté comme test
  exploratoire de cette variable, sans toucher aux verdicts D3/D4
  (qui restent impossibles pour KRAS/MTAP).

## 6. Critère de verdict du §8.89 (gelé)

- **TABLE TROUVÉE (KRAS et/ou MTAP recevable)** : T1/T2/T3 courus ;
  verdict du §8.89 = les résultats T1–T3 (hits FDR ou NON), avec
  l'effet sur les 2 hits D1 (T3) dit explicitement. La paire
  pipeline §8.84 n'est PAS recalculée (elle ne dépend pas de la
  table) ; A2 inchangé (paire Chen hors compte, exploratoire).
- **TABLE TROUVÉE (autre variable seulement)** : test analogue
  couru et rapporté ; D3/D4 restent IMPOSSIBLES pour KRAS/MTAP.
- **AUCUNE TABLE PAR-PDO** : verdict = **PISTE FERMÉE** — D3/D4
  restent impossibles, avec la liste exhaustive des suppléments
  vérifiés (nom, SHA, taille, contenu résumé) et le statut des
  dépôts. Ce n'est pas un échec caché : c'est la clôture mesurée
  de la piste ouverte au §8.84 §8.84.7(a).
- **BLOCAGE** (portail mort, paywall, fichier introuvable, accès
  contrôlé) : nommé tel quel avec la source tentée et le code
  d'erreur — jamais inventé, jamais contourné.

## 7. Règles du projet rappelées

- Provenance toujours nommée : source, URL, SHA-256, taille,
  statut de chaque fichier ; nature des lignes (mesure publiée vs
  échantillon hypothétique) dite explicitement.
- Aucun verdict d'une autre expérience n'est importé : seuls les
  chiffres mesurés sur les données et calculs du présent chantier
  font le verdict ; les p de l'article sont des résultats rapportés,
  re-mesurés ici quand ils sont testés (T1–T3).
- Un nul qui invalide une piste est un résultat ; une piste fermée
  faute de table est un verdict, pas un échec caché.
- Aucune affirmation clinique — écrans ex vivo, pas un traitement.
- Ne jamais présenter la paire Chen (n = 46, hors A2) comme une
  paire principale.

## 8. Livrables

- Ce protocole gelé (`PROTOCOL_chen_supplements_889.md`, SHA à
  noter après écriture).
- `PROVENANCE_889.md` (chaque fichier : source, URL, SHA-256,
  taille, statut ; statut des dépôts).
- `chen889_scratch/` : MOESM1, MOESM2, MOESM16 téléchargés
  (SHA consignés), sorties d'examen.
- Si table trouvée : `direct_tests_889_chen.py` + sorties,
  `verify_889_direct.py` + sortie de vérification.
- §8.89 dans le FICHIER SÉPARÉ
  `section_8.89_chen_supplements.md` (verdict d'abord, une phrase ;
  chiffres ensuite ; détail complet après ; liste exhaustive des
  suppléments vérifiés).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin du protocole gelé §8.89. —
