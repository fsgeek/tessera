# Scratch (prereg_scratch): derives the A8.4 files. SRC.pv -> a84_SRC.pv.
# (1) header comment line prepended; (2) every query declaration replaced by a comment
# (slice.py's regex); (3) BLOCK inserted before the REQUIRED-retained-queries comment line.
# Nothing else changes.
import re, sys
ANCHOR = '(* ---- the REQUIRED retained queries'
BLOCK = '''(* ---- A8.4 — standing key = the key the innermost acceptance verified under *)
(* Joined on intake aid, layer lyr, the evidenced tuple t, slot A (the slot   *)
(* argument is t's kfpr) and the signature TERM sg of the standing core.     *)
query aid: bitstring, lyr: bitstring, id: bitstring, kf: bitstring, ss: bitstring,
      al: bitstring, vr: bitstring, kS: pkey, ppf: bitstring, sg: bitstring,
      dcl: bitstring, ev: bitstring, kV: pkey, ppfV: bitstring, fb: bitstring;
  event(EstablishedWrapped(aid, lyr, authTuple(id, kf, ss, al, vr), kS,
          attemptCore(authTuple(id, kf, ss, al, vr), ppf, sg, dcl), ESTABLISHED))
  && event(LayerAccepted(aid, lyr, authTuple(id, kf, ss, al, vr), ev, kf, kV, ppfV, sg, fb))
  ==> kS = kV.
(* ---- A8.4w — vacuity witness: both events, same join, same key; REACHABLE *)
query aid: bitstring, lyr: bitstring, id: bitstring, kf: bitstring, ss: bitstring,
      al: bitstring, vr: bitstring, kS: pkey, ppf: bitstring, sg: bitstring,
      dcl: bitstring, ev: bitstring, ppfV: bitstring, fb: bitstring;
  event(EstablishedWrapped(aid, lyr, authTuple(id, kf, ss, al, vr), kS,
          attemptCore(authTuple(id, kf, ss, al, vr), ppf, sg, dcl), ESTABLISHED))
  && event(LayerAccepted(aid, lyr, authTuple(id, kf, ss, al, vr), ev, kf, kS, ppfV, sg, fb)).

'''
src, out = sys.argv[1:3]
txt = open(src).read()
n0 = len(re.findall(r'(?m)^query\b', txt))
txt, nq = re.subn(r'(?ms)^query\b.*?\.[ \t]*$', '(* query deleted for A8.4 *)', txt)
assert nq == n0 and txt.count(ANCHOR) == 1
txt = txt.replace(ANCHOR, BLOCK + ANCHOR)
hdr = f"(* A8.4 DERIVED FILE from {src.split('/')[-1]}: {nq} query declarations deleted; the A8.4 query and its witness added; no process, declaration or set line changed *)\n"
open(out, 'w').write(hdr + txt)
print(out, nq)
