### 8.95 Le score composite v6.5 — REJETÉE : une seule porte échouée suffit, et c'est la paire DepMap qui tombe (21 novembre 2026)

**Verdict d'abord, en trois phrases. (a) REJETÉE — le score composite
C_pair = (maxsep_R − maxsep_N) + 0,50×(MC_R − MC_N) + 0,50×(robustness_R
− robustness_N) + 0,25×(L7a_R − L7a_N) ne passe pas les quatre portes
gelées du protocole : C1 rotations 31/48 — PASSE (barre 30/48) ; C2
principales 5/8 au-dessus du plancher 0,07 et 8/8 positifs — ÉCHOUE
(barre 6/8 et 7/8) ; C3 HP35 C = +1,8012 — PASSE (barre 0,30) ; C4
relecture indépendante — PASSE (0,0 exact sur 120/120 runs, tous les
recoupements à 1e-9, SHAs des versions inchangés). Une seule porte
échouée suffit — comme pour v6.3 et v6.4 — donc le composite est
REJETÉ, et le score principal affiché reste maxsep seul, MC secondaire.
(b) Attribution précise : le composite ne perd qu'une seule paire
principale par rapport à maxsep seul, et c'est DepMap — d_maxsep
+0,1904, mais d_l7a −0,5409, donc C = +0,0292, sous le plancher ; les
deux autres paires perdues (GSE71729 C +0,0584, GSE62452 C +0,0295)
échouent déjà sous maxsep seul. Le composite est strictement
INFÉRIEUR à maxsep seul sur les deux compteurs : V1 5/8 contre 6/8,
V2 31/48 contre 37/48. (c) Sensibilités : sans le terme L7a, V1 passe
à 6/8 et V2 à 32/48 — c'est le terme L7a qui coûte la porte C2 ; sans
le terme robustesse, V1 reste à 5/8 et V2 monte à 34/48 ; plancher
0,05 → V1 6/8, V2 34/48 ; plancher 0,10 → V1 5/8, V2 30/48. Le terme
robustesse punit surtout les rotations PARP (d_rob −0,81 à −0,99 sur
ATM, ATR, PARP2, MUC16) même quand maxsep est positif : la robustesse
n'est pas un allié du composite ici. La copie v6.5 existe, construite
et vérifiée, mais son adoption reste à Zackary — et sur ces chiffres,
elle n'est pas recommandée.**

**Application de la correction de Zackary du 21 novembre 2026 à cette
piste (texte complet en tête de §8.93).** (1) Contrôle jamais analysé :
V2 (48 rotations) utilise les fichiers DEDUP du §8.44 — le flux
d'ordre est la première colonne (contrôle) et N'EST PAS parmi les flux
analysés, vérifié sur les 48 fichiers (0 colonne `.1`, 0 doublon) ;
V1 et descriptifs : contrôle `step`, PROLIF, MTAPCN ou `score_acineux`,
jamais un flux analysé. Le défaut connu des 96 fichiers de rotations
d'origine (§8.32 — `CEACAM5` en contrôle ET `CEACAM5.1` parmi les flux
analysés) n'est PAS utilisé ici ; ces fichiers restent sur le disque
comme témoins du défaut. Le composite V2 (31/48) est donc mesuré sur
les mêmes fichiers propres que le 37/48 de maxsep seul — comparaison à
base identique. (2) Aucun seuil écarté au motif de non-monotonie.
(3) Tous les verdicts de cette section sont formulés comme de
l'analyse : le REJET du composite décrit ce que les 60 paires
détenues montrent, il ne prédit pas sa performance ailleurs.**

## 8.95.1 Question, méthode, règles

**Question.** §8.56 a montré que maxsep seul sépare 37/48 rotations et
6/8 paires principales, mieux que MC (12/48, 5/8) et mieux que v6.3
(31/48) et v6.4 (28/48). Le composite v6.5 était la piste gelée pour
faire mieux que maxsep seul en additionnant les signaux : maxsep, MC,
robustesse et L7a signé, avec les poids 1 / 0,50 / 0,50 / 0,25 — poids
gelés dans le protocole, pas ajustés après coup. Question posée : le
composite bat-il maxsep seul sur les mêmes barres que §8.56 ?

**Méthode.** Protocole gelé `PROTOCOL_composite_v65_895.md` (SHA
`f3fcb38ef1d6ce68a14369ccd2a2baa62520fe124641ff8c411eb87692c66ece`,
écrit avant tout calcul). Rescore des 60 paires §8.56 depuis les
`master_results.json` détenus, AUCUN run : 8 paires principales (V1),
48 rotations (V2), 4 paires descriptives (hors portes). L7a signé =
±`global_confidence` (up +, down −, sinon 0 — même convention que
§8.44). La copie v6.5 est construite par diff minimal depuis v6.2
(§8.95.4), jamais en touchant l'original.

**Barres gelées (C1–C4 = A1–A4 du §8.56).** C1 rotations ≥ 30/48 ;
C2 principales ≥ 6/8 au-dessus du plancher 0,07 ET ≥ 7/8 positifs ;
C3 HP35 ≥ 0,30 ; C4 relecture indépendante : re-extraction 0,0 exact
sur 120/120 runs, recoupements à 1e-9, SHAs inchangés. Une seule
porte échouée suffit au rejet, comme pour v6.3 et v6.4.

## 8.95.2 Résultats — les quatre portes

| Porte | Barre gelée | Mesuré | Verdict |
|---|---|---|---|
| C1 rotations (V2, 48) | ≥ 30/48 | **31/48** (38/48 positifs, 10 négatifs, somme +13,4370) | PASSE |
| C2 principales (V1, 8) | ≥ 6/8 et ≥ 7/8 positifs | **5/8** au-dessus du plancher, 8/8 positifs | **ÉCHOUE** |
| C3 HP35 | ≥ 0,30 | **+1,8012** | PASSE |
| C4 relecture indépendante | 0,0 exact, 1e-9, SHAs inchangés | 120/120 exact, tous les recoupements à 1e-9, SHAs inchangés | PASSE |

**V1 — les 8 paires principales (détail).** C = d_maxsep + 0,50×d_MC
+ 0,50×d_rob + 0,25×d_l7a, plancher 0,07 :

| Paire | C | d_maxsep | d_MC | d_rob | d_l7a | Porte |
|---|---|---|---|---|---|---|
| HP35 | **+1,8012** | +1,6512 | +0,0129 | +0,2540 | +0,0982 | oui |
| TCGA v4 | **+0,1723** | +0,2928 | −0,0270 | −0,1772 | −0,0735 | oui |
| GSE71729 | +0,0584 | +0,0402 | −0,0131 | +0,0519 | −0,0160 | non |
| GSE62452 | +0,0295 | −0,0036 | −0,0186 | +0,0922 | +0,0000 | non |
| ICGC | **+0,2372** | +0,0970 | +0,0108 | +0,1273 | +0,2373 | oui |
| IMMUNE TCGA | **+0,2631** | +0,3675 | −0,0281 | +0,0505 | −0,3024 | oui |
| PARP TCGA | **+0,1260** | +0,1688 | −0,0326 | −0,0000 | +0,1275 | oui |
| DEPMAP | +0,0292 | +0,1904 | −0,0244 | −0,0000 | **−0,5409** | non |

**Lecture de V1.** Seule DepMap bascule par rapport à maxsep seul :
maxsep seul la classe oui (+0,1904), le composite la classe non
(+0,0292) — le terme L7a à −0,5409 (L7a réel down, nul up, écart
0,54 de confiance) coûte 0,1352 de C, plus que la marge. GSE71729
et GSE62452 sont perdues sous les deux scores : elles ne distinguent
pas le composite, elles confirment que ces deux paires ne séparent
pas. Somme V1 +2,7168, moyenne +0,3396.

**V2 — les 48 rotations.** 31/48 au-dessus du plancher, 38/48
positifs, 10 négatifs, somme +13,4370. Par famille : IMMROT 11/12
(12/12 positifs, somme +7,6500), V4ROT 9/12 (9/12 positifs, somme
+3,4528), PARPROT 7/12 (8/12 positifs, somme +1,3902), DEPMAPROT
4/12 (9/12 positifs, somme +0,9440). Les 17 paires sous le plancher :
DEPMAPROT ACO2 +0,0231, CCND1 −0,1045, CFLAR +0,0560, CRKL +0,0399,
MYC +0,0100, MYH9 −0,0160, RAB10 +0,0644, UROD −0,0278 ;
IMMROT CD19 +0,0641 ; PARPROT ATM −0,3871, ATR −0,2765, PARP1
−0,1253, PARP2 −0,5387, XRCC1 +0,0414 ; V4ROT CR2 −0,0968,
GSTM1 −0,0839, MUC16 −0,4826. Les échecs PARPROT et V4ROT-MUC16
sont dominés par d_rob : ATM −0,8494, ATR −0,8080, PARP2 −0,9898,
MUC16 −0,8309 — la robustesse réelle s'effondre sous ces contrôles
alors que maxsep reste positif (+0,1638, +0,2381, +0,0203, +0,0703).
La robustesse, en tant que terme du composite, punit des paires que
maxsep seul classe correctement.

## 8.95.3 Sensibilités — ce qui aide, ce qui coûte

| Variante | V1 (plancher 0,07) | V2 (plancher 0,07) | Lecture |
|---|---|---|---|
| Composite complet (gelé) | 5/8 | 31/48 | référence |
| Sans le terme L7a | **6/8** | 32/48 | le terme L7a coûte la porte C2 |
| Sans le terme robustesse | 5/8 | **34/48** | la robustesse coûte 3 rotations |
| Plancher 0,05 | 6/8 | 34/48 | le plancher 0,07 n'est pas le seul coupable |
| Plancher 0,10 | 5/8 | 30/48 | à 0,10, C1 passe tout juste |

Sans L7a, V1 passe à 6/8 — exactement le niveau de maxsep seul —
et V2 à 32/48, toujours sous les 37/48 de maxsep seul. Aucune
variante testée n'atteint maxsep seul sur V2. Le composite n'améliore
rien ; il redistribue les pertes.

## 8.95.4 La copie v6.5 — construite, vérifiée, non adoptée

Copie `universal_v6.5.0_cohen.py`, SHA
`983ec65dc607a2ca8445bed095e5d86b3e6560534c7e7ecf9eda587fb6420bf6`
(script `build_v65.py`, SHA
`18eaa1e8cf1284fd34e926871e3727e3b99d385219b8e27ec09d1b91da2871c4`).
Diff vs v6.2 = exactement 3 hunks, 70 lignes : (1) fonction pure
`composite_c65_run` après `evaluate_scan_quality` ; (2) site d'appel
avant `final_output` ; (3) `VERSION_MASTER` →
`v6.5.0-L7aL7b-CohenD-short` + commentaire. 1 seule ligne supprimée.
`py_compile` OK. SHA de v6.2 vérifié identique avant et après les
travaux (f07567c4…). L'adoption finale reste à Zackary ; sur ces
chiffres, la recommandation est de NE PAS adopter — le composite est
rejeté comme score principal, et il ne remplace pas la batterie
entière (règle §8.90.1.2 : maxsep est le score principal AFFICHÉ,
pas le verdict).

## 8.95.5 Paires descriptives — hors portes, rapportées

Test A (prolifération, §8.34) : C +0,0084 — quasi nul, attendu pour
un NON, pas d'anomalie. MTAP_PRMT5FLUX : C −0,1118 ; MTAP_SERIES :
C −0,5637 — la contradiction S_sep/MC du §8.40 persiste sous le
composite (le composite ne l'arbitre pas). V4R_PURITY : C +0,5188 —
le candidat bouge avec la composition, cohérent avec §8.51–§8.54.

## 8.95.6 Ce qui est établi, ce qui ne l'est pas

**Établi.** (1) Le composite gelé est rejeté sur C2, par une seule
paire (DepMap) perdue à cause du terme L7a. (2) Le composite est
strictement inférieur à maxsep seul sur V1 (5/8 contre 6/8) et V2
(31/48 contre 37/48) — il ne faut pas l'adopter. (3) Le terme
robustesse punit les rotations PARP même quand maxsep est positif :
la robustesse n'est pas un allié du composite. (4) La relecture
indépendante est parfaite (0,0 exact sur 120/120) : le rejet est un
verdict sur le score, pas un artefact d'extraction.

**Non établi.** (1) Aucune autre pondération n'a été testée — les
poids étaient gelés, et les repondérer après coup serait du
surajustement. (2) Le composite n'a pas été testé sur les paires
§8.93 (distributions de nuls) ni sur les bras §8.96 — ce n'est pas
son rôle : il est rejeté. (3) Le mécanisme de l'écart L7a DepMap
(d_l7a −0,5409) n'est pas élucidé ici — il est consigné, pas
expliqué. (4) Les 48 rotations V2 sont les fichiers DEDUP propres du
§8.44 (flux d'ordre = contrôle, jamais analysé) ; les 96 fichiers
d'origine §8.32, avec le doublon `X.1`, ne sont pas utilisés ici —
ils sont traités au §8.97, partie 1.

## 8.95.7 Provenance

Protocole gelé `PROTOCOL_composite_v65_895.md` (SHA
`f3fcb38ef1d6ce68a14369ccd2a2baa62520fe124641ff8c411eb87692c66ece`) ;
provenance `PROVENANCE_895.md` (SHA
`e32f47d917f5e6dc6ee939ef5faa5f428c531d2de8908622a2cfce66a91fd1ba`).
Extraction `extract_c65.py` (SHA
`c60ab9928a0b31b5d1c7112dfb6088b6e7bd825c8895c8cb54a41c8fec03220d`) ;
vérification indépendante `extract_c65_verify.py` (SHA
`a7f79b6dcb43d72d38fe863081f51d8f95b5ebc641b8a51596e4bd9072121950`) ;
table `c65_table.json` (SHA
`769e8653ad302c7d78e476d4a7205d8745728e6d6b809e8e00f8a0b7f07d56b8`) ;
`c65_table.csv` (SHA
`238a0e054322d416c74aec4114ebc1b99cb4e2112f91272dd8b81aaec36a37c4`) ;
vérification `c65_verify.json` (SHA
`ff8d0f358c7fab85759fb6c209c3e437e00b91ab221e0f4cbfadd5ae2eda8f26`).
Paires et listes reprises de `extract_sep_maxsep_856.py` (§8.56) ;
recoupements à 1e-9 contre `ssep_844_rotations.csv`,
`v62_phase2_table.csv`, `v63_mc_table.json`, `v64_mc_table.json`,
`sep_maxsep_856_table.json` ; ancien MC recoupé à 1e-9 contre §8.44 et
phase 2. Versions : v6.2 SHA `f07567c4…` (travail), v6.1 SHA
`2af5e5ce…` (référence), v6 SHA `bb8bbdba…`, v6.3 SHA
`3f5e1a5c…`, v6.4 SHA `a9d8c2f1…` — tous inchangés avant et après.
Aucun run pipeline. Aucune recommandation clinique.
