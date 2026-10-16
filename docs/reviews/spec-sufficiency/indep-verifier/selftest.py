"""Locally constructed falsification probes; no project fixtures or code read."""
import datetime as dt
import hashlib
import unittest

import verifier as v


def wrap(tag, body):
    return bytes([len(tag)]) + tag + b"\x00\x01" + len(body).to_bytes(4, "big") + body


def frame(tag, value):
    return wrap(tag, v.jcs_without_numbers(value))


def objects(alg=v.CLASSICAL, sig=None):
    manifest = {"alg": alg, "issuer": "wamason.com", "key_fp": "spki-sha256:" + "a" * 64,
                "sset": ["gpg-sha256:" + "b" * 64], "ver": "map-v1"}
    m = frame(v.MANIFEST, manifest)
    common = {"alg": alg, "binding_forms": ["STMT_DIRECT"], "content": "probe only",
              "declared_issue_time": "2026-10-13T00:00:00Z", "issuer": "wamason.com",
              "manifest_sha256": hashlib.sha256(m).hexdigest(), "preamble_sha256": "c" * 64,
              "profile": v.PROFILE, "spec": {"id": v.PROFILE + "/verification-spec/1", "sha256": "d" * 64},
              "vectors_sha256": "e" * 64}
    frames = [frame(v.ATTEST, {"common": common, "signer": {"key_fp": fp}})
              for fp in (manifest["key_fp"], manifest["sset"][0])]
    # MPI r=s=1 is merely structural: no mathematical signature claim.
    if sig is None:
        body = bytes.fromhex("04001308000000000000000101000101")
        sig = bytes([0x88, len(body)]) + body
    a = bytes([len(v.ANCHOR)]) + v.ANCHOR + b"\x02"
    for f in frames:
        a += len(f).to_bytes(4, "big") + f + len(sig).to_bytes(4, "big") + sig
    return m, a


class ProbeTests(unittest.TestCase):
    def rejects(self, reason, func, *args):
        with self.assertRaises(v.Reject) as caught:
            func(*args)
        self.assertEqual(str(caught.exception), reason)

    def test_structural_receipt_and_swap(self):
        m, a = objects()
        slots = v.anchor(a)
        self.assertEqual(v.receipt_consistency(m, slots)["issuer"], "wamason.com")
        self.rejects("RECEIPT_SLOT", v.receipt_consistency, m, slots[::-1])

    def test_no_signature_normalization(self):
        _, a = objects()
        _, changed = objects(sig=bytes.fromhex("881004001308000000000000000101000202"))
        v.anchor(changed)
        self.assertNotEqual(hashlib.sha256(a).digest(), hashlib.sha256(changed).digest())

    def test_unknown_alg_is_opaque_not_valid(self):
        m, a = objects("FUTURE", b"opaque")
        self.assertEqual(v.receipt_consistency(m, v.anchor(a))["alg"], "FUTURE")
        self.assertIsNone(v.report("STOPPED", "unknown algorithm")["v1_verdict"])

    def test_boundaries_and_withdrawn_tag(self):
        _, a = objects()
        self.rejects("TRAILING", v.anchor, a + b"x")
        self.rejects("TRUNCATED", v.anchor, a[:-1])
        old = b"tessera-v1/receipt-anchor"
        self.rejects("TAG_UNKNOWN", v.anchor, bytes([len(old)]) + old)

    def test_payload_categories(self):
        self.rejects("JSON_ENCODING", v.payload, b'"\xff"')
        self.rejects("JSON_SYNTAX", v.payload, b'{"x":NaN}')
        self.rejects("JSON_DUPLICATE_NAME", v.payload, b'{"x":null,"\\u0078":true}')
        self.rejects("JSON_STRING", v.payload, b'"\\ud800"')
        self.rejects("JSON_STRING", v.payload, '"e\u0301"'.encode())
        self.rejects("JSON_NONCANONICAL", v.payload, b'{"z":true,"a":null}')
        self.rejects("JSON_DEPTH", v.payload, b"[" * 65 + b"null" + b"]" * 65)
        self.assertIsInstance(v.payload(b"[" * 64 + b"null" + b"]" * 64), list)

    def test_number_is_a_stop_not_a_rejection(self):
        with self.assertRaises(v.Stop):
            v.payload(b"9.8")

    def test_subpacket_encoding_is_a_stop(self):
        body = bytes.fromhex("040013080002010000000000000101000101")
        with self.assertRaises(v.Stop) as caught:
            v.signature(bytes([0x88, len(body)]) + body, v.CLASSICAL)
        self.assertEqual(str(caught.exception), "OPENPGP_SUBPACKET_LENGTH_ENCODING_REQUIRED")

    def test_utf16_order(self):
        value = {"\ue000": None, "\U0001f600": True}
        raw = '{"\U0001f600":true,"\ue000":null}'.encode()
        self.assertEqual(v.jcs_without_numbers(value), raw)
        self.assertEqual(v.payload(raw), value)

    def test_window_inclusive_and_no_T_lower_bound(self):
        before, after = "2026-10-13T00:00:00Z", "2027-01-11T00:00:00Z"
        v.issuance_window(before, after, before, v.utc(after))
        v.issuance_window(before, after, before, v.utc(before) - dt.timedelta(seconds=1))
        self.rejects("ISSUANCE_WINDOW", v.issuance_window, before, after, before,
                     v.utc(after) + dt.timedelta(seconds=1))
        self.rejects("DNS_WINDOW_LENGTH", v.issuance_window, before, "2027-01-11T00:00:01Z", before, v.utc(before))


if __name__ == "__main__":
    unittest.main(verbosity=2)
