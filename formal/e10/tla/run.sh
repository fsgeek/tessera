#!/bin/bash
# E10 re-check harness (PROPOSED, 2026-10-26). TLC as formal/tla/E6a/run.sh finds it.
# The committed bridge module is found through -DTLA-Library and is not copied or edited.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
TLA_DIR="$(cd "$HERE/../../tla" && pwd)"
JAR="${TLA2TOOLS:-$HOME/.local/lib/tla2tools.jar}"
cd "$HERE" || exit 1
META="$(mktemp -d "${TMPDIR:-/tmp}/e10-meta.XXXXXX")"
tlc() { local out=$1 cfg=$2 mod=$3; shift 3
  java -XX:+UseParallelGC -Xmx10g -DTLA-Library="$TLA_DIR" -cp "$JAR" tlc2.TLC -deadlock -noGenerateSpecTE \
    -metadir "$(mktemp -d "$META/m.XXXXXX")" "$@" -config "$cfg" "$mod.tla" > "$out" 2>&1; }
mkcfg() { # mkcfg <file> <k-instance: k3|k6> <invariant...>
  local f=$1 inst=$2; shift 2
  { echo "CONSTANTS"
    if [ "$inst" = k3 ]; then
      printf '  MaxTime = 6\n  Delta = 2\n  Epsilon = 1\n  KConf = 3\n  DepthK = 2\n  MaxSkew = 2\n  MaxBlocks = 4\n'
    else
      printf '  MaxTime = 9\n  Delta = 2\n  Epsilon = 1\n  KConf = 6\n  DepthK = 5\n  MaxSkew = 1\n  MaxBlocks = 7\n'
    fi
    printf '\nINIT Init\nNEXT Next\n\nINVARIANTS\n'
    for i in "$@"; do echo "  $i"; done; } > "$f"; }
for inst in k3 k6; do
  mkcfg W_C2FailC3Pass_$inst.cfg $inst C2FailC3PassArtifactUnreachable
  tlc W_C2FailC3Pass_$inst.out W_C2FailC3Pass_$inst.cfg E10_BridgeRefuseC2 -workers 1
done
mkcfg S_C2FailNeverShipped_k3.cfg k3 C2FailNeverShipped
tlc S_C2FailNeverShipped_k3.out S_C2FailNeverShipped_k3.cfg E10_BridgeRefuseC2 -workers auto
if [ "${E10_FULL_K6:-0}" = 1 ]; then
  mkcfg S_C2FailNeverShipped_k6.cfg k6 C2FailNeverShipped
  tlc S_C2FailNeverShipped_k6.out S_C2FailNeverShipped_k6.cfg E10_BridgeRefuseC2 -workers auto
fi
rm -rf "$META"
