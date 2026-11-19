# PROVENANCE — Survie GSE71729 (Moffitt PDAC)

## Source de la survie
- **Dépôt :** GEO, série GSE71729 (Moffitt et al. 2015, *Nat Genet* 47:1168–78,
  « Virtual Microdissection of Pancreatic Ductal Adenocarcinoma Reveals Tumor
  and Stroma Subtypes », DOI 10.1038/ng.3398).
- **Fichier :** `data/GSE71729_series_matrix.txt.gz`, 15 622 315 octets,
  SHA-256 `b228789314ec4d866ec51b65724664abaa24b822577c55d3727820c867536a54`
  (déjà téléchargé le 15 nov. 2026, vérifié).
- **Champs de survie (caractéristiques ch2 de la matrice) :**
  `survival_months` (125 échantillons) et `death_event_1death_0censor`
  (125 échantillons ; 1 = décès, 0 = censure). La survie est DANS la matrice
  elle-même — aucun fichier clinique séparé n'existe pour cette série.
- **Vérification externe :** les effectifs correspondent aux publications :
  125 patients avec survie, 84 décès / 41 vivants (Wiley 2022, analyse des
  sous-types immunitaires, tableau 1) ; Frontiers 2026 rapporte 123 patients
  et 83 événements (2 de moins — probablement leurs exclusions).

## Recherche du fichier clinique (piste suivie, puis fermée)
1. Répertoire `suppl/` GEO : seulement `GSE71729_RAW.tar` (3,9 Go, données
   brutes Agilent) et `filelist.txt` — pas de clinique.
2. Suppléments Nature de l'article (téléchargés, SHA ci-dessous) :
   - `ng3398_MOESM59_ESM.pdf` (5 339 711 o, SHA `c18dbc59…320c0`) :
     figures supplémentaires + tableau 3 — pas de survie par patient.
   - `ng3398_MOESM60_ESM.txt` (19 393 438 o, SHA `516cf2eb…4c7db`) : matrice
     d'expression + annotations (mutation KRAS, CAF, PDX, lignée, primaire,
     sous-type Collisson) — aucune ligne de survie (recherche par regex).
   - `ng3398_MOESM61_ESM.xlsx` (460 785 o, SHA `ec26858b…c1c01ad`) :
     tableau 1, enrichissements de signatures par facteur NMF.
   - `ng3398_MOESM62_ESM.xlsx` (2 612 836 o, SHA `25c35346…08b5c`) :
     tableau 2, factorisation des gènes.
   - `ng3398_MOESM63_ESM.xlsx` (14 141 o, SHA `3d508a54…20905`) :
     tableau 4, correspondance ID Moffitt ↔ GSM Stratford.
3. Suppléments de Birnbaum et al. 2017 (validation des classifications,
   PMC5674743, via static-content Springer, MOESM1–5, SHA à vérifier dans
   les fichiers) : tableaux récapitulatifs seulement, pas de survie par
   patient.
4. Conclusion : la survie par patient est dans la matrice GEO (ch2).

## Méthode
- **Script :** `survival_geo71729.py`.
- **Jointure :** l'ordre des 145 tumeurs primaires est reproduit EXACTEMENT
  comme dans `build_fluxes_geo71729.py` (même lecture de la matrice, mêmes
  primaires `tissue type: Primary`, même tri KRAS croissant) et vérifié
  ligne par ligne contre `pdac_geo71729_fluxes.csv` : MUC16, CEACAM5, PGC
  identiques (vrai pour les 3) ; KRAS trié croissant (min 1,55, médiane
  3,28, max 4,15 — identiques aux valeurs du rapport GEO).
- **Survie jointe :** 125/145 primaires ont une survie (84 décès).
  20 primaires sans survie, exclues, n rapporté.
- **Analyses :** paysage complet (top12/top7/top20 KRAS, quartiles sup.
  MUC16 / CEACAM5 / KRAS seuls, double-quartile CA125+CEA — médiane
  Kaplan-Meier, log-rank contre le reste) + Cox continu (HR par +1
  écart-type) univarié (un gène à la fois) et multivarié (KRAS+MUC16+
  CEACAM5). Implémentation numpy (KM, log-rank, Cox Breslow Newton-Raphson),
  même que la survie TCGA.
- **Fichiers produits :**
  - `geo71729_survival_table.csv` — SHA `1f7a14a7a696…` (145 lignes :
    step, GSM, KRAS, 12 gènes, os_months, dead, sous-types).
  - `geo71729_survival_results.txt` — paysage + Cox.

## Corrections trouvées pendant la vérification (16 nov. 2026)
1. **Log-rank faux (CORRIGÉ) :** la première exécution passait les décès
   en entiers (0/1) ; `t1[e1]` faisait alors de l'indexation fantaisie au
   lieu d'un masque booléen. Le top20 sortait à p=0,008 (faux positif).
   Après correction (conversion booléenne dans `logrank`), les vraies p
   sont top12 0,886 / top7 0,710 / top20 0,758 — vérifiées par une
   ré-implémentation indépendante. Les médianes KM n'étaient pas touchées.
2. **« Univarié » mal étiqueté (CORRIGÉ) :** la première version appelait
   `cox_fit` une seule fois avec les 6 gènes et présentait le résultat
   comme univarié — c'était l'ajustement à 6 gènes (KRAS 1,32, CEA 0,83,
   PGC 0,75). Les vrais univariés (un gène à la fois, vérifiés par une
   maximisation groupée de Breslow indépendante, scipy) sont KRAS 1,24 /
   MUC16 1,06 / CEA 1,00 / PGC 0,85. L'ajustement à 6 gènes est gardé en
   référence, étiqueté comme tel.
3. **À VÉRIFIER côté parent (TCGA) :** le script de survie TCGA utilisait
   la même structure — vérifier (a) que ses p log-rank viennent bien
   d'événements booléens (le code TCGA utilisait `str.startswith('1')`,
   donc booléen — probablement correct) et (b) que son tableau dit
   « univarié » est bien un gène à la fois et non un ajustement à 6 gènes
   (KRAS 1,29 / MUC16 1,28 / CEA 1,02 / PGC 1,00 / DPCR1 1,26 /
   CLDN18 0,96 — à confirmer).

## Résultats (n=125, 84 décès, OS médiane de la cohorte 17,0 mois)
- Paysage (log-rank corrigé) : top12 KRAS 17,0 contre 17,0 mois, p=0,886 ;
  top7 17,0 contre 16,0, p=0,710 ; top20 17,0 contre 16,0, p=0,758 ;
  quartile MUC16 17,0 contre 16,0, p=0,729 ; quartile CEACAM5 19,0 contre
  15,0, p=0,205 ; quartile KRAS 10,0 contre 19,0, p=0,020 (seul test de
  groupe significatif) ; double-quartile CA125+CEA 19,0 contre 16,0,
  p=0,456.
- Cox univarié (vrai, un gène à la fois) : KRAS HR 1,24 (p=0,075) ; MUC16
  HR 1,06 (p=0,58) ; CEACAM5 HR 1,00 (p=0,97) ; PGC HR 0,85 (p=0,15) ;
  DPCR1 HR 1,01 (p=0,90) ; CLDN18 HR 1,01 (p=0,95).
- Cox multivarié (KRAS+MUC16+CEACAM5) : KRAS HR 1,25 (p=0,066) ; MUC16
  HR 1,08 (p=0,51) ; CEACAM5 HR 0,93 (p=0,52).
- Cox ajusté 6 gènes (référence) : KRAS HR 1,32 (p=0,035) ; PGC HR 0,75
  (p=0,035) ; MUC16 HR 1,04 (p=0,76) ; CEACAM5 HR 0,83 (p=0,19) ;
  DPCR1 HR 1,07 (p=0,63) ; CLDN18 HR 1,14 (p=0,43).

## Verdict
**PARTIEL.** KRAS confirme en direction (HR 1,24–1,32 selon l'ajustement,
  même sens que TCGA 1,29) mais l'univarié n'atteint pas 0,05 (p=0,075) ;
  le quartile KRAS, lui, est significatif (10,0 contre 19,0 mois,
  p=0,020). CA125 ne confirme PAS (HR 1,06, p=0,58 ; multivarié 1,08,
  p=0,51 — contre TCGA multivarié 1,34, p=0,014). CEA : rien nulle part,
  comme en TCGA. Le groupe top12 (TCGA : 9,1 contre 20,4 mois, p=0,024)
  ne montre rien ici (17,0 contre 17,0, p=0,89). PGC protecteur seulement
  dans l'ajustement à 6 gènes (0,75, p=0,035), pas en univarié — fragile,
  pas un résultat.

## Ce qui manque
- Pas de survie sans progression (DFS) dans GEO pour cette série.
- 20/145 tumeurs primaires sans survie (sans OS ni statut).
- La survie est en mois entiers (43 temps distincts pour 125 patients) :
  beaucoup de liens, méthode de Breslow utilisée.
