#!/bin/bash
# §8.62 — Lot B : 31 runs v6.2 fast sur sous-échantillons (préfixe + stride).
# Protocole gelé : PROTOCOL_delta_scaling_862.md
# (SHA 8e67f8c7f17f92d297c5cbf02884e9a82778dd6c20fb8ee681afb3b24fb995b0).
# Lanceur séquentiel, journal des exit codes. À lancer via systemd-run
# (leçon AGENTS.md : les lots longs survivent à la session).
V6="/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
V6_SHA_ATTENDU="f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"
LOG="/home/hatch/workspace/runs/pdac-v6/runs_delta_scaling_862.log"
cd /home/hatch/workspace/runs/pdac-v6 || exit 1
echo "=== LOT 862 $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" >> "$LOG"
V6_SHA=$(sha256sum "$V6" | cut -d' ' -f1)
echo "V6 SHA: $V6_SHA (attendu $V6_SHA_ATTENDU)" >> "$LOG"
if [ "$V6_SHA" != "$V6_SHA_ATTENDU" ]; then
  echo "ABANDON : SHA v6.2 non conforme" >> "$LOG"
  exit 2
fi
run_one() {
  label="$1"; input="$2"; out="$3"
  echo "--- $label : $input -> $out $(date -u '+%H:%M:%S')" >> "$LOG"
  python3 "$V6" --input "$input" --mode fast --output "$out" >> "$LOG" 2>&1
  ec=$?
  echo "V62_862_${label}_EXIT:$ec" >> "$LOG"
  echo "--- $label exit $ec $(date -u '+%H:%M:%S')" >> "$LOG"
}
for k in 45 70 100 145 178 285 515 1000; do
  run_one "hp35_n${k}" "pdac_862_hp35_n${k}.csv" "results_fast_v62_862_hp35_n${k}"
done
for k in 45 70 100 145 178 285 515 1000; do
  run_one "hp35nul_n${k}" "pdac_862_hp35nul_n${k}.csv" "results_fast_v62_862_hp35nul_n${k}"
done
for k in 45 70 100 145 178 285 515; do
  run_one "luad_n${k}" "pdac_862_luad_n${k}.csv" "results_fast_v62_862_luad_n${k}"
done
for k in 45 70 100 145 178; do
  run_one "tcga_n${k}" "pdac_862_tcga_n${k}.csv" "results_fast_v62_862_tcga_n${k}"
done
for k in 100 285 515; do
  run_one "hp35_stride_n${k}" "pdac_862_hp35_stride_n${k}.csv" "results_fast_v62_862_hp35_stride_n${k}"
done
V6_SHA_FIN=$(sha256sum "$V6" | cut -d' ' -f1)
echo "V6 SHA fin: $V6_SHA_FIN" >> "$LOG"
echo "=== LOT 862 FIN $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" >> "$LOG"
