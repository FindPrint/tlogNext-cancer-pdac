#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test C — série TCGA v4 ordonnée par stade clinique (19 nov. 2026).
Protocole gelé : PROTOCOL_testC_stage.md (écrit avant ce script).

- Recalcule les résidus v4 depuis la matrice Firehose (même méthode que
  build_fluxes_tcga_v4.py) et VÉRIFIE qu'ils reproduisent le CSV v4
  (12 colonnes de flux, triées par résidu KRAS croissant, atol 1e-9).
  Arrêt si un écart dépasse le seuil.
- Stade clinique : AJCC_PATHOLOGIC_TUMOR_STAGE de
  data_clinical_patient.txt (fichier TCGA PanCanAtlas déjà sur le disque ;
  SHA-256 consigné en provenance — premier hachage, acquisition non
  documentée, voir protocole §9). Rang du stade PRINCIPAL : I=1, II=2,
  III=3, IV=4 (sous-stades repliés). Départage des ex æquo dans un même
  stade : code-barres échantillon TCGA, ordre lexicographique croissant
  (neutre ; jamais KRAS, jamais un flux).
- Tumeurs sans stade connu : EXCLUES, sans imputation (rapportées).
- Série réelle : STAGE en 1re colonne (contrôle), 12 flux v4 dans
  l'ordre v4, lignes triées par (rang de stade, code-barres). STAGE n'est
  pas un flux : pas de doublon contrôle/flux (défaut des rotations §8.32
  évité).
- Nul : bloc des 12 flux permuté par lignes, graine 42, générateur frais
  rng(42), colonne de contrôle intacte (même convention que les autres
  nuls).
"""
import hashlib
import json
import tarfile

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
TARBALL = f"{DATA}/tcga_paad_rsem.tar.gz"
TARBALL_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
V4_CSV = f"{OUT}/pdac_tcga_fluxes_v4.csv"
V4_SHA = "e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0"
CLINICAL = f"{OUT}/data_clinical_patient.txt"
SEED = 42
ATOL = 1e-9

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


def main_stage(stage_raw):
    """'STAGE IIB' -> 'II', 'STAGE I' -> 'I', vide/NaN -> None."""
    if stage_raw is None:
        return None
    s = str(stage_raw).strip()
    if s in ("", "nan", "NaN", "None"):
        return None
    if s.startswith("STAGE "):
        s = s[len("STAGE "):].strip()
    if s.startswith("III"):
        return "III"
    if s.startswith("IV"):
        return "IV"
    if s.startswith("II"):
        return "II"
    if s.startswith("I"):
        return "I"
    return None


RANK = {"I": 1, "II": 2, "III": 3, "IV": 4}


def main():
    assert md5(TARBALL) == TARBALL_MD5, "MD5 du tarball non conforme"
    assert sha(V4_CSV) == V4_SHA, "SHA du CSV v4 non conforme"
    clin_sha = sha(CLINICAL)
    print(f"SHA-256 fichier clinique : {clin_sha}")

    # --- Fichier clinique : 4 lignes descriptives, puis en-tête, puis 184 patients ---
    raw = pd.read_csv(CLINICAL, sep="\t", header=None, dtype=str, low_memory=False)
    header = list(raw.iloc[4])
    assert header[0] == "PATIENT_ID", f"en-tête clinique inattendu : {header[0]}"
    assert header[6] == "AJCC_PATHOLOGIC_TUMOR_STAGE", \
        f"colonne stade inattendue : {header[6]}"
    clin = raw.iloc[5:].copy()
    clin.columns = header
    clin = clin[clin["PATIENT_ID"].notna() & (clin["PATIENT_ID"] != "")]
    assert clin["PATIENT_ID"].duplicated().sum() == 0, "doublon PATIENT_ID"
    assert set(clin["CANCER_TYPE_ACRONYM"].unique()) == {"PAAD"}
    print(f"Patients cliniques : {len(clin)}")
    stage_raw_counts = clin["AJCC_PATHOLOGIC_TUMOR_STAGE"].fillna("(vide)").value_counts().to_dict()
    print(f"Stades bruts (184 patients) : {stage_raw_counts}")
    clin["STAGE_MAIN"] = clin["AJCC_PATHOLOGIC_TUMOR_STAGE"].apply(main_stage)
    clin["STAGE_RANK"] = clin["STAGE_MAIN"].map(RANK)
    stage_map = dict(zip(clin["PATIENT_ID"], clin["STAGE_RANK"]))
    stage_str_map = dict(zip(clin["PATIENT_ID"],
                             clin["AJCC_PATHOLOGIC_TUMOR_STAGE"].fillna("(vide)")))
    n_clin_no_stage = int(clin["STAGE_RANK"].isna().sum())

    # --- Résidus v4 recalculés depuis le tarball ---
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
    print(f"Tumeurs primaires (code 01) : {logmat.shape[1]} ; gènes : {logmat.shape[0]}")

    score_ac = logmat.loc[[g for g in ACINAR if g in logmat.index]].median(axis=0)
    score_is = logmat.loc[[g for g in ISLET if g in logmat.index]].median(axis=0)
    X = np.column_stack([np.ones(len(logmat.columns)), score_ac.values,
                         score_is.values])
    Y = logmat.values
    beta, *_ = np.linalg.lstsq(X, Y.T, rcond=None)
    resid = Y - (X @ beta).T
    resid_df = pd.DataFrame(resid, index=logmat.index, columns=logmat.columns)

    # --- Vérification de reproduction du CSV v4 (arrêt si écart > atol) ---
    v4 = pd.read_csv(V4_CSV)
    flux_cols = list(v4.columns[1:])
    kras_res = resid_df.loc["KRAS"].sort_values(ascending=True)
    order_kras = list(kras_res.index)
    recomputed = resid_df.loc[flux_cols, order_kras].T.reset_index(drop=True)
    assert recomputed.shape == v4[flux_cols].shape, "forme v4 différente"
    max_diff = float(np.abs(recomputed.values - v4[flux_cols].values).max())
    print(f"Vérification v4 : 12 flux recalculés, écart max vs CSV v4 = {max_diff:.3e} (atol {ATOL:g})")
    assert max_diff <= ATOL, f"ÉCART v4 {max_diff:.3e} > atol — ARRÊT"
    pgc_diff = float(np.abs(recomputed["PGC"].values - v4["PGC"].values).max())
    print(f"Colonne PGC seule : écart max = {pgc_diff:.3e} — reproduction exacte.")
    assert len(order_kras) == 178 == len(v4)

    # --- Jointure stade : patient = 12 premiers caractères du code-barres ---
    rows = []
    excluded = []
    for bc in logmat.columns:
        patient = bc[:12]
        rank = stage_map.get(patient)
        if rank is None or (isinstance(rank, float) and np.isnan(rank)):
            excluded.append(bc)
        else:
            rows.append({"barcode": bc, "patient": patient,
                         "stage_main": clin.loc[clin["PATIENT_ID"] == patient,
                                                "STAGE_MAIN"].iloc[0],
                         "stage_raw": stage_str_map[patient],
                         "rank": int(rank)})
    print(f"Tumeurs appariées avec stade connu : {len(rows)} ; exclues (sans stade) : {len(excluded)} {excluded}")
    n_clin_no_rsem = len(set(stage_map) - {bc[:12] for bc in logmat.columns})
    print(f"Patients cliniques sans échantillon RSEM : {n_clin_no_rsem}")
    assert len(rows) >= 40, f"série trop courte ({len(rows)} < 40) — ARRÊT (protocole §2)"
    order_stage = sorted(rows, key=lambda r: (r["rank"], r["barcode"]))
    barcodes_stage = [r["barcode"] for r in order_stage]
    ranks = np.array([r["rank"] for r in order_stage])
    counts = {s: int((ranks == RANK[s]).sum()) for s in ["I", "II", "III", "IV"]}
    print(f"Effectifs par stade dans la série : {counts} (total {len(order_stage)})")
    sub_counts = {}
    for s in ["I", "II", "III", "IV"]:
        sub = pd.Series([r["stage_raw"] for r in order_stage
                         if r["stage_main"] == s]).value_counts().to_dict()
        sub_counts[s] = sub
    print(f"Sous-stades par stade principal : {sub_counts}")

    # --- Cohérence avec KRAS (rapportée, ne change pas la série) ---
    kras_rank = {bc: i for i, bc in enumerate(order_kras)}
    rho_stage_kras, p_stage_kras = spearmanr(
        ranks, np.array([kras_rank[bc] for bc in barcodes_stage]))
    print(f"Spearman rang de stade vs rang KRAS : {rho_stage_kras:+.4f} (p={p_stage_kras:.3g})")
    top12_stage = set(barcodes_stage[-12:])
    top12_kras = set(order_kras[-12:])
    print(f"Recouvrement top-12 stade/KRAS : {len(top12_stage & top12_kras)}/12")
    top12_comp = pd.Series([r["stage_raw"] for r in order_stage[-12:]]).value_counts().to_dict()
    print(f"Composition des 12 dernières lignes : {top12_comp}")

    # --- Série réelle : STAGE contrôle, 12 flux v4, tri par (stade, code-barres) ---
    flux = resid_df.loc[flux_cols, barcodes_stage].T
    assert flux.isna().sum().sum() == 0
    out = pd.DataFrame({"STAGE": ranks})
    out = pd.concat([out, flux.reset_index(drop=True)], axis=1)
    out_path = f"{OUT}/pdac_tcga_fluxes_v4_stage.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes)")

    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_tcga_fluxes_v4_stage_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} (permutation graine {SEED}, contrôle intact)")

    provenance = {
        "date": "2026-11-19",
        "test": "Test C — série TCGA v4 ordonnée par stade clinique",
        "protocole": "PROTOCOL_testC_stage.md (gelé avant les runs)",
        "go": "chantier 3, go parent 19 nov. 2026",
        "source": "Broad GDAC Firehose stddata 2016-01-28, PAAD, RSEM genes "
                  "normalized, tarball déjà sur disque",
        "tarball": {"fichier": TARBALL, "md5": TARBALL_MD5},
        "base_v4": {"fichier": V4_CSV, "sha256": V4_SHA},
        "clinique": {
            "fichier": CLINICAL,
            "sha256": clin_sha,
            "contenu": "TCGA PanCanAtlas, 184 patients PAAD, 0 doublon PATIENT_ID",
            "colonne": "AJCC_PATHOLOGIC_TUMOR_STAGE (7e colonne)",
            "edition_ajcc": "7e (colonne AJCC_STAGING_EDITION)",
            "stades_bruts_184_patients": stage_raw_counts,
            "patients_sans_stade": n_clin_no_stage,
            "provenance_acquisition": "MANQUANTE — fichier déjà sur le disque "
                "au début du chantier (15 nov. 2026, 15h13 UTC) ; aucune entrée "
                "dans fetch_tcga.log, download_firehose.log ni PROVENANCE_tcga*.md ; "
                "premier hachage consigné ici ; rien re-téléchargé",
        },
        "verification_reproduction": {
            "méthode": "résidus v4 recalculés depuis le tarball, triés par "
                       "résidu KRAS croissant, comparés au CSV v4",
            "échantillon": 178,
            "écart_max_12_flux": max_diff,
            "écart_max_PGC": pgc_diff,
            "atol": ATOL,
            "résultat": "reproduction exacte (écart <= atol)" if max_diff <= ATOL else "ÉCHEC",
        },
        "jointure": {
            "méthode": "patient = 12 premiers caractères du code-barres "
                       "échantillon RSEM (code 01) vers PATIENT_ID clinique",
            "tumeurs_appariées_stade_connu": len(rows),
            "tumeurs_exclues_sans_stade": excluded,
            "patients_cliniques_sans_rsem": n_clin_no_rsem,
        },
        "ordre": {
            "définition": "rang du stade principal I=1, II=2, III=3, IV=4 ; "
                          "sous-stades repliés (IA/IB -> I, IIA/IIB -> II)",
            "départage_ex_aequo": "code-barres échantillon TCGA, ordre "
                                  "lexicographique croissant (neutre)",
            "effectifs_par_stade": counts,
            "sous_stades_par_stade": sub_counts,
            "spearman_rang_stade_vs_rang_KRAS": {"rho": round(float(rho_stage_kras), 4),
                                                 "p": float(p_stage_kras)},
            "recouvrement_top12_stade_vs_KRAS": len(top12_stage & top12_kras),
            "composition_12_dernières_lignes": top12_comp,
        },
        "série": {"fichier": out_path, "sha256": sha(out_path),
                  "lignes": int(out.shape[0]), "colonnes": list(out.columns),
                  "ordre": "(rang de stade, code-barres) croissants",
                  "contrôle": "STAGE (1re colonne, pas un flux — pas de doublon)"},
        "nul": {"fichier": nul_path, "sha256": sha(nul_path),
                "méthode": "bloc des 12 flux permuté par lignes, graine 42, contrôle intact"},
        "script": "build_fluxes_tcga_v4_stage.py",
    }
    with open(f"{OUT}/PROVENANCE_testC_stage.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — Test C : série TCGA v4 ordonnée par stade clinique (19 nov. 2026)\n\n")
        f.write("```json\n" + json.dumps(provenance, indent=2, ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_testC_stage.md")
    print(f"SHA script : {sha(__file__)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
