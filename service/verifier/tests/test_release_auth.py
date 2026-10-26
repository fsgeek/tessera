"""TEST-release authentication (profile 3.5 EA-01), production-by-default and refusal of TEST authority (15.9 R4).
Keys and releases are generated here; no conformance import."""
import base64
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from fixtures import make_fixture, new_key, key_file, make_release
from tessera_verify.codec import Fault, jcs, shahex
from tessera_verify import release_auth
from tessera_verify import release_constants

HERE = Path(__file__).resolve().parent.parent


class ReleaseAuthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base, cls.trust, cls.catalog = make_fixture()
        cls.trust_bytes = jcs(cls.trust)
        cls.cat_obj = dict(cls.catalog, TEST='label')
        cls.signer, cls.spki = new_key()
        cls.other, cls.other_spki = new_key()
        cls.tmp = tempfile.TemporaryDirectory()
        t = Path(cls.tmp.name)
        (t / 'trust.json').write_bytes(cls.trust_bytes)
        (t / 'bundle.json').write_bytes(jcs(cls.base))
        (t / 'key.json').write_text(json.dumps(key_file(cls.spki)))
        (t / 'otherkey.json').write_text(json.dumps(key_file(cls.other_spki)))
        cls.write_release('release.json', make_release(cls.signer, cls.spki, cls.trust_bytes, cls.cat_obj))
        cls.write_release('foreign.json', make_release(cls.other, cls.other_spki, cls.trust_bytes, cls.cat_obj))
        cls.write_release('wrongfmt.json', make_release(cls.signer, cls.spki, cls.trust_bytes, cls.cat_obj, fmt='tessera-v1-release/1'))

    @classmethod
    def tearDownClass(cls): cls.tmp.cleanup()

    @classmethod
    def write_release(cls, name, obj): (Path(cls.tmp.name) / name).write_text(json.dumps(obj))

    def p(self, name): return str(Path(self.tmp.name) / name)

    def setUp(self): self._saved = {k: getattr(release_constants, k) for k in ('NAMESPACE', 'TRUST_SHA256', 'CATALOG_SHA256', 'CATALOG_BYTES')}
    def tearDown(self):
        for k, v in self._saved.items(): setattr(release_constants, k, v)

    def code(self, code, fn, *a, **kw):
        with self.assertRaises(Fault) as cm: fn(*a, **kw)
        self.assertEqual(cm.exception.code, code)

    def cli(self, *args, env=None):
        e = {k: v for k, v in os.environ.items() if not k.startswith('TESSERA_V1_')}
        e.update(env or {})
        return subprocess.run([sys.executable, '-m', 'tessera_verify', '--trust', self.p('trust.json'),
                               '--bundle', self.p('bundle.json'), *args], capture_output=True, text=True, env=e, cwd=self.tmp.name)

    def test_authentic_release_accepted(self):
        body = release_auth.authenticate_test_release(self.p('release.json'), self.p('key.json'))
        self.assertEqual(body['trust_config_sha256'], shahex(self.trust_bytes))

    def test_foreign_signer_and_wrong_key_refused(self):
        self.code('TRUST_CONFIG_UNAUTHENTICATED', release_auth.authenticate_test_release, self.p('foreign.json'), self.p('key.json'))
        self.code('TRUST_CONFIG_UNAUTHENTICATED', release_auth.authenticate_test_release, self.p('release.json'), self.p('otherkey.json'))

    def test_tampered_body_and_bad_signature_refused(self):
        rel = json.loads(Path(self.p('release.json')).read_text())
        rel['release']['trust_config_sha256'] = '0' * 64
        self.write_release('tampered.json', rel)
        self.code('TRUST_CONFIG_UNAUTHENTICATED', release_auth.authenticate_test_release, self.p('tampered.json'), self.p('key.json'))
        rel = json.loads(Path(self.p('release.json')).read_text())
        rel['signature']['r_s_hex'] = rel['signature']['r_s_hex'][:-1] + ('0' if rel['signature']['r_s_hex'][-1] != '0' else '1')
        self.write_release('badsig.json', rel)
        self.code('TRUST_CONFIG_UNAUTHENTICATED', release_auth.authenticate_test_release, self.p('badsig.json'), self.p('key.json'))
        rel['signature'] = {'alg': 'ECDSA-P256-SHA256'}
        self.write_release('nosig.json', rel)
        self.code('TRUST_CONFIG_UNAUTHENTICATED', release_auth.authenticate_test_release, self.p('nosig.json'), self.p('key.json'))

    def test_unknown_format_and_catalog_hash_refused(self):
        self.code('RELEASE_FORMAT_UNKNOWN', release_auth.authenticate_test_release, self.p('wrongfmt.json'), self.p('key.json'))
        c = dict(self.cat_obj); c['k'] = '7'
        rel = make_release(self.signer, self.spki, self.trust_bytes, self.cat_obj)
        rel['release']['catalog'] = c   # then re-sign so only the catalog hash is inconsistent
        r, s = decode_dss_signature(self.signer.sign(release_auth.jcs_ascii(rel['release']), ec.ECDSA(hashes.SHA256())))
        rel['signature']['r_s_hex'] = f'{r:064x}{s:064x}'
        self.write_release('badcat.json', rel)
        self.code('CATALOG_UNAUTHENTICATED', release_auth.authenticate_test_release, self.p('badcat.json'), self.p('key.json'))

    def test_cli_test_release_gives_verdict_and_refusals_give_none(self):
        ok = self.cli('--mode', 'test', '--test-release', self.p('release.json'), '--test-release-key', self.p('key.json'))
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertEqual(json.loads(ok.stdout)['stable']['T'], '2026-10-14T12:00:00Z')
        self.assertEqual(json.loads(ok.stdout)['stable']['verdict'], 'VALID_STRICT')
        for rel, key in [('foreign.json', 'key.json'), ('release.json', 'otherkey.json')]:
            bad = self.cli('--mode', 'test', '--test-release', self.p(rel), '--test-release-key', self.p(key))
            self.assertEqual((bad.returncode, bad.stdout, bad.stderr.strip()), (2, '', 'TRUST_CONFIG_UNAUTHENTICATED'))

    def test_test_mode_environment_interface_matches_flags(self):
        env = {release_auth.ENV_RELEASE: self.p('release.json'), release_auth.ENV_KEY: self.p('key.json')}
        self.assertEqual(self.cli('--mode', 'test', env=env).returncode, 0)
        env[release_auth.ENV_RELEASE] = self.p('foreign.json')
        self.assertEqual(self.cli('--mode', 'test', env=env).stderr.strip(), 'TRUST_CONFIG_UNAUTHENTICATED')
        self.assertEqual(self.cli('--mode', 'test', env={release_auth.ENV_RELEASE: self.p('release.json')}).stderr.strip(), 'TRUST_CONFIG_UNAUTHENTICATED')

    def test_test_mode_without_release_refuses(self):
        r = self.cli('--mode', 'test')
        self.assertEqual((r.returncode, r.stdout, r.stderr.strip()), (2, '', 'TRUST_CONFIG_UNAUTHENTICATED'))

    def test_production_is_the_default_and_refuses_test_authority(self):
        # No --mode: production. A correct TEST release with a TEST key, by flags or by environment, is refused and
        # no verdict is printed (15.9 R4). The same with --mode production given explicitly.
        for mode in ([], ['--mode', 'production']):
            for args, env in [(('--test-release', self.p('release.json'), '--test-release-key', self.p('key.json')), None),
                              ((), {release_auth.ENV_RELEASE: self.p('release.json'), release_auth.ENV_KEY: self.p('key.json')}),
                              ((), {release_auth.ENV_CATALOG: self.p('release.json')})]:
                r = self.cli(*mode, *args, env=env)
                self.assertEqual((r.returncode, r.stdout, r.stderr.strip()), (2, '', 'TEST_AUTHORITY_REFUSED'))
        self.code('TEST_AUTHORITY_REFUSED', release_auth.authenticate, 'production', self.p('release.json'), self.p('key.json'))

    def test_unprovisioned_production_does_not_accept(self):
        r = self.cli()   # no TEST input; a source tree has no production binding, so it refuses
        self.assertEqual((r.returncode, r.stdout, r.stderr.strip()), (2, '', 'TRUST_CONFIG_UNAUTHENTICATED'))
        self.assertEqual(release_constants.NAMESPACE, None)

    def test_production_compiled_installation_refuses_test_mode(self):
        release_constants.NAMESPACE = 'PRODUCTION'
        self.code('TEST_AUTHORITY_REFUSED', release_auth.authenticate, 'test', self.p('release.json'), self.p('key.json'))
        self.assertEqual(release_constants.TRUST_SHA256, self._saved['TRUST_SHA256'])   # nothing was provisioned

    def test_production_with_compiled_binding_is_accepted_without_test_material(self):
        release_constants.NAMESPACE = 'PRODUCTION'; release_constants.TRUST_SHA256 = '0' * 64; release_constants.CATALOG_BYTES = b'{}'
        self.assertEqual(release_auth.authenticate('production', env={}), 'PRODUCTION')

    def test_unknown_mode_refused(self):
        self.code('MODE_UNKNOWN', release_auth.authenticate, 'staging', env={})

    def test_test_provisioning_sets_namespace_test_and_strips_label(self):
        release_auth.authenticate('test', self.p('release.json'), self.p('key.json'))
        self.assertEqual(release_constants.NAMESPACE, 'TEST')
        self.assertNotIn(b'"TEST"', release_constants.CATALOG_BYTES)
        self.assertEqual(release_constants.CATALOG_BYTES, jcs(self.catalog))

    def test_provisioning_is_in_memory_only(self):
        before = (HERE / 'tessera_verify' / 'release_constants.py').read_bytes()
        self.cli('--mode', 'test', '--test-release', self.p('release.json'), '--test-release-key', self.p('key.json'))
        self.assertEqual((HERE / 'tessera_verify' / 'release_constants.py').read_bytes(), before)


if __name__ == '__main__': unittest.main()
