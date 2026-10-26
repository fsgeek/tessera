"""Command line (profile 3.5, 15.9): production by default, install record checks, release checker, output shape."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from fixtures import make_fixture, write_test_release
from tessera_verify import install_record
from tessera_verify.codec import jcs, shahex


def cli(*args, env=None):
    return subprocess.run([sys.executable, '-m', 'tessera_verify', *args], capture_output=True, text=True, env=env)


class CliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(); cls.root = Path(cls.tmp.name)
        cls.b, cls.t, cls.c = make_fixture()
        (cls.root / 'bundle.json').write_bytes(jcs(cls.b)); (cls.root / 'trust.json').write_bytes(jcs(cls.t))
        cls.test_args = write_test_release(cls.root, cls.t, cls.c)
        cls.base = ['--trust', str(cls.root / 'trust.json'), '--bundle', str(cls.root / 'bundle.json')]

    @classmethod
    def tearDownClass(cls): cls.tmp.cleanup()

    def test_default_mode_is_production(self):
        r = cli(*self.base)
        self.assertEqual((r.returncode, r.stdout, r.stderr.strip()), (2, '', 'TRUST_CONFIG_UNAUTHENTICATED'))
        r = cli(*self.base, '--mode', 'production', *self.test_args[2:])
        self.assertEqual((r.returncode, r.stdout, r.stderr.strip()), (2, '', 'TEST_AUTHORITY_REFUSED'))

    def test_test_mode_must_be_explicit(self):
        r = cli(*self.test_args[2:], *self.base)       # release and key flags but no --mode test
        self.assertEqual((r.returncode, r.stdout, r.stderr.strip()), (2, '', 'TEST_AUTHORITY_REFUSED'))
        r = cli(*self.test_args, *self.base)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(set(out), {'stable', 'utc_assessment'}); self.assertEqual(r.stdout.strip(), jcs(out).decode())

    def test_request_other_than_strict_is_out_of_profile(self):
        out = json.loads(cli(*self.test_args, *self.base, '--request', 'degraded').stdout)
        self.assertEqual((out['stable']['verdict'], out['stable']['reason'], out['stable']['T']), ('UNVERIFIABLE', 'OUT_OF_PROFILE', None))
        self.assertIsNone(out['utc_assessment']['utc_upper_bound'])

    def test_missing_or_altered_install_record_refuses(self):
        r = cli(*self.test_args, *self.base, '--install-record', str(self.root / 'absent.json'))
        self.assertEqual((r.returncode, r.stdout, r.stderr.strip()), (2, '', 'INSTALL_RECORD_MISSING'))
        rec = json.loads(install_record.default_path().read_text()); rec['unicode_module_sha256'] = '0' * 64
        (self.root / 'bad.json').write_text(json.dumps(rec))
        r = cli(*self.test_args, *self.base, '--install-record', str(self.root / 'bad.json'))
        self.assertEqual((r.returncode, r.stdout, r.stderr.strip()), (2, '', 'UNICODE_TABLES_UNSUPPORTED'))
        (self.root / 'junk.json').write_text('{}')
        r = cli(*self.test_args, *self.base, '--install-record', str(self.root / 'junk.json'))
        self.assertEqual((r.returncode, r.stdout, r.stderr.strip()), (2, '', 'INSTALL_RECORD_INVALID'))

    def test_missing_sha1dc_detector_is_a_startup_refusal_without_verdict(self):
        rec = json.loads(install_record.default_path().read_text()); rec['sha1dc_binary'] = str(self.root / 'no-such-sha1dcsum')
        (self.root / 'nodet.json').write_text(json.dumps(rec))
        r = cli(*self.test_args, *self.base, '--install-record', str(self.root / 'nodet.json'))
        self.assertEqual((r.returncode, r.stdout, r.stderr.strip()), (2, '', 'SHA1DC_UNAVAILABLE'))
        rec['sha1dc_binary'] = '/bin/true'   # present but wrong hash / non-functional
        (self.root / 'badet.json').write_text(json.dumps(rec))
        r = cli(*self.test_args, *self.base, '--install-record', str(self.root / 'badet.json'))
        self.assertEqual((r.returncode, r.stdout, r.stderr.strip()), (2, '', 'SHA1DC_UNAVAILABLE'))

    def test_install_record_hash_is_a_diagnostic_only(self):
        r = cli(*self.test_args, *self.base, '--diagnostics')
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr.strip(), 'install.json sha256: ' + shahex(install_record.default_path().read_bytes()))
        self.assertEqual(json.loads(r.stdout), json.loads(cli(*self.test_args, *self.base).stdout))

    def test_missing_bundle_is_an_io_refusal_without_verdict(self):
        r = cli(*self.test_args, '--trust', str(self.root / 'trust.json'), '--bundle', str(self.root / 'nope.json'))
        self.assertEqual((r.returncode, r.stdout), (2, '')); self.assertTrue(r.stderr.startswith('INPUT_IO_ERROR'))

    def test_release_checker(self):
        new = copy.deepcopy(self.t); new['version'] = '2'; new['previous_sha256'] = shahex(jcs(self.t))
        (self.root / 'next.json').write_bytes(jcs(new))
        self.assertEqual(cli('--previous', str(self.root / 'trust.json'), '--next', str(self.root / 'next.json')).stdout.strip(), 'ACCEPT')
        del new['header_pins']['100']; (self.root / 'next2.json').write_bytes(jcs(new))
        self.assertEqual(cli('--previous', str(self.root / 'trust.json'), '--next', str(self.root / 'next2.json')).stdout.strip(), 'REJECT')


if __name__ == '__main__': unittest.main()
