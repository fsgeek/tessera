#!/usr/bin/env python3
"""Development helper (scratch): reads every .out beside it and prints a TSV of
   file / registered-query key / .out line number / ProVerif verdict.
   It computes nothing and decides nothing; it only saves transcribing line
   numbers by hand into RESULTS.md.  Not a model, not a result."""
import os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(os.path.dirname(__file__) + "/x"))
OUTDIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

KEYS = [
 ("link1a",        "ChainBroken(l_1,LINK_1A)"),
 ("link1b",        "AuthorityPublishedDNS"),
 ("link2a",        "ChainBroken(l_1,LINK_2A)"),
 ("link2b-s0",     "signers0,alg_4,ver_4))) ==> event(SlotSatisfied"),
 ("link2b-A",      "signers1(fpB),alg_4,ver_4),fpA)"),
 ("link2b-B",      "signers1(fpB),alg_4,ver_4),fpB)"),
 ("C-Q7",          "SigTransplanted("),
 ("C-Q8",          "SigBytesUnbound("),
 ("C-Q9",          "PossessionUnbound("),
 ("link3",         "ChainBroken(l_1,LINK_3)"),
 ("link4",         "ChainBroken(l_1,LINK_4)"),
 ("link5",         "ChainBroken(l_1,LINK_5)"),
 ("link6a",        "ChainBroken(l_1,LINK_6A)"),
 ("link6b",        "ChainBroken(l_1,LINK_6B)"),
 ("C-Q2",          "TwoWorldsBroken("),
 ("C-Q3-A",        "ReattributedA("),
 ("C-Q3-B",        "ReattributedB("),
 ("C-Q4-Rescoped", "not event(Rescoped("),
 ("C-Q4-InnerSig", "InnerSigTransplanted("),
 ("C-Q5",          "SetAltered("),
 ("C-Q5w-1",       "signers0,algH[],verH[]),verified1"),
 ("C-Q5w-2",       "verified2(k1,k2)"),
 ("C-Q10",         "TagConfused("),
 ("C-Q6-c1-unres", "EstablishedWrapped(aid_6,lyr_12,t_9,kX_9,co,ESTABLISHED)"),
 ("C-Q6-c1-skI",   "EstablishedWrapped(aid_6,lyr_12,t_9,pk(skI[]),co,ESTABLISHED)"),
 ("C-Q6-c1-skI2",  "EstablishedWrapped(aid_6,lyr_12,t_9,pk(skI2[]),co,ESTABLISHED)"),
 ("C-Q6-c2",       "StandingUnentitledWrapped("),
 ("C-Q6-c3",       "ScopeMisreported("),
 ("RET-accept",    "==> event(IssuerSigned(k_1,fb_8))"),
 ("RET-honestkey", "AcceptedUnderHonestKey(k_1,fb_8)) ==>"),
 ("RET-Stripped",  "not event(Stripped("),
 ("RET-SignerForged", "not event(SignerForged("),
 ("RET-Spliced",   "not event(Spliced("),
 ("RET-TypeConfused", "not event(TypeConfused("),
 ("RET-VersionLied", "not event(VersionLied("),
 ("W-HonestChainL0", "HonestChain(L0,"),
 ("W-HonestChainL1", "HonestChain(L1,"),
 ("W-HonestChainL2", "HonestChain(L2,"),
 ("W-HonestAccepted", "not event(HonestAccepted("),
 ("W-HonestWrapped",  "HonestWrappedAccepted("),
 ("W-HonestStanding", "HonestStandingEstablished("),
 ("W-Agreed",         "HonestWrappedStandingAgreed("),
 ("V-S1",  "StandingReport(ESTABLISHED,TERMINAL_DISPOSITION_SHOWN"),
 ("V-S2",  "StandingReport(ABSENT,SUPERSEDED"),
 ("V-S3",  "StandingReport(ABSENT,NO_TERMINAL_DISPOSITION_EVIDENCE"),
 ("V-S4",  "StandingReport(ABSENT,ISSUANCE_REFUSED"),
 ("V-MIS", "StandingReport(ABSENT,STANDING_EVIDENCE_MISMATCH"),
 ("OBS-key",      "ScopeKeyOnly("),
 ("OBS-identity", "ScopeIdentityOnly("),
]


def main():
    files = sorted(glob.glob(os.path.join(OUTDIR, "*.out")))
    print("file\tkey\tline\tverdict")
    for path in files:
        base = os.path.basename(path)
        seen = {}
        for n, ln in enumerate(open(path, errors="replace"), 1):
            if not ln.startswith("RESULT"):
                continue
            verdict = ("true" if ln.rstrip().endswith("is true.")
                       else "false" if ln.rstrip().endswith("is false.")
                       else "cannot-be-proved" if "cannot be proved" in ln
                       else "?")
            for key, needle in KEYS:
                if needle in ln and key not in seen:
                    seen[key] = (n, verdict)
                    break
        for key, _ in KEYS:
            if key in seen:
                n, v = seen[key]
                print("%s\t%s\t%d\t%s" % (base, key, n, v))


if __name__ == "__main__":
    main()
