"""Independent P8 falsification instrument. All generated artifacts stay beside this file.
Run from repository root with prototype/.venv/bin/python -B prototype/p8-falsify/review.py COMMAND.
"""
import sys
sys.dont_write_bytecode = True
import argparse, base64, collections, copy, datetime, hashlib, importlib.util, json
import math, os, pathlib, random, struct, subprocess, time, unicodedata
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE / 'deps'))

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    obj = importlib.util.module_from_spec(spec); sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj

B = module('review_B', 'formal/p8/vectors/check.py')
I = module('review_I', 'prototype/indep-verifier/codec.py')
REG = I.registered_codecs(I.HYBRID_ALG)
GS = [v for f in ('golden.json', 'hybrid-golden.json')
      for v in json.loads((ROOT / 'formal/p8/vectors' / f).read_text())['vectors']]
RS = [v for f in ('reject.json', 'hybrid-reject.json')
      for v in json.loads((ROOT / 'formal/p8/vectors' / f).read_text())['vectors']]
byid = {v['id']:v for v in GS}

def outcome(fn):
    try: return 'OK', fn()
    except (B.Bad,I.Fault) as e: return e.code,None
    except Exception as e: return 'CRASH:'+type(e).__name__, str(e)

def canon_i(v): return I.jcs(v)
def payload(b): return outcome(lambda:B.payload_value(b)),outcome(lambda:I.parse_json(b,canonical=True))
def ingest(b): return outcome(lambda:B.ingest(b)),outcome(lambda:I.parse_json(b,max_depth=62))
def frame(b, kind='attest'):
    return outcome(lambda:B.frame_decode(b,kind)),outcome(lambda:I.read_frame(b,'tessera-v1/'+kind))
def anchor(b):
    return outcome(lambda:B.anchor_decode(b)),outcome(lambda:[(f,s) for f,_,s,_ in I.read_anchor(b,registry=REG)])
def pgp(body): return bytes([0x88,len(body)])+body if len(body)<=255 else b'\x89'+len(body).to_bytes(2,'big')+body
def tiny_sig(h=b'',u=b''):
    return pgp(b'\x04\x00\x13\x08'+len(h).to_bytes(2,'big')+h+len(u).to_bytes(2,'big')+u+b'\x00\x00\x00\x01\x01\x00\x01\x01')
def show(label,a,b): print(label, 'B='+a[0], 'I='+b[0])

def probes():
    print('Python',sys.version.split()[0], 'Unicode',unicodedata.unidata_version)
    # Registered hybrid must be explicitly installed for I; defaults model the baseline.
    f0,s0,f1,s1 = [bytes.fromhex(byid['A-H1']['input'][k]) for k in ('f0_hex','s0_hex','f1_hex','s1_hex')]
    malformed = B.anchor_encode(f0,b'x',f1,s1)
    show('hybrid-short installed',*anchor(malformed))
    show('hybrid-short default',outcome(lambda:B.anchor_decode(malformed)),outcome(lambda:I.read_anchor(malformed)))
    # Declared body is complete, but mandatory body fields are absent.
    s=b'\x88\x00'
    show('empty-pgp-body signature',outcome(lambda:B.sig_check(s,B.V1_ALG,0)),outcome(lambda:I.parse_signature(s)))
    f=bytes.fromhex(byid['F-01']['bytes_hex']); g=bytes.fromhex(byid['F-02']['bytes_hex'])
    show('empty-pgp-body anchor',*anchor(B.anchor_encode(f,s,g,tiny_sig())))
    for n in (4300,4301):
        raw=b'0e'+b'9'*n
        show('zero-exponent-digits='+str(n)+' ingest',*ingest(raw))
        show('zero-exponent-digits='+str(n)+' payload',*payload(raw))
    raw=b'['*65+b'0'+b']'*65
    show('lemma3-depth65',*payload(raw))
    show('BOM-invalid-UTF8',*ingest(b'\xef\xbb\xbf\xff'))
    raw=b'['*1200+b'0'+b']'*1200
    show('depth1200',*payload(raw))
    # ECDSA at digest level: same key/signature verifies distinct digest scalars.
    # d=1, k=2; z2=-z1-2*r*d mod n negates the verification point.
    from cryptography.hazmat.primitives.asymmetric import ec,utils
    from cryptography.hazmat.primitives import hashes
    n=I.N; d=1; k=2; z1=1
    key=ec.derive_private_key(d,ec.SECP256R1()).public_key()
    r=ec.derive_private_key(k,ec.SECP256R1()).public_key().public_numbers().x % n
    s=pow(k,-1,n)*(z1+r*d)%n; z2=(-z1-2*r*d)%n
    der=utils.encode_dss_signature(r,s)
    results=[]
    for z in (z1,z2):
        digest=z.to_bytes(32,'big'); key.verify(der,digest,ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        q=key.public_numbers(); assert B.p256_verify((q.x,q.y),digest,r,s)
        results.append(digest.hex())
    print('lemma9 digest witness: distinct='+str(z1!=z2)+' B-verifies=2/2 OpenSSL-verifies=2/2')
    print('digest1='+results[0]); print('digest2='+results[1])
    print('This is a missing-implication witness, not two SHA256 preimages or an encoding collision.')
    print('hybrid-id-actual-length='+str(len(I.HYBRID_ALG)))

def mutate(rng,raw):
    b=bytearray(raw)
    for _ in range(rng.randint(1,3)):
        at=rng.randrange(len(b)+1); op=rng.randrange(5)
        if op==0 and at<len(b): b[at]^=1<<rng.randrange(8)
        elif op==1 and at<len(b): del b[at]
        elif op==2: b[at:at]=rng.randbytes(rng.randint(1,3))
        elif op==3 and at<len(b): b[at]=rng.randrange(256)
        elif at<len(b): b=b[:at]
    return bytes(b)

def campaign():
    rng=random.Random(0x50384620261019); start=time.monotonic()
    hist=collections.defaultdict(collections.Counter); examples={}; collisions={}; seen={}; counts=collections.Counter()
    def check(kind,raw,pair):
        a,b=pair; counts[kind]+=1; hist[kind][a[0]+' / '+b[0]]+=1
        if a[0]!=b[0]:
            key=(kind,a[0],b[0])
            if key not in examples: examples[key]={'kind':kind,'B':a[0],'I':b[0],'hex':raw.hex()}
        elif a[0]=='OK':
            if kind.endswith('anchor'):
                assert a[1]==b[1], ('tuple mismatch',kind)
                assert B.anchor_encode(*sum(([f,s] for f,s in a[1]),[]))==raw
            elif kind not in ('sig',):
                assert B.jcs(a[1])==I.jcs(b[1]), ('decoded mismatch',kind,raw.hex())
            if kind=='valid-frame':
                assert B.frame_encode('attest',a[1])==raw
    frames=[bytes.fromhex(g['bytes_hex']) for g in GS if g['kind'] in ('frame-attest','frame-manifest')]
    anchors=[bytes.fromhex(g['bytes_hex']) for g in GS if g['kind']=='anchor']
    texts=[bytes.fromhex(v['input']['text_hex']) for v in GS if v['kind']=='content']
    texts += [bytes.fromhex(v['input']['text_hex']) for v in RS if v['entry']=='content']
    for v in GS:
        if v['kind'] in ('frame-attest','frame-manifest'):
            raw=bytes.fromhex(v['bytes_hex']); check('vector-frame',raw,frame(raw,'manifest' if v['kind']=='frame-manifest' else 'attest'))
        elif v['kind']=='anchor':
            raw=bytes.fromhex(v['bytes_hex']); check('vector-anchor',raw,anchor(raw))
        elif v['kind']=='content':
            raw=bytes.fromhex(v['bytes_hex']);check('vector-payload',raw,payload(raw))
    for v in RS:
        ent=v['entry'];i=v['input']
        if ent in ('frame-attest','frame-manifest','anchor','content'):
            raw=bytes.fromhex(i['text_hex' if ent=='content' else 'bytes_hex'])
            pair=ingest(raw) if ent=='content' else anchor(raw) if ent=='anchor' else frame(raw,'manifest' if ent=='frame-manifest' else 'attest')
            assert pair[0][0]==v['expect'],v['id']
            check('vector-reject-'+ent,raw,pair)
    def scalar():
        x=rng.randrange(6)
        if x==0:
            while True:
                f=struct.unpack('>d',rng.randbytes(8))[0]
                if math.isfinite(f) and not (f==0 and math.copysign(1,f)<0): return f
        if x==1: return rng.choice([None,True,False])
        return ''.join(rng.choice(['a','é','😀','\x00','\n','"','\\','\ue000','\U0001e900']) for _ in range(rng.randrange(9)))
    def value(d=0):
        if d>=3 or rng.random()<.6:return scalar()
        if rng.random()<.5:return [value(d+1) for _ in range(rng.randrange(5))]
        return {str(scalar()):value(d+1) for _ in range(rng.randrange(5))}
    # Typed structural identity, independent of JCS. Object order has no meaning.
    def ident(v):
        if v is None:return ('null',)
        if isinstance(v,bool):return ('bool',v)
        if isinstance(v,float):return ('number',struct.pack('>d',v))
        if isinstance(v,str):return ('string',v)
        if isinstance(v,list):return ('array',tuple(map(ident,v)))
        return ('object',tuple(sorted((k,ident(x)) for k,x in v.items())))
    base=B.frame_decode(bytes.fromhex(byid['F-01']['bytes_hex']),'attest')
    for j in range(12000):
        v=value();raw=B.jcs(v);check('generated-payload',raw,payload(raw))
        key=ident(v)
        assert raw not in seen or seen[raw]==key,'ENCODING COLLISION'
        seen[raw]=key
        # Existing schema, arbitrary accepted content, issuer and algorithm variation.
        obj=copy.deepcopy(base);obj['common']['content']=v
        obj['common']['alg']=rng.choice([B.V1_ALG,B.HYB_ALG,'Z-CANARY','0'])
        raw=B.frame_encode('attest',obj);check('valid-frame',raw,frame(raw))
        if j%1000==0: print('progress valid-values',j,flush=True)
    for _ in range(20000):
        raw=mutate(rng,rng.choice(texts));check('mutant-ingest',raw,ingest(raw))
    for _ in range(20000):
        raw=mutate(rng,rng.choice(frames));kind='manifest' if raw[1:20]==b'tessera-v1/manifest' else 'attest'
        check('mutant-frame',raw,frame(raw,kind))
    for _ in range(20000):
        raw=mutate(rng,rng.choice(anchors));check('mutant-anchor',raw,anchor(raw))
    # Generate accepted O packets of varied subpacket lengths/MPI sizes, then corrupt them.
    for _ in range(12000):
        n=rng.choice([0,1,2,190,191,192,193,255,256,500])
        area=b'' if not n else (bytes([n]) if n<192 else bytes([192+((n-192)>>8),(n-192)&255]))+rng.randbytes(n)
        raw=tiny_sig(h=area) if rng.randrange(2) else tiny_sig(u=area)
        if rng.random()<.7:raw=mutate(rng,raw)
        check('sig',raw,(outcome(lambda:B.sig_check(raw,B.V1_ALG,0)),outcome(lambda:I.parse_signature(raw))))
    # Cross-slot anchors; mixed algs are permitted at codec level, constrained by receipts.
    anseen={}
    for _ in range(10000):
        obj=copy.deepcopy(base); obj['common']['alg']=rng.choice([B.V1_ALG,B.HYB_ALG,'X-CANARY'])
        obj['common']['content']=scalar(); f0=B.frame_encode('attest',obj)
        ob1=copy.deepcopy(obj);ob1['signer']['key_fp']='gpg-sha256:'+'1'*64;f1=B.frame_encode('attest',ob1)
        s0=rng.randbytes(3309) if obj['common']['alg']==B.HYB_ALG else rng.randbytes(rng.randrange(1,64)) if obj['common']['alg']=='X-CANARY' else tiny_sig(u=b'\x02\x63'+rng.randbytes(1))
        s1=rng.randbytes(rng.randrange(1,64)) if obj['common']['alg']=='X-CANARY' else tiny_sig()
        raw=B.anchor_encode(f0,s0,f1,s1);check('valid-anchor',raw,anchor(raw));key=(f0,s0,f1,s1)
        assert raw not in anseen or anseen[raw]==key,'ANCHOR COLLISION'
        anseen[raw]=key
    bundle=json.loads((ROOT/'prototype/e2e/receipts/real-1/bundle.json').read_text())
    for layer in bundle['layers']:
        raw=base64.b64decode(layer['a_sig']);check('real-anchor',raw,anchor(raw))
        for f,sg in B.anchor_decode(raw):check('real-frame',f,frame(f))
    data={'seed':'0x50384620261019','elapsed_seconds':round(time.monotonic()-start,3),
          'counts':dict(counts),'histograms':{k:dict(v) for k,v in hist.items()},
          'unique_payload_structures':len(seen),'unique_anchor_tuples':len(anseen),
          'collision_count':0,'disagreements':list(examples.values())}
    (HERE/'campaign.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ('histograms','disagreements')},indent=2))
    print('disagreement classes',[(e['kind'],e['B'],e['I']) for e in data['disagreements']])

def properties():
    from hypothesis import given,settings,strategies as st, HealthCheck
    chars=st.characters(blacklist_categories=('Cs','Cn'),blacklist_characters=[chr(c) for c in range(0xfdd0,0xfdf0)])
    strings=st.text(chars,max_size=20).filter(lambda s:unicodedata.normalize('NFC',s)==s and all(ord(c)&0xffff not in (0xfffe,0xffff) for c in s))
    leaves=st.one_of(st.none(),st.booleans(),st.floats(allow_nan=False,allow_infinity=False,allow_subnormal=True).filter(lambda x:x!=0 or math.copysign(1,x)>0),strings)
    values=st.recursive(leaves,lambda x:st.one_of(st.lists(x,max_size=5),st.dictionaries(strings,x,max_size=5)),max_leaves=20)
    count=collections.Counter(); seen={}
    @settings(max_examples=3000,deadline=None,derandomize=True,database=None,suppress_health_check=[HealthCheck.filter_too_much])
    @given(values,values)
    def prop(v,w):
        count['pairs']+=1
        # Type-aware equality is recovered by decoding tagged JSON representations here.
        for x in (v,w):
            raw=B.jcs(x);a,b=payload(raw)
            assert a[0]==b[0]=='OK',(raw,a[0],b[0])
            assert B.jcs(a[1])==I.jcs(b[1])==raw
            count['payload_roundtrips']+=1
        def typed(x):
            if isinstance(x,dict):return ('obj',tuple(sorted((k,typed(y)) for k,y in x.items())))
            if isinstance(x,list):return ('arr',tuple(map(typed,x)))
            return (type(x).__name__,x)
        assert (B.jcs(v)==B.jcs(w)) == (typed(v)==typed(w))
    prop();print('hypothesis',dict(count),'PASS')

def numbers():
    rng=random.Random(0x4e554d); xs=[]
    for _ in range(100000):
        bits=rng.getrandbits(64);f=struct.unpack('>d',bits.to_bytes(8,'big'))[0]
        if math.isfinite(f) and not (f==0 and bits>>63):xs.append((bits,f))
    for p in range(-1074,1024):
        f=math.ldexp(1.0,p)
        xs.extend((int.from_bytes(struct.pack('>d',g),'big'),g) for g in (math.nextafter(f,0),f,math.nextafter(f,math.inf)) if math.isfinite(g))
    js="const fs=require('fs');for(const h of fs.readFileSync(0,'utf8').trim().split('\\n')){const b=Buffer.from(h,'hex'); console.log(JSON.stringify(b.readDoubleBE()));}"
    node=subprocess.run(['node','-e',js],input='\n'.join(f'{bits:016x}' for bits,f in xs),text=True,capture_output=True,check=True)
    out=node.stdout.splitlines();assert len(xs)==len(out)
    for (_,f),s in zip(xs,out):assert B.es_string(f)==s,(f,B.es_string(f),s)
    print('Node-vs-B finite-binary64',len(xs),'PASS')
    for (_,f),s in list(zip(xs,out))[:5000]:assert I.es(f)==s,(f,I.es(f),s)
    print('Node-vs-I finite-binary64',min(5000,len(xs)),'PASS')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['probes','campaign','properties','numbers']);args=parser.parse_args()
    globals()[args.command]()
