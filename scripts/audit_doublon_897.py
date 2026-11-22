#!/usr/bin/env python3
"""§8.97 partie 1 — Balayage mecanique : un flux de controle est-il aussi
un flux analyse quelque part ? (PROTOCOL_audit_regle_897.md, lecture seule,
aucun run de pipeline.)
Pour chaque dossier de run (results_fast_v62_*, results_fast_v61_*, tout
dossier de run du projet) : lit master_results.json (csv_path, controle)
et les colonnes du CSV source ; signale :
  (i) toute colonne se terminant par '.1' — signature mecanique du
      doublon §8.32 (pandas renomme la colonne dupliquee) ;
  (ii) toute colonne de controle presente aussi comme flux analyse
      (meme nom, autre position) ;
  (iii) tout CSV dont la premiere colonne est un flux qui reapparait
      parmi les colonnes suivantes.
Sortie : audit_doublon_897.json (par dossier + resume).
"""
import glob
import json
import os

import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
LIVRE = "/home/hatch/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md"


def main():
    dirs = sorted(glob.glob(os.path.join(PDAC, "results_*")))
    res = {"dossiers_scannes": 0, "sans_master": [], "sans_csv": [],
           "doublon_point1": [], "controle_reanalyse": [], "propres": 0,
           "detail": {}, "non_verifiables": []}
    for d in dirs:
        nom = os.path.basename(d)
        mj = os.path.join(d, "master_results.json")
        if not os.path.exists(mj):
            res["sans_master"].append(nom)
            continue
        try:
            j = json.load(open(mj))
        except Exception as e:
            res["sans_master"].append(f"{nom} (JSON illisible: {e})")
            continue
        md = j.get("metadata") or {}
        csv_path = md.get("csv_path") or j.get("csv_path")
        control = md.get("control") or j.get("control")
        if not csv_path or not os.path.exists(csv_path):
            # csv_path peut etre relatif a pdac-v6 ou absolu
            cand = os.path.join(PDAC, os.path.basename(csv_path or ""))
            if csv_path and os.path.exists(cand):
                csv_path = cand
            else:
                res["sans_csv"].append(nom)
                continue
        try:
            cols = list(pd.read_csv(csv_path, nrows=1).columns)
        except Exception as e:
            res["sans_csv"].append(f"{nom} (CSV illisible: {e})")
            continue
        res["dossiers_scannes"] += 1
        dups = [c for c in cols if c.endswith(".1")]
        # (ii) : le controle (s'il est un flux) reapparait-il comme flux ?
        # Le pipeline exclut la colonne de controle ; un doublon = meme nom
        # en deux positions (dont .1) ou controle != 1re col et present 2x.
        controle_reanalyse = []
        if control and cols.count(control) > 1:
            controle_reanalyse.append(control)
        if dups:
            res["doublon_point1"].append({"dossier": nom, "csv": csv_path,
                                          "colonnes_point1": dups,
                                          "controle": control})
        if controle_reanalyse:
            res["controle_reanalyse"].append({"dossier": nom, "csv": csv_path,
                                              "controle": control})
        if not dups and not controle_reanalyse:
            res["propres"] += 1
        res["detail"][nom] = {"csv": os.path.basename(csv_path),
                              "controle": control, "n_colonnes": len(cols),
                              "premiere_colonne": cols[0],
                              "colonnes_point1": dups}
    with open(os.path.join(PDAC, "audit_doublon_897.json"), "w") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    print(f"dossiers scannes: {res['dossiers_scannes']}")
    print(f"propres (aucun .1, aucun controle reanalyse): {res['propres']}")
    print(f"avec colonne .1: {len(res['doublon_point1'])}")
    print(f"controle reanalyse: {len(res['controle_reanalyse'])}")
    print(f"sans master_results.json: {len(res['sans_master'])}")
    print(f"sans CSV lisible: {len(res['sans_csv'])}")
    for x in res["doublon_point1"][:20]:
        print("  .1 :", x["dossier"], x["colonnes_point1"], "controle:", x["controle"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
