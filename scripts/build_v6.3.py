#!/usr/bin/env python3
"""Construit universal_v6.3.0_cohen.py depuis universal_v6.2.0_cohen.py.

Conception gelee : PROTOCOL_v6.3_mc.md (19 nov. 2026), section 7.1.
- C1 : VERSION_MASTER v6.3.0-L7aL7b-CohenD-short + note d'en-tete.
- C2 : fonction pure mc_recomposed_score (formule §3, exacte) — ajout seul.
- C3 : appel APRES la selection du best_config (lecture seule) : ecrit
       threshold_optimization['mc_recomposed'] et best_config['mc_recomposed'],
       sans toucher a best_config['score'], 'threshold', ni a la cascade.
Remplacements exacts, assertions, comptage. L'original (v6.2) n'est jamais
modifie ; v6.1 et v6 non plus. Aucun run de validation dans ce script.
"""
import difflib
import hashlib
import pathlib

SRC = pathlib.Path.home() / "workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
DST = pathlib.Path.home() / "workspace/runs/biophysique-hp35/universal_v6.3.0_cohen.py"

src_bytes = SRC.read_bytes()
src_sha = hashlib.sha256(src_bytes).hexdigest()
assert src_sha == "f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf", \
    f"SHA v6.2 inattendu : {src_sha}"
text = src_bytes.decode("utf-8")

FUNC = '''
def mc_recomposed_score(best_metrics, all_maxseps):
    """Score MC recompose v6.3 (PROTOCOL_v6.3_mc.md §3) — LECTURE SEULE.

    MC_new = 0.60*sep + 0.25*stability + 0.15*recur
    sep    = max_separation / (1 + max_separation)   (best_config ancien)
    recur  = mediane_i(max_separation_i) / max_separation_best
             (tirages de all_results ; 0 si best=0 ou aucun tirage).
    Fonction pure : ne lit que les metriques fournies, n'ecrit rien dans
    le pipeline, ne choisit aucun seuil. La selection du best_config
    (ancien composite) est inchangee.
    """
    try:
        maxsep = float(best_metrics.get('max_separation', 0.0) or 0.0)
    except (TypeError, ValueError):
        maxsep = 0.0
    try:
        stab = float(best_metrics.get('stability', 0.0) or 0.0)
    except (TypeError, ValueError):
        stab = 0.0
    sep = maxsep / (1.0 + maxsep) if maxsep > 0 else 0.0
    vals = []
    for x in (all_maxseps or []):
        try:
            fx = float(x)
        except (TypeError, ValueError):
            continue
        if np.isfinite(fx):
            vals.append(fx)
    if maxsep > 0 and vals:
        recur = float(np.median(np.asarray(vals, dtype=float))) / maxsep
        recur = float(min(1.0, max(0.0, recur)))
    else:
        recur = 0.0
    score = 0.60 * sep + 0.25 * stab + 0.15 * recur
    return {
        'mc_new': float(score),
        'sep': float(sep),
        'stability': float(stab),
        'recur': float(recur),
        'formula': 'MC_new=0.60*maxsep/(1+maxsep)+0.25*stability+0.15*median_i(maxsep_i)/maxsep_best',
        'weights': {'separation': 0.60, 'stability': 0.25, 'recurrence': 0.15},
        'n_iterations_used': int(len(vals)),
    }

'''

CALL = """        # v6.3.0 — MC recompose (PROTOCOL_v6.3_mc.md §3) : LECTURE SEULE du
        # best_config deja selectionne par l'ancien composite. Ne touche ni
        # au seuil, ni au score ancien, ni a la cascade.
        if best_config is not None:
            _mc63_all = [float(r['metrics']['max_separation']) for r in (optimization_results or [])
                         if isinstance(r, dict) and r.get('metrics')
                         and r['metrics'].get('max_separation') is not None]
            _mc63 = mc_recomposed_score(best_config.get('metrics', {}), _mc63_all)
            threshold_optimization['mc_recomposed'] = dict(_mc63)
            best_config['mc_recomposed'] = dict(_mc63)
            print(f"MC recompose v6.3 : {_mc63['mc_new']:.4f} (sep={_mc63['sep']:.4f}, "
                  f"stab={_mc63['stability']:.4f}, recur={_mc63['recur']:.4f})")
        else:
            threshold_optimization['mc_recomposed'] = {'mc_new': None,
                                                        'reason': 'best_config is None'}

"""

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
    'VERSION_MASTER = "v6.3.0-L7aL7b-CohenD-short"\n'
    '# v6.3.0 (19 nov. 2026) — voir PROTOCOL_v6.3_mc.md §7.1 :\n'
    '#  SEUL changement de code : ajout du score MC recompose en LECTURE\n'
    '#  SEULE (mc_recomposed_score). La selection du best_config (ancien\n'
    '#  composite 0.3/0.3/0.2/0.2), le seuil MC, la cascade, S_sep, Delta,\n'
    '#  L5/L4/L7a et les estimateurs sont intacts. MC_new = 0.60*sep +\n'
    '#  0.25*stability + 0.15*recur, sep = maxsep/(1+maxsep), recur =\n'
    '#  mediane des maxsep des tirages / maxsep du best. Robustness et\n'
    '#  sharpness supprimees du score (D1/D3), recurrence ajoutee (D5).\n'
    '#  Proposition NON adoptee : voir §8.49 (portes A2/A3 en echec).',
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
    "C2 fonction mc_recomposed_score",
)

# C3 — appel apres la creation de threshold_optimization (ancre : commentaire
# qui suit immediatement le dict, avant l'utilisation du meilleur scan)
rep(
    "        # Utiliser directement le meilleur scan lorsqu'il existe. Sinon, le\n",
    CALL + "        # Utiliser directement le meilleur scan lorsqu'il existe. Sinon, le\n",
    "C3 appel lecture seule mc_recomposed",
)

# Verifications d'invariance
assert 'VERSION_MASTER = "v6.2.0-L7aL7b-CohenD-short"' not in text
assert text.count('VERSION_MASTER = "v6.3.0-L7aL7b-CohenD-short"') == 1
assert text.count("def mc_recomposed_score(") == 1
assert text.count("mc_recomposed") >= 5
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
print(f"SHA v6.3 (copie) : {dst_sha}")
print(f"Octets v6.3 : {DST.stat().st_size}")
