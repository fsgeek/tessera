#!/usr/bin/env bash
# Run each witness invariant of a witness cfg (IssuerLifecycleR53 witness cfg, e.g. IssuerLifecycleR53_ResidualBurst.cfg)
# (revision 5.3) as its OWN TLC run, stopping at the first
# violation. With ghosts on, an exhaustive -continue run of the whole witness
# set does not finish in minutes; a breadth-first run per witness stops at the
# shortest trace that reaches it. A witness that is NOT violated is reported
# as "UNREACHABLE (no error)" — that is the unhealthy result for a sanity
# witness and the "path absent" result for a residual witness.
#
# Usage: formal/tla/issuer-lifecycle/run-witnesses-r53.sh IssuerLifecycleR53_ResidualBurst.cfg
# Output: one block per witness on stdout (header line, the TLC error line,
# the trace, the statistics). Writes only under a mktemp -d directory.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
cfg="$here/$1"
jar="${TLA2TOOLS:-$HOME/.local/lib/tla2tools.jar}"
work="$(mktemp -d)"
# constants block, everything before INVARIANTS
head_part="$(sed -n '1,/^INVARIANTS/p' "$cfg" | sed '$d')"
mapfile -t invs < <(sed -n '/^INVARIANTS/,$p' "$cfg" | sed '1d' | awk 'NF && $1 !~ /^\\\*/ {print $1}')
cp "$here/IssuerLifecycleR53.tla" "$work/"
for inv in "${invs[@]}"; do
  printf '%s\nINVARIANTS\n  %s\n' "$head_part" "$inv" > "$work/W_$inv.cfg"
  echo "################ WITNESS $inv"
  meta="$(mktemp -d)"
  ( cd "$work" && java -XX:+UseParallelGC -cp "$jar" tlc2.TLC -workers auto -deadlock \
      -noGenerateSpecTE -metadir "$meta" -config "W_$inv.cfg" IssuerLifecycleR53.tla 2>&1 ) \
    | sed -n '/^Error: Invariant/,$p;/^Model checking completed/,$p' \
    | grep -v '^Error: The behavior up to this point is:$' || true
done
