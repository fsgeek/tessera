#!/bin/bash
# Sequential, ONE proverif at a time.  Waits for any running proverif of this dir first.
cd "$(dirname "$0")"
while pidof proverif >/dev/null; do sleep 5; done
landed() { grep -q '^RESULT' "$1.out"; }
# registered order on cc02_d link 1a: stop at the first landing
for f in A1_cc02d_1a A12_cc02d_1a A123_cc02d_1a A1234_cc02d_1a; do
  ./run1.sh $f.pv; landed $f && { echo "BREAK cc02d at $f" >> abl.log; break; }
done
# diagnostic control
./run1.sh X_cc02d_1a_wrapreverted.pv
# cc05_d link 2b conj 1: isolated baseline, then registered order
./run1.sh B0_cc05d_c1.pv
if ! landed B0_cc05d_c1; then
  for f in B1_cc05d_c1 B12_cc05d_c1 B123_cc05d_c1 B1234_cc05d_c1; do
    ./run1.sh $f.pv; landed $f && { echo "BREAK cc05d at $f" >> abl.log; break; }
  done
fi
echo CHAIN1 DONE >> abl.log
