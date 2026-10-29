"""Broken companions for the A9.4 missing-capture negative control.

Each companion is the real service verifier (run as its own CLI, TEST mode) plus ONE change: when the bundle carries
no status capture and the real verdict is VALID_STRICT, it reports a failing verdict instead.  Every other case is
passed through byte-for-byte, so the companions differ from the verifier only in missing-capture behaviour.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
KEY = ROOT / 'prototype' / 'conformance' / 'universe-release-key.json'   # data only; nothing imported from prototype/
CAPTURE_MEMBERS = ('status_capture', 'revocation_status', 'status')      # names a status-capture member would plausibly take


def has_status_capture(bundle):
    """True if the bundle carries a status-capture member.  V1 defines none (P6 status capture is T4, A9 line 236),
    so for every V1 bundle this is False; the name list is the companion's own guess, not a V1 field."""
    layers = bundle.get('layers') or [{}]
    return any(k in (layers[0] if isinstance(layers[0], dict) else {}) for k in CAPTURE_MEMBERS) or \
           any(k in bundle for k in CAPTURE_MEMBERS)


def real_verifier(case_dir, bundle_path):
    """Run the real service verifier on a fixture directory's trust/release and the given bundle file; return the
    stable object (the six fields) parsed from stdout."""
    case_dir = Path(case_dir)
    p = subprocess.run([sys.executable, '-m', 'tessera_verify', '--mode', 'test',
                        '--test-release', str(case_dir / 'release.json'), '--test-release-key', str(KEY),
                        '--trust', str(case_dir / 'trust.json'), '--bundle', str(bundle_path)],
                       capture_output=True, timeout=300)
    out = json.loads(p.stdout.decode())
    return out.get('stable', out)


def companion(case_dir, bundle_path, failing_verdict, failing_reason):
    """The broken companion: identical to real_verifier except that a VALID_STRICT result on a bundle with no
    status capture is replaced by (failing_verdict, failing_reason)."""
    report = real_verifier(case_dir, bundle_path)
    bundle = json.loads(Path(bundle_path).read_bytes())
    if report['verdict'] == 'VALID_STRICT' and not has_status_capture(bundle):
        report = dict(report, verdict=failing_verdict, reason=failing_reason)
    return report


def companion_invalid(case_dir, bundle_path):
    return companion(case_dir, bundle_path, 'INVALID', 'STATUS_CAPTURE_MISSING')


def companion_unverifiable(case_dir, bundle_path):
    return companion(case_dir, bundle_path, 'UNVERIFIABLE', 'STATUS_CAPTURE_MISSING')
