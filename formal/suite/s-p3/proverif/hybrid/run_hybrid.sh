#!/usr/bin/env bash
# S-P3 hybrid ladder (2026-10-14). Correct model first, then companions. Exit 124 = TIMEOUT.
cd "$(dirname "$0")"
LIB=../../../lib/tessera_theory.pvl
run() { local f=$1 box=$2; local s=$(date +%s)
  timeout "$box" proverif -lib $LIB "$f.pv" > "$f.out" 2>&1; local rc=$?
  echo "$f rc=$rc seconds=$(( $(date +%s) - s )) box=$box" >> ladder.log; }
: > ladder.log
run sp3_h1_hybrid_correct 1800
run sp3_h2_companion_possession_unnamed_R 900
run sp3_h3_companion_unboundA_R 900
run sp3_h4_companion_single_rule 900
echo DONE >> ladder.log
