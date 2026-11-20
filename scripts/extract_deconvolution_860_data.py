#!/usr/bin/env python3
"""Extraction .rda -> CSV en clair (§8.60, Porte D).
Sources : imogimap (Korkut lab, GitHub korkutlab/imogimap), miroir public
des fractions CIBERSORT (Thorsson et al. 2018) et de la fraction
leucocytaire TCGA. Fichiers bruts jamais modifies ; lecture seule.
Sorties : data_deconvolution_860/TCGA_IMCell_fraction.csv,
          data_deconvolution_860/TCGA_Leukocyte_fraction.csv
          + inventaire JSON deconvolution_860_rda_inventory.json
"""
import hashlib
import json
import sys

import pandas as pd
import rdata

D = "/home/hatch/workspace/runs/pdac-v6/data_deconvolution_860/"
PROJ = "/home/hatch/workspace/runs/pdac-v6/"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load_rda(path):
    objs = rdata.read_rda(path)
    assert len(objs) == 1, f"{path}: {len(objs)} objets, attendu 1"
    name, obj = next(iter(objs.items()))
    if hasattr(obj, "to_pandas"):
        df = obj.to_pandas()
    else:
        df = pd.DataFrame(obj)
    return name, df


inv = {}
for fname in ["TCGA_IMCell_fraction.rda", "TCGA_Leukocyte_fraction.rda"]:
    name, df = load_rda(D + fname)
    out = D + fname.replace(".rda", ".csv")
    df.to_csv(out, index=False)
    frac_cols = [c for c in df.columns if c not in ("PATIENT_BARCODE", "Tumor_Sample_ID")]
    inv[fname] = {
        "rda_object": name,
        "rda_sha256": sha256(D + fname),
        "csv": out,
        "csv_sha256": sha256(out),
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "columns": list(df.columns),
        "n_unique_barcodes": int(df.iloc[:, 0].nunique()),
        "n_duplicates_barcode": int(df.shape[0] - df.iloc[:, 0].nunique()),
    }
    print(f"{fname}: objet={name} shape={df.shape}")
    print("  colonnes:", list(df.columns))
    if frac_cols:
        sub = df[frac_cols].apply(pd.to_numeric, errors="coerce")
        print("  min global:", float(sub.min().min()), " max global:", float(sub.max().max()))
        print("  somme par ligne: min=%.4f med=%.4f max=%.4f" % (
            sub.sum(axis=1).min(), sub.sum(axis=1).median(), sub.sum(axis=1).max()))
        print("  NaN total:", int(sub.isna().sum().sum()))
        nan_per_col = sub.isna().sum()
        print("  NaN par colonne (top):", nan_per_col[nan_per_col > 0].to_dict())
        n_nan_rows = int(sub.isna().any(axis=1).sum())
        n_all_nan_rows = int(sub.isna().all(axis=1).sum())
        print(f"  lignes avec >=1 NaN: {n_nan_rows} ; lignes tout-NaN: {n_all_nan_rows}")
        inv[fname]["nan_total"] = int(sub.isna().sum().sum())
        inv[fname]["nan_par_colonne"] = {str(k): int(v) for k, v in nan_per_col.items() if v > 0}
        inv[fname]["lignes_avec_nan"] = n_nan_rows
        inv[fname]["lignes_tout_nan"] = n_all_nan_rows

# Jointure avec les 178 tumeurs du projet (par patient, 12 caracteres)
# Les barcodes sont dans immune_kras_order_tcga.csv (colonne sample).
order = pd.read_csv(PROJ + "immune_kras_order_tcga.csv")
proj_pat = order["sample"].str[:12]
print("colonnes ordre:", list(order.columns))
print("n tumeurs projet:", len(order))
inv["projet"] = {"n_tumeurs": int(len(order)),
                 "ordre_sha256": sha256(PROJ + "immune_kras_order_tcga.csv"),
                 "flux_sha256": sha256(PROJ + "pdac_immune_tcga_fluxes.csv")}

im = pd.read_csv(D + "TCGA_IMCell_fraction.csv")
lk = pd.read_csv(D + "TCGA_Leukocyte_fraction.csv")
print("IMCell barcode col:", im.columns[0], " ex:", im.iloc[0, 0])
print("Leuko barcode col:", lk.columns[0], " ex:", lk.iloc[0, 0])
print("Leuko colonnes:", list(lk.columns))
for df, label, key in [(im, "IMCell", "PATIENT_BARCODE"), (lk, "Leuko", None)]:
    k = key or df.columns[0]
    m = proj_pat.isin(set(df[k].astype(str).str[:12]))
    print(f"jointure {label} (patient 12 car.): {int(m.sum())}/178 appariees")
    inv[f"jointure_{label}"] = {"appariees": int(m.sum()), "sur": 178,
                                "non_appariees": order.loc[~m, "sample"].tolist()}

with open(D + "deconvolution_860_rda_inventory.json", "w") as f:
    json.dump(inv, f, indent=2, ensure_ascii=False)
print("inventaire:", D + "deconvolution_860_rda_inventory.json")
