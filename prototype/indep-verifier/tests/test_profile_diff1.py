"""Independent regressions derived from the 2026-10-14 profile corrections."""
import copy
import unittest
from fixtures import make_fixture,rr,enc
from codec import Fault,b64,jcs
from dnssec import parse_snapshot,wire,rrsig_order
from policy import parse_trust,parse_catalog
from verify import verify_bundle


class ProfileDiff1Tests(unittest.TestCase):
    def test_noncanonical_signer_rejects_beside_valid_witness(self):
        b,t,c=make_fixture(); body=b64(b['layers'][0]['dns']['snapshot_body'])
        txt=parse_snapshot(body).txt; original=txt.sigs[0].data
        for signer in [wire((b'Wamason',b'com')),b'\xc0\x00']:
            with self.subTest(signer=signer):
                bad=original[:16]+b'\xff\xff'+signer+original[-64:]
                mutated=body[:txt.sigs[0].offset]+rr(txt.owner,46,bad)+body[txt.sigs[0].offset:]
                with self.assertRaises(Fault) as cm: parse_snapshot(mutated)
                self.assertEqual(cm.exception.code,'SNAPSHOT_FORMAT')
                bundle=copy.deepcopy(b); bundle['layers'][0]['dns']['snapshot_body']=enc(mutated)
                report=verify_bundle(jcs(bundle),parse_trust(jcs(t)),parse_catalog(jcs(c)))
                self.assertEqual((report['verdict'],report['reason']),('INVALID','SNAPSHOT_FORMAT'))

    def test_malformed_rrsig_keeps_readable_sort_fields(self):
        # Empty signature is malformed, but tag and both times remain readable.
        def sig(tag,inception,expiration,signature=b''):
            return b'\x00\x30\x0d\x00'+bytes(4)+expiration.to_bytes(4,'big')+inception.to_bytes(4,'big')+tag.to_bytes(2,'big')+b'\x00'+signature
        for first,second in [(sig(1,20,30,b'x'),sig(2,10,30)),
                             (sig(1,10,30,b'x'),sig(1,20,30)),
                             (sig(1,10,20,b'x'),sig(1,10,30))]:
            with self.subTest(first=first,second=second):
                prefix=rr((),48,b'key')
                parse_snapshot(prefix+rr((),46,first)+rr((),46,second))
                with self.assertRaises(Fault) as cm:
                    parse_snapshot(prefix+rr((),46,second)+rr((),46,first))
                self.assertEqual(cm.exception.code,'SNAPSHOT_FORMAT')

    def test_schema_invalid_headers_are_excluded_from_all_anchor_checks(self):
        b,t,c=make_fixture()
        for height,value,expected_time in [('0120',b['layers'][0]['headers']['120'],'2026-10-14T12:00:00Z'),
                                            ('999','GG'*80,'2026-10-14T12:00:00Z'),
                                            ('120','00',None),('110',None,'2026-10-14T12:00:00Z'),
                                            ('100',False,'2026-10-14T12:00:00Z')]:
            with self.subTest(height=height,value=value):
                bundle=copy.deepcopy(b); bundle['layers'][0]['headers'][height]=value
                report,ledger=verify_bundle(jcs(bundle),parse_trust(jcs(t)),parse_catalog(jcs(c)),diagnostics=True)
                self.assertEqual((report['verdict'],report['reason']),('INVALID','CONTAINER_SCHEMA'))
                self.assertEqual(report['T'],expected_time)
                self.assertFalse(any(check.row.startswith('10.') and check.status!='pass' for check in ledger.checks))

    def test_sort_fallback_preserves_each_available_field(self):
        raw=b'\x00\x30\x0d\x00'+bytes(4)+(30).to_bytes(4,'big')+(20).to_bytes(4,'big')
        self.assertEqual(rrsig_order(raw),(0,20,30,b'',raw,b''))
        short=raw[:12]
        self.assertEqual(rrsig_order(short),(0,0,30,b'',short,b''))
        # A malformed signer cannot hide the fixed-width selector or times.
        broken=raw+b'\x00\x07\x03x'
        self.assertEqual(rrsig_order(broken),(7,20,30,b'',broken,b''))
