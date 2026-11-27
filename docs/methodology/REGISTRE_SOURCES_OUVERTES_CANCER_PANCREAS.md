# Registre vérifié des sources ouvertes candidates — cancer du pancréas

> Ce registre sert exclusivement à sélectionner un pilote de recherche rétrospectif, reproductible et non clinique. Une disponibilité publique ne transforme pas une cohorte en outil de décision thérapeutique.

## Cohortes et ressources examinées

| Ressource | Contenu documenté | Accès et taille | Rôle adapté dans un pilote | Limites essentielles |
| --- | --- | --- | --- | --- |
| TCGA-PAAD (GDC) | 185 cas ; données cliniques et bio-échantillons pour tous les cas ; transcriptome pour 178 cas, méthylation pour 184 cas, WES pour 185 cas et RPPA pour 120 cas. | Portail GDC ; mélange de données ouvertes et contrôlées selon le type. | Cohorte de développement ou réplication moléculaire, après figer la version GDC et les fichiers autorisés. | Cohorte relativement petite, avec données manquantes par modalité ; le GDC indique que les pipelines évoluent. |
| CPTAC-PDA (TCIA/PDC/GDC) | Imagerie CT/MR/US/PT, lames histologiques, clinique, génomique et protéomique ; liens de sujet communs entre ressources CPTAC. | 168 sujets pour la collection complète ; 155,24 Go annoncés ; images CC BY 4.0, mais vérifier les conditions de chaque ressource liée. | Deuxième projet, consacré à une analyse multimodale ou à une validation imagerie–omique. | Imagerie et protocoles d’acquisition hétérogènes ; volume élevé ; ne convient pas au premier pilote du pipeline Apamea. |
| PACA-AU / PACA-CA (PGPA) | PACA-AU : 461 patients, ADN tumoral profond, expression RNA-seq et métadonnées clinico-pathologiques, traitement et outcome. PACA-CA : 317 patients avec exome/transcriptome. | Ressources historiques ICGC disponibles pour exploration via PGPA ; l’accès aux fichiers doit être vérifié avant téléchargement. | Validation externe potentielle d’une hypothèse transcriptomique, sans supposer l’accès aux fichiers bruts. | Les cohortes et les voies d’accès doivent être figées et documentées ; ne pas mélanger sous-types ni statuts de traitement. |
| QCMG Nature 2016 (cBioPortal) | 456 patients, WGS/exome profond ; mutations disponibles pour 383 échantillons et expression pour 96 échantillons. | Portail et archive de données cBioPortal publics. | Réplication mutationnelle ou exploratoire des altérations moléculaires. | Chevauchement incomplet entre expression et mutations ; pas un jeu approprié pour un modèle d’expression principal. |
| MetaGxPancreas (Bioconductor) | Compendium de jeux transcriptomiques pancréatiques convertis en objets `SummarizedExperiment`, avec sources et détails de normalisation conservés dans les objets. L’étude MetaGxData rapporte 11 jeux pancréatiques dans sa carte de risque et 12 jeux avec survie globale dans une analyse à l’échelle du génome. | Paquet Bioconductor sous licence Artistic-2.0 ; téléchargement reproductible via ExperimentHub après gel de version. | **Meilleur candidat pour un premier pilote** : plusieurs cohortes, transcriptomique et annotations cliniques curatées, validation leave-one-cohort-out naturelle. | Données hétérogènes par plateforme et métadonnées incomplètes selon les jeux ; résultats seulement associatifs et rétrospectifs. |

## Choix de travail recommandé

Le premier projet doit utiliser **MetaGxPancreas** comme base de données de recherche, avec un protocole pré-écrit de réplication multi-cohortes. Il est plus adapté que CPTAC-PDA à une première démonstration parce qu’il permet de tester la reproductibilité entre cohortes sans commencer par une imagerie massive, un accès contrôlé ou une cible thérapeutique.

Le projet ne tentera pas de proposer un traitement. Sa question initiale sera :

> Une association transcriptomique pré-spécifiée avec la survie globale est-elle stable en direction, en ampleur et en incertitude lorsque chaque cohorte indépendante est exclue à tour de rôle ?

## Références

[1] [GDC — TCGA-PAAD](https://portal.gdc.cancer.gov/projects/TCGA-PAAD)

[2] [TCIA — CPTAC-PDA](https://doi.org/10.7937/K9/TCIA.2018.SC20FO18)

[3] [PGPA — cohortes ICGC pancréatiques](https://pancreasexpression.org/analytics/icgc/)

[4] [cBioPortal — Pancreatic Adenocarcinoma (QCMG, Nature 2016)](https://www.cbioportal.org/study/summary?id=paad_qcmg_uq_2016)

[5] [Bioconductor — MetaGxPancreas](https://doi.org/10.18129/B9.bioc.MetaGxPancreas)

[6] [Gendoo et al., *Scientific Reports* (2019)](https://doi.org/10.1038/s41598-019-45165-4)
