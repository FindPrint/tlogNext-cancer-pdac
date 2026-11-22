### 8.97 Extension d'audit — la règle du 21 nov. 2026 appliquée à tout le livre blanc (§8.1–§8.89) (21 novembre 2026)

**Correction de Zackary, datée et nommée, qui déclenche cette section
(21 novembre 2026, 12h03 ; portée étendue à tout le projet le 12h04 ;
partie 4 ajoutée le 12h05).** Trois points, portés à TOUT le projet,
pas seulement aux quatre pistes du lot en cours : (1) un flux en axe
de contrôle ne doit JAMAIS être un flux analysé ; (2) même un flux NON
monotone en axe de contrôle peut donner un seuil différent — c'est de
l'information, pas une erreur, il ne faut pas l'écarter ; (3) le
pipeline est AVANT TOUT un pipeline d'ANALYSE, pas forcément de
prédiction — les verdicts se formulent comme de l'analyse, jamais
comme des prédictions. L'audit §8.90 est déjà fusionné et publié, donc
ces trois vérifications deviennent cette section propre, EN PLUS des
§8.93–§8.96. La correction en tête de §8.93 reste en place : §8.93
porte la règle pour les quatre pistes, §8.97 l'applique
rétrospectivement à tout le livre blanc.

**Verdict d'abord, en quatre phrases — une par partie. (1) Contrôle
jamais analysé : AUCUN autre cas que le défaut connu des rotations
d'origine (§8.32) — balayage mécanique de 752 dossiers de runs : 650
propres, 102 avec la signature du doublon, tous des rotations, 0
ailleurs ; les 2 dossiers sans `master_results.json` sont des
répertoires vides et 1 run BRCA en cours (CSV déjà vérifié propre).
(2) Contrôles non monotones : AUCUN seuil écarté au motif de
non-monotonie dans tout le livre blanc — 38 occurrences de
« monotone » et « monotonie » lues en contexte ; la règle ancienne, sous
sa forme littérale « le contrôle doit être monotone en T », n'apparaît
même pas dans le livre blanc (elle vit dans la philosophie de travail),
et les cas proches (stade, Tiriac, Delta) lisent les seuils, ils ne
les écartent pas. (3) Analyse, pas prédiction : 257 lignes contiennent
un terme de prédiction ; 9 formulations de verdict sont reformulées
en langage d'analyse par addendum daté ci-dessous (survie Cox et axe
Chronos, titres §8.48) ; le reste est conforme avec raison écrite
(négations, modélisation statistique testée, questions ouvertes,
stipulations de protocole, plans d'industriels). (4) Reproductibilité
et clarté : chaque preuve citée a été re-vérifiée contre le dépôt réel
— test à froid §8.77 (0,0 exact, flux SHA-identiques), script de
re-téléchargement (SHA 55811136…, EXIT:0, 52 fichiers, 2,4 Go),
DATA_SOURCES.md (1 484 lignes, SHA dec70e17…), pipeline v6.2 SHA
f07567c4… et v6.1/v6 intacts — et les dettes connues sont nommées
ci-dessous, dont l'avertissement médical toujours absent en tête du
document (priorité haute).**

## 8.97.0 Portée, méthode, règles

**Portée gelée : §8.1–§8.89.** Le livre blanc sur le disque
(`livre-blanc-pdac-v6.md`, SHA `2606caf3…`, 23 739 lignes) contient
aussi §8.90 (l'audit lui-même), §8.91 et §8.92 (finisseur) — ces trois
sections sont HORS de ce balayage : §8.90 parce qu'il est l'audit qui
a déclenché ce travail ; §8.91–§8.92 parce qu'elles appartiennent au
finisseur et ne sont pas encore poussées. Les §8.93–§8.96 sont couverts
par la correction en tête de §8.93, pas par ce balayage.

**Méthode.** Protocole gelé `PROTOCOL_audit_regle_897.md` (SHA
`fa04f4fee49648b7ad409a5323d75f3a61324f94bb40e3ca37dfec55a035370e`,
écrit avant tout balayage, toute lecture, toute rédaction de section).
Travail de LECTURE SEULE : aucun run de pipeline, aucune modification
du livre blanc ni d'aucune ancienne section. Les corrections se font
par addendum daté DANS cette section, texte d'origine intact.

## 8.97.1 Partie 1 — Contrôle jamais analysé : aucun autre cas

**Question.** Existe-t-il, ailleurs que dans les 96 rotations
d'origine du §8.32 (défaut connu, corrigé au §8.44), des endroits où
un flux de contrôle était aussi un flux analysé ?

**Méthode.** Deux volets, lecture seule. (a) Balayage mécanique de
TOUS les dossiers `results_*` du projet (script `audit_doublon_897.py`,
SHA `731dbe25f5cab43d1c5acc3cb13856c33cdbf5694167e46af15476bcfc10f5de`) :
pour chaque dossier, lecture de `master_results.json` (csv_path,
contrôle) et des colonnes du CSV source ; signalement de toute colonne
se terminant par `.1` — signature mécanique du doublon §8.32 (pandas
renomme la colonne dupliquée) — et de tout contrôle présent aussi
comme flux analysé. (b) Table des familles : variable d'ordre nommée
pour chaque famille, avec sa source, vérifiée absente des flux
analysés.

**Résultat du balayage (21 novembre 2026, 17h14).** 752 dossiers
scannés : **650 propres** (aucune colonne `.1`, aucun contrôle
réanalysé), **102 avec une colonne `.1`**, **0 contrôle réanalysé
sous le même nom**, 0 CSV illisible. Les 3 dossiers sans
`master_results.json` : `results_fast_pdac_depmap` et
`results_fast_pdac_depmap_nul` — deux répertoires VIDES (créés le
15 nov. 2026 12h39, jamais remplis, aucune donnée) — et
`results_fast_v62_896_brca` — le run BRCA du lot en cours, en train
de tourner au moment du balayage, dont le CSV a déjà été vérifié
propre séparément (ESR1 absent des flux, §8.96).

**Les 102 dossiers avec `.1` sont TOUS des rotations, 0 ailleurs.**
Composition exacte : 96 fichiers §8.32 (v6.1, 4 familles × 12
contrôles × réel/nul : V4ROT, IMMROT, PARPROT, DEPMAPROT) + 6
dossiers de la rotation CLDN18 (la paire qui a RÉVÉLÉ le défaut,
§8.31(4) : `results_fast_v4r_cldn18` + nul, `results_fast_v61_
v4r_cldn18` + nul, `results_fast_v62_v4r_cldn18` + nul — la même
rotation courue sous trois nommages/versions, toujours avec le
doublon). Exemple : `pdac_tcga_fluxes_v4rot_CEACAM5.csv` —
`CEACAM5,PGC,REG4,…,CEACAM5.1,…,MUC16` (le flux d'ordre en contrôle
ET en `CEACAM5.1` parmi les flux analysés). Le livre blanc le dit
déjà au §8.44 (ligne 772) : « CLDN18 est à la fois le contrôle et
un flux (lu `CLDN18.1`) ».

**Table des familles (variable d'ordre → absente des flux ?).**

| Famille | Variable d'ordre | Source | Absente des flux analysés ? |
|---|---|---|---|
| Paires principales V1 + A2 (15) | KRAS croissant | §8.4, §8.88.3 | Oui — contrôle `step`, KRAS absent des 15 CSV |
| Rotations §8.32 (96 fichiers) | flux de rotation | §8.32 | **NON — défaut connu (colonne `.1`)** |
| Rotations DEDUP §8.44 (48 paires) | flux de rotation | §8.44 | Oui — flux d'ordre = 1re colonne (contrôle), 0 `.1` sur 48/48 |
| Rotation CLDN18 (6 dossiers) | CLDN18 | §8.31(4) | **NON — même défaut, cas révélateur** |
| Test A §8.34 (prolifération) | score PROLIF | §8.34 | Oui — contrôle PROLIF, MKI67 absent |
| Test C §8.45 (stade) | stade clinique | §8.45 | Oui — le stade n'est pas un flux |
| Série MTAP §8.43 | MTAPCN | §8.43 | Oui — contrôle MTAPCN, 12 flux |
| MTAP_PRMT5FLUX §8.41 | dépendance PRMT5 | §8.41 | Oui — contrôle `step`, PRMT5 absent |
| V4R_PURITY | score acineux | §8.51 | Oui — contrôle `score_acineux` |
| HP35 (biophysique) | température (ordre des lignes) | §8.1 | Oui — contrôle `step`, T n'est pas une colonne |
| Chen drogue §8.84 | AUC médicament (ordre des lignes) | §8.84 | Oui — contrôle `step`, l'AUC n'est pas un flux |
| GDC organoid §8.85/§8.87, GSE194249 §8.88 | KRAS croissant | §8.85/§8.88 | Oui — mêmes CSV que les paires A2 |
| LUAD/BRCA §8.96 | KRAS / ESR1 (ordre des lignes) | §8.96 | Oui — contrôle `step`, KRAS/ESR1 absents |

**Mécanisme vérifié par lecture du code.** Le pipeline exclut la
colonne de contrôle des flux analysés quand aucun `flux_mapping`
n'est fourni — cas de tous nos runs — (ligne 6787 de
`universal_v6.2.0_cohen.py` : `[c for c in ... if c != control_col]`).
Le doublon §8.32 ne venait donc pas du pipeline : il venait des CSV
construits avec le flux d'ordre en double (contrôle + colonne `.1`).
Les fichiers DEDUP du §8.44 ont retiré la colonne en double, et ce
sont eux qui sont utilisés depuis (§8.56, §8.95 : 48/48 vérifiés
propres le 21 novembre 2026).

**Verdict partie 1 : AUCUN autre cas.** Le défaut est circonscrit
aux rotations d'origine et à la rotation CLDN18 qui l'a révélé —
déjà documenté au §8.32, déjà corrigé au §8.44, déjà dit dans le
livre blanc. Aucun addendum de correction n'est nécessaire pour
cette partie : il n'y a rien d'autre à corriger. Les 102 dossiers
défectueux restent sur le disque comme témoins du défaut, ils ne
sont plus utilisés pour aucun verdict depuis §8.44.

## 8.97.2 Partie 2 — Contrôles non monotones : aucun seuil écarté

**Question.** Quelque part dans le livre blanc, le seuil d'un contrôle
non monotone a-t-il été écarté ou traité comme une erreur ?

**Méthode.** Grep `monotone` et `monotonie` dans tout le livre blanc
(38 occurrences, lignes 48 à 23669) ; lecture de chaque occurrence en
contexte ; jugement : un seuil a-t-il été écarté ou traité comme une
erreur au motif de non-monotonie ?

**Résultat : NON — aucun seuil écarté pour non-monotonie.** Les 38
occurrences se répartissent ainsi : relations monotones entre
variables (dose–réponse, Spearman, Delta en w et en n) ; propriétés
mathématiques (`sep`/`maxsep` monotones l'un en l'autre, §8.56.2) ;
descriptions de données (survie par stade non monotone, §7 ligne 50 ;
Delta non monotone en n aux petites tailles, §8.62.5). Aucune ne dit
qu'un seuil est écarté parce que son contrôle est non monotone.

**La règle ancienne, sous sa forme littérale, n'apparaît pas dans le
livre blanc.** « Le contrôle doit être monotone en T » — cette
formulation vit dans la philosophie de travail (synthèse
d'alignement, règles de l'instrument), pas dans le texte du livre
blanc. Dans le livre, la monotonie apparaît comme une aide à la
lecture, jamais comme une condition d'admission d'un seuil. La nuance
du 21 novembre 2026 la corrige donc sans contredire aucun texte du
livre : la monotonie aide à lire, elle n'est pas une condition pour
que le seuil compte.

**Exemples vérifiés (les cas proches, lus en contexte).**
- **Test C, stade (§8.45, ligne 3042).** Le contrôle (stade) est
  monotone non décroissant mais n'a que 4 valeurs distinctes
  (corrélation rang/valeur 0,646, ties massives) : les seuils sont
  LUS (T_0 à 98,41 %, T_-1 au pas 50, T_-2 au pas 2), pas écartés —
  le verdict est NON, porté par la lecture, pas par un tri.
- **Tiriac et al. 2018 (§8.78.8, ligne 18497).** « T0 ambigu partout,
  contrôle non monotone partout (v5.9.4, 19–20 nov. 2026). » La
  non-monotonie est RAPPORTÉE comme une propriété des données déjà
  courues ; la cohorte est classée non-candidate parce que ce n'est
  « pas une nouvelle cohorte » (déjà courue), pas pour sa
  non-monotonie. Aucun seuil n'est écarté au motif de non-monotonie.
- **Delta en n (§8.62.5).** « Delta croît avec n — localement, non
  monotone » : la non-monotonie est décrite, elle ne disqualifie
  rien.
- **Le cas le plus proche d'une mise à l'écart — et ce n'en est pas
  une au sens de la règle.** Au §8.45 toujours : « un “seuil” à
  l'intérieur du stade II ne mesure rien » — le seuil est mis de
  côté parce que l'ordre DANS le stade II est l'ordre des
  codes-barres, arbitraire par construction (aucune information),
  et non parce que le contrôle serait non monotone. La nuance du
  21 novembre 2026 ne change pas ce jugement : un ordre arbitraire
  ne porte pas d'information, un contrôle non monotone en porte —
  la distinction est écrite ici pour qu'elle ne soit pas confondue
  avec un tri par monotonie.

**Verdict partie 2 : aucun cas à réhabiliter.** Aucun addendum de
correction n'est nécessaire pour cette partie. La nuance est
consignée : désormais, si un contrôle non monotone donne un seuil
différent, il est lu comme un résultat d'analyse à part entière.

## 8.97.3 Partie 3 — Analyse, pas prédiction : 9 formulations de verdict reformulées

**Question.** Où le livre blanc présente-t-il un résultat comme une
prédiction ?

**Méthode.** Grep dans tout le livre blanc : `prédit`, `prédiction`,
`prévoit`, `annoncera`, `prédire`, `prévoir`, `prédira`, `prédisent`,
`prédictions` (257 lignes contiennent au moins un de ces termes, sur
23 739 lignes ; liste complète avec section et contexte dans
`audit_prediction_897_hits.json`, SHA
`7c4e0b73757b21c398a301cccf35e688afa7c651fb3145a209b139c3b94a1158`).
Chaque ligne a été classée : présente-t-elle un RÉSULTAT comme une
prédiction ? Les négations, les stipulations de protocole, les
discussions de méthode et les questions ouvertes ne sont pas des
présentations de résultat comme prédiction — chacune est listée avec
sa raison.

**Comptage par catégorie (257 lignes).**

| Catégorie | Lignes | Jugement |
|---|---|---|
| Régression du couplage (§8.48 + sections T3) | 143 | Sens statistique testé — voir ci-dessous |
| Modélisation Delta (§8.39, §8.41, §8.42, §8.57, §8.62, §8.73, §8.47, §8.53, §8.35, §8.37) | 31 + ~20 dans « autre » | Évaluation de modèle, taux d'erreur donnés — conforme |
| Survie, formulations de verdict (§8.83, §8.12, §8.13, §8.16, §8.20 Chronos) | 20 + 3 | **REFORMULÉES par addendum (table A)** |
| Négations (« pas une prédiction du pipeline », « ne prédit pas », « pas de prédiction sans rigueur ») | 11 | Conformes — le livre se corrige déjà lui-même |
| Journal §7 (dont requalification pronostique) | 7 | Conformes — dont « stratification pronostique, pas prédiction par pseudo-temps » (ligne 31) |
| Citations par l'audit §8.90 | 5 | Renvoient aux reformulations (table A) |
| Questions ouvertes, stipulations, plans d'industriels, notes de sources | ~14 | Conformes avec raison (voir texte) |

**Table A — Addendum daté, 21 novembre 2026 (correction de Zackary).
Formulations de verdict reformulées en langage d'analyse. Texte
d'origine intact dans le livre blanc ; les reformulations ci-dessous
sont les formulations à lire à la place, à compter de cette section.**

| # | Localisation exacte | Formulation d'origine | Reformulation (analyse) |
|---|---|---|---|
| A1 | §8.12, ligne 382 | « KRAS, CA125, CEA et DPCR1 prédisent chacun une survie plus courte pris seuls » | « KRAS, CA125, CEA et DPCR1 sont chacun associés à une survie plus courte pris seuls (Cox univarié) » — mêmes HR, mêmes p |
| A2 | §8.13, ligne 394 | « **Survie : CA125 prédit une survie plus courte dans 2 cohortes sur 3** (TCGA : HR 1,44 univarié / 1,32 multivarié ; ICGC : 1,57 / 1,56 ; GSE71729 : non, 1,06) » | « **Survie : CA125 est associé à une survie plus courte dans 2 cohortes sur 3** (mêmes chiffres) » |
| A3 | §8.83, titre, ligne 19853 | « les gènes de privilège prédisent-ils la survie comme CA125 ? OUI, pour 3 items sur 8 » | « les gènes de privilège sont-ils associés à la survie comme CA125 ? OUI, pour 3 items sur 8 » |
| A4 | §8.83, verdict, lignes 19861–19862 | « AU MOINS UN gène de privilège prédit la survie comme CA125 : 3 items sur 8 sont dans la catégorie « PRÉDIT COMME CA125 » (Cox univarié… » | « AU MOINS UN gène de privilège est associé à la survie comme CA125 : 3 items sur 8 sont dans la catégorie « ASSOCIÉ COMME CA125 » (Cox univarié… » — mêmes critères (HR > 1, p < 0,05 dans ≥ 2/3 cohortes), mêmes gènes (TGFB2, HLA-G, score combiné) |
| A5 | §8.83, lignes 19870, 20060 | « FASLG et IDO1 ne prédisent rien nulle part » ; « 3 items sur 8 prédisent la survie comme CA125 (TGFB2, HLA-G, score) » | « FASLG et IDO1 ne sont associés à rien nulle part » ; « 3 items sur 8 sont associés à la survie comme CA125 (TGFB2, HLA-G, score) » |
| A6 | §7, ligne 245 (journal, §8.83) | « **3 items sur 8 PRÉDISENT COMME CA125** (Cox HR > 1, p < 0,05 dans ≥ 2/3 cohortes) — TGFB2, HLA-G et le score combiné » | « **3 items sur 8 ASSOCIÉS COMME CA125** (mêmes critères) — TGFB2, HLA-G et le score combiné » ; le titre cité devient « sont-ils associés à la survie comme CA125 ? » |
| A7 | §8.90, lignes 22736, 22808 (tables de vérification) | « 3 items sur 8 prédisent comme CA125 » ; « 3/8 prédisent comme CA125 sur ≥ 2/3 cohortes » | « 3 items sur 8 sont associés comme CA125 » ; « 3/8 associés comme CA125 sur ≥ 2/3 cohortes » — chiffres inchangés |
| A8 | §8.20, ligne 512 | « L'axe Chronos KRAS prédit la sensibilité chez les G12D : Spearman rho +0,47 (p=0,079, n=15) » | « L'axe Chronos KRAS est associé à la sensibilité chez les G12D : Spearman rho +0,47 (p=0,079, n=15) — direction juste, effectif trop petit pour conclure » |
| A9 | §8.48.3 (titre) + titres T3 (§8.51.5, §8.54.5, §8.55.6, §8.60.5, §8.61.5, §8.67.5, §8.68.5) | « Le couplage prédit S_sep — test principal » ; « Couplage prédit : la régression §8.48 tient, avant comme après » | « Le couplage est associé à S_sep, et l'association tient hors échantillon — test principal » ; « Couplage associé : la régression §8.48 tient, avant comme après » — le contenu du test (r = 0,954, H2/H3) est inchangé |

**Ce qui n'est PAS reformulé, avec la raison (sens statistique ou
méthodologique du mot « prédire », pas une prédiction du pipeline).**
- **Modélisation interne testée (§8.39, §8.41, §8.42, §8.57, §8.62,
  §8.73, §8.47, §8.53).** « Prédire la paire à ±0,10 », « r(prédit,
  vrai) », « la courbe réplique prédit » : un modèle ajusté sur des
  données, évalué sur des données tenues à l'écart, avec son taux
  d'erreur écrit (souvent un ÉCHEC : 46,8 %, 47,3 %, « NON ÉLUCIDÉ »).
  Le mot est employé au sens statistique — évaluer un modèle — et les
  verdicts disent déjà l'échec. Rien à reformuler : ce n'est pas un
  résultat du pipeline présenté comme une prédiction sur le monde.
- **« Prédictions gelées avant les runs » (§8.48.6).** Des prévisions
  écrites AVANT les runs, puis testées par les runs (H2/H3) — le sens
  scientifique du mot (une prévision testée par des données nouvelles),
  avec l'issue écrite. Conforme.
- **Négations (11 lignes).** « Pas une prédiction du pipeline »
  (§7 ligne 180 ; §8.20 ligne 503 ; §8.90 ligne 23040), « le pipeline
  ne prédit pas », « la construction ne prédit pas le verdict d'une
  paire » (§8.85.7, §8.88.7), « Le pilote ne prédit rien ici »
  (§8.84.1), « aucun flux ne prédit seul » (§7 ligne 29, R2 infirmé),
  « pas de prédiction sans rigueur ». Le livre se corrige déjà
  lui-même : ces lignes sont conformes à la règle du 21 novembre 2026.
- **Requalification déjà faite (§7 lignes 29 et 31).** « L'axe
  pseudo-temporel comme source prédictive hors échantillon (accuracy
  0,4612, p = 0,9581) » est un RÉSULTAT NÉGATIF sur la capacité
  prédictive (R2 infirmé), et « le projet est devenu de la
  stratification pronostique, pas de la prédiction par pseudo-temps »
  est la requalification elle-même. Conformes.
- **Questions ouvertes.** « Prédisent-ils… ? » (§8.82.7, ligne 19812),
  « la dépendance KRAS prédit-elle le bénéfice de la combinaison ? »
  (§8.22, ligne 571 — test non fait, faute de matrice) : des
  questions, pas des verdicts. Conformes.
- **« Prévoit » (4 occurrences).** Deux stipulations de protocole
  (« le protocole gelé ne prévoit pas de second bras », ligne 8750 ;
  « protocole §4.3 ne prévoit d'addendum qu'en cas de… », ligne
  21614 — « prévoir » = stipuler) et deux plans d'industriel
  (« Tango prévoit de lancer… une étude de phase 1/2 », lignes 19041
  et 19109 — le plan annoncé d'une entreprise, pas un résultat).
  Aucune n'est un résultat présenté comme une prédiction. « Annoncera »,
  « prédira », « prévoir » : 0 occurrence.
- **Notes de sources.** §8.78.10, ligne 18542 : « ni prédiction ni
  alerte opérationnelle » — une mention sur un dépôt de données, pas
  un résultat.
- **Synthèse §8.5 (lignes 23616–23669).** Ces lignes citent les
  verdicts de leurs sections d'origine : elles héritent de leur
  jugement — les citations de §8.48 relèvent de A9, celles de survie
  de A1–A8, celles de modélisation du sens statistique ci-dessus.

**Verdict partie 3 : 9 reformulations, par addendum daté (table A).**
Aucun chiffre ne change : seules les formulations de verdict passent
du langage de la prédiction à celui de l'association mesurée. Le reste
des 257 lignes est conforme avec raison écrite.

## 8.97.4 Partie 4 — Preuves de reproductibilité et de clarté, vérifiables par un lecteur extérieur

**Question.** Ce qui est sur GitHub est-il reproductible, clair et
propre — et comment un lecteur extérieur peut-il le vérifier
lui-même, sans nous croire sur parole ? Langage simple, moyen concret
de vérification pour chaque affirmation. Chaque preuve ci-dessous a
été re-vérifiée contre le dépôt réel le 21 novembre 2026 ; si une
preuve ne tenait plus, elle serait dite ici et corrigée — aucune ne
s'est effondrée, une précision de nom est corrigée (voir le script).

### 8.97.4.1 Ce qui prouve que le dépôt est REPRODUCTIBLE

**1. Le test à froid du §8.77 — reproduction exacte à 0,0.**
Ce que dit le livre blanc (§8.77, et journal ligne 239) : après
réparation, les flux TCGA v4 ont été reconstruits depuis les sources
et sont SHA-IDENTIQUES aux flux tenus (`e7a2adab…` et `895a4562…`,
identiques à l'octet), et les runs v6.2 redonnent les chiffres tenus
à **0,0 exact des deux côtés** (cascade, MC, maxsep, S_sep, Delta,
L7a, falsification), avec d_maxsep froid +0,29276219, égal au tenu.
Comment vérifier : lire §8.77 dans le livre blanc ; relancer les
deux runs TCGA v4 depuis les flux reconstruits et comparer les
chiffres au §8.77 — l'écart doit être 0,0 exact. Limite écrite au
§8.77 lui-même : le test à froid ne couvre que la paire TCGA v4, pas
la pérennité des liens de téléchargement.

**2. Le script de re-téléchargement — 52 fichiers, 2,4 Go, EXIT:0.**
Précision de nom (correction de cette section) : le script vérifié au
§8.77 s'appelle `download_data_877.sh`, pas `download_data.sh` — il
est dans `runs/pdac-v6/repro_877/download_data_877.sh` (323 lignes,
SHA `558111360ceda48bece577d7176a5ad5e46630f0a39fc85c03e8c3635564c78f`,
vérifié aujourd'hui, identique au SHA consigné au §8.77). Un fichier
`download_data.sh` existe aussi sous `staging-pdac/` (16 nov. 2026) :
ce n'est pas celui du test §8.77. Ce que dit le §8.77 : le script a
été exécuté en entier jusqu'à **EXIT:0 — 52 fichiers, 2,4 Go, tous
vérifiés** (36 déjà présents et vérifiés + 16 OK frais, 0 erreur).
Comment vérifier : `bash repro_877/download_data_877.sh`, attendre
EXIT:0, puis vérifier chaque fichier contre son SHA dans
DATA_SOURCES.md. Le dossier `data/` tient 168 fichiers, 2,9 Go,
présents localement au 21 novembre 2026.

**3. Chaque fichier avec sa source et son SHA — DATA_SOURCES.md.**
Le fichier vivant est `DATA_SOURCES.md`, **1 484 lignes, SHA
`dec70e17639348ac171c95f7f1128cef9918fc2f263b7c0bdd8d79e28bc47326`**
(dans le répertoire de construction `push_v62_892_build/`, état
§8.91–§8.92). Comment vérifier : ouvrir DATA_SOURCES.md, prendre
n'importe quelle ligne, suivre sa source (URL) et recalculer le
SHA-256 du fichier — il doit correspondre. Au §8.77, il faisait 900
lignes (SHA `17b8428b…`) ; il a grandi depuis avec les nouvelles
sections — c'est normal, il suit le livre blanc.

**4. Le pipeline v6.2, original intact — et v6.1, v6 intacts.**
SHA vérifiés aujourd'hui, 21 novembre 2026, avant et après les lots
du jour : v6.2 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
v6.1 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`,
v6 `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773` —
tous trois identiques aux SHA consignés depuis leur adoption.
Comment vérifier : `sha256sum runs/biophysique-hp35/universal_v6.*.0_cohen.py`
et comparer aux SHA ci-dessus et à ceux du §8.37 (§8.37) et du §7.
La copie v6.5 (§8.95, SHA `983ec65d…`) est une copie, jamais
l'original — et elle est rejetée, donc non adoptée.

### 8.97.4.2 Ce qui prouve qu'il est CLAIR

**1. Chaque verdict avec ses limites écrites.** Exemples vérifiables :
§8.87 (consolidation GDC FRAGILE, « réel sous le p95 des nuls »),
§8.88 (GSE194249 NON, « le nul sépare plus que le réel »), §8.94
Tier 1 (NON ÉLUCIDÉ, « aucun angle n'atteint la barre »), §8.95
(REJETÉE, « une seule porte échouée suffit »). Ouvrir n'importe
quelle section : le verdict est en tête, les limites sont dans la
section « Ce qui est établi, ce qui ne l'est pas ».

**2. Chaque correction par addendum daté, texte d'origine intact.**
Trois exemples vérifiables : (a) §8.70 porte un
« ADDENDUM — 20 novembre 2026 (§8.72) : NOTE DATÉE DE CORRECTION —
LECTURE RENVERSEE » — le verdict « sous le plancher » du §8.70 est
renversé par la distribution des 13 nuls du §8.72 (d_médian +0,1447),
et le texte d'origine du §8.70 est intact sous l'addendum ;
(b) l'audit §8.90 a ajouté des addenda datés du 21 novembre 2026
(volet 3, R2 ligne 45, R6 ligne 505, précision FDA ligne 521) —
reformulations proposées, texte d'origine intact ; (c) la coquille
de SHA dans PROVENANCE_889 §7, trouvée par l'audit §8.90 (I-1,
ligne 22749 : SHA tronqué faux, ligne 236, `examine_889.json`),
est consignée comme erreur de valeur — sa correction fait partie
des dettes ci-dessous.

**3. Chaque section avec son protocole gelé avant les runs et sa
provenance nommée.** Exemples : §8.93–§8.96 (protocoles gelés avec
SHA, addenda de la correction du 21 novembre 2026), §8.97 lui-même
(protocole `PROTOCOL_audit_regle_897.md`, SHA `fa04f4fe…`,
provenance `PROVENANCE_897.md`, SHA `5482fcac…`). Ouvrir n'importe
quelle section : le protocole est cité avec son SHA, la provenance
avec ses fichiers.

### 8.97.4.3 Ce qui reste comme DETTE CONNUE — nommé explicitement

Une dette nommée n'est pas un défaut caché — c'est la preuve que
l'audit est honnête. Dettes au 21 novembre 2026 :

1. **(Priorité haute) L'avertissement médical en tête du document
   est toujours absent.** Dette de gabarit de l'audit §8.90 : le
   livre blanc ne porte pas encore, en tête, l'avertissement
   « aucune recommandation clinique — données d'essais seulement, à
   discuter avec un oncologue ». Vérifié aujourd'hui : les 30
   premières lignes du livre blanc ne contiennent aucun avertissement
   médical. À ajouter à la prochaine fusion (ce lot, §8.93–§8.97).
2. **Entrées de journal à ajouter à la prochaine publication.**
   Dettes connues : le journal de la poussée e0e282d9 (06h51, 19
   novembre 2026) manque toujours ; les entrées des poussées
   §8.90–§8.92 sont à ajouter ; les deux corrections datées du
   21 novembre 2026 (A2 périmé « 9/13 » corrigé en 10/14 dans
   §8.84/§8.86, suffixes SHA MOESM5/7/8 corrigés dans
   PROVENANCE_884) sont dans le livre blanc local, en avance sur la
   poussée — à consigner dans le journal à la fusion.
3. **Coquille SHA PROVENANCE_889 §7** (audit §8.90, I-1) : SHA
   tronqué faux, ligne 236 (`examine_889.json`) — à corriger à la
   prochaine publication.
4. **Synchronisation du dépôt suite.** Le dépôt privé
   `FindPrint/tlogNext-cancer-pdac-suite` est mis à jour à chaque
   publication du lot ; sa copie de DATA_SOURCES.md dans le
   répertoire de préparation `push_ds_suite_sync/` (21 nov. 2026
   01h26, 702 lignes) est antérieure à l'état actuel (1 484 lignes)
   — la synchronisation fait partie de la fusion de ce lot, elle
   n'est pas faite au moment où cette section est écrite.
5. **Les 102 dossiers de runs défectueux (§8.32) restent sur le
   disque.** Ce n'est pas un oubli : ce sont les témoins du défaut,
   conservés exprès. Ils ne sont plus utilisés pour aucun verdict
   depuis §8.44 — mais un lecteur qui les ouvre sans lire §8.44
   pourrait les prendre pour des runs valides. La mention est ici
   pour qu'on ne les confonde pas avec les fichiers DEDUP propres.

**Verdict partie 4 : les preuves tiennent, les dettes sont nommées.**
Le dépôt est reproductible (test à froid 0,0 ; script EXIT:0 ;
sources + SHA ; pipeline intact) et clair (verdicts avec limites,
corrections par addendum, protocoles gelés) — et ce qui manque est
écrit ci-dessus, pas caché.

## 8.97.5 Provenance

Protocole gelé `PROTOCOL_audit_regle_897.md` (SHA
`fa04f4fee49648b7ad409a5323d75f3a61324f94bb40e3ca37dfec55a035370e`) ;
provenance `PROVENANCE_897.md` (SHA
`5482fcace62d307b40db0454c1c7d1f3bc939d8778dfbdb68fe05c2f5957183d`).
Balayage mécanique `audit_doublon_897.py` (SHA
`731dbe25f5cab43d1c5acc3cb13856c33cdbf5694167e46af15476bcfc10f5de`),
sortie `audit_doublon_897.json` (SHA
`e64d435932bdc5aed48d8344633e8edf59a70e2964d866673427cb43f8f975af`,
752 dossiers scannés, 650 propres, 102 avec `.1`, 2 répertoires
vides, 1 run en cours) ; occurrences de prédiction
`audit_prediction_897_hits.json` (SHA
`7c4e0b73757b21c398a301cccf35e688afa7c651fb3145a209b139c3b94a1158`,
257 lignes). Livre blanc audité : SHA `2606caf3…`, 23 739 lignes.
Versions : v6.2 SHA `f07567c4…`, v6.1 SHA `2af5e5ce…`, v6 SHA
`bb8bbdba…` — tous vérifiés inchangés le 21 novembre 2026. Aucun run
de pipeline dans cette section. Aucune recommandation clinique.
