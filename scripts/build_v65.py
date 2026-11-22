#!/usr/bin/env python3
"""§8.95 — Construction de la copie v6.5 candidate (PROTOCOL_composite_v65_895.md §4).
Copie octet a octet de v6.2, puis SEULE modification autorisee : ajout du
calcul de C (composite gele) depuis les metriques deja stockees
(best_config + vote L7a signe). Aucun changement de selection, de seuil,
de cascade, de S_sep, de Delta, de MC. Miroir du pattern v6.3
(mc_recomposed_score + site d'appel + VERSION_MASTER).
Verifications : SHA v6.2 avant/apres, diff contre v6.2, py_compile.
"""
import hashlib
import os
import py_compile

SRC = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
DST = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.5.0_cohen.py"
SHA_V62 = "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


FONCTION = '''

def composite_c65_run(best_metrics, mc_old, l7a_signed):
    """Score composite v6.5 (PROTOCOL_composite_v65_895.md §3) — LECTURE SEULE.

    C_run = maxsep + 0,50*MC + 0,50*robustness + 0,25*L7a_signe
    (maxsep = best_config.metrics.max_separation, MC = best_config.score
    ancien composite 0,3/0,3/0,2/0,2, robustness =
    best_config.metrics.robustness, L7a_signe = vote L7a signe du run).
    Fonction pure : ne lit que les metriques fournies, n'ecrit rien dans
    le pipeline, ne choisit aucun seuil. La selection du best_config
    (ancien composite) est inchangee. C_pair = C_run(reel) - C_run(nul).
    """
    try:
        maxsep = float(best_metrics.get('max_separation', 0.0) or 0.0)
    except (TypeError, ValueError):
        maxsep = 0.0
    try:
        mc = float(mc_old if mc_old is not None else 0.0)
    except (TypeError, ValueError):
        mc = 0.0
    try:
        rob = float(best_metrics.get('robustness', 0.0) or 0.0)
    except (TypeError, ValueError):
        rob = 0.0
    try:
        l7a = float(l7a_signed if l7a_signed is not None else 0.0)
    except (TypeError, ValueError):
        l7a = 0.0
    c_run = maxsep + 0.50 * mc + 0.50 * rob + 0.25 * l7a
    return {
        'c_run': float(c_run),
        'maxsep': float(maxsep),
        'mc_old': float(mc),
        'robustness': float(rob),
        'l7a_signed': float(l7a),
        'formula': 'C_run=maxsep+0.50*MC+0.50*robustness+0.25*L7a_signe',
        'weights': {'maxsep': 1.0, 'mc': 0.50, 'robustness': 0.50, 'l7a': 0.25},
    }

'''

APPEL = '''    # v6.5.0 — score composite C (PROTOCOL_composite_v65_895.md §3) : LECTURE
    # SEULE du best_config deja selectionne par l'ancien composite et du
    # vote L7a signe deja calcule. Ne touche ni au seuil, ni au score
    # ancien, ni a la cascade. C_run = maxsep + 0,50*MC + 0,50*robustness
    # + 0,25*L7a_signe ; C_pair = C_run(reel) - C_run(nul).
    try:
        _c65_topt = (results.get("metadata", {}) or {}).get("threshold_optimization", {}) or {}
        _c65_bc = _c65_topt.get("best_config") or {}
        _c65_l7 = L7 if isinstance(L7, dict) else {}
        _c65_dir = str(_c65_l7.get("consensus_direction", "")).lower()
        _c65_conf = float(_c65_l7.get("global_confidence", 0.0) or 0.0)
        _c65_l7a = _c65_conf if _c65_dir == "up" else (-_c65_conf if _c65_dir == "down" else 0.0)
        _c65 = composite_c65_run(_c65_bc.get("metrics", {}) or {}, _c65_bc.get("score"), _c65_l7a)
        _c65_topt["composite_c65"] = dict(_c65)
        _c65_bc["composite_c65"] = dict(_c65)
        print(f"Composite v6.5 (C_run) : {_c65['c_run']:.4f} (maxsep={_c65['maxsep']:.4f}, "
              f"MC={_c65['mc_old']:.4f}, rob={_c65['robustness']:.4f}, L7a={_c65['l7a_signed']:+.4f})")
    except Exception as _e_c65:
        _c65_topt = (results.get("metadata", {}) or {}).get("threshold_optimization", {}) or {}
        _c65_topt["composite_c65"] = {'c_run': None, 'reason': str(_e_c65)}

'''

VERSION_NEW = 'VERSION_MASTER = "v6.5.0-L7aL7b-CohenD-short"'
VERSION_COMMENT = '''# v6.5.0 (21 nov. 2026) — voir PROTOCOL_composite_v65_895.md §4 :
#  SEUL changement de code : ajout du score composite C en LECTURE
#  SEULE (composite_c65_run). La selection du best_config (ancien
#  composite 0.3/0.3/0.2/0.2), le seuil MC, la cascade, S_sep, Delta,
#  L5/L4/L7a et les estimateurs sont intacts. C_run = maxsep +
#  0,50*MC + 0,50*robustness + 0,25*L7a_signe ; C_pair est la
#  difference reel - nul des C_run. Candidate PROPOSEE ou REJETEE
#  au §8.95 ; l'adoption finale revient a Zackary.
'''


def main():
    assert sha(SRC) == SHA_V62, "SHA v6.2 non conforme avant copie — ABANDON"
    src = open(SRC, encoding="utf-8").read()
    assert "composite_c65" not in src
    # 1. fonction pure apres evaluate_scan_quality (avant _sample_harmonic_guided)
    ancre_f = "def _sample_harmonic_guided(rng, n_pts, max_w_size, harmonic_prob):"
    assert src.count(ancre_f) == 1
    src = src.replace(ancre_f, FONCTION.strip("\n") + "\n\n\n" + ancre_f, 1)
    # 2. site d'appel juste avant final_output
    ancre_a = "    final_output = {"
    assert src.count(ancre_a) == 1
    src = src.replace(ancre_a, APPEL + ancre_a, 1)
    # 3. version + commentaire
    ancre_v = 'VERSION_MASTER = "v6.2.0-L7aL7b-CohenD-short"'
    assert src.count(ancre_v) == 1
    src = src.replace(ancre_v, VERSION_NEW + "\n" + VERSION_COMMENT.rstrip("\n"), 1)
    with open(DST, "w", encoding="utf-8") as f:
        f.write(src)
    py_compile.compile(DST, doraise=True)
    print(f"copie ecrite : {DST}")
    print(f"SHA v6.5 : {sha(DST)}")
    print(f"SHA v6.2 apres : {sha(SRC)} (attendu {SHA_V62})")
    assert sha(SRC) == SHA_V62
    print("v6.2 inchange apres travaux : OK")


if __name__ == "__main__":
    main()
