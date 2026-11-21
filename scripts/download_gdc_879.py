#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Telechargement §8.79 — GDC ORGANOID-PANCREATIC, 55 fichiers ouverts.
Protocole PROTOCOL_nouvelle_serie_879.md (§4.1). Version curl :
chaque file_id est telecharge via `curl -C - --retry 5
--retry-all-errors` (reprise sur coupure, l'API GDC accepte les
requetes Range — verifie 206 le 21 nov. 2026). MD5 verifie contre
le manifeste, SHA-256 consigne. Ne lit ni ne transforme les valeurs.
Usage : python3 download_gdc_879.py
Sorties : data/gdc_organoid_879/<file_id>.tsv (55 fichiers),
download_gdc_879_receipt.json, download_gdc_879.log.
"""
import csv
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

PDAC = "/home/hatch/workspace/runs/pdac-v6"
MANIFEST = f"{PDAC}/data/GDC_ORGANOID_PANCREATIC_OPEN_RNASEQ_MANIFEST_879.tsv"
DEST = f"{PDAC}/data/gdc_organoid_879"
RECEIPT = f"{PDAC}/download_gdc_879_receipt.json"
LOG = f"{PDAC}/download_gdc_879.log"
EXPECTED_MANIFEST_SHA256 = (
    "f713edebf0f8afb20305b1472d480564e45ac31ce79e28350d7dde6ae496220b")
API_PREFIX = "https://api.gdc.cancer.gov/data/"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def md5_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat()} {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def main():
    os.makedirs(DEST, exist_ok=True)
    if sha256_file(MANIFEST) != EXPECTED_MANIFEST_SHA256:
        print("ERREUR : manifeste SHA different de l'empreinte gelee.")
        sys.exit(1)
    with open(MANIFEST, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    assert len(rows) == 55, f"manifeste : {len(rows)} lignes, attendu 55"
    log(f"Manifeste OK (55 lignes, SHA verifie). Total attendu : "
        f"{sum(int(r['file_size_bytes']) for r in rows)} o.")
    results = []
    n_ok = n_fail = n_skip = 0
    total_bytes = 0
    for i, r in enumerate(rows, 1):
        fid, fname, md5exp = r["file_id"], r["file_name"], r["md5sum"]
        size_exp = int(r["file_size_bytes"])
        dest = os.path.join(DEST, fid + ".tsv")
        if os.path.exists(dest) and md5_file(dest) == md5exp:
            log(f"[{i}/55] SKIP {fid} (deja present, MD5 OK)")
            results.append({"file_id": fid, "file_name": fname,
                            "status": "skip_md5_ok",
                            "md5": md5exp, "sha256": sha256_file(dest),
                            "size_bytes": os.path.getsize(dest)})
            n_skip += 1
            total_bytes += os.path.getsize(dest)
            continue
        cmd = ["curl", "-sS", "-L", "-C", "-", "--retry", "8",
               "--retry-all-errors", "--retry-delay", "5",
               "--connect-timeout", "30", "--max-time", "600",
               "-o", dest, API_PREFIX + fid]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            log(f"[{i}/55] ECHEC curl {fid} rc={proc.returncode} "
                f"stderr={proc.stderr.strip()[-300:]}")
            results.append({"file_id": fid, "file_name": fname,
                            "status": "download_failed",
                            "curl_rc": proc.returncode})
            n_fail += 1
            continue
        md5got = md5_file(dest)
        size_got = os.path.getsize(dest)
        if md5got != md5exp or size_got != size_exp:
            log(f"[{i}/55] ECHEC INTEGRITE {fid} md5={md5got} "
                f"(attendu {md5exp}) taille={size_got} (attendu {size_exp})")
            results.append({"file_id": fid, "file_name": fname,
                            "status": "integrity_failed", "md5": md5got,
                            "size_bytes": size_got})
            n_fail += 1
            continue
        log(f"[{i}/55] OK {fid} ({size_got} o, MD5 OK)")
        results.append({"file_id": fid, "file_name": fname, "status": "ok",
                        "md5": md5got, "sha256": sha256_file(dest),
                        "size_bytes": size_got})
        n_ok += 1
        total_bytes += size_got
    receipt = {"manifeste_sha256": EXPECTED_MANIFEST_SHA256,
               "n_attendu": 55, "n_ok": n_ok, "n_skip": n_skip,
               "n_fail": n_fail, "total_bytes": total_bytes,
               "date_utc": datetime.now(timezone.utc).isoformat(),
               "fichiers": results}
    with open(RECEIPT, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)
    log(f"FIN ok={n_ok} skip={n_skip} echecs={n_fail} "
        f"total_bytes={total_bytes}")
    print(f"ok={n_ok} skip={n_skip} echecs={n_fail} "
          f"total_bytes={total_bytes}")
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()
