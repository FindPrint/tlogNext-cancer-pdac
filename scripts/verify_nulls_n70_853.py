#!/usr/bin/env python3
"""§8.53 (a) — Vérification des entrées (aucun run).
Re-vérifie les SHA-256 des 6 CSV de flux (réel + nul graine 42, ICGC /
GSE62452 / TCGA) contre PROVENANCE_immune_v6.md ; vérifie que chaque nul
graine 42 est une permutation par ligne du réel ; 0 valeur manquante ;
n par bras. Sortie : nulls_n70_853_verify.json.
Protocole gelé : PROTOCOL_nulls_n70_853.md
"""
import hashlib
import json

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
EXPECTED = {
    "pdac_immune_tcga_fluxes.csv": "66dbb672ea2a305ea67b51be3f9522a47e5003425f271c9cc4f42bc0427bbd2e",
    "pdac_immune_geo62452_fluxes.csv": "97c4689a6ecacd0a73a77804200a72a90994d60bea7e6b2c079195acbffd79a3",
    "pdac_immune_icgc_fluxes.csv": "10823879c0632d8c3ec7a07b0e73047a81ece2052aff9c2e5cd96bbf4d388adc",
}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    out = {"sha": {}, "permutation_par_ligne": {}, "n": {}, "manquantes": {}}
    ok = True
    for cohorte in ("icgc", "geo62452", "tcga"):
        reel = f"pdac_immune_{cohorte}_fluxes.csv"
        nul = f"pdac_immune_{cohorte}_fluxes_nul.csv"
        df_r = pd.read_csv(f"{PDAC}/{reel}")
        df_n = pd.read_csv(f"{PDAC}/{nul}")
        s_r = sha(f"{PDAC}/{reel}")
        s_n = sha(f"{PDAC}/{nul}")
        out["sha"][reel] = s_r
        out["sha"][nul] = s_n
        exp = EXPECTED.get(reel)
        match = (s_r == exp) if exp else None
        out["sha"][reel + "_conforme_PROVENANCE"] = match
        if match is False:
            ok = False
        out["n"][cohorte] = {"reel": int(len(df_r)), "nul": int(len(df_n))}
        out["manquantes"][cohorte] = {
            "reel": int(df_r.isna().sum().sum()),
            "nul": int(df_n.isna().sum().sum())}
        if df_r.isna().sum().sum() or df_n.isna().sum().sum():
            ok = False
        # permutation par ligne : même multi-ensemble de lignes, step inchangé
        same_step = bool((df_r["step"].values == df_n["step"].values).all())
        cols = [c for c in df_r.columns if c != "step"]
        r_rows = sorted(map(tuple, df_r[cols].values.tolist()))
        n_rows = sorted(map(tuple, df_n[cols].values.tolist()))
        same_multiset = r_rows == n_rows
        out["permutation_par_ligne"][cohorte] = {
            "step_inchange": same_step, "meme_multi_ensemble": bool(same_multiset)}
        if not (same_step and same_multiset):
            ok = False
        print(f"[{cohorte}] n={len(df_r)} SHA réel conforme={match} "
              f"step_inchangé={same_step} multi_ensemble={same_multiset} "
              f"manquantes={int(df_r.isna().sum().sum())}/{int(df_n.isna().sum().sum())}")
    out["ok"] = bool(ok)
    with open(f"{PDAC}/nulls_n70_853_verify.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("écrit: nulls_n70_853_verify.json ok=", ok)


if __name__ == "__main__":
    main()
