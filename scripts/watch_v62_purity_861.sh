#!/bin/bash
# Surveillance §8.55 — relance le lot v6.2 tant que les 4 master_results.json
# ne sont pas présents ; s'arrête d'elle-même à 4/4.
# Ne supprime jamais le dossier d'un run en cours (le lanceur saute les
# sorties complètes). Miroir de watch_v62_immrot_848.sh, adapté §8.55 (4 runs).
# Lancement : systemd-run --unit=v62-purity-861 --collect \
#   --working-directory=/home/hatch/workspace/runs/pdac-v6 \
#   /bin/bash ./watch_v62_purity_861.sh
PDAC=/home/hatch/workspace/runs/pdac-v6
cd "$PDAC" || exit 1
OUTDIRS=$(awk -F'|' '{print $3}' manifest_v62_purity_861.txt)
for i in $(seq 1 12); do
  ./run_v62_lot.sh manifest_v62_purity_861.txt runs_v62_purity_861.log
  n=0
  for d in $OUTDIRS; do
    [ -f "$d/master_results.json" ] && n=$((n+1))
  done
  echo "WATCH purity-861 $(date -u +%Y-%m-%dT%H:%M:%SZ) complets=$n/4 (tour $i/12)" >> runs_v62_purity_861.log
  [ "$n" -eq 4 ] && exit 0
  sleep 300
done
echo "WATCH purity-861 : 12 tours écoulés sans 4/4 — arrêt, à relancer à la main." >> runs_v62_purity_861.log
exit 1
