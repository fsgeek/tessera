#!/usr/bin/env bash
# STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
# adopted; the commit is the author's.
#
# PROBE — NON-DISCHARGING. Reproduces every .out in this directory from the
# committed .tla/.cfg files. Two run shapes:
#   single  — the cfg's whole INVARIANTS list in one TLC run (correct model,
#             reading variant): the expected result is green.
#   per-inv — one TLC run PER invariant in the cfg (sanity witnesses and
#             companions), because TLC reports only the FIRST violated
#             invariant for a given state even under -continue, so a
#             witness or companion invariant co-violated with an earlier-
#             listed one is silently never printed (RECUT 3, RESULTS-PROBE.md).
#             The .out is the concatenation of each run's evidentiary core:
#             the section header, the first violation (error line + trace)
#             or the "No error" line, and the state-count line.
# Timebox: 300 s per TLC run (PROBE.md); a timeout is recorded verbatim as
# "mechanism failure, not property evidence".
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../../.." && pwd)"
JAR="${TLA2TOOLS:-$HOME/.local/lib/tla2tools.jar}"
TLC=(java "-DTLA-Library=$REPO/formal/tla" -XX:+UseParallelGC -jar "$JAR" -workers 4)
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP" "$HERE/states"; rm -f "$HERE"/*_TTrace_*' EXIT  # TLC trace dumps are regenerable noise
cd "$HERE"

status_line() {  # first lines of every .out: label + which P4 module text was joined
  echo "### STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's. PROBE — NON-DISCHARGING."
  echo "### P4 join source: formal/tla/P4_VerifierStates.tla sha256=$(sha256sum "$REPO/formal/tla/P4_VerifierStates.tla" | cut -c1-16) HEAD=$(git -C "$REPO" rev-parse --short HEAD) working-tree=$(git -C "$REPO" diff --quiet -- formal/tla/P4_VerifierStates.tla && echo clean || echo modified-uncommitted)"
}

core() {  # trim a TLC output to its evidentiary core
  awk '
    /^Error: Invariant .* is violated/ { keep = 1 }
    /^Error: The behavior up to this point is:/ { keep = 1 }
    /^Model checking completed\. No error has been found\./ { print; next }
    /^Error: TLC threw|^Error: Parsing|^Semantic errors|Exception/ { print; keep = 1 }
    /^[0-9]+ states generated/ { print; keep = 0; next }
    /^Finished in / { print; next }
    keep { print }
  '
}

run_single() {  # module cfg
  local mod="$1" cfg="$2" out="${2%.cfg}.out"
  { status_line; echo "### run-probe.sh single: $mod with $cfg ($(date -u +%Y-%m-%dT%H:%MZ))";
    timeout 300 "${TLC[@]}" -config "$cfg" "$mod.tla" 2>&1; echo "### exit=$?"; } > "$out"
  grep -E "^Error: Invariant|No error has been found|### exit" "$out" | sed "s|^|$out: |"
}

run_perinv() {  # module cfg
  local mod="$1" cfg="$2" out="${2%.cfg}.out"
  local invs; invs=$(awk '/^INVARIANTS/{f=1;next} f && NF {print $1}' "$cfg")
  { status_line; echo "### run-probe.sh per-invariant: $mod with $cfg ($(date -u +%Y-%m-%dT%H:%MZ))";
    echo "### one TLC run per invariant; each section is that run's evidentiary core";
    for inv in $invs; do
      printf 'INIT Init\nNEXT Next\nINVARIANT %s\n' "$inv" > "$TMP/$inv.cfg"
      echo; echo "### ---- $mod / $inv ----"
      timeout 300 "${TLC[@]}" -config "$TMP/$inv.cfg" "$mod.tla" 2>&1 | core
      rc=${PIPESTATUS[0]}; [ "$rc" = 124 ] && echo "### TIMEOUT at 300 s — mechanism failure, not property evidence"
      echo "### exit=$rc"
    done; } > "$out"
  grep -E "^### ---- |^Error: Invariant|No error has been found" "$out" | sed "s|^|$out: |"
}

run_single P10_ManifestAuthority            P10_ManifestAuthority.cfg
run_perinv P10_ManifestAuthority            P10_ManifestAuthority_Sanity.cfg
run_single P10_ManifestAuthority_A32Reading P10_ManifestAuthority_A32Reading.cfg
run_perinv P10_ManifestAuthority_A32Reading P10_ManifestAuthority_A32Reading_Sanity.cfg   # added 2026-09-06 (later still): vacuity witnesses on the reading variant (PROBE.md post-run note 3 item 3)
run_perinv P10_ManifestAuthority_A121Literal P10_ManifestAuthority_A121Literal.cfg   # added 2026-09-06 (later): O1 made reproducible
for n in BrokenSilent BrokenSelfCounted BrokenAnchorIgnored BrokenAnyOne; do
  run_perinv "P10_ManifestAuthority_$n" "P10_ManifestAuthority_$n.cfg"
done
