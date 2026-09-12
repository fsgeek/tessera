#!/usr/bin/env bash
# STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's.
# S-P1 ablation probes (unregistered; discharge nothing): runs each probe
# inside a 30 min box, writes <probe>.out, appends "probe rc seconds box"
# to probes.log. p7 runs against the total-exclusive-ownership-failure
# library copy lib_total_eo_failure.pvl; p1–p6 against the suite library.
# rc=124 = timeout = "mechanism failure, not property evidence".
# Added 2026-09-06 (skeptic nit: probes.log carried no timing field);
# the original probe runs were made by hand with the same commands.
set -u
cd "$(dirname "$0")"
LIB=/home/tony/projects/tessera/formal/suite/lib/tessera_theory.pvl
PV=/home/tony/.local/bin/proverif
NOTE="${1:-}"
LABEL="# STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's."
[ -f probes.log ] || echo "$LABEL" > probes.log   # label line emitted when the log is created (added 2026-09-06, skeptic pass 2)
run() {
  local m="$1" box="$2" lib="$3"
  local t0=$(date +%s)
  timeout "$box" "$PV" -lib "$lib" "$m.pv" > "$m.out" 2>&1
  local rc=$?
  local t1=$(date +%s)
  echo "$m rc=$rc seconds=$((t1-t0)) box=$box${NOTE:+ ($NOTE)}" >> probes.log
}
run p1_no_fp_check            1800 "$LIB"
run p2_no_possession          1800 "$LIB"
run p3_no_manifest_hash       1800 "$LIB"
run p4_frame_unpinned         1800 "$LIB"
run p5_no_authority_evidence  1800 "$LIB"
run p6_no_attestation_sig     1800 "$LIB"
run p7_total_eo_failure       1800 "$(pwd)/lib_total_eo_failure.pvl"
echo "DONE" >> probes.log
