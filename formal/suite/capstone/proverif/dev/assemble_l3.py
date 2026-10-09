#!/usr/bin/env python3
"""Development helper (scratch), LADDER 3.  Written 2026-10-06 by the capstone builder.

Adapted from dev/assemble_l2.py, which is kept unedited as the record of the ladder-2 assembly.
The KEYS, the section-1 prediction table P, the per-companion registration SPEC, judge(),
PREDBOX and MATRIX are copied from assemble_l2.py VERBATIM (nothing in the registration moved).
What changed, and why (2026-10-06):
  1. Ladder 3 (blob 35d8c702...) is ./ladder.log; ladder 2 is ladder2/ladder.log (with its BF-4
     superseded runs in ladder2/superseded-by-BF-4/); ladder 1 is ladder1/ladder.log.
  2. rc=NOT-RUN lines (the eleven .notrun markers) give the disposition "not run under this
     blob".  A repeated NOT-RUN line for the same stem (a resume artifact; see the RESTART comment
     at ladder.log:47) is collapsed to the first and counted in NOTRUN_DUPS; it is not a run.
  3. *.interrupted-by-host-crash.out is never read: a stem's output is exactly <stem>.out, and the
     script stops if a landed stem's ladder.log line is missing.
  4. Every cell for one of the eleven cites its ladder-3 NOT-RUN line and gives the ladder-2
     failure as history (ladder2/ladder.log line), never as a ladder-3 result.
  5. The cross-check is ladder 2 against ladder 3, per file AND per keyed query.  Every changed
     verdict is attributed to BF-5/BF-6 (C-Q6 keys and the two standing witnesses, any file) or
     BF-7 (C-C7(i) files), or flagged UNEXPLAINED.
  6. The two standing witnesses' trace layer is read off each landed run (BF-6's check).
  7. The ceiling is summed over ladders 1, 2 (incl. BF-4 superseded runs) and 3.
It transcribes and compares; it decides nothing.
Usage: python3 dev/assemble_l3.py          -> rewrites the marked regions of ../../RESULTS.md and
                                              writes dev/l3/{print.txt,crosscheck.tsv,linemap.tsv,witness_layers.tsv}
       python3 dev/assemble_l3.py --print  -> writes dev/l3/ outputs only, not RESULTS.md
"""
import os, re, sys, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
PROV = os.path.abspath(os.path.join(HERE, ".."))
RES = os.path.abspath(os.path.join(PROV, "..", "RESULTS.md"))
L1 = os.path.join(PROV, "ladder1")
L2 = os.path.join(PROV, "ladder2")
OUTD = os.path.join(HERE, "l3")

# ---------------------------------------------------------------------------------------------
# 1. Keys.  (key, regex over the NORMALISED RESULT line).  Exactly one must match each line.
KEYS = [
 ("link1a", r"ChainBroken\(l,LINK_1A\)"),
 ("link1b", r"AuthorityPublishedDNS"),
 ("link2a", r"ChainBroken\(l,LINK_2A\)"),
 ("link2b-s0", r"signers0,alg,ver\)\)\) ==> event\(SlotSatisfied"),
 ("link2b-A", r"signers1\(fpB\),alg,ver\),fpA\)\)"),
 ("link2b-B", r"signers1\(fpB\),alg,ver\),fpB\)\)"),
 ("C-Q7", r"not event\(SigTransplanted\("),
 ("C-Q8", r"not event\(SigBytesUnbound\("),
 ("C-Q9", r"not event\(PossessionUnbound\("),
 ("link3", r"ChainBroken\(l,LINK_3\)"),
 ("link4", r"ChainBroken\(l,LINK_4\)"),
 ("link5", r"ChainBroken\(l,LINK_5\)"),
 ("link6a", r"ChainBroken\(l,LINK_6A\)"),
 ("link6b", r"ChainBroken\(l,LINK_6B\)"),
 ("C-Q2", r"TwoWorldsBroken\("),
 ("C-Q3-A", r"ReattributedA\("),
 ("C-Q3-B", r"ReattributedB\("),
 ("C-Q4-Rescoped", r"not event\(Rescoped\("),
 ("C-Q4-InnerSig", r"InnerSigTransplanted\("),
 ("C-Q5", r"SetAltered\("),
 ("C-Q5w-1", r"verified1\(k1\)"),
 ("C-Q5w-2", r"verified2\(k1,k2\)"),
 ("C-Q10", r"TagConfused\("),
 ("C-Q6-c1-unres", r"EstablishedWrapped\(aid,lyr,t,kX,co,ESTABLISHED\)"),
 ("C-Q6-c1-skI", r"EstablishedWrapped\(aid,lyr,t,pk\(skI\[\]\),co"),
 ("C-Q6-c1-skI2", r"EstablishedWrapped\(aid,lyr,t,pk\(skI2\[\]\),co"),
 ("C-Q6-c2", r"StandingUnentitledWrapped\("),
 ("C-Q6-c3", r"ScopeMisreported\("),
 ("RET-accept", r"event\((Accept|AcceptS)\([^)]*\)\) ==> event\(IssuerSigned"),
 ("RET-honestkey", r"event\(AcceptedUnderHonestKey\("),
 ("RET-Stripped", r"not event\(Stripped\("),
 ("RET-SignerForged", r"not event\(SignerForged\("),
 ("RET-Spliced", r"not event\(Spliced\("),
 ("RET-TypeConfused", r"not event\(TypeConfused\("),
 ("RET-VersionLied", r"not event\(VersionLied\("),
 ("W-HonestChainL0", r"HonestChain\(L0,"),
 ("W-HonestChainL1", r"HonestChain\(L1,"),
 ("W-HonestChainL2", r"HonestChain\(L2,"),
 ("W-HonestAccepted", r"not event\(HonestAccepted\("),
 ("W-HonestWrapped", r"HonestWrappedAccepted\("),
 ("W-HonestStanding", r"HonestStandingEstablished\("),
 ("W-Agreed", r"HonestWrappedStandingAgreed\("),
 ("V-S1", r"StandingReport\(ESTABLISHED,TERMINAL_DISPOSITION_SHOWN"),
 ("V-S2", r"StandingReport\(ABSENT,SUPERSEDED"),
 ("V-S3", r"StandingReport\(ABSENT,NO_TERMINAL_DISPOSITION_EVIDENCE"),
 ("V-S4", r"StandingReport\(ABSENT,ISSUANCE_REFUSED"),
 ("V-MIS", r"StandingReport\(ABSENT,STANDING_EVIDENCE_MISMATCH"),
 ("OBS-key", r"ScopeKeyOnly\("),
 ("OBS-identity", r"ScopeIdentityOnly\("),
]
KRE = [(k, re.compile(r)) for k, r in KEYS]
NAME = {
 "link1a": "C-Q1 link 1a", "link1b": "C-Q1 link 1b", "link2a": "C-Q1 link 2a",
 "link2b-s0": "link 2b one-signer conj.", "link2b-A": "link 2b slot-A conj.",
 "link2b-B": "link 2b slot-B conj.", "C-Q7": "C-Q7", "C-Q8": "C-Q8", "C-Q9": "C-Q9",
 "link3": "link 3", "link4": "link 4", "link5": "link 5", "link6a": "link 6a", "link6b": "link 6b",
 "C-Q2": "C-Q2", "C-Q3-A": "C-Q3 `ReattributedA`", "C-Q3-B": "C-Q3 `ReattributedB`",
 "C-Q4-Rescoped": "C-Q4 `Rescoped`", "C-Q4-InnerSig": "C-Q4 `InnerSigTransplanted`",
 "C-Q5": "C-Q5", "C-Q5w-1": "`HonestComplete` (1-signer)", "C-Q5w-2": "`HonestComplete` (2-signer)",
 "C-Q10": "C-Q10", "C-Q6-c1-unres": "C-Q6 c1 unrestricted", "C-Q6-c1-skI": "C-Q6 c1 `skI`",
 "C-Q6-c1-skI2": "C-Q6 c1 `skI2`", "C-Q6-c2": "C-Q6 c2", "C-Q6-c3": "C-Q6 c3 `ScopeMisreported`",
 "RET-accept": "`Accept(S) => IssuerSigned`", "RET-honestkey": "`AcceptedUnderHonestKey => IssuerSigned`",
 "RET-Stripped": "`Stripped`", "RET-SignerForged": "`SignerForged`", "RET-Spliced": "`Spliced`",
 "RET-TypeConfused": "`TypeConfused`", "RET-VersionLied": "`VersionLied`",
 "W-HonestChainL0": "`HonestChain(L0)`", "W-HonestChainL1": "`HonestChain(L1)`",
 "W-HonestChainL2": "`HonestChain(L2)`", "W-HonestAccepted": "`HonestAccepted`",
 "W-HonestWrapped": "`HonestWrappedAccepted`", "W-HonestStanding": "`HonestStandingEstablished`",
 "W-Agreed": "`HonestWrappedStandingAgreed`", "V-S1": "S1", "V-S2": "S2", "V-S3": "S3",
 "V-S4": "S4", "V-MIS": "MISMATCH", "OBS-key": "observer `ScopeKeyOnly`",
 "OBS-identity": "observer `ScopeIdentityOnly`",
}
HONEST_W = ["C-Q5w-1", "C-Q5w-2", "W-HonestChainL0", "W-HonestChainL1", "W-HonestChainL2",
            "W-HonestAccepted", "W-HonestWrapped", "W-HonestStanding", "W-Agreed"]
VOCAB_W = ["V-S1", "V-S2", "V-S3", "V-S4", "V-MIS"]
WITNESS = HONEST_W + VOCAB_W
SAFETY = [k for k, _ in KEYS if k not in WITNESS]          # includes the two observers
C_Q3 = ("C-Q3-A", "C-Q3-B")

NORM = re.compile(r"(^|[^K])_[0-9]+")


def norm(ln):
    prev = None
    while prev != ln:
        prev, ln = ln, NORM.sub(r"\1", ln)
    return ln


def parse(path):
    """key -> (line, 'true'|'false').  Stops on an unkeyed or doubly-keyed RESULT line."""
    d = {}
    for n, ln in enumerate(open(path, errors="replace"), 1):
        if not ln.startswith("RESULT"):
            continue
        s = norm(ln.rstrip())
        v = "true" if s.endswith("is true.") else "false" if s.endswith("is false.") else None
        if v is None:
            sys.exit("UNREADABLE VERDICT %s:%d %s" % (path, n, s[-80:]))
        hit = [k for k, r in KRE if r.search(s)]
        if len(hit) != 1:
            sys.exit("KEYING FAILURE %s:%d %s -> %s" % (path, n, s[:160], hit))
        if hit[0] in d:
            sys.exit("DUPLICATE KEY %s:%d %s (first :%d)" % (path, n, hit[0], d[hit[0]][0]))
        d[hit[0]] = (n, v)
    return d


# ---------------------------------------------------------------------------------------------
# 2. Ladder logs.
BFRE = re.compile(r"^# (BF-\d+) REPAIR (\S+): (\S+) regenerated")
SUPERSEDED2 = {}     # ladder 2 only: stem -> (BF id, [(logline, dict), ...])
SUPDIR2 = os.path.join(L2, "superseded-by-BF-4")
NOTRUN_DUPS = []     # (stem, logline) of repeated NOT-RUN lines, collapsed


def _expand(spec):
    m = re.match(r"^(.*)\{([^}]*)\}(.*)$", spec)
    return [m.group(1) + x + m.group(3) for x in m.group(2).split(",")] if m else [spec]


def ladder(path, repairs=None, dedupe_notrun=False):
    """stem -> list of (logline, dict)."""
    runs = collections.defaultdict(list)
    for n, ln in enumerate(open(path), 1):
        m = BFRE.match(ln)
        if repairs is not None and m:
            for stem in _expand(m.group(3)):
                repairs[stem] = (m.group(1), runs.pop(stem, []))
            continue
        if ln.startswith("#") or " rc=" not in ln:
            continue
        parts = ln.split()
        dd = {}
        for x in parts[1:]:
            if x.startswith("note="):
                break
            if "=" in x:
                a, b = x.split("=", 1)
                dd.setdefault(a, b)
        if dedupe_notrun and dd.get("rc") == "NOT-RUN" and any(
                d0.get("rc") == "NOT-RUN" for _, d0 in runs[parts[0]]):
            NOTRUN_DUPS.append((parts[0], n))
            continue
        runs[parts[0]].append((n, dd))
    return runs


L3RUNS = ladder(os.path.join(PROV, "ladder.log"), dedupe_notrun=True)
L2RUNS = ladder(os.path.join(L2, "ladder.log"), repairs=SUPERSEDED2)
L1RUNS = ladder(os.path.join(L1, "ladder.log"))
STEMS = sorted(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(PROV, "*.pv")))


def _final(rs):
    if not rs:
        return ("no line", [], {})
    lines = [n for n, _ in rs]
    n, d = rs[-1]
    rc = d.get("rc")
    if rc == "0":
        return ("landed", lines, d)
    if rc == "NOT-RUN":
        return ("not run", lines, d)
    if rc == "124":
        return ("timeout", lines, d)
    if rc in ("143", "MECHFAIL-MEMORY"):
        for nn, dd in rs:
            if dd.get("rc") == "143":
                d = dd
        return ("memory", lines, d)
    return ("rc=%s" % rc, lines, d)


def final(stem):
    """Ladder-3 disposition."""
    return _final(L3RUNS.get(stem, []))


def final2(stem):
    """Ladder-2 disposition (history)."""
    return _final(L2RUNS.get(stem, []))


OUTCOME2 = {"timeout": "timeout (mechanism-viability failure)",
            "memory": "terminated by memory guard, classified as mechanism failure (memory)"}


def history2(stem):
    disp, lines, d = final2(stem)
    secs = int(d.get("seconds", "0") or 0)
    pk = d.get("peakRSSkB")
    pkt = (", %.1f GiB" % (int(pk) / 1048576.0)) if pk else ""
    return "ladder 2, history: %s, %d s%s (%s)" % (
        OUTCOME2.get(disp, disp), secs, pkt, ", ".join("`ladder2/ladder.log:%d`" % n for n in lines))


NOTRUN_TXT = "**not run under this blob**"


def outcome(stem):
    disp = final(stem)[0]
    if disp == "not run":
        return "%s (`ladder.log:%d`; %s)" % (NOTRUN_TXT, final(stem)[1][0], history2(stem))
    return disp


def runcell(stem):
    disp, lines, d = final(stem)
    if disp == "not run":
        return disp, "not run (`ladder.log:%d`); %s" % (lines[0], history2(stem))
    secs = int(d.get("seconds", "0") or 0)
    pk = d.get("peakRSSkB")
    pkt = (", %.1f GiB peak" % (int(pk) / 1048576.0)) if pk else ""
    rcs = ", ".join("`ladder.log:%d`" % n for n in lines)
    rcv = "/".join(dd.get("rc") for _, dd in L3RUNS.get(stem, []))
    return disp, "`rc=%s`, %d s%s (%s)" % (rcv, secs, pkt, rcs)


# ---------------------------------------------------------------------------------------------
# 2b. The two standing witnesses' trace layer (BF-6).  HonestWrappedStandingAgreed carries the
#     layer in its goal event; HonestStandingEstablished does not, so its layer is read from the
#     last out(estCh, (aid, L?, ...)) in the query's trace block, which StandingJudge receives.
def standing_layers(path):
    res = {}
    blk, key = [], None
    for n, ln in enumerate(open(path, errors="replace"), 1):
        if ln.startswith("-- Query"):
            key, blk = None, []
            if ln.startswith("-- Query not event(HonestStandingEstablished"):
                key = "W-HonestStanding"
            elif ln.startswith("-- Query not event(HonestWrappedStandingAgreed"):
                key = "W-Agreed"
        if key is None:
            continue
        if key == "W-HonestStanding":
            m = re.search(r"^out\(estCh, \(\w+,(L[0-2]),", ln)
            if m:
                blk.append((n, m.group(1)))
        else:
            m = re.search(r"^event HonestWrappedStandingAgreed\(\w+,(L[0-2])\) at", ln)
            if m:
                blk.append((n, m.group(1)))
        if ln.startswith("RESULT"):
            res[key] = blk[-1] if blk else None
            key = None
    return res

# ---------------------------------------------------------------------------------------------
# 3. Section 1: every registered query, by case (correct-form runs).  Predictions and lines as
#    mkresults.py carried them (spot-checked against PREDICTIONS.md 2026-10-01).
G, R, RE, NA = "green", "red", "reachable", "not stated"
P = [
 ("link1a", "green, p ~ 0.8", "362", "abcd"),
 ("link1b", "`is true` in (a) and (b), p ~ 0.8; `is false` in (c)", "379", "abc"),
 ("link2a", "green, p ~ 0.8", "408", "abcd"),
 ("link2b-s0", "all three conjuncts `is true`, p ~ 0.55", "447", "abcd"),
 ("link2b-A", "all three conjuncts `is true`, p ~ 0.55", "447", "abcd"),
 ("link2b-B", "all three conjuncts `is true`, p ~ 0.55", "447", "abcd"),
 ("C-Q7", "green, p ~ 0.8", "1371", "abcd"),
 ("C-Q8", "green, p ~ 0.75", "1391", "abcd"),
 ("C-Q9", "green, p ~ 0.8", "1408", "abcd"),
 ("link3", "green, p ~ 0.8", "466", "abcd"),
 ("link4", "green, p ~ 0.75", "479", "abcd"),
 ("link5", "green, p ~ 0.65", "509", "abcd"),
 ("link6a", "green, p ~ 0.85", "527", "abcd"),
 ("link6b", "green, p ~ 0.8", "583", "abcd"),
 ("C-Q2", "green, p ~ 0.65", "599", "ab"),
 ("C-Q3-A", "green, p ~ 0.8", "615", "abcd"),
 ("C-Q3-B", "green, p ~ 0.8", "615", "abcd"),
 ("C-Q4-Rescoped", "both green, p ~ 0.75", "630", "abcd"),
 ("C-Q4-InnerSig", "both green, p ~ 0.75", "630", "abcd"),
 ("C-Q5", "green, p ~ 0.8", "689", "abcd"),
 ("C-Q5w-1", "reachable, p ~ 0.85", "699", "abcd"),
 ("C-Q5w-2", "reachable, p ~ 0.85", "699", "abcd"),
 ("C-Q10", "green, p ~ 0.85", "1459", "abd"),
 ("C-Q6-c1-unres", "all three conjuncts hold, p ~ 0.5 (unrestricted form strict only)", "1324", "ab"),
 ("C-Q6-c1-skI", "green in (a), (b) and (d)", "1233", "abd"),
 ("C-Q6-c1-skI2", "green in (a), (b) and (d)", "1233", "abd"),
 ("C-Q6-c2", "unreachable in (a), (b) and (d)", "1245", "abd"),
 ("C-Q6-c3", "unreachable in (a), (b) and (d)", "1289", "abd"),
 ("RET-accept", "green in (a)/(b) p ~ 0.85; RED in (c) p ~ 0.9; degraded `AcceptS` form registered RED in (d), the A4.6 cost", "1569, 1580", "abcd"),
 ("RET-honestkey", "green, p ~ 0.85", "1570", "abcd"),
 ("RET-Stripped", "green, p ~ 0.8", "1571", "abcd"),
 ("RET-SignerForged", "green, p ~ 0.8", "1572", "abcd"),
 ("RET-Spliced", "green, p ~ 0.75", "1573", "abcd"),
 ("RET-TypeConfused", "green, p ~ 0.85", "1574", "abcd"),
 ("RET-VersionLied", "green, p ~ 0.85", "1575", "abcd"),
 ("W-HonestChainL0", "reachable in all four cases, p ~ 0.85", "1487", "abcd"),
 ("W-HonestChainL1", "reachable in all four cases, p ~ 0.85", "1487", "abcd"),
 ("W-HonestChainL2", "reachable in all four cases, p ~ 0.85", "1487", "abcd"),
 ("W-HonestAccepted", "reachable in all four cases, p ~ 0.85", "1487", "abcd"),
 ("W-HonestWrapped", "reachable in all four cases, p ~ 0.85", "1487", "abcd"),
 ("W-HonestStanding", "reachable in all four cases, p ~ 0.85", "1487", "abcd"),
 ("W-Agreed", "reachable in all four cases, p ~ 0.85", "1487", "abcd"),
 ("V-S1", "reachable in every correct-form run", "1516", "abd"),
 ("V-S2", "reachable in every correct-form run", "1516", "abd"),
 ("V-S3", "reachable in every correct-form run", "1516", "abd"),
 ("V-S4", "reachable in every correct-form run", "1516", "abd"),
 ("V-MIS", "reachable in every correct-form run", "1516", "abd"),
]
REDIN = {"link1b": "c", "RET-accept": "cd"}
CASEFILE = {"a": "capstone", "b": "capstone_b", "c": "cap_cc01_c", "d": "capstone_d"}


def want(key, cs):
    if key in WITNESS:
        return RE
    return R if cs in REDIN.get(key, "") else G


def colour(key, v):
    if key in WITNESS:
        return "REACHABLE" if v == "false" else "UNREACHABLE"
    return "GREEN" if v == "true" else "RED"


# ---------------------------------------------------------------------------------------------
# 4. The registration per companion per case.  red: list of requirements, each a tuple of keys
#    of which AT LEAST ONE must be red (C-Q3's two roles are one query).  either: keys the cell
#    leaves open (predicted neither way, or genuinely ambiguous - each one is named in `note`).
#    alt: a whole alternative red list (a registered fork).  vex: vocabulary witnesses
#    registered UNREACHABLE.  Every key not required red and not in `either` must be green; every
#    witness must be reachable (C-N1, PREDICTIONS.md:1503-1510), vocabulary witnesses except vex.
#    In (d) `AcceptS => IssuerSigned` is registered red in EVERY run (the A4.6 cost, :1580; §4
#    builder note (2), :1788-1791) and is added to every (d) requirement list below.
S = lambda *k: tuple(k)
Q3 = C_Q3
SPEC = {
 "cc01": {"row": "C-C1, §4 `:1770`", "c": dict(red=[S("RET-accept"), S("link1b")])},
 "cc02": {"row": "C-C2, §4 `:1771`",
          "a": dict(red=[], note="strict: set (1)'s C-Q3 and link 5 registered GREEN (three lists)"),
          "b": dict(red=[], note="as (a), predicted on channel symmetry"),
          "d": dict(red=[Q3, S("link5")])},
 "cc03": {"row": "C-C3, §4 `:1772`",
          "a": dict(red=[S("C-Q9"), S("link3")], note="strict MIXED: C-Q5 green"),
          "b": dict(red=[S("C-Q9"), S("link3")], note="as (a), predicted"),
          "d": dict(red=[S("C-Q5"), S("C-Q9"), S("link3")])},
 "cc04": {"row": "C-C4, §4 `:1773`",
          "a": dict(red=[S("C-Q4-Rescoped"), S("C-Q4-InnerSig"), Q3, S("link6b"), S("link5")], alt=[],
                    note="registered FORK: the five reds, or green throughout (predicted configuration-level reading)"),
          "b": dict(red=[S("C-Q4-Rescoped"), S("C-Q4-InnerSig"), Q3, S("link6b"), S("link5")], alt=[],
                    note="registered FORK, as (a)"),
          "d": dict(red=[S("C-Q4-Rescoped"), S("C-Q4-InnerSig"), Q3, S("link6b"), S("link5")])},
 "cc05": {"row": "C-C5, §4 `:1774`",
          "a": dict(red=[S("C-Q8"), S("link4")], note="strict MIXED: `InnerSigTransplanted` descended green"),
          "b": dict(red=[S("C-Q8"), S("link4")], note="strict MIXED, descended"),
          "d": dict(red=[S("C-Q4-InnerSig"), S("C-Q8"), S("link4")])},
 "cc06": {"row": "C-C6, §4 `:1775`",
          "a": dict(red=[], note="green control, predicted (round 9 disposition 4)"),
          "b": dict(red=[], note="green control, predicted"),
          "d": dict(red=[S("C-Q7"), S("C-Q4-InnerSig"), S("C-Q8"), S("link4")])},
 "cc07i": {"row": "C-C7(i), §4 `:1776`",
           "a": dict(red=[S("C-Q8"), S("link4"), S("RET-honestkey"), S("RET-accept")]),
           "b": dict(red=[S("C-Q8"), S("link4"), S("RET-honestkey"), S("RET-accept")]),
           "d": dict(red=[S("C-Q8"), S("link4"), S("RET-honestkey")])},
 "cc07ii": {"row": "C-C7(ii), §4 `:1776`",
            "a": dict(red=[S("C-Q8"), S("link4"), S("RET-honestkey"), S("RET-accept")],
                      note="C-Q7 GREEN in strict, a registered per-case outcome"),
            "b": dict(red=[S("C-Q8"), S("link4"), S("RET-honestkey"), S("RET-accept")]),
            "d": dict(red=[S("C-Q8"), S("link4"), S("C-Q7"), S("RET-honestkey")])},
 "cc08": {"row": "C-C8, §4 `:1777`",
          "a": dict(red=[S("C-Q9"), S("link3")], note="(beta)-only strict split: C-Q5 and link 5 green"),
          "b": dict(red=[S("C-Q9"), S("link3")], note="as (a), descended (cap22i)"),
          "d": dict(red=[S("C-Q9"), S("C-Q5"), S("link3"), S("link5")])},
 "cc08i": {"row": "C-C8-i, §9(2) `:2546`",
           "a": dict(red=[], note="isolation result: all green"),
           "b": dict(red=[], note="isolation result: all green"),
           "d": dict(red=[], either=["link5"],
                     note="link 5's `mh` half 'stays the registered (d) red' (:2546) is ambiguous for this configuration")},
 "cc08ii": {"row": "C-C8-ii, §9(2) `:2547`",
            "a": dict(red=[S("C-Q9")], either=["link3"],
                      note="link 3 not named in the cell; §3 link 3 says its producer 'is C-Q9' (:464)"),
            "b": dict(red=[S("C-Q9")], either=["link3"], note="as (a)"),
            "d": dict(red=[S("C-Q9")], either=["link3"], note="as (a)")},
 "cc09": {"row": "C-C9, §4 `:1778`",
          "a": dict(red=[S("link2b-B"), S("RET-Stripped")]),
          "b": dict(red=[S("link2b-B"), S("RET-Stripped")]),
          "d": dict(red=[S("link2b-B"), S("RET-Stripped")])},
 "cc10": {"row": "C-C10, §4 `:1779`",
          "a": dict(red=[S("link1a"), S("link1b"), S("RET-accept")]),
          "b": dict(red=[S("link1a"), S("link1b"), S("RET-accept")]),
          "d": dict(red=[S("link1a")])},
 "cc10iso": {"row": "C-C10 isolation control, §4 `:1779`",
             "a": dict(red=[S("link1a")], note="MIXED control: link 1a red, link 1b green"),
             "b": dict(red=[S("link1a")])},
 "cc11": {"row": "C-C11 (Q2), §4 `:1805`",
          "a": dict(red=[S("C-Q6-c1-unres"), S("C-Q6-c1-skI"), S("C-Q6-c1-skI2")]),
          "b": dict(red=[S("C-Q6-c1-unres"), S("C-Q6-c1-skI"), S("C-Q6-c1-skI2")]),
          "d": dict(red=[S("C-Q6-c1-skI"), S("C-Q6-c1-skI2")], note="(d) predicted; unrestricted form not asserted")},
 "cc11q4": {"row": "C-C11 alternate Q4, §4 `:1805`",
            "a": dict(red=[S("C-Q6-c1-unres"), S("C-Q6-c1-skI"), S("C-Q6-c1-skI2")], vex=["V-S2", "V-S4"]),
            "b": dict(red=[S("C-Q6-c1-unres"), S("C-Q6-c1-skI"), S("C-Q6-c1-skI2")], vex=["V-S2", "V-S4"]),
            "d": dict(red=[S("C-Q6-c1-skI"), S("C-Q6-c1-skI2")], vex=["V-S2", "V-S4"])},
 "cc11abl6": {"row": "C-C11 alternate abl6, §4 `:1805`",
              "a": dict(red=[S("C-Q6-c1-unres"), S("C-Q6-c1-skI"), S("C-Q6-c1-skI2")]),
              "b": dict(red=[S("C-Q6-c1-unres"), S("C-Q6-c1-skI"), S("C-Q6-c1-skI2")]),
              "d": dict(red=[S("C-Q6-c1-skI"), S("C-Q6-c1-skI2")])},
 "cc12": {"row": "C-C12, §4 `:1806`",
          "a": dict(red=[S("C-Q6-c2"), S("C-Q6-c1-unres")], note="unrestricted form red as the registered consequence (§3 C-Q6 §(6))"),
          "b": dict(red=[S("C-Q6-c2"), S("C-Q6-c1-unres")]),
          "d": dict(red=[S("C-Q6-c2")])},
 "cc13i": {"row": "C-C13(i), §9(1) `:2501`",
           "a": dict(red=[S("link6a"), S("RET-TypeConfused")]),
           "b": dict(red=[S("link6a"), S("RET-TypeConfused")]),
           "d": dict(red=[S("link6a"), S("RET-TypeConfused")])},
 "cc13ii": {"row": "C-C13(ii), §9(1) `:2501`",
            "a": dict(red=[S("link6a"), S("RET-TypeConfused")], note="per-layer claim (wrapper layers only) not observable: B-2"),
            "b": dict(red=[S("link6a"), S("RET-TypeConfused")]),
            "d": dict(red=[S("link6a"), S("RET-TypeConfused")])},
 "cc14": {"row": "C-C14, §9(1) `:2502`",
          "a": dict(red=[S("C-Q2"), S("link1a"), S("link1b"), S("RET-accept")],
                    note="the spike's one combined formula; 'this file predicts no different answer than all three'"),
          "b": dict(red=[S("C-Q2"), S("link1a"), S("link1b"), S("RET-accept")])},
 "cc15i": {"row": "C-C15(i), §9(1) `:2503`",
           "a": dict(red=[S("C-Q9"), S("link3"), S("link1a"), S("link1b"), S("link2a"), S("link5"),
                          S("C-Q5"), S("RET-SignerForged")], either=["C-Q6-c3"],
                     note="strict: the eight (seven relations) descended red; `Rescoped`, `InnerSigTransplanted`, C-Q3, `TypeConfused`, C-Q7, C-Q8 descended green; link 6b not produced in strict; C-Q6 c3 for (i) in strict is not case-assigned (set (1) says both configurations red it; the D11 sentence says the key half is severed by nothing the strict fixture can present)"),
           "b": dict(red=[S("C-Q9"), S("link3"), S("link1a"), S("link1b"), S("link2a"), S("link5"),
                          S("C-Q5"), S("RET-SignerForged")], either=["C-Q6-c3"], note="as (a)"),
           "d": dict(red=[S("link6b"), S("C-Q4-Rescoped"), Q3, S("link5"), S("C-Q7"), S("C-Q4-InnerSig"),
                          S("C-Q6-c3"), S("link1a"), S("link2a"), S("C-Q5"), S("RET-SignerForged"),
                          S("C-Q9"), S("link3")],
                     note="(d): set (1) plus the round-10/11 predicted reds (the eight less link 1b); `InnerSigTransplanted` from set (1)'s set-completeness note")},
 "cc15ii": {"row": "C-C15(ii), §9(1) `:2503`",
            "a": dict(red=[S("link6b"), S("C-Q4-Rescoped"), S("C-Q6-c3")], alt=[],
                      note="registered FORK, predicted neither way: red if the depth-2 honest route exists, else green throughout"),
            "b": dict(red=[S("link6b"), S("C-Q4-Rescoped"), S("C-Q6-c3")], alt=[], note="FORK, as (a)"),
            "d": dict(red=[S("link6b"), S("C-Q4-Rescoped"), S("C-Q6-c3")])},
 "cc15iii": {"row": "C-C15(iii), §9(1) `:2503`",
             "a": dict(red=[S("C-Q4-Rescoped"), S("link6b"), S("C-Q6-c3"), S("OBS-identity")]),
             "b": dict(red=[S("C-Q4-Rescoped"), S("link6b"), S("C-Q6-c3"), S("OBS-identity")]),
             "d": dict(red=[S("C-Q4-Rescoped"), S("link6b"), S("C-Q6-c3"), S("OBS-identity")])},
 "cc16": {"row": "C-C16, §9(3) `:2609`",
          "a": dict(red=[S("link5"), S("RET-Spliced")]), "b": dict(red=[S("link5"), S("RET-Spliced")]),
          "d": dict(red=[S("link5"), S("RET-Spliced")])},
 "cc17": {"row": "C-C17, §9(4) `:2666`",
          "a": dict(red=[S("link2a"), S("RET-SignerForged")], note="`PossessionTransplanted` (set 1) is not a capstone query: B-3"),
          "b": dict(red=[S("link2a"), S("RET-SignerForged")]),
          "d": dict(red=[S("link2a"), S("RET-SignerForged")])},
 "cc18": {"row": "C-C18, §9(5) `:2725`",
          "a": dict(red=[S("C-Q10"), S("C-Q6-c1-skI"), S("C-Q6-c1-unres")]),
          "b": dict(red=[S("C-Q10"), S("C-Q6-c1-skI"), S("C-Q6-c1-unres")]),
          "d": dict(red=[S("C-Q10"), S("C-Q6-c1-skI")])},
}
FORKS = {("cc04", "a"), ("cc04", "b"), ("cc15ii", "a"), ("cc15ii", "b")}
NOT_STATED = {"c": ["C-Q2", "C-Q10", "C-Q6-c1-unres", "C-Q6-c1-skI", "C-Q6-c1-skI2", "C-Q6-c2",
                    "C-Q6-c3"] + VOCAB_W}


def judge(comp, cs, d):
    """Return (verdict, divergences list, fired list, notes)."""
    sp = SPEC[comp][cs]
    reqs = list(sp.get("red", []))
    if cs == "d":
        reqs = reqs + [S("RET-accept")]
    either = set(sp.get("either", []))
    vex = set(sp.get("vex", []))
    ns = set(NOT_STATED.get(cs, []))

    def evaluate(reqs):
        div = []
        need = set(k for r in reqs for k in r)
        for r in reqs:
            decl = [k for k in r if k in d]
            if not decl:
                div.append("registered red %s **not declared** in the file" % "/".join(NAME[k] for k in r))
            elif not any(d[k][1] == "false" for k in decl):
                div.append("registered red %s **did not fire** (%s)" % (
                    "/".join(NAME[k] for k in r), ", ".join("`:%d` `is %s`" % (d[k][0], d[k][1]) for k in decl)))
        for k in SAFETY:
            if k in d and d[k][1] == "false" and k not in need and k not in either and k not in ns:
                if k in C_Q3 and any(set(r) == set(C_Q3) for r in reqs):
                    continue
                div.append("**red not registered in this case:** %s `:%d`" % (NAME[k], d[k][0]))
        for k in WITNESS:
            if k not in d or k in ns:
                continue
            reach = d[k][1] == "false"
            if k in vex:
                if reach:
                    div.append("vocabulary witness %s registered UNREACHABLE but reachable `:%d`" % (NAME[k], d[k][0]))
            elif not reach:
                kind = "honest-flow" if k in HONEST_W else "vocabulary"
                div.append("**dead %s witness:** %s `:%d`" % (kind, NAME[k], d[k][0]))
        return div

    div = evaluate(reqs)
    branch = ""
    if (comp, cs) in FORKS:
        div_green = evaluate([])
        if not div:
            branch = "fork branch: the registered reds"
        elif not div_green:
            div, branch = [], "fork branch: green throughout"
        else:
            branch = "matches neither fork branch; divergences stated against the red branch"
    fired = [k for k in SAFETY if k in d and d[k][1] == "false" and k not in ns]
    return div, fired, branch


# ---------------------------------------------------------------------------------------------
PREDBOX = {
 "cc01": (30, "retained `Accept => IssuerSigned`"), "cc02": (45, "C-Q3"), "cc03": (45, "C-Q5 / link 3"),
 "cc04": (45, "link 6b / C-Q3"), "cc05": (45, "link 4"), "cc06": (45, "C-Q7 / link 4"),
 "cc07i": (30, "retained honest-key authorship"), "cc07ii": (45, "link 4"), "cc08": (45, "C-Q5 / link 3"),
 "cc08i": (60, "C-Q9 (§9(2))"), "cc08ii": (60, "C-Q9 (§9(2))"), "cc09": (30, "retained `Stripped`"),
 "cc10": (30, "retained `Accept => IssuerSigned`"), "cc10iso": (45, "link 1a"), "cc11": (90, "C-Q6"),
 "cc11q4": (90, "C-Q6"), "cc11abl6": (90, "C-Q6"), "cc12": (90, "C-Q6"),
 "cc13i": (30, "retained `TypeConfused`"), "cc13ii": (30, "retained `TypeConfused`"),
 "cc14": (30, "retained `Accept => IssuerSigned`"), "cc15i": (30, "retained `SignerForged`"),
 "cc15ii": (45, "link 6b"), "cc15iii": (45, "link 6b"), "cc16": (30, "retained `Spliced`"),
 "cc17": (30, "retained `SignerForged`"), "cc18": (30, "C-Q10"),
}
ORDER = ["cc01", "cc02", "cc03", "cc04", "cc05", "cc06", "cc07i", "cc07ii", "cc08", "cc08i", "cc08ii",
         "cc09", "cc10", "cc10iso", "cc11", "cc11q4", "cc11abl6", "cc12", "cc13i", "cc13ii", "cc14",
         "cc15i", "cc15ii", "cc15iii", "cc16", "cc17", "cc18"]


def lab(comp):
    m = re.match(r"cc(\d+)(.*)", comp)
    n, sfx = str(int(m.group(1))), m.group(2)
    sfx = {"i": "(i)", "ii": "(ii)", "iii": "(iii)", "iso": " isolation control", "q4": " alt. Q4",
           "abl6": " alt. abl6", "": ""}[sfx]
    if comp in ("cc08i", "cc08ii"):
        sfx = "-" + sfx.strip("()")
    return "C-C" + n + sfx


# ---------------------------------------------------------------------------------------------
MATRIX = [
 ("D1", "S-P3 Q2 `Reattributed`", ["C-Q3-A", "C-Q3-B"], ["cc02"], ["C-Q3-A", "C-Q3-B", "link5"]),
 ("D2", "S-P3 Q2 `Reattributed` (C-Q4 `Rescoped`)", ["C-Q4-Rescoped"], ["cc04"], ["C-Q4-Rescoped"]),
 ("D3", "S-P3 Q1(ii) chain correspondence", ["RET-accept"], ["cc01"], ["RET-accept"]),
 ("D4", "link 1b: S-P3 Q1(ii); link 1a: structural", ["link1a", "link1b"], ["cc01", "cc10"], ["link1b", "link1a"]),
 ("D5", "**C-Q7**", ["C-Q7"], ["cc05"], ["C-Q4-InnerSig"]),
 ("D6", "**C-Q8**, structural", ["C-Q8"], ["cc07i", "cc07ii"], ["C-Q8", "link4"]),
 ("D7", "S-P2 `Stripped` / `SignerForged` + Q6 `Spliced`", ["RET-Stripped", "RET-SignerForged", "RET-Spliced"],
  ["cc09", "cc16", "cc17"], ["link2b-B", "link5", "link2a"]),
 ("D8", "S-P7 `TypeConfused`", ["RET-TypeConfused"], ["cc13i", "cc13ii"], ["link6a"]),
 ("D9", "first-link Q4 `TwoWorldsBroken`", ["C-Q2"], ["cc14"], ["C-Q2"]),
 ("D10", "**C-Q9**", ["C-Q9"], ["cc03", "cc08"], ["C-Q5", "C-Q9"]),
 ("D11", "S-P7 `Rescoped` (link 6b)", ["link6b"], ["cc15i", "cc15ii", "cc15iii"], ["link6b"]),
 ("D12", "S-STANDING `Established => Designated`", ["C-Q6-c1-skI"], ["cc11"], ["C-Q6-c1-skI"]),
 ("D13", "S-STANDING `StandingUnentitled`", ["C-Q6-c2"], ["cc12"], ["C-Q6-c2"]),
]



def section1():
    out = ["| Registered query | Registered prediction (`PREDICTIONS.md` line) | Case | Observed (`.out` line, verdict) | Outcome in the registered vocabulary |",
           "|---|---|---|---|---|"]
    tally = collections.Counter()
    for key, pred, line, cases in P:
        for cs in "abcd":
            stem = CASEFILE[cs]
            if cs not in cases:
                continue
            disp, _, _ = final(stem)
            if disp != "landed":
                out.append("| %s | %s (`:%s`) | (%s) | %s | %s |" % (NAME[key], pred, line, cs, "no result", outcome(stem)))
                tally["failed"] += 1
                continue
            d = PARSED[stem]
            if key not in d:
                out.append("| %s | %s (`:%s`) | (%s) | not declared in `%s.pv` | **not observable** |" % (NAME[key], pred, line, cs, stem))
                tally["undeclared"] += 1
                continue
            n, v = d[key]
            w = want(key, cs)
            ok = (w == G and v == "true") or (w in (R, RE) and v == "false")
            tally["as" if ok else "miss"] += 1
            verdict = "**as registered**" if ok else "**MISSED the registered branch**"
            if key in WITNESS:
                verdict = "**as registered**" if ok else "**DEAD WITNESS — broken fixture under C-N1**"
            lay = ""
            if key in ("W-HonestStanding", "W-Agreed") and v == "false":
                ly = LAYERS[stem].get(key)
                lay = "; trace at `%s` (`:%d`)" % (ly[1], ly[0]) if ly else "; trace layer NOT FOUND"
            out.append("| %s | %s (`:%s`) | (%s) | `%s.out:%d` `is %s` — %s%s | %s |" % (
                NAME[key], pred, line, cs, stem, n, v, colour(key, v), lay, verdict))
    out.append("")
    out.append("**Tally:** %d cells as registered, %d missed, %d not declared, %d from a run that did not land." %
               (tally["as"], tally["miss"], tally["undeclared"], tally["failed"]))
    return "\n".join(out), tally


def companions():
    rows = ["| Companion / configuration | Case | `rc`, seconds, peak (ladder 3 log line) | Inside the box of its predicted-red query? | Observed reds (`.out` line) | Witnesses |",
            "|---|---|---|---|---|---|"]
    vrows = ["| Companion / configuration (registration) | Case | Required red in this case, per its Cases cell (everything else declared must be green; every witness reachable) | Verdict against §4 / §9 | Divergences, exactly (broken-fixture-or-finding items under §4, listed and not resolved) | Note from the Cases cell |",
             "|---|---|---|---|---|---|"]
    counts = collections.defaultdict(collections.Counter)
    divlist = []
    for comp in ORDER:
        for cs in "abcd":
            stem = "cap_%s_%s" % (comp, cs)
            if stem not in STEMS:
                continue
            sp = SPEC[comp].get(cs)
            disp, rcc = runcell(stem)
            pb, why = PREDBOX[comp]
            _, _, dd = final(stem)
            secs = int(dd.get("seconds", "0") or 0)
            if disp == "not run":
                inside = "- (not run)"
            else:
                inside = ("yes, %d s <= %d min (%s)" % (secs, pb, why) if (disp == "landed" and secs <= pb * 60)
                          else "**no**, %d s > %d min (%s)" % (secs, pb, why))
            label = "**%s** — %s" % (lab(comp), SPEC[comp]["row"])
            req = "; ".join(" or ".join(NAME[k] for k in r) for r in sp.get("red", [])) or "none (green throughout)"
            if cs == "d":
                req += "; baseline `AcceptS => IssuerSigned`"
            if (comp, cs) in FORKS:
                req = "FORK: {" + req + "} or green throughout"
            if sp.get("either"):
                req += "; left open: " + ", ".join(NAME[k] for k in sp["either"])
            if sp.get("vex"):
                req += "; registered UNREACHABLE: " + ", ".join(NAME[k] for k in sp["vex"])
            if disp != "landed":
                rows.append("| %s | (%s) | %s | %s | %s — no result | - |" % (label, cs, rcc, inside, NOTRUN_TXT if disp == "not run" else disp))
                vrows.append("| %s | (%s) | %s | %s | none: no result to compare | %s |" % (label, cs, req, NOTRUN_TXT if disp == "not run" else disp, sp.get("note", "") if sp else ""))
                counts[cs]["not run" if disp == "not run" else disp] += 1
                continue
            d = PARSED[stem]
            div, fired, branch = judge(comp, cs, d)
            ns = set(NOT_STATED.get(cs, []))
            reds = ", ".join("%s `:%d`" % (NAME[k], d[k][0]) for k in fired) or "none"
            wun = [k for k in WITNESS if k in d and d[k][1] != "false"]
            wit = ("all %d declared reachable" % len([k for k in WITNESS if k in d])) if not wun else \
                  "UNREACHABLE: " + ", ".join("%s `:%d`" % (NAME[k], d[k][0]) for k in wun)
            lys = [LAYERS[stem].get(k) for k in ("W-HonestStanding", "W-Agreed")]
            if all(lys):
                wit += "; standing traces at `%s`/`%s`" % (lys[0][1], lys[1][1])
            notst = [k for k in ns if k in SAFETY and k in d and d[k][1] == "false"]
            if notst:
                reds += "; *not stated for (%s):* %s" % (cs, ", ".join("%s `:%d`" % (NAME[k], d[k][0]) for k in notst))
            rows.append("| %s | (%s) | %s | %s | %s | %s |" % (label, cs, rcc, inside, reds, wit))
            v = "**AS REGISTERED**" if not div else "**DIVERGENT**"
            if branch:
                v += " (%s)" % branch
            note = (sp.get("note", "") if sp else "")
            vrows.append("| %s | (%s) | %s | %s | %s | %s |" % (label, cs, req, v, "; ".join(div) or "none", note))
            counts[cs]["as registered" if not div else "divergent"] += 1
            for x in div:
                divlist.append((stem, x))
    return "\n".join(rows), "\n".join(vrows), counts, divlist


def matrix():
    out = ["| Row | Producer query; GREEN in the correct model? (`capstone.out`, case (a)) | Severing companion(s) | The severing key, per case, observed; and whether the registration expects it red in that case |",
           "|---|---|---|---|"]
    for row, prod, pk, comps, ck in MATRIX:
        pc = "; ".join("%s `capstone.out:%d` `is %s`" % (NAME[k], PARSED["capstone"][k][0], PARSED["capstone"][k][1]) for k in pk)
        cells = []
        for comp in comps:
            for cs in "abcd":
                stem = "cap_%s_%s" % (comp, cs)
                if stem not in STEMS:
                    continue
                disp, _, _ = final(stem)
                if disp != "landed":
                    cells.append("`%s`: %s" % (stem, outcome(stem)))
                    continue
                reqs = SPEC[comp][cs].get("red", [])
                need = set(k for r in reqs for k in r)
                parts = []
                for k in ck:
                    if k not in PARSED[stem]:
                        continue
                    n, v = PARSED[stem][k]
                    if (comp, cs) in FORKS:
                        exp = "registered FORK: red, or the configuration green throughout"
                    else:
                        exp = "registered red" if k in need else "registered green in this case" if k not in SPEC[comp][cs].get("either", []) else "left open"
                    parts.append("%s `:%d` %s (%s)" % (NAME[k], n, "**RED**" if v == "false" else "green", exp))
                cells.append("`%s`: %s" % (stem, "; ".join(parts)))
        out.append("| **%s** | %s — %s | %s | %s |" % (row, prod, pc, ", ".join(lab(c) for c in comps), "<br>".join(cells)))
    return "\n".join(out)


# ---------------------------------------------------------------------------------------------
# Cross-check: ladder 2 against ladder 3, per file and per keyed query.
BF56_KEYS = {"C-Q6-c1-unres", "C-Q6-c1-skI", "C-Q6-c1-skI2", "C-Q6-c2", "C-Q6-c3",
             "W-HonestStanding", "W-Agreed"}


def explain(stem, key):
    why = []
    if key in BF56_KEYS:
        why.append("BF-5/BF-6 (standing path / standing witnesses, every file)")
    if stem.startswith("cap_cc07i_"):
        why.append("BF-7 (C-C7(i) frame pattern)")
    return " or ".join(why) if why else "UNEXPLAINED"


def results(path):
    return [l.rstrip() for l in open(path, errors="replace") if l.startswith("RESULT")]


def crosscheck():
    out = ["| File | Ladder-2 disposition (`ladder2/ladder.log` line) | Ladder-3 disposition (`ladder.log` line) | RESULT lines, ladder 2 / ladder 3 | Comparison | Per-query verdicts |",
           "|---|---|---|---|---|---|"]
    tally = collections.Counter()
    changed = []
    groups = collections.defaultdict(list)
    tsv = ["stem\tl2disp\tl2lines\tl3disp\tl3lines\tn2\tn3\tcomparison\tqueries_same\tqueries_changed\tqueries_new\tqueries_gone"]
    for stem in STEMS:
        d2, l2l, _ = final2(stem)
        d3, l3l, _ = final(stem)
        p2 = os.path.join(L2, stem + ".out")
        p3 = os.path.join(PROV, stem + ".out")
        raw2 = results(p2) if (d2 == "landed" and os.path.exists(p2)) else []
        raw3 = results(p3) if d3 == "landed" else []
        l2c = "%s %s" % (d2, ", ".join("`:%d`" % n for n in l2l))
        l3c = "%s %s" % (d3, ", ".join("`:%d`" % n for n in l3l))
        same = chg = new = gone = 0
        qtxt = "-"
        if d3 == "not run":
            c = "not run under ladder 3; ladder-2 outcome is history only"
            tally["not-run-l3"] += 1
        elif d2 != "landed":
            c = "**NEW**: no ladder-2 result"
            tally["new"] += 1
        else:
            if raw2 == raw3:
                c = "**identical** (byte-for-byte)"; tally["identical"] += 1
            elif [norm(x) for x in raw2] == [norm(x) for x in raw3]:
                c = "identical after variable-suffix normalisation"; tally["identical-normalised"] += 1
            else:
                c = "**DIFFERENT**"; tally["different"] += 1
            q2, q3 = PARSED2[stem], PARSED[stem]
            for k in sorted(set(q2) | set(q3)):
                if k in q2 and k in q3:
                    if q2[k][1] == q3[k][1]:
                        same += 1
                    else:
                        chg += 1
                        changed.append((stem, k, q2[k], q3[k], explain(stem, k)))
                elif k in q3:
                    new += 1
                    changed.append((stem, k, None, q3[k], "NEW QUERY: " + explain(stem, k)))
                else:
                    gone += 1
                    changed.append((stem, k, q2[k], None, "QUERY GONE: " + explain(stem, k)))
            qtxt = "%d same, %d changed, %d new, %d gone" % (same, chg, new, gone)
            tally["q-same"] += same; tally["q-changed"] += chg; tally["q-new"] += new; tally["q-gone"] += gone
        kind = "identical" if c.startswith("**identical**") and not chg and not new and not gone else \
               "not-run" if d3 == "not run" else "other"
        groups[kind].append((stem, len(raw3), same))
        if kind == "other":
            out.append("| `%s` | %s | %s | %d / %d | %s | %s |" % (stem, l2c, l3c, len(raw2), len(raw3), c, qtxt))
        tsv.append("\t".join(str(x) for x in (stem, d2, ",".join(map(str, l2l)), d3, ",".join(map(str, l3l)),
                                               len(raw2), len(raw3), c.replace("*", ""), same, chg, new, gone)))
    # Compact form (2026-10-06, to keep RESULTS.md from growing): the table lists only files that are
    # neither byte-identical with every query verdict unchanged nor not run; the per-file rows for all
    # 80 are in dev/l3/crosscheck.tsv.
    if len(out) == 2:
        out = ["*No file is in the exception table: every file is either identical or not run.*"]
    else:
        out.insert(0, "Files that are not byte-identical, or whose query verdicts differ, or that are new:\n")
    out.append("")
    out.append("**Identical byte for byte, every keyed verdict the same (%d files, %d verdicts):** %s." % (
        len(groups["identical"]), sum(x[2] for x in groups["identical"]),
        ", ".join("`%s`" % st for st, n, _ in groups["identical"])))
    out.append("")
    out.append("**Not run under ladder 3 (%d files):** %s." % (
        len(groups["not-run"]), ", ".join("`%s`" % st for st, _, _ in groups["not-run"])))
    return "\n".join(out), tally, changed, tsv


def linemap():
    """ladder-2 RESULT line -> ladder-3 RESULT line, by position, for every file landed in both."""
    rows = ["stem\tkey\tl2line\tl3line\tl2verdict\tl3verdict"]
    M = {}
    for stem in STEMS:
        if stem in PARSED and stem in PARSED2:
            for k in PARSED[stem]:
                if k in PARSED2[stem]:
                    M[(stem, PARSED2[stem][k][0])] = PARSED[stem][k][0]
                    rows.append("%s\t%s\t%d\t%d\t%s\t%s" % (stem, k, PARSED2[stem][k][0], PARSED[stem][k][0],
                                                            PARSED2[stem][k][1], PARSED[stem][k][1]))
    return M, rows


# ---------------------------------------------------------------------------------------------
def _secs(runs):
    return sum(int(dd.get("seconds", "0") or 0) for rs in runs.values() for _, dd in rs)


def ceiling():
    CEIL = 4740 * 60
    s1 = _secs(L1RUNS)
    s2 = _secs(L2RUNS) + sum(int(dd.get("seconds", "0") or 0) for _, rs in SUPERSEDED2.values() for _, dd in rs)
    s3 = _secs(L3RUNS)
    by3 = collections.Counter()
    for rs in L3RUNS.values():
        for _, dd in rs:
            by3[dd.get("rc")] += int(dd.get("seconds", "0") or 0)
    n3 = collections.Counter(dd.get("rc") for rs in L3RUNS.values() for _, dd in rs)
    tot = s1 + s2 + s3
    return dict(CEIL=CEIL, s1=s1, s2=s2, s3=s3, tot=tot, by3=dict(by3), n3=dict(n3),
                pct1=100.0 * s1 / CEIL, pct2=100.0 * s2 / CEIL, pct3=100.0 * s3 / CEIL,
                pct=100.0 * tot / CEIL, x=tot / CEIL, over=tot - CEIL)


# ---------------------------------------------------------------------------------------------
PARSED, PARSED2, LAYERS = {}, {}, {}
for st in STEMS:
    if final(st)[0] == "landed":
        p = os.path.join(PROV, st + ".out")
        if not os.path.exists(p):
            sys.exit("LANDED WITHOUT OUTPUT %s" % st)
        PARSED[st] = parse(p)
        LAYERS[st] = standing_layers(p)
    elif final(st)[0] != "not run":
        sys.exit("UNEXPECTED LADDER-3 DISPOSITION %s %s" % (st, final(st)[0]))
    if final2(st)[0] == "landed":
        PARSED2[st] = parse(os.path.join(L2, st + ".out"))


def partials2():
    """Ladder-2 partial lines of the eleven: history only."""
    out = []
    for st in STEMS:
        if final(st)[0] != "not run":
            continue
        p = os.path.join(L2, st + ".out")
        d = parse(p) if os.path.exists(p) else {}
        items = ", ".join("%s `ladder2/%s.out:%d` `is %s`" % (NAME[k], st, n, v) for k, (n, v) in sorted(d.items(), key=lambda x: x[1][0]))
        out.append("- `%s` (ladder 2, %s): %s" % (st, final2(st)[0], items or "no RESULT line before the run ended"))
    return "\n".join(out)


def build():
    s1, t1 = section1()
    comp, ver, counts, divlist = companions()
    mx = matrix()
    xc, xt, changed, xtsv = crosscheck()
    ce = ceiling()
    landed = [s for s in STEMS if final(s)[0] == "landed"]
    notrun = [s for s in STEMS if final(s)[0] == "not run"]
    return dict(s1=s1, t1=t1, comp=comp, ver=ver, counts=counts, divlist=divlist, mx=mx, xc=xc, xt=xt,
                changed=changed, xtsv=xtsv, ce=ce, landed=landed, notrun=notrun, partials=partials2())


def replace(s, a, b, body):
    i, j = s.index(a), s.index(b)
    return s[:i] + a + "\n" + body + "\n" + s[j:]


if __name__ == "__main__":
    B = build()
    c = B["counts"]
    summ = []
    for cs in "abcd":
        if c[cs]:
            summ.append("(%s): %d as registered, %d divergent, %d not run under this blob" % (
                cs, c[cs]["as registered"], c[cs]["divergent"], c[cs]["not run"]))
    VERDICT = (B["ver"] + "\n\n**Counts, per case** (one row per configuration file): " + "; ".join(summ) + ".")
    ce = B["ce"]
    xt = B["xt"]
    chg = B["changed"]
    XC_TALLY = ("**Tally, per file:** %d identical byte for byte, %d identical after normalisation, %d different, "
                "%d new, %d not run under ladder 3. **Per query** (files landed in both): %d verdicts the same, "
                "%d changed, %d new, %d gone." % (xt["identical"], xt["identical-normalised"], xt["different"],
                                                   xt["new"], xt["not-run-l3"], xt["q-same"], xt["q-changed"],
                                                   xt["q-new"], xt["q-gone"]))
    if chg:
        XC_TALLY += "\n\n**Changed, each with its explanation:**\n" + "\n".join(
            "- `%s` %s: ladder 2 %s, ladder 3 %s — %s" % (st, NAME[k], a and "`:%d` `is %s`" % a, b and "`:%d` `is %s`" % b, why)
            for st, k, a, b, why in chg)
    else:
        XC_TALLY += " **No verdict changed, so none needs a BF to explain it, and none is UNEXPLAINED.**"
    M, lm = linemap()
    os.makedirs(OUTD, exist_ok=True)
    open(os.path.join(OUTD, "linemap.tsv"), "w").write("\n".join(lm) + "\n")
    open(os.path.join(OUTD, "crosscheck.tsv"), "w").write("\n".join(B["xtsv"]) + "\n")
    wl = ["stem\tHonestStandingEstablished_layer\tline\tHonestWrappedStandingAgreed_layer\tline"]
    for st in sorted(LAYERS):
        a, b = LAYERS[st].get("W-HonestStanding"), LAYERS[st].get("W-Agreed")
        wl.append("%s\t%s\t%s\t%s\t%s" % (st, a and a[1], a and a[0], b and b[1], b and b[0]))
    open(os.path.join(OUTD, "witness_layers.tsv"), "w").write("\n".join(wl) + "\n")
    lay_tally = collections.Counter((k, v[1]) for st in LAYERS for k, v in LAYERS[st].items() if v)
    with open(os.path.join(OUTD, "print.txt"), "w") as f:
        for part in (B["s1"], B["comp"], VERDICT, B["mx"], B["xc"], XC_TALLY, B["partials"]):
            f.write(part + "\n\n")
        f.write("CEILING %r\n" % (ce,))
        f.write("NOTRUN_DUPS %r\n" % (NOTRUN_DUPS,))
        f.write("LAYER_TALLY %r\n" % (dict(lay_tally),))
        f.write("LANDED %d NOTRUN %d STEMS %d\n" % (len(B["landed"]), len(B["notrun"]), len(STEMS)))
        for x in B["divlist"]:
            f.write("DIV %r\n" % (x,))
    print("dev/l3/ outputs written; counts:", "; ".join(summ))
    print("crosscheck:", dict(xt), "changed:", len(chg))
    print("ceiling:", ce)
    print("NOT-RUN duplicates collapsed:", NOTRUN_DUPS)
    print("standing-witness layers:", dict(lay_tally))
    if "--print" in sys.argv:
        sys.exit(0)
    s = open(RES).read()
    s = replace(s, "<!--S1-->", "<!--END-S1-->", B["s1"])
    s = replace(s, "<!--S2-->", "<!--END-S2-->", B["comp"])
    s = replace(s, "<!--VERDICTS-->", "<!--END-VERDICTS-->", VERDICT)
    s = replace(s, "<!--S3-->", "<!--END-S3-->", B["mx"])
    s = replace(s, "<!--CROSSCHECK-->", "<!--END-CROSSCHECK-->", B["xc"] + "\n\n" + XC_TALLY)
    s = replace(s, "<!--PARTIALS-->", "<!--END-PARTIALS-->", B["partials"])
    nl = ("**Landed under ladder 3 (%d of %d):** %s\n\n**Not run under this blob (%d of %d); the ladder-2 outcome is history:** %s" % (
        len(B["landed"]), len(STEMS), ", ".join("`%s`" % f for f in B["landed"]),
        len(B["notrun"]), len(STEMS), ", ".join("`%s` (ladder 2: %s)" % (f, final2(f)[0]) for f in B["notrun"])))
    s = replace(s, "<!--NOTRUNLIST-->", "<!--END-NOTRUNLIST-->", nl)
    open(RES, "w").write(s)
    print("RESULTS.md regions written")
