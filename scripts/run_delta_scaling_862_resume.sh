#!/bin/bash
# §8.62 — REPRISE du lot B après redémarrage machine (20 nov. 2026 ~13h21 UTC).
# Le lot initial (unité delta-scaling-862) s'est arrêté au run 14
# (hp35nul_n285, démarré 13:20:42, sans master_results.json) quand la
# machine a redémarré ; 13 runs exit 0 déjà valides (d_div/d_sat/Delta
# finis, vérifiés). Cette reprise SAUTE les sorties valides et relance
# les 18 restantes, même commande, même protocole gelé.
# Précédent : run_nulls_n70_853_resume.sh (§8.53).
V6="/home/hatch/workspace/runs/biophysique-hp35/universal_v6.2.0_cohen.py"
V6_SHA_ATTENDU="f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf"
LOG="/home/hatch/workspace/runs/pdac-v6/runs_delta_scaling_862.log"
cd /home/hatch/workspace/runs/pdac-v6 || exit 1
echo "=== LOT 862 REPRISE $(date -u '+%Y-%m-%d %H:%M:%S UTC') (redémarrage machine, 13 valides conservés) ===" >> "$LOG"
V6_SHA=$(sha256sum "$V6" | cut -d' ' -f1)
echo "V6 SHA: $V6_SHA (attendu $V6_SHA_ATTENDU)" >> "$LOG"
if [ "$V6_SHA" != "$V6_SHA_ATTENDU" ]; then
  echo "ABANDON : SHA v6.2 non conforme" >> "$LOG"
  exit 2
fi
run_one() {
  label="$1"; input="$2"; out="$3"
  if [ -f "$out/master_results.json" ] && python3 -c "
import json,math,sys
j=json.load(open('$out/master_results.json'))
dv=j['holographic_tension_state']['D_vector']
d=j['reading_synthesis']['Delta_tension']
assert all(math.isfinite(float(dv[k])) for k in ('d_div','d_sat')) and math.isfinite(float(d))
" 2>/dev/null; then
    echo "SKIP $label : $out déjà valide" >> "$LOG"
    return 0
  fi
  # sortie partielle (run tué par le redémarrage) : repartir d'un dossier propre
  if [ -d "$out" ]; then rm -rf "$out"; echo "RESET $label : dossier partiel supprimé" >> "$LOG"; fi
  echo "--- $label : $input -> $out $(date -u '+%H:%M:%S')" >> "$LOG"
  python3 "$V6" --input "$input" --mode fast --output "$out" >> "$LOG" 2>&1
  ec=$?
  echo "V62_862_${label}_EXIT:$ec" >> "$LOG"
  echo "--- $label exit $ec $(date -u '+%H:%M:%S')" >> "$LOG"
}
for k in 45 70 100 145 178 285 515 1000; do
  run_one "hp35_n${k}" "pdac_862_hp35_n${k}.csv" "results_fast_v62_862_hp35_n${k}"
done
for k in 45 70 100 145 178 285 515 1000; do
  run_one "hp35nul_n${k}" "pdac_862_hp35nul_n${k}.csv" "results_fast_v62_862_hp35nul_n${k}"
done
for k in 45 70 100 145 178 285 515; do
  run_one "luad_n${k}" "pdac_862_luad_n${k}.csv" "results_fast_v62_862_luad_n${k}"
done
for k in 45 70 100 145 178; do
  run_one "tcga_n${k}" "pdac_862_tcga_n${k}.csv" "results_fast_v62_862_tcga_n${k}"
done
for k in 100 285 515; do
  run_one "hp35_stride_n${k}" "pdac_862_hp35_stride_n${k}.csv" "results_fast_v62_862_hp35_stride_n${k}"
done
V6_SHA_FIN=$(sha256sum "$V6" | cut -d' ' -f1)
echo "V6 SHA fin: $V6_SHA_FIN" >> "$LOG"
echo "=== LOT 862 REPRISE FIN $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" >> "$LOG"
