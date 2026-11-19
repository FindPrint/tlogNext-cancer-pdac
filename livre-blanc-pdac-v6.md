# Livre blanc — PDAC : chercher des pistes thérapeutiques avec UNIVERSAL_LOG v6

**Projet :** cancer du pancréas (PDAC), ARN + protéine + CRISPR + autres flux/données, pipeline UNIVERSAL_LOG v6.
**Mandat de Zackary :** 15 novembre 2026 — « Trouver un remède pour le cancer du pancréas en utilisant ARN, protéine et CRISPR et autre flux/data information et avec mon pipeline. Maintenir un livre blanc de tout ce que tu fais tester penser analyse connais connais pas. »
**Document vivant :** mis à jour à chaque étape (fait / testé / pensé / analysé / connu / inconnu). Rien n'est effacé : une correction remplace, elle ne supprime pas l'historique.
**Pipeline :** UNIVERSAL_LOG v6.0.0 (`universal_v6.0.0_cohen.py`, SHA `bb8bbdba…c0773`) — Cohen-d partout, Cliff retiré, preuve HP35 14 nov. 2026 (4/4 cascades identiques, ~11x plus rapide). Original v5.9.0f intact. **v6.1 :** copie validée le 16 nov. 2026 (§8.30, SHA `2af5e5ce…c1c9`) — adoptée comme version de travail le 16 nov. 2026, 18h34, sur le go de Zackary ; **devient la référence le 19 nov. 2026 (adoption v6.2).** **v6.2 :** copie validée le 19 nov. 2026 (§8.37, SHA `f07567c4…ec3abf`) — **adoptée comme version de travail le 19 nov. 2026, ~05h47, sur le go de Zackary (« Lance tout cela »).** La v6.0.0 reste intacte comme référence historique.
**Règle de provenance (permanente) :** chaque donnée, chaque résultat, chaque affirmation porte sa source complète (ouvrage/auteur/date/dépôt/URL), la nature des lignes (mesure instrumentale vs mot humain vs échantillon hypothétique), comment chaque valeur a été produite, les hachages, et ce qui manque.

---

## 1. Objectif, dit honnêtement

**But visé :** trouver des pistes thérapeutiques contre le PDAC — des cibles, des combinaisons, des moments d'intervention — en détectant des changements de régime dans des séries de flux multi-omiques réelles avec la v6.

**Ce que le pipeline fait vraiment :** il détecte des seuils et des cascades de seuils dans des séries ordonnées. Il ne trouve pas un remède tout seul. Il peut montrer *où* un système change de régime, *dans quel ordre* les flux réagissent, et *quels flux portent la tension* — ce qui pointe vers des cibles et des combinaisons à tester ensuite, jamais vers une conclusion clinique.

**Ce que ce livre blanc ne fera jamais :** présenter une piste comme un remède, présenter un seuil comme une preuve clinique, ou cacher un résultat négatif. Un nul qui invalide une piste est un résultat, il est noté ici comme tel.

---

## 2. État antérieur — ce qui est connu (projet tlog28, juillet–octobre 2026)

Projet d'origine : juillet 2026, UNIVERSAL_LOG v3.0 appliqué au PDAC — CSD, découverte de combinaisons thérapeutiques, simulation EDO. Code, données et figures reproductibles. Dépôt local `~/workspace/tlog28-cancer-pdac/` (original archivé intact, jamais touché) ; dépôt privé GitHub FindPrint/tlog28-cancer-pdac créé le 2 oct. 2026 (seul le README poussé à ce jour, envoi du contenu en pause) ; archive complète `tlog28-cancer-pdac-complet.zip` (17 Mo, 118 fichiers) dans ce dossier de projet.

Données réelles déjà utilisées : z-scores RNA-seq TCGA PAAD via cBioPortal, données cliniques TCGA, MSK, ctDNA longitudinales Pietrasz et al. 2017 (38 points).

**Résultats validés / invalidés (à ne pas répéter comme acquis) :**
- **R1 — infirmé :** le seuil pseudo-temporel à 7,3 % comme point de bascule (0/5 expériences).
- **R2 — infirmé :** l'axe pseudo-temporel comme source prédictive hors échantillon (accuracy 0,4612, p = 0,9581 ; aucun flux ne prédit seul).
- **R3 — confirmé en simulation EDO seulement :** le timing influence continûment l'issue.
- **Requalification :** le projet est devenu de la stratification pronostique, pas de la prédiction par pseudo-temps.
- **Balayage de raideur (~560 runs EDO, σ de 0,25 à 24 jours) :** durcir concentre la courbure (0,176 → 0,896), adoucir la disperse ; les seuils apparents à δ = 40/75/105 sont des sorties de phase de la fenêtre de protocole de 120 jours, pas de la criticité du système ; le levier b2 reste dominant à toutes les raideurs.
- **Conclusion durable :** ces résultats ne constituent ni validation clinique ni réhabilitation du pseudo-temps.

**À revoir — demande de Zackary, 15 nov. 2026, 07h34 :** l'axe pseudo-temporel invalidé n'est pas à jeter — l'échec lui-même peut apporter de l'information. À relire en détail (R1/R2/R3 + balayage de raideur) : pourquoi le seuil à 7,3 % apparaît puis disparaît après correction, ce que la stratification pronostique montre quand même, ce que la structure de l'échec dit de l'ordonnancement, et si une partie du signal survit sous une autre lecture. Témoin dormant, jamais détruit.

### 2.1 Relecture du 15 nov. 2026 — ce que l'échec apporte (lu dans les 4 rapports)

Sources relues : `~/workspace/tlog28-cancer-pdac/docs/VALIDATION_REPORT.md` (R1, 5 expériences), `VALIDATION_R2_REPORT.md`, `VALIDATION_R3_REPORT.md`, `EXPLORATION_STEEPNESS.md`. Ce qui suit est mesuré dans ces rapports, pas une opinion.

1. **Loi générale pour les scans de la v6 — le biais d'argmax (+9,3 pp).** Exp 1 : même avec un proxy PARFAIT (ordre exact, |ρ| = 1,0), le scan par argmax du |d de Cohen| place le seuil à 59–67 % au lieu du vrai 50 % — biais systématique de +9,3 pp sur 200 réplicats, pas du bruit. Mécanisme : l'argmax maximise le contraste standardisé pré/post, pas la position du coude. **Conséquence pour la v6 :** l'optimum Monte-Carlo de la v6 est aussi un maximum de contraste — un T0 ne doit jamais être lu comme « l'emplacement d'une bifurcation » sans confirmation indépendante (cascade, F1/F2, nul, rotation). Point positif : le test de permutation fonctionne (p < 0,05 dans 20/25 runs ordonnés).
2. **Deux flux survivent à tout : EMT_Invasion et Stroma_Desmoplasia.** Exp 5 (pipeline corrigé) : le 7,3 % disparaît, nouveau seuil ~82 % avec séparation faible (0,362 / 0,231, MEDIUM/LOW), et ce sont ces deux flux qui sont sélectionnés — plausibles pour une progression tardive, détection faible. **À reprendre en priorité** comme flux dans le nouveau travail TCGA.
3. **Le levier thérapeutique, c'est b2.** R3 + raideur : la transition phase 1→2 (ATR/G6PD → MRTX/venetoclax) domine à toutes les raideurs et dans toutes les analyses (24,3 pts de charge ; b2 ≫ b3 > b1, à tout σ). La combinaison ATR-i + G6PD-i et le timing du passage à MRTX/venetoclax sont l'hypothèse mécanistique la plus forte à tester contre DepMap/GDSC.
4. **Le chevauchement bat le séquençage net (intra-modèle).** Raideur : adoucir améliore le meilleur outcome (charge min 12,40 → 7,53) — la polythérapie partielle simultanée bat le séquençage net. Réserve : la sigmoïde « fuit » (à σ=24, activité pré-onset ~42 %) — c'est séquençage net contre polythérapie floue à démarrage précoce, pas deux phasages équivalents. Hypothèse à tester, pas conclusion.
5. **Lire les cascades comme des paysages d'influence, pas des interrupteurs.** R3 : le paysage d'onset est monotone et continu, SANS seuil discret (charge 12,31 → 78,91, +540 %) ; l'influence est répartie (24/34/37 % par tiers), densifiée vers le tardif, sans pic étroit pré-rupture ; point de rupture du système non traité : 81,17 j (transition douce, 2nd ordre). Le CTST a été reformulé : « optimiser le timing sur le paysage d'influence », pas « déclencher AU seuil ». La référence [15,45,80] perd contre +18 j ([33,63,98], −13,3 %, robuste 9/9) — ne pas s'ancrer sur les premiers seuils trouvés.
6. **Les pics de courbure à δ=40/75/105 sont des falaises de protocole, pas de la criticité.** Raideur : ce sont les points où des phases entières tombent hors de la fenêtre de 120 jours. Dans la région intérieure (δ ≤ 40), la courbure est faible à tout σ — aucun point-seuil n'émerge, même en quasi-marche.
7. **Biais de cohorte TCGA-PAAD :** patients opérés/résécables sur-représentés (stade IIB 68 %) ; IA (n=2), III (n=3), IV (n=3) minuscules. Survie par stade non monotone (IB 16,4 / IIA 15,8 / IIB 15,3 / III 17,8 / IV 17,9 mois). Tout résultat TCGA hérite de ce biais.
8. **Les négatifs sont solides (pas des instruments cassés) :** contrôles positifs prouvent que les tests détectent un vrai signal quand il existe (R2 : signal distribué → accuracy 0,9456, p=0,0196). Les invalidations sont des mesures. Limites connues : n=99 petit ; vote majoritaire dilue un signal porté par un seul flux (signal concentré : 0,64) ; dichotomie médiane de la survie.
9. **Drapeaux rouges à surveiller dans les runs v6 :** seuil qui isole un minuscule groupe extrême (le 7,26 % isolait le groupe à progression quasi nulle) ; colonnes dérivées de la variable d'ordonnancement (en exp 3, elles portaient la séparation publiée) ; ordonnancement par une variable de sortie (circularité, exp 4) ; affirmations CSD avec 4–5 points par patient (infaisable, exp 4).

**Conséquence directe pour ce nouveau mandat :** l'axe pseudo-temporel est invalidé comme axe de contrôle. Il faut un autre axe pour ordonner les séries (temps réel, progression clinique, dose, ordre de sensibilité, etc.). Cet axe est une question ouverte — voir §5.

---

## 3. Cadre de travail

- **Système :** PDAC humain — tumeurs, lignées, organoïdes selon les données disponibles.
- **Flux (familles) :** ARN (expression RNA-seq, simple-cellule), protéine (protéomique, phospho-protéomique), CRISPR (scores de dépendance / essentialité), sensibilité aux médicaments, clinique (survie, stade, ctDNA).
- **Contrôle :** à définir par source (voir §5) — jamais le pseudo-temps invalidé, jamais une variable importée sans justification.
- **Cible :** à définir par run (un flux mesuré, jamais une vérité terrain importée dans le pipeline).
- **Pipeline aveugle :** la v6 ne voit ni la variable de contrôle physique ni la vérité terrain. La traduction et les comparaisons se font après le run, dans le harnais, sans retour dans les paramètres.
- **Règle du 15 nov. 2026 (Zackary) :** les données et les conclusions des autres expériences ne sont PAS importées dans le travail du jour — elles restent des hypothèses à tester, jamais des entrées. Seules les données du jour et les runs du jour font les verdicts. L'état antérieur (§2) est du contexte, pas une preuve.
- **Exigence du 15 nov. 2026 (Zackary) :** tout doit être **traçable, reproductible, clair et public**. Traçable : chaque valeur porte sa source, sa méthode et son hachage. Reproductible : chaque run porte son protocole gelé, sa commande exacte, ses graines, ses versions. Clair : expliqué simplement, sans jargon — Zackary ne connaît pas ce domaine, et c'est à moi de rendre chaque résultat compréhensible. Public : le travail (livre blanc, données, résultats) doit pouvoir être montré et vérifié par d'autres. **Limite : le pipeline lui-même reste privé** (règle permanente de Zackary : jamais vendu ni exposé) — c'est le travail PDAC qui est public, pas le code du pipeline, sauf s'il me dit explicitement le contraire.
- **Témoins :** chaque run a son nul permuté (mêmes marginales, ordre temporel détruit). Un seuil qui survit au nul vaut d'être regardé ; un seuil que le nul reproduit ne prouve rien.
- **Rotation des contrôles :** chaque flux est testé en colonne de contrôle à tour de rôle. Jamais de verdict depuis un seul contrôle.
- **Seuils multiples :** on ne cherche pas UN seuil. On lit chaque seuil détecté et son pourquoi ; une chaîne causale de seuils critiques serait le résultat le plus intéressant.

---

## 4. Hypothèses (toutes à tester, aucune n'est un fait)

1. **H1 —** Des changements de régime existent dans l'expression ARN le long de la progression du PDAC, et la v6 peut les dater en ordre (quels gènes/voies bougent en premier).
2. **H2 —** La protéomique porte une information que l'ARN seul ne porte pas (les deux couches ne sont pas redondantes).
3. **H3 —** Les scores de dépendance CRISPR (DepMap) identifient des gènes essentiels propres aux lignées pancréatiques, et leurs variations le long d'un axe ordonné pointent des fenêtres de vulnérabilité.
4. **H4 —** Une combinaison (deux cibles dont les seuils se succèdent en chaîne causale) vaut plus qu'une cible seule.
5. **H5 —** Les seuils détectés sur données réelles survivent au nul permuté et à la rotation des contrôles (sinon ce sont des artefacts de construction).
6. **H6 —** Il existe un axe d'ordonnancement légitime autre que le pseudo-temps (temps réel, dose, progression) — à trouver par source, pas à supposer.

---

## 5. Ce que je sais / ce que je ne sais pas / ce que j'attends

### Je sais
- La v6 fonctionne et donne les mêmes seuils que la v5.9.0f en Cohen (vérifié sur HP35, 15 nov. 2026).
- Le pseudo-temps est invalidé comme axe prédictif sur TCGA (R1, R2).
- Les données TCGA PAAD (ARN + clinique) existent et sont accessibles ; DepMap, CPTAC, GEO existent aussi (à vérifier une par une).
- Le PDAC est un cancer à forte létalité, avec KRAS muté dans ~90 % des cas (connaissance scientifique générale — hypothèse de contexte, pas une mesure de ce projet).

### Je ne sais pas
- Quel axe ordonnera chaque série de flux (la question centrale, ouverte).
- Si les flux ARN/protéine/CRISPR porteront des seuils qui survivent au nul et à la rotation des contrôles.
- Si les cibles pointées par la v6 auront un sens biologique ou seront des artefacts.
- Quelles sources seront réellement téléchargeables et utilisables sur cette machine (2 vCPU, 7,7 Go RAM — pas de données brutes massives).
- Si une piste thérapeutique concrète émergera — c'est le but, pas une promesse.

### J'attends de voir
- Des cascades de seuils stables sur au moins une source réelle, avec un nul qui ne les reproduit pas en force.
- Des flux qui réagissent dans un ordre lisible (chaîne causale candidate).
- Des cibles qui reviennent dans plusieurs sources indépendantes (ARN + protéine + CRISPR).

---

## 6. Données — inventaire et provenance

*Section tenue à jour au fur et à mesure du repérage et des téléchargements. Chaque source : nom, auteur/date, dépôt, URL, accès, taille, hachage, nature des lignes, ce qui manque.*

### 6.1 Déjà présentes (projet tlog28)
- TCGA PAAD : z-scores RNA-seq via cBioPortal ; données cliniques TCGA ; MSK ; ctDNA Pietrasz et al. 2017 (38 points). Provenance détaillée dans le dépôt tlog28 (à recopier ici avec hachages).
- *À compléter après inventaire du 15 nov. 2026.*

### 6.2 Repérées / à télécharger — rapport du 15 nov. 2026, vérifié

Inventaire tlog28 confirmé : données réelles présentes = TCGA PAAD via cBioPortal (RNA-seq RSEM z-scores, ~70 gènes ciblés, 179 échantillons, `expression_matrix_real.csv`) + clinique 107 patients ; ctDNA MSK, 188 patients ; Pietrasz et al. 2017, VAF KRAS ddPCR longitudinal, 38 points / 9 patients ; dérivé `pdac_fluxes.csv` (10 scores de voies, 99 patients, ordonnés par survie décroissante = le pseudo-temps). Manques confirmés : pas de protéomique, pas de CRISPR, pas de sensibilité aux médicaments, pas de single-cell.

| # | Source | Provenance | Accès / taille | Statut vérifié le 15 nov. 2026 |
|---|--------|------------|----------------|--------------------------------|
| C1 | **DepMap Public 24Q4** — `CRISPRGeneEffect.csv` (Chronos) + `Model.csv` | DepMap, Broad Institute ; figshare article 27993248, DOI 10.25452/figshare.plus.27993248.v1 | Libre, sans compte, via figshare. `CRISPRGeneEffect.csv` = **428,7 Mo** (fichier 51064667), `Model.csv` = 0,6 Mo (51065297) | **CONFIRMÉ via API figshare.** Taille réelle supérieure à l'estimation (428,7 Mo, pas ~200). À télécharger en premier. |
| A1b | **TCGA-PAAD via Firehose** — matrice RSEM normalisée complète, 20 532 gènes × 183 échantillons | TCGA ; Broad GDAC Firehose stddata 2016-01-28, PAAD ; RNA-seq V2 RSEM normalisé (UNC Illumina HiSeq) | Libre, sans compte. Tarball 15 296 232 o, **MD5 vérifié `b09569ce…`** | **TÉLÉCHARGÉ et vérifié le 15 nov. 2026, 07h58.** 178 tumeurs primaires (code 01) retenues, 5 autres écartées (06/11). Flux v1 : 12 gènes de plus forte variance (PNLIP, CTRB2, CELA3A, CTRB1, CPA1, CELA2A, CPB1, CELA3B, CLPS, XIST, CTRC, CPA2 — SHA `e012e9fd…`). Flux v2 : mêmes règles, 40 gènes de pureté/sexe exclus (SHA `9d0b1ca8…`). Ordre des deux : expression KRAS croissante. Provenance : `PROVENANCE_tcga.md`, `PROVENANCE_tcga_v2.md`. |
| A1 | **TCGA-PAAD PanCancer Atlas 2018** via cBioPortal | TCGA ; Liu et al., *Cell* 2018 (PMID 29625055) ; étude `paad_tcga_pan_can_atlas_2018` | Libre, sans compte. ~10–30 Mo estimés, TSV | Étude **EXISTE** dans datahub (liste GitHub vérifiée), mais le lien S3 direct renvoie **403 Forbidden** et le README datahub (lu le 15 nov. 2026) ne donne aucune URL de téléchargement (notes de transformation seulement, sources GDAC Firehose). **Accès correct = API cBioPortal (https://www.cbioportal.org/api) — à mettre en place.** Non bloquant : les données TCGA 70 gènes existent déjà localement. |
| B1 | **CPTAC PDAC** — protéomique TMT, 140 tumeurs + 67 NAT, + phospho/glyco + ARN apparié | Cao et al., *Cell* 2021, 184:5031–5052 (PMID 34534465) ; PDC **PDC000393** ; tables via linkedomics ; étude cBioPortal `paad_cptac_2021` | Libre, sans compte (tables traitées). Quelques dizaines de Mo estimés, TSV | À vérifier au téléchargement. Cibles nommées par l'article : **PAK1/PAK2** (aval de KRAS). |
| D1 | **GDSC release 8.5** — dose-réponse ajustée (LN IC50 + AUC) | Garnett et al., *Nature* 2012 ; Iorio et al., *Cell* 2016 ; Sanger | Libre, sans compte. ~130 Mo estimés, XLSX | **LIENS MORTS : les deux XLSX renvoient 404** (vérifié 15 nov. 2026). FTP Sanger : releases jusqu'à 8.4 visibles, pas de 8.5. Nouvelle adresse à retrouver avant tout téléchargement. |
| A2 | **Single-cell PDAC — TISCH2** (Steele 2020 GSE155698, Lin 2020 GSE154778, Moncada 2020 GSE111672) | Steele et al., *Nat. Cancer* 2020 ; Lin et al., *Genome Med.* 2020 ; Moncada et al., *Nat. Biotechnol.* 2020 ; GEO + TISCH2 | Libre, sans compte. Quelques Mo par jeu, matrices traitées | En réserve, après les 3 premières. |
| D2 | **PRISM Repurposing 24Q2** | Corsello et al., *Nat. Cancer* 2020 ; DepMap ; figshare article 25917643 | Libre via figshare. Matrice primaire : plusieurs centaines de Mo (non vérifiée) | En réserve. |

**Versions à épingler :** DepMap 24Q4, GDSC 8.5, CPTAC PDC000393, cBioPortal PanCancer Atlas 2018. Sans version, l'analyse n'est pas reproductible.

**Avertissement central (confirmé par le repérage) :** aucune de ces sources ne fournit un axe temporel réel de progression tumorale chez le patient (sauf Pietrasz, déjà présent : 38 points — CSD infaisable). Toute série ordonnée par un score construit (survie, trajectoire inférée, rang d'AUC) est une hypothèse d'ordonnancement, pas un temps : elle exige un nul permuté et une validation externe.

---

## 7. Expériences

*Chaque expérience : protocole gelé avant le run, commande exacte, SHA du code et des données, sorties complètes, verdict. Aucun run sans protocole gelé.*

| # | Date | Données | Contrôle | Cible | Mode | Résultat | Verdict |
|---|------|---------|----------|-------|------|----------|---------|
| 1 | 15 nov. 2026, 07h39 | DepMap 24Q4, 45 lignées pancréas, 12 flux (voir §6.2 + PROVENANCE_depmap.md) | step (ordre = effet KRAS croissant) | EFR3A (1re colonne, politique fixe du pipeline) | fast v6 | **ÉCHEC technique, exit 1 en 4 s** : « Série trop courte : 45 points valides. Au moins 50 sont requis » (min_len 50, w_size 80). Idem pour le nul. Log : `runs_pdac_v6.log`. | Pas un verdict sur les données — la v6 n'a rien calculé. Mur à contourner (voir §10). |
| 1b | 15 nov. 2026, 07h39 | idem, nul permuté (graine 42) | step | EFR3A | fast v6 | **ÉCHEC technique, exit 1**, même raison. | Idem. |
| 2 | 15 nov. 2026, 07h59 | TCGA-PAAD Firehose, 178 tumeurs, 12 flux v1 (variance brute — voir §6.2 + PROVENANCE_tcga.md) | step (ordre = expression KRAS croissante) | PNLIP (1re colonne) | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 49,63 % → 88 / **T_0 60,90 % → 108** / 97,39 % → 173 (×2). MC optimum 66,30 %. L7a DOWN (34,7 % up / 49,9 % down, conf. 0,195). L7b FRAGILE. Régime divergence, Delta 3,68. Log `runs_tcga_v6.log`, sorties `results_fast_tcga_v1/` (36 fichiers). | L'ordre par KRAS porte l'information (voir §8). La v1 mesurant la pureté, le DOWN = les marqueurs acineux baissent quand KRAS monte. |
| 2b | 15 nov. 2026, 07h59 | idem, nul permuté (graine 42) | step | PNLIP | fast v6 | **TERMINÉ, exit 0.** Cascade 1,06 / 6,39 / **9,58** / 15,96 / 22,63. MC optimum 70,65 %. L7a UP 77,7 % (down 0 %). L7b FRAGILE. Régime divergence, Delta 4,30. | Le nul place son seuil ailleurs et vote à l'inverse. Delta ne distingue pas réel et nul. |
| 3 | 15 nov. 2026, 07h59 | TCGA-PAAD Firehose, 178 tumeurs, 12 flux v2 (variance hors 40 gènes pureté/sexe — voir PROVENANCE_tcga_v2.md) | step (ordre = expression KRAS croissante) | PNLIPRP1 (1re colonne) | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 29,55 % → 53 / **T_0 48,70 % → 87** / 58,35 % → 104 / 67,12 % → 120. MC optimum 66,30 %. L7a DOWN (31,9 % up / 52,0 % down, conf. 0,201). L7b FRAGILE. Régime divergence, Delta 3,74. | La v2 lit encore la pureté : à T_-1 les marqueurs acineux montent (+0,2 à +0,75 sd), à T_0 ils baissent tous (−0,36 à −0,67 sd). Voir §8. |
| 3b | 15 nov. 2026, 07h59 | idem, nul permuté (graine 42) | step | PNLIPRP1 | fast v6 | **TERMINÉ, exit 0.** Cascade 0,53 / 6,39 / **9,58** / 15,96 / 16,54. MC optimum 69,57 %. L7a UP 85,0 %. L7b FRAGILE. Régime divergence, Delta 4,30. | Nul : seuil au début, vote inverse. |
| 4 | 15 nov. 2026, 08h10 | TCGA-PAAD Firehose, 178 tumeurs, 12 flux v3 (résidus après régression sur 2 scores de pureté — voir PROVENANCE_tcga_v3.md) | step (ordre = résidu KRAS croissant) | XIST (1re colonne) | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 25,55 % → 45 / **T_0 89,57 % → 159** / 97,91 % → 174 (×2). MC optimum 14,13 %. L7a DOWN (39,7 % up / 46,2 % down, conf. 0,174). L7b FRAGILE. Régime divergence, Delta 3,84. | À T_0, XIST baisse (−0,52 sd) et les 6 gènes Y montent (+0,42 à +0,51 sd) : le seuil v3 est d'abord une frontière homme/femme, avec la baisse tumorale dessous (PGC −0,55, DPCR1 −0,40). Voir §8. |
| 4b | 15 nov. 2026, 08h10 | idem, nul permuté (graine 42) | step | XIST | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 49,63 / **61,32** / 88,01 / 88,01. MC optimum 55,43 %. L7a DOWN 85,7 % (conf. 0,420). L7b FRAGILE. Régime divergence, Delta 3,89. | Attention : le nul v3 vote DOWN lui aussi (fort). La direction ne distingue pas réel et nul en v3 — seule la position du seuil diffère (89,57 % contre 61,32 %). |
| 5 | 15 nov. 2026, 08h10 | TCGA-PAAD Firehose, 178 tumeurs, 12 flux v4 (v3 + exclusion des gènes du sexe — voir PROVENANCE_tcga_v4.md) | step (ordre = résidu KRAS croissant) | PGC (1re colonne) | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 74,06 % → 132 / **T_0 93,22 % → 166** / 98,44 % → 175 / 98,96 % → 176. MC optimum 10,87 %. L7a DOWN 86,3 % (up 0 %, conf. 0,408 — la plus forte des 4 versions). L7b FRAGILE. Régime divergence, Delta 4,18. Falsification delta_vs_null 0,849 (seuil 0,5). | **Le résultat le plus fort du jour.** Chaîne en deux temps : à T_-1, KRT20 −0,66 sd et CLCA1 −0,59 sd baissent, CEACAM5 +0,43 sd monte ; à T_0, PGC −0,89 sd, DPCR1 −0,85 sd, CLDN18 −0,46 sd s'effondrent, MUC16 +0,64 sd monte. Voir §8. |
| 5b | 15 nov. 2026, 08h10 | idem, nul permuté (graine 42) | step | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 10,65 / **15,96** / 67,12 / 67,12. MC optimum 81,52 %. L7a UP 45,1 % (conf. 0,167, faible). L7b FRAGILE. Régime divergence, Delta 3,77. | Nul : seuil au début, vote inverse et faible. La v4 sépare réel et nul sur la position ET le sens. |
| 6 | 15 nov. 2026, 08h33 | **CPTAC PDAC PDC000393, centre UMich, 63 tumeurs** (cas complets, 7 flux protéiques : PGC, REG4, CLDN18, KRT20, CEACAM5, CLCA1, MUC16 — voir PROVENANCE_cptac.md) | KRAS protéique croissant | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 1,69 % → 1 / **T_0 4,69 % → 3** / 25,00 % → 16 (×2). MC optimum 19,35 %. L7a UP mais **probabilités NaN, conf. 0,5 (dégénéré)**. L7b FRAGILE. Régime criticité, Delta 1,48. | **Non-confirmation.** Le T_0 tombe au tout début (3 points avant) ; le test direct s'inverse entre top 4 et top 12. Voir §8.8. |
| 6b | 15 nov. 2026, 08h33 | idem, nul permuté (graine 42) | KRAS protéique | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 44,40 / **51,65** / 54,91 / 68,15. MC optimum 58,06 %. L7a UP, NaN aussi. L7b FRAGILE. Régime criticité, Delta 1,49. | Delta réel ≈ Delta nul (1,48 contre 1,49) : le pipeline ne sépare pas réel et nul en protéine. |
| 7 | 15 nov. 2026, 08h33 | **CPTAC PDAC PDC000393, centre BCM, 52 tumeurs** (cas complets, 6 flux — MUC16 exclue, 48/52 < 50) | KRAS protéique croissant | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 5,71 / 59,64 / **T_0 63,26 % → 33** / 69,04 (×2). MC optimum 23,81 %. L7a UP, **NaN**. L7b FRAGILE. Régime criticité, Delta 1,55. | **Non-confirmation.** Le T_0 à 63 % n'a aucun mouvement de flux derrière lui (+0,01 à +0,33 sd). Voir §8.8. |
| 7b | 15 nov. 2026, 08h33 | idem, nul permuté (graine 42) | KRAS protéique | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 15,22 / **20,93** / 32,40 / 46,64. MC optimum 23,81 %. L7a UP, NaN. L7b ROBUSTE (non informatif — verdict clos). Régime criticité, Delta 1,52. | Delta réel ≈ Delta nul (1,55 contre 1,52). |
| 8 | 15 nov. 2026, 08h52 | Rotations de contrôle v4 — **KRAS-valeur** (même ordre, contrôle = valeur du résidu KRAS au lieu du rang step) | KRAS_resid | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 74,06 / **93,22** / 98,44 / 98,96 — **IDENTIQUE à la v4, chiffre par chiffre**. L7a DOWN 85,8 % (conf. 0,404). Delta 4,18. MC optimum 10,87 %. | La métrique du contrôle ne change rien : le résultat ne dépend pas du rang uniforme. Voir §8.9. |
| 8b | 15 nov. 2026, 08h52 | idem, nul permuté (graine 42) | KRAS_resid | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 10,65 / **15,96** / 67,12 / 67,12. L7a UP 45,1 % (conf. 0,167). Delta 3,77. | Identique au nul v4 — cohérent, même ordre. |
| 9 | 15 nov. 2026, 08h52 | Rotations — **CLDN18** comme contrôle (lignes triées par CLDN18 croissant) | CLDN18 | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 4,26 / 46,59 / **84,42** / 91,14 / 91,14. L7a UP 85,5 % (conf. 0,417). Delta 3,86. | Pas de discrimination : le nul vote pareil (UP 86,3 %). La chaîne est spécifique à l'axe KRAS. Voir §8.9. |
| 9b | 15 nov. 2026, 08h52 | idem, nul permuté (graine 42) | CLDN18 | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 1,06 / 34,29 / **60,38** / 97,39 / 97,39. L7a UP 86,3 % (conf. 0,420). Delta 3,80. | Nul quasi identique au réel sur le vote. |
| 10 | 15 nov. 2026, 08h52 | Rotations — **pureté** comme contrôle (lignes triées par score acineux croissant, témoin négatif) | score_acineux | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 3,19 / 24,57 / **42,52** / 59,37 / 59,37. L7a UP 53,4 % (conf. 0,198, faible). Delta 3,10. | **Aucune chaîne** : vote faible, mouvements modestes et uniformes (−0,13 à −0,55 sd). Le témoin négatif se comporte comme attendu. Voir §8.9. |
| 10b | 15 nov. 2026, 08h52 | idem, nul permuté (graine 42) | score_acineux | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 59,37 / **81,51** / 94,26 / 94,26. L7a DOWN 58,2 % (conf. 0,225). Delta 3,77. | Vote faible aussi — rien de fort ni d'un côté ni de l'autre. |
| 11 | 15 nov. 2026, 08h52 | Rotations — **miroir** (ordre KRAS décroissant, contrôle step) | step | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 1,06 / 46,59 / **60,38** / 84,86 / 84,86. L7a DOWN 86,2 % (conf. 0,431). Delta 3,96. | **La chaîne est dans les données, miroir exact flux par flux** (voir §8.9), mais la cascade ne place pas son T_0 au miroir (60,38 % au lieu de ~6,8 %) et L7a ne se retourne pas — deux comportements de l'instrument à noter, pas des verdicts sur les données. |
| 11b | 15 nov. 2026, 08h52 | idem, nul permuté (graine 42) | step | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 0 / 61,80 / **98,44** / 100,00 / 100,00. L7a UP 85,3 % (conf. 0,406). Delta 3,80. | Nul : seuil au bout, vote inverse. |
| 12 | 15 nov. 2026, 09h16 | **GEO GSE71729, 145 tumeurs primaires** (Moffitt 2015, puce Agilent GPL20769 ; variante (a) : les 12 mêmes gènes que la v4 TCGA — voir PROVENANCE_geo71729.md) | KRAS croissant | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 1,31 / 43,85 / **76,77 % → 111** / 89,70 / 89,70. L7a UP 82,1 % (conf. 0,416). Delta 2,16. | **Non-confirmation.** À T_0 les gènes montent (+0,18 à +0,65 sd) au lieu de s'effondrer. Test direct top 12 : CLDN18 **+0,68**, MUC16 +0,67, DPCR1 +0,60 — l'inverse de TCGA. Voir §8.10. |
| 12b | 15 nov. 2026, 09h16 | idem, nul permuté (graine 42) | KRAS | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade — T_0 **7,84 %**. L7a UP 85 % (conf. ~0,42). Delta 2,20. | Réel ≈ nul (Delta 2,16 contre 2,20, L7a UP des deux côtés) : pas de séparation. |
| 13 | 15 nov. 2026, 09h16 | GEO GSE71729 — variante (b) : re-sélection fraîche protocole v4 (top 12 : CABP7, DMBT1, PPY, C4orf7, TFF2, RPA4, DES, PPY2, IGH@, REG4, CCL19, SPINK4 — seul REG4 recoupe la v4) | KRAS croissant | CABP7 | fast v6 | **TERMINÉ, exit 0.** T_0 **25,09 %**. L7a UP 82,8 % (conf. 0,398). Delta 2,96. | Réel et nul placent leur seuil au même endroit (25,09 % contre 24,44 %) — pas de chaîne. |
| 13b | 15 nov. 2026, 09h16 | idem, nul permuté (graine 42) | KRAS | CABP7 | fast v6 | **TERMINÉ, exit 0.** T_0 **24,44 %**. Delta 2,90. | Seuil au même endroit que le réel. |
| 14 | 15 nov. 2026, 09h16 | GEO GSE71729 — variante (c) : les 12 mêmes gènes, corrigés de la pureté par régression, ordre résidu KRAS | résidu KRAS | PGC | fast v6 | **TERMINÉ, exit 0.** T_0 **41,11 %**. L7a UP 83,1 % (conf. 0,429). Delta 2,93. | À T_0 : CEACAM5 −0,70, REG4 −0,46, CLDN18 −0,19, MUC16 +0,05 — aucun effondrement. La correction de pureté ne retourne pas le sens. |
| 14b | 15 nov. 2026, 09h16 | idem, nul permuté (graine 42) | résidu KRAS | PGC | fast v6 | **TERMINÉ, exit 0.** T_0 **85,68 %**. Delta 2,66. | — |
| 15 | 15 nov. 2026, 10h11 | **GEO GSE62452, 69 tumeurs** (puce Affymetrix HuGene-1.0-st, plateforme réelle GPL6244 — pas GPL570 comme annoncé ; variante (a) : les 12 mêmes gènes que la v4 TCGA — voir PROVENANCE_geo62452.md) | KRAS croissant | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 1,42 / 35,67 / **95,64 % → 66** / 98,64 / 100,00. L7a UP, **NaN** (dégénéré, comme CPTAC). Delta 1,41. | **OUI, 3/3.** Test direct top 12 : MUC16 **+0,48 sd**, CEACAM5 **+0,63** (rho +0,441, p=0,0001), DPCR1 +0,93, CLDN18 +0,55 — l'effondrement ne réapparaît pas. Voir §8.13. |
| 15b | 15 nov. 2026, 10h11 | idem, nul permuté (graine 42) | KRAS | PGC | fast v6 | **TERMINÉ, exit 0.** T_0 **17,10 %**. Delta 1,26. L7a NaN. | Nul : tout entre −0,38 et +0,45 sd. Pas de séparation réel/nul sur la cascade. |
| 16 | 15 nov. 2026, 10h11 | GEO GSE62452 — variante (b) : re-sélection fraîche protocole v4 (top 12 : DPCR1, CEACAM5, PPY, SLC6A14, CRP, OLFM4, GABRP, CRISP3, CP, IGJ, RNU5D-1, HLA-DRB5) | KRAS croissant | DPCR1 | fast v6 | **TERMINÉ, exit 0.** T_0 **79,67 %**. L7a UP, NaN. Delta 1,37. | La sélection indépendante retrouve DPCR1 (rho +0,394, p=0,0008) et CEACAM5 (rho +0,372, p=0,0016) qui montent avec KRAS — preuve convergente. |
| 16b | 15 nov. 2026, 10h11 | idem, nul permuté (graine 42) | KRAS | DPCR1 | fast v6 | **TERMINÉ, exit 0.** T_0 **84,02 %**. Delta 1,40. | Réel et nul au même endroit — pas de séparation. |
| 17 | 16 nov. 2026, 07h08 | **Survie GSE71729** (125 tumeurs avec survie, 84 décès ; survie dans les ch2 de la matrice — aucun fichier clinique séparé) : paysage 7 définitions + Cox continu | — | — | hors pipeline (KM/log-rank/Cox) | **TERMINÉ. PARTIEL.** Quartile KRAS 10,0 contre 19,0 mois (p=0,020) ; top12 rien (17,0 contre 17,0, p=0,89). Cox univarié KRAS 1,24 (p=0,075), MUC16 1,06 (p=0,58), CEACAM5 1,00. | KRAS tient en direction, CA125 ne confirme pas, top12 ne confirme pas. Voir §8.15. |
| 18 | 16 nov. 2026, 07h30 | **Vérification indépendante de la survie TCGA (§8.12)** : script sauvegardé `survival_tcga_verify.py` (SHA `937bdb6e…dade2`), refait depuis les données ; Cox vérifié par 3 implémentations, log-rank par 2 | — | — | hors pipeline (KM/log-rank/Cox) | **TERMINÉ. CORRECTION.** Le tableau « univarié » du 15 nov. était l'ajustement à 6 gènes, mal étiqueté. Vrais univariés : KRAS 1,42 (p=0,0003), MUC16 1,44 (p=0,001), CEACAM5 1,31 (p=0,011), DPCR1 1,43 (p=0,001). Multivarié confirmé : 1,33/1,32/1,07. Paysage refait : top12 p=0,017, top20 p=0,0415, quartiles et double-quartile non significatifs. | La conclusion se renforce. Voir §8.12 (correction en tête de section). |
| 19 | 16 nov. 2026, 07h08 | **ICGC PACA-AU, 70 tumeurs** (Bailey et al. 2016 ; DCC mort, expression via UCSC Xena, survie via Bailey Suppl. Table 1) — variante (a) : les 12 mêmes gènes, ordre KRAS croissant | KRAS croissant | PGC | fast v6 | **TERMINÉ, exit 0.** Cascade 1,41 / 9,84 / **52,31 %** / 94,27 / 94,27. L7a UP, **NaN** (n=70 < 75, §8.14). Delta 1,44. | **Expression NON : 3/4.** Test direct top12 : MUC16 **+0,13**, CEACAM5 **+0,28** — dans le bruit du nul (−0,53 à +1,28). Voir §8.16. |
| 19b | 16 nov. 2026, 07h08 | idem, nul permuté (graine 42) | KRAS | PGC | fast v6 | **TERMINÉ, exit 0.** T_0 **32,43 %**. Delta 1,37. L7a NaN. | Pas de séparation réel/nul. |
| 20 | 16 nov. 2026, 07h08 | **Survie ICGC** (70 tumeurs, 47 décès OS) : paysage 7 définitions + Cox continu (expression brute) | — | — | hors pipeline (KM/log-rank/Cox) | **TERMINÉ. CA125 OUI, FORT.** Quartile MUC16 9,5 contre 23,8 mois (p=0,002, vérifié 2 implémentations). Cox univarié MUC16 1,57 (p=0,008), multivarié 1,56 (p=0,008), ajusté sous-type 1,75 (p=0,004) ; KRAS 1,25 (p=0,12), CEACAM5 0,80 (p=0,16). | Survie CA125 : 2/3 cohortes. Voir §8.16. |
| 21 | 16 nov. 2026, 07h08 | **Médicaments ciblés KRAS, dose-réponse GDSC2** (269 composés, 27 lignées pancréas, jointure DepMap par SANGER_MODEL_ID) : Spearman LN_IC50 et AUC contre Chronos KRAS + tertiles + FDR | — | — | hors pipeline (criblage) | **TERMINÉ. NON.** Aucun inhibiteur MEK/ERK/RAF/KRAS significatif (meilleur : ERK_2440 rho +0,246, FDR 0,385 ; sélumétinib +0,217, FDR 0,402). Médiane rho des 269 = −0,295 (lignées KRAS-dépendantes globalement plus résistantes). Seul FDR < 0,05 : staurosporine, direction négative (curiosité). Inhibiteurs KRAS de clinique absents de GDSC2 (sotorasib, adagrasib, MRTX1133). | Pas de piste médicamenteuse pour le groupe KRAS fort. Voir §8.17. |
| 22 | 16 nov. 2026, 07h42 | **Thérapies ciblées MUC16 et CLDN18.2** : revue des thérapies (sources nommées, 3 pivots vérifiés indépendamment) + vérification mesurée sur les 4 cohortes (fractions au-dessus des seuils, chevauchement KRAS fort) + TCGA clinique (chimio ? radiothérapie ?) | — | — | hors pipeline (revue + tests directs) | **TERMINÉ.** MUC16 : NON — 0 réponse chez 11 patients pancréatiques (DMUC5754A) ; rien d'autre de clinique. CLDN18.2 : piste réelle mais précoce — zolbetuximab ÉCHEC randomisé (GLEAM 13,7 vs 13,6 mois, HR 0,999) ; IBI343 phase I 22,7 % de réponses, phase III en cours (NCT07066098). Nos cohortes : KRAS fort enrichi en MUC16 et CLDN18 élevés (3/4) ; double-positifs 0–2/12 — pas de base pour une combinaison. TCGA : aucune donnée de chimio ; radiothérapie sans effet sur le signal CA125. | Aucun remède démontré. La piste à suivre : IBI343 (phase III). Voir §8.18. |
| 23 | 16 nov. 2026, 07h41 | **Médicaments en dose-réponse, PRISM secondaire 19Q4** (1 427 composés, 29 lignées pancréas ; miroir figshare Corsello et al. Nat Cancer 2020, MD5 vérifié — portail DepMap bloqué par Cloudflare) : Spearman AUC et log10(IC50) contre Chronos KRAS + tertiles corrigés + FDR | — | — | hors pipeline (criblage) | **TERMINÉ. NON.** Zéro composé FDR < 0,05 (FDR min 0,418 en AUC, 0,619 en IC50). Médiane rho −0,013, symétrique. MEK plat (+0,008, 18 composés). Inhibiteurs KRAS de clinique absents (secondaire de 2019). | Les 3 criblages convergent vers le même négatif. Reste non testé : inhibiteurs KRAS directs et combinaisons. Voir §8.19. |
| 24 | 16 nov. 2026, 07h42 | **Inhibiteurs directs KRAS G12D / pan-RAS** : présence par nom dans PRISM/GDSC2/secondaire + test par allèle KRAS (MAF DepMap 24Q4, 54 lignées) + revue essais (sources nommées) | — | — | hors pipeline (test direct + revue) | **TERMINÉ. OUI pour un seul.** MRTX1133 tue les G12D : viabilité −1,70 contre −0,38, Mann-Whitney p=0,0001 ; Chronos prédit la sensibilité chez les G12D (rho +0,47, p=0,079, n=15 — suggestif). Essai MRTX1133 TERMINATED (formulation/PK). **Daraxonrasib (RMC-6236) : FDA approuvé 26 août 2026, RASolute-302 OS 13,2 contre 6,7 mois, HR 0,40 — vérifié indépendamment.** Aucune matrice publique pour RMC-6236/9805/ASP3082/sotorasib/adagrasib. | Première avance réelle du dossier : un médicament approuvé qui double la survie médiane — pas un remède, pas une prédiction du pipeline. Voir §8.20. |
| 25 | 16 nov. 2026, 07h42 | **Balayage CRISPR génome entier** (47 lignées pancréas, 17 787 gènes testés, Spearman contre Chronos KRAS + FDR + nul permuté graine 42) | — | — | hors pipeline (criblage génétique) | **TERMINÉ. 2 hits faibles, pas un remède.** TCF7L2 rho +0,614 (FDR 0,039), PRDX4 +0,602 (FDR 0,045) ; nul 0 hit. Essentialité absolue faible (−0,43 / −0,25) ; TCF7L2 non druggable, PRDX4 sans médicament connu. Aucun candidat connu significatif (RAF1/PLK1/BCL2L1 top ~50–70, FDR 0,45–0,49). | Le côté CRISPR est épuisé sur ces données. Voir §8.21. |
| 26 | 16 nov. 2026, 07h58 | **Combinaisons** : revue ciblée (11 sections, sources nommées, NCT) + matrice PANC-1 (496 paires, NCATS) + recherche d'une matrice multi-lignées pancréas (ALMANAC, AZ-DREAM, O'Neil, DrugComb) | — | — | hors pipeline (revue + test direct) | **TERMINÉ. OUI — vopimetostat + daraxonrasib, MTAP-délétés : 82 % de réponses (18/22), contrôle 100 %, PFS 9 mois 88 %, médiane non atteinte (phase 1/2 NCT06922591, ESMO 2026 — vérifié indépendamment).** Non randomisé, n=22, pas de survie globale ; phase 3 prévue 1H 2027. MEK + autophagie : ÉCHEC clinique. MEK + CDK4/6 : échec. PANC-1 : 280/496 synergiques, top panobinostat + carfilzomib (gamma 0,035), zéro paire MEK/KRAS/ERK/HCQ. Aucune matrice multi-lignées pancréas publique — le test axe × combinaison n'a pas pu être fait. | La piste la plus solide du projet après le daraxonrasib seul. Voir §8.22. |
| 27 | 16 nov. 2026, 08h57 | **Paysage immunitaire le long de l'axe KRAS, runs v6** (4 cohortes, 12 gènes, KRAS brut croissant, réel + nul, 8 runs v6 fast) | v6.0.0-Cohen, fast | KRAS brut | réel + nul (graine 42) | **TERMINÉ. OUI, la tumeur devient froide : T baissent dans les 4 cohortes (PDCD1 significatif partout, top-12 −0,61 à −0,88) ; PD-L1 ne monte qu'en TCGA (+0,26) et top-12 ns partout. KRAS + anti-PD-(L)1 : NON.** v6 ne sépare pas réel/nul (MC ICGC réel sous le nul). L7a UP 50 % = repli NaN (n<75). | ARN bulk sans correction de pureté — composition ou expression, mécanisme non établi. Voir §8.23. |
| 28 | 16 nov. 2026, 08h57 | **Paysage réparation/PARP le long de l'axe KRAS, runs v6** (TCGA 178, 12 gènes, KRAS brut croissant, réel + nul, 2 runs v6 fast + contrôle GEO 145) | v6.0.0-Cohen, fast | KRAS brut | réel + nul (graine 42) | **TERMINÉ. OUI, mais pas côté PARP : BRCA2 +0,420, ATR +0,407, POLQ +0,289 (Bonferroni) ; répliqués BRCA2/ATR/RAD51 en GEO. PARP1/PARP2 plats partout. KRAS + PARP : NON (3 angles négatifs). Piste : ATR/CHEK1.** v6 ne sépare pas réel/nul. | Prolifération non contrôlée ; indication BRCA germinale non concernée. Voir §8.24. |
| 29 | 16 nov. 2026, 09h28 | **Re-test ATR/CHEK1** (TCGA 178 : correction pureté + contrôle prolifération ; contrôles ICGC 70 et GSE62452 69 ; 2 runs v6 sur flux corrigés ; inhibiteurs ATR/CHEK1 dans les 3 criblages existants ; CRISPR déjà mesuré) | v6.0.0-Cohen, fast | KRAS brut puis résidu | réel + nul (graine 42) | **TERMINÉ. Piste redressée : le « stress de réplication » large était de la prolifération. ATR seul survit au contrôle prolif (TCGA partiel +0,366, p 5,6e-7 ; GSE62452 +0,488, p 2,4e-5) ; BRCA2 survit 1/2 ; CHEK1/RAD51/POLQ morts. Médicaments ATR/CHEK1 : 0/60 FDR < 0,05. CRISPR : rien. Aucun test ne justifie KRAS + ATR/CHEK1.** v6 ne sépare pas réel/nul. | Reste ouvert : ATR seul, hypothèse d'expression, sans appui CRISPR ni médicament. Voir §8.25. |
| 30 | 16 nov. 2026, 14h37 | **MTAP / PRMT5 et l'axe KRAS** (TCGA PAAD 178 : expression MTAP/PRMT5/CDKN2A contre KRAS + délétion GISTIC mesurée ; CRISPR DepMap déjà mesuré) | — | — | hors pipeline (test direct) | **TERMINÉ. NON, délétion MTAP non démontrée enrichie chez les KRAS-forts : 6/12 (50 %) contre 37/165 (22 %), OR 3,46, Fisher p = 0,073 (NS). Fait nouveau : PRMT5 monte en expression avec KRAS (rho +0,196, top-12 +0,83 sd), mais dépendance CRISPR plate (−0,189, FDR 0,87).** | Vopimetostat cible un sous-groupe distinct (MTAP-délétés, 24 %) — elle complète l'axe. Voir §8.26. |
| 31 | 16 nov. 2026, 14h37 | **Pan-cancer : axe KRAS → CA125/CEA dans le poumon et le côlon** (TCGA LUAD 515, COAD 285, matrices Firehose MD5 vérifiés, 12 gènes v4, 4 runs v6 fast réel + nul) | v6.0.0-Cohen, fast | KRAS brut | réel + nul (graine 42) | **TERMINÉ. NON : MUC16 plat partout (LUAD +0,020, COAD +0,019) ; CEACAM5 lien faible sans enrichissement top-12. Fait nouveau : le côlon a son propre programme KRAS (MUC2 +0,302, REG4, CLCA1, KRT20, CEACAM5).** v6 ne sépare pas réel/nul. | CA125 reste un marqueur pancréatique. Voir §8.27. |
| 32 | 16 nov. 2026, 15h00 | **Dépendance PRMT5 contre statut MTAP mesuré (DepMap)** (OmicsCNGene 24Q4, 1,4 Go, MD5 vérifié ; 47 lignées pancréas + 1 178 pan-cancer ; Mann-Whitney + Spearman + contrôles KRAS/ACTB/CDKN2A) | — | — | hors pipeline (test direct) | **TERMINÉ. OUI : pancréas PRMT5 médian −1,385 (MTAP-délétées, n=20) contre −1,010 (intactes, n=27), p=0,0036 ; Spearman +0,497 (p=0,0004). Pan-cancer même direction, effet plus petit (p=1,7e-14). Contrôles propres. Limite : MTAP et CDKN2A presque toujours perdus ensemble (CN +0,808) — effet MTAP contre effet 9p21 non séparé par ce test seul.** | Appui mesuré au rationnel vopimetostat — fenêtre réelle, pas dépendance absolue. Voir §8.28. |
| 33 | 16 nov. 2026, 15h50 | **Séparation MTAP vs délétion 9p21 entière (DepMap)** (OmicsCNGene 24Q4 ; 1 178 modèles ; CN < 0,5 = délétion profonde ; Mann-Whitney + Spearman) | — | — | hors pipeline (test direct) | **TERMINÉ. OUI : l'effet PRMT5 suit MTAP, pas 9p21.** CDKN2A-seul (n=137) PRMT5 −1,013 contre −0,973 intactes, p=0,26 ; MTAP+CDKN2A (n=293) −1,098, p=1,5e-5 ; Spearman PRMT5 ~ CN MTAP +0,244 (p=2,9e-7), 2× le CN CDKN2A (+0,122). Pancréas seul même direction (−1,385 / −1,049 / −0,984), p=0,081 faute de puissance. MTAP seul : n=1 pan-cancer, 0 en pancréas. | Rationnel vopimetostat + daraxonrasib renforcé ; combinaison toujours non prouvée. Voir §8.29. |
| 34 | 16 nov. 2026, 18h05–18h20 | **Pipeline v6.1 — construction, validation, bras CRISPR DepMap** (copie v6 + gardes L7a + séries courtes min_len fast 50→40 ; 10 runs fast v6.1 : HP35, TCGA v4, GSE62452, ICGC, DepMap — réel + nul) | v6.1.0-Cohen-short, fast | step | réel + nul (graine 42) | **TERMINÉ. VALIDÉE.** HP35 et TCGA v4 : cascades identiques à v6. GSE62452/ICGC : plus de faux « up »/0,50 — votes finis (down 0,197 / up 0,181). **DepMap (n=45) tourne pour la première fois : cascade 0/1,40/4,40/11,01/26,42, L7a down 0,196 — mais ne sépare pas le nul (MC 0,3615 contre 0,3499, Delta 1,93 contre 1,69).** Falsification indisponible sous n=75. Gigue L5 mesurée (±0,07, hash Python aléatoire). | Le pipeline a testé le CRISPR : pas de rupture nette. Lots v6.1 en cours (44 étendus + 96 rotations). Voir §8.30. |
| 35 | 17 nov. 2026, 14h45–15h10 | **Lot étendu v6.1 — 43/44 runs + comparaison v6.1/v6 + lecture flux par flux des 3 pistes** (22 séries PDAC × réel/nul, `manifest_v61_extended.txt` ; extracteur corrigé `extract_v61_lot_compare_v2.py` ; lecture `pistes_v61_flux_reading.py`) | v6.1.0-Cohen-short, fast | step / valeur | réel + nul (graine 42) | **TERMINÉ (43/44 — côlon réel perdu, dossier effacé par une relance en collision, à refaire). Cascades identiques à v6 sur 41/41 comparables. L7a corrigé sur les 5 petites cohortes (ex. CPTAC_UMICH down 0,148, v6 up 0,500 NaN). MC, Delta, falsification ne séparent PAS réel/nul dans l'ensemble (falsification > 0,5 : 16/21 réels contre 15/21 nuls). Pistes : PURITY = artefact du terme robustesse (0,808 contre 0) ; CLDN18 = contrôle dupliqué en flux (rho 1,000) + vraie co-expression PGC/REG4/MUC17/DPCR1/CEACAM5 ; IMMUNE_TCGA = nul anormalement bas (Delta 2,30, régime criticité) ; le réel montre la chute cytotoxique en haut de l'axe KRAS (GZMB −1,65).** | Lecture de harnais, pas verdict du pipeline. Rotation CLDN18 sans doublon : à proposer. 96 rotations en cours. Voir §8.31. |
| 36 | 17 nov. 2026, 17h17–17h56 | **Rotation CLDN18 sans doublon** (TCGA v4, 178 tumeurs ; CSV sans le flux CLDN18 en double, 11 flux + contrôle CLDN18, SHA `b1071f84…` / nul `33d5f317…` ; `build_v4r_cldn18_dedup.py`, SHA `30aba3b4…`) | v6.1.0-Cohen-short, fast | CLDN18 | PGC | **TERMINÉ, 2/2, exit 0.** Cascade réelle **identique au centième** à avec-doublon (4,26 / 46,59 / **84,42** / 91,14 / 91,14). MC 0,4257 contre nul 0,3313 ; Delta 3,862 contre 3,854 ; L7a UP des deux côtés (0,852 contre 0,847) ; falsification > 0,5 des deux côtés ; L7b FRAGILE des deux côtés. Le groupe PGC/REG4/MUC17/DPCR1/CEACAM5 bouge encore sans le doublon, avec les mêmes valeurs — et bouge aussi dans le nul, en sens inverse à T_0. | **NON : le réel ne se sépare toujours pas du nul.** Le doublon ne faisait pas le résultat. Piste fermée comme test de séparation. Voir §8.31. |
| 37 | 18 nov. 2026, 06h47–10h45 | **Rotations de contrôle systématiques v6.1 — 96/96 runs** (4 familles × 12 flux × réel/nul : V4ROT TCGA v4, DEPMAPROT CRISPR DepMap n=45, IMMROT immunitaire TCGA, PARPROT réparation TCGA ; `manifest_v61_rotations.txt` ; construction `build_rotations_v61.py`, `PROVENANCE_rotations_v61.md` ; extracteur `extract_v61_rotations_v3.py`, lecture `rotations_flux_reading.py`) | v6.1.0-Cohen-short, fast | un flux à tour de rôle | premier flux après le contrôle | **TERMINÉ, 96/96, exit 0, 0 échec. Lots complets : 140/140.** **Aucun contrôle ne sépare réel/nul proprement** (MC, Delta, L7a, falsification). Plus grands écarts : Delta = sauts de niveau de d_div (IFNG +2,396, nul tombé au niveau 3,38) ; MC porté par la séparation (CTLA4 +0,146), robustesse favorisant 5 nuls. **Défaut systématique : les 48 CSV ont le contrôle aussi en flux (13 colonnes) — le doublon domine la lecture à T_0 (d +2,0 à +4,7) dans le réel.** **3 blocs de co-expression réels confirmés par tests directs top-12 (réel ≫ bruit des nuls) : estomac/mucus, immunitaire, réparation. La chaîne KRAS (bloc qui chute + MUC16 qui monte) ne réapparaît sous aucun autre contrôle — elle est propre à l'axe KRAS.** | Lecture de harnais, pas verdict du pipeline. Phase 2 (discrimination, protocole gelé) attend toujours son go. Voir §8.32. |
| 38 | 18 nov. 2026, 10h45–11h30 | **Audit de la nature des flux (§8.33)** (inventaire des 24 séries de base + 96 rotations ; enrichissements possibles avec les fichiers déjà sur le disque : allèle KRAS, TP53/SMAD4/CDKN2A, CN MTAP/CDKN2A, prolifération, sous-type, stade ; déconvolution immunitaire absente) | — | — | hors pipeline (inventaire + vérifications sur disque, aucun run) | **TERMINÉ. 4 natures seulement : ARN tumeurs, ARN lignées, protéine tumeurs, dépendance CRISPR lignées.** Allèle KRAS présent (54 lignées, §8.20) mais jamais en série v6.1 ; MAF TP53/SMAD4/CDKN2A présent mais jointure PR→ACH non construite ; GISTIC MTAP/CDKN2A présent, tests directs seulement ; prolifération calculée (§8.25), test direct seulement ; sous-type ICGC utilisé (§8.16), stade TCGA présent jamais utilisé ; déconvolution immunitaire absente. | **Impossible : pas de vrai temps (KRAS = pseudo-temps), pas de single-cell, pas de spatial, pas de longitudinal.** Voir §8.33. |
| 39 | 18 nov. 2026, 15h06–15h18 (UTC 20h09–20h18) | **Test A — série TCGA v4 ordonnée par prolifération** (178 tumeurs ; score = médiane des résidus MKI67/TOP2A/PCNA/CCNB1, §8.25 ; CSV réel SHA `c87a4e0a…`, nul `99cbc377…` ; `build_fluxes_tcga_v4_prolif.py`, SHA `4bb05e62…` ; `PROTOCOL_testA_proliferation.md`) | v6.1.0-Cohen-short, fast | PROLIF croissant | PGC | **TERMINÉ, 2/2, exit 0.** Vérification de reproduction v4 passée (écart max 1,776e-15, atol 1e-9). Cascade réelle 0 / 0,73 / **3,73** / 24,57 / 24,57 (pas 0/1/**7**/43/43) ; MC 0,3638 contre nul 0,4587 ; Delta 3,798 contre 4,590 ; L7a UP 0,412 contre DOWN 0,196 ; falsification 0,737 contre 0,733 ; L7b FRAGILE des deux côtés. **Le pipeline ne sépare pas réel et nul.** Tests directs top-12 : PGC −0,57 sd (seul mouvement au-dessus du nul), DPCR1 −0,35 (sous son nul −0,47), CLDN18 −0,14, MUC16 −0,04 ; le reste du bloc monte (KRT20 +0,63, MUC2 +0,47, CEACAM5 +0,39). Recouvrement top-12 prolif/KRAS : 1/12. Incident : 1er lancement tué par un redémarrage du service, relance réussie, surveillance cron supprimée après 2/2. | **NON : la chaîne ne réapparaît pas sous l'ordre prolifération.** MUC16 monte doucement le long de l'axe (rho +0,277) sans saut au bout. Lecture « rupture » propre à l'axe KRAS. Voir §8.34. |
| 40 | 18 nov. 2026, 15h21–15h26 (UTC 20h21–20h26) | **Phase 2 — discrimination réel/nul** (8 indicateurs × 8 paires principales, protocole gelé `PROTOCOL_phase2_discrimination.md` du 16 nov. ; critère ≥ 6/8 ; extracteur `extract_phase2.py`, SHA `5eb3ac24…75aa`) | v6.1.0-Cohen-short, lecture seule (aucun nouveau run) | step / KRAS | réel contre nul (graine 42) | **TERMINÉ, lecture seule, 0 run.** Delta 6/8 (réel > nul, mais échoue sur HP35) ; **max_separation 6/8** (HP35 +1,65, PDAC +0,10 à +0,37) ; MC best_score **1/8** (HP35 seul ; écarts PDAC +0,006 à +0,055, sous la gigue ±0,07) ; cohérence par flux 2/8 ; L7a 4/8 ; falsification 4/5 disponibles (comparaison interne, pas au nul permuté) ; T_0 8/8 et cascade 8/8 — triviaux par construction. Annexe 23 paires : max_sep 16/23, MC 2/23, Delta 13/23. COAD réel refait depuis (lot 140/140) inclus. Piste v6.2 proposée seulement (`PROTOCOLE_v6.2_proposition.md`) : hachage stable L5 d'abord, puis score max_separation, puis élucidation des niveaux Delta — rien construit, go séparé requis. | **Le pipeline ne sépare pas réel/nul par ses scores principaux (MC, L7a, cohérence) ; seuls Delta et surtout max_separation montrent un écart réel > nul cohérent sur 6/8 — une piste, pas une discrimination démontrée.** Voir §8.35. |
| 41 | 18 nov. 2026, 16h05–16h08 (heure de Montréal) | **Étape 4 (a) + (b) — allèles KRAS et statuts mutationnels, tests directs** (protocole gelé `PROTOCOL_enrichissements_833.md` ; vérifications `verify_alleles_mutations.py`, SHA `53b90536…b8781`, sortie `verify_alleles_mutations.txt`, SHA `96fd1026…e979`) | hors pipeline (tests directs, aucun run) | — | — | **TERMINÉ. (a) Série par allèle IMPOSSIBLE : max 23 lignées (G12D, sur 54) et 19 (sur 45), minimum fast 40.** Chronos KRAS : G12D vs G12V p=0,15 (d −0,69, NS) ; G12D vs autres p=0,0017 (d −1,42) ; G12V vs autres p=0,017 (d −1,08) ; sauvages n=3, médiane −0,36 contre −2,34/−1,84. Chronos PRMT5 : aucune différence par allèle (p 0,90–0,95). MRTX1133 recalculé : G12D vs G12V p=0,00039 (d −1,52, moyennes −1,70 contre −0,37 — identiques au §8.20, p 0,0001 là-bas, test non précisé). **(b) Jointure MAF PR→ACH revérifiée : relance du constructeur, SHA de sortie identique (`f3fa2bd2…63f36`) — la jointure dite « non construite » au §8.33 était construite le 18 nov. en préparation, et elle est exacte.** TP53 38/45, SMAD4 11/45, CDKN2A 12/45. TP53 : rien (KRAS p=0,19, PRMT5 p=0,89, ATR p=0,94). SMAD4 : KRAS p=0,089 (d −0,79, tendance NS). CDKN2A : PRMT5 p=0,014 (d +0,78, mutées moins dépendantes) — **mais c'est du MTAP** : CN MTAP médiane +0,96 chez les mutées contre +0,29, 2/12 délétées contre 18/33 ; stratifié MTAP-intacte, p=0,76 (d +0,19) : l'effet disparaît. **Séries v6.1 impossibles aussi : plus grand groupe 38 < 40 ; ordre binaire 0/1 dégénéré (seuil forcé à la frontière), non lancé.** | **Allèle : G12D/G12V plus KRAS-dépendantes que les autres, PRMT5 indifférent ; MRTX1133 confirmé G12D-spécifique. Mutations : TP53/SMAD4 ne déplacent rien ; l'effet apparent CDKN2A sur PRMT5 est un confondant MTAP — renforce §8.29 (l'effet PRMT5 suit MTAP).** Voir §8.36. |
| 42 | 18 nov. 2026, 16h09–16h20 (heure de Montréal ; UTC 21h09–21h20) | **Étape 4 (c) — série TCGA v4 ordonnée par CN MTAP** (177 tumeurs appariées sur 178 — TCGA-FB-A4P6-01 sans GISTIC ; CSV réel SHA `578b8d3b…90df6`, nul `e6786a47…53b9` ; `build_fluxes_tcga_v4_mtap.py`, SHA `38346e16…34ef` ; `PROTOCOL_enrichissements_833.md` ; provenance `PROVENANCE_mtap_series.md`) | v6.1.0-Cohen-short, fast | MTAPCN croissant (GISTIC continu, log2) | PGC | **TERMINÉ, 2/2, exit 0, 36 fichiers chacun** (`runs_v61_mtap.log`, FIN 2026-11-18T21:18:51Z, terminés=2, échecs=0). Vérification de reproduction v4 passée (écart max 1,776e-15, atol 1e-9). CN MTAP médiane −0,181 ; top-12 tous seuillés −2 ; Spearman CN MTAP vs rang KRAS −0,309 (p=2,9e-05). Cascade réelle 0,54 / 60,74 / **72,77** / 92,11 / 92,11 (pas 1/107/**128**/162/162, T_0 à CN −0,026) ; MC 0,3512 contre nul 0,5153 ; Delta 3,805 contre 4,347 ; L7a DOWN 0,423 contre UP 0,331 ; falsification 0,733 contre 0,816 ; L7b FRAGILE des deux côtés. **Le pipeline ne sépare pas réel et nul** (MC, Delta, falsification tous meilleurs au nul) ; seuls max_separation (0,339 contre 0,143) et le sens opposé de L7a vont dans le sens réel — pistes, pas preuves. Tests directs top-12 (les plus délétées) : CEACAM5 +0,585 (seul au-dessus du max du nul 0,55), PGC −0,399, CR2 −0,570, MUC16 −0,143, CLDN18 +0,012, DPCR1 −0,078. Recouvrement top-12 MTAP/KRAS : 1/12. Incident : 1er lancement tué par un redémarrage du service (~21h11 UTC), relance par la surveillance systemd-run, cron filet supprimé après 2/2. | **NON : la chaîne ne réapparaît pas sous l'ordre MTAP.** La signature KRAS (PGC −0,89, DPCR1 −0,85, CLDN18 −0,46, MUC16 +0,64) est absente ; MUC16 et les autres ne montent qu'en pente douce le long de l'axe (rho −0,22 à −0,39), sans saut chez les 12 plus délétées. La chaîne reste propre à l'axe KRAS (3e axe testé : prolifération, MTAP). Voir §8.36. |
| 43 | 18–19 nov. 2026 | **v6.2 — hachage stable L5, score S_sep, élucidation de Delta** (go de Zackary 18 nov. 18h07 : « pousser mon pipeline, je veux vraiment qu'il soit en capacité de trouver un remède, pas juste montrer un axe » ; protocole gelé `PROTOCOL_v6.2.md`, SHA `6e9324a2…dfad` ; construction `build_v6.2.py`, SHA `5348636e…fa0` ; `PROVENANCE_v6.2.md`) | v6.2.0-CohenD-short, fast | step / KRAS | réel contre nul (graine 42) | **TERMINÉ. Validation 20/20 exit 0** (10 runs fast × 2 répétitions, processus séparés ; cascades identiques à la v6.1 sur 10/10 ; L7a finis sur les petites cohortes ; **gigue mesurée = 0,0000 sur tous les indicateurs** — seuls divergent les chemins runtime et les champs worker_budget, RAM au lancement ; 0 champ scientifique divergent ; 3 redémarrages machine, reprise par le lanceur). **Discrimination : S_sep 6/8** (HP35, TCGA v4, ICGC, immunitaire, PARP, DepMap ; échecs GSE71729 +0,0405, GSE62452 −0,0072), 16/23 en annexe — exactement max_separation en v6.1 ; MC 7/8 et max_separation 7/8 en v6.2 contre 1/8 et 6/8 en v6.1 **parce que la gigue appliquée est passée de 0,07 à 0,00 mesurée, pas parce que l'instrument a changé** ; avec le forfait 0,07 les verdicts seraient ceux de la v6.1. **Delta NON ÉLUCIDÉ** (222 runs : meilleure combinaison masque+MFA+n 80,2 % paire / 61,7 % valeur, sous les 90 % exigés ; DFA −38,16 retrouvé, sans effet sur d_sat). | **La v6.2 ne sépare pas mieux que la v6.1 ; elle sépare pareil, et de façon déterministe (gigue 0). S_sep atteint la barre ≥ 6/8 mais n'apporte rien au-delà de max_separation ici (stabilité ~0,98–1,00, saturée). Adoption comme version de travail : FAITE le 19 nov. 2026, ~05h47, sur le go de Zackary (« Lance tout cela ») — la v6.2 devient la version de travail, la v6.1 devient la référence, la v6 reste la référence historique.** Voir §8.37. |
| 44 | 19 nov. 2026, 06h27–06h34 (heure de Montréal) | **S_sep appliqué aux bras existants (§8.38)** (go de Zackary « Lance tout cela », 19 nov. 2026 ~05h47 ; formule gelée `PROTOCOL_v6.2.md` : S_sep = max_separation × stability, gigue mesurée 0 ; 2 nouveaux runs v6.2 MTAP via systemd-run, unité `v62-mtap-838`, 2/2 exit 0) | v6.2.0-CohenD-short, fast | step / KRAS | réel contre nul (graine 42) | **TERMINÉ. S_sep v6.2 = S_sep v6.1 exactement sur 29/29 paires distinctes** (max |Δ| = 0,0000 ; ATR +0,2262 ; MTAP +0,1968 ; immunitaire TCGA +0,3659, GSE62452 +0,1534, GSE71729 +0,1343, ICGC −0,2200 inversé ; PARP TCGA +0,1680, GSE71729 +0,1066 ; principales 6/8 sous la règle 0,07 et 7/8 sous la règle gigue 0 ; annexe 16/23 et 20/23). **Le passage 6/8 → 7/8 vient uniquement du passage de la gigue 0,07 à 0,00 — les écarts sont identiques à la v6.1, ce n'est pas une amélioration de l'instrument.** Stabilité quasi saturée (0,97–1,00), S_sep ≈ max_separation ; MTAP : S_sep +0,20 mais MC −0,16 et Delta −0,54 restent inversés, contradiction non résolue. | **S_sep ne classe aucun bras autrement que max_separation en v6.1. Il ne devient pas un discriminateur recommandé au-delà de max_separation.** Voir §8.38. |
| 45 | 19 nov. 2026 | **Élucidation de Delta (§8.39)** (go de Zackary « Lance tout cela », 19 nov. 2026 ~05h47 ; 222 runs, lecture seule, aucun run supplémentaire, aucun code modifié ; hypothèses H8–H15 testées en échantillon + hold-out v6.1 → v6.2) | v6.2.0-CohenD-short, fast | step / KRAS | réel contre nul (graine 42) | **TERMINÉ. Delta NON ÉLUCIDÉ** (critère ≥ 90 % paires ET valeurs non atteint : meilleur score honnête hold-out 87,9 % paires / 81,8 % valeurs, H9e famille+masque+MFA+n ; en échantillon 89,6 % / 84,7 %, H11). Nouveauté structurelle : GraphDimension et PersistentHomology toujours les deux plus basses (222/222), LocalPCA toujours 3e ou 4e (222/222, 3e dans 212 cas) ; le choix se joue entre trois magnitudes continues séparées de ~0,5, qui varient librement dans chaque groupe structurel. Réel/nul : 44,6 % (= base sans prédicteur — la permutation ne change pas la paire, ce qui explique pourquoi Delta ne sépare pas réel et nul). Même en connaissant le rang (donc les 6 valeurs), le critère valeur échoue (70,3 % / 80,3 %). Déduplication : H11 à 90,8 % paires mais 86,9 % valeurs avec 85 groupes / 153 runs — rejeté comme mémorisation. DFA −38,16 confirmé sans effet. | **Delta reste une piste fragile et ne devient pas un discriminateur recommandé. La seule voie ouverte serait de modéliser les magnitudes des estimateurs depuis les flux — hors protocole, non lancée.** Voir §8.39. |

---

## 8. Résultats et analyses

*À remplir après chaque run : cascade seuil par seuil, lecture flux par flux, comparaison au nul, rotation des contrôles, ce qui bouge et ce qui ne bouge pas.*

### 8.1 Run v1 — TCGA, 178 tumeurs, ordre KRAS croissant (15 nov. 2026, exit 0)

**Ce que la v1 mesure :** les 12 flux sont des marqueurs de pancréas normal (enzymes digestives) + XIST. La v1 lit donc le gradient de pureté (quantité de pancréas normal dans la biopsie) le long de l'expression KRAS. Ce n'est pas une transition du cancer lui-même — c'est la lecture de référence, le témoin contre lequel v2/v3/v4 seront jugées.

**Cascade (réel) :** T_-2 0 % → step 0 ; T_-1 49,63 % → step 88 ; **T_0 60,90 % → step 108** ; T_+1 = T_+2 97,39 % → step 173. MC optimum 66,30 % (distinct de T_0, comme sur HP35).

**L7a :** DOWN — up 34,7 %, down 49,9 %, flat 15,4 %, confiance 0,195 (faible). Lecture simple : quand l'expression KRAS monte, les marqueurs acineux baissent. **L7b :** FRAGILE, mode léger — non informatif (verdict clos le 13 nov.), ne pas l'utiliser comme mesure de fragilité. **Régime :** divergence, Delta 3,68 (d_div 5,30, d_sat 1,63, d_crit 3,16). Diagnostic de bruit : score moyen 0,508, verdict MEDIUM, « Mixte » ; XIST se comporte comme du bruit blanc en série (Q5 0,13 contre 0,12).

**Nul permuté (graine 42) :** cascade 1,06 / 6,39 / **9,58** / 15,96 / 22,63 ; L7a UP 77,7 % (down 0 %) ; Delta 4,30. Le nul place son seuil tout au début et vote à l'inverse du réel.

**Ce qui distingue le réel du nul :** l'endroit où tombe le seuil (60,9 % contre 9,6 %) et le sens du vote (DOWN contre UP). **Ce qui ne distingue pas :** le régime divergence (Delta 4,30 nul > 3,68 réel) et L7b FRAGILE des deux côtés — même leçon que sur HP35. L'ordre par KRAS porte donc une information réelle : la relation « KRAS monte, pancréas normal baisse » n'est pas un artefact de l'ordre des lignes.

**Ce que ça ne prouve pas :** aucune cible thérapeutique. La v1 ne dit rien du cancer lui-même, seulement de la composition des biopsies. Les cibles ne pourront venir que des versions nettoyées (v2/v3/v4).

### 8.2 Run v2 — pureté, deuxième couche (15 nov. 2026, exit 0)

**Cascade (réel) :** 0 / 29,55 % → 53 / **48,70 % → 87** / 58,35 % → 104 / 67,12 % → 120. L7a DOWN (conf. 0,201). Delta 3,74. Nul : T_0 9,58 %, L7a UP 85,0 %, Delta 4,30.

**Lecture flux par flux :** à T_-1 (step 53), tous les marqueurs acineux/îlots MONTENT (+0,19 à +0,75 sd, PGC +0,75) ; à T_0 (step 87), ils BAISSENT tous (−0,36 à −0,67 sd, sauf GCG/INS qui montent un peu). La v2 décrit donc une arche de pureté le long de KRAS : les biopsies contiennent de plus en plus de pancréas normal jusqu'au step 53, puis de moins en moins après le step 87. Même leçon que v1, un cran plus fin — toujours pas le cancer lui-même.

### 8.3 Run v3 — après correction de pureté, le sexe apparaît (15 nov. 2026, exit 0)

**Cascade (réel) :** 0 / 25,55 % → 45 / **89,57 % → 159** / 97,91 % → 174 (×2). L7a DOWN (conf. 0,174, faible). Delta 3,84. Nul : T_0 61,32 %, L7a DOWN 85,7 % (conf. 0,420).

**Lecture flux par flux :** à T_0 (step 159), XIST baisse de −0,52 sd et les 6 gènes Y montent de +0,42 à +0,51 sd : après le step 159, les patients sont presque tous des hommes. Le seuil v3 est donc d'abord une frontière homme/femme dans l'ordre KRAS. Mais dessous, les mêmes gènes tumoraux baissent déjà : PGC −0,55 sd, DPCR1 −0,40 sd, CLDN18 −0,34 sd.

**Avertissement honnête :** le nul v3 vote DOWN lui aussi, et fort (85,7 %, conf. 0,420). En v3, la direction ne distingue pas le réel du nul — seule la position du seuil diffère (89,57 % contre 61,32 %). La v3 seule ne suffit pas ; c'est la v4 qui tranche, en enlevant le sexe.

### 8.4 Run v4 — la couche tumorale : une chaîne en deux temps (15 nov. 2026, exit 0)

**Cascade (réel) :** 0 / 74,06 % → 132 / **93,22 % → 166** / 98,44 % → 175 / 98,96 % → 176. L7a DOWN 86,3 % (up 0 %, conf. 0,408 — la plus forte des 4 versions réelles). Delta 4,18. Falsification delta_vs_null 0,849 (seuil 0,5). Nul : T_0 15,96 %, L7a UP 45,1 % (conf. 0,167, faible), Delta 3,77. **La v4 sépare le réel du nul sur la position du seuil ET sur le sens du vote.**

**Lecture flux par flux — la chaîne :**
- **Premier temps, T_-1 (step 132, 74,06 %) :** KRT20 −0,66 sd et CLCA1 −0,59 sd baissent, CR2 −0,42 sd baisse, CEACAM5 (CEA) +0,43 sd monte. Les marqueurs d'épithélium commencent à tomber, le marqueur tumoral CEA monte.
- **Deuxième temps, T_0 (step 166, 93,22 %) :** PGC −0,89 sd (de +1,72 à −2,14), DPCR1 −0,85 sd (de +2,83 à −0,47), CLDN18 −0,46 sd (de +1,75 à −0,07) s'effondrent ; MUC16 (CA125) +0,64 sd monte (de −0,22 à +2,11) ; CLCA1 +0,32 sd et CEACAM5 +0,21 sd montent un peu.

**Lecture simple :** les ~12 patients avec l'expression KRAS la plus forte (steps 166–178, après correction de pureté) forment un groupe à part : leurs tumeurs perdent leurs marqueurs de différenciation (PGC, DPCR1, CLDN18) et gagnent MUC16. C'est une chaîne causale en deux temps — exactement le type de résultat cherché — et c'est le seul run du jour où le réel se distingue du nul sur les deux plans (position + sens) avec la confiance la plus forte.

**Ce que ça ne prouve pas :** ce n'est pas un remède, pas une cible validée, pas un pronostic (aucune donnée de survie n'a servi ici). C'est un sous-groupe moléculaire mesuré, reproductible (protocole gelé, SHA, nul), qui demande une confirmation indépendante (autre cohorte : CPTAC protéine, GEO, ou DepMap/GDSC pour la réponse aux médicaments). Les pistes qui en sortent sont au §9 — des pistes, pas des candidats.

### 8.6 Couche CRISPR — test « plus que mesurer » nº 1 (15 nov. 2026, 08h34)

**Question :** dans DepMap 24Q4 (47 lignées pancréatiques, effets Chronos), les lignées les plus dépendantes de KRAS dépendent-elles différemment des gènes de la v4 ? Autrement dit : CLDN18, MUC16, CEACAM5 sont-ils des vulnérabilités génétiques du sous-groupe, ou seulement des marqueurs ?

**Résultat : NON — ce sont des marqueurs, pas des vulnérabilités.** Corrélations de Spearman avec la dépendance KRAS (47 lignées) : CLDN18 +0,045 ; MUC16 −0,117 ; CEACAM5 −0,131 ; PGC −0,122 ; KRT20 +0,061 ; CLCA1 +0,232 ; CR2 +0,217 ; REG4 −0,036 ; MUC17 +0,005 ; GSTM1 +0,129 — toutes faibles (|rho| ≤ 0,23). Par tertile KRAS, la dépendance moyenne ne bouge pas : CLDN18 +0,09 / +0,10 / +0,09 (jamais essentiel nulle part) ; MUC16 −0,03 / −0,02 / −0,05 ; CEACAM5 +0,03 / +0,02 / +0,01. DPCR1 et MUC2 sont absents de la bibliothèque DepMap 24Q4 (DPCR1 : aucune entrée ; MUC2 : seuls MUC20/21/22 présents).

**Lecture :** éteindre ces gènes ne tue pas les lignées pancréatiques, quel que soit KRAS. C'est cohérent avec leur biologie : CLDN18 (protéine de jonction serrée), MUC16 (mucine) et CEACAM5 sont des protéines de surface — des cibles pour anticorps et conjugués anticorps-médicament, pas des gènes essentiels. La piste thérapeutique n'est donc pas une létalité synthétique CRISPR, mais un ciblage de surface — à tester sur des données de sensibilité aux médicaments (PRISM, test nº 2 ci-dessous), pas sur CRISPR.

**Détail technique :** la première colonne de `CRISPRGeneEffect.csv` est sans nom (les ModelID sont l'index) et les gènes sont nommés « SYMBOLE (Entrez) » — deux scripts ont échoué sur ces formats avant le bon (alignement des colonnes vérifié par le KRAS médian −1,76, identique à la construction des flux du matin).

### 8.7 Couche médicaments (PRISM 24Q2) — test « plus que mesurer » nº 2 (15 nov. 2026, 08h36)

**Question :** parmi les lignées pancréatiques, un médicament tue-t-il de préférence les lignées les plus dépendantes de KRAS ? Criblage de 6 790 composés (dose unique 2,5 µM), 38 lignées pancréatiques communes PRISM × DepMap, corrélation de Spearman entre viabilité et effet Chronos KRAS. Provenance : DepMap Repurposing Public 24Q2, figshare article 25917643 (matrice 72 456 953 octets, métadonnées, liste des composés) ; script `prism_screen.py`, sorties `data/prism_kras_screen*.csv`.

**Résultat : NÉGATIF — aucun médicament ne se détache une fois la correction faite.** Le meilleur, le pamiparib (inhibiteur PARP), a rho −0,614 et p < 0,0001, mais FDR (Benjamini-Hochberg) = 0,286 ; **zéro composé passe FDR < 0,05** sur 6 790 testés (12 ont p < 0,001, contre ~7 attendus par hasard). Surtout, il n'y a **aucun effet de classe PARP** : médiane rho des 25 inhibiteurs PARP = +0,032 (olaparib −0,221 ; talazoparib −0,143 ; niraparib +0,048 ; rucaparib −0,252) — le pamiparib est un cas isolé dans sa propre classe, probablement un effet hors-cible ou du bruit. Les inhibiteurs MEK non plus ne montrent rien de cohérent (tramétinib +0,226 ; sélumétinib +0,063 ; signes mélangés). Les autres têtes de liste (céfopérazone, lévodopa, imétit, palmitate d'isopropyle — un hydratant cosmétique) n'ont aucun mécanisme plausible : du bruit d'écran.

**Lecture honnête :** le test médicaments ne donne pas de piste médicamenteuse pour le sous-groupe. Le pamiparib reste noté comme curiosité (nº 1 du criblage, p < 0,0001 non corrigé), mais il ne tient pas après correction et n'a pas d'appui de classe — ce n'est pas un candidat. Le sous-groupe v4 reste un sous-groupe moléculaire mesuré (ARN), dont la confirmation décisive est maintenant la protéine (CPTAC, §8.8) — pas un médicament.

**Note de traçabilité (16 nov. 2026) :** dans `prism_screen.py` (ligne 76), les tertiles étaient étiquetés `pd.qcut(kk, 3, labels=["faible", "moyen", "fort"])` — or qcut étiquette par ordre croissant, donc « fort » y désignait le Chronos le plus élevé, c'est-à-dire les lignées les **moins** dépendantes de KRAS (étiquettes inversées). Les rhos et le verdict (négatif, FDR) ne sont pas touchés, et aucune direction de tertile n'a été citée au §8.7 — le verdict ne change pas. Le script GDSC (§8.17) étiquette correctement (« fort » = Chronos le plus négatif = le plus dépendant).

### 8.8 Confirmation protéique CPTAC — NON, la chaîne ne se confirme pas (15 nov. 2026, 08h33–09h05)

**Ce qui a été testé :** étude CPTAC PDAC PDC000393 (Cao et al. 2021, *Cell*), deux centres séparés — UMich (63 tumeurs, 7 flux) et BCM (52 tumeurs, 6 flux, MUC16 exclue car 48/52 < 50). Fichiers téléchargés depuis le miroir Zenodo du paquet `cptac` (record 8394329), MD5 vérifiés exacts ; l'accès PDC n'était ni contrôlé ni bloqué. DPCR1 exclu (symbole ambigu en protéine), CR2/MUC17/GSTM1/MUC2 exclus (trop peu de valeurs mesurées, jamais d'imputation). Ordre = KRAS protéique croissant, nul permuté graine 42, v6 fast, 4 runs exit 0. Détail complet : `PROVENANCE_cptac.md`.

**Résultat : NON.** UMich : T_0 à 4,69 % (step 3 — trois points avant le seuil, porté par la seule tumeur au KRAS le plus faible) ; Delta réel 1,48 contre nul 1,49 (quasi identiques, contre 4,18 contre 3,77 en ARN) ; L7a **dégénéré — probabilités NaN, confiance 0,5 — sur les 4 runs**, réel comme nul (cause non diagnostiquée, à investiguer avant tout nouveau run protéique). BCM : T_0 à 63,26 % mais aucun mouvement de flux derrière lui (+0,01 à +0,33 sd) ; Delta 1,55 contre 1,52. Test direct : UMich top 4 → CLDN18 −0,28 sd, MUC16 +0,99 sd (un air de la chaîne) mais top 12 → CLDN18 +0,41 sd, MUC16 −0,25 sd (**inversion**) ; BCM top 4 → CLDN18 −0,52 sd, top 12 → +0,57 sd (même instabilité). Spearman flux contre rang KRAS : tous |rho| ≤ 0,14 (UMich) et ≤ 0,20 (BCM), p > 0,16 — aucune relation monotone.

**Ce que ça n'invalide pas :** le résultat ARN v4 reste debout — autre cohorte (178 patients TCGA contre 63/52 CPTAC, patients différents, pas d'appariement), autre couche de mesure (ARN ≠ protéine, surtout pour des mucines bruyantes en protéomique), cohortes protéiques plus petites. La voie de secours RPPA n'a pas été lancée : le panel RPPA ne contient ni CLDN18, ni MUC16, ni CEACAM5, ni KRAS — elle ne servirait à rien ici.

**Suite proposée (à décider) :** (a) confirmation sur une **autre cohorte ARN** (ICGC ou GEO PDAC) — la confirmation la plus directe du motif ARN ; (b) test de la réponse aux médicaments anti-CLDN18.2 selon CLDN18/KRAS dans les lignées ; (c) diagnostic du L7a NaN sur matrices protéiques avant tout nouveau run protéique.

### 8.9 Rotations de contrôle — la chaîne est réelle et propre à l'axe KRAS (15 nov. 2026, 08h52–09h24)

**Question (règle permanente) :** la chaîne v4 tient-elle quand on change l'axe de contrôle ? Quatre rotations, mêmes 12 flux, mêmes 178 patients, 8 runs exit 0. Protocole et provenance : `build_rotations.py`, `PROVENANCE_rotations.md` (ordre v4 reproduit exactement, SHA v4 inchangé `e7a2adab…`).

1. **KRAS-valeur — IDENTIQUE, chiffre par chiffre.** Contrôle = valeur du résidu KRAS au lieu du rang step : cascade 0 / 74,06 / **93,22** / 98,44 / 98,96, L7a DOWN 85,8 % (conf. 0,404), Delta 4,18, MC 10,87 % — les mêmes nombres que la v4. La métrique du contrôle ne change rien : le résultat ne dépend pas de l'espacement uniforme des rangs.
2. **Miroir (KRAS décroissant) — la chaîne est dans les données, miroir exact flux par flux.** Aux positions miroirs, les mouvements sont les mêmes avec les signes inversés : au step 12 (miroir du T_0) PGC **+0,89** sd, DPCR1 **+0,85**, CLDN18 **+0,46**, MUC16 **−0,64** (v4 : −0,89 / −0,85 / −0,46 / +0,64) ; au step 46 (miroir du T_-1) KRT20 **+0,66**, CLCA1 **+0,59**, CEACAM5 **−0,43** (v4 : −0,66 / −0,59 / +0,43). **Mais** la cascade ne place pas son T_0 au miroir (60,38 % au lieu de ~6,8 % ; à son T_0 les mouvements sont petits, max +0,34 sd) et L7a ne se retourne pas (DOWN 86,2 %, conf. 0,431, quasi identique à la v4). Deux comportements de l'instrument à noter comme questions ouvertes (le balayage et le vote semblent directionnels) — pas des verdicts sur les données, qui, elles, se retournent exactement.
3. **CLDN18 comme contrôle — pas de discrimination.** Réel : T_0 84,42 %, L7a UP 85,5 % (conf. 0,417) ; nul : T_0 60,38 %, L7a UP 86,3 % (conf. 0,420). Le nul vote pareil et aussi fort — ordonner par CLDN18 ne sépare pas réel et nul. La chaîne est spécifique à l'axe KRAS : elle ne se lit pas depuis un autre gène.
4. **Pureté comme contrôle (témoin négatif) — aucune chaîne, comme attendu.** Réel : T_0 42,52 %, L7a UP 53,4 % (conf. 0,198, faible) ; à son T_0 tous les flux baissent modestement et ensemble (−0,13 à −0,55 sd). Nul : DOWN 58,2 % (conf. 0,225). Rien de fort d'aucun côté — la v4, qui a enlevé la pureté, ne réapparaît pas quand on ordonne par la pureté.

**Verdict des rotations :** la chaîne est invariante à la métrique du contrôle (KRAS valeur = KRAS rang, identique), elle se retourne exactement dans les données (miroir), elle est propre à l'axe KRAS (absente sous CLDN18 et sous pureté). Les deux bizarreries de l'instrument — cascade qui ne place pas son T_0 au miroir, L7a qui ne se retourne pas — sont notées comme questions ouvertes, à investiguer avant d'en tirer un verdict.

### 8.10 Confirmation GEO GSE71729 — NON, et la moitié « marqueurs qui montent » tient (15 nov. 2026, 09h16–09h40)

**Ce qui a été testé :** cohorte Moffitt GSE71729 (Moffitt et al. 2015), 145 tumeurs primaires, puce Agilent GPL20769, matrice 15 622 315 octets, SHA `b2287893…536a54`. Les ID de la matrice sont déjà des symboles de gènes (19 749 lignes, 0 duplicata). Trois variantes, 6 runs exit 0 : (a) les 12 mêmes gènes que la v4 ; (b) re-sélection fraîche protocole v4 ; (c) les 12 mêmes gènes corrigés de la pureté. Détail complet : `PROVENANCE_geo71729.md`. Limite de traçabilité notée : le script de la variante (c) a été exécuté en ligne et n'a pas été sauvegardé en fichier — sa construction est décrite dans la provenance et reproductible depuis la matrice, mais le fichier manque.

**Résultat : NON pour la chaîne, OUI partiel pour deux marqueurs.** (a) T_0 76,77 %, L7a UP 82,1 % contre nul UP 85 %, Delta 2,16 contre 2,20 — le pipeline ne sépare pas réel et nul. À T_0 les gènes MONTENT (+0,18 à +0,65 sd) au lieu de s'effondrer. Test direct (top 12 KRAS contre le reste, vérifié) : CLDN18 **+0,68 sd**, MUC16 **+0,67**, DPCR1 +0,60, KRT20 +0,60, CEACAM5 +0,38, PGC +0,25 — **l'inverse de TCGA pour CLDN18, PGC, DPCR1, KRT20** (TCGA : −0,46 / −0,89 / −0,85 / −0,66). (b) Réel et nul placent leur seuil au même endroit (25,09 % contre 24,44 %) — pas de chaîne. (c) La correction de pureté ne retourne pas le sens (CLDN18 −0,19, MUC16 +0,05 à T_0) — l'objection la plus directe est fermée.

**Ce qui tient dans les deux cohortes : MUC16 et CEACAM5.** MUC16 est plus élevé dans le groupe KRAS-le-plus-fort dans les deux cohortes (TCGA +0,64 sd ; GEO (c) +0,65 top 12 / +0,73 top 7) et CEACAM5 aussi (TCGA +0,43 sd à T_-1 ; GEO +0,38 / +0,33 top 12). La moitié « marqueurs qui montent » (CA125, CEA) tient ; la moitié « marqueurs de différenciation qui s'effondrent » (PGC, DPCR1, CLDN18, KRT20) s'inverse. Note d'honnêteté : en variante (a), MUC16 vaut +0,67 au top 12 mais +0,10 au top 7 — c'est la variante (c), corrigée pureté, qui rend l'élévation MUC16 robuste au choix du seuil.

**Ce que ça n'invalide pas :** le résultat TCGA v4 reste debout dans sa cohorte (rotations §8.9). Hypothèses non testées sur la différence : technologie (puce Agilent contre ARN-seq), cohortes différentes (Moffitt 2015, chirurgie, contre TCGA mixte), ou chaîne spécifique à la cohorte TCGA.

### 8.11 Test décisif : l'effondrement est-il dans les données brutes ? (15 nov. 2026, 10h05)

**Question :** la moitié « effondrement » de la chaîne v4 (PGC, DPCR1, CLDN18 qui tombent) existe-t-elle dans les valeurs brutes, ou est-elle créée par la correction de pureté de la v4 ? Test direct sur la matrice Firehose (log2 RSEM+1, sans correction), mêmes 12 patients que la v4 (11/12 communs entre l'ordre par résidu KRAS et l'ordre par KRAS brut).

**Résultat : la moitié « marqueurs qui montent » est dans le brut, la moitié « effondrement » dépend de la correction.** Valeurs brutes, top 12 contre reste : MUC16 **+0,58 sd** (v4 : +0,64), CEACAM5 **+0,75** (v4 : +0,43 à T_-1) — présentes et aussi fortes sans correction. PGC **−0,51** (v4 : −0,89) — la baisse existe dans le brut, plus faible. DPCR1 **−0,17** (v4 : −0,85) et CLDN18 **−0,04** (v4 : −0,46) — quasiment absentes dans le brut, l'essentiel de leur « effondrement » vient de la correction. KRT20 +0,24 et CLCA1 +0,37 dans le brut (en v4 ils baissaient à T_-1 : −0,66 / −0,59).

**Lecture honnête :** la correction de pureté n'explique que 2,0 % de la variance en médiane (v3) — elle ne devrait pas créer un tel écart, et la question reste ouverte (modèle linéaire imparfait ? scores de pureté incomplets ?). Ce qui est mesuré, sans interprétation : la hausse de CA125/CEA ne dépend d'aucune correction et tient dans deux cohortes ; l'effondrement de DPCR1/CLDN18 dépend de la correction et ne tient dans aucune autre cohorte. **Le résultat robuste du jour se resserre donc sur : le groupe KRAS-le-plus-fort a CA125 et CEA élevés.** L'effondrement reste une observation TCGA, à ne pas présenter comme un fait général.

### 8.12 Survie — le paysage dépend du seuil, le test sans seuil tient (15 nov. 2026, 10h11–10h20)

**CORRECTION 16 nov. 2026 (vérification indépendante, script sauvegardé `survival_tcga_verify.py`, SHA `937bdb6e…dade2`, résultats `tcga_survival_verify_results.txt`, SHA `bcca9898…108655`) :** le tableau « Cox univarié » du 15 nov. était en fait l'ajustement à 6 gènes, mal étiqueté — la même erreur que le bras GSE71729 a trouvée dans son propre premier script. Les anciens chiffres (KRAS 1,29 ; MUC16 1,28 ; CEACAM5 1,02 ; PGC 1,00 ; DPCR1 1,26 ; CLDN18 0,96) sont l'ajustement à 6 gènes (recalculé ici : 1,30 / 1,26 / 1,03 / 1,00 / 1,24 / 0,94 — accord à 0,02 près). Les VRAIS univariés, vérifiés par 3 implémentations (Newton-Raphson, agent GSE71729, statsmodels PHReg — accord à 0,01 près), sont plus forts (voir ci-dessous). Le multivarié, lui, était correct (recalculé : 1,33 / 1,32 / 1,07 contre 1,31 / 1,34 / 1,08 publiés). Le paysage log-rank a aussi été refait (2 implémentations, accord exact) : les top12 et top20 tiennent, les quartiles seuls et le double-quartile ne tiennent plus. La conclusion se renforce, elle ne s'affaiblit pas.

**Données :** clinique TCGA PAAD PanCan Atlas (cBioPortal datahub, `data_clinical_patient.txt`, 184 patients, OS_MONTHS/OS_STATUS/DFS, âge, sexe, stade) ; 177 patients avec ARN + survie (92 décès), OS médiane de la cohorte 20,0 mois (Kaplan-Meier). Source et SHA dans la provenance (à ajouter à `PROVENANCE_tcga.md`). Un patient (TCGA-IB-7654, rang KRAS 172/178, dans le top12) n'a pas de survie : les groupes top7/top20 du 15 nov. le comptaient dans la définition sans survie (n=6 et n=19 avec survie) ; la vérification classe parmi les 177 avec survie (n=7 et n=20) — un patient suffit à retourner une médiane à n=6–7, c'est la fragilité du paysage, pas une erreur de calcul.

**Paysage de survie (9 définitions de groupe, toutes rapportées — aucune choisie) — valeurs VÉRIFIÉES 16 nov. :**
| Groupe | n | décès | OS médiane (reste) | log-rank p |
|---|---|---|---|---|
| top12 KRAS résidu (v4) | 11 | 9 | 9,1 mois (20,6) | 0,017 |
| top12 KRAS brut | 11 | 10 | 9,1 mois (20,8) | 0,0015 |
| top12 score KRAS+CA125+CEA | 11 | 8 | 8,2 mois (20,6) | 0,0498 |
| top7 KRAS résidu | 7 | 6 | 9,1 mois (20,6) | 0,072 |
| top20 KRAS résidu | 20 | 14 | 17,9 mois (20,8) | 0,0415 |
| quartile sup. MUC16 (CA125) seul | 45 | 30 | 15,8 mois (21,4) | 0,070 |
| quartile sup. CEACAM5 (CEA) seul | 45 | 27 | 15,9 mois (20,8) | 0,25 |
| quartile sup. KRAS brut seul | 45 | 30 | 15,6 mois (22,5) | 0,0136 |
| CA125 ET CEA élevés (2 quartiles sup.) | 16 | 10 | 22,5 mois (20,2) | 0,90 |

**Lecture — exactement l'avertissement de l'utilisateur (10h11) : le seuil change la réponse.** Le groupe top12 meurt nettement plus tôt (9 contre 20 mois), mais l'effet s'affaiblit au top7 (p=0,072) ; les quartiles seuls (CA125 p=0,070, CEA p=0,25) et le double-quartile (p=0,90, médiane 22,5 mois — le groupe vit plus longtemps, non significatif) ne tiennent pas. Avec 9 définitions testées et n=11, ce paysage est une piste, pas une preuve — et il est plus fragile que le 15 nov. ne le disait.

**Test sans seuil (Cox continu, aucune coupure, aucun groupe) — n=177, 92 décès, risque par +1 écart-type — valeurs VÉRIFIÉES 16 nov. :** KRAS HR 1,42 (p=0,0003) ; MUC16 HR 1,44 (p=0,001) ; CEACAM5 HR 1,31 (p=0,011) ; PGC HR 1,16 (p=0,13) ; DPCR1 HR 1,43 (p=0,001) ; CLDN18 HR 1,22 (p=0,064). **En multivarié (KRAS + MUC16 + CEACAM5 ensemble) : KRAS HR 1,33 (p=0,014), MUC16 HR 1,32 (p=0,019), CEACAM5 HR 1,07 (p=0,57).** Sans aucun seuil : KRAS, CA125, CEA et DPCR1 prédisent chacun une survie plus courte pris seuls ; en multivarié, KRAS et CA125 restent indépendants, CEA disparaît (son signal passe par KRAS/CA125). C'est la version du résultat qui ne dépend d'aucun seuil, et elle est plus forte que celle du 15 nov. — le tableau « univarié » publié alors était l'ajustement à 6 gènes (voir la correction en tête de section).

### 8.13 Troisième cohorte GSE62452 — OUI, 3/3, et le seuil seul retourne le signe (15 nov. 2026, 10h11–10h36)

**Ce qui a été testé :** GEO GSE62452, 69 tumeurs PDAC, puce Affymetrix HuGene-1.0-st (plateforme réelle GPL6244 — la mission annonçait GPL570 par erreur, corrigé en cours ; mapping extrait de la table GPL6244, 25 293 sondes avec symbole). Matrice 14 447 291 octets, SHA `8f41d5b3…078cba` (premier téléchargement tronqué à 12 943 600 octets, re-téléchargé et vérifié). Deux variantes, 4 runs exit 0. Détail complet : `PROVENANCE_geo62452.md`. Note : KRAS R² pureté = 19,6 % ici (contre 0,3 % TCGA, 1,4 % GSE71729) — la pureté pèse beaucoup plus sur KRAS dans cette cohorte ; données fusionnées de deux lots, effet de lot retiré par les auteurs (Partek), non vérifiable depuis la matrice. Survie absente de la matrice.

**Résultat : OUI, 3 cohortes sur 3.** Test direct (top 12 contre le reste, vérifié) : MUC16 **+0,48 sd**, CEACAM5 **+0,63** (Spearman rho +0,441, p=0,0001 — le signal le plus fort du paysage), DPCR1 +0,93 (rho +0,334, p=0,005), CLDN18 +0,55, PGC +0,11, KRT20 +0,15. Nul : tout entre −0,38 et +0,45 sd. **Comparaison 3 cohortes (top 12) : MUC16 +0,64 / +0,67 / +0,48 ; CEACAM5 +0,43 / +0,38 / +0,63 — 3/3 en hausse. CLDN18 −0,46 / +0,68 / +0,55 ; DPCR1 −0,85 / +0,60 / +0,93 ; PGC −0,89 / +0,25 / +0,11 — l'effondrement ne tient que dans TCGA.** La variante (b), re-sélection fraîche, retrouve indépendamment DPCR1 (rho +0,394, p=0,0008) et CEACAM5 (rho +0,372, p=0,0016) qui montent avec KRAS — preuve convergente sans utiliser la liste v4.

**Le pipeline ne sépare pas réel et nul ici** (Delta 1,41 contre 1,26 ; en (b) T_0 réel 79,67 % contre nul 84,02 %) — le verdict repose sur les tests directs, pas sur sa cascade. **L7a dégénéré (NaN) sur les 4 runs** — comme CPTAC (n=63/52). Motif qui se précise pour la question ouverte : L7a dégénère aux petits n (52, 63, 69) et fonctionne à n=145, 178, 1000 — piste, pas une preuve.

**Illustration vivante de l'avertissement de l'utilisateur (10h11) :** le T_0 de la variante (a) tombe au step 66 — il ne reste que 3 points après. La lecture par flux à ce seuil donne MUC16 **−0,83 sd** (3 points), alors que le test top 12 donne **+0,48** et le top 7 **+0,29**. Un seul seuil, 3 points, et le signe de MUC16 se retourne. Le verdict ne doit pas venir de ce seuil : il vient des tests directs (12 et 7 points) et des Spearman, cohérents entre eux et entre les 3 cohortes.

**État du résultat robuste après 4 cohortes :** le groupe KRAS-le-plus-fort a CA125 et CEA élevés — 3/4 (TCGA, GSE71729, GSE62452 oui ; ICGC non, §8.16). L'effondrement des marqueurs de différenciation est une observation TCGA seule. **Survie : CA125 prédit une survie plus courte dans 2 cohortes sur 3** (TCGA : HR 1,44 univarié / 1,32 multivarié ; ICGC : 1,57 / 1,56 ; GSE71729 : non, 1,06) ; KRAS pointe dans le même sens partout (1,42 / 1,24 / 1,25) mais n'est significatif qu'en TCGA ; CEA ne tient nulle part en multivarié.

### 8.14 Diagnostic L7a NaN — cause trouvée, de bout en bout (15 nov. 2026, 11h08–11h20)

**Question ouverte depuis CPTAC :** pourquoi L7a donne-t-il des probabilités NaN (vote « up », confiance 0,5) sur les petites cohortes (n=52, 63, 69) et fonctionne-t-il à n=145, 178, 1000 ? Diagnostic par lecture seule du code v6 (jamais modifié), vérifié à chaque étape sur les sorties réelles.

**Chaîne complète, vérifiée :**
1. **Le diagnostic de bruit coupe la série en 5 bins et exige ≥15 points par bin** (étape Hurst, lignes ~4137–4147 ; `insufficient_data_bins > 2` force aussi l'échec). Il faut donc 5×15 = **75 points minimum**. À n=52/63/69, chaque bin n'a que ~10–14 points → `hurst_computed = False` pour chaque flux (la pente spectrale, elle, se calcule bien). À n=145/178, les bins ont ~29 points → ça passe. La frontière n'est pas « petit n » en général : c'est **n < 75**.
2. `computed_status = False` → `variance_proxy_score = NaN` pour chaque flux (lignes ~4321–4328) ; `avg_variance_proxy_score` = None.
3. `csd_ranking` = que des NaN (lignes ~7550–7557) ; `avg_csd_proxy` est ramené à 0,0 par `_sf` dans `level_risk`, mais **`top_csd = float(csd[0][1])` n'a AUCUNE protection contre NaN** (lignes 8943–8948 ; `float(nan)` ne lève pas d'exception, le try/except ne l'attrape pas).
4. `risk_score = clip(0,40×0 + 0,25×NaN + 0,35×0) = NaN` ; `level` = « low » (une comparaison avec NaN est toujours fausse) ; `confidence` = NaN (lignes 8950–8960).
5. **L7a** (`level_coherence_universal`) : L4 a le statut « ok » et le niveau « low » → branche else : `votes["flat"] += w×0,35` avec `w = 0,20 × NaN = NaN` → `votes["flat"] = NaN` → `raw_total = NaN` → le test `raw_total <= 1e-9` est **faux** pour NaN (il ne protège pas) → division par NaN → probabilités toutes NaN → `max(probs)` retourne la première clé, « up », par accident → `global_conf` NaN → repli à 0,50.

**Ce que ça veut dire :** le « up » et la confiance 0,5 des petits runs ne sont pas un vote — ce sont l'artefact d'un `max()` sur des NaN et d'un repli. L7a ne dit rien sur ces cohortes ; il ne faut pas le lire. Les autres sorties des mêmes runs (cascade, tests directs) ne sont pas touchées par cette chaîne.

**Correctif proposé (sur COPIE, jamais sur l'original, avec conception gelée + go explicite) :** (a) protéger `top_csd` par `_sf(..., 0.0)` dans `level_risk`, comme `avg_proxy` l'est déjà ; (b) protéger les votes L7a contre les poids non finis (ignorer une contribution NaN, ou retourner « insufficient_data » si le total n'est pas fini). Avec (a), L7a se calculerait alors sur L1/L3/L5 seuls — à valider sur copie contre les runs connus avant tout usage. L'option (c) — rendre le nombre de bins Hurst adaptatif sous 75 points — changerait le comportement de l'instrument et demande une conception gelée séparée.

### 8.15 Survie GSE71729 — partiel : KRAS tient en direction, CA125 ne tient pas (16 nov. 2026, 07h08–07h14)

**Données :** pas de fichier clinique séparé pour GSE71729 (suppléments GEO : seulement le RAW ; suppléments Nature vérifiés un par un — aucune survie par patient ; suppléments Birnbaum : tableaux récapitulatifs seulement). La survie est dans les caractéristiques ch2 de la matrice elle-même : `survival_months` et `death_event_1death_0censor` — **125 tumeurs primaires avec survie, 84 décès, OS médiane 17,0 mois** (20/145 sans survie). Effectifs confirmés par la littérature (Wiley 2022 : 125 patients, 41 vivants / 84 décédés). Jointure vérifiée ligne par ligne contre `pdac_geo71729_fluxes.csv`. Script `survival_geo71729.py`, table `geo71729_survival_table.csv` (SHA `1f7a14a7…`), résultats `geo71729_survival_results.txt`, provenance `PROVENANCE_geo71729_survival.md`. Deux erreurs trouvées et corrigées pendant la vérification : un log-rank faux dans la première exécution (événements en entiers au lieu de booléens — top20 sortait à p=0,008, faux positif) et un « univarié » qui était en fait l'ajustement à 6 gènes. Les chiffres ci-dessous sont les chiffres corrigés, vérifiés par une ré-implémentation indépendante.

**Paysage complet (log-rank, toutes définitions, n=125) :**
| Groupe | n | décès | OS médiane (reste) | log-rank p |
|---|---|---|---|---|
| top12 KRAS | 12 | 7 | 17,0 (17,0) | 0,89 |
| top7 KRAS | 7 | 4 | 17,0 (16,0) | 0,71 |
| top20 KRAS | 17 | 11 | 17,0 (16,0) | 0,76 |
| quartile MUC16 (CA125) seul | 33 | 22 | 17,0 (16,0) | 0,73 |
| quartile CEACAM5 (CEA) seul | 32 | 18 | 19,0 (15,0) | 0,20 |
| quartile KRAS seul | 32 | 23 | **10,0 (19,0)** | **0,020** |
| CA125 ET CEA élevés | 11 | 6 | 19,0 (16,0) | 0,46 |

**Cox continu (aucun seuil, HR par +1 écart-type) :** univarié — KRAS 1,24 (p=0,075) ; MUC16 1,06 (p=0,58) ; CEACAM5 1,00 (p=0,97) ; PGC 0,85 (p=0,15) ; DPCR1 1,01 (p=0,90) ; CLDN18 1,01 (p=0,95). Multivarié (KRAS+MUC16+CEACAM5) — KRAS 1,25 (p=0,066) ; MUC16 1,08 (p=0,51) ; CEACAM5 0,93 (p=0,52). Ajustement 6 gènes (référence) — KRAS 1,32 (p=0,035) ; PGC 0,75 (p=0,035, fragile, pas en univarié).

**Verdict : partiel.** KRAS tient en direction (1,24 contre 1,42 en TCGA, même ordre de grandeur, sous le seuil en univarié ; le quartile KRAS seul est significatif : 10 contre 19 mois, p=0,020). CA125 ne confirme pas (1,06–1,08, p≈0,5, contre 1,44/1,32 en TCGA). Le groupe top12 ne confirme pas (17,0 contre 17,0, p=0,89, contre 9,1 contre 20,6 en TCGA). CEA : rien des deux côtés, cohérent. La survie KRAS est donc un signal en deux cohortes sur la direction, la survie CA125 reste TCGA seule. Ce qui manque : pas de survie sans progression (DFS) dans GEO.

### 8.16 Quatrième cohorte ICGC PACA-AU — expression NON, survie CA125 OUI et fort (16 nov. 2026, 07h08–07h23)

**Données :** le portail ICGC (DCC) est hors service (vérifié 16 nov. : toute requête redirige vers `index.html` — `donor.PACA-AU.tsv.gz` et `exp_seq.PACA-AU.tsv.gz` inaccessibles à la source). Contournement vérifié : expression via UCSC Xena, jeu `PACA-AU/nature16965-s2_normalised_exp.txt` (96 échantillons, log2(cpm), Bailey et al. Nature 2016), objet S3 9 841 881 octets, SHA `c2cb57af…0f49fa`, probe map SHA `b09a746f…5537` ; clinique + survie via Bailey et al. 2016, Supplementary Tables 1–13 (22 104 569 octets, SHA `778224b3…4258a`, feuille 'Supp Table 1 Clinical', 458 patients). Écarté après vérification : cBioPortal `paad_qcmg_uq_2016` (pas de OS_MONTHS/OS_STATUS, identifiants incompatibles) et `paad_icgc` (mutations seulement). **70 tumeurs primaires PDAC** (les 26 autres échantillons sont d'autres histologies), suivi renseigné 70/70, 47 décès OS (42 de la maladie). Flux (a) : les 12 mêmes gènes, ordre KRAS croissant, sans imputation — `pdac_icgc_fluxes.csv` (SHA `710d41e5…b61941`), nul graine 42 (SHA `e020a2c4…65f25e`) ; clinique `icgc_clinical_70.csv` ; scripts `build_fluxes_icgc.py`, `survival_icgc.py` ; provenance `PROVENANCE_icgc.md`. Variante (b) non faite (optionnelle ; la (a) étant plate sur les 12 gènes, une re-sélection aurait été de la pêche).

**Pipeline v6 (original intact) — 2 runs, exit 0 :** réel cascade 1,41 / 9,84 / **T_0 52,31 %** / 94,27 / 94,27 ; nul T_0 32,43 % ; Delta 1,44 contre 1,37 — pas de séparation réel/nul. L7a NaN sur les 2 runs — cohérent avec la cause diagnostiquée au §8.14 (n=70 < 75). Sorties `results_fast_icgc/`, `results_fast_icgc_nul/` (36 fichiers chacun), journal `runs_icgc_v6.log`.

**Paysage complet d'expression (n=70, test direct, en sd) — vérifié indépendamment :** MUC16 (CA125) top12 **+0,13** (rho +0,048, p=0,69) ; CEACAM5 (CEA) top12 **+0,28** (rho +0,062, p=0,61) ; CLDN18 −0,09 ; DPCR1 −0,06 ; PGC −0,18 ; KRT20 −0,53. Le nul produit de −0,53 à +1,28 au top12 : les valeurs réelles sont dans le bruit du nul. **Comparaison 4 cohortes (top12) : MUC16 +0,64 / +0,67 / +0,48 / +0,13 ; CEACAM5 +0,43 / +0,38 / +0,63 / +0,28. L'élévation n'est pas universelle : 3/4.**

**Survie (n=70, 47 décès OS, médiane 16,6 mois) — paysage complet :**
| Groupe | n | décès | OS médiane (reste) | log-rank p |
|---|---|---|---|---|
| top12 KRAS | 12 | 10 | 14,1 (17,7) | 0,58 |
| top7 KRAS | 7 | 6 | 14,1 (19,8) | 0,78 |
| top20 KRAS | 20 | 15 | 14,1 (19,8) | 0,46 |
| quartile sup. MUC16 (CA125) seul | 18 | 16 | **9,5 (23,8)** | **0,002** |
| quartile sup. CEACAM5 (CEA) seul | 18 | 10 | 14,1 (17,7) | 0,90 |
| quartile sup. KRAS seul | 18 | 13 | 14,1 (17,7) | 0,85 |
| CA125 ET CEA élevés (2 quartiles) | 8 | 6 | 9,0 (19,8) | 0,25 |

**Cox continu (aucun seuil, HR par +1 écart-type) — vrais univariés, vérifiés indépendamment (2 implémentations, accord exact) :** KRAS 1,25 (p=0,12) ; **MUC16 1,57 (p=0,008)** ; CEACAM5 0,80 (p=0,16) ; PGC 0,78 ; DPCR1 0,83 ; CLDN18 0,79. Multivarié (KRAS+MUC16+CEACAM5) : KRAS 1,28 (p=0,084) ; **MUC16 1,56 (p=0,008)** ; CEACAM5 0,78. Survie spécifique de la maladie (DSS) : MUC16 1,68 (p=0,004). **Contrôle sous-type Bailey :** MUC16 suit le sous-type Squamous (8,23 contre 3,39 Immunogenic), MAIS le Cox MUC16 ajusté sur le sous-type reste **HR 1,75 (p=0,004)** et les sous-types eux-mêmes ne sont pas significatifs — le signal CA125 n'est pas un proxy du sous-type. KRAS est plat entre sous-types (6,28–6,48).

**Lecture d'ensemble :** expression « KRAS fort = CA125/CEA élevés » : **3/4 cohortes**. Survie CA125 : **2/3 cohortes** (TCGA 1,44/1,32 ; ICGC 1,57/1,56 ; GSE71729 non). Survie KRAS : direction partout, significatif seulement en TCGA. Survie CEA : non. Limites honnêtes : n=70 (petite cohorte) ; technologie différente encore (ARN-seq CPM contre RSEM et puces) — hypothèse, pas verdict ; variante (b) non faite ; fichier donneur ICGC original inaccessible (survie via Bailey Suppl. Table 1, mêmes patients). Note de méthode : la survie ICGC et GSE71729 est calculée sur l'expression brute, celle de TCGA sur les résidus corrigés de la pureté — chaque cohorte tient sur ses propres données, la comparaison entre cohortes en tient compte.

### 8.17 Médicaments ciblés KRAS en dose-réponse (GDSC2) — NON (16 nov. 2026, 07h08–07h28)

**Données :** l'ancien site GDSC (410 Gone) et les liens release-8.5 (404) sont morts, mais les données vivent dans l'API publique Cell Model Passports (`api.cellmodelpassports.sanger.ac.uk/download_files`, groupe 46 « GDSC2 IC50 Data », fichier 22870). Fichier `GDSC2_fitted_dose_response_27Oct23.xlsx` : **22 112 537 octets exacts, SHA `0e99120a…c899`** (3 tentatives, serveur lent, 2 coupures, reprises `curl -C -`, HTTP 206). Annotation : `screened_compounds_rel_8.5.csv`, 46 414 octets, SHA `d3cbb8b5…e782`. Journal des 10 tentatives : `gdsc_access.log`. Provenance `PROVENANCE_gdsc.md`. Script `gdsc_kras_screen.py` (SHA `f1c4c157…`, exit 0).

**Méthode :** jointure GDSC2 → DepMap par SANGER_MODEL_ID ; filtre lignée pancréas : 31 lignées GDSC2, **27 avec Chronos KRAS** (min −4,14, médiane −1,89, max −0,36). Par composé (n ≥ 15) : Spearman LN_IC50 et AUC contre Chronos KRAS + moyennes par tertile + FDR Benjamini-Hochberg sur 269 composés. Sens : rho > 0 = les lignées KRAS-dépendantes sont plus sensibles. Tertiles étiquetés correctement (« fort » = Chronos le plus négatif = le plus dépendant — le script PRISM du 15 nov. avait les étiquettes inversées, voir note au §8.7 ; ici c'est corrigé et vérifié).

**Résultat : NON — le groupe KRAS fort ne répond pas mieux aux inhibiteurs de la voie KRAS.**
| Composé (voie KRAS) | n | rho LN_IC50 | p | FDR | rho AUC |
|---|---|---|---|---|---|
| ERK_2440 (ERK1/2) | 23 | +0,246 | 0,258 | 0,385 | +0,513 |
| Sélumétinib (MEK) | 27 | +0,217 | 0,276 | 0,402 | +0,372 |
| ERK_6604 (ERK1/2) | 23 | +0,191 | 0,383 | 0,493 | +0,365 |
| Tramétinib (MEK) | 27 | +0,164 | 0,415 | 0,521 | +0,285 |
| Réfamétinib (MEK) | 26 | +0,128 | 0,533 | 0,640 | +0,228 |
| PD0325901 (MEK) | 27 | +0,120 | 0,552 | 0,657 | +0,272 |
| SCH772984 (ERK) | 27 | +0,085 | 0,672 | 0,756 | +0,194 |
| KRAS (G12C) Inhibitor-12 | 23 | −0,053 | 0,809 | 0,857 | +0,352 |
| Ulixertinib (ERK) | 27 | −0,294 | 0,137 | 0,282 | +0,005 |
| Dabrafénib (BRAF) | 27 | −0,283 | 0,152 | 0,290 | +0,243 |
| SB590885 (BRAF) | 26 | −0,411 | 0,037 | 0,174 | +0,095 |
| PLX-4720 (BRAF) | 27 | −0,543 | 0,003 | 0,086 | −0,133 |

Effet de classe : voie « ERK MAPK signaling » médiane rho +0,085 (13 composés) ; cible MEK1/MEK2 +0,146 (4 composés) — seule direction positive, amplitude faible, rien de significatif. Médiane du groupe KRAS/MEK/ERK/RAF/SHP2/SOS1 : −0,039 (15 composés). **Fait global : médiane rho sur les 269 composés = −0,295 (5,9 % seulement ont rho > 0) — les lignées KRAS-dépendantes sont globalement plus résistantes à la plupart des médicaments.** Seul composé FDR < 0,05 : la staurosporine (rho −0,715, p=2,8e-5, FDR 0,0075), direction **négative** (les KRAS-dépendantes y sont plus résistantes) — inhibiteur de kinases à large spectre, non spécifique : curiosité, pas un candidat.

**Absents de GDSC2** (vérifié fichier + annotation) : sotorasib, adagrasib, MRTX1133 (G12D), cobimétinib, binimétinib, SHP099, TNO155, BI-3406, vémurafénib, encorafénib. Seul inhibiteur direct de KRAS présent : « KRAS (G12C) Inhibitor-12 » (composé-outil, rho −0,053, rien). Les inhibiteurs KRAS de clinique ne sont donc pas testables ici — et la plupart des PDAC sont G12D, pas G12C. Vérification indépendante : rhos et moyennes par tertile reproduits à l'identique, composé par composé, par un second calcul direct. Fichiers : `data/gdsc_kras_screen.csv` (269 composés, SHA `e3bbdc17…`), `data/gdsc_kras_screen_pathways.csv`, `data/gdsc_kras_screen_targets.csv`, `gdsc_kras_screen.log`, `gdsc_kras_screen_stdout.txt`.

### 8.18 Thérapies ciblées MUC16 (CA125) et CLDN18.2 — les deux marqueurs ont-ils un médicament derrière eux ? (16 nov. 2026, 07h42–07h50)

**Mandat :** ordre de Zackary, 16 nov. 07h41 : « Continue jusqu'à ce que tu trouve un remède ». Rapport complet : `muc16_cldn182_therapies.md` ; revue détaillée : `literature_muc16_cldn182_draft.md` (31 sources) ; provenance : `PROVENANCE_muc16_cldn182.md`. Les trois affirmations pivots ont été vérifiées indépendamment (deux sources concordantes chacune).

**MUC16 / CA125 — NON, aucune piste médicamenteuse réelle pour le pancréas.** Le seul anti-MUC16 testé chez des patients pancréatiques (sofituzumab védotine / DMUC5754A, phase I, NCT01335958, 11 patients) n'a donné **aucune réponse confirmée** chez eux (les 7 réponses étaient toutes ovariennes ; Liu et al., *Ann Oncol* 2016). Le second ADC (DMUC4064A) n'a **jamais eu un seul patient pancréatique** (programme arrêté avant l'enrôlement ; Liu et al., *Gynecol Oncol* 2021, texte intégral lu). Les CAR-T anti-MUC16 ne sont que précliniques pour le pancréas (souris, 2024) ; oregovomab et abagovomab ont échoué en phase III dans l'ovaire et n'ont jamais été testés dans le pancréas. **MUC16 reste un biomarqueur pronostique, pas une cible thérapeutique validée.**

**CLDN18.2 — OUI, une piste réelle mais précoce, et un échec randomisé.** Le zolbetuximab (anticorps nu, approuvé en gastrique oct. 2024 : SPOTLIGHT 18,2 vs 15,5 mois ; GLOW 14,4 vs 12,2 mois) a **échoué** dans le pancréas : essai randomisé GLEAM (n = 393, NCT03816163), survie globale médiane **13,7 vs 13,6 mois, HR 0,999, p = 0,499** (communiqué Astellas 14 oct. 2025 ; chiffres complets ESMO GI 2026, Park et al., résumé 342O) — programme pancréatique arrêté. Mais des modalités plus puissantes montrent des signaux réels en phase I/II, bras uniques : l'ADC **IBI343** (phase I, NCT05458219, 83 patients : réponse confirmée **22,7 %**, contrôle de la maladie 81,8 %, SSP méd. 5,4 mois, SG méd. 9,1 mois à 6 mg/kg, n = 44 ; Yu et al., *J Clin Oncol* 2025 ;43:4017) est en **phase III pancréatique** (G-HOPE-002, NCT07066098, en recrutement) ; le CAR-T **satri-cel / CT041** (réponse 16,7 % dans le pancréas, NCT04404595) ; le bispécifique **IBI389** (réponse 29,6 %, NCT05164458, communiqué d'entreprise). **Aucun remède démontré** : la seule preuve randomisée pancréatique est négative. Prévalence : CLDN18.2 fort (≥ 75 %) chez ~28 % des métastatiques — la cible ne couvre qu'une fraction des patients.

**Vérification mesurée sur nos 4 cohortes** (script `check_expression_muc16_cldn18.py`, CSV de flux déjà construits, aucune reconstruction) : le groupe KRAS fort est enrichi en MUC16 élevé dans 3 cohortes sur 4 (4–6/12 dans le quartile supérieur, contre 3 attendus ; ICGC 4/12, au hasard) et en CLDN18 élevé dans 3 sur 4 aussi (4–5/12 ; ICGC 3/12). En TCGA, paradoxe : CLDN18 rho +0,262 (p < 0,001) sur toute la série mais top12 −0,02 sd — il monte avec KRAS puis retombe à l'extrême (l'effondrement v4). **Double-positifs (MUC16 ET CLDN18 au-dessus du quartile supérieur) chez les KRAS-forts : 0/12, 2/12, 1/12, 0/12** — pas de sous-groupe « les deux cibles élevées », pas de base pour une combinaison des deux cibles. **LIMITE : l'ARN CLDN18 n'est pas l'IHC CLDN18.2 protéique qui décide de l'éligibilité** (≥ 75 % des cellules en IHC pour GLEAM) — aucun seuil ARN ne dit qui serait éligible.

**TCGA clinique — chimiothérapie : question sans réponse possible.** Le fichier clinique (184 patients) ne contient **aucune colonne chimiothérapie**. Seule la radiothérapie était testable (script `check_tcga_radiation.py`) : pas de différence de prescription selon CA125 (Q4 : 8/41, 20 %, vs reste 35/119, 29 %, Fisher p = 0,307) ; radiothérapie seule associée à une survie plus longue (24,3 vs 19,6 mois, p = 0,017 — observationnel, biais d'indication probable) ; interaction CA125 × radiothérapie non significative (HR 0,77, p = 0,345) — la radiothérapie ne modifie pas le signal CA125. La question de la réponse à la chimiothérapie selon CA125 reste ouverte et demande une autre source.

### 8.19 Médicaments en dose-réponse (PRISM secondaire 19Q4) — NON (16 nov. 2026, 07h41–07h47)

**Données :** le portail DepMap bloque curl avec une page de vérification Cloudflare Turnstile (vérifié 16 nov. : le fichier téléchargé n'est que du HTML, 4 937 octets). Route de repli : miroir figshare de Corsello et al. (*Nat Cancer* 2020, DOI 10.1038/s43018-019-0018-6), article 9393293, DOI 10.6084/m9.figshare.9393293.v4. Fichier principal `secondary-screen-dose-response-curve-parameters.csv` : **264 340 589 octets exacts, MD5 vérifié `e629b9d505ad3d6bf65fde96f1c54bee`** ; 3 fichiers d'accompagnement vérifiés. Journal `prism_secondary_access.log`. Script `prism_secondary_screen.py` (exit 0), provenance `PROVENANCE_prism_secondary.md`.

**Méthode :** 701 004 lignes ; déduplication entre écrans avec priorité MTS010 > HTS002 > MTS006 > MTS005 (le readme recommande MTS010) ; agrégation par nom (médiane). Jointure Model.csv × Chronos KRAS DepMap 24Q4 → **33 lignées pancréas dans le secondaire, 29 communes avec KRAS** (min −4,14, médiane −1,83, max −0,36). Par composé (n ≥ 15) : Spearman AUC et log10(IC50) contre Chronos KRAS + moyennes par tertile + FDR Benjamini-Hochberg. **Tertiles corrigés et vérifiés par assertion** (« fort » = Chronos le plus négatif = le plus dépendant — le bug de `prism_screen.py` n'est pas reproduit). Aucune imputation. AUC jamais manquante ; IC50 manquante sur 48 % des lignes (courbe n'atteignant jamais 50 % de viabilité) — d'où seulement 641 composés testables en IC50.

**Résultat : NON — la dose-réponse ne sauve pas le criblage.** Sur **1 427 composés** testés en dose-réponse (8 points), **zéro composé passe FDR < 0,05** — ni en AUC (FDR min 0,418), ni en IC50 (FDR min 0,619). Seulement 2 composés ont p < 0,001, contre ~1,4 attendus par hasard. Médiane rho AUC −0,013, 47,7 % des rho > 0 : la distribution est symétrique autour de zéro. Top 10 côté sensible (tous FDR ≥ 0,42, curiosités) : naloxone +0,679 ; P22077 (USP7) +0,563 ; estradiol +0,560 ; benzydamine +0,547 ; PF-04217903 (c-Met) +0,528. **Effets de classe (médiane rho AUC) : MEK (18 composés) +0,008 — plat ; RAF −0,056 ; groupe KRAS/MEK/ERK/RAF/SHP2/SOS1 −0,059 ; PARP −0,080 ; EGFR −0,103 ; PI3K −0,065 ; AKT −0,050 ; mTOR −0,054. Aucune classe ne se détache dans le bon sens.** Côté résistant : uprosertib (AKT) −0,625, buparlisib (PI3K) −0,605 — même direction que GDSC2 (KRAS-dépendantes plus résistantes aux inhibiteurs PI3K/AKT).

**Composés ciblés KRAS présents (tous non significatifs) :** tramétinib +0,065 (FDR 0,998), sélumétinib +0,043, cobimétinib +0,095, réfametinib −0,063, PD-0325901 −0,129, dabrafénib −0,056, vémurafénib +0,254, sorafénib +0,267, lonafarnib +0,110. **Absents du secondaire 19Q4** (le secondaire date de 2019) : MRTX1133, RMC-6236, sotorasib, adagrasib, BI-3406, SHP099, TNO155, binimétinib, ulixertinib, SCH772984, ERK_2440, ERK_6604, encorafénib. **Les trois criblages (PRISM primaire, PRISM secondaire, GDSC2) convergent vers le même négatif. Reste non testé : les inhibiteurs KRAS directs de clinique (absents des trois bases) et les combinaisons.** Fichiers : `data/prism_secondary_kras_screen.csv` (1 427 composés, SHA `49f974103d78…`), `data/prism_secondary_kras_screen_moa.csv`, `data/prism_secondary_kras_screen_targets.csv`, `prism_secondary_screen.log`, `prism_secondary_screen_stdout.txt`.

### 8.20 Inhibiteurs directs KRAS G12D / pan-RAS — OUI pour un seul, et une approbation FDA (16 nov. 2026, 07h42–07h50)

**Verdict : on peut tester ces inhibiteurs contre l'axe KRAS avec des données publiques pour un seul composé — MRTX1133 — et le test est positif. Pour RMC-6236, RMC-9805, ASP3082, sotorasib, adagrasib, BI-3406 et TNO155, aucune matrice publique de dose-réponse n'existe. Et le fait clinique le plus fort du dossier : le daraxonrasib (RMC-6236) a doublé la survie médiane en phase III et a été approuvé par la FDA — une avance réelle, pas un remède, et pas une prédiction du pipeline.**

**Présence dans les criblages (vérifiée par nom exact) :** MRTX1133 et SHP099 sont dans PRISM (6 790 composés) ; rien d'autre. GDSC2 (269) ne contient que l'outil KRAS (G12C) Inhibitor-12. PRISM secondaire (1 427 composés) ne contient aucun des 10 composés cibles. MRTX1133 était déjà dans le criblage PRISM du 15 nov. (rho +0,410, p=0,011, FDR 0,76 — non significatif après correction) : sans découpage par allèle, le signal se noie.

**Le test nouveau, par allèle KRAS** (script `mrtx1133_prism_allele.py`, SHA `932fcafc…b85be` ; allèles tirés du MAF DepMap 24Q4, 98 439 503 octets, SHA `86b8530b…5e96f` ; 54 lignées pancréas : G12D 23, G12V 20, G12R 5, Q61H 2, Q61R 1, G12C 1, G12A 1, G12I 1 ; 40 lignées dans PRISM). Sur 40 lignées pancréas PRISM (dose unique 2,5 µM), **vérifié indépendamment, chiffres exacts :**
- MRTX1133 tue son allèle cible : viabilité G12D **−1,70** (n=17) contre −0,38 (autres, n=23), **Mann-Whitney p=0,0001** ; G12V −0,37, G12R −0,29.
- L'axe Chronos KRAS prédit la sensibilité chez les G12D : Spearman **rho +0,47 (p=0,079, n=15)** — direction juste, effectif trop petit pour conclure ; toutes lignées rho +0,36 (p=0,031, n=36) ; non-G12D rho +0,11 (p=0,65, rien).
- Contrôles : SHP099 rien ; K-RAS(G12C)-INHIBITOR-6 rien. Note : le rho SHP099 −0,064 (p=0,74) cité dans le rapport est la valeur du criblage primaire du 15 nov. (n=29) ; recalculé sur le fichier allèle : −0,016 (p=0,93, n=28) — même conclusion (rien).
- ChEMBL : MRTX1133 `CHEMBL4858364`, 45 activités (Hallin 2022) — IC50 pancréas : PANC-1 2,3 nM, AsPC-1 11,0 nM, HPAC 4,2 nM, HPAF-II 14,9 nM, Panc 04.03 27,6 nM, PK-59 2,9 nM ; WT ~3 000–6 500 nM. Daraxonrasib `CHEMBL6168538`, 85 activités — HPAC 1,2 nM, Capan-2 1,4 nM, Capan-1 (G12V) 1,3 nM, AsPC-1 (G12D) 3,1 nM. RMC-9805 et ASP3082 : 0 résultat ChEMBL.
- Limite du test MRTX1133 : dose unique 2,5 µM (pas de courbe dose-réponse), n=15 G12D — le rho +0,47 est suggestif, pas une preuve.

**Composé par composé (essais, sources nommées) :**
- **MRTX1133** (G12D, Mirati/BMS) : préclinique Hallin et al. *Nat Med* 2022 (DOI 10.1038/s41591-022-02007-7) — régression ≥30 % dans 8/11 modèles PDAC. Clinique **NCT05737706 TERMINATED** début 2025 (formulation/PK après rachat Mirati par BMS).
- **RMC-6236 / daraxonrasib** (pan-RAS ON) : phase I/II NCT05379985, NEJM 2026 Wolpin (n=168, ORR 29 %) ; phase III **RASolute-302 NCT06625320 : OS 13,2 contre 6,7 mois, HR 0,40** ; **FDA approuvé le 26 août 2026 (RASONQUE™)** pour le PDAC métastatique prétraité — vérifié indépendamment sur plusieurs sources (communiqué FDA, *Drug Discov Ther* 2026 ;20:400–402, Cancer Network) ; adjuvant phase III RASolute-304 NCT07252232 ; 1re ligne RASolute-303 NCT07491445 en cours. **C'est un résultat clinique, pas une prédiction du pipeline : l'approbation ne dépend pas de l'axe.**
- **RMC-9805 / zoldonrasib** (G12D ON) : phase I NCT06040541 ; phase III NCT07805954 (+ daraxonrasib contre gem/nab-paclitaxel, 1re ligne G12D). Aucune donnée cellulaire publique.
- **ASP3082** (PROTAC G12D, Astellas) : phase I NCT05382559, 33,3 % à 300 mg (phase précoce). Aucune donnée cellulaire publique.
- **Sotorasib** (G12C) : CodeBreaK 100 NCT03600883, PDAC n=38 : ORR 21 %, DCR 84 %, PFS 4,0 mois, OS 6,9 mois. G12C = 1–2 % des PDAC. **Adagrasib** (G12C) : KRYSTAL-1 NCT03785249, PDAC n=21 : ORR 33 %, DCR 81 %, PFS 5,4 mois, OS 8,0 mois.
- **BI-3406** (SOS1) : jamais en clinique ; dérivé BI-1701963 phase I NCT04111458 (+ tramétinib). **SHP099 / TNO155** (SHP2) : TNO155 phase I NCT03114319, 20 % maladie stable.
- Autres repérés : INCB161734 (G12D, 41 patients PDAC, ASCO GI 2026) ; HRS-4642 + gem/nab-paclitaxel NCT06520488, DCR 93,3 % ; TSN1611 NCT06385925 ; LY3962673 NCT06586515 ; LY4066434 NCT06607185 ; BBO-10203 NCT06625775.

**Combinaisons publiées (pancréas) :** MRTX1133 + cetuximab (EGFR) : synergie (Hallin 2022 ; organoïdes G12D, *Gastroenterology* 2024, Bliss > 10). MRTX1133 + alpelisib (PI3Kα) : synergie. MRTX1133 + MEK/ERK/SHP2/SOS1 : pas de renforcement notable. MRTX1133 + gem/nab-paclitaxel : régression supérieure en modèles murins. MRTX1133 + anti-PD-1/PD-L1 : élimination durable, dépend des CD8+ (Kemp et al. 2023). RMC-6236 + PI3Kα/δ : synergie. RMC-6236 + gem/nab-paclitaxel : RASolute-303 phase III. RMC-6236 + RMC-9805 : NCT07805954 phase III. **KRAS + autophagie : non fouillée** (aucune source trouvée — reste à faire).

**Ce qui manque exactement :** aucune matrice publique de dose-réponse multi-lignées pour RMC-6236, RMC-9805, ASP3082, sotorasib, adagrasib, BI-3406, TNO155. Il existe : (a) des valeurs isolées par lignée dans les articles (ChEMBL — trop peu de lignées pour un test d'axe), (b) des données d'entreprise non publiques, (c) des essais cliniques. Pour tester le daraxonrasib contre l'axe, il faudrait un criblage type PRISM/GDSC incluant ce composé sur ≥15 lignées pancréas avec allèles connus, ou les données des entreprises. Fichiers : `kras_g12d_inhibitors.md`, `mrtx1133_prism_allele.py`, `data/kras_alleles_pancreas.csv` (SHA `9ac803ad…0d42`), `data/mrtx1133_prism_kras_allele.csv` (SHA `7a449c92…6e5ef`), `PROVENANCE_kras_g12d.md`.

### 8.21 Balayage CRISPR génome entier — 2 partenaires réels mais faibles, pas un remède (16 nov. 2026, 07h42–07h58)

**Verdict : le balayage trouve 2 gènes, TCF7L2 et PRDX4, plus essentiels dans les lignées pancréas KRAS-dépendantes (FDR < 0,05, le nul donne 0 hit). Mais ce ne sont pas des cibles de médicament : TCF7L2 est un facteur de transcription sans poche druggable, PRDX4 une enzyme antioxydante sans médicament connu, et leur essentialité absolue est faible. Aucun effet de classe, aucun candidat connu significatif. Ce bras ne donne pas un remède — il donne 2 pistes faibles à noter, pas à poursuivre comme cibles.**

**Méthode :** données déjà sur disque, non re-téléchargées : DepMap 24Q4 `CRISPRGeneEffect.csv` (428 678 699 octets, SHA `3d8f3ec6…`) + `Model.csv`. **47 lignées pancréas** dans GeneEffect (68 dans Model.csv, 21 absentes, jamais imputées). Axe Chronos KRAS : min −4,143, médiane −1,758, max −0,180. Script `crispr_genome_scan.py` (exit 0, 37,9 s). Lecture par blocs, Spearman par gène sur paires complètes, p par loi t, BH-FDR sur **17 787 gènes testés** (129 exclus, n < 30 paires). **Contrôle de cohérence réussi :** les 10 rhos v4 du 15 nov. reproduits à l'identique (écart 0,00, ex. CLDN18 +0,045, MUC16 −0,117, CLCA1 +0,232). Contrôle positif KRAS lui-même : rho = 1,0.

**Les 3 hits FDR < 0,05 (le nul : 0) :**
| Gène | rho | p | FDR | Chronos moyen fort / moyen / faible |
|---|---|---|---|---|
| KRAS (contrôle) | +1,000 | 0 | 0 | −2,66 / −1,77 / −0,94 |
| **TCF7L2** | +0,614 | 4,38e-06 | **0,039** | −0,43 / −0,31 / +0,05 |
| **PRDX4** | +0,602 | 7,64e-06 | **0,045** | −0,25 / −0,16 / −0,10 |

4e gène sous FDR < 0,10 : PSMD2 (rho +0,585, FDR 0,071) — non significatif. Sous le 3e, tout est FDR > 0,05 — le reste du top 30 est du bruit probable. On remarque 4 sous-unités du protéasome dans le top 30 (PSMD2, PSMA2, PSMB3, PSMD8, PSMC3) : un début d'effet de classe protéasome, mais aucun de ces gènes n'est significatif seul, et les inhibiteurs du protéasome ciblent les sous-unités catalytiques 20S, pas celles-ci. **Aucun hit FDR < 0,05 dans la direction négative** (gènes moins essentiels / protecteurs).

**Candidats connus de la littérature — tous non significatifs :** RAF1 +0,429 (FDR 0,45, rang 51/17 787) ; PLK1 +0,427 (0,45, rang 53) ; BCL2L1 (BCL-XL) +0,415 (0,49, rang 71) ; CDK4 +0,231 (0,79) ; MYC +0,133 (0,91) ; CDK6 +0,090 ; MAPK1 +0,050 ; PIK3CA +0,035 ; STK33 +0,024 ; MAPK3 +0,006 ; MTOR −0,039 ; TBK1 −0,172 (mauvaise direction) ; AURKA −0,216 (mauvaise direction). RAF1, PLK1 et BCL2L1 pointent dans le bon sens (top ~50–70) mais ne survivent pas à la correction : curiosités, pas des résultats.

**Pourquoi ce n'est pas un remède :** TCF7L2 — facteur de transcription, effecteur de la voie Wnt/β-caténine ; vérifié ChEMBL (UniProt Q9NQB0) : 3 cibles, toutes des complexes ou interactions protéine-protéine — aucune entrée « single protein » druggable directe, pas de poche à cibler avec une petite molécule classique. PRDX4 — peroxiredoxine 4, enzyme antioxydante ; vérifié ChEMBL (Q13162) : 1 cible, 17 activités ; aucun médicament approuvé identifié. DGIdb non vérifié par cette voie (API non exploitable) — marqué « à vérifier », rien inventé. **L'effet absolu est faible :** TCF7L2 −0,43 et PRDX4 −0,25 dans le tertile le plus KRAS-dépendant, contre un seuil usuel de dépendance autour de −0,5 à −1. Corrélation ≠ causalité, n = 47 lignées, aucune validation expérimentale ici. **Le côté CRISPR du « remède » est épuisé sur ces données : il ne reste pas de vulnérabilité forte non testée dans DepMap 24Q4.** Fichiers : `crispr_genome_scan.py`, `data/crispr_genome_scan.csv` (17 916 gènes, SHA `673e7080…`), `PROVENANCE_crispr_scan.md`, `crispr_genome_scan.log`, `crispr_genome_scan_stdout.txt`.

### 8.22 Combinaisons — OUI, vopimetostat + daraxonrasib, 82 % de réponses (16 nov. 2026, 07h58–08h10)

**Verdict : oui — vopimetostat (inhibiteur PRMT5) + daraxonrasib (pan-RAS), chez les patients MTAP-délétés : 82 % de réponses (18/22), contrôle de la maladie 100 %, survie sans progression à 9 mois 88 %, médiane non atteinte** (phase 1/2 NCT06922591, ESMO 2026, communiqué Tango du 23 oct. 2026, dépôt SEC 8-K ; **vérifié indépendamment sur plusieurs sources** : ORR 82 % (18/22), DCR 100 %, PFS 6 et 9 mois 88,4 %, suivi médian 7,1 mois, coupure 20 août 2026). C'est la première combinaison du projet dont les chiffres dépassent nettement la monothérapie daraxonrasib (~30 % de réponses). Limites honnêtes : non randomisé, n=22, un seul sous-groupe (MTAP-délété), pas de survie globale — la phase 3 randomisée est prévue au 1er semestre 2027. Ce n'est pas un remède démontré, c'est la piste la plus solide du projet.

**Les autres combinaisons (revue, 11 sections dans le rapport) :**
- **Vopimetostat + zoldonrasib : 54 % de réponses, PFS 9 mois 61 %, n=35.**
- **Daraxonrasib + chimiothérapie (RASolute-303, NCT07491445)** : phase 3 randomisée en cours (recrutement depuis avril 2026, sites Toronto/Montréal) ; ORR 58 % en données précoces non randomisées, aucun résultat randomisé.
- **Daraxonrasib + zoldonrasib (RASolute-309, NCT07805954)** : phase 3 en cours (premiers patients oct. 2026), aucun résultat.
- **MEK + autophagie (tramétinib + hydroxychloroquine) : échec clinique.** Synergie préclinique réelle (Kinsey et al. *Nat Med* 2019, PMID 30833748 ; Bryant 2019), mais Witte 2024 (PMID 39352477) : PFS 52 jours, survie 68 jours, tous en progression ; Tang 2023 : PFS 2,0 mois ; essais THREAD (NCT03825289) et PaTcH (NCT05518110) arrêtés en 2026.
- **MEK + CDK4/6 (tramétinib + palbociclib) : échec clinique** (Witte 2024 : PFS 56 jours, 1/9 réponse partielle ; Tang 2023 : PFS 2,8 mois) malgré la synergie préclinique.
- **MEK + PI3K : rien dans le pancréas** (Bedard 2015, PMID 25500057 : meilleure réponse = maladie stable).
- **KRAS + SHP2/SOS1** : synergie mesurée (Tapia Contreras 2025, *Mol Oncol*) mais sur G12C = 1–2 % des PDAC.
- **KRAS + anti-PD-1** : préclinique fort (MRTX1133 + anti-CTLA-4/PD-1, éradication synergique chez la souris, Kemp et al. bioRxiv 2023 ; MRTX1133 + olaparib, *Nat Commun* 2026) mais **zéro donnée humaine pancréatique** — les données publiées sont du poumon (KRYSTAL-7, SUNRAY-01).

**Données de combinaisons — la matrice récupérée et le test demandé :**
- **PANC-1 (NCATS, Pourmousa et al. *Nat Commun* 2025)** : 8 fichiers CSV téléchargés via GitHub (tailles vérifiées contre l'API, SHA consignés). **496 combinaisons mesurées, 280/496 synergiques (56,5 %), 12 fortes (gamma < 0,5)** ; top : panobinostat + carfilzomib (gamma 0,035). **Zéro paire avec un inhibiteur MEK/KRAS/ERK ou l'hydroxychloroquine** — les 32 composés n'en contiennent aucun (vérifié : aucune cible MEK/KRAS/ERK dans la liste). PANC-1 Chronos KRAS = −1,658 (dépendant).
- **Le test « la dépendance KRAS prédit-elle le bénéfice de la combinaison ? » n'a pas pu être fait : aucune matrice publique multi-lignées pancréas n'existe en accès libre.** ALMANAC (NCI-60), AZ-DREAM (85 lignées : sein/poumon/vessie/GI) et O'Neil (39 lignées : sein/côlon/poumon/mélanome/ovaire/prostate) ne contiennent **aucune** lignée pancréas — vérifié dans les articles. DrugComb : portail injoignable depuis cette VM le 16 nov. 2026 (curl HTTP 000/exit 52, DNS/connexion refusée, autres sites OK) — documenté exactement ; son seul contenu pancréatique serait FORCINA (1 lignée). Le fichier MIT/test.csv (10 000 scores) est constitué de **prédictions de modèle, pas de mesures** — exclu.

**Prochaines étapes nommées :** phase 3 vopimetostat + daraxonrasib (1H 2027) — c'est elle qui dira si les 82 % tiennent ; RASolute-303/309 en cours ; KRAS + immunothérapie et KRAS + PARP restent les deux hypothèses précliniques les plus fortes après PRMT5, sans donnée humaine pancréatique. Fichiers : `kras_combinations.md`, `PROVENANCE_kras_combinations.md`, `analyze_panc1_combos.py`, `data/panc1_combinations_summary.csv` (SHA `423ac175…`), `data/panc1_ncata/` (8 fichiers sources + SHA + README).

### 8.23 Paysage immunitaire le long de l'axe KRAS (v6) — tumeur froide, KRAS + anti-PD-(L)1 NON (16 nov. 2026, 08h57–09h27)

**Verdict : oui, le paysage immunitaire change le long de l'axe KRAS — et c'est une tumeur « froide », pas une cible anti-PD-(L)1.** Les lymphocytes T baissent quand KRAS monte, dans les 4 cohortes ; PD-L1 ne monte pas de façon fiable. **Combinaison KRAS + anti-PD-(L)1 : NON soutenue.**

**Méthode (protocole gelé, runs v6 mesurés) :** 4 cohortes, ordre KRAS **brut** croissant, 12 gènes immunitaires (CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274/PD-L1, PDCD1/PD-1, CTLA4, GZMB, IFNG, CD19), 8 runs v6 fast (réel + nul, graine 42), cible CD8A. Matrices vérifiées, rien re-téléchargé. Écart documenté : en ICGC, IFNG→PRF1 et CD19→MS4A1 (CD20) — le protocole ne nommait qu'un seul remplaçant. SHA des CSV : TCGA `66dbb672…`, GSE71729 `8987ffca…`, GSE62452 `97c4689a…`, ICGC `10823879…`.

**Tests directs (verdict principal) — Spearman contre KRAS (TCGA / GSE71729 / GSE62452 / ICGC) :** CD8A −0,19 / −0,16 / −0,35 / −0,15 ; PDCD1 (PD-1) −0,25 / −0,24 / −0,22 / −0,22, top-12 d −0,61 / −0,88 / −0,70 / −0,85, significatif (Welch) dans les 4 cohortes ; CD4 −0,15 / −0,30 / −0,15 / −0,16 ; FOXP3 −0,10 / −0,09 / −0,34 / −0,20 ; CD19 −0,18 / −0,09 / −0,42 (absent ICGC) ; CD68 +0,07 / +0,22 / +0,17 / +0,18 (1 p < 0,05 sur 4) ; **CD274 (PD-L1) +0,26 (p=0,0006) en TCGA seulement, −0,11 / +0,18 / +0,18 ailleurs, top-12 significatif nulle part.** 16/48 tests p < 0,05 contre ~2,4 attendus sous le nul. Signe constant sur 4 cohortes : CD8A, CD4, FOXP3, PDCD1 (négatifs), CD68 (positif faible).

**Runs v6 : ne séparent pas réel et nul.** MC réel vs nul : TCGA 0,379/0,324 ; GSE71729 0,344/0,324 ; GSE62452 0,369/0,348 ; ICGC 0,334/**0,368 (réel sous le nul)**. Delta net seulement en TCGA (4,21 vs 2,30). L7a DOWN 18 %/39 % (TCGA/GSE71729), UP 50 % en GSE62452/ICGC = repli NaN confirmé (`scores_unavailable`, n < 75 — artefact §8.14). Le nul fabrique lui aussi des cascades complètes. Le verdict vient des tests directs.

**Limite majeure :** ARN en vrac sans correction de pureté — la baisse des marqueurs T peut être une composition (moins de T / plus de tumeur) autant qu'une expression par cellule ; le mécanisme n'est pas établi. **Ce que ça veut dire :** la cible (PD-L1) n'est pas plus haute là où KRAS est fort, et les T à débloquer sont moins nombreux. La piste qui reste : comprendre pourquoi les T disparaissent quand KRAS monte. Fichiers : `immune_v6.md`, `PROVENANCE_immune_v6.md`, `build_fluxes_immune.py`, `immune_direct_tests.csv`, `immune_v6_runs_summary.json`, `results_fast_immune_*(_nul)/` (8 dossiers).

### 8.24 Paysage réparation / PARP le long de l'axe KRAS (v6) — axe BRCA2/ATR/RAD51, KRAS + PARP NON (16 nov. 2026, 08h57–09h11)

**Verdict : oui, le paysage de la réparation change le long de l'axe KRAS — mais PAS du côté PARP.** Ce qui monte avec KRAS, répliqué, c'est l'axe **BRCA2 / ATR / RAD51**. PARP1/PARP2 sont plats dans les deux cohortes. **Combinaison KRAS + PARP : NON** — trois angles indépendants convergent vers le négatif (expression plate ici, CRISPR sans dépendance, PRISM sans effet de classe). La piste cohérente qui sort de ce bras, c'est **ATR / CHEK1 (stress de réplication)**, à tester — pas une conclusion.

**Méthode (protocole gelé, runs v6 mesurés) :** TCGA PAAD (178), ordre KRAS brut croissant, 12 gènes (PARP1, PARP2, BRCA1, BRCA2, ATM, ATR, CHEK1, CHEK2, RAD51, XRCC1, POLQ, FANCD2), 2 runs v6 fast (réel + nul, graine 42), cible PARP1. Tous les gènes présents, 178/178 valeurs valides, aucune imputation. Contrôle GEO GSE71729 (145, tests directs seulement) fait car le temps le permettait.

**Tests directs TCGA :** 7/12 p < 0,05 ; 3 survivent à Bonferroni : **BRCA2 rho +0,420 (p 5,2×10⁻⁹, top12 +0,54 sd)**, **ATR +0,407 (p 1,7×10⁻⁸, +0,44)**, **POLQ +0,289 (p 9,1×10⁻⁵, +0,41)**. PARP1 −0,047 (p 0,54), PARP2 −0,088 (p 0,24). Nul : 1/12 p < 0,05, |rho| max 0,190. **Contrôle GEO :** CHEK1 +0,505 (p 9,5×10⁻¹¹), **BRCA2 +0,481 (p 9,4×10⁻¹⁰)**, RAD51 +0,427 (p 8,5×10⁻⁸), **ATR +0,250 (p 0,0024)** ; nul 0/12. **Répliqués : BRCA2, ATR, RAD51.** Non répliqués : POLQ (TCGA +0,289, GEO −0,023) et CHEK1 (forme différente). PARP1/PARP2 plats aussi en GEO.

**Runs v6 : ne séparent pas réel et nul** (MC 0,355 vs 0,331 ; Delta 4,30 vs 4,04 ; L7a UP 16,84 % désaccord vs UP 39,28 %). **Faits cités sans être réimportés :** CRISPR PARP1 +0,157 (FDR 0,89), PARP2 −0,120, BRCA1 −0,131, CHEK1 +0,260 (FDR 0,75) — tous NS ; PRISM aucun effet de classe PARP (médiane rho +0,032, 25 inhibiteurs). **Limites :** ARN bulk sans correction de pureté ; prolifération non contrôlée (BRCA2/ATR/CHEK1/RAD51 sont aussi des gènes du cycle) ; expression ≠ protéine ≠ mutation — l'indication PARP validée (mutation germinale BRCA, olaparib/POLO) n'est pas testée et n'est pas remise en cause. Fichiers : `parp_v6.md`, `PROVENANCE_parp_v6.md`, `pdac_tcga_fluxes_parp.csv` (SHA `c9549b68…c4309`), `results_fast_parp/` et `results_fast_parp_nul/`, `parp_direct_tests.csv`, contrôle GEO `parp_direct_tests_geo71729.csv`.

**Rapport combiné des deux bras :** `immune_parp_v6.md`, `PROVENANCE_immune_parp_v6.md`.

### 8.25 Re-test ATR/CHEK1 — la piste est redressée, pas fermée (16 nov. 2026, 09h28–09h45)

**Verdict : la hausse survit à la pureté, pas à la prolifération — sauf pour ATR seul. Le « stress de réplication » large était de la prolifération. ATR reste ouvert comme hypothèse d'expression, sans aucun appui en dépendance CRISPR ni en médicaments. CHEK1 est un marqueur de prolifération, pas une piste KRAS.**

**1. Pureté (TCGA, 178) — OUI, le signal est réel.** Correction v3 identique à la v4. R² pureté des 7 gènes : 0,02 % à 3,2 % seulement. Après correction : BRCA2 rho **+0,425** (brut +0,420), ATR **+0,409** (brut +0,407), CHEK1 +0,116, RAD51 +0,170, POLQ +0,275. Top12 brut contre résidu : 11/12 patients communs. Nul (graine 42) : |rho| max 0,171.

**2. Prolifération (TCGA) — le signal large meurt, ATR survit.** Le confondant est réel : score prolifération (médiane MKI67/TOP2A/PCNA/CCNB1) contre rang KRAS **+0,386 (p = 1,1×10⁻⁷)**. Rho gène–prolif : RAD51 +0,791, POLQ +0,768, CHEK1 +0,645, BRCA2 +0,543, **ATR +0,214** (le moins lié). Après double correction + Spearman partiel : **BRCA2 +0,266 (p 3,3e-4) / partiel +0,305 (p 3,6e-5)** — survit, mais top12 effondré (+0,08 sd) ; **ATR +0,273 (p 2,3e-4) / partiel +0,366 (p 5,6e-7)** — survit ; CHEK1 −0,087 / −0,143, RAD51 −0,187 / −0,171 (inversé), POLQ −0,008 / +0,023 — **morts**. Sensibilité au score brut : mêmes partiels. Signal secondaire : CHEK2 devient négatif après contrôle (−0,312, p 2,2e-5), non répliqué — curiosité notée, pas un verdict.

**3. Contrôles ICGC (70) et GSE62452 (69) — mêmes tests que GEO71729.** **ICGC : 0/7.** BRCA2 −0,023, ATR +0,056, CHEK1 +0,163, RAD51 +0,063, POLQ +0,037. L'axe KRAS-expression y est plat (prolif contre KRAS +0,080, ns), comme déjà vu pour CA125/CEA. **GSE62452 : 5/7 en brut** (ATR +0,656 p 9,4e-10, CHEK1 +0,610, BRCA2 +0,495, POLQ +0,447, RAD51 +0,352) mais prolif contre KRAS +0,597 (p 6,1e-8) et rho gène-prolif jusqu'à +0,920 (CHEK1). Après contrôle partiel : **seul ATR survit, +0,488 (p 2,4e-5)** ; BRCA2 +0,094, CHEK1 +0,192, RAD51 −0,164, POLQ −0,137 — morts. **Réplication brute (4 cohortes) :** ATR 3/4, BRCA2 3/4, RAD51 3/4, CHEK1 2/4, POLQ 2/4, PARP1/PARP2 0/4. **Après contrôle prolif :** ATR survit 2/2 cohortes où le signal existait, BRCA2 1/2, CHEK1/RAD51/POLQ 0/2.

**4. Runs v6 (flux TCGA corrigés pureté, 12 gènes, ordre KRAS résidu) — exit 0 / 0.** Réel : T_0 3,19 % (identique au bras PARP brut), T_+1 45,12 %, MC 0,358, Delta 4,096, L7a DOWN 16,06 % (désaccord), L7b FRAGILE. Nul : T_0 8,52 %, MC 0,325, Delta 4,001, L7a UP 40,59 %, L7b FRAGILE. **Ne sépare pas réel et nul**, comme le bras PARP. Le verdict repose sur les tests directs, comme établi.

**5. Inhibiteurs ATR/CHEK1 dans les 3 criblages existants — NON (0/60 FDR < 0,05).** 60 vrais inhibiteurs trouvés (bug de matching corrigé en cours de route : la 1re version attrapait les inhibiteurs de métalloprotéases via « MATRIX » contenant « ATR » — CSV régénéré, valeurs des vrais inhibiteurs inchangées). Ceralasertib (AZD6738) : PRISM +0,132 (FDR 0,956), GDSC2 −0,137 (FDR 0,605). Prexasertib (LY2606368) : +0,059 / −0,050. Plus forts : inhibiteur WEE1/CHEK1 GDSC2 −0,408 (FDR 0,174), ETP-46464 secondaire +0,330 (FDR 0,865), VE-821 GDSC2 −0,374 (FDR 0,194) — aucun ne survit à la correction. Berzosertib et SRA737 absents des 3 criblages.

**6. Dépendance CRISPR (balayage génome entier, déjà mesuré) — NON.** ATR +0,191 (FDR 0,865), CHEK1 +0,260 (FDR 0,748), BRCA2 −0,042, RAD51 −0,024, POLQ −0,246 — tous ns.

**Conclusion :** piste ATR/CHEK1 redressée — le « stress de réplication » large est fermé (prolifération). Reste ouvert : **ATR seul, hypothèse d'expression** — monte avec KRAS au-delà de la prolifération dans 2 cohortes sur 3 où l'axe existe, sans appui CRISPR ni médicament. Aucun test ici ne justifie une combinaison KRAS + ATR/CHEK1. Ce qui pourrait rouvrir la question : un criblage dose-réponse d'inhibiteurs ATR sur lignées pancréas avec allèles KRAS connus (comme le test MRTX1133 par allèle), ou des données cliniques de combinaison — aucune des deux n'existe dans ce projet. Fichiers : `atr_chek1_retest.md` (SHA `498b5ca4…`), `PROVENANCE_atr_chek1.md`, `atr_chek1_retest.py` (`df6d1ddf…`), `atr_chek1_direct_tests_tcga.csv` (`c19bbb70…`), `atr_chek1_cohorts.py` (`c5d5505e…`), `atr_chek1_direct_tests_cohorts.csv` (`1358f742…`), `atr_chek1_drugs.py` (`d4e81d76…`), `atr_chek1_drugs.csv` (`f1321d38…`), `pdac_tcga_fluxes_atr.csv` (`88e52311…`) + nul (`e7001154…`), `run_atr_v6.sh`, `runs_atr_v6.log` (exit 0/0), `results_fast_atr/` et `results_fast_atr_nul/` (36 fichiers chacun).

### 8.26 MTAP / PRMT5 et l'axe KRAS — délétion non démontrée enrichie, PRMT5 monte en expression (16 nov. 2026, 14h37–14h59)

**Verdict : NON, la délétion MTAP n'est pas démontrée enrichie chez les KRAS-forts — donc la combinaison vopimetostat + daraxonrasib ne s'adresse pas aux mêmes patients que l'axe KRAS. Elle cible les MTAP-délétés — 24 % des tumeurs (43/177) — un sous-groupe qui recoupe la moitié des KRAS-forts sans être le même groupe. Fait nouveau : l'expression PRMT5 monte avec KRAS — mais expression ≠ dépendance (le CRISPR ne montre aucune dépendance PRMT5 liée à KRAS). Hypothèse à tester, pas une cible validée.**

**Délétion MTAP mesurée (GISTIC −2, pas un proxy — le fichier GISTIC était accessible) : 6/12 KRAS-forts (50 %) contre 37/165 (22 %) ; OR 3,46 ; Fisher bilatéral p = 0,073 — non significatif** (critère pré-enregistré). Permutation unilatérale p = 0,038, mais avec 12 KRAS-forts la puissance est trop faible pour trancher. Expression MTAP : aucun lien avec l'axe (rho +0,125, p = 0,097 ; top-12 −0,27 sd). CDKN2A : rien (expression rho −0,063 ; délétion 6/12 contre 43/165, Fisher p = 0,095). Perte quelconque (−2 ou −1) secondaire : MTAP 11/12 (p = 0,029) — mais la perte −1 n'abaisse pas l'expression MTAP, donc pas une délétion fonctionnelle. Co-délétion 9p21 vérifiée : 43/43 MTAP −2 co-délétées avec CDKN2A ; CDKN2A −2 seul : 6.

**PRMT5 monte en expression avec KRAS :** rho +0,196 (p = 0,0087, Bonferroni 3 gènes OK), top-12 +0,83 sd (Welch p = 0,0007, d de Cohen +0,84), et +0,216 après correction pureté. Mais le CRISPR DepMap (balayage génome entier, déjà mesuré) ne montre aucune dépendance PRMT5 liée à KRAS (rho −0,189, FDR 0,87) ; MTAP +0,071, CDKN2A +0,161 — tous NS. **Suivi suggéré (non lancé) :** dépendance PRMT5 contre statut MTAP **mesuré** dans DepMap, plutôt que contre KRAS. Fichiers : `mtap.md`, `PROVENANCE_mtap.md`, `mtap_kras_tests.py`, `mtap_direct_tests.csv`, `mtap_controls.csv`, `mtap_gistic_status.csv`, `data/tcga_paad_gistic.tar.gz` (MD5 `816034f7…`).

### 8.27 Pan-cancer : l'axe KRAS → CA125/CEA ne se réplique pas (16 nov. 2026, 14h37–14h59)

**Verdict : NON — CA125 reste un marqueur pancréatique, pas une lecture universelle de KRAS. CA125 (MUC16) est plat dans le poumon et le côlon ; CEA montre un lien monotone faible sans enrichissement des KRAS-forts. Fait nouveau inattendu : le côlon a son propre programme lié à KRAS.**

**Méthode :** TCGA LUAD (515 tumeurs) et COAD (285 tumeurs), matrices RSEM Firehose téléchargées par la même route que PAAD (MD5 vérifiés : LUAD `4c36eec3…`, 47 043 687 octets ; COAD `e703a630…`, 26 401 036 octets). Ordre KRAS brut croissant, 12 mêmes gènes v4, 4 runs v6 fast (réel + nul, graine 42), tous exit 0. Tests directs top-12 + Spearman — le verdict principal.

**CA125 (MUC16) plat dans les deux cohortes :** LUAD rho +0,020 (p = 0,65), top-12 +0,26 sd ; COAD rho +0,019 (p = 0,75), top-12 +0,29 sd — au niveau du nul. Référence pancréas : +0,64 / +0,67 / +0,48. **CEA (CEACAM5) : lien monotone faible seulement, sans enrichissement des KRAS-forts** — LUAD rho +0,173 (p = 7,6e-05, Bonferroni) mais top-12 +0,17 sd = niveau du nul (+0,18), Welch p = 0,57 ; COAD rho +0,176 (p = 0,0028) mais top-12 −0,04 sd, Welch p = 0,92 (gène saturé, médiane +16,43). Critère gelé non atteint dans les deux cohortes.

**Programme propre au côlon :** 7/12 gènes p < 0,05, 5 après Bonferroni : MUC2 rho +0,302 (p = 2,1e-07), REG4 +0,250, CLCA1 +0,242, KRT20 +0,218, CEACAM5 +0,176. MUC16 n'en fait pas partie (à peine exprimée, médiane +0,81). LUAD : 3/12 p < 0,05, 1 après Bonferroni (CEACAM5 seul). Nuls 0/12 dans les deux cohortes. **Instrument : le v6 ne sépare pas réel et nul ici non plus** (Delta LUAD 2,511 contre 2,497 ; COAD 4,619 contre 4,599 ; cascades complètes dans les nuls) — les verdicts viennent des tests directs, comme le veut la règle. L7b FRAGILE partout, non-informatif. **Ce que ça change :** rien n'affaiblit les pistes pancréatiques ; la combinaison vopimetostat cible un sous-groupe distinct — elle complète l'axe, elle ne s'y substitue pas. Fichiers : `PROTOCOL_pancancer.md`, `pancancer.md`, `PROVENANCE_pancancer.md`, `build_fluxes_pancancer.py`, `pancancer_direct_tests.py`, `pdac_luad_fluxes.csv`, `pdac_coad_fluxes.csv`, `pancancer_direct_tests.csv`, `data/tcga_luad_rsem.tar.gz`, `data/tcga_coad_rsem.tar.gz`, `results_fast_pancancer_*` (4 dossiers), `runs_pancancer_v6.log`.

**Rapport combiné des deux bras :** `mtap_pancancer.md`, `PROVENANCE_mtap_pancancer.md`.

### 8.28 Dépendance PRMT5 contre statut MTAP mesuré — OUI, plus forte en pancréas (16 nov. 2026, 15h00–15h13)

**Verdict : oui, les lignées MTAP-délétées dépendent plus de PRMT5 — et l'effet est plus fort en pancréas qu'ailleurs. C'est un appui mesuré au rationnel de la combinaison vopimetostat + daraxonrasib — une fenêtre thérapeutique réelle, pas une dépendance absolue (PRMT5 reste essentiel même intactes, médiane −1,010), et ce test porte sur la dépendance PRMT5 seule, pas sur la combinaison.**

**Statut MTAP mesuré :** `OmicsCNGene.csv` (DepMap 24Q4, figshare 27993248) téléchargé — 1 394 554 236 octets, **MD5 exact `4696565fa74dc805983bc278b4a41802`**, SHA-256 `4851d3e939d4…`, 1 929 modèles. Taux de délétion mesurés : pancréas 20/47 (42,6 %) profondes, 38/47 (80,9 %) sous-diploïdes ; pan-cancer 294/1 178 (25,0 %). **Vérification interne passée :** Spearman PRMT5–KRAS sur les 47 pancréas = **−0,189 exactement**, identique au balayage génome entier.

**Test principal (lignées pancréas, 47) :** Chronos PRMT5 médian **−1,385** chez les 20 MTAP-délétées (CN < 0,5) contre **−1,010** chez les 27 intactes, différence −0,375, Mann-Whitney **p = 0,0036** ; en continu, Spearman PRMT5–CN MTAP **+0,497 (p = 0,0004, n = 47)**. **Pan-cancer :** même direction, effet plus petit (−1,092 contre −0,977, diff −0,114, p = 1,7×10⁻¹⁴, n = 294 contre 884 ; Spearman +0,165, p = 1,3×10⁻⁸, n = 1 178). **Contrôles propres :** KRAS et ACTB plats en Spearman (+0,009 et +0,019, p = 0,77 et 0,51) ; CDKN2A se comporte comme le contrôle de locus attendu. **Sensibilité :** au seuil large (CN < 1), PRMT5 reste significatif en pancréas (p = 0,030) mais plus faible ; ACTB sort à p = 0,041 à ce seuil avec seulement 9 intactes — probable bruit, noté comme tel ; au seuil principal ACTB est propre (p = 0,74).

**Spécificité 9p21 (limite honnête) :** CN MTAP contre CN CDKN2A, pancréas : Spearman +0,808 (p = 6,4×10⁻¹²) — les deux gènes sont presque toujours perdus ensemble, et le signal PRMT5 suit le CN CDKN2A (+0,528) comme le CN MTAP (+0,497). Ce test seul ne sépare donc pas « effet MTAP » de « effet délétion 9p21 entière » ; la spécificité MTAP vient de la littérature (MTA inhibant partiellement PRMT5 : Mavrakis et al., *Science* 2016 ; Kryukov et al., *Science* 2016).

**Deux bugs trouvés et corrigés en cours de route (traçabilité) :** (1) **Échelle CN** — la v1 supposait log2 (seuils < −1 et < 0) → zéro lignée classée délétée. En réalité `OmicsCNGene.csv` est en CN relatif **linéaire** depuis 24Q2 (1,0 = diploïde ; médiane globale 1,012, aucune valeur négative, MTAP 12,8 % < 0,01). Seuils corrigés : profond CN < 0,5, sensibilité CN < 1. (2) **Étiquettes de colonnes** — la v1 renommait les colonnes Chronos par position ; le fichier les trie alphabétiquement — PRMT5 et ACTB étaient échangés (contrôle de cohérence raté : +0,060 au lieu de −0,189). Corrigé : renommage par le nom. Après correction, le contrôle passe exactement. Fichiers : `prmt5_mtap_dependency.md`, `PROVENANCE_prmt5_mtap.md`, `prmt5_mtap_dependency.py` (exit 0, 31 s), `data/prmt5_mtap_results.csv` (25 lignes, SHA `e7c90e9a847c…`), `data/prmt5_mtap_pancreas_lines.csv` (47 lignées, SHA `348ccfa975ed…`), `data/OmicsCNGene.csv` (1,4 Go, MD5 vérifié exact).

### 8.29 Séparation MTAP vs délétion 9p21 entière — OUI, l'effet PRMT5 suit MTAP (16 nov. 2026, 15h50)

**Verdict : oui — l'effet PRMT5 suit MTAP, pas la délétion 9p21 entière. La limite honnête du §8.28 est levée : MTAP et CDKN2A sont presque toujours perdus ensemble, mais les lignées CDKN2A-délétées sans perte profonde de MTAP existent (137 sur 1 178 modèles) — et elles ne dépendent pas plus de PRMT5 que les lignées intactes. La dépendance PRMT5 supplémentaire n'apparaît que quand MTAP est perdu aussi. C'est un appui mesuré de plus au rationnel de la combinaison vopimetostat + daraxonrasib — une fenêtre thérapeutique réelle, pas une dépendance absolue, et ce test porte sur la dépendance PRMT5 seule, pas sur la combinaison.**

**Test principal (pan-cancer, 1 178 modèles, CN < 0,5 = délétion profonde) :** Chronos PRMT5 médian **−1,098** chez les 293 lignées MTAP + CDKN2A délétées ensemble, **−1,013** chez les 137 CDKN2A seules, **−0,973** chez les 747 ni l'un ni l'autre, −0,989 pour la seule lignée MTAP seule (n = 1). Both-del contre CDKN2A-seul : Mann-Whitney **p = 1,5×10⁻⁵** (hors pancréas : p = 6,5×10⁻⁵, n = 273 contre 130) ; CDKN2A-seul contre ni l'un ni l'autre : **p = 0,26** (hors pancréas : p = 0,34) — pas de différence ; both-del contre ni l'un ni l'autre : p = 1,3×10⁻¹⁴. **En continu, dans les 430 CDKN2A-délétées :** Spearman PRMT5 ~ CN MTAP **+0,244 (p = 2,9×10⁻⁷)**, contre PRMT5 ~ CN CDKN2A +0,122 (p = 0,011) — le CN MTAP suit la dépendance deux fois plus fort que le CN CDKN2A. **Contrôles propres :** KRAS et ACTB plats entre les groupes.

**Pancréas seul (même direction, petit n) :** both-del n = 20, PRMT5 **−1,385** ; CDKN2A-seul n = 7, **−1,049** ; ni l'un ni l'autre n = 20, **−0,984**. Both-del contre CDKN2A-seul : p = 0,081 ; CDKN2A-seul contre ni l'un ni l'autre : p = 0,46. **MTAP seul délété : n = 1 au pan-cancer, 0 en pancréas — la perte de MTAP sans perte de CDKN2A n'existe quasiment pas. La séparation ne pouvait se faire que dans ce sens-là (CDKN2A seul), et elle est faite.**

**Limite restante :** PRMT5 reste essentiel même sans délétion (médiane −0,973 chez les intactes) — fenêtre thérapeutique, pas dépendance absolue. Ce test porte sur la dépendance PRMT5 seule, pas sur la combinaison vopimetostat + daraxonrasib (toujours phase 1/2 non randomisée, n = 22, pas de survie globale).

**Honnêteté d'instrument :** test direct sur les données DepMap, comme le §8.28 — **pas un run v6**. Le pipeline n'a pas été lancé sur cette question.

**Fichiers :** `prmt5_mtap_9p21_separation.md`, `prmt5_mtap_9p21_separation.py` (exit 0, 23,4 s ; lecture par blocs, mêmes sources et seuils que `prmt5_mtap_dependency.py`), `prmt5_mtap_9p21_separation.log`, `data/prmt5_mtap_pancancer_lines.csv` (SHA `1085cbb14d21bec4358947b5d35d76c51352294a09b2e46b423612891cec2c03`). Sources : `OmicsCNGene.csv` (DepMap 24Q4, MD5 vérifié `4696565fa74dc805983bc278b4a41802`) et `CRISPRGeneEffect.csv`, déjà sur disque. Protocole : CN relatif linéaire (1,0 = diploïde), délétion profonde CN < 0,5 ; aucune imputation, paires complètes seulement.

### 8.30 Pipeline v6.1 — construction, validation, bras CRISPR DepMap (16 nov. 2026, 18h05–18h23)

**Ordre de Zackary :** « Continue mais concentre-toi plus sur mon pipeline, ne le mets pas de côté, l'améliorer si possible » (17h45), go confirmé « Allez-y, faites vos possibles pour trouver quelque chose avec mon pipeline sur le cancer du pancréas » (17h58), priorité confirmée « Teste mon pipeline » (18h13). **Adoption de v6.1 comme version de travail : go de Zackary le 16 nov. 2026, 18h34.**

**Deux défauts mesurés en v6, corrigés sur copie (conception gelée avant code : `PROTOCOL_v6.1.md`) :**
- **(a) L7a dégénère sous n = 75.** Le diagnostic de bruit coupe en 5 bins et exige ≥ 15 points par bin → Hurst échoue → score NaN → `top_csd = float(csd[0][1])` sans protection → risque NaN → vote L7a NaN → `max()` retourne « up » par accident, confiance repliée à 0,50. Le « up » des petits runs v6 (GSE62452, ICGC, CPTAC) est un **faux vote**. Correctif : gardes `_sf(..., 0.0)` sur `top_csd`, sur les 4 poids de vote L7a et l'incrément magnitude, `_sf(..., 0.50)` sur le `csd` du Monte-Carlo — quand tous les poids sont non finis, le retour `indeterminate` existant se déclenche, jamais « up » par accident.
- **(b) Séries courtes bloquées.** Fast mode min_len 50 → 50 points minimum. Le bras CRISPR DepMap (45 lignées adéno) échouait en 4 s. Correctif : min_len fast **50 → 40** (cible 45 lignées, marge 5 ; 40 = seuil déjà utilisé comme bascule par Higuchi ; scan bloque `w_size` à `n//2` = 22 à n = 45 → 24 fenêtres ; autres modes inchangés).
- **(c) Discrimination faible : étude seulement, aucun changement de code** — protocole gelé `PROTOCOL_phase2_discrimination.md` (voir fin de section).

**Construction :** copie `universal_v6.1.0_cohen.py`, VERSION_MASTER `v6.1.0-L7aL7b-CohenD-short`, SHA-256 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` (623 495 octets), construite par `build_v6.1.py` (10 remplacements exacts avec assertions) ; parent v6 SHA `bb8bbdba…c0773` revérifié inchangé ; compile OK. **Ne changent pas :** estimateurs, autres modes, cascade, seuils, Cohen-d. Provenance complète : `PROVENANCE_v6.1.md`.

**Validation — 10 runs fast, tous exit 0** (lanceur `run_v6.1_validation.sh`, log `runs_v61_validation.log`, extracteur `extract_v61_validation.py`, sorties `results_fast_v61_*` ; fin du lot 23:20:09 UTC) :

| Série | Cascade v6.1 (T_-2/T_-1/T_0/T_+1/T_+2 %) | v6 | L7a v6.1 | L7a v6 | Delta | MC opt / best |
|---|---|---|---|---|---|---|
| HP35 réel (n=1000) | 0,00 / 1,55 / 9,08 / 37,78 / 37,78 | **identique** (0/16/90/376) | up 0,382 | up 0,377 | 4,48 | 6,62 / 0,6035 |
| HP35 nul | 0,00 / 20,60 / 27,41 / 73,70 / 73,70 | **identique** | up 0,338 | up 0,337 | 4,57 | 4,91 / 0,4086 |
| TCGA v4 réel (n=178) | 0,00 / 74,06 / 93,22 / 98,44 / 98,96 | **identique** | **DOWN 0,405** (down 0,858) | DOWN 0,408 (0,863) | 4,18 | 10,87 / 0,3720 |
| TCGA v4 nul | 0,00 / 10,65 / 15,96 / 67,12 / 67,12 | **identique** | up 0,167 | up 0,167 | 3,77 | 81,52 / 0,3268 |
| GSE62452 réel (n=69) | 1,42 / 35,67 / 95,64 / 98,64 / 100,00 | identique | **down 0,197** (probs finies) | up 0,500 **NaN** | 1,41 | 18,18 / 0,3454 |
| GSE62452 nul | 0,00 / 12,82 / 17,10 / 21,37 / 21,37 | — | down 0,336 | — | 1,26 | 51,35 / 0,3485 |
| ICGC réel (n=70) | 1,41 / 9,84 / 52,31 / 94,27 / 94,27 | identique | up 0,181 (probs finies) | up 0,500 **NaN** | 1,44 | 70,59 / 0,3600 |
| ICGC nul | 0,00 / 28,12 / 32,43 / 36,54 / 49,10 | — | down 0,350 | — | 1,37 | 79,41 / 0,3450 |
| **DepMap réel (n=45)** | 0,00 / 1,40 / 4,40 / 11,01 / 26,42 | **jamais tourné en v6 (bloqué)** | down 0,196 | — | 1,93 | 57,14 / 0,3615 |
| **DepMap nul** | 0,00 / 13,21 / 17,61 / 26,42 / 26,42 | — | up 0,345 | — | 1,69 | 60,87 / 0,3499 |

**Critères d'acceptation (écrits avant les runs) : tous tenus.** HP35 réel/nul et TCGA v4 réel/nul : cascades identiques à v6. Falsification TCGA v4 v6.1 : delta_vs_null 0,849386, status ok — identique à v6. GSE62452 et ICGC : plus de faux « up » / 0,50 — les votes sont désormais finis et honnêtes (confiances 0,18–0,35, faibles). DepMap réel + nul : exit 0 — le bras CRISPR tourne pour la première fois.

**Bras CRISPR DepMap — première lecture par le pipeline.** Flux `pdac_depmap_fluxes.csv` (SHA `7d605fef…`), 45 lignées adéno, 12 gènes (top 12 par Chronos médian pancréas vs autres, hors KRAS : EFR3A, RAB10, CCND1, UROD, CFLAR, DOCK5, MYH9, SCAP, RAB6A, CRKL, MYC, ACO2), ordre = Chronos KRAS croissant (KRAS = axe, jamais un flux) ; nul SHA `ac2e0db5…` (lignes permutées, graine 42). Sources : DepMap CRISPR 24Q4 (figshare 27993248), `CRISPRGeneEffect.csv` SHA `3d8f3ec6…`, `Model.csv` SHA `b7a0c138…`.
- **Cascade réelle :** 0,00 / 1,40 / 4,40 / 11,01 / 26,42 % → pas 0 / 1 / 2 / 5 / 12. **Cascade nulle :** 0,00 / 13,21 / 17,61 / 26,42 / 26,42 % → pas 0 / 6 / 8 / 12 / 12.
- **Lecture par flux** (`per_flux_reading.py`, z-score global, fenêtres ±10, d de Cohen ; méthode propre à ce script, ne pas comparer chiffre à chiffre aux lectures du 15 nov.) : pas 2 (T_0) — fenêtre avant = 2 points seulement, EFR3A z −1,91, CCND1 −1,56, UROD −1,31 (les 2 lignées les plus KRAS-dépendantes ont des Chronos très négatifs pour ces gènes — fragile, n = 2 avant) ; pas 5 — RAB10 d +1,12, DOCK5 +1,13, SCAP −1,70, CFLAR −1,04 ; pas 12 — SCAP −1,77, le reste |d| ≤ 0,61 ; top-12 (premières lignes = plus dépendantes) contre reste — DOCK5 −1,03, SCAP +0,88, CFLAR −0,74, CRKL −0,67, CCND1 −0,56 : effets modérés, signes mêlés, aucun gène dominant.
- **Verdict honnête : le pipeline ne sépare PAS DepMap réel et nul.** Les deux cascades tombent tôt dans la série (T_+2 à 26,42 % dans les deux) ; MC best_score 0,3615 contre 0,3499 (quasi identiques) ; Delta 1,93 contre 1,69 ; max_separation 0,4436 contre 0,2532 ; L7a down 0,196 contre up 0,345 (deux votes faibles). Le T_0 réel (pas 2) est plus tôt que le nul (pas 8), mais avec une fenêtre avant de 2 points, ce n'est pas une preuve — c'est l'effet de 1–2 lignées extrêmes. Cohérent avec le test direct du 15 nov. : dépendances CRISPR des 12 gènes |rho| ≤ 0,23 — marqueurs, pas vulnérabilités.
- **Limite :** la falsification est **indisponible** à n = 45 (« comparaison impossible sans les deux dimensions » — la dimension spectrale vient du diagnostic de bruit, dégénéré sous n = 75, 0/12 complet). Le test qui séparait TCGA v4 (delta 0,849) n'existe pas sur les séries courtes. L4 risque = 0,000 (repli gardé, honnête).

**Découverte d'instrument — gigue L5 (à consigner, pas un défaut v6.1).** Les alertes L5 sont non déterministes d'un run à l'autre **par construction** : `level_complexity` graine les chemins MC avec `int(seed) + (hash(metric) % 1000)` et le hachage Python des chaînes est aléatoire par processus (vérifié : `hash('PersistentHomology') % 1000` = 14 puis 133 dans deux processus). Sur HP35, l'alerte PersistentHomology (0,559 en v6) disparaît en v6.1 → L4 risque 0,84 → 0,91, L7a conf 0,377 → 0,382. La cascade et Delta sont déterministes ; L4/L7a portent une gigue de l'ordre de ±0,07 sur HP35 (v5.9.0f → v6 montrait déjà une gigue de mean_alert 0,7687 contre 0,7783 avec le même code L5). **Piste future v6.2 (hors scope v6.1, à proposer seulement) :** remplacer `hash(metric)` par un hachage stable (ex. `hashlib.sha256`).

**Lots v6.1 TERMINÉS le 18 nov. 2026 (140/140, vérifié par comptage des `master_results.json`) :** lot étendu 44/44 (§8.31) et rotations 96/96 (§8.32) ; surveillance arrêtée d'elle-même à 140/140. Lanceur reprenable `run_v61_lot.sh` (lancé 16 nov. 18h23, plusieurs redémarrages de la machine, relances par la surveillance toutes les 15 min, 0 échec non récupéré). Audit des flux au §8.33.

**Phase 2 — étude de discrimination réel / nul (protocole gelé, pas de code).** Protocole `PROTOCOL_phase2_discrimination.md` : sur les paires réel/nul connues (HP35, TCGA v4, GSE71729, GSE62452, ICGC, immunitaire, PARP, DepMap + lots), tester 8 indicateurs dérivés (Delta, MC optimum, MC best_score, max_separation, position de T_0, delta de falsification, cohérence par flux à T_0, L7a). Critère de succès écrit d'avance : un indicateur sépare s'il dépasse la gigue run-to-run connue ET si la direction de l'écart est cohérente sur ≥ 6 des 8 paires principales ; sinon le verdict est « sépare sur X/8 paires » avec les chiffres — et si aucun indicateur ne tient, « le pipeline, en l'état, ne sépare pas réel et nul sur ces séries PDAC ». **Exécution et tout changement de code attendent le go de Zackary après la phase 1.**

### 8.31 Lot étendu v6.1 — 43/44 runs, comparaison v6.1/v6 et lecture flux par flux des 3 pistes (17 nov. 2026)

**Verdict d'abord.** La v6.1 reproduit la v6 à l'identique sur toutes les séries comparables (cascades identiques sur **41/41**). Elle corrige le faux vote L7a sur les 5 petites cohortes. **Dans l'ensemble, le pipeline ne sépare pas le réel du nul** : ni le score MC, ni Delta, ni la falsification. Les 3 plus grands écarts réel/nul ont été lus flux par flux. Aucun ne tient comme preuve d'une structure du cancer captée par le pipeline : **pureté = artefact du score composite** ; **CLDN18 = en partie un artefact de construction (le contrôle est aussi un flux), en partie une vraie co-expression** ; **immunitaire = un nul anormalement bas**, et le réel montre une baisse cohérente des gènes cytotoxiques vers le haut de l'axe KRAS, déjà connue par test direct (§8.23).

**Le lot.** Le manifeste `manifest_v61_extended.txt` (SHA `c74eb09f…e5eb`) compte 22 séries × (réel + nul), soit 44 runs. Pipeline : `universal_v6.1.0_cohen.py`, SHA `2af5e5ce…c1c9`, revérifié inchangé le 17 nov. Mode fast ; nuls à graine 42. Le lot a fini le 17 nov. vers 14h45 avec **43/44**. **Le côlon réel (COAD) est perdu** : une relance manuelle et une relance automatique sont entrées en collision, et son dossier a été effacé pendant le run (`FileNotFoundError` sur `results_fast_v61_coad/landscape_complexity.png`). **Il sera refait à la fin des rotations.** Le nul du côlon est présent. Le run GEO71729_PARP avait échoué de la même façon ; il a été refait avec succès.

**Extracteur corrigé (copie, original intact).** L'original `extract_v61_lot_compare.py` (SHA `d4f52af7…9efb`) lisait des clés absentes du JSON. La copie `extract_v61_lot_compare_v2.py` (SHA `4cb9b14d…15bb`) lit les bonnes clés :
- `prediction_levels.L7a_coherence` ;
- `reading_synthesis.Delta_tension` ;
- `run_pipeline.threshold_metadata.threshold_optimization.best_config` (seuil, score, max_separation) ;
- `five_threshold_cascade` T_-2…T_+2 ;
- `holographic_tension_state.falsification_vs_null.delta_vs_null`.

Elle retrouve l'équivalent v6 **par le CSV d'entrée** (`metadata.csv_path`), pas par le nom de dossier. Sorties : `v61_extended_compare.csv` (SHA `a97a387b…d729`) et `v61_extended_compare.md` (SHA `31cbd345…84cc`). **Attention :** la « falsification » compare la dimension critique géométrique à la dimension spectrale (seuil 0,5). Ce n'est **pas** une comparaison au nul permuté, malgré le nom de la clé.

**Recoupement avec `v61_extended_verified.md` : toutes les valeurs concordent** (cascades, L7a, Delta, MC, max_separation, falsification). Deux écarts de décompte sont corrigés ici :
- (a) **41** runs ont un équivalent v6, et non 33. Les 8 en plus (PARP_TCGA ±nul, ATR_TCGA ±nul, LUAD ±nul, COAD_NUL) avaient échappé à l'ancien appariement par nom de dossier ; ils sont tous identiques à v6. Seuls GEO71729_PARP et son nul n'ont pas de run v6.
- (b) La falsification dépasse 0,5 sur **16/21 réels contre 15/21 nuls** (et non 16/21 contre 16/21). Conclusion inchangée : elle ne sépare pas.

**L7a corrigé sur les 5 petites cohortes (n ≤ 70) — v6.1 contre v6.** En v6, tous ces votes valaient « up 0,500 », un faux vote causé par un NaN (§8.14, §8.30).

| Série | L7a v6.1 réel | L7a v6 réel | L7a v6.1 nul |
|---|---|---|---|
| CPTAC_UMICH | down 0,148 | up 0,500 (NaN) | down 0,359 (v6 : up 0,500) |
| CPTAC_BCM | down 0,152 | up 0,500 (NaN) | up 0,323 |
| GEO62452_V4B | down 0,206 | up 0,500 (NaN) | up 0,164 |
| IMMUNE_GEO62452 | flat 0,280 | up 0,500 (NaN) | up 0,282 |
| IMMUNE_ICGC | up 0,358 | up 0,500 (NaN) | up 0,325 |

Les grandes cohortes ne changent pas (ex. TCGA_V1 down 0,195 / 0,195 ; GEO71729 up 0,415 / 0,416). GEO71729_NUL passe de up 0,402 à up 0,354, dans la gigue L5 connue (±0,07, §8.30). Les votes des petites cohortes sont désormais finis, mais faibles (0,15–0,36) : ce sont des votes honnêtes, pas des signaux.

**Réel contre nul (21 paires complètes) — pas de séparation d'ensemble.**
- Écart de score MC le plus souvent ≤ 0,05. Les plus grands écarts : V4R_PURITY +0,152 (0,4841 contre 0,3321) et V4R_CLDN18 +0,119 (0,4504 contre 0,3312). Le nul dépasse le réel sur 4 paires : GEO71729_V4C −0,164, IMMUNE_ICGC −0,034, LUAD −0,020, CPTAC_BCM −0,017.
- Delta : le plus grand écart est IMMUNE_TCGA, +1,91 (4,21 contre 2,30). Le nul dépasse le réel sur TCGA_V1 (−0,62), TCGA_V2 (−0,56) et PURITY (−0,67).
- La falsification reste sous 0,3 sur toutes les petites cohortes, réel et nul confondus.

**Lecture flux par flux des 3 pistes (réel ET nul).** Script de lecture `pistes_v61_flux_reading.py` (SHA `0009b46f…b899`), sortie `pistes_v61_flux_reading.md` (SHA `cb1a5ab7…f6c`). Lecture seule, aucun run.

Ce qui vient **du pipeline** :
- la cascade et le seuil MC, avec les composantes du score ;
- F1/F2 avant et après le seuil (`transition_analysis.json`, colonne « Tous », 29 estimateurs) ;
- le test de bruit (`noise_diagnostic.json`).

Ce qui est **apporté par le harnais** :
- les flux qui bougent à chaque seuil (z global, fenêtres ±20, d de Cohen, même méthode que `per_flux_reading.py`, SHA `896b096c…a2d28`) ;
- l'ordre de réaction des estimateurs, lu sur `df_feat.csv` : position du max |F1| de la trajectoire médiane de chaque estimateur, bords du scan (< 10 % et > 90 %) exclus. Ce n'est pas une sortie native du pipeline.

CSV : pureté `41e11870…35fb` / nul `5382bbed…0731` ; CLDN18 `ef90c6de…70be` / nul `e7ddfce1…e29e27` ; immunitaire `66dbb672…bd2e` / nul `9100d181…a405`. Aucune exigence de consensus entre flux. Un nul produit aussi des seuils, et il en produit ici.

*(1) V4R_PURITY — contrôle négatif — l'écart vient du score, pas des données.*
- **Composition du score MC.** Le score composite vaut 0,3·s_norm + 0,3·stabilité + 0,2·robustesse + 0,2·acuité (code v6.1, `evaluate_scan_quality`). La « robustesse » récompense un pic de scan d'environ 10 % de largeur (gaussienne autour de 10 %, écart-type 5). Réel : 0,3×0,072 + 0,3×0,991 + 0,2×**0,808** + 0,2×0,017 = 0,484. Nul : 0,3×0,105 + 0,3×0,999 + 0,2×**0,000** + 0,2×0,005 = 0,332. **Tout l'écart (+0,16) vient de la largeur du pic.** La séparation est même **plus faible** dans le réel (max_separation 0,144 contre 0,211). Dans les 10 autres runs examinés, la robustesse vaut ≈ 0.
- **Flux à chaque seuil (réel).**
  - Cascade 3,19 / 24,57 / 42,52 / 59,37 / 59,37 %, soit les pas 6 / 43 / 75 / 105.
  - T_-2 : CLDN18 −0,59 (fenêtre avant de 6 points seulement).
  - T_-1 : PGC +0,62.
  - T_0, T_+1 et seuil MC (pas 146) : aucun flux à |d| ≥ 0,5 (max 0,49).
- **Flux à chaque seuil (nul).**
  - Cascade 0 / 59,37 / 81,51 / 94,26 %.
  - T_-1 : KRT20 −0,95.
  - T_0 : CEACAM5 +0,56.
  - T_+1 : MUC17 −0,80.
  - Seuil MC : KRT20 −0,85, MUC17 −0,62.
  - **Le nul fait bouger plus de flux que le réel.**
- **Test de bruit** : MEDIUM « Mixte » des deux côtés (score moyen 0,570 contre 0,588).
- **F1/F2 (« Tous »)** : réel |F1| ×7,97, |F2| ×23,8 après le seuil ; nul ×2,64 et ×2,06. Changement de signe de F1 : 25/29 contre 24/29.
- **Ordre de réaction** : médiane des positions 24,8 % dans le réel contre 63,9 % dans le nul.
- **Verdict : artefact de construction du score** (le terme robustesse), sans gain de séparation. Le contrôle négatif reste négatif. Le résiduel acineux est bien décorrélé des flux (|rho| ≤ 0,117 dans le réel).

*(2) V4R_CLDN18 — n'avait pas séparé en v6 — artefact partiel + vraie co-expression.*
- **Artefact trouvé.** L'en-tête de `pdac_tcga_fluxes_v4r_cldn18.csv` est `CLDN18,PGC,REG4,CLDN18,…` : CLDN18 est **à la fois le contrôle et un flux** (lu `CLDN18.1`). Dans le réel, Spearman contrôle ~ CLDN18.1 = **1,000** ; dans le nul (flux permutés), 0,003.
- **Composition du score MC.** L'écart vient de la séparation : s_norm 0,491 contre 0,102 (max_separation 1,076 contre 0,205). La robustesse vaut 0 des deux côtés.
- **Flux à chaque seuil (réel).**
  - Cascade 4,26 / 46,59 / 84,42 / 91,14 %, soit les pas 8 / 82 / 149 / 161. Seuil MC : 10,87 %, pas 19.
  - **CLDN18.1 domine chaque seuil** : d +2,42 / +3,08 / +3,15 / +3,08, et +2,96 au seuil MC. C'est le contrôle qui se voit lui-même.
  - D'autres flux bougent aussi au seuil MC : DPCR1 +1,52, CEACAM5 +1,25, PGC +1,02, MUC17 +0,79, GSTM1 +0,75, MUC16 +0,67.
  - Au T_0 : DPCR1 +0,86, PGC +0,85 contre MUC2 −0,82, REG4 −0,65, CLCA1 −0,60, KRT20 −0,57.
  - Co-expression sous l'ordre CLDN18 : PGC +0,612, REG4 +0,625, MUC17 +0,667, DPCR1 +0,587, CEACAM5 +0,551. Dans le nul, tous les |rho| ≤ 0,14.
- **Flux à chaque seuil (nul).**
  - Cascade 1,06 / 34,29 / 60,38 / 97,39 %.
  - T_-2 : CR2 −2,35, CLCA1 −1,77 (fenêtre avant de 2 points, fragile).
  - T_0 : KRT20 +0,66, CEACAM5 +0,63.
  - Seuil MC : MUC17 +0,73.
- **Test de bruit** : réel MEDIUM_HIGH « Proxy de variance modéré » (moyenne 0,723 ; MUC17 1,0, PGC 0,983) contre nul MEDIUM « Mixte » (0,536).
- **F1/F2** : réel |F1| ×0,02 et |F2| ×0,01 après le seuil (tout se passe avant les 10 % : rupture précoce puis plateau) ; nul ×4,13 et ×5,40. Changement de signe : 26/29 contre 27/29.
- **Ordre de réaction** : médiane 26,9 % des deux côtés. **Pas de différence d'ordre.**
- **Verdict : mixte.** Une part de l'écart est **triviale** : un flux identique au contrôle. Une autre part est **réelle** : un groupe de gènes gastriques et mucineux (PGC, REG4, MUC17, DPCR1, CEACAM5) co-varie avec CLDN18 dans les tumeurs, et pas dans le nul. Le test propre serait une rotation CLDN18 **sans le doublon**. C'est **proposé seulement** : aucun CSV modifié, aucun run lancé.

*(3) IMMUNE_TCGA — axe KRAS (contrôle `step`) — l'écart Delta vient surtout du nul.*
- **Delta.** Réel 4,21 (d_div 5,784 − d_sat 1,574), régime divergence ; nul 2,30 (d_div 3,904 − d_sat 1,608), régime **criticité**. Les autres nuls TCGA du lot ont un Delta de 3,77–4,30, et les réels TCGA de 3,68–4,30. **Le réel est typique ; c'est le nul qui est anormalement bas.**
- **Flux à chaque seuil (réel).**
  - Cascade 1,60 / 29,15 / 59,91 / 75,10 %, soit les pas 3 / 52 / 106 / 133. Seuil MC : 79,35 %, pas 140.
  - T_-2 : CD274 +1,15 (fenêtre de 3 points, fragile).
  - T_-1 et T_0 : aucun flux à |d| ≥ 0,5.
  - **T_+1 : baisse groupée** — CD19 −0,88, FOXP3 −0,79, CD8A −0,74, CD4 −0,58, GZMB −0,55, CTLA4 −0,53, IFNG −0,51.
  - **Seuil MC (pas 140, les 20 % de tumeurs les plus KRAS) : chute nette des gènes de lymphocytes tueurs** — GZMB −1,65, IFNG −1,25, CD8A −1,08, CD8B −1,01, FOXP3 −1,00, CTLA4 −0,93, CD19 −0,83, PDCD1 −0,83, CD163 −0,76.
- **Flux à chaque seuil (nul).**
  - Seuils très précoces : 0 / 2,13 / 8,52 / 35,34 %, soit les pas 0 / 4 / 15 / 63.
  - T_-1 et T_0 : FOXP3 +1,00 / +1,02, CD8A +0,74 / +0,99, CD4, CD163… sur des fenêtres avant de 4 et 15 points.
  - T_+1 et seuil MC : aucun flux à |d| ≥ 0,5.
- **Test de bruit** : réel MEDIUM_HIGH (moyenne 0,718 ; IFNG 0,862, CD274 0,807) contre nul MEDIUM « Mixte » (0,529).
- **F1/F2** : réel |F1| ×11,5 et |F2| ×18,7 après le seuil ; nul ×0,05 et ×0,03 (tout se passe au début). Changement de signe : 23/29 contre 24/29.
- **Ordre de réaction** : médiane 40,3 % dans le réel contre 12,2 % dans le nul.
- **Verdict.** L'écart Delta n'est **pas** une preuve que le pipeline sépare. Il vient d'un d_div nul anormalement bas et d'un nul qui place ses seuils au tout début, sur quelques points. Mais le réel montre une structure absente du nul : vers le haut de l'axe KRAS, les gènes cytotoxiques chutent ensemble (« tumeur froide »). C'est **concordant** avec le test direct du §8.23, et c'est une lecture de harnais sur des seuils du pipeline, pas un verdict du pipeline.

**Ce qui manque.**
- Le côlon réel (à refaire).
- La rotation CLDN18 sans doublon (terminée — voir (4) ci-dessous).
- Une mesure de la gigue run-to-run du terme robustesse : on ne sait pas encore si 0,808 se reproduit.
- L'ordre de réaction est une lecture de harnais avec un choix de méthode : max |F1| et bords exclus. La première lecture, sans exclusion des bords, plaçait presque tous les estimateurs aux bords du scan.
- Les 96 rotations sont en cours (§8.32 à venir).

*(4) Rotation CLDN18 sans doublon — le test propre, terminé le 17 nov. 2026 à 17h56 (heure de Montréal).*
- **Le test.** Go de Zackary à 17h17. Le script `build_v4r_cldn18_dedup.py` (SHA `30aba3b4…`) retire le flux CLDN18 en double du CSV ; le contrôle, l'ordre des lignes et les 11 autres flux sont inchangés (en-tête `CLDN18,PGC,REG4,MUC17,DPCR1,CR2,KRT20,MUC2,GSTM1,CEACAM5,CLCA1,MUC16`). CSV réel SHA `b1071f84…`, nul SHA `33d5f317…`. Lot de 2 runs v6.1 (`manifest_v61_cldn18_dedup.txt`, SHA `f832d749…`), journal `runs_v61_cldn18_dedup.log` (SHA `64760bed…`) : 2/2, exit 0, aucun Traceback. Pipeline inchangé (`2af5e5ce…c1c9`).
- **Verdict : NON, le réel ne se sépare toujours pas du nul.** Retirer le doublon n'a presque rien changé : la cascade du réel est **identique au centième** à celle avec doublon (4,26 / 46,59 / **84,42** / 91,14 / 91,14 %). Le score MC baisse à peine : réel 0,4257 contre nul 0,3313 (écart +0,094 ; avec doublon 0,4504 contre 0,3312, écart +0,119). Le nul n'a pas bougé du tout en MC (0,3313 contre 0,3312). L'écart vient de la séparation (max_separation 0,871 contre 0,188 ; s_norm 0,410 contre 0,094) ; la robustesse vaut ≈ 0 des deux côtés (3,4e-41 contre 3,5e-26).
- **Delta et L7a ne séparent pas.** Delta réel 3,862 contre nul 3,854 (écart 0,008 — avec doublon, 3,863 contre 3,797). L7a vote UP des deux côtés, presque à l'identique (réel up 0,852, confiance 0,415 ; nul up 0,847, confiance 0,402). Falsification au-dessus de 0,5 des deux côtés (0,8125 contre 0,7356) : elle ne sépare pas non plus. L7b FRAGILE des deux côtés (réel : horizon FAIL, T_0 très variable en walk-forward, t0_std 24,35 ; nul : walk-forward FAIL, t0_std 12,90).
- **Le groupe estomac/mucus bouge encore — mais il bouge aussi dans le nul.** Lecture flux par flux sur copie du script (`pistes_dedup.py`, SHA `247feb23…`, sortie `/tmp/pistes_dedup.md`, SHA `06e009ba…`), même méthode que ci-dessus. Réel sans doublon, aux seuils : T_-2 MUC17 +0,83, DPCR1 +0,67, PGC +0,64, CEACAM5 +0,61 ; T_0 DPCR1 +0,86, PGC +0,85, REG4 −0,65 ; T_+1 DPCR1 +0,88, PGC +0,60, MUC17 +0,54 ; seuil MC DPCR1 +1,52, CEACAM5 +1,25, PGC +1,02, MUC17 +0,79 — **les mêmes valeurs qu'avec le doublon, à CLDN18.1 près**. Le seul seuil où le doublon dominait, c'était T_-1 (CLDN18.1 +3,08 ; sans doublon : aucun flux à |d| ≥ 0,5, max CLCA1 −0,36). Dans le nul sans doublon, le même groupe bouge à T_0, en sens inverse : MUC17 −1,13, DPCR1 −0,81, REG4 −0,65, PGC −0,52. La co-expression du groupe est donc réelle (elle survit au retrait du doublon), mais **son mouvement ne distingue pas le réel du nul** : elle bouge des deux côtés, seule la direction diffère à T_0. Ce n'est pas une preuve.
- **Deux observations, pas des preuves.** (a) F1/F2 (« Tous », 29 estimateurs) : le réel chute après le seuil (médiane |F1| ×0,03 ; avec doublon ×0,02), le nul monte (×30,17 ; avec doublon ×4,13) — le sens s'inverse entre réel et nul, mais le changement de signe de F1 est de 25/29 des deux côtés. (b) Retirer le doublon a déplacé la cascade du nul (1,06 / 34,29 / 60,38 / 97,39 % → 0,53 / 49,11 / 77,87 / 81,51 %) alors que celle du réel n'a pas bougé d'un centième — le réel est insensible au doublon, le nul non. Test de bruit : réel MEDIUM_HIGH 0,720 (0,723 avec doublon), nul MEDIUM_HIGH 0,668 (MEDIUM 0,536 avec doublon).
- **Conclusion de la piste CLDN18.** Le doublon n'était pas ce qui faisait le résultat : sans lui, tout est pareil, sauf T_-1. La co-expression gastrique/mucineuse sous l'ordre CLDN18 est réelle, mais elle ne sépare pas le réel du nul. La piste est **fermée comme test de séparation** ; le groupe reste une co-expression à noter, pas une structure validée par le pipeline.

### 8.32 Rotations de contrôle systématiques v6.1 — 96/96 runs, aucun contrôle ne sépare réel et nul (18 nov. 2026)

**Verdict d'abord.** Les 96 rotations sont terminées (48 paires réel/nul, toutes exit 0, 0 échec) ; avec le lot étendu, le programme v6.1 est complet : **140/140 runs**. Aucun des 48 contrôles ne sépare le réel du nul proprement — ni le score MC, ni Delta, ni L7a, ni la falsification. Les plus grands écarts viennent d'un saut de niveau d'une ancre interne (Delta) ou d'une séparation gonflée par la construction (MC). **Mais trois blocs de co-expression réels sont confirmés par tests directs** (top-12 contre reste, réel bien au-dessus du bruit des nuls) : le bloc estomac/mucus (PGC, REG4, CLDN18, MUC17, DPCR1, CEACAM5), le bloc immunitaire (CD8A, CD8B, PDCD1, GZMB, IFNG…) et le bloc réparation (ATR, BRCA2, POLQ, CHEK1, RAD51). **La chaîne du 15 nov. — le bloc qui s'effondre pendant que MUC16 monte, au bout de l'axe KRAS — ne réapparaît sous aucun autre contrôle.** Ce qui réapparaît, c'est le bloc lui-même et son anti-corrélation avec MUC16, vus depuis l'autre côté : sous les contrôles du bloc, c'est le bloc qui est haut et MUC16 qui est bas. La lecture « rupture » reste propre à l'axe KRAS.

**Le lot.** Manifeste `manifest_v61_rotations.txt` (96 lignes) : 4 familles × 12 flux × (réel + nul). V4ROT (TCGA v4, ARN tumeurs, n=178), DEPMAPROT (CRISPR DepMap, lignées, n=45), IMMROT (immunitaire TCGA, ARN tumeurs, n=178), PARPROT (réparation de l'ADN TCGA, ARN tumeurs, n=178). Dans chaque rotation, un flux sert de colonne de contrôle à tour de rôle ; les lignes sont triées par ce flux croissant ; le nul est les mêmes lignes permutées (graine 42, un générateur par jeu, tirages séquentiels dans l'ordre des flux), colonne de contrôle intacte. Construction : `build_rotations_v61.py`, même méthode que `build_rotations.py` (15 nov.) ; provenance complète `PROVENANCE_rotations_v61.md` (100 SHA, un par fichier réel et nul). Pipeline `universal_v6.1.0_cohen.py`, SHA `2af5e5ce…c1c9`, revérifié inchangé ; mode fast ; journal `runs_v61_rotations.log` (FIN 2026-11-18T15:43:15Z, déjà_faits=80, terminés=16, échecs=0 sur la dernière reprise — le lot a survécu à plusieurs redémarrages de la machine, relancé par la surveillance toutes les 15 min). Lecture : extracteur `extract_v61_rotations_v3.py` (SHA `91b165b7…`), lecture flux par flux `rotations_flux_reading.py` (SHA `41937798…`) ; tables `v61_rotations_verified.md` (SHA `4ea56c4d…`), `v61_rotations_flux_reading.md` (SHA `a2d703c1…`), données `v61_rotations_extract.csv` (SHA `99b8a6d3…`) et `v61_rotations_flux_reading.json` (SHA `db04622e…`). Les nuls des rotations sont des tirages différents de ceux du lot étendu (même graine 42, ordre de tirage différent) : leurs valeurs MC/Delta diffèrent donc légèrement de celles du §8.31 pour la même série (ex. nul CLDN18 : MC 0,363 ici contre 0,331 au lot étendu).

**Défaut de construction systématique — à lire avant tout le reste.** Les 48 CSV de rotation ont 13 colonnes : **le contrôle figure aussi parmi les flux** (vérifié sur les 48 fichiers : chaque en-tête contient le nom du contrôle deux fois, ex. `CLDN18,PGC,REG4,CLDN18,…`). C'est le même défaut que pour CLDN18 au §8.31, généralisé à toutes les rotations. Conséquence mesurée : à T_0, dans le réel, le flux en double est le premier moteur partout, avec un d de Cohen de **+2,00 à +4,69 (48/48 runs)**. C'est mécanique : le flux en double EST l'axe de tri, il monte donc par construction d'un côté du seuil à l'autre. Dans les nuls, le même flux vaut |d| ≤ 0,96 presque partout (exceptions : MYH9 nul −2,58 et RAB6A nul −1,21, seuils à 2–3 points du bord, fenêtres tronquées — fragiles). **Il faut donc lire les mouvements des 11 autres flux, pas celui du doublon.** Le test propre du §8.31 (4) a montré que retirer le doublon ne change presque rien aux scores (cascade identique au centième, MC 0,450 → 0,426) : le doublon gonfle la lecture flux par flux, il ne fait pas les scores. Toutes les lectures ci-dessous excluent le doublon.

**Score MC — petit écart moyen, porté par la séparation, pas par la robustesse.** Écart réel−nul moyen : V4ROT +0,051 (max +0,107 MUC17, min −0,120 MUC16) ; DEPMAPROT +0,033 (tous positifs, +0,011 à +0,055) ; IMMROT +0,056 (max +0,146 CTLA4, +0,142 PDCD1, min −0,080 FOXP3) ; PARPROT +0,035 (max +0,096 BRCA1, min −0,117 ATM). Le nul dépasse le réel sur **9/48 paires**. Dans les plus grands écarts, c'est la séparation qui porte tout : CTLA4 réel max_separation 1,344 contre nul 0,214 (s_norm 0,586 contre 0,107) ; PDCD1 1,231 contre 0,147 ; CD8B 1,255 contre 0,227. La cible de l'optimisation MC est la 1re colonne après le contrôle — le doublon seulement quand le contrôle est le 1er flux de sa famille (PGC, CD8A, PARP1, EFR3A : 4 paires sur 48). La robustesse, elle, est au plancher (≈ 3,4e-41) sur 35/96 runs et vaut 0,69–1,00 sur 5 nuls (MUC16 0,831, ATM 0,849, PARP2 0,693, FOXP3 0,999, CD8A 0,999) : avec un poids de 0,2 dans le score composite, ce terme **fait passer ces 5 nuls au-dessus de leur réel** — même famille d'artefact que la pureté au §8.31. La stabilité est ~0,99 des deux côtés et ne sépare rien ; la netteté (sharpness) est petite partout (0,004–0,049).

**Delta — vérifié : c'est un saut de niveau, pas une séparation continue.** Sur les 96 runs, **Delta = d_div − d_sat, erreur max 0,0009** (vérifié sur les 96). d_sat est presque constant par famille (TCGA 1,53–1,61 ; DepMap 1,19–1,33) ; d_crit aussi (TCGA 3,10–3,42). Tout le mouvement vient de **d_div, qui prend des niveaux discrets** : DepMap ~3,0–3,15 des deux côtés (Delta ~1,7–1,95, aucune séparation) ; TCGA ~4,7, ~5,4 et ~5,8–5,9. V4ROT : réel 11/12 à 5,38–5,43, 1 à 4,67 (REG4) ; nul 11/12 à 5,37–5,43, 1 à 6,00 (CLDN18). IMMROT : réel 2 à ~4,7, 10 à 5,73–5,88 ; nul de 3,38 à 5,86. PARPROT : réel 3 à ~4,7, 9 à 5,68–5,90 ; nul 1 à 3,92, 3 à ~4,7, 8 à 5,63–5,90. Les plus grands écarts ΔDelta sont tous des différences de niveau : IFNG **+2,396** (réel 4,241, nul 1,845 — le nul est tombé au niveau 3,38), BRCA2 +1,143, PARP2 +1,077, CD68 +1,081, CD19 +1,059, ATM +0,995, ATR +0,781 ; et en négatif CD4 −1,125, XRCC1 −1,193, RAD51 −1,156, CD8B −0,723 (le réel est tombé au niveau 4,7 pendant que le nul restait à 5,8). **Les deux côtés visitent tous les niveaux** : le niveau n'est pas un marqueur du réel. Aucun seuil de séparation n'avait été pré-enregistré pour ces écarts : ce sont des pistes, pas des preuves. Ce que Delta mesure ici, c'est dans quel niveau l'instrument est tombé — le mécanisme qui choisit le niveau n'est pas élucidé (pas de corrélation avec T_0 : r = −0,04 ; ni avec MC : r = +0,25 ; ni avec L7a : r = −0,03).

**L7a, falsification, bruit, F1/F2 — rien ne sépare.** L7a : directions et confiances se recouvrent entièrement entre réel et nul dans les 4 familles (V4ROT réel 6 up/6 down, 0,17–0,42 ; nul 7 up/5 down, 0,19–0,42 ; DEPMAPROT 10 up/2 down des deux côtés ; IMMROT réel 12/12 up, 0,17–0,45, nul 9 up/3 down ; PARPROT réel 7 up/5 down, nul 8 up/2 flat/2 down). Falsification (delta_vs_null interne, d_crit contre SpectralDimension — **pas** une comparaison au nul permuté, cf. §8.31) : au-dessus de 0,5 presque partout, réel comme nul (V4ROT 12/12 des deux côtés, 0,61–0,83 réel contre 0,67–0,86 nul ; IMMROT 0,69–0,92 contre 0,67–1,14 ; PARPROT 0,63–0,96 contre 0,69–0,92). DEPMAPROT : falsification **indisponible** sur les 24 runs (n=45 < 75, « comparaison impossible sans les deux dimensions »). Test de bruit : réels presque tous MEDIUM_HIGH, nuls MEDIUM à MEDIUM_HIGH — pas de séparation ; DEPMAPROT : verdict indisponible (n=45, score moyen None, « Scores proxy complets indisponibles »). F1/F2 (transition_analysis « Tous ») : les rapports après/avant vont de 0,01 à 39 dans le réel comme dans le nul, dans les deux sens — aucune direction cohérente. Corrélation score CSD ↔ F1 : r = +0,179 (n=72) — faible, notée comme information, pas comme signal.

**La chaîne du 15 nov. sous d'autres contrôles — test direct top-12 contre reste (d de Cohen, z global, doublon exclu ; nuls en comparaison).** La chaîne, c'est : au bout de l'axe KRAS, PGC/DPCR1/CLDN18 chutent et MUC16 monte. Sous les autres contrôles V4ROT, elle **ne réapparaît pas** : sous PGC, CLDN18, MUC17 et DPCR1, les 12 premiers ont le bloc **haut** (PGC +0,92 à +1,27, DPCR1 +0,69 à +1,18, CLDN18 +0,66 à +1,03) et MUC16 **bas** (−0,18 à −0,60) ; sous REG4 : CLDN18 +1,09, CEACAM5 +1,25, MUC16 −0,83 ; sous CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16 : presque plat (|d| < 0,5), sauf CEACAM5 +0,85 à +0,96 et CLDN18 +0,65 à +0,90. Les nuls correspondants restent à |d| ≤ 0,72 : les effets réels (+0,7 à +1,3) sont bien au-dessus du bruit des nuls. **Ce qui est réel, c'est le bloc et son anti-corrélation avec MUC16** — pas la lecture « rupture » qui reste propre à l'axe KRAS. Même chose à T_0 (fenêtres ±20, doublon exclu) : sous REG4, MUC2 et CLCA1, le bloc chute au seuil (DPCR1 −2,78, MUC16 −1,99 sous REG4 ; MUC16 −2,25, DPCR1 −1,59 sous MUC2) — mais MUC16 chute aussi, à l'inverse de la chaîne ; et ces T_0 tombent aux pas 173–174, il ne reste que 3–4 points après : fragile, même leçon que GSE62452 (§8.13), où 3 points retournaient le signe de MUC16. Sous MUC16 comme contrôle, le bloc monte au début de la série (PGC +1,87, DPCR1 +1,28, CLDN18 +1,19 au pas 10) : le même groupe, vu depuis l'autre bout.

**Les deux autres blocs — mêmes tests, même conclusion.** **Immunitaire :** dans les 12 premiers de presque chaque contrôle IMMROT, les gènes des lymphocytes sont hauts ensemble — PDCD1 +1,34 à +2,15, CD8A +1,29 à +1,79, GZMB +1,01 à +1,97, IFNG +0,75 à +1,65 (seuls CD68 et CD274 donnent moins, +0,45 à +0,65 pour PDCD1). Les nuls : |d| ≤ 0,74. C'est le bloc immunitaire, vu de l'intérieur : ordonner par n'importe quel gène immunitaire met les tumeurs « chaudes » en haut. Le §8.23 reste la lecture directionnelle : le long de l'axe KRAS, ce même bloc **tombe** (tumeur froide). **Réparation de l'ADN :** ATR, BRCA2, POLQ, CHEK1, RAD51 sont hauts ensemble dans les 12 premiers des contrôles BRCA1, BRCA2, ATR, CHEK1, POLQ et FANCD2 (+0,76 à +1,66) ; nuls |d| ≤ 0,91. XRCC1 est anti-corrélé au bloc (−0,69 à −1,13 dans ses 12 premiers) ; sous PARP1 et CHEK2, le bloc est plat ou négatif. C'est le bloc « stress de réplication » du §8.25 — en partie de la prolifération, comme montré là-bas.

**Ce qui ne sépare pas — bilan par famille.** V4ROT : ΔMC +0,02 à +0,11, ΔDelta −0,70 à +0,08, L7a et falsification identiques des deux côtés ; le plus grand écart (MUC17, ΔMC +0,107) vient de la séparation (0,936 contre 0,185), pas d'une rupture visible flux par flux au-delà du doublon. DEPMAPROT : ΔMC +0,01 à +0,06, Delta ~1,9 des deux côtés, falsification et bruit indisponibles — rien ne sépare, comme au bras CRISPR du §8.30. IMMROT : les ΔDelta > +1,0 (IFNG, CD19, CD68) sont des nuls tombés au niveau bas de d_div ; les ΔMC > +0,12 (CTLA4, PDCD1, CD8B, CD163) sont de la séparation, dont une partie vient du doublon quand le contrôle est le 1er flux. PARPROT : mêmes motifs (BRCA2, PARP2, ATM en ΔDelta ; BRCA1 en ΔMC). **Aucun contrôle, dans aucune famille, ne donne une séparation qui tienne sur les quatre indicateurs à la fois.** La Phase 2 (protocole gelé, §8.30) devra trancher avec son critère écrit d'avance ; elle attend toujours le go de Zackary.

### 8.33 Audit de la nature des flux — ce que chaque CSV contient vraiment, et ce qui peut encore enrichir les séries (18 nov. 2026)

**Verdict d'abord.** Les 24 séries de flux PDAC du projet sont de quatre natures seulement : **ARN de tumeurs** (la plupart), **ARN de lignées cellulaires** (DepMap), **protéine de tumeurs** (CPTAC) et **dépendance CRISPR de lignées** (DepMap). Aucune série ne mélange ces natures. Les enrichissements possibles avec ce qui est déjà sur le disque sont : allèle KRAS (fichier présent, utilisé en test direct au §8.20, jamais en série v6.1), mutations TP53/SMAD4/CDKN2A (fichier MAF présent, jointure non construite), nombre de copies MTAP/CDKN2A (GISTIC présent, utilisé en tests directs §8.26/§8.28/§8.29, jamais en série v6.1), prolifération (score calculé au §8.25, test direct seulement), sous-type (ICGC Bailey utilisé au §8.16, stade TCGA présent dans le fichier clinique, jamais utilisés comme axe). La déconvolution immunitaire n'existe pas sur le disque : seuls 12 gènes marqueurs. **Impossible, à nommer : pas de vrai temps** (l'ordre KRAS n'est qu'un pseudo-temps — un classement, pas une horloge), **pas de single-cell, pas de spatial.**

**Inventaire — les 24 séries de base (hors rotations et nuls ; 150 fichiers `pdac_*.csv` au total, rotations et nuls compris).** « Contrôle » = 1re colonne du CSV. Les séries de base ont `step` comme contrôle (l'ordre des lignes) ; les rotations ont le flux-contrôle lui-même comme 1re colonne — avec le doublon signalé au §8.32. « Corrigé » = résidus après régression sur les scores acinaire/îlots (v3/v4) ou valeurs brutes sinon. Toutes les séries ont leur nul permuté (graine 42) et leur provenance (`PROVENANCE_*.md`).

| Série (fichier) | Nature | n | Ordre (axe) | Corrigé ? | Runs v6.1 |
|---|---|---|---|---|---|
| TCGA v1 (`pdac_tcga_fluxes.csv`) | ARN, tumeurs TCGA PAAD (Firehose RSEM, log2(RSEM+1)) | 178 | KRAS brut croissant | Non — enzymes digestives + XIST (pureté + sexe) | Lot étendu, réel + nul |
| TCGA v2 (`…_v2.csv`) | ARN, tumeurs | 178 | KRAS brut | Non — 40 gènes pureté/sexe exclus, reste acinaire/îlots | Lot étendu |
| TCGA v3 (`…_v3.csv`) | ARN, tumeurs | 178 | KRAS résidu croissant | Oui — résidus (pureté) ; gènes du sexe dominent | Lot étendu |
| TCGA v4 (`…_v4.csv`) | ARN, tumeurs | 178 | KRAS résidu croissant | Oui — résidus + 17 gènes du sexe exclus ; 12 gènes tumoraux | Lot étendu + rotations V4ROT |
| TCGA v4r KRAS-valeur / KRAS-desc / CLDN18 / pureté (`…_v4r_*.csv`) | ARN, tumeurs | 178 | KRAS valeur / KRAS décroissant / CLDN18 / score acinaire | Oui (v4) | Lot étendu (v6, §8.9 ; refaits en v6.1) |
| TCGA v4r CLDN18 sans doublon (`…_v4r_cldn18_dedup.csv`) | ARN, tumeurs | 178 | CLDN18 croissant | Oui (v4) | 2 runs v6.1 (§8.31 (4)) |
| DepMap CRISPR (`pdac_depmap_fluxes.csv`) | Dépendance CRISPR (Chronos), lignées pancréas | 45 | KRAS Chronos croissant (KRAS = axe, jamais flux) | Non | Lot étendu + rotations DEPMAPROT |
| CPTAC UMich (`pdac_cptac_fluxes.csv`) | Protéine (spectrométrie de masse), tumeurs | 63 | KRAS protéine croissant | Non | Lot étendu |
| CPTAC BCM (`pdac_cptac_bcm_fluxes.csv`) | Protéine, tumeurs | 52 | KRAS protéine croissant | Non | Lot étendu |
| GSE71729 (`pdac_geo71729_fluxes.csv`, v4b, v4c) | ARN (puce Agilent), tumeurs Moffitt | 145 | KRAS brut croissant | Non (v4c : corrigé pureté) | Lot étendu |
| GSE71729 PARP (`…_parp.csv`) | ARN (puce), tumeurs | 145 | KRAS brut croissant | Non — 12 gènes réparation | Lot étendu |
| GSE62452 (`pdac_geo62452_fluxes.csv`, v4b) | ARN (puce Affymetrix HuGene-1.0-st), tumeurs | 69 | KRAS brut croissant | Non | Lot étendu |
| ICGC PACA-AU (`pdac_icgc_fluxes.csv`) | ARN (log2 CPM, Bailey 2016), tumeurs | 70 | KRAS brut croissant | Non | Lot étendu |
| Immunitaire TCGA / GSE71729 / GSE62452 / ICGC (`pdac_immune_*_fluxes.csv`) | ARN, tumeurs (12 gènes marqueurs immunitaires) | 178 / 145 / 69 / 70 | KRAS brut croissant | Non (bulk, sans correction de pureté) | Lot étendu (TCGA) + rotations IMMROT (TCGA) ; ICGC/GSE62452 en v6 (§8.23) |
| PARP/ATR TCGA (`pdac_tcga_fluxes_parp.csv`, `…_atr.csv`) | ARN, tumeurs (12 gènes réparation) | 178 | KRAS brut / KRAS résidu (atr : corrigé pureté) | atr : oui ; parp : non | Lot étendu + rotations PARPROT |
| LUAD (`pdac_luad_fluxes.csv`) | ARN, tumeurs poumon TCGA | 515 | KRAS brut croissant | Non | Lot étendu |
| COAD (`pdac_coad_fluxes.csv`) | ARN, tumeurs côlon TCGA | 285 | KRAS brut croissant | Non | Lot étendu (réel refait après perte) |
| Rotations V4ROT / DEPMAPROT / IMMROT / PARPROT (96 fichiers) | Mêmes natures que leurs séries mères | 178 / 45 / 178 / 178 | Un flux à tour de rôle, croissant | Comme la série mère | 96 runs v6.1 (§8.32) |

**Ce que les flux ne sont pas.** Aucun flux n'est une mesure de temps, de dose ou de réponse à un traitement : ce sont des niveaux d'expression, d'abondance protéique ou de dépendance génétique, rangés le long d'un axe choisi (KRAS le plus souvent). Les flux « step » des séries de base ne sont pas des données : c'est l'indice de ligne. Les 12 flux d'une série ne sont pas indépendants : ils ont été choisis par variance ou par protocole sur la même matrice (v1–v4), et les blocs de co-expression du §8.32 (estomac/mucus, immunitaire, réparation) en sont la preuve directe — un seuil qui fait bouger 8 flux ensemble peut être un seul fait, pas huit.

**Enrichissements possibles avec ce qui est déjà sur le disque — un par un.**

- **Allèle KRAS — PRÉSENT, utilisé en test direct, jamais en série v6.1.** `data/kras_alleles_pancreas.csv` (54 lignées DepMap : G12D 23, G12V 20, G12R 5, Q61H 2, Q61R 1, G12C 1, G12A 1, G12I 1 ; source : MAF DepMap 24Q4, SHA `86b8530b…`). Utilisé au §8.20 : MRTX1133 tue les G12D spécifiquement (p=0,0001). Pourquoi pas en série v6.1 : il faudrait construire une série par allèle (ou ordonner par allèle), ce qui n'a pas été fait — mini-protocole gelé à écrire, go de Zackary à demander. Les données TCGA ont aussi leurs mutations KRAS (`data/kras_mutations_maf.csv`, allèles des tumeurs) : même statut, jamais utilisées comme axe.
- **TP53, SMAD4, CDKN2A (mutations) — PRÉSENT en fichier, jointure non construite, jamais testé.** `data/OmicsSomaticMutationsMAFProfile.maf` (DepMap 24Q4, 98 Mo, 919 profils) contient les mutations, mais ses identifiants sont des codes `PR-…`, pas les `ACH-…` des lignées : la jointure passe par `data/OmicsProfiles.csv` et n'a pas été construite (vérifié le 18 nov. : 0 mutation trouvée avant jointure — ce zéro est un artefact de la jointure absente, pas une mesure). Pourquoi pas en série v6.1 : pas de série par statut mutationnel construite ; le statut TP53/SMAD4 n'a été utilisé nulle part dans le projet. À faire : construire la table lignée × (KRAS allèle, TP53, SMAD4, CDKN2A) puis, si le go est donné, des séries ordonnées ou stratifiées.
- **Nombre de copies MTAP / CDKN2A — PRÉSENT, utilisé en tests directs, jamais en série v6.1.** `data/tcga_paad_gistic.tar.gz` (MD5 `816034f7…`, §8.26) et `data/OmicsCNGene.csv` (1,4 Go, MD5 `4696565f…`, §8.28/§8.29) : délétions mesurées, pas des proxys. Pourquoi pas en série v6.1 : aucune série de flux ordonnée par statut MTAP n'existe — les tests directs ont suffi au verdict (effet PRMT5 suit MTAP). Une série « ordonnée par CN MTAP » est constructible sur les 47 lignées DepMap, mais n=47 et le pipeline n'y sépare déjà pas le nul (§8.30).
- **Déconvolution immunitaire — ABSENTE.** Aucune estimation de fractions cellulaires (CIBERSORT, xCell, MCP-counter, EPIC) n'est sur le disque. Les séries immunitaires n'ont que 12 gènes marqueurs en ARN bulk : elles ne distinguent pas « plus de cellules T » de « plus d'expression par cellule ». Pourquoi pas fait : aucun outil de déconvolution n'a été lancé ; les matrices d'expression complètes sont pourtant sur le disque (Firehose TCGA, GEO, ICGC), donc c'est faisable sans nouveau téléchargement — mais cela demande un choix d'outil et un go, et le §8.23 a déjà fermé la piste KRAS + anti-PD-(L)1 par les marqueurs.
- **Prolifération — CALCULÉE, test direct seulement, jamais en série v6.1.** Score = médiane de MKI67, TOP2A, PCNA, CCNB1, calculé sur la matrice TCGA au §8.25 (`atr_chek1_retest.py`, SHA `df6d1ddf…`) : il explique le signal large de réparation (RAD51 +0,791 avec la prolifération) et laisse ATR seul survivant. Pourquoi pas en série v6.1 : le score a servi de contrôle (corrélation partielle), pas d'axe ; une série « ordonnée par prolifération » est constructible directement depuis la matrice Firehose, sans nouvelle donnée.
- **Sous-type — PRÉSENT pour ICGC, utilisé ; présent pour TCGA, jamais utilisé.** ICGC : sous-types de Bailey (Squamous, Pancréatique progéniteur, Immunogénique, ADEX) extraits des tableaux supplémentaires de Bailey 2016 (`data/bailey2016_suppl_tables1-13.xlsx`, SHA `778224b3…`) — utilisés au §8.16 (Cox ajusté sur le sous-type : MUC16 HR 1,75, p=0,004). TCGA : la colonne `SUBTYPE` existe dans `data_clinical_patient.txt` (fichier clinique, 184 patients) — jamais utilisée comme axe ni comme ajustement. GSE71729 : sous-types de Moffitt (classique/basal) non extraits. Pourquoi pas en série v6.1 : aucune série ordonnée ou stratifiée par sous-type n'a été construite ; c'est un enrichissement direct à partir des fichiers déjà là.
- **Stade — PRÉSENT (TCGA), jamais utilisé.** `AJCC_PATHOLOGIC_TUMOR_STAGE` (et PATH_T/N/M) dans `data_clinical_patient.txt` ; survie dans le même fichier (§8.12) et dans les matrices GEO/ICGC. Pourquoi pas en série v6.1 : aucune série ordonnée par stade n'a été construite. Attention de méthode : le stade est une variable de résultat clinique, pas un axe neutre — l'ordonner, c'est tester « le pipeline voit-il la progression clinique », une question différente de l'axe KRAS, à formuler avant de lancer.
- **MTAP / PRMT5 en série de flux — ABSENT.** Il n'existe aucune série de flux MTAP/PRMT5 : tout le travail MTAP est en tests directs (§8.26–§8.29). Construire une série demanderait un mini-protocole gelé (quels flux ? expression PRMT5 + voisins 9p21 ? ordre = CN MTAP ?) et le go de Zackary.

**Ce qui est impossible — à nommer honnêtement.** **Pas de vrai temps :** l'ordre KRAS (ou tout autre flux) est un classement, pas une horloge ; un « seuil » le long de cet axe est une coupure dans un classement, pas un moment. Les rotations le montrent : le même groupe de tumeurs se retrouve en haut ou en bas selon l'axe, sans qu'aucun axe soit « le » temps. **Pas de single-cell :** toutes les séries sont du bulk (tumeur entière) ou des lignées ; aucune donnée cellule par cellule n'est sur le disque, et aucune ne peut être fabriquée à partir du bulk. **Pas de spatial :** aucune coordonnée dans la tumeur, aucune lame annotée ; la question « où, dans la tumeur, le bloc s'effondre » ne peut pas être posée avec ces données. **Pas de longitudinal :** aucune tumeur n'est mesurée deux fois (avant/après traitement) dans ces cohortes ; les séries ne suivent pas des patients dans le temps. Ce qui manque pour ces quatre impossibilités, ce sont d'autres données, pas d'autres runs du même pipeline.

### 8.34 Test A — série TCGA v4 ordonnée par prolifération : NON, la chaîne ne réapparaît pas (18 nov. 2026)

**Verdict d'abord : NON — la chaîne du 15 nov. ne réapparaît pas quand les 178 mêmes tumeurs sont rangées par vitesse de division au lieu de KRAS.** Au bout de l'axe KRAS, PGC/DPCR1/CLDN18 s'effondraient et MUC16 montait (top-12 : PGC −0,89 sd, DPCR1 −0,85 sd, CLDN18 −0,46 sd, MUC16 +0,64 sd, §8.4). Au bout de l'axe prolifération, seul PGC baisse nettement (−0,57 sd) ; DPCR1 baisse moins que son nul (−0,35 contre −0,47) ; CLDN18 est plat (−0,14) ; MUC16 est plate (−0,04). Le reste du bloc ne s'effondre pas : il monte (KRT20 +0,63, MUC2 +0,47, CEACAM5 +0,39, GSTM1 +0,54). La lecture « rupture » reste propre à l'axe KRAS — comme sous les 48 contrôles du §8.32. Ce qui est réel, c'est le bloc et son anti-corrélation avec MUC16, pas la coupure.

**Le lot.** Go de Zackary le 18 nov. 2026, 15h06 (test A, 1re des 4 propositions, recommandée). Protocole gelé `PROTOCOL_testA_proliferation.md` (écrit avant les runs). Construction `build_fluxes_tcga_v4_prolif.py` (SHA `4bb05e62…1386`) : score de prolifération = médiane des résidus (correction pureté v4) de MKI67, TOP2A, PCNA, CCNB1 — définition (c) du §8.25 — recalculé depuis la matrice Firehose `data/tcga_paad_rsem.tar.gz` (MD5 `b09569ce…ac0a`), rien de re-téléchargé. **Vérification de reproduction passée : les 12 flux v4 recalculés reproduisent le CSV v4 à 1,776e-15 près (atol 1e-9), PGC seul pareil.** Série réelle `pdac_tcga_fluxes_v4_prolif.csv` (SHA `c87a4e0a…e5700`), nul `…_prolif_nul.csv` (SHA `99cbc377…3019`, lignes permutées, graine 42, contrôle intact) ; contrôle PROLIF en 1re colonne — PROLIF n'est pas un flux, donc **pas de doublon** (défaut des rotations §8.32 explicitement évité). Provenance complète `PROVENANCE_testA_proliferation.md`. Pipeline `universal_v6.1.0_cohen.py`, SHA `2af5e5ce…c1c9`, revérifié inchangé ; mode fast ; 2 runs, exit 0/0, 36 fichiers chacun, journal `runs_v61_testa.log` (FIN 2026-11-18T20:18:30Z, terminés=2, échecs=0). Incident rapporté honnêtement : le 1er lancement (systemd-run, 20h09 UTC) a été tué ~1 min après par un redémarrage du service ; une surveillance cron toutes les 15 min a été créée comme filet, la relance a réussi du 1er coup, la surveillance s'est arrêtée d'elle-même à 2/2 et le cron a été supprimé. Aucun dossier de run supprimé, aucun CSV modifié. Lecture : `testa_reading.py` (SHA `312983df…0647`), données `testa_direct_tests.csv` (SHA `9c2afa41…ed06`) et `testa_extract.json` (SHA `5e76f0c7…4731`).

**Le pipeline ne sépare pas réel et nul, ici non plus.** Réel : cascade 0 / 0,73 / **3,73** / 24,57 / 24,57 % (pas 0/1/**7**/43/43) ; MC best 0,3638 (seuil 10,87 %) ; Delta 3,798 ; L7a UP 0,412 ; falsification 0,737 ; L7b FRAGILE ; régime divergence. Nul : cascade 0 / 2,32 / **5,32** / 46,59 / 46,59 % (pas 0/4/**9**/82/82) ; MC best **0,4587** (plus haut que le réel) ; Delta **4,590** (plus haut que le réel) ; L7a DOWN 0,196 ; falsification 0,733 (identique au réel) ; L7b FRAGILE. Le MC du nul dépasse le réel par la robustesse (0,693 contre ~0) — même famille d'artefact qu'aux §8.31/§8.32 (la robustesse au plancher dans le réel fait passer le nul devant). Seule piste, pas une preuve (aucun seuil de séparation n'était pré-enregistré) : L7a vote en sens opposé (UP 0,412 réel contre DOWN 0,196 nul), mais avec un T_0 au pas 7 et une falsification identique des deux côtés, ce n'est pas une séparation. Bruit : réel « proxy de variance modéré » (score moyen 0,629), nul « mixte » (0,475). F1/F2 « Tous » (médiane sur 29 estimateurs) : le rapport après/avant s'effondre des deux côtés (F1 ×0,025 réel contre ×0,069 nul ; F2 ×0,005 contre ×0,093) et le signe de F1 change chez 23/29 estimateurs réels contre 26/29 nuls — aucune direction cohérente.

**Tests directs top-12 contre reste (d de Cohen ; + = plus haut chez les 12 tumeurs les plus proliférantes ; en sd, mêmes unités que le §8.4).** Réel : PGC **−0,57** (d −0,61), DPCR1 −0,35 (d −0,37), CLDN18 −0,14 (d −0,15), MUC16 **−0,04** (d −0,04) ; le reste du bloc monte : KRT20 +0,63, GSTM1 +0,54, MUC2 +0,47, CEACAM5 +0,39, CLCA1 +0,26, REG4 +0,14 ; CR2 −0,22, MUC17 −0,08. Nul : |d| ≤ 0,55 partout (CR2 +0,55, DPCR1 −0,51, MUC16 −0,45, CLCA1 +0,26) — la baisse de DPCR1 dans le réel (−0,37) est **en dessous** du bruit du nul ; seule la baisse de PGC (−0,61 contre −0,00 au nul) dépasse le nul. Référence KRAS (§8.4) : PGC −0,89, DPCR1 −0,85, CLDN18 −0,46, MUC16 +0,64 — aucun des quatre ne se retrouve ici. **MUC16 monte doucement le long de l'axe** (Spearman +0,277, p < 0,001 ; CEACAM5 +0,306, KRT20 +0,212) **mais sans saut chez les 12 premières** (−0,04 sd) : une pente graduelle, pas une rupture. Autour de T_0 (pas 7, fenêtres ±20) : tous les flux montent (+0,61 à +2,42) — mais la fenêtre « avant » ne compte que 7 points (les tumeurs les moins proliférantes sont globalement basses) : fragile, même leçon que DepMap (§8.30) et CPTAC (§8.8), pas une lecture de chaîne. Le nul autour de son T_0 (pas 9) : |d| ≤ 0,93, signes mêlés.

**Pourquoi les deux axes ne se recouvrent pas.** Le score prolifération suit KRAS (+0,339 en résidus, +0,382 en brut — le §8.25 rapportait +0,386), mais les 12 tumeurs les plus proliférantes et les 12 plus KRAS ne se recouvrent qu'à **1/12**. Les deux axes trient les mêmes tumeurs dans un ordre globalement proche, mais pas les mêmes extrêmes — et c'est aux extrêmes que la chaîne KRAS se joue. Sensibilité : score brut contre score résidus, Spearman +0,944, recouvrement top-12 9/12 — le choix résidus/brut ne fait pas le résultat.

**Ce que ça change.** La chaîne (bloc qui chute + MUC16 qui monte) est confirmée comme propre à l'axe KRAS : elle ne réapparaît ni sous les 48 contrôles du §8.32, ni sous l'ordre prolifération. La prolifération explique une partie du paysage (le §8.25 l'a montré pour la réparation), mais elle ne porte pas la coupure estomac/mucus. Prochaines étapes : tests B (TP53/SMAD4/CDKN2A, directs) et C (ordre par stade) — protocole gelé à écrire, go de Zackary à demander ; la Phase 2 (discrimination) attend toujours son go.

### 8.35 Phase 2 — discrimination réel / nul : ce qui sépare, ce qui ne sépare pas (18 nov. 2026)

**Verdict d'abord : le pipeline, en l'état, ne sépare pas réel et nul sur ces
séries PDAC par ses scores principaux — MC best_score 1/8, cohérence des flux
2/8, L7a 4/8. Seuls deux indicateurs atteignent la barre des 6/8 fixée
d'avance : Delta (6/8) et surtout max_separation (6/8), tous deux dans le
sens réel > nul. Les deux 8/8 (position de T_0, écart cascade complet) sont
triviaux par construction et ne prouvent rien. La phrase globale du protocole
(« le pipeline, en l'état, ne sépare pas réel et nul ») ne s'applique donc
pas au pied de la lettre — deux indicateurs tiennent — mais elle reste vraie
pour l'essentiel de l'instrument : ses scores vedettes ne discriminent pas.**

**L'étude.** Go de Zackary le 18 nov. 2026, 15h06 (phase 2, 2e des 4
propositions, dans l'ordre, après le test A §8.34). Protocole gelé
`PROTOCOL_phase2_discrimination.md` (écrit le 16 nov., avant tout calcul).
Question : quels indicateurs dérivés du pipeline séparent une série réelle de
son nul permuté (graine 42) ? Les 8 indicateurs du §3, les 8 paires
principales du §4 (HP35 n=1000, TCGA v4 n=178, GSE71729 n=145, GSE62452 n=69,
ICGC n=70, immunitaire TCGA n=178, PARP TCGA n=178, DepMap n=45), critère
du §4 (écart > gigue ET direction cohérente sur ≥ 6/8 paires). **Aucun
nouveau run du pipeline** : tout est lu dans les `master_results.json` v6.1
déjà sur disque (lots 140/140 terminés + test A) et dans les CSV d'entrée
pour l'indicateur 6. Pipeline `universal_v6.1.0_cohen.py`, SHA
`2af5e5ce…c1c9`, revérifié inchangé, jamais modifié. Extracteur
`extract_phase2.py` (SHA `5eb3ac24…75aa`, règles de comptage écrites dans le
script avant tout calcul, log `v61_phase2_extract.log`) ; table
`v61_phase2_table.md` (SHA `1ef15409…eb04`) et données brutes
`v61_phase2_table.csv` (SHA `6b5bb790…5bb7`, 8 principales + 23 secondaires)
et `v61_phase2_table.json` (SHA `8748745a…aa57`). Nul jamais redéfini après
les résultats (graine 42, permutation des lignes, contrôle intact). Aucun
seuil de séparation pré-enregistré au-delà du critère du protocole. Aucun
consensus exigé entre flux ou contrôles.

**Les verdicts, un par un (formulation du protocole).**

1. **Delta — « Sépare sur 6/8 : [TCGA v4, GSE62452, ICGC, immunitaire TCGA,
   PARP TCGA, DepMap], échoue sur [HP35, GSE71729]. »** Écarts réel−nul :
   TCGA v4 +0,42 (4,18 contre 3,77) ; GSE62452 +0,15 (1,41 contre 1,26) ;
   ICGC +0,07 (1,44 contre 1,37) ; immunitaire +1,91 (4,21 contre 2,30) ;
   PARP +0,26 (4,30 contre 4,04) ; DepMap +0,24 (1,93 contre 1,69) ; HP35
   −0,09 (4,48 contre 4,57) ; GSE71729 −0,04 (2,16 contre 2,20). Réserve :
   il échoue sur HP35, le témoin positif connu — là où le pipeline sépare
   nettement par ailleurs, c'est le nul qui a le Delta le plus haut. Deux
   des six écarts sont petits (ICGC +0,07 ; GSE62452 +0,15). En annexe :
   13/23 seulement.
2. **MC best_score — « Sépare sur 1/8 : [HP35], échoue sur [TCGA v4,
   GSE71729, GSE62452, ICGC, immunitaire TCGA, PARP TCGA, DepMap]. »** Le
   score vedette ne dépasse la gigue (±0,07) sur aucune série PDAC : TCGA v4
   +0,0453 ; GSE71729 +0,0059 ; GSE62452 −0,0031 ; ICGC +0,0150 ;
   immunitaire +0,0545 ; PARP +0,0244 ; DepMap +0,0116. Seul HP35 passe,
   largement (+0,1950 ; 0,6035 contre 0,4086). Nuance à ne pas écraser :
   7/8 écarts sont positifs — le MC penche du bon côté — mais tous sous la
   gigue : il ne dépasse jamais le bruit. Le seuil MC, lui, saute d'un bout
   à l'autre (TCGA v4 : 10,87 % réel contre 81,52 % nul ; immunitaire :
   79,35 % contre 15,56 %) : pas une position stable. En annexe : 2/23.
3. **max_separation — « Sépare sur 6/8 : [HP35, TCGA v4, ICGC, immunitaire
   TCGA, PARP TCGA, DepMap], échoue sur [GSE71729, GSE62452]. »**
   L'indicateur le plus solide : HP35 +1,6512 (1,7718 contre 0,1206) ;
   TCGA v4 +0,2928 ; ICGC +0,0970 ; immunitaire +0,3675 ; PARP +0,1688 ;
   DepMap +0,1904 ; GSE71729 +0,0402 (sous la gigue) ; GSE62452 −0,0036
   (plat). En annexe : 16/23 — le seul indicateur qui tient à peu près
   partout.
4. **Position de T_0 — « Sépare sur toutes les paires » (8/8) — MAIS
   TRIVIAL.** |T_0 réel − T_0 nul| : 18,33 (HP35) ; 77,26 (TCGA v4) ; 68,92
   (GSE71729) ; 78,54 (GSE62452) ; 19,88 (ICGC) ; 51,39 (immunitaire) ;
   51,19 (PARP) ; 13,21 (DepMap) points. Jamais nul. Le critère du
   protocole (écart > 0, gigue 0) ne peut échouer que sur égalité exacte :
   ce 8/8 prouve que le nul place son seuil ailleurs — ce qu'on savait
   déjà (§8.31/§8.32) — pas une discrimination.
5. **Falsification delta_vs_null — « Sépare sur 4/5 disponibles : [HP35,
   TCGA v4, GSE71729, PARP TCGA], échoue sur [immunitaire TCGA] ;
   indisponible sur [GSE62452, ICGC, DepMap] (n < 75). »** Écarts :
   HP35 +0,148 (1,266 contre 1,118) ; TCGA v4 +0,207 (0,849 contre 0,642) ;
   GSE71729 +0,114 (0,601 contre 0,487) ; PARP +0,169 (0,867 contre
   0,698) ; immunitaire −0,147 (0,985 contre 1,132 — inversé). Réserves :
   ce n'est pas une comparaison au nul permuté — c'est une comparaison
   interne (d_crit géométrique contre SpectralDimension, §8.31) — et en
   annexe la direction majoritaire s'inverse (7/18, direction − : TCGA
   v1/v2/v3 ont une falsification plus haute au nul qu'au réel). GSE62452
   et ICGC : valeurs brutes JSON présentes (0,199/0,340 et 0,238/0,135)
   mais non utilisées (n < 75, protocole §3) ; DepMap réel : valeur absente
   du JSON lui-même (nul brut 0,043).
6. **Cohérence par flux à T_0 — « Sépare sur 2/8 : [HP35, TCGA v4], échoue
   sur [GSE71729, GSE62452, ICGC, immunitaire TCGA, PARP TCGA, DepMap]. »**
   Fraction des flux dont le d de Cohen à T_0 a le signe du vote L7a de la
   série elle-même (fenêtre ±20, ±10 si n < 100 ; pas T_0 =
   arrondi(T_0% × n / 100) ; aucun doublon contrôle=flux à exclure ici —
   contrôle = « step », pas un flux) : HP35 0,71 contre 0,14 (pas 91/274,
   7 flux) ; TCGA v4 0,67 contre 0,33 (pas 166/28) ; GSE71729 0,67 contre
   0,67 ; GSE62452 0,42 contre 0,58 ; ICGC 0,50 contre 0,58 ; immunitaire
   0,92 contre 1,00 ; PARP 0,67 contre 0,83 ; DepMap 0,50 contre 0,67
   (fenêtre « avant » de 2 points seulement, pas 2 — fragile). Le |d|
   médian seul ferait 6/8, mais la fraction — le cœur de l'indicateur —
   ne fait que 2/8. Le point dur : le nul est parfois PLUS cohérent que
   le réel à son propre T_0 — immunitaire nul 12/12 flux (1,00, |d|
   médian 0,76) contre réel 0,92 (0,24) ; PARP nul 0,83 contre réel 0,67.
   La cohérence des flux autour d'un seuil ne distingue pas réel et nul.
7. **L7a — « Sépare sur 4/8 : [TCGA v4, immunitaire TCGA, PARP TCGA,
   DepMap], échoue sur [HP35, GSE71729, GSE62452, ICGC]. »** Confiance
   signée (s = +conf si up, −conf si down) : direction majoritaire
   NÉGATIVE — le réel vote plus « down » / moins confiant « up » que le
   nul. Écarts : TCGA v4 −0,572 (down 0,405 contre up 0,167) ; immunitaire
   −0,526 (down 0,183 contre up 0,343) ; PARP −0,220 (up 0,173 contre up
   0,393) ; DepMap −0,541 (down 0,196 contre up 0,345) ; HP35 +0,044 ;
   GSE71729 +0,061 ; GSE62452 +0,139 (sens inverse) ; ICGC +0,531 (sens
   inverse : réel up 0,181 contre nul down 0,350). Le vote L7a ne sépare
   pas.
8. **Écart cascade complet — « Sépare sur toutes les paires » (8/8) — MAIS
   TRIVIAL.** Somme |Δ| sur les 5 positions : 109,21 (HP35) ; 203,83
   (TCGA v4) ; 263,68 (GSE71729) ; 258,71 (GSE62452) ; 142,46 (ICGC) ;
   159,54 (immunitaire) ; 139,68 (PARP) ; 40,43 (DepMap). Même réserve que
   l'indicateur 4 : la somme ne peut être nulle que si les deux cascades
   sont identiques chiffre par chiffre.

**Annexe (23 paires secondaires, mêmes règles, mêmes gigues).** Delta
13/23 ; MC 2/23 ; max_separation 16/23 ; T_0 23/23 ; falsification 7/18
(direction inversée) ; cohérence fraction 8/22 (une paire sans fraction :
immunitaire GSE62452, L7a réel « flat ») ; L7a 12/23 ; cascade 23/23. Le
COAD réel, manquant dans `v61_extended_compare.csv` (43/44, §8.31), a été
refait ensuite (lot final 140/140, §8.32) et entre ici directement depuis
son `master_results.json` (n=285 : ΔDelta +0,02, ΔMC +0,0195, Δmax_sep
+0,1201, |ΔT_0| 18,69, Δfals +0,004, Δfrac −0,33, ΔL7a −0,621, Σ|Δ|
57,84). V4R_KRASVAL est la même série que TCGA v4 (doublon de nom, pas un
9e point). TESTA_PROLIF (test A, §8.34) comme paire secondaire : Delta et
MC inversés (nul devant : −0,79 et −0,0948), max_separation toujours
positif (+0,2501). Les 48 paires de rotations (§8.32) ne sont pas
recomptées ici : leur lecture existe déjà (§8.32 — aucun contrôle ne
sépare proprement) et elles portent le défaut du doublon contrôle=flux.

**Ce que ça change.** Trois choses. D'abord, le verdict honnête sur
l'instrument : sur les séries PDAC, le pipeline place des seuils et des
cascades (c'est mesuré, §8.31/§8.32), mais ses scores principaux ne disent
pas « ceci est réel, ceci est un nul ». Seul max_separation — un
sous-produit du MC, pas le score MC lui-même — tient sur 6/8 paires
principales et 16/23 secondaires. Ensuite, une piste précise : le MC
best_score penche du bon côté sur 7/8 paires mais reste sous la gigue
(±0,07, hachage Python non déterministe, §8.30) — la gigue elle-même est
peut-être ce qui cache la séparation. Enfin, la falsification et la
cohérence des flux, deux lectures qu'on croyait discriminantes, ne le sont
pas : la falsification compare autre chose que le nul permuté, et un nul
peut être plus « cohérent » que le réel autour de son propre seuil.

**Piste v6.2 — PROPOSITION SEULEMENT, rien n'est construit.** L'étude
justifie de proposer (conception gelée séparée :
`PROTOCOLE_v6.2_proposition.md`, à écrire et à faire valider avant tout
code) : (a) hachage stable L5 (hashlib.sha256 au lieu de `hash()`,
proposition déjà faite au §8.30 — la phase 2 la renforce : si la gigue
tombe, les écarts MC de +0,01 à +0,05 deviennent lisibles au lieu d'être
noyés) ; (b) tester, en protocole gelé séparé, si un score fondé sur
max_separation (plutôt que sur le best_score MC) discrimine mieux, sans
jamais le présenter comme une séparation avant le test ; (c) élucider les
niveaux discrets de Delta (§8.32 : d_div ne prend que quelques niveaux —
le 6/8 de Delta vient-il de sauts de niveau ?) avant d'en faire un
indicateur de discrimination. **Aucun changement de code, aucun run, sans
le go séparé de Zackary.** La v6.1 reste la version de travail, la v6 la
référence intacte.

**Ce que ça ne change pas.** Les résultats cliniques du dossier (daraxonrasib,
vopimetostat + daraxonrasib, §8.20/§8.22) ne viennent pas du pipeline et ne
sont pas touchés par ce verdict : ce sont des avancées trouvées, pas des
prédictions. Les 3 blocs de co-expression (§8.32) et la chaîne KRAS (§8.4)
restent des faits de tests directs, pas des verdicts du pipeline. Prochaines
étapes : étape 3 du programme (PDF + GitHub, avec cette section incluse),
puis étape 4 (enrichissements §8.33) ; la v6.2 attend son go.

### 8.36 Étape 4 — enrichissements du §8.33 : allèles KRAS, statuts mutationnels, série ordonnée par CN MTAP (18 nov. 2026)

**Verdict d'abord, en trois phrases. (a) Série par allèle KRAS : IMPOSSIBLE — 23 lignées au maximum par allèle (G12D), le minimum fast est 40 ; les tests directs disent que G12D et G12V sont plus KRAS-dépendantes que les autres allèles, que PRMT5 ne change pas avec l'allèle, et que le MRTX1133 reste G12D-spécifique (recalculé). (b) Statuts TP53/SMAD4/CDKN2A : TP53 et SMAD4 ne déplacent ni KRAS ni PRMT5 ni ATR ; l'effet apparent de CDKN2A sur PRMT5 (p=0,014) est un confondant MTAP — il disparaît quand on fixe MTAP (p=0,76) — ce qui renforce le §8.29 : l'effet PRMT5 suit MTAP, pas la délétion 9p21. Aucune série v6.1 n'est possible non plus ici (plus grand groupe 38 < 40). (c) Série ordonnée par perte de MTAP : NON, la chaîne ne réapparaît pas — le pipeline ne sépare pas réel et nul (MC, Delta et falsification tous meilleurs au nul), et les tests directs ne retrouvent pas la signature KRAS (PGC −0,40, DPCR1 −0,08, CLDN18 +0,01, MUC16 −0,14 chez les 12 plus délétées). La chaîne reste propre à l'axe KRAS — troisième axe testé qui ne la porte pas, après la prolifération (§8.34) et les 48 contrôles (§8.32).**

**Le lot.** Go de Zackary le 18 nov. 2026, 15h06 (étape 4, dernière des 4 propositions, dans l'ordre ; test A §8.34, Phase 2 §8.35 et PDF 457 pages terminés ; les poussées GitHub de l'étape 3 sont préparées mais non poussées, approbation expirée — hors de cette étape). Protocole gelé `PROTOCOL_enrichissements_833.md` (écrit avant tout test et tout run ; SHA `fdffeed4…cc8f`). Pipeline `universal_v6.1.0_cohen.py`, SHA `2af5e5ce…c1c9`, revérifié inchangé avant les runs ; mode fast ; nul permuté graine 42, contrôle intact. Aucun seuil de séparation pré-enregistré. PDF non régénéré (c'est la publication finale).

**(a) Allèle KRAS — série impossible, tests directs seulement.** Comptages vérifiés sur les données : `data/kras_alleles_pancreas.csv` (SHA `9ac803ad…0d42`, 54 lignées) — G12D 23, G12V 20, G12R 5, Q61H 2, Q61R 1, G12C 1, G12A 1, G12I 1 ; dans les 45 lignées DepMap de la table de mutations — G12D 19, G12V 14, G12R 5, Q61H 2, G12C 1, G12A 1, inconnu 3. Maximum 23 < 40 : la série v6.1 par allèle est impossible, règle écrite d'avance. Vérifications et tests directs : `verify_alleles_mutations.py` (SHA `53b90536…b8781`), sortie `verify_alleles_mutations.txt` (SHA `96fd1026…e979`). Dépendance Chronos KRAS (45 lignées, Mann-Whitney bilatéral + d de Cohen) : G12D vs G12V p=0,15 (d −0,69, non significatif — les deux sont très dépendantes, médianes −2,34 contre −1,84) ; G12D vs autres allèles p=0,0017 (d −1,42) ; G12V vs autres p=0,017 (d −1,08). Les 3 lignées KRAS sauvages / allèle inconnu sont à peine dépendantes (médiane −0,36). Dépendance Chronos PRMT5 : aucune différence par allèle (G12D vs G12V p=0,93, d +0,16 ; G12D vs autres p=0,95 ; G12V vs autres p=0,90) — l'allèle KRAS ne déplace pas PRMT5. Viabilité MRTX1133 recalculée aujourd'hui depuis `data/mrtx1133_prism_kras_allele.csv` (SHA `7a449c92…5ef6`, 40 lignées) : G12D vs G12V p=0,00039 (d −1,52 ; moyennes −1,70 contre −0,37 — identiques au §8.20, dont le p=0,0001 venait d'un test non précisé là-bas ; même conclusion) ; G12D vs autres p=0,0060 (d −1,31) ; G12V vs autres p=0,68 (d +0,08). Le MRTX1133 tue les G12D spécifiquement — confirmé par recalcul, pas importé.

**(b) Jointure MAF TP53/SMAD4/CDKN2A — construite, vérifiée, tests directs ; série impossible.** Correction au §8.33 : la jointure PR→ACH n'était pas « non construite » au moment de l'étape 4 — elle avait été construite le 18 nov. en préparation du §8.33 (`build_mutation_table_pancreas.py`, SHA `49b87f4d…1061`), et l'étape 4 l'a **revérifiée en relançant le constructeur : SHA de sortie identique** (`f3fa2bd2…63f36`), 45 lignées, 2 925 lignes MAF pour les 4 gènes, 0 profil PR sans correspondance. Statuts : TP53 mutée 38/45, SMAD4 11/45, CDKN2A 12/45, KRAS 42/45 ; co-occurrences déjà notées au §8.33. Tests directs Chronos (Mann-Whitney bilatéral + d de Cohen, mêmes conventions que §8.28/§8.29) : TP53 muté contre sauvage (38/7) — KRAS p=0,19 (d −0,38), PRMT5 p=0,89 (d −0,08), ATR p=0,94 (d +0,07) : rien. SMAD4 (11/34) — KRAS p=0,089 (d −0,79, tendance non significative), PRMT5 p=0,29 (d +0,35), ATR p=0,52 (d −0,19) : rien de significatif. CDKN2A (12/33) — KRAS p=0,19 (d −0,57), PRMT5 **p=0,014 (d +0,78, médianes −0,94 contre −1,14 : les mutées semblent moins PRMT5-dépendantes)**, ATR p=0,40 (d −0,15). **Le « mais » qui compte : les lignées CDKN2A-mutées ont un CN MTAP médian de +0,96 contre +0,29 chez les sauvages, et seulement 2/12 sont MTAP-délétées (< 0,5) contre 18/33 — le groupe muté est justement celui où MTAP est intact.** Stratifié par délétion MTAP, l'effet disparaît : strate MTAP-intacte, CDKN2A mut contre sauv, PRMT5 p=0,76 (d +0,19, n=10 contre 15) ; strate MTAP-délétée, effectifs trop petits (mut n=2). L'effet apparent CDKN2A→PRMT5 est donc un **confondant MTAP**, pas un effet CDKN2A — et il renforce le §8.29 par un angle nouveau : même en regardant par la mutation CDKN2A, c'est MTAP qui porte l'effet PRMT5. Cohérence : Spearman PRMT5 ~ CN MTAP reste fort dans les groupes où MTAP varie (TP53 mut +0,50, p=0,0013 ; CDKN2A sauv +0,54, p=0,0013 ; SMAD4 sauv +0,58, p=0,0003) et absent là où MTAP ne varie presque pas (CDKN2A mut −0,06, n=12, presque toutes intactes). **Séries v6.1 : impossibles.** Deux séries muté/non-muté exigeraient 40 + 40 — plus grand groupe 38 (TP53 muté). Ordonner les 45 lignées par statut binaire (0/1) serait dégénéré : le seuil serait forcé à la frontière des groupes par construction, pas découvert — non lancé, règle écrite d'avance dans le protocole.

**(c) Série ordonnée par CN MTAP — NON, la chaîne ne réapparaît pas.** Construction `build_fluxes_tcga_v4_mtap.py` (SHA `38346e16…34ef`) : mêmes 12 flux v4 (`pdac_tcga_fluxes_v4.csv`, SHA `e7a2adab…a0b0`), contrôle = CN MTAP continue GISTIC (`all_data_by_genes.txt`, log2 ratio ; tarball `data/tcga_paad_gistic.tar.gz`, MD5 `816034f7…04d5` revérifié), tri croissant (perte profonde d'abord). Le seuillé (−2…+2) n'a servi qu'en contrôle de cohérence (trop de ties : 46/66/69/2/1 sur 184 échantillons). **Vérification de reproduction passée : les 12 flux v4 recalculés depuis la matrice Firehose (`data/tcga_paad_rsem.tar.gz`, MD5 `b09569ce…ac0a`) reproduisent le CSV v4 à 1,776e-15 près (atol 1e-9)**, comme au test A. Appariement : **177/178** tumeurs — TCGA-FB-A4P6-01 n'a pas d'échantillon GISTIC (7 échantillons GISTIC sans RSEM dans l'autre sens) ; la série utilise les 177 appariées, comme le prévoyait le protocole. CN MTAP sur les 177 : min −1,293, médiane −0,181, max +1,922 ; seuillé −2 : 43, −1 : 62, 0 : 69, +1 : 2, +2 : 1. Les 12 plus délétées sont toutes seuillées −2 (CN −1,293 à −1,111). **La perte de MTAP suit KRAS en pente douce : Spearman CN MTAP contre rang KRAS −0,309 (p=2,9e-05)** — mais les extrêmes diffèrent : recouvrement top-12 MTAP/KRAS 1/12, comme pour la prolifération (§8.34). Séries `pdac_tcga_fluxes_v4_mtap.csv` (SHA `578b8d3b…90df6`) et nul `…_mtap_nul.csv` (SHA `e6786a47…53b9`, lignes permutées, graine 42, contrôle intact) ; MTAPCN en 1re colonne — pas un flux, donc **pas de doublon** (défaut des rotations §8.32 explicitement évité). Provenance complète `PROVENANCE_mtap_series.md` (SHA `5fed7231…872e`). 2 runs v6.1 fast, exit 0/0, 36 fichiers chacun, journal `runs_v61_mtap.log` (FIN 2026-11-18T21:18:51Z, terminés=2, échecs=0). Incident rapporté honnêtement : le 1er lancement (systemd-run, 21h10 UTC) a été tué ~1 min après par un redémarrage du service ; la surveillance systemd-run a relancé, le cron filet (toutes les 15 min) n'a pas eu à intervenir, la surveillance s'est arrêtée d'elle-même à 2/2 et le cron a été supprimé. Aucun dossier de run supprimé, aucun CSV modifié. Lecture : `mtap_reading.py` (SHA `9b1efc08…fcbe`), données `mtap_direct_tests.csv` (SHA `ef55df26…7fa8`) et `mtap_extract.json` (SHA `ab03ad40…69b3`).

**Le pipeline ne sépare pas réel et nul, ici non plus.** Réel : cascade 0,54 / 60,74 / **72,77** / 92,11 / 92,11 % (pas 1/107/**128**/162/162) ; MC best 0,3512 (seuil 69,57 %) ; Delta 3,805 ; L7a DOWN 0,423 ; falsification 0,733 ; L7b FRAGILE ; régime divergence. Nul : cascade 1,07 / 2,14 / **8,57** / 15,58 / 15,58 % (pas 2/4/**15**/27/27) ; MC best **0,5153** (plus haut que le réel) ; Delta **4,347** (plus haut que le réel) ; L7a UP 0,331 ; falsification **0,816** (plus haute que le réel) ; L7b FRAGILE. **MC, Delta et falsification sont tous meilleurs au nul** — le critère écrit d'avance (séparation sur position du seuil ET sens L7a) n'est pas rempli. Deux pistes seulement, pas des preuves (aucun seuil de séparation n'était pré-enregistré) : max_separation favorise le réel (0,339 contre 0,143 — comme à la Phase 2, où c'était l'indicateur le plus cohérent, 6/8) et L7a vote en sens opposé (DOWN 0,423 réel contre UP 0,331 nul — comme au test A). Le T_0 réel tombe au pas 128, à CN MTAP −0,026 — pratiquement à la diploïdie, pas dans la zone délétée : le « seuil » du pipeline n'est pas une frontière de délétion. Bruit : « proxy de variance modéré » des deux côtés (0,688 réel, 0,672 nul). F1/F2 « Tous » : les rapports après/avant montent des deux côtés (F1 ×2,65 réel contre ×11,10 nul ; F2 ×5,33 contre ×13,37) et le signe de F1 change chez 23/29 estimateurs réels contre 27/29 nuls — aucune direction cohérente.

**Tests directs top-12 contre reste (d de Cohen ; + = plus haut chez les 12 tumeurs les plus délétées en MTAP ; mêmes unités que §8.4/§8.34).** Réel : CEACAM5 **+0,585** (d +0,59), REG4 +0,238, MUC17 +0,185, GSTM1 +0,063, CLDN18 +0,012, CLCA1 −0,010, MUC2 −0,026, DPCR1 −0,078, MUC16 **−0,143**, KRT20 −0,146, PGC **−0,399**, CR2 −0,570. Nul : |d| ≤ 0,55 partout (GSTM1 −0,55, KRT20 −0,25) — la baisse de PGC (−0,40) et de CR2 (−0,57) est dans le bruit du nul ; seule la hausse de CEACAM5 (+0,59) dépasse à peine le maximum du nul. Référence KRAS (§8.4) : PGC −0,89, DPCR1 −0,85, CLDN18 −0,46, MUC16 +0,64 — **aucun des quatre ne se retrouve ici** : le bloc ne s'effondre pas et MUC16 ne monte pas chez les plus délétées. **Le long de l'axe, en revanche, plusieurs flux montent doucement quand MTAP se perd** (Spearman flux contre rang — le rang monte avec CN MTAP, donc un rho négatif = plus haut chez les délétées) : CEACAM5 −0,390, CLDN18 −0,270, MUC16 −0,270, DPCR1 −0,262, MUC17 −0,219, REG4 −0,181 (nuls |rho| ≤ 0,10). Des pentes graduelles, pas des sauts : MUC16 a rho −0,270 mais top-12 −0,14 — comme au test A (MUC16 rho +0,277, top-12 −0,04), la pente ne se concentre pas aux extrêmes. Autour de T_0 (pas 128, fenêtres ±20) : la plupart des flux baissent après le seuil (MUC2 −0,88, CLCA1 −0,85, REG4 −0,70, GSTM1 −0,64, KRT20 −0,48) — mais le nul autour de son T_0 (pas 15) montre aussi |d| jusqu'à 0,71 (REG4 −0,71, GSTM1 +0,66, signes mêlés) : pas distinctif.

**Ce que ça change.** La chaîne (bloc qui chute + MUC16 qui monte) est confirmée comme propre à l'axe KRAS : elle ne réapparaît ni sous les 48 contrôles du §8.32, ni sous l'ordre prolifération (§8.34), ni sous l'ordre MTAP. La perte de MTAP accompagne KRAS en pente douce (rho −0,31) sans porter la coupure — cohérent avec le §8.26 (délétion MTAP non significativement enrichie chez les KRAS-forts, p=0,073) : MTAP et KRAS varient ensemble, mais l'axe MTAP n'ordonne pas la rupture estomac/mucus. Côté lignées, le statut mutationnel n'ajoute rien au-delà de MTAP : TP53 et SMAD4 ne déplacent aucune dépendance, et l'effet apparent de CDKN2A sur PRMT5 s'efface dès qu'on fixe MTAP — troisième confirmation indépendante que l'effet PRMT5 suit MTAP (§8.28/§8.29, puis ici). Ce qui reste ouvert : la série par stade TCGA (protocole C du brouillon `PROTOCOL_enrichissements_833_DRAFT.md`, go à demander — avec la réserve de méthode : le stade est une variable de résultat clinique, pas un axe neutre) ; la publication finale (PDF + GitHub) après le go de Zackary. L'étape 4 est terminée : les 4 propositions du 18 nov. 15h06 sont faites (test A, Phase 2, PDF, enrichissements) — seules les poussées GitHub de l'étape 3 restent à retenter à la publication finale.

### 8.37 v6.2 : hachage stable L5, score S_sep, élucidation de Delta (18–19 nov. 2026)

Date : 18–19 novembre 2026. Go de Zackary : 18 nov. 18h07 (construire et
valider la v6.2, protocole gelé `PROTOCOL_v6.2.md`, SHA
`6e9324a2f2ff0720c6dd23d403a281e7f15bf5c7b4a8d04f8bba41ed7f84dfad`).
Travail exécuté en sous-agent : étapes 3 (validation) et 4 (discrimination)
+ élucidation de Delta. **Adoption : faite le 19 nov. 2026, ~05h47, sur le
go de Zackary (« Lance tout cela ») — la v6.2 devient la version de travail,
la v6.1 devient la référence, la v6 reste la référence historique (voir
§8.37.5 et journal §10).** PDF régénéré et poussée GitHub dans le nouveau
dépôt `tlogNext-cancer-pdac` : voir journal §10.

**Verdict d'abord, en trois phrases.**

1. **Validation : réussie.** La gigue L5 est bien 0 entre deux répétitions
   (10 runs × 2, tous les indicateurs à 0,0000), les cascades sont identiques
   à la v6.1 sur 10/10, les L7a des petites cohortes sont finis.
2. **Discrimination : S_sep atteint la barre (6/8), mais la v6.2 ne sépare
   pas mieux que la v6.1.** S_sep fait 6/8 sur les paires principales et
   16/23 en annexe — exactement le score de max_separation en v6.1, mêmes
   paires. Tous les écarts réel−nul sont identiques à ceux de la v6.1 au
   chiffre près.
3. **Delta : non élucidé.** La meilleure variable nommée (masque + MFA + n)
   prédit la paire médiane à 80,2 % et la valeur à 61,7 % — loin des 90 %
   exigés. Delta reste une piste fragile et ne devient pas un
   discriminateur recommandé.

**8.37.1 Construction de la v6.2 (rappel, détail dans `PROVENANCE_v6.2.md`).**

Un seul changement de code par rapport à la v6.1, construit par script
(`build_v6.2.py`, SHA `5348636e0633b2b25a418bfa162adbec9277025fff72565f4bfb2c6efd951fa0`) :

- `import hashlib` ajouté (ligne 392) ;
- ligne 8985 (8986 après l'import) : `int(seed) + (hash(metric) % 1000)`
  remplacé par `int(seed) + (int.from_bytes(hashlib.sha256(metric.encode('utf-8')).digest()[:8], 'little') % 1000)` —
  la graine MC de L5 ne dépend plus du hachage Python, aléatoire par processus ;
- `VERSION_MASTER` : `v6.2.0-L7aL7b-CohenD-short` (+ note d'en-tête).

Vérifications de construction : `grep "hash("` = 0 occurrence, `grep
"hashlib"` = 2 occurrences, `python3 -m py_compile` exit 0, `diff -u`
v6.1 → v6.2 = exactement 3 hunks. Incident consigné : la première
construction s'est arrêtée sur assertion parce que la note d'en-tête
contenait elle-même la chaîne littérale `hash(metric)` ; note reformulée,
construction relancée proprement. SHA-256 : v6.2
`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
(624 157 octets) ; v6.1 source
`2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`
(623 495 octets) ; v6
`bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`
(622 526 octets), revérifiée inchangée après travaux. S_sep et
l'élucidation Delta sont des lectures hors pipeline — aucun code pour ça
dans la v6.2.

**8.37.2 Validation (§5 du protocole) — 20/20, gigue 0.**

Lanceur reprenable `run_v62_lot.sh` + `manifest_v62_validation.txt`,
surveillé par `watch_v62_validation.sh` (systemd-run). Log :
`runs_v62_validation.log`. Extraction : `extract_v62_validation.py`.
Table complète : `v62_validation_table.md` (+ `.json`).

- **20/20 runs exit 0** (10 runs fast, réel + nul, chacun lancé 2 fois dans
  des processus séparés). Trois redémarrages machine pendant les lots
  (18 nov. ~23h25 UTC et 19 nov. ~00h05 UTC pendant la validation, 19 nov.
  ~02h05 UTC pendant la phase 2) : le lanceur a repris là où il s'était
  arrêté ; les runs partiels tués (TCGA v4 réel, DepMap nul rep2, V4R_CLDN18
  nul) ont été refaits proprement, les runs complets conservés.
- **Cascades identiques à la v6.1 : 10/10.** HP35 réel : valeurs brutes du
  contrôle [0, 16, 90, 376, 376] (celles du protocole §5.3) ; TCGA v4 réel
  0,00 / 74,06 / 93,22 / 98,44 / 98,96.
- **L7a fini sur les petites cohortes** : GSE62452 (n=69) down 0,197, ICGC
  (n=70) up 0,181, DepMap (n=45) down 0,196 — votes finis, strictement
  identiques à la v6.1. Pas de faux « up » / 0,50.
- **Gigue mesurée = 0,0000 sur tous les indicateurs** (max |rép1 − rép2|
  sur les 10 runs) : MC best_score, max_separation, stability, S_sep,
  Delta, falsification, L4 risk, L5 confidence, L5 stability, L7a
  (confiance signée), cascade. L5, L4 et L7a sont identiques entre
  répétitions sur 10/10.
- **Nuance honnête sur l'octet-pour-octet (§5.2, repli documenté)** : les
  `master_results.json` ne sont PAS identiques octet pour octet entre
  répétitions (0/10). La comparaison champ par champ (NaN-aware) montre
  que les seules divergences sont (1) les deux chemins
  `/runtime/dashboard_status/path` et `/runtime/telemetry_path` — ils
  contiennent le nom du dossier de sortie, qui diffère par construction
  (`_rep2`) ; (2) les champs `worker_budget` (RAM libre, `memory_cap`,
  `chosen`, `safe_cap`, `n_workers`, `chunksize`) — ils reflètent la RAM
  libre au lancement, qui a varié entre les redémarrages. **Aucun champ
  scientifique ne diffère sur les 10 runs (0 divergence « autre »).**
  Aucune clé d'horodatage exacte (`timestamp`, `date`, `generated_at`,
  `run_date`, `created_at`) dans aucun JSON (10/10) — une première version
  du contrôle comptait à tort « candidate » comme une date (sous-chaîne),
  corrigée en contrôle par nom exact.
- **Petit mouvement attendu, sans conséquence** : la graine L5 stable
  change légèrement les alertes L5, donc le vote L7a bouge un peu sur les
  grandes séries (HP35 réel up 0,378 contre 0,377 en v6.1 ; TCGA v4 réel
  down 0,405, inchangé à 0,001 près). Directions inchangées partout ;
  petites cohortes strictement identiques.
- **Verdict §5.3 : validation réussie.** Gigue effective S_sep pour la
  phase 2 : max(0,00 mesurée ; 0,07 plancher) = **0,07**.

**8.37.3 Test de discrimination (§6) — S_sep 6/8, pareil que la v6.1.**

Extracteur : `extract_phase2_v62.py` (copie de `extract_phase2.py`,
étendue du 9e indicateur, mêmes règles de comptage, fonction `verdict()`
inchangée). Table complète : `v62_phase2_table.md` (+ `.csv`, `.json`).
46 runs phase 2 (6 paires principales restantes + 40 secondaires), tous
exit 0, log `runs_v62_phase2.log`. Aucun nouveau run au-delà du §5 sauf
les paires restantes, comme le protocole l'autorise.

**Gigues appliquées** (mesurées en validation, §6) : MC 0,00 ; max_separation
0,00 ; L7a 0,00 ; S_sep 0,07 (plancher) ; Delta / cascade / falsification 0.
En v6.1, MC, max_separation et L7a utilisaient le forfait ±0,07. Ce
changement de règle — pas de changement de l'instrument — explique tous
les compteurs qui montent (voir ci-dessous).

**S_sep = max_separation × stability (§3.1), paires principales :**

| Paire | S_sep réel | S_sep nul | Écart | Sépare ? |
|---|---|---|---|---|
| HP35 | 1,5391 | 0,1185 | +1,4206 | oui |
| TCGA v4 | 0,4548 | 0,1688 | +0,2860 | oui |
| GSE71729 | 0,2579 | 0,2174 | +0,0405 | non (< 0,07) |
| GSE62452 | 0,3044 | 0,3116 | −0,0072 | non |
| ICGC | 0,4034 | 0,3073 | +0,0960 | oui |
| Immunitaire TCGA | 0,5263 | 0,1604 | +0,3659 | oui |
| PARP TCGA | 0,3667 | 0,1987 | +0,1680 | oui |
| DepMap | 0,4339 | 0,2524 | +0,1815 | oui |

**« S_sep sépare sur 6/8 : [HP35, TCGA v4, ICGC, immunitaire TCGA, PARP
TCGA, DepMap], échoue sur [GSE71729, GSE62452]. »** La barre ≥ 6/8 (§3.4)
est atteinte, exactement.

**Par bras (v6.2 contre v6.1, indicateur par indicateur) :**

- **TCGA v4** : sépare par S_sep (+0,286), max_separation (+0,293), Delta
  (+0,42) et MC (+0,045, avec gigue 0). Comme en v6.1, en mieux compté.
- **Immunitaire TCGA** : sépare par S_sep (+0,366), max_separation
  (+0,368), Delta (+1,91, le plus gros écart PDAC) et MC (+0,055). Comme
  en v6.1.
- **PARP TCGA** : sépare par S_sep (+0,168), max_separation (+0,169),
  Delta (+0,26) et MC (+0,024). Comme en v6.1.
- **DepMap (n=45)** : sépare par S_sep (+0,182), max_separation (+0,190),
  Delta (+0,24) et MC (+0,012). Comme en v6.1 — le MC ne dépassait pas
  0,07, il dépasse 0.
- **HP35 (témoin positif)** : S_sep écrase (+1,421), MC (+0,195) et
  max_separation (+1,651) séparent ; Delta échoue (−0,09, nul devant),
  comme en v6.1.
- **GSE71729 et GSE62452** : les deux échecs de S_sep, comme ceux de
  max_separation en v6.1. GSE71729 : S_sep +0,041 (< 0,07) mais
  max_separation +0,040 passe avec gigue 0 ; GSE62452 est plat partout
  (S_sep −0,007, max_separation −0,004, MC −0,003).

**Verdicts par indicateur (principales, v6.2 contre v6.1) :**

| Indicateur | v6.2 | v6.1 |
|---|---|---|
| Delta | 6/8 | 6/8, mêmes paires |
| MC best_score | 7/8 | 1/8 |
| max_separation | 7/8 | 6/8 |
| S_sep | 6/8 | — (nouveau ; prévu 6/8 au §3.3) |
| T_0 | 8/8 — trivial | 8/8 — trivial |
| Falsification | 4/5 disponibles | 4/5, mêmes paires |
| Cohérence par flux (fraction) | 2/8 | 2/8 |
| \|d\| médian à T_0 | 6/8 | 6/8 |
| L7a | 4/8, direction négative | 4/8, mêmes paires |
| Écart cascade | 8/8 — trivial | 8/8 — trivial |

**Annexe (23 paires secondaires)** : Delta 13/23 (v6.1 : 13/23) ; MC 18/23
(v6.1 : 2/23) ; max_separation 20/23 (v6.1 : 16/23) ; S_sep **16/23** ;
T_0 23/23 ; falsification 7/18, direction inversée (v6.1 : 7/18) ;
cohérence 8/22 (v6.1 : 8/22) ; L7a 13/23 (v6.1 : 12/23 — V4R_CLDN18,
écart −0,002, compte avec gigue 0) ; cascade 23/23.

**Ce qu'il faut retenir, sans arrondir :** la v6.2 ne sépare pas mieux que
la v6.1. Tous les écarts réel−nul sont identiques à ceux de la v6.1 au
chiffre près, sauf les écarts L7a signés (mouvements ≤ 0,031, verdicts
inchangés) et le nouvel indicateur S_sep. S_sep (6/8, 16/23) reproduit
exactement max_separation en v6.1 (6/8, 16/23) parce que la stabilité est
quasi saturée (~0,98–1,00) sur toutes les paires PDAC — S_sep ≈
max_separation, et le garde-fou anti-pic-bruité ne s'est pas déclenché
ici. Les seuls compteurs qui montent (MC 1/8 → 7/8, max_separation 6/8 →
7/8, 2/23 → 18/23 et 16/23 → 20/23 en annexe) montent parce que la gigue
appliquée est passée de 0,07 (forfait historique) à 0,00 (mesurée en
validation, comme le protocole §6 l'ordonne). Avec le forfait 0,07, les
verdicts v6.2 seraient exactement ceux de la v6.1. La v6.2 apporte le
déterminisme (gigue 0), pas une meilleure séparation.

**8.37.4 Élucidation de Delta (§4) — non élucidé.**

Script externe `extract_delta_levels.py`, lecture seule, 222 runs
(156 v6.1 + 66 v6.2). Table complète : `v62_delta_elucidation.md` (+
`v62_delta_levels.csv` / `.json`, log `v62_delta_extract.log`).

- **Identités vérifiées 222/222** : d_div = moyenne des 3e et 4e médianes
  divergence triées (0 écart) ; d_sat = 4e médiane saturation triée
  (0 écart). Le mécanisme est connu : d_div est entièrement déterminé par
  l'identité de la paire médiane (3e/4e) et leurs valeurs (reconstruction
  à ±0,10 sur 222/222 — identité de construction, pas une prédiction).
- **Ce qui choisit la paire reste indéterminé.** Taux de prédiction
  (paire / valeur à ±0,10, majorité dans le groupe pour la paire,
  moyenne du groupe pour la valeur) :
  - H1 masque (Levina/PH absents) : 60,8 % / 14,9 % ;
  - H2 MFA (9 valeurs distinctes : 3,0 ; 4,0 ; 4,5 ; 5,0 ; 6,0 ; 6,25 ;
    6,5 ; 6,75 ; 7,0) : 62,2 % / 36,0 % ;
  - H3 n : 63,1 % / 56,3 % ; n_fluxes seul : 46,8 % / 8,1 % ;
  - H4 robustness : corrélation Pearson avec d_div +0,197 — faible,
    infirmée comme prédicteur seul (les quartiles mélangent toutes les
    paires) ;
  - H5 contrôle : 68,0 % / 32,9 % seul, 74,3 % / 36,5 % avec le masque ;
  - **meilleure combinaison (masque + MFA + n) : 80,2 % / 61,7 %**
    (v6.2 seuls : 86,4 % / 78,8 %, n=66) — **sous les 90 % exigés**.
- **Corrélations avec d_div** (Pearson, 222 runs) : LocalPCA +0,968 ;
  MFA +0,968 ; GraphDimension +0,864 ; LevinaBickel +0,807 ;
  PersistentHomology +0,796 ; PCAIntrinsic +0,708 ; sharpness +0,227 ;
  robustness +0,197 ; max_separation +0,187 ; stability +0,031. Une
  corrélation n'est pas une prédiction de la paire.
- **H7 (d_sat quasi constant)** : d_sat moyenne 1,520 ± 0,124
  (min 1,184, max 1,656) ; 4e membre dominant : Hurst2mH (126 runs),
  DFA (72), Katz (22), BoxCounting (2). Par n : n=45 → 1,240 ± 0,078
  (4e = Katz) ; n=178 → 1,580 ± 0,022 (4e = Hurst2mH) ; n=515 → 1,652.
  Delta ≈ d_div − constante par famille, mais la constante change avec n.
- **Anomalie DFA = −38,16, retrouvée et classée** : 22 runs avec DFA <
  −10 (dont −38,1597 sur `results_fast_v61_depmaprot_aco2_nul`, celui du
  protocole §4.2 ; DepMap v6.2 : −18,5768, rep1 et rep2 identiques). Sur
  les 22, DFA est toujours la 1re valeur triée (la plus basse) de la
  saturation — jamais la 4e, donc jamais la médiane : d_sat vaut alors
  Katz (~1,19) et Delta n'est pas touché. Les DFA extrêmes se concentrent
  sur DepMap et ses rotations protéines (n=45).
- **Verdict §4.4 : NON ÉLUCIDÉ.** Delta garde son statut de piste fragile
  (6/8 en phase 2, 13/23 en annexe, échec sur HP35) et ne devient pas un
  discriminateur recommandé.

**8.37.5 Ce qui change, ce qui ne change pas, et la suite.**

- **Ce qui change avec la v6.2** : le déterminisme. La gigue L5 mesurée
  passe de ±0,07 (v6.1, hachage Python aléatoire par processus) à 0. Les
  répétitions d'un même run donnent les mêmes L5, L4, L7a, MC, Delta et
  cascades. C'est la seule chose que la v6.2 démontre de mieux que la v6.1.
- **Ce qui ne change pas** : aucun écart réel−nul (sauf L7a à ≤ 0,031
  près), aucune cascade, aucun Delta, aucun score MC. S_sep atteint la
  barre ≥ 6/8 mais n'apporte rien au-delà de max_separation sur ces
  séries — la stabilité ne discrimine pas ici.
- **Adoption** : **faite le 19 nov. 2026, ~05h47, sur le go de Zackary
  (« Lance tout cela », feu vert pour les 3 chantiers : adoption v6.2, PDF,
  GitHub). La v6.2 devient la version de travail ; la v6.1 devient la
  référence ; la v6.0.0 reste intacte comme référence historique.** Tous les
  runs PDAC suivants utilisent la v6.2. Les trois SHA ont été revérifiés
  inchangés le 19 nov. 2026 avant adoption (v6 `bb8bbdba…c0773`, v6.1
  `2af5e5ce…c1c9`, v6.2 `f07567c4…ec3abf` — complets en provenance §8.37) ;
  aucun des trois codes n'a été modifié. Ce qui ne change pas avec
  l'adoption : la v6.2 ne sépare pas mieux que la v6.1 (voir §8.37.3) — le
  gain adopté est le déterminisme (gigue L5 = 0), pas une meilleure
  séparation.
- **Limites nommées** : les gigues mesurées (0) rendent le critère
  « écart > gigue » trivial pour MC, max_separation et L7a (tout écart non
  nul passe) — les 7/8 de MC et de max_separation doivent se lire avec
  cette réserve, et le forfait historique ±0,07 reste l'échelle de
  lisibilité du projet pour juger si un écart est gros. T_0 et l'écart
  cascade restent triviaux par construction (8/8 ne prouve rien). La
  falsification reste une comparaison interne, pas au nul permuté, et
  indisponible sous n = 75.

**Provenance (§8.37).**

- **Protocole gelé** : `PROTOCOL_v6.2.md`, SHA-256
  `6e9324a2f2ff0720c6dd23d403a281e7f15bf5c7b4a8d04f8bba41ed7f84dfad`
  (l'annonce `fb27b39a…` de l'auteur du protocole ne correspond pas au
  fichier ; le SHA mesuré fait foi, voir `PROVENANCE_v6.2.md` §2).
- **Pipelines** : v6.2 SHA
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` ;
  v6.1 SHA `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ;
  v6 SHA `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`.
  Aucune des trois n'a été modifiée pendant ce travail.
- **Entrées (paires principales, SHA-256, fichiers inchangés depuis la
  phase 2)** : HP35 réel
  `6b656540598579a37cbc97c9dfbee26bf6186611f84f397cf9e7e6f1e88bb35e`,
  HP35 nul
  `ad669e51a8b783fdae3f0f68020cf56871e3a620b7857d4adc96d73ab015e947` ;
  TCGA v4 réel
  `e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0`,
  nul
  `895a456295d2b0553a2a62910461aedecb1aeccca59f57751c87b75ce0b97da4` ;
  GSE71729 réel
  `7d69fa888f15e9a1a128e149e35f9eeacac106198c33929dfc51e113ee8c0cf1`,
  nul
  `13b1ac801faccfa1410382d329625a4d65ed8e1ed26e03f2331c73ca66f246ec` ;
  GSE62452 réel
  `d7419c0ec3ed649d98ba920411ef5f41a056caa69b38c6b9a5e3ab702cc03abf`,
  nul
  `d396e5f58cfadbc37171a2d9015941be9807c6e53f31753ccaded0761f71502d` ;
  ICGC réel
  `710d41e55d32360b95f81113579eac4b6de023130b77410bd9ac3df906b61941`,
  nul
  `e020a2c4a7950692ae0e08353db411ceec9b90f564e1f618fc19ef49a065f25e` ;
  immunitaire TCGA réel
  `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e`,
  nul
  `9100d181e3391d558eec6bc97e82f93b16c118b807b4a5f0c0992f4bda51a405` ;
  PARP TCGA réel
  `c9549b68280b2f4ca3d9b62020efa21ab97249b10e176de87ec528a0258c4309`,
  nul
  `57245c728dacf264654f77a4b4d6d608bbe3fb8c300b287061063bd062ab1360` ;
  DepMap réel
  `7d605fefb412fe16151a1b2508dffa6a1c2b8353600dccffd4af3333198e37f8`,
  nul
  `ac2e0db558ad2e2c4bf9240b8fab0d0c2125e9890212034a6f3b6a9f08326c80`.
  Les 23 paires secondaires utilisent les mêmes CSV que la phase 2 v6.1
  (voir `manifest_v62_phase2.txt`).
- **Nature des lignes** : les CSV d'entrée sont des flux numériques
  dérivés de mesures instrumentales (ARN tumoral et cellulaire, protéine
  tumorale, dépendance CRISPR) — voir les `PROVENANCE_*.md` par série ;
  les nuls sont des lignes permutées (graine 42, colonne de contrôle
  intacte), c'est-à-dire des échantillons construits, pas des mesures.
  Aucun mot humain, aucun échantillon hypothétique d'une autre nature.
- **Runs** : 66 runs v6.2 (20 validation + 46 phase 2), tous exit 0 ;
  222 runs analysés pour Delta (156 v6.1 + 66 v6.2). Commandes : mode
  `fast`, `--seed 42` (défaut), lanceurs `run_v62_lot.sh` (reprenable,
  saute les sorties complètes), manifestes `manifest_v62_validation.txt`
  et `manifest_v62_phase2.txt`, surveillances `watch_v62_validation.sh`
  et `watch_v62_phase2.sh` (systemd-run).
- **Fichiers de ce §8.37** : `v62_validation_table.md` (+ `.json`,
  `v62_validation_extract.log`), `v62_phase2_table.md` (+ `.csv`,
  `.json`, `v62_phase2_extract.log`), `v62_delta_elucidation.md` (+
  `v62_delta_levels.csv` / `.json`, `v62_delta_extract.log`),
  `extract_v62_validation.py`, `extract_phase2_v62.py`
  (SHA `f7c8893885cc3de437bfabdff67b657c0cb2a79877fc2fe0691cddc5e39fc693`),
  `extract_delta_levels.py`
  (SHA `48f4c8859e7a76b1d152558874d7a1376a781e9830d35ac33439f2df8f637284`),
  `PROVENANCE_v6.2.md`, logs `runs_v62_validation.log` et
  `runs_v62_phase2.log` — tous dans `~/workspace/runs/pdac-v6/`.
- **Ce qui manque** : **la poussée GitHub.** Adoption faite le 19 nov. 2026
  (~05h47, go « Lance tout cela ») et PDF régénéré le 19 nov. 2026 avec
  ce §8.37 — mais la poussée GitHub dans le nouveau dépôt
  `FindPrint/tlogNext-cancer-pdac` n'a PAS eu lieu : l'approbation
  d'écriture a expiré sans réponse après ~30 min d'attente
  (`approval_expired`, 19 nov. 2026, approval_id
  `connector-attempt-a6d281f83b6bb0a4878e3f5593c007415af7b191885e3d5ca50422fba2dd1f7f`)
  ; rien n'a été poussé, rien n'a changé sur GitHub (tête distante
  vérifiée inchangée, `baf1e02f`, commit initial). Snapshot prêt et
  vérifié (8 fichiers, 991 746 octets, UTF-8 : livre blanc, PROTOCOL_v6.2,
  PROVENANCE_v6.2, build_v6.2, 3 tables v6.2, code v6.2) — à retenter
  après une nouvelle approbation de Zackary, sans relancer en boucle.
  La machine a redémarré trois fois pendant les lots ; rien n'a été perdu
  (reprise par le lanceur), mais les champs `worker_budget` des JSON en
  portent la trace (voir §8.37.2).

### 8.38 S_sep appliqué aux bras existants (19 novembre 2026)

Date : 19 novembre 2026. Go : Zackary, « Lance tout cela », 19 nov. 2026 ~05h47.

**Verdict d'abord**

**S_sep ne classe aucun bras autrement que max_separation en v6.1.**
Sur les 29 paires distinctes relues (8 principales + 20 secondaires
distinctes + MTAP ; l'annexe compte 23 lignes dont 3 doublons des
paires principales),
S_sep en v6.2 est **identique à S_sep en v6.1 au chiffre près**
(max |Δ| = 0,0000 sur S_sep, max_separation, MC et Delta) : le hachage
stable L5 ne touche pas ces champs, comme le prévoyait le protocole §2.3.
La seule chose qui change un compteur, c'est la règle de gigue — et elle
change max_separation exactement pareil :

| Règle | S_sep, paires principales | max_separation, même règle |
|---|---|---|
| (A) gelée §3.4 : écart > 0,07 | **6/8** : HP35, TCGA v4, ICGC, immunitaire TCGA, PARP TCGA, DepMap ; échecs GSE71729 (+0,0405), GSE62452 (−0,0072) | v6.1 : 6/8, **mêmes paires** |
| (B) gigue 0 : écart > 0 | **7/8** : + GSE71729 ; échec GSE62452 seul | v6.2 : 7/8, **mêmes paires** |

En annexe (23 paires) : S_sep (A) **16/23**, exactement max_separation v6.1
(16/23, mêmes paires) ; S_sep (B) **20/23**, exactement max_separation v6.2
à gigue 0 (20/23, mêmes paires).

**Réserve explicite, à garder avec le chiffre : le passage de 6/8 à 7/8
(et de 16/23 à 20/23) vient uniquement du passage de la gigue appliquée
de 0,07 à 0,00. Les écarts réel−nul eux-mêmes sont identiques à ceux de
la v6.1 au chiffre près. Ce n'est pas une amélioration de l'instrument —
c'est le même écart mesuré contre un seuil devenu nul.** Le plancher 0,07
du protocole (§3.4) existe précisément pour que « écart > 0 » ne devienne
pas trivial ; la règle (B) est rapportée ici à la demande du chantier,
elle ne remplace pas la règle gelée (A).

Verdict par bras (détail au §8.38.2) :

| Bras | Paires | S_sep (A) 0,07 | S_sep (B) gigue 0 | Classe autrement que v6.1 ? |
|---|---|---|---|---|
| ATR | ATR_TCGA | passe (+0,2262) | passe | **Non** — identique à max_sep v6.1 (+0,2262, passait) |
| MTAP | MTAP (TCGA v4 ordonnée par CN MTAP) | passe (+0,1968) | passe | **Non** sur S_sep — mais MC (−0,1642) et Delta (−0,5416) restent inversés : bras contrasté, verdict §8.36 non renversé |
| Immunitaire | TCGA, GSE62452, GSE71729, ICGC | 3/4 passent ; ICGC inversé (−0,2200) | 3/4 passent ; ICGC inversé | **Non** — identique à max_sep v6.1 sur les 4 |
| PARP | TCGA, GSE71729 | 2/2 passent | 2/2 passent | **Non** — identique à max_sep v6.1 sur les 2 |
| Principales (Phase 2) | 8 paires | 6/8 | 7/8 | **Non** — identique à max_sep sous chaque règle |

**8.38.1 Question, méthode, règles**

**Question.** S_sep (formule gelée, PROTOCOL_v6.2.md §3 :
`S_sep = max_separation × stability`, lus dans le `best_config` de chaque
run) classe-t-il les pistes autrement que la v6.1, quand on le réapplique
aux bras déjà faits — ATR, MTAP, immunitaire, PARP — et aux paires
principales de la Phase 2 ?

**Méthode — relecture, pas recopie.** Toutes les valeurs ci-dessous ont été
relues dans les `master_results.json` par un extracteur indépendant,
`extract_ssep_838.py` (SHA-256
`d7b8bd663fb36340779ebb4d7ce307775d4e9896afee4a75236192cf026bb14a`),
écrit pour ce chantier ; les tables existantes n'ont servi que de
comparaison. Résultat de la comparaison :

- **0 écart** entre les valeurs relues et `v62_phase2_table.json`
  (max_separation, stabilité, S_sep, MC, Delta, L7a — 29 paires, tolérance
  10⁻⁶) ;
- **0 écart** entre les valeurs v6.1 relues et `v61_phase2_table.csv`
  (champs comparables, tolérance 5×10⁻⁵, le CSV étant arrondi) ;
- **S_sep v62 = S_sep v61 exactement sur 29/29 paires comparées**
  (max |Δ| = 0,0000) ; max_separation, MC et Delta aussi (0,0000).
  Seul le L7a signé bouge entre v6.1 et v6.2 (max 0,0304, sur TCGA_V2 ;
  ≤ 0,0041 partout ailleurs) — effet attendu du hachage stable L5 sur
  les votes, sans changement de verdict L7a sur les paires principales
  (4/8 inchangé).

**Règles de comptage.** Direction majoritaire = signe de la somme des
écarts réel−nul (comme `verdict()` de `extract_phase2.py`) ; une paire
« sépare » si |écart| > gigue ET signe = direction majoritaire. Deux
gigues sont appliquées et distinguées partout : **(A)** la règle gelée
§3.4, gigue effective = max(gigue mesurée 0,00 ; plancher 0,07) = **0,07** ;
**(B)** la gigue mesurée seule, **0,00** (commande de ce chantier), rapportée
à part avec la réserve ci-dessus. Nul : lignes permutées, graine 42,
colonne de contrôle intacte (convention du projet). Aucun nouveau seuil,
aucune sélection d'indicateur après coup.

**Nouveaux runs — un seul bras en demandait.** ATR, immunitaire et PARP
avaient déjà leurs runs v6.2 dans le lot phase 2 (66 dossiers). MTAP
n'y était pas : seuls les runs v6.1 existaient (`results_fast_v61_mtap`,
`results_fast_v61_mtap_nul`). Deux runs v6.2 ont donc été lancés pour ce
chantier, avec les CSV et le protocole existants, sans modifier aucun code :
manifeste `manifest_v62_mtap.txt`, lanceur reprenable `run_v62_lot.sh`
(existant), surveillance `watch_v62_mtap.sh` (miroir de
`watch_v61_mtap.sh`), unité systemd `v62-mtap-838`, log
`runs_v62_mtap.log` — 19 nov. 2026, 11h27–11h34 UTC, **2/2, exit 0**,
SHA v6.2 `f07567c4…` et SHA v6.1 `2af5e5ce…` confirmés dans le log.
Cascades MTAP v6.2 = v6.1 exactement (réel 0,54 / 60,74 / 72,77 / 92,11 /
92,11 % ; nul 1,07 / 2,14 / 8,57 / 15,58 / 15,58 %), comme l'exigeait le
protocole §5.3.

**8.38.2 Résultats par bras**

Les stabilités sont données parce qu'elles expliquent pourquoi S_sep ≈
max_separation ici (voir §8.38.3). Toutes les valeurs sont S_sep réel /
nul (écart réel−nul), relues dans les JSON v6.2.

**ATR — 1 paire (annexe Phase 2)**

Série TCGA, 178 tumeurs, 12 flux de réparation de l'ADN (PARP1, PARP2,
BRCA1, BRCA2, ATM, ATR, CHEK1, CHEK2, RAD51, XRCC1, POLQ, FANCD2),
lignes ordonnées par résidu KRAS croissant, contrôle `step`
(PROVENANCE_atr_chek1.md).

| Paire | n | S_sep réel / nul | Écart | Stabilité R / N | (A) 0,07 | (B) 0 |
|---|---|---|---|---|---|---|
| ATR_TCGA | 178 | 0,3784 / 0,1522 | **+0,2262** | 0,9968 / 0,9917 | passe | passe |

Contexte, mêmes JSON v6.2 : max_separation +0,2262 (identique à v6.1),
MC +0,0331 (sous 0,07), Delta +0,0944, L7a signé −0,566 (réel down 0,161
contre nul up 0,406). **S_sep ne reclasse pas ATR** : il passait déjà en
max_separation v6.1 sous la gigue 0,07, il passe pareil en S_sep sous les
deux règles. Le bras ATR reste une piste à écart positif net (+0,23),
portée par max_separation/S_sep seuls — MC et Delta ne dépassent pas le
bruit historique sur cette paire.

**MTAP — 1 paire, nouveaux runs v6.2 (§8.36)**

Série TCGA v4 ordonnée par nombre de copies MTAP croissant (perte profonde
d'abord), 177 tumeurs (177/178 appariées), contrôle `MTAPCN`, monotone
croissant (Spearman ordre vs valeur 0,99996). Voir
PROVENANCE_mtap_series.md.

| Paire | n | S_sep réel / nul | Écart | Stabilité R / N | (A) 0,07 | (B) 0 |
|---|---|---|---|---|---|---|
| MTAP | 177 | 0,3378 / 0,1409 | **+0,1968** | 0,9959 / 0,9825 | passe | passe |

Valeurs v6.2 vérifiées : max_separation 0,3392 / 0,1434 (+0,1957),
identiques à la v6.1 au chiffre près, ainsi que MC et Delta. **Mais les
autres indicateurs disent l'inverse, avec de gros écarts : MC 0,3511 /
0,5153 (−0,1642, le nul devant) et Delta 3,8051 / 4,3466 (−0,5416, le nul
devant)** ; L7a signé −0,7579 (réel down 0,427 contre nul up 0,331).
C'est le seul bras où S_sep/max_separation et MC/Delta se contredisent
aussi franchement.

**Lecture honnête : S_sep « sépare » sur MTAP, mais il ne renverse pas le
verdict §8.36 (NON).** Le NON de §8.36 était porté par le MC
(nul 0,515 > réel 0,351) ; ce fait est confirmé en v6.2, au chiffre près,
et Delta l'aggrave (−0,54). Un seul indicateur positif (S_sep, qui est
max_separation pondéré par ~0,99) contre deux indicateurs inversés ne
suffit pas à rouvrir la piste. MTAP reste le cas d'école de ce chantier :
S_sep hérite exactement des forces et des faiblesses de max_separation,
il ne les corrige pas.

**Immunitaire — 4 paires (1 principale + 3 secondaires)**

Séries ordonnées par KRAS croissant, contrôle `step`, 12 flux immunitaires
(CD8A, CD8B, CD4, FOXP3, CD68, CD163, CD274, PDCD1, CTLA4, GZMB, IFNG,
CD19 — sauf ICGC : PRF1 et MS4A1 remplacent IFNG et CD19, voir
PROVENANCE_immune_v6.md).

| Paire | n | S_sep réel / nul | Écart | Stabilité R / N | (A) 0,07 | (B) 0 |
|---|---|---|---|---|---|---|
| IMMUNE_TCGA | 178 | 0,5263 / 0,1604 | **+0,3659** | 0,9914 / 0,9819 | passe | passe |
| IMMUNE_GEO62452 | 69 | 0,4656 / 0,3122 | **+0,1534** | 0,9692 / 0,9899 | passe | passe |
| IMMUNE_GEO71729 | 145 | 0,2900 / 0,1557 | **+0,1343** | 0,9916 / 0,9964 | passe | passe |
| IMMUNE_ICGC | 70 | 0,2289 / 0,4489 | **−0,2200** | 0,9955 / 0,9976 | échoue (inversé) | échoue (inversé) |

Contexte v6.2 : max_separation +0,3675 / +0,1650 / +0,1362 / −0,2200 —
**les mêmes verdicts que S_sep sous les deux règles, et les mêmes que
max_separation v6.1 sous 0,07** (l'annexe v6.1 comptait déjà ces trois
premières parmi ses 16/23). MC : +0,0545 / +0,0217 / +0,0204 / −0,0343
(tous sous 0,07) ; Delta : +1,9142 / −0,0417 / +0,1903 /
+0,1782 ; L7a signé : −0,526 / −0,282 (réel flat 0,280) / −0,562 /
+0,033. **Le bras immunitaire se lit 3/4 en S_sep, avec ICGC inversé de
−0,22 — le nul y sépare plus que le réel.** S_sep n'y change rien par
rapport à la v6.1 : ni la hiérarchie des cohortes, ni l'inversion ICGC,
ni le fait que TCGA porte l'essentiel de l'écart (+0,37 contre +0,13 à
+0,15 ailleurs).

**PARP — 2 paires (1 principale + 1 secondaire)**

Séries ordonnées par expression KRAS croissante, contrôle `step`, mêmes
12 flux de réparation de l'ADN que le bras ATR
(PROVENANCE_parp_v6.md).

| Paire | n | S_sep réel / nul | Écart | Stabilité R / N | (A) 0,07 | (B) 0 |
|---|---|---|---|---|---|---|
| PARP_TCGA | 178 | 0,3667 / 0,1987 | **+0,1680** | 0,9963 / 0,9973 | passe | passe |
| GEO71729_PARP | 145 | 0,3356 / 0,2290 | **+0,1066** | 0,9923 / 0,9921 | passe | passe |

Contexte v6.2 : max_separation +0,1688 / +0,1074 ; MC +0,0244 / +0,0139 ;
Delta +0,2616 / −0,0139 ; L7a signé −0,220 / +0,006. **PARP est le bras
le plus régulier : 2/2 en S_sep sous les deux règles, 2/2 en max_sep
v6.1 sous 0,07.** Rien ne change — ni les écarts, ni leur ordre
(TCGA > GSE71729), ni le fait que MC et Delta restent faibles ou nuls
sur GSE71729.

**Paires principales (Phase 2) — rappel vérifié**

| Paire | n | S_sep réel / nul (v6.2) | Écart | (A) 0,07 | (B) 0 | max_sep v6.1 (0,07) |
|---|---|---|---|---|---|---|
| HP35 | 1000 | 1,5391 / 0,1185 | +1,4206 | passe | passe | passait (+1,6512) |
| TCGA v4 | 178 | 0,4548 / 0,1688 | +0,2860 | passe | passe | passait (+0,2928) |
| GSE71729 | 145 | 0,2579 / 0,2174 | +0,0405 | échoue | passe | échouait (+0,0402) |
| GSE62452 | 69 | 0,3044 / 0,3116 | −0,0072 | échoue | échoue | échouait (−0,0036) |
| ICGC | 70 | 0,4034 / 0,3073 | +0,0960 | passe | passe | passait (+0,0970) |
| IMMUNE_TCGA | 178 | 0,5263 / 0,1604 | +0,3659 | passe | passe | passait (+0,3675) |
| PARP_TCGA | 178 | 0,3667 / 0,1987 | +0,1680 | passe | passe | passait (+0,1688) |
| DEPMAP | 45 | 0,4339 / 0,2524 | +0,1815 | passe | passe | passait (+0,1904) |

**Total (A) : 6/8 ; total (B) : 7/8.** La seule paire qui change de
verdict entre (A) et (B) est GSE71729 (+0,0405) ; GSE62452 reste négative
sous les deux règles. Sous chaque règle, S_sep et max_separation donnent
exactement les mêmes listes. Pour mémoire, MC v6.2 à gigue 0 donne aussi
7/8 (mêmes paires) contre 1/8 en v6.1 à 0,07 — même mécanisme, même
réserve : les écarts MC sont identiques à la v6.1, seul le seuil a bougé.

**Annexe (23 paires secondaires) — contrôle d'ensemble**

S_sep (A) **16/23** : ATR_TCGA, GEO62452_V4B, GEO71729_PARP, GEO71729_V4B,
GEO71729_V4C, IMMUNE_GEO62452, IMMUNE_GEO71729, IMMUNE_TCGA, PARP_TCGA,
TCGA_V2, TCGA_V3, V4R_CLDN18, V4R_KRASDESC, V4R_KRASVAL, TESTA_PROLIF,
COAD — **exactement les 16 paires de max_separation v6.1**. Échecs (A) :
CPTAC_BCM, CPTAC_UMICH, GEO71729, IMMUNE_ICGC, LUAD, TCGA_V1, V4R_PURITY.
S_sep (B) **20/23** — exactement max_separation v6.2 à gigue 0 (20/23,
mêmes paires) ; échecs (B) : CPTAC_BCM, IMMUNE_ICGC, V4R_PURITY. Les
quatre paires qui ne passent qu'à gigue 0 sont CPTAC_UMICH (+0,0212),
GEO71729 (+0,0405), LUAD (+0,0152) et TCGA_V1 (+0,0049) — toutes sous
0,07, toutes déjà positives en max_separation v6.1.

**8.38.3 Pourquoi S_sep ≈ max_separation ici (et ce que ça veut dire)**

La stabilité est quasi saturée sur toutes les paires PDAC : 0,9692 à
0,9976 sur les bras de ce chantier (ATR 0,9968/0,9917 ; MTAP 0,9959/
0,9825 ; immunitaire 0,9692–0,9976 ; PARP 0,9921–0,9973), et 0,9782 à
0,9973 sur les paires principales. S_sep vaut donc max_separation ×
~0,99 : les écarts S_sep diffèrent des écarts max_separation de moins
de 0,01 partout sauf sur HP35 (réel 0,8687 contre nul 0,9827 : S_sep
+1,4206 contre max_sep +1,6512 — le seul cas où le garde-fou mord un
peu, sans changer le verdict). **Le garde-fou anti-pic-bruité ne s'est
déclenché sur aucune série PDAC de ce chantier.** Ce n'est pas une
preuve qu'il ne servirait jamais — c'est le constat qu'il n'a rien eu à
pénaliser ici : les pics sont localement plats partout, y compris sur
les nuls. S_sep atteint la barre ≥ 6/8 du protocole (§3.4), mais il
hérite exactement des forces et des faiblesses de max_separation :
mêmes paires qui passent, mêmes paires qui échouent (GSE71729 de peu,
GSE62452 plat, ICGC immunitaire inversé), même fragilité face au nul
sur MTAP quand on regarde MC et Delta.

**8.38.4 Provenance**

- **Codes (jamais modifiés).** Pipeline v6.2
  `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` ;
  v6.1 de référence SHA-256
  `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`.
  Mode `fast`, graine 42 (défaut), nul = lignes permutées, graine 42,
  contrôle intact.
- **Formule et règles.** PROTOCOL_v6.2.md §3 (S_sep, exclusions de
  s_norm / robustness / sharpness, plancher 0,07) et §3.4 (critère ≥ 6/8) ;
  règles de comptage de `extract_phase2.py` (direction = signe de la
  somme des écarts).
- **Entrées (SHA-256 vérifiés avant les runs MTAP ; les autres relus
  depuis les JSON des lots existants).** MTAP :
  `pdac_tcga_fluxes_v4_mtap.csv`
  `578b8d3b9b26099d0784ed23754d1cc9717be7f9292eb47e201d186cdbc90df6`,
  `pdac_tcga_fluxes_v4_mtap_nul.csv`
  `e6786a47ce107dbf9785d83981ab413f8afb4e75fbdbae4da56da8c1e46453b9`
  (PROVENANCE_mtap_series.md : Broad GDAC Firehose stddata 2016-01-28,
  PAAD, RSEM ; GISTIC2 Level 4 ; 177/178 appariées). ATR :
  `pdac_tcga_fluxes_atr.csv`
  `88e52311a2cc10371647ff0b9ebbe909b49afe58cf8f8a72e67b7ee31c5fe849`,
  nul `e70011545f230f77d64d4b084addcab83a8cc40508f97cc47e54b08f95f1b090`.
  Immunitaire TCGA `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e`
  / nul `9100d181e3391d558eec6bc97e82f93b16c118b807b4a5f0c0992f4bda51a405` ;
  GSE62452 `97c4689a6ecacd0a73a77804200a72a90994d60bea7e6b2c079195acbffd79a3`
  / nul `b0496cb923d49ef4913f90b895d856e3c02a1b1b4d78a2cc11a9f198c367d3a9` ;
  GSE71729 `8987ffcaeb9cac848bd220c2a1816f63ecbcd63e5cd68c4f698e7c3234952219`
  / nul `b96b1f744db30193098e588326db33c3bca448bb87615fd011d9302e7c605fc7` ;
  ICGC `10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc`
  / nul `3393ecd662e6decfa41416b535e509089cb43bd63345097fe3f25ad9b7860955`.
  PARP TCGA `c9549b68280b2f4ca3d9b62020efa21ab97249b10e176de87ec528a0258c4309`
  / nul `57245c728dacf264654f77a4b4d6d608bbe3fb8c300b287061063bd062ab1360` ;
  PARP GSE71729 `99abbd6e08d7d2e1bc9ef60cb3b158f5d7d55e70ebbfec98cacebea1d936722c`
  / nul `3a8b076456f20bf5a66b6ec7354a70ddc290e04bec0a29fc0c425e963e684ce3`.
  Sources : TCGA-PAAD ARN Broad GDAC Firehose 2016-01-28 (RSEM, tarball
  MD5 `b09569ce3f4721f514bc137bd109ac0a`) ; GEO GSE62452 et GSE71729 ;
  ICGC PACA-AU (UCSC Xena, Bailey et al. 2016). Voir PROVENANCE_atr_chek1.md,
  PROVENANCE_immune_v6.md, PROVENANCE_parp_v6.md, PROVENANCE_mtap_series.md.
- **Nature des lignes.** Les CSV sont des résidus d'expression génique
  (mesures instrumentales — séquençage ARN — transformées : correction
  de pureté, résidus) ordonnés par une variable de contrôle (KRAS, CN
  MTAP, ou index `step`) ; les nuls sont des lignes permutées, graine 42
  — des échantillons hypothétiques, pas des mesures. Aucun mot humain,
  aucun échantillon hypothétique dans les séries réelles.
- **Sorties et scripts.** Runs MTAP v6.2 :
  `results_fast_v62_mtap/master_results.json`,
  `results_fast_v62_mtap_nul/master_results.json` ; log
  `runs_v62_mtap.log` (2/2, exit 0, 19 nov. 2026 11h27–11h34 UTC) ;
  manifeste `manifest_v62_mtap.txt` ; surveillance `watch_v62_mtap.sh` ;
  unité systemd `v62-mtap-838` (arrêtée d'elle-même à 2/2). Les autres
  paires sont relues depuis les 66 dossiers `results_fast_v62_*` du lot
  phase 2 (§8.37) et les 156 dossiers `results_fast_v61_*`. Extraction
  de ce chantier : `extract_ssep_838.py` (SHA-256
  `d7b8bd663fb36340779ebb4d7ce307775d4e9896afee4a75236192cf026bb14a`),
  sortie brute `ssep_838_verify.json` (SHA-256
  `d10727a30afc91886495ba64d882bc692ad1348625ee4f6982560db96600dbbd`).
  Tables comparées : `v62_phase2_table.json` (0 écart),
  `v61_phase2_table.csv` (0 écart, champs comparables).

**8.38.5 Ce qui manque, ce qui reste ouvert**

- **S_sep ne devient pas un discriminateur recommandé au-delà de
  max_separation** : il ne sépare ni mieux ni autrement, sous aucune
  des deux règles de gigue. Le garde-fou stabilité ne s'est jamais
  déclenché sur ces séries ; il faudrait une série à pic bruité
  (stabilité basse côté réel, haute côté nul) pour tester s'il sert à
  quelque chose — aucune série de ce chantier ne présente ce cas.
- **MTAP : contradiction non résolue.** S_sep/max_sep disent réel > nul
  (+0,20) pendant que MC (−0,16) et Delta (−0,54) disent nul > réel.
  Aucun des quatre indicateurs ne suffit seul ; la piste reste fermée
  comme en §8.36, et S_sep ne fournit pas l'arbitrage.
- **Immunitaire ICGC inversé (−0,22).** Le nul y sépare plus que le
  réel en S_sep comme en max_sep, alors que Delta y est positif
  (+0,18). La cohorte ICGC (n=70, flux PRF1/MS4A1 au lieu de IFNG/CD19)
  reste le point faible du bras immunitaire ; pas d'explication
  mesurée à ce jour.
- **Périmètre.** Les rotations (§8.32 : 96 paires, contrôle = flux) et
  les bras parprot / immrot / depmaprot n'ont pas été réappliqués en
  S_sep — hors périmètre de ce chantier (bras nommés : ATR, MTAP,
  immunitaire, PARP, paires principales). À faire sur demande, avec le
  même extracteur ; attention au doublon contrôle=flux (§8.32), qui
  fausserait la lecture par flux mais pas S_sep (best_config).
- **Répétition.** MTAP v6.2 n'a qu'une répétition (comme la phase 2) ;
  la gigue 0 mesurée en validation porte sur 10 autres runs, pas sur
  MTAP. Mais S_sep, max_separation, MC et Delta sont déterministes
  hors L5 et identiques entre v6.1 et v6.2 : une 2e répétition MTAP
  n'apporterait rien sur S_sep (elle ne testerait que L5/L7a, déjà
  validés à gigue 0 sur 10 runs).
- **Falsification.** Indisponible sous n = 75 (GSE62452, ICGC, DepMap)
  — rappel des §8.31/§8.35, inchangé par S_sep.
- **L7a.** Bouge de ≤ 0,0304 entre v6.1 et v6.2 (TCGA_V2, annexe) ;
  aucun verdict L7a ne change sur les paires principales.
- **Aucun nouveau seuil proposé, aucun code modifié, aucun push GitHub
  dans ce chantier** (publication sur go séparé, comme au §8.37).

— Fin de la §8.38. —

### 8.39 Élucidation de Delta (19 novembre 2026)

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

**§8.39.1 Ce qui était acquis avant ce chantier**

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

**§8.39.2 Méthode du chantier 3**

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

**§8.39.3 Ce que la structure dit : l'ordre est presque figé, le choix se joue entre trois estimateurs**

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

**§8.39.4 Hypothèses H8–H15 : taux de prédiction**

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

**§8.39.5 Le plafond de la valeur : même en trichant, on n'atteint pas 90 %**

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

**§8.39.6 Sensibilité : déduplication et le cas H11 à 90,8 % (rejeté)**

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

**§8.39.7 Pourquoi des runs supplémentaires ne trancheraient pas**

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

**§8.39.8 Anomalie DFA = −38,16 — confirmée sans effet (rappel)**

22 runs avec DFA < −10 (dont −38,1597 sur
`results_fast_v61_depmaprot_aco2_nul`), tous DepMap et rotations
protéines DepMap (n=45). Sur les 22, DFA est toujours la 1re valeur
triée de la saturation — jamais la 4e, donc jamais la médiane :
d_sat vaut alors Katz (~1,19) et Delta n'est pas touché
(Delta 1,89–1,95 sur ces runs). DepMap v6.2 (rep1 et rep2, identiques) :
DFA = −18,5768, d_sat = 1,1900 (4e = Katz), Delta = 1,9338.
Une médiane d'estimateur extrême isolée sur petites séries, pas une
rupture de d_sat. Statut inchangé depuis §4.

**§8.39.9 Conséquence : Delta reste une piste fragile**

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

**§8.39.10 Ce qui reste ouvert**

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

**Provenance (§8.39)**

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

### 8.5 Synthèse des 4 versions — ce qui bouge, ce qui ne bouge pas

| | v1 (brute) | v2 (hors pureté) | v3 (+ correction) | v4 (+ hors sexe) |
|---|---|---|---|---|
| Ce que ça mesure | Pureté | Pureté, 2e couche | Sexe (+ tumeur dessous) | Tumeur |
| T_0 réel | 60,90 % → 108 | 48,70 % → 87 | 89,57 % → 159 | 93,22 % → 166 |
| T_0 nul | 9,58 % | 9,58 % | 61,32 % | 15,96 % |
| L7a réel | DOWN (conf. 0,195) | DOWN (0,201) | DOWN (0,174) | **DOWN 86,3 % (0,408)** |
| L7a nul | UP 77,7 % | UP 85,0 % | DOWN 85,7 % | UP 45,1 % |
| Delta réel / nul | 3,68 / 4,30 | 3,74 / 4,30 | 3,84 / 3,89 | 4,18 / 3,77 |
| MC optimum réel | 66,30 % | 66,30 % | 14,13 % | 10,87 % |

**Ce qui ne bouge pas :** les 4 runs réels votent DOWN ; L7b FRAGILE partout (non informatif) ; le régime divergence partout ; Delta ne sépare jamais réel et nul. **Ce qui bouge :** l'endroit du seuil (60,9 → 48,7 → 89,6 → 93,2 %) et ce que le seuil mesure (pureté → sexe → tumeur). Chaque version décrit sa propre fenêtre — comme prévu, ce n'est pas une propriété absolue, c'est une lecture par couches. La couche tumorale (v4) est la plus forte et la seule à se distinguer du nul sur les deux plans.

**Note sur MC optimum contre T_0 :** en v3/v4 ils s'écartent fortement (14,13 % contre 89,57 % ; 10,87 % contre 93,22 %). Le MC optimum et le T_0 de la cascade sont deux quantités différentes (scan contre structure F1/F2) — ne pas les confondre, ne pas en choisir une seule.

---

## 9. Candidats thérapeutiques

*À remplir uniquement à partir de résultats mesurés : cible/combinaison, sources qui la soutiennent, seuils associés, force de la preuve, ce qui manque pour y croire. Aucun candidat sans preuve mesurée.*

**Aucun candidat validé à ce jour (15 nov. 2026). Ce qui suit sont des PISTES — des hypothèses issues du run v4, à tester, pas des candidats.**

| Piste (hypothèse) | Ce qui a été mesuré (v4, TCGA 178 patients) | Ce que ça suggérerait, si confirmé | Ce qui manque pour y croire |
|---|---|---|---|
| **CLDN18 (Claudine 18.2) — le groupe KRAS-très-fort y répondrait MOINS** | CLDN18 s'effondre de −0,46 sd à T_0 (step 166, 93,22 %) et baisse déjà de −0,34 sd en v3 ; les 12 patients KRAS-les-plus-forts perdent ce marqueur | Les thérapies anti-CLDN18.2 (connues dans le cancer gastrique) seraient moins efficaces dans ce sous-groupe — il faudrait le tester avant de traiter | Confirmation indépendante (CPTAC protéine : CLDN18 protéique dans le même sous-groupe ; autre cohorte ARN) ; lien avec la réponse réelle au médicament (GDSC/PRISM) |
| **MUC16 (CA125) — marqueur du groupe KRAS-très-fort** | MUC16 monte de +0,64 sd à T_0 (de −0,22 à +2,11) | CA125, déjà utilisé comme marqueur tumoral, marquerait ce sous-groupe agressif | Même confirmation indépendante ; corrélation avec la survie (non testée ici) |
| **CEACAM5 (CEA) — monte dès le premier temps** | CEACAM5 monte de +0,43 sd à T_-1 (step 132, 74,06 %), puis encore +0,21 sd à T_0 | Le CEA monte avant l'effondrement des marqueurs de différenciation — un signal précoce possible du basculement | Confirmation indépendante ; test : le CEA sérique sépare-t-il ces patients en clinique ? |
| **Le sous-groupe lui-même (~12 patients, KRAS le plus fort)** | Chaîne en deux temps (T_-1 74,06 % puis T_0 93,22 %), L7a DOWN 86,3 % (conf. 0,408), nul à l'inverse | Un sous-groupe moléculaire distinct, moins différencié, à étudier en priorité | Reproduction sur une autre cohorte ; caractérisation clinique (stade, survie, mutations) de ces patients |

**Ce qui n'est PAS dans ce tableau :** aucune combinaison thérapeutique, aucun médicament nommé comme efficace, aucune promesse clinique. Les pistes ci-dessus disent seulement où regarder ensuite — et ce qu'il faudrait mesurer pour y croire.

---

## 10. Journal

- **15 nov. 2026, 07h30 :** mandat de Zackary — v6 + remède PDAC (ARN, protéine, CRISPR, autres flux/données) + livre blanc. Livre blanc créé. Agent de repérage lancé (inventaire tlog28 + sources réelles gratuites). Rien téléchargé, aucun run lancé.
- **15 nov. 2026, 07h33 :** rapport de repérage reçu et vérifié. Inventaire confirmé (voir §6.1). 3 sources recommandées, mais vérification faite : DepMap 24Q4 CONFIRMÉ (CRISPRGeneEffect.csv 428,7 Mo, Model.csv 0,6 Mo, via figshare) ; cBioPortal S3 403 (étude existe dans datahub, accès à retrouver) ; GDSC 8.5 liens 404 (nouvelle adresse à retrouver). Téléchargement DepMap lancé.
- **15 nov. 2026, 07h34 :** Zackary demande de revoir l'axe pseudo-temporel invalidé — il peut apporter de l'information. Relecture détaillée R1/R2/R3 à venir, résultats notés ici.
- **15 nov. 2026, 07h36 :** relecture faite (4 rapports relus en entier, §2.1). Apports : biais d'argmax +9,3 pp (un T0 est un maximum de contraste, pas une bifurcation) ; EMT_Invasion + Stroma_Desmoplasia survivent au pipeline corrigé ; levier b2 (ATR/G6PD → MRTX/venetoclax) dominant partout ; chevauchement des phases > séquençage net (intra-modèle) ; lire les cascades comme paysages d'influence ; pics δ=40/75/105 = falaises de protocole ; biais de cohorte TCGA (IIB 68 %) ; drapeaux rouges pour les runs v6. Téléchargement DepMap en cours (~43 % à 07h35, ~1 min restante estimée).
- **15 nov. 2026, 07h37 :** `CRISPRGeneEffect.csv` téléchargé — taille exacte 428 678 699 octets, conforme à l'API figshare (MD5 non fourni par figshare, vérification par taille + SHA-256 consigné dans `download_depmap.log`). `Model.csv` en cours. Accès cBioPortal résolu : pas de tarball S3 (403) ni de fichiers dans datahub (README lu, aucune URL) — la voie est l'API cBioPortal, à mettre en place ; non bloquant.
- **15 nov. 2026, 07h38 :** téléchargement DepMap TERMINÉ et vérifié (exits 0, tailles exactes, SHA `3d8f3ec6…` / `b7a0c138…`). Inspecté : 2 105 modèles, 68 lignées pancréas dont 64 adénocarcinomes, 17 916 gènes, tous les gènes candidats présents.
- **15 nov. 2026, 07h38 :** correction de Zackary — ne pas importer les données/conclusions des autres expériences, se concentrer sur le travail du jour. Règle ajoutée au §3 : l'état antérieur est du contexte, jamais une entrée ; seuls les données et runs du jour font les verdicts.
- **15 nov. 2026, 07h39 :** exigence de Zackary — tout traçable, reproductible, clair et public ; il ne connaît pas ce domaine, donc tout expliqué simplement. Règle ajoutée au §3 (travail public, pipeline privé). Instruction : donner le maximum, ne pas s'arrêter avant d'avoir quelque chose de vrai à présenter — ni faux espoir, ni défaite.
- **15 nov. 2026, 07h39 :** flux du jour construits (45 lignées × 12 gènes, SHA `7d605fef…`, nul SHA `ac2e0db5…`). **Premiers runs v6 BLOQUÉS : la v6 exige ≥ 50 points, on en a 45 (47 avec les 2 adénosquameuses). Échecs enregistrés au §7 (exit 1, pas un verdict). Solution proposée : copie v6.1 « séries courtes », en attente du go de Zackary.**
- **15 nov. 2026, 07h46–07h58 :** Zackary demande une autre source pour dépasser 50 points. **Pour CRISPR : non — DepMap est déjà la plus grande source au monde (47 lignées pancréas max).** Pour les patients : oui. **TCGA-PAAD via API cBioPortal : vérifié que l'étude et les profils existent (184 échantillons, 177 ARN), mais le téléchargement complet est BLOQUÉ par l'API : le GET `molecular-data` exige un gène à la fois (20 000 requêtes), le POST `molecular-data/fetch` est refusé par le serveur (« interceptedMolecularDataMultipleStudyFilter must be true »), les fichiers datahub sont des pointeurs Git LFS (130 o) et le tarball S3 refuse (403). UCSC Xena : S3 AccessDenied. Voie retenue : Broad GDAC Firehose 2016-01-28, matrice RSEM normalisée PAAD complète (un seul fichier) — téléchargement lancé 07h58, MD5 à vérifier. Secours : GEO GSE71729 (145 tumeurs primaires, matrice 15,6 Mo, vérifiée accessible).**
- **15 nov. 2026, 07h58 :** Firehose TÉLÉCHARGÉ et vérifié (15 296 232 o, MD5 exact `b09569ce…`). Matrice : 20 532 gènes × 183 échantillons, 178 tumeurs primaires. **Premier fait mesuré du jour : les 12 gènes de plus forte variance sont presque tous des enzymes digestives du pancréas normal (PNLIP, CTRB, CELA, CPA, CPB, CLPS, CTRC) + XIST (sexe) — dans une biopsie, ils mesurent la quantité de pancréas normal mélangée à la tumeur et le sexe, pas le cancer. Variante v2 construite (40 gènes exclus, liste consignée) : les 12 suivants sont encore des marqueurs de pancréas normal (PNLIPRP1/2, CELA2B, PLA2G1B, GP2, CEL, INS, GCG, PPY…) — la variance dominante des données brutes, c'est la composition du tissu. Runs v6 lancés (v1 + v1 nul + v2 + v2 nul, log `runs_tcga_v6.log`).**
- **15 nov. 2026, 08h01 :** variante **v3** construite : correction de pureté par régression (2 scores — acineux 11 gènes, îlots 4 gènes — médiane des gènes : 2,0 % de variance expliquée seulement ; KRAS 0,3 %). Après correction, la variance dominante devient le **sexe** (XIST + 6 gènes Y dans le top 12). Variante **v4** construite (v3 + exclusion des 17 gènes du sexe) : top 12 enfin tumoraux — PGC, REG4, **CLDN18**, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, **CEACAM5**, CLCA1, **MUC16**. Chaque version est un témoin de la suivante ; rien n'est caché. Runs v3/v4 à lancer après le lot v1/v2.
- **15 nov. 2026, 07h46 : échec TCGA, HTTP 400 (GET sans entrezGeneId + POST champ singulier) ; correctif vérifié 08h00 (molecularProfileIds pluriel, transport curl) ; relance cBioPortal arrêtée volontairement, voie Firehose 178 patients retenue, runs en cours.** Détail vérifié : le POST `/molecular-data/fetch` exige le champ `molecularProfileIds` (pluriel, liste) — avec le singulier, le serveur refuse en 400 « interceptedMolecularDataMultipleStudyFilter must be true » ; avec le pluriel, HTTP 200, 531 lignes pour 3 gènes × 177 échantillons, valeurs identiques au GET (KRAS TCGA-2J-AAB1-01 : −0,562). Deuxième problème : urllib levait `IncompleteRead` sur les réponses chunked de cBioPortal — transport passé à curl (vérifié 3/3 sur `/api/genes`). Script corrigé : `runs/pdac-v6/fetch_tcga_fluxes.py` (POST par lots de 1000 gènes via `/api/genes`, champ pluriel, transport curl, 5 tentatives) — gardé comme route de contre-vérification (z-scores cBioPortal, 177 patients), à ne lancer que sous un autre nom de fichier, pour ne pas écraser la v1 Firehose pendant les runs (SHA préservés : v1 `e012e9fd…` vérifié inchangé).
- **15 nov. 2026, 08h07 : run v1 TERMINÉ, exit 0.** Cascade : 0 / 49,63 % → step 88 / **T_0 60,90 % → step 108** / 97,39 % → step 173 (×2). Cible PNLIP. L7a DOWN (up 34,7 %, down 49,9 %, confiance 0,195). L7b FRAGILE (léger, non informatif — verdict clos). Régime divergence, Delta 3,68. Nul : cascade 1,06 / 6,39 / **9,58** / 15,96 / 22,63, L7a UP 77,7 %, Delta 4,30 — le nul place son seuil ailleurs et vote à l'inverse ; Delta ne distingue pas réel et nul (4,30 nul > 3,68 réel). Lecture : l'ordre par KRAS porte l'information (où tombe le seuil, dans quel sens) ; la v1 mesurant la pureté, le DOWN dit que les marqueurs acineux baissent quand KRAS monte. Détail au §8.
- **15 nov. 2026, 08h10 : redémarrage VM — le lot v2 a été tué en cours (dossier `results_fast_tcga_v2/` vide, 0 fichier, aucun EXIT ; la v6 n'écrit qu'à la fin). v1 réel + v1 nul intacts (exit 0, 36 fichiers chacun). Relance : v2 réel + v2 nul, puis v3 + v3 nul, v4 + v4 nul, en une seule file (log `runs_tcga_v6.log`).**
- **15 nov. 2026, 08h31 : LES 8 RUNS TCGA TERMINÉS, exit 0.** v2 : T_0 48,70 % → 87, L7a DOWN, Delta 3,74 (nul : T_0 9,58 %, UP 85 %). v3 : T_0 89,57 % → 159, L7a DOWN (nul : T_0 61,32 %, DOWN 85,7 % — la direction ne distingue pas en v3). v4 : **T_0 93,22 % → 166, L7a DOWN 86,3 % (conf. 0,408, la plus forte), Delta 4,18** (nul : T_0 15,96 %, UP 45,1 %). **Premier résultat vrai du jour (§8.4) : chaîne en deux temps — à T_-1 (74,06 %) KRT20 et CLCA1 baissent, CEA monte ; à T_0 (93,22 %) PGC, DPCR1 et CLDN18 s'effondrent, MUC16 monte. Les ~12 patients KRAS-les-plus-forts forment un groupe à part, moins différencié. Pistes au §9 (CLDN18, MUC16, CEACAM5) — des hypothèses à tester, pas des candidats, pas un remède.**
- **15 nov. 2026, 08h34 : « Essaie de faire plus que mesurer » — deux tests d'action lancés. Test CRISPR (DepMap 24Q4, 47 lignées) : NÉGATIF — aucune corrélation forte avec KRAS (CLDN18 +0,045, MUC16 −0,117, CEACAM5 −0,131) : ces gènes sont des marqueurs de surface, pas des vulnérabilités génétiques. Test médicaments (PRISM 24Q2, 6 790 composés, 38 lignées) : NÉGATIF — pamiparib nº 1 (rho −0,614, p < 0,0001) mais FDR 0,286, zéro composé sous FDR 0,05, aucun effet de classe PARP (médiane +0,032). La confirmation décisive restante est la protéine CPTAC (PDC000393, agent lancé 08h33). Détail au §8.6/§8.7.**
- **15 nov. 2026, 09h05 : CPTAC — NON-CONFIRMATION. Sur les deux centres (UMich 63 tumeurs, BCM 52 tumeurs), la chaîne v4 n'apparaît pas en protéine : UMich T_0 à 4,69 % (3 points avant), Delta réel 1,48 contre nul 1,49 ; BCM T_0 à 63,26 % sans aucun mouvement de flux ; L7a dégénéré (probabilités NaN) sur les 4 runs ; le test direct s'inverse entre top 4 et top 12 dans les deux centres. Le résultat ARN v4 reste debout (autre cohorte, autre couche), mais il n'est pas confirmé. Suite proposée : autre cohorte ARN (ICGC/GEO) — la confirmation la plus directe. Détail au §8.8. Rotations de contrôle v4 en cours (2/8 terminées).**
- **15 nov. 2026, 09h24 : ROTATIONS v4 TERMINÉES, 8/8 exit 0 — la chaîne est réelle et propre à l'axe KRAS. (1) KRAS-valeur : cascade IDENTIQUE à la v4 chiffre par chiffre (0 / 74,06 / 93,22 / 98,44 / 98,96, L7a DOWN 85,8 %) — la métrique du contrôle ne change rien. (2) Miroir : la chaîne se retourne EXACTEMENT flux par flux (PGC +0,89, DPCR1 +0,85, CLDN18 +0,46, MUC16 −0,64 au step 12), mais la cascade ne place pas son T_0 au miroir (60,38 %) et L7a ne se retourne pas — comportements de l'instrument notés comme questions ouvertes. (3) CLDN18 comme contrôle : pas de discrimination (réel UP 85,5 % contre nul UP 86,3 %). (4) Pureté comme contrôle : aucune chaîne, comme attendu (vote faible). Tout consigné au §8.9. GEO GSE71729 en cours.**
- **15 nov. 2026, 09h40 : GEO GSE71729 — NON-CONFIRMATION, mais la moitié « marqueurs qui montent » tient. Sur 145 tumeurs (3 variantes, 6 runs exit 0), la chaîne ne se confirme pas : les gènes qui s'effondraient en TCGA MONTENT avec KRAS ici (top 12 : CLDN18 +0,68 sd, DPCR1 +0,60, KRT20 +0,60 — vérifié) ; le pipeline ne sépare pas réel et nul (Delta 2,16 contre 2,20). En revanche MUC16 (CA125) et CEACAM5 (CEA) sont plus élevés dans le groupe KRAS-le-plus-fort dans LES DEUX cohortes (MUC16 : +0,64 TCGA, +0,65 GEO ; CEA : +0,43 TCGA, +0,38 GEO). La moitié « différenciation qui s'effondre » s'inverse ; la moitié « marqueurs qui montent » tient. Le résultat TCGA reste debout dans sa cohorte, mais il n'est pas universel. Détail au §8.10. Limite : script de la variante (c) non sauvegardé (exécuté en ligne, construction décrite dans la provenance).**
- **15 nov. 2026, 10h05 : TEST DÉCISIF — les données brutes tranchent les deux moitiés. Sur la matrice Firehose sans correction, mêmes 12 patients que la v4 : CA125 +0,58 sd et CEA +0,75 sont là dans le brut (aussi forts qu'en v4) ; PGC −0,51 existe mais plus faible ; DPCR1 −0,17 et CLDN18 −0,04 sont quasiment absents dans le brut (contre −0,85 / −0,46 en v4). La hausse de CA125/CEA ne dépend d'aucune correction et tient dans deux cohortes ; l'effondrement de DPCR1/CLDN18 dépend de la correction et ne tient nulle part ailleurs. Le résultat robuste se resserre sur : le groupe KRAS-le-plus-fort a CA125 et CEA élevés. Détail au §8.11.**
- **15 nov. 2026, 10h20 : SURVIE — le paysage dépend du seuil (avertissement de Zackary, 10h11 : ne pas se fixer sur un seuil/flux/contrôle). 9 définitions testées, toutes rapportées : top12 KRAS vit 9,1 mois contre 20,4 (p=0,024 ; brut p=0,002), mais top7 rien (19,5 mois, p=0,24), top20 limite (p=0,053), score combiné et double-quartile non significatifs. Test SANS seuil (Cox continu, n=177, 92 décès) : KRAS HR 1,29 (p=0,035), MUC16 HR 1,28 (p=0,072) ; en multivarié KRAS HR 1,31 (p=0,018) et MUC16 HR 1,34 (p=0,014) ; CEA rien en continu (HR 1,02, p=0,89). Sans aucun seuil, KRAS et CA125 prédisent chacun une survie plus courte. Troisième cohorte ARN (GSE62452) lancée pour tester CA125/CEA une troisième fois, paysage complet demandé. Détail au §8.12.**
- **15 nov. 2026, 10h36 : TROISIÈME COHORTE — OUI, 3/3. GSE62452 (69 tumeurs, puce Affymetrix HuGene-1.0-st, GPL6244 réelle) : CA125 +0,48 sd et CEA +0,63 chez les KRAS-les-plus-forts (CEA rho +0,441, p=0,0001) ; DPCR1 +0,93 et CLDN18 +0,55 MONTENT aussi — l'effondrement ne tient que dans TCGA. Re-sélection fraîche retrouve DPCR1 et CEA qui montent. Le pipeline ne sépare pas réel et nul ici (Delta 1,41 contre 1,26) ; L7a NaN sur les 4 runs — motif qui se précise : L7a dégénère aux petits n (52, 63, 69) et fonctionne à 145, 178, 1000. Illustration de l'avertissement : le T_0 tombe au step 66 (3 points après) et retourne le signe de CA125 (−0,83) contre +0,48 au top 12 — le verdict vient des tests directs, pas du seuil. Résultat robuste : KRAS fort = CA125 et CEA élevés, 3 cohortes sur 3. Détail au §8.13.**
- **16 nov. 2026, 07h20 : DIAGNOSTIC L7a NaN — CAUSE TROUVÉE. Le diagnostic de bruit coupe la série en 5 bins et exige ≥15 points par bin (il faut 75 points) : à n=52/63/69, l'estimation de Hurst échoue pour chaque flux → score NaN → classement CSD que des NaN → `top_csd` NaN sans protection → risque et confiance L4 NaN, niveau « low » → le vote L7a devient NaN, `max()` retourne « up » par accident, confiance repliée à 0,50. Le « up » des petits runs n'est pas un vote. Correctif proposé sur copie (protéger `top_csd`, protéger les votes L7a) — en attente de son go. Détail au §8.14. Les 4 bras lancés le 16 nov. à 07h08 : ICGC (4e cohorte + survie), survie GSE71729, médicaments ciblés KRAS (GDSC), diagnostic L7a (terminé).**
- **16 nov. 2026, 07h35 : SURVIE GSE71729 — PARTIEL. Sur 125 tumeurs avec survie (84 décès) : KRAS tient en direction (Cox univarié 1,24, p=0,075 ; quartile KRAS 10,0 contre 19,0 mois, p=0,020), CA125 ne confirme pas (1,06, p=0,58), le groupe top12 ne confirme pas (17,0 contre 17,0, p=0,89). Deux erreurs corrigées en route (log-rank faux, « univarié » mal étiqueté). Détail au §8.15.**
- **16 nov. 2026, 07h40 : CORRECTION SURVIE TCGA — le tableau « Cox univarié » du 15 nov. (§8.12) était en fait l'ajustement à 6 gènes, mal étiqueté. Vérification indépendante (script sauvegardé, 3 implémentations Cox, 2 log-rank) : vrais univariés KRAS 1,42 (p=0,0003), MUC16 1,44 (p=0,001), CEACAM5 1,31 (p=0,011), DPCR1 1,43 (p=0,001) ; multivarié confirmé (1,33/1,32/1,07) ; paysage refait (top12 p=0,017, top20 p=0,0415, quartiles et double-quartile non significatifs). La conclusion se renforce. Détail au §8.12.**
- **16 nov. 2026, 07h45 : QUATRIÈME COHORTE ICGC — EXPRESSION NON, SURVIE CA125 OUI. Sur 70 tumeurs PACA-AU (Bailey 2016 ; portail ICGC mort, données via Xena + tables Bailey) : CA125 +0,13 et CEA +0,28 chez les KRAS-les-plus-forts — dans le bruit du nul. Le « 3/3 » devient « 3/4 » pour l'expression. En revanche CA125 prédit une survie plus courte, fort et indépendant : quartile 9,5 contre 23,8 mois (p=0,002), Cox 1,57 (p=0,008), 1,56 en multivarié, 1,75 ajusté sur le sous-type. KRAS rien (1,25), CEA rien (0,80). Survie CA125 : 2/3 cohortes. Détail au §8.16.**
- **16 nov. 2026, 07h50 : MÉDICAMENTS CIBLÉS KRAS (GDSC2) — NON. Sur 269 composés et 27 lignées pancréas : aucun inhibiteur MEK/ERK/RAF/KRAS significatif (sélumétinib +0,217, tramétinib +0,164, ERK_2440 +0,246 — FDR 0,39–0,52) ; les lignées KRAS-dépendantes sont globalement plus résistantes (médiane rho −0,295) ; seul FDR < 0,05 : la staurosporine, direction négative (curiosité). Les inhibiteurs KRAS de clinique (sotorasib, adagrasib, MRTX1133) sont absents de GDSC2 — non testables ici. Note : les étiquettes de tertiles du script PRISM du 15 nov. étaient inversées (sans effet sur le verdict, rien de cité au §8.7). Détail au §8.17. Les 4 bras sont terminés.**
- **16 nov. 2026, 07h50 : THÉRAPIES MUC16 / CLDN18.2 — MUC16 NON, CLDN18.2 PISTE RÉELLE MAIS PRÉCOCE. MUC16 : 0 réponse chez 11 patients pancréatiques (DMUC5754A, seul test humain) ; rien d'autre de clinique — biomarqueur pronostique, pas une cible validée. CLDN18.2 : zolbetuximab ÉCHEC randomisé (GLEAM 13,7 vs 13,6 mois, HR 0,999, programme arrêté) ; mais l'ADC IBI343 répond chez 22,7 % des patients en phase I et est en phase III pancréatique (NCT07066098) ; CAR-T satri-cel 16,7 %, bispécifique IBI389 29,6 % — signaux précoces, non randomisés. Nos cohortes : KRAS fort enrichi en MUC16 et CLDN18 élevés (3/4) ; double-positifs 0–2/12, pas de base pour une combinaison ; ARN ≠ IHC d'éligibilité. TCGA : aucune donnée de chimio ; la radiothérapie ne modifie pas le signal CA125. Aucun remède démontré. Détail au §8.18.**
- **16 nov. 2026, 07h55 : NOUVEL ORDRE — « Continue jusqu'à ce que tu trouve un remède. » Quatre nouveaux bras lancés en parallèle : (A) balayage CRISPR génome entier (17 916 gènes, données déjà sur disque) ; (B) PRISM secondaire dose-réponse ; (C) thérapies ciblées MUC16/CLDN18.2 ; (D) inhibiteurs directs KRAS G12D / pan-RAS (données publiques ou gap nommé).**
- **16 nov. 2026, 07h47 : PRISM SECONDAIRE (dose-réponse, 19Q4) — NON. Sur 1 427 composés et 29 lignées pancréas : zéro composé FDR < 0,05 (FDR min 0,418 en AUC, 0,619 en IC50) ; MEK plat (+0,008). Les trois criblages (PRISM primaire, PRISM secondaire, GDSC2) convergent vers le même négatif. Reste non testé : les inhibiteurs KRAS directs de clinique (absents des trois bases) et les combinaisons. Détail au §8.19. Bras A et D en cours.**
- **16 nov. 2026, 07h50 : INHIBITEURS KRAS G12D / PAN-RAS — OUI POUR UN SEUL, ET UNE APPROBATION FDA. Test par allèle (vérifié) : le MRTX1133 tue les lignées G12D (−1,70 contre −0,38, p=0,0001) ; l'axe Chronos prédit la sensibilité chez les G12D (rho +0,47, p=0,079, n=15 — suggestif, pas une preuve). Son essai est arrêté (formulation/PK). Le fait le plus fort : le daraxonrasib (RMC-6236) est approuvé par la FDA depuis le 26 août 2026 — premier médicament ciblant RAS dans le pancréas, phase III RASolute-302 : survie 13,2 contre 6,7 mois, HR 0,40 (vérifié indépendamment, plusieurs sources). Ce n'est pas un remède et pas une prédiction du pipeline — c'est un résultat clinique réel. Aucune matrice publique pour tester le daraxonrasib contre l'axe. Détail au §8.20. Il ne reste que le balayage CRISPR (bras A) en cours.**
- **16 nov. 2026, 07h58 : BALAYAGE CRISPR GÉNOME ENTIER — 2 PARTENAIRES RÉELS MAIS FAIBLES, PAS UN REMÈDE. Sur 17 787 gènes testés (47 lignées) : TCF7L2 rho +0,614 (FDR 0,039) et PRDX4 +0,602 (FDR 0,045) ; nul 0 hit. Mais essentialité absolue faible (−0,43 / −0,25), TCF7L2 non druggable, PRDX4 sans médicament connu ; aucun candidat connu significatif (RAF1/PLK1/BCL2L1 top ~50–70, FDR 0,45–0,49). Le côté CRISPR est épuisé sur ces données. Détail au §8.21. Les 4 bras « continue jusqu'à trouver un remède » sont terminés.**
- **16 nov. 2026, 07h58 : BILAN DU ROUND « REMÈDE » — trouvé : le daraxonrasib, approuvé FDA, survie doublée en phase III (13,2 contre 6,7 mois, HR 0,40) — une avance réelle, pas une guérison, pas une prédiction du pipeline. Piste précoce : IBI343 anti-CLDN18.2 (22,7 % de réponses en phase I, phase III en cours). Test positif du projet : MRTX1133 tue les G12D (p=0,0001), essai arrêté. Négatifs : 3 criblages médicaments, CRISPR génome entier (2 hits faibles non druggables), MUC16 comme cible. Angle restant non fouillé : les combinaisons (KRAS + autophagie notamment) — bras lancé.**
- **16 nov. 2026, 08h10 : COMBINAISONS — OUI, VOPIMETOSTAT + DARAXONRASIB, 82 % DE RÉPONSES. Chez les patients MTAP-délétés prétraités (n=22) : 82 % de réponses (18/22), contrôle de la maladie 100 %, survie sans progression à 9 mois 88 %, médiane non atteinte (phase 1/2 NCT06922591, ESMO 2026 — vérifié indépendamment, plusieurs sources). Non randomisé, pas de survie globale ; phase 3 prévue 1H 2027. C'est la piste la plus solide du projet. En revanche MEK + autophagie : ÉCHEC clinique (PFS 52 jours) ; MEK + CDK4/6 : échec. PANC-1 : 280/496 paires synergiques, top panobinostat + carfilzomib, zéro paire MEK/KRAS/ERK/HCQ. Aucune matrice publique multi-lignées pancréas — le test axe × combinaison n'a pas pu être fait. Détail au §8.22.**
- **16 nov. 2026, 09h27 : TESTE TOUT AVEC LE PIPELINE — IMMUNITAIRE ET PARP, 10 RUNS v6. Ordre de Zackary (« Teste tout et n'oublie pas d'utiliser mon pipeline »). Immunitaire (4 cohortes, 8 runs) : OUI, la tumeur devient froide quand KRAS monte — T baissent partout (PD-1 significatif dans les 4), PD-L1 ne monte qu'en TCGA et top-12 ns partout → KRAS + anti-PD-(L)1 NON. PARP (TCGA + contrôle GEO, 2 runs) : OUI, mais pas côté PARP — BRCA2/ATR/RAD51 répliqués en hausse, PARP1/PARP2 plats partout → KRAS + PARP NON (3 angles négatifs). Piste cohérente : ATR/CHEK1 (stress de réplication), à tester. Dans les deux bras le v6 ne sépare pas réel et nul — les verdicts viennent des tests directs. Détail aux §8.23–8.24.**
- **16 nov. 2026, 09h45 : RE-TEST ATR/CHEK1 — LA PISTE EST REDRESSÉE, PAS FERMÉE. La hausse survit à la pureté, pas à la prolifération — sauf ATR seul. Le « stress de réplication » large était de la prolifération (score prolif contre KRAS +0,386 ; RAD51/CHEK1/POLQ liés à la prolif à +0,65–0,79). Après contrôle : ATR survit dans les 2 cohortes où le signal existait (TCGA partiel +0,366, p 5,6e-7 ; GSE62452 +0,488, p 2,4e-5), BRCA2 1/2, CHEK1/RAD51/POLQ morts. ICGC : 0/7 (axe plat). Médicaments ATR/CHEK1 : 0/60 FDR < 0,05 dans les 3 criblages (ceralasertib, prexasertib : rien). CRISPR : rien. Reste ouvert : ATR seul, hypothèse d'expression, sans appui CRISPR ni médicament — aucun test ne justifie une combinaison KRAS + ATR/CHEK1. Détail au §8.25.**
- **16 nov. 2026, 14h59 : MTAP/PRMT5 ET PAN-CANCER — DEUX NON, DEUX FAITS NOUVEAUX. MTAP : délétion non démontrée enrichie chez les KRAS-forts (6/12 contre 37/165, OR 3,46, Fisher p=0,073 — NS) ; la combinaison vopimetostat cible donc un sous-groupe distinct (MTAP-délétés, 24 %), elle complète l'axe. Fait nouveau : PRMT5 monte en expression avec KRAS (+0,196, top-12 +0,83 sd), mais la dépendance CRISPR est plate. Pan-cancer : CA125 plat dans le poumon (+0,020) et le côlon (+0,019) ; CEA lien faible sans enrichissement top-12 — l'axe est spécifique au pancréas. Fait nouveau : le côlon a son propre programme KRAS (MUC2 +0,302, REG4, CLCA1, KRT20). Détail aux §8.26–8.27.**
- **16 nov. 2026, 15h13 : DÉPENDANCE PRMT5 CONTRE STATUT MTAP MESURÉ — OUI, PLUS FORTE EN PANCRÉAS. Lignées pancréas : Chronos PRMT5 médian −1,385 chez les 20 MTAP-délétées contre −1,010 chez les 27 intactes (p=0,0036) ; Spearman +0,497 (p=0,0004). Pan-cancer même direction, effet plus petit (p=1,7e-14). Contrôles KRAS/ACTB propres. Limite : MTAP et CDKN2A presque toujours perdus ensemble (CN +0,808) — effet MTAP contre effet 9p21 non séparé par ce test seul. C'est un appui mesuré au rationnel de la combinaison vopimetostat — une fenêtre thérapeutique réelle, pas une dépendance absolue. Détail au §8.28.**
- **16 nov. 2026, 17h28 : PDF COMPLET + GITHUB — PUBLICATION (ordre de Zackary : tout dans le PDF, peu importe la grosseur, chaque source avec son lien). PDF régénéré : 404 pages A4, 9 932 890 octets, SHA-256 `7a1c6eef…cea530` (ancien 21 pages, 572 035 octets, périmé). Contenu : texte intégral §1–§10, §8.1–§8.28, annexes A–G — reproduction (17 jeux de données, URL + MD5/SHA recalculés), 25 provenances intégrales, tables complètes, code intégral v6 (13 010 lignes) + 41 scripts + 6 lanceurs avec SHA, 15 figures, éthique/reproductibilité, registre de 189 sources avec liens (17 sources sans URL vérifiable, déclarées comme telles avec la raison). GitHub, dépôts PRIVÉS, rien rendu public : travail PDAC dans `FindPrint/pancreatic-cancer-open-data-reproducibility` (176 fichiers, 6,85 Mo, 4 commits, tête `ecb5d1f3`) ; pipeline v6 dans `FindPrint/Code` (commit `6a1d2130`). Le dépôt `FindPrint/tlog28-cancer-pdac` n'existe pas (404 vérifié). Exclus : matrices brutes ~2 Go (re-téléchargeables vérifiées via `download_data.sh`), sorties complètes des runs, PDF binaire (création de Release impossible via l'outil — à faire à la main sur github.com si voulu). Chaîne de construction dans `.src/` (`build_appendix.py` + `build_pdf.py`, WeasyPrint 70.0). Le PDF est l'instantané du livre blanc au 16 nov. 15h13 ; cette entrée sera reprise dans le PDF à la prochaine régénération, quand le round « remède » se clôturera.**
- **16 nov. 2026, 17h55 : SÉPARATION MTAP vs 9p21 — OUI, L'EFFET PRMT5 SUIT MTAP. La limite du §8.28 est levée par un test mesuré : CDKN2A-délétées sans perte profonde de MTAP (n=137) : PRMT5 −1,013 contre −0,973 intactes, p=0,26 — pas plus dépendantes ; MTAP+CDKN2A ensemble (n=293) : −1,098, p=1,5e-5 ; Spearman PRMT5 ~ CN MTAP +0,244 (p=2,9e-7), deux fois le CN CDKN2A (+0,122). Pancréas seul : même direction (both-del −1,385 n=20 ; CDKN2A-seul −1,049 n=7 ; neither −0,984 n=20), p=0,081 faute de puissance. MTAP seul : n=1 pan-cancer, 0 en pancréas. Test direct DepMap, pas un run v6 — le pipeline n'a pas été lancé sur cette question. Le rationnel vopimetostat + daraxonrasib gagne un appui mesuré ; ça ne prouve pas la combinaison. Détail au §8.29.**
- **16 nov. 2026, 18h23 : PIPELINE v6.1 — VALIDÉE, BRAS CRISPR TESTÉ POUR LA PREMIÈRE FOIS. Ordre de Zackary (« Teste mon pipeline », 18h13) + go confirmé 17h58. Copie v6.1 construite (SHA `2af5e5ce…c1c9`, 10 remplacements, conception gelée `PROTOCOL_v6.1.md`) : gardes L7a (plus de faux « up »/0,50 sous n=75) + séries courtes (min_len fast 50→40). Validation 10 runs, tous exit 0 : HP35 réel/nul et TCGA v4 réel/nul cascades identiques à v6 ; TCGA v4 L7a DOWN 0,405 (v6 : 0,408), falsification 0,849 identique ; GSE62452 et ICGC : votes désormais finis et honnêtes. DepMap CRISPR (45 lignées) : le pipeline tourne enfin — cascade 0/1,40/4,40/11,01/26,42, L7a down 0,196 — mais ne sépare pas le nul (MC 0,3615 contre 0,3499, Delta 1,93 contre 1,69, T_+2 à 26,42 % dans les deux). Falsification indisponible sous n=75. Gigue L5 mesurée (±0,07, hash Python aléatoire) — piste v6.2 : hachage stable. Lots v6.1 en cours (44 runs étendus + 96 rotations, lanceur reprenable). Protocole phase 2 (discrimination réel/nul) écrit, exécution en attente du go. Détail au §8.30.**
- **16 nov. 2026, 18h34 : ADOPTION v6.1 — Zackary adopte la v6.1 comme version de travail (« Oui, adopte la v6.1 comme version de travail »). La v6.0.0 reste intacte comme référence ; tous les runs PDAC suivants utilisent la v6.1.**
- **17 nov. 2026, 15h10 : LOT ÉTENDU v6.1 — 43/44, LA v6.1 REPRODUIT LA v6, MAIS NE SÉPARE TOUJOURS PAS RÉEL ET NUL. Côlon réel perdu (dossier effacé pendant le run par une relance manuelle et automatique en collision) — refait à la fin des rotations. Extracteur corrigé sur copie (`extract_v61_lot_compare_v2.py`, SHA `4cb9b14d…15bb` ; original intact) : cascades identiques à v6 sur 41/41 (et non 33 — 8 runs v6 manqués par l'ancien appariement par nom) ; falsification > 0,5 sur 16/21 réels contre 15/21 nuls (et non 16/16). L7a des 5 petites cohortes : votes finis et faibles (0,15–0,36) au lieu du faux « up 0,500 ». Les 3 plus grands écarts réel/nul lus flux par flux, réel ET nul (`pistes_v61_flux_reading.py`, SHA `0009b46f…b899`) : pureté = artefact du score composite (robustesse 0,808 contre 0 ; séparation même plus faible dans le réel, 0,144 contre 0,211) ; CLDN18 = le contrôle figure aussi parmi les flux (Spearman 1,000) + vraie co-expression gastrique/mucineuse absente du nul ; immunitaire = Delta du nul anormalement bas (2,30, régime criticité, contre 3,77–4,30 pour les autres nuls TCGA) — le réel montre la chute groupée des gènes cytotoxiques chez les 20 % les plus KRAS (GZMB −1,65, IFNG −1,25, CD8A −1,08), concordant avec le test direct §8.23. Aucun run lancé, aucun CSV modifié, pipeline `2af5e5ce…c1c9` inchangé. PDF non régénéré. Détail au §8.31.**
- **17 nov. 2026, 17h56 : ROTATION CLDN18 SANS DOUBLON — TERMINÉE, 2/2, ET LE RÉEL NE SE SÉPARE TOUJOURS PAS DU NUL.** Go de Zackary 17h17. CSV construits par `build_v4r_cldn18_dedup.py` (SHA `30aba3b4…`) : le flux CLDN18 en double est retiré, contrôle/ordre/11 autres flux inchangés ; SHA réel `b1071f84…`, nul `33d5f317…`. Runs v6.1 exit 0, journal `runs_v61_cldn18_dedup.log` (SHA `64760bed…`), pipeline `2af5e5ce…c1c9` inchangé. Cascade réelle identique au centième à avec-doublon (4,26 / 46,59 / 84,42 / 91,14 / 91,14) ; MC 0,4257 contre 0,3313 nul ; Delta 3,862 contre 3,854 ; L7a UP des deux côtés (0,852 contre 0,847) ; falsification > 0,5 des deux côtés ; L7b FRAGILE des deux côtés. Le groupe estomac/mucus (PGC, REG4, MUC17, DPCR1, CEACAM5) bouge encore sans le doublon, avec les mêmes valeurs — mais il bouge aussi dans le nul, en sens inverse à T_0 (MUC17 −1,13, DPCR1 −0,81). La co-expression est réelle, elle ne sépare pas. La piste CLDN18 est fermée comme test de séparation. Détail au §8.31 ; ligne 36 au §7.
- **18 nov. 2026, ~10h45 : LOTS v6.1 TERMINÉS — 140/140, SURVEILLANCE ARRÊTÉE.** Lot étendu 44/44 + rotations 96/96, 0 échec non récupéré, pipeline `2af5e5ce…c1c9` inchangé, aucun CSV modifié. Dernière reprise du journal des rotations : FIN 2026-11-18T15:43:15Z (16 runs, 0 échec) ; total vérifié par comptage des `master_results.json` (140/140).
- **18 nov. 2026, 10h45–11h30 : ROTATIONS LUES (§8.32) ET FLUX AUDITÉS (§8.33).** 96/96 runs lus avec l'extracteur corrigé sur copie (`extract_v61_rotations_v3.py`, SHA `91b165b7…` — les clés de la v2 étaient fausses pour la cascade et L7a : vraies clés `five_threshold_cascade.T_*`, `prediction_levels.L7a_coherence.consensus_direction/global_confidence`, `holographic_tension_state.falsification_vs_null.delta_vs_null`) et la lecture flux par flux (`rotations_flux_reading.py`, SHA `41937798…`, réutilisant `pistes_v61_flux_reading.py`). **Aucun des 48 contrôles ne sépare réel et nul** (MC, Delta, L7a, falsification). **Vérifié : Delta = d_div − d_sat, erreur max 0,0009 sur 96 runs** ; d_div prend des niveaux discrets (~3,0 DepMap ; ~4,7 / ~5,4 / ~5,8 TCGA), visités des deux côtés — les plus grands ΔDelta (IFNG +2,396) sont des différences de niveau. **Défaut systématique : les 48 CSV de rotation ont le contrôle aussi en flux** (13 colonnes, vérifié) — le doublon domine la lecture à T_0 dans le réel (d +2,00 à +4,69, 48/48). **3 blocs de co-expression réels, confirmés par tests directs top-12** (réel +0,7 à +2,2, nuls |d| ≤ 0,91) : estomac/mucus, immunitaire, réparation (XRCC1 anti-corrélé). **La chaîne KRAS ne réapparaît sous aucun autre contrôle** : sous PGC/CLDN18/MUC17/DPCR1, le bloc est haut et MUC16 bas dans les 12 premiers — l'anti-corrélation est réelle, la lecture « rupture » est propre à l'axe KRAS. **Audit §8.33 : 4 natures de flux seulement** (ARN tumeurs, ARN lignées, protéine tumeurs, dépendance CRISPR) ; allèle KRAS présent mais jamais en série v6.1 ; MAF TP53/SMAD4/CDKN2A présent, jointure PR→ACH non construite (le « 0 mutation » brut est un artefact de jointure absente) ; GISTIC présent, tests directs seulement ; prolifération calculée au §8.25 ; sous-type ICGC utilisé au §8.16, stade TCGA présent jamais utilisé ; déconvolution immunitaire absente. **Impossible nommé : pas de vrai temps, pas de single-cell, pas de spatial, pas de longitudinal.** Aucun run lancé, aucun CSV modifié, PDF non régénéré. Détail aux §8.32–8.33 ; lignes 37–38 au §7.
- **18 nov. 2026, 15h06–15h18 : TEST A — NON, LA CHAÎNE NE RÉAPPARAÎT PAS SOUS L'ORDRE PROLIFÉRATION.** Go de Zackary 15h06 (1re des 4 propositions, recommandée). Protocole gelé avant les runs (`PROTOCOL_testA_proliferation.md`) ; score prolifération = médiane des résidus MKI67/TOP2A/PCNA/CCNB1 (§8.25) ; vérification de reproduction v4 passée (écart max 1,776e-15, atol 1e-9) ; 2 runs v6.1 fast, exit 0/0 (`runs_v61_testa.log`, FIN 20h18 UTC). 1er lancement tué par un redémarrage du service, relance réussie, surveillance cron supprimée après 2/2. Pipeline : cascade réelle 0 / 0,73 / 3,73 / 24,57 / 24,57 (T_0 pas 7), MC 0,3638 contre nul 0,4587, Delta 3,798 contre 4,590, L7a UP 0,412 contre DOWN 0,196, falsification 0,737 contre 0,733, L7b FRAGILE des deux côtés — **ne sépare pas réel et nul**. Tests directs top-12 : PGC −0,57 sd (seul mouvement au-dessus du nul), DPCR1 −0,35 (sous son nul), CLDN18 −0,14, MUC16 −0,04 ; le reste du bloc monte (KRT20 +0,63, MUC2 +0,47, CEACAM5 +0,39). MUC16 monte doucement le long de l'axe (rho +0,277) sans saut au bout. Recouvrement top-12 prolif/KRAS : 1/12. PDF non régénéré. Détail au §8.34 ; ligne 39 au §7. Prochaines étapes : tests B (TP53/SMAD4/CDKN2A) et C (stade), en attente du go de Zackary.
- **18 nov. 2026, 15h21–15h26 : PHASE 2 — DISCRIMINATION RÉEL/NUL : LE PIPELINE NE SÉPARE PAS PAR SES SCORES PRINCIPAUX.** Go de Zackary 15h06 (2e des 4 propositions, après le test A). Protocole gelé du 16 nov. (`PROTOCOL_phase2_discrimination.md`) ; 8 indicateurs × 8 paires principales, critère ≥ 6/8, écarts > gigue ET direction cohérente ; lecture seule dans les `master_results.json` v6.1 déjà sur disque, 0 nouveau run ; extracteur `extract_phase2.py` (SHA `5eb3ac24…75aa`). **Delta 6/8** (réel > nul, mais échoue sur HP35, le témoin positif ; écarts ICGC +0,07, GSE62452 +0,15) ; **max_separation 6/8** (HP35 +1,65, PDAC +0,10 à +0,37 ; échoue sur GSE71729 +0,04 et GSE62452 −0,004) ; **MC best_score 1/8** (HP35 seul ; écarts PDAC +0,006 à +0,055, tous sous la gigue ±0,07, 7/8 positifs mais noyés) ; cohérence par flux 2/8 (le nul est parfois plus cohérent que le réel : immunitaire nul 1,00 contre réel 0,92) ; L7a 4/8 (direction majoritaire négative) ; falsification 4/5 disponibles (comparaison interne, pas au nul permuté ; direction inversée en annexe) ; T_0 8/8 et cascade 8/8 — triviaux par construction (écart > 0 ne peut échouer que sur égalité exacte). Annexe 23 paires : max_sep 16/23, MC 2/23, Delta 13/23 ; COAD réel refait depuis (lot 140/140) inclus. La phrase globale du protocole (« le pipeline ne sépare pas ») ne s'applique pas au pied de la lettre — deux indicateurs tiennent — mais elle reste vraie pour l'essentiel de l'instrument. Piste v6.2 proposée SEULEMENT (`PROTOCOLE_v6.2_proposition.md`, SHA `fcab5f55…08c6`) : hachage stable L5 d'abord, puis score max_separation, puis élucidation des niveaux Delta — rien construit, go séparé requis. PDF non régénéré (c'est l'étape 3). Détail au §8.35 ; ligne 40 au §7. Prochaines étapes : étape 3 (PDF + GitHub), puis étape 4 (enrichissements §8.33).
- **18 nov. 2026, 16h04 (heure de Montréal) : ÉTAPE 3 — PDF RÉGÉNÉRÉ ET VÉRIFIÉ, POUSSÉES GITHUB NON FAITES (approbation expirée).** Go de Zackary 15h06 (3e des 4 propositions). PDF régénéré avec la chaîne existante `.src/` (`build_appendix.py` puis `build_pdf.py`, WeasyPrint 70.0 — installé pour l'occasion dans `~/workspace/venv_weasyprint`, absent du Python système) : **457 pages A4, 10 205 579 octets, SHA-256 `b900d97250936ad98285b55573393e5e68c85efa14b21629c84459fd555e1b64`** (ancien 410 pages, 9 950 685 octets, SHA `3d7e3b48…b09ba`). Contenu : texte intégral §1–§10, §8.1–§8.35, journal jusqu'à la phase 2, annexes A–G. Vérifié par lecture du PDF : §8.30 à §8.35 présents, chiffres clés présents (daraxonrasib 13,2 contre 6,7 ; vopimetostat 82 % ; MRTX1133 p=0,0001 ; CA125 3 cohortes sur 4). Limite connue : la couverture du PDF porte encore la date du 16 nov. et « §8.1–§8.29 » (texte figé de `build_pdf.py`, chaîne non modifiée) — le corps, lui, est à jour jusqu'au §8.35. **Poussées GitHub PRÉPARÉES mais NON EFFECTUÉES :** snapshots prêts et vérifiés (PDAC : 38 fichiers — livre blanc, README mis à jour, 7 protocoles/provenances, 10 scripts, 18 résultats/tables ; Code : 3 fichiers — `universal_v6.1.0_cohen.py` SHA `2af5e5ce…a9c9`, `build_v6.1.py`, README mis à jour), têtes distantes vérifiées avant (PDAC `6327245c…`, Code `6a1d2130…`), mais **l'approbation d'écriture a expiré sans réponse après ~30 min d'attente — rien n'a été poussé, rien n'a changé sur GitHub, et aucune approbation n'est plus en attente.** À refaire après une nouvelle approbation : pousser les 38 fichiers PDAC puis les 3 fichiers Code, vérifier chaque push par relecture distante, puis noter les têtes de commits ici. Le PDF binaire, lui, ne va dans aucun dépôt (limite snapshot) et la création d'une Release GitHub reste impossible via l'outil — à faire à la main sur github.com si voulu.
- **18 nov. 2026, 16h05–16h20 : ÉTAPE 4 TERMINÉE — ENRICHISSEMENTS §8.33 : DEUX SÉRIES IMPOSSIBLES, UNE SÉRIE NÉGATIVE.** Go de Zackary 15h06 (4e et dernière des 4 propositions). Protocole gelé avant tout test (`PROTOCOL_enrichissements_833.md`). **(a) Allèles KRAS : série IMPOSSIBLE (max 23 lignées G12D, minimum fast 40).** Tests directs (45 lignées) : G12D/G12V plus KRAS-dépendantes que les autres allèles (G12D vs autres p=0,0017, d −1,42 ; G12V vs autres p=0,017, d −1,08 ; G12D vs G12V p=0,15, NS) ; PRMT5 indifférent à l'allèle (p 0,90–0,95) ; MRTX1133 recalculé G12D-spécifique (G12D vs G12V p=0,00039, d −1,52, moyennes −1,70 contre −0,37 identiques au §8.20). **(b) Jointure MAF PR→ACH revérifiée à l'identique (SHA de sortie `f3fa2bd2…63f36`)** — correction au §8.33 : elle était construite le 18 nov. en préparation, pas « non construite ». TP53 (38/7) : rien sur KRAS/PRMT5/ATR. SMAD4 (11/34) : KRAS p=0,089, tendance NS. CDKN2A (12/33) : PRMT5 p=0,014 (d +0,78) — **mais c'est du MTAP** : CN MTAP médiane +0,96 chez les mutées contre +0,29, 2/12 délétées contre 18/33 ; stratifié MTAP-intacte p=0,76 : l'effet disparaît — troisième confirmation que l'effet PRMT5 suit MTAP (§8.28/§8.29). Séries v6.1 impossibles aussi (plus grand groupe 38 < 40 ; ordre binaire dégénéré, non lancé). **(c) Série TCGA v4 ordonnée par CN MTAP (177/178 appariées, TCGA-FB-A4P6-01 sans GISTIC) : NON, la chaîne ne réapparaît pas.** 2 runs v6.1 fast exit 0/0 (FIN 21h18:51Z ; 1er lancement tué par un redémarrage du service, relance par la surveillance, cron filet supprimé après 2/2). Cascade réelle 0,54 / 60,74 / **72,77** / 92,11 / 92,11 (T_0 à CN −0,026, pas dans la zone délétée) ; MC 0,3512 contre nul 0,5153, Delta 3,805 contre 4,347, falsification 0,733 contre 0,816 — **le pipeline ne sépare pas réel et nul** ; seuls max_separation (0,339 contre 0,143) et le sens opposé de L7a (DOWN 0,423 contre UP 0,331) vont dans le sens réel — pistes, pas preuves. Tests directs top-12 (les plus délétées) : CEACAM5 +0,585 (seul au-dessus du nul), PGC −0,399, CR2 −0,570, MUC16 −0,143, CLDN18 +0,012, DPCR1 −0,078 — signature KRAS absente ; pentes douces le long de l'axe (CEACAM5 rho −0,390, MUC16 −0,270), sans saut au bout. La perte MTAP suit KRAS (rho −0,309, p=2,9e-05) sans porter la coupure. **Les 4 propositions du 18 nov. 15h06 sont faites** (test A, Phase 2, PDF, enrichissements) ; restent à retenter à la publication finale : les poussées GitHub de l'étape 3. Reste ouvert : série par stade TCGA (protocole C du brouillon, go à demander). PDF non régénéré. Détail au §8.36 ; lignes 41–42 au §7.
- **18 nov. 2026, 16h28–17h00 (heure de Montréal ; UTC 21h28–22h00) : PUBLICATION FINALE — PDF RÉGÉNÉRÉ ET VÉRIFIÉ, POUSSÉES GITHUB NON FAITES (approbation expirée, 2e fois).** Les 4 propositions du 18 nov. 15h06 sont faites (test A §8.34, Phase 2 §8.35, PDF étape 3, enrichissements §8.36). PDF régénéré avec la chaîne existante `.src/` (`build_appendix.py` puis `build_pdf.py`, WeasyPrint 70.0 ; `/usr/bin/python3.12` utilisé pour les deux scripts car le `python3` de l'unité systemd-run ne voyait pas le module `markdown` installé en site-packages utilisateur — chaîne non modifiée, deux premiers lancements en échec pour cette raison, 3e réussi) : **471 pages A4, 10 266 464 octets, SHA-256 `12c3622867d6d2e2d2175aad432ce113c82411cf45bb726a7fa119a26336f346`** (ancien 457 pages, 10 205 579 octets, SHA `b900d9725…`). Contenu : texte intégral §1–§10, §8.1–§8.36, journal jusqu'à l'étape 4, annexes A–G. Vérifié par lecture du PDF (`pdftotext`) : §8.30 à §8.36 présents, chiffres clés présents (daraxonrasib 13,2 contre 6,7 ; vopimetostat 82 % ; MRTX1133 p=0,0001 ; CA125 3 cohortes sur 4 ; 9,5 contre 23,8 mois). Limite connue : la couverture du PDF porte encore la date du 16 nov. et « §8.1–§8.29 » (texte figé de `build_pdf.py`, chaîne non modifiée) — le corps, lui, est à jour jusqu'au §8.36. **Poussées GitHub PRÉPARÉES mais NON EFFECTUÉES (2e expiration) :** snapshots prêts et vérifiés (PDAC : 48 fichiers — livre blanc §8.30–§8.36, README mis à jour §8.36, 2 provenances + 3 scripts + 6 résultats de l'étape 4 dont `mtap_direct_tests.csv` nouvelle version — attention : ce chemin écrase la version §8.29 du même nom, conservée dans l'historique git à `6327245c` ; `MANIFEST_SHA256.txt` exclu de la poussée, contenu distant différent et provenance locale non vérifiable ; Code : 3 fichiers — `universal_v6.1.0_cohen.py` SHA `2af5e5ce…a9c9`, `build_v6.1.py`, README mis à jour ; manifestes persistants `hidden_files/pdac-paths.txt` et `code-paths.txt`), têtes distantes vérifiées avant et après (PDAC `6327245c…`, Code `6a1d2130…`, inchangées), mais **l'approbation d'écriture a de nouveau expiré sans réponse après ~30 min d'attente (`approval_expired`, approval_id `connector-attempt-17bb5acfd294dbf8717e81a1f1639762714dc0d89b49d46b6fae0b04d7fb70e5`) — rien n'a été poussé, rien n'a changé sur GitHub, aucune approbation n'est plus en attente.** À refaire après une nouvelle approbation : pousser les 48 fichiers PDAC puis les 3 fichiers Code, vérifier chaque push par relecture distante, puis noter les têtes de commits ici. Le PDF binaire ne va dans aucun dépôt (limite snapshot) et la création d'une Release GitHub reste impossible via l'outil — à faire à la main sur github.com si voulu. Cette entrée n'entrera dans le PDF qu'à la prochaine régénération.
- **14 nov. 2026 :** preuve Cohen vs Cliff complète (4/4 cascades identiques) ; v6 construite et vérifiée sur HP35.
- **2 oct. 2026 :** synthèse des trois validations PDAC (R1/R2/R3) ; pseudo-temps invalidé ; projet requalifié en stratification pronostique.

---

- **18–19 nov. 2026 : v6.2 CONSTRUITE, VALIDÉE, TESTÉE — §8.37.** Go de Zackary 18 nov. 18h07 (« pousser mon pipeline, je veux vraiment qu'il soit en capacité de trouver un remède, pas juste montrer un axe »). Protocole gelé avant tout code (`PROTOCOL_v6.2.md`, SHA `6e9324a2…dfad` — l'annonce `fb27b39a…` de son auteur ne correspond pas au fichier, le SHA mesuré fait foi). Construction sur copie : `build_v6.2.py` (SHA `5348636e…fa0`), un seul changement — `hash(metric)` remplacé par `hashlib.sha256` stable dans le seed L5 (ligne 8985), + `import hashlib` + `VERSION_MASTER` v6.2.0 ; diff 3 hunks, compilation OK, v6.2 SHA `f07567c4…3abf`, v6.1 et v6 inchangées ; 1er essai arrêté sur assertion (la note d'en-tête contenait elle-même la chaîne `hash(metric)`), reformulée, reconstruction propre. **Validation 20/20 exit 0** (10 runs fast × 2, processus séparés, 3 redémarrages machine, reprise par le lanceur) : cascades identiques à la v6.1 sur 10/10, L7a finis sur les petites cohortes, **gigue mesurée = 0,0000 sur tous les indicateurs** — les JSON ne sont pas identiques octet pour octet, mais les seules divergences sont les chemins runtime et les champs worker_budget (RAM au lancement) : 0 champ scientifique divergent. **Discrimination : S_sep = max_separation × stability atteint 6/8** (barre du protocole), 16/23 en annexe — exactement max_separation en v6.1, mêmes paires ; MC 7/8 et max_separation 7/8 en v6.2 (1/8 et 6/8 en v6.1) uniquement parce que la gigue appliquée est passée de 0,07 à 0,00 mesurée — avec le forfait 0,07, les verdicts seraient ceux de la v6.1. **Delta NON ÉLUCIDÉ** (222 runs ; meilleure combinaison 80,2 % / 61,7 %, sous les 90 % ; DFA −38,16 retrouvé, sans effet sur d_sat). **Verdict : la v6.2 ne sépare pas mieux que la v6.1 ; elle sépare pareil, et de façon déterministe.** Adoption : faite le 19 nov. 2026 — voir l'entrée du 19 nov. 2026 ci-dessous (v6.2 version de travail, v6.1 référence). Détail au §8.37 ; ligne 43 au §7.
- **18 nov. 2026, 18h07 : POUSSÉES GITHUB RÉUSSIES (correction des entrées 16h04 et 16h28–17h00, qui disaient « approbation expirée, rien poussé »).** Après une nouvelle approbation de Zackary, poussées et vérifiées par relecture distante : PDAC commit `8c88810b` (livre blanc §8.30–§8.36, 48 fichiers), Code commit `70f52ad5` (v6.1, SHA `2af5e5ce…c1c9`). Les deux dépôts restent privés à ce moment-là. **18 nov. 19h10 : Zackary annonce un nouveau dépôt, https://github.com/FindPrint/tlogNext-cancer-pdac (commit initial `baf1e02f`, vérifié), et qu'il a mis les deux anciens dépôts PUBLICS lui-même — toute publication future (PDF avec §8.37, v6.2 si adoptée) va dans `tlogNext-cancer-pdac`, pas dans les anciens ; l'App GitHub devra être vérifiée installée sur le nouveau dépôt avant de pousser (voir `runs/pdac-v6/PUBLICATION_tlogNext.md`).**
- **19 nov. 2026, ~05h47 : ADOPTION v6.2 — Zackary dit « Lance tout cela » (feu vert pour les 3 chantiers : adoption, PDF, GitHub). La v6.2 devient la version de travail ; la v6.1 devient la référence ; la v6.0.0 reste la référence historique.** Les trois SHA revérifiés inchangés avant adoption : v6 `bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773`, v6.1 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`, v6.2 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` ; aucun code modifié. Consigné : en-tête du livre blanc, ligne 43 au §7, §8.37 (intro, §8.37.5, provenance) et `PROVENANCE_v6.2.md` (addendum du 19 nov. 2026). Rappel du verdict adopté : la v6.2 ne sépare pas mieux que la v6.1 — le gain est le déterminisme (gigue L5 = 0), S_sep 6/8 = max_separation v6.1, Delta non élucidé. **PDF régénéré le 19 nov. 2026 avec ce §8.37 (chaîne `.src/` : `build_appendix.py` puis `build_pdf.py`, WeasyPrint 70.0) : 500 pages A4, 10 398 134 octets, SHA-256 `0d53ad1aa66ae332516ba14fa4a84175f4d560695c5811f7221039669dbf82ef`** (ancien 471 pages, 10 266 464 octets, SHA `12c36228…`) ; couverture corrigée (date 19 nov. 2026, §8.1–§8.37, nouveau dépôt `tlogNext-cancer-pdac`) ; §8.37 vérifié présent par lecture du PDF (`pdftotext`, 54 occurrences de « 8.37 »). **Poussée GitHub NON FAITE le 19 nov. 2026 : approbation d'écriture expirée sans réponse après ~30 min d'attente (`approval_expired`, approval_id `connector-attempt-a6d281f83b6bb0a4878e3f5593c007415af7b191885e3d5ca50422fba2dd1f7f`) ; rien n'a été poussé, tête distante vérifiée inchangée (`baf1e02f`, commit initial).** Snapshot prêt et vérifié (8 fichiers, 991 746 octets, UTF-8 : livre blanc, PROTOCOL_v6.2, PROVENANCE_v6.2, build_v6.2, 3 tables v6.2, code v6.2) — à retenter après une nouvelle approbation de Zackary, sans relancer en boucle. Ce premier PDF portait au §8.37 une ligne « Ce qui manque » affirmant la poussée faite — fausse ; PDF reconstruit le 19 nov. 2026 avec la ligne corrigée (SHA du PDF reconstruit dans `PROVENANCE_v6.2.md` §7 ; cette phrase n'entrera dans le PDF qu'à la prochaine régénération).
- **19 nov. 2026, ~06h40 (heure de Montréal) : §8.38 et §8.39 écrits au livre blanc** (go de Zackary « Lance tout cela », 19 nov. 2026 ~05h47). **§8.38 — S_sep appliqué aux bras existants : S_sep ne classe aucun bras autrement que max_separation en v6.1** (29/29 paires identiques, max |Δ| = 0,0000 ; principales 6/8 sous la règle 0,07, 7/8 sous la règle gigue 0 — le gain vient uniquement du passage de la gigue 0,07 à 0,00, pas de l'instrument ; MTAP : S_sep +0,1968 mais MC −0,1642 et Delta −0,5416 inversés, contradiction non résolue ; immunitaire ICGC −0,2200 inversé). **§8.39 — Élucidation de Delta : NON ÉLUCIDÉ** (meilleur score honnête hold-out 87,9 % paires / 81,8 % valeurs, sous les 90 % exigés ; structure des rangs presque figée — GraphDimension et PersistentHomology toujours les deux plus basses, LocalPCA toujours 3e ou 4e — mais le choix entre les trois magnitudes restantes varie librement dans chaque groupe ; la permutation réel/nul ne change pas la paire, 44,6 %). Sections rédigées dans `section_8.38_ssep.md` (SHA `92e62bbb…`) et `section_8.39_delta.md` (SHA `e9f1f1ca…`), fusionnées au livre blanc par le coordinateur ; lignes 44–45 au §7. PDF régénéré après fusion (pages et SHA dans `PROVENANCE_v6.2.md`, addendum du 19 nov. 2026) ; poussée GitHub dans `tlogNext-cancer-pdac` toujours en attente d'une nouvelle approbation de Zackary (première tentative expirée, rien poussé).

---

*Fin de la version initiale du livre blanc — 15 novembre 2026. Le reste se mesure.*
