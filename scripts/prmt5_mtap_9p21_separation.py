#!/usr/bin/env python3
"""
Séparation MTAP vs délétion 9p21 entière — DepMap 24Q4 (16 nov. 2026).
Suite directe du §8.28 du livre blanc : la limite honnête du test PRMT5/MTAP
était que MTAP et CDKN2A sont presque toujours perdus ensemble (CN +0,808
en pancréas). Ce script compte les lignées DISCORDANTES et compare la
dépendance PRMT5 entre :
  - both-del     : MTAP < 0,5 ET CDKN2A < 0,5
  - CDKN2A-only  : MTAP >= 0,5 ET CDKN2A < 0,5
  - MTAP-only    : MTAP < 0,5 ET CDKN2A >= 0,5
  - neither      : les deux >= 0,5
Si l'effet PRMT5 suit MTAP (et non la délétion 9p21), le groupe CDKN2A-only
doit ressembler à "neither", pas à "both-del".
Mêmes sources et seuils que prmt5_mtap_dependency.py (CN linéaire, < 0,5
= délétion profonde). Lecture par blocs, aucune imputation.
"""
import hashlib, time
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr

T0 = time.time()
DATA = "data"
GE = f"{DATA}/CRISPRGeneEffect.csv"
MO = f"{DATA}/Model.csv"
CN = f"{DATA}/OmicsCNGene.csv"
LOG = open("prmt5_mtap_9p21_separation.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); LOG.write(s + "\n"); LOG.flush()

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

log("=== Séparation MTAP vs 9p21 — DepMap 24Q4 ===")
model = pd.read_csv(MO, low_memory=False)
lineage = model.set_index("ModelID")["OncotreeLineage"]

cn_head = pd.read_csv(CN, nrows=0)
cn_cols = list(cn_head.columns[1:])
mtap_col = [c for c in cn_cols if c.startswith("MTAP (")][0]
cdkn2a_col = [c for c in cn_cols if c.startswith("CDKN2A (")][0]
chunks = []
for ch in pd.read_csv(CN, index_col=0, chunksize=200,
                      usecols=[cn_head.columns[0], mtap_col, cdkn2a_col],
                      dtype={mtap_col: "float32", cdkn2a_col: "float32"}):
    chunks.append(ch)
cn = pd.concat(chunks).astype("float64")

ge_head = pd.read_csv(GE, nrows=0)
ge_cols = list(ge_head.columns[1:])
need = {}
for sym in ["PRMT5", "CDKN2A", "KRAS", "ACTB"]:
    hits = [c for c in ge_cols if c.startswith(sym + " (")]
    assert len(hits) == 1, f"{sym} : {len(hits)} colonnes"
    need[sym] = hits[0]
ge_chunks = []
dtypes = {c: "float32" for c in need.values()}
for ch in pd.read_csv(GE, index_col=0, chunksize=200,
                      usecols=[ge_head.columns[0]] + list(need.values()),
                      dtype=dtypes):
    ge_chunks.append(ch)
ge = pd.concat(ge_chunks).astype("float64")
_name_to_sym = {v: k for k, v in need.items()}
ge.columns = [_name_to_sym[c] for c in ge.columns]

df = ge.join(cn.rename(columns={mtap_col: "MTAP_CN", cdkn2a_col: "CDKN2A_CN"}), how="inner")
df["lineage"] = lineage.reindex(df.index)
df["is_panc"] = df["lineage"] == "Pancreas"
log("jointure CN x Chronos :", len(df), "modèles | pancréas :", int(df["is_panc"].sum()))

def group(r):
    m = r["MTAP_CN"] < 0.5; c = r["CDKN2A_CN"] < 0.5
    if m and c: return "both-del"
    if (not m) and c: return "CDKN2A-only"
    if m and (not c): return "MTAP-only"
    return "neither"
df["grp"] = df.apply(group, axis=1)
df.to_csv("data/prmt5_mtap_pancancer_lines.csv")
log("CSV lignées pan-cancer écrit : data/prmt5_mtap_pancancer_lines.csv | lignes :", len(df))

def report(sub, label):
    log(f"--- {label} (n={len(sub)}) ---")
    for gname in ["both-del", "CDKN2A-only", "MTAP-only", "neither"]:
        s = sub[sub["grp"] == gname]
        if len(s):
            log(f"  {gname}: n={len(s)} PRMT5 médiane {s['PRMT5'].median():+.3f} "
                f"(moyenne {s['PRMT5'].mean():+.3f}) | KRAS méd {s['KRAS'].median():+.3f} "
                f"| ACTB méd {s['ACTB'].median():+.3f}")
        else:
            log(f"  {gname}: n=0")
    def mw(a, b, gene="PRMT5"):
        x = sub[sub["grp"] == a][gene].dropna(); y = sub[sub["grp"] == b][gene].dropna()
        if len(x) >= 3 and len(y) >= 3:
            u, p = mannwhitneyu(x, y, alternative="two-sided")
            log(f"  MW {gene} {a} (n={len(x)}) vs {b} (n={len(y)}): U={u:.0f} p={p:.4g}")
        else:
            log(f"  MW {gene} {a} vs {b}: impossible (n={len(x)}/{len(y)})")
    mw("both-del", "CDKN2A-only")
    mw("CDKN2A-only", "neither")
    mw("both-del", "neither")
    mw("MTAP-only", "neither")
    # Dans les CDKN2A-délétées seules : PRMT5 suit-il encore le CN MTAP ?
    d = sub[sub["CDKN2A_CN"] < 0.5]
    if len(d) >= 10:
        r, pp = spearmanr(d["MTAP_CN"], d["PRMT5"], nan_policy="omit")
        log(f"  Dans CDKN2A-del (n={len(d)}): Spearman PRMT5~CN MTAP rho {r:+.3f} p={pp:.3g}")
        r2, pp2 = spearmanr(d["CDKN2A_CN"], d["PRMT5"], nan_policy="omit")
        log(f"  Dans CDKN2A-del (n={len(d)}): Spearman PRMT5~CN CDKN2A rho {r2:+.3f} p={pp2:.3g}")

report(df, "PAN-CANCER (tous modèles)")
report(df[~df["is_panc"]], "PAN-CANCER hors pancréas")
report(df[df["is_panc"]], "PANCRÉAS seul (vérification, doit reproduire le comptage manuel)")
log("SHA data/prmt5_mtap_pancancer_lines.csv :", sha("data/prmt5_mtap_pancancer_lines.csv"))
log("durée : %.1f s" % (time.time() - T0))
log("=== FIN, exit 0 ===")
LOG.close()
