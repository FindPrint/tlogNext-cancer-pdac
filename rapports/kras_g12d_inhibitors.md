# Inhibiteurs directs de KRAS G12D et pan-RAS — données publiques de dose-réponse dans le pancréas

**Date :** 16 novembre 2026. **Projet :** PDAC v6.

## Verdict d'abord

**Peut-on tester ces inhibiteurs contre l'axe KRAS avec des données publiques ? Oui pour un seul : MRTX1133 — et le test est positif.** MRTX1133 est dans le criblage PRISM (dose unique 2,5 µM, 40 lignées pancréas) : il tue spécifiquement les lignées G12D (viabilité −1,70 contre −0,38, p=0,0001) et, chez les G12D seules, l'axe Chronos KRAS du projet prédit la sensibilité (rho +0,47, p=0,079, n=15 — direction juste, effectif trop petit pour conclure).

**Pour les autres — non, aucune matrice publique de dose-réponse n'existe :** RMC-6236 (daraxonrasib), RMC-9805 (zoldonrasib), ASP3082, sotorasib, adagrasib, BI-3406 et TNO155 sont absents de PRISM (6 790 composés) comme de GDSC2 (269 composés). Les données existent sous trois formes seulement : quelques valeurs isolées dans des articles (ChEMBL), des données d'entreprise non publiques, et des essais cliniques (qui ne sont pas des données de sensibilité cellulaire).

**Le fait clinique le plus fort du dossier :** le daraxonrasib (RMC-6236) a doublé la survie médiane en phase III (RASolute-302 : 13,2 contre 6,7 mois, HR 0,40) et a été approuvé par la FDA pour le PDAC métastatique prétraité. Ce n'est pas un remède — c'est une avance réelle, mesurée chez des patients, pas une prédiction du pipeline. Aucune donnée publique ne permet de le tester contre l'axe KRAS du projet.

## 1. Présence dans les criblages déjà téléchargés

Vérifié par recherche exacte sur les noms (Drug.Name) — la première recherche sur la colonne des identifiants BRD avait manqué MRTX1133 et SHP099, corrigé ici.

| Composé | PRISM 24Q2 (6 790) | GDSC2 (269) | PRISM secondaire 19Q4 (1 427) |
|---|---|---|
| MRTX1133 | **PRÉSENT** | absent | absent |
| SHP099 | **PRÉSENT** | absent | absent |
| K-RAS(G12C)-INHIBITOR-6 | **PRÉSENT** (outil) | — | absent |
| RMC-6236 / daraxonrasib | absent | absent | absent |
| RMC-9805 / zoldonrasib | absent | absent | absent |
| ASP3082 | absent | absent | absent |
| Sotorasib | absent | absent | absent |
| Adagrasib | absent | absent | absent |
| BI-3406 | absent | absent | absent |
| TNO155 | absent | absent | absent |
| KRAS (G12C) Inhibitor-12 | — | **PRÉSENT** (outil) | absent |

Vérifié aussi sur la liste des traitements du secondaire (`secondary-screen-replicate-collapsed-treatment-info.csv`, 13 008 lignes, colonne `name`) : MRTX1133, SHP099, sotorasib et adagrasib absents. Le criblage secondaire PRISM (dose-réponse, 19Q4, 1 427 composés, 29 lignées pancréas — bras parallèle, 16 nov. 07h47) est lui aussi négatif : zéro composé FDR < 0,05. Les trois criblages (PRISM primaire, PRISM secondaire, GDSC2) convergent vers le même négatif — sauf MRTX1133, qui n'est que dans le primaire, à dose unique.

## 2. Le test MRTX1133 — nouveau, par allèle KRAS (16 nov. 2026)

**Méthode.** Allèles KRAS des lignées pancréas tirés du MAF DepMap 24Q4 (`OmicsSomaticMutationsMAFProfile.maf`, 98 439 503 octets, SHA `86b8530b…5e96f` ; 390 lignes KRAS, jointes aux modèles par `OmicsProfiles.csv`). 54 lignées pancréas avec allèle : G12D 23, G12V 20, G12R 5, Q61H 2, Q61R 1, G12C 1, G12A 1, G12I 1 (14 lignées pancréas sans mutation KRAS dans le MAF). Viabilité PRISM (dose unique 2,5 µM) + Chronos KRAS joints. Script : `mrtx1133_prism_allele.py` (SHA `932fcafc…b85be`, reproduit les chiffres à l'identique). Sorties : `data/kras_alleles_pancreas.csv` (SHA `9ac803ad…0d42`), `data/mrtx1133_prism_kras_allele.csv` (SHA `7a449c92…6e5ef`).

**Résultats.**
| Groupe | n | Viabilité MRTX1133 moyenne |
|---|---|---|
| G12D | 17 | **−1,70** |
| G12V | 15 | −0,37 |
| G12R | 5 | −0,29 |
| G12C / G12A / Q61H | 1 chacun | −0,84 / −0,84 / −0,10 |
| Non-G12D (tous) | 23 | −0,38 |

Mann-Whitney G12D vs autres : **p=0,0001**. Le médicament tue son allèle cible, et seulement lui — c'est la sélectivité attendue d'un inhibiteur G12D, mesurée sur 40 lignées.

**L'axe Chronos prédit-il la sensibilité ?** Spearman Chronos KRAS vs viabilité MRTX1133 : toutes lignées rho **+0,36 (p=0,031, n=36)** ; **G12D seules rho +0,47 (p=0,079, n=15)** ; non-G12D rho +0,11 (p=0,65, rien). Lecture : chez les lignées qui portent la cible (G12D), plus la lignée dépend de KRAS, plus MRTX1133 la tue — l'axe du projet prédit la réponse au bon médicament, au bon allèle. L'effectif (n=15) est trop petit pour un p < 0,05 : c'est un signal suggestif, pas une preuve. Les lignées G12D sont aussi en moyenne plus dépendantes de KRAS (Chronos −2,29 contre −1,65).

**Contexte PRISM (15 nov., sans allèle) :** rho +0,410, p=0,011, FDR 0,76 — non significatif après correction sur 6 790 composés. Le découpage par allèle est ce qui fait apparaître le signal : sans lui, la dilution par les G12V/G12R (insensibles) noie l'effet.

**Contrôles négatifs.** SHP099 (PRISM) : rho −0,064, p=0,74 ; G12D +0,36 contre autres +0,32 — rien, comme attendu. K-RAS(G12C)-INHIBITOR-6 (PRISM) : rho −0,19, p=0,33 — rien (une seule lignée G12C dans le pancréas). KRAS (G12C) Inhibitor-12 (GDSC2) : rho −0,053 — rien.

## 3. Composé par composé — données, essais, sources

### MRTX1133 — G12D sélectif, non covalent (Mirati / BMS)
- **Données publiques :** PRISM (voir §2) + ChEMBL `CHEMBL4858364` : 45 activités, pour l'essentiel tirées de Hallin et al. 2022. IC50 antiprolifératives pancréas : PANC-1 (pERK) 2,3 nM ; AsPC-1 11,0 nM (56,8 nM dans un second essai) ; HPAC 4,2 nM ; HPAF-II 14,9 nM ; Panc 04.03 27,6 nM ; PK-59 2,9 nM. Lignées WT : MKN-1 3 000 nM, SNU-1033 4 981 nM — sélectivité > 1 000×. Ce sont des valeurs isolées d'un article, pas une matrice multi-lignées.
- **Préclinique :** Hallin et al., *Nat Med* 2022 (DOI 10.1038/s41591-022-02007-7, PMID 36216931) — Kd ~0,2 pM, IC50 < 2 nM, sélectivité ~700× vs KRAS WT ; IC50 médiane ~5 nM sur lignées G12D ; régression ≥ 30 % dans 8/11 (73 %) modèles PDAC (xénogreffes dérivées de lignées et de patients).
- **Clinique :** phase I/II **NCT05737706 — TERMINATED** début 2025 (défis de formulation et de pharmacocinétique après le rachat de Mirati par BMS ; source : revue *Advances in KRAS-Targeted Therapies for Pancreatic Cancer*, PMC13604613, vérifié contre ClinicalTrials.gov sept. 2026 ; confirmé par Selleckchem, données ClinicalTrials.gov). Le composé n'avance plus en clinique sous ce nom.
- **Combinaisons (voir §4).**

### RMC-6236 / daraxonrasib — pan-RAS(ON), tri-complexe (Revolution Medicines)
- **Données publiques :** aucune matrice de dose-réponse. ChEMBL `CHEMBL6168538` : 85 activités, 80 tirées d'un seul document (CHEMBL6115029) — valeurs isolées : HPAC IC50 1,2 nM ; Capan-2 1,4 nM ; Capan-1 (G12V) EC50 1,3 nM ; AsPC-1 (G12D) EC50 3,1 nM ; A-375 (RAS WT) EC50 7 213 nM. Pas de criblage multi-lignées public.
- **Clinique — le résultat le plus fort du dossier :** phase I/II **NCT05379985** (RMC-6236-001) : NEJM 2026, Wolpin et al. (doi 10.1056/NEJMoa2505783), n=168 PDAC métastatiques prétraités, ORR 29 %, PFS médiane 8,1–8,5 mois, OS médiane 13,1–15,6 mois. Phase III **RASolute-302, NCT06625320** (n=500, 2e ligne) : **OS médiane 13,2 contre 6,7 mois, HR 0,40** (IC 95 % 0,30–0,53), données de coupure 10 fév. 2026. **Approbation FDA** (RASONQUE™) pour le PDAC métastatique ayant reçu au moins une ligne de traitement — première approbation d'un inhibiteur ciblant RAS dans le pancréas (revue *Cancers* 2026, doi 10.3390/cancers18213519 ; ESMO 2026, analyses de sous-groupes : bénéfice conservé par sous-groupe RAS, y compris HR 0,43 pour les tumeurs sans mutation RAS identifiée, intervalle large). Avis positif CHMP/EMA le 15 oct. 2026.
- **Autres essais :** adjuvant phase III RASolute-304 **NCT07252232** (500 patients, PDAC réséqué) ; 1re ligne phase III RASolute-303 (daraxonrasib ± chimiothérapie) ; **NCT06445062** (phase I/II, PDAC/CRC) ; **NCT06040541** (phase I, RMC-9805 — voir ci-dessous).
- **Ce qui manque pour le projet :** aucune donnée de sensibilité par lignée publiée — on ne peut pas tester si l'axe Chronos KRAS prédit la réponse au daraxonrasib. Les données de criblage de Revolution Medicines ne sont pas publiques.

### RMC-9805 / zoldonrasib — G12D(ON) (Revolution Medicines)
- **Données publiques :** aucune. Absent de PRISM, de GDSC2 et de ChEMBL (recherche « RMC-9805 » et « zoldonrasib » : 0 résultat).
- **Clinique :** phase I **NCT06040541** (tumeurs solides, dont PDAC). Phase III **NCT07805954** (recrutement) : zoldonrasib + daraxonrasib contre gemcitabine + nab-paclitaxel en 1re ligne du PDAC métastatique G12D. RASolute-305 : zoldonrasib + chimiothérapie, 1re ligne G12D.
- **Ce qui manque :** toute donnée de sensibilité cellulaire publique.

### ASP3082 — dégradeur PROTAC G12D (Astellas)
- **Données publiques :** aucune. Absent de PRISM, de GDSC2 et de ChEMBL (0 résultat).
- **Clinique :** phase I **NCT05382559** ; 33,3 % de réponse à 300 mg (phase précoce, source : *Cancers* 2025, 17, 2453, tableau 2). Profil sûr préliminaire. (Un dégradeur G12D de nouvelle génération, le setidegrasib, est cité en phase III dans la revue *Cancers* 2026 — composé distinct, non vérifié ici.)
- **Ce qui manque :** toute donnée de sensibilité cellulaire publique.

### Sotorasib — G12C covalent (Amgen)
- **Données publiques :** aucune matrice. Absent de PRISM et de GDSC2.
- **Clinique :** CodeBreaK 100 **NCT03600883**, PDAC n=38 prétraités : **ORR 21 %, DCR 84 %, PFS médiane 4,0 mois, OS médiane 6,9 mois** (sources concordantes : *Frontiers in Oncology* 2024, doi 10.3389/fonc.2024.1402128 ; *Therapeutic Advances in Medical Oncology* 2026). G12C ne représente que 1–2 % des PDAC — marginal pour la maladie.
- **Combinaisons :** CodeBreaK 101 **NCT04185883** (sotorasib + anti-PD-1/PD-L1, tramétinib, RMC-4630, afatinib, pembrolizumab, panitumumab, atezolizumab, évérolimus, palbociclib, bevacizumab, TNO155, chimiothérapies).

### Adagrasib (MRTX849) — G12C covalent (Mirati / BMS)
- **Données publiques :** aucune matrice. Absent de PRISM et de GDSC2.
- **Clinique :** KRYSTAL-1 **NCT03785249**, PDAC n=21 : **ORR 33 %, DCR 81 %, PFS médiane 5,4 mois, OS médiane 8,0 mois**. (Une source donne DCR 100 % dans le texte contre 81 % dans son propre tableau — je cite 81 %, valeur du tableau.) Combinaison avec cetuximab (anti-EGFR) évaluée dans KRYSTAL-1 (données surtout colorectales).

### BI-3406 — SOS1 (Boehringer Ingelheim)
- **Données publiques :** aucune matrice. Absent de PRISM et de GDSC2.
- **Clinique :** BI-3406 lui-même n'est jamais allé en clinique. Son dérivé **BI-1701963** est en phase I **NCT04111458** (seul ou + tramétinib), actif non recruteur : 31 patients KRAS-mutés, tolérable, maladie stable chez 7/31 à 18 mois. Deux autres essais BI-1701963 arrêtés par le sponsor (NCT04835714, NCT04627142). Préclinique : BI-3406 inhibe sélectivement la prolifération des cellules KRAS-mutées et bloque la réactivation par rétrocontrôle SOS1 ; synergie avec les inhibiteurs de MEK (*Frontiers in Immunology* 2023, doi 10.3389/fimmu.2023.1223433).

### SHP099 (SHP2, Novartis) et TNO155 (SHP2, Novartis)
- **SHP099 — données publiques :** présent dans PRISM, **rien** (rho −0,064, p=0,74, n=29 ; G12D +0,36 contre autres +0,32). Absent de GDSC2. Pas de donnée de dose-réponse multi-lignées.
- **TNO155 — données publiques :** aucune matrice. Absent de PRISM et de GDSC2.
- **Clinique TNO155 :** phase I **NCT03114319** (dose-finding, tumeurs solides avancées), actif non recruteur : 118 patients, 20 % de maladie stable. Combinaisons : NCT04000529, NCT04330664, NCT04699188 (KontRASt-01 : JDQ443 + TNO155 + tislelizumab). Autres SHP2 : RMC-4630 (NCT03634982, + cobimetinib ; DCR 71 % sur 7 patients G12C NSCLC), BBP-398 (NCT04528836, terminé), ERAS-601 (FLAGSHP-1 : 1 réponse partielle sur 27 — décevant).

### Autres inhibiteurs G12D en clinique (repérés, non demandés mais pertinents)
- **INCB161734** (G12D) : phase I/II, 41 patients PDAC G12D lourdement prétraités, données ASCO GI 2026 (source : honcology.com).
- **HRS-4642** (G12D) : phase I **NCT05533463** ; + gemcitabine/nab-paclitaxel phase Ib/II **NCT06520488** : DCR 93,3 %.
- **TSN1611** (G12D) : phase I/II **NCT06385925**. **LY3962673** (G12D, Lilly) : phase I **NCT06586515**. **LY4066434** (pan-KRAS, Lilly) : phase I **NCT06607185**. **BBO-10203** (pan-RAS) : phase I **NCT06625775**.

## 4. Combinaisons publiées avec ces inhibiteurs (pancréas, préclinique et clinique)

| Combinaison | Preuve | Source |
|---|---|---|
| MRTX1133 + cetuximab (EGFR) | Synergie lignées PDAC/CRC, efficace même là où chaque drogue seule échoue ; sans perte de poids chez la souris | Hallin et al. 2022 ; Drosten & Barbacid, *Mol Oncol* 2022 |
| MRTX1133 + BYL-719 / alpelisib (PI3Kα) | Synergie lignées PDAC/CRC | Hallin et al. 2022 |
| MRTX1133 + MEK / ERK / SHP2 / SOS1 | N'a PAS sensiblement renforcé l'activité (contrairement aux inhibiteurs G12C) | Hallin et al. 2022, via Drosten & Barbacid 2022 |
| MRTX1133 + gemcitabine + nab-paclitaxel | Régression supérieure et prévention des métastases vs chaque modalité seule (modèles murins génétiques) | Revue PMC13604613, réf. 47 |
| MRTX1133 + anti-PD-1 / PD-L1 | Élimination durable, survie améliorée, modèles immunocompétents (16 modèles) ; l'effet dépend des lymphocytes T CD8+ | Kemp et al. 2023, *Cancer Cell* / *Dev Cell* (MD Anderson TRACTION) |
| MRTX1133 + anti-EGFR (erlotinib, osimertinib) | Synergie spécifique aux organoïdes G12D (19 organoïdes dérivés de patients : 9 G12D, 10 autres) ; seule la voie des récepteurs tyrosine-kinases donne un score de Bliss > 10 | *Gastroenterology* 2024, doi 10.1016/S0016-5085(24)05027-3 |
| RMC-6236 + PI3Kα/δ | Synergie (modèles patients et in vivo) ; co-dépendance PI3Kα/δ–SUMO identifiée | Köse et al., cité dans *Cancers* 2026 |
| RMC-6236 + gemcitabine/nab-paclitaxel | Phase III 1re ligne en cours (RASolute-303) | *Cancers* 2026, tableau 1 |
| RMC-6236 + RMC-9805 | Phase III 1re ligne G12D en cours (NCT07805954) | ClinicalTrials.gov |
| RMC-6236 + anti-PD-1, + SHP2 | Stratégies listées, essais en cours | *Turk J Gastroenterol* 2026, tableau 1 |
| Adagrasib + cetuximab | KRYSTAL-1 (données surtout colorectales) | *Turk J Gastroenterol* 2026 |
| Sotorasib + MEK / SHP2 / EGFR / PD-1 | CodeBreaK 101 (NCT04185883) | ClinicalTrials.gov |
| HRS-4642 + gemcitabine/nab-paclitaxel | Phase Ib/II, DCR 93,3 % | *Cancers* 2026, tableau 1 |

**Note sur l'autophagie :** aucune combinaison KRAS + autophagie publiée n'a été trouvée dans les sources consultées pour ces inhibiteurs — la mission la mentionnait comme piste à vérifier ; elle reste à fouiller (littérature hydroxychloroquine + inhibiteurs MEK/ERK, hors périmètre de ce rapport).

## 5. Ce qui manque exactement — et ce qu'il faudrait pour tester

1. **Aucune matrice publique de dose-réponse multi-lignées** pour RMC-6236, RMC-9805, ASP3082, sotorasib, adagrasib, BI-3406, TNO155. Les données de criblage de ces composés sont soit chez les entreprises (Revolution Medicines, Mirati/BMS, Astellas, Amgen, Boehringer, Novartis), soit limitées à quelques lignées dans les articles.
2. **Ce qui existe à la place :** (a) des valeurs isolées par lignée dans les articles, extraites dans ChEMBL (MRTX1133 : 45 activités ; daraxonrasib : 85 activités, un seul document source) — trop peu de lignées pour un test d'axe (6 lignées pancréas pour MRTX1133, 4 pour le daraxonrasib) ; (b) des essais cliniques (réponses chez des patients, pas des IC50 par lignée) ; (c) le criblage PRISM à dose unique pour MRTX1133 et SHP099 — c'est la seule donnée de sensibilité multi-lignées publique pour ces composés, et elle a été exploitée ici.
3. **Ce qu'il faudrait pour tester RMC-6236 / RMC-9805 contre l'axe KRAS :** un criblage de type PRISM ou GDSC incluant ces composés sur ≥ 15 lignées pancréas avec allèles KRAS connus — ou l'accès aux données de criblage des entreprises. Alternative réaliste : les organoïdes dérivés de patients (l'étude *Gastroenterology* 2024 a testé MRTX1133 ± EGFR sur 19 organoïdes) — mais ces données ne sont pas publiques sous forme de matrice.
4. **Limite du test MRTX1133 :** dose unique (2,5 µM) et non une courbe dose-réponse ; n=15 lignées G12D avec Chronos — le rho +0,47 (p=0,079) est suggestif, pas une preuve. Une IC50 multi-doses sur les mêmes lignées trancherait.
5. **Le résultat clinique ne dépend pas du pipeline :** l'approbation du daraxonrasib repose sur des essais chez des patients (RASolute-302), pas sur l'axe Chronos. Le pipeline n'a pas prédit ce résultat — il a seulement, pour MRTX1133, montré que son axe prédit la sensibilité au bon allèle.

## Fichiers

- `kras_g12d_inhibitors.md` — ce rapport
- `mrtx1133_prism_allele.py` — script du test par allèle (SHA `932fcafc…b85be`)
- `data/kras_alleles_pancreas.csv` — allèles KRAS, 54 lignées pancréas (SHA `9ac803ad…0d42`)
- `data/mrtx1133_prism_kras_allele.csv` — viabilité PRISM + Chronos + allèle, 40 lignées (SHA `7a449c92…6e5ef`)
- `data/kras_mutations_maf.csv` — 390 lignes KRAS extraites du MAF (SHA `fcf0eed2…00a1`)
- `data/OmicsSomaticMutationsMAFProfile.maf` — 98 439 503 octets (SHA `86b8530b…5e96f`)
- `data/OmicsSomaticMutationsMatrixHotspot.csv` — 4 210 723 octets (SHA `6444ce81…e3d8`)
- `data/OmicsProfiles.csv` — 254 733 octets (SHA `0bb19ee5…f91c`)
- `PROVENANCE_kras_g12d.md` — provenance complète
