#!/bin/bash
# DIAGNOSTIC (not an experiment): manual 6.7.2's procedure -- set verboseRules
# = true on a short capped run; the clause stream goes to the scratchpad, only
# a summary is kept here (diag_summary.log).
cd "$(dirname "$0")"
src="$1"; tag="$2"; box="${3:-300}"
SP=/tmp/claude-1000/-home-tony-projects-tessera/4bb3083e-03e6-42f4-8a0b-ece54c8af197/scratchpad
python3 mk.py "$src" "$tag.pv" "${4:-link1a}" "+set verboseRules = true." 2>/dev/null
echo "# DIAG START $(date -u +%FT%TZ) $tag blob=$(git hash-object $tag.pv) box=${box}s" >> abl.log
s=$(date +%s)
( ulimit -v 10485760; nice -n 19 timeout "$box" \
    proverif -lib /home/tony/projects/tessera/formal/suite/lib/tessera_theory.pvl "$tag.pv" 2>&1 | head -c 3000000000 > "$SP/$tag.out" )
echo "# DIAG END $(date -u +%FT%TZ) $tag secs=$(( $(date +%s)-s )) bytes=$(stat -c%s $SP/$tag.out)" >> abl.log
{ echo "== $tag ($src, ${4:-link1a} only, verboseRules, box ${box}s) secs=$(( $(date +%s)-s ))"
  grep '^RESULT' "$SP/$tag.out" || echo "no RESULT"
  grep 'rules inserted' "$SP/$tag.out" | tail -1
  awk '/^Rule with/{getline r; n++; if (r ~ /dsks/) d++; if (r ~ /mess\(stageCh/) s++; if (r~/mess\(stageCh/ && r~/dsks/) sd++; if (r ~ /-> mess\(stageCh/) cs++} END{printf "clauses=%d with_dsks=%d (%.0f%%) with_stageCh=%d stageCh_and_dsks=%d concl_stageCh=%d\n", n, d, 100*d/n, s, sd, cs}' "$SP/$tag.out"
  grep '^Rule with hypothesis fact' "$SP/$tag.out" | sed -E 's/^Rule with hypothesis fact [0-9]+ selected: //' | sed -E 's/^(attacker|mess)\(([a-zA-Z_0-9]+)\(\(?([A-Za-z_0-9]*).*/\1 \2 \3/; s/^mess\(([a-zA-Z_0-9]+)\[\],.*/mess \1/' | sort | uniq -c | sort -rn | head -8
} | tee -a diag_summary.log
