#!/bin/bash
# Runs v6 fast — paysage immunitaire le long de l'axe KRAS (Bras 1, 16 nov. 2026)
# 8 runs séquentiels : réel + nul x 4 cohortes. Mode fast, cohen_d partout.
# Pipeline : universal_v6.0.0_cohen.py, SHA bb8bbdba4eb1f8c55b49748274ae8fbfef8a43f6c1b890964f18ba77960c0773 (vérifié avant lancement).
V6=/home/hatch/workspace/runs/biophysique-hp35/universal_v6.0.0_cohen.py
LOG=/home/hatch/workspace/runs/pdac-v6/runs_immune_v6.log
cd /home/hatch/workspace/runs/pdac-v6
echo "=== IMMUNE v6 $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" > "$LOG"
for TAG in tcga geo71729 geo62452 icgc; do
  python3 "$V6" --input pdac_immune_${TAG}_fluxes.csv --mode fast --output results_fast_immune_${TAG} >> "$LOG" 2>&1
  echo "V6_IMMUNE_${TAG}_EXIT:$?" >> "$LOG"
  python3 "$V6" --input pdac_immune_${TAG}_fluxes_nul.csv --mode fast --output results_fast_immune_${TAG}_nul >> "$LOG" 2>&1
  echo "V6_IMMUNE_${TAG}_NUL_EXIT:$?" >> "$LOG"
done
echo "=== FIN $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" >> "$LOG"
