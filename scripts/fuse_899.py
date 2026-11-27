#!/usr/bin/env python3
"""Fusion §8.99 dans le livre blanc PDAC + ligne §7 + addendum Cox §8.12
+ addendum registre A2 (§8.99.4).

Ordre (même pratique que §8.98) : sauvegarde .bak-899, insertion de la
section avant « ### 8.5 », ligne 105 au §7, addendum §8.12 daté 27 nov. 2026,
addendum A2 daté 27 nov. 2026 (nul graine 42 lu dans son dossier de run).
Le nul graine 42 doit exister (results_fast_v62_899_gse184585_nul_s42/
master_results.json) — sinon arrêt, rien n'est modifié.
"""
import hashlib
import json
import os
import shutil
import sys

RUNS = "/home/hatch/workspace/runs/pdac-v6"
LB = "/home/hatch/workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md"
SEC = os.path.join(RUNS, "section_8.99_gse184585.md")
S42 = os.path.join(RUNS, "results_fast_v62_899_gse184585_nul_s42/master_results.json")
REAL = os.path.join(RUNS, "results_fast_v62_899_gse184585/master_results.json")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def maxsep(path):
    m = json.load(open(path))
    return m["run_pipeline"]["threshold_metadata"]["threshold_optimization"]["best_config"]["metrics"]["max_separation"]


def fail(msg):
    print("ABANDON :", msg, file=sys.stderr)
    sys.exit(2)


# --- 0. Préconditions ---
if not os.path.exists(S42):
    fail("nul graine 42 non couru (pas de master_results.json) — lancer run_899_s42.sh d'abord")
real_ms = maxsep(REAL)
s42_ms = maxsep(S42)
d42 = real_ms - s42_ms
a2_pass = d42 > 0.07
print(f"réel maxsep={real_ms:.4f} | nul s42 maxsep={s42_ms:.4f} | écart={d42:+.4f} | A2: {'PASSE' if a2_pass else 'NON'}")
# A2 classique avant : 10/15 (§8.88). Après : 11/16 si passe, 10/16 sinon.
a2_new = "11/16" if a2_pass else "10/16"
# LOO pire cas (A2 classique) : avant 9/14 (§8.88). Avec 16 paires :
# si la nouvelle passe : retirer une passante -> 10/15 ; retirer une non-passante -> 11/15 ; pire = 10/15.
# si elle ne passe pas : retirer une passante -> 9/15 ; pire = 9/15.
loo_new = "10/15" if a2_pass else "9/15"
print(f"A2 classique : 10/15 -> {a2_new} | LOO pire cas : 9/14 -> {loo_new}")

wb = open(LB, encoding="utf-8").read()
lines_before = wb.count("\n") + (0 if wb.endswith("\n") else 1)
lb_sha_before = sha(LB)
print(f"livre blanc avant fusion : {lines_before} lignes, SHA {lb_sha_before[:16]}...")
assert lines_before == 26317, f"lignes attendues 26317, lues {lines_before}"
assert lb_sha_before.startswith("02f56d33"), f"SHA attendu 02f56d33..., lu {lb_sha_before[:16]}"

# --- 1. Sauvegarde ---
bak = LB + ".bak-899"
shutil.copyfile(LB, bak)
assert sha(bak) == lb_sha_before
print(f"sauvegarde : {bak} (SHA conforme)")

# --- 2. Insertion de la section avant ### 8.5 ---
body = open(SEC, encoding="utf-8").read().rstrip("\n") + "\n"
assert body.startswith("### 8.99 "), "la section ne commence pas par ### 8.99"
assert "### 8.8.99" not in body and "### 8.99.99" not in body
anchor = "### 8.5 Synthèse des 4 versions — ce qui bouge, ce qui ne bouge pas"
assert wb.count(anchor) == 1, f"ancre ### 8.5 : {wb.count(anchor)} occurrences"
wb = wb.replace(anchor, body + "\n" + anchor, 1)
assert wb.count("### 8.99 Nouvelle paire") == 1
assert wb.count("## 8.99.1") == 1 and wb.count("## 8.99.8") == 1
print("section §8.99 insérée avant ### 8.5")

# --- 3. Addendum A2 (§8.99.4), juste avant ## 8.99.5 ---
a2_text = (
    f"\n**ADDENDUM 27 nov. 2026 (registre A2, coordinateur) :** nul graine 42 couru après le verdict, "
    f"hors du protocole gelé §8.99 (qui juge sur les 10 nuls frais 9301–9310), pour le registre A2 classique "
    f"uniquement — il ne change pas le verdict SOLIDE ci-dessus. Nul s42 : `maxsep` {s42_ms:.4f}, écart "
    f"réel−nul s42 {d42:+.4f} ({'au-dessus' if a2_pass else 'en dessous'} du plancher 0,07) : "
    f"**A2 classique 10/15 → {a2_new}**, LOO pire cas 9/14 → {loo_new}. "
    f"CSV `pdac_899_gse184585_fluxes_nul_s42.csv`, run `results_fast_v62_899_gse184585_nul_s42`, "
    f"lanceur `run_899_s42.sh`, journal `runs_899_s42.log`. A2-distrib (200 nuls) inchangé 6/15 : "
    f"la paire n'y entre qu'après la consolidation à 200 nuls (§8.99.7, limite 1).\n"
)
anchor_995 = "## 8.99.5 — Tests directs en appui (ne décident pas)"
assert wb.count(anchor_995) == 1
wb = wb.replace(anchor_995, a2_text + "\n" + anchor_995, 1)
print("addendum A2 ajouté au §8.99.4")

# --- 4. Addendum Cox §8.12, après la correction du 16 nov. ---
cox_anchor = "La conclusion se renforce, elle ne s'affaiblit pas."
assert wb.count(cox_anchor) == 1
cox_text = (
    "\n\n**CORRECTION 27 nov. 2026 (re-vérification Cox, trois implémentations indépendantes) :** "
    "les HR univariés et multivariés publiés au §8.12 se reproduisent. Univariés (résidus v4 corrigés de la "
    "pureté, HR par +1 écart-type, n=177, 92 décès) : KRAS 1,4232 (p=0,0003), MUC16 1,4386 (p=0,0011), "
    "CEACAM5 1,3081 (p=0,0106), DPCR1 1,4259 (p=0,0011) ; multivariés (KRAS+MUC16+CEACAM5) : KRAS 1,3265 "
    "(p=0,0146), MUC16 1,3155 (p=0,0191), CEACAM5 1,0708 (p=0,5716) — accord à 0,001 près entre "
    "l'implémentation maison (Breslow, Newton-Raphson), statsmodels (Breslow/Efron) et lifelines (Efron). "
    "La non-reproduction signalée par la revue indépendante du 15 nov. (universal-log-research, "
    "REVUE_INDEPENDANTE_2026-11-15) n'est pas confirmée par ce re-calcul ; causes plausibles de l'écart de "
    "la revue : jointure naïve sur le CSV de flux sans identifiants (signal détruit) ou HR par unité log2 "
    "non standardisée. Le script original du 15 nov. reste introuvable ; le fichier archivé "
    "`check_cox_tcga_results.txt` contient un bloc buggué antérieur à la correction du vérificateur "
    "(MUC16 1,58) et n'est pas la source des chiffres publiés. Médiane KM de cohorte : **20,0 → 20,2 mois** "
    "(définition pas-à-pas, premier temps où S ≤ 0,5 ; confirmée par lifelines 20,2) — écart déjà documenté "
    "au §8.83.1 ; la médiane simple des temps observés (15,2) n'est pas une médiane de survie. "
    "Script `survival_tcga_recalc_20261127.py` (SHA `6da679c6…3529b56`), hypothèses "
    "`survival_tcga_recalc_20261127_hypotheses.py` (SHA `ac739f1d…ed27a`), résultats "
    "`survival_tcga_recalc_20261127_results.txt` (SHA `fa5cff07…20b20`)."
)
wb = wb.replace(cox_anchor, cox_anchor + cox_text, 1)
print("addendum Cox ajouté au §8.12")

# --- 5. Ligne 105 au §7, après la ligne 104 ---
row104_anchor = "| 104 | 22–23 nov. 2026 | **Suivi §8.93"
assert wb.count(row104_anchor) == 1
# fin de la ligne 104 : jusqu'au retour à la ligne suivant l'ancre
i = wb.index(row104_anchor)
j = wb.index("\n", i)
row105 = (
    "\n| 105 | 27 nov. 2026 | **Nouvelle paire : GSE184585 CONFIRME — SOLIDE à 10 nuls (§8.99)** "
    "(protocole gelé avant tout run `PROTOCOL_899_gse184585.md`, SHA `00f04748…3057c` ; provenance "
    "`PROVENANCE_899.md` ; cohorte GSE184585, 82 tumeurs PDAC primaires MSKCC, GPL17586, choisie avant toute "
    "lecture d'association — aucune candidate §8.78 ne passait les portes ; remappage DPCR1 → MUCL3 vérifié 5/5 ; "
    "pipeline v6.2 SHA `f07567c4…` inchangé ; 11/11 runs exit 0, nuls frais graines 9301–9310 ; "
    f"**réel 0,3712, médiane des nuls 0,2231, p95 0,2884, 10/10 écarts > 0,07 (min +0,0777)** — SOLIDE selon la règle "
    "gelée §8.93 §4 ; MC réel 0,3552 sous le p95 MC des nuls 0,3722 (rapporté, ne décide pas) ; tests directs partagés "
    "(Δρ médian −0,0098, CEACAM5 +0,550, CLCA1 −0,531) ; A2 classique 10/15 → " + a2_new +
    f" (nul graine 42, addendum §8.99.4), LOO pire cas 9/14 → {loo_new} ; consolidation 200 nuls non faite, nommée "
    "comme suite ; **correction Cox §8.12 (addendum 27 nov.) : HR univariés et multivariés reproduits par 3 "
    "implémentations, médiane KM 20,0 → 20,2 mois** ; dette SHA du §8.98 soldée le 27 nov. (209/209). Détail au §8.99. |"
)
wb = wb[:j] + row105 + wb[j:]
assert wb.count("| 105 | 27 nov. 2026 |") == 1
print("ligne 105 ajoutée au §7")

# --- 6. Écriture + vérifications ---
open(LB, "w", encoding="utf-8").write(wb)
lines_after = wb.count("\n") + (0 if wb.endswith("\n") else 1)
lb_sha_after = sha(LB)
print(f"livre blanc après fusion : {lines_after} lignes (+{lines_after - lines_before}), SHA {lb_sha_after[:16]}...")
assert "### 8.8.99" not in wb and "### 8.99.99" not in wb
assert wb.count("### 8.99 Nouvelle paire") == 1
assert wb.count("### 8.5 Synthèse des 4 versions — ce qui bouge, ce qui ne bouge pas") == 1
assert wb.count("CORRECTION 27 nov. 2026 (re-vérification Cox") == 1
assert wb.count("ADDENDUM 27 nov. 2026 (registre A2") == 1
print("vérifications : 0 titre doublé, 0 marqueur dupliqué, addenda 2/2 présents")
print(f"SHA avant : {lb_sha_before}")
print(f"SHA après : {lb_sha_after}")
print(f"LIGNES : {lines_before} -> {lines_after}")
print(f"A2 : {a2_new} | LOO : {loo_new}")
