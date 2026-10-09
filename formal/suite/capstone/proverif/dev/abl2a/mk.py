#!/usr/bin/env python3
"""Build isolated / ablated copies for the link-2b-conjunct-1 diagnosis.
Read-only on everything above dev/abl2a/: sources are read, outputs written here.
"""
import sys, os

SRC = "/home/tony/projects/tessera/formal/suite/capstone/proverif"

TARGET_QUERY = """(* ---- THE ONE QUERY UNDER DIAGNOSIS ---------------------------------- *)
(* The 4th query in the capstone's declaration order: C-Q1 link 2b,      *)
(* conjunct 1 (the signers0 / |set| = 1 conjunct).  Every other query is *)
(* deleted; NOTHING else in this file changes.                           *)
query aid: bitstring, lyr: bitstring, id: bitstring, fpA: bitstring,
      alg: bitstring, ver: bitstring;
  event(AcceptanceComplete(aid, lyr, authTuple(id, fpA, signers0, alg, ver)))
    ==> event(SlotSatisfied(aid, lyr, authTuple(id, fpA, signers0, alg, ver), fpA)).
"""

def isolate(text):
    lines = text.split("\n")
    start = next(i for i,l in enumerate(lines) if l.startswith("(* ---- C-Q1 link 1a"))
    end = next(i for i,l in enumerate(lines) if "==== THE FIXTURE'S HONEST PROCESSES" in l)
    # back up over the banner line directly above it
    while not lines[end].startswith("(* ====="[:5]) or "FIXTURE" not in lines[end]:
        end -= 1
    end -= 1  # the (* ===== *) rule line above the banner
    return "\n".join(lines[:start] + TARGET_QUERY.split("\n") + lines[end:])

def sub(text, old, new, label):
    """Exact, single-occurrence substitution; aborts if the anchor is absent
    or ambiguous, so no ablation can silently remove more than it names."""
    n = text.count(old)
    if n != 1:
        sys.exit("ABLATION %s: anchor occurs %d times: %r" % (label, n, old))
    sys.stderr.write("ablation %s applied\n" % label)
    return text.replace(old, new, 1)


def abl1(t):
    """ABLATION 1 -- drop the DEPTH-2 LAYER.  Only the L1 -> L2 instantiations
    of WrapStage and SUnwrap go; L0 -> L1 stays, so depth 1 still runs."""
    t = sub(t,
        "  | !WrapStage(pk(skD), pk(skR), L0, L1) | !WrapStage(pk(skD), pk(skR), L1, L2)",
        "  | !WrapStage(pk(skD), pk(skR), L0, L1)\n"
        "    (* ABLATION 1: !WrapStage(pk(skD), pk(skR), L1, L2) removed *)",
        "1a (depth-2 wrapper stage)")
    t = sub(t,
        "  | !SUnwrap(L0, L1) | !SUnwrap(L1, L2)",
        "  | !SUnwrap(L0, L1)\n"
        "    (* ABLATION 1: !SUnwrap(L1, L2) removed *)",
        "1b (depth-2 standing unwrap)")
    return t


def abl2(t):
    """ABLATION 2 -- drop skI2.  Its publication and its three honest
    processes go.  M1 (which names fp(pk(skI2))) is LEFT IN PLACE: the
    ablation names the key, not the manifest."""
    t = sub(t,
        "  out(c, pk(skI)); out(c, pk(skB2)); out(c, pk(skI2)); out(c, pk(skW));",
        "  out(c, pk(skI)); out(c, pk(skB2)); out(c, pk(skW));"
        "  (* ABLATION 2: pk(skI2) not published *)",
        "2a (publication)")
    t = sub(t,
        "  | !out(honestKeyCh, pk(skI2)) | !out(honestKeyCh, pk(skW))",
        "  | !out(honestKeyCh, pk(skW))  (* ABLATION 2: skI2 honest key removed *)",
        "2b (honest key)")
    t = sub(t,
        "  | !out(honestMemberCh, (pk(skI2), M1)) | !out(honestMemberCh, (pk(skW), MW))",
        "  | !out(honestMemberCh, (pk(skW), MW))  (* ABLATION 2: skI2 membership removed *)",
        "2c (honest membership)")
    t = sub(t,
        "  | !ShipIssuer(skI2, issuerId, M1, cvA) | !RefuseIssuer(skI2, issuerId, M1, cvA)",
        "  (* ABLATION 2: !ShipIssuer(skI2, ...) and !RefuseIssuer(skI2, ...) removed *)",
        "2d (issuer processes)")
    return t


def abl3(t):
    """ABLATION 3 -- drop the SECOND LINEAGE SHAPE.  The fixture carries two
    terminal dispositions: ShipIssuer's lineage2(ABANDONED, SHIPPED) with
    TERM_SHIPPED, and RefuseIssuer's lineage2(ABANDONED, ABANDONED) with
    TERM_REFUSED (PREDICTIONS.md Sec 1.1, "both terminal dispositions present
    across the fixture").  The second shape is RefuseIssuer's; only the
    RefuseIssuer instantiations are removed, ShipIssuer's stay."""
    if "  | !ShipIssuer(skI, issuerId2, M2, cvA) | !RefuseIssuer(skI, issuerId2, M2, cvA)" in t:
        t = sub(t,
            "  | !ShipIssuer(skI, issuerId2, M2, cvA) | !RefuseIssuer(skI, issuerId2, M2, cvA)",
            "  | !ShipIssuer(skI, issuerId2, M2, cvA)"
            "  (* ABLATION 3: !RefuseIssuer(skI, ...) removed *)",
            "3a (skI refuse lineage)")
    if "  | !ShipIssuer(skI2, issuerId, M1, cvA) | !RefuseIssuer(skI2, issuerId, M1, cvA)" in t:
        t = sub(t,
            "  | !ShipIssuer(skI2, issuerId, M1, cvA) | !RefuseIssuer(skI2, issuerId, M1, cvA)",
            "  | !ShipIssuer(skI2, issuerId, M1, cvA)"
            "  (* ABLATION 3: !RefuseIssuer(skI2, ...) removed *)",
            "3b (skI2 refuse lineage)")
    return t


def abl4(t):
    return cut_branch(t)


def cut_branch(text):
    """ABLATION 4: delete the |set| = 2 branch from BOTH verifier stages.

    Both stages have the identical shape

        ( (* one-signer branch *)
          ( if ss = signers0 then ... ( out(...) | ... ) )
        | (* two-signer branch *)
          ( let signers1(kfprB) = ss in ... ( out(...) | ... ) ) ).

    so the cut runs from the `| (* ... two-signer ... *)` line through the
    stage's final `) ) ).` line, and the one-signer group is re-closed with
    `  ).`  (its own branch and out-group are already closed by the `) )` on
    its last line).
    """
    lines = text.split("\n")
    out, i, cuts = [], 0, 0
    while i < len(lines):
        l = lines[i]
        if l.lstrip().startswith("|") and ("the two-signer branch" in l
                                           or "the two-signer wrapper layer" in l):
            k = i
            while not lines[k].rstrip().endswith(")."):
                k += 1
            out.append("  (* ABLATION 4 (|set| = 2 branch): the two-signer branch of")
            out.append("     this stage is deleted in full -- the one-signer branch is")
            out.append("     now the stage's sole continuation. *)")
            out.append("  ).")
            i = k + 1
            cuts += 1
            continue
        out.append(l)
        i += 1
    if cuts != 2:
        sys.exit("ablation 4: expected 2 branch cuts, made %d" % cuts)
    sys.stderr.write("ablation 4 cut %d two-signer branches\n" % cuts)
    return "\n".join(out)


if __name__ == "__main__":
    src = sys.argv[1]; dst = sys.argv[2]; steps = sys.argv[3:]
    t = open(os.path.join(SRC, src)).read()
    t = isolate(t)
    for s in steps:
        t = {"1": abl1, "2": abl2, "3": abl3, "4": abl4}[s](t)
    open(dst, "w").write(t)
    print("wrote", dst)
