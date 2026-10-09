#!/usr/bin/env python3
# STATUS: PROPOSED - 2026-09-19 - produced by the AI collaborator (Claude Opus 5,
# builder, directed by the owner instance); not adopted; the commit is the author's.
#
# derive.py - generates every case and companion .pv file of the capstone from
# capstone.pv by the smallest mechanical delta, as PREDICTIONS.md's freeze
# statement (3) and the builder's brief require.  Each generated file carries a
# header naming: its STATUS, what it mutates, which registered prediction it
# serves, and the registered box.  Nothing here edits capstone.pv.
#
#   python3 derive.py            # writes the files beside this script
#
# The four compromise cases (PREDICTIONS.md §1.1):
#   (a) strict, skD (DNS) public          - capstone.pv itself
#   (b) strict, skR (repository) public   - one line
#   (c) strict, BOTH public               - one line; this case IS companion C-C1
#   (d) degraded, sole channel public     - the mode delta below
#
# Every companion is a named list of exact-string edits applied inside a named
# block of the model, so that the delta can be read off this file and checked
# against the generated .pv by diff.

import os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(HERE, "capstone.pv")).read()

# ---------------------------------------------------------------- blocks ----
# Block boundaries are the model's own section comments, so a mutation can be
# confined to (for example) the two-signer branch of the attestation layer.
MARKS = {
    "ATTEST1": ("(* ---------------- the one-signer branch ---------------- *)",
                "(* ---------------- the two-signer branch ---------------- *)"),
    "ATTEST2": ("(* ---------------- the two-signer branch ---------------- *)",
                "(* ==== THE WRAPPER LAYER"),
    "WRAP1":   ("(* ---------------- the one-signer wrapper layer ---------------- *)",
                "(* ---------------- the two-signer wrapper layer ---------------- *)"),
    "WRAP2":   ("(* ---------------- the two-signer wrapper layer ---------------- *)",
                "(* ==== THE STANDING PATH"),
    "STAND":   ("let StandingPath(",
                "(* ==== THE JUDGES"),
    "DECIDE":  ("let StandingDecide(kT: pkey",
                "let StandingPath("),
    "AUTH":    ("(* --- the two authority channels",
                "(* --- an honest attester"),
    "ALL":     (None, None),
}
BLOCKGROUPS = {
    "ATTEST": ["ATTEST1", "ATTEST2"],
    "WRAP":   ["WRAP1", "WRAP2"],
    "LAYERS": ["ATTEST1", "ATTEST2", "WRAP1", "WRAP2"],
}


def edit(text, block, old, new, count=None):
    """Replace `old` by `new` everywhere inside `block`.  At least one block of a
    group must contain it; fails loudly if none does."""
    blocks = BLOCKGROUPS.get(block, [block])
    total = 0
    for b in blocks:
        s, e = MARKS[b]
        i = 0 if s is None else text.index(s)
        j = len(text) if e is None else text.index(e, i)
        seg = text[i:j]
        total += seg.count(old)
        text = text[:i] + seg.replace(old, new) + text[j:]
    if total == 0:
        raise SystemExit("derive.py: not found in %s: %r" % (block, old[:70]))
    if count is not None and total != count:
        raise SystemExit("derive.py: %d occurrences (wanted %d) in %s: %r"
                         % (total, count, block, old[:70]))
    return text


def drop(text, block, line):
    """Delete a whole source line (matched by its stripped prefix).  A line may
    be absent from some blocks of a group (the one-signer branches have no slot
    B); at least one block must contain it."""
    blocks = BLOCKGROUPS.get(block, [block])
    total = 0
    for b in blocks:
        s, e = MARKS[b]
        i = 0 if s is None else text.index(s)
        j = len(text) if e is None else text.index(e, i)
        seg = text[i:j]
        keep = []
        for ln in seg.split("\n"):
            if ln.strip().startswith(line):
                total += 1
                continue
            keep.append(ln)
        text = text[:i] + "\n".join(keep) + text[j:]
    if total == 0:
        raise SystemExit("derive.py: no line starting %r in %s" % (line, block))
    return text


def qdrop(text, needle):
    """Delete a registered query (the comment line through the blank line)."""
    i = text.index(needle)
    j = text.index("\n\n", i)
    return text[:i] + text[j + 1:]


# --------------------------------------------------- the compromise cases ---
LEAK_A = ("  (* CASE (a): STRICT, DNS channel compromised "
          "— its signing key is public *)\n  out(c, skD);")


def case(text, which):
    if which == "a":
        return text
    if which == "b":
        return text.replace(LEAK_A,
            "  (* CASE (b): STRICT, repository channel compromised "
            "— its signing key is public *)\n  out(c, skR);", 1)
    if which == "c":
        return text.replace(LEAK_A,
            "  (* CASE (c): STRICT, BOTH channel keys public.  This case IS "
            "companion C-C1 *)\n  out(c, skD); out(c, skR);", 1)
    raise SystemExit("bad case " + which)


# --------------------------------------------------------- degraded mode ---
# capstone_d.pv is a DOCUMENTED COPY: the sole-channel form of the same model.
# The transformation is the list below and nothing else; `diff capstone.pv
# capstone_d.pv` shows exactly it.
def degraded(text):
    t = text
    # --- header
    t = t.replace("capstone.pv — THE COMPOSED MODEL. Case (a): STRICT, DNS channel",
                  "capstone_d.pv — THE COMPOSED MODEL. Case (d): DEGRADED, sole channel", 1)
    t = t.replace("(* compromised.                                                        *)",
                  "(* compromised.  Derived from capstone.pv by derive.py's degraded()     *)\n"
                  "(* transformation; a documented copy, see RESULTS.md.                   *)", 1)
    # --- queries that C-Q1-degraded / §3 do NOT assert in (d)
    t = qdrop(t, "(* ---- C-Q1 link 1b — authority -> tuple (correspondence, STRICT only) - *)")
    t = qdrop(t, "(* ---- C-Q2 — the §A3.2.1 boundary judge, PAIR FORM (D9) -------------- *)")
    # conjunct 1's UNRESTRICTED form is not asserted in (d); the honest-key forms are
    t = t.replace(
        "query aid: bitstring, lyr: bitstring, t: bitstring, kX: pkey, co: bitstring;\n"
        "  event(EstablishedWrapped(aid, lyr, t, kX, co, ESTABLISHED))\n"
        "    ==> event(Designated(kX, h(co))).\n",
        "(* conjunct 1's UNRESTRICTED form is NOT asserted in (d): S-STANDING's own\n"
        "   unrestricted correspondence is registered red in degraded mode (L-18),\n"
        "   the A4.6 cost.  The honest-key forms below ARE asserted. *)\n", 1)
    # the retained unrestricted acceptance query takes its degraded name AcceptS
    t = t.replace(
        "query evD: bitstring, evR: bitstring, t: bitstring, k: pkey, fb: bitstring;\n"
        "  event(Accept(evD, evR, t, k, fb)) ==> event(IssuerSigned(k, fb)).",
        "query ev: bitstring, t: bitstring, k: pkey, fb: bitstring;\n"
        "  event(AcceptS(ev, t, k, fb)) ==> event(IssuerSigned(k, fb)).", 1)
    # --- the front end's ONE read of the bundle, and the per-layer material
    #     it forwards: one evidence term per layer, not §1.3's pair
    for n in ("0", "1", "2"):
        t = t.replace("ev%sD: bitstring, ev%sR: bitstring," % (n, n), "ev%s: bitstring," % n)
        t = t.replace(", ev%sD, ev%sR," % (n, n), ", ev%s," % n)
    t = t.replace("t: bitstring, evD: bitstring, evR: bitstring,\n              kA: pkey",
                  "t: bitstring, ev: bitstring,\n              kA: pkey")
    t = t.replace("t: bitstring, evD: bitstring, evR: bitstring,\n              kX: pkey",
                  "t: bitstring, ev: bitstring,\n              kX: pkey")
    # --- the sole authority channel
    t = t.replace(
        "let AuthorityDNS(skDp: skey, t: bitstring) =\n"
        "  event AuthorityPublishedDNS(t);\n"
        "  out(c, sign((STMT_DIGEST, h(t)), skDp)).\n"
        "\n"
        "let AuthorityRepo(skRp: skey, t: bitstring) =\n"
        "  event AuthorityPublishedRepo(t);\n"
        "  out(c, sign((STMT_DIGEST, h(t)), skRp)).",
        "let AuthorityS(skSp: skey, t: bitstring) =\n"
        "  event AuthorityPublishedDNS(t);\n"
        "  out(c, sign((STMT_DIGEST, h(t)), skSp)).", 1)
    # --- the verifier: ONE evidence check, ev the sole term
    t = t.replace("(pkDv: pkey, pkRv: pkey", "(pkSv: pkey")
    t = t.replace(
        "  let (=STMT_DIGEST, =h(t)) = checksign(evD, pkDv) in\n"
        "  let (=STMT_DIGEST, =h(t)) = checksign(evR, pkRv) in",
        "  let (=STMT_DIGEST, =h(t)) = checksign(ev, pkSv) in")
    t = t.replace(
        "  event AuthorityEvidence(t, evD, pkDv);\n"
        "  event AuthorityEvidence(t, evR, pkRv);",
        "  event AuthorityEvidence(t, ev, pkSv);")
    t = t.replace("  in(c, (t: bitstring, evD: bitstring, evR: bitstring,\n"
                  "         kA: pkey, ppfA: bitstring, kB: pkey, ppfB: bitstring));",
                  "  in(c, (t: bitstring, ev: bitstring,\n"
                  "         kA: pkey, ppfA: bitstring, kB: pkey, ppfB: bitstring));")
    t = t.replace("  in(c, (t: bitstring, evD: bitstring, evR: bitstring, kX: pkey,\n"
                  "         ppfI: bitstring, core: bitstring, se: bitstring));",
                  "  in(c, (t: bitstring, ev: bitstring, kX: pkey,\n"
                  "         ppfI: bitstring, core: bitstring, se: bitstring));")
    t = t.replace("t, (evD, evR),", "t, ev,")
    t = t.replace("event Accept(evD, evR, t, kA, fbA);", "event AcceptS(ev, t, kA, fbA);")
    t = t.replace("event Accept(evD, evR, t, kB, fbB);", "event AcceptS(ev, t, kB, fbB);")
    t = t.replace("out(link1aCh, (lyr, t, evD, evR))", "out(link1aCh, (lyr, t, ev))")
    t = t.replace("out(link1aCh, (lyrIn, t, evD, evR))", "out(link1aCh, (lyrIn, t, ev))")
    t = t.replace("      | out(twoWorldsCh, (evD, evR, t))\n", "")
    # --- link 1a's judge over the SOLE carried term
    t = t.replace(
        "let Link1aJudge(pkSv: pkey) =\n"
        "  in(link1aCh, (lyr: bitstring, t: bitstring, evD: bitstring, evR: bitstring));\n"
        "  ( ( let (=STMT_DIGEST, =h(t)) = checksign(evD, pkDv) in 0\n"
        "      else ( let (=STMT_DIRECT, =t) = checksign(evD, pkDv) in 0\n"
        "             else event ChainBroken(lyr, LINK_1A) ) )\n"
        "  | ( let (=STMT_DIGEST, =h(t)) = checksign(evR, pkRv) in 0\n"
        "      else ( let (=STMT_DIRECT, =t) = checksign(evR, pkRv) in 0\n"
        "             else event ChainBroken(lyr, LINK_1A) ) ) ).",
        "let Link1aJudge(pkSv: pkey) =\n"
        "  in(link1aCh, (lyr: bitstring, t: bitstring, ev: bitstring));\n"
        "  ( let (=STMT_DIGEST, =h(t)) = checksign(ev, pkSv) in 0\n"
        "    else ( let (=STMT_DIRECT, =t) = checksign(ev, pkSv) in 0\n"
        "           else event ChainBroken(lyr, LINK_1A) ) ).", 1)
    # C-Q2's judge is not stated in (d); its channel loses its only writer too
    t = t.replace(
        "let TwoWorldsJudge =\n"
        "  in(twoWorldsCh, (e1: bitstring, e2: bitstring, t1: bitstring));\n"
        "  in(twoWorldsCh, (=e1, =e2, t2: bitstring));\n"
        "  if t1 = t2 then 0 else event TwoWorldsBroken(e1, e2, t1, t2).",
        "(* C-Q2 is stated for (a) and (b) only (§3); its judge is not built here. *)", 1)
    t = t.replace("  | !TwoWorldsJudge | !ChainWitnessJudge", "  | !ChainWitnessJudge")
    # --- the fixture: one channel
    t = t.replace("  new skD: skey; new skR: skey; new skAdv: skey;",
                  "  new skS: skey; new skAdv: skey;", 1)
    t = t.replace("  out(c, pk(skD)); out(c, pk(skR));", "  out(c, pk(skS));", 1)
    t = t.replace(LEAK_A,
        "  (* CASE (d): DEGRADED, the SOLE authority channel compromised "
        "— its signing key is public *)\n  out(c, skS);", 1)
    t = t.replace(
        "  | !AuthorityDNS(skD, M1) | !AuthorityDNS(skD, M2) | !AuthorityDNS(skD, MW)\n"
        "  | !AuthorityRepo(skR, M1) | !AuthorityRepo(skR, M2) | !AuthorityRepo(skR, MW)",
        "  | !AuthorityS(skS, M1) | !AuthorityS(skS, M2) | !AuthorityS(skS, MW)", 1)
    t = t.replace("(pk(skD), pk(skR))", "(pk(skS))")
    t = t.replace("!WrapStage(pk(skD), pk(skR), L0, L1) | !WrapStage(pk(skD), pk(skR), L1, L2)",
                  "!WrapStage(pk(skS), L0, L1) | !WrapStage(pk(skS), L1, L2)")
    # the enrolment rule in degraded: the sole channel is the compromised one
    t = t.replace("insufficient for strict acceptance at L0", "the SOLE channel in (d), which is the A4.6 cost")
    return t


# ------------------------------------------------------- the companions -----
# Each entry: (name, row/served, box minutes, cases, edit function).
FPIN_A = "let framed(otA, =alg, =id, =fp(kA), mhA, cvsA, plA) = fbA in"
FPIN_B = "let framed(otB, =alg, =id, =fp(kB), mhB, cvsB, plB) = fbB in"
WFPIN_A = ("let framed(otA, =alg, =id, =fp(kA), mhA, cvsA,\n"
           "                 wrap(cvIw: bitstring, (fbIA: bitstring, sgIA: bitstring,\n"
           "                                        fbIB: bitstring, sgIB: bitstring))) = fbA in")

SIGFRAME = """
(* companion-local total accessors on the SIGNED payload (the mutation needs
   the signed frame's own fields; a catch-all otherwise keeps them total). *)
fun sigFrameKfp(bitstring, pkey): bitstring
  reduc forall o: bitstring, a: bitstring, i: bitstring, kf: bitstring,
               m: bitstring, cv: bitstring, p: bitstring, k: pkey;
          sigFrameKfp(framed(o, a, i, kf, m, cv, p), k) = kf
  otherwise forall x: bitstring, k: pkey; sigFrameKfp(x, k) = fp(k).
fun sigFrameOt(bitstring): bitstring
  reduc forall o: bitstring, a: bitstring, i: bitstring, kf: bitstring,
               m: bitstring, cv: bitstring, p: bitstring;
          sigFrameOt(framed(o, a, i, kf, m, cv, p)) = o
  otherwise forall x: bitstring; sigFrameOt(x) = OT_ATTEST.
"""


def add_accessors(t):
    anchor = "(* verifier-path context handed to the judges"
    return t.replace(anchor, SIGFRAME + "\n" + anchor, 1)


def unpin_frames(t, block):
    t = edit(t, block, "=fp(kA), mhA", "kfpxA, mhA")
    t = edit(t, block, "=fp(kB), mhB", "kfpxB, mhB")
    return t


def drop_mh(t, block):
    t = drop(t, block, "if mhA = h(t) then")
    t = drop(t, block, "if mhB = h(t) then")
    return t


def poss_fponly(t, block):
    """The D-3 UNDER-ENCODING.  It is a mutation of the FIXTURE as well as of
    the verifier, and the family source says so: S-P2's Q5-C2 companion changes
    the honest signer's possession object at
    `sp2_q5_c2_fponly_frame_nomh.pv:117` -- `sign((POSS, fp(pk(sk))), sk)` --
    as well as the two verifier checks at `:133`, `:151-152`.  The library's D-3
    note is the reason: possession is over the MANIFEST, and "a model signing
    POSS over a fingerprint alone is a broken companion by definition".  Mutating
    the verifier alone leaves the honest signers producing (POSS, m) that the
    mutated verifier can never accept, so nothing is accepted at all and every
    acceptance-dependent witness dies -- a BROKEN FIXTURE, not a severing.
    (Diagnosed on the first cap_cc03_a run; see RESULTS.md, "Broken fixtures,
    diagnosed and repaired".)"""
    t = t.replace("let ppf = sign((POSS, m), sk) in",
                  "let ppf = sign((POSS, fp(pk(sk))), sk) in")
    t = edit(t, block, "let (=POSS, =t) = checksign(ppfA, kA) in",
             "let (=POSS, =fp(kA)) = checksign(ppfA, kA) in")
    t = edit(t, block, "let (=POSS, =t) = checksign(ppfB, kB) in",
             "let (=POSS, =fp(kB)) = checksign(ppfB, kB) in")
    return t


def cond_unbind(t, cond_a, cond_b):
    t = add_accessors(t)
    for blk, A, B in (("ATTEST", "fbA", "fbB"), ("WRAP", "fbA", "fbB")):
        t = edit(t, blk, "let (=BYTES, =%s) = checksign(sgA, kA) in" % A,
                 "let (=BYTES, sbA: bitstring) = checksign(sgA, kA) in\n"
                 "      if " + cond_a + " then")
        t = edit(t, blk, "let (=BYTES, =%s) = checksign(sgB, kB) in" % B,
                 "let (=BYTES, sbB: bitstring) = checksign(sgB, kB) in\n"
                 "      if " + cond_b + " then")
    return t


def cc02(t):
    # the multi-signer path, at every layer the composed verifier has one
    t = unpin_frames(t, "ATTEST2"); t = drop_mh(t, "ATTEST2")
    t = unpin_frames(t, "WRAP2")
    t = drop(t, "WRAP2", "if mhA = h(t) then")
    t = drop(t, "WRAP2", "if mhB = h(t) then")
    return t


def cc03(t):
    t = drop_mh(t, "LAYERS"); t = poss_fponly(t, "LAYERS"); return t


def cc04(t):
    # "inside InnerCheck" — the attestation layer, shared by the base path and
    # the innermost layer of a wrapped presentation, as S-P7's InnerCheck is.
    t = edit(t, "ATTEST", "=fp(kA), mhA", "kfpxA, mhA")
    t = edit(t, "ATTEST2", "=fp(kB), mhB", "kfpxB, mhB")
    t = drop_mh(t, "ATTEST2")
    t = drop(t, "ATTEST1", "if mhA = h(t) then")
    return t


def cc05(t):
    t = edit(t, "ATTEST", "let (=BYTES, =fbA) = checksign(sgA, kA) in",
             "let (=BYTES, anybA: bitstring) = checksign(sgA, kA) in")
    t = edit(t, "ATTEST2", "let (=BYTES, =fbB) = checksign(sgB, kB) in",
             "let (=BYTES, anybB: bitstring) = checksign(sgB, kB) in")
    return t


def cc06(t):
    return cond_unbind(t, "sbA = fbA || sigFrameKfp(sbA, kA) <> fp(kA)",
                          "sbB = fbB || sigFrameKfp(sbB, kB) <> fp(kB)")


def cc07i(t):
    t = add_accessors(t)
    for blk in ("ATTEST", "WRAP"):
        t = edit(t, blk, "let (=BYTES, =fbA) = checksign(sgA, kA) in",
                 "let (=BYTES, sbA: bitstring) = checksign(sgA, kA) in\n"
                 "      if sigFrameKfp(sbA, kA) = fp(kA) then")
        t = edit(t, blk, "let (=BYTES, =fbB) = checksign(sgB, kB) in",
                 "let (=BYTES, sbB: bitstring) = checksign(sgB, kB) in\n"
                 "      if sigFrameKfp(sbB, kB) = fp(kB) then")
    return t


def cc07ii(t):
    return cond_unbind(t, "sbA = fbA || sigFrameOt(sbA) <> OT_ATTEST",
                          "sbB = fbB || sigFrameOt(sbB) <> OT_ATTEST")


def cc08(t):
    t = drop_mh(t, "LAYERS"); t = poss_fponly(t, "LAYERS"); return t


def cc08i(t):
    return drop_mh(t, "LAYERS")


def cc08ii(t):
    return poss_fponly(t, "LAYERS")


def cc09(t):
    # the required-set read dropped from the one-signer branch: a two-signer
    # manifest now completes through it.  Every per-slot check is retained.
    t = edit(t, "ATTEST1", "( if ss = signers0 then", "(")
    t = edit(t, "WRAP1", "( if ss = signers0 then", "(")
    return t


def _drop_ev(t, which):
    """which in {'D','R'}: delete that channel's evidence check everywhere."""
    if which == "D":
        return t.replace("  let (=STMT_DIGEST, =h(t)) = checksign(evD, pkDv) in\n", "")
    return t.replace("  let (=STMT_DIGEST, =h(t)) = checksign(evR, pkRv) in\n", "")


def cc10_a(t):   return _drop_ev(t, "R")   # (a): DNS leaked -> the HONEST check is repo's
def cc10_b(t):   return _drop_ev(t, "D")   # (b): repo leaked -> the HONEST check is DNS's
def cc10iso_a(t): return _drop_ev(t, "D")  # isolation control: the COMPROMISED check
def cc10iso_b(t): return _drop_ev(t, "R")
def cc10_d(t):
    return t.replace("  let (=STMT_DIGEST, =h(t)) = checksign(ev, pkSv) in\n", "")


def cc11(t):
    # the attempt identity is read from the bundle instead of derived: the
    # front end forwards a declared label alongside the core and the standing
    # evidence, and the standing path uses it in place of h(core).
    t = t.replace("  in(standCore, (=intake, core: bitstring, se: bitstring));",
                  "  in(standCore, (=intake, core: bitstring, se: bitstring));\n"
                  "  in(c, aidDecl: bitstring);")
    t = edit(t, "STAND", "let aidD = h(core) in", "let aidD = aidDecl in")
    return t


Q4BODY = [
    'let StandingDecide(kT: pkey, t: bitstring, aidD: bitstring, d: bitstring,',
    '                   terminal: bitstring, intake: bitstring, lyr: bitstring,',
    '                   core: bitstring, idS: bitstring) =',
    '  (* MUTATION (ALTERNATE Q4): the terminal disposition is IGNORED.  Membership',
    '     of the derived identity in the lineage alone yields ESTABLISHED.  The',
    '     parameters d and terminal are received and never read, so the SUPERSEDED',
    '     (S2) and ISSUANCE_REFUSED (S4) branches no longer exist -- the registered',
    '     vocabulary-witness consequence of this alternate (PREDICTIONS.md, C-C11 row). *)',
    '  ( event Established(kT, t, aidD);',
    '    event StandingReport(ESTABLISHED, TERMINAL_DISPOSITION_SHOWN, kT, t, aidD);',
    '    ( ( if lyr <> L0 then',
    '          event EstablishedWrapped(intake, lyr, t, kT, core, ESTABLISHED) )',
    '    | out(estCh, (intake, lyr, kT, t, aidD))',
    '    | out(scopeStanding, (intake, lyr, kT, idS, aidD)) ) ).',
]


def cc11_q4(t):
    """ALTERNATE Q4, S-STANDING's companion C transcribed: the terminal
    disposition is IGNORED -- membership of the derived identity in the lineage
    alone yields ESTABLISHED, and `d` and `terminal` are received and never read.
    The family replaces the WHOLE StandingDecide body
    (ss_q4_companionC_terminal_unchecked.pv:234-237), which is what makes the S2
    (SUPERSEDED) and S4 (ISSUANCE_REFUSED) branches cease to exist -- the
    registered vocabulary-witness consequence of section 4's C-C11 row.
    Replacing less than the whole body would leave S4 alive and the registered
    consequence unreproduced."""
    a = t.index("let StandingDecide(kT: pkey")
    b = t.index("\n\nlet StandingPath(", a)
    return t[:a] + "\n".join(Q4BODY) + t[b:]


def cc11_abl6(t):
    return edit(t, "STAND",
        "let (=TLR, (lin: bitstring, terminal: bitstring, declT: bitstring)) =\n"
        "                checksign(tlrSig, kT) in",
        "(* ALTERNATE abl6: the TLR is taken UNSIGNED — no signature check. *)\n"
        "          let (=TLR, (lin: bitstring, terminal: bitstring, declT: bitstring)) =\n"
        "                tlrSig in")


def cc12(t):
    t = edit(t, "STAND",
        "      if fp(kT) = kfpr then\n        ( if kT = kX then",
        "      (* C-C12: NO fp(kT) = kfpr check in the standing path; the TLR key\n"
        "         equality kT = kX is RETAINED. *)\n        ( if kT = kX then")
    t = edit(t, "STAND",
        "            event StandingReport(UNVERIFIABLE, STANDING_EVIDENCE_SIGNATURE_INVALID, kT, t, aidD) )\n"
        "      else\n"
        "        event StandingReport(UNVERIFIABLE, STANDING_EVIDENCE_SIGNATURE_INVALID, kT, t, aidD) ).",
        "            event StandingReport(UNVERIFIABLE, STANDING_EVIDENCE_SIGNATURE_INVALID, kT, t, aidD) ) ).")
    return t


def cc13i(t):
    t = drop(t, "ATTEST", "if otA = OT_ATTEST then")
    t = drop(t, "ATTEST2", "if otB = OT_ATTEST then")
    return t


def cc13ii(t):
    t = drop(t, "WRAP", "if otA = OT_WRAPPER then")
    t = drop(t, "WRAP2", "if otB = OT_WRAPPER then")
    return t


def cc14(t):
    t = t.replace(
        "  event AuthorityPublishedDNS(t);\n"
        "  out(c, sign((STMT_DIGEST, h(t)), skDp)).",
        "  event AuthorityPublishedDNS(t);\n"
        "  let authTuple(idE, kfprE, ssE, algE, verE) = t in\n"
        "  out(c, sign((STMT_DIGEST, idE), skDp)).")
    t = t.replace(
        "  event AuthorityPublishedRepo(t);\n"
        "  out(c, sign((STMT_DIGEST, h(t)), skRp)).",
        "  event AuthorityPublishedRepo(t);\n"
        "  let authTuple(idE, kfprE, ssE, algE, verE) = t in\n"
        "  out(c, sign((STMT_DIGEST, idE), skRp)).")
    t = t.replace(
        "  event AuthorityPublishedDNS(t);\n"
        "  out(c, sign((STMT_DIGEST, h(t)), skSp)).",
        "  event AuthorityPublishedDNS(t);\n"
        "  let authTuple(idE, kfprE, ssE, algE, verE) = t in\n"
        "  out(c, sign((STMT_DIGEST, idE), skSp)).")
    t = t.replace(
        "  let (=STMT_DIGEST, =h(t)) = checksign(evD, pkDv) in\n"
        "  let (=STMT_DIGEST, =h(t)) = checksign(evR, pkRv) in",
        "  let authTuple(idE, kfprE, ssE, algE, verE) = t in\n"
        "  let (=STMT_DIGEST, =idE) = checksign(evD, pkDv) in\n"
        "  let (=STMT_DIGEST, =idE) = checksign(evR, pkRv) in")
    t = t.replace(
        "  let (=STMT_DIGEST, =h(t)) = checksign(ev, pkSv) in",
        "  let authTuple(idE, kfprE, ssE, algE, verE) = t in\n"
        "  let (=STMT_DIGEST, =idE) = checksign(ev, pkSv) in")
    return t


def cc16(t):
    for blk in ("ATTEST2",):
        t = drop(t, blk, "if otA = otB then")
        t = drop(t, blk, "if cvsA = cvsB then")
        t = drop(t, blk, "if plA = plB then")
    t = drop(t, "WRAP2", "if otA = otB then")
    t = drop(t, "WRAP2", "if cvsA = cvsB then")
    t = drop(t, "WRAP2", "if wrap(cvIw, (fbIA, sgIA, fbIB, sgIB)) = plB then")
    return t


def cc17(t):
    t = drop(t, "ATTEST2", "if fp(kB) = kfprB then")
    t = drop(t, "WRAP2", "if fp(kB) = kfprB then")
    return t


def cc18(t):
    t = edit(t, "STAND",
        "let (=TLR, (lin: bitstring, terminal: bitstring, declT: bitstring)) =\n"
        "                checksign(tlrSig, kT) in",
        "(* C-C18: the D-6 TLR TAG CHECK UNBOUND.  The parsed tag is still\n"
        "             reported to C-Q10's judge. *)\n"
        "          let (uncheckedTag: bitstring,\n"
        "               (lin: bitstring, terminal: bitstring, declT: bitstring)) =\n"
        "                checksign(tlrSig, kT) in")
    t = edit(t, "STAND", "out(tagCh, (kT, TLR))", "out(tagCh, (kT, uncheckedTag))")
    return t




# ---------------------------------------------------------------- C-C15 ----
# D11's companion needs the ATTESTATION layer to behave differently when it is
# reached THROUGH A WRAPPER, exactly as S-P7's Q6b/Q5c/Q6a companions mutate
# the wrapped path and leave VerifierBase alone.  The capstone shares one
# AttestStage between the base path and the innermost layer, so the mutant
# SPLITS it: the correct stage keeps the cases the configuration does not
# touch, and a copy, AttestStageW, carries the mutation for the wrapped ones.
# This is a block duplication, not a line edit; it is the only companion that
# needs one, and it is written out here so the delta can be read.
ATT_START = "let AttestStage(pkDv: pkey, pkRv: pkey) ="
ATT_START_D = "let AttestStage(pkSv: pkey) ="
ATT_END = "(* ==================================================================== *)\n(* ==== THE WRAPPER LAYER"


def _split_attest(t, guard_correct, guard_w, muts):
    start = ATT_START if ATT_START in t else ATT_START_D
    i = t.index(start)
    j = t.index(ATT_END, i)
    body = t[i:j]
    # the point after the two input prefixes, where a guard may be inserted
    anchor = "         kA: pkey, ppfA: bitstring, kB: pkey, ppfB: bitstring));\n"
    k = body.index(anchor) + len(anchor)
    correct = body[:k] + guard_correct + body[k:]
    w = body[:k] + guard_w + body[k:]
    w = w.replace("let AttestStage(", "let AttestStageW(", 1)
    applied = 0
    for old, new in muts:
        if old not in w:
            continue          # mode-specific line (evD/evR vs ev, slot B, ...)
        w = w.replace(old, new); applied += 1
    if applied == 0:
        raise SystemExit("derive.py C-C15: no mutation applied")
    t = t[:i] + correct + "\n" + w + t[j:]
    t = t.replace("  | !AttestStage(pk(skD), pk(skR))",
                  "  | !AttestStage(pk(skD), pk(skR)) | !AttestStageW(pk(skD), pk(skR))")
    t = t.replace("  | !AttestStage(pk(skS))",
                  "  | !AttestStage(pk(skS)) | !AttestStageW(pk(skS))")
    return t


WCTX = ("  let wctx(kEncW: pkey, idEncW: bitstring, fbEncW: bitstring) = ctx in\n")

# attribution rewrites shared by (i) and (ii): the layer reports the ENCLOSING
# wrapper's key and identity in place of its own accepting key and identity.
ATTRIB_BOTH = [
  ("event ScopeReported(aid, lyr, kA, id);", "event ScopeReported(aid, lyr, kEncW, idEncW);"),
  ("out(link6bCh, (aid, lyr, kA, id, fbA))", "out(link6bCh, (aid, lyr, kEncW, idEncW, fbA))"),
  ("out(scopeCh, (ctx, kA, id, fbA))", "out(scopeCh, (ctx, kEncW, idEncW, fbA))"),
  ("out(scopeCh, (ctx, kB, id, fbB))", "out(scopeCh, (ctx, kEncW, idEncW, fbB))"),
  ("out(scopeEnvelope, (aid, lyr, kA, id))", "out(scopeEnvelope, (aid, lyr, kEncW, idEncW))"),
]
ATTRIB_ID = [
  ("event ScopeReported(aid, lyr, kA, id);", "event ScopeReported(aid, lyr, kA, idEncW);"),
  ("out(link6bCh, (aid, lyr, kA, id, fbA))", "out(link6bCh, (aid, lyr, kA, idEncW, fbA))"),
  ("out(scopeCh, (ctx, kA, id, fbA))", "out(scopeCh, (ctx, kA, idEncW, fbA))"),
  ("out(scopeCh, (ctx, kB, id, fbB))", "out(scopeCh, (ctx, kB, idEncW, fbB))"),
  ("out(scopeEnvelope, (aid, lyr, kA, id))", "out(scopeEnvelope, (aid, lyr, kA, idEncW))"),
]


def cc15i(t):
    # S-P7 Q6b transcribed: on the wrapped path the key and authority are read
    # from the WRAPPER frame.  The inner signature is verified under kW; the
    # presented inner tuple, evidence, possession proof and frame fields are
    # read but NEVER MATCHED.  Under §1.3's report contract the acceptance
    # carries the terms that layer's acceptance was ABOUT.
    muts = [
      ("  let (=STMT_DIGEST, =h(t)) = checksign(evD, pkDv) in\n", ""),
      ("  let (=STMT_DIGEST, =h(t)) = checksign(evR, pkRv) in\n", ""),
      ("  let (=STMT_DIGEST, =h(t)) = checksign(ev, pkSv) in\n", ""),
      ("if fp(kA) = kfprA then", "if true then"),
      ("if fp(kB) = kfprB then", "if true then"),
      ("let framed(otA, =alg, =id, =fp(kA), mhA, cvsA, plA) = fbA in",
       "let framed(otA, algxA, idxA, kfpxA, mhA, cvsA, plA) = fbA in"),
      ("let framed(otB, =alg, =id, =fp(kB), mhB, cvsB, plB) = fbB in",
       "let framed(otB, algxB, idxB, kfpxB, mhB, cvsB, plB) = fbB in"),
      ("if mhA = h(t) then", "if true then"),
      ("if mhB = h(t) then", "if true then"),
      ("let (=POSS, =t) = checksign(ppfA, kA) in", "if true then"),
      ("let (=POSS, =t) = checksign(ppfB, kB) in", "if true then"),
      ("let (=BYTES, =fbA) = checksign(sgA, kA) in",
       "let (=BYTES, =fbA) = checksign(sgA, kEncW) in"),
      ("let (=BYTES, =fbB) = checksign(sgB, kB) in",
       "let (=BYTES, =fbB) = checksign(sgB, kEncW) in"),
      ("out(sigCh, (ctx, kA, sgA))", "out(sigCh, (ctx, kEncW, sgA))"),
      ("out(sigCh, (ctx, kB, sgB))", "out(sigCh, (ctx, kEncW, sgB))"),
    ] + ATTRIB_BOTH
    t = _split_attest(t, "  if ctx = BASE then\n", WCTX, muts)
    # REPAIR 2026-10-01 (broken fixture BF-4, diagnosed in
    # dev/divergences/DIAGNOSIS.md G3): the transcription above re-keyed only the
    # scope reports (ATTRIB_BOTH) and sigCh to the wrapper key; every other event
    # and report in AttestStageW (LayerAccepted, Accept, link2aCh, possCh,
    # bytesCh, link5Ch, slotCh, setCh, acceptCh, acceptKeyCh, gsigCh, chainCh)
    # still carried the PRESENTED inner kA/kB, which after the mutation no check
    # touches.  That contradicts the registered report contract -- "the inner
    # acceptance of this configuration reports the presented inner (kW, tI,
    # ppfI)" (PREDICTIONS.md:2503, C-C15(i) Cases cell) -- and the family
    # descent (cap25a_sp7_strict_q6b_sigjudges.pv:331-336 reports kW
    # everywhere), and it redded seven out-of-set strict queries.  The repair
    # replaces kA/kB by kEncW in AttestStageW's EVENTS AND REPORTS ONLY, never in
    # a check -- exactly the change of dev/divergences/mk_cc15i_kw.py, whose
    # diagnostic copies dv_cc15i_kw_{a,b,d} confirmed it.  The scope reports are
    # already kEncW and are unchanged; the correct AttestStage is untouched.
    return _report_wrapper_key(t)


def _report_wrapper_key(t):
    # BF-4 repair (see cc15i): inside AttestStageW only, kA/kB -> kEncW on every
    # line that is an event or an output; lines that check are left alone.
    i = t.index("let AttestStageW(")
    j = t.index(ATT_END, i)
    out = []
    for ln in t[i:j].split("\n"):
        s = ln.strip()
        if s.startswith("event ") or "out(" in s:
            ln = re.sub(r"\bkA\b", "kEncW", ln)
            ln = re.sub(r"\bkB\b", "kEncW", ln)
        out.append(ln)
    return t[:i] + "\n".join(out) + t[j:]


def cc15ii(t):
    # S-P7 Q5c transcribed: at DEPTH 2 the scope is taken from the MIDDLE layer
    # rather than the innermost.  ctx at L2 IS the middle wrapper.  Every
    # verification is left alone.
    return _split_attest(t, "  if lyr <> L2 then\n", WCTX + "  if lyr = L2 then\n",
                         ATTRIB_BOTH)


OBSQ = """
(* ---- the TWO ISOLATION OBSERVERS, queried HERE AND NOWHERE ELSE.
   They are observers, not queries: never counted among the 27 registered
   entries, never timeboxed on their own, and no discharge of any matrix row
   rests on either of them.  Configuration (iii) requires the IDENTITY
   observer REACHABLE and the KEY observer UNREACHABLE. *)
query a: bitstring, l: bitstring, k: pkey, ka: pkey; event(ScopeKeyOnly(a, l, k, ka)).
query a: bitstring, l: bitstring, i1: bitstring, i2: bitstring;
  event(ScopeIdentityOnly(a, l, i1, i2)).
"""


def cc15iii(t):
    # S-P7 Q6a transcribed, the ISOLATION configuration: the attributed ISSUER
    # IDENTITY is read from the enclosing frame; the KEY and the whole key
    # binding are RETAINED.
    t = t.replace("(* ---- the REQUIRED retained queries", OBSQ + "\n(* ---- the REQUIRED retained queries", 1)
    return _split_attest(t, "  if ctx = BASE then\n", WCTX, ATTRIB_ID)


# name -> (mutation, what-it-mutates, serves, box-minutes, cases)
COMPANIONS = [
 ("cc02", cc02,  "the frame's =fp(k_) pin AND the manifest-hash equality, multi-signer path",
   "D1; set (1): C-Q3, C-Q1 link 5's frame-to-key half", 45, "abd"),
 ("cc03", cc03,  "both SetAltered routes: the frames' mh pin AND possession-over-manifest",
   "D10; set (1): C-Q5, C-Q9, C-Q1 link 3", 45, "abd"),
 ("cc04", cc04,  "the complete key-binding relation inside InnerCheck: inner =fp(kI) AND mhI = h(tI)",
   "D2; set (1): C-Q4 Rescoped, InnerSigTransplanted, C-Q3, links 6b and 5", 60, "abd"),
 ("cc05", cc05,  "the inner signature unbound from the presented bytes inside InnerCheck",
   "D5; set (1): C-Q4 InnerSigTransplanted, C-Q8, link 4", 60, "abd"),
 ("cc06", cc06,  "the CONDITIONAL unbinding: byte equality only when the signed frame's kfp matches",
   "D5/D6; set (1): C-Q7, C-Q4 InnerSigTransplanted, (predicted) C-Q8 and link 4", 45, "abd"),
 ("cc07i", cc07i, "configuration (i): same-key byte unbinding",
   "D6; set (1): C-Q8, link 4, AcceptedUnderHonestKey => IssuerSigned", 60, "abd"),
 ("cc07ii", cc07ii, "configuration (ii): type-conditional byte unbinding",
   "D6; set (1): C-Q8, link 4 (and, composed, C-Q7 and honest-key authorship)", 60, "abd"),
 ("cc08", cc08,  "possession made fingerprint-only AND the frames' mh = h(t) guards dropped",
   "D10; set (1): C-Q9, C-Q5, link 3, link 5's mh half", 60, "abd"),
 ("cc08i", cc08i, "ISOLATION i: the frames' manifest-hash guards ALONE",
   "D10 isolation; required: C-Q9 green and C-Q5 green", 60, "abd"),
 ("cc08ii", cc08ii, "ISOLATION ii: the possession binding ALONE (fingerprint-only)",
   "D10 isolation; required: C-Q5 green, C-Q9 RED by construction", 60, "abd"),
 ("cc09", cc09,  "the required-set read dropped from the one-signer branch",
   "D7 (set/completeness half); set (1): link 2b's slot-B conjunct, Stripped", 60, "abd"),
 ("cc11", cc11,  "S-STANDING Q2: the attempt identity read from the bundle, not derived",
   "D12; set (1): C-Q6's standing conjunct, honest-key forms AND unrestricted", 90, "abd"),
 ("cc11q4", cc11_q4, "ALTERNATE Q4: terminal disposition unchecked",
   "D12 alternate; S2 and S4 vocabulary witnesses UNREACHABLE as a registered consequence", 90, "abd"),
 ("cc11abl6", cc11_abl6, "ALTERNATE abl6: the TLR taken unsigned",
   "D12 alternate; set (1): C-Q6's standing conjunct", 90, "abd"),
 ("cc12", cc12,  "S-STANDING Q3: the standing path drops fp(kT) = kfpr, RETAINS kT = kX",
   "D13; set (1): C-Q6's entitled-key conjunct (StandingUnentitledWrapped reachable)", 90, "abd"),
 ("cc13i", cc13i, "configuration (i): the acceptance path's object-type equality relaxed",
   "D8; set (1): C-Q1 link 6a, TypeConfused", 45, "abd"),
 ("cc13ii", cc13ii, "configuration (ii): the wrapped path's outer =OT_WRAPPER equality dropped",
   "D8; set (1): C-Q1 link 6a at the WRAPPER LAYERS only, TypeConfused", 45, "abd"),
 ("cc14", cc14,  "the authority evidence commits to a PROPER SUBSET of the tuple (the identity alone)",
   "D9; set (1): C-Q2 TwoWorldsBroken, link 1a, link 1b, Accept => IssuerSigned", 45, "ab"),
 ("cc15i", cc15i, "configuration (i) — S-P7 Q6b: outermost scope; the inner signature verified under the wrapper key and the presented inner terms never matched",
   "D11; set (1): C-Q1 link 6b, C-Q4 Rescoped, C-Q3, C-Q7, C-Q9, link 3, links 1a/1b/2a, link 5's mh half, C-Q5, SignerForged", 45, "abd"),
 ("cc15ii", cc15ii, "configuration (ii) — S-P7 Q5c: at depth 2 the scope is taken from the MIDDLE layer",
   "D11; set (1): C-Q1 link 6b at L2, C-Q4's depth-2 scope half", 45, "abd"),
 ("cc15iii", cc15iii, "configuration (iii) — S-P7 Q6a, ISOLATION: the attributed IDENTITY from the enclosing frame, the key retained",
   "D11 isolation; set (1): C-Q1 link 6b, C-Q4 Rescoped, C-Q6 conjunct 3 with ScopeIdentityOnly; set (2) contains the observer ScopeKeyOnly, which must stay UNREACHABLE", 45, "abd"),
 ("cc16", cc16,  "the three §A5.4 cross-slot content equalities dropped (check 4)",
   "D7 (common-content half); set (1): link 5's content conjunct, Spliced", 60, "abd"),
 ("cc17", cc17,  "slot B's key-fingerprint equality removed on the two-signer branch (check 3)",
   "D7 (membership half); set (1): link 2a, SignerForged", 45, "abd"),
 ("cc18", cc18,  "the D-6 TLR tag check UNBOUND in check 7",
   "the composed D-6 tag property; set (1): C-Q10 TagConfused, C-Q6's standing conjunct", 30, "abd"),
]

CASENAME = {"a": "(a) STRICT, DNS compromised", "b": "(b) STRICT, repository compromised",
            "c": "(c) STRICT, both channels leaked", "d": "(d) DEGRADED, sole channel"}


def header(name, mutates, serves, box, cs):
    L = []
    L.append("(* ==================================================================== *)")
    L.append("(* STATUS: PROPOSED - 2026-09-19 - produced by the AI collaborator")
    L.append("   (Claude Opus 5, builder, directed by the owner instance); not adopted;")
    L.append("   the commit is the author's.  GENERATED by derive.py from capstone.pv;")
    L.append("   do not edit by hand.")
    L.append("   FILE:    " + name)
    L.append("   CASE:    " + CASENAME[cs])
    L.append("   MUTATES: " + mutates)
    L.append("   SERVES:  " + serves)
    L.append("   REGISTERED BOX: %d min - the box of the query this companion is" % box)
    L.append("   predicted to red.  No companion carries a timebox of its own")
    L.append("   (PREDICTIONS.md section 4, \"The count\").")
    L.append("*)")
    L.append("(* ==================================================================== *)")
    return "\n".join(L) + "\n\n"


def write(path, text):
    open(os.path.join(HERE, path), "w").write(text)
    print("wrote", path)


def main():
    bases = {"a": case(BASE, "a"), "b": case(BASE, "b"), "c": case(BASE, "c"),
             "d": degraded(BASE)}
    # the correct-form runs, and case (c) which IS companion C-C1
    # case (a) IS capstone.pv itself; no copy is written, so that the model the
    # registration names is the file that runs and the blob hash is its own.
    write("capstone_b.pv", bases["b"])
    write("capstone_d.pv", bases["d"])
    write("cap_cc01_c.pv",
          bases["c"].replace("(* capstone.pv — THE COMPOSED MODEL",
                             "(* cap_cc01_c.pv — COMPANION C-C1 (case (c)) — THE COMPOSED MODEL", 1))
    # the companions
    for name, fn, mutates, serves, box, cases in COMPANIONS:
        for cs in cases:
            if name == "cc10":
                continue
            t = fn(bases[cs])
            fname = "cap_%s_%s.pv" % (name, cs)
            write(fname, header(fname, mutates, serves, box, cs) + t)
    # C-C10 and its isolation control are stated per mode (§4)
    for cs, fn in (("a", cc10_a), ("b", cc10_b), ("d", cc10_d)):
        fname = "cap_cc10_%s.pv" % cs
        write(fname, header(fname,
              "the HONEST channel's evidence check deleted (in (d): the sole channel's)",
              "D4; set (1): link 1a; in strict also link 1b and Accept => IssuerSigned",
              45, cs) + fn(bases[cs]))
    for cs, fn in (("a", cc10iso_a), ("b", cc10iso_b)):
        fname = "cap_cc10iso_%s.pv" % cs
        write(fname, header(fname,
              "ISOLATION CONTROL: the COMPROMISED channel's evidence check deleted instead",
              "D4 isolation; required: link 1a RED, link 1b GREEN (the distinguishing signal)",
              45, cs) + fn(bases[cs]))


if __name__ == "__main__":
    main()
