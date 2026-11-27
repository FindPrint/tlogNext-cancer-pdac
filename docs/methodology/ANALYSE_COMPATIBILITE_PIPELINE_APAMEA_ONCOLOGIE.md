# Compatibilité du pipeline Apamea avec un projet oncologique — analyse de sécurité

> **Avertissement médical.** Cette analyse décrit une méthodologie de recherche sur données ouvertes et dé-identifiées. Elle ne fournit ni diagnostic, ni pronostic individuel, ni recommandation de traitement. Un modèle ne peut être envisagé pour la clinique qu’après validation scientifique, clinique, éthique et réglementaire indépendante.

## Conclusion courte

Le pipeline Apamea ne peut **pas** être transféré tel quel à un jeu de données sur le cancer du pancréas, et il ne peut pas aboutir seul à un traitement « safe, réel et robuste ». Son apport transférable est son **discipline de reproductibilité** : données traçables, tests d’exclusion, analyses de sensibilité, variantes explicitement séparées, rapports et archivage vérifiable.

Le code v3 doit rester intact dans le projet Apamea et ne doit jamais être exécuté comme pipeline clinique. Un projet oncologique nécessiterait un adaptateur séparé, avec des métriques, des splits et des critères pré-spécifiés adaptés aux cohortes de patients.

## Analyse composant par composant

| Élément du pipeline v3 | Portabilité vers une étude oncologique | Décision |
| --- | --- | --- |
| Graine, manifestes SHA-256, JSON de paramètres, scripts de reprise | Bonne portabilité. | Réutiliser dans un dépôt distinct. |
| Tests par exclusion de blocs, de températures et de familles | Portables sous une autre forme : leave-one-cohort-out, leave-one-site-out, ablation de groupes de variables et évaluation de données manquantes. | Réimplémenter et pré-spécifier. |
| Tri d’une colonne de contrôle puis scan de seuil Monte Carlo | Non portable : les patients ne forment pas une série ordonnée par une variable de contrôle choisie après observation. | Interdit pour la cible clinique ou la survie. |
| Score de séparation pré/post-seuil | Non portable : un seuil optimisé sur les mêmes données créerait une sélection circulaire et ne définit pas une classe clinique. | Interdit. |
| Estimateurs de complexité temporelle (Hurst, DFA, Higuchi, SampleEn) | Conditionnellement applicable seulement à une série longitudinale suffisamment dense par patient et avec une mesure validée. | Hors périmètre du premier pilote transcriptomique transversal. |
| CSD, F1′/F2″ et cartes de partitions | Spécifiques au système Apamea et non validées médicalement. | Ne pas réutiliser. |
| Injection de bruit et diagnostics de stabilité | L’intention est utile, mais la forme doit être remplacée par des analyses de sensibilité biomédicales : imputation encadrée, normalisation, lots, plateformes, confusion et robustesse inter-cohorte. | Réimplémenter sous protocole nouveau. |

## Adaptateur de recherche proposé

Le premier projet ne cherchera ni un « seuil critique », ni un traitement, ni une étiquette patient. Il testera une question descriptive pré-spécifiée :

> Une association entre un ensemble de gènes ou une signature définie avant l’analyse et la survie globale garde-t-elle une direction cohérente entre cohortes transcriptomiques indépendantes de cancer du pancréas ?

### Unités d’analyse et règles de séparation

| Élément | Règle proposée |
| --- | --- |
| Unité analytique | Une personne ou un échantillon tumoral, avec un identifiant dé-identifié et une cohorte source. |
| Cible de recherche | Survie globale censurée, ou autre endpoint explicitement disponible ; jamais une recommandation de traitement. |
| Variables | Ensembles de gènes pré-spécifiés à partir d’une source indépendante, ou variables descriptives de qualité. Toute exploration à l’échelle génomique doit être marquée exploratoire. |
| Normalisation | Réalisée à l’intérieur de chaque cohorte ; aucune information de la cohorte de validation ne doit régler la cohorte de développement. |
| Séparation | Toute cohorte entière doit rester hors développement pour former une validation externe. Aucun patient ne peut apparaître dans deux partitions. |
| Résultat primaire | Direction et amplitude d’association par cohorte, hétérogénéité, incertitude et qualité de calibration lorsque celle-ci est pertinente. |
| Interprétation | Hypothèse biologique ou pronostique de recherche seulement ; pas d’usage patient individuel. |

## Contrôles de robustesse obligatoires

Le nouvel adaptateur doit produire les contrôles suivants, séparés des résultats principaux :

1. une validation leave-one-cohort-out complète, sans réutilisation de la cohorte exclue pour choisir variables ou paramètres ;
2. une analyse leave-one-platform-out lorsqu’elle est possible ;
3. une ablation des groupes de variables et une analyse de stabilité du sens des associations ;
4. une analyse de sensibilité aux données manquantes, aux méthodes de normalisation et au filtrage de qualité ;
5. une comparaison à une baseline pré-spécifiée ne faisant pas appel aux variables moléculaires ;
6. une mesure de l’incertitude par intervalle de confiance ou bootstrap par patient, sans bootstrap de lignes dupliquant un même patient ;
7. un tableau des limitations : population, stades, échantillonnage, plateformes, suivi, traitements et confusion disponible ;
8. une révision du protocole et des interprétations par un clinicien spécialiste du PDAC et un biostatisticien avant toute communication pouvant être considérée comme clinique.

## Architecture logicielle recommandée

```text
apamea-artificial-spin-ice-multiflux/        # Projet historique, inchangé
pancreatic-cancer-open-data-reproducibility/ # Projet médical distinct et privé
  docs/protocol/
  docs/data-governance/
  docs/reports/
  scripts/00_fetch_metadata.py
  scripts/01_build_cohort_manifest.py
  scripts/02_quality_control.py
  scripts/03_prespecified_association.py
  scripts/04_leave_one_cohort_out.py
  scripts/05_sensitivity_analyses.py
  scripts/06_generate_report.py
  data/manifests/
  results/
  release-assets/
  MANIFEST_SHA256.txt
```

Le premier dépôt ne doit contenir aucune donnée patient brute ni donnée sous accès contrôlé. Il doit uniquement référencer des DOI, URL, versions, licences, checksums, scripts et résultats agrégés autorisés.

## Décision proposée

Le premier objectif réalisable est un **pilote de reproductibilité transcriptomique multi-cohortes avec MetaGxPancreas**, sans entraînement de modèle clinique et sans prédiction de traitement. Sa réussite serait de démontrer une procédure transparente qui sépare exploration et validation externe. Cette réussite ne constituerait pas une validation clinique ; elle déterminerait seulement si un programme de recherche plus ambitieux est scientifiquement défendable.
