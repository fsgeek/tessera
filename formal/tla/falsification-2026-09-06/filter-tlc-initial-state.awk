# STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted;
# the commit is the author's.
#
# Initial-state-aware variant of scripts/filter-tlc-output.sh, archived so the
# elided evidence file P5P6_TemporalRevocation_Sanity.out reproduces from
# recorded tooling (skeptic finding, 2026-09-06: the earlier elision was made
# by an unarchived one-off). The committed script keys on the line form
# `Error: Invariant X is violated.` and does not match TLC's stateless-model
# form `Error: Invariant X is violated by the initial state:`; this variant
# matches both, keeps the FIRST violation block per invariant, drops the rest,
# and prints the per-invariant counts from the raw stream plus the raw line
# count in the elision note. Whether to fold this into scripts/ is the
# author's call (outside formal/tla/).
#
# Usage: tlc ... -continue ... 2>&1 | awk -f filter-tlc-initial-state.awk
BEGIN { keep = 1; total = 0; dropped = 0; n = 0 }
/^Error: Invariant [A-Za-z0-9_]+ is violated( by the initial state:|\.)?$/ {
  inv = $3; total++; count[inv]++
  if (inv in seen) { keep = 0; dropped++ } else { seen[inv] = 1; order[++n] = inv; keep = 1 }
}
/^Finished computing initial states:/ || /^[0-9]+ states generated/ {
  if (dropped > 0 && !noted) {
    noted = 1
    printf "\n[... %d further violation report(s) of already-witnessed invariants elided from this\n", dropped
    printf " evidence file by falsification-2026-09-06/filter-tlc-initial-state.awk (the committed\n"
    printf " scripts/filter-tlc-output.sh keys on \"is violated.\" and does not match TLC's \"is violated\n"
    printf " by the initial state:\" form; noted in falsification-2026-09-06/FIXES-2026-09-06.md). The\n"
    printf " sanity methodology EXPECTS violations (vacuity witnesses). Per-invariant counts, from the\n"
    printf " raw stream of this run:\n"
    for (i = 1; i <= n; i++) printf "  %10d Invariant %s is violated\n", count[order[i]], order[i]
    printf " Raw output of this run: %d lines, not archived; reproduces from the .cfg. ...]\n\n", NR
  }
  keep = 1
}
keep { print }
