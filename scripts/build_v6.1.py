#!/usr/bin/env python3
"""Construit universal_v6.1.0_cohen.py depuis universal_v6.0.0_cohen.py.

Conception gelée : PROTOCOL_v6.1.md (16 nov. 2026).
- C1 : garde top_csd dans level_risk (_sf 0.0) + garde risk_score.
- C2 : garde csd du Monte-Carlo (_sf 0.50).
- C3 : gardes des poids de vote L7a (_sf 0.0).
- C4 : min_len fast 50 -> 40 (séries courtes).
- C5 : VERSION_MASTER v6.1.0-L7aL7b-CohenD-short + note d'en-tête.
Remplacements exacts, assertions, comptage. L'original n'est jamais modifié.
"""
import hashlib
import pathlib

SRC = pathlib.Path.home() / "workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py"
DST = pathlib.Path.home() / "workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py"

src_bytes = SRC.read_bytes()
src_sha = hashlib.sha256(src_bytes).hexdigest()
assert src_sha == "bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773", \
    f"SHA v6 inattendu : {src_sha}"
text = src_bytes.decode("utf-8")

REPLACEMENTS = []

def rep(old, new, label):
    global text
    n = text.count(old)
    assert n == 1, f"{label} : {n} occurrence(s) (attendu 1)"
    text = text.replace(old, new)
    REPLACEMENTS.append((label, 1))

# C5 — version
rep(
    'VERSION_MASTER = "v6.0.0-L7aL7b-CohenD"',
    'VERSION_MASTER = "v6.1.0-L7aL7b-CohenD-short"\n'
    '# v6.1.0 (16 nov. 2026) — voir PROTOCOL_v6.1.md :\n'
    '#  (C1) garde top_csd dans level_risk (_sf 0.0) + garde risk_score ;\n'
    '#  (C2) garde csd du Monte-Carlo (_sf 0.50) ;\n'
    '#  (C3) gardes des poids de vote L7a (_sf 0.0) : quand tous les poids sont\n'
    '#       nuls/non finis, L7a dit "indeterminate" (retour existant), jamais\n'
    '#       "up" par accident via max() sur des NaN ;\n'
    '#  (C4) min_len fast 50 -> 40 : les séries de 40-49 points (DepMap 45)\n'
    '#       passent la porte ; autres modes inchangés ; diagnostic de bruit\n'
    '#       toujours dégénéré sous n=75 (5 bins x 15), désormais gardé.\n'
    '#  Validation attendue : cascades HP35 et TCGA v4 identiques à v6.',
    "C5 VERSION_MASTER + note",
)

# C4 — min_len fast 50 -> 40
rep(
    "'fast': {'n_bootstrap': 1, 'w_size': 80, 'test': 'cohen_d', 'min_grp': 2, 'min_len': 50,",
    "'fast': {'n_bootstrap': 1, 'w_size': 80, 'test': 'cohen_d', 'min_grp': 2, 'min_len': 40,",
    "C4 min_len fast",
)

# C1 — garde top_csd dans level_risk
rep(
    "    top_csd = 0.0\n"
    "    if csd:\n"
    "        try:\n"
    "            top_csd = float(csd[0][1]) if isinstance(csd[0], (list, tuple)) else float(csd[0].get(\"score\", 0))\n"
    "        except Exception:\n"
    "            top_csd = 0.0\n",
    "    top_csd = 0.0\n"
    "    if csd:\n"
    "        try:\n"
    "            _raw_csd = float(csd[0][1]) if isinstance(csd[0], (list, tuple)) else float(csd[0].get(\"score\", 0))\n"
    "            top_csd = _sf(_raw_csd, 0.0)  # v6.1 C1 : NaN -> 0.0 (meme repli que csd vide)\n"
    "        except Exception:\n"
    "            top_csd = 0.0\n",
    "C1 garde top_csd",
)

# C1 (suite) — garde risk_score
rep(
    "    risk_score = float(np.clip(0.40 * avg_proxy + 0.25 * top_csd + 0.35 * mean_alert, 0, 1))",
    "    risk_score = _sf(float(np.clip(0.40 * avg_proxy + 0.25 * top_csd + 0.35 * mean_alert, 0, 1)), 0.0)  # v6.1 C1",
    "C1 garde risk_score",
)

# C2 — garde csd du Monte-Carlo
rep(
    "    elif csd_ranking:\n"
    "        try:\n"
    "            csd = float(csd_ranking[0][1]) if isinstance(csd_ranking[0], (list, tuple)) else float(csd_ranking[0].get(\"score\", 0.50))\n"
    "        except Exception:\n"
    "            csd = 0.50\n",
    "    elif csd_ranking:\n"
    "        try:\n"
    "            _raw_csd_mc = float(csd_ranking[0][1]) if isinstance(csd_ranking[0], (list, tuple)) else float(csd_ranking[0].get(\"score\", 0.50))\n"
    "            csd = _sf(_raw_csd_mc, 0.50)  # v6.1 C2 : NaN -> 0.50 (repli du except)\n"
    "        except Exception:\n"
    "            csd = 0.50\n",
    "C2 garde csd MC",
)

# C3 — gardes des poids de vote L7a (level_coherence_universal)
rep(
    '        w = domain_weights.get("L1_direction", 0.25) * L1.get("confidence", 0.5) * _h_stab\n'
    "        votes[d] = votes.get(d, 0) + w\n",
    '        w = _sf(domain_weights.get("L1_direction", 0.25) * L1.get("confidence", 0.5) * _h_stab, 0.0)  # v6.1 C3\n'
    "        votes[d] = votes.get(d, 0) + w\n",
    "C3 poids L1",
)
rep(
    '            votes[d] += domain_weights.get("L2_magnitude", 0.15) * 0.6 * L1.get("confidence", 0.5) * _h_stab\n',
    '            votes[d] += _sf(domain_weights.get("L2_magnitude", 0.15) * 0.6 * L1.get("confidence", 0.5) * _h_stab, 0.0)  # v6.1 C3\n',
    "C3 magnitude L1",
)
rep(
    '        w = domain_weights.get("L3_regime", 0.20) * L3.get("confidence", 0.5) * _l3_stab\n',
    '        w = _sf(domain_weights.get("L3_regime", 0.20) * L3.get("confidence", 0.5) * _l3_stab, 0.0)  # v6.1 C3\n',
    "C3 poids L3",
)
rep(
    '        w = domain_weights.get("L4_risk", 0.20) * L4.get("confidence", 0.5)\n',
    '        w = _sf(domain_weights.get("L4_risk", 0.20) * L4.get("confidence", 0.5), 0.0)  # v6.1 C3\n',
    "C3 poids L4",
)
rep(
    '        w = domain_weights.get("L5_complexity", 0.15) * L5.get("confidence", 0.5) * _l5_stab\n',
    '        w = _sf(domain_weights.get("L5_complexity", 0.15) * L5.get("confidence", 0.5) * _l5_stab, 0.0)  # v6.1 C3\n',
    "C3 poids L5",
)

# Vérifications d'invariance : aucun autre changement
assert "v6.0.0-L7aL7b-CohenD" not in text, "ancienne version encore présente"
assert text.count("_sf(_raw_csd, 0.0)") == 1
assert text.count("_sf(_raw_csd_mc, 0.50)") == 1
assert text.count("'min_len': 40") == 1, "min_len 40 doit apparaître 1 fois (fast)"
assert text.count("'min_len': 50") == 0, "min_len 50 ne doit plus apparaître dans les configs"
assert text.count("min_len=50") >= 1, "le min_len=50 du chemin predict/MC doit rester"

DST.write_bytes(text.encode("utf-8"))
dst_sha = hashlib.sha256(DST.read_bytes()).hexdigest()
print(f"Remplacements : {len(REPLACEMENTS)}")
for label, n in REPLACEMENTS:
    print(f"  - {label} : {n}")
print(f"SHA v6 (source, inchangé) : {src_sha}")
print(f"SHA v6.1 (copie) : {dst_sha}")
print(f"Octets v6.1 : {DST.stat().st_size}")
