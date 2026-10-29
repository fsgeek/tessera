"""Generate the P3 verification-profile vectors (vectors/*.json).

Run from service/verifier:  .venv/bin/python ../../formal/p3-verification-profile/gen_vectors.py
`cryptography` and p256.py are used only to CONSTRUCT inputs. Acceptance is decided by the tests, which call the
service verifier's own functions. Keys are fixed (P-256 scalars, ML-DSA seed); rule-O signatures use RFC 6979
deterministic ECDSA; ML-DSA signing is hedged (random), so regeneration changes the rule-R signature bytes but not
any expected outcome. The committed files are the record; this script is their provenance.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERIFIER = HERE.parent.parent / 'service' / 'verifier'
sys.path[:0] = [str(VERIFIER), str(HERE)]

import cryptography
from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, mldsa, utils
from tessera_verify.codec import ALG, HYBRID_ALG, GPG_PREFIX, SPKI, MLDSA65_SPKI, frame, jcs, sha
import p256

OUT = HERE / 'vectors'
PAIR = HYBRID_ALG
GAMMA1, BETA, OMEGA, K = 1 << 19, 196, 55, 6
SHA256_OID = bytes.fromhex('0609608648016503040201')
SHA512_OID = bytes.fromhex('0609608648016503040203')

GPG_D = int.from_bytes(hashlib.sha256(b'tessera p3 profile gpg key').digest(), 'big') % p256.N
KMS_D = int.from_bytes(hashlib.sha256(b'tessera p3 profile fallback kms key').digest(), 'big') % p256.N
OTHER_D = int.from_bytes(hashlib.sha256(b'tessera p3 profile other key').digest(), 'big') % p256.N
MLDSA_SEED = hashlib.sha256(b'tessera p3 profile ml-dsa-65 seed').digest()

gpg_priv = ec.derive_private_key(GPG_D, ec.SECP256R1())
kms_priv = ec.derive_private_key(KMS_D, ec.SECP256R1())
other_priv = ec.derive_private_key(OTHER_D, ec.SECP256R1())
ml_priv = mldsa.MLDSA65PrivateKey.from_seed_bytes(MLDSA_SEED)
ml_pub_raw = ml_priv.public_key().public_bytes_raw()
ml_spki = ml_priv.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
assert ml_spki == MLDSA65_SPKI + ml_pub_raw

DOC = frame('tessera-v1/attest', jcs({'common': {'note': 'P3 verification-profile vector document'},
                                      'signer': {'key_fp': 'gpg-sha256:' + '0' * 64}}))
OTHER_DOC = DOC[:-2] + b'x}'  # same length, different bytes (still not re-parsed by these functions)


def xy(priv):
    n = priv.public_key().public_numbers(); return n.x, n.y


def pt65(x, y, lead=4): return bytes([lead]) + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')
def gpg_packet(point, version=4, creation=bytes(4), prefix=GPG_PREFIX): return bytes([version]) + creation + prefix + point
def spki_p256(point): return SPKI + point


def mpi(n, bits=None, pad=b''):
    bits = n.bit_length() if bits is None else bits
    return bits.to_bytes(2, 'big') + pad + n.to_bytes((n.bit_length() + 7) // 8, 'big')


CT = b'\x05\x02' + bytes.fromhex('6a0e0b00')  # creation-time subpacket, 4 data octets


def head(version=4, typ=0, pkalg=0x13, halg=8, hashed=CT):
    return bytes([version, typ, pkalg, halg]) + len(hashed).to_bytes(2, 'big') + hashed


def digest_for(document, h): return sha(document + h + b'\x04\xff' + len(h).to_bytes(4, 'big'))


def ecdsa_rs(priv, digest):
    der = priv.sign(digest, ec.ECDSA(utils.Prehashed(hashes.SHA256()), deterministic_signing=True))
    return utils.decode_dss_signature(der)


def packet(h, prefix, rm, sm, unhashed=b''):
    body = h + len(unhashed).to_bytes(2, 'big') + unhashed + prefix + rm + sm
    if len(body) <= 255: return b'\x88' + bytes([len(body)]) + body
    return b'\x89' + len(body).to_bytes(2, 'big') + body


def rule_o(priv, document, **kw):
    h = head(**{k: v for k, v in kw.items() if k in ('version', 'typ', 'pkalg', 'halg', 'hashed')})
    d = digest_for(document, h); r, s = ecdsa_rs(priv, d)
    if s > p256.N // 2: s = p256.N - s  # normalize to low-S, so the O-02 twin is the high-S one (P3R-05)
    return h, d, r, s


def hx(b): return b.hex()


def write(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=1, sort_keys=False) + '\n')


# ---------------------------------------------------------------- keys used by signature vectors
GPG_KEY = gpg_packet(pt65(*xy(gpg_priv)))
KMS_P256_KEY = spki_p256(pt65(*xy(kms_priv)))
KEYS = {'gpg': {'slot': 'gpg', 'alg': PAIR, 'hex': hx(GPG_KEY)},
        'kms-mldsa65': {'slot': 'kms', 'alg': PAIR, 'hex': hx(ml_spki)},
        'kms-p256-fallback': {'slot': 'kms', 'alg': ALG, 'hex': hx(KMS_P256_KEY)}}
DOCS = {'doc': hx(DOC), 'other': hx(OTHER_DOC)}


def sigv(vid, case, slot, alg, key, sig, expect, why, document='doc'):
    return {'id': vid, 'case': case, 'slot': slot, 'alg': alg, 'key': key, 'document': document,
            'sig_hex': hx(sig), 'expect': expect, 'why': why}


def keyv(vid, case, slot, alg, key, expect, why):
    return {'id': vid, 'case': case, 'slot': slot, 'alg': alg, 'key_hex': hx(key), 'expect': expect, 'why': why}


def build_f2_rule_o():
    h, d, r, s = rule_o(gpg_priv, DOC)
    good = packet(h, d[:2], mpi(r), mpi(s))
    hs = packet(h, d[:2], mpi(r), mpi(p256.N - s))
    # A longer unhashed area forces the two-octet legacy length (body >= 256 bytes).
    pad = b'\x41' + b'\x65' + b'z' * 64  # non-critical type 101 subpacket, 65 bytes (ignored: unhashed)
    long_ok = packet(h, d[:2], mpi(r), mpi(s), unhashed=pad * 3)
    assert long_ok[0] == 0x89
    raw_rs = r.to_bytes(32, 'big') + s.to_bytes(32, 'big')
    assert raw_rs[0] not in (0x88, 0x89)
    der = utils.encode_dss_signature(r, s)
    body = good[2:]
    v = [
        sigv('O-01', 'valid rule-O packet (positive control)', 'gpg', PAIR, 'gpg', good, 'ACCEPT', 'ENC 5.2 rule O'),
        sigv('O-02', 'high-S twin (r, n-s) of the low-S O-01', 'gpg', PAIR, 'gpg', hs, 'ACCEPT', 'V1-PROFILE 8: "low-s not required"; ECDSA is malleable, exact-copy integrity comes from the anchor'),
        sigv('O-03', 'two-octet legacy length for a body >= 256 bytes', 'gpg', PAIR, 'gpg', long_ok, 'ACCEPT', 'ENC 5.2: 0x89 u16 for 256..1021'),
        sigv('O-04', 'OpenPGP-format (0xC2) header', 'gpg', PAIR, 'gpg', b'\xc2' + bytes([len(body)]) + body, 'SIG_PACKET', 'ENC 5.2: legacy header only'),
        sigv('O-05', 'non-shortest legacy header (0x89 for a short body)', 'gpg', PAIR, 'gpg', b'\x89' + len(body).to_bytes(2, 'big') + body, 'SIG_PACKET', 'ENC 5.2: shortest form only'),
        sigv('O-06', 'bare DER ECDSA-Sig-Value instead of an OpenPGP packet', 'gpg', PAIR, 'gpg', der, 'SIG_PACKET', 'DER is never accepted as S; the verifier builds DER itself from the MPIs'),
        sigv('O-07', 'raw r||s (64 bytes) instead of an OpenPGP packet', 'gpg', PAIR, 'gpg', raw_rs, 'SIG_PACKET', 'only rule O serialization'),
        sigv('O-08', 'ASCII armor', 'gpg', PAIR, 'gpg', b'-----BEGIN PGP SIGNATURE-----\n', 'SIG_PACKET', 'ENC 5.2: never armor'),
        sigv('O-09', 'trailing byte after the packet', 'gpg', PAIR, 'gpg', good + b'\x00', 'TRAILING', 'decoder consumes S exactly'),
        sigv('O-10', 'packet truncated by one byte', 'gpg', PAIR, 'gpg', good[:-1], 'TRUNCATED', 'decoder consumes S exactly'),
        sigv('O-11', 'version 5 signature', 'gpg', PAIR, 'gpg', packet(head(version=5), d[:2], mpi(r), mpi(s)), 'SIG_FORMAT', 'v4 only'),
        sigv('O-12', 'signature type 0x01 (text)', 'gpg', PAIR, 'gpg', packet(head(typ=1), d[:2], mpi(r), mpi(s)), 'SIG_FORMAT', 'D-10: type 0x00 only'),
        sigv('O-13', 'public-key algorithm 22 (EdDSA) in place of 19 (ECDSA)', 'gpg', PAIR, 'gpg', packet(head(pkalg=22), d[:2], mpi(r), mpi(s)), 'SIG_FORMAT', 'algorithm 0x13 only'),
        sigv('O-14', 'hash algorithm 10 (SHA-512) in place of 8', 'gpg', PAIR, 'gpg', packet(head(halg=10), d[:2], mpi(r), mpi(s)), 'SIG_FORMAT', 'SHA-256 only'),
        sigv('O-15', 'MPI r with a leading zero octet (bit count overstated by 8)', 'gpg', PAIR, 'gpg', packet(h, d[:2], mpi(r, r.bit_length() + 8, b'\x00'), mpi(s)), 'SIG_FORMAT', 'exact MPI bit count (non-canonical integer encoding)'),
        sigv('O-16', 'MPI r of 257 bits (r + 2^256)', 'gpg', PAIR, 'gpg', packet(h, d[:2], mpi(r + (1 << 256)), mpi(s)), 'SIG_FORMAT', 'MPI 1..256 bits'),
        sigv('O-17', 'r = 0 (zero-bit MPI)', 'gpg', PAIR, 'gpg', packet(h, d[:2], b'\x00\x00', mpi(s)), 'SIG_FORMAT', 'V1-PROFILE 8: zero fails the MPI grammar first'),
        sigv('O-18', 'r = n', 'gpg', PAIR, 'gpg', packet(h, d[:2], mpi(p256.N), mpi(s)), 'SIG_POLICY', 'V1-PROFILE 8: r outside [1, n-1] is SIG_POLICY'),
        sigv('O-19', 's = n', 'gpg', PAIR, 'gpg', packet(h, d[:2], mpi(r), mpi(p256.N)), 'SIG_POLICY', 'V1-PROFILE 8'),
        sigv('O-20', 'r = 2^256 - 1', 'gpg', PAIR, 'gpg', packet(h, d[:2], mpi((1 << 256) - 1), mpi(s)), 'SIG_POLICY', 'V1-PROFILE 8'),
        sigv('O-21', 'hash-prefix octets flipped (signature otherwise valid)', 'gpg', PAIR, 'gpg', packet(h, bytes([d[0] ^ 1, d[1]]), mpi(r), mpi(s)), 'SIG_INVALID', 'V1-PROFILE 8 hash prefix'),
        sigv('O-22', 'valid packet over a different document', 'gpg', PAIR, 'gpg', good, 'SIG_INVALID', 'signature binds the frame', document='other'),
    ]
    oh, od, orr, os_ = rule_o(other_priv, DOC)
    v.append(sigv('O-23', 'valid packet by a different P-256 key', 'gpg', PAIR, 'gpg', packet(oh, od[:2], mpi(orr), mpi(os_)), 'SIG_INVALID', 'wrong key'))
    # Fallback catalog: rule O in the kms slot with a P-256 SPKI key.
    kh, kd, kr, ks = rule_o(kms_priv, DOC)
    v.append(sigv('O-24', 'fallback id: rule O in slot kms with a P-256 SPKI (positive control)', 'kms', ALG, 'kms-p256-fallback', packet(kh, kd[:2], mpi(kr), mpi(ks)), 'ACCEPT', 'ENC 5.2 classical row'))
    v.append(sigv('O-25', 'rule-O packet presented in the hybrid kms slot', 'kms', PAIR, 'kms-mldsa65', good, 'SIG_FORMAT', 'rule R: any length other than 3309 below the cap'))
    return v


def mldsa_variants():
    tr = hashlib.shake_256(ml_pub_raw).digest(64)
    mu = lambda m: hashlib.shake_256(tr + m).digest(64)
    # Find a pure signature whose hint vector leaves room for the lax-equivalent rewrites.
    for _ in range(200):
        sig = ml_priv.sign(DOC, context=b'')
        hints = sig[3248:]; counts = list(hints[OMEGA:])
        if counts[0] >= 2 and counts[-1] <= OMEGA - 2: break
    else: raise SystemExit('no suitable signature found')
    idx = hints[:OMEGA]; c, z = sig[:48], sig[48:3248]
    dup = (idx[:1] + idx[:counts[-1]]).ljust(OMEGA, b'\x00') + bytes(x + 1 for x in counts)
    swap = bytearray(hints); swap[0], swap[1] = swap[1], swap[0]
    pad = bytearray(hints); pad[OMEGA - 1] = 1
    over = bytearray(hints); over[-1] = OMEGA + 1
    decr = bytearray(hints); decr[OMEGA], decr[OMEGA + 1] = decr[OMEGA + 1], decr[OMEGA]
    zbits = int.from_bytes(z, 'little')
    def zset(coef):
        return (((zbits >> 20) << 20) | (GAMMA1 - coef)).to_bytes(3200, 'little')
    flip = bytes([c[0] ^ 1]) + c[1:]
    return {'pure': sig, 'hints': hints, 'counts': counts, 'tr': tr, 'mu': mu,
            'dup': c + z + dup, 'swap': c + z + bytes(swap), 'pad': c + z + bytes(pad),
            'over': c + z + bytes(over), 'decr': c + z + bytes(decr),
            'zhi': c + zset(GAMMA1 - BETA) + hints, 'zlo': c + zset(-(GAMMA1 - BETA)) + hints,
            'zedge': c + zset(GAMMA1 - BETA - 1) + hints, 'ctilde': flip + z + hints}


def build_f2_rule_r(m):
    v = [
        sigv('R-01', 'pure ML-DSA-65, empty context (positive control)', 'kms', PAIR, 'kms-mldsa65', m['pure'], 'ACCEPT', 'ENC 5.2 rule R'),
        sigv('R-02', 'external-mu signature of the same message (positive control)', 'kms', PAIR, 'kms-mldsa65', ml_priv.sign_mu(m['mu'](b'\x00\x00' + DOC)), 'ACCEPT', 'issuer uses EXTERNAL_MU; result is an ordinary pure signature'),
        sigv('R-03', 'empty signature', 'kms', PAIR, 'kms-mldsa65', b'', 'SIG_EMPTY', 'HS 2'),
        sigv('R-04', '3308 bytes (truncated)', 'kms', PAIR, 'kms-mldsa65', m['pure'][:-1], 'SIG_FORMAT', 'HS 2'),
        sigv('R-05', '3310 bytes (trailing byte)', 'kms', PAIR, 'kms-mldsa65', m['pure'] + b'\x00', 'LENGTH_CAP', 'HS 2: cap 3309'),
        sigv('R-06', 'ML-DSA-44 signature (2420 bytes)', 'kms', PAIR, 'kms-mldsa65', mldsa.MLDSA44PrivateKey.from_seed_bytes(MLDSA_SEED).sign(DOC), 'SIG_FORMAT', 'parameter set is fixed by (alg, slot)'),
        sigv('R-07', 'ML-DSA-87 signature (4627 bytes)', 'kms', PAIR, 'kms-mldsa65', mldsa.MLDSA87PrivateKey.from_seed_bytes(MLDSA_SEED).sign(DOC), 'LENGTH_CAP', 'parameter set is fixed by (alg, slot)'),
        sigv('R-08', 'hint: nonzero padding in an unused index slot (a lax decoder decodes the same h)', 'kms', PAIR, 'kms-mldsa65', m['pad'], 'SIG_INVALID', 'FIPS 204 Alg. 21 HintBitUnpack; HS 2 internal malformation is verification failure'),
        sigv('R-09', 'hint: duplicated index in polynomial 0 (a lax decoder decodes the same h)', 'kms', PAIR, 'kms-mldsa65', m['dup'], 'SIG_INVALID', 'FIPS 204 Alg. 21: strictly increasing'),
        sigv('R-10', 'hint: two indices of polynomial 0 swapped (a lax decoder decodes the same h)', 'kms', PAIR, 'kms-mldsa65', m['swap'], 'SIG_INVALID', 'FIPS 204 Alg. 21: strictly increasing'),
        sigv('R-11', 'hint: final count omega+1', 'kms', PAIR, 'kms-mldsa65', m['over'], 'SIG_INVALID', 'FIPS 204 Alg. 21: count <= omega'),
        sigv('R-12', 'hint: decreasing cumulative counts', 'kms', PAIR, 'kms-mldsa65', m['decr'], 'SIG_INVALID', 'FIPS 204 Alg. 21'),
        sigv('R-13', 'z coefficient 0 set to +(gamma1 - beta)', 'kms', PAIR, 'kms-mldsa65', m['zhi'], 'SIG_INVALID', 'FIPS 204 Alg. 8: ||z||inf < gamma1 - beta'),
        sigv('R-14', 'z coefficient 0 set to -(gamma1 - beta)', 'kms', PAIR, 'kms-mldsa65', m['zlo'], 'SIG_INVALID', 'FIPS 204 Alg. 8'),
        sigv('R-15', 'z coefficient 0 set to gamma1 - beta - 1 (in range; signature still wrong)', 'kms', PAIR, 'kms-mldsa65', m['zedge'], 'SIG_INVALID', 'in-bound z passes the gate, fails the equation'),
        sigv('R-16', 'c-tilde bit flipped', 'kms', PAIR, 'kms-mldsa65', m['ctilde'], 'SIG_INVALID', 'challenge hash mismatch'),
        sigv('R-17', 'valid pure signature over a different document', 'kms', PAIR, 'kms-mldsa65', m['pure'], 'SIG_INVALID', 'signature binds the frame', document='other'),
        sigv('R-18', 'valid pure signature by a different ML-DSA-65 key', 'kms', PAIR, 'kms-mldsa65', mldsa.MLDSA65PrivateKey.from_seed_bytes(bytes(32)).sign(DOC), 'SIG_INVALID', 'wrong key'),
    ]
    return v


def sp(t, data, crit=False):
    """One shortest-form subpacket (all here are < 192 octets)."""
    assert len(data) + 1 < 192
    return bytes([len(data) + 1, t | (0x80 if crit else 0)]) + data


def build_f2_policy():
    """Rule-O signature policy (V1-PROFILE 8, 'Rule-O signature policy' and 'Advisory metadata'). Every vector is
    a correctly signed packet over its own hashed area, so each negative would verify if sig_policy were removed
    ('verifies_without_policy', checked by the tests)."""
    ct = bytes.fromhex('6a0e0b00')
    fp20 = hashlib.sha1(b'tessera p3 profile v4 fingerprint').digest()
    fp33 = b'\x04' + fp20; kid = fp20[-8:]
    def pv(vid, case, hashed, expect, why, unhashed=b''):
        h, d, r, s = rule_o(gpg_priv, DOC, hashed=hashed)
        v = sigv(vid, case, 'gpg', PAIR, 'gpg', packet(h, d[:2], mpi(r), mpi(s), unhashed=unhashed), expect, why)
        v['verifies_without_policy'] = True
        return v
    C = sp(2, ct)
    return [
        pv('P-01', 'creation time marked critical', sp(2, ct, True), 'ACCEPT', 'critical or not'),
        pv('P-02', 'GnuPG shape: hashed creation time + type 33; type 16 unhashed', C + sp(33, fp33), 'ACCEPT', 'GnuPG output satisfies the policy', unhashed=sp(16, kid)),
        pv('P-03', 'hashed types 16 and 33, consistent', C + sp(16, kid) + sp(33, fp33), 'ACCEPT', 'type-16 = last 8 octets of type 33'),
        pv('P-04', 'hashed types 16 and 33 both critical, consistent (recognized critical types)', C + sp(16, kid, True) + sp(33, fp33, True), 'ACCEPT', 'critical bits on 2/16/33 confer nothing and are allowed'),
        pv('P-05', 'unknown noncritical hashed subpacket (type 101)', C + sp(101, b'opaque'), 'ACCEPT', 'unknown noncritical ignored'),
        pv('P-06', 'unhashed area: critical unknown, critical expiration, malformed and inconsistent 16/33, duplicate creation time', C, 'ACCEPT', 'unhashed area ignored entirely, critical bits included',
           unhashed=sp(101, b'x', True) + sp(3, bytes(4), True) + sp(16, b'1234567') + sp(16, b'abcdefgh') + sp(33, b'\x05' + fp20) + sp(33, b'', True) + sp(2, ct) + sp(2, ct)),
        pv('P-10', 'no creation-time subpacket', b'', 'SIG_POLICY', 'exactly one type 2'),
        pv('P-11', 'two creation-time subpackets', C + C, 'SIG_POLICY', 'exactly one type 2'),
        pv('P-12', 'creation time with 3 data octets', sp(2, ct[:3]), 'SIG_POLICY', 'exactly four data octets'),
        pv('P-13', 'creation time with 5 data octets', sp(2, ct + b'\x00'), 'SIG_POLICY', 'exactly four data octets'),
        pv('P-14', 'creation time with 0 data octets', sp(2, b''), 'SIG_POLICY', 'exactly four data octets'),
        pv('P-15', 'signature-expiration subpacket (type 3), noncritical', C + sp(3, bytes.fromhex('00015180')), 'SIG_POLICY', 'no type 3, critical or not'),
        pv('P-16', 'signature-expiration subpacket (type 3), critical', C + sp(3, bytes.fromhex('00015180'), True), 'SIG_POLICY', 'no type 3, critical or not'),
        pv('P-17', 'unknown critical hashed subpacket (type 101)', C + sp(101, b'opaque', True), 'SIG_POLICY', 'other types fail if critical'),
        pv('P-18', 'RFC-known type 4 (exportable) marked critical', C + sp(4, b'\x01', True), 'SIG_POLICY', 'only 2, 16, 33 may be critical'),
        pv('P-19', 'type 16 with 7 octets', C + sp(16, kid[:7]), 'SIG_POLICY', 'type 16 exactly 8 octets'),
        pv('P-20', 'two type-16 subpackets', C + sp(16, kid) + sp(16, kid), 'SIG_POLICY', 'at most one type 16'),
        pv('P-21', 'type 33 with 20 octets', C + sp(33, fp33[:20]), 'SIG_POLICY', 'type 33 exactly 21 octets'),
        pv('P-22', 'type 33 version octet 05', C + sp(33, b'\x05' + fp20), 'SIG_POLICY', 'first octet 04'),
        pv('P-23', 'two type-33 subpackets', C + sp(33, fp33) + sp(33, fp33), 'SIG_POLICY', 'at most one type 33'),
        pv('P-24', 'types 16 and 33 inconsistent', C + sp(16, bytes(8)) + sp(33, fp33), 'SIG_POLICY', 'type-16 must equal last 8 octets of type 33'),
        pv('P-25', 'zero-data critical type 33', C + sp(33, b'', True), 'SIG_POLICY', 'V1-PROFILE 8: "A zero-data critical type 33 is therefore SIG_POLICY"'),
    ]


EXTRA_KEYS = {}


def equation_vectors():
    """P3R-03 (Codex construction, probe.py): a key for which u1 G + u2 Q = R with x(R) = n + r >= n, accepted
    because FIPS 186-5 compares x(R) mod n with r; and a key for which u1 G + u2 Q is the point at infinity."""
    h = head(); d = digest_for(DOC, h); e = int.from_bytes(d, 'big') % p256.N
    r = next(i for i in range(1, 100) if p256.lift_x(p256.N + i)); R = p256.lift_x(p256.N + r)
    assert R[0] == p256.N + r and R[0] < p256.P
    q = p256.mul(pow(r, -1, p256.N), p256.add(R, p256.neg(p256.mul(e, p256.G))))  # s = 1: R = e G + r Q
    q_inf = p256.mul((-e * pow(r, -1, p256.N)) % p256.N, p256.G)                  # e G + r Q = O
    EXTRA_KEYS['xr-ge-n'] = {'slot': 'gpg', 'alg': PAIR, 'hex': hx(gpg_packet(pt65(*q)))}
    EXTRA_KEYS['eq-infinity'] = {'slot': 'gpg', 'alg': PAIR, 'hex': hx(gpg_packet(pt65(*q_inf)))}
    sig = packet(h, d[:2], mpi(r), mpi(1))
    return [{**sigv('E-10', f'rule O: constructed key with x(R) = n + {r}, r = {r}, s = 1', 'gpg', PAIR, 'xr-ge-n', sig, 'ACCEPT',
                    'FIPS 186-5: accept iff x(R) mod n = r; an unreduced comparison x(R) = r would reject'), 'x_R': hex(R[0])},
            sigv('E-11', 'rule O: constructed key for which u1 G + u2 Q is the point at infinity (same r, s)', 'gpg', PAIR, 'eq-infinity', sig, 'SIG_INVALID',
                 'FIPS 186-5: R = O rejects')]


def build_f5(m):
    tr, mu = m['tr'], m['mu']
    h, d, r, s = rule_o(gpg_priv, DOC)
    # Equation input variants for rule O.
    plain = sha(DOC)  # ECDSA over SHA256(F) with no OpenPGP trailer
    r1, s1 = ecdsa_rs(gpg_priv, plain)
    der2 = gpg_priv.sign(d, ec.ECDSA(hashes.SHA256(), deterministic_signing=True))  # signs SHA256(digest)
    r2, s2 = utils.decode_dss_signature(der2)
    sha512d = hashlib.sha512(DOC + h + b'\x04\xff' + len(h).to_bytes(4, 'big')).digest()
    r3, s3 = ecdsa_rs(gpg_priv, sha512d[:32])  # SHA-512 digest truncated to 256 bits
    v = [
        sigv('E-01', 'rule O: ECDSA over SHA256(F) without the OpenPGP v4 trailer (correct prefix octets)', 'gpg', PAIR, 'gpg', packet(h, d[:2], mpi(r1), mpi(s1)), 'SIG_INVALID', 'message representative is SHA256(F || trailer)'),
        sigv('E-02', 'rule O: ECDSA over SHA256(SHA256(F || trailer)) (double hash; correct prefix octets)', 'gpg', PAIR, 'gpg', packet(h, d[:2], mpi(r2), mpi(s2)), 'SIG_INVALID', 'verifier passes the digest Prehashed; no second hash'),
        sigv('E-03', 'rule O: ECDSA over truncated SHA-512 of the hashed data, labelled SHA-256', 'gpg', PAIR, 'gpg', packet(h, d[:2], mpi(r3), mpi(s3)), 'SIG_INVALID', 'hash fixed to SHA-256'),
        sigv('E-04', 'rule R: pure ML-DSA with context "tessera-v1"', 'kms', PAIR, 'kms-mldsa65', ml_priv.sign(DOC, context=b'tessera-v1'), 'SIG_INVALID', 'empty context only: M\' = 00 || 00 || F'),
        sigv('E-05', 'rule R: HashML-DSA with SHA-256 (M\' = 01 || 00 || OID || SHA256(F))', 'kms', PAIR, 'kms-mldsa65', ml_priv.sign_mu(mu(b'\x01\x00' + SHA256_OID + hashlib.sha256(DOC).digest())), 'SIG_INVALID', 'pure mode only'),
        sigv('E-06', 'rule R: HashML-DSA with SHA-512', 'kms', PAIR, 'kms-mldsa65', ml_priv.sign_mu(mu(b'\x01\x00' + SHA512_OID + hashlib.sha512(DOC).digest())), 'SIG_INVALID', 'pure mode only'),
        sigv('E-07', 'rule R: ML-DSA.Sign_internal over F with no domain prefix (mu = H(tr || F))', 'kms', PAIR, 'kms-mldsa65', ml_priv.sign_mu(mu(DOC)), 'SIG_INVALID', 'FIPS 204 final external interface, not the internal one'),
        sigv('E-08', 'rule R: pure signature whose message is mu itself (issuer passed mu as M)', 'kms', PAIR, 'kms-mldsa65', ml_priv.sign(mu(b'\x00\x00' + DOC), context=b''), 'SIG_INVALID', 'verifier verifies over F, never over mu'),
        *equation_vectors(),
        sigv('E-09', 'rule R: pure signature with context of 255 zero bytes', 'kms', PAIR, 'kms-mldsa65', ml_priv.sign(DOC, context=bytes(255)), 'SIG_INVALID', 'empty context only'),
    ]
    return v


def build_f3_keys():
    gx, gy = xy(gpg_priv); kx, ky = xy(kms_priv)
    # A canonical point whose x is small enough that x + p still fits in 32 bytes.
    x0 = next(x for x in range(1000) if p256.lift_x(x))
    _, y0 = p256.lift_x(x0); assert x0 + p256.P < (1 << 256)
    noncanon = pt65(x0 + p256.P, y0)
    canon = pt65(x0, y0)
    small_y = p256.point_with_small_y(); assert small_y[1] + p256.P < (1 << 256)
    comp = bytes([2 + (gy & 1)]) + gx.to_bytes(32, 'big')
    comp_spki = bytes.fromhex('3039301306072a8648ce3d020106082a8648ce3d030107032200') + bytes([2 + (ky & 1)]) + kx.to_bytes(32, 'big')
    k1 = ec.derive_private_key(KMS_D, ec.SECP256K1()).public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    p384 = ec.derive_private_key(KMS_D, ec.SECP384R1()).public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    gpg_ok = GPG_KEY
    v = [
        keyv('K-01', 'gpg: v4 P-256 public-key packet body (positive control)', 'gpg', PAIR, gpg_ok, 'ACCEPT', 'V1-PROFILE 8 transported keys'),
        keyv('K-02', 'gpg: canonical point with small x (positive control for K-04)', 'gpg', PAIR, gpg_packet(canon), 'ACCEPT', 'on-curve, coordinates < p'),
        keyv('K-03', 'gpg: off-curve point (y + 1)', 'gpg', PAIR, gpg_packet(pt65(gx, (gy + 1) % p256.P)), 'KEY_FORMAT', 'FIPS 186-5 / SP 800-186 public-key validation'),
        keyv('K-04', 'gpg: non-canonical x (x + p, same residue as K-02)', 'gpg', PAIR, gpg_packet(noncanon), 'KEY_FORMAT', 'coordinates must be in [0, p-1]; the library alone would accept and reduce (L-02)'),
        keyv('K-05', 'gpg: compressed point (02/03 || x) with MPI bit count 263', 'gpg', PAIR, gpg_packet(comp, prefix=GPG_PREFIX[:-2] + b'\x01\x07'), 'KEY_FORMAT', 'uncompressed only'),
        keyv('K-06', 'gpg: hybrid point encoding (06/07 || x || y)', 'gpg', PAIR, gpg_packet(pt65(gx, gy, 6 + (gy & 1))), 'KEY_FORMAT', 'uncompressed 04 only'),
        keyv('K-07', 'gpg: version 5 key packet', 'gpg', PAIR, gpg_packet(pt65(gx, gy), version=5), 'KEY_FORMAT', 'v4 only'),
        keyv('K-08', 'gpg: algorithm 22 (EdDSA) in place of 19', 'gpg', PAIR, gpg_packet(pt65(gx, gy), prefix=b'\x16' + GPG_PREFIX[1:]), 'KEY_FORMAT', 'ECDSA P-256 only'),
        keyv('K-09', 'gpg: secp256k1 curve OID', 'gpg', PAIR, gpg_packet(pt65(gx, gy), prefix=b'\x13\x05\x2b\x81\x04\x00\x0a\x02\x03'), 'KEY_FORMAT', 'P-256 OID only'),
        keyv('K-10', 'gpg: point MPI bit count 520 in place of 515', 'gpg', PAIR, gpg_packet(pt65(gx, gy), prefix=GPG_PREFIX[:-2] + b'\x02\x08'), 'KEY_FORMAT', 'exact prefix'),
        keyv('K-11', 'gpg: trailing byte', 'gpg', PAIR, gpg_ok + b'\x00', 'KEY_FORMAT', 'exact length 82'),
        keyv('K-12', 'gpg: 0x99 || u16 length prefix (fingerprint preimage form)', 'gpg', PAIR, b'\x99' + len(gpg_ok).to_bytes(2, 'big') + gpg_ok, 'KEY_FORMAT', 'bare body only'),
        keyv('K-13', 'gpg: P-256 SPKI in the gpg slot', 'gpg', PAIR, KMS_P256_KEY, 'KEY_FORMAT', 'rule chosen by slot, not by key bytes'),
        keyv('K-14', 'kms fallback: P-256 SPKI (positive control)', 'kms', ALG, KMS_P256_KEY, 'ACCEPT', 'ENC 3.3'),
        keyv('K-15', 'kms fallback: off-curve point', 'kms', ALG, spki_p256(pt65(kx, (ky + 1) % p256.P)), 'KEY_FORMAT', 'public-key validation'),
        keyv('K-16', 'kms fallback: non-canonical x (x + p)', 'kms', ALG, spki_p256(noncanon), 'KEY_FORMAT', 'coordinates < p'),
        keyv('K-17', 'kms fallback: compressed-point SPKI (59 bytes)', 'kms', ALG, comp_spki, 'KEY_FORMAT', 'exact 91-byte encoding; the library alone would accept (L-03)'),
        keyv('K-18', 'kms fallback: secp256k1 SPKI', 'kms', ALG, k1, 'KEY_FORMAT', 'P-256 only'),
        keyv('K-19', 'kms fallback: P-384 SPKI', 'kms', ALG, p384, 'KEY_FORMAT', 'P-256 only'),
        keyv('K-20', 'kms fallback: ML-DSA-65 SPKI', 'kms', ALG, ml_spki, 'KEY_FORMAT', 'EA-24'),
        keyv('K-21', 'kms fallback: gpg key packet', 'kms', ALG, gpg_ok, 'KEY_FORMAT', 'slot rule'),
        keyv('K-22', 'kms hybrid: exact ML-DSA-65 SPKI (positive control)', 'kms', PAIR, ml_spki, 'ACCEPT', 'HS 3'),
        keyv('K-23', 'kms hybrid: all-zero 1952-byte public key in the exact SPKI', 'kms', PAIR, MLDSA65_SPKI + bytes(1952), 'ACCEPT', 'HS 3: no ML-DSA validation beyond encoding exists; every 1952-byte pkEncode is well formed'),
        keyv('K-24', 'kms hybrid: bare 1952-byte key', 'kms', PAIR, ml_pub_raw, 'KEY_FORMAT', 'exact SPKI only'),
        keyv('K-25', 'kms hybrid: NULL parameters in AlgorithmIdentifier', 'kms', PAIR, bytes.fromhex('308207b4300d06096086480165030403120500038207a100') + ml_pub_raw, 'KEY_FORMAT', 'RFC 9881: parameters absent'),
        keyv('K-26', 'kms hybrid: nonzero unused-bits octet', 'kms', PAIR, MLDSA65_SPKI[:-1] + b'\x01' + ml_pub_raw, 'KEY_FORMAT', 'zero unused bits'),
        keyv('K-27', 'kms hybrid: ML-DSA-44 OID with ML-DSA-65 length', 'kms', PAIR, MLDSA65_SPKI[:14] + b'\x11' + MLDSA65_SPKI[15:] + ml_pub_raw, 'KEY_FORMAT', 'id-ml-dsa-65 only'),
        keyv('K-28', 'kms hybrid: ML-DSA-44 SPKI', 'kms', PAIR, mldsa.MLDSA44PrivateKey.from_seed_bytes(MLDSA_SEED).public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo), 'KEY_FORMAT', 'parameter set fixed'),
        keyv('K-29', 'kms hybrid: ML-DSA-87 SPKI', 'kms', PAIR, mldsa.MLDSA87PrivateKey.from_seed_bytes(MLDSA_SEED).public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo), 'KEY_FORMAT', 'parameter set fixed'),
        keyv('K-30', 'kms hybrid: P-256 SPKI', 'kms', PAIR, KMS_P256_KEY, 'KEY_FORMAT', 'slot rule under the pair id'),
        keyv('K-31', 'kms hybrid: non-minimal DER outer length (0x83)', 'kms', PAIR, bytes.fromhex('30830007b2300b0609608648016503040312038207a100') + ml_pub_raw, 'KEY_FORMAT', 'DER, exact bytes'),
        keyv('K-32', 'kms hybrid: truncated by one byte', 'kms', PAIR, ml_spki[:-1], 'KEY_FORMAT', 'exact length 1974'),
        keyv('K-33', 'kms hybrid: trailing byte', 'kms', PAIR, ml_spki + b'\x00', 'KEY_FORMAT', 'exact length 1974'),
        keyv('K-35', 'gpg: canonical point with small y (positive control for K-36)', 'gpg', PAIR, gpg_packet(pt65(*small_y)), 'ACCEPT', 'on-curve, coordinates < p'),
        keyv('K-36', 'gpg: non-canonical y (y + p, same residue as K-35)', 'gpg', PAIR, gpg_packet(pt65(small_y[0], small_y[1] + p256.P)), 'KEY_FORMAT', 'coordinates must be in [0, p-1]'),
        keyv('K-37', 'kms fallback: non-canonical y (y + p)', 'kms', ALG, spki_p256(pt65(small_y[0], small_y[1] + p256.P)), 'KEY_FORMAT', 'coordinates < p'),
        keyv('K-34', 'kms hybrid: PEM text', 'kms', PAIR, ml_priv.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo), 'KEY_FORMAT', 'DER only'),
    ]
    return v, {'x0': x0}


def build_f4_points():
    gx, gy = xy(gpg_priv)
    # (1, 0) has order 2 on E': y^2 = x^3 - 3x + 2 (y = 0), and is not on P-256.
    assert p256.on_curve((1, 0), b=2) and not p256.on_curve((1, 0))
    # A point on another short-Weierstrass curve with a = -3, b = 7 (invalid-curve attack input).
    xb = next(x for x in range(1, 1000) if p256.lift_x(x, b=7))
    ib = p256.lift_x(xb, b=7); assert not p256.on_curve(ib)
    v = [
        keyv('L-01', 'gpg: point at infinity as 04 || 0^64 (the encoding some libraries use for O)', 'gpg', PAIR, gpg_packet(pt65(0, 0)), 'KEY_FORMAT', 'finite point required; (0,0) is not on P-256'),
        keyv('L-02', 'gpg: point at infinity as the single octet 00 in place of the point', 'gpg', PAIR, gpg_packet(b'\x00'), 'KEY_FORMAT', 'SEC1 infinity encoding'),
        keyv('L-03', 'gpg: order-2 point (1, 0) of y^2 = x^3 - 3x + 2 (invalid-curve, small order)', 'gpg', PAIR, gpg_packet(pt65(1, 0)), 'KEY_FORMAT', 'on-curve check excludes invalid-curve points'),
        keyv('L-04', 'gpg: point of y^2 = x^3 - 3x + 7 (invalid curve)', 'gpg', PAIR, gpg_packet(pt65(*ib)), 'KEY_FORMAT', 'on-curve check'),
        keyv('L-05', 'gpg: negated key (x, p - y) (positive control: a valid, different key)', 'gpg', PAIR, gpg_packet(pt65(gx, p256.P - gy)), 'ACCEPT', 'h = 1: every finite on-curve point has order n'),
        keyv('L-06', 'kms fallback: point at infinity 04 || 0^64', 'kms', ALG, spki_p256(pt65(0, 0)), 'KEY_FORMAT', 'finite point required'),
        keyv('L-07', 'kms fallback: order-2 invalid-curve point (1, 0)', 'kms', ALG, spki_p256(pt65(1, 0)), 'KEY_FORMAT', 'on-curve check'),
        keyv('L-08', 'kms fallback: SPKI with a 1-byte BIT STRING holding 00 (infinity)', 'kms', ALG, bytes.fromhex('3019301306072a8648ce3d020106082a8648ce3d030107030200') + b'\x00', 'KEY_FORMAT', 'exact 91-byte encoding'),
    ]
    return v


def build_dsks():
    """Function-level key substitution: a different P-256 key, computed from (F, S) alone, under which the honest
    rule-O signature verifies. The vector records the substitute key; the test shows signature_verifies accepts it,
    i.e. the verification equation does not bind the issuer (P3's premise), and the bundle-level test shows the
    fingerprint binding rejects it (KEY_MISMATCH)."""
    h, d, r, s = rule_o(gpg_priv, DOC)
    good = packet(h, d[:2], mpi(r), mpi(s))
    cands = p256.dsks_keys(int.from_bytes(d, 'big'), r, s)
    honest = xy(gpg_priv)
    assert honest in cands
    sub = next(c for c in cands if c != honest)
    return [sigv('D-01', 'honest rule-O signature (positive control)', 'gpg', PAIR, 'gpg', good, 'ACCEPT', 'baseline'),
            {**sigv('D-02', 'same signature under a substitute key computed from (F, S) alone', 'gpg', PAIR, 'dsks', good, 'ACCEPT',
                    'ECDSA has no exclusive ownership: Q\' = r^-1(s(-R) - eG). Acceptance here is the expected library/equation behaviour; issuer binding must come from the signed key_fp (P3 [model]) and the 5.2 fingerprint check')},
            ], gpg_packet(pt65(*sub))


def main():
    OUT.mkdir(exist_ok=True)
    meta = {'generated_with': {'cryptography': cryptography.__version__, 'openssl': backend.openssl_version_text(),
                               'python': sys.version.split()[0]},
            'generator': 'formal/p3-verification-profile/gen_vectors.py'}
    m = mldsa_variants()
    dsks_vectors, dsks_key = build_dsks()
    keys = dict(KEYS); keys['dsks'] = {'slot': 'gpg', 'alg': PAIR, 'hex': hx(dsks_key)}
    write('F2-signature-encodings.json', {**meta, 'field': 'F2 accepted signature encodings and rule-O policy', 'kind': 'sig',
          'keys': keys, 'documents': DOCS, 'vectors': build_f2_rule_o() + build_f2_policy() + build_f2_rule_r(m)})
    f3, info = build_f3_keys()
    write('F3-public-key-validation.json', {**meta, 'field': 'F3 public-key validation', 'kind': 'key', 'vectors': f3})
    write('F4-low-order-points.json', {**meta, 'field': 'F4 low-order / invalid-curve points (translated)', 'kind': 'key',
          'vectors': build_f4_points()})
    f5 = build_f5(m) + dsks_vectors  # fills EXTRA_KEYS before the keys map is written
    write('F5-equation-variant.json', {**meta, 'field': 'F5 verification equation / message-representative variant (translated)',
          'kind': 'sig', 'keys': {**keys, **EXTRA_KEYS}, 'documents': DOCS, 'vectors': f5})
    print('wrote', sorted(p.name for p in OUT.iterdir()))


if __name__ == '__main__':
    main()
