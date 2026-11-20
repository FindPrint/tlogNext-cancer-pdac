#!/usr/bin/env python3
"""Construit universal_v6.4.0_cohen.py depuis universal_v6.2.0_cohen.py.

Conception gelee : PROTOCOL_v6.4_mc.md (19 nov. 2026), section 7.1.
Source = v6.2 UNIQUEMENT (jamais la v6.3 rejetee).
- C1 : VERSION_MASTER v6.4.0-L7aL7b-CohenD-short + note d'en-tete.
- C2 : fonction pure mc_v64_score (formule §3, exacte) — ajout seul.
- C3 : appel APRES la selection du best_config (lecture seule) : ecrit
       threshold_optimization['mc_v64'] et best_config['mc_v64'],
       sans toucher a best_config['score'], 'threshold', ni a la cascade.
Remplacements exacts, assertions, comptage. L'original (v6.2) n'est jamais
modifie ; v6.1, v6 et v6.3 non plus. Aucun run de validation dans ce script.
"""
import difflib
import hashlib
import pathlib

SRC = pathlib.Path.home() / "workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
DST = pathlib.Path.home() / "workspace/runs/biophysique-hp35/universal_v6.4.0_cohen.py"

src_bytes = SRC.read_bytes()
src_sha = hashlib.sha256(src_bytes).hexdigest()
assert src_sha == "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf", \
    f"SHA v6.2 inattendu : {src_sha}"
text = src_bytes.decode("utf-8")

FUNC = '''\ndef mc_v64_score(best_metrics, all_thresholds, best_threshold):\n    """Score MC v6.4 (PROTOCOL_v6.4_mc.md §3) — LECTURE SEULE.\n\n    MC2  = 0.70*sep + 0.30*conc\n    sep  = max_separation / (1 + max_separation)   (best_config ancien)\n    conc = 1 - mediane_i(|theta_i - theta*|) / (theta_max - theta_min)\n           (theta_i = seuils des tirages de all_results ; theta* = seuil\n            du best_config ; conc=1 si etendue 0 ; conc=0 si <2 seuils).\n    Fonction pure : ne lit que les metriques fournies, n'ecrit rien dans\n    le pipeline, ne choisit aucun seuil. La selection du best_config\n    (ancien composite) est inchangee. Stability, robustness, sharpness et\n    la recurrence mediane/best sont SUPPRIMEES du score (v6.3, D1-D3, §8.49.6).\n    """\n    try:\n        maxsep = float(best_metrics.get('max_separation', 0.0) or 0.0)\n    except (TypeError, ValueError):\n        maxsep = 0.0\n    sep = maxsep / (1.0 + maxsep) if maxsep > 0 else 0.0\n    vals = []\n    for x in (all_thresholds or []):\n        try:\n            fx = float(x)\n        except (TypeError, ValueError):\n            continue\n        if np.isfinite(fx):\n            vals.append(fx)\n    if len(vals) < 2:\n        conc = 0.0\n    else:\n        rng = float(max(vals) - min(vals))\n        if rng == 0:\n            conc = 1.0\n        else:\n            try:\n                b = float(best_threshold)\n            except (TypeError, ValueError):\n                conc = 0.0\n                rng = None\n            if rng is not None:\n                med_dev = float(np.median(np.asarray(\n                    [abs(v - b) for v in vals], dtype=float)))\n                conc = float(min(1.0, max(0.0, 1.0 - med_dev / rng)))\n    score = 0.70 * sep + 0.30 * conc\n    return {\n        'mc2': float(score),\n        'sep': float(sep),\n        'conc': float(conc),\n        'formula': 'MC2=0.70*maxsep/(1+maxsep)+0.30*(1-median_i(|theta_i-theta*|)/(theta_max-theta_min))',\n        'weights': {'separation': 0.70, 'concentration': 0.30},\n        'n_thresholds_used': int(len(vals)),\n    }\n\n'''

CALL = """        # v6.4.0 — MC par concentration des seuils (PROTOCOL_v6.4_mc.md §3) :\n        # LECTURE SEULE du best_config deja selectionne par l'ancien\n        # composite. Ne touche ni au seuil, ni au score ancien, ni a la cascade.\n        if best_config is not None:\n            _mc64_thr = [float(r['threshold']) for r in (optimization_results or [])\n                         if isinstance(r, dict) and r.get('threshold') is not None]\n            _mc64 = mc_v64_score(best_config.get('metrics', {}), _mc64_thr,\n                                 best_config.get('threshold'))\n            threshold_optimization['mc_v64'] = dict(_mc64)\n            best_config['mc_v64'] = dict(_mc64)\n            print(f\"MC v6.4 : {_mc64['mc2']:.4f} (sep={_mc64['sep']:.4f}, \"\n                  f\"conc={_mc64['conc']:.4f})\")\n        else:\n            threshold_optimization['mc_v64'] = {'mc2': None,\n                                                'reason': 'best_config is None'}\n\n"""

REPLACEMENTS = []


def rep(old, new, label):
    global text
    n = text.count(old)
    assert n == 1, f"{label} : {n} occurrence(s) (attendu 1)"
    text = text.replace(old, new)
    REPLACEMENTS.append((label, 1))


# C1 — version + note d'en-tete
rep(
    'VERSION_MASTER = "v6.2.0-L7aL7b-CohenD-short"',
    'VERSION_MASTER = "v6.4.0-L7aL7b-CohenD-short"\n'
    '# v6.4.0 (19 nov. 2026) — voir PROTOCOL_v6.4_mc.md §7.1 :\n'
    '#  SEUL changement de code : ajout du score MC v6.4 en LECTURE\n'
    '#  SEULE (mc_v64_score). La selection du best_config (ancien\n'
    '#  composite 0.3/0.3/0.2/0.2), le seuil MC, la cascade, S_sep, Delta,\n'
    '#  L5/L4/L7a et les estimateurs sont intacts. MC2 = 0.70*sep +\n'
    '#  0.30*conc, sep = maxsep/(1+maxsep), conc = 1 - mediane des\n'
    '#  |seuil_i - seuil*| / etendue des seuils. Stability, robustness,\n'
    '#  sharpness et la recurrence mediane/best supprimees du score.\n'
    '#  Construite depuis la v6.2 (jamais depuis la v6.3 rejetee).\n'
    '#  Proposition NON adoptee : voir §8.52 (porte A2 en echec).',
    "C1 VERSION_MASTER + note",
)

# C2 — fonction pure apres evaluate_scan_quality (ancre : son return final)
rep(
    "    return {\n"
    "        'max_separation': float(max_separation),\n"
    "        's_norm': s_norm,\n"
    "        'stability': float(stability),\n"
    "        'robustness': float(robustness),\n"
    "        'sharpness': sharpness_norm\n"
    "    }\n",
    "    return {\n"
    "        'max_separation': float(max_separation),\n"
    "        's_norm': s_norm,\n"
    "        'stability': float(stability),\n"
    "        'robustness': float(robustness),\n"
    "        'sharpness': sharpness_norm\n"
    "    }\n"
    + FUNC,
    "C2 fonction mc_v64_score",
)

# C3 — appel apres la creation de threshold_optimization (ancre : commentaire
# qui suit immediatement le dict, avant l'utilisation du meilleur scan)
rep(
    "        # Utiliser directement le meilleur scan lorsqu'il existe. Sinon, le\n",
    CALL + "        # Utiliser directement le meilleur scan lorsqu'il existe. Sinon, le\n",
    "C3 appel lecture seule mc_v64",
)

# Verifications d'invariance
assert 'VERSION_MASTER = "v6.2.0-L7aL7b-CohenD-short"' not in text
assert text.count('VERSION_MASTER = "v6.4.0-L7aL7b-CohenD-short"') == 1
assert text.count("def mc_v64_score(") == 1
assert text.count("mc_v64") >= 5
assert text.count("best_config['score']") == 0, "score ancien touche ?"
# Diff : seuls les blocs C1-C3 doivent differer
diff_lines = [ln for ln in difflib.unified_diff(
    src_bytes.decode("utf-8").splitlines(), text.splitlines(), lineterm="")]
added = [ln[1:] for ln in diff_lines if ln.startswith("+") and not ln.startswith("+++")]
removed = [ln[1:] for ln in diff_lines if ln.startswith("-") and not ln.startswith("---")]
print(f"lignes ajoutees : {len(added)}, retirees : {len(removed)}")
for ln in removed:
    print(f"  - RETIRE : {ln[:100]}")
assert removed == ['VERSION_MASTER = "v6.2.0-L7aL7b-CohenD-short"'], \
    f"lignes retirees inattendues : {removed}"
# Controle structurel : exactement 3 blocs differants (C1, C2, C3)
_sm = difflib.SequenceMatcher(a=src_bytes.decode("utf-8").splitlines(),
                              b=text.splitlines(), autojunk=False)
_opcodes = [op for op in _sm.get_opcodes() if op[0] != "equal"]
print(f"blocs differants : {len(_opcodes)}")
for tag, i1, i2, j1, j2 in _opcodes:
    print(f"  - {tag} src[{i1}:{i2}] -> dst[{j1}:{j2}]")
assert len(_opcodes) == 3, f"attendu 3 blocs differants (C1/C2/C3), lu {len(_opcodes)}"
assert sorted(op[0] for op in _opcodes) == ["insert", "insert", "replace"], \
    f"opcodes inattendus : {_opcodes}"

DST.write_bytes(text.encode("utf-8"))
dst_sha = hashlib.sha256(DST.read_bytes()).hexdigest()
print(f"Remplacements : {len(REPLACEMENTS)}")
for label, n in REPLACEMENTS:
    print(f"  - {label} : {n}")
print(f"SHA v6.2 (source, inchange) : {src_sha}")
print(f"SHA v6.4 (copie) : {dst_sha}")
print(f"Octets v6.4 : {DST.stat().st_size}")
