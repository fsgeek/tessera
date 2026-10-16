"""Independent ENC codecs. No repository implementation imports."""
import base64
import datetime as dt
import decimal
import hashlib
import json
import math
import re
import unicodedata
from dataclasses import dataclass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils, mldsa
from cryptography.exceptions import InvalidSignature

ALG = 'OPENPGP4-ECDSA-P256-SHA256'
HYBRID_ALG = 'KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256'
# ENCODING-V1 baseline. Compiled supplement code is not registration.
BASELINE_CODECS = frozenset((ALG,))
PROFILE = 'tessera-v1-strict'
HEX = re.compile(r'[0-9a-f]{64}\Z')
TAGS = {'tessera-v1/attest','tessera-v1/manifest','tessera-v1/receipt-anchor-sig','tessera-v1/dnssec-snapshot'}
SPKI = bytes.fromhex('3059301306072a8648ce3d020106082a8648ce3d030107034200')
MLDSA65_SPKI = bytes.fromhex('308207b2300b0609608648016503040312038207a100')
GPG_PREFIX = bytes.fromhex('13082a8648ce3d0301070203')
P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
N = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

class Fault(ValueError):
    def __init__(self,code): self.code=code; super().__init__(code)

def demand(condition,code):
    if not condition: raise Fault(code)

def sha(data): return hashlib.sha256(data).digest()
def shahex(data): return sha(data).hex()
def b64(value):
    try:
        demand(isinstance(value,str) and not isinstance(value,Literal),'CONTAINER_SCHEMA')
        raw=base64.b64decode(value,validate=True)
        demand(base64.b64encode(raw).decode()==value,'CONTAINER_SCHEMA')
        return raw
    except (ValueError,UnicodeError): raise Fault('CONTAINER_SCHEMA') from None

def utc(s):
    demand(isinstance(s,str) and re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z',s),'SCHEMA')
    try: return int((dt.datetime.strptime(s,'%Y-%m-%dT%H:%M:%SZ')-dt.datetime(1970,1,1)).total_seconds())
    except ValueError: raise Fault('SCHEMA') from None

def isotime(t): return (dt.datetime(1970,1,1)+dt.timedelta(seconds=t)).strftime('%Y-%m-%dT%H:%M:%SZ')
def domain(s):
    return isinstance(s,str) and len(s)<=241 and len(s.split('.'))>=2 and all(re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?',x) for x in s.split('.'))
def fp(s,slot=None):
    if not isinstance(s,str): return False
    options=['spki-sha256:'] if slot=='kms' else ['gpg-sha256:'] if slot=='gpg' else ['spki-sha256:','gpg-sha256:']
    return any(s.startswith(p) and HEX.fullmatch(s[len(p):]) for p in options)

class Literal(str): pass
class Pairs(list): pass
@dataclass(frozen=True)
class Number:
    value: float

def es(value):
    """Shortest binary64 roundtrip, closest decimal then even, ECMA layout."""
    if value==0: return '0'
    if value<0: return '-'+es(-value)
    with decimal.localcontext() as ctx:
        ctx.prec=1100
        exact=decimal.Decimal.from_float(value)
        exponent=exact.adjusted()
        candidates=[]
        for k in range(1,18):
            step=decimal.Decimal(10)**(exponent-k+1)
            nearest=int((exact/step).to_integral_value(rounding=decimal.ROUND_HALF_EVEN))
            for i in (nearest-1,nearest,nearest+1):
                if i>0:
                    candidate=decimal.Decimal(i)*step
                    if float(candidate)==value:
                        candidates.append((abs(candidate-exact),i%2,candidate))
            if candidates: break
        demand(bool(candidates),'JSON_NUMBER')
        d=min(candidates)[2].normalize()
        digits=''.join(map(str,d.as_tuple().digits)); n=len(digits)+d.as_tuple().exponent; k=len(digits)
        if k<=n<=21: return digits+'0'*(n-k)
        if 0<n<=21: return digits[:n]+'.'+digits[n:]
        if -6<n<=0: return '0.'+'0'*(-n)+digits
        return digits[0]+('.'+digits[1:] if k>1 else '')+'e'+('+' if n-1>=0 else '-')+str(abs(n-1))

def parse_json(raw,canonical=False,no_numbers=False,max_depth=64, numbers=True):
    try: text=raw.decode('utf-8',errors='strict')
    except UnicodeError: raise Fault('JSON_ENCODING') from None
    try:
        obj=json.loads(text,object_pairs_hook=Pairs,parse_int=Literal,parse_float=Literal,
                       parse_constant=lambda _: (_ for _ in ()).throw(Fault('JSON_SYNTAX')))
    except (ValueError,RecursionError): raise Fault('JSON_SYNTAX') from None
    def visit(v,depth=0):
        if isinstance(v,(Pairs,list)):
            demand(depth+1<=max_depth,'JSON_DEPTH')
            for x in ( [v for _,v in v] if isinstance(v,Pairs) else v): visit(x,depth+1)
    visit(obj)
    def walk(v):
        yield v
        if isinstance(v,Pairs):
            for key,val in v: yield key; yield from walk(val)
        elif isinstance(v,list):
            for val in v: yield from walk(val)
    values=list(walk(obj))
    for val in values:
        if isinstance(val,Pairs): demand(len({k for k,_ in val})==len(val),'JSON_DUPLICATE_NAME')
    for val in values:
        if isinstance(val,str) and not isinstance(val,Literal):
            demand(all(not (0xd800<=ord(c)<=0xdfff or 0xfdd0<=ord(c)<=0xfdef or ord(c)&0xffff in (0xfffe,0xffff))
                       and unicodedata.category(c)!='Cn' for c in val) and unicodedata.normalize('NFC',val)==val,'JSON_STRING')
    def convert(v):
        if isinstance(v,Literal):
            if not numbers: return v
            demand(not no_numbers,'JSON_NUMBER')
            # Decimal accepts huge exponents poorly; zero is handled without constructing it.
            mantissa=re.split('[eE]',v)[0]
            zero=all(c in '-.0' for c in mantissa)
            demand(not (zero and v.startswith('-')),'JSON_NUMBER')
            if zero: return Number(0.0)
            try:
                exact=decimal.Decimal(v); f=float(v)
                demand(math.isfinite(f) and decimal.Decimal(es(f))==exact,'JSON_NUMBER')
                return Number(f)
            except (decimal.InvalidOperation,OverflowError,ValueError): raise Fault('JSON_NUMBER') from None
        if isinstance(v,Pairs): return {k:convert(x) for k,x in v}
        if isinstance(v,list): return [convert(x) for x in v]
        return v
    obj=convert(obj)
    if canonical: demand(jcs(obj)==raw,'JSON_NONCANONICAL')
    return obj

def jcs(v):
    def dump(v):
        if isinstance(v,Literal):
            try:
                f=float(v); demand(math.isfinite(f),'JSON_NONCANONICAL'); return es(f)
            except (ValueError,OverflowError): raise Fault('JSON_NONCANONICAL') from None
        if isinstance(v,Number): return es(v.value)
        if v is None: return 'null'
        if v is True: return 'true'
        if v is False: return 'false'
        if isinstance(v,str): return json.dumps(v,ensure_ascii=False,separators=(',',':'))
        if isinstance(v,list): return '['+','.join(dump(x) for x in v)+']'
        if isinstance(v,dict): return '{'+','.join(dump(k)+':'+dump(v[k]) for k in sorted(v,key=lambda k:k.encode('utf-16be')))+'}'
        raise TypeError('not a JSON value')
    return dump(v).encode('utf-8')

class Cursor:
    def __init__(self,data,code='TRUNCATED'): self.data=data; self.pos=0; self.code=code
    def take(self,n):
        demand(n>=0 and n<=len(self.data)-self.pos,self.code)
        out=self.data[self.pos:self.pos+n]; self.pos+=n; return out
    def uint(self,n): return int.from_bytes(self.take(n),'big')
    def end(self,code='TRAILING'): demand(self.pos==len(self.data),code)

def tag(c,expected):
    t=c.take(c.uint(1))
    demand(t in {t.encode() for t in TAGS},'TAG_UNKNOWN')
    demand(t==expected.encode(),'TAG_MISMATCH')

def frame(t,payload): return bytes([len(t)])+t.encode()+b'\x00\x01'+len(payload).to_bytes(4,'big')+payload

def schema(obj,expected): demand(isinstance(obj,dict) and set(obj)==set(expected),'SCHEMA')
def schema_alg(a): demand(isinstance(a,str) and re.fullmatch(r'[A-Z0-9][A-Z0-9-]{0,63}',a),'SCHEMA')

def read_frame(raw,expected):
    c=Cursor(raw); tag(c,expected); demand(c.uint(2)==1,'CV_UNKNOWN'); n=c.uint(4)
    demand(n<=2**24,'LENGTH_CAP'); payload=c.take(n); c.end()
    obj=parse_json(payload,canonical=True)
    if expected=='tessera-v1/manifest':
        schema(obj,['alg','issuer','key_fp','sset','ver']); schema_alg(obj['alg'])
        demand(domain(obj['issuer']) and fp(obj['key_fp'],'kms') and obj['ver']=='map-v1','SCHEMA')
        demand(isinstance(obj['sset'],list) and len(obj['sset'])==1 and fp(obj['sset'][0],'gpg'),'SCHEMA')
    else:
        schema(obj,['common','signer']); schema(obj['signer'],['key_fp']); demand(fp(obj['signer']['key_fp']),'SCHEMA')
        co=obj['common']; schema(co,['alg','binding_forms','content','declared_issue_time','issuer','manifest_sha256','preamble_sha256','profile','spec','vectors_sha256'])
        schema_alg(co['alg']); schema(co['spec'],['id','sha256'])
        demand(domain(co['issuer']) and co['profile']==PROFILE,'SCHEMA'); utc(co['declared_issue_time'])
        demand(isinstance(co['spec']['id'],str) and re.fullmatch(r'[a-z0-9][a-z0-9._/-]{0,127}',co['spec']['id']),'SCHEMA')
        for value in [co['manifest_sha256'],co['preamble_sha256'],co['vectors_sha256'],co['spec']['sha256']]: demand(isinstance(value,str) and HEX.fullmatch(value),'SCHEMA')
        forms=co['binding_forms']; demand(isinstance(forms,list) and bool(forms) and all(isinstance(f,str) and re.fullmatch(r'[A-Z][A-Z0-9_]{0,31}',f) for f in forms),'SCHEMA')
        demand(forms==sorted(set(forms)),'SCHEMA')
    return obj

def subpackets(raw):
    c=Cursor(raw,'SIG_FORMAT'); out=[]
    while c.pos<len(raw):
        o=c.uint(1)
        if o<192: n=o
        elif o<255: n=((o-192)<<8)+c.uint(1)+192
        else:
            n=c.uint(4); demand(n>=16320,'SIG_FORMAT')
        demand(n>=1,'SIG_FORMAT'); p=c.take(n); out.append((p[0]&127,bool(p[0]&128),p[1:]))
    return out

@dataclass
class Signature:
    hashed: list
    unhashed: list
    prefix: bytes
    r: int
    s: int
    trailer: bytes

def registered_codecs(catalog_alg):
    """Profile §8: only the installed hybrid catalog registers its supplement."""
    return BASELINE_CODECS | (frozenset((HYBRID_ALG,)) if catalog_alg==HYBRID_ALG else frozenset())

def signature_rule(alg,slot,registry=BASELINE_CODECS):
    if alg not in registry: return 'opaque',65536
    if alg==HYBRID_ALG and slot=='kms': return 'R',3309
    if alg in (ALG,HYBRID_ALG): return 'O',1024
    return 'opaque',65536

def parse_signature(raw,alg=ALG,slot='kms',registry=BASELINE_CODECS):
    rule,cap=signature_rule(alg,slot,registry)
    demand(len(raw)>0,'SIG_EMPTY'); demand(len(raw)<=cap,'LENGTH_CAP')
    if rule=='opaque': return None
    if rule=='R':
        # HS §2: codec is length-only; sigDecode belongs to verification.
        demand(len(raw)==3309,'SIG_FORMAT'); return raw
    c=Cursor(raw); first=c.uint(1); demand(first in (0x88,0x89),'SIG_PACKET')
    n=c.uint(1 if first==0x88 else 2); demand(first==0x88 or n>255,'SIG_PACKET')
    body=c.take(n); c.end(); b=Cursor(body,'SIG_FORMAT'); demand(b.take(4)==b'\x04\x00\x13\x08','SIG_FORMAT')
    hlen=b.uint(2); h=b.take(hlen); header=body[:6+hlen]
    hashed=subpackets(h); unhashed=subpackets(b.take(b.uint(2))); prefix=b.take(2)
    def mpi():
        bits=b.uint(2); demand(1<=bits<=256,'SIG_FORMAT'); value=int.from_bytes(b.take((bits+7)//8),'big'); demand(value.bit_length()==bits,'SIG_FORMAT'); return value
    r=mpi(); s=mpi(); b.end('SIG_FORMAT')
    return Signature(hashed,unhashed,prefix,r,s,header+b'\x04\xff'+len(header).to_bytes(4,'big'))

def sig_policy(sig):
    # Rule R has no OpenPGP policy/trailer. FIPS gates run at verification,
    # mapping to SIG_INVALID or POSSESSION_INVALID, never SIG_POLICY.
    if isinstance(sig,bytes): return
    demand(sig is not None,'SIG_POLICY')
    creation=[d for t,_,d in sig.hashed if t==2]
    demand(len(creation)==1 and len(creation[0])==4,'SIG_POLICY')
    ids=[d for t,_,d in sig.hashed if t==16]; fps=[d for t,_,d in sig.hashed if t==33]
    demand(len(ids)<=1 and all(len(d)==8 for d in ids),'SIG_POLICY')
    demand(len(fps)<=1 and all(len(d)==21 and d[0]==4 for d in fps),'SIG_POLICY')
    demand(not ids or not fps or ids[0]==fps[0][-8:],'SIG_POLICY')
    for t,critical,_ in sig.hashed: demand(t!=3 and (t in (2,16,33) or not critical),'SIG_POLICY')
    demand(1<=sig.r<N and 1<=sig.s<N,'SIG_POLICY')

def point(raw):
    demand(len(raw)==65 and raw[0]==4,'KEY_FORMAT')
    x=int.from_bytes(raw[1:33],'big'); y=int.from_bytes(raw[33:],'big')
    demand(x<P and y<P and (y*y-(x*x*x-3*x+B))%P==0,'KEY_FORMAT')
    try: return ec.EllipticCurvePublicNumbers(x,y,ec.SECP256R1()).public_key()
    except ValueError: raise Fault('KEY_FORMAT') from None

def public_key(raw,slot,alg=ALG):
    if slot=='kms':
        if alg==HYBRID_ALG:
            # HS §3 / RFC 9881 §§2,4: exact DER, absent parameters, zero
            # unused bits. Every 1952-byte pkDecode input is well formed.
            demand(len(raw)==1974 and raw[:22]==MLDSA65_SPKI,'KEY_FORMAT')
            return mldsa.MLDSA65PublicKey.from_public_bytes(raw[22:])
        demand(len(raw)==91 and raw[:26]==SPKI,'KEY_FORMAT'); return point(raw[26:])
    demand(len(raw)==82 and raw[0]==4 and raw[5:17]==GPG_PREFIX,'KEY_FORMAT'); return point(raw[17:])

def mldsa65_encoding_valid(sig):
    """FIPS 204 Algorithms 21, 27, 8; verification gates, not rule-R codec."""
    if len(sig)!=3309: return False
    # HintBitUnpack: counts bounded and nondecreasing; strict order within
    # each polynomial (including no duplicates); unused indices all zero.
    hints=sig[3248:]; start=0
    for end in hints[55:]:
        if not start<=end<=55: return False
        indices=hints[start:end]
        if any(a>=b for a,b in zip(indices,indices[1:])): return False
        start=end
    if any(hints[start:55]): return False
    # BitUnpack(z, gamma1-1, gamma1), 20 little-endian bits/coefficient.
    # ML-DSA-65: gamma1=2^19, beta=196; strict infinity-norm bound.
    bits=int.from_bytes(sig[48:3248],'little')
    for _ in range(5*256):
        coefficient=(1<<19)-(bits&((1<<20)-1))
        if abs(coefficient)>=(1<<19)-196: return False
        bits>>=20
    return True

def signature_verifies(document,sig,key):
    if isinstance(sig,bytes):
        if not mldsa65_encoding_valid(sig): return False
        try:
            # Algorithm 3 applies 00 00 itself: pass exact F, not mu or M'.
            key.verify(sig,document,context=b''); return True
        except (InvalidSignature,ValueError): return False
    digest=sha(document+sig.trailer)
    if digest[:2]!=sig.prefix: return False
    try: key.verify(utils.encode_dss_signature(sig.r,sig.s),digest,ec.ECDSA(utils.Prehashed(hashes.SHA256()))); return True
    except (InvalidSignature,ValueError): return False

def read_anchor(raw,registry=BASELINE_CODECS):
    c=Cursor(raw); tag(c,'tessera-v1/receipt-anchor-sig'); demand(c.uint(1)==2,'ANCHOR_COUNT'); out=[]
    for slot in ('kms','gpg'):
        n=c.uint(4); demand(n<=2**24+64,'LENGTH_CAP'); f=c.take(n); obj=read_frame(f,'tessera-v1/attest')
        n=c.uint(4); demand(n>0,'SIG_EMPTY'); demand(n<=signature_rule(obj['common']['alg'],slot,registry)[1],'LENGTH_CAP')
        s=c.take(n); parsed=parse_signature(s,obj['common']['alg'],slot,registry); out.append((f,obj,s,parsed))
    c.end(); return out
