#!/usr/bin/env python3
"""Elucidation Delta — chantier 3 (§8.39). Au-dela de H1-H7 (PROTOCOL_v6.2 §4).
Lecture SEULE de v62_delta_levels.csv (222 runs, derivee des master_results.json
par extract_delta_levels.py). Aucun run du pipeline, aucune modification du pipeline.
But : tester des hypotheses mesurables supplementaires H8-H17 et, surtout,
tester honnetement la generalisation : majorite apprise sur v6.1 (156 runs)
appliquee aux 66 runs v6.2 (ensemble de replication independant ; Delta est
deterministe et le hachage L5 ne le touche pas).
Sorties : v62_delta_h8.log (stdout), v62_delta_h8.json (resume chiffre).
Regle d'honnetete : un predicteur qui utilise les 6 medianes divergence
elles-memes (ou leur rang) est une reformulation du mecanisme, pas une
explication ; il est rapporte comme diagnostic et marque CIRCULAIRE.
Seuls comptent pour le critere >= 90 % les predicteurs structurels
(masque, MFA, n, controle, famille, reel/nul, scan, d_sat/d_crit/d_null).
"""
import csv
import json
import math
import os
from collections import Counter, defaultdict

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(BASE, "v62_delta_levels.csv")
DIV = ["LevinaBickel", "PCAIntrinsic", "LocalPCA", "GraphDimension",
       "PersistentHomology", "MFA"]


def parse_sorted(s):
    out = []
    if not s:
        return out
    for tok in s.split(";"):
        if "=" in tok:
            k, v = tok.split("=", 1)
            try:
                out.append((k, float(v)))
            except ValueError:
                pass
    return out


def family_of(d):
    n = d.replace("results_fast_v61_", "").replace("results_fast_v62_", "")
    n = n.replace("_rep2", "")
    if n.endswith("_nul"):
        n = n[:-4]
    for p in ("immrot_", "parprot_", "depmaprot_"):
        if n.startswith(p):
            return p[:-1]
    for p in ("immune_", "tcga_", "geo71729", "geo62452", "icgc", "depmap",
              "hp35", "cptac", "coad", "luad", "mtap", "prolif", "atr",
              "parp_"):
        if n.startswith(p):
            return p.rstrip("_")
    return n.split("_")[0]


rows = []
with open(CSV, newline="") as fh:
    for r in csv.DictReader(fh):
        div = parse_sorted(r["div_sorted"])
        sat = parse_sorted(r["sat_sorted"])
        vals = {k: v for k, v in div}
        r["div_list"] = div
        r["sat_list"] = sat
        r["vals"] = vals
        r["n_f"] = float(r["n"]) if r["n"] else None
        r["mfa_f"] = float(r["mfa"]) if r["mfa"] else None
        r["d_div_f"] = float(r["d_div"]) if r["d_div"] else None
        r["d_sat_f"] = float(r["d_sat"]) if r["d_sat"] else None
        r["d_crit_f"] = float(r["d_crit"]) if r["d_crit"] else None
        r["d_null_f"] = float(r["d_null"]) if r["d_null"] else None
        r["trio_f"] = float(r["trio_gap_E"]) if r["trio_gap_E"] else None
        r["maxsep_f"] = float(r["max_sep"]) if r["max_sep"] else None
        r["stab_f"] = float(r["stability"]) if r["stability"] else None
        r["sharp_f"] = float(r["sharpness"]) if r["sharpness"] else None
        r["rob_f"] = float(r["robustness"]) if r["robustness"] else None
        r["l7a_f"] = float(r["l7a_conf"]) if r["l7a_conf"] else None
        r["dfa_f"] = float(r["dfa"]) if r["dfa"] else None
        r["is_nul"] = r["dir"].endswith("_nul")
        r["is_rep2"] = r["dir"].endswith("_rep2")
        r["family"] = family_of(r["dir"])
        r["version_short"] = "v6.1" if str(r["version"]).startswith("v6.1") else "v6.2"
        # rang (0-based) de chaque estimateur dans le tri divergence
        r["rank"] = {k: i for i, (k, v) in enumerate(div)}
        # paire non ordonnee (frozenset) pour mesurer si c'est l'ordre qui bloque
        r["upair"] = tuple(sorted(r["pair"].split("+"))) if r["pair"] else None
        rows.append(r)

print(f"Runs : {len(rows)} (v6.1 {sum(1 for r in rows if r['version_short']=='v6.1')}, "
      f"v6.2 {sum(1 for r in rows if r['version_short']=='v6.2')})")
print(f"Familles : {dict(Counter(r['family'] for r in rows))}")
print(f"Reel/nul : reel {sum(1 for r in rows if not r['is_nul'])}, "
      f"nul {sum(1 for r in rows if r['is_nul'])}")
print(f"Rep2 (duplicatas exacts v6.2) : {sum(1 for r in rows if r['is_rep2'])}")

# ---------------------------------------------------------------- structure
print("\n== STRUCTURE : rang de chaque estimateur divergence (0=plus bas) ==")
for name in DIV:
    c = Counter(r["rank"][name] for r in rows if name in r["rank"])
    print(f"  {name:20s} rangs {dict(sorted(c.items()))}  "
          f"dans-paire(3e/4e) : {sum(1 for r in rows if r['rank'].get(name) in (2, 3))}")
print("  Paires ordonnees : " + str(dict(Counter(r['pair'] for r in rows))))
print("  Paires non ordonnees : " + str(dict(Counter(r['upair'] for r in rows))))
inpair = Counter()
for r in rows:
    if r["upair"]:
        for m in r["upair"]:
            inpair[m] += 1
print(f"  Presence dans la paire (non ordonnee) : {dict(inpair)} / {len(rows)} runs")
print(f"  LocalPCA dans la paire : {inpair['LocalPCA']}/{len(rows)} = "
      f"{inpair['LocalPCA']/len(rows):.3f}")
print(f"  GraphDimension ou PersistentHomology dans la paire : "
      f"{inpair.get('GraphDimension', 0) + inpair.get('PersistentHomology', 0)}")
# singletons : k impair (5 ou 4 membres) -> mediane = une seule valeur
n_single = sum(1 for r in rows if r['pair'] and '+' not in r['pair'])
print(f"  Paires singleton (k impair) : {n_single} "
      f"({dict(Counter(r['pair'] for r in rows if r['pair'] and '+' not in r['pair']))})")

print("\n== ECARTS entre valeurs divergence triees (ce qui decide la paire) ==")
for (i, j, label) in [(1, 2, "2e->3e"), (2, 3, "3e->4e (ecart median)"),
                      (3, 4, "4e->5e"), (0, 1, "1re->2e"), (4, 5, "5e->6e")]:
    gaps = []
    for r in rows:
        d = r["div_list"]
        if len(d) == 6:
            gaps.append(d[j][1] - d[i][1])
    gaps = np.array(gaps)
    print(f"  {label:22s} n={len(gaps)} mediane {np.median(gaps):.3f} "
          f"Q1 {np.quantile(gaps, .25):.3f} Q3 {np.quantile(gaps, .75):.3f} "
          f"min {gaps.min():.3f} max {gaps.max():.3f} ; "
          f"ecart < 0,10 : {int((gaps < 0.10).sum())}/{len(gaps)} "
          f"({(gaps < 0.10).mean():.1%}), < 0,25 : {(gaps < 0.25).mean():.1%}")
# etendue totale des 6 valeurs
spans = np.array([r["div_list"][-1][1] - r["div_list"][0][1] for r in rows
                  if len(r["div_list"]) == 6])
print(f"  Etendue 6 valeurs : mediane {np.median(spans):.3f} "
      f"(Q1 {np.quantile(spans, .25):.3f}, Q3 {np.quantile(spans, .75):.3f})")

# ---------------------------------------------------------------- outils
def majority_accuracy(sub, keyfn, target="pair"):
    groups = defaultdict(list)
    for r in sub:
        if r[target] is None or r["d_div_f"] is None:
            continue
        groups[keyfn(r)].append(r)
    n_tot = sum(len(v) for v in groups.values())
    ok_pair = ok_val = 0
    for rs in groups.values():
        maj = Counter(x[target] for x in rs).most_common(1)[0][0]
        mean_div = float(np.mean([x["d_div_f"] for x in rs]))
        for x in rs:
            if x[target] == maj:
                ok_pair += 1
            if abs(x["d_div_f"] - mean_div) <= 0.10:
                ok_val += 1
    return ok_pair / n_tot, ok_val / n_tot, len(groups), n_tot


def holdout(train, test, keyfn, target="pair"):
    groups = defaultdict(list)
    for r in train:
        if r[target] is None:
            continue
        groups[keyfn(r)].append(r)
    global_maj = Counter(r[target] for r in train if r[target]).most_common(1)[0][0]
    global_mean = float(np.mean([r["d_div_f"] for r in train if r["d_div_f"] is not None]))
    ok_pair = ok_val = 0
    n = 0
    unseen = 0
    for r in test:
        if r[target] is None or r["d_div_f"] is None:
            continue
        n += 1
        g = groups.get(keyfn(r))
        if not g:
            unseen += 1
            maj, mean_div = global_maj, global_mean
        else:
            maj = Counter(x[target] for x in g).most_common(1)[0][0]
            mean_div = float(np.mean([x["d_div_f"] for x in g]))
        if r[target] == maj:
            ok_pair += 1
        if abs(r["d_div_f"] - mean_div) <= 0.10:
            ok_val += 1
    return ok_pair / n, ok_val / n, n, unseen


def quartiles(sub, field):
    vals = sorted(r[field] for r in sub if r[field] is not None and math.isfinite(r[field]))
    if len(vals) < 8:
        return None
    qs = np.quantile(vals, [0, .25, .5, .75, 1.0])
    return qs


def qbucket(qs):
    def f(r, field=None):
        return None
    return qs


def make_qfn(field, qs):
    def fn(r):
        v = r[field]
        if v is None or not math.isfinite(v):
            return "NA"
        for i in range(4):
            if v <= qs[i + 1] + (1e-12 if i == 3 else 0):
                return i
        return 3
    return fn


v61 = [r for r in rows if r["version_short"] == "v6.1"]
v62 = [r for r in rows if r["version_short"] == "v6.2"]
dedup = []
seen = set()
for r in rows:
    if r["is_rep2"]:
        continue
    key = r["div_sorted"]
    if key in seen:
        continue
    seen.add(key)
    dedup.append(r)
print(f"\nDedup (sans rep2, sans div_sorted identique) : {len(dedup)} runs "
      f"({len(rows) - len(dedup)} lignes retirees)")

# ---------------------------------------------------------------- H8-H17
cands = {
    # H8 : un seul membre continu, par quartiles (meme esprit que H2/MFA)
    "H8a LocalPCA (quartiles)": None,
    "H8b LevinaBickel (quartiles)": None,
    "H8c PCAIntrinsic (quartiles)": None,
    "H8d GraphDimension (quartiles)": None,
    "H8e PersistentHomology (quartiles)": None,
    # H9 : famille / reel-nul
    "H9 famille": lambda r: r["family"],
    "H10 reel/nul": lambda r: r["is_nul"],
    "H9b (famille, nul)": lambda r: (r["family"], r["is_nul"]),
    "H9c (famille, MFA)": lambda r: (r["family"], round(r["mfa_f"], 3) if r["mfa_f"] is not None else None),
    "H9d (famille, n)": lambda r: (r["family"], r["n_f"]),
    "H9e (famille, masque, MFA, n)": lambda r: (r["family"], r["mask"],
                                                round(r["mfa_f"], 3) if r["mfa_f"] is not None else None,
                                                r["n_f"]),
    # H11 : combinaison complete structurelle
    "H11 (masque, MFA, n, controle)": lambda r: (r["mask"],
                                                 round(r["mfa_f"], 3) if r["mfa_f"] is not None else None,
                                                 r["n_f"], r["control"]),
    "H11b (masque, MFA, n, famille)": lambda r: (r["mask"],
                                                 round(r["mfa_f"], 3) if r["mfa_f"] is not None else None,
                                                 r["n_f"], r["family"]),
    "H11c (masque, MFA, n, nul)": lambda r: (r["mask"],
                                             round(r["mfa_f"], 3) if r["mfa_f"] is not None else None,
                                             r["n_f"], r["is_nul"]),
    # H12 : n_fluxes detaille par estimateur (pas seulement le mode)
    "H12 n_fluxes_div (detail)": lambda r: r["n_fluxes_div"],
    # H13 : autres sorties du pipeline (scan / D_vector / trio)
    "H13a d_sat (quartiles)": None,
    "H13b d_crit (quartiles)": None,
    "H13c d_null (quartiles)": None,
    "H13d trio_gap_E (quartiles)": None,
    "H13e max_sep (quartiles)": None,
    "H13f (d_sat q, MFA)": None,
    "H13g (d_crit q, MFA)": None,
    # H14 : L7a / robustesse / sharpness en quartiles
    "H14a robustness log-quartiles": None,
    "H14b sharpness (quartiles)": None,
    "H14c l7a_dir": lambda r: r["l7a_dir"],
    "H14d (l7a_dir, MFA)": lambda r: (r["l7a_dir"],
                                      round(r["mfa_f"], 3) if r["mfa_f"] is not None else None),
    # H15 : reference H1+H2+H3 (rappel) et sa version non ordonnee
    "H15 REF (masque, MFA, n)": lambda r: (r["mask"],
                                           round(r["mfa_f"], 3) if r["mfa_f"] is not None else None,
                                           r["n_f"]),
}
# quartiles calcules sur l'ensemble (comme H4 dans l'extracteur d'origine)
qfields = {"H8a LocalPCA (quartiles)": ("vals", "LocalPCA"),
           "H8b LevinaBickel (quartiles)": ("vals", "LevinaBickel"),
           "H8c PCAIntrinsic (quartiles)": ("vals", "PCAIntrinsic"),
           "H8d GraphDimension (quartiles)": ("vals", "GraphDimension"),
           "H8e PersistentHomology (quartiles)": ("vals", "PersistentHomology")}
for label, (src, name) in qfields.items():
    vals = sorted(r["vals"][name] for r in rows if r["vals"].get(name) is not None)
    qs = np.quantile(vals, [0, .25, .5, .75, 1.0])

    def mk(name=name, qs=qs):
        def fn(r):
            v = r["vals"].get(name)
            if v is None:
                return "NA"
            for i in range(4):
                if v <= qs[i + 1] + (1e-12 if i == 3 else 0):
                    return i
            return 3
        return fn
    cands[label] = mk()
qmap = {"H13a d_sat (quartiles)": "d_sat_f", "H13b d_crit (quartiles)": "d_crit_f",
        "H13c d_null (quartiles)": "d_null_f", "H13d trio_gap_E (quartiles)": "trio_f",
        "H13e max_sep (quartiles)": "maxsep_f", "H14b sharpness (quartiles)": "sharp_f"}
for label, field in qmap.items():
    vals = sorted(r[field] for r in rows if r[field] is not None and math.isfinite(r[field]))
    qs = np.quantile(vals, [0, .25, .5, .75, 1.0])
    cands[label] = make_qfn(field, qs)
# robustness en log10 (etendue 1e-50..1)
robvals = sorted(math.log10(r["rob_f"]) for r in rows
                 if r["rob_f"] is not None and r["rob_f"] > 0)
qs_rob = np.quantile(robvals, [0, .25, .5, .75, 1.0])

def rob_fn(r):
    if r["rob_f"] is None or r["rob_f"] <= 0:
        return "NA"
    v = math.log10(r["rob_f"])
    for i in range(4):
        if v <= qs_rob[i + 1] + (1e-12 if i == 3 else 0):
            return i
    return 3
cands["H14a robustness log-quartiles"] = rob_fn
qs_sat = np.quantile(sorted(r["d_sat_f"] for r in rows if r["d_sat_f"] is not None),
                     [0, .25, .5, .75, 1.0])
qs_crit = np.quantile(sorted(r["d_crit_f"] for r in rows if r["d_crit_f"] is not None),
                      [0, .25, .5, .75, 1.0])
cands["H13f (d_sat q, MFA)"] = lambda r: (make_qfn("d_sat_f", qs_sat)(r),
                                          round(r["mfa_f"], 3) if r["mfa_f"] is not None else None)
cands["H13g (d_crit q, MFA)"] = lambda r: (make_qfn("d_crit_f", qs_crit)(r),
                                           round(r["mfa_f"], 3) if r["mfa_f"] is not None else None)

results = {}
print("\n== H8-H15 : prediction en echantillon (majorite) + hold-out v6.1 -> v6.2 ==")
print("   (hold-out : majorites apprises sur les 156 v6.1, testees sur les 66 v6.2 ;")
print("    groupe inconnu -> majorite globale v6.1. C'est le test honnete.)")
for label, fn in cands.items():
    a_pair, a_val, ng, n_tot = majority_accuracy(rows, fn)
    h_pair, h_val, h_n, h_unseen = holdout(v61, v62, fn)
    # paire non ordonnee, en echantillon
    u_pair, _, _, _ = majority_accuracy(rows, fn, target="upair")
    results[label] = {"acc_paire": a_pair, "acc_valeur": a_val, "n_groupes": ng,
                      "holdout_paire": h_pair, "holdout_valeur": h_val,
                      "holdout_unseen": h_unseen, "acc_upair": u_pair}
    print(f"{label:38s} echantillon paire {a_pair:.3f} | val {a_val:.3f} | "
          f"upaire {u_pair:.3f} ({ng} gr.) || hold-out paire {h_pair:.3f} | "
          f"val {h_val:.3f} (n={h_n}, inconnus {h_unseen})")

# ---------------------------------------------------------------- diagnostics circulaires
print("\n== DIAGNOSTIC (CIRCULAIRE — reformulation, pas explication) ==")
print("   Rang de MFA / LocalPCA parmi les 6 : predire la paire par le rang,")
print("   c'est utiliser les 6 valeurs elles-memes. Rapporte pour montrer OU")
print("   l'information vit, pas comme un predicteur eligible.")
for label, fn in {
        "rang MFA": lambda r: r["rank"].get("MFA"),
        "rang LocalPCA": lambda r: r["rank"].get("LocalPCA"),
        "(rang MFA, rang LocalPCA)": lambda r: (r["rank"].get("MFA"), r["rank"].get("LocalPCA")),
        "(rang MFA, masque, n)": lambda r: (r["rank"].get("MFA"), r["mask"], r["n_f"]),
}.items():
    a_pair, a_val, ng, n_tot = majority_accuracy(rows, fn)
    h_pair, h_val, h_n, h_unseen = holdout(v61, v62, fn)
    print(f"  {label:32s} echantillon paire {a_pair:.3f} | val {a_val:.3f} "
          f"({ng} gr.) || hold-out paire {h_pair:.3f} | val {h_val:.3f}")

# ---------------------------------------------------------------- residu dans le meilleur groupe
print("\n== RESIDU : que se passe-t-il DANS un groupe (masque, MFA, n) ? ==")
groups = defaultdict(list)
for r in rows:
    groups[(r["mask"], round(r["mfa_f"], 3) if r["mfa_f"] is not None else None,
            r["n_f"])].append(r)
multi = {k: v for k, v in groups.items() if len(v) >= 5}
print(f"  Groupes (masque,MFA,n) de taille >= 5 : {len(multi)} ; "
      f"groupes ou >= 2 paires differentes : "
      f"{sum(1 for v in multi.values() if len(set(x['pair'] for x in v)) >= 2)}")
for k in sorted(multi, key=lambda k: -len(multi[k]))[:6]:
    v = multi[k]
    print(f"  groupe {k} n={len(v)} paires={dict(Counter(x['pair'] for x in v))} "
          f"d_div {min(x['d_div_f'] for x in v):.2f}..{max(x['d_div_f'] for x in v):.2f}")
    # ecart LocalPCA-Levina-PCAIntr-MFA dans ce groupe : l'ordre y est-il serre ?
    for name in ("LocalPCA", "LevinaBickel", "PCAIntrinsic", "MFA"):
        vs = [x["vals"][name] for x in v if x["vals"].get(name) is not None]
        if vs:
            print(f"     {name:16s} {min(vs):.2f}..{max(vs):.2f} (etendue {max(vs)-min(vs):.2f})")
# ordre LocalPCA vs MFA : dans combien de groupes les deux ordres coexistent ?
flip = 0
tot = 0
for v in groups.values():
    if len(v) >= 3:
        tot += 1
        orders = set()
        for x in v:
            if "LocalPCA" in x["rank"] and "MFA" in x["rank"]:
                orders.add(x["rank"]["LocalPCA"] < x["rank"]["MFA"])
        if len(orders) == 2:
            flip += 1
print(f"  Groupes (taille>=3) ou LocalPCA passe devant ET derriere MFA : "
      f"{flip}/{tot}")

# ---------------------------------------------------------------- sensibilite dedup
print("\n== SENSIBILITE : ensemble dedup (sans rep2, sans doublon div_sorted) ==")
for label in ["H15 REF (masque, MFA, n)", "H11 (masque, MFA, n, controle)",
              "H11b (masque, MFA, n, famille)", "H9e (famille, masque, MFA, n)"]:
    fn = cands[label]
    a_pair, a_val, ng, n_tot = majority_accuracy(dedup, fn)
    print(f"  dedup {label:38s} paire {a_pair:.3f} | val {a_val:.3f} ({ng} gr., n={n_tot})")
a_pair, a_val, ng, n_tot = majority_accuracy(dedup, cands["H15 REF (masque, MFA, n)"],
                                            target="upair")
print(f"  dedup REF upaire (non ordonnee) : {a_pair:.3f} (n={n_tot})")

# ---------------------------------------------------------------- Delta : discrimination rappel
print("\n== RAPPEL : Delta comme discriminateur (phase 2, v6.1/v6.2) ==")
print("  (chiffres repris de PROTOCOL_v6.2 §1 et v62_delta_elucidation.md ; "
      "non recalcules ici)")
print("  Phase 2 : Delta 6/8 paires principales ; echec HP35 (nul 4,57 > reel 4,48) ;")
print("  annexe 13/23 ; deux ecarts <= 0,15. Statut inchange : piste fragile.")

best = max(results.items(), key=lambda kv: (kv[1]["acc_paire"] or 0))
best_ho = max(results.items(), key=lambda kv: (kv[1]["holdout_paire"] or 0))
print(f"\nMEILLEUR en echantillon : {best[0]} paire {best[1]['acc_paire']:.3f} "
      f"valeur {best[1]['acc_valeur']:.3f}")
print(f"MEILLEUR en hold-out v6.1->v6.2 : {best_ho[0]} paire "
      f"{best_ho[1]['holdout_paire']:.3f} valeur {best_ho[1]['holdout_valeur']:.3f}")
elucide = (best[1]["acc_paire"] >= 0.90 and best[1]["acc_valeur"] >= 0.90
           and best_ho[1]["holdout_paire"] >= 0.90 and best_ho[1]["holdout_valeur"] >= 0.90)
print(f"VERDICT §8.39 (critere >= 90 % paire ET valeur, en echantillon ET en "
      f"hold-out) : {'ELUCIDE' if elucide else 'NON ELUCIDE'}")

json.dump({"n_runs": len(rows), "n_v61": len(v61), "n_v62": len(v62),
           "n_dedup": len(dedup),
           "localpca_dans_paire": inpair["LocalPCA"],
           "graphdim_ph_dans_paire": inpair.get("GraphDimension", 0) + inpair.get("PersistentHomology", 0),
           "predictions": results,
           "meilleure_echantillon": best[0], "meilleure_holdout": best_ho[0],
           "elucide": elucide,
           "familles": dict(Counter(r["family"] for r in rows))},
          open(os.path.join(BASE, "v62_delta_h8.json"), "w"), indent=1, default=str)
print("Ecrit : v62_delta_h8.json")
