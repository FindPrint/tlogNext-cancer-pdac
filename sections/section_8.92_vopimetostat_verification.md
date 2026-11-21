# §8.92 — Vérification vopimetostat + daraxonrasib, phase 3 : NON CHANGÉ pour la combinaison — toujours pas de numéro NCT, toujours pas de nouvelle coupe de données ; deux faits nouveaux par ailleurs (21 novembre 2026)

**Projet :** PDAC — livre blanc v6.2
**Section :** §8.92 (suite du §8.80, vérifié le 21 nov. 2026,
07h00–07h15 EST)
**Période couverte :** depuis la vérification du §8.80 (21 nov.
2026, 07h15 EST) — soit, en pratique, une re-vérification le même
jour, ~11h15–12h00 EST, avec une interrogation directe et
exhaustive de ClinicalTrials.gov que le §8.80 n'avait pas pu faire
(§8.80 §7)
**Protocole gelé :** `PROTOCOL_vopimetostat_verification_892.md`
**Provenance :** `PROVENANCE_892.md`
**Statut :** veille documentaire — aucune donnée nouvelle mesurée
ici ; tous les faits cliniques ci-dessous sont externes, rapportés
avec leur source.

---

## Verdict

**NON CHANGÉ pour la combinaison vopimetostat + daraxonrasib : la
phase 3 n'a toujours pas de numéro NCT, toujours pas de date de
premier patient, et il n'existe toujours aucune nouvelle coupe de
données TNG462-C102 depuis ESMO 2026 (coupure du 20 août 2026,
ORR 82 %, n=22).** Le chiffre clinique central est inchangé, le
rationnel MTAP/PRMT5 mesuré ici (§8.28/§8.29/§8.40) n'est ni
confirmé ni infirmé par quoi que ce soit de nouveau. **Deux faits
sont en revanche nouveaux pour le livre blanc : (1) un nouvel
essai vopimetostat a été enregistré, NCT07938463 (TAP-ALK :
vopimetostat + lorlatinib dans le cancer du poumon ALK+ MTAP-délété,
première publication le 16 novembre 2026) — une autre combinaison,
pas la phase 3 pancréatique ; (2) le 10-Q de Tango du 9 novembre
2026, lu ici à la source primaire (SEC), avertit qu'il n'y a
« aucune assurance » que Tango obtienne l'approvisionnement
clinique en daraxonrasib pour la phase 3 prévue, dans les délais
prévus, à des conditions raisonnables, ou du tout — le démarrage
« 1er semestre 2027 » est donc explicitement conditionné à
l'approvisionnement, pas seulement au calendrier.**

Une annonce d'essai n'est pas une preuve d'efficacité : le chiffre
de 82 % reste celui d'une étude de phase 1/2 non randomisée, n=22,
sans survie globale, et seule la phase 3 randomisée pourra le
confirmer ou l'infirmer.

---

## 0. Rappel — la référence (§8.80, vérifié le matin même)

- TNG462-C102 (NCT06922591), phase 1/2, patients MTAP-délétés /
  RAS-mutés, 2e et 3e ligne, PDAC métastatique : **ORR 82 %
  (18/22)**, DCR 100 %, PFS médiane non atteinte, suivi médian
  7,1 mois, coupure des données 20 août 2026 (ESMO 2026, poster
  3149P, Spira et al.).
- Phase 3 : mondiale, randomisée 1:1, première ligne, PDAC
  MTAP-délété, vopimetostat 200 mg + daraxonrasib 100 mg 1×/jour
  contre chimiothérapie standard, doubles critères principaux ORR
  et PFS, survie globale en critère secondaire clé, démarrage
  prévu 1er semestre 2027, **sans numéro NCT** (Tango, 9 nov.
  2026).
- Rationnel DepMap mesuré ici : effet PRMT5 suit MTAP, pas
  CDKN2A (§8.28/§8.29/§8.40 ; PRMT5 Chronos −1,385 MTAP-délété
  vs −1,010 intact, p=0,0036, 4 confirmations).

## 1. La phase 3 vopimetostat + daraxonrasib : toujours pas enregistrée

### 1.1 Interrogation directe de ClinicalTrials.gov (nouveauté méthodologique)

Le §8.80 §7 déclarait ne pas avoir eu d'accès direct exhaustif
au registre. Ce chantier l'a fait, par l'API v2, le 21 nov. 2026
(reçus conservés, voir `PROVENANCE_892.md`) :

- Requête `vopimetostat` : **exactement 2 études** —
  NCT07897734 (TNG462-C103, déjà au §8.80) et NCT07938463
  (TAP-ALK, §2 ci-dessous). **Aucune phase 3 de la combinaison.**
- Requête `daraxonrasib` : **16 études**, dont RASolute 302
  (NCT06625320), RASolute 303 (NCT07491445), RASolute 304
  (NCT07252232), MountainTAP-5 (NCT07492680) et l'accès élargi
  (NCT07573215). **Aucune n'est la phase 3 vopimetostat +
  daraxonrasib.**
- Requête `TNG462-C102` : **1 étude**, NCT06922591, la phase 1/2
  de la combinaison elle-même (voir §1.2).

**Conclusion : au 21 novembre 2026, ~12h00 EST, la phase 3
vopimetostat + daraxonrasib n'est enregistrée nulle part sur
ClinicalTrials.gov.** La lacune méthodologique du §8.80 est
ainsi comblée pour cette question : ce n'est plus une absence
constatée dans les communiqués, c'est une absence constatée dans
le registre lui-même.

### 1.2 TNG462-C102 (NCT06922591) : aucune nouvelle coupe de données

Fiche ClinicalTrials.gov lue en direct (reçu
`ctg_NCT06922591_892.json`, SHA `d53ad88b…3b7e7`) :

- Statut : **RECRUITING**. Première publication : 10 avril 2025.
  **Dernière mise à jour : 23 octobre 2026** (jour du communiqué
  ESMO). Début : 31 mai 2025. Fin primaire estimée : juin 2027.
  Effectif estimé : 183. **Aucun résultat publié sur le registre.**
- Aucune mise à jour du registre depuis le 23 octobre 2026, donc
  **aucune nouvelle coupe de données** : les chiffres restent ceux
  de la coupure du 20 août 2026 (ORR 82 %, 18/22 ; PFS médiane
  non atteinte ; suivi médian 7,1 mois). Aucune PFS médiane
  atteinte, aucune donnée de survie globale, aucun nouveau signal
  de tolérance.
- **SITC 2026 (7–9 nov. 2026) : aucune présentation sur la
  combinaison trouvée** (re-vérifié dans ce chantier ; confirme
  le §8.80).

## 2. Fait nouveau (1) — nouvel essai vopimetostat enregistré : TAP-ALK, NCT07938463

**Nouveau pour le livre blanc, daté du 16 novembre 2026** (donc
antérieur à la vérification du §8.80, mais absent du §8.80 — le
registre n'avait pas été interrogé directement ce matin-là).

- **NCT07938463**, « Lorlatinib Plus TNG462 in ALK+ MTAP Del
  NSCLC » (TAP-ALK) : étude de phase 1/2, promue par le
  **Dana-Farber Cancer Institute** (investigatrice principale :
  Alice Shaw, MD), en collaboration avec Tango Therapeutics.
- **Vopimetostat (TNG462) + lorlatinib** chez des patients
  atteints de cancer du poumon non à petites cellules (CBNPC)
  **MTAP-délété et ALK-réarrangé**, après progression sous
  inhibiteur de tyrosine kinase. 30 participants prévus.
- Statut : **NOT_YET_RECRUITING**. Première publication sur le
  registre : **16 novembre 2026**. Début estimé : 30 avril 2027.
  Fin primaire estimée : novembre 2027.
- Source : fiche ClinicalTrials.gov, lue en direct, reçu
  `ctg_NCT07938463_892.json`, SHA `13d56de2…60bf1` ;
  https://clinicaltrials.gov/study/NCT07938463
- **Portée :** c'est une nouvelle combinaison PRMT5 + inhibiteur
  ciblé, dans le poumon, pas dans le pancréas, et pas avec
  daraxonrasib. Elle ne concerne pas la phase 3 pancréatique,
  ne change pas le rationnel MTAP/PRMT5, et ne fournit aucune
  donnée d'efficacité — c'est un enregistrement, pas un résultat.
  Elle montre en revanche que le champ d'emploi de vopimetostat
  continue de s'élargir au-delà du pancréas.

## 3. Fait nouveau (2) — le 10-Q de Tango : l'approvisionnement en daraxonrasib pour la phase 3 n'est pas assuré

**Nouveau pour le livre blanc, daté du 9 novembre 2026** (le
communiqué T3 du même jour était au §8.80 ; le contenu du 10-Q,
lui, n'y était pas).

Formulaire 10-Q de Tango Therapeutics, trimestre clos le 30
septembre 2026, déposé le 9 novembre 2026, lu ici à la source
primaire (SEC, accession 0001193125-26-452634, document
`tngx-20260930.htm`), extrait conservé
(`tango_10q_supply_excerpt_892.txt`, SHA `e229daaf…82ed7466`),
cité verbatim (section Risk Factors) :

> « While we are pursuing multiple pathways to obtain clinical
> supply of daraxonrasib for the planned trial, there is no
> assurance that we will be able to secure clinical supply of
> daraxonrasib on our anticipated timeline, on commercially
> reasonable terms, or at all. »

Traduction : « Bien que nous poursuivions plusieurs voies pour
obtenir l'approvisionnement clinique en daraxonrasib pour l'essai
prévu, rien ne garantit que nous puissions obtenir cet
approvisionnement dans les délais prévus, à des conditions
commercialement raisonnables, ou du tout. »

Le même 10-Q confirme le plan de phase 3 (randomisation 1:1,
vopimetostat 200 mg + daraxonrasib 100 mg 1×/jour contre
chimiothérapie standard, doubles critères ORR/PFS, OS secondaire
clé, démarrage 1er semestre 2027) et le projet d'essai MTAP
wild-type (~25 patients, 1er semestre 2027) — faits déjà au §8.80
via le communiqué, confirmés ici à la source primaire.

**Portée :**

- Ce n'est pas une donnée d'efficacité et cela ne change rien au
  rationnel MTAP/PRMT5 mesuré ici. C'est un **risque de
  calendrier** : le démarrage « 1er semestre 2027 » dépend
  explicitement de l'obtention de l'approvisionnement clinique
  en daraxonrasib — un médicament dont Tango n'est pas le
  promoteur (Revolution Medicines en détient l'approvisionnement
  et les essais d'enregistrement propres ; l'accord de
  collaboration et de fourniture de novembre 2024 couvre les
  essais de combinaison en cours, la fourniture pour la phase 3
  restant à sécuriser).
- La prochaine vérification utile reste la même : l'apparition
  d'un numéro NCT pour la phase 3 et/ou l'annonce du premier
  patient randomisé — avec désormais un jalon intermédiaire à
  surveiller : toute annonce de sécurisation (ou non) de
  l'approvisionnement.

## 4. Le reste du champ : rien de nouveau depuis le §8.80

- **Vopimetostat + ERAS-0015 (TNG462-C103, NCT07897734)** :
  première publication 27 octobre 2026, NOT_YET_RECRUITING,
  début estimé novembre 2026 — déjà au §8.80, aucune donnée.
- **MountainTAP-5 (NCT07492680, navlimetostat + daraxonrasib)** :
  en recrutement, aucune donnée — déjà au §8.80.
- **Daraxonrasib seul** : aucune nouvelle donnée RASolute 303 /
  304 depuis le §8.80 (le point du 4 nov. 2026 et les données ENA
  du 19 nov. 2026 y sont déjà).
- **Recherche web générale** (21 nov. 2026) : aucune annonce
  postérieure au 9 novembre 2026 sur la combinaison ; les
  reprises du 9–13 novembre (Morningstar, Readthrough, VigiEye,
  WhyMyStockMoved, FrontierPicks) ne font que relayer le
  communiqué T3 et le 10-Q.

## 5. Ce que cela change — et ne change pas — pour le rationnel MTAP/PRMT5

### 5.1 Ce qui ne change pas

- **Le rationnel DepMap mesuré ici est intact** : l'effet PRMT5
  suit MTAP, pas CDKN2A (§8.28/§8.29/§8.40 ; 4 confirmations ;
  PRMT5 Chronos −1,385 MTAP-délété vs −1,010 intact, p=0,0036).
  **Aucun fait nouveau de cette vérification ne le contredit.**
- **Le chiffre clinique central est inchangé** : ORR 82 % (18/22),
  DCR 100 %, PFS médiane non atteinte, n=22, non randomisé, sans
  OS. Il n'a été ni confirmé sur un plus grand effectif, ni
  infirmé.
- **La phase 3 reste le test décisif**, et son design (1:1 contre
  chimiothérapie, doubles critères ORR/PFS, OS secondaire clé)
  reste celui qu'une confirmation exigerait.

### 5.2 Ce qui change — ou se précise

1. **L'absence de numéro NCT est désormais établie par le
   registre lui-même**, pas seulement par les communiqués : la
   limite méthodologique du §8.80 §7 est levée pour cette
   question (interrogation directe de l'API v2, 2 études
   vopimetostat, 16 études daraxonrasib, aucune phase 3 de la
   combinaison).
2. **Le calendrier « 1er semestre 2027 » est explicitement
   conditionné à l'approvisionnement** (10-Q, 9 nov. 2026) : ce
   n'est plus seulement une intention d'entreprise, c'est une
   intention assortie d'un risque déclaré par l'entreprise
   elle-même. Un glissement de ce calendrier ne serait pas une
   surprise — il est annoncé comme possible.
3. **Le champ vopimetostat s'élargit encore** (TAP-ALK, poumon
   ALK+ MTAP-délété) : troisième famille de combinaisons
   vopimetostat en développement clinique (après RAS(ON) et
   ERAS-0015), toujours sans donnée d'efficacité.

## 6. Ce qui reste ouvert — jalons à vérifier (mise à jour du §8.80 §6)

| Jalon | Échéance annoncée | Source | Statut au 21 nov. 2026, ~12h00 EST |
|---|---|---|---|
| Phase 3 vopimetostat + daraxonrasib : numéro NCT, premier patient | 1er semestre 2027 | Tango, 9 nov. 2026 ; 10-Q, 9 nov. 2026 | Non démarrée, pas de NCT ; approvisionnement non sécurisé (risque déclaré) |
| Phase 3 : discussion d'une voie d'approbation accélérée en 2e ligne | Non datée | Tango, 9 nov. 2026 | Discussion prévue, rien de déposé |
| Phase 1/2 vopimetostat + pan-RAS, PDAC MTAP wild-type (~25 pts, 2e ligne) | 1er semestre 2027 | Tango, 9 nov. 2026 | Prévue, pas de NCT publié |
| Vopimetostat + ERAS-0015 (NCT07897734) : premières données | Non datée | Tango/Erasca, 4 nov. 2026 | Recrutement non encore démarré, aucune donnée |
| MountainTAP-5, cohortes navlimetostat + daraxonrasib (NCT07492680) : premières données | Non datée | BMS / registre | En recrutement, aucune donnée |
| TAP-ALK, vopimetostat + lorlatinib (NCT07938463) : premières données | Non datée | Dana-Farber / registre, 16 nov. 2026 | Non encore en recrutement, aucune donnée |
| Vopimetostat monothérapie poumon + TNG456 : données | Janvier 2027 | Tango, 9 nov. 2026 | En attente |
| RASolute 303 : fin du recrutement mondial | 1er semestre 2027 | Revolution Medicines, 4 nov. 2026 | Recrutement US terminé |
| RASolute 304 (adjuvant) : données | Non datée | Revolution Medicines, 4 nov. 2026 | En cours, aucune donnée |
| Nouvelle coupe de données TNG462-C102 (vopimetostat + daraxonrasib) : PFS médiane ? OS ? | Non datée | — | Aucune annoncée ; dernière màj du registre : 23 oct. 2026 |

## 7. Limites de cette vérification

- **Fenêtre très courte** : quelques heures séparent cette
  vérification de celle du §8.80 (même jour, 21 nov. 2026).
  L'absence de nouveauté sur la combinaison dans cette fenêtre
  est un fait de calendrier autant qu'un fait de fond — la valeur
  ajoutée de ce chantier est l'interrogation directe du registre
  et la lecture du 10-Q à la source primaire, pas une fenêtre plus
  longue.
- **Aucune donnée mesurée ici** : cette section est une veille
  documentaire. Les seuls chiffres mesurés dans ce projet
  restent ceux des §8.28/§8.29/§8.40 (DepMap).
- **Sources secondaires** : pour les reprises du communiqué T3
  (Morningstar, Readthrough, VigiEye, WhyMyStockMoved,
  FrontierPicks), les faits retenus comme nouveaux (TAP-ALK,
  avertissement d'approvisionnement) ont été vérifiés à la source
  primaire (fiche ClinicalTrials.gov ; 10-Q SEC) avant d'être
  rapportés.

## 8. Sécurité — rappel

Cette section rapporte des données d'essais cliniques publiées.
Elle ne contient **aucune recommandation clinique**. Le livre
blanc n'est pas un conseil médical : toute question de traitement
se discute avec un oncologue.

---

*Fin de la section §8.92. Prochaine vérification proposée : à
l'apparition d'un numéro NCT pour la phase 3 vopimetostat +
daraxonrasib, ou à la prochaine donnée TNG462-C102, ou au plus
tard à la fin du 1er semestre 2027.*
