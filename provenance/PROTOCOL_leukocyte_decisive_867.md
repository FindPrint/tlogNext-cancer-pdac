# PROTOCOLE — Test décisif sur la fraction leucocytaire (§8.67)

Date de gel : 20 novembre 2026 (avant tout calcul NOUVEAU de ce chantier,
avant tout nouveau run ; aucun nouveau téléchargement — voir §2).
Chantier §8.67 du projet PDAC (go de Zackary « Fait tout cela »,
20 nov. 2026 13h04 heure de Montréal, 18h04 UTC ; question ouverte des
§8.60.9–§8.60.11 et §8.61.11 : « la fraction leucocytaire (annexe
descriptive, moyenne |r| 0,5456 avec les flux) » — « piste la plus
forte pour la suite »).
Règle permanente (27 oct. 2026) : provenance toujours nommée — source
complète, nature des lignes, comment chaque valeur a été produite,
hachages des données, et ce qui manque. Publication GitHub/PDF par le
coordinateur, pas dans ce chantier. Ne jamais modifier v6 / v6.1 / v6.2 ;
aucune modification du livre blanc ici ; ne pas toucher à
tlogNext-pdac-phase2.

## 1. Question

Le §8.54 a établi que la corrélation intra-famille immunitaire
(0,5563) est expliquée par l'infiltration immunitaire GLOBALE
(ImmuneScore ESTIMATE calculé : 0,5563 → 0,2002 après régression, chute
64,0 % ; I-RES +0,1982, 20,2 % du brut CD8A +0,9838 conservés) —
verdict H1 SOUTENUE. Le §8.60 (bras L) a établi, par une voie
indépendante de l'ARN, que la fraction leucocytaire par méthylation
retire un tiers de la cohésion (0,5035 → 0,3372, chute 33,0 %,
PARTIELLE) et ordonne les flux (D-LEU +0,7129, prédit +0,7552) — mais
le run RÉSIDUEL manquant n'a jamais été fait : on ne sait pas si la
séparation survit quand on FIXE la fraction leucocytaire. Le §8.61 a
montré que la pureté par méthylation, elle, laisse survivre la
séparation à 55,2 % (M-RES +0,5427) — zone grise.

Question décisive : **la fraction leucocytaire PORTE-t-elle l'effet —
c'est-à-dire l'écart S_sep s'effondre-t-il quand on la fixe (par
régression / par stratification), et quand on ordonne par elle les flux
déjà résidualisés — ou non ?**

Définition opérationnelle gelée de « porter l'effet » : la fraction
leucocytaire PORTE l'effet si, une fois la fraction leucocytaire fixée,
la séparation S_sep entre flux immunitaires résidualisés s'effondre
(L-RES < 0,30, soit ≤ 30,5 % du brut CD8A +0,9838 — le niveau de
l'ImmuneScore I-RES +0,1982) ET la fraction leucocytaire n'ordonne
plus les flux résidualisés (L-ORD < 0,30). Elle NE PORTE PAS l'effet
si la séparation survit à ≥ 0,70 (≥ 71 % du brut conservés — le niveau
du D-RES par type +0,7692) après fixation. Entre les deux : PARTIELLE.
La règle de verdict complète est au §7.

**Point d'honnêteté sur l'ordre des opérations (gelé ici).** Les
chiffres T1-L (moyenne |r| = 0,5456) et T2-L (0,5035 → 0,3372,
chute 33,0 %) et l'écart D-LEU (+0,7129) sont DÉJÀ publiés au §8.60
(bras L) : ils sont cités ici comme références relues en machine, et
RE-VÉRIFIÉS dans ce chantier (T1-L2, T2-L2, §7) comme garde-fou de
transcription — ils ne sont PAS des résultats nouveaux de ce chantier.
Conséquence gelée : T2-L est déjà connue PARTIELLE, donc
l'effondrement de la COHÉSION globale (chute ≥ 45 % + résiduelle
< 0,30) est exclu d'avance. **Le verdict PORTE ne peut donc pas exiger
T2 = effondrement ; il exige l'effondrement de la SÉPARATION
(L-RES, L-ORD) et, si une bande étroite existe, de la cohésion en
bande étroite (T4-L).** C'est précisément la question décisive : la
séparation s'effondre-t-elle PLUS que la cohésion (porteur non
linéaire / à seuil) ou MOINS (part linéaire seulement) ? Aucun chiffre
T4-L, L-RES, L-ORD, T2-J1, T2-J2, T2-L-imog n'a été calculé avant ce
gel.

## 2. Sources (gelées, toutes déjà détenues — AUCUN nouveau téléchargement)

1. **Base immunitaire** `pdac_immune_tcga_fluxes.csv`, SHA-256
   `66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e`,
   n = 178, 12 gènes bruts log2(RSEM+1) : CD8A, CD8B, CD4, FOXP3, CD68,
   CD163, CD274, PDCD1, CTLA4, GZMB, IFNG, CD19 ; axe
   `immune_kras_order_tcga.csv`, SHA-256
   `31d31ae64baf0a4a9247424f877ae6b0c3524cf97cf15c19d4bab80af417b62d`.
2. **Fraction leucocytaire par méthylation** : colonne
   `DNA.methylation.leukocyte.percent.estimate` du sampInfo transcrit
   au §8.55, `purity_855_sampinfo.csv`, SHA-256
   `7a09dde3d374d1afb64f1d1d053193fc884c04d62e63e519fcf4dbf17378b014`
   (181 lignes × 55 colonnes, transcription mécanique du
   `TCGA_PAAD.rds` de pdacR, SHA `52020679…ea76`, lui-même issu de la
   Table S1 de Raphael et al. 2017, Cancer Cell 32:185–203.e13, PMID
   28810144, PMCID PMC5964983, DOI 10.1016/j.ccell.2017.07.007).
   Garde-fou : la colonne est re-dérivée depuis le sampInfo dans le
   script d'analyse et son égalité est assertée avec les deux
   transcriptions détenues du projet : `purity_861_external.csv`
   (colonne `leukocyte_methyl_percent`, SHA `cf127ef7…d24b`) et
   `deconvolution_860_external.csv` (colonne
   `Leukocyte_fraction_methylation_Raphael`, SHA `438d677a…9cf`).
3. **Fraction leucocytaire imogimap** (sensibilité T2-L-imog) :
   `deconvolution_860_external.csv`, colonne
   `Leukocyte_fraction_imogimap` — fractions CIBERSORT publiées de
   Thorsson et al. 2018 via le miroir imogimap, `.rda` SHA
   `f576f5f2…a4e68289` (§8.60.10) ; r = +0,9947 avec la méthylation
   (n = 150, §8.60.2, référence relue).
4. **ImmuneScore ESTIMATE calculé (§8.54)** : `infiltration_854_scores.csv`,
   SHA-256 `628732ecbcc30a3281b0df7a5039ec2520a1c5f1a1ae9ce412c4d0d7caf78aa7`,
   colonne `ImmuneScore` (la même que pour I-IMM/I-RES au §8.54).
5. **Pureté ABSOLUTE externe (§8.55)** : `purity_855_external.csv`,
   SHA `03f34fe0…bd6f` (colonne de pureté), pour la sensibilité
   conjointe T2-J2.
6. **Références relues en machine (non recalculées)** :
   `ssep_844_rotations.csv` (CD8A brut IMMROT : réel 1,2310, nul
   0,2472, écart +0,9838), `infiltration_854_runs.json` (I-IMM +1,1942 ;
   I-RES +0,1982), `purity_855_runs.json` (E-ABS +0,6911 ; E-RES
   +0,6499), `purity_861_runs.json` (M-METH +0,6739 ; M-RES +0,5427),
   `deconvolution_860_runs.json` (D-TOP1 +0,5867 ; D-TOP2 +0,5609 ;
   D-RES +0,7692 ; D-LEU +0,7129) ; régression §8.48 :
   d_ssep = −0,175 + 1,705·C ; IMMROT sans doublon, moyenne +0,7521,
   minimum +0,4508.

## 3. Porte L (source) — AVANT tout test

- Vérifier les SHA-256 gelés (§2) : pipeline v6.2, base immunitaire,
  axe, sampInfo, transcriptions, scores §8.54, externe §8.55. Tout
  mismatch arrête le chantier.
- Compter la couverture leucocytaire : nombre de tumeurs du projet
  (178) appariées avec une valeur
  `DNA.methylation.leukocyte.percent.estimate` non nulle (attendu 150,
  comme aux §8.60/§8.61 ; seuil ≥ 100).
- **Porte L OUVERTE** si et seulement si : fichiers détenus vérifiés
  par SHA + colonne leucocytaire présente + couverture appariée
  ≥ 100 tumeurs + toutes les valeurs dans [0, 1] + égalité assertée
  entre la colonne re-dérivée et les deux transcriptions détenues.
- **Porte L FERMÉE** : si la couverture est < 100 ou si un SHA ne
  correspond pas ou si les transcriptions divergent → **arrêt du
  chantier** : section §8.67 écrite avec le verdict « données
  inaccessibles / incohérentes », AUCUNE valeur inventée, aucun run,
  aucun test sur des fractions fictives.

## 4. Jointure

- Clé de jointure : barcode échantillon TCGA, **15 premiers caractères**
  (`TCGA-XX-XXXX-01`) — même règle que les §8.55/§8.60/§8.61.
  0 collision de clé tolérée des deux côtés.
- Les analyses T1-L2–T4-L et les runs T5-L2 portent sur les tumeurs
  APPARIÉES avec la fraction leucocytaire par méthylation uniquement
  (n ≤ 178, attendu 150, noté) ; la base immunitaire est restreinte
  aux lignes appariées, ordre KRAS brut conservé.
- La cohésion brute de référence est RECALCULÉE sur le sous-ensemble
  apparié (n = 150 attendu) — jamais importée du §8.54 (n = 178) ni
  du §8.60 (même n, mais re-vérifiée ici).

## 5. Définitions gelées (miroir des §8.54/§8.60/§8.61)

- Fraction leucocytaire : `leuco` =
  `DNA.methylation.leukocyte.percent.estimate` (ADN, méthylation —
  mesure primaire de ce chantier, indépendante de l'ARN).
- Résidus : pour chaque gène immunitaire g, OLS de g sur [1, leuco]
  (moindres carrés, n apparié) ; résidu = observé − prédit.
  Sensibilités conjointes : résidus sur [1, leuco, ImmuneScore] et
  sur [1, leuco, ABSOLUTE].
- Cohésion H : moyenne des |r de Pearson| sur les 66 paires
  intra-famille (12 gènes). Couplage C : moyenne des |r| entre le
  contrôle et les flux analysés (définition §8.48). Nul du projet :
  bloc analysé permuté conjointement, default_rng(42), colonne de
  contrôle intacte.
- « Fixer » la fraction leucocytaire = deux voies indépendantes :
  (a) régression linéaire (résidus OLS — ne retire que la part
  linéaire ; un porteur non linéaire / à seuil peut survivre aux
  résidus) ; (b) stratification (bandes de fraction leucocytaire —
  non paramétrique, indépendante de toute linéarité). Les runs L-ORD
  et le test T4-L sont les garde-fous contre un porteur non linéaire :
  si la fraction leucocytaire portait l'effet par un seuil, elle
  ordonnerait encore les résidus (L-ORD élevé) et la cohésion
  s'effondrerait en bande étroite (T4-L).

## 6. Hypothèses gelées

- H1-leu (la fraction leucocytaire PORTE l'effet) : la corrélation
  intra-famille immunitaire et la séparation des flux sont portées
  par la quantité de leucocytes infiltrants. Prédictions : (a) chaque
  flux corrèle substantiellement avec la fraction leucocytaire
  (déjà établi au §8.60 : moyenne |r| = 0,5456) ; (b) après
  régression sur la fraction leucocytaire, la corrélation chute
  d'au moins un tiers (déjà établi au §8.60 : −33,0 %) ; (c) ordonner
  les flux par la fraction leucocytaire les sépare (déjà établi au
  §8.60 : D-LEU +0,7129) ; (d) **NOUVEAU, décisif** : ordonner les
  flux RÉSIDUALISÉS par CD8A résidualisé ne sépare PLUS (L-RES
  < 0,30) et la fraction leucocytaire n'ordonne plus les résidus
  (L-ORD < 0,30) ; (e) la cohésion s'effondre dans une bande
  étroite de fraction leucocytaire (T4-L).
- H0-leu (la fraction leucocytaire NE PORTE PAS l'effet — elle
  n'est qu'un corrélat de la composition) : la corrélation et la
  séparation persistent après fixation de la fraction leucocytaire,
  par toutes les voies (b)–(e). La fraction leucocytaire est alors
  un marqueur de l'infiltration globale, pas son porteur — le
  porteur reste l'infiltrat dans son ensemble (ImmuneScore, −64 %)
  ou une co-expression propre aux tumeurs.

## 7. Tests gelés et critères de décision (avant les calculs)

Critères = ceux des §8.54/§8.60/§8.61 (mêmes seuils, pas de nouveau
seuil inventé après coup), appliqués à la fraction leucocytaire.

### T1-L2 — Re-vérification : chaque flux suit-il la fraction leucocytaire ?
Pearson r + Spearman ρ (+ p bilatérale, brutes, sans correction pour
tests multiples — le jugement porte sur les moyennes, pas sur une p
isolée) de chaque flux contre `leuco` (n apparié) ; R² par flux (OLS
sur [1, leuco]). Critère : lien substantiel si moyenne |r| ≥ 0,30.
Valeur attendue du §8.60 (re-vérification, pas découverte) : 0,5456.
Tout écart > 0,005 avec le §8.60 arrête l'analyse (à dire, à
expliquer) — les données sont les mêmes, le chiffre doit reproduire.

### T2-L2 — Re-vérification : la cohésion chute-t-elle d'un tiers ?
Matrice 66 paires : brute (n apparié) vs résidus [1, leuco].
Rapportés : moyenne |r|, médiane |r|, fraction |r| > 0,5. Critère
gelé : EFFONDREMENT si moyenne |r| résiduelle < 0,30 (chute ≥ 45 %
depuis la brute appariée) ET fraction > 0,5 < 0,20 ; PERSISTANCE si
chute < 20 % ; entre les deux : partielle. Valeur attendue du §8.60 :
0,5035 → 0,3372 (chute 33,0 %, PARTIELLE). Tout écart > 0,005 avec le
§8.60 arrête l'analyse (même règle qu'en T1-L2).

### T2-L-imog — Sensibilité : la chute dépend-elle de la mesure de la fraction leucocytaire ?
Même matrice, résidus [1, LF_imogimap] sur les mêmes n appariées
(méthylation). Critère : chute dans [25 %, 45 %] = la part d'un tiers
est robuste à la mesure (deux voies quasi identiques, r = 0,9947) ;
chute < 20 % ou > 45 % = la part dépend de la mesure, à dire.
Descriptif de robustesse, pas un critère de verdict.

### T2-J1 — Conjointe : la fraction leucocytaire ajoute-t-elle quelque chose à l'ImmuneScore ?
Sur les mêmes n appariées : résidus [1, ImmuneScore] seuls, résidus
[1, leuco] seuls (T2-L2), résidus [1, leuco, ImmuneScore] conjoints.
Critère : si la chute conjointe est dans [chute ImmuneScore seul
− 2 points, chute ImmuneScore seul + 2 points], la fraction
leucocytaire n'ajoute rien au-delà du score global — elle est
contenue dans ce que mesure l'ImmuneScore ; si la chute conjointe
dépasse la chute ImmuneScore seul de ≥ 10 points, la fraction
leucocytaire porte une part INDÉPENDANTE du score global. Descriptif
de soutien, pas un critère de verdict.

### T2-J2 — Conjointe : la fraction leucocytaire ajoute-t-elle quelque chose à ABSOLUTE ?
Même construction sur les n communes aux deux mesures (attendu 149) :
résidus [1, ABSOLUTE] seuls (référence §8.55 : chute 25,5 % à n = 149,
recalculée ici sur le même n), résidus [1, leuco] seuls, résidus
[1, leuco, ABSOLUTE] conjoints. Mêmes critères de lecture que T2-J1
(± 2 points = rien ajouté ; ≥ +10 points = part indépendante).
Descriptif de soutien, pas un critère de verdict.

### T3-L2 — Couplage prédit (sans nouveau run)
C par contrôle immunitaire avant/après résidualisation sur `leuco`
(12 contrôles) ; d_ssep prédit par la régression §8.48
(d = −0,175 + 1,705·C) : pour L-RES (C_résid de CD8A) et pour L-ORD
(C = moyenne |r| entre `leuco` et les 12 flux résidualisés).
Prédictions calculées AVANT de lire les sorties des runs, consignées
dans `leukocyte_867_predictions.json` avant le lancement du lot.
Descriptif, pas un verdict seul.

### T4-L — Stratification par fraction leucocytaire (non paramétrique, NOUVEAU)
Médiane de `leuco` : matrice intra-famille dans chaque moitié
(moyenne |r|, fraction > 0,5) + écart-type de `leuco` dans chaque
moitié rapporté en % de l'écart-type global. Critère : une moitié est
dite BANDE ÉTROITE si son écart-type est < 50 % de l'écart-type
global. Si une bande étroite existe : effondrement dans cette bande
(moyenne |r| < 0,30) = argument pour H1-leu ; persistance
(≥ 0,80 × brute appariée) = argument pour H0-leu. Si aucune moitié
n'est étroite : T4-L est NON CONCLUANT (comme au §8.54.6) et n'entre
pas dans la règle de verdict. Persistance dans les deux moitiés
(≥ 0,80 × brute dans chaque moitié) = argument pour H0-leu même sans
bande étroite.

### T5-L2 — Runs v6.2 (4 maximum, prédictions AVANT lecture des sorties)
CSV construits par `build_leukocyte_867.py` (nuls graine 42,
construction du projet) :
- L-RES : contrôle CD8A RÉSIDUALISÉ ([1, leuco]), analysés = 11 autres
  flux RÉSIDUALISÉS (sans doublon, comme §8.44/§8.51/§8.54/§8.60/
  §8.61). Réel + nul (2 runs).
- L-ORD : contrôle fraction leucocytaire BRUTE, analysés = 12 flux
  RÉSIDUALISÉS ([1, leuco]). Réel + nul (2 runs).
Prédictions (T3-L2, calculées à partir de T1-L2/T2-L2 AVANT de lire
les sorties) : d_pred = −0,175 + 1,705·C_mesuré pour L-RES
(C = C_résid CD8A) et pour L-ORD (C = moyenne |r| entre `leuco` et les
12 flux résidualisés) ; comparaison directe à CD8A brut IMMROT
(+0,9838), à I-RES (+0,1982), à E-RES (+0,6499), à M-RES (+0,5427),
à D-RES (+0,7692) et à D-LEU (+0,7129).
Critères gelés : L-RES SOUTIENT H1-leu si son écart < 0,30 ;
L-RES SOUTIENT H0-leu si son écart ≥ 0,70 (et ≥ 0,45 = encore
séparant) ; L-ORD SOUTIENT H1-leu si son écart < 0,30 ; L-ORD
SOUTIENT H0-leu si son écart ≥ 0,45.

### Verdict de synthèse (règle gelée)
- **PORTE — DÉCISIF (H1-leu SOUTENUE)** si L-RES < 0,30 ET
  L-ORD < 0,30 (la séparation s'effondre quand on fixe la fraction
  leucocytaire, par les deux voies en run ; et, si une bande étroite
  existe au T4-L, la cohésion y est < 0,30 — sinon T4-L est non
  concluant et la règle tombe sur les deux runs).
- **PARTIEL** si L-RES ∈ [0,30 ; 0,70[ ET L-ORD < 0,70 (la séparation
  survit réduite quand on fixe la fraction leucocytaire, et la
  fraction leucocytaire n'ordonne plus — ou n'ordonne que faiblement —
  les résidus) — avec T2-L2 partielle en soutien.
- **NE PORTE PAS (H0-leu SOUTENUE)** si L-RES ≥ 0,70 ET L-ORD ≥ 0,45
  ET T4-L = persistance dans les deux moitiés (cohésion
  ≥ 0,80 × brute appariée dans chaque moitié).
- Toute autre combinaison : **ZONE GRISE**, à dire comme telle, test
  par test. En particulier : L-RES < 0,30 avec L-ORD ≥ 0,70 = zone
  grise (contradiction : les résidus ne se séparent plus entre eux
  mais restent fortement ordonnés par la fraction leucocytaire —
  effet non linéaire nommé, non tranché).
Aucun consensus exigé entre les tests : chaque test est rapporté avec
son propre critère ; le verdict suit la règle ci-dessus, pas un vote.
Les tests T2-J1/T2-J2/T2-L-imog ne changent pas le verdict — ils
précisent si la part leucocytaire est indépendante du score global /
de la pureté / de la mesure.

## 8. Nouveaux runs : 4 maximum
Mode fast, graine 42 (défaut pipeline), pipeline v6.2
SHA `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`,
jamais modifié, vérifié avant et après les runs. Lanceur existant
`run_v62_lot.sh` + manifeste `manifest_v62_leukocyte_867.txt`, log
`runs_v62_leukocyte_867.log`, unité systemd-run `v62-leuko-867`
(+ relance reprenable si mort d'unité ; jamais de nohup — leçon du
17 nov.). Sorties `results_fast_v62_leuko867_*`. Extraction par script
dédié `extract_leukocyte_867.py` (mêmes champs que
`extract_purity_861.py` : max_separation, stability, S_sep = produit).
Aucun re-run de D-LEU (§8.60) : l'écart +0,7129 est relu en machine.

## 9. Vérifications gelées
- SHA-256 du pipeline v6.2, de la base immunitaire, du fichier d'axe,
  du sampInfo, des transcriptions, des scores §8.54, de l'externe
  §8.55 : revérifiés avant tout calcul ; tout mismatch arrête le
  chantier.
- Égalité assertée entre la colonne leucocytaire re-dérivée du sampInfo
  et les deux transcriptions détenues (`purity_861_external.csv`,
  `deconvolution_860_external.csv`) ; toute divergence arrête le
  chantier.
- Reproduction des chiffres §8.60 bras L à ± 0,005 près (T1-L2, T2-L2) ;
  tout écart supérieur arrête l'analyse.
- Aucune valeur S_sep recopiée à la main ; écarts §8.44/§8.54/§8.55/
  §8.60/§8.61 relus en machine dans leurs fichiers de runs.
- Aucune conclusion d'une autre expérience n'est importée : seuls les
  chiffres de ce chantier (Porte L, T1-L2–T5-L2 du jour) et les écarts
  relus font le verdict. Les chiffres §8.60 bras L sont des références
  re-vérifiées, jamais le verdict.
- Aucun seuil nouveau, aucune sélection d'indicateur après coup.
- Si la porte L est fermée : aucun calcul T1-L2–T5-L2, aucun run,
  aucune valeur de fraction leucocytaire inventée ou approximée.

## 10. Livrables
1. Ce protocole (SHA noté dans le rapport final).
2. Section §8.67 : `~/workspace/runs/pdac-v6/section_8.67_leukocyte_decisive.md`.
3. Scripts : `analyze_leukocyte_867.py` (porte L, jointure, T1-L2–T4-L,
   sensibilités T2-L-imog/T2-J1/T2-J2, prédictions T3-L2),
   `build_leukocyte_867.py` (4 CSV T5-L2),
   `extract_leukocyte_867.py`.
4. Données : `leukocyte_867_external.csv` (tumeurs appariées : barcode,
   fraction leucocytaire méthylation + imogimap, ImmuneScore, ABSOLUTE,
   METH), `leukocyte_867_results.json/.csv` (T1-L2–T4-L + sensibilités),
   `leukocyte_867_predictions.json` (T3-L2, avant les runs),
   `leukocyte_867_csv_sha.json`, manifeste + log du lot.
5. Aucun push GitHub, aucune modification du livre blanc, aucune touche à
   tlogNext-pdac-phase2.

## 11. Ce qui manque (connu d'avance)
- La fraction leucocytaire par méthylation et ABSOLUTE partagent la
  même Table S1 (Raphael et al. 2017) : deux mesures, une seule table,
  pas deux sources indépendantes — à dire. La fraction imogimap vient
  d'une autre source (Thorsson et al. 2018) mais elle est calculée
  depuis l'ARN, donc non indépendante des flux (circularité partielle
  : c'est une sensibilité, pas une preuve).
- n apparié ≤ 178 (150 attendus) : les comparaisons se font sur le
  sous-ensemble apparié, avec la brute recalculée sur ce même
  sous-ensemble (jamais en mélangeant les n). Les 28 tumeurs sans
  fraction leucocytaire sont les non-whitelistées de Raphael (§8.60.2).
- La résidualisation OLS ne retire que la part LINÉAIRE : un porteur
  non linéaire / à seuil peut survivre aux résidus — c'est pourquoi
  L-ORD et T4-L sont gelés comme garde-fous, et pourquoi un L-RES
  élevé ne prouve pas à lui seul l'absence de portage non linéaire
  (à dire dans la section, avec les chiffres T4-L/L-ORD).
- Ce chantier ne teste pas le sous-type moléculaire (autre variable
  latente du §8.48.8), ni la survie par fraction leucocytaire, ni
  xCell (toujours ouvert, §8.60.11).
