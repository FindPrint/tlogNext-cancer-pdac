#!/usr/bin/env python3
"""Convertit le livre blanc Markdown en HTML imprimable (source du PDF).
Fidelite : le corps est la conversion directe du Markdown source,
aucun texte ajoute ni retire dans le corps. Seuls la couverture et
les mentions de bas de page sont composes ici, a partir des faits
de l'en-tete du document source."""
import markdown, pathlib, html

SRC = pathlib.Path.home() / "workspace/goals/pdac-pseudo-time-validation-tlog28-cancer-project/files/livre-blanc-pdac-v6.md"
OUT = pathlib.Path(__file__).parent / "index.html"

text = SRC.read_text(encoding="utf-8")
lines = text.splitlines()
# Le corps commence a la section 1 ; l'en-tete va sur la couverture.
start = next(i for i, l in enumerate(lines) if l.startswith("## 1."))
body_lines = lines[start:]
# Un tableau colle a un paragraphe n'est pas reconnu par le convertisseur :
# inserer une ligne vide avant tout bloc de tableau colle (cas du paysage
# de survie, section 8.12, dans le document source).
fixed = []
for i, l in enumerate(body_lines):
    if l.startswith("|") and fixed and fixed[-1].strip() and not fixed[-1].startswith("|"):
        fixed.append("")
    fixed.append(l)
body_md = "\n".join(fixed)
body_html = markdown.markdown(body_md, extensions=["tables", "sane_lists"])

CSS = """
@page { size: A4; margin: 13mm 0 13mm 0;
  @bottom-center { content: "Livre blanc PDAC v6 - page " counter(page);
    font-family: 'Liberation Sans', sans-serif; font-size: 8pt; color: #666; } }
* { box-sizing: border-box; print-color-adjust: exact; -webkit-print-color-adjust: exact; }
body { margin: 0; font-family: 'Liberation Serif', 'Noto Serif', serif;
  font-size: 10.5pt; line-height: 1.45; color: #1a1a1a; }
.page { min-height: 271mm; padding: 0.6cm 1.9cm; }
.content { padding: 0 1.9cm; }
.cover .kicker { font-family: 'Liberation Sans', sans-serif; font-size: 10pt;
  letter-spacing: 2px; text-transform: uppercase; color: #7a4a12; margin-top: 2.2cm; }
.cover h1 { font-family: 'Liberation Sans', sans-serif; font-size: 27pt; line-height: 1.2;
  margin: 0.5cm 0 0.4cm 0; color: #14213d; }
.cover .sub { font-size: 13pt; color: #444; margin-bottom: 1cm; }
.cover table.meta { width: 100%; border-collapse: collapse; font-size: 10pt;
  font-family: 'Liberation Sans', sans-serif; margin-bottom: 0.9cm; }
.cover table.meta td { border-top: 1px solid #ccc; padding: 5px 6px; vertical-align: top; }
.cover table.meta td.k { width: 26%; font-weight: bold; color: #14213d; }
.result { border: 1.5px solid #14213d; padding: 0.45cm 0.55cm; margin-bottom: 0.8cm; }
.result h2 { font-family: 'Liberation Sans', sans-serif; font-size: 12.5pt; margin: 0 0 6px 0; color: #14213d; }
.result p { margin: 0 0 6px 0; font-size: 10.5pt; }
.cover .note { font-size: 9.5pt; color: #555; }
h2 { font-family: 'Liberation Sans', sans-serif; font-size: 15pt; color: #14213d;
  border-bottom: 2px solid #14213d; padding-bottom: 4px; margin: 26px 0 10px 0;
  break-after: avoid; }
h3 { font-family: 'Liberation Sans', sans-serif; font-size: 12pt; color: #24365e;
  margin: 18px 0 7px 0; break-after: avoid; }
p { margin: 0 0 8px 0; text-align: justify; }
ul, ol { margin: 4px 0 10px 0; }
li { margin-bottom: 3px; text-align: justify; }
table { border-collapse: collapse; width: 100%; margin: 10px 0 14px 0;
  font-family: 'Liberation Sans', sans-serif; font-size: 8.2pt; line-height: 1.3; }
th { background: #e9edf3; border: 0.6pt solid #9aa5b5; padding: 4px 5px; text-align: left; }
td { border: 0.6pt solid #b9c1cd; padding: 4px 5px; vertical-align: top; }
tr { break-inside: avoid; }
code { font-family: 'Liberation Mono', monospace; font-size: 8.6pt; background: #f0f0f0; padding: 0 2px; }
hr { border: none; border-top: 1px solid #bbb; margin: 16px 0; }
em { color: inherit; }
strong { color: inherit; }
pre { font-family: 'Liberation Mono', monospace; font-size: 7pt; line-height: 1.25;
  background: #f7f7f7; border: 0.6pt solid #ccc; padding: 6px 8px; white-space: pre-wrap;
  word-wrap: break-word; margin: 8px 0 14px 0; }
.codehead { font-family: 'Liberation Sans', sans-serif; font-size: 8.5pt; color: #14213d;
  background: #e9edf3; border: 0.6pt solid #9aa5b5; padding: 4px 6px; margin: 14px 0 0 0; }
figure { margin: 12px 0 16px 0; break-inside: avoid; text-align: center; }
figure img { max-width: 100%; }
figcaption { font-family: 'Liberation Sans', sans-serif; font-size: 8.5pt; color: #333;
  text-align: left; margin-top: 4px; }
.small { font-size: 8.5pt; color: #444; }
a { color: #14213d; }
"""

COVER = """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Livre blanc PDAC v6 — UNIVERSAL_LOG</title>
<style>__CSS__</style></head><body>
<div class="page cover">
<div class="kicker">Livre blanc — document vivant — 16 novembre 2026</div>
<h1>PDAC : chercher des pistes thérapeutiques avec UNIVERSAL_LOG v6</h1>
<div class="sub">Cancer du pancréas — ARN, protéine, CRISPR et autres flux —
pipeline UNIVERSAL_LOG v6.0.0 (Cohen-d). Tout ce qui a été fait, testé,
pensé, analysé — ce qui est connu et ce qui ne l'est pas.</div>
<table class="meta">
<tr><td class="k">Mandat</td><td>Zackary Drasse-Ménard, 15 novembre 2026 :
« Trouver un remède pour le cancer du pancréas en utilisant ARN, protéine
et CRISPR et autre flux/data information et avec mon pipeline. Maintenir un
livre blanc de tout ce que tu fais tester penser analyse connais connais pas. »
Ordre du 16 novembre 2026 : « Continue jusqu'à ce que tu trouve un remède. »</td></tr>
<tr><td class="k">Pipeline</td><td>UNIVERSAL_LOG v6.0.0 (universal_v6.0.0_cohen.py,
SHA bb8bbdba…c0773) — Cohen-d partout, Cliff retiré, preuve HP35 du
14 novembre 2026 (4/4 cascades identiques, environ 11x plus rapide).
Original v5.9.0f intact.</td></tr>
<tr><td class="k">Règle de provenance</td><td>Chaque donnée, chaque résultat,
chaque affirmation porte sa source complète, la nature des lignes, comment
chaque valeur a été produite, les hachages, et ce qui manque. Chaque source
citée porte son lien complet (annexe « Registre des sources »).</td></tr>
<tr><td class="k">Contenu de ce PDF</td><td>Texte intégral du livre blanc (§1–§10,
§8.1–§8.28, §7, journal) + annexes complètes : reproduction, provenances
intégrales, tables de résultats complètes, code intégral (pipeline v6 +
scripts), figures, registre des sources avec liens, éthique et
reproductibilité. Les matrices brutes (~2 Go) ne peuvent pas tenir dans
un PDF : elles se re-téléchargent vérifiées (URL + MD5/SHA) via le script
du dépôt GitHub — voir l'annexe « Reproduction ».</td></tr>
<tr><td class="k">Dépôts GitHub (privés)</td><td>github.com/FindPrint/pancreatic-cancer-open-data-reproducibility
(travail PDAC v6 : livre blanc, scripts, provenances, résultats,
script de téléchargement) et github.com/FindPrint/Code (pipeline v6).
Le pipeline reste privé ; rien n'est rendu public.</td></tr>
</table>
<div class="result">
<h2>Le résultat qui tient — état au 16 novembre 2026</h2>
<p>Le groupe de patients au KRAS le plus fort a les marqueurs CA125 (MUC16)
et CEA (CEACAM5) élevés : CA125 +0,64 / +0,67 / +0,48 / +0,13 écarts-types
et CEA +0,43 / +0,38 / +0,63 / +0,28 dans TCGA (178 tumeurs), GSE71729
(145), GSE62452 (69) et ICGC (70) — expression confirmée 3 cohortes sur 4.
CA125 prédit une survie plus courte dans 2 cohortes sur 3 (TCGA : Cox 1,44
univarié ; ICGC : quartile 9,5 contre 23,8 mois, p = 0,002, Cox 1,57).
Sans aucun seuil, KRAS et CA125 prédisent chacun une survie plus courte
(Cox continu TCGA, 177 patients : HR 1,42 et 1,44 univariés).</p>
<p>L'effondrement des marqueurs de différenciation (PGC, DPCR1, CLDN18)
observé en TCGA ne tient que dans TCGA : il dépend de la correction de
pureté et s'inverse dans les autres cohortes. Les tests CRISPR (DepMap,
balayage génome entier : 2 hits faibles non druggables) et les trois
criblages de médicaments (PRISM primaire, PRISM secondaire, GDSC2) sont
négatifs. La chaîne ne se confirme pas en protéine (CPTAC).</p>
<p><strong>Avance clinique réelle, trouvée hors pipeline :</strong> le
daraxonrasib (pan-RAS, approuvé par la FDA le 26 août 2026) double la
survie médiane en phase III (13,2 contre 6,7 mois, HR 0,40).
<strong>Piste la plus solide du projet :</strong> vopimetostat + daraxonrasib,
82 % de réponses (18/22) chez les patients MTAP-délétés prétraités
(phase 1/2, non randomisée ; phase 3 prévue 1<sup>er</sup> semestre 2027),
avec un appui mesuré (dépendance PRMT5 plus forte en pancréas, p = 0,0036).
<strong>Seule piste ouverte :</strong> ATR seul (hypothèse d'expression,
sans appui CRISPR ni médicament). <strong>Ce n'est pas un remède démontré.</strong></p>
<p><strong>Note de lecture — §9 :</strong> le tableau des pistes (§9) reflète
l'état du 15 novembre, tel qu'écrit dans le livre blanc source. Les
résultats du 16 novembre sont aux §8.20–§8.28 et au journal (§10).</p>
</div>
<p class="note">Lecture honnête, exigée par le mandat : ce document ne présente
jamais une piste comme un remède, ni un seuil comme une preuve clinique.
Un résultat négatif est un résultat, il est noté comme tel. Le pipeline
lui-même reste privé (règle permanente) ; le travail PDAC est public.</p>
</div>
<div class="content">
"""

APPENDIX = pathlib.Path(__file__).parent / "appendix.html"
appendix_html = ""
if APPENDIX.exists():
    appendix_html = APPENDIX.read_text(encoding="utf-8")
    print("annexe incluse:", APPENDIX, len(appendix_html), "caracteres")
else:
    print("annexe absente: aucune annexe ajoutee")

doc = COVER.replace("__CSS__", CSS) + body_html + appendix_html + "\n</div></body></html>\n"
OUT.write_text(doc, encoding="utf-8")
print("index.html ecrit:", len(doc), "caracteres")
