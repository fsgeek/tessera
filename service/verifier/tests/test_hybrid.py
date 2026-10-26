"""Independent synthetic hybrid tests; no project vectors or other implementations."""
import copy
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from fixtures import make_fixture,enc,sign,stamp,write_test_release
from tessera_verify import codec
from tessera_verify.codec import ALG,Fault,b64,frame,jcs,parse_signature,public_key,read_anchor,shahex,signature_verifies,utc
from tessera_verify.policy import parse_catalog,parse_trust
from tessera_verify.verify import verify_bundle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec,mldsa
from tessera_verify import sha1dc

PAIR='KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256'
HYBRID_CODECS=codec.registered_codecs(PAIR)
PREFIX=bytes.fromhex('308207b2300b0609608648016503040312038207a100')
POSITIVE=('VALID_STRICT','OK')   # the detector's presence is a startup condition (conftest applies install.json)

def evaluate(b,t,c):
    return verify_bundle(jcs(b),parse_trust(jcs(t)),parse_catalog(jcs(c)),diagnostics=True)

def faults(ledger): return [(c.row,c.reason) for c in ledger.checks if c.status in ('invalid','unknown')]

def anchor_bytes(items):
    raw=b'\x1d'+b'tessera-v1/receipt-anchor-sig'+b'\x02'
    for document,signature in items:
        raw+=len(document).to_bytes(4,'big')+document+len(signature).to_bytes(4,'big')+signature
    return raw

class HybridCodecTests(unittest.TestCase):
    def code(self,expected,fn,*args):
        with self.assertRaises(Fault) as cm: fn(*args)
        self.assertEqual(cm.exception.code,expected)

    def test_default_codec_registry_is_baseline_only(self):
        for slot in ('kms','gpg'):
            self.assertIsNone(parse_signature(b'\xc2'*65536,PAIR,slot))
            self.code('LENGTH_CAP',parse_signature,bytes(65537),PAIR,slot)
            self.code('SIG_PACKET',parse_signature,b'\xc2\x00',ALG,slot)
        b,_,_=make_fixture(hybrid=True)
        self.assertTrue(all(f[3] is None for f in read_anchor(b64(b['layers'][0]['a_sig']))))

    def test_raw_length_only_codec_and_slot_rules(self):
        # Every 3309-byte string is codec-valid, including invalid FIPS encodings.
        for raw in (bytes(3309),b'\xff'*3309):
            self.assertEqual(parse_signature(raw,PAIR,'kms',HYBRID_CODECS),raw)
        for n,reason in ((0,'SIG_EMPTY'),(1,'SIG_FORMAT'),(3308,'SIG_FORMAT'),(3310,'LENGTH_CAP'),(6618,'LENGTH_CAP')):
            self.code(reason,parse_signature,bytes(n),PAIR,'kms',HYBRID_CODECS)
        key=ec.generate_private_key(ec.SECP256R1()); packet=sign(key,b'frame')
        self.assertIsInstance(parse_signature(packet,PAIR,'gpg',HYBRID_CODECS),codec.Signature)
        self.code('SIG_FORMAT',parse_signature,packet,PAIR,'kms',HYBRID_CODECS)
        self.code('LENGTH_CAP',parse_signature,bytes(3309),PAIR,'gpg',HYBRID_CODECS)
        self.code('LENGTH_CAP',parse_signature,bytes(3309),ALG,'kms')
        self.assertIsNone(parse_signature(b'x'*3310,'UNKNOWN','kms'))
        self.code('LENGTH_CAP',parse_signature,bytes(65537),'UNKNOWN','kms')

    def test_exact_spki_and_parameter_sets(self):
        key=mldsa.MLDSA65PrivateKey.generate().public_key()
        der=key.public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
        self.assertEqual(der,PREFIX+key.public_bytes_raw())
        self.assertEqual(public_key(der,'kms',PAIR).public_bytes_raw(),key.public_bytes_raw())
        self.code('KEY_FORMAT',public_key,der,'kms',ALG)
        variants=[der[:-1],der+b'x',der[22:],b'-----BEGIN PUBLIC KEY-----',
                  der[:21]+b'\x01'+der[22:],der[:14]+b'\x11'+der[15:],
                  bytes.fromhex('308207b4300d06096086480165030403120500038207a100')+der[22:],
                  bytes.fromhex('30830707b2300b0609608648016503040312038207a100')+der[22:],
                  b'\x30\x80'+der[4:]+b'\x00\x00']
        for kind in (mldsa.MLDSA44PrivateKey,mldsa.MLDSA87PrivateKey):
            variants.append(kind.generate().public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo))
        variants.append(codec.SPKI+b'\x04'+bytes(64))
        for raw in variants:
            with self.subTest(length=len(raw)): self.code('KEY_FORMAT',public_key,raw,'kms',PAIR)
        # All raw 1952-byte strings have well-formed pkDecode fields.
        for raw in (bytes(1952),b'\xff'*1952):
            self.assertEqual(public_key(PREFIX+raw,'kms',PAIR).public_bytes_raw(),raw)

    def test_anchor_lengths_and_each_frames_own_codec(self):
        b,_,_=make_fixture(hybrid=True)
        frames=read_anchor(b64(b['layers'][0]['a_sig']),HYBRID_CODECS)
        items=[(f[0],f[2]) for f in frames]
        for n,reason in ((0,'SIG_EMPTY'),(3308,'SIG_FORMAT'),(3310,'LENGTH_CAP')):
            self.code(reason,read_anchor,anchor_bytes([(items[0][0],bytes(n)),items[1]]),HYBRID_CODECS)
        self.code('TRUNCATED',read_anchor,anchor_bytes(items)[:len(items[0][0])+45],HYBRID_CODECS)
        # The second frame's classical id selects rule O despite the first's R.
        second=copy.deepcopy(frames[1][1]); second['common']['alg']=ALG
        mixed=[items[0],(frame('tessera-v1/attest',jcs(second)),items[1][1])]
        self.assertIsInstance(read_anchor(anchor_bytes(mixed),HYBRID_CODECS)[1][3],codec.Signature)
        self.code('SIG_PACKET',read_anchor,anchor_bytes([items[0],(mixed[1][0],b'\xc2\x00')]),HYBRID_CODECS)

    def test_pure_empty_context_external_mu_and_wrong_modes(self):
        key=mldsa.MLDSA65PrivateKey.generate(); pub=public_key(PREFIX+key.public_key().public_bytes_raw(),'kms',PAIR)
        document=frame('tessera-v1/manifest',b'{}')+b'x'*5000
        tr=hashlib.shake_256(key.public_key().public_bytes_raw()).digest(64)
        mu=hashlib.shake_256(tr+b'\x00\x00'+document).digest(64)
        signatures=[key.sign(document,context=b''),key.sign_mu(mu)]
        for sig in signatures:
            self.assertTrue(signature_verifies(document,parse_signature(sig,PAIR,'kms',HYBRID_CODECS),pub))
            self.assertFalse(signature_verifies(document+b'x',sig,pub))
            self.assertFalse(signature_verifies(mu,sig,pub))
        # FIPS 204 Algorithm 4: HashML-DSA with SHA-256's DER OID.
        wrong_hash_message=b'\x01\x00'+bytes.fromhex('0609608648016503040201')+hashlib.sha256(document).digest()
        bad=[key.sign(document,context=b'tessera-v1'),key.sign(mu),
             key.sign_mu(hashlib.shake_256(tr+document).digest(64)),
             key.sign_mu(hashlib.shake_256(tr+wrong_hash_message).digest(64))]
        for sig in bad: self.assertFalse(signature_verifies(document,sig,pub))

    def test_strict_encoding_before_backend_verification(self):
        # A permissive backend must never accept malformed hint or z encodings.
        backend=Mock(); backend.verify.return_value=None
        z=int.from_bytes(b'\x00'*3200,'little')
        for i in range(1280): z|=(1<<19)<<(20*i)  # coefficients zero
        base=bytes(48)+z.to_bytes(3200,'little')+bytes(61)
        self.assertTrue(signature_verifies(b'frame',base,backend))
        variants=[]
        for indices,counts in ((b'\x07\x07',[2]*6),(b'\x08\x07',[2]*6),(b'',[56]*6),(b'\x07\x08',[2,1,2,2,2,2])):
            variants.append(base[:3248]+indices+bytes(55-len(indices))+bytes(counts))
        variants.append(base[:3248]+b'\x01'+bytes(60))  # nonzero unused padding
        for coefficient in ((1<<19)-196,-((1<<19)-196)):
            bits=(z&~((1<<20)-1))|((1<<19)-coefficient)
            variants.append(bytes(48)+bits.to_bytes(3200,'little')+bytes(61))
        variants.extend([base[:-1],base+b'x'])
        backend.verify.reset_mock()
        for sig in variants:
            with self.subTest(tail=sig[-61:].hex()): self.assertFalse(signature_verifies(b'frame',sig,backend))
        backend.verify.assert_not_called()
        # Same index in different polynomials is legal; per-polynomial order only.
        legal=base[:3248]+b'\x07\x07'+bytes(53)+bytes([1,2,2,2,2,2])
        self.assertTrue(signature_verifies(b'frame',legal,backend))

class HybridProfileTests(unittest.TestCase):
    def test_complete_hybrid_and_fingerprint(self):
        b,t,c=make_fixture(hybrid=True,common_overrides={'content':{'large':'x'*5000}})
        result,ledger=evaluate(b,t,c)
        self.assertEqual((result['verdict'],result['reason']),POSITIVE)
        self.assertEqual(result['T'],'2026-10-14T12:00:00Z')
        self.assertEqual(faults(ledger),[])
        frames=read_anchor(b64(b['layers'][0]['a_sig']),HYBRID_CODECS)
        self.assertGreater(len(frames[0][0]),4096)
        self.assertEqual(frames[0][1]['signer']['key_fp'],'spki-sha256:'+shahex(b64(b['layers'][0]['keys']['kms'])))
        self.assertTrue(all(any(c.row==row and c.status=='pass' for c in ledger.checks) for row in ('5.1','5.2','9.2','9.5')))

    def test_wrong_installation_skips_key_and_signature_semantics(self):
        for hybrid in (False,True):
            b,t,c=make_fixture(hybrid=hybrid); c['alg']=ALG if hybrid else PAIR
            for bad_keys in (False,True):
                sample=copy.deepcopy(b)
                if bad_keys: sample['layers'][0]['keys']={'kms':enc(b'bad key'),'gpg':enc(b'bad key')}
                result,ledger=evaluate(sample,t,c)
                self.assertEqual((result['verdict'],result['reason']),('UNVERIFIABLE','ALG_UNKNOWN'))
                self.assertFalse(any(c.row in ('5.1','5.2','9.1','9.2','9.4','9.5') for c in ledger.checks))
                self.assertEqual(result['T'],'2026-10-14T12:00:00Z')

    def test_unknown_algorithm_skips_semantics_but_keeps_independent_checks(self):
        b,t,c=make_fixture(common_overrides={'alg':'UNKNOWN'},manifest_overrides={'alg':'UNKNOWN'})
        b['layers'][0]['keys']={'kms':enc(b'bad'),'gpg':enc(b'bad')}
        b['layers'][0]['possession']={'kms':enc(b'opaque'),'gpg':enc(b'opaque')}
        result,ledger=evaluate(b,t,c)
        self.assertEqual((result['verdict'],result['reason']),('UNVERIFIABLE','ALG_UNKNOWN'))
        self.assertFalse(any(c.row in ('5.1','5.2','9.1','9.2','9.4','9.5') for c in ledger.checks))
        b['layers'][0]['spec']=enc(b'wrong object')
        result,_=evaluate(b,t,c); self.assertEqual((result['verdict'],result['reason']),('INVALID','BUNDLE_OBJECT_HASH'))

    def test_unselected_codec_known_id_still_enforces_its_codec(self):
        # Classical is in the baseline, even in a hybrid installation.
        for slot in ('kms','gpg'):
            b,t,c=make_fixture(); c['alg']=PAIR
            b['layers'][0]['possession'][slot]=enc(b'\xc2\x00')
            result,_=evaluate(b,t,c)
            self.assertEqual((result['verdict'],result['reason']),('INVALID','SIG_PACKET'))
            frames=read_anchor(b64(b['layers'][0]['a_sig']))
            items=[(f[0],f[2]) for f in frames]; i=('kms','gpg').index(slot)
            items[i]=(items[i][0],b'\xc2\x00'); b['layers'][0]['a_sig']=enc(anchor_bytes(items))
            result,ledger=evaluate(b,t,c)
            self.assertEqual((result['verdict'],result['reason']),('INVALID','SIG_PACKET'))
            self.assertIn(('3.1','SIG_PACKET'),faults(ledger))

    def test_fallback_hybrid_receipt_uses_opaque_slots(self):
        # A compiled hybrid decoder must not impose R/O rules on fallback.
        b,t,c=make_fixture(hybrid=True); c['alg']=ALG
        frames=read_anchor(b64(b['layers'][0]['a_sig']),HYBRID_CODECS)
        for i,slot in enumerate(('kms','gpg')):
            for n,verdict,reason in ((0,'INVALID','SIG_EMPTY'),
                                     (1,'UNVERIFIABLE','ALG_UNKNOWN'),
                                     (3308,'UNVERIFIABLE','ALG_UNKNOWN'),
                                     (3310,'UNVERIFIABLE','ALG_UNKNOWN'),
                                     (65536,'UNVERIFIABLE','ALG_UNKNOWN'),
                                     (65537,'INVALID','LENGTH_CAP')):
                with self.subTest(slot=slot,n=n):
                    sample,trust=copy.deepcopy((b,t))
                    items=[(f[0],f[2]) for f in frames]; items[i]=(items[i][0],b'\xc2'*n)
                    raw=anchor_bytes(items); layer=sample['layers'][0]; layer['a_sig']=enc(raw)
                    proof,txid=stamp(raw,120,utc('2026-10-14T12:00:00Z'),layer['headers'],trust['header_pins'])
                    layer['receipt_anchor']={'ots':enc(proof),'txid':txid}
                    result,ledger=evaluate(sample,trust,c)
                    self.assertEqual((result['verdict'],result['reason']),(verdict,reason))
                    self.assertEqual(result['T'],'2026-10-14T12:00:00Z')
                    self.assertFalse(any(check.row in ('5.1','5.2','9.1','9.2','9.4','9.5') for check in ledger.checks))
                    if verdict=='INVALID': self.assertIn(('3.1',reason),faults(ledger))

    def test_fallback_hybrid_possession_uses_opaque_slots(self):
        b,t,c=make_fixture(hybrid=True); c['alg']=ALG
        for slot in ('kms','gpg'):
            for n,verdict,reason in ((0,'INVALID','SIG_EMPTY'),
                                     (1,'UNVERIFIABLE','ALG_UNKNOWN'),
                                     (3308,'UNVERIFIABLE','ALG_UNKNOWN'),
                                     (3310,'UNVERIFIABLE','ALG_UNKNOWN'),
                                     (65536,'UNVERIFIABLE','ALG_UNKNOWN'),
                                     (65537,'INVALID','LENGTH_CAP')):
                with self.subTest(slot=slot,n=n):
                    sample=copy.deepcopy(b); sample['layers'][0]['possession'][slot]=enc(b'\xc2'*n)
                    result,ledger=evaluate(sample,t,c)
                    self.assertEqual((result['verdict'],result['reason']),(verdict,reason))
                    self.assertEqual(result['T'],'2026-10-14T12:00:00Z')
                    self.assertFalse(any(check.row in ('5.1','5.2','9.1','9.2','9.4','9.5') for check in ledger.checks))
                    if verdict=='INVALID': self.assertIn(('9.3',reason),faults(ledger))

    def test_fallback_opaque_cap_checked_before_truncation(self):
        b,t,c=make_fixture(hybrid=True); c['alg']=ALG
        frames=read_anchor(b64(b['layers'][0]['a_sig']),HYBRID_CODECS)
        prefix=b'\x1d'+b'tessera-v1/receipt-anchor-sig'+b'\x02'
        for i,slot in enumerate(('kms','gpg')):
            for n,reason in ((65536,'TRUNCATED'),(65537,'LENGTH_CAP')):
                with self.subTest(slot=slot,n=n):
                    raw=prefix
                    if i: raw+=len(frames[0][0]).to_bytes(4,'big')+frames[0][0]+len(frames[0][2]).to_bytes(4,'big')+frames[0][2]
                    raw+=len(frames[i][0]).to_bytes(4,'big')+frames[i][0]+n.to_bytes(4,'big')
                    sample=copy.deepcopy(b); sample['layers'][0]['a_sig']=enc(raw)
                    result,ledger=evaluate(sample,t,c)
                    self.assertEqual((result['verdict'],result['reason']),('INVALID',reason))
                    self.assertIn(('3.1',reason),faults(ledger))

    def test_fallback_registry_independent_of_spec_lookup(self):
        b,t,c=make_fixture(hybrid=True,kms_signer=lambda k,d:bytes(3308))
        c['alg']=ALG; c['spec_sha256']=shahex(b'other spec')
        result,ledger=evaluate(b,t,c)
        self.assertEqual((result['verdict'],result['reason']),('UNVERIFIABLE','ALG_UNKNOWN'))
        self.assertIn(('8.3','SPEC_UNKNOWN'),faults(ledger))
        self.assertFalse(any(check.row in ('3.1','9.3') and check.status!='pass' for check in ledger.checks))

    def test_registry_selection_is_per_call(self):
        b,t,c=make_fixture(hybrid=True); b['layers'][0]['possession']['kms']=enc(bytes(3308))
        for alg,verdict,reason in ((ALG,'UNVERIFIABLE','ALG_UNKNOWN'),
                                   (PAIR,'INVALID','SIG_FORMAT'),
                                   ('UNKNOWN','UNVERIFIABLE','ALG_UNKNOWN'),
                                   (ALG,'UNVERIFIABLE','ALG_UNKNOWN')):
            with self.subTest(alg=alg):
                catalog=copy.deepcopy(c); catalog['alg']=alg
                result,_=evaluate(b,t,catalog)
                self.assertEqual((result['verdict'],result['reason']),(verdict,reason))

    def test_possession_registry_without_decodable_receipt(self):
        b,t,c=make_fixture(hybrid=True); b['layers'][0]['a_sig']=enc(b'')
        b['layers'][0]['possession']['kms']=enc(bytes(3308))
        for alg,status,reason in ((ALG,'pass',None),(PAIR,'invalid','SIG_FORMAT')):
            with self.subTest(alg=alg):
                catalog=copy.deepcopy(c); catalog['alg']=alg
                _,ledger=evaluate(b,t,catalog)
                checks=[check for check in ledger.checks if check.row=='9.3']
                self.assertEqual((checks[0].status,checks[0].reason),(status,reason))

    def test_supported_key_format_precedes_fingerprint(self):
        for hybrid in (False,True):
            b,t,c=make_fixture(hybrid=hybrid); b['layers'][0]['keys']['kms']=enc(b'bad')
            result,_=evaluate(b,t,c); self.assertEqual(result['reason'],'KEY_FORMAT')
        b,t,c=make_fixture(hybrid=True)
        other=mldsa.MLDSA65PrivateKey.generate().public_key()
        b['layers'][0]['keys']['kms']=enc(PREFIX+other.public_bytes_raw())
        result,_=evaluate(b,t,c); self.assertEqual(result['reason'],'KEY_MISMATCH')
        b,t,c=make_fixture(); b['layers'][0]['keys']['kms']=enc(PREFIX+other.public_bytes_raw())
        result,_=evaluate(b,t,c); self.assertEqual(result['reason'],'KEY_FORMAT')

    def test_supported_unknown_spec_still_verifies(self):
        b,t,c=make_fixture(hybrid=True); c['spec_sha256']=shahex(b'other spec')
        result,ledger=evaluate(b,t,c)
        self.assertEqual(result['reason'],'SPEC_UNKNOWN')
        self.assertTrue(all(any(c.row==row and c.status=='pass' for c in ledger.checks) for row in ('5.1','9.2','9.5')))

    def test_internal_malformation_is_verification_not_codec_failure(self):
        def duplicate(k,d):
            s=k.sign(d); return s[:3248]+b'\x07\x07'+bytes(53)+bytes([2]*6)
        for possession in (False,True):
            kwargs={'kms_possession_signer':duplicate} if possession else {'kms_signer':duplicate}
            b,t,c=make_fixture(hybrid=True,**kwargs); result,ledger=evaluate(b,t,c)
            self.assertEqual(result['reason'],'POSSESSION_INVALID' if possession else 'SIG_INVALID')
            self.assertFalse(any(row in ('3.1','9.3') for row,_ in faults(ledger)))

    def test_wrong_context_and_mode_receipt_and_possession(self):
        def hash_mode(k,d):
            representative=b'\x01\x00'+bytes.fromhex('0609608648016503040201')+hashlib.sha256(d).digest()
            tr=hashlib.shake_256(k.public_key().public_bytes_raw()).digest(64)
            return k.sign_mu(hashlib.shake_256(tr+representative).digest(64))
        for possession in (False,True):
            for signing in (lambda k,d:k.sign(d,context=b'tessera-v1'),lambda k,d:k.sign_mu(hashlib.shake_256(hashlib.shake_256(k.public_key().public_bytes_raw()).digest(64)+d).digest(64)),hash_mode):
                kwargs={'kms_possession_signer':signing} if possession else {'kms_signer':signing}
                b,t,c=make_fixture(hybrid=True,**kwargs); result,_=evaluate(b,t,c)
                self.assertEqual(result['reason'],'POSSESSION_INVALID' if possession else 'SIG_INVALID')

    def test_another_valid_signature_still_fails_original_anchor(self):
        alternative=[]
        def capture(k,d):
            alternative.append(k.sign(d)); return k.sign(d)
        b,t,c=make_fixture(hybrid=True,kms_signer=capture)
        frames=read_anchor(b64(b['layers'][0]['a_sig']),HYBRID_CODECS)
        self.assertNotEqual(alternative[0],frames[0][2])
        b['layers'][0]['a_sig']=enc(anchor_bytes([(frames[0][0],alternative[0]),(frames[1][0],frames[1][2])]))
        result,ledger=evaluate(b,t,c)
        self.assertEqual(result['reason'],'RECEIPT_ANCHOR_MISMATCH'); self.assertIsNone(result['T'])
        self.assertFalse(any(row=='9.2' for row,_ in faults(ledger)))

    def test_both_slot_possession_proofs_bind_exact_manifest(self):
        b,t,c=make_fixture(hybrid=True)
        frames=read_anchor(b64(b['layers'][0]['a_sig']),HYBRID_CODECS)
        for i,slot in enumerate(('kms','gpg')):
            sample=copy.deepcopy(b); sample['layers'][0]['possession'][slot]=enc(frames[i][2])
            result,_=evaluate(sample,t,c)
            self.assertEqual(result['reason'],'POSSESSION_INVALID')

    def test_mixed_pair_common_values_rejected(self):
        b,t,c=make_fixture(hybrid=True,gpg_common_overrides={'alg':ALG})
        result,_=evaluate(b,t,c); self.assertEqual(result['reason'],'RECEIPT_COMMON_MISMATCH')

    def test_cli_installed_codec_registry(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary); b,t,c=make_fixture(hybrid=True)
            for name,obj in (('bundle',b),('trust',t)): (root/(name+'.json')).write_bytes(jcs(obj))
            for alg in (PAIR,ALG):
                catalog=copy.deepcopy(c); catalog['alg']=alg
                (root/'catalog.json').write_bytes(jcs(catalog))
                command=[sys.executable,'-m','tessera_verify']+write_test_release(root,t,catalog,'rel-'+str(alg=='PAIR'))+['--trust',str(root/'trust.json'),'--bundle',str(root/'bundle.json')]
                for length,expected in ((None,POSITIVE if alg==PAIR else ('UNVERIFIABLE','ALG_UNKNOWN')),
                                         (3308,('INVALID','SIG_FORMAT') if alg==PAIR else ('UNVERIFIABLE','ALG_UNKNOWN')),
                                         (65537,('INVALID','LENGTH_CAP'))):
                    sample=copy.deepcopy(b)
                    if length is not None: sample['layers'][0]['possession']['kms']=enc(bytes(length))
                    (root/'bundle.json').write_bytes(jcs(sample))
                    for suffix in ([],['--catalog',str(root/'catalog.json')]):
                        with self.subTest(alg=alg,length=length,suffix=suffix):
                            run=subprocess.run(command+suffix,capture_output=True)
                            self.assertEqual(run.returncode,0,run.stderr.decode())
                            whole=codec.parse_json(run.stdout.strip(),canonical=True)
                            self.assertEqual(set(whole),{'stable','utc_assessment'}); result=whole['stable']
                            self.assertEqual((result['verdict'],result['reason']),expected); self.assertEqual(len(result),6)
