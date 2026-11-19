#!/usr/bin/env python3
"""Construit universal_v6.2.0_cohen.py depuis universal_v6.1.0_cohen.py.

Conception gelee : PROTOCOL_v6.2.md (18 nov. 2026), section 2.2.
- H1 : import hashlib (en tete, avec les autres imports).
- H2 : hachage stable L5 — hash(metric) remplace par SHA-256 stable
       (int.from_bytes(hashlib.sha256(...).digest()[:8], 'little') % 1000).
- V  : VERSION_MASTER v6.2.0-L7aL7b-CohenD-short + note d'en-tete.
Remplacements exacts, assertions, comptage. L'original (v6.1) n'est jamais
modifie ; la v6 non plus. Aucun run de validation dans ce script.
"""
import hashlib
import pathlib

SRC = pathlib.Path.home() / "workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py"
DST = pathlib.Path.home() / "workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"

src_bytes = SRC.read_bytes()
src_sha = hashlib.sha256(src_bytes).hexdigest()
assert src_sha == "2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9", \
    f"SHA v6.1 inattendu : {src_sha}"
text = src_bytes.decode("utf-8")

# Pre-conditions verifiees avant toute copie (PROTOCOL_v6.2 §2.1) :
assert text.count("hash(") == 1, \
    f"hash( natif : {text.count('hash(')} occurrence(s) (attendu 1)"
assert text.count("hashlib") == 0, \
    f"hashlib deja present : {text.count('hashlib')} occurrence(s) (attendu 0)"
assert "hash(metric) % 1000" in text

REPLACEMENTS = []

def rep(old, new, label):
    global text
    n = text.count(old)
    assert n == 1, f"{label} : {n} occurrence(s) (attendu 1)"
    text = text.replace(old, new)
    REPLACEMENTS.append((label, 1))

# H1 — import hashlib (bloc IMPORTS, apres import sys / import json)
rep(
    "import sys\nimport json\n",
    "import sys\nimport json\nimport hashlib\n",
    "H1 import hashlib",
)

# H2 — ligne 8985, seed MC de level_complexity (hachage stable L5)
rep(
    "int(seed) + (hash(metric) % 1000)",
    "int(seed) + (int.from_bytes(hashlib.sha256(metric.encode('utf-8')).digest()[:8], 'little') % 1000)",
    "H2 hachage stable L5",
)

# V — version + note d'en-tete (la note v6.1 reste en dessous, comme la
# note v6.1 avait conserve l'historique precedent)
rep(
    'VERSION_MASTER = "v6.1.0-L7aL7b-CohenD-short"',
    'VERSION_MASTER = "v6.2.0-L7aL7b-CohenD-short"\n'
    '# v6.2.0 (18 nov. 2026) — voir PROTOCOL_v6.2.md §2.2 :\n'
    '#  SEUL changement de code : hachage stable L5. Le seed MC de\n'
    '#  level_complexity utilisait le hachage natif de la metrique,\n'
    '#  aleatoire par processus Python (gigue L5 mesuree +-0,07,\n'
    '#  phase 2 §8.35) ; il utilise desormais un SHA-256 stable de la\n'
    '#  metrique, robuste quel que soit l\'environnement d\'execution.\n'
    '#  Rien d\'autre ne change : cascade, seuils, Delta, estimateurs\n'
    '#  et scores MC sont intacts.\n'
    '#  Validation attendue : gigue L5 = 0 entre deux processus separes,\n'
    '#  cascades HP35 et TCGA v4 identiques a v6.1.',
    "V VERSION_MASTER + note",
)

# Verifications d'invariance : aucun autre changement
assert 'VERSION_MASTER = "v6.1.0-L7aL7b-CohenD-short"' not in text, \
    "ancienne version encore presente"
assert text.count('VERSION_MASTER = "v6.2.0-L7aL7b-CohenD-short"') == 1
assert text.count("hash(") == 0, \
    f"hash( natif encore present : {text.count('hash(')} occurrence(s) (attendu 0)"
assert text.count("hashlib") == 2, \
    f"hashlib : {text.count('hashlib')} occurrence(s) (attendu 2 : import + usage)"
assert text.count("hash(metric)") == 0, "hash(metric) encore present"
assert text.count("import hashlib") == 1

DST.write_bytes(text.encode("utf-8"))
dst_sha = hashlib.sha256(DST.read_bytes()).hexdigest()
print(f"Remplacements : {len(REPLACEMENTS)}")
for label, n in REPLACEMENTS:
    print(f"  - {label} : {n}")
print(f"SHA v6.1 (source, inchange) : {src_sha}")
print(f"SHA v6.2 (copie) : {dst_sha}")
print(f"Octets v6.2 : {DST.stat().st_size}")
