#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bras 2 pan-cancer — construit les flux TCGA-LUAD et TCGA-COAD.
Protocole gelé : PROTOCOL_pancancer.md (16 nov. 2026), avant tout run.
- Source : Broad GDAC Firehose stddata 2016-01-28, même route que PAAD.
- Tumeurs primaires uniquement (code TCGA 01).
- Valeurs log2(RSEM normalisé + 1).
- Ordre : expression KRAS brute croissante. KRAS = axe, jamais un flux.
- Flux FIXÉS par la question (les 12 mêmes gènes v4 que le pancréas) :
  PGC, REG4, CLDN18, MUC17, DPCR1, CR2, KRT20, MUC2, GSTM1, CEACAM5, CLCA1, MUC16.
  Pas de re-sélection par variance, pas de correction de pureté (scores
  acineux/îlots spécifiques au pancréas).
- Règle ≥ 50 valeurs valides par gène, jamais d'imputation. Remplacement :
  liste v3 hors gènes de sexe = PGC, REG4, CLDN18, MUC17, DPCR1 — tous déjà
  dans les 12, donc aucun remplacement sensé n'existe ; si un gène manque,
  procéder avec les flux restants (minimum 10) et le documenter.
- Nul : mêmes lignes permutées, graine 42.
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
SEED = 42
MIN_VALID = 50
MIN_FLUX = 10

GENES_V4 = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
            "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]
# Liste v3 hors gènes de sexe (déjà écartés en v4) — tous déjà dans GENES_V4.
V3_NON_SEX = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1"]

COHORTS = {
    "luad": {"tarball": f"{DATA}/tcga_luad_rsem.tar.gz",
             "md5": "4c36eec3f6df75630292c5a569cfc8f4",
             "label": "TCGA-LUAD (adénocarcinome pulmonaire)"},
    "coad": {"tarball": f"{DATA}/tcga_coad_rsem.tar.gz",
             "md5": "e703a630556d42f098cf0df87d4712bb",
             "label": "TCGA-COAD (colorectal)"},
}


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
    provenance = {"date": "2026-11-16", "protocole": "PROTOCOL_pancancer.md",
                  "cohortes": {}}
    for tag, cfg in COHORTS.items():
        print(f"=== {cfg['label']} ===")
        assert md5(cfg["tarball"]) == cfg["md5"], f"MD5 non conforme : {tag}"
        size = __import__("os").path.getsize(cfg["tarball"])
        with tarfile.open(cfg["tarball"], "r:gz") as tf:
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
        assert "KRAS" in mat.index, "KRAS absent de la matrice"
        logmat = np.log2(mat + 1.0)

        # Vérification des 12 gènes : présence + ≥50 valeurs valides.
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
        print(f"Gènes v4 présents avec ≥{MIN_VALID} valides : {len(kept)}/12")
        if missing:
            print(f"  ABSENTS : {missing}")
        if low_n:
            print(f"  <{MIN_VALID} valides : {low_n}")
        # Remplacements possibles : liste v3 hors sexe, hors gènes déjà là.
        candidates = [g for g in V3_NON_SEX if g not in kept]
        print(f"Remplacements possibles (v3 hors sexe, non déjà présents) : "
              f"{candidates if candidates else 'AUCUN — tous déjà dans les 12'}")
        assert len(kept) >= MIN_FLUX, f"moins de {MIN_FLUX} flux : {tag}"
        if missing or low_n:
            print("  -> on procède avec les flux restants, sans imputation.")

        kras = logmat.loc["KRAS"].dropna().sort_values(ascending=True)
        order = list(kras.index)
        print(f"KRAS log2(RSEM+1) : n={len(kras)} min={kras.min():.3f} "
              f"médiane={kras.median():.3f} max={kras.max():.3f}")
        flux = logmat.loc[kept, order].T
        # Jamais d'imputation : si un NaN subsiste dans les flux, on le signale.
        n_nan = int(flux.isna().sum().sum())
        print(f"NaN dans les flux : {n_nan}")
        assert n_nan == 0, "NaN dans les flux — arrêt, pas d'imputation"
        out = pd.DataFrame({"step": np.arange(len(flux))})
        out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
        out_path = f"{OUT}/pdac_{tag}_fluxes.csv"
        out.to_csv(out_path, index=False)
        print(f"Écrit : {out_path} ({out.shape[0]} lignes x "
              f"{out.shape[1]} colonnes)")

        rng = np.random.default_rng(SEED)
        perm = rng.permutation(len(out))
        nul = out.copy()
        nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
        nul_path = f"{OUT}/pdac_{tag}_fluxes_nul.csv"
        nul.to_csv(nul_path, index=False)
        print(f"Écrit : {nul_path} (permutation graine {SEED})")

        provenance["cohortes"][tag] = {
            "label": cfg["label"],
            "source": {
                "dépôt": "Broad GDAC Firehose stddata 2016-01-28",
                "fichier": member.name.split("/")[-1],
                "url": "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/"
                       f"data/{tag.upper()}/20160128/",
                "taille_octets": size,
                "md5_observé": cfg["md5"],
                "matrice_interne": member.name,
                "matrice": f"{df.shape[0]} gènes x {df.shape[1]} échantillons",
                "données": "RNA-seq V2 RSEM normalisé (TCGA, UNC Illumina HiSeq)",
            },
            "patients": {
                "critère": "échantillons tumoraux primaires, code TCGA 01",
                "retenus": int(len(tumor_cols)),
                "écartés": int(len(other)),
                "transformation": "log2(RSEM normalisé + 1)",
            },
            "gènes": {
                "demandés_v4": GENES_V4,
                "retenus": kept,
                "absents": missing,
                "moins_de_50_valides": low_n,
                "remplacements_v3_hors_sexe_disponibles": candidates,
                "remplacement_effectué": None,
            },
            "KRAS_log2": {"n": int(len(kras)),
                          "min": round(float(kras.min()), 4),
                          "médiane": round(float(kras.median()), 4),
                          "max": round(float(kras.max()), 4)},
            "ordre": "expression KRAS brute croissante ; KRAS = axe, jamais un flux",
            "flux_csv": {"fichier": out_path, "sha256": sha(out_path),
                         "lignes": int(out.shape[0]),
                         "colonnes": list(out.columns)},
            "nul_csv": {"fichier": nul_path, "sha256": sha(nul_path),
                        "méthode": "mêmes lignes permutées, graine 42"},
        }
    with open(f"{OUT}/PROVENANCE_pancancer.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — Bras 2 pan-cancer (TCGA-LUAD, TCGA-COAD, Firehose)\n\n")
        f.write("```json\n" + json.dumps(provenance, indent=2, ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_pancancer.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
