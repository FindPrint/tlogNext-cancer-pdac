#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Téléchargement §8.86 — GSE194249, matrice FPKM déposée (APRÈS le gel
du protocole PROTOCOL_gse194249_886.md, SHA b620238b…).
Source unique : https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194249/suppl/GSE194249_PDPCOs_FPKM.txt.gz
(miroir HTTPS du FTP GEO ; repli ftp:// consigné si HTTPS échoue).
Vérifications : gzip intègre, taille, SHA-256, premières lignes d'en-tête
(consignées, non interprétées ici — la construction est dans
build_fluxes_886.py).
Sortie : data/GSE194249_PDPCOs_FPKM.txt.gz + download_gse194249_886_receipt.json
Usage : python3 download_gse194249_886.py
"""
import gzip
import hashlib
import json
import os
import urllib.request

PDAC = os.path.dirname(os.path.abspath(__file__))
URLS = [
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194249/suppl/GSE194249_PDPCOs_FPKM.txt.gz",
    "ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194249/suppl/GSE194249_PDPCOs_FPKM.txt.gz",
]
DEST = os.path.join(PDAC, "data", "GSE194249_PDPCOs_FPKM.txt.gz")
RECEIPT = os.path.join(PDAC, "download_gse194249_886_receipt.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    os.makedirs(os.path.join(PDAC, "data"), exist_ok=True)
    last_err = None
    used = None
    for url in URLS:
        for attempt in (1, 2, 3):
            try:
                print(f"tentative {attempt} : {url}")
                req = urllib.request.Request(url, headers={"User-Agent": "TagPrint-PDAC-audit/1.0"})
                with urllib.request.urlopen(req, timeout=300) as r, open(DEST, "wb") as f:
                    while True:
                        chunk = r.read(1 << 20)
                        if not chunk:
                            break
                        f.write(chunk)
                used = url
                break
            except Exception as e:  # noqa: BLE001
                last_err = e
                print(f"  échec tentative {attempt} : {e}")
        if used:
            break
    if not used:
        raise SystemExit(f"TÉLÉCHARGEMENT ÉCHOUÉ (3 tentatives × {len(URLS)} URL) : {last_err}")
    size = os.path.getsize(DEST)
    digest = sha256(DEST)
    # Intégrité gzip + aperçu d'en-tête (premières lignes, consignées verbatim).
    with gzip.open(DEST, "rt") as f:
        header = f.readline().rstrip("\n")
        line2 = f.readline().rstrip("\n")
        n_lines = 2
        for _ in f:
            n_lines += 1
    header_cols = header.split("\t")
    receipt = {
        "serie": "GSE194249",
        "url_utilisee": used,
        "fichier": "data/GSE194249_PDPCOs_FPKM.txt.gz",
        "taille_octets": size,
        "sha256": digest,
        "gzip_integre": True,
        "n_lignes_total": n_lines,
        "n_colonnes_en_tete": len(header_cols),
        "en_tete_premieres_colonnes": header_cols[:6],
        "en_tete_derniere_colonne": header_cols[-1] if header_cols else None,
        "deuxieme_ligne_premieres_colonnes": line2.split("\t")[:6],
    }
    with open(RECEIPT, "w") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)
    print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
