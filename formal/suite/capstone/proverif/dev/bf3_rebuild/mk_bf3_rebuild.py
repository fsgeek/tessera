#!/usr/bin/env python3
# STATUS: PROPOSED - 2026-10-01 - written by the AI collaborator (Claude Opus 5.5,
# capstone builder, directed by the owner instance); not adopted; the commit is
# the author's.  DIAGNOSTIC SCRATCH, NOT A LADDER RESULT.
#
# REPAIR 2026-10-01, skeptic S-12.  Rebuilds the pre-BF-3 model (the defect
# RESULTS.md *Broken fixtures* BF-3 describes) from files in the tree, so that
# BF-3's evidence, whose .out files were deleted on 2026-09-19, can be re-made:
#
#   1. ladder-1 capstone.pv = current capstone.pv minus the 34-line RECUT R-9
#      block (lines 45-78); asserted to hash to c6969b4c... (ladder 1's blob);
#   2. the BF-3 repair undone: the Front reads ONLY (fbA, sgA, fbB, sgB) from c,
#      and the envelope path (AttestStage, WrapStage) and the standing path each
#      read their own (t, ev, k, ppf, ...) from the public channel c, as the
#      printed initial process of dev/first.out (blob 508b9018...) shows.  The
#      three reads are written exactly as derive.py's degraded() still matches
#      them (derive.py:184-191, the pre-BF-3 source lines it was written
#      against), so degraded() rewrites them to the sole `ev` unaided.  The
#      Front's original source formatting and comment are not recoverable; its
#      printed process is (first.out:406);
#   3. case (d) derived with derive.py's own degraded(), nothing else.  No
#      `set selFun` line: ProVerif 2.05's default selection function, as the
#      original pre-BF-3 runs used.
#
# Checks printed: the step-1 hash; that degraded(step 1) hashes to ladder 1's
# capstone_d blob d4f0851d... (ladder1/ladder.log:25), i.e. the derivation path
# is the ladder's; and the hashes of the two written files.
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, PV)
import derive  # noqa: E402  (main() runs only under __main__)


def blob(text):
    b = text.encode()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


cur = open(os.path.join(PV, "capstone.pv")).read().split("\n")
assert cur[44].startswith("(* =====") and cur[45].startswith("(* RECUT 2026-09-24"), cur[44:46]
assert cur[76] == "set selFun = Term." and cur[77] == "", cur[76:78]
l1 = "\n".join(cur[:44] + cur[78:])
assert blob(l1) == "c6969b4cc2f2e30be7a7a950af7609ea75e4c700", blob(l1)
assert blob(derive.degraded(l1)) == "d4f0851db6cd81e760c5cb847664b558a194911c", blob(derive.degraded(l1))

EDITS = [
    # the Front: one read of frames and signatures only; nothing forwarded
    ("""  (* ONE read of the presented bundle: the frames and signatures of the
     outermost object, the per-layer verification material for L0, L1 and L2,
     and the standing path's core and standing evidence.  Everything a path
     uses below comes from THIS read.                                          *)
  in(c, (fbA: bitstring, sgA: bitstring, fbB: bitstring, sgB: bitstring,
         t0: bitstring, ev0D: bitstring, ev0R: bitstring,
         kA0: pkey, ppfA0: bitstring, kB0: pkey, ppfB0: bitstring,
         t1: bitstring, ev1D: bitstring, ev1R: bitstring,
         kA1: pkey, ppfA1: bitstring, kB1: pkey, ppfB1: bitstring,
         t2: bitstring, ev2D: bitstring, ev2R: bitstring,
         kA2: pkey, ppfA2: bitstring, kB2: pkey, ppfB2: bitstring,
         coreIn: bitstring, seIn: bitstring));""",
     """  in(c, (fbA: bitstring, sgA: bitstring, fbB: bitstring, sgB: bitstring));""", 1),
    ("""  | out(sStageCh, (aid, L0, fbA, sgA, fbB, sgB))
  | !out(envMat, (aid, L0, t0, ev0D, ev0R, kA0, ppfA0, kB0, ppfB0))
  | !out(envMat, (aid, L1, t1, ev1D, ev1R, kA1, ppfA1, kB1, ppfB1))
  | !out(envMat, (aid, L2, t2, ev2D, ev2R, kA2, ppfA2, kB2, ppfB2))
  | !out(stdMat, (aid, L0, t0, ev0D, ev0R, kA0, ppfA0, kB0, ppfB0))
  | !out(stdMat, (aid, L1, t1, ev1D, ev1R, kA1, ppfA1, kB1, ppfB1))
  | !out(stdMat, (aid, L2, t2, ev2D, ev2R, kA2, ppfA2, kB2, ppfB2))
  | !out(standCore, (aid, coreIn, seIn)) ).""",
     """  | out(sStageCh, (aid, L0, fbA, sgA, fbB, sgB)) ).""", 1),
    # AttestStage
    ("""  in(envMat, (=aid, =lyr, t: bitstring, evD: bitstring, evR: bitstring,
              kA: pkey, ppfA: bitstring, kB: pkey, ppfB: bitstring));""",
     """  in(c, (t: bitstring, evD: bitstring, evR: bitstring,
         kA: pkey, ppfA: bitstring, kB: pkey, ppfB: bitstring));""", 1),
    # WrapStage
    ("""  in(envMat, (=aid, =lyrIn, t: bitstring, evD: bitstring, evR: bitstring,
              kA: pkey, ppfA: bitstring, kB: pkey, ppfB: bitstring));""",
     """  in(c, (t: bitstring, evD: bitstring, evR: bitstring,
         kA: pkey, ppfA: bitstring, kB: pkey, ppfB: bitstring));""", 1),
    # the standing path
    ("""  in(stdMat, (=intake, =lyr, t: bitstring, evD: bitstring, evR: bitstring,
              kX: pkey, ppfI: bitstring, kBs: pkey, ppfBs: bitstring));
  in(standCore, (=intake, core: bitstring, se: bitstring));""",
     """  in(c, (t: bitstring, evD: bitstring, evR: bitstring, kX: pkey,
         ppfI: bitstring, core: bitstring, se: bitstring));""", 1),
]
old = l1
for a, b, n in EDITS:
    assert old.count(a) == n, (old.count(a), a[:60])
    old = old.replace(a, b)

old_d = derive.degraded(old)
open(os.path.join(HERE, "capstone_pre_bf3.pv"), "w").write(old)
open(os.path.join(HERE, "capstone_d_pre_bf3.pv"), "w").write(old_d)
print("ladder-1 text      ", blob(l1))
print("degraded(ladder-1) ", blob(derive.degraded(l1)))
print("capstone_pre_bf3   ", blob(old))
print("capstone_d_pre_bf3 ", blob(old_d))
