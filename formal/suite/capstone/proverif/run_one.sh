#!/usr/bin/env bash
# One-file run with run_ladder.sh's exact logging line (owner instance, 2026-09-28).
cd "$(dirname "$0")"; f=$1; box=$2; s=$(date +%s)
/usr/bin/time -f %M -o "${f%.pv}.rss" timeout "$box" $HOME/.local/bin/proverif -lib ../../lib/tessera_theory.pvl "$f" > "${f%.pv}.out" 2>&1; rc=$?
echo "${f%.pv} rc=$rc seconds=$(( $(date +%s) - s )) peakRSSkB=$(tail -1 "${f%.pv}.rss") box=${box}s blob=$(git hash-object "$f")" >> ladder.log
