#!/bin/bash
# Surveillance §8.58 — relance le lanceur tant que les 24 master_results.json
# ne sont pas présents ; s'arrête d'elle-même à 24/24. Ne supprime jamais
# le dossier d'un run en cours.
PDAC=/home/hatch/workspace/runs/pdac-v6
LOG=$PDAC/watch_v62_858.log
TOTAL=24
tour=0
while true; do
  tour=$((tour+1))
  n=$(ls $PDAC/results_fast_v62_858_*/master_results.json 2>/dev/null | wc -l)
  echo "WATCH 858 $(date -u +%Y-%m-%dT%H:%M:%SZ) complets=$n/$TOTAL (tour $tour)" >> "$LOG"
  if [ "$n" -ge "$TOTAL" ]; then
    echo "WATCH 858 TERMINE $n/$TOTAL" >> "$LOG"
    break
  fi
  "$PDAC/run_v62_lot.sh" "$PDAC/manifest_v62_858.txt" "$PDAC/runs_v62_858.log" >> "$LOG" 2>&1
  sleep 20
  if [ "$tour" -ge 60 ]; then
    echo "WATCH 858 ABANDON apres 60 tours, complets=$n/$TOTAL" >> "$LOG"
    break
  fi
done
