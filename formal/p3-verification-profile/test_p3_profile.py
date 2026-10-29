"""P3 [assumption] half: the V1 verification profile as executable evidence (H1a).

Run from service/verifier:
    .venv/bin/python -m pytest -q ../../formal/p3-verification-profile/test_p3_profile.py

Vector tests call the service verifier's own functions (tessera_verify.codec: parse_signature, sig_policy,
public_key, signature_verifies; tessera_verify.verify.verify_bundle; tessera_verify.policy.parse_trust).
`cryptography` is called directly only (a) to construct inputs and (b) in TestLibraryBehaviour, whose tests
characterize the library itself and back PROFILE.md's library claims; those are labelled as such.
"""
import base64
import copy
import hashlib
import json
import os
import posixpath
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

HERE = Path(__file__).resolve().parent
VERIFIER = HERE.parent.parent / 'service' / 'verifier'
ISSUER = HERE.parent.parent / 'service' / 'issuer'
sys.path[:0] = [str(VERIFIER), str(VERIFIER / 'tests'), str(HERE)]

from tessera_verify import install_record  # noqa: E402
install_record.load_and_apply()  # as tests/conftest.py does: the SHA-1DC hook is an installation fact

import cryptography  # noqa: E402
from cryptography.exceptions import InvalidSignature  # noqa: E402
from cryptography.hazmat.backends.openssl.backend import backend  # noqa: E402
from cryptography.hazmat.primitives import hashes, serialization  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import ec, mldsa, utils  # noqa: E402

from tessera_verify import codec, release_auth  # noqa: E402
from tessera_verify.codec import (ALG, HYBRID_ALG, Fault, b64, jcs, mldsa65_encoding_valid, parse_signature,  # noqa: E402
                                  public_key, read_anchor, registered_codecs, sha, sig_policy, signature_verifies)
from tessera_verify.policy import parse_catalog, parse_trust  # noqa: E402
from tessera_verify.verify import verify_bundle  # noqa: E402
from fixtures import enc, make_fixture, make_release, key_file  # noqa: E402
import p256  # noqa: E402

VEC = HERE / 'vectors'
F1 = json.loads((VEC / 'F1-library.json').read_text())
SIG_FILES = ['F2-signature-encodings.json', 'F5-equation-variant.json']
KEY_FILES = ['F3-public-key-validation.json', 'F4-low-order-points.json']


def load(name): return json.loads((VEC / name).read_text())


def wheel_tag(text):
    tags = [l.split(':', 1)[1].strip() for l in text.splitlines() if l.startswith('Tag:')]
    assert len(tags) == 1, tags
    return tags[0]


def tested_verifier_files():
    """The verifier code this floor exercised (service/verifier/tessera_verify), as {zip path: bytes}."""
    root = VERIFIER / 'tessera_verify'
    return {('tessera_verify/' + f.relative_to(root).as_posix()): f.read_bytes()
            for f in sorted(root.rglob('*')) if f.is_file() and '__pycache__' not in f.parts and f.suffix != '.pyc'}


def check_zip(path):
    """The zip carries the recorded cryptography build AND exactly the verifier code the floor tested
    (A11C-01: a matching wheel alone would let different verifier code pass)."""
    with zipfile.ZipFile(path) as z:
        binding = z.read(F1['wheel']['rust_binding'])
        tag = wheel_tag(z.read('cryptography-%s.dist-info/WHEEL' % F1['cryptography']).decode())
        names = z.namelist()
        # Codex confirmation 2: an alias ('./tessera_verify/codec.py') extracts over the checked file. Only canonical,
        # unique, relative POSIX paths are accepted. This is build-content evidence for zips our packager writes; it
        # does NOT show that every extractor reads a zip as Python's zipfile does (A11C3B: they can disagree).
        # Deployment identity comes from the exact-digest comparison in test_deployed_zip_identity.
        bad = [n for n in names if n != posixpath.normpath(n) + ('/' if n.endswith('/') else '') or n.startswith('/')
               or '\\' in n or n.split('/')[0] in ('', '.', '..')]
        assert bad == [] and len(names) == len(set(names)), (bad, len(names) - len(set(names)))
        links = [i.filename for i in z.infolist() if (i.external_attr >> 16) & 0o170000 == 0o120000]
        assert links == [], links                          # a symlink entry can redirect extraction
        shipped = {n: z.read(n) for n in names if n.startswith('tessera_verify/') and not n.endswith('/')}
    assert hashlib.sha256(binding).hexdigest() == F1['wheel']['rust_binding_sha256']
    assert tag == F1['wheel']['tag']
    tested = tested_verifier_files()
    assert sorted(shipped) == sorted(tested), sorted(set(shipped) ^ set(tested))
    assert [n for n in tested if shipped[n] != tested[n]] == []


def run_sig(v, keys, docs):
    """Function-level harness for one signature against one known-good key: signature codec (the function of rows
    3.1/9.3), policy (9.1/9.4), then verification (9.2/9.5). Returns 'ACCEPT', the Fault code, or 'SIG_INVALID'
    (POSSESSION_INVALID for a possession proof: same function, different row). It is NOT the bundle's order: a
    bundle evaluates keys (5.1) before signature policy (9.1) and reports by row precedence. Precedence claims come
    only from TestBundle."""
    alg, slot = v['alg'], v['slot']
    try:
        parsed = parse_signature(bytes.fromhex(v['sig_hex']), alg, slot, registered_codecs(alg))
        sig_policy(parsed)
    except Fault as e:
        return e.code
    k = keys[v['key']]
    key = public_key(bytes.fromhex(k['hex']), k['slot'], k['alg'])
    return 'ACCEPT' if signature_verifies(bytes.fromhex(docs[v['document']]), parsed, key) else 'SIG_INVALID'


def run_key(v):
    try:
        public_key(bytes.fromhex(v['key_hex']), v['slot'], v['alg'])
        return 'ACCEPT'
    except Fault as e:
        return e.code


def sig_cases():
    for name in SIG_FILES:
        f = load(name)
        for v in f['vectors']: yield pytest.param(v, f['keys'], f['documents'], id=v['id'])


def key_cases():
    for name in KEY_FILES:
        for v in load(name)['vectors']: yield pytest.param(v, id=v['id'])


def by_id(vid):
    for name in SIG_FILES + KEY_FILES:
        for v in load(name)['vectors']:
            if v['id'] == vid: return v
    raise KeyError(vid)


# --------------------------------------------------------------------------------------------- F1
class TestF1Library:
    def test_installed_library_is_the_recorded_one(self):
        assert cryptography.__version__ == F1['cryptography']
        assert backend.openssl_version_text() == F1['openssl']
        assert '%d.%d' % sys.version_info[:2] == F1['python']

    def test_requirements_pin(self):
        pins = [l.strip() for l in (VERIFIER / 'requirements.txt').read_text().splitlines() if l.strip()]
        assert F1['requirements_pin'] in pins
        assert 'cryptography==%s' % F1['cryptography'] == F1['requirements_pin']

    def test_codec_uses_this_library(self):
        assert codec.mldsa is mldsa and codec.ec is ec and codec.utils is utils

    def test_installed_wheel_identity(self):
        import cryptography as c
        root = Path(c.__file__).resolve().parent
        assert hashlib.sha256((root.parent / F1['wheel']['rust_binding']).read_bytes()).hexdigest() == F1['wheel']['rust_binding_sha256']
        assert wheel_tag((root.parent / ('cryptography-%s.dist-info' % F1['cryptography']) / 'WHEEL').read_text()) == F1['wheel']['tag']

    def test_lambda_package_wheel_identity(self, tmp_path):
        """Builds the issuer's bootstrap Lambda zip with service/issuer/package.py (its own wheel resolution) and
        checks the bundled cryptography binding against F1. Skips, with the reason, if uv or the network is absent."""
        sys.path.insert(0, str(ISSUER))
        try:
            import package
        finally:
            sys.path.remove(str(ISSUER))
        if shutil.which('uv') is None:
            pytest.skip('uv not on PATH: package.py cannot resolve the Lambda wheel here')
        out = tmp_path / 'lambda.zip'
        try:
            package.build(out)
        except (SystemExit, subprocess.CalledProcessError) as e:
            pytest.skip(f'package.py could not build (offline or missing prerequisite?): {e}')
        check_zip(out)

    def test_deployed_zip_identity(self):
        """A11.2 3(c). TESSERA_LAMBDA_ZIP: the exact zip package.py built and infra deployed. TESSERA_LAMBDA_CODESHA256:
        AWS's CodeSha256 for every function the discharge covers (comma-separated; `aws lambda get-function-configuration
        --query CodeSha256`). Its verifier content must match the tested tree, and its digest must be what AWS deployed."""
        path, reported = os.environ.get('TESSERA_LAMBDA_ZIP'), os.environ.get('TESSERA_LAMBDA_CODESHA256')
        if not path or not reported:
            pytest.skip('TESSERA_LAMBDA_ZIP and TESSERA_LAMBDA_CODESHA256 not both set: no deployed package to tie')
        check_zip(Path(path))
        data = Path(path).read_bytes()
        digests = [d.strip() for d in reported.split(',') if d.strip()]
        assert digests and all(code_sha256_matches(data, d) for d in digests), digests

    @pytest.mark.parametrize('name', sorted(F1['calls']))
    def test_recorded_call_is_the_verifiers_call(self, name):
        src = (VERIFIER / 'tessera_verify' / 'codec.py').read_text()
        assert src.count(F1['calls'][name]) == 1, name


# ------------------------------------------------------------------------------------ F2, F5 (sig)
@pytest.mark.parametrize('v,keys,docs', list(sig_cases()))
def test_signature_vector(v, keys, docs):
    assert run_sig(v, keys, docs) == v['expect'], v['case']


# ------------------------------------------------------------------------------------ F3, F4 (key)
@pytest.mark.parametrize('v', list(key_cases()))
def test_key_vector(v):
    assert run_key(v) == v['expect'], v['case']


class TestControls:
    """The vector suites cannot pass by rejecting (or accepting) everything."""
    def test_each_file_has_accept_and_reject(self):
        for name in SIG_FILES + KEY_FILES:
            outcomes = {v['expect'] for v in load(name)['vectors']}
            assert 'ACCEPT' in outcomes and len(outcomes) > 1, name

    def test_each_slot_rule_has_a_positive_control(self):
        seen = {(v['slot'], v['alg']) for n in SIG_FILES + KEY_FILES for v in load(n)['vectors'] if v['expect'] == 'ACCEPT'}
        assert {('gpg', HYBRID_ALG), ('kms', HYBRID_ALG), ('kms', ALG)} <= seen

    def test_vector_ids_unique(self):
        ids = [v['id'] for n in SIG_FILES + KEY_FILES for v in load(n)['vectors']]
        assert len(ids) == len(set(ids))


# ----------------------------------------------------------------- the verifier's own ML-DSA gate
class TestMLDSAGate:
    MALFORMED = ['R-08', 'R-09', 'R-10', 'R-11', 'R-12', 'R-13', 'R-14']

    @pytest.mark.parametrize('vid', MALFORMED)
    def test_gate_rejects_before_library(self, vid):
        assert mldsa65_encoding_valid(bytes.fromhex(by_id(vid)['sig_hex'])) is False

    @pytest.mark.parametrize('vid', ['R-01', 'R-02', 'R-15', 'R-16'])
    def test_gate_passes_well_encoded(self, vid):
        assert mldsa65_encoding_valid(bytes.fromhex(by_id(vid)['sig_hex'])) is True

    @pytest.mark.parametrize('vid', MALFORMED)
    def test_rejection_does_not_depend_on_library_strictness(self, vid):
        permissive = Mock(); permissive.verify.return_value = None
        assert signature_verifies(b'any', bytes.fromhex(by_id(vid)['sig_hex']), permissive) is False
        permissive.verify.assert_not_called()


# ------------------------------------------------------------------- rule-O policy (P3R-01)
def policy_vectors():
    f = load('F2-signature-encodings.json')
    return [pytest.param(v, f['keys'], f['documents'], id=v['id']) for v in f['vectors'] if v.get('verifies_without_policy')]


class TestRuleOPolicy:
    def test_policy_vectors_present(self):
        outcomes = [p.values[0]['expect'] for p in policy_vectors()]
        assert outcomes.count('SIG_POLICY') >= 15 and outcomes.count('ACCEPT') >= 5

    @pytest.mark.parametrize('v,keys,docs', policy_vectors())
    def test_policy_vector_is_correctly_signed(self, v, keys, docs):
        """Every policy vector verifies when sig_policy is skipped, so a SIG_POLICY outcome is the policy's doing."""
        parsed = parse_signature(bytes.fromhex(v['sig_hex']), v['alg'], v['slot'], registered_codecs(v['alg']))
        k = keys[v['key']]
        assert signature_verifies(bytes.fromhex(docs[v['document']]), parsed, public_key(bytes.fromhex(k['hex']), k['slot'], k['alg']))


# --------------------------------------------------------------- high-S / low-S labels (P3R-05)
def test_O01_is_low_s_and_O02_is_its_high_s_twin():
    a = parse_signature(bytes.fromhex(by_id('O-01')['sig_hex']))
    b = parse_signature(bytes.fromhex(by_id('O-02')['sig_hex']))
    assert a.r == b.r and a.s + b.s == p256.N
    assert a.s <= p256.N // 2 < b.s


# ------------------------------------------------ constructed verification-equation cases (P3R-03)
class TestEquationConstruction:
    def equation_point(self, vid):
        f = load('F5-equation-variant.json'); v = by_id(vid)
        sig = parse_signature(bytes.fromhex(v['sig_hex']))
        doc = bytes.fromhex(f['documents'][v['document']])
        q = bytes.fromhex(f['keys'][v['key']]['hex'])[-64:]
        Q = (int.from_bytes(q[:32], 'big'), int.from_bytes(q[32:], 'big'))
        e = int.from_bytes(sha(doc + sig.trailer), 'big'); w = pow(sig.s, -1, p256.N)
        return sig, p256.add(p256.mul(e * w % p256.N, p256.G), p256.mul(sig.r * w % p256.N, Q))

    def test_E10_x_of_R_is_at_least_n(self):
        sig, R = self.equation_point('E-10')
        assert R is not None and R[0] >= p256.N and R[0] == p256.N + sig.r and R[0] % p256.N == sig.r
        assert R[0] != sig.r  # an unreduced comparison x(R) == r would reject E-10, which the verifier accepts

    def test_E11_equation_result_is_infinity(self):
        _, R = self.equation_point('E-11')
        assert R is None


# --------------------------------------- P-256 checks happen before the EC constructor (P3R-02)
class TestPointBeforeConstructor:
    """codec.ec is replaced, for codec only, by a permissive stand-in whose constructor accepts anything. A
    rejection here is therefore the verifier's own check; a positive control shows the constructor is reached."""

    def run(self, raw, slot='gpg', alg=HYBRID_ALG):
        ctor = Mock(return_value=Mock(public_key=Mock(return_value='KEY')))
        fake = SimpleNamespace(EllipticCurvePublicNumbers=ctor, SECP256R1=Mock(return_value='P256'))
        with patch.object(codec, 'ec', fake):
            try:
                return public_key(raw, slot, alg), ctor
            except Fault as e:
                return e.code, ctor

    def key(self, vid): return bytes.fromhex(by_id(vid)['key_hex'])

    @pytest.mark.parametrize('vid', ['K-01', 'K-02', 'K-35', 'K-14'])
    def test_valid_point_reaches_constructor(self, vid):
        v = by_id(vid); raw = self.key(vid)
        out, ctor = self.run(raw, v['slot'], v['alg'])
        assert out == 'KEY'
        ctor.assert_called_once_with(int.from_bytes(raw[-64:-32], 'big'), int.from_bytes(raw[-32:], 'big'), 'P256')

    @pytest.mark.parametrize('vid,what', [('K-04', 'X >= p'), ('K-16', 'X >= p (SPKI)'), ('K-36', 'Y >= p'), ('K-37', 'Y >= p (SPKI)'),
                                          ('K-03', 'off curve'), ('K-15', 'off curve (SPKI)'), ('L-03', 'invalid-curve order-2 point'),
                                          ('L-01', '(0, 0)')])
    def test_rejected_before_constructor(self, vid, what):
        v = by_id(vid)
        out, ctor = self.run(self.key(vid), v['slot'], v['alg'])
        assert out == 'KEY_FORMAT', what
        ctor.assert_not_called()

    @pytest.mark.parametrize('what', ['compressed', 'hybrid', 'bare-xy', 'leading-05'])
    def test_representation_rejected_before_constructor(self, what):
        raw = self.key('K-01'); x, y = raw[-64:-32], raw[-32:]
        point = {'compressed': bytes([2 + (y[-1] & 1)]) + x + bytes(32),  # padded to the 65-byte length
                 'hybrid': bytes([6 + (y[-1] & 1)]) + x + y,
                 'bare-xy': b'\x00' + x + y,
                 'leading-05': b'\x05' + x + y}[what]
        out, ctor = self.run(raw[:17] + point)
        assert out == 'KEY_FORMAT'
        ctor.assert_not_called()


# -------------------------------------------------------- library characterization (backs PROFILE.md)
class TestLibraryBehaviour:
    """These call cryptography directly ON PURPOSE: they record what the library does without the verifier's
    own checks, so PROFILE.md can say which verifier checks are load-bearing and which are defence in depth."""

    def point(self, vid):
        raw = bytes.fromhex(by_id(vid)['key_hex'])
        return raw[-64:-32], raw[-32:]

    def test_LIB01_numbers_rejects_off_curve(self):
        x, y = self.point('K-03')
        with pytest.raises(ValueError):
            ec.EllipticCurvePublicNumbers(int.from_bytes(x, 'big'), int.from_bytes(y, 'big'), ec.SECP256R1()).public_key()

    def test_LIB02_numbers_accepts_and_reduces_x_ge_p(self):
        x, y = self.point('K-04'); xc, yc = self.point('K-02')
        x = int.from_bytes(x, 'big'); assert x >= p256.P
        k = ec.EllipticCurvePublicNumbers(x, int.from_bytes(y, 'big'), ec.SECP256R1()).public_key()
        assert k.public_numbers().x == int.from_bytes(xc, 'big')  # library alone: non-canonical x accepted

    def test_LIB09_numbers_accepts_and_reduces_y_ge_p(self):
        x, y = self.point('K-36'); _, yc = self.point('K-35')
        y = int.from_bytes(y, 'big'); assert y >= p256.P
        k = ec.EllipticCurvePublicNumbers(int.from_bytes(x, 'big'), y, ec.SECP256R1()).public_key()
        assert k.public_numbers().y == int.from_bytes(yc, 'big')  # library alone: non-canonical y accepted

    def test_LIB10_ecdsa_x_of_R_reduced_mod_n(self):
        """Direct library call on E-10's inputs: accepted, so the library compares x(R) mod n with r."""
        f = load('F5-equation-variant.json'); v = by_id('E-10')
        sig = parse_signature(bytes.fromhex(v['sig_hex']))
        q = bytes.fromhex(f['keys']['xr-ge-n']['hex'])[-64:]
        pub = ec.EllipticCurvePublicNumbers(int.from_bytes(q[:32], 'big'), int.from_bytes(q[32:], 'big'), ec.SECP256R1()).public_key()
        digest = sha(bytes.fromhex(f['documents']['doc']) + sig.trailer)
        pub.verify(utils.encode_dss_signature(sig.r, sig.s), digest, ec.ECDSA(utils.Prehashed(hashes.SHA256())))

    def test_LIB03_der_loader_accepts_compressed_and_other_curves(self):
        comp = serialization.load_der_public_key(bytes.fromhex(by_id('K-17')['key_hex']))
        assert isinstance(comp, ec.EllipticCurvePublicKey) and comp.curve.name == 'secp256r1'
        k1 = serialization.load_der_public_key(bytes.fromhex(by_id('K-18')['key_hex']))
        assert isinstance(k1, ec.EllipticCurvePublicKey) and k1.curve.name == 'secp256k1'

    def test_LIB04_der_loader_accepts_other_mldsa_parameter_sets(self):
        for vid, kind in (('K-28', mldsa.MLDSA44PublicKey), ('K-29', mldsa.MLDSA87PublicKey)):
            assert isinstance(serialization.load_der_public_key(bytes.fromhex(by_id(vid)['key_hex'])), kind)

    def test_LIB05_ecdsa_verify_high_s_and_range(self):
        k = ec.derive_private_key(7, ec.SECP256R1()); pub = k.public_key(); d = sha(b'm')
        algo = ec.ECDSA(utils.Prehashed(hashes.SHA256()))
        r, s = utils.decode_dss_signature(k.sign(d, ec.ECDSA(utils.Prehashed(hashes.SHA256()), deterministic_signing=True)))
        pub.verify(utils.encode_dss_signature(r, s), d, algo)
        pub.verify(utils.encode_dss_signature(r, p256.N - s), d, algo)  # high-S accepted by the library
        for rr, ss in ((0, s), (r, 0), (p256.N, s), (r, p256.N), (r + p256.N, s), (r, s + p256.N)):
            with pytest.raises(InvalidSignature):
                pub.verify(utils.encode_dss_signature(rr, ss), d, algo)

    def test_LIB06_mldsa_key_loader(self):
        assert mldsa.MLDSA65PublicKey.from_public_bytes(bytes(1952)).public_bytes_raw() == bytes(1952)
        for n in (1951, 1953):
            with pytest.raises(ValueError):
                mldsa.MLDSA65PublicKey.from_public_bytes(bytes(n))

    @pytest.mark.parametrize('vid', TestMLDSAGate.MALFORMED + ['R-04', 'R-05'])
    def test_LIB07_mldsa_library_rejects_malformed_without_gate(self, vid):
        f = load('F2-signature-encodings.json')
        pub = public_key(bytes.fromhex(f['keys']['kms-mldsa65']['hex']), 'kms', HYBRID_ALG)
        with pytest.raises(InvalidSignature):
            pub.verify(bytes.fromhex(by_id(vid)['sig_hex']), bytes.fromhex(f['documents']['doc']), context=b'')

    def test_LIB08_mldsa_context_none_equals_empty(self):
        f = load('F2-signature-encodings.json')
        pub = public_key(bytes.fromhex(f['keys']['kms-mldsa65']['hex']), 'kms', HYBRID_ALG)
        sig = bytes.fromhex(by_id('R-01')['sig_hex']); doc = bytes.fromhex(f['documents']['doc'])
        pub.verify(sig, doc); pub.verify(sig, doc, context=b'')
        with pytest.raises(ValueError):
            pub.verify(sig, doc, context=bytes(256))


# ------------------------------------------------------------------------------- bundle level
def evaluate(b, t, c):
    return verify_bundle(jcs(b), parse_trust(jcs(t)), parse_catalog(jcs(c)))


def rebuild_anchor(items):
    raw = b'\x1d' + b'tessera-v1/receipt-anchor-sig' + b'\x02'
    for document, signature in items:
        raw += len(document).to_bytes(4, 'big') + document + len(signature).to_bytes(4, 'big') + signature
    return raw


@pytest.fixture(scope='module')
def hybrid():
    return make_fixture(hybrid=True)


class TestBundle:
    def test_B01_positive_control(self, hybrid):
        assert evaluate(*hybrid)['verdict'] == 'VALID_STRICT'

    def substitute(self, hybrid):
        b, t, c = copy.deepcopy(hybrid); layer = b['layers'][0]
        frames = read_anchor(b64(layer['a_sig']), registered_codecs(HYBRID_ALG))
        f, sig = frames[1][0], frames[1][3]
        honest = b64(layer['keys']['gpg'])
        e = int.from_bytes(sha(f + sig.trailer), 'big')
        hx, hy = int.from_bytes(honest[18:50], 'big'), int.from_bytes(honest[50:82], 'big')
        cands = p256.dsks_keys(e, sig.r, sig.s); assert (hx, hy) in cands
        sx, sy = next(q for q in cands if q != (hx, hy))
        sub = honest[:17] + b'\x04' + sx.to_bytes(32, 'big') + sy.to_bytes(32, 'big')
        return b, t, c, f, sig, sub

    def test_B02_key_substitution_verifies_but_is_bound_out(self, hybrid):
        b, t, c, f, sig, sub = self.substitute(hybrid)
        # The equation accepts the honest signature under a different, valid key (P3's premise) ...
        assert signature_verifies(f, sig, public_key(sub, 'gpg', HYBRID_ALG)) is True
        # ... and the verifier rejects the substituted bundle by the signed fingerprint binding.
        b['layers'][0]['keys']['gpg'] = enc(sub)
        r = evaluate(b, t, c)
        assert (r['verdict'], r['reason']) == ('INVALID', 'KEY_MISMATCH')

    def test_B03_substitution_with_rewritten_manifest(self, hybrid):
        b, t, c, f, sig, sub = self.substitute(hybrid)
        layer = b['layers'][0]
        manifest = codec.read_frame(b64(layer['manifest']), 'tessera-v1/manifest')
        manifest['sset'] = ['gpg-sha256:' + codec.shahex(sub)]
        layer['manifest'] = enc(codec.frame('tessera-v1/manifest', jcs(manifest)))
        layer['keys']['gpg'] = enc(sub)
        r = evaluate(b, t, c)
        assert r['verdict'] == 'INVALID' and r['reason'] == 'RECEIPT_MANIFEST_MISMATCH'

    def test_B04_off_curve_transported_key(self, hybrid):
        b, t, c = copy.deepcopy(hybrid); layer = b['layers'][0]
        k = bytearray(b64(layer['keys']['gpg'])); k[-1] ^= 1
        layer['keys']['gpg'] = enc(bytes(k))
        r = evaluate(b, t, c)
        assert (r['verdict'], r['reason']) == ('INVALID', 'KEY_FORMAT')

    def test_B05_out_of_range_r_in_receipt_slot(self, hybrid):
        b, t, c = copy.deepcopy(hybrid); layer = b['layers'][0]
        frames = read_anchor(b64(layer['a_sig']), registered_codecs(HYBRID_ALG))
        raw = frames[1][2]; sig = frames[1][3]
        rm = sig.r.bit_length().to_bytes(2, 'big') + sig.r.to_bytes((sig.r.bit_length() + 7) // 8, 'big')
        nm = (256).to_bytes(2, 'big') + p256.N.to_bytes(32, 'big')
        assert raw.count(rm) == 1
        bad = raw.replace(rm, nm); bad = bytes([bad[0], len(bad) - 2]) + bad[2:]
        layer['a_sig'] = enc(rebuild_anchor([(frames[0][0], frames[0][2]), (frames[1][0], bad)]))
        r = evaluate(b, t, c)
        assert (r['verdict'], r['reason']) == ('INVALID', 'SIG_POLICY')

    def test_B08_combined_failure_key_before_policy(self, hybrid):
        """Off-curve gpg key AND out-of-range r in the gpg receipt signature: row 5.1 (KEY_FORMAT) outranks 9.1."""
        b, t, c = copy.deepcopy(hybrid); layer = b['layers'][0]
        frames = read_anchor(b64(layer['a_sig']), registered_codecs(HYBRID_ALG))
        raw = frames[1][2]; sig = frames[1][3]
        rm = sig.r.bit_length().to_bytes(2, 'big') + sig.r.to_bytes((sig.r.bit_length() + 7) // 8, 'big')
        bad = raw.replace(rm, (256).to_bytes(2, 'big') + p256.N.to_bytes(32, 'big')); bad = bytes([bad[0], len(bad) - 2]) + bad[2:]
        layer['a_sig'] = enc(rebuild_anchor([(frames[0][0], frames[0][2]), (frames[1][0], bad)]))
        k = bytearray(b64(layer['keys']['gpg'])); k[-1] ^= 1; layer['keys']['gpg'] = enc(bytes(k))
        r = evaluate(b, t, c)
        assert (r['verdict'], r['reason']) == ('INVALID', 'KEY_FORMAT')

    @pytest.mark.parametrize('possession', [False, True])
    def test_B06_lax_equivalent_hint_padding(self, possession):
        def padded(k, d):
            import hashlib
            tr = hashlib.shake_256(k.public_key().public_bytes_raw()).digest(64)
            for _ in range(200):
                s = k.sign_mu(hashlib.shake_256(tr + b'\x00\x00' + d).digest(64))
                if s[-1] < 55: return s[:3248 + 54] + b'\x01' + s[3248 + 55:]
            raise AssertionError('no signature with a free hint slot')
        kw = {'kms_possession_signer': padded} if possession else {'kms_signer': padded}
        r = evaluate(*make_fixture(hybrid=True, **kw))
        assert (r['verdict'], r['reason']) == ('INVALID', 'POSSESSION_INVALID' if possession else 'SIG_INVALID')

    def test_B07_off_curve_repository_key_refuses_trust_config(self, hybrid):
        _, t, _ = copy.deepcopy(hybrid)
        k = bytearray(b64(t['repository_keys'][0]['key'])); k[-1] ^= 1
        t['repository_keys'][0]['key'] = enc(bytes(k))
        with pytest.raises(Fault) as e:
            parse_trust(jcs(t))
        assert e.value.code == 'TRUST_CONFIG_UNAUTHENTICATED'


# ------------------------------------------------------------- observation outside P3 (DIVERGENCES.md D1)
def test_OBS_test_release_auth_accepts_non_p256_curve(tmp_path, hybrid):
    """The TEST release stand-in checks isinstance(EllipticCurvePublicKey), not the curve: a secp256k1 key is
    accepted under alg 'ECDSA-P256-SHA256'. Recorded as observed behaviour, not fixed (outside P3; TEST path)."""
    _, _, catalog = hybrid
    signer = ec.derive_private_key(11, ec.SECP256K1())
    spki = signer.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    (tmp_path / 'r.json').write_text(json.dumps(make_release(signer, spki, b'trust', catalog)))
    (tmp_path / 'k.json').write_text(json.dumps(key_file(spki)))
    body = release_auth.authenticate_test_release(tmp_path / 'r.json', tmp_path / 'k.json')
    assert body['format'] == release_auth.TEST_FORMAT


# ------------------------------------------------------------------------------------ A11C-01 (path aliases)
BINDING = b'stand-in native binding'


@pytest.fixture
def stand_in_wheel(monkeypatch):
    """Record a stand-in binding digest so a hand-built zip passes the wheel checks and reaches the path checks
    (without it every case fails on the binding digest, and the alias tests would pass vacuously)."""
    monkeypatch.setitem(F1['wheel'], 'rust_binding_sha256', hashlib.sha256(BINDING).hexdigest())


def _zip_with(tmp_path, name, extra):
    """A zip holding the (stand-in) wheel binding and tag, the tested verifier, and `extra` entries."""
    out = tmp_path / name
    with zipfile.ZipFile(out, 'w') as z:
        z.writestr(F1['wheel']['rust_binding'], BINDING)
        z.writestr('cryptography-%s.dist-info/WHEEL' % F1['cryptography'], 'Tag: %s\n' % F1['wheel']['tag'])
        for n, data in tested_verifier_files().items():
            z.writestr(n, data)
        for n, data in extra:
            z.writestr(n, data)
    return out


def test_A11C01_a_clean_zip_passes(tmp_path, stand_in_wheel):
    check_zip(_zip_with(tmp_path, 'clean.zip', []))           # positive control: the refusals below are about paths


@pytest.mark.parametrize('alias', ['./tessera_verify/codec.py', 'tessera_verify//codec.py',
                                   'tessera_verify/../tessera_verify/codec.py', '/tessera_verify/codec.py',
                                   'tessera_verify\\codec.py', 'tessera_verify/codec.py'])
def test_A11C01_an_alias_or_duplicate_of_a_verifier_file_is_refused(tmp_path, alias, stand_in_wheel):
    """Codex confirmation 2: './tessera_verify/codec.py' passed a literal-prefix check and overwrote the checked file
    on extraction. Every non-canonical or duplicate entry is refused, whatever it names."""
    z = _zip_with(tmp_path, 'alias.zip', [(alias, b'raise RuntimeError("substituted verifier")\n')])
    with pytest.raises(AssertionError):
        check_zip(z)


def test_A11C01_a_symlink_entry_is_refused(tmp_path, stand_in_wheel):
    """An entry marked as a symlink (S_IFLNK in external_attr) can redirect extraction on unpackers that honour it."""
    out = _zip_with(tmp_path, 'link.zip', [])
    with zipfile.ZipFile(out, 'a') as z:
        info = zipfile.ZipInfo('tessera_link')
        info.external_attr = (0o120777 << 16)
        z.writestr(info, 'tessera_verify')
    with pytest.raises(AssertionError):
        check_zip(out)


# ------------------------------------------------------------------------------------ A11C3B (deployed identity)
def code_sha256_matches(zip_bytes, aws_code_sha256):
    """AWS reports CodeSha256 as base64 of the raw SHA-256 of the deployment package (FunctionConfiguration)."""
    return base64.b64encode(hashlib.sha256(zip_bytes).digest()).decode() == aws_code_sha256


def test_A11C3B_code_sha256_comparison():
    z = b'PK\x05\x06' + bytes(18)
    assert code_sha256_matches(z, base64.b64encode(hashlib.sha256(z).digest()).decode())
    assert not code_sha256_matches(z + b'x', base64.b64encode(hashlib.sha256(z).digest()).decode())
    assert not code_sha256_matches(z, hashlib.sha256(z).hexdigest())   # hex, as package.py prints, is not AWS's form
