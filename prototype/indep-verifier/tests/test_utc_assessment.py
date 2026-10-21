"""A10.1.1 / profile 7.4: the conditional UTC assessment.

U = 7200 + max(uint64 nTime(h*..h*+5)), reported in `utc_assessment` beside `assumption_id` A-UTC-7200-6, outside
the stable six. Null exactly when T is null. Never changes the verdict."""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fixtures import make_fixture,enc
from codec import jcs,utc,isotime
from policy import parse_trust,parse_catalog
from verify import verify_bundle,utc_assessment,UTC_ASSUMPTION
import sha1dc

HERE=Path(__file__).resolve().parents[1]
REAL1=HERE.parent/'e2e'/'receipts'/'real-1'
POSITIVE=('VALID_STRICT','OK') if sha1dc.available() else ('UNVERIFIABLE','INDEPENDENT_SHA1DC_UNAVAILABLE')
T0=utc('2026-10-14T12:00:00Z')

def run(b,t,c,**kw):
    return verify_bundle(jcs(b),parse_trust(jcs(t)),parse_catalog(jcs(c)),**kw)

def both(b,t,c):
    """Stable result without and with the assessment, plus the assessment."""
    plain=run(b,t,c); stable,assessment=run(b,t,c,utc=True)
    return plain,stable,assessment

class UtcAssessmentTests(unittest.TestCase):
    def check(self,b,t,c,bound,expected=None):
        plain,stable,a=both(b,t,c)
        self.assertEqual(plain,stable)                       # never changes the stable six
        self.assertEqual(len(stable),6); self.assertNotIn('utc_assessment',stable)
        self.assertEqual(a,{'assumption_id':'A-UTC-7200-6','utc_upper_bound':bound})
        if expected: self.assertEqual((stable['verdict'],stable['reason']),expected)
        self.assertEqual(bound is None,stable['T'] is None)  # null exactly when T is null
        return stable

    def test_monotone_fixture(self):
        b,t,c=make_fixture()
        s=self.check(b,t,c,isotime(T0+7200),POSITIVE)       # fixture: all six headers carry T0
        self.assertEqual(s['T'],isotime(T0))

    def test_nonmonotone_max_in_middle(self):
        times=[T0,T0+600,T0+9000,T0+1200,T0+1800,T0+2400]
        b,t,c=make_fixture(receipt_times=times)
        self.check(b,t,c,isotime(T0+9000+7200),POSITIVE)    # max is h*+2, not h*+5 and not T

    def test_nonmonotone_h_star_is_max(self):
        times=[T0,T0-3000,T0-2400,T0-1800,T0-1200,T0-600]
        b,t,c=make_fixture(receipt_times=times)
        s=self.check(b,t,c,isotime(T0+7200),POSITIVE)       # confirmed_at < T: not a failure, U uses T
        self.assertEqual(s['T'],isotime(T0))

    def test_2106_boundary_no_modular_reduction(self):
        times=[T0,T0+600,T0+1200,4294967295,T0+2400,T0+3000]
        b,t,c=make_fixture(receipt_times=times)
        self.check(b,t,c,'2106-02-07T08:28:15Z',POSITIVE)
        self.assertEqual(utc('2106-02-07T08:28:15Z'),4294974495)

    def test_reported_with_invalid(self):
        b,t,c=make_fixture(); b=copy.deepcopy(b); b['layers'][0]['spec']=enc(b'wrong spec')
        s=self.check(b,t,c,isotime(T0+7200),('INVALID','BUNDLE_OBJECT_HASH'))
        self.assertIsNotNone(s['T'])

    def test_reported_with_unverifiable(self):
        b,t,c=make_fixture(); b=copy.deepcopy(b); del b['layers'][0]['git']
        s=self.check(b,t,c,isotime(T0+7200))
        self.assertEqual(s['verdict'],'UNVERIFIABLE')

    def test_null_when_no_qualifying_anchor(self):
        b,t,c=make_fixture(); b=copy.deepcopy(b); del b['layers'][0]['headers']['125']
        s=self.check(b,t,c,None)                             # h*+5 missing: no qualifying attestation, T null
        self.assertEqual((s['verdict'],s['reason']),('UNVERIFIABLE','HEADERS_MISSING'))

    def test_null_when_digest_mismatch(self):
        # Selected anchor exists but its digest is not SHA256(a_sig): T is null, so U is null.
        b,t,c=make_fixture(); other,_,_=make_fixture(); b=copy.deepcopy(b)
        b['layers'][0]['receipt_anchor']=other['layers'][0]['receipt_anchor']
        from anchors import sha256d
        for h in range(120,126):                             # swap in, and pin, the other fixture's receipt headers
            b['layers'][0]['headers'][str(h)]=other['layers'][0]['headers'][str(h)]
            t['header_pins'][str(h)]=sha256d(bytes.fromhex(b['layers'][0]['headers'][str(h)]))[::-1].hex()
        s=self.check(b,t,c,None)
        self.assertEqual(s['verdict'],'INVALID')

    def test_dispatch_terminal(self):
        _,t,c=make_fixture()
        for bundle in (b'not json',jcs({'profile':'other','layers':[]})):
            stable,a=verify_bundle(bundle,parse_trust(jcs(t)),parse_catalog(jcs(c)),utc=True)
            self.assertEqual((stable['verdict'],stable['reason'],stable['T']),('UNVERIFIABLE','OUT_OF_PROFILE',None))
            self.assertEqual(a,{'assumption_id':UTC_ASSUMPTION,'utc_upper_bound':None})
        b,t,c=make_fixture()
        stable,a=verify_bundle(jcs(b),parse_trust(jcs(t)),parse_catalog(jcs(c)),request='degraded',utc=True)
        self.assertEqual((stable['reason'],stable['T'],a['utc_upper_bound']),('OUT_OF_PROFILE',None,None))

    def test_helper_null(self):
        self.assertEqual(utc_assessment(),{'assumption_id':'A-UTC-7200-6','utc_upper_bound':None})

@unittest.skipUnless((REAL1/'bundle.json').exists(),'real-1 receipt not present')
@unittest.skipIf((REAL1/'release.json').exists() and 'utc_delta_s' not in json.loads((REAL1/'release.json').read_text())['release']['catalog'],
    'real-1 TEST release predates the catalog fields utc_delta_s/utc_m (2026-10-19 item 8); the verifier fails closed on it by design; rebuild under e2e')
class RealReceiptTests(unittest.TestCase):
    """First real V1 receipt (TEST pipeline): inclusion block 972187 and successors 972188..972192."""
    def test_real1_header_set(self):
        hs=json.loads((REAL1/'bundle.json').read_text())['layers'][0]['headers']
        times=[int.from_bytes(bytes.fromhex(hs[str(h)])[68:72],'little') for h in range(972187,972193)]
        self.assertEqual(max(times),1792435812)              # nTime(972192), 2026-10-19T18:50:12Z
        r=subprocess.run([sys.executable,str(HERE/'verify.py'),'--trust',str(REAL1/'trust.json'),'--bundle',str(REAL1/'bundle.json'),
                          '--test-release',str(REAL1/'release.json'),'--test-release-key',str(REAL1/'release-key.json')],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        out=json.loads(r.stdout)
        self.assertEqual(set(out),{'stable','utc_assessment'})
        self.assertEqual(out['stable']['T'],'2026-10-19T17:49:13Z')
        self.assertEqual(out['utc_assessment'],{'assumption_id':'A-UTC-7200-6','utc_upper_bound':'2026-10-19T20:50:12Z'})
        if sha1dc.available(): self.assertEqual((out['stable']['verdict'],out['stable']['reason']),('VALID_STRICT','OK'))

if __name__=='__main__': unittest.main()
