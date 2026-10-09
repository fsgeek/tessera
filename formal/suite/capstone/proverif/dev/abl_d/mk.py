#!/usr/bin/env python3
"""Build isolated / ablated copies of DEGRADED (case d) companions.
Read-only on everything above dev/abl_d/: sources are read, outputs written here.

usage: mk.py <src.pv> <dst.pv> <qsel> [steps...] [+setting ...]
  qsel  : link1a | conj1 | conj2 | witness | all     (all = keep every query untouched)
  steps : 1 2 3 4  (the registered ablations, applied in the order given)
  +X    : a solver line inserted right after `set selFun = Term.` (or replacing it
          when X itself starts with 'set selFun')
"""
import sys, os

SRC = "/home/tony/projects/tessera/formal/suite/capstone/proverif"

Q = {
"link1a": """(* ---- THE ONE QUERY UNDER DIAGNOSIS: C-Q1 link 1a (1st in order) ---- *)
(* Every other query is deleted; NOTHING else in this file changes.      *)
query l: bitstring; event(ChainBroken(l, LINK_1A)).
""",
"conj1": """(* ---- THE ONE QUERY UNDER DIAGNOSIS: C-Q1 link 2b conjunct 1 -------- *)
(* Every other query is deleted; NOTHING else in this file changes.      *)
query aid: bitstring, lyr: bitstring, id: bitstring, fpA: bitstring,
      alg: bitstring, ver: bitstring;
  event(AcceptanceComplete(aid, lyr, authTuple(id, fpA, signers0, alg, ver)))
    ==> event(SlotSatisfied(aid, lyr, authTuple(id, fpA, signers0, alg, ver), fpA)).
""",
"witness": """(* ---- THE HONEST-FLOW WITNESSES ONLY (C-Q5w and C-N1), verbatim ------ *)
(* Every other query is deleted; NOTHING else in this file changes.      *)
(* Added 2026-09-29 by the resuming dev/abl_d agent.                     *)
query k1: pkey;
  event(HonestComplete(authTuple(issuerId, fp(pk(skI2)), signers0, algH, verH),
                       verified1(k1))).
query k1: pkey, k2: pkey;
  event(HonestComplete(authTuple(issuerId2, fp(pk(skI)), signers1(fp(pk(skB2))), algH, verH),
                       verified2(k1, k2))).
query t: bitstring; event(HonestChain(L0, t)).
query t: bitstring; event(HonestChain(L1, t)).
query t: bitstring; event(HonestChain(L2, t)).
query k: pkey, fb: bitstring; event(HonestAccepted(k, fb)).
query kH: pkey, fb: bitstring, kW: pkey; event(HonestWrappedAccepted(kH, fb, kW)).
query k: pkey, aid: bitstring; event(HonestStandingEstablished(k, aid)).
query a: bitstring, l: bitstring; event(HonestWrappedStandingAgreed(a, l)).
""",
"conj2": """(* ---- THE ONE QUERY UNDER DIAGNOSIS: C-Q1 link 2b conjunct 2 -------- *)
query aid: bitstring, lyr: bitstring, id: bitstring, fpA: bitstring,
      fpB: bitstring, alg: bitstring, ver: bitstring;
  event(AcceptanceComplete(aid, lyr, authTuple(id, fpA, signers1(fpB), alg, ver)))
    ==> event(SlotSatisfied(aid, lyr, authTuple(id, fpA, signers1(fpB), alg, ver), fpA)).
""",
}

def isolate(text, qsel):
    if qsel == "all":
        return text
    lines = text.split("\n")
    start = next(i for i,l in enumerate(lines) if l.startswith("(* ---- C-Q1 link 1a"))
    end = next(i for i,l in enumerate(lines) if "==== THE FIXTURE'S HONEST PROCESSES" in l)
    end -= 1  # the (* ===== *) rule line above the banner
    assert lines[end].startswith("(* ====="), lines[end]
    return "\n".join(lines[:start] + Q[qsel].split("\n") + lines[end:])

def sub(text, old, new, label):
    n = text.count(old)
    if n != 1:
        sys.exit("ABLATION %s: anchor occurs %d times: %r" % (label, n, old))
    sys.stderr.write("ablation %s applied\n" % label)
    return text.replace(old, new, 1)

def abl1(t):
    """ABLATION 1 -- drop the DEPTH-2 LAYER: the L1 -> L2 WrapStage and SUnwrap."""
    t = sub(t, "  | !WrapStage(pk(skS), L0, L1) | !WrapStage(pk(skS), L1, L2)",
               "  | !WrapStage(pk(skS), L0, L1)\n"
               "    (* ABLATION 1: !WrapStage(pk(skS), L1, L2) removed *)", "1a")
    t = sub(t, "  | !SUnwrap(L0, L1) | !SUnwrap(L1, L2)",
               "  | !SUnwrap(L0, L1)\n    (* ABLATION 1: !SUnwrap(L1, L2) removed *)", "1b")
    return t

def abl2(t):
    """ABLATION 2 -- drop skI2 (publication, honest-key/membership entries,
    ShipIssuer/RefuseIssuer).  M1 stays: the step names the key."""
    t = sub(t, "  out(c, pk(skI)); out(c, pk(skB2)); out(c, pk(skI2)); out(c, pk(skW));",
               "  out(c, pk(skI)); out(c, pk(skB2)); out(c, pk(skW));"
               "  (* ABLATION 2: pk(skI2) not published *)", "2a")
    t = sub(t, "  | !out(honestKeyCh, pk(skI2)) | !out(honestKeyCh, pk(skW))",
               "  | !out(honestKeyCh, pk(skW))  (* ABLATION 2 *)", "2b")
    t = sub(t, "  | !out(honestMemberCh, (pk(skI2), M1)) | !out(honestMemberCh, (pk(skW), MW))",
               "  | !out(honestMemberCh, (pk(skW), MW))  (* ABLATION 2 *)", "2c")
    t = sub(t, "  | !ShipIssuer(skI2, issuerId, M1, cvA) | !RefuseIssuer(skI2, issuerId, M1, cvA)",
               "  (* ABLATION 2: !ShipIssuer(skI2, ...) and !RefuseIssuer(skI2, ...) removed *)", "2d")
    return t

def abl3(t):
    """ABLATION 3 -- drop the SECOND LINEAGE SHAPE (RefuseIssuer's)."""
    a = "  | !ShipIssuer(skI, issuerId2, M2, cvA) | !RefuseIssuer(skI, issuerId2, M2, cvA)"
    t = sub(t, a, "  | !ShipIssuer(skI, issuerId2, M2, cvA)"
                  "  (* ABLATION 3: !RefuseIssuer(skI, ...) removed *)", "3a")
    b = "  | !ShipIssuer(skI2, issuerId, M1, cvA) | !RefuseIssuer(skI2, issuerId, M1, cvA)"
    if b in t:
        t = sub(t, b, "  | !ShipIssuer(skI2, issuerId, M1, cvA)"
                      "  (* ABLATION 3: !RefuseIssuer(skI2, ...) removed *)", "3b")
    return t

def abl4(text):
    """ABLATION 4 -- delete the |set| = 2 branch of AttestStage and WrapStage."""
    lines = text.split("\n"); out=[]; i=0; cuts=0
    while i < len(lines):
        l = lines[i]
        if l.lstrip().startswith("|") and ("the two-signer branch" in l
                                           or "the two-signer wrapper layer" in l):
            k = i
            while not lines[k].rstrip().endswith(")."):
                k += 1
            out += ["  (* ABLATION 4 (|set| = 2 branch): this stage's two-signer branch",
                    "     is deleted in full. *)", "  )."]
            i = k + 1; cuts += 1; continue
        out.append(l); i += 1
    if cuts != 2:
        sys.exit("ablation 4: expected 2 branch cuts, made %d" % cuts)
    sys.stderr.write("ablation 4 cut 2 branches\n")
    return "\n".join(out)

def setting(t, line):
    anchor = "set selFun = Term.\n"
    assert t.count(anchor) == 1
    if line.startswith("set selFun"):
        return t.replace(anchor, "(* dev/abl_d SOLVER SETTING: selFun replaced *)\n" + line + "\n", 1)
    return t.replace(anchor, anchor + "(* dev/abl_d SOLVER SETTING, added *)\n" + line + "\n", 1)

if __name__ == "__main__":
    src, dst, qsel = sys.argv[1:4]; rest = sys.argv[4:]
    t = open(os.path.join(SRC, src)).read()
    t = isolate(t, qsel)
    for s in rest:
        if s.startswith("+"):
            t = setting(t, s[1:])
        else:
            t = {"1": abl1, "2": abl2, "3": abl3, "4": abl4}[s](t)
    open(dst, "w").write(t)
