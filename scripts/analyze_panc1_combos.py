#!/usr/bin/env python3
"""Analyse des combinaisons PANC-1 (NCATS, Pourmousa et al. Nat Commun 2025).

Donnees : depot GitHub ncats/PANC1 (main), dossiers NCATS/9191 et NCATS/9197,
telecharges par raw.githubusercontent.com le 16 nov. 2026 (tailles verifiees
contre l'API GitHub ; SHA-256 dans panc1_sha256.txt).
  - metadata.csv : une ligne par bloc = une paire (RowName, ColName) + cibles + IC50.
  - calc.csv : une ligne par bloc x replicat, scores de synergie (Gamma, Beta,
    ExcessHSA, ...). Gamma < 0,95 = synergique (definition de l'article).

But : (1) decrire la matrice (nombre de paires, medicaments, cibles) ;
(2) chercher les paires impliquant un inhibiteur MEK/KRAS/ERK ou
l'hydroxychloroquine ; (3) compter les synergies ; (4) rattacher PANC-1
a l'axe Chronos KRAS (DepMap 24Q4, deja sur disque) — PANC-1 est UNE
seule lignee : aucun test de correlation inter-lignees n'est possible,
c'est documente, pas contourne.
"""
import hashlib
import os
import pandas as pd
import numpy as np

DATA = os.path.expanduser("~/workspace/runs/pdac-v6/data/panc1_ncata")
OUT = os.path.expanduser("~/workspace/runs/pdac-v6/data/panc1_combinations_summary.csv")

frames = []
for assay in ["9191", "9197"]:
    meta = pd.read_csv(f"{DATA}/{assay}_metadata.csv")
    calc = pd.read_csv(f"{DATA}/{assay}_calc.csv")
    print(f"assay {assay} : metadata {len(meta)} blocs, calc {len(calc)} lignes, "
          f"blocs uniques calc {calc['BlockId'].nunique()}, "
          f"replicats {sorted(calc['Replicate'].unique())}")
    print(f"  colonnes calc : {list(calc.columns)}")
    m = meta.merge(calc, on="BlockId", how="left", suffixes=("", "_calc"))
    m["assay"] = assay
    frames.append(m)

df = pd.concat(frames, ignore_index=True)
print(f"\nTOTAL lignes (bloc x replicat) : {len(df)}")
print(f"paires uniques (assay, RowName, ColName) : "
      f"{df[['assay', 'RowName', 'ColName']].drop_duplicates().shape[0]}")
print(f"paires uniques (RowName, ColName) tous assays : "
      f"{df[['RowName', 'ColName']].drop_duplicates().shape[0]}")

drugs = sorted(set(df["RowName"]) | set(df["ColName"]))
print(f"\nmedicaments distincts : {len(drugs)}")
for d in drugs:
    tg = set(df.loc[df["RowName"] == d, "RowTarget"]) | set(df.loc[df["ColName"] == d, "ColTarget"])
    print(f"  - {d} :: {'; '.join(sorted(tg))}")

# Moyenne gamma par paire (tous replicats confondus)
g = (df.groupby(["RowName", "ColName", "RowTarget", "ColTarget"])
       .agg(gamma_mean=("Gamma", "mean"), gamma_min=("Gamma", "min"),
            n_rep=("Gamma", "size"), beta_mean=("Beta", "mean"),
            hsa_mean=("ExcessHSA", "mean"))
       .reset_index())
g["synergique"] = g["gamma_mean"] < 0.95
g["synergie_forte"] = g["gamma_mean"] < 0.5
g = g.sort_values("gamma_mean")
g.to_csv(OUT, index=False)
print(f"\nresume ecrit : {OUT} ({len(g)} paires)")
print(f"synergiques (gamma moyen < 0,95) : {int(g['synergique'].sum())}/{len(g)} "
      f"({100 * g['synergique'].mean():.1f} %)")
print(f"synergie forte (gamma moyen < 0,5) : {int(g['synergie_forte'].sum())}")

# Paires impliquant MEK / KRAS / ERK / autophagie (HCQ, chloroquine)
keys = ["MEK", "KRAS", "ERK", "Hydroxychloroquine", "Chloroquine", "Autophagy",
        "Trametinib", "Cobimetinib", "Selumetinib", "Binimetinib", "Sotorasib",
        "SOS1", "SHP2", "RAF"]
mask = g["RowTarget"].str.contains("|".join(keys), case=False, na=False) | \
       g["ColTarget"].str.contains("|".join(keys), case=False, na=False) | \
       g["RowName"].str.contains("|".join(keys), case=False, na=False) | \
       g["ColName"].str.contains("|".join(keys), case=False, na=False)
print(f"\npaires impliquant MEK/KRAS/ERK/SHP2/SOS1/HCQ : {int(mask.sum())}")
print(g[mask].to_string(index=False) if mask.sum() else "  AUCUNE")

print("\n=== TOP 15 synergies (gamma moyen le plus bas) ===")
print(g.head(15)[["RowName", "ColName", "gamma_mean", "n_rep"]].to_string(index=False))

# PANC-1 dans DepMap Chronos KRAS (contexte : une seule lignee)
ge = pd.read_csv(os.path.expanduser(
    "~/workspace/runs/pdac-v6/data/CRISPRGeneEffect.csv"),
    index_col=0, usecols=["KRAS (3845)"])
# la premiere colonne est sans nom : on relit par position
ge = pd.read_csv(os.path.expanduser(
    "~/workspace/runs/pdac-v6/data/CRISPRGeneEffect.csv"),
    index_col=0)
kras_col = [c for c in ge.columns if c.startswith("KRAS (")][0]
model = pd.read_csv(os.path.expanduser("~/workspace/runs/pdac-v6/data/Model.csv"))
panc1 = model[model["CellLineName"].str.upper().str.replace("-", "") == "PANC1"]
print(f"\nPANC-1 dans Model.csv : {len(panc1)} ligne(s)")
for _, row in panc1.iterrows():
    mid = row["ModelID"]
    if mid in ge.index:
        print(f"  {mid} {row['CellLineName']} : Chronos KRAS = "
              f"{ge.loc[mid, kras_col]:.3f} (mediane pancreas DepMap -1,76)")
print("\nSHA-256 des 8 fichiers sources :")
for f in sorted(os.listdir(DATA)):
    if f.endswith(".csv"):
        h = hashlib.sha256(open(f"{DATA}/{f}", "rb").read()).hexdigest()
        print(f"  {f} {h[:16]}...")
