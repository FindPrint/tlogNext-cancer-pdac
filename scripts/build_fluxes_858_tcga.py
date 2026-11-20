#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construction des flux §8.58 (TCGA) — protocole gelé
PROTOCOL_stomach_mucus_flux_858.md. Listes candidates copiées du protocole.
Méthode v4 exacte : log2(RSEM+1), scores acineux/îlots, régression par gène
sur [1, acineux, îlots], flux = résidu. Vérification de reproduction du CSV
v4 à atol 1e-9 avant toute construction (sinon ARRÊT).
Groupes : G1 mucus/gastrique, G2 enzymes digestives, G3 récepteurs
olfactifs (regex ^OR[0-9]+[A-Z]?[0-9]*$ + liste fermée), G4 volatil /
signalisation, G5 intestinal/neuroendocrine, TEMOIN acineux (11 gènes).
Plafond gelé : >20 gènes présents -> 20 de plus forte variance des résidus.
Ordres : KRAS (résidu KRAS croissant, 178 lignes, colonne `step`) et stade
(rang principal I=1..IV=4, départage code-barres, 175 lignes, colonne
`STAGE`). Nuls : bloc des flux permuté par lignes, graine 42, rng(42),
contrôle intact. Le contrôle n'est jamais un flux.
Sorties : pdac_tcga_858_<groupe>_<ordre>.csv (+ _nul.csv).
"""
import hashlib
import re
import tarfile

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"
TARBALL = f"{DATA}/tcga_paad_rsem.tar.gz"
TARBALL_MD5 = "b09569ce3f4721f514bc137bd109ac0a"
V4_CSV = f"{OUT}/pdac_tcga_fluxes_v4.csv"
V4_SHA = "e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0"
CLINICAL = f"{OUT}/data_clinical_patient.txt"
SEED = 42
ATOL = 1e-9
CAP = 20

ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]
ISLET = ["INS", "GCG", "PPY", "SST"]

GROUPS = {
    "G1": ["MUC1", "MUC3A", "MUC4", "MUC5AC", "MUC5B", "MUC6", "MUC7",
           "MUC12", "MUC13", "MUC15", "MUC19", "MUC20", "MUC21", "TFF1",
           "TFF2", "TFF3", "GKN1", "GKN2", "PGA3", "PGA4", "PGA5",
           "ATP4A", "ATP4B", "GIF", "LIPF", "GAST", "GHRL", "SST",
           "REG1A", "REG1B", "REG3A", "REG3G", "FCGBP", "AGR2", "SPDEF",
           "AQP5"],
    "G2": ["PNLIP", "PNLIPRP1", "PNLIPRP2", "CEL", "CELA1", "CELA2A",
           "CELA2B", "CELA3A", "CELA3B", "CPA1", "CPA2", "CPB1", "CPB2",
           "CTRB1", "CTRB2", "CTRC", "AMY2A", "AMY2B", "AMY1A", "AMY1B",
           "AMY1C", "PLA2G1B", "CLPS", "PRSS1", "PRSS2", "PRSS3", "CPA3",
           "ELA2A", "ELA3A", "ELA3B"],
    "G4": ["ADH1A", "ADH1B", "ADH1C", "ADH4", "ADH5", "ADH6", "ADH7",
           "ALDH1A1", "ALDH2", "ALDH3A1", "ALDH3B1", "CYP2E1", "CYP2A6",
           "CYP2A13", "CYP1A2", "CYP3A4", "CYP2C9", "UGT1A1", "UGT2B7",
           "SULT1A1", "AOX1", "FMO1", "FMO3", "TAAR1", "TAAR2", "TAAR5",
           "TAAR6", "TAAR8", "TAAR9", "TAS1R1", "TAS1R2", "TAS1R3",
           "TAS2R1", "TAS2R3", "TAS2R4", "TAS2R5", "TAS2R7", "TAS2R8",
           "TAS2R9", "TAS2R10", "TAS2R13", "TAS2R14", "TAS2R16", "TAS2R19",
           "TAS2R20", "TAS2R30", "TAS2R31", "TAS2R38", "TAS2R39", "TAS2R40",
           "TAS2R41", "TAS2R42", "TAS2R43", "TAS2R44", "TAS2R45", "TAS2R46",
           "TAS2R50", "NOS1", "NOS2", "NOS3", "CBS", "CTH", "MPST",
           "HMOX1", "HMOX2"],
    "G5": ["CDX1", "CDX2", "VIL1", "SI", "LCT", "FABP2", "APOA4", "APOB",
           "KRT7", "KRT19", "CHGA", "CHGB", "SYP", "INSM1", "NEUROD1"],
    "TEMOIN": ACINAR,
}
OR_RE = re.compile(r"^OR[0-9]+[A-Z]?[0-9]*$")
OR_EXTRA = ["OR51E2", "OR51E1", "OR2AT4", "OR1A1", "OR2J3", "OR10J5"]


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
    print(f"SHA-256 fichier clinique : {sha(CLINICAL)}")

    # --- Résidus v4 recalculés depuis le tarball ---
    with tarfile.open(TARBALL, "r:gz") as tf:
        member = [m for m in tf.getmembers() if m.name.endswith(".data.txt")][0]
        df = pd.read_csv(tf.extractfile(member), sep="\t", index_col=0,
                         low_memory=False)
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

    # --- Vérification de reproduction du CSV v4 ---
    v4 = pd.read_csv(V4_CSV)
    kras_res = resid_df.loc["KRAS"].sort_values(ascending=True)
    order_kras = list(kras_res.index)
    repro = resid_df.loc[list(v4.columns[1:]), order_kras].T
    assert list(repro.columns) == list(v4.columns[1:])
    maxdiff = float(np.abs(repro.values - v4.iloc[:, 1:].values).max())
    print(f"Reproduction v4 : écart max = {maxdiff:.3e} (atol {ATOL:.0e})")
    assert maxdiff <= ATOL, "ARRÊT : v4 non reproduit"
    print(f"Résidus : {len(resid_df)} gènes x {len(resid_df.columns)} tumeurs")

    # --- Stade clinique (même lecture qu'au §8.45) ---
    raw = pd.read_csv(CLINICAL, sep="\t", header=None, dtype=str,
                      low_memory=False)
    header = list(raw.iloc[4])
    assert header[0] == "PATIENT_ID"
    assert header[6] == "AJCC_PATHOLOGIC_TUMOR_STAGE"
    clin = raw.iloc[5:].copy()
    clin.columns = header
    clin = clin[clin["PATIENT_ID"].notna() & (clin["PATIENT_ID"] != "")]
    clin["STAGE_MAIN"] = clin["AJCC_PATHOLOGIC_TUMOR_STAGE"].apply(main_stage)
    clin["STAGE_RANK"] = clin["STAGE_MAIN"].map(RANK)
    stage_map = dict(zip(clin["PATIENT_ID"], clin["STAGE_RANK"]))
    print(f"Patients cliniques : {len(clin)} ; sans stade : "
          f"{int(clin['STAGE_RANK'].isna().sum())}")

    # --- Groupe G3 : scan OR sur l'univers TCGA ---
    or_genes = sorted(g for g in resid_df.index if OR_RE.match(g))
    for g in OR_EXTRA:
        if g in resid_df.index and g not in or_genes:
            or_genes.append(g)
    GROUPS["G3"] = sorted(or_genes)
    print(f"G3 OR présents dans TCGA : {len(or_genes)}")

    var_res = resid_df.var(axis=1)
    manifest = []
    for gname, genes in GROUPS.items():
        present = [g for g in genes if g in resid_df.index]
        absent = [g for g in genes if g not in resid_df.index]
        if len(present) < 3:
            print(f"{gname}: {len(present)} gènes présents — GROUPE NON "
                  f"CONSTRUIT (< 3). Absents : {absent}")
            continue
        retained = present
        dropped = []
        if len(present) > CAP:
            ranked = var_res.loc[present].sort_values(ascending=False)
            retained = list(ranked.head(CAP).index)
            dropped = list(ranked.iloc[CAP:].index)
        print(f"{gname}: {len(present)} présents, {len(retained)} retenus "
              f"comme flux ; absents TCGA : {absent if absent else '(aucun)'}")
        if dropped:
            print(f"  présents-non-retenus (plafond 20, variance résiduelle) : "
                  f"{dropped}")
        flux = resid_df.loc[retained]
        # Ordre KRAS
        fl_k = flux[order_kras].T
        out_k = pd.DataFrame({"step": np.arange(len(fl_k))})
        for c in fl_k.columns:
            out_k[c] = fl_k[c].values
        assert out_k.isna().sum().sum() == 0
        p_k = f"{OUT}/pdac_tcga_858_{gname}_kras.csv"
        out_k.to_csv(p_k, index=False)
        # Ordre stade
        barcodes = [c for c in resid_df.columns]
        rows = []
        excluded = []
        for bc in barcodes:
            pid = bc[:12]
            r = stage_map.get(pid)
            if r is None or (isinstance(r, float) and np.isnan(r)):
                excluded.append(bc)
            else:
                rows.append((int(r), bc))
        rows.sort(key=lambda t: (t[0], t[1]))
        order_stage = [bc for _, bc in rows]
        fl_s = flux[order_stage].T
        out_s = pd.DataFrame({"STAGE": [r for r, _ in rows]})
        for c in fl_s.columns:
            out_s[c] = fl_s[c].values
        assert out_s.isna().sum().sum() == 0
        p_s = f"{OUT}/pdac_tcga_858_{gname}_stage.csv"
        out_s.to_csv(p_s, index=False)
        print(f"  stade : {len(order_stage)} lignes, exclues : {excluded}")
        # Nuls (graine 42, contrôle intact)
        for p in (p_k, p_s):
            d = pd.read_csv(p)
            rng = np.random.default_rng(SEED)
            perm = rng.permutation(len(d))
            dn = d.copy()
            dn.iloc[:, 1:] = d.iloc[:, 1:].values[perm]
            pn = p.replace(".csv", "_nul.csv")
            dn.to_csv(pn, index=False)
            manifest.append((gname, p, sha(p), pn, sha(pn)))
    print("\nFICHIERS :")
    for gname, p, s1, pn, s2 in manifest:
        print(f"  {gname} {p.split('/')[-1]} SHA {s1[:12]}… ; "
              f"{pn.split('/')[-1]} SHA {s2[:12]}…")
    with open(f"{OUT}/manifest_858_files.txt", "w") as f:
        for gname, p, s1, pn, s2 in manifest:
            f.write(f"{gname} {p} {s1}\n{gname} {pn} {s2}\n")


if __name__ == "__main__":
    main()
