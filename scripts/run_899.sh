#!/bin/bash
# §8.99 — Lot pipeline v6.2 (11 runs fast : 1 réel GSE184585 + 10 nuls
# frais graines 9301-9310, PROTOCOL_899_gse184585.md gelé 27 nov. 2026).
# Lanceur séquentiel, reprenable (saute tout run dont
# master_results.json existe), journal des exit codes.
# Lancement : systemd-run --unit=v62-899-gse184585 --collect \
#   --working-directory=/home/hatch/workspace/runs/pdac-v6 \
#   /bin/bash ./run_899.sh
# Ne supprime JAMAIS un dossier de run. Ne jamais écraser.
V6="/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
V6_SHA_ATTENDU="f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"
LOG="/home/hatch/workspace/runs/pdac-v6/runs_899.log"
cd /home/hatch/workspace/runs/pdac-v6 || exit 1
echo "=== LOT 899 $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" >> "$LOG"
V6_SHA=$(sha256sum "$V6" | cut -d' ' -f1)
echo "V6 SHA avant lot: $V6_SHA (attendu $V6_SHA_ATTENDU)" >> "$LOG"
if [ "$V6_SHA" != "$V6_SHA_ATTENDU" ]; then
  echo "ABANDON : SHA v6.2 non conforme" >> "$LOG"
  exit 2
fi
run_one() {
  label="$1"; input="$2"; out="$3"
  if [ -f "$out/master_results.json" ]; then
    echo "--- $label : deja complet, saute $(date -u '+%H:%M:%S')" >> "$LOG"
    echo "V62_899_${label}_EXIT:0 (saute, deja complet)" >> "$LOG"
    return 0
  fi
  echo "--- $label : $input -> $out $(date -u '+%H:%M:%S')" >> "$LOG"
  python3 "$V6" --input "$input" --mode fast --output "$out" >> "$LOG" 2>&1
  ec=$?
  echo "V62_899_${label}_EXIT:$ec" >> "$LOG"
  echo "--- $label exit $ec $(date -u '+%H:%M:%S')" >> "$LOG"
}
run_one "reel" "pdac_899_gse184585_fluxes.csv" "results_fast_v62_899_gse184585"
for s in 9301 9302 9303 9304 9305 9306 9307 9308 9309 9310; do
  run_one "nul_s${s}" "pdac_899_gse184585_fluxes_nul_s${s}.csv" \
    "results_fast_v62_899_gse184585_nul_s${s}"
done
V6_SHA_APRES=$(sha256sum "$V6" | cut -d' ' -f1)
echo "V6 SHA apres lot: $V6_SHA_APRES (attendu $V6_SHA_ATTENDU)" >> "$LOG"
if [ "$V6_SHA_APRES" != "$V6_SHA_ATTENDU" ]; then
  echo "ALERTE : SHA v6.2 modifie pendant le lot" >> "$LOG"
  exit 3
fi
echo "=== LOT 899 TERMINE $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" >> "$LOG"
