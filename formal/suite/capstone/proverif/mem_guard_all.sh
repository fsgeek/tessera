#!/usr/bin/env bash
# STATUS: PROPOSED - 2026-09-20 - written by the owner instance (Claude Fable 5.1);
# not adopted; the commit is the author's.
#
# THE GENERAL MEMORY RULE for the capstone ladder, adopted by the owner instance
# 2026-09-20 18:35 UTC after the kernel OOM-killed three ProVerif runs that day
# (13:25, 15:47, 16:47 UTC; the last two triggered by the author's OTHER
# programs asking for memory).  It generalizes mem_guard.sh (capstone_d only):
#   every 30 s, if `free` shows available < 2500 MB, OR any ProVerif process
#   exceeds 24 GB resident, send SIGTERM (rc=143) to the LARGEST ProVerif process.
# A run so terminated is recorded by run_ladder.sh with rc=143 and its peak RSS,
# and is classified in RESULTS.md as MECHANISM FAILURE (memory), the registration
# boxing TIME and not MEMORY; the rule is stated so nobody judges at the edge and
# the kernel never chooses a victim unrecorded.  The 24 GB ceiling and the
# 2500 MB floor are scheduling, chosen so the author's desktop keeps headroom
# on a 31 GB machine; they change no box, model, query or prediction.
cd "$(dirname "$0")"
LOG=mem_guard_all.log
echo "# mem_guard_all armed $(date -u +%Y-%m-%dT%H:%M:%SZ): SIGTERM largest proverif iff availMB<2500 OR its rssKB>24000000" >> $LOG
while true; do
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  avail=$(free -m | awk 'NR==2{print $7}')
  line=$(ps -C proverif -o pid=,rss=,args= --sort=-rss 2>/dev/null | head -1)
  if [ -z "$line" ]; then
    echo "$ts availMB=$avail no proverif running" >> $LOG
    grep -q '^DONE' ladder.log && { echo "$ts ladder DONE; guard exits" >> $LOG; break; }
    sleep 30; continue
  fi
  pid=$(echo "$line" | awk '{print $1}'); rss=$(echo "$line" | awk '{print $2}'); f=$(echo "$line" | awk '{print $NF}')
  echo "$ts availMB=$avail largest=$f rssMB=$((rss/1024))" >> $LOG
  if [ "$avail" -lt 2500 ] || [ "$rss" -gt 24000000 ]; then
    echo "$ts TRIGGER MET (availMB=$avail<2500 OR rssKB=$rss>24000000) -- SIGTERM $pid ($f)" >> $LOG
    kill -TERM "$pid"
    sleep 20
  fi
  sleep 30
done
