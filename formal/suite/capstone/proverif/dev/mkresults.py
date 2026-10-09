#!/usr/bin/env python3
"""Development helper (scratch): turns the .out files into the RESULTS.md
   tables.  It transcribes; it decides nothing.  The registered predictions
   below are quoted from PREDICTIONS.md with their line numbers; the observed
   columns are read off the .out files by summarize.py's keys."""
import os, subprocess, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
PROV = os.path.abspath(os.path.join(HERE, ".."))

# key -> (registered prediction as PREDICTIONS.md states it, its line, polarity
#         wanted per case: dict case -> "green"/"red"/"reach"/"-")
G, R, RE, NA = "green", "red", "reachable", "not stated"
P = [
 ("link1a", "C-Q1 link 1a", "green, p ~ 0.8", "362",
    {"a": G, "b": G, "c": G, "d": G}),
 ("link1b", "C-Q1 link 1b", "`is true` in (a) and (b), p ~ 0.8; `is false` in (c)", "379",
    {"a": G, "b": G, "c": R, "d": NA}),
 ("link2a", "C-Q1 link 2a", "green, p ~ 0.8", "408",
    {"a": G, "b": G, "c": G, "d": G}),
 ("link2b-s0", "C-Q1 link 2b, signers0 conjunct", "all three conjuncts `is true`, p ~ 0.55", "447",
    {"a": G, "b": G, "c": G, "d": G}),
 ("link2b-A", "C-Q1 link 2b, signers1 slot-A conjunct", "all three conjuncts `is true`, p ~ 0.55", "447",
    {"a": G, "b": G, "c": G, "d": G}),
 ("link2b-B", "C-Q1 link 2b, signers1 slot-B conjunct", "all three conjuncts `is true`, p ~ 0.55", "447",
    {"a": G, "b": G, "c": G, "d": G}),
 ("C-Q7", "C-Q7 `SigTransplanted`", "green, p ~ 0.8", "1371",
    {"a": G, "b": G, "c": G, "d": G}),
 ("C-Q8", "C-Q8 `SigBytesUnbound`", "green, p ~ 0.75", "1391",
    {"a": G, "b": G, "c": G, "d": G}),
 ("C-Q9", "C-Q9 `PossessionUnbound`", "green, p ~ 0.8", "1408",
    {"a": G, "b": G, "c": G, "d": G}),
 ("link3", "C-Q1 link 3", "green, p ~ 0.8", "466",
    {"a": G, "b": G, "c": G, "d": G}),
 ("link4", "C-Q1 link 4", "green, p ~ 0.75", "479",
    {"a": G, "b": G, "c": G, "d": G}),
 ("link5", "C-Q1 link 5", "green, p ~ 0.65", "509",
    {"a": G, "b": G, "c": G, "d": G}),
 ("link6a", "C-Q1 link 6a", "green, p ~ 0.85", "527",
    {"a": G, "b": G, "c": G, "d": G}),
 ("link6b", "C-Q1 link 6b", "green, p ~ 0.8", "583",
    {"a": G, "b": G, "c": G, "d": G}),
 ("C-Q2", "C-Q2 `TwoWorldsBroken`", "green, p ~ 0.65", "599",
    {"a": G, "b": G, "c": NA, "d": NA}),
 ("C-Q3-A", "C-Q3 `ReattributedA`", "green, p ~ 0.8", "615",
    {"a": G, "b": G, "c": G, "d": G}),
 ("C-Q3-B", "C-Q3 `ReattributedB`", "green, p ~ 0.8", "615",
    {"a": G, "b": G, "c": G, "d": G}),
 ("C-Q4-Rescoped", "C-Q4 `Rescoped`", "both green, p ~ 0.75", "630",
    {"a": G, "b": G, "c": G, "d": G}),
 ("C-Q4-InnerSig", "C-Q4 `InnerSigTransplanted`", "both green, p ~ 0.75", "630",
    {"a": G, "b": G, "c": G, "d": G}),
 ("C-Q5", "C-Q5 `SetAltered`", "green, p ~ 0.8", "689",
    {"a": G, "b": G, "c": G, "d": G}),
 ("C-Q5w-1", "C-Q5w, one-signer set", "reachable, p ~ 0.85", "699",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("C-Q5w-2", "C-Q5w, two-signer set", "reachable, p ~ 0.85", "699",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("C-Q10", "C-Q10 `TagConfused`", "green, p ~ 0.85", "1459",
    {"a": G, "b": G, "c": NA, "d": G}),
 ("C-Q6-c1-unres", "C-Q6 conjunct 1, UNRESTRICTED", "all three conjuncts hold, p ~ 0.5; the unrestricted form is registered RED in (d), the A4.6 cost", "1324",
    {"a": G, "b": G, "c": NA, "d": NA}),
 ("C-Q6-c1-skI", "C-Q6 conjunct 1, honest key `skI`", "green in (a), (b) and (d)", "1233",
    {"a": G, "b": G, "c": NA, "d": G}),
 ("C-Q6-c1-skI2", "C-Q6 conjunct 1, honest key `skI2`", "green in (a), (b) and (d)", "1233",
    {"a": G, "b": G, "c": NA, "d": G}),
 ("C-Q6-c2", "C-Q6 conjunct 2 `StandingUnentitledWrapped`", "unreachable in (a), (b) and (d)", "1245",
    {"a": G, "b": G, "c": NA, "d": G}),
 ("C-Q6-c3", "C-Q6 conjunct 3 `ScopeMisreported`", "unreachable in (a), (b) and (d)", "1289",
    {"a": G, "b": G, "c": NA, "d": G}),
 ("RET-accept", "retained: `Accept => IssuerSigned` (strict) / `AcceptS => IssuerSigned` (d)", "green in (a)/(b) p ~ 0.85; RED in (c) p ~ 0.9; the degraded unrestricted form registered RED in (d), the A4.6 cost", "1569, 1580",
    {"a": G, "b": G, "c": R, "d": R}),
 ("RET-honestkey", "retained: `AcceptedUnderHonestKey => IssuerSigned`", "green, p ~ 0.85", "1570",
    {"a": G, "b": G, "c": G, "d": G}),
 ("RET-Stripped", "retained: `Stripped`", "green, p ~ 0.8", "1571",
    {"a": G, "b": G, "c": G, "d": G}),
 ("RET-SignerForged", "retained: `SignerForged`", "green, p ~ 0.8", "1572",
    {"a": G, "b": G, "c": G, "d": G}),
 ("RET-Spliced", "retained: `Spliced`", "green, p ~ 0.75", "1573",
    {"a": G, "b": G, "c": G, "d": G}),
 ("RET-TypeConfused", "retained: `TypeConfused`", "green, p ~ 0.85", "1574",
    {"a": G, "b": G, "c": G, "d": G}),
 ("RET-VersionLied", "retained: `VersionLied`", "green, p ~ 0.85", "1575",
    {"a": G, "b": G, "c": G, "d": G}),
 ("W-HonestChainL0", "C-N1 witness `HonestChain(L0, t)`", "reachable in all four cases, p ~ 0.85", "1487",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("W-HonestChainL1", "C-N1 witness `HonestChain(L1, t)`", "reachable in all four cases, p ~ 0.85", "1487",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("W-HonestChainL2", "C-N1 witness `HonestChain(L2, t)`", "reachable in all four cases, p ~ 0.85", "1487",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("W-HonestAccepted", "C-N1 witness `HonestAccepted`", "reachable in all four cases, p ~ 0.85", "1487",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("W-HonestWrapped", "C-N1 witness `HonestWrappedAccepted`", "reachable in all four cases, p ~ 0.85", "1487",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("W-HonestStanding", "C-N1 witness `HonestStandingEstablished`", "reachable in all four cases, p ~ 0.85", "1487",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("W-Agreed", "C-N1 witness `HonestWrappedStandingAgreed`", "reachable in all four cases, p ~ 0.85", "1487",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("V-S1", "vocabulary witness S1 (ESTABLISHED, TERMINAL_DISPOSITION_SHOWN)", "reachable in every correct-form run", "1516",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("V-S2", "vocabulary witness S2 (ABSENT, SUPERSEDED)", "reachable in every correct-form run", "1516",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("V-S3", "vocabulary witness S3 (ABSENT, NO_TERMINAL_DISPOSITION_EVIDENCE)", "reachable in every correct-form run", "1516",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("V-S4", "vocabulary witness S4 (ABSENT, ISSUANCE_REFUSED)", "reachable in every correct-form run", "1516",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
 ("V-MIS", "vocabulary witness MISMATCH (ABSENT, STANDING_EVIDENCE_MISMATCH)", "reachable in every correct-form run", "1516",
    {"a": RE, "b": RE, "c": RE, "d": RE}),
]

CASEFILE = {"a": "capstone.out", "b": "capstone_b.out",
            "c": "cap_cc01_c.out", "d": "capstone_d.out"}


def load():
    tsv = subprocess.run([sys.executable, os.path.join(HERE, "summarize.py")],
                         capture_output=True, text=True).stdout
    d = collections.defaultdict(dict)
    for ln in tsv.splitlines()[1:]:
        f, k, n, v = ln.split("\t")
        d[f][k] = (int(n), v)
    return d


def finished(fname):
    """A run is finished only when run_ladder.sh has logged its rc and seconds."""
    stem = fname[:-4]
    try:
        for ln in open(os.path.join(PROV, "ladder.log")):
            if ln.startswith(stem + " ") and " rc=" in ln:
                return True
    except IOError:
        pass
    return False


def obs(d, fname, key, want):
    """The observed cell: the .out line number, the ProVerif verdict, and the
       registered vocabulary the verdict falls under."""
    if fname not in d or not finished(fname):
        return "**not run** (this run had not landed when the file was written)"
    if key not in d[fname]:
        return "not declared in this case"
    n, v = d[fname][key]
    if v == "true":
        colour = "GREEN (unreachable / correspondence holds)"
    elif v == "false":
        colour = "RED" if want in (G,) else ("REACHABLE" if want == RE else "RED")
    else:
        colour = v
    return "`:%d` `is %s` -- %s" % (n, v, colour)


def landed(d, fname, key, want):
    if fname not in d or key not in d[fname] or not finished(fname):
        return None
    v = d[fname][key][1]
    if want == G:
        return v == "true"
    if want == R:
        return v == "false"
    if want == RE:
        return v == "false"
    return None


def main():
    d = load()
    secs = {}
    for ln in open(os.path.join(PROV, "ladder.log")):
        if " rc=" in ln:
            parts = ln.split()
            secs[parts[0]] = (parts[1], parts[2])
    print("| Registered query | Registered prediction (PREDICTIONS.md line) | Case | Observed (`.out` line, verdict) | Outcome in the registered vocabulary |")
    print("|---|---|---|---|---|")
    hit = miss = notrun = 0
    for key, name, pred, line, want in P:
        for cs in "abcd":
            w = want[cs]
            if w == NA:
                continue
            o = obs(d, CASEFILE[cs], key, w)
            L = landed(d, CASEFILE[cs], key, w)
            if L is None:
                verdict = "not run" if o == "not run" else "-"
                notrun += 1
            elif L:
                verdict = "**as registered**"; hit += 1
            else:
                verdict = "**MISSED the registered branch**"; miss += 1
            print("| %s | %s (`:%s`) | (%s) | %s | %s |" % (name, pred, line, cs, o, verdict))
    sys.stderr.write("landed=%d missed=%d notrun=%d\n" % (hit, miss, notrun))





# ---------------------------------------------------------------------------
# The companion table.  EXPECTED is set (1) of PREDICTIONS.md §4 / §9, written
# in this model's query keys.  A companion's row says which of its registered
# reds fired, which did not, and whether anything went red outside the set.
EXPECTED = {
 "cc01":    (["RET-accept", "link1b"], "C-C1 (§4 row), D3/D4"),
 "cc02":    (["C-Q3-A", "C-Q3-B", "link5"], "C-C2 (§4 row), D1"),
 "cc03":    (["C-Q5", "C-Q9", "link3"], "C-C3 (§4 row), D10"),
 "cc04":    (["C-Q4-Rescoped", "C-Q4-InnerSig", "C-Q3-A", "C-Q3-B", "link6b", "link5"],
             "C-C4 (§4 row), D2"),
 "cc05":    (["C-Q4-InnerSig", "C-Q8", "link4"], "C-C5 (§4 row), D5"),
 "cc06":    (["C-Q7", "C-Q4-InnerSig", "C-Q8", "link4"], "C-C6 (§4 row), D5/D6"),
 "cc07i":   (["C-Q8", "link4", "RET-honestkey"], "C-C7(i) (§4 row), D6"),
 "cc07ii":  (["C-Q8", "link4"], "C-C7(ii) (§4 row), D6"),
 "cc08":    (["C-Q9", "C-Q5", "link3", "link5"], "C-C8 (§4 row), D10"),
 "cc08i":   ([], "C-C8-i (§9(2)): the ISOLATION result is C-Q9 GREEN and C-Q5 GREEN"),
 "cc08ii":  (["C-Q9"], "C-C8-ii (§9(2)): C-Q9 RED by construction, C-Q5 GREEN"),
 "cc09":    (["link2b-B", "RET-Stripped"], "C-C9 (§4 row), D7 set/completeness"),
 "cc10":    (["link1a"], "C-C10 (§4 row), D4; in strict also link 1b and the unrestricted acceptance"),
 "cc10iso": (["link1a"], "C-C10's ISOLATION CONTROL (§4): link 1a RED, link 1b GREEN"),
 "cc11":    (["C-Q6-c1-unres", "C-Q6-c1-skI", "C-Q6-c1-skI2"], "C-C11 (§4 row), D12"),
 "cc11q4":  (["C-Q6-c1-unres", "C-Q6-c1-skI", "C-Q6-c1-skI2"],
             "C-C11 alternate Q4 (§4 row), D12; S2 and S4 vocabulary witnesses UNREACHABLE as a registered consequence"),
 "cc11abl6":(["C-Q6-c1-unres", "C-Q6-c1-skI", "C-Q6-c1-skI2"], "C-C11 alternate abl6 (§4 row), D12"),
 "cc12":    (["C-Q6-c2"], "C-C12 (§4 row), D13"),
 "cc13i":   (["link6a", "RET-TypeConfused"], "C-C13(i) (§9(1)), D8"),
 "cc13ii":  (["link6a", "RET-TypeConfused"], "C-C13(ii) (§9(1)), D8"),
 "cc14":    (["C-Q2", "link1a", "link1b", "RET-accept"], "C-C14 (§9(1)), D9"),
 "cc15i":   (["link6b", "C-Q4-Rescoped", "C-Q3-A", "C-Q7", "C-Q9", "link3",
              "link1a", "link1b", "link2a", "link5", "C-Q5", "RET-SignerForged"],
             "C-C15(i) (§9(1)), D11"),
 "cc15ii":  (["link6b", "C-Q4-Rescoped"], "C-C15(ii) (§9(1)), D11"),
 "cc15iii": (["link6b", "C-Q4-Rescoped", "C-Q6-c3", "OBS-identity"],
             "C-C15(iii) (§9(1)), D11 isolation; the observer OBS-key must stay UNREACHABLE"),
 "cc16":    (["link5", "RET-Spliced"], "C-C16 (§9(3)), D7 common content"),
 "cc17":    (["link2a", "RET-SignerForged"], "C-C17 (§9(4)), D7 membership"),
 "cc18":    (["C-Q10", "C-Q6-c1-skI"], "C-C18 (§9(5)), the composed D-6 tag property"),
}
SAFETY = [k for k, _, _, _, w in P if w["a"] in (G, R)]
WITNESS = [k for k, _, _, _, w in P if w["a"] == RE]


# The box of the query each companion is predicted to red (§3's timebox table,
# read through §4's "a companion runs inside the box of the query it is
# predicted to red").  Where a companion is predicted to red more than one
# query, the STRICTEST reading is taken: the SMALLEST of their boxes, named.
PREDBOX = {
 "cc01":    (30, "the retained `Accept => IssuerSigned`, 30 min (link 1b's box is 45)"),
 "cc02":    (45, "C-Q3, 45 min (link 5's box is 60)"),
 "cc03":    (45, "C-Q5 and link 3, 45 min (C-Q9's box is 60)"),
 "cc04":    (45, "link 6b and C-Q3, 45 min (C-Q4's and link 5's are 60)"),
 "cc05":    (45, "link 4, 45 min (C-Q4's and C-Q8's are 60)"),
 "cc06":    (45, "C-Q7 and link 4, 45 min"),
 "cc07i":   (30, "the retained `AcceptedUnderHonestKey => IssuerSigned`, 30 min"),
 "cc07ii":  (45, "link 4, 45 min (C-Q8's is 60)"),
 "cc08":    (45, "C-Q5 and link 3, 45 min"),
 "cc08i":   (60, "C-Q9's 60 min — §9(2): the isolation runs run inside C-Q9's box"),
 "cc08ii":  (60, "C-Q9's 60 min — §9(2)"),
 "cc09":    (30, "the retained `Stripped`, 30 min (link 2b's box is 60)"),
 "cc10":    (30, "the retained `Accept => IssuerSigned` in strict, 30 min (link 1a's is 45)"),
 "cc10iso": (45, "link 1a, 45 min — §4: the control runs inside link 1a's existing box"),
 "cc11":    (90, "C-Q6, 90 min"),
 "cc11q4":  (90, "C-Q6, 90 min"),
 "cc11abl6":(90, "C-Q6, 90 min"),
 "cc12":    (90, "C-Q6, 90 min"),
 "cc13i":   (30, "the retained `TypeConfused`, 30 min (link 6a's is 45)"),
 "cc13ii":  (30, "the retained `TypeConfused`, 30 min (link 6a's is 45)"),
 "cc14":    (30, "the retained `Accept => IssuerSigned`, 30 min (C-Q2's and link 1a/1b's are 45)"),
 "cc15i":   (30, "the retained `SignerForged`, 30 min (link 6b's is 45, C-Q9's 60)"),
 "cc15ii":  (45, "link 6b, 45 min — §9(1): (ii) runs inside link 6b's box"),
 "cc15iii": (45, "link 6b, 45 min — §9(1): (iii) runs inside link 6b's 45-min and C-Q6's 90-min boxes"),
 "cc16":    (30, "the retained `Spliced`, 30 min (link 5's is 60)"),
 "cc17":    (30, "the retained `SignerForged`, 30 min (link 2a's is 45)"),
 "cc18":    (30, "C-Q10, 30 min — §4: C-C18 runs inside C-Q10's box"),
}


def ladderline(stem):
    try:
        for ln in open(os.path.join(PROV, "ladder.log")):
            if ln.startswith(stem + " ") and " rc=" in ln:
                d = dict(x.split("=", 1) for x in ln.split()[1:] if "=" in x)
                return d
    except IOError:
        pass
    return None


def companions():
    d = load()
    print()
    print("| Companion / configuration | Case | Registered expected failed set (§4 / §9) | `rc` / seconds, under the per-case-sum box | Inside the box of its predicted-red query? | Observed reds (`.out` line) | Registered reds that did NOT fire | Reds outside the set | Witnesses |")
    print("|---|---|---|---|---|---|---|---|---|")
    import glob
    allout = sorted(set(list(d) + [os.path.basename(x)[:-3] + ".out"
                        for x in glob.glob(os.path.join(PROV, "cap_*.pv"))]))
    for f in allout:
        if not f.startswith("cap_"):
            continue
        d.setdefault(f, {})
        name = f[4:-4]
        cs = name[-1]
        comp = name[:-2]
        exp, row = EXPECTED.get(comp, ([], "?"))
        pb, pbwhy = PREDBOX.get(comp, (0, "?"))
        ll = ladderline(f[:-4])
        if ll:
            secs = int(ll.get("seconds", "0"))
            rccol = "`rc=%s`, %d s (box %s)" % (ll.get("rc"), secs, ll.get("box"))
            inside = ("**yes**, %d s <= %d min" % (secs, pb) if secs <= pb * 60
                      else "**NO** — %d s exceeds %d min" % (secs, pb)) + " (%s)" % pbwhy
        else:
            rccol = "**not run**"
            inside = "not run (strict box would be %d min: %s)" % (pb, pbwhy)
        if not finished(f):
            print("| **%s** — %s | (%s) | %s | %s | %s | **not run** (this run had not landed when the file was written) | - | - | - |"
                  % (comp.upper(), row, cs,
                     ", ".join("`%s`" % k for k in exp) or "(the isolation result is all green)",
                     rccol, inside))
            continue
        reds = [k for k in SAFETY if k in d[f] and d[f][k][1] == "false"]
        fired = [k for k in exp if k in reds]
        missing = [k for k in exp if k not in reds and k in d[f]]
        absent = [k for k in exp if k not in d[f]]
        extra = [k for k in reds if k not in exp]
        wr = [k for k in WITNESS if k in d[f] and d[f][k][1] == "false"]
        wu = [k for k in WITNESS if k in d[f] and d[f][k][1] != "false"]
        print("| **%s** — %s | (%s) | %s | %s | %s | %s | %s | %s | reachable: %s%s |" % (
          comp.upper(), row, cs,
          ", ".join("`%s`" % k for k in exp) or "(the isolation result is all green)",
          rccol, inside,
          ", ".join("`%s` `:%d`" % (k, d[f][k][0]) for k in fired) or "none",
          (", ".join("`%s`" % k for k in missing) or "none") +
            (" (not declared in this case: " + ", ".join(absent) + ")" if absent else ""),
          ", ".join("`%s` `:%d`" % (k, d[f][k][0]) for k in extra) or "none",
          ", ".join(k.replace("W-", "").replace("V-", "") for k in wr) or "NONE",
          ("; UNREACHABLE: " + ", ".join(k.replace("W-", "").replace("V-", "") for k in wu)) if wu else ""))


# ---------------------------------------------------------------------------
# The discharge matrix, D1-D11 (§2(a)'s eleven rows) plus D12 and D13 (§2(c)'s
# standing-verdict rows, outside the matrix and outside its count).  Cells from
# PREDICTIONS.md §5.  For each row: which PRODUCER query went green, and which
# COMPANION went red -- or that it did not.
MATRIX = [
 ("D1",  "S-P3 Q2 `Reattributed`, transcribed", ["C-Q3-A", "C-Q3-B"], "C-C2",  ["C-Q3-A", "C-Q3-B", "link5"]),
 ("D2",  "S-P3 Q2 `Reattributed`, transcribed", ["C-Q4-Rescoped"],    "C-C4",  ["C-Q4-Rescoped"]),
 ("D3",  "S-P3 Q1(ii) chain correspondence",    ["RET-accept"],       "C-C1",  ["RET-accept"]),
 ("D4",  "link 1b: S-P3 Q1(ii); link 1a: structural", ["link1a", "link1b"], "C-C1 (1b) and C-C10 (1a)", ["link1b", "link1a"]),
 ("D5",  "**C-Q7**, registered here",           ["C-Q7"],             "C-C5",  ["C-Q4-InnerSig"]),
 ("D6",  "**C-Q8**, registered here, structural", ["C-Q8"],           "C-C7",  ["C-Q8", "link4"]),
 ("D7",  "S-P2 Q2 `Stripped` / `SignerForged` + Q6 `Spliced`",
         ["RET-Stripped", "RET-SignerForged", "RET-Spliced"],
         "C-C9 / C-C16 / C-C17", ["link2b-B", "link5", "link2a"]),
 ("D8",  "S-P7 Q2/Q1 `TypeConfused`",           ["RET-TypeConfused"], "C-C13", ["link6a"]),
 ("D9",  "first-link Q4 `TwoWorldsBroken`, both variants", ["C-Q2"],  "C-C14", ["C-Q2"]),
 ("D10", "**C-Q9**, registered here",           ["C-Q9"],             "C-C3",  ["C-Q5"]),
 ("D11", "S-P7 Q2/Q5 `Rescoped`",               ["link6b"],           "C-C15", ["link6b"]),
 ("D12", "S-STANDING Q1(i)/(ii) `Established => Designated`", ["C-Q6-c1-skI"], "C-C11", ["C-Q6-c1-skI"]),
 ("D13", "S-STANDING Q1(iii) `StandingUnentitled`", ["C-Q6-c2"],      "C-C12", ["C-Q6-c2"]),
]
COMPFILE = {"C-C1": "cap_cc01_c.out", "C-C2": "cap_cc02_a.out", "C-C3": "cap_cc03_a.out",
 "C-C4": "cap_cc04_a.out", "C-C5": "cap_cc05_a.out", "C-C7": "cap_cc07i_a.out",
 "C-C9 / C-C16 / C-C17": "cap_cc09_a.out", "C-C13": "cap_cc13i_a.out",
 "C-C14": "cap_cc14_a.out", "C-C15": "cap_cc15iii_a.out", "C-C11": "cap_cc11_a.out",
 "C-C12": "cap_cc12_a.out", "C-C1 (1b) and C-C10 (1a)": "cap_cc10_a.out"}


def matrix():
    d = load()
    print()
    print("| Row | Producer query, and whether it went GREEN in the correct model (case (a), `capstone.out`) | Severing companion | Whether it went RED, and where |")
    print("|---|---|---|---|")
    for row, prod, pkeys, comp, ckeys in MATRIX:
        pcells = []
        for k in pkeys:
            e = d.get("capstone.out", {}).get(k)
            pcells.append("`%s` %s" % (k, ("`:%d` `is %s`" % e) if e else "not run"))
        f = COMPFILE.get(comp, "")
        ccells = []
        for k in ckeys:
            e = d.get(f, {}).get(k) if finished(f) else None
            if not e:
                ccells.append("`%s` **not run**" % k)
            else:
                ccells.append("`%s` `%s:%d` `is %s`%s" % (k, f, e[0], e[1],
                              " — **RED as required**" if e[1] == "false" else " — **DID NOT GO RED**"))
        print("| **%s** | %s — %s | **%s** | %s |" % (row, prod, "; ".join(pcells), comp, "; ".join(ccells)))


def _run():
    main()
    companions()
    matrix()


if __name__ == "__main__":
    _run()
