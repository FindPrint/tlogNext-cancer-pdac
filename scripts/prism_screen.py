"""PRISM 24Q2 — test médicamenteux du sous-groupe v4.
Question : parmi les lignées pancréatiques, les lignées les plus dépendantes
de KRAS (axe du sous-groupe v4 TCGA) répondent-elles différemment à certains
médicaments ? Test par composé : corrélation de Spearman entre la viabilité
PRISM et l'effet Chronos KRAS, + écart moyen tertile KRAS-fort vs KRAS-faible.
Provenance : DepMap Repurposing Public 24Q2, figshare article 25917643.
"""
import json, subprocess, sys, os
import pandas as pd, numpy as np

DATA = os.path.dirname(os.path.abspath(__file__)) + "/data"
os.makedirs(DATA, exist_ok=True)

def dl(name, url):
    path = os.path.join(DATA, name)
    if os.path.exists(path):
        print("déjà là :", name, os.path.getsize(path), "octets", flush=True)
        return path
    subprocess.run(["curl", "-sS", "-L", "--max-time", "600", "-o", path, url],
                   check=True)
    print("téléchargé :", name, os.path.getsize(path), "octets", flush=True)
    return path

# 1. URLs figshare
meta = json.loads(subprocess.run(
    ["curl", "-sS", "--max-time", "60",
     "https://api.figshare.com/v2/articles/25917643"],
    capture_output=True, text=True, check=True).stdout)
files = {f["name"]: f["download_url"] for f in meta["files"]}
MATRIX = "Repurposing_Public_24Q2_Extended_Primary_Data_Matrix.csv"
META = "Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv"
COMPOUNDS = "Repurposing_Public_24Q2_Extended_Primary_Compound_List.csv"
for n in (MATRIX, META, COMPOUNDS):
    dl(n, files[n])

# 2. Lignées pancréatiques — jointure avec Model.csv (DepMap 24Q4, déjà vérifié) :
# PRISM ne donne pas la lignée ; Model.csv donne OncotreeLineage par ModelID.
cl = pd.read_csv(os.path.join(DATA, META))
print("colonnes métadonnées :", list(cl.columns), flush=True)
mod = pd.read_csv(os.path.join(DATA, "Model.csv"))
panc_mod = mod[mod["OncotreeLineage"] == "Pancreas"][["ModelID"]]
merged = cl.merge(panc_mod, left_on="depmap_id", right_on="ModelID", how="inner")
print("lignées pancréas PRISM (jointure Model.csv) :", len(merged), flush=True)
panc_ids = set(merged["depmap_id"])

# 3. Matrice de viabilité — lignes = composés (BRD), colonnes = lignées (ACH) :
# on transpose pour avoir les lignées en lignes.
m = pd.read_csv(os.path.join(DATA, MATRIX), index_col=0).T
print("matrice transposée :", m.shape, "(lignées x composés)", flush=True)
# orientation : lignes = lignées (ACH-...) ?
m = m[m.index.isin(panc_ids)]
print("lignées pancréas dans la matrice :", len(m), flush=True)

# 4. Axe KRAS (Chronos DepMap 24Q4, déjà vérifié)
import csv
with open(os.path.join(DATA, "CRISPRGeneEffect.csv")) as f:
    header = next(csv.reader(f))
kpos = [i for i, c in enumerate(header) if c.startswith("KRAS (")][0]
ge = pd.read_csv(os.path.join(DATA, "CRISPRGeneEffect.csv"),
                 usecols=[0, kpos], index_col=0)
ge.columns = ["KRAS"]
kras = ge["KRAS"].dropna()
common = m.index.intersection(kras.index)
print("lignées communes PRISM x DepMap KRAS :", len(common), flush=True)
m = m.loc[common]
k = kras.loc[common]

# 5. Test par composé
rows = []
for comp in m.columns:
    v = m[comp].dropna()
    if len(v) < 15:
        continue
    kk = k.loc[v.index]
    rho = v.corr(kk, method="spearman")
    tert = pd.qcut(kk, 3, labels=["faible", "moyen", "fort"])
    hi = v[tert == "fort"].mean()
    lo = v[tert == "faible"].mean()
    rows.append((comp, len(v), rho, hi - lo, hi, lo))
res = pd.DataFrame(rows, columns=["compound", "n", "spearman_kras",
                                  "delta_fort_moins_faible",
                                  "viab_kras_fort", "viab_kras_faible"])
res = res.sort_values("spearman_kras")
res.to_csv(os.path.join(DATA, "prism_kras_screen.csv"), index=False)
print("\nTOP 10 — tuent le plus les lignées KRAS-fort (rho négatif) :",
      flush=True)
print(res.head(10).round(3).to_string(index=False))
print("\nTOP 10 — épargnent les lignées KRAS-fort (rho positif) :", flush=True)
print(res.tail(10).round(3).to_string(index=False))

# 6. Noms et cibles des composés du top
comp = pd.read_csv(os.path.join(DATA, COMPOUNDS))
print("\ncolonnes composés :", list(comp.columns), flush=True)
comp.to_csv(os.path.join(DATA, "prism_compounds_saved.csv"), index=False)
top_ids = list(res.head(10)["compound"]) + list(res.tail(5)["compound"])
sub = comp[comp["IDs"].astype(str).apply(
    lambda s: any(t in s for t in top_ids))]
print(sub[["IDs", "Drug.Name", "repurposing_target", "MOA", "dose"]].to_string(index=False))
print("\nFIN PRISM", flush=True)
