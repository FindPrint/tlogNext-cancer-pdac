#!/bin/bash
# File d'attente §8.93–§8.96 (go de Zackary 21 nov. 2026 11h36).
# Execute SEQUENTIELLEMENT, un seul lot CPU a la fois (2 vCPU) :
#   0. attente fin du lot LUAD §8.96 bras A (4/4)
#   1. lot BRCA §8.96 bras B (4 runs, run_brca_896.sh)
#   2. replique Tier-2 §8.94 A1 (replica_w_894.py --lot, 16 cal + 32 builds)
#   3. replique §8.93 (replica_nulls_893.py --lot, 30 000 tirages)
#   4. nuls frais §8.93 etape 1 (80 runs, run_nulls_893_e1.sh)
#   5. nuls frais §8.93 etape 2 (70 runs, run_nulls_893_e2.sh)
# Chaque etape est reprenable (saute le travail deja complet) ; ce script
# ecrit un marqueur QUEUE_893_896_DONE quand tout est termine.
# Lancement : systemd-run --unit=v62-queue-893-896 --collect \
#   --working-directory=/home/hatch/workspace/runs/pdac-v6 \
#   /bin/bash ./queue_893_896.sh
# Surveillance : watch_queue_893_896.sh relance ce script tant que le
# marqueur DONE est absent. Ne supprime JAMAIS un dossier de run.
PDAC=/home/hatch/workspace/runs/pdac-v6
cd "$PDAC" || exit 1
LOG="$PDAC/queue_893_896.log"
qlog() { echo "QUEUE $(date -u +%Y-%m-%dT%H:%M:%SZ) $*" >> "$LOG"; echo "QUEUE $*"; }
[ -f "$PDAC/QUEUE_893_896_DONE" ] && { qlog "deja termine (marqueur DONE present)"; exit 0; }

# 0. Attendre LUAD 4/4 (max 60 min)
qlog "etape 0 : attente LUAD 4/4"
for i in $(seq 1 60); do
  n=0
  for d in results_fast_v62_896_luad results_fast_v62_896_luad_nul results_fast_v62_896_luad_nul_s9601 results_fast_v62_896_luad_nul_s9602; do
    [ -f "$d/master_results.json" ] && n=$((n+1))
  done
  qlog "LUAD complets=$n/4 (attente $i/60)"
  [ "$n" -eq 4 ] && break
  sleep 60
done
n=0
for d in results_fast_v62_896_luad results_fast_v62_896_luad_nul results_fast_v62_896_luad_nul_s9601 results_fast_v62_896_luad_nul_s9602; do
  [ -f "$d/master_results.json" ] && n=$((n+1))
done
if [ "$n" -ne 4 ]; then qlog "ABANDON etape 0 : LUAD $n/4 apres 60 min"; exit 1; fi
qlog "etape 0 OK : LUAD 4/4"

# 1. BRCA
qlog "etape 1 : lot BRCA"
./run_brca_896.sh
n=0
for d in results_fast_v62_896_brca results_fast_v62_896_brca_nul results_fast_v62_896_brca_nul_s9601 results_fast_v62_896_brca_nul_s9602; do
  [ -f "$d/master_results.json" ] && n=$((n+1))
done
qlog "etape 1 : BRCA complets=$n/4"
[ "$n" -ne 4 ] && { qlog "etape 1 INCOMPLETE ($n/4) — arret, reprise par le watcher"; exit 1; }

# 2. Replique Tier-2 §8.94 A1
qlog "etape 2 : replique Tier-2 §8.94 A1"
python3 replica_w_894.py --lot >> "$LOG" 2>&1
ec=$?
qlog "etape 2 : replica_w_894.py exit=$ec"
[ "$ec" -ne 0 ] && { qlog "etape 2 ECHEC (exit $ec) — arret, diagnostic a faire"; exit 1; }

# 3. Replique §8.93
qlog "etape 3 : replique §8.93 (30 000 tirages)"
python3 replica_nulls_893.py --lot >> "$LOG" 2>&1
ec=$?
qlog "etape 3 : replica_nulls_893.py exit=$ec"
[ "$ec" -ne 0 ] && { qlog "etape 3 ECHEC (exit $ec) — arret, diagnostic a faire (calibration ?)"; exit 1; }

# 4. Nuls frais etape 1
qlog "etape 4 : nuls frais §8.93 etape 1 (80 runs)"
./run_nulls_893_e1.sh
n=0
for paire in hp35 tcga_v4 geo71729 geo62452 icgc immune_tcga parp_tcga depmap; do
  for d in results_fast_v62_893_${paire}_nul_s91*/master_results.json; do
    [ -f "$d" ] && n=$((n + 1))
  done
done
qlog "etape 4 : dossiers E1=$n (attendu 80)"
[ "$n" -ne 80 ] && { qlog "etape 4 INCOMPLETE ($n/80) — arret, reprise par le watcher"; exit 1; }

# 5. Nuls frais etape 2
qlog "etape 5 : nuls frais §8.93 etape 2 (70 runs)"
./run_nulls_893_e2.sh
n2=0
for paire in geo21501 geo79668 geo60979 yeh_ff geo57495 gdc_organoid gse194249; do
  for d in results_fast_v62_893_${paire}_nul_s91*/master_results.json; do
    [ -f "$d" ] && n2=$((n2 + 1))
  done
done
qlog "etape 5 : dossiers E2=$n2 (attendu 70)"
[ "$n2" -ne 70 ] && { qlog "etape 5 INCOMPLETE ($n2/70) — arret, reprise par le watcher"; exit 1; }

qlog "FILE TERMINEE : toutes les etapes 0-5 OK"
touch "$PDAC/QUEUE_893_896_DONE"
exit 0
