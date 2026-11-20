# Cancer du pancréas (PDAC) — pipeline universel v6.2

Dépôt public de travail du projet PDAC : recherche d'un remède pour le
cancer du pancréas avec le pipeline universel de détection de ruptures
(v6.2), données ouvertes, protocoles gelés, résultats vérifiés.

## État au 20 novembre 2026

- Livre blanc : `livre-blanc-pdac-v6.md`, 1007 pages (PDF partagé séparément),
  SHA-256 `e780e8604f6d947e15921f7ce329070b09a11e5999a8d6adb69c565877655e42`
  (12937137 octets), sections §8.1–§8.70. Le fichier Markdown ici a pour SHA-256
  `072c0f512beefc8f42da5d27ffc8663fc188e8b67cb22242429214c0fb3c8f79`
  (14483 lignes).
- Pipeline : `universal_v6.2.0_cohen.py`, version de travail, SHA-256
  `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`.
  v6.1 = référence, v6 = historique. `universal_v6.3.0_cohen.py`
  (recomposition du score MC) est joint pour vérification : proposition
  REJETÉE (§8.49), v6.2 reste la version de travail.
  `universal_v6.4.0_cohen.py` (recomposition du MC par la
  récurrence-concentration) est joint pour vérification : proposition
  REJETÉE (§8.52), v6.2 reste la version de travail.
- Le verdict §8.70 : confirmation indépendante maxsep (C3) —
  PARTIEL : la paire GSE79668 (n = 51, Kirby et coll. 2016, PMID 27282075,
  GPL11154) donne d_maxsep +0,0567 (réel 0,4104 contre nul 0,3538), positif
  mais sous le plancher 0,07 ; A2 étendu 6/10 (8/10 positifs), LOO 5/9 —
  C3 NON levée (elle exige 7 paires passantes au total, soit 7/10 avec la
  dixième paire, LOO pire cas 6/9) ; 2 nuls frais passent le plancher
  (+0,0890 et +0,1538), verdict fragile, non consolidé ; MC inversé
  (−0,0053), Delta plat (+0,0467), L7a UP des deux côtés, falsification
  indisponible (n = 51 < 75) ; extraction 4/4 à 0,0 exact. La table de la
  matrice est vide (0 ligne de données) : les valeurs viennent du fichier
  supplémentaire de la série (comptages bruts GENCODE v.9). Le test de
  Cohen marginal est vacueux par construction (d = 0,0000, 12 gènes) ;
  le test de Spearman contre le pas porte l'information (Δρ médian
  +0,186, 9/12 positifs). L'adoption pleine de maxsep, décidée par
  Zackary le 20 nov. 2026 à 13h04, reste sa décision — la confirmation
  reste ouverte.
- Les 3 verdicts §8.67–§8.69 : (§8.67) fraction leucocytaire —
  PARTIEL : elle retire un tiers de la cohésion (0,5035 → 0,3372,
  −33,0 %) et ordonne les flux bruts (+0,7129), mais une fois les flux
  résidualisés elle ne les ordonne plus du tout (−0,0099) et la
  séparation survit (+0,5662, 57,6 % du brut CD8A conservés) ; la
  quantité de leucocytes ne porte pas la séparation. (§8.68) xCell
  64 types — H1-xcell PARTIELLE SOUTENUE : les cellules dendritiques
  activées (aDC) retirent à elles seules 41,2 % de la cohésion
  (0,5563 → 0,3270) ; les DC ordonnent les flux à +1,1804 ; mais les
  flux résidualisés séparent encore +0,6040 (61,4 % du brut) — aucun
  type ne porte tout. (§8.69) confirmation indépendante maxsep (C3) —
  NON : la paire GSE21501 ne sépare pas (d_maxsep −0,0100), A2 étendu
  6/9, C3 non levée ; l'adoption pleine de maxsep, décidée par Zackary
  le 20 nov. 2026 à 13h04 (note §8.64.12), reste sa décision — la
  confirmation reste ouverte (piste GSE79668) ; correction : la
  plateforme GSE57495 est GPL15048, pas GPL6244 comme l'affirmait le
  §8.66 §1.2.
- Les 3 verdicts §8.64–§8.66 : (§8.64) adoption de maxsep —
  ADOPTER SOUS CONDITION CONFIRMÉ par une troisième lecture indépendante
  (0 écart contre le §8.59 : 37/48, 6/8, HP35 +1,6512, 120/120 à 0,0
  exact) ; maxsep devient le score principal affiché, MC reste
  secondaire, aucune v6.5 créée, v6.2 reste la version de travail.
  (§8.65) scores ESTIMATE publiés — H1-pub TOTALE SOUTENUE : la table
  publiée MD Anderson confirme le §8.54 à la décimale près (scores
  publiés ↔ recalculés r = 0,9999998, cohésion 0,5563 → 0,2001,
  −64,0 %, jointure 178/178) ; la question ouverte du §8.54 est fermée.
  (§8.66) bloc estomac/mucus, quatrième cohorte GSE62165 (118 tumeurs)
  — le cœur du §8.58 est confirmé et deux bords cassent : G5/KRAS
  CONFIRME 4/4 (KRT19 +0,577, p = 7,7e-12) et G1/KRAS CONFIRME, mais
  G1/stade NON CONFIRMÉ (sens inverse de TCGA) et G3 NON CONFIRMÉ
  (OR2B6 MONTE +0,293, premier OR montant en confirmation) ; le
  pipeline ne sépare pas du nul (MC 4/10, S_sep 5/10).
- Les 5 verdicts §8.59–§8.63 : (§8.59) maxsep seul — ADOPTER SOUS
  CONDITION (provisoire, pas pleine) : re-confirmé 37/48, 6/8, HP35
  +1,6512 ; le verdict tient à une paire (retirer l'une des 6 paires
  passantes → 5/7) et à la convention du plancher 0,07 (au plancher
  équivalent-sep, 5/8) ; 30 changements de classe ancien → maxsep, tous
  en gain, 0 en perte ; aucune v6.5 créée, v6.2 reste la version de
  travail. (§8.60) déconvolution — ZONE GRISE : aucun type cellulaire
  seul ne porte la corrélation immunitaire (retirer le meilleur type ne
  retire que 4,7 % de la cohésion) ; c'est la quantité totale
  d'infiltrat qui la porte ; la fraction leucocytaire par méthylation
  en explique un tiers (PARTIELLE, −33,0 %). (§8.61) pureté par
  méthylation — ZONE GRISE : elle ordonne les flux presque comme
  ABSOLUTE (+0,6739, 97,5 % d'E-ABS) mais ne retire que 15,9 % de la
  corrélation en linéaire, contre 25,5 % pour ABSOLUTE. (§8.62) loi
  d'échelle en n pour Delta — NON TROUVÉE (LOCO R² = −0,005) et elle NE
  SUFFIT PAS (réel/nul |Δ| ≤ 0,10 sur 53/106 paires) ; une loi est en
  revanche TROUVÉE pour quatre estimateurs (Katz, Petrosian, Sevcik,
  GraphDimension), qui ne portent pas Delta. (§8.63) mécanismes §8.50 /
  §8.53 — M1 EXPLIQUÉ (MC haut = permutation, Delta bas = w = 27, qui
  porte 96,8 % de l'effet) ; M2 PARTIELLEMENT EXPLIQUÉ (l'optimiseur
  maximise le MC sur 12 configs fixes, réplication hors échantillon
  indécise 6/10) ; Delta doit se comparer à w égal.
- Les 5 verdicts §8.54–§8.58 : (§8.54) infiltration — H1 SOUTENUE : la
  corrélation immunitaire est largement un effet de composition — après
  déconvolution ESTIMATE, la cohésion intra-famille tombe de 0,5563 à
  0,2002 (−64,0 %) ; ordonner par ImmuneScore sépare de +1,1942 ; le
  verdict « propriété propre aux tumeurs » du §8.51 est révisé.
  (§8.55) pureté externe — H1-ext PARTIELLE : ABSOLUTE (pdacR, 149/178)
  explique une partie de la corrélation immunitaire (0,5040 → 0,3757,
  −25,5 %) ; 66,1 % de la séparation conservés après régression ; le
  verdict « H0 soutenue » du §8.51 est qualifié, pas renversé.
  (§8.56) maxsep seul SUFFIT (rotations 37/48, paires principales 6/8,
  HP35 +1,6512) ; sep seul est REJETÉ (35/48, 5/8) — décision d'adoption
  à prendre, v6.2 reste la version de travail. (§8.57) Delta reste NON
  ÉLUCIDÉ depuis les séries complètes (meilleur modèle 89,2 % paires /
  90,5 % valeurs en LOCO). (§8.58) flux inattendus du bloc estomac/mucus
  confirmés sur 3 cohortes : le programme neuroendocrine s'efface avec
  KRAS (SYP −0,503), le métabolisme volatil confirme plus fort qu'en TCGA
  (AOX1 −0,611), les récepteurs d'odeurs chutent, aucun ne monte.
- Les 4 verdicts §8.50–§8.53 : (§8.50) arbitrage MTAP TIENT — sur 10 nuls
  frais (graines 1011 à 11111), l'écart S_sep réel − nul vaut au minimum
  +0,1110 (médiane +0,1595, maximum +0,1981), 10/10 au-dessus du plancher
  0,07, 13/13 avec les 3 nuls anciens ; la marge fragile du §8.46 était la
  queue basse de la distribution nulle. (§8.51) la pureté n'explique PAS
  la corrélation immunitaire — après régression de chaque gène immunitaire
  sur les deux scores de pureté, la corrélation intra-famille demeure
  (0,5563 → 0,5480, chute de 1,5 %) ; ordonner les flux immunitaires
  résidualisés par CD8A résidualisé sépare presque autant que le brut
  (+0,9174 contre +0,9838, 93,3 % conservés), comme prédit par la
  régression §8.48 (+0,9185, à 0,0011 près). (§8.52) recomposition du MC (v6.4) REJETÉE — MC2 suit
  maxsep sans ressusciter Test A ni renverser les verdicts NON (§8.34,
  §8.43), sous les critères gelés. (§8.53) plancher honnête des S_sep
  nuls à n≈70 : 0,38 en ICGC, 0,36 en GSE62452 (p95, réplique 1000
  tirages) — le réel ICGC (0,2289) est sous ce plancher, le réel GSE62452
  (0,4656) est au-dessus ; ≈200 nuls au total, la médiane converge dès
  ~50–100, le p95 exige davantage.

## Structure

- `livre-blanc-pdac-v6.md` — livre blanc complet (§8.1–§8.70).
- `universal_v6.2.0_cohen.py` — pipeline v6.2 (Cohen-d partout).
- `universal_v6.3.0_cohen.py` — proposition v6.3 REJETÉE (§8.49).
- `universal_v6.4.0_cohen.py` — proposition v6.4 REJETÉE (§8.52).
- `README.md`, `DATA_SOURCES.md`, `MANIFEST_SHA256.txt` — ce fichier,
  les sources des données, les SHA-256 de chaque fichier du dépôt.
- `provenance/` — 76 fichiers : protocoles gelés (`PROTOCOL_*.md`) et
  provenances (`PROVENANCE_*.md`) de chaque lot, plus
  `PUBLICATION_tlogNext.md`.
- `results/` — 93 tables vérifiées v6.1/v6.2/v6.3/v6.4 (validation, phase 2,
  Delta, MC recomposé, infiltration, pureté externe, sep/maxsep, Delta séries, estomac/mucus, adoption maxsep, déconvolution, pureté méthylation, loi d'échelle Delta, mécanismes, décision maxsep, ESTIMATE publiés, quatrième cohorte GSE62165, fraction leucocytaire, xCell, confirmation indépendante GSE21501, confirmation indépendante GSE79668).
- `sections/` — sections §8.38–§8.70 du livre blanc, fichiers sources.
- `scripts/` — 171 scripts de construction des flux, d'extraction et
  d'analyse.
- `data_flux/` — 623 CSV/JSON : flux d'entrée des runs, tests directs,
  extraits ssep / v62_delta / §8.46–§8.70.

## Données brutes

Les matrices brutes (~2 Go) ne sont pas dans ce dépôt (limite snapshot
GitHub : 2 000 fichiers, 16 Mio). Voir `DATA_SOURCES.md` : chaque source
(URL, accès, hachage) et le script pour les re-télécharger et reconstruire
les flux de `data_flux/`.

## PDF

Le PDF du livre blanc (1007 pages, binaire) est partagé séparément : les
snapshots GitHub n'acceptent que des fichiers UTF-8 de moins de 16 Mio
au total. Son SHA-256 est rappelé ci-dessus.

## Suite

La suite du travail (phase 2) se poursuit dans le dépôt
`tlogNext-pdac-phase2`, travail d'un autre agent — ce dépôt-ci reste
l'état vérifié du travail v6.2 au 20 novembre 2026.

Projet : FindPrint / TagPrint. Données ouvertes, code reproductible,
résultats négatifs rapportés comme les positifs.
