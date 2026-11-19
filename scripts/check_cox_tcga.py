#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contre-vérification du Cox TCGA par 3 implémentations indépendantes :
(1) cox_fit de survival_tcga_verify.py (Breslow + BFGS + Hessienne num.),
(2) cox_fit de survival_geo71729.py (Newton-Raphson, sommes cumulées),
(3) statsmodels PHReg (bibliothèque de référence).
Mêmes données, mêmes covariables standardisées (ddof=0).
"""
import sys
import tarfile

import numpy as np
import pandas as pd

sys.path.insert(0, "/home/hatch/workspace/runs/pdac-v6")
import survival_tcga_verify as _tv  # noqa: F401  (ré-exécute la vérif.)
import survival_geo71729 as _g  # noqa: F401

# Les données préparées par survival_tcga_verify sont dans son espace de noms.
time, ev = _tv.time, _tv.ev
covs = _tv.covs
print(f"n={len(time)} décès={int(ev.sum())}")

# --- (2) cox_fit de l'agent GSE71729 ---------------------------------------
df = pd.DataFrame({k: v for k, v in covs.items()})
df["os_months"] = time
df["dead"] = ev.astype(int)
print("--- (2) Newton-Raphson agent GSE71729, univarié ---")
for col in ["KRAS résidu", "MUC16", "CEACAM5", "PGC", "DPCR1", "CLDN18"]:
    c, hr, b, se, p = _g.cox_fit(df, [col])[0]
    print(f"  {c:12s} HR={hr:.2f} coef={b:+.2f} se={se:.2f} p={p:.4f}")
print("--- (2) multivarié KRAS+MUC16+CEACAM5 ---")
for c, hr, b, se, p in _g.cox_fit(df, ["KRAS résidu", "MUC16", "CEACAM5"]):
    print(f"  {c:12s} HR={hr:.2f} coef={b:+.2f} se={se:.2f} p={p:.4f}")
print("--- (2) ajusté 6 gènes ---")
for c, hr, b, se, p in _g.cox_fit(
        df, ["KRAS résidu", "MUC16", "CEACAM5", "PGC", "DPCR1", "CLDN18"]):
    print(f"  {c:12s} HR={hr:.2f} coef={b:+.2f} se={se:.2f} p={p:.4f}")

# --- (3) statsmodels PHReg --------------------------------------------------
from statsmodels.duration.hazard_regression import PHReg

print("--- (3) statsmodels PHReg, univarié ---")
for col in ["KRAS résidu", "MUC16", "CEACAM5", "PGC", "DPCR1", "CLDN18"]:
    res = PHReg(time, covs[col].reshape(-1, 1), status=ev.astype(int)).fit()
    b, se, p = res.params[0], res.bse[0], res.pvalues[0]
    print(f"  {col:12s} HR={np.exp(b):.2f} coef={b:+.2f} se={se:.2f} p={p:.4f}")
print("--- (3) multivarié KRAS+MUC16+CEACAM5 ---")
Zm = np.column_stack([covs["KRAS résidu"], covs["MUC16"], covs["CEACAM5"]])
res = PHReg(time, Zm, status=ev.astype(int)).fit()
for name, b, s, p in zip(["KRAS résidu", "MUC16", "CEACAM5"],
                         res.params, res.bse, res.pvalues):
    print(f"  {name:12s} HR={np.exp(b):.2f} coef={b:+.2f} se={s:.2f} p={p:.4f}")
print("--- (3) ajusté 6 gènes ---")
Z6 = np.column_stack([covs["KRAS résidu"], covs["MUC16"], covs["CEACAM5"],
                      covs["PGC"], covs["DPCR1"], covs["CLDN18"]])
res = PHReg(time, Z6, status=ev.astype(int)).fit()
for name, b, s, p in zip(["KRAS résidu", "MUC16", "CEACAM5", "PGC",
                          "DPCR1", "CLDN18"], res.params, res.bse,
                         res.pvalues):
    print(f"  {name:12s} HR={np.exp(b):.2f} coef={b:+.2f} se={s:.2f} p={p:.4f}")
