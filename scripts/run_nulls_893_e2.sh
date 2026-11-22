#!/bin/bash
# §8.93 etape 2 — Lot pipeline v6.2 (70 runs fast : 10 nuls frais x 7 paires
# A2 restantes). Graines 9101-9110 (PROTOCOL_nulls_distribution_893.md §3c).
# Lanceur sequentiel, journal des exit codes. A lancer via systemd-run.
V6="/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
V6_SHA_ATTENDU="f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"
LOG="/home/hatch/workspace/runs/pdac-v6/runs_nulls_893_e2.log"
cd /home/hatch/workspace/runs/pdac-v6 || exit 1
echo "=== LOT 893-E2 $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" >> "$LOG"
V6_SHA=$(sha256sum "$V6" | cut -d' ' -f1)
echo "V6 SHA: $V6_SHA (attendu $V6_SHA_ATTENDU)" >> "$LOG"
if [ "$V6_SHA" != "$V6_SHA_ATTENDU" ]; then
  echo "ABANDON : SHA v6.2 non conforme" >> "$LOG"
  exit 2
fi
run_one() {
  label="$1"; input="$2"; out="$3"
  if [ -f "$out/master_results.json" ]; then
    echo "--- $label : deja complet, saute $(date -u '+%H:%M:%S')" >> "$LOG"
    echo "V62_893_E2_${label}_EXIT:0 (saute, deja complet)" >> "$LOG"
    return 0
  fi
  echo "--- $label : $input -> $out $(date -u '+%H:%M:%S')" >> "$LOG"
  python3 "$V6" --input "$input" --mode fast --output "$out" >> "$LOG" 2>&1
  ec=$?
  echo "V62_893_E2_${label}_EXIT:$ec" >> "$LOG"
  echo "--- $label exit $ec $(date -u '+%H:%M:%S')" >> "$LOG"
}
for paire in geo21501 geo79668 geo60979 yeh_ff geo57495 gdc_organoid gse194249; do
  case "$paire" in
    geo21501) base="pdac_869_geo21501_fluxes" ;;
    geo79668) base="pdac_870_geo79668_fluxes" ;;
    geo60979) base="pdac_871_geo60979_fluxes" ;;
    yeh_ff) base="pdac_874_yeh_ff_fluxes" ;;
    geo57495) base="pdac_879_geo57495_fluxes" ;;
    gdc_organoid) base="pdac_885_gdc_organoid_fluxes" ;;
    gse194249) base="pdac_888_gse194249_fluxes" ;;
  esac
  for s in 9101 9102 9103 9104 9105 9106 9107 9108 9109 9110; do
    run_one "${paire}_nul_s${s}" "${base}_nul_s${s}.csv" "results_fast_v62_893_${paire}_nul_s${s}"
  done
done
V6_SHA_FIN=$(sha256sum "$V6" | cut -d' ' -f1)
echo "V6 SHA fin: $V6_SHA_FIN" >> "$LOG"
echo "=== LOT 893-E2 FIN $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" >> "$LOG"
