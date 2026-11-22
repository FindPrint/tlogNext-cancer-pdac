#!/bin/bash
# §8.93 etape 1 — Lot pipeline v6.2 (80 runs fast : 10 nuls frais x 8 paires
# principales). Graines 9101-9110 (PROTOCOL_nulls_distribution_893.md §3b).
# Lanceur sequentiel, journal des exit codes. A lancer via systemd-run
# (lecon AGENTS.md : les lots longs survivent a la session).
V6="/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
V6_SHA_ATTENDU="f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"
LOG="/home/hatch/workspace/runs/pdac-v6/runs_nulls_893_e1.log"
cd /home/hatch/workspace/runs/pdac-v6 || exit 1
echo "=== LOT 893-E1 $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" >> "$LOG"
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
    echo "V62_893_E1_${label}_EXIT:0 (saute, deja complet)" >> "$LOG"
    return 0
  fi
  echo "--- $label : $input -> $out $(date -u '+%H:%M:%S')" >> "$LOG"
  python3 "$V6" --input "$input" --mode fast --output "$out" >> "$LOG" 2>&1
  ec=$?
  echo "V62_893_E1_${label}_EXIT:$ec" >> "$LOG"
  echo "--- $label exit $ec $(date -u '+%H:%M:%S')" >> "$LOG"
}
for paire in hp35 tcga_v4 geo71729 geo62452 icgc immune_tcga parp_tcga depmap; do
  case "$paire" in
    hp35) base="test_biophysique_input" ;;
    tcga_v4) base="pdac_tcga_fluxes_v4" ;;
    geo71729) base="pdac_geo71729_fluxes" ;;
    geo62452) base="pdac_geo62452_fluxes" ;;
    icgc) base="pdac_icgc_fluxes" ;;
    immune_tcga) base="pdac_immune_tcga_fluxes" ;;
    parp_tcga) base="pdac_tcga_fluxes_parp" ;;
    depmap) base="pdac_depmap_fluxes" ;;
  esac
  for s in 9101 9102 9103 9104 9105 9106 9107 9108 9109 9110; do
    run_one "${paire}_nul_s${s}" "${base}_nul_s${s}.csv" "results_fast_v62_893_${paire}_nul_s${s}"
  done
done
V6_SHA_FIN=$(sha256sum "$V6" | cut -d' ' -f1)
echo "V6 SHA fin: $V6_SHA_FIN" >> "$LOG"
echo "=== LOT 893-E1 FIN $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" >> "$LOG"
