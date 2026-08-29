"""
PROBE — NON-DISCHARGING. Runs Q1–Q7 of ../PROBE.md and prints observations.
Run: .venv/bin/python formal/spike/standing-probe/probe/run_probe.py
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from probe import (ChainStub, ChannelStub, Issuer, Key, TrustConfig, Verifier, bundle,  # noqa: E402
                   issue_with_reissue, lineage_of, refuse_all)

K, DELTA, ISSUER_TIMEOUT = 3, 60, 40


def section(t: str) -> None:
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


def show(label: str, r: dict) -> None:
    print(f"{label:<44} verification={r['verification']:<15} standing={r['protocol_standing']:<12} reason={r['standing_reason']}"
          + (f"  env-reasons={r['reasons']}" if r["reasons"] else ""))


def fixture():
    issuer, dns, repo, chain = Issuer(), ChannelStub("dns"), ChannelStub("repo"), ChainStub()
    ev = [dns.publish(issuer.tuple()), repo.publish(issuer.tuple())]
    trust = TrustConfig(channel_pubs={"dns": dns.key.pub, "repo": repo.key.pub}, k=K, delta=DELTA)
    return issuer, ev, chain, trust


def main() -> None:
    content = b"the attested content"

    # ---------------------------------------------------------------- Q1
    section("Q1 — baseline: two valid artifacts, no standing mechanism")
    issuer, ev, chain, trust = fixture()
    attempts, shipped = issue_with_reissue(issuer, chain, content, K, DELTA, ISSUER_TIMEOUT)
    assert len(attempts) == 2 and shipped is attempts[1], "fixture did not produce the reissue"
    a1, a2 = attempts
    V = Verifier(trust)
    r1 = V.assess(bundle(a1, ev, chain)); show("attempt 1 (abandoned by issuer) alone", r1)
    fields1 = r1["fields_read"]
    r2 = V.assess(bundle(a2, ev, chain)); show("attempt 2 (shipped) alone", r2)
    print("fields the verifier read:", fields1)
    diff = {k: (a1["core"][k], a2["core"][k]) for k in a1["core"] if a1["core"][k] != a2["core"][k]}
    print("core fields that differ between the two artifacts:", sorted(diff))
    print("  declared:", diff.get("declared"), " anchor heights:", a1["anchor_ref"], a2["anchor_ref"])
    print("does any field say 'shipped'?", any("SHIP" in json.dumps(x).upper() for x in (a1["core"], a2["core"])))
    print("chain-time check: attempt 1 confirmed_at", ChainStub.confirmed_at(chain.view(), a1["anchor_ref"], K),
          "declared", a1["core"]["declared"], "delta", DELTA, "-> within window:",
          ChainStub.confirmed_at(chain.view(), a1["anchor_ref"], K) <= a1["core"]["declared"] + DELTA)
    # the reorg case, for contrast: not the residue
    chain_reorg = copy.deepcopy(chain)
    for b in chain_reorg.blocks:
        if b["height"] == a1["anchor_ref"]["height"]:
            b["anchors"] = []
    show("contrast: attempt 1 with anchor orphaned", V.assess(bundle(a1, ev, chain_reorg)))

    # ---------------------------------------------------------------- Q2
    section("Q2 — terminal lineage record: S1 / S2 / S3")
    tlr = issuer.tlr(lineage_of(attempts), {"disposition": "SHIPPED", "handle": a2["handle"], "ordinal": 2})
    print("TLR body:", json.dumps(tlr["body"], indent=1)[:600], "...")
    rS1 = V.assess(bundle(a2, ev, chain, tlr)); show("S1: attempt 2 + TLR", rS1)
    rS2 = V.assess(bundle(a1, ev, chain, tlr)); show("S2: attempt 1 + TLR", rS2)
    rS3 = V.assess(bundle(a1, ev, chain, None)); show("S3: attempt 1 alone", rS3)
    outs = {(r["protocol_standing"], r["standing_reason"]) for r in (rS1, rS2, rS3)}
    print("three distinct (standing, reason) outputs:", len(outs) == 3, sorted(outs))
    print("S1/S2/S3 verification verdicts unchanged by standing:", {r["verification"] for r in (rS1, rS2, rS3)})

    # ---------------------------------------------------------------- Q3
    section("Q3 — transplant, with and without artifact binding")
    other = issuer.attempt(b"different content", declared=chain.tip["ts"])
    other["anchor_ref"] = chain.anchor(other["handle"]); [chain.mine(5) for _ in range(K)]
    show("(a) other content + attempt 2's TLR [handle]", V.assess(bundle(other, ev, chain, tlr)))
    wrapped = copy.deepcopy(a1); wrapped["claimed_ordinal"] = 2   # a wrapper re-labelling attempt 1 as "the shipped one"
    show("(b) wrapper(attempt 1 as #2) + TLR [handle]", V.assess(bundle(wrapped, ev, chain, tlr)))
    tlr_ord = issuer.tlr(lineage_of(attempts), {"disposition": "SHIPPED", "handle": a2["handle"], "ordinal": 2}, binding="ordinal")
    other["claimed_ordinal"] = 2
    show("(a) other content + TLR [ordinal, BROKEN]", V.assess(bundle(other, ev, chain, tlr_ord)))
    show("(b) wrapper(attempt 1 as #2) + TLR [ordinal, BROKEN]", V.assess(bundle(wrapped, ev, chain, tlr_ord)))
    print("what 'handle' binds to:", "sha256 of the signed core (tuple, manifest sig, content hash, bytes sig, declared, pub)")

    # ---------------------------------------------------------------- Q4
    section("Q4 — collapsing negative control (one reason code for S2 and S3)")
    Vc = Verifier(trust, collapse_reasons=True)
    c2 = Vc.assess(bundle(a1, ev, chain, tlr)); c3 = Vc.assess(bundle(a1, ev, chain, None))
    show("collapsed verifier, S2", c2); show("collapsed verifier, S3", c3)
    disc_ok = c2["standing_reason"] != c3["standing_reason"]
    print("discrimination check on the collapsed verifier:", "PASS (bad — control did not fire)" if disc_ok else "FAIL (good — control fired)")
    print("discrimination check on the correct verifier:", "PASS" if rS2["standing_reason"] != rS3["standing_reason"] else "FAIL")

    # ---------------------------------------------------------------- Q5
    section("Q5 — equivocation: two TLRs from the same key")
    tlr_alt = issuer.tlr(lineage_of(attempts), {"disposition": "SHIPPED", "handle": a1["handle"], "ordinal": 1})
    show("attempt 1 + TLR-B (names attempt 1 shipped)", V.assess(bundle(a1, ev, chain, tlr_alt)))
    show("attempt 2 + TLR-A (names attempt 2 shipped)", V.assess(bundle(a2, ev, chain, tlr)))
    print("a verifier holding either bundle alone detects the conflict:", False, "(it has no way to see the other TLR)")

    # ---------------------------------------------------------------- Q6
    section("Q6 — what the verifier obtained from outside the bundle")
    print("external fetches across Q1–Q3:", V.external_fetches)
    print("inputs the verifier held BEFORE the bundle (trust configuration):", sorted(trust.channel_pubs), "k, delta")
    print("inputs from the bundle only:", sorted(set(V.fields_read)))

    # ---------------------------------------------------------------- Q7
    section("Q7 — refusal join: TLR with terminal REFUSED vs A3.7.2's portable refusal record")
    issuer2, ev2, chain2, trust2 = fixture()
    ra = refuse_all(issuer2, chain2, content, K, n_attempts=3, issuer_timeout=ISSUER_TIMEOUT)
    for _ in range(K): chain2.mine(5)          # blocks keep coming; the abandoned anchors bury late
    tlr_ref = issuer2.tlr(lineage_of(ra), {"disposition": "REFUSED", "handle": None, "ordinal": None})
    V2 = Verifier(trust2)
    for i, a in enumerate(ra, 1):
        show(f"refused lifecycle: attempt {i} + REFUSED TLR", V2.assess(bundle(a, ev2, chain2, tlr_ref)))
    show("refused lifecycle: attempt 1 alone", V2.assess(bundle(ra[0], ev2, chain2, None)))
    print("TLR(REFUSED) fields:", sorted(tlr_ref["body"].keys()), "| lineage entry fields:", sorted(tlr_ref["body"]["lineage"][0].keys()))
    print("A3.7.2 portable refusal record fields (from the amendment text): attempt identity, disposition, "
          "disclosable reasons, evidence needed to verify it; plus a non-identifying public commitment value.")
    print("overlap: attempt identity (handle), disposition. TLR lacks: reasons, commitment value. "
          "Refusal record lacks: the full attempt lineage with anchor refs.")


if __name__ == "__main__":
    main()
