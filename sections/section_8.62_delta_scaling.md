# §8.62 Loi d'échelle en n pour Delta — chantier (20 novembre 2026)

**Verdict d'abord : AUCUNE LOI D'ÉCHELLE EN n N'EST TROUVÉE POUR DELTA,
et une telle loi ne peut pas expliquer pourquoi Delta ne sépare pas le
réel du nul.** Sur les 222 runs détenus, la meilleure forme en n
explique 67,3 % de la variance de Delta (quadratique en ln n, R²=0,673),
loin du seuil de 0,80 — et en leave-one-cohort-out, la forme log n
tombe à R²=−0,005 : elle ne porte pas d'une cohorte à l'autre. Le lot
causal B (même matrice, n qui varie, 31 runs v6.2, 31/31 exit 0)
confirme que Delta croît bien avec n à matrice fixée, mais avec une
pente qui dépend de la matrice (1,08 pour HP35, 0,82 pour LUAD, 1,91
pour TCGA) et de façon non monotone (LUAD redescend à son n plein) —
ce n'est pas une loi universelle, c'est une tendance locale. Et le point
logique est décisif : le réel et son nul partagent le même n, donc toute
loi en n pur leur prédit le même Delta ; or sur les 106 paires réel/nul,
la moitié seulement (53/106) a |Delta_réel − Delta_nul| ≤ 0,10, avec un
écart-type de 0,536 — retirer la loi en n ne change rien à ces écarts
(53/106 identiques). **La non-séparation de Delta ne vient pas de n :
elle vient de l'ordre des lignes, que n ne voit pas.** Nuance honnête,
mesurée et non cherchée après coup : une loi d'échelle **est** trouvée
pour quatre estimateurs — Katz, Petrosian, Sevcik et GraphDimension,
sous la forme quadratique en ln n (F2), qui passe les trois volets du
critère — mais aucun des quatre ne porte Delta, et aucun estimateur qui
décide de la paire (LocalPCA, LevinaBickel, PCAIntrinsic, MFA) n'a de
loi. Delta reste une piste fragile et ne devient pas un discriminateur
recommandé.

## §8.62.1 Ce qui était acquis avant ce chantier

Le §8.42.5 avait établi que `log(n)` est le meilleur trait unique pour
12 cibles sur 13 (BoxCounting r=+0,932, Petrosian −0,949, Katz −0,922,
LevinaBickel +0,868, MFA +0,847, LocalPCA +0,824) et conclu que « les
magnitudes portent l'échelle de n, pas le contenu des flux ». Le §8.57
avait confirmé depuis les séries entières que les magnitudes sont presque
recalculées par la moitié de leur propre construction (meilleur modèle
honnête 89,2 % / 90,5 %, sous le critère ≥ 90 %), sans élucider Delta.
La question restée ouverte au §8.42.9 point 2 et au §8.57.9 point 1 était
analytique : pourquoi chaque estimateur croît ou décroît avec n, et avec
quelle forme (log ? puissance ?) — y compris pour DFA et ses extrêmes
(−38,16). Ce chantier est cette question, testée en deux temps : d'abord
sur les 222 runs détenus (ensemble A, descriptif), puis causalement, en
faisant varier n à matrice fixée (ensemble B, 31 runs v6.2 nouveaux).

## §8.62.2 Méthode du chantier

Protocole gelé `PROTOCOL_delta_scaling_862.md` avant toute modélisation
et avant tout run (SHA `8e67f8c7f17f92d297c5cbf02884e9a82778dd6c20fb8ee681afb3b24fb995b0`,
après une correction consignée avant exécution : le stride défini d'abord
par « une ligne sur m, m = arrondi(n/k) » ne donnait pas k lignes —
ex. n=1000, k=285 → 250 lignes — remplacé par des indices régulièrement
espacés de linspace(0, n−1, k)) ; script `v62_delta_scaling_862.py`.
Sept formes candidates, les mêmes pour les 16 cibles (13 médianes +
d_div + d_sat + Delta), ajustées par moindres carrés ordinaires :
F0 constante ; F1 a+b·ln n ; F2 a+b·ln n+c·(ln n)² ; F3 a+b·n ;
F4 a+b/n ; F5 a+b/√n ; F6 a+b·√n. Aucune autre forme.

**Ensemble A (222 runs, 156 matrices, 9 cohortes, identique aux
§8.39/§8.42/§8.57).** Cibles parsées depuis `v62_delta_levels.csv` ;
identités d_div/d_sat re-vérifiées : 0 écart > 10⁻³ sur 222/222 ; 0 écart
entre n du CSV et n du JSON. Hold-out primaire : leave-one-cohort-out
(LOCO) pour F1. Paires réel/nul : 106 paires appariées par nom de dossier.

**Ensemble B (31 runs v6.2 fast nouveaux, §8.62.3).** Trois matrices
sources à contrôle `step` (SHA notés) : HP35 réel
(`test_biophysique_input.csv`, n=1000, p=7) et son nul, LUAD
(`pdac_luad_fluxes.csv`, n=515, p=12), TCGA v4
(`pdac_tcga_fluxes_v4.csv`, n=178, p=12). Sous-échantillons PRÉFIXE
(les k premières lignes, `step` réécrit 0..k−1) aux tailles
k ∈ {45, 70, 100, 145, 178, 285, 515, 1000} ∩ k ≤ n : HP35 réel 8 runs,
HP35 nul 8, LUAD 7, TCGA 5 = 28 runs ; plus STRIDE (k lignes
régulièrement espacées couvrant toute la série) pour HP35 réel à
k ∈ {100, 285, 515} = 3 runs. Commande identique aux lots précédents
(`python3 universal_v6.2.0_cohen.py --input <csv> --mode fast --output
<dir>`), lancement via `systemd-run`, journal des exit codes.

**Critères gelés.** LOI TROUVÉE pour une cible si UNE MÊME forme atteint
(a) R² ≥ 0,80 sur A (222 runs) ET (b) R² ≥ 0,80 sur B poolé (31 runs) ET
(c) transfert A→B : ≥ 90 % des points B prédits à ±0,10. LA LOI SUFFIT À
EXPLIQUER LA NON-SÉPARATION si la loi est trouvée pour Delta ET (i) à n
fixé, l'écart-type intra-cohorte de Delta est ≤ 0,10 dans au moins 6 des
8 cohortes à n unique, ET (ii) le résidu Delta − F1(ln n) ne sépare pas
réel de nul (≥ 90 % des paires avec |Δrésidu| ≤ 0,10 et |moyenne| ≤ 0,10),
ET (iii) en B, courbes HP35 réel vs nul coïncidentes à ±0,10 sur au moins
7 des 8 tailles.

## §8.62.3 Résultats A : log n porte le niveau, pas la loi

| Cible | F1 ln n R² | F2 (ln n)² R² | Meilleure forme (R²) | LOCO F1 R² | r(y, ln n) |
|---|---|---|---|---|---|
| LevinaBickel | 0,753 | 0,799 | F2 0,799 | 0,472 | +0,868 |
| PCAIntrinsic | 0,207 | 0,360 | F2 0,360 | −0,425 | +0,455 |
| LocalPCA | 0,679 | 0,707 | F2 0,707 | 0,258 | +0,824 |
| GraphDimension | 0,726 | 0,817 | F2 0,817 | 0,564 | +0,852 |
| PersistentHomology | 0,430 | 0,659 | F2 0,659 | −0,263 | +0,655 |
| MFA | 0,717 | 0,808 | F2 0,808 | 0,253 | +0,847 |
| Higuchi | 0,139 | 0,195 | F3 0,197 | −0,064 | −0,373 |
| Katz | 0,851 | 0,949 | F4 0,955 | 0,610 | −0,922 |
| Petrosian | 0,901 | 0,970 | F2 0,970 | 0,745 | −0,949 |
| Sevcik | 0,785 | 0,877 | F4 0,876 | 0,562 | +0,886 |
| BoxCounting | 0,868 | 0,985 | F2 0,985 | 0,583 | +0,932 |
| Hurst2mH | 0,474 | 0,827 | F2 0,827 | −0,401 | +0,689 |
| DFA | 0,299 | 0,451 | F4 0,461 | −0,418 | +0,547 |
| d_div | 0,646 | 0,736 | F2 0,736 | 0,073 | +0,804 |
| d_sat | 0,632 | 0,826 | F4 0,835 | 0,053 | +0,795 |
| **Delta** | **0,599** | **0,673** | **F2 0,673** | **−0,005** | **+0,774** |

Lecture :

- **Delta échoue au volet (a) pour toutes les formes.** La meilleure,
  F2 (quadratique en ln n), n'explique que 67,3 % de sa variance sur les
  222 runs ; F1 (log n) 59,9 %, MAE 0,574 — cinq fois la tolérance ±0,10.
  Le critère de loi est donc déjà manqué avant même le lot B : aucune
  forme en n seul ne prédit Delta à ±0,10 sur les runs détenus.
- **La forme log n ne porte pas d'une cohorte à l'autre.** En LOCO,
  F1 pour Delta tombe à R²=−0,005 (pire que la constante du train) :
  tenir une cohorte à l'écart, c'est tenir ses n à l'écart, et
  l'extrapolation échoue — y compris sur les petites cohortes (MAE LOCO
  par pli pour Delta : luad 2,615 ; hp35 1,670 ; tcga 1,154 ; icgc 0,979 ;
  geo62452 1,051 ; depmap 0,281). Seuls trois estimateurs gardent un
  R² LOCO > 0,5 (Petrosian 0,745 ; Katz 0,610 ; BoxCounting 0,583) —
  les trois mêmes dont la forme en n est la plus forte en échantillon.
- **Ce n'est pas « log n » qui est la bonne forme, c'est « 1/n » pour
  la saturation.** F4 (a+b/n) bat F1 pour Katz (0,955 contre 0,851),
  BoxCounting (0,972 contre 0,868), Petrosian (0,959 contre 0,901),
  Sevcik (0,876 contre 0,785), d_sat (0,835 contre 0,632) et DFA
  (0,461 contre 0,299). La saturation sature en 1/n, pas en log n —
  le §8.42.5 avait nommé log n « meilleur trait unique » parmi ses 41
  traits, mais 1/n n'y figurait pas comme trait. Pour la divergence,
  F2 domine ; aucune forme unique ne sert les 16 cibles.
- **Les cibles qui résistent sont celles qui portent la paire.**
  PCAIntrinsic (F1 R²=0,207, LOCO −0,425) et Higuchi (0,139, LOCO
  −0,064) ne suivent presque pas n ; LocalPCA, toujours dans la paire,
  n'est qu'à 0,679 / LOCO 0,258. La loi en n, même là où elle existe,
  ne touche pas les estimateurs qui décident de la paire.
- **Moyennes par matrice (156, contre la pseudo-réplication) :**
  Delta F1 R²=0,633, F2 R²=0,684 ; d_div 0,690 / 0,752 ; d_sat 0,743 /
  0,870. Les chiffres ne bougent pas : l'échec n'est pas un artefact
  des rep2 / v6.1+v6.2.
- **Sensibilités F1 pour Delta :** sans les 22 runs |DFA| > 10 :
  R²=0,540 (n=200) ; sans hp35 (n=1000, seul point au-delà de 515) :
  R²=0,628 (n=216) ; déduplication §8.39.6 (153 runs) : R²=0,632.
  La loi ne tient pas mieux sans son point extrême ni sans les
  extrêmes de DFA — elle est faible partout, pas tirée par des
  points isolés.

## §8.62.4 À n fixé, Delta varie — et le résidu réel/nul ne bouge pas

**À n fixé (7 cohortes à n unique, tcga exclue car n=177/178) :**

| Cohorte | n | Runs | Écart-type Delta | Étendue Delta | Écart-type d_div |
|---|---|---|---|---|---|
| coad | 285 | 4 | 0,012 | 4,599–4,619 | 0,013 |
| depmap | 45 | 30 | 0,096 | 1,667–1,952 | 0,026 |
| geo62452 | 69 | 14 | 0,060 | 1,260–1,412 | 0,072 |
| geo71729 | 145 | 20 | **0,292** | 2,159–2,965 | 0,279 |
| hp35 | 1000 | 6 | 0,049 | 4,483–4,572 | 0,107 |
| icgc | 70 | 10 | 0,066 | 1,321–1,499 | 0,010 |
| luad | 515 | 4 | 0,008 | 2,497–2,511 | 0,013 |

Six cohortes sur sept ont un écart-type de Delta à n fixé ≤ 0,10 — le
volet (i) du critère §6.2 est formellement passé — mais l'exception est
instructive : geo71729 (n=145, 10 matrices distinctes) étale Delta de
2,16 à 2,97 (écart-type 0,292, portée 0,81). À n fixé, des matrices
différentes donnent des Delta différents de 0,8 : n fixe le niveau
moyen de la cohorte, pas la valeur du run. Et dans tcga (n=178, 124
runs), l'étalement est du même ordre — c'est là que se joue la
non-séparation (voir ci-dessous).

**Réel contre nul (106 paires, même matrice, même version) :**
Delta_réel − Delta_nul : moyenne +0,077, écart-type 0,536,
|diff| ≤ 0,10 sur **53/106 (50,0 %)** seulement. Le résidu après retrait
de F1(ln n) donne exactement les mêmes chiffres (53/106, moyenne +0,077,
écart-type 0,536) — c'est mathématique : réel et nul partagent le même n,
donc F1(ln n) se retranche à l'identique des deux côtés. **Le volet (ii)
échoue : 50 % contre 90 % exigés.** La loi en n ne retire rien de
l'écart réel/nul, parce que l'écart réel/nul n'est pas en n : il est
dans l'ordre des lignes, que la permutation détruit et que n ne voit pas.

**La même loi pour le réel et pour le nul.** F1 pour Delta ajustée sur
les réels seuls (n=116) : R²=0,620, β=[−3,068 ; 1,270] ; sur les nuls
seuls (n=106) : R²=0,576, β=[−3,348 ; 1,321]. Mêmes pente et intercept à
l'erreur près : le nul suit la même loi d'échelle que le réel. Une loi
qui vaut identiquement des deux côtés ne peut pas séparer les deux côtés.
C'est la forme précise de l'explication négative : **Delta ne sépare pas
le réel du nul parce que ce qui, en lui, dépend de n est invariant par
permutation — et ce qui en dépend (l'écart réel/nul, écart-type 0,536)
ne dépend pas de n.**

## §8.62.5 Résultats B : Delta croît avec n — localement, non monotone, et autrement pour le nul

Lot B : **31/31 runs exit 0**, 31/31 valides (d_div/d_sat/Delta finis),
0 écart aux identités d_div/d_sat ; SHA v6.2 vérifié avant et après le
lot. Incident consigné : la machine a redémarré le 20 nov. ~13h21 UTC
pendant le lot initial (unité `delta-scaling-862` tuée au run 14,
hp35nul_n285, sans `master_results.json`) ; reprise
(`run_delta_scaling_862_resume.sh`, unité `delta-scaling-862-resume`)
sautant les 13 sorties valides et refaisant les 18 restantes, terminée
14:15:23 UTC, 31/31 exit 0 au total. Le dossier partiel du run tué a été
supprimé avant sa relance (aucun run ne tournait alors) ; les 13 runs
conservés n'ont pas été relancés.

**Delta par taille k, par courbe (préfixe) :**

| k | HP35 réel | HP35 nul | LUAD | TCGA v4 |
|---|---|---|---|---|
| 45 | 1,847 | 1,789 | 1,357 | 1,395 |
| 70 | 1,630 | 1,414 | 1,335 | 1,351 |
| 100 | 2,281 | 1,992 | 1,403 | 1,466 |
| 145 | 3,153 | 2,900 | 2,839 | 2,853 |
| 178 | 3,805 | 4,092 | 3,767 | 4,181 |
| 285 | 4,479 | 3,340 | 3,288 | — |
| 515 | 4,535 | 4,681 | 2,511 | — |
| 1000 | 4,483 | 4,572 | — | — |

Lecture :

- **Delta croît avec n à matrice fixée — puis sature ou redescend.**
  HP35 monte de ~1,8 à ~4,5 puis plafonne (4,54 à k=515, 4,48 à
  k=1000) ; TCGA monte jusqu'à son n plein (4,18) ; **LUAD monte puis
  redescend** (3,77 à k=178, 3,29 à k=285, 2,51 à k=515 — son n plein
  est plus bas que son k=178). Une « loi » qui redescend à n plein
  n'est pas une loi de croissance en n : le préfixe change le segment
  autant que la longueur, et le contenu du segment pèse autant que n.
  Même HP35 n'est pas monotone aux petites tailles (1,85 à k=45,
  1,63 à k=70).
- **La pente dépend de la matrice.** F1 intra-courbe pour Delta :
  HP35 R²=0,833, β=[−2,36 ; 1,084] ; HP35 nul R²=0,818, β=[−2,75 ;
  1,125] ; LUAD R²=0,455, β=[−1,69 ; 0,817] ; TCGA R²=0,715,
  β=[−6,46 ; 1,908]. Les pentes vont de 0,82 à 1,91, les intercepts
  de −1,69 à −6,46 : il n'y a pas de coefficients universels. Le
  poolé B (31 runs) le confirme : Delta F1 R²=0,651, F2 R²=0,679 —
  le volet (b) du critère (≥ 0,80) échoue comme le volet (a).
- **Le transfert A→B échoue pour Delta : 2/31 à ±0,10** (F1 comme F2 ;
  MAE de transfert 0,73 / 0,64). La loi ajustée sur les 222 runs ne
  prédit pas les sous-échantillons des mêmes matrices : ce n'est pas
  de l'extrapolation qui échoue, c'est la forme elle-même qui ne tient
  pas à matrice fixée. Le volet (c) échoue lui aussi.
- **Réel contre nul, à n fixé (HP35, 8 tailles) : les courbes ne
  coïncident pas.** Delta_réel − Delta_nul par k : +0,058 ; +0,216 ;
  +0,289 ; +0,253 ; −0,287 ; **+1,139** ; −0,146 ; −0,090 — seulement
  **2/8 ≤ 0,10** (volet (iii) : il en fallait ≥ 7/8). À k=285, le réel
  vaut 4,48 quand le nul vaut 3,34 : la courbe en n du nul n'est pas
  celle du réel. La loi d'échelle elle-même dépend de l'ordre — elle
  ne peut donc pas être l'explication de la non-séparation, elle en
  est une victime de plus. Pour d_div : 3/8 ≤ 0,10 ; pour d_sat :
  1/8 — et les 8 écarts de d_sat sont négatifs (−0,10 à −0,27) : le
  nul a systématiquement une d_sat plus haute que le réel, à toutes
  les tailles (la permutation relève la 4e médiane de saturation).
- **Le schéma de sous-échantillonnage change Delta (0/3).**
  Stride vs préfixe (HP35) : Delta −0,712 à k=100, +0,271 à k=285,
  **−1,739 à k=515** (stride 2,80 contre préfixe 4,54). À n fixé,
  Delta dépend de quelles lignes on garde, pas seulement de leur
  nombre. d_sat, elle, est stable entre schémas (2/3 ≤ 0,10 :
  +0,198 ; +0,044 ; +0,032) quand d_div ne l'est pas (0/3) — la même
  asymétrie qu'au §8.57 : la saturation est stable, la divergence
  bouge.

**Par cible, poolé B (31 runs) — la loi existe pour quatre estimateurs,
pas pour Delta :**

| Cible | F2 R² sur A | F2 R² sur B | Transfert F2 ≤ 0,10 | Loi ? |
|---|---|---|---|---|
| Katz | 0,949 | 0,905 | 31/31 | **TROUVÉE** |
| Petrosian | 0,970 | 0,972 | 31/31 | **TROUVÉE** |
| Sevcik | 0,877 | 0,887 | 31/31 | **TROUVÉE** |
| GraphDimension | 0,817 | 0,928 | 29/31 | **TROUVÉE** |
| BoxCounting | 0,985 | 0,986 | 24/31 | non (transfert) |
| LevinaBickel | 0,799 | 0,918 | 5/27 | non (A, transfert) |
| MFA | 0,808 | 0,863 | 0/31 | non (transfert) |
| LocalPCA | 0,707 | 0,729 | 0/31 | non |
| PCAIntrinsic | 0,360 | 0,124 | 7/31 | non |
| Higuchi | 0,195 | 0,106 | 29/31 | non (R²) |
| Hurst2mH | 0,827 | 0,477 | 25/31 | non (B) |
| DFA | 0,451 | 0,318 | 0/31 | non |
| d_div | 0,736 | 0,735 | 4/31 | non |
| d_sat | 0,826 | 0,614 | 23/31 | non (B) |
| **Delta** | **0,673** | **0,679** | **2/31** | **non** |

Quatre estimateurs passent les trois volets sous la même forme F2
(quadratique en ln n) : Katz, Petrosian, Sevcik (saturation) et
GraphDimension (divergence basse). Leurs transferts sont parfaits
(31/31, 31/31, 31/31, 29/31) — y compris sur les points stride, que la
forme F2 n'avait jamais vus. Mais aucun des quatre ne porte Delta :
ce sont les estimateurs bas de leurs familles, jamais dans la paire
médiane (GraphDimension est toujours l'une des deux plus basses,
§8.42). À l'inverse, les estimateurs qui décident de la paire échouent
tous : LocalPCA (F2 A 0,707, transfert 0/31), LevinaBickel (A 0,799 —
manque le volet (a) de 0,001 — transfert 5/27), PCAIntrinsic (0,360),
MFA (transfert 0/31 malgré R² > 0,80 des deux côtés : sa quasi-discrétion
en 9 valeurs casse le transfert). BoxCounting échoue de peu au transfert
(24/31, 77 %) malgré des R² de 0,985/0,986 : un R² presque parfait ne
garantit pas la prédiction à ±0,10. **La loi d'échelle en n existe —
par estimateur, en (ln n)² — mais elle s'arrête aux estimateurs qui ne
décident de rien.**

## §8.62.6 Conséquence : pas de loi pour Delta, et la non-séparation n'est pas en n

Application des critères gelés (§6) :

- **(Q1) LOI TROUVÉE — partiellement, pas pour Delta.** Pour Delta :
  (a) meilleur R² sur A = 0,673 (F2) < 0,80 ; (b) meilleur R² sur B
  poolé = 0,679 (F2) < 0,80 ; (c) transfert 2/31 < 90 %. Les trois
  volets échouent : **loi NON TROUVÉE pour Delta**, comme pour d_div
  (0,736 / 0,735 / 4/31) et d_sat (0,826 / 0,614 / 23/31). En revanche,
  la loi est **TROUVÉE pour Katz, Petrosian, Sevcik et GraphDimension**
  (F2, trois volets passés, tableau §8.62.5).
- **(Q2) LA LOI NE SUFFIT PAS À EXPLIQUER LA NON-SÉPARATION.** La loi
  pour Delta n'existe pas, donc elle ne peut rien expliquer ; et même
  ses volets partiels échouent : (i) passé formellement (6/7 cohortes
  à n fixé avec écart-type ≤ 0,10 — mais geo71729 à 0,292 montre que
  la variation à n fixé existe) ; (ii) **échoué** (résidu réel/nul
  ≤ 0,10 sur 53/106, 50 %, contre 90 % exigés — et identique à
  l'écart brut, puisque n se retranche) ; (iii) **échoué** (courbes
  HP35 réel/nul coïncidentes sur 2/8 tailles, contre ≥ 7/8 — avec un
  écart de 1,139 à k=285). **Verdict : NE SUFFIT PAS.**
- **Ce qui explique la non-séparation, en creux.** Trois faits
  convergent : (1) la loi en n vaut identiquement pour le réel et le
  nul (F1 Delta : réels seuls R²=0,620, β=[−3,07 ; 1,27] ; nuls seuls
  R²=0,576, β=[−3,35 ; 1,32]) ; (2) les courbes en n du réel et du nul
  diffèrent pourtant à n fixé (jusqu'à 1,14) ; (3) Delta à n fixé
  dépend du schéma de sous-échantillonnage (jusqu'à 1,74). Donc ce
  qui, en Delta, dépend de n est invariant par permutation — et ce qui
  diffère entre réel et nul ne dépend pas de n, mais de l'ordre des
  lignes et de leur contenu. Delta ne sépare pas le réel du nul parce
  que la partie ordonnée de l'information (celle que la permutation
  détruit) n'est pas dans n, et que la partie en n ne distingue pas
  les deux côtés. C'est le même verdict que les §8.39/§8.42/§8.57,
  atteint par une voie indépendante : Delta n'est pas élucidé, et sa
  non-séparation n'est pas un effet de taille d'échantillon.
- **La loi partielle trouvée ne sauve pas Delta.** Katz, Petrosian,
  Sevcik et GraphDimension ont leur loi en (ln n)² — un résultat
  positif, à consigner comme tel — mais d_sat, qui en dépendrait, n'a
  pas de loi (F2 B 0,614), et d_div non plus : la loi des membres bas
  ne se transmet pas aux médianes qui portent Delta. La voie « loi
  d'échelle en n » est close pour Delta.

## §8.62.7 Ce qui reste ouvert

1. **La forme analytique par estimateur.** La loi existe pour quatre
   estimateurs en (ln n)² (Katz, Petrosian, Sevcik, GraphDimension) et
   pour la saturation c'est 1/n qui domine en échantillon — une question
   pour la définition même des estimateurs (des dimensions fractales
   dont le biais en n est connu en théorie), pas un modèle de plus. La
   voie « loi d'échelle en n » est close pour Delta (§8.62.6) ; elle
   reste ouverte comme question analytique pour les estimateurs un par
   un, y compris DFA et ses extrêmes (−38,16), qui n'ont pas de loi
   (F2 R²=0,451 sur A, 0,318 sur B, transfert 0/31).
2. **La dispersion inter-flux de LevinaBickel** (§8.57.9 point 2) :
   inchangée — c'est elle qui fait basculer la paire sur les cas limites,
   et n n'y touche pas.
3. **d_sat.** Entièrement déterminée par la moitié des flux (222/222,
   §8.57) et la mieux expliquée par n (F4 R²=0,835) : son élucidation
   par n est la plus proche d'aboutir, mais elle ne sauve pas d_div —
   et Delta est porté par d_div (écart-type 1,18 contre 0,12 pour d_sat).

## Provenance (§8.62)

- **Demande et go :** chantier §8.62 du projet PDAC v6.2, 20 novembre
  2026 (voie ouverte au §8.42.9 point 2 et au §8.57.9 point 1).
  Protocole gelé avant toute modélisation et avant tout run :
  `PROTOCOL_delta_scaling_862.md`, SHA-256
  `8e67f8c7f17f92d297c5cbf02884e9a82778dd6c20fb8ee681afb3b24fb995b0`
  (correction consignée avant exécution : définition du stride, voir
  §8.62.2).
- **Pipeline :** v6.2 `universal_v6.2.0_cohen.py`,
  SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (vérifié avant travail et avant le lot B, jamais modifié) ; v6.1
  SHA-256 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` ;
  v6 SHA-256 `bb8bbdba…c0773`.
- **Données A (lecture seule) :** 222 `master_results.json`
  (156 v6.1 + 66 v6.2) dans `~/workspace/runs/pdac-v6/` ; base de cibles
  `v62_delta_levels.csv` ; 156 matrices de flux distinctes (9 cohortes,
  voir §8.62.2 et les `PROVENANCE_*.md` du dossier — et leurs nuls
  permutés, graine 42). Nature des lignes : sorties instrumentales du
  pipeline (médianes par estimateur) ; matrices de flux = mesures
  omiques publiques (TCGA, GEO, ICGC, CPTAC, DepMap, COAD, LUAD) ou
  série biophysique simulée (HP35) ; contrôles = noms de flux
  (étiquettes, mots humains) sauf `step`.
- **Données B :** 4 matrices sources (§8.62.2, SHA-256 :
  HP35 réel `6b656540…`, HP35 nul `ad669e51…`, LUAD `d407849b…`,
  TCGA v4 `e7a2adab…`) et leurs 31 sous-échantillons déterministes
  (préfixe/stride, SHA dans `v62_delta_scaling_862_manifest.json`).
  Lot B : lanceur `run_delta_scaling_862.sh` (unité systemd
  `delta-scaling-862`, tuée par un redémarrage machine le 20 nov.
  ~13h21 UTC au run 14) puis `run_delta_scaling_862_resume.sh`
  (unité `delta-scaling-862-resume`, 13 sorties valides conservées,
  18 runs relancés), journal `runs_delta_scaling_862.log` —
  **31/31 exit 0**, fin 14:15:23 UTC, SHA v6.2 final conforme.
- **Script et sorties :** `v62_delta_scaling_862.py`,
  `v62_delta_scaling_862.log`, `v62_delta_scaling_862_phaseA.json`,
  `v62_delta_scaling_862_phaseB.json`,
  `v62_delta_scaling_862_features.csv` (cibles, n, cohorte, résidu par
  run, 222 A + 31 B), `v62_delta_scaling_862_manifest.json` (SHA des
  31 CSV sous-échantillonnés).
- **Vérifications préalables :** identités d_div/d_sat 0 écart > 10⁻³
  sur 222/222 ; 0 écart n CSV vs n JSON ; 70 cibles manquantes, toutes
  LevinaBickel (41) ou PersistentHomology (29), c'est-à-dire le masque.
- **Limites déclarées :** dans A, n et cohorte sont presque parfaitement
  confondus (n constant intra-cohorte) ; B ne teste que 3 matrices
  sources et 1 nul ; le transfert A→B partage les matrices sources (il
  teste n, pas une matrice nouvelle) ; le préfixe confond longueur et
  segment (sensibilité stride sur 1 matrice, 3 tailles) ; aucune source
  entièrement nouvelle au-delà des 9 cohortes n'est testée ; le lot B
  tourne en concurrence avec d'autres lots sur la même machine
  (charge ~2–8, ~3–9 min par run ; un redémarrage machine a interrompu
  le lot initial au run 14 — reprise documentée, §8.62.5).
- Section rédigée dans `section_8.62_delta_scaling.md` (ce fichier) ;
  le livre blanc et le PDF ne sont pas régénérés dans ce chantier
  (coordinateur) ; rien n'est poussé sur GitHub dans ce chantier.

— Fin de la §8.62. —
