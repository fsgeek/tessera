"""release/release_tool.py (profile 15.9 R1-R5): deterministic build, the author's check, R2 bindings, rule-O and
release-key acceptance, and A10 row 36 (an otherwise correct archive signed only by a TEST key is refused by the
acquisition procedure, including when the TEST public key is offered as the key). Builds from this repository's
HEAD; the gpg cases use throwaway keys in a fresh GNUPGHOME and skip without gpg."""
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parent.parent
spec = importlib.util.spec_from_file_location('release_tool', HERE / 'release' / 'release_tool.py')
rt = importlib.util.module_from_spec(spec); spec.loader.exec_module(rt)
RELEASE_FPR = 'CADC96CF002355F8E83FE97FAFF80961D825035E'
RELEASE_KEY = REPO / 'docs/ceremony/keys/release-CADC96CF002355F8E83FE97FAFF80961D825035E.pub.asc'
VECTORS = REPO / 'service/release-vectors'
GPG = shutil.which('gpg') and shutil.which('gpgv')


class Build(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name, cls.data = rt.build(str(REPO), 'HEAD', 'PRODUCTION', '1')
        cls.parts = rt.parse_archive(cls.data)

    def test_name_and_determinism(self):
        self.assertEqual(self.name, 'tessera-verifier-v1-1.parts')
        self.assertEqual(rt.build(str(REPO), 'HEAD', 'PRODUCTION', '1')[1], self.data)

    def test_round_trip_and_bindings(self):
        self.assertEqual(rt.assemble(self.parts), self.data)
        m, t, cpath = rt.check_bindings(self.parts)
        self.assertEqual((m['namespace'], m['release'], m['release_key_successor']), ('PRODUCTION', '1', None))
        self.assertEqual(m['catalog_sha256'], rt.FROZEN_CATALOG_SHA256)
        self.assertEqual(m['freeze_record_sha256'], rt.FREEZE_RECORD_SHA256)
        self.assertEqual(cpath, 'service/verifier/release/v1-1/release_constants.py')
        self.assertNotIn('service/verifier/tessera_verify/release_constants.py', self.parts)
        self.assertFalse(any(p.startswith(('service/verifier/tests/', 'prototype/')) for p in self.parts))

    def test_author_check_passes(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / self.name; p.write_bytes(self.data)
            rt.check(str(p), str(REPO))

    def test_any_changed_part_or_manifest_is_refused(self):
        for path in ('service/verifier/release/v1-1/trust.json', 'service/verifier/tessera_verify/verify.py',
                     'formal/freeze-v1/objects/catalog.json', 'RELEASE.json'):
            bad = dict(self.parts); bad[path] = bad[path][:-1] + bytes([bad[path][-1] ^ 1])
            with self.assertRaises(rt.Refused, msg=path): rt.check_bindings(bad)

    def test_constants_disagreeing_with_trust_are_refused(self):
        bad = dict(self.parts)
        c = 'service/verifier/release/v1-1/release_constants.py'
        bad[c] = bad[c].replace(b"NAMESPACE = 'PRODUCTION'", b"NAMESPACE = 'TEST'")
        m = json.loads(bad['RELEASE.json']); m['parts'][c] = rt.sha(bad[c]); bad['RELEASE.json'] = rt.jcs(m)
        with self.assertRaises(rt.Refused): rt.check_bindings(bad)

    def test_grammar(self):
        for bad in (self.data + b'\n', self.data[:-1], b'tessera-v1-part ../x 0\n\n', b'tessera-v1-part b 0\n\ntessera-v1-part a 0\n\n'):
            with self.assertRaises(rt.Refused): rt.parse_archive(bad)

    def test_release_key_file(self):
        self.assertTrue(rt.release_key(str(RELEASE_KEY), RELEASE_FPR))
        with self.assertRaises(rt.Refused): rt.release_key(str(RELEASE_KEY), 'A' * 40)


@unittest.skipUnless(GPG, 'gpg and gpgv needed')
class RowThirtySix(unittest.TestCase):
    """The production candidate signed by a throwaway TEST key: refused by key, whatever key file is offered."""
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix='row36-')
        home = os.path.join(cls.tmp, 'gnupg'); os.mkdir(home, 0o700)
        gpg = ['gpg', '--homedir', home, '--batch', '--no-tty', '--pinentry-mode', 'loopback', '--passphrase', '']
        subprocess.run(gpg + ['--quick-generate-key', 'THROWAWAY TEST release key <throwaway@invalid>', 'nistp256', 'sign', 'never'], check=True, capture_output=True)
        out = subprocess.run(gpg + ['--with-colons', '--list-keys'], check=True, capture_output=True, text=True).stdout
        cls.test_fpr = [l.split(':')[9] for l in out.splitlines() if l.startswith('fpr:')][0]
        cls.test_key = os.path.join(cls.tmp, 'test.pub.pgp')
        Path(cls.test_key).write_bytes(subprocess.run(gpg + ['--export', cls.test_fpr], check=True, capture_output=True).stdout)
        name, data = rt.build(str(REPO), 'HEAD', 'PRODUCTION', '1')
        cls.archive = os.path.join(cls.tmp, name); Path(cls.archive).write_bytes(data)
        cls.sig = cls.archive + '.sig'
        subprocess.run(gpg + ['--local-user', cls.test_fpr + '!', '--digest-algo', 'SHA256', '--detach-sign', '--output', cls.sig, cls.archive], check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def refused(self, key, fpr=RELEASE_FPR):
        with self.assertRaises(rt.Refused) as e: rt.verify_sig(self.archive, self.sig, fpr, str(key))
        return str(e.exception)

    def test_refused_against_the_production_key(self):
        self.assertIn('not by the authenticated key', self.refused(RELEASE_KEY))

    def test_refused_when_the_test_key_is_offered_as_the_key(self):
        self.assertIn('not by the authenticated key', self.refused(self.test_key))

    def test_acquire_writes_nothing_on_refusal(self):
        out = os.path.join(self.tmp, 'never')
        with self.assertRaises(rt.Refused): rt.acquire(self.archive, self.sig, RELEASE_FPR, str(RELEASE_KEY), out)
        self.assertFalse(os.path.exists(out))

    def test_the_test_path_needs_the_test_fingerprint_named_explicitly(self):
        # R4(a): a TEST acquisition names the TEST key explicitly; it is the same check, never a production acceptance.
        self.assertEqual(rt.verify_sig(self.archive, self.sig, self.test_fpr, self.test_key), self.test_fpr)

    def test_one_byte_mutation_fails(self):
        bad = self.archive + '.mut'; b = bytearray(Path(self.archive).read_bytes()); b[len(b) // 2] ^= 1; Path(bad).write_bytes(b)
        with self.assertRaises(rt.Refused): rt.verify_sig(bad, self.sig, self.test_fpr, self.test_key)

    def test_armored_or_doubled_signature_fails_rule_o(self):
        sig = Path(self.sig).read_bytes()
        for bad in (sig + sig, b'-----BEGIN PGP SIGNATURE-----\n' + sig):
            with self.assertRaises(rt.Refused): rt.rule_o(bad)


@unittest.skipUnless(GPG, 'gpg and gpgv needed')
class ReleaseVectors(unittest.TestCase):
    """The committed section 15.9 vectors: acceptance (`accept` in expected.json) under the R5 production fingerprint."""
    def test_every_case(self):
        fps = json.loads((VECTORS / 'keys/FINGERPRINTS.json').read_text())
        for case in sorted((VECTORS / 'cases').iterdir()):
            e = json.loads((case / 'expected.json').read_text())
            fpr = fps['test'] if case.name == '02-valid-test' else fps['production']
            try:
                rt.verify_sig(str(case / e['archive']), str(case / e['signature']), fpr, str(case / e['keyring'])); got = True
            except rt.Refused:
                got = False
            self.assertEqual(got, e['accept'], case.name)

    def test_key_file_must_be_the_authenticated_key(self):
        fps = json.loads((VECTORS / 'keys/FINGERPRINTS.json').read_text())
        c = VECTORS / 'cases/01-valid-production'
        with self.assertRaises(rt.Refused) as e:
            rt.verify_sig(str(c / 'tessera-verifier-v1-1.parts'), str(c / 'tessera-verifier-v1-1.parts.sig'), fps['production'], str(VECTORS / 'keys/test.pub.pgp'))
        self.assertIn('is not the authenticated', str(e.exception))


if __name__ == '__main__': unittest.main()
