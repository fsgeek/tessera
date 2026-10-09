#!/usr/bin/env python3
# DIAGNOSTIC ONLY (divergence diagnosis, 2026-10-01). Not a ladder file, not a
# registration, discharges nothing.  Builds cap_cc15i_{a,b,d} exactly as derive.py
# does, then -- inside AttestStageW ONLY -- replaces the presented inner keys kA/kB
# by the enclosing wrapper key kEncW in every event and report (never in a check),
# which is the report contract the registration states for C-C15(i):
# "the inner acceptance ... reports the presented inner (kW, tI, ppfI)"
# (PREDICTIONS.md:2503).  Everything else is byte-identical to the ladder file.
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, PV)
os.chdir(PV)
import derive

def kw(t):
    i = t.index("let AttestStageW(")
    j = t.index(derive.ATT_END, i)
    body = t[i:j]
    out = []
    for ln in body.split("\n"):
        s = ln.strip()
        if s.startswith("event ") or "out(" in s:
            ln = re.sub(r"\bkA\b", "kEncW", ln)
            ln = re.sub(r"\bkB\b", "kEncW", ln)
        out.append(ln)
    return t[:i] + "\n".join(out) + t[j:]

bases = {"a": derive.case(derive.BASE, "a"), "b": derive.case(derive.BASE, "b"),
         "d": derive.degraded(derive.BASE)}
for cs in "abd":
    orig = derive.cc15i(bases[cs])
    ladder = open(os.path.join(PV, "cap_cc15i_%s.pv" % cs)).read()
    assert ladder.endswith(orig), "derive.py no longer reproduces cap_cc15i_%s.pv" % cs
    open(os.path.join(HERE, "dv_cc15i_kw_%s.pv" % cs), "w").write(
        "(* DIAGNOSTIC COPY dv_cc15i_kw_%s.pv: cap_cc15i_%s.pv with AttestStageW reporting kEncW\n"
        "   in place of the presented kA/kB in every event/report.  Not a ladder file. *)\n" % (cs, cs)
        + kw(orig))
    print("wrote dv_cc15i_kw_%s.pv" % cs)
