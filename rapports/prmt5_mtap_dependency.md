# Dépendance PRMT5 contre statut MTAP mesuré — DepMap 24Q4 (16 nov. 2026)

## Verdict : OUI — les lignées MTAP-délétées dépendent plus de PRMT5

**Lignées pancréas (test principal) : les 20 lignées MTAP-délétées (CN < 0,5) ont
un effet Chronos PRMT5 médian de −1,385 contre −1,010 chez les 27 intactes
(différence −0,375, Mann-Whitney p = 0,0036). En continu : Spearman entre
Chronos PRMT5 et CN MTAP +0,497 (p = 0,0004, n = 47) — plus le CN MTAP est bas,
plus PRMT5 est essentiel. Pan-cancer (test de puissance) : même direction,
effet plus petit — délétées −1,092 contre intactes −0,977 (diff −0,114,
p = 1,7×10⁻¹⁴, n = 294 contre 884) ; Spearman +0,165 (p = 1,3×10⁻⁸, n = 1 178).
Les contrôles sont propres : KRAS et ACTB sont plats en Spearman continu
(+0,009 et +0,019, p = 0,77 et 0,51), et CDKN2A se comporte comme le contrôle
de locus attendu. C'est un appui mesuré au rationnel de la combinaison
vopimetostat + daraxonrasib — avec les limites honnêtes ci-dessous.**

## Ce qui a été fait

- **Statut MTAP mesuré** : `OmicsCNGene.csv` (DepMap 24Q4, figshare 27993248),
  téléchargé le 16 nov. 2026 (1 394 554 236 octets, MD5 exact
  `4696565fa74dc805983bc278b4a41802`), 1 929 modèles, 38 590 gènes.
- **Échelle du fichier** : CN relatif **linéaire** (1,0 = diploïde), pas log2 —
  depuis 24Q2 DepMap ne log-transforme plus la matrice CN relative (annonce
  24Q2, confirmé par le forum DepMap ; vérifié : médiane globale 1,012, aucune
  valeur négative, MTAP 12,8 % des modèles < 0,01). Seuils : délétion profonde
  CN < 0,5 ; sensibilité CN < 1.
- **Données Chronos** : `CRISPRGeneEffect.csv` déjà sur disque (SHA `3d8f3ec6…`),
  jointure sur 1 178 modèles avec les deux données ; 47 lignées pancréas.
- **Vérification interne** : Spearman PRMT5–KRAS sur les 47 pancréas = −0,189,
  identique au balayage génome entier — le pipeline de lecture est validé.

## Résultats détaillés

### Pancréas (47 lignées ; 20 délétées profondes, 38 sous-diploïdes)

| Gène | Délétées (CN<0,5) médiane | Intactes médiane | Diff | Mann-Whitney p |
|---|---|---|---|---|
| **PRMT5** | **−1,385 (n=20)** | **−1,010 (n=27)** | **−0,375** | **0,0036** |
| CDKN2A | +0,211 | +0,146 | +0,065 | 0,19 (ns) |
| KRAS | −1,903 | −1,648 | −0,256 | 0,30 (ns) |
| ACTB | −0,495 | −0,638 | +0,142 | 0,74 (ns) |

Sensibilité (CN < 1, 38 contre 9) : PRMT5 −1,126 contre −0,945, diff −0,181,
p = 0,030 — significatif mais plus faible, comme attendu (le groupe < 1 dilue
avec les pertes hétérozygotes). Note : à ce seuil large, ACTB sort à p = 0,041
(diff −0,200) avec seulement 9 intactes — probable bruit (tests multiples,
petit groupe) ; au seuil principal ACTB est propre (p = 0,74).

Spearman continus (pancréas) : PRMT5 vs CN MTAP **+0,497 (p = 0,0004)** ;
PRMT5 vs CN CDKN2A +0,528 (p = 0,0001) ; CDKN2A vs CN MTAP −0,287 (p = 0,050).

### Pan-cancer (1 178 modèles ; 294 délétés profonds)

| Gène | Délétées médiane | Intactes médiane | Diff | Mann-Whitney p |
|---|---|---|---|---|
| **PRMT5** | **−1,092 (n=294)** | **−0,977 (n=884)** | **−0,114** | **1,7×10⁻¹⁴** |
| CDKN2A | +0,214 | +0,132 | +0,082 | 9,3×10⁻¹³ |
| KRAS | −0,418 | −0,362 | −0,057 | 0,0053 |
| ACTB | −0,601 | −0,564 | −0,037 | 0,26 (ns) |

Spearman continus (pan-cancer) : PRMT5 vs CN MTAP **+0,165 (p = 1,3×10⁻⁸)** ;
CDKN2A vs CN MTAP −0,209 (p = 4,4×10⁻¹³) ; PRMT5 vs CN CDKN2A +0,149
(p = 2,8×10⁻⁷) ; KRAS vs CN MTAP +0,009 (p = 0,77) ; ACTB vs CN MTAP +0,019
(p = 0,51).

Note sur le KRAS pan-cancer (MW p = 0,005, diff −0,057) : avec n = 1 178, une
toute petite différence devient significative ; l'effet est 2× plus petit que
celui de PRMT5 et le Spearman KRAS est plat (+0,009). Le test continu, plus
fin, sépare nettement PRMT5 des témoins.

### Contrôles et spécificité 9p21

- **CDKN2A** : Chronos plus haut dans le groupe délété (+0,214 contre +0,132
  pan-cancer ; +0,211 contre +0,146 pancréas) — direction prédite : le gène
  étant déjà absent, son knockout ne fait rien. Le contrôle de classification
  fonctionne, et le Spearman CDKN2A–MTAP CN (−0,209, p = 4,4×10⁻¹³) confirme
  que la classification capte l'état du locus 9p21.
- **Co-délétion** : CN MTAP contre CN CDKN2A, pancréas : Spearman +0,808
  (p = 6,4×10⁻¹²) — les deux gènes sont presque toujours perdus ensemble.
- **Limite de spécificité** : le signal PRMT5 suit le CN MTAP (+0,497) comme
  le CN CDKN2A (+0,528) — ce test seul ne sépare pas « effet MTAP » de
  « effet délétion 9p21 entière ». La spécificité MTAP vient de la littérature
  (l'accumulation de MTA inhibe partiellement PRMT5 dans les cellules
  MTAP-nulles : Mavrakis et al., *Science* 2016 ; Kryukov et al., *Science*
  2016), pas de ce test.

### Taux de délétion MTAP mesurés

Pancréas : 20/47 (42,6 %) délétées profondes (les 20 sont des adénocarcinomes ;
les 2 adénosquameux sont intactes), 38/47 (80,9 %) sous-diploïdes. Pan-cancer :
294/1 178 (25,0 %) profondes. Les lignées pancréas sont donc enrichies en
délétion MTAP par rapport à la moyenne des cancers.

## Ce que ça veut dire pour la combinaison vopimetostat

**Appui mesuré, pas une preuve clinique.** Le rationnel est confirmé sur les
données : les cellules MTAP-délétées dépendent davantage de PRMT5, et
l'effet est **plus fort en pancréas** (diff −0,375 ; Spearman +0,497) que dans
l'ensemble des cancers (diff −0,114 ; Spearman +0,165). C'est cohérent avec
les 82 % de réponses de vopimetostat + daraxonrasib chez les MTAP-délétés
(phase 1/2) : la combinaison exploite une vulnérabilité réelle et mesurable,
pas une hypothèse en l'air.

**Limites honnêtes :**
- PRMT5 est essentiel dans les deux groupes (médiane −1,010 même intactes) :
  c'est une **fenêtre thérapeutique** (inhibition partielle sélective), pas une
  dépendance absolue. L'effet Chronos ne prédit pas à lui seul une réponse
  clinique.
- Ce test porte sur la **dépendance PRMT5**, pas sur la combinaison : il ne
  dit rien de l'addition du daraxonrasib (ni synergie, ni absence de synergie).
- La spécificité MTAP contre délétion 9p21 entière n'est pas démontrable avec
  ces seules données (voir ci-dessus).
- Le lien PRMT5–KRAS reste nul (rho −0,189, FDR 0,87 dans le balayage ;
  reproduit ici) : la dépendance PRMT5 ne suit pas l'axe KRAS, elle suit le
  statut MTAP — les deux axes sont indépendants, ce qui est cohérent avec le
  fait que la combinaison cible un sous-groupe distinct (MTAP-délétés, ~24 %).

## Corrections en cours de route (traçabilité)

1. **Échelle CN** : v1 du script supposait log2 (seuils < −1 et < 0) → zéro
   lignée classée délétée. Corrigé après vérification (forum DepMap + distribution).
2. **Étiquettes de colonnes** : v1 renommait les colonnes Chronos par position ;
   le fichier les trie alphabétiquement — PRMT5 et ACTB étaient échangés
   (contrôle de cohérence raté : +0,060 au lieu de −0,189). Corrigé : renommage
   par le nom. Après correction, le contrôle passe exactement.

## Fichiers

- `prmt5_mtap_dependency.py` — script (exit 0, 31 s)
- `prmt5_mtap_dependency.log` — journal complet
- `data/prmt5_mtap_results.csv` (SHA `e7c90e9a847c…`, 25 lignes)
- `data/prmt5_mtap_pancreas_lines.csv` (SHA `348ccfa975ed…`, 47 lignées)
- `PROVENANCE_prmt5_mtap.md` — provenance complète
