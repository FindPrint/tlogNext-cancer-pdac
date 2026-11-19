#!/usr/bin/env python3
"""Rotations sans doublon, chantier §8.44 (19 nov. 2026).
Refait les 44 paires restantes (les 4 déjà refaites au §8.41 sont exclues :
CLDN18/V4ROT v6.1, CTLA4/IMMROT, ACO2/DEPMAPROT, PARP1/PARPROT).
Méthode — MÊME PERMUTATION que l'original, partout (leçon du §8.41.3 :
le nul à nouvelle permutation mélangeait retrait du doublon et nouvelle
permutation ; à n=45 le nul variait de 0,26 à 0,43 entre deux permutations) :
- CSV réel dédoublonné : on retire seulement la colonne doublon du flux
  contrôle (colonne k, valeurs identiques à la col. 0 vérifiées) ;
  contrôle, ordre et autres flux inchangés, ligne par ligne.
- CSV nul dédoublonné : on part du CSV _nul.csv ORIGINAL (même permutation
  que la rotation avec doublon) et on retire seulement la colonne doublon
  (multi-ensemble égal à la col. 0 vérifié ; les 11 autres colonnes
  identiques ligne par ligne au nul original).
Aucune valeur recalculée ni imputée. Sorties : *_dedup.csv et
*_dedup_nul.csv ; manifeste manifest_v62_dedup_844.txt ; SHA-256 affichés.
Liste des 44 paires lue dans PROVENANCE_rotations_v61.md (bloc JSON),
dont les SHA des 96 CSV d'origine ont été vérifiés avant construction
(96/96 conformes, 4 bases conformes).
"""
import hashlib
import json
import re

import numpy as np
import pandas as pd

BASE = "."
DONE = {("V4ROT", "CLDN18"), ("IMMROT", "CTLA4"),
        ("DEPMAPROT", "ACO2"), ("PARPROT", "PARP1")}

FAM_PREFIX = {"V4ROT": "v4rot", "DEPMAPROT": "depmaprot",
              "IMMROT": "immrot", "PARPROT": "parprot"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


prov_text = open("PROVENANCE_rotations_v61.md").read()
prov = json.loads(re.search(r"```json\n(.*?)```", prov_text, re.S).group(1))

# Familles -> préfixe de jeu dans la provenance
JEU = {"V4ROT": "tcga_v4", "DEPMAPROT": "depmap",
       "IMMROT": "immune_tcga", "PARPROT": "parp_tcga"}

pairs = []
for fam, jeu_nom in JEU.items():
    jeu = prov["jeux"][jeu_nom]
    for rot, rec in sorted(jeu["rotations"].items()):
        if (fam, rot) in DONE:
            continue
        pairs.append((fam, rot, rec["fichier"], rec["nul"]))
assert len(pairs) == 44, f"paires restantes: {len(pairs)}, attendu 44"

manifest_lines = []
shas = {}
for fam, ctrl, src, nul_src in pairs:
    # --- réel ---
    hdr = open(src).readline().strip().split(",")
    assert hdr[0] == ctrl, f"{src}: col 0 = {hdr[0]}, attendu {ctrl}"
    dup = [i for i in range(1, len(hdr)) if hdr[i] == ctrl]
    assert len(dup) == 1, f"{src}: doublons de {ctrl} en {dup}, attendu 1"
    k = dup[0]
    raw = pd.read_csv(src, header=None, skiprows=1)
    assert np.allclose(raw[0].values, raw[k].values), f"{src}: col {k} != col 0"
    keep = [i for i in range(len(hdr)) if i != k]
    out = raw[keep]
    out.columns = [hdr[i] for i in keep]
    assert list(out.columns).count(ctrl) == 1
    assert out.shape == (len(raw), len(hdr) - 1)
    dst = src[:-4] + "_dedup.csv"
    out.to_csv(dst, index=False)
    # contrôle et ordre inchangés, ligne par ligne
    assert np.allclose(out.iloc[:, 0].values, raw[0].values)
    for j, i in enumerate(keep[1:], start=1):
        assert np.allclose(out.iloc[:, j].values, raw[i].values), f"{src}: col {i} modifiée"

    # --- nul, même permutation que l'original ---
    hdr_n = open(nul_src).readline().strip().split(",")
    assert hdr_n[0] == ctrl and hdr_n.count(ctrl) == 2, f"{nul_src}: en-tête inattendu"
    k_n = [i for i in range(1, len(hdr_n)) if hdr_n[i] == ctrl]
    assert len(k_n) == 1 and k_n[0] == k, f"{nul_src}: doublon en {k_n}, attendu {k}"
    raw_n = pd.read_csv(nul_src, header=None, skiprows=1)
    assert np.allclose(np.sort(raw_n[0].values), np.sort(raw_n[k].values)), \
        f"{nul_src}: col {k} n'est pas une permutation de col 0"
    keep_n = [i for i in range(len(hdr_n)) if i != k]
    out_n = raw_n[keep_n]
    out_n.columns = [hdr_n[i] for i in keep_n]
    assert list(out_n.columns).count(ctrl) == 1
    assert out_n.shape == (len(raw_n), len(hdr_n) - 1)
    for j, i in enumerate(keep_n):
        assert np.allclose(out_n.iloc[:, j].values, raw_n[i].values), \
            f"{nul_src}: col {i} modifiée"
    nul_dst = src[:-4] + "_dedup_nul.csv"
    out_n.to_csv(nul_dst, index=False)

    shas[f"{fam}_{ctrl}"] = {"reel": sha(dst), "nul": sha(nul_dst),
                             "reel_src": sha(src), "nul_src": sha(nul_src),
                             "doublon_col": k, "n": len(out),
                             "colonnes": f"{len(hdr)}->{len(keep)}"}
    outdir = f"results_fast_v62_{FAM_PREFIX[fam]}_{ctrl.lower()}_dedup"
    manifest_lines.append(
        f"DEDUP844_{fam}_{ctrl}|{dst}|{outdir}")
    manifest_lines.append(
        f"DEDUP844_{fam}_{ctrl}_NUL|{nul_dst}|{outdir}_nul")
    print(f"{fam} {ctrl}: doublon_col={k} n={len(out)} "
          f"colonnes {len(hdr)}->{len(keep)}")
    print(f"  {dst} {shas[f'{fam}_{ctrl}']['reel']}")
    print(f"  {nul_dst} {shas[f'{fam}_{ctrl}']['nul']}")

with open("manifest_v62_dedup_844.txt", "w") as fh:
    fh.write("\n".join(manifest_lines) + "\n")
json.dump(shas, open("dedup_844_csv_sha.json", "w"), indent=1)
print(f"paires: {len(pairs)}, lignes manifeste: {len(manifest_lines)}")
print("écrit: manifest_v62_dedup_844.txt, dedup_844_csv_sha.json")
