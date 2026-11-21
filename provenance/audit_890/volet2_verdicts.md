# Audit §8.90 — VOLET 2 : relecture de tous les verdicts (§8.1–§8.89)

**Nature du document :** lecture seule. Aucun fichier du livre blanc ni aucun fichier de résultats n'a été modifié ; aucun run de pipeline n'a été lancé. Ce rapport est le seul fichier écrit.

**Livre blanc audité :** `~/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md`
— SHA-256 `39d3abd65eda029efb959934ecdf17a10f14ba85b0b15f9c03c9e86fc8358696` (vérifié par `sha256sum` le 21 nov. 2026), 22 783 lignes, §8.1–§8.89.
PDF associé : 1310 p., SHA `9a04e93b37d55ccbdfc2eda995f7e2837d3adfc87579233367661346d4c65bfa` (cité dans l'entrée de journal, ligne 22781 du livre blanc ; le PDF lui-même n'a pas été relu ici, seulement le `.md`).
Pipeline : v6.2 SHA `f07567c4…` ; maxsep adopté pleinement par Zackary le 20 nov. 2026 13h04 comme score principal affiché, MC secondaire.

**Méthode :** chaque chiffre clé ci-dessous a été recalculé depuis le fichier de résultats (JSON d'extraction, CSV, script direct), pas seulement relu dans le texte. Les sections ont été relues pour (i) la cohérence verdict/limites, (ii) les contradictions entre sections, (iii) la présence des notes de correction datées. Les numéros de ligne cités sont ceux du livre blanc audité.

**Provenance des vérifications :** répertoire `~/workspace/runs/pdac-v6/` (extraits `extract_879_c3.json`, `extract_884.json`, `extract_885.json`, `extract_887.json`, `extract_888.json` ; `direct_tests_884_chen.json` ; `survival_privilege_883_results.json` ; `mtap_consolidation_850_results.csv` + `mtap_consolidation_850_extract.json` ; `data/prmt5_mtap_results.csv` ; `chen889_scratch/examine_889.json` ; `dist_887.json` ; `PROVENANCE_884.md`, `PROVENANCE_889.md`).

---

## 1. Tableau de vérification des chiffres clés

| # | Chiffre cité (section, §7 / résumé) | Chiffre revérifié (fichier source) | Source du fichier | Statut |
|---|---|---|---|---|
| (a) | §8.79 GSE57495 : d_maxsep **+0,4494** (réel 0,6381 contre nul 0,1887) ; A2 **9/13** (11/13 positifs), LOO **8/12** | 0,6381160120056911 − 0,1887249135434316 = **+0,4494** ; A2 recompté paire par paire depuis la table §8.88.3 (13 premières paires) : 9 passantes, 11 positives, LOO 8/12 | `extract_879_c3.json` (vérification 2/2 à 0,0 exact, `maxsep_879_c3_verify.json`) ; table §8.88.3, lignes 22035–22065 du livre blanc | **OK** |
| (b) | §8.85 GDC : d_maxsep **+0,0884** (réel 0,2542 contre nul 0,1658), marge 0,0184 ; A2 **10/14** (12/14 positifs), LOO **9/13** ; nuls frais s8851 **+0,0376** (sous le plancher), s8852 **+0,0936** | 0,2542142850 − 0,1657676707 = **+0,0884** ; s8851 : 0,2542142850 − 0,2165939226 = **+0,0376** ; s8852 : 0,2542142850 − 0,1605986015 = **+0,0936** ; A2 recompté depuis la table §8.88.3 (14 premières paires) : 10 passantes, 12 positives, LOO 9/13 | `extract_885.json` (vérification 4/4 à 0,0 exact, `maxsep_885_verify.json`) ; table §8.88.3 | **OK** |
| (c) | §8.84 Chen : d_maxsep **+0,0982** (réel 0,3478 contre nul 0,2496), **3/3 nuls au-dessus du plancher** (frais +0,1528 / +0,1607) ; **2 hits FDR < 0,05** : paclitaxel rho +0,5085, FDR 0,0191 ; mitomycine C rho +0,4759, FDR 0,0257 ; Olaparib/BRCA2 p = 0,00015 ; 5/5 correcteurs CFTR | 0,3477606744 − 0,2495638180 = **+0,0982** ; s8841 : 0,3477606744 − 0,1949927558 = **+0,1528** ; s8842 : 0,3477606744 − 0,1870370511 = **+0,1607** ; D1 : 2 hits, paclitaxel rho 0,5085425286, FDR 0,0190935334 ; mitomycine C rho 0,4758703632, FDR 0,0257301868 ; D2a Olaparib/BRCA2 p = 0,0001466069 (≈ 0,00015) ; D2c : 5/5 correcteurs CFTR, p 0,0015–0,0156, conformes à l'article (0,002–0,016) | `extract_884.json` (vérification 4/4 à 0,0 exact) ; `direct_tests_884_chen.json` (D1, D2a, D2c) | **OK** |
| (d) | §8.83 survie : **3 items sur 8** prédisent comme CA125 (Cox HR > 1, p < 0,05 dans ≥ 2/3 cohortes) — **TGFB2, HLA-G, score combiné** ; aucun gène ne monte avec KRAS dans ≥ 2/3 cohortes | Recompté cohorte par cohorte (Cox p < 0,05, HR > 1) : TGFB2 TCGA p=0,0139 ✓, ICGC p=0,0482 ✓, GSE71729 p=0,9135 ✗ → 2/3 ✓ ; HLA-G TCGA p=0,1149 ✗, ICGC p=0,0004 ✓, GSE71729 p=0,0349 ✓ → 2/3 ✓ ; SCORE TCGA p=0,0201 ✓, ICGC p=0,0013 ✓, GSE71729 p=0,5340 ✗ → 2/3 ✓ ; CD47 exclu (HR 0,76 en GSE71729, sens opposé) ✓ ; CD274 1/3 ; TGFB1 1/3. Montée avec KRAS : TGFB2 1/3 (TCGA rho +0,337), TGFB1 1/3, CD274 1/3, HLA-G 0/3 → **aucun ≥ 2/3 ✓** | `survival_privilege_883_results.json` (TCGA n=177, ICGC n=70, GSE71729 n=125) + `survival_privilege_883_results.txt` | **OK** (avec la nuance I-5 : TGFB2 monte avec KRAS en TCGA seule, rho +0,337, p < 0,0001 — le corps du §8.83 le dit, le titre ne le dit pas) |
| (e) | §8.50 MTAP : **10/10** nuls frais au-dessus du plancher 0,07, **13/13** avec les 3 anciens ; écarts min **+0,1110**, médiane **+0,1595**, max **+0,1981**, moyenne +0,1564 ; MC réel 0,3511 > 9/10 frais (médiane nulle 0,3288) | 10 frais : min **+0,1110**, médiane **+0,1595**, max **+0,1981**, moyenne **+0,1564** (recalculés) ; 13/13 au-dessus du plancher ✓ (le plus petit des 13 est +0,0715, nul S7) ; MC réel 0,3511385 > 9/10 frais, médiane MC des frais **0,3288** ✓ ; Delta réel 3,8051, 9/10 frais entre 3,8010 et 3,8482 ✓ | `mtap_consolidation_850_results.csv` (13 écarts) ; `mtap_consolidation_850_extract.json` (MC, Delta par run) | **OK, avec ambiguïté de périmètre (I-2)** : min/médiane/max/moyenne sont ceux des **10 frais seuls** ; sur les 13 nuls, min = +0,0715 et médiane = +0,1590. La phrase du §7 (ligne 209) ne le précise pas. |
| (f) | PRMT5 : pancréas **−1,385 vs −1,010, p = 0,0036** (MTAP-délétées n=20 contre intactes n=27) | Médianes −1,3849882483 vs −1,0098854303, U = 134, p = **0,0035512389** (≈ 0,0036) ; Spearman PRMT5–CN MTAP +0,497 (p=0,0004) confirmé au §8.40 (reproduction à l'identique) | `data/prmt5_mtap_results.csv` (ligne « pancréas profond », PRMT5) | **OK** |
| (g) | §8.87 consolidation GDC : **FRAGILE CONFIRMÉ**, d_médian **+0,0314**, rang **13/14**, **2/13** écarts au-dessus du plancher, réel sous le p95 des nuls ; A2 inchangé 10/14 | Médiane des 13 nuls 0,2228539322 ; 0,2542142850 − 0,2228539322 = **+0,0314** ; écarts > 0,07 : 2/13 (+0,0936 s8852, +0,0884 graine 42), 0/10 frais ; réel battu par 1 nul (s8880, 0,2689) ; p95 des nuls 0,2584172851, réel − p95 = −0,0042 ✓ ; A2 non recompté (règle gelée) ✓ | `extract_887.json` (14/14) ; `dist_887.json` (`d_median` 0,0313603528, `rang_reel_sur_14` 13, `nuls_battus_par_reel` 12) | **OK** (convention de rang à clarifier, I-8) |
| (h) | §8.88 GSE194249 à 11 flux : **NON**, 15e paire, d_maxsep **−0,0239** (réel 0,2306 contre nul 0,2545) ; A2 **10/15** (12/15 positifs), LOO **9/14** ; nuls frais +0,0517 / +0,0354 | 0,2306 − 0,2545 = **−0,0239** ; s8881 : 0,2306 − 0,1789 = **+0,0517** ; s8882 : 0,2306 − 0,1952 = **+0,0354** ; 0/3 au-dessus du plancher ✓ ; table §8.88.3 recomptée : 10 passantes (HP35, TCGA v4, ICGC, Imm TCGA, PARP TCGA, DepMap, GSE60979, GSE131050, GSE57495, GDC), 12 positives, LOO 9/14 ✓ | `extract_888.json` (4/4) ; table §8.88.3, lignes 22035–22065 du livre blanc | **OK** |
| (i) | §8.89 suppléments Chen : **PISTE FERMÉE** — aucune table par-PDO KRAS/MTAP dans les 17 suppléments ni les dépôts ; seule variable nouvelle : statut CFTR MT/WT Fig. 14c (38/46 couverts, MT n=4, en conflit avec la Fig. 6e) | `keyword_counts` : MTAP 0 mention dans MOESM1/2/16, 9p21 0, CDKN2A 0–1 ; KRAS 6/15/0 mentions, aucune table par-PDO ; `fig14c_overlap_screened` : 38/46 couverts ✓ ; `fig14c_MT` : n_MT = 4 ✓ ; `fig6e_MT_vs_fig14c` : DAC_24 et DAC_84 MT en Fig. 6e mais WT en Fig. 14c, DAC_30 et DAC_73 MT en Fig. 14c mais absents des 15 de la Fig. 6e ✓ (conflit confirmé) | `chen889_scratch/examine_889.json` ; `PROVENANCE_889.md` | **OK** |

**Bilan du §1 : 0 écart numérique sur les 9 chiffres vérifiés.** Tous les chiffres clés sont exacts à la 4e décimale près contre les fichiers de résultats. Les deux points à retenir sont une ambiguïté de périmètre (§8.50, I-2) et une nuance déjà écrite dans le corps du §8.83 mais absente de son titre (I-5).

---

## 2. Incohérences trouvées, avec corrections proposées

Règle suivie : texte d'origine intact, correction par addendum daté uniquement. Je propose, je ne corrige pas dans le livre blanc.

### I-1 — Coquille factuelle (la seule erreur de valeur trouvée) : SHA tronqué faux dans PROVENANCE_889 §7

- **Localisation exacte :** `~/workspace/runs/pdac-v6/PROVENANCE_889.md`, §7, ligne 236 : `` `examine_889.json` (SHA `0f828245…bef946`) ``.
- **Preuve :** `sha256sum chen889_scratch/examine_889.json` = `0f828245cfad1a2b996c61886aef2f54557e1576035f684668890e9e3aadadb0` (suffixe `…aadadb0`, pas `…bef946`). Le §4 de la même provenance donne le SHA complet correct (`0f828245cfad…aadadb0`), et le SHA complet cité au §40 de DATA_SOURCES.md est celui du fichier détenu. L'entrée de journal du livre blanc (ligne 22781) nomme déjà cette coquille ; je l'ai revérifiée indépendamment depuis le fichier.
- **Correction proposée (addendum daté, 21 nov. 2026) :** dans PROVENANCE_889 §7, remplacer `` `0f828245…bef946` `` par `` `0f828245…aadadb0` `` ; noter que le §4 de la même provenance et le §40 de DATA_SOURCES.md portaient déjà la bonne valeur. Aucun verdict n'est touché (le fichier `examine_889.json` lui-même est intact et conforme).

### I-2 — Ambiguïté de périmètre : les statistiques du §8.50 portent sur les 10 nuls frais, pas sur les 13

- **Localisation exacte :** livre blanc, §7 ligne 209 (row 56) : « écarts S_sep réel−nul min +0,1110, médiane +0,1595, max +0,1981 — 10/10 au-dessus du plancher 0,07, 13/13 avec les 3 nuls anciens » ; même formulation au §8.50.2 (« médiane +0,1595, Q3 +0,1718, max +0,1981, moyenne +0,1564 »).
- **Preuve :** recalculés depuis `mtap_consolidation_850_results.csv` : sur les 10 frais, min +0,1110 / médiane +0,1595 / Q3 +0,1718 / max +0,1981 / moyenne +0,1564 (tous exacts) ; sur les 13 nuls, min +0,0715 (nul S7) et médiane +0,1590. Un lecteur qui recalcule sur les 13 trouve deux valeurs différentes et conclut à tort à une erreur.
- **Correction proposée (addendum daté) :** ajouter « (10 nuls frais) » après « min +0,1110, médiane +0,1595, max +0,1981, moyenne +0,1564 » au §7 ligne 209 et au §8.50.2, et ajouter la ligne « sur les 13 nuls : min +0,0715, médiane +0,1590 ».

### I-3 — Incohérence de titre (la plus grave sur le fond) : le §7 et le titre du §8.51 affirment ce que le §8.54 révise

- **Localisation exacte :** livre blanc, §7 ligne 210 (row 57) : « **NON, la corrélation immunitaire n'est pas un artefact de composition** » ; titre du §8.51 (ligne 4866) : « la corrélation immunitaire n'est pas un artefact de composition ».
- **Preuve :** le §8.51 ne testait que les proxys de pureté internes (acineux/îlots) — son §8.51.8(b) le dit lui-même (« Cela ne dit pas que l'infiltration est innocentée : aucune infiltration INDÉPENDANTE n'a été testée ici »). Le §8.54 teste l'infiltration (score ESTIMATE calculé) et conclut H1 totale (effondrement 0,5563 → 0,2002, chute 64,0 %), et son §8.54.8(f) écrit noir sur blanc : « cela RÉVISE l'interprétation du §8.51.8 : la corrélation immunitaire n'est pas une "propriété propre aux tumeurs" — elle est largement un effet de composition (infiltration). » Ni le titre du §8.51 ni la ligne §7 ne portent de renvoi vers cette révision : lus seuls, ils affirment le contraire du verdict final du dossier.
- **Correction proposée (addendum daté au §8.51 et note au §7 ligne 210, texte d'origine intact) :** « Lecture révisée au §8.54.8(f) (21 nov. 2026) : le §8.51 ne portait que sur les proxys de pureté internes ; l'infiltration explique largement la corrélation (§8.54, H1 totale). Le titre et la ligne §7 doivent se lire "n'est pas un artefact de la pureté (proxys internes)", pas "n'est pas un artefact de composition". »

### I-4 — Réconciliation manquante : le « deux tiers propres » du §8.55 face au H1 totale du §8.54

- **Localisation exacte :** livre blanc, §8.55.9 : « La corrélation intra-famille immunitaire est portée pour environ un tiers par la pureté tumorale (ABSOLUTE) et pour environ deux tiers par une co-expression propre aux tumeurs. »
- **Preuve :** le §8.54.8 conclut H1 totale (infiltration explique la corrélation, résidu +0,1982, soit ~36 % du brut 0,5563). Les deux régressions ne portent pas sur le même axe (pureté ADN ABSOLUTE, n=149, vs infiltration ARN ESTIMATE, n=178) et le §8.54.8(f) dit qu'il s'agit de « deux axes de composition différents », mais aucune phrase du livre blanc ne réconcilie les deux chiffres : le résidu « deux tiers propres » du §8.55 contient l'effet infiltration non retiré par ABSOLUTE. Le §8.55.9(b) (« Cela ne dit pas que l'infiltration est expliquée ») peut en outre se lire comme si l'infiltration n'avait pas été testée, alors que le §8.54 l'a testée.
- **Correction proposée (note datée d'une ligne, à ajouter au §8.55.9) :** « Les "deux tiers" ci-dessus sont le résidu après régression sur ABSOLUTE seule ; ils contiennent l'effet infiltration mesuré au §8.54 (résidu +0,1982 après régression ESTIMATE). Pureté et infiltration sont deux axes de composition différents (§8.54.8(f)) ; les deux chiffres ne s'additionnent pas. »

### I-5 — Titre plus fort que le corps : §8.83, « pas parce qu'ils montent avec KRAS »

- **Localisation exacte :** titre du §8.83 (ligne 19820) : « OUI, pour 3 items sur 8 — mais pas parce qu'ils montent avec KRAS » ; §7 ligne 242 (row 89) : « le signal de survie ne passe pas par KRAS ».
- **Preuve :** TGFB2, l'un des trois passants, monte avec KRAS en TCGA seule (rho +0,337, p < 0,0001 — `survival_privilege_883_results.json`), c'est-à-dire dans la cohorte où il prédit la survie (Cox p=0,0139). Le corps du §8.83 le dit explicitement (« C'est le seul des trois passants qui monte avec KRAS quelque part » ; « TGFB2 ne monte qu'en TCGA (rho +0,337) et est plat ailleurs »). La formulation exacte, vérifiée, est : « aucun gène ne monte avec KRAS dans ≥ 2/3 cohortes ».
- **Correction proposée (addendum daté au §8.83 et à la ligne §7 242) :** qualifier par « dans ≥ 2/3 cohortes » et nommer l'exception : « sauf TGFB2, qui monte avec KRAS en TCGA seule (rho +0,337) — son signal de survie en TCGA peut partiellement passer par KRAS ; HLA-G et le score combiné, eux, ne montent avec KRAS nulle part. »

### I-6 — Citation périmée : le §7 cite le SHA de PROVENANCE_884 antérieur à sa correction

- **Localisation exacte :** livre blanc, §7 ligne 243 (row 90, §8.84) : provenance `PROVENANCE_884.md`, SHA `1eb03395…ca43`.
- **Preuve :** ce SHA est celui de la version poussée à c696e173, antérieure à la correction des suffixes SHA MOESM5/7/8. Le fichier local corrigé est SHA `8a1ffcd3…` (entrée de journal, ligne 22781 : « PROVENANCE_884.md local (SHA `8a1ffcd3…`) diffère du distant à c696e173 (SHA `1eb03395…`) uniquement par les 3 suffixes MOESM5/7/8 corrigés »). Les suffixes corrigés sont vérifiés présents dans le fichier `PROVENANCE_884.md` (lignes 138–140 : MOESM5 `c759ab51…ef25eb`, MOESM7 `bf5cab3f…a194fe`, MOESM8 `9b440dd9…d5e389`).
- **Correction proposée (addendum daté) :** ajouter à la ligne §7 243 : « PROVENANCE_884.md local corrigé SHA `8a1ffcd3…` (suffixes MOESM5/7/8 corrigés le 21 nov. 2026 ; le SHA cité `1eb03395…ca43` est celui de la version poussée à c696e173, antérieure à la correction ; le fichier corrigé sera repris au prochain snapshot). »

### I-7 — Formulation imprécise dans le journal : les suffixes corrigés ne sont pas dans le corps du §8.84

- **Localisation exacte :** livre blanc, ligne 22781 (entrée de journal, fusion §8.87–§8.89) : « suffixes corrigés ef25eb / a194fe / d5e389 : présents, via le corps du §8.84 et l'annexe des provenances, PROVENANCE_884.md corrigée ».
- **Preuve :** par `grep` sur le livre blanc audité, les trois suffixes corrigés n'apparaissent que sur la ligne 22781 elle-même (l'entrée de journal qui les nomme) ; le corps du §8.84 ne reproduit pas la table SHA MOESM5/7/8. Ils sont en revanche présents dans le fichier `PROVENANCE_884.md` (lignes 138–140, vérifié). Leur présence dans le PDF dépend donc de l'annexe des provenances générée par `build_appendix.py`, pas du corps du §8.84. De même, les anciens suffixes (1eb46c / 2a1957 / 4f06e) n'apparaissent dans le `.md` que sur cette même ligne 22781 : l'affirmation « 0 occurrence » vaut pour le PDF régénéré avant l'ajout de l'entrée de journal, pas pour le fichier `.md` actuel.
- **Correction proposée (note datée) :** reformuler : « suffixes corrigés présents dans PROVENANCE_884.md (fichier, lignes 138–140) et repris dans l'annexe des provenances du PDF ; le corps du §8.84 ne les reproduit pas. Anciens suffixes : 0 occurrence dans le PDF ; 1 occurrence dans le fichier `.md` (la présente entrée de journal, qui les nomme comme anciennes valeurs). »

### I-8 — Clarification (pas une erreur) : le « rang 13/14 » du §8.87 est un rang ascendant

- **Localisation exacte :** livre blanc, §8.87, verdict d'abord : « le réel est battu par 1 nul sur 13 (s8880, 0,2689 — rang 13/14) ».
- **Preuve :** `dist_887.json` : `rang_reel_sur_14` = 13, `nuls_battus_par_reel` = 12 — le rang est compté en ordre croissant (13e sur 14 = 2e plus haut). Le texte l'explicite (« battu par 1 nul sur 13 »), mais un lecteur peut lire « 13e sur 14 » comme quasi-dernier.
- **Correction proposée (clarification d'une parenthèse) :** « rang 13/14 (ascendant : 2e plus haut, battu par 1 nul sur 13) ».

### Points vérifiés et jugés CONFORMES (pas d'incohérence)

- **§8.84 / §8.86 — corrections datées du 21 nov. 2026 présentes :** paragraphe « Correction datée (21 novembre 2026, après fusion) » présent à la ligne 20598 (§8.84 : A2 « 9/13, 11/13 positifs, LOO 8/12 » = état avant le §8.85, compte final 10/14, 12/14 positifs, LOO 9/13) et à la ligne 21389 (§8.86 : même correction + phrase périmée « la quatorzième paire n'a pas eu lieu »). Textes d'origine intacts. Le §7 ligne 245 (row 92, §8.86) porte déjà le compte corrigé (« A2 reste 10/14 »).
- **§8.70 contre §8.72 — note de correction datée présente :** addendum « ADDENDUM — 20 novembre 2026 (§8.72) : NOTE DATÉE DE CORRECTION — LECTURE RENVERSE » présent aux lignes 14363–14393, texte original intact, lecture corrigée (d_médian +0,1447, rang 14/14, 12/13 au-dessus du plancher), avec les garde-fous explicites : verdict graine 42 inchangé (PARTIEL +0,0567), A2 gelé 6/10 non recompté, C3 non levée par le §8.72 seul. Cohérent avec le §8.71 qui lève C3 (7/11) et avec le §7 ligne 231.
- **§8.59 / §8.64 contre §8.64.12 — distinction décision/preuve claire :** §8.64.12 (ligne 11012) : « Zackary adopte `maxsep` pleinement — décision, pas preuve nouvelle » ; « La confirmation indépendante devient une vérification a posteriori » ; le §8.69 (NON, d_maxsep −0,0100) « ne rouvre pas la décision et ne la conditionne pas ». La même formule est répétée aux §8.70, §8.71, §8.87 (« l'adoption pleine … n'est ni rouverte ni conditionnée ici »). Les échecs des portes D3/D4 au §8.59 restent consignés. Aucune section ne présente l'adoption comme une preuve.
- **§8.51 contre §8.54/§8.55 — qualification présente dans les corps de section :** §8.51.8(b) (infiltration non testée), §8.54.8(f) (révision explicite), §8.55.9 (tableau comparatif §8.51 vs §8.55). L'incohérence restante est seulement au niveau du titre et de la ligne §7 (I-3), pas dans les corps.
- **A2 final cohérent sur toute la chaîne :** 9/13 (§8.79) → 10/14 (§8.85) → 10/14 (§8.86, inchangé) → 10/14 (§8.87, inchangé) → 10/15 (§8.88), LOO 8/12 → 9/13 → 9/14 ; positifs 11/13 → 12/14 → 12/15. Recompté paire par paire depuis la table §8.88.3 (15 paires, valeurs reprises telles quelles des sections sources). Les exclusions sont motivées et constantes : lot FNA §8.76 apparié (pas indépendant), lot drogue §8.84 hors compte (n=46 < 50, objet drogue).

---

## 3. Tableau en trois colonnes

Définitions appliquées : **SOLIDE** = confirmé sur plusieurs cohortes ou plusieurs nuls ; **FRAGILE** = une seule paire, marge étroite, non consolidé ; **NON PROUVÉ / FERMÉ** = négatif ou inutilisable. Une justification d'une ligne par verdict.

### SOLIDE

| Verdict | Justification (une ligne) |
|---|---|
| CA125/CEA — survie | CA125 prédit la survie dans 2 cohortes sur 3 (TCGA Cox p=0,001 ; ICGC 9,5 contre 23,8 mois, le plus fort marqueur de survie), GSE71729 seule en échec. |
| PRMT5 / MTAP | Effet confirmé 4 fois par tests directs indépendants (pancréas −1,385 vs −1,010, p=0,0036 ; reproduit à l'identique au §8.40 ; effet CDKN2A nul quand MTAP est fixé, p=0,76). |
| Daraxonrasib | Fait clinique externe : FDA approuvé le 26 août 2026, phase III RASolute-302 OS 13,2 contre 6,7 mois, HR 0,40 (pas une prédiction du pipeline). |
| Blocs de co-expression (3) | Estomac/mucus, immunitaire et réparation ADN confirmés par tests directs sur plusieurs cohortes, réels bien au-dessus du bruit des nuls (§8.32, §8.33, §8.66). |
| M1 (mécanisme, §8.63) | Expliqué : la configuration (28,27,6) ne cause ni MC haut ni Delta bas — MC haut = pic étroit du scan, Delta bas = w=27. |
| M2 (mécanisme, §8.63 → §8.75) | Expliqué : réplication hors échantillon 80 % (24/30 ICGC frais, 9/10 GSE62452 frais, 40/40 runs), taux corrigé de 85 % à 80 %. |

### FRAGILE

| Verdict | Justification (une ligne) |
|---|---|
| Chaîne KRAS | Vue en TCGA v4 seule, jamais répliquée (CPTAC NON, GSE71729 inversée, tests A/C NON) et le pipeline ne sépare pas réel et nul sur cet axe. |
| CA125/CEA — expression | Monte avec KRAS en TCGA et GSE62452 (3/3) mais pas en GSE71729 (inversée pour CLDN18/PGC/DPCR1) ni en ICGC ni en pan-cancer. |
| Vopimetostat + daraxonrasib | 82 % de réponses (18/22) en phase 1/2 non randomisée, un seul sous-groupe (MTAP-délété), pas de survie globale ; phase 3 attendue 1H 2027. |
| ATR | Survit au contrôle prolifération en expression seule (2/2 cohortes, partiel +0,366 à +0,488) mais zéro appui CRISPR ni médicaments (0/60 FDR < 0,05). |
| Maxsep comme score | Passe A2 10/15 mais 5/15 échouent, deux paires passent à moins de 0,02 de marge (GDC +0,0184, GSE131050 +0,0039), D3/D4 en échec au §8.59 ; adoption pleine = décision de Zackary, pas preuve. |
| C3 (confirmation indépendante) | Levée à 7/11 par une seule paire (GSE60979 +0,2045), LOO 6/10, et les paires suivantes échouent (§8.88 NON) sans la relever. |
| Survie des gènes de privilège | 3/8 prédisent comme CA125 sur ≥ 2/3 cohortes, mais p limites (TGFB2 ICGC p=0,048), aucun ne passe Bonferroni dans ≥ 2 cohortes, log-rank contredit Cox pour le score en TCGA. |
| Chen drogue (§8.84) | Paire exploratoire CONFIRME consolidée (3/3 nuls au-dessus du plancher, 2 hits FDR) mais n=46 < 50, hors A2, et drogue × KRAS / × MTAP impossibles (§8.89). |
| GDC / MUCL3 (§8.85 → §8.87) | CONFIRME par règle graine 42 (+0,0884, marge 0,0184) mais FRAGILE CONFIRMÉ contre 13 nuls (d_médian +0,0314 sous le plancher, réel sous le p95 des nuls). |

### NON PROUVÉ / FERMÉ

| Verdict | Justification (une ligne) |
|---|---|
| Delta | Jamais élucidé (§8.39, §8.42, §8.57, §8.62) : aucun modèle, aucun hold-out ne passe, les magnitudes portent l'échelle de n, pas le contenu des flux. |
| Pic étroit (§8.73) | Déclencheur NON ÉLUCIDÉ, bloc extrême écarté, résidu renvoyé au §8.73 sans mécanisme. |
| Œil (§8.81) | MIXTE puis CLOSE comme copie d'un programme : score PRIV rho médian +0,122 sous le seuil +0,15, 3/7 gènes montent, UVM en image miroir. |
| Cerveau (§8.82) | Inverse de l'hypothèse : 7/7 gènes de privilège DESCENDENT quand la prolifération monte (médiane rho −0,287), pipeline PARTIEL fragile +0,0283 sous le plancher. |
| GSE194249 (§8.86 + §8.88) | INUTILISABLE à 12 flux (DPCR1 0/15 609, 0 run) puis NON à 11 flux (−0,0239, nul sépare plus que le réel, 0/3 nuls au-dessus du plancher). |
| Suppléments Chen (§8.89) | PISTE FERMÉE : aucune table par-PDO KRAS/MTAP dans les 17 suppléments ni les dépôts ; la question des hits §8.84 reste sans réponse, pas tranchée négativement. |

---

## 4. Résumé (5 lignes maximum)

- **0 écart numérique** sur les 9 chiffres clés revérifiés contre les fichiers de résultats (dont §8.79 +0,4494, §8.85 +0,0884, §8.84 +0,0982 et 2 hits FDR, §8.83 3/8, §8.50 médiane +0,1595, PRMT5 −1,385/−1,010 p=0,0036, §8.87 +0,0314, §8.88 −0,0239).
- **1 seule erreur de valeur trouvée :** la coquille SHA dans PROVENANCE_889 §7 (`0f828245…bef946` au lieu de `…aadadb0`, vérifiée par sha256sum ; le §4 de la même provenance porte la bonne valeur).
- **Plus grave incohérence :** le titre du §8.51 et la ligne §7 210 affirment que « la corrélation immunitaire n'est pas un artefact de composition », alors que le §8.54.8(f) révise explicitement cette lecture (effet d'infiltration) sans aucun renvoi depuis le titre ni le §7.
- **Corrections datées vérifiées présentes :** A2 9/13 → 10/14 aux §8.84 (ligne 20598) et §8.86 (ligne 21389), addendum §8.70/§8.72 (ligne 14363), distinction décision/preuve §8.64.12.
- **Classement :** 6 SOLIDE, 9 FRAGILE, 6 NON PROUVÉ / FERMÉ ; le dossier tient par ses tests directs (PRMT5/MTAP, blocs, daraxonrasib) et reste fragile sur l'instrument (maxsep, chaîne KRAS, Delta non élucidé).
