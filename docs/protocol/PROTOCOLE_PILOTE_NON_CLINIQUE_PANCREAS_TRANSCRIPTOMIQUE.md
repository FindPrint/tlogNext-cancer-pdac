# Protocole pilote — reproductibilité transcriptomique multi-cohortes du cancer du pancréas

> **Avertissement médical.** Il s’agit d’un protocole rétrospectif de recherche sur données ouvertes et dé-identifiées. Il ne produit pas de diagnostic, de pronostic individuel, de recommandation thérapeutique ni de dispositif destiné au soin. Toute hypothèse qui persisterait après ce pilote devrait être évaluée par des cliniciens, biostatisticiens et instances compétentes avant toute ambition clinique.

## 1. Titre et question pré-spécifiée

**Titre de travail :** stabilité inter-cohortes d’associations transcriptomiques pré-spécifiées avec la survie globale dans le PDAC.

**Question primaire :** pour une signature transcriptomique définie avant l’analyse, le sens et l’amplitude de son association avec la survie globale sont-ils cohérents entre cohortes indépendantes de PDAC ?

Cette question n’évalue ni la réponse à un médicament, ni la sélection d’un traitement, ni la probabilité individuelle de survie. Les informations de traitement seront utilisées, lorsqu’elles existent, pour décrire les cohortes et les limitations, jamais pour recommander une thérapie.

## 2. Données et gel de provenance

Le pilote visera la version publiée de `MetaGxPancreas` via Bioconductor/ExperimentHub. Ce paquet distribue des jeux transcriptomiques pancréatiques comme objets `SummarizedExperiment` et conserve la provenance ainsi que les détails de normalisation dans les métadonnées des objets [1].

Avant tout calcul, le projet créera un manifeste par cohorte contenant : nom, source primaire, version de paquet, date d’installation, plateforme, nombre de participants, nombre d’événements disponibles, période de suivi, variables cliniques présentes, licence/conditions accessibles et checksum des artefacts téléchargés. Toute cohorte sans définition explicite de la survie globale ou sans identifiant indépendant de cohorte sera exclue de l’analyse primaire.

## 3. Population et unité d’analyse

L’unité d’analyse est un participant dé-identifié. Une même personne, un échantillon répété ou une mesure technique ne peut contribuer qu’une fois à l’analyse primaire. Les diagnostics non-PDAC, les types histologiques mélangés et les données sans endpoint correctement défini seront soit exclus, soit documentés dans une analyse exploratoire distincte.

Les résultats seront présentés cohorte par cohorte avant toute synthèse. Une distribution démographique ou clinique non fournie par une cohorte restera explicitement inconnue, sans imputation narrative.

## 4. Variables et modèle primaire

Le marqueur primaire ne sera pas découvert sur les mêmes données. Deux possibilités admises, à choisir avant téléchargement complet, sont :

| Option | Définition | Statut |
| --- | --- | --- |
| Signature externe publiée | Ensemble fixe de gènes et pondérations explicitement tiré d’une publication ou d’une ressource indépendante. | Préférée, sous réserve d’une traçabilité claire. |
| Ensemble biologique prédéfini | Ensemble de gènes issu d’une base de voies biologiques versionnée, sans optimisation sur les cohortes. | Admissible comme analyse de recherche. |

Le score doit être calculé à l’intérieur de chaque cohorte après une normalisation documentée. Aucun seuil de score ne sera choisi à partir de la survie, aucune sélection de gènes ne sera optimisée sur les données d’évaluation, et aucune partition pré/post analogue au pipeline Apamea ne sera créée.

L’analyse primaire utilisera une association de survie appropriée à des données censurées, avec un effet continu et son incertitude. Les variables cliniques disponibles pourront être utilisées dans un modèle ajusté secondaire uniquement si leur taux de données manquantes, leur définition et leur rôle pronostique sont décrits par cohorte. Les effets ne seront jamais convertis en conseil thérapeutique.

## 5. Validation indépendante et analyses de robustesse

Chaque cohorte est exclue à tour de rôle du développement éventuel de toute règle fixe ; elle devient alors une cohorte d’évaluation strictement tenue à l’écart. Cette organisation répond au principe selon lequel les données d’évaluation ne doivent pas servir à l’entraînement, au réglage ou à la sélection [2] [3].

| Contrôle | Exigence | Signal d’alerte |
| --- | --- | --- |
| Leave-one-cohort-out | La cohorte exclue n’intervient pas dans la normalisation globale, le choix du score ou le réglage. | Toute fuite de participants ou de paramètres. |
| Direction d’effet | Rapporter le sens de l’association par cohorte et une synthèse à effets aléatoires seulement si les cohortes sont comparables. | Inversion répétée de direction ou hétérogénéité majeure. |
| Incertitude | Rapporter intervalles de confiance et nombre d’événements, pas seulement une valeur de p. | Intervalles trop larges pour soutenir une conclusion. |
| Sensibilité plateforme | Répéter en excluant une plateforme lorsque plusieurs plateformes existent. | Résultat déterminé par une unique plateforme. |
| Données manquantes | Décrire les manquants et comparer les analyses sans imputation à toute méthode d’imputation autorisée. | Conclusion qui dépend d’un choix d’imputation. |
| Comparaison clinique | Examiner l’ajustement à des variables standard seulement lorsqu’elles sont disponibles et comparables. | Confusion non mesurée ou définitions incompatibles. |
| Revue du biais | Renseigner une grille PROBAST+AI adaptée au statut de modèle ou de marqueur. | Risque de biais élevé sans validation externe. |

## 6. Critères de décision du pilote

Le pilote peut être décrit comme **reproductible sur cohortes ouvertes** si, et seulement si, toutes les conditions suivantes sont satisfaites :

1. toutes les sources, versions, exclusions et transformations sont manifestées et reproductibles ;
2. aucun patient ou paramètre provenant de la cohorte d’évaluation ne fuit dans le développement ;
3. l’effet est rapporté, avec incertitude, dans au moins deux cohortes indépendantes ;
4. toute contradiction ou hétérogénéité est présentée comme résultat et non éliminée ;
5. la documentation de rapport couvre les éléments pertinents de REMARK et TRIPOD+AI ;
6. le résultat reste libellé comme **association de recherche**, sans allégation de bénéfice thérapeutique ou de validité clinique.

L’échec de ces critères est un résultat utile : il déclenche un rapport de non-généralisabilité, pas une recherche post hoc de seuil ou de sous-groupe favorable.

## 7. Gouvernance et communication

Le rapport inclura une déclaration explicite de non-usage clinique, les conflits d’intérêts disponibles, les sources de données, les limitations de population et les conditions d’accès. Les conclusions devront suivre les recommandations de transparence de TRIPOD+AI pour une éventuelle étude de modèle [2], les domaines de risque de biais de PROBAST+AI [3] et les items pertinents de REMARK pour les marqueurs tumoraux pronostiques [4].

Aucune donnée individuelle, aucun identifiant patient, aucune information sous accès contrôlé et aucune recommandation de traitement ne seront placés dans GitHub. Les résultats publics éventuels seront uniquement agrégés, après vérification des licences et de la gouvernance.

## Références

[1] [Bioconductor — MetaGxPancreas](https://doi.org/10.18129/B9.bioc.MetaGxPancreas)

[2] [Collins et al. — TRIPOD+AI, *BMJ* (2024)](https://doi.org/10.1136/bmj-2023-078378)

[3] [Moons et al. — PROBAST+AI, *BMJ* (2025)](https://doi.org/10.1136/bmj-2024-082505)

[4] [Altman et al. — REMARK explanation and elaboration, *PLOS Medicine* (2012)](https://doi.org/10.1371/journal.pmed.1001216)
