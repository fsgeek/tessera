"""Wycheproof vectors (C2SP/wycheproof, pinned in wycheproof/SOURCE.md) run against the V1 service verifier.

Run from service/verifier:
    .venv/bin/python -m pytest -q ../../formal/p3-verification-profile/test_wycheproof.py
The per-case table (counts per result class, every disagreement with tcId and comment) is printed even under
capture, by TestReport.

LAYERS. Every case is labelled with the layer that decided it; nothing here claims more than that layer.

  VERIFIER  calls tessera_verify.codec's own functions: public_key, parse_signature, sig_policy,
            signature_verifies (and, through them, point and mldsa65_encoding_valid).
  LIBRARY   calls `cryptography` directly, with Wycheproof's own encodings. It characterizes the backend the verifier
            uses; it is NOT evidence about the verifier.

ML-DSA-65 (VERIFIER, end to end, no adaptation beyond wrapping):
  key  = public_key(publicKeyDer, 'kms', HYBRID_ALG)            (Wycheproof supplies the exact RFC 9881 SPKI)
  sig  = parse_signature(sig, HYBRID_ALG, 'kms', registered_codecs(HYBRID_ALG)); sig_policy(sig)
  ok   = signature_verifies(msg, sig, key)                       (the verifier's document F is Wycheproof's msg)
  V1 verifies with the empty context only, so a case with a non-empty ctx is evaluated as V1 would evaluate those
  bytes: under the empty context.

ECDSA P-256 (VERIFIER for keys, signature codec, policy and the verification call, with ONE substitution):
  key  = public_key(04 || ts || GPG_PREFIX || uncompressed, 'gpg')      (the V1 gpg-slot key form)
         public_key(publicKeyDer, 'kms', ALG)                           (the fallback-slot SPKI form; must agree)
  sig  = an OpenPGP v4 signature packet built from (r, s): hashed area = one creation-time subpacket, empty unhashed
         area, prefix = SHA256(msg)[:2], r and s as minimal MPIs. Run through parse_signature(.., ALG, 'gpg') and
         sig_policy, which apply V1's MPI rules and its r, s in [1, n-1] range check.
  ok   = signature_verifies(msg, replace(parsed, trailer=b''), key)
  The substitution: V1's digest is SHA256(F || v4 trailer); Wycheproof's is SHA256(msg). No choice of F makes
  F || trailer equal an arbitrary msg (the trailer is fixed by the packet header), so the parsed Signature's trailer
  is replaced by b''. The digest then equals SHA256(msg), and everything else (the prefix comparison, DER encoding of
  (r, s), the Prehashed verify call) is the verifier's own code. This is the only deviation from a real V1 packet.
  Encodings with no V1 counterpart are NOT routed: P1363 strings that are not 64 bytes (there is no fixed-width form
  in V1), DER that the strict decoder rejects (V1 never parses DER), and DER INTEGERs that decode negative (V1 MPIs are
  unsigned). For DER, decoding is done by cryptography's decode_dss_signature (LIBRARY): V1 has no DER parser.
"""
import collections
import dataclasses
import hashlib
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
VERIFIER = HERE.parent.parent / 'service' / 'verifier'
sys.path[:0] = [str(VERIFIER)]

from tessera_verify import install_record  # noqa: E402
install_record.load_and_apply()  # as tests/conftest.py does

from cryptography.exceptions import InvalidSignature  # noqa: E402
from cryptography.hazmat.primitives import hashes, serialization  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import ec, mldsa, utils  # noqa: E402

from tessera_verify.codec import (ALG, GPG_PREFIX, HYBRID_ALG, Fault, mldsa65_encoding_valid,  # noqa: E402
                                  parse_signature, public_key, registered_codecs, sig_policy, signature_verifies)

WP = HERE / 'wycheproof'
FILES = {
    'der': 'ecdsa_secp256r1_sha256_test.json',
    'p1363': 'ecdsa_secp256r1_sha256_p1363_test.json',
    'mldsa': 'mldsa_65_verify_test.json',
}
SHA256 = {  # as recorded in wycheproof/SOURCE.md
    'ecdsa_secp256r1_sha256_test.json': '182db4f3e230f6f9fa9f800d2a614dede30284b8e8438bbfe1171905402e9332',
    'ecdsa_secp256r1_sha256_p1363_test.json': 'c60de693930e386c3a5472d08081623ef8504decc54b38ac01ec6b2a2575c986',
    'mldsa_65_verify_test.json': '1ca235f61928421a173a171780beb00264ae9155dc33c52a11e1766cc7979034',
}
NOT_ROUTED = 'NOT_ROUTED'   # no V1 encoding of this input exists; see the module docstring
KEY_TS = bytes.fromhex('65000000')

# Every case where the VERIFIER verdict differs from Wycheproof's valid/invalid, with the reason. The test fails if
# the observed set of disagreements differs from this table in either direction.
DOCUMENTED = {
    ('mldsa', 3): 'V1 policy: pure ML-DSA-65 with the EMPTY context only (PROFILE.md §2 rule R, §4 E-04/E-09; '
                  'HYBRID-SUPPLEMENT §2). Wycheproof signs under a 7-byte context; V1 verifies under b\'\'.',
    ('mldsa', 4): 'V1 policy: empty context only (as tcId 3). Wycheproof signs under a 255-byte context.',
}


def load(kind):
    return json.loads((WP / FILES[kind]).read_text())


def cases(kind):
    for g in load(kind)['testGroups']:
        for t in g['tests']:
            yield g, t


# --------------------------------------------------------------------------------------------- ML-DSA
def v1_mldsa(g, t):
    try:
        key = public_key(bytes.fromhex(g['publicKeyDer']), 'kms', HYBRID_ALG)
        sig = parse_signature(bytes.fromhex(t['sig']), HYBRID_ALG, 'kms', registered_codecs(HYBRID_ALG))
        sig_policy(sig)
    except Fault as e:
        return e.code
    return 'ACCEPT' if signature_verifies(bytes.fromhex(t['msg']), sig, key) else 'SIG_INVALID'


def lib_mldsa(g, t):
    try:
        key = mldsa.MLDSA65PublicKey.from_public_bytes(bytes.fromhex(g['publicKey']))
        key.verify(bytes.fromhex(t['sig']), bytes.fromhex(t['msg']), context=bytes.fromhex(t.get('ctx', '')))
        return 'ACCEPT'
    except InvalidSignature:
        return 'SIG_INVALID'
    except ValueError:
        return 'ValueError'


# --------------------------------------------------------------------------------------------- ECDSA
def gpg_key_body(uncompressed_hex):
    return b'\x04' + KEY_TS + GPG_PREFIX + bytes.fromhex(uncompressed_hex)


def mpi(v):
    bits = v.bit_length()
    return bits.to_bytes(2, 'big') + v.to_bytes((bits + 7) // 8, 'big')


def packet(r, s, msg):
    hashed = b'\x05\x02' + KEY_TS
    body = (b'\x04\x00\x13\x08' + len(hashed).to_bytes(2, 'big') + hashed + b'\x00\x00'
            + hashlib.sha256(msg).digest()[:2] + mpi(r) + mpi(s))
    head = b'\x88' + bytes([len(body)]) if len(body) <= 255 else b'\x89' + len(body).to_bytes(2, 'big')
    return head + body


def rs_of(kind, sig):
    """(r, s) for routing, or None if V1 has no encoding for this input."""
    if kind == 'p1363':
        if len(sig) != 64: return None
        return int.from_bytes(sig[:32], 'big'), int.from_bytes(sig[32:], 'big')
    try:
        r, s = utils.decode_dss_signature(sig)   # LIBRARY: V1 never parses DER
    except ValueError:
        return None
    if r < 0 or s < 0: return None
    return r, s


def v1_keys(g):
    """Both V1 P-256 key forms; they must be accepted identically and give the same point."""
    out = []
    for raw, slot, alg in ((gpg_key_body(g['publicKey']['uncompressed']), 'gpg', ALG),
                           (bytes.fromhex(g['publicKeyDer']), 'kms', ALG)):
        try:
            out.append(public_key(raw, slot, alg))
        except Fault as e:
            out.append(e.code)
    return out


def v1_ecdsa(kind, g, t):
    msg, sig = bytes.fromhex(t['msg']), bytes.fromhex(t['sig'])
    k_gpg, k_kms = v1_keys(g)
    if isinstance(k_gpg, str): return k_gpg
    rs = rs_of(kind, sig)
    if rs is None: return NOT_ROUTED
    try:
        parsed = parse_signature(packet(*rs, msg), ALG, 'gpg')
        sig_policy(parsed)
    except Fault as e:
        return e.code
    assert (parsed.r, parsed.s) == rs
    ok = signature_verifies(msg, dataclasses.replace(parsed, trailer=b''), k_gpg)
    return 'ACCEPT' if ok else 'SIG_INVALID'


def lib_ecdsa(kind, g, t):
    msg, sig = bytes.fromhex(t['msg']), bytes.fromhex(t['sig'])
    key = serialization.load_der_public_key(bytes.fromhex(g['publicKeyDer']))
    if kind == 'p1363':
        if len(sig) != 64: return NOT_ROUTED      # the library has no P1363 interface
        sig = utils.encode_dss_signature(int.from_bytes(sig[:32], 'big'), int.from_bytes(sig[32:], 'big'))
    try:
        key.verify(sig, msg, ec.ECDSA(hashes.SHA256())); return 'ACCEPT'
    except InvalidSignature:
        return 'SIG_INVALID'
    except ValueError:
        return 'ValueError'


# --------------------------------------------------------------------------------------------- table
def evaluate():
    rows = []
    for kind in FILES:
        for g, t in cases(kind):
            v1 = v1_mldsa(g, t) if kind == 'mldsa' else v1_ecdsa(kind, g, t)
            lib = lib_mldsa(g, t) if kind == 'mldsa' else lib_ecdsa(kind, g, t)
            rows.append(dict(kind=kind, tcId=t['tcId'], comment=t['comment'], flags=t['flags'], result=t['result'],
                             ctx=len(t.get('ctx', '')) // 2, v1=v1, lib=lib,
                             gate=(mldsa65_encoding_valid(bytes.fromhex(t['sig'])) if kind == 'mldsa'
                                   and len(t['sig']) == 2 * 3309 else None)))
    return rows


ROWS = evaluate()


def disagrees(outcome, result):
    if outcome == NOT_ROUTED or result == 'acceptable': return False
    return (outcome == 'ACCEPT') != (result == 'valid')


def report():
    lines = []
    for kind in FILES:
        rs = [r for r in ROWS if r['kind'] == kind]
        lines.append(f'== {FILES[kind]}: {len(rs)} cases')
        c = collections.Counter((r['result'], r['v1']) for r in rs)
        for (res, out), n in sorted(c.items()):
            lines.append(f'   wycheproof={res:<10} VERIFIER={out:<14} {n:4d}')
        c = collections.Counter((r['result'], r['lib']) for r in rs)
        for (res, out), n in sorted(c.items()):
            lines.append(f'   wycheproof={res:<10} LIBRARY ={out:<14} {n:4d}')
        acc = [r for r in rs if r['result'] == 'acceptable']
        lines.append(f'   acceptable cases: {len(acc)}' + ''.join(f'\n     tcId {r["tcId"]}: V1 {r["v1"]}' for r in acc))
        for layer in ('v1', 'lib'):
            d = [r for r in rs if disagrees(r[layer], r['result'])]
            lines.append(f'   {"VERIFIER" if layer == "v1" else "LIBRARY"} disagreements: {len(d)}')
            for r in d:
                lines.append(f'     tcId {r["tcId"]:>3} wycheproof={r["result"]} got={r[layer]} ctx={r["ctx"]} '
                             f'flags={",".join(r["flags"])} :: {r["comment"]}')
        if kind == 'mldsa':
            gate = [r for r in rs if r['gate'] is False]
            lines.append(f'   rejected by the verifier\'s own mldsa65_encoding_valid gate (before the library): '
                         f'{len(gate)}; Wycheproof results {dict(collections.Counter(r["result"] for r in gate))}')
            lines.append('   evaluated under the empty context although Wycheproof gives a non-empty ctx: ' + ', '.join(
                f'tcId {r["tcId"]} (ctx {r["ctx"]} B, wycheproof={r["result"]}, V1 {r["v1"]})' for r in rs if r['ctx']))
        nr = [r for r in rs if r['v1'] == NOT_ROUTED]
        if nr:
            lines.append(f'   NOT_ROUTED (no V1 encoding): {len(nr)}; Wycheproof results '
                         f'{dict(collections.Counter(r["result"] for r in nr))}')
    return '\n'.join(lines)


# --------------------------------------------------------------------------------------------- tests
class TestSource:
    @pytest.mark.parametrize('name', sorted(SHA256))
    def test_pinned_digest(self, name):
        assert hashlib.sha256((WP / name).read_bytes()).hexdigest() == SHA256[name]
        assert SHA256[name] in (WP / 'SOURCE.md').read_text()

    def test_counts_match_headers(self):
        for kind in FILES:
            assert load(kind)['numberOfTests'] == sum(1 for r in ROWS if r['kind'] == kind)


def ids(kind): return [pytest.param(r, id=f'{kind}-{r["tcId"]}') for r in ROWS if r['kind'] == kind]


@pytest.mark.parametrize('row', ids('mldsa') + ids('p1363') + ids('der'))
def test_verifier_case(row):
    """VERIFIER layer: the verdict equals Wycheproof's, or the disagreement is the documented one."""
    key = (row['kind'], row['tcId'])
    if key in DOCUMENTED:
        assert disagrees(row['v1'], row['result']), DOCUMENTED[key]
    else:
        assert not disagrees(row['v1'], row['result']), (row['v1'], row['comment'])


def test_documented_set_is_exact():
    observed = {(r['kind'], r['tcId']) for r in ROWS if disagrees(r['v1'], r['result'])}
    assert observed == set(DOCUMENTED)


def test_library_layer_agrees_with_wycheproof():
    """LIBRARY layer (the backend alone, Wycheproof's own encodings and contexts). Not evidence about the verifier."""
    assert [(r['kind'], r['tcId']) for r in ROWS if disagrees(r['lib'], r['result'])] == []


def test_no_acceptable_cases_in_pinned_files():
    assert not [r for r in ROWS if r['result'] == 'acceptable']


def test_mldsa_gate_rejects_only_invalid():
    """The verifier's own FIPS 204 encoding gate never rejects a Wycheproof-valid signature."""
    gated = [r for r in ROWS if r['gate'] is False]
    assert gated and all(r['result'] == 'invalid' for r in gated)


class TestEcdsaAdaptation:
    def test_every_key_accepted_identically_in_both_v1_forms(self):
        for kind in ('der', 'p1363'):
            for g in load(kind)['testGroups']:
                k_gpg, k_kms = v1_keys(g)
                assert not isinstance(k_gpg, str) and not isinstance(k_kms, str)
                assert k_gpg.public_numbers() == k_kms.public_numbers()

    def test_trailer_substitution_is_neutral_on_a_real_packet(self):
        """The substitution only redirects the digest: on a real V1 packet (trailer kept) the same code accepts a
        signature over SHA256(F || trailer), and the substituted path accepts a signature over SHA256(msg)."""
        priv = ec.derive_private_key(7, ec.SECP256R1())
        raw = priv.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
        key = public_key(gpg_key_body(raw.hex()), 'gpg')
        msg = b'wycheproof-adaptation-control'
        # substituted path
        r, s = utils.decode_dss_signature(priv.sign(msg, ec.ECDSA(hashes.SHA256())))
        p = parse_signature(packet(r, s, msg), ALG, 'gpg'); sig_policy(p)
        assert signature_verifies(msg, dataclasses.replace(p, trailer=b''), key)
        assert not signature_verifies(msg, p, key)       # with its real trailer, the digest differs
        # real packet path: sign SHA256(msg || trailer)
        trailer = p.trailer
        d = hashlib.sha256(msg + trailer).digest()
        r2, s2 = utils.decode_dss_signature(priv.sign(d, ec.ECDSA(utils.Prehashed(hashes.SHA256()))))
        raw_pkt = bytearray(packet(r2, s2, msg)); i = 2 + 4 + 2 + 6 + 2; raw_pkt[i:i + 2] = d[:2]
        p2 = parse_signature(bytes(raw_pkt), ALG, 'gpg'); sig_policy(p2)
        assert p2.trailer == trailer and signature_verifies(msg, p2, key)

    def test_routed_rs_reach_range_check(self):
        """Out-of-range (r, s) are decided by the verifier's own codec/policy, not by the library."""
        routed = [r for r in ROWS if r['kind'] != 'mldsa' and r['v1'] in ('SIG_FORMAT', 'SIG_POLICY')]
        assert routed and all(r['result'] == 'invalid' for r in routed)


class TestReport:
    def test_print_table(self, capsys):
        text = report()
        with capsys.disabled():
            print('\n' + text)
        assert text
