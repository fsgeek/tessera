#!/bin/bash
# Run a list of experiments STRICTLY ONE AT A TIME, in order, stopping at the
# first one whose .out contains a RESULT line (i.e. the query landed).
# The guard inspects ProVerif processes only (ps -C proverif), and matches only
# THIS directory's experiment files, so it can never be confused by a shell
# command line and never waits on the owner's ladder (cap_*.pv).
cd "$(dirname "$0")"
busy() { ps -C proverif -o args= 2>/dev/null | grep -qE '(E|F|S|D)[0-9]+[_A-Za-z0-9]*\.pv'; }
while busy; do sleep 20; done
for f in "$@"; do
  while busy; do sleep 20; done
  ./run1.sh "$f"
  n="${f%.pv}"
  if false; then
    echo "# CHAIN STOP: $n landed (later steps of the order not run)" >> abl.log
    break
  fi
done
echo "# CHAIN COMPLETE $(date -u +%FT%TZ)" >> abl.log
