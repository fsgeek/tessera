p='capstone.pv'; t=open(p).read()
def rep(old,new):
    global t
    assert t.count(old)==1, (t.count(old), old[:60])
    t=t.replace(old,new)

HDR = """\nset selFun = Term.

(* ==================================================================== *)
(* REPAIR 2026-10-01 (BF-5, BF-6; ladder 3) -- builder fixes after the  *)
(* cross-family review docs/reviews/2026-10-01-codex-review-capstone-   *)
(* build.md, findings 2 and 4, ACCEPTED by the owner instance as        *)
(* defects of this file.  Added by the AI collaborator (capstone        *)
(* builder, directed by the owner instance); not adopted; the commit    *)
(* is the author's.                                                     *)
(*                                                                      *)
(* BF-5: the standing path consumed ANY layer its own structural parse  *)
(* reached, so EstablishedWrapped could fire at an INTERMEDIATE wrapper *)
(* (review probe capstone_d_noninnermost_attest: wrapper -> wrapper ->  *)
(* attestation, established at L1).  StandingPath now proceeds only on  *)
(* the layer where its own structural descent has FINISHED.  No         *)
(* envelope event, check or success is consulted (E1).                  *)
(* BF-6: HonestStandingEstablished and HonestWrappedStandingAgreed are  *)
(* now emitted only at wrapped layers (lyr <> L0), as registered.       *)
(*                                                                      *)
(* The RECUT block above says every other line is byte-identical to    *)
(* the ladder-1 model; that described ladder 2 (blob a9fb7da1...).      *)
(* Under ladder 3 the lines marked BF-5 and BF-6 below also differ.     *)
(* This is a different blob and so a different model (section 8 item 2).*)
(* ==================================================================== *)
"""
rep("\nset selFun = Term.\n", HDR)

rep("""let StandingPath(pkDv: pkey, pkRv: pkey) =
  in(sStageCh, (intake: bitstring, lyr: bitstring, fbI: bitstring, sgI: bitstring,
                fbIB: bitstring, sgIB: bitstring));
""", """let StandingPath(pkDv: pkey, pkRv: pkey) =
  in(sStageCh, (intake: bitstring, lyr: bitstring, fbI: bitstring, sgI: bitstring,
                fbIB: bitstring, sgIB: bitstring));
  (* BF-5 REPAIR 2026-10-01 -- STRUCTURAL SELECTION OF THE INNERMOST LAYER.
     Registered: lyr "For C-Q6 ... is the **innermost** layer of the wrapped
     presentation" (PREDICTIONS.md:782); "(E4) Wrapped. lyr <> L0; at depth 2
     the innermost layer is L2" (:939-940); the wrapped flag is "the
     front-end's structural parse of the outer frame -- an OT_WRAPPER frame
     whose payload field is a wrap() term" (:942-944); and (E1) the standing
     path "computes over the innermost (t, ppf, sg, fb) that it extracts
     structurally, itself" (:892-894).  So a layer is innermost exactly when
     that SAME parse does NOT match its frame -- i.e. SUnwrap would not descend
     from it.  This is the complement of SUnwrap's own pattern and nothing
     more: no type check, no signature, no authority, and no envelope event or
     success (E1).  Before this repair StandingPath consumed every layer
     SUnwrap reached, so standing could establish at an intermediate wrapper
     (review finding 2, dev/codex/scratch/capstone_d_noninnermost_attest.out
     :3010).                                                                 *)
  let framed(=OT_WRAPPER, awi, iwi, kwi, mwi, cwi,
             wrap(cwii, (fbNA: bitstring, sgNA: bitstring,
                         fbNB: bitstring, sgNB: bitstring))) = fbI in 0
  else
""")

rep("""    ( in(designCh, (=kX, =aidD));
      event HonestStandingEstablished(kX, aidD) ).""",
"""    ( in(designCh, (=kX, =aidD));
      (* BF-6 REPAIR 2026-10-01: registered "HonestStandingEstablished over
         a **wrapped** presentation" (PREDICTIONS.md:1341); lyr is in scope
         here (estCh carries it), so the emission is guarded to wrapped
         layers, as StandingUnentitledWrapped's already is.  No query and no
         event signature changes.                                        *)
      if lyr <> L0 then event HonestStandingEstablished(kX, aidD) ).""")

rep("""      else ( in(designCh, (=k, =derived)); event HonestWrappedStandingAgreed(a, l) ) )""",
"""      (* BF-6 REPAIR 2026-10-01: the witness is registered for "an honest
         wrapped acceptance" (PREDICTIONS.md:1210-1212); emitted only at
         l <> L0.  The pair judge ScopeMisreported is NOT guarded.       *)
      else ( in(designCh, (=k, =derived));
             if l <> L0 then event HonestWrappedStandingAgreed(a, l) ) )""")
open(p,'w').write(t)
