"""TEST release authentication (profile 3.5 EA-01; A10.4.2) and the production/TEST mode rule (profile 15.9 R4).

The release-signature format is OPEN (profile 14.2 item 2); `tessera-v1-test-release/1` is a TEST stand-in:
raw ECDSA P-256 r||s over SHA-256 of the JCS release body, signer named by SPKI hash.

Production is the default mode. It accepts only the compiled binding in release_constants (NAMESPACE =
"PRODUCTION") and refuses any TEST authority: a TEST-format release, a TEST key, or the TESSERA_V1_TEST_* variables
(TEST_AUTHORITY_REFUSED). TEST mode is entered only by the explicit --mode test, which provisions the bindings in
memory from an authentic TEST release; an installation compiled as PRODUCTION refuses it. No production release
signature exists yet (the production key and ceremony come after the freeze), so a source tree is unprovisioned.
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
from .codec import Fault, demand, jcs, shahex
from . import release_constants

TEST_FORMAT = 'tessera-v1-test-release/1'
ENV_RELEASE, ENV_KEY = 'TESSERA_V1_TEST_RELEASE', 'TESSERA_V1_TEST_RELEASE_KEY'
ENV_CATALOG = 'TESSERA_V1_TEST_CATALOG'

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


def catalog_bytes(cat):
    """TEST release catalog object -> the frozen-catalog bytes: the object without its TEST label, canonical JCS."""
    demand(isinstance(cat, dict), 'CATALOG_UNAUTHENTICATED')
    return jcs({k: v for k, v in cat.items() if k != 'TEST'})


def provision(body):
    """Set the TEST release bindings in memory only. Never writes release_constants.py."""
    catalog = catalog_bytes(body['catalog'])
    release_constants.NAMESPACE = 'TEST'
    release_constants.TRUST_SHA256 = body['trust_config_sha256']
    release_constants.CATALOG_BYTES = catalog
    release_constants.CATALOG_SHA256 = shahex(catalog)


def authenticate(mode='production', release_path=None, key_path=None, env=None):
    """Startup authentication. Returns 'PRODUCTION' or 'TEST', or raises Fault.
    production (the default): any TEST flag or TESSERA_V1_TEST_* variable is refused (TEST_AUTHORITY_REFUSED) and the
    compiled binding must be a PRODUCTION one. test: explicit; needs an authentic TEST release; refused if this
    installation is compiled as PRODUCTION. Paths come from the flags, else from the TESSERA_V1_TEST_* variables."""
    env = os.environ if env is None else env
    if mode == 'production':
        demand(not (release_path or key_path or test_override_present(env)), 'TEST_AUTHORITY_REFUSED')
        demand(release_constants.NAMESPACE == 'PRODUCTION' and release_constants.TRUST_SHA256 is not None
               and release_constants.CATALOG_BYTES is not None, 'TRUST_CONFIG_UNAUTHENTICATED')
        return 'PRODUCTION'
    demand(mode == 'test', 'MODE_UNKNOWN')
    demand(release_constants.NAMESPACE != 'PRODUCTION', 'TEST_AUTHORITY_REFUSED')
    release_path = release_path or env.get(ENV_RELEASE)
    key_path = key_path or env.get(ENV_KEY)
    demand(release_path and key_path, 'TRUST_CONFIG_UNAUTHENTICATED')
    provision(authenticate_test_release(release_path, key_path))
    return 'TEST'
