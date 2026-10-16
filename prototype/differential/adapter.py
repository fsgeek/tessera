#!/usr/bin/env python3.14
"""Differential adapter: conformance run.py interface -> independent verifier (prototype/indep-verifier).

Translates ONLY interface matters the V1 profile leaves unspecified (see ADAPTER.md):
  T1 release provisioning   conformance EA-01 (signed TEST release in env)  -> indep A01 (release_constants)
  T2 catalog transport      conformance universe catalog (EA-01)            -> indep A02 catalog bytes
  T3 request flag           conformance EA-02 `--request V`                 -> indep verify_bundle(request=V)
  T4 output / refusal       conformance EA-03                                -> indep CLI output, passed through
  T5 release checker        conformance EA-12 `--previous P --next N`        -> indep policy.check_extension (A01)
It never reads the bundle, never emits a verdict or refusal itself, and never touches indep verification logic.
Run with the indep venv:  prototype/indep-verifier/.venv/bin/python prototype/differential/adapter.py ...
"""
import argparse
import functools
import hashlib
import json
import os
import sys
import unicodedata
from pathlib import Path

INDEP = Path(__file__).resolve().parent.parent / 'indep-verifier'
sys.path.insert(0, str(INDEP))

from cryptography.exceptions import InvalidSignature  # noqa: E402
from cryptography.hazmat.primitives import hashes, serialization  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import ec  # noqa: E402
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature  # noqa: E402

import release_constants  # noqa: E402  (indep's release binding module; set in memory only, never written)
import verify  # noqa: E402


class AdapterError(Exception):
    """A translation the adapter cannot perform without possibly changing a verdict: stop, do not guess."""


def jcs_ascii(obj):
    # The TEST release body holds only ASCII strings, lists and objects; for that subset JCS is exactly this.
    out = json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
    if not out.isascii() or any(isinstance(v, (int, float)) for v in _leaves(obj)):
        raise AdapterError('release body outside the ASCII/no-number subset')
    return out.encode()


def _leaves(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from _leaves(v)
    elif isinstance(o, list):
        for v in o:
            yield from _leaves(v)
    else:
        yield o


def authentic_release():
    """T1: the conformance stand-in for an authenticated release (EA-01). Returns the release body, or None if the
    record is not signed by the TEST release key (then indep stays unprovisioned and refuses on its own)."""
    rel = json.loads(Path(os.environ['TESSERA_V1_TEST_RELEASE']).read_text())
    key = json.loads(Path(os.environ['TESSERA_V1_TEST_RELEASE_KEY']).read_text())
    import base64
    spki = base64.b64decode(key['spki_b64'], validate=True)
    if hashlib.sha256(spki).hexdigest() != key['spki_sha256']:
        raise AdapterError('release key file inconsistent')
    sig = rel['signature']
    if sig.get('alg') != 'ECDSA-P256-SHA256' or sig.get('signer_spki_sha256') != key['spki_sha256']:
        return None
    rs = bytes.fromhex(sig['r_s_hex'])
    if len(rs) != 64:
        return None
    der = encode_dss_signature(int.from_bytes(rs[:32], 'big'), int.from_bytes(rs[32:], 'big'))
    pub = serialization.load_der_public_key(spki)
    try:
        pub.verify(der, jcs_ascii(rel['release']), ec.ECDSA(hashes.SHA256()))
    except InvalidSignature:
        return None
    body = rel['release']
    if body.get('format') != 'tessera-v1-test-release/1':
        raise AdapterError('unknown TEST release format')
    if hashlib.sha256(jcs_ascii(body['catalog'])).hexdigest() != body['catalog_sha256']:
        raise AdapterError('signed release catalog hash inconsistent')
    return body


# Universe catalog field -> indep A02 field. Every A02 field must be filled; no value is invented.
FIELD_MAP = {'alg': 'alg', 'alg_prohibited': 'alg_prohibited', 'binding_forms': 'binding_forms',
             'D': 'issuer_domain', 'delta_s': 'delta_s', 'dependency_manifest_sha256': 'dependency_manifest_sha256',
             'dnssec_algorithms': 'dnssec_algorithms', 'ds_digest_types': 'ds_digest_types',
             'epsilon_s': 'epsilon_s', 'k': 'k', 'preamble_sha256': 'preamble_sha256',
             'spec_sha256': 'spec_sha256', 'vectors_sha256': 'vectors_sha256'}
# Universe fields with no A02 slot; each is checked to equal what indep already hard-codes, else stop.
INDEP_SPEC_ID = 'tessera-v1-strict/verification-spec/1'   # indep verify.py row 8.2 constant


def translate_catalog(cat):
    """T2: universe catalog object -> indep `tessera-v1-independent-catalog/1` bytes (A02)."""
    extra = set(cat) - set(FIELD_MAP) - {'spec_id', 'TEST'}
    if extra or set(FIELD_MAP) - set(cat):
        raise AdapterError(f'catalog fields not translatable: extra={sorted(extra)}')
    if cat['spec_id'] != INDEP_SPEC_ID:
        raise AdapterError('catalog spec_id differs from the constant indep checks at row 8.2')
    entry = {FIELD_MAP[k]: v for k, v in cat.items() if k in FIELD_MAP}
    for k in ('dnssec_algorithms', 'ds_digest_types'):
        # Set-valued lists; A02 fixes ascending numeric order. Same members, same verdicts.
        entry[k] = sorted(entry[k], key=int)
    obj = {'entries': [entry], 'format': 'tessera-v1-independent-catalog/1'}
    return verify.jcs(obj)


def provision(body):
    """Set indep's release bindings in memory exactly as build_release.py would write them."""
    catalog_bytes = translate_catalog(body['catalog'])
    release_constants.TRUST_SHA256 = body['trust_config_sha256']
    release_constants.CATALOG_BYTES = catalog_bytes
    release_constants.CATALOG_SHA256 = hashlib.sha256(catalog_bytes).hexdigest()
    release_constants.UNICODE_MODULE_SHA256 = hashlib.sha256(
        Path(getattr(unicodedata, '__file__', sys.executable)).read_bytes()).hexdigest()


def release_check(prev_path, next_path):
    """T5: EA-12 release-checker interface -> indep's build-time append-only check (build_release.py
    --previous-trust), which parses both configs and runs policy.check_extension. ACCEPT iff it raises nothing."""
    from codec import Fault
    from policy import check_extension, parse_trust
    prev_raw, next_raw = Path(prev_path).read_bytes(), Path(next_path).read_bytes()
    try:
        check_extension(parse_trust(prev_raw), parse_trust(next_raw), prev_raw)
    except Fault as e:
        print('REJECT ' + e.code)
        return 0
    print('ACCEPT')
    return 0


def main():
    if '--previous' in sys.argv:
        rp = argparse.ArgumentParser()
        rp.add_argument('--previous', required=True)
        rp.add_argument('--next', required=True)
        r = rp.parse_args()
        return release_check(r.previous, r.next)
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--trust', required=True)
    ap.add_argument('--bundle', required=True)
    ap.add_argument('--request')
    a = ap.parse_args()
    try:
        body = authentic_release()
    except AdapterError as e:
        print('ADAPTER_ERROR: ' + str(e), file=sys.stderr)
        return 3
    if body is not None:
        try:
            provision(body)
        except AdapterError as e:
            print('ADAPTER_ERROR: ' + str(e), file=sys.stderr)
            return 3
    if a.request is not None:   # T3
        verify.verify_bundle = functools.partial(verify.verify_bundle, request=a.request)
    sys.argv = [str(INDEP / 'verify.py'), '--trust', a.trust, '--bundle', a.bundle]   # T4: indep CLI, unchanged
    return verify.main()


if __name__ == '__main__':
    raise SystemExit(main())
