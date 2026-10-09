"""Phase 3 tests: real mechanisms in place of the stubs (THROWAWAY). Each test pins an observation
PHASE3-REPORT.md relies on. No network: DNS and Bitcoin data come from fixtures captured 2026-10-07.
gpg tests use a throwaway GNUPGHOME under prototype/.gnupg-phase3/ and skip if /usr/bin/gpg is absent."""
import base64
import copy
import hashlib
import json
import struct

import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from consumers import examiner as E
from consumers import relying_party as R
from consumers import scenarios
from consumers.submitter import Submitter, acme_release, make_sbom
from tessera_proto import frame, jcs
from tessera_proto.real import btc, canonical, dnssec, gitchannel, kms, ots, pairings, rerun
from tessera_proto.real import gpg as G
from tessera_proto.real import openpgp as P
from tessera_proto.real import world as RW
from tessera_proto.verifier import verify_bundle
from tessera_proto.world import T0

FX = "tessera_proto/real/fixtures/"
needs_gpg = pytest.mark.skipif(not G.available(), reason="/usr/bin/gpg not installed")
FB = frame.encode("OT_ATTEST", 1, b'{"common":{"x":"y"},"signer":{"key_fp":"z"}}')


@pytest.fixture(scope="module")
def home():
    h = G.GpgHome()
    yield h
    h.close()


@pytest.fixture(scope="module")
def real():
    old = jcs.NUMBER_RULE
    try:
        yield scenarios.build("real")
    finally:
        RW.close()
        jcs.NUMBER_RULE = old


@pytest.fixture(scope="module")
def runs(real):
    rp, results, rev = R.run_all(real)
    by = {(r.case, r.policy): r for r in results}
    for k, case in rerun.extra_cases(real).items():
        by[(k, "strict")] = rp.run(case, "strict")
    return rp, by, rev


# ------------------------------------------------------------------ 1. canonical form

def test_rfc8785_appendix_b_numbers_match_prototype_and_reference_package():
    for bits, want, mine, ref in canonical.appendix_b_results():
        assert ref == want, bits
        if bits != "8000000000000000":
            assert mine == want, bits


def test_precision_rule_readings_disagree_on_real_inputs():
    c = canonical.classify(canonical.PROBE_LITERALS)
    assert c["9.8"]["literal"].startswith("REJECT") and c["9.8"]["value-preserving"] == "9.8"
    assert c["9.8"]["rfc8785-package"] == "9.8"
    # the reference package silently changes a value the value-preserving reading refuses
    assert c["333333333.33333329"]["rfc8785-package"] == "333333333.3333333"
    assert c["333333333.33333329"]["value-preserving"].startswith("REJECT")
    # and refuses an integer that IS exactly a double's shortest form
    assert c["123456789012345680000"]["rfc8785-package"].startswith("REJECT")
    assert c["123456789012345680000"]["value-preserving"] == "123456789012345680000"
    # RFC 8785 itself has a vector for 5e-324; phase 1's literal reading refuses it as input
    assert c["5e-324"]["literal"].startswith("REJECT") and c["5e-324"]["value-preserving"] == "5e-324"
    # -0: JCS writes "0"; Tessera's R-3.4 refuses it under every reading (a rule on top of JCS)
    assert c["-0"]["rfc8785-package"] == "0" and all(c["-0"][r].startswith("REJECT") for r in canonical.RULES)


def test_cvss_sbom_accepted_under_value_preserving_reading():
    sbom = make_sbom("x", "1", "00" * 32)
    with pytest.raises(jcs.CanonicalizationRejected):
        jcs.canonicalize_text(sbom)                              # phase-1 literal reading (G-03)
    with canonical.number_rule("value-preserving"):
        out = jcs.canonicalize_text(sbom)
        assert b'"score":9.8' in out and jcs.is_canonical(out)
    assert jcs.NUMBER_RULE == "literal"


# ------------------------------------------------------------------ 2. signatures

def test_kms_raw_and_digest_both_verify_over_the_frame_but_kms_sees_only_a_digest():
    k = kms.KmsSlotKey.generate("A")
    big = FB + b"x" * 5000
    for msg in (FB, big):
        assert kms.verify_spki(kms.ALG_ECDSA, k.pub_raw, k.sign(msg), msg)
    assert [c["type"] for c in k.kms.calls] == ["RAW", "DIGEST"]
    assert k.kms.calls[1]["saw"] == hashlib.sha256(big).digest()      # the custodian never saw the frame
    with pytest.raises(kms.KmsValidationException):
        k.kms.sign(big, "RAW", "ECDSA_SHA_256")
    r = kms.KmsSlotKey.generate("R", alg=kms.ALG_RSAPSS)
    s1, s2 = r.sign(FB), r.sign(FB)
    assert s1 != s2 and kms.verify_spki(kms.ALG_RSAPSS, r.pub_raw, s1, FB)   # PSS is randomized


def test_ecdsa_is_malleable_ed25519_is_not():
    k = kms.KmsSlotKey.generate("A")
    s = k.sign(FB)
    s2 = kms.ecdsa_malleate(s)
    assert s2 != s and kms.verify_spki(kms.ALG_ECDSA, k.pub_raw, s2, FB)
    sk = Ed25519PrivateKey.generate()
    sig = sk.sign(FB)
    L = 2**252 + 27742317777372353535851937790883648493
    bad = sig[:32] + ((int.from_bytes(sig[32:], "little") + L).to_bytes(32, "little"))
    with pytest.raises(InvalidSignature):
        sk.public_key().verify(bad, FB)


@needs_gpg
def test_openpgp_signs_frame_plus_trailer_not_the_frame(home):
    kp = G.GpgSlotKey.generate("B", home)
    s = P.parse_signature(kp.sign(FB))
    pub = P.first_public_key(kp.pub_raw).crypto_key()
    der = utils.encode_dss_signature(*s.mpis)
    with pytest.raises(InvalidSignature):
        pub.verify(der, FB, ec.ECDSA(hashes.SHA256()))
    pub.verify(der, FB + s.trailer(), ec.ECDSA(hashes.SHA256()))
    assert s.signed_message(FB)[:len(FB)] == FB and len(s.trailer()) > 6
    assert s.creation_time and s.issuer_fpr                          # signed metadata outside the frame
    assert home.verify(s.raw, FB)[0]


@needs_gpg
def test_openpgp_ed25519_signs_the_digest_bytes(home):
    ke = G.GpgSlotKey.generate("E", home, G.ALG_PGP_ED25519)
    s = P.parse_signature(ke.sign(FB))
    pub = P.first_public_key(ke.pub_raw).crypto_key()
    rs = s.mpis[0].to_bytes(32, "big") + s.mpis[1].to_bytes(32, "big")
    for m in (FB, s.signed_message(FB)):
        with pytest.raises(InvalidSignature):
            pub.verify(rs, m)
    pub.verify(rs, s.digest(FB))


@needs_gpg
def test_openpgp_signature_bytes_are_third_party_malleable(home):
    kp = G.GpgSlotKey.generate("M", home)
    s = P.parse_signature(kp.sign(FB))
    k = P.first_public_key(kp.pub_raw)
    m1 = s.with_unhashed(s.unhashed_area + P.subpacket(20, b"\x80\0\0\0\0\x01\0\x01ab"))
    m2 = s.with_mpis([s.mpis[0], kms.P256_N - s.mpis[1]])
    for m in (m1, m2):
        assert m.raw != s.raw and P.verify(m, k, FB) and home.verify(m.raw, FB)[0]


@needs_gpg
def test_kms_backed_openpgp_key_and_signature_accepted_by_gpg(home):
    kq = G.KmsOpenPGPSlotKey.generate("A")
    assert home.import_key(kq.transferable("Tessera proto A <a@proto.invalid>")).returncode == 0
    sig = kq.sign(FB)
    assert home.verify(sig, FB)[0] and G.verify_openpgp_slot(G.ALG_PGP_P256, kq.pub_raw, sig, FB)
    assert kq.kms.calls[-1]["type"] == "DIGEST"


@needs_gpg
def test_same_algorithm_rule_blocks_natural_kms_gpg_pairings(home):
    old = jcs.NUMBER_RULE
    w = RW.make_world_real()
    try:
        res = {}
        for name, keys in pairings.pairings(home).items():
            b = pairings.build_pair_layer(w, keys, {"x": "y"}, T0, per_slot_alg=True)
            res[name[:2]] = verify_bundle(b, w.trust(), evaluate_standing=False)["layers"][0]
        assert res["P1"]["verification"] == "INVALID" and "V13[B]" in res["P1"]["failed"]
        assert res["P2"]["verification"] == "INVALID" and "V13[B]" in res["P2"]["failed"]
        assert res["P3"]["verification"] == "VALID_STRICT"
        assert res["P4"]["verification"] == "VALID_STRICT"
        # P3's GPG-held signature is raw DER ECDSA, not an OpenPGP packet: nothing gpg can verify
        agent = pairings.GpgAgentSlotKey.generate("ag", home)
        raw = agent.sign(FB)
        with pytest.raises(Exception):
            P.parse_signature(raw)
        assert not home.verify(raw, FB)[0]
    finally:
        jcs.NUMBER_RULE = old


# ------------------------------------------------------------------ 3. OpenTimestamps

@pytest.mark.parametrize("name,hf,heights", [
    ("commit-03cd3db.txt", "btc_headers_956576_956644.json", [956582, 956586, 956620, 956639]),
    ("commit-fcaa11b.txt", "btc_headers_959013_959094.json", [959013, 959015, 959052, 959089]),
])
def test_real_ots_proof_against_archived_mainnet_headers(name, hf, heights):
    hs = btc.load_mainnet(hf)
    assert btc.check_segment(hs, min(hs), max(hs)) == (True, "")        # real PoW, real linkage
    c = ots.check(ots.load(open(FX + name + ".ots", "rb").read()), open(FX + name, "rb").read(), hs)
    assert c.file_digest_ok
    assert sorted(b["height"] for b in c.verified()) == heights        # FOUR anchors in one proof
    assert len({b["txids"][-1] for b in c.bitcoin}) == 4                # four different transactions
    times = sorted(b["time"] for b in c.verified())
    assert times[-1] - times[0] > 8 * 3600                             # anchor_time is not one number
    assert len(c.pending) == 4                                         # pending attestations stay in the file
    # the file stamped is the commit id as hex text: the anchor reaches git content only via SHA-1
    assert open(FX + name, "rb").read().strip().decode() == gitchannel.git("rev-parse", name[7:14]).decode().strip()


def test_ots_proof_carries_no_time_no_depth_and_needs_external_headers():
    hs = btc.load_mainnet("btc_headers_956576_956644.json")
    dtf = ots.load(open(FX + "commit-03cd3db.txt.ots", "rb").read())
    assert ots.check(dtf, open(FX + "commit-03cd3db.txt", "rb").read(), {}).verified() == []
    forged = dict(hs)
    h = hs[956582]
    forged[956582] = btc.Header(h.version, h.prev, b"\x00" * 32, h.time, h.bits, h.nonce)
    c = ots.check(dtf, open(FX + "commit-03cd3db.txt", "rb").read(), forged)
    assert 956582 not in [b["height"] for b in c.verified()]
    assert not forged[956582].pow_ok()                                 # and PoW catches the forged header
    assert btc.UINT32_MAX_TIME == 4294967295                           # nTime ends 2106-02-07


def test_two_frames_one_calendar_round_gives_two_proofs_with_one_commitment():
    from opentimestamps.core.op import OpSHA256
    from opentimestamps.core.timestamp import DetachedTimestampFile, Timestamp, make_merkle_tree
    a, b = (DetachedTimestampFile(OpSHA256(), Timestamp(hashlib.sha256(x).digest())) for x in (b"frameA", b"frameB"))
    root = make_merkle_tree([a.timestamp, b.timestamp])
    tips = [ots.attestation_paths(x.timestamp) for x in (a, b)]
    assert a.file_digest != b.file_digest and root.msg is not None and tips == [[], []]
    assert all(any(t.msg == root.msg for t in _walk(x.timestamp)) for x in (a, b))


def _walk(ts):
    yield ts
    for c in ts.ops.values():
        yield from _walk(c)


# ------------------------------------------------------------------ verifier stage (h) on OTS

def _anchor(bundle):
    return bundle["layers"][0]["anchor"]


def test_real_anchor_verifies_and_reports_every_attestation(real):
    b = real.cases["a"].bundle
    a = _anchor(b)
    assert a["format"] == "ots-bitcoin" and a["network"] == "regtest"
    L = verify_bundle(b, real.trust())["layers"][0]
    assert L["verification"] == "VALID_STRICT"
    for cid in ("V33a", "V33", "V34", "V35", "V36", "V37", "V38"):
        assert L["checks"][cid]["status"] == "pass", cid


def test_real_anchor_failure_modes(real):
    b = real.cases["a"].bundle
    tr = real.trust()
    pend = copy.deepcopy(b)
    from opentimestamps.core.op import OpSHA256
    from opentimestamps.core.timestamp import DetachedTimestampFile, Timestamp
    from opentimestamps.core.notary import PendingAttestation
    dtf = ots.load(base64.b64decode(_anchor(b)["ots_b64"]))
    p = DetachedTimestampFile(OpSHA256(), Timestamp(dtf.file_digest))
    p.timestamp.attestations.add(PendingAttestation("https://cal.invalid"))
    _anchor(pend)["ots_b64"] = base64.b64encode(ots.dump(p)).decode()
    L = verify_bundle(pend, tr)["layers"][0]
    assert L["verification"] == "UNVERIFIABLE" and L["checks"]["V33a"]["reason"] == "ANCHOR_PENDING_ONLY"
    other = copy.deepcopy(b)
    _anchor(other)["ots_b64"] = _anchor(real.cases["f"].bundle)["ots_b64"]
    assert verify_bundle(other, tr)["layers"][0]["checks"]["V33a"]["reason"] == "ANCHOR_NOT_OVER_THIS_RECEIPT"
    wrongtx = copy.deepcopy(b)
    _anchor(wrongtx)["txid"] = "00" * 32
    assert verify_bundle(wrongtx, tr)["layers"][0]["checks"]["V33a"]["reason"] == "TXID_NOT_ON_ATTESTATION_PATH"


def test_header_store_policy_decides_the_submitters_self_check(real):
    r = rerun.submitter_self_checks(real)
    assert r["stale/pin-every-header"][0] == "UNVERIFIABLE"
    assert r["stale/checkpoint+pow"] == ("VALID_STRICT", [], "EXTENDED_BY_POW_FROM_PINNED_HEADER")


# ------------------------------------------------------------------ 4. authority channels

def test_wamason_com_has_no_dnssec_today():
    r = dnssec.validate_offline(dnssec.load("dnssec_wamason.com_TXT.json"), 1791400000)
    assert r["status"] == "INSECURE" and r["insecure_at"] == "wamason.com."


def test_root_anchor_authenticates_any_name_and_rrsig_windows_expire():
    fx = dnssec.load("dnssec_ietf.org_TXT.json")
    lo, hi = dnssec.common_window(fx)
    r = dnssec.validate_offline(fx, (lo + hi) / 2)
    assert r["status"] == "SECURE" and r["owner"] == "ietf.org."       # validated by the ROOT key alone
    assert hi - lo < 3 * 86400                                          # the whole chain is valid together < 3 days
    assert dnssec.validate_offline(fx, hi + 1)["status"] == "BOGUS"
    assert dnssec.validate_offline(fx, 4_291_000_000)["status"] == "BOGUS"   # a 2106 clock


def test_git_commit_signature_covers_commit_minus_gpgsig_and_ids_are_sha1():
    ev = gitchannel.collect("03cd3db06d4261ace0c8e8c9f18dcdb34d78e8a9", "docs/phase-0-prereg-amendment-1.md")
    r = gitchannel.verify_offline(ev, open(FX + "tyst-commit-signing-key.pub.gpg", "rb").read())
    assert r["signature_ok"] and r["object_ids_ok"] and r["tree_link_ok"]
    assert r["sig_creation_time"] == r["committer_time"]               # both self-asserted by the signer
    key = P.first_public_key(open(FX + "tyst-commit-signing-key.pub.gpg", "rb").read())
    assert not P.verify(ev.signature, key, ev.commit_raw)               # the id covers the sig; the sig does not cover the id
    assert len(ev.commit_id) == 40 and hashlib.sha1(b"commit %d\0" % len(ev.commit_raw) + ev.commit_raw).hexdigest() == ev.commit_id


# ------------------------------------------------------------------ 5. consumers on the de-stubbed path

STUB_MATRIX = {  # (case, policy) -> (naive outcome, careful outcome), from PHASE2-REPORT
    ("a", "strict"): ("correct", "correct"), ("g", "strict"): ("correct", "false reject (safe, costly)"),
    ("c", "degraded"): ("UNSAFE ACCEPT", "correct"), ("d3", "degraded"): ("UNSAFE ACCEPT", "UNSAFE ACCEPT"),
    ("e", "strict"): ("UNSAFE ACCEPT", "UNSAFE ACCEPT"), ("f", "strict"): ("UNSAFE ACCEPT", "UNSAFE ACCEPT"),
    ("h", "strict"): ("correct", "false reject (safe, costly)"), ("b", "strict"): ("correct", "correct"),
    ("d2", "strict"): ("false reject (safe, costly)", "false reject (safe, costly)"),
}


def test_relying_party_matrix_unchanged_on_real_mechanisms(runs):
    _, by, rev = runs
    for key, (n, c) in STUB_MATRIX.items():
        r = by[key]
        assert (r.outcome(r.naive), r.outcome(r.careful)) == (n, c), key
    assert rev["verdict_as_reported"] == "VALID_STRICT"


def test_malleated_signatures_turn_established_into_absent(runs):
    _, by, _ = runs
    assert by[("a", "strict")].layers[0][:2] == ("VALID_STRICT", "ESTABLISHED")
    for k in ("m1", "m2", "m3"):
        r = by[(k, "strict")]
        assert r.layers[0] == ("VALID_STRICT", "ABSENT", "STANDING_EVIDENCE_MISMATCH"), k
        assert r.outcome(r.careful) == "false reject (safe, costly)"


def test_attack_pairs_reproduce_on_real_signatures(real):
    r = rerun.replay_pairs(real)
    assert r["C-C2"][0] == "INVALID" and set(r["C-C2"][1]) == {"V17[A]", "V17[B]", "V18[A]", "V18[B]"}
    assert r["C-C2"][2].startswith("VALID_DEGRADED") and r["C-C2"][3]
    assert r["C-C5"][0] == "INVALID" and r["C-C5"][1] == ["V19[A]"]
    assert r["C-C5"][2].startswith("VALID_DEGRADED") and r["C-C5"][3]


def test_submitter_inline_sbom_now_accepted(real):
    content = json.loads(real.honest_payload)
    assert content["sbom"]["vulnerabilities"][0]["ratings"][0]["score"] == 9.8


def test_examiner_blockers_move(real):
    store = E.archived_store(real.world)
    ex = E.examine(real.cases["a"].bundle, store)
    blocked = {s.name for s in ex.blocked()}
    assert "anchor proof path to the block" not in blocked             # a standard format can be followed
    assert {"slot A: payload canonical + signature over the frame", "possession proofs"} <= blocked
    full = E.examine(real.cases["a"].bundle, store, E.complete_spec_supplement(real.world))
    assert [s.name for s in full.blocked()] == ["revocation time-relativity (R-5.21)"]
    assert "OpenTimestamps proof format" in full.unlisted
