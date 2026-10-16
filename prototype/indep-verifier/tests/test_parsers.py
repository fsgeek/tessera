import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from codec import Fault, parse_json, jcs, frame, read_frame, parse_signature, b64
from anchors import Reader, parse_ots, transaction, MAGIC
from dnssec import name, parse_snapshot, rrsig_time, txt_value
from git_channel import parse_tree, parse_commit, dearmor

class ParserTests(unittest.TestCase):
    def code(self, code, fn, *args):
        with self.assertRaises(Fault) as cm: fn(*args)
        self.assertEqual(cm.exception.code, code)
    def test_json_order(self):
        self.code('JSON_DUPLICATE_NAME', parse_json, b'{"a":1,"a":2}')
        self.code('JSON_ENCODING', parse_json, b'"\xff"')
        self.code('JSON_SYNTAX', parse_json, b'NaN')
        self.code('JSON_STRING', parse_json, b'"e\\u0301"')
        self.code('JSON_NUMBER', parse_json, b'-0')
        self.code('JSON_NUMBER', parse_json, b'9007199254740993')
    def test_json_numbers(self):
        for raw, expected in [(b'9.80',b'9.8'),(b'1E2',b'100'),(b'1e21',b'1e+21'),
                              (b'5e-324',b'5e-324'),(b'1e-6',b'0.000001')]:
            self.assertEqual(jcs(parse_json(raw)), expected)
        self.assertEqual(jcs(parse_json(b'{"\xee\x80\x80":true,"\xf0\x9f\x98\x80":null}')),
                         b'{"\xf0\x9f\x98\x80":null,"\xee\x80\x80":true}')
    def test_frame_boundaries(self):
        raw=frame('tessera-v1/manifest',b'{}')
        self.code('SCHEMA',read_frame,raw,'tessera-v1/manifest')
        self.code('TRAILING',read_frame,raw+b'x','tessera-v1/manifest')
        self.code('TRUNCATED',read_frame,raw[:-1],'tessera-v1/manifest')
        self.code('TAG_UNKNOWN',read_frame,b'\x01x','tessera-v1/manifest')
    def test_signature_boundaries(self):
        self.code('SIG_EMPTY',parse_signature,b'')
        self.code('SIG_PACKET',parse_signature,b'\xc2\x00')
        self.code('TRUNCATED',parse_signature,b'\x88\x05x')
        self.code('SIG_PACKET',parse_signature,b'\x89\x00\x01x')
    def test_base64(self):
        self.assertEqual(b64('YQ=='), b'a')
        for s in ['YR==','YQ','YQ==\n']: self.code('CONTAINER_SCHEMA',b64,s)
    def test_varuint(self):
        self.assertEqual(Reader(b'\xff\xff\xff\xff\x0f').varuint(),2**32-1)
        for raw in [b'\x80\x00',b'\x80',b'\x80\x80\x80\x80\x10']:
            self.code('OTS_FORMAT',lambda x:Reader(x).varuint(),raw)
    def test_pending_ots(self):
        raw=MAGIC+b'\x01\x08'+bytes(32)+b'\x00'+bytes.fromhex('83dfe30d2ef90c8e')+b'\x02\x01x'
        proof=parse_ots(raw)
        self.assertEqual(proof.digest,bytes(32)); self.assertEqual(len(proof.pending),1)
        self.code('OTS_FORMAT',parse_ots,raw+b'x')
        self.code('OTS_FORMAT',parse_ots,raw[:-1])
    def test_bitcoin_transaction(self):
        raw=bytes(4)+b'\x01'+bytes(36)+b'\x00'+bytes(4)+b'\x01'+bytes(8)+b'\x22\x6a\x20'+bytes(32)+bytes(4)
        self.assertEqual(transaction(raw),[b'\x6a\x20'+bytes(32)])
        self.code('OTS_TX_SHAPE',transaction,raw+b'x')
        self.code('OTS_TX_SHAPE',transaction,bytes(4)+b'\x00\x01')
    def test_dns_wire(self):
        self.assertEqual(name(b'\x03com\x00',0),( (b'com',),5))
        self.code('SNAPSHOT_FORMAT',name,b'\xc0\x00',0)
        self.code('SNAPSHOT_FORMAT',name,b'\x03COM\x00',0)
        self.code('LENGTH_CAP',parse_snapshot,b'')
        self.code('SNAPSHOT_FORMAT',parse_snapshot,b'\x00')
    def test_serial_time(self):
        self.assertIsNone(rrsig_time(0,0,2**32))
        self.assertEqual(rrsig_time(2**31,0,0),'RRSIG_TIME_AMBIGUOUS')
        self.assertEqual(rrsig_time(10,9,10),'RRSIG_INTERVAL_REVERSED')
        self.assertEqual(rrsig_time(1,2,3),'RRSIG_NOT_VALID_AT_EVAL_TIME')
    def test_txt(self):
        value=('v=tessera1;profile=tessera-v1-strict;kms='+'0'*64+';gpg='+'1'*64+
               ';issuance-not-before=2026-10-01T00:00:00Z;issuance-not-after=2026-10-02T00:00:00Z').encode()
        self.assertEqual(len(value),255)
        self.assertEqual(txt_value([bytes([255])+value])['kms'],'0'*64)
        self.code('DNS_STRINGS',txt_value,[b'\x01x\x01y'])
        self.code('DNS_RDATA',txt_value,[b'\x05x'])
    def test_tree(self):
        tree=b'100644 a\x00'+bytes(20)+b'40000 z\x00'+bytes(20)
        self.assertEqual(len(parse_tree(tree)),2)
        self.code('GIT_TREE_FORMAT',parse_tree,tree+b'x')
        self.code('GIT_TREE_FORMAT',parse_tree,b'100644 ..\x00'+bytes(20))
    def test_git_commit(self):
        raw=b'tree '+b'0'*40+b'\nauthor a\ncommitter b\ngpgsig armor\n continuation\n\nmsg'
        tree,payload,armor=parse_commit(raw)
        self.assertEqual(tree,'0'*40)
        self.assertEqual(armor,b'armor\ncontinuation')
        self.assertEqual(payload,b'tree '+b'0'*40+b'\nauthor a\ncommitter b\n\nmsg')
        self.code('GIT_COMMIT_FORMAT',parse_commit,raw.replace(b'author a',b'encoding UTF-8'))
        self.code('GIT_SIG_FORMAT',dearmor,b'armor')

if __name__=='__main__': unittest.main()

class NumberExamplesTests(unittest.TestCase):
    def test_encoding_number_examples(self):
        for literal in ['9.8','9.80','1E2','1e21','5e-324','123456789012345680000','0e99999999999999999999']:
            self.assertIsNotNone(parse_json(literal.encode()))
        for literal in ['1e400','1e-400','333333333.33333329','9007199254740993',
                        '0.1000000000000000055511151231257827021181583404541015625','4.9e-324','-0']:
            with self.assertRaises(Fault) as cm: parse_json(literal.encode())
            self.assertEqual(cm.exception.code,'JSON_NUMBER')
