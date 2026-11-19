#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Table lignée x mutations pour les lignées pancréas DepMap 24Q4.
Préparation seulement (18 nov. 2026) : AUCUN run pipeline, AUCUN CSV de flux
modifié, AUCUNE série construite. Sert le §8.33 du livre blanc : la jointure
PR -> ACH n'était pas construite, donc le « 0 mutation » brut était un
artefact de jointure absente, pas une mesure.

Entrées (déjà sur le disque, SHA256 calculés et consignés dans la sortie) :
- runs/pdac-v6/data/Model.csv (DepMap 24Q4)
- runs/pdac-v6/data/CRISPRGeneEffect.csv (DepMap 24Q4)
- runs/pdac-v6/data/OmicsProfiles.csv (ProfileID PR-... -> ModelID ACH-...)
- runs/pdac-v6/data/OmicsSomaticMutationsMAFProfile.maf (DepMap 24Q4)
- runs/pdac-v6/data/kras_alleles_pancreas.csv (54 lignées, §8.20)
Sortie : runs/pdac-v6/data/mutation_table_pancreas.csv
  une ligne par lignée pancréas (n=45, même définition que
  build_fluxes_depmap.py : OncotreePrimaryDisease == 'Pancreatic
  Adenocarcinoma' dans Model.csv ET présente dans CRISPRGeneEffect.csv).
  Colonnes : ModelID, CellLineName, KRAS_allele,
  TP53_mut, SMAD4_mut, CDKN2A_mut, KRAS_mut (statut MAF),
  avec pour chaque gène la liste des Variant_Classification observées
  (ex. Missense_Mutation) ou 'absent' si aucune ligne MAF.
  'mut' = au moins une ligne MAF non silencieuse pour le gène
  (Silent exclu ; tout le reste compté, classifications listées).
"""
import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path("/home/hatch/workspace/runs/pdac-v6")
DATA = BASE / "data"
GENES = ["TP53", "SMAD4", "CDKN2A", "KRAS"]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    import pandas as pd

    model = pd.read_csv(DATA / "Model.csv", low_memory=False)
    panc_ids = model.loc[
        model["OncotreePrimaryDisease"] == "Pancreatic Adenocarcinoma",
        ["ModelID", "CellLineName"],
    ].drop_duplicates("ModelID")
    ge = pd.read_csv(DATA / "CRISPRGeneEffect.csv", index_col=0, usecols=[0])
    panc = panc_ids[panc_ids["ModelID"].isin(ge.index)].sort_values("ModelID")
    print(f"lignées pancréas retenues : {len(panc)}")
    assert len(panc) == 45, f"attendu 45, obtenu {len(panc)}"

    profiles = pd.read_csv(DATA / "OmicsProfiles.csv", low_memory=False)
    pr_to_ach = dict(zip(profiles["ProfileID"], profiles["ModelID"]))
    assert profiles["ProfileID"].is_unique, "ProfileID non unique"
    print(f"profils : {len(profiles)}, ModelID uniques : "
          f"{profiles['ModelID'].nunique()}")

    alleles = {}
    with open(DATA / "kras_alleles_pancreas.csv", newline="") as f:
        for row in csv.DictReader(f):
            alleles[row["ModelID"]] = row["Protein_Change"]

    # MAF : une seule passe, on ne garde que les 4 gènes + les PR pancréas.
    panc_set = set(panc["ModelID"])
    muts = defaultdict(lambda: defaultdict(list))  # ModelID -> gène -> [classifications]
    n_maf_rows = 0
    n_pr_unmatched = 0
    with open(DATA / "OmicsSomaticMutationsMAFProfile.maf", newline="") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            if row["Hugo_Symbol"] not in GENES:
                continue
            n_maf_rows += 1
            ach = pr_to_ach.get(row["Tumor_Sample_Barcode"])
            if ach is None:
                n_pr_unmatched += 1
                continue
            if ach not in panc_set:
                continue
            if row["Variant_Classification"] == "Silent":
                continue
            muts[ach][row["Hugo_Symbol"]].append(row["Variant_Classification"])
    print(f"lignes MAF pour les 4 gènes : {n_maf_rows}, "
          f"PR sans profil : {n_pr_unmatched}")

    out = DATA / "mutation_table_pancreas.csv"
    hashes = {name: sha(DATA / name) for name in
              ["Model.csv", "CRISPRGeneEffect.csv", "OmicsProfiles.csv",
               "OmicsSomaticMutationsMAFProfile.maf",
               "kras_alleles_pancreas.csv"]}
    with open(out, "w", newline="") as f:
        f.write("# Table lignée x mutations, lignées pancréas DepMap 24Q4\n")
        f.write("# Préparation 18 nov. 2026, §8.33 livre blanc — aucun run, "
                "aucun flux modifié.\n")
        for name, h in hashes.items():
            f.write(f"# SHA256 {name} : {h}\n")
        f.write("# mut=1 si >=1 ligne MAF non silencieuse ; "
                "classes = Variant_Classification listées, 'absent' sinon.\n")
        w = csv.writer(f)
        w.writerow(["ModelID", "CellLineName", "KRAS_allele"] +
                   [f"{g}_mut" for g in GENES] +
                   [f"{g}_classes" for g in GENES])
        for _, line in panc.iterrows():
            mid = line["ModelID"]
            w.writerow([mid, line["CellLineName"],
                        alleles.get(mid, "inconnu")] +
                       [1 if muts[mid][g] else 0 for g in GENES] +
                       [";".join(sorted(set(muts[mid][g]))) or "absent"
                        for g in GENES])
    counts = Counter()
    for mid in panc["ModelID"]:
        for g in GENES:
            counts[g] += 1 if muts[mid][g] else 0
    print("mutées /45 :", dict(counts))
    print(f"écrit : {out}")


if __name__ == "__main__":
    main()
