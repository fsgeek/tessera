# EXPLORATORY PROBE 2026-10-04 — non-discharging; not part of any registration
# (run with: bash run.sh ...)
# usage: run.sh MEMMAX BOXSEC JOBS file1.pv file2.pv ...   (paths under gen/)
# Runs as a pool of JOBS concurrent jobs (xargs -P). Each run: its own systemd user scope (MemoryMax, no swap), `timeout`, /usr/bin/time %M.
cd "$(dirname "$0")"
LIB=../../../../lib/tessera_theory.pvl
MEM=$1 BOX=$2 JOBS=$3; shift 3
mkdir -p out
one() {
  local f=$1 b; b=$(basename "$f" .pv); local s=$(date +%s.%N)
  systemd-run --user --scope -q -p MemoryMax=$MEM -p MemorySwapMax=0 \
    /usr/bin/time -f %M -o out/$b.rss timeout $BOX nice -n 10 ~/.local/bin/proverif -lib $LIB "$f" > out/$b.out 2>&1
  local rc=$?; local e=$(date +%s.%N)
  local res=$(grep -E '^RESULT' out/$b.out | sed 's/^RESULT //' | tr '\n' ' ')
  local tr=$(grep -c 'A trace has been found' out/$b.out)
  echo "$b rc=$rc wall=$(printf '%.1f' $(echo "$e-$s"|bc)) peakRSSkB=$(tail -1 out/$b.rss 2>/dev/null) mem=$MEM box=${BOX}s traceFound=$tr blob=$(git hash-object $f) result=[$res]" >> runs.log
}
export -f one; export LIB MEM BOX
printf '%s\n' "$@" | xargs -P "$JOBS" -I{} bash -c 'one "$1"' _ {}
