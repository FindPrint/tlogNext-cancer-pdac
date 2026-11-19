# PROTOCOLE — Expliquer la domination IMMROT (§8.48)

Date de gel : 19 novembre 2026 (avant tout calcul de ce chantier, avant tout nouveau run).
Chantier 3/4 des étapes v6.2 approuvées par Zackary le 19 nov. 2026 ~08h16.
Règle permanente (27 oct. 2026) : provenance toujours nommée — source complète,
nature des lignes, comment chaque valeur a été produite, hachages des données,
et ce qui manque. Règle permanente (19 nov. 09h45) : « Toujours github et pdf !!! »
— publication par le coordinateur, pas dans ce chantier.

## 1. Question

Rotations SANS doublon (§8.44, 44 paires refaites, 88 runs v6.2 + 4 paires §8.41) :
IMMROT 12/12, somme des écarts S_sep +9,0256, moyenne +0,7521 par paire, plus petit
écart +0,4508 (CD68) ; V4ROT 10/12 (+3,6063, moyenne +0,3005) ; DEPMAPROT 6/12
(+0,9036, moyenne +0,0753) ; PARPROT 9/12 (+3,6259, moyenne +0,3022).
Avec doublon (§8.41) : IMMROT +10,8540 sur +25,7324 au total, 48/48.
Le bloc co-expression immunitaire (PDCD1/CD8A/GZMB/IFNG) est confirmé par tests
directs (§8.32). S_sep détecte l'ordre, pas une rupture (§8.41).

Question : qu'est-ce qui, dans la construction des flux immunitaires (gènes corrélés
entre eux, ordre par un flux immunitaire), produit cette domination ? Est-ce un effet
de la corrélation interne des flux plutôt qu'une rupture ?

## 2. Ce que fait le scan (lu dans le code, jamais modifié)

Pipeline v6.2 `universal_v6.2.0_cohen.py`, mode `fast` : w_size = 80 (plafonné à
n//2, donc 22 à n=45), min_grp = 2. Le scan trie les lignes par le contrôle
(axe de progression MC, monotone en le contrôle), construit des fenêtres glissantes
de w_size points, ordonne les fenêtres par leur progression moyenne, puis pour
chaque seuil candidat s (percentile 0–100 de la progression des fenêtres) partage
les fenêtres en deux groupes et calcule, par flux analysé, le |d de Cohen| entre
les deux groupes ; le score du candidat est la MOYENNE sur les flux des |d| ;
max_separation est le maximum de ce score ; S_sep = max_separation × stabilité
(stabilité quasi saturée, 0,9463–0,9986, §8.44).

Conséquence mécanique, à tester et non à supposer : si un flux analysé j est
corrélé au contrôle c avec un coefficient r_j, alors trier par c trie partiellement
j, et le |d| de j au seuil est grand ; max_separation est alors grand sans qu'aucune
rupture n'existe. Le nul du projet permute les lignes du bloc analysé CONJOINTEMENT
(`nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]`, graine 42, colonne de contrôle
intacte) : il conserve les corrélations ENTRE flux analysés et brise seulement
l'alignement contrôle↔flux. Le nul isole donc exactement l'alignement contrôle-flux.
Toute explication par « les flux sont corrélés entre eux » doit survivre à ce fait :
la cohésion entre flux analysés, seule, ne peut pas produire S_sep, puisque le nul
la conserve et que S_sep nul reste bas (0,08–0,43).

## 3. Hypothèses gelées (avant les calculs)

- H1 (principale) : l'écart S_sep réel−nul par rotation est prédit par le COUPLAGE
  contrôle↔flux analysés, c'est-à-dire la force avec laquelle les flux analysés
  suivent le contrôle. IMMROT domine parce que les flux immunitaires sont fortement
  couplés à chaque contrôle immunitaire.
- H0 (négative) : la COHÉSION entre flux analysés (corrélations flux↔flux hors
  contrôle) ne prédit pas l'écart S_sep. Si elle le prédisait aussi bien que le
  couplage, H1 ne serait pas spécifique.
- H2 (contrôle immunitaire universel ?) : un flux immunitaire, comme contrôle,
  ordonne-t-il AUSSI des flux non immunitaires ? Si oui, la domination viendrait
  du contrôle lui-même (ex. il suit une variable latente partagée : infiltration,
  pureté) ; si non, elle vient de la paire contrôle immunitaire × flux immunitaires
  (corrélation intra-famille).
- H3 (dose–réponse) : dégrader progressivement l'alignement contrôle↔flux fait
  chuter S_sep progressivement. Si S_sep ne bouge pas quand on casse l'alignement,
  H1 est fausse.

## 4. Définitions gelées

Bases (12 flux chacune, colonne `step` exclue de tous les calculs) :
- V4ROT : `pdac_tcga_fluxes_v4.csv`, n=178, SHA e7a2adab…13a0b0.
- DEPMAPROT : `pdac_depmap_fluxes.csv`, n=45, SHA 7d605fef…98e37f8.
- IMMROT : `pdac_immune_tcga_fluxes.csv`, n=178, SHA 66dbb672…bbd2e.
- PARPROT : `pdac_tcga_fluxes_parp.csv`, n=178, SHA c9549b68…c4309.
(SHA vérifiés contre PROVENANCE_rotations_v61.md avant ce chantier : 4/4 conformes ;
re-vérifiés par le script d'analyse, §7.)

Pour une rotation de contrôle c, sur le fichier DE BASE (ordre des lignes indifférent
pour une corrélation) :
- Couplage C_c = moyenne sur les 11 flux j≠c de |r_Pearson(c, j)|. Robustesse :
  même quantité en Spearman (rangs), notée C_c^S.
- Cohésion H_c = moyenne sur les 55 paires (j,k), j<k, j,k≠c, de |r_Pearson(j, k)|.
  Robustesse Spearman H_c^S.
- Couplage nul C_c^nul et cohésion nulle H_c^nul : mêmes quantités calculées sur le
  CSV nul dédoublonné correspondant (contrôle intact, bloc analysé permuté).
  Attendu sous la construction du nul : C_c^nul ≈ 0 (bruit d'échantillonnage seul),
  H_c^nul ≈ H_c (conservée). C'est un contrôle de SANITÉ de la construction du nul,
  pas un résultat.

Écarts S_sep repris tels quels, sans recalcul : `ssep_844_rotations.csv`
(sans doublon, 48 paires, SHA d1abc0ab…f999) et `ssep_841_rotations.csv`
(avec doublon, 48 paires, SHA 1d3b28a4…). Aucune valeur S_sep recopiée à la main ;
lues en machine par le script d'analyse.

Statistique D_full (réplication analytique TRANSPARENTE du mécanisme, sans
l'axe MC ni les fenêtres) : sur un CSV dédoublonné (réel ou nul), lignes triées
par le contrôle (elles le sont déjà), pour chaque coupure k (k = 20..n−20, pas de 1),
|d de Cohen| par flux analysé entre les k premières et les n−k dernières lignes,
moyenne sur les flux ; D_full = maximum sur k. Variante à coupure FIXE : médiane
(k = n//2), notée D_med. Prédiction bivariée-normale par flux, à la médiane :
d_j^pred = 1,596·r_j / sqrt(1 − 0,637·r_j²), avec r_j = Pearson(c, j) ; comparer
d_j observé (à la médiane) à d_j^pred sur les 48×11 = 528 paires (réel sans doublon).

## 5. Tests gelés et critères de décision (avant les calculs)

### (b) Corrélations internes par famille
Matrices de corrélation Pearson + Spearman des 12 flux de chaque base (66 paires
hors diagonale). Par famille : moyenne |r|, médiane |r|, fraction |r|>0,5,
plus forte et plus faible paire. Comparer réel vs nul (nul de base : `*_nul.csv`).

### (c) Le couplage prédit-il S_sep ? (test principal)
Sur les 48 rotations sans doublon : Pearson r et Spearman ρ entre C_c et
d_ssep (écart réel−nul) ; régression linéaire d_ssep ~ a + b·C_c (R² rapporté).
Même calcul avec doublon (d_ssep §8.41) et en Spearman (C_c^S).
Critère gelé : H1 est SOUTENUE si r_Pearson(C_c, d_ssep sans doublon) > 0,7 ET
ρ_Spearman > 0,7 ; H1 est REJETÉE (« non expliqué » honnête) si r < 0,5.
Entre 0,5 et 0,7 : partiel, à dire comme tel. Par famille (n=12) : descriptif
seulement, puissance insuffisante pour un test.
Contrôles négatifs gelés : r(H_c, d_ssep) et r(C_c, S_sep nul) — attendus |r| < 0,3
sous H1. Si r(H_c, d_ssep) > 0,7, H1 n'est pas spécifique : le dire.
Moyennes par famille (4 points) : descriptif seulement, jamais un test.

### (b3) Réplication analytique D_full
Sur les 96 CSV dédoublonnés (48 réels + 48 nuls) : corrélation Pearson entre
D_full et max_separation pipeline ; écart moyen |D_full − maxsep|.
Critère gelé : mécanisme CONFIRMÉ si r > 0,95 et écart moyen < 0,10.
Par flux à la médiane : corrélation entre d_j observé et d_j^pred (528 paires) ;
critère : r > 0,8 pour que la formule bivariée-normale soit une bonne description.
Si D_full ne reproduit pas maxsep, le dire et ne pas utiliser D_full comme preuve.

### (d1) Sanité du nul
C_c^nul ≈ 0 et H_c^nul ≈ H_c sur les 48 paires (moyennes rapportées, écart-type).
Si C_c^nul n'est pas proche de 0, la construction du nul est à réexaminer et
les tests (c) sont suspendus (à dire dans la section).

### (d2) Permutation partielle (dose–réponse, nouveaux runs v6.2)
Sur CSV dédoublonnés RÉELS, bloc analysé permuté CONJOINTEMENT (comme le nul),
avec une fraction q de lignes FIXÉES (choisies par default_rng(1234)) et le reste
permuté entre elles : q = 0,5 pour CD8A (IMMROT, plus fort écart +0,9838),
CD68 (IMMROT, plus faible écart +0,4508), CLDN18 (V4ROT, contraste non immunitaire) ;
q = 0,25 pour CD8A seulement. Soit 4 nouveaux runs (réels partiels ; pas de nul :
q=1 est le réel §8.44, q=0 est le nul §8.44 graine 42 — seeds différents, noté).
Critère gelé : H3 SOUTENUE si S_sep(q=0,5) tombe entre le réel et le nul pour les
3 rotations ET S_sep CD8A(q=0,25) < S_sep CD8A(q=0,5) ; sinon H3 rejetée.
Le pipeline est lancé EXACTEMENT comme au §8.44 (mode fast, graine 42 par défaut,
`run_v62_lot.sh` + manifeste, unité systemd-run, exit codes journalisés).

### (d3) Flux immunitaire témoin hors famille (nouveaux runs v6.2) — SOUS RÉSERVE DE LA PORTE G
Deux CSV croisés, contrôle + 12 flux analysés (pas de doublon possible, le contrôle
n'appartient pas à la famille analysée) :
- X1 : contrôle CD8A (immunitaire), analysés = les 12 flux PARP (TCGA).
- X2 : contrôle POLQ (PARP, plus fort écart PARPROT sans doublon +0,6093),
  analysés = les 12 flux immunitaires (TCGA).
Chacun avec son nul (bloc analysé permuté conjointement, default_rng(42), contrôle
intact). Soit 4 nouveaux runs. Prédiction H2 : si la domination est intra-famille,
d_ssep(X1) et d_ssep(X2) restent SOUS 0,30 (moyennes PARPROT/V4ROT sans doublon) ;
si l'un des deux atteint ≥ 0,45 (minimum IMMROT sans doublon), H2 est soutenue
(le contrôle ordonne hors famille) et H1 doit être reformulée. Entre 0,30 et 0,45 :
zone grise, à dire comme telle.
PORTE G (vérification de la jointure, AVANT de construire X1/X2) : les bases
IMMROT et PARPROT doivent avoir la MÊME ligne i = le MÊME patient. Vérification :
recharger le tarball TCGA-PAAD RSEM (MD5 b09569ce…ac0a), filtrer tumeurs primaires
(code 01), log2(RSEM+1), compter les NaN sur KRAS + 12 gènes immunitaires et sur
KRAS + 12 gènes PARP, trier par KRAS brut croissant, comparer l'ordre des
échantillons à `immune_kras_order_tcga.csv` (178 lignes, colonne sample).
G est OUVERTE si et seulement si : (i) 178 tumeurs primaires ; (ii) 0 NaN sur les
deux jeux de gènes (donc cas complets = les 178) ; (iii) l'ordre KRAS brut
recalculé égale EXACTEMENT l'ordre de `immune_kras_order_tcga.csv` (178/178).
Si G est FERMÉE : X1/X2 sont ABANDONNÉS (jointure non prouvée), H2 reste non
testée par run et est tranchée seulement par les corrélations croisées (C_c
calculé entre CD8A et les flux PARP après jointure par index — non, sans jointure
prouvée, même les corrélations croisées sont interdites : H2 est alors déclarée
NON TESTABLE dans ce chantier, avec la raison). La base V4ROT est EXCLUE de tout
croisement : ses lignes sont ordonnées par KRAS RÉSIDUEL (corrigé pureté), pas
par KRAS brut — la jointure par index y serait fausse.

### (d4) Comparaison avec doublon (§8.41)
Refaire le test (c) sur les écarts AVEC doublon (48 paires) : si le couplage
prédit aussi les écarts avec doublon (r > 0,7), la domination IMMROT ne dépend
pas du doublon ; sinon, quantifier la différence. Comparer aussi les pertes
d'écart (avec − sans) au couplage : le doublon ajoute-t-il ~1/12 de |d| du
contrôle (une colonne sur 12) ? Rapport descriptif, pas de nouveau run.

## 6. Nouveaux runs : 8 maximum

4 (d2) + 4 (d3, si G ouverte). Aucun autre run. Mode fast, graine 42, pipeline
v6.2 SHA f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf,
jamais modifié. Lanceur `run_v62_lot.sh` (existant, SHA 7e501733…35b) + manifeste
`manifest_v62_immrot_848.txt`, log `runs_v62_immrot_848.log`, unité systemd-run
`v62-immrot-848` (+ relance reprenable si mort d'unité, comme aux §8.41/§8.44).
Sorties `results_fast_v62_immrot848_*`. Extraction par un script dédié
`extract_immrot_848.py`, sorties `immrot_848_correlations.csv/.json`,
`immrot_848_results.csv/.json` (SHA notés dans la section).

## 7. Vérifications gelées

- SHA-256 des 4 bases, de `ssep_844_rotations.csv`, de `ssep_841_rotations.csv`,
  du pipeline v6.2 : revérifiés par le script d'analyse avant tout calcul ;
  tout mismatch arrête le chantier (à dire dans la section).
- Le doublon est exclu de toutes les lectures par flux (règle §8.32) ; les
  corrélations sont calculées sur les bases à 12 flux (le contrôle y est un flux
  comme les autres) et sur les CSV dédoublonnés à 11 flux analysés — les deux
  donnent les mêmes C_c/H_c (la corrélation ne dépend pas de l'ordre des lignes),
  vérifié sur 4 paires témoins (une par famille) et rapporté.
- Aucun seuil nouveau, aucune sélection d'indicateur après coup. Les critères
  des §5 sont ceux du verdict, pas d'autres.
- Aucune conclusion d'une autre expérience n'est importée : seuls les chiffres
  de ce chantier (corrélations du jour, D_full du jour, 8 runs du jour) et les
  écarts S_sep relus des §8.41/§8.44 font le verdict.

## 8. Livrables

1. Ce protocole (SHA noté dans le rapport final).
2. Section §8.48 complète : `~/workspace/runs/pdac-v6/section_8.48_immrot_domination.md`
   (verdict d'abord, chiffres, méthode, limites, provenance).
3. Scripts : `analyze_immrot_domination.py` (corrélations + D_full),
   `build_immrot_848.py` (CSV partiels + croisés + nuls), `extract_immrot_848.py`.
4. Données : `immrot_848_correlations.csv/.json`, `immrot_848_results.csv/.json`,
   `immrot_848_csv_sha.json`, manifeste + log du lot.
5. Aucun push GitHub, aucun PDF dans ce chantier (publication par le coordinateur).

## 9. Ce qui manque (connu d'avance)

- D_full est une réplication transparente, pas le scan exact (axe MC non répliqué) ;
  son accord avec maxsep est MESURÉ (§5 b3), pas supposé.
- n=12 par famille : les tests par famille sont descriptifs.
- DEPMAPROT n=45 : corrélations estimées sur 45 points, incertitude plus grande
  (intervalles rapportés quand ils sont calculés, sinon le dire).
- H2 dépend de la porte G ; si elle est fermée, H2 reste ouverte.
- Ce chantier n'explique pas POURQUOI les gènes immunitaires sont corrélés entre
  eux (biologie : infiltration, pureté, sous-types) — il mesure si cette
  corrélation suffit à produire la domination S_sep. La cause biologique de la
  corrélation elle-même est hors périmètre.
