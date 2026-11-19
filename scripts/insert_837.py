import re

W = "/home/hatch/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md"
D = "/home/hatch/workspace/runs/pdac-v6/v62_section_837_draft.md"

wb = open(W, encoding="utf-8").read()
draft = open(D, encoding="utf-8").read()

# --- Extraire le corps du brouillon (de "## §8.37" à avant "— Fin du brouillon") ---
start = draft.index("## §8.37 v6.2")
end = draft.index("— Fin du brouillon")
body = draft[start:end].strip() + "\n"

# --- Adapter les titres au style du livre blanc ---
body = body.replace(
    "## §8.37 v6.2 : hachage stable L5, score S_sep, élucidation de Delta",
    "### 8.37 v6.2 : hachage stable L5, score S_sep, élucidation de Delta (18–19 nov. 2026)",
    1)
body = body.replace(
    "### Verdict d'abord — trois réponses, en une phrase chacune",
    "**Verdict d'abord, en trois phrases.**", 1)
for n, t in [
    ("8.37.1", "Construction de la v6.2 (rappel, détail dans `PROVENANCE_v6.2.md`)"),
    ("8.37.2", "Validation (§5 du protocole) — 20/20, gigue 0"),
    ("8.37.3", "Test de discrimination (§6) — S_sep 6/8, pareil que la v6.1"),
    ("8.37.4", "Élucidation de Delta (§4) — non élucidé"),
    ("8.37.5", "Ce qui change, ce qui ne change pas, et la suite"),
]:
    body = body.replace(f"### {n} {t}", f"**{n} {t}.**", 1)
body = body.replace("### Provenance (§8.37)", "**Provenance (§8.37).**", 1)

assert "## §8.37" not in body and "### 8.37" in body
assert "BROUILLON" not in body and "Fin du brouillon" not in body

# --- 1. Insérer le §8.37 juste avant le §8.5 ---
anchor = "### 8.5 Synthèse des 4 versions"
assert wb.count(anchor) == 1, wb.count(anchor)
wb = wb.replace(anchor, body + "\n" + anchor, 1)

# --- 2. Ligne 43 du §7, après la ligne 42 ---
row43 = (
    "| 43 | 18–19 nov. 2026 | **v6.2 — hachage stable L5, score S_sep, élucidation de Delta** "
    "(go de Zackary 18 nov. 18h07 : « pousser mon pipeline, je veux vraiment qu'il soit en capacité de trouver "
    "un remède, pas juste montrer un axe » ; protocole gelé `PROTOCOL_v6.2.md`, SHA `6e9324a2…dfad` ; construction "
    "`build_v6.2.py`, SHA `5348636e…fa0` ; `PROVENANCE_v6.2.md`) | v6.2.0-CohenD-short, fast | step / KRAS | réel "
    "contre nul (graine 42) | **TERMINÉ. Validation 20/20 exit 0** (10 runs fast × 2 répétitions, processus séparés ; "
    "cascades identiques à la v6.1 sur 10/10 ; L7a finis sur les petites cohortes ; **gigue mesurée = 0,0000 sur tous "
    "les indicateurs** — seuls divergent les chemins runtime et les champs worker_budget, RAM au lancement ; 0 champ "
    "scientifique divergent ; 3 redémarrages machine, reprise par le lanceur). **Discrimination : S_sep 6/8** "
    "(HP35, TCGA v4, ICGC, immunitaire, PARP, DepMap ; échecs GSE71729 +0,0405, GSE62452 −0,0072), 16/23 en annexe — "
    "exactement max_separation en v6.1 ; MC 7/8 et max_separation 7/8 en v6.2 contre 1/8 et 6/8 en v6.1 **parce que la "
    "gigue appliquée est passée de 0,07 à 0,00 mesurée, pas parce que l'instrument a changé** ; avec le forfait 0,07 "
    "les verdicts seraient ceux de la v6.1. **Delta NON ÉLUCIDÉ** (222 runs : meilleure combinaison masque+MFA+n 80,2 % "
    "paire / 61,7 % valeur, sous les 90 % exigés ; DFA −38,16 retrouvé, sans effet sur d_sat). | **La v6.2 ne sépare "
    "pas mieux que la v6.1 ; elle sépare pareil, et de façon déterministe (gigue 0). S_sep atteint la barre ≥ 6/8 "
    "mais n'apporte rien au-delà de max_separation ici (stabilité ~0,98–1,00, saturée). Adoption comme version de "
    "travail : attend le go de Zackary — v6.1 reste la version de travail, v6 la référence.** Voir §8.37. |\n"
)
lines = wb.split("\n")
idx42 = next(i for i, l in enumerate(lines) if l.startswith("| 42 |"))
assert lines[idx42 + 1].startswith("| 40 |") is False  # garde-fou : la ligne 42 est bien la dernière du tableau
lines.insert(idx42 + 1, row43.rstrip("\n"))
wb = "\n".join(lines)

# --- 3. Entrées de journal, à la fin du fichier ---
journal = (
    "- **18–19 nov. 2026 : v6.2 CONSTRUITE, VALIDÉE, TESTÉE — §8.37.** Go de Zackary 18 nov. 18h07 (« pousser mon "
    "pipeline, je veux vraiment qu'il soit en capacité de trouver un remède, pas juste montrer un axe »). Protocole "
    "gelé avant tout code (`PROTOCOL_v6.2.md`, SHA `6e9324a2…dfad` — l'annonce `fb27b39a…` de son auteur ne correspond "
    "pas au fichier, le SHA mesuré fait foi). Construction sur copie : `build_v6.2.py` (SHA `5348636e…fa0`), un seul "
    "changement — `hash(metric)` remplacé par `hashlib.sha256` stable dans le seed L5 (ligne 8985), + `import "
    "hashlib` + `VERSION_MASTER` v6.2.0 ; diff 3 hunks, compilation OK, v6.2 SHA `f07567c4…3abf`, v6.1 et v6 "
    "inchangées ; 1er essai arrêté sur assertion (la note d'en-tête contenait elle-même la chaîne `hash(metric)`), "
    "reformulée, reconstruction propre. **Validation 20/20 exit 0** (10 runs fast × 2, processus séparés, 3 "
    "redémarrages machine, reprise par le lanceur) : cascades identiques à la v6.1 sur 10/10, L7a finis sur les "
    "petites cohortes, **gigue mesurée = 0,0000 sur tous les indicateurs** — les JSON ne sont pas identiques octet "
    "pour octet, mais les seules divergences sont les chemins runtime et les champs worker_budget (RAM au "
    "lancement) : 0 champ scientifique divergent. **Discrimination : S_sep = max_separation × stability atteint "
    "6/8** (barre du protocole), 16/23 en annexe — exactement max_separation en v6.1, mêmes paires ; MC 7/8 et "
    "max_separation 7/8 en v6.2 (1/8 et 6/8 en v6.1) uniquement parce que la gigue appliquée est passée de 0,07 à "
    "0,00 mesurée — avec le forfait 0,07, les verdicts seraient ceux de la v6.1. **Delta NON ÉLUCIDÉ** (222 runs ; "
    "meilleure combinaison 80,2 % / 61,7 %, sous les 90 % ; DFA −38,16 retrouvé, sans effet sur d_sat). **Verdict : "
    "la v6.2 ne sépare pas mieux que la v6.1 ; elle sépare pareil, et de façon déterministe.** Adoption comme "
    "version de travail : attend le go de Zackary après lecture — v6.1 reste la version de travail. PDF non "
    "régénéré, rien poussé sur GitHub. Détail au §8.37 ; ligne 43 au §7.\n"
    "- **18 nov. 2026, 18h07 : POUSSÉES GITHUB RÉUSSIES (correction des entrées 16h04 et 16h28–17h00, qui disaient "
    "« approbation expirée, rien poussé »).** Après une nouvelle approbation de Zackary, poussées et vérifiées par "
    "relecture distante : PDAC commit `8c88810b` (livre blanc §8.30–§8.36, 48 fichiers), Code commit `70f52ad5` "
    "(v6.1, SHA `2af5e5ce…c1c9`). Les deux dépôts restent privés à ce moment-là. **18 nov. 19h10 : Zackary annonce "
    "un nouveau dépôt, https://github.com/FindPrint/tlogNext-cancer-pdac (commit initial `baf1e02f`, vérifié), et "
    "qu'il a mis les deux anciens dépôts PUBLICS lui-même — toute publication future (PDF avec §8.37, v6.2 si "
    "adoptée) va dans `tlogNext-cancer-pdac`, pas dans les anciens ; l'App GitHub devra être vérifiée installée "
    "sur le nouveau dépôt avant de pousser (voir `runs/pdac-v6/PUBLICATION_tlogNext.md`).**\n"
)
wb = wb.rstrip("\n") + "\n" + journal

open(W, "w", encoding="utf-8").write(wb)
print("OK — lignes:", len(wb.split("\n")))
print("§8.37 présent:", wb.count("### 8.37 v6.2"))
print("ligne 43 présente:", wb.count("| 43 |"))
print("journal v6.2 présent:", "v6.2 CONSTRUITE, VALIDÉE, TESTÉE" in wb)
print("journal GitHub présent:", "POUSSÉES GITHUB RÉUSSIES" in wb)
