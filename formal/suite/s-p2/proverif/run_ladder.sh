#!/usr/bin/env bash
# STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's.
# S-P2 ladder runner. Ordering rule (PREDICTIONS.md): Q1 before Q2; Q2 before Q3/Q4; Q5 last, C1 then C2 then C3.
# Timeboxes per registered plan (seconds). Exit 124 from timeout = the registered TIMEOUT outcome
# ("mechanism failure, not property evidence").
cd "$(dirname "$0")"
LIB=../../lib/tessera_theory.pvl
run() { local f=$1 box=$2; local s=$(date +%s)
  timeout "$box" proverif -lib $LIB "$f.pv" > "$f.out" 2>&1; local rc=$?
  echo "$f rc=$rc seconds=$(( $(date +%s) - s )) box=$box" >> ladder.log; }
: > ladder.log
run sp2_q1_strict_dns_compromised 900
run sp2_q1_strict_repo_compromised 900
run sp2_q2_degraded_compromised 1800
run sp2_q3_companion_cardinality_ignored 900
run sp2_q4_companion_slot_unbound 900
run sp2_q5_c1_fponly_frame_mh 1200
run sp2_q5_c2_fponly_frame_nomh 1200
run sp2_q5_c3_manifestposs_frame_nomh 1200
# Post-freeze addendum 1 (2026-09-12, Amendment 5 §A5.4; PREDICTIONS.md).
# Q6 is the AMENDED Q2 model itself (the three equalities, contentCh, ContentJudge,
# Spliced): re-run here under Q6's own registered 15-min box; it writes the same .out.
run sp2_q2_degraded_compromised 900
# Q6-C, the content-splicing companion, last.
run sp2_q6_companion_content_unchecked 900
echo DONE >> ladder.log
