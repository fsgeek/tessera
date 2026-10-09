#!/usr/bin/env bash
# STATUS: PROPOSED - 2026-09-19 - produced by the AI collaborator (Claude Opus 5,
# builder, directed by the owner instance); not adopted; the commit is the author's.
#
# The MECHANICAL MEMORY TRIGGER for capstone_d, pre-authorized by the owner
# instance on 2026-09-19 so that nobody judges at the edge.
#
# THE RULE, verbatim in effect: let capstone_d run to its registered box
# (1095 min) UNLESS `free` shows available < 1 GB AND swap free < 1 GB, with
# capstone_d the ONLY ProVerif process; at that point terminate it with SIGTERM
# (rc=143) and classify the run in RESULTS.md as MECHANISM FAILURE (memory),
# stating that the registration boxes TIME and not MEMORY, and apply section 3's
# ablation order as if the box had expired, with the memory figures beside it.
# DO NOT WAIT FOR THE KERNEL: a kernel OOM kill yields no rc line, no
# classification and no record.
#
# The pattern is ANCHORED (`^proverif`) on purpose: the unanchored form also matches
# the `timeout` WRAPPER, whose RSS is ~2 MB, and killing the wrapper would orphan the
# ProVerif process rather than terminate it.
#
# Every check is appended to mem_guard.log, so a reader can see that the rule
# was applied mechanically and not by anyone's judgement.
cd "$(dirname "$0")"
LOG=mem_guard.log
echo "# mem_guard armed $(date -u +%Y-%m-%dT%H:%M:%SZ): SIGTERM capstone_d iff availMB<1024 AND swapfreeMB<1024 AND it is the only proverif process" >> $LOG
while true; do
  dpid=$(pgrep -f "^proverif .*capstone_d\.pv" | head -1)
  ts=$(date -u +%H:%M:%S)
  if [ -z "$dpid" ]; then
    echo "$ts capstone_d no longer running; guard exits without firing" >> $LOG
    break
  fi
  n=$(pgrep -x proverif | wc -l)
  avail=$(free -m | awk 'NR==2{print $7}')
  swapfree=$(free -m | awk 'NR==3{print $4}')
  rss=$(ps -o rss= -p "$dpid" | tr -d ' ')
  echo "$ts availMB=$avail swapfreeMB=$swapfree proverifProcs=$n capstone_d_rssMB=$((rss/1024))" >> $LOG
  if [ "$n" -eq 1 ] && [ "$avail" -lt 1024 ] && [ "$swapfree" -lt 1024 ]; then
    echo "$ts TRIGGER MET (availMB=$avail<1024 AND swapfreeMB=$swapfree<1024 AND proverifProcs=1) -- sending SIGTERM to $dpid" >> $LOG
    kill -TERM "$dpid"
    # Mark it so run_ladder.sh does NOT simply rerun the same file: under the
    # owner instance's rule this is a MECHANISM FAILURE (memory), and section
    # 3's ablation order applies as if the box had expired.
    echo "terminated by mem_guard at $ts: availMB=$avail swapfreeMB=$swapfree rssMB=$((rss/1024))" > capstone_d.mechfail
    echo "$ts SIGTERM sent; wrote capstone_d.mechfail; the wrapper will write rc=143 to ladder.log" >> $LOG
    break
  fi
  sleep 30
done
