#!/usr/bin/env bash
# S-P3 ladder runner. Ordering rule (PREDICTIONS.md): Q1 before Q2; Q2 before Q3/Q4.
# Timeboxes per registered plan. Exit 124 from timeout = the registered TIMEOUT outcome.
cd "$(dirname "$0")"
LIB=../../lib/tessera_theory.pvl
run() { local f=$1 box=$2; local s=$(date +%s)
  timeout "$box" proverif -lib $LIB "$f.pv" > "$f.out" 2>&1; local rc=$?
  echo "$f rc=$rc seconds=$(( $(date +%s) - s )) box=$box" >> ladder.log; }
: > ladder.log
run sp3_q1_strict_dns_compromised 900
run sp3_q1_strict_repo_compromised 900
run sp3_q2_degraded_compromised 1800
run sp3_q3_companionA_frame_unbound 900
run sp3_q4_companionB_possession_unnamed 900
echo DONE >> ladder.log
# Q5 (added to the runner 2026-09-04 after Q1–Q4 completed; ordering rule: Q5 last; correct before companions)
run sp3_q5_multikey_correct 1800
run sp3_q5_multikey_companion_noFpB 1800
run sp3_q5_multikey_companion2_unboundB 1800
echo DONE-Q5 >> ladder.log
