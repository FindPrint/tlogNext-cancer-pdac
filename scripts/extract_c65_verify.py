#!/usr/bin/env python3
"""§8.95 — Re-extraction INDEPENDANTE du composite v6.5 (porte C4a).
Chemin de code distinct de extract_c65.py : aucune importation de
extract_c65 ni de extract_sep_maxsep_856 ; navigation JSON manuelle
(.get en cascade), paires reconstruites depuis le manifeste brut et
les listes V1/V3-V5 recopiees ici, formule re-derivee depuis le
protocole. Compare C a 0,0 exact sur les 120/120 runs.
Sortie : c65_verify.json (inclut les SHA v6.x APRES travaux, porte C4d).
"""
import hashlib
import json
import os

PDAC = "/home/hatch/workspace/runs/pdac-v6"

V1 = [
    ("HP35", "results_fast_v62_hp35", "results_fast_v62_hp35_nul"),
    ("TCGA_v4", "results_fast_v62_tcga_v4", "results_fast_v62_tcga_v4_nul"),
    ("GSE71729", "results_fast_v62_geo71729", "results_fast_v62_geo71729_nul"),
    ("GSE62452", "results_fast_v62_geo62452", "results_fast_v62_geo62452_nul"),
    ("ICGC", "results_fast_v62_icgc", "results_fast_v62_icgc_nul"),
    ("IMMUNE_TCGA", "results_fast_v62_immune_tcga", "results_fast_v62_immune_tcga_nul"),
    ("PARP_TCGA", "results_fast_v62_parp_tcga", "results_fast_v62_parp_tcga_nul"),
    ("DEPMAP", "results_fast_v62_depmap", "results_fast_v62_depmap_nul"),
]
DESCR = [
    ("TESTA_PROLIF", "results_fast_v62_prolif", "results_fast_v62_prolif_nul"),
    ("MTAP_PRMT5FLUX", "results_fast_v62_prmt5flux", "results_fast_v62_prmt5flux_nul"),
    ("MTAP_SERIES", "results_fast_v62_mtap", "results_fast_v62_mtap_nul"),
    ("V4R_PURITY", "results_fast_v62_v4r_purity", "results_fast_v62_v4r_purity_nul"),
]
ROT_EXIST = {
    "V4ROT_CLDN18": ("results_fast_v61_v4r_cldn18_dedup",
                     "results_fast_v61_v4r_cldn18_dedup_nul"),
    "IMMROT_CTLA4": ("results_fast_v62_immrot_ctla4_dedup",
                     "results_fast_v62_immrot_ctla4_dedup_nul"),
    "DEPMAPROT_ACO2": ("results_fast_v62_depmaprot_aco2_dedup",
                       "results_fast_v62_depmaprot_aco2_dedup_nul_sp"),
    "PARPROT_PARP1": ("results_fast_v62_parprot_parp1_dedup",
                      "results_fast_v62_parprot_parp1_dedup_nul_sp"),
}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_run(d):
    """Autre navigation : .get en cascade, pas d'indexation directe."""
    with open(os.path.join(PDAC, d, "master_results.json")) as f:
        j = json.load(f)
    rp = j.get("run_pipeline") or {}
    tm = rp.get("threshold_metadata") or {}
    to = tm.get("threshold_optimization") or {}
    bc = to.get("best_config") or {}
    met = bc.get("metrics") or {}
    pl = j.get("prediction_levels") or {}
    l7 = pl.get("L7a_coherence") or {}
    conf = float(l7.get("global_confidence"))
    direc = str(l7.get("consensus_direction")).lower()
    if direc == "up":
        l7a = conf
    elif direc == "down":
        l7a = -conf
    else:
        l7a = 0.0
    return (float(met.get("max_separation")), float(bc.get("score")),
            float(met.get("robustness")), l7a)


def rotations():
    table = {}
    with open(os.path.join(PDAC, "manifest_v62_dedup_844.txt")) as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne or ligne.startswith("#"):
                continue
            nom, _entree, sortie = ligne.split("|")
            base = nom[len("DEDUP844_"):]
            nul = base.endswith("_NUL")
            if nul:
                base = base[:-4]
            fam, ctrl = base.rsplit("_", 1)
            table.setdefault(f"{fam}_{ctrl}", {})["NUL" if nul else "REEL"] = sortie
    for k, (r, n) in ROT_EXIST.items():
        table[k] = {"REEL": r, "NUL": n}
    return table


def main():
    ref = json.load(open(os.path.join(PDAC, "c65_table.json")))
    ref_c = {p["paire"]: p["C"] for p in ref["paires"]}
    paires = [(n, r, u) for n, r, u in V1]
    paires += [(f"{k}", v["REEL"], v["NUL"]) for k, v in sorted(rotations().items())]
    paires += [(n, r, u) for n, r, u in DESCR]
    ecarts, manquants = [], []
    n_runs = 0
    for nom, dr, dn in paires:
        try:
            mr, mn = read_run(dr), read_run(dn)
        except Exception as exc:
            manquants.append(f"{nom}: {exc}")
            continue
        n_runs += 2
        c = ((mr[0] - mn[0]) + 0.50 * (mr[1] - mn[1])
             + 0.50 * (mr[2] - mn[2]) + 0.25 * (mr[3] - mn[3]))
        if nom not in ref_c:
            ecarts.append(f"{nom}: absente de c65_table.json")
        elif c != ref_c[nom]:
            ecarts.append(f"{nom}: re-extraction {c!r} != table {ref_c[nom]!r} "
                          f"(diff {c - ref_c[nom]:.3e})")
    shas_apres = {}
    for nom, path, att in (
            ("v6.2", "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py",
             "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"),
            ("v6.1", "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py",
             "2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9"),
            ("v6", "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py",
             "bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773"),
            ("v6.3", "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.3.0_cohen.py",
             "552e735910a1fac183ad2ce5713ffa2888e9214c764b103707eeef1787044ffb"),
            ("v6.4", "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.4.0_cohen.py",
             "9ed728da7168925f629258e671971d3e2724c35c812a60d9bd95f5fd8199ea3d")):
        got = sha(path)
        shas_apres[nom] = {"attendu": att, "observe": got, "ok": got == att}
    out = {"n_paires": len(paires), "n_runs": n_runs,
           "ecarts": ecarts, "manquants": manquants,
           "c4a_0_0_exact_120_120": (not ecarts and not manquants and n_runs == 120),
           "sha_apres": shas_apres,
           "c4d_tous_inchanges": all(v["ok"] for v in shas_apres.values())}
    with open(os.path.join(PDAC, "c65_verify.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"paires re-extraites: {len(paires)} ({n_runs} runs)")
    print(f"ecarts: {ecarts if ecarts else 'AUCUN'}")
    print(f"manquants: {manquants if manquants else 'AUCUN'}")
    print(f"C4a 0,0 exact 120/120 : {out['c4a_0_0_exact_120_120']}")
    print("SHA apres : " + ", ".join(
        f"{k}={'OK' if v['ok'] else 'ECART'}" for k, v in shas_apres.items()))
    print("ecrit: c65_verify.json")


if __name__ == "__main__":
    main()
