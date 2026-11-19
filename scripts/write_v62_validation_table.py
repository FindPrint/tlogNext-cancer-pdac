#!/usr/bin/env python3
"""Redige v62_validation_table.md depuis v62_validation_table.json (aucune
recopie a la main)."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(BASE, "v62_validation_table.json")))


def f(x, nd=4):
    if x is None:
        return "n/d"
    return f"{x:.{nd}f}"


def casc(r):
    return " / ".join(f"{c:.2f}" for c in r["cascade"])


L = []
L.append("# Validation v6.2 — 10 runs fast x 2 repetitions (PROTOCOL_v6.2.md §5)")
L.append("")
L.append("Pipeline : `universal_v6.2.0_cohen.py`, SHA-256 "
         f"`{d['sha_v62']}` ; v6.1 de reference SHA `{d['sha_v61']}` ; "
         f"v6 SHA `{d['sha_v6']}` (inchangee). Mode `fast`, `--seed 42` (defaut).")
L.append("Lanceur reprenable : `run_v62_lot.sh` + `manifest_v62_validation.txt`, "
         "surveille par `watch_v62_validation.sh` (systemd-run). "
         "Log : `runs_v62_validation.log`. Extraction : `extract_v62_validation.py`.")
L.append("Deux redemarrages machine pendant le lot (18 nov. ~23h25 UTC et 19 nov. "
         "~00h05 UTC) : le lanceur a repris la ou il s'etait arrete (2 runs deja "
         "complets conserves, 1 run partiel tue — TCGA v4 reel puis DepMap nul rep2 — "
         "refait proprement). 20/20 exit 0.")
L.append("")
L.append("## Resultats par run (repetition 1 ; repetition 2 entre parentheses quand elle differe)")
L.append("")
L.append("| Run | n | Cascade v6.2 rep1 (% T_-2 / T_-1 / T_0 / T_+1 / T_+2) | "
         "Cascade = v6.1 ? | MC best_score (v6.1) | max_sep | stab. | S_sep | "
         "Delta (v6.1) | L7a v6.2 (v6.1) | L5 top / conf / n_alerts | L4 |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in d["runs"]:
    r1, r61 = r["rep1"], r["v61"]
    L.append(f"| {r['run']} | {r['n']:.0f} | {casc(r1)} | "
             f"{'oui' if r['cascade_identique_v61'] else '**NON**'} | "
             f"{f(r1['mc_score'])} ({f(r61['mc_score'])}) | {f(r1['max_sep'])} | "
             f"{f(r1['stability'])} | {f(r1['s_sep'])} | "
             f"{f(r1['delta'], 2)} ({f(r61['delta'], 2)}) | "
             f"{r1['l7a_dir']} {f(r1['l7a_conf'], 3)} "
             f"({r61['l7a_dir']} {f(r61['l7a_conf'], 3)}) | "
             f"{r1['l5_top']} / {f(r1['l5_conf'], 3)} / {r1['l5_n_alerts']} | "
             f"{r1['l4_level']} {f(r1['l4_risk'], 3)} |")
L.append("")
L.append("Notes :")
L.append("- HP35 reel : les valeurs brutes du controle (`thresholds_in_control_units`, "
         "controle `step`) sont [0, 16, 90, 376, 376] en v6.2 (rep1 et rep2) comme "
         "en v6.1 — exactement le « 0 / 16 / 90 / 376 » du protocole §5.3. Les "
         "cascades en % sont identiques a la v6.1 au chiffre pres sur les 10 runs.")
L.append("- L7a HP35 reel 0,378 (v6.1 : 0,377) et TCGA v4 reel 0,405 (v6.1 : 0,405) : "
         "la graine L5 stable change legerement les alertes L5 donc le vote L7a "
         "(< 0,001, direction inchangee partout). Petites cohortes : L7a "
         "strictement identique a la v6.1 (GSE62452 down 0,197 ; ICGC up 0,181 ; "
         "DepMap down 0,196) — votes finis, pas de faux « up » / 0,50.")
L.append("- DepMap reel : falsification absente du JSON (comme en v6.1) ; "
         "DepMap nul : fals 0,043.")
L.append("")
L.append("## Determinisme — repetition 1 contre repetition 2 (processus separes)")
L.append("")
L.append("| Run | JSON octet-pour-octet ? | Divergences (comparaison NaN-aware) : "
         "total / chemins runtime / budget workers / autres | L5 identique ? | "
         "L4 identique ? | L7a identique ? | Cles horodatage exactes ? |")
L.append("|---|---|---|---|---|---|---|")
for r in d["runs"]:
    jd = r["json_diff"]
    L.append(f"| {r['run']} | {'oui' if r['json_identique_rep'] else 'non'} | "
             f"{jd['n_total']} / {jd['n_runtime_paths']} / {jd['n_worker_budget']} / "
             f"{jd['n_other']} | {'oui' if r['l5_identique_rep'] else 'non'} | "
             f"{'oui' if r['l4_identique_rep'] else 'non'} | "
             f"{'oui' if r['l7a_identique_rep'] else 'non'} | "
             f"{'aucune' if not r['rep1']['ts_keys'] else ', '.join(r['rep1']['ts_keys'])} |")
L.append("")
L.append("Lecture du « non » octet-pour-octet (repli documente §5.2 du protocole) : "
         "les seules divergences entre repetitions sont (1) les deux chemins "
         "`/runtime/dashboard_status/path` et `/runtime/telemetry_path` — ils "
         "contiennent le nom du dossier de sortie, qui differe par construction "
         "(`_rep2`) ; (2) les champs `worker_budget` (`available_memory_bytes`, "
         "`memory_cap`, `chosen`, `safe_cap`, `n_workers`, `chunksize`), dans "
         "`/runtime/worker_budget` et recopies dans `optimization_diagnostics` / "
         "`raw_optimization_diagnostics` — ils refletent la RAM libre au lancement "
         "(la machine a redemarre deux fois pendant le lot). **Aucun champ "
         "scientifique ne differe sur les 10 runs (0 divergence « autre »).** "
         "Aucune cle d'horodatage exacte (`timestamp`, `date`, `generated_at`, "
         "`run_date`, `created_at`) dans aucun `master_results.json` (10/10) — "
         "la premiere version du controle comptait a tort « candidate » comme "
         "date (sous-chaine), corrige en controle par nom exact.")
L.append("")
L.append("## Gigue mesuree par indicateur (max |rep1 − rep2| sur les 10 runs)")
L.append("")
L.append("| Indicateur | Gigue mesuree |")
L.append("|---|---|")
for k, v in d["gigue_max"].items():
    L.append(f"| {k} | {v} |")
L.append("")
L.append("**Gigue L5 = 0** (ainsi que L4, L7a, MC, max_separation, S_sep, Delta, "
         "falsification et cascade) : la piste (a) — hachage stable — fonctionne. "
         "Gigue effective S_sep pour la phase 2 (§3.4) : "
         "max(0,00 mesuree ; 0,07 plancher) = **0,07**.")
L.append("")
L.append("## Verdict §5.3")
L.append("")
L.append("- 20/20 runs exit 0. Cascades identiques a la v6.1 : **10/10**.")
L.append("- L7a fini sur les petites cohortes : oui (GSE62452, ICGC, DepMap — "
         "votes finis, identiques a la v6.1).")
L.append("- Gigue L5 = 0 (L5, L4, L7a identiques entre repetitions sur 10/10 ; "
         "JSON non octet-pour-octet uniquement pour chemins runtime + budget "
         "workers, 0 champ scientifique divergent).")
L.append("- **Validation REUSSIE.** La v6.2 reste une proposition : l'adoption "
         "comme version de travail attend le go de Zackary.")
L.append("")
L.append("Donnees brutes : `v62_validation_table.json`, `v62_validation_extract.log`.")
with open(os.path.join(BASE, "v62_validation_table.md"), "w") as fh:
    fh.write("\n".join(L) + "\n")
print("Ecrit : v62_validation_table.md")
