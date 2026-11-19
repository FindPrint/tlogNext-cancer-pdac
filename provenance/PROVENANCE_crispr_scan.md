# PROVENANCE — Balayage CRISPR génome entier (bras A, 16 nov. 2026)

## Source des données
- **DepMap Public 24Q4** (Broad Institute), via figshare article 27993248,
  DOI 10.25452/figshare.plus.27993248.v1. Fichiers **déjà téléchargés le 15 nov. 2026,
  non re-téléchargés** :
  - `data/CRISPRGeneEffect.csv` — 428 678 699 octets exacts,
    SHA-256 `3d8f3ec6dbf2db7ff834b79b508622ec0b226f3518003fe96ecf5a4fcf167e3b`
  - `data/Model.csv` — 645 696 octets,
    SHA-256 `b7a0c1385e6cef30132b56aff61f1261d11e3f490490b355c430d32ee0dbdcfa`
- **Piège de format (connu, 15 nov.) :** la première colonne de CRISPRGeneEffect.csv
  est SANS NOM (les ModelIDs sont l'index) ; les colonnes gènes sont nommées
  « SYMBOLE (Entrez) », ex. `KRAS (3845)`. Lecture par blocs (RAM limitée),
  `index_col=0`, dtype float32 sur les colonnes gènes uniquement.

## Lignées
- Model.csv : 68 lignées pancréas (`OncotreeLineage == Pancreas`).
- Présentes dans GeneEffect : **47** (45 adénocarcinomes + 2 adénosquameux) ;
  21 lignées Model.csv absentes de GeneEffect (non imputées, simplement absentes).
- Axe : Chronos KRAS — min −4,143 / médiane −1,758 / max −0,180 ; 0 valeur manquante.
  Chronos négatif = essentiel ; Chronos bas = lignée dépendante de KRAS.

## Méthode (protocole gelé)
- Script `crispr_genome_scan.py`, **exit 0**, 37,9 s.
  Journaux : `crispr_genome_scan.log` et `crispr_genome_scan_stdout.txt`.
- Pour chacun des 17 916 gènes : Spearman entre l'effet Chronos du gène et le
  Chronos KRAS sur les 47 lignées, paires complètes uniquement (**jamais d'imputation**).
  p par la distribution t (t = rho·√((n−2)/(1−rho²))).
- Correction BH-FDR sur les gènes testés. Significatif = FDR < 0,05.
  Gènes avec n < 30 paires valides exclus du FDR : **129 exclus, 17 787 testés**.
- Nul : vecteur Chronos KRAS permuté (graine 42), même balayage.
- Sens : rho POSITIF = gène plus essentiel quand la lignée dépend de KRAS
  (partenaire létal synthétique) ; rho NÉGATIF = gène moins essentiel (ou protecteur).
- Tertiles de dépendance KRAS : « fort » = Chronos le plus bas = le plus dépendant
  (étiquettes corrigées — voir note §8.7 du livre blanc sur l'inversion PRISM du 15 nov.).
- Contrôle de cohérence : rhos des 10 gènes v4 du 15 nov. reproduits à l'identique
  (écart 0,00e+00 entre `corrwith` et `scipy.stats.spearmanr`, et égaux aux valeurs
  du 15 nov.) ; KRAS lui-même rho = 1,0 (contrôle positif).

## Résultats (fichier `data/crispr_genome_scan.csv`, 17 916 lignes, SHA `673e7080…`)
- **3 hits FDR < 0,05 :** KRAS (rho +1,000, contrôle), **TCF7L2** (rho +0,614,
  p 4,38e-06, FDR 0,039 ; Chronos moyen fort −0,43 / moyen −0,31 / faible +0,05),
  **PRDX4** (rho +0,602, p 7,64e-06, FDR 0,045 ; fort −0,25 / moyen −0,16 / faible −0,10).
- 4e gène sous FDR < 0,10 : PSMD2 (rho +0,585, FDR 0,0706) — non significatif.
- **Nul : 0 hit FDR < 0,05** — les 2 hits non triviaux battent le nul.
- Candidats connus (tous non significatifs après correction) : RAF1 +0,429 (FDR 0,45),
  PLK1 +0,427 (FDR 0,45), BCL2L1 +0,415 (FDR 0,49), CDK4 +0,231 (FDR 0,79),
  MYC +0,133 (FDR 0,91), TBK1 −0,172 (FDR 0,88, mauvaise direction),
  MTOR −0,039, MAPK1 +0,050, MAPK3 +0,006, PIK3CA +0,035, CDK6 +0,090,
  AURKA −0,216, STK33 +0,024.

## Vérification druggabilité (ChEMBL, API publique, 16 nov. 2026)
- TCF7L2 (UniProt Q9NQB0) : 3 cibles ChEMBL, toutes des complexes / interactions
  protéine-protéine — TCF4/β-caténine CHEMBL3038511 (616 activités),
  APC/TCF7L2 CHEMBL3885511 (14 activités), Cadherin-1/TCF7L2 CHEMBL3885533.
  Aucune entrée « single protein » druggable directe pour TCF7L2 lui-même.
- PRDX4 (UniProt Q13162) : 1 cible, Peroxiredoxin-4 CHEMBL4295812, 17 activités
  enregistrées ; aucun médicament approuvé identifié dans cette vérification.
- PSMD2 (UniProt Q13200) : sous-unité 26S CHEMBL3831209 (4 activités) ; les
  inhibiteurs du protéasome ciblent les sous-unités catalytiques 20S, pas PSMD2.
- **DGIdb : non vérifié par cette voie** — l'API REST renvoie la page de l'application
  (JavaScript, pas de JSON), le GraphQL n'a pas renvoyé de réponse exploitable.
  Marqué « à vérifier », rien inventé.

## Limites honnêtes
- n = 47 lignées seulement : la puissance est limitée, les rhos sont bruités ;
  le FDR protège contre le hasard (nul = 0 hit), pas contre la faiblesse de l'effet.
- **Essentialité absolue faible :** même dans le tertile le plus dépendant,
  TCF7L2 n'est qu'à −0,43 et PRDX4 à −0,25 (le seuil usuel de dépendance est
  autour de −0,5 à −1). La corrélation est significative, l'effet absolu est modeste.
- Corrélation ≠ causalité : aucune validation expérimentale ici (pas de knock-out
  ciblé, pas de test in vivo). Chronos = viabilité in vitro, pas efficacité clinique.
- TCF7L2 est un facteur de transcription (voie Wnt/β-caténine) : pas de poche
  druggable classique ; PRDX4 est une enzyme antioxydante, pas une cible validée.
- Ce balayage ne donne pas un remède : 2 partenaires faibles, non druggables
  directement, sans effet de classe.
