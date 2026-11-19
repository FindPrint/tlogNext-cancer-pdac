#!/usr/bin/env python3
"""Helper minimal pour interroger l'API GraphQL du PDC (open access).
Usage: python3 pdc_query.py '<requête GraphQL>' [fichier_sortie.json]
Transport curl (même raison que fetch_tcga_fluxes.py : urllib lève
IncompleteRead sur les réponses chunked).
"""
import json
import subprocess
import sys

URL = "https://pdc.cancer.gov/graphql"


def query(q, tries=3):
    body = json.dumps({"query": q})
    for attempt in range(tries):
        try:
            out = subprocess.run(
                ["curl", "-sS", "--max-time", "120",
                 "-H", "Content-Type: application/json",
                 "-d", body, URL],
                capture_output=True, text=True, timeout=150, check=True,
            )
            return json.loads(out.stdout)
        except Exception as e:  # noqa: BLE001
            if attempt == tries - 1:
                raise
            print(f"tentative {attempt+1} échouée : {e}", file=sys.stderr)


if __name__ == "__main__":
    q = sys.argv[1]
    res = query(q)
    text = json.dumps(res, indent=1)
    if len(sys.argv) > 2:
        open(sys.argv[2], "w").write(text)
    print(text[:4000])
