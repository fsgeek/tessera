"""Print the phase-1 outcome table (THROWAWAY). Usage: uv run python run_phase1.py"""
from tessera_proto import attacks
from tessera_proto.verifier import Mutations, Policy, verify_bundle
from tessera_proto.world import T0, make_world

w = make_world()
r = w.issuer.issue(b'{"claim": "the minutes of 2026-10-06", "pages": 3}', T0)
rows = []
rep = verify_bundle(r.shipped, w.trust())
rows.append(("honest issue -> verify (strict)", "-", [(L["verification"], L["protocol_standing"]["value"]) for L in rep["layers"]]))
rp = attacks.replay_cc02(w, r.shipped, T0 + 7200)
for name, m in (("correct", Mutations()), ("mutated: no =fp pin, no mh", Mutations(drop_frame_pin_and_mh=True))):
    rep = verify_bundle(rp.bundle, w.trust(), attacks.DEGRADED_SOLE_DNS, m)
    rows.append(("C-C2 reattribution (degraded, skS leaked)", name,
                 [(L["verification"], L["failed"]) for L in rep["layers"]] + [("ReattributedA", attacks.judge_reattributed(rep, rp))]))
rp5 = attacks.replay_cc05(w, r.shipped, T0 + 7200)
for name, m in (("correct", Mutations()), ("mutated: signature bytes unbound", Mutations(unbind_signature_bytes=True))):
    rep = verify_bundle(rp5.bundle, w.trust(), attacks.DEGRADED_SOLE_DNS, m, dsks=rp5.dsks)
    rows.append(("C-C5 inner-sig transplant (wrapped, dsks EMULATED)", name,
                 [(L["verification"], L["failed"]) for L in rep["layers"]] + [("InnerSigTransplanted", attacks.judge_inner_sig_transplanted(rep, rp5))]))
for a, b, c in rows:
    print(f"{a:52s} | {b:34s} | {c}")
