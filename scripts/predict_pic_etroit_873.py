#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§8.73 (E) — Prédictions hors échantillon AVANT lecture des frais.
Calibre T_H par config sur le corpus ICGC EXISTANT (§8.63), puis
prédit, pour chaque nul frais s41-s60 et chacune des 12 configs ICGC,
G(c), H(c), H_max, E_max, le candidat prédit ĉ = argmax G(c) et
rob-on prédit (H_max >= T_H).
À lancer AVANT la fin du lot v6.2 §8.73 et AVANT toute lecture des
résultats frais. Protocole gelé : PROTOCOL_pic_etroit_873.md
(SHA 28d2326c3ae83676d3e15f7283f0b37ae69a1791bcaa1f50c7b06ee368651a4c).
"""
import datetime
import hashlib
import json
import os

import numpy as np

import pic_etroit_873 as p873

PDAC = p873.PDAC


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def csv_for_immune(label, cohorte):
    if label == f"{cohorte}_reel":
        return f"pdac_immune_{cohorte}_fluxes.csv"
    if label.endswith("_nul42"):
        return f"pdac_immune_{cohorte}_fluxes_nul.csv"
    s = label.rsplit("_s", 1)[1]
    return f"pdac_immune_{cohorte}_fluxes_nul_s{s}.csv"


def main():
    v62 = p873.load_v62()
    ex863 = p873.load_extract863()
    prog, cfg = p873.progress_axis(v62, 70)
    # ---- calibration T_H sur le corpus ICGC existant (35 runs x 12 configs)
    hmax_par_config = {}
    for label, rec in ex863["runs_immune"].items():
        if rec["cohorte"] != "icgc":
            continue
        csv_file = csv_for_immune(label, "icgc")
        mat, cols, _ = p873.load_mat(csv_file)
        for r in rec["all_results"]:
            cfg_t = (r["n_candidates"], r["w_size"], r["min_grp"])
            gh = p873.gh_at_candidates(mat, cfg_t[1], cfg_t[2], cfg_t[0], prog)
            hmax = max(gh["H"]) if gh["H"] else None
            hmax_par_config.setdefault(cfg_t, []).append(
                (float(r["robustness"]), hmax))
    T_H = {}
    for cfg_t, vals in sorted(hmax_par_config.items()):
        on = [h for rob, h in vals if rob > 0.5 and h is not None]
        off = [h for rob, h in vals if rob < 0.05 and h is not None]
        if on and off:
            T_H[str(list(cfg_t))] = (max(off) + min(on)) / 2.0
        else:
            T_H[str(list(cfg_t))] = None
        print(f"[T_H {cfg_t}] n_on={len(on)} n_off={len(off)} "
              f"T_H={T_H[str(list(cfg_t))]}")
    # ---- prédictions sur les 20 nuls frais
    preds = []
    for seed in range(41, 61):
        csv_file = f"pdac_immune_icgc_fluxes_nul_s{seed}.csv"
        mat, cols, _ = p873.load_mat(csv_file)
        e, z, med = p873.row_extremity(mat)
        for cfg_t in p873.ICGC_CONFIGS:
            ncand, w, mingrp = cfg_t
            gh = p873.gh_at_candidates(mat, w, mingrp, ncand, prog)
            winp, nw = p873.win_progress_of(prog, w)
            ek = np.array([e[k:k + w].mean() for k in range(nw)])
            hmax = max(gh["H"]) if gh["H"] else None
            gmax = gh["G"][int(np.argmax(gh["G"]))] if gh["G"] else None
            chat = (gh["candidats"][int(np.argmax(gh["G"]))]
                    if gh["G"] else None)
            th = T_H.get(str(list(cfg_t)))
            preds.append({
                "graine": seed, "csv": csv_file, "config": list(cfg_t),
                "H_max": hmax, "G_max": gmax, "E_max": float(np.max(ek)),
                "candidat_pred_G": chat, "T_H": th,
                "rob_on_predit": bool(th is not None and hmax is not None
                                     and hmax >= th)})
    n_pred_on = sum(1 for p in preds if p["rob_on_predit"])
    out = {
        "protocole": "PROTOCOL_pic_etroit_873.md",
        "protocole_sha": ("28d2326c3ae83676d3e15f7283f0b37ae69a1791bcaa1f50c7b06ee368651a4c"),
        "horodatage_utc": datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "v62_sha": sha(p873.V62_PATH),
        "sha_extract_863": sha(p873.EXTRACT863),
        "sha_nuls_frais": json.load(
            open(os.path.join(PDAC, "nulls_icgc_873_files.json"))),
        "T_H": T_H,
        "n_predictions": len(preds),
        "n_rob_on_predites": n_pred_on,
        "predictions": preds,
    }
    p = os.path.join(PDAC, "pic_etroit_873_predictions.json")
    with open(p, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=str)
    print(f"écrit: pic_etroit_873_predictions.json "
          f"({len(preds)} prédictions, {n_pred_on} rob-on prédites, "
          f"SHA {sha(p)[:12]}…)")


if __name__ == "__main__":
    main()
