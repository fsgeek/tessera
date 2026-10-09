#!/bin/bash
# EXPLORATORY PROBE 2026-10-04 — non-discharging; not part of any registration
# usage: run_lemma.sh TAG LEMMA TIMEOUT MEMMAX [extra tamarin args...]
# Logs one line per attempt to runs/attempts.tsv:
#   tag lemma wall_s peak_rss_kb rc outcome command
set -u
cd "$(dirname "$0")"
TAG=$1; LEMMA=$2; TO=$3; MEM=$4; shift 4
MODEL=${MODEL:-cap_cc02_d.spthy}
OUT=runs/$TAG.$LEMMA.out
CMD="tamarin-prover $* --prove=$LEMMA $MODEL --output=runs/$TAG.$LEMMA.proof.spthy"
START=$(date +%s.%N)
systemd-run --user --scope -q -p MemoryMax=$MEM -p MemorySwapMax=0 \
  /usr/bin/time -f "PEAKRSS_KB %M WALL %e" -o runs/$TAG.$LEMMA.time \
  timeout $TO $HOME/.local/bin/tamarin-prover "$@" --prove=$LEMMA $MODEL \
     --output=runs/$TAG.$LEMMA.proof.spthy > $OUT 2>&1
RC=$?
END=$(date +%s.%N)
WALL=$(python3 -c "print(round($END-$START,1))")
RSS=$(grep -o 'PEAKRSS_KB [0-9]*' runs/$TAG.$LEMMA.time | awk '{print $2}')
RES=$(grep -E "^  $LEMMA \(" $OUT | sed 's/^ *//')
if [ -z "$RES" ]; then
  if [ $RC -eq 124 ]; then RES="TIMEOUT"; elif [ $RC -eq 137 ] || [ $RC -eq 143 ] || grep -q -i "out of memory\|heap" $OUT; then RES="OOM (cgroup MemoryMax=$MEM kill) rc=$RC"; else RES="ERROR rc=$RC"; fi
fi
printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$TAG" "$LEMMA" "$WALL" "${RSS:-NA}" "$RC" "$RES" "$CMD" >> runs/attempts.tsv
echo "$TAG $LEMMA $WALL s rss=${RSS:-NA}KB rc=$RC :: $RES"
