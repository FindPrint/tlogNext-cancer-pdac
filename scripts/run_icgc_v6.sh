#!/bin/bash
# Runs v6 fast ICGC PACA-AU — 16 nov. 2026
V6=/home/hatch/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py
LOG=/home/hatch/workspace/runs/pdac-v6/runs_icgc_v6.log
echo "=== ICGC v6 $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" > "$LOG"
python3 "$V6" --input pdac_icgc_fluxes.csv --mode fast --output results_fast_icgc >> "$LOG" 2>&1
echo "V6_ICGC_EXIT:$?" >> "$LOG"
python3 "$V6" --input pdac_icgc_fluxes_nul.csv --mode fast --output results_fast_icgc_nul >> "$LOG" 2>&1
echo "V6_ICGC_NUL_EXIT:$?" >> "$LOG"
echo "=== FIN $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" >> "$LOG"
