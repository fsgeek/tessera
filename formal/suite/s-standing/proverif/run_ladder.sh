#!/usr/bin/env bash
# STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's.
# S-STANDING ladder runner. Ordering rule (PREDICTIONS.md): Q1 (both variants) before Q1d and before
# every companion; Q2, Q3, Q4 in any order after Q1; Q5 (B9 companion) last.
# Timeboxes per registered plan (Q1/Q1d 30 min; companions 15 min; Q5 given the companion box).
# Exit 124 from timeout = the registered TIMEOUT outcome (mechanism failure, not property evidence).
cd "$(dirname "$0")"
LIB=../../lib/tessera_theory.pvl
run() { local f=$1 box=$2; local s=$(date +%s)
  timeout "$box" proverif -lib $LIB "$f.pv" > "$f.out" 2>&1; local rc=$?
  echo "$f rc=$rc seconds=$(( $(date +%s) - s )) box=$box" >> ladder.log; }
: > ladder.log
run ss_q1_strict_dns_compromised 1800
run ss_q1_strict_repo_compromised 1800
run ss_q1d_degraded_compromised 1800
run ss_q2_companionA_identity_declared 900
run ss_q3_companionB_entitled_via_envelope 900
run ss_q4_companionC_terminal_unchecked 900
run ss_q5_companionD_reason_collapsed 900
echo DONE >> ladder.log
