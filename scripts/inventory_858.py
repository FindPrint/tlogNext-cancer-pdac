#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventaire §8.58 — présence/absence des gènes candidats dans les 6 matrices
déjà détenues. Protocole gelé : PROTOCOL_stomach_mucus_flux_858.md.
Listes candidates copiées du protocole (définies AVANT l'inventaire).
Aucune imputation, aucun remplacement. Sorties : inventory_858.csv,
or_scan_858.csv, inventory_858_summary.txt.
"""
import gzip
import hashlib
import re
import tarfile

import numpy as np
import pandas as pd

DATA = "/home/hatch/workspace/runs/pdac-v6/data"
OUT = "/home/hatch/workspace/runs/pdac-v6"

G1 = ["MUC1", "MUC3A", "MUC4", "MUC5AC", "MUC5B", "MUC6", "MUC7", "MUC12",
      "MUC13", "MUC15", "MUC19", "MUC20", "MUC21", "TFF1", "TFF2", "TFF3",
      "GKN1", "GKN2", "PGA3", "PGA4", "PGA5", "ATP4A", "ATP4B", "GIF",
      "LIPF", "GAST", "GHRL", "SST", "REG1A", "REG1B", "REG3A", "REG3G",
      "FCGBP", "AGR2", "SPDEF", "AQP5"]
G2 = ["PNLIP", "PNLIPRP1", "PNLIPRP2", "CEL", "CELA1", "CELA2A", "CELA2B",
      "CELA3A", "CELA3B", "CPA1", "CPA2", "CPB1", "CPB2", "CTRB1", "CTRB2",
      "CTRC", "AMY2A", "AMY2B", "AMY1A", "AMY1B", "AMY1C", "PLA2G1B",
      "CLPS", "PRSS1", "PRSS2", "PRSS3", "CPA3", "ELA2A", "ELA3A", "ELA3B"]
G4 = ["ADH1A", "ADH1B", "ADH1C", "ADH4", "ADH5", "ADH6", "ADH7", "ALDH1A1",
      "ALDH2", "ALDH3A1", "ALDH3B1", "CYP2E1", "CYP2A6", "CYP2A13", "CYP1A2",
      "CYP3A4", "CYP2C9", "UGT1A1", "UGT2B7", "SULT1A1", "AOX1", "FMO1",
      "FMO3", "TAAR1", "TAAR2", "TAAR5", "TAAR6", "TAAR8", "TAAR9", "TAS1R1",
      "TAS1R2", "TAS1R3", "TAS2R1", "TAS2R3", "TAS2R4", "TAS2R5", "TAS2R7",
      "TAS2R8", "TAS2R9", "TAS2R10", "TAS2R13", "TAS2R14", "TAS2R16",
      "TAS2R19", "TAS2R20", "TAS2R30", "TAS2R31", "TAS2R38", "TAS2R39",
      "TAS2R40", "TAS2R41", "TAS2R42", "TAS2R43", "TAS2R44", "TAS2R45",
      "TAS2R46", "TAS2R50", "NOS1", "NOS2", "NOS3", "CBS", "CTH", "MPST",
      "HMOX1", "HMOX2"]
G5 = ["CDX1", "CDX2", "VIL1", "SI", "LCT", "FABP2", "APOA4", "APOB", "KRT7",
      "KRT19", "CHGA", "CHGB", "SYP", "INSM1", "NEUROD1"]
REF = ["PGC", "REG4", "CLDN18", "MUC17", "DPCR1", "MUC2", "MUC16", "KRT20",
       "CEACAM5", "CLCA1", "GSTM1", "CR2"]
OR_EXTRA = ["OR51E2", "OR51E1", "OR2AT4", "OR1A1", "OR2J3", "OR10J5"]
OR_RE = re.compile(r"^OR[0-9]+[A-Z]?[0-9]*$")
ACINAR = ["PNLIP", "CTRB2", "CELA3A", "CTRB1", "CPA1", "CELA2A",
          "CPB1", "CELA3B", "CLPS", "CTRC", "CPA2"]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    universes = {}
    notes = {}

    # ---- TCGA RSEM ----
    tarball = f"{DATA}/tcga_paad_rsem.tar.gz"
    assert md5(tarball) == "b09569ce3f4721f514bc137bd109ac0a", "MD5 tarball non conforme"
    with tarfile.open(tarball, "r:gz") as tf:
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
    universes["TCGA"] = set(logmat.index)
    notes["TCGA"] = (f"{len(logmat)} genes x {len(logmat.columns)} tumeurs "
                     f"(RSEM log2+1, cas complets)")
    tcga_med = logmat.median(axis=1)
    tcga_frac_nonzero = (mat > 0).mean(axis=1)

    # ---- GSE71729 (symboles directs) ----
    m = pd.read_csv(f"{DATA}/GSE71729_series_matrix.txt.gz", sep="\t",
                    comment="!", index_col=0, low_memory=False)
    m.index = m.index.str.strip('"')
    m.columns = [c.strip('"') for c in m.columns]
    m = m.groupby(level=0).median()
    universes["GSE71729"] = set(m.index)
    notes["GSE71729"] = f"{len(m)} genes x {len(m.columns)} echantillons (GPL20769)"

    # ---- GSE62452 (mapping GPL6244) ----
    pmap = {}
    with open(f"{DATA}/GPL6244_probe2symbol.tsv") as f:
        header = f.readline()
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[1] and parts[1] != "---":
                pmap[parts[0]] = parts[1]
    g = pd.read_csv(f"{DATA}/GSE62452_series_matrix.txt.gz", sep="\t",
                    comment="!", index_col=0, low_memory=False)
    g.index = g.index.astype(str).str.strip('"')
    g.columns = [c.strip('"') for c in g.columns]
    g.index = g.index.map(lambda p: pmap.get(p, p))
    g = g[~g.index.str.startswith("789")]  # sondes sans symbole
    g = g.groupby(level=0).median()
    universes["GSE62452"] = set(g.index)
    notes["GSE62452"] = (f"{len(g)} genes x {len(g.columns)} echantillons "
                         f"(GPL6244, {len(pmap)} sondes mappees)")

    # ---- ICGC ----
    exp = pd.read_csv(f"{DATA}/icgc_pacaau_exp.txt.gz", sep="\t", index_col=0,
                      compression="gzip")
    pm = pd.read_csv(f"{DATA}/icgc_pacaau_probemap.gz", sep="\t",
                     compression="gzip")
    mapping = dict(zip(pm["#id"], pm["gene"]))
    exp.index = exp.index.map(lambda x: mapping.get(x, x))
    exp = exp.groupby(level=0).median()
    universes["ICGC"] = set(exp.index)
    notes["ICGC"] = f"{len(exp)} genes x {len(exp.columns)} echantillons (PACA-AU)"

    # ---- CPTAC UMich (genes en colonnes) ----
    u = pd.read_csv(f"{DATA}/cptac/pdac_umich_protein_gene_matrix.csv",
                    index_col=0, low_memory=False)
    universes["CPTAC_UMich"] = set(u.columns)
    notes["CPTAC_UMich"] = f"{len(u.columns)} genes-proteines x {len(u)} tumeurs"

    # ---- CPTAC BCM (lignes ENSG -> symbole via rapport UMich) ----
    mapping_bcm = {}
    u_idx = pd.read_csv(f"{DATA}/cptac/umich-pdac-proteomics-Report_abundance_"
                        f"groupby=protein_protNorm=MD_gu=2.tsv.gz",
                        sep="\t", compression="gzip", usecols=["Index"])
    for idx in u_idx["Index"]:
        parts = str(idx).split("|")
        ensg = next((p.split(".")[0] for p in parts if p.startswith("ENSG")), None)
        sym = parts[-2] if len(parts) >= 2 else None
        if ensg and sym and not sym.startswith("ENS"):
            mapping_bcm.setdefault(ensg, sym)
    b = pd.read_csv(f"{DATA}/cptac/bcm-pdac-proteomics-PDAC_proteomics_gene_"
                    f"abundance_log2_reference_intensity_normalized_Tumor.txt.gz",
                    sep="\t", compression="gzip")
    b["ensg"] = b["idx"].str.split(".").str[0]
    b["gene"] = b["ensg"].map(mapping_bcm)
    bcm_genes = set(b["gene"].dropna())
    universes["CPTAC_BCM"] = bcm_genes
    notes["CPTAC_BCM"] = (f"{len(bcm_genes)} genes-proteines mappes "
                          f"({len(mapping_bcm)} ENSG->symbole dans le rapport UMich)")

    # ---- DepMap CRISPR (genes en colonnes "SYMBOL (Entrez)") ----
    d = pd.read_csv(f"{DATA}/CRISPRGeneEffect.csv", nrows=0)
    dep_genes = set()
    for c in d.columns[1:]:
        sym = c.split(" (")[0].strip()
        if sym:
            dep_genes.add(sym)
    universes["DepMap_CRISPR"] = dep_genes
    notes["DepMap_CRISPR"] = (f"{len(dep_genes)} genes (dependance CRISPR, "
                              f"pas expression)")

    # ---- OR scan par matrice ----
    or_rows = []
    for name, uni in universes.items():
        ors = sorted(g for g in uni if OR_RE.match(g))
        for gsym in ors:
            row = {"gene": gsym, "matrice": name, "regex_OR": 1}
            if name == "TCGA" and gsym in tcga_med.index:
                row["tcga_mediane_log2RSEM+1"] = round(float(tcga_med.loc[gsym]), 3)
                row["tcga_frac_tumeurs_RSEM>0"] = round(float(tcga_frac_nonzero.loc[gsym]), 3)
            or_rows.append(row)
    or_df = pd.DataFrame(or_rows)

    # ---- Inventaire candidats ----
    groups = {"G1_mucus_gastrique": G1, "G2_enzymes_digestives": G2,
              "G4_volatil_signalisation": G4, "G5_intestinal_neuroendocrine": G5,
              "REF_bloc_v4": REF, "G3_OR_liste_fermee": OR_EXTRA,
              "TEMOIN_acineux": ACINAR}
    rows = []
    for gname, genes in groups.items():
        for gsym in genes:
            r = {"gene": gsym, "groupe": gname}
            for mname, uni in universes.items():
                r[mname] = 1 if gsym in uni else 0
            rows.append(r)
    inv = pd.DataFrame(rows)
    inv.to_csv(f"{OUT}/inventory_858.csv", index=False)
    or_df.to_csv(f"{OUT}/or_scan_858.csv", index=False)

    # ---- Résumé ----
    lines = []
    lines.append("INVENTAIRE §8.58 — presence/absence par matrice (1=present, 0=absent)")
    for mname in universes:
        lines.append(f"Univers {mname}: {len(universes[mname])} symboles. {notes[mname]}")
    lines.append("")
    for gname, genes in groups.items():
        tot = len(genes)
        parts = []
        for mname in universes:
            n = sum(1 for gsym in genes if gsym in universes[mname])
            parts.append(f"{mname} {n}/{tot}")
        lines.append(f"{gname} (n={tot}): " + " ; ".join(parts))
        for mname in universes:
            absent = [g for g in genes if g not in universes[mname]]
            if absent:
                lines.append(f"  absents {mname}: {', '.join(absent)}")
    lines.append("")
    lines.append("SCAN OR (regex ^OR[0-9]+[A-Z]?[0-9]*$) :")
    for mname in universes:
        ors = sorted(g for g in universes[mname] if OR_RE.match(g))
        lines.append(f"  {mname}: {len(ors)} symboles OR")
        lines.append(f"    {', '.join(ors) if ors else '(aucun)'}")
    lines.append("")
    lines.append("OR presents dans TCGA (mediane log2(RSEM+1) ; frac tumeurs RSEM>0) :")
    if not or_df.empty:
        t = or_df[or_df["matrice"] == "TCGA"].sort_values("tcga_mediane_log2RSEM+1",
                                                          ascending=False)
        for _, r in t.iterrows():
            lines.append(f"  {r['gene']}: med={r['tcga_mediane_log2RSEM+1']:.3f} "
                         f"frac>0={r['tcga_frac_tumeurs_RSEM>0']:.3f}")
    txt = "\n".join(lines) + "\n"
    with open(f"{OUT}/inventory_858_summary.txt", "w") as f:
        f.write(txt)
    print(txt)
    print("SHA inventory_858.csv:", sha(f"{OUT}/inventory_858.csv"))
    print("SHA or_scan_858.csv:", sha(f"{OUT}/or_scan_858.csv"))


if __name__ == "__main__":
    main()
