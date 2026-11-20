# PROTOCOLE GELÉ — §8.69 : Confirmation indépendante pour `maxsep` (C3)

Date : 20 novembre 2026, 13h05 EST. Chantier §8.69, mission parent du
20 nov. 2026 (« confirmation indépendante pour maxsep », go de Zackary
« Fait tout cela », 13h04).
Ce protocole est gelé AVANT tout téléchargement, toute construction et
tout run. Aucun téléchargement sans ce fichier. Aucun paramètre ne
change après les résultats. Le livre blanc N'EST PAS édité, le PDF
N'EST PAS régénéré, rien n'est poussé sur GitHub dans ce chantier
(convention des chantiers ; fusion par le coordinateur). La section
§8.69 est écrite dans un FICHIER SÉPARÉ
(`section_8.69_maxsep_independent.md`).
Pipeline de travail : `universal_v6.2.0_cohen.py`, SHA-256
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(vérifié avant tout run ; le fichier n'est JAMAIS modifié ; v6.1
`2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`).

## 0. Contexte décisionnel — à lire avant tout le reste

- §8.56 : `maxsep` seul SUFFIT aux barres gelées (A1 37/48, A2 6/8
  avec 7/8 positifs, A3 HP35 +1,6512) ; `sep` seul REJETÉ (A2 5/8).
- §8.59 : ADOPTER SOUS CONDITION (D1, D2, D5 passent ; D3 et D4
  échouent — le verdict de suffisance tient à une paire et à
  l'échelle du plancher). Condition C3 : pleine adoption différée
  jusqu'à une confirmation indépendante portant A2 à 7/8.
- §8.64 : adoption sous condition CONFIRMÉE par troisième lecture
  (0 écart), convention d'affichage figée (maxsep principal, ancien
  MC secondaire, sep compagnon borné, mention de fragilité en tête
  de chaque table).
- **Le 20 nov. 2026 à 13h04, Zackary a décidé d'ADOPTER maxsep
  pleinement dès maintenant** (convention d'affichage : maxsep score
  principal, MC secondaire, aucun changement de code). **La
  confirmation indépendante du présent chantier devient donc une
  vérification a posteriori, pas une condition.** Si elle passe,
  elle consolide l'adoption ; si elle échoue, l'adoption pleine
  reste sa décision et la confirmation reste ouverte — à dire
  plainement dans les deux cas, dans la section comme dans le
  rapport. Ce chantier ne rouvre pas les §8.56/§8.59/§8.64 et ne
  change aucune décision de Zackary.

## 1. Les 8 paires principales déjà utilisées (V1, §8.56/§8.59/§8.64)

Valeurs reprises du §8.56.3 (re-vérifiées à l'identique aux §8.59
et §8.64, 0 écart). Écart = maxsep réel − maxsep nul (|d| de Cohen).
Plancher 0,07 en |d|.

| Paire | maxsep R / N | Écart | > 0,07 ? | Positif ? |
|---|---|---|---|---|
| HP35 | 1,7718 / 0,1206 | **+1,6512** | oui | oui |
| TCGA v4 | 0,4623 / 0,1696 | **+0,2928** | oui | oui |
| GSE71729 | 0,2593 / 0,2191 | +0,0402 | non | oui |
| GSE62452 | 0,3100 / 0,3136 | −0,0036 | non | NON (négatif, quasi nul) |
| ICGC | 0,4080 / 0,3110 | **+0,0970** | oui | oui |
| Immunitaire TCGA | 0,5309 / 0,1634 | **+0,3675** | oui | oui |
| PARP TCGA | 0,3680 / 0,1992 | **+0,1688** | oui | oui |
| DepMap | 0,4436 / 0,2532 | **+0,1904** | oui | oui |

Bilan V1 : **6/8 au-dessus du plancher, 7/8 positifs.** Échecs :
GSE71729 (+0,0402, sous le plancher) et GSE62452 (−0,0036, négatif).
Paire charnière : ICGC (+0,0970, passe le plancher littéral de
+0,0270 mais échoue au plancher équivalent-sep 0,1292).
À noter (hors V1, descriptif) : l'arm ICGC immunitaire, inversé
(−0,22 en S_sep, §8.47), n'est PAS une paire principale — il ne
compte ni dans V1 ni dans le présent chantier.

Rotations V2 (48 paires, §8.44, sans doublon) : 37/48 pour `maxsep`.
Elles ne sont PAS rejouées ici : le présent chantier ne porte que
sur UNE paire principale supplémentaire (C3), pas sur les rotations.

## 2. Paire choisie : GSE57495 — et pourquoi elle est vraiment indépendante

### 2.1 Choix

**Cohorte primaire : GSE57495, NCBI GEO** — cohorte PDAC de 63
patients, Moffitt Cancer Center (Tampa, FL, USA), Chen et coll.
2015, *PLoS ONE* 10(8): e0133562 (doi 10.1371/journal.pone.0133562),
« Prognostic Fifteen-Gene Signature for Early Stage Pancreatic
Ductal Adenocarcinoma ». Tumeurs réséquées, stades précoces
(IB, IIA, IIB). Dépôt GEO, série GSE57495, URL (même convention
FTP que les autres provenances) :
`https://ftp.ncbi.nlm.nih.gov/geo/series/GSE57nnn/GSE57495/matrix/GSE57495_series_matrix.txt.gz`

### 2.2 Justification d'indépendance (écrite avant tout téléchargement)

1. **Pré-enregistrée comme réserve, avant tout résultat.** GSE57495
   est la cohorte de repli désignée au §1.2 du protocole §8.66
   (`PROTOCOL_stomach_mucus_cohort4_866.md`), gelé le 20 nov. 2026
   AVANT tout téléchargement et tout résultat du §8.66 — et
   `PROVENANCE_866.md` consigne qu'elle est restée « non
   téléchargée, non utilisée ». Elle n'a été choisie par personne
   pour ses résultats : aucun résultat n'existe pour elle dans ce
   projet, sous aucune forme.
2. **Jamais utilisée dans ce projet.** Ni comme cohorte, ni comme
   paire principale, ni comme rotation, ni comme bras descriptif.
   Aucun CSV de flux, aucun run, aucun JSON, aucune valeur `maxsep`
   n'existe pour GSE57495 dans `~/workspace/runs/pdac-v6/`.
   Vérifié par grep sur `*.md` / `*.py` avant le gel : seules
   mentions = protocole §8.66 §1.2 et provenance §8.66 (réserve
   non utilisée).
3. **Nouveaux patients, nouveau centre, nouvelle plateforme.**
   Moffitt Cancer Center (Tampa) — aucun recoupement avec TCGA,
   ICGC PACA-AU, ni les cohortes GEO déjà utilisées (NCI pour
   GSE62452, autres centres pour GSE71729/GSE62165). Plateforme
   distincte (voir §2.3). Patients distincts (cohorte Moffitt
   2006–2011, 63 patients, stades précoces IB/IIA/IIB).
4. **Même construction que les autres paires principales GEO.**
   Variante (a) des builders `build_fluxes_geo71729.py` /
   `build_fluxes_geo62452.py` : les 12 mêmes gènes que la v4 TCGA,
   ordre = KRAS croissant, sans correction, cas complets, nul =
   lignes permutées graine 42 (§4). La paire est donc comparable
   aux 8 paires V1 par construction, et son issue est inconnue :
   aucun `maxsep` GSE57495 n'existe à ce jour, et rien dans les
   résultats publiés (signature pronostique de 15 gènes, survie)
   ne prédit l'écart réel−nul du pipeline.
5. **Pas un re-test déguisé.** Ce n'est ni une relecture d'un JSON
   existant (§8.64.7 : « pas une relecture : les relectures sont
   épuisées comme preuve »), ni une rotation déjà comptée, ni une
   sous-paire d'une paire V1 (nouveaux patients, pas un sous-ensemble
   de TCGA/ICGC/GEO déjà utilisés), ni un nouvel ordre sur des CSV
   existants (nouveaux CSV, nouveaux runs). Les paires GSE62165 du
   §8.66 (groupes G1–G5, autres constructions) sont explicitement
   EXCLUES comme paire principale du présent chantier, sauf comme
   repli technique (§3) — et dans ce cas avec une construction
   nouvelle (variante (a) 12 flux), jamais en reprenant leurs CSV.

### 2.3 CORRECTION d'une erreur du protocole §8.66 §1.2 — plateforme

Le protocole §8.66 §1.2 affirme que GSE57495 est sur « plateforme
GPL6244 (même plateforme que GSE62452, mapping déjà détenu) ».
**C'est faux.** Vérifié avant le gel du présent protocole par
recherche web (sources secondaires concordantes) : GSE57495 est
sur **GPL15048** — table de caractérisation (Wu et coll., *Sci
Rep* 2025 : « GSE57495 (GPL15048 platform) comprised 63 tumor
pancreatic tissue samples ») et tableau supplémentaire (Springer :
« GSE57495 63 GPL15048 »). L'article Chen et coll. 2015 précise
que les données viennent d'une puce « Rosetta/Merck Human RSTA
Custom Affymetrix 2.0 ». La plateforme exacte sera confirmée dans
l'en-tête de la matrice téléchargée (`!Series_platform_id`) et
consignée dans `PROVENANCE_869.md` ; si l'en-tête dit autre chose
que GPL15048, c'est consigné tel quel et la construction s'adapte
à la plateforme réelle (le mapping se construit depuis la table
de LA plateforme indiquée par la matrice, jamais depuis un
mapping d'une autre plateforme). **Le mapping GPL6244 détenu ne
sera PAS utilisé pour GSE57495.** Le mapping GPL15048 sera
construit à neuf (§4.1), par la même méthode en streaming que
`download_gpl6244_mapping.py` (arrêt après `!platform_table_end`).

### 2.4 Candidats écartés (enquête §8.66 §1.3, reprise telle quelle)

GSE15471 (39 < 40), GSE16515 (36 < 40), GSE32676 (25 < 40),
GSE28735 (45 mais pas de stade par échantillon exploitable),
GSE21501 (102 mais répartition des stades publiée incohérente +
plateforme Agilent GPL4133), GSE91035 (25 < 40), ICGC PACA-CA /
E-MTAB-6134 (accès hors périmètre). GSE62165 est la quatrième
cohorte du §8.66 — utilisée, donc exclue comme primaire, repli
technique seulement (§3).

## 3. Repli technique (gelé) : GSE62165, construction nouvelle

**Si et seulement si** la primaire GSE57495 est INUTILISABLE selon
les critères d'acceptation du §5 (téléchargement impossible,
plateforme sans table exploitable, n < 40, KRAS absent, < 12 gènes
v4 mappés, < 40 cas complets), alors — et alors seulement — la
paire est construite sur **GSE62165** (données déjà détenues :
`data/GSE62165_series_matrix.txt.gz`, SHA
`fd50fc415a31…03727f`, provenance `PROVENANCE_866.md`), avec la
MÊME construction variante (a) (§4), en runs FRAIS (nouveaux CSV
`pdac_869_geo62165_fluxes.csv`, nouveaux dossiers
`results_fast_v62_869_geo62165[_nul]`).

- Le repli ne s'applique JAMAIS après avoir vu le résultat de la
  primaire : si GSE57495 est utilisable et que sa paire échoue,
  l'échec est le verdict — on ne court pas après une autre cohorte.
- Indépendance du repli (à dire plainement dans la section) :
  GSE62165 a servi au §8.66, mais UNIQUEMENT pour des tests
  directs et des runs de groupes G1–G5 (autres listes de gènes,
  autres questions). La construction variante (a) 12-flux est
  nouvelle pour cette cohorte ; son `maxsep` n'est déterminé par
  aucune valeur du §8.66 (les S_sep/MC des paires de groupes ne
  portent pas sur ces CSV et n'entrent pas dans le verdict).
  C'est une indépendance de second rang (même cohorte que le
  §8.66) — la section le dira, et le verdict portera la mention.
- Si le repli est lui aussi inutilisable, le chantier s'arrête sur
  un blocage documenté (section §8.69 écrite quand même, avec les
  tentatives chiffrées, aucune valeur inventée).

## 4. Construction des flux — variante (a), comme les paires GEO V1

Nouveau script `build_fluxes_869.py` (copie adaptée de
`build_fluxes_geo62452.py`, original intact). Préfixe `_869_` pour
tous les fichiers du chantier.

### 4.1 Mapping sondes → symboles (GSE57495 / GPL15048)

- Télécharger en streaming la table de plateforme
  `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL15nnn/GPL15048/soft/GPL15048_family.soft.gz`
  (nouveau script `download_gpl15048_mapping_869.py`, adapté de
  `download_gpl6244_mapping.py` : arrêt après
  `!platform_table_end`), extraire ID → symbole depuis la
  colonne « Gene Symbol » si elle existe, sinon depuis
  « gene_assignment » (forme `accession // SYMBOLE // …`,
  première assignation, comme GPL6244) — la colonne utilisée
  est consignée dans `PROVENANCE_869.md`, jamais devinée.
- Sortie : `data/GPL15048_probe2symbol.tsv` (SHA consigné).
- Sondes multiples vers un même symbole : agrégation par médiane
  (règle du projet). Sonde sans symbole : non mappée. Sonde vers
  plusieurs symboles : exclue si ambiguë (règle consignée selon
  ce que la table permet ; aucune sonde mappée à la main).
- Pour le repli GSE62165 : mapping déjà détenu
  `data/GPL13667_probe2symbol.tsv` (SHA `c0a5e8fc…8c2b2`,
  `PROVENANCE_866.md`), réutilisé tel quel.

### 4.2 Série réelle (variante (a))

- Gènes v4 (les 12 mêmes que TCGA v4, ordre de la liste) :
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1,
  CEACAM5, CLCA1, MUC16.
- Contrôle : KRAS (expression puce brute, croissant). Le contrôle
  n'est JAMAIS un flux : pas de doublon.
- Tumeurs seules (caractéristiques `!Sample_characteristics_ch1`
  ; si la matrice ne contient que des tumeurs, c'est consigné
  tel quel ; si des non-tumeurs existent, elles sont exclues et
  comptées). Cas complets seulement (KRAS + 12 gènes présents),
  jamais d'imputation. Valeurs : log2 telles que fournies (nature
  exacte consignée dans `PROVENANCE_869.md` d'après l'en-tête
  de la matrice ; aucune renormalisation).
- Ordre stade : NON construit (les paires principales V1 sont en
  ordre KRAS ; GSE57495 est de toute façon quasi mono-stade
  précoce — IB/IIA/IIB — un ordre stade n'y mesurerait rien).
- Sorties : `pdac_869_geo57495_fluxes.csv` (+ `_nul.csv`) ;
  repli : `pdac_869_geo62165_fluxes.csv` (+ `_nul.csv`).
  Colonnes : `step` + 12 flux. SHA-256 consignés.

### 4.3 Nul

Bloc des flux permuté par lignes, graine 42, `rng(42)`, contrôle
(KRAS, ordre) intact — même convention que les paires V1
(§8.56.8, PROTOCOL_phase2 §2). Le nul est un échantillon
hypothétique, pas une mesure.

## 5. Critères d'acceptation de la cohorte (vérifiés après téléchargement, avant construction)

- Matrice téléchargée, HTTP 200, lecture complète vérifiée
  (nombre de lignes, 0 NaN ou NaN comptés) ; SHA-256 consigné
  dans `PROVENANCE_869.md` avant toute construction.
- Plateforme lue dans l'en-tête de la matrice ; table de
  plateforme téléchargeable et exploitable (colonne de symbole
  identifiée) — sinon ARRÊT, repli §3.
- n ≥ 40 tumeurs PDAC (minimum v6.2 fast) ; sinon ARRÊT, repli §3.
- KRAS présent comme ligne mappée ; sinon ARRÊT, repli §3.
- Les 12 gènes v4 présents (mappés) ; sinon ARRÊT, repli §3
  (aucun gène remplacé, aucun absent toléré pour une paire
  principale — la comparabilité aux 8 paires V1 l'exige).
- Cas complets (KRAS + 12 gènes) ≥ 40 ; sinon ARRÊT, repli §3.

## 6. Runs v6.2 (mode fast)

- Lot : 2 runs — réel + nul — manifeste `manifest_v62_869.txt`,
  lanceur reprenable existant `run_v62_lot.sh` (saute les sorties
  déjà complètes), journal `runs_v62_869.log` (SHA du pipeline
  en tête, exits consignés).
- Dossiers : `results_fast_v62_869_geo57495` et
  `results_fast_v62_869_geo57495_nul` (repli :
  `results_fast_v62_869_geo62165[_nul]`).
- Lancement en `systemd-run --unit=v62-869 --collect`
  (JAMAIS nohup — leçon AGENTS.md 2026-11-17), surveillance qui
  s'arrête d'elle-même à 2/2. Ne JAMAIS supprimer le dossier d'un
  run en cours. Si la machine redémarre, reprise sans perte
  (SKIP des dossiers complets, jamais de relance à l'aveugle).
- SHA du pipeline revérifié avant ET après le lot.

## 7. Critère de passage — GELÉ avant tout run

**La paire PASSE si et seulement si :**
`d_maxsep = maxsep_R − maxsep_N > 0,07` (plancher, en unités |d|,
gigue_eff = max(gigue mesurée, 0,07) — v6.2 déterministe, gigue
attendue 0, comme §8.56 §3) **ET** `d_maxsep > 0` (positif —
impliqué par > 0,07, mais consigné séparément comme au §8.56).

`maxsep` = `best_config.metrics.max_separation`, |d de Cohen|
maximal du scan, lu sur le best_config ANCIEN (sélection par
l'ancien composite) — mêmes définitions que §8.56.2. Le seuil MC,
la cascade, S_sep, Delta, L7a sont inchangés par construction.

**Verdict étendu (A2 à 9 paires) :**
- Si la paire passe : A2 étendu = **7/9 au-dessus du plancher,
  8/9 positifs** (les 8 paires V1 gardent leurs valeurs : 6/8 et
  7/8 positifs). La condition C3 du §8.59.8 est levée — la
  confirmation indépendante consolide l'adoption pleine décidée
  par Zackary le 20 nov. 13h04. Le leave-one-out sur les 9 paires
  est calculé en descriptif : retirer n'importe quelle paire
  passante laisse 6/8, qui satisfait encore la barre A2 d'origine
  (≥ 6/8) — l'adoption ne tient plus à une seule paire.
- Si la paire échoue : A2 étendu = **6/9, 7/9 ou 8/9 positifs
  selon le signe** (à consigner tel quel). C3 reste OUVERTE, la
  confirmation reste à trouver, et l'adoption pleine reste la
  décision de Zackary du 20 nov. 13h04 — ce chantier ne la
  rouvre pas et ne la conditionne pas.

Note sur le libellé du §8.59.8 : « porter A2 à 7/8 » y est écrit
de façon lâche — la lecture précise retenue ici est **7 paires
passantes sur 9 au total (7/9)**, et un leave-one-out dont le
pire cas (retrait d'une paire passante) laisse 6/8, soit la barre
A2 d'origine toujours satisfaite. C'est le sens opératoire de
« l'adoption ne tient plus à une paire ».

**Contrôles descriptifs (à publier, ne décident pas) :**
- `sep` compagnon (= maxsep/(1+maxsep)), ancien MC (secondaire),
  S_sep, Delta, L7a, cascade, falsification (indisponible sous
  n = 75 — GSE57495 n = 63 : noter « indisponible », ne pas
  imputer ; repli GSE62165 n = 118 : disponible) — affichés selon
  la convention §8.64.6 (maxsep principal, ancien MC secondaire,
  sep compagnon, mention de fragilité en tête de table).
- Plancher équivalent-sep (descriptif) : la paire passe-t-elle
  aussi `0,07·(1+m_R)(1+m_N)` ? Rapporté, non décisif (D4 n'est
  pas rejoué ici : il porte sur les 8 paires V1, déjà tranché).
- Aucun autre critère, aucune repondération, aucune redéfinition
  du plancher après avoir vu les chiffres.

## 8. Extraction et vérification

1. Extracteur propre du chantier, `extract_869.py` (SHA noté) :
   réutilise `extract()` de `extract_858.py` (original intact,
   comme `extract_866.py`) ; lit `maxsep`, `mc_score`,
   `stability`, `ssep`, `delta`, `l7a`, cascade, falsification
   dans les 2 `master_results.json` ; sorties
   `extract_869.json` / `extract_869.csv`.
2. Second calcul indépendant : relecture directe des 2 JSON par
   un chemin distinct (script `verify_869.py`, SHA noté) —
   `maxsep` et ancien MC recoupés à 0,0 exact ; tout écart =
   résultat à diagnostiquer, pas un bruit.
3. Recoupements : les 8 valeurs V1 reprises telles quelles du
   §8.56 (table `sep_maxsep_856_table.json`, SHA
   `ec5ee6382d5fd80d691ae7983ffbb31f14bb9074ded2bc6aad16327b1cc34f8b`),
   jamais recalculées ici — ce chantier ne re-vérifie pas les
   §8.56/§8.59/§8.64 (trois lectures, 0 écart, déjà closes).
4. SHA-256 de v6.2 revérifié après travaux, inchangé.

## 9. Règles du projet rappelées

- Pipeline aveugle : il ne voit ni T ni Tc ; la traduction et le
  jugement sont post-hoc, hors pipeline.
- Aucune conclusion d'une autre expérience n'est importée comme
  verdict : les tests directs du §8.66, la signature pronostique
  Chen et coll., les S_sep des paires de groupes ne prédisent
  rien ici — seul l'écart `maxsep` mesuré sur les 2 runs du
  présent chantier fait le verdict.
- Un nul qui invalide une piste est un résultat ; un échec de la
  paire est un verdict, pas un échec caché.
- Ne jamais présenter une lecture préliminaire comme un verdict.
- Aucun consensus exigé entre flux ou contrôles ; aucune
  affirmation clinique — l'étude porte sur l'instrument.

## 10. Livrables

- Ce protocole (gelé avant téléchargement, construction et runs).
- `PROVENANCE_869.md` (source, auteur, date, dépôt, URL, SHA-256
  des fichiers téléchargés, plateforme réelle, effectifs, exclus,
  mapping — avec la correction GPL15048 du §2.3).
- `download_gpl15048_mapping_869.py` + `data/GPL15048_probe2symbol.tsv`
  (repli : mapping GPL13667 déjà détenu, réutilisé tel quel).
- `build_fluxes_869.py` + CSV de flux (`pdac_869_*`, SHA consignés).
- `manifest_v62_869.txt`, `runs_v62_869.log`, dossiers
  `results_fast_v62_869_*`, `extract_869.json` / `.csv`,
  `verify_869.py` + sortie de vérification.
- §8.69 dans le FICHIER SÉPARÉ
  `section_8.69_maxsep_independent.md` (verdict d'abord, une
  phrase : A2 passe-t-elle à 7 paires passantes ou non ; chiffres
  ensuite ; détail complet après ; provenance nommée partout).
- Livre blanc NON édité. PDF NON régénéré. Rien poussé sur GitHub.

— Fin du protocole gelé §8.69. —

---

## ADDENDUM du 20 nov. 2026, ~13h40 EST — cohorte #3 (DERNIÈRE du chantier)

**Le corps gelé ci-dessus n'est pas modifié.** Le présent addendum est
ajouté après les faits qu'il consigne, avant tout téléchargement et
tout run de la cohorte #3. Aucun `maxsep` n'a été vu à ce jour dans
ce chantier (aucun run lancé, aucun CSV de flux écrit) : l'addendum
ne touche à aucun résultat, il élargit la recherche de cohorte.

**Faits déclencheurs (construction, pas des résultats).**
- Primaire GSE57495 : porte ÉCHEC — 11/12 gènes v4 (GSTM1 absent :
  aucune sonde à symbole exact GSTM1 ; seule la sonde partagée
  `merck-NM_000561_s_at`, annotée « GSTM1 GSTM2 GSTM4 », exclue
  comme ambiguë per §4.1). 63/63 cas complets sur 11 gènes.
- Repli GSE62165 : porte ÉCHEC — 10/12 gènes v4 (DPCR1 et GSTM1
  absents). 118/118 cas complets sur 10 gènes.
- Les deux cohortes sont donc inutilisables selon §5, sans qu'aucun
  run ait été lancé. Le repli §3 est épuisé ; la règle d'arrêt §3
  (« le chantier s'arrête sur un blocage documenté ») s'appliquerait.

**Vérifications d'indépendance faites avant cet addendum.**
- GSE78229 (50 échantillons, GPL6244) : EXCLUE — ses échantillons
  sont déjà inclus dans GSE62452 (résumé de la série : « The
  Affymetrix gene-expression data of these 50 samples were also
  included in the earlier submission by us as GEO accession number
  GSE62452 »). Re-test déguisé de la paire V1 GSE62452.
- GSE28735 (45 tumeurs + 45 normaux, GPL6244) : EXCLUE — ses
  échantillons sont ceux de GSE62452 (provenance §8.66 : les
  échantillons 1–90 de GSE62452 avaient été soumis comme GSE28735).
  Re-test déguisé de la paire V1 GSE62452.
- COAD / LUAD : EXCLUS — autres cancers (pas des paires
  principales PDAC) ET lots déjà courus (relecture, interdite par
  §8.64.7). CPTAC : EXCLU — protéine, 7/6 flux (pas 12), lots
  déjà courus. GSE15471 / GSE16515 / GSE32676 / GSE91035 : EXCLUS
  (n < 40, enquête §8.66 §1.3). GSE84219 (30) et GSE179351 (12) :
  EXCLUS (n < 40).

**Cohorte #3 — GSE21501 (DERNIÈRE du chantier).**
- Série GEO GSE21501, Stratford et coll., 102 patients PDAC,
  plateforme Agilent GPL4133. C'est la cohorte de validation
  indépendante du papier Chen et coll. 2015 (« evaluated using an
  independent microarray cohort dataset (Stratford et al: n = 102) »).
- Raison du choix : n le plus grand des candidats restants (102) ;
  indépendance documentée (cohorte Stratford, centre et patients
  distincts des cohortes V1) ; l'exclusion §8.66 §1.3 reposait sur
  le stade (répartition publiée incohérente : 73 stade I, 0 stade
  II) — inapplicable ici car l'ordre est KRAS uniquement (§4.2 :
  pas d'ordre stade construit).
- Mêmes portes (§5 : KRAS présent, 12 gènes v4 présents, ≥ 40 cas
  complets), même construction (§4, variante (a)), même critère de
  passage (§7), même nul (graine 42). Mapping à construire à neuf
  depuis la table de plateforme GPL4133 (colonne de symbole,
  même méthode en streaming que GPL15048/GPL6244 ; colonne
  utilisée consignée dans `PROVENANCE_869.md`).
- URL (même convention FTP) :
  `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE21nnn/GSE21501/matrix/GSE21501_series_matrix.txt.gz`
- Fichiers : `pdac_869_geo21501_fluxes.csv` (+ `_nul.csv`) ;
  dossiers `results_fast_v62_869_geo21501[_nul]` ; manifeste
  `manifest_v62_869.txt` ; extracteur / vérifieur avec
  `--tag geo21501`.

**Arrêt borné.** Si GSE21501 échoue aussi à ses portes, le chantier
s'arrête sur le blocage documenté (§3) : section §8.69 écrite avec
les tentatives chiffrées, aucune valeur inventée. **Aucune cohorte
#4 dans ce chantier.** La seule piste restante non vérifiée,
GSE79668 (51 cas, GPL11154, Illumina — indépendance et couverture
génique inconnues), est nommée ici comme piste pour un chantier
futur, pas tentée ici. L'addendum ne change ni les portes, ni la
construction, ni le critère de passage, ni les verdicts des deux
premières cohortes.

— Fin de l'addendum. —

