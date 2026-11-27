# Revue des thérapies ciblées MUC16 (CA125) et CLDN18.2 dans le cancer du pancréas

**Projet :** PDAC v6 — livre blanc, revue de littérature (brouillon)
**Date de rédaction :** 16 novembre 2026
**Auteur :** TagPrint (agent), à la demande de Zackary Drasse-Ménard
**Méthode :** recherche web (browser.search / browser.open) le 16 novembre 2026 ; chaque affirmation est rattachée à sa source nommée ci-dessous. Aucun identifiant NCT n'a été inventé : les NCT cités proviennent des pages ClinicalTrials.gov ou des articles/ communiqués cités ; quand un NCT n'a pas pu être vérifié, c'est écrit explicitement.
**Contexte projet :** dans le projet PDAC v6, CA125 (protéine MUC16) prédit une survie plus courte dans 2 cohortes sur 3 et est élevé chez les patients KRAS-les-plus-forts dans 3 cohortes sur 4 ; CLDN18 était un gène du projet. MUC16 et CLDN18.2 sont des protéines de surface, donc des cibles possibles d'anticorps / ADC / CAR-T. Cette revue vérifie s'il existe des preuves thérapeutiques dans le pancréas spécifiquement.
**Règle d'or appliquée :** un médicament approuvé dans un autre cancer (gastrique, ovarien) n'est PAS une preuve pour le pancréas. Les approbations gastriques/ovariennes sont signalées comme telles et jamais présentées comme des preuves pancréatiques.

---

## Verdict (d'abord)

**MUC16 / CA125 — NON, pas de piste médicamenteuse réelle pour le pancréas à ce jour.**
Le seul ADC anti-MUC16 testé chez des patients pancréatiques (sofituzumab védotine / DMUC5754A, phase I, 11 patients pancréatiques) n'a produit **aucune réponse confirmée chez ces 11 patients** — toutes les réponses étaient ovariennes. Le second ADC (DMUC4064A) n'a **jamais reçu un seul patient pancréatique** : le programme a été arrêté par le sponsor avant l'enrôlement pancréatique. Les CAR-T anti-MUC16CD ne sont que **précliniques** pour le pancréas (souris, 2024) ; en clinique humaine, elles n'ont été testées que dans l'ovaire, avec comme meilleure réponse une maladie stable. Les anticorps anti-CA125 de première génération (oregovomab, abagovomab) ont **échoué en phase III** dans l'ovaire et n'ont jamais été testés dans le pancréas. MUC16 reste une cible biologiquement plausible (forte expression, survie plus courte), mais il n'existe **aucune preuve d'efficacité chez un patient pancréatique** pour aucune thérapie anti-MUC16.

**CLDN18.2 — OUI, une piste réelle, mais précoce et non prouvée en survie.**
C'est la cible la plus avancée des deux pour le pancréas — et c'est aussi celle dont le médicament le plus avancé vient d'échouer :
- **Zolbetuximab (anticorps nu, approuvé en gastrique en oct. 2024) a ÉCHOUÉ dans le pancréas :** l'essai randomisé de phase II GLEAM (n = 393, NCT03816163) n'a pas atteint son critère principal de survie globale (annonce Astellas, 14 oct. 2025) et Astellas a **arrêté le programme pancréatique en déc. 2025**.
- **Mais les modalités plus puissantes montrent des signaux d'activité pancréatique réels, en phase I/II, bras uniques, petits effectifs :** l'ADC **IBI343** (phase I, NCT05458219, 83 patients pancréatiques : réponse confirmée 22,7 %, survie médiane 9,1 mois à 6 mg/kg) est passé en **phase III pancréatique** (G-HOPE-002, NCT07066098, en recrutement) ; le CAR-T **satri-cel / CT041** (phase Ib, NCT04404595 : réponse 16,7 % dans le pancréas) ; le bispécifique **IBI389** (phase I, NCT05164458 : réponse 29,6 % dans le pancréas). Aucun de ces trois n'a encore démontré de bénéfice de survie dans un essai randomisé pancréatique.
- **Conclusion CLDN18.2 :** piste réelle et active (une phase III en cours), mais **aucun remède démontré** : les signaux viennent d'essais précoces non randomisés, et l'anticorps nu a échoué. La prévalence limite aussi la portée : seuls ~28 % des patients pancréatiques métastatiques ont une expression CLDN18.2 forte (≥ 75 % des cellules tumorales) selon le dépistage de GLEAM.

**En une phrase :** derrière MUC16, rien de clinique pour le pancréas ; derrière CLDN18.2, des signaux précoces réels (IBI343 en phase III) mais un échec randomisé (zolbetuximab/GLEAM) qui rappelle qu'une cible de surface n'est pas un remède.

---

## 1. MUC16 (CA125)

### 1.1 Contexte biologique (pourquoi la cible est plausible)

- MUC16 est une grande mucine transmembranaire ; son domaine clivé et libéré dans le sang est le CA125, biomarqueur sérique classique du cancer de l'ovaire. Le domaine retenu à la membrane après clivage (Muc16CD) reste à la surface de la cellule tumorale et c'est lui que ciblent les ADC et CAR-T modernes — les premiers anticorps ciblaient le CA125 circulant, ce qui est une des explications avancées de leurs échecs (l'anticorps est capté par le CA125 soluble avant d'atteindre la tumeur).
  - Source : Chekmasova et al., résumés précliniques ; Lin et al. 2024 (voir §1.4) ; D. et al., « Understanding the Unique Attributes of MUC16 (CA125) », *Cancer Research* 2015 ;75(22):4669–4674.
- Dans le pancréas : expression de MUC16 significativement plus élevée dans les tumeurs que dans le pancréas normal (TCGA), et les patients à forte expression MUC16 ont une survie globale significativement plus courte.
  - Source : Lin H.K. et al., « Muc16CD is a novel CAR T cell target antigen for the treatment of pancreatic cancer », *Molecular Therapy — Oncolytics* 2024 ;32(4):200868. DOI 10.1016/j.omton.2024.200868 ; PMCID PMC11426034, PMID 39346763.
- MUC16 est aussi exprimé dans une proportion importante d'adénocarcinomes pancréatiques, mais moins que dans l'ovaire (Lin et al. 2024, analyse TCGA et Human Protein Atlas).

### 1.2 Sofituzumab védotine / DMUC5754A (RG7458) — ADC anti-MUC16, MMAE

- **Nature :** ADC : anticorps monoclonal humanisé IgG1 anti-MUC16 (hu3A5 / sofituzumab) conjugué à la monométhyl auristatine E (MMAE, poison des microtubules) par un linker clivable par protéase. Développé par Genentech.
- **Stade :** phase I terminée ; **aucun développement ultérieur trouvé** (pas de phase II/III, pas d'approbation). Programme arrêté (pas de communiqué de fin trouvé ; le fait est qu'aucun essai ultérieur n'existe dans les sources consultées).
- **Preuves pancréas — c'est le SEUL anti-MUC16 testé chez des patients pancréatiques, et le résultat pancréatique est négatif :**
  - Essai de phase I, dose-escalation : **66 patientes avec cancer de l'ovaire platine-résistant et 11 patients avec cancer du pancréas non résécable**, DMUC5754A toutes les 3 semaines (0,3–3,2 mg/kg) ou hebdomadaire (0,8–1,6 mg/kg). Dose recommandée phase II : 2,4 mg/kg toutes les 3 semaines.
  - **Réponses confirmées : 1 réponse complète + 6 réponses partielles — toutes chez des patientes ovariennes** à tumeurs MUC16-positives en immunohistochimie (2+ ou 3+). **Aucune réponse confirmée rapportée chez les 11 patients pancréatiques.** Six patientes ovariennes supplémentaires ont eu une maladie stable > 6 mois.
  - Toxicité : fatigue, neuropathie périphérique, nausées, baisse d'appétit, vomissements, diarrhée, alopécie, fièvre ; neutropénie de grade ≥ 3 chez 9 % (schéma toutes les 3 semaines) et 17 % (hebdomadaire) ; un cas de syndrome d'encéphalopathie postérieure réversible (PRES), réversible après arrêt. Pas de signal de toxicité oculaire.
  - Source : Liu J.F. et al., « Phase I study of safety and pharmacokinetics of the anti-MUC16 antibody-drug conjugate DMUC5754A in patients with platinum-resistant ovarian cancer or unresectable pancreatic cancer », *Annals of Oncology* 2016 ;27(11):2124–2130. DOI 10.1093/annonc/mdw401. **NCT01335958.**
  - Synthèse secondaire concordante : Wang et al., « A review of recent advances on single use of antibody-drug conjugates… », *Frontiers in Pharmacology* 2022 ;13:1093666 ; et « Emerging role of mucins in antibody drug conjugates for ovarian cancer therapy », *Journal of Ovarian Research* 2024 ;17:161 (qui précise : « PaC patients did not respond as well (NCT01335958) »).

### 1.3 DMUC4064A (RG7882) — ADC anti-MUC16 de 2e génération (THIOMAB)

- **Nature :** même anticorps anti-MUC16, conjugué MMAE par technologie THIOMAB (conjugaison site-spécifique, ratio médicament/anticorps homogène). Genentech.
- **Stade :** phase I terminée (ovaire uniquement) ; **programme arrêté par le sponsor. Zéro patient pancréatique.**
- **Preuves pancréas — aucune, et c'est documenté comme tel :** l'article de phase I indique noir sur blanc : « Patients with pancreatic cancer were also planned to be enrolled, but the study was halted prior to enrollment of any pancreatic patients due to the Sponsor's decision to discontinue the development of the DMUC4064A molecule and not due to any safety concerns. » (les patients pancréatiques devaient être enrôlés, mais l'étude a été arrêtée avant l'enrôlement d'un seul patient pancréatique, par décision du sponsor d'arrêter le développement de la molécule, et non pour des raisons de sécurité).
  - Résultats ovariens (pour mémoire, pas une preuve pancréatique) : 65 patientes, ovaire platine-résistant, 1,0–5,6 mg/kg toutes les 3 semaines, dose recommandée 5,2 mg/kg ; 25 % de réponses objectives confirmées (16/65), bénéfice clinique 42 %, survie sans progression médiane 3,9 mois ; toxicités oculaires chez 40 % des patientes (vision floue notamment), toxicités de grade ≥ 3 liées chez 25 %.
  - Une base de données industrielle (Synapse / PatSnap) classe le produit « Highest Phase: Suspended Phase 1 » ; un dirigeant de Whitehawk Therapeutics (fév. 2026) a déclaré que le programme avait été arrêté en raison de son profil de sécurité (toxicités oculaires et autres) — à noter : cette explication par la toxicité contredit la raison officielle donnée dans l'article (décision du sponsor, « not due to any safety concerns »). Les deux versions sont rapportées ici sans trancher.
  - Source : Liu J.F. et al., « An open-label phase I dose-escalation study of the safety and pharmacokinetics of DMUC4064A in patients with platinum-resistant ovarian cancer », *Gynecologic Oncology* 2021. **NCT02146313.** (Article lu en texte intégral le 16 nov. 2026.)

### 1.4 CAR-T anti-MUC16CD (4H11) — préclinique pancréas, phase I ovaire

- **Nature :** CAR-T de 2e génération ciblant le domaine ectodomaine retenu Muc16CD, scFv dérivé de l'anticorps 4H11, domaine costimulateur CD28. Versions armées : sécrétion d'IL-12 (ovaire) ; version « blindée » anti-VIP (pancréas, préclinique).
- **Stade pancréas : préclinique uniquement. Aucun essai clinique pancréatique trouvé.**
- **Preuves pancréas (précliniques, 2024) :**
  - Lin H.K., Blake D.A., Liu T. et al. (Rafiq, Emory University), *Molecular Therapy — Oncolytics* 2024 ;32(4):200868 : expression endogène de Muc16CD démontrée dans des tumeurs pancréatiques dérivées de patients (xénogreffes PDX) et dans les lignées HPAC et PANCII ; les CAR-T anti-Muc16CD reconnaissent et tuent ces cellules in vitro (cytotoxicité dose-dépendante, sécrétion d'IL-2, IFN-γ, TNF-α, granzyme B) ; in vivo, chez des souris SCID/beige porteuses de tumeurs Panc1 modifiées pour exprimer Muc16CD, une dose unique intrapéritonéale de CAR-T améliore significativement le contrôle tumoral et la survie. Les auteurs le présentent explicitement comme une preuve de concept, pas comme une preuve clinique.
  - Lin H.K. et al., résumé ASCO 2024 (J Clin Oncol 2024 ;42(16_suppl):2558) : CAR-T anti-Muc16CD « blindée » antagonisant les récepteurs du VIP (CAR/VIPRa) : dans un modèle PDX pancréatique chez la souris, réduction significative du fardeau tumoral là où les CAR-T classiques sont inefficaces. Préclinique uniquement.
- **Preuves humaines — ovaire seulement, efficacité limitée :**
  - Phase I (Memorial Sloan Kettering, Brentjens et coll.) : CAR-T anti-MUC16ecto sécrétant de l'IL-12, administration intraveineuse et intrapéritonéale, **18 patientes lourdement prétraitées** (ovaire, trompe, péritoine) : **meilleure réponse observée = maladie stable, aucune réponse objective** ; persistance des CAR-T dans le sang ; 2 des 3 patientes du cohort avec chimiothérapie de lymphodéplétion ont eu une toxicité dose-limitante (syndrome de type activation macrophagique), cohort fermée.
  - Source : O'Cearbhaill R.E. et al., résumé, *Gynecologic Oncology* 2020 ;159:42 ; cité et résumé dans « Dual targeting ovarian cancer by Muc16 CAR T cells… », *Cancer Immunology, Immunotherapy* 2023 ;72(11):3773–3786, et dans « The Landscape of Adoptive Cellular Therapies in Ovarian Cancer » (revue). **Le numéro NCT de cet essai de phase I n'a pas pu être vérifié dans les sources consultées — il n'est pas cité ici.** Un essai de suite est signalé comme en recrutement dans la revue : **NCT03907527** (cohorte ovaire platine-résistant, ~71 patientes prévues) — statut non vérifié indépendamment.
  - Anixa Biosciences / Moffitt (CAR-T ovarienne anti-MUC16, « lira-cel ») : phase I en cours, 5e cohorte terminée fin 2026, aucune toxicité dose-limitante signalée, 4 patientes survivantes à plus d'un an — communiqué d'entreprise, ovaire uniquement, pas de preuve pancréatique.
- **Autres CAR-T MUC16 en développement :** version sécrétant un BiTE anti-WT1 (préclinique ovaire, 2023) ; aucune donnée pancréatique trouvée.

### 1.5 Anticorps bispécifiques anti-MUC16

- **Ubamatamab (REGN4018, MUC16 × CD3, Regeneron)** — phase I/II, **ovaire uniquement** dans les données trouvées : chez 11 patientes avec cancer séreux de bas grade récurrent à la dose de 800 mg, taux de réponse objective confirmée 72,7 %, durée médiane de réponse 9 mois, survie sans progression médiane 11,1 mois ; syndrome de libération de cytokines surtout grade 1–2. **NCT03564340.** Aucune donnée pancréatique trouvée.
  - Source : Van Nieuwenhuysen E., présentation IGCS 2026, relayée par OncLive, 23 oct. 2026.
- **REGN5668 (MUC16 × CD28)** — phase I/II, tumeurs gynécologiques, NCT04590326 (signalé dans une revue systématique des essais gynécologiques, *Frontiers in Medicine* 2025). Aucune donnée pancréatique trouvée.
- **IMV-M (bispécifique anti-MUC16 / anti-DR5)** — **préclinique uniquement** : régression tumorale prononcée après une injection unique dans des xénogreffes de la lignée d'adénocarcinome pancréatique HPAC chez la souris (5 mg/kg, et activité dès 1 mg/kg) ; pas de toxicité dans une étude pilote chez le primate non humain. Aucun essai clinique.
  - Source : « A bispecific anti-MUC16/anti-death receptor 5 antibody… », *Scientific Reports* 2025 ;15:9909. DOI 10.1038/s41598-025-93927-0.

### 1.6 Anticorps anti-CA125 de première génération et vaccins — échecs de phase III (ovaire)

- **Oregovomab** (anticorps murin modifié anti-CA125, Mab B43.13) : phase II encourageante (réponses immunitaires chez 58 %, stabilisation chez 23 %), puis **échec en phase III** en maintenance après rémission complète : temps médian jusqu'à rechute 10,3 mois vs 12,9 mois placebo (p = 0,29) ; survie médiane 57,5 vs 48,6 mois, non significatif (HR 0,72 ; IC 95 % 0,41–1,25). Un essai de phase III en association concomitante à la chimiothérapie (FLORA-5, **NCT04498117**) était en cours. **Aucune étude pancréatique trouvée.**
  - Sources : Berek J.S. et al., *J Clin Oncol* 2009 ;27:418–425 ; résumé dans « Virus-like particle vaccine displaying an external, membrane adjacent MUC16 epitope… », *Journal of Ovarian Research* 2023.
- **Abagovomab** (vaccin anti-idiotype anti-CA125) : **échec de la phase III pivot MIMOSA** (n international, ovaire avancé en rémission) : aucun bénéfice en survie sans progression ni en survie globale.
  - Source : Sabbatini P. et al., « Abagovomab as maintenance therapy in patients with epithelial ovarian cancer: a phase III trial… — the MIMOSA study », *J Clin Oncol* 2013 ;31(12):1554–1561.
- **Leçon documentée :** ces anticorps ciblaient le CA125 circulant (domaine clivé) et n'atteignaient probablement pas les cellules tumorales — d'où le passage aux cibles Muc16CD retenues à la membrane. Source : « Understanding the Unique Attributes of MUC16 (CA125) », *Cancer Research* 2015 (voir §1.1).

### 1.7 Nouveaux ADC anti-MUC16 (sans données pancréatiques)

- **HWK-016 (Whitehawk Therapeutics)** : ADC anti-MUC16, IND déposée déc. 2025, phase I en recrutement en 2026, focus initial ovaire et endomètre ; le pancréas est cité par l'entreprise comme « potentiel d'expansion » futur, sans aucune donnée. Source : transcription d'appel résultats Whitehawk, fév. 2026 (source entreprise, à prendre comme déclaration, pas comme preuve).

### 1.8 Tableau récapitulatif MUC16

| Thérapie | Modalité | Stade global | Patients pancréatiques testés ? | Résultat pancréas |
|---|---|---|---|---|
| Sofituzumab védotine (DMUC5754A) | ADC MMAE | Phase I terminée, arrêté | Oui, 11 (NCT01335958) | 0 réponse confirmée ; réponses toutes ovariennes |
| DMUC4064A | ADC MMAE (THIOMAB) | Phase I ovaire, programme arrêté | Non, 0 (arrêt avant enrôlement pancréatique) | Aucune donnée |
| CAR-T anti-Muc16CD (4H11) | CAR-T | Préclinique (pancréas) ; phase I (ovaire) | Non (humain) ; souris oui | Preuve de concept souris 2024 ; ovaire humain : maladie stable au mieux |
| CAR-T anti-Muc16CD + anti-VIP | CAR-T blindée | Préclinique | Souris (PDX) oui | Réduction tumorale souris (ASCO 2024) |
| IMV-M (MUC16 × DR5) | Bispécifique | Préclinique | Souris (HPAC) oui | Régression xénogreffe HPAC |
| Ubamatamab (MUC16 × CD3) | Bispécifique | Phase I/II ovaire | Non | Aucune donnée (ovaire : ORR 72,7 % en bas grade, n=11) |
| Oregovomab | Anticorps anti-CA125 | Phase III ovaire : échec | Non | Aucune donnée |
| Abagovomab | Vaccin anti-idiotype | Phase III MIMOSA : échec | Non | Aucune donnée |
| HWK-016 | ADC | Phase I (2026, gynéco) | Non | Aucune donnée |

---

## 2. CLDN18.2

### 2.1 Contexte biologique et prévalence dans le pancréas

- CLDN18.2 est l'isoforme 2 de la claudine 18, protéine de jonction serrée normalement restreinte à la muqueuse gastrique, exprimée de façon aberrante dans les cancers gastriques, pancréatiques et œsophagiens.
- Prévalence dans l'adénocarcinome pancréatique (PDAC) : les chiffres dépendent du seuil. Environ **30 % des PDAC** ont une expression forte selon les grandes séries immunohistochimiques (revue *Frontiers in Oncology* 2026) ; **59,2 % des PDAC primitifs** sont positifs à un seuil quelconque (Xing et al., *Frontiers in Immunology* 2026) ; dans le dépistage de l'essai GLEAM, **27,7 %** des patients métastatiques avaient une expression CLDN18.2 dans ≥ 75 % des cellules tumorales (seuil d'éligibilité de l'essai) — soit environ 1 patient sur 4 éligible au critère strict.
  - Sources : « Resistance mechanisms and countermeasures in CLDN18.2-positive tumors », *Frontiers in Oncology* 2026 ;10.3389/fonc.2026.1910011 ; Xing Y. et al., *Frontiers in Immunology* 2026 ;16:1638585 ; communiqué Astellas, 14 oct. 2025 (GLEAM).

### 2.2 Zolbetuximab (Vyloy, IMAB362) — anticorps monoclonal anti-CLDN18.2

- **Nature :** anticorps monoclonal chimérique IgG1 anti-CLDN18.2 (ADCC/CDC). Astellas.
- **Stade global : APPROUVÉ en gastrique / jonction gastro-œsophagienne, ÉCHEC en pancréas.**
  - Approbations (gastrique/GEJ, HER2-négatif, CLDN18.2-positif, en 1re ligne avec chimiothérapie) : Japon (PMDA, mars 2024), Union européenne (sept. 2024), États-Unis (FDA, **18 oct. 2024**). Basées sur deux phases III randomisées :
    - **SPOTLIGHT (NCT03504397**, Shitara et al., *Lancet* 2023) : zolbetuximab + mFOLFOX6 vs placebo + mFOLFOX6, n = 565 ; survie globale médiane **18,2 vs 15,5 mois** (HR 0,75), survie sans progression 10,6 vs 8,7 mois.
    - **GLOW (NCT03653507**, Shah et al., *Nature Medicine* 2023) : zolbetuximab + CAPOX vs placebo + CAPOX, n = 507 ; survie globale médiane **14,4 vs 12,2 mois**.
  - **Ces deux approbations sont gastriques. Elles ne constituent pas une preuve pour le pancréas.**
- **Preuves pancréas — essai randomisé négatif, programme arrêté :**
  - **GLEAM (NCT03816163**, étude 8951-CL-5201) : phase II randomisée, ouverte, zolbetuximab + gemcitabine + nab-paclitaxel vs gemcitabine + nab-paclitaxel en 1re ligne, patients avec adénocarcinome pancréatique métastatique CLDN18.2-positif (≥ 75 % des cellules tumorales, coloration membranaire modérée à forte en IHC centrale), n = **393** patients, 136 centres (États-Unis, Europe, Asie, Australie), début mars 2019.
  - **Résultat (14 oct. 2025, communiqué Astellas) : l'essai n'a PAS atteint son critère principal de survie globale à l'analyse finale.** Le profil de sécurité de la combinaison était globalement cohérent avec les profils connus de chaque traitement. Aucun chiffre de survie n'a été publié dans ce communiqué ; Astellas a annoncé une évaluation complète des données et une diffusion ultérieure (critères secondaires, sous-groupes).
  - **Conséquence : Astellas a arrêté le programme de développement pancréatique de zolbetuximab à partir de déc. 2025** (mention portée sur les fiches ClinicalTrials.gov / Astellas : « Astellas is terminating the zolbetuximab pancreatic development program from Dec 2025 (following the final OS analysis in Oct 2025) » ; les patients sous traitement peuvent le poursuivre si l'investigateur juge qu'ils en bénéficient).
  - Sources : ClinicalTrials.gov NCT03816163 (fiche consultée le 16 nov. 2026, dernière mise à jour affichée 14 oct. 2026) ; communiqué Astellas, 14 oct. 2025, relayé par Drugs.com ; fiche Astellas clinicaltrials.astellas.com, étude 8951-CL-5201.

### 2.3 IBI343 (arcotatug tavatecan / TAK-921) — ADC anti-CLDN18.2, exatecan

- **Nature :** ADC : anticorps monoclonal humain anti-CLDN18.2 + exatécan (inhibiteur de topoisomérase I). Innovent Biologics (Takeda hors Grande Chine).
- **Stade : phase I pancréas avec signal d'activité ; phase III pancréatique en cours ; phase III gastrique en cours.**
- **Preuves pancréas — le signal clinique pancréatique le plus solide de cette revue (mais phase I, bras unique, non randomisé) :**
  - Étude de phase I/1b multi-régionale (Chine, Australie, États-Unis), **NCT05458219**, dose-escalation et expansion, patients avec PDAC avancé CLDN18.2-positif prétraités (≥ 1 ligne antérieure).
  - Données actualisées présentées à l'ASCO 2025 (Yu X. et al., *J Clin Oncol* 2025 ;43:4017) et communiquées par Innovent : au 14 mars 2025, **83 patients pancréatiques** traités, suivi médian 11,1 mois ; dans le groupe CLDN18.2 1+/2+/3+ ≥ 60 % à la dose de 6 mg/kg (n = 44) : **taux de réponse objective confirmée 22,7 %, taux de contrôle de la maladie 81,8 %, survie sans progression médiane 5,4 mois, survie globale médiane 9,1 mois** (12,1 mois chez les 17 patients n'ayant reçu qu'une seule ligne antérieure ; 9,1 mois chez les 18 patients à deux lignes). Données antérieures (ESMO Asia 2024, n = 43) : ORR confirmée 23,3 %, survie sans progression médiane 5,3 mois.
  - Sécurité : 98,8 % d'événements indésirables liés au traitement, les plus fréquents étant anémie et baisse des neutrophiles/leucocytes ; **aucune nausée/vomissement de grade ≥ 3** ; profil jugé favorable par le promoteur.
  - Distinctions réglementaires : Breakthrough Therapy Designation (NMPA, Chine) pour le PDAC avancé CLDN18.2-positif après ≥ 1 ligne ; Fast Track Designation (FDA, États-Unis).
  - **Phase III pancréatique en cours : G-HOPE-002 (NCT07066098)** — étude randomisée, double aveugle, IBI343 en monothérapie + meilleurs soins de support vs placebo + meilleurs soins de support, patients avec cancer du pancréas localement avancé non résécable ou métastatique CLDN18.2-positif ayant reçu ≥ 2 lignes antérieures, ~201 patients prévus, en recrutement (achèvement primaire estimé juin 2027 selon la revue *Frontiers in Oncology* 2026).
  - Sources : communiqué Innovent / PR Newswire Asia, ASCO 2025 ; Yu X. et al., *J Clin Oncol* 2025 ;43:4017 ; « Research advances in targeting claudin 18.2 in pancreatic ductal adenocarcinoma treatment », *World J Gastroenterol* 2026 ;32(45):122906 ; revue *Frontiers in Oncology* 2026 (tableau des essais, NCT07066098).

### 2.4 Satri-cel / CT041 (satricabtagene autoleucel) — CAR-T anti-CLDN18.2

- **Nature :** CAR-T autologue anti-CLDN18.2. CARsgen Therapeutics.
- **Stade : phase I/II ; phase II randomisée positive en gastrique (pas en pancréas) ; pas d'approbation à ce jour (demande d'enregistrement déposée en Chine en 2025 pour le gastrique).**
- **Preuves pancréas — activité modeste, petits effectifs :**
  - Étude internationale de phase Ib **ELIMYN18.2 (NCT04404595)** : ORR **16,7 % dans le pancréas** (vs 42,9 % en gastrique/GEJ), d'après la revue *Frontiers in Oncology* 2026 (qui cite l'essai). Étude de phase I CT041-CG4006 (**NCT03874897**) : sur 98 patients (tumeurs gastro-intestinales), ORR globale 38,8 %, survie sans progression médiane 4,4 mois, survie globale médiane 8,8 mois — chiffres globaux, non spécifiques au pancréas.
  - Étude adjuvante **CT041-ST-05** (phase Ib, Chine, présentée à l'ESMO 2025) : première exploration d'un CAR-T en adjuvant d'une tumeur solide — 6 patients avec PDAC CLDN18.2-positif réséqué, CA19-9 anormal après 3 mois de chimiothérapie adjuvante, sans signe de récidive ; suivi médian 6,05 mois après perfusion : **1 seule récidive ; survie sans maladie médiane et survie globale médiane non atteintes ; taux de survie sans maladie à 9 mois depuis la chirurgie : 83,3 %** ; baisse du CA19-9 chez 5 patients sur 6 (51,3 % à 96,1 %) ; syndrome de libération de cytokines grade 1–2 chez tous les patients. Effectif de 6 patients, suivi court, sans groupe contrôle — signal préliminaire uniquement.
  - Sécurité (général) : syndrome de libération de cytokines fréquent (~95 % dans les séries, surtout grade 1–2) ; toxicité gastrique sur cible (nausées/vomissements liés à l'expression normale de CLDN18.2 dans l'estomac).
  - **Preuve gastrique (à ne pas confondre avec une preuve pancréatique) :** essai randomisé de phase II **CT041-ST-01 (NCT04581473)**, 156 patients, gastrique/GEJ prétraités : survie sans progression médiane 3,25 mois vs 1,77 mois (HR 0,37, p < 0,0001) — première preuve randomisée d'efficacité d'un CAR-T dans une tumeur solide, mais en gastrique.
  - Sources : revue « CAR-T and CAR-NK cell therapy targets in gastrointestinal malignancies », *Frontiers in Oncology* 2026 ;10.3389/fonc.2026.1960663 ; communiqué CARsgen / M2 Pharma, 20 oct. 2025 (CT041-ST-05, ESMO 2025) ; Qi C. et al., *Nature Medicine* 2022 (CT041-CG4006, NCT03874897) via la revue ci-dessus ; Qi C., Liu C. et al., *Lancet* 2025 (CT041-ST-01, NCT04581473) via la revue ci-dessus.

### 2.5 AZD0901 / CMG901 (sonesitatug védotine) — ADC anti-CLDN18.2, MMAE

- **Nature :** ADC anti-CLDN18.2 + MMAE. KYM Biosciences (Keymed / Lepu) ; AstraZeneca.
- **Stade : phase II pancréas en cours, sans résultats publiés ; phase III gastrique en cours.**
- **Preuves pancréas — aucune donnée d'efficacité publiée à ce jour :**
  - Étude **CLARITY-PanTumour01 (NCT06219941)**, phase II, ouverte, multicentrique : sous-étude 1 = monothérapie en gastrique/GEJ ; **sous-étude 2 = AZD0901 en combinaison avec différentes chimiothérapies chez des patients avec cancer du pancréas (1re ligne)** ; sous-étude 3 = voies biliaires. Début déc. 2023, ~226 patients au total, achèvement primaire estimé nov. 2026. Aucun résultat pancréatique publié trouvé au 16 nov. 2026.
  - Données gastriques (pour mémoire) : ORR confirmée 28 % (32/113) en gastrique/GEJ prétraité (revue citée dans la recherche).
  - Phase III gastrique : CLARITY-Gastric 01 (**NCT06346392**).
  - Sources : ClinicalTrials.gov NCT06219941 ; revue *Frontiers in Oncology* 2026.

### 2.6 LM-302 (tecotabart védotine / TPX-4589) — ADC anti-CLDN18.2, MMAE

- **Nature :** ADC anti-CLDN18.2 + MMAE. LaNova Medicines (filiale de Sino Biopharmaceutical ; BioNTech a acquis LaNova en oct. 2023).
- **Stade : phase III gastrique ; phase II pancréas prévue / en démarrage, sans données.**
- **Preuves pancréas — aucune donnée :** étude de phase II **NCT07108504** (LM-302 + gemcitabine en 2e ligne, PDAC CLDN18.2-positif non résécable localement avancé ou métastatique, 30 patients prévus, promoteur : Shanghai Zhongshan Hospital, début août 2025) — statut « pas encore en recrutement » / en démarrage selon les sources consultées ; aucun résultat.
  - Phase III gastrique : NCT06351020 (2e ligne et au-delà) et NCT07385703 (1re ligne, + tislelizumab).
  - Sources : ClinicalTrials.gov via OnCo dossier CLDN18.2 (consulté le 16 nov. 2026) et ClinTrialFinder (nov. 2026) ; fiche NCT07108504 (PatLynk / DecenTrialz).

### 2.7 IBI389 — anticorps bispécifique CLDN18.2 × CD3

- **Nature :** bispécifique anti-CLDN18.2 / anti-CD3 (engageur de lymphocytes T). Innovent Biologics.
- **Stade : phase I, avec signal pancréatique précoce.**
- **Preuves pancréas (phase I, bras unique) :** étude **NCT05164458** ; au 11 mars 2024, **72 patients avec PDAC** avancé non résécable/métastatique traités ; 27 patients avec au moins une évaluation tumorale post-baseline : **ORR 29,6 %, ORR confirmée 25,9 %, taux de contrôle de la maladie 70,4 %** ; chez les 18 patients CLDN18.2 IHC 2/3+ ≥ 40 %, ORR confirmée 38,9 %. Survie sans progression médiane non mature au 1er mai 2024 (taux de survie sans progression à 3 mois : 57,1 %).
  - Source : communiqué Innovent / PR Newswire, ASCO 2024 (données au 11 mars 2024). Données de communiqué d'entreprise, pas d'article revu par les pairs trouvé pour ce bras pancréatique.

### 2.8 Autres anti-CLDN18.2 (pancréas : essais en cours, sans résultats)

- **CAR-T double cible mésothéline + CLDN18.2 (BAH2573-102, Essen Biotech)** : phase I/II, **NCT07066995**, 60 patients prévus, PDAC avancé/métastatique, deux perfusions séquentielles ; début avril 2025, achèvement primaire estimé déc. 2027. Aucun résultat. La fiche de l'essai mentionne que les CAR-T anti-CLDN18.2 ont donné des rémissions objectives (dont des complètes) dans le cancer du pancréas réfractaire dans des études antérieures — sans chiffres pancréatiques précis sur la fiche.
- **CAR-T anti-CLDN18.2 VHH (nanobody)** : préclinique pancréas (Xing Y. et al., *Frontiers in Immunology* 2026 ;16:1638585) — efficacité in vivo chez la souris ; pas d'essai clinique.
- **CAR-T anti-CLDN18.2 armées IP10 / IL-15** : préclinique souris (modèle Panc02-CLDN18.2) — survie améliorée, 3 souris sur 5 sans tumeur à J78 avec la double modification IP10+IL-15. *Frontiers in Immunology* 2026. Pas d'essai clinique.
- **Autres ADC / bispécifiques en phase I/II gastrique** (SHR-A1904, RC118, AZD4360, ASP2138, AZD5863…) : aucun résultat pancréatique trouvé ; non détaillés ici faute de preuves pancréatiques.

### 2.9 Tableau récapitulatif CLDN18.2

| Thérapie | Modalité | Stade global | Patients pancréatiques testés ? | Résultat pancréas |
|---|---|---|---|---|
| Zolbetuximab | Anticorps nu | **Approuvé gastrique/GEJ (FDA oct. 2024)** | Oui, 393 (GLEAM, NCT03816163) | **ÉCHEC : critère principal de survie globale non atteint (oct. 2025) ; programme pancréatique arrêté déc. 2025** |
| IBI343 | ADC exatécan | Phase I pancréas ; phase III pancréas en cours | Oui, 83 (NCT05458219) | ORR confirmée 22,7 %, DCR 81,8 %, SSP méd. 5,4 mois, SG méd. 9,1 mois (6 mg/kg) ; phase III G-HOPE-002 (NCT07066098) en recrutement |
| Satri-cel / CT041 | CAR-T | Phase I/II ; phase II randomisée positive en gastrique | Oui (NCT04404595 ; CT041-ST-05, n=6 adjuvant) | ORR 16,7 % (métastatique) ; adjuvant : 1 récidive / 6, DFS 9 mois 83,3 % (préliminaire) |
| AZD0901 / CMG901 | ADC MMAE | Phase II ; phase III gastrique | En cours (NCT06219941, sous-étude 2) | Aucun résultat publié |
| LM-302 | ADC MMAE | Phase III gastrique | Prévu (NCT07108504, 30 patients) | Aucun résultat |
| IBI389 | Bispécifique CD3 | Phase I | Oui, 72 (NCT05164458) | ORR 29,6 %, ORR confirmée 25,9 %, DCR 70,4 % (27 évaluables) |
| CAR-T MSLN + CLDN18.2 | CAR-T double cible | Phase I/II | En cours (NCT07066995) | Aucun résultat |
| CAR-T VHH / IP10+IL-15 | CAR-T | Préclinique | Souris oui | Efficacité souris uniquement |

---

## 3. Ce que cette revue ne permet pas de conclure

- **Aucune thérapie anti-MUC16 ou anti-CLDN18.2 n'est un remède démontré pour le cancer du pancréas.** La seule preuve randomisée de phase II/III en pancréas dans cette revue (zolbetuximab/GLEAM) est négative.
- **Les signaux positifs (IBI343, IBI389, satri-cel) viennent d'essais de phase I/II à bras unique, petits effectifs, sans groupe contrôle.** Un taux de réponse de ~23–30 % en phase I ne prédit pas un bénéfice de survie ; la phase III G-HOPE-002 (IBI343) est l'essai qui pourra le tester.
- **Les deux cibles ne couvrent qu'une fraction des patients :** CLDN18.2 fort (≥ 75 %) chez ~28 % des métastatiques ; MUC16 élevé chez une fraction importante mais variable selon les séries, et les ADC anti-MUC16 n'ont répondu que chez les patients MUC16-forts en ovaire.
- **Le statut pronostique (CA125 élevé = survie plus courte) ne prouve pas qu'inhiber la cible prolonge la survie.** C'est exactement la distinction entre un biomarqueur pronostique et une cible thérapeutique validée.
- **Limites de cette revue :** recherche web du 16 nov. 2026, sources secondaires incluses (communiqués d'entreprise pour IBI343/IBI389/satri-cel adjuvant ; revues 2026 pour certains chiffres) ; les articles de phase I cités ont été lus en résumé ou en texte intégral selon les cas (DMUC4064A lu en texte intégral ; Liu 2016 lu en résumé détaillé) ; les statuts d'essais « en recrutement » datent de nov. 2026 et peuvent changer ; aucun contact avec les promoteurs ; aucune donnée non publiée.

---

## 4. Sources (par ordre d'apparition)

1. Liu J.F. et al., *Ann Oncol* 2016 ;27(11):2124–2130. DOI 10.1093/annonc/mdw401 — DMUC5754A, NCT01335958. https://www.sciencedirect.com/ (résumé consulté via Mendeley / Annals of Oncology)
2. Liu J.F. et al., *Gynecol Oncol* 2021 — DMUC4064A, NCT02146313. https://www.gynecologiconcology-online.net/article/S0090-8258(21)01403-7/fulltext (texte intégral lu le 16 nov. 2026)
3. Lin H.K. et al., *Mol Ther Oncolytics* 2024 ;32(4):200868. DOI 10.1016/j.omton.2024.200868. https://pmc.ncbi.nlm.nih.gov/articles/PMC11426034/
4. Lin H.K. et al., *J Clin Oncol* 2024 ;42(16_suppl):2558 (résumé ASCO 2024, CAR/VIPRa).
5. O'Cearbhaill R.E. et al., *Gynecol Oncol* 2020 ;159:42 (résumé) — CAR-T MUC16 IL-12, 18 patientes, maladie stable au mieux. Cité dans : *Cancer Immunol Immunother* 2023 ;72(11):3773–3786. https://pmc.ncbi.nlm.nih.gov/articles/PMC10991175/
6. « The Landscape of Adoptive Cellular Therapies in Ovarian Cancer » (revue ; NCT03907527 signalé en recrutement).
7. « A bispecific anti-MUC16/anti-death receptor 5 antibody… », *Sci Rep* 2025 ;15:9909. DOI 10.1038/s41598-025-93927-0. https://pmc.ncbi.nlm.nih.gov/articles/PMC11929789/
8. Van Nieuwenhuysen E., IGCS 2026, ubamatamab, relayé par OncLive, 23 oct. 2026. NCT03564340.
9. Berek J.S. et al., *J Clin Oncol* 2009 ;27:418–425 — oregovomab, phase III négative.
10. Sabbatini P. et al., *J Clin Oncol* 2013 ;31(12):1554–1561 — abagovomab, MIMOSA, phase III négative.
11. « Understanding the Unique Attributes of MUC16 (CA125) », *Cancer Res* 2015 ;75(22):4669–4674.
12. « Virus-like particle vaccine displaying an external, membrane adjacent MUC16 epitope… », *J Ovarian Res* 2023. https://ovarianresearch.biomedcentral.com/articles/10.1186/s13048-023-01325-9
13. Wang et al., *Front Pharmacol* 2022 ;13:1093666 — revue ADC gynécologiques (DMUC5754A).
14. « Emerging role of mucins in antibody drug conjugates for ovarian cancer therapy », *J Ovarian Res* 2024 ;17:161. https://pmc.ncbi.nlm.nih.gov/articles/PMC11308542/
15. Whitehawk Therapeutics, transcription d'appel résultats, fév. 2026 — HWK-016, arrêt de DMUC4064A (déclaration d'entreprise).
16. Shitara K. et al., *Lancet* 2023 ;401:1655–1668 — SPOTLIGHT, NCT03504397.
17. Shah M.A. et al., *Nat Med* 2023 ;29:2133–2141 — GLOW, NCT03653507.
18. FDA, « FDA approves zolbetuximab-clzb with chemotherapy for gastric or gastroesophageal junction adenocarcinoma », 18 oct. 2024. https://www.fda.gov/drugs/resources-information-approved-drugs/fda-approves-zolbetuximab-clzb-chemotherapy-gastric-or-gastroesophageal-junction-adenocarcinoma
19. ClinicalTrials.gov, NCT03816163 (GLEAM) — fiche consultée le 16 nov. 2026. https://clinicaltrials.gov/study/NCT03816163
20. Astellas Pharma, communiqué, 14 oct. 2025 — GLEAM n'atteint pas le critère principal de survie globale ; programme pancréatique arrêté déc. 2025. Relayé par Drugs.com : https://www.drugs.com/clinical_trials/astellas-confirms-phase-2-gleam-trial-did-not-meet-primary-endpoint-overall-survival-patients-22199.html
21. Yu X. et al., *J Clin Oncol* 2025 ;43:4017 (résumé ASCO 2025) — IBI343, phase I pancréas, NCT05458219 ; communiqué Innovent / PR Newswire Asia, ASCO 2025.
22. « Research advances in targeting claudin 18.2 in pancreatic ductal adenocarcinoma treatment », *World J Gastroenterol* 2026 ;32(45):122906. http://www.wjgnet.com/1007-9327/full/v32/i45/122906.htm
23. « Resistance mechanisms and countermeasures in CLDN18.2-positive tumors », *Front Oncol* 2026. https://www.frontiersin.org/journals/oncology/articles/10.3389/fonc.2026.1910011/full
24. « CAR-T and CAR-NK cell therapy targets in gastrointestinal malignancies », *Front Oncol* 2026. https://www.frontiersin.org/journals/oncology/articles/10.3389/fonc.2026.1960663/full
25. CARsgen Therapeutics, communiqué, 20 oct. 2025 — satri-cel adjuvant pancréas (CT041-ST-05), ESMO 2025. http://www.m2pharma.com/news/therapy-areas/oncology/article.php?id=106851
26. ClinicalTrials.gov, NCT06219941 (AZD0901, CLARITY-PanTumour01). https://clinicaltrials.gov/study/NCT06219941
27. ClinicalTrials.gov, NCT07108504 (LM-302 + gemcitabine, pancréas) — via OnCo dossier CLDN18.2 : https://onco.cc/dossiers/cldn18-2/ et https://decentrialz.com/clinical-trials/NCT07108504/
28. Innovent Biologics, communiqué, ASCO 2024 — IBI389, NCT05164458 (données au 11 mars 2024).
29. ClinicalTrials.gov, NCT07066995 (CAR-T mésothéline + CLDN18.2, BAH2573-102). https://clinicaltrials.gov/study/NCT07066995
30. Xing Y. et al., *Front Immunol* 2026 ;16:1638585 — CAR-T VHH anti-CLDN18.2, modèles pancréatiques ; prévalence CLDN18.2 59,2 % dans le PDAC primitif.
31. « IP10 armoring enhances CLDN-18.2–directed CAR-T cell therapy in pancreatic cancer… », *Front Immunol* 2026. https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2026.1998845/full

---

## 5. Points non vérifiés (à ne pas citer comme établis)

- Le numéro NCT de l'essai de phase I CAR-T anti-MUC16 de Memorial Sloan Kettering (O'Cearbhaill 2020) n'a pas été vérifié dans les sources consultées : il n'est pas cité dans ce document.
- Les chiffres de survie de GLEAM (zolbetuximab pancréas) n'ont pas été publiés dans le communiqué du 14 oct. 2025 : seul l'échec du critère principal est établi.
- Les données IBI389 (pancréas) et satri-cel adjuvant proviennent de communiqués d'entreprise / présentations de congrès, pas d'articles revus par les pairs.
- Le statut exact de recrutement des essais en cours (NCT07066098, NCT06219941, NCT07108504, NCT07066995) date de nov. 2026 et doit être revérifié sur ClinicalTrials.gov avant toute citation publique.

---

*Fin du brouillon — 16 novembre 2026. Provenance : recherche web du 16 nov. 2026, sources nommées §4. Aucune valeur inventée ; les lacunes sont nommées au §5.*
