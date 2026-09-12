#!/usr/bin/env bash
# S-P7 ablation runner. STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's.
# UNREGISTERED runs: none of these is evidence for any property; they locate which checks carry Q2's results
# (S-P3 F5/F7 pattern) and which confusion routes Q3's mutation opens (p01). Same run() idiom as ../run_ladder.sh:
# every run is wrapped in `timeout <box>`; exit 124 = the registered TIMEOUT outcome ("mechanism failure, not
# property evidence"). Box 1800 s for the Q2 ablations (Q2's registered box), 900 s for the Q3 probe (Q3's).
# Each log line carries a green/RED summary per query, in the order the RESULT lines appear in the .out.
# Added 2026-09-06 after the skeptic review of RESULTS.md (the first ablation runs were made by hand and only
# their log survived); a17/a18 added by the same review.
cd "$(dirname "$0")"
LIB=/home/tony/projects/tessera/formal/suite/lib/tessera_theory.pvl
PV=/home/tony/.local/bin/proverif
summary() {  # "green Ev" for `is true`, "RED Ev" for `is false`, per RESULT line
  sed -n 's/^RESULT not event(\([A-Za-z0-9]*\)(.*)) is \(true\|false\)\.$/\1 \2/p' "$1" \
  | awk '{ printf "%s %s ", ($2=="true" ? "green" : "RED"), $1 }'; }
run() { local f=$1 box=$2; local s=$(date +%s)
  timeout "$box" $PV -lib $LIB "$f.pv" > "$f.out" 2>&1; local rc=$?
  echo "$f rc=$rc seconds=$(( $(date +%s) - s )) box=$box :: $(summary "$f.out")" >> ablations.log; }
runraw() { local f=$1 box=$2; local s=$(date +%s)   # p01: the per-route RESULT lines verbatim
  timeout "$box" $PV -lib $LIB "$f.pv" > "$f.out" 2>&1; local rc=$?
  echo "$f rc=$rc seconds=$(( $(date +%s) - s )) box=$box :: $(grep '^RESULT' "$f.out" | tr '\n' ' ')" >> ablations.log; }
: > ablations.log
for a in a01_no_id_match a02_no_kfp_match a03_no_id_no_kfp a04_no_mh a05_no_id_no_mh a06_no_kfp_no_mh \
         a07_no_slot a08_no_inner_poss a09_no_kfp_no_slot a10_no_wrapper_type a11_no_inner_sig \
         a12_no_inner_evidence a13_no_outer_kfp a14_no_kfp_no_slot_no_mh a15_no_id_no_kfp_no_mh_no_slot \
         a16_no_inner_sig_no_kfp a17_no_slot_no_mh a18_kfp_only; do run "$a" 1800; done
runraw p01_q3_routes 900
echo DONE >> ablations.log
