#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Récupère le tableau d'annotation de la plateforme GPL4133 (Agilent-014850
Whole Human Genome Microarray 4x44K G4112F, puce de GSE21501) en streaming :
le fichier family.soft.gz du FTP GEO contient table plateforme + tables
d'échantillons, donc on coupe le transfert dès le marqueur
!platform_table_end vu. Adapté de download_gpl15048_mapping_869.py
(chantier §8.69 ; originaux intacts).
Sortie : GPL4133_probe2symbol.tsv (probe id -> gene symbol).
Colonne de symbole : « GeneSymbol » / « Gene Symbol » / « GENE_SYMBOL »
/ « gene_symbol » (première trouvée), sinon « gene_assignment » comme
GPL6244. Si aucune : ÉCHEC explicite, pas de mapping deviné.
"""
import gzip
import subprocess
import sys

URL = ("https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL4nnn/GPL4133/"
       "soft/GPL4133_family.soft.gz")
OUT = "/home/hatch/workspace/runs/pdac-v6/data/GPL4133_probe2symbol.tsv"

SYM_CANDIDATES = ("GeneSymbol", "Gene Symbol", "GENE_SYMBOL",
                  "gene_symbol", "GENE SYMBOL")

proc = subprocess.Popen(["curl", "-sL", URL],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
mapping = {}
in_table = False
header = None
sym_idx = None
sym_mode = None
n_table = 0
end_seen = False
try:
    with gzip.GzipFile(fileobj=proc.stdout) as gz:
        for raw in gz:
            line = raw.decode("utf-8", errors="replace")
            if line.startswith("!platform_table_begin"):
                in_table = True
                continue
            if line.startswith("!platform_table_end"):
                end_seen = True
                break
            if in_table:
                if line.startswith("ID\t"):
                    header = line.rstrip("\n").split("\t")
                    print("Colonnes table :", header)
                    for cand in SYM_CANDIDATES:
                        if cand in header:
                            sym_idx = header.index(cand)
                            sym_mode = "symbol"
                            break
                    if sym_idx is None and "gene_assignment" in header:
                        sym_idx = header.index("gene_assignment")
                        sym_mode = "assignment"
                    if sym_idx is None:
                        print("ÉCHEC : aucune colonne de symbole",
                              file=sys.stderr)
                        sys.exit(2)
                    print("Colonne symbole :", sym_mode,
                          "index", sym_idx)
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) > sym_idx:
                    n_table += 1
                    if sym_mode == "symbol":
                        sym = parts[sym_idx].strip()
                        if sym and sym != "---":
                            mapping[parts[0]] = sym
                    else:
                        assign = parts[sym_idx].strip()
                        if assign and assign != "---":
                            first = assign.split(" /// ")[0].strip()
                            fields = [x.strip()
                                      for x in first.split(" // ")]
                            if len(fields) >= 2 and fields[1]:
                                mapping[parts[0]] = fields[1]
finally:
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()

print("lignes table plateforme :", n_table)
print("marqueur !platform_table_end vu :", end_seen)
print("sondes avec symbole :", len(mapping))
print("symboles uniques :", len(set(mapping.values())))
with open(OUT, "w") as f:
    f.write("probe\tsymbol\n")
    for p, s in sorted(mapping.items()):
        f.write(f"{p}\t{s}\n")
print("mapping sauvé :", OUT)
if not end_seen or n_table < 30000:
    print("ÉCHEC : table incomplète", file=sys.stderr)
    sys.exit(1)
