# Elucidation Delta — PROTOCOL_v6.2.md §4 (H1–H7)

Ensemble : **222 runs** (156 v6.1 + 66 v6.2), lecture seule dans les `master_results.json`, script `extract_delta_levels.py`, log `v62_delta_extract.log`, donnees brutes `v62_delta_levels.csv` / `.json`. Aucun run du pipeline, aucune modification du pipeline.

## Verdict §4.4 — NON ELUCIDE

Meilleure variable : **H1+H2+H3 (masque, MFA, n)** — identite de la paire mediane predite sur 80.2 %, valeur de d_div a ±0,10 pres sur 61.7 %. Le critere exige ≥ 90 % sur les deux. **Delta reste non elucide** : son 6/8 en phase 2 reste une piste fragile, et Delta ne devient PAS un discriminateur recommande.

## Ce qui est verifie (identites de construction, 222/222)

- d_div = moyenne des 3e et 4e medianes divergence triees : 222/222 (0 ecart).
- d_sat = 4e mediane saturation triee : 222/222 (0 ecart).
- d_div prend 133 valeurs distinctes (a 10⁻³) sur 222 runs — ce ne sont pas « quelques niveaux fixes » au sens brut ; les « niveaux » sont des grappes.
- MFA : 9 valeurs distinctes : [3.0, 4.0, 4.5, 5.0, 6.0, 6.25, 6.5, 6.75, 7.0].
- Masques fini/absent (LevinaBickel / PersistentHomology) : {'LP': 181, '-P': 12, '--': 29}.
- Paires medianes (3e+4e divergence) : {'LocalPCA+LevinaBickel': 31, 'LocalPCA+MFA': 99, 'LocalPCA': 7, 'MFA': 5, 'MFA+LocalPCA': 30, 'LocalPCA+PCAIntrinsic': 46, 'PCAIntrinsic+LocalPCA': 4}.

## H1–H7 : taux de prediction (paire mediane / valeur de d_div a ±0,10)

Methode : pour chaque variable candidate, la paire predite est la paire majoritaire dans le groupe, la valeur predite est la moyenne de d_div du groupe (lecture honnete). La reconstruction par les valeurs memes de la paire est une identite de construction (H6), pas une prediction.

| Hypothese | Variable | Paires predites | Valeur ±0,10 | Groupes | n |
|---|---|---|---|---|---|
| H1 — composition finie (masque L/P) | H1 masque (L/P) | 60.8 % | 14.9 % | 3 | 222 |
| H1b — Levina seule | H1b masque Levina seule | 57.7 % | 14.9 % | 2 | 222 |
| H1c — PersistentHomology seule | H1c masque PH seule | 57.7 % | 13.5 % | 2 | 222 |
| H2 — MFA discret | H2 MFA | 62.2 % | 36.0 % | 9 | 222 |
| H3 — n (taille d'echantillon) | H3 n | 63.1 % | 56.3 % | 11 | 222 |
| H3b — n_fluxes (mode) | H3b n_fluxes_mode | 46.8 % | 8.1 % | 4 | 222 |
| H3c — (n, n_fluxes) | H3c (n, n_fluxes_mode) | 63.1 % | 56.3 % | 12 | 222 |
| H5 — controle | H5 controle | 68.0 % | 32.9 % | 53 | 222 |
| H5b — (controle, masque) | H5b (controle, masque) | 74.3 % | 36.5 % | 56 | 222 |
| H1+H2 — (masque, MFA) | H1+H2 (masque, MFA) | 74.3 % | 51.4 % | 11 | 222 |
| H2+H3 — (MFA, n) | H2+H3 (MFA, n) | 78.4 % | 59.9 % | 19 | 222 |
| H1+H3 — (masque, n) | H1+H3 (masque, n) | 64.9 % | 58.1 % | 13 | 222 |
| H1+H2+H3 — (masque, MFA, n) | H1+H2+H3 (masque, MFA, n) | 80.2 % | 61.7 % | 21 | 222 |

Lecture par hypothese :
- **H1 (composition finie)** : le masque seul ne predit la paire qu'a 60,8 % et la valeur a 14,9 %. La composition finie change le rang median (5 ou 4 valeurs au lieu de 6), mais elle ne determine pas la paire.
- **H2 (MFA discret)** : 62,2 % / 36,0 %. MFA est quasi discret (9 valeurs) et tres correle a d_div (Pearson +0,968), mais sa valeur seule ne dit pas quelle paire est mediane.
- **H3 (n)** : 63,1 % / 56,3 %. n predit la grappe mais pas monotonement (voir H7) ; n_fluxes seul est presque inutile (46,8 % / 8,1 %).
- **H4 (largeur du pic / robustness)** : correlation Pearson (robustness, d_div) = 0.19742680275709168 — faible, confirmee sur 222 runs. Les quartiles de robustness melangent toutes les paires (Q1 : 4 paires differentes, Q4 : 6 paires). H4 infirmee comme predicteur seul.
  - Q1 robustness [7.95e-50, 3.37e-41] n=78 : {'LocalPCA+LevinaBickel': 14, 'LocalPCA+MFA': 35, 'LocalPCA+PCAIntrinsic': 27, 'PCAIntrinsic+LocalPCA': 2}
  - Q2 robustness [3.37e-41, 2.59e-19] n=98 : {'LocalPCA+LevinaBickel': 18, 'LocalPCA': 4, 'LocalPCA+MFA': 56, 'LocalPCA+PCAIntrinsic': 20}
  - Q3 robustness [2.59e-19, 4.63e-06] n=56 : {'MFA': 4, 'MFA+LocalPCA': 20, 'LocalPCA': 3, 'LocalPCA+MFA': 19, 'LocalPCA+LevinaBickel': 5, 'LocalPCA+PCAIntrinsic': 5}
  - Q4 robustness [4.63e-06, 9.99e-01] n=57 : {'MFA+LocalPCA': 10, 'MFA': 1, 'LocalPCA+MFA': 21, 'LocalPCA+PCAIntrinsic': 14, 'LocalPCA+LevinaBickel': 9, 'PCAIntrinsic+LocalPCA': 2}
- **H5 (controle)** : 68,0 % / 32,9 % seul ; 74,3 % / 36,5 % avec le masque. Le controle deplace la paire, sans la determiner.
- **H6 (paire mediane)** : mecanisme exact confirme — d_div est entierement determine par l'identite des 3e/4e estimateurs et leurs valeurs (reconstruction a ±0,10 sur 222/222). C'est une identite de construction, pas une prediction : il reste a predire la paire.
- **H7 (d_sat quasi constant)** : d_sat est la mediane DFA ou Hurst2mH selon la famille (voir table par n). Delta ≈ d_div − constante par famille, mais la constante change avec n.

## Correlations avec d_div (Pearson, 222 runs)

- LevinaBickel : 0.8070059323802591
- PCAIntrinsic : 0.7076143107283076
- LocalPCA : 0.9679780540299259
- GraphDimension : 0.8636384949787402
- PersistentHomology : 0.7961604197339519
- MFA : 0.967754291731523
- robustness : 0.19742680275709168
- sharpness : 0.2267540255417084
- max_sep : 0.18712112263836916
- stability : 0.03069998144640139

LocalPCA (+0,968) et MFA (+0,968) suivent d_div de tres pres — normal : ce sont presque toujours eux qui forment la paire mediane (LocalPCA+MFA : 99 runs, LocalPCA+PCAIntrinsic : 46, LocalPCA+LevinaBickel : 31). Une correlation n'est pas une prediction de la paire : savoir que LocalPCA bouge avec d_div ne dit pas quand il est 3e ou 4e, ni avec qui.

## H7 — d_sat par taille d'echantillon

| n | runs | d_sat (moyenne ± ecart-type) | 4e membre dominant |
|---|---|---|---|
| 45 | 30 | 1.240 ± 0.078 | ('Katz', 22), ('Hurst2mH', 8) |
| 52 | 4 | 1.464 ± 0.018 | ('DFA', 2), ('Hurst2mH', 2) |
| 63 | 4 | 1.413 ± 0.014 | ('DFA', 4) |
| 69 | 14 | 1.482 ± 0.028 | ('DFA', 14) |
| 70 | 10 | 1.483 ± 0.055 | ('DFA', 5), ('Hurst2mH', 5) |
| 145 | 20 | 1.568 ± 0.032 | ('Hurst2mH', 12), ('DFA', 8) |
| 177 | 2 | 1.586 ± 0.008 | ('Hurst2mH', 1), ('DFA', 1) |
| 178 | 124 | 1.580 ± 0.022 | ('Hurst2mH', 98), ('DFA', 24) |
| 285 | 4 | 1.633 ± 0.001 | ('DFA', 4) |
| 515 | 4 | 1.652 ± 0.005 | ('DFA', 4) |
| 1000 | 6 | 1.589 ± 0.053 | ('DFA', 6) |

## Anomalie DFA = −38,16 — retrouvee, sans effet sur d_sat

**22 runs avec DFA < −10** (dont le −38,1597 de `results_fast_v61_depmaprot_aco2_nul`, celui du protocole §4.2). Sur les 22, DFA est toujours la 1re valeur triee (la plus basse) de la saturation — jamais la 4e, donc jamais la mediane : d_sat vaut alors Katz (~1,19) et Delta n'est pas touche. Exemples : DepMap v6.2 (rep1 et rep2, identiques) DFA = −18,5768, d_sat = 1,1900 (4e = Katz), Delta = 1,9338. Les DFA extremes se concentrent sur DepMap et ses rotations proteines (n=45) : une mediane d'estimateur extreme isolee sur petites series, pas une rupture de d_sat.

## Conclusion

**Delta n'est pas elucide.** La meilleure combinaison nommee (masque + MFA + n) predit la paire mediane a 80,2 % et la valeur a 61,7 % — loin des 90 % exiges, meme sur les seuls runs v6.2 (86,4 % / 78,8 %, n=66). Le mecanisme est connu (moyenne des 3e/4e medianes divergence), mais ce qui choisit la paire reste en partie indetermine : ni le masque, ni MFA, ni n, ni le controle, ni la robustness, ni leurs combinaisons ne suffisent. Delta garde son statut de piste fragile (6/8 en phase 2, 13/23 en annexe, echec sur HP35) et ne devient pas un discriminateur recommande.

Donnees brutes : `v62_delta_levels.csv`, `v62_delta_levels.json`, `v62_delta_extract.log`.
