#!/bin/bash
# Runs v6 fast GEO GSE62452 — 15 nov. 2026
V6=/home/hatch/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py
LOG=/home/hatch/workspace/runs/pdac-v6/runs_geo62452_v6.log
echo "=== GEO62452 v6 $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" > "$LOG"
python3 "$V6" --input pdac_geo62452_fluxes.csv --mode fast --output results_fast_geo62452 >> "$LOG" 2>&1
echo "V6_GEO62452_EXIT:$?" >> "$LOG"
python3 "$V6" --input pdac_geo62452_fluxes_nul.csv --mode fast --output results_fast_geo62452_nul >> "$LOG" 2>&1
echo "V6_GEO62452_NUL_EXIT:$?" >> "$LOG"
python3 "$V6" --input pdac_geo62452_fluxes_v4b.csv --mode fast --output results_fast_geo62452_v4b >> "$LOG" 2>&1
echo "V6_GEO62452_V4B_EXIT:$?" >> "$LOG"
python3 "$V6" --input pdac_geo62452_fluxes_v4b_nul.csv --mode fast --output results_fast_geo62452_v4b_nul >> "$LOG" 2>&1
echo "V6_GEO62452_V4B_NUL_EXIT:$?" >> "$LOG"
echo "=== FIN $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" >> "$LOG"
