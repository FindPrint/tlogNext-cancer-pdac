#!/usr/bin/env python3
"""Fusion §8.100 dans le livre blanc PDAC + ligne 106 au §7.

Ordre (même pratique que §8.99, fuse_899.py) : sauvegarde .bak-8100,
insertion de la section avant « ### 8.5 », ligne 106 au §7.
Différence vs §8.99 : le fichier section_8.100_fusion_depots.md porte un
bloc « ## Ligne §7 » (lignes 317–320) + le marqueur de fin. Le bloc
« ## Ligne §7 » est RETIRÉ du corps inséré (le livre blanc ne contient
aucun « ## Ligne §7 » : 0 occurrence avant fusion) et sa ligne est
reprise pour la table §7. Le marqueur « — Fin de la §8.100. — » est
déjà dans le fichier source (contrairement au §8.99) : rien à ajouter
après le rendu PDF sur ce point.

Préconditions : livre blanc 26 794 lignes, SHA bf80f029… (après journal
des poussées §8.99) ; section SHA 71be6cd6… ; PROVENANCE_8100 SHA ca5aed94….
"""
import hashlib
import shutil

RUNS = "/home/hatch/workspace/runs/pdac-v6"
LB = "/home/hatch/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md"
SEC = RUNS + "/section_8.100_fusion_depots.md"
PROV = RUNS + "/PROVENANCE_8100.md"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def fail(msg):
    print("ABANDON :", msg)
    raise SystemExit(2)


# --- 0. Préconditions ---
assert sha(SEC).startswith("71be6cd6"), sha(SEC)[:16]
assert sha(PROV).startswith("ca5aed94"), sha(PROV)[:16]
wb = open(LB, encoding="utf-8").read()
lines_before = wb.count("\n") + (0 if wb.endswith("\n") else 1)
lb_sha_before = sha(LB)
print(f"livre blanc avant fusion : {lines_before} lignes, SHA {lb_sha_before[:16]}...")
assert lines_before == 26794, f"lignes attendues 26794, lues {lines_before}"
assert lb_sha_before.startswith("bf80f029"), f"SHA attendu bf80f029..., lu {lb_sha_before[:16]}"
assert wb.count("## Ligne §7") == 0, "le livre blanc contient déjà un bloc Ligne §7"
assert wb.count("### 8.100") == 0, "§8.100 déjà présent"

# --- 1. Sauvegarde ---
bak = LB + ".bak-8100"
shutil.copyfile(LB, bak)
assert sha(bak) == lb_sha_before
print(f"sauvegarde : {bak} (SHA conforme)")

# --- 2. Lecture section : extraire la ligne §7, retirer le bloc ---
sec_lines = open(SEC, encoding="utf-8").read().split("\n")
assert sec_lines[0].startswith("### 8.100 "), sec_lines[0][:40]
assert sec_lines[-1] == "" and sec_lines[-2] == "— Fin de la §8.100. —", "marqueur de fin absent"
idx_ligne7 = next(i for i, l in enumerate(sec_lines) if l == "## Ligne §7")
row_lines = [l for l in sec_lines[idx_ligne7:] if l.startswith("| 106 |")]
assert len(row_lines) == 1, f"ligne 106 : {len(row_lines)} occurrences"
row106 = row_lines[0]
assert row106.startswith("| 106 | 27 nov. 2026 | **Fusion des cinq dépôts"), row106[:60]
body_lines = sec_lines[:idx_ligne7]
# retirer les lignes vides finales du corps (avant le bloc Ligne §7)
while body_lines and body_lines[-1] == "":
    body_lines.pop()
assert body_lines[-1] == "— Fin de la §8.100. —" or True
# le marqueur de fin est APRÈS le bloc Ligne §7 dans le fichier source :
# il doit terminer le corps inséré, pas rester orphelin.
body_lines.append("")
body_lines.append("— Fin de la §8.100. —")
body = "\n".join(body_lines) + "\n"
assert body.startswith("### 8.100 "), "le corps ne commence pas par ### 8.100"
assert "### 8.8.100" not in body and "### 8.100.100" not in body
assert body.count("— Fin de la §8.100. —") == 1
assert "## Ligne §7" not in body
print(f"corps inséré : {len(body_lines)} lignes (bloc Ligne §7 retiré, marqueur conservé)")
print(f"ligne §7 extraite : {row106[:80]}...")

# --- 3. Insertion de la section avant ### 8.5 ---
anchor = "### 8.5 Synthèse des 4 versions — ce qui bouge, ce qui ne bouge pas"
assert wb.count(anchor) == 1, f"ancre ### 8.5 : {wb.count(anchor)} occurrences"
wb = wb.replace(anchor, body + "\n" + anchor, 1)
assert wb.count("### 8.100 Fusion des cinq dépôts") == 1
assert wb.count("## 8.100.1") == 1 and wb.count("## 8.100.8") == 1
print("section §8.100 insérée avant ### 8.5")

# --- 4. Ligne 106 au §7, après la ligne 105 ---
row105_anchor = "| 105 | 27 nov. 2026 | **Nouvelle paire : GSE184585"
assert wb.count(row105_anchor) == 1
i = wb.index(row105_anchor)
j = wb.index("\n", i)
wb = wb[:j] + "\n" + row106 + wb[j:]
assert wb.count("| 106 | 27 nov. 2026 |") == 1
print("ligne 106 ajoutée au §7")

# --- 5. Écriture + vérifications ---
open(LB, "w", encoding="utf-8").write(wb)
lines_after = wb.count("\n") + (0 if wb.endswith("\n") else 1)
lb_sha_after = sha(LB)
print(f"livre blanc après fusion : {lines_after} lignes (+{lines_after - lines_before}), SHA {lb_sha_after[:16]}...")
assert "### 8.8.100" not in wb and "### 8.100.100" not in wb
assert wb.count("### 8.5 Synthèse des 4 versions — ce qui bouge, ce qui ne bouge pas") == 1
assert wb.count("— Fin de la §8.100. —") == 1
assert wb.count("## Ligne §7") == 0
print("vérifications : 0 titre doublé, 0 marqueur dupliqué, ligne §7 1/1")
print(f"SHA avant : {lb_sha_before}")
print(f"SHA après : {lb_sha_after}")
print(f"LIGNES : {lines_before} -> {lines_after}")
