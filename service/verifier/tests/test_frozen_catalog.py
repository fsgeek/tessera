"""The frozen catalog and spec identifiers are test FIXTURES here (read from formal/freeze-v1/objects/); the package
never reads that directory. The verifier must accept the frozen catalog bytes as they are, and read Delta and m
from them."""
import hashlib
import json
import unittest
from pathlib import Path
from tessera_verify.codec import jcs
from tessera_verify.policy import parse_catalog
from tessera_verify.verify import utc_assessment

FREEZE = Path(__file__).resolve().parents[3] / 'formal' / 'freeze-v1'
CATALOG = FREEZE / 'objects' / 'catalog.json'
CATALOG_SHA256 = 'aaf4306fed070119022c8486219f5160dc869edaa929f323d962fbb679e27fc2'   # docs: FREEZE-RECORD.md table


class FrozenCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.raw = CATALOG.read_bytes()

    def test_fixture_is_the_recorded_object(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), CATALOG_SHA256)
        self.assertEqual(jcs(json.loads(self.raw)), self.raw)             # it is canonical JCS

    def test_parses_and_carries_delta_and_m(self):
        cat = parse_catalog(self.raw)
        (spec_sha, entry), = cat.items()
        self.assertEqual(spec_sha, json.loads(self.raw)['spec_sha256'])
        self.assertEqual((entry['utc_delta_s'], entry['utc_m'], entry['k']), ('7200', '6', '6'))
        self.assertEqual(entry['alg'], 'KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256')
        self.assertEqual(entry['spec_id'], 'tessera-v1-strict/verification-spec/1')

    def test_assumption_id_is_derived_from_the_catalog(self):
        self.assertEqual(utc_assessment(catalog=parse_catalog(self.raw)), {'assumption_id': 'A-UTC-7200-6', 'utc_upper_bound': None})

    def test_each_frozen_object_hash_matches_the_catalog(self):
        entry = json.loads(self.raw)
        for key, name in (('spec_sha256', 'spec.bin'), ('vectors_sha256', 'vectors.bin'), ('preamble_sha256', 'preamble.bin'),
                          ('dependency_manifest_sha256', 'dependency-manifest.json')):
            self.assertEqual(hashlib.sha256((FREEZE / 'objects' / name).read_bytes()).hexdigest(), entry[key], name)

    def test_fails_closed_on_any_change(self):
        from tessera_verify.codec import Fault
        for mutate in (lambda d: d.pop('utc_delta_s'), lambda d: d.pop('utc_m'), lambda d: d.update(utc_m='5'),
                       lambda d: d.update(spec_id='x'), lambda d: d.update(extra='x'), lambda d: d.update(D='example.com')):
            d = json.loads(self.raw); mutate(d)
            with self.assertRaises(Fault): parse_catalog(jcs(d))
        with self.assertRaises(Fault): parse_catalog(self.raw + b'\n')


if __name__ == '__main__': unittest.main()
