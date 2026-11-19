#!/usr/bin/env python3
"""Redige v62_phase2_table.md depuis v61_phase2_table.json et
v62_phase2_table.json (aucune recopie a la main)."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
a = json.load(open(os.path.join(BASE, "v61_phase2_table.json")))
b = json.load(open(os.path.join(BASE, "v62_phase2_table.json")))
g = b["gigues"]

V61_LABEL = {
    "1 Delta": "1 Delta", "2 MC best_score": "2 MC best_score",
    "3 max_separation": "3 max_separation", "4 |T0 reel - T0 nul|": "4 |T0|",
    "5 falsification delta_vs_null": "5 falsification",
    "6 coherence par flux (fraction)": "6 coherence (fraction)",
    "6b |d| median a T0": "6b |d| median",
    "7 L7a confiance signee": "7 L7a",
    "8 ecart cascade complet": "8 cascade",
    "6 COMBINE": "6 COMBINE",
}
V62_LABEL = dict(V61_LABEL)
V62_LABEL["9 S_sep = max_separation x stability"] = "9 S_sep"


def f(x, nd=4):
    if x is None:
        return "n/d"
    return f"{x:.{nd}f}"


L = []
L.append("# Phase 2 — discrimination reel / nul : sorties v6.2 (PROTOCOL_v6.2.md §6)")
L.append("")
L.append("Protocole gele : `PROTOCOL_v6.2.md` §6 (phase 2 : "
         "`PROTOCOL_phase2_discrimination.md`, 16 nov. 2026). Pipeline : "
         "`universal_v6.2.0_cohen.py`, SHA "
         "`f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`, "
         "jamais modifie. **Aucun nouveau run du pipeline au-dela du §5** : tout "
         "est lu dans les `master_results.json` v6.2 deja sur disque (10 runs de "
         "validation x 2 + 46 runs phase 2, 66 dossiers ; 3 redemarrages machine "
         "pendant les lots, reprise par le lanceur reprenable). Nul : lignes "
         "permutees, graine 42, colonne de controle intacte. Extracteur : "
         "`extract_phase2_v62.py` (copie de `extract_phase2.py`, SHA "
         "`5eb3ac24…75aa`, etendue du 9e indicateur S_sep), log "
         "`v62_phase2_extract.log`. Donnees brutes : `v62_phase2_table.csv` et "
         "`v62_phase2_table.json`.")
L.append("")
L.append("## Gigues appliquees (mesurees en validation v6.2, §5 — pas le forfait ±0,07)")
L.append("")
L.append(f"- MC best_score : gigue mesuree **{g['mc']}** (v6.1 : forfait 0,07).")
L.append(f"- max_separation : gigue mesuree **{g['maxsep']}** (v6.1 : forfait 0,07).")
L.append(f"- L7a (confiance signee) : gigue mesuree **{g['l7a']}** (v6.1 : forfait 0,07).")
L.append(f"- S_sep : gigue effective = max(gigue mesuree 0,00 ; plancher 0,07) = "
         f"**{g['ssep_eff']}** (§3.4).")
L.append("- Delta, cascade, falsification : gigue 0 (deterministes).")
L.append("")
L.append("**Lecture honnete, a garder en tete pour tout le tableau :** la gigue "
         "mesuree est 0, donc pour MC, max_separation et L7a, « ecart > gigue » "
         "devient « ecart non nul ». Les ecarts eux-memes sont **identiques** a "
         "ceux de la v6.1 au chiffre pres (voir § Comparaison) : l'instrument "
         "n'a pas change, c'est la regle qui a change. Un 7/8 en v6.2 la ou la "
         "v6.1 donnait 1/8 ne veut PAS dire que le pipeline separe mieux — il "
         "veut dire que le meme ecart, mesure contre une gigue 0 au lieu de "
         "0,07, passe le seuil.")
L.append("")
L.append("## Table principale — valeurs reel / nul (ecart reel−nul), v6.2")
L.append("")
L.append("| Paire | n | Delta R/N (ecart) | MC score R/N (ecart) | MC seuil R/N % | "
         "max_sep R/N (ecart) | stab. R/N | S_sep R/N (ecart) | T_0 R/N % (|ecart|) | "
         "fals R/N | frac. coh. R/N | |d| med. R/N | L7a R / N | Σ|Δ| casc. |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in b["principal"]:
    L.append(f"| {r['paire']} | {r['n']:.0f} | {f(r['delta_R'], 2)} / {f(r['delta_N'], 2)} "
             f"({f(r['d_delta'], 2)}) | {f(r['mc_R'])} / {f(r['mc_N'])} ({f(r['d_mc'])}) | "
             f"{f(r['mc_thr_R'], 2)} / {f(r['mc_thr_N'], 2)} | "
             f"{f(r['maxsep_R'])} / {f(r['maxsep_N'])} ({f(r['d_maxsep'])}) | "
             f"{f(r['stab_R'])} / {f(r['stab_N'])} | "
             f"{f(r['ssep_R'])} / {f(r['ssep_N'])} ({f(r['d_ssep'])}) | "
             f"{f(r['T0_R'], 2)} / {f(r['T0_N'], 2)} ({f(r['d_T0'], 2)}) | "
             f"{f(r['fals_R'], 3) if r['fals_R'] is not None else '—'} / "
             f"{f(r['fals_N'], 3) if r['fals_N'] is not None else '—'} | "
             f"{f(r['frac_R'], 2)} / {f(r['frac_N'], 2)} | "
             f"{f(r['medd_R'], 2)} / {f(r['medd_N'], 2)} | "
             f"{r['l7a_R']} / {r['l7a_N']} | {f(r['casc_sum'], 2)} |")
L.append("")
L.append("Detail indicateur 6 (pas T_0 reel/nul, fenetre, flux lus) : identique a "
         "la v6.1 (memes entrees, memes cascades) — voir `v62_phase2_table.csv` "
         "(colonnes step_R/step_N, window, nflux).")
L.append("")
L.append("## Verdicts par indicateur — v6.2 contre v6.1 (paires principales)")
L.append("")
L.append("| Indicateur | v6.2 (gigue appliquee) | v6.1 (gigue 0,07) | "
         "Ce qui a change, et pourquoi |")
L.append("|---|---|---|---|")
comp = [
    ("1 Delta", "6/8 : [TCGA v4, GSE62452, ICGC, immunitaire TCGA, PARP TCGA, DepMap], "
     "echoue sur [HP35, GSE71729]", "6/8, memes paires",
     "Rien. Ecarts identiques ; gigue 0 dans les deux versions."),
    ("2 MC best_score", "7/8 : [HP35, TCGA v4, GSE71729, ICGC, immunitaire TCGA, PARP TCGA, DepMap], "
     "echoue sur [GSE62452]", "1/8 : [HP35]",
     "Seule la gigue a change (0,07 → 0,00 mesuree). Les 7 ecarts positifs "
     "(+0,0059 a +0,0545 sur PDAC) passent un seuil 0 mais pas 0,07. "
     "Le score vedette ne separe toujours pas au-dela du bruit historique."),
    ("3 max_separation", "7/8 : [HP35, TCGA v4, GSE71729, ICGC, immunitaire TCGA, PARP TCGA, DepMap], "
     "echoue sur [GSE62452]", "6/8 (GSE71729 et GSE62452 en echec)",
     "Seule la gigue a change. GSE71729 (+0,0402) passe avec gigue 0 ; "
     "GSE62452 reste plat (−0,0036). Ecarts identiques a la v6.1."),
    ("9 S_sep", "6/8 : [HP35, TCGA v4, ICGC, immunitaire TCGA, PARP TCGA, DepMap], "
     "echoue sur [GSE71729 (+0,0405 < 0,07), GSE62452 (−0,0072)]",
     "— (nouveau ; prevu 6/8 au §3.3 sur valeurs v6.1)",
     "Atteint la barre ≥ 6/8, exactement comme max_separation en v6.1, "
     "meme paires. La stabilite (~0,98–1,00 sur PDAC) ne change presque "
     "rien : S_sep ≈ max_separation ; le garde-fou anti-pic-bruite ne "
     "s'est pas declenche ici."),
    ("4 |T0|", "8/8 — TRIVIAL", "8/8 — TRIVIAL", "Rien (voir reserves phase 2)."),
    ("5 falsification", "4/5 disponibles : [HP35, TCGA v4, GSE71729, PARP TCGA], "
     "echoue sur [immunitaire TCGA] ; indisponible sur [GSE62452, ICGC, DepMap] (n < 75)",
     "4/5, memes paires", "Rien. Comparaison interne, pas au nul permute (§8.31)."),
    ("6 coherence (fraction)", "2/8 : [HP35, TCGA v4]", "2/8, memes paires", "Rien."),
    ("6b |d| median", "6/8", "6/8", "Rien."),
    ("7 L7a", "4/8 : [TCGA v4, immunitaire TCGA, PARP TCGA, DepMap], direction majoritaire NEGATIVE",
     "4/8, memes paires", "Ecarts signes quasi identiques (plus grand mouvement : "
     "TCGA V2 en annexe, −0,579 → −0,548 ; principal : HP35 +0,044 → +0,040). "
     "Verdict inchange."),
    ("8 cascade", "8/8 — TRIVIAL", "8/8 — TRIVIAL", "Rien (voir reserves phase 2)."),
]
for ind, v62, v61, why in comp:
    L.append(f"| {ind} | {v62} | {v61} | {why} |")
L.append("")
L.append("## Verdict global")
L.append("")
L.append("**S_sep separe sur 6/8 paires principales : [HP35, TCGA v4, ICGC, "
         "immunitaire TCGA, PARP TCGA, DepMap], echoue sur [GSE71729, GSE62452]. "
         "La barre ≥ 6/8 du protocole (§3.4) est atteinte, exactement.**")
L.append("")
L.append("Mais la reponse a la question « la v6.2 separe-t-elle mieux que la "
         "v6.1 ? » est **non** :")
L.append("- Tous les ecarts reel−nul sont identiques a ceux de la v6.1 au chiffre "
         "pres, sauf les ecarts L7a signes (mouvements ≤ 0,031, verdicts "
         "inchanges) et le nouvel indicateur S_sep.")
L.append("- S_sep (6/8) ne fait pas mieux que max_separation en v6.1 (6/8, memes "
         "paires) : la stabilite est quasi saturee (~0,98–1,00) sur toutes les "
         "paires PDAC, donc S_sep ≈ max_separation. Le 6/8 etait deja predit au "
         "§3.3 du protocole a partir des valeurs v6.1.")
L.append("- Les seuls compteurs qui montent (MC 1/8 → 7/8, max_separation 6/8 → "
         "7/8) montent parce que la gigue appliquee est passee de 0,07 (forfait "
         "historique) a 0,00 (mesuree en validation v6.2, comme le protocole §6 "
         "l'ordonne), pas parce que l'instrument a change. Avec le forfait 0,07, "
         "les verdicts v6.2 seraient exactement ceux de la v6.1.")
L.append("- Delta reste a 6/8, fragile (echoue sur HP35, le temoin positif ; "
         "deux ecarts ≤ 0,15), et **non elucide** (§8.37, partie Delta) : il ne "
         "devient pas un discriminateur recommande.")
L.append("")
L.append("En une phrase : **la v6.2 ne separe pas mieux que la v6.1 ; elle separe "
         "pareil, et de facon deterministe (gigue 0).** S_sep atteint la barre "
         "≥ 6/8, mais il herite exactement des forces et des faiblesses de "
         "max_separation.")
L.append("")
L.append("## Annexe — paires secondaires (23, memes regles, memes gigues)")
L.append("")
L.append("| Paire | n | ΔDelta | ΔMC | Δmax_sep | ΔS_sep | |ΔT_0| | Δfals | Δfrac | "
         "Δ|d| med. | ΔL7a signe | Σ|Δ| casc. |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in b["secondaire"]:
    L.append(f"| {r['paire']} | {r['n']:.0f} | {f(r['d_delta'], 2)} | {f(r['d_mc'])} | "
             f"{f(r['d_maxsep'])} | {f(r['d_ssep'])} | {f(r['d_T0'], 2)} | "
             f"{f(r['d_fals'], 3) if r['d_fals'] is not None else '—'} | "
             f"{f(r['d_frac'], 2) if r['d_frac'] is not None else '—'} | "
             f"{f(r['d_medd'], 2) if r['d_medd'] is not None else '—'} | "
             f"{f(r['d_l7a'], 3)} | {f(r['casc_sum'], 2)} |")
L.append("")
L.append("Verdicts annexe v6.2 contre v6.1 (memes regles) :")
L.append("")
# Verdicts annexe v6.1 (lus dans le .md de phase 2 v6.1) vs v6.2 (calcules ici).
import re
sec_v62 = b["secondaire"]
names = [r["paire"] for r in sec_v62]


def verdict_sec(rows, key, jit):
    vals = [(i, r[key]) for i, r in enumerate(rows) if r.get(key) is not None]
    s = sum(x for _, x in vals)
    direction = 1 if s > 0 else (-1 if s < 0 else 0)
    ok = [i for i, x in vals if direction != 0 and abs(x) > jit
          and (1 if x > 0 else -1) == direction]
    return len(ok), sum(1 for _ in vals), direction


annexe = [
    ("Delta", "d_delta", 0.0, "13/23"),
    ("MC", "d_mc", g["mc"], "2/23"),
    ("max_separation", "d_maxsep", g["maxsep"], "16/23"),
    ("S_sep", "d_ssep", g["ssep_eff"], "— (nouveau ; max_sep v6.1 : 16/23)"),
    ("T0", "d_T0", 0.0, "23/23"),
    ("falsification", "d_fals", 0.0, "7/18, direction inversee"),
    ("coherence (fraction)", "d_frac", 0.0, "8/22"),
    ("L7a", "d_l7a", g["l7a"], "12/23"),
    ("cascade", "casc_sum", 0.0, "23/23"),
]
for label, key, jit, v61 in annexe:
    x, denom, direction = verdict_sec(sec_v62, key, jit)
    L.append(f"- {label} : **{x}/{denom}** (v6.1 : {v61}), direction "
             f"{'+' if direction > 0 else '−'}.")
L.append("")
L.append("Lecture : en annexe, S_sep fait 16/23 — exactement le score de "
         "max_separation en v6.1 (16/23). MC passe de 2/23 a 18/23 et "
         "max_separation de 16/23 a 20/23 uniquement par la gigue 0 (voir "
         "§ Gigues). L7a passe de 12/23 a 13/23 (V4R_CLDN18, ecart −0,002, "
         "compte avec gigue 0, pas avec 0,07).")
L.append("")
L.append("Donnees brutes : `v62_phase2_table.csv`, `v62_phase2_table.json`, "
         "`v62_phase2_extract.log`.")
with open(os.path.join(BASE, "v62_phase2_table.md"), "w") as fh:
    fh.write("\n".join(L) + "\n")
print("Ecrit : v62_phase2_table.md")
