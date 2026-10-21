"""Boundary, rejection-precedence and proof-text witnesses; no outside writes."""
import sys
sys.dont_write_bytecode=True
from review import *

def witness():
    probes()
    sg=bytes.fromhex(byid['SIG-01']['bytes_hex']);parsed=I.parse_signature(sg)
    print('trailer-length actual='+str(len(parsed.trailer))+' final-u32='+str(int.from_bytes(parsed.trailer[-4:],'big'))+' difference='+str(len(parsed.trailer)-int.from_bytes(parsed.trailer[-4:],'big')))
    print('trailer-suffix-literal-split-equals-trailer='+str(parsed.trailer[-int.from_bytes(parsed.trailer[-4:],'big'):]==parsed.trailer))
    f0=bytes.fromhex(byid['F-01']['bytes_hex']);f1=bytes.fromhex(byid['F-02']['bytes_hex'])
    positions=[i for i,(a,b) in enumerate(zip(f0,f1)) if a!=b]
    print('F01/F02 lengths='+str((len(f0),len(f1)))+' first-difference='+str(positions[0])+' signer-prefix-difference='+str(positions[1]))
    # Minimal inner-format mismatch: complete packet, only 4 bytes in body.
    for sg in (pgp(b'\x04\x00\x13\x08'),tiny_sig()+b'x'):
        show('signature-'+sg.hex(),outcome(lambda:B.sig_check(sg,B.V1_ALG,0)),outcome(lambda:I.parse_signature(sg)))
    # B sees syntax before scanning the invalid UTF8 tail.
    raw=b'\xef\xbb\xbf\xff'
    show('precedence-content-'+raw.hex(),*ingest(raw))
    obj=B.frame_decode(f0,'attest');raw=B.jcs(obj)
    fr=I.frame('tessera-v1/attest',b'\xef\xbb\xbf'+raw+b'\xff')
    show('precedence-frame-BOM-invalid',*frame(fr))
    # Explicit boundary: all accepted spellings are valid RFC8259 ASCII, no size issue.
    for raw in (b'0e'+b'0'*4301,b'1e'+b'0'*4301,b'1e'+b'9'*4301):
        show('large-exponent-'+raw[:2].decode()+'-'+raw[2:3].decode(),*ingest(raw))
    # Schema and float identities disambiguate bools, null and numerals.
    for text in (b'true',b'1',b'false',b'0',b'null',b'"0"',b'[]',b'{}'):
        show('typed-'+text.decode(),*payload(text))

def lemma9():
    """Actual SHA256 messages, same OpenPGP packet, same chosen P256 key.

    A birthday search finds equal *16-bit prefixes*, not a SHA256 collision.
    Choose a public key after hashing the messages, using ECDSA algebra.
    Lemma 9 imposes no prior fixed/honestly generated key or frame/key binding.
    """
    from cryptography.hazmat.primitives.asymmetric import ec,utils
    from cryptography.hazmat.primitives import hashes
    h=b'\x05\x02'+(1).to_bytes(4,'big')
    head=b'\x04\x00\x13\x08'+len(h).to_bytes(2,'big')+h
    trailer=head+b'\x04\xff'+len(head).to_bytes(4,'big')
    obj=B.frame_decode(bytes.fromhex(byid['F-01']['bytes_hex']),'attest')
    seen={}
    for i in range(100000):
        obj['common']['content']='P8 lemma9 chosen-key witness '+str(i)
        f=B.frame_encode('attest',obj);digest=hashlib.sha256(f+trailer).digest()
        if digest[:2] in seen:
            f0,z0,idx=seen[digest[:2]];f1,z1=f,digest;break
        seen[digest[:2]]=f,digest,i
    else:raise AssertionError('16-bit prefix birthday search failed')
    n=I.N;k=2
    r=ec.derive_private_key(k,ec.SECP256R1()).public_key().public_numbers().x%n
    a,b=int.from_bytes(z0,'big'),int.from_bytes(z1,'big')
    d=(-(a+b)*pow(2*r,-1,n))%n
    s=((a+r*d)*pow(k,-1,n))%n
    assert d and r and s and z0!=z1 and z0[:2]==z1[:2]
    def mpi(x):return x.bit_length().to_bytes(2,'big')+x.to_bytes((x.bit_length()+7)//8,'big')
    sg=pgp(head+b'\x00\x00'+z0[:2]+mpi(r)+mpi(s))
    key=ec.derive_private_key(d,ec.SECP256R1()).public_key();q=key.public_numbers()
    parsed=I.parse_signature(sg);I.sig_policy(parsed)
    b_ok=[];i_ok=[]
    for f in (f0,f1):
        assert frame(f)[0][0]==frame(f)[1][0]=='OK'
        b_ok.append(B.pgp4_verify(f,sg,(q.x,q.y)))
        i_ok.append(I.signature_verifies(f,parsed,key))
    assert all(b_ok+i_ok)
    print('lemma9 actual-frame witness: attempts='+str(i+1)+' indices='+str((idx,i)))
    print('frames-distinct='+str(f0!=f1)+' SHA256-digests-distinct='+str(z0!=z1)+' left16-equal='+str(z0[:2]==z1[:2]))
    print('same-key same-packet B-verifies='+str(b_ok)+' I/OpenSSL-verifies='+str(i_ok)+' sig-policy=OK')
    print('F0/F1 codec B=OK/OK I=OK/OK')
    print('digest0='+z0.hex());print('digest1='+z1.hex())
    record={'f0_hex':f0.hex(),'f1_hex':f1.hex(),'signature_hex':sg.hex(),'private_test_scalar_hex':hex(d),'public_x':hex(q.x),'public_y':hex(q.y),'digest0':z0.hex(),'digest1':z1.hex()}
    (HERE/'lemma9-witness.json').write_text(json.dumps(record,indent=2)+'\n')
    print('The chosen key does not match the frames\' illustrative key_fp; no complete receipt is claimed.')

def text():
    t0=b'tessera-v1/attest';t1=b'tessera-v1/manifest'
    h0=bytes([len(t0)])+t0;h1=bytes([len(t1)])+t1
    last=1+max(len(t0),len(t1))
    print('lemma4 header-lengths='+str((len(h0),len(h1)))+' asserted-common-covered-prefix='+str(last)+' both-cover='+str(len(h0)>=last and len(h1)>=last))
    print('lemma4 first-bytes-differ='+str(h0[0]!=h1[0])+' prefix-free-result-still=True')
    fr=bytes.fromhex(byid['M-01']['bytes_hex'])
    print('M-01 version-at-offset18='+fr[18:20].hex()+' version-at-offset20='+fr[20:22].hex())
    sg=bytes.fromhex(byid['SIG-01']['bytes_hex']);parsed=I.parse_signature(sg)
    print('SIG-01 trailer-length='+str(len(parsed.trailer))+' final-u32='+str(int.from_bytes(parsed.trailer[-4:],'big')))

def oversize():
    raw=b'"'+b'a'*(B.CAP-1)+b'"'
    assert len(raw)==B.CAP+1
    a=outcome(lambda:B.payload_value(raw));b=outcome(lambda:I.parse_json(raw,canonical=True))
    print('standalone payload bytes='+str(len(raw))+' cap='+str(B.CAP)+' B='+a[0]+' I='+b[0])
    obj=B.frame_decode(bytes.fromhex(byid['F-01']['bytes_hex']),'attest');obj['common']['content']='a'*(B.CAP-1)
    fr=B.frame_encode('attest',obj);a,b=frame(fr)
    print('same-content framed bytes='+str(len(fr))+' B='+a[0]+' I='+b[0])

def boundaries():
    counts=collections.Counter();hist=collections.Counter()
    def check(kind,raw,pair,expected=None):
        a,b=pair;counts[kind]+=1;hist[a[0]+' / '+b[0]]+=1
        assert a[0]==b[0],(kind,a[0],b[0])
        if expected:assert a[0]==expected,(kind,a[0],expected)
    base=B.frame_decode(bytes.fromhex(byid['F-01']['bytes_hex']),'attest')
    for depth in (0,1,60,61,62,63,64,65):
        raw=b'['*depth+b'0'+b']'*depth
        check('ingest-depth',raw,ingest(raw),'OK' if depth<=62 else 'JSON_DEPTH')
        check('payload-depth',raw,payload(raw),'OK' if depth<=64 else 'JSON_DEPTH')
        obj=copy.deepcopy(base);v=0.0
        for _ in range(depth):v=[v]
        obj['common']['content']=v;fr=B.frame_encode('attest',obj)
        check('frame-depth',fr,frame(fr),'OK' if depth<=62 else 'JSON_DEPTH')
    for field,vals in [
        ('declared_issue_time',['0001-01-01T00:00:00Z','9999-12-31T23:59:59Z','0000-01-01T00:00:00Z','1900-02-29T00:00:00Z','2000-02-29T00:00:00Z','2026-10-19T23:59:60Z','2026-10-19T24:00:00Z']),
        ('issuer',['a.b','0.1','a'*63+'.'+'b'*63+'.'+'c'*63+'.'+'d'*49,'a'*63+'.'+'b'*63+'.'+'c'*63+'.'+'d'*50,'a'*64+'.b','-a.b','a.b.']),
        ('alg',['0','A'*64,'A'*65,'','A_','A-','UNKNOWN'])]:
        for val in vals:
            obj=copy.deepcopy(base);obj['common'][field]=val;raw=B.frame_encode('attest',obj)
            check('schema-'+field,raw,frame(raw))
    for forms in ([],['A'],['A','B'],['B','A'],['A','A'],['A'*32],['A'*33],['a'],[True]):
        obj=copy.deepcopy(base);obj['common']['binding_forms']=forms;raw=B.frame_encode('attest',obj);check('schema-forms',raw,frame(raw))
    # Every Unicode scalar individually in an NFC/assignment decision; stringify only at boundary samples.
    # Full scalar set compares the two acceptance predicates rather than reusing either decoder.
    for cp in range(0x110000):
        ch=chr(cp);a=outcome(lambda:B.string_ok(ch))[0]
        good=(not (0xd800<=cp<=0xdfff or 0xfdd0<=cp<=0xfdef or cp&65535 in (65534,65535))
              and unicodedata.category(ch)!='Cn' and unicodedata.normalize('NFC',ch)==ch)
        assert (a=='OK')==good,cp
        counts['unicode-scalar-domain']+=1
    for cp in (0,1,8,9,10,12,13,31,32,34,47,92,127,0x7ff,0x800,0xd7ff,0xd800,0xdbff,0xdc00,0xdfff,0xe000,0xfdd0,0xfdef,0xfffd,0xfffe,0xffff,0x10000,0x1f600,0x10fffd,0x10fffe,0x10ffff):
        ch=chr(cp);raw=json.dumps(ch,ensure_ascii=True).encode();check('unicode-decoder',raw,ingest(raw))
    # Payload cap: exact schema with content adjusted to total lengths cap-1/cap/cap+1.
    for size in (B.CAP-1,B.CAP,B.CAP+1):
        obj=copy.deepcopy(base);obj['common']['content']='';overhead=len(B.jcs(obj));obj['common']['content']='a'*(size-overhead)
        raw=B.frame_encode('attest',obj);assert len(raw)==size+24
        a=outcome(lambda:B.frame_decode(raw,'attest'));b=outcome(lambda:I.read_frame(raw,'tessera-v1/attest'))
        # No duplicate huge data in evidence files.
        print('payload-bytes',size,'B='+a[0],'I='+b[0],flush=True)
        check('frame-size',b'',(a,b),'OK' if size<=B.CAP else 'LENGTH_CAP')
    f0=bytes.fromhex(byid['F-01']['bytes_hex']); f1=bytes.fromhex(byid['F-02']['bytes_hex'])
    # Exercise all rules, slot capacities, mixed ids, signature contents and tag cross-products.
    for alg in (B.V1_ALG,B.HYB_ALG,'X-CANARY'):
        for n in (0,1,2,1023,1024,1025,3308,3309,3310,65535,65536,65537):
            for slot in (0,1):
                raw=b'x'*n
                pair=(outcome(lambda:B.sig_check(raw,alg,slot)),outcome(lambda:I.parse_signature(raw,alg,('kms','gpg')[slot],REG)))
                check('signature-cap',raw,pair)
    tagged=[bytes.fromhex(byid[x]['bytes_hex']) for x in ('F-01','M-01','A-01','S-01')]
    for raw in tagged:
        for kind in ('attest','manifest'):check('cross-tag-frame',raw,frame(raw,kind))
        check('cross-tag-anchor',raw,anchor(raw))
    snapcounts=0
    for size in (0,1,B.CAP-1,B.CAP,B.CAP+1):
        raw=b'a'*size;enc=B.snapshot_encode(raw);code,value=outcome(lambda:B.snapshot_decode(enc))
        expected='SCHEMA' if size==0 else 'LENGTH_CAP' if size>B.CAP else 'OK'
        assert code==expected
        if code=='OK':assert value==raw
        snapcounts+=1
    counts['snapshot-size']=snapcounts
    print(json.dumps({'counts':dict(counts),'histogram':dict(hist)},indent=2))

if __name__=='__main__':
    {'witness':witness,'boundaries':boundaries,'lemma9':lemma9,'text':text,'oversize':oversize}[sys.argv[1]]()
