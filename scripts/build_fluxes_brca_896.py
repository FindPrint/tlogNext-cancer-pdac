#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.96 bras B — construit les flux TCGA-BRCA.
Protocole gele : PROTOCOL_universalite_896.md + ADDENDUM_axe_brca_896.md
(axe ESR1, choisi apres lecture de la matrice, avant tout run).
Calque sur build_fluxes_pancancer.py (LUAD/COAD) :
- Source : Broad GDAC Firehose stddata 2016-01-28, cohorte BRCA.
- Tumeurs primaires uniquement (code TCGA 01).
- Valeurs log2(RSEM normalisé + 1).
- Ordre : expression ESR1 brute croissante. ESR1 = axe, jamais un flux.
- Flux : les 12 memes genes v4 que PAAD/LUAD/COAD (gate 12/12 passe,
  0 remplacement, 0 NaN — verifie dans ce script, arret sinon).
- Nul : memes lignes permutees, graine 42 ; nuls frais 9601, 9602.
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd

PDAC = "/home/hatch/workspace/runs/pdac-v6"
TARBALL = (f"{PDAC}/downloads_brca_896/gdac.broadinstitute.org_BRCA.Merge_"
           "rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_"
           "normalized__data.Level_3.2016012800.0.0.tar.gz")
MD5_ATTENDU = "b4eed57d14ca2fa563ca0dd05d4fba7f"
SEED = 42
MIN_VALID = 50
MIN_FLUX = 10

GENES_V4 = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
            "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]
AXE = "ESR1"


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


def build_nul(df_out, seed, suffix):
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(df_out))
    nul = df_out.copy()
    nul.iloc[:, 1:] = df_out.iloc[:, 1:].to_numpy()[perm]
    assert (nul["step"].values == df_out["step"].values).all()
    cols = [c for c in df_out.columns if c != "step"]
    assert sorted(map(tuple, nul[cols].values.tolist())) == sorted(
        map(tuple, df_out[cols].values.tolist()))
    assert not nul.isna().any().any()
    path = f"{PDAC}/pdac_brca_fluxes_nul{suffix}.csv"
    nul.to_csv(path, index=False)
    return path


def main():
    print("=== TCGA-BRCA (cancer du sein) ===")
    assert md5(TARBALL) == MD5_ATTENDU, "MD5 tarball non conforme"
    size = __import__("os").path.getsize(TARBALL)
    print(f"Tarball : {size} octets, MD5 {MD5_ATTENDU} OK")
    with tarfile.open(TARBALL, "r:gz") as tf:
        member = [m for m in tf.getmembers()
                  if m.name.endswith(".data.txt")][0]
        print(f"Fichier matrice : {member.name} ({member.size} octets)")
        f = tf.extractfile(member)
        df = pd.read_csv(f, sep="\t", index_col=0, low_memory=False)
    print(f"Matrice : {df.shape[0]} genes x {df.shape[1]} echantillons")
    df.index = df.index.to_series().str.split("|").str[0]
    df = df[~df.index.duplicated(keep="first")]
    cols = df.columns.to_series()
    tumor_cols = cols[cols.str[13:15] == "01"]
    other = cols[cols.str[13:15] != "01"]
    print(f"Tumeurs primaires (01) : {len(tumor_cols)} ; autres "
          f"({sorted(set(other.str[13:15]))}) : {len(other)}")
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    assert AXE in mat.index, "ESR1 absent de la matrice"
    logmat = np.log2(mat + 1.0)

    kept, missing, low_n = [], [], []
    for g in GENES_V4:
        if g not in logmat.index:
            missing.append(g)
        else:
            n_valid = int(logmat.loc[g].notna().sum())
            if n_valid < MIN_VALID:
                low_n.append((g, n_valid))
            else:
                kept.append(g)
    print(f"Genes v4 presents avec >={MIN_VALID} valides : {len(kept)}/12")
    if missing:
        print(f"  ABSENTS : {missing}")
    if low_n:
        print(f"  <{MIN_VALID} valides : {low_n}")
    assert len(kept) >= MIN_FLUX, f"moins de {MIN_FLUX} flux"
    assert not missing and not low_n, "gate 12/12 non passe — arret"

    axe = logmat.loc[AXE].dropna().sort_values(ascending=True)
    order = list(axe.index)
    print(f"ESR1 log2(RSEM+1) : n={len(axe)} min={axe.min():.3f} "
          f"mediane={axe.median():.3f} max={axe.max():.3f} "
          f"ecart-type={axe.std():.3f}")
    flux = logmat.loc[kept, order].T
    n_nan = int(flux.isna().sum().sum())
    print(f"NaN dans les flux : {n_nan}")
    assert n_nan == 0, "NaN dans les flux — arret, pas d'imputation"
    out = pd.DataFrame({"step": np.arange(len(flux))})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{PDAC}/pdac_brca_fluxes.csv"
    out.to_csv(out_path, index=False)
    print(f"Ecrit : {out_path} ({out.shape[0]} lignes x "
          f"{out.shape[1]} colonnes)")

    files = {}
    for seed, suffix in ((42, ""), (9601, "_s9601"), (9602, "_s9602")):
        p = build_nul(out, seed, suffix)
        files[p.split("/")[-1]] = sha(p)
        print(f"Ecrit : {p} (permutation graine {seed})")
    files["pdac_brca_fluxes.csv"] = sha(out_path)

    with open(f"{PDAC}/brca_896_download.json", "w") as f:
        json.dump({
            "cohorte": "TCGA-BRCA",
            "source": {
                "depot": "Broad GDAC Firehose stddata 2016-01-28",
                "tarball": TARBALL.split("/")[-1],
                "url": "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/BRCA/20160128/",
                "taille_octets": size,
                "md5_observe": MD5_ATTENDU,
                "matrice_interne": member.name,
                "matrice_interne_octets": member.size,
                "matrice_interne_md5": md5(f"{PDAC}/downloads_brca_896/{member.name}"),
                "matrice": f"{df.shape[0]} genes x {df.shape[1]} echantillons",
                "donnees": "RNA-seq V2 RSEM normalisé (TCGA, UNC Illumina HiSeq)",
            },
            "patients": {
                "critere": "echantillons tumoraux primaires, code TCGA 01",
                "retenus": int(len(tumor_cols)),
                "ecartes": int(len(other)),
                "transformation": "log2(RSEM normalisé + 1)",
            },
            "genes": {"demandes_v4": GENES_V4, "retenus": kept,
                      "absents": missing, "moins_de_50_valides": low_n,
                      "remplacement_effectue": None},
            "axe": {"gene": AXE, "n": int(len(axe)),
                    "min": round(float(axe.min()), 4),
                    "mediane": round(float(axe.median()), 4),
                    "max": round(float(axe.max()), 4),
                    "ecart_type": round(float(axe.std()), 4),
                    "choix": "ADDENDUM_axe_brca_896.md (ESR1, apres lecture "
                             "de la matrice, avant tout run)"},
            "ordre": "expression ESR1 brute croissante ; ESR1 = axe, jamais un flux",
            "fichiers_sha256": files,
        }, f, indent=2, ensure_ascii=False)
    print("Provenance ecrite : brca_896_download.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
