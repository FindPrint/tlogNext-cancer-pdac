#!/bin/bash
# Surveillance de la file §8.93–§8.96 — relance queue_893_896.sh tant que
# le marqueur QUEUE_893_896_DONE est absent ; s'arrete d'elle-meme quand
# la file est terminee. Ne supprime jamais le dossier d'un run en cours
# (chaque etape saute le travail deja complet).
# Lancement : systemd-run --unit=v62-queue-893-896-watch --collect \
#   --working-directory=/home/hatch/workspace/runs/pdac-v6 \
#   /bin/bash ./watch_queue_893_896.sh
# TEST DU WATCHER (lecon AGENTS.md) : avant de lancer, verifier qu'un
# arret reel de queue_893_896.sh (exit 1) est bien suivi d'une relance
# au tour suivant — le watcher ne fait que relancer le script, il ne
# touche a aucun dossier de run.
PDAC=/home/hatch/workspace/runs/pdac-v6
cd "$PDAC" || exit 1
for i in $(seq 1 96); do
  if [ -f "$PDAC/QUEUE_893_896_DONE" ]; then
    echo "WATCH queue-893-896 $(date -u +%Y-%m-%dT%H:%M:%SZ) TERMINEE (marqueur DONE)" >> queue_893_896.log
    exit 0
  fi
  if systemctl is-active --quiet v62-queue-893-896 2>/dev/null; then
    echo "WATCH queue-893-896 $(date -u +%Y-%m-%dT%H:%M:%SZ) file en cours (tour $i/96)" >> queue_893_896.log
  else
    echo "WATCH queue-893-896 $(date -u +%Y-%m-%dT%H:%M:%SZ) relance de la file (tour $i/96)" >> queue_893_896.log
    systemd-run --unit=v62-queue-893-896 --collect --working-directory="$PDAC" /bin/bash ./queue_893_896.sh >> queue_893_896.log 2>&1
  fi
  sleep 900
done
echo "WATCH queue-893-896 : 96 tours ecoules (24 h) sans DONE — arret, a relancer a la main." >> queue_893_896.log
exit 1
