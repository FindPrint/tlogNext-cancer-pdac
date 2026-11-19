#!/usr/bin/env python3
"""Insertion de la §8.40 (arbitrage MTAP) au livre blanc — 19 nov. 2026.
Ancres exactes, vérifiées avant écriture ; arrêt si une ancre est absente
ou multiple (un autre chantier écrit en parallèle dans le même fichier).
1. §8.40 entre « — Fin de la §8.39. — » et « # §8.42 ».
2. Ligne 47 au §7, après la ligne 46 (Modélisation des magnitudes).
3. Entrée datée au §10 Journal, avant la ligne de fin de version initiale.
"""
import hashlib, sys

WB = "/home/hatch/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md"
SEC = "/home/hatch/workspace/runs/pdac-v6/section_8.40_mtap_arbitration.md"

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

with open(WB, encoding="utf-8") as f:
    txt = f.read()
sha_avant = sha(WB)
print("SHA livre blanc AVANT :", sha_avant)

with open(SEC, encoding="utf-8") as f:
    sec = f.read().rstrip("\n") + "\n"
print("SHA section_8.40 :", sha(SEC))

# --- 1. §8.40 ---
ancre1 = "— Fin de la §8.39. —\n\n# §8.42 Modélisation des magnitudes"
assert txt.count(ancre1) == 1, f"ancre §8.39/§8.42 : {txt.count(ancre1)} occurrences"
assert "### 8.40 Arbitrage de la contradiction MTAP" not in txt, "§8.40 déjà présente !"
txt = txt.replace(ancre1, "— Fin de la §8.39. —\n\n" + sec + "\n# §8.42 Modélisation des magnitudes", 1)
print("§8.40 insérée entre §8.39 et §8.42.")

# --- 2. Ligne 47 au §7 ---
lignes = txt.split("\n")
idx46 = [i for i, l in enumerate(lignes) if l.startswith("| 46 | 19 nov. 2026 | **Modélisation des magnitudes")]
assert len(idx46) == 1, f"ligne 46 : {len(idx46)} occurrences"
assert not any(l.startswith("| 47 |") for l in lignes), "ligne 47 déjà présente !"
row47 = ("| 47 | 19 nov. 2026 | **Arbitrage de la contradiction MTAP (§8.40)** (chantier 1 ; go parent 19 nov. 06h55 ; "
         "script neuf `mtap_arbitration_840.py`, SHA `1fccc2f6…e6a688`, systemd-run unité `mtap-840c`, exit 0, 144,8 s ; "
         "tests directs, aucun run de pipeline ; DepMap 24Q4 SHA vérifiés, PRISM primaire 24Q2 / secondaire 19Q4 / GDSC2 déjà sur disque) | — | — | "
         "hors pipeline (tests directs) | **TERMINÉ. (a) OUI, le groupe MTAP-délété se distingue par la dépendance PRMT5 : pancréas −1,385 contre −1,010, p=0,0036, reproduit à l'identique ; "
         "Spearman +0,497 (p=0,0004) ; MAT2A plat (p=0,14) ; effet CDKN2A fixé confirmé 4 fois (CN p=0,26/0,46, mutation p=0,76 reconfirmé au chiffre près). "
         "(b) NON, aucun médicament ne distingue le groupe : 0 FDR < 0,05 sur 6 790 (primaire, FDR min 0,959), 1 437 (secondaire, 0,625) et 269 (GDSC2, 0,561/0,882) ; "
         "inhibiteurs PRMT5 présents tous NS (EPZ015666 p=0,37, GSK3326595 p=0,53, JNJ-64619178 p=0,43, HLCL-61 p=0,68, GSK591 p=0,24) ; vopimetostat et inhibiteurs MAT2A absents des trois bibliothèques. "
         "(c) NON, pas le groupe KRAS-fort : Fisher TCGA reconfirmé exactement 6/12 vs 37/165, OR 3,46, p=0,073 ; lignées p=0,31 (top-12) / 0,54 (tertile) ; Spearman CN MTAP vs Chronos KRAS −0,037, p=0,81 ; chevauchement 6/12 tumeurs, 7/12 lignées. "
         "Trois erreurs de comptage attrapées et corrigées (Fisher NaN p=0,041→0,073 ; GDSC courbes en double, Acetalax artefact ; BRD en double au primaire).** | "
         "**Arbitrage partiel : le groupe MTAP-délété existe comme groupe biologique et n'est pas le groupe KRAS-fort — mais la contradiction S_sep (+0,20) contre MC (−0,16) / Delta (−0,54) reste ouverte ; "
         "le verdict §8.36 (pipeline ne sépare pas réel/nul sur la série MTAP) n'est pas renversé. MAT2A sort des vulnérabilités à tester ; Fisher TCGA fragile à une tumeur près. Voir §8.40.** |")
lignes.insert(idx46[0] + 1, row47)
txt = "\n".join(lignes)
print("Ligne 47 ajoutée au §7.")

# --- 3. Entrée datée au §10 Journal ---
ancre3 = "\n---\n\n*Fin de la version initiale du livre blanc — 15 novembre 2026. Le reste se mesure.*"
assert txt.count(ancre3) == 1, f"ancre fin §10 : {txt.count(ancre3)} occurrences"
entry = ("\n- **19 nov. 2026 :** chantier 1 — **arbitrage de la contradiction MTAP (§8.40)** : S_sep +0,1968 contre MC −0,1642 et Delta −0,5416 (§8.38). "
         "Tests directs, données du jour, aucun run : (a) OUI, dépendance PRMT5 plus forte chez les MTAP-délétées (pancréas −1,385 contre −1,010, p=0,0036, reproduit à l'identique ; Spearman +0,497) ; "
         "MAT2A plat ; effet CDKN2A fixé confirmé 4 fois (p=0,26 / 0,46 / 0,76). (b) NON, aucun médicament des 3 écrans ne distingue le groupe (0 FDR < 0,05 ; inhibiteurs PRMT5 présents tous NS ; vopimetostat et inhibiteurs MAT2A absents). "
         "(c) NON, pas le groupe KRAS-fort (Fisher TCGA p=0,073 reconfirmé exactement ; lignées p=0,31). "
         "**Arbitrage partiel : le groupe existe biologiquement et n'est pas KRAS-fort, mais la contradiction entre indicateurs du pipeline reste ouverte ; §8.36 non renversé.** "
         "Trois erreurs de comptage corrigées en route (Fisher NaN, GDSC courbes en double, BRD en double). Détail au §8.40 ; ligne 47 au §7. PDF non régénéré, rien poussé sur GitHub (hors de ce chantier).")
txt = txt.replace(ancre3, entry + ancre3, 1)
print("Entrée datée ajoutée au §10.")

with open(WB, "w", encoding="utf-8") as f:
    f.write(txt)
print("SHA livre blanc APRÈS :", sha(WB))
print("OK")
