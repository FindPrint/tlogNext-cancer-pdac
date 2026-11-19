#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construction des CSV de contrôle §8.48 (PROTOCOL_immrot_domination.md).
- (d2) Permutation partielle : CSV dédoublonnés réels, bloc analysé permuté
  CONJOINTEMENT, fraction q de lignes FIXÉES (default_rng(1234) frais par CSV),
  le reste permuté entre elles. Contrôle intact.
- (d3) Croisés inter-familles (porte G OUVERTE : 178/178 concordants, MD5 ok,
  0 NaN — voir immrot_848_gate.json) : X1 contrôle CD8A (immunitaire) sur les
  12 flux PARP ; X2 contrôle POLQ (PARP) sur les 12 flux immunitaires.
  Jointure par index de ligne (même patient par ligne, KRAS brut croissant
  dans les deux bases). Nuls : bloc analysé permuté conjointement,
  default_rng(42) frais par fichier, contrôle intact.
Vérifications : contrôle intact, multi-ensembles conservés, fraction fixée = q,
tri croissant du contrôle, 0 NaN. Sorties : CSV + immrot_848_csv_sha.json
+ manifest_v62_immrot_848.txt (8 runs).
"""
import hashlib
import json

import numpy as np
import pandas as pd

OUT = "/home/hatch/workspace/runs/pdac-v6"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(df, path):
    df.to_csv(path, index=False)
    return sha(path)


def partial_permutation(df, q, seed=1234):
    """Permute conjointement le bloc analysé (colonnes 1..), en fixant une
    fraction q des lignes. Retourne (nouveau df, indices fixés)."""
    n = len(df)
    rng = np.random.default_rng(seed)
    k = int(round(q * n))
    fixed = np.sort(rng.permutation(n)[:k])
    fixed_set = set(fixed.tolist())
    moving = np.array([i for i in range(n) if i not in fixed_set])
    sub = rng.permutation(len(moving))
    block = df.iloc[:, 1:].to_numpy()
    new_block = block.copy()
    new_block[moving] = block[moving[sub]]
    out = df.copy()
    out.iloc[:, 1:] = new_block
    return out, fixed


def joint_permutation_nul(df, seed=42):
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(df))
    out = df.copy()
    out.iloc[:, 1:] = df.iloc[:, 1:].to_numpy()[perm]
    return out


def check_multiset(a, b, label):
    for c in a.columns:
        assert sorted(a[c].tolist()) == sorted(b[c].tolist()), \
            f"{label}: multi-ensemble différent sur {c}"
    assert int(a.isna().sum().sum()) == 0 and int(b.isna().sum().sum()) == 0


def main():
    shas = {}
    manifest = []

    # ---- (d2) Permutation partielle ----
    pp_specs = [
        ("pdac_immune_tcga_fluxes_immrot_CD8A_dedup.csv",
         "pdac_immune_tcga_fluxes_immrot_CD8A_pp50.csv",
         "results_fast_v62_immrot848_cd8a_pp50", 0.50),
        ("pdac_immune_tcga_fluxes_immrot_CD8A_dedup.csv",
         "pdac_immune_tcga_fluxes_immrot_CD8A_pp25.csv",
         "results_fast_v62_immrot848_cd8a_pp25", 0.25),
        ("pdac_immune_tcga_fluxes_immrot_CD68_dedup.csv",
         "pdac_immune_tcga_fluxes_immrot_CD68_pp50.csv",
         "results_fast_v62_immrot848_cd68_pp50", 0.50),
        ("pdac_tcga_fluxes_v4r_cldn18_dedup.csv",
         "pdac_tcga_fluxes_v4r_cldn18_pp50.csv",
         "results_fast_v62_immrot848_cldn18_pp50", 0.50),
    ]
    for src, dst, outdir, q in pp_specs:
        df = pd.read_csv(f"{OUT}/{src}")
        ctrl = df.columns[0]
        new, fixed = partial_permutation(df, q, seed=1234)
        # vérifications
        assert (new[ctrl].values == df[ctrl].values).all(), f"{dst}: contrôle bougé"
        check_multiset(df, new, dst)
        # fraction de lignes du bloc vraiment inchangées : les k fixées le sont
        # toutes ; parmi les lignes permutées, quelques-unes peuvent retomber
        # sur leur place par hasard (point fixe de la permutation) — attendu ~1.
        same = int((new.iloc[:, 1:].values == df.iloc[:, 1:].values).all(axis=1).sum())
        print(f"{dst}: q={q} fixées={len(fixed)}/{len(df)} "
              f"lignes_bloc_inchangées={same} (dont hasard: {same - len(fixed)})")
        assert same >= len(fixed) and same - len(fixed) <= 5, \
            f"{dst}: q non respectée ({same})"
        shas[dst] = write_csv(new, f"{OUT}/{dst}")
        manifest.append((dst.replace(".csv", "").upper().replace("PDAC_", "IMMROT848_"),
                         f"{OUT}/{dst}", outdir))
        print(f"Écrit : {dst} SHA {shas[dst][:12]}...")

    # ---- (d3) Croisés inter-familles (porte G ouverte) ----
    imm = pd.read_csv(f"{OUT}/pdac_immune_tcga_fluxes.csv")
    parp = pd.read_csv(f"{OUT}/pdac_tcga_fluxes_parp.csv")
    assert len(imm) == len(parp) == 178
    imm_flux = [c for c in imm.columns if c != "step"]
    parp_flux = [c for c in parp.columns if c != "step"]
    assert len(imm_flux) == 12 and len(parp_flux) == 12

    # X1 : contrôle CD8A, analysés = 12 flux PARP
    order1 = imm["CD8A"].sort_values(ascending=True).index
    x1 = pd.DataFrame({"CD8A": imm.loc[order1, "CD8A"].values})
    for g in parp_flux:
        x1[g] = parp.loc[order1, g].values
    assert (np.diff(x1["CD8A"].values) >= 0).all()
    assert int(x1.isna().sum().sum()) == 0
    # vérification multi-ensembles : chaque colonne = la colonne de base
    for g in parp_flux:
        assert sorted(x1[g].tolist()) == sorted(parp[g].tolist())
    assert sorted(x1["CD8A"].tolist()) == sorted(imm["CD8A"].tolist())
    shas["xfam_cd8a_over_parp.csv"] = write_csv(
        x1, f"{OUT}/xfam_cd8a_over_parp.csv")
    x1n = joint_permutation_nul(x1, seed=42)
    assert (x1n["CD8A"].values == x1["CD8A"].values).all()
    check_multiset(x1, x1n, "xfam_cd8a_over_parp_nul")
    shas["xfam_cd8a_over_parp_nul.csv"] = write_csv(
        x1n, f"{OUT}/xfam_cd8a_over_parp_nul.csv")
    print("Écrit : xfam_cd8a_over_parp.csv (+nul)")

    # X2 : contrôle POLQ, analysés = 12 flux immunitaires
    order2 = parp["POLQ"].sort_values(ascending=True).index
    x2 = pd.DataFrame({"POLQ": parp.loc[order2, "POLQ"].values})
    for g in imm_flux:
        x2[g] = imm.loc[order2, g].values
    assert (np.diff(x2["POLQ"].values) >= 0).all()
    assert int(x2.isna().sum().sum()) == 0
    for g in imm_flux:
        assert sorted(x2[g].tolist()) == sorted(imm[g].tolist())
    assert sorted(x2["POLQ"].tolist()) == sorted(parp["POLQ"].tolist())
    shas["xfam_polq_over_immune.csv"] = write_csv(
        x2, f"{OUT}/xfam_polq_over_immune.csv")
    x2n = joint_permutation_nul(x2, seed=42)
    assert (x2n["POLQ"].values == x2["POLQ"].values).all()
    check_multiset(x2, x2n, "xfam_polq_over_immune_nul")
    shas["xfam_polq_over_immune_nul.csv"] = write_csv(
        x2n, f"{OUT}/xfam_polq_over_immune_nul.csv")
    print("Écrit : xfam_polq_over_immune.csv (+nul)")

    manifest += [
        ("IMMROT848_XFAM_CD8A_OVER_PARP", f"{OUT}/xfam_cd8a_over_parp.csv",
         "results_fast_v62_immrot848_xfam_cd8a_over_parp"),
        ("IMMROT848_XFAM_CD8A_OVER_PARP_NUL", f"{OUT}/xfam_cd8a_over_parp_nul.csv",
         "results_fast_v62_immrot848_xfam_cd8a_over_parp_nul"),
        ("IMMROT848_XFAM_POLQ_OVER_IMMUNE", f"{OUT}/xfam_polq_over_immune.csv",
         "results_fast_v62_immrot848_xfam_polq_over_immune"),
        ("IMMROT848_XFAM_POLQ_OVER_IMMUNE_NUL", f"{OUT}/xfam_polq_over_immune_nul.csv",
         "results_fast_v62_immrot848_xfam_polq_over_immune_nul"),
    ]
    assert len(manifest) == 8, f"manifeste : {len(manifest)} lignes, attendu 8"
    with open(f"{OUT}/manifest_v62_immrot_848.txt", "w", encoding="utf-8") as f:
        for name, inp, outd in manifest:
            f.write(f"{name}|{inp}|{outd}\n")
    with open(f"{OUT}/immrot_848_csv_sha.json", "w", encoding="utf-8") as f:
        json.dump(shas, f, indent=2)
    print("Manifeste 8 runs :", f"{OUT}/manifest_v62_immrot_848.txt")
    print("SHA :", json.dumps(shas, indent=2))


if __name__ == "__main__":
    main()
