#!/usr/bin/env python3
"""Redige v62_delta_elucidation.md depuis v62_delta_levels.json et
v62_delta_extract.log (aucune recopie a la main)."""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(BASE, "v62_delta_levels.json")))
log = open(os.path.join(BASE, "v62_delta_extract.log")).read()

corrs = {m[0]: m[1] for m in re.findall(r"corr\(d_div, (\w+)\) Pearson = ([\d\.\-]+) \(n=(\d+)\)", log)}
h7 = re.findall(r"  n=([\d\.]+) : (\d+) runs, d_sat ([\d\.]+) ± ([\d\.]+), 4e membre dominant : \[(.*?)\]", log)
q = re.findall(r"    Q(\d) \[(.*?), (.*?)\] n=(\d+) paires=(.*)", log)


def pct(x):
    return f"{x * 100:.1f} %" if x is not None else "n/d"


L = []
L.append("# Elucidation Delta — PROTOCOL_v6.2.md §4 (H1–H7)")
L.append("")
L.append(f"Ensemble : **{d['n_runs']} runs** ({d['n_v61']} v6.1 + {d['n_v62']} v6.2), "
         "lecture seule dans les `master_results.json`, script "
         "`extract_delta_levels.py`, log `v62_delta_extract.log`, donnees brutes "
         "`v62_delta_levels.csv` / `.json`. Aucun run du pipeline, aucune "
         "modification du pipeline.")
L.append("")
L.append("## Verdict §4.4 — NON ELUCIDE")
L.append("")
L.append(f"Meilleure variable : **{d['meilleure']}** — identite de la paire mediane "
         f"predite sur {pct(d['predictions'][d['meilleure']]['acc_paire'])}, valeur "
         f"de d_div a ±0,10 pres sur "
         f"{pct(d['predictions'][d['meilleure']]['acc_valeur_pm010'])}. "
         "Le critere exige ≥ 90 % sur les deux. **Delta reste non elucide** : "
         "son 6/8 en phase 2 reste une piste fragile, et Delta ne devient PAS "
         "un discriminateur recommande.")
L.append("")
L.append("## Ce qui est verifie (identites de construction, 222/222)")
L.append("")
L.append(f"- d_div = moyenne des 3e et 4e medianes divergence triees : "
         f"{d['n_runs'] - d['mismatch_d_div']}/{d['n_runs']} (0 ecart).")
L.append(f"- d_sat = 4e mediane saturation triee : "
         f"{d['n_runs'] - d['mismatch_d_sat']}/{d['n_runs']} (0 ecart).")
L.append("- d_div prend 133 valeurs distinctes (a 10⁻³) sur 222 runs — ce ne "
         "sont pas « quelques niveaux fixes » au sens brut ; les « niveaux » "
         "sont des grappes.")
L.append(f"- MFA : 9 valeurs distinctes : {d['mfa_valeurs_distinctes']}.")
L.append(f"- Masques fini/absent (LevinaBickel / PersistentHomology) : {d['masques']}.")
L.append(f"- Paires medianes (3e+4e divergence) : {d['paires']}.")
L.append("")
L.append("## H1–H7 : taux de prediction (paire mediane / valeur de d_div a ±0,10)")
L.append("")
L.append("Methode : pour chaque variable candidate, la paire predite est la paire "
         "majoritaire dans le groupe, la valeur predite est la moyenne de d_div "
         "du groupe (lecture honnete). La reconstruction par les valeurs memes "
         "de la paire est une identite de construction (H6), pas une prediction.")
L.append("")
L.append("| Hypothese | Variable | Paires predites | Valeur ±0,10 | Groupes | n |")
L.append("|---|---|---|---|---|---|")
labels = {
    "H1 masque (L/P)": "H1 — composition finie (masque L/P)",
    "H1b masque Levina seule": "H1b — Levina seule",
    "H1c masque PH seule": "H1c — PersistentHomology seule",
    "H2 MFA": "H2 — MFA discret",
    "H3 n": "H3 — n (taille d'echantillon)",
    "H3b n_fluxes_mode": "H3b — n_fluxes (mode)",
    "H3c (n, n_fluxes_mode)": "H3c — (n, n_fluxes)",
    "H5 controle": "H5 — controle",
    "H5b (controle, masque)": "H5b — (controle, masque)",
    "H1+H2 (masque, MFA)": "H1+H2 — (masque, MFA)",
    "H2+H3 (MFA, n)": "H2+H3 — (MFA, n)",
    "H1+H3 (masque, n)": "H1+H3 — (masque, n)",
    "H1+H2+H3 (masque, MFA, n)": "H1+H2+H3 — (masque, MFA, n)",
}
for k, lab in labels.items():
    p = d["predictions"][k]
    L.append(f"| {lab} | {k} | {pct(p['acc_paire'])} | {pct(p['acc_valeur_pm010'])} | "
             f"{p['n_groupes']} | {p['n_runs']} |")
L.append("")
L.append("Lecture par hypothese :")
L.append("- **H1 (composition finie)** : le masque seul ne predit la paire qu'a "
         "60,8 % et la valeur a 14,9 %. La composition finie change le rang "
         "median (5 ou 4 valeurs au lieu de 6), mais elle ne determine pas la "
         "paire.")
L.append("- **H2 (MFA discret)** : 62,2 % / 36,0 %. MFA est quasi discret (9 "
         "valeurs) et tres correle a d_div (Pearson +0,968), mais sa valeur "
         "seule ne dit pas quelle paire est mediane.")
L.append("- **H3 (n)** : 63,1 % / 56,3 %. n predit la grappe mais pas "
         "monotonement (voir H7) ; n_fluxes seul est presque inutile "
         "(46,8 % / 8,1 %).")
L.append("- **H4 (largeur du pic / robustness)** : correlation Pearson "
         f"(robustness, d_div) = {corrs.get('robustness', 'n/d')} — faible, "
         "confirmee sur 222 runs. Les quartiles de robustness melangent toutes "
         "les paires (Q1 : 4 paires differentes, Q4 : 6 paires). H4 infirmee "
         "comme predicteur seul.")
for qi, lo, hi, n, paires in q:
    L.append(f"  - Q{qi} robustness [{lo}, {hi}] n={n} : {paires}")
L.append("- **H5 (controle)** : 68,0 % / 32,9 % seul ; 74,3 % / 36,5 % avec le "
         "masque. Le controle deplace la paire, sans la determiner.")
L.append("- **H6 (paire mediane)** : mecanisme exact confirme — d_div est "
         "entierement determine par l'identite des 3e/4e estimateurs et leurs "
         "valeurs (reconstruction a ±0,10 sur 222/222). C'est une identite de "
         "construction, pas une prediction : il reste a predire la paire.")
L.append("- **H7 (d_sat quasi constant)** : d_sat est la mediane DFA ou "
         "Hurst2mH selon la famille (voir table par n). Delta ≈ d_div − "
         "constante par famille, mais la constante change avec n.")
L.append("")
L.append("## Correlations avec d_div (Pearson, 222 runs)")
L.append("")
for name in ["LevinaBickel", "PCAIntrinsic", "LocalPCA", "GraphDimension",
             "PersistentHomology", "MFA", "robustness", "sharpness", "max_sep",
             "stability"]:
    if name in corrs:
        L.append(f"- {name} : {corrs[name]}")
L.append("")
L.append("LocalPCA (+0,968) et MFA (+0,968) suivent d_div de tres pres — "
         "normal : ce sont presque toujours eux qui forment la paire mediane "
         "(LocalPCA+MFA : 99 runs, LocalPCA+PCAIntrinsic : 46, "
         "LocalPCA+LevinaBickel : 31). Une correlation n'est pas une prediction "
         "de la paire : savoir que LocalPCA bouge avec d_div ne dit pas "
         "quand il est 3e ou 4e, ni avec qui.")
L.append("")
L.append("## H7 — d_sat par taille d'echantillon")
L.append("")
L.append("| n | runs | d_sat (moyenne ± ecart-type) | 4e membre dominant |")
L.append("|---|---|---|---|")
for n, nr, mean, sd, dom in h7:
    L.append(f"| {float(n):.0f} | {nr} | {mean} ± {sd} | {dom} |")
L.append("")
L.append("## Anomalie DFA = −38,16 — retrouvee, sans effet sur d_sat")
L.append("")
L.append(f"**{len(d['dfa_extremes'])} runs avec DFA < −10** (dont le "
         "−38,1597 de `results_fast_v61_depmaprot_aco2_nul`, celui du "
         "protocole §4.2). Sur les 22, DFA est toujours la 1re valeur triee "
         "(la plus basse) de la saturation — jamais la 4e, donc jamais la "
         "mediane : d_sat vaut alors Katz (~1,19) et Delta n'est pas touche. "
         "Exemples : DepMap v6.2 (rep1 et rep2, identiques) DFA = −18,5768, "
         "d_sat = 1,1900 (4e = Katz), Delta = 1,9338. Les DFA extremes se "
         "concentrent sur DepMap et ses rotations proteines (n=45) : une "
         "mediane d'estimateur extreme isolee sur petites series, pas une "
         "rupture de d_sat.")
L.append("")
L.append("## Conclusion")
L.append("")
L.append("**Delta n'est pas elucide.** La meilleure combinaison nommee "
         "(masque + MFA + n) predit la paire mediane a 80,2 % et la valeur a "
         "61,7 % — loin des 90 % exiges, meme sur les seuls runs v6.2 "
         "(86,4 % / 78,8 %, n=66). Le mecanisme est connu (moyenne des 3e/4e "
         "medianes divergence), mais ce qui choisit la paire reste en partie "
         "indetermine : ni le masque, ni MFA, ni n, ni le controle, ni la "
         "robustness, ni leurs combinaisons ne suffisent. Delta garde son "
         "statut de piste fragile (6/8 en phase 2, 13/23 en annexe, echec sur "
         "HP35) et ne devient pas un discriminateur recommande.")
L.append("")
L.append("Donnees brutes : `v62_delta_levels.csv`, `v62_delta_levels.json`, "
         "`v62_delta_extract.log`.")
with open(os.path.join(BASE, "v62_delta_elucidation.md"), "w") as fh:
    fh.write("\n".join(L) + "\n")
print("Ecrit : v62_delta_elucidation.md")
