#!/bin/bash
# Surveillance §8.72 — relance le lanceur tant que les 10 master_results.json
# ne sont pas présents. Usage : ./watch_v62_873.sh
# (modèle : watch_v62_870.sh, §8.70 ; jamais de suppression de dossier.)
PDAC=/home/hatch/workspace/runs/pdac-v6
MANIFEST="$PDAC/manifest_v62_873.txt"
LOG="$PDAC/runs_v62_873.log"
TOTAL=20
TAG="873"
tour=0
while true; do
  tour=$((tour+1))
  n=$(ls $PDAC/results_fast_v62_873_*/master_results.json 2>/dev/null | wc -l)
  echo "WATCH 873 $(date -u +%Y-%m-%dT%H:%M:%SZ) complets=$n/$TOTAL (tour $tour)" >> "$PDAC/watch_v62_873.log"
  if [ "$n" -ge "$TOTAL" ]; then
    echo "WATCH 873 TERMINE $n/$TOTAL" >> "$PDAC/watch_v62_873.log"
    break
  fi
  "$PDAC/run_v62_lot.sh" "$MANIFEST" "$LOG" >> "$PDAC/watch_v62_873.log" 2>&1
  sleep 20
  if [ "$tour" -ge 120 ]; then
    echo "WATCH 873 ABANDON apres 120 tours, complets=$n/$TOTAL" >> "$PDAC/watch_v62_873.log"
    break
  fi
done
