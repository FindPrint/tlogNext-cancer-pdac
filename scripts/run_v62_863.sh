#!/bin/bash
# §8.63 (D) — Lot pipeline v6.2 (10 runs fast : nuls ICGC frais s31-s40).
# Copie de run_v62_lot.sh (lanceur reprenable) : lit le manifeste
# (NOM|ENTREE|SORTIE), saute les sorties déjà complètes
# (master_results.json présent), journalise les exits.
# À lancer via systemd-run (leçon AGENTS.md : les lots longs survivent
# à la session, jamais nohup).
# Usage : ./run_v62_863.sh manifest_v62_863.txt runs_v62_863.log
# Protocole gelé : PROTOCOL_mechanisms_863.md
V62=/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py
MANIFEST="$1"
LOG="$2"
PDAC=/home/hatch/workspace/runs/pdac-v6
cd "$PDAC" || exit 1
echo "=== LOT v6.2 §8.63 $(date -u +%Y-%m-%dT%H:%M:%SZ) manifeste=$MANIFEST ===" >> "$LOG"
echo "V62_SHA256: $(sha256sum "$V62" | cut -d' ' -f1)" >> "$LOG"
n_done=0; n_run=0; n_fail=0
while IFS='|' read -r name input output; do
  case "$name" in ''|'#'*) continue;; esac
  if [ -f "$output/master_results.json" ]; then
    echo "SKIP $name ($output deja complet)" >> "$LOG"
    n_done=$((n_done+1)); continue
  fi
  echo "--- $name : $input -> $output ---" >> "$LOG"
  python3 "$V62" --input "$input" --mode fast --output "$output" >> "$LOG" 2>&1
  code=$?
  echo "EXIT_${name}:$code" >> "$LOG"
  if [ "$code" -eq 0 ]; then n_run=$((n_run+1)); else n_fail=$((n_fail+1)); fi
done < "$MANIFEST"
echo "=== FIN $(date -u +%Y-%m-%dT%H:%M:%SZ) deja_faits=$n_done termines=$n_run echecs=$n_fail ===" >> "$LOG"
echo "deja_faits=$n_done termines=$n_run echecs=$n_fail"
