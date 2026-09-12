#!/usr/bin/env bash
# S-P7 ladder runner. STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's.
# Ordering rule (PREDICTIONS.md): Q1 before Q2; Q2 before Q3, Q4, Q6; Q5 and Q5c last.
# Timeboxes are the registered ones (seconds). Exit 124 from timeout = the registered TIMEOUT outcome
# ("mechanism failure, not property evidence"). Unregistered runs are marked as such.
cd "$(dirname "$0")"
LIB=/home/tony/projects/tessera/formal/suite/lib/tessera_theory.pvl
PV=/home/tony/.local/bin/proverif
run() { local f=$1 box=$2 note=$3; local s=$(date +%s)
  timeout "$box" $PV -lib $LIB "$f.pv" > "$f.out" 2>&1; local rc=$?
  echo "$f rc=$rc seconds=$(( $(date +%s) - s )) box=$box $note" >> ladder.log; }
: > ladder.log
run sp7_q1_strict_dns_compromised        900  "(Q1, strict, DNS leaked)"
run sp7_q1_strict_repo_compromised       900  "(Q1, strict, repo leaked)"
run sp7_q2_degraded_compromised          1800 "(Q2, the C2 claim)"
run sp7_q3_companion_type_unchecked      900  "(Q3 companion; required red: TypeConfused)"
run sp7_q4_companion_reserialize_twoversion 900 "(Q4 companion, two-version; required red: HonestWrappedAccepted unreachable)"
run sp7_q4_companion_reserialize_isolation  900 "(Q4 isolation config; required: HonestWrappedAccepted reachable)"
run sp7_q4_control_opaque_twoversion     900  "(UNREGISTERED added control: opaque wrapper, two versions)"
run sp7_q4_probe_degraded_twoversion     900  "(UNREGISTERED probe: mutated wrapper, degraded mode)"
run sp7_q6a_companion_identity_outermost 900  "(Q6a companion; required red: Rescoped)"
run sp7_q6b_companion_key_outermost      900  "(Q6b companion; required red: Rescoped AND InnerSigTransplanted)"
run sp7_q5_depth2_correct                2700 "(Q5 correct, depth 2)"
run sp7_q5c_companion_one_level_in       2700 "(Q5c companion; required red: RescopedD2 only)"
echo DONE >> ladder.log
