# EXPLORATORY PROBE 2026-10-04 — non-discharging; not part of any registration
#
# Derives a PROCESS SLICE of a capstone .pv file by DELETING top-level parallel
# components of the main process (never editing a process body, a declaration, a
# destructor or a `set` line), and by keeping ONE query (deleting the other query
# declarations; queries do not change the model).
#
#   python3 slice.py SRC.pv SLICE QUERY OUT.pv
#     SLICE in: none | depth{0,1,2} | depth{0,1,2}.attOnly | depth{0,1,2}.cone
#     QUERY in: all | a key of QUERY_RE below
#   python3 slice.py --identity SRC.pv   (checks that `none`+`all` reproduces SRC byte-for-byte
#                                         after the one banner line)
#
# Deleting a replicated component only removes traces (see REPORT.md section 2), so a
# reconstructed attack ("is false" + "A trace has been found.") in a slice is an
# attack on SRC; a "true" in a slice says nothing about SRC.
import re, sys

BANNER = "(* EXPLORATORY PROBE 2026-10-04 — non-discharging; not part of any registration *)\n"

# Tamarin slice.py correspondence:
#   depth0   ~ Tamarin depth0  : no wrapped layer (both WrapStage, both SUnwrap)
#   attOnly  ~ Tamarin attOnly : the honest processes other than Attester deleted
#              (ShipIssuer, RefuseIssuer, ForeignIssuer, Wrapper).  Tamarin's attOnly ALSO
#              deletes the dsks reductions of the POSS checks; that is NOT a deletion of
#              behaviour in ProVerif (removing a destructor rewrite rule makes `else`
#              branches reachable), so it is not mirrored here.
#   cone     = attOnly + every process the query's event cannot depend on
WRAP = r'WrapStage|SUnwrap'
OTHERS = r'ShipIssuer|RefuseIssuer|ForeignIssuer|Wrapper'
# what a cone keeps (by component head name) for each query; everything else goes
CORE = {'Front', 'AttestStage', 'WrapStage', 'SUnwrap'}
CONE_KEEP = {
    # C-C2's set (1) and the A4.6 control
    'cq3a':  CORE | {'Attester', 'SP3Judge'},
    'cq3b':  CORE | {'Attester', 'SP3Judge'},
    'link5': CORE | {'Link5Judge'},
    'a46':   CORE,
    # EXTENSION (beyond the brief; section 4 of REPORT.md): one set-(1) member per other
    # degraded mechanism failure.  'out:CH' keeps the fixture's `!out(CH, ...)` components.
    'cq5':    CORE | {'Attester', 'MemberJudge', 'out:honestMemberCh'},
    'sf':     CORE | {'Attester', 'MemberJudge', 'out:honestMemberCh'},
    'cq9':    CORE | {'Attester', 'PossJudge'},
    'cq8':    CORE | {'Attester', 'BytesJudge'},
    'cq7':    CORE | {'Attester', 'GenericSigJudge'},
    'cq4r':   CORE | {'Attester', 'ScopeJudge'},
    'cq4s':   CORE | {'Attester', 'SigJudge'},
    'link6b': CORE | {'Attester', 'Link6bJudge'},
    'link2a': CORE | {'Link2aJudge'},
    'link3':  CORE | {'Attester', 'PossJudge'},
    'link4':  CORE | {'Attester', 'BytesJudge'},
    'auhk':   CORE | {'Attester', 'JudgeH', 'out:honestKeyCh'},
}
QUERY_RE = {
    'cq3a':  r'event\(ReattributedA\(',
    'cq3b':  r'event\(ReattributedB\(',
    'link5': r'event\(ChainBroken\(l, LINK_5\)\)',
    'a46':   r'event\(AcceptS\(ev, t, k, fb\)\) ==> event\(IssuerSigned\(k, fb\)\)',
    'cq5':    r'event\(SetAltered\(',
    'sf':     r'event\(SignerForged\(',
    'cq9':    r'event\(PossessionUnbound\(',
    'cq8':    r'event\(SigBytesUnbound\(',
    'cq7':    r'event\(SigTransplanted\(',
    'cq4r':   r'event\(Rescoped\(',
    'cq4s':   r'event\(InnerSigTransplanted\(',
    'link6b': r'event\(ChainBroken\(l, LINK_6B\)\)',
    'link2a': r'event\(ChainBroken\(l, LINK_2A\)\)',
    'link3':  r'event\(ChainBroken\(l, LINK_3\)\)',
    'link4':  r'event\(ChainBroken\(l, LINK_4\)\)',
    'auhk':   r'event\(AcceptedUnderHonestKey\(k, fb\)\) ==>',
}
# depth1 (extension): only the (L1 -> L2) wrapper layer and its standing-side unwrap go
DEPTH1 = r'!WrapStage\(pk\(skS\), L1, L2\)|!SUnwrap\(L1, L2\)'

def head(comp):
    m = re.match(r'!?\s*(\w+)\s*(?:\(\s*(\w*))?', comp)
    return (m.group(1), m.group(2)) if m else (comp, '')

def drop_pred(slice_, query):
    def pred(comp):
        name, arg0 = head(comp)
        if slice_ == 'none':
            return False
        depth, _, guide = slice_.partition('.')
        if depth == 'depth0' and re.fullmatch(WRAP, name):
            return True
        if depth == 'depth1' and re.fullmatch(DEPTH1, comp):
            return True
        if guide == 'attOnly' and re.fullmatch(OTHERS, name):
            return True
        if guide == 'cone':
            keep = CONE_KEEP[query]
            return name not in keep and (name + ':' + (arg0 or '')) not in keep
        return False
    return pred

def split_top(block):
    # block is "( c1 | c2 | ... )" ; split on '|' at depth 1, '||' excluded (none at top)
    assert block.startswith('(') and block.rstrip().endswith(')')
    inner = block[1:block.rstrip().rfind(')')]
    comps, depth, cur = [], 0, ''
    for ch in inner:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if ch == '|' and depth == 0:
            comps.append(cur); cur = ''
        else:
            cur += ch
    comps.append(cur)
    return [c.strip() for c in comps]

def make(src_text, slice_, query):
    txt = src_text
    dropped_q = 0
    if query != 'all':
        qre = re.compile(QUERY_RE[query])
        def qsub(m):
            nonlocal dropped_q
            if qre.search(m.group(0)):
                return m.group(0)
            dropped_q += 1
            return '(* query deleted by slice.py *)'
        txt = re.sub(r'(?ms)^query\b.*?\.[ \t]*$', qsub, txt)
        kept = len(re.findall(r'(?m)^query\b', txt))
        assert kept == 1, (query, kept)
    dropped = []
    if slice_ != 'none':
        # the main process's parallel block: from "\n  ( !out(honestKeyCh" to EOF
        i = txt.index('\n  ( !out(honestKeyCh')
        pre, block = txt[:i + 1], txt[i + 1:].strip()
        comps = split_top(block)
        pred = drop_pred(slice_, query)
        keep = [c for c in comps if not pred(c)]
        dropped = [c for c in comps if pred(c)]
        txt = pre + '  ( ' + '\n  | '.join(keep) + ' )\n'
    return txt, dropped, dropped_q

if __name__ == '__main__':
    if sys.argv[1] == '--identity':
        src = open(sys.argv[2]).read()
        out, d, dq = make(src, 'none', 'all')
        ok = (out == src and not d and dq == 0)
        print('identity', sys.argv[2], 'OK' if ok else 'MISMATCH')
        sys.exit(0 if ok else 1)
    srcp, slice_, query, outp = sys.argv[1:5]
    src = open(srcp).read()
    out, dropped, dq = make(src, slice_, query)
    note = (f"(* GENERATED by slice.py from {srcp.split('/')[-1]}: slice={slice_} query={query}; "
            f"{dq} query declarations deleted; {len(dropped)} process components deleted: "
            f"{' ; '.join(dropped) if dropped else '(none)'} *)\n")
    open(outp, 'w').write(BANNER + note + out)
    print(outp, 'queries-deleted', dq, 'components-deleted', len(dropped))
