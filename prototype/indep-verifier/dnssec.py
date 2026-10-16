"""Wire snapshots and explicit RFC 4034/4035 V1 candidate classification."""
import hashlib
import re
from dataclasses import dataclass,field
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec,rsa,padding,utils
from codec import Cursor,Fault,demand,point,utc,HEX


def name(raw,pos):
    start=pos; labels=[]
    while True:
        demand(pos<len(raw),'SNAPSHOT_FORMAT'); n=raw[pos]; pos+=1
        demand(n<=63 and pos+n<=len(raw),'SNAPSHOT_FORMAT')
        if n==0: break
        label=raw[pos:pos+n]; demand(all(not 65<=b<=90 for b in label),'SNAPSHOT_FORMAT')
        labels.append(label); pos+=n
    demand(pos-start<=255,'SNAPSHOT_FORMAT'); return tuple(labels),pos

def wire(labels): return b''.join(bytes([len(l)])+l for l in labels)+b'\x00'
def below(child,parent): return len(child)>len(parent) and (not parent or child[-len(parent):]==parent)
def keytag(raw):
    acc=sum(b<<(8 if i%2==0 else 0) for i,b in enumerate(raw)); acc+=(acc>>16)&0xffff; return acc&0xffff

@dataclass
class RR:
    owner: tuple
    type: int
    ttl: int
    data: bytes
    offset: int
@dataclass
class RRSig:
    covered:int
    alg:int
    labels:int
    ttl:int
    expiration:int
    inception:int
    tag:int
    signer:tuple
    signature:bytes
    prefix:bytes
    raw:bytes
    def order(self,key=b''):
        return (self.tag,self.inception,self.expiration,self.signature,self.raw,key)

def parse_rrsig(raw):
    try:
        c=Cursor(raw,'DNSSEC_FORMAT'); covered=c.uint(2); alg=c.uint(1); labels=c.uint(1); ttl=c.uint(4)
        expiration=c.uint(4); inception=c.uint(4); tag=c.uint(2)
        signer,end=name(raw,c.pos); prefix=raw[:end]; signature=raw[end:]
        demand(bool(signature),'DNSSEC_FORMAT')
        return RRSig(covered,alg,labels,ttl,expiration,inception,tag,signer,signature,prefix,raw)
    except Fault: raise Fault('DNSSEC_FORMAT') from None

def canonical_signer(raw):
    """Reject observable noncanonical names, leaving other truncation candidate-local."""
    pos=18
    while pos<len(raw):
        n=raw[pos]; pos+=1
        demand(n&0xc0!=0xc0,'SNAPSHOT_FORMAT')
        if n==0 or n>63: return
        label=raw[pos:pos+n]
        demand(all(not 65<=b<=90 for b in label),'SNAPSHOT_FORMAT')
        if len(label)<n: return
        pos+=n


def rrsig_order(raw,key=b''):
    """G35 with a fallback only for individually unobtainable fields."""
    def uint(start,size):
        return int.from_bytes(raw[start:start+size],'big') if len(raw)>=start+size else 0
    try: _,end=name(raw,18); signature=raw[end:]
    except Fault: signature=b''
    return (uint(16,2),uint(12,4),uint(8,4),signature,raw,key)

@dataclass
class Group:
    owner:tuple
    type:int
    rr:list=field(default_factory=list)
    sigs:list=field(default_factory=list)
@dataclass
class Snapshot:
    groups:list
    zones:list
    txt:Group|None
    wildcard:bool
    def group(self,owner,t): return next((g for g in self.groups if g.owner==owner and g.type==t),None)

def parse_snapshot(raw):
    demand(1<=len(raw)<=2**24,'LENGTH_CAP'); c=Cursor(raw,'SNAPSHOT_FORMAT'); records=[]; seen=set()
    while c.pos<len(raw):
        offset=c.pos; owner,end=name(raw,c.pos); c.pos=end
        t=c.uint(2); klass=c.uint(2); ttl=c.uint(4); data=c.take(c.uint(2))
        demand(klass==1 and t in (16,43,46,48),'SNAPSHOT_FORMAT')
        key=(owner,t,data); demand(key not in seen,'SNAPSHOT_FORMAT'); seen.add(key)
        records.append(RR(owner,t,ttl,data,offset))
    groups=[]; wildcard=False
    for rr in records:
        if rr.type==46:
            canonical_signer(rr.data)
            # Covered type is the minimal grouping discriminator. Undecodable RDATA
            # attaches to the preceding group, then fails DNSSEC_FORMAT locally.
            t=int.from_bytes(rr.data[:2],'big') if len(rr.data)>=2 else (groups[-1].type if groups else 48)
            demand(t in (16,43,48),'SNAPSHOT_FORMAT')
        else: t=rr.type
        if not groups or (groups[-1].owner,groups[-1].type)!=(rr.owner,t):
            demand(not any((g.owner,g.type)==(rr.owner,t) for g in groups),'SNAPSHOT_FORMAT'); groups.append(Group(rr.owner,t))
        g=groups[-1]
        if rr.type==46:
            g.sigs.append(rr)
            if len(rr.data)>=4: wildcard|=rr.data[3]<len(rr.owner)
            try:
                sig=parse_rrsig(rr.data); wildcard|=sig.labels<len(rr.owner)
            except Fault: pass
        else:
            demand(not g.sigs,'SNAPSHOT_FORMAT'); g.rr.append(rr)
    zones={()}
    for g in groups:
        if g.type in (43,48): zones.add(g.owner)
        for rr in g.sigs:
            try: zones.add(parse_rrsig(rr.data).signer)
            except Fault: pass
        demand(not g.rr or len({r.ttl for r in g.rr})==1,'SNAPSHOT_FORMAT')
        demand([r.data for r in g.rr]==sorted(r.data for r in g.rr),'SNAPSHOT_FORMAT')
        sortable=[]
        for r in g.sigs:
            try: sortable.append(parse_rrsig(r.data).order())
            except Fault: sortable.append(rrsig_order(r.data))
        demand(sortable==sorted(sortable),'SNAPSHOT_FORMAT')
    zones=sorted(zones,key=lambda z:(len(z),z))
    demand(all(below(zones[i],zones[i-1]) for i in range(1,len(zones))),'SNAPSHOT_FORMAT')
    rank={}; rank[((),48)]=0
    for i,z in enumerate(zones[1:]): rank[(z,43)]=1+2*i; rank[(z,48)]=2+2*i
    ranks=[]; txt=None
    for g in groups:
        if g.type==16:
            demand(txt is None,'SNAPSHOT_FORMAT'); txt=g; ranks.append(2*len(zones)+1)
        else:
            demand((g.owner,g.type) in rank,'SNAPSHOT_FORMAT'); ranks.append(rank[(g.owner,g.type)])
        for r in g.sigs:
            try: sig=parse_rrsig(r.data)
            except Fault: continue
            if g.type==48: demand(sig.signer==g.owner,'SNAPSHOT_FORMAT')
            elif g.type==43:
                idx=zones.index(g.owner); demand(idx>0 and sig.signer==zones[idx-1],'SNAPSHOT_FORMAT')
            else: demand(sig.signer in zones,'SNAPSHOT_FORMAT')
    demand(ranks==sorted(ranks) and len(set(ranks))==len(ranks),'SNAPSHOT_FORMAT')
    return Snapshot(groups,zones,txt,wildcard)

def rrsig_time(inception,expiration,evaluation):
    def resolve(v):
        delta=(v-evaluation)%(2**32)
        if delta==2**31: raise Fault('RRSIG_TIME_AMBIGUOUS')
        if delta>2**31: delta-=2**32
        return evaluation+delta
    try: start=resolve(inception); end=resolve(expiration)
    except Fault as e: return e.code
    if start>end: return 'RRSIG_INTERVAL_REVERSED'
    if not start<=evaluation<=end: return 'RRSIG_NOT_VALID_AT_EVAL_TIME'
    return None

def dnskey(raw):
    demand(len(raw)>=4,'DNSSEC_FORMAT'); flags=int.from_bytes(raw[:2],'big'); protocol=raw[2]; alg=raw[3]
    demand(flags&256 and not flags&128 and protocol==3,'DNSSEC_KEY_MISMATCH')
    if alg==13:
        demand(len(raw)==68,'DNSSEC_FORMAT')
        try: return alg,point(b'\x04'+raw[4:])
        except Fault: raise Fault('DNSSEC_FORMAT') from None
    if alg==8:
        c=Cursor(raw[4:],'DNSSEC_FORMAT'); n=c.uint(1)
        if n==0:
            n=c.uint(2); demand(n>=256,'DNSSEC_FORMAT')
        demand(n>0,'DNSSEC_FORMAT'); exponent=c.take(n); modulus=c.take(len(c.data)-c.pos)
        demand(bool(modulus) and exponent[0]!=0 and modulus[0]!=0,'DNSSEC_FORMAT')
        demand(512<=int.from_bytes(modulus,'big').bit_length()<=4096,'DNSSEC_FORMAT')
        try: return alg,rsa.RSAPublicNumbers(int.from_bytes(exponent,'big'),int.from_bytes(modulus,'big')).public_key()
        except ValueError: raise Fault('DNSSEC_FORMAT') from None
    raise Fault('DNSSEC_ALGORITHM_UNSUPPORTED')

def signed_data(group,sig):
    return sig.prefix+b''.join(wire(group.owner)+group.type.to_bytes(2,'big')+b'\x00\x01'+sig.ttl.to_bytes(4,'big')+len(rr.data).to_bytes(2,'big')+rr.data for rr in group.rr)

def verify_rr(group,sig,key):
    alg,pub=dnskey(key); demand(alg==sig.alg,'DNSSEC_RRSIG_METADATA')
    demand(sig.covered==group.type and sig.labels==len(group.owner) and (group.owner==sig.signer or below(group.owner,sig.signer)),'DNSSEC_RRSIG_METADATA')
    data=signed_data(group,sig)
    try:
        if alg==8:
            demand(len(sig.signature)==(pub.key_size+7)//8,'DNSSEC_FORMAT')
            pub.verify(sig.signature,data,padding.PKCS1v15(),hashes.SHA256())
        else:
            demand(len(sig.signature)==64,'DNSSEC_FORMAT')
            r=int.from_bytes(sig.signature[:32],'big'); s=int.from_bytes(sig.signature[32:],'big')
            pub.verify(utils.encode_dss_signature(r,s),data,ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature: return False
    except ValueError: raise Fault('DNSSEC_FORMAT') from None

@dataclass
class Auth:
    status:str
    reason:str|None=None
    witness:RRSig|None=None
    rank:int=99
    order:tuple=()

def interval(entry,t,as_of,ksk=False):
    start=utc(entry['signing_start']); end=entry['signing_end']
    if end is None:
        if t>as_of and t>=start: return 'horizon'
        return 'pass' if start<=t<=as_of else 'outside'
    stop=utc(end)+(int(entry['reliance_lifetime_s']) if ksk else 0)
    return 'pass' if start<=t<=stop else 'outside'

def root_auth(group,config,t):
    if group is None or not group.rr or not group.sigs: return Auth('unknown','NO_TRUSTED_KSK_USABLE')
    outcomes=[]; eligible=[]
    for rr in group.sigs:
        try: sig=parse_rrsig(rr.data)
        except Fault:
            if len(rr.data)>=18 and any(int(e['key_tag'])==int.from_bytes(rr.data[16:18],'big') for e in config['root_ksks']):
                outcomes.append((4,rrsig_order(rr.data),'DNSSEC_FORMAT'))
            continue
        for entry in config['root_ksks']:
            key=entry['_key']
            if sig.tag!=int(entry['key_tag']): continue
            order=sig.order(key)
            try:
                demand(sig.signer==() and sig.alg==key[3] and key in [r.data for r in group.rr],'DNSSEC_RRSIG_METADATA')
                good=verify_rr(group,sig,key)
            except Fault as e: outcomes.append((4,order,e.code)); continue
            if not good: outcomes.append((4,order,'TRUSTED_KSK_SIGNATURE_INVALID')); continue
            time=rrsig_time(sig.inception,sig.expiration,t)
            if time: outcomes.append((3,order,time)); continue
            state=interval(entry,t,utc(config['as_of']),True)
            if state=='pass': eligible.append((order,sig))
            elif state=='horizon': outcomes.append((1,order,'TRUST_HORIZON'))
            else: outcomes.append((2,order,'KSK_OUTSIDE_RELIANCE_PERIOD'))
    if eligible: return Auth('pass',witness=min(eligible,key=lambda x:x[0])[1])
    if outcomes:
        rank,_,code=min(outcomes,key=lambda x:(x[0],x[1])); return Auth('unknown' if rank==1 else 'invalid',code)
    return Auth('unknown','NO_TRUSTED_KSK_USABLE')

def ds_matches(ds,owner,key):
    if len(ds)<4: return False
    if int.from_bytes(ds[:2],'big')!=keytag(key) or len(key)<4 or ds[2]!=key[3]: return False
    if ds[3] not in (2,4) or ds[2] not in (8,13): return None
    expected=hashlib.sha256(wire(owner)+key).digest() if ds[3]==2 else hashlib.sha384(wire(owner)+key).digest()
    return ds[4:]==expected

def group_auth(group,signer_keys,parent,t,ds_group=None):
    if group is None or not group.rr or not group.sigs or signer_keys is None or not signer_keys.rr:
        return Auth('unknown','DNS_EVIDENCE_MISSING')
    candidates=[]; local=[]; passes=[]; unsupported=False; matched_ds=False
    keys=[r.data for r in signer_keys.rr]
    if group.type==48 and parent.status=='pass' and ds_group:
        unsupported=any(ds_matches(ds.data,group.owner,key) is None for ds in ds_group.rr for key in keys)
    for rr in group.sigs:
        try: sig=parse_rrsig(rr.data)
        except Fault:
            candidates.append((6,rrsig_order(rr.data),'DNSSEC_FORMAT')); continue
        matching=[key for key in keys if len(key)>=4 and key[3]==sig.alg and keytag(key)==sig.tag]
        if sig.signer!=signer_keys.owner or sig.covered!=group.type or sig.labels>len(group.owner):
            candidates.append((5,sig.order(),'DNSSEC_RRSIG_METADATA')); continue
        if sig.alg not in (8,13):
            if parent.status=='pass' and matching: unsupported=True
            continue
        eligible=[]
        for key in matching:
            try: dnskey(key); eligible.append(key)
            except Fault as e: candidates.append((6 if e.code=='DNSSEC_FORMAT' else 3,sig.order(key),e.code))
        if not eligible:
            if not matching: candidates.append((3,sig.order(),'DNSSEC_KEY_MISMATCH'))
            continue
        for key in eligible:
            order=sig.order(key); authorized=True
            if group.type==48:
                statuses=[ds_matches(r.data,group.owner,key) for r in (ds_group.rr if ds_group else [])]
                if parent.status=='pass' and None in statuses: unsupported=True
                authorized=True in statuses; matched_ds|=authorized
            try: good=verify_rr(group,sig,key)
            except Fault as e: candidates.append((5 if e.code=='DNSSEC_RRSIG_METADATA' else 6,order,e.code)); continue
            if not good: candidates.append((2,order,'DNSSEC_SIGNATURE_INVALID')); continue
            time=rrsig_time(sig.inception,sig.expiration,t)
            if time: candidates.append((1,order,time)); continue
            local.append((order,sig))
            if parent.status=='pass' and authorized: passes.append((order,sig))
    if passes: return Auth('pass',witness=min(passes,key=lambda x:x[0])[1])
    if unsupported: return Auth('unknown','DNSSEC_ALGORITHM_UNSUPPORTED')
    if parent.status!='pass' and local: return Auth('unknown')
    if group.type==48 and parent.status=='pass' and not matched_ds: candidates.append((4,(0,0,0,b'',b'',b''),'DNSKEY_DS_MISMATCH'))
    if candidates:
        rank,order,code=min(candidates,key=lambda x:(x[0],x[1])); return Auth('invalid',code,rank=rank,order=order)
    # No selected supported witness can complete this path.
    return Auth('unknown','DNS_EVIDENCE_MISSING')

def validate_snapshot(snapshot,config,t):
    outcomes=[]; key_auth={}; root=snapshot.group((),48)
    result=root_auth(root,config,t); outcomes.append(result); key_auth[()]=result
    for i,z in enumerate(snapshot.zones[1:],1):
        parent=snapshot.zones[i-1]; ds=snapshot.group(z,43); keys=snapshot.group(z,48)
        ds_auth=group_auth(ds,snapshot.group(parent,48),key_auth.get(parent,Auth('unknown')),t)
        outcomes.append(ds_auth)
        result=group_auth(keys,keys,ds_auth,t,ds); outcomes.append(result); key_auth[z]=result
    txt=snapshot.txt
    if txt is None: outcomes.append(Auth('unknown','DNS_EVIDENCE_MISSING'))
    else:
        # Ancestor TXT witnesses can use different zones. Aggregate once, across all.
        txt_out=[]
        for z in snapshot.zones:
            sigs=[]
            for rr in txt.sigs:
                try:
                    if parse_rrsig(rr.data).signer==z: sigs.append(rr)
                except Fault: sigs.append(rr)
            if sigs:
                txt_out.append(group_auth(Group(txt.owner,16,txt.rr,sigs),snapshot.group(z,48),key_auth[z],t))
        valid=[a for a in txt_out if a.status=='pass']
        if valid: outcomes.append(min(valid,key=lambda a:a.witness.order()))
        elif any(a.status=='unknown' and a.reason=='DNS_EVIDENCE_MISSING' for a in txt_out): outcomes.append(Auth('unknown','DNS_EVIDENCE_MISSING'))
        elif any(a.status=='unknown' and a.reason=='DNSSEC_ALGORITHM_UNSUPPORTED' for a in txt_out): outcomes.append(Auth('unknown','DNSSEC_ALGORITHM_UNSUPPORTED'))
        elif any(a.status=='unknown' and a.reason is None for a in txt_out): outcomes.append(Auth('unknown'))
        elif txt_out: outcomes.append(min(txt_out,key=lambda a:(a.rank,a.order)))
        else: outcomes.append(Auth('unknown','DNS_EVIDENCE_MISSING'))
    return outcomes

FIELDS=['v','profile','kms','gpg','issuance-not-before','issuance-not-after']
def txt_value(rdatas):
    demand(len(rdatas)==1,'DNS_RRSET'); raw=rdatas[0]; c=Cursor(raw,'DNS_RDATA'); strings=[]
    while c.pos<len(raw): strings.append(c.take(c.uint(1)))
    demand(len(strings)==1,'DNS_STRINGS'); value=strings[0]
    demand(all(0x21<=b<=0x7e for b in value),'DNS_SYNTAX')
    fields=value.decode('ascii').split(';'); pairs=[]
    for f in fields:
        demand(f.count('=')==1,'DNS_SYNTAX'); k,v=f.split('='); demand(re.fullmatch(r'[a-z][a-z-]*',k) and v,'DNS_SYNTAX'); pairs.append((k,v))
    names=[k for k,_ in pairs]
    demand(bool(pairs) and pairs[0]==('v','tessera1') and names.count('v')==1,'DNS_VERSION')
    demand(all(k in FIELDS for k in names),'DNS_FIELD_UNKNOWN')
    for k in names:
        demand(names.count(k)==1,'DNS_SLOT_DUPLICATE' if k in ('kms','gpg') else 'DNS_FIELD_DUPLICATE')
    demand('kms' in names and 'gpg' in names,'DNS_SLOT_MISSING')
    demand(all(k in names for k in ('profile','issuance-not-before','issuance-not-after')),'DNS_FIELD_MISSING')
    demand(names==FIELDS,'DNS_ORDER'); data=dict(pairs); demand(data['profile']=='tessera-v1-strict','DNS_PROFILE')
    demand(HEX.fullmatch(data['kms']) and HEX.fullmatch(data['gpg']),'DNS_VALUE')
    try: start=utc(data['issuance-not-before']); end=utc(data['issuance-not-after'])
    except Fault: raise Fault('DNS_VALUE') from None
    demand(end>start,'DNS_WINDOW'); demand(end-start<=7776000,'DNS_WINDOW_LENGTH')
    demand(len(value)==255,'DNS_VALUE'); data['_raw']=value; data['_start']=start; data['_end']=end; return data
