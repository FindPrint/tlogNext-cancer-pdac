#!/bin/bash
# Runs v6 fast — Bras 2 PARP (TCGA-PAAD) — 16 nov. 2026
# Invocation exacte reprise des bras précédents (run_icgc_v6.sh) :
#   python3 <v6> --input <csv> --mode fast --output <dir>
# SHA-256 v6 vérifié avant lancement :
#   bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773
V6=/home/hatch/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py
LOG=/home/hatch/workspace/runs/pdac-v6/runs_parp_v6.log
cd /home/hatch/workspace/runs/pdac-v6
echo "=== PARP v6 $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" > "$LOG"
echo "V6_SHA256: $(sha256sum "$V6" | cut -d' ' -f1)" >> "$LOG"
python3 "$V6" --input pdac_tcga_fluxes_parp.csv --mode fast --output results_fast_parp >> "$LOG" 2>&1
echo "V6_PARP_EXIT:$?" >> "$LOG"
python3 "$V6" --input pdac_tcga_fluxes_parp_nul.csv --mode fast --output results_fast_parp_nul >> "$LOG" 2>&1
echo "V6_PARP_NUL_EXIT:$?" >> "$LOG"
echo "=== FIN $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" >> "$LOG"
