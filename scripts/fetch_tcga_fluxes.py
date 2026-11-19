#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Télécharge TCGA-PAAD (ARN, z-scores RSEM) depuis l'API cBioPortal et
construit les flux du jour (15 nov. 2026).
Protocole gelé :
- Source : étude paad_tcga_pan_can_atlas_2018, profil
  paad_tcga_pan_can_atlas_2018_rna_seq_v2_mrna_median_Zscores
  (z-scores RSEM relatifs aux échantillons diploïdes), liste d'échantillons
  paad_tcga_pan_can_atlas_2018_rna_seq_v2_mrna (177 patients).
- Sélection des flux PAR LES DONNÉES DU JOUR : les 12 gènes de plus forte
  variance entre les 177 patients, hors KRAS. La variance ne dépend pas de
  l'ordre des lignes : la sélection n'est PAS circulaire avec l'axe.
- Ordre des lignes : z-score KRAS croissant (expression la plus faible
  d'abord). KRAS est l'axe d'ordonnancement, JAMAIS un flux.
- Flux : z-scores des 12 gènes sélectionnés. step = 0..N-1.
- Nul : mêmes lignes permutées, graine 42.
Aucune donnée d'une autre expérience n'entre ici (téléchargement frais
depuis la source publique, pas de réutilisation du fichier local tlog28).
"""
import hashlib
import json
import subprocess
import time

import numpy as np
import pandas as pd

BASE = "https://www.cbioportal.org/api"
STUDY = "paad_tcga_pan_can_atlas_2018"
PROFILE = "paad_tcga_pan_can_atlas_2018_rna_seq_v2_mrna_median_Zscores"
SAMPLE_LIST = "paad_tcga_pan_can_atlas_2018_rna_seq_v2_mrna"
OUT = "/home/hatch/workspace/runs/pdac-v6"
N_FLUX = 12
SEED = 42
PAGE_SIZE = 100000


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def get_json(url, tries=5):
    # Transport par curl (vérifié 3/3 sur /api/genes) : urllib levait
    # IncompleteRead sur les réponses chunked de cBioPortal (15 nov. 2026,
    # 3 tentatives échouées sur pageSize=1000). Même logique de reprise.
    for attempt in range(tries):
        try:
            out = subprocess.run(
                ["curl", "-sS", "--max-time", "120",
                 "-H", "Accept: application/json", url],
                capture_output=True, text=True, timeout=150, check=True,
            )
            return json.loads(out.stdout)
        except Exception as e:  # noqa: BLE001 - retry then raise
            if attempt == tries - 1:
                raise
            print(f"  nouvelle tentative {url[:90]}... ({e})")
            time.sleep(5)


def post_json(url, body, tries=5):
    # Transport par curl, même raison que get_json (IncompleteRead urllib).
    data = json.dumps(body)
    for attempt in range(tries):
        try:
            out = subprocess.run(
                ["curl", "-sS", "--max-time", "170",
                 "-H", "Accept: application/json",
                 "-H", "Content-Type: application/json",
                 "-X", "POST", "-d", data, url],
                capture_output=True, text=True, timeout=200, check=True,
            )
            return json.loads(out.stdout)
        except Exception as e:  # noqa: BLE001 - retry then raise
            if attempt == tries - 1:
                raise
            print(f"  nouvelle tentative POST {url[:90]}... ({e})")
            time.sleep(5)


def main():
    # Passe 1 : balayage du profil complet.
    # CORRECTIF 15 nov. 2026, 07h56 : le GET
    # /molecular-profiles/{id}/molecular-data exige le paramètre entrezGeneId
    # (HTTP 400 sans lui, 3 tentatives échouées, FETCH_TCGA_EXIT:1 à 07h46,
    # rien téléchargé). La passe 1 passe donc par POST /molecular-data/fetch
    # par lots d'entrezGeneIds, après récupération de la liste des gènes via
    # GET /api/genes paginé (entrezGeneId > 0 ; les entrées à entrez négatif,
    # ex. phosphoprotéines, sont exclues). Détail décisif vérifié à 08h00 :
    # le POST exige « molecularProfileIds » (pluriel, liste) — avec le champ
    # singulier « molecularProfileId » (passe 2 d'origine, jamais exécutée),
    # le serveur refuse en 400 « interceptedMolecularDataMultipleStudyFilter
    # must be true ». Avec le pluriel : HTTP 200, 531 lignes pour 3 gènes
    # × 177 échantillons, valeurs identiques au GET (KRAS TCGA-2J-AAB1-01 :
    # -0,562). Même sélection ensuite (variance, top 12 hors KRAS).
    print("Passe 1 : récupération de la liste des gènes...")
    gene_ids = []
    seen = set()
    page = 0
    while True:
        genes = get_json(f"{BASE}/genes?pageSize=1000&pageNumber={page}")
        if not genes:
            break
        for g in genes:
            entrez = g.get("entrezGeneId")
            if entrez is not None and entrez > 0 and int(entrez) not in seen:
                seen.add(int(entrez))
                gene_ids.append(int(entrez))
        print(f"  page {page} : {len(genes)} gènes "
              f"(total {len(gene_ids)} entrez > 0)")
        page += 1
    print(f"Total : {len(gene_ids)} gènes (entrezGeneId > 0)")

    print("Passe 1 : balayage du profil complet (POST par lots)...")
    stats = {}  # entrez -> [n, somme, somme², symbole]
    kras = {}   # sampleId -> valeur KRAS
    samples = set()
    total_rows = 0
    BATCH = 1000
    for start in range(0, len(gene_ids), BATCH):
        batch = gene_ids[start:start + BATCH]
        body = {
            "entrezGeneIds": batch,
            "molecularProfileIds": [PROFILE],
            "sampleListId": SAMPLE_LIST,
        }
        rows = post_json(f"{BASE}/molecular-data/fetch", body)
        for r in rows:
            entrez = r["entrezGeneId"]
            symbol = (r.get("hugoGeneSymbol")
                      or (r.get("gene") or {}).get("hugoGeneSymbol")
                      or str(entrez))
            val = r.get("value")
            if val is None:
                continue
            acc = stats.get(entrez)
            if acc is None:
                stats[entrez] = [1, float(val), float(val) ** 2, symbol]
            else:
                acc[0] += 1
                acc[1] += float(val)
                acc[2] += float(val) ** 2
            samples.add(r["sampleId"])
            if symbol == "KRAS":
                kras[r["sampleId"]] = float(val)
        total_rows += len(rows)
        print(f"  lot {start // BATCH + 1} : {len(rows)} valeurs "
              f"(total {total_rows}, {len(stats)} gènes)")
    print(f"Total : {total_rows} valeurs, {len(stats)} gènes, "
          f"{len(samples)} échantillons, KRAS sur {len(kras)} échantillons")
    assert len(kras) == len(samples), "KRAS manquant sur certains échantillons"

    var = {}
    for entrez, (n, s, s2, symbol) in stats.items():
        if n < 50:
            continue
        mean = s / n
        var[entrez] = (s2 / n - mean ** 2, symbol, n)
    ranking = sorted(var.items(), key=lambda kv: -kv[1][0])
    kras_entrez = [e for e, (_, sym, _) in var.items() if sym == "KRAS"]
    assert len(kras_entrez) == 1
    top = [(e, v) for e, v in ranking if e != kras_entrez[0]][:N_FLUX]
    print("Top 12 gènes par variance (hors KRAS) :")
    for entrez, (v, symbol, n) in top:
        print(f"  {symbol:12s} (entrez {entrez}) variance={v:.3f} n={n}")

    # Passe 2 : valeurs complètes des 12 gènes sélectionnés.
    print("Passe 2 : récupération des 12 gènes sélectionnés...")
    body = {
        "entrezGeneIds": [int(e) for e, _ in top],
        "molecularProfileIds": [PROFILE],
        "sampleListId": SAMPLE_LIST,
    }
    rows = post_json(f"{BASE}/molecular-data/fetch", body)
    print(f"  {len(rows)} valeurs récupérées")
    by_gene = {}
    for r in rows:
        by_gene.setdefault(r["hugoGeneSymbol"], {})[r["sampleId"]] = float(r["value"])

    order = sorted(kras, key=lambda s: kras[s])
    flux_cols = [v[1] for _, v in top]
    data = {"step": np.arange(len(order))}
    for symbol in flux_cols:
        vals = [by_gene[symbol][s] for s in order]
        assert len(vals) == len(order) and not any(np.isnan(vals))
        data[symbol] = vals
    out = pd.DataFrame(data)
    out_path = f"{OUT}/pdac_tcga_fluxes.csv"
    out.to_csv(out_path, index=False)
    print(f"Écrit : {out_path} ({out.shape[0]} lignes x {out.shape[1]} colonnes)")

    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(out))
    nul = out.copy()
    nul.iloc[:, 1:] = out.iloc[:, 1:].to_numpy()[perm]
    nul_path = f"{OUT}/pdac_tcga_fluxes_nul.csv"
    nul.to_csv(nul_path, index=False)
    print(f"Écrit : {nul_path} (permutation graine {SEED})")

    provenance = {
        "date": "2026-11-15",
        "source": {
            "étude": STUDY,
            "titre": "Pancreatic Adenocarcinoma (TCGA, PanCancer Atlas)",
            "publication": "TCGA, Cell 2018 (PMID 29625055)",
            "profil": PROFILE,
            "liste_échantillons": SAMPLE_LIST,
            "api": BASE,
            "valeurs_lues": total_rows,
            "gènes_lus": len(stats),
            "échantillons": len(samples),
        },
        "sélection_gènes": {
            "méthode": "variance entre les patients, par gène ; top 12 hors KRAS "
                       "(la variance ne dépend pas de l'ordre des lignes)",
            "gènes": [
                {"gène": v[1], "entrez": int(e), "variance": round(float(v[0]), 4),
                 "n": int(v[2])}
                for e, v in top
            ],
        },
        "ordre": "z-score KRAS croissant (expression la plus faible d'abord) ; "
                 "KRAS = axe d'ordonnancement, jamais un flux",
        "flux_csv": {"fichier": out_path, "sha256": sha(out_path),
                     "lignes": int(out.shape[0]), "colonnes": list(out.columns)},
        "nul_csv": {"fichier": nul_path, "sha256": sha(nul_path),
                    "méthode": "mêmes lignes permutées, graine 42"},
        "règle": "Données du jour uniquement (téléchargement frais depuis "
                 "cBioPortal). Aucune donnée ni conclusion d'une autre "
                 "expérience importée (règle 15 nov. 2026).",
    }
    with open(f"{OUT}/PROVENANCE_tcga.md", "w", encoding="utf-8") as f:
        f.write("# Provenance — flux PDAC du jour (TCGA-PAAD)\n\n")
        f.write("```json\n" + json.dumps(provenance, indent=2, ensure_ascii=False) + "\n```\n")
    print("Provenance écrite : PROVENANCE_tcga.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
