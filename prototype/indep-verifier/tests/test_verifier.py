import copy
import subprocess
import tempfile
import unittest
from pathlib import Path
from fixtures import make_fixture,enc,stamp,rrset,dnskey,gpgkey,sign
from codec import ALG,Fault,b64,jcs,parse_signature,public_key,sig_policy,shahex,utc
from policy import parse_trust,parse_catalog,check_extension
from verify import verify_bundle,Ledger
from anchors import parse_ots,select,tx_path,sha256d
from dnssec import parse_snapshot,validate_snapshot,root_auth,keytag,Group,RR,Auth,group_auth,wire
from cryptography.hazmat.primitives.asymmetric import ec
import sha1dc
# Row 14.4: with the owner-pinned SHA-1DC built (sha1dc.py), a complete honest bundle is VALID_STRICT.
POSITIVE=('VALID_STRICT','OK') if sha1dc.available() else ('UNVERIFIABLE','INDEPENDENT_SHA1DC_UNAVAILABLE')

class VerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.base,cls.trust,cls.catalog=make_fixture()
    def run_bundle(self,bundle=None,trust=None,catalog=None):
        return verify_bundle(jcs(bundle or self.base),parse_trust(jcs(trust or self.trust)),parse_catalog(jcs(catalog or self.catalog)),diagnostics=True)
    def test_synthetic_all_available_checks(self):
        report,ledger=self.run_bundle()
        self.assertEqual((report['verdict'],report['reason']),POSITIVE)
        self.assertEqual(report['T'],'2026-10-14T12:00:00Z')
        failures=[(c.row,c.reason) for c in ledger.checks if c.status!='pass']
        self.assertEqual(failures,[] if POSITIVE[0]=='VALID_STRICT' else [('14.4','INDEPENDENT_SHA1DC_UNAVAILABLE')])
        self.assertEqual(len(report),6)
    @unittest.skipUnless(sha1dc.available(),'pinned SHA-1DC not built')
    def test_sha1dc_hook_frames_and_reports(self):
        seen=[]; original=sha1dc.collision
        def fake(kind,body): seen.append(kind); return kind=='blob'
        sha1dc.collision=fake
        try: report,ledger=self.run_bundle()
        finally: sha1dc.collision=original
        self.assertEqual(seen,['commit','tree','tree','blob'])
        self.assertEqual((report['verdict'],report['reason']),('INVALID','GIT_SHA1_COLLISION'))
        self.assertFalse(original('blob',b'hello\n'))
    def test_missing_evidence_not_schema(self):
        b=copy.deepcopy(self.base); del b['layers'][0]['git']
        report,_=self.run_bundle(b)
        self.assertEqual(report['reason'],'MEMBER_MISSING:git'); self.assertEqual(report['verdict'],'UNVERIFIABLE')
        self.assertIsNotNone(report['T'])
    def test_invalid_dominates_missing_and_keeps_T(self):
        b=copy.deepcopy(self.base); del b['layers'][0]['git']; b['layers'][0]['spec']=enc(b'wrong spec')
        report,_=self.run_bundle(b)
        self.assertEqual(report['reason'],'BUNDLE_OBJECT_HASH'); self.assertEqual(report['verdict'],'INVALID')
        self.assertIsNotNone(report['T'])
    def test_wrong_parent_no_synthesized_children(self):
        b=copy.deepcopy(self.base); b['layers'][0]['git']=None
        report,ledger=self.run_bundle(b)
        self.assertEqual(report['reason'],'CONTAINER_SCHEMA')
        self.assertFalse(any(c.reason and c.reason.startswith('MEMBER_MISSING:git.') for c in ledger.checks))
    def test_object_format_absence_and_null(self):
        for value,expected in [('absent','GIT_OBJECT_FORMAT_MISSING'),(None,'CONTAINER_SCHEMA'),('sha256','GIT_OBJECT_FORMAT')]:
            b=copy.deepcopy(self.base)
            if value=='absent': del b['layers'][0]['git']['object_format']
            else: b['layers'][0]['git']['object_format']=value
            report,_=self.run_bundle(b); self.assertEqual(report['reason'],expected)
    def test_bad_receipt_signature_does_not_suppress_T(self):
        b=copy.deepcopy(self.base); raw=bytearray(b64(b['layers'][0]['a_sig'])); raw[-1]^=1
        b['layers'][0]['a_sig']=enc(raw)
        headers=b['layers'][0]['headers']; pins=copy.deepcopy(self.trust['header_pins'])
        ots,txid=stamp(raw,120,utc('2026-10-14T12:00:00Z'),headers,pins)
        b['layers'][0]['receipt_anchor']={'ots':enc(ots),'txid':txid}
        trust=copy.deepcopy(self.trust); trust['header_pins']=pins
        report,_=self.run_bundle(b,trust)
        self.assertEqual(report['reason'],'SIG_INVALID'); self.assertIsNotNone(report['T'])
    def test_digest_mismatch_clears_T(self):
        b=copy.deepcopy(self.base); raw=bytearray(b64(b['layers'][0]['receipt_anchor']['ots'])); raw[len(__import__('anchors').MAGIC)+2]^=1
        b['layers'][0]['receipt_anchor']['ots']=enc(raw)
        report,_=self.run_bundle(b)
        self.assertEqual(report['verdict'],'INVALID'); self.assertIsNone(report['T'])
    def test_txid_failure_keeps_T(self):
        b=copy.deepcopy(self.base); b['layers'][0]['receipt_anchor']['txid']='0'*64
        report,_=self.run_bundle(b); self.assertEqual(report['reason'],'ANCHOR_TXID_MISMATCH'); self.assertIsNotNone(report['T'])
    def test_header_conflict_and_unused_unpinned(self):
        b=copy.deepcopy(self.base); raw=bytearray.fromhex(b['layers'][0]['headers']['100']); raw[-1]=1; b['layers'][0]['headers']['100']=raw.hex()
        report,_=self.run_bundle(b); self.assertEqual(report['reason'],'HEADER_CONFLICTS_PIN')
        b=copy.deepcopy(self.base); b['layers'][0]['headers']['999']='0'*160
        report,_=self.run_bundle(b); self.assertEqual(report['reason'],'HEADERS_NOT_COVERED'); self.assertIsNotNone(report['T'])
    def test_chain_precommit(self):
        b=copy.deepcopy(self.base); trust=copy.deepcopy(self.trust)
        commit=b64(b['layers'][0]['git']['commit']); oid=__import__('git_channel').object_id('commit',commit)
        proof,_=stamp((oid+'\n').encode(),130,utc('2026-10-14T12:00:00Z'),b['layers'][0]['headers'],trust['header_pins'])
        b['layers'][0]['git']['ots']=enc(proof)
        report,_=self.run_bundle(b,trust); self.assertEqual(report['reason'],'GIT_NOT_PRECOMMITTED')
    def test_noncanonical_dispatch_and_number_member(self):
        config=parse_trust(jcs(self.trust)); catalog=parse_catalog(jcs(self.catalog))
        report=verify_bundle(b' '+jcs(self.base),config,catalog)
        self.assertEqual(report['reason'],'JSON_NONCANONICAL')
        b=copy.deepcopy(self.base); b['layers'][0]['a_sig']='PLACEHOLDER'
        raw=jcs(b).replace(b'"PLACEHOLDER"',b'1000')
        report=verify_bundle(raw,config,catalog); self.assertEqual(report['reason'],'CONTAINER_SCHEMA')
        for raw in [b'NaN',b'{}',b'{"profile":"unknown","layers":[]}']:
            self.assertEqual(verify_bundle(raw,config,catalog)['reason'],'OUT_OF_PROFILE')
    def test_ledger_order_independent(self):
        checks=[('17.1',False,'BUNDLE_OBJECT_HASH',(),False),('2.2',False,'MEMBER_MISSING:git',(),True),('9.5',False,'POSSESSION_INVALID',(1,),False)]
        for sequence in (checks,list(reversed(checks))):
            l=Ledger()
            for c in sequence: l.add(*c)
            self.assertEqual(l.report(None)['reason'],'POSSESSION_INVALID')
    def test_signature_policy_metadata(self):
        key=ec.generate_private_key(ec.SECP256R1()); doc=b'document'
        signature=parse_signature(sign(key,doc,hashed=b'\x05\x82'+bytes(4)))
        sig_policy(signature)
        for hashed in [b'',b'\x05\x02'+bytes(4)+b'\x01\xa1',b'\x05\x02'+bytes(4)+b'\x02\x03\x00']:
            with self.assertRaises(Fault) as cm: sig_policy(parse_signature(sign(key,doc,hashed=hashed)))
            self.assertEqual(cm.exception.code,'SIG_POLICY')
    def test_public_key_point(self):
        with self.assertRaises(Fault): public_key(bytes.fromhex('3059301306072a8648ce3d020106082a8648ce3d030107034200')+b'\x04'+bytes(64),'kms')
    def test_root_existential_and_horizon(self):
        config=parse_trust(jcs(self.trust)); snapshot=parse_snapshot(b64(self.base['layers'][0]['dns']['snapshot_body'])); t=utc('2026-10-14T12:00:00Z')
        self.assertTrue(all(a.status=='pass' for a in validate_snapshot(snapshot,config,t)))
        config['as_of']='2026-10-14T11:00:00Z'
        self.assertEqual(root_auth(snapshot.group((),48),config,t).reason,'TRUST_HORIZON')
        config['root_ksks'][0]['signing_end']='2026-09-01T00:00:00Z'
        self.assertEqual(root_auth(snapshot.group((),48),config,t).reason,'KSK_OUTSIDE_RELIANCE_PERIOD')
    def test_trust_and_catalog_closure(self):
        for key in ['unexpected','signer']:
            t=copy.deepcopy(self.trust); t[key]='x'
            with self.assertRaises(Fault) as cm: parse_trust(jcs(t))
            self.assertEqual(cm.exception.code,'TRUST_CONFIG_UNAUTHENTICATED')
        c=copy.deepcopy(self.catalog); c['entries'][0]['k']='7'
        with self.assertRaises(Fault): parse_catalog(jcs(c))
        for f,v in (('utc_delta_s','7201'),('utc_m','5')):   # A10.1.1: catalog must equal the built-in check values
            c=copy.deepcopy(self.catalog); c['entries'][0][f]=v
            with self.assertRaises(Fault): parse_catalog(jcs(c))
        c=copy.deepcopy(self.catalog); del c['entries'][0]['utc_m']
        with self.assertRaises(Fault): parse_catalog(jcs(c))
    def test_append_only(self):
        old=parse_trust(jcs(self.trust)); new=copy.deepcopy(self.trust)
        new['version']='2'; new['previous_sha256']=shahex(jcs(self.trust))
        check_extension(old,parse_trust(jcs(new)),jcs(self.trust))
        del new['header_pins']['100']
        with self.assertRaises(Fault): check_extension(old,parse_trust(jcs(new)),jcs(self.trust))
    def test_no_config_auto_trust(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as path:
            trust=Path(path)/'trust.json'; bundle=Path(path)/'bundle.json'
            trust.write_bytes(jcs(self.trust)); bundle.write_bytes(jcs(self.base))
            proc=subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'verify.py'),'--trust',str(trust),'--bundle',str(bundle)],capture_output=True)
            self.assertEqual(proc.returncode,2); self.assertEqual(proc.stdout,b''); self.assertIn(b'TRUST_CONFIG_UNAUTHENTICATED',proc.stderr)

import sys
if __name__=='__main__': unittest.main()

class TemporalAndCliTests(unittest.TestCase):
    def test_three_receipt_conjuncts(self):
        for delta,confirmation,reason in [(-86401,None,'TIME_BEFORE_DECLARED_EPSILON'),(259201,None,'TIME_AFTER_DECLARED_DELTA'),(0,259201,'CONFIRMATION_LATE')]:
            b,t,c=make_fixture(); base=utc('2026-10-14T12:00:00Z')
            proof,txid=stamp(b64(b['layers'][0]['a_sig']),120,base+delta,b['layers'][0]['headers'],t['header_pins'],None if confirmation is None else base+confirmation)
            b['layers'][0]['receipt_anchor']={'ots':enc(proof),'txid':txid}
            report=verify_bundle(jcs(b),parse_trust(jcs(t)),parse_catalog(jcs(c)))
            self.assertEqual(report['reason'],reason)
    def test_snapshot_confirmation_conjunct(self):
        b,t,c=make_fixture(); layer=b['layers'][0]; body=b64(layer['dns']['snapshot_body']); envelope=b'\x1a'+b'tessera-v1/dnssec-snapshot'+len(body).to_bytes(4,'big')+body
        proof,_=stamp(envelope,110,utc('2026-10-14T12:00:00Z'),layer['headers'],t['header_pins'],utc('2026-10-17T12:00:01Z'))
        layer['dns']['ots']=enc(proof)
        report=verify_bundle(jcs(b),parse_trust(jcs(t)),parse_catalog(jcs(c)))
        self.assertEqual(report['reason'],'SNAPSHOT_TIME')
    def test_cli_provisioning_and_config_refusal(self):
        directory=Path(__file__).resolve().parents[1]; constants=directory/'release_constants.py'; original=constants.read_bytes()
        try:
            with tempfile.TemporaryDirectory(dir=directory) as temporary:
                root=Path(temporary); b,t,c=make_fixture()
                for name,obj in [('bundle',b),('trust',t),('catalog',c)]: (root/(name+'.json')).write_bytes(jcs(obj))
                build=subprocess.run([sys.executable,str(directory/'build_release.py'),'--trust',str(root/'trust.json'),'--catalog',str(root/'catalog.json')],capture_output=True)
                self.assertEqual(build.returncode,0,build.stderr.decode())
                command=[sys.executable,str(directory/'verify.py'),'--trust',str(root/'trust.json'),'--bundle',str(root/'bundle.json')]
                for suffix in [[],['--catalog',str(root/'catalog.json')]]:
                    run=subprocess.run(command+suffix,capture_output=True)
                    self.assertEqual(run.returncode,0,run.stderr.decode()); self.assertEqual(run.stderr,b'')
                    from codec import parse_json
                    whole=parse_json(run.stdout.strip(),canonical=True)
                    self.assertEqual(set(whole),{'stable','utc_assessment'}); report=whole['stable']
                    self.assertEqual(set(report),{'verdict','reason','T','revocation','historical_security','standing'})
                    self.assertEqual(report['reason'],POSITIVE[1])
                t['as_of']='2026-10-21T00:00:00Z'; (root/'trust.json').write_bytes(jcs(t))
                refused=subprocess.run(command,capture_output=True)
                self.assertEqual(refused.returncode,2); self.assertEqual(refused.stdout,b'')
                self.assertEqual(refused.stderr.strip(),b'TRUST_CONFIG_UNAUTHENTICATED')
        finally: constants.write_bytes(original)

class ConsistencyAndWindowTests(unittest.TestCase):
    def check(self,reason,**kwargs):
        b,t,c=make_fixture(**kwargs)
        report,ledger=verify_bundle(jcs(b),parse_trust(jcs(t)),parse_catalog(jcs(c)),diagnostics=True)
        self.assertEqual(report['reason'],reason)
        return report,ledger
    def test_manifest_digest_and_tuple(self):
        self.check('RECEIPT_MANIFEST_MISMATCH',common_overrides={'manifest_sha256':'0'*64})
        self.check('RECEIPT_MANIFEST_MISMATCH',manifest_overrides={'alg':'OTHER'})
    def test_common_byte_equality(self):
        self.check('RECEIPT_COMMON_MISMATCH',gpg_common_overrides={'content':{'contract':'different'}})
    def test_pinned_issuer_before_missing_authority(self):
        self.check('ISSUER_NOT_PINNED',common_overrides={'issuer':'evil.com'},manifest_overrides={'issuer':'evil.com'})
    def test_unknown_alg_uses_opaque_codec(self):
        report,_=self.check('ALG_UNKNOWN',common_overrides={'alg':'UNKNOWN'},manifest_overrides={'alg':'UNKNOWN'})
        self.assertEqual(report['verdict'],'UNVERIFIABLE')
    def test_binding_forms(self):
        self.check('BINDING_FORM_UNSUPPORTED',common_overrides={'binding_forms':['STMT_DIGEST','STMT_DIRECT']})
        self.check('BINDING_FORM_UNKNOWN',common_overrides={'binding_forms':['UNKNOWN']})
    def test_window_boundaries(self):
        for kwargs in [{'window_start':'2026-10-14T12:00:00Z'}, {'window_end':'2026-10-14T12:00:00Z'}]:
            _,ledger=self.check(POSITIVE[1],**kwargs)
            self.assertTrue(all(c.status=='pass' for c in ledger.checks if c.row=='16.1'))
        self.check('ISSUANCE_WINDOW',window_start='2026-10-14T12:00:01Z')
        self.check('ISSUANCE_WINDOW',window_end='2026-10-14T11:59:59Z')
    def test_record_window_length(self):
        self.check('DNS_WINDOW_LENGTH',window_start='2026-01-01T00:00:00Z',window_end='2026-10-14T12:00:00Z')
    def test_unknown_spec_independent_object_checks(self):
        for bad_object in [False,True]:
            b,t,c=make_fixture(common_overrides={'spec':{'id':'tessera-v1-strict/verification-spec/1','sha256':shahex(b'new spec')}},objects_overrides={'spec':b'new spec'})
            c['entries'][0]['spec_sha256']=shahex(b'independent test spec')
            b['layers'][0]['dependency_manifest']=enc(b'unmatched dependency bytes')
            if bad_object: b['layers'][0]['preamble']=enc(b'wrong preamble')
            report=verify_bundle(jcs(b),parse_trust(jcs(t)),parse_catalog(jcs(c)))
            self.assertEqual(report['reason'],'BUNDLE_OBJECT_HASH' if bad_object else 'SPEC_UNKNOWN')
    def test_optional_diagnostics_schema(self):
        b,t,c=make_fixture(); b['layers'][0]['issuer_record']={}
        report=verify_bundle(jcs(b),parse_trust(jcs(t)),parse_catalog(jcs(c)))
        self.assertEqual(report['reason'],'CONTAINER_SCHEMA')

class MutationTests(unittest.TestCase):
    def test_seeded_malformed_binary_inputs_never_crash(self):
        import random
        b,t,c=make_fixture(); config=parse_trust(jcs(t)); catalog=parse_catalog(jcs(c)); randomizer=random.Random(20261014)
        paths=[('a_sig',),('manifest',),('keys','kms'),('keys','gpg'),('possession','kms'),('possession','gpg'),('receipt_anchor','ots'),('dns','snapshot_body'),('dns','ots'),('git','commit'),('git','blob'),('git','ots')]
        for i in range(180):
            mutated=copy.deepcopy(b); target=mutated['layers'][0]; path=paths[i%len(paths)]
            for component in path[:-1]: target=target[component]
            raw=randomizer.randbytes(randomizer.randrange(0,128)); target[path[-1]]=enc(raw)
            report=verify_bundle(jcs(mutated),config,catalog)
            self.assertEqual(len(report),6)
            self.assertIn(report['verdict'],('INVALID','UNVERIFIABLE'))
