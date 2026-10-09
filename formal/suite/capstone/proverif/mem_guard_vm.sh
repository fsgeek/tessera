#!/usr/bin/env bash
# STATUS: PROPOSED - 2026-09-20 - written by the owner instance (Claude Fable 5.1);
# not adopted; the commit is the author's.
#
# THE MEMORY RULE ON THE SECOND MACHINE (ubuntu24 = wam-desktop, a Hyper-V guest
# with DYNAMIC memory, maximum 96 GB, on a 64-core Threadripper host).  The guest's
# MemTotal GROWS on demand (measured 2026-09-20: 6.7 GB -> 60 GB while a test
# process held 40 GB, never under ~2 GB available), so a low MemAvailable alone
# means "the balloon is still inflating", not "the machine is full".  The rule:
#   every 30 s, SIGTERM (rc=143) the LARGEST ProVerif process iff
#     (MemAvailable < 3000 MB AND MemTotal >= 90000 MB)   -- the ceiling is reached
#     OR that process's RSS > 80 GB.                     -- one run cannot own the box
# A run so terminated is logged by run_ladder.sh with rc=143 and its peak RSS and
# is classified in RESULTS.md as MECHANISM FAILURE (memory), the registration
# boxing TIME and not MEMORY.  Scheduling only: no box, model, query or prediction
# changes.  Every check is appended to mem_guard_vm.log.
cd "$(dirname "$0")"
LOG=mem_guard_vm.log
echo "# mem_guard_vm armed $(date -u +%Y-%m-%dT%H:%M:%SZ) on $(hostname): SIGTERM largest proverif iff (availMB<3000 AND totalMB>=90000) OR rssKB>80000000" >> $LOG
while true; do
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  avail=$(free -m | awk 'NR==2{print $7}'); total=$(free -m | awk 'NR==2{print $2}')
  line=$(ps -C proverif -o pid=,rss=,args= --sort=-rss 2>/dev/null | head -1)
  if [ -z "$line" ]; then
    echo "$ts totalMB=$total availMB=$avail no proverif running" >> $LOG
    grep -q '^DONE' ladder.log && { echo "$ts ladder DONE; guard exits" >> $LOG; break; }
    sleep 30; continue
  fi
  pid=$(echo "$line" | awk '{print $1}'); rss=$(echo "$line" | awk '{print $2}'); f=$(echo "$line" | awk '{print $NF}')
  n=$(pgrep -c -x proverif)
  echo "$ts totalMB=$total availMB=$avail proverifProcs=$n largest=$f rssMB=$((rss/1024))" >> $LOG
  if { [ "$avail" -lt 3000 ] && [ "$total" -ge 90000 ]; } || [ "$rss" -gt 80000000 ]; then
    echo "$ts TRIGGER MET (availMB=$avail totalMB=$total rssKB=$rss) -- SIGTERM $pid ($f)" >> $LOG
    kill -TERM "$pid"
    sleep 20
  fi
  sleep 30
done
