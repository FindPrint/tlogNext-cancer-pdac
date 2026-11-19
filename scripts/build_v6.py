#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit universal_v6.0.0_cohen.py depuis la v5.9.0f (originale intacte).
Chaque remplacement est vérifié par son nombre d'occurrences attendu.
Échoue bruyamment si un remplacement ne correspond pas.
Le mot "Cliff" ne survit que dans la note v6.0.0 de l'en-tête (la raison),
jamais comme code : 0 occurrence de cliff_delta / cliff_between / cliff_pairs.
"""
import hashlib
import sys

SRC = "/home/hatch/workspace/user/files/universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f_0_fqyq.py"
DST = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py"
ORIG_SHA = "4f80f6a7d0809e802cbc9ec30c0bed552c1c8a95eb58687fd78e4ffd8e808260"

NOTE = (
    "v6.0.0 (15 nov. 2026) — BASCULE COHEN-D PARTOUT, CLIFF RETIRÉ.\n"
    "Raison (preuve mesurée sur HP35, 14 nov. 2026) : les cascades de seuils\n"
    "sont identiques entre Cohen-d et Cliff's delta sur 4 comparaisons sur 4 —\n"
    "fast original (0 / 16 / 90 / 376), fast nul permuté (0 / 204 / 273 / 735),\n"
    "fast sans les 5 premières ns (0 / 225 / 462 / 786), full Cliff contre\n"
    "fast Cohen (0 / 16 / 90 / 376) — alors que Cohen-d est ~11x plus rapide\n"
    "(~4 min par run fast contre ~45 min en Cliff). Cliff's delta est donc\n"
    "retiré partout : modes robust/full/predict passés en cohen_d, fonction\n"
    "de Cliff supprimée, comparaisons entre classes passées en Cohen-d.\n"
    "Fichier d'origine v5.9.0f intact (SHA-256 4f80f6a7...808260).\n"
)

CLIFF_DEF = (
    "def cliff_delta(g1, g2, min_grp=3):\n"
    "    g1, g2 = np.asarray(g1), np.asarray(g2)\n"
    "    g1 = g1[~np.isnan(g1)]\n"
    "    g2 = g2[~np.isnan(g2)]\n"
    "    n1, n2 = len(g1), len(g2)\n"
    "    if n1 < min_grp or n2 < min_grp:\n"
    "        return np.nan\n"
    "    try:\n"
    "        U, _ = stats.mannwhitneyu(g1, g2, alternative='two-sided')\n"
    "        return (2 * U - n1 * n2) / (n1 * n2)\n"
    "    except Exception:\n"
    "        return np.nan\n"
    "\n"
)

# (ancien, nouveau, occurrences attendues)
REPLACEMENTS = [
    ("UNIVERSAL_LOG v5.8 — Multi-horizons",
     "UNIVERSAL_LOG v6.0.0 — Multi-horizons", 1),
    ("conservées, y compris KolmogorovLZ et PermutationEntropy) + Cliff's delta",
     "conservées, y compris KolmogorovLZ et PermutationEntropy) + Cohen-d", 1),
    ("#            - w_size: 150, test: cliff_delta, n_est: 5, boot: True",
     "#            - w_size: 150, test: cohen_d, n_est: 5, boot: True", 1),
    ("STATISTICAL_TEST = 'cohen_d'  # Options: 'cohen_d', 'cliff_delta'",
     "STATISTICAL_TEST = 'cohen_d'  # v6.0.0 : test statistique unique, Cliff retire (voir en-tete).", 1),
    ("'test': 'cliff_delta'", "'test': 'cohen_d'", 3),
    ("# Les autres restent dans la couche relative (z croise + Cliff).",
     "# Les autres restent dans la couche relative (z croise + Cohen-d).", 1),
    (CLIFF_DEF, "", 1),
    ("    d = cohen_d(g1, g2) if stat_test == 'cohen_d' else cliff_delta(g1, g2, min_grp)",
     "    d = cohen_d(g1, g2)  # v6.0.0 : cohen_d partout, Cliff retire (stat_test conserve pour compatibilite).", 1),
    ("cliff_between_classes", "cohen_between_classes", 4),  # dont 2 sur la ligne 12306 (label + .get)
    ("z croise des 29 medianes + Cliff's delta entre classes.",
     "z croise des 29 medianes + Cohen-d entre classes.", 1),
    ("# Cliff's delta entre classes sur les z (comparable, hors T_log)",
     "# Cohen-d entre classes sur les z (comparable, hors T_log) — v6.0.0", 1),
    ("cliff_pairs", "cohen_pairs", 4),  # 8165, 8184, 8191 + 8266 (valeur du dict)
    ("cd = float(cliff_delta(ga, gb, min_grp=2))",
     "cd = float(cohen_d(ga, gb))", 1),
    ('"cliff_delta":', '"cohen_d":', 2),
    ('"cross_estimator_z_of_29_raw_medians_plus_cliff_delta"',
     '"cross_estimator_z_of_29_raw_medians_plus_cohen_d"', 1),
    ('VERSION_MASTER = "v5.9.0-L7aL7b-CoherenceRobustesse"',
     'VERSION_MASTER = "v6.0.0-L7aL7b-CohenD"', 1),
    ('# -> "v5.8.0"', '# -> "v6.0.0"', 1),
]


def main():
    src_bytes = open(SRC, "rb").read()
    sha = hashlib.sha256(src_bytes).hexdigest()
    assert sha == ORIG_SHA, f"SHA source inattendu : {sha} (attendu {ORIG_SHA})"
    text = src_bytes.decode("utf-8")

    for old, new, expected in REPLACEMENTS:
        found = text.count(old)
        assert found == expected, (
            f"Remplacement inattendu ({found} au lieu de {expected}) : {old[:80]!r}"
        )
        text = text.replace(old, new)

    # Insertion de la note v6.0.0 juste après la ligne d'en-tête.
    anchor = "UNIVERSAL_LOG v6.0.0 — Multi-horizons L1/L3/L5/L6 + semantic_split L7 (T0 hors grilles prédictives)\n"
    assert text.count(anchor) == 1, "ancre d'en-tête introuvable"
    text = text.replace(anchor, anchor + NOTE, 1)

    # Vérifications finales : plus aucun identifiant Cliff dans le code.
    # Le mot "Cliff" ne survit que dans la note v6.0.0 et dans deux commentaires
    # qui expliquent le retrait (lignes marquées v6.0.0) — jamais comme code.
    assert text.count("cliff_delta") == 0, "il reste cliff_delta"
    assert text.count("cliff_between") == 0, "il reste cliff_between"
    assert text.count("cliff_pairs") == 0, "il reste cliff_pairs"
    assert text.count("cliff") == 0, "il reste 'cliff' minuscule"
    assert text.lower().count("cliff") == NOTE.lower().count("cliff") + 2, (
        "occurrences de Cliff hors de la note v6.0.0 et des 2 commentaires"
    )
    assert "cliff" not in text.split(NOTE)[0].lower(), "Cliff avant la note"
    for line in text.split(NOTE)[1].splitlines():
        if "cliff" in line.lower():
            assert "v6.0.0" in line or line in NOTE, f"Cliff inattendu : {line[:80]}"
    assert text.count("'test': 'cliff_delta'") == 0
    assert text.count("'test': 'cohen_d'") == 5, "les 5 modes doivent être en cohen_d"

    with open(DST, "w", encoding="utf-8") as f:
        f.write(text)
    dst_sha = hashlib.sha256(open(DST, "rb").read()).hexdigest()
    print(f"OK v6 écrite : {DST}")
    print(f"SHA v6 : {dst_sha}")
    print(f"SHA origine vérifié inchangé : {ORIG_SHA}")
    print(f"Occurrences 'Cliff' restantes (toutes dans la note) : {NOTE.lower().count('cliff')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
