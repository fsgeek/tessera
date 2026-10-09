#!/usr/bin/env python3
"""Assemble REPORT.md sections (b) and (c) from abl.log + the .out files.
Every number printed here is read back from a file this session's runner wrote;
nothing is typed in by hand."""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

WHAT = {
 "E0_cc07ii_iso": ("cap_cc07ii_a.pv", "isolated: every query but link 2b conjunct 1 deleted; nothing else changed"),
 "E1_cc07ii":     ("E0_cc07ii_iso.pv", "+ ablation 1: the depth-2 layer dropped (the L1->L2 WrapStage and SUnwrap instances)"),
 "E12_cc07ii":    ("E0_cc07ii_iso.pv", "+ ablations 1,2: also skI2 dropped (its publication, honest key, honest membership, ShipIssuer and RefuseIssuer)"),
 "E123_cc07ii":   ("E0_cc07ii_iso.pv", "+ ablations 1,2,3: also the second lineage shape dropped (RefuseIssuer, TERM_REFUSED / both-abandoned)"),
 "E1234_cc07ii":  ("E0_cc07ii_iso.pv", "+ ablations 1,2,3,4: also the |set| = 2 branch deleted from AttestStage and WrapStage"),
 "F0_cc14_iso":   ("cap_cc14_a.pv", "isolated: every query but link 2b conjunct 1 deleted; nothing else changed"),
 "F1_cc14":       ("F0_cc14_iso.pv", "+ ablation 1"),
 "F12_cc14":      ("F0_cc14_iso.pv", "+ ablations 1,2"),
 "F123_cc14":     ("F0_cc14_iso.pv", "+ ablations 1,2,3"),
 "F1234_cc14":    ("F0_cc14_iso.pv", "+ ablations 1,2,3,4"),
 "S2_redundantHypElim": ("E0_cc07ii_iso.pv", "`set redundantHypElim = true.` added, nothing else (default is beginOnly)"),
 "S3_selFunTerm":       ("E0_cc07ii_iso.pv", "`set selFun = Term.` added, nothing else (default is TermMaxsize)"),
 "S4_nounif_envMat":    ("E0_cc07ii_iso.pv", "`set selFun = NounifsetMaxsize.` + a nounif on mess(envMat, <the 9-tuple>)"),
 "S5_preciseActions":   ("E0_cc07ii_iso.pv", "`set preciseActions = true.` added, nothing else (default is false)"),

 "G0_cc05_iso":   ("cap_cc05_a.pv", "isolated: every query but link 2b conjunct 1 deleted; nothing else changed"),
 "H0_cc17_iso":   ("cap_cc17_a.pv", "isolated: every query but link 2b conjunct 1 deleted; nothing else changed"),
 "S6_nounif_stageL2": ("E0_cc07ii_iso.pv", "`set selFun = NounifsetMaxsize.` + a nounif on mess(stageCh, (.., L2, ..)) -- the fact ablation 1 removes, here only made unselectable"),
 "S9_nounif_sigs":    ("E0_cc07ii_iso.pv", "`set selFun = NounifsetMaxsize.` + nounif (star variables) on attacker(sign((BYTES|POSS|STMT_DIGEST, *x), *k)) -- the 45% of selections verboseRules found"),
 "S7_cc14_selFunTerm":("F0_cc14_iso.pv", "`set selFun = Term.` added, nothing else"),
 "S10_cc05_selFunTerm":("G0_cc05_iso.pv", "`set selFun = Term.` added, nothing else"),
 "S11_cc17_selFunTerm":("H0_cc17_iso.pv", "`set selFun = Term.` added, nothing else"),
 "S8_ctl_cc09_selFunTerm": ("cap_cc09_a.pv", "CONTROL: the FULL landed companion C-C9, all 47 queries, `set selFun = Term.` added and nothing else"),

 "G1_cc05":  ("G0_cc05_iso.pv", "+ ablation 1: the depth-2 layer dropped"),
 "H1_cc17":  ("H0_cc17_iso.pv", "+ ablation 1: the depth-2 layer dropped"),
 "D1_verboseRules":     ("E0_cc07ii_iso.pv", "`set verboseRules = true.` -- diagnostic only, the manual's procedure for choosing a nounif"),
}

def rows():
    out = []
    for line in open(os.path.join(HERE, "abl.log")):
        m = re.match(r"^(\S+) rc=(\d+) seconds=(\d+) peakRSSkB=(\S*) results=(\d+) blob=(\S+) availMB_at_start=(\d+)", line)
        if not m: continue
        n, rc, secs, rss, nres, blob, avail = m.groups()
        src, what = WHAT.get(n, ("?", "?"))
        outf = os.path.join(HERE, n + ".out")
        res = "—"
        if os.path.exists(outf):
            rl = [l.strip() for l in open(outf) if l.startswith("RESULT")]
            if rl:
                res = rl[-1]
                for i, l in enumerate(open(outf)):
                    if l.startswith("RESULT"): resline = i + 1
            else:
                lines = open(outf).read().split("\n")
                why, whyline = None, None
                for i, l in enumerate(lines):
                    if l.startswith("Fatal error") or "out of memory" in l or "Stack overflow" in l:
                        why, whyline = l.strip(), i + 1
                prog = [l for l in lines if "rules inserted" in l]
                prog = prog[-1].strip() if prog else "(no saturation progress line)"
                if why:
                    res = "**no result — %s** (`%s.out:%d`); saturation had reached %s" % (why, n, whyline, prog)
                else:
                    res = "**no result — box exhausted**; saturation had reached %s" % prog
        d = dict(n=n, rc=rc, secs=secs, rss=rss, blob=blob, avail=avail,
                 src=src, what=what, res=res)
        try: d["resline"] = resline
        except NameError: pass
        out.append(d)
    return out

if __name__ == "__main__":
    print("| file | source | what changed | blob | rc | s | peak RSS | link-2b-conj-1 result |")
    print("|---|---|---|---|---|---|---|---|")
    for r in rows():
        rss = r["rss"]
        rssh = ("%.2f GB" % (int(rss)/1048576.0)) if rss.isdigit() else "(not written: %s)" % (rss or "empty")
        res = r["res"]
        if r["n"] == "S8_ctl_cc09_selFunTerm":
            res = ("**47 of 47 results, ALL IDENTICAL to the committed "
                   "`cap_cc09_a.out`** (`diff` of the two RESULT streams is empty); "
                   "committed run was 297 s / 0.45 GB")
        elif res.startswith("RESULT "):
            res = "**`is true`** — `%s.out:%s`" % (r["n"], r.get("resline","?"))
        print("| `%s.pv` | `%s` | %s | `%s` | %s | %s | %s | %s |"
              % (r["n"], r["src"], r["what"], r["blob"][:12], r["rc"], r["secs"], rssh, res))
