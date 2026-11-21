# PROTOCOLE GELÉ — §8.83 : Survie — les gènes de privilège prédisent-ils la survie comme CA125 ?

Date : 21 novembre 2026, ~07h25 EST (12h25 UTC). Chantier §8.83, deuxième bras
supplémentaire autorisé par Zackary (idées propres). Ce protocole est gelé
AVANT toute analyse de survie sur les gènes de privilège. Aucun paramètre
ne change après les résultats. Le livre blanc N'EST PAS édité, le PDF N'EST
PAS régénéré, rien n'est poussé sur GitHub dans ce chantier (convention des
chantiers ; fusion par le coordinateur). La section §8.83 est écrite dans un
FICHIER SÉPARÉ (`section_8.83_survie_privilege.md`).

## 0. Contexte décisionnel — à lire avant tout le reste

- Référence à battre : **CA125 (MUC16) prédit une survie plus courte dans
  2 cohortes sur 3** — TCGA : Cox univarié HR 1,44 (p=0,001), multivarié
  1,32 ; ICGC : HR 1,57 (p=0,008), multivarié 1,56, quartile 9,5 vs 23,8
  mois (p=0,002) ; GSE71729 : HR 1,06 (p=0,58), quartile p=0,73 — NON.
  (Sources : §8.12 corrigé le 16 nov., §8.15, §8.16 ; valeurs reprises
  telles quelles, jamais recalculées — sauf la calibration du §6, qui les
  REPRODUIT comme contrôle de l'outil, sans les modifier.)
- Question posée : les gènes de privilège qui montent avec KRAS
  prédisent-ils la survie dans nos 3 cohortes avec survie (TCGA, ICGC,
  GSE71729), comme CA125 l'a fait (2/3 cohortes) ?
- **Gènes testés (gelés, liste fermée) :** les 7 gènes de privilège
  définis dans la mission et repris du bras œil (§8.81) — FASLG, TGFB1,
  TGFB2, IDO1, HLA-G, CD47, CD274/PD-L1 — **plus un score combiné**
  (moyenne des z-scores des 7, par cohorte), soit **8 items testés**.
  Aucun gène ajouté ou retiré après avoir vu les résultats. En
  particulier : on ne choisit PAS les gènes « qui montent avec KRAS »
  après avoir vu les survies, et on ne retire PAS un gène parce que sa
  survie est nulle. La colonne « monte avec KRAS » (§4) est calculée
  ICI, sur les mêmes données, avec sa propre règle gelée — elle n'est
  PAS importée du §8.81 ni d'aucune autre expérience (règle du 15 nov. :
  les données/conclusions d'AUTRES expériences ne sont pas importées
  comme verdicts).
- **Ce chantier ne rouvre rien :** C3 reste LEVÉE (§8.71), le test C
  reste NON (§8.45), l'adoption pleine de maxsep reste la décision de
  Zackary du 20 nov. 13h04. Ce chantier n'utilise PAS le pipeline
  (hors pipeline : KM / log-rank / Cox, comme les §8.12/§8.15/§8.16).
- Méthode de survie : **exactement celle des §8.12/§8.15/§8.16**
  (même implémentation KM / log-rank Mantel-Haenszel / Cox Breslow
  Newton-Raphson en numpy, événements booléens — voir les corrections
  du 16 nov. : log-rank sur événements entiers = faux positif ;
  « univarié » = UN gène à la fois, jamais un ajustement multi-gènes
  mal étiqueté). Le script `survival_privilege_883.py` réutilise ces
  fonctions (copie littérale avec attribution, ou import — le choix est
  consigné dans le script, le code de calcul est identique).
- Aucun test multivarié en critère : le critère principal est
  l'univarié, comme pour le record de CA125. Aucun ajustement sur le
  stade, le sous-type ou KRAS n'est ajouté après coup — si un gène
  passe, la section le dit avec son univarié seul, et la question
  d'un ajustement est notée comme piste, pas comme résultat.

## 1. Cohortes et échelles d'expression — reprises des bras de survie, pas réinventées

| Cohorte | Effectif survie | Décès | Expression utilisée (même que le bras de survie antérieur) | Source survie |
|---|---|---|---|---|
| TCGA-PAAD | n=177, OS médiane cohorte 20,0 mois | 92 | **Résidus corrigés de la pureté** (régression sur scores acineux/îlots, log2(RSEM+1)), même construction que `survival_tcga_verify.py` (§8.12) ; KRAS = résidu KRAS | `data_clinical_patient.txt` (184 patients), jointure par patient (12 premiers caractères), comme au §8.12 |
| ICGC PACA-AU | n=70 | 47 (OS) | **log2(cpm) brut Xena**, même que `survival_icgc.py` (§8.16) ; ordre = `kras_rank` de `icgc_clinical_70.csv` | Bailey et al. 2016, Suppl. Table 1 (`Status` + `Length of Follow Up (months)`), via `icgc_clinical_70.csv` ; OS = tout statut `Deceased...` |
| GSE71729 | n=125, OS médiane cohorte 17,0 mois | 84 | **Expression brute de la matrice** (mêmes valeurs que `survival_geo71729.py`, §8.15) ; ordre KRAS croissant, mêmes 145 primaires | Caractéristiques ch2 de la matrice : `survival_months`, `death_event_1death_0censor` |

- Fichiers sources déjà sur le disque, SHA déjà vérifiés aux §8.12/§8.15/
  §8.16 (TCGA tarball MD5 `b09569ce…` ; GSE71729 SHA
  `b2287893…` ; ICGC exp SHA `c2cb57af…`, probemap `b09a746f…`,
  Bailey XLSX `778224b3…`) — re-vérifiés dans le script avant lecture ;
  aucun nouveau téléchargement.
- **Vérification de jointure (gelée) :** pour chaque cohorte, le script
  reproduit d'abord les valeurs KRAS/MUC16/CEACAM5 du bras antérieur et
  les compare aux tables sauvegardées (`tcga_survival_verify_results.txt`,
  `geo71729_survival_table.csv`, `icgc_clinical_70.csv`) ; tout écart
  > 1e-9 sur une valeur d'expression jointe = ARRÊT et diagnostic.
  Les 20 primaires GSE71729 sans survie sont exclues, n rapporté.
  Aucune imputation.

## 2. Score combiné (gelé)

- **Score combiné privilège** (par patient, dans chaque cohorte
  séparément) = moyenne des z-scores (centrés réduits DANS la cohorte,
  un gène à la fois) des 7 gènes de privilège. Le score est calculé sur
  les patients AVEC survie uniquement (même population que les Cox),
  pour éviter qu'un patient sans survie influence la standardisation.
- Le score combiné est le 8e item testé, avec exactement les mêmes
  tests que les 7 gènes (§3).

## 3. Tests — pour chaque item (7 gènes + score), dans chaque cohorte

### 3.1 Test principal (décide) : Cox univarié continu, sans seuil

- Un gène à la fois (UN SEUL covariate), HR par **+1 écart-type**,
  vraisemblance partielle de Breslow, Newton-Raphson (même
  implémentation que `survival_tcga_verify.py`).
- Rapporté : HR, coef, se, p (Wald). Direction : HR > 1 = expression
  haute associée à une survie plus courte ; HR < 1 = sens inverse.
- **24 tests Cox au total** (8 items × 3 cohortes). **Correction pour
  tests multiples : Bonferroni 0,05/24 ≈ 0,0021, rapportée à titre
  descriptif, PAS une porte** — CA125 lui-même ne la passerait pas
  partout (ICGC p=0,008) ; exiger Bonferroni reviendrait à changer la
  règle du jeu après coup. Les p brutes décident (§5) ; les p
  Bonferroni sont affichées à côté, sans décider.

### 3.2 Test secondaire (appui) : log-rank quartile supérieur vs reste

- Groupe = quartile supérieur de l'item (Q4). Définition PAR COHORTE =
  celle du bras de survie publié de CETTE cohorte (les trois bras
  n'utilisaient pas la même définition — c'est consigné, pas unifié
  après coup) : TCGA = seuil au quantile 0,75 des patients avec survie
  (177), même fonction que le §8.12 (qui l'appliquait aux 178) ; ICGC =
  top 18 par rang (même que le §8.16) ; GSE71729 = top 36 par rang sur
  les 145 primaires, restreint aux patients avec survie (même que le
  §8.15). Les effectifs n du Q4 sont rapportés à chaque fois.
  Cas particulier (gelé) : le score combiné GSE71729 n'a pas de
  population de 145 (il est calculé sur les patients avec survie) —
  son Q4 est le top 36 par rang sur les 125 avec survie.
- Rapporté : n, décès, OS médiane (groupe et reste), log-rank p
  (Mantel-Haenszel, événements booléens). Direction attendue : médiane
  du Q4 PLUS COURTE que le reste.
- Le log-rank ne décide PAS du verdict (§5) : il est l'appui
  « seuil » du test sans seuil, comme aux §8.12/§8.15/§8.16 — où il
  a contredit le Cox pour CA125 en TCGA (p=0,070) comme en GSE71729.

### 3.3 Sensibilité ICGC : survie spécifique (DSS)

- Pour les items qui passent le critère Cox-OS en ICGC (§5), le Cox
  univarié DSS (événement = `Deceased - Of Disease` seul) est
  rapporté en sensibilité, comme au §8.16. Il ne change pas le
  verdict. Si aucun item ne passe en ICGC, aucun DSS n'est calculé.

## 4. Colonne « monte avec KRAS » — calculée ici, règle gelée

Pour chaque gène de privilège, dans chaque cohorte, Spearman rho(gène,
KRAS) + p bilatérale (scipy), sur les patients avec survie :

- TCGA : KRAS = résidu KRAS (même échelle que §8.12).
- ICGC : KRAS = log2(cpm) (même échelle que §8.16).
- GSE71729 : KRAS = valeur matrice (même échelle que §8.15).

Catégories par cohorte (gelées) : **MONTE** si rho ≥ +0,15 et p < 0,05 ;
**PLAT** si |rho| < 0,15 ; **DESCEND** si rho ≤ −0,15 et p < 0,05 ;
**FAIBLE** sinon (rho entre 0,15 et le seuil de p, ou rho < 0,15 avec
p < 0,05 — dit tel quel). Le croisement final est un TABLEAU, pas un
filtre : gènes qui montent avec KRAS (≥2/3 cohortes MONTE) × gènes qui
prédisent la survie (§5) — la question de la mission est répondue par
ce tableau, pas en excluant des gènes après coup.

## 5. Catégories de verdict — par item, gelées avant toute analyse

Critère PRINCIPAL = Cox univarié (§3.1), seuil p < 0,05, direction
cohérente :

| Catégorie | Condition gelée (Cox univarié, HR par +1 sd) | Lecture |
|---|---|---|
| **PRÉDIT COMME CA125** | HR > 1 et p < 0,05 dans **≥ 2/3 cohortes** | même niveau de preuve que CA125 (2/3) |
| **UNE COHORTE** | HR > 1 et p < 0,05 dans **exactement 1/3** cohortes, jamais HR > 1 p < 0,05 ailleurs, et jamais HR < 1 p < 0,05 | signal limité à une cohorte, nommé |
| **SENS INVERSE** | HR < 1 et p < 0,05 dans **≥ 2/3 cohortes**, et aucun HR > 1 p < 0,05 | expression haute = survie PLUS longue, dans 2/3 cohortes |
| **NE PRÉDIT RIEN** | aucune cohorte avec p < 0,05 dans un sens ou dans l'autre | rien de mesurable dans nos 3 cohortes |
| **MIXTE** | significatif dans les deux sens selon la cohorte (≥ 1 HR > 1 p < 0,05 ET ≥ 1 HR < 1 p < 0,05) | contradiction entre cohortes, dite telle quelle |

- Le log-rank quartile (§3.2) est rapporté pour chaque item et chaque
  cohorte, mais il NE CHANGE PAS la catégorie : un item « PRÉDIT COMME
  CA125 » au Cox avec des log-rank non significatifs reste « PRÉDIT
  COMME CA125 » — c'est exactement le cas de CA125 en TCGA (Cox
  p=0,001, log-rank p=0,070). L'accord/désaccord Cox/log-rank est
  consigné par item.
- **Verdict d'ensemble du chantier (gelé) :** « AU MOINS UN gène de
  privilège prédit la survie comme CA125 » si au moins un des 8 items
  est dans la catégorie PRÉDIT COMME CA125 ; sinon « AUCUN gène de
  privilège ne prédit la survie comme CA125 dans nos 3 cohortes ».
  Le score combiné compte comme un item : s'il est le seul à passer,
  le verdict d'ensemble est positif mais la section dit plainement
  que c'est le score, pas un gène seul.
- Aucune autre lecture (multivarié, ajustement, sous-groupe) n'est
  ajoutée après coup. Les pistes ouvertes sont listées, pas testées.

## 6. Calibration — porte d'entrée gelée, avant lecture des résultats

Le script NE LIT AUCUN résultat privilège avant d'avoir passé la
calibration suivante (reproduction des chiffres publiés, mêmes données,
même code) :

1. **Cox MUC16 univarié** reproduit à ±0,02 près (HR) dans les 3
   cohortes : TCGA 1,44 ; ICGC 1,57 ; GSE71729 1,06.
2. **Log-rank quartile MUC16** reproduit à ±0,01 près (p) dans les 3
   cohortes : TCGA 0,070 ; ICGC 0,002 ; GSE71729 0,73.
3. **Effectifs** exacts : TCGA n=177 / 92 décès ; ICGC n=70 / 47 décès
   OS ; GSE71729 n=125 / 84 décès ; OS médianes de cohorte 20,0 /
   16,6 (ICGC, §8.16) / 17,0 mois, tolérance ±0,5 mois — la médiane KM
   dépend de l'implémentation au dixième de mois près (le §8.12 donne
   20,0 ; l'implémentation gelée, premier temps d'événement où S ≤ 0,5,
   donne 20,2 ; la médiane simple des temps observés, elle, vaut 15,2
   et n'est PAS la médiane de survie — ne pas confondre).
   AMENDEMENT 21 nov. 2026 (avant toute lecture des résultats
   privilège — la porte n'avait pas encore été franchie) : la
   calibration log-rank MUC16 GSE71729 utilise la définition publiée
   du §8.15 (top 36 par rang sur les 145 primaires), pas un seuil au
   quantile 0,75 (qui inclut un patient lié de plus, n=34 au lieu de
   33, et donne p=0,86 au lieu de 0,73) ; la tolérance sur la médiane
   de cohorte passe de ±0,1 à ±0,5 mois pour la raison ci-dessus.
   Les deux écarts ont été diagnostiqués par re-calcul direct
   (top-36 : n=33, décès 22, médiane 17,0 vs 16,0, p=0,7292 — identique
   au §8.15 à 0,001 près), pas par ajustement sur les résultats
   privilège, qui n'ont pas été lus.

Si un seul de ces contrôles échoue, ARRÊT : le script s'arrête, le
diagnostic est consigné, aucun résultat privilège n'est lu. (Tolérance
HR ±0,02 : les chiffres publiés sont arrondis à 2 décimales et les
implémentations ont déjà été croisées à 0,01 près le 16 nov. ; un écart
au-delà signale un vrai changement de données ou de code, pas un
arrondi.)

## 7. Fichiers produits (liste gelée)

- `PROTOCOL_survie_privilege_883.md` (ce fichier).
- `PROVENANCE_883.md` (sources, SHA, jointures, calibration, SHAs des
  sorties).
- `survival_privilege_883.py` (SHA noté dans la section), avec les
  fonctions KM / log-rank / Cox reprises des §8.12/§8.15/§8.16.
- `survival_privilege_883_table.csv` (par cohorte : patient, item,
  temps, événement — sans identifiant clinique nominatif au-delà du
  rang/ID technique déjà présent dans les tables antérieures).
- `survival_privilege_883_results.txt` (paysage complet + Cox, toutes
  définitions, sans sélection).
- `section_8.83_survie_privilege.md` (verdict d'abord, chiffres ensuite).
