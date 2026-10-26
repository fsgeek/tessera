"""A10.1.1 / profile 7.4: the conditional UTC assessment.

U = 7200 + max(uint64 nTime(h*..h*+5)), reported in `utc_assessment` beside `assumption_id` A-UTC-7200-6, outside
the stable six. Null exactly when T is null. Never changes the verdict."""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from fixtures import make_fixture,enc
from tessera_verify.codec import jcs,utc,isotime
from tessera_verify.policy import parse_trust,parse_catalog
from tessera_verify.verify import verify_bundle,utc_assessment
from tessera_verify import sha1dc

HERE=Path(__file__).resolve().parents[1]
POSITIVE=('VALID_STRICT','OK')   # the detector's presence is a startup condition (conftest applies install.json)
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
        from tessera_verify.anchors import sha256d
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
            self.assertEqual(a,{'assumption_id':'A-UTC-7200-6','utc_upper_bound':None})
        b,t,c=make_fixture()
        stable,a=verify_bundle(jcs(b),parse_trust(jcs(t)),parse_catalog(jcs(c)),request='degraded',utc=True)
        self.assertEqual((stable['reason'],stable['T'],a['utc_upper_bound']),('OUT_OF_PROFILE',None,None))

    def test_helper_null(self):
        _,_,c=make_fixture()
        self.assertEqual(utc_assessment(catalog=parse_catalog(jcs(c))),{'assumption_id':'A-UTC-7200-6','utc_upper_bound':None})

    def test_delta_and_m_come_from_the_catalog(self):
        # Not compiled in: a catalog carrying Delta = 3600 moves the bound and names itself in the assumption id.
        b,t,c=make_fixture(); c['utc_delta_s']='3600'
        plain,stable,a=both(b,t,c)
        self.assertEqual(a,{'assumption_id':'A-UTC-3600-6','utc_upper_bound':isotime(T0+3600)})
        self.assertEqual(plain,stable)

if __name__=='__main__': unittest.main()
