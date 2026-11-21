#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construction des flux §8.86 — GSE194249, variante (a).
Protocole PROTOCOL_gse194249_886.md (SHA b620238b…), gelé AVANT le
téléchargement. Matrice : data/GSE194249_PDPCOs_FPKM.txt.gz (FPKM
déposées, aucune transformation, aucune renormalisation).
Règles gelées appliquées ici :
- mise en page (A) : col1 = symbole de gène exact ; sinon ARRÊT ;
- symboles dupliqués agrégés par médiane ;
- colonnes NPC-* (normaux) EXCLUES et comptées ; colonnes retenues
  = PDPCOs (attendu 84) ;
- 12 gènes v4 + KRAS au symbole exact ; DPCR1 exigé exact, aucun
  remappage vers MUCL3 (présence de MUCL3 rapportée descriptivement
  seulement) ;
- ordre = KRAS FPKM croissant ; step = rang ; cas complets seulement ;
- nul = permutation des lignes, graine 42 (ou --nul-seed), contrôle intact.
Usage : python3 build_fluxes_886.py [--nul-seed 42]
Sorties : pdac_886_gse194249_fluxes.csv (+ _nul.csv),
build_fluxes_886_audit.json (+ résumé stdout).
"""
import argparse
import hashlib
import json
import os

import numpy as np
import pandas as pd

PDAC = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(PDAC, "data", "GSE194249_PDPCOs_FPKM.txt.gz")
ESUMMARY = os.path.join(PDAC, "gse194249_esummary_886.json")
V4 = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "CR2", "KRT20",
      "MUC2", "GSTM1", "CEACAM5", "CLCA1", "MUC16"]
CONTROL = "KRAS"
AUDIT = os.path.join(PDAC, "build_fluxes_886_audit.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nul-seed", type=int, default=42)
    args = ap.parse_args()

    # --- Titres GSM attendus (esummary pré-gel, métadonnées) ---
    with open(ESUMMARY) as f:
        esum = json.load(f)
    samples = esum["result"]["200194249"]["samples"]
    titre_par_gsm = {s["accession"]: s["title"] for s in samples}
    titre_attendu = {s["title"] for s in samples}

    # --- Lecture matrice (mise en page (A) attendue) ---
    df = pd.read_csv(MATRIX, sep="\t")
    cols = list(df.columns)
    assert cols[0] == "GeneSymbol", f"mise en page non (A) : col1={cols[0]!r} — ARRÊT (§3)"
    echantillons = cols[1:]
    audit = {
        "matrice": "data/GSE194249_PDPCOs_FPKM.txt.gz",
        "matrice_sha256": sha256(MATRIX),
        "matrice_taille_octets": os.path.getsize(MATRIX),
        "n_lignes_fichier": len(df) + 1,
        "n_lignes_genes": len(df),
        "n_colonnes_total": len(cols),
        "n_colonnes_echantillons": len(echantillons),
        "mise_en_page": "A (col1=GeneSymbol)",
    }
    titres_inattendus = [c for c in echantillons if c not in titre_attendu]
    titres_manquants = sorted(titre_attendu - set(echantillons))
    audit["titres_inattendus"] = titres_inattendus
    audit["titres_esummary_absents_matrice"] = titres_manquants
    print(f"matrice : {len(df)} lignes gènes, {len(echantillons)} colonnes échantillons")
    print(f"titres inattendus : {titres_inattendus} ; titres esummary absents : {titres_manquants}")

    # --- Exclusion des normaux NPC-* ---
    normaux = [c for c in echantillons if c.startswith("NPC-")]
    pdpco = [c for c in echantillons if not c.startswith("NPC-")]
    audit["colonnes_normales_NPC_exclues"] = normaux
    audit["n_normaux_exclus"] = len(normaux)
    audit["n_pdpco_retenus"] = len(pdpco)
    print(f"normaux exclus ({len(normaux)}) : {normaux}")
    print(f"PDPCO retenus : {len(pdpco)}")

    # --- Symboles : doublons -> médiane ; présence des 13 gènes ---
    df = df.set_index("GeneSymbol")
    dup = df.index[df.index.duplicated(keep=False)]
    audit["n_symboles_dupliques_lignes"] = int(len(dup))
    audit["symboles_dupliques"] = sorted(set(dup.tolist()))
    df = df.groupby(level=0).median(numeric_only=True)
    audit["n_genes_uniques_apres_agregation"] = int(len(df))
    print(f"lignes dupliquées : {len(dup)} (symboles : {sorted(set(dup.tolist()))[:10]}) ; "
          f"gènes uniques après médiane : {len(df)}")

    utiles = V4 + [CONTROL]
    presence = {}
    for g in utiles:
        presence[g] = bool(g in df.index)
    audit["presence_13_genes"] = presence
    audit["genes_absents"] = [g for g in utiles if not presence[g]]
    audit["MUCL3_present_descriptif"] = bool("MUCL3" in df.index)
    print(f"présence 13 gènes : {presence}")
    print(f"absents : {audit['genes_absents']} ; MUCL3 présent (descriptif) : {audit['MUCL3_present_descriptif']}")
    if audit["genes_absents"]:
        with open(AUDIT, "w") as f:
            json.dump(audit, f, indent=2, ensure_ascii=False)
        raise SystemExit(f"ARRÊT (§3) : gènes absents {audit['genes_absents']} — aucune construction, aucun run.")

    # --- Sous-matrice PDPCO × 13 gènes ; complétude ; KRAS ---
    sub = df.loc[utiles, pdpco].T  # lignes = lignées, colonnes = gènes
    audit["n_nan_total_13xN"] = int(sub.isna().sum().sum())
    audit["nan_par_gene"] = {g: int(sub[g].isna().sum()) for g in utiles}
    complet = sub.dropna()
    audit["n_cas_complets"] = int(len(complet))
    audit["n_cas_incomplets_exclus"] = int(len(sub) - len(complet))
    kras = complet[CONTROL].astype(float)
    audit["KRAS_FPKM_min"] = float(kras.min())
    audit["KRAS_FPKM_mediane"] = float(kras.median())
    audit["KRAS_FPKM_max"] = float(kras.max())
    audit["KRAS_FPKM_zero_ou_negatif"] = int((kras <= 0).sum())
    print(f"NaN total : {audit['n_nan_total_13xN']} ; cas complets : {len(complet)}/{len(sub)}")
    print(f"KRAS FPKM : min {kras.min():.4f} médiane {kras.median():.4f} max {kras.max():.4f} ; ≤0 : {(kras <= 0).sum()}")
    if len(complet) < 40:
        with open(AUDIT, "w") as f:
            json.dump(audit, f, indent=2, ensure_ascii=False)
        raise SystemExit(f"ARRÊT (§3) : cas complets {len(complet)} < 40.")

    # --- Composition histologique des retenus (titres) ---
    def histo(t):
        if t.startswith("CAS-DAC-"):
            return "PDAC"
        if t.startswith("CAS-NEN-"):
            return "NEN"
        if t.startswith("CAS-IPMN-"):
            return "IPMN"
        if t.startswith("CAS-ACC-"):
            return "ACC"
        return "autre"
    comp = {}
    for t in pdpco:
        comp[histo(t)] = comp.get(histo(t), 0) + 1
    audit["composition_histologique_retenus"] = comp
    print(f"composition retenus : {comp}")

    # --- Série réelle : tri KRAS croissant, step = rang ---
    ordre = complet.sort_values(CONTROL, kind="mergesort")
    reel = pd.DataFrame({"step": np.arange(len(ordre))})
    for g in V4:
        reel[g] = ordre[g].to_numpy(dtype=float)
    reel_path = os.path.join(PDAC, "pdac_886_gse194249_fluxes.csv")
    reel.to_csv(reel_path, index=False)
    audit["csv_reel"] = "pdac_886_gse194249_fluxes.csv"
    audit["csv_reel_sha256"] = sha256(reel_path)
    audit["csv_reel_shape"] = list(reel.shape)

    # --- Nul : permutation des lignes, graine gelée, contrôle intact ---
    rng = np.random.default_rng(args.nul_seed)
    perm = rng.permutation(len(reel))
    nul = reel.copy()
    nul[V4] = reel[V4].to_numpy()[perm]
    suffix = "_nul" if args.nul_seed == 42 else f"_nul_s{args.nul_seed}"
    nul_path = os.path.join(PDAC, f"pdac_886_gse194249_fluxes{suffix}.csv")
    nul.to_csv(nul_path, index=False)
    audit[f"csv_nul{suffix}"] = os.path.basename(nul_path)
    audit[f"csv_nul{suffix}_sha256"] = sha256(nul_path)
    audit["nul_seed"] = args.nul_seed
    audit["n"] = int(len(reel))

    with open(AUDIT, "w") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)
    print(f"réel : {reel_path} SHA {audit['csv_reel_sha256']}")
    print(f"nul (graine {args.nul_seed}) : {nul_path} SHA {audit[f'csv_nul{suffix}_sha256']}")
    print(f"audit : {AUDIT}")


if __name__ == "__main__":
    main()
