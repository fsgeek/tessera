"""Regression tests for implementation B (check.py) from the P8 falsification review.

prototype/p8-falsify/REPORT.md, findings P8F-02 (oversized exponents crashed B), P8F-03 (B reported a BOM before
invalid UTF-8) and P8F-04 (B's standalone payload helper had no size cap), and the same three in implementation A (gen.py).
Disposition:
docs/reviews/p8-falsification/DISPOSITION.md.

Run: prototype/.venv/bin/python -B -m unittest discover -s formal/p8/vectors -p 'test_*.py'
"""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check as B  # noqa: E402


class CheckRegressions(unittest.TestCase):
    def code(self, code, fn, *args):
        with self.assertRaises(B.Bad) as cm:
            fn(*args)
        self.assertEqual(cm.exception.code, code)

    # P8F-02: E§1.2 accepts arbitrary-exponent zero and value-preserving spellings of any length.
    def test_oversized_exponents(self):
        self.assertEqual(B.ingest(b"0e" + b"9" * 4300), 0.0)
        self.assertEqual(B.ingest(b"0e" + b"9" * 4301), 0.0)
        self.assertEqual(B.ingest(b"0e" + b"0" * 4301), 0.0)
        self.assertEqual(B.ingest(b"1e" + b"0" * 4301), 1.0)
        self.assertEqual(B.ingest(b"1e-" + b"0" * 4301), 1.0)
        self.assertEqual(B.ingest(b"0e-" + b"9" * 5000), 0.0)
        self.code("JSON_NUMBER", B.ingest, b"1e" + b"9" * 4301)       # overflow
        self.code("JSON_NUMBER", B.ingest, b"1e-" + b"9" * 4301)      # nonzero, rounds to 0
        self.code("JSON_NUMBER", B.ingest, b"-0e" + b"9" * 4301)      # negative zero
        self.code("JSON_NONCANONICAL", B.payload_value, b"0e" + b"9" * 4301)
        # The exponent clamp must not disturb ordinary literals.
        for lit, want in [(b"9.80", 9.8), (b"1E2", 100.0), (b"5e-324", 5e-324), (b"1e21", 1e21),
                          (b"0e99999999999999999999", 0.0), (b"123456789012345680000", 123456789012345680000.0)]:
            self.assertEqual(B.ingest(lit), want)
        self.code("JSON_NUMBER", B.ingest, b"1e400")
        self.code("JSON_NUMBER", B.ingest, b"1e-400")

    # P8F-03: E§1.4 checks strict UTF-8 over the whole input before JSON syntax, so a BOM followed by invalid
    # UTF-8 is JSON_ENCODING, through ingest, payload and the frame decoder.
    def test_encoding_before_bom(self):
        self.code("JSON_ENCODING", B.ingest, b"\xef\xbb\xbf\xff")
        self.code("JSON_ENCODING", B.payload_value, b"\xef\xbb\xbf\xff")
        self.code("JSON_SYNTAX", B.ingest, b"\xef\xbb\xbf{}")
        golden = {v["id"]: v for v in json.loads((HERE / "golden.json").read_text())["vectors"]}
        f0 = bytes.fromhex(golden["F-01"]["bytes_hex"])
        p = b"\xef\xbb\xbf" + B.jcs(B.frame_decode(f0, "attest")) + b"\xff"
        fr = bytes([17]) + b"tessera-v1/attest" + b"\x00\x01" + len(p).to_bytes(4, "big") + p
        self.code("JSON_ENCODING", B.frame_decode, fr, "attest")

    # P8F-04: payload(bytes) accepts at most 2^24 bytes (E§1.1), with LENGTH_CAP as through the frame.
    def test_standalone_payload_cap(self):
        at_cap = b'"' + b"a" * (B.CAP - 2) + b'"'
        self.assertEqual(len(B.payload_value(at_cap)), B.CAP - 2)
        over = b'"' + b"a" * (B.CAP - 1) + b'"'
        self.assertEqual(len(over), B.CAP + 1)
        self.code("LENGTH_CAP", B.payload_value, over)


try:
    import rfc8785  # noqa: F401
    import gen as A
except ImportError:  # implementation A needs rfc8785 0.1.4
    A = None


@unittest.skipIf(A is None, "rfc8785 not installed")
class GenRegressions(unittest.TestCase):
    """The same three reproductions against implementation A (gen.py), which had the same defects."""
    def code(self, code, fn, *args):
        with self.assertRaises(A.Reject) as cm:
            fn(*args)
        self.assertEqual(cm.exception.code, code)

    def test_oversized_exponents(self):
        self.assertEqual(A.ingest(b"0e" + b"9" * 4301), 0.0)
        self.assertEqual(A.ingest(b"1e" + b"0" * 4301), 1.0)
        self.assertEqual(A.ingest(b"1" + b"0" * 200000 + b"e-200000"), 1.0)
        self.code("JSON_NUMBER", A.ingest, b"1e" + b"9" * 4301)
        self.code("JSON_NUMBER", A.ingest, b"-0e" + b"9" * 4301)

    def test_encoding_before_bom(self):
        self.code("JSON_ENCODING", A.ingest, b"\xef\xbb\xbf\xff")
        self.code("JSON_SYNTAX", A.ingest, b"\xef\xbb\xbf{}")

    def test_standalone_payload_cap(self):
        self.code("LENGTH_CAP", A.decode_payload, b'"' + b"a" * (A.MAX_PAYLOAD - 1) + b'"')


if __name__ == "__main__":
    unittest.main()
