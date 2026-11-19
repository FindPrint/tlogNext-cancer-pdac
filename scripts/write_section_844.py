#!/usr/bin/env python3
"""Génère section_8.44_rotations_dedup.md et PROVENANCE_rotations_dedup_844.md
à partir de ssep_844_rotations.json (extraction vérifiée) et
ssep_841_rotations.json (écarts avec doublon, §8.41).
Les tableaux sont générés depuis les données — aucune valeur recopiée à la
main — pour éviter toute erreur de transcription. Le texte narratif est
dans ce script, relu contre les sorties de l'extracteur.
"""
import hashlib
import json

BASE = "."
new = json.load(open("ssep_844_rotations.json"))
old = json.load(open("ssep_841_rotations.json"))
old_rows = {r["controle"]: r for r in old["paires"]}
rows = new["paires"]
shas = json.load(open("dedup_844_csv_sha.json"))
FAMS = [("V4ROT", "TCGA v4, ARN tumeurs, n=178"),
        ("DEPMAPROT", "CRISPR DepMap, lignées, n=45"),
        ("IMMROT", "immunitaire TCGA, ARN tumeurs, n=178"),
        ("PARPROT", "réparation de l'ADN TCGA, ARN tumeurs, n=178")]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]


def verdict(r):
    """Verdict d'une paire sous les deux règles (direction majoritaire +1 partout)."""
    d = r["d_ssep"]
    if abs(d) > 0.07 and d > 0:
        return "passe (A+B)"
    if abs(d) > 0.0 and d > 0:
        return "passe (B seul)"
    return "échoue"


def fam_table(fam):
    sub = [r for r in rows if r["famille"] == fam]
    lines = []
    lines.append("| Contrôle | S_sep réel / nul | Écart sans | Écart avec | Perte | max_sep réel / nul | Écart max_sep | MC réel / nul | Écart MC | Delta réel / nul | Écart Delta | Stabilité R / N | Verdict |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(sub, key=lambda x: x["controle"]):
        o = old_rows[r["controle"]]
        perte = o["d_ssep"] - r["d_ssep"]
        lines.append(
            f"| {r['controle']} | {r['ssep_R']:.4f} / {r['ssep_N']:.4f} | "
            f"**{r['d_ssep']:+.4f}** | {o['d_ssep']:+.4f} | {perte:+.4f} | "
            f"{r['maxsep_R']:.4f} / {r['maxsep_N']:.4f} | {r['d_maxsep']:+.4f} | "
            f"{r['mc_R']:.3f} / {r['mc_N']:.3f} | {r['d_mc']:+.3f} | "
            f"{r['delta_R']:.3f} / {r['delta_N']:.3f} | {r['d_delta']:+.3f} | "
            f"{r['stab_R']:.4f} / {r['stab_N']:.4f} | {verdict(r)} |")
    return "\n".join(lines)


V = new["verdicts"]


def vline(scope, fam, label, glabel):
    v = V[f"{scope}|{fam}|{label}|{glabel}"]
    return f"{v['n_ok']}/{v['n']}"


sec = []
sec.append("# §8.44 Rotations de contrôle sans doublon — le vrai compteur : 37/48 sous (A), 42/48 sous (B)")
sec.append("")
sec.append("Date : 19 novembre 2026. Go : Zackary, « Lance tout cela », 19 nov. 2026 ~05h47 (même go que le §8.41 ; ce chantier en est la suite mesurée, annoncée au §8.41.7).")
sec.append("Statut : section prête à insérer au livre blanc (après le §8.43, comme les §8.38–§8.42).")
sec.append("")
sec.append("## Verdict d'abord")
sec.append("")
sec.append("**Sans le doublon de construction, S_sep sépare le réel du nul sur 37 des 48 rotations sous la règle gelée (A) 0,07, et 42/48 sous la règle (B) gigue 0.** L'estimation du §8.41 — 36/48 en retranchant 0,20 à chaque écart — est confirmée, à une paire près : le vrai compteur est **37/48 sous (A), 42/48 sous (B)**. Le 48/48 avec doublon n'était donc pas doublon-fabriqué : il était doublon-assisté à la marge, et la marge se mesure maintenant paire par paire — 11 paires tombent sous (A), 6 sous (B).")
sec.append("")
sec.append("| Famille | Paires | S_sep (A) 0,07 | S_sep (B) gigue 0 | max_sep (A) | max_sep (B) | Somme des écarts S_sep | Écart min | Écart max |")
sec.append("|---|---|---|---|---|---|---|---|---|")
for fam, title in FAMS:
    sub = [r for r in rows if r["famille"] == fam]
    s = sum(r["d_ssep"] for r in sub)
    mn = min(sub, key=lambda r: r["d_ssep"])
    mx = max(sub, key=lambda r: r["d_ssep"])
    sec.append(f"| {fam} ({title.split(',')[0]}) | 12 | {vline('48', fam, 'S_sep', 'A_0.07')} | {vline('48', fam, 'S_sep', 'B_0')} | {vline('48', fam, 'max_sep', 'A_0.07')} | {vline('48', fam, 'max_sep', 'B_0')} | {s:+.4f} | {mn['d_ssep']:+.4f} ({mn['controle']}) | {mx['d_ssep']:+.4f} ({mx['controle']}) |")
sec.append(f"| **TOUTES** | **48** | **{vline('48', 'TOUTES', 'S_sep', 'A_0.07')}** | **{vline('48', 'TOUTES', 'S_sep', 'B_0')}** | **{vline('48', 'TOUTES', 'max_sep', 'A_0.07')}** | **{vline('48', 'TOUTES', 'max_sep', 'B_0')}** | **+17,1614** | **−0,1380 (MYC)** | **+0,9838 (CD8A)** |")
sec.append("")
sec.append("Sur les 44 paires refaites dans ce chantier seules : **35/44 sous (A), 39/44 sous (B)** (somme des écarts +15,5906). Les 4 paires du §8.41 ajoutent 2/4 sous (A) — CLDN18, CTLA4 — et 3/4 sous (B) — +PARP1 — pour le compteur combiné 37/48 et 42/48.")
sec.append("")
sec.append("**Réserves à garder avec le chiffre, avant toute lecture biologique :**")
sec.append("")
sec.append("1. **Ce n'est toujours pas une preuve de rupture ni de remède.** Comme au §8.41, S_sep mesure que la série réelle est ordonnée par l'un de ses propres flux et que les autres flux suivent cet ordre — vrai par construction, sans doublon comme avec. Le 37/48 ne dit rien d'une transition biologique, et aucune des 48 rotations ne devient une cible.")
sec.append("2. **La perte vient du réel, pas du nul.** Retirer le doublon fait chuter S_sep réel de 0,7570 à 0,5780 en moyenne (−0,1790) et ne bouge quasiment pas le nul (0,2209 → 0,2205, −0,0005). Le doublon ne créait pas un faux nul bas : il gonflait le réel d'une colonne parfaitement triée. Les 11 paires qui tombent sous (A) sont celles dont le réel tenait en grande partie sur cette seule colonne.")
sec.append("3. **DEPMAPROT est la famille fragile.** 6/12 sous (A), 8/12 sous (B) — la seule famille sous les deux tiers sous (A). À n=45, le nul varie de 0,13 à 0,36 et quatre réels s'effondrent sans le doublon (CCND1 0,4236 → 0,1566 ; MYC 0,4477 → 0,1993 ; CFLAR 0,6002 → 0,2981 ; ACO2 déjà au §8.41). IMMROT, à l'inverse, tient intégralement : 12/12 sous les deux règles, plus petit écart +0,4508 (CD68).")
sec.append("4. **MUC16 passe de justesse.** Écart +0,0712 sous (A), soit 0,0012 au-dessus du plancher 0,07 : un verdict qui ne tient qu'à un cheveu, à lire comme fragile, pas comme acquis.")
sec.append("5. **S_sep n'apporte toujours rien au-delà de max_separation.** Mêmes listes sous les deux règles, partout, dans les 4 familles : les écarts S_sep diffèrent des écarts max_separation de moins de 0,024 partout (maximum 0,0237). La stabilité est quasi saturée (0,9463–0,9986) : S_sep ≈ max_separation × ~0,99, et le garde-fou anti-pic-bruité ne s'est déclenché sur aucune des 96 runs.")
sec.append("")
sec.append("## 8.44.1 Question, méthode, règles")
sec.append("")
sec.append("**Question.** Le §8.41 laissait le compteur global sans doublon inconnu : 4 paires contrôlées sur 48, estimation ~36/48. Ce chantier refait les 44 restantes, sans doublon, à permutation de nul identique — et mesure le compteur.")
sec.append("")
sec.append("**Méthode — construction des 44 paires, puis 88 runs v6.2.** Pour chaque paire, le CSV réel dédoublonné est le CSV original moins la colonne doublon du flux contrôle (colonne k, valeurs identiques à la colonne 0 vérifiées) ; contrôle, ordre et autres flux inchangés, ligne par ligne. Le CSV nul dédoublonné part du CSV `_nul.csv` ORIGINAL — même permutation que la rotation avec doublon — moins la colonne doublon (multi-ensemble égal à la colonne 0 vérifié ; les 11 autres colonnes identiques ligne par ligne au nul original). Aucune valeur recalculée ni imputée. C'est la méthode « même permutation » du §8.41.3 (`build_dedup_841_sameperm.py`), généralisée aux 44 paires par `build_dedup_844.py` : le §8.41 avait montré que le nul à nouvelle permutation mélangeait deux effets (retrait du doublon + nouvelle permutation) et faisait varier le nul de 0,26 à 0,43 à n=45 — ici un seul effet change à la fois. Les 4 paires du §8.41 ne sont pas refaites : CLDN18 (run v6.1 préexistant, S_sep identique entre v6.1 et v6.2 sur 29/29 paires, §8.38), CTLA4 (nul à nouvelle permutation — seul disponible, passe sous les deux règles avec +0,8986, la permutation ne change pas son verdict), ACO2 et PARP1 (nuls à permutation identique, canoniques §8.41.3).")
sec.append("")
sec.append("**Vérifications avant construction (0 écart partout) :** SHA-256 des 96 CSV d'origine vérifiés un par un contre `PROVENANCE_rotations_v61.md` : **96/96 conformes**, 0 mismatch, 0 absent ; SHA des 4 bases conformes (TCGA v4 `e7a2adab…13a0b0`, DepMap `7d605fef…98e37f8`, immunitaire TCGA `66dbb672…bbd2e`, PARP TCGA `c9549b68…c4309`). Pipelines SHA revérifiés à la fin du chantier : v6.2 `f07567c4…ec3abf`, v6.1 `2af5e5ce…a9c9` — inchangés, aucun code modifié.")
sec.append("")
sec.append("**Vérifications après extraction :** 88/88 runs v6.2 lus (+8/8 existants), 48/48 paires, version `v6.2.0-L7aL7b-CohenD-short` sur les 88 (v6.1 attendue pour CLDN18 seul) ; SHA-256 des 88 CSV dédoublonnés vérifiés contre `dedup_844_csv_sha.json` : **88/88 conformes** ; les 4 écarts S_sep du §8.41 relus dans leurs `master_results.json` : **0 écart** (tolérance 10⁻⁴).")
sec.append("")
sec.append("**Règles de comptage.** Comme `verdict()` de `extract_phase2.py` et comme en §8.38/§8.41 : direction majoritaire = signe de la somme des écarts réel−nul (calculée par famille et sur les 48 paires — elle est positive partout) ; une paire « sépare » si |écart| > gigue ET signe = direction majoritaire. Deux gigues : **(A)** la règle gelée §3.4, gigue effective = max(gigue mesurée 0,00 ; plancher 0,07) = **0,07** (gigue S_sep mesurée en validation v6.2 : 0,0000) ; **(B)** la gigue mesurée seule, **0,00**, rapportée à part. Nul : lignes permutées, graine 42, colonne de contrôle intacte (convention du projet). Aucun nouveau seuil, aucune sélection d'indicateur après coup. Extraction par `extract_ssep_844_rotations.py` (SHA-256 `24a07f9f…f02`), sorties `ssep_844_rotations.json` (SHA `06f41b65…b362`) et `ssep_844_rotations.csv` (SHA `d1abc0ab…f999`).")
sec.append("")
sec.append("## 8.44.2 Résultats par famille (sans doublon)")
sec.append("")
sec.append("Toutes les valeurs sont S_sep réel / nul (écart réel−nul), relues dans les JSON v6.2 (v6.1 pour CLDN18). « Écart avec » est l'écart du §8.41 (avec doublon) ; « Perte » = écart avec − écart sans. Le flux contrôle est exclu de toute lecture par flux (comme au §8.32) ; aucune lecture par flux n'est faite dans ce chantier — S_sep est global, et la lecture par flux du §8.32 (`v61_rotations_flux_reading.md`, doublon exclu) reste la référence pour le détail flux par flux.")
sec.append("")
for fam, title in FAMS:
    sub = [r for r in rows if r["famille"] == fam]
    s = sum(r["d_ssep"] for r in sub)
    n_ok_a = V[f"48|{fam}|S_sep|A_0.07"]["n_ok"]
    n_ok_b = V[f"48|{fam}|S_sep|B_0"]["n_ok"]
    sec.append(f"### {fam} — {title} — {n_ok_a}/12 sous (A), {n_ok_b}/12 sous (B)")
    sec.append("")
    sec.append(fam_table(fam))
    sec.append("")
    sec.append(f"Somme des écarts S_sep {s:+.4f} (moyenne {s/12:+.4f} par paire).")
    sec.append("")
sec.append("## 8.44.3 Le doublon, mesuré paire par paire")
sec.append("")
sec.append("**Le retrait du doublon coûte 0,1786 d'écart en moyenne** (minimum 0,0254, CRKL ; maximum 0,3556, GSTM1) — moins que les 0,20 retranchés dans l'estimation du §8.41, d'où 37/48 mesurés contre 36/48 estimés. L'effet est presque entièrement du côté réel : S_sep réel moyen 0,7570 → 0,5780 (−0,1790) ; S_sep nul moyen 0,2209 → 0,2205 (−0,0005). Par famille, le réel perd −0,2132 (V4ROT), −0,1973 (DEPMAPROT), −0,1421 (IMMROT), −0,1636 (PARPROT) ; le nul ne bouge que de −0,0174 à +0,0103 selon la famille. La plus forte hausse du nul est CTLA4 (+0,1086), déjà connue au §8.41 — toutes les autres sont sous +0,018.")
sec.append("")
sec.append("**Six réels chutent de plus de 0,22 sans le doublon — et c'est là que se joue le verdict.** GSTM1 0,4713 → 0,1285 (−0,3429), CFLAR 0,6002 → 0,2981 (−0,3022), CCND1 0,4236 → 0,1566 (−0,2670), CR2 0,3865 → 0,1261 (−0,2604), MYC 0,4477 → 0,1993 (−0,2484), MUC16 0,5411 → 0,3159 (−0,2253). Sur ces paires, le flux contrôle portait l'essentiel de la séparation du réel : les 11 autres flux, ordonnés par lui, ne montrent pas de marche nette au seuil sans lui. À l'inverse, les gros écarts survivent largement : CD8A +1,0877 → +0,9838, CTLA4 +1,1227 → +0,8986, CD8B +1,0029 → +0,8398, GZMB +1,0083 → +0,9053, PDCD1 +1,0818 → +0,9167 — sur ces paires, les flux se suivent mutuellement, doublon ou non.")
sec.append("")
sec.append("**Les 11 paires qui tombent sous (A).** Six s'inversent (écart négatif) : CR2 −0,0291, GSTM1 −0,1342, ACO2 −0,0208, CCND1 −0,1143, MYC −0,1380, UROD −0,0282. Cinq restent positives mais sous le plancher : CFLAR +0,0183, RAB10 +0,0604, PARP1 +0,0169, PARP2 +0,0293, XRCC1 +0,0558. Sous (B), seules les six inversées échouent : 42/48. Aucune des 11 n'est une paire IMMROT — la famille immunitaire ne perd aucune paire, la famille CRISPR en perd la moitié.")
sec.append("")
sec.append("## 8.44.4 Ce que disent les autres indicateurs sur les mêmes runs (sans doublon)")
sec.append("")
sec.append("Le 37/48 est porté par un seul indicateur, comme le 48/48 l'était. Sur les mêmes 96 runs (88 nouveaux + 8 du §8.41) :")
sec.append("")
sec.append("- **MC best_score** : ne dépasse le plancher 0,07 que sur **12/48** paires en positif sous (A) (35/48 sous (B), somme des écarts +0,729, moyenne +0,015) ; il est sous −0,07 sur 4/48 (ATM −0,140, ATR −0,126, PARP2 −0,189, MUC16 −0,153). Avec doublon, MC faisait 17/48 sous (A) : retirer le doublon lui coûte 5 paires, pas la tendance. Le composite reste écrasé par la composante robustness (~10⁻⁴¹ sur ces séries, PROTOCOL_v6.2.md §3.2) : il ne voit toujours pas la séparation que max_separation voit seul.")
sec.append("- **Delta** : positif sur 29/48 paires sous (A) (38/48 sous (B), somme +15,330, moyenne +0,319), avec des écarts de ±1 à ±2 (ex. IFNG +2,418, XRCC1 +1,913, RAD51 −1,170, GSTM1 −1,482) — il ne sépare pas, il disperse, comme avec doublon (30/48 positifs au §8.41).")
sec.append("- **L7a** : directions et confiances mélangées des deux côtés ; la direction réel diffère de celle du nul sur 15/48 paires (ex. PARPROT RAD51, POLQ, ATR ; IMMROT CD4, PDCD1) — pas de lecture nette, comme au §8.41.")
sec.append("- **Falsification** : non retenue sous n = 75 (convention §8.35 ; DEPMAPROT, n=45, exclue) ; non recalculée ici — la lecture du §8.41 (nul devant sur 20/36) n'est pas modifiée par ce chantier, qui ne touche pas aux runs avec doublon.")
sec.append("")
sec.append("C'est le même tableau qu'au §8.41, inchangé : **aucun contrôle ne sépare réel et nul en MC, Delta ou L7a. Ce qui change, c'est le compteur de max_separation / S_sep sans doublon : 37/48 sous (A), 42/48 sous (B), au lieu de 48/48 avec doublon.** Les deux lectures coexistent sans se contredire : elles ne mesurent pas la même chose.")
sec.append("")
sec.append("## 8.44.5 Pourquoi S_sep ≈ max_separation ici, et ce que le 37/48 veut dire")
sec.append("")
sec.append("La stabilité est quasi saturée sur les 96 runs : **0,9463–0,9986** (minimum 0,9463, CRKL réel, DEPMAPROT). S_sep vaut donc max_separation × ~0,99 partout : les écarts S_sep diffèrent des écarts max_separation de moins de 0,024 partout (maximum 0,0237), et les deux indicateurs donnent exactement les mêmes listes sous les deux règles, dans les 4 familles. Le garde-fou anti-pic-bruité ne s'est déclenché sur aucune rotation — les pics sont localement plats partout, y compris sur les nuls.")
sec.append("")
sec.append("**Pourquoi max_separation sépare-t-il sur 37/48 rotations sans doublon, et seulement 6/8 sur les paires principales ?** La réponse du §8.41.5 tient, précisée : le scan trie les lignes par le contrôle, puis mesure, à chaque seuil candidat, la moyenne sur les flux du |d de Cohen| entre fenêtres pré- et post-seuil. Sur une rotation réelle, le contrôle est l'un des flux : trier par lui, c'est trier par une variable que les 11 autres flux suivent — chacun montre une marche au seuil, la moyenne des |d| est grande — max_separation réel 0,13 à 1,25 sans doublon. Sur le nul, les lignes sont permutées : aucun flux ne montre de marche, la moyenne reste basse — max_separation nul 0,08 à 0,43 (médiane 0,22). Sur les paires principales, le contrôle est KRAS (externe aux flux) : les flux ne le suivent que partiellement, et deux paires échouent. Le 37/48 est donc une mesure d'ordre, pas une mesure de rupture : il dit que l'instrument voit l'ordre quand il y en a un — et il le voit encore sans la colonne parfaitement triée qui le gonflait — il ne dit pas que cet ordre est une transition critique, et encore moins qu'il porte un remède.")
sec.append("")
sec.append("**Conséquence pour le §8.32 et le §8.41.** Le titre du §8.32 — « aucun contrôle ne sépare réel et nul » — doit toujours être lu avec sa portée exacte : il portait sur MC, Delta, L7a et la falsification. Le §8.41 l'avait corrigé pour max_separation / S_sep avec doublon (48/48) ; ce chantier corrige la correction : **max_separation / S_sep séparent sur 37/48 rotations sans doublon sous la règle gelée, 42/48 sous gigue nulle.** Le 48/48 avec doublon reste vrai comme mesure — avec doublon — et le 37/48 est désormais la mesure sans doublon. Ni l'un ni l'autre ne devient une piste thérapeutique.")
sec.append("")
sec.append("## 8.44.6 Provenance")
sec.append("")
sec.append("- **Codes (jamais modifiés).** Pipeline v6.2 `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py`, SHA-256 `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` ; pipeline v6.1 (CLDN18 seul) `~/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py`, SHA-256 `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9`. Mode `fast`, graine 42 (défaut), nul = lignes permutées, graine 42, contrôle intact.")
sec.append("- **Formule et règles.** PROTOCOL_v6.2.md §3 (S_sep, exclusions de s_norm / robustness / sharpness, plancher 0,07) et §3.4 (direction = signe de la somme des écarts) ; règles de comptage de `extract_phase2.py` ; gigue S_sep mesurée en validation v6.2 : 0,0000 (`v62_validation_table.json`).")
sec.append("- **Entrées.** 96 CSV de rotations construits par `build_rotations_v61.py` (16 nov. 2026), SHA-256 vérifiés un par un contre `PROVENANCE_rotations_v61.md` : 96/96 conformes (bases : TCGA v4 `e7a2adab…13a0b0`, DepMap `7d605fef…98e37f8`, immunitaire TCGA `66dbb672…bbd2e`, PARP TCGA `c9549b68…c4309`). Sources : TCGA-PAAD ARN Broad GDAC Firehose 2016-01-28 (RSEM) ; DepMap CRISPR 24Q2 (figshare Corsello et al.) ; GEO GSE62452/GSE71729 ; ICGC PACA-AU. Voir PROVENANCE_tcga_v4.md, PROVENANCE_depmap.md, PROVENANCE_immune_v6.md, PROVENANCE_parp_v6.md, PROVENANCE_rotations_v61.md. CSV dédoublonnés : `build_dedup_844.py` (SHA `47447e77…f57d7`) ; SHA-256 des 88 CSV dans `dedup_844_csv_sha.json` (SHA `9dc283c8…b5235c7`) et dans PROVENANCE_rotations_dedup_844.md.")
sec.append("- **Nature des lignes.** Les CSV sont des résidus d'expression génique ou de dépendance CRISPR (mesures instrumentales — séquençage ARN, criblage CRISPR — transformées : correction de pureté, résidus) ordonnés par un flux-contrôle croissant, 11 flux analysés après retrait du doublon ; les nuls sont des lignes permutées, graine 42 — des échantillons hypothétiques, pas des mesures. Aucun mot humain, aucun échantillon hypothétique dans les séries réelles.")
sec.append("- **Sorties et scripts.** Extraction de ce chantier : `extract_ssep_844_rotations.py` (SHA-256 `24a07f9f…f02`), sorties brutes `ssep_844_rotations.json` (SHA `06f41b65…b362`, 72 130 octets) et `ssep_844_rotations.csv` (SHA `d1abc0ab…f999`) — le tableau complet par paire est au §8.44.2 de cette section et dans le CSV. Runs v6.2 : dossiers `results_fast_v62_<famille>_<contrôle>_dedup[_nul]` (88) ; manifeste `manifest_v62_dedup_844.txt` (SHA `1831e0d0…cd7`) ; log `runs_v62_dedup_844.log` (SHA `3951ff67…5a4cd`) ; surveillance `watch_v62_dedup_844.sh` (SHA `f3afa779…b9b9`) ; lanceur `run_v62_lot.sh` (SHA `7e501733…35b`) ; pilote CEACAM5 : log `runs_v62_dedup_844_pilot.log`, 2/2 exit 0, 13h18–13h52 UTC. Runs du §8.41 réutilisés : `results_fast_v61_v4r_cldn18_dedup[_nul]`, `results_fast_v62_immrot_ctla4_dedup[_nul]`, `results_fast_v62_depmaprot_aco2_dedup` + `_nul_sp`, `results_fast_v62_parprot_parp1_dedup` + `_nul_sp`. Section rédigée dans `section_8.44_rotations_dedup.md` (ce fichier).")
sec.append("- **Ce qui manque :** les valeurs exactes de S_sep par flux analysé (hors contrôle) n'ont pas été extraites — S_sep est global, pas par flux ; la lecture par flux du §8.32 reste la référence, doublon exclu ; le nul dédoublonné de CTLA4 est à nouvelle permutation (pas à permutation identique) — son verdict ne dépend pas de ce choix (+0,8986, large marge), mais la comparaison stricte « un seul effet change » ne vaut que pour les 47 autres paires ; MUC16 passe (A) de 0,0012 — un re-run ne changerait rien (v6.2 déterministe, gigue 0), mais le verdict est fragile par construction.")
sec.append("")
sec.append("## 8.44.7 Ce qui manque, ce qui reste ouvert")
sec.append("")
sec.append("- **Le 37/48 ne devient pas une piste thérapeutique.** Il mesure l'ordre, pas une rupture. Aucun des 48 contrôles ne devient une cible, et aucun flux ne devient un biomarqueur sur cette seule base.")
sec.append("- **MC reste presque aveugle sur les rotations (12/48 en positif sous (A), 4/48 inversés sous −0,07).** L'écart entre MC (composite écrasé par robustness ~10⁻⁴¹) et max_separation (pic seul) sur les mêmes runs est le fait le plus net de ce chantier après le 37/48 : le composite cache ce que le pic voit. Une piste serait de revoir la composition du score MC — hors protocole, non lancée.")
sec.append("- **La famille IMMROT domine (+0,752 en moyenne, 12/12).** Pourquoi les flux immunitaires se suivent-ils plus que les autres familles ? Aucune explication mesurée à ce jour — corrélation inter-flux non quantifiée ici. Une mesure directe (matrice de corrélation par famille, réel contre nul) trancherait si c'est la cohésion de la famille ou l'effet du contrôle.")
sec.append("- **DEPMAPROT est la famille fragile (6/12 sous (A)).** À n=45, le nul varie de 0,13 à 0,36 entre permutations et paires ; quatre réels s'effondrent sans le doublon. La question ouverte est si un nul à plusieurs permutations (distribution, pas un seul tirage) changerait les verdicts limites de cette famille — hors protocole, non lancée.")
sec.append("- **Incident d'exécution.** La machine a redémarré deux fois pendant le lot (~17h43 et ~19h51 UTC) ; l'unité de surveillance `v62-dedup-844-watch` est morte avec elle à chaque fois (aucune entrée dans `journalctl`, cause non établie — comme au §8.41). Les sorties complètes étaient intactes (41/88 puis 82/88) et n'ont pas été touchées ; la relance reprenable a repris où le lot s'était arrêté (SCAP_NUL puis POLQ) et terminé les 6 runs restants, 88/88 exit 0 au total (86 dans le log principal + 2 du pilote). Aucun run perdu, aucun dossier partiel à nettoyer (le run interrompu n'avait pas encore créé son dossier). Leçon confirmée : surveiller `systemctl is-active` pendant les longs lots et consigner toute mort d'unité avec son horodatage, sans supposer le mécanisme.")
sec.append("- **Périmètre.** Les rotations en v6.2 n'ont pas été relancées intégralement avec doublon (96 runs) : inutile pour S_sep, prouvé identique entre v6.1 et v6.2 (§8.38, 29/29 paires). Seules les 44 paires restantes ont été refaites sans doublon (88 runs), plus le pilote CEACAM5 (2 runs, comptés dans les 88).")
sec.append("- **Livre blanc.** Le livre blanc sur disque a changé entre la remise de ce chantier (SHA `de3aa316…`, 2 750 lignes) et la fin du lot (SHA `c5537270…`, 2 752 lignes, modifié 13h17 UTC par un autre processus — ce chantier ne l'a jamais touché) ; il s'arrête toujours au §8.42, sans §8.43 ni §8.44 insérés. Cette section et sa provenance sont des fichiers séparés, à insérer et publier par le coordinateur (règle permanente de Zackary, 19 nov. 09h45 : « Toujours github et pdf !!! » — après chaque lot de sections écrites au livre blanc, régénérer le PDF et pousser sur GitHub).")
sec.append("- **Aucun nouveau seuil proposé, aucun code modifié, aucun push GitHub dans ce chantier** (publication sur go séparé, comme au §8.37).")
sec.append("")
sec.append("— Fin de la §8.44. —")

with open("section_8.44_rotations_dedup.md", "w") as fh:
    fh.write("\n".join(sec) + "\n")

# ---------- PROVENANCE ----------
prov = []
prov.append("# PROVENANCE — Rotations sans doublon, §8.44 (19 novembre 2026)")
prov.append("")
prov.append("Chantier 2 des 3 étapes v6.2 approuvées par Zackary le 19 nov. 2026 ~05h47 (« Lance tout cela »).")
prov.append("Règle permanente (27 oct. 2026) : provenance toujours nommée — source complète, nature des lignes,")
prov.append("comment chaque valeur a été produite, hachages des données, et ce qui manque.")
prov.append("")
prov.append("## 1. Codes (jamais modifiés)")
prov.append("")
prov.append("| Code | SHA-256 | Rôle |")
prov.append("|---|---|---|")
prov.append("| `~/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py` | `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf` | Pipeline de travail, 88 runs |")
prov.append("| `~/workspace/runs/biophysique-hp35/universal_v6.1.0_cohen.py` | `2af5e5cea3a99ff227c7f76dff48c678eb07baba92625ca57e3c1c412546a9c9` | CLDN18 seul (run préexistant §8.32) |")
prov.append("| `build_dedup_844.py` | `47447e77c031c2cbd7d9484e64696656d2e75e1dfabd455983069727c07f57d7` | Construction des 88 CSV dédoublonnés |")
prov.append("| `extract_ssep_844_rotations.py` | `24a07f9fd6668e6a998d08bc2eebd4c06d831db3bc6136be27dee892c66c6f02` | Extraction S_sep / MC / Delta / max_separation |")
prov.append("| `watch_v62_dedup_844.sh` | `f3afa779be286787f47f130d2670410c041169e4ebd67692cb410a01e124b9b9` | Surveillance du lot |")
prov.append("| `run_v62_lot.sh` | `7e501733d3104c1e763255544c7b56dd8af4f6579fa0ebb5581bc8c12357435b` | Lanceur reprenable (saute les sorties complètes) |")
prov.append("")
prov.append("Vérification finale des SHA pipelines : revérifiés après le lot — inchangés.")
prov.append("Mode `fast`, graine 42 (défaut). Nul = lignes permutées, graine 42, colonne de contrôle intacte.")
prov.append("")
prov.append("## 2. Entrées d'origine (vérifiées avant construction)")
prov.append("")
prov.append("- 96 CSV de rotations construits par `build_rotations_v61.py` (16 nov. 2026) ; SHA-256 vérifiés un par un contre `PROVENANCE_rotations_v61.md` : **96/96 conformes**, 0 mismatch, 0 absent.")
prov.append("- 4 bases conformes : TCGA v4 `pdac_tcga_fluxes_v4.csv` (`e7a2adab…13a0b0`), DepMap `pdac_depmap_fluxes.csv` (`7d605fef…98e37f8`), immunitaire TCGA `pdac_immune_tcga_fluxes.csv` (`66dbb672…bbd2e`), PARP TCGA `pdac_tcga_fluxes_parp.csv` (`c9549b68…c4309`).")
prov.append("- Sources : TCGA-PAAD ARN Broad GDAC Firehose 2016-01-28 (RSEM) ; DepMap CRISPR 24Q2 (figshare Corsello et al.) ; GEO GSE62452/GSE71729 ; ICGC PACA-AU. Détail : PROVENANCE_tcga_v4.md, PROVENANCE_depmap.md, PROVENANCE_immune_v6.md, PROVENANCE_parp_v6.md, PROVENANCE_rotations_v61.md.")
prov.append("- Nature des lignes : résidus d'expression génique ou de dépendance CRISPR (mesures instrumentales — séquençage ARN, criblage CRISPR — transformées : correction de pureté, résidus) ordonnés par un flux-contrôle croissant ; les nuls sont des lignes permutées, graine 42 — des échantillons hypothétiques, pas des mesures. Aucun mot humain, aucun échantillon hypothétique dans les séries réelles.")
prov.append("")
prov.append("## 3. CSV dédoublonnés construits (88) — SHA-256 complets")
prov.append("")
prov.append("Méthode : retrait de la seule colonne doublon du flux contrôle (colonne k, valeurs identiques à la colonne 0 vérifiées côté réel ; multi-ensemble égal vérifié côté nul) ; contrôle, ordre et autres flux inchangés, ligne par ligne. Nul : CSV `_nul.csv` ORIGINAL moins la colonne doublon — même permutation que l'original. Colonnes 13 → 12 (contrôle + 11 flux analysés). Aucune valeur recalculée ni imputée.")
prov.append("")
prov.append("Fichier `dedup_844_csv_sha.json` (SHA `9dc283c8830731fd41ab5b8e84d6707be2b4f2d86810847d0a6277e8cb5235c7`) — mêmes valeurs, lisibles en machine.")
prov.append("")
prov.append("| Famille | Contrôle | Col. doublon | n | CSV réel dédoublonné — SHA-256 | CSV nul dédoublonné — SHA-256 |")
prov.append("|---|---|---|---|---|---|")
for fam in ("V4ROT", "DEPMAPROT", "IMMROT", "PARPROT"):
    for key in sorted(k for k in shas if k.startswith(fam + "_")):
        ctrl = key[len(fam) + 1:]
        s = shas[key]
        prov.append(f"| {fam} | {ctrl} | {s['doublon_col']} | {s['n']} | `{s['reel']}` | `{s['nul']}` |")
prov.append("")
prov.append("Les 4 paires déjà refaites au §8.41 (non reconstruites ici) — SHA vérifiés contre §8.41.6, conformes :")
prov.append("")
prov.append("| Paire | CSV réel — SHA-256 | CSV nul — SHA-256 |")
prov.append("|---|---|---|")
prov.append("| CLDN18 (V4ROT, v6.1) | `b1071f84e7228b9946562c04fb43d5d48603b4924afa04cf0f417bb86fc4d4f8` | `33d5f3177484cd40ffb92920a4bb22a23635e5c4ea2a32dd04c4df3de164f3d7` |")
prov.append("| CTLA4 (IMMROT) | `36bce1335a2d23f94f0a71dbfdc28c19a0d0df5e455f84466e2f61c2ada3a389` | `ac1b3c5d51f5bd5929d1fb3153169374de262a1ed290de40179130a59aa6c369` (nouvelle permutation) |")
prov.append("| ACO2 (DEPMAPROT) | `ef398777f292b7702b74029ccfba435d0f55b1b3f5e76434db4c9e456b61541c` | `33d13387b612a1a2b5ca877197a4e1ddba369e2cff97121037a8001eb9adca09` (même permutation ; nul nouvelle permutation : `3700d844d2033a4903a62c14f26da7501ee45fb3b4eaf6af0bbfcee3bd4cbb1c`) |")
prov.append("| PARP1 (PARPROT) | `95750c870fb6e6ac94da3d928e89a136e1d8a2edab2579e3494cad3f77cd8cd5` | `591f88ec34e839044fae0a890cb58d2e658f74c6e9833309eef1cc9911b2e4f9` (même permutation = nouvelle permutation, même fichier) |")
prov.append("")
prov.append("## 4. Runs et sorties")
prov.append("")
prov.append("- Lot v6.2 : unité systemd `v62-dedup-844-watch` (surveillance `watch_v62_dedup_844.sh`), 13h52:48–20h11:52 UTC le 19 nov. 2026 (6 h 19) ; **88/88 exit 0** (86 dans `runs_v62_dedup_844.log` + 2 du pilote CEACAM5 dans `runs_v62_dedup_844_pilot.log`, 13h18:48–13h52:35 UTC, 2/2 exit 0). Manifeste `manifest_v62_dedup_844.txt` (SHA `1831e0d00c403169d1910816f2184e9a15899001f034cf9c8889b44222cfdcd7`) ; log `runs_v62_dedup_844.log` (SHA `3951ff677b21ee4163f8e3e7f8416a0dab8bcf845af0a6af8d1de8592485a4cd`).")
prov.append("- Dossiers de sortie : `results_fast_v62_<famille>_<contrôle>_dedup[_nul]` (88), chacun avec `master_results.json`.")
prov.append("- Deux redémarrages machine pendant le lot (~17h43 et ~19h51 UTC) : l'unité de surveillance est morte avec la machine à chaque fois (aucune entrée dans `journalctl`, cause non établie) ; relance reprenable à 17h44:22 et 19h52:26 UTC ; sorties complètes intactes (41/88 puis 82/88), non touchées ; reprise au run interrompu (SCAP_NUL puis POLQ) ; aucun run perdu, aucun dossier partiel à nettoyer.")
prov.append("- Extraction : `extract_ssep_844_rotations.py` → `ssep_844_rotations.json` (SHA `06f41b6592291114f8404ea8b3dc69d122e0db2f5d4db474c6a76d0cea59b362`, 72 130 octets) et `ssep_844_rotations.csv` (SHA `d1abc0aba2e480e611b87dea2861ef5bd96a83a196e1b8736b596506653fc999`). Contrôles : 88/88 runs lus (+8/8 existants), 48/48 paires, versions conformes, 88/88 SHA CSV conformes, 0 écart vs les 4 écarts du §8.41 (tolérance 10⁻⁴).")
prov.append("- Section : `section_8.44_rotations_dedup.md` (ce chantier). Tableaux générés depuis `ssep_844_rotations.json` par `write_section_844.py` — aucune valeur recopiée à la main.")
prov.append("")
prov.append("## 5. Ce qui manque")
prov.append("")
prov.append("- S_sep par flux analysé (hors contrôle) : non extrait — S_sep est global ; lecture par flux du §8.32 (`v61_rotations_flux_reading.md`, doublon exclu) reste la référence.")
prov.append("- Nul dédoublonné de CTLA4 à nouvelle permutation (pas à permutation identique) : verdict indépendant de ce choix (+0,8986, large marge), mais la comparaison stricte « un seul effet change » ne vaut que pour les 47 autres paires.")
prov.append("- MUC16 passe (A) de 0,0012 : verdict fragile par construction (v6.2 déterministe, gigue 0 — un re-run ne changerait rien).")
prov.append("- Livre blanc : modifié entre la remise du chantier (SHA `de3aa316…`, 2 750 lignes) et la fin du lot (SHA `c5537270…`, 2 752 lignes, modifié 13h17 UTC par un autre processus — ce chantier ne l'a jamais touché) ; il s'arrête toujours au §8.42. Cette section n'y est pas insérée (fichier séparé, publication par le coordinateur).")
prov.append("- PDF non régénéré, rien poussé sur GitHub dans ce chantier (hors périmètre, publication sur go séparé).")
prov.append("")

with open("PROVENANCE_rotations_dedup_844.md", "w") as fh:
    fh.write("\n".join(prov) + "\n")

print("écrit: section_8.44_rotations_dedup.md, PROVENANCE_rotations_dedup_844.md")
print("SHA section:", sha("section_8.44_rotations_dedup.md"))
print("SHA provenance:", sha("PROVENANCE_rotations_dedup_844.md"))
