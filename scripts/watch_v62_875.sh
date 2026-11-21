#!/bin/bash
# Surveillance §8.75 — relance le lanceur tant que les 40
# master_results.json ne sont pas présents. Usage : ./watch_v62_875.sh
# (modèle : watch_v62_873.sh, §8.73 ; jamais de suppression de dossier ;
# chaque grep est protégé, leçon AGENTS.md sur les hooks en
# set -o pipefail — ici pas de pipefail, mais les comptes passent par
# des fichiers temporaires, pas par des pipes fragiles.)
PDAC=/home/hatch/workspace/runs/pdac-v6
MANIFEST="$PDAC/manifest_v62_875.txt"
LOG="$PDAC/runs_v62_875.log"
TOTAL=40
tour=0
while true; do
  tour=$((tour+1))
  ls "$PDAC"/results_fast_v62_875_*/master_results.json > /tmp/watch875_list.txt 2>/dev/null || true
  n=$(wc -l < /tmp/watch875_list.txt || true)
  echo "WATCH 875 $(date -u +%Y-%m-%dT%H:%M:%SZ) complets=$n/$TOTAL (tour $tour)" >> "$PDAC/watch_v62_875.log"
  if [ "$n" -ge "$TOTAL" ]; then
    echo "WATCH 875 TERMINE $n/$TOTAL" >> "$PDAC/watch_v62_875.log"
    break
  fi
  "$PDAC/run_v62_875.sh" "$MANIFEST" "$LOG" >> "$PDAC/watch_v62_875.log" 2>&1
  sleep 20
  if [ "$tour" -ge 200 ]; then
    echo "WATCH 875 ABANDON apres 200 tours, complets=$n/$TOTAL" >> "$PDAC/watch_v62_875.log"
    break
  fi
done
