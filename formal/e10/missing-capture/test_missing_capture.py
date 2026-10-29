"""A9.4 missing-capture negative control (C7 evidence).  Run:
  service/verifier/.venv/bin/python -m pytest formal/e10/missing-capture
"""
import copy
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import companion as C  # noqa: E402
from tessera_verify.codec import jcs  # noqa: E402  (the real verifier's own canonicalizer)

FIX = Path(__file__).resolve().parents[1] / 'fixtures' / 'E10-POS-01'   # honest receipt as shipped, read in place
STABLE = ('verdict', 'reason', 'T', 'revocation', 'historical_security', 'standing')


def harness_goes_red(report):
    """The control's detector: the registered text says a companion returning INVALID or UNVERIFIABLE on an
    otherwise valid bundle with only the capture missing must go red.  True means 'red' (wrong verdict seen)."""
    return report['verdict'] in ('INVALID', 'UNVERIFIABLE')


def test_fixture_is_valid_and_has_no_status_capture():
    bundle = json.loads((FIX / 'bundle.json').read_bytes())
    assert set(bundle) == {'profile', 'layers'}
    assert not C.has_status_capture(bundle)
    exp = json.loads((FIX / 'expected.json').read_text())
    assert (exp['verdict'], exp['reason']) == ('VALID_STRICT', 'OK')


def test_real_verifier_valid_strict_without_capture():
    r = C.real_verifier(FIX, FIX / 'bundle.json')
    assert (r['verdict'], r['reason']) == ('VALID_STRICT', 'OK')
    assert r['revocation'] == 'NOT_EVALUATED' and r['historical_security'] == 'NOT_EVALUATED'
    assert not harness_goes_red(r)                      # the real verifier stays green
    exp = json.loads((FIX / 'expected.json').read_text())
    assert {k: r[k] for k in STABLE} == {k: exp[k] for k in STABLE}


def test_companion_invalid_goes_red():
    r = C.companion_invalid(FIX, FIX / 'bundle.json')
    assert (r['verdict'], r['reason']) == ('INVALID', 'STATUS_CAPTURE_MISSING')
    assert harness_goes_red(r)


def test_companion_unverifiable_goes_red():
    r = C.companion_unverifiable(FIX, FIX / 'bundle.json')
    assert (r['verdict'], r['reason']) == ('UNVERIFIABLE', 'STATUS_CAPTURE_MISSING')
    assert harness_goes_red(r)


def test_faithful_companion_stays_green():
    """Detector control: a companion that changes nothing is not flagged."""
    r = C.companion(FIX, FIX / 'bundle.json', 'VALID_STRICT', 'OK')
    assert not harness_goes_red(r) and r == C.real_verifier(FIX, FIX / 'bundle.json')


def test_companions_change_only_missing_capture_behaviour():
    """On a bundle that fails for another reason (git member removed), both companions equal the real verifier."""
    bundle = json.loads((FIX / 'bundle.json').read_bytes())
    broken = copy.deepcopy(bundle); del broken['layers'][0]['git']
    with tempfile.TemporaryDirectory(prefix='missing-capture-') as tmp:
        p = Path(tmp) / 'no-git.bundle.json'; p.write_bytes(jcs(broken))   # the verifier requires canonical (JCS) bytes
        real = C.real_verifier(FIX, p)
        assert (real['verdict'], real['reason']) == ('UNVERIFIABLE', 'MEMBER_MISSING:git')
        assert C.companion_invalid(FIX, p) == real
        assert C.companion_unverifiable(FIX, p) == real
