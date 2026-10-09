#!/bin/bash
# one smoke run: ulimit -v 10 GiB, nice 19, timeout 1800 s; logs rc, seconds, peak RSS
cd /home/tony/projects/tessera/formal/suite/capstone/proverif/ladder3-staging
f=$1; out=smoke/${2:-$(basename $f .pv)}.out
ulimit -v 10485760
s=$(date +%s)
/usr/bin/time -f "%M" -o $out.rss nice -n 19 timeout 1800 /home/tony/.local/bin/proverif -lib ../../../lib/tessera_theory.pvl $f > $out 2>&1
rc=$?
e=$(date +%s)
echo "$(date -u +%FT%TZ) file=$f rc=$rc secs=$((e-s)) peak_kb=$(cat $out.rss | tail -1) blob=$(git hash-object $f)" >> smoke/smoke.log
