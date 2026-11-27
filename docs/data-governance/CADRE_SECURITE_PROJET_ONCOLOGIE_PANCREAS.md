# Cadre de sécurité et de gouvernance — exploration reproductible en oncologie pancréatique

> **Avertissement médical.** Ce projet doit être compris comme une analyse informatique de recherche sur données ouvertes et dé-identifiées. Il ne constitue ni un diagnostic, ni une recommandation thérapeutique, ni un dispositif médical. Toute conclusion susceptible d’influencer la prise en charge d’une personne doit être évaluée par des cliniciens qualifiés, soumise à une validation indépendante et, le cas échéant, à la gouvernance réglementaire et éthique applicable.

## 1. Finalité autorisée

L’objectif initial autorisé est de tester si une adaptation explicitement documentée du pipeline peut détecter des **structures reproductibles dans des données de recherche sur le cancer du pancréas**. Les sorties admises sont des hypothèses, des diagnostics de stabilité, des analyses descriptives et, éventuellement, des modèles prédictifs purement rétrospectifs sur données ouvertes.

Les sorties ne doivent pas être utilisées pour choisir un traitement, trier des patients, estimer un pronostic individuel, déclencher une intervention ou prétendre qu’un seuil algorithmique correspond à une réponse clinique. Le pipeline Apamea n’est pas un outil médical : ses mécanismes de partition, ses rangs et ses scores doivent être reconstruits pour les données biomédicales et validés séparément.

## 2. Distinction entre réutilisation et adaptation

| Composant Apamea | Statut pour un projet oncologique | Règle de sécurité |
| --- | --- | --- |
| Principes de traçabilité, versionnage, manifestes SHA-256 et archivage | Réutilisable | Conserver les données, scripts, paramètres, environnements et résultats avec des identifiants immuables. |
| Tests de robustesse par exclusions, ablations et partitions temporelles | Réutilisable après redéfinition | Les splits doivent respecter les patients, les sites, les cohortes et la chronologie clinique ; aucune fuite patient n’est admise. |
| Rang de la colonne de contrôle et seuil Monte Carlo v3 | Non transférable tel quel | Ne jamais l’assimiler à une dose, une réponse, un stade, une survie ou une décision de soin. |
| Variables de spin, CSD et F1′/F2″ | Non transférables telles quelles | Toute analogie de vocabulaire ou interprétation physique est interdite. |
| Pipeline v2/v3 original | À conserver comme référence historique, non clinique | Ne pas l’exécuter sur une cohorte de patients comme s’il s’agissait d’un validateur médical. |

## 3. Données admises pour le pilote

Le pilote doit se limiter à des données **ouvertes, publiques, dé-identifiées et correctement attribuées**. Les jeux candidats doivent préciser leur licence, leur provenance, leur niveau d’accès, les types de mesures, les effectifs, les critères cliniques disponibles et les limites connues.

Aucune donnée identifiante, aucun dossier médical local, aucun compte rendu clinique individuel et aucune information de contact patient ne doit être placé dans le dépôt ou l’environnement de calcul. Les données sous accès contrôlé ne doivent être utilisées qu’après obtention indépendante des autorisations requises ; elles ne seront pas copiées ni utilisées dans le pilote ouvert sans validation explicite.

## 4. Critères minimaux avant toute prétention de robustesse

Un résultat de recherche ne peut être qualifié de robuste qu’après :

1. la pré-spécification claire de la question, de la population, de la variable cible et des critères d’évaluation ;
2. une séparation stricte des individus entre entraînement, réglage et évaluation ;
3. des validations internes structurées par patient, site et, lorsque pertinent, période temporelle ;
4. une validation externe sur une cohorte indépendante et non utilisée pour le développement ;
5. l’évaluation de calibration, de discrimination, d’incertitude, de données manquantes, de sous-groupes et de biais de sélection ;
6. une comparaison avec des baselines cliniquement pertinentes ;
7. une revue par un clinicien spécialiste du cancer du pancréas et un biostatisticien ;
8. une documentation des limites et des domaines hors périmètre.

Même une analyse validée rétrospectivement ne devient pas automatiquement un outil clinique. Toute utilisation au soin nécessite un développement, une validation prospective, une évaluation éthique et, selon le contexte, un parcours réglementaire spécifique.

## 5. Organisation GitHub proposée

Un dépôt **GitHub privé distinct** est requis pour chaque projet de données. Le dépôt initial peut être intitulé `pancreatic-cancer-open-data-reproducibility` et ne contiendra que des scripts, manifestes, documentation et résultats agrégés autorisés.

La structure minimale proposée est la suivante :

```text
README.md
STATUS.md
LICENSE_OR_DATA_NOTICES.md
docs/
  protocol/
  data-governance/
  methodology/
  reports/
scripts/
data/
  manifests/
  external-links/
results/
  exploratory/
  validation/
release-assets/
MANIFEST_SHA256.txt
```

Les fichiers de données lourds ou restreints sont référencés par URL, DOI, checksum et conditions d’accès, mais ne sont pas publiés sans vérifier la licence. Les releases doivent fournir des archives vérifiables et les dépôts doivent rester privés par défaut.

## 6. Décision de départ

Avant de créer un dépôt ou d’exécuter une analyse, il faut sélectionner un jeu de données ouvert dont le contenu permet une question de recherche non clinique précise. La prochaine phase consiste à comparer des ressources publiques reconnues pour le cancer du pancréas, en privilégiant les cohortes offrant une documentation, des mesures omiques ou d’imagerie et des métadonnées cliniques dé-identifiées.
