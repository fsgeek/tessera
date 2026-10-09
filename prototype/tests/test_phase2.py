"""Phase 2 scenario tests: the three consumers (THROWAWAY). Each test pins an observation the
PHASE2-REPORT relies on, so a change to the prototype that moves a finding turns a test red."""
import json

import pytest

from consumers import examiner as E
from consumers import relying_party as R
from consumers import scenarios
from consumers.log import BLOCKED, CONFUSED
from consumers.submitter import Submitter, acme_release
from tessera_proto.issuer import ChainSchedule
from tessera_proto.world import T0, make_world

HOUR = 3600


@pytest.fixture(scope="module")
def sc():
    return scenarios.build("stub")


@pytest.fixture(scope="module")
def rp_run(sc):
    rp, results, rev = R.run_all(sc)
    return rp, {(r.case, r.policy): r for r in results}, rev


# ------------------------------------------------------------------ submitter

def test_submitter_inline_sbom_refused_digest_statement_accepted():
    w = make_world()
    s = Submitter("Acme Corp", w.issuer, w.trust())
    out = s.submit(acme_release(), T0)
    assert out.rejection == "P8_NUMBER_NOT_DOUBLE"            # CVSS 9.8 (GUESS G-03 literal reading)
    assert out.result.disposition == "SHIPPED"
    assert [d.kind for d in out.deliveries] == ["SHIPPED_BUNDLE", "STANDING_EVIDENCE"]
    assert out.deliveries[1].at > out.deliveries[0].at        # standing evidence is late by construction


def test_submitter_receipt_self_check_and_completion(sc):
    s = sc.submitter
    at_ship = sc.cases["g"].bundle
    stale = s.self_check(at_ship, "at-ship")                   # verifier release fetched before submitting
    assert stale["layers"][0]["verification"] == "UNVERIFIABLE"
    assert "V38" in stale["layers"][0]["unperformable"]
    fresh = s.self_check(at_ship, "at-ship", trust=sc.trust())
    assert fresh["layers"][0]["verification"] == "VALID_STRICT"
    assert fresh["layers"][0]["protocol_standing"]["reason"] == "NO_TERMINAL_DISPOSITION_EVIDENCE"
    full = s.self_check(sc.cases["a"].bundle, "completed", trust=sc.trust())
    assert full["layers"][0]["protocol_standing"]["value"] == "ESTABLISHED"


def test_submitter_cannot_read_back_its_statement_without_internals(sc):
    b = sc.cases["a"].bundle
    tar_sha = json.loads(sc.honest_payload)["artifacts"][0]["sha256"]
    assert tar_sha not in json.dumps(b)                         # only inside base64 frames
    content = sc.submitter.find_my_statement(b, sc.honest_payload)
    assert content is not None
    # the attested bytes are the canonical form, not the submitted bytes
    from tessera_proto import jcs
    assert jcs.canonicalize(content) != sc.honest_payload
    kit = sc.submitter.portable_kit(b, sc.honest_release)
    assert json.loads(json.dumps(kit))["receipt"] == b          # storable and hand-on-able as one JSON file


def test_submitter_refusal_gets_only_a_stub():
    w = make_world()
    s = Submitter("Acme Corp", w.issuer, w.trust())
    late = ChainSchedule(inclusion_delay=70 * HOUR, block_interval=HOUR)
    out = s.submit(acme_release(), T0, [late])
    assert out.result.disposition == "REFUSED"
    assert out.deliveries[0].kind == "REFUSAL" and "NOT BUILT" in out.deliveries[0].body["status"]
    assert any("portable refusal record" in f.what for f in s.log.of(BLOCKED))


# ------------------------------------------------------------------ relying party

@pytest.mark.parametrize("case,policy,headline,naive,careful", [
    ("a", "strict", "VALID_STRICT", "correct", "correct"),
    ("g", "strict", "VALID_STRICT", "correct", "false reject (safe, costly)"),
    ("b", "strict", "INVALID", "correct", "correct"),
    ("b", "degraded", "INVALID", "correct", "correct"),
    ("c", "strict", "UNVERIFIABLE", "correct", "correct"),
    ("c", "degraded", "VALID_DEGRADED(policy=degraded-waive-repo)", "UNSAFE ACCEPT", "correct"),
    ("d1", "degraded", "VALID_DEGRADED(policy=degraded-waive-repo)", "correct", "correct"),
    ("d2", "strict", "UNVERIFIABLE", "false reject (safe, costly)", "false reject (safe, costly)"),
    ("d2", "degraded", "VALID_DEGRADED(policy=degraded-waive-repo)", "correct", "correct"),
    ("d3", "strict", "UNVERIFIABLE", "correct", "correct"),
    ("d3", "degraded", "VALID_DEGRADED(policy=degraded-waive-repo)", "UNSAFE ACCEPT", "UNSAFE ACCEPT"),
    ("e", "strict", "VALID_STRICT", "UNSAFE ACCEPT", "UNSAFE ACCEPT"),
    ("f", "strict", "VALID_STRICT", "UNSAFE ACCEPT", "UNSAFE ACCEPT"),
    ("h", "strict", "VALID_STRICT", "correct", "false reject (safe, costly)"),
])
def test_relying_party_matrix(rp_run, case, policy, headline, naive, careful):
    _, by, _ = rp_run
    r = by[(case, policy)]
    assert r.layers[0][0] == headline
    assert r.outcome(r.naive) == naive
    assert r.outcome(r.careful) == careful


def test_cc05_layers_disagree(rp_run):
    _, by, _ = rp_run
    r = by[("c", "degraded")]
    assert [x[0].split("(")[0] for x in r.layers] == ["VALID_DEGRADED", "INVALID"]
    assert r.failed == ["V19[A]"]


def test_lost_evidence_and_leaked_key_clone_are_indistinguishable(rp_run):
    _, by, _ = rp_run
    assert R.shape(by[("d2", "degraded")]) == R.shape(by[("d3", "degraded")])


def test_revocation_cannot_be_learned(sc, rp_run):
    _, by, rev = rp_run
    assert sc.cases["e"].bundle is sc.cases["a"].bundle         # the world fact changes no input byte
    assert R.shape(by[("e", "strict")]) == R.shape(by[("a", "strict")])
    assert rev["bundle_members_carrying_revocation"] == []
    assert set(rev["reported_REV_checks"].values()) == {"pass"}  # reported as passed, never performed
    assert rev["verdict_as_reported"] == "VALID_STRICT"
    assert rev["verdict_if_REV_unperformable"] == "UNVERIFIABLE"
    assert rev["verdict_with_G27_extension"] == "INVALID" and rev["failed_with_G27_extension"] == ["REV[B]"]


def test_relying_party_logged_confusions(rp_run):
    rp, _, _ = rp_run
    text = " ".join(f.what for f in rp.log.of(CONFUSED))
    for needle in ("C-C5", "same report", "Impostor", "Fresh receipt", "renewal wrapper"):
        assert needle in text


# ------------------------------------------------------------------ 2106 examiner

def test_examiner_is_independent_of_the_prototype_verifier():
    import ast
    import pathlib
    src = pathlib.Path(E.__file__).read_text()
    top = [n for n in ast.parse(src).body if isinstance(n, (ast.Import, ast.ImportFrom))]
    assert not [n for n in top if isinstance(n, ast.ImportFrom) and (n.module or "").startswith("tessera_proto")]


def test_examiner_as_is_cannot_reach_a_verdict(sc):
    ex = E.examine(sc.cases["a"].bundle, E.archived_store(sc.world))
    names = {s.name for s in ex.blocked()}
    assert ex.verdict == "UNVERIFIABLE"
    assert {"verification procedure from the embedded spec", "receipt-to-anchor binding (what digest was anchored)",
            "temporal predicate (needs k, delta, epsilon)", "revocation time-relativity (R-5.21)"} <= names
    recon = {s.name for s in ex.steps if s.status == "reconstructed"}
    assert "key fingerprint function (pubkey -> tuple key_fp / sset)" in recon
    assert "OpenTimestamps proof format [hidden by stub]" in ex.unlisted


def test_examiner_with_complete_spec_still_lacks_revocation(sc):
    store = E.archived_store(sc.world)
    sup = E.complete_spec_supplement(sc.world)
    ex = E.examine(sc.cases["a"].bundle, store, sup)
    assert [s.name for s in ex.blocked()] == ["revocation time-relativity (R-5.21)"]
    assert ex.verdict == "UNVERIFIABLE"
    assert ex.verdict_if_trusting_reconstructions.startswith("VALID_STRICT")
    # the revoked-in-window world gives the examiner exactly the same ledger
    ex_e = E.examine(sc.cases["e"].bundle, store, sup)
    assert ex_e.table() == ex.table()
    # equivocation stays undecidable without a log
    assert any(s.name == "no contradictory TLR exists" and s.status == "blocked" for s in ex.steps)
