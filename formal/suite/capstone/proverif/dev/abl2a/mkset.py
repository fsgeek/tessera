#!/usr/bin/env python3
"""Insert ProVerif solver settings / nounif declarations into the isolated
file WITHOUT touching the fixture, the verifier or the query."""
import sys
src, dst = sys.argv[1], sys.argv[2]
decls = sys.argv[3]
t = open(src).read()
anchor = "(* ==== model-local declarations (library terms are NOT redeclared) ==== *)"
assert t.count(anchor) == 1
t = t.replace(anchor,
    "(* ---- SOLVER SETTING UNDER TEST (step 3): no fixture, verifier or\n"
    "       query change whatsoever; only these lines are added. ---- *)\n"
    + decls.rstrip() + "\n\n" + anchor, 1)
open(dst, "w").write(t)
print("wrote", dst)
