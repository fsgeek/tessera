"""G-17 (+K-4): can a bundle choose its own required set and reach VALID_STRICT with fewer authority
channels than the verifier intends? (THROWAWAY; see G17-REPORT.md.)

Runs on BOTH worlds: "stub" (Ed25519 slots, stub chain) and "real" (KMS-OpenPGP / gpg slots,
OTS-on-regtest anchor; channels are still stub Ed25519 keys in both, real/world.py l.11).

Attacker (capstone case (b)): it holds the leaked repo channel key skR, runs its own issuer under
Tessera's issuer id with its OWN slot key (so every signature in the bundle, including the one over
the required set, is legitimately its own), anchors on the public chain, and has no dns evidence.

TrustConfig switches (verifier.py):
  binding_ids   "forms" (spec l.792: STMT_DIGEST/STMT_DIRECT)  | "channels" (the set names channels)
  required_from "bundle" (R-3.37/V21 literal)                   | "policy" (verifier fixes the set)
"""
import json

import pytest

from consumers import scenarios
from tessera_proto import jcs
from tessera_proto.crypto import KeyPair
from tessera_proto.issuer import Issuer
from tessera_proto.real import world as RW
from tessera_proto.verifier import Policy, verify_bundle
from tessera_proto.world import T0

HOUR = 3600
STATEMENT = json.dumps({"name": "acme-widget", "version": "1.4.2", "sha256": "ee" * 32}).encode()


@pytest.fixture(scope="module", params=["stub", "real"])
def world(request):
    old = jcs.NUMBER_RULE
    try:
        yield request.param, scenarios.build(request.param).world
    finally:
        RW.close()
        jcs.NUMBER_RULE = old


def attacker_key(mode):
    if mode == "real":
        from tessera_proto.real.gpg import KmsOpenPGPSlotKey
        return KmsOpenPGPSlotKey.generate("attacker-kms", created=T0 - 86400)
    return KeyPair.generate("attacker")


def honest(w, declared_set=None, forms=("STMT_DIGEST",)):
    iss = Issuer(w.issuer.issuer_id, w.issuer.slot_keys, [w.dns, w.repo], w.chain, w.params,
                 binding_forms=forms, declared_set=declared_set)
    return iss.issue(STATEMENT, T0 + 7 * HOUR).shipped


def downgrade(mode, w, declared_set=None, forms=("STMT_DIGEST",)):
    """Attacker's own issuer, own key, leaked repo channel only; signs its own required set."""
    iss = Issuer(w.issuer.issuer_id, [attacker_key(mode)], [w.repo], w.chain, w.params,
                 binding_forms=forms, declared_set=declared_set)
    r = iss.issue(STATEMENT, T0 + 8 * HOUR)
    assert r.disposition == "SHIPPED"
    return r.shipped


def v(bundle, w, **trust_kw):
    return verify_bundle(bundle, w.trust(**trust_kw), Policy())["layers"][0]


# ---------------------------------------------------------------- spec-literal: the set names FORMS

def test_forms_baseline_strict(world):
    mode, w = world
    r = v(honest(w), w)
    assert r["verification"] == "VALID_STRICT"
    assert [c for c in r["checks"] if c.startswith("V20")] == ["V20[dns:STMT_DIGEST]", "V20[repo:STMT_DIGEST]"]


def test_forms_downgrade_not_strict(world):
    """Spec-literal: the identifier vocabulary is statement forms (l.792), so the bundle cannot name
    channels at all; channels come from the trust configuration (R-5.8, V23 'both'). dns absent."""
    mode, w = world
    r = v(downgrade(mode, w), w)
    assert r["verification"] == "UNVERIFIABLE"
    assert r["unperformable"] == ["V20[dns:STMT_DIGEST]"]
    assert r["checks"]["V20[repo:STMT_DIGEST]"]["status"] == "pass"


def test_forms_downgrade_naming_a_channel_is_unknown_identifier(world):
    """The attacker writes {"repo"} into the forms vocabulary: R-2.37 unknown identifier."""
    mode, w = world
    r = v(downgrade(mode, w, declared_set=["repo"]), w)
    assert r["verification"] == "UNVERIFIABLE"
    assert r["checks"]["V21"]["reason"] == "BINDING_FORM_UNKNOWN"
    assert not [c for c in r["checks"] if c.startswith("V20")]   # zero channel checks performed


def test_forms_bundle_chooses_the_form(world):
    """The residual the spec-literal reading DOES leave: the verifier cannot require a form. A bundle
    whose signed set is {STMT_DIGEST} is strict even if the verifier wanted STMT_DIRECT."""
    mode, w = world
    b = honest(w)   # signs {STMT_DIGEST}
    assert v(b, w, policy_forms=frozenset({"STMT_DIRECT"}))["verification"] == "VALID_STRICT"  # bundle wins
    r = v(b, w, policy_forms=frozenset({"STMT_DIRECT"}), required_from="policy")
    assert r["verification"] == "UNVERIFIABLE"
    assert set(r["unperformable"]) == {"V20[dns:STMT_DIRECT]", "V20[repo:STMT_DIRECT]"}


# ------------------------------------------------- the feared reading: the set names CHANNELS

def test_channels_baseline_strict_both_readings(world):
    mode, w = world
    b = honest(w, declared_set=["dns", "repo"])
    for rf in ("bundle", "policy"):
        assert v(b, w, binding_ids="channels", required_from=rf)["verification"] == "VALID_STRICT"


def test_channels_from_bundle_downgrade_reaches_strict(world):
    """THE ATTACK. Set read from the bundle, signed by the attacker's own key: {repo}. One leaked
    channel, no dns evidence, attacker key, VALID_STRICT. The standing path (which fixes channels
    from the trust config, standing.py:26) refuses to evaluate: the two paths disagree."""
    mode, w = world
    r = v(downgrade(mode, w, declared_set=["repo"]), w, binding_ids="channels", required_from="bundle")
    assert r["verification"] == "VALID_STRICT"
    assert r["failed"] == [] and r["unperformable"] == []
    assert [c for c in r["checks"] if c.startswith("V20")] == ["V20[repo:STMT_DIGEST]"]
    assert r["protocol_standing"]["value"] is None


def test_channels_from_policy_downgrade_not_strict(world):
    """The fix: strict's channels come from verifier policy; V21 checks the bundle's set is
    well-formed only. Same bytes as the attack: dns evidence required and absent."""
    mode, w = world
    b = downgrade(mode, w, declared_set=["repo"])
    r = v(b, w, binding_ids="channels", required_from="policy")
    assert r["verification"] == "UNVERIFIABLE"
    assert r["checks"]["V21"]["status"] == "pass"
    assert r["unperformable"] == ["V20[dns:STMT_DIGEST]"]
    # Degraded under the fix is the registered cost (capstone case (d)), and it is labelled so.
    rd = verify_bundle(b, w.trust(binding_ids="channels", required_from="policy"),
                       Policy(name="degraded-waive-dns", waive_channels=frozenset({"dns"})))["layers"][0]
    assert rd["verification"] == "VALID_DEGRADED(policy=degraded-waive-dns)"
    assert rd["waivers"]["channel:dns"]["observation"] == "absent"
