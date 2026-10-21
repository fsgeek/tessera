"""TEST release authentication (profile 3.5 EA-01; A10.4.2). Lifted from prototype/differential/adapter.py T1/T2.

The release-signature format is OPEN (profile 14.2 item 2); `tessera-v1-test-release/1` is a TEST stand-in:
raw ECDSA P-256 r||s over SHA-256 of the JCS release body, signer named by SPKI hash.

A TEST release is accepted only when its signature verifies under the supplied TEST key. Production
authentication (production=True) accepts no TEST authority: not a TEST-format release, not a TEST key, and not
the TESSERA_V1_TEST_* provisioning override. No production release format exists yet, so production mode
accepts only a compile-time binding (build_release.py) and never a release file.
"""
import base64
import hashlib
import json
import os
import unicodedata
import sys
from pathlib import Path
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from codec import Fault, demand, jcs, shahex
import release_constants

TEST_FORMAT = 'tessera-v1-test-release/1'
ENV_RELEASE, ENV_KEY = 'TESSERA_V1_TEST_RELEASE', 'TESSERA_V1_TEST_RELEASE_KEY'
ENV_CATALOG = 'TESSERA_V1_TEST_CATALOG'
SPEC_ID = 'tessera-v1-strict/verification-spec/1'   # verify.py row 8.2 constant
FIELD_MAP = {'alg': 'alg', 'alg_prohibited': 'alg_prohibited', 'binding_forms': 'binding_forms',
             'D': 'issuer_domain', 'delta_s': 'delta_s', 'dependency_manifest_sha256': 'dependency_manifest_sha256',
             'dnssec_algorithms': 'dnssec_algorithms', 'ds_digest_types': 'ds_digest_types',
             'epsilon_s': 'epsilon_s', 'k': 'k', 'utc_delta_s': 'utc_delta_s', 'utc_m': 'utc_m', 'preamble_sha256': 'preamble_sha256',
             'spec_sha256': 'spec_sha256', 'vectors_sha256': 'vectors_sha256'}


def _leaves(o):
    if isinstance(o, dict):
        for v in o.values(): yield from _leaves(v)
    elif isinstance(o, list):
        for v in o: yield from _leaves(v)
    else:
        yield o


def jcs_ascii(obj):
    """JCS for the TEST release body: ASCII strings, lists and objects only (no numbers)."""
    out = json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
    demand(out.isascii() and not any(isinstance(v, (int, float)) for v in _leaves(obj)), 'RELEASE_BODY_UNSUPPORTED')
    return out.encode()


def test_override_present(env=None):
    env = os.environ if env is None else env
    return any(env.get(k) for k in (ENV_RELEASE, ENV_KEY, ENV_CATALOG))


def authenticate_test_release(release_path, key_path):
    """Return the release body iff its TEST signature verifies; otherwise raise Fault."""
    try:
        rel = json.loads(Path(release_path).read_text())
        key = json.loads(Path(key_path).read_text())
        spki = base64.b64decode(key['spki_b64'], validate=True)
        sig = rel['signature']; body = rel['release']
    except (OSError, ValueError, KeyError, TypeError):
        raise Fault('TRUST_CONFIG_UNAUTHENTICATED') from None
    demand(hashlib.sha256(spki).hexdigest() == key.get('spki_sha256'), 'TRUST_CONFIG_UNAUTHENTICATED')
    demand(isinstance(sig, dict) and sig.get('alg') == 'ECDSA-P256-SHA256'
           and sig.get('signer_spki_sha256') == key['spki_sha256'], 'TRUST_CONFIG_UNAUTHENTICATED')
    try:
        rs = bytes.fromhex(sig['r_s_hex'])
        demand(len(rs) == 64, 'TRUST_CONFIG_UNAUTHENTICATED')
        der = encode_dss_signature(int.from_bytes(rs[:32], 'big'), int.from_bytes(rs[32:], 'big'))
        pub = serialization.load_der_public_key(spki)
        demand(isinstance(pub, ec.EllipticCurvePublicKey), 'TRUST_CONFIG_UNAUTHENTICATED')
        pub.verify(der, jcs_ascii(body), ec.ECDSA(hashes.SHA256()))
    except (InvalidSignature, ValueError, KeyError, TypeError):
        raise Fault('TRUST_CONFIG_UNAUTHENTICATED') from None
    demand(body.get('format') == TEST_FORMAT, 'RELEASE_FORMAT_UNKNOWN')
    demand(hashlib.sha256(jcs_ascii(body['catalog'])).hexdigest() == body['catalog_sha256'], 'CATALOG_UNAUTHENTICATED')
    return body


def translate_catalog(cat):
    """Universe catalog object -> `tessera-v1-independent-catalog/1` bytes (A02)."""
    demand(not (set(cat) - set(FIELD_MAP) - {'spec_id', 'TEST'}) and not (set(FIELD_MAP) - set(cat)), 'CATALOG_UNAUTHENTICATED')
    demand(cat['spec_id'] == SPEC_ID, 'CATALOG_UNAUTHENTICATED')
    entry = {FIELD_MAP[k]: v for k, v in cat.items() if k in FIELD_MAP}
    for k in ('dnssec_algorithms', 'ds_digest_types'): entry[k] = sorted(entry[k], key=int)
    return jcs({'entries': [entry], 'format': 'tessera-v1-independent-catalog/1'})


def provision(body):
    """Set the release bindings in memory only (as build_release.py would write them)."""
    catalog = translate_catalog(body['catalog'])
    release_constants.TRUST_SHA256 = body['trust_config_sha256']
    release_constants.CATALOG_BYTES = catalog
    release_constants.CATALOG_SHA256 = shahex(catalog)
    release_constants.UNICODE_MODULE_SHA256 = shahex(Path(getattr(unicodedata, '__file__', sys.executable)).read_bytes())


def authenticate(release_path=None, key_path=None, production=False, env=None):
    """Startup authentication. Explicit paths win over the environment. Returns 'TEST', 'COMPILED' or raises Fault.
    production=True: any TEST override or TEST-format release is refused (TEST_AUTHORITY_REFUSED)."""
    env = os.environ if env is None else env
    release_path = release_path or env.get(ENV_RELEASE)
    key_path = key_path or env.get(ENV_KEY)
    if production:
        demand(not (release_path or key_path or test_override_present(env)), 'TEST_AUTHORITY_REFUSED')
        return 'COMPILED'
    if not (release_path or key_path): return 'COMPILED'
    demand(release_path and key_path, 'TRUST_CONFIG_UNAUTHENTICATED')
    provision(authenticate_test_release(release_path, key_path))
    return 'TEST'
