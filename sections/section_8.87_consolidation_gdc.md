# §8.87 — Consolidation de §8.85 : 10 nuls frais sur GDC ORGANOID-PANCREATIC — FRAGILE CONFIRMÉ (21 novembre 2026)

Piste 1 du lot du 21 nov. 2026 ; go de Zackary 21 nov. 2026 10h07 ;
protocole gelé 21 nov. 2026 ~10h09 EST avant toute construction et
tout run (`PROTOCOL_consolidation_gdc_887.md`, SHA
`956d5e44…aa30ed2`) ; provenance `PROVENANCE_887.md`. Cette section
exécute la piste ouverte du §8.85.9 (d) : combien de nuls frais
faut-il pour stabiliser le verdict d'une paire à n = 44 — et la
méthode est celle du §8.72, miroir exact, avec les catégories
renommées pour le sens de la consolidation (protocole §4.3).

## Verdict d'abord

**FRAGILE CONFIRMÉ — contre la distribution des 13 nuls, la
paire GDC ORGANOID-PANCREATIC ne passe PAS le plancher :
`d_médian = +0,0314` (réel 0,2542 contre nul médian 0,2229),
sous le seuil de consolidation 0,09 et sous le plancher 0,07
lui-même. Le réel est battu par 1 nul sur 13 (s8880, 0,2689 —
rang 13/14) et se situe SOUS le p95 des nuls (`d` contre p95 =
−0,0042). Seuls 2 écarts sur 13 dépassent le plancher — les
deux déjà connus du §8.85 (graine 42 et s8852) ; aucun des 10
nuls frais ne donne un écart au-dessus du plancher. La lecture
« fragile, non consolidé » du §8.85 n'était PAS un artefact du
tirage s8851 : elle tient contre le nul typique. Le verdict de
la paire graine 42 reste CONFIRME — règle gelée §8.85 §7,
l'histoire n'est pas réécrite — mais sa lecture est confirmée
fragile, et aucune note de correction n'est ajoutée au §8.85.**

| Porte (PROTOCOL_consolidation_gdc_887.md §4.3, gelé) | Exigé | Mesuré 21 nov. 2026 | Sort |
|---|---|---|---|
| `d_médian` (réel − médiane des 13 nuls) | > 0,09 CONSOLIDÉ ; 0,05–0,09 INCONCLUSIF ; < 0,05 FRAGILE CONFIRMÉ | **+0,0314** | **FRAGILE CONFIRMÉ** |
| Médiane 10 frais vs médiane 13 nuls | écart ≤ 0,03 | **+0,0047** | **cohérent** |
| Exactitude de l'extraction | 14/14 à 0,0 exact | **14/14, écart max 0,0** | **PASSE** |
| Relecture des valeurs §8.85 | 4/4 à 0,0 exact | **4/4, écart 0,0** | **PASSE** |
| Exits des 10 runs | 10 × 0 | **10 × 0, 0 échec** | **PASSE** |

**Ce que ce verdict dit, et ce qu'il ne dit pas.** Il dit que
la paire GDC ORGANOID-PANCREATIC, jugée non contre un tirage
unique mais contre la distribution de son nul, ne sépare pas
le réel du nul en `maxsep` au-dessus du plancher gelé — et
largement en dessous : +0,0314 contre 0,07 exigé, soit 0,45
fois le plancher. Il dit aussi que le §8.85 avait raison de
se dire fragile, et pour la raison inverse de celle qu'il
craignait : ce n'est pas le nul frais s8851 qui était un
tirage défavorable — c'est le nul graine 42 qui était un
tirage favorable, le deuxième plus bas des 13 nuls (0,1658 ;
seul s8852 est plus bas, 0,1606). Le passage du §8.85 tenait
au tirage le plus favorable possible, pas au pire. Il ne dit
pas que le verdict §8.85 est effacé : la paire graine 42
reste CONFIRME par règle gelée, et l'A2 étendu gelé (10/14,
paires graine 42) n'est PAS recompté ici — la confirmation
de fragilité est une correction de lecture, pas un
recomptage. Il ne dit pas non plus que `maxsep` échoue « en
général » : c'est une paire, à n = 44, sur une distribution
de 13 nuls — pas un plancher stable (le §8.53 estime ~200
nuls pour un plancher stable à petit n). Il dit, en substance,
que la quatorzième paire indépendante ne passe pas contre son
nul typique — et que c'est le miroir exact du §8.72, où la
dixième paire avait été renversée dans l'autre sens. L'adoption
pleine de `maxsep`, décidée par Zackary le 20 nov. 13h04,
n'est ni rouverte ni conditionnée ici : ce chantier est une
vérification a posteriori, comme le §8.85.

**Le fait nouveau, dit en tête.** Sur 3 nuls, le §8.85 voyait
une étendue de 0,0560 — plus grande que la marge de la paire
(+0,0184) — et concluait « fragile, non consolidé » sans
pouvoir trancher le sens de la fragilité. Sur 13 nuls, la
distribution est désormais décrite : médiane 0,2229, p95
0,2584, étendue 0,1083. Le réel (0,2542) est SOUS le p95 des
nuls — et même sous le p95 de 0,0042. Le plus grand écart parmi
les 10 frais est s8874 à +0,0693 — juste sous le plancher, à
0,0007 près. Les 10 écarts frais vont de −0,0147 à +0,0693 :
aucun ne passe. Ce n'est plus un
quasi-passage : c'est un non-passage contre le nul typique,
confirmé par 10 tirages sur 10.

Protocole gelé : `PROTOCOL_consolidation_gdc_887.md` (21 nov.
2026, SHA `956d5e44…aa30ed2` au gel, inchangé). Critère de
verdict écrit AVANT toute construction et tout run (§4.3 du
protocole) ; aucune repondération, aucun nouveau terme, aucune
redéfinition du plancher après avoir vu les chiffres. Les
nombres du §8.85 étaient la motivation, pas le verdict : le
verdict repose sur les 10 runs neufs mesurés ci-dessous, joints
aux 3 nuls anciens relus à 0,0 exact.

## 8.87.1 — La distribution des 13 nuls : le réel ne bat pas tout le monde

**Les 13 nuls, triés par `maxsep` croissant** (réel 0,2542 en
tête de liste, hors distribution) :

| Rang | Nul | `maxsep` nul | `d_maxsep` (réel − nul) | > 0,07 ? |
|---|---|---|---|---|
| 1 (min) | s8852 | 0,1606 | **+0,0936** | oui |
| 2 | **graine 42** | **0,1658** | **+0,0884** | **oui** |
| 3 | s8874 | 0,1849 | +0,0693 | non |
| 4 | s8873 | 0,1922 | +0,0620 | non |
| 5 | s8879 | 0,2082 | +0,0460 | non |
| 6 | s8851 | 0,2166 | +0,0376 | non |
| 7 (médiane) | **s8872** | **0,2229** | **+0,0314** | **non** |
| 8 | s8877 | 0,2234 | +0,0308 | non |
| 9 | s8876 | 0,2317 | +0,0225 | non |
| 10 | s8878 | 0,2363 | +0,0179 | non |
| 11 | s8875 | 0,2407 | +0,0135 | non |
| 12 | s8871 | 0,2514 | +0,0028 | non |
| 13 (max) | **s8880** | **0,2689** | **−0,0147** | **non** |

Valeurs exactes : réel `maxsep` 0,2542142849980612 ; médiane
des 13 nuls 0,22285393215883886 (le nul s8872) ; `d_médian` =
+0,03136035283922234. Écarts triés : −0,0147 / +0,0028 /
+0,0135 / +0,0179 / +0,0225 / +0,0308 / +0,0314 / +0,0376 /
+0,0460 / +0,0620 / +0,0693 / +0,0884 / +0,0936.

**Statistiques des distributions** (`numpy.percentile`,
interpolation linéaire — méthode gelée §4.1) :

| Statistique | 13 nuls (primaire) | 10 frais seuls (contrôle) |
|---|---|---|
| Médiane | **0,2229** | 0,2276 |
| p95 | **0,2584** | 0,2610 |
| Min / max | 0,1606 / 0,2689 | 0,1849 / 0,2689 |
| Étendue | **0,1083** | 0,0839 |
| Q1 / Q3 | 0,1922 / 0,2363 | 0,2119 / 0,2396 |
| IQR | 0,0441 | 0,0277 |
| Écart-type | 0,0324 | 0,0258 |

Valeurs exactes (13 nuls) : p95 0,2584172850921196 ; étendue
0,10828437033043026 ; IQR 0,044082176997452205 ; écart-type
0,03240960117213505. (10 frais) : médiane
0,2275605730536211 ; p95 0,2610337067888172 ; étendue
0,08394173327873244 ; IQR 0,02770760168339917 ; écart-type
0,02581882975755259.

**Lecture.** La médiane des 10 frais (0,2276) diffère de la
médiane totale (0,2229) de +0,0047 — très loin du seuil
d'alerte gelé (0,03) : les 3 anciens nuls ne tirent pas la
distribution. L'écart contre la médiane des 10 frais seuls
est +0,0267 — identique à `d_médian` (+0,0314) à 0,0047 près :
le verdict ne dépend pas de l'inclusion des 3 anciens nuls.
Le nul graine 42 (0,1658) est le deuxième plus bas des 13 —
il ne dépasse que s8852 (0,1606) de 0,0052 et se situe sous le
Q1 (0,1922) : c'est un tirage de queue basse, pas un nul
typique. Le nul médian (s8872, 0,2229) donne un écart de
+0,0314 — le verdict ne tient donc plus à un tirage : 11
tirages sur 13 sont sous le plancher, et le réel est sous le
p95 des nuls de 0,0042. À l'inverse du §8.72, où l'écart
médian (+0,1447) dépassait l'étendue des nuls (0,1110),
l'écart médian (+0,0314) est ici trois fois plus petit que
l'étendue des 13 nuls (0,1083) et que celle des 10 frais
(0,0839) : le signal est plus petit que la dispersion du nul.
Le rang du réel est 13/14 : un nul le bat (s8880, 0,2689, soit
+0,0147 au-dessus du réel).

**Lot.** Pipeline `universal_v6.2.0_cohen.py`, SHA
`f07567c4…c3abf`, revérifié inchangé avant ET après le lot ;
mode fast ; 10 runs, exits 0 × 10, 0 échec, 0 déjà fait.
Lancement en `systemd-run` (unité `v62-887`), surveillance
`watch_v62_887.sh` (arrêtée d'elle-même à 10/10,
`WATCH 887 TERMINE 10/10`, tour 2) ; journal
`runs_v62_887.log` (SHA du pipeline en tête, FIN
15h41:40Z, déjà faits 0, terminés 10, échecs 0). Durée du lot :
15h09:50Z → 15h41:40Z (~32 min, durées allongées par la
contention CPU — d'autres lots v6.2 tournaient en parallèle
sur la VM partagée). Aucun redémarrage de machine pendant le
lot, aucune relance, aucun dossier supprimé. Le livre blanc
n'est PAS édité, le PDF N'EST PAS régénéré, rien n'est poussé
sur GitHub dans ce chantier.

## 8.87.2 — Ce que la confirmation de fragilité dit, et ce qu'elle ne dit pas

**Ce qui est confirmé.** La lecture du §8.85, pas son verdict.
Le §8.85 disait, sur la paire graine 42 : CONFIRME, +0,0884,
au-dessus du plancher — et il disait aussi que ce verdict
était fragile, parce qu'un nul frais sur deux passait sous le
plancher. La présente section confirme la fragilité dans le
sens exact où le §8.85 la craignait, et plus fort encore : le
verdict tenait au tirage, et le tirage gelé était le deuxième
plus favorable des 13. Contre le nul typique, la paire ne
passe pas — et elle ne passe pas nettement (+0,0314, soit
0,45 fois le plancher). Aucune note de correction n'est
ajoutée au §8.85 : la lecture y était déjà la bonne, et le
protocole §4.3 ne prévoit d'addendum qu'en cas de
CONSOLIDÉ — ce qui n'est pas le cas ici.

**Ce qui n'est pas confirmé.** Le verdict de la paire graine
42 reste CONFIRME : la règle gelée §8.85 §7 l'interdit de
changer, et ce chantier la respecte — l'histoire n'est pas
réécrite, elle est complétée. L'A2 étendu gelé reste 10/14
(12/14 positifs, LOO 9/13) : les 14 paires comptées gardent
leurs valeurs, et la quatorzième garde sa valeur de paire
graine 42 (+0,0884). Le protocole §4.3 l'a gelé ainsi : la
confirmation de fragilité est une correction de lecture, pas
un recomptage.

**C3, dite plainement.** C3 RESTE LEVÉE — elle l'était déjà
depuis le §8.71, et ce chantier est une consolidation
supplémentaire, pas une condition ; il ne rouvre rien, dans
aucun sens. En substance, en revanche, la quatorzième paire
indépendante ne passe pas contre son nul typique (+0,0314) :
c'est ce que le §8.85 craignait sans pouvoir le mesurer sur
3 tirages, mesuré ici sur 13. Les deux faits coexistent et
sont dits tels quels : C3 levée au sens gelé, confirmation de
fragilité de substance mesurée. Trancher entre les deux
lectures — retirer la paire du compte A2 sur la base de la
distribution, ou la garder comme paire graine 42 — est une
décision de Zackary et du coordinateur, pas de ce chantier.
Ce chantier mesure ; il ne recompte pas et ne lève ni ne
rétablit aucune condition.

**Le miroir du §8.72, dit en une phrase.** Au §8.72, le nul
graine 42 était le PLUS HAUT des 13 nuls et le verdict
PARTIEL avait été renversé ; ici, le nul graine 42 est le
deuxième PLUS BAS des 13 nuls et le verdict CONFIRME fragile
est confirmé fragile. Les deux chantiers disent la même chose
sur l'instrument à petit n : à n = 44–51, un seul tirage de
nul décide presque à lui seul si une paire passe ou non — et
c'est mesuré dans les deux sens, pas supposé.

**Ce que la confirmation ne prouve pas.** Elle ne prouve pas
que `maxsep` échoue « en général » : c'est une paire, à
n = 44, sur une distribution de 13 nuls — pas un plancher
stable (le §8.53 estime ~200 nuls pour un plancher stable à
petit n). Elle ne prouve pas que le nul graine 42 était un
« mauvais » tirage au sens d'une erreur : c'est un tirage
légitime de la même distribution, simplement un tirage de
queue basse (sous le Q1). Elle ne change rien à l'adoption
pleine : elle a été décidée par Zackary le 20 nov. 13h04, et
ce chantier la consolide par son honnêteté, comme le §8.85
l'avait fait par la sienne.

## 8.87.3 — Contrôles descriptifs (à publier, ne décident pas)

**Ancien MC : positif contre le nul médian, pas contre tous
les nuls.** Réel 0,3880 ; nuls médiane 0,3843, min 0,3731,
max 0,3911 ; `d_MC` contre le nul médian +0,0037. Un nul
frais (s8880, MC 0,3911) bat le réel en MC — comme au §8.85,
où le MC était déjà minuscule (+0,0113) contre graine 42. Le
MC ne porte pas la séparation ici : c'est `maxsep` qui la
porte, et le critère gelé est `maxsep` seul.

**S_sep : même histoire que `maxsep`.** Réel 0,2496 ; nuls
médiane 0,2207 ; `d_Ssep` contre le nul médian +0,0289 —
du même ordre que `d_médian` (+0,0314), comme au §8.85 où
S_sep (+0,0847) suivait `maxsep` (+0,0884). Le même nul
frais s8880 bat le réel en S_sep (0,2667 contre 0,2496).

**Delta : écart positif contre le nul médian, mais un nul
bat le réel.** Réel 1,468 ; nuls médiane 1,149, min 0,706,
max 1,433 — un nul frais (s8872, 1,433) est à 0,035 du réel
sans le dépasser ; aucun nul ne dépasse le réel en Delta,
mais l'étendue des nuls (0,727) est plus de deux fois
l'écart réel–médiane (+0,318). Delta ne distingue pas le
réel du nul sur cette paire de façon stable, comme au §8.85.

**L7a : UP presque partout.** Réel UP 0,3372. Sur les 13
nuls : 12 UP, 1 DOWN (s8874 0,1731 — confiance faible,
~0,17, contre ~0,33–0,38 pour les UP). Descriptif : L7a
n'est pas le critère gelé, et il ne distingue pas les séries
ici — 12 nuls sont UP comme le réel.

**L7b : FRAGILE sur les 14 runs** — même non-informativité
que partout (réel + 13 nuls). **Falsification :
indisponible** (n = 44 < 75, règle du projet) — valeurs
brutes rapportées à titre descriptif seulement, sans statut
de test : réel 1,51771, nuls 1,40983–1,80160, tous au-dessus
du seuil 0,5 du JSON.

**Cascades : formes instables, comme au §8.85.** Réel
[41,0 / 72,5 / 79,4 / 84,0 / 95,4] (pas 18/31/34/36/41).
Nuls frais à Q5 : de 22,5 % (s8871) à 99,1 % (s8876) — la
forme de la cascade nulle n'est pas une caractéristique
stable à n = 44 : elle mesure le tirage, elle ne distingue
pas les séries. Aucune rupture visible qui distinguerait le
réel des 13 nuls à la fois — la séparation est dans le score
`maxsep`, pas dans la forme de la cascade. Le nul s8876
atteint 86,3 % dès Q2 (pas 37) et 99,1 % en Q5 : à n = 44,
un nul peut monter plus haut que le réel.

**Régimes.** Réel `criticality` ; nuls : `criticality` pour
graine 42, s8872 et s8880, `saturation` pour les 10 autres —
descriptif, pas un verdict.

## 8.87.4 — Ce que ça change, et ce que ça ne change pas

| Poste | Change ? | Détail |
|---|---|---|
| Lecture du §8.85 (« fragile, non consolidé ») | **Oui — CONFIRMÉE** | Contre le nul médian, la paire ne passe pas (+0,0314). Aucune note de correction au §8.85 : la lecture y était déjà la bonne. |
| Verdict de la paire graine 42 (§8.85) | **Non — reste CONFIRME** | Règle gelée §8.85 §7. L'histoire n'est pas réécrite. |
| A2 étendu gelé (paires graine 42) | **Non — reste 10/14, 12/14 positifs, LOO 9/13** | Pas de recomptage (protocole §4.3). |
| Condition C3 (§8.59.8, sens gelé) | **Non — RESTE LEVÉE** | Levée depuis le §8.71 ; ce chantier est une consolidation supplémentaire, pas une condition. |
| Adoption pleine de `maxsep` | **Non — décidée par Zackary le 20 nov. 13h04** | Ce chantier est une vérification a posteriori, pas une condition. |
| Score MC affiché (convention §8.64.6) | Non | `maxsep` principal, ancien MC secondaire, `sep` compagnon, mention de fragilité — inchangée. |
| Sélection du best_config, seuil MC, cascade, S_sep, Delta, L7a | Non | Inchangés par construction. |
| Code v6.2 / v6.1 / v6 | Non | Aucune modification, aucune v6.5. |
| Verdicts des §8.56, §8.59, §8.64, §8.69, §8.70, §8.72, §8.85 | Non | Confirmés, pas rouverts ; les 14 paires comptées gardent leurs valeurs. |
| Pistes ouvertes | Oui, une de plus | (a) La question « combien de nuls faut-il pour un plancher stable à n ≈ 44 ? » (§8.85.9 (d), §8.53) reste ouverte : 13 nuls décrivent la distribution, ils ne stabilisent pas un plancher — ~200 nuls seraient nécessaires ; (b) la paire GDC est désormais la seule paire passante en graine 42 dont la distribution dit « fragile confirmé » — à comparer aux autres paires passantes si elles sont consolidées de la même façon : le compte A2 en paires graine 42 surestime-t-il la robustesse des paires à petit n ? (c) si Zackary veut trancher le statut de la paire dans A2, la voie est soit une décision sur la base de la distribution mesurée ici, soit une quinzième paire indépendante avec son propre protocole gelé. |

**Suite du dossier.** Si Zackary veut une nouvelle paire
indépendante : un chantier ultérieur, avec son propre
protocole gelé, sur une autre cohorte vérifiée indépendante —
pas une relecture, pas un re-test déguisé, et pas GDC
ORGANOID-PANCREATIC (mesurée, consolidée par distribution).
Si Zackary décide de retirer la paire du compte A2 sur la
base de la distribution : la présente section fournit les
chiffres, et le retrait est consigné par le coordinateur avec
sa date et sa décision — pas par ce chantier. Dans les deux
cas, le PDF et GitHub sont régénérés et poussés par le
coordinateur (règle permanente « Toujours github et pdf !!! »),
avec la présente section fusionnée.

## 8.87.5 — Limites et ce qui reste

- 13 nuls ne font pas un plancher stable : §8.53 estime ~200
  nuls pour un plancher stable à petit n. La médiane de 13
  nuls porte ~±0,02 — d'où la bande d'inconclusivité gelée
  (±0,02 autour du plancher). Ici `d_médian` (+0,0314) est
  sous la bande (0,05) : le verdict FRAGILE CONFIRMÉ ne tient
  pas à la bande. Mais la queue de la distribution (p95) reste
  estimée sur 13 tirages seulement.
- Le nul est une permutation par lignes (corrélations
  inter-flux préservées) : la distribution mesurée est celle
  du nul du projet, pas d'un nul à corrélations brisées
  (même réserve qu'au §8.53 §8).
- Le nul graine 42 est un tirage légitime, pas une erreur :
  il est sous le Q1, mais il appartient à la distribution. La
  confirmation de fragilité dit que le verdict §8.85 tenait à
  ce tirage — elle ne dit pas que ce tirage était invalide.
- Une seule paire a été consolidée : le verdict porte sur
  elle, pas sur « `maxsep` en général ».
- La paire est construite sur des TPM GDC (`tpm_unstranded`,
  §8.85.1) : la nature des valeurs est nommée comme limite,
  pas corrigée après coup — comme au §8.85.
- Delta ne diverge pas ici (+0,32 contre le nul médian) :
  la divergence du §8.69 (+2,01 contre −0,01) n'est ni
  confirmée ni infirmée comme phénomène — une seule paire
  de plus, dans l'autre sens. L7b est FRAGILE sur les 14 runs
  — non-informatif, comme partout.
- Rien de clinique : l'étude porte sur l'instrument.

## 8.87.6 — Provenance

- Protocole gelé : `PROTOCOL_consolidation_gdc_887.md`, SHA-256
  `956d5e447f0aad67a937f6bbd75c711960d94e75696b004b580f0cd69aa30ed2`
  (au gel, avant construction et runs ; fichier inchangé
  depuis).
- Provenance complète : `PROVENANCE_887.md` (ce chantier).
- Provenance de la cohorte et des données : `PROVENANCE_885.md`,
  SHA-256
  `fe26f4e0d2b5de30f9f666ccfedda07e1cfa5386905abba71823e53f66869f2b`
  (GDC ORGANOID-PANCREATIC, 55 TSV, manifeste SHA
  `f713edebf…6220b`, 44 fichiers Tumor, MUCL3 ex-DPCR1 —
  relus, rien re-téléchargé).
- Construction : `build_nulls_887.py`, SHA-256
  `4da79e8a912b62634e96ed3a2f2a4ef681c0ef5e4b2587b2c4bfa4ec2be61e05`
  (graines gelées 8871–8880 ; CSV réel relu sans être réécrit,
  SHA vérifié inchangé après chaque graine).
- Flux : `pdac_885_gdc_organoid_fluxes.csv` (44 lignes), SHA-256
  `a83b98175bdbc33525ba8a175aa898504d2cc44125b891d0902c6c6c26345eaf`
  (inchangé) ; nuls frais
  `pdac_885_gdc_organoid_fluxes_nul_s8871.csv` …
  `pdac_885_gdc_organoid_fluxes_nul_s8880.csv`, SHA consignés dans
  `nulls_887_files.json`, SHA-256
  `7703708b79018d833479fa4528bc4f3c85e01876baff8cdb085c387d40bbe360`
  (s8871 `4ad645ca…`, s8872 `7888cdfd…`, s8873 `804571d7…`,
  s8874 `605ae022…`, s8875 `2e74c5a0…`, s8876 `ec2ca1a7…`,
  s8877 `64e1eb43…`, s8878 `7f46f581…`, s8879 `5460483f…`,
  s8880 `449eff62…`).
- Runs : manifeste `manifest_v62_887.txt`, SHA-256
  `d013077a1d01686c7730adcb6f027e872babb5a81237c6f8a93df38582c70913` ;
  journal `runs_v62_887.log`, SHA-256
  `b9a0e84a1af568297c8e917c6bee90de339195ddbd404949e5c736e64247a698` ;
  surveillance `watch_v62_887.sh`, SHA-256
  `b3cdffb1eb32b6e539041567a2b790692946293e2fc04a0b1a87f7a2ef5f44e0` ;
  dossiers `results_fast_v62_887_gdc_organoid_nul_s8871` … `s8880`
  (10 runs, exits 0 × 10, 35 fichiers chacun — sans
  `csd_consensus.png`, comme au §8.85).
- Extraction : `extract_887.py`, SHA-256
  `1f608c82ee58400b59f039ac2d0207237daf1f0abaa54875009116281c98f57c`
  → `extract_887.json`, SHA-256
  `ca66461a50df41ec38e8cd3001e2fb6377b461c687d7902a98baa404a4cb5e74` /
  `extract_887.csv`, SHA-256
  `5dfad9318d743cdf1d32083b5f2bb0465fdf420f38d009ff6f97e9471e7a7b5b` /
  `dist_887.json`, SHA-256
  `aacd01c3e99554c3e6b8861a88c590602892ef9ea01d19256d818b5880cc28fd`.
- Vérification indépendante : `verify_887.py`, SHA-256
  `b173c3733d4a5141d7ade7daeb6dec3992874054b328c7e2222ec3695f3298af`
  → `maxsep_887_verify.json`, SHA-256
  `9926c87de071ce4fddbdd14648e76c5d6bb727e28393737b841d12a6186cb381`
  (14/14 comparaisons, écart max 0,0 exact, verdict OK).
- Valeurs §8.85 relues : `extract_885.json` (réel
  0,2542142849980612 ; nuls 0,1657676706638558 /
  0,2165939226122164 / 0,1605986015484797 — relecture à 0,0
  exact dans `extract_887.py`).
- Codes jamais modifiés : v6.2 (`f07567c4…c3abf`, revérifié
  avant ET après le lot), v6.1 (`2af5e5ce…c1c9`), v6
  (`bb8bbdba…c0773`). Aucune nouvelle version construite dans
  ce chantier — pas de v6.5. Dix runs du pipeline lancés dans
  ce chantier (10 nuls frais, exits 0 × 10) ; aucun run réel
  relancé ; aucun push GitHub, aucune Release dans ce chantier.
- Section : `section_8.87_consolidation_gdc.md` (ce fichier ;
  SHA noté au rapport).
- Données : série réelle = TPM GDC (`tpm_unstranded`, mesures
  instrumentales du fournisseur, symboles extraits
  mécaniquement, ordre par KRAS). Nuls = lignes permutées,
  graines 42 / 8851 / 8852 / 8871–8880 — échantillons
  hypothétiques, pas des mesures. Aucune valeur inventée ;
  aucune valeur recopiée à la main (tables générées depuis
  `extract_887.json` et `dist_887.json`, vérifiées à 0,0 exact
  par `verify_887.py`).

— Fin de la §8.87. —

---

## 8.87.7 — Note de fin de chantier (pour le coordinateur)

- Livre blanc NON édité, PDF NON régénéré, rien poussé sur
  GitHub (convention des chantiers ; fusion par le
  coordinateur).
- Titre à normaliser à la fusion : « ### 8.87 Consolidation
  de §8.85 : 10 nuls frais sur GDC ORGANOID-PANCREATIC —
  FRAGILE CONFIRMÉ (21 novembre 2026) ».
- Entrée de journal à ajouter : §8.87, protocole gelé
  ~10h09 EST, 10/10 runs exit 0, FRAGILE CONFIRMÉ
  (d_médian +0,0314 ; rang 13/14 ; 2/13 écarts au-dessus du
  plancher), A2 gelé inchangé 10/14, C3 reste levée.
- Aucune note de correction au §8.85 : la catégorie gelée
  FRAGILE CONFIRMÉ ne prévoit pas d'addendum (la lecture du
  §8.85 était déjà la bonne).
