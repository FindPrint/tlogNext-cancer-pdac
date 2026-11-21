# VOLET 3 — Sécurité médicale (§8.90, audit PDAC)

**Nature du travail :** lecture seule. Aucune modification du livre blanc ni d'aucun fichier de résultats ; aucun run de pipeline lancé.
**Document audité :** `~/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md`
— 22 783 lignes, SHA-256 `39d3abd65eda029e…` (16 premiers caractères `39d3abd65eda029e`), état §8.1–§8.89, 21 novembre 2026.
**Date de l'audit :** 21 novembre 2026.
**Méthode :** grep exhaustif (motifs français et anglais, voir chaque section), lecture des passages concernés en contexte, vérification des faits cliniques contre les sources nommées dans le livre blanc (§8.20, §8.22, §8.80 et sa liste de sources, lignes 19183–19197) et contre des sources externes publiques (FDA, ONS, OncLive, Targeted Oncology, Drug Discov Ther 2026, SEC 8-K Tango du 23 oct. 2026, ClinicalTrials.gov NCT07066098, OncoDaily/Quiver pour l'approbation européenne).
**DATA_SOURCES.md :** le fichier `DATA_SOURCES.md` à la racine du dépôt n'est pas présent localement ; le snapshot local consulté (`~/workspace/push_v62_858_build/snap/DATA_SOURCES.md`, antérieur au §8.80) ne couvre pas les faits cliniques du §8.80. Les sources nommées pour ces faits sont donc celles de la liste « Sources » du §8.80 lui-même (14 sources, lignes 19183–19197) et celles des §8.20/§8.22. C'est une limite de traçabilité mineure, pas une erreur de fait (voir §3.6).

---

## 1. État de l'avertissement médical

### 1.1 Verdict : ABSENT en tête du document — non visible pour un lecteur qui n'ouvre que la couverture et l'introduction

Recherches effectuées (0 occurrence sauf mention contraire) :

| Motif cherché | Résultat |
|---|---|
| `conseil médical`, `pas un conseil médical`, `not medical advice`, `medical advice`, `disclaimer` | **0 occurrence** dans tout le livre blanc |
| `oncologue`, `médecin traitant`, `parlez-en`, `consulter` (au sens médical) | **0 occurrence** — le mot « oncologue » n'apparaît nulle part |
| `à titre informatif`, `but informatif`, `avis médical`, `ne remplace pas` (au sens médical) | **0 occurrence** pertinente |
| `pas d'usage médical` | 1 occurrence, ligne 18082 — mais elle décrit le README d'un **autre dépôt** (`universal-log-research`, §8.78.2), pas ce livre blanc |
| `Avertissement` | ~10 occurrences, toutes au sens méthodologique (« avertissement de Zackary : ne pas se fixer sur un seuil », « avertissement honnête : le nul vote DOWN lui aussi »), jamais au sens médical |
| Section « Éthique » ou « Reproductibilité » en titre de section | **Aucune.** Les seules occurrences du mot « éthique » sont dans le journal (§10, ligne 22690 : le PDF de 404 pages « contient […] éthique/reproductibilité ») — aucune section dédiée repérable par titre dans le livre blanc lui-même |

### 1.2 Ce qui existe déjà (protections implicites, réelles mais dispersées)

Le document n'est pas sans garde-fous — ils sont simplement éparpillés et formulés en langage de recherche, pas en langage d'avertissement au lecteur :

1. **§1 « Objectif, dit honnêtement » (lignes 11–19) :** « Il ne trouve pas un remède tout seul », « jamais vers une conclusion clinique », « Ce que ce livre blanc ne fera jamais : présenter une piste comme un remède, présenter un seuil comme une preuve clinique, ou cacher un résultat négatif. » — C'est la protection la plus proche d'un avertissement, mais elle parle du *document* et de sa méthode, pas du *lecteur* : elle ne dit pas « ne prenez aucune décision de traitement sur la base de ce document » et ne nomme ni l'oncologue ni le médecin.
2. **§9 « Candidats thérapeutiques » (lignes 22632–22647) :** « Aucun candidat validé à ce jour […] Ce qui suit sont des PISTES — des hypothèses […] à tester, pas des candidats » et « aucune combinaison thérapeutique, aucun médicament nommé comme efficace, aucune promesse clinique. » — Bien, mais placé à la ligne 22632 sur 22 783, donc invisible pour qui ne lit pas jusqu'au bout.
3. **Formule répétée en fin de chantiers** (ex. lignes 16258, 16831, 17241, 18614, 19248, 19451, 20669, 21875) : « Il ne dit rien de clinique : l'étude porte sur l'instrument, pas sur un remède — aucune affirmation sur le cancer du pancréas n'est tirée de ce chantier. » — Utile, mais enterrée en fin de sections techniques que seul un lecteur assidu atteint.
4. **Hedges ponctuels sur les faits cliniques** (§8.22 ligne 542 : « Ce n'est pas un remède démontré » ; §8.80 ligne 19017 : « Une annonce d'essai n'est pas une preuve d'efficacité » ; §8.18 ligne 479 : « Aucun remède démontré »). — Corrects, mais ce sont des réserves *sur les chiffres*, pas un avertissement *au lecteur*.

### 1.3 Jugement de visibilité

**Un lecteur qui n'ouvre que le PDF et lit la couverture + l'introduction ne voit PAS d'avertissement médical.** La couverture (lignes 1–9) donne le projet, le mandat (« Trouver un remède pour le cancer du pancréas ») et la règle de provenance — sans une ligne de mise en garde. L'introduction (§1) dit ce que le document ne fera jamais, sans jamais s'adresser à un patient ou à un proche, sans nommer l'oncologue, sans dire « ne changez pas votre traitement ». Or le mandat affiché en couverture (« trouver un remède ») est exactement le type de phrase qu'un lecteur en détresse peut prendre au pied de la lettre. **L'avertissement est donc à ajouter, en tête, et sa mise en tête du document est une dette explicite pour la prochaine révision du gabarit** (voir §1.4).

### 1.4 Texte d'avertissement renforcé proposé (à placer immédiatement sous le titre, avant le §1)

> **⚠ AVERTISSEMENT — LISEZ CECI D'ABORD**
>
> Ce document n'est **pas un conseil médical**. Il ne dit à personne quel traitement prendre, et il ne remplace pas l'avis d'un médecin.
>
> Ce que vous lisez ici est un **travail de recherche** : des calculs sur des données publiques, des essais cliniques publiés par d'autres, et des pistes à tester. Le mot « remède » dans ce document veut dire « piste de recherche à tester », jamais « traitement prouvé » ou « traitement à prendre ».
>
> **Aucune décision de traitement ne doit reposer sur ce document.** Les médicaments cités ici (par exemple le daraxonrasib ou le vopimetostat) sont des données d'essais cliniques publiés : certains sont approuvés dans certains pays et pour certains patients seulement, d'autres sont encore en essai et ne sont pas disponibles en dehors d'un essai. Les doses écrites ici sont celles des essais, pas des doses à prendre.
>
> **Si vous êtes malade ou si un proche est malade, parlez-en à votre oncologue (le médecin spécialiste du cancer) ou à votre médecin traitant.** Eux seuls connaissent votre situation et peuvent dire ce qui s'applique à vous. Ne commencez, ne changez et n'arrêtez aucun traitement à cause de ce document.
>
> Si une phrase de ce document vous fait espérer un traitement, montrez-la à votre oncologue et demandez-lui ce qu'elle vaut pour vous.

**Dette de gabarit (à inscrire dans le journal, §10) :** la mise en tête de cet avertissement — et sa reprise sur la page de couverture du PDF généré — est une dette pour la prochaine révision du gabarit du livre blanc. Tant qu'elle n'est pas faite, chaque PDF publié porte en première page un document dont le mandat affiché (« trouver un remède ») n'est contrebalancé par aucun avertissement visible. Priorité : haute, avant la prochaine publication.

---

## 2. Recommandations implicites — recherche par grep

### 2.1 Motifs cherchés, résultats bruts

| Motif | Occurrences |
|---|---|
| `prendre` / `administrer` / `donner` + dose ; `prescrire` ; `devrait recevoir` / `doivent recevoir` ; `il faut traiter` ; `à utiliser chez` ; `posologie` ; `dose` employée comme consigne | **0 occurrence d'ordre ou de consigne de traitement.** Aucune phrase du type « prendre X mg », « administrer », « prescrire », « le patient devrait recevoir ». |
| Doses chiffrées (mg, mg/kg, µM, nM) | **Toutes descriptives** (doses d'essais cliniques ou concentrations in vitro, avec source et contexte d'essai). Inventaire complet au §2.2. |
| `recommande` / `recommandation` | 12 occurrences — toutes portent sur le **pipeline** (adopter `maxsep` comme score) ou sur des chantiers internes, sauf 2 : la mention NCCN (§2.3, R5) et « recommandée » pour le test A (§8.34, interne). Aucune recommandation de traitement. |
| `traitement de première ligne` / `first-line` | Employé uniquement comme **cadre d'essai** (« en première ligne » = ligne de traitement de l'essai cité), jamais comme conseil. |
| `conseill-`, `doit être traité`, `efficace chez` (au sens prescriptif) | 0 occurrence prescriptive. |

**Conclusion de la recherche : aucune recommandation clinique directe n'a été trouvée.** Le risque ne vient pas d'un ordre de traitement, mais de formulations superlatives et de doses recopiables (voir §2.3).

### 2.2 Inventaire complet des doses et schémas cités (tous descriptifs — à conserver tels quels, sauf R3/R4)

| # | Ligne(s) | Phrase exacte (extraits) | Statut |
|---|---|---|---|
| D1 | 239, 19017, 19044 | « design désormais précisé (1:1, vopimetostat 200 mg + daraxonrasib 100 mg 1×/jour contre chimiothérapie standard, doubles critères ORR et PFS, démarrage 1er semestre 2027) » ; « Randomisation 1:1 : vopimetostat 200 mg 1×/jour + daraxonrasib 100 mg 1×/jour, contre chimiothérapie standard » | Descriptif : design de la phase 3 annoncée (communiqué Tango, 9 nov. 2026). Légitime. Voir R3 pour un ajout de garde-fou. |
| D2 | 19028 | « Tolérance (dose niveau 1, DL1 : vopimetostat 200 mg + daraxonrasib 100 mg 1×/jour) : chez 25 patients PDAC, 76,0 % d'événements indésirables […] DL2 (vopimetostat 250 mg) non tolérable (DLT chez 2 patients sur 4) — DL1 retenue comme dose candidate pour la phase 3. » | Descriptif : résultats de tolérance de la phase 1/2 (ESMO 2026). Légitime. Voir R4 (« dose candidate »). |
| D3 | 19029 | « dose retenue : vopimetostat 200 mg + zoldonrasib 1200 mg » (bras KRAS G12D, ORR 54,3 %) | Descriptif (ESMO 2026). Légitime. |
| D4 | 479 | « l'ADC IBI343 (phase I, NCT05458219, 83 patients : réponse confirmée 22,7 %, […] SG méd. 9,1 mois à 6 mg/kg, n = 44 ; Yu et al., J Clin Oncol 2025 ;43:4017) est en phase III pancréatique (G-HOPE-002, NCT07066098, en recrutement) » | Descriptif : dose de la cohorte de phase I. Légitime. |
| D5 | 512 | « ASP3082 (PROTAC G12D, Astellas) : phase I NCT05382559, 33,3 % à 300 mg (phase précoce). » | Descriptif. Légitime. |
| D6 | §8.20 (~l. 503–510) | MRTX1133 : « dose unique 2,5 µM » (PRISM) ; IC50 ChEMBL en nM (PANC-1 2,3 nM, AsPC-1 11,0 nM, HPAC 4,2 nM…) ; daraxonrasib ChEMBL (HPAC 1,2 nM, Capan-2 1,4 nM…) | Descriptif : concentrations in vitro / criblage. Légitime, non transposable à un patient. |

Aucune de ces doses n'est présentée comme une dose à prendre. Elles restent néanmoins **recopiables** par un lecteur non averti — d'où l'importance de l'avertissement du §1.4, qui les couvre toutes d'un coup (« Les doses écrites ici sont celles des essais, pas des doses à prendre »).

### 2.3 Occurrences à reformuler (formulations superlatives ou ambiguës — pas des recommandations directes)

| # | Ligne(s) / section | Phrase exacte | Problème | Reformulation proposée |
|---|---|---|---|---|
| R1 | 542, §8.22 | « C'est la première combinaison du projet dont les chiffres dépassent nettement la monothérapie daraxonrasib (~30 % de réponses). […] Ce n'est pas un remède démontré, c'est la piste la plus solide du projet. » | Superlatif « la plus solide du projet » accolé à un chiffre spectaculaire (82 %) ; le hedge (« pas un remède démontré ») est présent mais une lecture rapide ne retient que « 82 % » + « la plus solide ». | « C'est la combinaison dont les chiffres publiés sont les plus élevés parmi celles examinées dans ce projet (82 % de réponses en phase 1/2 non randomisée, n=22 — voir les limites ci-dessous). Cela en fait la piste à tester en priorité **en recherche**, pas un traitement recommandé : elle n'est pas prouvée, elle n'a jamais été comparée directement au daraxonrasib seul, et seule la phase 3 randomisée pourra dire si le chiffre tient. À discuter avec un oncologue ; ne pas en déduire un traitement. » |
| R2 | 43, §2 (état antérieur, simulation EDO) | « La combinaison ATR-i + G6PD-i et le timing du passage à MRTX/venetoclax sont l'hypothèse mécanistique la plus forte à tester contre DepMap/GDSC. » | « La plus forte » + noms de médicaments, dans une section d'état antérieur fondée sur une simulation (R3), sans rappel immédiat du statut simulationnel dans la phrase. | « La combinaison ATR-i + G6PD-i et le timing du passage à MRTX/venetoclax sont, **dans la simulation EDO du projet tlog28 seulement**, l'hypothèse mécanistique à tester en priorité contre DepMap/GDSC. Il s'agit d'une hypothèse issue d'une simulation, pas d'une piste clinique. » |
| R3 | 239, 19017, 19044, §8.80 + journal | « design désormais précisé (1:1, vopimetostat 200 mg + daraxonrasib 100 mg 1×/jour contre chimiothérapie standard…) » | La dose exacte de la future phase 3 est répétée 3 fois (journal, verdict, §1.1) sans jamais dire qu'il s'agit d'un **protocole d'essai à venir**, pas d'un schéma utilisable. | Ajouter, à la première occurrence (ligne 239 et verdict §8.80) : « (doses du protocole de l'essai à venir, publiées par le promoteur — pas un schéma de traitement ; la phase 3 n'a pas démarré et n'a pas de numéro NCT au 21 nov. 2026) ». |
| R4 | 19028, §8.80 §0 | « DL1 retenue comme dose candidate pour la phase 3. » | « Dose candidate » peut se lire comme « dose recommandée ». | « DL1 (vopimetostat 200 mg + daraxonrasib 100 mg 1×/jour) est la dose que le promoteur a choisie **pour tester dans la phase 3** — ce n'est pas une dose recommandée en dehors d'un essai. » |
| R5 | 19105, §8.80 §4.2 | « les recommandations américaines NCCN incluent désormais RASONQUE comme option préférée de catégorie 1 en traitement ultérieur du cancer du pancréas localement avancé ou métastatique, et le listent en première ligne comme "utile dans certaines circonstances". » | C'est un **compte rendu de recommandation d'un tiers** (NCCN), légitime en soi — mais rapporté sans lien vérifiable (absent de la liste « Sources » du §8.80, lignes 19183–19197) et sans préciser que ce n'est pas une recommandation de ce livre blanc. Un lecteur peut le prendre pour l'avis du document. | « Les recommandations américaines NCCN (rapportées ici, source à ajouter avec lien) incluent désormais RASONQUE comme option préférée de catégorie 1 en traitement ultérieur […] — il s'agit de la position du NCCN, pas d'une recommandation de ce livre blanc, qui ne recommande aucun traitement. » + ajouter la référence NCCN (version/date) à la liste des sources du §8.80. |
| R6 | 177 (journal §10) et 497 (§8.20) | « Première avance réelle du dossier : un médicament approuvé qui double la survie médiane — pas un remède, pas une prédiction du pipeline. » / « le daraxonrasib (RMC-6236) a doublé la survie médiane en phase III et a été approuvé par la FDA — une avance réelle, pas un remède » | Fait exact (13,2 vs 6,7 mois), mais « double la survie » sans population ni condition dans le résumé du journal peut se lire comme une promesse générale. | « Première avance réelle du dossier : dans l'essai RASolute 302, chez des patients prétraités, la survie médiane était de 13,2 mois avec le daraxonrasib contre 6,7 mois avec la chimiothérapie — une avance réelle pour ces patients de l'essai, pas une promesse pour un patient donné, et pas un remède. » |
| R7 | 22636–22647, §9 | « Les thérapies anti-CLDN18.2 (connues dans le cancer gastrique) seraient moins efficaces dans ce sous-groupe — il faudrait le tester avant de traiter » | « Avant de traiter » suppose un traitement à venir et s'adresse implicitement à une décision de traitement. La phrase est en réalité une mise en garde (tester avant), mais sa forme conditionnelle clinique est ambiguë. | « Les thérapies anti-CLDN18.2 seraient peut-être moins efficaces dans ce sous-groupe — c'est une hypothèse à tester en recherche, avant toute décision de traitement, qui relève de l'oncologue. » |
| R8 | 179 (journal §10) et 542 (§8.22) | « vopimetostat + daraxonrasib, MTAP-délétés : 82 % de réponses (18/22), contrôle 100 %, PFS 9 mois 88 %, médiane non atteinte (phase 1/2 NCT06922591, ESMO 2026 — vérifié indépendamment). Non randomisé, n=22, pas de survie globale ; phase 3 prévue 1H 2027. » | Fait exact et bien hedgé dans le corps (§8.22), mais dans le **journal** (ligne 179) la même formule apparaît en une ligne dense, sans le rappel « ce n'est pas un remède démontré » qui figure au §8.22. Le journal est la partie la plus lue en diagonale. | Dans le journal, ajouter à chaque mention du « 82 % » la courte réserve : « (phase 1/2 non randomisée, n=22, sans survie globale — piste, pas un traitement prouvé) ». |

**Bilan du §2 :** 0 recommandation clinique directe ; 8 reformulations proposées, toutes de l'ordre du garde-fou rédactionnel (superlatifs, doses répétées sans rappel du statut d'essai, compte rendu de recommandation tierce sans attribution explicite). Les descriptions d'essais (D1–D6) sont légitimes et n'ont pas à être supprimées — seulement encadrées par l'avertissement du §1.4.

---

## 3. Vérification des faits cliniques sensibles

Vérifiés contre les sources nommées dans le livre blanc et contre des sources externes publiques consultées le 21 novembre 2026 (FDA, ONS, OncLive, Targeted Oncology, Drug Discov Ther 2026 ;20:400–402, SEC 8-K Tango 23 oct. 2026, ClinicalTrials.gov).

| # | Fait tel qu'énoncé dans le livre blanc | Sections / lignes | Source nommée dans le livre blanc | Vérification externe | Verdict |
|---|---|---|---|---|---|
| F1 | Daraxonrasib (RMC-6236, RASONQUE™) approuvé par la FDA le **26 août 2026**, pour le PDAC métastatique prétraité | §8.20, l. 510 ; §8.80 §4.1, l. ~19100 ; journal l. 177 | Communiqué FDA ; Drug Discov Ther 2026 ;20:400–402 ; Cancer Network | Confirmé : FDA, 26 août 2026 ; ONS et OncLive reprennent la même date et la même indication | **CONFORME** |
| F2 | RASolute 302 (NCT06625320, phase III) : **OS médiane 13,2 vs 6,7 mois, HR 0,40** | §8.20, l. 510 ; §8.80 §4.2 | NEJM 2026, O'Reilly et al. 2026 ;395(4):325–337 (cité §8.80, source 11) | Confirmé en population ITT : 13,2 (IC 95 % 10,0–NE) vs 6,7 (5,8–8,0), HR 0,40 (0,30–0,53), p < 0,0001 ; PFS 7,2 vs 3,6 mois ; ORR 31,6 % vs 11,2 % | **CONFORME** (population ITT ; voir note N1) |
| F3 | Vopimetostat + daraxonrasib : **ORR 82 % (18/22), DCR 100 %, PFS à 9 mois 88 %**, phase 1/2 ESMO 2026 (NCT06922591), **non randomisé, n=22, pas de survie globale** | §8.22, l. 542 ; §8.80 §0, l. 19026–19028 ; journal l. 179 | Communiqué Tango 23 oct. 2026 ; dépôt SEC 8-K ; poster ESMO 3149P, Spira et al. ; Targeted Oncology 23 oct. 2026 | Confirmé mot pour mot par le 8-K : ORR 82 % (18/22, 11 confirmées + 7 non confirmées à la coupure, confirmées après), DCR 100 %, PFS médiane non atteinte, PFS à 9 mois 88 % (88,4 % valeur précise, IC 60,3–97,1 %), suivi médian 7,1 mois, coupure 20 août 2026, n=22 évaluables, étude ouverte non randomisée, pas d'OS | **CONFORME** (voir note N2, écart mineur de ventilation) |
| F4 | Approbation européenne de daraxonrasib seul (RASONQUE) le **16 nov. 2026** | §8.80 §4.1 ; journal l. 239 | Communiqué Revolution Medicines 16 nov. 2026 (rapporté via Quiver Quantitative et OncoDaily — sources 8 et 9 du §8.80) | Confirmé : décision de la Commission européenne annoncée le 16 nov. 2026, après avis positif du CHMP (oct. 2026, examen accéléré, Cancer Medicines Pathfinder) ; indication : adultes, PDAC métastatique, ≥1 traitement systémique antérieur, avec ou sans mutation RAS ; couverture UE + Islande, Norvège, Liechtenstein | **CONFORME** (voir note N3 sur le caractère indirect de la source) |
| F5 | IBI343 en **phase III pancréatique** (G-HOPE-002, NCT07066098, en recrutement) ; phase I : réponse confirmée **22,7 %**, DCR 81,8 %, SSP méd. 5,4 mois, SG méd. 9,1 mois à 6 mg/kg (n=44) | §8.18, l. 479 ; journal l. 22679 | Yu et al., J Clin Oncol 2025 ;43:4017 (phase I NCT05458219) ; NCT07066098 | Phase III confirmée : NCT07066098, « A Multicenter Study of IBI343 Monotherapy Versus Placebo… Pancreatic Cancer (G-HOPE-002) », phase 3, recrutement en cours, 201 participants prévus, dose 6 mg/kg IV J1 toutes les 3 semaines. Chiffres de phase I (22,7 % etc.) : source JCO 2025 nommée dans le livre blanc ; texte intégral de l'article non re-vérifié dans ce volet | **CONFORME** pour la phase III ; chiffres de phase I **non re-vérifiés en texte intégral** (source nommée, à re-vérifier à l'occasion) |
| F6 | Phase 3 vopimetostat + daraxonrasib : design précisé — 1:1, **vopimetostat 200 mg + daraxonrasib 100 mg 1×/jour** contre chimiothérapie, doubles critères ORR/PFS, OS secondaire clé, démarrage 1er semestre 2027, **pas de numéro NCT** au 21 nov. 2026 | §8.80 §1, l. 19040–19055 ; verdict l. 19017 | Communiqué Tango T3 2026, 9 nov. 2026 (source 1 du §8.80) | Confirmé : le communiqué T3 2026 de Tango annonce la phase 3 pivot en 1re ligne MTAP-délété, démarrage 1H 2027, et la dose de niveau 1 (200 mg / 100 mg QD) comme dose retenue ; aucune trace d'un numéro NCT publié à ce jour dans les sources consultées | **CONFORME** |
| F7 | NCCN : RASONQUE « option préférée de catégorie 1 » en traitement ultérieur du PDAC localement avancé ou métastatique ; « utile dans certaines circonstances » en première ligne | §8.80 §4.2, l. 19105 | « Recommandations américaines NCCN » — **aucun lien ni référence de version/date dans la liste des sources du §8.80** | Non re-vérifié en externe dans ce volet (pas de source primaire consultée) | **NON RE-VÉRIFIÉ** — affirmation sans source vérifiable jointe ; à sourcer (version/date NCCN) ou à retirer avant publication (voir R5) |

### 3.1 Notes et écarts mineurs (aucun fait clinique faux trouvé)

- **N1 — RASolute 302, sous-groupe G12 :** dans la population RAS G12-mutante, la survie du bras chimiothérapie est de **6,6 mois** (et non 6,7) — le livre blanc utilise partout le chiffre **ITT 6,7 mois**, qui est le bon chiffre pour la population totale citée. Pas d'erreur ; simplement ne jamais citer « 13,2 vs 6,7 » en l'attribuant au sous-groupe G12.
- **N2 — Ventilation 2e/3e ligne du 82 % (§8.80 §0) :** le livre blanc écrit « ORR 85,7 % en 2e ligne (n=7) et 84,6 % en 3e ligne (n=13) ». Or 7 + 13 = 20 patients et 6 + 11 = 17 réponses, alors que le total est de 22 patients et 18 réponses. **2 patients et 1 réponse ne sont pas expliqués par cette ventilation** (ligne de traitement inconnue ou non ventilée dans la source). Ce n'est pas un fait faux — le total 18/22 est confirmé par le 8-K — mais une incohérence interne mineure. **Correction proposée (addendum daté, §3.2) :** préciser « 2 patients non ventilés par ligne de traitement dans les sources consultées (7 en 2e ligne + 13 en 3e ligne = 20 sur 22) ».
- **N3 — Approbation européenne, source indirecte :** le livre blanc le déclare lui-même (§8.80 §7, Limites) : le communiqué original de Revolution Medicines n'a pas été lu directement mais via Quiver Quantitative et OncoDaily. La vérification externe de ce volet confirme le fait (date, indication, périmètre EEE) via ces mêmes reprises et via OncLive/The Pharma Letter. Pas d'erreur ; la réserve de source indirecte est déjà dans le document et doit y rester.
- **N4 — Indication FDA, simplification au §8.20 :** le §8.20 écrit « pour le PDAC métastatique prétraité », alors que l'indication FDA complète est « ≥1 traitement antérieur **ou** non candidat à une chimiothérapie multi-agents ». Le §8.80 §4.1, lui, donne l'indication complète. **Correction proposée (addendum daté) :** aligner le §8.20 sur le §8.80 en ajoutant « ou non candidat à une chimiothérapie multi-agents ».
- **N5 — « PFS 6 et 9 mois 88,4 % » (§8.22) :** le 8-K donne un taux de PFS à 9 mois de 88 % (88,4 % valeur précise avec IC 60,3–97,1 % au §8.80). La formulation « 6 et 9 mois 88,4 % » est ambiguë (même taux aux deux temps). Conforme au fond ; reformuler en « PFS à 6 et 9 mois : 88,4 % » avec l'IC, comme au §8.80.

### 3.2 Addendum daté proposé (à joindre à la prochaine publication, sans réécrire l'historique)

> **Addendum — 21 novembre 2026 (audit §8.90, volet 3, sécurité médicale).**
> 1. Aucun fait clinique sensible vérifié n'est faux. Les chiffres daraxonrasib (FDA 26 août 2026 ; RASolute 302 OS 13,2 vs 6,7 mois, HR 0,40), vopimetostat + daraxonrasib (ORR 82 %, 18/22, DCR 100 %, phase 1/2 non randomisée, n=22, sans OS), approbation européenne (16 nov. 2026) et IBI343 phase III (G-HOPE-002, NCT07066098, en recrutement) sont conformes à leurs sources.
> 2. Précision — ventilation 2e/3e ligne (§8.80 §0) : 7 patients en 2e ligne + 13 en 3e ligne = 20 patients sur 22 ; 2 patients (et 1 réponse sur 18) ne sont pas ventilés par ligne dans les sources consultées.
> 3. Précision — indication FDA (§8.20) : ajouter « ou non candidat à une chimiothérapie multi-agents » (indication complète, déjà donnée au §8.80 §4.1).
> 4. À sourcer — NCCN catégorie 1 (§8.80 §4.2, l. 19105) : aucune référence (version/date/lien) n'est jointe ; à compléter ou à retirer.
> 5. Avertissement médical en tête du document : absent (voir §1 du présent volet) — dette de gabarit pour la prochaine révision.

### 3.3 Ce qui n'a pas été vérifié dans ce volet

- Le texte intégral de Yu et al., JCO 2025 (chiffres de phase I d'IBI343 : 22,7 %, DCR 81,8 %, SSP 5,4, SG 9,1 mois) — source nommée, non re-lue en texte intégral.
- Les chiffres des autres essais cités en passant (§8.18 : GLEAM 13,7 vs 13,6 mois, HR 0,999 ; SPOTLIGHT/GLOW ; satri-cel 16,7 % ; IBI389 29,6 % ; sotorasib/adagrasib) — hors du périmètre demandé, non re-vérifiés ici.
- Le fichier `DATA_SOURCES.md` à la racine du dépôt distant (non présent localement) — voir l'introduction du présent rapport.

---

## 4. Appréciation globale du risque pour un lecteur

**Risque réel ou théorique ? Réel mais circonscrit — et entièrement évitable par l'avertissement du §1.4.**

- **Ce qui rend le risque réel :** (a) le document est public (dépôts GitHub publics, PDF partageable) et son mandat affiché en couverture est « trouver un remède » ; (b) il répète des chiffres spectaculaires et exacts — « 82 % de réponses », « double la survie médiane », « la piste la plus solide » — sans jamais dire au lecteur « parlez-en à votre oncologue » (0 occurrence du mot) ; (c) il donne des doses exactes et recopiables (200/100 mg, 6 mg/kg, 300 mg) ; (d) il n'a ni avertissement en tête ni section éthique. Un patient ou un proche en détresse, lisant le PDF seul, peut en déduire un traitement à demander — ou pire, à chercher hors circuit médical — sans que rien dans le document ne l'en dissuade explicitement.
- **Ce qui circonscrit le risque :** (a) **aucune recommandation clinique directe n'existe** — aucune phrase ne dit de prendre quoi que ce soit ; (b) les faits cliniques sensibles vérifiés sont **tous exacts** (aucun faux chiffre qui ferait espérer à tort ou qui minimiserait un danger) ; (c) les réserves méthodologiques sont honnêtes et répétées (« non randomisé, n=22, pas de survie globale », « ce n'est pas un remède démontré », « une annonce d'essai n'est pas une preuve d'efficacité ») ; (d) les doses sont toujours présentées dans leur contexte d'essai, jamais comme des posologies.
- **En une phrase :** le document ne dit à personne de se traiter, mais il ne dit à personne de ne pas se traiter sur sa base — et c'est cette absence, pas une erreur de contenu, qui constitue le risque. L'avertissement du §1.4 le supprime presque entièrement, à coût nul.

## 5. Actions proposées (par ordre de priorité)

1. **Avant la prochaine publication :** insérer l'avertissement du §1.4 immédiatement sous le titre (et sur la couverture du PDF). Dette de gabarit à inscrire au §10.
2. **Avec la prochaine publication :** joindre l'addendum daté du §3.2 (4 précisions, aucune correction de fait majeur).
3. **Révisions rédactionnelles :** appliquer les 8 reformulations R1–R8 (superlatifs, « dose candidate », compte rendu NCCN, journal).
4. **Traçabilité :** ajouter la référence NCCN (version/date/lien) ou retirer l'affirmation F7 ; re-vérifier les chiffres de phase I d'IBI343 en texte intégral à l'occasion.

---

## Résumé (5 lignes maximum)

1. Aucune recommandation clinique directe et aucun fait clinique faux : les chiffres daraxonrasib (FDA 26 août 2026, OS 13,2 vs 6,7 mois, HR 0,40), vopimetostat + daraxonrasib (82 %, 18/22, non randomisé, n=22, sans OS), approbation européenne (16 nov. 2026) et IBI343 phase III sont tous conformes à leurs sources.
2. En revanche, le livre blanc ne porte aucun avertissement médical visible : 0 occurrence de « conseil médical » ou « oncologue », aucune section éthique, et la couverture affiche « trouver un remède » sans mise en garde.
3. Le risque vient de formulations superlatives (« la piste la plus solide », « double la survie ») et de doses exactes recopiables (200/100 mg, 6 mg/kg), sans aiguillage vers un oncologue.
4. Risque réel mais circonscrit : personne n'est incité à prendre un traitement, mais rien ne dissuade un lecteur en détresse d'interpréter les chiffres comme un traitement à demander.
5. Correctif : insérer en tête le texte d'avertissement proposé (§1.4), joindre l'addendum daté (§3.2, 4 précisions mineures dont la ventilation 2e/3e ligne incomplète), appliquer 8 reformulations — dette de gabarit à inscrire au §10 avant la prochaine publication.
