#!/usr/bin/env python3
"""Chantier §8.95 — score composite gele, candidate v6.5
(PROTOCOL_composite_v65_895.md). Lecture SEULE des master_results.json
v6.2/v6.1 deja sur disque. AUCUN run du pipeline, AUCUN code modifie
(par ce script ; la copie v6.5 est construite separement, voir §4).
Regle gelee (niveau paire) :
  C_pair = (maxsep_R - maxsep_N)
         + 0,50 x (MC_R - MC_N)
         + 0,50 x (robustness_R - robustness_N)
         + 0,25 x (L7a_R - L7a_N)
ou maxsep = best_config.metrics.max_separation, MC = best_config.score
(ancien composite 0,3/0,3/0,2/0,2), robustness =
best_config.metrics.robustness, L7a = vote signe L7a
(+global_confidence si up, - si down, 0 sinon ; meme convention que
§8.44). Memes 60 paires que §8.56 (V1 8 + V2 48 + V3/V4/V5 4).
Barres C1-C4 (§5 du protocole). Sorties : c65_table.json / .csv.
"""
import csv
import hashlib
import json
import math
import os
from pathlib import Path

import extract_sep_maxsep_856 as e56

HERE = Path(__file__).resolve().parent
PLANCHER = 0.07
W_MC, W_ROB, W_L7A = 0.50, 0.50, 0.25

V62 = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
V61 = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py"
V6 = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py"
V63 = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.3.0_cohen.py"
V64 = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.4.0_cohen.py"
SHA_ATTENDUS = {
    "v6.2": ("f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf", V62),
    "v6.1": ("2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9", V61),
    "v6": ("bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773", V6),
    "v6.3": ("552e735910a1fac183ad2ce5713ffa2888e9214c764b103707eeef1787044ffb", V63),
    "v6.4": ("9ed728da7168925f629258e671971d3e2724c35c812a60d9bd95f5fd8199ea3d", V64),
}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_master(outdir):
    """Lit un master_results.json et renvoie les 4 metriques du best_config
    + L7a signe. Chemin de code distinct de extract_sep_maxsep_856."""
    p = HERE / outdir / "master_results.json"
    if not p.is_file():
        return None, f"absent: {p}"
    data = json.loads(p.read_text())
    try:
        bc = (data["run_pipeline"]["threshold_metadata"]
              ["threshold_optimization"]["best_config"])
        met = bc["metrics"]
        l7a = data["prediction_levels"]["L7a_coherence"]
        conf = float(l7a["global_confidence"])
        direction = str(l7a["consensus_direction"]).lower()
        signed = conf if direction == "up" else (-conf if direction == "down" else 0.0)
        return {
            "maxsep": float(met["max_separation"]),
            "mc_old": float(bc["score"]),
            "robustness": float(met["robustness"]),
            "l7a_signed": signed,
            "l7a_dir": direction,
            "l7a_conf": conf,
            "version": data.get("version"),
            "n": data["reading_synthesis"]["n_samples"],
        }, None
    except (KeyError, TypeError, ValueError) as exc:
        return None, f"champ manquant dans {p}: {exc}"


def c_pair(r, n):
    """Candidat gele, niveau paire. Retourne (C, composantes)."""
    d_maxsep = r["maxsep"] - n["maxsep"]
    d_mc = r["mc_old"] - n["mc_old"]
    d_rob = r["robustness"] - n["robustness"]
    d_l7a = r["l7a_signed"] - n["l7a_signed"]
    c = d_maxsep + W_MC * d_mc + W_ROB * d_rob + W_L7A * d_l7a
    return c, {"d_maxsep": d_maxsep, "d_mc": d_mc, "d_rob": d_rob, "d_l7a": d_l7a}


def main():
    shas = {}
    for nom, (att, path) in SHA_ATTENDUS.items():
        got = sha(path) if os.path.exists(path) else "INTROUVABLE"
        shas[nom] = {"attendu": att, "observe": got, "ok": got == att}
    print("SHA avant travaux : " +
          ", ".join(f"{k}={'OK' if v['ok'] else 'ECART'}" for k, v in shas.items()))
    manquants, versions_bad, ecarts_pub = [], [], []
    lignes = []

    def ajouter(portee, nom, rep_r, rep_n):
        r, e1 = load_master(rep_r)
        n, e2 = load_master(rep_n)
        if e1:
            manquants.append(f"{nom} REEL: {e1}")
            return
        if e2:
            manquants.append(f"{nom} NUL: {e2}")
            return
        for cote, v in (("REEL", r), ("NUL", n)):
            if v["version"] not in ("v6.2.0-L7aL7b-CohenD-short",
                                    "v6.1.0-L7aL7b-CohenD-short"):
                versions_bad.append(f"{nom} {cote}: {v['version']}")
        c, comp = c_pair(r, n)
        c_sans_l7a = comp["d_maxsep"] + W_MC * comp["d_mc"] + W_ROB * comp["d_rob"]
        c_sans_rob = comp["d_maxsep"] + W_MC * comp["d_mc"] + W_L7A * comp["d_l7a"]
        lignes.append({
            "scope": portee, "paire": nom, "n": r["n"],
            "maxsep_R": r["maxsep"], "maxsep_N": n["maxsep"],
            "d_maxsep": comp["d_maxsep"],
            "mc_old_R": r["mc_old"], "mc_old_N": n["mc_old"],
            "d_mc_old": comp["d_mc"],
            "robust_R": r["robustness"], "robust_N": n["robustness"],
            "d_rob": comp["d_rob"],
            "l7a_R": r["l7a_signed"], "l7a_N": n["l7a_signed"],
            "l7a_dir_R": r["l7a_dir"], "l7a_dir_N": n["l7a_dir"],
            "d_l7a": comp["d_l7a"],
            "C": c, "C_sans_l7a": c_sans_l7a, "C_sans_rob": c_sans_rob,
            "version_R": r["version"], "version_N": n["version"],
        })

    for nom, rr, nn in e56.PRINCIPALES:
        ajouter("V1_principales", nom, rr, nn)
    for (fam, ctrl), cotes in sorted(e56.dossiers_rotations().items()):
        ajouter("V2_rotations", f"{fam}_{ctrl}", cotes["REEL"], cotes["NUL"])
    for nom, rr, nn in e56.DESCRIPTIFS:
        ajouter("V3_V4_V5_descriptif", nom, rr, nn)

    # --- Garde-fous C4(b)(c) : recoupements a 1e-9 ---
    s844 = {}
    with open(HERE / "ssep_844_rotations.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            s844[f"{row['famille']}_{row['controle']}"] = row
    for lig in lignes:
        if lig["scope"] == "V2_rotations" and lig["paire"] in s844:
            if abs(lig["d_mc_old"] - float(s844[lig["paire"]]["d_mc"])) > 1e-9:
                ecarts_pub.append(f"{lig['paire']}: d_mc_old relu vs §8.44")
            if abs(lig["d_maxsep"] - float(s844[lig["paire"]]["d_maxsep"])) > 1e-9:
                ecarts_pub.append(f"{lig['paire']}: d_maxsep relu vs §8.44")
    ph2 = {}
    with open(HERE / "v62_phase2_table.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            ph2[row["paire"]] = row
    for lig in lignes:
        if lig["scope"] == "V1_principales" and lig["paire"] in ph2:
            if abs(lig["d_mc_old"] - float(ph2[lig["paire"]]["d_mc"])) > 1e-9:
                ecarts_pub.append(f"{lig['paire']}: d_mc_old relu vs phase2")
    for tab in ("v63_mc_table.json", "v64_mc_table.json",
                "sep_maxsep_856_table.json"):
        ref = {r["paire"]: r
               for r in json.loads((HERE / tab).read_text())["paires"]}
        for lig in lignes:
            if lig["paire"] in ref:
                r = ref[lig["paire"]]
                for cle in ("maxsep_R", "maxsep_N", "d_maxsep",
                            "mc_old_R", "mc_old_N", "d_mc_old"):
                    if cle in r and abs(lig[cle] - r[cle]) > 1e-9:
                        ecarts_pub.append(f"{lig['paire']}: {cle} relu vs {tab}")
                if "robust_R" in r:
                    for cle in ("robust_R", "robust_N"):
                        if abs(lig[cle] - r[cle]) > 1e-9:
                            ecarts_pub.append(f"{lig['paire']}: {cle} relu vs {tab}")

    # --- Portes C1-C3 (plancher 0,07) ---
    rot = [l for l in lignes if l["scope"] == "V2_rotations"]
    princ = [l for l in lignes if l["scope"] == "V1_principales"]
    descr = [l for l in lignes if l["scope"] == "V3_V4_V5_descriptif"]
    portes = {
        "C1_rotations_30_48": e56.compter({l["paire"]: l["C"] for l in rot}, PLANCHER),
        "C2_principales_6_8_et_7_8_positifs": e56.compter(
            {l["paire"]: l["C"] for l in princ}, PLANCHER),
        "C3_HP35_0_30": [l for l in lignes if l["paire"] == "HP35"][0]["C"],
    }
    portes["C1_passe"] = portes["C1_rotations_30_48"]["n_ok"] >= 30
    portes["C2_passe"] = (portes["C2_principales_6_8_et_7_8_positifs"]["n_ok"] >= 6
                          and portes["C2_principales_6_8_et_7_8_positifs"]["n_positifs"] >= 7)
    portes["C3_passe"] = portes["C3_HP35_0_30"] >= 0.30
    # --- Sensibilites (non decisives) ---
    sens = {
        "C1_a_24_48": e56.compter({l["paire"]: l["C"] for l in rot}, PLANCHER)["n_ok"] >= 24,
        "plancher_0_05": {
            "V1": e56.compter({l["paire"]: l["C"] for l in princ}, 0.05),
            "V2": e56.compter({l["paire"]: l["C"] for l in rot}, 0.05)},
        "plancher_0_10": {
            "V1": e56.compter({l["paire"]: l["C"] for l in princ}, 0.10),
            "V2": e56.compter({l["paire"]: l["C"] for l in rot}, 0.10)},
        "C_sans_l7a": {
            "V1": e56.compter({l["paire"]: l["C_sans_l7a"] for l in princ}, PLANCHER),
            "V2": e56.compter({l["paire"]: l["C_sans_l7a"] for l in rot}, PLANCHER)},
        "C_sans_rob": {
            "V1": e56.compter({l["paire"]: l["C_sans_rob"] for l in princ}, PLANCHER),
            "V2": e56.compter({l["paire"]: l["C_sans_rob"] for l in rot}, PLANCHER)},
        "maxsep_seul_rappel": {
            "V1": e56.compter({l["paire"]: l["d_maxsep"] for l in princ}, PLANCHER),
            "V2": e56.compter({l["paire"]: l["d_maxsep"] for l in rot}, PLANCHER)},
        "familles_V2": {},
    }
    for fam in ("IMMROT", "V4ROT", "PARPROT", "DEPMAPROT"):
        sous = [l for l in rot if l["paire"].startswith(fam + "_")]
        sens["familles_V2"][fam] = e56.compter(
            {l["paire"]: l["C"] for l in sous}, PLANCHER)
    descriptifs = {l["paire"]: {"C": l["C"], "d_maxsep": l["d_maxsep"],
                                "d_mc_old": l["d_mc_old"], "d_rob": l["d_rob"],
                                "d_l7a": l["d_l7a"]} for l in descr}
    sortie = {"paires": lignes, "portes": portes, "sensibilites": sens,
              "descriptifs": descriptifs,
              "controles": {"manquants": manquants,
                            "version_non_attendue": versions_bad,
                            "ecarts_vs_publie": ecarts_pub,
                            "gigue_eff": PLANCHER,
                            "formule": "C_pair = d_maxsep + 0,50*d_MC + 0,50*d_rob + 0,25*d_L7a",
                            "poids": {"maxsep": 1.0, "mc": W_MC,
                                      "robustness": W_ROB, "l7a": W_L7A},
                            "sha_avant": shas}}
    (HERE / "c65_table.json").write_text(
        json.dumps(sortie, indent=1, ensure_ascii=False))
    colonnes = ["scope", "paire", "n", "maxsep_R", "maxsep_N", "d_maxsep",
                "mc_old_R", "mc_old_N", "d_mc_old", "robust_R", "robust_N",
                "d_rob", "l7a_R", "l7a_N", "d_l7a", "C", "C_sans_l7a",
                "C_sans_rob", "version_R", "version_N"]
    with open(HERE / "c65_table.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=colonnes)
        w.writeheader()
        for l in lignes:
            w.writerow({k: l.get(k, "") for k in colonnes})

    print(f"paires lues: {len(lignes)} (V1: {len(princ)}, V2: {len(rot)}, "
          f"descriptif: {len(descr)} attendus 4)")
    print(f"manquants: {manquants if manquants else 'AUCUN'}")
    print(f"version non attendue: {versions_bad if versions_bad else 'AUCUNE'}")
    print(f"ecarts vs publie: {ecarts_pub if ecarts_pub else 'AUCUN'}")
    c1 = portes["C1_rotations_30_48"]
    print(f"C1 rotations: {c1['n_ok']}/{c1['n']} dir={c1['direction']:+d} "
          f"positifs={c1['n_positifs']}/{c1['n']} somme={c1['somme']:+.4f} "
          f"-> {'PASSE' if portes['C1_passe'] else 'ECHOUE'} (barre 30/48)")
    c2 = portes["C2_principales_6_8_et_7_8_positifs"]
    print(f"C2 principales: {c2['n_ok']}/8 >0,07, positifs={c2['n_positifs']}/8 "
          f"somme={c2['somme']:+.4f} -> {'PASSE' if portes['C2_passe'] else 'ECHOUE'} "
          f"(barre 6/8 et 7/8)")
    print(f"C3 HP35: C={portes['C3_HP35_0_30']:.4f} -> "
          f"{'PASSE' if portes['C3_passe'] else 'ECHOUE'} (barre 0,30)")
    for k, v in descriptifs.items():
        print(f"descriptif {k}: C={v['C']:+.4f} (d_maxsep={v['d_maxsep']:+.4f}, "
              f"d_mc={v['d_mc_old']:+.4f}, d_rob={v['d_rob']:+.4f}, d_l7a={v['d_l7a']:+.4f})")
    print("ecrit: c65_table.json, c65_table.csv")


if __name__ == "__main__":
    main()
