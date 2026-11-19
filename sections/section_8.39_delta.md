# §8.39 Élucidation de Delta — chantier 3 (19 novembre 2026)

**Verdict d'abord : Delta reste NON ÉLUCIDÉ.** Le mécanisme est désormais
compris dans sa structure (voir §8.39.3), mais aucune variable ni aucun petit
ensemble nommé — parmi H1–H7 du protocole et H8–H17 testées ici — ne prédit
à la fois l'identité de la paire médiane et la valeur de d_div au critère
exigé de ≥ 90 %. Meilleur score honnête mesuré : **87,9 % des paires et
81,8 % des valeurs** en validation hold-out (H9e : famille, masque, MFA, n ;
majorités apprises sur les 156 runs v6.1, testées sur les 66 runs v6.2).
Meilleur score en échantillon : 89,6 % / 84,7 % (H11 : masque, MFA, n,
contrôle — 87 groupes pour 222 runs, voir §8.39.6 sur le surajustement).
Delta garde son statut de **piste fragile** (6/8 en phase 2, échec sur HP35)
et ne devient **pas** un discriminateur recommandé.

## §8.39.1 Ce qui était acquis avant ce chantier

Protocole gelé `PROTOCOL_v6.2.md` §4 ; première élucidation
`v62_delta_elucidation.md` (18–19 nov. 2026, 222 runs : 156 v6.1 + 66 v6.2) :

- Identités de construction vérifiées 222/222 (0 écart) : d_div = moyenne des
  3e et 4e médianes divergence triées ; d_sat = 4e médiane saturation triée.
- d_div prend 133 valeurs distinctes (à 10⁻³) : ce ne sont pas « quelques
  niveaux fixes » au sens brut, ce sont des grappes.
- MFA quasi discret : 9 valeurs distinctes [3,0 ; 4,0 ; 4,5 ; 5,0 ; 6,0 ;
  6,25 ; 6,5 ; 6,75 ; 7,0].
- Masques fini/absent : LP 181 runs, -P 12, -- 29 (LevinaBickel absent sur
  41 runs, PersistentHomology absent sur 29 ; saturation toujours complète,
  7/7 membres).
- Meilleure combinaison H1+H2+H3 (masque, MFA, n) : paire 80,2 %, valeur
  ±0,10 61,7 %. Corrélations avec d_div : LocalPCA +0,968, MFA +0,968,
  GraphDimension +0,864, LevinaBickel +0,807, PersistentHomology +0,796,
  PCAIntrinsic +0,708 ; robustness +0,197, sharpness +0,227,
  max_separation +0,187, stability +0,031.
- Anomalie DFA = −38,16 retrouvée et classée sans effet sur d_sat
  (voir §8.39.8).

## §8.39.2 Méthode du chantier 3

Lecture seule, aucun run du pipeline, aucune modification d'un code.
Ensemble : les 222 runs de `v62_delta_levels.csv` (dérivé des
`master_results.json` par `extract_delta_levels.py`), soit 156 v6.1 et
66 v6.2. Script de ce chantier : `v62_delta_elucidation_h8.py`
(log `v62_delta_h8.log`, supplément `v62_delta_h8_supplement.log`,
résumé `v62_delta_h8.json`).

Trois garde-fous ajoutés au protocole §4.4, qui ne mesurait qu'en
échantillon :

1. **Hold-out v6.1 → v6.2.** Les majorités par groupe sont apprises sur
   les 156 runs v6.1 et testées sur les 66 runs v6.2, ensemble de
   réplication indépendant (le hachage L5, seule différence v6.1→v6.2, ne
   touche pas Delta, déterministe). Un groupe inconnu au test reçoit la
   majorité globale v6.1. C'est le test honnête : un score qui ne tient
   qu'en échantillon est du surajustement, pas une élucidation.
2. **Paire non ordonnée.** La prédiction est aussi mesurée en ignorant
   l'ordre 3e/4e, pour voir si c'est l'ordre — et non la composition —
   qui bloque. Réponse : non (les deux scores sont quasiment identiques,
   voir §8.39.4).
3. **Sensibilité à la déduplication.** L'ensemble contient 10 répétitions
   rep2 exactes (validation v6.2) et des `div_sorted` identiques entre
   runs (rotations d'une même série) : 69 lignes retirées, 153 runs
   distincts. Tous les scores principaux sont recalculés sur cet ensemble
   dédupliqué.

Règle d'honnêteté appliquée partout : un prédicteur qui utilise les 6
médianes divergence elles-mêmes — ou leur rang — est une reformulation du
mécanisme, pas une explication. Il est rapporté comme diagnostic et marqué
**CIRCULAIRE** (§8.39.5). Seuls comptent pour le critère ≥ 90 % les
prédicteurs structurels : masque, MFA, n, contrôle, famille de série,
réel/nul, sorties du scan, d_sat/d_crit/d_null, L7a.

Nouvelles hypothèses testées (H8–H17) : H8 — quartiles d'un seul membre
continu (LocalPCA, LevinaBickel, PCAIntrinsic, GraphDimension,
PersistentHomology) ; H9 — famille de série et ses combinaisons avec MFA,
n, masque ; H10 — réel/nul ; H11 — combinaison complète (masque, MFA, n,
contrôle / famille / nul) ; H12 — `n_fluxes_used` détaillé par estimateur ;
H13 — quartiles de d_sat, d_crit, d_null, trio_gap_E, max_separation, et
leurs croisements avec MFA ; H14 — robustness (log-quartiles), sharpness,
direction L7a ; H15 — référence H1+H2+H3, re-mesurée en hold-out ;
H16 — structure des rangs et des écarts entre valeurs triées (§8.39.3) ;
H17 — plafonds par régression linéaire (§8.39.5).

## §8.39.3 Ce que la structure dit : l'ordre est presque figé, le choix se joue entre trois estimateurs

C'est le résultat nouveau de ce chantier. Sur les 222 runs, les rangs
(0 = valeur la plus basse) des six membres divergence sont :

| Estimateur | Rangs observés | Dans la paire (3e/4e) |
|---|---|---|
| GraphDimension | 0 : 184, 1 : 38 | 0/222 |
| PersistentHomology | 0 : 38, 1 : 155 | 0/222 |
| LocalPCA | 2 : 212, 3 : 10 | 222/222 |
| LevinaBickel | 3 : 31, 4 : 73, 5 : 77 | 31/222 |
| PCAIntrinsic | 2 : 4, 3 : 75, 4 : 77, 5 : 66 | 79/222 |
| MFA | 1 : 29, 2 : 6, 3 : 106, 4 : 43, 5 : 38 | 112/222 |

Lecture :

- **GraphDimension et PersistentHomology sont toujours les deux plus
  basses** (rangs 0–1 sur 222/222) : elles ne sont jamais médianes.
  **LocalPCA est toujours 3e ou 4e** (222/222) — presque toujours
  exactement 3e (212/222). **LevinaBickel n'est jamais sous le rang 3.**
  L'ordre est donc séparé en deux blocs par une échelle : les deux bas
  (~1,4 et ~1,7), LocalPCA (~2,7–5,5), puis les trois hauts
  (LevinaBickel, PCAIntrinsic, MFA, ~3–8).
- **d_div = (LocalPCA + X) / 2**, où X est l'autre membre médian. Sur les
  181 runs à 6 membres (k=6), LocalPCA est 3e dans 176 cas, et le 4e
  membre est alors **le minimum de {MFA, LevinaBickel, PCAIntrinsic}
  dans 176/176 cas**. La question « pourquoi d_div choisit sa paire »
  se réduit donc à : **lequel des trois estimateurs hauts est le plus
  petit, une fois LocalPCA fixée en 3e position** (plus les 5 runs où
  LocalPCA est 4e, et les cas à k impair, ci-dessous).
- Paires ordonnées observées : LocalPCA+MFA 99, LocalPCA+PCAIntrinsic 46,
  LocalPCA+LevinaBickel 31, MFA+LocalPCA 30, PCAIntrinsic+LocalPCA 4,
  singletons LocalPCA 7, MFA 5. En paire non ordonnée : {LocalPCA, MFA}
  129, {LocalPCA, PCAIntrinsic} 50, {LocalPCA, LevinaBickel} 31,
  {LocalPCA} 7, {MFA} 5. LocalPCA figure dans la paire 217/222 (97,7 %).
- Cas à k impair : masque -P (k=5, 12 runs) → médiane = 3e valeur seule
  (LocalPCA 7, MFA 5) ; masque -- (k=4, 29 runs) → médiane = moyenne des
  2e et 3e valeurs, paire unique MFA+LocalPCA sur 29/29 runs,
  d_div 3,08–3,15 (le groupe le plus serré de tout l'ensemble).
- Écarts entre valeurs triées (k=6, n=181) : 2e→3e médiane 3,045
  (min 1,134 ; 0 % sous 0,10) — le bloc bas est séparé de la médiane par
  un large fossé ; 3e→4e médiane 1,263 (min 0,156 ; 11,6 % sous 0,25) ;
  4e→5e médiane 0,472 (16,6 % sous 0,10) ; 1re→2e médiane 0,294 ;
  5e→6e médiane 0,278 ; étendue totale des 6 valeurs, médiane 5,517.
  La séparation bas/médiane est robuste, mais **le concours pour la 4e
  place se joue entre trois valeurs séparées de ~0,5 en médiane** —
  c'est là que vit l'indétermination.
- **Le résidu est intra-groupe, pas inter-groupes.** Dans le groupe
  (LP, MFA 6,0, n=178), n=62, trois paires coexistent (LocalPCA+MFA 47,
  LocalPCA+PCAIntrinsic 13, LocalPCA+LevinaBickel 2), d_div s'étale de
  4,62 à 5,46, LocalPCA de 3,80 à 4,92, LevinaBickel de 5,62 à 7,29,
  PCAIntrinsic de 5,33 à 6,88. Dans le groupe (LP, MFA 7,0, n=178),
  n=53, deux paires se partagent presque moitié-moitié
  (LocalPCA+LevinaBickel 23, LocalPCA+PCAIntrinsic 30), d_div 5,58–6,13,
  LevinaBickel 6,38–7,57, PCAIntrinsic 6,64–7,20. Sur les 7 groupes
  (masque, MFA, n) de taille ≥ 5, 4 contiennent ≥ 2 paires différentes.
  À l'inverse, l'ordre LocalPCA vs MFA ne bascule jamais à l'intérieur
  d'un groupe de taille ≥ 3 (0/13 groupes) : ce qui varie, c'est
  l'ordre relatif des trois hauts entre eux, décidé par leurs magnitudes
  continues — magnitudes que ni le masque, ni MFA, ni n, ni le contrôle,
  ni la famille ne contiennent.

## §8.39.4 Hypothèses H8–H15 : taux de prédiction

Majorité dans le groupe (paire ordonnée / valeur de d_div à ±0,10 par
moyenne de groupe), en échantillon sur 222 runs puis en hold-out
(majorités v6.1 → test v6.2, n=66). Référence de base : la paire la plus
fréquente (LocalPCA+MFA, 99/222) donne 44,6 % sans aucun prédicteur.

| Hypothèse | Variable | Paire (éch.) | Valeur (éch.) | Paire (hold-out) | Valeur (hold-out) | Groupes |
|---|---|---|---|---|---|---|
| H15 réf. | (masque, MFA, n) | 80,2 % | 61,7 % | 81,8 % | 65,2 % | 21 |
| H8a–e | 1 membre, quartiles | 46,8–57,7 % | 13,1–35,1 % | 39,4–60,6 % | 4,5–22,7 % | 4–5 |
| H9 | famille | 76,1 % | 49,1 % | 72,7 % | 50,0 % | 19 |
| H10 | réel/nul | 44,6 % | 5,4 % | 56,1 % | 0,0 % | 2 |
| H9b | (famille, nul) | 79,3 % | 54,5 % | 77,3 % | 56,1 % | 38 |
| H9c | (famille, MFA) | 84,2 % | 80,6 % | 81,8 % | 78,8 % | 36 |
| H9d | (famille, n) | 77,9 % | 52,7 % | 75,8 % | 56,1 % | 23 |
| **H9e** | **(famille, masque, MFA, n)** | **87,8 %** | **82,4 %** | **87,9 %** | **81,8 %** | 40 |
| H11 | (masque, MFA, n, contrôle) | 89,6 % | 84,7 % | 86,4 % | 78,8 % | 87 |
| H11b | = H9e (famille remplace le contrôle) | 87,8 % | 82,4 % | 87,9 % | 81,8 % | 40 |
| H11c | (masque, MFA, n, nul) | 82,4 % | 68,5 % | 83,3 % | 66,7 % | 33 |
| H12 | n_fluxes détaillé | 63,1 % | 22,1 % | 71,2 % | 21,2 % | 8 |
| H13a–e | d_sat / d_crit / d_null / trio / max_sep, quartiles | 48,2–54,5 % | 0,5–24,3 % | 42,4–56,1 % | 0,0–25,8 % | 4–5 |
| H13f–g | (d_sat ou d_crit, MFA) | 62,2–67,6 % | 39,6–53,2 % | 50,0–57,6 % | 24,2–47,0 % | 17–19 |
| H14a–d | robustness / sharpness / L7a | 44,6–67,1 % | 0,9–47,7 % | 31,8–57,6 % | 0,0–36,4 % | 3–18 |

Lecture par hypothèse :

- **H8 (un membre continu seul)** : rien ne dépasse 57,7 % sur la paire.
  Même la valeur de LocalPCA — qui est presque toujours dans la paire —
  ne prédit la paire qu'à 46,8 % (quartiles trop grossiers pour un ordre
  décidé par des différences de ~0,5).
- **H9 (famille)** : la famille seule vaut 76,1 % / 49,1 % ; croisée avec
  MFA elle monte à 84,2 % / 80,6 %, et avec masque + n (H9e) à
  87,8 % / 82,4 % — **le meilleur score honnête, confirmé en hold-out
  (87,9 % / 81,8 %)**. La famille apporte de l'information (les séries
  partagent une échelle d'estimateurs), mais elle ne résout pas le
  concours intra-groupe du §8.39.3.
- **H10 (réel/nul)** : 44,6 % en échantillon, soit exactement la base
  sans prédicteur ; valeur 5,4 %. **La permutation des lignes ne change
  pas la paire médiane** : la paire est une propriété de l'échelle des
  estimateurs sur la série, pas du caractère réel ou nul des données.
  C'est aussi pourquoi Delta ne sépare pas réel et nul (voir §8.39.9).
- **H11 (combinaison complète)** : 89,6 % / 84,7 % en échantillon, mais
  87 groupes pour 222 runs (2,6 runs par groupe en moyenne) et hold-out
  en baisse (86,4 % / 78,8 %) : le gain sur H9e est du surajustement,
  pas de l'information (voir §8.39.6).
- **H12–H14** : `n_fluxes_used` détaillé, les quartiles de d_sat/d_crit/
  d_null/trio/max_sep, robustness, sharpness, direction L7a — tous sous
  68 % sur la paire, la plupart proches de la base 44,6 %. H4 (robustness)
  est confirmée infirmée comme prédicteur, comme en §4.
- **Paire non ordonnée** : les scores sont quasiment identiques aux
  scores ordonnés (ex. H9e 87,8 % dans les deux cas, H11 89,6 % dans les
  deux cas). Ce n'est pas l'ordre 3e/4e qui bloque : c'est la composition
  elle-même (lequel des trois hauts est 4e).

## §8.39.5 Le plafond de la valeur : même en trichant, on n'atteint pas 90 %

Le critère (b) — la valeur de d_div à ±0,10 — est le plus dur, et il
l'est structurellement. Régressions linéaires (moindres carrés, 222 runs) :

- Structurel seul (MFA, n, d_sat, d_crit) : R² = 0,942, résidu
  écart-type 0,283, **47,3 % des prédictions à ±0,10**. Ajouter le
  masque (indicatrices) ne change rien (47,3 %).
- LocalPCA seul : R² = 0,937, 25,2 % à ±0,10.
- LocalPCA + MFA (deux membres de la paire) : R² = 0,969, résidu 0,208,
  **84,2 % à ±0,10** (79,0 % sur les 181 runs k=6 seuls).
- Les 4 membres hauts en linéaire (k=6) : R² = 0,985, résidu 0,121,
  74,6 % à ±0,10 — le modèle linéaire ne peut pas capturer le
  minimum qui choisit le 4e membre.

Diagnostic **CIRCULAIRE** (utilise les rangs, donc les 6 valeurs
elles-mêmes — rapporté pour localiser l'information, pas comme un
prédicteur éligible) : (rang de MFA, masque, n) prédit la paire à
92,8 % en échantillon et 95,5 % en hold-out — la paire, oui — mais la
valeur seulement à 70,3 % / 80,3 %. **Même en connaissant le rang de
MFA, on ne prédit pas d_div à ±0,10 sur 90 % des runs.** Seule
l'identité de construction H6 — la moyenne des deux valeurs médianes
elles-mêmes — atteint 100 % sur la valeur (222/222 à ±0,001 sur le CSV
arrondi à 4 décimales ; 222/222 à 10⁻⁶ sur les JSON pleins dans
l'extracteur d'origine). Conclusion : le critère (b) n'est satisfait
par rien d'autre que la chose elle-même. Ce n'est pas un manque de
données (voir §8.39.7), c'est la nature de d_div : une moyenne de deux
magnitudes continues, dont la seconde est le minimum de trois
magnitudes continues qui varient librement dans chaque groupe
structurel.

## §8.39.6 Sensibilité : déduplication et le cas H11 à 90,8 % (rejeté)

Ensemble dédupliqué : 153 runs (sans les 10 rep2, sans les doublons de
`div_sorted`) :

- Référence H1+H2+H3 : 79,7 % / 60,8 % (contre 80,2 % / 61,7 %) — stable.
- H9e : 87,6 % / 83,7 % — stable.
- H11 (masque, MFA, n, contrôle) : **90,8 % / 86,9 %** — la paire
  franchit 90 %, mais avec **85 groupes pour 153 runs (1,8 run par
  groupe)** et la valeur toujours sous 90 % (86,9 %). C'est de la
  mémorisation, pas une élucidation : le contrôle (53 valeurs distinctes)
  découpe l'ensemble en singletons, et le hold-out v6.1→v6.2 de H11
  (86,4 % / 78,8 %) confirme que ce score ne se généralise pas.
  **H11 est donc rejeté comme élucidation**, et le critère §4.4 exige
  les deux volets (paire ET valeur) : aucun candidat ne les remplit,
  en échantillon, en hold-out, ni sur l'ensemble dédupliqué.

## §8.39.7 Pourquoi des runs supplémentaires ne trancheraient pas

**Aucun run supplémentaire n'a été lancé dans ce chantier, et c'est un
choix mesuré, pas une omission.** Le résidu n'est pas un bruit
d'échantillonnage : les deux plus gros groupes existent déjà avec
n=62 et n=53 runs et se partagent entre deux ou trois paires
(§8.39.3) ; ajouter des runs du même plan (mêmes familles, mêmes
rotations, mêmes nuls graine 42) affinerait la proportion du partage
vers ~50/50, il ne la résoudrait pas. Ajouter de nouvelles familles
ajouterait de nouveaux groupes, sans résoudre le concours intra-groupe.
Ce qui trancherait le critère (b) serait un modèle des magnitudes des
estimateurs eux-mêmes à partir du contenu des flux — c'est-à-dire
prédire LevinaBickel, PCAIntrinsic et MFA (et LocalPCA) depuis la
matrice de flux avant de calculer la médiane — un travail hors du
protocole H1–H7, hors de la lecture des sorties, qui exigerait un
nouveau protocole gelé et le go de Zackary. Il est consigné ici comme
piste ouverte (§8.39.10), pas lancé.

## §8.39.8 Anomalie DFA = −38,16 — confirmée sans effet (rappel)

22 runs avec DFA < −10 (dont −38,1597 sur
`results_fast_v61_depmaprot_aco2_nul`), tous DepMap et rotations
protéines DepMap (n=45). Sur les 22, DFA est toujours la 1re valeur
triée de la saturation — jamais la 4e, donc jamais la médiane :
d_sat vaut alors Katz (~1,19) et Delta n'est pas touché
(Delta 1,89–1,95 sur ces runs). DepMap v6.2 (rep1 et rep2, identiques) :
DFA = −18,5768, d_sat = 1,1900 (4e = Katz), Delta = 1,9338.
Une médiane d'estimateur extrême isolée sur petites séries, pas une
rupture de d_sat. Statut inchangé depuis §4.

## §8.39.9 Conséquence : Delta reste une piste fragile

Rappel (chiffres de la phase 2, `PROTOCOL_v6.2.md` §1 et
`v62_delta_elucidation.md`, non recalculés ici) : Delta sépare 6/8
paires principales, mais échoue sur HP35 — le témoin positif —
(nul 4,57 > réel 4,48), deux écarts ≤ 0,15, annexe 13/23. Ce chantier
en donne la raison structurelle : **la paire médiane est insensible à
la permutation réel/nul (H10 = base, 44,6 %)**, parce qu'elle est fixée
par l'échelle des estimateurs sur la série, pas par le contenu réel ou
nul des lignes. Un écart de Delta entre réel et nul ne peut donc venir
que de petites différences de magnitudes, noyées dans la variation
intra-groupe (§8.39.3). Delta n'est pas un discriminateur recommandé ;
son 6/8 reste une piste fragile, à ne pas utiliser comme critère de
décision.

## §8.39.10 Ce qui reste ouvert

1. **Modéliser les magnitudes.** Prédire les médianes LevinaBickel,
   PCAIntrinsic, MFA et LocalPCA depuis la matrice de flux elle-même
   (avant médiane) : seul un tel modèle pourrait, en principe, prédire
   la paire et la valeur à ≥ 90 %. Nouveau protocole gelé + go requis ;
   non lancé ici.
2. **d_sat.** La médiane saturation est quasi constante par famille
   (Hurst2mH 4e dans 126 runs, DFA 72, Katz 22, BoxCounting 2) et sa
   variation est petite (moyenne 1,520 ± 0,124 sur 222 runs) : Delta ≈
   d_div − constante par famille, mais la constante change avec n
   (n=45 : 1,240 ± 0,078 ; n=178 : 1,580 ± 0,022 ; n=515 : 1,652 ±
   0,005). L'élucidation complète de Delta exigerait aussi celle de
   d_sat ; elle n'est pas faite ici.
3. **Le trio.** `trio_gap_E` (Higuchi / InformationD1 / LevinaBickel)
   reste rapporté descriptivement ; il ne devient pas un indicateur de
   discrimination (aucune sélection d'indicateur après coup).
4. **Généralisation à de nouvelles familles.** Les scores hold-out
   (H9e 87,9 % / 81,8 %) sont mesurés sur les 66 runs v6.2, qui
   partagent les familles des 156 v6.1. Une famille entièrement nouvelle
   n'a pas été testée et dégraderait probablement les scores fondés sur
   la famille.

## Provenance (§8.39)

- **Demande et go :** Zackary, « Lance tout cela », 19 novembre 2026
  ~05h47 (chantier 3 de la session v6.2). Protocole gelé :
  `PROTOCOL_v6.2.md` §4 (critère ≥ 90 % paire ET valeur), plan
  H1–H7 ; ce chantier ajoute H8–H17 et les garde-fous hold-out /
  déduplication décrits au §8.39.2.
- **Pipeline :** v6.2 `universal_v6.2.0_cohen.py`,
  SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant travail, jamais modifié) ; v6.1
  `universal_v6.1.0_cohen.py`,
  SHA-256 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`.
  **Aucun run du pipeline dans ce chantier.**
- **Données lues (lecture seule) :** 222 `master_results.json`
  (156 `results_fast_v61_*`, 66 `results_fast_v62_*`) dans
  `~/workspace/runs/pdac-v6/` ; 223 dossiers au total, dont un vide,
  `results_fast_v62_mtap` (0 octet, créé le 19 nov. 11h27 — run en cours
  d'un autre chantier au moment de l'écriture, non compté, non touché).
  Nature des lignes : les JSON sont des sorties instrumentales du
  pipeline (médianes calculées par estimateur, métriques du scan,
  L7a) ; les CSV d'entrée sont des matrices de flux (mesures omiques
  publiques : TCGA, GEO, ICGC, CPTAC, DepMap — voir les fichiers
  `PROVENANCE_*.md` du dossier — et leurs nuls permutés, graine 42) ;
  les contrôles sont des noms de flux (étiquettes, mots humains).
- **Scripts et sorties de ce chantier :**
  `extract_delta_levels.py` (base, SHA-256
  `48f4c8859e7a76b1d152558874d7a1376a781e9830d35ac33439f2df8f637284`) ;
  `v62_delta_levels.csv` (SHA-256
  `463df02cca786b3fd9d135ac8e90825ed4290e7ac21e689232b1d32b8f25ac84`) et
  `v62_delta_levels.json` (SHA-256
  `3321fc3a2f87c13f6f9c617efb534f711089fd7e0cb463e532f287278e0985a9`) ;
  `v62_delta_elucidation_h8.py` (ce chantier, SHA-256
  `15212102d1c7582b97a80e456d93f25b322475a56e85513c3cbc7a72713c48ab`) ;
  `v62_delta_h8.log` (SHA-256
  `d173064e0c7704d492a70ef5810523256a559f28b3c228663edcd8f5688e1f68`) ;
  `v62_delta_h8_supplement.log` (SHA-256
  `2b90cc41c7bba20ca181f5ff67e57a19139148255fb5caa5ebfdcf86ba084ade`) ;
  `v62_delta_h8.json` (SHA-256
  `83141bb6b5883da136a118e72423a462670cf720d2cfd7384cdc8a2d95306d00`) ;
  synthèse antérieure `v62_delta_elucidation.md` (SHA-256
  `0794eb0ea3cf1317bd10d33ac33d798b07a44c8864185287469cf28d6eaac56a`).
  Section rédigée dans `section_8.39_delta.md` (ce fichier) ; le livre
  blanc n'a pas été modifié directement.
- **Ce qui manque :** les valeurs brutes par flux (colonnes `_*_mean`)
  ne sont pas extraites ici — seules les médianes par estimateur
  figurent dans les JSON lus, ce qui borne ce chantier à la structure
  des rangs ; les hachages des CSV d'entrée sont ceux des fichiers
  `PROVENANCE_*.md` (non re-vérifiés ici, les CSV n'ayant pas été
  relus) ; le run `results_fast_v62_mtap` (dossier vide, autre
  chantier) n'est pas inclus ; aucune famille entièrement nouvelle
  n'a été testée en hold-out (§8.39.10 point 4).
- **Date de rédaction :** 19 novembre 2026. Auteur : TagPrint.

— Fin de la §8.39. —
