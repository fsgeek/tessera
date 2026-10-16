#!/usr/bin/env python3
"""Supplementary L-74 probes (not conformance cases; expectations are NOT asserted here).

Builds three bundles with the conformance TEST issuer, read-only use of prototype/conformance/, into OUT_DIR:
  PROBE-74v  honest TXT witness + uppercase-signer TXT RRSIG, same inception (issuer sort order)
  PROBE-74e  honest TXT witness + uppercase-signer TXT RRSIG with inception one day earlier (sorts first)
  PROBE-74l  honest TXT witness + uppercase-signer TXT RRSIG with inception one second later (sorts last)
The expected.json written is the conformance L-74 reading (INVALID / SNAPSHOT_FORMAT) carried over, for run.py
convenience only; it is not a derived expectation. See FINDINGS.md F-1.

  prototype/.venv/bin/python -I prototype/differential/probe_l74.py OUT_DIR
  prototype/.venv/bin/python prototype/conformance/run.py --cases OUT_DIR --verifier "<adapter cmd>"
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'conformance'))
import cases as C  # noqa: E402

C.OUT = Path(sys.argv[1])
U, I = C.U, C.I
DAY = 86400


def upper(shift):
    return lambda c: C.sig(c.zk["w_zsk"], c.inc + shift, c.exp, signer="wamason.com",
                           signer_wire=U.name_wire("Wamason.com"))


C.CASES.clear()
for cid, shift, title in [("PROBE-74v", 0, "same inception"), ("PROBE-74e", -DAY, "sorts first"),
                          ("PROBE-74l", 1, "sorts last")]:
    C.case(cid, "probe", f"valid TXT witness plus uppercase-signer TXT RRSIG ({title})", "INVALID",
           "SNAPSHOT_FORMAT", why="L-74 reading carried over; not derived")(
        (lambda s: lambda: I.issue(adversarial=True, hooks=C.hk(dns_plan=C._txt_sigs(C.TXT_OK, upper(s)))))(shift))
C.OUT.mkdir(parents=True, exist_ok=True)
for spec in C.CASES:
    C.write_case(spec)
    print(spec["id"])
