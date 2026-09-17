#!/bin/bash
cd "$(dirname "$0")"
J="java -XX:+UseParallelGC -Xmx12g -cp $HOME/.local/lib/tla2tools.jar tlc2.TLC -workers auto -deadlock"
BASE="MaxTime = 9
  Delta = 2
  Epsilon = 1
  KConf = 6
  DepthK = 5
  MaxSkew = 1
  MaxBlocks = 7"
mk(){ n=$1; shift 1; { echo "CONSTANTS"; echo "  $BASE"; echo; echo "INIT Init"; echo "NEXT Next"; echo; echo "INVARIANTS"; for i in "$@"; do echo "  $i"; done; } > $n.cfg; }
run(){ n=$1; m=$2; rm -rf st-$n; echo "START $n $(date +%T)" >> bridge2.log; $J -metadir st-$n -config $n.cfg $m.tla > $n.out 2>&1; echo "END $n $(date +%T) | $(grep -o 'Invariant [A-Za-z]* is violated' $n.out | sort -u | tr '\n' ';') | $(grep 'states generated' $n.out)" >> bridge2.log; }
for w in NonMonotonicShipUnreachable WallClockDivergenceUnreachable BurialGapUnreachable ShipUnreachable LateBurialArtifactUnreachable EpsilonSideUnreachable; do mk W_$w $w; run W_$w P5cP5P6_Bridge; done
mk C_AnchorSubst_Corr ShippedDesignatedAgree; run C_AnchorSubst_Corr P5cP5P6_Bridge_BrokenAnchorSubst
mk C_AnchorSubst_Late LateBurialRejected; run C_AnchorSubst_Late P5cP5P6_Bridge_BrokenAnchorSubst
mk C_AnchorSubst_Green PinAgreement HonestShipAccepted; run C_AnchorSubst_Green P5cP5P6_Bridge_BrokenAnchorSubst
mk C_WallClock_Red HonestShipAccepted; run C_WallClock_Red P5cP5P6_Bridge_BrokenWallClock
mk C_WallClock_Green PinAgreement ShippedDesignatedAgree LateBurialRejected; run C_WallClock_Green P5cP5P6_Bridge_BrokenWallClock
echo DONE > bridge2.done
