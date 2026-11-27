# Séparation MTAP vs délétion 9p21 entière — DepMap 24Q4 (16 nov. 2026)

## Verdict : OUI — l'effet PRMT5 suit MTAP, pas la délétion 9p21

La limite honnête du §8.28 du livre blanc est levée : MTAP et CDKN2A sont
presque toujours perdus ensemble, mais les lignées **CDKN2A-délétées sans
perte profonde de MTAP existent (137 sur 1 178 modèles)** — et elles ne
dépendent pas plus de PRMT5 que les lignées intactes. La dépendance PRMT5
supplémentaire n'apparaît que quand MTAP est perdu aussi.

## Chiffres (test principal : pan-cancer, 1 178 modèles, CN < 0,5 = délétion profonde)

| Groupe | n | PRMT5 Chronos médiane | KRAS méd. | ACTB méd. |
|---|---|---|---|---|
| MTAP + CDKN2A délétés | 293 | **−1,098** | −0,416 | −0,602 |
| CDKN2A seul délété | 137 | −1,013 | −0,361 | −0,575 |
| Ni l'un ni l'autre | 747 | −0,973 | −0,362 | −0,557 |
| MTAP seul délété | 1 | −0,989 | −0,440 | −0,293 |

- Both-del contre CDKN2A-seul : Mann-Whitney **p = 1,5×10⁻⁵** (hors pancréas : p = 6,5×10⁻⁵, n = 273 contre 130).
- CDKN2A-seul contre neither : **p = 0,26** (hors pancréas : p = 0,34) — pas de différence.
- Both-del contre neither : p = 1,3×10⁻¹⁴.
- Dans les lignées CDKN2A-délétées seules (n = 430) : Spearman PRMT5 ~ CN MTAP **+0,244 (p = 2,9×10⁻⁷)**, contre PRMT5 ~ CN CDKN2A +0,122 (p = 0,011) — le CN MTAP suit la dépendance deux fois plus fort que le CN CDKN2A.
- Contrôles propres : KRAS et ACTB plats entre les groupes.

## Pancréas seul (vérification, reproduit le comptage manuel)

- Both-del n = 20, PRMT5 −1,385 ; CDKN2A-seul n = 7, PRMT5 −1,049 ; neither n = 20, PRMT5 −0,984.
- Both-del contre CDKN2A-seul : p = 0,081 (même direction, petit n) ; CDKN2A-seul contre neither : p = 0,46.
- MTAP-seul : n = 0 en pancréas, n = 1 au pan-cancer — la perte de MTAP sans perte de CDKN2A n'existe quasiment pas. La séparation ne peut se faire que dans ce sens-là (CDKN2A-seul), et elle est faite.

## Ce que ça change

- Le rationnel de la combinaison vopimetostat + daraxonrasib gagne un appui
  mesuré de plus : la fenêtre PRMT5 est liée à la perte de MTAP elle-même,
  pas à la perte du locus 9p21 en général. Ça ne prouve pas la combinaison
  (toujours phase 1/2 non randomisée, n = 22), mais ça enlève l'objection
  « effet 9p21 » du §8.28.
- Limite restante : PRMT5 reste essentiel même sans délétion (médiane
  −0,973 chez les intactes) — fenêtre thérapeutique, pas dépendance absolue.
  Et ce test porte sur la dépendance PRMT5 seule, pas sur la combinaison.

## Honnêteté d'instrument

Test direct sur les données DepMap, comme le §8.28 — pas un run v6
(réel contre nul). Le pipeline n'a pas été lancé sur cette question.

## Fichiers

- Script : `prmt5_mtap_9p21_separation.py` (lecture par blocs, mêmes sources
  et seuils que `prmt5_mtap_dependency.py`)
- Log : `prmt5_mtap_9p21_separation.log`
- Données par lignée : `data/prmt5_mtap_pancancer_lines.csv`
  (SHA `1085cbb14d21bec4358947b5d35d76c51352294a09b2e46b423612891cec2c03`)
- Sources : `OmicsCNGene.csv` (DepMap 24Q4, MD5 vérifié
  `4696565fa74dc805983bc278b4a41802`) et `CRISPRGeneEffect.csv`, déjà sur disque.
- Durée : 23,4 s. Protocole : CN relatif linéaire (1,0 = diploïde),
  délétion profonde CN < 0,5 ; aucune imputation, paires complètes seulement.
