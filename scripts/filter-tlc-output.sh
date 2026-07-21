#!/usr/bin/env bash
# Filter TLC `-continue` output down to its evidentiary core for
# committing: the run header, the FIRST violation block (error line +
# counterexample trace) for each distinct invariant, and the closing
# statistics. All later repetitions of an already-witnessed invariant
# are dropped — in a vacuity-witness run the evidence is "each witness
# fired, here is one state it fired on", and the full dump reproduces
# deterministically from the committed .tla + .cfg (record-norms ruling,
# Tony, 2026-07-21; adopted over git-LFS and compressed-binary options).
#
# Usage: tlc-command ... -continue ... | scripts/filter-tlc-output.sh
set -euo pipefail

awk '
  BEGIN { keep = 1; total = 0; dropped = 0 }
  /^Error: Invariant [A-Za-z0-9_]+ is violated\.?$/ {
    inv = $3; total++
    if (inv in seen) { keep = 0; dropped++ } else { seen[inv] = 1; keep = 1 }
  }
  /^[0-9]+ states generated/ {
    if (dropped > 0)
      printf "### filter-tlc-output.sh: %d further violation report(s) of already-witnessed invariants omitted; full output reproduces from the .cfg ###\n", dropped
    keep = 1
  }
  keep { print }
'
