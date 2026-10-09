#!/bin/bash
# ONE experiment, hard-capped.  Never two at once.
# usage: ./run1.sh <file.pv>
set -u
cd "$(dirname "$0")"
f="$1"; n="${f%.pv}"
blob=$(git hash-object "$f")
avail=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
echo "# START $(date -u +%FT%TZ) $n blob=$blob availMB=$avail" >> abl.log
s=$(date +%s)
( ulimit -v 10485760; /usr/bin/time -f %M -o "$n.rss" nice -n 19 timeout 3600 \
    proverif -lib /home/tony/projects/tessera/formal/suite/lib/tessera_theory.pvl "$f" > "$n.out" 2>&1 )
rc=$?
e=$(date +%s)
rss=$(tail -1 "$n.rss")
res=$(grep -c '^RESULT' "$n.out")
echo "$n rc=$rc seconds=$((e-s)) peakRSSkB=$rss results=$res blob=$blob availMB_at_start=$avail" | tee -a abl.log
grep -n '^RESULT\|^Error\|Out of memory\|Fatal error\|Stack overflow' "$n.out" | tail -5 | tee -a abl.log
echo "# END $(date -u +%FT%TZ)" >> abl.log
