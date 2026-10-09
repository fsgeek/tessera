#!/usr/bin/env bash
# STATUS: PROPOSED - 2026-09-19 - produced by the AI collaborator (Claude Opus 5,
# builder, directed by the owner instance); not adopted; the commit is the author's.
#
# The capstone ladder runner.  Pattern: s-standing/proverif/run_ladder.sh.
# Exit 124 from `timeout` = the registered TIMEOUT outcome (a mechanism-viability
# failure, evidence about the tool or the encoding and NEVER about the property;
# disposed by PREDICTIONS.md §3's ablation order, never by raising the box).
#
# ORDERING RULE (PREDICTIONS.md §3): "C-Q1's links before every companion;
# (a), (b), (d) before (c); C-Q7, C-Q8, C-Q9 before links 3 and 4 and before
# C-Q6."  The last clause is a QUERY order and is honoured by the declaration
# order inside capstone.pv.  The first two are RUN order and are honoured here:
# the three correct-form runs complete (a barrier) before any companion starts,
# and case (c) - which IS companion C-C1 - runs after them.
#
# TIMEBOXES (PREDICTIONS.md §3 "Timeboxes declared").  Each .pv here carries
# EVERY registered query of its case, so each run is given the PER-CASE SUM of
# the registered boxes: 1185 min for a strict case (27 entries), 1095 min for
# the degraded case (which asserts neither C-Q1 link 1b nor C-Q2).  Because the
# whole-model wall clock is an upper bound on every query's own time, a run that
# finishes under 30 minutes is inside the smallest registered box for every
# query it carries; run_ladder.sh records the seconds so that can be checked.
# No companion carries a box of its own (§4, "The count"): it runs inside the
# box of the query it is predicted to red, and a fortiori inside the sum.
#
# PARALLELISM (scheduling only; no box, model, query or prediction changes).
# JOBS was 6 and is now 3, at the owner instance's instruction after the
# 19:11:24 UTC memory event: 12 cores is not this machine's limit, 31 GB is.
# A companion's ProVerif process grows to 3-9 GB -- eight concurrent runs took
# the machine to 0 GB available and 5.4 GB of swap, and the kernel OOM killer
# would have chosen a victim for us within minutes, at random and unrecorded.
# Each run still gets its own process and its own `timeout`, so no run's box is
# shortened by another's.
#
# KILLED RUNS ARE RERUN.  A ladder.log line whose rc is 137 (SIGKILL) or 143
# (SIGTERM) records a run that was killed, not a result.  It STAYS in the log as
# history, and the file is run again -- the skip guard below ignores such lines.
# Any other logged rc means the run landed, and the file is skipped.
#
# PEAK MEMORY is recorded per run (`/usr/bin/time -f %M`, kB) so a reader can see
# what each companion cost in memory as well as in seconds.

cd "$(dirname "$0")"
LIB=../../lib/tessera_theory.pvl
JOBS=${JOBS:-3}
BOX_STRICT=$((1185 * 60))
BOX_DEGRADED=$((1095 * 60))

# ladder.log is APPENDED to: a file whose run is already logged is skipped, so
# the ladder can be resumed without re-running what has landed.
touch ladder.log
echo "# capstone ladder — $(date -u +%Y-%m-%dT%H:%M:%SZ) — ProVerif 2.05 — -lib $LIB" >> ladder.log
echo "# model: capstone.pv blob $(git hash-object capstone.pv)" >> ladder.log

box_for() { case "$1" in *_d.pv) echo $BOX_DEGRADED ;; *) echo $BOX_STRICT ;; esac; }

TIMER=$(command -v /usr/bin/time || true)

run() {
  local f=$1 box; box=$(box_for "$f")
  # A file marked as a MECHANISM FAILURE is not rerun unablated: section 3's
  # ablation order applies to it instead, and that is a judgement recorded in
  # RESULTS.md, not something this runner makes.
  if [ -f "${f%.pv}.mechfail" ]; then
    echo "${f%.pv} rc=MECHFAIL-MEMORY seconds=0 box=${box}s note=$(tr -d '\n' < "${f%.pv}.mechfail")" >> ladder.log
    return 0
  fi
  # skip only if this file has a logged run that was NOT killed (137/143)
  # Skip only if this file has at least one logged run that was NOT killed.
  # (Written as three stages on purpose: `grep -qv` on EMPTY input returns 0 on
  # this system, so the two-stage form would have skipped every unrun file.)
  if grep -E "^${f%.pv} rc=" ladder.log | grep -vE "rc=(137|143) " | grep -q .; then
    return 0
  fi
  local s=$(date +%s) rc rss="?"
  if [ -n "$TIMER" ]; then
    "$TIMER" -f %M -o "${f%.pv}.rss" timeout "$box" proverif -lib $LIB "$f" > "${f%.pv}.out" 2>&1
    rc=$?
    rss=$(tail -1 "${f%.pv}.rss" 2>/dev/null)
  else
    timeout "$box" proverif -lib $LIB "$f" > "${f%.pv}.out" 2>&1
    rc=$?
  fi
  echo "${f%.pv} rc=$rc seconds=$(( $(date +%s) - s )) peakRSSkB=${rss:-?} box=${box}s blob=$(git hash-object "$f")" >> ladder.log
}

wave() {   # run the named files, at most $JOBS at a time, then wait for THIS
           # wave's jobs only (a bare `wait` would also block on the case (c)
           # and case (d) runs that deliberately proceed alongside).
  local n=0; local pids=()
  for f in "$@"; do
    [ -f "$f" ] || { echo "${f%.pv} rc=MISSING seconds=0 box=0s" >> ladder.log; continue; }
    # 2026-09-20 (owner instance, scheduling only): a file that has already landed
    # is skipped HERE, before it is counted, so that JOBS counts RUNNING jobs.  Before
    # this line the counter counted skipped files too, and on resume a big companion
    # sitting beside two landed files ran alone; the first hour on ubuntu24 showed it.
    if [ ! -f "${f%.pv}.mechfail" ] && grep -E "^${f%.pv} rc=" ladder.log | grep -vE "rc=(137|143) " | grep -q .; then continue; fi
    run "$f" & pids+=($!)
    n=$((n+1))
    if [ $((n % JOBS)) -eq 0 ]; then wait "${pids[@]}" 2>/dev/null; pids=(); fi
  done
  if [ ${#pids[@]} -gt 0 ]; then wait "${pids[@]}" 2>/dev/null; fi
  return 0
}

# ---- 1. the correct-form runs.  Cases (a) and (b) are the BARRIER for every
#         companion: C-Q1's links land here before any of them starts.
wave capstone.pv capstone_b.pv
echo "# wave 1 complete (correct form, cases a and b)" >> ladder.log

# ---- 2. case (d), the degraded correct-form run, in a slot of its own: it
#         reaches ~9-12 GB resident and the case-(d) companions must wait for
#         it (the ordering rule).  Skipped if it has already landed.
wave capstone_d.pv
echo "# correct form, case d, complete" >> ladder.log

# ---- 3. the companions, case (a).  JOBS=3, for memory (see the header).
wave $(ls cap_cc*_a.pv 2>/dev/null | sort)
echo "# wave 3 complete (companions, case a)" >> ladder.log

# ---- 4. the companions, case (b)
wave $(ls cap_cc*_b.pv 2>/dev/null | sort)
echo "# wave 4 complete (companions, case b)" >> ladder.log

# ---- 5. the companions, case (d)
wave $(ls cap_cc*_d.pv 2>/dev/null | sort)
echo "# wave 5 complete (companions, case d)" >> ladder.log

# ---- 6. CASE (c) LAST, AND ALONE, WITH THE WHOLE MACHINE.  It is the largest
#         process in the suite -- over 20 GB resident before it was terminated
#         at 3 of 47 queries -- so it is not run in a wave and shares with
#         nothing.  It is also companion C-C1, so the ordering rule
#         "(a), (b), (d) before (c)" puts it here anyway.  If it cannot finish
#         alone within its box or within memory, that is a MECHANISM FAILURE
#         under the same rule and section 3's ablation order applies to it.
run cap_cc01_c.pv
echo "# wave 6 complete (case c = C-C1, run alone)" >> ladder.log

echo DONE >> ladder.log
