#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construction des flux TCGA-GBM (§8.82).
Protocole gelé : PROTOCOL_cerveau_privilege_882.md (21 nov. 2026), avant
tout run et toute analyse.
- Source : Broad GDAC Firehose stddata 2016-01-28, GBM, RSEM genes
  normalized (même route que PAAD/LUAD/COAD). Tarball déjà téléchargé et
  MD5 vérifié avant le gel : cfc6cf0a2c3c2e9f0ea7a11f2ba32d28.
- Tumeurs primaires (code TCGA 01) uniquement ; log2(RSEM normalisé + 1).
- Aucune correction de pureté (scores acineux/îlots spécifiques au
  pancréas). Aucune imputation.
- Ordre PRIMAIRE : score de prolifération croissant (moyenne log2 des
  6 gènes gelés MKI67, TOP2A, PCNA, CCNB1, BUB1, AURKB).
- Ordre SECONDAIRE : score de privilège croissant (moyenne des z-scores
  des 7 gènes FASLG, TGFB1, TGFB2, IDO1, HLA-G, CD47, CD274).
- Flux FIXÉS : les 12 mêmes gènes v4 que le pancréas (PGC, REG4, CLDN18,
  MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16).
- Nuls : mêmes lignes permutées, graine 42.
- Contrôle anti-doublon (§8.44) : le contrôle du pipeline est la colonne
  `step` ; ni le score de prolifération ni le score de privilège ne sont
  parmi les 12 flux analysés (assertions ci-dessous).
- Minimum 40 cas complets, sinon ARRÊT.
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd

BASE = "/home/hatch/workspace/runs/pdac-v6"
DATA = f"{BASE}/data"
OUT = BASE
TARBALL = f"{DATA}/tcga_gbm_rsem.tar.gz"
TARBALL_MD5 = "cfc6cf0a2c3c2e9f0ea7a11f2ba32d28"
SEED = 42
MIN_CASES = 40

GENES_V4 = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
            "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]
PRIV = ["FASLG", "TGFB1", "TGFB2", "IDO1", "HLA-G", "CD47", "CD274"]
PROLIF = ["MKI67", "TOP2A", "PCNA", "CCNB1", "BUB1", "AURKB"]
IMM = ["CD8A", "CD8B", "CD4", "FOXP3", "CD68", "CD163", "CD274",
       "PDCD1", "CTLA4", "GZMB", "IFNG", "CD19"]


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
    assert md5(TARBALL) == TARBALL_MD5, "MD5 du tarball GBM non conforme"
    with tarfile.open(TARBALL, "r:gz") as tf:
        member = [m for m in tf.getmembers()
                  if m.name.endswith(".data.txt")][0]
        print(f"Fichier matrice : {member.name} ({member.size} octets)")
        f = tf.extractfile(member)
        df = pd.read_csv(f, sep="\t", index_col=0, low_memory=False)
    print(f"Matrice : {df.shape[0]} gènes x {df.shape[1]} échantillons")
    df.index = df.index.to_series().str.split("|").str[0]
    df = df[~df.index.duplicated(keep="first")]
    cols = df.columns.to_series()
    tumor_cols = cols[cols.str[13:15] == "01"]
    other = cols[cols.str[13:15] != "01"]
    print(f"Tumeurs primaires (01) : {len(tumor_cols)} ; autres "
          f"({sorted(set(other.str[13:15]))}) : {len(other)}")
    mat = df[tumor_cols].apply(pd.to_numeric, errors="coerce")
    logmat = np.log2(mat + 1.0)

    # Présence des gènes (aucun remplacement prévu ; règle §8.27 sinon).
    for name, genes in [("v4", GENES_V4), ("privilège", PRIV),
                        ("prolifération", PROLIF), ("immunitaire", IMM)]:
        missing = [g for g in genes if g not in logmat.index]
        print(f"Gènes {name} : {len(genes) - len(missing)}/{len(genes)} "
              f"présents" + (f" ; ABSENTS : {missing}" if missing else ""))
    kept_v4 = [g for g in GENES_V4 if g in logmat.index]
    assert len(kept_v4) >= 10, "moins de 10 flux v4 : ARRÊT"
    # Anti-doublon : le contrôle (step / scores) n'est jamais un flux.
    assert not set(PROLIF) & set(kept_v4)
    assert not set(PRIV) & set(kept_v4)

    # Scores (définitions gelées §2 du protocole).
    prolif_score = logmat.loc[PROLIF].mean(axis=0)

    def zscore(s):
        return (s - s.mean()) / s.std(ddof=0)

    priv_z = pd.DataFrame({g: zscore(logmat.loc[g]) for g in PRIV})
    priv_score = priv_z.mean(axis=1)
    cold_genes = ["CD8A", "CD4", "FOXP3", "PDCD1"]
    cold_z = pd.DataFrame({g: zscore(logmat.loc[g]) for g in cold_genes})
    cold_score = cold_z.mean(axis=1)

    # Cas complets.
    need = list(set(kept_v4 + PRIV + PROLIF + IMM))
    sub = logmat.loc[need]
    complete = sub.columns[~sub.isna().any(axis=0)]
    print(f"Cas complets : {len(complete)} / {len(tumor_cols)}")
    assert len(complete) >= MIN_CASES, "moins de 40 cas complets : ARRÊT"
    logmat = logmat[complete]
    prolif_score = prolif_score[complete]
    priv_score = priv_score[complete]
    cold_score = cold_score[complete]
    print(f"Score prolifération : min={prolif_score.min():.3f} "
          f"médiane={prolif_score.median():.3f} max={prolif_score.max():.3f}")
    print(f"Score privilège : min={priv_score.min():.3f} "
          f"médiane={priv_score.median():.3f} max={priv_score.max():.3f}")
    print(f"Score froid : min={cold_score.min():.3f} "
          f"médiane={cold_score.median():.3f} max={cold_score.max():.3f}")

    provenance = {
        "date": "2026-11-21",
        "protocole": "PROTOCOL_cerveau_privilege_882.md",
        "source": {
            "dépôt": "Broad GDAC Firehose stddata 2016-01-28, GBM",
            "fichier": member.name.split("/")[-1],
            "url": "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/"
                   "data/GBM/20160128/",
            "fichier_local": TARBALL,
            "taille_octets": __import__("os").path.getsize(TARBALL),
            "md5_observé": TARBALL_MD5,
            "sha256": sha(TARBALL),
            "matrice_interne": member.name,
            "matrice": f"{df.shape[0]} gènes x {df.shape[1]} échantillons",
            "données": "RNA-seq V2 RSEM normalisé (TCGA, UNC Illumina HiSeq)",
        },
        "patients": {
            "critère": "échantillons tumoraux primaires, code TCGA 01",
            "retenus": int(len(tumor_cols)),
            "écartés": int(len(other)),
            "cas_complets": int(len(complete)),
            "transformation": "log2(RSEM normalisé + 1)",
            "correction_pureté": "aucune (scores acineux/îlots spécifiques "
                                 "au pancréas)",
        },
        "axes": {
            "prolifération": {"gènes": PROLIF,
                              "définition": "moyenne log2(RSEM+1) par patient"},
            "privilège": {"gènes": PRIV,
                          "définition": "moyenne des z-scores (dans la "
                                        "cohorte GBM) par patient"},
            "froid": {"gènes": cold_genes,
                      "définition": "moyenne des z-scores (dans la cohorte "
                                    "GBM) par patient"},
            "grade": "non utilisable : tous les TCGA-GBM sont WHO grade IV "
                     "par définition de la cohorte",
        },
        "gènes_v4_retenus": kept_v4,
        "anti_doublon": "contrôle = colonne step ; scores de prolifération "
                        "et de privilège absents des 12 flux (vérifié par "
                        "assertion)",
    }

    def write_fluxes(order, tag):
        flux = logmat.loc[kept_v4, order].T
        assert int(flux.isna().sum().sum()) == 0, f"NaN dans les flux {tag}"
        out = pd.DataFrame({"step": np.arange(len(flux))})
        out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
        out_path = f"{OUT}/pdac_882_gbm_{tag}_fluxes.csv"
        out.to_csv(out_path, index=False)
        print(f"Écrit : {out_path} ({out.shape[0]} lignes x "
              f"{out.shape[1]} colonnes)")
        rng = np.random.default_rng(SEED)
        perm = rng.permutation(len(out))
        nul = out.copy()
        nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
        nul_path = f"{OUT}/pdac_882_gbm_{tag}_fluxes_nul.csv"
        nul.to_csv(nul_path, index=False)
        print(f"Écrit : {nul_path} (permutation graine {SEED})")
        provenance[tag] = {
            "ordre": ("score de prolifération croissant" if tag == "prolif"
                      else "score de privilège croissant"),
            "flux_csv": {"fichier": out_path, "sha256": sha(out_path),
                         "lignes": int(out.shape[0]),
                         "colonnes": list(out.columns)},
            "nul_csv": {"fichier": nul_path, "sha256": sha(nul_path),
                        "méthode": "mêmes lignes permutées, graine 42"},
        }
        return out_path

    order_prolif = list(prolif_score.sort_values(ascending=True).index)
    order_priv = list(priv_score.sort_values(ascending=True).index)
    write_fluxes(order_prolif, "prolif")
    write_fluxes(order_priv, "privilege")

    # Table directe (ordre prolifération) : scores + tous les gènes.
    direct = pd.DataFrame({
        "step": np.arange(len(order_prolif)),
        "sample": order_prolif,
        "score_prolif": prolif_score[order_prolif].values,
        "score_privilege": priv_score[order_prolif].values,
        "score_froid": cold_score[order_prolif].values,
    })
    for g in PRIV + IMM + kept_v4:
        direct[g] = logmat.loc[g, order_prolif].values
    direct["KRAS"] = logmat.loc["KRAS", order_prolif].values
    direct_path = f"{OUT}/gbm_882_direct_table.csv"
    direct.to_csv(direct_path, index=False)
    print(f"Écrit : {direct_path} ({direct.shape[0]} lignes)")
    provenance["table_directe"] = {"fichier": direct_path,
                                    "sha256": sha(direct_path),
                                    "lignes": int(direct.shape[0]),
                                    "colonnes": list(direct.columns),
                                    "ordre": "score de prolifération "
                                             "croissant"}

    with open(f"{OUT}/PROVENANCE_882.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — §8.82 Cerveau, TCGA-GBM (Firehose)\n\n")
        f.write("```json\n"
                + json.dumps(provenance, indent=2, ensure_ascii=False)
                + "\n```\n")
    print("Provenance écrite : PROVENANCE_882.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
