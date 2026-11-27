#!/usr/bin/env python3
"""Vérification du livre blanc après fusion §8.99 (lecture seule)."""
import hashlib
import sys

LB = "/home/hatch/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md"
wb = open(LB, encoding="utf-8").read()
lines = wb.count("\n") + (0 if wb.endswith("\n") else 1)
print(f"lignes : {lines} (attendu 26786)")
checks = [
    ("lignes 26786", lines == 26786),
    ("### 8.99 une fois", wb.count("### 8.99 Nouvelle paire") == 1),
    ("## 8.99.1 une fois", wb.count("## 8.99.1") == 1),
    ("## 8.99.8 une fois", wb.count("## 8.99.8") == 1),
    ("titre §8.5 unique (ligne complète)", wb.count("### 8.5 Synthèse des 4 versions — ce qui bouge, ce qui ne bouge pas") == 1),
    ("§8.99 avant §8.5", wb.index("### 8.99 Nouvelle paire") < wb.index("### 8.5 Synthèse des 4 versions — ce qui bouge")),
    ("0 titre doublé 8.8.99", "### 8.8.99" not in wb),
    ("0 marqueur 8.99.99", "### 8.99.99" not in wb),
    ("ligne 105 §7", wb.count("| 105 | 27 nov. 2026 |") == 1),
    ("addendum A2", wb.count("ADDENDUM 27 nov. 2026 (registre A2") == 1),
    ("addendum Cox", wb.count("CORRECTION 27 nov. 2026 (re-vérification Cox") == 1),
    ("A2 11/16 dans l'addendum", "A2 classique 10/15 → 11/16" in wb),
    ("LOO 10/15 dans l'addendum", "LOO pire cas 9/14 → 10/15" in wb),
    ("KM 20,2 dans l'addendum Cox", "20,0 → 20,2 mois" in wb),
    ("réel 0,3712 dans §8.99", "0,3712" in wb),
    ("p95 0,2884 dans §8.99", "0,2884" in wb),
    ("nul s42 0,1833", "0,1833" in wb),
    ("écart s42 +0,1879", "+0,1879" in wb),
    ("seul « prédiction » ligne 199", wb.count("prédiction") >= 1),
]
bad = [n for n, ok in checks if not ok]
for n, ok in checks:
    print(("OK  " if ok else "ÉCHEC") + "  " + n)
h = hashlib.sha256(wb.encode("utf-8")).hexdigest()
print("SHA livre blanc fusionné :", h)
print("LIGNES :", lines)
sys.exit(1 if bad else 0)
