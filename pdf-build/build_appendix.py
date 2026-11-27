#!/usr/bin/env python3
"""Genere appendix.html : annexes completes du PDF PDAC v6.
Lit les fichiers de ~/workspace/runs/pdac-v6/ et du pipeline v6, ne modifie
aucune source, ecrit appendix.html dans le dossier .src/ du livre blanc.
Usage : python3 build_appendix.py  (avec le module markdown disponible)
Contenu : A Reproduction, B Provenances integrales, C Tables completes,
D Code integral, E Figures, F Ethique et reproductibilite,
G Registre des sources (source_registry.md si present)."""
import csv
import hashlib
import html
import pathlib
import re

import markdown

HOME = pathlib.Path.home()
RUNS = HOME / "workspace/runs/pdac-v6"
HP35 = HOME / "workspace/runs/biophysique-hp35"
SRC = pathlib.Path(__file__).parent
OUT = SRC / "appendix.html"
REGISTRY = RUNS / "source_registry.md"
V6 = HP35 / "universal_v6.0.0_cohen.py"
BUILD_V6 = HP35 / "build_v6.py"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def size_str(n):
    for unit in ("o", "Ko", "Mo", "Go"):
        if n < 1024 or unit == "Go":
            return f"{n:,.0f} {unit}".replace(",", " ")
        n /= 1024.0
    return f"{n:.1f} Go"


def md_html(text):
    return markdown.markdown(text, extensions=["tables", "sane_lists"])


def fmt_num(x):
    """Formate un nombre pour les tables : 4 decimales, notation
    scientifique sous 1e-4, tel quel sinon."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return html.escape(str(x))
    if v == 0:
        return "0"
    if abs(v) < 0.0001 or abs(v) >= 100000:
        return f"{v:.2e}"
    return f"{v:.4f}"


def is_num(s):
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        return False


def csv_table(path, caption, note="", limit=None, sort_key=None, reverse=False,
              filter_fn=None, round_cols=True):
    """Rend un CSV en table HTML. Retourne (html, n_total, n_shown)."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    total = len(rows)
    if filter_fn is not None:
        rows = [r for r in rows if filter_fn(r)]
    if sort_key is not None:
        rows = sorted(rows, key=sort_key, reverse=reverse)
    shown = rows if limit is None else rows[:limit]
    if not shown:
        return "", total, 0
    cols = list(shown[0].keys())
    parts = [f"<p class=\"small\">{html.escape(caption)} "
             f"Fichier : <code>{html.escape(path.name)}</code> — "
             f"SHA-256 <code>{sha256(path)[:16]}…</code> — "
             f"{total} lignes au total, {len(shown)} affichees.</p>"]
    if note:
        parts.append(f"<p class=\"small\">{html.escape(note)}</p>")
    parts.append("<table><thead><tr>")
    for c in cols:
        parts.append(f"<th>{html.escape(c)}</th>")
    parts.append("</tr></thead><tbody>")
    for r in shown:
        parts.append("<tr>")
        for c in cols:
            v = r.get(c, "")
            if round_cols and is_num(str(v).strip()):
                parts.append(f"<td>{fmt_num(v)}</td>")
            else:
                parts.append(f"<td>{html.escape(str(v))}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table>")
    if limit is not None and total > limit:
        parts.append(f"<p class=\"small\">Table tronquee a {limit} lignes sur "
                     f"{total}. L'integralite est dans le fichier CSV du depot "
                     f"GitHub (voir annexe A).</p>")
    return "\n".join(parts), total, len(shown)


def pre_file(path, label):
    """Contenu integral d'un fichier en <pre>, avec en-tete SHA/lignes."""
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return (f"<p class=\"codehead\">{html.escape(label)} — "
                f"{html.escape(path.name)} — {len(data)} octets — "
                f"NON INCLUS : fichier non UTF-8 (binaire).</p>")
    nlines = text.count("\n") + (0 if text.endswith("\n") else 1)
    head = (f"<p class=\"codehead\">{html.escape(label)} — "
            f"<code>{html.escape(path.name)}</code> — "
            f"SHA-256 <code>{sha256(path)}</code> — "
            f"{len(data)} octets — {nlines} lignes.</p>")
    return head + "<pre>" + html.escape(text) + "</pre>"


def file_row(path, label, url, script, flux):
    """Ligne du tableau des jeux de donnees, hachages recalcules en direct."""
    if path is not None and path.exists():
        sz = path.stat().st_size
        return (f"<tr><td>{html.escape(label)}</td>"
                f"<td><a href=\"{html.escape(url)}\">{html.escape(url)}</a></td>"
                f"<td>{size_str(sz)} ({sz} octets)</td>"
                f"<td>MD5 <code>{md5(path)}</code><br>SHA-256 "
                f"<code>{sha256(path)}</code></td>"
                f"<td>{html.escape(script)}</td><td>{html.escape(flux)}</td></tr>")
    return (f"<tr><td>{html.escape(label)}</td>"
            f"<td><a href=\"{html.escape(url)}\">{html.escape(url)}</a></td>"
            f"<td>Fichier non present localement au moment de la construction "
            f"du PDF — voir la provenance integrale (annexe B).</td>"
            f"<td>—</td><td>{html.escape(script)}</td>"
            f"<td>{html.escape(flux)}</td></tr>")


# ---------------------------------------------------------------- annexe A
def annexe_a():
    rows = []
    rows.append(file_row(
        RUNS / "data/CRISPRGeneEffect.csv",
        "DepMap Public 24Q4 — CRISPRGeneEffect (scores Chronos, 17 916 genes x 2 105 modeles)",
        "https://doi.org/10.25452/figshare.plus.27993248.v1",
        "build_fluxes_depmap.py ; crispr_genome_scan.py",
        "pdac_depmap_fluxes.csv (45 adeno)"))
    rows.append(file_row(
        RUNS / "data/Model.csv",
        "DepMap Public 24Q4 — Model.csv (annotation des modeles)",
        "https://doi.org/10.25452/figshare.plus.27993248.v1",
        "build_fluxes_depmap.py",
        "pdac_depmap_fluxes.csv"))
    rows.append(file_row(
        RUNS / "data/OmicsCNGene.csv",
        "DepMap Public 24Q4 — OmicsCNGene (nombre de copies relatif, lineaire, 1 929 modeles)",
        "https://doi.org/10.25452/figshare.plus.27993248.v1",
        "prmt5_mtap_dependency.py",
        "data/prmt5_mtap_results.csv"))
    rows.append(file_row(
        RUNS / "data/tcga_paad_rsem.tar.gz",
        "TCGA-PAAD — Broad GDAC Firehose stddata 2016-01-28, matrice RSEM genes normalises (20 532 genes x 183 echantillons)",
        "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/PAAD/20160128/",
        "build_fluxes_tcga.py, _v2.py, _v3.py, _v4.py",
        "pdac_tcga_fluxes*.csv (178 tumeurs primaires)"))
    rows.append(file_row(
        RUNS / "data/tcga_paad_gistic.tar.gz",
        "TCGA-PAAD — Broad GDAC Firehose 2016-01-28, appels GISTIC (deletions MTAP/CDKN2A)",
        "https://gdac.broadinstitute.org/runs/analyses__2016_01_28/data/PAAD/20160128/",
        "mtap_kras_tests.py",
        "mtap_gistic_status.csv"))
    rows.append(file_row(
        RUNS / "data/tcga_luad_rsem.tar.gz",
        "TCGA-LUAD — Broad GDAC Firehose stddata 2016-01-28, matrice RSEM (515 tumeurs)",
        "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/LUAD/20160128/",
        "build_fluxes_pancancer.py",
        "pdac_luad_fluxes.csv"))
    rows.append(file_row(
        RUNS / "data/tcga_coad_rsem.tar.gz",
        "TCGA-COAD — Broad GDAC Firehose stddata 2016-01-28, matrice RSEM (285 tumeurs)",
        "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/COAD/20160128/",
        "build_fluxes_pancancer.py",
        "pdac_coad_fluxes.csv"))
    rows.append(file_row(
        RUNS / "data/GSE71729_series_matrix.txt.gz",
        "GEO GSE71729 — Moffitt et al. 2015, 145 tumeurs primaires, puce Agilent GPL20769",
        "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE71nnn/GSE71729/matrix/GSE71729_series_matrix.txt.gz",
        "build_fluxes_geo71729.py ; survival_geo71729.py",
        "pdac_geo71729_fluxes*.csv"))
    rows.append(file_row(
        RUNS / "data/GSE62452_series_matrix.txt.gz",
        "GEO GSE62452 — 69 tumeurs PDAC, puce Affymetrix HuGene-1.0-st GPL6244",
        "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62452/matrix/GSE62452_series_matrix.txt.gz",
        "build_fluxes_geo62452.py",
        "pdac_geo62452_fluxes*.csv"))
    rows.append(file_row(
        RUNS / "data/icgc_pacaau_exp.txt.gz",
        "ICGC PACA-AU — expression Bailey et al. Nature 2016, 70 tumeurs, via UCSC Xena (le portail ICGC DCC est mort : https://dcc.icgc.org/ redirige vers l'accueil)",
        "https://icgc-xena-hub.s3.amazonaws.com/download/PACA-AU/nature16965-s2_normalised_exp.txt.gz",
        "build_fluxes_icgc.py ; survival_icgc.py",
        "pdac_icgc_fluxes.csv"))
    rows.append(file_row(
        RUNS / "data/bailey2016_suppl_tables1-13.xlsx",
        "ICGC PACA-AU — tables supplementaires Bailey et al. Nature 2016 (survie : 70 tumeurs, 47 deces OS)",
        "https://static-content.springer.com/esm/art%3A10.1038%2Fnature16965/MediaObjects/41586_2016_BFnature16965_MOESM270_ESM.xlsx",
        "survival_icgc.py",
        "icgc_clinical_70.csv"))
    rows.append(file_row(
        RUNS / "data/cptac/pdac_umich_protein_gene_matrix.csv",
        "CPTAC PDC000393 (Cao et al. Cell 2021) — proteomique UMich, 68 tumeurs (63 retenues)",
        "https://zenodo.org/records/8394329",
        "build_fluxes_cptac.py ; build_matrix_umich.py",
        "pdac_cptac_fluxes.csv"))
    rows.append(file_row(
        RUNS / "data/cptac/bcm-pdac-proteomics-PDAC_proteomics_gene_abundance_log2_reference_intensity_normalized_Tumor.txt.gz",
        "CPTAC PDC000393 (Cao et al. Cell 2021) — proteomique BCM, 52 tumeurs",
        "https://zenodo.org/records/8394329",
        "build_fluxes_cptac_bcm.py",
        "pdac_cptac_bcm_fluxes.csv"))
    rows.append(file_row(
        RUNS / "data/Repurposing_Public_24Q2_Extended_Primary_Data_Matrix.csv",
        "PRISM Repurposing Public 24Q2 — criblage primaire, 6 790 composes, dose unique 2,5 uM",
        "https://doi.org/10.6084/m9.figshare.25917643",
        "prism_screen.py",
        "data/prism_kras_screen_named.csv"))
    rows.append(file_row(
        RUNS / "data/secondary-screen-dose-response-curve-parameters.csv",
        "PRISM secondaire (19Q4, Corsello et al. Nat Cancer 2020) — dose-reponse, 1 427 composes testables",
        "https://doi.org/10.6084/m9.figshare.9393293.v4",
        "prism_secondary_screen.py",
        "data/prism_secondary_kras_screen.csv"))
    rows.append(file_row(
        RUNS / "data/GDSC2_fitted_dose_response_27Oct23.xlsx",
        "GDSC2 — dose-reponse ajustee (27 oct. 2023), via Cell Model Passports",
        "https://cmp.cog.sanger.ac.uk/download/GDSC2_fitted_dose_response_27Oct23.xlsx",
        "gdsc_kras_screen.py",
        "data/gdsc_kras_screen.csv"))
    rows.append(file_row(
        RUNS / "data/OmicsSomaticMutationsMAFProfile.maf",
        "DepMap 24Q4 — mutations somatiques MAF (alleles KRAS des lignees pancras : G12D 23, G12V 20, G12R 5, Q61H 2, Q61R 1, G12C 1, G12A 1, G12I 1)",
        "https://doi.org/10.25452/figshare.plus.27993248.v1",
        "mrtx1133_prism_allele.py",
        "data/kras_alleles_pancreas.csv"))
    rows.append(file_row(
        RUNS / "data/panc1_ncata/panc1_sha256.txt",
        "PANC-1 (NCATS, Pourmousa et al. Nat Commun 2025) — 8 fichiers CSV sources, 496 combinaisons mesurees (SHA de chaque fichier dans panc1_sha256.txt ; le fichier mit_test.csv, predictions de modele, est exclu)",
        "https://github.com/ncats/PANC1",
        "analyze_panc1_combos.py",
        "data/panc1_combinations_summary.csv"))
    return ("<h2>Annexe A — Reproduction : donnees, code, commandes</h2>"
            "<p>Cette annexe donne tout ce qu'il faut pour reproduire le "
            "travail a partir de zero : chaque jeu de donnees avec sa source "
            "exacte, sa taille et ses hachages <strong>recalcules au moment "
            "de la construction de ce PDF</strong> (ils doivent correspondre "
            "a ceux des provenances de l'annexe B ; tout ecart serait une "
            "erreur a signaler) ; chaque script avec son role ; la commande "
            "exacte du pipeline v6 ; les depots GitHub.</p>"
            "<h3>A.1 Jeux de donnees — source, taille, hachages</h3>"
            "<p class=\"small\">Nature des lignes et methode de production "
            "de chaque valeur : voir la provenance integrale correspondante "
            "(annexe B) et le registre des sources (annexe G). Toutes les "
            "donnees sont publiques et gratuites ; aucune donnee privee, "
            "aucune donnee payante.</p>"
            "<table><thead><tr><th>Jeu de donnees</th><th>URL exacte</th>"
            "<th>Taille</th><th>MD5 / SHA-256</th><th>Script</th>"
            "<th>Fichier produit</th></tr></thead><tbody>"
            + "\n".join(rows) + "</tbody></table>"
            "<h3>A.2 Commande exacte du pipeline v6 (mode fast)</h3>"
            "<pre>python3 universal_v6.0.0_cohen.py "
            "--input pdac_tcga_fluxes_v4.csv --output results_fast_tcga_v4 "
            "--mode fast --control_col step --target_col PGC\n"
            "# Variante nul (lignes permutees, graine 42) : meme commande avec\n"
            "# --input pdac_tcga_fluxes_v4_nul.csv --output results_fast_tcga_v4_nul\n"
            "# Mode fast = cohen_d, 12 iterations Monte Carlo, ~4 minutes sur\n"
            "# cette machine (2 vCPU, 7,7 Go RAM). Minimum : 50 points par serie\n"
            "# (min_len 50, w_size 80). Le pipeline ne voit jamais la\n"
            "# temperature ni la verite terrain : l'ordre des lignes est la\n"
            "# seule information d'ordonnancement ; toute traduction en\n"
            "# temperature ou comparaison a une valeur critique se fait\n"
            "# APRES le run, dans le harnais, sans retour dans les parametres.</pre>"
            "<h3>A.3 Depots GitHub (prives)</h3>"
            "<ul><li>Travail PDAC v6 (livre blanc, scripts, provenances, "
            "resultats, script de telechargement) : "
            "<a href=\"https://github.com/FindPrint/pancreatic-cancer-open-data-reproducibility\">"
            "https://github.com/FindPrint/pancreatic-cancer-open-data-reproducibility</a></li>"
            "<li>Pipeline v6 (code integral + preuve Cohen) : "
            "<a href=\"https://github.com/FindPrint/Code\">"
            "https://github.com/FindPrint/Code</a></li></ul>"
            "<p class=\"small\">Le PDF lui-meme (binaire) ne peut pas etre "
            "pousse dans l'arbre snapshot GitHub (fichiers UTF-8 uniquement, "
            "16 Mo maximum). Il est partageable depuis l'espace de travail ; "
            "sa source Markdown et les scripts de construction sont dans le "
            "depot PDAC.</p>")

# ---------------------------------------------------------------- annexe B
def annexe_b():
    provs = sorted(RUNS.glob("PROVENANCE_*.md"))
    parts = ["<h2>Annexe B — Provenances integrales</h2>"
             "<p>Texte integral de chaque fichier de provenance du projet, "
             "sans resume ni coupure. Chaque fichier est reproduit tel quel, "
             "avec son nom. Les provenances sont la reference : en cas de "
             "desaccord entre cette annexe et un resume ailleurs dans ce PDF, "
             "c'est la provenance qui fait foi.</p>"]
    for p in provs:
        parts.append(f"<h3>{html.escape(p.name)}</h3>")
        parts.append(md_html(p.read_text(encoding="utf-8")))
    return "\n".join(parts)


# ---------------------------------------------------------------- annexe C
def annexe_c():
    parts = ["<h2>Annexe C — Tables de resultats completes</h2>"
             "<p>Toutes les tables qui portent un verdict, dans leur "
             "integralite quand la taille le permet. Les nombres sont "
             "arrondis a 4 decimales (notation scientifique sous 1e-4) ; "
             "les valeurs exactes sont dans les fichiers CSV du depot "
             "GitHub. Les tables trop longues pour un PDF (PRISM primaire : "
             "6 790 composes ; balayage CRISPR : 17 916 genes) sont donnees "
             "en integralite pour les lignes significatives, avec les "
             "effectifs totaux et le fichier complet cite.</p>"]
    # C.1 immune
    t, _, _ = csv_table(
        RUNS / "immune_direct_tests.csv",
        "Tests directs immunitaires le long de l'axe KRAS (4 cohortes, 12 genes).",
        "Verdict : la tumeur devient froide quand KRAS monte ; KRAS + anti-PD-(L)1 NON.")
    parts.append("<h3>C.1 Paysage immunitaire — tests directs (48 lignes)</h3>" + t)
    # C.2 parp
    t, _, _ = csv_table(
        RUNS / "parp_direct_tests.csv",
        "Tests directs reparation/PARP, TCGA (178).",
        "Verdict : BRCA2/ATR/RAD51 montent, PARP1/PARP2 plats ; KRAS + PARP NON.")
    parts.append("<h3>C.2 Paysage reparation / PARP — TCGA</h3>" + t)
    t, _, _ = csv_table(
        RUNS / "parp_direct_tests_geo71729.csv",
        "Tests directs reparation/PARP, controle GEO GSE71729 (145).")
    parts.append("<h3>C.3 Paysage reparation / PARP — controle GEO GSE71729</h3>" + t)
    # C.4 atr
    t, _, _ = csv_table(
        RUNS / "atr_chek1_direct_tests_tcga.csv",
        "Re-test ATR/CHEK1, TCGA : brut, corrige purete, corrige proliferation, Spearman partiel.",
        "Verdict : seul ATR survit au controle proliferation ; CHEK1/RAD51/POLQ morts.")
    parts.append("<h3>C.4 Re-test ATR/CHEK1 — TCGA</h3>" + t)
    t, _, _ = csv_table(
        RUNS / "atr_chek1_direct_tests_cohorts.csv",
        "Re-test ATR/CHEK1, controles ICGC (70) et GSE62452 (69).")
    parts.append("<h3>C.5 Re-test ATR/CHEK1 — controles ICGC et GSE62452</h3>" + t)
    # C.6 atr drugs (60)
    t, _, _ = csv_table(
        RUNS / "atr_chek1_drugs.csv",
        "Inhibiteurs ATR/CHEK1 dans les 3 criblages (60 vrais inhibiteurs).",
        "Verdict : 0/60 FDR < 0,05. Aucun inhibiteur ATR/CHEK1 significatif.")
    parts.append("<h3>C.6 Inhibiteurs ATR/CHEK1 — les 60, dans les 3 criblages</h3>" + t)
    # C.7 mtap
    t, _, _ = csv_table(
        RUNS / "mtap_direct_tests.csv",
        "MTAP/PRMT5 contre l'axe KRAS, TCGA (deletion GISTIC mesuree, expression).",
        "Verdict : deletion MTAP non demontree enrichie (Fisher p = 0,073) ; PRMT5 monte en expression.")
    parts.append("<h3>C.7 MTAP / PRMT5 — tests directs</h3>" + t)
    t, _, _ = csv_table(
        RUNS / "mtap_controls.csv",
        "Controles MTAP/PRMT5 (CDKN2A, co-deletion 9p21).")
    parts.append("<h3>C.8 MTAP / PRMT5 — controles</h3>" + t)
    # C.9 pancancer
    t, _, _ = csv_table(
        RUNS / "pancancer_direct_tests.csv",
        "Pan-cancer : les 12 genes v4 contre l'axe KRAS, TCGA LUAD (515) et COAD (285).",
        "Verdict : CA125 plat dans les deux cohortes ; le colon a son propre programme KRAS (MUC2, REG4, CLCA1, KRT20).")
    parts.append("<h3>C.9 Pan-cancer — tests directs</h3>" + t)
    # C.10 prmt5
    t, _, _ = csv_table(
        RUNS / "data/prmt5_mtap_results.csv",
        "Dependance PRMT5 contre statut MTAP mesure (DepMap 24Q4, CN lineaire).",
        "Verdict : OUI, plus forte en pancreas (p = 0,0036).")
    parts.append("<h3>C.10 Dependance PRMT5 contre statut MTAP mesure</h3>" + t)
    # C.11 gdsc full
    t, _, _ = csv_table(
        RUNS / "data/gdsc_kras_screen.csv",
        "GDSC2 — les 269 composes testes contre l'axe Chronos KRAS (27 lignees pancras).",
        "Verdict : aucun inhibiteur MEK/ERK/RAF/KRAS significatif ; mediane rho -0,295 (lignées KRAS-dependantes globalement plus resistantes). Seul FDR < 0,05 : staurosporine, direction negative.")
    parts.append("<h3>C.11 GDSC2 — les 269 composes</h3>" + t)
    for extra in ("data/gdsc_kras_screen_pathways.csv", "data/gdsc_kras_screen_targets.csv"):
        p = RUNS / extra
        if p.exists():
            t, _, _ = csv_table(p, f"GDSC2 — {p.name}.")
            parts.append(f"<h3>C.12 GDSC2 — {html.escape(p.name)}</h3>" + t)
    # C.13 prism primaire : significatifs p<0.001 + totaux
    t, ntot, _ = csv_table(
        RUNS / "data/prism_kras_screen_named.csv",
        "PRISM primaire — composes avec p < 0,001 (sur 6 790 testes, 38 lignees).",
        "Verdict : ZERO compose FDR < 0,05. Les 12 ci-dessous sont les seuls p < 0,001 (environ 7 attendus par hasard). Le tableau complet de 6 790 lignes est dans le depot GitHub.",
        filter_fn=lambda r: float(r["p"]) < 0.001,
        sort_key=lambda r: float(r["p"]))
    parts.append("<h3>C.13 PRISM primaire — composes p &lt; 0,001 (12 sur 6 790)</h3>" + t)
    # MRTX1133 row explicite
    t, _, _ = csv_table(
        RUNS / "data/prism_kras_screen_named.csv",
        "PRISM primaire — MRTX1133 (inhibiteur KRAS G12D) : ligne complete.",
        "Valeur sur toutes les lignees (non significative apres correction) ; le test par allele est en C.16.",
        filter_fn=lambda r: "MRTX1133" in (r.get("Drug.Name") or ""))
    parts.append("<h3>C.14 PRISM primaire — MRTX1133</h3>" + t)
    # C.15 prism secondaire
    t, _, _ = csv_table(
        RUNS / "data/prism_secondary_kras_screen.csv",
        "PRISM secondaire dose-reponse — composes avec p_auc < 0,01 ou p_ic50 < 0,01 (sur 1 427 testes, 29 lignees).",
        "Verdict : ZERO compose FDR < 0,05 (FDR min 0,418 en AUC, 0,619 en IC50).",
        filter_fn=lambda r: (r.get("p_auc") not in ("", None) and float(r["p_auc"]) < 0.01)
        or (r.get("p_ic50") not in ("", None) and float(r["p_ic50"]) < 0.01),
        sort_key=lambda r: float(r["p_auc"]) if r.get("p_auc") not in ("", None) else 1.0)
    parts.append("<h3>C.15 PRISM secondaire — composes p &lt; 0,01</h3>" + t)
    # C.16 mrtx allele full
    t, _, _ = csv_table(
        RUNS / "data/mrtx1133_prism_kras_allele.csv",
        "MRTX1133 par allele — les 40 lignees PRISM (viabilite a 2,5 uM).",
        "Verdict : G12D -1,70 contre -0,38 autres, Mann-Whitney p = 0,0001.")
    parts.append("<h3>C.16 MRTX1133 par allele — les 40 lignees</h3>" + t)
    # C.17 crispr scan : top 30 + candidats connus
    scan_path = RUNS / "data/crispr_genome_scan.csv"
    with open(scan_path, newline="", encoding="utf-8") as f:
        scan = list(csv.DictReader(f))
    by_gene = {r["gene"]: r for r in scan}
    top = sorted(scan, key=lambda r: abs(float(r["rho"])), reverse=True)[:30]
    import io
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["gene", "entrez", "n", "rho", "p", "fdr",
                                        "mean_fort", "mean_moyen", "mean_faible"])
    w.writeheader()
    for r in top:
        w.writerow(r)
    tmp = RUNS / "data/_tmp_top30.csv"
    tmp.write_text(buf.getvalue(), encoding="utf-8")
    t, _, _ = csv_table(tmp, "Balayage CRISPR genome entier — top 30 par |rho| (sur 17 787 genes testes, 47 lignees).",
                        "Verdict : 2 hits FDR < 0,05 (TCF7L2, PRDX4) — faibles et non druggables ; le reste est du bruit probable.")
    tmp.unlink()
    parts.append("<h3>C.17 Balayage CRISPR — top 30</h3>" + t)
    known = ["KRAS", "TCF7L2", "PRDX4", "PSMD2", "RAF1", "PLK1", "BCL2L1",
             "CDK4", "MYC", "CDK6", "MAPK1", "PIK3CA", "STK33", "MAPK3",
             "MTOR", "TBK1", "AURKA", "ATR", "CHEK1", "BRCA2", "RAD51",
             "POLQ", "PARP1", "PARP2", "PRMT5", "MTAP", "CDKN2A"]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["gene", "entrez", "n", "rho", "p", "fdr",
                                        "mean_fort", "mean_moyen", "mean_faible"])
    w.writeheader()
    for g in known:
        if g in by_gene:
            w.writerow(by_gene[g])
    tmp = RUNS / "data/_tmp_known.csv"
    tmp.write_text(buf.getvalue(), encoding="utf-8")
    t, _, _ = csv_table(tmp, "Balayage CRISPR — candidats connus de la litterature et genes des bras (rang et FDR exacts).",
                        "Tous non significatifs apres correction, sauf TCF7L2 et PRDX4 (voir C.17).")
    tmp.unlink()
    parts.append("<h3>C.18 Balayage CRISPR — candidats connus</h3>" + t)
    # C.19 panc1 full 496
    t, _, _ = csv_table(
        RUNS / "data/panc1_combinations_summary.csv",
        "PANC-1 (NCATS) — les 496 combinaisons mesurees (gamma : < 1 synergique, < 0,5 forte).",
        "Verdict : 280/496 synergiques, 12 fortes ; zero paire avec un inhibiteur MEK/KRAS/ERK ou l'hydroxychloroquine.")
    parts.append("<h3>C.19 PANC-1 — les 496 combinaisons</h3>" + t)
    # C.20 expression check MUC16/CLDN18
    t, _, _ = csv_table(
        RUNS / "expression_muc16_cldn18_check.csv",
        "Verification MUC16/CLDN18 dans les 4 cohortes (quartiles, double-positifs).",
        "Verdict : KRAS-fort enrichi en MUC16 et CLDN18 eleves (3/4) ; double-positifs 0-2/12 — pas de base pour une combinaison a deux cibles.")
    parts.append("<h3>C.20 MUC16 / CLDN18 — verification dans les 4 cohortes</h3>" + t)
    # C.21 survie : resultats texte intégraux
    for fname, title in (("tcga_survival_verify_results.txt",
                          "C.21 Survie TCGA — resultats verifies (Cox et log-rank)"),
                         ("geo71729_survival_results.txt",
                          "C.22 Survie GSE71729 — resultats (Cox et log-rank)")):
        p = RUNS / fname
        if p.exists():
            parts.append(f"<h3>{title}</h3>"
                         f"<p class=\"small\">Fichier : <code>{fname}</code> — "
                         f"SHA-256 <code>{sha256(p)[:16]}…</code></p><pre>"
                         + html.escape(p.read_text(encoding="utf-8")) + "</pre>")
    return "\n".join(parts)

# ---------------------------------------------------------------- annexe D
SCRIPT_ROLES = {
    "analyze_panc1_combos.py": "Analyse des 496 combinaisons PANC-1 (NCATS).",
    "atr_chek1_cohorts.py": "Re-test ATR/CHEK1 : controles ICGC (70) et GSE62452 (69).",
    "atr_chek1_drugs.py": "Recherche des inhibiteurs ATR/CHEK1 dans les 3 criblages.",
    "atr_chek1_retest.py": "Re-test ATR/CHEK1 : purete et proliferation (TCGA 178).",
    "build_fluxes_cptac.py": "Construction des flux proteine CPTAC, centre UMich.",
    "build_fluxes_cptac_bcm.py": "Construction des flux proteine CPTAC, centre BCM.",
    "build_fluxes_depmap.py": "Construction des flux CRISPR DepMap (45 adeno, ordre Chronos KRAS).",
    "build_fluxes_geo62452.py": "Construction des flux GSE62452 (variantes a/b).",
    "build_fluxes_geo71729.py": "Construction des flux GSE71729 (variantes a/b/c).",
    "build_fluxes_geo71729_parp.py": "Construction des flux PARP GSE71729 (controle).",
    "build_fluxes_icgc.py": "Construction des flux ICGC PACA-AU.",
    "build_fluxes_immune.py": "Construction des flux immunitaires (4 cohortes).",
    "build_fluxes_pancancer.py": "Construction des flux pan-cancer LUAD/COAD.",
    "build_fluxes_tcga.py": "Construction des flux TCGA v1.",
    "build_fluxes_tcga_parp.py": "Construction des flux PARP TCGA.",
    "build_fluxes_tcga_v2.py": "Construction des flux TCGA v2 (hors purete).",
    "build_fluxes_tcga_v3.py": "Construction des flux TCGA v3 (correction purete).",
    "build_fluxes_tcga_v4.py": "Construction des flux TCGA v4 (hors sexe).",
    "build_matrix_umich.py": "Construction de la matrice proteine UMich (CPTAC).",
    "build_rotations.py": "Rotations de controle v4 (KRAS-valeur, CLDN18, purete, miroir).",
    "check_cox_tcga.py": "Contre-verification des Cox TCGA (2e implementation).",
    "check_expression_muc16_cldn18.py": "Verification MUC16/CLDN18 dans les 4 cohortes.",
    "check_tcga_radiation.py": "Radiotherapie TCGA et interaction avec CA125.",
    "crispr_genome_scan.py": "Balayage CRISPR genome entier (17 787 genes, DepMap 24Q4).",
    "direct_tests_immune.py": "Tests directs immunitaires le long de l'axe KRAS.",
    "download_gpl6244_mapping.py": "Telechargement du mapping sonde-vers-gene GPL6244.",
    "extract_immune_v6.py": "Extraction des resumes des runs immunitaires v6.",
    "fetch_tcga_fluxes.py": "Recuperation TCGA via API cBioPortal (route de contre-verification).",
    "gdsc_kras_screen.py": "Criblage GDSC2 contre l'axe Chronos KRAS.",
    "mrtx1133_prism_allele.py": "Test MRTX1133 par allele KRAS (PRISM).",
    "mtap_kras_tests.py": "Tests MTAP/PRMT5 contre l'axe KRAS (deletion GISTIC mesuree).",
    "pancancer_direct_tests.py": "Tests directs pan-cancer (LUAD, COAD).",
    "parp_direct_tests.py": "Tests directs reparation/PARP.",
    "pdc_query.py": "Requete PDC (CPTAC) via GraphQL.",
    "prism_screen.py": "Criblage PRISM primaire contre l'axe Chronos KRAS.",
    "prism_secondary_screen.py": "Criblage PRISM secondaire dose-reponse.",
    "prmt5_mtap_9p21_separation.py": "Separation effet MTAP / deletion 9p21 entiere.",
    "prmt5_mtap_dependency.py": "Dependance PRMT5 contre statut MTAP mesure.",
    "survival_geo71729.py": "Survie GSE71729 (Cox et log-rank).",
    "survival_icgc.py": "Survie ICGC PACA-AU (Cox et log-rank).",
    "survival_tcga_verify.py": "Survie TCGA verifiee (Cox Newton-Raphson, statsmodels, 2 log-rank).",
}


def annexe_d():
    parts = ["<h2>Annexe D — Code integral</h2>"
             "<p>Le pipeline v6 complet et l'integralite des scripts du "
             "projet, tels qu'ils ont tourne. Quelqu'un qui n'a que ce PDF "
             "peut relire le code exact. Les fichiers sont reproduits "
             " integralement, avec leur SHA-256. Le pipeline v6 original "
             "n'a jamais ete modifie ; la v6 est une copie construite par "
             "<code>build_v6.py</code> (voir l'en-tete du fichier).</p>"]
    # inventaire
    parts.append("<h3>D.1 Inventaire des scripts (SHA-256 et role)</h3>")
    inv = ["<table><thead><tr><th>Fichier</th><th>Octets</th>"
           "<th>SHA-256</th><th>Role</th></tr></thead><tbody>"]
    scripts = sorted(RUNS.glob("*.py")) + sorted(RUNS.glob("*.sh"))
    for s in scripts:
        inv.append(f"<tr><td><code>{html.escape(s.name)}</code></td>"
                   f"<td>{s.stat().st_size}</td>"
                   f"<td><code>{sha256(s)[:16]}…</code></td>"
                   f"<td>{html.escape(SCRIPT_ROLES.get(s.name, 'Voir l\u2019en-tete du fichier.'))}</td></tr>")
    inv.append("</tbody></table>")
    parts.append("\n".join(inv))
    # pipeline v6
    parts.append("<h3>D.2 Pipeline UNIVERSAL_LOG v6.0.0 — integral</h3>")
    parts.append(pre_file(V6, "Pipeline v6.0.0-L7aL7b-CohenD"))
    if BUILD_V6.exists():
        parts.append("<h3>D.3 Script de construction de la v6</h3>")
        parts.append(pre_file(BUILD_V6, "Construction v6 depuis v5.9.0f"))
    # tous les scripts
    parts.append("<h3>D.4 Scripts du projet — integral</h3>")
    for s in sorted(RUNS.glob("*.py")):
        parts.append(pre_file(s, SCRIPT_ROLES.get(s.name, "Script du projet")))
    for s in sorted(RUNS.glob("*.sh")):
        parts.append(pre_file(s, "Lanceur de runs v6 (mode fast)"))
    return "\n".join(parts)


# ---------------------------------------------------------------- annexe E
FIGURES = [
    ("results_fast_tcga_v4/csd_consensus.png",
     "Figure E.1 — CSD, TCGA v4 (178 patients, ordre KRAS croissant). "
     "Trois panneaux : AR(1), variance et |skewness| croissantes ; rho de "
     "Spearman par flux entre fenetres et indicateur ; traits rouges = "
     "quantiles nuls empiriques groupes. C'est le consensus CSD qui classe "
     "les flux et alimente le seuil L4/L7a du run v4 (T_0 93,22 %, L7a DOWN "
     "86,3 %). Source : results_fast_tcga_v4/csd_consensus.png, run v6 fast, "
     "15 nov. 2026."),
    ("results_fast_tcga_v4/landscape_complexity.png",
     "Figure E.2 — Paysage de complexite, TCGA v4. Vue d'ensemble du run : "
     "cascades, scores et structure detectee. Source : "
     "results_fast_tcga_v4/landscape_complexity.png, run v6 fast, 15 nov. 2026."),
    ("results_fast_tcga_v4/threshold_scan.png",
     "Figure E.3 — Scan des seuils (F1/F2), TCGA v4. Le scan dont sont issus "
     "les seuils T_-2 a T_+2 de la cascade (0 / 74,06 / 93,22 / 98,44 / "
     "98,96 %). Source : results_fast_tcga_v4/threshold_scan.png, run v6 "
     "fast, 15 nov. 2026."),
    ("results_fast_tcga_v4/post_threshold.png",
     "Figure E.4 — Flux apres seuil, TCGA v4. Lecture des flux de part et "
     "d'autre du seuil T_0 (step 166) : PGC, DPCR1 et CLDN18 s'effondrent, "
     "MUC16 monte. Source : results_fast_tcga_v4/post_threshold.png, run v6 "
     "fast, 15 nov. 2026."),
    ("results_fast_tcga_v4/zscore_fluxes.png",
     "Figure E.5 — Flux z-scores le long de l'ordre KRAS, TCGA v4. Les 12 "
     "flux normalises, ordonnes par KRAS croissant (purete et sexe "
     "corriges). Source : results_fast_tcga_v4/zscore_fluxes.png, run v6 "
     "fast, 15 nov. 2026."),
    ("results_fast_tcga_v4/raw_fluxes.png",
     "Figure E.6 — Flux bruts le long de l'ordre KRAS, TCGA v4. Meme ordre, "
     "valeurs non normalisees. Source : results_fast_tcga_v4/raw_fluxes.png, "
     "run v6 fast, 15 nov. 2026."),
    ("results_fast_icgc/csd_consensus.png",
     "Figure E.7 — CSD, ICGC PACA-AU (70 tumeurs). Meme lecture que E.1. "
     "Verdict du run : aucune separation reel/nul (Delta 1,44 contre 1,37) ; "
     "L7a NaN (n &lt; 75). Source : results_fast_icgc/csd_consensus.png, "
     "run v6 fast, 16 nov. 2026."),
    ("results_fast_geo62452/csd_consensus.png",
     "Figure E.8 — CSD, GSE62452 (69 tumeurs). Meme lecture que E.1. "
     "Verdict du run : aucune separation reel/nul (Delta 1,41 contre 1,26) ; "
     "L7a NaN (n &lt; 75). Source : results_fast_geo62452/csd_consensus.png, "
     "run v6 fast, 15 nov. 2026."),
    ("results_fast_geo71729/csd_consensus.png",
     "Figure E.9 — CSD, GSE71729 (145 tumeurs). Meme lecture que E.1. "
     "Verdict du run : aucune separation reel/nul (Delta 2,16 contre 2,20). "
     "Source : results_fast_geo71729/csd_consensus.png, run v6 fast, "
     "15 nov. 2026."),
    ("results_fast_pancancer_coad/csd_consensus.png",
     "Figure E.10 — CSD, TCGA COAD (285 tumeurs, colon). Meme lecture que "
     "E.1. Verdict : le colon a son propre programme KRAS (MUC2, REG4, "
     "CLCA1, KRT20) ; CA125 plat. Source : "
     "results_fast_pancancer_coad/csd_consensus.png, run v6 fast, 16 nov. 2026."),
    ("results_fast_pancancer_luad/csd_consensus.png",
     "Figure E.11 — CSD, TCGA LUAD (515 tumeurs, poumon). Meme lecture que "
     "E.1. Verdict : CA125 plat ; seul CEA garde un lien faible. Source : "
     "results_fast_pancancer_luad/csd_consensus.png, run v6 fast, 16 nov. 2026."),
    ("results_fast_immune_tcga/csd_consensus.png",
     "Figure E.12 — CSD, paysage immunitaire TCGA (178 patients, 12 genes "
     "immunitaires). Meme lecture que E.1. Verdict du run : aucune "
     "separation reel/nul ; le verdict (tumeur froide) vient des tests "
     "directs (annexe C.1). Source : "
     "results_fast_immune_tcga/csd_consensus.png, run v6 fast, 16 nov. 2026."),
    ("results_fast_parp/csd_consensus.png",
     "Figure E.13 — CSD, paysage reparation/PARP TCGA (178 patients). Meme "
     "lecture que E.1. Verdict du run : aucune separation reel/nul ; le "
     "verdict (BRCA2/ATR/RAD51 montent, PARP plat) vient des tests directs "
     "(annexe C.2). Source : results_fast_parp/csd_consensus.png, run v6 "
     "fast, 16 nov. 2026."),
    ("results_fast_atr/csd_consensus.png",
     "Figure E.14 — CSD, re-test ATR/CHEK1 TCGA (flux corriges purete). "
     "Meme lecture que E.1. Verdict du run : aucune separation reel/nul ; le "
     "verdict (ATR seul survit a la proliferation) vient des tests directs "
     "(annexe C.4). Source : results_fast_atr/csd_consensus.png, run v6 "
     "fast, 16 nov. 2026."),
    ("results_fast_cptac/csd_consensus.png",
     "Figure E.15 — CSD, proteine CPTAC UMich (63 tumeurs). Meme lecture "
     "que E.1. Verdict du run : aucune separation reel/nul (Delta 1,48 "
     "contre 1,49) ; L7a NaN ; la chaine v4 ne se confirme pas en proteine. "
     "Source : results_fast_cptac/csd_consensus.png, run v6 fast, 15 nov. 2026."),
]


def annexe_e():
    import base64
    parts = ["<h2>Annexe E — Figures</h2>"
             "<p>Les figures existantes qui portent un verdict, reproduites "
             "telles quelles (aucune figure generee pour ce PDF, aucune "
             "retouche). Chaque figure porte sa legende et sa provenance "
             "exacte (dossier de run, date). Les 670 figures PNG des runs ne "
             "sont pas toutes ici : seules celles qui portent un verdict sont "
             "reproduites ; les autres restent dans les dossiers de runs "
             "(archive locale et depot, voir annexe A).</p>"]
    for rel, caption in FIGURES:
        p = RUNS / rel
        if not p.exists():
            parts.append(f"<p class=\"small\">Figure manquante au moment de "
                         f"la construction : <code>{html.escape(rel)}</code> "
                         f"— signale, non inventee.</p>")
            continue
        b64 = base64.b64encode(p.read_bytes()).decode("ascii")
        parts.append(f"<figure><img src=\"data:image/png;base64,{b64}\" "
                     f"alt=\"{html.escape(caption[:120])}\">"
                     f"<figcaption>{html.escape(caption)}</figcaption></figure>")
    return "\n".join(parts)


# ---------------------------------------------------------------- annexe F
def annexe_f():
    return """<h2>Annexe F — Ethique et reproductibilite</h2>
<h3>F.1 Ce que ce document est, et ce qu'il n'est pas</h3>
<p>Ce document est un travail de recherche non clinique, benevole et sans
financement, sur des donnees publiques. Il ne donne aucun avis medical, ne
recommande aucun traitement a aucun patient, et ne promet aucune guerison.
Les medicaments cites (daraxonrasib, vopimetostat, IBI343, MRTX1133 et les
autres) sont rapportes tels que publies dans des essais cliniques ou des
communiques d'entreprises, avec leurs limites (effectifs, randomisation,
suivi) ; ce sont des faits publies, pas des recommandations. Toute decision
therapeutique appartient aux medecins et aux patients, jamais a ce document.</p>
<h3>F.2 Methodes completes</h3>
<p>Chaque bras est decrit dans le livre blanc (§8) avec son protocole, ses
effectifs, ses tests et ses fichiers ; chaque provenance (annexe B) donne la
source exacte, la nature des lignes et la production de chaque valeur ;
chaque table (annexe C) donne les effectifs et les corrections ; chaque
script (annexe D) est reproduit integralement. Les graines sont 42 partout
pour les nuls et les permutations. Les corrections pour tests multiples sont
Bonferroni ou Benjamini-Hochberg (FDR), precisees a chaque fois. Les seuils
de decision ont ete fixes avant les tests quand c'etait possible (ex. Fisher
p &lt; 0,05 bilateral pour MTAP ; FDR &lt; 0,05 pour les criblages) ; quand
un critere n'etait pas pre-enregistre, c'est ecrit.</p>
<h3>F.3 Versions exactes</h3>
<ul>
<li>Pipeline : UNIVERSAL_LOG v6.0.0-L7aL7b-CohenD,
<code>universal_v6.0.0_cohen.py</code>, SHA-256
bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773,
622 526 octets, 13 010 lignes. Original v5.9.0f intact, SHA-256
4f80f6a7d0809e802cbc9ec30c0bed552c1c8a95eb58687fd78e4ffd8e808260.</li>
<li>Python systeme 3.12 ; MDTraj 1.10.3 (construction HP35) ; module
<code>markdown</code> 3.11.3 (construction de ce PDF) ; Chromium (rendu
PDF). Les versions des librairies scientifiques (numpy, scipy, pandas,
statsmodels) ne sont pas consignees dans les provenances : c'est une limite
nommee — la reproduction exacte des p-values a la derniere decimale peut en
dependre, les verdicts (significatif ou non, direction) n'en dependent pas
aux effectifs utilises.</li>
<li>Machine : 2 vCPU, 7,7 Go RAM, pas de swap. Les runs v6 fast durent
environ 4 minutes ; les runs complets Cliff environ 2 h 30 (preuve du
14 novembre 2026).</li>
</ul>
<h3>F.4 Limites de chaque resultat (resume)</h3>
<table><thead><tr><th>Resultat</th><th>Limite principale</th></tr></thead><tbody>
<tr><td>CA125/CEA eleves chez les KRAS-forts (3/4 cohortes)</td><td>ARN en vrac (composition tissulaire) ; ICGC ne confirme pas en expression ; tailles modestes (12 patients dans le groupe).</td></tr>
<tr><td>Survie CA125 (2/3 cohortes)</td><td>Observationnel ; GSE71729 ne confirme pas ; pas de validation prospective.</td></tr>
<tr><td>Effondrement PGC/DPCR1/CLDN18 (TCGA seulement)</td><td>Depend de la correction de purete ; inverse ailleurs ; non confirme en proteine.</td></tr>
<tr><td>Daraxonrasib (13,2 contre 6,7 mois)</td><td>Resultat clinique publie, pas une prediction du pipeline ; population pretraitee ; suivi limite.</td></tr>
<tr><td>Vopimetostat + daraxonrasib (82 %, 18/22)</td><td>Phase 1/2 non randomisee, n = 22, sous-groupe MTAP-delete, pas de survie globale ; phase 3 en cours.</td></tr>
<tr><td>IBI343 (22,7 % de reponses)</td><td>Phase I non randomisee ; phase III en cours.</td></tr>
<tr><td>MRTX1133 tue les G12D (p = 0,0001)</td><td>Dose unique 2,5 uM ; essai clinique arrete ; axe Chronos chez les G12D suggestif seulement (n = 15).</td></tr>
<tr><td>ATR seul (expression)</td><td>Hypothese d'expression ; aucun appui CRISPR ni medicament ; aucune combinaison justifiee.</td></tr>
<tr><td>PRMT5 dependance (p = 0,0036)</td><td>Effet MTAP contre deletion 9p21 entiere non separe par ce test seul ; dependance PRMT5 seule, pas la combinaison.</td></tr>
<tr><td>Instrument v6</td><td>Ne separe pas reel et nul sur GEO/ICGC/pan-cancer/immunitaire/PARP ; L7a degenere sous n = 75 ; les verdicts reposent sur les tests directs.</td></tr>
</tbody></table>
<h3>F.5 Tous les resultats negatifs sont presents</h3>
<p>Aucun negatif n'est cache : effondrement TCGA non replique ; CRISPR des 12
genes negatif ; trois criblages negatifs ; CPTAC negatif ; MUC16 comme cible
negatif ; zolbetuximab echec randomise ; MEK + autophagie et MEK + CDK4/6
echecs cliniques ; KRAS + anti-PD-(L)1 non soutenu ; KRAS + PARP non soutenu ;
pan-cancer negatif ; MTAP non enrichi ; balayage CRISPR sans candidat
druggable ; ATR/CHEK1 sans appui medicament. Un negatif est un resultat : il
est note comme tel, avec ses effectifs.</p>
<h3>F.6 Ce qui n'a pas pu etre teste, et pourquoi</h3>
<ul>
<li>Daraxonrasib, RMC-9805, ASP3082, sotorasib, adagrasib, BI-3406, TNO155
contre l'axe KRAS : aucune matrice publique de dose-reponse multi-lignees ne
les contient ; donnees d'entreprises non publiques.</li>
<li>Combinaisons multi-lignees contre l'axe : aucune matrice publique
pancreatique n'existe (ALMANAC, AZ-DREAM, O'Neil : zero lignee pancreas ;
DrugComb injoignable depuis cette machine le 16 nov. 2026).</li>
<li>DGIdb (druggabilite TCF7L2/PRDX4) : API non exploitable par cette voie —
marque « a verifier », rien invente.</li>
<li>KRAS + autophagie (combinaison) : non fouillee dans ce projet.</li>
<li>Runs v6 CRISPR DepMap (45 &lt; 50 points minimum) : bloques ; la copie
v6.1 « series courtes » et le correctif L7a sont proposes, en attente du go
de Zackary — rien n'a ete lance sans son accord.</li>
</ul>
<h3>F.7 Conflits d'interets et statut des donnees</h3>
<p>Aucun financement ; aucun lien avec l'industrie pharmaceutique ; aucun
auteur ne vend quoi que ce soit ; le pipeline reste prive et n'est jamais
commercialise. Toutes les donnees sont publiques et gratuites, sources
nommees avec liens (annexe G). Aucune donnee privee, aucune donnee
identifiante : les identifiants patients (ex. TCGA-2J-AAB1-01) sont les codes
publics des depots. Les donnees d'origine (tlog28, juillet-octobre 2026)
sont du contexte, jamais une entree des verdicts du jour (regle du
15 novembre 2026).</p>
<h3>F.8 Ce que ce PDF ne contient pas, et pourquoi</h3>
<p>Les matrices brutes (~2 Go : DepMap CRISPRGeneEffect 428 Mo, OmicsCNGene
1,4 Go, tarballs Firehose, matrices GEO, matrices CPTAC) ne peuvent pas
tenir dans un PDF. Elles se re-telechargent verifiees (URL + MD5/SHA exacts,
annexe A) via le script <code>download_data.sh</code> du depot GitHub.
Les sorties completes des runs (670 figures PNG, fichiers df_feat, journaux)
ne sont pas toutes reproduites : 15 figures portent un verdict (annexe E) ;
le reste est dans les dossiers de runs (archive locale) et reproductible par
les commandes de l'annexe A. L'archive ZIP complete du 15 novembre (945 Mo,
1 841 fichiers) existe en local ; elle est perimee pour le 16 novembre et
sera reconstruite quand le round « remede » se cloture.</p>"""


# ---------------------------------------------------------------- annexe G
def annexe_g():
    if REGISTRY.exists():
        return ("<h2>Annexe G — Registre des sources (toutes, avec liens)</h2>"
                "<p>Chaque source citee dans ce document, avec son URL "
                "complete et cliquable. Aucune source nommee sans lien. Les "
                "liens morts sont notes avec leur miroir qui fonctionne.</p>"
                + md_html(REGISTRY.read_text(encoding="utf-8")))
    return ("<h2>Annexe G — Registre des sources (toutes, avec liens)</h2>"
            "<p class=\"small\">Registre en cours de compilation au moment "
            "de la construction de ce PDF (<code>source_registry.md</code> "
            "absent). Les liens des jeux de donnees sont dans l'annexe A, "
            "les liens complets des articles, essais et communiques sont "
            "dans les provenances (annexe B). Le registre complet sera "
            "ajoute a la prochaine regeneration du PDF.</p>")


def main():
    parts = [annexe_a(), annexe_b(), annexe_c(), annexe_d(),
             annexe_e(), annexe_f(), annexe_g()]
    doc = "\n".join(parts)
    OUT.write_text(doc, encoding="utf-8")
    print("appendix.html ecrit:", OUT, len(doc), "caracteres")


if __name__ == "__main__":
    main()
