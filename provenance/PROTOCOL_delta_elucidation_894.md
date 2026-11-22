# PROTOCOLE GELÉ — §8.94 : élucider Delta, nouvelle tentative

Date de gel : 21 novembre 2026, avant tout calcul neuf et tout run neuf.
Statut : **PROTOCOLE GELÉ. Aucune modélisation lancée avant ce gel. Toute déviation arrête le travail et se consigne, elle ne se corrige pas en silence.**
Coordinateur : TagPrint. Go de Zackary « Faite tout cela », 21 nov. 2026 11h36, piste 2/4.
Dossier : `~/workspace/runs/pdac-v6/`.
Pipeline : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256 vérifié avant gel `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` (v6.1 `2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`, revérifiés inchangés le 21 nov. 2026). v6.2, v6.1, v6 ne sont JAMAIS modifiées.
Références : livre blanc §8.39 (222 runs, critère 90 % hold-out), §8.42 (voie « résumés de flux » close), §8.50.4 (M1), §8.53.4 (M2), §8.57 (séries complètes), §8.62 (loi d'échelle en n), §8.63 (M1 expliqué, M2 partiel), §8.73 (pic étroit NON ÉLUCIDÉ), §8.75 (M2 clôturé NON CONCLUANT), §8.90.1.2 (batterie entière = verdict).

## 0. Question

Delta est NON ÉLUCIDÉ aux §8.39, §8.42, §8.57, §8.62 — le mécanisme qui choisit le niveau n'est pas compris. Cette tentative reprend les pistes NON CLOSES des tentatives précédentes et ajoute trois angles neufs, tous gelés ici avant tout calcul.

## 1. Inventaire des pistes non closes (relu, jamais rouvert sans protocole)

| Piste | Statut au 21 nov. 2026 | Ce qui reste ouvert |
|---|---|---|
| §8.39/§8.42 — identité de la paire médiane + valeur d_div | NON ÉLUCIDÉ (hold-out < 90 %) | Le mécanisme qui choisit LEQUEL des trois estimateurs hauts {MFA, LevinaBickel, PCAIntrinsic} est le plus petit, et à quelle magnitude |
| §8.50.4 M1 — config (28, 27, 6) → MC haut, Delta bas | EXPLIQUÉ au §8.63 (M1a + M1b) | M1c : MC haut et Delta bas ont-ils une cause commune ? (qualifié, non tranché) |
| §8.53.4 M2 — l'optimiseur choisit-il sa config ? | PARTIEL au §8.63, clôturé NON CONCLUANT au §8.75 | M2d : réplication hors échantillon (lot frais ICGC s31–s40) — l'optimiseur maximiserait MC sur 12 configs fixes par n sans rien reconnaître du réel ; la réplication n'a pas tranché |
| §8.57 — modéliser depuis les séries entières | NON ÉLUCIDÉ (hold-out < 90 %, piège de circularité nommé) | Les séries `df_feat.csv` portent-elles une signature du niveau choisi, sans recalculer l'estimateur ? |
| §8.62 — loi d'échelle en n | NON TROUVÉE (F2 R² = 0,673 < 0,80 ; LOCO R² = −0,005) ; en revanche 4 estimateurs ont une loi en n (Katz, Petrosian, Sevcik, GraphDimension), qui ne portent pas Delta | Le résidu Delta − F2(ln n) sépare-t-il réel de nul ? (critère (ii) du §8.62 jamais testé seul, la loi ayant manqué) |
| §8.63 M1 — écart +0,7 entre w=27 et w=30 | EXPLIQUÉ (Delta bas vient de w=27) | **Delta à w ÉGAL** : à w fixé, Delta sépare-t-il réel de nul ? Jamais testé |
| §8.73 — pic étroit : qu'est-ce qui le déclenche ? | NON ÉLUCIDÉ (ni bloc extrême, ni ligne unique) | Le déclencheur (position de split ? extrémité non signée ? cohérence de signe entre flux ?) |

## 2. Données (détenues, relues, jamais recalculées sans vérification)

- `v62_delta_levels.csv` : 222 runs (156 v6.1 + 66 v6.2), 223 lignes avec en-tête — ensemble gelé des §8.39/§8.42/§8.57, repris tel quel pour comparabilité.
- Ensemble B (§8.62) : 31 runs v6.2 fast (HP35 réel/nul, LUAD, TCGA v4, sous-échantillons préfixe + stride).
- `df_feat.csv` présent dans 222/222 dossiers de run (120 lignes, Progress 0 → 100) ; `fluxes_raw.csv` présent dans 222/222 ; `scan_curve.json` disponible.
- Vérification préalable (dans le script, avant modélisation) : d_div recalculé depuis les médianes parsées = d_div du CSV à 10⁻³ près sur 222/222 ; recomputation `raw_median` depuis `df_feat.csv` = `master_results.json` à 10⁻⁶ près ; sinon arrêt et diagnostic (comme §8.57 §4.1).

## 3. Angles neufs gelés (ordre d'exécution)

### A1. Delta à w égal (neuf, suite directe de §8.63 M1)
- Sur les 222 runs + ensemble B : extraire, pour chaque run, Delta (d_div − d_sat) ET la valeur de w choisie par l'optimiseur, ET les médianes d_div/d_sat à w fixé (w=27 et w=30, les deux valeurs du §8.63, lues dans `df_feat.csv` / `scan_curve.json` — pas de nouveau run pipeline, lecture seule des sorties détenues).
- Test : à w=27 fixé et à w=30 fixé séparément, l'écart Delta réel−nul (sur les paires dont les deux côtés sont détenus) dépasse-t-il 0,10 sur ≥ 90 % des paires ? Et le niveau choisi (d_div) à w égal est-il prédictible à ±0,10 sur ≥ 90 % des runs en hold-out (même critère que §8.39) ?
- Si oui sur l'un des deux w : le mécanisme est « le niveau est choisi par w, pas par le contenu » — à nommer et à vérifier sur l'ensemble B (transfert).

### A2. Delta résiduel après loi en n (neuf, suite du §8.62)
- Résidu R = Delta − F2(ln n) (F2 = meilleure forme du §8.62, R² = 0,673, coefficients gelés du §8.62, NON ré-estimés ici — sinon le test serait circulaire).
- Test : sur les 106 paires réel/nul détenues (§8.62), |R_réel − R_nul| ≤ 0,10 sur ≥ 90 % des paires ET |moyenne| ≤ 0,10 ? Si oui : Delta ne porte rien au-delà de n (le résidu est du bruit) — c'est une ÉLUCIDATION NÉGATIVE, à nommer comme telle. Si non (le résidu sépare) : le résidu devient le candidat discriminateur, et le mécanisme est cherché dans le résidu (A3).

### A3. Structure des flux (neuf)
- Prédicteurs candidats, calculés depuis `fluxes_raw.csv` + `df_feat.csv` SANS recalculer les estimateurs (piège de circularité du §8.57 §3) : p (nombre de flux), n, dispersion inter-flux (écart-type des médianes de flux), corrélation moyenne intra-famille, part de variance du premier axe (PCA sur les flux bruts), asymétrie (skew) moyenne des flux.
- Test : ces prédicteurs prédisent-ils (a) l'identité de la paire médiane sur ≥ 90 % des runs ET (b) d_div à ±0,10 près sur ≥ 90 % des runs, en hold-out par cohorte (LOCO, comme §8.62) ? Un modèle en échantillon seul ne compte pas.

### A4. Pic étroit : déclencheur (reprise du §8.73, résidu ouvert)
- Reprendre les critères P1/P2 du §8.73 (bloc porte le pic / ligne unique) sur les 20 nuls frais du §8.73 + les runs MTAP rob-on : le déclencheur est-il la position du split (extrémité non signée, sans cohérence de signe entre flux) ?
- Critères gelés du §8.73 repris tels quels (P1 ≥ 9/11, P2 ≥ 9/11) ; si les deux échouent, le déclencheur est consigné « non élucidables par cette voie » et le verdict global reste NON ÉLUCIDÉ.

## 4. Barres gelées (identiques au §8.39, §5.4 — la barre ne bouge pas)

**ÉLUCIDÉ** si ET SEULEMENT SI (a) l'identité de la paire médiane est prédite sur ≥ 90 % des runs en hold-out (LOCO par cohorte) ET (b) la valeur de d_div est prédite à ±0,10 près sur ≥ 90 % des runs en hold-out — avec le mécanisme NOMMÉ (quelle variable choisit le niveau, et comment) et VÉRIFIÉ sur l'ensemble B (transfert ≥ 90 % à ±0,10).
**ÉLUCIDATION NÉGATIVE** (compte comme élucidation, à nommer ainsi) si A2 montre que le résidu Delta − F2(ln n) est du bruit (≥ 90 % des paires |Δrésidu| ≤ 0,10) ET A1 montre qu'à w égal Delta ne sépare pas : alors le mécanisme est « Delta est une fonctionnelle de n et de w, sans contenu de flux » — vérifié sur B.
**NON ÉLUCIDÉ** sinon, avec la liste exacte de ce qui a été exclu cette fois (chaque angle : chiffres, pas d'adjectifs).
Aucune repondération, aucun nouveau prédicteur, aucun changement de tolérance après coup. Un modèle en échantillon ne compte jamais ; seul le hold-out compte.

## 5. Ce qui n'est PAS fait ici

- Aucun nouveau run pipeline (tous les angles lisent des sorties détenues ; si un angle exige un run neuf, il s'arrête et le besoin est consigné, pas lancé).
- Aucun recalcul d'estimateur (circularité §8.57) ; `csd_fractal_estimators.json` NON utilisée (dérivée du même paysage `df_feat`).
- Aucune conclusion importée d'autres bras ; Delta n'est jamais présenté comme discriminateur tant qu'il n'est pas élucidé.

## 6. Livrables

- `v62_delta_elucidation_894.py` + log de vérification préalable (d_div à 10⁻³, raw_median à 10⁻⁶).
- `delta_894_results.json` + CSV bruts (par run : w, d_div, d_sat, Delta, résidu R, prédicteurs A3, verdicts A1–A4).
- Section `section_8.94_delta_elucidation.md` (fichier séparé ; livre blanc NON édité directement ; PDF NON régénéré ; rien poussé).
- Provenance `PROVENANCE_894.md` (SHA des scripts et des fichiers d'entrée ; coefficients F2 repris du §8.62 avec leur SHA).

## 7. Limites déclarées d'avance

- Les 222 runs sont un ensemble gelé de comparabilité, pas un échantillon représentatif : les 185 dossiers v62 supplémentaires (§8.47, §8.53) restent HORS ensemble, comme au §8.57.
- A1 lit w dans des sorties détenues : si w n'est pas récupérable à 10⁻⁶ près sur tous les runs, A1 est consigné « non testable sur ces données » et le chantier continue sur A2–A4.
- Une élucidation négative reste une élucidation du mécanisme, pas une preuve que Delta est inutile partout : elle dit ce que Delta EST (fonction de n et w), pas ce qu'il ne pourra jamais être.

---
## ADDENDUM — Correction de Zackary du 21 novembre 2026, 12h03 (portée : tout le projet, précisée 12h04)
**Ajouté le 21 novembre 2026, après le gel du protocole — le texte gelé
ci-dessus est intact, cet addendum l'applique.**

**1. Contrôle jamais analysé.** Aucun run pipeline dans cette piste
(Tier 1 = lecture seule des sorties détenues). Le Tier 2 (réplique à
w = 27/30) reconstruit `df_feat` depuis les CSV détenus avec les
fonctions DU PIPELINE (`replica_w_894.py`, calque de
`replica_delta_863.py`) : la colonne de contrôle (`step`) est exclue
des flux analysés par construction (pipeline, ligne 6787 :
`c != control_col`), et la variable d'ordre (KRAS pour les paires
PDAC) est absente des colonnes de flux des CSV sources — vérifié le
21 novembre 2026 sur les 15 CSV des paires principales et A2.
**Règle respectée.** Le défaut connu des 96 rotations d'origine
(§8.32) ne concerne pas cette piste ; traité au §8.97, partie 1.

**2. Contrôles non monotones.** Aucun seuil n'a été écarté dans le
Tier 1 au motif de non-monotonie : A1 lit Delta à w égal, A2 le
résidu F2, A3 la structure des flux, A4 le pic étroit — aucun de ces
angles ne trie ni n'exclut un seuil parce que son contrôle serait non
monotone. La nuance du 21 novembre 2026 est appliquée : si un contrôle
non monotone donne un seuil différent, c'est de l'information, pas
une erreur. (Le contrôle ici est `step`, monotone par construction ;
la nuance porte sur la lecture, pas sur un tri.)

**3. Analyse, pas prédiction.** Le verdict (ÉLUCIDÉ / NON ÉLUCIDÉ)
décrit ce que les angles testés montrent sur les données détenues —
il ne prédit rien. Aucune formulation de prédiction dans cette piste.
