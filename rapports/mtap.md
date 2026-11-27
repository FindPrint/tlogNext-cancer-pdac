# Bras 1 — MTAP / PRMT5 et l'axe KRAS (TCGA-PAAD, tests directs)

**Date : 16 novembre 2026. Test direct, pas de run v6 dans ce bras.**

## Verdict

**NON — la délétion MTAP n'est pas démontrée enrichie chez les KRAS-forts.**

- Délétion profonde MTAP (GISTIC −2, mesurée, pas un proxy) : **6/12 KRAS-forts
  (50 %) contre 37/165 pour le reste (22 %) ; OR = 3,46 ; test exact de Fisher
  bilatéral (critère pré-enregistré) p = 0,073 — non significatif.**
- Le signal va dans le sens d'un enrichissement (attendu sous hasard : 2,9/12 ;
  permutation unilatérale p = 0,038), mais avec 12 KRAS-forts seulement la
  puissance est trop faible pour trancher : un enrichissement réel de cette
  ampleur demanderait une cohorte plus grande pour être confirmé ou infirmé.
- Expression MTAP : **aucun lien avec l'axe KRAS** — Spearman rho +0,125,
  p = 0,097 ; top-12 −0,27 sd, Welch p = 0,45 ; identique après correction de
  pureté (rho +0,135, p = 0,073 ; top-12 −0,03 sd).

**Donc la combinaison vopimetostat + daraxonrasib ne s'adresse pas aux mêmes
patients que l'axe KRAS.** Elle s'adresse aux patients MTAP-délétés — 24 %
des tumeurs ici (43/177) — un sous-groupe qui **recoupe partiellement** les
KRAS-forts (la moitié d'entre eux sont délétés) mais qui n'est pas le même
groupe : l'enrichissement n'est pas démontré, et la moitié des KRAS-forts ne
sont pas MTAP-délétés. Le ciblage MTAP est orthogonal à l'axe KRAS dans les
limites de cette cohorte.

**Le fait nouveau de ce bras, lui, est positif et tient après correction de
pureté : l'expression PRMT5 monte avec KRAS** — rho +0,196, p = 0,0087
(Bonferroni 3 gènes : p < 0,0167) ; top-12 +0,83 sd, Welch p = 0,0007,
d de Cohen +0,84 ; 7/12 KRAS-forts au-dessus du quartile supérieur (attendu 3).
Après correction de pureté v3 : rho +0,216, p = 0,0039 ; top-12 +0,90 sd.
Mais attention : **expression ≠ dépendance**. Le balayage CRISPR DepMap déjà
mesuré (cité, pas réimporté comme verdict) ne montre aucune dépendance PRMT5
liée à KRAS (rho −0,189, FDR 0,87). L'expression PRMT5 élevée chez les
KRAS-forts ne se traduit pas en dépendance mesurée — c'est une hypothèse à
tester, pas une cible validée par ce bras.

## Résultats chiffrés

### Test 1 — expression contre l'axe KRAS (n = 178, brut puis résidus pureté v3)

| Gène | rho KRAS (brut) | p | top-12 (sd) | Welch p | d Cohen | >Q3 (attendu 3) | rho (résidus) | p (résidus) | top-12 résidus |
|---|---|---|---|---|---|---|---|---|---|
| MTAP | +0,125 | 0,097 | −0,27 | 0,45 | −0,27 | 3/12 | +0,135 | 0,073 | −0,03 |
| **PRMT5** | **+0,196** | **0,0087** | **+0,83** | **0,0007** | **+0,84** | **7/12** | **+0,216** | **0,0039** | **+0,90** |
| CDKN2A | −0,063 | 0,40 | −0,19 | 0,55 | −0,19 | 4/12 | −0,058 | 0,44 | −0,01 |

Seuil Bonferroni 3 gènes : p < 0,0167. Seul PRMT5 le passe, dans les deux versions.

### Test 2 — délétion mesurée (GISTIC2, n = 177 appariées sur 178)

Fichier `all_thresholded.by_genes.txt` : −2 = délétion profonde (homozygote),
−1 = perte peu profonde (hétérozygote). Une tumeur sans échantillon GISTIC
(TCGA-FB-A4P6, hors top-12) — sans effet sur les comptes des KRAS-forts.

| Gène | Statut | KRAS-forts | Reste | OR | Fisher bilatéral p |
|---|---|---|---|---|---|
| MTAP | délétion profonde (−2) | 6/12 (50 %) | 37/165 (22 %) | 3,46 | **0,073 (ns)** |
| MTAP | perte quelconque (−2 ou −1) | 11/12 (92 %) | 94/165 (57 %) | 8,31 | 0,029 |
| CDKN2A | délétion profonde (−2) | 6/12 (50 %) | 43/165 (26 %) | 2,84 | 0,095 (ns) |
| CDKN2A | perte quelconque (−2 ou −1) | 12/12 (100 %) | 97/165 (59 %) | inf | 0,0037 |

Prévalence MTAP −2 sur la cohorte : 43/177 = 24,3 % (cohérent avec ~25 %
rapporté dans la littérature PDAC). CDKN2A −2 : 49/177 = 27,7 %.

**Lecture des lignes « perte quelconque » (secondaires, pas le critère
pré-enregistré) :** la perte −1 est fréquente (62/177 pour MTAP) et **ne
baisse pas l'expression MTAP** (médiane 9,18 contre 9,09 pour les diploïdes ;
voir contrôle qualité ci-dessous). Ce n'est donc pas une délétion
fonctionnelle — ces deux lignes ne doivent pas être lues comme « 11/12 des
KRAS-forts sont MTAP-délétés ». Le critère qui compte est la délétion
profonde −2 : p = 0,073, non démontrée.

- Permutation MTAP −2 (10 000 mélanges des 12 étiquettes KRAS-fort, graine 42,
  urne n = 177) : observé 6/12 ; p unilatérale = 0,038. Cohérent avec le
  Fisher : signal dans le même sens, sous le seuil unilatéral, au-dessus du
  seuil bilatéral pré-enregistré. **Suggestif, pas démontré.**
- Co-délétion 9p21 (n = 177) : MTAP −2 et CDKN2A −2 : 43 ; MTAP −2 seul : 0 ;
  CDKN2A −2 seul : 6 ; aucun : 128. **Toute délétion profonde MTAP est
  co-délétée avec CDKN2A** — attendu pour le locus 9p21, confirmé ici.

Contrôle qualité (expression MTAP médiane selon statut GISTIC) : −2 : 7,69
(n = 43) ; −1 : 9,18 (n = 62) ; 0 : 9,09 (n = 69) ; +1 : 8,58 (n = 2) ;
+2 : 7,66 (n = 1). La délétion profonde abaisse bien l'expression (~1,4 unité
log2) : les appels GISTIC sont cohérents avec l'ARN. La perte −1, elle, ne
l'abaisse pas.

### Test 3 — contrôles

- MTAP contre PRMT5 (expression) : rho **+0,237, p = 0,0015** — corrélation
  positive. Au niveau de l'expression, MTAP et PRMT5 montent ensemble ;
  ce n'est pas l'image naïve « MTAP perdu → PRMT5 monte ». La dépendance
  PRMT5 liée à la perte MTAP est un phénotype CRISPR, pas une corrélation
  d'expression — et le CRISPR DepMap cité ne la relie pas à KRAS.
- MTAP contre score acineux (pureté) : rho +0,094, p = 0,21 ; contre score
  îlots : rho +0,112, p = 0,14. **MTAP n'est pas sensible à la pureté.**
  R² pureté (v3) : MTAP 5,1 % ; PRMT5 1,4 % ; CDKN2A 2,2 % ; KRAS 0,3 %.
  La pureté n'est pas un facteur confondant dans ce bras — et le signal
  PRMT5 survit d'ailleurs à la correction.

## Ce que cela change, et ce que cela ne change pas

- **Ne change pas :** la combinaison vopimetostat + daraxonrasib reste la
  piste la plus solide du projet (82 % de réponses chez les MTAP-délétés,
  phase 1/2 NCT06922591, ESMO 2026 — résultat clinique externe, pas une
  prédiction du pipeline). Son biomarqueur est la délétion MTAP, présente
  chez 24 % des tumeurs, pas l'axe KRAS.
- **Change :** on ne peut pas présenter les KRAS-forts comme « les patients
  MTAP » — la moitié seulement le sont, et l'enrichissement n'est pas
  démontré. Si un essai devait cibler les KRAS-forts, il faudrait tester
  MTAP séparément chez chacun d'eux.
- **Nouvelle hypothèse (à tester, pas un verdict) :** PRMT5 s'exprime plus
  chez les KRAS-forts. Le CRISPR dit déjà que la dépendance PRMT5 ne suit
  pas KRAS — donc l'expression seule ne suffit pas à justifier une
  combinaison KRAS + PRMT5. Angle suivant possible : dépendance PRMT5 contre
  statut MTAP (délétion mesurée) dans DepMap, plutôt que contre KRAS.

## Limites

- n = 12 KRAS-forts : la puissance du Fisher est faible. Avec 6/12 contre
  22 % attendus, l'intervalle est large ; seule une cohorte plus grande
  (TCGA complet actuel, ou ICGC/GEO avec copy-number) peut confirmer ou
  infirmer l'enrichissement.
- L'axe est l'expression KRAS, pas la mutation KRAS : 178 tumeurs, KRAS
  muté chez ~90 % des PDAC, donc l'axe mesure un niveau d'expression, pas
  un statut muté/non muté.
- Le GISTIC date de 2016 (même run que l'expression) : les appels sont
  ceux de Firehose 2016-01-28, pas d'un appel moderne.

## Provenance (résumé — complète dans `PROVENANCE_mtap.md`)

- Expression : Broad GDAC Firehose stddata 2016-01-28, PAAD, RSEM normalisé,
  MD5 vérifié `b09569ce3f4721f514bc137bd109ac0a` ; 178 tumeurs primaires (01) ;
  log2(RSEM+1). Même matrice que v1.
- Copy-number : Broad GDAC Firehose **analyses** 2016-01-28, PAAD,
  `gdac.broadinstitute.org_PAAD-TP.CopyNumber_Gistic2.Level_4.2016012800.0.0.tar.gz`
  (26 189 717 octets), MD5 vérifié `816034f742e8f89ca8734ca2cf4404d5`,
  SHA256 `6edc20f365d2f828bf5b4ef90a93f67344928d069cdd138eb946ed3275eed0ed`,
  fichier interne `all_thresholded.by_genes.txt` (24 776 gènes × 184
  échantillons). Téléchargé le 16 nov. 2026 — **aucun proxy « MTAP bas »
  utilisé : la délétion est mesurée.**
- Définitions : KRAS-fort = 12 tumeurs à plus forte expression KRAS brute ;
  top12_sd = (moyenne top12 − moyenne reste) / écart-type (ddof=0) ;
  Bonferroni 3 gènes p < 0,0167 ; permutation 10 000 mélanges, graine 42.
- Faits cités sans être réimportés comme verdicts : balayage CRISPR DepMap
  24Q4, 47 lignées pancréas — dépendance Chronos contre KRAS : PRMT5 rho
  −0,189 (FDR 0,87), MTAP +0,071 (FDR 0,96), CDKN2A +0,161 (FDR 0,89),
  tous non significatifs.

## Fichiers

- Script : `mtap_kras_tests.py`
  (SHA256 `162aeff73f9ba919f1404daef2911e8ec3ed5b07d1ef139aede587d7fef5245f`)
- `mtap_direct_tests.csv`
  (SHA256 `9b445ac01d625e42fe876889515f48d7ffea9f6b7836a506f572e907c2d47b83`)
- `mtap_controls.csv`
  (SHA256 `51e1f93cb61b06facd3bbf35a342d2e133510352cb9ad18885cfbc3953a445e0`)
- `mtap_gistic_status.csv` — statut GISTIC MTAP/CDKN2A par tumeur, ordre KRAS
  (SHA256 `b54cb94ff6aaba67e71524476d4e47c567f20ca8d49c09c52a9118977a7c38cb`)
- `mtap_direct_tests.txt`
  (SHA256 `02c693ebfd170d454a294103faa0784dd77d05d7d0cf9dc2a397119a713152f5`)
- `PROVENANCE_mtap.md` — provenance complète (JSON)
- Données : `data/tcga_paad_gistic.tar.gz` (+ `.md5`)
