#!/usr/bin/env bash
# download_data.sh — Re-telecharge TOUS les jeux de donnees du projet PDAC v6
# depuis leurs sources publiques, et verifie taille + MD5/SHA-256.
# VERSION CORRIGEE §8.77 (21 nov. 2026) — voir livre blanc §8.77 et
# DATA_SOURCES.md §29. Corrections (chaque ancienne voie est nommee avec
# la raison de son echec ; l'historique n'est pas efface) :
#  (1) PANC-1 : tarball codeload remplace par fichiers un par un (tronque).
#  (2) PRISM 19Q4 : 2 fichiers manquants ajoutes au dictionnaire want.
#  (3) PRISM 24Q2 primaire : verification SHA-256/MD5 ajoutee (etait `- -`)
#      + fichier de metadonnees des lignees ajoute.
#  (4) Supplements Nature ng3398 (MOESM59-63) et Springer Birnbaum
#      (MOESM1-5) : sections ajoutees, URL verifiees par SHA-256 (§8.77).
#  (5) SOFT GPL20769 : section ajoutee (chemin corrige GPL20nnn, l'ancien
#      GPL2nnn donnait 404) ; verification par taille exacte + SHA-256.
#  (6) ICGC probe map + NMF (hub Xena), QCMG clinique, clinique PanCanAtlas
#      (test C) : sections ajoutees, URL verifiees par SHA-256 (§8.77).
#  (7) CPTAC : URLs directes consignées en commentaire (le telechargement
#      via API Zenodo, qui fonctionne, est conserve).
#  (8) Durcissement des retelechargements : --retry-all-errors --retry-delay 5
#      partout (curl ne reessaie pas les 403 par defaut ; un 403 transitoire
#      de ndownloader a arrete le script complet le 21 nov. 2026, voir §8.77).
#  (9) OmicsCNGene.csv : endpoint API figshare remplace par ndownloader
#      (meme fichier, ID 51065324) — l'endpoint API est reste bloque a 0
#      octet pendant 9+ min le 21 nov. 2026, ndownloader servait le fichier
#      immediatement (test range : HTTP 206, 672 Ko/s).
# (10) Anti-blocage : --speed-limit 1000 --speed-time 300 sur get().
#      Deux connexions sont restees bloquees a 0 o/s sans jamais echouer
#      le 21 nov. 2026 (API figshare 9+ min ; GDAC 13+ min) — curl sans
#      limite de vitesse attend indefiniment et --retry ne se declenche
#      jamais. Avec cette limite, une connexion a 0 o/s pendant 5 min
#      echoue et le retry ouvre une connexion fraiche (le test range
#      GDAC fait juste apres donnait HTTP 206 a 768 Ko/s : l'hote
#      fonctionnait, c'etait la connexion qui etait morte).
#      Diagnostic final (21 nov. 2026) : les blocages venaient de
#      l'absence des variables proxy dans les unites systemd — en acces
#      direct, api.figshare.com et gdac.broadinstitute.org restent
#      bloques a 0 octet, alors que ndownloader.figshare.com fonctionne.
#      Les lots longs doivent etre lances AVEC le proxy :
#      systemd-run --setenv=https_proxy=http://hatch-egress-proxy:3128
#      --setenv=http_proxy=http://hatch-egress-proxy:3128 (sans
#      identifiants : le proxy fonctionne sans). Le script lui-meme ne
#      code pas le proxy en dur (propre a l'environnement d'execution).
# (11) ICGC expression : URL S3 directe remplacee par l'URL du hub
#      (meme fichier, SHA identique) — la S3 directe renvoie 403.
# (12) Reprise : get_checked() remplace toutes les paires get + check
#      (44 paires) — un fichier deja present et verifie (taille + SHA)
#      n'est pas re-telecharge ; un fichier partiel/corrompu est
#      re-telecharge. Le script complet a ete interrompu 3 fois le
#      21 nov. 2026 (403 transitoire, blocages 0 o/s, redemarrage
#      machine) ; sans reprise chaque incident coutait ~30 min de
#      re-telechargement integral.
# Usage : bash download_data.sh [dossier-destination, defaut : ./data]
# Les matrices brutes (~2 Go) ne sont pas dans ce depot GitHub (limite
# snapshot : fichiers UTF-8, 16 Mo maximum). Ce script est le moyen de les
# obtenir, verifiees. Chaque URL est exacte ; chaque hachage est celui qui
# figure dans les provenances (dossier provenance/) et dans l'annexe A du
# livre blanc PDF. Tout ecart = arreter et verifier la source.
# Requiert : curl, md5sum, sha256sum, python3 (pour les API figshare/Zenodo).
set -euo pipefail
DEST="${1:-./data}"
mkdir -p "$DEST" "$DEST/cptac" "$DEST/panc1_ncata"
FAIL=0

check() { # check <fichier> <taille> <md5|-> <sha256|->
  local f="$1" size="$2" md5="$3" sha="$4"
  local ok=1
  [ -f "$f" ] || { echo "MANQUANT : $f"; return 1; }
  local s; s=$(stat -c%s "$f")
  [ "$s" = "$size" ] || { echo "TAILLE INCORRECTE : $f ($s au lieu de $size)"; ok=0; }
  if [ "$md5" != "-" ]; then
    local m; m=$(md5sum "$f" | cut -d' ' -f1)
    [ "$m" = "$md5" ] || { echo "MD5 INCORRECT : $f ($m)"; ok=0; }
  fi
  if [ "$sha" != "-" ]; then
    local h; h=$(sha256sum "$f" | cut -d' ' -f1)
    [ "$h" = "$sha" ] || { echo "SHA-256 INCORRECT : $f"; ok=0; }
  fi
  if [ "$ok" = 1 ]; then echo "OK : $f"; else FAIL=1; return 1; fi
}

get() { # get <url> <destination>
  echo "Telechargement : $1"
  # --retry-all-errors : le 21 nov. 2026, le premier telechargement du
  # script complet a echoue sur un HTTP 403 TRANSITOIRE de ndownloader
  # (apres ~10 telechargements figshare rapproches) ; sans cette option
  # curl ne reessaie pas les 403 et le script s'arrete (set -e).
  # Re-teste quelques minutes plus tard, la meme URL repondait 302
  # (redirection normale vers S3). Delai de 5 s entre tentatives.
  curl -L --fail --retry 3 --retry-all-errors --retry-delay 5 --speed-limit 1000 --speed-time 300 -o "$2" "$1"
}

get_checked() { # get_checked <url> <destination> <taille> <md5|-> <sha256|->
  # CORRIGE §8.77 (12) — REPRISE : si le fichier existe deja et passe
  # la verification taille + hachage, on le garde (pas de
  # re-telechargement) ; sinon on le re-telecharge puis on verifie.
  # Un fichier partiel ou corrompu echoue le check et est donc
  # re-telecharge (rm -f avant curl). La verification reste la meme
  # que sans reprise : chaque fichier est controle par taille + SHA
  # (ou MD5), que ce soit un nouveau telechargement ou un fichier
  # deja present. Motif : le script complet (~2,4 Go) a ete interrompu
  # 3 fois le 21 nov. 2026 par des incidents transitoires reseau et
  # par un redemarrage machine — sans reprise, chaque incident coute
  # un re-telechargement integral.
  if [ -f "$2" ] && check "$2" "$3" "$4" "$5" >/dev/null 2>&1; then
    echo "DEJA PRESENT ET VERIFIE : $2"
    return 0
  fi
  rm -f "$2"
  get "$1" "$2"
  check "$2" "$3" "$4" "$5"
}

# ---------------------------------------------------------------- DepMap 24Q4
# Article figshare : https://doi.org/10.25452/figshare.plus.27993248.v1
get_checked "https://ndownloader.figshare.com/files/51064667" "$DEST/CRISPRGeneEffect.csv" 428678699 6edf7ade09b9b34199210b559d4745d3 3d8f3ec6dbf2db7ff834b79b508622ec0b226f3518003fe96ecf5a4fcf167e3b
get_checked "https://ndownloader.figshare.com/files/51065297" "$DEST/Model.csv" 645696 675210d17675f3517b0ce39a3c274f16 b7a0c1385e6cef30132b56aff61f1261d11e3f490490b355c430d32ee0dbdcfa
# CORRIGE §8.77 : l'ANCIENNE voie etait l'endpoint API
#   https://api.figshare.com/v2/file/download/51065324
# (meme fichier, ID 51065324). Le 21 nov. 2026, cet endpoint est reste
# bloque a 0 octet pendant 9+ min (curl toujours en attente des
# en-tetes, aucun fichier cree) alors que l'equivalent ndownloader
# servait le meme fichier immediatement (test range 0-2 000 000 o :
# HTTP 206, 672 Ko/s). La voie ndownloader est donc utilisee ici ;
# la verification MD5 + SHA-256 ci-dessous tranche (c'est elle qui
# prouve que le fichier est le bon). L'URL API d'origine reste
# consignee dans DATA_SOURCES.md §1.
get_checked "https://ndownloader.figshare.com/files/51065324" "$DEST/OmicsCNGene.csv" 1394554236 4696565fa74dc805983bc278b4a41802 4851d3e939d48837a39a0f01294deb90fa507a85703586a927b77474f999134c
get_checked "https://ndownloader.figshare.com/files/51065741" "$DEST/OmicsSomaticMutationsMAFProfile.maf" 98439503 - 86b8530b31125305391dcffb7dffc5426535df63705a2bf76565368f3955e96f
get_checked "https://ndownloader.figshare.com/files/51065750" "$DEST/OmicsSomaticMutationsMatrixHotspot.csv" 4210723 - 6444ce819a28d4228ff7b748e309611c5830c551620d8d2c7f86052e2675e3d8
get_checked "https://ndownloader.figshare.com/files/51065723" "$DEST/OmicsProfiles.csv" 254733 - 0bb19ee57935d4b213d378a4db9caacaa1db7318a63ae81485d84f91c20a3bf2

# ------------------------------------------------- TCGA Firehose 2016-01-28
# https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/PAAD/20160128/
get_checked "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/PAAD/20160128/gdac.broadinstitute.org_PAAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz" "$DEST/tcga_paad_rsem.tar.gz" 15296232 b09569ce3f4721f514bc137bd109ac0a -
get_checked "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/LUAD/20160128/gdac.broadinstitute.org_LUAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz" "$DEST/tcga_luad_rsem.tar.gz" 47043687 4c36eec3f6df75630292c5a569cfc8f4 -
get_checked "https://gdac.broadinstitute.org/runs/stddata__2016_01_28/data/COAD/20160128/gdac.broadinstitute.org_COAD.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0.tar.gz" "$DEST/tcga_coad_rsem.tar.gz" 26401036 e703a630556d42f098cf0df87d4712bb -
get_checked "https://gdac.broadinstitute.org/runs/analyses__2016_01_28/data/PAAD/20160128/gdac.broadinstitute.org_PAAD-TP.CopyNumber_Gistic2.Level_4.2016012800.0.0.tar.gz" "$DEST/tcga_paad_gistic.tar.gz" 26189717 816034f742e8f89ca8734ca2cf4404d5 -

# ---------------------------------------------------------------- GEO
get_checked "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE71nnn/GSE71729/matrix/GSE71729_series_matrix.txt.gz" "$DEST/GSE71729_series_matrix.txt.gz" 15622315 - b228789314ec4d866ec51b65724664abaa24b822577c55d3727820c867536a54
get_checked "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62452/matrix/GSE62452_series_matrix.txt.gz" "$DEST/GSE62452_series_matrix.txt.gz" 14447291 - 8f41d5b3f11451e653fd6bfc0c6b216c219d46711a7676d1e453dee16a078cba

# ---------------------------------------------------------------- ICGC / Xena
# Le portail ICGC DCC (https://dcc.icgc.org/) est mort (redirige vers
# l'accueil). Miroir qui fonctionne : UCSC Xena.
# CORRIGE §8.77 : l'ANCIENNE URL etait l'adresse S3 directe
#   https://icgc-xena-hub.s3.amazonaws.com/download/PACA-AU/nature16965-s2_normalised_exp.txt.gz
# Elle renvoie HTTP 403 (4 tentatives, 21 nov. 2026, execution full5
# du script complet — le listing du bucket est interdit aussi). La voie
# qui fonctionne est l'URL du hub, qui redirige (302) vers le bucket :
#   https://icgc.xenahubs.net/download/PACA-AU/nature16965-s2_normalised_exp.txt.gz
# verifiee le 21 nov. 2026 : 9 841 881 o, SHA-256 identique au consigne.
get_checked "https://icgc.xenahubs.net/download/PACA-AU/nature16965-s2_normalised_exp.txt.gz" "$DEST/icgc_pacaau_exp.txt.gz" 9841881 - c2cb57af3ba4c3d7fdac292e66c81067d36e16aae9efdd8005147e20820f49fa
get_checked "https://static-content.springer.com/esm/art%3A10.1038%2Fnature16965/MediaObjects/41586_2016_BFnature16965_MOESM270_ESM.xlsx" "$DEST/bailey2016_suppl_tables1-13.xlsx" 22104569 - 778224b36343c6c65b6df49b0149219ba2038cbdec2333b96e4e8798ff74258a

# ---------------------------------------------------------------- PRISM
# Primaire 24Q2, figshare article 25917643 :
# https://doi.org/10.6084/m9.figshare.25917643
get_checked "https://ndownloader.figshare.com/files/46630984" "$DEST/Repurposing_Public_24Q2_Extended_Primary_Data_Matrix.csv" 72456953 042b15d3ebcc138a80a571b9286451ae 3b6554cfc6c765af53088a676edc7bce00ee7d84fe808b93bbfa892de607bc3d
get_checked "https://ndownloader.figshare.com/files/46630981" "$DEST/Repurposing_Public_24Q2_Extended_Primary_Compound_List.csv" 719567 - 7e78f5901c1a97d2baab0789ab89832e716388da4eacaa9f094e7d2f2f5a3463
# Metadonnees des lignees (figshare 25917643, fichier 46630978) — CORRIGE
# §8.77 : absent du script d'origine (URL non consignee) ; URL retrouvee
# via l'API figshare et verifiee par SHA-256.
get_checked "https://ndownloader.figshare.com/files/46630978" "$DEST/Repurposing_Public_24Q2_Cell_Line_Meta_Data.csv" 157294 - 13a85da9e45656c455d3911a4491f3636d7d0975a9d2333dc3d0a3e2cd3b0526
# Secondaire 19Q4, figshare article 9393293 (DOI 10.6084/m9.figshare.9393293.v4) :
# telecharge via l'API figshare (le portail DepMap/figshare bloque curl
# sans API ; l'API, elle, repond).
python3 - "$DEST" << 'PYEOF'
import json, subprocess, sys, hashlib
dest = sys.argv[1]
api = "https://api.figshare.com/v2/articles/9393293"
files = json.loads(subprocess.check_output(["curl", "-s", api]))["files"]
want = {
    "secondary-screen-dose-response-curve-parameters.csv": ("264340589", "e629b9d505ad3d6bf65fde96f1c54bee"),
    "secondary-screen-replicate-collapsed-treatment-info.csv": ("3788355", None),
    # CORRIGE §8.77 : ces 2 fichiers manquaient du dictionnaire want
    # (le script d'origine ne telechargeait que 2 des 4 fichiers 19Q4).
    # MD5 verifies §8.77 ; URLs directes figshare (lues dans l'API
    # https://api.figshare.com/v2/articles/9393293) :
    #   cell-line-info : https://ndownloader.figshare.com/files/20237769
    #   readme         : https://ndownloader.figshare.com/files/20238123
    #   dose-response  : https://ndownloader.figshare.com/files/20237739
    #   replicate-collapsed : https://ndownloader.figshare.com/files/20237763
    "secondary-screen-cell-line-info.csv": ("40979", "6737b4aa9fd85404fd2f0cf825b037e4"),
    "secondary-screen-readme.txt": ("7647", "421d0bbadec381adc0d7981ee7e16bd7"),
}
for f in files:
    name = f["name"]
    if name in want:
        out = f"{dest}/{name}"
        print("Telechargement (API figshare) :", f["download_url"])
        subprocess.run(["curl", "-L", "--fail", "--retry", "3", "--retry-all-errors", "--retry-delay", "5", "-o", out, f["download_url"]], check=True)
        size, md5 = want[name]
        got_size = str(__import__("os").path.getsize(out))
        assert got_size == size, f"taille {name} : {got_size} au lieu de {size}"
        if md5:
            h = hashlib.md5(open(out, "rb").read()).hexdigest()
            assert h == md5, f"MD5 {name} : {h}"
        print("OK :", out)
PYEOF

# ---------------------------------------------------------------- GDSC2
# Cell Model Passports (Sanger) : https://api.cellmodelpassports.sanger.ac.uk/download_files
get_checked "https://cmp.cog.sanger.ac.uk/download/GDSC2_fitted_dose_response_27Oct23.xlsx" "$DEST/GDSC2_fitted_dose_response_27Oct23.xlsx" 22112537 - 0e99120a14a003dcbd3c27c020f1cfd35e38ee091067a2406f66c0d4dbc1c899
get_checked "https://cmp.cog.sanger.ac.uk/download/screened_compounds_rel_8.5.csv" "$DEST/screened_compounds_rel_8.5.csv" 46414 - d3cbb8b595980b36bf92d54af1da1dd995d2e2ce624c7cc70aacf2a754dce782

# ---------------------------------------------------------------- CPTAC
# Miroir Zenodo du paquet cptac, record 8394329 :
# https://doi.org/10.5281/zenodo.8394329 (etude PDC000393, Cao et al. Cell 2021).
# NOTE §8.77 : URLs directes par fichier (champ links.self lu dans la
# reponse de l'API https://zenodo.org/api/records/8394329, tailles et MD5
# conformes au §6) — le telechargement via API ci-dessous, qui fonctionne,
# est conserve ; ces URLs sont consignees ici pour la tracabilite :
#   umich Report : https://zenodo.org/api/records/8394329/files/umich-pdac-proteomics-Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz/content
#   bcm Tumor    : https://zenodo.org/api/records/8394329/files/bcm-pdac-proteomics-PDAC_proteomics_gene_abundance_log2_reference_intensity_normalized_Tumor.txt.gz/content
#   umich mapping: https://zenodo.org/api/records/8394329/files/umich-pdac-mapping-aliquot_to_patient_ID.tsv.gz/content
#   cptac_genes  : https://zenodo.org/api/records/8394329/files/cptac_genes.csv/content
# La matrice UMich locale (pdac_umich_protein_gene_matrix.csv) est DERIVEE :
# elle se reconstruit avec scripts/build_matrix_umich.py a partir du fichier
# Report ci-dessous.
python3 - "$DEST" << 'PYEOF'
import json, subprocess, sys, hashlib, os
dest = sys.argv[1]
api = "https://zenodo.org/api/records/8394329"
rec = json.loads(subprocess.check_output(["curl", "-s", api]))
by_name = {f["key"]: f for f in rec["files"]}
want = {
    "umich-pdac-proteomics-Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz": ("20504572", "a8c89b796b8ddacd48609e8ca7aac676"),
    "bcm-pdac-proteomics-PDAC_proteomics_gene_abundance_log2_reference_intensity_normalized_Tumor.txt.gz": ("7382441", "988150c28a2c1db14a3c0e62d08c06d2"),
    "umich-pdac-mapping-aliquot_to_patient_ID.tsv.gz": ("22881", "b013fad4a8f9fa26aa3915c0ef636754"),
    "cptac_genes.csv": ("462309", "afc250790ed6d18a7624a38fb872f62a"),
}
for name, (size, md5) in want.items():
    if name not in by_name:
        print("ABSENT du record Zenodo :", name); sys.exit(1)
    link = by_name[name]["links"]["self"]
    out = f"{dest}/cptac/{name}"
    print("Telechargement (Zenodo) :", name)
    subprocess.run(["curl", "-L", "--fail", "--retry", "3", "--retry-all-errors", "--retry-delay", "5", "-o", out, link], check=True)
    assert str(os.path.getsize(out)) == size, f"taille {name}"
    h = hashlib.md5(open(out, "rb").read()).hexdigest()
    assert h == md5, f"MD5 {name} : {h}"
    print("OK :", out)
PYEOF

# ---------------------------------------------------------------- PANC-1
# Depot GitHub ncats/PANC1 : https://github.com/ncats/PANC1
# CORRIGE §8.77 : l'ANCIENNE voie telechargeait le tarball
#   https://codeload.github.com/ncats/PANC1/tar.gz/refs/heads/main
# qui s'est revele TRONQUE en pratique (569 815 185 o, erreur gzip
# « unexpected end of file » a l'extraction — archive supprimee).
# La voie qui fonctionne est le telechargement fichier par fichier via
# raw.githubusercontent.com (URLs = champ download_url de l'API GitHub,
# conservees dans data/panc1_9191.json et data/panc1_9197.json).
# Chaque fichier est verifie taille + SHA-256 (valeurs DATA_SOURCES §10).
mkdir -p "$DEST/panc1_ncata"
get_checked "https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9191/calc.csv" "$DEST/panc1_ncata/9191_calc.csv" 24780 - 7a5c88d74a0b512b451755d62287b3d62bcb28cb82847e58debbe409e6e916be
get_checked "https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9191/metadata.csv" "$DEST/panc1_ncata/9191_metadata.csv" 80936 - e12c0251d3c1708e15b4dc7cc1fafb551b8c1bcbc25be96c4d42eea2f6a97e70
get_checked "https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9191/metadata_smiles.csv" "$DEST/panc1_ncata/9191_metadata_smiles.csv" 120243 - 4e0f0119e1c3133689d586cca2237d7199c49b6e72018cc29041f4aa209ed662
get_checked "https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9191/responses.csv" "$DEST/panc1_ncata/9191_responses.csv" 760685 - f5cc98d3442d3754f49d3e1c36e6d427e38f3c109eeebfae85486303cf18c90f
get_checked "https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9197/calc.csv" "$DEST/panc1_ncata/9197_calc.csv" 24165 - 3c50bb1b32d451e18384c525e3c3315609f9aa27a3ed7f50fad0fb33985d397b
get_checked "https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9197/metadata.csv" "$DEST/panc1_ncata/9197_metadata.csv" 71459 - 1240777419d25e985f9cf6ae998cd4393b2d2f53be404c9b595cb66178bba0f0
get_checked "https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9197/metadata_smiles.csv" "$DEST/panc1_ncata/9197_metadata_smiles.csv" 108941 - d45b7d730c002e96340778396e222a76910c98d54060e2e221d4e1151b822cfa
get_checked "https://raw.githubusercontent.com/ncats/PANC1/main/NCATS/9197/responses.csv" "$DEST/panc1_ncata/9197_responses.csv" 750256 - cdece93912122bc6599942ee050c87501455d433d94ebf1d7e43960237ea1173
# mit_test.csv : URL reconstruite au §10, VERIFIEE par SHA-256 au §8.77.
get_checked "https://raw.githubusercontent.com/ncats/PANC1/main/MIT/test.csv" "$DEST/panc1_ncata/mit_test.csv" 3249228 - 9f3ae18976136412802831487b6187fcf062db8f4ca753990689d3ac62006e27

# ------------------------------------------------- Supplements Nature/Springer
# AJOUTE §8.77 : ces supplements n'etaient pas telecharges par le script
# d'origine (URLs non consignees). URLs verifiees par SHA-256 (§8.77).
# Moffitt et al. 2015, Nat Genet 47:1168-78, doi 10.1038/ng.3398.
get_checked "https://static-content.springer.com/esm/art%3A10.1038%2Fng.3398/MediaObjects/41588_2015_BFng3398_MOESM59_ESM.pdf" "$DEST/ng3398_MOESM59_ESM.pdf" 5339711 - c18dbc59b72733e170720f50c2d7f39c1cfdbac2ceb4d1bbdf16af0fb5d320c0
get_checked "https://static-content.springer.com/esm/art%3A10.1038%2Fng.3398/MediaObjects/41588_2015_BFng3398_MOESM60_ESM.txt" "$DEST/ng3398_MOESM60_ESM.txt" 19393438 - 516cf2eb976adb580b69979a0fae787e9728c463d924b574f8b56ac78a44c7db
get_checked "https://static-content.springer.com/esm/art%3A10.1038%2Fng.3398/MediaObjects/41588_2015_BFng3398_MOESM61_ESM.xlsx" "$DEST/ng3398_MOESM61_ESM.xlsx" 460785 - ec26858b1b3394c4dcb65b17310612e84d0b58b8cc2309d6d2cba65a8c1c01ad
get_checked "https://static-content.springer.com/esm/art%3A10.1038%2Fng.3398/MediaObjects/41588_2015_BFng3398_MOESM62_ESM.xlsx" "$DEST/ng3398_MOESM62_ESM.xlsx" 2612836 - 25c35346ec98bf067b563c943b7f74ac5bb78454a0191f22216a982196d08b5c
get_checked "https://static-content.springer.com/esm/art%3A10.1038%2Fng.3398/MediaObjects/41588_2015_BFng3398_MOESM63_ESM.xlsx" "$DEST/ng3398_MOESM63_ESM.xlsx" 14141 - 3d508a54d97f93d5f203ed9f431efe0e5f4699df41613c9b377257bb48020905
# Birnbaum et al. 2017, Mol Cancer 16:174, doi 10.1186/s12943-017-0739-z
# (PMC5674743).
get_checked "https://static-content.springer.com/esm/art%3A10.1186%2Fs12943-017-0739-z/MediaObjects/12943_2017_739_MOESM1_ESM.xlsx" "$DEST/birnbaum_springer_MOESM1.xlsx" 11209 - 3d9df7b9bdbb2cf8c0ee20a62c1b798f5faed4eec053b4e785f9f8e0dff4945b
get_checked "https://static-content.springer.com/esm/art%3A10.1186%2Fs12943-017-0739-z/MediaObjects/12943_2017_739_MOESM2_ESM.xlsx" "$DEST/birnbaum_springer_MOESM2.xlsx" 15240 - 721e19d95710413762ea92ba6ae216b18bdf25f0d736ffd78bcfafd34a8b77c3
get_checked "https://static-content.springer.com/esm/art%3A10.1186%2Fs12943-017-0739-z/MediaObjects/12943_2017_739_MOESM3_ESM.xlsx" "$DEST/birnbaum_springer_MOESM3.xlsx" 9119 - 8bfbdcd618ea2a9d9b8ae480c763b857c3e23e2022462ab61cff0aaa8c6b1a13
get_checked "https://static-content.springer.com/esm/art%3A10.1186%2Fs12943-017-0739-z/MediaObjects/12943_2017_739_MOESM4_ESM.xlsx" "$DEST/birnbaum_springer_MOESM4.xlsx" 15040 - 49fff4c84c8859ee12072282f4e69f02cf10cce90a638506c6888ea9fa7df361
get_checked "https://static-content.springer.com/esm/art%3A10.1186%2Fs12943-017-0739-z/MediaObjects/12943_2017_739_MOESM5_ESM.xlsx" "$DEST/birnbaum_springer_MOESM5.xlsx" 8767 - 94af1f7351a9028cab962c160c51ceea47f882705496db5e00f266a06fdb6ccb

# ------------------------------------------------- Annotation GPL20769 (SOFT)
# AJOUTE §8.77 : le SOFT n'etait pas conserve dans data/ et son URL
# n'etait pas consignee. L'ANCIEN chemin devine au §15.4
# (geo/platforms/GPL2nnn/GPL20769/soft/) donne 404 : le regroupement GEO
# masque les 3 derniers chiffres (20769 -> GPL20nnn, comme 6244 -> GPL6nnn).
# Verification par taille exacte (37 588 662 o) + SHA-256 (verifies §8.77).
get_checked "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL20nnn/GPL20769/soft/GPL20769_family.soft.gz" "$DEST/GPL20769_family.soft.gz" 37588662 4c39e802ec78170d7ed5c8c2cc2b0bec ecb1b79a6b89e521a1116a3113fcb9a5af1c181329eec8257e044e0683822d3e

# ------------------------------------------------- ICGC probe map + NMF (hub Xena)
# AJOUTE §8.77 : jeux nommes aux §5.3-5.4 mais URLs non consignees.
# Les URL S3 directes renvoient 403 ; les URL du hub fonctionnent
# (le hub redirige vers le bucket S3). Verifiees par SHA-256 (§8.77).
get_checked "https://icgc.xenahubs.net/download/PACA-AU/ensembleGene_hg19_nature16965-s2_normalised_exp.gz" "$DEST/icgc_pacaau_probemap.gz" 353314 - b09a746f6084215beea3632b72e87834ea577d18fcb52add3641de5d0d975537
get_checked "https://icgc.xenahubs.net/download/PACA-AU/nature16965-s2_NMF_class_assignment.txt.gz" "$DEST/icgc_pacaau_nmf.txt.gz" 447 - f1e84b997c24903c216fbe9806c1b048cd9f552894e018ca54d02b5413921e2f

# ------------------------------------------------- QCMG clinique (cBioPortal datahub)
# AJOUTE §8.77 : « fichier clinique datahub » sans URL (§12).
# Les fichiers du depot cBioPortal/datahub sont en Git LFS : le
# download_url de l'API GitHub (raw.githubusercontent.com) renvoie le
# pointeur LFS (130 o) ; le contenu reel est servi par
# media.githubusercontent.com. Verifies par SHA-256 (§8.77).
# Fichiers ECARTES pour les verdicts (non utilises) — recuperes pour
# la tracabilite seulement.
get_checked "https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_qcmg_uq_2016/data_clinical_patient.txt" "$DEST/qcmg_clinical_patient.txt" 49042 - ae7fc6d7a8c887bb890090f1fc1c3770b94fb31dde38e209c684bc0ffbfd6a95
get_checked "https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_qcmg_uq_2016/data_clinical_sample.txt" "$DEST/qcmg_clinical_sample.txt" 57215 - c70daf3e772cdcf99b62ca20f8a85f748df80631fd915b7da465e670a1fcceca

# ------------------------------------------------- Clinique TCGA PanCanAtlas (test C)
# AJOUTE §8.77 : provenance d'acquisition MANQUANTE (§11) — fichier
# retrouve dans le depot cBioPortal/datahub, etude
# paad_tcga_pan_can_atlas_2018 (meme remarque LFS que QCMG ci-dessus).
# Verifie par SHA-256 : le pointeur LFS lui-meme porte
# oid sha256:0c274268… (double confirmation). Sans cette verification,
# ce bloc n'existerait pas (aucune URL devinee).
get_checked "https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/paad_tcga_pan_can_atlas_2018/data_clinical_patient.txt" "$DEST/data_clinical_patient.txt" 58621 - 0c2742688e59bb918d446d35f755d7a849c3e647ab184dc54d4f7e807be2efe5

if [ "$FAIL" = 1 ]; then echo "ECHEC : au moins une verification a echoue."; exit 1; fi
echo "TERMINE : tous les jeux de donnees telecharges et verifies dans $DEST"
echo "Etapes suivantes : construire les flux (scripts/build_fluxes_*.py),"
echo "puis lancer le pipeline v6 (voir README.md)."
