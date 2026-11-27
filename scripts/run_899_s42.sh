#!/bin/bash
# §8.99 — Nul graine 42 pour le registre A2 classique (GSE184585).
# Hors verdict §8.99 (jugé sur les 10 nuls frais 9301-9310, protocole gelé) :
# ce nul sert uniquement à mettre à jour le registre A2 (défini contre le
# nul graine 42) et le LOO, comme le §8.99.4 le délègue au coordinateur.
# Lanceur reprenable (saute le run si master_results.json existe), journal.
# Lancement : systemd-run --unit=v62-899-gse184585-s42 --collect \
#   --working-directory=/home/hatch/workspace/runs/pdac-v6 \
#   /bin/bash ./run_899_s42.sh
V6="/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
V6_SHA_ATTENDU="f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"
BUILD_NULL="/home/hatch/workspace/runs/pdac-v6/nulls_lot_next/scripts/build_null_893.py"
BUILD_NULL_SHA_ATTENDU="572b55bc6d2b14e349e42850076e7ada331996da3a82947ca66bc08e2556f467"
LOG="/home/hatch/workspace/runs/pdac-v6/runs_899_s42.log"
cd /home/hatch/workspace/runs/pdac-v6 || exit 1
echo "=== LOT 899-s42 $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" >> "$LOG"
V6_SHA=$(sha256sum "$V6" | cut -d' ' -f1)
echo "V6 SHA avant: $V6_SHA (attendu $V6_SHA_ATTENDU)" >> "$LOG"
[ "$V6_SHA" = "$V6_SHA_ATTENDU" ] || { echo "ABANDON : SHA v6.2 non conforme" >> "$LOG"; exit 2; }
BN_SHA=$(sha256sum "$BUILD_NULL" | cut -d' ' -f1)
echo "build_null_893 SHA: $BN_SHA (attendu $BUILD_NULL_SHA_ATTENDU)" >> "$LOG"
[ "$BN_SHA" = "$BUILD_NULL_SHA_ATTENDU" ] || { echo "ABANDON : SHA build_null non conforme" >> "$LOG"; exit 2; }
if [ ! -f "pdac_899_gse184585_fluxes_nul_s42.csv" ]; then
  python3 "$BUILD_NULL" --real pdac_899_gse184585_fluxes.csv --seed 42 \
    --out pdac_899_gse184585_fluxes_nul_s42.csv >> "$LOG" 2>&1
  echo "BUILD_NULL_EXIT:$?" >> "$LOG"
  sha256sum pdac_899_gse184585_fluxes_nul_s42.csv >> "$LOG"
else
  echo "nul s42 deja construit, saute" >> "$LOG"
fi
OUT="results_fast_v62_899_gse184585_nul_s42"
if [ -f "$OUT/master_results.json" ]; then
  echo "--- nul_s42 : deja complet, saute $(date -u '+%H:%M:%S')" >> "$LOG"
  echo "V62_899_nul_s42_EXIT:0 (saute, deja complet)" >> "$LOG"
else
  echo "--- nul_s42 : pdac_899_gse184585_fluxes_nul_s42.csv -> $OUT $(date -u '+%H:%M:%S')" >> "$LOG"
  python3 "$V6" --input pdac_899_gse184585_fluxes_nul_s42.csv --mode fast --output "$OUT" >> "$LOG" 2>&1
  ec=$?
  echo "V62_899_nul_s42_EXIT:$ec" >> "$LOG"
  echo "--- nul_s42 exit $ec $(date -u '+%H:%M:%S')" >> "$LOG"
fi
V6_SHA_APRES=$(sha256sum "$V6" | cut -d' ' -f1)
echo "V6 SHA apres: $V6_SHA_APRES (attendu $V6_SHA_ATTENDU)" >> "$LOG"
[ "$V6_SHA_APRES" = "$V6_SHA_ATTENDU" ] || { echo "ALERTE : SHA v6.2 modifie pendant le lot" >> "$LOG"; exit 3; }
echo "=== LOT 899-s42 TERMINE $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" >> "$LOG"
