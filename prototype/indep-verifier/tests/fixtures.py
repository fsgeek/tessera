"""Locally generated evidence, not imported Tessera vectors or fixture formats."""
import base64
import hashlib
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec,utils,mldsa
from cryptography.hazmat.primitives import serialization
from codec import ALG,PROFILE,SPKI,GPG_PREFIX,frame,jcs,sha,shahex,utc
from anchors import MAGIC,BTC,sha256d
from dnssec import wire,keytag
from git_channel import object_id

def enc(raw): return base64.b64encode(raw).decode()
def varuint(n):
    out=b''
    while n>=128: out+=bytes([(n&127)|128]); n>>=7
    return out+bytes([n])
def varbytes(raw): return varuint(len(raw))+raw
def pointbytes(key):
    p=key.public_key().public_numbers(); return b'\x04'+p.x.to_bytes(32,'big')+p.y.to_bytes(32,'big')
def gpgkey(key): return b'\x04'+bytes(4)+GPG_PREFIX+pointbytes(key)
def mpi(n): return n.bit_length().to_bytes(2,'big')+n.to_bytes((n.bit_length()+7)//8,'big')
def sign(key,document,hashed=b'\x05\x02'+bytes(4),unhashed=b''):
    head=b'\x04\x00\x13\x08'+len(hashed).to_bytes(2,'big')+hashed
    trailer=head+b'\x04\xff'+len(head).to_bytes(4,'big'); digest=sha(document+trailer)
    der=key.sign(digest,ec.ECDSA(utils.Prehashed(hashes.SHA256()))); r,s=utils.decode_dss_signature(der)
    body=head+len(unhashed).to_bytes(2,'big')+unhashed+digest[:2]+mpi(r)+mpi(s)
    return (b'\x88'+bytes([len(body)]) if len(body)<=255 else b'\x89'+len(body).to_bytes(2,'big'))+body

def rr(owner,typ,data,ttl=3600): return wire(owner)+typ.to_bytes(2,'big')+b'\x00\x01'+ttl.to_bytes(4,'big')+len(data).to_bytes(2,'big')+data

def dnskey(key,flags=257): return flags.to_bytes(2,'big')+b'\x03\x0d'+pointbytes(key)[1:]
def rrset(owner,typ,rdatas,key,keydata,signer,t):
    prefix=typ.to_bytes(2,'big')+b'\x0d'+bytes([len(owner)])+(3600).to_bytes(4,'big')+(t+86400).to_bytes(4,'big')+(t-86400).to_bytes(4,'big')+keytag(keydata).to_bytes(2,'big')+wire(signer)
    data=prefix+b''.join(rr(owner,typ,r) for r in sorted(rdatas)); r,s=utils.decode_dss_signature(key.sign(data,ec.ECDSA(hashes.SHA256())))
    return b''.join(rr(owner,typ,r) for r in sorted(rdatas))+rr(owner,46,prefix+r.to_bytes(32,'big')+s.to_bytes(32,'big'))

def stamp(target,height,t,headers,pins,confirmation=None):
    digest=sha(target)
    # Append/prepend builds a transaction containing the current OTS message.
    prefix=bytes(4)+b'\x01'+bytes(36)+b'\x00'+bytes(4)+b'\x01'+bytes(8)+b'\x22\x6a\x20'
    suffix=bytes(4); transaction=prefix+digest+suffix; root=sha256d(transaction)
    ops=b'\xf1'+varbytes(prefix)+b'\xf0'+varbytes(suffix)+b'\x08\x08'
    proof=MAGIC+b'\x01\x08'+digest+ops+b'\x00'+BTC+varbytes(varuint(height))
    prev=bytes(32)
    for i in range(height,height+6):
        when=t if i==height or confirmation is None else confirmation
        header=b'\x01\x00\x00\x00'+prev+(root if i==height else bytes(32))+when.to_bytes(4,'little')+bytes(8)
        headers[str(i)]=header.hex(); pins[str(i)]=sha256d(header)[::-1].hex(); prev=sha256d(header)
    return proof,sha256d(transaction)[::-1].hex()

def make_fixture(common_overrides=None, manifest_overrides=None, gpg_common_overrides=None,
                 window_start='2026-10-01T00:00:00Z',window_end='2026-11-01T00:00:00Z',objects_overrides=None,
                 hybrid=False,kms_signer=None,kms_possession_signer=None):
    alg='KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256' if hybrid else ALG
    t=utc('2026-10-14T12:00:00Z'); kms=mldsa.MLDSA65PrivateKey.generate() if hybrid else ec.generate_private_key(ec.SECP256R1()); gpg=ec.generate_private_key(ec.SECP256R1())
    repo=ec.generate_private_key(ec.SECP256R1()); root=ec.generate_private_key(ec.SECP256R1()); zone=ec.generate_private_key(ec.SECP256R1())
    def external_mu(key,document):
        tr=hashlib.shake_256(key.public_key().public_bytes_raw()).digest(64)
        return key.sign_mu(hashlib.shake_256(tr+b'\x00\x00'+document).digest(64))
    kms_signer=kms_signer or (external_mu if hybrid else sign)
    kms_possession_signer=kms_possession_signer or kms_signer
    keys={'kms':kms.public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo) if hybrid else SPKI+pointbytes(kms),'gpg':gpgkey(gpg)}
    fps={'kms':'spki-sha256:'+shahex(keys['kms']),'gpg':'gpg-sha256:'+shahex(keys['gpg'])}
    manifest_value={'alg':alg,'issuer':'wamason.com','key_fp':fps['kms'],'sset':[fps['gpg']],'ver':'map-v1'}
    manifest_value.update(manifest_overrides or {})
    manifest=frame('tessera-v1/manifest',jcs(manifest_value))
    objects={'spec':b'independent test spec','vectors':b'independent test vectors','preamble':b'independent test preamble','dependency_manifest':b'independent test dependency manifest'}
    objects.update(objects_overrides or {})
    common={'alg':alg,'binding_forms':['STMT_DIRECT'],'content':{'contract':'opaque'},'declared_issue_time':'2026-10-14T12:00:00Z','issuer':'wamason.com','manifest_sha256':shahex(manifest),'preamble_sha256':shahex(objects['preamble']),'profile':PROFILE,'spec':{'id':'tessera-v1-strict/verification-spec/1','sha256':shahex(objects['spec'])},'vectors_sha256':shahex(objects['vectors'])}
    common.update(common_overrides or {})
    frames=[frame('tessera-v1/attest',jcs({'common':common if s=='kms' else {**common,**(gpg_common_overrides or {})},'signer':{'key_fp':fps[s]}})) for s in ('kms','gpg')]
    signatures=[kms_signer(kms,frames[0]),sign(gpg,frames[1])]
    anchor=b'\x1d'+b'tessera-v1/receipt-anchor-sig'+b'\x02'
    for f,s in zip(frames,signatures): anchor+=len(f).to_bytes(4,'big')+f+len(s).to_bytes(4,'big')+s
    value=('v=tessera1;profile='+PROFILE+';kms='+fps['kms'].split(':')[1]+';gpg='+fps['gpg'].split(':')[1]+';issuance-not-before='+window_start+';issuance-not-after='+window_end).encode()
    root_data=dnskey(root); zone_data=dnskey(zone); z=(b'wamason',b'com'); owner=(b'_tessera-v1',)+z
    ds=keytag(zone_data).to_bytes(2,'big')+b'\x0d\x02'+sha(wire(z)+zone_data)
    body=rrset((),48,[root_data],root,root_data,(),t)+rrset(z,43,[ds],root,root_data,(),t)+rrset(z,48,[zone_data],zone,zone_data,z,t)+rrset(owner,16,[bytes([255])+value],zone,zone_data,z,t)
    blob=value; sub=b'100644 key-assertion\x00'+bytes.fromhex(object_id('blob',blob)); tree=b'40000 tessera-v1\x00'+bytes.fromhex(object_id('tree',sub))
    unsigned=b'tree '+object_id('tree',tree).encode()+b'\nauthor Test <test@example.com> 0 +0000\ncommitter Test <test@example.com> 0 +0000\n\nassertion'
    armor=b'-----BEGIN PGP SIGNATURE-----\n\n'+base64.b64encode(sign(repo,unsigned))+b'\n-----END PGP SIGNATURE-----'
    # armor lines <=76, and git continuation framing
    siglines=armor.split(b'\n'); encoded=siglines[2]; siglines=siglines[:2]+[encoded[i:i+76] for i in range(0,len(encoded),76)]+siglines[3:]
    header,message=unsigned.split(b'\n\n',1); commit=header+b'\ngpgsig '+siglines[0]+b'\n'+b'\n'.join(b' '+x for x in siglines[1:])+b'\n\n'+message
    headers={}; pins={}
    receipt_ots,txid=stamp(anchor,120,t,headers,pins)
    envelope=b'\x1a'+b'tessera-v1/dnssec-snapshot'+len(body).to_bytes(4,'big')+body
    dns_ots,_=stamp(envelope,110,t,headers,pins)
    git_ots,_=stamp((object_id('commit',commit)+'\n').encode(),100,t+10,headers,pins)
    layer={'a_sig':enc(anchor),'manifest':enc(manifest),'possession':{'kms':enc(kms_possession_signer(kms,manifest)),'gpg':enc(sign(gpg,manifest))},'keys':{s:enc(k) for s,k in keys.items()},'receipt_anchor':{'ots':enc(receipt_ots),'txid':txid},'headers':headers,'dns':{'ots':enc(dns_ots),'snapshot_body':enc(body)},'git':{'blob':enc(blob),'commit':enc(commit),'trees':[enc(tree),enc(sub)],'object_format':'sha1','ots':enc(git_ots)},**{k:enc(v) for k,v in objects.items()}}
    sources=[{'description':'generated synthetic key','sha256':'0'*64,'uri':'urn:independent-test'}]
    trust={'format':'tessera-v1-trust/1','profile':PROFILE,'version':'1','previous_sha256':'0'*64,'as_of':'2026-10-20T00:00:00Z','issuer_domain':'wamason.com','header_pins':pins,
           'root_ksks':[{'name':'test-root','key_tag':str(keytag(root_data)),'algorithm':'13','dnskey_rdata':enc(root_data),'ds_sha256':shahex(b'\x00'+root_data),'signing_start':'2026-01-01T00:00:00Z','signing_end':None,'reliance_lifetime_s':'1814400','publication':None,'revocation':None,'sources':sources}],
           'repository_keys':[{'domain':'wamason.com','key':enc(gpgkey(repo)),'signing_start':'2026-01-01T00:00:00Z','signing_end':None,'sources':sources}]}
    entry={'spec_sha256':shahex(objects['spec']),'vectors_sha256':shahex(objects['vectors']),'preamble_sha256':shahex(objects['preamble']),'dependency_manifest_sha256':shahex(objects['dependency_manifest']),'alg':alg,'alg_prohibited':[],'binding_forms':['STMT_DIRECT'],'issuer_domain':'wamason.com','delta_s':'259200','epsilon_s':'86400','k':'6','dnssec_algorithms':['8','13'],'ds_digest_types':['2','4']}
    catalog={'format':'tessera-v1-independent-catalog/1','entries':[entry]}
    return {'layers':[layer],'profile':PROFILE},trust,catalog
