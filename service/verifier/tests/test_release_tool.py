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
BASELINE = 'b134cdfdacc5d89f2748fa7ec15c46e38b51a32c'   # the verifier package commit, OTS block 973240


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

    def rewrite(self, parts):
        m = json.loads(parts['RELEASE.json']); m['parts'] = {p: rt.sha(b) for p, b in parts.items() if p != 'RELEASE.json'}
        parts['RELEASE.json'] = rt.jcs(m); return parts

    def test_required_parts_and_string_types(self):
        for p in ('service/verifier/requirements.lock', 'docs/V1-RELYING-PARTY.md', 'service/verifier/install.sh',
                  'service/verifier/vendor/SHA1DC-PIN.md'):
            bad = dict(self.parts); del bad[p]
            with self.assertRaises(rt.Refused, msg=p) as e: rt.check_bindings(self.rewrite(bad))
            self.assertIn('required part is missing', str(e.exception))
        m = json.loads(self.parts['RELEASE.json']); m['trust_config_version'] = 1
        with self.assertRaises(rt.Refused): rt.check_bindings(dict(self.parts, **{'RELEASE.json': rt.jcs(m)}))

    def test_install_tree_must_be_exactly_the_release(self):
        with tempfile.TemporaryDirectory() as d:
            root = os.path.join(d, 'r'); rt.unpack(self.parts, root)
            self.assertEqual(rt.bindings(root), 'service/verifier/release/v1-1/release_constants.py')
            extra = os.path.join(root, 'service/verifier/tessera_verify/stray.py'); Path(extra).write_text('x = 1\n')
            with self.assertRaises(rt.Refused) as e: rt.bindings(root)
            self.assertIn('not exactly the release', str(e.exception))
            os.remove(extra); os.remove(os.path.join(root, 'service/verifier/README.md'))
            with self.assertRaises(rt.Refused): rt.bindings(root)

    def test_install_sh_refuses_an_unpacked_tree_run_by_hand(self):
        with tempfile.TemporaryDirectory() as d:
            root = os.path.join(d, 'r'); rt.unpack(self.parts, root)
            r = subprocess.run(['bash', os.path.join(root, 'service/verifier/install.sh')], capture_output=True, text=True,
                               env={k: v for k, v in os.environ.items() if k != 'TESSERA_ACQUIRED_ROOT'})
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('installed only by release_tool.py acquire', r.stderr)
            self.assertFalse(os.path.exists(os.path.join(root, 'service/verifier/.venv')))

    def test_diff_is_deterministic_and_self_hashed(self):
        a, line = rt.diff(str(REPO), BASELINE, 'HEAD', '1')
        self.assertEqual(rt.diff(str(REPO), BASELINE, 'HEAD', '1')[0], a)
        body, last = a.rsplit(b'\n', 2)[0] + b'\n', a.splitlines()[-1].decode()
        self.assertEqual(last, line); self.assertTrue(line.endswith(rt.groups(rt.sha(body), 8)))
        self.assertIn(b'added     ', a); self.assertIn(b'service/verifier/release/release_tool.py', a)

    def test_baseline_proof_parses_to_its_anchor(self):
        tree = rt.blobs_at(str(REPO), 'HEAD'); c = rt.resolve(str(REPO), BASELINE)
        stamp = rt.read_blob(str(REPO), tree['timestamps/anchored/' + c])
        atts = rt.ots_heights(rt.read_blob(str(REPO), tree['timestamps/anchored/%s.ots' % c]), rt.hashlib.sha256(stamp).digest())
        self.assertEqual(min(atts)[0], 973240)
        with self.assertRaises(rt.Refused): rt.ots_heights(rt.read_blob(str(REPO), tree['timestamps/anchored/%s.ots' % c]), b'\0' * 32)

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
        for key in (RELEASE_KEY, self.test_key):
            out = os.path.join(self.tmp, 'never')
            with self.assertRaises(rt.Refused) as e: rt.acquire(self.archive, self.sig, RELEASE_FPR, str(key), out)
            self.assertEqual(str(e.exception), 'signed by %s, not by the authenticated key %s' % (self.test_fpr, RELEASE_FPR))
            self.assertFalse(os.path.exists(out))

    def test_acquire_requires_the_expected_namespace(self):
        # M3: an explicit TEST acquisition refuses a PRODUCTION-labelled archive.
        with self.assertRaises(rt.Refused) as e: rt.acquire(self.archive, self.sig, self.test_fpr, self.test_key, None, namespace='TEST')
        self.assertIn('namespace is PRODUCTION, not the expected TEST', str(e.exception))
        # The boundary R4 states: refusal is by key. A caller who supplies a TEST fingerprint as if it were the
        # production one has substituted the bootstrap authority, which no label check can detect.
        m, h = rt.acquire(self.archive, self.sig, self.test_fpr, self.test_key, None)
        self.assertEqual((m['namespace'], h), ('PRODUCTION', rt.sha(Path(self.archive).read_bytes())))

    def test_signature_without_issuer_fingerprint_is_not_a_rule_o_refusal(self):
        # M4: rule O allows the hashed issuer fingerprint to be absent; the signer is then established by gpgv alone.
        sig = Path(self.sig).read_bytes(); h = 2 if sig[0] == 0x88 else 3; b = sig[h:]
        hl = int.from_bytes(b[4:6], 'big'); hashed = b[6:6 + hl]; kept, pos = b'', 0
        while pos < len(hashed):
            n = hashed[pos]; sp = hashed[pos:pos + 1 + n]
            if sp[1] & 0x7F != 33: kept += sp
            pos += 1 + n
        body = b[:4] + len(kept).to_bytes(2, 'big') + kept + b[6 + hl:]
        bad = bytes([0x88, len(body)]) + body
        self.assertIsNone(rt.rule_o(bad))
        with self.assertRaises(rt.Refused) as e: rt.verify_bytes(Path(self.archive).read_bytes(), bad, self.test_fpr, self.test_key)
        self.assertTrue(str(e.exception).startswith('gpgv refused'), str(e.exception))

    def test_the_test_path_needs_the_test_fingerprint_named_explicitly(self):
        # R4(a): a TEST acquisition names the TEST key explicitly; it is the same check, never a production acceptance.
        self.assertEqual(rt.verify_sig(self.archive, self.sig, self.test_fpr, self.test_key), self.test_fpr)

    def test_one_byte_mutation_fails(self):
        bad = self.archive + '.mut'; b = bytearray(Path(self.archive).read_bytes()); b[len(b) // 2] ^= 1; Path(bad).write_bytes(b)
        with self.assertRaises(rt.Refused) as e: rt.verify_sig(bad, self.sig, self.test_fpr, self.test_key)
        self.assertTrue(str(e.exception).startswith('gpgv refused (exit 1)'), str(e.exception))

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



class Pins(unittest.TestCase):
    """`pins`: recorded explorer answers (2026-11-24, blockstream.info and mempool.space), no network."""
    REC = json.loads((HERE / 'tests/fixtures_pins/explorers-976141-976209.json').read_text())
    TRUST = (HERE / 'release/v1-1/trust.json').read_bytes()
    NOW = rt.utc_s('2026-11-24T00:00:00Z')   # this machine's clock, after every recorded header

    def base(self):   # the release's first twelve pins, as before this change
        t = json.loads(self.TRUST)
        t['header_pins'] = {h: p for h, p in t['header_pins'].items() if int(h) <= 976146}
        t['as_of'] = '2026-11-16T15:48:11Z'
        return rt.jcs(t)

    def getter(self, **patch):
        rec = dict(self.REC, **patch)
        return lambda u: rec[u]

    def add(self, heights, trust=None, **patch):
        return rt.add_pins(trust or self.base(), heights, self.getter(**patch), now=self.NOW)

    def test_adds_six_pins_and_keeps_everything_else(self):
        new, added, as_of = self.add([976209])
        old, t = json.loads(self.base()), json.loads(new)
        self.assertEqual(added, list(range(976209, 976215)))
        for h, p in old['header_pins'].items():
            self.assertEqual(t['header_pins'][h], p)
        for h in added:
            self.assertEqual(t['header_pins'][str(h)], self.REC['https://blockstream.info/api/block-height/%d' % h])
        self.assertEqual({k: v for k, v in t.items() if k not in ('header_pins', 'as_of')},
                         {k: v for k, v in old.items() if k not in ('header_pins', 'as_of')})
        self.assertEqual((t['version'], t['previous_sha256']), ('1', '0' * 64))
        self.assertEqual(rt.jcs(t), new)
        times = [int.from_bytes(bytes.fromhex(self.REC['https://blockstream.info/api/block/%s/header' % t['header_pins'][str(h)]])[68:72], 'little') for h in added]
        self.assertEqual(rt.utc_s(as_of), max(times))

    def test_already_pinned_run_is_idempotent(self):
        new, added, as_of = self.add([976141])
        self.assertEqual((added, as_of), ([], '2026-11-16T15:48:11Z'))
        self.assertEqual(new, self.base())

    def test_as_of_never_decreases(self):
        t = json.loads(self.base()); t['as_of'] = '2026-11-30T00:00:00Z'
        later = rt.utc_s('2026-12-01T00:00:00Z')
        self.assertEqual(rt.add_pins(rt.jcs(t), [976209], self.getter(), now=later)[2], '2026-11-30T00:00:00Z')
        with self.assertRaises(rt.Refused):     # an as_of later than the clock is refused, not carried
            self.add([976209], trust=rt.jcs(t))

    def test_conflicting_existing_pin_is_refused(self):
        t = json.loads(self.base()); t['header_pins']['976143'] = 'ab' * 32
        with self.assertRaises(rt.Refused) as e: self.add([976141], trust=rt.jcs(t))
        self.assertIn('976143 is pinned', str(e.exception))

    def test_explorers_disagreeing_is_refused(self):
        m = 'https://mempool.space/api/block-height/976211'
        other = self.REC['https://blockstream.info/api/block-height/976141']   # a real block, hashes to its id
        with self.assertRaises(rt.Refused) as e:
            self.add([976209], **{m: other, 'https://mempool.space/api/block/%s/header' % other:
                                  self.REC['https://blockstream.info/api/block/%s/header' % other]})
        self.assertIn('disagree on block 976211', str(e.exception))

    def test_header_not_hashing_to_its_id_is_refused(self):
        bh = self.REC['https://blockstream.info/api/block-height/976212']
        u = 'https://mempool.space/api/block/%s/header' % bh
        bad = self.REC[u][:-2] + ('00' if self.REC[u][-2:] != '00' else '01')
        with self.assertRaises(rt.Refused) as e: self.add([976209], **{u: bad})
        self.assertIn('does not hash', str(e.exception))

    def test_broken_link_is_refused(self):
        other = self.REC['https://blockstream.info/api/block-height/976143']   # valid header, wrong parent
        patch = {}
        for api in rt.EXPLORERS:
            patch['%s/block-height/976212' % api] = other
            patch['%s/block/%s/header' % (api, other)] = self.REC['https://blockstream.info/api/block/%s/header' % other]
        with self.assertRaises(rt.Refused) as e: self.add([976209], **patch)
        self.assertIn('976212 does not link to block 976211', str(e.exception))

    def test_too_few_confirmations_is_refused(self):
        tip = {'%s/blocks/tip/height' % api: str(976209 + 5 + rt.PIN_DEPTH - 2) for api in rt.EXPLORERS}
        with self.assertRaises(rt.Refused) as e: self.add([976209], **tip)
        self.assertIn('fewer than 6 confirmations', str(e.exception))
        tip = {'%s/blocks/tip/height' % api: str(976209 + 5 + rt.PIN_DEPTH - 1) for api in rt.EXPLORERS}
        self.assertEqual(len(self.add([976209], **tip)[1]), 6)

    def test_noncanonical_trust_or_repeated_heights_are_refused(self):
        with self.assertRaises(rt.Refused): self.add([976209], trust=self.base() + b'\n')
        with self.assertRaises(rt.Refused): self.add([976209, 976209])

    def test_cli_rewrites_trust_and_constants(self):
        with tempfile.TemporaryDirectory() as d:
            tp, cp = Path(d) / 'trust.json', Path(d) / 'release_constants.py'
            tp.write_bytes(self.base())
            catalog = (REPO / rt.FROZEN_CATALOG).read_bytes()
            cp.write_bytes(rt.constants_source('PRODUCTION', self.base(), catalog))
            saved = rt.fetch; rt.fetch = self.getter()
            try:
                rt.pins_cmd(str(tp), [976209])
            finally:
                rt.fetch = saved
            c = rt.parse_constants(cp.read_bytes())
            self.assertEqual(c['TRUST_SHA256'], rt.sha(tp.read_bytes()))
            self.assertEqual((c['NAMESPACE'], c['CATALOG_BYTES']), ('PRODUCTION', catalog))
            self.assertEqual(sorted(os.listdir(d)), ['release_constants.py', 'trust.json'])

    def setup_dir(self, d):
        tp, cp = Path(d) / 'trust.json', Path(d) / 'release_constants.py'
        tp.write_bytes(self.base())
        cp.write_bytes(rt.constants_source('PRODUCTION', self.base(), (REPO / rt.FROZEN_CATALOG).read_bytes()))
        return tp, cp

    def run_cmd(self, tp, get=None):
        saved = rt.fetch; rt.fetch = get or self.getter()
        try:
            rt.pins_cmd(str(tp), [976209])
        finally:
            rt.fetch = saved

    def test_failure_between_the_replaces_restores_trust(self):
        import unittest.mock as um
        with tempfile.TemporaryDirectory() as d:
            tp, cp = self.setup_dir(d)
            t0, c0 = tp.read_bytes(), cp.read_bytes()
            real, n = os.replace, [0]
            def flaky(a, b):
                n[0] += 1
                if n[0] == 2: raise OSError('boom')
                return real(a, b)
            with um.patch('os.replace', flaky), self.assertRaises(OSError):
                self.run_cmd(tp)
            self.assertEqual((tp.read_bytes(), cp.read_bytes()), (t0, c0))
            self.assertEqual(sorted(os.listdir(d)), ['release_constants.py', 'trust.json'])

    def test_stale_new_file_does_not_block(self):
        with tempfile.TemporaryDirectory() as d:
            tp, cp = self.setup_dir(d)
            (Path(d) / 'release_constants.py.new').write_bytes(b'stale'); (Path(d) / 'trust.json.new').write_bytes(b'stale')
            self.run_cmd(tp)
            self.assertEqual(rt.parse_constants(cp.read_bytes())['TRUST_SHA256'], rt.sha(tp.read_bytes()))
            self.assertEqual(len(json.loads(tp.read_bytes())['header_pins']), 18)

    def test_disk_change_during_run_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            tp, cp = self.setup_dir(d)
            c0 = cp.read_bytes()
            other = json.loads(self.base()); other['as_of'] = '2026-11-17T00:00:00Z'
            other = rt.jcs(other)
            rec, hit = self.getter(), [False]
            def get(u):
                if not hit[0]: hit[0] = True; tp.write_bytes(other)   # a concurrent writer, mid-fetch
                return rec(u)
            with self.assertRaises(rt.Refused) as e: self.run_cmd(tp, get)
            self.assertIn('changed during this run', str(e.exception))
            self.assertEqual((tp.read_bytes(), cp.read_bytes()), (other, c0))
            self.assertEqual(sorted(os.listdir(d)), ['release_constants.py', 'trust.json'])

    def test_noncanonical_pin_key_is_refused(self):
        for bad in ('0976141', '+976141', '976141 '):
            t = json.loads(self.base()); t['header_pins'][bad] = t['header_pins'].pop('976141')
            with self.assertRaises(rt.Refused) as e: self.add([976209], trust=rt.jcs(t))
            self.assertIn('canonical decimal', str(e.exception))


if __name__ == '__main__': unittest.main()
