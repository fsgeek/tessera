#!/usr/bin/env bash
cd "$(dirname "$0")"
ulimit -v 16777216
echo "# recut_pre chain $(date -u +%FT%TZ) ulimit -v 16GiB, nice 19, one at a time, box 71100s" >> chain.log
for f in cap_cc07ii_a_selfun cap_cc07i_a_selfun cap_cc14_a_selfun; do
  s=$(date +%s)
  /usr/bin/time -f %M -o $f.rss nice -n 19 timeout 71100 proverif -lib ../../../../lib/tessera_theory.pvl $f.pv > $f.out 2>&1
  rc=$?
  echo "$f rc=$rc seconds=$(( $(date +%s) - s )) peakRSSkB=$(tail -1 $f.rss) blob=$(git hash-object $f.pv) results=$(grep -c '^RESULT' $f.out)" >> chain.log
done
echo DONE >> chain.log
