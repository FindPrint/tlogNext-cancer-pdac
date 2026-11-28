#!/usr/bin/env python3
"""Fusion §8.101 + §8.102 + §8.103 + résumé exécutif dans le livre blanc PDAC.

Ordre (même pratique que fuse_8100.py) : sauvegarde .bak-8103, insertion
des trois sections avant « ### 8.5 », résumé exécutif avant « ## 8.
Résultats et analyses » (titre « # » -> « ## » à la fusion), lignes
107/108/109 au §7 après la ligne 106, token __LIGNES_TOTALES__ remplacé
par le total final calculé.

Différences vs §8.100 :
- §8.101 n'a PAS de marqueur de fin dans son fichier source (contrairement
  à §8.102/§8.103) : le marqueur « — Fin de la §8.101. — » est AJOUTÉ à la
  fusion (il apparaîtra dans ce PDF-ci, pas de dette reportée comme §8.99).
- Aucune des trois sections ne porte de bloc « ## Ligne §7 » : les lignes
  107/108/109 sont écrites ici, dans le style de la table §7.
- Le résumé exécutif porte deux tokens : __LIGNES_TOTALES__ (remplacé ici
  par le total calculé) et __TEST_V621__ (DOIT être rempli AVANT la fusion,
  avec le résultat des tests de non-régression v6.2.1 — le script refuse
  sinon).

Préconditions : livre blanc 27 117 lignes, SHA 201a12d4… (journal des
poussées §8.100 inclus) ; sections SHA cb443b8a… / c01c15f9… / ce8f20df… ;
provenances SHA 4f7d4275… / 991dda3d… / 92ce3f57… ; v6.2.1 SHA 11a533e6….
"""
import hashlib
import shutil

RUNS = "/home/hatch/workspace/runs/pdac-v6"
LB = "/home/hatch/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md"
SEC101 = RUNS + "/section_8.101_consolidation_gse184585_200nuls.md"
SEC102 = RUNS + "/section_8.102_gse313117.md"
SEC103 = RUNS + "/section_8.103_delta_elucidation.md"
RESUME = RUNS + "/RESUME_EXECUTIF_draft.md"
V621 = "/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.1_cohen.py"


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
assert sha(SEC101).startswith("cb443b8a"), sha(SEC101)[:16]
assert sha(SEC102).startswith("c01c15f9"), sha(SEC102)[:16]
assert sha(SEC103).startswith("ce8f20df"), sha(SEC103)[:16]
assert sha(RUNS + "/PROVENANCE_8101.md").startswith("4f7d4275")
assert sha(RUNS + "/PROVENANCE_8102.md").startswith("991dda3d")
assert sha(RUNS + "/PROVENANCE_8103.md").startswith("92ce3f57")
assert sha(V621).startswith("11a533e6"), sha(V621)[:16]
wb = open(LB, encoding="utf-8").read()
lines_before = wb.count("\n") + (0 if wb.endswith("\n") else 1)
lb_sha_before = sha(LB)
print(f"livre blanc avant fusion : {lines_before} lignes, SHA {lb_sha_before[:16]}...")
assert lines_before == 27117, f"lignes attendues 27117, lues {lines_before}"
assert lb_sha_before.startswith("201a12d4"), f"SHA attendu 201a12d4..., lu {lb_sha_before[:16]}"
ligne7_avant = wb.count("## Ligne §7")
print(f"occurrences '## Ligne §7' avant fusion : {ligne7_avant} (prose du journal §8.100, pré-existante)")
assert wb.count("### 8.101") == 0, "§8.101 déjà présent"
assert wb.count("### 8.102") == 0, "§8.102 déjà présent"
assert wb.count("### 8.103") == 0, "§8.103 déjà présent"
assert wb.count("## Résumé exécutif") == 0, "résumé déjà présent"

# --- 1. Sauvegarde ---
bak = LB + ".bak-8103"
shutil.copyfile(LB, bak)
assert sha(bak) == lb_sha_before
print(f"sauvegarde : {bak} (SHA conforme)")

# --- 2. Lecture des sections ---
def read_section(path, num):
    txt = open(path, encoding="utf-8").read()
    lines = txt.split("\n")
    assert lines[0].startswith(f"### 8.{num} "), lines[0][:40]
    return txt

s101 = read_section(SEC101, 101)
s102 = read_section(SEC102, 102)
s103 = read_section(SEC103, 103)
# §8.101 : pas de marqueur de fin dans le fichier source — on l'ajoute.
assert "— Fin de la §8.101. —" not in s101
s101 = s101.rstrip("\n") + "\n\n— Fin de la §8.101. —\n"
assert s101.count("— Fin de la §8.101. —") == 1
assert s102.rstrip("\n").endswith("— Fin de la §8.102. —"), "marqueur §8.102 absent"
assert s103.rstrip("\n").endswith("— Fin de la §8.103. —"), "marqueur §8.103 absent"
for tag, txt in (("8.101", s101), ("8.102", s102), ("8.103", s103)):
    assert f"### 8.8.{tag.split('.')[1]}" not in txt, f"titre doublé dans §{tag}"
    assert "## Ligne §7" not in txt, f"bloc Ligne §7 dans §{tag}"
print("sections lues : §8.101 (marqueur ajouté), §8.102, §8.103")

# --- 3. Résumé exécutif ---
resume = open(RESUME, encoding="utf-8").read()
assert resume.count("__LIGNES_TOTALES__") == 1, "token lignes absent ou multiple"
assert "__TEST_V621__" not in resume, "token TEST_V621 non rempli — remplir le résultat des tests v6.2.1 AVANT la fusion"
assert "BROUILLON" not in resume and "PLACEHOLDER" not in resume
assert resume.startswith("# Résumé exécutif — Projet PDAC"), resume[:50]
resume = resume.replace("# Résumé exécutif — Projet PDAC",
                        "## Résumé exécutif — Projet PDAC", 1)
print("résumé lu (token lignes : 1, token test : rempli)")

# --- 4. Lignes §7 (107/108/109) ---
row107 = "| 107 | 28 nov. 2026 | **Consolidation GSE184585 à 200 nuls — FRAGILE (§8.101)** (lot §8.101 terminé 28 nov. 07h33, 100/100 locaux + 90/90 GitHub ; réel maxsep 0,3712 > p95 des nuls 0,3014 MAIS seulement 188/200 nuls sous le plancher 0,07 (94,0 %, il en fallait 190/200) ; rang 200/201, un seul nul au-dessus ; deux nuls à < 0,0001 du plancher (s9335 +0,0699, s9469 +0,0699942) ; le SOLIDE à 10 nuls du §8.99 ne survit pas à la consolidation ; MC réel 0,3552 (nuls médiane 0,3337, p95 0,3494), Delta 1,2804, falsification 0,2974 non significative, L7a down (0,1914), L7b FRAGILE (light), F1 0,6418, F2 0,1415 ; A2-distrib 5/16 paires PDAC (6/16 avec HP35), LOO 5/15 (4/14 paires PDAC) ; scores compagnons extraits, dette §8.99.7 soldée). Détail au §8.101. |"
row108 = "| 108 | 27 nov. 2026 | **Nouvelle paire : GSE313117 — FRAGILE à 10 nuls (§8.102)** (79 patients PDAC, essai PANCREAS NCT04683315, TPM 24 416 gènes × 79 ; 11/12 gènes exacts + MUCL3 pour DPCR1, remappage re-vérifié HGNC:21666 ; réel maxsep 0,4261 > p95 0,3614 MAIS 9/10 écarts > 0,07 (90,0 %, il fallait 95 %) ; Δρ médian +0,3070, 11/12 positifs ; nul graine 42 : écart +0,1278, A2 classique 11/16 → 12/17, LOO pire cas 10/15 → 11/16 ; première candidate GSE55643 écartée (cas complets 24/45 < 40, sans imputation) ; consolidation à 200 nuls proposée comme décisive). Détail au §8.102. |"
row109 = "| 109 | 27 nov. 2026 | **Delta, nouvelle tentative d'élucidation — NON ÉLUCIDÉ (§8.103)** (6e tentative ; corpus 3 015 runs §8.98 ; Delta(w) est une courbe irrégulière non monotone — 10 niveaux distincts sur 11 w, pas un escalier ; à w fixe, réel et nuls coïncident presque partout SAUF à w = 30 (le w du réel, +0,34 à +0,40 au-dessus des 10 nuls) ; la médiane LOO prédit chaque build à ±0,10 sur 113/121 ; extension B4b (~19 h, 800 builds) validée NON lancée — le critère (i) tranche déjà le verdict ; ne pas rouvrir Delta sans angle réellement nouveau). Détail au §8.103. |"

# --- 5. Insertion du résumé avant « ## 8. Résultats et analyses » ---
anchor8 = "## 8. Résultats et analyses"
assert wb.count(anchor8) == 1, f"ancre ## 8 : {wb.count(anchor8)} occurrences"
wb = wb.replace(anchor8, resume.rstrip("\n") + "\n\n" + anchor8, 1)
assert wb.count("## Résumé exécutif — Projet PDAC") == 1
print("résumé inséré avant ## 8")

# --- 6. Insertion des trois sections avant « ### 8.5 » ---
anchor = "### 8.5 Synthèse des 4 versions — ce qui bouge, ce qui ne bouge pas"
assert wb.count(anchor) == 1, f"ancre ### 8.5 : {wb.count(anchor)} occurrences"
block = s101.rstrip("\n") + "\n\n" + s102.rstrip("\n") + "\n\n" + s103.rstrip("\n") + "\n\n"
wb = wb.replace(anchor, block + anchor, 1)
assert wb.count("### 8.101 Consolidation GSE184585") == 1
assert wb.count("### 8.102 Nouvelle paire : GSE313117") == 1
assert wb.count("### 8.103 Delta, nouvelle tentative") == 1
assert wb.count("— Fin de la §8.101. —") == 1
assert wb.count("— Fin de la §8.102. —") == 1
assert wb.count("— Fin de la §8.103. —") == 1
print("sections §8.101/§8.102/§8.103 insérées avant ### 8.5")

# --- 7. Lignes 107/108/109 au §7, après la ligne 106 ---
row106_anchor = "| 106 | 27 nov. 2026 | **Fusion des cinq dépôts"
assert wb.count(row106_anchor) == 1
i = wb.index(row106_anchor)
j = wb.index("\n", i)
wb = wb[:j] + "\n" + row107 + "\n" + row108 + "\n" + row109 + wb[j:]
assert wb.count("| 107 | 28 nov. 2026 |") == 1
assert wb.count("| 108 | 27 nov. 2026 |") == 1
assert wb.count("| 109 | 27 nov. 2026 |") == 1
print("lignes 107/108/109 ajoutées au §7")

# --- 8. Token lignes : total final calculé ---
lines_after = wb.count("\n") + (0 if wb.endswith("\n") else 1)
assert wb.count("__LIGNES_TOTALES__") == 1
wb = wb.replace("__LIGNES_TOTALES__", f"{lines_after:,}".replace(",", " "), 1)
lines_final = wb.count("\n") + (0 if wb.endswith("\n") else 1)
assert lines_final == lines_after, "le remplacement du token a changé le nombre de lignes"
print(f"token lignes remplacé par {lines_after}")

# --- 9. Écriture + vérifications ---
open(LB, "w", encoding="utf-8").write(wb)
lb_sha_after = sha(LB)
print(f"livre blanc après fusion : {lines_final} lignes (+{lines_final - lines_before}), SHA {lb_sha_after[:16]}...")
assert "### 8.8.101" not in wb and "### 8.8.102" not in wb and "### 8.8.103" not in wb
assert "### 8.101.101" not in wb and "### 8.102.102" not in wb and "### 8.103.103" not in wb
assert wb.count("### 8.5 Synthèse des 4 versions — ce qui bouge, ce qui ne bouge pas") == 1
assert wb.count("## Ligne §7") == ligne7_avant, "nouveau bloc Ligne §7 introduit"
assert "__LIGNES_TOTALES__" not in wb and "__TEST_V621__" not in wb
assert wb.count("## Résumé exécutif — Projet PDAC") == 1
print("vérifications : 0 titre doublé, 0 marqueur dupliqué, lignes §7 107/108/109 1/1, 0 token restant")
print(f"SHA avant : {lb_sha_before}")
print(f"SHA après : {lb_sha_after}")
print(f"LIGNES : {lines_before} -> {lines_final}")
