#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.55 — Extraction mécanique du sampInfo de pdacR TCGA_PAAD.rds -> CSV.
Source : pdacR (Torre-Healy et al. 2023, Commun Biol 6:163),
fichier data/TCGA_PAAD.rds, GitHub rmoffitt/pdacR,
URL https://raw.githubusercontent.com/rmoffitt/pdacR/master/data/TCGA_PAAD.rds
SHA-256 52020679350d1539d7516f7d38f7bf09e510225eba2f228a4fe874f3c496ea76
(ne jamais modifier le .rds). Le .rds est un objet R (SummarizedExperiment) :
lu avec le package python `rdata` (lecture seule, aucune valeur calculée
ici — simple transcription des 181 lignes x 55 colonnes du sampInfo).
Sortie : purity_855_sampinfo.csv (SHA noté dans le rapport et la section).
Exécution : /tmp/purity855/venv855/bin/python extract_pdacr_sampinfo_855.py
(python système sans rdata ; l'environnement venv est documenté, pas un
artefact du projet).
"""
import hashlib
import os

import rdata

BASE = "/home/hatch/workspace/runs/pdac-v6"
RDS = f"{BASE}/data/pdacR_TCGA_PAAD.rds"
RDS_SHA = "52020679350d1539d7516f7d38f7bf09e510225eba2f228a4fe874f3c496ea76"
OUT = f"{BASE}/purity_855_sampinfo.csv"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    assert sha(RDS) == RDS_SHA, "SHA du .rds non conforme — arrêt"
    print("SHA .rds conforme.")
    d = rdata.read_rds(RDS)
    assert set(d.keys()) == {"ex", "sampInfo", "metadata", "featInfo"}, \
        f"clés inattendues : {list(d.keys())}"
    si = d["sampInfo"]
    print(f"sampInfo : {si.shape[0]} lignes x {si.shape[1]} colonnes")
    assert si.shape == (181, 55), f"forme inattendue : {si.shape}"
    assert "Tumor.Sample.ID" in si.columns and "ABSOLUTE.Purity" in si.columns
    assert si["Tumor.Sample.ID"].nunique() == 181, "doublons de Tumor.Sample.ID"
    meta = d["metadata"]
    print("metadata.reference :", list(meta["reference"]))
    print("metadata.description :", list(meta["description"]))
    si.to_csv(OUT, index=False)
    print(f"Écrit : {OUT} SHA {sha(OUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
