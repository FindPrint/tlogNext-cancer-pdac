### 8.40 Arbitrage de la contradiction MTAP — tests directs (19 novembre 2026)

**Verdict d'abord, en trois phrases. (a) OUI, le groupe MTAP-délété se distingue — par la dépendance PRMT5 : pancréas −1,385 contre −1,010, p = 0,0036, reproduit à l'identique, et l'effet suit MTAP et non CDKN2A pour la quatrième fois (stratifications CN et mutation, p = 0,26 / 0,46 / 0,76). (b) NON, aucun médicament des trois écrans détenus ne distingue ce groupe : 0 composé FDR < 0,05 sur 6 790 (PRISM primaire), 1 437 (PRISM secondaire) et 269 (GDSC2), et les inhibiteurs PRMT5 présents sont tous non significatifs. (c) NON, le groupe MTAP-délété n'est pas le groupe KRAS-fort : Fisher TCGA reconfirmé exactement à p = 0,073, Fisher lignées p = 0,31, chevauchement 6/12 tumeurs et 7/12 lignées. L'arbitrage est donc partiel : ces tests tranchent que le groupe MTAP-délété existe comme groupe biologique distinct et qu'il n'est pas le groupe KRAS-fort — mais ils ne tranchent pas la contradiction instrumentale : S_sep dit réel > nul (+0,20) pendant que MC (−0,16) et Delta (−0,54) disent nul > réel, et rien ici n'explique pourquoi le pipeline ne sépare pas réel et nul sur la série MTAP (§8.36/§8.38). La contradiction entre indicateurs reste ouverte.**

## 8.40.1 Question, méthode, règles

**Question.** Le pipeline v6.2 donne, sur la série TCGA v4 ordonnée par CN MTAP, S_sep +0,1968 (réel > nul) mais MC −0,1642 et Delta −0,5416 inversés (§8.38). Le groupe MTAP-délété se distingue-t-il vraiment — et si oui, de quoi, et par quoi ?

**Méthode — tests directs, aucun run de pipeline.** Trois tests, tous recalculés le 19 nov. 2026 depuis les fichiers déjà sur le disque, script neuf `mtap_arbitration_840.py` (SHA `1fccc2f6…e6a688`, systemd-run unité `mtap-840c`, exit 0, 144,8 s). Définitions gelées avant tout calcul : CN DepMap = relatif **linéaire** (1,0 = diploïde), délétion profonde CN < 0,5, sensibilité CN < 1 ; Chronos plus négatif = plus dépendant ; PRISM primaire = log-fold-change viabilité (plus bas = plus sensible, une seule dose 2,5 µM), PRISM secondaire = AUC (plus bas = plus sensible), GDSC2 = LN_IC50 et AUC (plus bas = plus sensible) ; par composé, test Mann-Whitney bilatéral si n_délétées ≥ 5 et n_intactes ≥ 5, FDR Benjamini-Hochberg par écran et par mesure ; Fisher exact bilatéral (critère pré-enregistré §8.26). Aucune imputation, paires complètes uniquement. Les résultats antérieurs (§8.26/§8.28/§8.29/§8.36/§8.38) ont servi d'attendus de reproduction, jamais de verdicts réimportés.

**Corrections trouvées en cours de route (traçabilité, pas silence).** Trois erreurs de comptage ont été attrapées avant le run final et corrigées : (1) le Fisher TCGA comptait d'abord la tumeur sans GISTIC (TCGA-FB-A4P6, NaN) dans la case « reste, non délétée » (166 au lieu de 165) et donnait p = 0,0409 au lieu de 0,0732 — corrigé par exclusion des NaN (n = 177 appariées) ; cette sensibilité à une seule tumeur est un résultat en soi (voir §8.40.4). (2) GDSC2 contient plusieurs courbes par paire (médicament, lignée) — 242 036 lignes pour 235 748 paires uniques — et sans déduplication le Mann-Whitney comptait plusieurs fois la même lignée (Acetalax en tête du top-10 avec n = 16/22 pour 8 délétées seulement) ; corrigé par agrégation par médiane par paire, Acetalax disparaît du top-10. (3) La liste des composés PRISM primaire contient 1 ID BRD en double (AZ-628, REP.1M et REP.300), qui gonflait le comptage à 6 791 composés ; corrigé par déduplication (6 789 IDs uniques, 6 790 lignes de matrice testées). Le secondaire agrège en plus par (nom, lignée), médiane AUC, comme au §8.19 (54 noms à 2 broad_id).

## 8.40.2 Test (a) — Dépendance PRMT5 par copie MTAP : OUI, reproduit à l'identique

| Test | Groupe | n | PRMT5 Chronos médiane | p (Mann-Whitney) |
|---|---|---|---|---|
| Pancréas, CN < 0,5 | délétées / intactes | 20 / 27 | **−1,385 / −1,010** (diff −0,375) | **0,0036** |
| Pancréas, CN < 1 (sensibilité) | sous-diploïdes / diploïdes+ | 38 / 9 | −1,126 / −0,945 (diff −0,181) | 0,0295 |
| Pan-cancer, CN < 0,5 | délétées / intactes | 294 / 884 | −1,092 / −0,977 (diff −0,114) | 1,7×10⁻¹⁴ |
| Spearman continu, pancréas | PRMT5 ~ CN MTAP | 47 | rho **+0,497** | 0,00038 |
| Spearman continu, pan-cancer | PRMT5 ~ CN MTAP | 1 178 | rho +0,165 | 1,3×10⁻⁸ |

Reproduction exacte des §8.28/§8.29 au chiffre près (médianes −1,385/−1,010, p = 0,0036 ; Spearman pancréas +0,497). Contrôles propres : CDKN2A Chronos p = 0,19, KRAS p = 0,30, ACTB p = 0,74 en pancréas. Cohérence interne : Spearman PRMT5–KRAS pancréas rho −0,189, identique au balayage (§8.28).

**MAT2A — nouveau, et négatif.** MAT2A est le partenaire synthétique-létal classique de la perte MTAP (la voie de sauvetage de la méthionine) : si la vulnérabilité MTAP passait par MAT2A, sa dépendance Chronos devrait suivre la délétion. Elle ne la suit pas en pancréas : médianes −2,068 contre −1,901 (diff −0,167), p = 0,14 ; Spearman +0,090, p = 0,55. Au pan-cancer, l'écart est petit (−1,804 contre −1,738, p = 0,041) et ne survit pas à la correction pour les 2 gènes testés (Bonferroni 0,025). **Pas de vulnérabilité MAT2A mesurable dans ces lignées** — la dépendance liée à MTAP passe par PRMT5, pas par MAT2A, sur ces données.

**CDKN2A quand MTAP est fixé — quatrième confirmation que l'effet suit MTAP.** Deux stratifications neuves, données du jour, en plus des deux déjà connues (§8.29 : p = 0,26 pan-cancer ; §8.36 : p = 0,76, par mutation) :

| Stratification | Strate | n (CDKN2A-délétée / intacte) | PRMT5 médianes | p | d de Cohen |
|---|---|---|---|---|---|
| Par CN, pancréas | MTAP-intacte | 7 / 20 | −1,049 / −0,984 | 0,46 | −0,30 |
| Par CN, pan-cancer | MTAP-intacte | 137 / 747 | −1,013 / −0,973 | 0,257 | −0,10 |
| Par mutation, pancréas (§8.36 reconfirmé) | MTAP-intacte | 10 / 15 | −0,978 / −1,010 | **0,76** | +0,19 |

La stratification par mutation reproduit le §8.36 au chiffre près (non stratifié p = 0,014, d = +0,78 ; stratifié MTAP-intacte p = 0,7603, d = +0,19). La strate MTAP-délétée ne peut pas être testée dans l'autre sens : en pancréas, les 20 lignées MTAP-délétées sont toutes CDKN2A-délétées (20/0) ; au pan-cancer, 293/1. La perte de MTAP sans perte de CDKN2A n'existe quasiment pas — la séparation ne peut se faire que dans ce sens-là, et elle est faite quatre fois, par deux angles (CN et mutation) et deux échelles (pancréas et pan-cancer).

**Verdict (a) : OUI.** Le groupe MTAP-délété se distingue par la dépendance PRMT5 — effet réel, reproductible à l'identique, spécifique (MAT2A non, contrôles plats), et porté par MTAP lui-même, pas par la délétion 9p21. Ce que ce test ne dit pas : il ne dit rien d'un médicament (voir test b), et il ne dit rien du pipeline (aucun run ici).

## 8.40.3 Test (b) — Écrans de médicaments : NON, aucun ne distingue le groupe

Trois écrans déjà détenus, re-criblés par groupe MTAP (délété vs intact, lignées pancréas seulement) :

| Écran | Lignées pancréas communes (dél. / intactes) | Composés testés | FDR < 0,05 | FDR min |
|---|---|---|---|---|
| PRISM primaire 24Q2 | 38 (16 / 22) | 6 790 | **0** | 0,959 |
| PRISM secondaire 19Q4 | 29 (13 / 16) | 1 437 | **0** | 0,625 |
| GDSC2 (LN_IC50 / AUC) | 23 (8 / 15) | 269 / 269 | **0 / 0** | 0,561 / 0,882 |

Aucune classe ne se dégage. Les plus petites p brutes sont des curiosités sans FDR (primaire : bromopride p = 0,00032, FDR 0,959 — et dans le sens inverse, les délétées *moins* sensibles, diff +0,326 ; secondaire : tyrphostin-A9 p = 0,00058, FDR 0,625, diff +0,064, même sens inverse ; GDSC2 : AZD5991, inhibiteur MCL1, LN_IC50 p = 0,0068, FDR 0,561, diff −1,337 — le seul top-10 dans le sens « délétées plus sensibles », suivi d'alisertib, vinorelbine, vinblastine, tous FDR ≥ 0,56).

**Inhibiteurs PRMT5 présents — tous non significatifs.** C'est le point qui compte pour la piste vopimetostat :

| Composé | Écran | n (dél. / intactes) | Diff médiane (dél. − intactes) | p | FDR |
|---|---|---|---|---|---|
| EPZ015666 (cible PRMT5) | PRISM primaire | 13 / 16 | −0,048 | 0,37 | 0,977 |
| GSK3326595 (inh. PRMT5) | PRISM primaire | 16 / 22 | −0,050 | 0,53 | 0,991 |
| JNJ-64619178 (inh. PRMT5) | PRISM primaire | 16 / 22 | −0,255 | 0,43 | 0,985 |
| HLCL-61 (cible PRMT5) | PRISM primaire | 13 / 16 | −0,001 | 0,68 | 0,998 |
| GSK591 (cible « PMRT5 », faute de frappe GDSC) | GDSC2 LN_IC50 / AUC | 8 / 15 | −0,593 / −0,007 | 0,238 / 0,776 | 0,583 / 0,951 |

**Absents, à nommer :** le vopimetostat n'est dans aucun des trois écrans (ni dans la recherche par nom sur les listes complètes) ; aucun inhibiteur MAT2A n'est présent nulle part (0 ligne « MAT2A » dans les trois bibliothèques) ; le secondaire 19Q4 ne contient aucun composé PRMT5/MAT2A (bibliothèque de 2019). L'adénine — dont la cible listée inclut MTAP — est non significative au primaire (p = 0,55).

**Lecture honnête de ce négatif.** Il ne contredit pas le test (a). Un Chronos mesure une dépendance génétique (perte du gène) ; un écran de viabilité à dose unique (primaire, 2,5 µM) ou une AUC dose-réponse mesure une sensibilité à une molécule donnée, à une exposition donnée, avec 8 à 16 lignées délétées seulement. Les inhibiteurs PRMT5 présents sont anciens et ne sont pas le vopimetostat ; l'absence de signal différentiel pour EPZ015666 ou GSK591, à ces effectifs, n'est pas une preuve que la fenêtre PRMT5 n'existe pas — c'est l'absence d'un signal médicamenteux mesurable dans ces écrans. **Verdict (b) : NON** — dans les écrans détenus, le groupe MTAP-délété n'a pas de médicament différentiel, et pas d'inhibiteur PRMT5 différentiel.

## 8.40.4 Test (c) — Lien avec l'axe KRAS : NON, ce n'est pas le même groupe

| Test | Groupes comparés | Chiffres | p (Fisher bilatéral) |
|---|---|---|---|
| TCGA, reconfirmé (§8.26) | MTAP −2 chez KRAS-forts vs reste | 6/12 (50 %) vs 37/165 (22 %), OR 3,46 | **0,073 (ns)** |
| Lignées, top-12 KRAS-dépendantes (Chronos KRAS le plus négatif) | MTAP-délétées chez KRAS-forts vs reste | 7/12 (58 %) vs 13/35 (37 %), OR 2,37 | 0,31 (ns) |
| Lignées, tertile KRAS-dépendant | MTAP-délétées, tertile vs reste | 8/16 vs 12/31, OR 1,58 | 0,54 (ns) |
| Lignées, continu | CN MTAP vs Chronos KRAS | rho −0,037, n = 47 | 0,81 (ns) |

**Chevauchements (listes exactes).** Tumeurs : 6 des 12 KRAS-forts sont MTAP-délétées — la moitié. Lignées : 7 des 12 plus KRAS-dépendantes sont MTAP-délétées — ACH-000114, ACH-000222, ACH-000266, ACH-000468, ACH-000517, ACH-000601, ACH-002186. Les deux groupes se recoupent à environ moitié, dans les deux sens (13 des 20 lignées MTAP-délétées ne sont pas dans le top-12 KRAS ; 5 des 12 KRAS-forts ne sont pas MTAP-délétées), sans enrichissement démontré dans aucune des quatre formulations.

**Fragilité du Fisher TCGA, consignée.** Le p = 0,0732 n'est retrouvé qu'après exclusion de la tumeur sans GISTIC (TCGA-FB-A4P6) : si on la compte comme non délétée (reste 166 au lieu de 165), p tombe à 0,0409 — le verdict bascule sur une seule tumeur sans statut. Le Fisher TCGA est donc, à ces effectifs, indécidable par une tumeur près : ni « enrichi » ni « non enrichi » ne tient fermement, et seule une cohorte plus grande trancherait. Les trois autres formulations (lignées, p = 0,31 / 0,54 / 0,81) vont toutes dans le même sens — pas de lien démontré — ce qui rend le « non » global plus solide que le seul p = 0,073.

**Verdict (c) : NON.** Le groupe MTAP-délété n'est pas le groupe KRAS-fort. Il le recoupe à ~50–58 %, sans enrichissement démontré. La combinaison vopimetostat + daraxonrasib ne s'adresse donc pas aux mêmes patients que l'axe KRAS — elle s'adresse aux MTAP-délétés, comme déjà conclu au §8.26.

## 8.40.5 Arbitrage — ce qui est tranché, ce qui reste ouvert

**Tranché par ce chantier.**

- Le groupe MTAP-délété **existe comme groupe biologique** : sa dépendance PRMT5 est réelle, reproductible à l'identique, spécifique (MAT2A non, contrôles plats), et portée par MTAP, pas par CDKN2A — quatrième confirmation, par deux angles et deux échelles.
- Il **n'est pas le groupe KRAS-fort** : quatre formulations, aucune significative, chevauchement ~50 %.
- Il **n'a pas de médicament différentiel dans les écrans détenus** : 0 FDR < 0,05 sur trois écrans, inhibiteurs PRMT5 présents tous non significatifs, vopimetostat et inhibiteurs MAT2A absents des bibliothèques.

**Non tranché — la contradiction instrumentale reste ouverte.** S_sep +0,1968 (réel > nul) est compatible avec une vraie distinction biologique du groupe MTAP — le groupe existe, donc un indicateur qui le voit n'est pas absurde. Mais MC −0,1642 et Delta −0,5416 (nul > réel, §8.38) restent inexpliqués : si le groupe est biologiquement distinct, pourquoi deux indicateurs du même pipeline voient-ils le nul devant ? Ces tests directs ne répondent pas à cette question — ils portent sur les lignées et les tumeurs, pas sur ce que le pipeline calcule sur la série ordonnée par CN MTAP. **Le verdict §8.36 (NON : la chaîne ne réapparaît pas sous l'ordre MTAP ; le pipeline ne sépare pas réel et nul sur cette série) n'est pas renversé.** S_sep ne devient pas, par ce chantier, un arbitre entre MC et Delta : un seul indicateur positif contre deux inversés ne suffit pas, comme déjà dit au §8.38.

**Ce que ça change, et ce que ça ne change pas.**

- **Ne change pas :** le rationnel vopimetostat + daraxonrasib reste appuyé par la dépendance PRMT5 (§8.28/§8.29, confirmés ici) et par le résultat clinique externe (82 % de réponses, §8.22) ; la combinaison reste non prouvée (phase 1/2 non randomisée, n = 22). Ce chantier n'ajoute ni n'enlève rien à ce rationnel — les écrans ne contiennent pas le vopimetostat.
- **Change :** MAT2A sort de la liste des vulnérabilités à tester sur ces données (dépendance plate en pancréas) ; le Fisher TCGA est reconnu fragile à une tumeur près (p = 0,073 contre 0,041 selon le traitement de la tumeur sans GISTIC) — il ne doit plus être cité sans cette réserve.
- **Nouvelle hypothèse (à tester, pas un verdict) :** si le groupe MTAP-délété est biologiquement distinct mais que le pipeline ne le sépare pas du nul sur la série ordonnée par CN MTAP, c'est peut-être que la série elle-même (12 flux d'expression ordonnés par CN) ne porte pas la distinction — la dépendance PRMT5 est un phénotype CRISPR, pas une signature d'expression. Tester une série dont les flux incluraient la dépendance PRMT5 elle-même ordonnerait le test sur la variable qui distingue — mais ce serait tester le pipeline sur la réponse, pas sur une question : à ne faire que sur protocole gelé explicite, avec le go de Zackary.

## 8.40.6 Provenance

- **Script neuf, aucun code original modifié.** `mtap_arbitration_840.py` (SHA-256 `1fccc2f60d2c032c803b8ec26748200d6eb9296d4d464c455e6a68803ab4e7af`), log `mtap_arbitration_840.log` (SHA `718139c607ee7b5a52b812a863b4af24e2bcc477b9eef4c4d5d8fd6ddde41a4a`), systemd-run unité `mtap-840c`, exit 0, 144,8 s. Deux lancements antérieurs documentés dans `PROVENANCE_mtap_arbitration_840.md` (exit 1, puis exit 0 avec erreurs de comptage).
- **Sources (SHA-256 vérifiés avant les tests, complets dans `PROVENANCE_mtap_arbitration_840.md`).** DepMap Public 24Q4 (figshare 27993248) : `CRISPRGeneEffect.csv` `3d8f3ec6…`, `Model.csv` `b7a0c138…`, `OmicsCNGene.csv` `4851d3e9…` (MD5 `4696565f…`, exact) ; PRISM primaire 24Q2 : matrice `3b6554cf…`, liste `7e78f590…`, méta `13a85da9…` ; PRISM secondaire 19Q4 (Corsello et al., *Nat Cancer* 2020, figshare 9393293) : `88d10135…` (MD5 `e629b9d5…`, exact) ; GDSC2 (Cell Model Passports, fichier 22870) : `0e99120a…` ; table de mutations `f3fa2bd2…` ; `mtap_gistic_status.csv` `b54cb94f…`. Aucun fichier retéléchargé.
- **Sorties.** `mtap_arbitration_840_results.csv` (SHA `277ca482…`, 27 lignes : tous les tests a/c) ; `mtap_arbitration_840_pancreas_lines.csv` (SHA `a10fd028…`, 47 lignées, CN + Chronos + statuts) ; `mtap_arbitration_840_prism_primary.csv` (SHA `67466b24…`, 6 790 composés) ; `mtap_arbitration_840_prism_secondary.csv` (SHA `39a63c42…`, 1 437 composés) ; `mtap_arbitration_840_gdsc.csv` (SHA `ceaedd89…`, 269 médicaments) ; `PROVENANCE_mtap_arbitration_840.md` (provenance complète, JSON).
- **Nature des lignes.** Dépendance Chronos, copies CN, viabilités PRISM, IC50 GDSC2 = mesures instrumentales ; statuts GISTIC = appels mesurés ; aucun nul dans ce chantier (tests directs, pas de run de pipeline) ; aucun mot humain, aucun échantillon hypothétique.
- **Ce qui manque, ce qui reste ouvert.** La contradiction S_sep / MC / Delta sur la série MTAP n'est pas arbitrée (voir §8.40.5) ; le Fisher TCGA est fragile à une tumeur près ; les écrans ne contiennent ni vopimetostat ni inhibiteur MAT2A — la sensibilité différentielle au vopimetostat lui-même n'est testable dans aucune donnée détenue ; la piste « série de flux incluant la dépendance PRMT5 » est une hypothèse, pas un protocole (go requis). PDF non régénéré, rien poussé sur GitHub (hors de ce chantier).

— Fin de la §8.40. —
