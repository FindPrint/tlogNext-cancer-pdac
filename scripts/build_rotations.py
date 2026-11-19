#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rotations de contrôle sur les flux v4 (TCGA-PAAD, 15 nov. 2026).
Règle permanente : chaque flux / chaque axe doit être testé comme contrôle
à tour de rôle — un seul contrôle n'est jamais un objectif.
La v4 a été lue avec le contrôle step (ordre = résidu KRAS croissant).
On teste ici 4 autres axes, mêmes 12 flux, mêmes 178 patients :
  v4r_krasval : contrôle = valeur du résidu KRAS (même ordre, métrique réelle
                 au lieu du rang uniforme step).
  v4r_cldn18  : contrôle = CLDN18 (résidu) ; lignes triées par CLDN18 croissant.
  v4r_purity  : contrôle = score acineux (pureté) ; lignes triées par pureté
                 croissante. Témoin négatif : la v4 a enlevé la pureté, la
                 chaîne tumorale ne devrait PAS réapparaître ici.
  v4r_krasdesc: contrôle = step, lignes en ordre KRAS DÉCROISSANT (miroir).
Nul de chaque rotation : mêmes lignes permutées (graine 42), colonne de
contrôle intacte. La colonne de contrôle est toujours la 1re colonne.
Les valeurs KRAS-résidu et score acineux sont recalculées exactement comme
dans build_fluxes_tcga_v4.py (même tarball, MD5 vérifié) — la v4 reste
intacte, SHA inchangé.
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
TARBALL = f"{DATA}/tcga_paad_rsem.tar.gz"
TARBALL_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
SEED = 42

ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]
ISLET = ["INS", "GCG", "PPY", "SST"]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    assert md5(TARBALL) == TARBALL_MD5, "MD5 du tarball non conforme"
    with tarfile.open(TARBALL, "r:gz") as tf:
        member = [m for m in tf.getmembers() if m.name.endswith(".data.txt")][0]
        f = tf.extractfile(member)
        df = pd.read_csv(f, sep="\t", index_col=0, low_memory=False)
    df.index = df.index.to_series().str.split("|").str[0]
    df = df[~df.index.duplicated(keep="first")]
    cols = df.columns.to_series()
    tumor_cols = cols[cols.str[13:15] == "01"]
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    mat = mat[~mat.isna().any(axis=1)]
    logmat = np.log2(mat + 1.0)

    acinar_present = [g for g in ACINAR if g in logmat.index]
    islet_present = [g for g in ISLET if g in logmat.index]
    score_ac = logmat.loc[acinar_present].median(axis=0)
    score_is = logmat.loc[islet_present].median(axis=0)
    X = np.column_stack([np.ones(len(logmat.columns)), score_ac.values,
                         score_is.values])
    Y = logmat.values
    beta, *_ = np.linalg.lstsq(X, Y.T, rcond=None)
    fitted = (X @ beta).T
    resid = Y - fitted
    resid_df = pd.DataFrame(resid, index=logmat.index, columns=logmat.columns)

    # Flux v4 existants — vérification que l'ordre recalculé est identique.
    v4 = pd.read_csv(f"{OUT}/pdac_tcga_fluxes_v4.csv")
    kras_res = resid_df.loc["KRAS"].sort_values(ascending=True)
    order = list(kras_res.index)
    flux_cols = list(v4.columns[1:])
    check = resid_df.loc[flux_cols, order].T.reset_index(drop=True)
    assert np.allclose(check.values, v4[flux_cols].values, atol=1e-9), \
        "ordre v4 non reproduit — ARRÊT"
    print("Ordre v4 reproduit exactement. Flux :", flux_cols)

    # Séries d'axe alignées sur l'ordre v4 (résidu KRAS croissant).
    kras_val = kras_res.values  # déjà trié croissant
    purity = score_ac.loc[order].values
    print(f"Résidu KRAS : min={kras_val.min():+.3f} médiane={np.median(kras_val):+.3f} "
          f"max={kras_val.max():+.3f}")
    print(f"Score acineux : min={purity.min():.2f} médiane={np.median(purity):.2f} "
          f"max={purity.max():.2f}")

    rng = np.random.default_rng(SEED)
    prov = {}

    def write_variant(tag, control_name, control_vals, flux_df):
        """flux_df : DataFrame des 12 flux, lignes dans l'ordre du contrôle."""
        out = pd.DataFrame({control_name: control_vals})
        out = pd.concat([out, flux_df.reset_index(drop=True)], axis=1)
        path = f"{OUT}/pdac_tcga_fluxes_{tag}.csv"
        out.to_csv(path, index=False)
        perm = rng.permutation(len(out))
        nul = out.copy()
        nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
        nul_path = f"{OUT}/pdac_tcga_fluxes_{tag}_nul.csv"
        nul.to_csv(nul_path, index=False)
        prov[tag] = {"contrôle": control_name,
                     "fichier": path, "sha256": sha(path),
                     "nul": nul_path, "sha256_nul": sha(nul_path),
                     "lignes": int(out.shape[0])}
        print(f"Écrit : {tag} ({out.shape[0]} lignes, contrôle {control_name})")

    base = v4[flux_cols]  # ordre résidu KRAS croissant

    # 1. Même ordre, contrôle = valeur du résidu KRAS.
    write_variant("v4r_krasval", "KRAS_resid", kras_val, base)

    # 2. Contrôle = CLDN18 ; lignes triées par CLDN18 croissant.
    o2 = base["CLDN18"].sort_values(ascending=True).index
    write_variant("v4r_cldn18", "CLDN18",
                  base.loc[o2, "CLDN18"].values, base.loc[o2].reset_index(drop=True))

    # 3. Contrôle = pureté (score acineux) ; lignes triées par pureté croissante.
    o3 = np.argsort(purity)
    write_variant("v4r_purity", "score_acineux", purity[o3],
                  base.iloc[o3].reset_index(drop=True))

    # 4. Miroir : ordre KRAS décroissant, contrôle step.
    rev = base.iloc[::-1].reset_index(drop=True)
    out = pd.DataFrame({"step": np.arange(len(rev))})
    out = pd.concat([out, rev], axis=1)
    path = f"{OUT}/pdac_tcga_fluxes_v4r_krasdesc.csv"
    out.to_csv(path, index=False)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_tcga_fluxes_v4r_krasdesc_nul.csv"
    nul.to_csv(nul_path, index=False)
    prov["v4r_krasdesc"] = {"contrôle": "step (ordre KRAS décroissant)",
                            "fichier": path, "sha256": sha(path),
                            "nul": nul_path, "sha256_nul": sha(nul_path),
                            "lignes": int(out.shape[0])}
    print("Écrit : v4r_krasdesc (miroir, ordre KRAS décroissant)")

    with open(f"{OUT}/PROVENANCE_rotations.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — rotations de contrôle sur la v4 (TCGA-PAAD)\n\n")
        f.write("```json\n" + json.dumps(
            {"date": "2026-11-15",
             "base": "flux v4 (178 patients, 12 flux tumoraux, PROVENANCE_tcga_v4.md) ; "
                     "la v4 reste intacte",
             "source": "Broad GDAC Firehose 2016-01-28, tarball MD5 vérifié "
                       "b09569ce3f4721f514bc137bd109ac0a",
             "rotations": prov}, indent=2, ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_rotations.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
