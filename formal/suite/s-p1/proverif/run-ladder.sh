#!/usr/bin/env bash
# STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's.
# S-P1 ladder: runs each registered model inside its registered timebox,
# writes <model>.out, appends "model rc seconds box" to ladder.log.
# rc=124 = timeout = "mechanism failure, not property evidence".
set -u
cd "$(dirname "$0")"
LIB=/home/tony/projects/tessera/formal/suite/lib/tessera_theory.pvl
PV=/home/tony/.local/bin/proverif
NOTE="${1:-}"
LABEL="# STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's."
[ -f ladder.log ] || echo "$LABEL" > ladder.log   # label line emitted when the log is created (added 2026-09-06, skeptic pass 2)
run() {
  local m="$1" box="$2"
  local t0=$(date +%s)
  timeout "$box" "$PV" -lib "$LIB" "$m.pv" > "$m.out" 2>&1
  local rc=$?
  local t1=$(date +%s)
  echo "$m rc=$rc seconds=$((t1-t0)) box=$box${NOTE:+ ($NOTE)}" >> ladder.log
}
# Ordering rule (PREDICTIONS.md): Q1 both variants, then Q2, then Q3, then Q4.
run sp1_q1_strict_dns_compromised   900
run sp1_q1_strict_repo_compromised  900
run sp1_q2_degraded_compromised    1800
run sp1_q3_companionA_sig_unbound   900
run sp1_q4_companionB_frame_unsigned 900
echo "DONE" >> ladder.log
