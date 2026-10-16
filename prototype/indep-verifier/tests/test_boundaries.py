import copy
import unittest
from fixtures import make_fixture,rr,rrset,dnskey,stamp,varbytes,varuint
from codec import Fault,parse_json,jcs,sha,utc
from anchors import MAGIC,BTC,parse_ots,select,tx_path,sha256d
from dnssec import parse_snapshot,root_auth,group_auth,validate_snapshot,parse_rrsig,keytag,Group,RR,Auth,wire
from policy import parse_trust
from cryptography.hazmat.primitives.asymmetric import ec

class BoundaryTests(unittest.TestCase):
    def code(self,code,fn,*args):
        with self.assertRaises(Fault) as cm: fn(*args)
        self.assertEqual(cm.exception.code,code)
    def test_deep_json_syntax_then_depth(self):
        self.code('JSON_DEPTH',parse_json,b'['*2000+b'0'+b']'*2000)
        self.code('JSON_SYNTAX',parse_json,b'['*2000+b'0'+b']'*1999)
        for raw in [b'[1,]',b'{"a":1,}',b'01',b'1true',b'{}{}',b'{"a" 1}',b'[1 2]']:
            self.code('JSON_SYNTAX',parse_json,raw)
    def test_json_category_whole_value(self):
        self.code('JSON_DUPLICATE_NAME',parse_json,b'{"bad":"\\ud800","a":0,"a":1}')
        self.code('JSON_STRING',parse_json,b'[9007199254740993,"\\ud800"]')
        self.assertEqual(jcs(parse_json(b'0e99999999999999999999')),b'0')
    def test_ots_non32_bitcoin_and_payload_trailing(self):
        raw=MAGIC+b'\x01\x08'+bytes(32)+b'\xf0\x01x'+b'\x00'+BTC+b'\x01\x01'
        self.code('OTS_FORMAT',parse_ots,raw)
        self.code('OTS_FORMAT',parse_ots,MAGIC+b'\x01\x08'+bytes(32)+b'\x00'+BTC+b'\x02\x01\x00')
    def test_ots_depth_exact(self):
        tail=b'\x00'+BTC+b'\x01\x01'
        self.assertEqual(len(parse_ots(MAGIC+b'\x01\x08'+bytes(32)+b'\x08'*256+tail).bitcoin),1)
        self.code('OTS_FORMAT',parse_ots,MAGIC+b'\x01\x08'+bytes(32)+b'\x08'*257+tail)
    def test_lowest_height_not_lowest_time(self):
        headers={}; pins={}; a,_=stamp(b'x',20,500,headers,pins,400); b,_=stamp(b'x',40,100,headers,pins)
        # ff duplicates the root message and takes both complete operation paths.
        offset=len(MAGIC)+34; proof=a[:offset]+b'\xff'+a[offset:]+b[offset:]
        parsed=parse_ots(proof)
        chosen,bad=select(parsed,{int(h):bytes.fromhex(v) for h,v in headers.items()},{int(h):v for h,v in pins.items()})
        self.assertEqual((chosen.height,chosen.time,chosen.confirmed),(20,500,400)); self.assertFalse(bad)
        self.assertTrue(all(tx_path(att) for att in chosen.paths))
    def test_unselected_incomplete_attestation(self):
        headers={};pins={}; proof,_=stamp(b'x',20,100,headers,pins)
        offset=len(MAGIC)+34
        proof=proof[:offset]+b'\xff'+b'\x00'+BTC+varbytes(varuint(999))+proof[offset:]
        selected,bad=select(parse_ots(proof),{int(h):bytes.fromhex(v) for h,v in headers.items()},{int(h):v for h,v in pins.items()})
        self.assertEqual(selected.height,20); self.assertFalse(bad)
    def test_root_extra_bad_candidate_in_any_order(self):
        b,t,c=make_fixture(); config=parse_trust(jcs(t)); snap=parse_snapshot(__import__('codec').b64(b['layers'][0]['dns']['snapshot_body'])); root=snap.group((),48)
        bad=copy.deepcopy(root.sigs[0]); bad.data=bad.data[:-1]+bytes([bad.data[-1]^1])
        for order in [[bad,root.sigs[0]],[root.sigs[0],bad]]:
            self.assertEqual(root_auth(Group((),48,root.rr,order),config,utc('2026-10-14T12:00:00Z')).status,'pass')
    def test_nonroot_key_selector_and_metadata(self):
        key=ec.generate_private_key(ec.SECP256R1()); kd=dnskey(key); owner=(b'_tessera-v1',b'wamason',b'com'); zone=(b'wamason',b'com'); t=100000
        body=rrset(owner,16,[b'\x01x'],key,kd,zone,t)
        snapshot=parse_snapshot(body); group=snapshot.txt; keys=Group(zone,48,[RR(zone,48,3600,kd,0)],[])
        self.assertEqual(group_auth(group,keys,Auth('pass'),t).status,'pass')
        wrong=bytearray(group.sigs[0].data); wrong[16:18]=((keytag(kd)+1)%65536).to_bytes(2,'big')
        group.sigs=[RR(owner,46,3600,bytes(wrong),0)]
        self.assertEqual(group_auth(group,keys,Auth('pass'),t).reason,'DNSSEC_KEY_MISMATCH')
        wrong[3]=len(owner)+1; group.sigs=[RR(owner,46,3600,bytes(wrong),0)]
        self.assertEqual(group_auth(group,keys,Auth('pass'),t).reason,'DNSSEC_RRSIG_METADATA')
    def test_parent_blocked_locally_good_and_bad(self):
        key=ec.generate_private_key(ec.SECP256R1()); kd=dnskey(key); owner=(b'com',); t=100000
        group=parse_snapshot(rrset(owner,48,[kd],key,kd,owner,t)).group(owner,48)
        self.assertIsNone(group_auth(group,group,Auth('unknown'),t).reason)
        group.sigs[0].data=group.sigs[0].data[:-1]+bytes([group.sigs[0].data[-1]^1])
        self.assertEqual(group_auth(group,group,Auth('unknown'),t).reason,'DNSSEC_SIGNATURE_INVALID')
    def test_missing_groups_recovery_and_wildcard_body(self):
        key=ec.generate_private_key(ec.SECP256R1()); kd=dnskey(key); owner=(b'_tessera-v1',b'wamason',b'com'); t=100000
        body=rrset(owner,16,[b'\x01x'],key,kd,(),t)
        self.assertEqual(parse_snapshot(body).zones,[()])
        parsed=parse_snapshot(body); sig=bytearray(parsed.txt.sigs[0].data); sig[3]=0
        self.assertTrue(parse_snapshot(rr(owner,16,b'\x01x')+rr(owner,46,bytes(sig))).wildcard)
    def test_unsupported_ds_selector_is_metadata_only(self):
        key=ec.generate_private_key(ec.SECP256R1()); kd=dnskey(key); z=(b'com',);t=100000
        group=parse_snapshot(rrset(z,48,[kd],key,kd,z,t)).group(z,48)
        # unsupported digest matches the key even when a signature selector is wrong
        ds=Group(z,43,[RR(z,43,0,keytag(kd).to_bytes(2,'big')+b'\x0d\x63'+bytes(32),0)],[])
        bad=bytearray(group.sigs[0].data); bad[16:18]=((keytag(kd)+1)%65536).to_bytes(2,'big'); group.sigs[0].data=bytes(bad)
        self.assertEqual(group_auth(group,group,Auth('pass'),t,ds).reason,'DNSSEC_ALGORITHM_UNSUPPORTED')

class WildcardRestrictionTests(unittest.TestCase):
    def test_wildcard_labels_survive_malformed_rdata(self):
        owner=(b'_tessera-v1',b'wamason',b'com')
        # Covered type and Labels are obtainable despite a truncated supported RDATA.
        malformed=b'\x00\x10\x0d\x00'
        snap=parse_snapshot(rr(owner,16,b'\x01x')+rr(owner,46,malformed))
        self.assertTrue(snap.wildcard)

class CountAndRsaTests(unittest.TestCase):
    def test_ots_attestation_bound(self):
        item=b'\x00'+BTC+b'\x01\x01'; header=MAGIC+b'\x01\x08'+bytes(32)
        self.assertEqual(len(parse_ots(header+(b'\xff'+item)*4095+item).bitcoin),4096)
        with self.assertRaises(Fault): parse_ots(header+(b'\xff'+item)*4096+item)
    def test_ots_op_bound(self):
        item=b'\x08'*256+b'\x00'+BTC+b'\x01\x01'; header=MAGIC+b'\x01\x08'+bytes(32)
        self.assertEqual(len(parse_ots(header+(b'\xff'+item)*255+item).bitcoin),256)
        with self.assertRaises(Fault): parse_ots(header+(b'\xff'+item)*256+item)
    def test_rsa_sha256_and_ds_sha384(self):
        from cryptography.hazmat.primitives.asymmetric import rsa,padding
        from cryptography.hazmat.primitives import hashes
        from dnssec import verify_rr,ds_matches,signed_data
        import hashlib
        key=rsa.generate_private_key(65537,2048); numbers=key.public_key().public_numbers()
        kd=b'\x01\x01\x03\x08\x03\x01\x00\x01'+numbers.n.to_bytes(256,'big')
        owner=(b'com',); data=b'\x01x'; t=100000
        prefix=b'\x00\x10\x08\x01'+(3600).to_bytes(4,'big')+(t+100).to_bytes(4,'big')+(t-100).to_bytes(4,'big')+keytag(kd).to_bytes(2,'big')+wire(owner)
        signature=key.sign(prefix+rr(owner,16,data),padding.PKCS1v15(),hashes.SHA256())
        group=Group(owner,16,[RR(owner,16,3600,data,0)],[RR(owner,46,3600,prefix+signature,0)])
        sig=parse_rrsig(prefix+signature)
        self.assertTrue(verify_rr(group,sig,kd))
        ds=keytag(kd).to_bytes(2,'big')+b'\x08\x04'+hashlib.sha384(wire(owner)+kd).digest()
        self.assertTrue(ds_matches(ds,owner,kd)); self.assertFalse(ds_matches(ds[:-1]+bytes([ds[-1]^1]),owner,kd))

class RsaFormatTests(unittest.TestCase):
    def test_wrong_signature_width(self):
        from cryptography.hazmat.primitives.asymmetric import rsa
        from dnssec import verify_rr
        key=rsa.generate_private_key(65537,2048); n=key.public_key().public_numbers().n
        kd=b'\x01\x01\x03\x08\x03\x01\x00\x01'+n.to_bytes(256,'big'); owner=(b'com',)
        prefix=b'\x00\x10\x08\x01'+(3600).to_bytes(4,'big')+(100100).to_bytes(4,'big')+(99900).to_bytes(4,'big')+keytag(kd).to_bytes(2,'big')+wire(owner)
        sig=parse_rrsig(prefix+b'x'); group=Group(owner,16,[RR(owner,16,3600,b'\x01x',0)],[])
        with self.assertRaises(Fault) as cm: verify_rr(group,sig,kd)
        self.assertEqual(cm.exception.code,'DNSSEC_FORMAT')
