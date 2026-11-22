# PROTOCOLE GELÉ — §8.96 : universalité — le pipeline sur un autre cancer

Date de gel : 21 novembre 2026, avant tout téléchargement nouveau, toute copie et tout calcul.
Statut : **PROTOCOLE GELÉ. Aucune donnée nouvelle téléchargée, aucun CSV de flux construit, aucun run lancé avant ce gel. Toute déviation arrête le travail et se consigne, elle ne se corrige pas en silence.**
Coordinateur : TagPrint. Go de Zackary « Faite tout cela », 21 nov. 2026 11h36, piste 4/4.
Dossier : `~/workspace/runs/pdac-v6/`.
Pipeline : `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256 vérifié avant gel `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` (v6.1 `2af5e5ce…c1c9`, v6 `bb8bbdba…c0773`, revérifiés inchangés le 21 nov. 2026). v6.2, v6.1, v6 ne sont JAMAIS modifiées.
Références : livre blanc §8.27 (pan-cancer : CA125 plat poumon/côlon ; programme KRAS du côlon différent), §8.33 (pas d'autre cancer que PAAD / LUAD / COAD / GBM / UVM), §8.62 (série LUAD n=45…515, 31 runs), §8.90.4 (volet 4 : le mot « universel » est exagéré tel quel), `PROTOCOL_pancancer.md`, `PROVENANCE_pancancer.md`.

## 0. Question

Tout le travail PDAC est pancréas-spécifique. Le pipeline sépare-t-il le réel du nul ailleurs, et trouve-t-il une structure analogue ? Deux bras, dans cet ordre : (A) LUAD — données déjà détenues, axe analogue déjà construit ; (B) BRCA — données à sourcer, construction neuve. La question porte sur l'instrument, pas sur le cancer : aucune affirmation clinique.

## 1. Bras A — TCGA-LUAD (données DÉTENUES, rien à télécharger)

### 1.1 Source (reprise telle quelle, jamais re-téléchargée ici)
- Broad GDAC Firehose stddata 2016-01-28, fichier `LUAD.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt`, URL `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/LUAD/20160128/`, taille 47 043 687 octets, MD5 observé `4c36eec3f6df75630292c5a569cfc8f4` (aucun MD5 de référence publié par Firehose ; MD5 observé consigné dans `PROVENANCE_pancancer.md` et vérifié à chaque lecture par `build_fluxes_pancancer.py`).
- Matrice : 20 503 gènes × 576 échantillons ; retenus : 515 tumeurs primaires (code TCGA 01) ; transformation log2(RSEM normalisé + 1).
- Flux : `pdac_luad_fluxes.csv`, SHA-256 `d407849b991aa758398c85796662f51787cc54bbac62e824308f29787238091e`, 515 lignes, 12 flux — les 12 MÊMES gènes que PAAD v4 (PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16), 12/12 présents, 0 NaN, aucun remplacement.
- Nul : `pdac_luad_fluxes_nul.csv`, SHA-256 `93766e8c14e140f6b7946b67db9c0f2ad4beff0c1790d84a9c1357c56f978a6b`, mêmes lignes permutées, graine 42.
- Axe : **expression KRAS brute croissante ; KRAS = axe, jamais un flux** (KRAS log2 : n=515, min 8,921, médiane 10,4127, max 14,8647). C'est l'axe analogue exact de PAAD (même gène pilote, même sens) — la comparaison est donc directe, pas analogique.

### 1.2 Ce qui est déjà couru (relu, jamais recalculé ici)
- `results_fast_pancancer_luad[_nul]` (v6.0/v6.1, §8.27) : réel n=515, cascades 0,76 / 46,69 / 68,62 / 80,82 / 80,82, Delta 2,511, L7a UP 42,11 % ; nul : Delta 2,497, L7a DOWN 23,25 % ; MC prédictif 48 scénarios ; L7b FRAGILE sur réel et nul alike (non-informatif, règle du projet).
- `results_fast_v62_luad[_nul]` + série `results_fast_v62_862_luad_n45/n70/n100/n145/n178/n285/n515` (§8.62, ensemble B) : sous-échantillons PRÉFIXE (les k premières lignes, `step` réécrit 0..k−1) — relus tels quels.
- COAD, bras témoin déjà détenu : `pdac_coad_fluxes.csv` (SHA `79e23912158dfe1a4acabde40f9b0e59cff5fdee8bd1fb02d2010aded528281f`, n=285), nul graine 42, runs pancancer (réel Delta 4,619 ; nul 4,599). COAD est lu en témoin, pas en bras principal : son programme KRAS est déjà connu différent (§8.27).

### 1.3 Runs neufs du bras A (les seuls runs pipeline de ce chantier, lot systemd)
- 2 runs v6.2 fast : LUAD réel n=515 (`pdac_luad_fluxes.csv`) + LUAD nul graine 42 — commande identique aux lots précédents (`python3 universal_v6.2.0_cohen.py --input <csv> --mode fast --output <dir>`), lancement via `systemd-run`, journal des exit codes. ~10 min.
- 2 nuls frais LUAD (graines gelées ici, jamais utilisées dans ce projet : 9601, 9602), mêmes 515 lignes permutées par ligne, 2 runs v6.2 fast. ~10 min.
- Gate des flux (avant les runs) : 12/12 gènes présents avec ≥ 50 valeurs valides, 0 NaN dans les flux — déjà vérifié au §8.27 (12/12, 0 NaN) et re-vérifié par script avant les runs ; si le gate échoue, arrêt et diagnostic.
- n minimum : 40 (minimum fast v6.2) — ici n=515, largement au-dessus ; la série n=45…515 du §8.62 est relue en sensibilité (le pipeline sépare-t-il à petit n en LUAD comme en PAAD ?).

### 1.4 Lecture gelée du bras A
- Batterie entière par paire (§8.90.1.2) : maxsep, MC, Delta, L7a, falsification, F1/F2, tests de bruit — `maxsep` ne porte jamais le verdict seul.
- **CONFIRME (partiellement)** si LUAD réel vs nul graine 42 : écart maxsep > 0,07 ET écart positif sur MC ou Delta ou L7a dans le même sens (au moins 2 indicateurs de la batterie au-dessus de leur plancher, directions concordantes) — avec les 2 nuls frais en confirmation (au moins 1/2 au-dessus du plancher).
- **CONFIRME (totalement)** si en plus la structure analogue est trouvée : le bloc estomac/mucus (ou un bloc de co-expression équivalent) varie avec KRAS en LUAD comme en PAAD (test direct de corrélation, mêmes gènes, mêmes seuils que §8.33/§8.66).
- **NON** sinon — dit plainement, sans forcer : un NON en LUAD ne retire rien aux résultats PAAD, il borne l'universalité.
- Le bras COAD est lu avec la même batterie, en témoin : un NON en COAD était déjà attendu (§8.27) et ne compte ni pour ni contre LUAD.

## 2. Bras B — TCGA-BRCA (données À SOURCER, construction neuve)

### 2.1 Repérage des sources (fait avant le gel — lecture seule, 0 téléchargement)
- Source visée : **Broad GDAC Firehose stddata 2016-01-28, cohorte BRCA** — même millésime que LUAD/COAD/PAAD, pour comparabilité directe. URL patron (même structure que LUAD, à vérifier avant téléchargement) : `https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/BRCA/20160128/` ; fichier attendu : `BRCA.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt`.
- Source de secours si Firehose 2016-01-28 BRCA est indisponible : GDC (TCGA-BRCA, RNA-seq STAR counts) — à consigner comme changement de source, avec URL, SHA et date, jamais comme équivalent silencieux.
- **État au gel : BRCA n'est détenu NULLE PART dans ce projet** (0 occurrence dans DATA_SOURCES.md et ses annexes ; seuls des flux PARP BRCA1/BRCA2 existent, sur TCGA-PAAD, pas sur TCGA-BRCA — ce ne sont pas des données BRCA). Le bras B est donc une construction neuve complète : téléchargement + vérification MD5/SHA + construction des flux + gate + runs.
- Gène pilote pour l'axe : **à choisir APRÈS lecture de la matrice, AVANT tout run, et consigné par addendum daté au présent protocole** — candidats gelés ici : ESR1 (récepteur œstrogène, définit les sous-types BRCA) ou TP53 (muté dans ~30 % des BRCA, pilote fréquent) ou la prolifération (score de prolifération, comme Test A §8.34). Le choix se fait sur (a) la présence du gène avec ≥ 50 valeurs valides, (b) sa variance inter-tumeurs, (c) sa pertinence comme axe de classement — jamais sur le résultat d'un run. KRAS n'est PAS l'axe en BRCA (KRAS rarement pilote du sein ; imposer KRAS serait importer une hypothèse PAAD).

### 2.2 Construction des flux (après téléchargement, avant tout run)
- 12 flux adaptés au cancer choisi : les 12 gènes PAAD v4 d'abord testés tels quels (gate : 12/12 présents avec ≥ 50 valeurs valides, 0 NaN) ; si un gène est absent ou sous le seuil, remplacement documenté par la liste de remplacement v3 hors sexe (même règle que PAAD v3), avec le remplacement nommé et justifié gène par gène — jamais de remplacement silencieux.
- Transformation : log2(RSEM normalisé + 1), comme LUAD/COAD ; échantillons : tumeurs primaires (code TCGA 01) seulement ; n minimum 40 (minimum fast v6.2), visé ≥ 100.
- Nul : mêmes lignes permutées par ligne, graine 42 (même règle que tout le projet) + 2 nuls frais (graines 9601, 9602, mêmes que le bras A — des graines, pas des données, la réutilisation est légitime).
- Script de construction neuf, `build_fluxes_brca_896.py`, calqué sur `build_fluxes_pancancer.py` (vérification MD5/SHA à chaque lecture).

### 2.3 Runs et lecture du bras B
- 4 runs v6.2 fast (réel + nul 42 + 2 nuls frais), lot systemd, ~20 min.
- Lecture gelée identique au bras A (§1.4) : batterie entière, CONFIRME (partiel/total) ou NON, mêmes seuils (maxsep > 0,07 + 1 autre indicateur concordant ; nuls frais ≥ 1/2).
- Si le téléchargement BRCA échoue (source indisponible, accès refusé, matrice illisible) : le bras B est consigné **PISTE FERMÉE (données non accessibles)** avec les 5 contrôles d'accès nommés, comme §8.91 — 0 run, 0 CSV, et le §8.96 porte sur le bras A seul. Aucune donnée n'est inventée, aucun substitut non sourcé n'est utilisé.

## 3. Ce qui n'est PAS fait ici

- Aucun autre cancer que LUAD (bras A), COAD (témoin) et BRCA (bras B) ; GBM/UVM (§8.33) ne sont pas rouverts.
- Aucune comparaison PAAD vs LUAD au niveau d'un seul score : la batterie entière, paire par paire.
- Aucune recommandation clinique, jamais ; données d'essais seulement, à discuter avec un oncologue (règle de sécurité §8.90).
- Aucune conclusion importée : le programme KRAS du côlon est différent (§8.27) — ce qui est vrai en PAAD ne se transporte pas, il se re-teste.

## 4. Livrables

- Bras A : `luad_896_verify.json` (gate + SHA re-vérifiés), `luad_896_fresh.json` (4 runs, exit codes, batterie par run), `luad_896_table.json`.
- Bras B : `brca_896_download.json` (URL, taille, MD5/SHA observés), `pdac_brca_fluxes.csv` (+ SHA) et `pdac_brca_fluxes_nul.csv` (+ SHA), `brca_896_fresh.json`, `brca_896_table.json`.
- Section `section_8.96_universalite.md` (fichier séparé ; livre blanc NON édité directement ; PDF NON régénéré ; rien poussé).
- Provenance `PROVENANCE_896.md` (sources, SHA, graines, lots systemd ; choix de l'axe BRCA par addendum daté).

## 5. Limites déclarées d'avance

- LUAD et PAAD partagent les 12 mêmes flux : une structure analogue trouvée en LUAD pourrait tenir aux gènes choisis, pas au cancer — le bras BRCA (flux adaptés) est le vrai test d'universalité, LUAD est le test de transport direct.
- Les sous-échantillons préfixe du §8.62 ne sont pas des cohortes indépendantes : ils servent la sensibilité en n, pas des paires nouvelles.
- Firehose 2016-01-28 est un millésime figé (2016) : les résultats BRCA/LUAD portent sur ces données, pas sur TCGA actuel ; c'est un choix de comparabilité, consigné, pas une limite cachée.

---
## ADDENDUM — Correction de Zackary du 21 novembre 2026, 12h03 (portée : tout le projet, précisée 12h04)
**Ajouté le 21 novembre 2026, après le gel du protocole — le texte gelé
ci-dessus est intact, cet addendum l'applique.**

**1. Contrôle jamais analysé.** Vérification faite le 21 novembre
2026 : bras A LUAD — les 4 runs étaient déjà lancés au moment de la
correction ; vérification faite immédiatement sur les fichiers
construits (pas de relance à l'aveugle) : `pdac_luad_fluxes.csv`,
contrôle `step`, 12 flux (PGC, REG4, CLDN18, MUC17, DPCR1, CR2,
KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16) — KRAS, la variable
d'ordre, est ABSENT des flux analysés ; les 4 runs (réel, nul42,
s9601, s9602) sont terminés exit 0 avec ces fichiers. Bras B BRCA —
runs lancés par la file après la vérification : `pdac_brca_fluxes.csv`,
contrôle `step`, mêmes 12 flux — ESR1, la variable d'ordre, est
ABSENT des flux analysés ; KRAS absent aussi. Témoin COAD : mêmes
12 flux, KRAS absent. **Règle respectée dans les deux bras.** Le
pipeline exclut en outre la colonne de contrôle des flux analysés
par construction (ligne 6787 : `c != control_col`). Le défaut connu
des 96 rotations d'origine (§8.32) ne concerne pas cette piste ;
traité au §8.97, partie 1.

**2. Contrôles non monotones.** Aucune condition de monotonie n'est
imposée à KRAS (LUAD) ni à ESR1 (BRCA) comme axes d'ordre : un seuil
différent sous un axe non monotone serait lu comme de l'information,
pas comme une erreur. Les seuils sont lus comme des résultats
d'analyse à part entière.

**3. Analyse, pas prédiction.** Le verdict d'universalité (CONFIRME /
NON) décrit ce que les bras LUAD et BRCA montrent — il ne prédit pas
que le pipeline séparera le réel du nul sur un troisième cancer.
