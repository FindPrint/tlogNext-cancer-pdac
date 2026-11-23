#!/usr/bin/env python3
"""Lot suivant §8.93 (double piste) — construction des nuls frais LOCAUX.

Moitié locale = les 7 paires A2 restantes (E2 du protocole gelé) :
GSE21501, GSE79668, GSE60979, GSE131050 Yeh FF, GSE57495, GDC ORGANOID,
GSE194249. Graines 9111–9300 (190 par paire, 1330 fichiers), disjointes
de 9101–9110 (lot en cours), de 3000–3999 (réplique §8.93) et de 42
(nul unique historique).

Méthode : scripts/build_null_893.py (règle gelée, validée octet à octet
contre le lot en cours — voir README.md). Les CSV sont écrits dans
~/workspace/runs/pdac-v6/ (même emplacement que les nuls 9101–9110).
Reprise : un fichier existant est sauté (déterministe : reconstruire
donnerait les mêmes octets). Les SHA-256 sont consignés dans
nulls_893_next_files.json (même format que nulls_893_files.json).

Usage : python3 build_nulls_next_local.py [--check N]
  --check N : au lieu de construire, revérifie N fichiers pris au hasard
  (reconstruction + comparaison SHA).
Aucun run pipeline ici — construction de données seulement.
"""
import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from build_null_893 import build_nul  # noqa: E402

PDAC = Path("/home/hatch/workspace/runs/pdac-v6")
NEXT = Path(__file__).resolve().parent
GRAINES = list(range(9111, 9301))

# (nom paire, CSV reel de base) — memes bases que run_nulls_893_e2.sh
PAIRES_E2 = [
    ("geo21501", "pdac_869_geo21501_fluxes"),
    ("geo79668", "pdac_870_geo79668_fluxes"),
    ("geo60979", "pdac_871_geo60979_fluxes"),
    ("yeh_ff", "pdac_874_yeh_ff_fluxes"),
    ("geo57495", "pdac_879_geo57495_fluxes"),
    ("gdc_organoid", "pdac_885_gdc_organoid_fluxes"),
    ("gse194249", "pdac_888_gse194249_fluxes"),
]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", type=int, default=0,
                    help="Reverifie N fichiers au hasard au lieu de construire")
    args = ap.parse_args()

    record_path = NEXT / "nulls_893_next_files.json"
    if record_path.exists():
        record = json.load(open(record_path))
        fichiers = dict(record["fichiers"])
    else:
        fichiers = {}

    if args.check:
        rng = random.Random(20261122)
        noms = rng.sample(sorted(fichiers), min(args.check, len(fichiers)))
        ok = 0
        for nom in noms:
            base, _, seed = nom[:-4].rpartition("_nul_s")
            src = PDAC / f"{base}.csv"
            tmp = f"/tmp/check_{nom}"
            s = build_nul(str(src), int(seed), tmp)
            if s == fichiers[nom]:
                ok += 1
            else:
                print(f"ECART {nom} : reconstruit {s} != consigne {fichiers[nom]}")
        print(f"check : {ok}/{len(noms)} conformes")
        return 0 if ok == len(noms) else 1

    n_nouveaux = 0
    for nom, base in PAIRES_E2:
        src = PDAC / f"{base}.csv"
        for seed in GRAINES:
            out_name = f"{base}_nul_s{seed}.csv"
            out = PDAC / out_name
            if out.exists():
                if out_name not in fichiers:
                    fichiers[out_name] = sha(out)
                continue
            fichiers[out_name] = build_nul(str(src), seed, str(out))
            n_nouveaux += 1
        print(f"[{nom}] construit/saute -> {len(GRAINES)} nuls (nouveaux cumul : {n_nouveaux})",
              flush=True)

    with open(record_path, "w") as f:
        json.dump({"fichiers": fichiers, "n_fichiers": len(fichiers),
                   "graines": GRAINES, "paires": [p[0] for p in PAIRES_E2]},
                  f, indent=2, ensure_ascii=False)
    print(f"ecrit: {record_path} ({len(fichiers)} fichiers, {n_nouveaux} nouveaux)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
