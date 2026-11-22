# PROTOCOLE GELÉ — §8.97 Extension d'audit : la règle du 21 nov. 2026 appliquée à tout le livre blanc (§8.1–§8.89)

**Gel : 21 novembre 2026, avant tout travail de lecture. Protocole
écrit avant le balayage, la lecture et toute rédaction de section.
Travail de LECTURE SEULE : aucun run de pipeline, aucune modification
du livre blanc ni d'aucune ancienne section. Les corrections se font
par addendum daté DANS §8.97, texte d'origine intact.**

## Contexte et portée

Correction de Zackary, 21 novembre 2026, 12h03 (portée étendue à tout
le projet le 12h04) — trois points : (1) un flux en axe de contrôle ne
doit JAMAIS être un flux analysé ; (2) un contrôle non monotone peut
donner un seuil différent, c'est de l'information, pas une erreur ;
(3) le pipeline est avant tout un pipeline d'ANALYSE, pas forcément
de prédiction. L'audit §8.90 est déjà fusionné et publié, donc ces
trois vérifications deviennent une section propre, §8.97, EN PLUS des
4 pistes (§8.93–§8.96, numéros gelés inchangés).

**Portée gelée : livre blanc §8.1–§8.89.** Le livre blanc sur le
disque (`livre-blanc-pdac-v6.md`, SHA `2606caf3…`, 23 739 lignes)
contient aussi §8.90 (l'audit lui-même), §8.91 et §8.92 (finisseur) —
ces trois sections sont HORS de la portée de ce balayage, et
l'exclusion est dite ici : §8.90 parce qu'il est l'audit qui a
déclenché ce travail ; §8.91–§8.92 parce qu'elles appartiennent au
finisseur et ne sont pas encore poussées. Les §8.93–§8.96 sont
couverts par la correction en tête de §8.93, pas par ce balayage.

## Partie 1 — Contrôle jamais analysé

**Question.** Existe-t-il, ailleurs que dans les 96 rotations
d'origine du §8.32 (défaut connu, corrigé au §8.44), des endroits où
un flux de contrôle était aussi un flux analysé ?

**Méthode (deux volets, lecture seule).**
(a) Balayage mécanique de TOUS les dossiers de runs sur le disque
(`results_fast_v62_*`, `results_fast_v61_*`, et tout autre dossier de
run du projet) : pour chacun, lire `master_results.json` (csv_path,
contrôle) et les colonnes du CSV source ; signaler (i) toute colonne
se terminant par `.1` — signature mécanique du doublon §8.32 (pandas
renomme la colonne dupliquée) ; (ii) toute colonne de contrôle
présente aussi comme flux analysé ; (iii) tout CSV dont la première
colonne est un flux qui réapparaît parmi les colonnes suivantes.
(b) Table des familles : pour chaque famille de runs, nommer la
variable d'ordre (KRAS, prolifération, MTAPCN, stage, score de
pureté, flux de rotation, température pour HP35, etc.) avec sa source
(section du livre blanc ou script de construction), et vérifier
qu'elle est absente des flux analysés.
Chaque cas trouvé est nommé avec sa localisation exacte (section,
dossier de run, fichier CSV, colonnes) et corrigé par addendum daté
dans §8.97 (texte d'origine intact). Si aucun autre cas n'existe, le
dire plainement avec la méthode de vérification (quels dossiers et
quelles sections ont été contrôlés, combien de fichiers).

## Partie 2 — Contrôles non monotones

**Question.** Quelque part dans le livre blanc, le seuil d'un contrôle
non monotone a-t-il été écarté ou traité comme une erreur ?

**Méthode.** Grep `monotone` et `monotonie` dans tout le livre blanc ;
lire chaque occurrence en contexte ; juger si un seuil a été écarté
ou traité comme une erreur au motif de non-monotonie. Si oui, le
réhabiliter comme information, par addendum daté dans §8.97. Si non,
le dire avec les exemples vérifiés : localiser la règle ancienne
(« le contrôle doit être monotone en T » — où apparaît-elle ?) et
écrire comment la nuance du 21 novembre 2026 la corrige (la monotonie
aide à lire, elle n'est pas une condition pour que le seuil compte).

## Partie 3 — Analyse, pas prédiction

**Question.** Où le livre blanc présente-t-il un résultat comme une
prédiction ?

**Méthode.** Grep dans tout le livre blanc : `prédit`, `prédiction`,
`prévoit`, `annoncera`, `prédire`, `prévoir`, `prédira`,
`prédisent`, `prédictions`, et les formulations équivalentes
relevées en lecture. Juger chaque occurrence : présente-t-elle un
RÉSULTAT comme une prédiction ? Ne sont PAS des présentations de
résultat comme prédiction : les négations (« le pipeline ne prédit
pas », « pas de prédiction sans rigueur »), les stipulations de
protocole (« le protocole prévoit que… » = le protocole stipule), les
discussions de méthode sur la prédiction en général. Chaque occurrence
exclue est listée avec sa raison. Chaque occurrence retenue est
reformulée en langage d'analyse (« les données montrent »,
« on observe »), par addendum daté dans §8.97, texte d'origine intact.

## Partie 4 — Preuves de reproductibilité et de clarté, vérifiables par un lecteur extérieur

**Question.** Ce qui est sur GitHub est-il reproductible, clair et
propre — et comment un lecteur extérieur peut-il le vérifier lui-même,
sans nous croire sur parole ? Langage simple, moyen concret de
vérification pour chaque affirmation.

**Méthode — vérifier chaque preuve contre le dépôt réel avant de
l'écrire ; si une preuve ne tient plus, le dire et corriger.**
(a) Reproductibilité : test à froid §8.77 (reproduction exacte à 0,0
— citer le chiffre et où le vérifier) ; `download_data.sh` (52
fichiers, 2,4 Go — où le trouver, comment le lancer ; vérifier la
liste des fichiers contre DATA_SOURCES.md et les SHA des copies
locales — NE PAS re-télécharger 2,4 Go) ; chaque fichier avec sa
source et son SHA (`DATA_SOURCES.md` — citer sa longueur et son SHA
actuel) ; pipeline v6.2 SHA `f07567c4…`, original intact (v6.1 et v6
intacts, SHA vérifiés avant et après chaque lot — re-vérifier
maintenant).
(b) Clarté : chaque verdict avec ses limites écrites ; chaque
correction par addendum daté, texte d'origine intact (citer 2–3
exemples : §8.70/§8.72, corrections du §8.90, coquille
PROVENANCE_889 §7) ; chaque section avec son protocole gelé avant
les runs et sa provenance nommée.
(c) Dettes connues : nommer explicitement (au minimum :
l'avertissement médical en tête du document, dette de gabarit de
l'audit §8.90, priorité haute ; les entrées de journal à ajouter à
chaque publication suivante ; toute autre dette trouvée en vérifiant).
Une dette nommée n'est pas un défaut caché — c'est la preuve que
l'audit est honnête.

## Règles de rédaction de §8.97

- Un verdict par partie, chiffres d'abord.
- La correction de Zackary (12h03, portée 12h04) apparaît nommément
  et datée en tête de §8.97.
- Aucune recommandation clinique, jamais.
- Si ce travail retarde le lot, ne pas bâcler et ne pas bloquer les
  4 pistes : rapporter l'état exact au parent, qui décide.
